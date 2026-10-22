# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""The Jurthati syllabary: 87 signs, each a simplified Teng Chou character.

    import syllabary as J

    J.SIGNS[0]                  # Sign("a", "yan", "cut")
    J.render("ka")              # a pathops.Path on the 1000-unit em

Each sign is drawn from the strokes of its source character, read close to the
sign's syllable, by one of four simplifications:

- ``cut``: a pictograph cut to its first three strokes, the closing one turned
  into a tail (a horizontal or a vertical ends in a point);
- ``sound``: the meaning component dropped and the sound component kept, reduced
  to its outline: its three or four longest strokes, in stroke order;
- ``whole``: the whole character in the running hand, closed into its three or
  four longest strokes;
- ``part:<component>``: the whole character in the running hand, that component
  reduced to its one longest stroke and the rest to its outline.

A sign is written with a lighter brush than a character and set smaller in the
square, as kana sit beside kanji: ``WEIGHT`` and ``SIZE``. ``picks`` names the
strokes a sign keeps, by their index in the source, where the rule's choice is
too close to another sign's. The order of ``ROWS`` is the order of the code
points.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import pathops

import characters as C
import components as K
import layout as Y
import strokes as S

WEIGHT = 0.80  # of a character's brush
SIZE = 0.80  # of the em the sign's ink spans, at most
LIFT = 10

# the tail a closing stroke takes in a cut pictograph
TAIL = {"horizontal": "fall-flat", "vertical": "needle", "vertical-spur": "needle", "turn": "turn-sweep",
        "turn-spur": "turn-sweep"}


@dataclass
class Sign:
    syllable: str
    source: str  # the morpheme whose character it simplifies
    method: str
    picks: tuple = ()  # stroke indices kept, overriding the rule

    @property
    def glyph(self) -> str:
        return f"js.{self.syllable}"


ROWS = [
    ('a', 'yan', 'cut'),
    ('i', 'yei', 'sound'),
    ('u', 'wou', 'sound'),
    ('e', 'jie', 'sound'),
    ('o', 'wuo', 'sound'),
    ('ka', 'ka', 'sound'),
    ('ki', 'ki', 'sound'),
    ('ku', 'kuo', 'whole'),
    ('ke', 'keng', 'sound'),
    ('ko', 'ko', 'sound'),
    ('ga', 'ga', 'whole'),
    ('gi', 'gui', 'sound'),
    ('gu', 'gou', 'sound'),
    ('ge', 'gen', 'sound'),
    ('go', 'go', 'whole'),
    ('sa', 'sa', 'sound'),
    ('si', 'sing', 'part:death'),
    ('su', 'sou', 'sound'),
    ('se', 'seng', 'sound'),
    ('so', 'sou', 'whole'),
    ('sha', 'shai', 'sound'),
    ('shi', 'shi', 'whole'),
    ('shu', 'shou', 'cut'),
    ('she', 'shen', 'sound'),
    ('sho', 'sho', 'sound'),
    ('za', 'zha', 'part:plant'),
    ('zi', 'zhi', 'whole'),
    ('zu', 'zhou', 'sound'),
    ('ze', 'zheng', 'whole'),
    ('zo', 'zho', 'cut'),
    ('ja', 'ja', 'cut'),
    ('ji', 'jing', 'cut'),
    ('ju', 'jou', 'sound'),
    ('je', 'jei', 'whole'),
    ('jo', 'jo', 'whole'),
    ('ta', 'ta', 'sound'),
    ('ti', 'ti', 'whole'),
    ('te', 'teng', 'cut'),
    ('to', 'to', 'whole'),
    ('tsa', 'tsai', 'whole'),
    ('tsu', 'tou', 'cut'),
    ('tse', 'tsen', 'cut'),
    ('tso', 'tsong', 'cut'),
    ('cha', 'chai', 'cut'),
    ('chi', 'ching', 'cut'),
    ('chu', 'chou', 'whole'),
    ('che', 'cheng', 'whole'),
    ('cho', 'chiao', 'part:ice'),
    ('da', 'da', 'sound'),
    ('di', 'di', 'whole'),
    ('du', 'dou', 'part:motion'),
    ('de', 'dei', 'sound'),
    ('do', 'do', 'sound'),
    ('na', 'na', 'sound'),
    ('ni', 'ni', 'whole'),
    ('nu', 'nou', 'cut'),
    ('ne', 'nie', 'part:grain'),
    ('no', 'no', 'sound'),
    ('ha', 'ha', 'part:cover'),
    ('hi', 'hing', 'sound'),
    ('he', 'hen', 'sound'),
    ('ho', 'ho', 'cut'),
    ('fa', 'fa', 'whole'),
    ('fu', 'hou', 'part:person'),
    ('ba', 'ba', 'whole'),
    ('bi', 'bin', 'sound'),
    ('bu', 'bou', 'whole'),
    ('be', 'beng', 'whole'),
    ('bo', 'bo', 'whole'),
    ('ma', 'ma', 'sound'),
    ('mi', 'mi', 'cut'),
    ('mu', 'mou', 'cut'),
    ('me', 'mei', 'part:moon'),
    ('mo', 'mong', 'part:cover'),
    ('ya', 'ya', 'whole'),
    ('yu', 'you', 'cut'),
    ('yo', 'yo', 'whole'),
    ('ra', 'la', 'whole'),
    ('ri', 'ri', 'whole'),
    ('ru', 'lou', 'sound'),
    ('re', 'leng', 'part:sun'),
    ('ro', 'lo', 'whole'),
    ('wa', 'wa', 'whole'),
    ('wu', 'gwo', 'whole'),
    ('we', 'weng', 'whole'),
    ('wo', 'wo', 'whole'),
    ('n', 'wen', 'part:enclosure'),]

# Strokes kept by hand, by syllable, where the rule's choice is too close to another sign
# at body size; proposed by ``syllabary_distinct.py --search``.
PICKS: dict[str, tuple] = {
    "ka": (0, 1, 3),
    "ke": (0, 2, 3),
    "ko": (0, 2, 3),
    "gu": (1, 2, 5),
    "sa": (0, 1),
    "sha": (1, 2, 3),
    "she": (0, 2, 8),
    "sho": (0, 2, 3),
    "ju": (1, 2, 4),
    "to": (1, 2, 5),
    "tso": (1, 2),
    "da": (0, 1, 4),
    "do": (1, 5, 7),
    "mo": (0, 1, 4),
    "ya": (0, 4, 5),
    "ru": (1, 2),
}

SIGNS = [Sign(s, src, m, PICKS.get(s, ())) for s, src, m in ROWS]
BY_SYLLABLE = {s.syllable: s for s in SIGNS}


def _extent(group) -> float:
    xs = [x for t in group for x, _, _ in t.samples]
    ys = [y for t in group for _, y, _ in t.samples]
    return math.hypot(max(xs) - min(xs), max(ys) - min(ys))


def _outline_of(strokes, k):
    """The ``k`` longest strokes, in stroke order."""
    ranked = sorted(range(len(strokes)), key=lambda i: -_extent(strokes[i][2]))[:k]
    return [strokes[i] for i in sorted(ranked)]


def _tail(stroke):
    """The closing stroke of a cut pictograph, ending in a point."""
    sid = TAIL.get(stroke.sid)
    if not sid:
        return None
    params = {k: v for k, v in stroke.params.items() if k in S.STROKES[sid].params}
    if sid == "turn-sweep":
        params = {"l1": min(600, max(100, stroke.params.get("l1", 300))), "l2": min(600, max(180, stroke.params.get("l2", 380)))}
    if sid == "fall-flat":
        params = {"l": min(920, max(300, stroke.params.get("l", 480))), "a": -6}
    if sid == "needle":
        params = {"l": min(860, max(300, stroke.params.get("l", 520)))}
    return K.Stroke(sid, stroke.x, stroke.y, params).tracks()


def chosen(sign: Sign):
    """The source strokes the sign keeps, each ``(part, stroke, tracks)``, in em units."""
    strokes, parts = source_strokes(sign)
    if sign.picks:
        return [strokes[i] for i in sign.picks]
    return rule_choice(sign, strokes, parts if sign.method != "sound" else [])


def source_strokes(sign: Sign):
    """The strokes the sign is chosen from: the source character's, or for ``sound`` its
    sound component's alone, each ``(part, stroke, tracks)``; and the parts."""
    ch = C.BY_MORPHEME[sign.source]
    if sign.method == "sound":
        tree = Y.parse(ch.formula)
        sound = next(k for k in tree.kids if isinstance(k, Y.Leaf) and k.sound)
        comp = K.COMPONENTS[sound.cid]
        formula = comp.idc or "{" + sound.cid + "}"
        overrides = C.BY_MORPHEME[comp.char].overrides if comp.char in C.BY_MORPHEME else {}
        strokes, parts, _ = Y.strokes_of(formula, overrides)
    else:
        strokes, parts, _ = Y.strokes_of(ch.formula, ch.overrides)
    return strokes, parts


def rule_choice(sign: Sign, strokes, parts):
    if sign.method == "cut":
        kept = strokes[:3]
        if len(strokes) > 3:
            part, st, group = kept[-1]
            kept[-1] = (part, st, _tail_mapped(st, group))
        return kept
    k = 4 if len(strokes) >= 8 else 3
    if sign.method.startswith("part:"):
        cid = sign.method.split(":", 1)[1]
        mine = [next(i for i, p in enumerate(parts) if p.leaf.cid == cid)]
        reduced = [s for s in strokes if s[0] in mine]
        rest = [s for s in strokes if s[0] not in mine]
        keep = _outline_of(reduced, 1) + _outline_of(rest, k - 1)
        order = {id(s): n for n, s in enumerate(strokes)}
        return sorted(keep, key=lambda s: order[id(s)])
    return _outline_of(strokes, k)


def _tail_mapped(stroke, group):
    """A tail drawn where the closing stroke lay: the tail's own brush path is mapped
    onto the box the closing stroke's path spans."""
    tail = _tail(stroke)
    if tail is None:
        return group
    src = stroke.tracks()

    def box(ts):
        xs = [x for t in ts for x, _, _ in t.samples]
        ys = [y for t in ts for _, y, _ in t.samples]
        return min(xs), min(ys), max(xs), max(ys)

    a0, b0, a1, b1 = box(src)
    c0, d0, c1, d1 = box(group)
    sx = (c1 - c0) / max(a1 - a0, 1.0)
    sy = (d1 - d0) / max(b1 - b0, 1.0)
    for t in tail:
        t.samples = [(c0 + (x - a0) * sx, d0 + (y - b0) * sy, p) for x, y, p in t.samples]
    return tail


def tracks_of(syllable: str):
    """The sign's brush paths, fitted to its square."""
    sign = BY_SYLLABLE[syllable]
    tracks = [t for _, _, g in chosen(sign) for t in g]
    xs = [x for t in tracks for x, _, _ in t.samples]
    ys = [y for t in tracks for _, y, _ in t.samples]
    x0, y0, x1, y1 = min(xs), min(ys), max(xs), max(ys)
    span = Y.EM * SIZE - 2 * Y.INSET
    k = min(span / max(x1 - x0, 1.0), span / max(y1 - y0, 1.0), 1.25)
    cx, cy = Y.EM / 2, Y.EM / 2 + LIFT
    for t in tracks:
        t.samples = [(cx + (x - (x0 + x1) / 2) * k, cy + (y - (y0 + y1) / 2) * k, p) for x, y, p in t.samples]
    return tracks


def style() -> S.Style:
    return S.Style(weight=S.REGULAR.weight * WEIGHT)


def render(syllable: str) -> pathops.Path:
    return Y.outline(tracks_of(syllable), style())
