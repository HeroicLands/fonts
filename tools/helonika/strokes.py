# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""The Helónika book hand's stroke inventory, as parametric reed strokes that emit outlines.

    import strokes as S

    stem = S.shape("stem", 0, 0, top=S.X)       # a Shape: tracks, entry and exit
    bowl = S.shape("round", 0, 0)                # a full round on the line
    path = S.outline(stem.tracks + bowl.tracks)  # a pathops.Path, font units, y up

The Helónika runs left to right and stands upright. Coordinates are font units on a
1000-unit em, the line at y = 0, and the generator draws at the face's own size: the
minuscule body is the shared x-height, so no scale is applied afterwards.

**The reed.** A broad reed cut square, its edge held nearly flat, at ``Reed.angle``
to the line. A stroke's weight follows its direction and nothing else: an upright
runs across the edge and is the fullest the reed makes, a level stroke runs along
it and is a hairline, and a diagonal falls between. There is no pressure. At every
sample the reed leaves a flat footprint with slightly softened corners, and the
outline is the union of the convex hulls of neighbouring footprints.

**Ink edges.** A stroke's parameters name where its ink ends, not where its
centreline runs: a stem with ``top=X`` has its ink at the x-height. ``HALF_H`` and
``HALF_W`` are the reed's half extents, up and across, that the skeletons inset by.

**The knob.** A sample may shorten the edge that touches the page, as the copyist
does by letting only the reed's corner bear. Only the ``knob``, a hairline's
finishing wedge, does so; every other stroke is written with the whole edge.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Callable

import pathops


# -- metrics -----------------------------------------------------------------------------------

X = 513.0  # the minuscule body: the shared x-height
CAP = 730.0  # the majuscule and numeral height
ASC = 600.0  # the head of an ascending minuscule
DESC = -190.0  # the foot of a descending minuscule
OVER = 10.0  # how far a round passes the line and the body, so it looks as tall as a stem
DOT_Y = X  # the top of the raised dot
ACCENT_Y = X + 70.0  # the foot of the accent over a minuscule
BEARING = 30.0  # the white either side of a letter's ink
SPACE = 200.0  # the word space
STEP = 4.0  # the sampling interval along a track, in units


# -- the reed ----------------------------------------------------------------------------------


@dataclass(frozen=True)
class Reed:
    width: float  # the edge: the thickest stroke the reed makes
    thin: float  # the reed's thickness: the thinnest
    angle: float  # the edge's direction to the line, degrees, counter-clockwise from the right
    soften: float = 0.25  # how far the footprint's corners are rounded: 0 is square, 1 an ellipse
    facets: int = 24


# The book hand: one reed for both cases.
REED = Reed(width=80.0, thin=12.0, angle=10.0)
# The minuscules' reed: the same cut and angle with an edge a sixth narrower, so the
# running hand is lighter than the inscriptional capitals.
REED_MIN = Reed(width=67.0, thin=11.0, angle=10.0)


def _half(reed: Reed = REED):
    t = math.radians(reed.angle)
    across = reed.width / 2 * math.cos(t) + reed.thin / 2 * math.sin(t)
    up = reed.width / 2 * math.sin(t) + reed.thin / 2 * math.cos(t)
    return across, up


HALF_W, HALF_H = _half()  # about 40 across and 13 up


def weight(deg: float, reed: Reed = REED) -> float:
    """The thickness of a straight stroke travelling at ``deg``: the edge's projection
    across the stroke, plus the reed's thickness."""
    d = math.radians(deg - reed.angle)
    return abs(reed.width * math.sin(d)) + reed.thin * abs(math.cos(d))


# -- tracks ------------------------------------------------------------------------------------


@dataclass
class Track:
    """A reed path: samples of (x, y, angle, edge), where ``angle`` is None for the reed
    as held and ``edge`` scales the edge that touches the page."""

    x: float
    y: float
    angle: float | None = None
    edge: float = 1.0
    samples: list = field(default_factory=list)

    def __post_init__(self):
        self.samples = [(self.x, self.y, self.angle, self.edge)]

    @property
    def end(self):
        return self.samples[-1][:2]

    def line(self, x, y):
        x0, y0, a, k = self.samples[-1]
        n = max(2, math.ceil(math.hypot(x - x0, y - y0) / STEP))
        for i in range(1, n + 1):
            u = i / n
            self.samples.append((x0 + (x - x0) * u, y0 + (y - y0) * u, a, k))
        return self

    def curve(self, c1, c2, x, y):
        """A cubic Bezier to (x, y)."""
        x0, y0, a, k = self.samples[-1]
        approx = math.dist((x0, y0), c1) + math.dist(c1, c2) + math.dist(c2, (x, y))
        n = max(3, math.ceil(approx / STEP))
        for i in range(1, n + 1):
            u = i / n
            p, q, r, s = (1 - u) ** 3, 3 * u * (1 - u) ** 2, 3 * u * u * (1 - u), u**3
            self.samples.append((p * x0 + q * c1[0] + r * c2[0] + s * x, p * y0 + q * c1[1] + r * c2[1] + s * y, a, k))
        return self

    def ellipse(self, cx, cy, rx, ry, a0, a1):
        """Round an ellipse about (cx, cy) from angle ``a0`` to ``a1``, degrees; the
        track must already stand at ``a0``."""
        _, _, a, k = self.samples[-1]
        sweep = math.radians(a1 - a0)
        n = max(8, math.ceil(abs(sweep) * max(rx, ry) / STEP))
        for i in range(1, n + 1):
            t = math.radians(a0) + sweep * i / n
            self.samples.append((cx + rx * math.cos(t), cy + ry * math.sin(t), a, k))
        return self


def on_ellipse(cx, cy, rx, ry, deg):
    t = math.radians(deg)
    return cx + rx * math.cos(t), cy + ry * math.sin(t)


@dataclass
class Shape:
    """A stroke's tracks, with the points the pen enters and leaves by."""

    tracks: list
    entry: tuple  # (x, y)
    exit: tuple  # (x, y)

    def moved(self, dx, dy):
        tracks = []
        for t in self.tracks:
            n = Track(0, 0)
            n.samples = [(x + dx, y + dy, a, k) for x, y, a, k in t.samples]
            tracks.append(n)
        return Shape(tracks, (self.entry[0] + dx, self.entry[1] + dy), (self.exit[0] + dx, self.exit[1] + dy))


def join(*shapes: Shape) -> Shape:
    """Several strokes as one shape: the first one's entry, the last one's exit."""
    return Shape([t for s in shapes for t in s.tracks], shapes[0].entry, shapes[-1].exit)


# -- outlines ----------------------------------------------------------------------------------


def _footprint(x, y, angle, edge, reed: Reed):
    a = reed.width * edge / 2
    b = reed.thin / 2
    t = math.radians(reed.angle if angle is None else angle)
    ct, st = math.cos(t), math.sin(t)
    e = max(0.05, 1 - reed.soften) * 0.5  # the superellipse exponent: small is square
    pts = []
    for i in range(reed.facets):
        s = 2 * math.pi * i / reed.facets
        c, si = math.cos(s), math.sin(s)
        ex = a * math.copysign(abs(c) ** e, c)
        ey = b * math.copysign(abs(si) ** e, si)
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


def _polys(polys):
    path = pathops.Path()
    for poly in polys:
        path.moveTo(*poly[0])
        for q in poly[1:]:
            path.lineTo(*q)
        path.close()
    return path


def outline(tracks, reed: Reed = REED) -> pathops.Path:
    """The union of the footprints the reed leaves along the tracks."""
    hulls = []
    for track in tracks:
        prints, last = [], None
        for x, y, a, k in track.samples:
            if last is not None and math.hypot(x - last[0], y - last[1]) < 0.5 and len(track.samples) > 2:
                continue
            last = (x, y)
            prints.append([(round(p, 2), round(q, 2)) for p, q in _footprint(x, y, a, k, reed)])
        if len(prints) == 1:
            prints.append(prints[0])
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
            part = _polys(hulls[i:i + 40])
            part.simplify(fix_winding=True)
            out = pathops.op(out, part, pathops.PathOp.UNION)
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
# Each builder takes the stroke's origin (x, y) and its own parameters, and returns a
# Shape. Unless a docstring says otherwise, the origin is the left foot of the stroke's
# ink on the line, and the stroke is written left to right and top to bottom, as the
# copyist writes it.


def s_stem(x, y, top=X, foot=0.0):
    """An upright: the reed set down square at the head and pulled straight down to a
    square foot. The fullest stroke the reed makes. ``x`` is the stem's centre."""
    t = Track(x, y + top - HALF_H).line(x, y + foot + HALF_H)
    return Shape([t], (x, y + top), (x, y + foot))


TAILS = ("cut", "back", "forward")  # how a descender ends, by ``tail`` index


def s_descender(x, y, top=X, foot=DESC, tail=0, reach=1.0):
    """An upright carried below the line. It ends square (``cut``), turns back under
    itself into a hairline that finishes in a knob (``back``), or turns forward
    (``forward``). ``reach`` lengthens the turn. ``x`` is the stem's centre."""
    kind = TAILS[int(round(tail))]
    t = Track(x, y + top - HALF_H)
    if kind == "cut":
        t.line(x, y + foot + HALF_H)
        return Shape([t], (x, y + top), (x, y + foot))
    r = 70 * reach
    s = 1 if kind == "forward" else -1
    t.line(x, y + foot + HALF_H + r)
    t.curve((x, y + foot + HALF_H + 0.3 * r), (x + s * 0.3 * r, y + foot + HALF_H), x + s * r, y + foot + HALF_H)
    t.line(x + s * (r + 30 * reach), y + foot + HALF_H)
    end = t.end
    k = s_knob(end[0] + s * (HALF_W - KNOB_IN), end[1], drop=1, side=s)
    return Shape([t] + k.tracks, (x, y + top), end)


def s_round(x, y, w=X, h=X, over=OVER):
    """A full round, written as the copyist writes an omicron: two strokes from the
    head, the left side down and round to the foot, then the right side down to meet
    it. Thickest at the sides, hairline at the head and foot, its stress turned a
    little by the reed's 10°. ``w`` and ``h`` are the ink's width and height."""
    rx = w / 2 - HALF_W
    ry = h / 2 - HALF_H + over
    cx, cy = x + w / 2, y + h / 2
    left = Track(*on_ellipse(cx, cy, rx, ry, 100)).ellipse(cx, cy, rx, ry, 100, 275)
    right = Track(*on_ellipse(cx, cy, rx, ry, 95)).ellipse(cx, cy, rx, ry, 95, -95)
    return Shape([left, right], left.samples[0][:2], right.end)


def s_arc(x, y, w=X, h=X, start=45.0, sweep=270.0, over=OVER):
    """Part of the round: the same ellipse as ``round``, from ``start`` through
    ``sweep`` degrees, counter-clockwise from the right. A positive sweep runs
    counter-clockwise. The general bowl: a crescent, a hood or a cup. Its ends are
    the reed's own cuts."""
    rx = w / 2 - HALF_W
    ry = h / 2 - HALF_H + over
    cx, cy = x + w / 2, y + h / 2
    t = Track(*on_ellipse(cx, cy, rx, ry, start)).ellipse(cx, cy, rx, ry, start, start + sweep)
    return Shape([t], t.samples[0][:2], t.end)


def s_crescent(x, y, w=0.8 * X, h=X, open=110.0, over=OVER):
    """A round left open on the right by ``open`` degrees, written from the upper end
    round to the lower. Each end finishes in a knob, so the open side reads."""
    a0 = open / 2
    sh = s_arc(x, y, w, h, a0, 360 - open, over)
    t = sh.tracks[0]
    head = s_knob(*t.samples[0][:2], drop=1)
    foot = s_knob(*t.end, drop=-1)
    return Shape(sh.tracks + head.tracks + foot.tracks, sh.entry, sh.exit)


def s_hood(x, y, w=X, h=X, open=80.0, over=OVER):
    """A round left open at the foot by ``open`` degrees: the majuscule omega's body.
    Written as two strokes from the head, down each side to the open ends."""
    rx = w / 2 - HALF_W
    ry = h / 2 - HALF_H + over
    cx, cy = x + w / 2, y + h / 2
    a = 270 - open / 2
    b = -90 + open / 2
    left = Track(*on_ellipse(cx, cy, rx, ry, 100)).ellipse(cx, cy, rx, ry, 100, a)
    right = Track(*on_ellipse(cx, cy, rx, ry, 95)).ellipse(cx, cy, rx, ry, 95, b)
    return Shape([left, right], left.samples[0][:2], right.end)


def s_cup(x, y, w=0.5 * X, h=0.6 * X, left=1.0, right=1.0, over=OVER):
    """The lower half of a round with its sides carried up straight: from its left head,
    down, round the foot and up the right side. ``left`` and ``right`` set each side's
    height as a share of ``h``. The minuscule omega is two of them sharing a side."""
    rx = w / 2 - HALF_W
    cx = x + w / 2
    ry = min(rx, min(left, right) * h - HALF_H)  # the foot is a half-round
    cy = y + ry + HALF_H - over
    t = Track(cx - rx, y + left * h - HALF_H).line(cx - rx, cy)
    t.ellipse(cx, cy, rx, ry, 180, 360)
    t.line(cx + rx, y + right * h - HALF_H)
    return Shape([t], (cx - rx, y + left * h), (cx + rx, y + right * h))


def s_arch(x, y, w=0.62 * X, h=X, spring=0.62, foot=0.0):
    """The shoulder: from inside a stem at ``spring`` of the body, up and over in a
    half-round and down a straight right leg to ``foot``. ``x`` is the centre of the
    stem it springs from; ``w`` the ink width from that stem's left edge."""
    r = (w - 2 * HALF_W) / 2
    right = x + 2 * r
    cy = y + h - HALF_H - r
    t = Track(x, y + spring * h)
    t.curve((x, cy + 0.5 * r), (x + 0.2 * r, y + h - HALF_H), x + r, y + h - HALF_H)
    t.ellipse(x + r, cy, r, r, 90, 0)
    t.line(right, y + foot + HALF_H)
    return Shape([t], (x, y + spring * h), (right, y + foot))


def s_lobe(x, y, top=X, bottom=0.0, w=0.55 * X, side=1):
    """A bowl closed against a stem: from the stem at ``top``, out to the side
    ``side`` (1 forward, -1 back), round and back into the stem at ``bottom``.
    ``x`` is the stem's centre and ``w`` the ink's reach from it."""
    r = w - HALF_W
    a, b = y + top - HALF_H, y + bottom + HALF_H
    mid = (a + b) / 2
    t = Track(x, a)
    k = 0.552  # a quarter-circle's handle
    t.curve((x + side * k * r, a), (x + side * r, mid + k * (a - mid)), x + side * r, mid)
    t.curve((x + side * r, mid - k * (mid - b)), (x + side * k * r, b), x, b)
    return Shape([t], (x, y + top), (x, y + bottom))


def s_diagonal(x, y, w=0.6 * CAP, h=CAP, rise=1):
    """A straight diagonal across a box ``w`` by ``h``: rising forward from the left
    foot (``rise`` 1) or falling forward from the left head (``rise`` -1). A rising
    diagonal is lighter than a falling one, both lighter than a stem. Its ends are the
    reed's own cuts, so they lie at 10°, not level."""
    x0, x1 = x + HALF_W * 0.6, x + w - HALF_W * 0.6
    lo, hi = y + HALF_H, y + h - HALF_H
    if rise > 0:
        t = Track(x0, lo).line(x1, hi)
    else:
        t = Track(x0, hi).line(x1, lo)
    return Shape([t], t.samples[0][:2], t.end)


def s_bar(x, y, w=0.6 * CAP, at=0.5 * CAP, knobs=0, tilt=0.0):
    """A crossbar: the reed drawn along its edge, a hairline, its ink from ``x`` to
    ``x + w`` at height ``at``. A ``tilt`` of a few degrees lifts its right end.
    ``knobs`` 0 is bare ends, 1 a knob at the right end, 2 a knob at each end,
    hanging below the bar. The reed's edge runs along the bar, so its ink passes
    the track's ends by half the edge: the track is inset by ``HALF_W``."""
    dy = w * math.tan(math.radians(tilt))
    t = Track(x + HALF_W, y + at).line(x + w - HALF_W, y + at + dy)
    extra = []
    n = int(round(knobs))
    if n >= 2:
        extra += s_knob(x + KNOB_IN, y + at, side=-1).tracks
    if n >= 1:
        extra += s_knob(x + w - KNOB_IN, y + at + dy, side=1).tracks
    return Shape([t] + extra, t.samples[0][:2], t.end)


def s_beam(x, y, w=0.7 * CAP, at=CAP, overhang=40.0):
    """The gate's beam: a hairline laid along the head of two stems and run past them
    by ``overhang`` each side, both ends finished in a knob dropping below it. ``at``
    is the height of its ink's top; ``x`` is the beam's left ink."""
    return s_bar(x - overhang, y, w + 2 * overhang, at - HALF_H, knobs=2)


def s_neck(x, y, h=ASC, base=0.86 * X, lean=0.35, curl=0.6):
    """A stroke rising out of a bowl's head and curling over: from ``base`` above the
    line it climbs back and up to ``h`` and turns forward over its own head, the
    hairline turn finishing in a knob. ``lean`` sets how far back it climbs, ``curl``
    how far the head turns forward. ``x`` is where it leaves the bowl."""
    top = y + h - HALF_H
    y = y + base
    rise = top - y
    back = -lean * 160
    t = Track(x, y)
    t.curve((x + back * 0.5, y + 0.45 * rise), (x + back, top - 10), x + back * 0.4 + 30, top)
    t.curve((x + back * 0.1 + 70 * curl, top + 2), (x + 120 * curl, top - 4), x + 170 * curl, top - 22 * curl)
    k = s_knob(*t.end, drop=-1, size=0.9)
    return Shape([t] + k.tracks, (x, y), t.end)


def s_foot(x, y, reach=60.0, lift=40.0):
    """An exit: the reed coming off a stem's foot by turning forward along the line and
    up, a hairline that finishes the letter. ``x`` is the centre of the stem whose foot
    it leaves."""
    t = Track(x, y + 3 * HALF_H + 20)
    t.curve((x, y + HALF_H), (x + 0.4 * reach, y + HALF_H), x + reach, y + HALF_H + 4)
    t.curve((x + reach + 15, y + HALF_H + 6), (x + reach + 25, y + 0.5 * lift), x + reach + 30, y + lift)
    return Shape([t], (x, y + 3 * HALF_H + 20), t.end)


def s_lead(x, y, length=50.0, rise=-14.0):
    """An entry: before an upright the reed is laid on the left of its head and drawn
    along its edge into it, a short hairline flag. ``x, y`` is the head of the
    upright's ink, its centre; ``rise`` is how far the flag's start sits above (+) or
    below (-) it."""
    t = Track(x - HALF_W - length, y - HALF_H + rise).line(x, y - HALF_H)
    return Shape([t], t.samples[0][:2], t.end)


KNOB_IN = 14.0  # how far inside a hairline's ink end its knob is set


def s_knob(x, y, size=1.0, drop=-1, side=1):
    """The hairline's finish: at a hairline's free end the copyist lets the reed's
    corner bear on the page and draws it a short way off the line, lifting it as it
    goes, so the end swells into a small wedge rather than a hook. The wedge hangs
    below the hairline (``drop`` -1) or stands above it (1), and leans outward toward
    the end it finishes (``side`` 1 for a right end, -1 for a left). (x, y) is the
    hairline's centre where the knob springs from it. The one stroke in which the
    edge that touches the page shortens."""
    depth = 34.0 * size
    n = 10
    t = Track(x, y, None, 0.5 * size)
    t.samples = []
    for i in range(n + 1):
        u = i / n
        t.samples.append((x + side * 6 * size * u, y + drop * depth * u, None, (0.5 - 0.38 * u) * size))
    return Shape([t], (x, y), t.samples[-1][:2])


def s_dot(x, y, size=1.0, at=DOT_Y):
    """The raised dot: the reed set down and drawn straight down its own width, a
    square-shouldered point whose top stands at ``at``. ``x`` is its centre."""
    d = (REED.width * 0.95 - 2 * HALF_H) * size
    top = y + at - HALF_H
    t = Track(x, top).line(x, top - max(2.0, d))
    return Shape([t], (x, y + at), t.end)


def s_accent(x, y, length=110.0, angle=58.0, at=ACCENT_Y):
    """The accent: one stroke rising forward from its foot at ``at``, lighter than a
    stem by its slope. ``x`` is the centre of its foot."""
    dx = length * math.cos(math.radians(angle))
    dy = length * math.sin(math.radians(angle))
    t = Track(x, y + at + HALF_H).line(x + dx, y + at + HALF_H + dy)
    return Shape([t], t.samples[0][:2], t.end)


def s_length(x, y, w=150.0, at=X + 70.0):
    """The length bar over a vowel: a level hairline with a knob hanging from each end,
    so it holds at text size. ``x`` is its centre."""
    return s_bar(x - w / 2, y, w, at + HALF_H, knobs=2)


# -- the minuscule's curves --------------------------------------------------------------------
#
# The minuscule is the pen's own hand: its stems, diagonals and bars are drawn as
# curves, and a free end turns into a flourish rather than a knob.

CURL = 50.0  # the radius a flourish turns on


def heading(track: Track, at_end: bool = True) -> float:
    """The direction of travel at a track's end, or the direction pointing back out
    of its start, in degrees."""
    pts = track.samples
    if at_end:
        (x0, y0), (x1, y1) = pts[max(0, len(pts) - 4)][:2], pts[-1][:2]
    else:
        (x0, y0), (x1, y1) = pts[min(len(pts) - 1, 3)][:2], pts[0][:2]
    return math.degrees(math.atan2(y1 - y0, x1 - x0))


def curl(x, y, toward, turn, r=CURL):
    """A track that leaves (x, y) travelling ``toward`` degrees and turns through
    ``turn`` degrees on a circle of radius ``r``: positive turns left
    (counter-clockwise), negative right."""
    h = math.radians(toward)
    side = 1 if turn > 0 else -1
    cx, cy = x + r * math.cos(h + side * math.pi / 2), y + r * math.sin(h + side * math.pi / 2)
    a0 = math.degrees(math.atan2(y - cy, x - cx))
    return Track(x, y).ellipse(cx, cy, r, r, a0, a0 + turn)


def s_flourish(x, y, toward=-90.0, turn=120.0, r=CURL):
    """A flourish: a free end carried on past (x, y) in the direction ``toward`` and
    turned through ``turn`` degrees, so the stroke ends in a hook drawn by the reed.
    It thins where it runs level and swells where it runs upright."""
    t = curl(x, y, toward, turn, r)
    return Shape([t], (x, y), t.end)


def s_swing(x, y, dx=0.0, dy=-X, bow=0.06, head=0.0, tail=0.0, r=CURL):
    """A curved stroke from (x, y) to (x + dx, y + dy), bowed by ``bow`` of its length
    to the left of the way it travels (a stroke drawn downward bows forward). A
    ``head`` or ``tail`` other than 0 finishes that end in a flourish turning through
    so many degrees, positive to the left of the way the pen leaves the end. The
    minuscule's stem, diagonal and bar."""
    x1, y1 = x + dx, y + dy
    length = math.hypot(dx, dy)
    nx, ny = -dy / length, dx / length
    k = bow * length / 0.75
    c1 = (x + dx / 3 + nx * k, y + dy / 3 + ny * k)
    c2 = (x + 2 * dx / 3 + nx * k, y + 2 * dy / 3 + ny * k)
    t = Track(x, y).curve(c1, c2, x1, y1)
    tracks = [t]
    if abs(head) > 1:
        tracks.append(curl(x, y, heading(t, at_end=False), head, r))
    if abs(tail) > 1:
        tracks.append(curl(x1, y1, heading(t), tail, r))
    return Shape(tracks, (x, y), (x1, y1))


def s_hooked(x, y, top=X, foot=0.0, bow=0.10, entry=60.0, tail=1, r=60.0):
    """The minuscule's stem: set going by a small entry hairline that rises from the
    left into its head, a curve bowed by ``bow`` of its height, and a foot that turns
    into a tail, forward (``tail`` 1), back (-1), or not at all (0). ``x`` is the
    stem's centre; ``entry`` 0 leaves the head as the reed's cut."""
    t0, f0 = y + top - HALF_H, y + foot + HALF_H
    tracks = []
    if entry > 1:
        e = Track(x - entry, t0 - 0.45 * entry)
        e.curve((x - 0.6 * entry, t0 - 0.05 * entry), (x - 0.2 * entry, t0 + 2), x, t0)
        tracks.append(e)
    n = int(round(tail))
    body = s_swing(x, t0, 0.0, f0 - t0, bow, 0.0, 115.0 * n if n else 0.0, r)
    return Shape(tracks + body.tracks, (x - entry, t0 - 0.45 * entry) if entry > 1 else (x, t0), body.exit)


# -- the inventory -----------------------------------------------------------------------------


@dataclass(frozen=True)
class StrokeType:
    id: str
    name: str
    kind: str  # stem, bowl, diagonal, bar, descender, terminal, point, mark
    build: Callable
    params: dict  # name -> (minimum, default, maximum)
    skeleton: str
    weight: str  # where the stroke is fullest
    entry: str
    exit: str


def _t(*args):
    s = StrokeType(*args)
    return s.id, s


STROKES: dict[str, StrokeType] = dict([
    _t("stem", "Stem", "stem", s_stem, {"top": (120.0, X, CAP), "foot": (0.0, 0.0, 300.0)},
       "an upright, set down square and pulled straight down to a square foot",
       "all of it: the fullest stroke", "the reed's square cut", "the reed's square cut"),
    _t("descender", "Descender", "descender", s_descender,
       {"top": (200.0, X, ASC), "foot": (DESC, DESC, -80.0), "tail": (0, 0, 2), "reach": (0.5, 1.0, 1.6)},
       "an upright carried below the line, ending square, turned back under itself, or turned forward",
       "the upright", "the reed's square cut", "the square foot, or the knob on the turn"),
    _t("round", "Round", "bowl", s_round, {"w": (0.5 * X, X, CAP), "h": (0.5 * X, X, CAP), "over": (0.0, OVER, 20.0)},
       "a full round in two strokes from the head: the left side down to the foot, then the right side",
       "the sides", "the head", "the foot"),
    _t("arc", "Arc", "bowl", s_arc,
       {"w": (0.4 * X, X, CAP), "h": (0.4 * X, X, CAP), "start": (-180.0, 45.0, 360.0),
        "sweep": (-360.0, 270.0, 360.0), "over": (0.0, OVER, 20.0)},
       "part of the round, from a start angle through a sweep: the general bowl", "where it runs upright",
       "the reed's cut", "the reed's cut"),
    _t("crescent", "Crescent", "bowl", s_crescent,
       {"w": (0.5 * X, 0.8 * X, CAP), "h": (0.5 * X, X, CAP), "open": (60.0, 110.0, 160.0), "over": (0.0, OVER, 20.0)},
       "a round left open on the right, written from the upper end round to the lower, a knob at each end",
       "the back", "the upper knob", "the lower knob"),
    _t("hood", "Hood", "bowl", s_hood,
       {"w": (0.5 * X, X, CAP), "h": (0.5 * X, X, CAP), "open": (40.0, 80.0, 140.0), "over": (0.0, OVER, 20.0)},
       "a round left open at the foot, in two strokes from the head down each side", "the sides", "the head",
       "the open ends"),
    _t("cup", "Cup", "bowl", s_cup,
       {"w": (0.35 * X, 0.5 * X, X), "h": (0.3 * X, 0.6 * X, X), "left": (0.4, 1.0, 1.0), "right": (0.4, 1.0, 1.0),
        "over": (0.0, OVER, 20.0)},
       "a half-round foot with its sides carried straight up: down, round the foot and up",
       "the sides", "the left head", "the right head"),
    _t("arch", "Arch", "bowl", s_arch,
       {"w": (0.45 * X, 0.62 * X, 0.9 * X), "h": (0.5 * X, X, CAP), "spring": (0.4, 0.62, 0.85),
        "foot": (DESC, 0.0, 0.0)},
       "a shoulder springing from inside a stem, over in a half-round and down a straight right leg",
       "the right leg", "inside the stem", "the leg's square foot"),
    _t("lobe", "Lobe", "bowl", s_lobe,
       {"top": (0.4 * X, X, CAP), "bottom": (DESC, 0.0, 0.6 * X), "w": (0.3 * X, 0.55 * X, 0.8 * X),
        "side": (-1, 1, 1)},
       "a bowl closed against a stem: out from it at the head, round, and back into it at the foot",
       "the far side", "the stem's head", "the stem's foot"),
    _t("diagonal", "Diagonal", "diagonal", s_diagonal,
       {"w": (0.2 * CAP, 0.6 * CAP, 0.9 * CAP), "h": (0.5 * X, CAP, ASC - DESC), "rise": (-1, 1, 1)},
       "a straight diagonal across its box, rising or falling forward",
       "the falling one; the rising one is lighter", "the reed's cut, at 10°", "the reed's cut, at 10°"),
    _t("bar", "Crossbar", "bar", s_bar,
       {"w": (100.0, 0.6 * CAP, CAP), "at": (0.0, 0.5 * CAP, CAP), "knobs": (0, 0, 2), "tilt": (-8.0, 0.0, 8.0)},
       "a level hairline, the reed drawn along its edge, bare or knobbed at the ends",
       "nowhere: the hairline", "the reed's cut", "the cut, or a knob"),
    _t("beam", "Beam", "bar", s_beam,
       {"w": (0.3 * CAP, 0.7 * CAP, CAP), "at": (X, CAP, CAP), "overhang": (0.0, 40.0, 80.0)},
       "the gate's head: a hairline along the head of two stems, run past them, a knob dropping from each end",
       "the knobs", "the left knob", "the right knob"),
    _t("neck", "Neck", "ascender", s_neck,
       {"h": (X + 60, ASC, CAP), "base": (0.5 * X, 0.86 * X, X), "lean": (0.0, 0.35, 1.0),
        "curl": (0.2, 0.6, 1.0)},
       "a stroke rising back out of a bowl's head and turning forward over itself into a hairline and a knob",
       "the climb", "the bowl's head", "the knob"),
    _t("foot", "Foot", "terminal", s_foot, {"reach": (30.0, 60.0, 110.0), "lift": (20.0, 40.0, 80.0)},
       "an exit: a stem's foot turned forward along the line and up into a hairline",
       "the turn", "the stem's foot", "the hairline's tip"),
    _t("lead", "Lead", "terminal", s_lead, {"length": (20.0, 50.0, 90.0), "rise": (-40.0, -14.0, 20.0)},
       "an entry: a short hairline flag drawn along the reed's edge into an upright's head",
       "nowhere: the hairline", "the flag's tip", "the upright's head"),
    _t("knob", "Knob", "terminal", s_knob, {"size": (0.6, 1.0, 1.4), "drop": (-1, -1, 1), "side": (-1, 1, 1)},
       "a hairline's finish: the reed's corner drawn a short way off the line and lifted, a small wedge, never a hook",
       "the knob", "the hairline's end", "the hairline's end"),
    _t("dot", "Raised dot", "point", s_dot, {"size": (0.6, 1.0, 1.2), "at": (0.6 * X, DOT_Y, X + 40)},
       "the reed set down and drawn down its own width: a square-shouldered point with its top at the body",
       "all of it", "set down", "lifted"),
    _t("accent", "Accent", "mark", s_accent,
       {"length": (70.0, 110.0, 150.0), "angle": (40.0, 58.0, 75.0), "at": (X, ACCENT_Y, CAP + 60)},
       "one stroke rising forward from its foot", "even: lighter than a stem by its slope", "the foot", "the head"),
    _t("swing", "Swing", "curve", s_swing,
       {"dx": (-700.0, 0.0, 700.0), "dy": (-900.0, -X, 900.0), "bow": (-0.25, 0.06, 0.25),
        "head": (-240.0, 0.0, 240.0), "tail": (-240.0, 0.0, 240.0), "r": (25.0, CURL, 90.0)},
       "a curved stroke between two points, bowed to one side, either end finished in a flourish",
       "where it runs upright", "the reed's cut, or a flourish", "the reed's cut, or a flourish"),
    _t("flourish", "Flourish", "terminal", s_flourish,
       {"toward": (-180.0, -90.0, 360.0), "turn": (-240.0, 120.0, 240.0), "r": (25.0, CURL, 90.0)},
       "a free end carried on and turned into a hook by the reed, swelling where it runs upright",
       "the upright part of the turn", "the end it finishes", "the reed's cut"),
    _t("hooked", "Hooked stem", "curve", s_hooked,
       {"top": (0.4 * X, X, ASC), "foot": (DESC, 0.0, 0.5 * X), "bow": (-0.25, 0.10, 0.25), "entry": (0.0, 60.0, 120.0),
        "tail": (-1, 1, 1), "r": (30.0, 60.0, 90.0)},
       "the minuscule's stem: a small entry hairline rising into its head, a bowed fall, a foot turned into a tail",
       "the fall", "the entry's tip", "the tail's end"),
    _t("length", "Length bar", "mark", s_length, {"w": (100.0, 150.0, 260.0), "at": (X + 30, X + 70.0, CAP + 60)},
       "a level hairline over a vowel with a knob hanging from each end", "the knobs", "the left knob",
       "the right knob"),
])


def shape(sid: str, x: float, y: float, **params) -> Shape:
    """One stroke with its origin at (x, y)."""
    st = STROKES[sid]
    for k, v in params.items():
        if k not in st.params:
            raise ValueError(f"{sid}: no parameter {k!r}; it takes {', '.join(st.params)}")
        lo, _, hi = st.params[k]
        if not lo <= v <= hi:
            raise ValueError(f"{sid}: {k}={v} is outside {lo}..{hi}")
        if (lo, hi) == (-1, 1) and isinstance(lo, int) and v not in (-1, 1) and k != "tail":
            raise ValueError(f"{sid}: {k}={v} must be -1 or 1")
    return st.build(x, y, **params)


def stroke(sid: str, x: float, y: float, **params) -> pathops.Path:
    """The outline of one stroke."""
    return outline(shape(sid, x, y, **params).tracks)
