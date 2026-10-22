# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""The Veldikko letters and marks, as data over the stroke generator.

    import letters as L

    glyph = L.glyph("t", L.S.HAND, marks="a:")    # t with a long a over it
    path = L.S.outline(glyph.tracks, L.S.HAND)     # a pathops.Path, font units, y up
    word = L.word("k+a l p+i", L.S.HAND)           # kalpi, set right to left with touches

A letter is a stem at one of three grades and a bowl, or a stemless stroke. The
bowl names the place of articulation, the stem's height names the grade, and a
standing bowl turned over to hang names a voiced sound. Two Áelendan ligatures
extend the set: the breath, the hanging coil of _h_ written small at the head of
a stop for an aspirate, and the catch, the length bar laid across a stop's stem
for an ejective.

Marks float over the letter they follow: a vowel mark, drawn long for a long
vowel, with a pitch flick at its forward end; a diphthong is two marks in the
order they are said; the brow over a mark is emphasis; and the length bar under
a letter doubles its consonant.
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import strokes as S  # noqa: E402

# -- the stems ---------------------------------------------------------------------------------

GRADES = {
    "stop": {"top": S.ASC},  # raised: its head far above the bowl
    "fricative": {"top": S.X + 60},  # level: its head just clears the bowl
    "nasal": {"top": S.X + 60, "foot": S.DESC, "tail": 0},  # lowered, into a hooked tail
}


@dataclass(frozen=True)
class Letter:
    id: str  # the romanized spelling the letter is set from
    sound: str  # what it sounds like, in a few words
    family: str  # lips, tongue-tip, back, liquid, carrier
    form: str  # the stroke it is built on
    grade: str | None = None  # stop, fricative, nasal; None for a stemless letter
    voiced: bool = False
    breath: bool = False  # the aspirate's ligature: h's coil at the head of the stem
    catch: bool = False  # the ejective's ligature: the bar across the stem
    tongues: tuple = ("sinale", "aelendi")  # who writes it

    @property
    def hangs(self):
        return self.form.startswith("hung-")


def _l(id, sound, family, form, grade=None, **kw):
    return id, Letter(id, sound, family, form, grade, **kw)


SIN, AEL, BOTH = ("sinale",), ("aelendi",), ("sinale", "aelendi")

LETTERS: dict[str, Letter] = dict([
    # the lips: the bud, standing
    _l("p", "lips, stop", "lips", "bud", "stop"),
    _l("v", "lips, fricative", "lips", "bud", "fricative", tongues=SIN),
    _l("m", "lips, nasal", "lips", "bud", "nasal"),
    # the tongue-tip: arches on a floor, standing
    _l("t", "tongue-tip, stop", "tongue-tip", "arches", "stop"),
    _l("s", "tongue-tip, fricative", "tongue-tip", "arches", "fricative"),
    _l("n", "tongue-tip, nasal", "tongue-tip", "arches", "nasal"),
    # voiced tongue-tip: the arches turned over
    _l("d", "tongue-tip, voiced stop", "tongue-tip", "hung-arches", "stop", voiced=True),
    _l("dh", "tongue-tip, voiced fricative", "tongue-tip", "hung-arches", "fricative", voiced=True, tongues=SIN),
    # the back: the coil, hanging
    _l("k", "back, stop", "back", "hung-coil", "stop"),
    _l("h", "back, fricative", "back", "hung-coil", "fricative", tongues=SIN),
    _l("ng", "back, nasal", "back", "hung-coil", "nasal"),
    # voiced back: the coil turned over to stand
    _l("g", "back, voiced stop", "back", "coil", "stop", voiced=True, tongues=AEL),
    # outside the families
    _l("l", "liquid", "liquid", "riser"),
    _l("r", "liquid", "liquid", "crook"),
    _l("_", "the carrier: no sound", "carrier", "carrier"),
    # the Áelendan aspirates: a stop with the breath at its head
    _l("th", "tongue-tip, aspirated stop", "tongue-tip", "arches", "stop", breath=True, tongues=AEL),
    _l("kh", "back, aspirated stop", "back", "hung-coil", "stop", breath=True, tongues=AEL),
    _l("dhA", "tongue-tip, voiced aspirated stop", "tongue-tip", "hung-arches", "stop", voiced=True, breath=True,
       tongues=AEL),
    _l("gh", "back, voiced aspirated stop", "back", "coil", "stop", voiced=True, breath=True, tongues=AEL),
    # the Áelendan ejectives: a stop with the catch across its stem
    _l("t'", "tongue-tip, ejective", "tongue-tip", "arches", "stop", catch=True, tongues=AEL),
    _l("d'", "tongue-tip, voiced ejective", "tongue-tip", "hung-arches", "stop", voiced=True, catch=True, tongues=AEL),
    _l("k'", "back, ejective", "back", "hung-coil", "stop", catch=True, tongues=AEL),
    _l("g'", "back, voiced ejective", "back", "coil", "stop", voiced=True, catch=True, tongues=AEL),
])

# The romanized spelling of the Áelendan aspirate written dh, which is a stop, beside
# Sinale's dh, the voiced fricative. A spelling resolves to a letter by tongue.
SPELLING = {"aelendi": {"dh": "dhA"}}


def letter(spelling: str, tongue: str = "sinale") -> Letter:
    return LETTERS[SPELLING.get(tongue, {}).get(spelling, spelling)]


# -- the vowel marks ---------------------------------------------------------------------------

VOWELS = {"a": "one", "o": "two", "u": "three", "e": "dab", "i": "backdab", "y": "hook", "ë": "curl"}
SETS = {"a": "back", "o": "back", "u": "back", "e": "neutral", "i": "neutral", "y": "front", "ë": "front"}


@dataclass(frozen=True)
class Mark:
    vowel: str
    long: bool = False
    pitch: float = 0.0  # +1 a rise, -1 a fall
    emphasis: bool = False


def parse_marks(text: str) -> list[Mark]:
    """``"a"``, ``"a:"`` (long), ``"a/"`` (rising), ``"a\\"`` (falling), ``"a!"``
    (emphasis), and ``"ei"`` (a diphthong, two marks in the order said)."""
    out, i = [], 0
    while i < len(text):
        v = text[i]
        if v not in VOWELS:
            raise ValueError(f"{text!r}: {v!r} is not a vowel; the marks are {''.join(VOWELS)}")
        i += 1
        long, pitch, emph = False, 0.0, False
        while i < len(text) and text[i] in ":/\\!":
            c = text[i]
            long |= c == ":"
            pitch = 1.0 if c == "/" else -1.0 if c == "\\" else pitch
            emph |= c == "!"
            i += 1
        out.append(Mark(v, long, pitch, emph))
    return out


# -- the parts of a letter ---------------------------------------------------------------------

# Where a mark sits over each form: the fraction of the bowl's width forward of the stem
# at the middle of what the eye reads as the bowl.
ANCHOR = {"bud": 0.60, "arches": 0.57, "coil": 0.56, "hung-bud": 0.60, "hung-arches": 0.57, "hung-coil": 0.56,
          "crook": 0.45, "carrier": 0.0}
WIDTH = {sid: S.STROKES[sid].params["w"][1] for sid in ANCHOR if "w" in S.STROKES[sid].params}
BESIDE = 60.0  # the clearance between the riser and the mark set forward of it
MARK_GAP = 130.0  # the least clearance between a bowl's top line and the mark over it
BREATH = 0.48  # the scale the breath's coil is drawn at


def _lean(style):
    return math.tan(math.radians(style.slant))


def _stem_without_head(sh: S.Shape, top: float) -> S.Shape:
    """A stem with its vine curl cut away, so a ligature can take the head: the track
    begins at the top of the fall, set down from nothing."""
    t = sh.tracks[0]
    i = next(k for k, (f, y, _) in enumerate(t.samples) if abs(y - top) < 0.6 and abs(f) < 0.6)
    n = S.Track(0, 0, 0)
    n.samples = t.samples[i:]
    S._land(n, 0.06)
    return S.Shape([n], sh.entry, sh.exit)


def _breath(top: float, fl: float) -> list:
    """The aspirate's ligature: h's hanging coil, drawn small, hung from the stem's head."""
    sh = S.s_hung_coil(0, 0, fl)
    k, hang = BREATH, S.HANG
    tracks = []
    for t in sh.tracks:
        n = S.Track(0, 0, 0)
        n.samples = [(f * k, top + 6 + (y - hang) * k, p) for f, y, p in t.samples]
        tracks.append(n)
    return tracks


def _catch(stem: S.Shape, top: float, style) -> list:
    """The ejective's ligature: the length bar laid across the stem, two thirds up."""
    y = 0.62 * top
    f = min(stem.tracks[0].samples, key=lambda s: abs(s[1] - y))[0]
    return S.shape("bar", f, y, style, l=120, tilt=-24).tracks


@dataclass
class Glyph:
    """A letter's tracks in the forward frame, with the extent the next letter is set
    against and the point a touch leaves from."""

    tracks: list
    lo: float  # the backmost extent, in page-equivalent forward units (f + y·lean)
    hi: float  # the foremost extent
    exit: tuple  # where a touch to the next letter leaves
    mark_at: tuple = (0.0, S.MARK)  # the page-equivalent middle of the marks, and their floor
    bar_at: float = 0.0  # the page-equivalent middle of the length bar


def _parts(lt: Letter, style: S.Style):
    """The stem shape (or None) and the bowl shape, at the origin."""
    fl = style.flourish
    stem = None
    if lt.grade:
        stem = S.shape("stem", 0, 0, style, **GRADES[lt.grade])
        if lt.breath:
            stem = _stem_without_head(stem, GRADES[lt.grade]["top"])
    bowl = S.shape(lt.form, 0, 0, style)
    return stem, bowl, fl


def glyph(spelling: str | Letter, style: S.Style = S.HAND, marks: str | list = "", bar: bool = False,
          tongue: str = "sinale") -> Glyph:
    """One letter in its isolated form, with its marks, at the origin."""
    lt = spelling if isinstance(spelling, Letter) else letter(spelling, tongue)
    stem, bowl, fl = _parts(lt, style)
    lean = _lean(style)
    tracks = list(bowl.tracks)
    if stem:
        tracks = stem.tracks + tracks
        top = GRADES[lt.grade]["top"]
        if lt.breath:
            tracks += _breath(top, fl)
        if lt.catch:
            tracks += _catch(stem, top, style)
    pts = [(f + y * lean, y) for t in tracks for f, y, _ in t.samples]
    lo, hi = min(p[0] for p in pts), max(p[0] for p in pts)

    # The mark's point: over the middle of the bowl, clear of its top.
    body = [(f, y) for t in bowl.tracks for f, y, _ in t.samples]
    top_y = max(y for _, y in body)
    mid_y = (max(y for _, y in body) + max(0.0, min(y for _, y in body))) / 2
    y_mark = max(S.MARK, top_y + MARK_GAP)
    anchor = ANCHOR.get(lt.form, 0.0) * WIDTH.get(lt.form, 0) + mid_y * lean  # page-equivalent
    bar_at = anchor
    if lt.form == "riser":  # it rises past the mark line, so the mark stands forward of it at the line
        y_mark = S.MARK
        near = [f + y * lean for f, y in body if S.MARK - 60 <= y <= S.MARK + 160]
        anchor = max(near) + BESIDE + 45
        bar_at = 60.0  # under its foot
    ms = parse_marks(marks) if isinstance(marks, str) else marks
    if ms:
        mt = _marks(ms, anchor - y_mark * lean, y_mark, style)
        tracks += mt
        xs = [f + y * lean for t in mt for f, y, _ in t.samples]
        lo, hi = min(lo, min(xs)), max(hi, max(xs))
    if bar:
        tracks += S.shape("bar", bar_at - S.BAR * lean, S.BAR, style).tracks
    low = min(y for _, y in body)
    ef, ey = max((f, y) for f, y in body if y < low + 30)
    exit = (ef - 25, max(S.X * 0.06, ey))
    return Glyph(tracks, lo, hi, exit, (anchor, y_mark), bar_at)


MARK_SEP = 56.0  # clear space between two marks over one letter


def _marks(ms: list[Mark], f_mid: float, y: float, style: S.Style) -> list:
    """Marks in the order said, the first backmost (rightmost on the page), measured
    from their own extents so a long or pitched mark never crowds the next."""
    built = []
    for m in ms:
        sh = S.shape(VOWELS[m.vowel], 0, y, style, long=1.9 if m.long else 1.0, pitch=m.pitch)
        fs = [f for t in sh.tracks for f, _, _ in t.samples]
        built.append((m, sh, min(fs), max(fs)))
    total = sum(hi - lo for _, _, lo, hi in built) + MARK_SEP * (len(built) - 1)
    f = f_mid - total / 2
    tracks = []
    for m, sh, lo, hi in built:
        shift = f - lo
        tracks += sh.moved(shift, 0).tracks
        if m.emphasis:
            tops = [yy for t in sh.tracks for _, yy, _ in t.samples]
            tracks += _brow(shift, max(tops) + 60, style)
        f += hi - lo + MARK_SEP
    return tracks


def _brow(f: float, y: float, style: S.Style) -> list:
    """Emphasis: a touch arched over the mark like a brow."""
    return S.shape("touch", f - 85, y, style, df=170, dy=0, sag=-0.40).tracks


# -- words -------------------------------------------------------------------------------------

GAP = 100.0  # between one letter's foremost point and the next one's backmost, page-equivalent


def parse_word(spelling: str):
    """Tokens separated by spaces: a letter's romanized spelling, ``=`` after it for the
    length bar, then ``+`` and its marks. ``_`` is the carrier. ``"n+u: v+a"`` is
    _nuuva_; ``"m+o l=+u"`` is _mollu_."""
    out = []
    for tok in spelling.split():
        head, _, marks = tok.partition("+")
        bar = head.endswith("=")
        out.append((head.rstrip("="), bar, marks))
    return out


def word(spelling: str, style: S.Style = S.HAND, tongue: str = "sinale", gap: float = GAP) -> list:
    """A word's tracks in the forward frame, its letters set right to left, each
    touching the next with a hairline from floor to floor."""
    lean = _lean(style)
    tracks, f0, prev = [], 0.0, None
    for sp, bar, marks in parse_word(spelling):
        g = glyph(sp, style, marks, bar, tongue)
        shift = f0 - g.lo
        moved = [S.Shape([t], (0, 0, 0), (0, 0, 0)).moved(shift, 0).tracks[0] for t in g.tracks]
        if prev is not None:
            end = (f0 + 10 - 0.25 * S.X * lean, S.X * 0.25)
            tracks += S.shape("touch", prev[0], prev[1], style, df=max(60, end[0] - prev[0]),
                              dy=end[1] - prev[1]).tracks
        tracks += moved
        prev = (g.exit[0] + shift, g.exit[1])
        f0 = g.hi + shift + gap
    return tracks
