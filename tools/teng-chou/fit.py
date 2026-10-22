# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Fit the brush outlines' dense polygons with cubic curves, for the font.

    import fit

    contours = fit.fit(path)        # [[(kind, points), ...], ...] per contour

A brush outline is the union of many small footprint hulls, so its contours are
polygons with a point every few units. Each contour is cut at its corners, where
its direction turns by more than ``CORNER`` degrees within a few units, and each
run between two corners is fitted with as few cubic curves as keep every point
within ``TOLERANCE`` units (Schneider's method: a least-squares cubic with the run's
own end tangents, split at the worst point until it fits). A run too short to
bend is a line. Outer contours run counter-clockwise and holes clockwise, as a
UFO wants them.
"""

from __future__ import annotations

import math

TOLERANCE = 1.2  # units
CORNER = 38.0  # degrees
REACH = 6.0  # units over which a contour's direction is measured
MIN_SPACING = 0.6  # points closer than this are merged


def _dedupe(poly):
    out = []
    for p in poly:
        if not out or math.dist(p, out[-1]) >= MIN_SPACING:
            out.append(p)
    if len(out) > 2 and math.dist(out[0], out[-1]) < MIN_SPACING:
        out.pop()
    return out


def _area(poly) -> float:
    return 0.5 * sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(poly, poly[1:] + poly[:1]))


def _inside(pt, poly) -> bool:
    x, y = pt
    inside = False
    for (x0, y0), (x1, y1) in zip(poly, poly[1:] + poly[:1]):
        if (y0 > y) != (y1 > y) and x < x0 + (y - y0) * (x1 - x0) / (y1 - y0):
            inside = not inside
    return inside


def _heading(poly, i, step):
    """Direction of travel measured ``REACH`` units back (step -1) or ahead (step 1) of point i."""
    n = len(poly)
    x0, y0 = poly[i]
    j, dist = i, 0.0
    while dist < REACH:
        k = (j + step) % n
        dist += math.dist(poly[j], poly[k])
        j = k
        if j == i:
            break
    x1, y1 = poly[j]
    return math.atan2((y1 - y0) * step, (x1 - x0) * step)


def _corners(poly):
    out = []
    n = len(poly)
    turns = []
    for i in range(n):
        a = _heading(poly, i, -1)
        b = _heading(poly, i, 1)
        d = abs((b - a + math.pi) % (2 * math.pi) - math.pi)
        turns.append(math.degrees(d))
    for i in range(n):
        if turns[i] >= CORNER and turns[i] >= turns[i - 1] and turns[i] >= turns[(i + 1) % n]:
            if not out or i - out[-1] > 1:
                out.append(i)
    return out


# -- Schneider -----------------------------------------------------------------------------------


def _sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def _add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def _mul(a, k):
    return (a[0] * k, a[1] * k)


def _dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


def _norm(a):
    n = math.hypot(*a)
    return (a[0] / n, a[1] / n) if n else (0.0, 0.0)


def _bez(c, t):
    mt = 1 - t
    return (
        mt**3 * c[0][0] + 3 * mt * mt * t * c[1][0] + 3 * mt * t * t * c[2][0] + t**3 * c[3][0],
        mt**3 * c[0][1] + 3 * mt * mt * t * c[1][1] + 3 * mt * t * t * c[2][1] + t**3 * c[3][1],
    )


def _bez_d(c, t):
    mt = 1 - t
    return (
        3 * mt * mt * (c[1][0] - c[0][0]) + 6 * mt * t * (c[2][0] - c[1][0]) + 3 * t * t * (c[3][0] - c[2][0]),
        3 * mt * mt * (c[1][1] - c[0][1]) + 6 * mt * t * (c[2][1] - c[1][1]) + 3 * t * t * (c[3][1] - c[2][1]),
    )


def _bez_dd(c, t):
    return (
        6 * (1 - t) * (c[2][0] - 2 * c[1][0] + c[0][0]) + 6 * t * (c[3][0] - 2 * c[2][0] + c[1][0]),
        6 * (1 - t) * (c[2][1] - 2 * c[1][1] + c[0][1]) + 6 * t * (c[3][1] - 2 * c[2][1] + c[1][1]),
    )


def _chord(pts):
    u = [0.0]
    for a, b in zip(pts, pts[1:]):
        u.append(u[-1] + math.dist(a, b))
    total = u[-1] or 1.0
    return [x / total for x in u]


def _generate(pts, u, t1, t2):
    p0, p3 = pts[0], pts[-1]
    c = [[0.0, 0.0], [0.0, 0.0]]
    x = [0.0, 0.0]
    for p, t in zip(pts, u):
        a1, a2 = _mul(t1, 3 * (1 - t) ** 2 * t), _mul(t2, 3 * (1 - t) * t * t)
        c[0][0] += _dot(a1, a1)
        c[0][1] += _dot(a1, a2)
        c[1][1] += _dot(a2, a2)
        tmp = _sub(p, _bez((p0, p0, p3, p3), t))
        x[0] += _dot(a1, tmp)
        x[1] += _dot(a2, tmp)
    c[1][0] = c[0][1]
    det = c[0][0] * c[1][1] - c[1][0] * c[0][1]
    seg = math.dist(p0, p3)
    if abs(det) > 1e-12:
        alpha1 = (x[0] * c[1][1] - x[1] * c[0][1]) / det
        alpha2 = (c[0][0] * x[1] - c[1][0] * x[0]) / det
    else:
        alpha1 = alpha2 = seg / 3
    if alpha1 < 1e-6 * seg or alpha2 < 1e-6 * seg:
        alpha1 = alpha2 = seg / 3
    return (p0, _add(p0, _mul(t1, alpha1)), _add(p3, _mul(t2, alpha2)), p3)


def _reparam(c, pts, u):
    out = []
    for p, t in zip(pts, u):
        d = _sub(_bez(c, t), p)
        d1, d2 = _bez_d(c, t), _bez_dd(c, t)
        num = _dot(d, d1)
        den = _dot(d1, d1) + _dot(d, d2)
        out.append(min(1.0, max(0.0, t - num / den)) if abs(den) > 1e-12 else t)
    return out


def _error(c, pts, u):
    worst, at = 0.0, len(pts) // 2
    for i, (p, t) in enumerate(zip(pts, u)):
        d = math.dist(_bez(c, t), p)
        if d > worst:
            worst, at = d, i
    return worst, at


def _fit_run(pts, t1, t2, depth=0):
    if len(pts) == 2:
        seg = math.dist(*pts) / 3
        return [(pts[0], _add(pts[0], _mul(t1, seg)), _add(pts[1], _mul(t2, seg)), pts[1])]
    u = _chord(pts)
    c = _generate(pts, u, t1, t2)
    err, at = _error(c, pts, u)
    if err <= TOLERANCE:
        return [c]
    if err <= TOLERANCE * 4:
        for _ in range(6):
            u = _reparam(c, pts, u)
            c = _generate(pts, u, t1, t2)
            err, at = _error(c, pts, u)
            if err <= TOLERANCE:
                return [c]
    at = max(1, min(len(pts) - 2, at))
    if depth > 24:
        return [(a, a, b, b) for a, b in zip(pts, pts[1:])]
    tc = _norm(_sub(pts[at - 1], pts[at + 1]))
    return _fit_run(pts[: at + 1], t1, tc, depth + 1) + _fit_run(pts[at:], _mul(tc, -1), t2, depth + 1)


def _tangent(pts, forward=True):
    a = pts[0] if forward else pts[-1]
    for b in (pts[1:] if forward else reversed(pts[:-1])):
        if math.dist(a, b) >= 2.0:
            return _norm(_sub(b, a))
    return _norm(_sub(pts[1], pts[0]) if forward else _sub(pts[-2], pts[-1]))


def _fit_contour(poly):
    """One closed polygon as segments: ("line", end) or ("curve", c1, c2, end), starting at poly[0]."""
    corners = _corners(poly)
    if not corners:
        corners = [min(range(len(poly)), key=lambda i: (poly[i][0], poly[i][1]))]
    start = corners[0]
    poly = poly[start:] + poly[:start]
    corners = [(c - start) % len(poly) for c in corners] + [len(poly)]
    ring = poly + [poly[0]]
    segs = []
    for a, b in zip(corners, corners[1:]):
        run = ring[a: b + 1]
        if len(run) < 3 or math.dist(run[0], run[-1]) < 3.0 and len(run) < 5:
            segs.append(("line", run[-1]))
            continue
        straight = max(_line_dist(p, run[0], run[-1]) for p in run) <= TOLERANCE
        if straight:
            segs.append(("line", run[-1]))
            continue
        for c in _fit_run(run, _tangent(run, True), _tangent(run, False)):
            if max(_line_dist(c[1], c[0], c[3]), _line_dist(c[2], c[0], c[3])) <= 0.3:
                segs.append(("line", c[3]))
            else:
                segs.append(("curve", c[1], c[2], c[3]))
    return poly[0], segs


def _line_dist(p, a, b):
    ab = _sub(b, a)
    n = math.hypot(*ab)
    if not n:
        return math.dist(p, a)
    return abs(ab[0] * (a[1] - p[1]) - ab[1] * (a[0] - p[0])) / n


def fit(polygons):
    """Fitted contours from polygons (lists of (x, y)): each ``(start, segments)``, wound
    as a UFO wants (outer counter-clockwise, holes clockwise)."""
    polys = [p for p in (_dedupe(list(map(tuple, q))) for q in polygons) if len(p) >= 3 and abs(_area(p)) > 4]
    out = []
    for i, poly in enumerate(polys):
        depth = sum(1 for j, other in enumerate(polys) if j != i and _inside(poly[0], other))
        want_ccw = depth % 2 == 0
        if (_area(poly) > 0) != want_ccw:
            poly = poly[::-1]
        out.append(_fit_contour(poly))
    return out
