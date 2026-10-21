# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Add quadrat and cartouche layout to a built Khelathi Zethu Glyphs font.

    .venv/bin/python tools/khelathi-zethu-glyphs/layout.py fonts/KhelathiZethuGlyphs-Regular.ttf

`build.sh` runs this on the font fontmake writes, before the Macintosh names and the
WOFF2. It adds the glyphs the layout works with, compiles the source's ``features.fea``
together with the layout's lookups, and writes the font back in place. The result
depends only on the font it reads, so a build is reproducible.

**The text.** A quadrat is typed with Unicode's Egyptian Hieroglyph Format Controls:
the vertical and horizontal joiners, the four corner insertions and the begin and end
segment. A cartouche is a begin enclosure and an end enclosure round its signs. Each
control is mapped twice, at its Unicode code point and at the same offset from U+1EC60
in the font's own block (``controls`` in encoding.json), because a browser shapes a run
of one script at a time, and the Unicode controls belong to the Egyptian script while
Zethu's signs belong to none: only the controls in Zethu's own block reach the same
shaping run as the signs.

**The model.** Each sign has a natural size in eighths of a quadrat: its ink width and
height plus a margin, rounded up. A horizontal group is its items side by side, as wide
as their widths together and as tall as the tallest; a vertical group is its rows one
above another. A segment is one item made of the group inside it. A corner insertion
scales its argument into the quarter of the core's cell at the named corner, and the
pair is as large as the core. The quadrat is then scaled as a whole, keeping every
proportion, so that it fits a square of one quadrat, and is never enlarged; items are
centred across their group, and the quadrat on its square. ``reference()`` computes
the same layout in Python, and the guard compares the two.

**The shaping.** HarfBuzz and the browsers shape these right-to-left code points in
visual order, reversed, because the script they belong to runs left to right, so every
rule here reads the run left to right: a vertical group from the bottom row up, a
segment from its end control to its begin control. The lookups sit in ``rclt`` and
``dist``, which every HarfBuzz shaper applies to horizontal text and no style sheet
turns off. In order:

1. Each control takes its nesting depth; each sign in a quadrat is followed by a size
   token, and the first sign of a quadrat is preceded by a quadrat start token.
2. Each sign and segment control is followed by its tokens: one set per level of
   nesting it lies in. Each pass rewrites one kind of token, forward (a chaining
   substitution reads the tokens it has already rewritten) or backward (a reverse
   chaining substitution), and sees only its own tokens and the controls of its level,
   through a mark filtering set. The deepest level is computed first, so a segment
   knows its size before its own level lays it out.
3. The quadrat's size gives its scale; the scale is carried back over the quadrat,
   each natural length becomes a length in the font, and each sign becomes a copy
   of itself at that scale.
4. Positioning adds the offsets that the tokens hold to their sign, in ``dist``.
5. A cartouche's controls become the cord's ends, and every glyph between them is
   followed by a piece of cord as long as its advance.

The tokens are empty, zero-width marks. A sign in a quadrat is an empty-advance copy
drawn about the quadrat's centre, and the quadrat's advance is carried by its two
half-width carriers.
"""

import argparse
import json
import math
import sys
from pathlib import Path

import pathops
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables import otTables
from fontTools.ttLib.tables._g_l_y_f import Glyph, GlyphComponent

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
ENCODING = HERE / "encoding.json"
CONTROLS = HERE / "controls.json"
FEATURES = ROOT / "sources" / "KhelathiZethuGlyphs.ufo" / "features.fea"

QUADRAT = 770  # one quadrat, in font units (tools/vertical.py's scale of 1000)
EIGHTH = QUADRAT / 8  # the natural unit
MARGIN = 35  # added to a sign's ink before it is rounded up to eighths
MAX = 24  # the largest natural length: three quadrats
DEPTH = 3  # levels of nesting: the quadrat and two segments inside it
SIDE = 31  # the sidebearing a quadrat stands at, as every sign does
UNIT = 8  # the length of one step of a final offset, in font units
CENTRE_Y = QUADRAT / 2
STEPS = 13  # the scales a sign is drawn at: 2 ** (-j / 6), from 1 to 1/4
RATIO = 2 ** (-1 / 6)

# Hairline of the drawing and the cord's measures, in font units.
HAIR = 12
CORD = 26  # the cord's width
CORD_GAP = 3 * HAIR  # clear space between the signs and the cord
CORD_STEP = 8  # cord pieces come in lengths of this many units

CONTROL_NAMES = {
    "vj": "ctl.vj",
    "hj": "ctl.hj",
    "its": "ctl.its",
    "ibs": "ctl.ibs",
    "ite": "ctl.ite",
    "ibe": "ctl.ibe",
    "bs": "ctl.bs",
    "es": "ctl.es",
    "be": "ctl.be",
    "ee": "ctl.ee",
}
JOINERS = ["vj", "hj"]
INSERTS = ["its", "ibs", "ite", "ibe"]
# Which side of the core a corner insertion sits on, in the line as it is seen.
# The start of a right-to-left line is its right.
CORNER = {"its": (1, 1), "ibs": (1, -1), "ite": (-1, 1), "ibe": (-1, -1)}


def load_encoding():
    return json.loads(ENCODING.read_text(encoding="utf-8"))


def load_controls():
    return json.loads(CONTROLS.read_text(encoding="utf-8"))["controls"]


def gname(sid: str, v: str) -> str:
    return "z" + sid.replace("-", "_") + "." + v


def step_of(scale: float) -> int:
    """The largest drawn scale no larger than `scale`, as its step."""
    if scale >= 1:
        return 0
    j = math.ceil(math.log(scale) / math.log(RATIO) - 1e-9)
    return min(j, STEPS - 1)


def step_scale(j: int) -> float:
    return RATIO**j


def natural(length: float) -> int:
    return max(1, min(8, math.ceil((length + MARGIN) / EIGHTH - 1e-9)))


def corner_step(core: int, arg: int) -> int:
    """The step that fits an argument of natural length `arg` into half a core of `core`."""
    return step_of(min(1.0, core / (2 * arg)))


# -- the model the shaping and the guard share --------------------------------------------


class Sign:
    """A drawn form: its glyph, its ink centre and its natural size in eighths."""

    def __init__(self, glyph, bounds):
        x0, y0, x1, y1 = bounds
        self.glyph = glyph
        self.cx, self.cy = (x0 + x1) / 2, (y0 + y1) / 2
        self.w, self.h = natural(x1 - x0), natural(y1 - y0)


def signs_of(font: TTFont, enc) -> dict[str, Sign]:
    glyphs = font.getGlyphSet()
    out = {}
    for e in enc["signs"]:
        if not e["drawn"]:
            continue
        for v in e["variants"]:
            name = gname(e["id"], v)
            pen = BoundsPen(glyphs)
            glyphs[name].draw(pen)
            out[name] = Sign(name, pen.bounds)
    return out


# A parsed quadrat, in logical order. A node is ("sign", glyph), ("h", [items]),
# ("v", [rows]), ("seg", node) or ("ins", corner, core, arg).


def parse(items: list):
    """Parse one quadrat's tokens (glyph names and control keys, logical order) into a tree.

    Insertion binds tighter than the horizontal joiner, which binds tighter than the
    vertical joiner; a segment is a bracketed group."""
    pos = 0

    def atom():
        nonlocal pos
        t = items[pos]
        if t == "bs":
            pos += 1
            inner = vgroup()
            if pos >= len(items) or items[pos] != "es":
                raise ValueError("an unclosed segment")
            pos += 1
            return ("seg", inner)
        if t in CONTROL_NAMES:
            raise ValueError(f"a control {t} where a sign belongs")
        pos += 1
        return ("sign", t)

    def item():
        nonlocal pos
        core = atom()
        if pos < len(items) and items[pos] in INSERTS:
            corner = items[pos]
            pos += 1
            arg = atom()
            return ("ins", corner, core, arg)
        return core

    def hgroup():
        nonlocal pos
        out = [item()]
        while pos < len(items) and items[pos] == "hj":
            pos += 1
            out.append(item())
        return ("h", out) if len(out) > 1 else out[0]

    def vgroup():
        nonlocal pos
        out = [hgroup()]
        while pos < len(items) and items[pos] == "vj":
            pos += 1
            out.append(hgroup())
        return ("v", out) if len(out) > 1 else out[0]

    tree = vgroup()
    if pos != len(items):
        raise ValueError(f"unexpected {items[pos]}")
    return tree


def size(node, signs) -> tuple[int, int]:
    kind = node[0]
    if kind == "sign":
        s = signs[node[1]]
        return s.w, s.h
    if kind == "seg":
        return size(node[1], signs)
    if kind == "ins":
        return size(node[2], signs)
    sizes = [size(n, signs) for n in node[1]]
    if kind == "h":
        return min(MAX, sum(w for w, _ in sizes)), max(h for _, h in sizes)
    return max(w for w, _ in sizes), min(MAX, sum(h for _, h in sizes))


def place(node, signs, cx, cy, step, out):
    """Append (glyph, centre x, centre y, step) for each sign of `node`, centred at
    (cx, cy) in natural units of the quadrat, drawn at the scale of `step` steps more than
    the quadrat's."""
    kind = node[0]
    if kind == "sign":
        out.append((node[1], cx, cy, step))
    elif kind == "seg":
        place(node[1], signs, cx, cy, step, out)
    elif kind == "ins":
        _, corner, core, arg = node
        place(core, signs, cx, cy, step, out)
        (wc, hc), (wa, ha) = size(core, signs), size(arg, signs)
        j = max(corner_step(wc, wa), corner_step(hc, ha))
        k = step_scale(j)
        sx, sy = CORNER[corner]
        place(arg, signs, cx + sx * (wc - k * wa) / 2, cy + sy * (hc - k * ha) / 2, step + j, out)
    elif kind == "h":
        sizes = [size(n, signs) for n in node[1]]
        total = sum(w for w, _ in sizes)
        left = -total / 2
        # a right-to-left line: the first item stands at the right
        for n, (w, _) in reversed(list(zip(node[1], sizes))):
            place(n, signs, cx + left + w / 2, cy, step, out)
            left += w
    else:
        sizes = [size(n, signs) for n in node[1]]
        total = sum(h for _, h in sizes)
        top = total / 2
        for n, (_, h) in zip(node[1], sizes):
            place(n, signs, cx, cy + top - h / 2, step, out)
            top -= h


def reference(items: list, signs) -> dict:
    """The layout of one quadrat in font units: its advance and, for each sign in visual
    order (left to right), its glyph, the centre of its ink relative to the quadrat's
    left edge and baseline, and the step of the scale it is drawn at."""
    tree = parse(items)
    w, h = size(tree, signs)
    k = max(8, w, h)
    out = []
    place(tree, signs, 0.0, 0.0, step_of(8 / k), out)
    centre = carrier_half(k, w)
    placed = [
        (g, centre + x * EIGHTH * 8 / k, CENTRE_Y + y * EIGHTH * 8 / k, min(STEPS - 1, j)) for g, x, y, j in out
    ]
    placed.sort(key=lambda p: p[1])
    return {"advance": 2 * carrier_half(k, w), "signs": placed}


def carrier_half(k: int, w: int) -> int:
    """The advance of each of a quadrat's two carriers."""
    return 2 * round((8 / k * w * EIGHTH / 2) / 2) + SIDE


# -- glyph names ---------------------------------------------------------------------------


def sv(v: int) -> str:
    return f"m{-v}" if v < 0 else str(v)


def tok(kind: str, level, value) -> str:
    lev = "" if level is None else str(level)
    return f"q{kind}{lev}.{value}"


def ctl(key: str, depth=None) -> str:
    return CONTROL_NAMES[key] + ("" if depth is None else f".d{depth}")


def comp(glyph: str, j: int) -> str:
    return f"{glyph}.s{j}"


# The kinds of token each entity carries at each level, in order. CH and CW sit on a
# segment's closing control, OW on its opening one.
LEVEL_KINDS = ["ch", "cw", "xf", "yf", "ym", "xb", "ow", "yr", "yh", "wm", "wb"]
# Kinds whose value becomes an offset, with the multiplier from natural to final units.
OUTPUTS = {"xf": 0.5, "xb": -0.5, "yf": 1.0, "yr": 0.5, "yh": -0.5}
VALUES = range(MAX + 1)


class Fea:
    def __init__(self):
        self.lines = []
        self.lookups = []  # names, in order, for the feature
        self.classes = {}
        self.anon = 0

    def cls(self, name: str, glyphs) -> str:
        glyphs = list(dict.fromkeys(glyphs))
        if name not in self.classes:
            self.classes[name] = glyphs
            self.lines.append(f"@{name} = [{' '.join(glyphs)}];")
        return "@" + name

    def lookup(self, name: str, rules: list[str], flags: str = "", feature=True):
        body = [f"lookup {name} useExtension {{"]
        if flags:
            body.append(f"  lookupflag {flags};")
        body += ["  " + r for r in rules]
        body.append(f"}} {name};")
        self.lines += body
        if feature:
            self.lookups.append(name)
        return name

    def sub(self) -> str:
        self.anon += 1
        return f"L{self.anon}"


class Layout:
    """The glyphs and the feature code of the layout, built from a font's signs."""

    def __init__(self, font: TTFont, enc):
        self.enc = enc
        self.signs = signs_of(font, enc)
        self.forms = sorted(self.signs)
        self.order = font.getGlyphOrder()
        self.hmtx = font["hmtx"].metrics
        self.new = {}  # glyph name -> ("empty"|"comp"|"carrier"|"cord"|"cap", data)
        self.marks = []
        self.bases = []
        self.fea = Fea()
        self.fin_values = {}

    # -- glyph bookkeeping --------------------------------------------------------------

    def mark(self, name: str) -> str:
        if name not in self.new:
            self.new[name] = ("empty", None)
            self.marks.append(name)
        return name

    def base(self, name: str, kind: str, data) -> str:
        if name not in self.new:
            self.new[name] = (kind, data)
            self.bases.append(name)
        return name

    def family(self, kind, level, values) -> list[str]:
        return [self.mark(tok(kind, level, sv(v))) for v in values]

    # -- the feature code ---------------------------------------------------------------

    def build(self) -> str:
        f = self.fea
        for key in CONTROL_NAMES:
            if ctl(key) not in self.order:
                raise SystemExit(f"the font has no glyph {ctl(key)}")
        for key in JOINERS + INSERTS + ["bs", "es"]:
            for d in range(DEPTH):
                self.mark(ctl(key, d))
        self.mark("qqs")
        self.mark("qqe")
        for w in range(1, 9):
            for h in range(1, 9):
                self.mark(f"qe.w{w}h{h}")
        self.tokenize()
        for level in reversed(range(DEPTH)):
            if level < DEPTH - 1:
                self.deposits(level)
            self.level(level)
        self.insertions()
        self.scale()
        self.convert()
        self.composites()
        self.carriers()
        self.cartouche()
        gsub = list(f.lookups)
        f.lookups = []
        self.positions()
        gpos = list(f.lookups)
        head = [
            "# The quadrat and cartouche layout, written by tools/khelathi-zethu-glyphs/layout.py.",
        ]
        classes_gdef = [
            "table GDEF {",
            f"  GlyphClassDef [{' '.join(self.base_glyphs())}], , [{' '.join(self.mark_glyphs())}], ;",
            "} GDEF;",
        ]
        feats = ["feature rclt {"] + [f"  lookup {n};" for n in gsub] + ["} rclt;"]
        feats += ["feature dist {"] + [f"  lookup {n};" for n in gpos] + ["} dist;"]
        return "\n".join(head + f.lines + classes_gdef + feats) + "\n"

    def base_glyphs(self):
        controls = set(CONTROL_NAMES.values())
        old = [g for g in self.order if g not in controls and g not in ("ignorable", "ignorable.sub")]
        return old + self.bases

    def mark_glyphs(self):
        return list(CONTROL_NAMES.values()) + ["ignorable", "ignorable.sub"] + self.marks

    # Classes used throughout.
    def c(self, name, glyphs):
        return self.fea.cls(name, glyphs)

    def ctls(self, keys, depths) -> list[str]:
        return [ctl(k, d) for k in keys for d in depths]

    # -- 1. depth and tokens ------------------------------------------------------------

    def tokenize(self):
        f = self.fea
        signs = self.c("SIGN", self.forms)
        raw = {k: ctl(k) for k in JOINERS + INSERTS + ["bs", "es"]}
        allctl = self.c("CTLQ", list(raw.values()) + self.ctls(JOINERS + INSERTS + ["bs", "es"], range(DEPTH)))
        join = JOINERS + INSERTS
        # T1: each control takes its depth. "after" is the depth of the position after a
        # control: one deeper after an opening control (the end segment, first in the run).
        rules = []

        def target(key, after):
            return after - 1 if key == "bs" else after

        for key, g in raw.items():
            for prev in join + ["es", "bs"]:
                for d in range(DEPTH):
                    after = d + 1 if prev == "es" else d
                    t = target(key, after)
                    if 0 <= t < DEPTH:
                        if prev != "bs":
                            rules.append(f"sub {ctl(prev, d)} {signs} {g}' by {ctl(key, t)};")
            for prev in join + ["es", "bs"]:
                for d in range(DEPTH):
                    after = d + 1 if prev == "es" else d
                    t = target(key, after)
                    if 0 <= t < DEPTH:
                        rules.append(f"sub {ctl(prev, d)} {g}' by {ctl(key, t)};")
            if key != "bs":
                # a control with no sign and no control beside it stays as it is
                rules.append(f"sub {signs} {g}' by {ctl(key, 0)};")
                rules.append(f"sub {g}' [{signs} {allctl}] by {ctl(key, 0)};")
        f.lookup("depth", rules, f"UseMarkFilteringSet {allctl}")

        # T2: a sign joined to a control is followed by its size token; the first sign of a
        # quadrat is preceded by the quadrat start.
        dctl = self.ctls(join + ["bs", "es"], range(DEPTH))
        view = self.c("CTLD", dctl)
        before = self.c("JOINBEFORE", self.ctls(join + ["es"], range(DEPTH)))
        after_ = self.c("JOINAFTER", self.ctls(join + ["bs"], range(DEPTH)))
        size_rules, first_rules = [], []
        for g in self.forms:
            s = self.signs[g]
            size_rules.append(f"sub {g} by {g} qe.w{s.w}h{s.h};")
            first_rules.append(f"sub {g} by qqs {g} qe.w{s.w}h{s.h};")
        f.lookup("tok_size", size_rules, feature=False)
        f.lookup("tok_first", first_rules, feature=False)
        f.lookup(
            "tokens",
            [f"sub {before} {signs}' lookup tok_size;", f"sub {signs}' lookup tok_first {after_};"],
            f"UseMarkFilteringSet {view}",
        )

        # T3: each size token becomes the sign's list of tokens, by depth and role.
        e0 = [f"qe.w{w}h{h}" for w in range(1, 9) for h in range(1, 9)]
        E0 = self.c("E0", e0)
        expand = {}

        def expansion(depth, role, last):
            name = f"tok_x{depth}{role[0]}{int(last)}"
            if name not in expand:
                rules = []
                for w in range(1, 9):
                    for h in range(1, 9):
                        seq = self.entity(depth, role, w, h) + (["qqe"] if last else [])
                        rules.append(f"sub qe.w{w}h{h} by {' '.join(seq)};")
                f.lookup(name, rules, feature=False)
                expand[name] = True
            return name

        rules = []
        hv = lambda d: self.c(f"HV{d}", [ctl("vj", d), ctl("hj", d)])  # noqa: E731
        ins = lambda d: self.c(f"INS{d}", [ctl(k, d) for k in INSERTS])  # noqa: E731
        for d in range(DEPTH):
            prevs = [(hv(d), d, "item"), (ins(d), d, "core")]
            if d > 0:
                prevs.append((ctl("es", d - 1), d, "item"))
            nexts = [(hv(d), "item", False), (ins(d), "arg", False)]
            if d > 0:
                nexts.append((ctl("bs", d - 1), "item", False))
            for p, depth, prole in prevs:
                for n, nrole, last in nexts:
                    role = "arg" if nrole == "arg" else prole
                    if prole == "core" and nrole == "arg":
                        continue
                    rules.append(f"sub {p} {E0}' lookup {expansion(depth, role, last)} {n};")
            for p, depth, prole in prevs:
                rules.append(f"sub {p} {E0}' lookup {expansion(depth, prole, d == 0)};")
            for n, nrole, _ in nexts:
                rules.append(f"sub {E0}' lookup {expansion(d, nrole, False)} {n};")
        # The quadrat start is in view, so a quadrat's first sign never reads the last
        # control of the quadrat before it as its own.
        f.lookup("expand", rules, f"IgnoreBaseGlyphs UseMarkFilteringSet {self.c('EXPVIEW', e0 + dctl + ['qqs'])}")

        # The segment controls carry tokens too: an opening control (end segment) at the
        # start of a quadrat is preceded by the quadrat start, a closing one at its end
        # followed by the quadrat end. An empty base glyph stands between a control and
        # its tokens, so that positioning never pairs a sign with a control's token.
        blk = self.base("qblk", "empty-base", None)
        rules = []
        for d in range(DEPTH):
            o, c = ctl("es", d), ctl("bs", d)
            ol = f"tok_open{d}"
            f.lookup(ol, [f"sub {o} by {' '.join([o, blk] + self.entity(d, 'open', 0, 0))};"], feature=False)
            cl = f"tok_close{d}"
            f.lookup(cl, [f"sub {c} by {' '.join([c, blk] + self.entity(d, 'close', 0, 0))};"], feature=False)
            if d == 0:
                f.lookup("tok_open0f", [f"sub {o} by {' '.join(['qqs', o, blk] + self.entity(0, 'open', 0, 0))};"], feature=False)
                f.lookup("tok_close0l", [f"sub {c} by {' '.join([c, blk] + self.entity(0, 'close', 0, 0) + ['qqe'])};"], feature=False)
                rules.append(f"sub {self.c('JOIN0', self.ctls(join, [0]))} {o}' lookup {ol};")
                rules.append(f"sub {o}' lookup tok_open0f;")
                rules.append(f"sub {c}' lookup {cl} {self.c('JOIN0', self.ctls(join, [0]))};")
                rules.append(f"sub {c}' lookup tok_close0l;")
            else:
                rules.append(f"sub {o}' lookup {ol};")
                rules.append(f"sub {c}' lookup {cl};")
        f.lookup("segtokens", rules, f"UseMarkFilteringSet {view}")

    def entity(self, depth: int, role: str, w: int, h: int) -> list[str]:
        """The tokens that follow an entity of `role` at `depth`: a sign (item, core or
        insertion argument) or a segment control (open or close)."""
        out = [self.mark("qsk.u"), self.mark("qsw.u")]
        for level in range(depth + 1):
            r = role if level == depth else "pass"
            for kind in LEVEL_KINDS:
                g = self.initial(kind, level, r, w, h)
                if g:
                    out.append(self.mark(g))
        if role == "core":
            out += [self.mark(f"qczx.{w}"), self.mark(f"qczy.{h}")]
        if role == "arg":
            out += [
                self.mark(f"qaxi.i{w}"),
                self.mark(f"qayi.i{h}"),
                self.mark("qk.u"),
                self.mark("qdx1.u"),
                self.mark(f"qdx2.i{w}"),
                self.mark("qdy1.u"),
                self.mark(f"qdy2.i{h}"),
            ]
        return out

    def initial(self, kind, level, role, w, h):
        item = role in ("item", "core")
        t = lambda s: tok(kind, level, s)  # noqa: E731
        if kind == "ch" or kind == "cw":
            return t("u") if role == "close" else None
        if kind == "ow":
            return t("u") if role == "open" else None
        if kind == "xf":
            if role == "arg":
                return tok("xa", level, "u")
            return t(f"i{w}") if item else t("c") if role == "close" else t("p")
        if kind == "xb":
            if role == "arg":
                return tok("xc", level, "u")
            return t(f"i{w}") if item else t("o") if role == "open" else t("p")
        if kind == "ym":
            return t(f"i{h}") if item else t("c") if role == "close" else t("p")
        if kind in ("wm", "wb"):
            return None if role == "arg" else t("u")
        return t("u")

    # -- 2. the passes of one level -----------------------------------------------------

    def vals(self, kind, level):
        return self.family(kind, level, VALUES)

    def deposits(self, level):
        """A segment's closing control at `level` learns the width and height of the group
        inside it, and its opening control the width."""
        f = self.fea
        inner = level + 1
        wm, yh, wb = self.vals("wm", inner), self.vals("yh", inner), self.vals("wb", inner)
        cw, ch, ow = self.vals("cw", level), self.vals("ch", level), self.vals("ow", level)
        for kind, src, dst, fwd in (("cw", wm, cw, True), ("ch", yh, ch, True), ("ow", wb, ow, False)):
            u = tok(kind, level, "u")
            view = self.c(f"DEP_{kind}{level}", src + [u] + dst)
            if fwd:
                rules = [f"sub {s} {u}' by {d};" for s, d in zip(src, dst)]
            else:
                rules = [f"sub {u}' {s} by {d};" for s, d in zip(src, dst)]
            f.lookup(f"dep_{kind}{level}", rules, f"IgnoreBaseGlyphs UseMarkFilteringSet {view}")

    def level(self, lv):
        f = self.fea
        gs = ["qqs"] if lv == 0 else [ctl("es", lv - 1)]
        ge = ["qqe"] if lv == 0 else [ctl("bs", lv - 1)]
        vj = ctl("vj", lv)
        cap = lambda v: min(MAX, v)  # noqa: E731
        V = lambda k: self.vals(k, lv)  # noqa: E731
        T = lambda k, s: self.mark(tok(k, lv, s))  # noqa: E731
        items = lambda k: [T(k, f"i{w}") for w in range(1, 9)]  # noqa: E731
        flags = lambda name, glyphs: f"IgnoreBaseGlyphs UseMarkFilteringSet {self.c(name, glyphs)}"  # noqa: E731
        start = self.c(f"START{lv}", gs + [vj])

        # P1 XF, forward: the width of the row up to and including each entity.
        xf, cw = V("xf"), V("cw")
        rules = []
        for v in VALUES:
            # one class per rule input, so the lookup compiles as a class-based subtable
            outs = [xf[cap(v + w)] for w in range(1, 9)] + [xf[v]]
            rules.append(f"sub {xf[v]} [{' '.join(items('xf') + [T('xf', 'p')])}]' by [{' '.join(outs)}];")
            for w in VALUES:
                rules.append(f"sub {xf[v]} {cw[w]} {T('xf', 'c')}' by {xf[cap(v + w)]};")
        outs = [xf[w] for w in range(1, 9)] + [xf[0]]
        rules.append(f"sub {start} [{' '.join(items('xf') + [T('xf', 'p')])}]' by [{' '.join(outs)}];")
        for w in VALUES:
            rules.append(f"sub {start} {cw[w]} {T('xf', 'c')}' by {xf[cap(w)]};")
        view = xf + items("xf") + [T("xf", "p"), T("xf", "c")] + cw + gs + ge + [vj]
        f.lookup(f"xf{lv}", rules, flags(f"VXF{lv}", view))

        # P2 XB, backward: the width of the row from each entity to its end.
        xb, ow = V("xb"), V("ow")
        end = self.c(f"END{lv}", ge + [vj])
        # An opening control first takes the segment's width into its own token, so that
        # the backward pass maps whole classes: a reverse chaining substitution has one
        # subtable for each context.
        opened = [T("xb", f"o{w}") for w in VALUES]
        rules = [f"sub {T('xb', 'o')}' {a} by {b};" for a, b in zip(ow, opened)]
        f.lookup(f"xbo{lv}", rules, flags(f"VXBO{lv}", [T("xb", "o")] + ow))
        widths = items("xb") + opened
        adds = [w for w in range(1, 9)] + list(VALUES)
        rules = []
        for v in VALUES:
            outs = [xb[cap(v + w)] for w in adds]
            rules.append(f"rsub [{' '.join(widths)}]' {xb[v]} by [{' '.join(outs)}];")
            rules.append(f"rsub {T('xb', 'p')}' {xb[v]} by {xb[v]};")
        rules.append(f"rsub [{' '.join(widths)}]' {end} by [{' '.join(xb[cap(w)] for w in adds)}];")
        rules.append(f"rsub {T('xb', 'p')}' {end} by {xb[0]};")
        view = xb + widths + [T("xb", "p")] + gs + ge + [vj]
        f.lookup(f"xb{lv}", rules, flags(f"VXB{lv}", view))

        # P3 YM, forward: the tallest item of the row so far.
        ym, ch = V("ym"), V("ch")
        rules = []
        for v in VALUES:
            outs = [ym[max(v, h)] for h in range(1, 9)] + [ym[v]]
            rules.append(f"sub {ym[v]} [{' '.join(items('ym') + [T('ym', 'p')])}]' by [{' '.join(outs)}];")
            for h in VALUES:
                rules.append(f"sub {ym[v]} {ch[h]} {T('ym', 'c')}' by {ym[max(v, h)]};")
        outs = [ym[h] for h in range(1, 9)] + [ym[0]]
        rules.append(f"sub {start} [{' '.join(items('ym') + [T('ym', 'p')])}]' by [{' '.join(outs)}];")
        for h in VALUES:
            rules.append(f"sub {start} {ch[h]} {T('ym', 'c')}' by {ym[h]};")
        view = ym + items("ym") + [T("ym", "p"), T("ym", "c")] + ch + gs + ge + [vj]
        f.lookup(f"ym{lv}", rules, flags(f"VYM{lv}", view))

        # P4 YF, forward: the height of the rows below each entity's row.
        yf = V("yf")
        yfu = T("yf", "u")
        rules = []
        anyym = self.c(f"YMV{lv}", ym)
        for b in VALUES:
            for m in VALUES:
                rules.append(f"sub {yf[b]} {ym[m]} {yfu}' by {yf[b]};")
                rules.append(f"sub {yf[b]} {ym[m]} {vj} {yfu}' by {yf[cap(b + m)]};")
        rules.append(f"sub {self.c(f'GS{lv}', gs)} {yfu}' by {yf[0]};")
        view = yf + [yfu] + ym + gs + ge + [vj]
        f.lookup(f"yf{lv}", rules, flags(f"VYF{lv}", view))

        # P5 YR, backward: the height of each entity's row.
        yr = V("yr")
        yru = T("yr", "u")
        rules = []
        for m in VALUES:
            rules.append(f"rsub {ym[m]} {yru}' {self.c(f'END{lv}', ge + [vj])} by {yr[m]};")
            rules.append(f"rsub {yru}' {anyym} {yr[m]} by {yr[m]};")
        view = yr + [yru] + ym + ge + [vj]
        f.lookup(f"yr{lv}", rules, flags(f"VYR{lv}", view))

        # P6 YH, backward: the height of the whole group.
        yh = V("yh")
        yhu = T("yh", "u")
        anyyf = self.c(f"YFV{lv}", yf)
        gec = self.c(f"GE{lv}", ge)
        rules = []
        for b in VALUES:
            for m in VALUES:
                rules.append(f"sub {yf[b]} {ym[m]} {yhu}' {gec} by {yh[cap(b + m)]};")
        f.lookup(f"yhl{lv}", rules, flags(f"VYHL{lv}", yh + [yhu] + yf + ym + ge))
        rules = [f"rsub {yhu}' {anyyf} {anyym} {yh[hh]} by {yh[hh]};" for hh in VALUES]
        view = yh + [yhu] + yf + ym + ge
        f.lookup(f"yh{lv}", rules, flags(f"VYH{lv}", view))

        # P7 WM, forward, and P8 WB, backward: the widest row so far, from each side.
        wm, wmu = V("wm"), T("wm", "u")
        rules = []
        for p in VALUES:
            for x in VALUES:
                rules.append(f"sub {wm[p]} {xf[x]} {wmu}' by {wm[max(p, x)]};")
        for x in VALUES:
            rules.append(f"sub {self.c(f'GS{lv}', gs)} {xf[x]} {wmu}' by {wm[x]};")
        view = wm + [wmu] + xf + gs
        f.lookup(f"wm{lv}", rules, flags(f"VWM{lv}", view))
        wb, wbu = V("wb"), T("wb", "u")
        anyxb = self.c(f"XBV{lv}", xb)
        own = [T("wb", f"x{x}") for x in VALUES]
        rules = [f"sub {a} {wbu}' by {b};" for a, b in zip(xb, own)]
        f.lookup(f"wbx{lv}", rules, flags(f"VWBX{lv}", xb + [wbu]))
        rules = []
        for p in VALUES:
            rules.append(f"rsub [{' '.join(own)}]' {anyxb} {wb[p]} by [{' '.join(wb[max(p, x)] for x in VALUES)}];")
        rules.append(f"rsub [{' '.join(own)}]' {self.c(f'GE{lv}', ge)} by [{' '.join(wb)}];")
        view = wb + own + xb + ge
        f.lookup(f"wb{lv}", rules, flags(f"VWB{lv}", view))

        # P9: an insertion's argument takes its core's row widths, so it centres on the core.
        for src, dst in (("xf", "xa"), ("xb", "xc")):
            s = V(src)
            d = self.vals(dst, lv)
            u = T(dst, "u")
            insc = self.c(f"INS{lv}", [ctl(k, lv) for k in INSERTS])
            rules = [f"sub {u}' {insc} {a} by {b};" for a, b in zip(s, d)]
            view = s + d + [u] + [ctl(k, lv) for k in INSERTS]
            f.lookup(f"{dst}{lv}", rules, flags(f"V{dst.upper()}{lv}", view))

    # -- insertions ------------------------------------------------------------------------

    def insertions(self):
        f = self.fea
        insall = self.ctls(INSERTS, range(DEPTH))
        INS = self.c("INSALL", insall)
        czx = [self.mark(f"qczx.{w}") for w in range(1, 9)]
        czy = [self.mark(f"qczy.{h}") for h in range(1, 9)]
        axi_i = [self.mark(f"qaxi.i{w}") for w in range(1, 9)]
        ayi_i = [self.mark(f"qayi.i{h}") for h in range(1, 9)]
        axi = [self.mark(f"qaxi.{j}") for j in range(STEPS)]
        ayi = [self.mark(f"qayi.{j}") for j in range(STEPS)]
        flags = lambda name, glyphs: f"IgnoreBaseGlyphs UseMarkFilteringSet {self.c(name, glyphs)}"  # noqa: E731
        # I1: the step each axis allows the argument.
        rules = []
        for wa in range(1, 9):
            for wc in range(1, 9):
                rules.append(f"sub qaxi.i{wa}' {INS} qczx.{wc} by qaxi.{corner_step(wc, wa)};")
        f.lookup("ins_ax", rules, flags("VI1X", axi_i + czx + insall))
        rules = []
        for wa in range(1, 9):
            for wc in range(1, 9):
                rules.append(f"sub qayi.i{wa}' {INS} qczy.{wc} by qayi.{corner_step(wc, wa)};")
        f.lookup("ins_ay", rules, flags("VI1Y", ayi_i + czy + insall))
        # I2: the argument's step is the smaller of the two.
        rules = []
        for i in range(STEPS):
            for j in range(STEPS):
                rules.append(f"sub qaxi.{i} qayi.{j} qk.u' by {self.mark(f'qk.{max(i, j)}')};")
        f.lookup("ins_k", rules, flags("VI2", axi + ayi + ["qk.u"] + [f"qk.{j}" for j in range(STEPS)]))
        # I3: half the core's width or height, toward the corner (in quarters of an eighth).
        for axis, cz, sidx in (("x", czx, 0), ("y", czy, 1)):
            u = self.mark(f"qd{axis}1.u")
            rules = []
            for key in INSERTS:
                sgn = CORNER[key][sidx]
                ctlk = self.c(f"INS_{key}", [ctl(key, d) for d in range(DEPTH)])
                for n in range(1, 9):
                    val = sgn * n * 2
                    rules.append(f"sub {u}' {ctlk} {cz[n - 1]} by {self.mark(f'qd{axis}1.{sv(val)}')};")
            f.lookup(f"ins_d{axis}1", rules, flags(f"VI3{axis}", [u] + cz + insall))
        # I4: minus half the argument at its step.
        for axis, sidx in (("x", 0), ("y", 1)):
            rules = []
            for key in INSERTS:
                sgn = CORNER[key][sidx]
                ctlk = self.c(f"INS_{key}", [ctl(key, d) for d in range(DEPTH)])
                for n in range(1, 9):
                    for j in range(STEPS):
                        val = -sgn * round(step_scale(j) * n * 2)
                        rules.append(
                            f"sub qk.{j} qd{axis}2.i{n}' {ctlk} by {self.mark(f'qd{axis}2.{sv(val)}')};"
                        )
            k_all = [f"qk.{j}" for j in range(STEPS)]
            view = k_all + [self.mark(f"qd{axis}2.i{n}") for n in range(1, 9)] + insall
            f.lookup(f"ins_d{axis}2", rules, flags(f"VI4{axis}", view))

    # -- 3. scale ---------------------------------------------------------------------------

    def scale(self):
        f = self.fea
        yh, wm = self.vals("yh", 0), self.vals("wm", 0)
        rules = []
        for h in VALUES:
            for w in VALUES:
                k = max(8, w, h)
                rules.append(f"sub {yh[h]} {wm[w]} qqe' by {self.mark(f'qqe.k{k}w{w}')};")
        f.lookup("quadrat", rules, f"IgnoreBaseGlyphs UseMarkFilteringSet {self.c('VQE', yh + wm + ['qqe'])}")
        # The scale and the width are carried back over the quadrat by two tokens.
        qe = [f"qqe.k{k}w{w}" for k, w in self.kw()]
        ks = [self.mark(f"qsk.k{k}") for k in range(8, MAX + 1)]
        ws = [self.mark(f"qsw.w{w}") for w in VALUES]
        rules = []
        for k, g in zip(range(8, MAX + 1), ks):
            rules.append(f"rsub qsk.u' [{' '.join(f'qqe.k{k}w{w}' for w in VALUES if w <= k)}] by {g};")
            rules.append(f"rsub qsk.u' {g} by {g};")
        f.lookup("carry_k", rules, f"IgnoreBaseGlyphs UseMarkFilteringSet {self.c('VSK', qe + ks + ['qsk.u'])}")
        rules = []
        for w, g in zip(VALUES, ws):
            rules.append(f"rsub qsw.u' [{' '.join(f'qqe.k{k}w{w}' for k in range(max(8, w), MAX + 1))}] by {g};")
            rules.append(f"rsub qsw.u' {g} by {g};")
        f.lookup("carry_w", rules, f"IgnoreBaseGlyphs UseMarkFilteringSet {self.c('VSW', qe + ws + ['qsw.u'])}")
        rules = [f"sub qqs' qsk.k{k} qsw.w{w} by {self.mark(f'qqs.k{k}w{w}')};" for k, w in self.kw()]
        f.lookup("start", rules, f"IgnoreBaseGlyphs UseMarkFilteringSet {self.c('VQS', ks + ws + ['qqs'])}")

    def kw(self):
        return [(k, w) for k in range(8, MAX + 1) for w in VALUES if w <= k]

    def sc_class(self, k):
        return self.c(f"SC{k}", [f"qsk.k{k}"])

    def fin(self, kind, level, value) -> str:
        name = tok("f" + kind, level, sv(value))
        self.fin_values.setdefault((kind, level), set()).add(value)
        return self.mark(name)

    def convert(self):
        """Each natural length becomes a final offset at the quadrat's scale."""
        f = self.fea
        jobs = []
        for level in range(DEPTH):
            for kind, mult in OUTPUTS.items():
                jobs.append((kind, level, VALUES, mult, tok(kind, level, "{}")))
            jobs.append(("xa", level, VALUES, 0.5, tok("xa", level, "{}")))
            jobs.append(("xc", level, VALUES, -0.5, tok("xc", level, "{}")))
        for axis in "xy":
            jobs.append((f"d{axis}1", None, range(-16, 17), 0.25, f"qd{axis}1.{{}}"))
            jobs.append((f"d{axis}2", None, range(-16, 17), 0.25, f"qd{axis}2.{{}}"))
        for kind, level, values, mult, pattern in jobs:
            srcs = [pattern.format(sv(v)) for v in values]
            present = [(v, s) for v, s in zip(values, srcs) if s in self.new]
            if not present:
                continue
            tag = f"{kind}{'' if level is None else level}"
            rules = []
            for k in range(8, MAX + 1):
                name = f"cv_{tag}_k{k}"
                maps = []
                for v, s in present:
                    final = round(v * mult * EIGHTH * 8 / k / UNIT)
                    maps.append(f"sub {s} by {self.fin(kind, level, final)};")
                f.lookup(name, maps, feature=False)
                rules.append(f"sub {self.sc_class(k)} {self.c(f'SRC_{tag}', [s for _, s in present])}' lookup {name};")
            view = [s for _, s in present] + [g for kk in range(8, MAX + 1) for g in self.fea.classes[f"SC{kk}"]]
            f.lookup(f"cv_{tag}", rules, f"IgnoreBaseGlyphs UseMarkFilteringSet {self.c(f'VCV_{tag}', view)}")

    def composites(self):
        f = self.fea
        for j in range(STEPS):
            rules = []
            for g in self.forms:
                s = self.signs[g]
                self.base(comp(g, j), "comp", (g, step_scale(j), s.cx, s.cy))
                rules.append(f"sub {g} by {comp(g, j)};")
            f.lookup(f"comp_s{j}", rules, feature=False)
        signs = self.fea.classes["SIGN"] and "@SIGN"
        rules = []
        ks = [f"qk.{j}" for j in range(STEPS)]
        for k in range(8, MAX + 1):
            base = step_of(8 / k)
            for j in range(STEPS):
                rules.append(f"sub {signs}' lookup comp_s{min(STEPS - 1, base + j)} {self.sc_class(k)} qk.{j};")
        for k in range(8, MAX + 1):
            rules.append(f"sub {signs}' lookup comp_s{step_of(8 / k)} {self.sc_class(k)};")
        view = [g for kk in range(8, MAX + 1) for g in self.fea.classes[f"SC{kk}"]] + ks
        f.lookup("draw", rules, f"UseMarkFilteringSet {self.c('VCOMP', view)}")

    def carriers(self):
        f = self.fea
        rules = []
        for k, w in self.kw():
            half = carrier_half(k, w)
            car = self.base(f"qcar.{half}", "carrier", half)
            rules.append(f"sub qqs.k{k}w{w} by {car};")
            rules.append(f"sub qqe.k{k}w{w} by {car};")
        f.lookup("carriers", rules)

    # -- 5. the cartouche ----------------------------------------------------------------

    def cartouche(self):
        f = self.fea
        left = self.base("qcap.l", "cap", "left")
        right = self.base("qcap.r", "cap", "right")
        # In the run as it is seen, the end enclosure comes first: the tied end, at the left.
        f.lookup("caps", [f"sub {ctl('ee')} by {left};", f"sub {ctl('be')} by {right};"])
        inside = self.forms + [comp(g, j) for g in self.forms for j in range(STEPS)]
        inside += sorted({g for g, (kind, _) in self.new.items() if kind == "carrier"})
        inside += ["space", "qblk"]
        rules = []
        for g in inside:
            adv = self.advance(g)
            n = math.ceil(adv / CORD_STEP) * CORD_STEP
            piece = self.mark(f"qcord.{n}") if n > 0 else self.mark("qcord.0")
            if n > 0:
                self.new[piece] = ("cord", n)
            rules.append(f"sub {g} by {g} {piece};")
        f.lookup("cord_piece", rules, feature=False)
        cords = sorted(g for g in self.new if g.startswith("qcord."))
        cordc = self.c("CORDS", cords)
        ins = self.c("INSIDE", inside)
        f.lookup(
            "cord",
            [f"sub [{left} {cordc}] {ins}' lookup cord_piece;"],
            f"UseMarkFilteringSet {self.c('VCORD', cords)}",
        )

    def advance(self, g):
        if g in self.hmtx:
            return self.hmtx[g][0]
        kind, data = self.new[g]
        if kind == "carrier":
            return data
        return 0

    # -- 4. positions ---------------------------------------------------------------------

    def positions(self):
        """One pair positioning lookup per kind of offset: a sign's copy and the token of
        that kind after it, which moves the copy. A class pair keeps the lookup small: a
        single positioning lookup over every copy would cost HarfBuzz's table check one
        operation for every two glyphs it covers, and the table is rejected whole when the
        operations run out."""
        f = self.fea
        comps = self.c("COMP", [comp(g, j) for g in self.forms for j in range(STEPS)])
        for (kind, level), values in sorted(self.fin_values.items(), key=lambda kv: (kv[0][0], -1 if kv[0][1] is None else kv[0][1])):
            axis = "y" if kind.startswith(("y", "dy")) else "x"
            fam = [tok("f" + kind, level, sv(v)) for v in sorted(values)]
            rules = []
            for v in sorted(values):
                if v == 0:
                    continue
                rec = f"<{v * UNIT} 0 0 0>" if axis == "x" else f"<0 {v * UNIT} 0 0>"
                one = self.c(f"F_{kind}{'' if level is None else level}_{sv(v)}", [tok("f" + kind, level, sv(v))])
                rules.append(f"pos {comps} {one} {rec};")
            tag = f"{kind}{'' if level is None else level}"
            if rules:
                f.lookup(f"pos_{tag}", rules, f"UseMarkFilteringSet {self.c(f'VP_{tag}', fam)}")


# -- glyph construction -------------------------------------------------------------------


def empty_glyph():
    g = Glyph()
    g.numberOfContours = 0
    return g


def composite_glyph(font, glyph, scale, cx, cy):
    g = Glyph()
    g.numberOfContours = -1
    c = GlyphComponent()
    c.glyphName = glyph
    c.x = round(-scale * cx)
    c.y = round(CENTRE_Y - scale * cy)
    c.flags = 0x1000  # unscaled component offset
    if scale != 1:
        c.transform = [[scale, 0], [0, scale]]
    g.components = [c]
    return g


def polygon_glyph(contours):
    """A glyph of straight-sided contours, outer ones clockwise."""
    pen = TTGlyphPen(None)
    for pts in contours:
        pen.moveTo(pts[0])
        for p in pts[1:]:
            pen.lineTo(p)
        pen.closePath()
    return pen.glyph()


def _path_contours(path):
    out = []
    cur = None
    for verb, pts in path.segments:
        if verb == "moveTo":
            cur = [pts[0]]
        elif verb == "lineTo":
            cur.append(pts[0])
        elif verb in ("qCurveTo", "curveTo"):
            cur.extend(pts[1:] if len(pts) > 1 else pts)
        elif verb == "closePath":
            out.append(cur)
            cur = None
    return out


def _stroke(points, closed, width):
    p = pathops.Path()
    p.moveTo(*points[0])
    for x, y in points[1:]:
        p.lineTo(x, y)
    if closed:
        p.close()
    p.stroke(width, pathops.LineCap.BUTT_CAP, pathops.LineJoin.ROUND_JOIN, 4.0)
    p.convertConicsToQuads()
    return p


def _disc(cx, cy, r, n=24):
    p = pathops.Path()
    pts = [(cx + r * math.cos(2 * math.pi * i / n), cy + r * math.sin(2 * math.pi * i / n)) for i in range(n)]
    p.moveTo(*pts[0])
    for x, y in pts[1:]:
        p.lineTo(x, y)
    p.close()
    return p


def _union(paths):
    out = pathops.Path()
    pathops.union(paths, out.getPen())
    out.convertConicsToQuads()
    return out


def _rounded(path):
    """A path's contours with integer points, outer contours clockwise (y up)."""
    contours = []
    for c in _path_contours(path):
        pts = []
        for x, y in c:
            q = (round(x), round(y))
            if not pts or pts[-1] != q:
                pts.append(q)
        if len(pts) > 2 and pts[0] == pts[-1]:
            pts.pop()
        if len(pts) > 2:
            contours.append(pts)
    return contours


def _area(pts):
    return sum(x1 * y2 - x2 * y1 for (x1, y1), (x2, y2) in zip(pts, pts[1:] + pts[:1])) / 2


def _orient(contours):
    """Outer contours clockwise and holes counter-clockwise, by nesting depth."""
    out = []
    for i, c in enumerate(contours):
        inside = 0
        px, py = c[0]
        for j, o in enumerate(contours):
            if i != j and _point_in(px, py, o):
                inside += 1
        clockwise = inside % 2 == 0
        if (_area(c) < 0) != clockwise:
            c = c[::-1]
        out.append(c)
    return out


def _point_in(x, y, poly):
    inside = False
    n = len(poly)
    for k in range(n):
        x1, y1 = poly[k]
        x2, y2 = poly[(k + 1) % n]
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
            inside = not inside
    return inside


# The cord is a band two hairlines wide apart, twisted: short slanted strokes cross it
# at a fixed pitch. It runs as a top and a bottom band, clear of the signs by three
# hairlines, and the two ends of the cartouche join the bands round.
TWIST = 42  # the pitch of the twist


def cord_band_top():
    return QUADRAT + CORD_GAP + CORD / 2


def cord_band_bottom(font_min_y):
    return min(0, font_min_y) - CORD_GAP - CORD / 2


def _band_strokes(points, closed=False):
    """The two hairline edges of the cord along a centreline, and its twist."""
    parts = []
    n = len(points)
    normals = []
    for i in range(n):
        a = points[max(0, i - 1)]
        b = points[min(n - 1, i + 1)]
        tx, ty = b[0] - a[0], b[1] - a[1]
        L = math.hypot(tx, ty) or 1
        normals.append((-ty / L, tx / L))
    for side in (-1, 1):
        edge = [(x + side * nx * CORD / 2, y + side * ny * CORD / 2) for (x, y), (nx, ny) in zip(points, normals)]
        parts.append(_stroke(edge, closed, HAIR))
    # twist strokes at a fixed pitch along the line
    acc, nxt = 0.0, TWIST / 2
    for i in range(1, n):
        (x0, y0), (x1, y1) = points[i - 1], points[i]
        seg = math.hypot(x1 - x0, y1 - y0)
        while acc + seg >= nxt:
            t = (nxt - acc) / seg
            px, py = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
            nx, ny = normals[i]
            tx, ty = ny, -nx
            h = CORD / 2
            parts.append(
                _stroke([(px - nx * h - tx * h * 0.7, py - ny * h - ty * h * 0.7), (px + nx * h + tx * h * 0.7, py + ny * h + ty * h * 0.7)], False, HAIR * 0.8)
            )
            nxt += TWIST
        acc += seg
    return parts


def cord_piece(n, top, bottom):
    """Both bands of the cord over the `n` units before the pen."""
    parts = []
    for yc in (top, bottom):
        parts += _band_strokes([(-n, yc), (0, yc)])
    return _clip(_union(parts), -n, 0)


def _clip(path, x0, x1):
    out = pathops.op(path, _rect(x0, -10000, x1, 10000), pathops.PathOp.INTERSECTION)
    out.convertConicsToQuads()
    return out


def _rect(x0, y0, x1, y1):
    p = pathops.Path()
    p.moveTo(x0, y0)
    p.lineTo(x1, y0)
    p.lineTo(x1, y1)
    p.lineTo(x0, y1)
    p.close()
    return p


KNOT = 40  # the radius of the seal-knot
TAIL = 130  # the length of each loose end of the tie


def cap_paths(side, top, bottom):
    """One end of the cartouche: a half ellipse of cord joining the two bands. The end
    enclosure, first in the line as it is seen, is the tied end at the left: the knot where
    the cord's ends cross and its two ends splayed outward."""
    r = (top - bottom) / 2
    a = 0.55 * r  # the end's horizontal half axis
    cy = (top + bottom) / 2
    tie = KNOT + TAIL * 0.85 if side == "left" else 0
    sgn = -1 if side == "left" else 1
    x0 = tie + a + CORD if side == "left" else 0  # where the end meets the straight bands
    pts = []
    for i in range(65):
        t = math.pi / 2 - math.pi * i / 64
        pts.append((x0 + sgn * a * math.cos(t), cy + r * math.sin(t)))
    parts = _band_strokes(pts)
    if side == "left":
        # the bands run on to the cap's advance
        for yc in (top, bottom):
            parts += _band_strokes([(x0 - 1, yc), (x0 + CORD, yc)])
        kx = x0 - a
        parts.append(_disc(kx, cy, KNOT))
        for s in (1, -1):
            end = [(kx, cy), (kx - TAIL * 0.45, cy + s * TAIL * 0.22), (kx - TAIL * 0.85, cy + s * TAIL * 0.5)]
            parts += _band_strokes(end)
            ex, ey = end[-1]
            parts.append(_disc(ex, ey, CORD * 0.75))
        adv = x0 + CORD
    else:
        adv = a + CORD / 2 + HAIR + SIDE
    return _union(parts), adv


def add_controls(font: TTFont) -> None:
    """Map each control, at its Unicode code point and at its twin, to an empty glyph."""
    order = list(font.getGlyphOrder())
    glyf, hmtx = font["glyf"], font["hmtx"]
    for c in load_controls():
        if c["glyph"] not in order:
            order.append(c["glyph"])
            glyf.glyphs[c["glyph"]] = empty_glyph()
            hmtx.metrics[c["glyph"]] = (0, 0)
    font.setGlyphOrder(order)
    glyf.glyphOrder = order
    for table in font["cmap"].tables:
        if table.isUnicode() and table.format == 12:
            for c in load_controls():
                table.cmap[int(c["codepoint"][2:], 16)] = c["glyph"]
                table.cmap[int(c["twin"][2:], 16)] = c["glyph"]


def apply(path: Path) -> None:
    font = TTFont(str(path))
    enc = load_encoding()
    add_controls(font)
    lay = Layout(font, enc)
    code = lay.build()
    glyf, hmtx = font["glyf"], font["hmtx"]
    order = list(font.getGlyphOrder())
    min_y = min(
        (glyf[g].yMin for g in lay.forms if glyf[g].numberOfContours), default=0
    )
    top, bottom = cord_band_top(), cord_band_bottom(min_y)
    for name in lay.marks + lay.bases:
        kind, data = lay.new[name]
        adv = 0
        if kind in ("empty", "empty-base"):
            g = empty_glyph()
        elif kind == "comp":
            g = composite_glyph(font, *data)
        elif kind == "carrier":
            g, adv = empty_glyph(), data
        elif kind == "cord":
            g = polygon_glyph(_orient(_rounded(cord_piece(data, top, bottom))))
        elif kind == "cap":
            p, adv = cap_paths(data, top, bottom)
            g = polygon_glyph(_orient(_rounded(p)))
            adv = round(adv)
        order.append(name)
        glyf.glyphs[name] = g
        hmtx.metrics[name] = (adv, 0)
    font.setGlyphOrder(order)
    glyf.glyphOrder = order
    for name in lay.marks + lay.bases:
        g = glyf[name]
        g.recalcBounds(glyf)
        hmtx.metrics[name] = (hmtx.metrics[name][0], g.xMin if g.numberOfContours else 0)
    font["maxp"].numGlyphs = len(order)
    # The font now maps characters beyond the Basic Multilingual Plane that Unicode assigns.
    font["OS/2"].setUnicodeRanges(font["OS/2"].getUnicodeRanges() | {57})
    if "post" in font and font["post"].formatType == 2.0:
        font["post"].extraNames = []
        font["post"].mapping = {}
    for tag in ("GSUB", "GPOS", "GDEF"):
        if tag in font:
            del font[tag]
    fea = FEATURES.read_text(encoding="utf-8") + "\n" + code
    addOpenTypeFeaturesFromString(font, fea, filename=str(FEATURES))
    extend(font)
    font.save(str(path))


def extend(font: TTFont) -> None:
    """Make every lookup an extension lookup, so the lookup list's 16-bit offsets reach
    every lookup however large the tables grow."""
    for tag, ext in (("GSUB", 7), ("GPOS", 9)):
        if tag not in font:
            continue
        cls = otTables.lookupTypes[tag][ext]
        for lookup in font[tag].table.LookupList.Lookup:
            if lookup.LookupType == ext:
                continue
            for i, sub in enumerate(lookup.SubTable):
                e = cls()
                e.Format = 1
                e.ExtSubTable = sub
                lookup.SubTable[i] = e
            lookup.LookupType = ext


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("font", type=Path)
    ap.add_argument("--fea", type=Path, help="also write the generated feature code here")
    args = ap.parse_args()
    if args.fea:
        font = TTFont(str(args.font))
        add_controls(font)
        lay = Layout(font, load_encoding())
        args.fea.write_text(lay.build(), encoding="utf-8")
        return
    apply(args.font)


if __name__ == "__main__":
    sys.exit(main())
