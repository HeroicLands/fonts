# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Render the Vedyakshara stroke sheet from the stroke generator.

    .venv/bin/python tools/vedyakshara/specimens.py [--out specimens/vedyakshara/strokes.png]

The sheet has four parts: every stroke large, with the guides; every stroke at
24 and 48 px to the em; rough sign skeletons hanging from a headline at display size,
one drawn over its own skeleton; and the skeletons run on as words at 48 and
24 px beside a line of Liberation Mono at the same size, to check the x-height.
The skeletons test how the strokes sit together. They are not signs of the script.
"""

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "tools"))
import strokes as S  # noqa: E402
from render import latin_font  # noqa: E402

PAPER = (243, 239, 228)
INK = (28, 34, 40)
GREY = (118, 112, 100)
GHOST = (196, 188, 172)
RULE = (212, 202, 180)
FAINT = (228, 220, 202)
RED = (176, 48, 36)
BLUE = (40, 90, 170)
SS = 3
LABEL_FONT = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"


def font(size, path=LABEL_FONT):
    try:
        return ImageFont.truetype(str(path), size)
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
    """The line and the x-height and, in full, the top of the headline, the flag head
    and the hook foot."""
    levels = [(0, RULE), (S.X, RULE)]
    if full:
        levels += [(S.HEAD, FAINT), (S.FLAG, FAINT), (S.HOOK, FAINT)]
    for v, c in levels:
        y = oy - v * scale
        d.line([(x0, y), (x1, y)], fill=c, width=1)


def bounds_x(tracks):
    xs = [S.to_page(f, y)[0] for t in tracks for f, y, _ in t.samples]
    return min(xs), max(xs)


def skeleton(d, tracks, ox, oy, scale, color=RED):
    for t in tracks:
        pts = [S.to_page(f, y) for f, y, _ in t.samples]
        d.line([(ox + x * scale, oy - y * scale) for x, y in pts], fill=color, width=1)


# -- context drawn in grey under a stroke in the large cells -----------------------------------

def context(sid):
    """The strokes a stroke is shown against: a body under a rope, a mark on a stem."""
    st = S.STROKES[sid]
    if sid in ("lobe", "rung", "breath"):
        return S.shape("stem", 0, 0).tracks + S.shape("headline", -320, 0, w=380).tracks
    if sid == "rstem":
        return S.shape("headline", -320, 0, w=380).tracks
    if st.kind == "body":
        return S.shape("headline", -90, 0, w=560).tracks
    if sid == "flag":
        return S.shape("headline", -200, 0, w=400).tracks
    if sid in ("hook", "rfoot"):
        return S.shape("stem", 0, 0).tracks + S.shape("headline", -160, 0, w=200).tracks
    if sid == "dot":
        return S.shape("bowl", -188, 0, w=375).tracks + S.shape("headline", -188, 0, w=375).tracks
    return []


def origin(sid):
    """Where a stroke sits in its large cell, when its context needs it elsewhere."""
    return {"dot": (0, 0.42 * S.X)}.get(sid, (0, 0))


# -- the skeletons ----------------------------------------------------------------------------
#
# A skeleton is (name, advance, parts, rope): the parts are (stroke, f, y, params)
# from the sign's left edge, and ``rope`` is "full" for a headline over the whole
# advance, or a (stroke, params) pair for a sign that ends its own rope.

SB = 44  # the body's sidebearing; the headline reaches across it

SKELETONS = [
    ("bowl and stem", 500, [("bowl", SB, 0, dict(w=350)), ("stem", SB + 390, 0, {})], "full"),
    ("arc, stem and the i-flag", 450, [("arc", SB, 0, dict(w=275, turn=0.7)), ("stem", SB + 338, 0, {}),
                                       ("flag", SB + 300, 0, {})], "full"),
    ("short bowl, stem and the u-hook", 450, [("bowl", SB, 0, dict(w=275, h=0.55)), ("arc", SB + 12, 0,
                                              dict(w=250, h=0.5, side=-1, turn=0.0)), ("stem", SB + 332, 0, {}),
                                              ("hook", SB + 332, 0, {})], "full"),
    ("half form into a sign with the r-foot", 650, [("arc", SB, 0, dict(w=212, turn=0.0)), ("cut", SB + 250, 0, {}),
                                                     ("bowl", SB + 312, 0, dict(w=225, h=0.7)),
                                                     ("stem", SB + 540, 0, {}), ("rfoot", SB + 312, 0, {})], "full"),
    ("bowl and stem, the final form", 500, [("bowl", SB, 0, dict(w=350)), ("stem", SB + 390, 0, {})],
     ("tick", dict(w=390 + SB))),
    ("bowl with the soft dot, the o-hook and the e-flag", 500,
     [("bowl", SB, 0, dict(w=350, close=0.8)), ("dot", SB + 175, 0.42 * S.X, {}), ("stem", SB + 390, 0, {}),
      ("hook", SB + 175, 0, dict(side=-1)), ("flag", SB + 175, 0, {})], "full"),
    ("open arc and kicked stem", 375, [("arc", SB, 0, dict(w=212, side=-1, turn=0.5)),
                                       ("stem", SB + 250, 0, dict(foot=1.0))], "full"),
]


def sign_tracks(sk, f0=0.0):
    _, adv, parts, rope = sk
    tracks = []
    if rope == "full":
        tracks += S.shape("headline", f0, 0, w=adv).tracks
    else:
        sid, params = rope
        tracks += S.shape(sid, f0, 0, **params).tracks
    for sid, f, y, params in parts:
        tracks += S.shape(sid, f0 + f, y, **params).tracks
    return tracks


def word(signs, f0=0.0):
    """Signs set side by side, their headlines meeting in one rope; return tracks and width."""
    tracks, f = [], f0
    for sk in signs:
        tracks += sign_tracks(sk, f)
        f += sk[1]
    return tracks, f - f0


WORDS = [[0, 1], [3, 5, 2], [6, 0, 4], [1, 2, 5, 3], [5, 4]]


def sheet(out: Path):
    W = 2400
    ids = list(S.STROKES)
    cell = 380
    cols = W // cell
    rows = -(-len(ids) // cols)
    H = 260 + rows * (cell + 80) + 360 + 2 * 820 + 220 + 1400
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.text((40, 30), "Vedyakshara — layer 1: the reed strokes", fill=INK, font=font(46))
    d.text((40, 94), f"Written left to right with a broad reed cut square, its edge held steep at {S.HAND.nib.angle:g}°, "
           f"upright. The headline, a level pull, is the heaviest stroke ({S.HEAD_W} units); a stem is "
           f"{round(S._extent(S.HAND.nib, 90))}.", fill=GREY, font=font(22))
    d.text((40, 126), "Drawn from tools/vedyakshara/strokes.py. Guides in the stroke cells: the line, the x-height "
           "(the headline's underside), and faint, the headline's top, the flag head and the hook foot. Grey: context.",
           fill=GREY, font=font(22))
    d.text((40, 158), "The skeletons test how the strokes sit together. They are not signs of the script.",
           fill=RED, font=font(22))

    # -- part 1: every stroke large
    y = 210
    sc = 0.30
    for i, sid in enumerate(ids):
        st = S.STROKES[sid]
        cx = 20 + (i % cols) * cell
        cy = y + (i // cols) * (cell + 80)
        d.rectangle([cx + 8, cy, cx + cell - 8, cy + cell], outline=RULE)
        of, oyy = origin(sid)
        sh = S.shape(sid, of, oyy)
        ctx = context(sid)
        lo, hi = bounds_x(sh.tracks + ctx)
        ox = cx + cell / 2 - (lo + hi) / 2 * sc
        oy = cy + cell * 0.68
        guides(d, cx + 10, cx + cell - 10, oy, sc)
        if ctx:
            draw_path(img, S.outline(ctx), ox, oy, sc, color=GHOST)
        draw_path(img, S.outline(sh.tracks), ox, oy, sc)
        d.text((cx + 12, cy + cell + 6), sid, fill=INK, font=font(22))
        d.text((cx + 12, cy + cell + 34), f"{st.name} · {st.kind}", fill=GREY, font=font(18))
    y += rows * (cell + 80) + 20

    # -- part 2: every stroke at 24 px, with its context in ink, as it will meet the eye
    d.text((40, y), "Every stroke at 24 and 48 px to the em, after Liberation Mono at the same size", fill=INK, font=font(32))
    y += 60
    for px in (24, 48):
        scale = px / 1000
        oy = y + px * 1.1
        x = 60
        d.text((x, oy), "xhn", fill=BLUE, font=latin_font(px), anchor="ls")
        x += px * 2.4
        for sid in ids:
            of, oyy = origin(sid)
            tr = S.shape(sid, of, oyy).tracks
            ctx = context(sid)
            lo, hi = bounds_x(tr + ctx)
            draw_path(img, S.outline(ctx + tr), x - lo * scale, oy, scale)
            x += (hi - lo) * scale + px * 0.9
        y += px * 2.2 + 20
    y += 30

    # -- part 3: the skeletons at display size
    d.text((40, y), "Rough sign skeletons hanging from the headline — strokes set together; not signs of the script",
           fill=INK, font=font(32))
    y += 60
    sc = 0.36
    per_row = 4
    for r in range(0, len(SKELETONS), per_row):
        row = SKELETONS[r:r + per_row]
        oy = y + 380
        x = 60
        for sk in row:
            tr = sign_tracks(sk)
            guides(d, x - 10, x + sk[1] * sc + 10, oy, sc)
            draw_path(img, S.outline(tr), x, oy, sc)
            d.text((x, y + 520), sk[0], fill=GREY, font=font(18))
            x += 560
        y += 580
    # one skeleton over its own track
    sk = SKELETONS[3]
    tr = sign_tracks(sk)
    sc2 = 0.7
    oy = y + 560
    d.text((40, y), f"“{sk[0]}” over its own skeleton (red)", fill=INK, font=font(26))
    guides(d, 50, 60 + sk[1] * sc2 + 20, oy, sc2)
    draw_path(img, S.outline(tr), 60, oy, sc2)
    skeleton(d, tr, 60, oy, sc2)
    y += 760

    # -- part 4: words at text size beside Latin
    d.text((40, y), "The skeletons run on as words at 48 and 24 px, after a line of Liberation Mono at the same size; "
           "faint rule: the shared x-height", fill=INK, font=font(32))
    y += 70
    latin = "the rope with the words strung beneath it"
    for px in (48, 24, 20):
        scale = px / 1000
        for line in range(2 if px < 40 else 1):
            oy = y + px * 1.2
            d.line([(40, oy - S.X * scale), (W - 40, oy - S.X * scale)], fill=FAINT)
            d.text((60, oy), latin if line == 0 else "xhn", fill=BLUE, font=latin_font(px), anchor="ls")
            x = 60 + d.textlength(latin if line == 0 else "xhn", font=latin_font(px)) + px * 0.6
            k = line
            while True:
                tr, wd = word([SKELETONS[i] for i in WORDS[k % len(WORDS)]])
                if x + wd * scale > W - 60:
                    break
                draw_path(img, S.outline(tr), x, oy, scale)
                x += wd * scale + px * 0.35
                k += 1
            y += px * 1.8
        d.text((40, y), f"{px} px", fill=GREY, font=font(18))
        y += 40

    img = img.crop((0, 0, W, int(y + 30)))
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=ROOT / "specimens/vedyakshara/strokes.png")
    print(sheet(ap.parse_args().out))


if __name__ == "__main__":
    main()
