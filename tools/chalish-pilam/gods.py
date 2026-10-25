# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""The gods of the Itsani pantheon in the Ch'alish P'ilam ceremonial hand.

    import gods as G

    parts = G.SACRED_STAR.draw()             # [(pen, parts), ...]

A god is one glyph, as complicated as it needs to be, built from the symbol canon gives
the god and drawn in the ceremonial canon of ``ceremonial.py``: its kit, its two brushes,
and the carving rule that no groove is narrower than a chisel can cut.
"""

from __future__ import annotations

import math

import ceremonial as R
import strokes as S
from ceremonial import CONTOUR, DETAIL, CX0, CX1, CY0, CY1, B, C, Glyph

DOUBLE = R.WIDTH["double"]


def _star(cx, cy, r, inner=0.38):
    """A four-pointed star: the stellar sign."""
    pts = []
    for k in range(9):
        a = math.radians(90 + k * 45)
        rr = r if k % 2 == 0 else r * inner
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return S.poly(pts)


def _rosette(cx, cy, r):
    """A golden flower: a bead ringed by petals."""
    out = S.dot(cx, cy, r * 0.3)
    for k in range(6):
        a = math.radians(k * 60)
        out += S.dot(cx + r * math.cos(a), cy + r * math.sin(a), r * 0.24)
    return out


def _sun_at_the_edge():
    # Ts'en'ul Tq'an, order: the sun's disk cut by the horizon, its face above the line,
    # rays curling from its rim, and below the line the netted dark of its night road
    horizon = C - 40
    face = S.arc(C, horizon + 30, 190, 190, 0, 180)
    rays = []
    for a in (20, 55, 90, 125, 160):
        t = math.radians(a)
        rays += R.curl(C + 255 * math.cos(t), horizon + 30 + 230 * math.sin(t), 30, turns=1.0)
    band = S.bar(CX0 + 40, horizon + 30, CX1 - 40, horizon + 30) + S.bar(CX0 + 40, horizon - 40, CX1 - 40, horizon - 40)
    band += R.dotted([(CX0 + 80, horizon - 5), (CX1 - 80, horizon - 5)])
    features = R.eye(C - 40, horizon + 105, "open") + S.arc(C - 10, horizon + 70, 60, 26, 200, 340) + R.curl(C + 100, horizon + 110, 40, turns=1.0)
    night = R.net(C - 210, CY0 + 50, 420, horizon - 40 - CY0 - 80)
    return [(CONTOUR, R.cushion() + face + band), (DETAIL, rays + features + night)]


def _death_jaguar():
    # Ts'uqil Ish'bal, death: a jaguar's skull in profile, its eye an empty socket, its
    # teeth bared, spotted; crowned with three obsidian blades, an owl perched on the brow
    box = (CX0 + 10, CY0, CX1 - 10, CY1 - 190)
    contour, _ = R.head(*box, spool=False, band=False)
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    X = lambda u: x0 + u * w  # noqa: E731
    Y = lambda v: y0 + v * h  # noqa: E731
    socket = S.ring(X(0.3), Y(0.63), w * 0.1) + S.dot(X(0.3), Y(0.63), 14)
    nose = S.dot(X(0.13), Y(0.5), 12) + S.dot(X(0.19), Y(0.47), 12)
    teeth = []
    for k in range(5):
        x = X(0.08 + k * 0.07)
        teeth += S.poly([(x, Y(0.36)), (x, Y(0.24)), (x + w * 0.05, Y(0.24)), (x + w * 0.05, Y(0.36))])
    jaw = S.bar(X(0.06), Y(0.36), X(0.48), Y(0.36))
    spots = []
    for u, v in ((0.62, 0.7), (0.82, 0.48), (0.6, 0.36)):
        spots += S.ring(X(u), Y(v), 46) + S.dot(X(u), Y(v), 12)
    blades = []
    for k, cx in enumerate((X(0.5), X(0.68), X(0.86))):
        base, top = Y(1.0) - 16, CY1 - 10 - (0 if k == 1 else 40)
        blades += [S.Track([(cx - 40, base), (cx - 30, (base + top) / 2), (cx, top), (cx + 30, (base + top) / 2),
                            (cx + 40, base)])]
        blades += S.bar(cx, base + 30, cx, top - 70)
    owl_x, owl_y = X(0.25), Y(1.0) + 60
    owl = [S.Track(S._arc(owl_x, owl_y, 75, 70, 200, 520))] + S.ring(owl_x - 30, owl_y + 10, 22) + \
        S.ring(owl_x + 30, owl_y + 10, 22) + S.poly([(owl_x - 12, owl_y - 22), (owl_x, owl_y - 50), (owl_x + 12, owl_y - 22)])
    return [(CONTOUR, contour + blades + owl), (DETAIL, socket + nose + teeth + jaw + spots)]


def _storm_serpent():
    # P'uqil Ch'akun, storms: a feathered serpent's head, double-wide, its body coiled into
    # a thundercloud behind it; lightning tipped with a jade bead leaps from its jaws
    head_box = (CX0 + 60, CY0 + 60, 860, CY1 - 90)
    contour, detail = R.head(*head_box, eye_kind="spiral", spool=False, band=False)
    x0, y0, x1, y1 = head_box
    w, h = x1 - x0, y1 - y0
    X = lambda u: x0 + u * w  # noqa: E731
    Y = lambda v: y0 + v * h  # noqa: E731
    fangs = S.poly([(X(0.1), Y(0.34)), (X(0.14), Y(0.18)), (X(0.18), Y(0.34))])
    plumes = []
    for k in range(5):
        plumes += S.arc(X(0.36 + k * 0.13), Y(1.0) + 6, 46, 80, 0, 180)
    # the thundercloud: three swelling lobes over a flat base, the serpent's coils inside
    base = CY0 + 80
    cloud_pts = ([(900, base)] + S._arc(985, C - 20, 115, 115, 225, 60) + S._arc(1170, C + 40, 150, 150, 150, 30)
                 + S._arc(1360, C - 20, 105, 105, 120, -40) + [(1450, base), (900, base)])
    cloud = [S.Track(cloud_pts)]
    coils = R.curl(1020, C - 10, 66, turns=1.2) + R.curl(1190, C + 50, 80, turns=1.3, clockwise=True) + \
        R.curl(1335, C - 50, 50, turns=1.1)
    rain = R.dotted([(930, CY0 + 120), (1420, CY0 + 120)])
    scales = []
    for k, (u, v) in enumerate(((0.62, 0.66), (0.78, 0.6), (0.7, 0.38), (0.86, 0.36))):
        scales += S.ring(X(u), Y(v), 46) + S.dot(X(u), Y(v), 12)
    scales += R.dotted([(X(0.4), Y(0.14)), (X(0.9), Y(0.2))])
    bolt = S.poly([(X(0.05), Y(0.3)), (X(-0.05), Y(0.16)), (X(0.06), Y(0.1)), (X(-0.06), CY0 + 30)])
    jade = R.bead(X(-0.06), CY0 + 30, 26)
    return [(CONTOUR, contour + cloud), (DETAIL, detail + fangs + plumes + coils + rain + scales + bolt + jade)]


def _sacred_star():
    # Ish'ilan Ch'alish, knowledge: a star within an open codex, its folded leaves ruled
    # with counts of bar and dot
    x0, y0, x1, y1 = CX0 + 60, CY0 + 60, CX1 - 60, CY1 - 50
    folds = [x0 + (x1 - x0) * k / 3 for k in (1, 2)]
    leaves = []
    for fx in folds:
        leaves += S.bar(fx, CY0, fx, CY1)
    counts = []
    for k, fx in enumerate((x0, folds[1])):
        bx = fx + 30
        counts += S.bar(bx, y0 + 50, bx + (x1 - x0) / 3 - 60, y0 + 50)
        counts += R.dotted([(bx + 10, y0 + 110), (bx + (x1 - x0) / 3 - 70, y0 + 110)])
    star = _star(C, C + 60, 150) + S.dot(C, C + 60, 22)
    return [(CONTOUR, R.cushion() + leaves), (DETAIL, star + counts + R.dotted([(x0 + 40, CY0 + 60), (x1 - 40, CY0 + 60)]))]


def _golden_giver():
    # K'anish Ha'kan, prosperity: a maize stalk rising from the earth, bearing golden
    # flowers, its ear swelling in its husk, its leaves arching down to either side
    ground = R.dotted([(CX0 + 90, CY0 + 50), (CX1 - 90, CY0 + 50)])
    stalk = S.bar(C - 40, CY0, C - 40, CY1 - 170)
    leaves = S.arc(C - 200, C - 40, 160, 180, 0, 90) + S.arc(C + 110, C + 20, 150, 170, 90, 180)
    ear = S.frame(C + 50, C - 140, 150, 300, square=2.2)
    kernels = []
    for row in range(4):
        for col in range(2):
            kernels += S.dot(C + 92 + col * 66, C - 90 + row * 64, 15)
    flowers = _rosette(C - 40, CY1 - 110, 50) + _rosette(C - 210, CY1 - 210, 44) + _rosette(C + 175, CY1 - 160, 44)
    return [(CONTOUR, R.cushion() + ear + stalk), (DETAIL, ground + leaves + kernels + flowers)]


def _sacred_flame():
    # K'ayik Ch'alish, fire: a flame rising from a jade altar, the altar banded with beads
    # and netting, smoke going up from the flame's tip
    altar = S.poly([(C - 230, CY0), (C + 180 + 50, CY0), (C + 180, CY0 + 230), (C - 180, CY0 + 230), (C - 230, CY0)])
    altar += S.bar(C - 250, CY0 + 230, C + 250, CY0 + 230)
    jade = R.dotted([(C - 170, CY0 + 185), (C + 170, CY0 + 185)], r=13) + R.net(C - 150, CY0 + 75, 300, 80, n=3)
    flame = [S.Track(S._bezier((C - 140, CY0 + 230), (C - 220, C + 60), (C - 40, C + 120), (C - 10, CY1 - 60))
                     + S._bezier((C - 10, CY1 - 60), (C + 60, C + 80), (C + 230, C + 40), (C + 130, CY0 + 230))[1:])]
    tongues = R.curl(C - 60, C + 10, 60, turns=1.2) + R.curl(C + 70, C - 20, 50, turns=1.2, clockwise=True)
    smoke = R.dotted([(C + 10, CY1 - 20), (C + 60, CY1 + 10)], r=10)
    return [(CONTOUR, R.cushion() + altar + flame), (DETAIL, jade + tongues + smoke)]


def _peak_builder():
    # P'iqal Kul'qat, creation: the stepped pyramid beneath a crescent moon, its stair
    # climbing the middle, its shrine on the summit
    steps = [(CX0 + 70, CY0), (CX0 + 70, CY0 + 130), (CX0 + 150, CY0 + 130), (CX0 + 150, CY0 + 210),
             (CX0 + 230, CY0 + 210), (CX0 + 230, CY0 + 290), (CX1 - 230, CY0 + 290), (CX1 - 230, CY0 + 210),
             (CX1 - 150, CY0 + 210), (CX1 - 150, CY0 + 130), (CX1 - 70, CY0 + 130), (CX1 - 70, CY0)]
    stair = []
    for k in range(4):
        y = CY0 + 50 + k * 60
        stair += S.bar(C - 50, y, C + 50, y)
    shrine = S.poly([(C - 70, CY0 + 290), (C - 70, CY0 + 370), (C + 70, CY0 + 370), (C + 70, CY0 + 290)])
    moon = S.arc(C, CY0 + 470, 150, 90, 200, 340) + S.arc(C, CY0 + 520, 120, 90, 205, 335)
    return [(CONTOUR, R.cushion() + S.poly(steps)),
            (DETAIL, stair + shrine + moon + R.dotted([(C - 200, CY1 - 50), (C + 200, CY1 - 50)]))]


def _path_walker():
    # Shilan Ish'lan, voyages: a footprint on the white road, wide at the ball of the foot,
    # narrow at the heel, marked with the stars of the four quarters
    top, bot = C + 170, C - 210
    sole = [S.Track(S._bezier((C - 20, bot), (C - 110, bot + 20), (C - 130, C + 60), (C - 70, top))
                    + S._bezier((C - 70, top), (C - 20, top + 30), (C + 110, top + 20), (C + 110, C + 80))[1:]
                    + S._bezier((C + 110, C + 80), (C + 100, C - 40), (C + 60, bot + 40), (C - 20, bot))[1:], closed=True)]
    toes = []
    for dx, dy, r in ((-60, 235, 24), (-12, 252, 21), (32, 254, 19), (70, 240, 17), (100, 214, 15)):
        toes += S.dot(C + dx, C + dy, r)
    stars = _star(CX0 + 120, CY1 - 110, 62) + _star(CX1 - 120, CY1 - 110, 62) + _star(CX0 + 120, CY0 + 110, 62) + \
        _star(CX1 - 120, CY0 + 110, 62)
    road = R.dotted([(CX0 + 60, C - 10), (C - 150, C - 10)]) + R.dotted([(C + 150, C - 10), (CX1 - 60, C - 10)])
    return [(CONTOUR, R.cushion() + sole), (DETAIL, toes + stars + road + S.arc(C, C - 60, 50, 60, 200, 340))]


def _moon_dreamer():
    # Nal'ik Ts'uqal, dreams: a crescent moon cradling a sleeping face, threads of silver
    # mist trailing from it
    moon = S.arc(C - 90, C - 10, 200, 230, 60, 300) + S.arc(C - 10, C - 10, 150, 175, 75, 285)
    sleeper = R.eye(C - 130, C + 30, "closed") + S.arc(C - 120, C - 80, 40, 20, 200, 340)
    mist = []
    for k in range(3):
        mist += S.wave(C + 60, C + 120 - k * 110, CX1 - 50, 26, 1.5)
    return [(CONTOUR, R.cushion() + moon), (DETAIL, sleeper + mist + R.dotted([(C + 80, CY0 + 60), (CX1 - 70, CY0 + 60)]))]


def _living_blossom():
    # Shaq'ik Ha'nal, fertility: a water lily blooming from a spring, its petals open, its
    # pad beside it, the spring's rings of water at its root
    spring = S.arc(C, CY0 + 100, 230, 70, 0, 180) + R.dotted([(C - 170, CY0 + 50), (C + 170, CY0 + 50)])
    stem = S.bar(C, CY0 + 170, C, C + 20)
    cup = S.arc(C, C + 120, 160, 100, 200, 340)
    petals = []
    for k, a in enumerate((40, 140)):
        t = math.radians(a)
        bx, by = C + 120 * math.cos(t), C + 40 + 40 * math.sin(t)
        tx, ty = C + 210 * math.cos(t), C + 80 + 210 * math.sin(t)
        petals += S.poly([(bx - 26, by), (tx, ty), (bx + 26, by)])
    heart = S.poly([(C - 30, C + 40), (C, CY1 - 80), (C + 30, C + 40)])
    pad = S.arc(C + 230, C - 90, 100, 60, 30, 330)
    return [(CONTOUR, R.cushion() + cup + heart), (DETAIL, spring + stem + petals + pad)]


def _fallen_owl():
    # Pik'ul Ts'umaq, the fallen: an owl cast down headfirst, its great eyes staring up
    # from below, its tufts pointing to the earth, its feathers falling round it
    body = S.frame(CX0 + 120, CY0 + 40, CX1 - CX0 - 240, CY1 - CY0 - 80, square=2.2)
    eyes = S.ring(C - 85, CY0 + 220, 70) + S.ring(C + 85, CY0 + 220, 70) + S.dot(C - 85, CY0 + 220, 24) + \
        S.dot(C + 85, CY0 + 220, 24)
    beak = S.poly([(C - 30, CY0 + 320), (C, CY0 + 390), (C + 30, CY0 + 320)])
    tufts = S.poly([(C - 150, CY0 + 90), (C - 200, CY0 + 10), (C - 100, CY0 + 70)]) + \
        S.poly([(C + 150, CY0 + 90), (C + 200, CY0 + 10), (C + 100, CY0 + 70)])
    feathers = R.fringe(C - 170, C + 170, CY1 - 160, h=50)
    falling = R.dotted([(CX0 + 50, CY1 - 60), (CX0 + 50, CY0 + 120)]) + R.dotted([(CX1 - 50, CY1 - 60), (CX1 - 50, CY0 + 120)])
    return [(CONTOUR, body + tufts), (DETAIL, eyes + beak + feathers + falling)]


SUN_AT_THE_EDGE = Glyph("SUN-AT-THE-EDGE", "Ts'en'ul Tq'an, order", "tse", _sun_at_the_edge)
DEATH_JAGUAR = Glyph("DEATH-JAGUAR", "Ts'uqil Ish'bal, death", "tsu", _death_jaguar)
STORM_SERPENT = Glyph("STORM-SERPENT", "P'uqil Ch'akun, storms", "pu", _storm_serpent, "double")
SACRED_STAR = Glyph("SACRED-STAR", "Ish'ilan Ch'alish, knowledge", "i", _sacred_star)
GOLDEN_GIVER = Glyph("GOLDEN-GIVER", "K'anish Ha'kan, prosperity", "ka", _golden_giver)
SACRED_FLAME = Glyph("SACRED-FLAME", "K'ayik Ch'alish, fire", "ka", _sacred_flame)
PEAK_BUILDER = Glyph("PEAK-BUILDER", "P'iqal Kul'qat, creation", "pi", _peak_builder)
PATH_WALKER = Glyph("PATH-WALKER", "Shilan Ish'lan, voyages", "shi", _path_walker)
MOON_DREAMER = Glyph("MOON-DREAMER", "Nal'ik Ts'uqal, dreams", "na", _moon_dreamer)
LIVING_BLOSSOM = Glyph("LIVING-BLOSSOM", "Shaq'ik Ha'nal, fertility", "sha", _living_blossom)
FALLEN_OWL = Glyph("FALLEN-OWL", "Pik'ul Ts'umaq, the fallen", "pi", _fallen_owl)

GODS = [SUN_AT_THE_EDGE, DEATH_JAGUAR, STORM_SERPENT, SACRED_STAR, GOLDEN_GIVER, SACRED_FLAME, PEAK_BUILDER,
        PATH_WALKER, MOON_DREAMER, LIVING_BLOSSOM, FALLEN_OWL]
