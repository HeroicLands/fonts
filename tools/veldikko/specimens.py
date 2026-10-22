# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Render the Veldikko stroke sheet from the stroke generator.

    .venv/bin/python tools/veldikko/specimens.py [--out specimens/veldikko/strokes.png]

The sheet has five parts: every stroke large, with its entry
and exit marked; each stroke across its permitted ranges; the test sequences at
display size, right to left; the tests run on as lines at body
size; and one test drawn over its own skeleton, so the nib can be read against
the path it follows.
"""

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
import strokes as S  # noqa: E402
import tests as T  # noqa: E402

PAPER = (243, 239, 228)
INK = (28, 34, 40)
GREY = (118, 112, 100)
RULE = (212, 202, 180)
GREEN = (40, 130, 80)
BLUE = (40, 90, 170)
RED = (176, 48, 36)
SS = 3
LABEL_FONT = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"


def font(size):
    try:
        return ImageFont.truetype(LABEL_FONT, size)
    except OSError:
        return ImageFont.load_default()


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


def guides(d, x0, x1, oy, scale, full=True):
    """The line, the waist and, in full, the head and tail heights."""
    levels = [(0, RULE), (S.X, RULE)]
    if full:
        levels += [(S.ASC, (228, 220, 202)), (S.DESC, (228, 220, 202)), (S.MARK, (232, 214, 200))]
    for v, c in levels:
        y = oy - v * scale
        d.line([(x0, y), (x1, y)], fill=c, width=1)


def bounds_x(tracks, style):
    xs = [S.to_page(f, y, style)[0] for t in tracks for f, y, _ in t.samples]
    return min(xs), max(xs)


def dot(d, x, y, c, r=6):
    d.ellipse([x - r, y - r, x + r, y + r], fill=c)


def skeleton(d, tracks, style, ox, oy, scale, color=RED):
    for t in tracks:
        pts = [S.to_page(f, y, style) for f, y, _ in t.samples]
        d.line([(ox + x * scale, oy - y * scale) for x, y in pts], fill=color, width=1)


def place(img, d, tracks, style, x0, x1, oy, scale, rules=True):
    """Draw a run so its right end sits at x1 (it reads from the right); return its left end."""
    path = S.outline(tracks, style)
    lo, hi = bounds_x(tracks, style)
    ox = x1 - hi * scale
    if rules:
        guides(d, x0, x1, oy, scale, full=False)
    draw_path(img, path, ox, oy, scale)
    return ox, ox + lo * scale


def sheet(out: Path):
    W = 2400
    ids = list(S.STROKES)
    cell = 290
    cols = W // cell
    inv_rows = -(-len(ids) // cols)
    row_h = 220
    H = 300 + inv_rows * (cell + 80) + 120 + len(ids) * row_h + 200 + len(T.TESTS) * 700 + 400 + 1400 + 1200
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.text((40, 30), "Veldikko — layer 1: the pen strokes", fill=INK, font=font(46))
    d.text((40, 94), "Written right to left with a narrow, obliquely cut nib, edge at 62°, firm, flexing a little and lifting "
           "to nothing. One hand for Sinale and Áelendi alike.",
           fill=GREY, font=font(22))
    d.text((40, 126), "Drawn from tools/veldikko/strokes.py. Guides, in the stroke cells only: the line, the bowl height, the mark "
           "floor (rose), the raised and lowered stem (faint). A bowl is shown with its stem in grey. Green dot: entry.",
           fill=GREY, font=font(22))
    d.text((40, 158), "Tests set strokes side by side to test how they sit together. They are not letters or words of the script.",
           fill=RED, font=font(22))

    # -- part 1: the inventory, large
    y = 220
    style = S.HAND
    for i, sid in enumerate(ids):
        st = S.STROKES[sid]
        cx = 20 + (i % cols) * cell
        cy = y + (i // cols) * (cell + 80)
        d.rectangle([cx + 8, cy, cx + cell - 8, cy + cell], outline=RULE)
        sh = S.shape(sid, 0, 0, style)
        if st.kind == "mark":
            sc, oy = 0.95, cy + cell * 0.62
        else:
            sc, oy = 0.26, cy + cell * 0.70
        path = S.outline(sh.tracks, style)
        lo, hi = bounds_x(sh.tracks, style)
        ox = cx + cell / 2 - (lo + hi) / 2 * sc
        if st.kind != "mark":
            guides(d, cx + 10, cx + cell - 10, oy, sc)
        if st.kind in ("bowl", "hanging"):
            draw_path(img, S.stroke("stem", 0, 0, style), ox, oy, sc, color=(190, 182, 166))
        draw_path(img, path, ox, oy, sc)
        if st.kind not in ("mark", "join"):
            ex, ey = S.to_page(sh.entry[0], sh.entry[1], style)
            dot(d, ox + ex * sc, oy - ey * sc, GREEN, 5)
        d.text((cx + 12, cy + cell + 6), sid, fill=INK, font=font(22))
        d.text((cx + 12, cy + cell + 34), f"{st.name} · {st.kind}", fill=GREY, font=font(18))
    y += inv_rows * (cell + 80) + 30

    # -- part 2: each stroke across its ranges
    d.text((40, y), "Each stroke across its permitted ranges (Sinale)", fill=INK, font=font(32))
    y += 56
    for sid in ids:
        st = S.STROKES[sid]
        d.line([(40, y + row_h - 6), (W - 40, y + row_h - 6)], fill=RULE)
        d.text((40, y + 70), sid, fill=INK, font=font(22))
        x = 230
        sc = 0.75 if st.kind == "mark" else 0.19
        for label, params in variants(st):
            sh = S.shape(sid, 0, 0, style, **params)
            path = S.outline(sh.tracks, style)
            lo, hi = bounds_x(sh.tracks, style)
            ox = x + 95 - (lo + hi) / 2 * sc
            oy = y + row_h * (0.62 if st.kind == "mark" else 0.66)
            draw_path(img, path, ox, oy, sc)
            d.text((x + 6, y + row_h - 30), label, fill=GREY, font=font(16))
            x += 196
        y += row_h

    # -- part 3: the tests at display size
    y += 40
    d.text((40, y), "Tests at display size — strokes set side by side, no line drawn; not letters or words of the script",
           fill=INK, font=font(32))
    y += 50
    d.text((40, y), "Each test reads from the right.",
           fill=GREY, font=font(22))
    y += 50
    sc = 0.62
    half = W / 2
    for name, units in T.TESTS:
        d.text((40, y), f"test: {name}", fill=RED, font=font(24))
        y += 30
        oy = y + 440
        runs = [(stl, T.assemble(units, stl)) for stl in (S.HAND,)]
        widest = max(bounds_x(tr, stl)[1] - bounds_x(tr, stl)[0] for stl, tr in runs)
        k = min(sc, (half - 140) / widest)
        for col, (stl, tr) in enumerate(runs):
            x0 = 40 + col * half
            place(img, d, tr, stl, x0, x0 + half - 80, oy, k, rules=False)
            d.text((x0, y + 600), stl.name, fill=GREY, font=font(18))
        y += 650
    # -- part 4: body size
    y += 30
    d.text((40, y), "Body size — the tests run on as lines at 48, 24 and 20 px to the em, no line drawn", fill=INK, font=font(32))
    y += 60
    for stl in (S.HAND,):
        runs = [T.assemble(u, stl) for _, u in T.TESTS]
        for px in (48, 24, 20):
            scale = px / 1000
            d.text((40, y), f"{stl.name}, {px} px", fill=GREY, font=font(18))
            right = W - 60
            for line in range(2 if px < 40 else 1):
                oy = y + px * 1.0 + 4
                x1 = right
                k = line
                while True:
                    tr = runs[k % len(runs)]
                    lo, hi = bounds_x(tr, stl)
                    if x1 - (hi - lo) * scale < 260:
                        break
                    ox = x1 - hi * scale
                    draw_path(img, S.outline(tr, stl), ox, oy, scale)
                    x1 = ox + lo * scale - px * 0.45
                    k += 1
                y += px * 1.6
            y += 26
        y += 20

    # -- part 5: the skeleton under the ink
    y += 20
    d.text((40, y), "The second test over its own skeleton (red)", fill=INK, font=font(32))
    y += 50
    units = T.TESTS[1][1]
    sc = 0.5
    for stl in (S.HAND,):
        oy = y + 380
        tracks = T.assemble(units, stl)
        ox, _ = place(img, d, tracks, stl, 40, W - 60, oy, sc, rules=False)
        skeleton(d, tracks, stl, ox, oy, sc)
        d.text((40, y + 10), stl.name, fill=GREY, font=font(22))
        y += 560

    img = img.crop((0, 0, W, int(y + 30)))
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)
    return out


def variants(st, n=11):
    """(label, parameters) pairs over a stroke's ranges: the default, then each parameter
    at its two ends, the others at their defaults."""
    base = {k: v[1] for k, v in st.params.items()}
    out = [("default", dict(base))]
    for k, (lo, mid, hi) in st.params.items():
        vals = (lo, hi) if len(st.params) > 2 else (lo, (lo + mid) / 2, (mid + hi) / 2, hi)
        for v in vals:
            if v == mid:
                continue
            p = dict(base)
            p[k] = v
            out.append((f"{k} {v:g}", p))
    return out[:n]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=ROOT / "specimens/veldikko/strokes.png")
    print(sheet(ap.parse_args().out))


if __name__ == "__main__":
    main()
