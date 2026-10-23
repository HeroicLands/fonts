# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Write the cheatsheet of every font: a code chart and a table of each character.

    .venv/bin/python tools/charts.py

Everything is read from the ``codepoints`` tables of fonts.json and the committed font
files. A glyph is the outline the font draws for its code point, shaped with the
font's OpenType ``features``, so no font has to be installed to view a sheet.

- ``charts/<face folder>/chart-<n>.svg`` and ``chart-<n>.png``: the code chart, laid
  out like Unicode's charts. Columns are headed by the code point without its last
  hex digit and rows by that digit, ``0`` to ``F``; a cell holds the glyph with its
  code point beneath; a code point the font does not draw is hatched. The grid runs
  left to right in every font, as Unicode's charts do. A long range is split into
  pages of ``COLUMNS`` columns, and columns with no character are left out.
- ``charts/<face folder>/glyphs/U+XXXX.svg``: one glyph, for the table.
- ``charts/<face folder>.md``: the chart pages and then the table of Character Name,
  Character, Code Point, Entity and Hex Entity, grouped by kind.
- ``charts/index.md``: a link to every sheet.

The PNGs are rasterized from the SVGs with ``resvg-py``, pinned in ``requirements.txt``.
"""

import json
import shutil
import sys
from pathlib import Path

import resvg_py
import uharfbuzz as hb
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
from codepoints_chart import FOLDERS as LTR_FOLDERS  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "charts"

# The face folder of each family, by manifest class: the specimen folders, and one for the
# faces that have none.
FOLDERS = {
    **LTR_FOLDERS,
    "hl-thuravark-carved-bound": "thuravark-carved-bound",
    "hl-qalezu-hand": "qalezu-hand",
    "hl-khelathi-zethu-glyphs": "khelathi-zethu-glyphs",
    "hl-veldikko": "veldikko",
    "hl-vedyakshara-classical": "vedyakshara-classical",
    "hl-helonika-book": "helonika-book",
}

COLUMNS = 8
CELL_W, CELL_H = 88, 104
GLYPH_H = 76
EM = 52
HEAD_H, ROW_W, TITLE_H, PAD = 34, 34, 56, 16
HEAVY, THIN = 3, 1
SANS = "Helvetica, Arial, sans-serif"
INK, GREY = "#161412", "#6b665f"

GLYPH_EM = 40
GLYPH_BOX = 64

GROUPS = {
    "letter": "Letters",
    "digraph": "Digraphs",
    "diphthong": "Diphthongs",
    "doubled": "Doubled letters",
    "numeral": "Digits",
    "point": "Punctuation",
    "mark": "Marks",
    "sign": "Signs",
    "character": "Characters",
    "syllable": "Syllables",
    "control": "Controls",
}


def code(row: dict) -> int:
    return int(row["codepoint"][2:], 16)


def hexcode(row: dict) -> str:
    return f"{code(row):04X}"


class Face:
    """One font file shaped with one set of features."""

    def __init__(self, entry: dict):
        self.entry = entry
        self.path = ROOT / entry["files"]["ttf"]
        self.tt = TTFont(self.path)
        self.upem = self.tt["head"].unitsPerEm
        self.glyphs = self.tt.getGlyphSet()
        self.order = self.tt.getGlyphOrder()
        self.hb = hb.Font(hb.Face(self.path.read_bytes()))
        self.hb.scale = (self.upem, self.upem)
        self.features = {tag: True for tag in entry["features"]}
        self.direction = entry["direction"]

    def shape(self, row: dict) -> str:
        """The name of the one glyph the font draws for the row's code point."""
        buf = hb.Buffer()
        buf.add_str(chr(code(row)))
        buf.direction = self.direction
        buf.script = "Zyyy"
        buf.guess_segment_properties()
        hb.shape(self.hb, buf, self.features)
        names = [self.order[i.codepoint] for i in buf.glyph_infos]
        assert len(names) == 1, f"{self.entry['name']}: {row['codepoint']} shapes to {names}"
        return names[0]

    def outline(self, name: str) -> tuple[str, tuple | None, int]:
        """The SVG path (font units, y up), its ink bounds and its advance width."""
        pen = SVGPathPen(self.glyphs)
        self.glyphs[name].draw(pen)
        bounds = BoundsPen(self.glyphs)
        self.glyphs[name].draw(bounds)
        return pen.getCommands(), bounds.bounds, self.glyphs[name].width


def place(face: Face, name: str, box_w: float, box_h: float, em: float, centred: bool) -> str | None:
    """The SVG ``<path>`` for a glyph in a box whose origin is its top left corner."""
    d, bounds, advance = face.outline(name)
    if not d or bounds is None:
        return None
    x0, y0, x1, y1 = bounds
    scale = em / face.upem
    for _ in range(2):
        w, h = (x1 - x0) * scale, (y1 - y0) * scale
        if centred or advance <= 0 or w > box_w * 0.94 or h > box_h * 0.94:
            # Centre on the ink, shrunk to fit when it overflows.
            fit = min(1, box_w * 0.94 / w, box_h * 0.94 / h)
            scale *= fit
            tx = box_w / 2 - (x0 + x1) / 2 * scale
            ty = box_h / 2 + (y0 + y1) / 2 * scale
            break
        tx = box_w / 2 - advance * scale / 2
        ty = box_h * 0.78
        if ty + (-y0) * scale > box_h or ty - y1 * scale < 0:
            centred = True
            continue
        break
    return f'<path transform="translate({tx:.2f} {ty:.2f}) scale({scale:.5f} {-scale:.5f})" d="{d}"/>'


def centred(entry: dict) -> bool:
    """Signs and characters drawn in a square are centred on their ink; letters keep a common baseline."""
    return entry["codepoints"][0]["kind"] in ("sign", "character")


def glyph_svg(face: Face, row: dict) -> str:
    name = face.shape(row)
    path = place(face, name, GLYPH_BOX, GLYPH_BOX, GLYPH_EM, centred(face.entry))
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{GLYPH_BOX}" height="{GLYPH_BOX}" '
        f'viewBox="0 0 {GLYPH_BOX} {GLYPH_BOX}" role="img" aria-label="U+{hexcode(row)}">\n'
        f'<rect width="{GLYPH_BOX}" height="{GLYPH_BOX}" rx="6" fill="#ffffff"/>\n'
        f'<g fill="{INK}">{path or ""}</g>\n</svg>\n'
    )


def pages(table: list[dict]) -> list[list[int]]:
    """The chart pages: each a list of column numbers (code point >> 4), consecutive and at
    most COLUMNS long."""
    cols = sorted({code(r) >> 4 for r in table})
    runs: list[list[int]] = []
    for c in cols:
        if runs and runs[-1][-1] == c - 1:
            runs[-1].append(c)
        else:
            runs.append([c])
    return [run[i : i + COLUMNS] for run in runs for i in range(0, len(run), COLUMNS)]


def chart_svg(face: Face, table: list[dict], columns: list[int], page: int, count: int) -> str:
    by_code = {code(r): r for r in table}
    ncols = len(columns)
    grid_x, grid_y = PAD + ROW_W, PAD + TITLE_H + HEAD_H
    width = max(grid_x + ncols * CELL_W + PAD, 380)
    height = grid_y + 16 * CELL_H + PAD
    first, last = columns[0] << 4, (columns[-1] << 4) + 15
    title = face.entry["name"]
    sub = f"U+{first:04X}–U+{last:04X}" + (f", page {page} of {count}" if count > 1 else "")
    o = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        f"<title>{title} {sub}</title>",
        "<defs>",
        '<pattern id="hatch" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
        f'<line x1="0" y1="0" x2="0" y2="7" stroke="#8d877e" stroke-width="1"/></pattern>',
        "</defs>",
        f'<rect width="{width}" height="{height}" fill="#ffffff"/>',
        f'<text x="{PAD}" y="{PAD + 22}" font-family="{SANS}" font-size="22" fill="{INK}">{title}</text>',
        f'<text x="{PAD}" y="{PAD + 44}" font-family="{SANS}" font-size="14" fill="{GREY}">{sub}</text>',
    ]
    for i, col in enumerate(columns):
        x = grid_x + i * CELL_W + CELL_W / 2
        o.append(
            f'<text x="{x}" y="{grid_y - 10}" text-anchor="middle" font-family="{SANS}" font-size="15" '
            f'font-weight="bold" fill="{INK}">{col:04X}</text>'
        )
    for r in range(16):
        o.append(
            f'<text x="{grid_x - 10}" y="{grid_y + r * CELL_H + CELL_H / 2 + 5}" text-anchor="end" '
            f'font-family="{SANS}" font-size="15" font-weight="bold" fill="{INK}">{r:X}</text>'
        )
    mark = centred(face.entry)
    for i, col in enumerate(columns):
        for r in range(16):
            cp = (col << 4) | r
            x, y = grid_x + i * CELL_W, grid_y + r * CELL_H
            row = by_code.get(cp)
            if row is None:
                o.append(f'<rect class="undrawn" x="{x}" y="{y}" width="{CELL_W}" height="{CELL_H}" fill="url(#hatch)"/>')
                continue
            path = place(face, face.shape(row), CELL_W, GLYPH_H, EM, mark)
            o.append(f'<g class="drawn" id="cp-{cp:04X}" transform="translate({x} {y})">')
            o.append(f'<title>{row.get("name", "")} U+{cp:04X}</title>')
            o.append(f'<g fill="{INK}">{path or ""}</g>')
            o.append(
                f'<text x="{CELL_W / 2}" y="{CELL_H - 9}" text-anchor="middle" font-family="{SANS}" '
                f'font-size="12" fill="{GREY}">{cp:04X}</text>'
            )
            o.append("</g>")
    # Thin cell borders, then the heavy rules under the header and on the outer sides.
    gw, gh = ncols * CELL_W, 16 * CELL_H
    for i in range(ncols + 1):
        o.append(f'<line x1="{grid_x + i * CELL_W}" y1="{grid_y}" x2="{grid_x + i * CELL_W}" y2="{grid_y + gh}" stroke="#7a756d" stroke-width="{THIN}"/>')
    for r in range(17):
        o.append(f'<line x1="{grid_x}" y1="{grid_y + r * CELL_H}" x2="{grid_x + gw}" y2="{grid_y + r * CELL_H}" stroke="#7a756d" stroke-width="{THIN}"/>')
    for x1, y1, x2, y2 in (
        (grid_x - HEAVY / 2, grid_y, grid_x + gw + HEAVY / 2, grid_y),
        (grid_x, grid_y - HEAD_H, grid_x, grid_y + gh),
        (grid_x + gw, grid_y - HEAD_H, grid_x + gw, grid_y + gh),
    ):
        o.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{INK}" stroke-width="{HEAVY}"/>')
    o.append("</svg>")
    return "\n".join(o) + "\n"


def rasterize(svg: Path, png: Path) -> None:
    png.write_bytes(bytes(resvg_py.svg_to_bytes(svg_path=str(svg), zoom=2)))


def sheet_markdown(entry: dict, folder: str, table: list[dict], npages: int) -> str:
    first, last = code(table[0]), code(table[-1])
    out = [
        f"# {entry['name']}",
        "",
        f"{len(table)} characters, U+{first:04X} to U+{last:04X}, in the font `{entry['family']}`"
        + (f" with the OpenType feature `{'`, `'.join(entry['features'])}` on." if entry["features"] else "."),
        "",
        "## Code chart",
        "",
    ]
    out += [f"![{entry['name']}, code chart {n}]({folder}/chart-{n}.png)" for n in range(1, npages + 1)]
    out += ["", "## Characters", ""]
    kinds: dict[str, list[dict]] = {}
    for row in table:
        kinds.setdefault(row["kind"], []).append(row)
    for kind, rows in kinds.items():
        out += [f"### {GROUPS[kind]}", "", "| Character Name | Character | Code Point | Entity | Hex Entity |", "| --- | --- | --- | --- | --- |"]
        for row in rows:
            cp = code(row)
            image = f"![U+{cp:04X}]({folder}/glyphs/U+{cp:04X}.svg)"
            out.append(f"| {row.get('name', '')} | {image} | {row["codepoint"]} | `&#{cp};` | `&#x{cp:04X};` |")
        out.append("")
    return "\n".join(out)


def main() -> None:
    manifest = json.loads((ROOT / "fonts.json").read_text(encoding="utf-8"))
    OUT.mkdir(exist_ok=True)
    written = []
    index = ["# Cheatsheets", "", "Each font has a sheet of every character it draws: a code chart laid out like Unicode's, and a table of each character's name, glyph and code point.", ""]
    for entry in manifest["families"]:
        folder = FOLDERS[entry["class"]]
        table = sorted(entry["codepoints"], key=code)
        face = Face(entry)
        base = OUT / folder
        if base.exists():
            shutil.rmtree(base)
        (base / "glyphs").mkdir(parents=True)
        for row in table:
            path = base / "glyphs" / f"U+{hexcode(row)}.svg"
            path.write_text(glyph_svg(face, row), encoding="utf-8")
            written.append(path)
        chart_pages = pages(table)
        for n, columns in enumerate(chart_pages, 1):
            svg = base / f"chart-{n}.svg"
            svg.write_text(chart_svg(face, table, columns, n, len(chart_pages)), encoding="utf-8")
            png = svg.with_suffix(".png")
            rasterize(svg, png)
            written += [svg, png]
        md = OUT / f"{folder}.md"
        md.write_text(sheet_markdown(entry, folder, table, len(chart_pages)), encoding="utf-8")
        written.append(md)
        index.append(f"- [{entry['name']}]({folder}.md): {len(table)} characters on {len(chart_pages)} chart page{'s' if len(chart_pages) > 1 else ''}")
    index.append("")
    (OUT / "index.md").write_text("\n".join(index), encoding="utf-8")
    written.append(OUT / "index.md")
    for path in written:
        print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
