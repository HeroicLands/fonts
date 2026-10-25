# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Compact forms of the Ch'alish P'ilam ceremonial hand.

    import compact as M

    parts = M.COMPACT["SUN"]()               # [(pen, parts), ...]

A main sign that shares its block with affixes is squeezed into a fraction of it, too
small for its full drawing to be carved. Its compact form is its outline and one
**token**: a solid silhouette of the thing it shows, set in the middle. A solid token is
left raised by the carver and has no grooves of its own, so the only white to cut is the
margin between the token and the outline.

Head glyphs keep their profile, a solid eye, and their token on the crown: the mark of the
office, the sun, the house.
"""

from __future__ import annotations

import math

import ceremonial as R
import strokes as S
from ceremonial import CONTOUR, DETAIL, CX0, CX1, CY0, CY1, C

T = 0.18 * 730  # a token's half size: it fills the middle third of the block


def _poly(pts):
    return [S.Fill(pts)]


# -- tokens: solid silhouettes, centred at (cx, cy), half size r ----------------------------------


def disk(cx, cy, r):
    return S.dot(cx, cy, r * 0.7)


def crescent(cx, cy, r):
    outer = S._arc(cx, cy, r * 0.75, r * 0.75, 60, 300)
    inner = S._arc(cx + r * 0.35, cy, r * 0.55, r * 0.58, 255, 105)
    return _poly(outer + inner)


def star(cx, cy, r):
    pts = []
    for k in range(8):
        a = math.radians(90 + k * 45)
        rr = r * 0.95 if k % 2 == 0 else r * 0.38
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return _poly(pts)


def wave(cx, cy, r):
    top = [(cx - r * 0.85 + 1.7 * r * k / 30, cy + r * 0.15 + r * 0.18 * math.sin(2 * math.pi * 1.5 * k / 30)) for k in range(31)]
    bot = [(x, y - r * 0.4) for x, y in top]
    return _poly(top + bot[::-1])


def stair(cx, cy, r):
    s = r / 1.5
    return _poly([(cx - 1.5 * s, cy - s), (cx - 1.5 * s, cy - s * 0.2), (cx - 0.75 * s, cy - s * 0.2), (cx - 0.75 * s, cy + s * 0.5),
                  (cx, cy + s * 0.5), (cx, cy + s), (cx + 0.75 * s, cy + s), (cx + 0.75 * s, cy - s), (cx + 1.5 * s, cy - s)][:-1]
                 + [(cx + 1.5 * s, cy - s)])


def peak(cx, cy, r):
    return _poly([(cx - r, cy - r * 0.8), (cx - r * 0.55, cy - r * 0.8), (cx - r * 0.55, cy - r * 0.25), (cx - r * 0.2, cy - r * 0.25),
                  (cx - r * 0.2, cy + r * 0.35), (cx + r * 0.2, cy + r * 0.35), (cx + r * 0.2, cy - r * 0.25),
                  (cx + r * 0.55, cy - r * 0.25), (cx + r * 0.55, cy - r * 0.8), (cx + r, cy - r * 0.8)])


def triangle(cx, cy, r):
    return _poly([(cx - r, cy - r * 0.7), (cx, cy + r * 0.85), (cx + r, cy - r * 0.7)])


def square(cx, cy, r):
    return _poly([(cx - r * 0.75, cy - r * 0.75), (cx - r * 0.75, cy + r * 0.75), (cx + r * 0.75, cy + r * 0.75), (cx + r * 0.75, cy - r * 0.75)])


def diamond(cx, cy, r):
    return _poly([(cx, cy + r), (cx + r * 0.8, cy), (cx, cy - r), (cx - r * 0.8, cy)])


def drop(cx, cy, r):
    return _poly(S._arc(cx, cy - r * 0.2, r * 0.6, r * 0.6, 180, 360) + [(cx, cy + r)])


def two_drops(cx, cy, r):
    return drop(cx - r * 0.5, cy, r * 0.75) + drop(cx + r * 0.5, cy, r * 0.75)


def bar(cx, cy, r):
    return [S.Fill(S._capsule(cx - r, cy, cx + r, cy, r * 0.28))]


def two_bars(cx, cy, r):
    return [S.Fill(S._capsule(cx - r * 0.9, cy + r * 0.5, cx + r * 0.9, cy + r * 0.5, r * 0.18)),
            S.Fill(S._capsule(cx - r * 0.9, cy - r * 0.5, cx + r * 0.9, cy - r * 0.5, r * 0.18))]


def three_dots(cx, cy, r):
    return S.dot(cx - r * 0.7, cy, r * 0.24) + S.dot(cx, cy, r * 0.24) + S.dot(cx + r * 0.7, cy, r * 0.24)


def cross(cx, cy, r):
    return [S.Fill(S._capsule(cx - r, cy, cx + r, cy, r * 0.22)), S.Fill(S._capsule(cx, cy - r, cx, cy + r, r * 0.22))]


def x_cross(cx, cy, r):
    d = r * 0.75
    return [S.Fill(S._capsule(cx - d, cy - d, cx + d, cy + d, r * 0.2)), S.Fill(S._capsule(cx - d, cy + d, cx + d, cy - d, r * 0.2))]


def half_up(cx, cy, r):
    return _poly(S._arc(cx, cy - r * 0.4, r * 0.85, r * 0.85, 0, 180)) + [S.Fill(S._capsule(cx - r, cy - r * 0.55, cx + r, cy - r * 0.55, r * 0.15))]


def half_down(cx, cy, r):
    return _poly(S._arc(cx, cy + r * 0.4, r * 0.85, r * 0.85, 180, 360)) + [S.Fill(S._capsule(cx - r, cy + r * 0.55, cx + r, cy + r * 0.55, r * 0.15))]


def roof(cx, cy, r):
    return _poly([(cx - r, cy - r * 0.2), (cx, cy + r * 0.85), (cx + r, cy - r * 0.2)]) + square(cx, cy - r * 0.6, r * 0.45)


def hand(cx, cy, r):
    """A hand in one piece: the palm and two broad fingers grown from it."""
    return _poly([(cx - r * 0.7, cy - r * 0.9), (cx + r * 0.7, cy - r * 0.9), (cx + r * 0.7, cy + r * 0.9),
                  (cx + r * 0.15, cy + r * 0.9), (cx + r * 0.15, cy + r * 0.2), (cx - r * 0.15, cy + r * 0.2),
                  (cx - r * 0.15, cy + r * 0.9), (cx - r * 0.7, cy + r * 0.9)])


def eye(cx, cy, r):
    return _poly(S._arc(cx, cy - r * 0.5, r * 1.0, r * 1.0, 30, 150) + S._arc(cx, cy + r * 0.5, r * 1.0, r * 1.0, 210, 330))


def flame(cx, cy, r):
    return _poly(S._bezier((cx - r * 0.6, cy - r * 0.8), (cx - r * 0.9, cy + r * 0.2), (cx - r * 0.2, cy + r * 0.3), (cx, cy + r))
                 + S._bezier((cx, cy + r), (cx + r * 0.3, cy + r * 0.2), (cx + r * 0.9, cy), (cx + r * 0.6, cy - r * 0.8))[1:])


def skull(cx, cy, r):
    return _poly(S._arc(cx, cy, r * 0.85, r * 0.75, 0, 180) + [(cx + r * 0.85, cy - r * 0.5), (cx - r * 0.85, cy - r * 0.5)])


def bundle(cx, cy, r):
    return square(cx, cy - r * 0.15, r * 0.8) + S.dot(cx, cy + r * 0.85, r * 0.2)


def flower(cx, cy, r):
    """A rosette in one piece: a scalloped disk."""
    pts = []
    for k in range(73):
        a = math.radians(k * 5)
        rr = r * (0.7 + 0.15 * math.cos(6 * a))
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return _poly(pts)


def bird(cx, cy, r):
    return _poly([(cx - r, cy + r * 0.3), (cx, cy - r * 0.3), (cx + r, cy + r * 0.3), (cx, cy - r * 0.05)])


def paw(cx, cy, r):
    """A paw in one piece: the pad with three toes grown from its top."""
    pts = S._arc(cx, cy - r * 0.25, r * 0.6, r * 0.5, 180, 360)
    for k, dx in enumerate((0.45, 0, -0.45)):
        pts += S._arc(cx + r * dx, cy + r * 0.3, r * 0.2, r * 0.3, 0, 180)
    return _poly(pts)


def bolt(cx, cy, r):
    return _poly([(cx - r * 0.2, cy + r), (cx + r * 0.4, cy + r * 0.1), (cx, cy + r * 0.1), (cx + r * 0.3, cy - r),
                  (cx - r * 0.4, cy - r * 0.1), (cx, cy - r * 0.1)])


# -- compact forms -------------------------------------------------------------------------------


def _outline(glyph):
    """A glyph's outline: the first part its drawing lists, the cushion or the profile."""
    for pen, parts in glyph.draw():
        return pen, parts[0]


def motif_compact(glyph, motif, scale=0.95):
    """The compact form of a sign in a cushion, cartouche or roof: its outline and the
    syllabary's line motif of its concept (syllabary.py), drawn at ``scale`` of the token's
    size. Each motif's scale is the largest at which the sign stays carvable in every
    layout (``compact_sweep.py --fit`` finds it)."""
    def draw():
        pen, outline = _outline(glyph)
        return [(pen, [outline]), (DETAIL, motif(C, C, T * scale))]
    return draw


def compact(glyph, token, head=False, at=(C, C), size=0.22):
    """The compact form of ``glyph``: its outline, and ``token`` at ``at``. A head glyph
    keeps a solid eye and sets its token on the crown, ``size`` of the head's shorter side
    across."""
    def draw():
        pen, outline = _outline(glyph)
        if head:
            x0, y0, x1, y1 = (min(p[0] for p in outline.pts), min(p[1] for p in outline.pts),
                              max(p[0] for p in outline.pts), max(p[1] for p in outline.pts))
            w, h = x1 - x0, y1 - y0
            eye = S.dot(x0 + 0.3 * w, y0 + 0.56 * h, min(w, h) * 0.07)
            mark = token(x0 + 0.68 * w, y0 + 0.44 * h, min(w, h) * size) if token else []
            return [(pen, [outline]), (DETAIL, eye), (DETAIL, mark)]
        return [(pen, [outline]), (DETAIL, token(at[0], at[1], T))]
    return draw
