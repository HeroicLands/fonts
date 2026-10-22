# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Test sequences: stems, bowls and marks set side by side on an implied line.

They test the strokes and how they sit together. They are not letters or words of
the script: which strokes make which letter is the next layer's work.

A sequence is a list of units. A unit is a bowl with a stem at one of three grades,
or a stemless stroke, with vowel marks over it, optionally a length bar beneath it
and a touch to the next unit. ``assemble`` lays the units out in the forward frame
with no line drawn between them, so the same call serves every ``Style``.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import strokes as S

GAP = 120.0  # the space between one unit and the next, measured on the slanted page
STEMS = {
    "raised": {"top": S.ASC},
    "level": {"top": S.X + 60},
    "lowered": {"top": S.X + 60, "foot": S.DESC, "tail": 0},
    "lowered-ezh": {"top": S.X + 60, "foot": S.DESC, "tail": 1},
    "lowered-sweep": {"top": S.X + 60, "foot": S.DESC - 40, "tail": 2, "reach": 1.3},
}


@dataclass
class Unit:
    sid: str
    stem: str | None = None  # a key of STEMS; None for a stemless stroke
    params: dict = field(default_factory=dict)
    marks: list = field(default_factory=list)  # (mark id, params)
    bar: bool = False
    touch: bool = True  # a touch to the next unit


def _unit(u: Unit, f0: float, style: S.Style):
    shapes = []
    if u.stem:
        shapes.append(S.shape("stem", f0, 0, style, **STEMS[u.stem]))
    shapes.append(S.shape(u.sid, f0, 0, style, **u.params))
    lean = math.tan(math.radians(style.slant))
    pts = [(f + y * lean, y) for sh in shapes for t in sh.tracks for f, y, _ in t.samples]  # the letter alone
    lo, hi = min(p[0] for p in pts), max(p[0] for p in pts)
    body = [p[0] for p in pts if 0 <= p[1] <= S.X]
    mid = (min(body) + max(body)) / 2 - S.MARK * lean
    if u.marks:
        widths = [90 * m[1].get("long", 1.0) for m in u.marks]
        total = sum(widths) + 24 * (len(widths) - 1)
        f = mid - total / 2
        for (mid_, params), w in zip(u.marks, widths):
            shapes.append(S.shape(mid_, f + w / 2, S.MARK, style, **params))
            f += w + 24
    if u.bar:
        shapes.append(S.shape("bar", mid + S.MARK * lean - S.BAR * lean, S.BAR, style))
    return shapes, lo, hi


def assemble(units, style: S.Style):
    """The run's tracks in the forward frame."""
    tracks, f0, prev_touch = [], 0.0, None
    for u in units:
        shapes, lo, hi = _unit(u, f0, style)
        shift = f0 - lo
        shapes = [sh.moved(shift, 0) for sh in shapes]
        hi += shift
        if prev_touch is not None:
            start = prev_touch
            end = (f0 + 15, S.X * 0.25)
            tracks += S.shape("touch", start[0], start[1], style, df=end[0] - start[0], dy=end[1] - start[1]).tracks
        for sh in shapes:
            tracks += sh.tracks
        prev_touch = (hi - 25, S.X * 0.06) if u.touch else None
        f0 = hi + GAP
    return tracks


TESTS = [
    ("the three families: two standing, one hanging", [
        Unit("bud", "level", marks=[("one", {})]),
        Unit("arches", "level", marks=[("three", {})]),
        Unit("hung-coil", "level", marks=[("two", {})]),
    ]),
    ("arches at three grades", [
        Unit("arches", "raised", marks=[("dab", {})]),
        Unit("arches", "level", marks=[("dab", {})]),
        Unit("arches", "lowered", marks=[("dab", {})]),
    ]),
    ("voicing turns a letter over: standing, then hanging", [
        Unit("arches", "raised", marks=[("one", {})]),
        Unit("hung-arches", "raised", marks=[("one", {})]),
        Unit("arches", "level", marks=[("backdab", {})]),
        Unit("hung-arches", "level", marks=[("backdab", {})]),
    ]),
    ("every form turned over", [
        Unit("hung-bud", "level", marks=[("two", {})]),
        Unit("hung-arches", "lowered", marks=[("one", {})]),
        Unit("coil", "raised", marks=[("three", {})]),
    ]),
    ("the three tails below the line", [
        Unit("bud", "lowered", marks=[("backdab", {})]),
        Unit("hung-coil", "lowered-ezh", marks=[("one", {})]),
        Unit("arches", "lowered-sweep", marks=[("two", {})]),
    ]),
    ("stemless strokes, three arches, bar, length, pitch", [
        Unit("carrier", marks=[("one", {"long": 1.8})]),
        Unit("riser"),
        Unit("arches", "raised", params={"n": 3, "w": 460}, bar=True, marks=[("three", {})]),
        Unit("crook", marks=[("hook", {"pitch": 1.0})]),
    ]),
    ("a run mixing hanging and standing forms", [
        Unit("hung-coil", "raised", marks=[("curl", {})]),
        Unit("bud", "level", marks=[("two", {}), ("backdab", {"pitch": -1.0})]),
        Unit("arches", "lowered", touch=False),
        Unit("hung-coil", "level"),
        Unit("bud", "raised", marks=[("one", {})]),
    ]),
]
