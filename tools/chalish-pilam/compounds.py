# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Precomposed concepts of the Ch'alish P'ilam ceremonial hand.

    import compounds as X

    parts = X.MATRIARCH.draw()               # [(pen, parts), ...]

Where the common hand writes a concept with two or three glyphs, the ceremonial hand draws
it as one, built from the same components reshaped to work as a single picture. The house
compounds take PATRIARCH's form: the house's roof is the block's crown and the people of
the house stand under it. The life compounds set a head against the sun at the horizon:
rising for a birth, sinking for a death.
"""

from __future__ import annotations

import math

import ceremonial as R
import strokes as S
from ceremonial import CONTOUR, DETAIL, CX0, CX1, CY0, CY1, C, Glyph


def _housed(heads, ridge_mark=None):
    """The house's roof as the block's crown, with ``heads`` under it: a list of
    (x0, y0, x1, y1, woman, young) boxes. ``ridge_mark`` sets the HIGH bead at the ridge
    (True) or the LOW bead under the eaves (False)."""
    x0, y0, x1, y1 = CX0, CY0, CX1, CY1 - 20
    outline, (le, re) = R.roofed(x0, y0, x1, y1, ridge=y1 + 40)
    eaves = S.bar(le[0] + 10, le[1], re[0] - 10, re[1])
    contour, detail = outline + eaves, []
    for hx0, hy0, hx1, hy1, woman, young in heads:
        c, d = R.head(hx0, hy0, hx1, hy1, band=False, spool=not woman and not young)
        contour += c
        detail += d
        if woman:
            detail += R.dotted([(hx1 + 26, hy1 - 40), (hx1 + 26, hy0 + 40)], r=14)
    if ridge_mark is True:
        detail += S.dot(C, y1 - 30, 24)
    elif ridge_mark is False:
        detail += S.dot(C, le[1] - 50, 22)
    return [(CONTOUR, contour), (DETAIL, detail)]


def _matriarch():
    # the matriarch: WOMAN, HIGH and HOUSE made one
    return _housed([(150, CY0, CX1 - 160, 440, True, False)], ridge_mark=True)


def _son():
    # a son: a young head under the house's roof, the LOW bead under the eaves
    return _housed([(190, CY0, CX1 - 140, 370, False, True)], ridge_mark=False)


def _daughter():
    return _housed([(190, CY0, CX1 - 190, 370, True, True)], ridge_mark=False)


def _family():
    # the family: a man and a woman under one roof, side by side
    return _housed([(105, CY0, 330, 330, False, False), (395, CY0, 590, 310, True, False)])


def _life(rising, woman):
    def draw():
        # the birth or death of a person: the head with its eye open over the rising sun, or
        # closed over the sinking one
        hx0, hy0, hx1, hy1 = (170, C, CX1 - (150 if woman else 80), CY1 - 80)
        contour, detail = R.head(hx0, hy0, hx1, hy1, eye_kind="open" if rising else "closed", band=False, spool=False)
        y = CY0 + 150
        if rising:
            sun = S.arc(C, y, 140, 140, 0, 180) + S.bar(CX0 + 60, y, CX1 - 60, y)
            light = [t for a in (25, 155) for t in S.bar(C + 170 * math.cos(math.radians(a)), y + 170 * math.sin(math.radians(a)),
                                                          C + 220 * math.cos(math.radians(a)), y + 220 * math.sin(math.radians(a)))]
        else:
            sun = S.arc(C, y, 140, 140, 180, 360) + S.bar(CX0 + 60, y, CX1 - 60, y)
            light = R.dotted([(C - 210, y + 40), (C + 210, y + 40)])
        if woman:
            detail += R.dotted([(hx1 + 28, hy1 - 50), (hx1 + 28, hy0 + 30)], r=14)
        return [(CONTOUR, R.cushion() + contour + sun), (DETAIL, detail + light)]
    return draw


def _household(founded):
    def draw():
        # a household founded or ended: the house with the sun rising or setting before it
        x0, y0, x1, y1 = CX0, CY0, CX1, CY1 - 20
        outline, (le, re) = R.roofed(x0, y0, x1, y1, ridge=y1 + 40)
        door = S.arc(C, CY0 + 150, 75, 75, 0, 180) + S.bar(C - 75, CY0 + 150, C - 75, CY0 + 50) + S.bar(C + 75, CY0 + 150, C + 75, CY0 + 50)
        y = le[1] - 90 if founded else le[1] - 70
        if founded:
            sun = S.arc(C, y, 70, 70, 0, 180) + S.bar(C - 140, y, C + 140, y)
        else:
            sun = S.arc(C, y, 70, 70, 180, 360) + S.bar(C - 140, y, C + 140, y)
        return [(CONTOUR, outline + S.bar(le[0] + 10, le[1], re[0] - 10, re[1])), (DETAIL, door + sun)]
    return draw


MATRIARCH = Glyph("MATRIARCH", "the matriarch: WOMAN, HIGH and HOUSE made one", "che", _matriarch)
SON = Glyph("SON", "a son: MAN, LOW and HOUSE made one", "che", _son)
DAUGHTER = Glyph("DAUGHTER", "a daughter: WOMAN, LOW and HOUSE made one", "che", _daughter)
FAMILY = Glyph("FAMILY", "a family: MAN, WOMAN and HOUSE made one", "che", _family)
BIRTH_OF_A_BOY = Glyph("BIRTH-OF-A-BOY", "the birth of a boy: MAN and EAST made one", "che", _life(True, False))
BIRTH_OF_A_GIRL = Glyph("BIRTH-OF-A-GIRL", "the birth of a girl: WOMAN and EAST made one", "che", _life(True, True))
DEATH_OF_A_MAN = Glyph("DEATH-OF-A-MAN", "the death of a man: MAN and WEST made one", "che", _life(False, False))
DEATH_OF_A_WOMAN = Glyph("DEATH-OF-A-WOMAN", "the death of a woman: WOMAN and WEST made one", "che", _life(False, True))
HOUSEHOLD_FOUNDED = Glyph("HOUSEHOLD-FOUNDED", "a household founded: HOUSE and EAST made one", "shu", _household(True))
HOUSEHOLD_ENDED = Glyph("HOUSEHOLD-ENDED", "a household ended: HOUSE and WEST made one", "shu", _household(False))

COMPOUNDS = [MATRIARCH, SON, DAUGHTER, FAMILY, BIRTH_OF_A_BOY, BIRTH_OF_A_GIRL, DEATH_OF_A_MAN, DEATH_OF_A_WOMAN,
             HOUSEHOLD_FOUNDED, HOUSEHOLD_ENDED]
