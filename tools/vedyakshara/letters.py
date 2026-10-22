# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""The Vedyakshara signs, built from the reed strokes of ``strokes.py``.

    import letters as L

    g = L.sign("ka")                      # a Glyph: tracks, advance, anchors
    g = L.sign("ka", form="half")         # the half form, ending on the cut
    g = L.sign("dra", vowel="i")          # a fused sign with the i flag
    run = L.write("vedyara")              # romanized Vedyari, set as a run of glyphs
    path = S.outline(run.tracks)

A consonant is a **body** and a **right part**. The body is one of nine hanging
shapes (``BODIES``); the right part is a stem hanging from the rope at the body's
right, a stem with a rung reaching back into the body, or nothing. Every sign
carries the rope over its whole advance. The forms of a sign follow from that
build:

- the **half form** drops the right part and ends on the cut where the stem
  stood, and its rope runs on into the next sign;
- the **final form** carries the rope past the stem and turns it down in the tick;
- the **r-foot form** adds the r-foot at the body's foot on the left, or at the
  stem's foot where the body does not reach the line; a fused C + r sign has none;
- a fused **C + r** sign puts the r into the stem, which sweeps down and back
  below the line;
- a fused **r + C** sign tucks a small _ra_ under the rope at the left of _C_;
- _ksha_, _sta_ and _dya_ set the first body, narrowed, **side by side** with the
  second sign;
- every other fused sign **stacks** the first body over the second, both at half
  height, on the second's right part.

The vowels are marks placed on anchors: a flag over the right end for _i_ and
over the middle for _e_, a hook under the right for _u_ and under the middle for
_o_, both for _ai_ and _au_. The digits stand free of the rope on the line;
shonya, zero, is a hollow lozenge.

This module draws; it does not shape. ``write`` segments romanized Vedyari only
so that specimens can set real words.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import strokes as S
from strokes import X, Track, Shape

SB = 44  # the body's sidebearing; the rope reaches across it
GAP = 6  # from a body's right edge to the stem it meets
TICK_PAST = 90  # how far the final form's rope runs past the stem before it turns down
TICK_DROP = 190  # the length of the final tick
CUT_DEPTH = 0.55  # how far the half form's cut falls, as a share of the body
SIDE = ("ksha", "sta", "dya")  # fused signs set side by side: stacked, their parts would clog at text size


@dataclass
class Glyph:
    name: str
    tracks: list
    adv: float
    anchors: dict = field(default_factory=dict)

    def moved(self, dx):
        tr = [Shape([t], (0, 0, 0), (0, 0, 0)).moved(dx, 0).tracks[0] for t in self.tracks]
        an = {k: (v + dx if isinstance(v, (int, float)) and v is not None else v) for k, v in self.anchors.items()}
        return Glyph(self.name, tr, self.adv, an)


# -- bodies -------------------------------------------------------------------------------------
#
# A body occupies a band of the body height, from ``bot`` to ``top`` (shares of X),
# and its left edge stands at ``x``. ``sx`` is the stem the body meets, for a lobe.

def _down(shape: Shape, top: float) -> list:
    """Move a shape hung from the rope down so it hangs from ``top`` of the body."""
    return shape.moved(0, -(1 - top) * X).tracks


def _bowl(x, w, top, bot, close=1.0):
    return _down(S.s_bowl(x, 0, w=w, h=top - bot, close=close), top)


def _arc(x, w, top, bot, side, turn):
    return _down(S.s_arc(x, 0, w=w, h=top - bot, side=side, turn=turn), top)


def b_full(x, w, sx, top=1.0, bot=0.0):
    return _bowl(x, w, top, bot)


def b_short(x, w, sx, top=1.0, bot=0.0):
    return _bowl(x, w, top, top - 0.52 * (top - bot))


def b_open(x, w, sx, top=1.0, bot=0.0):
    return _bowl(x, w, top, bot, close=0.78)


def c_right(x, w, sx, top=1.0, bot=0.0):
    return _arc(x, w, top, bot, 1, 0.6)


def c_short(x, w, sx, top=1.0, bot=0.0):
    return _arc(x, w, top, top - 0.56 * (top - bot), 1, 0.5)


def c_left(x, w, sx, top=1.0, bot=0.0):
    return _arc(x, w, top, bot, -1, 0.5)


def lobe(x, w, sx, top=1.0, bot=0.0):
    return S.s_lobe(sx, 0, w=sx - x, top=bot + 0.62 * (top - bot), bottom=bot).tracks


def s_curve(x, w, sx, top=1.0, bot=0.0):
    mid = (top + bot) / 2
    return _bowl(x, w, top, mid + 0.02) + _arc(x, w, mid + 0.02, bot, -1, 0.3)


def twin(x, w, sx, top=1.0, bot=0.0):
    h = top - 0.55 * (top - bot)
    half = (w - 14) / 2
    return _bowl(x, half, top, h) + _bowl(x + half + 14, half, top, h)


def two_arcs(x, w, sx, top=1.0, bot=0.0):
    half = (w - 10) / 2
    return _arc(x, half, top, bot, 1, 0.5) + _arc(x + half + 10, half, top, bot, -1, 0.5)


# name -> (builder, width, reaches the line)
BODIES = {
    "full": (b_full, 375, True),
    "short": (b_short, 330, False),
    "open": (b_open, 375, True),
    "c": (c_right, 300, True),
    "c-short": (c_short, 280, False),
    "c-left": (c_left, 290, True),
    "lobe": (lobe, 300, True),
    "s": (s_curve, 330, True),
    "twin": (twin, 420, False),
    "two-arcs": (two_arcs, 420, True),
}


# -- the sign table -----------------------------------------------------------------------------
#
# consonant -> (body, right part, breath). The right part is "stem", "rung" (a stem
# with a rung) or "none". The breath curl marks the aspirates, on the stem of the
# sign they breathe.

CONSONANTS = {
    "ka": ("full", "stem", False),
    "kha": ("full", "stem", True),
    "ga": ("c", "stem", False),
    "gha": ("c", "stem", True),
    "nga": ("c", "rung", False),
    "cha": ("short", "stem", False),
    "ja": ("lobe", "stem", False),
    "nya": ("twin", "rung", False),
    "ta": ("c-left", "stem", False),
    "da": ("c-left", "none", False),
    "na": ("c-short", "stem", False),
    "pa": ("open", "none", False),
    "ba": ("twin", "stem", False),
    "bha": ("twin", "stem", True),
    "ma": ("full", "rung", False),
    "ya": ("s", "stem", False),
    "ra": ("c-short", "none", False),
    "la": ("s", "none", False),
    "va": ("short", "none", False),
    "sha": ("c-left", "rung", False),
    "sa": ("s", "rung", False),
    "ha": ("c", "none", False),
}

VOWELS = {
    "a": ("twin", "none", False),
    "i": ("lobe", "rung", False),
    "u": ("two-arcs", "none", False),
    "e": ("short", "rung", False),
    "o": ("c-short", "rung", False),
}
VOWEL_SIGNS = ("i", "e", "ai", "u", "o", "au")
INDEPENDENT = ("a", "i", "u", "e", "o", "ai", "au")

# The nineteen fused clusters: the commonest consonant pairs of the Vedyari note,
# by the census in ``census.py``, the ties at the foot of the list broken by the
# lexicon's own words.
FUSED = ["nda", "dra", "tra", "ksha", "pra", "rta", "rsha", "vra", "sta", "rna", "gra", "dya", "shta",
         "mra", "nta", "shra", "rma", "tka", "rka"]

DIGITS = "0123456789"


def parts(name):
    """The consonant letters of a fused sign, as consonant sign names."""
    root = name[:-1]
    for i in range(1, len(root)):
        a, b = root[:i] + "a", root[i:] + "a"
        if a in CONSONANTS and b in CONSONANTS:
            return a, b
    raise KeyError(name)


def _right(kind, sx, x, breath, rstem=False, floor=0.0):
    tr = []
    if kind == "rung":
        tr += S.s_rung(sx, 0, w=sx - x - 8).tracks
    if rstem:
        if kind != "none":
            tr += S.s_rstem(sx, 0).tracks
        else:  # a sign with no stem of its own: the r is a tail from the body's floor
            fx = x + 0.6 * (sx - x)
            tr += S.s_rstem(fx, 0, reach=1.4, top=floor / X).tracks
    elif kind in ("stem", "rung"):
        tr += S.s_stem(sx, 0).tracks
    if breath:
        tr += S.s_breath(sx, 0).tracks
    return tr


def _anchors(body, x, w, sx, right):
    stem = sx if right != "none" else None
    if BODIES[body][2]:
        foot = x + (0.5 if body == "lobe" else 0.32) * w  # the body's own foot on the line
    else:
        foot = stem if stem is not None else x + 0.5 * w  # the stem's foot, or a neck from the body
    return {"stem": stem, "right": (sx - 14) if stem else x + 0.84 * w, "mid": x + w / 2, "foot": foot,
            "counter": (x + w / 2, 0.5 * X)}


def _base(name, spec):
    body, right, breath = spec
    build, w, _ = BODIES[body]
    x = SB
    sx = x + w + GAP
    tr = build(x, w, sx)
    tr += _right(right, sx, x, breath)
    edge = sx + (110 if breath else 0) if right != "none" else x + w
    return tr, edge, _anchors(body, x, w, sx, right), (body, right, breath, x, w, sx)


def _fused(name):
    a, b = parts(name)
    ba, ra, _ = CONSONANTS[a]
    bb, rb, brb = CONSONANTS[b]
    x = SB
    if b == "ra":  # the r rides the stem
        build, w, _ = BODIES[ba]
        sx = x + w + GAP
        body = build(x, w, sx)
        floor = max(0.0, _bottom(body, x + 0.6 * w) - 10)
        tr = body + _right(ra, sx, x, False, rstem=True, floor=floor)
        right = ra if ra != "none" else "none"
        edge = sx if right != "none" else x + w
        return tr, edge, _anchors(ba, x, w, sx, right), (ba, right, False, x, w, sx)
    if a == "ra":  # a small ra tucked under the rope before the sign
        tuck = _arc(x, 150, 1.0, 0.58, 1, 0.35)
        build, w, _ = BODIES[bb]
        x2 = x + 120
        sx = x2 + w + GAP
        tr = tuck + build(x2, w, sx) + _right(rb, sx, x2, brb)
        edge = sx if rb != "none" else x2 + w
        return tr, edge, _anchors(bb, x2, w, sx, rb), (bb, rb, brb, x2, w, sx)
    if name in SIDE:  # the first body, narrowed, runs straight into the second sign
        build_a, wa, _ = BODIES[ba]
        build_b, wb, _ = BODIES[bb]
        wa = 0.72 * wa
        x2 = x + wa + 10
        sx = x2 + wb + GAP
        tr = build_a(x, wa, x2) + build_b(x2, wb, sx) + _right(rb, sx, x2, brb)
        edge = sx if rb != "none" else x2 + wb
        return tr, edge, _anchors(bb, x2, wb, sx, rb), (bb, rb, brb, x2, wb, sx)
    # stacked: the first body over the second, on the second's right part
    build_a, wa, _ = BODIES[ba]
    build_b, wb, _ = BODIES[bb]
    w = max(wa, wb) * 0.9
    sx = x + w + GAP
    right = rb if rb != "none" else ("stem" if ra != "none" else "none")
    tr = build_a(x, w, sx, top=1.0, bot=0.5) + build_b(x, w, sx, top=0.5, bot=0.0)
    tr += _right(right, sx, x, brb)
    edge = sx if right != "none" else x + w
    return tr, edge, _anchors(bb, x, w, sx, right), (bb, right, brb, x, w, sx)


def _independent(v):
    if v in ("ai", "au"):
        tr, edge, an, geo = _base(v, VOWELS["e" if v == "ai" else "o"])
        return tr, edge, an, geo
    return _base(v, VOWELS[v])


def _bottom(tracks, x, near=26):
    """The lowest ink of a sign's body near ``x``. A stroke that reaches below the line,
    an r-stem, an r-foot or a hook, is not the body, and is left out."""
    body = [t for t in tracks if min(y for _, y, _ in t.samples) > -50]
    ys = [y for t in body for f, y, _ in t.samples if abs(f - x) < near]
    return min(ys) if ys else 0.0


def _marks(tracks, an, vowel):
    out = []
    if vowel in ("i", "ai"):
        out += S.s_flag(an["right"], 0).tracks
    if vowel in ("e", "ai"):
        out += S.s_flag(an["mid"] - 30, 0).tracks
    for v, key, side in (("u", "right", 1), ("o", "mid", 1)):
        if vowel == v or (vowel == "au" and v in ("u", "o")):
            x = an[key]
            yb = max(0.0, _bottom(tracks, x))
            out += S.s_hook(x, yb - 16, d=yb - 16 - S.HOOK, side=side).tracks
    return out


def sign(name, form="full", vowel=None):
    """One sign. ``form`` is full, half, final or rfoot; ``vowel`` one of VOWEL_SIGNS."""
    if name in CONSONANTS:
        tr, edge, an, geo = _base(name, CONSONANTS[name])
    elif name in FUSED:
        tr, edge, an, geo = _fused(name)
    elif name in INDEPENDENT:
        tr, edge, an, geo = _independent(name)
        if name == "ai":
            vowel = "i"
        elif name == "au":
            vowel = "u"
    elif name == "fa":
        tr, edge, an, geo = _base("pa", CONSONANTS["pa"])
        cx, cy = an["counter"]
        tr += S.s_dot(cx, cy, size=1.2).tracks
    else:
        raise KeyError(name)
    body, right, breath, x, w, sx = geo
    if form == "half":
        if right != "none":
            # rebuild without the right part, ending on the cut where the stem stood
            keep = [t for t in tr if not _is_right(t, sx)]
            tr = keep + S.s_cut(sx, 0, depth=CUT_DEPTH).tracks
            adv = sx + 34
        else:
            tr = tr + S.s_cut(x + w + 4, 0, depth=CUT_DEPTH).tracks
            adv = x + w + 38
        rope = S.s_headline(0, 0, w=adv).tracks
        return Glyph(name + ".half", rope + tr, adv, an)
    if form == "rfoot":
        if name in FUSED and name.endswith("ra"):
            raise ValueError(f"{name}: a fused C + r sign carries its r already and takes no r-foot")
        fx = an["foot"]
        yb = max(0.0, _bottom(tr, fx))
        neck = []
        if yb > 30:
            t = Track(fx, yb, S.BODY_P)
            t.line(fx, 20, S.BODY_P)
            neck = [t]
        tr = tr + neck + S.s_rfoot(fx, 0).tracks
    if vowel:
        tr = tr + _marks(tr, an, vowel)
    if form == "final":
        end = edge + TICK_PAST if right != "none" else edge + 50
        rope = S.s_tick(0, 0, w=end, drop=TICK_DROP).tracks
        return Glyph(name + ".final", rope + tr, end + SB, an)
    adv = edge + SB
    rope = S.s_headline(0, 0, w=adv).tracks
    return Glyph(name + ("." + form if form != "full" else ""), rope + tr, adv, an)


def _is_right(track, sx):
    """A track that belongs to the right part: it starts on the stem's line (a stem, a
    breath curl) or ends there (a rung), and is not a body."""
    f0, y0, _ = track.samples[0]
    f1, y1, _ = track.samples[-1]
    if all(abs(f - sx) < 1 for f, _, _ in track.samples):
        return True  # a stem
    if abs(f0 - sx) < 1 and min(y for _, y, _ in track.samples) < -50:
        return True  # the r-stem
    if abs(f1 - sx) < 1 and abs(y1 - y0) < 1:
        return True  # a rung
    if abs(f0 - sx) < 1 and f1 > sx + 10:
        return True  # a breath curl
    return False


# -- digits --------------------------------------------------------------------------------------
#
# The digits stand free of the rope, on the line and as tall as the body, written
# with the same reed. Shonya, zero, is a hollow lozenge.

DW = 300  # a digit's width
DP = 0.7  # the pressure the digits are written at


def _t(f, y):
    return Track(f, y, DP)


def digit(d: str) -> Glyph:
    x, w, h = SB, DW, X
    cx = x + w / 2
    tr = []
    if d == "0":  # shonya, empty: a hollow lozenge standing on its point
        t = _t(cx, h)
        t.line(x + w - 30, h / 2, DP)
        t.line(cx, 0, DP)
        t.line(x + 30, h / 2, DP)
        t.line(cx, h, DP)
        tr = [t]
    elif d == "1":  # a stem with its head turned back and its foot kicked forward
        t = _t(cx - 70, h * 0.86)
        t.curve((cx - 40, h * 0.98), (cx - 10, h * 1.0), cx, h * 0.9, DP)
        t.line(cx, 70, DP)
        t.curve((cx, 20), (cx + 30, 0), cx + 90, 14, DP)
        tr = [t]
    elif d == "2":  # a c over a level foot
        t = _t(x + w - 30, h * 0.82)
        t.curve((x + w - 90, h * 1.02), (x + 20, h * 1.0), x + 30, h * 0.62, DP)
        t.curve((x + 40, h * 0.3), (x + 120, h * 0.1), x + 40, 30, DP)
        t.line(x + w, 30, DP)
        tr = [t]
    elif d == "3":  # two c's, one over the other, open forward
        for top, bot in ((h, h / 2), (h / 2 + 20, 0)):
            t = _t(cx + 100, top - 30)
            t.arc(cx, (top + bot) / 2, w / 2 - 20, (top - bot) / 2, 40, 300, DP)
            tr.append(t)
    elif d == "4":  # a level head on two legs, the left one short
        t = _t(x + 30, h * 0.40)
        t.line(x + 30, h * 0.80, DP)
        t.curve((x + 30, h * 0.92), (x + 50, h * 0.94), x + 90, h * 0.94, DP)
        t.line(x + w - 40, h * 0.94, DP)
        s2 = _t(x + w - 40, h * 0.98)
        s2.line(x + w - 40, 0, DP)
        tr = [t, s2]
    elif d == "5":  # a level head drawn back, a fall, a floor and a rise turned in
        t = _t(x + w - 20, h * 0.94)
        t.line(x + 90, h * 0.94, DP)
        t.curve((x + 40, h * 0.94), (x + 30, h * 0.80), x + 30, h * 0.62, DP)
        t.line(x + 30, h * 0.30, DP)
        t.curve((x + 30, 0), (x + w - 20, -10), x + w - 20, h * 0.30, DP)
        t.curve((x + w - 20, h * 0.48), (x + w - 80, h * 0.52), x + w - 130, h * 0.44, DP)
        tr = [t]
    elif d == "6":  # a ring in the upper body with a stem falling from its left
        t = _t(x + 40, h * 0.66)
        t.arc(cx + 10, h * 0.68, w / 2 - 30, h * 0.28, 180, 540, DP)
        s2 = _t(x + 40, h * 0.7)
        s2.line(x + 40, 0, DP)
        tr = [t, s2]
    elif d == "7":  # a level head and a stem falling from its left end, kicked forward
        t = _t(x + w, h * 0.92)
        t.line(x + 50, h * 0.92, DP)
        t.line(x + 50, 50, DP)
        t.curve((x + 50, 10), (x + 80, 0), x + 140, 10, DP)
        tr = [t]
    elif d == "8":  # an arch on two legs, the feet turned out
        t = _t(x + 10, 10)
        t.curve((x + 40, 0), (x + 60, 20), x + 60, 80, DP)
        t.line(x + 60, h * 0.55, DP)
        t.curve((x + 60, h * 1.02), (x + w - 60, h * 1.02), x + w - 60, h * 0.55, DP)
        t.line(x + w - 60, 80, DP)
        t.curve((x + w - 60, 20), (x + w - 40, 0), x + w - 10, 10, DP)
        tr = [t]
    elif d == "9":  # a stem with two level strokes reaching back from it, at the head and the middle
        t = _t(x + w - 50, h)
        t.line(x + w - 50, 0, DP)
        tr = [t]
        for yy in (h * 0.92, h * 0.52):
            r = _t(x + 30, yy)
            r.line(x + w - 50, yy, DP)
            tr.append(r)
    return Glyph("num." + d, _fit_body(tr), x + w + SB, {})


def _fit_body(tracks):
    """Map a digit's tracks vertically so that its ink, reed and all, stands exactly
    from the line to the x-height, as tall as the body of a sign."""
    ink = S.contours(S.outline(tracks))
    lo = min(y for p in ink for _, y in p)
    hi = max(y for p in ink for _, y in p)
    ys = [y for t in tracks for _, y, _ in t.samples]
    t_lo, t_hi = min(ys), max(ys)
    pad_top, pad_bot = hi - t_hi, t_lo - lo
    a = (X - pad_top - pad_bot) / (t_hi - t_lo)
    b = pad_bot - a * t_lo
    out = []
    for t in tracks:
        n = Track(0, 0, 0)
        n.samples = [(f, a * y + b, p) for f, y, p in t.samples]
        out.append(n)
    return out


def point(knots: int) -> Glyph:
    """The bar: none, one knot (the pause) or two (the end of a sentence)."""
    tr = S.s_bar(SB + 40, 0, knots=knots).tracks
    return Glyph(f"bar.{knots}", tr, SB + 80 + SB, {})


# -- writing romanized Vedyari, for the specimens ------------------------------------------------

DIGRAPHS = ["ch", "sh", "kh", "gh", "bh", "ny", "ng", "ai", "au"]
VOWEL_UNITS = {"a", "e", "i", "o", "u", "ai", "au"}


def units(word):
    out, i = [], 0
    while i < len(word):
        if word[i:i + 2] in DIGRAPHS:
            out.append(word[i:i + 2])
            i += 2
        else:
            out.append(word[i])
            i += 1
    return out


def _groups(cluster):
    """Split a consonant cluster into signs: fused pairs, C + r as an r-foot form, and
    single consonants. Each is (sign, rfoot)."""
    out, i = [], 0
    while i < len(cluster):
        if i + 1 < len(cluster) and cluster[i] + cluster[i + 1] + "a" in FUSED:
            name = cluster[i] + cluster[i + 1] + "a"
            i += 2
        else:
            c = cluster[i]
            name = "fa" if c == "f" else c + "a"
            i += 1
        rf = i < len(cluster) and cluster[i] == "r" and i + 1 == len(cluster) and not name.endswith("ra")
        if rf:
            i += 1
        out.append((name, rf))
    return out


@dataclass
class Run:
    tracks: list
    width: float


def write(word: str) -> Run:
    """Set a romanized Vedyari word, compounds solid, as one run of signs."""
    us = units(word.lower().replace("-", ""))
    glyphs, i = [], 0
    while i < len(us):
        if us[i] in VOWEL_UNITS:
            glyphs.append(sign(us[i]))
            i += 1
            continue
        j = i
        while j < len(us) and us[j] not in VOWEL_UNITS:
            j += 1
        vowel = us[j] if j < len(us) else None
        groups = _groups(us[i:j])
        for k, (name, rf) in enumerate(groups):
            last = k == len(groups) - 1
            if not last:
                glyphs.append(sign(name, form="half"))
            elif vowel is None:
                glyphs.append(sign(name, form="final"))
            else:
                v = None if vowel == "a" else vowel
                glyphs.append(sign(name, form="rfoot" if rf else "full", vowel=v))
        i = j + (1 if vowel else 0)
    tracks, x = [], 0.0
    for g in glyphs:
        tracks += g.moved(x).tracks
        x += g.adv
    return Run(tracks, x)
