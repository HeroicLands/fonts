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
  blocks overlap, or DEVELOPING.md's "Code point blocks" table is not the registry's;
- the cmap maps a code point to anything but its listed glyph, the space, the empty
  glyph of the default-ignorables or the box: U+0020 and U+00A0 are the only spaces,
  and every other character a face does not list, Latin included, draws the box;
- a GSUB substitution writes a listed glyph it does not read, so that one character
  becomes another (a spelling rule): what a face substitutes is a contextual form only, such as a
  joined, doubled or fused form, a mark's form, the box for a catch with no letter
  before it or for a Vedyakshara mark with no sign before it, or the empty glyph of an
  ignorable;
- a sequence of characters that a spelling rule once rewrote does not shape as
  written (``SEQUENCES``);
- the Pirzath Carved and Pirzath Hand tables differ;
- a Khelathi Zethu Glyphs sign has no key, its key is not a sign id, or two signs
  share a key, or one of its format controls carries a key; or a character of a script
  typed by sound (tools/sound_keys.json) carries a key of its own.

Text is shaped with the font's default features, so an optional style such as
joining stays off. Semaron's catch with no letter before it draws the box, so it is
shaped after a letter. A format control of Khelathi Zethu Glyphs is laid out
by the quadrat or cartouche it stands in, so only its cmap entry is checked.
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

# Glyphs a contextual rule reshapes alone, with the glyph that stands before and after them.
CONTEXT = {
    "grave": ("a", ""),
}

# Sequences of listed glyphs, by family stem, that must shape exactly as written: each
# was once rewritten by a spelling rule.
SEQUENCES = {
    "PirzathCarved-Regular": [["y", "ai"], ["y", "a", "i"], ["t", "h"], ["a", "i"], ["n", "g", "h"]],
    "PirzathHand-Regular": [["y", "ai"], ["y", "a", "i"], ["t", "h"], ["a", "i"], ["n", "g", "h"]],
    "SemaronKuriale-Regular": [["i", "i"], ["a", "a"], ["t", "h"], ["y", "t"], ["Y"]],
    "ThuravarkCarved-Regular": [["t", "h"], ["n", "g"], ["i"], ["j", "t"], ["a", "i"], ["a", "u"], ["o", "i"]],
    "HelonikaBook-Regular": [["e", "i"], ["o", "u"], ["t", "h"], ["k", "h"], ["z", "h"], ["a", "a"], ["E", "i"]],
}

# The only code points that draw the space.
SPACES = (0x20, 0xA0)
# The default-ignorable characters, which draw an empty glyph.
IGNORABLES = {*range(0x200B, 0x2010), *range(0x202A, 0x202F), *range(0x2066, 0x206A), 0xFEFF}
BOX = "notdef.box"

# Glyphs that are not characters, by family stem, with the reason.
NOT_CHARACTERS = {
    "SemaronKuriale-Regular": {},
    "PirzathCarved-Regular": {
        "doubling": "the mark a doubled consonant is drawn with",
    },
    "PirzathHand-Regular": {
        **{f"{v}acute": "a vowel and its length mark, drawn as one" for v in "aeiou"},
    },
    "TengChou-Regular": {},
    "ChalishPilamCommon-Regular": {},
    "HelonikaBook-Regular": {},
    "ThuravarkCarved-Regular": {
        **{f"{v}.acute": "the acute mark after a vowel, drawn as its stave again" for v in "aeiou"},
        **{name: "a bound rune, two staves on one stem, set by ss01" for name in "e_n e_l a_r a_l m_a z_a k_a u_r l_m l_th".split()},
    },
}



def _vedyakshara_forms() -> dict[str, str]:
    """Vedyakshara Classical's glyphs that are not characters: the forms its rules draw."""
    enc = json.loads((ROOT / "tools" / "vedyakshara" / "encoding.json").read_text(encoding="utf-8"))
    cons = [g["glyph"] for g in enc["glyphs"] if g["kind"] == "consonant"]
    fused = [f["glyph"] for f in enc["fused"]]
    out = {"fa": "pa and the soft dot, drawn as one"}
    out.update({f: "a fused pair of consonants" for f in fused})
    for b in cons + ["fa"] + fused:
        out[f"{b}.half"] = "a consonant before another, drawn as its half form"
        out[f"{b}.final"] = "a consonant ending a word, drawn as its final form"
        out[f"{b}.rfoot"] = "a consonant before r, drawn with the r-foot"
    for part in ("flag.i", "flag.e"):
        out[part] = "a part of a vowel sign, placed on its sign"
    return out


NOT_CHARACTERS["VedyaksharaClassical-Regular"] = _vedyakshara_forms()


def not_character(stem: str, glyph: str, excluded: dict[str, str]) -> bool:
    """Whether a glyph of a face is one of its forms rather than a character."""
    if stem == "VedyaksharaClassical-Regular" and glyph.startswith("hook."):
        return True  # a hook with the neck its sign asks for
    return glyph in excluded


def not_characters(stem: str, order: list[str]) -> dict[str, str]:
    """The glyphs of a face that are not characters: NOT_CHARACTERS, and for Thuravark
    Carved the crowned frame's glyphs, which tools/thuravark-carved/crown.py adds."""
    excluded = dict(NOT_CHARACTERS[stem])
    if stem == "ThuravarkCarved-Regular":
        import importlib.util

        spec = importlib.util.spec_from_file_location("thuravark_crown", ROOT / "tools" / "thuravark-carved" / "crown.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        excluded.update(module.not_characters(order))
    return excluded

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
    """What is wrong with the keys of a family's table. Khelathi Zethu Glyphs is typed by
    sign id, so every sign carries its id as its key; every other script is typed by
    sound, so none of its characters carries a key."""
    problems = []
    owner: dict[str, str] = {}
    zethu = label == "Khelathi Zethu Glyphs"
    for row in rows:
        glyph, key = row["glyph"], row.get("key")
        if zethu and row["kind"] == "control":
            if key is not None:
                problems.append(f"fonts.json: error: {label}: the control {glyph} has the key {key!r}")
            continue
        if not zethu:
            if key is not None:
                problems.append(f"fonts.json: error: {label}: {glyph} has the key {key!r}; the script is typed by sound")
            continue
        if not isinstance(key, str) or not key:
            problems.append(f"fonts.json: error: {label}: {glyph} has no key")
        elif not keyboard_keys.is_zethu(key):
            problems.append(f"fonts.json: error: {label}: {glyph} has the key {key!r}, which is not a sign id")
        elif key in owner:
            problems.append(f"fonts.json: error: {label}: {glyph} and {owner[key]} share the key {key}")
        else:
            owner[key] = glyph
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
    readme = (ROOT / "DEVELOPING.md").read_text(encoding="utf-8")
    heading = re.search(r"^## Code point blocks\n(.*?)(?=^## |\Z)", readme, re.M | re.S)
    if heading is None:
        problems.append("DEVELOPING.md: error: there is no Code point blocks section")
    elif cells(codepoint_order.readme_table()) not in cells(heading.group(1)):
        problems.append("DEVELOPING.md: error: the Code point blocks table differs from BLOCKS in tools/codepoint_order.py")
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


def cmap_problems(font: Path, cmap: dict[int, str], listed: dict[int, str]) -> list[str]:
    """Every cmap entry is a listed character, a space, an ignorable or the box."""
    space = cmap.get(0x20)
    ignorable = {cmap[c] for c in IGNORABLES if c in cmap}
    problems = []
    for code, glyph in sorted(cmap.items()):
        if code in listed:
            continue
        if code in SPACES:
            ok = glyph == space
        elif code in IGNORABLES:
            ok = glyph in ignorable and glyph != BOX
        else:
            ok = glyph == BOX
        if not ok:
            problems.append(f"{font}: error: U+{code:04X} maps to {glyph}; only the face's own characters draw")
    if space != "space":
        problems.append(f"{font}: error: U+0020 maps to {space}, not space")
    return problems


def substitution_rules(gsub):
    """Each GSUB substitution as (lookup index, glyphs read, glyphs written)."""
    if gsub is None:
        return
    for index, lookup in enumerate(gsub.table.LookupList.Lookup):
        for sub in lookup.SubTable:
            kind = lookup.LookupType
            if kind == 7:
                kind, sub = sub.ExtSubTable.LookupType, sub.ExtSubTable
            if kind == 1:
                for g, h in sub.mapping.items():
                    yield index, [g], [h]
            elif kind == 2:
                for g, seq in sub.mapping.items():
                    yield index, [g], list(seq)
            elif kind == 3:
                for g, alts in sub.alternates.items():
                    yield index, [g], list(alts)
            elif kind == 4:
                for first, ligs in sub.ligatures.items():
                    for lig in ligs:
                        yield index, [first, *lig.Component], [lig.LigGlyph]
            elif kind == 8:
                for g, h in zip(sub.Coverage.glyphs, sub.Substitute):
                    yield index, [g], [h]


def substitution_problems(font: Path, tt: TTFont, listed: set[str]) -> list[str]:
    """No substitution writes a character it did not read: one character never becomes another."""
    found: dict[str, set[int]] = {}
    for index, read, written in substitution_rules(tt.get("GSUB")):
        for g in written:
            if g in listed and g not in read:
                found.setdefault(g, set()).add(index)
    return [
        f"{font}: error: {', '.join(f'lookup {i}' for i in sorted(found[g]))} writes {g}, a character, "
        "from other glyphs, so it is a spelling rule"
        for g in sorted(found)
    ]


def check(font: Path) -> list[str]:
    stem = font.stem
    problems = []
    found = families(font)
    if not found:
        return [f"{font}: error: no family in fonts.json names this file"]
    renderer = Renderer(font)
    tt = TTFont(str(font))
    cmap = tt.getBestCmap()
    listed = {cp(r["codepoint"]): r["glyph"] for f in found for r in f.get("codepoints") or []}
    problems += cmap_problems(font, cmap, listed)
    problems += substitution_problems(font, tt, set(listed.values()))
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
            if row["kind"] == "control":
                # A format control is reshaped by the layout it takes part in, so only its
                # cmap entry is checked here; tools/khelathi-zethu-glyphs/quadrats.py shapes it.
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
        by_glyph = {r["glyph"]: cp(r["codepoint"]) for r in rows}
        for sequence in SEQUENCES.get(stem, []):
            got = shape(renderer, "".join(chr(by_glyph[g]) for g in sequence), family)
            if got != sequence:
                problems.append(f"{font}: error: {label}: {' '.join(sequence)} shapes to {got}, not as written")
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
            excluded = not_characters(stem, renderer.order)
            for glyph in glyphs:
                if not_character(stem, glyph, excluded) or is_structural(glyph, set(glyphs)):
                    problems.append(f"fonts.json: error: {label}: {glyph} is not a character")
            for glyph in renderer.order:
                if glyph in glyphs or not_character(stem, glyph, excluded) or is_structural(glyph, set(glyphs)):
                    continue
                problems.append(f"{font}: error: {label}: the character {glyph} has no code point")
    if stem == "PirzathHand-Regular":
        carved = next((f for f in manifest()["families"] if f["name"] == "Pirzath Carved"), None)
        for family in found:
            if carved is None:
                problems.append(f"fonts.json: error: {family['name']}: there is no Pirzath Carved table to agree with")
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
