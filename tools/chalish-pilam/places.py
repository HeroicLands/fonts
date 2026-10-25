# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""The city-states of the Ki'ich'chik in the Ch'alish P'ilam ceremonial hand.

    import places as P

    parts = P.ISHILANKUL.draw()              # [(pen, parts), ...]

Each city-state names itself on its monuments by an **emblem**: the city's own picture,
taken from its name, with the mark of a sovereign seat, a beaded prefix grown from the
sign's leading edge. Every emblem reads at once as a city of rank, and its picture says
which. Shelem Ish'bal, the Land of the Dead Jaguar, has no ruler, and its glyph carries
no seat.
"""

from __future__ import annotations

import ceremonial as R
import strokes as S
from ceremonial import CONTOUR, DETAIL, CX1, CY0, CY1, C, Glyph

BOX = (165.0, CY0, CX1, CY1)  # the main sign of an emblem, leaving room for the seat
MX = (BOX[0] + BOX[2]) / 2


def _seat():
    """The mark of a sovereign seat: a beaded prefix on the emblem's leading edge."""
    return R.prefix_on(BOX, 120, n=3, kind="beads")


def _mat(y):
    """The woven mat of rule, under a city's picture: a seat (kul)."""
    out = S.poly([(MX - 140, y), (MX - 140, y + 90), (MX + 140, y + 90), (MX + 140, y), (MX - 140, y)])
    for k in (1, 2, 3):
        x = MX - 140 + k * 70
        out += S.bar(x, y, x, y + 90)
    return out


def _star(cx, cy, r):
    return S.poly([(cx, cy + r), (cx + r * 0.3, cy + r * 0.3), (cx + r, cy), (cx + r * 0.3, cy - r * 0.3), (cx, cy - r),
                   (cx - r * 0.3, cy - r * 0.3), (cx - r, cy), (cx - r * 0.3, cy + r * 0.3), (cx, cy + r)])


def _ishilankul():
    # the Seat of the Stars: a great star over the mat of rule
    return [(CONTOUR, R.cushion(*BOX) + _seat()),
            (DETAIL, _star(MX, C + 90, 130) + S.dot(MX, C + 90, 22) + _mat(CY0 + 85))]


def _kankul():
    # the golden seat, the realm of knowledge: a golden flower over the mat, a count in
    # bar and dot beside it
    flower = S.dot(MX - 60, C + 80, 26)
    for dx, dy in ((0, 1), (0.87, 0.5), (0.87, -0.5), (0, -1), (-0.87, -0.5), (-0.87, 0.5)):
        flower += S.dot(MX - 60 + 70 * dx, C + 80 + 70 * dy, 22)
    count = S.bar(MX + 110, C + 20, MX + 110, C + 170) + S.dot(MX + 170, C + 50, 18) + S.dot(MX + 170, C + 140, 18)
    return [(CONTOUR, R.cushion(*BOX) + _seat()), (DETAIL, flower + count + _mat(CY0 + 85))]


def _neok_baate():
    # Ne'ok Ba'ate, between north and south: water flowing through a threshold
    door = S.arc(MX, C + 40, 150, 150, 0, 180) + S.bar(MX - 150, C + 40, MX - 150, CY0 + 30) + \
        S.bar(MX + 150, C + 40, MX + 150, CY0 + 30)
    water = S.wave(MX - 110, CY0 + 130, MX + 110, 22, 1.5) + S.wave(MX - 110, CY0 + 230, MX + 110, 22, 1.5)
    return [(CONTOUR, R.cushion(*BOX) + _seat() + door), (DETAIL, water + R.curl(MX, C + 70, 44, turns=0.9))]


def _shelem():
    # Shelem, the bird, the land of luxuries: a bird with a long plume
    wings = S.arc(MX - 110, C, 110, 120, 20, 160) + S.arc(MX + 110, C, 110, 120, 20, 160)
    plume = S.arc(MX + 160, CY0 + 60, 260, 200, 90, 180)
    body = S.dot(MX, C + 40, 28)
    return [(CONTOUR, R.cushion(*BOX) + _seat()), (DETAIL, wings + plume + body + R.dotted([(MX - 180, CY0 + 50), (MX + 40, CY0 + 50)]))]


def _ishbal_tsaku():
    # Ish'bal Tsa'ku, the Jaguar's House: jaguar spots under a roof
    roof = S.poly([(BOX[0] + 50, C + 60), (MX, CY1 - 50), (BOX[2] - 50, C + 60), (BOX[0] + 50, C + 60)])
    spots = []
    for x, y in ((MX - 120, C - 60), (MX + 120, C - 60), (MX, CY0 + 120)):
        spots += S.ring(x, y, 52) + S.dot(x, y, 14)
    return [(CONTOUR, R.cushion(*BOX) + _seat() + roof), (DETAIL, spots)]


def _kushi_ishbal():
    # K'ushi Ish'bal, the far south: the jaguar's paw, its pad and three toes
    pad = S.frame(MX - 120, CY0 + 70, 240, 200, square=2.2)
    toes = S.ring(MX - 110, C + 110, 50) + S.ring(MX, C + 150, 50) + S.ring(MX + 110, C + 110, 50)
    return [(CONTOUR, R.cushion(*BOX) + _seat() + pad), (DETAIL, toes + S.dot(MX, CY0 + 170, 30))]


def _qaptel_tsakul():
    # Q'aptel Tsa'kul, the border, given to the storm and to death: the border's line with
    # lightning striking across it
    border = S.bar(BOX[0] + 40, C - 30, BOX[2] - 40, C - 30)
    for k in range(4):
        x = BOX[0] + 90 + k * 110
        border += S.bar(x, C - 30, x, C - 120)
    bolt = S.poly([(MX - 60, CY1 - 60), (MX + 40, C + 60), (MX - 30, C + 60), (MX + 60, C - 10)])
    return [(CONTOUR, R.cushion(*BOX) + _seat()), (DETAIL, border + bolt + R.net(MX - 130, CY0 + 50, 260, 90, n=3))]


def _shelem_ishbal():
    # Shelem Ish'bal, the Land of the Dead Jaguar, which no one rules: the jaguar's empty
    # skull over ash, and no seat
    skull = S.arc(C, C + 30, 230, 200, 0, 180) + S.bar(C - 230, C + 30, C + 230, C + 30)
    eye = S.ring(C - 70, C + 115, 40)
    teeth = []
    for k in range(3):
        x = C - 150 + k * 105
        teeth += S.poly([(x, C + 30), (x, C - 40), (x + 50, C - 40), (x + 50, C + 30)])
    ash = R.dotted([(C - 190, CY0 + 140), (C + 190, CY0 + 140)])
    return [(CONTOUR, R.cushion() + skull), (DETAIL, eye + teeth + ash)]


ISHILANKUL = Glyph("ISHILANKUL", "Ish'ilankul, the Seat of the Stars", "i", _ishilankul)
KANKUL = Glyph("KANKUL", "K'ankul, the golden seat", "ka", _kankul)
NEOK_BAATE = Glyph("NEOK-BAATE", "Ne'ok Ba'ate, between north and south", "ne", _neok_baate)
SHELEM = Glyph("SHELEM", "Shelem, the land of the bird", "she", _shelem)
ISHBAL_TSAKU = Glyph("ISHBAL-TSAKU", "Ish'bal Tsa'ku, the Jaguar's House", "i", _ishbal_tsaku)
KUSHI_ISHBAL = Glyph("KUSHI-ISHBAL", "K'ushi Ish'bal, the far south", "ku", _kushi_ishbal)
QAPTEL_TSAKUL = Glyph("QAPTEL-TSAKUL", "Q'aptel Tsa'kul, the border", "qa", _qaptel_tsakul)
SHELEM_ISHBAL = Glyph("SHELEM-ISHBAL", "Shelem Ish'bal, the Land of the Dead Jaguar, unruled", "she", _shelem_ishbal)

PLACES = [ISHILANKUL, KANKUL, NEOK_BAATE, SHELEM, ISHBAL_TSAKU, KUSHI_ISHBAL, QAPTEL_TSAKUL, SHELEM_ISHBAL]
