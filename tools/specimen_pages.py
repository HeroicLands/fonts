# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Write the specimen page of each font, and the README's sample cells that link to it.

    .venv/bin/python tools/specimen_pages.py            # write the pages, their images and the README cells
    .venv/bin/python tools/specimen_pages.py --check    # fail where any of them is missing or out of date
    .venv/bin/python tools/specimen_pages.py --write-texts [--thalorna PATH] [--encoding SCRIPT=FILE]

Every family of fonts.json that is its own font file has a page, ``specimens/<class>.md``,
with its images in ``specimens/pages/``:

- ``<class>-letters.png``: every character the font draws, grouped as its chart groups
  them; Teng Chou and Khelathi Zethu Glyphs show a sample, and their pages link the chart;
- ``<class>-marks.png``: a sample of the marks set on a few letters, where the script has marks;
- ``<class>-passage.png``: a passage of thalorna in the script, its lines numbered, set
  right to left for a right-to-left font and in columns for Teng Chou. The page gives
  each line's English with its roman spelling under it.

Chalish Pilam Common has no encoding of spelling, since its glyphs record meaning rather than
spelling. Its page shows the committed sheets of ``specimens/chalish-pilam/`` (the glyphs
and the night's entry set through the font) and lists the entry phrase by phrase; its
``texts.json`` entry is written from ``tools/chalish-pilam/glyphs.py`` by ``--write-texts``.

Khelathi Zethu Glyphs' page also shows the Khelathu banner, ``<class>-banner.webp``,
with its English text.

The texts are ``specimens/texts.json``: per family its source, and each line's code
points, roman spelling and English, and each mark sample's code points. ``--write-texts``
writes it once from a thalorna checkout: each roman line is written in the script by the
script's encoding (``encodings/<name>.json``, or the file ``--encoding`` names), and every
roman and English line must stand in its source note as written. Building the pages needs
no thalorna checkout.

Every line is shaped by HarfBuzz from the built font. ``--check`` renders every image
and page afresh in memory and fails where a file is missing, differs from what the
fonts and ``texts.json`` give, or where a README sample cell is not the absolute image
URL linked to its page.
"""

import argparse
import hashlib
import io
import json
import re
import subprocess
import sys
from pathlib import Path

import uharfbuzz as hb
from PIL import Image, ImageChops, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
from charts import FOLDERS, GROUPS  # noqa: E402
from render import Renderer, Shaped  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SPECIMENS = ROOT / "specimens"
PAGES = SPECIMENS / "pages"
TEXTS = SPECIMENS / "texts.json"
README = ROOT / "README.md"
THALORNA = Path.home() / "dev/HeroicLands/thalorna"
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

# What each page writes, by class. ``script`` names the script and ``face`` the face whose
# encoding writes it; ``tongue`` names the language. A passage's ``lines`` are (roman, English) as the
# source note writes them. A mark sample is (label, glyph names).
PASSAGES = {
    "hl-pirzath-carved": {
        "script": "pirzath",
        "face": "pirzath-carved",
        "tongue": "Khazari",
        "source": {
            "note": "assets/content/Skills/Languages/Khazari.md",
            "title": "Khazari Language",
            "section": "Sample Phrases",
        },
        "lines": [
            ("Vog dalkir, vog rummák ramk", "He is a mason; he lays the course as a master does"),
            ("Thamr, dank. Vald, varn.", "The blow, the hammer-fall; the binding, the true line"),
            ("Dalkir sumág dalk, dalkir khusáp", "The mason listens to the stone; the mason cuts little"),
            ("Ramk samíd, ramk thamír", "The course is raised; the course is struck"),
            ("Dalík bant, maríg bant", "Oath of stone, oath of bone"),
        ],
        "marks": [
            ("a with the length mark", ["a", "lengthmark"]),
            ("i with the length mark", ["i", "lengthmark"]),
            ("u with the length mark", ["u", "lengthmark"]),
            ("o with the length mark", ["o", "lengthmark"]),
        ],
        "marks_note": "The length mark is typed after its vowel and stands over it.",
    },
    "hl-pirzath-hand": {
        "script": "pirzath",
        "face": "pirzath-hand",
        "tongue": "Khazari",
        "source": {
            "note": "assets/content/Skills/Languages/Khazari.md",
            "title": "Khazari Language",
            "section": "Sample Phrases",
        },
        "lines": [
            ("Vog dalkir, vog rummák ramk", "He is a mason; he lays the course as a master does"),
            ("Thamr, dank. Vald, varn.", "The blow, the hammer-fall; the binding, the true line"),
            ("Dalkir sumág dalk, dalkir khusáp", "The mason listens to the stone; the mason cuts little"),
            ("Ramk samíd, ramk thamír", "The course is raised; the course is struck"),
            ("Dalík bant, maríg bant", "Oath of stone, oath of bone"),
        ],
        "marks": [
            ("a with the length mark", ["a", "lengthmark"]),
            ("i with the length mark", ["i", "lengthmark"]),
            ("u with the length mark", ["u", "lengthmark"]),
            ("o with the length mark", ["o", "lengthmark"]),
        ],
        "marks_note": "The length mark is typed after its vowel and stands over it.",
    },
    "hl-thuravark-carved": {
        "script": "thuravark",
        "face": "thuravark-carved",
        "tongue": "Nordmal",
        "source": {
            "note": "assets/content/Skills/Languages/Nordmal.md",
            "title": "Nordmal Language",
            "section": "Sample Phrases",
        },
        "lines": [
            ("Hersvald kallar tingit.", "The host-wielder calls the assembly."),
            ("Ver gangum í fridi.", "We come in peace."),
            ("Thrunvald vakir, ulfar thyrsta!", "The Thunder-Wielder wakes, the wolves thirst!"),
            ("Tvau skip, ein ferd.", "Two ships, one voyage."),
            ("Stóraldit lifir í steini ok í minni.", "The saga lives in stone and in memory."),
        ],
        "marks": [
            ("i with the acute", ["i", "acutecomb"]),
            ("o with the acute", ["o", "acutecomb"]),
            ("a with the acute", ["a", "acutecomb"]),
            ("Thrunvald, crowned", ["crown.open", "th", "r", "u", "n", "v", "a", "l", "d", "crown.close"]),
        ],
        "marks_note": "A vowel with the acute is cut as its stave twice. The crown open and crown close frame the name of a god between them.",
    },
    "hl-semaron-kuriale": {
        "script": "semaron",
        "face": "semaron-kuriale",
        "tongue": "Vylari",
        "source": {
            "note": "assets/content/Lore/Cultures/Vylarian/The_Walking_of_the_Line.md",
            "title": "The Walking of the Line",
            "section": "lines 1–4",
        },
        "lines": [
            ("Thiruthriman sorimamen,", "The hallowed boundary I sing,"),
            ("ul alathas kedis alatha valmazor, ul talothoi", "and the one who walked it, and the stones"),
            ("lendthoi ir yormalis ol selthur malkothoi", "set down in the grass of the six hills"),
            ("pra kembothos us urkis ol alathoi thalezor.", "before a wall stood on any of them."),
        ],
        "marks": [
            ("a with the catch", ["a", "grave"]),
            ("o with the catch", ["o", "grave"]),
            ("e with the catch", ["e", "grave"]),
            ("u with the catch", ["u", "grave"]),
        ],
        "marks_note": "The catch, a glottal stop, is a grave stroke over the letter it follows.",
    },
    "hl-helonika-book": {
        "script": "helonika",
        "face": "helonika-book",
        "tongue": "Helonic",
        "source": {
            "note": "assets/content/Skills/Languages/Helonic.md",
            "title": "Helonic Language",
            "section": "Sample Phrases",
        },
        "lines": [
            ("Sothira ésarin arkhidhin plumon", "Wisdom is the beginning of all things"),
            ("Ath kéliran théradhin ésarin thásiron", "To behold beauty is divine"),
            ("Rhéthasin, dhidakhir!", "Speak, teach!"),
            ("Métharin thoir plumon ésarin ánthimor", "Man is the measure of all things"),
            ("Olasin kosamir in lékhisir", "The entire cosmos in a single word"),
        ],
        "marks": [
            ("a with the accent", ["a", "accent"]),
            ("e with the accent", ["e", "accent"]),
            ("o with the accent", ["o", "accent"]),
            ("long a, i and u, with the length bar", ["a.macron", "i.macron", "u.macron"]),
            ("long e and long o", ["e.long", "o.long"]),
        ],
        "marks_note": "The accent stands over the vowel before it; the long vowels carry their length bar as letters of their own.",
    },
    "hl-vedyakshara-classical": {
        "script": "vedyakshara",
        "face": "vedyakshara-classical",
        "tongue": "Vedyari",
        "source": {
            "note": "assets/content/Skills/Languages/Vedyari.md",
            "title": "Vedyari Language",
            "section": "Sample Phrases",
        },
        "lines": [
            ("Agarana dulipati, vandikana", "Honored elder, I show respect"),
            ("Vedyaram tivayu, tarajisum", "I dwell in Vedyaram, by birthright"),
            ("Bhaktir ushtami dulitara", "I hold devotion as my highest path"),
            ("Vastuna karmata vanisa?", "May the transaction bring prosperity?"),
            ("Rituta samarvana ushti", "The observance is offered to the sacred order"),
        ],
        "marks": [
            ("ka", ["ka"]),
            ("ki", ["ka", "vs.i"]),
            ("ke", ["ka", "vs.e"]),
            ("kai", ["ka", "vs.ai"]),
            ("ku", ["ka", "vs.u"]),
            ("ko", ["ka", "vs.o"]),
            ("kau", ["ka", "vs.au"]),
            ("k, with the cut", ["ka", "cut"]),
            ("fa, pa with the soft dot", ["pa", "dot"]),
        ],
        "marks_note": "A consonant carries the vowel a; a vowel sign gives it another vowel, and the cut takes the vowel away.",
    },
    "hl-veldikko": {
        "script": "veldikko",
        "face": None,
        "tongue": "Sinale",
        "source": {
            "note": "assets/content/Skills/Languages/Sinale.md",
            "title": "Sinale Language",
            "section": "Sample Phrases",
        },
        "lines": [
            ("Luuro nuuva liseriho", "Starlight sings on still water"),
            ("Li-setty lenti talveho", "The tall grass stands in the low fog, as it always does"),
            ("Ha-tupe tilvai hyssen", "The seam of light has held the breath"),
            ("Peheka huoman, peheka nylkin", "Give warmth, give root"),
            ("Luuro ileva, luuro rivy", "The clear place sings, the turning leaf sings"),
        ],
        "marks": [
            ("ta", ["t", "vowel.a"]),
            ("to", ["t", "vowel.o"]),
            ("tuu, with the long sign", ["t", "vowel.u", "long"]),
            ("le, with the rise", ["l", "vowel.e", "rise"]),
            ("ni, with the fall", ["n", "vowel.i", "fall"]),
            ("tty, with the doubling bar", ["t", "bar", "vowel.y"]),
            ("a on the carrier", ["carrier", "vowel.a"]),
        ],
        "marks_note": "Each vowel is a mark floating over its letter, with its signs of length, pitch and emphasis folded into it.",
    },
    "hl-qalezu-hand": {
        "script": "qalezu",
        "face": "qalezu-hand",
        "tongue": "Khelathi",
        "source": {
            "note": "assets/content/Skills/Languages/Khelathi.md",
            "title": "Khelathi Language",
            "section": "Sample Phrases",
        },
        "lines": [
            ("Khelathu elu anlagh", "the Khelathi way upon life"),
            ("Uqa'a, qamzet ezu gazlet", "Sun-lord, hidden in the sanctuary"),
            ("Erlem ez luzet", "I am bound to the throne"),
            ("Zab melet agu khelath", "The lord's goods shall prosper"),
            ("Shelmu zetem", "Let the followers hear"),
        ],
        "marks": [
            ("q", ["q"]),
            ("catch before q", ["catch", "q"]),
            ("r", ["r"]),
            ("catch before r", ["catch", "r"]),
            ("doubled l", ["l.dbl"]),
            ("catch before doubled l", ["catch", "l.dbl"]),
        ],
        "marks_note": "A catch before a consonant is drawn as three reed dabs over it; a doubled consonant carries a bar beneath.",
    },
    "hl-teng-chou": {
        "script": "teng-chou",
        "tongue": "Tantsou",
        "source": {
            "note": "assets/content/Skills/Languages/Tantsou.md",
            "title": "Tantsou Language",
            "section": "Grammar Notes",
        },
        "lines": [
            ("You cheng.", "The moon rises."),
            ("Zho teng cheng.", "The dragon ascends the sky."),
            ("Lei wa.", "The spirit answers."),
            ("Shou jong.", "The water falls."),
            ("Dao chen tsou wa.", "The people answer the great emperor."),
        ],
    },
    "hl-khelathi-zethu-glyphs": {
        "script": "zethu",
        "tongue": "Khelathi",
        "source": {
            "note": "utils/banner-meqes/sign-sequence.md",
            "title": "the Meqes VI memorial",
            "section": "The English text",
            "image": "assets/images/banners/khelathubnr.webp",
        },
    },
}

CHALISH = "hl-chalish-pilam-common"
CHALISH_IMAGES = {"glyphs": "chalish-pilam/glyphs.png", "text": "chalish-pilam/text.png"}

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


def points(text: str) -> str:
    return " ".join(f"U+{ord(c):04X}" for c in text)


def unpoints(text: str) -> str:
    return "".join(chr(int(p[2:], 16)) for p in text.split())


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


def label_of(row: dict) -> str:
    glyph = row["glyph"]
    if row.get("key"):
        return row["key"]
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
                first.setdefault(r["key"].split("-")[0], r)
        return [("The first sign of each group", [(label_of(r), char(r)) for r in first.values()])]
    groups = {}
    for r in rows:
        if r["kind"] == "control" or face.bounds(face.shape(char(r))) is None:
            continue
        groups.setdefault(r["kind"], []).append((label_of(r), char(r)))
    return [(GROUPS[k], cells) for k, cells in groups.items()]


def marks_groups(face: Face, texts: dict) -> list[tuple[str, list[tuple[str, str]]]]:
    return [("", [(m["label"], unpoints(m["script"])) for m in texts["marks"]])]


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


def relink(cell: str) -> str:
    """A README link cell rewritten for a page one folder down."""
    return re.sub(r"\]\((?!https?:)([^)]+)\)", r"](../\1)", cell)


def page_markdown(family: dict, texts: dict, row: list[str], images: dict[str, str]) -> str:
    name, klass = family["name"], family["class"]
    what, direction, keyboard = row[1], row[2], row[4]
    chart = f"../charts/{FOLDERS.get(klass, klass.removeprefix('hl-'))}.md"
    links = [f"[Back to the README](../README.md)", f"[Character chart]({chart})"]
    if keyboard.startswith("["):
        links.append(f"Keyboard cheatsheet: {relink(keyboard)}")
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
            problems.append(f"specimens/texts.json: error: {klass}: no texts; run tools/specimen_pages.py --write-texts")
            continue
        if family["name"] not in rows:
            problems.append(f"README.md: error: the font table has no row for {family['name']}")
            continue
        if klass == CHALISH:
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
            script = [unpoints(line["script"]) for line in data["lines"]]
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
                problems.append(f"{banner.relative_to(ROOT)}: error: missing; run tools/specimen_pages.py --write-texts")
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


# -- writing texts.json from thalorna --------------------------------------------


def note_text(thalorna: Path, note: str) -> str:
    return subprocess.run(
        ["git", "-C", str(thalorna), "show", f"origin/main:{note}"], capture_output=True, text=True, check=True
    ).stdout


def script_line(records: dict) -> str:
    """The encoded line with what no row matched dropped, apart from its spaces.

    An encoding writes the marks its script writes; any other punctuation of the
    roman line passes through unencoded and would print the box, so the script line
    leaves it out, as the script does.
    """
    text = records["text"]
    for piece in set(records.get("unencoded", [])) - {" "}:
        if any(c.isalpha() for c in piece):
            raise SystemExit(f"tools/specimen_pages.py: error: {piece!r} has no row in its encoding")
        text = text.replace(piece, "")
    return re.sub(r" {2,}", " ", text).strip()


def teng_chou_line(family: dict, roman: str) -> str:
    cp = {r["glyph"]: char(r) for r in family["codepoints"]}
    morphemes = re.findall(r"[a-z]+", roman.lower())
    missing = [m for m in morphemes if f"tc.{m}" not in cp]
    if missing:
        raise SystemExit(f"Teng Chou: error: no character for {missing}")
    return "".join(cp[f"tc.{m}"] for m in morphemes)


def chalish_entry(family: dict) -> dict:
    """The texts.json entry of Chalish Pilam Common: the night's entry, one phrase to a line."""
    here = str(Path(__file__).resolve().parent / "chalish-pilam")
    sys.path.insert(0, here)
    for name in ("build_ufo", "glyphs", "strokes"):
        sys.modules.pop(name, None)
    try:
        import build_ufo
        import glyphs

        cp = {r["glyph"]: char(r) for r in family["codepoints"]}
        lines = [
            {"script": points("".join(cp[build_ufo.glyph_name(g)] for g in gs)), "english": gloss}
            for gloss, gs in glyphs.PASSAGE
        ]
    finally:
        sys.path.remove(here)
        for name in ("build_ufo", "glyphs", "strokes"):
            sys.modules.pop(name, None)
    return {"tongue": "Ki'ich'chik", "images": CHALISH_IMAGES, "lines": lines}


def banner_english(md: str) -> list[str]:
    section = re.search(r"^## The English text\n(.*?)(?=^## )", md, re.M | re.S).group(1)
    return [m.group(1).strip() for m in re.finditer(r"^\d+\. (.+)$", section, re.M)]


def write_texts(thalorna: Path, files: dict[str, str]) -> None:
    from encoded import Encoded

    families = {f["class"]: f for f in manifest()}
    doc = {"families": {}}
    for klass, spec in PASSAGES.items():
        family = families[klass]
        src = spec["source"]
        body = note_text(thalorna, src["note"])
        entry = {"tongue": spec["tongue"], "source": src}
        if klass == "hl-khelathi-zethu-glyphs":
            image = subprocess.run(
                ["git", "-C", str(thalorna), "show", f"origin/main:{src['image']}"], capture_output=True, check=True
            ).stdout
            PAGES.mkdir(parents=True, exist_ok=True)
            (PAGES / f"{klass}-banner.webp").write_bytes(image)
            entry["banner"] = {"sha256": hashlib.sha256(image).hexdigest()}
            entry["english"] = banner_english(body)
            doc["families"][klass] = entry
            continue
        for roman, english in spec["lines"]:
            for text in (roman, english):
                if text not in body:
                    raise SystemExit(f"{src['note']}: error: {text!r} does not stand in the note as written")
        romans = [r for r, _ in spec["lines"]]
        if spec["script"] == "teng-chou":
            scripts = [teng_chou_line(family, r) for r in romans]
        else:
            encoded = Encoded(spec["face"], files.get(spec["script"]))
            scripts = [script_line(rec) for rec in encoded.records(romans)]
        entry["lines"] = [
            {"script": points(s), "roman": r, "english": e} for s, (r, e) in zip(scripts, spec["lines"])
        ]
        if spec.get("marks"):
            face = Face(family)
            entry["marks_note"] = spec["marks_note"]
            entry["marks"] = [
                {"label": label, "script": points("".join(face.by_glyph[g] for g in glyphs))}
                for label, glyphs in spec["marks"]
            ]
        doc["families"][klass] = entry
    doc["families"][CHALISH] = chalish_entry(families[CHALISH])
    TEXTS.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{TEXTS.relative_to(ROOT)}: written")


def main() -> None:
    ap = argparse.ArgumentParser(description="Write or check the specimen pages.")
    ap.add_argument("--check", action="store_true", help="fail where a page, image or README cell is missing or out of date")
    ap.add_argument("--write-texts", action="store_true", help="write specimens/texts.json from a thalorna checkout")
    ap.add_argument("--thalorna", default=str(THALORNA))
    ap.add_argument("--encoding", action="append", default=[], metavar="SCRIPT=FILE",
                    help="apply an encoding file for a script instead of encodings/<name>.json, such as vedyakshara=FILE")
    args = ap.parse_args()
    if args.write_texts:
        write_texts(Path(args.thalorna), dict(n.split("=", 1) for n in args.encoding))
        return
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
