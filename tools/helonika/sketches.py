# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Rough letter skeletons and stroke tests, set from the stroke inventory.

The skeletons are the six letters the owner ruled may echo Greek, _o_, _th_, _ō_,
_p_, _d_ and _l_, in both cases. They show the hand's character, so the reed, the
proportions and the terminals can be judged before any letter is drawn. They are
rough: the letters are the next layer's work.

The tests set strokes together to show how they sit. They are not letters of the
script.

Each entry builds its strokes on the line, and ``setting`` lays entries side by side
with ``S.BEARING`` either side of the ink.
"""

from __future__ import annotations

import strokes as S

C, X = S.CAP, S.X
W = S.HALF_W


def _o_cap():
    return [S.shape("round", 0, 0, w=0.95 * C, h=C)]


def _th_cap():
    w = 0.95 * C
    return [S.shape("round", 0, 0, w=w, h=C), S.shape("bar", 0, 0, w=0.56 * w, at=0.5 * C, knobs=2).moved(0.22 * w, 0)]


def _oo_cap():
    w = 0.92 * C
    hood = S.shape("hood", 60, 0, w=w, h=0.97 * C, open=86)
    (lx, _), (rx, _) = hood.tracks[0].end, hood.tracks[1].end
    left = S.shape("bar", 0, 0, w=lx + 30, at=S.HALF_H)
    right = S.shape("bar", rx - 30, 0, w=w + 120 - rx + 30, at=S.HALF_H)
    knobs = [S.shape("knob", S.KNOB_IN, S.HALF_H, drop=1, side=-1),
             S.shape("knob", w + 120 - S.KNOB_IN, S.HALF_H, drop=1, side=1)]
    return [hood, left, right] + knobs


def _p_cap():
    w = 0.74 * C
    return [S.shape("stem", W + 30, 0, top=C - 2 * S.HALF_H), S.shape("stem", w - W - 30, 0, top=C - 2 * S.HALF_H),
            S.shape("beam", 30, 0, w=w - 60, at=C, overhang=30)]


def _d_cap():
    w = 0.78 * C
    return [S.shape("diagonal", 0, 0, w=w / 2 + 20, h=C, rise=1), S.shape("diagonal", w / 2 - 20, 0, w=w / 2 + 20, h=C, rise=-1),
            S.shape("bar", -24, 0, w=w + 48, at=S.HALF_H)]


def _l_cap():
    w = 0.74 * C
    right = S.shape("diagonal", w / 2 - 40, 0, w=w / 2 + 40, h=C, rise=-1)
    # the short stroke rises into the long one and stops inside it, below the apex
    (ax, ay), (bx, by) = right.tracks[0].samples[0][:2], right.tracks[0].end
    u = 0.12
    tx, ty = ax + (bx - ax) * u, ay + (by - ay) * u
    left = S.shape("diagonal", 0, 0, w=tx + 0.6 * W, h=ty + S.HALF_H, rise=1)
    return [left, right]


def _o_min():
    return [S.shape("round", 0, 0, w=X, h=X)]


def _th_min():
    w = 0.62 * X
    return [S.shape("round", 0, 0, w=w, h=S.ASC), S.shape("bar", W, 0, w=w - 2 * W, at=0.48 * S.ASC)]


def _oo_min():
    w, h = 0.6 * X, 0.86 * X
    a = S.shape("cup", 0, 0, w=w, h=h, right=0.62)
    b = S.shape("cup", w - 2 * W, 0, w=w, h=h, left=0.62)
    return [a, b]


def _p_min():
    w = 0.78 * X
    return [S.shape("beam", 40, 0, w=w - 80, at=X, overhang=40),
            S.shape("stem", W + 40, 0, top=X - 2 * S.HALF_H),
            S.shape("stem", w - W - 40, 0, top=X - 2 * S.HALF_H),
            S.shape("foot", w - W - 40, 0, reach=50, lift=36)]


def _d_min():
    w = 0.9 * X
    bowl = S.shape("round", 0, 0, w=w, h=0.86 * X)
    head = S.shape("neck", w * 0.42, 0, h=S.ASC, base=0.86 * X - S.HALF_H, lean=0.5, curl=0.7)
    return [bowl, head]


def _l_min():
    w = 0.74 * X
    return [S.shape("diagonal", 0, 0, w=w, h=S.ASC, rise=-1), S.shape("diagonal", 0, 0, w=w * 0.5, h=0.55 * S.ASC, rise=1)]


def _dot():
    return [S.shape("dot", S.HALF_W, 0)]


SKETCHES = {
    "O": _o_cap, "TH": _th_cap, "Ō": _oo_cap, "P": _p_cap, "D": _d_cap, "L": _l_cap,
    "o": _o_min, "th": _th_min, "ō": _oo_min, "p": _p_min, "d": _d_min, "l": _l_min,
    "·": _dot,
}

CAPITALS = ["O", "TH", "Ō", "P", "D", "L"]
MINUSCULES = ["o", "th", "ō", "p", "d", "l"]


def _stem_arch():
    return [S.shape("stem", W, 0, top=S.ASC), S.shape("arch", W, 0)]


def _desc_lobe():
    return [S.shape("descender", W, 0, top=X, tail=1), S.shape("lobe", W, 0, top=X, bottom=0, w=0.5 * X)]


def _lead_stem_foot():
    return [S.shape("lead", W + 40, X), S.shape("stem", W + 40, 0), S.shape("foot", W + 40, 0)]


def _crescent_bar():
    return [S.shape("crescent", 0, 0), S.shape("bar", 0, 0, w=0.55 * X, at=0.5 * X, knobs=1).moved(S.HALF_W, 0)]


def _accented():
    return [S.shape("round", 0, 0, w=0.8 * X, h=X), S.shape("accent", 0.45 * X, 0)]


def _long():
    return [S.shape("round", 0, 0, w=0.8 * X, h=X), S.shape("length", 0.4 * X, 0)]


def _desc_forward():
    return [S.shape("descender", W, 0, top=X, tail=2), S.shape("cup", W * 2 - 2 * W, 0, w=0.55 * X, h=X)]


def _diagonals():
    return [S.shape("diagonal", 0, 0, w=0.5 * X, h=X, rise=-1), S.shape("diagonal", 0.5 * X - 2 * W, 0, w=0.5 * X, h=X, rise=1)]


TESTS = {
    "stem and arch": _stem_arch,
    "descender, tail back, and lobe": _desc_lobe,
    "lead, stem, foot": _lead_stem_foot,
    "crescent and knobbed bar": _crescent_bar,
    "descender forward and cup": _desc_forward,
    "falling then rising diagonal": _diagonals,
    "round with the accent": _accented,
    "round with the length bar": _long,
}


def tracks(build):
    return [t for sh in build() for t in sh.tracks]


def ink_x(trs):
    xs = [x for t in trs for x, *_ in t.samples]
    return min(xs) - S.HALF_W, max(xs) + S.HALF_W


_OUTLINES: dict = {}


def glyph(name, table=None):
    """One entry's outline and ink extent, drawn once and reused wherever it is set."""
    if name not in _OUTLINES:
        trs = tracks((table or {**SKETCHES, **TESTS})[name])
        _OUTLINES[name] = (S.outline(trs), *ink_x(trs))
    return _OUTLINES[name]


def setting(names, table=None):
    """Lay ``names`` side by side with ``S.BEARING`` either side of each one's ink;
    ``" "`` is the word space. Returns [(outline, x offset)] and the advance. Each
    entry is drawn once and only moved into place."""
    out, x = [], 0.0
    for n in names:
        if n == " ":
            x += S.SPACE
            continue
        path, lo, hi = glyph(n, table)
        out.append((path, x + S.BEARING - lo))
        x += (hi - lo) + 2 * S.BEARING
    return out, x
