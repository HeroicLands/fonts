# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""The cosmos and the counts in the Ch'alish P'ilam ceremonial hand.

    import cosmos as K

    parts = K.UNDERWORLD.draw()              # [(pen, parts), ...]

The realms above and below, the age of the world, the Living Flame that renews it, and
the four counts of days that the priests keep. The counts are day signs, so they stand in
the round cartouche; the realms are drawn in the cushion.
"""

from __future__ import annotations

import math

import ceremonial as R
import strokes as S
from ceremonial import CONTOUR, DETAIL, CX0, CX1, CY0, CY1, C, Glyph


def _underworld():
    # Ch'al Ts'umaq, beneath every cenote: the mouth of the earth opening downward, its
    # jaws toothed, the waters of the cenote at its lip and the dark below
    jaw = S.arc(C, CY1 - 60, 250, 300, 200, 340)
    teeth = []
    for k in range(4):
        x = C - 150 + k * 100
        teeth += S.poly([(x - 26, CY1 - 160), (x, CY1 - 240), (x + 26, CY1 - 160)])
    water = S.wave(C - 200, CY1 - 110, C + 200, 22, 1.5)
    dark = R.net(C - 140, CY0 + 70, 280, 170)
    return [(CONTOUR, R.cushion() + jaw), (DETAIL, teeth + water + dark)]


def _heaven():
    # the sacred realm above: the sky's vault enclosing the sun and two stars
    vault = S.arc(C, CY0 + 80, 260, 420, 0, 180) + S.bar(CX0 + 60, CY0 + 80, CX1 - 60, CY0 + 80)
    sun = S.ring(C, C + 40, 70) + S.dot(C, C + 40, 22)
    stars = []
    for x, y in ((C - 160, C - 60), (C + 160, C - 60)):
        stars += S.poly([(x, y + 48), (x + 14, y + 14), (x + 48, y), (x + 14, y - 14), (x, y - 48),
                         (x - 14, y - 14), (x - 48, y), (x - 14, y + 14), (x, y + 48)])
    return [(CONTOUR, R.cushion() + vault), (DETAIL, sun + stars + R.dotted([(C - 200, CY0 + 120), (C + 200, CY0 + 120)]))]


def _fifth_age():
    # the Fifth Age: the four ages past as four bars, the fifth as the living disk at
    # their head
    bars = []
    for k in range(4):
        y = CY0 + 105 + k * 78
        bars.append(S.Fill(S._capsule(C - 190, y, C + 190, y, 17)))
    disk = S.ring(C, CY1 - 165, 82) + S.dot(C, CY1 - 165, 26)
    return [(CONTOUR, R.cushion() + disk), (DETAIL, bars)]


def _living_flame():
    # K'ayik Kul'al, the new fire every fifty-two years: the fire drill set in its board,
    # the new flame rising beside it; the board rests on the block's floor
    board = S.poly([(C - 250, CY0), (C - 250, CY0 + 110), (C + 250, CY0 + 110), (C + 250, CY0)])
    drill = S.bar(C + 120, CY0 + 110, C + 220, CY1 - 70)
    flame = [S.Track(S._bezier((C - 180, CY0 + 120), (C - 300, C + 60), (C - 120, C + 120), (C - 60, CY1 - 90))
                     + S._bezier((C - 60, CY1 - 90), (C + 20, C + 100), (C + 80, C), (C + 20, CY0 + 120))[1:])]
    tongue = R.curl(C - 90, C, 52, turns=0.9)
    return [(CONTOUR, R.cushion() + board + flame), (DETAIL, drill + tongue)]


def _count(inner):
    def draw():
        return [(CONTOUR, R.cartouche()), (DETAIL, inner())]
    return draw


def _solar_count():
    # the Ts'en, 365 days: the sun's disk over the eighteen months' fringe
    sun = S.ring(C, C + 40, 120) + S.dot(C, C + 40, 30)
    rays = []
    for k in range(8):
        a = math.radians(k * 45)
        rays += S.bar(C + 150 * math.cos(a), C + 40 + 150 * math.sin(a), C + 190 * math.cos(a), C + 40 + 190 * math.sin(a))
    return sun + rays + R.fringe(C - 150, C + 150, C - 160, h=46)


def _lunar_count():
    # the Ts'uqal: the crescent and the dots of its nights
    moon = S.arc(C - 20, C, 170, 170, 70, 290) + S.arc(C + 50, C, 120, 125, 85, 275)
    nights = R.dotted([(C + 120, C - 170), (C + 120, C + 170)])
    return moon + nights


def _stellar_count():
    # the Ish'ilan: a great star with the small stars of its course in a ring about it
    star = S.poly([(C, C + 150), (C + 40, C + 40), (C + 150, C), (C + 40, C - 40), (C, C - 150),
                   (C - 40, C - 40), (C - 150, C), (C - 40, C + 40), (C, C + 150)])
    course = R.dotted_arc(C, C, 220, 220, 0, 360)
    return star + course


UNDERWORLD = Glyph("UNDERWORLD", "Ch'al Ts'umaq, the world below", "cha", _underworld)
HEAVEN = Glyph("HEAVEN", "the sacred realm above", "hu", _heaven)
FIFTH_AGE = Glyph("FIFTH-AGE", "the Fifth Age, the present age of the world", "la", _fifth_age)
LIVING_FLAME = Glyph("LIVING-FLAME", "K'ayik Kul'al, the new fire of fifty-two years", "ka", _living_flame)
SOLAR_COUNT = Glyph("SOLAR-COUNT", "the Ts'en, the count of 365 days", "tse", _count(_solar_count))
LUNAR_COUNT = Glyph("LUNAR-COUNT", "the Ts'uqal, the lunar count", "tsu", _count(_lunar_count))
STELLAR_COUNT = Glyph("STELLAR-COUNT", "the Ish'ilan, the stellar count", "i", _count(_stellar_count))

# The 260-day count is the pilot's TQ'AN, in ceremonial.py.
COSMOS = [UNDERWORLD, HEAVEN, FIFTH_AGE, LIVING_FLAME, SOLAR_COUNT, LUNAR_COUNT, STELLAR_COUNT]
