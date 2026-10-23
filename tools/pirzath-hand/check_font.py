# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Load the built hand font and confirm its character map, names, outlines and spacing.

    .venv/bin/python tools/pirzath-hand/check_font.py [fonts/PirzathHand-Regular.ttf]

The hand draws the same code points as the carved face, so the character map is
checked by the same rules, and Latin text draws the box. Every mapped glyph and every
lost letter must carry an outline, the default-ignorable characters must draw nothing,
every other character must map to the box (tools/notdef_box.py), and the .woff2
beside the .ttf must open and carry the same glyphs.

The hand is one printed face. It carries no joined forms and no ``ss01``, no
kerning, and no glyph named for a joined form. Every glyph with ink and an advance
stands at its ink with ``SB`` units of white either side; the length mark has no
advance; the notdef and the box keep their own width; and the space is ``SPACE``.
Each long vowel and each doubled consonant is drawn.
"""

import importlib.util
import sys
from pathlib import Path

from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent.parent


def _carved_check():
    spec = importlib.util.spec_from_file_location("pirzath_check", ROOT / "tools" / "pirzath" / "check_font.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


sys.path.insert(0, str(ROOT / "tools"))
import vertical  # noqa: E402

CARVED = _carved_check()
font_names = CARVED.font_names
notdef_box = CARVED.notdef_box

CONSONANTS = [
    "p", "b", "f", "v", "m", "t", "d", "t_h", "d_h", "n", "k", "g", "k_h", "g_h", "h", "s", "z", "l", "r",
    "sh", "zh", "ch", "ts", "j", "q", "ng", "ny", "hl", "catch", "w", "y",
]
VOWELS = ["a", "e", "i", "o", "u", "aacute", "eacute", "iacute", "oacute", "uacute", "ai", "au", "ei", "oi", "ou"]
DOUBLED = [f"{c}_{c}" for c in CONSONANTS]
MARKS = ["lengthmark"]
JOINED_SUFFIXES = (".init", ".medi", ".fina")
IGNORABLES = [*range(0x200B, 0x2010), *range(0x202A, 0x202F), *range(0x2066, 0x206A), 0xFEFF]
EMPTY = {"ignorable", "ignorable.sub"}
SB = 70  # the white either side of every sign's ink
SPACE = 500  # the word space
KEEP_WIDTH = {".notdef", "notdef.box", "space", *EMPTY, *MARKS}


def spacing_problems(font: TTFont) -> list[str]:
    """Every glyph with ink and an advance stands at its ink, SB either side."""
    from fontTools.pens.boundsPen import BoundsPen

    problems = []
    glyphset = font.getGlyphSet()
    hmtx = font["hmtx"]
    for name in font.getGlyphOrder():
        if name in KEEP_WIDTH:
            continue
        pen = BoundsPen(glyphset)
        glyphset[name].draw(pen)
        if pen.bounds is None:
            continue
        x0, _, x1, _ = pen.bounds
        adv = hmtx[name][0]
        if abs(x0 - SB) > 1 or abs(adv - x1 - SB) > 1:
            problems.append(f"{name}: its ink stands {x0:.0f} and {adv - x1:.0f} from its edges, not {SB}")
    if hmtx["space"][0] != SPACE:
        problems.append(f"the space is {hmtx['space'][0]} units, not {SPACE}")
    return problems


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
        elif name != "space" and name not in EMPTY and glyf[name].numberOfContours == 0:
            problems.append(f"U+{cp:04X} maps to {name}, which has no outline")
    problems += CARVED.latin_problems(cmap)
    for name in CARVED.LOST_LETTERS:
        if name not in order or glyf[name].numberOfContours == 0:
            problems.append(f"the lost letter {name} is missing or draws nothing")
    for name in CONSONANTS + VOWELS + DOUBLED + ["period", "exclam", "comma", "hyphen", "quote.open", "quote.close",
                                                ".notdef"] + [f"num.{i}" for i in range(16)]:
        if name not in order or glyf[name].numberOfContours == 0:
            problems.append(f"{name} is missing or draws nothing")
    if "space" not in order or glyf["space"].numberOfContours != 0:
        problems.append("the space must be in the font and draw nothing")
    for key in "?;:":
        if cmap.get(ord(key)) != notdef_box.BOX:
            problems.append(f"{key!r} is {cmap.get(ord(key))}; it must be {notdef_box.BOX}")
    problems += [line.split(": error: ", 1)[1] for line in notdef_box.check(path)]
    problems += [line.split(": error: ", 1)[1] for line in font_names.check(path)]
    hmtx = font["hmtx"]
    for cp in IGNORABLES:
        if cmap.get(cp) != "ignorable":
            problems.append(f"U+{cp:04X} must map to the empty glyph 'ignorable'")
    for name in EMPTY:
        if name not in order or glyf[name].numberOfContours != 0 or hmtx[name][0] != 0:
            problems.append(f"{name} must be in the font, empty and without advance")
    classes = font["GDEF"].table.GlyphClassDef.classDefs if "GDEF" in font else {}
    for name in MARKS:
        if name not in order or glyf[name].numberOfContours == 0:
            problems.append(f"{name} is missing or draws nothing")
        elif classes.get(name) != 3:
            problems.append(f"{name} is not a mark in GDEF")
        elif hmtx[name][0] != 0:
            problems.append(f"{name} has an advance")
    for name in ("GSUB", "GPOS"):
        if name not in font:
            problems.append(f"no {name} table")
    if "GSUB" in font:
        tags = {fr.FeatureTag for fr in font["GSUB"].table.FeatureList.FeatureRecord}
        for tag in ("ccmp", "liga", "rlig"):
            if tag not in tags:
                problems.append(f"no {tag} feature")
        if "ss01" in tags:
            problems.append("an ss01 feature is present; the hand is one printed face")
    if "GPOS" in font:
        tags = {fr.FeatureTag for fr in font["GPOS"].table.FeatureList.FeatureRecord}
        if "kern" in tags:
            problems.append("a kern feature is present; every sign stands at its own spacing")
        if "mark" not in tags:
            problems.append("no mark feature for the length mark over a vowel pair")
    joined = [g for g in order if g.endswith(JOINED_SUFFIXES)]
    if joined:
        problems.append(f"{len(joined)} joined forms are present, among them {sorted(joined)[0]}")
    if font["post"].italicAngle != 0:
        problems.append(f"the italic angle is {font['post'].italicAngle}; the hand stands upright")
    if font["head"].unitsPerEm != 1000:
        problems.append(f"units per em is {font['head'].unitsPerEm}, expected 1000")
    top = max(b for g in glyf.keys() if glyf[g].numberOfContours for b in [glyf[g].yMax])
    bottom = min(glyf[g].yMin for g in glyf.keys() if glyf[g].numberOfContours)
    hhea, os2 = font["hhea"], font["OS/2"]
    if hhea.ascent < top or hhea.descent > bottom:
        problems.append(f"the line metrics {hhea.ascent}/{hhea.descent} do not clear the ink {top}/{bottom}")
    if (hhea.ascent, hhea.descent, hhea.lineGap) != (vertical.ASCENT, vertical.DESCENT, vertical.LINE_GAP):
        problems.append(f"the line metrics are {hhea.ascent}/{hhea.descent}/{hhea.lineGap}, not the shared ones")
    if os2.usWinAscent < top or os2.usWinDescent < -bottom:
        problems.append("the Windows metrics do not clear the ink")
    names = {n.nameID: n.toUnicode() for n in font["name"].names if n.platformID == 3}
    expect = {
        1: "Pirzath Hand",
        5: "Version 0.3",
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
    problems += spacing_problems(font)

    woff2 = path.with_suffix(".woff2")
    if not woff2.exists():
        problems.append(f"{woff2} missing")
    else:
        w = TTFont(str(woff2))
        if w.getGlyphOrder() != font.getGlyphOrder():
            problems.append("woff2 glyph order differs from the ttf")
    print(f"{path}: {len(cmap)} code points mapped over {len(order)} glyphs, "
          f"{len(DOUBLED)} doubled consonants and {len(VOWELS) - 10} long vowels drawn, every sign {SB} units clear")
    return problems


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "fonts" / "PirzathHand-Regular.ttf"
    problems = check(path)
    for p in problems:
        print(f"{path}: error: {p}")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
