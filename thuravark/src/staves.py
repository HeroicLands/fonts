# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""The staves of Thuravark Runic, as stems and straight branches.

Every stave is one upright stem with up to four straight branches. A branch
is written as three characters: the side it leaves the stem on (F forward,
B back), the level of the stem it leaves from (T top, M middle, 0 foot) and
the level it ends at. A branch never ends at the level it leaves from, so no
cut runs along the line of text; the grain of the plank runs with the line and
a horizontal cut would split it. The one horizontal in the row is the short
nick of the sentence end.

Two branch lengths exist. A long branch spans the whole stem, foot to top, over
a short run at slope ``LONG_SLOPE``; a half branch spans half the stem over a
longer run at slope ``HALF_SLOPE``. The numerals use a third slope that no
stave has.

A tent or trough arm passes 135 units from the stem at the middle level, so a
half branch leaving there on the arm's side has no daylight against it. The
voicing branch of b and d therefore leaves at the end of the stem the arm does
not: from the foot under the tent (``B0M``), from the top over the trough
(``BTM``), and crosses the arm where the two are 271 units apart. The nasals
are one long arm of their family and one half branch leaving at the middle on
the other side, so no stave has more than two branches meeting at one point.

The strokes are Pirzath's: ``S`` is a groove that tapers to a point at both
ends, and the build unites them into one outline.
"""

import sys
from pathlib import Path

# Pirzath Carved owns the stroke primitives; this font imports them.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))
from glyphs import D, Glyph, S  # noqa: E402

STEM_H = 740  # every stave stands this tall
STEM_W = 84  # stroke weight of stems and branches
BEARING = 66  # room between the ink of one stave and the next
LONG_SLOPE = 2.73  # rise over run of a branch that spans the whole stem
HALF_SLOPE = 0.86  # rise over run of a branch that spans half of it
LONG_RUN = STEM_H / LONG_SLOPE
HALF_RUN = (STEM_H / 2) / HALF_SLOPE

LEVELS = {"T": STEM_H, "M": STEM_H / 2, "0": 0}

TENT = "FT0 BT0"
TROUGH = "F0T B0T"
POINT = "FTM F0M"

# (glyph name, sound, typed as, Pirzath parent as typed in Pirzath Carved, branches)
STAVE_TABLE = [
    ("a", "a", "a", "a", "F0T"),
    ("e", "e", "e", "e", "FTM BTM"),
    ("i", "i", "i, y not before a vowel", "i", ""),
    ("o", "o", "o", "o", "FTM F0M BTM B0M"),
    ("u", "u", "u", "u", "B0T"),
    ("p", "p", "p", "p", TENT),
    ("b", "b", "b", "b", TENT + " B0M"),
    ("f", "f", "f", "f", TENT + " FMT"),
    ("v", "v", "v", "v", TENT + " B0M FMT"),
    ("t", "t", "t", "t", TROUGH),
    ("d", "d", "d", "d", TROUGH + " BTM"),
    ("th", "th", "th", "th", TROUGH + " FMT"),
    ("dh", "dh", "dh", "dh", TROUGH + " BTM FMT"),
    ("k", "k", "k", "k", POINT),
    ("g", "g", "g", "g", POINT + " BM0"),
    ("kh", "kh", "kh", "kh", POINT + " FMT"),
    ("gh", "gh", "gh", "gh", POINT + " BM0 FMT"),
    ("s", "s", "s", "s", "FTM BM0"),
    ("z", "z", "z", "z", "FT0 B0T"),
    ("h", "h", "h", "h", "BM0 FMT"),
    ("l", "l", "l", "l", "FM0"),
    ("r", "r", "r", "r", "BTM B0M"),
    ("hl", "hl", "hl", "hl", "FM0 FMT"),
    ("m", "m", "m", "m", "FT0 BM0"),
    ("n", "n", "n", "n", "F0T BMT"),
    ("ng", "ng", "ng", "ng", "FTM F0M FMT FM0"),
    ("j", "y (glide)", "j, y before a vowel", "y", "FMT"),
    ("w", "w", "w", "w", "BMT"),
]
STAVE_NAMES = [row[0] for row in STAVE_TABLE]


def branch(spec: str):
    """The (x1, y1, x2, y2) of one branch, with the stem on x = 0."""
    side = {"F": 1, "B": -1}[spec[0]]
    y1, y2 = LEVELS[spec[1]], LEVELS[spec[2]]
    if y1 == y2:
        raise ValueError(f"{spec} is horizontal")
    run = LONG_RUN if {spec[1], spec[2]} == {"T", "0"} else HALF_RUN
    return (0.0, y1, side * run, y2)


def stem_cut(height=STEM_H):
    return S(0, 0, 0, height)


def _glyph(name, cuts, kind, weight=STEM_W):
    xs = [x for c in cuts if isinstance(c, S) for x in (c.x1, c.x2)]
    xs += [c.x for c in cuts if isinstance(c, D)]
    left = min(xs + [-weight / 2])
    right = max(xs + [weight / 2])
    dx = BEARING - left
    shifted = tuple(
        S(c.x1 + dx, c.y1, c.x2 + dx, c.y2, c.w) if isinstance(c, S) else D(c.x + dx, c.y)
        for c in cuts
    )
    return Glyph(name, shifted, int(round(right - left + 2 * BEARING)), weight, kind, int(BEARING))


def stave(name, branches):
    cuts = [stem_cut()] + [S(*branch(b)) for b in branches.split()]
    return _glyph(name, cuts, "stave")


STAVES = [stave(row[0], row[4]) for row in STAVE_TABLE]
# y is typed like j and drawn the same; the layout turns y into i or j.
Y_KEY = Glyph("y", STAVES[STAVE_NAMES.index("j")].cuts, STAVES[STAVE_NAMES.index("j")].width,
              STEM_W, "stave", int(BEARING))

# A long vowel is the stave twice. The precomposed code points carry the
# doubled outline for a renderer that applies no layout.
VOWELS = "aeiou"
ACUTES = {"á": "aacute", "é": "eacute", "í": "iacute", "ó": "oacute", "ú": "uacute"}


def doubled(vow: Glyph, name: str):
    shifted = tuple(
        S(c.x1 + vow.width, c.y1, c.x2 + vow.width, c.y2, c.w) for c in vow.cuts
    )
    return Glyph(name, vow.cuts + shifted, vow.width * 2, vow.weight, "stave", vow.bearing)


_BY_NAME = {g.name: g for g in STAVES}
LONG_VOWELS = [doubled(_BY_NAME[v], f"{v}acute") for v in VOWELS]

# ---------------------------------------------------------------------------
# Numerals: a stem taller than any stave, with up to four tally limbs worth 8,
# 4, 2 and 1. The limbs fall outward from the stem at a slope no stave has, and
# leave it at heights no stave branch leaves from; the lowest limb ends on the
# baseline. No two limbs leave at one height, so nought carries the one pair
# that does: two limbs rising from a height low on the stem, a cup no value
# makes, which tells it from the stave i by more than its height.
# ---------------------------------------------------------------------------

NUM_H = 900
NUM_SLOPE = 1.5
LIMB_RUN = 220
LIMB_DROP = LIMB_RUN * NUM_SLOPE
# place: (height the limb leaves the stem at, side)
TALLY = {8: (860, 1), 4: (520, 1), 2: (640, -1), 1: (330, -1)}
NOUGHT_CUP_Y = 150


def numeral(value):
    cuts = [stem_cut(NUM_H)]
    for place, (y, side) in TALLY.items():
        if value & place:
            cuts.append(S(0, y, side * LIMB_RUN, y - LIMB_DROP))
    if value == 0:
        for side in (1, -1):
            cuts.append(S(0, NOUGHT_CUP_Y, side * LIMB_RUN, NOUGHT_CUP_Y + LIMB_DROP))
    return _glyph(f"num.{value}", cuts, "numeral")


NUMERALS = [numeral(v) for v in range(10)]

# ---------------------------------------------------------------------------
# The sentence end and the keys that draw nothing.
# ---------------------------------------------------------------------------

DASH_RUN = 190
PERIOD = _glyph("period", [S(0, STEM_H / 2, DASH_RUN, STEM_H / 2)], "punct")

BLANK_NAMES = ("space", "hyphen", "blank", "acutecomb")
BLANKS = [Glyph(n, (), 0, STEM_W, "blank") for n in BLANK_NAMES]

# A key with no stave draws the blank stele: a stem with a drill mark either side.
STELE = _glyph("stele", [stem_cut(), D(-210, STEM_H / 2), D(210, STEM_H / 2)], "control", 70)
NOTDEF = Glyph(".notdef", STELE.cuts, STELE.width, 70, "control", STELE.bearing)

ALL_GLYPHS = [NOTDEF] + BLANKS + STAVES + [Y_KEY] + LONG_VOWELS + NUMERALS + [PERIOD, STELE]
GLYPHS = {g.name: g for g in ALL_GLYPHS}

# What types each stave. Digraphs are ligatures.
LETTERS = {c: c for c in "abdefghiklmnoprstuvz"}
LETTERS["j"] = "j"
LETTERS["w"] = "w"
LETTERS["y"] = "y"
DIGRAPHS = {"th": "th", "dh": "dh", "kh": "kh", "gh": "gh"}
OTHER_DIGRAPHS = {"ng": "ng", "hl": "hl"}
STELE_KEYS = "cqx"
HYPHENS = "-‐‑‒–—―"
SPACES = "    "
# Every other punctuation key draws nothing.
BLANK_KEYS = "!\"#$%&'()*+,/:;<=>?@[\\]^_`{|}~‘’“”„«»…·¡"


def cmap():
    """Every code point the font maps, to a glyph name."""
    m = {}
    for ch, name in LETTERS.items():
        m[ord(ch)] = name
        m[ord(ch.upper())] = name
    for ch in STELE_KEYS:
        m[ord(ch)] = "stele"
        m[ord(ch.upper())] = "stele"
    for ch, name in ACUTES.items():
        m[ord(ch)] = name
        m[ord(ch.upper())] = name
    m[0x0301] = "acutecomb"
    for ch in SPACES:
        m[ord(ch)] = "space"
    for ch in HYPHENS:
        m[ord(ch)] = "hyphen"
    for ch in BLANK_KEYS:
        m[ord(ch)] = "blank"
    m[ord(".")] = "period"
    for i in range(10):
        m[ord(str(i))] = f"num.{i}"
    return m
