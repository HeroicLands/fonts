# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Render the Ch'alish P'ilam ceremonial hand's canon sheet.

    .venv/bin/python tools/chalish-pilam/ceremonial_sheet.py [--out specimens/chalish-pilam/ceremonial.png]

The sheet has four parts: the kit, each recurring part drawn alone in a block; the
pilot glyphs large; the pilot set as an inscription in paired columns, read A1, B1,
A2, B2; and the blocks at 48 and 24 px beside Monaspace Neon.
"""

import argparse
import zlib
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
import ceremonial as R  # noqa: E402
import strokes as S  # noqa: E402
from strokes_sheet import BLUE, GREY, INK, RED, Sheet, svg_path  # noqa: E402

B = S.BLOCK


class CSheet(Sheet):
    def glyph(self, key, parts_fn, ox, oy, scale):
        if key not in self.defs:
            self.defs[key] = f"g{len(self.defs)}"
            p = R.ink(parts_fn(), seed=zlib.crc32(key.encode()))
            self.out.insert(0, f'<defs><path id="{self.defs[key]}" d="{svg_path(p, 0, 0, 1)}"/></defs>')
        self.out.append(f'<use href="#{self.defs[key]}" fill="{INK}" '
                        f'transform="matrix({scale} 0 0 {scale} {ox:.2f} {oy:.2f})"/>')


C = B / 2
KIT = [
    ("cushion", "the block, always drawn", lambda: [(R.CONTOUR, R.cushion())]),
    ("comb fringe", "hung under a sign", lambda: [(R.DETAIL, R.fringe(80, B - 80, C + 60))]),
    ("dotted line", "tracing an outline", lambda: [(R.DETAIL, R.dotted_arc(C, C - 80, 250, 200, 20, 160))]),
    ("netting", "a cross-hatched field", lambda: [(R.DETAIL, R.net(C - 180, C - 150, 360, 300, n=5))]),
    ("bead", "set beside a sign", lambda: [(R.DETAIL, R.bead(C, C, 80))]),
    ("ear spool", "behind a head", lambda: [(R.DETAIL, R.ear_spool(C, C, 140))]),
    ("the X", "a mark of crossing", lambda: [(R.DETAIL, R.x_mark(C, C, 140))]),
    ("eyes", "open, closed, spiral", lambda: [(R.DETAIL, R.eye(150, C) + R.eye(C, C, "closed") + R.eye(B - 150, C, "spiral"))]),
    ("the head", "facing the line's start", lambda: list(zip((R.CONTOUR, R.DETAIL), R.head()))),
    ("prefix", "a narrow affix before a sign", lambda: [(R.CONTOUR, R.prefix(C - 80, 120, C + 80, B - 120))]),
    ("superfix", "a flattened affix over a sign", lambda: [(R.CONTOUR, R.superfix(80, C - 90, B - 80, C + 90, "fringe"))]),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "specimens/chalish-pilam/ceremonial.png"))
    args = ap.parse_args()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    W = 2400
    sh = CSheet(W)
    sh.y = 50
    sh.text(40, sh.y, "Ch'alish P'ilam, the ceremonial hand — the canon and a pilot", 36)
    sh.y += 34
    for line in [
        "Every glyph is its own picture, drawn whole inside a cushion that always stands round it. Two brushes: the contour "
        f"brush, {R.CONTOUR.full:.0f} units, and the detail brush, {R.DETAIL.full:.0f}.",
        "Heads face the line's start. The kit of recurring parts gives the hand its look; no glyph is built from a skeleton. "
        "Drawn from tools/chalish-pilam/ceremonial.py.",
    ]:
        sh.text(40, sh.y, line, 15, GREY)
        sh.y += 21

    sh.heading("The kit")
    sc = 0.26
    cw = B * sc
    for i, (name, gloss, fn) in enumerate(KIT):
        x = 40 + i * (cw + 70)
        base = sh.y + cw + 10
        sh.cell(x, base, sc)
        sh.glyph(f"kit:{name}", fn, x, base, sc)
        sh.text(x, base + 22, name, 14, INK, weight="bold")
        sh.text(x, base + 40, gloss, 12, GREY)
    sh.y += cw + 70

    sh.heading("The pilot glyphs")
    sc = 0.36
    cw = B * sc
    for i, g in enumerate(R.PILOT):
        x = 40 + i * (cw + 60)
        base = sh.y + cw + 10
        sh.glyph(g.name, g.draw, x, base, sc)
        sh.text(x, base + 24, g.name, 15, INK, weight="bold")
        sh.text(x + cw - 4, base + 24, g.sound, 17, RED, weight="bold", anchor="end")
        sh.text(x, base + 42, g.meaning, 12, GREY)
    sh.y += cw + 80

    sh.heading("An inscription in paired columns: read A1, B1, A2, B2, down the pair")
    sc = 0.3
    cw = B * sc
    order = [R.LORD, R.JAGUAR, R.THIRTEEN, R.SUN, R.PEAK, R.MOON, R.WATER, R.SUN]
    for i, g in enumerate(order):
        row, col = divmod(i, 2)
        x = 60 + col * (cw + 18)
        base = sh.y + (row + 1) * (cw + 18)
        sh.glyph(g.name, g.draw, x, base, sc)
        sh.text(x + cw / 2, base + 16, f"{'AB'[col]}{row + 1}", 12, RED, anchor="middle")
    sh.text(60 + 2 * (cw + 18) + 40, sh.y + 60, "a lord, the jaguar, on the thirteenth;", 16, GREY)
    sh.text(60 + 2 * (cw + 18) + 40, sh.y + 84, "the sun over the sacred peak; the moon on the water; the sun", 16, GREY)
    sh.y += 4 * (cw + 18) + 50

    sh.heading("Blocks beside Monaspace Neon at 48 and 24 px")
    for px in (48, 24):
        sc = px / 1000
        base = sh.y + px
        x = 40 + sh.latin(40, base, "The stela reads ", px, BLUE)
        for g in order:
            sh.glyph(g.name, g.draw, x, base, sc)
            x += (B + 60) * sc
        sh.latin(x + px * 0.3, base, "and the sun.", px, BLUE)
        sh.y += px * 1.6

    height = int(sh.y + 40)
    svg_file = out.with_suffix(".svg")
    svg_file.write_text(sh.svg(height))
    subprocess.run(["rsvg-convert", "-o", str(out), str(svg_file)], check=True)
    print(out)


if __name__ == "__main__":
    main()
