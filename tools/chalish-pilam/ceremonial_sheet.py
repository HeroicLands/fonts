# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Render the Ch'alish P'ilam ceremonial hand's canon sheet.

    .venv/bin/python tools/chalish-pilam/ceremonial_sheet.py [--out specimens/chalish-pilam/ceremonial.png]

The sheet has four parts: the kit, each recurring part drawn alone in a block; the
pilot glyphs large; the pilot set as an inscription in paired columns, read A1, B1,
A2, B2; and the blocks at 48 and 24 px beside Courier New.
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
import gods as G  # noqa: E402
import ranks as T  # noqa: E402
import events as E  # noqa: E402
import blocks as Q  # noqa: E402
import syllabary as Y  # noqa: E402
import cosmos as K  # noqa: E402
import places as PL  # noqa: E402
import core as Z  # noqa: E402
import compounds as X  # noqa: E402
import strokes as S  # noqa: E402
from strokes_sheet import BLUE, FAINT, GREY, INK, RED, Sheet, svg_path  # noqa: E402

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

    sh.heading("The pilot glyphs: full, half and double footprints; cushion, round cartouche and free silhouette")
    sc = 0.27
    x = 40
    base = sh.y + B * sc + 10
    for g in R.PILOT:
        w = R.WIDTH[g.footprint] * sc
        if x + w > W - 40:
            x = 40
            base += B * sc + 90
        sh.glyph(g.name, g.draw, x, base, sc)
        sh.text(x, base + 24, g.name, 15, INK, weight="bold")
        sh.text(x + max(w, 150) - 4, base + 24, g.sound, 17, RED, weight="bold", anchor="end")
        sh.text(x, base + 42, f"{g.meaning} · {g.footprint}", 12, GREY)
        x += max(w, 160) + 70
    sh.y = base + 80

    sh.heading("The core concepts (with SUN, MOON and WATER above)")
    sc = 0.24
    per = 11
    pitch = (W - 80) / per
    for i, g in enumerate(Z.CORE):
        col, row = i % per, i // per
        x = 40 + col * pitch
        base = sh.y + (row + 1) * (B * sc + 60) - 50
        sh.glyph(g.name, g.draw, x, base, sc)
        sh.text(x, base + 22, g.name, 13, INK, weight="bold")
        sh.text(x, base + 40, g.sound, 12, RED)
    sh.y += ((len(Z.CORE) - 1) // per + 1) * (B * sc + 60) + 10

    sh.heading("Precomposed concepts: what the common hand writes with two or three glyphs, drawn as one")
    sc = 0.24
    per = 11
    pitch = (W - 80) / per
    for i, g in enumerate([R.PATRIARCH] + X.COMPOUNDS):
        col, row = i % per, i // per
        x = 40 + col * pitch
        base = sh.y + (row + 1) * (B * sc + 60) - 50
        sh.glyph(g.name, g.draw, x, base, sc)
        sh.text(x, base + 22, g.name, 11, INK, weight="bold")
    sh.y += ((len(X.COMPOUNDS)) // per + 1) * (B * sc + 60) + 10

    sh.heading("The gods: one glyph each, as complicated as it needs to be")
    sc = 0.3
    x = 40
    base = sh.y + B * sc + 10
    for g in G.GODS:
        w = R.WIDTH[g.footprint] * sc
        if x + w > W - 40:
            x = 40
            base += B * sc + 80
        sh.glyph(g.name, g.draw, x, base, sc)
        sh.text(x, base + 24, g.name, 14, INK, weight="bold")
        sh.text(x, base + 42, f"{g.meaning} · {g.sound}", 12, GREY)
        x += max(w, 200) + 60
    sh.y = base + 70

    sh.heading("Rank and office: a head wearing the regalia of its office")
    sc = 0.27
    x = 40
    base = sh.y + B * sc + 10
    for g in T.RANKS:
        w = R.WIDTH[g.footprint] * sc
        if x + w > W - 40:
            x = 40
            base += B * sc + 80
        sh.glyph(g.name, g.draw, x, base, sc)
        sh.text(x, base + 24, g.name, 13, INK, weight="bold")
        sh.text(x, base + 42, f"{g.meaning.split(',')[0]} · {g.sound}", 12, GREY)
        x += max(w, 200) + 50
    sh.y = base + 70

    sh.heading("The cosmos and the counts")
    sc = 0.27
    x = 40
    base = sh.y + B * sc + 10
    for g in K.COSMOS:
        sh.glyph(g.name, g.draw, x, base, sc)
        sh.text(x, base + 24, g.name, 13, INK, weight="bold")
        sh.text(x, base + 42, f"{g.meaning.split(',')[0]} · {g.sound}", 12, GREY)
        x += B * sc + 120
    sh.y = base + 70

    sh.heading("The city-states: each city's emblem, its picture with the beaded seat of rule; the unruled land has none")
    sc = 0.27
    x = 40
    base = sh.y + B * sc + 10
    for g in PL.PLACES:
        sh.glyph(g.name, g.draw, x, base, sc)
        sh.text(x, base + 24, g.name, 13, INK, weight="bold")
        sh.text(x, base + 42, g.meaning.split(",")[0], 12, GREY)
        x += B * sc + 90
    sh.y = base + 70

    sh.heading("The events of the record")
    sc = 0.27
    x = 40
    base = sh.y + B * sc + 10
    for g in E.EVENTS:
        w = R.WIDTH[g.footprint] * sc
        if x + w > W - 40:
            x = 40
            base += B * sc + 80
        sh.glyph(g.name, g.draw, x, base, sc)
        sh.text(x, base + 24, g.name, 13, INK, weight="bold")
        sh.text(x, base + 42, f"{g.meaning} · {g.sound}", 12, GREY)
        x += max(w, 200) + 50
    sh.y = base + 70

    sh.heading("The syllabary: every syllable's signs, flat (above or below a sign) and tall (before or after it); red: traditional sounds")
    sc = 0.3
    fw, fh = B * Y.SPAN * sc, B * Y.AFFIX * sc
    tw, th = B * Y.AFFIX * sc, B * Y.SPAN * sc
    per = 6
    pitch = (W - 80) / per
    items = list(Y.SIGNS.items())
    for i, (code, sg) in enumerate(items):
        col, row = i % per, i // per
        x = 40 + col * pitch
        base = sh.y + row * (th + 46) + th
        sh.glyph(code + ".tall", sg.tall, x, base, sc)
        sh.glyph(code + ".flat", sg.flat, x + tw + 16, base - (th - fh) / 2, sc)
        sh.text(x, base + 18, code, 13, RED if sg.traditional else INK, weight="bold")
        sh.text(x + 50, base + 18, sg.source[:30], 11, GREY)
    sh.y += ((len(items) - 1) // per + 1) * (th + 46) + 20

    sh.heading("Composed blocks: a name is a house emblem, syllable signs and a coefficient, written in codage")
    sc = 0.32
    x = 40
    base = sh.y + B * sc + 10
    for code, gloss in (("JAGUAR", "the emblem alone, full form"), ("n3*la1:JAGUAR", "three; la over the emblem, compact"),
                        ("sho1*bi1", "the name runs on: sho, bi"), ("la1:JAGUAR:bi1", "la over, bi under; squeezed"),
                        ("n13*JAGUAR", "thirteen before the emblem")):
        sh.cell(x, base, sc)
        sh.glyph(code, lambda code=code: Q.compose(code), x, base, sc)
        sh.text(x, base + 22, code, 13, INK, weight="bold")
        sh.text(x, base + 40, gloss, 12, GREY)
        x += B * sc + 150
    sh.y = base + 70

    sh.heading("An inscription in paired columns, packed by footprint as a page wraps it: two blocks to a row")
    sc = 0.27
    order = [R.LORD, R.PATRIARCH, R.THIRTEEN, R.TQAN, R.SERPENT, R.SUN, R.PEAK, R.MOON, R.WATER, R.JAGUAR]
    rows, cur, used = [], [], 0.0
    for g in order:
        span = R.WIDTH[g.footprint] / B
        if used + span > 2 and cur:
            rows.append(cur)
            cur, used = [], 0.0
        cur.append(g)
        used += span
    rows.append(cur)
    gap = 18
    for r, row in enumerate(rows):
        base = sh.y + (r + 1) * (B * sc + gap)
        x = 60
        for g in row:
            sh.glyph(g.name, g.draw, x, base, sc)
            x += R.WIDTH[g.footprint] * sc + gap
    tx = 60 + 2 * B * sc + 2 * gap + 40
    for k, line in enumerate(["the lord, the patriarch;", "on the thirteenth day of the count;", "the serpent;",
                              "the sun, the sacred peak;", "the moon, the water;", "the jaguar"]):
        sh.text(tx, sh.y + 60 + k * 24, line, 16, GREY)
    sh.y += len(rows) * (B * sc + gap) + 50

    sh.heading("Blocks beside Courier New at 48 and 24 px, set as the font sets them: spanning descender to ascender")
    for px in (48, 24):
        sc = px / 1000
        gs = sc * R.FONT_SCALE
        base = sh.y + px * 1.2
        sh.rule(40, W - 40, base - 945 * sc, FAINT)
        sh.rule(40, W - 40, base + 200 * sc, FAINT)
        x = 40 + sh.latin(40, base, "The stela reads ", px, BLUE)
        for g in order:
            sh.glyph(g.name, g.draw, x, base - R.FONT_DROP * sc, gs)
            x += (R.WIDTH[g.footprint] + 60) * gs
        sh.latin(x + px * 0.3, base, "and the jaguar.", px, BLUE)
        sh.y += px * 1.9

    height = int(sh.y + 40)
    svg_file = out.with_suffix(".svg")
    svg_file.write_text(sh.svg(height))
    subprocess.run(["rsvg-convert", "-o", str(out), str(svg_file)], check=True)
    print(out)


if __name__ == "__main__":
    main()
