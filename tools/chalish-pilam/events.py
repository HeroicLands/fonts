# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""The events of the record in the Ch'alish P'ilam ceremonial hand.

    import events as E

    parts = E.SEATING.draw()                 # [(pen, parts), ...]

What the stelae, lintels and codices record: births, accessions, deaths, wars, rites and
the turning of the counts. Each event is one glyph, mostly a hand, a figure or an object
caught in the act, drawn in the ceremonial canon of ``ceremonial.py``.
"""

from __future__ import annotations

import math

import ceremonial as R
import strokes as S
from ceremonial import CONTOUR, DETAIL, CX0, CX1, CY0, CY1, C, Glyph


def _hand(cx, cy, s=1.0, up=True):
    """A hand with its back to the reader: a palm, three fingers side by side, and the thumb
    out to the line's start. ``up`` points the fingers up; otherwise they hang down, as a
    hand reaching to take or give. A carved hand has room for three fingers with a groove
    between each; the white between them is a groove's width whatever the hand's size."""
    d = 1 if up else -1
    pw, ph = 280 * s, 150 * s
    palm = S.frame(cx - pw / 2, cy - ph / 2, pw, ph, square=2.6)
    gap = R.GAP + R.DETAIL.full + 18
    fw = (pw - 2 * gap) / 3
    r = fw / 2
    fl = 170 * s
    fingers = []
    for k in range(3):
        fx = cx - pw / 2 + r + k * (fw + gap)
        y0 = cy + d * (ph / 2 + r - 8)
        y1 = cy + d * (ph / 2 + fl - (30 * s if k != 1 else 0) - r)
        fingers.append(S.Fill(S._capsule(fx, y0, fx, y1, r)))
    thumb = [S.Fill(S._capsule(cx - pw / 2 - 90 * s, cy, cx - pw / 2 + 10, cy, 26 * s))]
    return palm + thumb, fingers


def _birth():
    # nal'tel, birth: a small head emerging from the womb's opening, the waters below
    womb = S.arc(C, C - 10, 230, 230, 215, 505)
    child = S.ring(C, C + 50, 66) + S.dot(C - 22, C + 58, 12) + S.dot(C + 22, C + 58, 12)
    water = S.wave(C - 140, C - 150, C + 140, 22, 1.5)
    return [(CONTOUR, R.cushion() + womb), (DETAIL, child + water)]


def _seating():
    # seating, accession: a lord's headband, the jewel at its front, set down on the woven
    # mat of rule; the mat rests on the block's floor and shares it
    y0, y1 = CY0, CY0 + 170
    mat = S.poly([(CX0 + 160, y0), (CX0 + 160, y1), (CX1 - 160, y1), (CX1 - 160, y0)])
    weave = []
    for k in range(1, 4):
        x = CX0 + 160 + k * (CX1 - CX0 - 320) / 4
        weave += S.bar(x, y0, x, y1)
    band = S.arc(C, y1 + 30, 230, 230, 15, 165) + S.arc(C, y1 + 30, 160, 160, 22, 158)
    jewel = S.dot(C, y1 + 225, 34)
    return [(CONTOUR, R.cushion() + mat + band), (DETAIL, weave + jewel)]


def _death():
    # ts'uqel, death: the closed eye and the skull's jaw, the breath leaving as a scroll
    skull = S.arc(C, C + 40, 210, 200, 0, 180) + S.bar(C - 210, C + 40, C + 210, C + 40)
    eye = R.eye(C - 60, C + 120, "closed")
    jaw = []
    for k in range(3):
        x = C - 150 + k * 115
        jaw += S.poly([(x, C + 40), (x, C - 40), (x + 60, C - 40), (x + 60, C + 40)])
    breath = R.curl(C + 110, C + 130, 50, turns=1.0) + R.dotted([(C + 180, C + 200), (C + 240, C + 270)])
    return [(CONTOUR, R.cushion() + skull), (DETAIL, eye + jaw + breath)]


def _burial():
    # burial, going into the earth: a bound bundle laid in the earth's opening, the cenote's
    # water beneath it
    pit = S.arc(C, C + 80, 260, 260, 190, 350)
    bundle = S.frame(C - 150, C - 40, 300, 150, square=2.6) + R.x_mark(C - 70, C + 35, 34) + R.x_mark(C + 70, C + 35, 34)
    water = S.wave(C - 160, CY0 + 100, C + 160, 24, 1.5)
    ground = R.dotted([(CX0 + 70, C + 100), (C - 280, C + 100)]) + R.dotted([(C + 280, C + 100), (CX1 - 70, C + 100)])
    return [(CONTOUR, R.cushion() + pit + bundle), (DETAIL, water + ground)]


def _marriage():
    # ashtsom, marriage: two hands reaching to clasp over a knotted cord
    lp, lf = _hand(C - 110, C - 20, 0.85, up=True)
    rp, rf = _hand(C + 150, C + 150, 0.85, up=False)
    cord = S.bar(CX0 + 70, CY0 + 90, CX1 - 70, CY0 + 90) + S.dot(C, CY0 + 90, 26) + \
        S.bar(C, CY0 + 90, C - 40, CY0 + 30) + S.bar(C, CY0 + 90, C + 40, CY0 + 30)
    return [(CONTOUR, R.cushion() + lp + rp), (DETAIL, lf + rf + cord)]


def _capture():
    # capture: a hand taking a captive by the hair, the lock gathered in its fist
    palm, nails = _hand(C + 30, C + 110, 1.1, up=False)
    lock = S.wave(C - 200, CY0 + 150, C + 220, 22, 1.5) + S.wave(C - 200, CY0 + 90, C + 220, 22, 1.5)
    return [(CONTOUR, R.cushion() + palm), (DETAIL, nails + lock)]


def _war():
    # shok'al, war: a shield behind two crossed spears, its fringe hanging
    shield = S.ring(C, C + 30, 170)
    spears = S.bar(CX0 + 80, CY0 + 50, CX1 - 80, CY1 - 50) + S.bar(CX0 + 80, CY1 - 50, CX1 - 80, CY0 + 50)
    fringe = R.fringe(C - 130, C + 130, C - 140, n=4, h=44)
    return [(CONTOUR, R.cushion() + shield), (DETAIL, spears + fringe)]


def _conquest():
    # conquest: a city's emblem cut through by a falling blade, its stones tumbling
    emblem = S.frame(C - 170, C - 100, 340, 260, square=2.6)
    blade = S.bar(C - 250, CY1 - 80, C + 250, CY0 + 80)
    stones = S.dot(C - 170, CY0 + 70, 22) + S.dot(C - 90, CY0 + 110, 18) + S.dot(C + 120, CY0 + 60, 20)
    return [(CONTOUR, R.cushion() + emblem), (DETAIL, blade + stones)]


def _tribute():
    # tribute: a filled bundle, tied with a knot on top and its count of beads along its foot
    bundle = S.frame(C - 170, CY0 + 70, 340, 300, square=2.4)
    ties = S.bar(C - 170, CY0 + 220, C + 170, CY0 + 220) + S.bar(C, CY0 + 70, C, CY0 + 370)
    knot = S.dot(C, CY0 + 370, 26) + S.bar(C, CY0 + 370, C - 70, CY1 - 50) + S.bar(C, CY0 + 370, C + 70, CY1 - 50)
    count = R.dotted([(C - 130, CY0 + 30), (C + 130, CY0 + 30)])
    return [(CONTOUR, R.cushion() + bundle), (DETAIL, ties + knot + count)]


def _foundation():
    # Kul'qat Tik'il, the laying of a foundation: a hand setting a squared stone on a line
    stone = S.poly([(C - 130, CY0 + 70), (C - 130, CY0 + 200), (C + 130, CY0 + 200), (C + 130, CY0 + 70), (C - 130, CY0 + 70)])
    line = S.bar(CX0 + 60, CY0 + 70, CX1 - 60, CY0 + 70)
    palm, nails = _hand(C + 20, CY1 - 170, 0.95, up=False)
    return [(CONTOUR, R.cushion() + stone + palm), (DETAIL, line + nails + R.x_mark(C, CY0 + 135, 36))]


def _dedication():
    # Kul'qat Ts'apel, dedication: the finished temple, smoke rising from its door
    temple = S.poly([(C - 200, CY0 + 60), (C - 200, CY0 + 260), (C + 200, CY0 + 260), (C + 200, CY0 + 60)])
    roof = S.poly([(C - 230, CY0 + 260), (C, CY0 + 420), (C + 230, CY0 + 260), (C - 230, CY0 + 260)])
    door = S.poly([(C - 60, CY0 + 60), (C - 60, CY0 + 180), (C + 60, CY0 + 180), (C + 60, CY0 + 60)])
    smoke = R.curl(C - 40, CY1 - 70, 46, turns=1.1) + R.curl(C + 60, CY1 - 50, 40, turns=1.1, clockwise=True)
    return [(CONTOUR, R.cushion() + temple + roof), (DETAIL, door + smoke)]


def _offering():
    # an offering of blood: drops falling from a hand into the bowl standing on the floor
    bowl = S.arc(C, CY0 + 150, 210, 150, 200, 340) + S.bar(C - 200, CY0 + 100, C + 200, CY0 + 100)
    palm, nails = _hand(C + 30, CY1 - 160, 0.95, up=False)
    drops = []
    for dx, dy in ((-70, 200), (10, 235), (90, 195)):
        drops += [S.Fill(S._arc(C + dx, CY0 + dy, 18, 18, 0, 360)[:-1])]
    return [(CONTOUR, R.cushion() + bowl + palm), (DETAIL, nails + drops)]


def _eclipse():
    # ts'anish, the eclipse: the sun's disk with a dark crescent biting into it
    sun = S.ring(C, C, 200)
    bite = S.arc(C + 110, C, 170, 170, 100, 260)
    dark = R.net(C - 60, C - 130, 150, 260, n=3)
    rays = R.dotted_arc(C, C, 250, 250, 0, 360)
    return [(CONTOUR, R.cushion() + sun + bite), (DETAIL, dark + rays)]


def _pilgrimage():
    # a pilgrimage: footprints along the dotted road toward a temple's steps
    road = R.dotted([(CX0 + 60, C - 60), (CX1 - 60, C - 60)])
    prints = []
    for k, x in enumerate((CX0 + 140, CX0 + 300, CX0 + 460)):
        y = C + (40 if k % 2 else 120)
        prints += S.frame(x - 40, y - 60, 80, 120, square=2.2)
    steps = S.poly([(CX1 - 60, CY0 + 60), (CX1 - 160, CY0 + 60), (CX1 - 160, CY0 + 140), (CX1 - 240, CY0 + 140)])
    return [(CONTOUR, R.cushion() + prints), (DETAIL, road + steps)]


def _eras_end():
    # the end of an era: the count's stone wrapped in cord and closed, the last day's sun
    # setting behind it
    stone = S.frame(C - 130, CY0 + 60, 260, 360, square=2.6)
    wraps = []
    for k in range(3):
        y = CY0 + 140 + k * 100
        wraps += S.bar(C - 130, y, C + 130, y - 40)
    return [(CONTOUR, R.cushion() + stone), (DETAIL, wraps + R.dotted_arc(C, CY0 + 60, 250, 230, 160, 20))]


def _ball_game():
    # the ball game: the ball rolling toward the court's sloping wall, its stone ring; the
    # wall and the court stand on the block's floor
    ball = S.ring(C - 110, C - 20, 125) + R.curl(C - 110, C - 20, 64, turns=0.9)
    wall = S.poly([(C + 70, CY0), (C + 210, CY0), (C + 210, CY1 - 80), (C + 140, CY1 - 80), (C + 70, CY0)])
    marker = S.ring(C + 172, C + 140, 44)
    return [(CONTOUR, R.cushion() + ball + wall), (DETAIL, marker)]


BIRTH = Glyph("BIRTH", "nal'tel, a birth", "na", _birth)
SEATING = Glyph("SEATING", "a lord seated: accession", "ku", _seating)
DEATH = Glyph("DEATH", "ts'uqel, a death", "tsu", _death)
BURIAL = Glyph("BURIAL", "a burial, going into the earth", "ye", _burial)
MARRIAGE = Glyph("MARRIAGE", "ashtsom, a marriage", "a", _marriage)
CAPTURE = Glyph("CAPTURE", "a captive taken", "bi", _capture)
WAR = Glyph("WAR", "shok'al, a war", "sho", _war)
CONQUEST = Glyph("CONQUEST", "a city overthrown", "hi", _conquest)
TRIBUTE = Glyph("TRIBUTE", "tribute brought", "tu", _tribute)
FOUNDATION = Glyph("FOUNDATION", "Kul'qat Tik'il, a foundation laid", "ku", _foundation)
DEDICATION = Glyph("DEDICATION", "Kul'qat Ts'apel, a dedication", "ku", _dedication)
OFFERING = Glyph("OFFERING", "an offering of blood", "tsu", _offering)
ECLIPSE = Glyph("ECLIPSE", "ts'anish, an eclipse", "tsa", _eclipse)
PILGRIMAGE = Glyph("PILGRIMAGE", "a pilgrimage made", "mi", _pilgrimage)
ERAS_END = Glyph("ERA'S-END", "an era ends", "be", _eras_end)
BALL_GAME = Glyph("BALL-GAME", "the ball game played", "te", _ball_game)

EVENTS = [BIRTH, SEATING, DEATH, BURIAL, MARRIAGE, CAPTURE, WAR, CONQUEST, TRIBUTE, FOUNDATION, DEDICATION,
          OFFERING, ECLIPSE, PILGRIMAGE, ERAS_END, BALL_GAME]
