# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""The Ch'alish P'ilam common hand's glyphs, and the words written with them.

    import glyphs as K

    K.WORDS["kul'qat"].glyphs                 # (PEAK,): one glyph, its own concept
    K.COMPOUNDS["priest"].glyphs              # (PEAK, PERSON): two glyphs, a concept of their own

A **glyph** is a skeleton ideogram drawn from the strokes of ``strokes.py``, filling a
whole cell. Each is a **concept**, the thing its picture shows, named by a Ki'i'chek
word, and has a **sound**: the opening consonant and vowel of that word, its catch left
out (the jaguar, _ish'bal_, is _i_; the serpent, _ch'akun_, is _cha_). Two glyphs may
share a sound.

A word is written with one glyph, or with two or three that together make a concept of
their own: WATER with FLAME is the sky, PEAK with PERSON a priest, LORD with STEPS a
king. A glyph may also stand for its sound, and a name is written in sounds, the way
Maya scribes wrote them: a closing consonant takes a syllable whose vowel is silent,
usually an echo of the vowel before it, so _Ch'akul_ is _cha-ku-lu_, and a catch is
left to the reader. Context decides how a glyph is read and how many glyphs make a
word, and a run may mean one thing by its pictures and another by its sounds at once.

The roman transcription records every sound; the script has no spelling and does not
have to. A glyph is always drawn whole and the same: no mark is ever added to it or
taken from it.

Text runs two glyphs to a row, left to right, down a column two cells wide. Rows are
layout only: a word may begin in either cell and run on into the next row.

The line keeps its width however a glyph is drawn, as a pen does.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable

import strokes as S

B = S.BLOCK
C = B / 2
LO, HI = 80.0, B - 80.0  # the ink's reach inside a cell, both ways


@dataclass(frozen=True)
class Glyph:
    name: str  # the name the sheets print, in capitals
    meaning: str  # what the picture shows
    word: str  # the Ki'i'chek word that names the picture, from the lexicon
    sound: str  # the syllable it writes when it stands for a sound
    draw: Callable[[], list]  # tracks and fills in a whole cell
    tier: str = "general"  # core, general, sacred, or trade:<occupation>
    traditional: bool = False  # its sound is the first codex's, not its word's opening

    def __post_init__(self):
        drawn = self.draw
        object.__setattr__(self, "draw", lambda: grow(drawn(), GROW))


# Every glyph is drawn inside an 80-unit margin and then grown about the cell's centre by
# GROW, so its ink fills the cell from the line to cap height. The line keeps its width.
GROW = 1.25


def grow(parts, k):
    out = []
    for p in parts:
        pts = [(C + (x - C) * k, C + (y - C) * k) for x, y in p.pts]
        if isinstance(p, S.Fill):
            out.append(S.Fill(pts))
        else:
            out.append(S.Track(pts, closed=p.closed, weight=p.weight))
    return out


def _parts(*groups):
    out = []
    for g in groups:
        out += g
    return out


# -- the glyphs ----------------------------------------------------------------------------------


def _sun():
    rays = []
    for a in (90, 0, 270, 180):
        t = math.radians(a)
        rays += S.bar(C + 205 * math.cos(t), C + 205 * math.sin(t), C + 285 * math.cos(t), C + 285 * math.sin(t))
    return _parts(S.ring(C, C, 150), S.dot(C, C, 34), rays)


def _water():
    return _parts(S.wave(LO + 20, C + 100, HI - 20, 60, 1.5), S.wave(LO + 20, C - 100, HI - 20, 60, 1.5))


def _river():
    return _parts(S.bar(LO, HI - 30, HI, HI - 30), S.wave(LO + 40, C, HI - 40, 55, 1.5), S.bar(LO, LO + 30, HI, LO + 30))


def _peak():
    # a stepped mountain-pyramid with a shrine post on its summit
    y0 = LO + 20
    pts = [(LO, y0), (LO + 70, y0), (LO + 70, y0 + 140), (LO + 150, y0 + 140), (LO + 150, y0 + 280),
           (C - 70, y0 + 280), (C - 70, y0 + 400), (C + 70, y0 + 400), (C + 70, y0 + 280),
           (HI - 150, y0 + 280), (HI - 150, y0 + 140), (HI - 70, y0 + 140), (HI - 70, y0), (HI, y0)]
    return _parts(S.poly(pts), S.bar(C, y0 + 400, C, HI))


def _steps():
    # a stair climbing to the right, closed under its back
    n = 4
    w = (HI - LO) / n
    pts, x, y = [(LO, LO)], LO, LO
    for _ in range(n):
        y += w
        pts.append((x, y))
        x += w
        pts.append((x, y))
    pts += [(HI, LO), (LO, LO)]
    return S.poly(pts)


def _jaguar():
    # a cat's head in profile, facing the line's start: the skull open at the mouth, a
    # round ear, the eye, a tooth and three spots
    return _parts(S.hook(C + 30, C - 10, 240, opening=200), S.arc(C + 100, C + 215, 70, 70, 10, 170),
                  S.ring(C - 70, C + 60, 42), S.tick(LO + 60, C - 70, 90, angle=270),
                  S.dot(C + 120, C + 20, 30), S.dot(C + 60, C - 110, 30), S.dot(C + 170, C - 100, 30))


def _serpent():
    return _parts(S.wave(C - 60, C - 40, HI - 10, 80, 1.25), S.curl(LO + 110, C - 20, 120, clockwise=True),
                  S.tick(LO - 20, C + 60, 90, angle=150))


def _flame():
    # a fire on its hearth: a rising curl at the centre and a tongue each side
    return _parts(S.bar(LO, LO + 20, HI, LO + 20), S.curl(C, C + 60, 150, turns=1.1),
                  S.arc(C - 150, LO + 20, 90, 220, 20, 90), S.arc(C + 150, LO + 20, 90, 220, 90, 160))


def _moon():
    return _parts(S.arc(C, C, 250, 250, 60, 300), S.arc(C + 110, C, 200, 210, 80, 280), S.dot(C - 20, C, 30))


def _person():
    return _parts(S.ring(C, HI - 90, 80), S.bar(C, HI - 170, C, C - 60), S.bar(LO + 80, C + 80, HI - 80, C + 80),
                  S.bar(C, C - 60, LO + 90, LO), S.bar(C, C - 60, HI - 90, LO))


def _all():
    return _parts(S.ring(C, C, 240), S.dot(C, C + 100, 36), S.dot(C - 95, C - 65, 36), S.dot(C + 95, C - 65, 36))


def _above():
    return _parts(S.bar(LO, C - 90, HI, C - 90), S.dot(C, C + 130, 58))


def _toward():
    # toward: two strokes meeting at the point they lead to
    return S.poly([(LO + 120, HI - 40), (HI - 100, C), (LO + 120, LO + 40)])


def _being():
    return _parts(S.bar(LO, LO + 30, HI, LO + 30), S.bar(C, LO + 30, C, HI), S.bar(C - 130, HI, C + 130, HI))


def _ok():
    return _parts(S.arc(C, C + 120, 230, 230, 200, 340), S.dot(C, C - 40, 40))


def _earth():
    # the ground line, with three furrows under it
    furrows = []
    for i in range(3):
        furrows += S.arc(LO + 110 + i * 190, C - 60, 70, 70, 200, 340)
    return _parts(S.bar(LO, C + 60, HI, C + 60), furrows)


def _hand():
    # the open hand: a palm that holds, and the fingers rising from it
    return _parts(S.arc(C, C + 60, 220, 240, 180, 360), S.bar(C, C - 180, C, HI - 40))


def _wood():
    # a tree: trunk, two branches and its roots
    return _parts(S.bar(C, LO + 40, C, HI), S.bar(C, C + 20, LO + 70, HI - 60), S.bar(C, C - 40, HI - 70, C + 140),
                  S.bar(LO + 40, LO + 40, HI - 40, LO + 40), S.tick(C - 120, LO + 40, 70, angle=270),
                  S.tick(C + 120, LO + 40, 70, angle=270))


def _pot():
    # a round-bellied pot: the body open at its shoulders, a flared neck and the rim
    cx, cy, r = C, C - 60, 220
    a0, a1 = math.radians(120), math.radians(60)
    lx, ly = cx + r * math.cos(a0), cy + r * math.sin(a0)
    rx, ry = cx + r * math.cos(a1), cy + r * math.sin(a1)
    return _parts(S.arc(cx, cy, r, r, 120, 420), S.bar(lx, ly, C - 160, HI - 30), S.bar(rx, ry, C + 160, HI - 30),
                  S.bar(C - 200, HI - 30, C + 200, HI - 30))


def _star():
    # eight short rays crossing at a point
    return _parts(S.bar(C, LO + 60, C, HI - 60), S.bar(LO + 60, C, HI - 60, C),
                  S.bar(C - 150, C - 150, C + 150, C + 150), S.bar(C - 150, C + 150, C + 150, C - 150))


def _stone():
    # a squat block of rock with a crack in it
    pts = [(LO + 40, LO + 60), (HI - 30, LO + 60), (HI, C), (HI - 90, HI - 90), (LO + 120, HI - 60), (LO, C + 20),
           (LO + 40, LO + 60)]
    return _parts(S.poly(pts), S.poly([(C - 40, HI - 75), (C + 10, C + 60), (C - 50, C - 10)]))


def _eye():
    # an open eye: the lids, the iris and the pupil
    return _parts(S.arc(C, C - 170, 300, 330, 35, 145), S.arc(C, C + 170, 300, 330, 215, 325), S.ring(C, C, 85),
                  S.dot(C, C, 30))


def _beside():
    # two uprights standing together on one ground
    return _parts(S.bar(C - 100, LO + 50, C - 100, HI - 40), S.bar(C + 100, LO + 50, C + 100, HI - 140),
                  S.bar(LO, LO + 50, HI, LO + 50))


def _chord_arc(x0, x1, y, sag):
    """An arc from (x0, y) to (x1, y) bowing ``sag`` units: up when positive, down when
    negative."""
    w, h = (x1 - x0) / 2, abs(sag)
    r = (w * w + h * h) / (2 * h)
    cx = (x0 + x1) / 2
    if sag > 0:
        cy = y - (r - h)
        a = math.degrees(math.asin(w / r))
        return S.arc(cx, cy, r, r, 90 - a, 90 + a)
    cy = y + (r - h)
    a = math.degrees(math.asin(w / r))
    return S.arc(cx, cy, r, r, 270 - a, 270 + a)


def _zero():
    # the shell: an empty thing, a deep bowl under a shallow lid, with its ribs. Grown, it
    # sits on the line and stands to Latin's x-height, as a small letter does.
    x0, x1, y = LO + 30, HI - 30, 380
    ribs = []
    for dx in (-100, 0, 100):
        ribs += S.bar(C + dx, y - 45, C + dx * 1.15, y - 190)
    return _parts(_chord_arc(x0, x1, y, -262), _chord_arc(x0, x1, y, 78), ribs)


def _glyph():
    # a folded screen of written leaves
    return _parts(S.poly([(LO + 40, LO + 30), (LO + 40, HI - 30), (HI - 40, HI - 30), (HI - 40, LO + 30), (LO + 40, LO + 30)]),
                  S.bar(C - 60, LO + 30, C - 60, HI - 30), S.bar(C + 90, LO + 30, C + 90, HI - 30),
                  S.bar(LO + 100, C + 110, C - 120, C + 110), S.bar(LO + 100, C - 30, C - 120, C - 30),
                  S.dot(C + 15, C + 40, 30))


def _blood():
    # a falling drop, and a second behind it
    return _parts(S.arc(C - 40, C - 70, 160, 160, 160, 380), S.bar(C - 40 - 150, C - 15, C - 40, HI - 40),
                  S.bar(C - 40 + 150, C - 15, C - 40, HI - 40), S.ring(HI - 90, LO + 70, 45))


def _numeral(n):
    """Bar-and-dot: a bar for each five, stacked from the bottom, and a dot for each one
    above them."""
    def draw():
        bars, dots = divmod(n, 5)
        out = []
        y = LO + 30
        for _ in range(bars):
            out += S.bar(LO + 40, y, HI - 40, y)
            y += 120
        if dots:
            gap = 120
            x0 = C - (dots - 1) * gap / 2
            out += [f for i in range(dots) for f in S.dot(x0 + i * gap, y + 20, 38)]
        return out
    return draw


def _sky():
    # the vault over the horizon, with a star in it
    return _parts(S.arc(C, LO + 60, 270, 470, 0, 180), S.bar(LO - 20, LO + 60, HI + 20, LO + 60), S.dot(C, C + 40, 36))


def _woman():
    # a person in a skirt: the head, the arms and the skirt's triangle
    return _parts(S.ring(C, HI - 90, 80), S.bar(C, HI - 170, C, C + 20), S.bar(LO + 80, C + 80, HI - 80, C + 80),
                  S.poly([(C, C + 20), (LO + 60, LO), (HI - 60, LO), (C, C + 20)]))


def _plant():
    # a stalk rising from the ground with two leaves and a head of grain
    return _parts(S.bar(LO, LO + 30, HI, LO + 30), S.bar(C, LO + 30, C, HI - 140), S.ring(C, HI - 70, 70),
                  S.arc(C - 120, C - 40, 120, 120, 0, 110), S.arc(C + 120, C + 40, 120, 120, 70, 180))


def _beast():
    # a four-footed animal in profile, facing the line's start: a curved back over a level
    # belly, legs in pairs fore and aft, the head raised on its neck, the tail curling up
    belly = C - 30
    return _parts(S.arc(C + 60, belly, 240, 170, 0, 180), S.bar(C - 180, belly, C + 300, belly),
                  S.bar(C - 130, belly, C - 150, LO), S.bar(C - 50, belly, C - 60, LO),
                  S.bar(C + 170, belly, C + 160, LO), S.bar(C + 250, belly, C + 260, LO),
                  S.bar(C - 180, belly + 20, LO + 70, C + 150), S.ring(LO + 40, C + 190, 62),
                  S.arc(HI - 10, belly + 120, 70, 110, 270, 400))


def _horizon_sun(rising):
    # the sun's half-disk on the horizon: over it, rising, with rays; under it, setting
    y = C - 40 if rising else C + 80
    a0, a1 = (0, 180) if rising else (180, 360)
    rays = []
    for a in (30, 90, 150):
        t = math.radians(a if rising else -a)
        rays += S.bar(C + 200 * math.cos(t), y + 200 * math.sin(t), C + 280 * math.cos(t), y + 280 * math.sin(t))
    return _parts(S.bar(LO - 20, y, HI + 20, y), S.arc(C, y, 140, 140, a0, a1), rays if rising else [])


def _quarter(up):
    # the four quarters, a cross, with the sun at the end of the arm named: at the
    # zenith for the north, under the world for the south
    y = HI - 70 if up else LO + 70
    return _parts(S.bar(C, LO + 140 if up else LO + 140, C, HI - 140), S.bar(LO, C, HI, C), S.ring(C, y, 70))


def _low():
    return _parts(S.bar(LO, C + 90, HI, C + 90), S.dot(C, C - 130, 58))


def _inside():
    # a thing within an enclosure
    return _parts(S.poly([(LO + 40, LO + 40), (LO + 40, HI - 40), (HI - 40, HI - 40), (HI - 40, LO + 40), (LO + 40, LO + 40)]),
                  S.dot(C, C, 50))


def _outside():
    # a thing beyond an enclosure open to it
    return _parts(S.poly([(C + 60, HI - 40), (LO + 40, HI - 40), (LO + 40, LO + 40), (C + 60, LO + 40)]),
                  S.bar(C + 60, HI - 40, C + 60, C + 90), S.bar(C + 60, LO + 40, C + 60, C - 90), S.dot(HI - 30, C, 50))


def _house():
    # shelter: a roof, and what it keeps under it
    return _parts(S.poly([(LO, LO + 60), (C, HI - 20), (HI, LO + 60)]), S.dot(C, LO + 130, 50))


def _mouth():
    # the open mouth: a plain ring
    return S.ring(C, C, 190)


def _danger():
    # fangs: a row of sharp points, angular where water's waves are round
    return S.poly([(LO, C - 120), (LO + 95, C + 130), (LO + 190, C - 120), (C, C + 130), (HI - 190, C - 120),
                   (HI - 95, C + 130), (HI, C - 120)])


# -- the core: the 24 glyphs nearly everyone knows -----------------------------------------------

SUN = Glyph("SUN", "the sun; light, revelation, authority", "ts'en", "tse", _sun, "core")
MOON = Glyph("MOON", "the moon; night, cycles, hidden things", "ish'uqal", "i", _moon, "core")
SKY = Glyph("SKY", "the sky, the heavens; divinity", "h'ulal", "hu", _sky, "core")
STAR = Glyph("STAR", "a star; fate, guidance, destiny", "ish'ilan", "i", _star, "core")
WATER = Glyph("WATER", "water; flow, cleansing, change", "ne'", "ne", _water, "core")
FIRE = Glyph("FIRE", "fire; heat, destruction, purification", "k'ayumel", "ka", _flame, "core")
EARTH = Glyph("EARTH", "earth, soil; fertility, foundation", "sh'akan", "sha", _earth, "core")
STONE = Glyph("STONE", "stone, mountain; permanence, strength", "kulum", "ku", _stone, "core")
MAN = Glyph("MAN", "a person, a man; manhood, fatherhood", "ch'ekbal cham", "che", _person, "core")
WOMAN = Glyph("WOMAN", "a woman; womanhood, motherhood", "ch'ekbal ishal", "che", _woman, "core")
PLANT = Glyph("PLANT", "vegetation; growth, cultivation", "shik", "shi", _plant, "core")
BEAST = Glyph("BEAST", "an animal; instinct, wilderness, flesh", "ch'ekum", "che", _beast, "core")
EAST = Glyph("EAST", "the east, sunrise; birth, beginning", "ts'en ch'ulun", "tse", lambda: _horizon_sun(True), "core")
WEST = Glyph("WEST", "the west, sunset; death, ending", "ts'en ishan", "tse", lambda: _horizon_sun(False), "core")
NORTH = Glyph("NORTH", "the north, the zenith; the world above, the gods and the honoured dead", "nukal", "nu", lambda: _quarter(True), "core")
SOUTH = Glyph("SOUTH", "the south, the nadir; the world below, the underworld and its trials", "toshal", "to", lambda: _quarter(False), "core")
HIGH = Glyph("HIGH", "above, greater; age, rank", "ts'ikik", "tsi", _above, "core")
LOW = Glyph("LOW", "below, lesser; youth, humility", "ch'alik", "cha", _low, "core")
INSIDE = Glyph("INSIDE", "within; hidden, belonging", "ch'ikal", "chi", _inside, "core")
OUTSIDE = Glyph("OUTSIDE", "beyond; foreign, exposed", "ts'ikal", "tsi", _outside, "core")
HOUSE = Glyph("HOUSE", "a house, shelter; family, community", "sh'ulum", "shu", _house, "core")
HAND = Glyph("HAND", "a hand; work, action, possession", "p'ishum", "pi", _hand, "core")
EYE = Glyph("EYE", "the eye; sight, knowledge, witness", "k'ayikash", "ka", _eye, "core")
MOUTH = Glyph("MOUTH", "the mouth; speech, naming", "nalak", "na", _mouth, "core")

CORE = [SUN, MOON, SKY, STAR, WATER, FIRE, EARTH, STONE, MAN, WOMAN, PLANT, BEAST, EAST, WEST, NORTH, SOUTH,
        HIGH, LOW, INSIDE, OUTSIDE, HOUSE, HAND, EYE, MOUTH]
CATEGORIES = [("The cosmos", CORE[0:4]), ("The world", CORE[4:8]), ("Living things", CORE[8:12]),
              ("The quarters", CORE[12:16]), ("Relations", CORE[16:20]), ("Human life", CORE[20:24])]

# -- beyond the core: glyphs a trade or a scribe knows -------------------------------------------

RIVER = Glyph("RIVER", "a river", "ha'nal", "ha", _river)
PEAK = Glyph("PEAK", "a sacred peak, a pyramid", "kul'qat", "ku", _peak, "sacred")
STEPS = Glyph("STEPS", "a stair; to climb", "pu'tal", "pu", _steps)
JAGUAR = Glyph("JAGUAR", "a jaguar", "ish'bal", "i", _jaguar)
SERPENT = Glyph("SERPENT", "a serpent", "ch'akun", "cha", _serpent)
POT = Glyph("POT", "a pot", "lu'she", "lu", _pot, "trade:potter")
WOOD = Glyph("WOOD", "wood, a tree", "shikum", "shi", _wood, "trade:carpenter")
BLOOD = Glyph("BLOOD", "blood; the offering", "ts'umulal", "tsu", _blood, "sacred")
GLYPH = Glyph("GLYPH", "a glyph; a codex", "p'ilam", "pi", _glyph)
BESIDE = Glyph("BESIDE", "beside", "p'ishalash", "pi", _beside)
TOWARD = Glyph("TOWARD", "toward", "ch'ul", "chu", _toward)
ALL = Glyph("ALL", "all", "kesh", "ke", _all)
BEING = Glyph("BEING", "to be", "k'alish", "ka", _being)
DANGER = Glyph("DANGER", "danger; a threat, beware", "shok'ul", "sho", _danger)
OK = Glyph("OK", "the ending -ok: having, running with", "-ok", "o", _ok)
ZERO = Glyph("ZERO", "zero; the shell, an empty thing; nothing", "ts'amal", "tsa", _zero)

METAL = Glyph("METAL", "metal; iron, steel", "kulishal", "ku", lambda: _metal())


# -- the sound glyphs: every syllable Ki'i'chek uses has at least one glyph ----------------------


def _diamond(bars):
    pts = [(C, HI - 10), (HI - 30, C), (C, LO + 10), (LO + 30, C), (C, HI - 10)]
    out = S.poly(pts)
    span = 300
    for k in range(bars):
        y = C + span / 2 - (k + 0.5) * span / bars if bars > 1 else C
        half = (span / 2 - abs(y - C)) * 0.95 + 40
        out += S.bar(C - half, y, C + half, y)
    return out


def _metal():
    # an ingot, struck through
    return _parts(S.poly([(LO + 40, LO + 120), (HI - 40, LO + 120), (HI - 130, HI - 140), (LO + 130, HI - 140),
                          (LO + 40, LO + 120)]), S.bar(LO + 110, C - 10, HI - 110, C - 10))


def _lord():
    # a head crowned with three plumes
    return _parts(S.ring(C, C - 80, 130), S.tick(C - 80, C + 70, 160, angle=110), S.tick(C, C + 70, 170),
                  S.tick(C + 80, C + 70, 160, angle=70))


def _light():
    # light falling: a point, and three rays spreading down from it
    return _parts(S.dot(C, HI - 70, 52), S.bar(C - 50, HI - 150, LO + 40, LO + 40), S.bar(C, HI - 150, C, LO + 20),
                  S.bar(C + 50, HI - 150, HI - 40, LO + 40))


def _coyote():
    # a pointed face: the muzzle's point and two ears
    return S.poly([(LO + 40, HI - 20), (LO + 150, C + 80), (HI - 150, C + 80), (HI - 40, HI - 20)]) + \
        S.poly([(LO + 150, C + 80), (C, LO + 30), (HI - 150, C + 80)])


def _edge():
    # an edge, a joining: a turn with a point set in its angle
    return _parts(S.corner(LO + 40, HI - 60, HI - 60, LO + 40), S.dot(HI - 210, HI - 210, 50))


def _self():
    # the one speaking: a head on its stem
    return _parts(S.ring(C, HI - 140, 100), S.bar(C, HI - 240, C, LO + 20))


def _you():
    # the one spoken to: a head on its stem, turned toward the line's end
    return _parts(S.ring(C - 60, HI - 140, 100), S.bar(C - 60, HI - 240, C - 60, LO + 20),
                  S.bar(C + 60, HI - 140, HI - 20, HI - 140))


def _bird():
    # a bird in flight: two wings meeting at its body
    return _parts(S.arc(C - 150, C - 40, 150, 160, 20, 160), S.arc(C + 150, C - 40, 150, 160, 20, 160))


def _quetzal():
    # a bird with a long trailing plume
    return _parts(S.ring(LO + 110, HI - 120, 70), S.arc(LO + 520, HI - 120, 400, 520, 180, 270),
                  S.arc(LO + 520, HI - 180, 300, 400, 180, 265))


def _war():
    # two weapons crossed
    return _parts(S.bar(LO + 40, LO + 40, HI - 40, HI - 40), S.bar(LO + 40, HI - 40, HI - 40, LO + 40))


def _affection():
    # two rings joined
    return _parts(S.ring(C - 100, C, 150), S.ring(C + 100, C, 150))


def _supreme():
    # above all: two points stacked over the line
    return _parts(S.bar(LO, LO + 120, HI, LO + 120), S.dot(C, C, 52), S.dot(C, HI - 60, 52))


def _maize():
    # an ear of maize in its husk: the ear, its rows, and the leaves at its foot
    return _parts(S.frame(C - 110, C - 70, 220, HI - C + 50, square=2.2), S.bar(C, C - 30, C, HI - 60),
                  S.arc(C - 160, LO + 40, 150, 180, 20, 90), S.arc(C + 160, LO + 40, 150, 180, 90, 160))


def _cord():
    # a knotted cord hanging from its bar
    return _parts(S.bar(LO + 60, HI - 30, HI - 60, HI - 30), S.bar(C, HI - 30, C, LO + 20), S.dot(C, C + 120, 48),
                  S.dot(C, C - 30, 48), S.dot(C, LO + 140, 48))


def _bear():
    # a heavy body, low on two thick legs, its round ears up
    return _parts(S.arc(C, C - 40, 250, 230, 0, 180), S.bar(LO + 60, C - 40, HI - 60, C - 40),
                  S.bar(C - 120, C - 40, C - 120, LO + 30), S.bar(C + 120, C - 40, C + 120, LO + 30),
                  S.ring(C - 150, C + 210, 50), S.ring(C + 150, C + 210, 50))


def _jade():
    # a pierced bead
    return _parts(S.ring(C, C, 210), S.ring(C, C, 70))


def _obsidian():
    # a blade: a long leaf of glass with its ridge
    return _parts(S.arc(C + 300, C, 420, 290, 136, 224), S.arc(C - 300, C, 420, 290, -44, 44),
                  S.bar(C, LO + 40, C, HI - 40))


def _feather():
    # a quill with its barbs on one side
    barbs = []
    for k in range(4):
        y = C - 120 + k * 90
        barbs += S.bar(C, y, C + 170, y + 110)
    return _parts(S.bar(C, LO + 20, C, HI - 20), barbs)


def _drum():
    # an upright drum: its body and its stretched head
    return _parts(S.poly([(C - 150, HI - 60), (C - 110, LO + 30), (C + 110, LO + 30), (C + 150, HI - 60),
                          (C - 150, HI - 60)]), S.bar(C - 150, HI - 140, C + 150, HI - 140))


def _turtle():
    # a domed shell over its belly, the head out toward the line's start, two feet
    return _parts(S.arc(C + 30, C - 60, 230, 230, 0, 180), S.bar(C - 200, C - 60, HI - 40, C - 60),
                  S.ring(LO + 50, C - 10, 50), S.tick(C - 90, C - 60, 110, angle=250), S.tick(C + 150, C - 60, 110, angle=290))


def _canoe():
    # a long shallow hull, its ends raised
    return _parts(S.arc(C, C + 120, 300, 220, 200, 340), S.bar(LO - 10, C + 120, LO + 60, C + 40 - 10),
                  S.bar(HI + 10, C + 120, HI - 60, C + 30))


def _incense():
    # smoke rising from a bowl
    smoke = []
    for dx in (-80, 80):
        pts = [(C + dx + 40 * math.sin(2 * math.pi * k / 30 * 1.5), C - 20 + k * (HI - C + 0) / 30) for k in range(31)]
        smoke += S.poly(pts)
    return _parts(S.arc(C, LO + 180, 210, 150, 200, 340), S.bar(C - 200, LO + 180 - 50, C + 200, LO + 180 - 50), smoke)


def _mat():
    # the woven mat: a square of interlaced strands
    out = S.poly([(LO + 40, LO + 40), (LO + 40, HI - 40), (HI - 40, HI - 40), (HI - 40, LO + 40), (LO + 40, LO + 40)])
    for k in (1, 2):
        t = LO + 40 + k * (HI - LO - 80) / 3
        out += S.bar(t, LO + 40, t, HI - 40) + S.bar(LO + 40, t, HI - 40, t)
    return out


def _salt():
    # a heap of grains
    return _parts(S.dot(C - 120, C - 80, 54), S.dot(C + 120, C - 80, 54), S.dot(C, C + 110, 54))


def _ball():
    # the ball, its band
    return _parts(S.ring(C, C, 220), S.bar(C - 220, C, C + 220, C))


def _monkey():
    # a head on a body ending in a curled tail
    return _parts(S.ring(C - 60, HI - 100, 80), S.bar(C - 60, HI - 180, C - 60, C - 60), S.curl(C + 70, C - 140, 130))


def _bat():
    # a body between two pointed wings
    return _parts(S.dot(C, C + 40, 52), S.poly([(C - 70, C + 40), (LO, HI - 60), (LO + 60, C - 60), (C - 70, C + 40)]),
                  S.poly([(C + 70, C + 40), (HI, HI - 60), (HI - 60, C - 60), (C + 70, C + 40)]))


def _net():
    # a bag of crossed meshes
    out = S.arc(C, HI - 60, 260, 470, 180, 360)
    for k in (-1, 1):
        out += S.bar(C + k * 110 - 120, HI - 60, C + k * 110 + 120, LO + 130)
        out += S.bar(C + k * 110 + 120, HI - 60, C + k * 110 - 120, LO + 130)
    return out


def _hummingbird():
    # a small body, a long straight bill toward the line's start, a raised wing
    return _parts(S.ring(C + 80, C, 90), S.bar(C - 10, C + 20, LO - 10, C + 60), S.arc(C + 160, C + 120, 120, 160, 100, 200))


def _shield():
    # a round shield with its fringe hanging below
    return _parts(S.ring(C, C + 70, 190), S.bar(C - 100, C - 110, C - 120, LO + 10), S.bar(C, C - 120, C, LO),
                  S.bar(C + 100, C - 110, C + 120, LO + 10))


def _deer():
    # a head crowned with branching antlers
    return _parts(S.ring(C, LO + 130, 85), S.bar(C - 60, LO + 200, C - 160, HI - 40), S.bar(C - 115, C + 110, C - 220, C + 160),
                  S.bar(C + 60, LO + 200, C + 160, HI - 40), S.bar(C + 115, C + 110, C + 220, C + 160))


def _mask():
    # a face put on: its outline and the eye-slits
    return _parts(S.frame(LO + 60, LO + 30, HI - LO - 120, HI - LO - 60, square=2.4), S.bar(C - 140, C + 60, C - 40, C + 60),
                  S.bar(C + 40, C + 60, C + 140, C + 60))


LORD = Glyph("LORD", "a lord; sovereignty", "mah", "ma", _lord)
LIGHT = Glyph("LIGHT", "light, brightness", "k'inish", "ki", _light)
COYOTE = Glyph("COYOTE", "a coyote", "ts'okum", "tso", _coyote, "trade:hunter")
EDGE = Glyph("EDGE", "an edge, a joining; the 260-day count", "tq'an", "qa", _edge, "sacred")
SELF = Glyph("SELF", "I, the speaker", "ni", "ni", _self)
YOU = Glyph("YOU", "you, the one addressed", "ti", "ti", _you)
BIRD = Glyph("BIRD", "a bird", "shelem", "she", _bird)
QUETZAL = Glyph("QUETZAL", "the quetzal; its plumes, rank", "p'ashel", "pa", _quetzal, "sacred")
WAR = Glyph("WAR", "war, a campaign", "shok'al", "sho", _war)
AFFECTION = Glyph("AFFECTION", "affection, fondness", "ashal", "a", _affection)
SUPREME = Glyph("SUPREME", "supreme; an overlord", "q'emul", "qe", _supreme)
MAIZE = Glyph("MAIZE", "maize", "ul'om", "u", _maize)
CORD = Glyph("CORD", "cord; the knotted records", "k'otsik", "ko", _cord)
BEAR = Glyph("BEAR", "a bear", "no'kin", "no", _bear, "trade:hunter")

JADE = Glyph("JADE", "jade; the precious, the green", "", "la", _jade, "sacred", True)
OBSIDIAN = Glyph("OBSIDIAN", "obsidian; the ritual blade, the mirror", "", "ba", _obsidian, "sacred", True)
FEATHER = Glyph("FEATHER", "a feather; lightness, rank", "", "ta", _feather, "general", True)
DRUM = Glyph("DRUM", "a drum; summons, the dance", "", "le", _drum, "general", True)
TURTLE = Glyph("TURTLE", "a turtle; the earth's shell", "", "me", _turtle, "general", True)
CANOE = Glyph("CANOE", "a canoe; river travel", "", "mi", _canoe, "trade:boatman", True)
INCENSE = Glyph("INCENSE", "incense; offering smoke", "", "yi", _incense, "sacred", True)
MAT = Glyph("MAT", "the woven mat; the seat of rule", "", "yu", _mat, "sacred", True)
SALT = Glyph("SALT", "salt", "", "tu", _salt, "trade:merchant", True)
BALL = Glyph("BALL", "the ball; the ball game", "", "te", _ball, "general", True)
MONKEY = Glyph("MONKEY", "a monkey; the arts, mischief", "", "ya", _monkey, "general", True)
BAT = Glyph("BAT", "a bat; the night's messenger", "", "ye", _bat, "general", True)
NET = Glyph("NET", "a net; catching, gathering", "", "bi", _net, "trade:fisher", True)
HUMMINGBIRD = Glyph("HUMMINGBIRD", "a hummingbird; the warrior's soul", "", "lo", _hummingbird, "general", True)
SHIELD = Glyph("SHIELD", "a shield; defence", "", "hi", _shield, "trade:warrior", True)
DEER = Glyph("DEER", "a deer; the hunt", "", "he", _deer, "trade:hunter", True)
MASK = Glyph("MASK", "a mask; a face put on, a god worn", "", "be", _mask, "sacred", True)

# The syllables Ki'i'chek's lexicon uses: 63 of the 70 its consonants and vowels allow. It never
# uses cho, mo, bo, bu, ho, yo or a bare e, and those have no glyph.
SYLLABLES = ("a i o u "
             "ka ke ki ko ku cha che chi chu tsa tse tsi tso tsu pa pe pi po pu qa qe qi qo qu ta te ti to tu "
             "sha she shi sho shu la le li lo lu ma me mi mu na ne ni no nu ba be bi ha he hi hu ya ye yi yu").split()

FROM_WORDS = [LORD, LIGHT, COYOTE, EDGE, SELF, YOU, BIRD, QUETZAL, WAR, AFFECTION, SUPREME, MAIZE, CORD, BEAR]
TRADITIONAL = [JADE, OBSIDIAN, FEATHER, DRUM, TURTLE, CANOE, INCENSE, MAT, SALT, BALL, MONKEY, BAT, NET, HUMMINGBIRD,
               SHIELD, DEER, MASK]

OUTER = [RIVER, PEAK, STEPS, JAGUAR, SERPENT, POT, WOOD, BLOOD, GLYPH, BESIDE, TOWARD, ALL, BEING, OK, DANGER]
GLYPHS = CORE + OUTER + [METAL] + FROM_WORDS + TRADITIONAL + [ZERO]

NUMBER_WORDS = ["pe'", "q'o", "lishe", "mushe", "p'o", "ts'ishe", "nuq'el", "q'ishe", "pek'ash", "olek'"]


def _number_word(n):
    return NUMBER_WORDS[n - 1] if n <= 10 else f"olek' {NUMBER_WORDS[n - 11]}"


def _opening(word):
    w = word.replace("'", "")
    for c in ("ch", "sh", "ts", "k", "p", "q", "t", "l", "m", "n", "b", "h", "y"):
        if w.startswith(c):
            return c + w[len(c)]
    return w[0]


NUMERALS = [Glyph(f"N{n}", f"{n}", _number_word(n), _opening(_number_word(n)), _numeral(n), "core")
            for n in range(1, 20)]
N = {g.name: g for g in NUMERALS}

# The places of the count: twenty, then each power of twenty, a diamond holding one bar more.
PLACES = [Glyph(f"P{v}", f"{v:,}", w, _opening(w), (lambda k: lambda: _diamond(k))(k + 1), "core")
          for k, (v, w) in enumerate([(20, "ts'ob"), (400, "pel'ush"), (8000, "q'umpel"), (160000, "sholemash")])]


def cell(glyph):
    """One cell: the glyph."""
    return glyph.draw()


# -- compounds ----------------------------------------------------------------------------------


@dataclass(frozen=True)
class Word:
    word: str  # what it means
    gloss: str  # the Ki'i'chek, where the lexicon has it
    glyphs: tuple
    why: str = ""


COMPOUNDS = [
    Word("kinsman", "", (MAN, INSIDE)), Word("stranger", "", (MAN, OUTSIDE)),
    Word("home", "", (HOUSE, INSIDE)), Word("village", "", (HOUSE, OUTSIDE)),
    Word("memory", "", (EYE, INSIDE)), Word("observation", "", (EYE, OUTSIDE)),
    Word("a secret", "", (MOUTH, INSIDE)), Word("proclamation", "", (MOUTH, OUTSIDE)),
    Word("heaven", "", (SKY, INSIDE)), Word("the unknown beyond creation", "", (SKY, OUTSIDE)),
    Word("boy, servant", "", (MAN, LOW)), Word("girl, servant", "", (WOMAN, LOW)),
    Word("elder, chief", "", (MAN, HIGH)), Word("elder woman, noblewoman", "", (WOMAN, HIGH)),
    Word("people", "", (MAN, MAN)), Word("women", "", (WOMAN, WOMAN)),
    Word("couple, marriage", "", (MAN, WOMAN)), Word("family", "", (MAN, WOMAN, HOUSE)),
    Word("patriarch", "", (MAN, HIGH, HOUSE)), Word("matriarch", "", (WOMAN, HIGH, HOUSE)),
    Word("son", "", (MAN, LOW, HOUSE)), Word("daughter", "", (WOMAN, LOW, HOUSE)),
    Word("god, exalted ancestor", "", (MAN, HIGH, SKY)),
    Word("birth of a boy", "", (MAN, EAST)), Word("birth of a girl", "", (WOMAN, EAST)),
    Word("death of a man", "", (MAN, WEST)), Word("death of a woman", "", (WOMAN, WEST)),
    Word("founding a household", "", (HOUSE, EAST)), Word("end of a household", "", (HOUSE, WEST)),
    Word("dawn", "", (SUN, EAST)), Word("sunset", "", (SUN, WEST)),
    Word("germination", "", (PLANT, EAST)), Word("harvest, withering", "", (PLANT, WEST)),
    Word("a lifetime", "", (EAST, WEST)), Word("rebirth", "", (WEST, EAST)),
    Word("an era begins", "", (EAST, HIGH)), Word("an era ends", "", (WEST, HIGH)),
    Word("caution", "", (DANGER, LOW)),
    Word("writing, craft", "", (HAND, EYE)), Word("prayer, prophecy", "", (MOUTH, SKY)),
    Word("an exalted ancestor", "", (MAN, NORTH)), Word("a soul among the dead", "", (MAN, SOUTH)),
    Word("a cenote", "", (WATER, SOUTH)),
    Word("noon", "", (SUN, NORTH)), Word("midnight", "", (SUN, SOUTH)),
    Word("the passage of the dead", "", (WEST, SOUTH)), Word("coming out of the trials", "", (SOUTH, EAST)),
    Word("a seed sown", "", (PLANT, SOUTH)),
    Word("the whole round: the sun's day, the soul's existence", "", (EAST, NORTH, WEST, SOUTH)),
]

SPELLINGS = [
    Word("K'ushi", "a man's name", (STONE, PLANT), "ku-shi"),
    Word("Ch'akul", "a man's name", (SERPENT, STONE, POT), "cha-ku-l(u): the last vowel is silent"),
]


# -- the passage: a night's entry at the sighting stones ----------------------------------------------
#
# The Faith of Ish'ilan Ch'alish keeps a record of every night at the sighting stones, whether or
# not anything happens. Each entry is a record of meaning, not of words.

PRIEST = (MAN, MOUTH, SKY)  # the one who prays
STAR_PRIEST = PRIEST + (STAR,)  # a four-glyph compound, a scribe's

PASSAGE = [
    ("night, the thirteenth", (MOON, N["N13"])),
    ("the star-priest", STAR_PRIEST),
    ("Ts'alam, by sound: tsa-la-m(a)", (ZERO, JADE, LORD)),
    ("at the sighting stones", (STONE, EYE)),
    ("the moon rises", (MOON, EAST)),
    ("over the mountain", (HIGH, STONE)),
    ("a star beside the moon", (STAR, BESIDE, MOON)),
    ("the priest observes", PRIEST + (EYE, OUTSIDE)),
    ("nothing happens", (ZERO,)),
    ("the priest writes", PRIEST + (HAND, EYE)),
    ("blood on the writing", (BLOOD, HAND, EYE)),
    ("night, the fourteenth", (MOON, N["N14"])),
    ("the star-priest", STAR_PRIEST),
    ("at the sighting stones", (STONE, EYE)),
    ("the moon rises", (MOON, EAST)),
    ("nothing happens", (ZERO,)),
    ("the priest writes", PRIEST + (HAND, EYE)),
]


def passage_glyphs():
    return [g for _, gs in PASSAGE for g in gs]
