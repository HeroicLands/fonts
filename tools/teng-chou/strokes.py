# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""The Teng Chou stroke inventory, as parametric brush strokes that emit outlines.

    from strokes import STROKES, Style, stroke, union

    path = stroke("turn-spur", 200, 800, l1=500, l2=560)   # a pathops.Path, font units
    glyph = union([stroke(...), stroke(...)])               # one clean outline

Coordinates are font units on a 1000-unit em, y up. Every stroke is given by its
start point and its own parameters; ``STROKES[id].params`` gives each parameter's
permitted range and default, and ``stroke`` refuses a value outside it.

**How a stroke is drawn.** A stroke is one or more *tracks*: a path the brush tip
follows, sampled every ``STEP`` units, with a *pressure* at every sample.
At each sample the brush leaves an elliptical footprint, its size set by the
pressure and its axis held at ``Style.nib_angle``, as a brush held at a fixed
slant is. The outline is the union of the convex hulls of each pair of
neighbouring footprints. The held slant is what makes a horizontal thinner than
a vertical; the pressure is what makes an entry press, a waist, a pause, a
shoulder and a taper. Nothing is offset from a centreline by a fixed width, so no
stroke is uniform.

The style is separate from the skeletons: a heavier or a seal-like face is a
different ``Style`` over the same stroke calls.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Callable

import pathops


# -- style -------------------------------------------------------------------------------------


@dataclass(frozen=True)
class Style:
    weight: float = 92.0  # footprint's long axis at pressure 1, in units: a loaded brush
    aspect: float = 0.40  # footprint's short axis over its long axis
    nib_angle: float = -30.0  # direction of the long axis, degrees, y up
    floor: float = 0.035  # the least pressure: a taper ends this fine, never at zero
    facets: int = 20  # points round one footprint


REGULAR = Style()
STEP = 5.0  # sampling interval along a track, in units


# -- tracks ------------------------------------------------------------------------------------


Ease = Callable[[float], float]


def linear(u: float) -> float:
    return u


def ease_in(k: float = 2.0) -> Ease:
    return lambda u: u**k


def ease_out(k: float = 2.0) -> Ease:
    return lambda u: 1 - (1 - u) ** k


def smooth(u: float) -> float:
    return u * u * (3 - 2 * u)


@dataclass
class Track:
    """A brush path: samples of (x, y, pressure)."""

    x: float
    y: float
    p: float
    samples: list = field(default_factory=list)

    def __post_init__(self):
        self.samples = [(self.x, self.y, self.p)]

    @property
    def end(self):
        return self.samples[-1]

    def line(self, x, y, p, ease: Ease = linear, wave: Callable[[float], float] | None = None):
        """Run straight to (x, y), pressure easing to ``p``; ``wave(u)`` adds a pressure term."""
        x0, y0, p0 = self.end
        n = max(2, math.ceil(math.hypot(x - x0, y - y0) / STEP))
        for i in range(1, n + 1):
            u = i / n
            q = p0 + (p - p0) * ease(u) + (wave(u) if wave else 0.0)
            self.samples.append((x0 + (x - x0) * u, y0 + (y - y0) * u, q))
        return self

    def curve(self, c1, c2, x, y, p, ease: Ease = linear, wave=None):
        """A cubic Bezier to (x, y) through control points c1 and c2."""
        x0, y0, p0 = self.end
        approx = math.dist((x0, y0), c1) + math.dist(c1, c2) + math.dist(c2, (x, y))
        n = max(3, math.ceil(approx / STEP))
        for i in range(1, n + 1):
            u = i / n
            a, b, c, d = (1 - u) ** 3, 3 * u * (1 - u) ** 2, 3 * u * u * (1 - u), u**3
            px = a * x0 + b * c1[0] + c * c2[0] + d * x
            py = a * y0 + b * c1[1] + c * c2[1] + d * y
            q = p0 + (p - p0) * ease(u) + (wave(u) if wave else 0.0)
            self.samples.append((px, py, q))
        return self

    def spiral(self, cx, cy, sweep_deg, shrink, p, ease: Ease = linear):
        """Turn about (cx, cy) by ``sweep_deg`` (negative is clockwise), the radius
        shrinking by the fraction ``shrink`` over the turn."""
        x0, y0, p0 = self.end
        r0 = math.hypot(x0 - cx, y0 - cy)
        t0 = math.atan2(y0 - cy, x0 - cx)
        sweep = math.radians(sweep_deg)
        n = max(6, math.ceil(abs(sweep) * r0 / STEP))
        for i in range(1, n + 1):
            u = i / n
            r = r0 * (1 - shrink * u)
            t = t0 + sweep * u
            q = p0 + (p - p0) * ease(u)
            self.samples.append((cx + r * math.cos(t), cy + r * math.sin(t), q))
        return self


# -- geometry ----------------------------------------------------------------------------------


def _footprint(x, y, p, style: Style):
    a = style.weight * max(p, style.floor) / 2
    b = a * style.aspect
    t = math.radians(style.nib_angle)
    ct, st = math.cos(t), math.sin(t)
    pts = []
    for i in range(style.facets):
        s = 2 * math.pi * i / style.facets
        ex, ey = a * math.cos(s), b * math.sin(s)
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
    return lower[:-1] + upper[:-1]  # counter-clockwise


def _add_polygon(path: pathops.Path, poly):
    path.moveTo(*poly[0])
    for q in poly[1:]:
        path.lineTo(*q)
    path.close()


def outline(tracks, style: Style = REGULAR) -> pathops.Path:
    """The union of the footprints the tracks leave."""
    path = pathops.Path()
    for track in tracks:
        prints = [_footprint(x, y, p, style) for x, y, p in track.samples]
        for a, b in zip(prints, prints[1:]):
            _add_polygon(path, _hull(a + b))
    path.simplify(fix_winding=True)
    return path


def union(paths) -> pathops.Path:
    out = pathops.Path()
    for p in paths:
        out.addPath(p)
    out.simplify(fix_winding=True)
    return out


def polar(x, y, length, deg):
    t = math.radians(deg)
    return x + length * math.cos(t), y + length * math.sin(t)


# -- the shared terminals ----------------------------------------------------------------------
#
# Every stroke opens and closes with one of these, so a terminal is drawn the same
# way wherever it appears.


def press_entry(x, y, p=1.12, depth=1.0) -> Track:
    """The angled press: the tip lands up and to the left and is pushed down-right
    into the stroke's start at (x, y), leaving a knob heavier than the body."""
    t = Track(x - 17 * depth, y + 15 * depth, 0.50)
    t.line(x + 3 * depth, y - 5 * depth, p + 0.22, ease_out(2))
    return t


def soft_entry(x, y, p=0.30) -> Track:
    """The tip lands lightly, with no press: the opening of a falling stroke or a dot."""
    return Track(x, y, p)


def pause_exit(t: Track, dx=7, dy=-9, p=1.08, back=0.82):
    """The pause: the brush presses down-right at the end, then lifts back inward."""
    x, y, _ = t.end
    t.line(x + dx, y + dy, p, ease_out(2))
    t.line(x + dx - 9, y + dy + 3, back)
    return t


def dew_exit(t: Track, p=1.0):
    """The blunt end of a vertical: a slight swell, then the tip drawn back up."""
    x, y, _ = t.end
    t.line(x + 2, y - 8, p, ease_out(2))
    t.line(x - 1, y - 2, 0.80)
    return t


def taper_exit(t: Track, x, y, k=1.5, c1=None, c2=None):
    """Lift the brush steadily to a point at (x, y)."""
    if c1 is None:
        t.line(x, y, REGULAR.floor, ease_out(k))
    else:
        t.curve(c1, c2, x, y, REGULAR.floor, ease_out(k))
    return t


def spur_exit(t: Track, heading_deg, length, p_heel=1.32):
    """The Teng Chou hook. The brush seats a heel at the stroke's end, then flicks out
    along ``heading_deg``, lifting to a point: a long low barb."""
    x, y, _ = t.end
    t.line(x + 4, y - 8, p_heel, ease_out(2))
    hx, hy, _ = t.end
    ex, ey = polar(hx, hy, length, heading_deg)
    t.line(ex, ey, REGULAR.floor, ease_in(1.7))
    return t


def shoulder(t: Track, x, y, lift=0.62, p=1.10):
    """A turn's shoulder: the brush eases off along the horizontal, rides up over the
    corner at (x, y), and presses down again to start the descent."""
    t.line(x - 4, y, lift, smooth)
    t.line(x + 8, y + 9, 0.78)
    t.line(x + 10, y - 12, p, ease_out(2))
    return t


# -- the strokes -------------------------------------------------------------------------------


def _horizontal_body(t: Track, x1, y1, bow, p_body=0.80):
    x0, y0, _ = t.end
    dx, dy = x1 - x0, y1 - y0
    length = math.hypot(dx, dy) or 1
    nx, ny = -dy / length, dx / length
    c1 = (x0 + dx / 3 + nx * bow * length, y0 + dy / 3 + ny * bow * length)
    c2 = (x0 + 2 * dx / 3 + nx * bow * length, y0 + 2 * dy / 3 + ny * bow * length)
    # the waist: thinnest a little before the middle, filling again toward the pause
    t.curve(c1, c2, x1, y1, p_body + 0.08, linear, wave=lambda u: -0.10 * math.sin(math.pi * u))
    return t


def s_dot(x, y, l=80, a=-55):
    t = soft_entry(x, y, 0.42)
    ex, ey = polar(x, y, l, a)
    mx, my = polar(x, y, l * 0.5, a + 5)
    t.curve((mx, my), polar(ex, ey, l * 0.25, a + 160), ex, ey, 1.55, ease_in(1.4))
    t.line(ex - 12, ey + 5, 1.15)
    return [t]


def s_dot_left(x, y, l=80, a=-125):
    t = soft_entry(x, y, 0.42)
    ex, ey = polar(x, y, l, a)
    t.curve(polar(x, y, l * 0.45, a - 5), polar(ex, ey, l * 0.2, a - 170), ex, ey, 1.45, ease_in(1.4))
    t.line(ex + 11, ey + 6, 1.10)
    return [t]


def s_horizontal(x, y, l=480, rise=4.0, bow=0.012):
    t = press_entry(x, y)
    ex, ey = polar(x, y, l, rise)
    _horizontal_body(t, ex, ey, bow)
    pause_exit(t)
    return [t]


def s_vertical(x, y, l=520, lean=0.0, bow=0.010):
    t = press_entry(x, y, 1.12)
    ex, ey = x + lean, y - l
    c1 = (x + lean / 3 - bow * l, y - l / 3)
    c2 = (x + 2 * lean / 3 - bow * l, y - 2 * l / 3)
    t.curve(c1, c2, ex, ey, 0.96, wave=lambda u: -0.07 * math.sin(math.pi * u))
    dew_exit(t)
    return [t]


def s_needle(x, y, l=560, lean=0.0):
    t = press_entry(x, y, 1.12)
    t.line(x + lean * 0.55, y - l * 0.55, 0.95)
    taper_exit(t, x + lean, y - l, k=1.15)
    return [t]


def s_sweep(x, y, l=420, a=-128, curl=0.35):
    t = press_entry(x, y, 1.10)
    ex, ey = polar(x, y, l, a)
    c1 = (x + 4, y - l * (0.30 + curl * 0.35))
    c2 = polar(ex, ey, l * 0.32, a + 180 - 28 * curl * 2)
    t.curve(c1, c2, ex, ey, REGULAR.floor, ease_out(0.9),
            wave=lambda u: 0.10 * math.sin(math.pi * min(u * 1.6, 1)))
    return [t]


def s_sweep_short(x, y, l=150, a=-158):
    t = press_entry(x, y, 1.05, 0.8)
    ex, ey = polar(x, y, l, a)
    taper_exit(t, ex, ey, 1.2, polar(x, y, l * 0.4, a + 22), polar(ex, ey, l * 0.3, a + 170))
    return [t]


def s_fall(x, y, l=460, a=-42, foot=0.30):
    t = soft_entry(x, y, 0.22)
    bx, by = polar(x, y, l, a)
    c1 = polar(x, y, l * 0.35, a + 9)
    c2 = polar(bx, by, l * 0.30, a + 180 + 6)
    t.curve(c1, c2, bx, by, 1.48, ease_in(1.4))
    fx, fy = polar(bx, by, l * foot, -8)
    t.line(fx, fy, REGULAR.floor, ease_out(1.1))
    return [t]


def s_fall_flat(x, y, l=560, a=-9, foot=0.28):
    t = press_entry(x, y, 0.85, 0.7)
    bx, by = polar(x, y, l * (1 - foot), a)
    c1 = polar(x, y, l * 0.25, a - 10)
    c2 = polar(bx, by, l * 0.25, a + 180 - 8)
    t.curve(c1, c2, bx, by, 1.42, ease_in(1.5))
    fx, fy = polar(bx, by, l * foot, a + 4)
    t.line(fx, fy, REGULAR.floor, ease_out(1.1))
    return [t]


def s_rise(x, y, l=200, a=32):
    t = press_entry(x, y, 1.25, 1.0)
    t.line(x - 2, y - 6, 1.22)
    ex, ey = polar(x, y - 4, l, a)
    taper_exit(t, ex, ey, 1.25)
    return [t]


def s_vertical_spur(x, y, l=560, spur=100, lean=0.0):
    t = press_entry(x, y, 1.12)
    t.curve((x - 6, y - l / 3), (x + lean - 6, y - 2 * l / 3), x + lean, y - l, 0.98,
            wave=lambda u: -0.07 * math.sin(math.pi * u))
    spur_exit(t, 160, spur)
    return [t]


def s_turn(x, y, l1=440, l2=480, rise=3.0, slope=-93.0):
    t = press_entry(x, y)
    cx, cy = polar(x, y, l1, rise)
    _horizontal_body(t, cx - 6, cy, 0.008, 0.78)
    shoulder(t, cx, cy)
    sx, sy, _ = t.end
    ex, ey = polar(sx, sy, l2, slope)
    t.line(ex, ey, 0.96, wave=lambda u: -0.05 * math.sin(math.pi * u))
    dew_exit(t)
    return [t]


def s_turn_spur(x, y, l1=440, l2=520, rise=3.0, spur=95, slope=-93.0):
    t = press_entry(x, y)
    cx, cy = polar(x, y, l1, rise)
    _horizontal_body(t, cx - 6, cy, 0.008, 0.78)
    shoulder(t, cx, cy)
    sx, sy, _ = t.end
    ex, ey = polar(sx, sy, l2, slope)
    t.line(ex, ey, 0.98, wave=lambda u: -0.05 * math.sin(math.pi * u))
    spur_exit(t, 160, spur)
    return [t]


def s_corner(x, y, l1=380, l2=420, rise=2.5):
    t = press_entry(x, y)
    t.line(x, y - l1, 0.98, wave=lambda u: -0.06 * math.sin(math.pi * u))
    t.line(x + 6, y - l1 - 6, 1.08, ease_out(2))
    _horizontal_body(t, *polar(x + 6, y - l1 - 6, l2, rise), 0.0, 0.82)
    pause_exit(t)
    return [t]


def s_bend_spur(x, y, l1=380, l2=440, r=90, spur=95):
    t = press_entry(x, y)
    t.line(x, y - l1 + r, 0.95)
    bx, by = x + r, y - l1
    t.curve((x, y - l1 + r * 0.35), (x + r * 0.35, by), bx, by, 0.84)
    t.line(bx + l2 - r, by + 8, 1.04, ease_in(1.5))
    spur_exit(t, 55, spur, p_heel=1.12)
    return [t]


def s_turn_sweep(x, y, l1=300, l2=380, rise=3.0, a=-122):
    t = press_entry(x, y)
    cx, cy = polar(x, y, l1, rise)
    _horizontal_body(t, cx - 6, cy, 0.006, 0.78)
    shoulder(t, cx, cy, p=1.05)
    sx, sy, _ = t.end
    ex, ey = polar(sx, sy, l2, a)
    taper_exit(t, ex, ey, 1.0, polar(sx, sy, l2 * 0.35, -98), polar(ex, ey, l2 * 0.35, a + 180 - 22))
    return [t]


def s_slant_spur(x, y, l=640, a=-62, bow=0.10, spur=90):
    t = press_entry(x, y, 1.05)
    ex, ey = polar(x, y, l, a)
    c1 = polar(*polar(x, y, l / 3, a), bow * l, a - 90)
    c2 = polar(*polar(x, y, 2 * l / 3, a), bow * l, a - 90)
    t.curve(c1, c2, ex, ey, 1.02, wave=lambda u: -0.10 * math.sin(math.pi * u))
    spur_exit(t, 62, spur)
    return [t]


def s_sweep_turn(x, y, l1=200, l2=260, a=-128, rise=18):
    t = press_entry(x, y, 1.08)
    cx, cy = polar(x, y, l1, a)
    t.curve(polar(x, y, l1 * 0.4, a + 15), polar(cx, cy, l1 * 0.3, a + 160), cx, cy, 0.78)
    t.line(cx + 4, cy - 4, 1.08, ease_out(2))
    ex, ey = polar(cx + 4, cy - 4, l2, rise)
    t.line(*polar(cx + 4, cy - 4, l2 * 0.5, rise), 0.82)
    taper_exit(t, ex, ey, 1.3)
    return [t]


# the novel strokes


def s_tally(x, y, l=150, sag=0.22):
    """Two beads on one stroke: a dot, a sagging hairline, and a heavier dot."""
    t = soft_entry(x, y, 0.30)
    bx, by = x + l * 0.18, y - l * 0.24
    t.curve((x + l * 0.05, y - l * 0.10), (bx - 6, by + 8), bx, by, 1.40, ease_in(1.3))
    t.line(bx + 4, by - 2, 0.70, ease_out(2))
    ex, ey = x + l * 0.72, y - l * 0.16
    t.curve((bx + l * 0.20, by - sag * l), (ex - l * 0.22, ey - sag * l * 0.8), ex, ey, 0.16,
            wave=lambda u: -0.50 * math.sin(math.pi * u) * (1 - u))
    t.curve((ex + l * 0.08, ey - l * 0.04), (ex + l * 0.18, ey - l * 0.16), x + l, ey - l * 0.26, 1.60,
            ease_in(1.3))
    t.line(x + l - 13, ey - l * 0.26 + 6, 1.20)
    return [t]


def s_rods(x, y, l=260, gap=58, rise=4.0):
    """A split brush: one press, and two short rods running right from it."""
    hx, hy = x, y - gap / 2
    head = press_entry(hx, hy, 1.30, 1.2)
    upper = Track(hx + 4, hy, 1.05)
    ux, uy = hx + l * 0.22, y
    upper.line(ux, uy, 0.62)
    _horizontal_body(upper, *polar(ux, uy, l * 0.56, rise + 1.5), 0.0, 0.58)
    pause_exit(upper, 5, -6, 0.86, 0.66)
    lower = Track(hx + 4, hy - 4, 1.05)
    lx, ly = hx + l * 0.20, y - gap
    lower.line(lx, ly, 0.66)
    _horizontal_body(lower, *polar(lx, ly, l * 0.80, rise), 0.0, 0.66)
    pause_exit(lower, 6, -8, 0.98, 0.72)
    return [head, upper, lower]


def s_barb_dot(x, y, l=90, a=-58, barb=48):
    """A dot whose heavy end flicks back up and to the left."""
    t = soft_entry(x, y, 0.42)
    ex, ey = polar(x, y, l, a)
    t.curve(polar(x, y, l * 0.5, a + 5), polar(ex, ey, l * 0.25, a + 165), ex, ey, 1.50, ease_in(1.4))
    t.line(ex - 6, ey - 10, 1.10)
    bx, by = polar(ex - 6, ey - 10, barb, 168)
    t.line(bx, by, REGULAR.floor, ease_in(1.6))
    return [t]


def s_coil(x, y, l1=420, l2=470, r=75, turn=245, rise=3.0):
    """A turn whose descending leg curls inward into an open spiral."""
    t = press_entry(x, y)
    cx, cy = polar(x, y, l1, rise)
    _horizontal_body(t, cx - 6, cy, 0.008, 0.78)
    shoulder(t, cx, cy)
    sx, sy, _ = t.end
    lx, ly = sx - 6, sy - (l2 - r)
    t.line(lx, ly, 0.96, wave=lambda u: -0.05 * math.sin(math.pi * u))
    t.spiral(lx - r, ly, -turn, 0.30, 0.24, ease_out(1.3))
    tx, ty, _ = t.end
    t.line(tx + 4, ty - 6, 0.78, ease_out(2))
    t.line(tx - 2, ty - 2, 0.55)
    return [t]


def s_scale(x, y, l=140, a=-18, sag=0.30):
    """A crescent, pointed at both ends and full in the middle."""
    t = Track(x, y, REGULAR.floor)
    ex, ey = polar(x, y, l, a)
    c1 = polar(*polar(x, y, l * 0.25, a), sag * l, a - 90)
    c2 = polar(*polar(x, y, l * 0.75, a), sag * l, a - 90)
    t.curve(c1, c2, ex, ey, REGULAR.floor, linear, wave=lambda u: 1.10 * math.sin(math.pi * u) ** 0.8)
    return [t]


# -- the inventory -----------------------------------------------------------------------------


@dataclass(frozen=True)
class StrokeType:
    id: str
    name: str
    build: Callable
    params: dict  # name -> (minimum, default, maximum)
    skeleton: str
    width: str
    entry: str
    exit: str
    confused: str
    novel: str = ""  # why Teng Chou has it, for a stroke Chinese lacks


def _t(*args, **kw):
    s = StrokeType(*args, **kw)
    return s.id, s


STROKES: dict[str, StrokeType] = dict([
    _t("dot", "Dot", s_dot, {"l": (50, 80, 120), "a": (-75, -55, -35)},
       "a short arc falling to the right", "fine at the head, swelling to full at the foot",
       "soft landing", "rounded, the tip drawn back up",
       "dot-left falls the other way; barb-dot flicks back at the foot; tally is two beads on a hairline"),
    _t("dot-left", "Left dot", s_dot_left, {"l": (50, 80, 120), "a": (-145, -125, -105)},
       "a short arc falling to the left", "fine at the head, full at the foot",
       "soft landing", "rounded, the tip drawn back up",
       "dot falls right; sweep-short is longer and ends in a point, not a bead"),
    _t("horizontal", "Horizontal", s_horizontal, {"l": (120, 480, 820), "rise": (2.0, 4.0, 7.0), "bow": (0.0, 0.012, 0.03)},
       "a line rising to the right, arched very slightly", "pressed head, thin waist before the middle, filling to the pause",
       "angled press", "pause: pressed down-right, lifted back",
       "rise climbs steeply and ends in a point; rods is two short horizontals from one press"),
    _t("vertical", "Vertical", s_vertical, {"l": (140, 520, 860), "lean": (-30, 0, 30), "bow": (0.0, 0.010, 0.025)},
       "a line falling straight, bowed slightly to the left", "pressed head, slight waist, swelling at the foot",
       "angled press", "dew: blunt and rounded",
       "needle ends in a point; vertical-spur ends in a heel and a barb"),
    _t("needle", "Needle", s_needle, {"l": (300, 560, 860), "lean": (-20, 0, 20)},
       "a line falling straight", "full to a little past the middle, then lifting to a point",
       "angled press", "taper to a point",
       "vertical ends blunt; sweep curves away to the left"),
    _t("sweep", "Sweep", s_sweep, {"l": (220, 420, 820), "a": (-150, -128, -100), "curl": (0.0, 0.35, 0.8)},
       "falls almost straight, then curves away down-left", "full from the press, lifting steadily to a point",
       "angled press", "taper to a point",
       "sweep-short is short and nearly flat; needle stays straight"),
    _t("sweep-short", "Short sweep", s_sweep_short, {"l": (80, 150, 240), "a": (-170, -158, -140)},
       "a short, nearly flat stroke to the left", "pressed head, lifting fast to a point",
       "angled press, shallow", "taper to a point",
       "dot-left ends in a bead; sweep is long and falls before it curves"),
    _t("fall", "Fall", s_fall, {"l": (240, 460, 720), "a": (-58, -42, -32), "foot": (0.2, 0.30, 0.4)},
       "a gently waved line falling right, turning flat at the foot", "fine at the head, swelling to the heaviest point of any stroke, then a long taper",
       "soft landing", "foot: flattens and tapers to a point",
       "fall-flat runs nearly level; dot is short and ends in a bead"),
    _t("fall-flat", "Flat fall", s_fall_flat, {"l": (300, 560, 920), "a": (-14, -9, -4), "foot": (0.2, 0.28, 0.4)},
       "a long, nearly level wave, dipping to the foot", "light at the head, swelling to the foot, then a long taper",
       "light press", "foot: tapers to a point",
       "fall drops steeply; horizontal ends in a pause, not a point"),
    _t("rise", "Rise", s_rise, {"l": (80, 200, 320), "a": (18, 32, 48)},
       "a short straight line climbing to the right", "heavy press, lifting at once to a point",
       "heavy press", "taper to a point",
       "horizontal is nearly level and ends blunt; sweep-turn climbs only after a fall"),
    _t("vertical-spur", "Vertical spur", s_vertical_spur, {"l": (200, 560, 860), "spur": (60, 100, 140), "lean": (-20, 0, 20)},
       "a vertical, then a low barb to the left", "as a vertical, a heel at the foot, the barb lifting to a point",
       "angled press", "spur: a heel, and a barb 20 degrees above level",
       "vertical ends blunt; a Chinese vertical hook flicks up at about 45 degrees and is short"),
    _t("turn", "Turn", s_turn, {"l1": (120, 440, 800), "l2": (120, 480, 820), "rise": (2.0, 3.0, 6.0), "slope": (-98, -93, -88)},
       "a horizontal, a shoulder, and a vertical leaning slightly inward", "thin across, full down; the shoulder pressed",
       "angled press", "dew",
       "corner turns at the bottom left, not the top right; turn-spur adds the barb; coil curls"),
    _t("turn-spur", "Turn spur", s_turn_spur, {"l1": (120, 440, 800), "l2": (160, 520, 860), "rise": (2.0, 3.0, 6.0), "spur": (60, 95, 140), "slope": (-98, -93, -88)},
       "a turn, then a low barb to the left", "as a turn; heel and barb at the foot",
       "angled press", "spur",
       "turn ends blunt; coil curls instead of barbing"),
    _t("corner", "Corner", s_corner, {"l1": (100, 380, 760), "l2": (120, 420, 800), "rise": (1.5, 2.5, 5.0)},
       "a vertical, a pressed corner, and a horizontal to the right", "full down, thinner across, a pause at the end",
       "angled press", "pause",
       "bend-spur rounds its corner and barbs; turn has its corner at the top right"),
    _t("bend-spur", "Bend spur", s_bend_spur, {"l1": (160, 380, 700), "l2": (200, 440, 760), "r": (40, 90, 160), "spur": (60, 95, 130)},
       "a vertical, a rounded bend, a level run, and a barb up and to the right", "full down, thinning in the bend, swelling to the heel",
       "angled press", "spur at 55 degrees, leaning forward",
       "corner turns square and ends in a pause; a Chinese vertical-bend hook ends straight up"),
    _t("turn-sweep", "Turn sweep", s_turn_sweep, {"l1": (100, 300, 600), "l2": (180, 380, 600), "rise": (2.0, 3.0, 6.0), "a": (-140, -122, -105)},
       "a short horizontal, a shoulder, and a sweep down-left", "thin across, pressed at the shoulder, lifting to a point",
       "angled press", "taper to a point",
       "turn descends straight and ends blunt; sweep has no horizontal"),
    _t("slant-spur", "Slant spur", s_slant_spur, {"l": (360, 640, 860), "a": (-70, -62, -52), "bow": (0.04, 0.10, 0.16), "spur": (60, 90, 130)},
       "a long curve falling right, bowed outward, and a barb up and to the right", "full and even, a waist past the middle, a heel at the foot",
       "angled press", "spur at 62 degrees",
       "fall ends in a flat foot, not a barb; a Chinese slant hook flicks straight up"),
    _t("sweep-turn", "Sweep turn", s_sweep_turn, {"l1": (100, 200, 320), "l2": (140, 260, 400), "a": (-140, -128, -110), "rise": (8, 18, 30)},
       "a short sweep down-left, a sharp turn, and a climb to the right", "full, easing into the turn, pressed, then lifting to a point",
       "angled press", "taper to a point",
       "rise has no fall before it; corner turns square and runs level"),
    _t("tally", "Tally", s_tally, {"l": (110, 150, 220), "sag": (0.10, 0.22, 0.34)},
       "two beads, the second lower, joined by a sagging hairline", "a bead, a hairline, a heavier bead",
       "soft landing", "rounded, the tip drawn back up",
       "two separate dots, which Chinese pairs constantly, have no hairline; dot is one bead",
       "A ledger is kept in pairs, the entry and its check, and the brush that marks one marks the other without lifting. "
       "No Chinese stroke carries two beads, so where Chinese would set two dots side by side Teng Chou can set one tally."),
    _t("rods", "Rods", s_rods, {"l": (140, 260, 400), "gap": (44, 58, 80), "rise": (2.0, 4.0, 6.0)},
       "one press, and from it two short level rods, the upper shorter", "a heavy shared head, thin rods, each ending in a small pause",
       "heavy press, shared", "two small pauses",
       "two horizontals start apart, each with its own press; horizontal is one rod",
       "The counting-rod bundle: the brush is pressed until its hairs part, so one stroke lays two rods side by side. "
       "It is the stroke of the count component, so numbers and tallies carry it."),
    _t("barb-dot", "Barb dot", s_barb_dot, {"l": (60, 90, 130), "a": (-70, -58, -40), "barb": (45, 70, 100)},
       "a dot falling right, its foot flicking back up and to the left", "fine at the head, full at the foot, the barb lifting to a point",
       "soft landing", "a barb back up and to the left",
       "dot ends rounded; rise climbs to the right, not the left",
       "The mark stroke: a dot that points back at what it marks. It is the stroke of the mark component, "
       "so a Teng Chou indicative is never a Chinese dot."),
    _t("coil", "Coil", s_coil, {"l1": (200, 420, 760), "l2": (260, 470, 800), "r": (50, 75, 110), "turn": (210, 245, 280)},
       "a turn whose leg curls inward, under and back up, into an open spiral", "as a turn; the curl lifting as it winds in",
       "angled press", "the curl's tail, a small press",
       "turn-spur barbs outward; bend-spur rounds a corner and runs on; no Chinese stroke winds back on itself",
       "The wind stroke. Wind in Tantsou thinking is the air that circles the sorted world, and the stroke closes on "
       "itself as nothing in Chinese regular script does. It gives the wind enclosure a right side of its own."),
    _t("scale", "Scale", s_scale, {"l": (80, 140, 220), "a": (-40, -18, 10), "sag": (0.18, 0.30, 0.42)},
       "a shallow crescent, bowed downward", "pointed at both ends, full in the middle",
       "lifted, a point", "lifted, a point",
       "sweep-short is pointed at one end only; fall-flat is long and swells at its foot",
       "The dragon's scale, for the Celestial Dragon and the scaled beasts. Every Chinese stroke lands with "
       "its tip on the paper and grows from there; a scale starts and ends in the air."),
])


def stroke(sid: str, x: float, y: float, style: Style = REGULAR, **params) -> pathops.Path:
    """The outline of one stroke started at (x, y)."""
    st = STROKES[sid]
    for k, v in params.items():
        if k not in st.params:
            raise ValueError(f"{sid}: no parameter {k!r}; it takes {', '.join(st.params)}")
        lo, _, hi = st.params[k]
        if not lo <= v <= hi:
            raise ValueError(f"{sid}: {k}={v} is outside {lo}..{hi}")
    return outline(st.build(x, y, **params), style)


def contours(path: pathops.Path):
    """The outline as polygons, each a list of (x, y)."""
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


def svg_path(path: pathops.Path) -> str:
    """The outline as SVG path data, y up as in the font."""
    return " ".join(
        "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in poly) + " Z" for poly in contours(path)
    )
