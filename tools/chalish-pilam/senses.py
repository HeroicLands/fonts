# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Precomposed concepts of the senses, speech and the sacred in the Ch'alish P'ilam
ceremonial hand.

    import senses as V

    parts = V.MEMORY.draw()                  # [(pen, parts), ...]

Where the common hand writes these with two glyphs, the ceremonial hand draws each as one.
The eye and the mouth keep their own drawing: shut in INSIDE's walled square they are kept
back, memory and a secret; standing in OUTSIDE's open wall they go out, observation and
proclamation. SKY's band of stars is the roof that prayer rises to, and the floor that the
unknown lies beyond. CAUTION carries the fangs of the common hand's DANGER, drawn in the
ceremonial canon over LOW's bar and jewel.
"""

from __future__ import annotations

import math

import ceremonial as R
import events as E
import strokes as S
from ceremonial import CONTOUR, DETAIL, CX0, CX1, CY0, CY1, C, Glyph


def _wall(x0, y0, x1, y1, open_side=None):
    """INSIDE's walled square, or OUTSIDE's, open on ``open_side`` (``right`` or ``top``)."""
    if open_side == "right":
        return S.poly([(x1, y0), (x0, y0), (x0, y1), (x1, y1)])
    if open_side == "top":
        return S.poly([(x0, y1), (x0, y0), (x1, y0), (x1, y1)])
    return S.poly([(x0, y0), (x0, y1), (x1, y1), (x1, y0), (x0, y0)])


def _almond(cx, cy, rx, lift):
    """EYE's almond: the two lids meeting at the corners, ``rx`` from the centre, opening
    ``lift`` above and below it."""
    ry = (rx * rx + lift * lift) / (2 * lift)
    a = math.degrees(math.asin(rx / ry))
    return (S.arc(cx, cy - (ry - lift), ry, ry, 90 - a, 90 + a)
            + S.arc(cx, cy + (ry - lift), ry, ry, 270 - a, 270 + a))


def _iris(cx, cy, r):
    return S.ring(cx, cy, r) + S.dot(cx, cy, r * 0.26)


def _sky_band(y_hi, y_lo, x0=CX0 + 50, x1=CX1 - 50, stars=3):
    """SKY's band: two bars with its stars set between them as crossed bars."""
    band = S.bar(x0, y_hi, x1, y_hi) + S.bar(x0, y_lo, x1, y_lo)
    marks = []
    span = (x1 - x0) / stars
    r = min(42.0, (y_hi - y_lo) / 2 - 30)
    for k in range(stars):
        marks += R.x_mark(x0 + span * (k + 0.5), (y_hi + y_lo) / 2, r)
    return band, marks


def _memory():
    # memory: the eye shut in INSIDE's walled square, what it has seen kept within; a row
    # of dots under the eye is the seen thing laid by
    wall = _wall(C - 215, C - 205, C + 215, C + 215)
    lids = _almond(C, C + 50, 180, 105)
    store = R.dotted([(C - 140, C - 120), (C + 140, C - 120)])
    return [(CONTOUR, R.cushion() + wall + lids), (DETAIL, _iris(C, C + 50, 50) + store)]


def _observation():
    # observation: the eye in OUTSIDE's wall, open toward the line's end, its sight going
    # out through the opening as a row of dots to the bead it rests on
    wall = _wall(CX0 + 90, C - 200, C + 110, C + 200, open_side="right")
    lids = _almond(C - 95, C, 165, 100)
    lashes = []
    for dx in (-60, 0, 60):
        lashes += S.tick(C - 95 + dx, C + 100 + 30, 34, angle=90)
    sight = R.dotted([(C + 100, C), (C + 180, C)])
    return [(CONTOUR, R.cushion() + wall + lids),
            (DETAIL, _iris(C - 95, C, 50) + lashes + sight + R.bead(C + 245, C, 50))]


def _lips(cx, cy, w, open_):
    """MOUTH's lips facing the line's start: parted over a row of teeth, or pressed shut."""
    if open_:
        return (S.arc(cx, cy - 150, w, 250, 60, 120) + S.arc(cx, cy + 150, w, 250, 240, 300),
                S.bar(cx - w * 0.45, cy, cx + w * 0.55, cy))
    return (S.arc(cx, cy - 120, w, 190, 58, 122) + S.arc(cx, cy + 160, w, 190, 238, 302), [])


def _secret():
    # a secret: MOUTH's lips pressed shut inside INSIDE's walled square, its scroll of
    # speech wound in on itself, and the dark of the netting below
    wall = _wall(C - 215, C - 205, C + 215, C + 215)
    lips, _ = _lips(C + 30, C + 80, 160, False)
    scroll = R.curl(C - 135, C + 140, 42, turns=1.3, clockwise=True)
    dark = R.net(C - 160, C - 165, 320, 120)
    return [(CONTOUR, R.cushion() + wall + lips), (DETAIL, scroll + dark)]


def _proclamation():
    # proclamation: the open mouth in OUTSIDE's wall, three scrolls of speech going out
    # through the opening
    wall = _wall(CX0 + 90, C - 200, C + 60, C + 200, open_side="right")
    lips, teeth = _lips(C - 110, C, 140, True)
    scrolls = []
    for k, (x, y) in enumerate(((C + 150, C + 150), (C + 210, C), (C + 150, C - 150))):
        scrolls += R.curl(x, y, 44, turns=1.1, clockwise=bool(k % 2))
    lines = S.bar(C + 10, C + 40, C + 130, C + 120) + S.bar(C + 10, C - 40, C + 130, C - 120)
    return [(CONTOUR, R.cushion() + wall + lips), (DETAIL, teeth + scrolls + lines)]


def _the_unknown():
    # the unknown beyond creation: SKY's band of stars as the floor of the picture, and
    # over it OUTSIDE's wall opening upward on a netted dark, the jewel gone out through
    # the opening
    band, stars = _sky_band(CY0 + 230, CY0 + 80)
    wall = _wall(C - 200, CY0 + 290, C + 200, CY1 - 80, open_side="top")
    dark = R.net(C - 140, CY0 + 330, 280, 140)
    out = R.dotted([(C, CY0 + 510), (C, CY1 - 150)]) + S.dot(C, CY1 - 115, 26)
    return [(CONTOUR, R.cushion() + band + wall), (DETAIL, stars + dark + out)]


def _writing():
    # writing, craft: EYE's almond over HAND, fingers raised, and the brush beside the hand
    # with its wet tip down
    lids = _almond(C + 20, C + 155, 185, 100)
    palm, fingers = E._hand(C - 10, CY0 + 130, 0.72, up=True)
    brush = S.bar(C + 250, CY0 + 320, C + 160, CY0 + 80) + S.dot(C + 154, CY0 + 62, 22)
    return [(CONTOUR, R.cushion() + lids + palm),
            (DETAIL, _iris(C + 20, C + 155, 50) + fingers + brush)]


def _prayer():
    # prayer, prophecy: the open mouth below SKY's band of stars, two scrolls of speech
    # rising to it
    band, stars = _sky_band(CY1 - 70, CY1 - 210)
    lips, teeth = _lips(C - 40, CY0 + 190, 160, True)
    scrolls = R.curl(C + 70, C + 20, 52, turns=1.2) + R.curl(C + 200, C - 50, 44, turns=1.1, clockwise=True)
    rise = S.bar(C + 40, CY0 + 200, C + 70, C - 30)
    return [(CONTOUR, R.cushion() + band + lips), (DETAIL, stars + teeth + scrolls + rise)]


def _cenote():
    # a cenote: the ground's line broken by the well's mouth, its walls bellying down to
    # WATER's waves, and below them SOUTH's sun at the nadir between the marks of the dark
    ground = S.bar(CX0 + 70, CY1 - 130, C - 130, CY1 - 130) + S.bar(C + 130, CY1 - 130, CX1 - 70, CY1 - 130)
    walls = [S.Track(S._bezier((C - 130, CY1 - 130), (C - 260, CY1 - 250), (C - 250, C - 120), (C - 110, CY0 + 80))),
             S.Track(S._bezier((C + 130, CY1 - 130), (C + 260, CY1 - 250), (C + 250, C - 120), (C + 110, CY0 + 80)))]
    floor = S.bar(C - 110, CY0 + 80, C + 110, CY0 + 80)
    water = S.wave(C - 160, C + 120, C + 160, 22, 1.5) + S.wave(C - 165, C + 30, C + 165, 22, 1.5)
    nadir = S.ring(C, CY0 + 170, 48) + S.dot(C, CY0 + 170, 16)
    dark = R.x_mark(C - 125, CY0 + 175, 28) + R.x_mark(C + 125, CY0 + 175, 28)
    return [(CONTOUR, R.cushion() + ground + walls + floor), (DETAIL, water + nadir + dark)]


def _caution():
    # caution: DANGER's row of fangs over LOW's bar, the jewel of the lesser beneath it;
    # the fangs hang from a jaw line, each solid, a groove apart
    jaw = S.bar(CX0 + 70, CY1 - 110, CX1 - 70, CY1 - 110)
    fangs = []
    n = 5
    x0, x1 = CX0 + 90, CX1 - 90
    w = (x1 - x0) / n
    for k in range(n):
        x = x0 + w * (k + 0.5)
        fangs.append(S.Fill([(x - w * 0.3, CY1 - 125), (x, CY1 - 265), (x + w * 0.3, CY1 - 125)]))
    bar = S.bar(CX0 + 60, C - 10, CX1 - 60, C - 10)
    warn = R.dotted([(C - 200, C + 60), (C + 200, C + 60)])
    return [(CONTOUR, R.cushion() + jaw + bar), (DETAIL, fangs + warn + R.bead(C, C - 170, 70))]


MEMORY = Glyph("MEMORY", "memory: EYE and INSIDE made one", "i", _memory)
OBSERVATION = Glyph("OBSERVATION", "observation: EYE and OUTSIDE made one", "tsa", _observation)
SECRET = Glyph("SECRET", "a secret: MOUTH and INSIDE made one", "ka", _secret)
PROCLAMATION = Glyph("PROCLAMATION", "proclamation: MOUTH and OUTSIDE made one", "na", _proclamation)
THE_UNKNOWN = Glyph("THE-UNKNOWN", "the unknown beyond creation: SKY and OUTSIDE made one", "hu", _the_unknown)
WRITING = Glyph("WRITING", "writing, craft: HAND and EYE made one", "pi", _writing)
PRAYER = Glyph("PRAYER", "prayer, prophecy: MOUTH and SKY made one", "na", _prayer)
CENOTE = Glyph("CENOTE", "a cenote, the sacred well: WATER and SOUTH made one", "ne", _cenote)
CAUTION = Glyph("CAUTION", "caution: DANGER and LOW made one", "sho", _caution)

SENSES = [MEMORY, OBSERVATION, SECRET, PROCLAMATION, THE_UNKNOWN, WRITING, PRAYER, CENOTE, CAUTION]
