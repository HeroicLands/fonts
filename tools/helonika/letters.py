# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""The Helónika book hand's signs, built from the stroke inventory.

    import letters as L

    L.SIGNS["th"]()              # the minuscule th: a list of Shapes, its ink on the line
    L.glyph("th")                # (outline, left ink, right ink), drawn once and cached
    L.spell("Sothira.")          # ['S', 'o', 'th', 'i', 'r', 'a', 'raisedDot']
    L.setting(L.spell("kosamir"))  # [(outline, x offset)], advance

Every sign is named as the font names its glyph: the capitals ``A`` … ``Z``, ``TH``,
``E.long`` and ``O.long`` (the letters _ē_ and _ō_), the additions ``KH`` and
``ZH``, and the long vowels ``A.macron``, ``I.macron`` and ``U.macron``; the
minuscules by the same names in lower case; the digits ``num.0`` … ``num.9``; and
``raisedDot``, ``registerMark`` and ``accent``.

A capital is the inscription, built from straight strokes and rounds at
``S.CAP``. The minuscules are a round book hand of their own on the body ``S.X``:
bowls, arches, cups and hooked stems (the ``hooked`` and ``swing`` strokes), free
ends turned into flourishes, and every free bar end curled up. They need not follow
their capitals, and only the six echoes, _o th ō p d l_, resemble Greek letters.

``spell`` is the Helonic spelling the specimens are set with; the encodings in
thalorna are what a text is written through.
"""

from __future__ import annotations

import math

import strokes as S

C, X, ASC, DESC = S.CAP, S.X, S.ASC, S.DESC
W, HH = S.HALF_W, S.HALF_H


# -- parts -------------------------------------------------------------------------------------


def seg(x0, y0, x1, y1):
    """A straight reed stroke between two centreline points: the ``diagonal`` stroke
    placed by its ends rather than by its box."""
    t = S.Track(x0, y0).line(x1, y1)
    return S.Shape([t], (x0, y0), (x1, y1))


def stem(x, top, foot=0.0):
    return S.s_stem(x, 0, top=top, foot=foot)


def hbar(x0, x1, y, left=False, right=False, drop=-1):
    """A level hairline whose ink runs from ``x0`` to ``x1`` with its centre at ``y``,
    a knob at either end on request, hanging (``drop`` -1) or standing (1)."""
    t = S.Track(x0 + W, y).line(x1 - W, y)
    out = [t]
    if left:
        out += S.s_knob(x0 + S.KNOB_IN, y, drop=drop, side=-1).tracks
    if right:
        out += S.s_knob(x1 - S.KNOB_IN, y, drop=drop, side=1).tracks
    return S.Shape(out, (x0, y), (x1, y))


def back_crescent(x, y, w, h, open=110.0):
    """A round left open on the left: the crescent turned to face back, a knob at
    each end."""
    sh = S.s_arc(x, y, w, h, 180 + open / 2, 360 - open)
    t = sh.tracks[0]
    lower = S.s_knob(*t.samples[0][:2], drop=-1, side=-1)
    upper = S.s_knob(*t.end, drop=1, side=-1)
    return [sh, lower, upper]


def wave_arc(x, y, w, h, start, sweep):
    return S.s_arc(x, y, w, h, start, sweep)


# -- the capitals -------------------------------------------------------------------------------
#
# The capitals are the inscription: straight strokes and rounds at the cap height
# ``C``. Each builder returns Shapes with the ink standing on the line from about
# x = 0.


def _a():
    """_A_: a tripod, two strokes meeting at the head with a stem let fall from the
    meeting point to the line."""
    w = 0.80 * C
    apex = (w / 2, C - HH)
    return [seg(0.6 * W, HH, *apex), seg(*apex, w - 0.6 * W, HH), stem(w / 2, C - HH)]


def _b():
    """_B_: a stem with a bowl at its head on the left and a bowl at its foot on the
    right."""
    r1, r2 = 0.34 * C, 0.38 * C
    xs = r1
    return [stem(xs, C), S.s_lobe(xs, 0, top=C, bottom=0.50 * C, w=r1, side=-1),
            S.s_lobe(xs, 0, top=0.52 * C, bottom=0, w=r2, side=1)]


def _e():
    """_E_: the round open on the left."""
    return back_crescent(0, 0, 0.74 * C, C)


def _ee():
    """_Ē_: the back crescent with a bar from its open side to its back."""
    w = 0.76 * C
    return back_crescent(0, 0, w, C) + [hbar(0.16 * w, w - W, C / 2, left=True)]


def _f():
    """_F_: half a triangle, a stroke rising from the line to the head of a stem."""
    w = 0.50 * C
    xs = w - W
    return [stem(xs, C), seg(0.6 * W, HH, xs, C - HH)]


def _k():
    """_K_: a stem met at its middle by two strokes from the left, one falling from
    the head, one rising from the foot."""
    reach = 0.46 * C
    xs = reach + 0.6 * W
    return [stem(xs, C), seg(xs - reach, C - HH, xs, 0.48 * C), seg(xs, 0.48 * C, xs - reach, HH)]


def _g():
    """_G_: the _K_ with its two strokes rounded into a bowl closed against the stem."""
    r = 0.56 * C
    xs = r
    return [stem(xs, C), S.s_lobe(xs, 0, top=C, bottom=0, w=r, side=-1)]


def _h():
    """_H_: small and plain, a stem with a bar on the right at its middle."""
    xs = W
    return [stem(xs, C), hbar(xs, xs + 0.40 * C, 0.50 * C, right=True)]


def _i():
    """_I_: a stem standing on a short base."""
    xs = 0.20 * C + W
    return [stem(xs, C), hbar(xs - 0.20 * C - W, xs + 0.20 * C + W, HH, left=True, right=True, drop=1)]


def _j():
    """_J_: the gate with its left leg splayed outward."""
    w = 0.72 * C
    o = 20
    xr = w - W - o
    beam = S.s_beam(o + 0.20 * w, 0, w=w - 2 * o - 0.20 * w, at=C, overhang=o)
    return [beam, seg(o + 0.20 * w + 0.6 * W, C - 2 * HH, 0.6 * W, HH), stem(xr, C - 2 * HH)]


def _kh():
    """_KH_: the _K_ with a bar struck through its stem above the meeting point."""
    xs = 0.46 * C + 0.6 * W
    return _k() + [hbar(xs - 0.12 * C, xs + 0.20 * C, 0.82 * C, left=True, right=True)]


def _m():
    """_M_: the gate on three legs."""
    w = 0.86 * C
    o = 20
    top = C - 2 * HH
    return [S.s_beam(o, 0, w=w - 2 * o, at=C, overhang=o), stem(W + o, top), stem(w / 2, top), stem(w - W - o, top)]


def _n():
    """_N_: the gate on two legs splayed outward."""
    w = 0.80 * C
    o = 20
    sp = 0.16 * w
    return [S.s_beam(o + sp, 0, w=w - 2 * o - 2 * sp, at=C, overhang=o),
            seg(o + sp + 0.6 * W, C - 2 * HH, 0.6 * W, HH), seg(w - o - sp - 0.6 * W, C - 2 * HH, w - 0.6 * W, HH)]


def _r():
    """_R_: a stem with a bowl at its head on the left."""
    r = 0.38 * C
    xs = r
    return [stem(xs, C), S.s_lobe(xs, 0, top=C, bottom=0.46 * C, w=r, side=-1)]


def _s():
    """_S_: the round struck through by a stroke falling from its upper left to its
    lower right."""
    w = 0.82 * C
    rx, ry = w / 2 - W, C / 2 - HH + S.OVER
    a = S.on_ellipse(w / 2, C / 2, rx, ry, 135)
    b = S.on_ellipse(w / 2, C / 2, rx, ry, -45)
    return [S.s_round(0, 0, w=w, h=C), seg(*a, *b)]


def _t():
    """_T_: a stem crossed high by a bar."""
    xs = 0.26 * C + W
    return [stem(xs, C), hbar(xs - 0.26 * C - W, xs + 0.26 * C + W, 0.66 * C, left=True, right=True)]


def _u():
    """_U_: the _Ō_ turned over: a round open at its head, standing on the line, each
    open end finished with a short level foot turned outward."""
    w = 0.80 * C
    hh = 0.97 * C
    rx, ry = w / 2 - W, hh / 2 - HH + S.OVER
    cx, cy = 60 + w / 2, hh / 2
    open_ = 86
    left = S.Track(*S.on_ellipse(cx, cy, rx, ry, 265)).ellipse(cx, cy, rx, ry, 265, 90 + open_ / 2)
    right = S.Track(*S.on_ellipse(cx, cy, rx, ry, 275)).ellipse(cx, cy, rx, ry, 275, 360 + 90 - open_ / 2)
    (lx, _), (rx2, _) = left.end, right.end
    top = C - HH
    return [S.Shape([left], left.samples[0][:2], left.end), S.Shape([right], right.samples[0][:2], right.end),
            hbar(0, lx + 30 + W, top), hbar(rx2 - 30 - W, w + 120, top),
            S.s_knob(S.KNOB_IN, top, drop=-1, side=-1), S.s_knob(w + 120 - S.KNOB_IN, top, drop=-1, side=1)]


def _v():
    """_V_: a round on the line carrying a stem up to the cap height."""
    w = 0.62 * C
    return [S.s_round(0, 0, w=w, h=0.60 * C), stem(w / 2, C, foot=0.60 * C - 2 * HH)]


def _z():
    """_Z_: a beam, a stroke falling from its right end, and a bowl open on the left
    below."""
    w = 0.62 * C
    lo = S.s_arc(0, 0, w, 0.56 * C, 100, -270)
    (sx, sy) = lo.tracks[0].samples[0][:2]
    return [hbar(0.04 * w, 0.92 * w, C - HH, left=True), seg(0.92 * w - 0.6 * W, C - HH, sx, sy), lo,
            S.s_knob(*lo.tracks[0].end, drop=-1, side=-1)]


def _zh():
    """_ZH_: the _Z_ with a bar struck through it."""
    w = 0.62 * C
    return _z() + [hbar(0.06 * w, 0.62 * w, 0.62 * C, left=True)]


# -- the capital echoes ------------------------------------------------------------------------


def _o():
    """_O_: the round."""
    return [S.s_round(0, 0, w=0.95 * C, h=C)]


def _th():
    """_TH_: the round barred across."""
    w = 0.95 * C
    return [S.s_round(0, 0, w=w, h=C), hbar(0.22 * w, 0.78 * w, 0.5 * C, left=True, right=True)]


def _oo():
    """_Ō_: the round open at its foot on two feet."""
    w = 0.92 * C
    hood = S.s_hood(60, 0, w=w, h=0.97 * C, open=86)
    (lx, _), (rx, _) = hood.tracks[0].end, hood.tracks[1].end
    return [hood, hbar(0, lx + 30 + W, HH), hbar(rx - 30 - W, w + 120, HH),
            S.s_knob(S.KNOB_IN, HH, drop=1, side=-1), S.s_knob(w + 120 - S.KNOB_IN, HH, drop=1, side=1)]


def _p():
    """_P_: the gate."""
    w = 0.74 * C
    return [stem(W + 30, C - 2 * HH), stem(w - W - 30, C - 2 * HH), S.s_beam(30, 0, w=w - 60, at=C, overhang=30)]


def _d():
    """_D_: the triangle on a base."""
    w = 0.78 * C
    return [seg(0.6 * W, HH, w / 2, C - HH), seg(w / 2, C - HH, w - 0.6 * W, HH), hbar(-24, w + 24, HH)]


def _l():
    """_L_: two strokes meeting at the head, the short one stopping inside the long."""
    w = 0.74 * C
    right = S.s_diagonal(w / 2 - 40, 0, w=w / 2 + 40, h=C, rise=-1)
    (ax, ay), (bx, by) = right.tracks[0].samples[0][:2], right.tracks[0].end
    tx, ty = ax + (bx - ax) * 0.12, ay + (by - ay) * 0.12
    return [seg(0.6 * W, HH, tx, ty), right]


# -- the long vowels ---------------------------------------------------------------------------


def _long(build):
    """A capital vowel with the length bar over it, centred on its ink."""
    parts = build()
    xs = [x for sh in parts for t in sh.tracks for x, *_ in t.samples]
    return parts + [S.s_length((min(xs) + max(xs)) / 2, 0, w=190, at=C + 40)]


# -- digits ------------------------------------------------------------------------------------


def _n0():
    """0: a diamond."""
    w = 0.60 * C
    top, mid, bot = (w / 2, C - HH), (0.6 * W, C / 2), (w / 2, HH)
    right = (w - 0.6 * W, C / 2)
    return [seg(*top, *mid), seg(*mid, *bot), seg(*bot, *right), seg(*right, *top)]


def _n1():
    """1: one rising stroke on a short foot."""
    return [seg(0.6 * W + 20, HH, 0.36 * C, C - HH), hbar(-10, 0.6 * W + 20 + 0.16 * C, HH, right=True, drop=1)]


def _n2():
    """2: a bracket open on the left."""
    w = 0.50 * C
    return [hbar(0, w, C - HH, left=True), stem(w - W, C), hbar(0, w, HH, left=True, drop=1)]


def _n3():
    """3: an angle: a base and a stroke rising from its left end."""
    w = 0.56 * C
    return [hbar(0, w, HH, right=True, drop=1), seg(0.6 * W, HH, w - 0.6 * W, C - HH)]


def _n4():
    """4: a point turned to the left."""
    w = 0.50 * C
    return [seg(w - 0.6 * W, C - HH, 0.6 * W, C / 2), seg(0.6 * W, C / 2, w - 0.6 * W, HH)]


def _n5():
    """5: a bracket open on the right, the 2 turned to face forward."""
    w = 0.50 * C
    return [hbar(0, w, C - HH, right=True), stem(W, C), hbar(0, w, HH, right=True, drop=1)]


def _n6():
    """6: a diamond carried on a short stem."""
    w = 0.56 * C
    y0 = 0.36 * C
    top, mid, bot = (w / 2, C - HH), (0.6 * W, (C + y0) / 2), (w / 2, y0)
    right = (w - 0.6 * W, (C + y0) / 2)
    return [seg(*top, *mid), seg(*mid, *bot), seg(*bot, *right), seg(*right, *top), stem(w / 2, y0 + HH)]


def _n7():
    """7: two rising strokes side by side."""
    d = 0.20 * C
    return [seg(0.6 * W, HH, 0.30 * C, C - HH), seg(0.6 * W + d, HH, 0.30 * C + d, C - HH)]


def _n8():
    """8: two rounds side by side at the middle of the height."""
    w, h = 0.38 * C, 0.44 * C
    y = (C - h) / 2
    return [S.s_round(0, y, w=w, h=h), S.s_round(w - 2 * W, y, w=w, h=h)]


def _n9():
    """9: a point turned to the right, the 4 turned to face forward."""
    w = 0.50 * C
    return [seg(0.6 * W, C - HH, w - 0.6 * W, C / 2), seg(w - 0.6 * W, C / 2, 0.6 * W, HH)]


# -- points and marks --------------------------------------------------------------------------


def _raised_dot():
    """The raised dot: the sentence's end."""
    return [S.s_dot(W, 0)]


def _register_mark():
    """The register-mark: a short wave at body height, over and under, marking a turn."""
    w, h = 0.52 * X, 0.50 * X
    y = 0.22 * X
    rx = w / 2 - W
    a = wave_arc(0, y, w, h, 180, -180)
    b = wave_arc(2 * rx, y, w, h, 180, 180)
    return [a, b, S.s_knob(*a.tracks[0].samples[0][:2], drop=-1, side=-1),
            S.s_knob(*b.tracks[0].end, drop=1, side=1)]


def _accent():
    """The accent, standing alone: over a minuscule it is set by the font."""
    return [S.s_accent(0.6 * W, 0)]


# -- the minuscules ----------------------------------------------------------------------------
#
# The minuscules are the pen's own round letters, not the capitals on the body: a
# stem is a ``hooked`` curve, a gate a bowed beam on curved legs, a free end a
# flourish, and a bar's free ends curl up. Each builder returns Shapes with the ink
# standing on the line from about x = 0.

R = 46.0  # the radius of a minuscule's flourish
MOVER = 6.0  # how far a minuscule round passes the line and the body: less than a capital's, on a smaller letter


def sw(p0, p1, bow=0.0, head=0.0, tail=0.0, r=R):
    """A ``swing`` from point to point."""
    return S.s_swing(p0[0], p0[1], p1[0] - p0[0], p1[1] - p0[1], bow, head, tail, r)


def end_curl(shape, turn, r=R, at_end=True):
    """A flourish carried on from the end (or, ``at_end`` False, the start) of a
    shape's first track."""
    t = shape.tracks[0]
    x, y = t.samples[-1][:2] if at_end else t.samples[0][:2]
    return S.s_flourish(x, y, S.heading(t, at_end), turn, r)


def bare(shape):
    """A shape with its knobs left off: its first track alone."""
    return S.Shape([shape.tracks[0]], shape.entry, shape.exit)


def m_a():
    """_a_: a round bowl standing against a stem on its left, the stem set going by an
    entry and turned forward at its foot."""
    xs = W + 40
    w = 0.72 * X
    return [S.s_round(xs - 0.4 * W, 0, w=w, h=X, over=MOVER), S.s_hooked(xs, 0, top=X, bow=0.0, entry=56, tail=1, r=44)]


def m_b():
    """_b_: a bowed stem with a small bowl on the left at its head and a larger bowl on
    the right at its foot."""
    r1, r2 = 0.34 * X, 0.38 * X
    xs = r1
    return [sw((xs, X - HH), (xs, HH), 0.072), S.s_lobe(xs, 0, top=X, bottom=0.50 * X, w=r1, side=-1),
            S.s_lobe(xs, 0, top=0.52 * X, bottom=0, w=r2, side=1)]


def m_d():
    """_d_: the round with its neck finished in a flourish turned down over the
    round."""
    w = 0.9 * X
    neck = bare(S.s_neck(w * 0.42, 0, h=ASC, base=0.86 * X - HH, lean=0.5, curl=0.7))
    return [S.s_round(0, 0, w=w, h=0.86 * X, over=MOVER), neck, end_curl(neck, -130, r=38)]


def _back(w, h, y=0.0, open=110.0):
    arc = S.s_arc(0, y, w, h, 180 + open / 2, 360 - open, over=MOVER)
    return [arc, end_curl(arc, 120, r=38), end_curl(arc, -120, r=38, at_end=False)]


def m_e():
    """_e_: the round open on the left, each end turned in on a flourish."""
    return _back(0.80 * X, X)


def m_ee():
    """_ē_: the _e_ with a bowed bar to its back, its free end curled up."""
    w = 0.82 * X
    return _back(w, X) + [sw((0.18 * w, X / 2), (w - W, X / 2), 0.09, head=-120, r=36)]


def m_f():
    """_f_: a stem falling from the body's head to the descender, its head hooked
    forward and its foot turned back, crossed in the body by a bar curled up at both
    ends."""
    xs = 0.30 * X + W
    return [sw((xs, X - HH), (xs, DESC + HH + 20), 0.08, head=-150, tail=-120, r=50),
            sw((xs - 0.30 * X, 0.62 * X), (xs + 0.30 * X, 0.62 * X), 0.10, head=-120, tail=120, r=34)]


def m_g():
    """_g_: the bowl closed against a stem that falls to the descender and hooks
    back."""
    r = 0.64 * X
    xs = r
    return [sw((xs, X - HH), (xs, DESC + HH + 20), 0.054, tail=-130), S.s_lobe(xs, 0, top=X, bottom=0, w=r, side=-1)]


def m_h():
    """_h_: small and plain, a bowed stem turned forward at its foot, with an arm
    springing from its middle and curling up."""
    xs = W + 30
    return [S.s_hooked(xs, 0, top=X, bow=0.08, entry=50, tail=1, r=44),
            sw((xs, 0.46 * X), (xs + 0.44 * X, 0.60 * X), 0.14, tail=120, r=36)]


def m_i():
    """_i_: a short stem set going by an entry from the left and turned back at its
    foot."""
    return [S.s_hooked(W + 80, 0, top=X, bow=0.07, entry=60, tail=-1, r=48)]


def m_j():
    """_j_: a stem set going by an entry, falling to the descender and turning back
    into a wide tail."""
    xs = W + 160
    return [S.s_hooked(xs, 0, top=X, foot=DESC + 20, bow=0.08, entry=60, tail=-1, r=72)]


def m_k():
    """_k_: an ascender set going by an entry and turned forward at its foot, met at
    the body's middle by two curves from the left whose free ends curl."""
    reach = 0.48 * X
    xs = reach + W + 20
    mid = (xs, 0.48 * X)
    return [S.s_hooked(xs, 0, top=ASC, bow=0.06, entry=50, tail=1, r=44),
            sw((xs - reach, X - HH), mid, -0.18, head=120, r=36),
            sw(mid, (xs - reach, HH + 10), -0.18, tail=-120, r=36)]


def m_kh():
    """_kh_: the _k_ with a bowed bar through its ascender, curled up at both ends."""
    reach = 0.48 * X
    xs = reach + W + 20
    return m_k() + [sw((xs - 0.26 * X, ASC - 70), (xs + 0.22 * X, ASC - 70), 0.10, head=-120, tail=120, r=32)]


def m_l():
    """_l_: the long stroke swung from the ascender to the line, hooked at its head
    and kicked forward at its foot, the short leg swung out to the left."""
    w = 0.78 * X
    long_ = sw((0.6 * W + 30, ASC - HH), (w - 0.6 * W, HH + 10), -0.072, head=120, tail=100, r=38)
    return [long_, sw((0.50 * w, 0.52 * ASC), (0.6 * W, HH + 10), -0.09, tail=-110, r=36)]


def m_m():
    """_m_: a hooked stem set going by an entry, with two humps arching from it and
    from each other, each leg's foot turned forward."""
    d = 0.40 * X
    x0 = W + 50
    parts = [S.s_hooked(x0, 0, top=X, bow=0.04, entry=50, tail=1, r=34)]
    for k in range(2):
        hump = S.s_arch(x0 + k * d, 0, w=d + 2 * W, h=X, spring=0.66)
        parts += [hump, end_curl(hump, 110, r=34)]
    return parts


def m_n():
    """_n_: a bell: one arch from the line over the body and back to the line, each
    foot flicked outward."""
    w = 0.80 * X
    rx, ry = w / 2 - W, X - 2 * HH + MOVER
    cx, cy = 40 + w / 2, HH
    t = S.Track(*S.on_ellipse(cx, cy, rx, ry, 180)).ellipse(cx, cy, rx, ry, 180, 0)
    arch = S.Shape([t], t.samples[0][:2], t.end)
    return [arch, end_curl(arch, -100, r=40, at_end=False), end_curl(arch, 100, r=40)]


def m_o():
    return [S.s_round(0, 0, w=X, h=X, over=MOVER)]


def m_oo():
    """_ō_: two cups round at the foot, sharing a shorter middle, their outer heads
    turned inward."""
    w, h = 0.56 * X, X
    rx, ry = w / 2 - W, 0.52 * X - HH
    cy = ry + HH - MOVER
    left = S.Track(*S.on_ellipse(w / 2, cy, rx, ry, 140)).ellipse(w / 2, cy, rx, ry, 140, 360)
    c2 = w / 2 + 2 * rx
    right = S.Track(*S.on_ellipse(c2, cy, rx, ry, 180)).ellipse(c2, cy, rx, ry, 180, 400)
    a = S.Shape([left], left.samples[0][:2], left.end)
    b = S.Shape([right], right.samples[0][:2], right.end)
    return [a, b, end_curl(a, 120, r=34, at_end=False), end_curl(b, 120, r=34)]


def m_p():
    """_p_: the gate rounded: a hump arching between two legs, its head carried past
    the left leg as an entry curling up and past the right shoulder in a curl turned
    up, the left foot turned back and the right turned outward."""
    d = 0.46 * X
    x0 = W + 90
    hump = S.s_arch(x0, 0, w=d + 2 * W, h=X, spring=0.70)
    xr = x0 + d
    return [S.s_hooked(x0, 0, top=X, bow=-0.05, entry=90, tail=-1, r=40), hump, end_curl(hump, 110, r=40),
            sw((xr - 0.10 * X, X - HH - 4), (xr + 0.20 * X, X - HH + 10), 0.06, tail=120, r=30)]


def m_r():
    """_r_: a bowed stem with its bowl at the head on the left, its foot turned into a
    tail."""
    r = 0.44 * X
    xs = r
    return [S.s_hooked(xs, 0, top=X, bow=0.08, entry=0, tail=1, r=48),
            S.s_lobe(xs, 0, top=X, bottom=0.44 * X, w=r, side=-1)]


def m_s():
    """_s_: the round struck through by a swung stroke."""
    w = 0.90 * X
    rx, ry = w / 2 - W, X / 2 - HH + MOVER
    a = S.on_ellipse(w / 2, X / 2, rx, ry, 135)
    b = S.on_ellipse(w / 2, X / 2, rx, ry, -45)
    return [S.s_round(0, 0, w=w, h=X, over=MOVER), sw(a, b, 0.08)]


def m_t():
    """_t_: an ascender set going by an entry and turned forward at its foot, crossed
    at the body's head by a bowed bar curled up at both ends."""
    xs = 0.30 * X + W
    return [S.s_hooked(xs, 0, top=ASC, bow=0.08, entry=50, tail=1, r=50),
            sw((xs - 0.30 * X - W, X - HH), (xs + 0.30 * X + W, X - HH), 0.10, head=-120, tail=120, r=34)]


def m_th():
    w = 0.62 * X
    return [S.s_round(0, 0, w=w, h=ASC, over=MOVER), sw((W, 0.48 * ASC), (w - W, 0.48 * ASC), 0.054)]


def m_u():
    """_u_: a single round cup open at its head, like an omega turned over, each rim
    tip flicked outward and curled down in a short turn of the reed. The tips turn
    down where the hand's bars turn up."""
    w, h = 0.80 * X, 0.92 * X
    x0 = 0.12 * X
    rx, ry = w / 2 - W, h / 2 - HH + MOVER
    cx, cy = x0 + w / 2, h / 2 - MOVER
    cup = S.Track(*S.on_ellipse(cx, cy, rx, ry, 132)).ellipse(cx, cy, rx, ry, 132, 408)
    face = S.Shape([cup], cup.samples[0][:2], cup.end)
    parts = [face, end_curl(face, 215, r=36, at_end=False), end_curl(face, -215, r=36)]
    # The curled tips stand above the rim; the whole letter is fitted to the body, its
    # bowl and its tips passing the line and the x-height by a round's overshoot.
    hh = S._half(S.REED_MIN)[1]
    ys = [y for sh in parts for t in sh.tracks for _, y, *_ in t.samples]
    lo, hi = min(ys) - hh, max(ys) + hh
    k = (X + 2 * MOVER) / (hi - lo)
    for sh in parts:
        for t in sh.tracks:
            t.samples = [(x, (y - lo) * k - MOVER, a, e) for x, y, a, e in t.samples]
    return parts


def m_v():
    """_v_: two closed rounds side by side, sharing their meeting side."""
    w, h = 0.58 * X, 0.86 * X
    return [S.s_round(0, 0, w=w, h=h, over=MOVER), S.s_round(w - 2 * W, 0, w=w, h=h, over=MOVER)]


def m_z():
    """_z_: two bowls open on the left, the lower hanging to the descender, each free
    end turned on a flourish."""
    w = 0.70 * X
    up = S.s_arc(0.10 * w, 0.46 * X, 0.82 * w, 0.54 * X, 160, -250, over=MOVER)
    lo = S.s_arc(0, DESC, w, 0.50 * X - DESC, 90, -260, over=MOVER)
    return [up, lo, end_curl(up, 120, r=34, at_end=False), end_curl(lo, -120, r=36)]


def m_zh():
    """_zh_: the _z_ with a bowed bar through where its bowls meet, curled at its free
    end."""
    w = 0.70 * X
    return m_z() + [sw((-0.10 * w, 0.48 * X), (0.62 * w, 0.48 * X), 0.09, head=-120, r=32)]


def _long_min(build):
    parts = build()
    xs = [x for sh in parts for t in sh.tracks for x, *_ in t.samples]
    return parts + [S.s_length((min(xs) + max(xs)) / 2, 0, w=150, at=X + 60)]


MIN = {"a": m_a, "b": m_b, "d": m_d, "e": m_e, "e.long": m_ee, "f": m_f, "g": m_g, "h": m_h, "i": m_i, "j": m_j,
       "k": m_k, "kh": m_kh, "l": m_l, "m": m_m, "n": m_n, "o": m_o, "o.long": m_oo, "p": m_p, "r": m_r, "s": m_s,
       "t": m_t, "th": m_th, "u": m_u, "v": m_v, "z": m_z, "zh": m_zh,
       "a.macron": lambda: _long_min(m_a), "i.macron": lambda: _long_min(m_i), "u.macron": lambda: _long_min(m_u)}


# -- the table ---------------------------------------------------------------------------------


LETTERS = [  # (capital, minuscule, the capital's builder): the minuscules are in MIN
    ("A", "a", _a), ("B", "b", _b), ("D", "d", _d), ("E", "e", _e), ("E.long", "e.long", _ee),
    ("F", "f", _f), ("G", "g", _g), ("H", "h", _h), ("I", "i", _i), ("J", "j", _j),
    ("K", "k", _k), ("L", "l", _l), ("M", "m", _m), ("N", "n", _n), ("O", "o", _o),
    ("O.long", "o.long", _oo), ("P", "p", _p), ("R", "r", _r), ("S", "s", _s), ("T", "t", _t),
    ("TH", "th", _th), ("U", "u", _u), ("V", "v", _v), ("Z", "z", _z),
]
ADDITIONS = [("KH", "kh", _kh), ("ZH", "zh", _zh)]
LONG = [("A.macron", "a.macron", _a), ("I.macron", "i.macron", _i), ("U.macron", "u.macron", _u)]
ECHOES = {"O", "TH", "O.long", "P", "D", "L"}

SIGNS: dict = {}
for cap, small, build in LETTERS + ADDITIONS:
    SIGNS[cap] = build
    SIGNS[small] = MIN[small]
for cap, small, build in LONG:
    SIGNS[cap] = (lambda b=build: _long(b))
    SIGNS[small] = MIN[small]
DIGITS = [f"num.{i}" for i in range(10)]
for i, build in enumerate([_n0, _n1, _n2, _n3, _n4, _n5, _n6, _n7, _n8, _n9]):
    SIGNS[f"num.{i}"] = build
SIGNS["raisedDot"] = _raised_dot
SIGNS["registerMark"] = _register_mark
SIGNS["accent"] = _accent

CAPITALS = [c for c, _, _ in LETTERS + ADDITIONS + LONG]
MINUSCULES = [s for _, s, _ in LETTERS + ADDITIONS + LONG]
POINTS = ["raisedDot", "registerMark", "accent"]

# How each sign is labelled in roman.
ROMAN = {"E.long": "Ē", "O.long": "Ō", "e.long": "ē", "o.long": "ō", "A.macron": "Ā", "I.macron": "Ī",
         "U.macron": "Ū", "a.macron": "ā", "i.macron": "ī", "u.macron": "ū", "raisedDot": "·",
         "registerMark": "§", "accent": "´", "TH": "TH", "KH": "KH", "ZH": "ZH"}
ROMAN.update({d: d[-1] for d in DIGITS})


def roman(name):
    return ROMAN.get(name, name)


# -- drawing and setting -----------------------------------------------------------------------


def tracks(name):
    return [t for sh in SIGNS[name]() for t in sh.tracks]


def ink_x(trs):
    xs = [x for t in trs for x, *_ in t.samples]
    return min(xs) - W, max(xs) + W


_OUTLINES: dict = {}


def glyph(name):
    """One sign's outline and ink extent, drawn once and reused wherever it is set."""
    if name not in _OUTLINES:
        trs = tracks(name)
        reed = S.REED_MIN if name in MIN or name in POINTS else S.REED
        _OUTLINES[name] = (S.outline(trs, reed), *ink_x(trs))
    return _OUTLINES[name]


def setting(names):
    """Lay ``names`` side by side with ``S.BEARING`` either side of each one's ink;
    ``" "`` is the word space. The accent takes no room: it is set over the sign
    before it. Returns [(outline, x offset)] and the advance."""
    out, x, last = [], 0.0, None
    for n in names:
        if n == " ":
            x += S.SPACE
            last = None
            continue
        path, lo, hi = glyph(n)
        if n == "accent" and last is not None:
            plo, phi, px = last
            mid = px + (plo + phi) / 2
            out.append((path, mid - (lo + hi) / 2 + 20))
            continue
        dx = x + S.BEARING - lo
        out.append((path, dx))
        last = (lo, hi, dx)
        x += (hi - lo) + 2 * S.BEARING
    return out, x


# -- the Helonic spelling the specimens use -----------------------------------------------------

_PLAIN = str.maketrans("áéíóúÁÉÍÓÚëïöüËÏÖÜ", "aeiouAEIOUeiouEIOU")
_PAIRS = {"th": "th", "ei": "e.long", "ou": "o.long"}
_SPLIT = {"kh": ["k", "h"], "gh": ["g", "h"], "dh": ["d", "h"], "rh": ["r", "h"], "sh": ["s", "h"],
          "zh": ["z", "h"], "ch": ["t", "s", "h"], "ph": ["f"]}
_ONE = {"y": "i", "w": "u", "q": "k"}


def spell(text: str) -> list[str]:
    """Helonic in roman to sign names, by the Helonic spelling: _th_ is one letter, _ei_
    is _ē_ and _ou_ is _ō_; the other aspirates are a stop and _h_; _y_ and _w_ are
    _i_ and _u_; Helonic writes no accent; ``.`` ``;`` ``:`` are the raised dot, and
    the comma, the dashes and the hyphen write nothing."""
    out, i = [], 0
    s = text.translate(_PLAIN)
    while i < len(s):
        c = s[i]
        pair = s[i:i + 2]
        low = pair.lower()
        cap = c.isupper()
        if low in _PAIRS:
            n = _PAIRS[low]
            out.append(n.upper().replace(".LONG", ".long") if cap else n)
            i += 2
            continue
        if low in _SPLIT:
            parts = _SPLIT[low]
            out += [parts[0].upper() if cap else parts[0]] + parts[1:]
            i += 2
            continue
        i += 1
        if c in ".;:":
            out.append("raisedDot")
        elif c == " ":
            out.append(" ")
        elif c in ",-–—":
            continue
        elif c.lower() in _ONE:
            n = _ONE[c.lower()]
            out.append(n.upper() if cap else n)
        elif c.lower() in "abdefghijklmnoprstuvz":
            out.append(c)
        else:
            raise ValueError(f"{text!r}: no Helónika sign for {c!r}")
    return out
