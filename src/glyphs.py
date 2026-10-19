# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""The letters of Pirzath Carved, as graver strokes on a grid.

Every glyph is a list of cuts. A cut is either a straight stroke, ``S(x1, y1,
x2, y2)``, a groove the graver drives from one point to the other and that
tapers to a point at both ends, or a drilled dot, ``D(x, y)``. No cut runs
along the line of text: the grain of the stone runs with the seam the
inscription follows, and a cut along it splits the stone, so every stroke is
vertical or diagonal.

Coordinates are font units on a 1000-unit em. A consonant stands in a box 520
wide and 700 tall; a vowel is scored small in a box 300 wide and 400 tall,
because carved Pirzath cuts the skeleton of a word deep and scores the frame
between. The length mark is a drilled dot that sits in the headroom above a
vowel.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class S:
    """A straight stroke from (x1, y1) to (x2, y2), at the glyph's weight unless `w` says otherwise."""

    x1: float
    y1: float
    x2: float
    y2: float
    w: float | None = None


@dataclass(frozen=True)
class D:
    """A drilled dot centred on (x, y)."""

    x: float
    y: float


@dataclass(frozen=True)
class Glyph:
    name: str
    cuts: tuple
    width: int  # advance width
    weight: int  # stroke weight; the dot radius follows it
    kind: str  # consonant, vowel, mark, numeral, punct, control
    bearing: int = 0  # left side bearing already applied to the cuts
    anchor: tuple | None = None  # where the length mark attaches, on a vowel
    below: tuple | None = None  # where the doubling mark attaches, on a consonant
    mark_anchor: tuple | None = None  # the mark's own attachment point


# Box measures.
CONS_W, CONS_H = 520, 700
VOW_W, VOW_H = 300, 440
CONS_WEIGHT = 104
VOW_WEIGHT = 82
MARK_WEIGHT = 104
BEARING = 70
LENGTH_MARK_Y = 590  # the dot's centre over a vowel


def _shift(cuts, dx, dy=0):
    out = []
    for c in cuts:
        if isinstance(c, S):
            out.append(S(c.x1 + dx, c.y1 + dy, c.x2 + dx, c.y2 + dy, c.w))
        else:
            out.append(D(c.x + dx, c.y + dy))
    return tuple(out)


DOUBLING_Y = -40  # the doubling mark hangs this far under the baseline


def consonant(name, *cuts):
    xs = [x for c in cuts for x in (c.x1, c.x2)]
    return Glyph(
        name,
        _shift(cuts, BEARING),
        CONS_W + 2 * BEARING,
        CONS_WEIGHT,
        "consonant",
        BEARING,
        below=(BEARING + (min(xs) + max(xs)) / 2, DOUBLING_Y),
    )


def vowel(name, *cuts):
    return Glyph(
        name,
        _shift(cuts, BEARING),
        VOW_W + 2 * BEARING,
        VOW_WEIGHT,
        "vowel",
        BEARING,
        anchor=(BEARING + VOW_W / 2, LENGTH_MARK_Y),
    )


# ---------------------------------------------------------------------------
# Consonants. Three families share a frame, and inside a family the voiced
# letter adds a pole and the breathed letter nests a second chevron:
#
#   labial  p b f v m    the tent, apex up        /\
#   dental  t d th dh n  the trough, apex down    \/
#   velar   k g kh gh    the point, apex forward  >
#
# The sibilants are parallel cuts, the liquids are a long cut with a branch
# or a point opening forward, and h is the breath notch on a bare stem.
# ---------------------------------------------------------------------------

def notch_across(x1, y1, x2, y2, at=0.5, length=380, weight=None):
    """A short cut scored across a stroke, centred `at` along it: the breath."""
    dx, dy = x2 - x1, y2 - y1
    ln = (dx * dx + dy * dy) ** 0.5
    nx, ny = -dy / ln, dx / ln
    cx, cy = x1 + dx * at, y1 + dy * at
    h = length / 2
    return S(cx - nx * h, cy - ny * h, cx + nx * h, cy + ny * h, weight)


# The tent.
TENT = (S(0, 0, 260, 700), S(260, 700, 520, 0))
TENT_BREATH = (notch_across(260, 700, 520, 0, 0.45),)
POLE_LOW = (S(260, 0, 260, 350),)

# The trough.
TROUGH = (S(0, 700, 260, 0), S(260, 0, 520, 700))
TROUGH_BREATH = (notch_across(260, 0, 520, 700, 0.55),)
POLE_HIGH = (S(260, 700, 260, 350),)

# The point.
POINT = (S(110, 700, 520, 350), S(520, 350, 110, 0))
POINT_BREATH = (notch_across(110, 700, 520, 350, 0.5),)
POINT_BAR = (S(110, 700, 110, 0),)

CONSONANTS = [
    consonant("p", *TENT),
    consonant("b", *TENT, *POLE_LOW),
    consonant("f", *TENT, *TENT_BREATH),
    consonant("v", *TENT, *TENT_BREATH, *POLE_LOW),
    consonant(
        "m", S(0, 0, 130, 700), S(130, 700, 260, 350), S(260, 350, 390, 700), S(390, 700, 520, 0)
    ),
    consonant("t", *TROUGH),
    consonant("d", *TROUGH, *POLE_HIGH),
    consonant("t_h", *TROUGH, *TROUGH_BREATH),
    consonant("d_h", *TROUGH, *TROUGH_BREATH, *POLE_HIGH),
    consonant(
        "n", S(0, 700, 130, 0), S(130, 0, 260, 350), S(260, 350, 390, 0), S(390, 0, 520, 700)
    ),
    consonant("k", *POINT),
    consonant("g", *POINT, *POINT_BAR),
    consonant("k_h", *POINT, *POINT_BREATH),
    consonant("g_h", *POINT, *POINT_BREATH, *POINT_BAR),
    # Sibilants: s is the closed stone, a tall lozenge; z is the cross.
    consonant("s", S(260, 700, 470, 350), S(470, 350, 260, 0), S(260, 0, 50, 350), S(50, 350, 260, 700)),
    consonant("z", S(0, 0, 520, 700), S(0, 700, 520, 0)),
    # The breath on its own: the notch that marks it on a consonant, scored
    # across a bare stem. The one letter of the row that stands on a stave.
    consonant("h", S(260, 0, 260, 700), S(110, 420, 410, 600)),
    # Liquids: l is a long forward cut with a branch falling off its middle,
    # r is the point turned to open forward, the one letter that does.
    consonant("l", S(0, 0, 390, 700), S(195, 350, 455, 0)),
    consonant("r", S(410, 700, 0, 350), S(0, 350, 410, 0)),
]

# ---------------------------------------------------------------------------
# Vowels, scored small: a is a forward cut, u a back cut, i an upright, and
# the two rare ones are built, e a small tent and o a small lozenge.
# ---------------------------------------------------------------------------

VOWELS = [
    vowel("a", S(40, 0, 260, 440)),
    vowel("u", S(260, 0, 40, 440)),
    vowel("i", S(150, 0, 150, 440)),
    vowel("e", S(0, 0, 150, 440), S(150, 440, 300, 0)),
    vowel("o", S(150, 440, 300, 220), S(300, 220, 150, 0), S(150, 0, 0, 220), S(0, 220, 150, 440)),
]

# ---------------------------------------------------------------------------
# The seventeen lost letters: sounds the old row wrote and Khazari has lost.
# Each fills an empty cell of the system above, by its sound. LOST_KEYS and
# the two tables after DIGRAPHS say what types them.
# ---------------------------------------------------------------------------

LOZENGE = (S(260, 700, 470, 350), S(470, 350, 260, 0), S(260, 0, 50, 350), S(50, 350, 260, 700))
LOZENGE_BREATH = (notch_across(260, 700, 470, 350, 0.5, 300),)
CROSS = (S(0, 0, 520, 700), S(0, 700, 520, 0))
CROSS_BREATH = (notch_across(0, 700, 520, 0, 0.75, 300),)
LAMBDA = (S(0, 0, 390, 700), S(195, 350, 455, 0))

# The glides w and y stand in a wider box than the other consonants, so that
# their slanted cut clears the pole at both ends.
GLIDE_W = 720


def glide(name, *cuts):
    return Glyph(
        name,
        _shift(cuts, BEARING),
        GLIDE_W + 2 * BEARING,
        CONS_WEIGHT,
        "consonant",
        BEARING,
        below=(BEARING + GLIDE_W / 2, DOUBLING_Y),
    )


LOST_CONSONANTS = [
    # Beside s and z: the hush is the breath notch on the sibilant.
    consonant("sh", *LOZENGE, *LOZENGE_BREATH),
    consonant("zh", *CROSS, *CROSS_BREATH),
    consonant("ts", S(130, 0, 130, 700), S(130, 350, 520, 700), S(130, 350, 520, 0)),
    consonant("ch", S(390, 0, 390, 700), S(390, 350, 0, 700), S(390, 350, 0, 0)),
    # j and q are the stem-and-arm family of ts and ch turned to stand on the
    # stem: j is the Y, a stem from the baseline to mid height with two arms
    # rising from it to the corners of the cap; q is the Y upside down, a stem
    # from mid height to the cap with two arms falling from it to the corners
    # of the baseline. The arms meet the stem exactly at mid height and run
    # the full width of the box, which tells each from a numeral, whose stem
    # runs the full height and whose limbs fall away from it, and tells q from
    # the tent of p, whose apex is at the cap. Every cut tapers to a point at
    # its ends, so each of the three is driven past the junction and the
    # tapers are buried in the others' ink: an arm runs 79 units beyond the
    # junction along its own line, which puts it at full width where it
    # crosses the stem and ends its point inside the stem's body, and the stem
    # runs 70 units beyond, ending its point under where the arms' inner edges
    # meet. The union leaves one solid join and the three free ends.
    consonant("j", S(260, 0, 260, 420), S(307, 287, 0, 700), S(213, 287, 520, 700)),
    consonant("q", S(260, 700, 260, 280), S(307, 413, 0, 0), S(213, 413, 520, 0)),
    # The nasals: ng is the point doubled, as m and n double the tent and the
    # trough; ny is the doubled trough with the hanging pole.
    consonant("ng", S(110, 700, 390, 525), S(390, 525, 110, 350), S(110, 350, 390, 175),
              S(390, 175, 110, 0)),
    consonant("ny", S(0, 700, 130, 0), S(130, 0, 260, 350), S(260, 350, 390, 0),
              S(390, 0, 520, 700), *POLE_HIGH),
    # The throat letters stand on the stem: h carries the breath notch high,
    # the catch carries it low.
    consonant("catch", S(260, 0, 260, 700), S(110, 120, 410, 300)),
    # The glides are the vowels u and a cut at consonant size: w the back cut,
    # y the forward cut. Each carries the pole from baseline to cap, which a
    # vowel never does, so the glide is told from the vowel by more than its
    # height. The cut runs corner to corner of a box 720 wide and crosses the
    # pole at mid height, so that where the two reach full width near either
    # end the pole stands about 160 units clear of the cut, and the two read
    # apart rather than as one mass.
    glide("w", S(720, 0, 0, 700), S(360, 0, 360, 700)),
    glide("y", S(0, 0, 720, 700), S(360, 0, 360, 700)),
    # hl is l with the breath notch across its long cut.
    consonant("hl", *LAMBDA, notch_across(0, 0, 390, 700, 0.72, 300)),
]

# The vowel pairs, one letter each, built from their two vowels joined: i
# joins as an upright, u as a back cut. oi is ei turned over: the small
# trough of au with i's upright rising from its apex, as ei is the small tent
# of e with the upright hanging from its apex.
LOST_VOWELS = [
    vowel("ai", S(0, 0, 150, 440), S(150, 440, 150, 0)),
    vowel("au", S(0, 440, 150, 0), S(150, 0, 300, 440)),
    vowel("ei", S(0, 0, 150, 440), S(150, 440, 300, 0), S(150, 440, 150, 0)),
    vowel("oi", S(0, 440, 150, 0), S(150, 0, 300, 440), S(150, 0, 150, 440)),
    vowel("ou", S(150, 440, 300, 220), S(300, 220, 150, 0), S(150, 0, 0, 220), S(0, 220, 150, 440),
          S(40, 420, 260, 20)),
]

ALL_CONSONANTS = CONSONANTS + LOST_CONSONANTS

# The length mark: a drilled dot, attached above the vowel it lengthens.
LENGTH_MARK = Glyph(
    "lengthmark",
    (D(0, 0),),
    0,
    MARK_WEIGHT,
    "mark",
    mark_anchor=(0, 0),
)

# The doubling mark: a short forward cut hung under the letter's centre. It
# is the one mark that sits below a letter, so it is not the length dot above
# a vowel, the pole or the notch inside a letter, the dividing dot at mid
# height, or the sentence end along the grain. A doubled consonant is the
# letter once with this mark; a doubled digraph the same.
DOUBLING_MARK = Glyph(
    "doubling",
    (S(-90, -150, 90, 0),),
    0,
    92,
    "mark",
    mark_anchor=(0, 0),
)

# ---------------------------------------------------------------------------
# Numerals: a stem with up to four tally limbs at fixed places, worth 8, 4,
# 2 and 1. Nought is the bare stem.
# ---------------------------------------------------------------------------

NUM_W = 420
NUM_STEM_X = 210
LIMB = 190
# (height, side): 8 and 4 leave the stem forward, 2 and 1 back.
TALLY = {8: (640, 1), 4: (420, 1), 2: (380, -1), 1: (160, -1)}


def numeral(value):
    cuts = [S(NUM_STEM_X, 0, NUM_STEM_X, CONS_H)]
    for place, (y, side) in TALLY.items():
        if value & place:
            cuts.append(S(NUM_STEM_X, y, NUM_STEM_X + side * LIMB, y - LIMB))
    return Glyph(
        f"num.{value}", _shift(cuts, BEARING), NUM_W + 2 * BEARING, CONS_WEIGHT, "numeral", BEARING
    )


NUMERALS = [numeral(v) for v in range(16)]

# ---------------------------------------------------------------------------
# Punctuation and the marks between words.
# ---------------------------------------------------------------------------

MID = 350


def punct(name, width, *cuts, weight=CONS_WEIGHT):
    return Glyph(name, _shift(cuts, BEARING), width + 2 * BEARING, weight, "punct", BEARING)


PUNCTUATION = [
    # The dash of a built name: a short forward cut at mid height.
    punct("hyphen", 220, S(20, 230, 200, 480)),
    # The sentence end: a short cut along the grain at mid height, the one
    # horizontal cut in the row, which closes a thought.
    punct("period", 300, S(20, MID, 280, MID)),
    # The imperative: two short cuts along the grain, stacked at mid height.
    punct("exclam", 300, S(20, MID - 85, 280, MID - 85), S(20, MID + 85, 280, MID + 85)),
    # The pause inside a sentence: a short back cut at mid height. It slants
    # the other way from the dash so the two stay apart.
    punct("comma", 200, S(20, MID + 100, 180, MID - 100)),
]

# Word division: a drilled dot at mid height with room either side, lower
# than the length mark that sits over a vowel.
SPACE = Glyph("space", (D(BEARING + 170, MID),), 340 + 2 * BEARING, 96, "punct", BEARING)

# A key that draws nothing: a question is marked by the particle zef, and the
# row has no semicolon or colon.

# .notdef is a blank stele: a stem with a drill mark either side of it. The
# letter c has no Pirzath form and draws the same.
NOTDEF_CUTS = (S(260, 0, 260, 700), D(110, 350), D(410, 350))
NOTDEF = Glyph(".notdef", _shift(NOTDEF_CUTS, BEARING), CONS_W + 2 * BEARING, 70, "control")
C_LETTER = Glyph("c", _shift(NOTDEF_CUTS, BEARING), CONS_W + 2 * BEARING, 70, "control")

# Quotation marks, built on g and enclosing the quoted words the way « » do:
# the opening mark is g with two notches across its forward arm, the closing
# mark g with two notches across its back arm. The closing mark differs from
# gh, which notches the back arm once at its middle, by its second notch. The
# pair stands on the apex half of the arm, 0.4 of the arm apart, and is cut
# lighter than the breath notch, so that each notch clears the bar and the cap
# height and the two read as a pair at reading size.
UPPER_ARM = (110, 700, 520, 350)  # the back cut of the point, bar end first
LOWER_ARM = (520, 350, 110, 0)  # the forward cut of the point, apex first
QUOTE_NOTCH = 280
QUOTE_NOTCH_WEIGHT = 84


def quote(name, arm, places):
    cuts = (*POINT, *POINT_BAR,
            *(notch_across(*arm, t, QUOTE_NOTCH, QUOTE_NOTCH_WEIGHT) for t in places))
    return Glyph(name, _shift(cuts, BEARING), CONS_W + 2 * BEARING, CONS_WEIGHT, "punct", BEARING)


QUOTES = [
    quote("quote.open", LOWER_ARM, (0.2, 0.6)),
    quote("quote.close", UPPER_ARM, (0.4, 0.8)),
    # A straight quote draws the opening mark; calt turns it to the closing
    # mark wherever it does not follow a space.
    quote("quotedbl", LOWER_ARM, (0.2, 0.6)),
]

# < and > have no form of their own; typed twice they are the quotation marks.
ANGLES = [
    Glyph("less", _shift(NOTDEF_CUTS, BEARING), CONS_W + 2 * BEARING, 70, "control"),
    Glyph("greater", _shift(NOTDEF_CUTS, BEARING), CONS_W + 2 * BEARING, 70, "control"),
]


def precomposed(vow):
    """A vowel with its length mark drawn in, for the precomposed code points.

    Shaping decomposes these to vowel plus mark; the outline is for a renderer
    that applies no GSUB.
    """
    ax, ay = vow.anchor
    return Glyph(
        vow.name + "acute",
        vow.cuts + (D(ax, ay),),
        vow.width,
        vow.weight,
        "vowel",
        vow.bearing,
    )


ALL_GLYPHS = (
    [NOTDEF, SPACE]
    + CONSONANTS
    + VOWELS
    + LOST_CONSONANTS
    + LOST_VOWELS
    + [precomposed(v) for v in VOWELS]
    + [LENGTH_MARK, DOUBLING_MARK]
    + NUMERALS
    + PUNCTUATION
    + QUOTES
    + ANGLES
    + [C_LETTER]
)

GLYPHS = {g.name: g for g in ALL_GLYPHS}

# The sounds and what types them. A digraph is one letter by ligature.
LETTERS = {
    "b": "b",
    "d": "d",
    "g": "g",
    "k": "k",
    "p": "p",
    "t": "t",
    "v": "v",
    "f": "f",
    "z": "z",
    "s": "s",
    "h": "h",
    "m": "m",
    "n": "n",
    "l": "l",
    "r": "r",
    "a": "a",
    "e": "e",
    "i": "i",
    "o": "o",
    "u": "u",
    "c": "c",
}
DIGRAPHS = {"th": "t_h", "dh": "d_h", "gh": "g_h", "kh": "k_h"}
# The lost letters, by the spelling that types them. A single key maps straight
# to its glyph; a two-letter spelling is a ligature, and the vowel pairs read
# through a length mark between their vowels. The key y draws the glide; a y
# that is not before a vowel is reshaped to the vowel i.
LOST_KEYS = {"j": "j", "q": "q", "w": "w", "y": "y", "'": "catch", "\u2019": "catch"}
LOST_CONSONANT_DIGRAPHS = {
    "sh": "sh",
    "zh": "zh",
    "ch": "ch",
    "ts": "ts",
    "ng": "ng",
    "ny": "ny",
    "hl": "hl",
}
LOST_VOWEL_PAIRS = {"ai": "ai", "au": "au", "ei": "ei", "oi": "oi", "ou": "ou"}
ACUTES = {
    "á": "aacute",
    "é": "eacute",
    "í": "iacute",
    "ó": "oacute",
    "ú": "uacute",
}
PUNCT_MAP = {
    "-": "hyphen",
    ".": "period",
    ",": "comma",
    "!": "exclam",
    "¡": "exclam",
    " ": "space",
    " ": "space",
    "‐": "hyphen",
    "‑": "hyphen",
    '"': "quotedbl",
    "“": "quote.open",
    "”": "quote.close",
    "«": "quote.open",
    "»": "quote.close",
    "[": "quote.open",
    "]": "quote.close",
    "<": "less",
    ">": "greater",
}
# The sixteen numerals: the digits type nought to nine, and six signs type ten
# to fifteen.
NUMERAL_KEYS = "0123456789@#$%^&"


def cmap():
    """Every code point the font maps, to a glyph name."""
    m = {}
    for ch, name in LETTERS.items():
        m[ord(ch)] = name
        m[ord(ch.upper())] = name
    for ch, name in ACUTES.items():
        m[ord(ch)] = name
        m[ord(ch.upper())] = name
    m[0x0301] = "lengthmark"
    for ch, name in LOST_KEYS.items():
        m[ord(ch)] = name
        m[ord(ch.upper())] = name
    for ch, name in PUNCT_MAP.items():
        m[ord(ch)] = name
    for i, ch in enumerate(NUMERAL_KEYS):
        m[ord(ch)] = f"num.{i}"
    return m
