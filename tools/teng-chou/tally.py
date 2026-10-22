# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""The tally of five: the count a clerk keeps, one stroke per item.

    import tally as T

    T.render(3)          # the tally after three items: its first three strokes
    T.STAGES[4].glyph    # "tc.tally5", the finished tally, which means five

Clerks, temple scribes and quartermasters keep a running count by writing one
stroke of the tally for each item, in a fixed order, so the first one to four
strokes are a partial count and a finished tally is five. The tally is five
strokes of the body, long and short, with no dab:

1. the left post, a vertical spur, its barb the script's own;
2. the lintel, a long horizontal from the post's head;
3. the right post, a needle hanging from the lintel's end;
4. the entry, a short horizontal inside under the lintel, the line of the ledger;
5. the audit, a fall across the frame from its upper left, which closes the count.

Every stage is drawn on the finished tally's square, so a partial count stands
where its strokes stand in the five, and the strokes do not move as it grows.
"""

from __future__ import annotations

from dataclasses import dataclass

import pathops

import components as K
import layout as Y
import strokes as S

STROKES = [
    "vertical-spur 240 820 l=640 spur=90",
    "horizontal 240 830 l=560 rise=3",
    "needle 770 820 l=640",
    "horizontal 330 610 l=340 rise=4",
    "fall 300 520 l=440 a=-46 foot=0.25",
]
NAMES = ["ONE", "TWO", "THREE", "FOUR", "FIVE"]
GLOSSES = ["a tally of one", "a tally of two", "a tally of three", "a tally of four", "five; a tally of five"]


@dataclass
class Stage:
    count: int
    gloss: str

    @property
    def glyph(self) -> str:
        return f"tc.tally{self.count}"

    @property
    def name(self) -> str:
        return f"TENG CHOU TALLY {NAMES[self.count - 1]}"


STAGES = {n: Stage(n, GLOSSES[n - 1]) for n in range(1, 6)}


def strokes_of(count: int):
    """The first ``count`` strokes, each ``(part, stroke, tracks)``, on the finished
    tally's square, fitted as the five are."""
    parsed = [K.Stroke.parse(t) for t in STROKES]
    groups = [(0, st, st.tracks()) for st in parsed]
    every = [t for _, _, g in groups for t in g]
    box = (Y.MARGIN_X, Y.MARGIN_Y, Y.EM - Y.MARGIN_X, Y.EM - Y.MARGIN_Y)
    Y._fit(every, box, (1.0, 1.0), Y.MAX_GROW)
    for t in every:
        t.samples = [(x, y + Y.LIFT, p) for x, y, p in t.samples]
    return groups[:count]


def render(count: int, style: S.Style | None = None) -> pathops.Path:
    tracks = [t for _, _, g in strokes_of(count) for t in g]
    return Y.outline(tracks, style or K.weight_for(len(STROKES)))
