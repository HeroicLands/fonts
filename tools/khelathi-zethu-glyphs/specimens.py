# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Render the specimen pages to PNG, all from the built font's own outlines.

    .venv/bin/python tools/khelathi-zethu-glyphs/specimens.py [--font fonts/KhelathiZethuGlyphs-Regular.ttf]
                                              [--out specimens/khelathi-zethu-glyphs]

One chart per group (01-men.png ... 16-strokes-and-figures.png) shows each drawn sign's
.a, .b and .c in a quadrat square with its id and code point. Three sample pages set
inscriptions: the Year 3 regnal date, the first sample of the crocodile hunt, and the whole
of the royal decree scene. Each inscription is set as a right-to-left line and as a column.

The font draws signs, not quadrats: a quadrat is two or more signs stacked or set
side by side, and a royal name sits in a cord oval. Both are laid out here, as the setting's
build lays them. The rules:

- a sign is scaled into its slot by its own box (the font's box width and height, in the
  encoding); a slot is the quadrat, or its half when two signs share it;
- two flat signs stack; a low flat sign stacks under a sign no taller than 64; two narrow
  tall signs stand side by side; anything else fills a quadrat alone;
- the signs after a cord-oval sign in a sample are framed: the smallest stadium whose cord
  clears every framed sign by three hairlines, tied at the left of a line or at the foot of
  a column, with the neighbours at least three hairlines clear of the cord.
"""

import argparse
import json
import math
import sys
from pathlib import Path

import pathops
from fontTools.pens.basePen import BasePen
from fontTools.ttLib import TTFont
from PIL import Image, ImageChops, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from render import label_font  # noqa: E402

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
PAPER = (243, 236, 220)
INK = (29, 26, 23)
GREY = (120, 112, 100)
RULE = (201, 188, 158)
HAIR = 1.5  # the cord's hairline, in quadrat units (a quadrat is 100)
SS = 3

GROUPS = [
    "Men", "Women", "Gods and their attributes", "The body", "Beasts", "Birds",
    "River creatures", "Plants and grain", "Sky, sun and stars", "Land, water and the river",
    "Buildings", "Boats", "Tools, weapons and measures", "Vessels and offerings",
    "Cloth, crowns and adornment", "Strokes and figures",
]


def slug(text: str) -> str:
    return "".join(c if c.isalnum() else "-" for c in text.lower()).strip("-").replace("--", "-")


def gname(sid: str, v: str) -> str:
    return "z" + sid.replace("-", "_") + "." + v


# -- the font's outlines ---------------------------------------------------------------------


class FlattenPen(BasePen):
    def __init__(self, glyphs):
        super().__init__(glyphs)
        self.contours, self.cur = [], None

    def _moveTo(self, p):
        self.cur = [p]

    def _lineTo(self, p):
        self.cur.append(p)

    def _qCurveToOne(self, c, p):
        a = self._getCurrentPoint()
        n = max(2, int(math.hypot(p[0] - a[0], p[1] - a[1]) / 6) + 2)
        for k in range(1, n + 1):
            t = k / n
            m = 1 - t
            self.cur.append((m * m * a[0] + 2 * m * t * c[0] + t * t * p[0], m * m * a[1] + 2 * m * t * c[1] + t * t * p[1]))

    def _curveToOne(self, c1, c2, p):
        a = self._getCurrentPoint()
        n = 12
        for k in range(1, n + 1):
            t = k / n
            m = 1 - t
            self.cur.append(tuple(m ** 3 * a[i] + 3 * m * m * t * c1[i] + 3 * m * t * t * c2[i] + t ** 3 * p[i] for i in (0, 1)))

    def _closePath(self):
        if self.cur:
            self.contours.append(self.cur)
        self.cur = None

    _endPath = _closePath


class Font:
    def __init__(self, path: Path):
        self.tt = TTFont(str(path))
        self.glyphs = self.tt.getGlyphSet()
        self.enc = json.loads((HERE / "encoding.json").read_text(encoding="utf-8"))
        self.signs = {e["id"]: e for e in self.enc["signs"]}
        self._cache = {}

    def contours(self, name):
        if name not in self._cache:
            pen = FlattenPen(self.glyphs)
            self.glyphs[name].draw(pen)
            self._cache[name] = pen.contours
        return self._cache[name]

    def advance(self, name):
        return self.tt["hmtx"][name][0]

    def sign(self, sid: str, v: str = "a"):
        """A placed-able sign: its glyph, its box in quadrat units and where the box sits in the glyph.

        The ink stands centred in the advance, so the box is centred there too."""
        e = self.signs[sid]
        bw, bh = e["box"][v]
        name = gname(sid, v)
        return dict(key=f"{sid}.{v}", glyph=name, box=(bw, bh), ox=(self.advance(name) - 10 * bw) / 2)


def area(pts):
    return sum(x1 * y2 - x2 * y1 for (x1, y1), (x2, y2) in zip(pts, pts[1:] + pts[:1])) / 2


def placed(font: Font, sgn, tx, ty, s):
    """The glyph's contours in page units, with the box's top-left corner at (tx, ty) and s page
    units to a quadrat unit."""
    k = s / 10
    top = 10 * sgn["box"][1]
    return [[(tx + (x - sgn["ox"]) * k, ty + (top - y) * k) for x, y in c] for c in font.contours(sgn["glyph"])]


# -- painting ----------------------------------------------------------------------------------


def fill(img: Image.Image, contours, color=INK):
    """Paint contours: those turning the way the largest does are ink, the others holes."""
    contours = [c for c in contours if len(c) > 2]
    if not contours:
        return
    xs = [p[0] for c in contours for p in c]
    ys = [p[1] for c in contours for p in c]
    x0, y0 = int(min(xs)) - 2, int(min(ys)) - 2
    w, h = int(max(xs)) + 3 - x0, int(max(ys)) + 3 - y0
    mask = Image.new("L", (w * SS, h * SS), 0)
    d = ImageDraw.Draw(mask)
    ordered = sorted(contours, key=lambda c: -abs(area(c)))
    outer = area(ordered[0]) > 0
    for c in ordered:
        d.polygon([((x - x0) * SS, (y - y0) * SS) for x, y in c], fill=255 if (area(c) > 0) == outer else 0)
    mask = mask.resize((w, h), Image.LANCZOS)
    region = img.crop((x0, y0, x0 + w, y0 + h))
    region.paste(Image.new("RGB", (w, h), color), (0, 0), mask)
    img.paste(region, (x0, y0))


# -- the cord oval -----------------------------------------------------------------------------


def _unit(dx, dy):
    L = math.hypot(dx, dy)
    return (dx / L, dy / L) if L > 1e-9 else (0.0, 0.0)


def spline(pts):
    """Open cubic segments through the points; the ends are corners."""
    n = len(pts)
    T = [None] * n
    for i in range(1, n - 1):
        u0 = _unit(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1])
        u1 = _unit(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1])
        T[i] = _unit(u0[0] + u1[0], u0[1] + u1[1])
    segs = []
    for i in range(n - 1):
        p0, p1 = pts[i], pts[i + 1]
        u = _unit(p1[0] - p0[0], p1[1] - p0[1])
        t0 = T[i] if T[i] is not None else (_unit(2 * u[0] - T[i + 1][0], 2 * u[1] - T[i + 1][1]) if T[i + 1] is not None else u)
        t1 = T[i + 1] if T[i + 1] is not None else (_unit(2 * u[0] - T[i][0], 2 * u[1] - T[i][1]) if T[i] is not None else u)
        k = math.hypot(p1[0] - p0[0], p1[1] - p0[1]) / 3
        segs.append((p0, (p0[0] + t0[0] * k, p0[1] + t0[1] * k), (p1[0] - t1[0] * k, p1[1] - t1[1] * k), p1))
    return segs


def bez(seg, t):
    p0, c1, c2, p1 = seg
    m = 1 - t
    return tuple(m ** 3 * p0[k] + 3 * m * m * t * c1[k] + 3 * m * t * t * c2[k] + t ** 3 * p1[k] for k in (0, 1))


def bez_d(seg, t):
    p0, c1, c2, p1 = seg
    m = 1 - t
    return tuple(3 * m * m * (c1[k] - p0[k]) + 6 * m * t * (c2[k] - c1[k]) + 3 * t * t * (p1[k] - c2[k]) for k in (0, 1))


def band(pts, w0, w1, step=4.0):
    """A closed outline round a smooth centreline, width w0 at the start and w1 at the end,
    square across at both ends."""
    segs = spline(pts)
    samples = []
    total = sum(math.hypot(s[3][0] - s[0][0], s[3][1] - s[0][1]) for s in segs)
    acc = 0.0
    for si, s in enumerate(segs):
        L = math.hypot(s[3][0] - s[0][0], s[3][1] - s[0][1])
        k = max(2, int(round(L / step)))
        for q in range(k + (1 if si == len(segs) - 1 else 0)):
            t = q / k
            samples.append((bez(s, t), bez_d(s, t), (acc + L * t) / total))
        acc += L
    left, right = [], []
    for p, d, f in samples:
        nx, ny = _unit(-d[1], d[0])
        w = (w0 + (w1 - w0) * f) / 2
        left.append((p[0] + nx * w, p[1] + ny * w))
        right.append((p[0] - nx * w, p[1] - ny * w))
    return left + right[::-1]


def stadium(x0, y0, x1, y1, n=96):
    """Points round a stadium (a rectangle with round ends) on its long axis."""
    w, h = x1 - x0, y1 - y0
    pts = []
    if w >= h:
        r, L = h / 2, w - h
        per = 2 * L + 2 * math.pi * r
        for k in range(n):
            t = k / n * per
            if t < L:
                pts.append((x0 + r + t, y0))
            elif t < L + math.pi * r:
                a = (t - L) / r - math.pi / 2
                pts.append((x1 - r + r * math.cos(a), y0 + r + r * math.sin(a)))
            elif t < 2 * L + math.pi * r:
                pts.append((x1 - r - (t - L - math.pi * r), y1))
            else:
                a = (t - 2 * L - math.pi * r) / r + math.pi / 2
                pts.append((x0 + r + r * math.cos(a), y0 + r + r * math.sin(a)))
    else:
        r, L = w / 2, h - w
        per = 2 * L + 2 * math.pi * r
        for k in range(n):
            t = k / n * per
            if t < L:
                pts.append((x1, y0 + r + t))
            elif t < L + math.pi * r:
                a = (t - L) / r
                pts.append((x0 + r + r * math.cos(a), y1 - r + r * math.sin(a)))
            elif t < 2 * L + math.pi * r:
                pts.append((x0, y1 - r - (t - L - math.pi * r)))
            else:
                a = (t - 2 * L - math.pi * r) / r + math.pi
                pts.append((x0 + r + r * math.cos(a), y0 + r + r * math.sin(a)))
    return pts


def offset_closed(pts, d):
    out, n = [], len(pts)
    for i in range(n):
        a, b = pts[i - 1], pts[(i + 1) % n]
        tx, ty = _unit(b[0] - a[0], b[1] - a[1])
        out.append((pts[i][0] - ty * d, pts[i][1] + tx * d))
    return out


def _poly(pts, closed):
    p = pathops.Path()
    p.moveTo(*pts[0])
    for x, y in pts[1:]:
        p.lineTo(x, y)
    if closed:
        p.close()
    return p


def _stroke(pts, closed, hair):
    p = _poly(pts, closed)
    p.stroke(hair, pathops.LineCap.BUTT_CAP, pathops.LineJoin.MITER_JOIN, 3.0)
    p.convertConicsToQuads()
    return p


def _disc(cx, cy, r, n=16):
    return _poly([(cx + r * math.cos(2 * math.pi * k / n), cy + r * math.sin(2 * math.pi * k / n)) for k in range(n)], True)


def flatten(path, step=1.2):
    """Contours of a pathops path as point lists."""
    out, cur, here = [], None, None
    for verb, seg in path.segments:
        seg = list(seg)
        if verb == "moveTo":
            cur = [seg[0]]
            here = seg[0]
        elif verb == "lineTo":
            n = max(1, int(math.hypot(seg[0][0] - here[0], seg[0][1] - here[1]) / step))
            cur += [(here[0] + (seg[0][0] - here[0]) * k / n, here[1] + (seg[0][1] - here[1]) * k / n) for k in range(1, n + 1)]
            here = seg[0]
        elif verb == "qCurveTo":
            offs, on = seg[:-1], seg[-1]
            if on is None:
                on = ((offs[-1][0] + offs[0][0]) / 2, (offs[-1][1] + offs[0][1]) / 2)
                cur = [on]
                here = on
            prev = here
            for k, o in enumerate(offs):
                nxt = on if k == len(offs) - 1 else ((o[0] + offs[k + 1][0]) / 2, (o[1] + offs[k + 1][1]) / 2)
                for t in (0.25, 0.5, 0.75, 1.0):
                    m = 1 - t
                    cur.append((m * m * prev[0] + 2 * m * t * o[0] + t * t * nxt[0], m * m * prev[1] + 2 * m * t * o[1] + t * t * nxt[1]))
                prev = nxt
            here = on
        elif verb == "curveTo":
            c = [here] + seg
            for k in range(1, 9):
                t = k / 8
                cur.append(bez(tuple(c), t))
            here = seg[-1]
        elif verb == "closePath":
            out.append(cur)
    return out


def cord(x0, y0, x1, y1, tie, q):
    """The knotted cord round a name, as page contours: a twisted cord on a stadium centreline,
    knotted at intervals, tied at `tie` ('left' or 'bottom') with the seal-knot and two ends."""
    hair = HAIR * q / 100
    cw = 0.034 * q
    centre = stadium(x0, y0, x1, y1, 160)
    parts = [_stroke(offset_closed(centre, cw / 2), True, hair), _stroke(offset_closed(centre, -cw / 2), True, hair)]
    n = len(centre)
    acc, nxt = 0.0, 0.0
    for i in range(n):
        a, b = centre[i - 1], centre[i]
        acc += math.hypot(b[0] - a[0], b[1] - a[1])
        if acc >= nxt:
            tx, ty = _unit(centre[(i + 1) % n][0] - a[0], centre[(i + 1) % n][1] - a[1])
            nx, ny = -ty, tx
            h = cw / 2 - hair * 0.5
            parts.append(_stroke([(b[0] + nx * h - tx * h * 0.7, b[1] + ny * h - ty * h * 0.7),
                                  (b[0] - nx * h + tx * h * 0.7, b[1] - ny * h + ty * h * 0.7)], False, hair))
            nxt += cw * 1.6
    beads = []
    if tie == "left":
        r = (y1 - y0) / 2
        for f in (0.3, 0.5, 0.7):
            bx = x0 + r + (x1 - x0 - 2 * r) * f if x1 - x0 > 2 * r else (x0 + x1) / 2
            beads += [(bx, y0), (bx, y1)]
        kx, ky, dx, dy = x0, (y0 + y1) / 2, -1, 0
    else:
        r = (x1 - x0) / 2
        for f in (0.3, 0.5, 0.7):
            by = y0 + r + (y1 - y0 - 2 * r) * f
            beads += [(x0, by), (x1, by)]
        kx, ky, dx, dy = (x0 + x1) / 2, y1, 0, 1
    L = cw * 4.2
    ends = []
    for side in (-1, 1):
        px, py = -dy * side, dx * side
        spec = [(kx, ky), (kx + dx * L * 0.45 + px * L * 0.22, ky + dy * L * 0.45 + py * L * 0.22),
                (kx + dx * L + px * L * 0.42, ky + dy * L + py * L * 0.42)]
        ends.append(_stroke(band(spec, cw, cw * 0.8), True, hair))
    for bx, by in beads:
        parts.append(_disc(bx, by, cw * 0.75, 10))
    parts.append(_disc(kx, ky, cw * 1.25, 12))
    out = pathops.Path()
    pathops.union(ends + parts, out.getPen())
    return flatten(out)


def min_distance(a_pts, b_pts, cell=4.0):
    grid = {}
    for p in b_pts:
        grid.setdefault((int(p[0] // cell), int(p[1] // cell)), []).append(p)
    best = 1e9
    for p in a_pts:
        gx, gy = int(p[0] // cell), int(p[1] // cell)
        found = False
        for r in range(0, 40):
            for i in range(gx - r, gx + r + 1):
                for j in range(gy - r, gy + r + 1):
                    if max(abs(i - gx), abs(j - gy)) != r:
                        continue
                    for q in grid.get((i, j), ()):
                        d = math.hypot(p[0] - q[0], p[1] - q[1])
                        if d < best:
                            best = d
                        found = True
            if found and r * cell > best + cell:
                break
    return best


def fit_cord(inks, tie, q):
    """The smallest stadium whose cord clears every ink inside it by three hairlines."""
    hair = HAIR * q / 100
    want = 3 * hair
    cw = 0.034 * q
    pts = [p for ink in inks for c in ink for p in c]
    x0, y0 = min(p[0] for p in pts), min(p[1] for p in pts)
    x1, y1 = max(p[0] for p in pts), max(p[1] for p in pts)
    pad = want + cw * 0.8
    sample = pts[::3]
    for grow in [k * 0.6 for k in range(60)]:
        if tie == "left":
            box = (x0 - pad - grow * 1.5, y0 - pad - grow * 0.5, x1 + pad + grow * 1.5, y1 + pad + grow * 0.5)
        else:
            box = (x0 - pad - grow * 0.5, y0 - pad - grow * 1.5, x1 + pad + grow * 0.5, y1 + pad + grow * 1.5)
        c = cord(*box, tie, q)
        if min_distance(sample, [p for cc in c for p in cc]) >= want:
            return box, c
    raise RuntimeError("no cord fits")


# -- quadrats ----------------------------------------------------------------------------------


def group_quadrats(sgns):
    """Group a sample's signs into quadrats in reading order."""
    qs, i = [], 0
    flat = lambda g: g["box"][1] <= 60  # noqa: E731
    narrow = lambda g: g["box"][0] <= 50 and g["box"][1] > 60  # noqa: E731
    sid = lambda g: g["key"].split(".")[0]  # noqa: E731
    while i < len(sgns):
        a = sgns[i]
        b = sgns[i + 1] if i + 1 < len(sgns) else None
        if b is not None and (sid(a), sid(b)) == ("11-001", "11-002"):
            qs.append(dict(rows=[[a], [b]], frame=False))
            i += 2
        elif b is not None and flat(a) and flat(b) and a["box"][1] + b["box"][1] <= 104:
            qs.append(dict(rows=[[a], [b]], frame=False))
            i += 2
        elif b is not None and b["box"][1] <= 40 and a["box"][1] <= 64:
            qs.append(dict(rows=[[a], [b]], frame=False))
            i += 2
        elif b is not None and narrow(a) and narrow(b):
            qs.append(dict(rows=[[a, b]], frame=False))
            i += 2
        else:
            qs.append(dict(rows=[[a]], frame=False))
            i += 1
    return qs


def quadrat_ink(font, q, x, y, size):
    """Lay a quadrat's rows into the square at (x, y): rows split the height, a row's signs split
    its width right to left, each scaled into its slot by its own box. Returns the contours of each sign."""
    out = []
    rows = q["rows"]
    rh = size / len(rows)
    for r, row in enumerate(rows):
        sw = size / len(row)
        for c, sgn in enumerate(row):
            sx = x + size - (c + 1) * sw
            sy = y + r * rh
            bw, bh = sgn["box"]
            slot_w = min(sw, sw * max(bw / 100, 0.45))
            slot_h = min(rh, rh * max(bh / 100, 0.45))
            px, py, pw, ph = sx + (sw - slot_w) / 2, sy + (rh - slot_h) / 2, slot_w, slot_h
            s = min(pw * 0.88 / bw, ph * 0.88 / bh)
            tx = px + (pw - bw * s) / 2
            ty = py + (ph - bh * s) / 2
            out.append(placed(font, sgn, tx, ty, s))
    return out


def _edge_gaps(qs):
    return {i for i in range(len(qs) - 1) if qs[i]["frame"] != qs[i + 1]["frame"]}


def set_inscription(font, qs, Q=120, gap=14):
    """Lay quadrats as a right-to-left line and as a top-down column, the framed ones inside one
    cord (tie at the left in the line, at the foot in the column). Returns dict(line=(inks, cord,
    xs), column=(inks, cord, ys))."""
    hair = HAIR * Q / 100
    edges = _edge_gaps(qs)
    framed_any = any(q["frame"] for q in qs)

    def layout(positions, horizontal):
        inks, framed, outside = [], [], []
        for (x, y), q in zip(positions, qs):
            k = quadrat_ink(font, q, x, y, Q)
            inks += k
            (framed if q["frame"] else outside).extend(k)
        if not framed_any:
            return inks, None, None
        box, c = fit_cord(framed, "left" if horizontal else "bottom", Q)
        cpts = [p for cc in c for p in cc]
        d_out = min((min_distance([p for cc in ink for p in cc][::3], cpts) for ink in outside), default=99 * hair)
        return inks, c, d_out

    res = {}
    n = len(qs)
    extra = 0.0
    width = n * (Q + gap) + 200
    while True:
        xs, x = [], width - 80
        for i in range(n):
            xs.append(x - Q)
            x -= Q + gap + (extra if i in edges else 0)
        inks, c, d_out = layout([(x, 0) for x in xs], True)
        if c is None or d_out >= 3 * hair:
            break
        extra += 2
    res["line"] = (inks, c, xs)
    extra = 0.0
    while True:
        ys, y = [], 0
        for i in range(n):
            ys.append(y)
            y += Q + gap + (extra if i in edges else 0)
        inks, c, d_out = layout([(0, y) for y in ys], False)
        if c is None or d_out >= 3 * hair:
            break
        extra += 2
    res["column"] = (inks, c, ys)
    return res


def shift(contours, dx, dy):
    return [[(x + dx, y + dy) for x, y in c] for c in contours]


def paint_set(img, inks, c, dx, dy):
    if c is not None:
        fill(img, shift(c, dx, dy))
    for ink in inks:
        fill(img, shift(ink, dx, dy))


def sample_quadrats(font, ids, framed_from=None, rows=None):
    """Quadrats for a sample: signs grouped by the stacking rules; those after a cord-oval sign framed."""
    if rows is not None:
        return [dict(rows=[[font.sign(i) for i in row] for row in q["rows"]], frame=q["frame"]) for q in rows]
    if "16-011" in ids:
        at = ids.index("16-011")
        qs = group_quadrats([font.sign(i) for i in ids[:at]])
        return qs + [dict(q, frame=True) for q in group_quadrats([font.sign(i) for i in ids[at + 1 :]])]
    return group_quadrats([font.sign(i) for i in ids])


# -- pages -------------------------------------------------------------------------------------


def page(width, height):
    img = Image.new("RGB", (width, height), PAPER)
    return img, ImageDraw.Draw(img)


def group_chart(font: Font, g: int, out: Path):
    ids = [e["id"] for e in font.enc["signs"] if e["drawn"] and int(e["id"][:2]) == g]
    cols, box, gap = 4, 112, 8
    cw = 3 * box + 2 * gap + 30
    ch = box + 74
    rows = math.ceil(len(ids) / cols)
    width, height = cols * cw + 40, rows * ch + 90
    img, d = page(width, height)
    d.text((20, 18), f"Khelathi Zethu Glyphs, group {g}: {GROUPS[g - 1]} ({len(ids)} signs; .a .b .c left to right)",
           fill=INK, font=label_font(22))
    lab, small = label_font(14), label_font(12)
    for i, sid in enumerate(ids):
        e = font.signs[sid]
        cx = 20 + (i % cols) * cw
        cy = 60 + (i // cols) * ch
        for k, v in enumerate(e["variants"]):
            bx, by = cx + 15 + k * (box + gap), cy + 4
            d.rectangle([bx, by, bx + box, by + box], outline=RULE)
            sgn = font.sign(sid, v)
            s = box * 0.92 / 100
            bw, bh = sgn["box"]
            tx = bx + (box - bw * box / 100 * 0.92) / 2
            ty = by + (box - bh * box / 100 * 0.92) / 2
            fill(img, placed(font, sgn, tx, ty, box * 0.92 / 100))
            d.text((bx + 3, by + 1), "." + v, fill=GREY, font=small)
        mid = cx + 15
        d.text((mid, cy + box + 10), f"{sid}  {e['codepoint']}", fill=INK, font=lab)
        d.text((mid, cy + box + 30), e["subject"][:44], fill=GREY, font=small)
        extra = " ".join(x for x in (e["consonants"], e["god"]) if x)
        if extra:
            d.text((mid, cy + box + 46), extra[:44], fill=GREY, font=small)
    img.save(out)


def inscription_block(font, img, d, title, lines, qs, x0, y0, Q=120):
    """Draw one inscription as a line and a column at (x0, y0); returns the y below the block."""
    res = set_inscription(font, qs, Q)
    inks, c, xs = res["line"]
    d.text((x0, y0), title, fill=INK, font=label_font(24))
    for k, t in enumerate(lines):
        d.text((x0, y0 + 40 + 24 * k), t, fill=GREY, font=label_font(16))
    top = y0 + 50 + 24 * len(lines)
    d.text((x0, top), "A line, read right to left:", fill=INK, font=label_font(15))
    line_y = top + 30
    x_min = min(xs)
    paint_set(img, inks, c, x0 + 110 - x_min, line_y)
    right = x0 + 110 - x_min + max(xs) + Q + 16
    d.text((right, line_y + Q / 2 - 12), "←", fill=INK, font=label_font(28))
    cinks, cc, ys = res["column"]
    col_top = line_y + Q + 50
    d.text((x0, col_top), "The same as a column, read top down:", fill=INK, font=label_font(15))
    paint_set(img, cinks, cc, x0 + 60, col_top + 40)
    return col_top + 40 + ys[-1] + Q + 40, right


def sample_pages(font: Font, out: Path, data: dict):
    extra = {e["name"]: e for e in data["extra"]}
    scenes = {s["scene"]: s for s in data["scenes"]}
    jobs = []
    y3 = extra["sample-year3"]
    jobs.append(("sample-year3.png", "A date: " + y3["title"].split(": ", 1)[-1],
                 [(y3["title"], y3["lines"], sample_quadrats(font, [], rows=y3["quadrats"]))]))
    s1 = scenes["3.1"]["samples"][0]
    jobs.append(("sample-crocodile-hunt.png", "The sacred crocodile hunt, first sample",
                 [(f"{s1['reading']}: {s1['gloss']}", [" + ".join(s1["ids"])], sample_quadrats(font, s1["ids"]))]))
    sc = scenes["3.10"]
    blocks = [(f"{s['reading']}: {s['gloss']}", [" + ".join(s["ids"])], sample_quadrats(font, s["ids"])) for s in sc["samples"]]
    jobs.append(("scene-royal-decree.png", f"A whole scene: {sc['title']}", blocks))
    for name, heading, blocks in jobs:
        # measure first: draw on a tall canvas, then crop
        img, d = page(2000, 6000)
        d.text((30, 20), "Khelathi Zethu Glyphs: " + heading, fill=INK, font=label_font(28))
        y, wide = 80, 0
        for title, lines, qs in blocks:
            y, right = inscription_block(font, img, d, title, lines, qs, 30, y)
            wide = max(wide, right)
        img.crop((0, 0, int(max(wide + 40, 1100)), int(y + 20))).save(out / name)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--font", default=str(ROOT / "fonts" / "KhelathiZethuGlyphs-Regular.ttf"))
    ap.add_argument("--out", default=str(ROOT / "specimens" / "khelathi-zethu-glyphs"))
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    font = Font(Path(args.font))
    for g in range(1, 17):
        group_chart(font, g, out / f"{g:02d}-{slug(GROUPS[g - 1])}.png")
    sample_pages(font, out, json.loads((HERE / "samples.json").read_text(encoding="utf-8")))


if __name__ == "__main__":
    main()
