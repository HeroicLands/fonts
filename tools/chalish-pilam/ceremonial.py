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
    X = lambda u: x0 + u * w  # noqa: E731
    Y = lambda v: y0 + v * h  # noqa: E731
    contour = profile(x0, y0, x1, y1)
    detail = []
    detail += S.arc(X(0.3), Y(0.6), w * 0.17, h * 0.1, 25, 160)  # the brow
    if eye_kind == "open":
        detail += S.arc(X(0.29), Y(0.5), w * 0.12, h * 0.12, 25, 155) + S.arc(X(0.29), Y(0.62), w * 0.12, h * 0.12, 205, 335)
        detail += S.dot(X(0.25), Y(0.62) - h * 0.1, w * 0.032)  # the pupil hangs from the upper lid
    elif eye_kind == "closed":
        detail += S.arc(X(0.29), Y(0.6), w * 0.1, h * 0.07, 200, 340)
    else:
        detail += curl(X(0.29), Y(0.56), w * 0.1, turns=1.4)
    detail += S.arc(X(0.11), Y(0.44), w * 0.06, h * 0.04, 120, 330)  # the upper lip
    detail += S.arc(X(0.12), Y(0.3), w * 0.06, h * 0.045, 30, 240)  # the lower lip
    if tooth:
        detail += S.poly([(X(0.08), Y(0.37)), (X(0.12), Y(0.27)), (X(0.16), Y(0.37))])
    detail += curl(X(0.4), Y(0.34), w * 0.08, turns=1.3, clockwise=True)  # the cheek
    if spool:
        detail += ear_spool(X(0.68), Y(0.46), w * 0.12)
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
    draw: Callable[[], list]  # [(pen, parts), ...]


def _lord():
    # a lord's head in profile: the beaded headband, a headdress of plumes rising over the
    # crown, netted hair at the back of the head, a jewelled ear spool with its pendant,
    # a bead at the nose, and the fringe under the chin
    x0, y0, x1, y1 = 190, CY0 + 60, CX1, CY1 - 90
    contour, detail = head(x0, y0, x1, y1)
    w, h = x1 - x0, y1 - y0
    X = lambda u: x0 + u * w  # noqa: E731
    Y = lambda v: y0 + v * h  # noqa: E731
    hair = []
    for k in range(3):
        hair += S.arc(X(0.62), Y(0.5), w * 0.36 - 44 * (k + 1), h * 0.46 - 44 * (k + 1), 18, 52)
    plumes = []
    for k, u in enumerate((0.3, 0.5, 0.7, 0.9)):
        plumes += S.arc(X(u) + 30, CY1 - 50, 55, 70, 180, 360 if k % 2 else 300)
        plumes += curl(X(u), CY1 - 20, 32, turns=1.1, clockwise=bool(k % 2))
    pendant = S.bar(X(0.68), Y(0.46) - w * 0.12, X(0.68), Y(0.12)) + bead(X(0.68), Y(0.08), 22)
    jaw = dotted_arc(X(0.4), Y(0.42), w * 0.32, h * 0.36, 215, 300, r=10, step=36)
    return [(CONTOUR, contour + prefix(CX0, CY0 + 80, 178, CY1 - 100, "bars")
             + S.arc(X(0.6), CY1 - 70, w * 0.42, 60, 0, 180)),
            (DETAIL, detail + hair + plumes + pendant + jaw + bead(X(0.0) - 8, Y(0.5), 18)
             + fringe(x0 + 40, x1 - 60, y0 + 6, h=44))]


def _jaguar():
    contour, detail = head(CX0, CY0, CX1, CY1, eye_kind="spiral", tooth=False, spool=False, band=False)
    spots = []
    for u, v in ((0.62, 0.78), (0.8, 0.62), (0.84, 0.34), (0.64, 0.24), (0.55, 0.5)):
        x, y = CX0 + u * CW, CY0 + v * CH
        spots += S.ring(x, y, 48) + S.dot(x, y, 12)
    fangs = S.poly([(CX0 + 0.12 * CW, CY0 + 0.34 * CH), (CX0 + 0.16 * CW, CY0 + 0.2 * CH),
                    (CX0 + 0.2 * CW, CY0 + 0.34 * CH)])
    ear = S.arc(CX0 + 0.55 * CW, CY1 - 10, 70, 70, 10, 170)
    return [(CONTOUR, contour + ear), (DETAIL, detail + spots + fangs)]


def _sun():
    # the sun: a disk inside a ring of beads, wrapped in curling rays, over the fringe, with
    # its bead prefix; at its heart the burning eye
    cx, cy = C + 50, C + 40
    rays = [t for k in range(10) for t in curl(cx + 205 * math.cos(math.radians(18 + k * 36)),
                                                    cy + 172 * math.sin(math.radians(18 + k * 36)), 28, turns=1.1)]
    return [(CONTOUR, cushion(140, CY0 + 70, CX1, CY1) + prefix(CX0, CY0 + 120, 152, CY1 - 50, "beads")),
            (DETAIL, S.ring(cx, cy, 160) + dotted_arc(cx, cy, 112, 112, 0, 360) + curl(cx, cy, 70, turns=1.6) + rays
             + fringe(170, CX1 - 30, CY0 + 76, h=44))]


def _moon():
    main = cushion(CX0, CY0, CX1, CY1 - 120)
    return [(CONTOUR, main + superfix(CX0 + 60, CY1 - 110, CX1 - 60, CY1, "dots")),
            (DETAIL, S.arc(C - 40, C - 70, 210, 190, 75, 285) + S.arc(C + 50, C - 70, 160, 160, 90, 270)
             + net(C - 220, C - 170, 120, 200, n=4) + curl(C + 190, C - 30, 60, turns=1.3)
             + R_dotted_line([(C + 120, CY0 + 70), (CX1 - 60, CY0 + 70)]))]


def _water():
    main = cushion(150, CY0, CX1, CY1)
    return [(CONTOUR, main + prefix(CX0, CY0 + 40, 162, CY1 - 40, "beads")),
            (DETAIL, S.wave(200, C + 160, CX1 - 50, 40, 1.5) + dotted([(210, C + 80), (CX1 - 60, C + 80)])
             + S.wave(200, C, CX1 - 50, 40, 1.5) + curl(310, C - 160, 75, turns=1.3)
             + curl(560, C - 160, 75, turns=1.3, clockwise=True) + S.dot(435, C - 150, 24))]


def _peak():
    # the sacred peak: a stepped pyramid with its shrine, smoke curling from the shrine,
    # each terrace marked, under a superfix of netting
    steps = [(CX0 + 80, CY0 + 60), (CX0 + 80, CY0 + 150), (CX0 + 170, CY0 + 150), (CX0 + 170, CY0 + 240),
             (CX0 + 260, CY0 + 240), (CX0 + 260, CY0 + 330), (CX1 - 260, CY0 + 330), (CX1 - 260, CY0 + 240),
             (CX1 - 170, CY0 + 240), (CX1 - 170, CY0 + 150), (CX1 - 80, CY0 + 150), (CX1 - 80, CY0 + 60)]
    terraces = []
    for y, x0, x1 in ((CY0 + 105, CX0 + 130, CX1 - 130), (CY0 + 195, CX0 + 220, CX1 - 220), (CY0 + 285, CX0 + 310, CX1 - 310)):
        terraces += dotted([(x0, y), (x1, y)], r=9, step=40)
    stair = []
    smoke = curl(C - 40, CY0 + 470, 48, turns=1.3) + curl(C + 50, CY0 + 500, 40, turns=1.3, clockwise=True)
    return [(CONTOUR, cushion(CX0, CY0, CX1, CY1 - 130) + superfix(CX0 + 40, CY1 - 120, CX1 - 40, CY1, "net")),
            (DETAIL, S.poly(steps) + S.bar(CX0 + 50, CY0 + 60, CX1 - 50, CY0 + 60) + terraces + stair
             + S.poly([(C - 60, CY0 + 330), (C - 60, CY0 + 410), (C + 60, CY0 + 410), (C + 60, CY0 + 330)])
             + S.ring(C, CY0 + 370, 16) + smoke)]


def R_dotted_line(points):
    return dotted(points, r=10, step=34)


def _bar_dot(n):
    def draw():
        out = []
        bars, dots = divmod(n, 5)
        y = CY0 + 40
        for _ in range(bars):
            out.append(S.Fill(S._capsule(CX0 + 60, y + 35, CX1 - 60, y + 35, 35)))
            y += 110
        if dots:
            gap = 120
            x0 = C - (dots - 1) * gap / 2
            out += [f for i in range(dots) for f in S.dot(x0 + i * gap, y + 50, 46)]
        return [(CONTOUR, out)]
    return draw


SUN = Glyph("SUN", "the sun", "tse", _sun)
MOON = Glyph("MOON", "the moon", "i", _moon)
WATER = Glyph("WATER", "water", "ne", _water)
JAGUAR = Glyph("JAGUAR", "the jaguar", "i", _jaguar)
LORD = Glyph("LORD", "a lord", "ma", _lord)
PEAK = Glyph("PEAK", "the sacred peak", "ku", _peak)
THIRTEEN = Glyph("N13", "thirteen", "o", _bar_dot(13))

PILOT = [LORD, JAGUAR, SUN, MOON, WATER, PEAK, THIRTEEN]


def ink(parts, seed=0) -> pathops.Path:
    """The union of every part, each drawn by its own brush, the brush wandering a little."""
    out = pathops.Path()
    for pen, ps in parts:
        p = S.ink(wobble(ps, seed), pen)
        out = pathops.op(out, p, pathops.PathOp.UNION) if list(out) else p
    return out
