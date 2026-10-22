# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Render the Teng Chou stroke sheet from the stroke generator.

    .venv/bin/python tools/teng-chou/specimens.py [--out specimens/teng-chou/strokes.png]

The sheet has three parts. Each stroke of the inventory, large, with its id and
name, the novel ones marked. A row per stroke at several lengths and angles from
its permitted range. And a test set: made-up characters assembled by hand from
the strokes, which are tests of the strokes and not characters of the script,
shown large and set as a line of text at body sizes.
"""

import argparse
import random
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
import strokes as S  # noqa: E402
import tests as T  # noqa: E402

PAPER = (244, 238, 224)
INK = (24, 21, 19)
GREY = (118, 110, 98)
RULE = (205, 192, 165)
RED = (168, 40, 30)
SS = 3
LABEL_FONT = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"


def font(size):
    try:
        return ImageFont.truetype(LABEL_FONT, size)
    except OSError:
        return ImageFont.load_default()


def draw_path(img: Image.Image, path, ox, oy, scale, color=INK):
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
    ink = Image.new("RGB", mask.size, color)
    img.paste(ink, (int(x0), int(y0)), mask)


def centred(path, cx, cy, scale):
    """The origin that centres ``path``'s bounds on pixel (cx, cy)."""
    xmin, ymin, xmax, ymax = path.bounds
    return cx - (xmin + xmax) / 2 * scale, cy + (ymin + ymax) / 2 * scale


def em_box(d: ImageDraw.ImageDraw, x, y, size):
    d.rectangle([x, y, x + size, y + size], outline=RULE, width=1)


def sheet(out: Path):
    W = 2400
    ids = list(S.STROKES)
    cell = 230
    cols = W // cell
    inv_rows = -(-len(ids) // cols)
    row_h = 230
    test_h = 1700
    H = 150 + inv_rows * (cell + 70) + 80 + len(ids) * row_h + test_h
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.text((40, 30), "Teng Chou — layer 1: the strokes", fill=INK, font=font(46))
    d.text((40, 92), f"{len(ids)} strokes. Red ids are the strokes Chinese lacks. "
           "Drawn from tools/teng-chou/strokes.py; each square is one em.", fill=GREY, font=font(24))

    # -- part 1: the inventory, large
    y = 150
    scale = (cell - 40) / 1000
    for i, sid in enumerate(ids):
        st = S.STROKES[sid]
        cx = 20 + (i % cols) * cell
        cy = y + (i // cols) * (cell + 70)
        em_box(d, cx + 20, cy, cell - 40)
        defaults = {k: v[1] for k, v in st.params.items()}
        path = S.stroke(sid, 0, 0, **defaults)
        ox, oy = centred(path, cx + cell / 2, cy + (cell - 40) / 2, scale)
        draw_path(img, path, ox, oy, scale)
        colour = RED if st.novel else INK
        d.text((cx + 20, cy + cell - 32), sid, fill=colour, font=font(22))
        d.text((cx + 20, cy + cell - 6), st.name, fill=GREY, font=font(19))
    y += inv_rows * (cell + 70) + 40

    # -- part 2: each stroke across its range
    d.text((40, y), "Each stroke across its permitted lengths and angles", fill=INK, font=font(32))
    y += 50
    rs = 0.2
    for sid in ids:
        st = S.STROKES[sid]
        d.line([(40, y + row_h - 8), (W - 40, y + row_h - 8)], fill=RULE)
        d.text((40, y + 80), sid, fill=RED if st.novel else INK, font=font(22))
        x = 250
        for label, params in variants(st):
            path = S.stroke(sid, 0, 0, **params)
            ox, oy = centred(path, x + 90, y + row_h / 2 - 18, rs)
            draw_path(img, path, ox, oy, rs)
            d.text((x + 10, y + row_h - 36), label, fill=GREY, font=font(16))
            x += 192
        y += row_h

    # -- part 3: the tests
    y += 30
    d.text((40, y), "Test set — made-up characters assembled by hand to test the strokes; "
           "they are not characters of the script", fill=INK, font=font(30))
    y += 56
    tests = T.TESTS
    big = 300
    for i, (name, parts) in enumerate(tests):
        x = 40 + i * (big + 34)
        em_box(d, x, y, big)
        path = T.assemble(parts)
        draw_path(img, path, x, y + big, big / 1000)
        d.text((x, y + big + 8), f"{name} · {T.count(parts)} strokes", fill=GREY, font=font(20))
    y += big + 70
    shapes = [T.assemble(parts) for _, parts in tests]
    order = random.Random(12)
    for px, lines in ((64, 1), (32, 2), (20, 3), (14, 3)):
        d.text((40, y + px * 0.3), f"{px} px", fill=GREY, font=font(18))
        for _ in range(lines):
            x = 130
            while x + px < W - 40:
                draw_path(img, order.choice(shapes), x, y + px, px / 1000)
                x += px * 1.04
            y += px * 1.5
        y += 24
    img = img.crop((0, 0, W, int(y + 40)))
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)
    return out


def variants(st, n=11):
    """(label, parameters) pairs spread over a stroke's ranges: the default, then each
    parameter in turn at its two ends and between them, the others at their defaults."""
    base = {k: v[1] for k, v in st.params.items()}
    out = [("default", dict(base))]
    for k, (lo, mid, hi) in st.params.items():
        for v in (lo, hi) if len(st.params) > 2 else (lo, (lo + mid) / 2, (mid + hi) / 2, hi):
            p = dict(base)
            p[k] = v
            out.append((f"{k} {v:g}", p))
    return out[:n]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=ROOT / "specimens/teng-chou/strokes.png")
    args = ap.parse_args()
    print(sheet(args.out))


if __name__ == "__main__":
    main()
