# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""The Ch'alish P'ilam ceremonial hand: its canon, its kit, and its glyphs.

    import ceremonial as R

    parts = R.SUN.draw()                      # [(pen, [Track | Fill, ...]), ...]
    ink = R.ink(parts)                        # a pathops.Path, font units, y up

The ceremonial hand is painted with a brush on fig-bark codices and plaster, and cut in
stone. Every glyph is its own picture, drawn whole inside a **cushion**: a rounded oblong
that always stands round the sign. There is no skeleton but the cushion. What gives the
hand its look is a small, fixed way of drawing, the **canon**, and a kit of recurring
parts that the glyphs share:

- **Two brushes.** The contour brush draws the cushion and a glyph's main outlines at
  about 4% of the block; the detail brush draws everything inside at about 2.5%.
- **Heads face the line's start**, in profile: a large eye under a brow, the nose on the
  outline, an open mouth with a tooth, and a spiral ear spool behind.
- **Fields and fillings**: cross-hatched netting, rows of small dots tracing an outline,
  curls, and the X.
- **Affixes** round a main sign: the comb fringe under it, a narrow oblong before it,
  and small ringed beads beside it.

A glyph's parts are lists of tracks and fills, each paired with the brush that draws it.
Coordinates are font units on a 1000-unit em; a block stands ``BLOCK`` high on the line.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable

import pathops

import strokes as S

B = S.BLOCK
C = B / 2

# The two brushes: fine at entry and exit, swelling through the stroke.
CONTOUR = S.Pen("contour", full=32.0, light=16.0, taper=60.0)
DETAIL = S.Pen("detail", full=20.0, light=9.0, taper=40.0)

# The cushion of a whole block: a little wider than tall, its corners round.
CX0, CY0, CX1, CY1 = 20.0, 60.0, B - 20.0, B - 30.0
CW, CH = CX1 - CX0, CY1 - CY0

# The brush wanders: every track is nudged by a smooth, seeded wobble of this many units,
# so no two strokes are mechanically alike.
WOBBLE = 7.0


def wobble(parts, seed):
    """Nudge every point of every track by a smooth wobble, seeded so a glyph is drawn the
    same every time."""
    import random
    rng = random.Random(seed)
    phases = [rng.uniform(0, 2 * math.pi) for _ in range(4)]
    out = []
    for p in parts:
        def nudge(x, y):
            dx = WOBBLE * (math.sin(x / 61 + phases[0]) + math.sin(y / 47 + phases[1])) / 2
            dy = WOBBLE * (math.sin(y / 53 + phases[2]) + math.sin(x / 71 + phases[3])) / 2
            return x + dx, y + dy
        pts = [nudge(x, y) for x, y in p.pts]
        out.append(S.Fill(pts) if isinstance(p, S.Fill) else S.Track(pts, closed=p.closed, weight=p.weight))
    return out


def fit(parts, x0, y0, x1, y1):
    """Parts drawn in a whole block, moved and scaled into the box (x0, y0)–(x1, y1). The
    brushes keep their widths; a dot keeps its size down to two thirds."""
    sx, sy = (x1 - x0) / B, (y1 - y0) / B
    out = []
    for p in parts:
        if isinstance(p, S.Fill):
            cx = sum(q[0] for q in p.pts) / len(p.pts)
            cy = sum(q[1] for q in p.pts) / len(p.pts)
            k = max(min(sx, sy), 0.66)
            out.append(S.Fill([(x0 + cx * sx + (qx - cx) * k, y0 + cy * sy + (qy - cy) * k) for qx, qy in p.pts]))
        else:
            out.append(S.Track([(x0 + qx * sx, y0 + qy * sy) for qx, qy in p.pts], closed=p.closed, weight=p.weight))
    return out


# The narrowest white a chisel can cut: as wide as a detail line, with a little to spare.
GAP = DETAIL.full * 1.1


# -- the kit -------------------------------------------------------------------------------------


def cushion(x0=CX0, y0=CY0, x1=CX1, y1=CY1, square=3.0):
    return S.frame(x0, y0, x1 - x0, y1 - y0, square=square)


def fringe(x0, x1, y, n=None, h=44.0):
    """The comb fringe: a row of scallops hanging from a line, each touching the next, so
    every opening is wide enough to cut."""
    n = n or max(3, round((x1 - x0) / 70))
    w = (x1 - x0) / n
    out = S.bar(x0, y, x1, y)
    for i in range(n):
        out += S.arc(x0 + (i + 0.5) * w, y, w * 0.5, h, 180, 360)
    return out


def dotted(points, r=11.0, step=None):
    """A row of dots tracing a path, a dot's width or more apart."""
    step = step or 2 * r + GAP
    out = []
    for (ax, ay), (bx, by) in zip(points, points[1:]):
        n = max(1, int(math.dist((ax, ay), (bx, by)) / step))
        for k in range(n):
            u = k / n
            out += S.dot(ax + (bx - ax) * u, ay + (by - ay) * u, r)
    out += S.dot(*points[-1], r)
    return out


def dotted_arc(cx, cy, rx, ry, a0, a1, r=11.0, step=None):
    step = step or 2 * r + GAP
    n = max(2, int(abs(math.radians(a1 - a0)) * max(rx, ry) / step))
    pts = [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * k / n)),
            cy + ry * math.sin(math.radians(a0 + (a1 - a0) * k / n))) for k in range(n + 1)]
    if abs(a1 - a0) >= 360:
        pts = pts[:-1]
    return [f for p in pts for f in S.dot(*p, r)]


def net(x, y, w, h, n=None):
    """A cross-hatched field: netting, darkness, a woven thing. Its strands stand a line
    and a groove apart."""
    span = (w + h) / math.sqrt(2)
    n = n or max(2, int(span / (DETAIL.full + GAP) / 1.6))
    return S.hatch(x, y, w, h, n=n, angle=45, cross=True, weight=1.0)


def bead(cx, cy, r=34.0):
    """A small ringed bead, set beside a sign."""
    return S.ring(cx, cy, r) + S.dot(cx, cy, r * 0.32)


def ear_spool(cx, cy, r=70.0):
    # a small spool has no room to cut round a centre stone, and is a plain ring
    if r - DETAIL.full - 2 * GAP < 12:
        return S.ring(cx, cy, r)
    return S.ring(cx, cy, r) + S.dot(cx, cy, max(r * 0.2, 12))


def curl(cx, cy, r, turns=1.25, clockwise=False, weight=1.0):
    """A spiral whose turns stay a line and a groove apart, however many are asked for."""
    most = r * 0.82 / (DETAIL.full + GAP)
    return S.curl(cx, cy, r, turns=min(turns, max(0.6, most)), clockwise=clockwise, weight=weight)


def x_mark(cx, cy, r=45.0):
    return S.bar(cx - r, cy - r, cx + r, cy + r) + S.bar(cx - r, cy + r, cx + r, cy - r)


def eye(cx, cy, kind="open"):
    """The eye of a head facing the line's start: open (a ring with its pupil forward),
    closed (a lid's curve with lashes), or the spiral eye of a god."""
    if kind == "closed":
        out = S.arc(cx, cy + 30, 62, 50, 200, 340)
        for a in (215, 245, 275, 305):
            t = math.radians(a)
            out += S.tick(cx + 62 * math.cos(t), cy + 30 + 50 * math.sin(t), 22, angle=a)
        return out
    if kind == "spiral":
        return curl(cx, cy, 62, turns=1.4)
    return S.ring(cx, cy, 58) + S.dot(cx - 20, cy, 20)


def profile(x0=CX0, y0=CY0, x1=CX1, y1=CY1):
    """The outline of a head facing the line's start, filling the box: the back of the head
    is the cushion's round, and the forward edge is the profile, the brow, the nose standing
    out, the lips and the chin."""
    w, h = x1 - x0, y1 - y0
    X = lambda u: x0 + u * w  # noqa: E731
    Y = lambda v: y0 + v * h  # noqa: E731
    pts = []
    pts += S._arc(X(0.62), Y(0.5), w * 0.38, h * 0.5, 270, 450)  # the back of the head, round
    pts += S._bezier((X(0.62), Y(1.0)), (X(0.35), Y(1.02)), (X(0.12), Y(0.98)), (X(0.1), Y(0.78)))[1:]  # crown to brow
    pts += S._bezier((X(0.1), Y(0.78)), (X(0.02), Y(0.7)), (X(-0.04), Y(0.6)), (X(0.0), Y(0.55)))[1:]  # the nose
    pts += S._bezier((X(0.0), Y(0.55)), (X(0.05), Y(0.5)), (X(0.07), Y(0.45)), (X(0.04), Y(0.4)))[1:]  # upper lip
    pts += S._bezier((X(0.04), Y(0.4)), (X(0.02), Y(0.33)), (X(0.06), Y(0.27)), (X(0.05), Y(0.2)))[1:]  # lower lip
    pts += S._bezier((X(0.05), Y(0.2)), (X(0.06), Y(0.05)), (X(0.3), Y(-0.01)), (X(0.62), Y(0.0)))[1:]  # the chin
    return [S.Track(pts, closed=True)]


def prefix(x0, y0, x1, y1, kind="bars"):
    """A narrow affix standing before a main sign: a tall cushion holding bars or beads."""
    out = cushion(x0, y0, x1, y1, square=2.4)
    cx, h = (x0 + x1) / 2, y1 - y0
    if kind == "bars":
        for k in range(3):
            y = y0 + h * (0.3 + 0.2 * k)
            out += S.bar(x0 + (x1 - x0) * 0.22, y, x1 - (x1 - x0) * 0.22, y)
    else:
        for k in range(3):
            out += S.dot(cx, y0 + h * (0.25 + 0.25 * k), (x1 - x0) * 0.16)
    return out


def superfix(x0, y0, x1, y1, kind="dots"):
    """A flattened affix lying over a main sign."""
    out = cushion(x0, y0, x1, y1, square=2.6)
    cy, w = (y0 + y1) / 2, x1 - x0
    if kind == "dots":
        for k in range(4):
            out += S.dot(x0 + w * (0.2 + 0.2 * k), cy, (y1 - y0) * 0.14)
    elif kind == "fringe":
        out += fringe(x0 + w * 0.12, x1 - w * 0.12, cy + (y1 - y0) * 0.12, h=(y1 - y0) * 0.45)
    elif kind == "net":
        out += net(x0 + w * 0.1, y0 + (y1 - y0) * 0.2, w * 0.8, (y1 - y0) * 0.6, n=4)
    return out


def head(x0=CX0, y0=CY0, x1=CX1, y1=CY1, eye_kind="open", tooth=False, spool=True, band=True):
    """A whole head in its box: the profile outline and its features, drawn large. A living
    face has an almond eye under its brow, two lips and a headband across the crown."""
    w, h = x1 - x0, y1 - y0
    m = min(w, h)  # features are sized by the head's shorter side, so a long head keeps its proportions
    X = lambda u: x0 + u * w  # noqa: E731
    Y = lambda v: y0 + v * h  # noqa: E731
    contour = profile(x0, y0, x1, y1)
    detail = []
    ey = Y(0.56)  # the eye's centre; the brow and lids are placed from it by the head's shorter side
    detail += S.arc(X(0.29), min(ey + m * 0.14, Y(0.68)), m * 0.17, m * 0.1, 25, 160)  # the brow, a groove clear of the eye
    if eye_kind == "open":
        detail += S.arc(X(0.29), ey - m * 0.06, m * 0.12, m * 0.12, 25, 155) + S.arc(X(0.29), ey + m * 0.06, m * 0.12, m * 0.12, 205, 335)
        detail += S.dot(X(0.29) - m * 0.04, ey - m * 0.04, m * 0.032)  # the pupil hangs from the upper lid
    elif eye_kind == "closed":
        detail += S.arc(X(0.29), ey + m * 0.04, m * 0.1, m * 0.07, 200, 340)
    else:
        detail += curl(X(0.29), ey - m * 0.02, m * 0.1, turns=1.4)
    detail += S.arc(X(0.11), Y(0.44), m * 0.06, h * 0.04, 120, 330)  # the upper lip
    detail += S.arc(X(0.12), Y(0.27), m * 0.06, h * 0.045, 30, 240)  # the lower lip
    if tooth:
        detail += S.poly([(X(0.08), Y(0.37)), (X(0.12), Y(0.27)), (X(0.16), Y(0.37))])
    detail += curl(X(0.29) + m * 0.11, Y(0.34), m * 0.08, turns=1.3, clockwise=True)  # the cheek
    if spool:
        detail += ear_spool(X(0.68), Y(0.46), m * 0.12)
    if band:
        detail += S.arc(X(0.62), Y(0.5), w * 0.33, h * 0.42, 60, 128)
        detail += dotted_arc(X(0.62), Y(0.5), w * 0.33 - 46, h * 0.42 - 46, 66, 122)
    return contour, detail


# -- glyphs --------------------------------------------------------------------------------------


@dataclass(frozen=True)
class Glyph:
    name: str
    meaning: str
    sound: str  # a sound the glyph may write; several ceremonial glyphs write the same sound
    draw: Callable[[], list]  # [(pen, parts), ...], drawn in a box WIDTH[footprint] wide and BLOCK high
    footprint: str = "full"  # half, full or double: how much of the block grid the glyph fills


# A block is drawn BLOCK high and set in the font this many times larger, so that it spans
# the line from Latin's descender to its ascender: a dense picture wants more height than
# a letter's cap height gives it.
FONT_SCALE = 1.5
# Where the block's foot sits in the font, so it reaches into the descent.
FONT_DROP = -180.0

# The width each footprint draws in; the height is always the block's.
WIDTH = {"half": B / 2, "full": B, "double": 2 * B}


# -- conforming affixes: shaped by the sign they attach to ------------------------------------------


def edge(box, side, lo=0.12, hi=0.88, square=3.0):
    """Points along one side of a cushion, in order: ``left`` and ``right`` bottom to top,
    ``top`` and ``bottom`` from the line's start to its end; ``lo`` and ``hi`` trim the run
    to the middle of the side, as shares of its length."""
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    pts = cushion(x0, y0, x1, y1, square)[0].pts
    if side in ("left", "right"):
        keep = [p for p in pts if (p[0] < cx if side == "left" else p[0] > cx)]
        keep.sort(key=lambda p: p[1])
        a, b = y0 + (y1 - y0) * lo, y0 + (y1 - y0) * hi
        return [p for p in keep if a <= p[1] <= b]
    keep = [p for p in pts if (p[1] > cy if side == "top" else p[1] < cy)]
    keep.sort(key=lambda p: p[0])
    a, b = x0 + (x1 - x0) * lo, x0 + (x1 - x0) * hi
    return [p for p in keep if a <= p[0] <= b]


def _swell(t):
    return math.sin(math.pi * t) ** 0.6


def prefix_on(box, width, n=3, kind="bars", square=3.0):
    """A prefix grown from the main sign's leading edge: the main sign's own outline is its
    inner side, and only its outer curve is drawn, swelling out and closing back onto the
    main sign at both ends. Bars cross it, or beads stand down it."""
    inner = edge(box, "left", square=square)
    outer = [(x - width * _swell(k / (len(inner) - 1)), y) for k, (x, y) in enumerate(inner)]
    out = [S.Track(outer)]
    for k in range(n):
        t = (k + 1) / (n + 1)
        i = round(t * (len(inner) - 1))
        (xi, y), (xo, _) = inner[i], outer[i]
        if kind == "bars":
            out += S.bar(xo, y, xi, y)
        else:
            out += S.dot((xi + xo) / 2, y, max(12.0, (xi - xo) * 0.2))
    return out


def superfix_on(box, height, kind="dots", square=3.0):
    """A superfix lying along the main sign's top, its lower side the main sign's own
    outline, its upper curve swelling over it."""
    inner = edge(box, "top", lo=0.1, hi=0.9, square=square)
    outer = [(x, y + height * _swell(k / (len(inner) - 1))) for k, (x, y) in enumerate(inner)]
    out = [S.Track(outer)]
    marks = 4
    for k in range(marks):
        t = (k + 0.5) / marks
        i = round(t * (len(inner) - 1))
        (x, yi), (_, yo) = inner[i], outer[i]
        if kind == "dots":
            out += S.dot(x, (yi + yo) / 2, 13)
        elif kind == "x":
            out += x_mark(x, (yi + yo) / 2, min(28.0, (yo - yi) * 0.28))
        elif kind == "bars":
            out += S.bar(x, yi, x, yo)
    return out


def fringe_on(box, h=44.0, square=3.0):
    """The comb fringe hung from the main sign's own lower edge, its scallops touching."""
    run = edge(box, "bottom", lo=0.14, hi=0.86, square=square)
    xa, xb = run[0][0], run[-1][0]
    n = max(3, round((xb - xa) / 70))
    w = (xb - xa) / n
    out = []
    for k in range(n):
        cx = xa + (k + 0.5) * w
        y = min(run, key=lambda p: abs(p[0] - cx))[1]
        out += S.arc(cx, y, w * 0.5, h, 180, 360)
    return out


def roofed(x0, y0, x1, y1, ridge, eave=0.74):
    """A cushion whose top rises to a ridge: the house's roof become the block's crown. The
    cushion is kept below ``eave`` (a share of its height), and the roof springs from there."""
    w, h = x1 - x0, y1 - y0
    cx, cy = (x0 + x1) / 2, y0 + h / 2
    cut = y0 + h * eave
    run = [p for p in cushion(x0, y0, x1, y1, square=3.2)[0].pts if p[1] <= cut]
    run.sort(key=lambda p: (math.atan2(p[1] - cy, p[0] - cx) - math.pi / 2) % (2 * math.pi))
    le, re = run[0], run[-1]
    roof_r = S._bezier(re, (re[0], re[1] + 40), (cx + w * 0.15, ridge - 30), (cx, ridge))
    roof_l = S._bezier((cx, ridge), (cx - w * 0.15, ridge - 30), (le[0], le[1] + 40), le)
    return [S.Track(run + roof_r[1:] + roof_l[1:], closed=True)], (le, re)


# -- the pilot glyphs ----------------------------------------------------------------------------


def _lord():
    # a lord's head in profile under his headdress: a band of beads along the crown, plumes
    # rising from it; netted hair, a jewelled ear spool with its pendant, a bead at the nose
    box = (60, CY0 + 20, CX1, CY1 - 120)
    contour, detail = head(*box, band=False)
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    X = lambda u: x0 + u * w  # noqa: E731
    Y = lambda v: y0 + v * h  # noqa: E731
    crown = [(X(0.62) + w * 0.38 * math.cos(math.radians(a)), Y(0.5) + h * 0.5 * math.sin(math.radians(a)))
             for a in range(40, 131, 3)]
    band = [S.Track([(x, y + 70 * _swell(k / (len(crown) - 1))) for k, (x, y) in enumerate(crown)])]
    beads = []
    for k in range(5):
        x, y = crown[round((k + 0.5) / 5 * (len(crown) - 1))]
        beads += S.dot(x, y + 36 * _swell((k + 0.5) / 5), 12)
    plumes = []
    for k, t in enumerate((0.15, 0.4, 0.65, 0.9)):
        x, y = crown[round(t * (len(crown) - 1))]
        plumes += curl(x - 10, y + 105, 44, turns=1.0, clockwise=bool(k % 2))
    hair = []
    for k in range(1):
        hair += S.arc(X(0.62), Y(0.5), w * 0.38 - 60, h * 0.5 - 60, 8, 38)
    pendant = S.bar(X(0.68), Y(0.46) - w * 0.12, X(0.68), Y(0.16)) + bead(X(0.68), Y(0.1), 24)
    return [(CONTOUR, contour + band), (DETAIL, detail + beads + plumes + hair + pendant + bead(X(0.0) - 6, Y(0.5), 20))]


def _patriarch():
    # the patriarch, MAN, HIGH and HOUSE made one: the house's roof is the block's crown, the
    # elder fills the house under it, the HIGH point a bead at the ridge, one line of thatch
    x0, y0, x1, y1 = CX0, CY0, CX1, CY1 - 20
    outline, (le, re) = roofed(x0, y0, x1, y1, ridge=y1 + 40)
    thatch = S.bar(le[0] + 95, le[1] + 22, C, y1 + 40 - 95) + S.bar(re[0] - 95, re[1] + 22, C, y1 + 40 - 95)
    eaves = S.bar(le[0] + 10, le[1], re[0] - 10, re[1])
    # the elder's chin rests on the house's floor: the two share one outline there
    contour, detail = head(135, y0, x1 - 85, le[1] - 22, band=False, spool=True)
    crest = S.dot(C, y1 - 30, 24)
    return [(CONTOUR, outline + contour + eaves), (DETAIL, detail + thatch + crest)]


def _jaguar():
    contour, detail = head(CX0, CY0, CX1, CY1 - 60, eye_kind="spiral", tooth=False, spool=False, band=False)
    spots = []
    for u, v in ((0.62, 0.76), (0.8, 0.6), (0.78, 0.32), (0.6, 0.22), (0.55, 0.5)):
        x, y = CX0 + u * CW, CY0 + v * (CH - 60)
        spots += S.ring(x, y, 48) + S.dot(x, y, 12)
    fangs = S.poly([(CX0 + 0.1 * CW, CY0 + 0.3 * CH), (CX0 + 0.14 * CW, CY0 + 0.16 * CH),
                    (CX0 + 0.18 * CW, CY0 + 0.3 * CH)])
    ears = []
    for u in (0.52, 0.74):
        x = CX0 + u * CW
        ears += S.arc(x, CY1 - 70, 52, 62, 10, 170)
    return [(CONTOUR, contour + ears), (DETAIL, detail + spots + fangs)]


def _sun():
    box = (170, CY0 + 60, CX1, CY1)
    cx, cy = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2 + 10
    rays = [t for k in range(10) for t in curl(cx + 190 * math.cos(math.radians(18 + k * 36)),
                                                  cy + 160 * math.sin(math.radians(18 + k * 36)), 26, turns=1.0)]
    return [(CONTOUR, cushion(*box) + prefix_on(box, 120, n=3, kind="beads")),
            (DETAIL, S.ring(cx, cy, 145) + dotted_arc(cx, cy, 100, 100, 0, 360) + curl(cx, cy, 62, turns=1.6)
             + rays + fringe_on(box, h=46))]


def _moon():
    box = (CX0, CY0, CX1, CY1 - 110)
    return [(CONTOUR, cushion(*box) + superfix_on(box, 100, "dots")),
            (DETAIL, S.arc(C - 40, C - 60, 210, 190, 75, 285) + S.arc(C + 50, C - 60, 160, 160, 90, 270)
             + net(C - 220, C - 140, 90, 160) + curl(C + 190, C - 30, 62, turns=1.3)
             + dotted([(C + 110, CY0 + 70), (CX1 - 70, CY0 + 70)]))]


def _water():
    box = (165, CY0, CX1, CY1)
    return [(CONTOUR, cushion(*box) + prefix_on(box, 115, n=4, kind="bars")),
            (DETAIL, S.wave(215, C + 160, CX1 - 50, 40, 1.5) + dotted([(225, C + 80), (CX1 - 60, C + 80)])
             + S.wave(215, C, CX1 - 50, 40, 1.5) + curl(320, C - 160, 75, turns=1.3)
             + curl(560, C - 160, 75, turns=1.3, clockwise=True) + S.dot(440, C - 150, 24))]


def _peak():
    box = (CX0, CY0, CX1, CY1 - 110)
    steps = [(CX0 + 80, CY0 + 60), (CX0 + 80, CY0 + 150), (CX0 + 170, CY0 + 150), (CX0 + 170, CY0 + 240),
             (CX0 + 260, CY0 + 240), (CX0 + 260, CY0 + 330), (CX1 - 260, CY0 + 330), (CX1 - 260, CY0 + 240),
             (CX1 - 170, CY0 + 240), (CX1 - 170, CY0 + 150), (CX1 - 80, CY0 + 150), (CX1 - 80, CY0 + 60)]
    terraces = []
    for y, x0, x1 in ((CY0 + 105, CX0 + 130, CX1 - 130), (CY0 + 195, CX0 + 220, CX1 - 220), (CY0 + 285, CX0 + 310, CX1 - 310)):
        terraces += dotted([(x0, y), (x1, y)])
    smoke = curl(C - 40, CY0 + 460, 50, turns=1.2) + curl(C + 50, CY0 + 490, 42, turns=1.2, clockwise=True)
    return [(CONTOUR, cushion(*box) + superfix_on(box, 110, "x")),
            (DETAIL, S.poly(steps) + S.bar(CX0 + 50, CY0 + 60, CX1 - 50, CY0 + 60) + terraces
             + S.poly([(C - 60, CY0 + 330), (C - 60, CY0 + 410), (C + 60, CY0 + 410), (C + 60, CY0 + 330)])
             + S.ring(C, CY0 + 370, 16) + smoke)]


def R_dotted_line(points):
    return dotted(points, r=10, step=34)


def _coefficient(n):
    """A number set before the sign it counts: half a block wide, in no frame, its bars
    upright beside the sign and its dots stacked up the column before them."""
    def draw():
        out = []
        bars, dots = divmod(n, 5)
        x = WIDTH["half"] - 70
        for _ in range(bars):
            out.append(S.Fill(S._capsule(x, CY0 + 50, x, CY1 - 50, 32)))
            x -= 100
        if dots:
            gap = (CY1 - CY0 - 120) / max(dots - 1, 1) if dots > 1 else 0
            y0 = C - (dots - 1) * min(gap, 120) / 2
            out += [f for i in range(dots) for f in S.dot(x + 10, y0 + i * min(gap, 120), 40)]
        return [(CONTOUR, out)]
    return draw


def cartouche(cx=C, cy=C - 5, r=None):
    """The round cartouche, kept for the days of the count."""
    r = r or (CY1 - CY0) / 2 + 10
    return S.ring(cx, cy, r)


def _tqan():
    # the 260-day count in its round cartouche: a sleeping face, its lashes down, a wavering
    # mouth, and the points of the count about it
    cx, cy = C, C - 5
    lashes = S.arc(cx - 30, cy + 70, 130, 60, 200, 340)
    for a in (220, 250, 280, 310):
        t = math.radians(a)
        lashes += S.tick(cx - 30 + 130 * math.cos(t), cy + 70 + 60 * math.sin(t), 34, angle=a)
    mouth = S.wave(cx - 150, cy - 110, cx + 110, 22, 1.5)
    return [(CONTOUR, cartouche(cx, cy)),
            (DETAIL, lashes + mouth + S.dot(cx + 170, cy + 120, 14) + S.dot(cx + 210, cy + 40, 14)
             + S.dot(cx + 190, cy - 40, 14) + curl(cx + 140, cy - 190, 40, turns=1.0))]


def _serpent():
    # the serpent, double-wide: a long head in profile, its jaw lined with teeth and a fang,
    # the spiral eye under a heavy brow, scales down its back, its tongue curling out
    x0, y0, x1, y1 = CX0, CY0 + 30, 2 * B - 20, CY1 - 50
    contour, detail = head(x0, y0, x1, y1, eye_kind="spiral", tooth=False, spool=False, band=False)
    w, h = x1 - x0, y1 - y0
    X = lambda u: x0 + u * w  # noqa: E731
    Y = lambda v: y0 + v * h  # noqa: E731
    teeth = []
    for k in range(5):
        x = X(0.14 + k * 0.045)
        teeth += S.poly([(x - 18, Y(0.36)), (x, Y(0.28)), (x + 18, Y(0.36))])
    scales = []
    for k in range(5):
        cx, cy = X(0.52 + k * 0.09), Y(0.66 - 0.06 * (k % 2))
        scales += S.ring(cx, cy, 48) + S.dot(cx, cy, 12)
    tongue = curl(X(0.0) - 30, Y(0.33), 46, turns=1.0, clockwise=True)
    belly = dotted([(X(0.42), Y(0.18)), (X(0.9), Y(0.22))])
    return [(CONTOUR, contour), (DETAIL, detail + teeth + scales + tongue + belly)]


SUN = Glyph("SUN", "the sun", "tse", _sun)
MOON = Glyph("MOON", "the moon", "i", _moon)
WATER = Glyph("WATER", "water", "ne", _water)
JAGUAR = Glyph("JAGUAR", "the jaguar", "i", _jaguar)
LORD = Glyph("LORD", "a lord", "ma", _lord)
PEAK = Glyph("PEAK", "the sacred peak", "ku", _peak)
PATRIARCH = Glyph("PATRIARCH", "the patriarch: MAN, HIGH and HOUSE made one", "che", _patriarch)
THIRTEEN = Glyph("N13", "thirteen, a coefficient", "o", _coefficient(13), "half")
TQAN = Glyph("TQ'AN", "the 260-day count, a day in its cartouche", "qa", _tqan)
SERPENT = Glyph("SERPENT", "the serpent", "cha", _serpent, "double")

PILOT = [LORD, PATRIARCH, JAGUAR, SUN, MOON, WATER, PEAK, THIRTEEN, TQAN, SERPENT]


def _ink_one(part, pen) -> pathops.Path:
    """One part's ink. A long track the simplifier rejects is inked in two halves that share
    a point and joined, which draws the same ink."""
    try:
        return S.ink([part], pen)
    except pathops.PathOpsError:
        if isinstance(part, S.Fill) or len(part.pts) < 4:
            raise
        m = len(part.pts) // 2
        a = S.Track(part.pts[: m + 1], weight=part.weight)
        b = S.Track(part.pts[m:] + (part.pts[:1] if part.closed else []), weight=part.weight)
        return pathops.op(_ink_one(a, pen), _ink_one(b, pen), pathops.PathOp.UNION)


def ink(parts, seed=0) -> pathops.Path:
    """The union of every part, each drawn by its own brush, the brush wandering a little."""
    out = pathops.Path()
    for pen, ps in parts:
        drawn = wobble(ps, seed)
        try:
            p = S.ink(drawn, pen)
        except pathops.PathOpsError:
            # The simplifier can reject a union of many parts that it accepts one at a
            # time; join them one by one, which draws the same ink.
            p = pathops.Path()
            for part in drawn:
                q = _ink_one(part, pen)
                p = pathops.op(p, q, pathops.PathOp.UNION) if list(p) else q
        out = pathops.op(out, p, pathops.PathOp.UNION) if list(out) else p
    return out
