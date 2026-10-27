# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Write the specimen page of each font, and the README's sample cells that link to it.

    .venv/bin/python tools/specimen_pages.py            # write the pages, their images and the README cells
    .venv/bin/python tools/specimen_pages.py --check    # fail where any of them is missing or out of date

Every family of fonts.json that is its own font file has a page, ``specimens/<class>.md``,
with its images in ``specimens/pages/``:

- ``<class>-letters.png``: every character the font draws, grouped as its chart groups
  them; Teng Chou and Khelathi Zethu Glyphs show a sample, and their pages link the chart;
- ``<class>-marks.png``: a sample of the marks set on a few letters, where the script has marks;
- ``<class>-passage.png``: a passage of thalorna in the script, its lines numbered, set
  right to left for a right-to-left font and in columns for Teng Chou. The page gives
  each line's English with its roman spelling under it.

Chalish Pilam Common's glyphs record meaning rather than spelling. Its page shows the
committed sheets of ``specimens/chalish-pilam/`` (the glyphs and the night's entry set
through the font) and lists the entry phrase by phrase. Chalish Pilam Ceremonial's page
shows the canon sheet of the ceremonial hand and the passage that
``tools/chalish-pilam/ceremonial_passage.py`` renders through the font, both committed in
``specimens/chalish-pilam/``, with the passage's glyph codes block by block and its English.

Khelathi Zethu Glyphs' page also shows the Khelathu banner, ``<class>-banner.webp``,
with its English text.

The texts are ``specimens/texts.json``: per family its source, and each line's glyph
codes (``tools/codes/<script>.json``, with ``U+0020`` for the space), roman spelling and
English, and each mark sample's glyph codes.

Every line is shaped by HarfBuzz from the built font. ``--check`` renders every image
and page afresh in memory and fails where a file is missing, differs from what the
fonts and ``texts.json`` give, or where a README sample cell is not the absolute image
URL linked to its page.
"""

import argparse
import hashlib
import io
import json
import sys
from pathlib import Path

import uharfbuzz as hb
from PIL import Image, ImageChops, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
import codes  # noqa: E402
from charts import FOLDERS, GROUPS  # noqa: E402
from render import Renderer, Shaped  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SPECIMENS = ROOT / "specimens"
PAGES = SPECIMENS / "pages"
TEXTS = SPECIMENS / "texts.json"
README = ROOT / "README.md"
RAW = "https://raw.githubusercontent.com/HeroicLands/fonts/main/specimens/readme"

PAPER = (255, 255, 255)
INK = (22, 20, 18)
GREY = (110, 104, 96)
RULE = (214, 206, 192)
SIZE = 56  # px per em for letters, marks and passages: a Latin label at this size reads at the same scale
SIGN_SIZE = 88  # Khelathi Zethu Glyphs' signs fill a quadrat, so their sample is set larger
LABEL = 18
MARGIN = 40
WIDTH = 1400

CHALISH = "hl-chalish-pilam-common"
CEREMONIAL = "hl-chalish-pilam-ceremonial"
# The families whose pages show committed sheets rather than images this tool renders.
COMMITTED = {CHALISH, CEREMONIAL}

# The pages' sample of Teng Chou: its first characters and syllables, in code point order.
TENG_CHOU_SAMPLE = {"character": 40, "syllable": 16}


# -- the font and its rows ------------------------------------------------------


def manifest() -> list[dict]:
    """The families that are their own font file, in fonts.json order."""
    seen, out = set(), []
    for family in json.loads((ROOT / "fonts.json").read_text(encoding="utf-8"))["families"]:
        if family["files"]["ttf"] in seen:
            continue
        seen.add(family["files"]["ttf"])
        out.append(family)
    return out


def char(row: dict) -> str:
    return chr(int(row["codepoint"][2:], 16))


def script_of(family: dict) -> str:
    """The script whose glyph codes name the family's characters."""
    return codes.SCRIPTS[Path(family["files"]["ttf"]).stem]


class Face:
    def __init__(self, family: dict):
        self.family = family
        self.r = Renderer(ROOT / family["files"]["ttf"])
        self.direction = "rtl" if family["direction"] == "rtl" else "ltr"
        self.features = {f: True for f in family["features"]}
        self.by_glyph = {row["glyph"]: char(row) for row in family["codepoints"]}

    def shape(self, text: str) -> Shaped:
        return self.r.shape(text, self.features, self.direction)

    def bounds(self, shaped: Shaped):
        """The ink box of shaped text in font units, (x0, y0, x1, y1) y up; None when it has no ink."""
        xs, ys = [], []
        for gid, gx, gy, _ in shaped.glyphs:
            for _, pts in self.r.contours(gid):
                xs += [gx + px for px, _ in pts]
                ys += [gy + py for _, py in pts]
        return (min(xs), min(ys), max(xs), max(ys)) if xs else None

    def draw(self, img, x, baseline, shaped, size):
        self.r.draw(img, x, baseline, shaped, size, INK)

    def column(self, text: str) -> Shaped:
        """The text shaped top to bottom, as Teng Chou is written."""
        buf = hb.Buffer()
        buf.add_str(text)
        buf.direction = "ttb"
        buf.script = "Zyyy"
        buf.guess_segment_properties()
        hb.shape(self.r.hb_font, buf, {})
        glyphs, pen_y = [], 0
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            glyphs.append((info.codepoint, pos.x_offset, pen_y + pos.y_offset, pos.y_advance))
            pen_y += pos.y_advance
        return Shaped(glyphs, -pen_y)


# -- images -----------------------------------------------------------------------


def label_font(size: int) -> ImageFont.FreeTypeFont:
    """Pillow's own Latin face, the same on every platform, so a page renders alike wherever it is checked."""
    return ImageFont.load_default(size)


def png_bytes(img: Image.Image) -> bytes:
    out = io.BytesIO()
    img.save(out, format="PNG", optimize=True)
    return out.getvalue()


def text_width(d: ImageDraw.ImageDraw, text: str, size: int) -> float:
    return d.textlength(text, font=label_font(size))


def cells_image(face: Face, groups: list[tuple[str, list[tuple[str, str]]]], size: int = SIZE) -> Image.Image:
    """Groups of cells, each cell a shaped string over its Latin label, on a ruled grid.

    Each cell's ink is centred across the cell and keeps the face's common baseline, so
    the letters stand as they stand in a line.
    """
    scale = size / face.r.upem
    probe = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    shaped = [[(label, face.shape(text)) for label, text in cells] for _, cells in groups]
    boxes = [[face.bounds(s) for _, s in row] for row in shaped]
    flat = [b for row in boxes for b in row if b]
    top = max(b[3] for b in flat) * scale
    bottom = -min(b[1] for b in flat) * scale
    ink_w = max((b[2] - b[0]) * scale for b in flat)
    label_w = max(text_width(probe, label, LABEL - 2) for row in shaped for label, _ in row)
    cell_w = int(max(ink_w + 24, label_w + 12, size * 1.25))
    cell_h = int(top + bottom + 18 + LABEL + 14)
    per_row = max(1, (WIDTH - 2 * MARGIN) // cell_w)
    height = MARGIN // 2
    for title, cells in groups:
        height += (LABEL + 18 if title else 0) + -(-len(cells) // per_row) * cell_h + 16
    width = 2 * MARGIN + min(per_row, max(len(c) for _, c in groups)) * cell_w
    img = Image.new("RGB", (width, height + MARGIN // 2), PAPER)
    d = ImageDraw.Draw(img)
    y = MARGIN // 2
    for (title, _), row, row_boxes in zip(groups, shaped, boxes):
        if title:
            d.text((MARGIN, y), title, fill=GREY, font=label_font(LABEL))
            y += LABEL + 18
        for i, ((label, s), box) in enumerate(zip(row, row_boxes)):
            cx = MARGIN + (i % per_row) * cell_w
            cy = y + (i // per_row) * cell_h
            d.rectangle([cx, cy, cx + cell_w, cy + cell_h], outline=RULE)
            baseline = cy + 9 + top
            if box:
                ink_mid = (box[0] + box[2]) / 2 * scale
                face.draw(img, cx + cell_w / 2 - ink_mid, baseline, s, size)
            lw = text_width(d, label, LABEL - 2)
            d.text((cx + (cell_w - lw) / 2, cy + cell_h - LABEL - 8), label, fill=GREY, font=label_font(LABEL - 2))
        y += -(-len(row) // per_row) * cell_h + 16
    return img


def sign_ids() -> dict[str, str]:
    """Khelathi Zethu Glyphs' sign ids, ``01-001``, by code point."""
    enc = json.loads((ROOT / "tools" / "khelathi-zethu-glyphs" / "encoding.json").read_text(encoding="utf-8"))
    return {s["codepoint"]: s["id"] for s in enc["signs"]}


SIGN_IDS = sign_ids()


def label_of(row: dict) -> str:
    glyph = row["glyph"]
    if row["kind"] == "sign":
        return SIGN_IDS[row["codepoint"]]
    for prefix in ("tc.", "js.", "num."):
        if glyph.startswith(prefix):
            return glyph[len(prefix):]
    return glyph


def letters_groups(face: Face) -> list[tuple[str, list[tuple[str, str]]]]:
    rows = face.family["codepoints"]
    klass = face.family["class"]
    if klass == "hl-teng-chou":
        picked = []
        for kind, count in TENG_CHOU_SAMPLE.items():
            picked.append((GROUPS[kind], [(label_of(r), char(r)) for r in rows if r["kind"] == kind][:count]))
        return picked
    if klass == "hl-khelathi-zethu-glyphs":
        first = {}
        for r in rows:
            if r["kind"] == "sign":
                first.setdefault(SIGN_IDS[r["codepoint"]].split("-")[0], r)
        return [("The first sign of each group", [(label_of(r), char(r)) for r in first.values()])]
    groups = {}
    for r in rows:
        if r["kind"] == "control" or face.bounds(face.shape(char(r))) is None:
            continue
        groups.setdefault(r["kind"], []).append((label_of(r), char(r)))
    return [(GROUPS[k], cells) for k, cells in groups.items()]


def marks_groups(face: Face, texts: dict) -> list[tuple[str, list[tuple[str, str]]]]:
    script = script_of(face.family)
    return [("", [(m["label"], codes.text(script, m["codes"])) for m in texts["marks"]])]


def passage_image(face: Face, lines: list[str], size: int = SIZE) -> Image.Image:
    """The lines in the script, numbered; right-aligned for a right-to-left face."""
    scale = size / face.r.upem
    shaped = [face.shape(t) for t in lines]
    boxes = [face.bounds(s) for s in shaped]
    top = max(b[3] for b in boxes if b) * scale
    bottom = -min(b[1] for b in boxes if b) * scale
    line_h = int(top + bottom + size * 0.35)
    gutter = 56
    widths = [s.advance * scale for s in shaped]
    width = int(2 * MARGIN + gutter + max(widths))
    img = Image.new("RGB", (width, 2 * MARGIN + line_h * len(lines)), PAPER)
    d = ImageDraw.Draw(img)
    for i, (s, w) in enumerate(zip(shaped, widths)):
        baseline = MARGIN + i * line_h + top
        number = str(i + 1)
        if face.direction == "rtl":
            face.draw(img, width - MARGIN - gutter - w, baseline, s, size)
            d.text((width - MARGIN - gutter + 18, baseline - LABEL - size * 0.15), number, fill=GREY, font=label_font(LABEL))
        else:
            face.draw(img, MARGIN + gutter, baseline, s, size)
            d.text((MARGIN, baseline - LABEL - size * 0.15), number, fill=GREY, font=label_font(LABEL))
    return img


def columns_image(face: Face, lines: list[str], size: int = 72) -> Image.Image:
    """Each line a column, top to bottom, the columns read from the right, numbered above."""
    scale = size / face.r.upem
    columns = [face.column(t) for t in lines]
    tallest = max(c.advance for c in columns) * scale
    pitch = int(size * 1.6)
    width = 2 * MARGIN + pitch * len(lines)
    head = LABEL + 16
    img = Image.new("RGB", (width, int(2 * MARGIN + head + tallest)), PAPER)
    d = ImageDraw.Draw(img)
    for i, c in enumerate(columns):
        axis = width - MARGIN - pitch * i - pitch / 2
        number = str(i + 1)
        d.text((axis - text_width(d, number, LABEL) / 2, MARGIN), number, fill=GREY, font=label_font(LABEL))
        face.draw(img, axis, MARGIN + head, c, size)
    return img


# -- the pages --------------------------------------------------------------------


def readme_rows() -> dict[str, list[str]]:
    """The README's font table, by font name: its cells."""
    rows = {}
    for line in README.read_text(encoding="utf-8").splitlines():
        if line.startswith("|") and not line.startswith("| ---"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            rows[cells[0]] = cells
    return rows


def sample_cell(family: dict) -> str:
    name, klass = family["name"], family["class"]
    return f"[![{name}]({RAW}/{klass}.png)](specimens/{klass}.md)"


def readme_text(families: list[dict]) -> str:
    """The README with each font's Sample cell the absolute image URL linked to its page."""
    out = []
    names = {f["name"]: f for f in families}
    for line in README.read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.strip("|").split("|")] if line.startswith("|") else []
        if cells and cells[0] in names and len(cells) == 5:
            cells[3] = sample_cell(names[cells[0]])
            line = "| " + " | ".join(cells) + " |"
        out.append(line)
    return "\n".join(out) + "\n"


def page_markdown(family: dict, texts: dict, row: list[str], images: dict[str, str]) -> str:
    name, klass = family["name"], family["class"]
    what, direction = row[1], row[2]
    chart = f"../charts/{FOLDERS.get(klass, klass.removeprefix('hl-'))}.md"
    links = ["[Back to the README](../README.md)", f"[Character chart]({chart})"]
    src = texts.get("source")
    written = "in columns, top to bottom" if direction.startswith("Vertical") else direction.lower()
    out = [f"# {name}", "", f"{what}, written {written}.", "", " · ".join(links), ""]
    if klass == "hl-khelathi-zethu-glyphs":
        out += [
            "## The banner",
            "",
            f"![The Khelathu banner, the memorial of Meqes VI]({images['banner']})",
            "",
            "The Khelathu banner, the memorial of Meqes VI in ten registers, drawn from this font's signs and painted. "
            f"It is thalorna's `{src['image']}`, and its English text, below, is from `{src['note']}` there. "
            "Square brackets mark text restored from the approved inscription; braces mark formulas added from other texts.",
            "",
        ]
        out += [f"{i}. {p}" for i, p in enumerate(texts["english"], 1)]
        out += [
            "",
            "## The signs",
            "",
            f"The font has {sum(1 for r in family['codepoints'] if r['kind'] == 'sign')} signs. "
            f"This is the first of each group, under its sign id; the [chart]({chart}) has them all.",
            "",
            f"![A sample of the signs of {name}]({images['letters']})",
            "",
        ]
        return "\n".join(out)
    if klass == CHALISH:
        out += [
            "## The glyphs",
            "",
            "Each glyph is a concept, built from strokes in one even line. The sheet groups them by who knows them: "
            f"the core glyphs everyone reads, then those of a trade, the scribes and the priests, then the numbers, the compounds and "
            f"names written in sounds. The [chart]({chart}) lists every glyph with its code point.",
            "",
            f"![The glyphs of {name}]({texts['images']['glyphs']})",
            "",
            "## A night's entry",
            "",
            "The Faith of Ish'ilan Ch'alish keeps a record of every night at the sighting stones, whether or not anything "
            "happens. The entry is a record of meaning, not of words: it is set here as text, and the page wraps it two glyphs "
            "to a row, read down each column.",
            "",
            f"![A night's entry in {name}]({texts['images']['text']})",
            "",
        ]
        out += [f"{i}. {line['english']}" for i, line in enumerate(texts["lines"], 1)]
        out.append("")
        return "\n".join(out)
    if klass == CEREMONIAL:
        out += [
            "## The glyphs",
            "",
            "Each glyph is carved whole, and glyphs are composed into blocks: a main sign with a number, syllable signs "
            "or both set beside it, over it or under it. A block is written as its glyphs with a joiner between two of "
            "them: `JOINER_BESIDE` sets two items side by side and `JOINER_STACK` stacks the first over the second, and "
            f"the font lays the block out from those joiners. The [chart]({chart}) lists every glyph with its code point "
            "and code.",
            "",
            f"![The canon sheet of {name}]({texts['images']['glyphs']})",
            "",
            "## A lord's seating",
            "",
            "Sixteen blocks in paired columns, read across each pair and down: A1, B1, A2, B2. Each block is listed "
            "below by its glyph codes and set through the font.",
            "",
            f"![A lord's seating in {name}]({texts['images']['text']})",
            "",
        ]
        out += [f"{i}. {line['english']}  \n{' ' * len(f'{i}. ')}`{line['codes']}`" for i, line in enumerate(texts["lines"], 1)]
        out += ["", texts["english"], ""]
        return "\n".join(out)
    out += ["## The letters", ""]
    if klass == "hl-teng-chou":
        counts = {k: sum(1 for r in family["codepoints"] if r["kind"] == k) for k in TENG_CHOU_SAMPLE}
        out += [
            f"A sample: the first {TENG_CHOU_SAMPLE['character']} of the font's {counts['character']} characters "
            f"and the first {TENG_CHOU_SAMPLE['syllable']} of its {counts['syllable']} syllables, each under its reading; "
            f"the [chart]({chart}) has them all.",
            "",
        ]
    else:
        out += ["Every character the font draws on its own, each under its glyph name.", ""]
    out += [f"![The letters of {name}]({images['letters']})", ""]
    if texts.get("marks"):
        out += ["## The marks", "", texts["marks_note"], "", f"![Marks of {name}]({images['marks']})", ""]
    where = f"_{src['title']}_" if src["section"].startswith("lines") else f"the {src['section']} of _{src['title']}_"
    lines_note = f", {src['section']}" if src["section"].startswith("lines") else ""
    out += ["## A passage", "", f"From {where}{lines_note}, in thalorna.", ""]
    if klass == "hl-teng-chou":
        out += ["Each sentence is a column, read top to bottom, the columns from the right.", ""]
    elif face_direction(family) == "rtl":
        out += ["Each line reads from the right.", ""]
    out += [f"![A passage in {name}]({images['passage']})", ""]
    for i, line in enumerate(texts["lines"], 1):
        out += [f"{i}. {line['english']}  ", f"   _{line['roman']}_"]
    out.append("")
    return "\n".join(out)


def face_direction(family: dict) -> str:
    return "rtl" if family["direction"] == "rtl" else "ltr"


def render(families: list[dict], texts: dict, problems: list[str]) -> dict[Path, bytes]:
    """Every page, image and the README, as bytes by path; a family that cannot be rendered adds a problem."""
    out = {}
    rows = readme_rows()
    for family in families:
        klass = family["class"]
        data = texts["families"].get(klass)
        if data is None:
            problems.append(f"specimens/texts.json: error: {klass}: no texts")
            continue
        if family["name"] not in rows:
            problems.append(f"README.md: error: the font table has no row for {family['name']}")
            continue
        if klass in COMMITTED:
            out[SPECIMENS / f"{klass}.md"] = page_markdown(family, data, rows[family["name"]], {}).encode("utf-8")
            for image in data["images"].values():
                if not (SPECIMENS / image).exists():
                    problems.append(f"specimens/{image}: error: missing; run the sheet scripts of tools/chalish-pilam")
            continue
        face = Face(family)
        images = {}

        def put(kind: str, img: Image.Image):
            path = PAGES / f"{klass}-{kind}.png"
            out[path] = png_bytes(img)
            images[kind] = path.relative_to(SPECIMENS).as_posix()

        put("letters", cells_image(face, letters_groups(face), SIGN_SIZE if klass == "hl-khelathi-zethu-glyphs" else SIZE))
        if data.get("marks"):
            put("marks", cells_image(face, marks_groups(face, data)))
        if data.get("lines"):
            script = [codes.text(script_of(family), line["codes"]) for line in data["lines"]]
            put("passage", columns_image(face, script) if klass == "hl-teng-chou" else passage_image(face, script))
        if data.get("banner"):
            images["banner"] = (PAGES / f"{klass}-banner.webp").relative_to(SPECIMENS).as_posix()
        out[SPECIMENS / f"{klass}.md"] = page_markdown(family, data, rows[family["name"]], images).encode("utf-8")
    out[README] = readme_text(families).encode("utf-8")
    return out


def readme_current(families: list[dict]) -> list[str]:
    """The README rows whose Sample cell is not the absolute image URL linked to the font's page."""
    rows = readme_rows()
    problems = []
    for family in families:
        cell = rows.get(family["name"], [None] * 5)[3]
        if cell != sample_cell(family):
            problems.append(f"README.md: error: {family['name']}: the sample cell is {cell!r}, not {sample_cell(family)!r}")
    return problems


def same(path: Path, data: bytes) -> bool:
    """Whether the file holds this content; an image is compared by its pixels."""
    if not path.exists():
        return False
    if path.suffix == ".png":
        old = Image.open(path).convert("RGB")
        new = Image.open(io.BytesIO(data)).convert("RGB")
        return old.size == new.size and ImageChops.difference(old, new).getbbox() is None
    return path.read_bytes() == data


def check(families: list[dict], texts: dict) -> list[str]:
    problems = []
    fresh = render(families, texts, problems)
    for path, data in fresh.items():
        rel = path.relative_to(ROOT).as_posix()
        if not path.exists():
            problems.append(f"{rel}: error: missing; run tools/specimen_pages.py")
        elif path == README:
            problems += readme_current(families)
        elif not same(path, data):
            problems.append(f"{rel}: error: out of date with the fonts and specimens/texts.json; run tools/specimen_pages.py")
    for family in families:
        data = texts["families"].get(family["class"], {})
        if data.get("banner"):
            banner = PAGES / f"{family['class']}-banner.webp"
            if not banner.exists():
                problems.append(f"{banner.relative_to(ROOT)}: error: missing")
            elif hashlib.sha256(banner.read_bytes()).hexdigest() != data["banner"]["sha256"]:
                problems.append(f"{banner.relative_to(ROOT)}: error: differs from the banner specimens/texts.json records")
    classes = [f["class"] for f in manifest()]
    checked = [f["class"] for f in families]
    stray = {
        p for p in PAGES.glob("*")
        if not any(p.name.startswith(f"{c}-") for c in classes)
        or (any(p.name.startswith(f"{c}-") for c in checked) and p not in fresh and not p.name.endswith("-banner.webp"))
    }
    problems += [f"{p.relative_to(ROOT)}: error: no family writes it" for p in sorted(stray)]
    return problems


def main() -> None:
    ap = argparse.ArgumentParser(description="Write or check the specimen pages.")
    ap.add_argument("--check", action="store_true", help="fail where a page, image or README cell is missing or out of date")
    args = ap.parse_args()
    families = manifest()
    texts = json.loads(TEXTS.read_text(encoding="utf-8"))
    if args.check:
        problems = check(families, texts)
        for line in problems:
            print(line, file=sys.stderr)
        print(f"specimen pages: {len(problems)} problems" if problems else "specimen pages: ok")
        sys.exit(1 if problems else 0)
    PAGES.mkdir(parents=True, exist_ok=True)
    problems = []
    rendered = render(families, texts, problems)
    if problems:
        raise SystemExit("\n".join(problems))
    for path, data in rendered.items():
        if path == README:
            if readme_current(families):
                path.write_bytes(data)
                print("README.md: sample cells written; run npm run format to align the table")
            continue
        if not same(path, data):
            path.write_bytes(data)
            print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
