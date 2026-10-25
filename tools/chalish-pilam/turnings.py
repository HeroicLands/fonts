# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""The turnings of time in the Ch'alish P'ilam ceremonial hand.

    import turnings as W

    parts = W.DAWN.draw()                    # [(pen, parts), ...]

The sun's day, the plant's year, a life and an era, each drawn as one glyph from the
quarters and the things they turn. EAST and WEST are time, rising and setting; NORTH is
the zenith and SOUTH the nadir, so EAST, NORTH, WEST and SOUTH in order are the whole
round. The sun of these glyphs is SUN's own face, its spiral and ring of light, set
against the horizon of the quarters; the line's start is the east.
"""

from __future__ import annotations

import math

import ceremonial as R
import strokes as S
from ceremonial import CONTOUR, DETAIL, CX0, CX1, CY0, CY1, C, Glyph


def _face(cx, cy, r):
    """SUN's face: its disk, a ring of light dots inside it and the spiral at its heart.
    Returns (contour, detail)."""
    detail = R.curl(cx, cy, r * 0.42, turns=1.4)
    if r >= 110:
        detail += R.dotted_arc(cx, cy, r * 0.7, r * 0.7, 0, 360)
    return S.ring(cx, cy, r), detail


def _rays(cx, cy, r, a0, a1, n, curl=True):
    """Light about a disk between angles ``a0`` and ``a1``: curls, or short bars."""
    out = []
    for k in range(n):
        t = math.radians(a0 + (a1 - a0) * k / max(n - 1, 1))
        if curl:
            out += R.curl(cx + (r + 50) * math.cos(t), cy + (r + 50) * math.sin(t), 24, turns=1.0)
        else:
            out += S.bar(cx + (r + 34) * math.cos(t), cy + (r + 34) * math.sin(t),
                         cx + (r + 84) * math.cos(t), cy + (r + 84) * math.sin(t))
    return out


def _dawn():
    # dawn: SUN's whole face lifted clear of the horizon, its light spreading along the
    # world's edge to either side, and below the line the earth's comb fringe
    y = C - 70
    face, inner = _face(C, y + 165, 150)
    spread = []
    for s in (-1, 1):
        spread += S.bar(C + s * 180, y + 75, C + s * 290, y + 75) + S.bar(C + s * 170, y + 135, C + s * 260, y + 175)
    return [(CONTOUR, R.cushion() + face + S.bar(CX0 + 50, y, CX1 - 50, y)),
            (DETAIL, inner + spread + _rays(C, y + 165, 150, 60, 120, 3) + R.fringe(C - 200, C + 200, y - 80, h=40))]


def _sunset():
    # sunset: SUN's face half sunk under the horizon, the part below the line traced only
    # in dots, its last light falling under it
    y = C + 60
    upper = S.arc(C, y, 170, 170, 0, 180)
    lower = R.dotted_arc(C, y, 170, 170, 196, 344, r=13)
    heart = R.curl(C, y + 70, 56, turns=1.3) + R.dotted_arc(C, y, 115, 115, 20, 160)
    fall = []
    for dx in (-150, -50, 50, 150):
        fall += S.bar(C + dx, y - 205, C + dx * 1.15, y - 290)
    return [(CONTOUR, R.cushion() + upper + S.bar(CX0 + 50, y, CX1 - 50, y)), (DETAIL, lower + heart + fall)]


def _noon():
    # noon: SUN's face at the top of the sky, its light falling straight down to the earth
    # in three shafts, the ground's line and its fringe under them
    cy = CY1 - 175
    face, inner = _face(C, cy, 115)
    shafts = []
    for dx in (-110, 0, 110):
        shafts += R.dotted([(C + dx, cy - 150), (C + dx, CY0 + 150)], r=13)
    ground = S.bar(CX0 + 60, CY0 + 115, CX1 - 60, CY0 + 115)
    return [(CONTOUR, R.cushion() + face + ground),
            (DETAIL, inner + _rays(C, cy, 115, 0, 180, 5) + shafts + R.fringe(C - 180, C + 180, CY0 + 115, h=34))]


def _star(x, y, r):
    """HEAVEN's four-pointed star."""
    k = r * 0.3
    return S.poly([(x, y + r), (x + k, y + k), (x + r, y), (x + k, y - k), (x, y - r), (x - k, y - k), (x - r, y),
                   (x - k, y + k), (x, y + r)])


def _midnight():
    # midnight: the sun asleep at the foot of the world, its eye closed, the dark's two
    # marks to either side; over the earth's line the night sky and its stars
    y = C + 90
    cy = CY0 + 170
    disk = S.ring(C, cy, 100)
    eye = R.eye(C, cy - 20, "closed")
    dark = R.x_mark(C - 200, cy, 44) + R.x_mark(C + 200, cy, 44)
    stars = []
    for x, yy in ((C - 170, y + 110), (C, y + 160), (C + 170, y + 110)):
        stars += _star(x, yy, 44)
    return [(CONTOUR, R.cushion() + disk + S.bar(CX0 + 50, y, CX1 - 50, y)), (DETAIL, eye + dark + stars)]


def _germination():
    # germination: the seed under the earth's line, its shoot rising through it and
    # unfurling, the rising sun's light fanned round the curl at its tip
    y = C - 60
    seed = [S.Track(S._arc(C, CY0 + 125, 75, 48, 0, 360), closed=True)] + S.dot(C, CY0 + 125, 16)
    shoot = S.bar(C, CY0 + 173, C, CY1 - 250)
    tip = R.curl(C + 50, CY1 - 200, 55, turns=1.2)
    leaves = S.arc(C - 110, y + 60, 110, 90, 0, 100) + S.arc(C + 110, y + 130, 110, 90, 80, 180)
    light = _rays(C + 50, CY1 - 200, 30, 0, 180, 5, curl=False)
    return [(CONTOUR, R.cushion() + S.bar(CX0 + 50, y, CX1 - 50, y) + shoot + seed), (DETAIL, tip + leaves + light)]


def _harvest():
    # harvest, withering: the stalk bowed over, its full head hanging, its leaves fallen;
    # under the earth's line the sun sinking
    y = CY0 + 200
    stalk = [S.Track(S._bezier((C - 130, y), (C - 130, CY1 - 60), (C + 110, CY1 - 50), (C + 170, C + 130)))]
    head = []
    for k in range(4):
        head += S.dot(C + 170 + (16 if k % 2 else -16), C + 80 - k * 50, 19)
    leaves = S.arc(C - 210, C - 10, 80, 100, 290, 360) + S.arc(C - 50, C - 30, 80, 100, 180, 250)
    sun = S.arc(C, y, 95, 95, 180, 360)
    fall = S.bar(C - 150, y - 40, C - 175, y - 95) + S.bar(C + 150, y - 40, C + 175, y - 95)
    return [(CONTOUR, R.cushion() + stalk + S.bar(CX0 + 50, y, CX1 - 50, y)),
            (DETAIL, head + leaves + sun + fall)]


def _seed_sown():
    # a seed sown: the furrows over the earth's line, the seed's road down into the earth
    # traced in dots, and the seed itself at the world's foot between the two marks of the
    # dark
    y = C + 110
    furrows = []
    for k in range(3):
        furrows += S.arc(C - 180 + k * 180, y + 130, 70, 60, 200, 340)
    road = R.dotted([(C, y - 40), (C, CY0 + 230)], r=13)
    seed = [S.Track(S._arc(C, CY0 + 140, 62, 82, 0, 360), closed=True)] + S.dot(C, CY0 + 140, 18)
    marks = R.x_mark(C - 185, CY0 + 140, 44) + R.x_mark(C + 185, CY0 + 140, 44)
    return [(CONTOUR, R.cushion() + S.bar(CX0 + 50, y, CX1 - 50, y) + seed), (DETAIL, furrows + road + marks)]


def _course(over):
    def draw():
        # a lifetime: the sun's course over the earth, rising at the line's start and
        # sinking at its end; rebirth: its course under the earth, from its setting at the
        # line's start to its rising at the end
        y = C - 40 if over else C + 70
        line = S.bar(CX0 + 50, y, CX1 - 50, y)
        a, b = CX0 + 150, CX1 - 150
        if over:
            first = S.arc(a, y, 90, 90, 0, 180)
            last = S.arc(b, y, 90, 90, 180, 360)
            road = R.dotted_arc(C, y + 30, 230, 250, 12, 168, r=13)
            more = _rays(a, y, 90, 30, 150, 3, curl=False) + S.dot(a, y + 40, 20)
            more += R.fringe(C - 110, C + 90, y - 60, n=3, h=40)
        else:
            first = S.arc(a, y, 90, 90, 180, 360)
            last = S.arc(b, y, 90, 90, 0, 180)
            road = R.dotted_arc(C, y - 40, 215, 230, 195, 345, r=13)
            more = _rays(b, y, 90, 30, 150, 3, curl=False) + S.dot(b, y + 40, 20)
            more += R.curl(C, y - 150, 60, turns=1.2)
            more += R.dotted([(C - 170, y + 170), (C + 90, y + 170)])
        return [(CONTOUR, R.cushion() + line + first + last), (DETAIL, road + more)]
    return draw


def _era_begins():
    # an era begins: the count's stone stands new, unbound, on the earth's line; the sun
    # rises from its crown and HIGH's jewel is raised over it
    y = CY0 + 100
    stone = S.frame(C - 115, y, 230, 250, square=2.6)
    top = y + 250
    sun = S.arc(C, top, 130, 130, 0, 180)
    light = _rays(C, top, 130, 20, 160, 5, curl=False)
    jewel = S.dot(C, top + 64, 24)
    face = R.x_mark(C, y + 135, 50)
    return [(CONTOUR, R.cushion() + stone + sun + S.bar(CX0 + 60, y, CX1 - 60, y)),
            (DETAIL, light + jewel + face + R.dotted([(C - 210, y - 55), (C + 210, y - 55)]))]


def _stairs(x0, y0, x1, y1, n):
    """A stair of ``n`` steps from (x0, y0) to (x1, y1), treads first."""
    pts = [(x0, y0)]
    for k in range(n):
        xa = x0 + (x1 - x0) * (k + 1) / n
        yb = y0 + (y1 - y0) * (k + 1) / n
        pts += [(xa, pts[-1][1]), (xa, yb)]
    return S.poly(pts)


def _passage():
    # the passage of the dead: the sun gone under the earth's line at the line's start,
    # the stair from it going down into the world below, the dead's road in dots on its
    # treads, the dark's two marks at its foot
    y = CY1 - 190
    sun = S.arc(CX0 + 150, y, 85, 85, 180, 360)
    stair = _stairs(CX0 + 235, y - 20, CX1 - 90, CY0 + 90, 4)
    road = []
    for k in range(4):
        x = CX0 + 235 + (CX1 - 90 - CX0 - 235) * (k + 0.5) / 4
        yy = y - 20 + (CY0 + 90 - y + 20) * k / 4
        road += S.dot(x, yy + 34, 14)
    marks = R.x_mark(CX0 + 150, CY0 + 160, 44) + R.x_mark(CX0 + 290, CY0 + 110, 36)
    fall = R.dotted([(CX0 + 150, y - 125), (CX0 + 150, C)], r=12)
    return [(CONTOUR, R.cushion() + sun + S.bar(CX0 + 50, y, CX1 - 50, y)), (DETAIL, stair + road + marks + fall)]


def _out_of_the_trials():
    # coming out of the trials: the stair climbing from the netted dark at the world's
    # foot, at the line's start, up through the earth's line to the sun rising at its end
    y = C + 80
    stair = _stairs(CX0 + 230, CY0 + 90, CX1 - 230, y, 3)
    dark = R.net(CX0 + 70, CY0 + 60, 140, 170, n=3)
    sun = S.arc(CX1 - 150, y, 85, 85, 0, 180)
    light = _rays(CX1 - 150, y, 85, 30, 150, 3, curl=False)
    sky = R.dotted([(CX0 + 110, CY1 - 110), (C + 40, CY1 - 110)])
    return [(CONTOUR, R.cushion() + sun + S.bar(CX0 + 50, y, CX1 - 50, y)),
            (DETAIL, stair + dark + light + sky + S.dot(CX1 - 150, y + 40, 18))]


def _whole_round():
    # the whole round: the sun's road in dots, a great ring, and the sun at each quarter:
    # rising at the line's start, at the zenith over it, sinking at its end and asleep at
    # the nadir between the dark's marks; the round's own heart, SUN's spiral, at the middle
    cx, cy, r = C, C - 5, 205
    road = R.dotted_arc(cx, cy, r, r - 15, 0, 360, r=12, step=58)
    east = S.arc(cx - r, cy, 58, 58, 0, 180) + S.bar(cx - r - 70, cy, cx - r + 70, cy)
    west = S.arc(cx + r, cy, 58, 58, 180, 360) + S.bar(cx + r - 70, cy, cx + r + 70, cy)
    north = S.ring(cx, cy + r - 15, 52)
    south = S.ring(cx, cy - r + 15, 52)
    marks = R.x_mark(cx - 110, cy - r + 10, 28) + R.x_mark(cx + 110, cy - r + 10, 28)
    halo = _rays(cx, cy + r - 15, 52, 20, 160, 3, curl=False)
    heart = R.curl(cx, cy, 72, turns=1.4)
    return [(CONTOUR, R.cushion() + east + west + north + south),
            (DETAIL, road + marks + halo + heart + S.dot(cx, cy - r + 15, 16) + S.dot(cx - r, cy + 28, 16))]


DAWN = Glyph("DAWN", "dawn: SUN and EAST made one", "tse", _dawn)
SUNSET = Glyph("SUNSET", "sunset: SUN and WEST made one", "tse", _sunset)
NOON = Glyph("NOON", "noon: SUN and NORTH made one", "tse", _noon)
MIDNIGHT = Glyph("MIDNIGHT", "midnight: SUN and SOUTH made one", "tse", _midnight)
GERMINATION = Glyph("GERMINATION", "germination: PLANT and EAST made one", "shi", _germination)
HARVEST = Glyph("HARVEST", "harvest, withering: PLANT and WEST made one", "shi", _harvest)
SEED_SOWN = Glyph("SEED-SOWN", "a seed sown: PLANT and SOUTH made one", "shi", _seed_sown)
LIFETIME = Glyph("LIFETIME", "a lifetime: EAST and WEST made one", "ku", _course(True))
REBIRTH = Glyph("REBIRTH", "rebirth: WEST and EAST made one", "tse", _course(False))
ERA_BEGINS = Glyph("ERA-BEGINS", "an era begins: EAST and HIGH made one", "tse", _era_begins)
PASSAGE_OF_THE_DEAD = Glyph("PASSAGE-OF-THE-DEAD", "the passage of the dead: WEST and SOUTH made one", "tse", _passage)
OUT_OF_THE_TRIALS = Glyph("OUT-OF-THE-TRIALS", "coming out of the trials: SOUTH and EAST made one", "to", _out_of_the_trials)
WHOLE_ROUND = Glyph("WHOLE-ROUND", "the whole round, the sun's day and the soul's existence: EAST, NORTH, WEST and SOUTH made one",
                    "tse", _whole_round)

TURNINGS = [DAWN, SUNSET, NOON, MIDNIGHT, GERMINATION, HARVEST, SEED_SOWN, LIFETIME, REBIRTH, ERA_BEGINS,
            PASSAGE_OF_THE_DEAD, OUT_OF_THE_TRIALS, WHOLE_ROUND]
