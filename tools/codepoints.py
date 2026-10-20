# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Confirm that every face draws exactly the characters its fonts.json table lists.

    .venv/bin/python tools/codepoints.py [font ...]

fonts.json states, for each family, a ``codepoints`` table: the code point, glyph
name and kind of every character the face draws. A font fails when

- fonts.json carries a table other than the one tools/codepoint_order.py defines;
- a listed code point, shaped alone, does not yield exactly its listed glyph;
- a left-to-right face has a code point outside its plane 15 block, a repeated code
  point or a repeated glyph, or its cmap holds an entry in the Private Use Area of the
  Basic Multilingual Plane (U+E000 to U+F8FF);
- a glyph of a left-to-right face is neither listed nor one of the glyphs that are
  not characters (the spelling helpers, the joined and doubled forms, the
  precomposed vowels, the box, the empty glyphs and the space), or a listed glyph is
  one of those;
- a character's code point lies outside every block that the registry
  (``BLOCKS`` in tools/codepoint_order.py) lists for its family, or two registered
  blocks overlap, or the README's "Code point blocks" table is not the registry's;
- the Pirzath Carved and Pirzath Hand tables differ;
- a character has no key, a key is not a key of tools/keyboard_keys.py, two characters
  of the family share a key, a plain key is the Option prefix of the Emacs input
  methods, or a Pirzath Hand face's keys differ from Pirzath Carved's.

Text is shaped with the font's default features, so an optional style such as
joining stays off. A few glyphs are reshaped by a typing rule when they stand alone,
so they are shaped in the context the face draws them in: a ``y`` before a vowel, and
Semaron's catch after a letter.
"""

import json
import re
import sys
from pathlib import Path

from fontTools.ttLib import TTFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
import codepoint_order  # noqa: E402
import keyboard_keys  # noqa: E402
from render import Renderer  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

# Glyphs a typing rule reshapes alone, with the glyph that stands before and after them.
# The rule exists only while the face still reads Latin spellings.
CONTEXT = {
    "y": ("", "a"),
    "Y": ("", "a"),
    "grave": ("a", ""),
}

# Glyphs that are not characters, by family stem, with the reason.
NOT_CHARACTERS = {
    "SemaronKuriale-Regular": {
        "c": "spells ch",
        "C": "spells ch",
    },
    "PirzathCarved-Regular": {
        "c": "spells ch",
        "less": "spells the opening quotation mark",
        "greater": "spells the closing quotation mark",
        "quotedbl": "becomes the opening or closing quotation mark",
        "doubling": "the mark a doubled consonant is drawn with",
        **{f"{v}acute": "a vowel and its length mark" for v in "aeiou"},
    },
    "PirzathHand-Regular": {
        "c": "spells ch",
        "less": "spells the opening quotation mark",
        "greater": "spells the closing quotation mark",
        "quotedbl": "becomes the opening or closing quotation mark",
        **{f"{v}acute": "a vowel and its length mark" for v in "aeiou"},
    },
    "ThuravarkCarved-Regular": {
        "y": "becomes i or j",
        "hyphen": "draws nothing",
        **{f"{v}acute": "a vowel and its acute mark" for v in "aeiou"},
    },
}

# The Private Use Area of the Basic Multilingual Plane, which no face's cmap uses.
BMP_PRIVATE = (0xE000, 0xF8FF)

# Glyphs of every left-to-right face that are not characters.
STRUCTURAL = {".notdef", "notdef.box", "ignorable", "ignorable.sub", "space"}
JOINED_SUFFIXES = (".init", ".medi", ".fina")


def is_structural(name: str, listed: set[str]) -> bool:
    if name in STRUCTURAL or name.endswith(JOINED_SUFFIXES):
        return True
    # A doubled consonant (p_p, t_h_t_h) is the letter written twice.
    parts = name.split("_")
    if len(parts) > 1:
        for size in range(1, len(parts) // 2 + 1):
            unit = "_".join(parts[:size])
            if len(parts) == 2 * size and unit == "_".join(parts[size:]):
                return True
    return False


def key_problems(label: str, rows: list[dict]) -> list[str]:
    """What is wrong with the keys of a family's table."""
    problems = []
    owner: dict[str, str] = {}
    for row in rows:
        glyph, key = row["glyph"], row.get("key")
        if not isinstance(key, str) or not key:
            problems.append(f"fonts.json: error: {label}: {glyph} has no key")
            continue
        if keyboard_keys.parse(key) is None and not keyboard_keys.is_zethu(key):
            problems.append(f"fonts.json: error: {label}: {glyph} has the key {key!r}, which is not a key")
        elif key in owner:
            problems.append(f"fonts.json: error: {label}: {glyph} and {owner[key]} share the key {key}")
        elif key == keyboard_keys.OPTION_PREFIX:
            problems.append(f"fonts.json: error: {label}: {glyph} has the Option prefix as its key")
        owner.setdefault(key, glyph)
    return problems


def cells(table: str) -> str:
    """A Markdown table's cells, whatever padding the formatter gave its columns."""
    rows = [[c.strip() for c in line.strip().strip("|").split("|")] for line in table.splitlines() if line.startswith("|")]
    return "\n".join("|".join("-" if set(c) <= {"-", ":"} else c for c in row) for row in rows)


def registry_problems() -> list[str]:
    """What is wrong with the block registry itself and its README table."""
    problems = []
    blocks = sorted(codepoint_order.BLOCKS, key=lambda b: b["start"])
    for b in blocks:
        if b["start"] > b["end"]:
            problems.append(f"tools/codepoint_order.py: error: the block {b['use']} ends before it starts")
    for a, b in zip(blocks, blocks[1:]):
        if b["start"] <= a["end"]:
            problems.append(
                f"tools/codepoint_order.py: error: the blocks U+{a['start']:04X}-U+{a['end']:04X} ({a['use']}) "
                f"and U+{b['start']:04X}-U+{b['end']:04X} ({b['use']}) overlap"
            )
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    heading = re.search(r"^## Code point blocks\n(.*?)(?=^## |\Z)", readme, re.M | re.S)
    if heading is None:
        problems.append("README.md: error: there is no Code point blocks section")
    elif cells(codepoint_order.readme_table()) not in cells(heading.group(1)):
        problems.append("README.md: error: the Code point blocks table differs from BLOCKS in tools/codepoint_order.py")
    return problems


def block_problems(label: str, rows: list[dict]) -> list[str]:
    """Every code point of a family lies in a registered block that lists the family."""
    own = [b for b in codepoint_order.BLOCKS if label in b["families"]]
    if not own:
        return [f"tools/codepoint_order.py: error: {label} has no registered block"]
    return [
        f"fonts.json: error: {label}: {r['codepoint']} is outside the blocks registered for it"
        for r in rows
        if not any(b["start"] <= cp(r["codepoint"]) <= b["end"] for b in own)
    ]


def manifest() -> dict:
    return json.loads((ROOT / "fonts.json").read_text(encoding="utf-8"))


def families(font: Path) -> list[dict]:
    return [f for f in manifest()["families"] if Path(f["files"]["ttf"]).name == font.name]


def cp(text: str) -> int:
    return int(text[2:], 16)


def shape(renderer: Renderer, text: str, family: dict) -> list[str]:
    direction = "rtl" if family["direction"] == "rtl" else "ltr"
    shaped = renderer.shape(text, direction=direction)
    names = [renderer.order[g[0]] for g in shaped.glyphs]
    return list(reversed(names)) if direction == "rtl" else names


def check(font: Path) -> list[str]:
    stem = font.stem
    problems = []
    found = families(font)
    if not found:
        return [f"{font}: error: no family in fonts.json names this file"]
    renderer = Renderer(font)
    cmap = TTFont(str(font)).getBestCmap()
    for family in found:
        label = family["name"]
        rows = family.get("codepoints")
        if rows is None:
            problems.append(f"fonts.json: error: {label}: no codepoints table")
            continue
        problems += key_problems(label, rows)
        problems += block_problems(label, rows)
        expected = codepoint_order.table(stem)
        if rows != expected:
            problems.append(f"fonts.json: error: {label}: the codepoints table differs from tools/codepoint_order.py")
        glyph_of = {}
        for row in rows:
            code, glyph = cp(row["codepoint"]), row["glyph"]
            if code in glyph_of:
                problems.append(f"fonts.json: error: {label}: {row['codepoint']} is listed twice")
            glyph_of[code] = glyph
            if cmap.get(code) != glyph:
                problems.append(f"{font}: error: {label}: {row['codepoint']} maps to {cmap.get(code)}, not {glyph}")
                continue
            before, after = CONTEXT.get(glyph, ("", ""))
            if (before or after) and stem in codepoint_order.LTR:
                by_glyph = {r["glyph"]: cp(r["codepoint"]) for r in rows}
                text = (chr(by_glyph[before]) if before else "") + chr(code) + (chr(by_glyph[after]) if after else "")
                want = [g for g in (before, glyph, after) if g]
            else:
                text, want = chr(code), [glyph]
            got = shape(renderer, text, family)
            if got != want:
                problems.append(f"{font}: error: {label}: {row['codepoint']} shapes to {got}, not {want}")
        if stem in codepoint_order.LTR:
            start, end = codepoint_order.block(stem)
            for row in rows:
                if not start <= cp(row["codepoint"]) <= end:
                    problems.append(f"fonts.json: error: {label}: {row['codepoint']} is outside U+{start:04X}-U+{end:04X}")
            for code in sorted(c for c in cmap if BMP_PRIVATE[0] <= c <= BMP_PRIVATE[1]):
                problems.append(f"{font}: error: {label}: the cmap has an entry at U+{code:04X}, in the Basic Multilingual Plane's Private Use Area")
            glyphs = [r["glyph"] for r in rows]
            if len(set(glyphs)) != len(glyphs):
                problems.append(f"fonts.json: error: {label}: a glyph is listed twice")
            excluded = NOT_CHARACTERS[stem]
            for glyph in glyphs:
                if glyph in excluded or is_structural(glyph, set(glyphs)):
                    problems.append(f"fonts.json: error: {label}: {glyph} is not a character")
            for glyph in renderer.order:
                if glyph in glyphs or glyph in excluded or is_structural(glyph, set(glyphs)):
                    continue
                problems.append(f"{font}: error: {label}: the character {glyph} has no code point")
    if stem == "PirzathHand-Regular":
        carved = next((f for f in manifest()["families"] if f["name"] == "Pirzath Carved"), None)
        for family in found:
            if carved is None:
                problems.append(f"fonts.json: error: {family['name']}: there is no Pirzath Carved table to agree with")
            elif [r.get("key") for r in family.get("codepoints", [])] != [r.get("key") for r in carved["codepoints"]]:
                problems.append(f"fonts.json: error: {family['name']}: the keys differ from Pirzath Carved's")
            elif carved.get("codepoints") != family.get("codepoints"):
                problems.append(f"fonts.json: error: {family['name']}: the table differs from Pirzath Carved's")
    return problems


def main() -> None:
    paths = [Path(a) for a in sys.argv[1:]] or sorted((ROOT / "fonts").glob("*-Regular.ttf"))
    status = 0
    registry = registry_problems()
    print("block registry: " + (f"{len(registry)} problems" if registry else "ok"))
    for line in registry:
        print(line)
    status |= bool(registry)
    for path in paths:
        problems = check(path)
        print(f"{path}: {len(problems)} problems" if problems else f"{path}: ok")
        for line in problems:
            print(line)
        status |= bool(problems)
    sys.exit(status)


if __name__ == "__main__":
    main()
