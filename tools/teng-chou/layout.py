# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""The Teng Chou layout engine: a character from its IDC formula.

    import layout as Y

    path = Y.render("⿰{water}‹mong›")          # a pathops.Path on the 1000-unit em
    Y.render_char("wong")                      # the same, by morpheme, with its overrides
    Y.parse("⿰{water}‹mong›")                 # the tree
    Y.place(Y.parse("⿰{water}‹mong›"))         # the leaves and their boxes

A formula is written as the proposal writes it: ``{id}`` is a meaning component,
``‹morpheme›`` a sound component (the whole character of that root), and an
Ideographic Description Character is followed by its two or three operands, which
may themselves be formulas. Twelve operators are understood:

    ⿰ left-right      ⿱ top-bottom        ⿲ left-middle-right  ⿳ top-middle-bottom
    ⿴ full enclosure  ⿵ open below       ⿶ open above         ⿷ open at the right
    ⿸ from upper left ⿹ from upper right  ⿺ from lower left    ⿻ overlaid

**Boxes.** Each operator divides its box between its operands. A two-way split
gives each side a share from a default and the operands' complexity: a meaning
component takes about 0.38 of a ⿰ or ⿱ beside a sound component, a sound
component the rest, and two meaning components share evenly. An enclosure gives
its frame the whole box and its contents the frame's ``inner`` area.

**Fitting.** A leaf's ink, not its drawing box, is fitted to its slot, so the gap
between two parts is the same in every character. A squeeze may narrow a part
by at most ``MAX_SQUEEZE`` against its height (or the reverse); past that, the part
keeps its proportions and is centred a little above the middle of its slot. The
brush path is mapped and only then is the brush laid along it, so a squeezed part
keeps the weight of the character's one brush.

**Context.** A positional form drawn for its place already follows the variant
rules. A part fitted to a place it has no drawing for is changed by rule:

- on the left, its lowest horizontal becomes a rise;
- on the left, or between two parts, a fall that reaches its right edge becomes a dot.

A part set below another is flattened by the fit itself, and the square of a
character with few strokes is drawn smaller, as regular script draws it.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass, field

import pathops

import components as K
import strokes as S

EM = 1000
MARGIN_X, MARGIN_Y = 40, 52  # the em's margin to the ink of a full character
LIFT = 10  # the visual centre sits this far above the geometric one
GAP = 46  # between the inks of two parts
MAX_SQUEEZE = 1.9  # the most a part's height may be scaled against its width, or the reverse
MAX_GROW = 1.3  # the most a part is enlarged past its drawing's own scale
INSET = 22  # skeleton to ink: a stroke's ink reaches about this far beyond its brush path

OPERATORS = {"⿰": 2, "⿱": 2, "⿲": 3, "⿳": 3, "⿴": 2, "⿵": 2, "⿶": 2, "⿷": 2, "⿸": 2, "⿹": 2, "⿺": 2, "⿻": 2}
ENCLOSURES = ("⿴", "⿵", "⿶", "⿷", "⿸", "⿹", "⿺")
CLOSE_LAST = ("⿺", "⿶")  # frames that close the character from below are written after their contents

# Where a frame without a drawn inner area leaves room, by operator, in em units.
DEFAULT_INNER = {
    "⿴": (220, 200, 780, 800), "⿵": (240, 60, 780, 760), "⿶": (220, 280, 780, 960),
    "⿷": (260, 200, 960, 800), "⿸": (300, 60, 960, 720), "⿹": (60, 60, 700, 720),
    "⿺": (300, 300, 960, 960),
}


# -- the formula -------------------------------------------------------------------------------


@dataclass
class Leaf:
    cid: str  # the component drawn
    sound: bool  # written ‹morpheme›: a sound component
    text: str

    def __str__(self):
        return self.text


@dataclass
class Node:
    op: str
    kids: list = field(default_factory=list)

    def __str__(self):
        return self.op + "".join(str(k) for k in self.kids)


def sound_component(morpheme: str) -> str:
    """The component that is the character of ``morpheme``, used for its reading."""
    for c in K.COMPONENTS.values():
        if c.char == morpheme:
            return c.id
    raise ValueError(f"‹{morpheme}›: no component is the character of {morpheme!r}")


TOKEN = re.compile(r"\{([a-z]+)\}|‹([a-z]+)›|([⿰-⿻])")


def parse(formula: str):
    """The tree of a formula. A formula that is a meaning compound's own layout is that
    compound, one leaf."""
    return _parse(formula, collapse=True)


def _parse_raw(formula: str):
    return _parse(formula, collapse=False)


def _parse(formula: str, collapse: bool):
    tokens = []
    pos = 0
    while pos < len(formula):
        m = TOKEN.match(formula, pos)
        if not m:
            raise ValueError(f"{formula!r}: cannot read from {formula[pos:]!r}")
        tokens.append(m)
        pos = m.end()

    def take(i):
        m = tokens[i]
        if m.group(1):
            if m.group(1) not in K.COMPONENTS:
                raise ValueError(f"{formula!r}: no component {m.group(1)!r}")
            return Leaf(m.group(1), False, m.group(0)), i + 1
        if m.group(2):
            return Leaf(sound_component(m.group(2)), True, m.group(0)), i + 1
        node = Node(m.group(3))
        i += 1
        for _ in range(OPERATORS[node.op]):
            if i >= len(tokens):
                raise ValueError(f"{formula!r}: {node.op} lacks an operand")
            kid, i = take(i)
            node.kids.append(kid)
        return node, i

    tree, end = take(0)
    if end != len(tokens):
        raise ValueError(f"{formula!r}: something follows the whole formula")
    whole = compound_of(formula) if collapse else None
    return Leaf(whole, False, formula) if whole else tree


def compound_of(formula: str) -> str | None:
    """The meaning compound whose layout is ``formula``, if one is."""
    for c in K.COMPONENTS.values():
        if c.idc == formula:
            return c.id
    return None


def expansion(cid: str):
    """A meaning compound is laid out from its formula by this engine, so the character
    and the sound component are one drawing. A compound drawn stroke by stroke (ten)
    is a leaf like any other."""
    comp = K.COMPONENTS[cid]
    if not comp.idc or comp.standalone.strokes:
        return None
    tree = parse_tree(comp.idc)
    return tree


def parse_tree(formula: str):
    """The tree of a formula, never collapsed into its compound."""
    return _parse_raw(formula)


# -- forms, complexity and the strokes of a leaf -----------------------------------------------


def form_for(cid: str, position: str) -> tuple[K.Form, bool]:
    """The form of ``cid`` at ``position`` and whether it is drawn for that place."""
    comp = K.COMPONENTS[cid]
    if position in comp.forms:
        return comp.forms[position], True
    return comp.standalone, False


def complexity(node, position="S") -> float:
    if isinstance(node, Leaf) and expansion(node.cid) is not None:
        return complexity(expansion(node.cid))
    if isinstance(node, Leaf):
        form, _ = form_for(node.cid, position)
        return form.weight
    return sum(complexity(k) for k in node.kids)


def stroke_count(node) -> int:
    """The strokes of a laid-out tree, each part counted in the form it is drawn in."""
    return sum(form_for(p.leaf.cid, p.position)[0].count for p in place(node))


@dataclass
class Placed:
    stroke: K.Stroke
    box: tuple  # (x0, y0, w, h): the stroke's coordinates are mapped from this box ...
    into: tuple  # ... onto this one, in the form's own units


def _strokes(form: K.Form, box=None):
    """Every stroke of a form, composed forms included, with the box it is drawn in and
    the box of the form it lands in."""
    box = box or (0, 0, form.w, form.h)
    out = []
    for c, f, (a0, b0, a1, b1) in form.parts:
        sub, _ = form_for(c, f)
        x0, y0, x1, y1 = box[0], box[1], box[0] + box[2], box[1] + box[3]
        sx, sy = box[2] / form.w, box[3] / form.h
        out += _strokes(sub, (x0 + a0 * sx, y0 + b0 * sy, (a1 - a0) * sx, (b1 - b0) * sy))
    for s in form.strokes:
        out.append(Placed(s, (0, 0, form.w, form.h), box))
    return out


def _map(placed: Placed, x, y):
    b0x, b0y, bw, bh = placed.box
    i0x, i0y, iw, ih = placed.into
    return i0x + (x - b0x) * iw / bw, i0y + (y - b0y) * ih / bh


def _tracks(placed: Placed):
    out = []
    for t in placed.stroke.tracks():
        t.samples = [(*_map(placed, x, y), p) for x, y, p in t.samples]
        out.append(t)
    return out


def _bounds(tracks):
    xs = [x for t in tracks for x, _, _ in t.samples]
    ys = [y for t in tracks for _, y, _ in t.samples]
    return min(xs), min(ys), max(xs), max(ys)


# -- the contextual rules ----------------------------------------------------------------------


def _replace(placed: Placed, sid: str, x: float, y: float, **params) -> Placed:
    return Placed(K.Stroke(sid, x, y, params), placed.box, placed.into)


def contextual(strokes: list[Placed], slot: str) -> tuple[list[Placed], list[str]]:
    """Apply the rules of a part fitted to a place it has no drawing for. ``slot`` is
    ``left``, ``middle`` or anything else. Returns the strokes and what was changed."""
    changed = []
    if slot not in ("left", "middle") or not strokes:
        return strokes, changed
    tracks = [_tracks(p) for p in strokes]
    x0, y0, x1, y1 = _bounds([t for ts in tracks for t in ts])
    out = list(strokes)
    if slot == "left":
        # the lowest horizontal, when nothing lies below it, rises toward the partner
        lows = [(i, _bounds(ts)) for i, (p, ts) in enumerate(zip(strokes, tracks)) if p.stroke.sid == "horizontal"]
        if lows:
            i, (bx0, by0, bx1, by1) = min(lows, key=lambda e: e[1][1])
            below = [b for j, ts in enumerate(tracks) if j != i for b in [_bounds(ts)] if b[1] < by0 - 30]
            if not below:
                p = strokes[i]
                length = max(80.0, min(320.0, p.stroke.params.get("l", 480) * 0.5))
                out[i] = _replace(p, "rise", p.stroke.x, p.stroke.y - 10, l=length, a=26)
                changed.append(f"{p.stroke.sid} > rise")
    for i, (p, ts) in enumerate(zip(strokes, tracks)):
        if p.stroke.sid in ("fall", "fall-flat"):
            bx0, by0, bx1, by1 = _bounds(ts)
            if bx1 >= x1 - 0.12 * (x1 - x0):
                out[i] = _replace(p, "dot", p.stroke.x + 10, p.stroke.y, l=110, a=-45)
                changed.append(f"{p.stroke.sid} > dot")
    return out, changed


# -- placing -----------------------------------------------------------------------------------


@dataclass
class Part:
    leaf: Leaf
    position: str  # the form asked for
    slot: tuple  # (x0, y0, x1, y1), em units: where its ink goes
    context: str = ""  # left, middle, right, top, bottom, frame, inside, whole
    drawn: bool = True  # the form is drawn for this place
    rules: list = field(default_factory=list)  # contextual changes made
    grow: float = 1.3  # the most the part is enlarged past its drawing's own scale


def compound_overrides(cid: str) -> dict:
    import characters

    ch = characters.BY_MORPHEME.get(cid)
    return ch.overrides if ch else {}


def _share(a, b, a_sound, b_sound, default=0.38) -> float:
    """The first operand's share of a two-way split."""
    if a_sound and not b_sound:
        base = 1 - default
    elif b_sound and not a_sound:
        base = default
    else:
        base = 0.5
    ca, cb = max(a, 0.5) ** 0.75, max(b, 0.5) ** 0.75
    raw = ca / (ca + cb)
    return min(0.62, max(0.3, 0.55 * base + 0.45 * raw))


def _is_sound(node) -> bool:
    return isinstance(node, Leaf) and node.sound


def place(tree, box=None, context="whole", overrides=None) -> list[Part]:
    """The leaves of ``tree`` and the slot each one's ink is fitted to."""
    overrides = overrides or {}
    box = box or (MARGIN_X, MARGIN_Y, EM - MARGIN_X, EM - MARGIN_Y)
    if isinstance(tree, Leaf) and expansion(tree.cid) is not None:
        own = compound_overrides(tree.cid)
        return place(expansion(tree.cid), box, context, {**own, **overrides} if context == "whole" else own)
    if isinstance(tree, Leaf):
        # a part takes the form drawn for its place, or else one drawn for a place of the
        # same shape: a flat form for any row of a column, a narrow one for any column
        tall = box[3] - box[1] > box[2] - box[0]
        wanted = {"left": "L", "right": "R", "top": "T", "bottom": "BT",
                  "middle": "LR" if tall else "TB"}.get(context, "S")
        forms = K.COMPONENTS[tree.cid].forms
        position = next((f for f in wanted if f in forms), wanted[0] if wanted != "S" else "S")
        if tree.sound and "S" in K.COMPONENTS[tree.cid].forms:
            # a sound component is the whole character, narrowed, never its radical form
            position = "S"
        _, drawn = form_for(tree.cid, position)
        drawn = drawn and position != "S" or context in ("whole", "inside")
        part = Part(tree, overrides.get("form", position), overrides.get("slot", box), context, drawn)
        part.grow = overrides.get("grow", MAX_GROW)
        return [part]
    x0, y0, x1, y1 = box
    op, kids = tree.op, tree.kids
    out = []
    if op in ("⿰", "⿱"):
        across = op == "⿰"
        pa, pb = ("L", "R") if across else ("T", "B")
        a, b = complexity(kids[0], pa), complexity(kids[1], pb)
        share = overrides.get("split", _share(a, b, _is_sound(kids[0]), _is_sound(kids[1])))
        if across:
            cut = x0 + (x1 - x0 - GAP) * share
            out += place(kids[0], (x0, y0, cut, y1), "left", overrides.get("first", {}))
            out += place(kids[1], (cut + GAP, y0, x1, y1), "right", overrides.get("second", {}))
        else:
            cut = y1 - (y1 - y0 - GAP) * share
            out += place(kids[0], (x0, cut, x1, y1), "top", overrides.get("first", {}))
            out += place(kids[1], (x0, y0, x1, cut - GAP), "bottom", overrides.get("second", {}))
    elif op in ("⿲", "⿳"):
        across = op == "⿲"
        weights = [max(complexity(k), 1.0) ** 0.75 for k in kids]
        shares = overrides.get("splits") or [w / sum(weights) for w in weights]
        span = (x1 - x0 if across else y1 - y0) - 2 * GAP
        names = ("left", "middle", "right") if across else ("top", "middle", "bottom")
        at = x0 if across else y1
        each = overrides.get("parts", [{}] * len(kids))
        for kid, share, name, own in zip(kids, shares, names, each):
            size = span * share
            if across:
                out += place(kid, (at, y0, at + size, y1), name, own)
                at += size + GAP
            else:
                out += place(kid, (x0, at - size, x1, at), name, own)
                at -= size + GAP
    elif op in ENCLOSURES:
        frame, inside = kids
        if not isinstance(frame, Leaf):
            raise ValueError(f"{tree}: an enclosure's frame must be one component")
        form, drawn = form_for(frame.cid, op)
        a0, b0, a1, b1 = form.inner or DEFAULT_INNER[op]
        sx, sy = (x1 - x0) / form.w, (y1 - y0) / form.h
        inner = (x0 + a0 * sx, y0 + b0 * sy, x0 + a1 * sx, y0 + b1 * sy)
        inner = overrides.get("inner", inner)
        contents = place(inside, inner, "inside")
        # stroke order: outside before inside, but a frame that closes below is written last
        if op in CLOSE_LAST:
            out += contents + [Part(frame, op, box, "frame", drawn)]
        else:
            out += [Part(frame, op, box, "frame", drawn)] + contents
    elif op == "⿻":
        for kid in kids:
            out += place(kid, box, "whole")
    else:
        raise ValueError(f"no operator {op!r}")
    return out


# -- fitting and rendering ---------------------------------------------------------------------


def _fit(tracks, slot, native=None, grow=MAX_GROW):
    """Map tracks so their brush paths fill ``slot`` less the ink's reach. ``native`` is
    the scale, x and y, that maps the form's own box onto the slot: no part is
    enlarged past ``MAX_GROW`` times it, so a sparse form keeps the room it was drawn with."""
    x0, y0, x1, y1 = _bounds(tracks)
    s0, t0, s1, t1 = slot
    s0, t0, s1, t1 = s0 + INSET, t0 + INSET, s1 - INSET, t1 - INSET
    w, h = max(x1 - x0, 1.0), max(y1 - y0, 1.0)
    sx, sy = (s1 - s0) / w, (t1 - t0) / h
    if native:
        sx, sy = min(sx, native[0] * grow), min(sy, native[1] * grow)
    if sy > sx * MAX_SQUEEZE:
        sy = sx * MAX_SQUEEZE
    elif sx > sy * MAX_SQUEEZE:
        sx = sy * MAX_SQUEEZE
    ox = s0 + ((s1 - s0) - w * sx) / 2
    spare = (t1 - t0) - h * sy
    oy = t0 + spare * 0.56  # a little above the middle
    for t in tracks:
        t.samples = [(ox + (x - x0) * sx, oy + (y - y0) * sy, p) for x, y, p in t.samples]
    return tracks


def _frame_strokes(part: Part):
    """A frame is not fitted to its ink: its own box is mapped onto the slot, so its
    inner area lands where the layout put the contents."""
    form, _ = form_for(part.leaf.cid, part.position)
    s0, t0, s1, t1 = part.slot
    out = []
    for placed in _strokes(form):
        group = _tracks(placed)
        for t in group:
            t.samples = [(s0 + x * (s1 - s0) / form.w, t0 + y * (t1 - t0) / form.h, p) for x, y, p in t.samples]
        out.append((placed.stroke, group))
    return out


def part_strokes(part: Part):
    """The part's strokes in stroke order, each ``(stroke, tracks)``, fitted to its slot."""
    if part.context == "frame":
        return _frame_strokes(part)
    form, drawn = form_for(part.leaf.cid, part.position)
    strokes = _strokes(form)
    if not drawn:
        strokes, part.rules = contextual(strokes, part.context)
    groups = [(p.stroke, _tracks(p)) for p in strokes]
    s0, t0, s1, t1 = part.slot
    _fit([t for _, g in groups for t in g], part.slot, ((s1 - s0) / form.w, (t1 - t0) / form.h), part.grow)
    return groups


def part_tracks(part: Part):
    return [t for _, g in part_strokes(part) for t in g]


def scale_for(count: int) -> float:
    """A character of few strokes sits smaller in its square."""
    return {1: 0.72, 2: 0.78, 3: 0.84, 4: 0.88, 5: 0.92, 6: 0.96}.get(count, 1.0)


def strokes_of(formula: str, overrides=None):
    """Every stroke of the character in stroke order, as ``(part index, stroke, tracks)``,
    in em units; and the parts and the stroke count."""
    overrides = overrides or {}
    tree = parse(formula)
    parts = place(tree, overrides=overrides)
    out = [(i, st, g) for i, part in enumerate(parts) for st, g in part_strokes(part)]
    count = len(out)
    k = overrides.get("scale", scale_for(count))
    cx, cy = EM / 2, EM / 2 + LIFT
    for _, _, g in out:
        for t in g:
            t.samples = [(cx + (x - EM / 2) * k, cy + (y - EM / 2) * k, p) for x, y, p in t.samples]
    return out, parts, count


def tracks_of(formula: str, overrides=None):
    strokes, parts, count = strokes_of(formula, overrides)
    return [t for _, _, g in strokes for t in g], parts, count


def outline(tracks, style: S.Style) -> pathops.Path:
    """The brush outline of the tracks. Skia's simplify can fail when two footprints
    meet exactly at a tangent; then every sample is moved by a few hundredths of a
    unit, in a fixed pattern, and the outline is taken again."""
    for k in range(6):
        if k:
            for j, t in enumerate(tracks):
                t.samples = [(x + 0.01 * math.sin(i * 1.7 + j), y + 0.01 * math.cos(i * 2.3 + j), p)
                             for i, (x, y, p) in enumerate(t.samples)]
        try:
            return S.outline(tracks, style)
        except pathops.PathOpsError:
            continue
    raise pathops.PathOpsError("the character's outline could not be simplified")


def render(formula: str, overrides=None, style: S.Style | None = None) -> pathops.Path:
    tracks, _, count = tracks_of(formula, overrides)
    return outline(tracks, style or K.weight_for(count))


def render_char(morpheme: str, style: S.Style | None = None) -> pathops.Path:
    import characters as C

    ch = C.BY_MORPHEME[morpheme]
    return render(ch.formula, ch.overrides, style)


def describe(formula: str, overrides=None) -> list[str]:
    """One line per part: the component, its form, its slot and any rule applied."""
    _, parts, _ = tracks_of(formula, overrides)
    out = []
    for p in parts:
        slot = ", ".join(f"{v:.0f}" for v in p.slot)
        note = f" ({'; '.join(p.rules)})" if p.rules else ""
        out.append(f"{p.leaf} as {p.position}{'' if p.drawn else ' squeezed'} in [{slot}]{note}")
    return out


def ink_bounds(path: pathops.Path):
    xs, ys = [], []
    for poly in S.contours(path):
        xs += [x for x, _ in poly]
        ys += [y for _, y in poly]
    return (min(xs), min(ys), max(xs), max(ys)) if xs else None
