# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Kin, strangers and the dead in the Ch'alish P'ilam ceremonial hand.

    import kin as N

    parts = N.KINSMAN.draw()                 # [(pen, parts), ...]

Where the common hand writes a person with a place, a rank or a quarter, the ceremonial
hand draws one picture. A head stands within INSIDE's walled square or outside its open
wall; under LOW's bar or over HIGH's; at the top of NORTH's cross or at its foot. A woman
wears the braid of beads behind her head and the bead at her ear, as WOMAN does. Two
heads one behind the other are a people.
"""

from __future__ import annotations

import math

import pathops

import ceremonial as R
import strokes as S
from ceremonial import CONTOUR, DETAIL, CX0, CX1, CY0, CY1, C, Glyph


def _woman(box, braid=True):
    """WOMAN's marks on a head in ``box``: the bead at her ear and the braid of beads
    hanging behind her head."""
    x0, y0, x1, y1 = box
    out = S.dot(x0 + 0.62 * (x1 - x0), y0 + 0.5 * (y1 - y0), 20)
    if braid:
        out += R.dotted([(x1 + 30, y1 - 60), (x1 + 30, y0 + 40)], r=14)
    return out


def _aged(box):
    """The face of age: a line under the eye and one from the nose to the mouth's corner."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    m = min(w, h)
    ey = y0 + 0.56 * h
    return S.arc(x0 + 0.29 * w, ey - m * 0.1, m * 0.15, m * 0.07, 215, 325) + \
        S.arc(x0 + 0.2 * w, y0 + 0.36 * h, m * 0.1, h * 0.12, 270, 350)


def _person(box, woman=False, young=False, eye="open", aged=False):
    """A head in ``box`` facing the line's start, with WOMAN's marks or the face of age."""
    contour, detail = R.head(*box, eye_kind=eye, band=False, spool=not woman and not young)
    if woman:
        detail += _woman(box)
    if aged:
        detail += _aged(box)
    return contour, detail


def _square(x0, y0, x1, y1, open_end=None):
    """INSIDE's walled square; ``open_end`` leaves the side at the line's end open, the
    top and foot of the wall stopping there."""
    if open_end is None:
        return S.poly([(x0, y0), (x0, y1), (x1, y1), (x1, y0), (x0, y0)])
    return S.poly([(open_end, y0), (x0, y0), (x0, y1), (open_end, y1)])


# -- within and beyond ------------------------------------------------------------------------------


def _kinsman():
    # a kinsman: MAN within INSIDE's walled square, the head the jewel it holds
    wall = _square(C - 240, CY0 + 80, C + 240, CY1 - 80)
    contour, detail = _person((C - 185, CY0 + 80, C + 180, CY1 - 145))
    return [(CONTOUR, R.cushion() + wall + contour), (DETAIL, detail)]


def _stranger():
    # a stranger: MAN outside OUTSIDE's open wall, facing it from beyond its opening
    wall = _square(CX0 + 70, C - 150, None, C + 150, open_end=C - 105)
    trail = R.dotted([(CX0 + 135, C), (C - 130, C)], r=13)
    contour, detail = _person((C - 60, CY0 + 90, CX1 - 85, CY1 - 95))
    return [(CONTOUR, R.cushion() + wall + contour), (DETAIL, detail + trail)]


def _home():
    # a home: HOUSE's roof as the block's crown, INSIDE's walled square and its jewel under it
    x0, y0, x1, y1 = CX0, CY0, CX1, CY1 - 20
    outline, (le, re) = R.roofed(x0, y0, x1, y1, ridge=y1 + 40)
    eaves = S.bar(le[0] + 10, le[1], re[0] - 10, re[1])
    top = le[1] - 70
    wall = _square(C - 170, CY0 + 85, C + 170, top)
    jewel = R.bead(C, (CY0 + 85 + top) / 2, 72)
    thatch = S.bar(le[0] + 95, le[1] + 22, C, y1 + 40 - 95) + S.bar(re[0] - 95, re[1] + 22, C, y1 + 40 - 95)
    return [(CONTOUR, outline + eaves + wall), (DETAIL, jewel + thatch)]


def _hut(cx, y, s):
    """A small house of HOUSE's form standing on ``y``: the roof on its posts and the
    doorway between them."""
    roof = S.poly([(cx - 1.35 * s, y + 1.05 * s), (cx, y + 2.1 * s), (cx + 1.35 * s, y + 1.05 * s)])
    posts = S.bar(cx - s, y + 1.05 * s, cx - s, y) + S.bar(cx + s, y + 1.05 * s, cx + s, y)
    door = S.arc(cx, y + 0.5 * s, 0.38 * s, 0.38 * s, 0, 180) + S.bar(cx - 0.38 * s, y + 0.5 * s, cx - 0.38 * s, y) + \
        S.bar(cx + 0.38 * s, y + 0.5 * s, cx + 0.38 * s, y)
    return roof + posts + door


def _village():
    # a village: houses standing together on the ground, and OUTSIDE's dotted path running
    # out from them to its jewel
    ground = C - 30
    huts = _hut(C, ground, 105) + _hut(C - 215, ground, 64) + _hut(C + 215, ground, 64)
    y = CY0 + 140
    path = R.dotted([(CX0 + 90, y), (CX1 - 250, y)], r=13) + R.bead(CX1 - 170, y, 58)
    return [(CONTOUR, R.cushion() + S.bar(CX0 + 60, ground, CX1 - 60, ground)), (DETAIL, huts + path)]


# -- lesser and greater -----------------------------------------------------------------------------


def _under_low(woman):
    def draw():
        # a boy or girl, a servant: a young head as LOW's jewel, under its bar
        y = CY1 - 150
        bar = S.bar(CX0 + 60, y, CX1 - 60, y)
        dots = R.dotted([(C - 200, CY1 - 75), (C + 200, CY1 - 75)])
        box = (C - 190, CY0 + 85, C + (100 if woman else 170), y - 60)
        contour, detail = _person(box, woman=woman, young=True)
        return [(CONTOUR, R.cushion() + bar + contour), (DETAIL, detail + dots)]
    return draw


def _over_high(woman):
    def draw():
        # an elder: an aged head as HIGH's jewel, raised over its bar
        y = CY0 + 150
        bar = S.bar(CX0 + 60, y, CX1 - 60, y)
        dots = R.dotted([(C - 200, CY0 + 75), (C + 200, CY0 + 75)])
        box = (C - 220, y + 60, C + (140 if woman else 225), CY1 - 85)
        contour, detail = _person(box, woman=woman, aged=True)
        return [(CONTOUR, R.cushion() + bar + contour), (DETAIL, detail + dots)]
    return draw


def _god():
    # a god, an ancestor raised to the sky: the head with a god's spiral eye, raised over
    # the band of the sky and its stars
    lo, hi = CY0 + 70, CY0 + 200
    band = S.bar(CX0 + 60, lo, CX1 - 60, lo) + S.bar(CX0 + 60, hi, CX1 - 60, hi)
    stars = []
    for x in (C - 190, C, C + 190):
        stars += R.x_mark(x, (lo + hi) / 2, 36)
    contour, detail = _person((C - 220, hi + 65, C + 225, CY1 - 85), eye="spiral")
    return [(CONTOUR, R.cushion() + band + contour), (DETAIL, detail + stars)]


# -- the world above and the world below ----------------------------------------------------------


def _above():
    # an exalted ancestor: the head at the top of NORTH's cross, in the zenith, ringed with
    # its light, its eye closed in death
    box = (C - 175, C - 20, C + 160, CY1 - 70)
    hx, hy = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2
    cross = S.bar(C, CY0 + 60, C, box[1]) + S.bar(CX0 + 60, CY0 + 200, CX1 - 60, CY0 + 200)
    light = R.dotted_arc(hx, hy, 245, 200, -15, 195)
    contour, detail = _person(box, eye="closed")
    return [(CONTOUR, R.cushion() + cross + contour), (DETAIL, detail + light)]


def _below():
    # a soul among the dead: the head at the foot of SOUTH's cross, under the world, its
    # eye closed, between the two marks of the dark
    box = (C - 175, CY0 + 80, C + 160, C + 50)
    cross = S.bar(C, box[3], C, CY1 - 60) + S.bar(CX0 + 60, CY1 - 170, CX1 - 60, CY1 - 170)
    dark = R.x_mark(CX0 + 90, C - 40, 40) + R.x_mark(CX1 - 90, C - 40, 40)
    contour, detail = _person(box, eye="closed")
    return [(CONTOUR, R.cushion() + cross + contour), (DETAIL, detail + dark)]


# -- many ---------------------------------------------------------------------------------------------


def _inside(pts, x, y):
    """Whether (x, y) lies inside the closed outline ``pts``."""
    n, hit = len(pts), False
    for i in range(n):
        (ax, ay), (bx, by) = pts[i], pts[(i + 1) % n]
        if (ay > y) != (by > y) and x < ax + (y - ay) * (bx - ax) / (by - ay):
            hit = not hit
    return hit


def _behind(front, parts, margin=0.0):
    """``parts`` with what the ``front`` outline hides left out: each track is cut where it
    passes behind it, and a fill under it is dropped."""
    pts = front.pts
    def hidden(x, y):
        if _inside(pts, x, y):
            return True
        return margin and min((x - px) ** 2 + (y - py) ** 2 for px, py in pts) < margin ** 2
    out = []
    for p in parts:
        if isinstance(p, S.Fill):
            if not any(hidden(x, y) for x, y in p.pts):
                out.append(p)
            continue
        run = []
        seq = p.pts + (p.pts[:1] if p.closed else [])
        for x, y in seq:
            if hidden(x, y):
                if len(run) > 1:
                    out.append(S.Track(run, weight=p.weight))
                run = []
            else:
                run.append((x, y))
        if len(run) > 1:
            out.append(S.Track(run, weight=p.weight))
    return out


def _union(a, b):
    """The outline of two overlapping closed outlines taken together."""
    def shape(pts):
        path = pathops.Path()
        pen = path.getPen()
        pen.moveTo(pts[0])
        for q in pts[1:]:
            pen.lineTo(q)
        pen.closePath()
        return path
    joined = max(S.contours(pathops.op(shape(a), shape(b), pathops.PathOp.UNION)), key=len)
    # the union keeps points closer than a track's sampling interval, which the brush
    # cannot stroke cleanly
    out = [joined[0]]
    for q in joined[1:]:
        if math.dist(q, out[-1]) >= S.STEP:
            out.append(q)
    return out


def _many(woman):
    def draw():
        # a people: two heads one behind the other, the nearer lower and before; women
        # wear WOMAN's marks. The two profiles make one outline, and the nearer head's
        # crown is drawn across the one behind.
        front_box = (CX0, CY0, C + 175, C + 170)
        back_box = (C - 55, C - 25, CX1 - (50 if woman else 0), CY1 + 10)
        fc, fd = R.head(*front_box, band=False, spool=not woman)
        bc, bd = _person(back_box, woman=woman)
        if woman:
            fd += _woman(front_box, braid=False)  # the nearer braid would hang over the head behind
        front, back = fc[0].pts, bc[0].pts
        outline = S.Track(_union(front, back), closed=True)
        crown = S.Track([q for q in front if _inside(back, *q)])
        back_detail = _behind(fc[0], bd, margin=R.GAP + CONTOUR.full)
        return [(CONTOUR, [outline, crown]), (DETAIL, fd + back_detail)]
    return draw


KINSMAN = Glyph("KINSMAN", "a kinsman: MAN and INSIDE made one", "na", _kinsman)
STRANGER = Glyph("STRANGER", "a stranger: MAN and OUTSIDE made one", "sha", _stranger)
HOME = Glyph("HOME", "a home: HOUSE and INSIDE made one", "shu", _home)
VILLAGE = Glyph("VILLAGE", "a village: HOUSE and OUTSIDE made one", "shu", _village)
BOY = Glyph("BOY", "a boy, a servant: MAN and LOW made one", "na", _under_low(False))
GIRL = Glyph("GIRL", "a girl, a servant: WOMAN and LOW made one", "na", _under_low(True))
ELDER = Glyph("ELDER", "an elder, a chief: MAN and HIGH made one", "shu", _over_high(False))
ELDER_WOMAN = Glyph("ELDER-WOMAN", "an elder woman: WOMAN and HIGH made one", "che", _over_high(True))
PEOPLE = Glyph("PEOPLE", "a people, everyone: MAN and MAN made one", "che", _many(False))
WOMEN = Glyph("WOMEN", "women: WOMAN and WOMAN made one", "che", _many(True))
GOD = Glyph("GOD", "a god, an exalted ancestor raised to the sky: MAN, HIGH and SKY made one", "che", _god)
EXALTED_ANCESTOR = Glyph("EXALTED-ANCESTOR", "an ancestor in the world above: MAN and NORTH made one", "na", _above)
SOUL_AMONG_THE_DEAD = Glyph("SOUL-AMONG-THE-DEAD", "a soul in the world below: MAN and SOUTH made one", "che", _below)

KIN = [KINSMAN, STRANGER, HOME, VILLAGE, BOY, GIRL, ELDER, ELDER_WOMAN, PEOPLE, WOMEN, GOD, EXALTED_ANCESTOR,
       SOUL_AMONG_THE_DEAD]
