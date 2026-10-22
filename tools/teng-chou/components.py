# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""The Teng Chou component assembler: renders a component from its strokes into a box.

    import components as K

    path = K.render("water", "L", (40, 60, 400, 940))     # a pathops.Path, font units
    K.COMPONENTS["water"].forms["L"].count                  # strokes in that form
    K.complexity("water")                                   # the layout weight

A component is defined in ``inventory.py``. Each of its *forms* (the standalone
form and one per position: L, R, T, B, or an enclosure) is drawn in its own box,
``w`` by ``h`` units with the origin at the lower left, as a list of strokes in
stroke order. A stroke is written ``"<stroke id> <x> <y> key=value ..."``: the
Layer 1 stroke started at (x, y) in the form's box, with its own parameters,
which ``strokes.STROKES`` checks against their permitted ranges.

A form may instead be *composed*, as a sound component that is a whole character
is: a list of parts, each ``(component, form, (x0, y0, x1, y1))`` in the form's box.

**How a form is fitted to a box.** The brush path of every stroke is mapped from
the form's box to the target box, x and y separately, and only then is the brush
footprint laid along it. A form squeezed into a narrow box therefore keeps its
stroke weight: its strokes come closer together, they do not get thinner. The
weight itself is the style's, so every component of one character is drawn with
one brush.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import pathops

import strokes as S

POSITIONS = ("S", "L", "R", "T", "B", "⿸", "⿵", "⿺", "⿴")
POSITION_NAMES = {
    "S": "standalone", "L": "left", "R": "right", "T": "top", "B": "bottom",
    "⿸": "enclosing from the upper left", "⿵": "enclosing, open below",
    "⿺": "enclosing from the lower left", "⿴": "enclosing all round",
}

# the share of a stroke's complexity, by stroke: a stroke with a turn, two beads or
# two rods takes more room than a straight one
STROKE_WEIGHT = {sid: 1.0 for sid in S.STROKES}
STROKE_WEIGHT.update({
    "dot": 0.6, "dot-left": 0.6, "barb-dot": 0.7, "scale": 0.6, "rise": 0.8, "sweep-short": 0.8,
    "turn": 1.4, "turn-spur": 1.4, "corner": 1.4, "bend-spur": 1.4, "turn-sweep": 1.4,
    "sweep-turn": 1.3, "coil": 1.6, "rods": 1.5, "tally": 1.2,
})


@dataclass
class Stroke:
    sid: str
    x: float
    y: float
    params: dict

    @classmethod
    def parse(cls, text: str) -> "Stroke":
        head, *rest = text.split()
        x, y, *kv = rest
        params = {}
        for item in kv:
            k, v = item.split("=")
            params[k] = float(v)
        if head not in S.STROKES:
            raise ValueError(f"{text!r}: no stroke {head!r}")
        st = S.STROKES[head]
        for k, v in params.items():
            if k not in st.params:
                raise ValueError(f"{text!r}: {head} has no parameter {k!r}")
            lo, _, hi = st.params[k]
            if not lo <= v <= hi:
                raise ValueError(f"{text!r}: {k}={v:g} is outside {lo:g}..{hi:g}")
        return cls(head, float(x), float(y), params)

    def tracks(self):
        return S.STROKES[self.sid].build(self.x, self.y, **self.params)


@dataclass
class Form:
    position: str
    w: float
    h: float
    strokes: list = field(default_factory=list)  # [Stroke], in stroke order
    parts: list = field(default_factory=list)  # [(component, form, box)] for a composed form
    inner: tuple | None = None  # an enclosure's open area, (x0, y0, x1, y1) in its box
    note: str = ""

    @property
    def count(self) -> int:
        if self.parts:
            return sum(form_of(c, f)[0].count for c, f, _ in self.parts) + len(self.strokes)
        return len(self.strokes)

    @property
    def weight(self) -> float:
        if self.parts:
            return sum(form_of(c, f)[0].weight for c, f, _ in self.parts) + sum(STROKE_WEIGHT[s.sid] for s in self.strokes)
        return sum(STROKE_WEIGHT[s.sid] for s in self.strokes)


@dataclass
class Component:
    id: str
    meaning: str
    role: str  # "meaning", "sound" or "structural"
    char: str | None  # the root this component writes alone, if any
    forms: dict  # position -> Form; "S" is the standalone form
    lookalike: str = ""  # the nearest Chinese component, and how this one departs from it
    novel: str = ""  # the novel stroke it carries, where the proposal asks for one
    sound: str | None = None  # for a sound component: the reading it gives
    positions: tuple = ()  # the positions the proposal uses it in
    idc: str = ""  # for a composed sound component: its layout, as the proposal writes it

    @property
    def standalone(self) -> Form:
        """The standalone form, or, for a bound component with one position, that form."""
        return self.forms.get("S") or next(iter(self.forms.values()))

    @property
    def bound(self) -> bool:
        return "S" not in self.forms


COMPONENTS: dict[str, Component] = {}
ERRORS: list[str] = []


def _parse_all(cid, pos, texts):
    out = []
    for t in texts:
        try:
            out.append(Stroke.parse(t))
        except ValueError as e:
            ERRORS.append(f"{cid} {pos}: {e}")
    return out


def define(cid, meaning, role, char, forms, lookalike="", novel="", positions=(), sound=None, idc=""):
    built = {}
    for pos, spec in forms.items():
        if pos not in POSITIONS:
            raise ValueError(f"{cid}: no position {pos!r}")
        w, h = spec.get("box", (1000, 1000))
        built[pos] = Form(
            pos, w, h,
            _parse_all(cid, pos, spec.get("strokes", [])),
            [tuple(p) for p in spec.get("parts", [])],
            spec.get("inner"), spec.get("note", ""),
        )
    if isinstance(positions, str):
        positions = positions.split()
    COMPONENTS[cid] = Component(cid, meaning, role, char, built, lookalike, novel, sound, tuple(positions), idc)


def complexity(cid: str, position: str = "S") -> float:
    """The room a component asks for: its strokes, each weighted by how much ground
    it covers. A layout divides a square between parts by this."""
    form = COMPONENTS[cid].forms.get(position) or COMPONENTS[cid].standalone
    return round(form.weight, 1)


# -- rendering ---------------------------------------------------------------------------------


def _mapped_tracks(form: Form, box):
    x0, y0, x1, y1 = box
    sx, sy = (x1 - x0) / form.w, (y1 - y0) / form.h
    out = []
    if form.parts:
        for c, f, (a0, b0, a1, b1) in form.parts:
            sub = (x0 + a0 * sx, y0 + b0 * sy, x0 + a1 * sx, y0 + b1 * sy)
            out.extend(_mapped_tracks(form_of(c, f)[0], sub))
    for s in form.strokes:
        for t in s.tracks():
            t.samples = [(x0 + x * sx, y0 + y * sy, p) for x, y, p in t.samples]
            out.append(t)
    return out


def form_of(cid: str, position: str) -> tuple[Form, str]:
    """The form a component takes at ``position``: its own drawing there, or, where it
    has none, its standalone form, which a layout then squeezes."""
    comp = COMPONENTS[cid]
    if position in comp.forms:
        return comp.forms[position], position
    return comp.standalone, comp.standalone.position


def render(cid: str, position: str = "S", box=None, style: S.Style = S.REGULAR) -> pathops.Path:
    """The outline of component ``cid`` at ``position``, fitted to ``box`` (font units).
    With no box, the form is drawn in its own box at the origin."""
    form, _ = form_of(cid, position)
    if box is None:
        box = (0, 0, form.w, form.h)
    return S.outline(_mapped_tracks(form, box), style)


def render_parts(parts, style: S.Style = S.REGULAR) -> pathops.Path:
    """One outline from several ``(component, position, box)`` placements."""
    tracks = []
    for cid, position, box in parts:
        form, _ = form_of(cid, position)
        tracks.extend(_mapped_tracks(form, box))
    return S.outline(tracks, style)


def weight_for(strokes: int) -> S.Style:
    """The brush for a character of ``strokes`` strokes: a dense character is written
    with a slightly finer brush, as a font's are, so it does not clot."""
    w = S.REGULAR.weight * max(0.74, min(1.0, 1.08 - 0.022 * strokes))
    return S.Style(weight=w)


def stroke_count(cid: str, position: str = "S") -> int:
    form, _ = form_of(cid, position)
    return form.count


def _load():
    import inventory  # noqa: F401  (defines the components)

    if ERRORS:
        raise ValueError("the inventory has strokes outside their ranges:\n  " + "\n  ".join(ERRORS))


_load()
