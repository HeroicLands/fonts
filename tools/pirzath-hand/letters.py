# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""The Pirzath Hand signs, each built from the strokes of ``strokes.py``.

    import letters as L

    sign = L.SIGNS["b"]                    # a Sign: its name, label and parts
    tracks, advance = L.draw("b")           # the tracks at the sign's own origin, and its advance
    L.write(["b", "a", "n", "t"])           # a run of signs: tracks and width

A sign is one, two or at most three strokes, and every part of it is a full stroke.
The hand is printed: each sign stands apart, with ``SB`` of white either side of its
ink, and a word space of ``WORD``.

**The families.** A consonant of the carved row keeps its family's frame, worn into
the pen's simplest stroke, and its two modifiers become full strokes inside the sign:

- **The tent** (``Λ``) writes _p_; **the trough** (``V``) _t_; **the point** (``>``) _k_.
- **Voiced** (_b_, _d_, _g_): the carved pole becomes a full stem standing in the
  frame, from its apex or point to the line or the head.
- **Breathed** (_f_, _th_, _kh_): one arm of the frame is worn to half its length,
  still a full stroke.
- **Voiced and breathed** (_v_, _dh_, _gh_): both.

The nasals are the roof with a heel: ``]`` for _m_, ``[`` for _n_, and the same
carried below the line for _ng_ and _ny_. The vowels stand at ``VOWEL``, smaller than
the consonants, as the carved face scores them; a long vowel carries the length bar
over it. A digit stands at ``DIGIT``, a little shorter than a consonant, and is a stem
with one full stroke: no letter is a lone stem with one stroke.
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import strokes as S  # noqa: E402

B = S.BODY
V = S.VOWEL
DIGIT = 0.85 * B  # a digit's height: a little shorter than a consonant, on the line
SB = 70.0  # the white either side of a sign's ink
WORD = 0.5 * 1000  # the word space, in units
W = 0.66 * B  # the standard frame width
INSET = S.IN * S.HALF_W  # how far a frame's track sits inside its ink box


@dataclass
class Sign:
    name: str  # the glyph name the font gives it
    label: str  # the roman that writes it
    parts: list = field(default_factory=list)  # (stroke, f, y, params)
    kind: str = "letter"  # letter, vowel, diphthong, digit, point, mark


# -- geometry the signs share ------------------------------------------------------------------


def tent_apex(f, w=W, peak=0.42):
    """The frame position of a tent's apex track."""
    return f + INSET + (w - 2 * INSET) * peak


def trough_base(f, w=W, base=0.4):
    """The frame position of a trough's base point."""
    return f + INSET + (w - 2 * INSET) * base


def point_vertex(f, w=0.42 * B, h=B, at=0.6, side=1):
    """The frame position and height of a point's vertex track."""
    x = f + w - INSET if side > 0 else f + INSET
    return x, S.HALF_H + (h - 2 * S.HALF_H) * at


# -- the signs ---------------------------------------------------------------------------------


def _vowels():
    out = {}
    out["a"] = Sign("a", "a", [("cut", 0, 0, dict(w=0.32 * B, h=V, top=V, fall=-1))], "vowel")
    out["e"] = Sign("e", "e", [("tent", 0, 0, dict(w=0.56 * B, h=V))], "vowel")
    out["i"] = Sign("i", "i", [("stem", S.HALF_W, 0, dict(top=V))], "vowel")
    out["o"] = Sign("o", "o", [("round", 0, 0, dict(w=0.52 * B, h=0.8 * V))], "vowel")
    out["u"] = Sign("u", "u", [("cut", 0, 0, dict(w=0.32 * B, h=V, top=V, fall=1))], "vowel")
    return out


def _long(v: Sign) -> Sign:
    """A long vowel: the vowel with the length bar over it, centred on its ink."""
    lo, hi = ink_x(v.parts)
    c = (lo + hi) / 2
    return Sign(v.name + ".long", v.label + "́",
                v.parts + [("bar", c - S.FULL / 2, 0, dict(at=S.LENGTH_Y))], "vowel")


def _diphthongs():
    out = {}
    aw = 0.32 * B
    # ai: the a-cut and the i-stem meeting at the head
    out["ai"] = Sign("ai", "ai", [("cut", 0, 0, dict(w=aw, h=V, top=V, fall=-1)),
                                  ("stem", aw - INSET, 0, dict(top=V))], "diphthong")
    # au: the a-cut and the u-cut meeting at the foot, a small trough
    out["au"] = Sign("au", "au", [("trough", 0, 0, dict(w=0.56 * B, h=V, base=0.5, rise=1.0))], "diphthong")
    # ei: the small tent with the i-stem standing close beside its right foot
    ew = 0.56 * B
    out["ei"] = Sign("ei", "ei", [("tent", 0, 0, dict(w=ew, h=V)), ("stem", ew + 0.06 * B, 0, dict(top=V))],
                     "diphthong")
    # oi: a small round with the i-stem rising from its head
    rw = 0.52 * B
    ro = 0.5 * V
    out["oi"] = Sign("oi", "oi", [("round", 0, 0, dict(w=0.4 * B, h=ro)),
                                  ("stem", 0.2 * B, 0, dict(top=ro + S.FULL - 2 * S.HALF_H, foot=ro - 2 * S.HALF_H))],
                     "diphthong")
    # ou: the round with the u-cut falling from its right
    out["ou"] = Sign("ou", "ou", [("round", 0, 0, dict(w=rw, h=0.8 * V)),
                                  ("cut", rw - 2 * INSET, 0, dict(w=0.3 * B, h=V, top=V, fall=1))], "diphthong")
    return out


def _consonants():
    out = {}
    ax = tent_apex(0)
    bx = trough_base(0)
    vx, vy = point_vertex(0)
    # the tent family
    out["p"] = Sign("p", "p", [("tent", 0, 0, {})])
    out["b"] = Sign("b", "b", [("tent", 0, 0, {}), ("stem", ax, 0, {})])
    out["f"] = Sign("f", "f", [("tent", 0, 0, dict(left=0.5))])
    out["v"] = Sign("v", "v", [("tent", 0, 0, dict(left=0.5)), ("stem", ax, 0, {})])
    # the trough family
    out["t"] = Sign("t", "t", [("trough", 0, 0, {})])
    out["d"] = Sign("d", "d", [("trough", 0, 0, {}), ("stem", bx, 0, {})])
    out["t_h"] = Sign("t_h", "th", [("trough", 0, 0, dict(rise=0.55))])
    out["d_h"] = Sign("d_h", "dh", [("trough", 0, 0, dict(rise=0.55)), ("stem", bx, 0, {})])
    # the point family
    out["k"] = Sign("k", "k", [("point", 0, 0, {})])
    out["g"] = Sign("g", "g", [("point", 0, 0, {}), ("stem", vx, 0, dict(top=vy + S.HALF_H))])
    out["k_h"] = Sign("k_h", "kh", [("point", 0, 0, dict(lower=0.5))])
    out["g_h"] = Sign("g_h", "gh", [("point", 0, 0, dict(lower=0.5)), ("stem", vx, 0, dict(top=vy + S.HALF_H))])
    # the nasals: the roof with a heel, carried below the line for ng and ny
    out["m"] = Sign("m", "m", [("roof", 0, 0, dict(heel=1, side=-1))])
    out["n"] = Sign("n", "n", [("roof", 0, 0, dict(hand=-1, heel=1, side=1))])
    out["ng"] = Sign("ng", "ng", [("roof", 0, 0, dict(foot=S.DESC, heel=1, side=-1))])
    out["ny"] = Sign("ny", "ny", [("roof", 0, 0, dict(hand=-1, foot=S.DESC, heel=1, side=1))])
    # the sibilants
    out["s"] = Sign("s", "s", [("cut", 0, 0, dict(heel=1, side=-1))])
    out["sh"] = Sign("sh", "sh", [("cut", 0, 0, dict(fall=-1, heel=1, side=1))])
    zw = 0.42 * B
    out["z"] = Sign("z", "z", [("cut", 0, 0, dict(w=zw)),
                               ("cut", 0.05 * B, 0, dict(w=0.4 * B, h=0.6 * B, top=B, fall=-1))])
    out["zh"] = Sign("zh", "zh", [("cut", 0, 0, dict(w=zw, heel=1, side=1)),
                                 ("cut", 0.05 * B, 0, dict(w=0.4 * B, h=0.6 * B, top=B, fall=-1))])
    # the liquids and h
    lw = 0.5 * B
    out["l"] = Sign("l", "l", [("cut", 0, 0, dict(w=lw, h=S.ASC, top=S.ASC, fall=-1)),
                               ("cut", 0.24 * B, 0, dict(w=0.3 * B, h=0.6 * S.ASC, top=0.6 * S.ASC))])
    out["hl"] = Sign("hl", "hl", [("cut", 0, 0, dict(w=lw, h=S.ASC, top=S.ASC, fall=-1)),
                                 ("cut", 0.24 * B, 0, dict(w=0.3 * B, h=0.6 * S.ASC, top=0.6 * S.ASC, heel=1, side=1))])
    out["r"] = Sign("r", "r", [("point", 0, 0, dict(side=-1))])
    out["h"] = Sign("h", "h", [("point", 0, 0, dict(side=-1, lower=0.5))])
    out["catch"] = Sign("catch", "'", [("cut", 0, 0, dict(w=0.35 * B, h=B - S.DESC, top=B, fall=-1))])
    # the lost letters
    out["ts"] = Sign("ts", "ts", [("point", 0, 0, dict(heel=1, away=1))])
    out["ch"] = Sign("ch", "ch", [("point", 0, 0, dict(side=-1, heel=1, away=1))])
    out["j"] = Sign("j", "j", [("cut", 0, 0, dict(w=0.4 * B, h=S.ASC - S.DESC, top=S.ASC))])
    out["q"] = Sign("q", "q", [("cut", 0, 0, dict(fall=-1, heel=1, side=-1))])
    out["w"] = Sign("w", "w", [("point", 0, 0, dict(upper=0.5))])
    yh = B - S.DESC
    out["y"] = Sign("y", "y", [("point", 0, S.DESC, dict(h=yh, at=(0.6 * B - S.DESC) / yh))])
    return out


def _digits():
    """Sixteen digits: a stem a little shorter than a consonant, with one full stroke
    or, for 12 to 15, two. The stroke is a limb running out from the stem at 60°, a
    level bar from or across it, or a shallow cut across it at 30°, at a fixed place:
    the head, the middle or the foot. 10 and 11 carry one shallow cut across the
    middle; 12 to 15 carry two strokes across the stem, so none of them can be taken
    for a digit with one limb. 1, 4 and 8 keep the places of the carved tally's limbs.
    No digit is a Latin letter or digit: no limb falls back from the head (a 1), no
    bar runs back from the head (a 7) or the foot (a J), and no limb rises from the
    middle (a Y)."""
    L = S.FULL
    c = 0.0  # the stem's centre
    head, mid, foot = DIGIT - S.HALF_H, DIGIT / 2, S.HALF_H

    def limb(y, deg):
        r = math.radians(deg)
        cx, cy = c + L / 2 * math.cos(r), y + L / 2 * math.sin(r)
        return ("notch", cx, 0, dict(length=L, angle=deg % 180, at=cy))

    def bar(y, direction):
        """A level stroke from the stem forward (1), back (-1) or across it (0)."""
        if direction == 0:
            return ("bar", c - L / 2, 0, dict(at=y))
        if direction > 0:
            return ("bar", c - S.HALF_W, 0, dict(at=y))
        return ("bar", c - L + S.HALF_W, 0, dict(at=y))

    def across(share, deg):
        """A shallow cut crossing the stem at ``share`` of its height."""
        return ("notch", c, 0, dict(length=L, angle=deg, at=share * DIGIT))

    stem = ("stem", c, 0, dict(top=DIGIT))
    hi, lo = 0.72, 0.28  # the places of a pair of strokes across the stem
    extra = {
        0: bar(mid, 0),
        1: limb(foot, 120),
        2: limb(foot, 60),
        3: limb(mid, 240),
        4: limb(mid, -60),
        5: bar(mid, -1),
        6: bar(mid, 1),
        7: bar(head, 1),
        8: limb(head, -60),
        9: bar(foot, 0),
        10: across(0.5, 30.0),
        11: across(0.5, 150.0),
        12: [across(hi, 30.0), across(lo, 30.0)],
        13: [across(hi, 150.0), across(lo, 150.0)],
        14: [bar(hi * DIGIT, 0), bar(lo * DIGIT, 0)],
        15: [across(0.5, 30.0), across(0.5, 150.0)],
    }
    return {f"num.{v}": Sign(f"num.{v}", str(v), [stem] + (e if isinstance(e, list) else [e]), "digit")
            for v, e in extra.items()}


def _points():
    out = {}
    out["period"] = Sign("period", ".", [("bar", 0, 0, dict(at=S.MID))], "point")
    out["exclam"] = Sign("exclam", "!", [("bar", 0, 0, dict(at=S.MID + 100)), ("bar", 0, 0, dict(at=S.MID - 100))],
                         "point")
    out["comma"] = Sign("comma", ",", [("bar", 0, 0, dict(at=S.HALF_H))], "point")
    out["hyphen"] = Sign("hyphen", "-", [("bar", 0, 0, dict(at=S.MID, tilt=20.0))], "point")
    # the quotation marks: the opening quote is drawn as the vowel u, the closing quote
    # as a, so a quotation reads \word/ and each mark leans into its word at the foot.
    # No Khazari word begins or ends with a vowel, so a u-sign set against the head of
    # a word can only open a quotation and an a-sign against its end can only close one.
    out["quote.open"] = Sign("quote.open", "“", list(VOWEL_PARTS["u"]), "point")
    out["quote.close"] = Sign("quote.close", "”", list(VOWEL_PARTS["a"]), "point")
    out["lengthmark"] = Sign("lengthmark", "́", [("bar", 0, 0, dict(at=S.LENGTH_Y))], "mark")
    out[".notdef"] = Sign(".notdef", "?", [("cross", 0, 0, dict(lean=0.0))], "point")
    return out


def _doubled(sign: Sign) -> Sign:
    """A doubled consonant: the letter once, with the doubling stroke laid shallow under
    it, centred on its ink."""
    lo, hi = ink_x(sign.parts)
    c = (lo + hi) / 2
    if descends(sign.parts):
        c = hi + S.FULL / 2 + 30  # under a descender the stroke stands beside it
    return Sign(sign.name + ".double", sign.label * 2 if len(sign.label) == 1 else sign.label + sign.label,
                sign.parts + [("notch", c, 0, dict(angle=8.0, at=-105.0))], sign.kind)


def descends(parts) -> bool:
    """Whether the parts reach below the line."""
    return any(py < -S.HALF_H for sid, f, y, p in parts for t in S.shape(sid, f, y, **p).tracks
               for _, py, _ in t.samples)


def ink_x(parts):
    """The page extent of the parts' tracks, ink included."""
    xs = []
    for sid, f, y, params in parts:
        for t in S.shape(sid, f, y, **params).tracks:
            xs += [S.to_page(px, py)[0] for px, py, _ in t.samples]
    return min(xs) - S.HALF_W, max(xs) + S.HALF_W


VOWELS = _vowels()
VOWEL_PARTS = {k: v.parts for k, v in VOWELS.items()}
LONG = {k + ".long": _long(v) for k, v in VOWELS.items()}
DIPHTHONGS = _diphthongs()
CONSONANTS = _consonants()
DIGITS = _digits()
POINTS = _points()
DOUBLED = {k + ".double": _doubled(v) for k, v in CONSONANTS.items()}

SIGNS: dict[str, Sign] = {**VOWELS, **LONG, **DIPHTHONGS, **CONSONANTS, **DIGITS, **POINTS, **DOUBLED}


def draw(name: str):
    """A sign's tracks with its ink starting ``SB`` from its origin, and its advance."""
    sign = SIGNS[name]
    lo, hi = ink_x(sign.parts)
    dx = SB - lo
    tracks = []
    for sid, f, y, params in sign.parts:
        tracks += S.shape(sid, f + dx, y, **params).tracks
    return tracks, hi - lo + 2 * SB


def write(names, f0=0.0):
    """A run of signs, ``None`` for a word space: their tracks and the run's width."""
    tracks, f = [], f0
    for n in names:
        if n is None:
            f += WORD
            continue
        tr, adv = draw(n)
        for t in tr:
            m = S.Track(0, 0)
            m.samples = [(x + f, y, p) for x, y, p in t.samples]
            tracks.append(m)
        f += adv
    return tracks, f - f0


def strokes_in(name: str) -> int:
    """How many pen movements a sign takes."""
    return sum(len(S.shape(sid, f, y, **p).tracks) for sid, f, y, p in SIGNS[name].parts)
