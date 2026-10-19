# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Load the built font and confirm every mapped character has a glyph.

    .venv/bin/python src/check_font.py [fonts/PirzathCarved-Regular.ttf]

Every code point in the cmap must name a glyph in the glyph order, and the
glyph must carry an outline unless it is one of the few that draw nothing by
design. The .woff2 beside the .ttf must open and carry the same glyphs.
"""

import sys
from pathlib import Path

from fontTools.ttLib import TTFont

sys.path.insert(0, str(Path(__file__).parent))
import glyphs as G  # noqa: E402

EMPTY_BY_DESIGN = set()

# What the owner's rulings say these keys type, independent of the glyph source.
RULED = {
    **{str(i): f"num.{i}" for i in range(10)},
    "@": "num.10",
    "#": "num.11",
    "$": "num.12",
    "%": "num.13",
    "^": "num.14",
    "&": "num.15",
    '"': "quotedbl",
    "“": "quote.open",
    "”": "quote.close",
    "«": "quote.open",
    "»": "quote.close",
    "[": "quote.open",
    "]": "quote.close",
    "<": "less",
    ">": "greater",
    " ": "space",
    ".": "period",
    "!": "exclam",
    ",": "comma",
    "-": "hyphen",
    "a": "a",
    "b": "b",
    "c": "c",
    "d": "d",
    "e": "e",
    "f": "f",
    "j": "j",
    "q": "q",
    "w": "w",
    "y": "y",
    "J": "j",
    "Q": "q",
    "W": "w",
    "Y": "y",
    "'": "catch",
    "\u2019": "catch",
}

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
    for cp, name in G.cmap().items():
        if cmap.get(cp) != name:
            problems.append(f"U+{cp:04X} should map to {name}, maps to {cmap.get(cp)}")
    for ch, name in RULED.items():
        if cmap.get(ord(ch)) != name:
            problems.append(f"{ch!r} should type {name}, types {cmap.get(ord(ch))}")
    for name in LOST_LETTERS:
        if name not in order or glyf[name].numberOfContours == 0:
            problems.append(f"the lost letter {name} is missing or draws nothing")
    for name in ("numopen", "numclose", "question", "semicolon", "colon"):
        if name in order:
            problems.append(f"{name} is still in the font")
    for name in ("space", "period", "exclam", "comma"):
        if glyf[name].numberOfContours == 0:
            problems.append(f"{name} draws nothing")
    cmap = font.getBestCmap()
    for key in "?;:":
        if ord(key) in cmap:
            problems.append(f"{key!r} is mapped; it must fall to .notdef")
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
        Path(__file__).resolve().parent.parent / "fonts" / "PirzathCarved-Regular.ttf"
    )
    problems = check(path)
    for p in problems:
        print(f"{path}: error: {p}")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
