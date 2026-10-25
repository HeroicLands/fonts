# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""The Ch'alish P'ilam ceremonial syllabary: the signs that write sound.

    import syllabary as Y

    Y.SIGNS["ka1"].flat()                     # [(pen, parts), ...] in a box B * SPAN wide, B * AFFIX high
    Y.SIGNS["ka1"].tall()                     # the same sign in a box B * AFFIX wide, B * SPAN high

Every syllable Ki'i'chek uses is written by one to three signs. A sign is the reduced
picture of a word that opens with its syllable, or for the seventeen syllables no word
opens on, a picture carrying a traditional sound. Each sign is one **motif**, drawn into
whatever box it is given, and its two forms are that motif inside a flat oblong, to set
above or below a main sign, or a tall one, to set before or after it. Repeated elements
run along the long side of the box; a picture stays square and centred.

The sources follow thalorna's syllabary report: ``SOURCES`` lists each syllable's signs
in order, so ``ka1`` is the flame, ``ka2`` the coal and ``ka3`` the eye.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable

import ceremonial as R
import strokes as S
from ceremonial import CONTOUR, DETAIL, B

AFFIX = 0.34  # a flat sign's height and a tall sign's width, as a share of the block
SPAN = 0.62  # a flat sign's width and a tall sign's height: shorter than the sign it sits by
PAD = R.CONTOUR.full / 2 + R.GAP + 2  # the white between an oblong's line and its motif
STRETCH = 1.8  # how far a picture may lie along a flat or tall slot, out of its own proportions


# -- the box a motif draws in --------------------------------------------------------------------


@dataclass(frozen=True)
class Box:
    x0: float
    y0: float
    x1: float
    y1: float

    @property
    def w(self):
        return self.x1 - self.x0

    @property
    def h(self):
        return self.y1 - self.y0

    @property
    def cx(self):
        return (self.x0 + self.x1) / 2

    @property
    def cy(self):
        return (self.y0 + self.y1) / 2

    @property
    def flat(self):
        return self.w >= self.h

    @property
    def s(self):
        """The side of the square centred in the box."""
        return min(self.w, self.h)

    def along(self, n, i):
        """The centre of the ``i``th of ``n`` places spread along the long side."""
        if self.flat:
            return self.x0 + self.w * (i + 0.5) / n, self.cy
        return self.cx, self.y1 - self.h * (i + 0.5) / n

    def square(self, k=1.0):
        """The square of side ``s * k`` centred in the box, as a Box."""
        half = self.s * k / 2
        return Box(self.cx - half, self.cy - half, self.cx + half, self.cy + half)


# -- motifs: each draws one picture into a box, in the detail brush ---------------------------------


def dots(n, r=None):
    def m(b):
        rr = r or min(b.s * 0.22, 26)
        return [f for i in range(n) for f in S.dot(*b.along(n, i), rr)]
    return m


def rings(n):
    def m(b):
        rr = min(b.s * 0.3, b.w / n * 0.3 if b.flat else b.h / n * 0.3)
        rr = max(rr, 26)
        return [t for i in range(n) for t in S.ring(*b.along(n, i), rr)]
    return m


def bars(n):
    """Bars across the short side, spread along the long one: the count's fives."""
    def m(b):
        out = []
        for i in range(n):
            x, y = b.along(n, i)
            if b.flat:
                out.append(S.Fill(S._capsule(x, b.y0 + 6, x, b.y1 - 6, 13)))
            else:
                out.append(S.Fill(S._capsule(b.x0 + 6, y, b.x1 - 6, y, 13)))
        return out
    return m


def bar_dots(nbars, ndots):
    """A count: bars, then dots, along the box."""
    def m(b):
        n = nbars + ndots
        out = []
        for i in range(n):
            x, y = b.along(n, i)
            if i < nbars:
                if b.flat:
                    out.append(S.Fill(S._capsule(x, b.y0 + 6, x, b.y1 - 6, 13)))
                else:
                    out.append(S.Fill(S._capsule(b.x0 + 6, y, b.x1 - 6, y, 13)))
            else:
                out += S.dot(x, y, min(b.s * 0.2, 22))
        return out
    return m


def crosses(n):
    def m(b):
        out = []
        for i in range(n):
            x, y = b.along(n, i)
            r = min(b.s * 0.32, (b.w if b.flat else b.h) / n * 0.32)
            out += R.x_mark(x, y, r)
        return out
    return m


def waves(n=2):
    def m(b):
        out = []
        for i in range(n):
            if b.flat:
                y = b.y0 + b.h * (i + 0.5) / n
                out += S.wave(b.x0 + b.w * 0.12, y, b.x1 - b.w * 0.12, min(b.h / n * 0.26, 18), 2.0)
            else:
                x = b.x0 + b.w * (i + 0.5) / n
                pts = [(x + min(b.w / n * 0.26, 18) * math.sin(2 * math.pi * 2 * k / 40), b.y0 + b.h * 0.12 + b.h * 0.76 * k / 40)
                       for k in range(41)]
                out += [S.Track(pts)]
        return out
    return m


def net(b):
    ix, iy = b.w * 0.12, b.h * 0.12
    return R.net(b.x0 + ix, b.y0 + iy, b.w - 2 * ix, b.h - 2 * iy)


def zigzag(b):
    n = 4
    pts = []
    for k in range(n * 2 + 1):
        t = k / (n * 2)
        if b.flat:
            pts.append((b.x0 + b.w * t, b.y0 + 8 if k % 2 == 0 else b.y1 - 8))
        else:
            pts.append((b.x0 + 8 if k % 2 == 0 else b.x1 - 8, b.y0 + b.h * t))
    return S.poly(pts)


def comb(b):
    """A row of teeth: legs, a fringe, grass."""
    n = 4
    out = S.bar(b.x0, b.y1 - 6, b.x1, b.y1 - 6) if b.flat else S.bar(b.x0 + 6, b.y0, b.x0 + 6, b.y1)
    for i in range(n):
        x, y = b.along(n, i)
        if b.flat:
            out += S.bar(x, b.y1 - 6, x, b.y0 + 8)
        else:
            out += S.bar(b.x0 + 6, y, b.x1 - 8, y)
    return out


def scallops(b):
    """The comb fringe: touching U-loops."""
    if b.flat:
        return R.fringe(b.x0, b.x1, b.y1 - 6, h=b.h * 0.6)
    out = S.bar(b.x0 + 6, b.y0, b.x0 + 6, b.y1)
    n = max(3, round(b.h / 70))
    for i in range(n):
        out += S.arc(b.x0 + 6, b.y0 + b.h * (i + 0.5) / n, b.w * 0.6, b.h / n / 2, 270, 450)
    return out


def chevrons(b):
    out = []
    for i in range(3):
        x, y = b.along(3, i)
        r = min(b.s * 0.32, 40)
        if b.flat:
            out += S.poly([(x - r * 0.6, y + r), (x + r * 0.6, y), (x - r * 0.6, y - r)])
        else:
            out += S.poly([(x - r, y + r * 0.6), (x, y - r * 0.6), (x + r, y + r * 0.6)])
    return out


def stairs(b):
    n = 3 if b.flat else 2  # a narrow slot has room for two steps
    ix, iy = b.w * 0.18, b.h * 0.22
    x0, y0, w, h = b.x0 + ix, b.y0 + iy, b.w - 2 * ix, b.h - 2 * iy
    pts = [(x0, y0)]
    for k in range(n):
        y = y0 + h * (k + 1) / n
        pts += [(x0 + w * k / n, y), (x0 + w * (k + 1) / n, y)]
    pts.append((x0 + w, y0))
    return S.poly(pts)


def knots(b):
    """A cord with knots tied along it."""
    out = S.bar(b.x0 + 4, b.cy, b.x1 - 4, b.cy) if b.flat else S.bar(b.cx, b.y0 + 4, b.cx, b.y1 - 4)
    for i in range(3):
        out += S.dot(*b.along(3, i), min(b.s * 0.24, 24))
    return out


def ticks(b):
    """A line with short marks along it: a border, an edge."""
    if b.flat:
        y = b.y0 + b.h * 0.25
        out = S.bar(b.x0 + b.w * 0.08, y, b.x1 - b.w * 0.08, y)
        for i in range(3):
            x, _ = b.along(3, i)
            out += S.bar(x, y, x, b.y1 - b.h * 0.15)
        return out
    x = b.x0 + b.w * 0.25
    out = S.bar(x, b.y0 + b.h * 0.08, x, b.y1 - b.h * 0.08)
    for i in range(3):
        _, y = b.along(3, i)
        out += S.bar(x, y, b.x1 - b.w * 0.15, y)
    return out


def curls(n):
    def m(b):
        out = []
        for i in range(n):
            x, y = b.along(n, i)
            out += R.curl(x, y, min(b.s * 0.38, (b.w if b.flat else b.h) / n * 0.4), turns=1.0, clockwise=bool(i % 2))
        return out
    return m


# pictures, drawn in the box's centred square


def P(fn, k=0.92):
    """A picture drawn in the centred square of side ``s * k``, then stretched along the
    box's long side by up to ``STRETCH``, so it lies along a flat or tall slot."""
    def m(b):
        q = b.square(k)
        parts = fn(q.cx, q.cy, q.s / 2)
        long_ = b.w if b.flat else b.h
        f = min(STRETCH, (long_ * 0.8) / q.s)
        out = []
        for part in parts:
            if b.flat:
                pts = [(b.cx + (x - b.cx) * f, y) for x, y in part.pts]
            else:
                pts = [(x, b.cy + (y - b.cy) * f) for x, y in part.pts]
            out.append(S.Fill(pts) if isinstance(part, S.Fill) else S.Track(pts, closed=part.closed, weight=part.weight))
        return out
    return m


def crescent(cx, cy, r):
    return S.arc(cx - r * 0.1, cy, r * 0.9, r * 0.9, 60, 300) + S.arc(cx + r * 0.35, cy, r * 0.6, r * 0.65, 95, 265)


def star4(cx, cy, r):
    pts = []
    for k in range(9):
        a = math.radians(90 + k * 45)
        rr = r * 0.95 if k % 2 == 0 else r * 0.36
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return S.poly(pts)


def spots(cx, cy, r):
    return S.ring(cx - r * 0.45, cy + r * 0.3, r * 0.42) + S.dot(cx + r * 0.5, cy - r * 0.35, r * 0.24)


def ring_dot(cx, cy, r):
    return S.ring(cx, cy, r * 0.8) + S.dot(cx, cy, r * 0.25)


def drop(cx, cy, r):
    return [S.Track(S._bezier((cx, cy + r * 0.9), (cx + r * 0.3, cy + r * 0.3), (cx + r * 0.75, cy - r * 0.2), (cx, cy - r * 0.85))
                    + S._bezier((cx, cy - r * 0.85), (cx - r * 0.75, cy - r * 0.2), (cx - r * 0.3, cy + r * 0.3), (cx, cy + r * 0.9))[1:])]


def ember(cx, cy, r):
    return S.ring(cx, cy, r * 0.8) + R.x_mark(cx, cy, r * 0.4)


def almond_eye(cx, cy, r):
    return S.arc(cx, cy - r * 0.9, r * 1.1, r * 1.2, 50, 130) + S.arc(cx, cy + r * 0.9, r * 1.1, r * 1.2, 230, 310) + \
        S.dot(cx, cy, r * 0.25)


def three_dots_ring(cx, cy, r):
    """All: four dots set in a square, every quarter."""
    return [f for dx, dy in ((-0.5, -0.5), (0.5, -0.5), (-0.5, 0.5), (0.5, 0.5)) for f in S.dot(cx + r * dx, cy + r * dy, r * 0.2)]


def key(cx, cy, r):
    return S.ring(cx - r * 0.45, cy, r * 0.42) + S.bar(cx - r * 0.03, cy, cx + r * 0.9, cy) + \
        S.bar(cx + r * 0.5, cy, cx + r * 0.5, cy - r * 0.45) + S.bar(cx + r * 0.85, cy, cx + r * 0.85, cy - r * 0.45)


def light(cx, cy, r):
    return S.dot(cx, cy + r * 0.6, r * 0.22) + S.bar(cx - r * 0.25, cy + r * 0.25, cx - r * 0.85, cy - r * 0.85) + \
        S.bar(cx + r * 0.25, cy + r * 0.25, cx + r * 0.85, cy - r * 0.85)


def hanging_cords(cx, cy, r):
    out = S.bar(cx - r * 0.85, cy + r * 0.8, cx + r * 0.85, cy + r * 0.8)
    for dx in (-0.55, 0, 0.55):
        out += S.bar(cx + r * dx, cy + r * 0.8, cx + r * dx, cy - r * 0.85) + S.dot(cx + r * dx, cy - r * 0.1, r * 0.17)
    return out


def cracked_stone(cx, cy, r):
    return S.poly([(cx - r * 0.85, cy - r * 0.6), (cx + r * 0.85, cy - r * 0.6), (cx + r * 0.7, cy + r * 0.6),
                   (cx - r * 0.6, cy + r * 0.75), (cx - r * 0.85, cy - r * 0.6)]) + \
        S.poly([(cx - r * 0.05, cy + r * 0.7), (cx + r * 0.1, cy), (cx - r * 0.15, cy - r * 0.55)])


def heart(cx, cy, r):
    return [S.Track(S._arc(cx - r * 0.4, cy + r * 0.25, r * 0.45, r * 0.45, 0, 200)
                    + [(cx, cy - r * 0.85)] + S._arc(cx + r * 0.4, cy + r * 0.25, r * 0.45, r * 0.45, -20, 180))]


def serpent(cx, cy, r):
    pts = [(cx - r * 0.85 + r * 1.7 * k / 40, cy + r * 0.35 * math.sin(2 * math.pi * 1.5 * k / 40)) for k in range(41)]
    return [S.Track(pts)] + S.dot(cx - r * 0.85, cy, r * 0.2)


def low(cx, cy, r):
    return S.bar(cx - r * 0.85, cy + r * 0.3, cx + r * 0.85, cy + r * 0.3) + S.dot(cx, cy - r * 0.4, r * 0.24)


def above(cx, cy, r):
    return S.bar(cx - r * 0.85, cy - r * 0.3, cx + r * 0.85, cy - r * 0.3) + S.dot(cx, cy + r * 0.4, r * 0.24)


def legs(cx, cy, r):
    out = S.bar(cx - r * 0.85, cy + r * 0.3, cx + r * 0.85, cy + r * 0.3)
    for dx in (-0.7, 0, 0.7):
        out += S.bar(cx + r * dx, cy + r * 0.3, cx + r * dx, cy - r * 0.85)
    return out


def worm(cx, cy, r):
    return R.curl(cx - r * 0.35, cy + r * 0.25, r * 0.5, turns=0.9) + R.curl(cx + r * 0.35, cy - r * 0.25, r * 0.5, turns=0.9, clockwise=True)


def mound(cx, cy, r):
    return S.arc(cx, cy - r * 0.6, r * 0.95, r * 1.2, 15, 165) + S.bar(cx - r * 0.95, cy - r * 0.6, cx + r * 0.95, cy - r * 0.6)


def bundle_x(cx, cy, r):
    """A gift: a bundle tied with a knot on top."""
    return S.frame(cx - r * 0.75, cy - r * 0.75, r * 1.5, r * 1.1, square=2.4) + S.dot(cx, cy + r * 0.45, r * 0.2) + \
        S.bar(cx, cy + r * 0.55, cx - r * 0.35, cy + r * 0.9) + S.bar(cx, cy + r * 0.55, cx + r * 0.35, cy + r * 0.9)


def scroll(cx, cy, r):
    return R.curl(cx + r * 0.25, cy + r * 0.2, r * 0.6, turns=1.1) + S.bar(cx - r * 0.85, cy - r * 0.6, cx + r * 0.1, cy - r * 0.2)


def chevron(cx, cy, r):
    return S.poly([(cx - r * 0.5, cy + r * 0.8), (cx + r * 0.6, cy), (cx - r * 0.5, cy - r * 0.8)])


def shell(cx, cy, r):
    return S.arc(cx, cy + r * 0.2, r * 0.9, r * 0.95, 200, 340) + S.bar(cx - r * 0.85, cy + r * 0.15, cx + r * 0.85, cy + r * 0.15) + \
        S.bar(cx - r * 0.3, cy + r * 0.05, cx - r * 0.35, cy - r * 0.55) + S.bar(cx + r * 0.3, cy + r * 0.05, cx + r * 0.35, cy - r * 0.55)


def tent(cx, cy, r):
    return S.poly([(cx - r * 0.9, cy - r * 0.7), (cx, cy + r * 0.85), (cx + r * 0.9, cy - r * 0.7)])


def sun(cx, cy, r):
    out = S.ring(cx, cy, r * 0.5)
    for k in range(4):
        a = math.radians(45 + k * 90)
        out += S.bar(cx + r * 0.68 * math.cos(a), cy + r * 0.68 * math.sin(a), cx + r * 0.95 * math.cos(a), cy + r * 0.95 * math.sin(a))
    return out


def day(cx, cy, r):
    return S.ring(cx, cy, r * 0.85) + S.bar(cx - r * 0.85, cy, cx + r * 0.85, cy) + S.dot(cx, cy + r * 0.4, r * 0.18)


def cup(cx, cy, r):
    return S.poly([(cx - r * 0.65, cy + r * 0.75), (cx - r * 0.4, cy - r * 0.8), (cx + r * 0.4, cy - r * 0.8), (cx + r * 0.65, cy + r * 0.75)])


def ears(cx, cy, r):
    return S.poly([(cx - r * 0.85, cy + r * 0.85), (cx - r * 0.3, cy + r * 0.2), (cx + r * 0.3, cy + r * 0.2), (cx + r * 0.85, cy + r * 0.85)]) + \
        S.poly([(cx - r * 0.3, cy + r * 0.2), (cx, cy - r * 0.85), (cx + r * 0.3, cy + r * 0.2)])


def plume(cx, cy, r):
    return S.arc(cx + r * 0.9, cy + r * 0.9, r * 1.6, r * 1.7, 180, 270) + S.ring(cx - r * 0.7, cy + r * 0.7, r * 0.22)


def table(cx, cy, r):
    return S.bar(cx - r * 0.9, cy + r * 0.3, cx + r * 0.9, cy + r * 0.3) + S.bar(cx - r * 0.6, cy + r * 0.3, cx - r * 0.6, cy - r * 0.8) + \
        S.bar(cx + r * 0.6, cy + r * 0.3, cx + r * 0.6, cy - r * 0.8)


def tufts(cx, cy, r):
    out = S.bar(cx - r * 0.9, cy - r * 0.6, cx + r * 0.9, cy - r * 0.6)
    for dx in (-0.5, 0.5):
        out.append(S.Fill([(cx + r * (dx - 0.2), cy - r * 0.6), (cx + r * dx, cy + r * 0.7), (cx + r * (dx + 0.2), cy - r * 0.6)]))
    return out


def diamond(n):
    """A diamond holding ``n`` dots in a row: a place of the count."""
    def d(cx, cy, r):
        out = S.poly([(cx, cy + r * 0.9), (cx + r * 0.9, cy), (cx, cy - r * 0.9), (cx - r * 0.9, cy), (cx, cy + r * 0.9)])
        for k in range(n):
            out += S.dot(cx + r * 0.32 * (k - (n - 1) / 2), cy, r * 0.11)
        return out
    return d


def palm(cx, cy, r):
    out = S.frame(cx - r * 0.75, cy - r * 0.85, r * 1.5, r * 0.8, square=2.4)
    for dx in (-0.5, 0.5):
        out += S.bar(cx + r * dx, cy - r * 0.05, cx + r * dx, cy + r * 0.85)
    return out


def clay(cx, cy, r):
    return [S.Track(S._arc(cx, cy, r * 0.85, r * 0.6, 0, 360), closed=True)] + S.dot(cx, cy, r * 0.2)


def needle(cx, cy, r):
    return S.bar(cx - r * 0.85, cy - r * 0.6, cx + r * 0.45, cy + r * 0.35) + S.dot(cx + r * 0.6, cy + r * 0.48, r * 0.2)


def dome_night(cx, cy, r):
    return S.arc(cx, cy - r * 0.7, r * 0.95, r * 1.5, 0, 180) + S.bar(cx - r * 0.95, cy - r * 0.7, cx + r * 0.95, cy - r * 0.7) + \
        S.dot(cx - r * 0.3, cy - r * 0.15, r * 0.14) + S.dot(cx + r * 0.3, cy - r * 0.15, r * 0.14)


def mesa(cx, cy, r):
    return S.poly([(cx - r * 0.95, cy - r * 0.7), (cx - r * 0.5, cy + r * 0.6), (cx + r * 0.5, cy + r * 0.6), (cx + r * 0.95, cy - r * 0.7)])


def corner_dot(cx, cy, r):
    return S.corner(cx - r * 0.85, cy + r * 0.8, cx + r * 0.8, cy - r * 0.85) + S.dot(cx + r * 0.25, cy + r * 0.25, r * 0.2)


def supreme(cx, cy, r):
    return S.bar(cx - r * 0.85, cy - r * 0.6, cx + r * 0.85, cy - r * 0.6) + S.dot(cx, cy, r * 0.2) + S.dot(cx, cy + r * 0.6, r * 0.2)


def you(cx, cy, r):
    return S.ring(cx - r * 0.35, cy + r * 0.4, r * 0.38) + S.bar(cx - r * 0.35, cy, cx - r * 0.35, cy - r * 0.9) + \
        S.bar(cx + r * 0.05, cy + r * 0.4, cx + r * 0.9, cy + r * 0.4)


def quarter(up):
    def q(cx, cy, r):
        y = cy + (r * 0.55 if up else -r * 0.55)
        return S.bar(cx, cy - r * 0.3 if up else cy + r * 0.3, cx, y) + S.bar(cx - r * 0.85, cy, cx + r * 0.85, cy) + \
            S.dot(cx, y + (r * 0.2 if up else -r * 0.2), r * 0.2)
    return q


def furrows(cx, cy, r):
    out = S.bar(cx - r * 0.9, cy + r * 0.5, cx + r * 0.9, cy + r * 0.5)
    for dx in (-0.55, 0, 0.55):
        out += S.arc(cx + r * dx, cy - r * 0.1, r * 0.25, r * 0.28, 200, 340)
    return out


def eagle(cx, cy, r):
    return S.poly([(cx - r * 0.95, cy + r * 0.7), (cx, cy - r * 0.2), (cx + r * 0.95, cy + r * 0.7)]) + S.dot(cx, cy - r * 0.55, r * 0.2)


def bird(cx, cy, r):
    return S.arc(cx - r * 0.45, cy - r * 0.2, r * 0.45, r * 0.55, 20, 160) + S.arc(cx + r * 0.45, cy - r * 0.2, r * 0.45, r * 0.55, 20, 160)


def seed(cx, cy, r):
    return [S.Track(S._arc(cx, cy, r * 0.55, r * 0.85, 0, 360), closed=True)] + S.dot(cx, cy, r * 0.18)


def tree(cx, cy, r):
    return S.bar(cx, cy - r * 0.9, cx, cy + r * 0.9) + S.bar(cx, cy + r * 0.1, cx - r * 0.7, cy + r * 0.7) + \
        S.bar(cx, cy - r * 0.2, cx + r * 0.7, cy + r * 0.4)


def crossed(cx, cy, r):
    return S.bar(cx - r * 0.85, cy - r * 0.85, cx + r * 0.85, cy + r * 0.85) + S.bar(cx - r * 0.85, cy + r * 0.85, cx + r * 0.85, cy - r * 0.85)


def door(cx, cy, r):
    return S.poly([(cx - r * 0.85, cy - r * 0.85), (cx - r * 0.85, cy + r * 0.85), (cx + r * 0.85, cy + r * 0.85), (cx + r * 0.85, cy - r * 0.85)]) + \
        S.bar(cx - r * 0.85, cy - r * 0.05, cx + r * 0.85, cy - r * 0.05)


def roof_dot(cx, cy, r):
    return tent(cx, cy, r) + S.dot(cx, cy - r * 0.3, r * 0.2)


def room(cx, cy, r):
    return S.poly([(cx - r * 0.85, cy - r * 0.85), (cx - r * 0.85, cy + r * 0.85), (cx + r * 0.85, cy + r * 0.85), (cx + r * 0.85, cy - r * 0.85), (cx - r * 0.85, cy - r * 0.85)]) + \
        S.dot(cx, cy, r * 0.25)


def pot(cx, cy, r):
    return S.arc(cx, cy - r * 0.15, r * 0.75, r * 0.7, 120, 420) + S.bar(cx - r * 0.5, cy + r * 0.85, cx + r * 0.5, cy + r * 0.85)


def lord(cx, cy, r):
    return S.ring(cx, cy - r * 0.35, r * 0.45) + S.tick(cx - r * 0.45, cy + r * 0.15, r * 0.7, angle=125) + \
        S.tick(cx + r * 0.45, cy + r * 0.15, r * 0.7, angle=55)


def mouth(cx, cy, r):
    return S.ring(cx, cy, r * 0.8)


def womb(cx, cy, r):
    return S.arc(cx, cy + r * 0.2, r * 0.8, r * 0.95, 190, 350) + S.dot(cx, cy + r * 0.3, r * 0.2)


def jar(cx, cy, r):
    return [S.Track(S._bezier((cx - r * 0.3, cy + r * 0.85), (cx - r * 0.95, cy + r * 0.3), (cx - r * 0.8, cy - r * 0.85), (cx, cy - r * 0.85))
                    + S._bezier((cx, cy - r * 0.85), (cx + r * 0.8, cy - r * 0.85), (cx + r * 0.95, cy + r * 0.3), (cx + r * 0.3, cy + r * 0.85))[1:])]


def self_(cx, cy, r):
    return S.ring(cx, cy + r * 0.45, r * 0.38) + S.bar(cx, cy + r * 0.07, cx, cy - r * 0.9)


def bear(cx, cy, r):
    return S.arc(cx, cy - r * 0.5, r * 0.9, r * 1.0, 0, 180) + S.bar(cx - r * 0.9, cy - r * 0.5, cx + r * 0.9, cy - r * 0.5) + \
        S.ring(cx - r * 0.55, cy + r * 0.55, r * 0.22) + S.ring(cx + r * 0.55, cy + r * 0.55, r * 0.22)


def peaks(cx, cy, r):
    return S.poly([(cx - r * 0.95, cy - r * 0.6), (cx - r * 0.45, cy + r * 0.6), (cx, cy - r * 0.1), (cx + r * 0.45, cy + r * 0.7), (cx + r * 0.95, cy - r * 0.6)])


def river(cx, cy, r):
    return S.bar(cx - r * 0.9, cy + r * 0.6, cx + r * 0.9, cy + r * 0.6) + S.bar(cx - r * 0.9, cy - r * 0.6, cx + r * 0.9, cy - r * 0.6) + \
        S.wave(cx - r * 0.75, cy, cx + r * 0.75, r * 0.2, 1.5)


def bowl(cx, cy, r):
    return S.arc(cx, cy + r * 0.3, r * 0.9, r * 0.9, 200, 340) + S.bar(cx - r * 0.85, cy + r * 0.0, cx + r * 0.85, cy + r * 0.0)


def mirror(cx, cy, r):
    return S.ring(cx, cy, r * 0.85) + S.dot(cx - r * 0.3, cy + r * 0.3, r * 0.16)


def sky(cx, cy, r):
    return S.arc(cx, cy - r * 0.6, r * 0.9, r * 1.4, 0, 180) + S.bar(cx - r * 0.95, cy - r * 0.6, cx + r * 0.95, cy - r * 0.6) + \
        S.dot(cx, cy + r * 0.1, r * 0.2)


def pierced_beads(cx, cy, r):
    return S.ring(cx - r * 0.5, cy, r * 0.38) + S.ring(cx + r * 0.5, cy, r * 0.38)


def quincunx(cx, cy, r):
    return [f for dx, dy in ((0, 0), (-0.6, -0.6), (0.6, -0.6), (-0.6, 0.6), (0.6, 0.6)) for f in S.dot(cx + r * dx, cy + r * dy, r * 0.17)]


def blade(cx, cy, r):
    return S.arc(cx + r * 0.9, cy, r * 1.25, r * 0.95, 140, 220) + S.arc(cx - r * 0.9, cy, r * 1.25, r * 0.95, -40, 40) + \
        S.bar(cx, cy - r * 0.8, cx, cy + r * 0.8)


def obsidian_mirror(cx, cy, r):
    return S.ring(cx, cy, r * 0.85) + R.x_mark(cx, cy, r * 0.42)


def quill(cx, cy, r):
    out = S.bar(cx - r * 0.3, cy - r * 0.9, cx - r * 0.3, cy + r * 0.9)
    for k in range(2):
        y = cy - r * 0.35 + k * r * 0.65
        out += S.bar(cx - r * 0.3, y, cx + r * 0.6, y + r * 0.35)
    return out


def three_plumes(cx, cy, r):
    out = []
    for dx in (-0.6, 0.6):
        out += S.arc(cx + r * dx + r * 0.25, cy - r * 0.8, r * 0.25, r * 1.6, 90, 180)
    return out


def drum(cx, cy, r):
    return S.poly([(cx - r * 0.65, cy + r * 0.8), (cx - r * 0.45, cy - r * 0.85), (cx + r * 0.45, cy - r * 0.85), (cx + r * 0.65, cy + r * 0.8), (cx - r * 0.65, cy + r * 0.8)]) + \
        S.bar(cx - r * 0.6, cy + r * 0.25, cx + r * 0.6, cy + r * 0.25)


def rattle(cx, cy, r):
    return S.ring(cx, cy + r * 0.3, r * 0.5) + S.bar(cx, cy - r * 0.2, cx, cy - r * 0.9) + S.dot(cx, cy + r * 0.3, r * 0.15)


def turtle(cx, cy, r):
    return S.arc(cx, cy - r * 0.3, r * 0.85, r * 1.0, 0, 180) + S.bar(cx - r * 0.95, cy - r * 0.3, cx + r * 0.95, cy - r * 0.3) + \
        S.bar(cx, cy - r * 0.3, cx, cy + r * 0.65)


def carapace(cx, cy, r):
    return S.ring(cx, cy, r * 0.85) + S.bar(cx - r * 0.85, cy, cx + r * 0.85, cy) + S.bar(cx, cy - r * 0.85, cx, cy + r * 0.85)


def canoe(cx, cy, r):
    return S.arc(cx, cy + r * 0.6, r * 0.95, r * 0.95, 200, 340) + S.bar(cx - r * 0.95, cy + r * 0.25, cx + r * 0.95, cy + r * 0.25)


def footprint(cx, cy, r):
    return [S.Track(S._arc(cx, cy - r * 0.15, r * 0.4, r * 0.7, 0, 360), closed=True)] + S.dot(cx - r * 0.15, cy + r * 0.75, r * 0.14) + \
        S.dot(cx + r * 0.22, cy + r * 0.72, r * 0.13)


def incense(cx, cy, r):
    out = S.arc(cx, cy - r * 0.3, r * 0.75, r * 0.55, 200, 340)
    for dx in (-0.3, 0.3):
        pts = [(cx + r * dx + r * 0.15 * math.sin(2 * math.pi * k / 20 * 1.5), cy - r * 0.3 + r * 1.15 * k / 20) for k in range(21)]
        out += [S.Track(pts)]
    return out


def censer(cx, cy, r):
    return pot(cx, cy, r) + S.dot(cx - r * 0.3, cy - r * 0.15, r * 0.13) + S.dot(cx + r * 0.3, cy - r * 0.15, r * 0.13)


def mat(cx, cy, r):
    out = S.poly([(cx - r * 0.85, cy - r * 0.85), (cx - r * 0.85, cy + r * 0.85), (cx + r * 0.85, cy + r * 0.85), (cx + r * 0.85, cy - r * 0.85), (cx - r * 0.85, cy - r * 0.85)])
    out += S.bar(cx, cy - r * 0.85, cx, cy + r * 0.85) + S.bar(cx - r * 0.85, cy, cx + r * 0.85, cy)
    return out


def throne(cx, cy, r):
    return S.poly([(cx - r * 0.85, cy + r * 0.9), (cx - r * 0.85, cy - r * 0.85), (cx + r * 0.85, cy - r * 0.85)]) + \
        S.bar(cx - r * 0.85, cy - r * 0.1, cx + r * 0.6, cy - r * 0.1)


def heap(cx, cy, r):
    return S.dot(cx - r * 0.45, cy - r * 0.35, r * 0.22) + S.dot(cx + r * 0.45, cy - r * 0.35, r * 0.22) + S.dot(cx, cy + r * 0.4, r * 0.22)


def tied(cx, cy, r):
    return S.frame(cx - r * 0.75, cy - r * 0.85, r * 1.5, r * 1.3, square=2.4) + S.dot(cx, cy + r * 0.6, r * 0.2)


def ball(cx, cy, r):
    return S.ring(cx, cy, r * 0.85) + S.bar(cx - r * 0.85, cy, cx + r * 0.85, cy)


def court(cx, cy, r):
    return S.bar(cx - r * 0.85, cy + r * 0.75, cx + r * 0.85, cy + r * 0.75) + S.bar(cx - r * 0.85, cy - r * 0.75, cx + r * 0.85, cy - r * 0.75) + \
        S.bar(cx, cy - r * 0.75, cx, cy + r * 0.75)


def monkey(cx, cy, r):
    return S.ring(cx - r * 0.35, cy + r * 0.5, r * 0.3) + S.bar(cx - r * 0.35, cy + r * 0.2, cx - r * 0.35, cy - r * 0.2) + \
        R.curl(cx + r * 0.25, cy - r * 0.45, r * 0.4, turns=0.9)


def arts(cx, cy, r):
    return R.curl(cx - r * 0.3, cy, r * 0.5, turns=0.9) + S.dot(cx + r * 0.45, cy + r * 0.45, r * 0.15) + S.dot(cx + r * 0.6, cy - r * 0.1, r * 0.15)


def bat(cx, cy, r):
    return S.dot(cx, cy, r * 0.2) + S.poly([(cx - r * 0.25, cy), (cx - r * 0.95, cy + r * 0.7), (cx - r * 0.75, cy - r * 0.5), (cx - r * 0.25, cy)]) + \
        S.poly([(cx + r * 0.25, cy), (cx + r * 0.95, cy + r * 0.7), (cx + r * 0.75, cy - r * 0.5), (cx + r * 0.25, cy)])


def burial(cx, cy, r):
    return S.arc(cx, cy + r * 0.3, r * 0.95, r * 1.1, 195, 345) + S.dot(cx, cy - r * 0.05, r * 0.22)


def capture(cx, cy, r):
    return palm(cx, cy + r * 0.2, r * 0.7) + S.wave(cx - r * 0.85, cy - r * 0.65, cx + r * 0.85, r * 0.15, 1.5)


def hummingbird(cx, cy, r):
    return S.ring(cx + r * 0.35, cy, r * 0.32) + S.bar(cx, cy + r * 0.05, cx - r * 0.9, cy + r * 0.2)


def soul(cx, cy, r):
    return R.curl(cx, cy, r * 0.6, turns=1.0) + S.dot(cx - r * 0.7, cy + r * 0.7, r * 0.14) + S.dot(cx + r * 0.7, cy - r * 0.7, r * 0.14)


def shield(cx, cy, r):
    return S.ring(cx, cy + r * 0.25, r * 0.6) + S.bar(cx - r * 0.3, cy - r * 0.35, cx - r * 0.35, cy - r * 0.9) + \
        S.bar(cx + r * 0.3, cy - r * 0.35, cx + r * 0.35, cy - r * 0.9)


def conquest(cx, cy, r):
    return S.frame(cx - r * 0.7, cy - r * 0.55, r * 1.4, r * 1.1, square=2.4) + S.bar(cx - r * 0.95, cy + r * 0.9, cx + r * 0.95, cy - r * 0.9)


def antlers(cx, cy, r):
    return S.ring(cx, cy - r * 0.55, r * 0.28) + S.bar(cx - r * 0.2, cy - r * 0.3, cx - r * 0.6, cy + r * 0.9) + \
        S.bar(cx + r * 0.2, cy - r * 0.3, cx + r * 0.6, cy + r * 0.9) + S.bar(cx - r * 0.42, cy + r * 0.4, cx - r * 0.85, cy + r * 0.55) + \
        S.bar(cx + r * 0.42, cy + r * 0.4, cx + r * 0.85, cy + r * 0.55)


def antler(cx, cy, r):
    return S.bar(cx - r * 0.6, cy - r * 0.9, cx + r * 0.4, cy + r * 0.9) + S.bar(cx - r * 0.1, cy, cx + r * 0.6, cy + r * 0.3) + \
        S.bar(cx + r * 0.15, cy + r * 0.45, cx - r * 0.5, cy + r * 0.6)


def mask(cx, cy, r):
    return S.frame(cx - r * 0.7, cy - r * 0.85, r * 1.4, r * 1.7, square=2.4) + S.bar(cx - r * 0.45, cy + r * 0.2, cx - r * 0.12, cy + r * 0.2) + \
        S.bar(cx + r * 0.12, cy + r * 0.2, cx + r * 0.45, cy + r * 0.2)


def eras_end(cx, cy, r):
    return S.frame(cx - r * 0.45, cy - r * 0.85, r * 0.9, r * 1.4, square=2.6) + S.bar(cx - r * 0.45, cy, cx + r * 0.45, cy - r * 0.3) + \
        S.dot(cx - r * 0.85, cy + r * 0.7, r * 0.13) + S.dot(cx + r * 0.85, cy + r * 0.7, r * 0.13)


def drops3(cx, cy, r):
    """Three falling drops: blood."""
    out = []
    for dx, dy in ((-0.55, 0.15), (0, -0.2), (0.55, 0.15)):
        x, y = cx + r * dx, cy + r * dy
        out.append(S.Fill(S._arc(x, y - r * 0.1, r * 0.17, r * 0.17, 180, 360) + [(x, y + r * 0.35)]))
    return out


def day_sun(cx, cy, r):
    """A day: the sun's disk ringed by four petals."""
    out = S.ring(cx, cy, r * 0.42)
    for k in range(4):
        a = math.radians(k * 90)
        out += S.dot(cx + r * 0.75 * math.cos(a), cy + r * 0.75 * math.sin(a), r * 0.16)
    return out


def carapace_hex(cx, cy, r):
    pts = [(cx + r * 0.9 * math.cos(math.radians(30 + k * 60)), cy + r * 0.9 * math.sin(math.radians(30 + k * 60))) for k in range(7)]
    return S.poly(pts) + S.dot(cx, cy, r * 0.2)


def black_mirror(cx, cy, r):
    """Polished obsidian: a solid disk."""
    return S.dot(cx, cy, r * 0.62)


def hand_mirror(cx, cy, r):
    return [S.Track(S._arc(cx + r * 0.2, cy, r * 0.6, r * 0.5, 0, 360), closed=True)] + S.bar(cx - r * 0.4, cy, cx - r * 0.95, cy)


def open_room(cx, cy, r):
    return S.poly([(cx - r * 0.3, cy - r * 0.85), (cx - r * 0.85, cy - r * 0.85), (cx - r * 0.85, cy + r * 0.85), (cx + r * 0.85, cy + r * 0.85),
                   (cx + r * 0.85, cy - r * 0.85), (cx + r * 0.3, cy - r * 0.85)])


def tripod(cx, cy, r):
    """The censer: a bowl on three legs."""
    return S.arc(cx, cy + r * 0.3, r * 0.85, r * 0.6, 190, 350) + S.bar(cx - r * 0.85, cy + r * 0.25, cx + r * 0.85, cy + r * 0.25) + \
        S.bar(cx - r * 0.5, cy - r * 0.3, cx - r * 0.6, cy - r * 0.85) + S.bar(cx, cy - r * 0.35, cx, cy - r * 0.85) + \
        S.bar(cx + r * 0.5, cy - r * 0.3, cx + r * 0.6, cy - r * 0.85)


def posted_house(cx, cy, r):
    return S.poly([(cx - r * 0.9, cy), (cx, cy + r * 0.85), (cx + r * 0.9, cy)]) + S.bar(cx - r * 0.55, cy, cx - r * 0.55, cy - r * 0.85) + \
        S.bar(cx + r * 0.55, cy, cx + r * 0.55, cy - r * 0.85)


def nested_diamond(cx, cy, r):
    out = S.poly([(cx, cy + r * 0.9), (cx + r * 0.9, cy), (cx, cy - r * 0.9), (cx - r * 0.9, cy), (cx, cy + r * 0.9)])
    return out + S.poly([(cx, cy + r * 0.42), (cx + r * 0.42, cy), (cx, cy - r * 0.42), (cx - r * 0.42, cy), (cx, cy + r * 0.42)])


def sprout_seed(cx, cy, r):
    return [S.Track(S._arc(cx, cy - r * 0.25, r * 0.45, r * 0.55, 0, 360), closed=True)] + \
        S.bar(cx, cy + r * 0.3, cx, cy + r * 0.9) + S.bar(cx, cy + r * 0.6, cx + r * 0.4, cy + r * 0.85)


def two_prints(cx, cy, r):
    return footprint(cx - r * 0.45, cy - r * 0.15, r * 0.7) + footprint(cx + r * 0.45, cy + r * 0.15, r * 0.7)


def handled_jar(cx, cy, r):
    return jar(cx, cy, r * 0.85) + S.ring(cx - r * 0.85, cy + r * 0.25, r * 0.17) + S.ring(cx + r * 0.85, cy + r * 0.25, r * 0.17)


def horizon_sun(cx, cy, r):
    return S.arc(cx, cy - r * 0.35, r * 0.6, r * 0.6, 0, 180) + S.bar(cx - r * 0.9, cy - r * 0.35, cx + r * 0.9, cy - r * 0.35)


def flaming_coal(cx, cy, r):
    return S.ring(cx, cy - r * 0.3, r * 0.5) + S.tick(cx - r * 0.35, cy + r * 0.3, r * 0.55, angle=115) + \
        S.tick(cx + r * 0.35, cy + r * 0.3, r * 0.55, angle=65)


def spiral_ball(cx, cy, r):
    return S.ring(cx, cy, r * 0.85) + R.curl(cx, cy, r * 0.4, turns=0.75)


def vault(cx, cy, r):
    """The sky: a star over the horizon."""
    return star4(cx, cy + r * 0.25, r * 0.55) + S.bar(cx - r * 0.95, cy - r * 0.6, cx + r * 0.95, cy - r * 0.6)


def lump(cx, cy, r):
    return [S.Track(S._arc(cx, cy, r * 0.85, r * 0.6, 0, 360), closed=True)] + R.curl(cx, cy, r * 0.32, turns=0.9)


def doorway(cx, cy, r):
    return S.arc(cx, cy + r * 0.1, r * 0.75, r * 0.75, 0, 180) + S.bar(cx - r * 0.75, cy + r * 0.1, cx - r * 0.75, cy - r * 0.85) + \
        S.bar(cx + r * 0.75, cy + r * 0.1, cx + r * 0.75, cy - r * 0.85) + S.bar(cx - r * 0.9, cy - r * 0.85, cx + r * 0.9, cy - r * 0.85)


def prowed_canoe(cx, cy, r):
    return S.arc(cx, cy + r * 0.5, r * 0.85, r * 0.85, 200, 340) + S.bar(cx - r * 0.8, cy + r * 0.2, cx - r * 0.95, cy + r * 0.75) + \
        S.bar(cx + r * 0.8, cy + r * 0.2, cx + r * 0.95, cy + r * 0.75)


def barred_diamond(cx, cy, r):
    """Eight thousand: a square frame with a raised diamond at its heart."""
    out = S.poly([(cx - r * 0.85, cy - r * 0.85), (cx - r * 0.85, cy + r * 0.85), (cx + r * 0.85, cy + r * 0.85),
                  (cx + r * 0.85, cy - r * 0.85), (cx - r * 0.85, cy - r * 0.85)])
    return out + [S.Fill([(cx, cy + r * 0.42), (cx + r * 0.42, cy), (cx, cy - r * 0.42), (cx - r * 0.42, cy)])]


def print_on_road(cx, cy, r):
    return footprint(cx, cy + r * 0.2, r * 0.8) + S.dot(cx - r * 0.75, cy - r * 0.75, r * 0.13) + S.dot(cx + r * 0.75, cy - r * 0.75, r * 0.13)


# -- the signs -----------------------------------------------------------------------------------


@dataclass(frozen=True)
class Sign:
    code: str  # its codage, as ka1
    syllable: str
    source: str  # the word or picture it comes from
    motif: Callable[[Box], list]
    traditional: bool = False

    def _in(self, w, h):
        return [(CONTOUR, R.cushion(0, 0, w, h, square=2.6)),
                (DETAIL, self.motif(Box(PAD, PAD, w - PAD, h - PAD)))]

    def flat(self):
        return self._in(B * SPAN, B * AFFIX)

    def tall(self):
        return self._in(B * AFFIX, B * SPAN)


# Each syllable's signs, in order: (source, motif). The order numbers the codes.
SOURCES = {
    "a": [("ashtsom, marriage", P(pierced_beads, 0.9)), ("ashal, affection", curls(2))],
    "i": [("ish'uqal, the moon", P(crescent, 0.85)), ("ish'ilan, a star", P(star4)), ("ish'bal, the jaguar", P(spots))],
    "o": [("olek', ten", bars(2))],
    "u": [("ul'om, maize", P(seed, 0.9))],
    "ka": [("k'ayik, a flame", P(drop)), ("k'aykulak, a coal", P(flaming_coal)), ("k'ayikash, the eye", P(almond_eye, 0.8))],
    "ke": [("kesh, all", P(three_dots_ring)), ("k'eshik, a key", P(key))],
    "ki": [("k'inish, sunlight", P(light))],
    "ko": [("k'otsik, cord", knots), ("k'otsel, the knotted records", P(hanging_cords))],
    "ku": [("kulum, stone", P(cracked_stone)), ("kul'qat, the sacred peak", stairs), ("kulam, the heart", P(heart, 0.85))],
    "cha": [("ch'akun, a serpent", P(serpent)), ("ch'alik, low", P(low))],
    "che": [("ch'ekum, an animal", P(legs)), ("ch'eknal, a worm", P(worm))],
    "chi": [("ch'imik, a hill", P(mound)), ("ch'imel, a gift", P(bundle_x))],
    "chu": [("ch'umel, the voice", P(scroll)), ("ch'ul, toward", P(chevron))],
    "tsa": [("ts'amal, the shell", P(shell)), ("ts'anul, a roof", P(tent))],
    "tse": [("ts'en, the sun", P(sun)), ("ts'ena, a day", P(horizon_sun))],
    "tsi": [("ts'ikel, a drink", P(cup, 0.85)), ("ts'ik, above", P(above))],
    "tso": [("ts'okum, a coyote", P(ears)), ("ts'obel, a number", chevrons)],
    "tsu": [("ts'umulal, blood", P(drops3)), ("ts'uqal, moonlight", waves(1))],
    "pa": [("p'ashel, the quetzal", P(plume, 0.85)), ("pakul, a table", P(table))],
    "pe": [("p'enqal, a grassland", P(tufts)), ("pel'ush, four hundred", P(diamond(2)))],
    "pi": [("p'ishum, the hand", P(palm)), ("p'ikul, clay", P(lump)), ("p'ilik, a needle", P(needle))],
    "po": [("p'o, five", bars(1))],
    "pu": [("p'uqal, night", P(dome_night)), ("pu'uts, a mesa", P(mesa))],
    "qa": [("tq'an, the edge", P(corner_dot)), ("q'aptel, the border", ticks)],
    "qe": [("q'emul, supreme", P(supreme))],
    "qi": [("q'ishe, eight", bar_dots(1, 3))],
    "qo": [("q'o, two", dots(2))],
    "qu": [("q'umpel, eight thousand", P(barred_diamond))],
    "ti": [("ti, you", P(you))],
    "to": [("toshal, the south", P(quarter(False)))],
    "sha": [("sh'akan, earth", P(furrows)), ("shak'nal, an eagle", P(eagle))],
    "she": [("shelem, a bird", P(bird))],
    "shi": [("shikik, a seed", P(sprout_seed)), ("shikmah, a tree", P(tree))],
    "sho": [("shok'al, war", P(crossed)), ("shots'em, a door", P(doorway))],
    "shu": [("sh'ulum, a house", P(posted_house)), ("sh'ulik, a room", P(open_room, 0.8))],
    "li": [("lishe, three", dots(3, 20))],
    "lu": [("lu'she, a pot", P(pot))],
    "ma": [("mah, a lord", P(lord))],
    "mu": [("mushe, four", dots(4, 18))],
    "na": [("nalak, the mouth", P(mouth, 0.85)), ("nal'bish, the womb", P(womb))],
    "ne": [("ne', water", waves(2)), ("ne'lum, a jar", P(handled_jar))],
    "ni": [("ni, the self", P(self_))],
    "no": [("no'kin, a bear", P(bear)), ("no'tun, a mountain range", P(peaks))],
    "nu": [("nukal, the north", P(quarter(True))), ("nuq'el, seven", bar_dots(1, 2))],
    "ha": [("ha'nal, a river", P(river)), ("ha'tan, a bowl", P(bowl)), ("ha'kin, a mirror", P(hand_mirror))],
    "hu": [("h'ulal, the sky", P(vault)), ("h'ul, air", curls(3))],
    "la": [("jade", rings(3)), ("the Fifth Age", P(quincunx))],
    "ba": [("obsidian", P(blade, 0.9)), ("the obsidian mirror", P(black_mirror))],
    "ta": [("a feather", P(quill)), ("the plume of rank", P(three_plumes))],
    "le": [("a drum", P(drum)), ("a rattle", P(rattle))],
    "me": [("a turtle", P(turtle)), ("the turtle's shell", P(carapace_hex))],
    "mi": [("a canoe", P(prowed_canoe)), ("a pilgrimage", P(print_on_road))],
    "yi": [("incense", P(incense)), ("the censer", P(tripod))],
    "yu": [("the mat", P(mat, 0.8)), ("the throne", P(throne))],
    "tu": [("salt", P(heap)), ("tribute", P(tied))],
    "te": [("the ball", P(spiral_ball)), ("the ballcourt", P(court))],
    "ya": [("a monkey", P(monkey)), ("the arts", P(arts))],
    "ye": [("a bat", P(bat)), ("a burial", P(burial))],
    "bi": [("a net", net), ("a capture", P(capture))],
    "lo": [("a hummingbird", P(hummingbird)), ("the warrior's soul", P(soul))],
    "hi": [("a shield", P(shield)), ("a conquest", P(conquest))],
    "he": [("a deer", P(antlers)), ("an antler", P(antler))],
    "be": [("a mask", P(mask)), ("the era's end", P(eras_end))],
}

TRADITIONAL = {"la", "ba", "ta", "le", "me", "mi", "yi", "yu", "tu", "te", "ya", "ye", "bi", "lo", "hi", "he", "be"}

SIGNS = {}
for _syl, _signs in SOURCES.items():
    for _i, (_src, _motif) in enumerate(_signs, 1):
        _code = f"{_syl}{_i}"
        SIGNS[_code] = Sign(_code, _syl, _src, _motif, _syl in TRADITIONAL)
