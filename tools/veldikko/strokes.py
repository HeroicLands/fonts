# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""The Veldikko stroke inventory, as parametric pen strokes that emit outlines.

    import strokes as S

    stem = S.shape("stem", 0, 0, top=S.ASC)  # a Shape: tracks, entry and exit, forward frame
    bowl = S.shape("bud", 0, 0)               # the bowl grows forward from the stem's foot
    path = S.outline(stem.tracks + bowl.tracks, S.HAND)   # a pathops.Path, font units, y up

The Veldikko runs right to left. Coordinates are font units on a 1000-unit em,
the line at y = 0. Nothing is drawn along the line: it is implied by the feet of
the stems and the floors of the bowls, which all stand on it.

**The forward frame.** Every skeleton is written in a frame where ``f`` runs the
way the pen travels and ``y`` is up; ``to_page`` turns ``f`` leftward. A letter's
stem stands at its back and its bowl lies forward of it.

**How a stroke is drawn.** A stroke is one or more *tracks*: a path the nib
follows, sampled every ``STEP`` units, with a *pressure* at every sample. The nib
is narrow, flat and cut obliquely, its edge held at ``Nib.angle`` on the page as
a qalam's is, so a stroke's weight follows its direction: a bowl's floor on the
line is the fullest, a stem is slender, and a stroke running along the edge is a
hairline. Pressure flexes the edge: at full pressure it is ``width`` long, and at
none it is ``1 - flex`` of that. A negative pressure is the pen lifting off the
page: the footprint shrinks with it, and at -1 it is gone, so a tail trails away
to nothing.

The outline is the union of the convex hulls of neighbouring footprints. The
style is separate from the skeletons: ``HAND`` is the one nib and ductus every
text is written with, Sinale and Áelendi alike.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Callable

import pathops


# -- metrics -----------------------------------------------------------------------------------

X = 270.0  # the height of a bowl above the line
ASC = 680.0  # the head of a raised stem
DESC = -280.0  # the foot of a lowered stem
MARK = 400.0  # the floor of the vowel marks over a bowl
BAR = -90.0  # the length bar's place beneath the line
STEP = 4.0  # sampling interval along a track, in units


# -- nib and style -----------------------------------------------------------------------------


@dataclass(frozen=True)
class Nib:
    width: float  # the edge at full pressure
    thin: float  # the nib's thickness: the hairline
    angle: float  # the edge's direction on the page, degrees, counter-clockwise from the right
    flex: float  # how far a light pressure narrows the edge
    facets: int = 20


@dataclass(frozen=True)
class Style:
    name: str
    nib: Nib
    slant: float = 0.0  # lean in the direction of travel, degrees
    flourish: float = 1.0  # scales the curls, eddies and spirals
    pressure: float = 1.0  # scales every positive pressure the skeletons give


# The hand: one nib and one ductus for every text, Sinale and Áelendi alike.
HAND = Style("Veldikko", Nib(width=54.0, thin=11.0, angle=62.0, flex=0.45), slant=12.0, flourish=1.0)


# -- tracks ------------------------------------------------------------------------------------


Ease = Callable[[float], float]


def linear(u: float) -> float:
    return u


def ease_in(k: float = 2.0) -> Ease:
    return lambda u: u**k


def ease_out(k: float = 2.0) -> Ease:
    return lambda u: 1 - (1 - u) ** k


def bell(u: float) -> float:
    return math.sin(math.pi * u)


@dataclass
class Track:
    """A pen path in the forward frame: samples of (f, y, pressure)."""

    f: float
    y: float
    p: float
    samples: list = field(default_factory=list)

    def __post_init__(self):
        self.samples = [(self.f, self.y, self.p)]

    @property
    def end(self):
        return self.samples[-1]

    def line(self, f, y, p, ease: Ease = linear, wave: Callable[[float], float] | None = None):
        f0, y0, p0 = self.end
        n = max(2, math.ceil(math.hypot(f - f0, y - y0) / STEP))
        for i in range(1, n + 1):
            u = i / n
            q = p0 + (p - p0) * ease(u) + (wave(u) if wave else 0.0)
            self.samples.append((f0 + (f - f0) * u, y0 + (y - y0) * u, q))
        return self

    def curve(self, c1, c2, f, y, p, ease: Ease = linear, wave: Callable[[float], float] | None = None):
        """A cubic Bezier to (f, y); pressure eases to ``p``, ``wave(u)`` adds to it."""
        f0, y0, p0 = self.end
        approx = math.dist((f0, y0), c1) + math.dist(c1, c2) + math.dist(c2, (f, y))
        n = max(3, math.ceil(approx / STEP))
        for i in range(1, n + 1):
            u = i / n
            a, b, c, d = (1 - u) ** 3, 3 * u * (1 - u) ** 2, 3 * u * u * (1 - u), u**3
            q = p0 + (p - p0) * ease(u) + (wave(u) if wave else 0.0)
            self.samples.append((a * f0 + b * c1[0] + c * c2[0] + d * f, a * y0 + b * c1[1] + c * c2[1] + d * y, q))
        return self

    def spiral(self, cf, cy, sweep_deg, shrink, p, ease: Ease = linear):
        """Turn about (cf, cy) by ``sweep_deg`` (positive is counter-clockwise in the
        forward frame), the radius shrinking by ``shrink`` over the turn."""
        f0, y0, p0 = self.end
        r0 = math.hypot(f0 - cf, y0 - cy)
        t0 = math.atan2(y0 - cy, f0 - cf)
        sweep = math.radians(sweep_deg)
        n = max(8, math.ceil(abs(sweep) * r0 / STEP))
        for i in range(1, n + 1):
            u = i / n
            r = r0 * (1 - shrink * u)
            t = t0 + sweep * u
            self.samples.append((cf + r * math.cos(t), cy + r * math.sin(t), p0 + (p - p0) * ease(u)))
        return self


@dataclass
class Shape:
    """A stroke's tracks with the points it is joined at. Headings are degrees in the
    forward frame: 0 is the way the pen travels, 90 is up."""

    tracks: list
    entry: tuple  # (f, y, heading)
    exit: tuple  # (f, y, heading)

    def moved(self, df, dy):
        tracks = []
        for t in self.tracks:
            n = Track(0, 0, 0)
            n.samples = [(f + df, y + dy, p) for f, y, p in t.samples]
            tracks.append(n)
        e, x = self.entry, self.exit
        return Shape(tracks, (e[0] + df, e[1] + dy, e[2]), (x[0] + df, x[1] + dy, x[2]))


def polar(f, y, length, deg):
    t = math.radians(deg)
    return f + length * math.cos(t), y + length * math.sin(t)


# -- geometry ----------------------------------------------------------------------------------


def to_page(f, y, style: Style):
    """Forward frame to page: the pen travels leftward."""
    return -(f + y * math.tan(math.radians(style.slant))), y


def _footprint(x, y, p, style: Style):
    n = style.nib
    if p < 0:
        k = max(0.0, 1 + p)  # lifting off the page
        p = 0.0
    else:
        k = 1.0
        p = min(1.0, p * style.pressure)
    a = k * n.width * (1 - n.flex + n.flex * p) / 2
    b = k * n.thin / 2
    a, b = max(a, 0.8), max(b, 0.8)  # a lifted pen ends in a point, never a degenerate footprint
    t = math.radians(n.angle)
    ct, st = math.cos(t), math.sin(t)
    pts = []
    for i in range(n.facets):
        s = 2 * math.pi * i / n.facets
        c, si = math.cos(s), math.sin(s)
        ex = a * math.copysign(abs(c) ** 0.4, c)  # a flat edge with softened corners
        ey = b * math.copysign(abs(si) ** 0.4, si)
        pts.append((x + ex * ct - ey * st, y + ex * st + ey * ct))
    return pts


def _hull(points):
    pts = sorted(set(points))
    if len(pts) <= 2:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower, upper = [], []
    for q in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], q) <= 0:
            lower.pop()
        lower.append(q)
    for q in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], q) <= 0:
            upper.pop()
        upper.append(q)
    return lower[:-1] + upper[:-1]


def _area(poly):
    return abs(sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(poly, poly[1:] + poly[:1]))) / 2


def outline(tracks, style: Style = HAND) -> pathops.Path:
    """The union of the footprints the nib leaves along the tracks."""
    hulls = []
    for track in tracks:
        prints, last = [], None
        for f, y, p in track.samples:
            x, yy = to_page(f, y, style)
            if last is not None and math.hypot(x - last[0], yy - last[1]) < 0.5:
                continue
            last = (x, yy)
            prints.append([(round(a, 2), round(b, 2)) for a, b in _footprint(x, yy, p, style)])
        for a, b in zip(prints, prints[1:]):
            poly = _hull(a + b)
            if len(poly) >= 3 and _area(poly) >= 1.0:
                hulls.append(poly)
    path = _polys(hulls)
    try:
        path.simplify(fix_winding=True)
        return path
    except pathops.PathOpsError:
        out = pathops.Path()
        for i in range(0, len(hulls), 40):
            out = pathops.op(out, _polys(hulls[i:i + 40], simplify=True), pathops.PathOp.UNION)
        return out


def _polys(polys, simplify=False):
    path = pathops.Path()
    for poly in polys:
        path.moveTo(*poly[0])
        for q in poly[1:]:
            path.lineTo(*q)
        path.close()
    if simplify:
        try:
            path.simplify(fix_winding=True)
        except pathops.PathOpsError:
            out = pathops.Path()
            for poly in polys:
                out = pathops.op(out, _polys([poly]), pathops.PathOp.UNION)
            return out
    return path


def union(paths) -> pathops.Path:
    out = pathops.Path()
    for p in paths:
        out.addPath(p)
    out.simplify(fix_winding=True)
    return out


def _lift(t: Track, frac: float = 0.35):
    """Lift the pen over the last ``frac`` of the track, so it trails away to nothing."""
    n = len(t.samples)
    k0 = int(n * (1 - frac))
    for i in range(k0, n):
        f, y, p = t.samples[i]
        u = (i - k0) / max(1, n - 1 - k0)
        t.samples[i] = (f, y, p * (1 - u) - u * u)
    return t


def _land(t: Track, frac: float = 0.25):
    """Set the pen down over the first ``frac`` of the track, from nothing."""
    n = len(t.samples)
    k1 = max(1, int(n * frac))
    for i in range(k1):
        f, y, p = t.samples[i]
        u = i / k1
        t.samples[i] = (f, y, p * u - (1 - u) ** 2)
    return t


# -- the strokes -------------------------------------------------------------------------------
#
# Each builder takes the stroke's origin (f, y), its own parameters and ``fl``, the
# style's flourish, and returns a Shape. A letter is a stem and a bowl: the stem's
# origin is its foot on the line, and a bowl's origin is the foot of the stem it
# grows from. A bowl lies forward of its stem and sweeps past it.


def _head_curl(f, y, c):
    """The vine's growing tip at the head of a stem whose top is (f, y): the pen sets
    down at the heart of a curl turned forward and unwinds out of it onto the top."""
    if c <= 0.05:
        return Track(f, y, -0.5)
    cf, cy = f + 34 * c, y - 4
    t = Track(cf + 8, cy, -0.5)
    t.spiral(cf, cy, 320 * c, -3.2 * c, 0.20)
    t.curve(polar(*t.end[:2], 24, 180), (f + 2, y + 4), f, y, 0.25)
    return t


TAILS = ("hook", "ezh", "sweep")  # the tails a lowered stem may run out into, by ``tail`` index


def s_stem(f, y, fl=1.0, top=X + 60, foot=0.0, arc=0.07, tail=0, reach=1.0):
    """A stem: from a curl at its head, a long fall bowed into a shallow arc, to its
    foot. Its head stands at ``top`` and its foot at ``foot``: raised above the bowls
    for a stop, level with them for a fricative, carried below the line for a nasal.
    Below the line the stem runs out into one of ``TAILS``: the hook, a j-like turn
    back and up with a curled tip; the ezh, a cursive z hung from the line, a level
    stroke back, a diagonal forward and a bowl swinging round under it, so that on
    the page it reads as a z and not its mirror; or the sweep, a long bowl forward
    under the letter. ``reach`` lengthens it."""
    c = 0.8 * (0.4 + 0.6 * fl) * (0.7 + 0.3 * min(1.0, top / ASC))
    t = _head_curl(f, y + top, c)
    h = top - foot
    b = -arc * h  # the arc bows back, against the slant, so the stem reads as drawn, not ruled
    if foot > -1:
        t.curve((f + b, y + top - 0.35 * h), (f + b, y + foot + 0.30 * h), f, y + foot, 0.85, ease_in(1.2))
        return Shape([t], (f, y + top, -90), (f, y + foot, -90))
    kind = TAILS[int(round(tail))]
    d = -foot
    r = (40 + 30 * reach) * (0.6 + 0.4 * fl)
    if kind == "ezh":  # a z hung from the line, turned so it reads on the page as a cursive z
        t.curve((f + b, y + top - 0.35 * h), (f + 0.6 * b, y + 0.30 * top), f, y + 6, 0.85, ease_in(1.2))
        t.curve((f - 0.3 * r, y + 2), (f - 0.7 * r, y + 2), f - 1.0 * r, y - 4, 0.45)
        t.curve((f - 0.7 * r, y - 0.18 * d), (f - 0.2 * r, y - 0.32 * d), f - 0.05 * r, y - 0.42 * d, 0.85)
        t.curve((f - 1.4 * reach * r, y - 0.36 * d), (f - 1.8 * reach * r, y - 1.02 * d), f - 0.5 * r, y - d, 0.90)
        t.curve((f + 0.3 * r, y - 0.98 * d), (f + 0.6 * r, y - 0.80 * d), f + 0.5 * r, y - 0.66 * d, 0.20)
        _lift(t, 0.25)
        return Shape([t], (f, y + top, -90), (f - 0.5 * r, y - d, 0))
    t.curve((f + b, y + top - 0.35 * h), (f + 0.6 * b, y + foot + 0.30 * h), f, y + foot + 50, 0.85, ease_in(1.2))
    if kind == "hook":  # back and up, like a j, the tip curled
        q = 1.4 * reach * r
        t.curve((f, y + foot - 6), (f - 0.5 * q, y + foot - 20), f - 1.2 * q, y + foot + 0.25 * q, 0.80)
        t.curve(polar(*t.end[:2], 0.4 * q, 100), (f - 1.4 * q, y + foot + 1.0 * q), f - 1.0 * q,
                y + foot + 1.05 * q, 0.25)
        t.spiral(f - 1.0 * q, y + foot + 0.85 * q, -220 * (0.5 + 0.5 * fl), 0.5, 0.25)
    else:  # forward, under the letter
        t.curve((f + 4, y + foot + 4), (f + 1.2 * r * reach, y + foot - 20), f + 3.2 * r * reach + 20,
                y + foot + 0.6 * r, 0.75)
        t.curve(polar(*t.end[:2], 30, 60), (f + 3.6 * r * reach + 30, y + foot + 1.6 * r), f + 3.0 * r * reach + 10,
                y + foot + 1.5 * r, 0.20)
    _lift(t, 0.3)
    return Shape([t], (f, y + top, -90), (f, y + foot, -90))


def s_bud(f, y, fl=1.0, w=300, h=250, seed=0.8, sweep=0.5):
    """The lips' bowl, open toward the stem: the pen comes in behind the stem, rounds
    onto the line under it, runs forward along the line, climbs the far side, turns
    back over the top and comes down toward the stem, stopping short of it in a seed,
    so the bowl is closed on the line and opens toward the stem."""
    k = seed * (0.5 + 0.5 * fl)
    t = Track(f - (0.10 + 0.25 * sweep) * w, y + 0.30 * h, -0.5)
    t.curve((f - 0.10 * w, y + 0.04 * h), (f + 0.04 * w, y), f + 0.30 * w, y, 0.90, ease_out(1.3))
    t.curve((f + 0.80 * w, y), (f + 1.02 * w, y + 0.24 * h), f + 1.00 * w, y + 0.56 * h, 0.30)
    t.curve((f + 0.98 * w, y + 1.00 * h), (f + 0.50 * w, y + 1.10 * h), f + 0.28 * w, y + 0.86 * h, 0.55)
    end = (f + 0.22 * w, y + 0.52 * h)
    t.curve((f + 0.18 * w, y + 0.76 * h), (f + 0.18 * w, y + 0.60 * h), *end, 0.55)
    if k > 0.05:
        t.spiral(end[0] + 0.07 * w * k, end[1], 300 * k, 0.6, 0.30)
    _lift(t, 0.22)
    return Shape([t], (f - (0.10 + 0.25 * sweep) * w, y + 0.30 * h, -60), (f + w, y, 0))


def s_arches(f, y, fl=1.0, w=320, h=260, n=2, curl=0.8):
    """The tongue-tip's form, arches on a floor: the pen comes in behind the stem, lays
    one long floor on the line, climbs the front and comes back over ``n`` round
    arches on near-upright legs, each leg standing down on the floor. The last leg
    comes down beside the stem and ends just above the floor in a small inward curl,
    short of closing."""
    e = curl * (0.45 + 0.55 * fl)
    n = int(round(n))
    t = Track(f - 0.18 * w, y + 0.30 * h, -0.5)
    t.curve((f - 0.10 * w, y + 0.02 * h), (f + 0.04 * w, y), f + 0.30 * w, y, 0.90, ease_out(1.3))
    t.curve((f + 0.70 * w, y), (f + 0.98 * w, y - 0.01 * h), f + 1.00 * w, y + 0.30 * h, 0.35)
    a = 0.86 * w / n
    right = f + 1.00 * w
    for k in range(n):
        left = right - a
        top_y = y + (1.0 - 0.05 * k) * h
        t.curve((right + 0.01 * w, top_y - 0.10 * h), (right - 0.10 * a, top_y + 0.04 * h), right - 0.5 * a, top_y, 0.45)
        last = k == n - 1
        foot_y = y + (0.16 if last else 0.04) * h
        t.curve((left + 0.10 * a, top_y), (left + 0.02 * a, top_y - 0.30 * h), left + 0.02 * a, foot_y, 0.85,
                ease_out(1.2))
        if not last:
            t.curve((left + 0.02 * a, y + 0.40 * h), (left + 0.02 * a, y + 0.60 * h), left - 0.02 * a, y + 0.80 * h, 0.15)
            right = left
        elif e > 0.05:
            t.spiral(left + 0.02 * a + 0.04 * w * e, foot_y, 260 * e, 0.55, 0.25)
    _lift(t, 0.22)
    return Shape([t], (f - 0.18 * w, y + 0.30 * h, -60), (f + w, y, 0))


def s_coil(f, y, fl=1.0, w=300, h=260, turn=1.0):
    """The back of the mouth's form, the tendril: the pen comes in behind the stem,
    lays a floor along the line, climbs the far side, turns back over the top and
    winds inward into a spiral that fills the counter and never reaches the stem."""
    k = turn * (0.55 + 0.45 * fl)
    t = Track(f - 0.15 * w, y + 0.30 * h, -0.5)
    t.curve((f - 0.08 * w, y + 0.02 * h), (f + 0.06 * w, y), f + 0.34 * w, y, 0.90, ease_out(1.3))
    t.curve((f + 0.84 * w, y), (f + 1.02 * w, y + 0.30 * h), f + 0.98 * w, y + 0.62 * h, 0.30)
    t.curve((f + 0.94 * w, y + 1.04 * h), (f + 0.40 * w, y + 1.10 * h), f + 0.24 * w, y + 0.74 * h, 0.55)
    t.spiral(f + 0.54 * w, y + 0.52 * h, 320 * k, 0.70, 0.30)
    _lift(t, 0.22)
    return Shape([t], (f - 0.15 * w, y + 0.30 * h, -60), (f + w, y, 0))


HANG = X + 40  # the height a hanging bowl hangs from


def _hung(build):
    """The hanging form of a floor bowl: the same skeleton turned over about a level
    line, so its floor becomes a heavy arch hung from the stem near its head at
    ``HANG``, and its counter opens toward the line."""

    def hung(f, y, fl=1.0, **params):
        sh = build(f, y, fl, **params)
        flip = lambda yy: y + HANG - (yy - y)  # noqa: E731
        tracks = []
        for t in sh.tracks:
            n = Track(0, 0, 0)
            n.samples = [(ff, flip(yy), p) for ff, yy, p in t.samples]
            tracks.append(n)
        e, x = sh.entry, sh.exit
        return Shape(tracks, (e[0], flip(e[1]), -e[2]), (x[0], flip(x[1]), -x[2]))

    hung.__doc__ = f"The hanging form of ``{build.__name__}``, turned over and hung from the stem."
    return hung


s_hung_bud = _hung(s_bud)
s_hung_arches = _hung(s_arches)
s_hung_coil = _hung(s_coil)


RISE = 840.0  # the head of the riser, clear above every raised stem


def s_riser(f, y, fl=1.0, h=RISE, arc=0.05, curl=1.0):
    """The riser: one tall stroke with no bowl, rising well above every stem. The pen
    sets down in the heart of an open tendril turned back over the head, unwinds out of
    it onto the top, falls in a gentle arc bowed forward, and turns forward at the
    line into a soft foot that lifts away. The tendril is wide and open where a
    stem's vine curl is small and turned forward, and the fall bows the other way."""
    c = curl * (0.55 + 0.45 * fl)
    top = y + h
    r = 52 * c  # the tendril's outer radius
    cf, cy = f - r, top - r
    r0 = 0.24 * r
    t = Track(cf + r0 * math.cos(math.radians(80)), cy + r0 * math.sin(math.radians(80)), -0.4)
    t.spiral(cf, cy, -440, 1 - r / r0, 0.45, ease_in(1.4))  # winding out of the heart, over the top
    b = arc * h
    t.curve((f + 0.4 * b, top - r - 0.30 * h), (f + b, y + 0.30 * h), f + 8, y + 90, 0.80, ease_in(1.2))
    t.curve((f + 10, y + 30), (f + 30, y - 2), f + 80, y + 2, 0.90)
    t.curve((f + 110, y + 4), (f + 128, y + 10), f + 140, y + 24, 0.20)
    _lift(t, 0.10)
    return Shape([t], (cf, cy, -90), (f + 140, y + 24, 30))


def s_crook(f, y, fl=1.0, w=180, h=X, roll=0.8):
    """A crozier with no stem: from a full foot on the line the pen climbs forward and
    rolls back over at the top into a fern's head, winding inward."""
    r = roll * (0.45 + 0.55 * fl)
    t = Track(f - 0.15 * w, y + 0.06 * h, -0.3)
    t.curve((f, y - 0.02 * h), (f + 0.10 * w, y), f + 0.20 * w, y + 0.06 * h, 0.85)
    top = (f + 0.62 * w, y + 0.92 * h)
    t.curve((f + 0.50 * w, y + 0.30 * h), (f + 0.80 * w, y + 0.62 * h), *top, 0.10)
    t.curve((f + 0.46 * w, y + 1.10 * h), (f + 0.16 * w, y + 0.90 * h), f + 0.24 * w, y + 0.62 * h, 0.55)
    if r > 0.05:
        t.spiral(f + 0.40 * w, y + 0.66 * h, 280 * r, 0.6, 0.30)
    _lift(t, 0.25)
    return Shape([t], (f - 0.15 * w, y + 0.06 * h, 0), (f + w, y, 0))


def s_carrier(f, y, fl=1.0, h=190, arc=0.07):
    """The carrier: a short arcing stem with a curled head, a sign with no sound of its
    own that vowel marks ride on."""
    return s_stem(f, y, fl, top=h, foot=0.0, arc=arc)


def s_touch(f, y, fl=1.0, df=260, dy=40.0, sag=-0.25):
    """A touch: a flowing hairline from one letter to the next, set down from nothing
    and lifted to nothing, where a join is natural. Letters are otherwise separate. A
    negative ``sag`` arches it upward; a positive one dips it."""
    t = Track(f, y, -0.6)
    d = math.hypot(df, dy)
    t.curve((f + df / 3, y + dy / 3 - sag * d), (f + 2 * df / 3, y + 2 * dy / 3 - sag * d), f + df, y + dy, -0.6,
            wave=lambda u: 0.75 * bell(u))
    return Shape([t], (f, y, 0), (f + df, y + dy, 0))


def s_bar(f, y, fl=1.0, l=90, tilt=-28):
    """The length bar beneath a doubled consonant: a short fallen leaf, pointed at
    both ends."""
    a = polar(f, y, -l / 2, tilt)
    b = polar(f, y, l / 2, tilt)
    t = Track(*a, 0.0)
    t.line(*b, 0.0, wave=lambda u: 0.9 * bell(u))
    _land(t, 0.3)
    _lift(t, 0.3)
    return Shape([t], (*a, tilt), (*b, tilt))


# -- the vowel marks ---------------------------------------------------------------------------
#
# A vowel mark is a small cluster of dots, a short dab or a small hook, floating
# with the middle of its foot at (f, y). The marks follow the harmony sets: the back
# vowels are dots, the neutral vowels dabs, the front vowels hooks. ``long`` draws
# the mark on into a hairline running forward, for a long vowel; ``pitch`` adds a
# tail at its forward end, a hairline flick upward for a rise, a fuller flick
# downward for a fall, none for level speech.

SPACE = 104.0  # between the dots of a cluster: a full dot's width clear at text size
DOT = 15.0  # the radius the pen turns the dot at
DAB = 160.0  # the length of a dab
LONG = 110.0  # how far a long vowel's hairline runs on, at long = 2
FLICK = 96.0  # the length of a pitch flick


def _dot(f, y):
    """One dot: the pen set down and turned once in a tight circle, a round dot rather
    than a lozenge."""
    t = Track(f + DOT, y, 0.60)
    t.spiral(f, y, 400, 0.7, 0.50)
    return t


def _tail(t: Track, long: float, pitch: float):
    """Draw a mark on for a long vowel, then add the pitch tail."""
    if long > 1.05:
        f, y, _ = t.end
        e = (f + LONG * (long - 1) + 24, y - 6)
        t.curve((f + 18, y - 14), (e[0] - 26, y - 10), *e, 0.45)
    if abs(pitch) < 0.05:
        return _lift(t, 0.25) if long > 1.05 else t
    f, y, _ = t.end
    if pitch > 0:
        a = 40 + 30 * pitch
        t.curve(polar(f, y, 16, 0), polar(f, y, 34, a - 12), *polar(f, y, FLICK + 16 * pitch, a), 0.40)
    else:
        a = -45 - 30 * abs(pitch)
        t.curve(polar(f, y, 16, 0), polar(f, y, 34, a + 12), *polar(f, y, FLICK + 16 * abs(pitch), a), 0.40,
                wave=lambda u: 0.55 * bell(u))
    return _lift(t, 0.25)


def _cluster(points, long, pitch):
    """Dots at ``points``; the last one, the most forward, carries length and pitch."""
    tracks = [_dot(*p) for p in points]
    _tail(tracks[-1], long, pitch)
    return tracks


def m_one(f, y, fl=1.0, long=1.0, pitch=0.0):
    """_a_: one dot."""
    tr = _cluster([(f, y + 24)], long, pitch)
    return Shape(tr, (f, y + 24, 0), (*tr[-1].end[:2], 0))


def m_two(f, y, fl=1.0, long=1.0, pitch=0.0):
    """_o_: two dots side by side."""
    tr = _cluster([(f - SPACE / 2, y + 24), (f + SPACE / 2, y + 24)], long, pitch)
    return Shape(tr, (f - SPACE / 2, y + 24, 0), (*tr[-1].end[:2], 0))


def m_three(f, y, fl=1.0, long=1.0, pitch=0.0):
    """_u_: three dots in a triangle standing on its point, two above and one below."""
    tr = _cluster([(f - SPACE / 2, y + 24 + 0.80 * SPACE), (f, y + 24), (f + SPACE / 2, y + 24 + 0.80 * SPACE)],
                  long, pitch)
    return Shape(tr, (f, y + 24, 0), (*tr[-1].end[:2], 0))


def _dab(f, y, deg):
    s = polar(f, y + 40, -DAB / 2, deg)
    e = polar(f, y + 40, DAB / 2, deg)
    t = Track(*s, 0.0)
    t.line(*e, 0.0, wave=lambda u: 0.95 * bell(u) ** 0.6)
    _land(t, 0.15)
    return t


def m_dab(f, y, fl=1.0, long=1.0, pitch=0.0):
    """_e_: a long dab rising forward, pointed at both ends; it crosses the nib's edge
    at a slant, so it is lighter than the level dab but holds at text size."""
    t = _tail(_dab(f, y, 38), long, pitch)
    return Shape([t], (f, y, 0), (*t.end[:2], 0))


def m_backdab(f, y, fl=1.0, long=1.0, pitch=0.0):
    """_i_: a long dab lying nearly level, falling a little forward, pointed at both
    ends; it runs across the nib's edge, so it is full."""
    t = _tail(_dab(f, y, -8), long, pitch)
    return Shape([t], (f, y, 0), (*t.end[:2], 0))


def m_hook(f, y, fl=1.0, long=1.0, pitch=0.0):
    """_y_: a hook, a fall whose foot turns forward and up, as wide as it is deep."""
    t = Track(f - 30, y + 170, 0.0)
    t.curve((f - 36, y + 100), (f - 34, y + 20), f + 4, y + 10, 0.95)
    t.curve((f + 50, y + 0), (f + 72, y + 40), f + 74, y + 92, 0.10)
    _land(t, 0.18)
    if long > 1.05 or abs(pitch) >= 0.05:
        _tail(t, long, pitch)
    else:
        _lift(t, 0.22)
    return Shape([t], (f - 30, y + 170, -90), (*t.end[:2], 0))


def m_curl(f, y, fl=1.0, long=1.0, pitch=0.0):
    """_ë_: a curl, a long fall whose foot sweeps forward and climbs back up the full
    height of the mark, turning over toward the fall and stopping short of it, so the
    loop stands open beside the fall with its counter clear."""
    t = Track(f - 40, y + 200, 0.0)
    t.curve((f - 46, y + 120), (f - 44, y + 20), f + 2, y + 6, 0.95)
    t.curve((f + 70, y - 8), (f + 112, y + 60), f + 100, y + 134, 0.55)
    t.curve((f + 90, y + 196), (f + 26, y + 206), f + 14, y + 160, 0.30)
    _land(t, 0.14)
    if long > 1.05 or abs(pitch) >= 0.05:
        _tail(t, long, pitch)
    else:
        _lift(t, 0.12)
    return Shape([t], (f - 40, y + 200, -90), (*t.end[:2], 0))


# -- the inventory -----------------------------------------------------------------------------


@dataclass(frozen=True)
class StrokeType:
    id: str
    name: str
    kind: str  # stem, bowl, letter, join, mark
    build: Callable
    params: dict  # name -> (minimum, default, maximum)
    skeleton: str
    weight: str  # where the stroke is fullest
    entry: str
    exit: str


def _t(*args):
    s = StrokeType(*args)
    return s.id, s


_MARK = {"long": (1.0, 1.0, 2.0), "pitch": (-1.0, 0.0, 1.0)}

STROKES: dict[str, StrokeType] = dict([
    _t("stem", "Stem", "stem", s_stem,
       {"top": (X + 20, X + 60, 760), "foot": (DESC - 60, 0.0, 0.0), "arc": (-0.04, 0.07, 0.14),
        "tail": (0, 0, 2), "reach": (0.4, 1.0, 1.8)},
       "a curl turned forward at the head, a long fall bowed into a shallow arc; below the line, a tail: "
       "the j-like hook, the ezh (a cursive z hung from the line), or the forward sweep",
       "near the foot, and the floor of a tail", "the heart of the head curl", "the foot, or the tail's end"),
    _t("bud", "Bud", "bowl", s_bud, {"w": (240, 300, 380), "h": (200, 250, 300), "seed": (0.0, 0.8, 1.0),
                                    "sweep": (0.0, 0.5, 1.0)},
       "a single bowl open toward the stem: in from behind the stem, a floor along the line, up the far side, "
       "back over the top and down toward the stem, ending short of it in a seed",
       "the floor on the line", "behind the stem, set down", "the heart of the seed"),
    _t("arches", "Arches", "bowl", s_arches,
       {"w": (260, 320, 480), "h": (220, 260, 300), "n": (1, 2, 3), "curl": (0.0, 0.8, 1.0)},
       "arches on a floor: in from behind the stem, one long floor, up the front, back over round arches on "
       "near-upright legs standing on the floor, the last leg curling in just short of it",
       "the floor and the legs", "behind the stem, set down", "the last leg's curl"),
    _t("coil", "Coil", "bowl", s_coil, {"w": (240, 300, 380), "h": (220, 260, 310), "turn": (0.5, 1.0, 1.4)},
       "a tendril: in from behind the stem, a floor along the line, up the far side, back over the top, winding "
       "inward into a spiral that fills the counter",
       "the floor on the line", "behind the stem, set down", "the heart of the spiral"),
    _t("hung-bud", "Hanging bud", "hanging", s_hung_bud,
       {"w": (240, 300, 380), "h": (200, 250, 300), "seed": (0.0, 0.8, 1.0), "sweep": (0.0, 0.5, 1.0)},
       "the bud turned over: a heavy arch hung from the stem's head, down the far side, back under and up "
       "toward the stem, ending in a seed; open toward the line",
       "the arch at the top", "behind the stem, set down", "the heart of the seed"),
    _t("hung-arches", "Hanging arches", "hanging", s_hung_arches,
       {"w": (260, 320, 480), "h": (220, 260, 300), "n": (1, 2, 3), "curl": (0.0, 0.8, 1.0)},
       "the arches turned over: one heavy arch hung from the stem's head with lobes hanging under it, "
       "open toward the line",
       "the arch at the top and the legs", "behind the stem, set down", "the last leg's curl"),
    _t("hung-coil", "Hanging coil", "hanging", s_hung_coil,
       {"w": (240, 300, 380), "h": (220, 260, 310), "turn": (0.5, 1.0, 1.4)},
       "the coil turned over: a heavy arch hung from the stem's head, down the far side and winding back "
       "up into a spiral, open toward the line",
       "the arch at the top", "behind the stem, set down", "the heart of the spiral"),
    _t("riser", "Riser", "letter", s_riser, {"h": (760, RISE, 900), "arc": (-0.02, 0.05, 0.10), "curl": (0.4, 1.0, 1.3)},
       "one tall stroke with no bowl: an open tendril turned back over its head, a long fall bowed gently "
       "forward, a soft foot turning forward on the line",
       "the fall, and the foot on the line", "the heart of the tendril", "the foot, lifted"),
    _t("crook", "Crozier", "letter", s_crook, {"w": (150, 180, 240), "h": (220, X, 330), "roll": (0.0, 0.8, 1.0)},
       "a crozier with no stem: a full foot on the line, a climb forward, a fern's head rolled back over",
       "the foot and the roll", "set down behind it", "the heart of the fern's head"),
    _t("carrier", "Carrier", "letter", s_carrier, {"h": (150, 190, 240), "arc": (-0.04, 0.07, 0.14)},
       "a short arcing stem with a curled head", "the fall", "the heart of the head curl", "the foot"),
    _t("touch", "Touch", "join", s_touch, {"df": (60, 260, 520), "dy": (-160, 40.0, 160), "sag": (-0.5, -0.25, 0.5)},
       "a flowing hairline from one letter to the next, arched above the line or dipped toward it",
       "nowhere: a faint swell", "set down from nothing", "lifted to nothing"),
    _t("bar", "Length bar", "mark", s_bar, {"l": (60, 90, 130), "tilt": (-45, -28, -10)},
       "a short fallen leaf beneath the line", "the middle; pointed at both ends", "set down", "lifted"),
    _t("one", "One dot (a)", "mark", m_one, _MARK, "one dot", "the dot", "set down", "lifted, or the tail"),
    _t("two", "Two dots (o)", "mark", m_two, _MARK, "two dots side by side", "the dots", "set down",
       "lifted, or the tail"),
    _t("three", "Three dots (u)", "mark", m_three, _MARK, "three dots in a triangle on its point", "the dots",
       "set down", "lifted, or the tail"),
    _t("dab", "Rising dab (e)", "mark", m_dab, _MARK, "a long dab rising forward", "the middle", "set down",
       "lifted, or the tail"),
    _t("backdab", "Level dab (i)", "mark", m_backdab, _MARK, "a long dab lying nearly level", "the middle", "set down",
       "lifted, or the tail"),
    _t("hook", "Hook (y)", "mark", m_hook, _MARK, "a dab whose foot turns forward and up", "the dab", "set down",
       "lifted, or the tail"),
    _t("curl", "Curl (ë)", "mark", m_curl, _MARK, "a fall whose foot sweeps forward and winds back up into an open loop", "the fall",
       "set down", "lifted, or the tail"),
])


def shape(sid: str, f: float, y: float, style: Style = HAND, **params) -> Shape:
    """One stroke with its origin at (f, y) in the forward frame."""
    st = STROKES[sid]
    for k, v in params.items():
        if k not in st.params:
            raise ValueError(f"{sid}: no parameter {k!r}; it takes {', '.join(st.params)}")
        lo, _, hi = st.params[k]
        if not lo <= v <= hi:
            raise ValueError(f"{sid}: {k}={v} is outside {lo}..{hi}")
    return st.build(f, y, fl=style.flourish, **params)


def stroke(sid: str, f: float, y: float, style: Style = HAND, **params) -> pathops.Path:
    """The outline of one stroke."""
    return outline(shape(sid, f, y, style, **params).tracks, style)


def contours(path: pathops.Path):
    out, cur = [], []
    for verb, pts in path.segments:
        if verb == "moveTo":
            cur = [pts[0]]
        elif verb == "lineTo":
            cur.append(pts[0])
        elif verb in ("qCurveTo", "curveTo"):
            cur.extend(pts)
        elif verb == "closePath":
            if cur:
                out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out
