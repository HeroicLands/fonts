# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""House emblems of the Ch'alish P'ilam ceremonial hand.

    import emblems as H

    parts = H.KANKUL_SEAT.draw()              # [(pen, parts), ...]

A name is written with a **house emblem**: the concept glyph of the name's first element,
the house name, as the main sign of its block, with syllable signs and a coefficient for
descent round it. Each emblem is a picture in a full cushion. A house named for a
quality takes a concrete object of that quality: the censer for the sacred, the plumed
crown for the supreme, the jade ear spool for the highborn. Ish'bal, Ne' and Ish take
the glyphs JAGUAR, WATER and STAR, which already exist.

The three seats share one stepped seat: studded with gold for K'ankul, under a crescent
for Ishkul, and with a serpent coiled round it for Ch'akul.
"""

from __future__ import annotations

import math

import ceremonial as R
import strokes as S
from ceremonial import CONTOUR, DETAIL, CX0, CX1, CY0, CY1, C, Glyph


def _closed(*runs):
    """One closed track through several runs of points, each run's first point dropped
    after the first run."""
    pts = list(runs[0])
    for run in runs[1:]:
        pts += run[1:]
    return [S.Track(pts, closed=True)]


def _ellipse(cx, cy, rx, ry):
    return [S.Track(S._arc(cx, cy, rx, ry, 90, 450), closed=True)]


# -- the seats -----------------------------------------------------------------------------------


def _seat(x0, y0, x1, y1):
    """A stepped seat in profile, facing the line's start: two steps rising to the seat,
    and its back standing at the far end."""
    w, h = x1 - x0, y1 - y0
    X = lambda u: x0 + u * w  # noqa: E731
    Y = lambda v: y0 + v * h  # noqa: E731
    return S.poly([(X(0), Y(0)), (X(0), Y(0.24)), (X(0.2), Y(0.24)), (X(0.2), Y(0.48)), (X(0.4), Y(0.48)),
                   (X(0.4), Y(0.62)), (X(0.78), Y(0.62)), (X(0.78), Y(1)), (X(1), Y(1)), (X(1), Y(0)), (X(0), Y(0))])


def _kankul_seat():
    # the golden seat: the stepped seat studded with gold beads, a bead on each tread and
    # three set in its body
    x0, y0, x1, y1 = 110, CY0 + 115, 610, CY1 - 110
    w, h = x1 - x0, y1 - y0
    studs = R.bead(x0 + 0.56 * w, y0 + 0.3 * h, 52) + R.bead(x0 + 0.85 * w, y0 + 0.3 * h, 52) + \
        S.dot(x0 + 0.89 * w, y0 + 0.8 * h, 22)
    treads = S.dot(x0 + 0.1 * w, y0 + 0.12 * h, 16) + S.dot(x0 + 0.3 * w, y0 + 0.36 * h, 16)
    base = S.bar(x0 + 0.08 * w, y0 - 50, x1 - 0.08 * w, y0 - 50)
    return [(CONTOUR, R.cushion() + _seat(x0, y0, x1, y1)), (DETAIL, studs + treads + base)]


def _ishkul():
    # the silver seat: the stepped seat under a crescent, a band of silver dots on its body
    x0, y0, x1, y1 = 230, CY0 + 115, 610, CY1 - 110
    w, h = x1 - x0, y1 - y0
    moon = S.arc(195, CY1 - 195, 90, 90, 60, 300) + S.arc(235, CY1 - 195, 58, 66, 95, 265)
    silver = R.dotted([(x0 + 0.5 * w, y0 + 0.32 * h), (x0 + 0.68 * w, y0 + 0.32 * h)], r=14) + \
        R.dotted([(x0 + 0.89 * w, y0 + 0.4 * h), (x0 + 0.89 * w, y0 + 0.82 * h)], r=14)
    base = S.bar(x0 - 80, y0 - 50, x1 - 0.08 * w, y0 - 50)
    return [(CONTOUR, R.cushion() + _seat(x0, y0, x1, y1) + moon), (DETAIL, silver + base)]


def _chakul():
    # the serpent seat: a serpent coiled round the stepped seat, its head raised over the
    # seat's back and facing the line's start
    x0, y0, x1, y1 = 240, CY0 + 150, 520, CY1 - 250
    seat = _seat(x0, y0, x1, y1)
    body = S._bezier((150, CY1 - 210), (110, CY0 + 120), (200, CY0 + 50), (365, CY0 + 55))
    body += S._bezier((365, CY0 + 55), (560, CY0 + 60), (640, CY0 + 120), (610, C + 40))[1:]
    body += S._bezier((610, C + 40), (590, C + 150), (560, CY1 - 160), (470, CY1 - 120))[1:]
    head = _closed(S._bezier((470, CY1 - 120), (430, CY1 - 70), (330, CY1 - 70), (250, CY1 - 110)),
                   S._bezier((250, CY1 - 110), (300, CY1 - 190), (430, CY1 - 200), (470, CY1 - 120)))
    eye = S.dot(370, CY1 - 122, 20)
    tongue = R.curl(200, CY1 - 120, 36, turns=1.0, clockwise=True)
    scales = R.dotted([(170, C + 60), (175, CY0 + 160)], r=12) + R.dotted([(300, CY0 + 105), (520, CY0 + 105)], r=12)
    tail = R.curl(150, CY1 - 175, 44, turns=1.0)
    return [(CONTOUR, R.cushion() + seat + [S.Track(body)] + head), (DETAIL, eye + tongue + scales + tail)]


# -- water, plants and things ------------------------------------------------------------------


def _tsalam():
    # a spring: water welling from a cleft in a rock and falling in curls on either side
    rock = S.poly([(90, CY0 + 70), (140, C - 20), (230, C + 30), (330, C - 20), (365, C - 120),
                   (400, C - 20), (500, C + 30), (590, C - 20), (640, CY0 + 70), (90, CY0 + 70)])
    cleft = S.bar(365, C - 120, 365, CY0 + 120)
    welling = S._bezier((365, C - 70), (350, C + 60), (380, C + 140), (365, CY1 - 90))
    fall_l = R.curl(220, C + 150, 70, turns=1.3)
    fall_r = R.curl(510, C + 150, 70, turns=1.3, clockwise=True)
    drops = S.dot(290, CY1 - 110, 16) + S.dot(440, CY1 - 110, 16)
    grain = R.dotted([(170, CY0 + 130), (300, CY0 + 130)], r=12) + R.dotted([(430, CY0 + 130), (560, CY0 + 130)], r=12)
    return [(CONTOUR, R.cushion() + rock), (DETAIL, cleft + [S.Track(welling)] + fall_l + fall_r + drops + grain)]


def _kushi():
    # the maize ear: the cob in rows of kernels, the husk folded back on either side, the
    # silk curling from its tip
    cx, cy = C, C + 10
    cob = _ellipse(cx, cy, 105, 215)
    kernels = []
    for dx in (-48, 0, 48):
        top = 150 if dx == 0 else 125
        for k in range(7):
            y = cy - top + k * (2 * top) / 6
            kernels += S.dot(cx + dx, y, 13)
    husk_l = S._bezier((cx - 44, cy - 195), (cx - 200, cy - 240), (cx - 270, C + 40), (cx - 190, C + 190))
    husk_r = S._bezier((cx + 44, cy - 195), (cx + 200, cy - 240), (cx + 270, C + 40), (cx + 190, C + 190))
    silk = R.curl(cx - 70, CY1 - 50, 38, turns=1.0, clockwise=True) + R.curl(cx + 70, CY1 - 50, 38, turns=1.0)
    return [(CONTOUR, R.cushion() + cob + [S.Track(husk_l), S.Track(husk_r)]),
            (DETAIL, kernels + silk)]


def _tsul():
    # a stand of reeds: four stalks rising from the water, each with its seed head and a
    # leaf, the water's line at their foot
    out, heads = [], []
    for x, top, lean in ((170, CY1 - 120, -1), (290, CY1 - 60, 1), (430, CY1 - 90, -1), (560, CY1 - 140, 1)):
        out += S.bar(x, CY0 + 120, x, top - 70)
        heads.append(S.Fill(S._capsule(x, top - 70, x, top, 22)))
        y = CY0 + 230 + (x % 3) * 30
        out += S.arc(x + lean * 60, y, 60, 90, 90 + lean * 90 if lean > 0 else 0, 180 if lean > 0 else 90)
    water = S.wave(110, CY0 + 95, CX1 - 90, 18, 2.5)
    return [(CONTOUR, R.cushion() + water), (DETAIL, out + heads)]


def _vertical_wave(x, y0, y1, amp, periods):
    n = 40
    return [S.Track([(x + amp * math.sin(2 * math.pi * periods * i / n), y0 + (y1 - y0) * i / n) for i in range(n + 1)])]


def _chalish():
    # the sacred: a censer on its pedestal, copal smoke rising from it in three scrolls
    bowl = _closed(S._arc(C, CY0 + 300, 190, 150, 180, 360), [(C + 190, CY0 + 300), (C - 190, CY0 + 300)])
    foot = S.poly([(C - 90, CY0 + 160), (C - 120, CY0 + 80), (C + 120, CY0 + 80), (C + 90, CY0 + 160)])
    rim = S.bar(C - 230, CY0 + 300, C + 230, CY0 + 300)
    copal = R.dotted([(C - 110, CY0 + 245), (C + 110, CY0 + 245)], r=15)
    spikes = S.dot(C - 120, CY0 + 200, 14) + S.dot(C + 120, CY0 + 200, 14)
    smoke = _vertical_wave(C - 130, CY0 + 340, CY1 - 120, 26, 1.0) + _vertical_wave(C + 130, CY0 + 340, CY1 - 120, 26, 1.0) + \
        _vertical_wave(C, CY0 + 340, CY1 - 80, 26, 1.25)
    scrolls = R.curl(C - 145, CY1 - 95, 36, turns=1.0) + R.curl(C + 145, CY1 - 95, 36, turns=1.0, clockwise=True)
    return [(CONTOUR, R.cushion() + bowl + foot + rim), (DETAIL, copal + spikes + smoke + scrolls)]


def _qemul():
    # the supreme: the plumed crown, a beaded band with a jewel at its front and a fan of
    # long plumes rising from it, no head under it
    band = R.cushion(120, CY0 + 70, CX1 - 100, CY0 + 220, square=3.0)
    beads = R.bead(C - 125, CY0 + 145, 50) + R.bead(C + 10, CY0 + 145, 50) + R.bead(C + 145, CY0 + 145, 50)
    plumes = []
    for a in (160, 125, 90, 55, 20):
        t = math.radians(a)
        bx, by = C + 15 + 170 * math.cos(t), CY0 + 240
        tx, ty = C + 15 + 290 * math.cos(t), CY0 + 230 + 370 * math.sin(t)
        nx, ny = -math.sin(t) * 40, math.cos(t) * 40
        mx, my = (bx + tx) / 2, (by + ty) / 2
        plumes.append(S.Fill(S._bezier((bx, by), (mx + nx, my + ny), (tx + nx * 0.6, ty + ny * 0.6), (tx, ty))
                             + S._bezier((tx, ty), (tx - nx * 0.6, ty - ny * 0.6), (mx - nx, my - ny), (bx, by))[1:]))
    return [(CONTOUR, R.cushion() + band + plumes), (DETAIL, beads)]


def _puqem():
    # the highborn: the jade ear spool, its flare ringed with jade beads, a jewel at its
    # throat, and the pendant hanging from it with its tassel
    cx, cy = C, C + 60
    flare = S.ring(cx, cy, 190)
    jade = R.dotted_arc(cx, cy, 145, 145, 0, 360, r=13)
    throat = S.ring(cx, cy, 90) + S.dot(cx, cy, 30)
    pendant = S.bar(cx, cy - 190, cx, CY0 + 120)
    tassel = R.fringe(cx - 110, cx + 110, CY0 + 120, n=3, h=50)
    return [(CONTOUR, R.cushion() + flare), (DETAIL, jade + throat + pendant + tassel)]


def _nelush():
    # the great: the ceiba, its straight trunk spined with thorns, buttress roots spread at
    # its foot and its branches standing out level from the crown
    trunk = S.bar(C - 50, CY0 + 120, C - 50, CY1 - 210) + S.bar(C + 50, CY0 + 120, C + 50, CY1 - 210)
    roots = S._bezier((C - 50, CY0 + 140), (C - 70, CY0 + 70), (C - 160, CY0 + 50), (C - 260, CY0 + 50))
    roots_r = S._bezier((C + 50, CY0 + 140), (C + 70, CY0 + 70), (C + 160, CY0 + 50), (C + 260, CY0 + 50))
    thorns = R.dotted([(C, CY0 + 150), (C, CY1 - 240)], r=12, step=60)
    crown = S._bezier((C - 50, CY1 - 210), (C - 150, CY1 - 210), (C - 220, CY1 - 170), (C - 260, CY1 - 130))
    crown_r = S._bezier((C + 50, CY1 - 210), (C + 150, CY1 - 210), (C + 220, CY1 - 170), (C + 260, CY1 - 130))
    top = S.arc(C, CY1 - 210, 120, 120, 20, 160)
    leaves = R.curl(C - 240, CY1 - 90, 40, turns=1.0, clockwise=True) + R.curl(C + 240, CY1 - 90, 40, turns=1.0) + \
        R.curl(C, CY1 - 140, 40, turns=1.0)
    return [(CONTOUR, R.cushion() + trunk + [S.Track(roots), S.Track(roots_r), S.Track(crown), S.Track(crown_r)] + top),
            (DETAIL, thorns + leaves)]


def _chakal():
    # the big: the great gate, its corbelled arch stepping in to a capstone, a frieze of
    # crosses over it and a stair at its foot
    x0, x1, y0, y1 = 110, CX1 - 90, CY0 + 70, CY1 - 110
    wall = S.poly([(x0, y0), (x0, y1), (x1, y1), (x1, y0)])
    arch = S.poly([(C - 120, y0), (C - 120, y0 + 220), (C - 75, y0 + 220), (C - 75, y0 + 290), (C - 30, y0 + 290),
                   (C - 30, y0 + 350), (C + 30, y0 + 350), (C + 30, y0 + 290), (C + 75, y0 + 290), (C + 75, y0 + 220),
                   (C + 120, y0 + 220), (C + 120, y0)])
    frieze = S.bar(x0, y1 - 110, x1, y1 - 110)
    for k in range(4):
        frieze += R.x_mark(x0 + 70 + k * ((x1 - x0 - 140) / 3), y1 - 55, 28)
    ground = S.bar(CX0 + 60, y0, CX1 - 60, y0)
    stones = R.dotted([(x0 + 60, y0 + 200), (x0 + 60, y0 + 330)], r=13) + R.dotted([(x1 - 60, y0 + 200), (x1 - 60, y0 + 330)], r=13)
    return [(CONTOUR, R.cushion() + wall + arch + ground), (DETAIL, frieze + stones)]


def _toshel():
    # the southward: the conch, its spire to the line's start, knobs along its shoulder,
    # its whorl wound in and its lip opening below
    outline = _closed(S._bezier((110, CY1 - 160), (260, CY1 - 90), (480, CY1 - 110), (590, C + 60)),
                      S._bezier((590, C + 60), (650, C - 40), (640, CY0 + 120), (620, CY0 + 70)),
                      S._bezier((620, CY0 + 70), (520, CY0 + 120), (380, CY0 + 110), (250, C - 30)),
                      S._bezier((250, C - 30), (180, C + 30), (130, C + 120), (110, CY1 - 160)))
    whorl = R.curl(280, C + 60, 85, turns=1.5)
    knobs = R.dotted([(300, CY1 - 160), (520, CY1 - 175)], r=14, step=70)
    lip = S._bezier((420, C + 30), (520, C), (560, CY0 + 180), (580, CY0 + 120))
    return [(CONTOUR, R.cushion() + outline), (DETAIL, whorl + knobs + [S.Track(lip)])]


# -- creatures -----------------------------------------------------------------------------------


def _shaknal():
    # the eagle's head in profile, facing the line's start: the hooked beak, a great eye
    # under its brow, the crest swept back and the neck's feathers in a fringe
    outline = _closed(S._bezier((300, CY0 + 90), (280, C - 60), (240, C - 40), (200, C - 30)),
                      S._bezier((200, C - 30), (150, C - 40), (100, C - 20), (110, C - 80)),
                      S._bezier((110, C - 80), (90, C + 20), (130, C + 110), (240, C + 110)),
                      S._bezier((240, C + 110), (300, CY1 - 70), (500, CY1 - 70), (590, CY1 - 130)),
                      S._bezier((590, CY1 - 130), (620, C), (620, CY0 + 160), (610, CY0 + 90)),
                      [(610, CY0 + 90), (300, CY0 + 90)])
    cere = S.arc(250, C + 10, 60, 100, 300, 420)
    eye = S.ring(390, C + 50, 54) + S.dot(390, C + 50, 16)
    brow = S.arc(405, C + 60, 110, 95, 40, 100)
    crest = R.curl(520, CY1 - 175, 46, turns=1.2, clockwise=True)
    neck = R.fringe(330, 580, CY0 + 210, n=4, h=45)
    return [(CONTOUR, R.cushion() + outline), (DETAIL, cere + eye + brow + crest + neck)]


def _shelem_bird():
    # a perched bird in profile, facing the line's start: its round head and short beak,
    # the wing folded on its back, the long tail falling, its feet gripping the branch
    head = S.ring(260, C + 150, 80)
    eye = S.dot(245, C + 160, 18)
    beak = S.poly([(185, C + 170), (120, C + 140), (185, C + 120)])
    body = _closed(S._bezier((320, C + 100), (430, C + 120), (540, C + 40), (560, C - 70)),
                   S._bezier((560, C - 70), (500, C - 150), (330, C - 140), (260, C - 30)),
                   S._bezier((260, C - 30), (230, C + 20), (250, C + 70), (320, C + 100)))
    wing = S.arc(430, C - 30, 110, 70, 100, 200)
    feathers = R.dotted([(340, C - 80), (470, C - 80)], r=12)
    tail = S.bar(560, C - 70, 615, CY0 + 120) + S.bar(520, C - 110, 555, CY0 + 110)
    branch = S.bar(100, CY0 + 90, CX1 - 230, CY0 + 90)
    feet = S.bar(340, C - 120, 340, CY0 + 90) + S.bar(450, C - 140, 450, CY0 + 90)
    return [(CONTOUR, R.cushion() + body + head + branch), (DETAIL, eye + beak + wing + feathers + tail + feet)]


def _talon(tx, ty, d, k=1.0):
    """A talon hooked from a toe's tip at (tx, ty), curling down and back under the
    branch; ``d`` is 1 for a toe reaching toward the line's start, -1 for one behind, and
    ``k`` its size."""
    e, f = d * k, k
    return [S.Fill(S._bezier((tx + 18 * d, ty + 18), (tx - 60 * e, ty + 10 * f), (tx - 75 * e, ty - 70 * f), (tx - 10 * e, ty - 115 * f))
                   + S._bezier((tx - 10 * e, ty - 115 * f), (tx - 40 * e, ty - 70 * f), (tx - 30 * e, ty - 25 * f), (tx + 22 * d, ty - 16))[1:])]


def _ishtem():
    # the claw: a raptor's foot gripping a branch, its scaled leg slanting down from a
    # jewelled band, a toe forward along the branch, one down its face and one behind,
    # and the great talons hooked round it
    by = CY0 + 170
    branch = S.bar(80, by, CX1 - 60, by)
    bark = R.dotted([(110, by - 60), (200, by - 60)], r=11) + R.dotted([(480, by - 60), (560, by - 60)], r=11)
    leg = S.bar(390, by + 55, 450, CY1 - 90) + S.bar(500, by + 55, 560, CY1 - 90) + S.bar(450, CY1 - 90, 560, CY1 - 90)
    anklet = S.bar(430, 510, 540, 510)
    beads = S.dot(480, 560, 16)
    scales = []
    for y in (290, 345, 400):
        x = 445 + (y - 290) * 0.2
        scales += S.arc(x, y + 20, 32, 24, 205, 335)
    toes = [S.Track(S._bezier((395, by + 58), (320, by + 70), (230, by + 70), (180, by + 45))),
            S.Track(S._bezier((430, by + 58), (400, by + 30), (370, by), (345, by - 25))),
            S.Track(S._bezier((495, by + 58), (530, by + 70), (560, by + 65), (575, by + 45)))]
    talons = _talon(180, by + 45, 1, 1.2) + _talon(345, by - 25, 1, 0.85) + _talon(575, by + 45, -1, 1.1)
    knuckles = S.dot(300, by + 70, 15) + S.dot(410, by + 40, 13)
    return [(CONTOUR, R.cushion() + branch + leg + toes), (DETAIL, anklet + beads + scales + talons + bark + knuckles)]


# -- places --------------------------------------------------------------------------------------


def _tsultel():
    # the mountain: a rounded mountain of two summits, its cave mouth open at the foot with
    # fangs in its lip, and the curls of a living hill on its flanks
    hill = S._bezier((100, CY0 + 90), (100, C + 80), (180, CY1 - 100), (290, CY1 - 110))
    hill += S._bezier((290, CY1 - 110), (330, CY1 - 120), (340, C + 160), (380, C + 150))[1:]
    hill += S._bezier((380, C + 150), (420, C + 190), (440, CY1 - 80), (500, CY1 - 80))[1:]
    hill += S._bezier((500, CY1 - 80), (600, CY1 - 90), (630, C + 60), (630, CY0 + 90))[1:]
    cave = S.arc(C, CY0 + 90, 120, 160, 0, 180)
    fangs = S.poly([(C - 60, CY0 + 245), (C - 40, CY0 + 180), (C - 20, CY0 + 248)]) + \
        S.poly([(C + 20, CY0 + 248), (C + 40, CY0 + 180), (C + 60, CY0 + 245)])
    flanks = R.curl(170, C + 20, 55, turns=1.2) + R.curl(560, C + 20, 55, turns=1.2, clockwise=True)
    grapes = S.dot(270, C + 150, 15) + S.dot(250, C + 90, 15) + S.dot(480, C + 150, 15) + S.dot(500, C + 90, 15)
    ground = S.bar(CX0 + 60, CY0 + 90, CX1 - 60, CY0 + 90)
    return [(CONTOUR, R.cushion() + [S.Track(hill)] + cave + ground), (DETAIL, fangs + flanks + grapes)]


def _penqal():
    # the grassland: a tuft of tall grass, its blades springing from one root and bending
    # outward, seed heads on two of them, the ground under it
    root = (C, CY0 + 130)
    blades = []
    for tip, c in (((110, C + 120), (200, C - 120)), ((200, CY1 - 70), (280, C - 40)), ((340, CY1 - 40), (330, C)),
                   ((470, CY1 - 60), (420, C)), ((600, C + 150), (500, C - 100)), ((650, C - 30), (520, C - 180))):
        blades.append(S.Track(S._bezier(root, c, ((c[0] + tip[0]) / 2, (c[1] + tip[1]) / 2), tip)))
    seeds = R.dotted([(170, CY1 - 160), (190, CY1 - 90)], r=13, step=36) + R.dotted([(500, CY1 - 160), (480, CY1 - 90)], r=13, step=36)
    ground = S.arc(C, CY0 + 70, 220, 60, 0, 180) + S.bar(CX0 + 50, CY0 + 70, CX1 - 50, CY0 + 70)
    soil = R.dotted([(C - 120, CY0 + 100), (C + 120, CY0 + 100)], r=11)
    return [(CONTOUR, R.cushion() + ground), (DETAIL, blades + seeds + soil)]


def _qaptel():
    # the border: a boundary post set in the ground, its cord wound round it and stretched
    # out to either side, knotted along its length
    post = _closed([(C - 55, CY0 + 110), (C - 55, CY1 - 160)],
                   S._arc(C, CY1 - 160, 55, 70, 180, 0),
                   [(C + 55, CY1 - 160), (C + 55, CY0 + 110)])
    wraps = S.bar(C - 55, C + 40, C + 55, C + 90) + S.bar(C - 55, C - 20, C + 55, C + 30)
    cord = S.wave(80, C + 60, C - 55, 16, 1.5) + S.wave(C + 55, C + 60, CX1 - 60, 16, 1.5)
    knots = S.dot(140, C + 60, 20) + S.dot(250, C + 60, 20) + S.dot(480, C + 60, 20) + S.dot(590, C + 60, 20)
    ground = S.bar(CX0 + 70, CY0 + 110, CX1 - 70, CY0 + 110)
    ticks = []
    for x in (180, 260, 490, 570):
        ticks += S.bar(x, CY0 + 110, x - 25, CY0 + 60)
    cap = S.dot(C, CY1 - 120, 18)
    return [(CONTOUR, R.cushion() + post + ground), (DETAIL, wraps + cord + knots + ticks + cap)]


def _neok():
    # flowing: a river winding between its banks, the current running down its channel,
    # sand dotted on the near bank and reeds on the far one
    upper = S._bezier((70, C + 200), (300, C + 220), (380, C - 20), (660, C + 40))
    lower = S._bezier((70, C - 20), (300, C), (380, C - 240), (660, C - 180))
    current = S._bezier((120, C + 90), (310, C + 110), (380, C - 130), (610, C - 70))
    curls = R.curl(200, C + 40, 30, turns=1.0) + R.curl(520, C - 30, 30, turns=1.0)
    sand = R.dotted([(150, CY0 + 140), (380, CY0 + 60)], r=12)
    reeds = S.bar(470, C + 150, 470, CY1 - 60) + S.bar(540, C + 160, 560, CY1 - 70) + S.bar(610, C + 170, 650, CY1 - 120)
    return [(CONTOUR, R.cushion() + [S.Track(upper), S.Track(lower)]), (DETAIL, [S.Track(current)] + curls + sand + reeds)]


KANKUL_SEAT = Glyph("KANKUL-SEAT", "K'ankul, the golden seat: a stepped seat studded with gold", "ka", _kankul_seat)
ISHKUL = Glyph("ISHKUL", "Ishkul, the silver seat: the stepped seat under a crescent", "i", _ishkul)
CHAKUL = Glyph("CHAKUL", "Ch'akul, the serpent seat: a serpent coiled round the stepped seat", "cha", _chakul)
TSALAM = Glyph("TSALAM", "Ts'alam, a spring: water welling from a cleft rock", "tsa", _tsalam)
KUSHI = Glyph("KUSHI", "K'ushi, the maize ear: an ear of maize in its husk", "ku", _kushi)
TSUL = Glyph("TSUL", "Tsul, a reed: a stand of reeds", "tsu", _tsul)
CHALISH = Glyph("CHALISH", "Ch'alish, sacred: a censer with rising copal smoke", "cha", _chalish)
QEMUL = Glyph("QEMUL", "Q'emul, supreme: the plumed crown", "qe", _qemul)
PUQEM = Glyph("PUQEM", "Puq'em, highborn: the jade ear spool", "pu", _puqem)
NELUSH = Glyph("NELUSH", "Nelush, great: the great tree, the ceiba", "ne", _nelush)
CHAKAL = Glyph("CHAKAL", "Ch'akal, big: the great gate", "cha", _chakal)
TOSHEL = Glyph("TOSHEL", "Toshel, southward: the conch shell", "to", _toshel)
SHAKNAL = Glyph("SHAKNAL", "Shak'nal, the eagle: an eagle's head", "sha", _shaknal)
TSULTEL = Glyph("TSULTEL", "Ts'ultel, the mountain: a mountain with its cave mouth", "tsu", _tsultel)
PENQAL = Glyph("PENQAL", "P'enqal, the grassland: a tuft of tall grass", "pe", _penqal)
SHELEM_BIRD = Glyph("SHELEM-BIRD", "Shelem, the bird: a perched bird", "she", _shelem_bird)
ISHTEM = Glyph("ISHTEM", "Ishtem, the claw: a raptor's talon", "i", _ishtem)
QAPTEL = Glyph("QAPTEL", "Q'aptel, the border: a boundary post with its cord", "qa", _qaptel)
NEOK = Glyph("NEOK", "Ne'ok, flowing: a river between its banks", "ne", _neok)

EMBLEMS = [KANKUL_SEAT, ISHKUL, CHAKUL, TSALAM, KUSHI, TSUL, CHALISH, QEMUL, PUQEM, NELUSH, CHAKAL, TOSHEL,
           SHAKNAL, TSULTEL, PENQAL, SHELEM_BIRD, ISHTEM, QAPTEL, NEOK]
