# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""The Ch'alish P'ilam common hand's strokes: the lines every common sign is built from.

    import strokes as S

    t = S.bar(0, 0, 0, S.BLOCK) + S.ring(300, 365, 120)   # a list of Tracks and Fills
    ink = S.ink(t, S.COMMON)                             # a pathops.Path, font units, y up

Ch'alish P'ilam is the writing of the Ki'ich'chik city-states, and it has two hands
that share their readings and nothing else:

- **The common hand** is written in plain lines: chalk on a shaft wall or a slate, a
  point on a wooden palette, a stylus on bark paper, a pen or brush on vellum. Every
  tool writes the same even line, and weight never tells two signs apart. A sign is
  built from a small fixed set of strokes, and fills a square **cell** that is never
  drawn: the cell is implied by the spacing alone. Signs are read in rows of two, left
  to right, down a column two cells wide.
- **The ceremonial hand** is not built from these strokes. Each of its signs is an
  individual picture drawn inside a box, as the Khelathi temple hieroglyphs are.

Coordinates are font units on a 1000-unit em, the line at y = 0, drawn at the size the
font sets them. A cell stands ``BLOCK`` high, Latin's cap height, on the line.

**Tracks.** A stroke is a list of :class:`Track` objects, centrelines sampled with a
pressure at every point, plus solid :class:`Fill` shapes. A pen turns tracks into ink:
the union of its round footprints, each as wide as the pen makes it at that pressure.
The common pen has one width at every pressure.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import pathops

# -- metrics -----------------------------------------------------------------------------------

BLOCK = 730.0  # a full block, square: Latin's cap height, 0.73 em
AFFIX = 0.34 * BLOCK  # the short side of an affix, the oblong set beside or above a main sign
LATIN_X = 513.5  # the shared x-height, a guide
STEP = 3.0  # sampling interval along a track, in units

ASCENT, DESCENT, LINE_GAP = 945, -200, 100  # the shared line metrics of tools/vertical.py


# -- pens --------------------------------------------------------------------------------------


@dataclass(frozen=True)
class Pen:
    """A round point whose width follows pressure: ``light`` at pressure 0, ``full`` at 1."""

    name: str
    full: float
    light: float
    taper: float  # how far along a track (in units) a free end lifts to ``light``


# The common hand's line: chalk, a stylus, a pen or a brush, all writing one even line.
# Weight never tells two signs apart, so the line is the same everywhere.
COMMON = Pen("common", full=50.0, light=50.0, taper=1.0)
# The pointed brush: fine at entry and exit, swelling through the stroke.
CEREMONIAL = Pen("ceremonial", full=30.0, light=7.0, taper=120.0)


# -- tracks and fills --------------------------------------------------------------------------


@dataclass
class Track:
    """A centreline: samples of (x, y). ``closed`` tracks have no free ends."""

    pts: list = field(default_factory=list)
    closed: bool = False
    weight: float = 1.0  # a multiplier on the pen's width, for a detail drawn finer

    def length(self):
        return sum(math.dist(a, b) for a, b in zip(self.pts, self.pts[1:]))


@dataclass
class Fill:
    """A solid region, drawn the same by both pens: a dot, a pupil, a numeral's bar."""

    pts: list


def _bezier(p0, c1, c2, p1):
    approx = math.dist(p0, c1) + math.dist(c1, c2) + math.dist(c2, p1)
    n = max(4, math.ceil(approx / STEP))
    out = []
    for i in range(n + 1):
        u = i / n
        a, b, c, d = (1 - u) ** 3, 3 * u * (1 - u) ** 2, 3 * u * u * (1 - u), u**3
        out.append((a * p0[0] + b * c1[0] + c * c2[0] + d * p1[0], a * p0[1] + b * c1[1] + c * c2[1] + d * p1[1]))
    return out


def _line(p0, p1):
    n = max(2, math.ceil(math.dist(p0, p1) / STEP))
    return [(p0[0] + (p1[0] - p0[0]) * i / n, p0[1] + (p1[1] - p0[1]) * i / n) for i in range(n + 1)]


def _arc(cx, cy, rx, ry, a0, a1):
    """Degrees, counter-clockwise from the right."""
    n = max(6, math.ceil(abs(math.radians(a1 - a0)) * max(rx, ry) / STEP))
    return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


# -- the strokes -------------------------------------------------------------------------------
#
# Each takes a box or a centre and returns a list of Tracks and Fills. The names are the
# names the sheets print.


def frame(x, y, w, h, square=3.2):
    """The cushion: the rounded square every main sign is drawn in, a superellipse whose
    sides swell evenly into round corners. ``square`` is its exponent: 2 is an ellipse,
    and the higher it goes the squarer the corners."""
    cx, cy, a, b = x + w / 2, y + h / 2, w / 2, h / 2
    n = max(120, math.ceil(2 * (w + h) / STEP))
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n
        c, s = math.cos(t), math.sin(t)
        pts.append((cx + a * math.copysign(abs(c) ** (2 / square), c), cy + b * math.copysign(abs(s) ** (2 / square), s)))
    return [Track(pts, closed=True)]


def affix(x, y, w, h):
    """The oblong: a narrow cushion, the shape of a sign set beside, above or below a main
    sign. Its ends are rounder than the main sign's corners."""
    return frame(x, y, w, h, square=2.6)


def bar(x0, y0, x1, y1, weight=1.0):
    """A straight stroke from one point to another: a stem, a bar, a slash or a fall."""
    return [Track(_line((x0, y0), (x1, y1)), weight=weight)]


def tick(x, y, length, angle=90.0, weight=1.0):
    """A short straight mark from (x, y) at ``angle``."""
    t = math.radians(angle)
    return bar(x, y, x + length * math.cos(t), y + length * math.sin(t), weight)


def dot(cx, cy, r):
    """A round dab, solid in both hands."""
    return [Fill(_arc(cx, cy, r, r, 0, 360)[:-1])]


def ring(cx, cy, r, weight=1.0):
    """A small closed circle: an eye, a bead, a disk."""
    return [Track(_arc(cx, cy, r, r, 90, 450), closed=True, weight=weight)]


def arc(cx, cy, rx, ry, a0, a1, weight=1.0):
    """An open curve, part of an ellipse: a brow, a lid, a bowl, a band."""
    return [Track(_arc(cx, cy, rx, ry, a0, a1), weight=weight)]


def hook(cx, cy, r, opening=0.0, weight=1.0):
    """Three quarters of a circle, open toward ``opening`` degrees: a cheek, a mouth,
    an ear, a bracket."""
    return arc(cx, cy, r, r, opening + 45, opening + 315, weight)


def curl(cx, cy, r, turns=1.25, clockwise=False, weight=1.0):
    """A volute: a spiral wound in from radius ``r`` toward the centre. Speech, breath,
    smoke, the curl of water and the ornament of a ceremonial sign."""
    n = max(40, math.ceil(turns * 2 * math.pi * r / STEP))
    pts = []
    for i in range(n + 1):
        u = i / n
        a = 2 * math.pi * turns * u * (-1 if clockwise else 1)
        rr = r * (1 - 0.82 * u)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return [Track(pts, weight=weight)]


def poly(points, weight=1.0):
    """Straight strokes through ``points`` without lifting: a run of corners."""
    pts = [points[0]]
    for a, b in zip(points, points[1:]):
        pts += _line(a, b)[1:]
    return [Track(pts, weight=weight)]


def corner(x0, y0, x1, y1, weight=1.0):
    """Two straight strokes meeting at a turn: across from (x0, y0) to (x1, y0), then to
    (x1, y1)."""
    return [Track(_line((x0, y0), (x1, y0)) + _line((x1, y0), (x1, y1))[1:], weight=weight)]


def wave(x0, y0, x1, amp, periods=1.0, weight=1.0):
    """A running S: water, a serpent's body, a band of cloth."""
    n = max(20, math.ceil(abs(x1 - x0) / STEP))
    return [Track([(x0 + (x1 - x0) * i / n, y0 + amp * math.sin(2 * math.pi * periods * i / n))
                   for i in range(n + 1)], weight=weight)]


def hatch(x, y, w, h, n=5, angle=45.0, cross=False, weight=0.7):
    """Parallel strokes filling a box: the painter's shading, and darkness. ``cross``
    lays a second set across the first."""
    out = []
    for a in ([angle, -angle] if cross else [angle]):
        t = math.radians(a)
        dx, dy = math.cos(t), math.sin(t)
        nx, ny = -dy, dx
        cx, cy = x + w / 2, y + h / 2
        span = abs(w * nx) + abs(h * ny)
        for i in range(n):
            off = (i + 0.5) / n - 0.5
            px, py = cx + nx * off * span, cy + ny * off * span
            seg = _clip_line(px, py, dx, dy, x, y, x + w, y + h)
            if seg:
                out.append(Track(_line(*seg), weight=weight))
    return out


def _clip_line(px, py, dx, dy, x0, y0, x1, y1):
    lo, hi = -1e9, 1e9
    for p, d, a, b in ((px, dx, x0, x1), (py, dy, y0, y1)):
        if abs(d) < 1e-9:
            if p < a or p > b:
                return None
            continue
        t0, t1 = (a - p) / d, (b - p) / d
        lo, hi = max(lo, min(t0, t1)), min(hi, max(t0, t1))
    if hi - lo < 1:
        return None
    return (px + dx * lo, py + dy * lo), (px + dx * hi, py + dy * hi)


def beads(x0, y0, x1, y1, n, r):
    """A row of dots along a line: the border of a ceremonial block, a string of jade."""
    return [f for i in range(n) for f in dot(x0 + (x1 - x0) * (i + 0.5) / n, y0 + (y1 - y0) * (i + 0.5) / n, r)]


# -- numerals: a test of the bar and the dot ---------------------------------------------------


def numeral(n, x, y, w, h):
    """Bar-and-dot, 1 to 19: up to three bars for fives, stacked from the bottom, and
    up to four dots above them, centred. A test of how the bar and the dot sit together."""
    out = []
    bars, dots = divmod(n, 5)
    bh, gap = 0.13 * h, 0.07 * h
    yy = y
    for _ in range(bars):
        out += [Fill(_capsule(x + 0.08 * w, yy + bh / 2, x + 0.92 * w, yy + bh / 2, bh / 2))]
        yy += bh + gap
    if dots:
        r = 0.07 * h
        span = (dots - 1) * 2.9 * r
        for i in range(dots):
            out += dot(x + w / 2 - span / 2 + i * 2.9 * r, yy + r, r)
    return out


def _capsule(x0, y0, x1, y1, r):
    a = math.degrees(math.atan2(y1 - y0, x1 - x0))
    return _arc(x1, y1, r, r, a - 90, a + 90) + _arc(x0, y0, r, r, a + 90, a + 270)


# -- ink ---------------------------------------------------------------------------------------


def _pressure(track: Track, pen: Pen):
    """Pressure along a track: 1 in the body, easing to 0 over ``pen.taper`` at a free end.
    The brush's ease is longer, so its strokes swell; the stylus barely eases."""
    if track.closed:
        return [1.0] * len(track.pts)
    total = track.length()
    taper = min(pen.taper, total / 2.2) or 1.0
    out, run = [], 0.0
    for i, p in enumerate(track.pts):
        if i:
            run += math.dist(track.pts[i - 1], p)
        e = min(run, total - run) / taper
        out.append(min(1.0, math.sin(min(1.0, e) * math.pi / 2)))
    return out


def _circle(cx, cy, r, facets=20):
    return [(cx + r * math.cos(2 * math.pi * i / facets), cy + r * math.sin(2 * math.pi * i / facets))
            for i in range(facets)]


def _hull(pts):
    pts = sorted(set(pts))
    if len(pts) < 3:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def _poly(path: pathops.Path, pts):
    pen = path.getPen()
    pen.moveTo(pts[0])
    for p in pts[1:]:
        pen.lineTo(p)
    pen.closePath()


def ink(parts, pen: Pen) -> pathops.Path:
    """The ink the pen leaves for ``parts``: the union of every footprint hull and fill."""
    path = pathops.Path()
    for part in parts:
        if isinstance(part, Fill):
            _poly(path, part.pts)
            continue
        ps = _pressure(part, pen)
        pts = part.pts + ([part.pts[0]] if part.closed else [])
        ps = ps + ([ps[0]] if part.closed else [])
        for (a, pa), (b, pb) in zip(zip(pts, ps), zip(pts[1:], ps[1:])):
            ra = part.weight * (pen.light + (pen.full - pen.light) * pa) / 2
            rb = part.weight * (pen.light + (pen.full - pen.light) * pb) / 2
            _poly(path, _hull(_circle(*a, ra) + _circle(*b, rb)))
    path.simplify(fix_winding=True)
    return path


def contours(path: pathops.Path):
    """The path's contours as lists of (x, y)."""
    out, cur = [], []
    for verb, pts in path:
        if verb == pathops.PathVerb.MOVE:
            cur = [pts[0]]
        elif verb in (pathops.PathVerb.LINE, pathops.PathVerb.QUAD, pathops.PathVerb.CUBIC):
            cur.append(pts[-1])
        elif verb == pathops.PathVerb.CLOSE:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out
