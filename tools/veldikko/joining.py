# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""The Veldikko joining: each letter's contextual forms, as the font draws them.

    import joining as J

    f = J.form("t", "medi")            # t joined on both sides
    f.tracks, f.advance, f.mark, f.bar  # forward-frame tracks, then font units
    J.setting("k+a l p+i")             # kalpi set from its forms, as the font sets it

A letter has four forms. **Isolated**, it stands alone. **Initial**, it begins a
word and joins forward to the next letter. **Medial**, it joins on both sides.
**Final**, it ends a word and is joined from the letter before it. The forms are
the one drawing of the letter, never redrawn, with the halves of the ``touch``
added on the sides that join.

**The join.** A touch is cut in two at the join point, ``JOIN_Y`` above the line
at the advance edge, where it runs level at its fullest, ``JOIN_P``. The half that
leaves a letter rises from the end of its floor, set down from nothing, and levels
off into the join point at the letter's forward edge; the half that enters the
next letter runs on level from the join point at its back edge and falls into it
just behind its stem, lifted to nothing. Every form that joins meets every other
at the same point, heading and pressure, so any two letters make one unbroken
hairline. A side that joins stands ``HALF`` beyond the letter's ink above the
line; a side that does not stands ``SIDEBEARING`` beyond all its ink.

**Below the line nothing is spaced.** A nasal's hooked tail turns back under the
letter before it, as a long tail does in Arabic calligraphy, so the gaps above
the line stay even.

**The long tails.** A nasal that ends a word may take the forward sweep or the
ezh in place of its hook (``TAILS``): the room below the line at a word's end is
where the scribe has it. The font offers them as alternates; it cannot see where
a line ends.

**The stretch.** A letter that carries a long vowel, a pitched vowel or a
diphthong, and joins forward, draws its leaving half ``STRETCH`` longer, so the
mark's tail has room before the next letter: the connector is drawn out, as a
calligrapher draws out a join to make space.
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import letters as L  # noqa: E402
import strokes as S  # noqa: E402

FORMS = ("isol", "init", "medi", "fina")
JOINS = {"isol": (False, False), "init": (False, True), "medi": (True, True), "fina": (True, False)}  # (back, forward)

JOIN_Y = 72.0  # the join point's height above the line
JOIN_P = 0.15  # the touch's pressure at the join point: its faint swell
HALF = 50.0  # from a joining side's ink above the line to the join point
SIDEBEARING = 24.0  # from a side that does not join to its ink
ABOVE = -40.0  # ink below this is a tail, and is not spaced
ENTRY_Y = 0.25 * S.X  # where the entering half lands on the letter's back
LEAVE = 35.0  # the heading the leaving half sets out at, degrees above level
ARRIVE = -28.0  # the heading the entering half lands at
STRETCH = 130.0  # how much longer a stretched form's leaving half is

# The long tails a word's last nasal may take, by alternate: the sweep forward under
# the letter, and the ezh hung from the line.
TAILS = {"sweep": 2, "ezh": 1}
NASALS = ("m", "n", "ng")


def _lean(style):
    return math.tan(math.radians(style.slant))


def _pe(f, y, lean):
    """Page-equivalent forward position: the page x, negated."""
    return f + y * lean


@dataclass
class Form:
    """A letter's form: its tracks in the forward frame, and its metrics in font
    units with x running right on the page from the form's left edge."""

    name: str
    tracks: list
    left_pe: float  # the page-equivalent position of the left (forward) edge
    advance: float
    mark: tuple  # (x, y) where the marks' middle stands
    bar: float  # x where the length bar's middle stands

    def x(self, pe: float) -> float:
        """Font x of a page-equivalent position."""
        return self.left_pe - pe


def _letter_tracks(letter: L.Letter, style, tail: str | None):
    """The letter's own tracks and its isolated glyph data; a long tail, when asked
    for, replaces the nasal's hook."""
    g = L.glyph(letter, style)
    if tail is None:
        return g.tracks, g
    stem, bowl, _ = L._parts(letter, style)
    grade = dict(L.GRADES[letter.grade])
    grade["tail"] = TAILS[tail]
    stem = S.shape("stem", 0, 0, style, **grade)
    return stem.tracks + bowl.tracks, g


def _leaving(e, j_f, style, stretch: float):
    """The half of a touch that leaves a letter: from the end of its floor, set down
    from nothing, rising and levelling off into the join point."""
    ef, ey = e
    d = max(40.0, j_f - ef)
    t = S.Track(ef, ey, -0.6)
    c1 = S.polar(ef, ey, min(0.45 * d, 70.0), LEAVE)
    c2 = (j_f - 0.40 * d, JOIN_Y)
    t.curve(c1, c2, j_f, JOIN_Y, JOIN_P, ease=lambda u: math.sin(math.pi * u / 2))
    return t


def _entering(j_f, n, style):
    """The half of a touch that enters a letter: from the join point, level, falling
    into the letter behind its stem and lifted to nothing."""
    nf, ny = n
    d = max(30.0, nf - j_f)
    t = S.Track(j_f, JOIN_Y, JOIN_P)
    c1 = (j_f + 0.40 * d, JOIN_Y)
    c2 = S.polar(nf, ny, -min(0.40 * d, 50.0), ARRIVE)
    t.curve(c1, c2, nf, ny, -0.6, ease=lambda u: 1 - math.cos(math.pi * u / 2))
    return t


def _extent(tracks, lean, low=None):
    pts = [_pe(f, y, lean) for t in tracks for f, y, _ in t.samples if low is None or y > low]
    return min(pts), max(pts)


def form(spelling: str | L.Letter, name: str, style: S.Style = S.HAND, tail: str | None = None,
         stretch: bool = False, tongue: str = "sinale") -> Form:
    """One form of a letter: ``isol``, ``init``, ``medi`` or ``fina``."""
    letter = spelling if isinstance(spelling, L.Letter) else L.letter(spelling, tongue)
    back, forward = JOINS[name]
    lean = _lean(style)
    tracks, g = _letter_tracks(letter, style, tail)
    lo_all, hi_all = _extent(tracks, lean)
    lo, hi = _extent(tracks, lean, ABOVE)

    left_pe = hi + HALF + (STRETCH if stretch else 0.0) if forward else hi_all + SIDEBEARING
    right_pe = lo - HALF if back else lo_all - SIDEBEARING
    out = list(tracks)
    if forward:
        j_f = left_pe - JOIN_Y * lean
        out.append(_leaving(g.exit, j_f, style, STRETCH if stretch else 0.0))
    if back:
        j_f = right_pe - JOIN_Y * lean
        band = [_pe(f, y, lean) for t in tracks for f, y, _ in t.samples if 30 <= y <= 120]
        n_pe = min(band) + 8.0
        out.append(_entering(j_f, (n_pe - ENTRY_Y * lean, ENTRY_Y), style))
    anchor_pe, y_mark = g.mark_at
    f = Form(name, out, left_pe, left_pe - right_pe, (0.0, y_mark), 0.0)
    f.mark = (f.x(anchor_pe), y_mark)
    f.bar = f.x(g.bar_at)
    return f


# -- setting a word from its forms, as the font does --------------------------------------------


def forms_of(n: int) -> list[str]:
    """The forms of the letters of an n-letter word, every letter joining both ways."""
    if n == 1:
        return ["isol"]
    return ["init"] + ["medi"] * (n - 2) + ["fina"]


def marks_tracks(marks: str, style):
    """A run of marks over one letter, centred on (0, 0) in the page-equivalent frame."""
    ms = L.parse_marks(marks)
    return L._marks(ms, 0.0, 0.0, style) if ms else []


def needs_stretch(marks: str) -> bool:
    ms = L.parse_marks(marks)
    return len(ms) > 1 or any(m.long or m.pitch for m in ms)


def setting(spelling: str, style: S.Style = S.HAND, tongue: str = "sinale", tails: str | None = None):
    """A word set from its forms, right to left, as the font sets it: the tracks of
    every letter and mark moved to the page in font units, x running right from
    the word's left edge, and the word's width. ``tails`` gives a word's last nasal
    its long tail."""
    toks = L.parse_word(spelling)
    names = forms_of(len(toks))
    placed, x = [], 0.0
    for (sp, bar, marks), nm in zip(toks, names):
        lt = L.letter(sp, tongue)
        tail = tails if tails and nm in ("fina", "isol") and lt.id in NASALS else None
        fm = form(lt, nm, style, tail=tail, stretch=needs_stretch(marks) and JOINS[nm][1], tongue=tongue)
        x += fm.advance
        placed.append((fm, x, bar, marks))
    width = x
    out = []
    for fm, right, bar, marks in placed:
        ox = width - right  # the form's left edge
        out += page_tracks(fm.tracks, style, fm.left_pe + ox)
        if marks:
            out += page_tracks(marks_tracks(marks, style), style, fm.mark[0] + ox, fm.mark[1])
        if bar:
            out += page_tracks(S.shape("bar", 0, 0, style).tracks, style, fm.bar + ox, S.BAR)
    return out, width


def page_tracks(tracks, style, dx=0.0, dy=0.0):
    """Tracks moved so that their page origin lands at (dx, dy) in font units, x
    running right: a point at page x ``-(f + y lean)`` moves to that plus ``dx``."""
    lean = _lean(style)
    out = []
    for t in tracks:
        n = S.Track(0, 0, 0)
        n.samples = [(f - dx - dy * lean, y + dy, p) for f, y, p in t.samples]
        out.append(n)
    return out
