# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Semaron Kuriale's drawing kit: the chancery hand of the Vylarian letters, drawn from Thuravark's staves.

    import kit as K
    K.glyph("th")      # the glyph: contours, advance and catch anchor

Every letter is a Thuravark stave read from its branch table: one stem, and up to four
branches named by side, the level they leave from and the level they end at. The
majuscule keeps that skeleton at the cap height, its branches straight and the pen's
rounding limited to the joins. The minuscule is the full pen form: each branch is a bow
of the system oval, the stem is lengthened where it is free, and the whole is written
with one broad nib held at one angle, so the weight of every stroke follows from its
direction. The row is unjoined and wide-spaced: a Kuriale letter stands apart.

Everything is drawn upright on a baseline at y = 0, the stem at x = 0, then sheared
by the slant; the nib is applied after the shear, as a real pen is held.
build_ufo.py writes the letters into sources/SemaronKuriale.ufo.
"""

import cmath
import math

import pathops
from fontTools.pens.recordingPen import RecordingPen


# =============================================================================
# THE SYSTEM
# =============================================================================

EM = 1000
BODY = 440         # the body: the minuscule's x-height, in units of a 1000 em
ASC = 528          # 1.2 x body: the tall minuscules (l, h, t, th, u) stand here
DESC = -220        # 0.5 x body below the line: p, f, j, s, and g's tail
CAP = 572          # 1.3 x body: every majuscule and every numeral

SLANT = 12         # degrees forward, one slant for every stroke

# The pen: one broad nib, held at one angle to the line. A stroke's width is what the
# nib covers across its direction of travel: full on the diagonal falling forward,
# three quarters on the stems, half on a level stroke, the nib's thickness on a stroke
# rising along the nib's edge. The weight is a fact of the direction, not of pressure.
NIB = 84           # the nib's width: the body is five nibs and a half
NIB_ANGLE = 30     # the nib's edge, degrees from the writing line
HAIR = 28          # the nib's thickness: the thinnest a stroke can be, kept to a pixel at 18 px

# The oval and the reaches. The bowls, arches and cups are cut from one oval, wider
# than tall is not: a width of 0.82 of its height.
OVAL = 0.82
ARCH = 232         # a long branch's reach from the stem: the arch and the cup
HALF = 232         # a half branch's reach: shoulder, bowl, arm, leg, ear
LEG_BACK = 0.55    # the back leg (h, m, s) reaches this fraction of a half reach: a short foot, not a lead-in
APEX = 0.52        # where along the reach an arch crests, as a fraction
SPRING = 0.62      # an arch leaves the stem at this fraction of the body; a cup at 1 - it
ARCH_START = 18    # degrees off the vertical an arch or cup leaves the stem at: steeper than its chord, so it turns once
HALF_START = 30    # the same for a shoulder, bowl or voicing bow
HALF_TOP = 0.80    # a shoulder or ear leaves the stem here; a bowl returns at 1 - it
CUP_LEAN = 18      # a cup's free side leans in this much at the top
RING = 197         # o's ring: half its width, 0.85 of a half reach
HOOD = 181         # e's hood: half its width, 0.78 of a half reach
TAIL = (0.85, 0.8)  # g's tail ends at these fractions of HALF back and DESC down

# Entry, exit and terminals. A stem whose top is free starts with a straight hairline
# wedge; a stem whose foot is free turns once into a straight exit. Every other end is
# the nib's own cut, straight along the nib angle. A stroke that would stop square across
# the nib (its run within ACROSS of the nib's normal) does not stop there: it turns once,
# as the foot does, into the same exit, so it thins and ends in the nib's slanted cut.
ENTRY_ANGLE = 52
ENTRY_LEN = 72
EXIT_ANGLE = 34
EXIT_LEN = 78
FOOT_R = 54
ACROSS = 15        # degrees from the nib's normal within which a bare end reads as a square block

# The marks, written with the same nib. The hook is the breath notch scored across the arm:
# one straight stroke that leaves the stem's middle and runs forward and up through the arch,
# or across the cup or bowl, and out of it. The curl is the long vowel's mark: a small arch seated on the vowel, the
# nib riding along the stroke at its feet so they are hairlines, and turned TWIST degrees
# across it at the crown so the crown swells. The catch is the glottal stop's mark: a grave,
# one short stroke falling from the upper left to the lower right over the letter before it.
# The hook runs on past the arch, cup or bowl it crosses, so its end shows outside the letter, and
# the nib turns across it as it does across the curl's crown: hairline at the stem and at the tip,
# swelling where it crosses. Held at the writing angle, a stroke rising forward runs along the nib's
# edge and is a hairline its whole length.
HOOK = (1.25, 70)   # the hook ends this fraction of a half reach forward, this far above the body line
HOOK_TWIST = 55     # degrees the nib turns across the hook at its middle
BURY = 30          # a branch's first run is straight, this long, at its heading, from the stem's centreline out
ARM_THROUGH = (1.5, 90)  # v's arm runs on through the arch, to here past the half reach and above the body
CURL = (104, 48)   # the curl's width and height, centred on the stem: its feet stand on the stem's shoulders
CURL_FEET = 68     # degrees from the level the curl's feet stand at
TWIST = 14         # degrees the nib turns across the curl at its crown
CURL_SINK = 10     # the curl's underside sits this far into the letter's top where they are closest
GRAVE = (70, -80)  # the catch's run from its head to its foot
MARK_GAP = 24      # the clearance between the catch and the letter it sits over or beside
BESIDE = 48        # on a tall letter the catch's head sits this far below the stem's top, at its upper right
DOT_RUN = NIB      # the point, the one pause mark: the nib drawn this far straight down, a diamond at mid-height

# The majuscule: the stave's straight branches at the cap height.
LONG_C = 0.40      # a long branch's run, as a fraction of the cap
HALF_C = 0.46      # a half branch's run
FILLET = 72        # a branch turns off the stem over this run

# The numerals.
LIMB = 0.30        # a limb's run, as a fraction of the cap: steeper than any letter's branch
LIMB_DROP = 0.40   # how far a limb falls
LIMBS = {8: ("F", 0.92), 4: ("F", 0.58), 2: ("B", 0.76), 1: ("B", 0.42)}  # leaving at heights no branch leaves from
NOUGHT = (0.20, 0.17)  # nought's ring at the foot: half-width and half-height, of the cap

# Spacing: close, as a book hand sets: the white between letters about a counter, and the
# word space about two stems, enough to read the words apart.
BEAR = 12
SPACE = 24

TAN = math.tan(math.radians(SLANT))
M = BODY / 2


# =============================================================================
# Hobby's algorithm and the curvature-continuous refit (the Pirzath Hand machinery)
# =============================================================================


def _wrap(a):
    while a > math.pi:
        a -= 2 * math.pi
    while a <= -math.pi:
        a += 2 * math.pi
    return a


def _vel(th, ph):
    st, ct, sp, cp = math.sin(th), math.cos(th), math.sin(ph), math.cos(ph)
    num = 2 + math.sqrt(2) * (st - sp / 16) * (sp - st / 16) * (ct - cp)
    den = 3 * (1 + 0.5 * (math.sqrt(5) - 1) * ct + 0.5 * (3 - math.sqrt(5)) * cp)
    return num / den


def _solve(A, b):
    n = len(b)
    Mx = [row[:] + [b[i]] for i, row in enumerate(A)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(Mx[r][c]))
        Mx[c], Mx[p] = Mx[p], Mx[c]
        for r in range(n):
            if r != c and Mx[r][c]:
                f = Mx[r][c] / Mx[c][c]
                for k in range(c, n + 1):
                    Mx[r][k] -= f * Mx[c][k]
    return [Mx[i][n] / Mx[i][i] for i in range(n)]


def hobby(pts, dirs, tension=1.0):
    """Cubic segments [(c1, c2, z)] through pts; dirs[k] in radians or None."""
    n = len(pts) - 1
    d = [abs(pts[k + 1] - pts[k]) for k in range(n)]
    a = [cmath.phase(pts[k + 1] - pts[k]) for k in range(n)]
    N = 2 * n
    th = lambda k: k  # noqa: E731
    ph = lambda k: n + k - 1  # noqa: E731
    A, b = [], []

    def eq(coefs, rhs):
        row = [0.0] * N
        for i, c in coefs:
            row[i] += c
        A.append(row)
        b.append(rhs)

    if dirs[0] is not None:
        eq([(th(0), 1)], _wrap(dirs[0] - a[0]))
    else:
        eq([(th(0), 1), (ph(1), -1)], 0)
    for k in range(1, n):
        if dirs[k] is not None:
            eq([(th(k), 1)], _wrap(dirs[k] - a[k]))
            eq([(ph(k), 1)], _wrap(a[k - 1] - dirs[k]))
        else:
            psi = _wrap(a[k] - a[k - 1])
            eq([(th(k), 1), (ph(k), 1)], -psi)
            eq([(th(k - 1), 1 / d[k - 1]), (ph(k), 2 / d[k - 1]), (th(k), -2 / d[k]), (ph(k + 1), -1 / d[k])], 0)
    if dirs[n] is not None:
        eq([(ph(n), 1)], _wrap(a[n - 1] - dirs[n]))
    else:
        eq([(ph(n), 1), (th(n - 1), -1)], 0)
    x = _solve(A, b)
    segs = []
    for k in range(n):
        t0, p1 = x[th(k)], x[ph(k + 1)]
        rho, sig = _vel(t0, p1) / tension, _vel(p1, t0) / tension
        c1 = pts[k] + rho * d[k] * cmath.exp(1j * (a[k] + t0))
        c2 = pts[k + 1] - sig * d[k] * cmath.exp(1j * (a[k] - p1))
        segs.append((c1, c2, pts[k + 1]))
    return segs


SMOOTH = True
FLAT_PINS = 2
SMOOTH_SPACING = 9.0
SMOOTH_BEND = 30.0
EXTEND = 40.0


def _unit(v):
    d = abs(v)
    return v / d if d else v


def _bez(c, t):
    s = 1 - t
    return s ** 3 * c[0] + 3 * s * s * t * c[1] + 3 * s * t * t * c[2] + t ** 3 * c[3]


def _knotvec(n):
    inner = [i / (n - 3) for i in range(1, n - 3)]
    return [0.0] * 4 + inner + [1.0] * 4


def _basis(T, n, deg, u):
    m = len(T) - 1
    if u >= T[-1]:
        k = max(i for i in range(m) if T[i] < T[i + 1])
    else:
        k = max(i for i in range(m) if T[i] <= u < T[i + 1])
    N = [0.0] * m
    N[k] = 1.0
    for d in range(1, deg + 1):
        for i in range(max(0, k - d), min(k, m - d - 1) + 1):
            a = (u - T[i]) / (T[i + d] - T[i]) * N[i] if T[i + d] > T[i] else 0.0
            b = (T[i + d + 1] - u) / (T[i + d + 1] - T[i + 1]) * N[i + 1] if T[i + d + 1] > T[i + 1] else 0.0
            N[i] = a + b
    return N[:n]


def _bs_eval(Q, T, u):
    N = _basis(T, len(Q), 3, u)
    return sum(c * q for c, q in zip(N, Q))


def _bs_deriv(Q, T, u):
    n = len(Q)
    D = [3 * (Q[i + 1] - Q[i]) / (T[i + 4] - T[i + 1]) for i in range(n - 1)]
    N = _basis(T[1:-1], n - 1, 2, u)
    return sum(c * q for c, q in zip(N, D))


def _arc(p, d, kappa, length):
    if abs(kappa) < 1e-5:
        return [(p + d * length / 3, p + d * 2 * length / 3, p + d * length)]
    out = []
    n = 2
    for _ in range(n):
        a = kappa * length / n
        r = 1 / kappa
        centre = p + 1j * d * r
        q = centre + (p - centre) * cmath.exp(1j * a)
        dq = d * cmath.exp(1j * a)
        h = 4 / 3 * math.tan(a / 4) * r
        out.append((p + d * h, q - dq * h, q))
        p, d = q, dq
    return out


def _end_kappa(q):
    d1, d2 = 3 * (q[1] - q[0]), 6 * (q[2] - 2 * q[1] + q[0])
    v = abs(d1)
    return (d1.conjugate() * d2).imag / v ** 3 if v > 1e-9 else 0.0


def _split(q, t):
    a, b, c, d = q
    ab, bc, cd = a + (b - a) * t, b + (c - b) * t, c + (d - c) * t
    abc, bcd = ab + (bc - ab) * t, bc + (cd - bc) * t
    m = abc + (bcd - abc) * t
    return [a, ab, abc, m], [m, bcd, cd, d]


def _trim(p0, spans, start, end):
    qs = []
    prev = p0
    for c1, c2, z in spans:
        qs.append([prev, c1, c2, z])
        prev = z

    def span_len(q):
        return sum(abs(_bez(q, (k + 1) / 8) - _bez(q, k / 8)) for k in range(8))

    def locate(target, from_end):
        order = range(len(qs) - 1, -1, -1) if from_end else range(len(qs))
        near, run = [], 0.0
        for i in order:
            near.append(i)
            run += span_len(qs[i])
            if run > 2.5 * EXTEND:
                break
        best = None
        for i in near:
            q = qs[i]
            for k in range(0, 65):
                t = k / 64
                d = abs(_bez(q, t) - target)
                if best is None or d < best[0]:
                    best = (d, i, t)
        _, i, t = best
        for _ in range(4):
            lo, hi = max(0.0, t - 1 / 64), min(1.0, t + 1 / 64)
            ts = [lo + (hi - lo) * j / 16 for j in range(17)]
            t = min(ts, key=lambda u: abs(_bez(qs[i], u) - target))
        return i, t

    if start is not None:
        i, t = locate(start, False)
        qs = [_split(qs[i], t)[1]] + qs[i + 1:]
    if end is not None:
        i, t = locate(end, True)
        qs = qs[:i] + [_split(qs[i], t)[0]]
    return qs[0][0], [(q[1], q[2], q[3]) for q in qs]


def _smooth_run(p0, cubics, flat=(True, True), extended=False):
    f0, f1 = flat
    start = end = None
    if not extended and (not f0 or not f1):
        q0 = [p0, *cubics[0]]
        qn = [cubics[-2][2] if len(cubics) > 1 else p0, *cubics[-1]]
        if not f0:
            d0 = _unit(q0[1] - q0[0] if abs(q0[1] - q0[0]) > 1e-9 else q0[2] - q0[0])
            k0 = _end_kappa(q0)
            back = _arc(p0, -d0, -k0, EXTEND)
            ext_start = back[-1][2]
            pts_b = [p0] + [c[2] for c in back]
            pre = []
            for (c1, c2, z), a in zip(reversed(back), reversed(pts_b[:-1])):
                pre.append((c2, c1, a))
            start = p0
            p0 = ext_start
            cubics = pre + list(cubics)
        if not f1:
            rq = [qn[3], qn[2], qn[1], qn[0]]
            d1 = _unit(rq[1] - rq[0] if abs(rq[1] - rq[0]) > 1e-9 else rq[2] - rq[0])
            k1 = _end_kappa(rq)
            fwd = _arc(qn[3], -d1, -k1, EXTEND)
            end = qn[3]
            cubics = list(cubics) + fwd
        res = _smooth_run(p0, cubics, (FLAT_PINS == 3, FLAT_PINS == 3), extended=True)
        if res is None:
            return None
        return _trim(p0, res[1], start, end)
    pts = [p0]
    prev = p0
    for c1, c2, z in cubics:
        q = [prev, c1, c2, z]
        for k in range(1, 25):
            t = k / 24
            s_ = 1 - t
            pts.append(s_ ** 3 * q[0] + 3 * s_ * s_ * t * q[1] + 3 * s_ * t * t * q[2] + t ** 3 * q[3])
        prev = z
    cum = [0.0]
    for a, b in zip(pts, pts[1:]):
        cum.append(cum[-1] + abs(b - a))
    length = cum[-1]
    if length < 1e-6:
        return None
    t0 = _unit(cubics[0][0] - p0 if abs(cubics[0][0] - p0) > 1e-9 else cubics[0][1] - p0)
    t1 = _unit(cubics[-1][2] - cubics[-1][1] if abs(cubics[-1][2] - cubics[-1][1]) > 1e-9 else cubics[-1][2] - cubics[-1][0])
    n = max(6, min(160, round(length / SMOOTH_SPACING) + 4))
    T = _knotvec(n)
    P0, P1 = pts[0], pts[-1]
    f0, f1 = f0 and FLAT_PINS == 3, f1 and FLAT_PINS == 3
    free = list(range(3 if f0 else 2, n - 3 if f1 else n - 2))
    nu = 4 + 2 * len(free)

    def ctrl_terms(i):
        if i == 0:
            return P0, []
        if i == 1:
            return P0, [(0, t0)]
        if i == 2 and f0:
            return P0, [(1, t0)]
        if i == n - 1:
            return P1, []
        if i == n - 2:
            return P1, [(nu - 2, -t1)]
        if i == n - 3 and f1:
            return P1, [(nu - 1, -t1)]
        j = free.index(i)
        return 0, [(2 + 2 * j, 1), (3 + 2 * j, 1j)]

    terms = [ctrl_terms(i) for i in range(n)]
    us = [c / length for c in cum]
    lam = SMOOTH_BEND * len(pts) / n
    for _ in range(3):
        AtA = [[0.0] * nu for _ in range(nu)]
        Atb = [0.0] * nu

        def add(coefs, rhs, w=1.0):
            for part in (lambda z: z.real, lambda z: z.imag):
                row = {k: part(v) for k, v in coefs.items()}
                r = part(rhs)
                for k1, v1 in row.items():
                    if not v1:
                        continue
                    Atb[k1] += w * v1 * r
                    for k2, v2 in row.items():
                        AtA[k1][k2] += w * v1 * v2

        for S, u in zip(pts, us):
            N = _basis(T, n, 3, u)
            const, coefs = 0, {}
            for i, c in enumerate(N):
                if not c:
                    continue
                k0, ts = terms[i]
                const += c * k0
                for k, v in ts:
                    coefs[k] = coefs.get(k, 0) + c * v
            add(coefs, S - const)
        for i in range(0, n - 3):
            const, coefs = 0, {}
            for w_, idx in ((1, i), (-3, i + 1), (3, i + 2), (-1, i + 3)):
                k0, ts = terms[idx]
                const += w_ * k0
                for k, v in ts:
                    coefs[k] = coefs.get(k, 0) + w_ * v
            add(coefs, -const, lam)
        for k in range(nu):
            AtA[k][k] += 1e-9
        x = _solve(AtA, Atb)
        Q = []
        for k0, ts in terms:
            Q.append(k0 + sum(v * x[k] for k, v in ts))
        nus = []
        for S, u in zip(pts, us):
            for _ in range(3):
                c = _bs_eval(Q, T, u)
                d = _bs_deriv(Q, T, u)
                dd = abs(d) ** 2
                if dd < 1e-12:
                    break
                u = min(1.0, max(0.0, u + ((S - c).conjugate() * d).real / dd))
            nus.append(u)
        nus[0], nus[-1] = 0.0, 1.0
        us = nus
    out = []
    for k in range(3, n):
        a, b = T[k], T[k + 1]
        if b <= a:
            continue
        z0, z1 = _bs_eval(Q, T, a), _bs_eval(Q, T, b)
        d0, d1 = _bs_deriv(Q, T, a), _bs_deriv(Q, T, b - 1e-12)
        out.append((z0 + d0 * (b - a) / 3, z1 - d1 * (b - a) / 3, z1))
    out[-1] = (out[-1][0], out[-1][1], P1)
    return P0, out


def smooth(segs):
    """The segment list with every run of curves refitted as one curvature-continuous curve.
    A run that meets a straight segment leaves it with no step; a free end keeps its curvature."""
    if not SMOOTH:
        return segs
    out, i = [], 0
    while i < len(segs):
        if segs[i][0] != "C":
            out.append(segs[i])
            i += 1
            continue
        j = i
        while j < len(segs) and segs[j][0] == "C":
            j += 1
        p0 = segs[i - 1][-1]
        f0 = segs[i - 1][0] == "L"
        f1 = j < len(segs) and segs[j][0] == "L"
        run = _smooth_run(p0, [sg[1:] for sg in segs[i:j]], flat=(f0, f1))
        if run is None:
            out += segs[i:j]
        else:
            start, spans = run
            if out and out[-1][0] == "M":
                out[-1] = ("M", start)
            out += [("C", *c) for c in spans]
        i = j
    return out


# =============================================================================
# Strokes
# =============================================================================


def K(x, y, d=None):
    """A knot: position and heading in upright degrees (None leaves it free)."""
    return (x, y, d)


def line(x0, y0, x1, y1):
    return ("L", (x0, y0), (x1, y1))


class Stroke:
    """A centreline: a list of runs. A run is a list of knots (a Hobby curve) or a straight
    segment ("L", (x0, y0), (x1, y1)). Consecutive runs share a point. The pen is the one
    broad nib for everything; `kind` names the part for the sheets and the checks."""

    def __init__(self, runs, kind="stroke", twist=None):
        self.runs = runs
        self.kind = kind
        self.twist = twist   # degrees the nib turns across the stroke at its middle; None holds the writing angle

    def polys(self):
        return sweep(self.segments(), self.twist)

    def segments(self):
        out = []
        for r in self.runs:
            if isinstance(r, tuple) and r[0] == "L":
                (x0, y0), (x1, y1) = r[1], r[2]
                if not out:
                    out.append(("M", complex(x0, y0)))
                out.append(("L", complex(x1, y1)))
                continue
            pts = [complex(k[0], k[1]) for k in r]
            dirs = [math.radians(k[2]) if k[2] is not None else None for k in r]
            if not out:
                out.append(("M", pts[0]))
            for c1, c2, z in hobby(pts, dirs):
                out.append(("C", c1, c2, z))
        return smooth(out)


# =============================================================================
# The pen: sample, shear, sweep the nib
# =============================================================================


def shear(x, y):
    return x + y * TAN, y


def sample(segs, step=3.0):
    """Points along the centreline, upright, about `step` apart."""
    pts = []
    cur = None
    for op, *zs in segs:
        if op == "M":
            cur = zs[0]
            pts.append(cur)
        elif op == "L":
            z = zs[0]
            n = max(1, int(abs(z - cur) / step))
            for k in range(1, n + 1):
                pts.append(cur + (z - cur) * k / n)
            cur = z
        else:
            c1, c2, z = zs
            q = [cur, c1, c2, z]
            approx = abs(c1 - cur) + abs(c2 - c1) + abs(z - c2)
            n = max(2, int(approx / step))
            for k in range(1, n + 1):
                pts.append(_bez(q, k / n))
            cur = z
    return pts


_NA = math.radians(NIB_ANGLE)
NIB_VEC = (NIB / 2 * math.cos(_NA), NIB / 2 * math.sin(_NA))
HAIR_VEC = (-HAIR / 2 * math.sin(_NA), HAIR / 2 * math.cos(_NA))


def nib_at(p, angle=None):
    """The four corners of the nib standing on point p (sheared coordinates), its edge at the
    writing angle or at `angle` degrees where the pen is turned."""
    if angle is None:
        (nx, ny), (hx, hy) = NIB_VEC, HAIR_VEC
    else:
        a = math.radians(angle)
        (nx, ny), (hx, hy) = (NIB / 2 * math.cos(a), NIB / 2 * math.sin(a)), (-HAIR / 2 * math.sin(a), HAIR / 2 * math.cos(a))
    x, y = p
    return [(x + nx + hx, y + ny + hy), (x + nx - hx, y + ny - hy), (x - nx - hx, y - ny - hy), (x - nx + hx, y - ny + hy)]


def hull(points):
    pts = sorted(set(points))
    if len(pts) < 3:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def width_of(heading):
    """The width the nib lays down across a stroke heading `heading` degrees (sheared frame):
    the nib's edge and its thickness, each projected across the stroke."""
    n = math.radians(heading + 90)
    return abs(NIB * math.cos(n - _NA)) + abs(HAIR * math.sin(n - _NA))


LEVEL_HALF = width_of(0) / 2   # half the height of a level stroke: how far a bar's ink reaches from its centreline


def across_nib(heading):
    """Whether a stroke heading `heading` degrees (upright frame) runs, after the shear, within
    ACROSS degrees of the nib's normal, so a bare end there is cut square across the stroke."""
    h = math.radians(heading)
    dx, dy = math.cos(h) + math.sin(h) * TAN, math.sin(h)
    th = math.degrees(math.atan2(dy, dx)) % 180
    return abs((th - (NIB_ANGLE + 90) + 90) % 180 - 90) <= ACROSS


def sweep(segs, twist=None):
    """The nib swept along a centreline: a list of small convex polygons (sheared). The nib
    lays down its width across the direction of travel, and its own cut at either end. With
    `twist`, the pen is turned as it goes: its edge lies along the stroke at either end, so
    the ends are hairlines, and turns `twist` degrees across it at the middle."""
    raw = sample(segs)
    pts = [shear(p.real, p.imag) for p in raw]
    clean = [pts[0]]
    for p in pts[1:]:
        if abs(p[0] - clean[-1][0]) + abs(p[1] - clean[-1][1]) > 1e-6:
            clean.append(p)
    if len(clean) == 1:
        return [nib_at(clean[0])]
    if twist is None:
        return [hull(nib_at(a) + nib_at(b)) for a, b in zip(clean, clean[1:])]
    cum = [0.0]
    for a, b in zip(clean, clean[1:]):
        cum.append(cum[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
    angles = []
    for i, p in enumerate(clean):
        a, b = clean[max(0, i - 1)], clean[min(len(clean) - 1, i + 1)]
        tangent = math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
        angles.append(tangent + twist * math.sin(math.pi * cum[i] / cum[-1]))
    return [hull(nib_at(a, ta) + nib_at(b, tb)) for a, b, ta, tb in zip(clean, clean[1:], angles, angles[1:])]


def union(polys):
    """One outline from many polygons, as (signed area, contour) with the largest first."""
    builder = pathops.OpBuilder(fix_winding=True, keep_starting_points=False)
    for poly in polys:
        if len(poly) < 3:
            continue
        p = pathops.Path()
        p.moveTo(*poly[0])
        for pt in poly[1:]:
            p.lineTo(*pt)
        p.close()
        builder.add(p, pathops.PathOp.UNION)
    result = builder.resolve()
    pen = RecordingPen()
    result.draw(pen)
    contours, cur = [], []
    for op, args in pen.value:
        if op == "moveTo":
            cur = [args[0]]
        elif op == "lineTo":
            cur.append(args[0])
        elif op == "qCurveTo":
            offs, end = list(args[:-1]), args[-1]
            ons = [((a[0] + b[0]) / 2, (a[1] + b[1]) / 2) for a, b in zip(offs, offs[1:])] + [end]
            p0 = cur[-1]
            for c, p1 in zip(offs, ons):
                for k in range(1, 9):
                    t = k / 8
                    u = 1 - t
                    cur.append((u * u * p0[0] + 2 * u * t * c[0] + t * t * p1[0],
                                u * u * p0[1] + 2 * u * t * c[1] + t * t * p1[1]))
                p0 = p1
        elif op == "curveTo":
            q = [complex(*cur[-1])] + [complex(*a) for a in args]
            for k in range(1, 9):
                z = _bez(q, k / 8)
                cur.append((z.real, z.imag))
        elif op in ("closePath", "endPath") and cur:
            contours.append(cur)
            cur = []
    if cur:
        contours.append(cur)

    def area(c):
        return sum(x1 * y2 - x2 * y1 for (x1, y1), (x2, y2) in zip(c, c[1:] + c[:1])) / 2

    return sorted(((area(c), c) for c in contours), key=lambda ac: -abs(ac[0]))


# =============================================================================
# The kit: the parts every minuscule is cut from
# =============================================================================


def final(x, y, heading):
    """The terminal every free end shares: from (x, y), heading `heading` (falling), the stroke
    turns once, left, about a radius of FOOT_R, into the straight exit along EXIT_ANGLE and
    stops. Its knots are the arc's start, its lowest point and its end. Returns the runs."""
    r = FOOT_R
    h, e = math.radians(heading), math.radians(EXIT_ANGLE)
    cx, cy = x - r * math.sin(h), y + r * math.cos(h)
    mid = 0.0 if h < 0 < e else (h + e) / 2
    mx, my = cx + r * math.sin(mid), cy - r * math.cos(mid)
    px, py = cx + r * math.sin(e), cy - r * math.cos(e)
    ex, ey = px + EXIT_LEN * math.cos(e), py + EXIT_LEN * math.sin(e)
    return [[K(x, y, heading), K(mx, my, math.degrees(mid)), K(px, py, EXIT_ANGLE)], line(px, py, ex, ey)]


def final_start(x, level, heading):
    """Where a run heading `heading` must end for its final's turn to bottom on `level`, with
    the arc's lowest point at x."""
    r = FOOT_R
    h = math.radians(heading)
    return x + r * math.sin(h), level + r - r * math.cos(h)


def foot_turn(x):
    """The foot: a stem falling down x turns once into the straight exit. Returns the runs
    from (x, FOOT_R) down and out, ending on the exit's straight run."""
    return final(x, FOOT_R, -90)


def entry_run(top):
    """The entry wedge: a straight hairline rising into the stem's top."""
    e = math.radians(ENTRY_ANGLE)
    return line(-ENTRY_LEN * math.cos(e), top - ENTRY_LEN * math.sin(e), 0, top)


def from_stem(y0, heading):
    """A branch's first run: straight, at its heading, from the stem's centreline at y0 out to
    where the curve begins. The run starts under the stem's own nib, so no corner of the pen
    shows past the stem's edge, and the curve leaves it pinned to one direction and turns
    once. Returns the run and the curve's first knot."""
    h = math.radians(heading)
    x1, y1 = BURY * math.cos(h), y0 + BURY * math.sin(h)
    return line(0, y0, x1, y1), K(x1, y1, heading)


def into_stem(y1, heading):
    """A stroke's last run: straight, at its heading, ending on the stem's centreline at y1.
    Returns the curve's last knot and the run."""
    h = math.radians(heading)
    x0, y0 = -BURY * math.cos(h), y1 - BURY * math.sin(h)
    return K(x0, y0, heading), line(x0, y0, 0, y1)


def half_depth(reach):
    """The depth of the quarter oval that turns an arch or cup's crest into its side."""
    return reach * (1 - APEX) / OVAL


def arch(side, top=BODY):
    """FT0 / BT0: a long branch from the top, bowed over and falling to the line, with a foot."""
    s = 1 if side == "F" else -1
    hd = half_depth(ARCH)
    h0 = 90 - s * ARCH_START
    pin, k0 = from_stem(SPRING * top, h0)
    knots = [k0, K(s * ARCH * APEX, top, 0 if s > 0 else 180), K(s * ARCH, top - hd, -90)]
    return Stroke([pin, knots, line(s * ARCH, top - hd, s * ARCH, FOOT_R)] + foot_turn(s * ARCH), "arch " + side)


def cup_knots(side):
    s = 1 if side == "F" else -1
    hd = half_depth(ARCH)
    return [K(s * ARCH * APEX, 0, 0 if s > 0 else 180), K(s * ARCH, hd, 90), K(s * (ARCH - CUP_LEAN), BODY, 90 + s * 10)]


def cup_back():
    """B0T: a long branch from the foot, rising back in a bow to the body line."""
    h0 = -(90 + ARCH_START)
    pin, k0 = from_stem((1 - SPRING) * BODY, h0)
    return Stroke([pin, [k0] + cup_knots("B")], "cup B")


def shoulder(side):
    """FTM / BTM: a half branch from the top, bowed forward (a shoulder) or back (an ear) to the middle."""
    s = 1 if side == "F" else -1
    h0 = 90 - s * HALF_START
    pin, k0 = from_stem(HALF_TOP * BODY, h0)
    return Stroke([pin, [k0, K(s * HALF * 0.5, BODY, 0 if s > 0 else 180), K(s * HALF, M, -90)]], "shoulder " + side)


def bowl(side):
    """FTM + F0M (or the back pair): the two half branches that meet at the middle, closed by the pen
    into one bowl from the stem's top to its foot."""
    s = 1 if side == "F" else -1
    h0, h1 = 90 - s * HALF_START, 90 + s * HALF_START
    pin0, k0 = from_stem(HALF_TOP * BODY, h0)
    k1, pin1 = into_stem((1 - HALF_TOP) * BODY, h1)
    return Stroke([pin0,
                   [k0, K(s * HALF * 0.5, BODY, 0 if s > 0 else 180), K(s * HALF, M, -90),
                    K(s * HALF * 0.5, 0, 180 if s > 0 else 0), k1],
                   pin1], "bowl " + side)


def voicing(side="B"):
    """B0M: the voicing branch of b and v, a bow from the foot rising back to the middle, where it
    meets the back arch's leg and closes it. F0M alone is its mirror, the lower half of a bowl."""
    s = 1 if side == "F" else -1
    h0 = -(90 - s * HALF_START)
    pin, k0 = from_stem((1 - HALF_TOP) * BODY, h0)
    return Stroke([pin, [k0, K(s * HALF * 0.5, 0, 0 if s > 0 else 180), K(s * HALF, M, 90)]],
                  "voicing" if s < 0 else "voicing F")


def arm(side, through=False):
    """FMT / BMT: a half branch from the middle rising to the top, bowed. v's forward arm runs
    on through the arch and out of it, as the carved branch crosses the arm."""
    s = 1 if side == "F" else -1
    end = (s * HALF * ARM_THROUGH[0], BODY + ARM_THROUGH[1]) if through else (s * HALF, BODY)
    h0 = 90 - s * 20
    pin, k0 = from_stem(M, h0)
    return Stroke([pin, [k0, K(end[0], end[1], 90 - s * 35)]], "arm " + side)


def leg(side, through=False):
    """FM0 / BM0: a half branch from the middle falling to the foot, bowed. The forward leg would
    stop square across the nib at the line, so it takes the final: it turns out and exits. The
    back leg is short, LEG_BACK of the reach, so it reads as the letter's foot and not as a
    lead-in reaching under the letter before."""
    s = 1 if side == "F" else -1
    h0, h1 = -(90 - s * 20), -(90 - s * 35)
    reach = HALF if s > 0 else HALF * LEG_BACK
    end_y = 0
    if through:
        # a leg on the side of a cup runs on through the cup's foot and out of it, as v's arm runs
        # through its arch: its own reach lengthened as the arm's is, and as far below the line as
        # the arm rises above the body, so the back leg stays a foot under its own letter
        reach, end_y = reach * ARM_THROUGH[0], -ARM_THROUGH[1]
    pin, k0 = from_stem(M, h0)
    if across_nib(h1):
        x1, y1 = final_start(s * reach, end_y, h1)
        return Stroke([pin, [k0, K(x1, y1, h1)]] + final(x1, y1, h1), "leg " + side)
    return Stroke([pin, [k0, K(s * reach, end_y, h1)]], "leg " + side)


def tail():
    """g's BM0, carried below the line by the pen."""
    pin, k0 = from_stem(M, -110)
    return Stroke([pin, [k0, K(-HALF * TAIL[0], DESC * TAIL[1], -160)]], "tail")


def hood():
    """e's FTM + BTM: one bow over the stem's top, from the middle on the back to the middle on the fore."""
    return Stroke([[K(-HOOD, M, 90), K(0, BODY, 0), K(HOOD, M, -90)]], "hood")


def ring():
    """o's four half branches: one closed round about the stem."""
    return Stroke([[K(0, BODY, 0), K(RING, M, -90), K(0, 0, 180), K(-RING, M, 90), K(0, BODY, 0)]], "ring")


def hook(scale=1.0):
    """The aspirate hook of f and th: one straight stroke of the nib from the stem's middle,
    rising forward across the arch or the cup; the majuscule's is the same at the cap's scale."""
    return Stroke([line(0, M * scale, HOOK[0] * HALF * scale, (BODY + HOOK[1]) * scale)], "hook", twist=HOOK_TWIST)


def ink_profile(contours, x_lo, x_hi, band=None, top=True):
    """The ink's top edge (or, with top False, its underside) at every fourth sheared x between
    x_lo and x_hi, as {x: y}. With `band`, only ink within that distance of the ink's peak
    counts, so a letter's foot never passes for its top."""
    peak = max(y for _, c in contours for _, y in c)
    out = {}
    for x in range(int(math.ceil(x_lo)), int(x_hi) + 1, 4):
        best = None
        for _, c in contours:
            for (ax, ay), (bx, by) in zip(c, c[1:] + c[:1]):
                if (ax <= x < bx) or (bx <= x < ax):
                    y = ay + (by - ay) * (x - ax) / (bx - ax)
                    if band is not None and y < peak - band:
                        continue
                    if best is None or (y > best if top else y < best):
                        best = y
        if best is not None:
            out[x] = best
    return out


def ink_top(strokes, x_lo, x_hi, band):
    """The lowest point of the ink's top edge between sheared x_lo and x_hi, counting only ink
    within `band` of the letter's peak."""
    polys = []
    for st in strokes:
        polys += st.polys()
    prof = ink_profile(union(polys), x_lo, x_hi, band)
    return min(prof.values()) if prof else None


def grave():
    """The catch: the glottal stop's mark, a grave: one short stroke of the nib falling from the
    upper left to the lower right, at the weight the nib gives that run, and short enough to
    read as a mark. Its head is the origin; a base letter names where it goes."""
    return Stroke([line(0, 0, GRAVE[0], GRAVE[1])], "grave")


def grave_anchor(strokes, tall, top, long_mark=None):
    """Where the catch's head goes on a base, in the base's own sheared frame before its
    shift. Centred over an x-height letter; at the upper right of the stem's top on a tall
    letter; to the right of the curl on a long vowel. In every case it clears the ink beneath
    it by MARK_GAP, found as the curl's seat is."""
    mark = union(grave().polys())
    mx = [x for _, c in mark for x, _ in c]
    my = [y for _, c in mark for _, y in c]
    m_lo, m_hi, m_bot, m_mid = min(mx), max(mx), min(my), (min(my) + max(my)) / 2
    polys = []
    for st in strokes:
        polys += st.polys()
    contours = union(polys)
    if long_mark is not None:
        lx = [x for poly in long_mark.polys() for x, _ in poly]
        ly = [y for poly in long_mark.polys() for _, y in poly]
        foot_x = max(lx) + MARK_GAP - m_lo
        foot_y = (min(ly) + max(ly)) / 2 - m_mid
    elif tall:
        foot_x = top * TAN + NIB_VEC[0] - HAIR_VEC[0] + MARK_GAP - m_lo
        foot_y = top - BESIDE
    else:
        xs = [x for _, c in contours for x, y in c if y >= 0.6 * BODY]
        foot_x = (min(xs) + max(xs)) / 2 - (m_lo + m_hi) / 2
        foot_y = BODY + MARK_GAP - m_bot
    lowest = ink_top(strokes, foot_x + m_lo, foot_x + m_hi, CAP / 2)
    if lowest is not None:
        foot_y = max(foot_y, lowest + MARK_GAP - m_bot)
    return foot_x, foot_y


def curl_at(y):
    w, h = CURL
    return Stroke([[K(-w / 2, y, CURL_FEET), K(0, y + h, 0), K(w / 2, y, -CURL_FEET)]], "curl", twist=TWIST)


def curl(strokes):
    """The long vowel's curl: a small arch of the nib centred on the stem and seated on the
    letter. It is lowered until, at the point where its underside and the letter's top edge
    come closest, it is sunk CURL_SINK into the ink, so the mark and the letter are one ink
    with no light between them."""
    polys = []
    for st in strokes:
        polys += st.polys()
    letter = union(polys)
    y = BODY
    for _ in range(3):
        c = union(curl_at(y).polys())
        xs = [x for _, cc in c for x, _ in cc]
        under = ink_profile(c, min(xs), max(xs), top=False)
        top = ink_profile(letter, min(xs), max(xs), CAP / 2)
        clearance = min(under[x] - top[x] for x in under if x in top)
        y -= clearance + CURL_SINK
    return curl_at(y)


# =============================================================================
# Letters
# =============================================================================

# Each stave's branches, by the Thuravark design: the side a branch leaves the stem on
# (F forward, B back), the level it leaves from and the level it ends at (T top, M middle,
# 0 foot). This is the Thuravark guard's table, row for row; j is the letter Tharavarkon
# adds for a sound the north never wrote, built as Pirzath's j is: a stem forking into two
# arms. y is Thuravark's glide (its j); Thuravark's y is the vowel i.
BRANCHES = {
    "a": "F0T", "b": "FT0 BT0 B0M", "d": "F0T B0T BTM", "e": "FTM BTM", "f": "FT0 BT0 FMT",
    "g": "FTM F0M BM0", "h": "BM0 FMT", "i": "", "j": "FMT BMT", "k": "FTM F0M", "l": "FM0",
    "m": "FT0 BM0", "n": "F0T BMT", "o": "FTM F0M BTM B0M", "p": "FT0 BT0", "r": "BTM B0M",
    "s": "FTM BM0", "t": "F0T B0T", "th": "F0T B0T FMT", "u": "B0T", "v": "FT0 BT0 B0M FMT",
    "w": "BMT", "y": "FMT", "z": "FT0 B0T",
}
# The digraph letters and q: each a Thuravark stave, or a family member built on one. On dh, kh,
# gh, sh and zh the FMT branch is the aspirate hook.
BRANCHES.update({
    "dh": "F0T B0T BTM FMT", "kh": "FTM F0M FMT", "gh": "FTM F0M BM0 FMT", "ng": "FTM F0M FMT FM0",
    "sh": "FTM BM0 FMT", "zh": "FT0 B0T FMT", "ts": "F0T B0T FTM BM0", "ch": "F0T B0T BTM FM0",
    "ny": "F0T BMT FMT", "q": "FTM F0M BMT",
})
LETTERS = list(BRANCHES)
ASPIRATES = {"f", "th", "dh", "kh", "gh", "sh", "zh"}   # the FMT branch is the hook here, not an arm
TALL = {"l", "h", "t", "th", "u"}  # the stem rises to ASC: its top is free of branches
DEEP = {"p", "f", "j", "s", "sh"}  # the stem falls to DESC: its foot is free of branches
TAILED = {"g", "gh"}               # BM0 is g's tail, carried below the line
VOWELS = "aeiou"


def minuscule(name, long=False):
    codes = BRANCHES[name].split()
    top = ASC if name in TALL else BODY
    bottom = DESC if name in DEEP else 0
    strokes = []
    aspirate = name in ASPIRATES
    if aspirate:
        codes = [c for c in codes if c != "FMT"]
    cs = set(codes)
    closed_f = {"FTM", "F0M"} <= cs
    closed_b = {"BTM", "B0M"} <= cs and "BT0" not in cs
    is_ring = closed_f and closed_b
    is_hood = cs == {"FTM", "BTM"}
    has_fcup = "F0T" in cs
    has_farch = "FT0" in cs
    # the stem, with its entry wedge where its top is free and its exit where its foot is
    wedge = not (is_ring or is_hood)
    exit_ = bottom == 0 and not (has_fcup or has_farch or closed_f or is_ring or "FM0" in cs)
    runs = [entry_run(top)] if wedge else []
    if has_fcup:
        # the forward cup continues the stem's foot: one stroke down and round and up
        runs += [line(0, top, 0, FOOT_R), [K(0, FOOT_R, -90)] + cup_knots("F")]
        strokes.append(Stroke(runs, "stem+cup F"))
    elif exit_:
        runs += [line(0, top, 0, FOOT_R)] + foot_turn(0)
        strokes.append(Stroke(runs, "stem"))
    else:
        runs += [line(0, top, 0, bottom)]
        strokes.append(Stroke(runs, "stem"))
    # the branches
    if is_ring:
        strokes.append(ring())
    elif is_hood:
        strokes.append(hood())
    else:
        if closed_f:
            strokes.append(bowl("F"))
        elif "FTM" in cs:
            strokes.append(shoulder("F"))
        elif "F0M" in cs:
            strokes.append(voicing("F"))
        if closed_b:
            strokes.append(bowl("B"))
        else:
            if "BTM" in cs:
                strokes.append(shoulder("B"))
            if "B0M" in cs:
                strokes.append(voicing())
        for c in codes:
            if c == "FT0":
                strokes.append(arch("F"))
            elif c == "BT0":
                strokes.append(arch("B"))
            elif c == "B0T":
                strokes.append(cup_back())
            # a middle branch on the side of a long branch runs on through it and out, as v's
            # arm runs through its arch
            elif c == "FMT":
                strokes.append(arm("F", through=bool({"FT0", "F0T"} & cs)))
            elif c == "BMT":
                strokes.append(arm("B", through=bool({"BT0", "B0T"} & cs)))
            elif c == "FM0":
                strokes.append(leg("F", through=bool({"FT0", "F0T"} & cs)))
            elif c == "BM0":
                strokes.append(tail() if name in TAILED else leg("B", through=bool({"BT0", "B0T"} & cs)))
    if aspirate:
        strokes.append(hook())
    if long:
        strokes.append(curl(strokes))
    return strokes


def majuscule(name, long=False):
    """The carved skeleton at the cap height: the stem and its straight branches, each
    turning off the stem over a short fillet; the hook of F and TH is the same stroke. A
    branch whose end is free and would stop square across the nib takes the final."""
    codes = BRANCHES[name].split()
    aspirate = name in ASPIRATES
    if aspirate:
        codes = [c for c in codes if c != "FMT"]
    level = {"T": CAP, "M": CAP / 2, "0": 0}
    # a branch leaving the stem's end begins a fillet's length beyond it, on the stem's line,
    # and the stem runs to that same point, so its cut and the branch's start are one nib
    top = CAP + (FILLET if any(c[1] == "T" for c in codes) else 0)
    bottom = -FILLET if any(c[1] == "0" for c in codes) else 0
    strokes = [Stroke([line(0, top, 0, bottom)], "stem")]
    ends = [c[0] + c[2] for c in codes]
    for c in codes:
        s = 1 if c[0] == "F" else -1
        y0, y1 = level[c[1]], level[c[2]]
        long_ = {c[1], c[2]} == {"T", "0"}
        run = (LONG_C if long_ else HALF_C) * CAP
        x1 = s * run
        if not long_ and any(o[0] == c[0] and {o[1], o[2]} == {"T", "0"} and o[2] == c[2] for o in codes):
            # a half branch ending where a long branch on its side ends would run into it: it runs
            # on along its own line, as v's arm runs through its arch, to the arm's height past the cap
            k = (abs(y1 - y0) + ARM_THROUGH[1]) / abs(y1 - y0)
            x1, y1 = x1 * k, y0 + (y1 - y0) * k
        d = math.degrees(math.atan2(y1 - y0, x1))
        # the pen comes along the stem toward the join and turns off onto the branch
        up = 1 if y1 > y0 else -1
        p0 = (0, y0 - up * FILLET)
        p1 = (FILLET * math.cos(math.radians(d)), y0 + FILLET * math.sin(math.radians(d)))
        runs = [[K(p0[0], p0[1], 90 * up), K(p1[0], p1[1], d)]]
        free = ends.count(c[0] + c[2]) == 1
        if free and up < 0 and across_nib(d):
            xe, ye = final_start(x1, y1, d)
            runs += [line(p1[0], p1[1], xe, ye)] + final(xe, ye, d)
        else:
            runs.append(line(p1[0], p1[1], x1, y1))
        strokes.append(Stroke(runs, "branch " + c))
    if aspirate:
        strokes.append(hook(CAP / BODY))
    if long:
        strokes.append(curl(strokes))
    return strokes


def numeral(n):
    """A stem at the cap height with up to four limbs, each a bow falling outward: 8 high on the
    fore side, 4 below it, 2 high on the back, 1 low on the back; nought is the stem with a closed
    ring at its foot, the pen's form of the carved row's rising pair."""
    strokes = [Stroke([line(0, CAP, 0, 0)], "stem")]
    if n == 0:
        w, h = NOUGHT[0] * CAP, NOUGHT[1] * CAP
        strokes.append(Stroke([[K(0, 2 * h, 0), K(w, h, -90), K(0, 0, 180), K(-w, h, 90), K(0, 2 * h, 0)]], "nought"))
    for value, (side, frac) in LIMBS.items():
        if n & value:
            s = 1 if side == "F" else -1
            y0 = frac * CAP
            strokes.append(Stroke([[K(0, y0, -(90 - s * 30)), K(s * LIMB * CAP, y0 - LIMB_DROP * CAP, -(90 - s * 70))]],
                                  f"limb {value}"))
    return strokes


def point_runs(x, y):
    """The sentence point: a punctus, the nib set down and drawn one nib's width straight down,
    which leaves a diamond; centred on (x, y)."""
    return line(x, y + DOT_RUN / 2, x, y - DOT_RUN / 2)


def mark_glyph(name):
    if name == "point":
        return [Stroke([point_runs(0, M)], "point")]
    if name == ".notdef":
        return [Stroke([line(0, BODY, 0, 0)], "stem"), Stroke([point_runs(-130, M)], "point"),
                Stroke([point_runs(120, M)], "point")]
    raise KeyError(name)


class Glyph:
    """One drawing: its strokes, its outline as contours (sheared, shifted so its ink begins at
    the bearing), its advance, and where its stem stands."""

    def __init__(self, name, strokes, adv=None, mark=False, anchor=None):
        self.name = name
        self.strokes = strokes
        polys = []
        for st in strokes:
            polys += st.polys()
        self.contours = union(polys) if polys else []
        if self.contours and not mark:
            xs = [x for _, c in self.contours for x, _ in c]
            lo, hi = min(xs), max(xs)
            self.shift = BEAR - lo
            self.adv = hi - lo + 2 * BEAR
        else:
            # a mark keeps its own origin and takes no room: its base says where it goes
            self.shift = 0
            self.adv = adv or 0
        self.contours = [(a, [(x + self.shift, y) for x, y in c]) for a, c in self.contours]
        self.stem_x = self.shift  # the stem's foot, sheared x = 0, after the shift
        if adv is not None:
            self.adv = adv
        # where the catch's foot goes on this base, in the shifted frame
        self.anchor = (anchor[0] + self.shift, anchor[1]) if anchor else None


_CACHE = {}


def glyph(name):
    if name in _CACHE:
        return _CACHE[name]
    if name == "space":
        g = Glyph(name, [], adv=SPACE)
    elif name == "grave":
        g = Glyph(name, [grave()], adv=0, mark=True)
    elif name.startswith("num."):
        g = Glyph(name, numeral(int(name[4:])))
    elif name in ("point", ".notdef"):
        g = Glyph(name, mark_glyph(name))
    else:
        base, long = (name[:-5], True) if name.endswith(".long") else (name, False)
        if base in LOWER_OF:
            strokes, tall = majuscule(LOWER_OF[base], long), True
        else:
            strokes, tall = minuscule(base, long), base in TALL
        stem = next(st for st in strokes if st.kind.startswith("stem"))
        top = max(r[1][1] for r in stem.runs if isinstance(r, tuple) and r[0] == "L")
        g = Glyph(name, strokes, anchor=grave_anchor(strokes, tall, top, strokes[-1] if long else None))
    _CACHE[name] = g
    return g


def _upper(n):
    head, dot, rest = n.partition(".")
    return head.upper() + dot + rest


MAJ = {n: _upper(n) for n in BRANCHES}
LOWER_OF = {u: n for n, u in MAJ.items()}
ALPHABET = [(MAJ[n], n) for n in LETTERS]
LONGS = [(MAJ[v] + ".long", v + ".long") for v in VOWELS]
NUMERALS = [f"num.{i}" for i in range(10)]
MARKS = ["point", "grave", ".notdef"]
EVERY = [g for pair in ALPHABET + LONGS for g in pair] + NUMERALS + MARKS
BASES = set(g for pair in ALPHABET + LONGS for g in pair)   # the letters a catch can sit on


# =============================================================================
# Typing: Vylari text to glyph names
# =============================================================================

ACUTE = {"á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u", "Á": "A", "É": "E", "Í": "I", "Ó": "O", "Ú": "U"}
