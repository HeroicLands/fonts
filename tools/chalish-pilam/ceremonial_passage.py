# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Render the Ch'alish P'ilam ceremonial hand's passage through the built font.

    .venv/bin/python tools/chalish-pilam/ceremonial_passage.py [--out specimens/chalish-pilam/ceremonial-passage.png]

The passage is a lord's seating and his deeds, sixteen blocks written in codage
(``PASSAGE``). Each block is written in code points by the Chalish Ceremonial Codage,
``encodings/chalish-ceremonial.json``, shaped by HarfBuzz through
``fonts/ChalishPilamCeremonial-Regular.ttf`` and drawn from the font's own outlines, so
the font lays out every block from its joiners. The blocks stand in paired columns, read
A1, B1, A2, B2, each over its place and its meaning. Shaping fails the run if any glyph
comes back as the box or ``.notdef``.
"""

import argparse
import subprocess
import sys
from pathlib import Path

import uharfbuzz as hb
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT))
import encode as E  # noqa: E402

FONT = ROOT / "fonts" / "ChalishPilamCeremonial-Regular.ttf"
ENCODING = ROOT / "encodings" / "chalish-ceremonial.json"
BAD = {".notdef", "notdef.box"}

# The passage, block by block in reading order (A1, B1, A2, B2, ...), each block's codage
# with its meaning.
PASSAGE = [
    ("n13*TQAN", "on 13 [day]"),
    ("DAWN", "at dawn"),
    ("n3*JAGUAR:tso1", "Ish'bal Ts'o-"),
    ("ma1*li1", "-malil"),
    ("ki1*ni1", "K'ini"),
    ("LORD", "a lord"),
    ("SEATING", "was seated"),
    ("KANKUL", "at K'ankul"),
    ("WAR", "made war"),
    ("CAPTURE", "took captives"),
    ("TRIBUTE", "tribute brought"),
    ("PRIEST", "the priest"),
    ("OFFERING", "made the offering"),
    ("SUN_PRIEST", "the sun priest"),
    ("SOLAR_COUNT", "kept the count"),
    ("ERA_BEGINS", "an era begins"),
]

# The passage in English.
ENGLISH = (
    "On 13 [day], at dawn, Ish'bal Ts'omalil K'ini, the third of the name, a lord, was seated "
    "at K'ankul. He made war, he took captives, tribute was brought. The priest made the "
    "offering, and the sun priest kept the count. An era begins."
)

PX = 140  # px to the em
COLUMN = 280  # the width of each column, in px
LABEL_GAP = 34  # from a block's descent to its label


def codage() -> str:
    """The passage as one codage string, its blocks separated by spaces."""
    return " ".join(code for code, _ in PASSAGE)


class Face:
    def __init__(self, path: Path):
        self.tt = TTFont(str(path))
        self.gs = self.tt.getGlyphSet()
        self.order = self.tt.getGlyphOrder()
        self.hb = hb.Font(hb.Face(hb.Blob.from_file_path(str(path))))
        self.upem = self.tt["head"].unitsPerEm
        self.ascent = self.tt["hhea"].ascent
        self.descent = self.tt["hhea"].descent

    def shape(self, text: str) -> list[tuple[str, int, int, int]]:
        """(glyph name, x offset, y offset, advance) of each glyph the text shapes to."""
        buf = hb.Buffer()
        buf.add_str(text)
        buf.direction = "ltr"
        buf.script = "Zyyy"
        buf.guess_segment_properties()
        hb.shape(self.hb, buf, {})
        out = []
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            name = self.order[info.codepoint]
            if name in BAD:
                raise SystemExit(f"{FONT.relative_to(ROOT)}: error: U+{ord(text[info.cluster]):05X} shapes to {name}")
            out.append((name, pos.x_offset, pos.y_offset, pos.x_advance))
        return out

    def path(self, name: str) -> str:
        pen = SVGPathPen(self.gs)
        self.gs[name].draw(pen)
        return pen.getCommands()

    def ink(self, shaped) -> tuple[float, float] | None:
        """The left and right edges of the shaped glyphs' ink, in font units."""
        xs, pen_x = [], 0
        for name, dx, _, adv in shaped:
            pen = BoundsPen(self.gs)
            self.gs[name].draw(pen)
            if pen.bounds:
                xs += [pen_x + dx + pen.bounds[0], pen_x + dx + pen.bounds[2]]
            pen_x += adv
        return (min(xs), max(xs)) if xs else None


def draw(sh, face: Face, shaped, x: float, base: float, colour: str):
    sc = PX / face.upem
    pen_x = 0
    for name, dx, dy, adv in shaped:
        d = face.path(name)
        if d:
            sh.out.append(f'<path d="{d}" fill="{colour}" '
                          f'transform="matrix({sc} 0 0 {-sc} {x + (pen_x + dx) * sc:.2f} {base - dy * sc:.2f})"/>')
        pen_x += adv


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default=str(ROOT / "specimens" / "chalish-pilam" / "ceremonial-passage.png"))
    args = ap.parse_args()
    # The sheet's drawing kit loads the stroke generator, which other scripts' tools share
    # a module name with, so it is imported only to draw.
    from strokes_sheet import GREY, INK, Sheet

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    face = Face(FONT)
    encoding = E.load(str(ENCODING))
    whole = E.encode(encoding, codage())
    if E.decode(encoding, whole) != codage():
        raise SystemExit(f"{ENCODING.relative_to(ROOT)}: error: the passage does not read back as written")
    face.shape(whole)

    sc = PX / face.upem
    row_h = (face.ascent - face.descent) * sc + LABEL_GAP + 50
    margin = 40
    width = int(2 * margin + 2 * COLUMN)
    sh = Sheet(width)
    for i, (code, gloss) in enumerate(PASSAGE):
        row, col = divmod(i, 2)
        shaped = face.shape(E.encode(encoding, code))
        left, right = face.ink(shaped)
        x0 = margin + col * COLUMN
        base = margin + row * row_h + face.ascent * sc
        draw(sh, face, shaped, x0 + COLUMN / 2 - (left + right) / 2 * sc, base, INK)
        label_y = base - face.descent * sc + LABEL_GAP
        sh.text(x0 + 10, label_y, f"{'AB'[col]}{row + 1}", 13, GREY)
        sh.text(x0 + 38, label_y, gloss, 13, GREY)
    height = int(margin + -(-len(PASSAGE) // 2) * row_h + margin / 2)
    svg_file = out.with_suffix(".svg")
    svg_file.write_text(sh.svg(height), encoding="utf-8")
    subprocess.run(["rsvg-convert", "-o", str(out), str(svg_file)], check=True)
    print(out.relative_to(ROOT) if out.is_relative_to(ROOT) else out)


if __name__ == "__main__":
    main()
