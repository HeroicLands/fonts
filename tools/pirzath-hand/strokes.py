# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""The Pirzath Hand stroke inventory, as parametric strokes of a blunt tool that emit outlines.

    import strokes as S

    tent = S.shape("tent", 0, 0, heel=1)          # a Shape: tracks, entry and exit
    cut = S.shape("cut", 560, 0, fall=-1)         # a back fall
    path = S.outline(tent.tracks + cut.tracks)    # a pathops.Path, font units, y up

Pirzath Hand runs left to right with a slight forward lean. Coordinates are font
units on a 1000-unit em, the line at y = 0, drawn at the size the font sets them, so
the font takes the outlines unscaled.

**The body.** The hand has no capitals and few extenders, so nearly all of its ink
stands in one band, the body, from the line to ``BODY``. A line of Latin is read at
the size its capitals and ascenders give it, not at its x-height, so the body stands
at Latin's cap height, ``BODY`` = 0.73 em, as Pirzath Carved's consonants do. A
vowel stands at ``VOWEL``, about Latin's x-height.

**The frame.** A skeleton is written with ``f`` running the way the tool travels,
rightward, and ``y`` up. ``to_page`` applies the hand's slant, which is zero: the
hand stands upright. A stroke's origin is the left foot
of its ink on the line unless its docstring says otherwise.

**The tool.** The hand is written in chalk on a shaft wall, on a slab of slate, or in
pencil on a scrap of paper, so its tool is blunt: the squared end of a chalk stick or
a broad carpenter's pencil, held at ``Pen.angle`` to the line. Its end is a little
wider than it is thick, so a stroke's weight follows its direction only mildly: a
diagonal falling forward (``\\``) or an upright is the fullest, a stroke rising at the
tool's own angle the lightest, and the two differ by less than two to one. Every
letter must read as if written monoline; the contrast is what the tool gives and is
never what tells two letters apart. Chalk does not flex: ``flex`` is small. At every
sample the tool leaves a footprint with soft corners, and the outline is the union of
the convex hulls of neighbouring footprints.

**Turns.** The hand does not loop. Where a stroke changes direction the tool pivots
through a small turn of radius ``turn``: decisive, but blunt, as a chalk point makes
it, never a needle-sharp angle.

**Ink edges.** A stroke's parameters name where its ink ends, not where its
centreline runs: a stem with ``top=BODY`` has its ink at the body's top. ``HALF_H`` and
``HALF_W`` are the tool's half extents, up and across, that the skeletons inset by.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Callable

import pathops


# -- metrics -----------------------------------------------------------------------------------

BODY = 730.0  # a consonant's body: Latin's cap height, 0.73 em, the carved consonants' height
VOWEL = 460.0  # a vowel's body, 0.63 of a consonant's, as the carved face scores its vowels small
LATIN_X = 513.5  # the shared x-height, 0.5135 em: a guide, which the vowels stand near
ASC = 870.0  # the head of a rising stroke: a fifth of the body above it
DESC = -175.0  # the foot of a descending stroke, inside the shared descent of 200
LENGTH_Y = VOWEL + 120.0  # the height of the length bar over a vowel
MID = 0.45 * BODY  # the height the marks between words stand at
STEP = 4.0  # sampling interval along a track, in units
TURN = 18.0  # the radius the tool pivots on in a turn: small, and blunt

# The shared line metrics of tools/vertical.py, which the font takes.
ASCENT, DESCENT, LINE_GAP = 945, -200, 100


# -- pen and style -----------------------------------------------------------------------------


@dataclass(frozen=True)
class Pen:
    width: float  # the end's width: the thickest stroke the tool makes, near enough
    thin: float  # the end's thickness: the lightest
    angle: float  # the edge's direction on the page, degrees, counter-clockwise from the right
    flex: float = 0.10  # how far a light pressure narrows the edge
    square: float = 0.5  # corner softness of the footprint: 0 a sharp rectangle, 1 an ellipse
    facets: int = 24


@dataclass(frozen=True)
class Style:
    name: str
    pen: Pen
    slant: float = 0.0  # forward lean of the frame's upright, degrees


# The common hand: a blunt squared tool, chalk or a carpenter's pencil, held at 45°,
# upright.
HAND = Style("Pirzath Hand", Pen(width=74.0, thin=46.0, angle=45.0), slant=0.0)


def _footprint(x, y, p, style: Style):
    n = style.pen
    if p < 0:
        k = max(0.0, 1 + p)  # lifting off the page
        p = 0.0
    else:
        k = 1.0
        p = min(1.0, p)
    a = max(0.8, k * n.width * (1 - n.flex + n.flex * p) / 2)
    b = max(0.8, k * n.thin / 2)
    t = math.radians(n.angle)
    ct, st = math.cos(t), math.sin(t)
    pts = []
    for i in range(n.facets):
        s = 2 * math.pi * i / n.facets
        c, si = math.cos(s), math.sin(s)
        ex = a * math.copysign(abs(c) ** n.square, c)
        ey = b * math.copysign(abs(si) ** n.square, si)
        pts.append((x + ex * ct - ey * st, y + ex * st + ey * ct))
    return pts


def extent(heading: float, style: Style = HAND) -> float:
    """The width of the band the tool leaves on a straight pull at ``heading`` degrees,
    measured on the page."""
    pts = _footprint(0, 0, 1.0, style)
    t = math.radians(heading + 90)
    nx, ny = math.cos(t), math.sin(t)
    d = [x * nx + y * ny for x, y in pts]
    return max(d) - min(d)


def _half(style: Style = HAND):
    pts = _footprint(0, 0, 1.0, style)
    return max(abs(x) for x, _ in pts), max(abs(y) for _, y in pts)


HALF_W, HALF_H = _half()


# -- tracks ------------------------------------------------------------------------------------


@dataclass
class Track:
    """A pen path in the frame: samples of (f, y, pressure)."""

    f: float
    y: float
    p: float = 1.0
    samples: list = field(default_factory=list)

    def __post_init__(self):
        self.samples = [(self.f, self.y, self.p)]

    @property
    def end(self):
        return self.samples[-1][:2]

    def line(self, f, y, p=None):
        f0, y0, p0 = self.samples[-1]
        p = p0 if p is None else p
        n = max(2, math.ceil(math.hypot(f - f0, y - y0) / STEP))
        for i in range(1, n + 1):
            u = i / n
            self.samples.append((f0 + (f - f0) * u, y0 + (y - y0) * u, p0 + (p - p0) * u))
        return self

    def curve(self, c1, c2, f, y, p=None):
        """A cubic Bezier to (f, y)."""
        f0, y0, p0 = self.samples[-1]
        p = p0 if p is None else p
        approx = math.dist((f0, y0), c1) + math.dist(c1, c2) + math.dist(c2, (f, y))
        n = max(3, math.ceil(approx / STEP))
        for i in range(1, n + 1):
            u = i / n
            a, b, c, d = (1 - u) ** 3, 3 * u * (1 - u) ** 2, 3 * u * u * (1 - u), u**3
            self.samples.append((a * f0 + b * c1[0] + c * c2[0] + d * f, a * y0 + b * c1[1] + c * c2[1] + d * y,
                                 p0 + (p - p0) * u))
        return self

    def through(self, points, turn=TURN, p=None):
        """Straight runs through ``points``, the tool pivoting on a turn of radius
        ``turn`` at each corner: the hand's way of changing direction."""
        pts = [self.end] + [tuple(q) for q in points]
        for i in range(1, len(pts)):
            v = pts[i]
            if i == len(pts) - 1:
                self.line(*v, p)
                break
            a, b = pts[i - 1], pts[i + 1]
            la, lb = math.dist(a, v), math.dist(b, v)
            r = min(turn, la / 2, lb / 2)
            if r < 0.5:
                self.line(*v, p)
                continue
            p1 = (v[0] + (a[0] - v[0]) * r / la, v[1] + (a[1] - v[1]) * r / la)
            p2 = (v[0] + (b[0] - v[0]) * r / lb, v[1] + (b[1] - v[1]) * r / lb)
            self.line(*p1, p)
            c1 = (p1[0] + 2 / 3 * (v[0] - p1[0]), p1[1] + 2 / 3 * (v[1] - p1[1]))
            c2 = (p2[0] + 2 / 3 * (v[0] - p2[0]), p2[1] + 2 / 3 * (v[1] - p2[1]))
            self.curve(c1, c2, *p2, p)
        return self


@dataclass
class Shape:
    """A stroke's tracks, with the points the tool enters and leaves by, in the frame."""

    tracks: list
    entry: tuple  # (f, y)
    exit: tuple  # (f, y)

    def moved(self, df, dy):
        tracks = []
        for t in self.tracks:
            n = Track(0, 0)
            n.samples = [(f + df, y + dy, p) for f, y, p in t.samples]
            tracks.append(n)
        return Shape(tracks, (self.entry[0] + df, self.entry[1] + dy), (self.exit[0] + df, self.exit[1] + dy))


def combine(*shapes: Shape) -> Shape:
    """Several strokes as one shape: the first one's entry, the last one's exit."""
    return Shape([t for s in shapes for t in s.tracks], shapes[0].entry, shapes[-1].exit)


# -- outlines ----------------------------------------------------------------------------------


def heading(df, dy, style: Style = HAND) -> float:
    """The page direction, degrees, of a frame displacement (df, dy)."""
    x, yy = to_page(df, dy, style)
    return math.degrees(math.atan2(yy, x))


def to_page(f, y, style: Style = HAND):
    """Frame to page: the frame's upright leans forward by the slant."""
    return f + y * math.tan(math.radians(style.slant)), y


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


def _polys(polys):
    path = pathops.Path()
    for poly in polys:
        path.moveTo(*poly[0])
        for q in poly[1:]:
            path.lineTo(*q)
        path.close()
    return path


def _track_hulls(track, style):
    prints, last, hulls = [], None, []
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
    return hulls


def outline(tracks, style: Style = HAND) -> pathops.Path:
    """The union of the footprints the tool leaves along the tracks. Each track is
    united on its own and the tracks then united together; contours of negligible area,
    which skia can leave behind where two hulls meet edge on, are dropped."""
    out = pathops.Path()
    for track in tracks:
        part = _clean(_simplified(_track_hulls(track, style)))
        out = pathops.op(out, part, pathops.PathOp.UNION)
    return _clean(out)


def _simplified(polys):
    """The union of ``polys``, in chunks, and one at a time where skia cannot take a
    chunk together."""
    part = _polys(polys)
    try:
        part.simplify(fix_winding=True)
        return part
    except pathops.PathOpsError:
        out = pathops.Path()
        for i in range(0, len(polys), 40):
            chunk = _polys(polys[i:i + 40])
            try:
                chunk.simplify(fix_winding=True)
            except pathops.PathOpsError:
                chunk = pathops.Path()
                for poly in polys[i:i + 40]:
                    chunk = pathops.op(chunk, _polys([poly]), pathops.PathOp.UNION)
            out = pathops.op(out, chunk, pathops.PathOp.UNION)
        return out


SLIVER = 40.0  # the area, in square units, below which a contour is debris


def _clean(path: pathops.Path) -> pathops.Path:
    """``path`` without the contours whose area is below ``SLIVER``."""
    keep = [c for c in contours(path) if len(c) >= 3 and _area(c) >= SLIVER]
    out = _polys(keep)
    try:
        out.simplify(fix_winding=True)
    except pathops.PathOpsError:
        pass
    return out


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


# -- the strokes -------------------------------------------------------------------------------
#
# Each builder takes the stroke's origin (f, y) and its own parameters and returns a
# Shape. Unless a docstring says otherwise the origin is the left foot of the stroke's
# ink on the line, and the stroke is written as the scribe writes it: down where it
# can, the tool never leaving the page inside one stroke.
#
# The hand is printed: each letter stands apart, made in its own one or two strokes
# and at most three, with open counters and nothing inside a counter. Every stroke is
# a straight line or the one plain curve, the round: a letter changes direction only
# at a clear corner where two straight runs meet, never inside a run, because on rough
# rock in chalk a small change of direction is lost or turns into a wobble. A
# ``heel`` is such a second run, a plain base along the line. Only the length bar, the
# doubling mark and a digit's tally strokes stand apart.
#
# Every part of a letter is either a full stroke, at least ``FULL`` long, that a
# hurried hand still makes deliberately, or it is absent. There are no flicks, ticks,
# stubs or short heels: a hand writing in chalk on the ground drops them. A part that
# could be left off with the letter still distinct goes; a part the letter needs is
# made full-size.

IN = 0.55  # how far, as a share of HALF_W, a diagonal's track is inset from its ink box
FULL = 0.5 * BODY  # the shortest part a letter may have: a stroke a hurried chalk hand still makes
HEEL = FULL  # the length of a heel: a full base along the line


def _heel(track: Track, heel: int = 0, side: int = -1):
    """With ``heel``, turn a track at its foot through a clear corner into a plain base
    along the line, back (``side`` -1) or forward (1), half the body long: a full
    second run that tells one letter from another on a rough wall."""
    if not heel:
        return track
    f, y = track.end
    r = math.radians(180 if side < 0 else 0)
    track.samples = track.samples[:-1]
    track.through([(f, y), (f + HEEL * math.cos(r), y + HEEL * math.sin(r))], TURN)
    return track


def s_stem(f, y, top=BODY, foot=0.0, heel=0, side=-1):
    """An upright: the tool set down square at the head and pulled straight down. Its
    foot is the tool's square end, or a ``heel`` run along the line,
    back (``side`` -1) or forward (1). A stem may stand to the ascender or fall to the
    descender. ``f`` is the stem's centre."""
    t = Track(f, y + top - HALF_H).line(f, y + foot + HALF_H)
    t = _heel(t, heel, side)
    return Shape([t], (f, y + top), t.end)


def s_cut(f, y, w=0.45 * BODY, h=BODY, top=BODY, fall=1, heel=0, side=-1):
    """A straight diagonal, the hand's form of a rune's cut, written from its head down:
    falling forward (``fall`` 1, ``\\``), the fullest stroke the tool makes, or falling
    back (-1, ``/``), a little lighter. Its ink fills the box ``w`` wide from ``f``,
    from ``top - h`` to ``top``. ``heel`` turns the foot into a base along the line,
    back (``side`` -1) or forward (1)."""
    a, b = f + IN * HALF_W, f + w - IN * HALF_W
    hi, lo = y + top - HALF_H, y + top - h + HALF_H
    p, q = ((a, hi), (b, lo)) if fall > 0 else ((b, hi), (a, lo))
    t = _heel(Track(*p).line(*q), heel, side)
    return Shape([t], p, t.end)


def s_tent(f, y, w=0.66 * BODY, h=BODY, peak=0.42, turn=TURN, left=1.0, heel=0, side=1):
    """The tent, the carved ``Λ`` as the tool writes it: from the left foot up a rising
    diagonal to the apex and, pivoting there, down a forward fall to the right foot. The
    rise is a little lighter than the fall, so the tent leans on its right leg, and
    ``peak`` below one half sets the apex back, so its legs are uneven. ``left`` is the
    share of the left leg written, down from the apex: at one half and above it stays
    a full stroke. ``heel`` turns the right leg's foot into a base, forward (``side``
    1), so it never closes the tent, or back (-1)."""
    a, b = f + IN * HALF_W, f + w - IN * HALF_W
    apex = (a + (b - a) * peak, y + h - HALF_H)
    p = (apex[0] + (a - apex[0]) * left, apex[1] + (y + HALF_H - apex[1]) * left)
    q = (b, y + HALF_H)
    t = Track(*p).through([apex, q], turn)
    t = _heel(t, heel, side)
    return Shape([t], p, t.end)


def s_trough(f, y, w=0.66 * BODY, h=BODY, base=0.4, rise=0.82, turn=TURN):
    """The trough, the carved ``V``: from the left head down a forward fall to the base
    and, pivoting there, up a lighter arm to the right head. ``base`` below one half and
    ``rise`` below one make it uneven: the point sits back and the right arm stands
    short."""
    a, b = f + IN * HALF_W, f + w - IN * HALF_W
    p = (a, y + h - HALF_H)
    pt = (a + (b - a) * base, y + HALF_H)
    t = Track(*p).through([pt, (b, y + rise * h - HALF_H)], turn)
    return Shape([t], (a, y + h), t.end)


def s_point(f, y, w=0.42 * BODY, h=BODY, at=0.6, side=1, turn=TURN, heel=0, upper=1.0, lower=1.0, away=0):
    """The point, the carved ``>``: from the head down to the point at ``at`` of the
    height and, pivoting there, down and back to the foot. ``side`` 1 points forward;
    -1 points back and opens forward (``<``). The point stands narrow, so its lower arm
    falls steeper than the tool's angle and keeps its weight. ``heel`` turns the
    foot into a base along the line under the open side, or, with ``away``, out from
    the point on the other side. ``upper`` and ``lower`` are
    the share of each arm written, from the point outward; a shortened arm stays at
    least half its length, a full stroke."""
    a, b = f + IN * HALF_W, f + w - IN * HALF_W
    near, far = (a, b) if side > 0 else (b, a)
    mid = y + HALF_H + (h - 2 * HALF_H) * at
    head, foot = (near, y + h - HALF_H), (near, y + HALF_H)
    m = (far, mid)
    p = (m[0] + (head[0] - m[0]) * upper, m[1] + (head[1] - m[1]) * upper)
    q = (m[0] + (foot[0] - m[0]) * lower, m[1] + (foot[1] - m[1]) * lower)
    t = Track(*p).through([m, q], turn)
    t = _heel(t, heel, -side if away else side)
    return Shape([t], p, t.end)


def s_roof(f, y, w=0.55 * BODY, h=BODY, lean=0.0, turn=TURN, heel=0, side=-1, hand=1, foot=0.0):
    """The roof: one movement along the top and, pivoting at its end, down to the foot.
    With ``hand`` 1 the head runs forward and falls at the right; with -1 it runs back
    from the right and falls at the left. The level run is as full as a stem, so the
    roof is a solid head. ``lean`` sets the foot forward (+) or back (-) of the head's
    end as a share of the width; ``foot`` carries the fall below the line; the foot may
    take a ``heel`` along the line, back (``side`` -1) or forward (1)."""
    a, b = f + IN * HALF_W, f + w - IN * HALF_W
    if hand < 0:
        a, b = b, a
    top = y + h - HALF_H
    t = Track(a, top).through([(b, top), (b + lean * w, y + foot + HALF_H)], turn)
    t = _heel(t, heel, side)
    return Shape([t], (a, y + h), t.end)


def s_zigzag(f, y, w=0.7 * BODY, h=BODY, turns=2, start=1, turn=TURN):
    """A run of angular turns in one movement, between the line and the head: from the
    line up (``start`` 1) or from the head down (-1), pivoting ``turns`` times. Two
    frames written as one movement wear into this."""
    a, b = f + IN * HALF_W, f + w - IN * HALF_W
    n = int(round(turns)) + 1
    lo, hi = y + HALF_H, y + h - HALF_H
    pts = [(a + (b - a) * i / n, (lo if (i % 2 == 0) == (start > 0) else hi)) for i in range(n + 1)]
    t = Track(*pts[0]).through(pts[1:], turn)
    return Shape([t], pts[0], t.end)


def s_round(f, y, w=0.62 * BODY, h=0.62 * BODY, square=0.0):
    """The round: a plain oval written in one movement from its head, back and down,
    round the foot and up the fore side to close where it began. The only closed shape
    the hand makes, and nothing stands inside it. Its weight swings with the tool: full
    on the back and fore sides where they fall across the tool's end, lighter where they run
    along it. ``square`` flattens it toward a rounded box, 0 for a true oval."""
    rx, ry = w / 2 - HALF_W, h / 2 - HALF_H
    cx, cy = f + w / 2, y + h / 2
    e = 2 / (2 + 6 * square)  # the superellipse exponent: 1 an ellipse, smaller squarer
    pts = []
    for i in range(0, 361, 3):
        a = math.radians(90 + i)
        c, sn = math.cos(a), math.sin(a)
        pts.append((cx + rx * math.copysign(abs(c) ** e, c), cy + ry * math.copysign(abs(sn) ** e, sn)))
    t = Track(*pts[0])
    for q in pts[1:]:
        t.line(*q)
    return Shape([t], (cx, y + h), (cx, y + h))


def s_cross(f, y, w=0.6 * BODY, h=BODY, lean=0.1):
    """The cross, the carved ``X``: the forward fall, then the back fall over it.
    ``lean`` shifts the crossing toward the fore side as a share of the width, so the
    two cuts are uneven."""
    a, b = f + IN * HALF_W, f + w - IN * HALF_W
    top, bot = y + h - HALF_H, y + HALF_H
    d = lean * (b - a) / 2
    one = Track(a + d, top).line(b - d, bot)
    two = Track(b + d, top).line(a - d, bot)
    return Shape([one, two], (a + d, y + h), (a - d, y))


def s_notch(f, y, length=FULL, angle=120.0, at=0.5 * BODY):
    """A free cut, full-size like every other part: a numeral's tally strokes, and the
    doubling mark, laid shallow under a letter. ``f`` and ``at`` are its centre; ``angle`` is its direction in the frame,
    counter-clockwise from the right, and decides its weight with the tool's angle."""
    r = math.radians(angle)
    dx, dy = (length / 2 - HALF_H) * math.cos(r), (length / 2 - HALF_H) * math.sin(r)
    t = Track(f - dx, y + at - dy).line(f + dx, y + at + dy)
    return Shape([t], t.samples[0][:2], t.end)


def s_bar(f, y, w=FULL, at=MID, tilt=0.0):
    """A level stroke drawn forward at height ``at``, rising ``tilt`` degrees, full-size:
    the sentence end, the dash, and the length bar over a vowel. Its ink runs from ``f``
    to ``f + w``."""
    dy = (w - 2 * HALF_W) * math.tan(math.radians(tilt))
    t = Track(f + HALF_W, y + at - dy / 2).line(f + w - HALF_W, y + at + dy / 2)
    return Shape([t], t.samples[0][:2], t.end)


# -- the inventory -----------------------------------------------------------------------------


@dataclass(frozen=True)
class StrokeType:
    id: str
    name: str
    kind: str  # stem, frame, mark
    build: Callable
    params: dict  # name -> (minimum, default, maximum)
    skeleton: str
    weight: str  # where the stroke is fullest
    entry: str
    exit: str


def _t(*args):
    s = StrokeType(*args)
    return s.id, s


SIDE = (-1, 1, 1)  # a choice of -1 or 1
FLAG = (0, 0, 1)  # off or on
B = BODY

STROKES: dict[str, StrokeType] = dict([
    _t("stem", "Stem", "stem", s_stem,
       {"top": (0.4 * B, B, ASC), "foot": (DESC, 0.0, 0.95 * B), "heel": FLAG,
        "side": (-1, -1, 1)},
       "an upright set down square and pulled straight down, to the ascender or the descender if need be",
       "all of it", "the tool's square end", "the square end or a heel along the line"),
    _t("cut", "Cut", "frame", s_cut,
       {"w": (0.1 * B, 0.45 * B, 0.8 * B), "h": (0.3 * B, B, ASC - DESC), "top": (0.3 * B, B, ASC), "fall": SIDE,
        "heel": FLAG, "side": (-1, -1, 1)},
       "a straight diagonal written from its head down, falling forward or back",
       "the forward fall; the back fall is a little lighter", "the tool's end", "the tool's end"),
    _t("tent", "Tent", "frame", s_tent,
       {"w": (0.4 * B, 0.66 * B, 0.9 * B), "h": (0.5 * VOWEL, B, ASC), "peak": (0.3, 0.42, 0.6),
        "turn": (0.0, TURN, 30.0), "left": (0.5, 1.0, 1.0), "heel": FLAG, "side": (-1, 1, 1)},
       "up a rising diagonal to a pointed apex set back of centre, pivot, and down a forward fall",
       "the right leg", "the left foot", "the right foot, or a heel"),
    _t("trough", "Trough", "frame", s_trough,
       {"w": (0.45 * B, 0.66 * B, 0.9 * B), "h": (0.5 * VOWEL, B, ASC), "base": (0.15, 0.4, 0.6), "rise": (0.5, 0.82, 1.0),
        "turn": (0.0, TURN, 30.0)},
       "down a forward fall to a pointed base set back of centre, pivot, and up a shorter, lighter arm",
       "the left arm", "the left head", "the right head"),
    _t("point", "Point", "frame", s_point,
       {"w": (0.3 * B, 0.42 * B, 0.7 * B), "h": (0.5 * VOWEL, B, ASC - DESC), "at": (0.4, 0.6, 0.7), "side": SIDE,
        "turn": (0.0, TURN, 30.0), "heel": FLAG, "upper": (0.5, 1.0, 1.0), "lower": (0.5, 1.0, 1.0),
        "away": FLAG},
       "down to a point at the fore (or back) side, pivot, and down again to the foot, standing narrow",
       "the upper arm of >, the lower arm of <", "the head", "the foot or a heel along the line"),
    _t("roof", "Roof", "frame", s_roof,
       {"w": (0.3 * B, 0.55 * B, 0.8 * B), "h": (0.5 * VOWEL, B, ASC), "lean": (-0.3, 0.0, 0.3),
        "turn": (0.0, TURN, 30.0), "heel": FLAG, "side": (-1, -1, 1), "hand": SIDE, "foot": (DESC, 0.0, 0.0)},
       "one movement: along the top, forward or back, pivot, and down to the foot",
       "the head and the fall alike", "the head's left end", "the foot, or a heel"),
    _t("zigzag", "Zigzag", "frame", s_zigzag,
       {"w": (0.5 * B, 0.7 * B, 1.1 * B), "h": (0.5 * VOWEL, B, ASC), "turns": (2, 2, 4), "start": SIDE,
        "turn": (0.0, TURN, 30.0)},
       "one movement of angular turns between the line and the head, from the line up or the head down",
       "the forward falls", "the first end", "the last end"),
    _t("round", "Round", "frame", s_round,
       {"w": (0.35 * B, 0.62 * B, 0.85 * B), "h": (0.5 * VOWEL, 0.62 * B, B), "square": (0.0, 0.0, 0.4)},
       "a plain oval in one movement from the head, back, round the foot and up to close: the only closed shape",
       "the back and fore sides", "the head", "the head"),
    _t("cross", "Cross", "frame", s_cross,
       {"w": (0.35 * B, 0.6 * B, 0.8 * B), "h": (0.5 * VOWEL, B, ASC), "lean": (-0.3, 0.1, 0.3)},
       "two diagonals crossing: the forward fall, then the back fall over it",
       "the forward fall", "the head of the first cut", "the foot of the second"),
    _t("notch", "Notch", "mark", s_notch,
       {"length": (FULL, FULL, 0.7 * B), "angle": (0.0, 120.0, 175.0), "at": (DESC, 0.5 * B, ASC)},
       "a free straight cut, full-size: a numeral's tally strokes, the doubling mark laid shallow under a letter",
       "the whole cut", "the lower end", "the upper end"),
    _t("bar", "Bar", "mark", s_bar,
       {"w": (FULL, FULL, 0.8 * B), "at": (0.0, MID, ASC), "tilt": (-20.0, 0.0, 20.0)},
       "a level stroke drawn forward: the sentence end, the dash, the length bar over a vowel",
       "the whole stroke", "the tool's end", "the tool's end"),
])


def shape(sid: str, f: float, y: float, **params) -> Shape:
    """One stroke with its origin at (f, y). A parameter outside its range is refused."""
    st = STROKES[sid]
    for k, v in params.items():
        if k not in st.params:
            raise ValueError(f"{sid}: no parameter {k!r}; it takes {', '.join(st.params)}")
        lo, _, hi = st.params[k]
        if not lo <= v <= hi:
            raise ValueError(f"{sid}: {k}={v} is outside {lo:g}..{hi:g}")
        if (lo, hi) == (-1, 1) and v not in (-1, 1):
            raise ValueError(f"{sid}: {k}={v} must be -1 or 1")
        if (lo, hi) == (0, 1) and isinstance(lo, int) and v not in (0, 1):
            raise ValueError(f"{sid}: {k}={v} must be 0 or 1")
    return st.build(f, y, **params)


def stroke(sid: str, f: float, y: float, **params) -> pathops.Path:
    """The outline of one stroke."""
    return outline(shape(sid, f, y, **params).tracks)
