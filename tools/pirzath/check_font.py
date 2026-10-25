# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Load the built font and confirm every mapped character has a glyph.

    .venv/bin/python tools/pirzath/check_font.py [fonts/PirzathCarved-Regular.ttf]

Every code point in the cmap must name a glyph in the glyph order, and the
glyph must carry an outline unless it is one of the few that draw nothing by
design. The default-ignorable characters map to an empty glyph with no advance, and
every other character, Latin included, maps to the box (tools/notdef_box.py): the
face draws its own code points alone, which tools/codepoints.py checks.
The .woff2 beside the .ttf must open and carry the same glyphs.
"""

import sys
from pathlib import Path

from fontTools.ttLib import TTFont

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import font_names  # noqa: E402
import notdef_box  # noqa: E402

IGNORABLES = [*range(0x200B, 0x2010), *range(0x202A, 0x202F), *range(0x2066, 0x206A), 0xFEFF]
# HarfBuzz draws every default-ignorable as the space glyph, so the space glyph is
# empty, and a space draws its dot, space.dot, by a ccmp substitution.
EMPTY_BY_DESIGN = {"ignorable", "ignorable.sub", "space"}

# Latin text is not the face's: every Latin letter, digit and mark draws the box,
# and the space is the only character the face shares with it.
LATIN = "0123456789@#$%^&\"“”«»[]<>.!¡,-'’" + "bdgkptvfzshmnlrcaeiouyjqwxBDGKPTVFZSHMNLRCAEIOUYJQWX" + "áéíóúÁÉÍÓÚ"


def latin_problems(cmap: dict[int, str]) -> list[str]:
    """Every Latin character draws the box."""
    return [
        f"{ch!r} maps to {cmap.get(ord(ch))}; Latin text draws {notdef_box.BOX}"
        for ch in LATIN
        if cmap.get(ord(ch)) != notdef_box.BOX
    ]


# The seventeen lost letters, each of which must be in the font with an outline.
LOST_LETTERS = [
    "sh", "zh", "ch", "j", "ts", "q", "ng", "ny", "hl", "w", "catch", "y",
    "ai", "au", "ei", "oi", "ou",
]


def check(path: Path) -> list[str]:
    problems = []
    font = TTFont(str(path))
    order = set(font.getGlyphOrder())
    glyf = font["glyf"]
    cmap = font.getBestCmap()
    if not cmap:
        return ["no Unicode cmap"]
    for cp, name in sorted(cmap.items()):
        if name not in order:
            problems.append(f"U+{cp:04X} maps to {name}, which is not in the font")
        elif name not in EMPTY_BY_DESIGN and glyf[name].numberOfContours == 0:
            problems.append(f"U+{cp:04X} maps to {name}, which has no outline")
    problems += latin_problems(cmap)
    for name in LOST_LETTERS:
        if name not in order or glyf[name].numberOfContours == 0:
            problems.append(f"the lost letter {name} is missing or draws nothing")
    for name in ("numopen", "numclose", "question", "semicolon", "colon"):
        if name in order:
            problems.append(f"{name} is still in the font")
    for name in ("space.dot", "period", "exclam", "comma"):
        if glyf[name].numberOfContours == 0:
            problems.append(f"{name} draws nothing")
    if glyf["space"].numberOfContours != 0:
        problems.append("space draws; it must be empty, with the dot of a space drawn by substitution")
    cmap = font.getBestCmap()
    for key in "?;:":
        if cmap.get(ord(key)) != notdef_box.BOX:
            problems.append(f"{key!r} is {cmap.get(ord(key))}; it must be {notdef_box.BOX}")
    hmtx = font["hmtx"]
    for cp in IGNORABLES:
        if cmap.get(cp) != "ignorable":
            problems.append(f"U+{cp:04X} must map to the empty glyph 'ignorable'")
    for name in ("ignorable", "ignorable.sub"):
        if name not in order or glyf[name].numberOfContours != 0 or hmtx[name][0] != 0:
            problems.append(f"{name} must be in the font, empty and without advance")
    problems += [line.split(": error: ", 1)[1] for line in notdef_box.check(path)]
    problems += [line.split(": error: ", 1)[1] for line in font_names.check(path)]
    classes = font["GDEF"].table.GlyphClassDef.classDefs if "GDEF" in font else {}
    for name in ("lengthmark", "doubling"):
        if name not in order or glyf[name].numberOfContours == 0:
            problems.append(f"{name} is missing or draws nothing")
        elif classes.get(name) != 3:
            problems.append(f"{name} is not a mark in GDEF")
    for name in ("GSUB", "GPOS"):
        if name not in font:
            problems.append(f"no {name} table")
    names = {n.nameID: n.toUnicode() for n in font["name"].names if n.platformID == 3}
    expect = {
        1: "Pirzath Carved",
        5: "Version 0.1",
        13: "SIL Open Font License 1.1",
        14: "https://openfontlicense.org",
    }
    for nid, value in expect.items():
        if names.get(nid) != value:
            problems.append(f"name {nid} is {names.get(nid)!r}, expected {value!r}")
    if 7 in names:
        problems.append("name table carries a trademark")
    if not names.get(0, "").startswith("Copyright"):
        problems.append("name table carries no copyright line")

    woff2 = path.with_suffix(".woff2")
    if not woff2.exists():
        problems.append(f"{woff2} missing")
    else:
        w = TTFont(str(woff2))
        if w.getGlyphOrder() != font.getGlyphOrder():
            problems.append("woff2 glyph order differs from the ttf")
    print(f"{path}: {len(cmap)} code points mapped over {len(order)} glyphs")
    return problems


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else (
        Path(__file__).resolve().parent.parent.parent / "fonts" / "PirzathCarved-Regular.ttf"
    )
    problems = check(path)
    for p in problems:
        print(f"{path}: error: {p}")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
