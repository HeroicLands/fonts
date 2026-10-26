# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Render the Pirzath Hand stroke sheet from the stroke generator.

    .venv/bin/python tools/pirzath-hand/strokes_sheet.py [--out specimens/pirzath-hand/strokes.png]

The sheet has five parts: every stroke large, with the guides; every stroke at 24
and 48 px to the em after Liberation Mono's "xhn"; rough skeletons built from the
strokes at display size, one drawn over its own track; the skeletons written with the
pen at four angles, for comparison; and runs of the worn forms at 96, 48 and 24 px beside
a mixed-case Latin sentence in Liberation Mono and the same words in Pirzath Carved,
all three at one font size. The hand's body stands at Latin's cap height, so the
three should read as one size of text. The skeletons test how the strokes sit
together. They are not letters of the script.
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
from encoded import Encoded  # noqa: E402
from render import Renderer, latin_font  # noqa: E402

PAPER = (247, 243, 235)
INK = (28, 24, 20)
GREY = (120, 112, 104)
GHOST = (200, 192, 178)
RULE = (212, 202, 184)
FAINT = (230, 222, 206)
RED = (176, 48, 36)
BLUE = (40, 90, 170)
SS = 3
LABEL_FONT = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
CARVED_FONT = ROOT / "fonts/PirzathCarved-Regular.ttf"


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
    """The line and the body and, in full, the vowel height, the ascender and the
    descender."""
    levels = [(0, RULE), (S.BODY, RULE)]
    if full:
        levels += [(S.VOWEL, FAINT), (S.ASC, FAINT), (S.DESC, FAINT)]
    for v, c in levels:
        y = oy - v * scale
        d.line([(x0, y), (x1, y)], fill=c, width=1)


def bounds_x(tracks, style=S.HAND):
    xs = [S.to_page(f, y, style)[0] for t in tracks for f, y, _ in t.samples]
    return min(xs) - S.HALF_W, max(xs) + S.HALF_W


def skeleton_line(d, tracks, ox, oy, scale, color=RED):
    for t in tracks:
        pts = [S.to_page(f, y) for f, y, _ in t.samples]
        d.line([(ox + x * scale, oy - y * scale) for x, y in pts], fill=color, width=1)


# -- context drawn in grey under a stroke in the large cells -----------------------------------

def context(sid):
    """The strokes a stroke is shown against: a mark on the letter it marks."""
    if sid == "notch":
        return S.shape("stem", 0, 0, top=0.85 * S.BODY).tracks
    return []


def origin(sid):
    """Where a stroke sits in its large cell."""
    return {"notch": (0.5 * S.FULL * 0.5, 0)}.get(sid, (0, 0))


# -- the skeletons ----------------------------------------------------------------------------
#
# A skeleton is (label, advance, parts): the parts are (stroke, f, y, params) from the
# skeleton's left edge. They test how strokes sit together; none is a letter.

SB = 70  # the white either side of a skeleton's ink: generous, so letters never touch in low light
WORD = 0.5  # the word space, in ems
B = S.BODY
W = 0.66 * B  # the standard frame width
V = S.VOWEL

SKELETONS = [
    ("tent", 2 * SB + W, [("tent", SB, 0, {})]),
    ("tent with a heel", 2 * SB + W + S.HEEL, [("tent", SB, 0, dict(heel=1))]),
    ("trough", 2 * SB + W, [("trough", SB, 0, {})]),
    ("stem closing a point", 2 * SB + 0.5 * B, [("stem", SB + S.HALF_W * 0.7, 0, {}),
                                                ("point", SB, 0, dict(w=0.5 * B))]),
    ("point with a heel", 2 * SB + S.HEEL + 30, [("point", SB, 0, dict(heel=1))]),
    ("round", 2 * SB + 0.62 * B, [("round", SB, 0, {})]),
    ("cross", 2 * SB + 0.6 * B, [("cross", SB, 0, {})]),
    ("stem to the ascender with a forward cut", 2 * SB + 0.5 * B,
     [("stem", SB + S.HALF_W * 0.7, 0, dict(top=S.ASC)),
      ("cut", SB, 0, dict(w=0.5 * B, h=0.6 * B, top=0.6 * B))]),
    ("stem into the descender with a heel", 2 * SB + 0.5 * B,
     [("stem", SB + 0.5 * B - S.HALF_W, 0, dict(foot=S.DESC, heel=1))]),
    ("trough with the doubling mark laid under it", 2 * SB + W,
     [("trough", SB, 0, {}), ("notch", SB + W / 2, 0, dict(angle=8.0, at=-105.0))]),
    ("vowel height: back cut, tent, round with the length bar", 2 * SB + 0.3 * B + 0.5 * B + 0.5 * B + 60,
     [("cut", SB, 0, dict(w=0.3 * B, h=V, top=V, fall=-1)),
      ("tent", SB + 0.3 * B + 30, 0, dict(w=0.5 * B, h=V)),
      ("round", SB + 0.8 * B + 60, 0, dict(w=0.5 * B, h=0.8 * V)),
      ("bar", SB + 0.8 * B + 60, 0, dict(at=S.LENGTH_Y))]),
    ("roof with a heel back, and forward", 2 * SB + 0.55 * B + 120 + 0.45 * B,
     [("roof", SB, 0, dict(heel=1)), ("roof", SB + 0.55 * B + 120, 0, dict(heel=1, side=1, w=0.45 * B))]),
]

# Worn forms: a carved frame as the hand first wrote it (grey) beside the settled form
# that thousands of years of daily writing leave, one or two quick movements. Tests of
# the strokes' economy; none is a letter.
WORN = [
    ("Λ worn to a fall with a half leg", [("tent", 0, 0, {})], [("tent", 0, 0, dict(left=0.5, peak=0.3))], W),
    ("ΛΛ worn to one zigzag", [("tent", 0, 0, dict(w=0.66 * W)), ("tent", 0.55 * W, 0, dict(w=0.66 * W))],
     [("zigzag", 0, 0, dict(turns=2, start=-1, w=0.7 * B))], 0.7 * B),
    ("V worn to a fall with an upturn", [("trough", 0, 0, {})], [("trough", 0, 0, dict(base=0.55, rise=0.55, w=0.55 * B))],
     0.5 * B),
    ("stem closing a point worn to a roof with a heel", [("stem", S.HALF_W * 0.7, 0, {}), ("point", 0, 0, dict(w=0.5 * B))],
     [("roof", 0, 0, dict(heel=1))], 0.55 * B),
    ("Λ with a pole worn to Λ with a heel", [("tent", 0, 0, {}), ("stem", 0.27 * W + 22, 0, dict(top=0.42 * B))],
     [("tent", 0, 0, dict(heel=1))], W + S.HEEL),
    ("◇ worn to the round", [("point", 0, 0, dict(w=0.3 * B, side=-1, at=0.5)), ("point", 0.3 * B - 2 * S.IN * S.HALF_W, 0,
                                                                              dict(w=0.3 * B, at=0.5))],
     [("round", 0, 0, dict(w=0.5 * B, h=0.62 * B))], 0.5 * B),
    ("X worn to a fall crossed high by a full back cut", [("cross", 0, 0, {})],
     [("cut", 0, 0, dict(w=0.42 * B)), ("cut", 0.05 * B, 0, dict(w=0.4 * B, h=0.6 * B, top=B, fall=-1))], 0.45 * B),
]

WORN_WORDS = [[0, 5, 2], [3, 1], [4, 6, 5], [2, 0], [1, 5, 3], [6, 4]]


def worn_word(indices):
    """Worn forms set side by side, each with its white; return tracks and width."""
    tracks, f = [], 0.0
    for i in indices:
        _, _, parts, wd = WORN[i]
        for sid, ff, yy, pr in parts:
            tracks += S.shape(sid, f + SB + ff, yy, **pr).tracks
        f += wd + 2 * SB
    return tracks, f


TICK = S.FULL  # a tally stroke's length: full-size, like every part
DIGIT = 0.85 * B  # a digit stands a little shorter than a letter, on the line


def numeral_tracks(v, f0=0.0):
    """A tally test: a stem a little shorter than a letter, with up to four full-size
    strokes at fixed places, each starting at the stem and running out at 60°: 8 from
    the head down forward, 4 from the middle down forward, 2 from the middle up back
    and 1 from the line up back. Each is as long as half the body and as heavy as the
    stem, and only its place counts."""
    c = f0 + 0.31 * B
    tracks = S.shape("stem", c, 0, top=DIGIT).tracks
    off = 0.25 * TICK  # each stroke starts at the stem and runs out to one side, at 60°
    for bit, side, at in ((8, 1, 0.745), (4, 1, 0.255), (2, -1, 0.745), (1, -1, 0.255)):
        if v & bit:
            tracks += S.shape("notch", c + side * off, 0, length=TICK, angle=120.0, at=at * DIGIT).tracks
    return tracks, 0.62 * B


OVER = 1  # the skeleton drawn over its own track


def tracks_of(sk, f0=0.0):
    _, _, parts = sk
    tracks = []
    for sid, f, y, params in parts:
        tracks += S.shape(sid, f0 + f, y, **params).tracks
    return tracks


def word(indices, f0=0.0, gap=0.0):
    tracks, f = [], f0
    for i in indices:
        sk = SKELETONS[i]
        tracks += tracks_of(sk, f)
        f += sk[1] + gap
    return tracks, f - f0


WORDS = [[0, 5, 2], [3, 6], [10], [1, 2, 7], [4, 5], [8, 0], [6, 5, 2]]


def carved_line(text, px):
    """Pirzath Carved, ``text`` written through the encoding, at ``px`` to the em: returned
    as an image with its baseline."""
    r = Renderer(CARVED_FONT)
    size = px
    cps = Encoded("pirzath-carved").one(text)
    w = int(r.width(cps, size)) + 20
    h = int(size * 1.4)
    img = Image.new("RGB", (w, h), PAPER)
    r.text(img, 10, int(size * 1.05), cps, size, color=INK)
    return img, int(size * 1.05)


def sheet(out: Path):
    WIDTH = 2400
    ids = list(S.STROKES)
    cell = 380
    cols = WIDTH // cell
    rows = -(-len(ids) // cols)
    H = 260 + rows * (cell + 80) + 400 + 3 * 640 + 900 + 700 + 900 + 1200 + 700
    img = Image.new("RGB", (WIDTH, H), PAPER)
    d = ImageDraw.Draw(img)
    pen = S.HAND.pen
    run = 0.45 * S.BODY - 2 * S.IN * S.HALF_W  # the default cut's track, across and down
    drop = S.BODY - 2 * S.HALF_H
    fall, back = S.heading(run, -drop), S.heading(-run, -drop)
    d.text((40, 30), "Pirzath Hand — layer 1: the strokes", fill=INK, font=font(46))
    d.text((40, 94), f"Written left to right with a blunt squared tool, chalk or a carpenter's pencil, {pen.width:g} by "
           f"{pen.thin:g} units, held at {pen.angle:g}°, upright. Across the stroke, a forward fall (\\) is "
           f"{round(S.extent(fall))} units, a stem {round(S.extent(S.heading(0, -1)))}, a back fall (/) "
           f"{round(S.extent(back))}, a level stroke {round(S.extent(0))} and a stroke at the tool's angle "
           f"{round(S.extent(pen.angle))}.", fill=GREY, font=font(22))
    d.text((40, 126), f"The body stands at Latin's cap height, {S.BODY:g} units; a vowel at {S.VOWEL:g}. Drawn from "
           "tools/pirzath-hand/strokes.py. Guides: the line and the body, and faint, the vowel height, the ascender and "
           "the descender. Grey: context.", fill=GREY, font=font(22))
    d.text((40, 158), "The skeletons test how the strokes sit together. They are not letters of the script.",
           fill=RED, font=font(22))

    # -- part 1: every stroke large
    y = 210
    sc = 0.3
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
        oy = cy + cell * 0.8
        guides(d, cx + 10, cx + cell - 10, oy, sc)
        if ctx:
            draw_path(img, S.outline(ctx), ox, oy, sc, color=GHOST)
        draw_path(img, S.outline(sh.tracks), ox, oy, sc)
        d.text((cx + 12, cy + cell + 6), sid, fill=INK, font=font(22))
        d.text((cx + 12, cy + cell + 34), f"{st.name} · {st.kind}", fill=GREY, font=font(18))
    y += rows * (cell + 80) + 20

    # -- part 2: every stroke at 24 and 48 px, after xhn
    d.text((40, y), "Every stroke at 24 and 48 px to the em, after Liberation Mono's “xhn” at the same size",
           fill=INK, font=font(32))
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
    d.text((40, y), "Rough skeletons built from the strokes — tests of how they sit together; not letters",
           fill=INK, font=font(32))
    y += 60
    sc = 0.42
    x = 60
    oy = y + 400
    for sk in SKELETONS:
        wpx = sk[1] * sc
        if x + wpx > WIDTH - 40:
            x = 60
            y += 540
            oy = y + 400
        guides(d, x - 6, x + wpx + 6, oy, sc)
        draw_path(img, S.outline(tracks_of(sk)), x, oy, sc)
        lab = sk[0]
        d.text((x, oy + 100), lab, fill=GREY, font=font(18))
        x += max(wpx, d.textlength(lab, font=font(18))) + 60
    y += 560
    d.text((40, y), "Worn forms: a carved frame as the hand first wrote it (grey), and the settled form thousands of "
           "years of daily writing leave — tests of economy; not letters", fill=INK, font=font(32))
    y += 60
    sc4 = 0.3
    x = 60
    oy = y + 300
    for label, old_parts, new_parts, wd in WORN:
        old_tr = [t for sid, f, yy, pr in old_parts for t in S.shape(sid, f, yy, **pr).tracks]
        new_tr = [t for sid, f, yy, pr in new_parts for t in S.shape(sid, f, yy, **pr).tracks]
        lo, hi = bounds_x(old_tr)
        cell_w = (hi - lo) * sc4 + 40 + wd * sc4 + 40
        if x + cell_w > WIDTH - 40:
            x = 60
            y += 420
            oy = y + 300
        guides(d, x - 6, x + cell_w - 20, oy, sc4, full=False)
        draw_path(img, S.outline(old_tr), x - lo * sc4, oy, sc4, color=GHOST)
        x2 = x + (hi - lo) * sc4 + 40
        draw_path(img, S.outline(new_tr), x2, oy, sc4)
        d.text((x, oy + 40), label, fill=GREY, font=font(18))
        x += max(cell_w, d.textlength(label, font=font(18)) + 20) + 50
    y = oy + 110

    # numerals: the tally test, 0 to 15
    d.text((40, y), "The tally test: a short stem with up to four full-size strokes, 0 to 15, places only — "
           "a test of the strokes; not the numerals", fill=INK, font=font(32))
    y += 50
    for px, gap in ((300, 10), (48, 6), (24, 4)):
        scale = px / 1000
        oy = y + S.BODY * scale + 10
        x = 60
        guides(d, 50, WIDTH - 50, oy, scale, full=False)
        for v in range(16):
            tr, wd = numeral_tracks(v)
            draw_path(img, S.outline(tr), x, oy, scale)
            if px > 100:
                d.text((x + 0.25 * B * scale, oy + 16), str(v), fill=GREY, font=font(18))
            x += wd * scale + gap
        y = oy + (60 if px > 100 else 30)
    y += 20
    tr = tracks_of(SKELETONS[OVER])
    sc2 = 0.7
    d.text((40, y), f"“{SKELETONS[OVER][0]}” over its own track (red)", fill=INK, font=font(26))
    oy = y + 60 + S.ASC * sc2
    guides(d, 50, 80 + SKELETONS[OVER][1] * sc2, oy, sc2)
    draw_path(img, S.outline(tr), 60, oy, sc2)
    skeleton_line(d, tr, 60, oy, sc2)
    y = oy + 80

    # -- part 4: the tool at four angles
    d.text((40, y), "The same skeletons written with the tool at four angles; the sheet's tool is at "
           f"{pen.angle:g}°", fill=INK, font=font(32))
    y += 50
    sc3 = 0.18
    oy = y + 230
    x = 60
    for ang in (30.0, 40.0, 50.0, 60.0):
        style = S.Style(f"{ang:g}", S.Pen(pen.width, pen.thin, ang, pen.flex, pen.square), S.HAND.slant)
        tr, wd = word([0, 1, 2, 3], gap=0)
        draw_path(img, S.outline(tr, style), x, oy, sc3)
        d.text((x, oy + 70), f"{ang:g}°", fill=GREY, font=font(20))
        x += wd * sc3 + 60
    y = oy + 120

    # -- part 5: beside a mixed-case Latin sentence and Pirzath Carved, at one font size
    d.text((40, y), "Worn forms run on beside Liberation Mono in a mixed-case sentence and beside Pirzath Carved, all "
           "three at one font size; faint rules: Latin's x-height and cap height", fill=INK, font=font(32))
    y += 70
    latin = "Gaz Guruz, Tanv-guráz."
    for px in (96, 48, 24):
        scale = px / 1000
        for row in ("latin", "carved"):
            oy = int(y + px * 1.0)
            for v in (S.LATIN_X, S.BODY):
                d.line([(40, oy - v * scale), (WIDTH - 40, oy - v * scale)], fill=FAINT)
            d.line([(40, oy), (WIDTH - 40, oy)], fill=FAINT)
            x = 60
            if row == "latin":
                d.text((x, oy), latin, fill=BLUE, font=latin_font(px), anchor="ls")
                x += d.textlength(latin, font=latin_font(px)) + px * 0.6
            else:
                cimg, base = carved_line(latin.lower(), px)
                img.paste(cimg, (int(x - 10), oy - base))
                x += cimg.width + px * 0.6
            k = 0 if row == "latin" else 3
            while True:
                tr, wd = worn_word(WORN_WORDS[k % len(WORN_WORDS)])
                if x + wd * scale > WIDTH - 60:
                    break
                draw_path(img, S.outline(tr), x, oy, scale)
                x += wd * scale + px * WORD
                k += 1
            y += px * 1.5
        d.text((40, y - 4), f"{px} px", fill=GREY, font=font(18))
        y += 40

    img = img.crop((0, 0, WIDTH, int(y + 30)))
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=ROOT / "specimens/pirzath-hand/strokes.png")
    print(sheet(ap.parse_args().out))


if __name__ == "__main__":
    main()
