# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Render the Helónika stroke sheet from the stroke generator.

    .venv/bin/python tools/helonika/specimens.py [--out specimens/helonika/strokes.png]

The sheet has six parts: every stroke large, with its entry and exit marked; each
stroke across its permitted ranges; every stroke at 24 px to the em; the rough
letter skeletons and the stroke tests at display size; the same run on as lines
at 48, 24 and 18 px; and the minuscules beside Semaron Kuriale and Latin at one
size, on one x-height. One skeleton is drawn over its own centreline.
"""

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "tools"))
import sketches as K  # noqa: E402
import strokes as S  # noqa: E402
from render import latin_font  # noqa: E402

PAPER = (243, 239, 228)
INK = (28, 34, 40)
GREY = (118, 112, 100)
RULE = (212, 202, 180)
FAINT = (228, 220, 202)
GREEN = (40, 130, 80)
BLUE = (40, 90, 170)
RED = (176, 48, 36)
SS = 3
LABEL_FONT = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
SEMARON_FONT = ROOT / "fonts/SemaronKuriale-Regular.ttf"
SEMARON_ORDER = "a b d e f g h i j k l m n o p r s t u v w y z".split()


def font(size, path=LABEL_FONT):
    try:
        return ImageFont.truetype(str(path), size)
    except OSError:
        return ImageFont.load_default()


def semaron(text):
    """Roman minuscules as Semaron Kuriale's own code points."""
    return "".join(" " if c == " " else chr(0xF0230 + SEMARON_ORDER.index(c)) for c in text)


def draw_path(img, path, ox, oy, scale, color=INK):
    """Paint ``path`` (font units, y up) with its origin at pixel (ox, oy)."""
    polys = S.contours(path)
    if not polys:
        return
    xs = [x for p in polys for x, _ in p]
    ys = [y for p in polys for _, y in p]
    x0, x1 = min(xs) * scale + ox - 2, max(xs) * scale + ox + 2
    y0, y1 = oy - max(ys) * scale - 2, oy - min(ys) * scale + 2
    w, h = int((x1 - x0) * SS) + 2, int((y1 - y0) * SS) + 2
    mask = Image.new("1", (w, h), 0)
    for poly in polys:
        layer = Image.new("1", (w, h), 0)
        pts = [((x * scale + ox - x0) * SS, (oy - y * scale - y0) * SS) for x, y in poly]
        if len(pts) >= 3:
            ImageDraw.Draw(layer).polygon(pts, fill=1)
        mask = ImageChops.logical_xor(mask, layer)
    mask = mask.convert("L").resize((max(1, w // SS), max(1, h // SS)), Image.LANCZOS)
    img.paste(Image.new("RGB", mask.size, color), (int(x0), int(y0)), mask)


def guides(d, x0, x1, oy, scale, caps=True):
    """The line and the body, and in full the cap height, ascender and descender."""
    levels = [(0, RULE), (S.X, RULE)]
    if caps:
        levels += [(S.CAP, FAINT), (S.ASC, (232, 214, 200)), (S.DESC, FAINT)]
    for v, c in levels:
        y = oy - v * scale
        d.line([(x0, y), (x1, y)], fill=c, width=1)


def bounds_x(tracks):
    xs = [x for t in tracks for x, *_ in t.samples]
    return min(xs) - S.HALF_W, max(xs) + S.HALF_W


def dot(d, x, y, c, r=6):
    d.ellipse([x - r, y - r, x + r, y + r], fill=c)


def skeleton(d, tracks, ox, oy, scale, color=RED):
    for t in tracks:
        d.line([(ox + x * scale, oy - y * scale) for x, y, *_ in t.samples], fill=color, width=2)


# Where a stroke is shown in its cell, when its origin is not a foot on the line.
CELL_ORIGIN = {"lead": (0, S.X), "knob": (0, S.X / 2)}


def variants(st, n=11):
    """(label, parameters) pairs over a stroke's ranges: the default, then each parameter
    at its two ends, the others at their defaults."""
    base = {k: v[1] for k, v in st.params.items()}
    out = [("default", dict(base))]
    for k, (lo, mid, hi) in st.params.items():
        vals = [v for v in range(lo, hi + 1) if v or lo >= 0] if isinstance(lo, int) else (lo, hi)
        for v in vals:
            if v == mid:
                continue
            p = dict(base)
            p[k] = v
            out.append((f"{k} {v:g}", p))
    return out[:n]


def run_line(img, placed, x, oy, scale):
    for path, dx in placed:
        draw_path(img, path, x + dx * scale, oy, scale)


def sheet(out: Path):
    W = 2400
    ids = list(S.STROKES)
    cell = 290
    cols = W // cell
    inv_rows = -(-len(ids) // cols)
    row_h = 230
    H = 400 + inv_rows * (cell + 80) + 120 + len(ids) * row_h + 3000 + 2400
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.text((40, 30), "Helónika Book — layer 1: the pen strokes", fill=INK, font=font(46))
    d.text((40, 94), "Written left to right, upright, with a broad reed cut square and held nearly flat, edge at 10°: "
           "heavy uprights, hairline crossbars, about 3 : 1. Weight follows direction, never pressure.",
           fill=GREY, font=font(22))
    d.text((40, 126), "Drawn from tools/helonika/strokes.py at the face's own size. Guides, in the stroke cells: the line, "
           "the body (513), the ascender (600, rose), the cap height (730) and the descender (−190), faint.",
           fill=GREY, font=font(22))
    d.text((40, 158), "Green dot: where the pen enters. Blue dot: where it leaves. Skeletons are rough, to judge the hand; "
           "tests are strokes set together, not letters of the script.", fill=RED, font=font(22))

    # -- part 1: the inventory, large
    y = 220
    sc = 0.30
    for i, sid in enumerate(ids):
        st = S.STROKES[sid]
        cx = 20 + (i % cols) * cell
        cy = y + (i // cols) * (cell + 80)
        d.rectangle([cx + 8, cy, cx + cell - 8, cy + cell], outline=RULE)
        ax, ay = CELL_ORIGIN.get(sid, (0, 0))
        sh = S.shape(sid, ax, ay)
        oy = cy + cell * 0.80
        lo, hi = bounds_x(sh.tracks)
        ox = cx + cell / 2 - (lo + hi) / 2 * sc
        guides(d, cx + 10, cx + cell - 10, oy, sc)
        if sid in ("arch", "lobe", "foot", "lead"):
            draw_path(img, S.stroke("stem", 0, 0), ox, oy, sc, color=(190, 182, 166))
        if sid in ("accent", "length"):
            draw_path(img, S.stroke("round", -0.4 * S.X, 0, w=0.8 * S.X), ox, oy, sc, color=(190, 182, 166))
        if sid == "knob":
            draw_path(img, S.stroke("bar", -200, 0, w=200 + S.KNOB_IN, at=S.X / 2), ox, oy, sc, color=(190, 182, 166))
        draw_path(img, S.outline(sh.tracks), ox, oy, sc)
        dot(d, ox + sh.entry[0] * sc, oy - sh.entry[1] * sc, GREEN, 5)
        dot(d, ox + sh.exit[0] * sc, oy - sh.exit[1] * sc, BLUE, 4)
        d.text((cx + 12, cy + cell + 6), sid, fill=INK, font=font(22))
        d.text((cx + 12, cy + cell + 34), f"{st.name} · {st.kind}", fill=GREY, font=font(18))
    y += inv_rows * (cell + 80) + 30

    # -- part 2: each stroke across its ranges
    d.text((40, y), "Each stroke across its permitted ranges", fill=INK, font=font(32))
    y += 56
    sc = 0.2
    for sid in ids:
        st = S.STROKES[sid]
        d.line([(40, y + row_h - 6), (W - 40, y + row_h - 6)], fill=RULE)
        d.text((40, y + 80), sid, fill=INK, font=font(22))
        x = 230
        for label, params in variants(st):
            sh = S.shape(sid, 0, 0, **params)
            lo, hi = bounds_x(sh.tracks)
            ox = x + 95 - (lo + hi) / 2 * sc
            oy = y + row_h * 0.72
            draw_path(img, S.outline(sh.tracks), ox, oy, sc)
            d.text((x + 6, y + row_h - 30), label, fill=GREY, font=font(16))
            x += 196
        y += row_h

    # -- part 3: every stroke at 24 px
    y += 30
    d.text((40, y), "Every stroke at 24 px to the em, in inventory order", fill=INK, font=font(32))
    y += 60
    px = 24
    sc = px / 1000
    x = 60
    oy = y + 22
    for sid in ids:
        sh = S.shape(sid, 0, 0)
        lo, hi = bounds_x(sh.tracks)
        draw_path(img, S.outline(sh.tracks), x - lo * sc, oy, sc)
        x += (hi - lo) * sc + 14
    y += 70

    # -- part 4: skeletons and tests at display size
    y += 20
    d.text((40, y), "Rough skeletons of the six letters that echo Greek: o, th, ō, p, d, l, and the raised dot",
           fill=INK, font=font(32))
    y += 60
    for row, sc in ((K.CAPITALS, 0.42), (K.MINUSCULES + ["·"], 0.42)):
        oy = y + 400
        guides(d, 40, W - 40, oy, sc)
        x = 60
        for name in row:
            trs = K.tracks(K.SKETCHES[name])
            lo, hi = bounds_x(trs)
            ox = x + S.BEARING * sc - lo * sc
            draw_path(img, S.outline(trs), ox, oy, sc)
            d.text((x + 10, oy + 100), name, fill=GREY, font=font(20))
            x += (hi - lo + 2 * S.BEARING) * sc + 60
        y += 520

    d.text((40, y), "Tests — strokes set together; not letters of the script", fill=INK, font=font(32))
    y += 60
    sc = 0.36
    oy = y + 300
    guides(d, 40, W - 40, oy, sc)
    x = 60
    for name, build in K.TESTS.items():
        trs = K.tracks(build)
        lo, hi = bounds_x(trs)
        ox = x - lo * sc
        draw_path(img, S.outline(trs), ox, oy, sc)
        d.text((x, oy + 90), name, fill=GREY, font=font(16))
        x += max((hi - lo) * sc, 170) + 100
    y += 420

    # -- part 5: body sizes
    d.text((40, y), "The skeletons run on as lines at 48, 24 and 18 px to the em", fill=INK, font=font(32))
    y += 60
    lines = [
        ["O", "TH", "Ō", " ", "P", "D", "L", "·", " ", "th", "o", "d", " ", "p", "ō", "l", " ", "l", "o", "p", "·"],
        ["d", "o", "l", " ", "p", "o", "th", " ", "ō", "l", "o", " ", "d", "ō", "p", "·", " ", "TH", "o", "l", " ",
         "p", "o", "d", "·"],
    ]
    runs = [K.setting(line) for line in lines]
    for px in (48, 24, 18):
        sc = px / 1000
        d.text((40, y), f"{px} px", fill=GREY, font=font(18))
        for k in range(2):
            oy = y + px + 6
            x = 120
            while x < W - 200:
                placed, adv = runs[k]
                if x + adv * sc > W - 40:
                    break
                run_line(img, placed, x, oy, sc)
                x += adv * sc + S.SPACE * sc
            y += px * 1.7
        y += 30

    # -- part 6: beside Semaron Kuriale and Latin
    y += 20
    d.text((40, y), "One x-height: Helónika, Semaron Kuriale and Latin (Liberation Mono) at the same size, on one line",
           fill=INK, font=font(32))
    y += 60
    words = ["o", "d", "o", "l", " ", "p", "o", "th", "o", "l", " ", "ō", "p", "o", "d", "·"]
    for px in (120, 24):
        sc = px / 1000
        oy = y + int(px * 0.85) + 10
        if px >= 60:
            for v in (0, S.X):
                d.line([(40, oy - v * sc), (W - 40, oy - v * sc)], fill=(222, 170, 160), width=1)
        x = 60
        placed, adv = K.setting(words)
        run_line(img, placed, x, oy, sc)
        x += adv * sc + 60 * px / 120
        for word in ("selan", "vyra", "tolde"):
            d.text((x, oy), semaron(word), fill=INK, font=font(px, SEMARON_FONT), anchor="ls")
            x += d.textlength(semaron(word), font=font(px, SEMARON_FONT)) + S.SPACE * sc
        x += 60 * px / 120
        d.text((x, oy), "the book hand", fill=INK, font=latin_font(px), anchor="ls")
        y += int(px * 1.3) + 30
    d.text((40, y), "Helónika skeletons, then Semaron Kuriale, then Latin. The rose rules are the line and 0.5135 em.",
           fill=GREY, font=font(18))
    y += 60

    # -- part 7: the skeleton under the ink
    d.text((40, y), "The minuscule d and th and the capital Ō over their own centrelines (red)", fill=INK, font=font(32))
    y += 50
    sc = 0.6
    oy = y + 480
    x = 80
    for name in ("d", "th", "Ō"):
        trs = K.tracks(K.SKETCHES[name])
        lo, hi = bounds_x(trs)
        ox = x - lo * sc
        draw_path(img, S.outline(trs), ox, oy, sc)
        skeleton(d, trs, ox, oy, sc)
        x += (hi - lo) * sc + 120
    y += 600

    img = img.crop((0, 0, W, int(y + 30)))
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=ROOT / "specimens/helonika/strokes.png")
    print(sheet(ap.parse_args().out))


if __name__ == "__main__":
    main()
