# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""The block layouts of Chalish Pilam Ceremonial, and the OpenType rules that choose them.

A block holds a main sign and at most two affixes, so the layouts a block can take are
a small closed set. The font carries every item already placed and squeezed for each
layout it can take, drawn by ``blocks.compose()`` itself; shaping only chooses the
variant. No positioning or scaling happens at shaping time.

In the codage ``*`` sets side by side and ``:`` stacks, first over second. Each concept
glyph, syllable sign and number is one character, and the two joiners are characters
that draw nothing. A block ends wherever no joiner follows.

A layout is written with ``L`` a lead (a number or a syllable sign set before the
main), ``O`` a syllable over, ``U`` a syllable under, ``M`` the main concept glyph and
``S`` an item of a block that has no main:

    L*M  L*L*M  O:M  M:U  O:M:U  L*O:M  L*M:U  S  S*S  S*S*S

Every variant of a block is drawn from the block's left edge. Every item but the last
in text order has no advance, and the last carries the block's whole advance, so the
items overlay into one block. The main's footprint (half, full or double) sets the
block's width; a block with no main is a full block.

A block that is not one of these layouts is rejected: its items stay in their plain
forms, written as they stand.
"""

import sys
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import blocks as Q  # noqa: E402
import ceremonial as R  # noqa: E402

SCALE = R.FONT_SCALE
DROP = R.FONT_DROP
GUTTER = 60.0  # the white each side of a block, in font units
INK_SEED = 0  # one wobble field for every variant, so the items of a block agree

JOINERS = {"*": "join_beside", ":": "join_stack"}

NUMBER_VALUES = [*range(20), 20, 400, 8000, 160000]
DRAWN_NUMBERS = list(range(1, 20))  # coefficients; zero and the places have no ceremonial glyph

NUMBERS = [f"n{v}" for v in DRAWN_NUMBERS]
SYLLABLES = list(Q.SIGNS)
ITEMS = NUMBERS + SYLLABLES
MAINS = list(Q.MAINS)
FOOTPRINTS = ["full"] + sorted({g.footprint for g in Q.MAINS.values()} - {"full"})


def base_name(code: str) -> str:
    """The glyph name of a code in its plain form."""
    return code.lower() if code in Q.MAINS else code


def block_advance(footprint: str) -> float:
    """The advance of a block whose main has this footprint, gutters included."""
    return R.WIDTH[footprint] * SCALE + 2 * GUTTER


def footprint_of(code: str) -> str:
    return Q.MAINS[code].footprint if code in Q.MAINS else "full"


def capture(block: str) -> list:
    """The parts ``blocks.compose`` places for each item of a block, in the order it
    places them: leads, items over, items under, then the main."""
    calls = []
    original = Q._item

    def record(*args):
        out = original(*args)
        calls.append(out)
        return out

    Q._item = record
    try:
        Q.compose(block)
    finally:
        Q._item = original
    return calls


@dataclass(frozen=True)
class Role:
    """One drawing of an item: the block it is composed in to find its slot, which of
    that block's items it is, and what advance it carries."""

    suffix: str
    kind: str  # item, syl or main
    template: str
    index: int
    advance: str  # zero, full, own or a footprint


# A main of each footprint, to compose the blocks that find where its affixes sit.
SAMPLE = {fp: "SUN" if fp == "full" else next(c for c in MAINS if footprint_of(c) == fp) for fp in FOOTPRINTS}
# The roles of the items that share a block with a main. Where they sit depends on the
# width of that block, so each has a drawing for every footprint.
AFFIXES = ("lead0", "lead1", "over0", "over1", "under0", "under1")


def _roles() -> list[Role]:
    out = [
        Role("s2a", "item", "{x}*n1", 0, "zero"),
        Role("s2b", "item", "n1*{x}", 1, "full"),
        Role("s3a", "item", "{x}*n1*n1", 0, "zero"),
        Role("s3b", "item", "n1*{x}*n1", 1, "zero"),
        Role("s3c", "item", "n1*n1*{x}", 2, "full"),
        Role("mL", "main", "n1*{x}", -1, "own"),
        Role("mLL", "main", "n1*n1*{x}", -1, "own"),
        Role("mO", "main", "ka1:{x}", -1, "own"),
        Role("mLO", "main", "n1*ka1:{x}", -1, "own"),
        Role("mU", "main", "{x}:ka1", -1, "zero"),
        Role("mOU", "main", "ka1:{x}:ka1", -1, "zero"),
        Role("mLU", "main", "n1*{x}:ka1", -1, "zero"),
    ]
    for fp in FOOTPRINTS:
        m = SAMPLE[fp]
        out += [
            Role(sized("lead0", fp), "item", "{x}*" + m, 0, "zero"),
            Role(sized("lead1", fp), "item", "n1*{x}*" + m, 1, "zero"),
            Role(sized("over0", fp), "syl", "{x}:" + m, 0, "zero"),
            Role(sized("over1", fp), "syl", "n1*{x}:" + m, 1, "zero"),
            Role(sized("under0", fp), "syl", m + ":{x}", 0, fp),
            Role(sized("under1", fp), "syl", "n1*" + m + ":{x}", 1, fp),
        ]
    return out


def sized(suffix: str, footprint: str) -> str:
    """The suffix of an affix's role in a block whose main has ``footprint``."""
    return suffix + ("" if footprint == "full" else f"_{footprint}")


ROLES = _roles()
BY_SUFFIX = {r.suffix: r for r in ROLES}

# The layouts, longest first, each with the role of every item in text order.
CONFIGS = [
    ("L*L*M", ["lead0", "lead1", "mLL"]),
    ("O:M:U", ["over0", "mOU", "under0"]),
    ("L*O:M", ["lead0", "over1", "mLO"]),
    ("L*M:U", ["lead0", "mLU", "under1"]),
    ("S*S*S", ["s3a", "s3b", "s3c"]),
    ("L*M", ["lead0", "mL"]),
    ("O:M", ["over0", "mO"]),
    ("M:U", ["mU", "under0"]),
    ("S*S", ["s2a", "s2b"]),
]

KINDS = {"item": ITEMS, "syl": SYLLABLES, "main": MAINS}


def role_codes(role: Role) -> list[str]:
    return KINDS[role.kind]


def variant_name(code: str, suffix: str) -> str:
    return f"{base_name(code)}.{suffix}"


def role_advance(role: Role, code: str) -> float:
    if role.advance == "zero":
        return 0.0
    if role.advance == "full":
        return block_advance("full")
    if role.advance == "own":
        return block_advance(footprint_of(code))
    return block_advance(role.advance)


def parts_of(role: Role, code: str) -> list:
    """The parts ``blocks.compose`` draws for ``code`` in this role."""
    return capture(role.template.format(x=code))[role.index]


def plain_parts(code: str) -> list:
    """The parts of a code set alone in a block: a main in its full form, an item in the
    one slot of a block that has no main."""
    return capture(code)[-1]


# -- the OpenType rules --------------------------------------------------------------------------


def _glyph_class(name: str, codes: list[str]) -> str:
    return f"@{name} = [{' '.join(base_name(c) for c in codes)}];"


def _pattern(config: str, roles: list[str], footprint: str | None):
    """(class, lookup suffix or None) for every glyph of a layout, joiners included."""
    out, letter = [], 0
    for ch in config:
        if ch in JOINERS:
            out.append(("JB" if ch == "*" else "JS", None))
            continue
        suffix = roles[letter]
        letter += 1
        if ch in "LS":
            cls = "ITEM"
        elif ch in "OU":
            cls = "SYL"
        else:
            cls = "MAIN" if footprint is None else f"MAIN_{footprint}"
        if footprint is not None and suffix in AFFIXES:
            suffix = sized(suffix, footprint)
        out.append((cls, suffix))
    return out


def features() -> str:
    """The feature file: the glyph classes, one single substitution per role and one
    contextual lookup in ``rclt`` holding a rule per layout."""
    lines = [
        "# HarfBuzz replaces a default-ignorable character the font maps directly with",
        "# the space glyph, so it draws nothing only when it is substituted. Each",
        "# ignorable is substituted once, to a second empty glyph.",
        "feature ccmp {",
        "  sub ignorable by ignorable.sub;",
        "} ccmp;",
        "",
        "# The classes: numbers and syllable signs, syllable signs, main signs by the",
        "# footprint they set, and the joiners.",
        _glyph_class("ITEM", ITEMS),
        _glyph_class("SYL", SYLLABLES),
        _glyph_class("MAIN", MAINS),
    ]
    for fp in FOOTPRINTS:
        lines.append(_glyph_class(f"MAIN_{fp}", [c for c in MAINS if footprint_of(c) == fp]))
    lines += [
        f"@JB = [{JOINERS['*']}];",
        f"@JS = [{JOINERS[':']}];",
        "@JOIN = [@JB @JS];",
        "@ALL = [@ITEM @MAIN];",
        "",
        "# One substitution per role: each item to its drawing in that role.",
    ]
    used = {s for _, rs in CONFIGS for s in rs}
    used |= {sized(s, fp) for s in used if s in AFFIXES for fp in FOOTPRINTS}
    for role in ROLES:
        if role.suffix not in used:
            continue
        codes = role_codes(role)
        src = " ".join(base_name(c) for c in codes)
        dst = " ".join(variant_name(c, role.suffix) for c in codes)
        lines += [f"lookup r_{role.suffix} {{", f"  sub [{src}] by [{dst}];", f"}} r_{role.suffix};", ""]
    lines += [
        "# A block is matched whole, from its first item. A rule that ignores the block",
        "# followed by another joiner leaves a block of more than two affixes in plain",
        "# forms, and the first rule leaves what follows a joiner in plain forms, so no",
        "# part of a rejected block is laid out as though it were a block of its own.",
        "feature rclt {",
        "  lookup block {",
        "    ignore sub @JOIN @ALL';",
    ]
    for config, roles in CONFIGS:
        footprints = [None]
        if "M" in config:
            footprints = FOOTPRINTS
        marks = " ".join(f"@{c}'" for c, _ in _pattern(config, roles, None))
        lines.append(f"    ignore sub {marks} @JOIN;")
        for fp in footprints:
            parts = []
            for cls, suffix in _pattern(config, roles, fp):
                parts.append(f"@{cls}'" + (f" lookup r_{suffix}" if suffix else ""))
            lines.append(f"    sub {' '.join(parts)};")
    lines += ["  } block;", "} rclt;", ""]
    return "\n".join(lines)
