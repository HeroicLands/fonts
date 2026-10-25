# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Render the Ch'alish P'ilam common hand's stroke sheet from the stroke generator.

    .venv/bin/python tools/chalish-pilam/strokes_sheet.py [--out specimens/chalish-pilam/strokes.png]

The sheet has six parts: every stroke large, in its cell; every stroke at 24 and 48 px
to the em after Monaspace Neon's "xHn"; rough signs built from the strokes, a test of
how they sit together in the cell; bar-and-dot counts, 1 to 19; a page of paired
columns with its reading order, the implied cells drawn on one column only; and runs of
the rough signs at 96, 48 and 24 px beside a Latin sentence in Monaspace Neon at one
font size. The rough signs are not signs of the script.
"""

import argparse
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
import strokes as S  # noqa: E402
from fontTools.pens.svgPathPen import SVGPathPen  # noqa: E402
from fontTools.ttLib import TTFont  # noqa: E402

PAPER = "#f7f3eb"
INK = "#1c1814"
GREY = "#786f68"
RULE = "#d4cab8"
FAINT = "#e6dece"
CELL = "#c9b9a0"
RED = "#a8301f"
BLUE = "#285aaa"
LABEL = "Helvetica, Arial, sans-serif"
LATIN_TT = TTFont(str(Path.home() / "Library/Fonts/MonaspaceNeon-Regular.otf"))  # the face the shared metrics come from
B = S.BLOCK
M = 80.0  # the white inside a cell, a side, that keeps two neighbouring signs apart
ADVANCE = B + 2 * 60.0  # every sign takes one advance: the cell and its gutter
LO, HI = M, B - M  # the ink's reach inside a cell, both ways


def svg_path(path, ox, oy, scale):
    """SVG path data for ``path`` (font units, y up) with its origin at (ox, oy)."""
    d = []
    for c in S.contours(path):
        d.append("M" + " L".join(f"{ox + x * scale:.2f},{oy - y * scale:.2f}" for x, y in c) + "Z")
    return " ".join(d)


class Sheet:
    def __init__(self, width):
        self.w = width
        self.y = 0
        self.out = []
        self.defs = {}

    def text(self, x, y, s, size=14, color=INK, weight="normal", anchor="start"):
        s = s.replace("&", "&amp;").replace("<", "&lt;")
        self.out.append(f'<text x="{x}" y="{y}" font-family="{LABEL}" font-size="{size}" fill="{color}" '
                        f'font-weight="{weight}" text-anchor="{anchor}">{s}</text>')

    def ink(self, key, make, ox, oy, scale, color=INK):
        """Ink ``make()`` once with the common pen, and place it by reference wherever it recurs."""
        if key not in self.defs:
            self.defs[key] = f"g{len(self.defs)}"
            p = S.ink(make(), S.COMMON)
            self.out.insert(0, f'<defs><path id="{self.defs[key]}" d="{svg_path(p, 0, 0, 1)}"/></defs>')
        self.out.append(f'<use href="#{self.defs[key]}" fill="{color}" '
                        f'transform="matrix({scale} 0 0 {scale} {ox:.2f} {oy:.2f})"/>')

    def latin(self, x, base, s, px, color=BLUE):
        """Set ``s`` in Monaspace Neon Regular from its font file; return the advance in px."""
        sc = px / LATIN_TT["head"].unitsPerEm
        cmap, gs, hmtx = LATIN_TT.getBestCmap(), LATIN_TT.getGlyphSet(), LATIN_TT["hmtx"]
        xx = x
        for ch in s:
            g = cmap.get(ord(ch))
            if g is None:
                continue
            pen = SVGPathPen(gs)
            gs[g].draw(pen)
            d = pen.getCommands()
            if d:
                self.out.append(f'<path d="{d}" fill="{color}" transform="matrix({sc} 0 0 {-sc} {xx:.2f} {base:.2f})"/>')
            xx += hmtx[g][0] * sc
        return xx - x

    def rule(self, x0, x1, y, color=RULE):
        self.out.append(f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{color}" stroke-width="1"/>')

    def cell(self, x, base, scale, color=CELL):
        """The implied cell, dashed: the sheet draws it; the hand never does."""
        self.out.append(f'<rect x="{x:.2f}" y="{base - B * scale:.2f}" width="{B * scale:.2f}" height="{B * scale:.2f}" '
                        f'fill="none" stroke="{color}" stroke-dasharray="4 4"/>')

    def heading(self, s):
        self.y += 34
        self.text(40, self.y, s, 20)
        self.y += 18

    def svg(self, height):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{height}" '
                f'viewBox="0 0 {self.w} {height}"><rect width="100%" height="100%" fill="{PAPER}"/>'
                + "".join(self.out) + "</svg>")


C = B / 2

# -- the strokes, each in its cell -----------------------------------------------------------------

STROKES = [
    ("stem", "an upright", lambda: S.bar(C, LO, C, HI)),
    ("bar", "a level stroke", lambda: S.bar(LO, C, HI, C)),
    ("slash", "rising to the right", lambda: S.bar(LO + 60, LO, HI - 60, HI)),
    ("fall", "falling to the right", lambda: S.bar(LO + 60, HI, HI - 60, LO)),
    ("corner", "across, then down", lambda: S.corner(LO + 40, HI - 40, HI - 40, LO + 40)),
    ("tick", "a short mark", lambda: S.tick(C, C - 90, 180)),
    ("dot", "a dab", lambda: S.dot(C, C, 42)),
    ("ring", "a closed circle", lambda: S.ring(C, C, 150)),
    ("arc", "an open bowl", lambda: S.arc(C, C - 140, 230, 230, 25, 155)),
    ("hook", "three quarters of a circle", lambda: S.hook(C, C, 200, opening=0)),
    ("curl", "a spiral wound inward", lambda: S.curl(C, C, 220)),
    ("wave", "a running S", lambda: S.wave(LO + 20, C, HI - 20, 90, periods=1.5)),
]


# -- rough signs: tests of how the strokes fill a cell; not signs of the script --------------------

ROUGH = [
    ("a stem crossed by two bars",
     lambda: S.bar(C, LO, C, HI) + S.bar(LO + 60, C + 120, HI - 60, C + 120) + S.bar(LO + 120, C - 120, HI - 120, C - 120)),
    ("a ring over a bar",
     lambda: S.ring(C, C + 110, 160) + S.bar(LO, LO + 70, HI, LO + 70)),
    ("a curl beside a stem",
     lambda: S.bar(LO + 70, LO, LO + 70, HI) + S.curl(C + 90, C, 190)),
    ("a hook holding a dot",
     lambda: S.hook(C, C, 250, opening=90) + S.dot(C, C - 30, 46)),
    ("two waves under an arc",
     lambda: S.arc(C, C, 260, 230, 25, 155) + S.wave(LO + 20, C - 40, HI - 20, 55, 1.5)
     + S.wave(LO + 20, LO + 70, HI - 20, 55, 1.5)),
    ("a corner over a ring",
     lambda: S.corner(LO, HI, HI, C + 40) + S.ring(C - 60, C - 100, 130)),
    ("a tent over a bar",
     lambda: S.bar(LO + 40, LO + 150, C, HI) + S.bar(C, HI, HI - 40, LO + 150) + S.bar(LO, LO + 40, HI, LO + 40)),
    ("three ticks over a wave",
     lambda: sum((S.tick(LO + 110 + i * 175, C + 20, 170) for i in range(3)), []) + S.wave(LO + 20, LO + 110, HI - 20, 60, 1.5)),
    ("a ring in a hook, with a tick",
     lambda: S.hook(C + 30, C, 250, opening=180) + S.ring(C + 30, C, 90) + S.tick(LO + 20, HI - 160, 160, angle=90)),
    ("a stem and a curl on a bar",
     lambda: S.bar(LO + 90, LO + 100, LO + 90, HI) + S.curl(C + 100, C + 100, 150, clockwise=True)
     + S.bar(LO, LO + 40, HI, LO + 40)),
]


def numeral(n):
    """Bar-and-dot in the common line: a bar for each five, stacked from the bottom, and a
    dot for each one above them."""
    bars, dots = divmod(n, 5)
    out = []
    y = LO + 30
    for _ in range(bars):
        out += S.bar(LO + 40, y, HI - 40, y)
        y += 120
    if dots:
        gap = 120
        x0 = C - (dots - 1) * gap / 2
        out += [f for i in range(dots) for f in S.dot(x0 + i * gap, y + 20, 38)]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "specimens/chalish-pilam/strokes.png"))
    args = ap.parse_args()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    W = 2400
    sh = Sheet(W)
    sh.y = 50
    sh.text(40, sh.y, "Ch'alish P'ilam, the common hand — layer 1: the strokes", 36)
    sh.y += 34
    for line in [
        "Written in plain lines: chalk on a shaft wall or slate, a point on a wooden palette, a stylus on bark paper, a pen or brush "
        f"on vellum. One even line, {S.COMMON.full:.0f} units; weight never tells two signs apart.",
        f"Every sign fills a square cell, {B:.0f} units, Latin's cap height, that is never drawn: the dashed square is the sheet's, "
        f"not the hand's. Every sign takes one advance, {ADVANCE:.0f} units.",
        "Signs are read in rows of two, left to right, down a column two cells wide. Drawn from tools/chalish-pilam/strokes.py.",
    ]:
        sh.text(40, sh.y, line, 15, GREY)
        sh.y += 21
    sh.text(40, sh.y, "The rough signs test how the strokes sit together in a cell. They are not signs of the script.", 15, RED)
    sh.y += 20

    # -- part 1: every stroke
    sh.heading("The strokes")
    scale = 0.3
    cw = B * scale
    per_row = 8
    pitch = (W - 80) / per_row
    for i, (name, gloss, fn) in enumerate(STROKES):
        col, row = i % per_row, i // per_row
        if col == 0 and row:
            sh.y += cw + 70
        x = 40 + col * pitch
        base = sh.y + cw + 10
        sh.cell(x, base, scale)
        sh.ink(name, fn, x, base, scale)
        sh.text(x, base + 24, name, 15, INK, weight="bold")
        sh.text(x, base + 42, gloss, 12, GREY)
    sh.y += cw + 70

    # -- part 2: at 24 and 48 px
    sh.heading("Every stroke at 24 and 48 px to the em, after Monaspace Neon's “xHn” at the same size")
    for px in (24, 48):
        sc = px / 1000
        base = sh.y + px + 6
        x = 40 + sh.latin(40, base, "xHn", px) + px * 0.3
        for name, _, fn in STROKES:
            sh.ink(name, fn, x, base, sc)
            x += ADVANCE * sc
        sh.y += px + 22

    # -- part 3: rough signs
    sh.heading("Rough signs built from the strokes, each in its cell — tests of how they sit together; not signs")
    scale = 0.3
    per_row = 5
    pitch = (W - 80) / per_row
    for i, (name, fn) in enumerate(ROUGH):
        col, row = i % per_row, i // per_row
        if col == 0 and row:
            sh.y += cw + 60
        x = 40 + col * pitch
        base = sh.y + cw + 10
        sh.cell(x, base, scale)
        sh.ink(f"rough{i}", fn, x, base, scale)
        sh.text(x, base + 24, name, 13, GREY)
    sh.y += cw + 60

    # -- part 4: bar and dot
    sh.heading("The bar-and-dot test: 1 to 19 in the common line — a test of the strokes; not the numerals")
    sc = 0.12
    base = sh.y + B * sc + 10
    for n in range(1, 20):
        x = 40 + (n - 1) * (ADVANCE * sc + 20)
        sh.cell(x, base, sc, FAINT)
        sh.ink(f"num{n}", lambda n=n: numeral(n), x, base, sc)
        sh.text(x + B * sc / 2, base + 22, str(n), 12, GREY, anchor="middle")
    sh.y += B * sc + 50

    # -- part 5: a page of paired columns
    sh.heading("A page of paired columns: rows of two, left to right, down the column; then the next column. "
               "Cells drawn on the first column only")
    sc = 0.11
    rows, cols = 8, 5
    colgap = 70
    colw = 2 * ADVANCE * sc
    linep = ADVANCE * sc * 1.15
    order = 0
    for c in range(cols):
        x0 = 40 + c * (colw + colgap)
        for r in range(rows):
            for k in range(2):
                x = x0 + k * ADVANCE * sc
                base = sh.y + (r + 1) * linep
                if c == 0:
                    sh.cell(x, base, sc)
                sh.ink(f"rough{order % len(ROUGH)}", ROUGH[order % len(ROUGH)][1], x, base, sc)
                if c == 0:
                    sh.text(x + B * sc / 2, base + 13, str(order + 1), 10, RED, anchor="middle")
                order += 1
    sh.text(40 + cols * (colw + colgap), sh.y + 40, "read down the first column, two at a time,", 14, GREY)
    sh.text(40 + cols * (colw + colgap), sh.y + 60, "then down the next", 14, GREY)
    sh.y += rows * linep + 40

    # -- part 6: runs beside Latin
    sh.heading("Rough signs run on beside Monaspace Neon at one font size; faint rules: Latin's x-height and cap height")
    sentence = "Rows of two."
    for px in (96, 48, 24):
        sc = px / 1000
        base = sh.y + px * 0.85 + 8
        sh.rule(40, W - 40, base - S.LATIN_X * sc, FAINT)
        sh.rule(40, W - 40, base - 730 * sc, FAINT)
        x = 40 + sh.latin(40, base, sentence, px) + px * 0.5
        i = 0
        while x + B * sc < W - 40:
            sh.ink(f"rough{i % len(ROUGH)}", ROUGH[i % len(ROUGH)][1], x, base, sc)
            x += ADVANCE * sc
            i += 1
        sh.y += px * 1.3 + 10

    height = int(sh.y + 40)
    svg_file = out.with_suffix(".svg")
    svg_file.write_text(sh.svg(height))
    subprocess.run(["rsvg-convert", "-o", str(out), str(svg_file)], check=True)
    print(out)


if __name__ == "__main__":
    main()
