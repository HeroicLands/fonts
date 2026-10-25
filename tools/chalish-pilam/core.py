# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""The core concepts in the Ch'alish P'ilam ceremonial hand.

    import core as Z

    parts = Z.SKY.draw()                     # [(pen, parts), ...]

The 24 concepts every reader of the common hand knows, each drawn whole as a ceremonial
glyph. SUN, MOON and WATER are the pilot's, in ceremonial.py. People and the body are
heads and hands in the head canon; the quarters keep the common hand's family, the sun at
the horizon and at the ends of the cross, in the ceremonial manner.
"""

from __future__ import annotations

import math

import ceremonial as R
import strokes as S
from ceremonial import CONTOUR, DETAIL, CX0, CX1, CY0, CY1, C, Glyph


def _sky():
    # the sky: a band of sky over the horizon, its stars set in it as crossed bars
    band = S.bar(CX0 + 50, C + 70, CX1 - 50, C + 70) + S.bar(CX0 + 50, C - 70, CX1 - 50, C - 70)
    stars = []
    for x in (C - 180, C, C + 180):
        stars += R.x_mark(x, C, 42)
    return [(CONTOUR, R.cushion() + band), (DETAIL, stars + R.dotted([(C - 200, CY1 - 90), (C + 200, CY1 - 90)])
                                          + R.dotted([(C - 200, CY0 + 90), (C + 200, CY0 + 90)]))]


def _star():
    # a star: four points about a ringed heart, and its light in dots
    pts = []
    for k in range(9):
        a = math.radians(90 + k * 45)
        rr = 230 if k % 2 == 0 else 80
        pts.append((C + rr * math.cos(a), C - 10 + rr * math.sin(a)))
    return [(CONTOUR, R.cushion() + S.poly(pts)), (DETAIL, S.dot(C, C - 10, 30))]


def _fire():
    # fire: three tongues of flame rising from a bed of embers
    tongues = []
    for dx, h in ((-140, 300), (0, 400), (140, 300)):
        x = C + dx
        tongues += [S.Track(S._bezier((x - 60, CY0 + 120), (x - 90, CY0 + 120 + h * 0.5), (x - 10, CY0 + 120 + h * 0.6), (x, CY0 + 120 + h))
                            + S._bezier((x, CY0 + 120 + h), (x + 40, CY0 + 120 + h * 0.5), (x + 70, CY0 + 120 + h * 0.4), (x + 60, CY0 + 120))[1:])]
    embers = R.dotted([(C - 210, CY0 + 70), (C + 210, CY0 + 70)], r=13)
    return [(CONTOUR, R.cushion() + tongues), (DETAIL, embers)]


def _earth():
    # earth, soil: the ground's line over tilled furrows, a sprouting seed in one
    ground = S.bar(CX0 + 50, C + 60, CX1 - 50, C + 60)
    furrows = []
    for k in range(3):
        furrows += S.arc(C - 180 + k * 180, C - 60, 70, 60, 200, 340)
    seed = S.bar(C, C + 60, C, CY1 - 90) + S.arc(C - 90, C + 160, 90, 70, 330, 400) + \
        S.arc(C + 90, C + 210, 90, 70, 140, 210)
    return [(CONTOUR, R.cushion() + ground), (DETAIL, furrows + seed + R.dotted([(C - 200, CY0 + 70), (C + 200, CY0 + 70)]))]


def _stone():
    # stone, the mountain: a cut block, its crack, and the X of hardness on its face
    block = S.poly([(C - 190, CY0 + 90), (C + 190, CY0 + 90), (C + 170, CY1 - 130), (C - 150, CY1 - 110), (C - 190, CY0 + 90)])
    crack = S.poly([(C + 40, CY1 - 125), (C + 90, C + 50), (C + 20, C - 40)])
    return [(CONTOUR, R.cushion() + block), (DETAIL, crack + R.x_mark(C - 90, C - 60, 60))]


def _person(woman=False):
    def draw():
        # a person, a head in profile; a woman wears a braid of beads hanging behind her head
        x0, y0, x1, y1 = (CX0 + 40, CY0 + 20, CX1 - 120, CY1 - 60) if woman else (CX0 + 40, CY0 + 20, CX1 - 40, CY1 - 60)
        contour, detail = R.head(x0, y0, x1, y1, spool=not woman, band=False)
        if woman:
            bx = x1 + 40
            detail += R.dotted([(bx, y1 - 120), (bx, y0 + 40)], r=20)
            detail += S.dot(x0 + 0.62 * (x1 - x0), y0 + 0.5 * (y1 - y0), 26)
        return [(CONTOUR, contour), (DETAIL, detail)]
    return draw


def _plant():
    # vegetation: a stalk with three leaves unfurling, its root in the ground
    stalk = S.bar(C, CY0 + 60, C, CY1 - 80)
    leaves = S.arc(C - 120, C - 20, 120, 110, 0, 100) + S.arc(C + 120, C + 60, 120, 110, 80, 180) + \
        R.curl(C, CY1 - 90, 50, turns=1.0)
    root = S.bar(C - 160, CY0 + 60, C + 160, CY0 + 60) + S.bar(C, CY0 + 60, C - 60, CY0 + 10) + S.bar(C, CY0 + 60, C + 60, CY0 + 10)
    return [(CONTOUR, R.cushion() + stalk + leaves), (DETAIL, root)]


def _beast():
    # an animal: a four-footed beast in profile, its spotted flank, facing the line's start
    back = S.arc(C + 40, C - 40, 230, 160, 0, 180)
    belly = S.bar(C - 190, C - 40, C + 270, C - 40)
    legs = []
    for x in (C - 140, C - 40, C + 140, C + 230):
        legs += S.bar(x, C - 40, x, CY0 + 40)
    head = S.ring(CX0 + 90, C + 140, 60) + S.bar(CX0 + 140, C + 110, C - 190, C - 30)
    spots = S.dot(C + 30, C + 50, 20) + S.dot(C + 140, C + 30, 20)
    return [(CONTOUR, R.cushion() + back + belly + head), (DETAIL, legs + spots)]


def _horizon(rising):
    def draw():
        # east and west: the sun at the horizon, rising over it with rays, or sinking under
        # it with its last light falling below
        y = C - 40 if rising else C + 90
        disk = S.arc(C, y, 170, 170, 0, 180) if rising else S.arc(C, y, 170, 170, 180, 360)
        line = S.bar(CX0 + 50, y, CX1 - 50, y)
        out = []
        if rising:
            out += S.dot(C, y + 70, 26)
            for a in (30, 70, 110, 150):
                t = math.radians(a)
                out += S.bar(C + 210 * math.cos(t), y + 210 * math.sin(t), C + 270 * math.cos(t), y + 270 * math.sin(t))
        else:
            for dx in (-110, 0, 110):
                out += S.bar(C + dx, y - 210, C + dx * 1.2, y - 290)
        return [(CONTOUR, R.cushion() + disk + line), (DETAIL, out)]
    return draw


def _quarter(up):
    def draw():
        # north and south: the cross of the quarters, the sun at its top (the zenith) ringed
        # with light, or at its foot (under the world) between the dark's two marks
        cross = S.bar(C, CY0 + 60, C, CY1 - 60) + S.bar(CX0 + 60, C, CX1 - 60, C)
        y = CY1 - 140 if up else CY0 + 140
        mark = R.dotted_arc(C, y, 120, 120, 0, 360) if up else R.x_mark(C - 180, y, 46) + R.x_mark(C + 180, y, 46)
        return [(CONTOUR, R.cushion() + cross + S.ring(C, y, 70)), (DETAIL, S.dot(C, y, 22) + mark)]
    return draw


def _high():
    # above, greater: a bar with the jewel of rank raised over it
    return [(CONTOUR, R.cushion() + S.bar(CX0 + 60, C - 80, CX1 - 60, C - 80)),
            (DETAIL, R.bead(C, C + 110, 70) + R.dotted([(C - 200, C - 160), (C + 200, C - 160)]))]


def _low():
    # below, lesser: a bar with the jewel beneath it
    return [(CONTOUR, R.cushion() + S.bar(CX0 + 60, C + 80, CX1 - 60, C + 80)),
            (DETAIL, R.bead(C, C - 110, 70) + R.dotted([(C - 200, C + 160), (C + 200, C + 160)]))]


def _inside():
    # within: a jewel enclosed in a walled square
    wall = S.poly([(C - 200, C - 200), (C - 200, C + 200), (C + 200, C + 200), (C + 200, C - 200), (C - 200, C - 200)])
    return [(CONTOUR, R.cushion() + wall), (DETAIL, R.bead(C, C, 70))]


def _outside():
    # beyond: the walled square open at one side, the jewel gone out through it
    wall = S.poly([(C + 60, C - 200), (C - 200, C - 200), (C - 200, C + 200), (C + 60, C + 200)])
    return [(CONTOUR, R.cushion() + wall), (DETAIL, R.bead(C + 190, C, 56) + R.dotted([(C - 120, C), (C + 80, C)]))]


def _house():
    # a house: the thatched roof on its posts, the doorway between them
    roof = S.poly([(CX0 + 50, C + 30), (C, CY1 - 50), (CX1 - 50, C + 30), (CX0 + 50, C + 30)])
    thatch = S.bar(C - 140, C + 100, C - 40, CY1 - 160) + S.bar(C + 140, C + 100, C + 40, CY1 - 160)
    posts = S.bar(C - 200, C + 30, C - 200, CY0 + 40) + S.bar(C + 200, C + 30, C + 200, CY0 + 40)
    door = S.arc(C, CY0 + 150, 80, 80, 0, 180) + S.bar(C - 80, CY0 + 150, C - 80, CY0 + 40) + S.bar(C + 80, CY0 + 150, C + 80, CY0 + 40)
    return [(CONTOUR, R.cushion() + roof + posts), (DETAIL, thatch + door)]


def _hand():
    # a hand, its back to the reader: palm, three fingers and the thumb
    import events as E
    palm, fingers = E._hand(C + 30, C - 60, 1.3, up=True)
    return [(CONTOUR, R.cushion() + palm), (DETAIL, fingers)]


def _eye():
    # the eye, seeing: the almond of the lids, the iris and its light
    lids = S.arc(C, C - 210, 300, 330, 42, 138) + S.arc(C, C + 210, 300, 330, 222, 318)
    iris = S.ring(C, C, 70) + S.dot(C - 18, C, 24)
    lashes = []
    for a in (60, 80, 100, 120):
        t = math.radians(a)
        x, y = C + 300 * math.cos(t), C - 210 + 330 * math.sin(t)
        lashes += S.tick(x + 30 * math.cos(t), y + 30 * math.sin(t), 40, angle=a)
    return [(CONTOUR, R.cushion() + lids), (DETAIL, iris + lashes)]


def _mouth():
    # the mouth, speaking: the open lips and the scroll of speech rising from them
    lips = S.arc(C + 40, C - 160, 220, 240, 45, 135) + S.arc(C + 40, C + 100, 220, 240, 225, 315)
    teeth = S.bar(C - 80, C - 30, C + 160, C - 30)
    scroll = R.curl(C - 170, C + 170, 70, turns=1.1) + S.bar(C - 120, C + 20, C - 170, C + 100)
    return [(CONTOUR, R.cushion() + lips), (DETAIL, teeth + scroll)]


SKY = Glyph("SKY", "the sky, the heavens", "hu", _sky)
STAR = Glyph("STAR", "a star", "i", _star)
FIRE = Glyph("FIRE", "fire", "ka", _fire)
EARTH = Glyph("EARTH", "earth, soil", "sha", _earth)
STONE = Glyph("STONE", "stone, the mountain", "ku", _stone)
MAN = Glyph("MAN", "a person, a man", "che", _person(False))
WOMAN = Glyph("WOMAN", "a woman", "che", _person(True))
PLANT = Glyph("PLANT", "vegetation", "shi", _plant)
BEAST = Glyph("BEAST", "an animal", "che", _beast)
EAST = Glyph("EAST", "the east, sunrise; birth", "tse", _horizon(True))
WEST = Glyph("WEST", "the west, sunset; death", "tse", _horizon(False))
NORTH = Glyph("NORTH", "the north, the zenith; the world above", "nu", _quarter(True))
SOUTH = Glyph("SOUTH", "the south, the nadir; the world below", "to", _quarter(False))
HIGH = Glyph("HIGH", "above, greater", "tsi", _high)
LOW = Glyph("LOW", "below, lesser", "cha", _low)
INSIDE = Glyph("INSIDE", "within", "chi", _inside)
OUTSIDE = Glyph("OUTSIDE", "beyond", "tsi", _outside)
HOUSE = Glyph("HOUSE", "a house, shelter", "shu", _house)
HAND = Glyph("HAND", "a hand", "pi", _hand)
EYE = Glyph("EYE", "the eye", "ka", _eye)
MOUTH = Glyph("MOUTH", "the mouth", "na", _mouth)

CORE = [SKY, STAR, FIRE, EARTH, STONE, MAN, WOMAN, PLANT, BEAST, EAST, WEST, NORTH, SOUTH, HIGH, LOW, INSIDE, OUTSIDE,
        HOUSE, HAND, EYE, MOUTH]
