# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Rank and office in the Ch'alish P'ilam ceremonial hand.

    import ranks as T

    parts = T.KING.draw()                    # [(pen, parts), ...]

Each title canon gives is one glyph: a head in profile, facing the line's start, wearing
the regalia of its office. The head is the same canon every title shares, set low in the
block; the headdress zone above it, and what the head holds or wears, tell the offices
apart.
"""

from __future__ import annotations

import math

import ceremonial as R
import strokes as S
from ceremonial import CONTOUR, DETAIL, CX1, CY0, CY1, C, Glyph

# The head every title shares, and the zone above it that the regalia fills.
HEAD = (140.0, CY0, CX1 - 70, C + 35)
CROWN_Y = C + 35  # the head's crown; the headdress rests on it
TOP = CY1 + 10
BAND = 140  # how far the headdress band swells above the crown: the headdress fills half the block


def _box():
    x0, y0, x1, y1 = HEAD
    w, h = x1 - x0, y1 - y0
    return x0, y0, x1, y1, w, h, (lambda u: x0 + u * w), (lambda v: y0 + v * h)


def _crown(lo=40, hi=131):
    """Points along the head's crown, from the back of the head to the brow."""
    x0, y0, x1, y1, w, h, X, Y = _box()
    return [(X(0.62) + w * 0.38 * math.cos(math.radians(a)), Y(0.5) + h * 0.5 * math.sin(math.radians(a)))
            for a in range(lo, hi, 3)]


def _band_top(wave=0.0):
    """The top edge of a headdress band resting on the crown, swelling over it; ``wave``
    makes the edge run as water."""
    crown = _crown()
    n = len(crown) - 1
    return [(x, y + BAND * R._swell(k / n) + wave * math.sin(k / n * 4 * math.pi) * R._swell(k / n))
            for k, (x, y) in enumerate(crown)]


def _at(top, t):
    """The point a share ``t`` of the way along a band's top, from the brow."""
    return top[round((1 - t) * (len(top) - 1))]


def _crown_band(beads=True, wave=0.0):
    """A headdress band resting on the crown, beaded inside."""
    top = _band_top(wave)
    out = [S.Track(top)]
    if beads:
        crown = _crown()
        for k in range(5):
            t = (k + 0.5) / 5
            (x, y), (_, yt) = _at(crown, t), _at(top, t)
            if yt - y > 95:  # room for a bead with a groove either side
                out += S.dot(x, (y + yt) / 2, 11)
    return out


def _sun_disk(cx, cy, r):
    rays = []
    for k in range(6):
        a = math.radians(90 + k * 60)
        rays += S.bar(cx + (r + 26) * math.cos(a), cy + (r + 26) * math.sin(a), cx + (r + 62) * math.cos(a),
                      cy + (r + 62) * math.sin(a))
    return S.ring(cx, cy, r) + S.dot(cx, cy, r * 0.32) + rays


def _plumes(xs, base, tall=90):
    out = []
    for k, x in enumerate(xs):
        out += S.arc(x + 34, base, 34, tall, 90, 180) + S.arc(x - 34, base, 34, tall, 0, 90)
    return out


def titled(eye="open", spool=True, tooth=False, face=""):
    """The head every title shares. ``face`` marks the office on the face itself: ``age``
    (a line under the eye), ``beard`` (a fringe at the chin) or ``paint`` (bars across the
    cheek)."""
    contour, detail = R.head(*HEAD, eye_kind=eye, spool=spool, band=False, tooth=tooth)
    x0, y0, x1, y1, w, h, X, Y = _box()
    m = min(w, h)
    if face == "age":
        # deep lines: one under the eye, one from the nose to the mouth's corner
        detail += S.arc(X(0.29), Y(0.5), m * 0.15, h * 0.07, 215, 325) + S.arc(X(0.2), Y(0.36), m * 0.1, h * 0.14, 270, 350)
    elif face == "beard":
        # a full beard hanging from the chin in locks
        for k in range(3):
            bx = X(0.06) + k * m * 0.09
            detail += [S.Fill(S._capsule(bx, Y(0.2), bx + 8, Y(0.2) - 70 - 12 * k, 16))]
    elif face == "paint":
        # broad bars of paint across the cheek and over the eye
        detail += [S.Fill(S._capsule(X(0.36), Y(0.48), X(0.52), Y(0.44), 16)),
                   S.Fill(S._capsule(X(0.38), Y(0.26), X(0.54), Y(0.22), 16))]
    return contour, detail


def _overlord():
    # Q'emulmah, the supreme lord: a towering headdress of plumes, the two stacked beads
    # of the supreme over the brow, a jewelled ear spool, the face of age
    contour, detail = titled(face="age")
    x0, y0, x1, y1, w, h, X, Y = _box()
    top = _band_top()
    plumes = []
    for t in (0.3, 0.55, 0.8):
        x, y = _at(top, t)
        plumes += _plumes([x], y, 210)
    bx, by = _at(top, 0.08)
    crest = S.dot(bx, by + 34, 18) + S.dot(bx, by + 86, 18)
    return [(CONTOUR, contour + _crown_band(False) + plumes), (DETAIL, detail + crest + _crown_band()[1:])]


def _king():
    # Ts'enmah, the Lord of the Sun: the sun's disk rising over his crown
    contour, detail = titled()
    x0, y0, x1, y1, w, h, X, Y = _box()
    x, y = _at(_band_top(), 0.5)
    return [(CONTOUR, contour + _crown_band()), (DETAIL, detail + _sun_disk(x, y + 90, 78))]


def _prince():
    # Ts'enilbal, heir to the sun: a young head with the sun's disk small at the brow and
    # its shining rising from it in curls
    contour, detail = titled(spool=False)
    x0, y0, x1, y1, w, h, X, Y = _box()
    top = _band_top()
    (sx, sy), (ax, ay), (bx, by) = _at(top, 0.15), _at(top, 0.5), _at(top, 0.78)
    shine = R.curl(ax, ay + 50, 40, turns=1.0) + R.curl(bx, by + 46, 40, turns=1.0, clockwise=True)
    return [(CONTOUR, contour + _crown_band(False)), (DETAIL, detail + _sun_disk(sx, sy + 52, 46) + shine)]


def _noble():
    # K'anulmah, the golden lord: a beaded band of gold with a golden flower at the brow
    contour, detail = titled()
    x0, y0, x1, y1, w, h, X, Y = _box()
    fx, fy = _at(_band_top(), 0.2)
    fy += 60
    flower = S.dot(fx, fy, 14)
    for k in range(6):
        a = math.radians(k * 60)
        flower += S.dot(fx + 46 * math.cos(a), fy + 46 * math.sin(a), 13)
    return [(CONTOUR, contour + _crown_band()), (DETAIL, detail + flower)]


def _seated_lord():
    # Kulmah, lord of a seat: the head over the woven mat of the seat he holds
    x0, y0, x1, y1 = HEAD
    contour, detail = R.head(x0, y0 + 110, x1, y1 + 110, spool=True, band=False)
    mat = S.poly([(x0 + 40, CY0), (x0 + 40, CY0 + 90), (x1 - 40, CY0 + 90), (x1 - 40, CY0), (x0 + 40, CY0)])
    for k in range(1, 4):
        x = x0 + 40 + k * (x1 - x0 - 80) / 4
        mat += S.bar(x, CY0, x, CY0 + 90)
    return [(CONTOUR, contour + mat), (DETAIL, detail)]


def _lady():
    # Ish'kanmah, the golden noblewoman: a beaded band, and her hair falling behind in long
    # locks
    contour, detail = titled(spool=True)
    x0, y0, x1, y1, w, h, X, Y = _box()
    locks = []
    for k in range(3):
        a = math.radians(30 - k * 30)
        sx, sy = X(0.62) + w * 0.38 * math.cos(a), Y(0.5) + h * 0.5 * math.sin(a)
        locks += S.bar(sx, sy, sx + 70, sy - 140 + k * 10)
    return [(CONTOUR, contour + _crown_band()), (DETAIL, detail + locks)]


def _landholder():
    # Ha'nalmah, lord of the land: a band of river water across his headdress
    contour, detail = titled()
    x0, y0, x1, y1, w, h, X, Y = _box()
    return [(CONTOUR, contour + _crown_band(False, wave=22)), (DETAIL, detail + _crown_band(wave=22)[1:])]


def _knight():
    # Ts'omilbal, servant of the bond: the knotted cord of his oath tied across his crown,
    # his face painted for war
    contour, detail = titled(face="paint")
    x0, y0, x1, y1, w, h, X, Y = _box()
    top = _band_top()
    knots = []
    for t in (0.25, 0.5, 0.75):
        x, y = _at(top, t)
        knots += S.dot(x, y, 26) + S.bar(x, y + 24, x + 16, y + 96)
    ex, ey = _at(top, 1.0)
    ends = S.bar(ex, ey, ex + 50, ey - 120) + S.bar(ex, ey, ex + 90, ey - 90)
    return [(CONTOUR, contour + _crown_band(False)), (DETAIL, detail + knots + ends)]


def _war_leader():
    # Shok'almah, the war-leader: a crested helmet of steel over the head, a feather at its
    # crest
    contour, detail = titled(spool=False, face="paint")
    x0, y0, x1, y1, w, h, X, Y = _box()
    helmet = S.arc(X(0.62), Y(0.5), w * 0.42, h * 0.56, 40, 140)
    ridge = S.bar(X(0.46), Y(0.6), X(0.96), Y(0.6))
    top = Y(0.5) + h * 0.56
    crest = S.arc(X(0.62), top - 10, 130, 110, 15, 165)
    feather = [S.Fill([(X(0.58), top + 96), (X(0.62), TOP - 10), (X(0.66), top + 96)])]  # solid: too narrow to cut hollow
    rivets = R.dotted([(X(0.5), Y(0.68)), (X(0.82), Y(0.68))])
    return [(CONTOUR, contour + helmet + crest), (DETAIL, detail + ridge + feather + rivets)]


def _sun_priest():
    # Ts'enbal, keeper of the count of days: the sun's disk, and the count in bar and dot
    # beside it; the face of age
    contour, detail = titled(face="age")
    x0, y0, x1, y1, w, h, X, Y = _box()
    top = _band_top()
    (sx, sy), (cx, cy) = _at(top, 0.3), _at(top, 0.72)
    count = S.bar(cx - 60, cy + 36, cx + 60, cy + 36) + S.dot(cx - 34, cy + 96, 15) + S.dot(cx + 34, cy + 96, 15)
    return [(CONTOUR, contour + _crown_band()), (DETAIL, detail + _sun_disk(sx, sy + 80, 66) + count)]


def _priest():
    # Ch'alishbal, servant of the sacred: a stepped headdress in the shape of the sacred
    # peak, and a beard
    contour, detail = titled(face="beard")
    x0, y0, x1, y1, w, h, X, Y = _box()
    peak = S.poly([(X(0.3), CROWN_Y - 20), (X(0.3), CROWN_Y + 70), (X(0.42), CROWN_Y + 70), (X(0.42), CROWN_Y + 140),
                   (X(0.54), CROWN_Y + 140), (X(0.54), TOP - 20), (X(0.7), TOP - 20), (X(0.7), CROWN_Y + 140),
                   (X(0.82), CROWN_Y + 140), (X(0.82), CROWN_Y + 70), (X(0.94), CROWN_Y + 70), (X(0.94), CROWN_Y - 60)])
    return [(CONTOUR, contour + peak), (DETAIL, detail + S.dot(X(0.62), CROWN_Y + 170, 16))]


def _scribe():
    # P'ilambal, servant of the glyphs: a brush thrust through his headband, its tip wet
    contour, detail = titled()
    x0, y0, x1, y1, w, h, X, Y = _box()
    (ax, ay), (bx, by) = _at(_band_top(), 0.15), _at(_band_top(), 0.7)
    brush = S.bar(ax - 30, ay - 40, bx + 40, by + 150) + [S.Fill(S._arc(ax - 44, ay - 58, 30, 20, 0, 360)[:-1])]
    return [(CONTOUR, contour + _crown_band()), (DETAIL, detail + brush + R.curl(bx + 70, by + 170, 30, turns=1.0))]


def _herald():
    # Ch'umts'om, the speaking link: two scrolls of speech leaving his lips
    contour, detail = titled()
    x0, y0, x1, y1, w, h, X, Y = _box()
    scrolls = R.curl(X(0.0) - 60, Y(0.48), 46, turns=1.1) + R.curl(X(0.0) - 50, Y(0.2), 40, turns=1.1, clockwise=True)
    scrolls += S.bar(X(0.04), Y(0.42), X(0.0) - 14, Y(0.48)) + S.bar(X(0.05), Y(0.26), X(0.0) - 12, Y(0.2))
    return [(CONTOUR, contour + _crown_band()), (DETAIL, detail + scrolls)]


def _merchant():
    # P'ik'ulmah, the master merchant: the bundle of his trade carried on his back by a
    # strap across his brow
    contour, detail = titled(spool=False)
    x0, y0, x1, y1, w, h, X, Y = _box()
    bundle = S.frame(X(0.6), CROWN_Y - 110, 230, 230, square=2.4)
    strap = S.bar(X(0.22), Y(0.76), X(0.62), CROWN_Y + 20)
    ties = R.x_mark(X(0.6) + 115, CROWN_Y + 10, 42)
    return [(CONTOUR, contour + bundle), (DETAIL, detail + strap + ties)]


def _guildsman():
    # P'ik'ulbal, keeper of a craft: the hammer of his craft crossing his headband
    contour, detail = titled()
    x0, y0, x1, y1, w, h, X, Y = _box()
    (ax, ay), (bx, by) = _at(_band_top(), 0.2), _at(_band_top(), 0.75)
    handle = S.bar(ax - 20, ay - 30, bx + 20, by + 130)
    hx, hy = bx + 20, by + 130
    head = S.poly([(hx - 40, hy + 50), (hx + 70, hy + 10), (hx + 40, hy - 50), (hx - 70, hy - 10), (hx - 40, hy + 50)])
    return [(CONTOUR, contour + _crown_band(False) + head), (DETAIL, detail + handle)]


def _freeman():
    # Nal'ikbal, the independent one: bareheaded, a spring's petal rising over his brow
    contour, detail = titled(spool=False)
    x0, y0, x1, y1, w, h, X, Y = _box()
    petal = S.poly([(X(0.38), CROWN_Y - 40), (X(0.46), CROWN_Y + 170), (X(0.54), CROWN_Y - 40)])
    return [(CONTOUR, contour), (DETAIL, detail + petal)]


def _serf():
    # Ch'ulmaqbal, the bound one: a cord bound round the head and knotted
    contour, detail = titled(spool=False)
    x0, y0, x1, y1, w, h, X, Y = _box()
    bind = S.bar(X(0.1), Y(0.76), X(0.98), Y(0.7)) + S.dot(X(0.72), Y(0.72), 26) + \
        S.bar(X(0.74), Y(0.66), X(0.8), Y(0.46)) + S.bar(X(0.7), Y(0.66), X(0.66), Y(0.46))
    return [(CONTOUR, contour), (DETAIL, detail + bind)]


def _slave():
    # Ts'ik'ibal, the shadowed one: the face netted in shadow
    contour, detail = titled(spool=False)
    x0, y0, x1, y1, w, h, X, Y = _box()
    shadow = R.net(X(0.38), Y(0.18), w * 0.42, h * 0.62)
    return [(CONTOUR, contour), (DETAIL, detail + shadow)]


OVERLORD = Glyph("OVERLORD", "Q'emulmah, the supreme lord", "qe", _overlord)
KING = Glyph("KING", "Ts'enmah, Lord of the Sun", "tse", _king)
PRINCE = Glyph("PRINCE", "Ts'enilbal, heir to the sun", "tse", _prince)
NOBLE = Glyph("NOBLE-LORD", "K'anulmah, a noble of the court", "ka", _noble)
SEATED_LORD = Glyph("SEATED-LORD", "Kulmah, lord of a seat", "ku", _seated_lord)
LADY = Glyph("LADY", "Ish'kanmah, golden noblewoman", "i", _lady)
LANDHOLDER = Glyph("LANDHOLDER", "Ha'nalmah, lord of the land", "ha", _landholder)
KNIGHT = Glyph("KNIGHT", "Ts'omilbal, servant of the bond", "tso", _knight)
WAR_LEADER = Glyph("WAR-LEADER", "Shok'almah, the war-leader", "sho", _war_leader)
SUN_PRIEST = Glyph("SUN-PRIEST", "Ts'enbal, keeper of the count", "tse", _sun_priest)
PRIEST = Glyph("PRIEST", "Ch'alishbal, servant of the sacred", "cha", _priest)
SCRIBE = Glyph("SCRIBE", "P'ilambal, servant of the glyphs", "pi", _scribe)
HERALD = Glyph("HERALD", "Ch'umts'om, the speaking link", "chu", _herald)
MERCHANT = Glyph("MASTER-MERCHANT", "P'ik'ulmah, lord of the trade", "pi", _merchant)
GUILDSMAN = Glyph("GUILDSMAN", "P'ik'ulbal, keeper of a craft", "pi", _guildsman)
FREEMAN = Glyph("FREEMAN", "Nal'ikbal, the independent one", "na", _freeman)
SERF = Glyph("SERF", "Ch'ulmaqbal, the bound one", "chu", _serf)
SLAVE = Glyph("SLAVE", "Ts'ik'ibal, the shadowed one", "tsi", _slave)

RANKS = [OVERLORD, KING, PRINCE, NOBLE, SEATED_LORD, LADY, LANDHOLDER, KNIGHT, WAR_LEADER, SUN_PRIEST, PRIEST,
         SCRIBE, HERALD, MERCHANT, GUILDSMAN, FREEMAN, SERF, SLAVE]
