# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""The Vedyakshara stroke inventory, as parametric reed strokes that emit outlines.

    import strokes as S

    rope = S.shape("headline", 0, 0, w=400)       # a Shape: tracks, entry and exit
    stem = S.shape("stem", 360, 0)                # hangs from the headline to the line
    path = S.outline(rope.tracks + stem.tracks)   # a pathops.Path, font units, y up

The Vedyakshara runs left to right. Coordinates are font units on a 1000-unit em,
the line at y = 0, drawn at the size the font sets them: the body of a sign hangs
from the underside of the headline at ``X``, the shared x-height, to the line.

**The frame.** A skeleton is written with ``f`` running the way the pen travels,
rightward, and ``y`` up; the hand is upright, so ``to_page`` only applies the
style's slant, which is zero. A stroke's origin is the left end of the headline
segment it hangs from, at the line: its ``f`` is the sign's left edge.

**How a stroke is drawn.** A stroke is one or more *tracks*: a path the reed
follows, sampled every ``STEP`` units, with a *pressure* at every sample. The reed
is broad and cut square, its edge held steep at ``Nib.angle`` on the page, so a
level pull runs across the edge and is the fullest stroke the pen makes, and an
upright pull runs nearly along it and is the lightest. The headline is therefore
the heaviest stroke, the bodies hang beneath it in lighter strokes that swell on
their diagonals and floors, and a stem is a firm thin line. A reed hardly flexes:
``flex`` is small, and the bodies are written at ``BODY_P``, a lighter hand than
the headline. A negative pressure is the reed lifting; the reed ends most strokes
square instead, at its own cut.

The outline is the union of the convex hulls of neighbouring footprints.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Callable

import pathops


# -- metrics -----------------------------------------------------------------------------------

X = 514.0  # the underside of the headline: the body's height, the shared x-height (0.5135 em)
STEP = 4.0  # sampling interval along a track, in units
BODY_P = 0.55  # the pressure the bodies are written at; the headline is written at 1
OVERLAP = 14.0  # how far a hanging stroke starts inside the headline, so the two fuse


# -- nib and style -----------------------------------------------------------------------------


@dataclass(frozen=True)
class Nib:
    width: float  # the edge at full pressure
    thin: float  # the reed's thickness at the cut
    angle: float  # the edge's direction on the page, degrees, counter-clockwise from the right
    flex: float  # how far a light pressure narrows the edge
    square: float = 0.22  # corner softness of the footprint: 0 is a sharp rectangle, 1 an ellipse
    facets: int = 24


@dataclass(frozen=True)
class Style:
    name: str
    nib: Nib
    slant: float = 0.0  # lean in the direction of travel, degrees
    pressure: float = 1.0  # scales every positive pressure the skeletons give


# The classical hand: a broad reed cut square, held steep, upright.
HAND = Style("Vedyakshara", Nib(width=78.0, thin=22.0, angle=75.0, flex=0.30), slant=0.0)


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
    """A reed path: samples of (f, y, pressure)."""

    f: float
    y: float
    p: float
    samples: list = field(default_factory=list)

    def __post_init__(self):
        self.samples = [(self.f, self.y, self.p)]

    @property
    def end(self):
        return self.samples[-1]

    def line(self, f, y, p, ease: Ease = linear):
        f0, y0, p0 = self.end
        n = max(2, math.ceil(math.hypot(f - f0, y - y0) / STEP))
        for i in range(1, n + 1):
            u = i / n
            self.samples.append((f0 + (f - f0) * u, y0 + (y - y0) * u, p0 + (p - p0) * ease(u)))
        return self

    def curve(self, c1, c2, f, y, p, ease: Ease = linear):
        """A cubic Bezier to (f, y); pressure eases to ``p``."""
        f0, y0, p0 = self.end
        approx = math.dist((f0, y0), c1) + math.dist(c1, c2) + math.dist(c2, (f, y))
        n = max(3, math.ceil(approx / STEP))
        for i in range(1, n + 1):
            u = i / n
            a, b, c, d = (1 - u) ** 3, 3 * u * (1 - u) ** 2, 3 * u * u * (1 - u), u**3
            self.samples.append((a * f0 + b * c1[0] + c * c2[0] + d * f, a * y0 + b * c1[1] + c * c2[1] + d * y,
                                 p0 + (p - p0) * ease(u)))
        return self

    def arc(self, cf, cy, rf, ry, a0, a1, p, ease: Ease = linear):
        """Round an ellipse about (cf, cy) from angle ``a0`` to ``a1`` (degrees, positive
        counter-clockwise); the track first runs straight to the arc's start."""
        s = (cf + rf * math.cos(math.radians(a0)), cy + ry * math.sin(math.radians(a0)))
        if math.dist(self.end[:2], s) > 0.5:
            self.line(*s, self.end[2])
        p0 = self.end[2]
        n = max(8, math.ceil(math.radians(abs(a1 - a0)) * max(rf, ry) / STEP))
        for i in range(1, n + 1):
            u = i / n
            t = math.radians(a0 + (a1 - a0) * u)
            self.samples.append((cf + rf * math.cos(t), cy + ry * math.sin(t), p0 + (p - p0) * ease(u)))
        return self


@dataclass
class Shape:
    """A stroke's tracks with the points it is joined at. Headings are degrees: 0 is
    rightward, 90 is up."""

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


# -- geometry ----------------------------------------------------------------------------------


def to_page(f, y, style: Style = HAND):
    """Frame to page: the pen travels rightward; the hand is upright."""
    return f + y * math.tan(math.radians(style.slant)), y


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
    a, b = max(a, 0.8), max(b, 0.8)
    t = math.radians(n.angle)
    ct, st = math.cos(t), math.sin(t)
    pts = []
    for i in range(n.facets):
        s = 2 * math.pi * i / n.facets
        c, si = math.cos(s), math.sin(s)
        ex = a * math.copysign(abs(c) ** n.square, c)  # a square cut with barely softened corners
        ey = b * math.copysign(abs(si) ** n.square, si)
        pts.append((x + ex * ct - ey * st, y + ex * st + ey * ct))
    return pts


def _extent(nib: Nib, heading: float) -> float:
    """The width of the band the nib leaves on a straight pull at ``heading`` degrees."""
    pts = _footprint(0, 0, 1.0, Style("probe", nib))
    t = math.radians(heading + 90)
    nx, ny = math.cos(t), math.sin(t)
    d = [x * nx + y * ny for x, y in pts]
    return max(d) - min(d)


HEAD_W = round(_extent(HAND.nib, 0))  # the headline's weight: a level pull at full pressure
HEAD = X + HEAD_W  # the top of the headline
FLAG = 800.0  # the head of a front-vowel flag
HOOK = -230.0  # the foot of a back-vowel hook and the r-foot
RAIL = HEAD + 12  # the foot of a flag, sunk into the headline's top


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
    """The union of the footprints the reed leaves along the tracks."""
    hulls = []
    for track in tracks:
        prints, last = [], None
        for f, y, p in track.samples:
            x, yy = to_page(f, y, style)
            if last is not None and math.hypot(x - last[0], yy - last[1]) < 0.5:
                continue
            last = (x, yy)
            prints.append([(round(a, 2), round(b, 2)) for a, b in _footprint(x, yy, p, style)])
        if len(prints) == 1:
            hulls.append(_hull(prints[0]))
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


def _lift(t: Track, frac: float = 0.3):
    """Lift the reed over the last ``frac`` of the track, so the stroke thins away."""
    n = len(t.samples)
    k0 = int(n * (1 - frac))
    for i in range(k0, n):
        f, y, p = t.samples[i]
        u = (i - k0) / max(1, n - 1 - k0)
        t.samples[i] = (f, y, p * (1 - u) - 0.7 * u * u)
    return t


# -- the strokes -------------------------------------------------------------------------------
#
# Each builder takes the stroke's origin (f, y), the left end of the headline at the
# line, and its own parameters, and returns a Shape. A hanging stroke sets down
# ``OVERLAP`` inside the headline so the two fuse into one rope.

TOP = X + OVERLAP  # where a hanging stroke sets down, inside the headline


def s_headline(f, y, w=400.0, sag=0.0):
    """The rope: one level pull at full pressure along the top of the body, its
    underside on ``X``. Both ends are the reed's own square cut, standing at the
    reed's angle, so a word's rope begins and ends square and a space breaks it.
    ``sag`` lowers its middle by that many units, for a slack rope."""
    yc = y + X + HEAD_W / 2
    t = Track(f + HEAD_W * 0.13, yc, 1.0)
    if abs(sag) < 0.5:
        t.line(f + w - HEAD_W * 0.13, yc, 1.0)
    else:
        t.curve((f + w / 3, yc - sag * 1.33), (f + 2 * w / 3, yc - sag * 1.33), f + w - HEAD_W * 0.13, yc, 1.0)
    return Shape([t], (f, yc, 0), (f + w, yc, 0))


def s_stem(f, y, depth=1.0, foot=0.0):
    """A stem hanging from the headline: the reed sets down inside the rope and pulls
    straight down. ``depth`` is the share of the body it falls (1 to the line, more
    carries it below); ``foot`` turns its end rightward in a short kick, 0 for the
    reed's square cut."""
    end = y + X - depth * X
    t = Track(f, y + TOP, BODY_P)
    if foot < 0.05:
        t.line(f, end, BODY_P)
    else:
        r = 46 * foot
        t.line(f, end + r, BODY_P)
        t.curve((f, end + 0.3 * r), (f + 0.3 * r, end), f + 1.3 * r, end + 0.15 * r, BODY_P)
    return Shape([t], (f, y + TOP, -90), (*t.end[:2], -90 if foot < 0.05 else 0))


def s_bowl(f, y, w=375.0, h=1.0, close=1.0):
    """A hanging bowl: from under the headline the reed rounds down the left side,
    lays a full floor, climbs the right side and comes back toward the rope. ``h``
    is the share of the body it hangs; at ``close`` 1 it shuts against the headline,
    less leaves it open at the top right, a half form's place to end."""
    hh = h * X
    cf, cy, rf, ry = f + w / 2, y + X - hh / 2 + OVERLAP / 2, w / 2, hh / 2 + OVERLAP / 2
    t = Track(cf, y + TOP, BODY_P)
    t.arc(cf, cy, rf, ry, 90, 90 + 360 * close, BODY_P)
    return Shape([t], (cf, y + TOP, 180), (*t.end[:2], 90))


def s_arc(f, y, w=275.0, h=1.0, side=1, turn=0.4):
    """A hanging arc: an open curve from the headline down one side to a floor, its
    open face toward ``side`` (1 opens right, as a c; -1 opens left). ``turn`` carries
    it on up the open side, 0 ending on the floor and 1 rising to mid-body."""
    hh = h * X
    cf, cy, rf, ry = f + w / 2, y + X - hh / 2 + OVERLAP / 2, w / 2, hh / 2 + OVERLAP / 2
    sweep = 180 + 90 * turn
    if side > 0:
        a0, a1 = 70, 70 + sweep + 20
    else:
        a0, a1 = 110, 110 - sweep - 20
    t = Track(cf + rf * math.cos(math.radians(a0)), y + TOP, BODY_P)
    t.arc(cf, cy, rf, ry, a0, a1, BODY_P)
    return Shape([t], (t.samples[0][0], y + TOP, 180 if side > 0 else 0), (*t.end[:2], 90))


def s_cut(f, y, depth=0.55, lean=0.25, heel=1.0):
    """The half-form cut: where a half form's body ends early. A short spur falls from
    the rope, turned a little forward by ``lean``, and ends in a level heel pulled
    forward, ``heel`` long, at the reed's full width, so the end reads as cut at
    text size rather than unfinished. ``depth`` is the share of the body."""
    end = y + X - depth * X
    t = Track(f, y + TOP, BODY_P)
    t.curve((f, y + TOP - 0.5 * (TOP - end)), (f + 0.3 * lean * 80, end + 20), f + lean * 80, end, BODY_P)
    if heel > 0.05:
        ex = f + lean * 80
        t.curve((ex + 6, end - 10), (ex + 16, end - 14), ex + 26, end - 14, 1.0)
        t.line(ex + 26 + 54 * heel, end - 14, 1.0)
    return Shape([t], (f, y + TOP, -90), (*t.end[:2], 0 if heel > 0.05 else -45))


def s_lobe(f, y, w=260.0, top=0.55, bottom=0.0):
    """A lobe on a stem: from the stem at ``f``, at ``top`` of the body, the reed
    rounds back leftward ``w`` units to a floor at ``bottom`` and returns to the stem,
    so the bowl hangs from the stem rather than from the rope."""
    yt, yb = y + top * X, y + bottom * X
    cy, ry = (yt + yb) / 2, (yt - yb) / 2
    t = Track(f, yt, BODY_P)
    t.curve((f - 0.35 * w, yt + 0.06 * ry), (f - w, cy + 0.9 * ry), f - w, cy, BODY_P)
    t.curve((f - w, cy - 0.9 * ry), (f - 0.35 * w, yb - 0.06 * ry), f, yb + 0.12 * ry, BODY_P)
    return Shape([t], (f, yt, 180), (*t.end[:2], 0))


def s_rung(f, y, w=260.0, at=0.42):
    """A rung: a level pull of ``w`` units ending at a stem at ``f``, at ``at`` of the
    body. Level, it is drawn at the rope's full weight, the heaviest mark in a body."""
    yc = y + at * X
    t = Track(f - w, yc, 0.85)
    t.line(f, yc, 0.85)
    return Shape([t], (f - w, yc, 0), (f, yc, 0))


def s_breath(f, y, size=1.0, at=0.66):
    """The breath curl of the aspirates: from the stem at ``f``, at ``at`` of the body,
    a pull out to the right that rolls down and back into an open hook, its counter
    left wide so it reads as a curl and not a dot at text size."""
    r = 74 * size
    yc = y + at * X
    t = Track(f, yc, BODY_P)
    t.curve((f + 0.7 * r, yc + 0.45 * r), (f + 1.9 * r, yc + 0.4 * r), f + 1.95 * r, yc - 0.45 * r, BODY_P)
    t.curve((f + 2.0 * r, yc - 1.3 * r), (f + 0.9 * r, yc - 1.55 * r), f + 0.55 * r, yc - 1.05 * r, BODY_P)
    return Shape([t], (f, yc, 0), (*t.end[:2], 90))


def s_rstem(f, y, reach=1.0, top=1.0):
    """The stem a fused _r_ rides: the stem falls to the line and sweeps on down and
    back to the left past it, the fall against the edge swelling as it turns. Below
    ``top`` 1 it starts on the body at that share of the body instead of the rope; at
    0 it is a tail from the body's floor, for a sign that has no stem of its own."""
    t = Track(f, y + (TOP if top >= 1 else top * X), BODY_P)
    if t.end[1] > y + 70:
        t.line(f, y + 70, BODY_P)
    ex, ey = f - 150 * reach, y + HOOK + 30
    t.curve((f, y + 10), (f - 30 * reach, ey + 90), ex, ey, BODY_P)
    return Shape([t], (f, y + TOP, -90), (ex, ey, -135))


def s_tick(f, y, w=300.0, drop=230.0):
    """The final tick, the rope cut: the headline pulled at full weight stops short of
    the sign's right edge and turns down and forward in a tick at full pressure. The
    tick falls at about 60° below the line, across the edge, so it keeps half the
    rope's weight and reads at text size. ``w`` is the length of rope before the turn."""
    yc = y + X + HEAD_W / 2
    t = Track(f + HEAD_W * 0.13, yc, 1.0)
    t.line(f + w - 40, yc, 1.0)
    t.curve((f + w - 14, yc), (f + w, yc - 16), f + w + 8, yc - 46, 1.0)
    t.line(f + w + 8 + 0.55 * (drop - 46), yc - drop, 1.0)
    return Shape([t], (f, yc, 0), (*t.end[:2], -60))


def s_flag(f, y, h=FLAG - RAIL, lean=60.0, curl=0.5):
    """A front-vowel flag: a short stroke rising from the top of the headline, leaning
    forward by ``lean``, its head turned forward by ``curl`` into a small pennant.
    The rise runs across the edge more than along it, so it swells as it climbs."""
    t = Track(f, y + RAIL - 8, BODY_P)
    hy = y + RAIL + h
    t.curve((f + 0.1 * lean, y + RAIL + 0.4 * h), (f + 0.6 * lean, hy - 0.2 * h), f + lean, hy, BODY_P)
    if curl > 0.05:
        r = 60 * curl
        t.curve((f + lean + 0.3 * r, hy + 0.25 * r), (f + lean + 1.0 * r, hy + 0.15 * r), f + lean + 1.4 * r,
                hy - 0.4 * r, BODY_P * 0.9)
    return Shape([t], (f, y + RAIL, 90), (*t.end[:2], 0))


def s_hook(f, y, d=-HOOK, turn=0.6, side=1):
    """A back-vowel hook: a short stroke from the body's foot falling below the line,
    its end turned toward ``side`` (1 right, -1 left) and up by ``turn``. The turn
    is a floor, so the hook is fullest where it bends."""
    foot = y - d
    r = 0.42 * d
    t = Track(f, y + 16, BODY_P)
    t.line(f, foot + r, BODY_P)
    t.curve((f, foot + 0.2 * r), (f + side * 0.4 * r, foot), f + side * r, foot, BODY_P)
    if turn > 0.05:
        t.curve((f + side * (r + 0.6 * r * turn), foot), (f + side * (r + 0.9 * r * turn), foot + 0.4 * r * turn),
                f + side * (r + 0.9 * r * turn), foot + 1.0 * r * turn, BODY_P)
    return Shape([t], (f, y + 16, -90), (*t.end[:2], 90))


def s_rfoot(f, y, l=150.0, angle=-120.0):
    """The r-foot, r after a consonant: a short stroke at the body's foot on the left,
    drawn down and back at ``angle`` degrees. Falling against the edge, it is nearly
    the reed's full width, so it reads below the line beside the hooks."""
    t = Track(f, y + 20, BODY_P)
    ex, ey = f + l * math.cos(math.radians(angle)), y + 20 + l * math.sin(math.radians(angle))
    t.curve((f - 10, y), (ex + 30, ey + 30), ex, ey, BODY_P)
    return Shape([t], (f, y + 20, -90), (ex, ey, angle))


def s_dot(f, y, size=1.0):
    """The soft dot: the reed set down and turned a quarter in place, a small square-
    shouldered dot set inside a body's counter."""
    s = 10 * size
    t = Track(f - s, y - s * 0.3, BODY_P * 0.8)
    t.line(f + s, y + s * 0.3, BODY_P * 0.8)
    return Shape([t], (f, y, 0), (f, y, 0))


def s_bar(f, y, h=1.0, knots=0):
    """The punctuation bar: a short upright length of rope standing alone on the line,
    as tall as the body and the headline together, by ``h``. ``knots`` ties one or two
    knots in it: one for the pause, two for the end of a sentence."""
    top = y + h * (HEAD - 20)
    t = Track(f, top, BODY_P)
    t.line(f, y, BODY_P)
    tracks = [t]
    k = int(round(knots))
    for i in range(k):
        cy = y + (HEAD - 20) * h * (0.5 if k == 1 else (0.36 + 0.30 * i))
        n = Track(f + 4, cy + 32, BODY_P)
        n.arc(f + 4, cy, 34, 32, 90, 90 + 360, BODY_P)
        tracks.append(n)
    return Shape(tracks, (f, top, -90), (f, y, -90))


# -- the inventory -----------------------------------------------------------------------------


@dataclass(frozen=True)
class StrokeType:
    id: str
    name: str
    kind: str  # rope, body, mark, point
    build: Callable
    params: dict  # name -> (minimum, default, maximum)
    skeleton: str
    weight: str  # where the stroke is fullest


def _t(*args):
    s = StrokeType(*args)
    return s.id, s


STROKES: dict[str, StrokeType] = dict([
    _t("headline", "Headline", "rope", s_headline, {"w": (120.0, 400.0, 900.0), "sag": (0.0, 0.0, 12.0)},
       "one level pull along the top of the body, its underside on the x-height, square-cut at both ends",
       "everywhere: the heaviest stroke"),
    _t("tick", "Final tick", "rope", s_tick, {"w": (160.0, 300.0, 700.0), "drop": (120.0, 230.0, 280.0)},
       "the headline stopping short of the sign's right edge and turning down: the rope cut",
       "the rope; the tick is light"),
    _t("stem", "Stem", "body", s_stem, {"depth": (0.5, 1.0, 1.25), "foot": (0.0, 0.0, 1.0)},
       "an upright fall hanging from the headline to the line, ending square or kicked forward",
       "nowhere: a firm thin line"),
    _t("bowl", "Hanging bowl", "body", s_bowl, {"w": (200.0, 375.0, 550.0), "h": (0.45, 1.0, 1.0),
                                                "close": (0.6, 1.0, 1.0)},
       "from under the headline, down the left side, a floor, up the right side and back to the rope",
       "the floor and the shoulders"),
    _t("arc", "Hanging arc", "body", s_arc, {"w": (150.0, 275.0, 450.0), "h": (0.45, 1.0, 1.0), "side": (-1, 1, 1),
                                             "turn": (0.0, 0.4, 1.0)},
       "an open curve from the headline down one side to a floor, open toward one side, turning up it",
       "the floor"),
    _t("cut", "Half-form cut", "body", s_cut, {"depth": (0.25, 0.55, 0.7), "lean": (0.0, 0.25, 0.6),
                                                     "heel": (0.0, 1.0, 1.5)},
       "a short spur falling from the rope and ending in a level heel pulled forward",
       "the turn at its end"),
    _t("lobe", "Lobe", "body", s_lobe, {"w": (150.0, 260.0, 400.0), "top": (0.3, 0.55, 1.0), "bottom": (0.0, 0.0, 0.6)},
       "a bowl hung from a stem: from the stem, round back to a floor and return to the stem",
       "the floor"),
    _t("rung", "Rung", "body", s_rung, {"w": (80.0, 260.0, 450.0), "at": (0.2, 0.42, 0.8)},
       "a level pull ending at a stem, inside or below a body",
       "everywhere: level, near the rope's weight"),
    _t("rstem", "R-stem", "body", s_rstem, {"reach": (0.6, 1.0, 1.4), "top": (0.0, 1.0, 1.0)},
       "the stem a fused r rides: falling to the line and sweeping on down and back below it; from the rope, or from a body's floor",
       "the sweep below the line"),
    _t("breath", "Breath curl (kh, gh, bh)", "mark", s_breath, {"size": (0.7, 1.0, 1.3), "at": (0.4, 0.62, 0.8)},
       "from the stem, a pull out to the right rolling down and back into an open hook",
       "the roll"),
    _t("flag", "Flag (i, e)", "mark", s_flag, {"h": (140.0, FLAG - RAIL, 240.0), "lean": (0.0, 60.0, 120.0),
                                               "curl": (0.0, 0.5, 1.0)},
       "a short stroke rising forward from the top of the headline, its head turned forward",
       "the rise"),
    _t("hook", "Hook (u, o)", "mark", s_hook, {"d": (160.0, -HOOK, 260.0), "turn": (0.0, 0.6, 1.0),
                                               "side": (-1, 1, 1)},
       "a short fall from the body's foot below the line, its end turned aside and up",
       "the bend"),
    _t("rfoot", "R-foot", "mark", s_rfoot, {"l": (100.0, 150.0, 200.0), "angle": (-150.0, -120.0, -100.0)},
       "a short stroke from the body's foot, down and back to the left",
       "the whole stroke: it falls against the edge"),
    _t("dot", "Soft dot (f)", "mark", s_dot, {"size": (0.7, 1.0, 1.4)},
       "the reed set down and turned in place, inside a body's counter",
       "the dot"),
    _t("bar", "Punctuation bar", "point", s_bar, {"h": (0.7, 1.0, 1.0), "knots": (0, 0, 2)},
       "a short upright length of rope standing alone on the line, with none, one or two knots tied in it",
       "the knots"),
])


def shape(sid: str, f: float, y: float, style: Style = HAND, **params) -> Shape:
    """One stroke with its origin at (f, y)."""
    st = STROKES[sid]
    for k, v in params.items():
        if k not in st.params:
            raise ValueError(f"{sid}: no parameter {k!r}; it takes {', '.join(st.params)}")
        lo, _, hi = st.params[k]
        if not lo <= v <= hi:
            raise ValueError(f"{sid}: {k}={v} is outside {lo}..{hi}")
    return st.build(f, y, **params)


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
