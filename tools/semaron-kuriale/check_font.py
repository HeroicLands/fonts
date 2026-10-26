# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Load the built Semaron Kuriale font and confirm its character map, names, outlines and catch.

    .venv/bin/python tools/semaron-kuriale/check_font.py [fonts/SemaronKuriale-Regular.ttf]

The font carries letters and dedicated consonant groups in both cases, five long
vowels with their majuscules, the numerals, the point and the catch. The checks:

- every letter, long vowel, numeral and the point has an outline, and the space
  and the default-ignorables draw nothing;
- the space is U+0020 and U+00A0, and every other character of the box ranges,
  Latin text included, maps to the box (tools/notdef_box.py): the face draws its
  own code points alone, which tools/codepoints.py checks;
- the names, the OS/2 declarations (tools/font_names.py) and the win metrics
  (tools/notdef_box.py) pass, and the win metrics also enclose the catch where
  it stands on its base;
- the catch is a zero-advance mark in GDEF, and every base carries a GPOS anchor
  for it;
- the .woff2 beside the .ttf opens and carries the same glyphs.
"""

import sys
from pathlib import Path

from fontTools.pens.boundsPen import BoundsPen
from fontTools.ttLib import TTFont

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import font_names  # noqa: E402
import notdef_box  # noqa: E402
import vertical  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent

LETTERS = ["a", "b", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "th", "u",
           "v", "w", "y", "z"]
LETTERS += [n.upper() for n in LETTERS]
LONGS = [f"{v}.long" for v in "aeiou"] + [f"{v.upper()}.long" for v in "aeiou"]
NUMERALS = [f"num.{i}" for i in range(10)]
DRAWN = LETTERS + LONGS + NUMERALS + ["point", "grave", ".notdef"]
BASES = LETTERS + LONGS
# These assigned signs remain blocked until their glyph designs are supplied.
AELWYTHI_REQUIRED = [0xF0217, 0xF0247, *range(0xF0280, 0xF0292)]
EMPTY = {"ignorable", "ignorable.sub", "space"}
IGNORABLES = [*range(0x200B, 0x2010), *range(0x202A, 0x202F), *range(0x2066, 0x206A), 0xFEFF]

# Latin text, which must print the box: the face draws its own code points alone.
BOXED = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZáéíóúÁÉÍÓÚ0123456789.,;:—–'’`-‐‑?!¡\"“”«»()[]<>"


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
    for point in AELWYTHI_REQUIRED:
        name = cmap.get(point)
        if name is None or name not in order or name in {".notdef", "notdef.box"} or glyf[name].numberOfContours == 0:
            problems.append(f"U+{point:04X} requires a supplied Aelwythi glyph design")
    for name in DRAWN:
        if name not in order or glyf[name].numberOfContours == 0:
            problems.append(f"{name} is missing or draws nothing")
    for code in (0x20, 0xA0):
        if cmap.get(code) != "space":
            problems.append(f"U+{code:04X} maps to {cmap.get(code)}, not space")
    for ch in BOXED:
        if cmap.get(ord(ch)) != notdef_box.BOX:
            problems.append(f"{ch!r} is {cmap.get(ord(ch))}; it must be {notdef_box.BOX}")
    hmtx = font["hmtx"]
    if "space" not in order or glyf["space"].numberOfContours != 0:
        problems.append("the space must be in the font and draw nothing")
    for cp in IGNORABLES:
        if cmap.get(cp) != "ignorable":
            problems.append(f"U+{cp:04X} must map to the empty glyph 'ignorable'")
    if cmap.get(0xE0114) != "ignorable":
        problems.append("the stress modifier U+E0114 must map to the empty glyph ignorable")
    for name in EMPTY - {"space"}:
        if name not in order or glyf[name].numberOfContours != 0 or hmtx[name][0] != 0:
            problems.append(f"{name} must be in the font, empty and without advance")
    problems += [line.split(": error: ", 1)[1] for line in notdef_box.check(path)]
    problems += [line.split(": error: ", 1)[1] for line in font_names.check(path)]

    classes = font["GDEF"].table.GlyphClassDef.classDefs if "GDEF" in font else {}
    if classes.get("grave") != 3:
        problems.append("grave is not a mark in GDEF")
    if "grave" in order and hmtx["grave"][0] != 0:
        problems.append("grave has an advance")
    anchored = set()
    if "GPOS" in font:
        tags = {fr.FeatureTag for fr in font["GPOS"].table.FeatureList.FeatureRecord}
        if "mark" not in tags:
            problems.append("no mark feature")
        if "kern" in tags:
            problems.append("a kern feature is present; the catch takes no room and letters stand apart")
        for lookup in font["GPOS"].table.LookupList.Lookup:
            for sub in lookup.SubTable:
                if sub.LookupType == 4:
                    anchored |= set(sub.BaseCoverage.glyphs)
    else:
        problems.append("no GPOS table")
    for name in BASES:
        if name not in anchored:
            problems.append(f"{name} has no anchor for the catch")
    if "GSUB" in font:
        tags = {fr.FeatureTag for fr in font["GSUB"].table.FeatureList.FeatureRecord}
        if "ccmp" not in tags:
            problems.append("no ccmp feature")
    else:
        problems.append("no GSUB table")

    if font["head"].unitsPerEm != 1000:
        problems.append(f"units per em is {font['head'].unitsPerEm}, expected 1000")
    glyphs = font.getGlyphSet()
    hhea, os2 = font["hhea"], font["OS/2"]
    top, bottom, band = -10**6, 10**6, 10**6
    for name in font.getGlyphOrder():
        pen = BoundsPen(glyphs)
        glyphs[name].draw(pen)
        if pen.bounds:
            top, bottom = max(top, pen.bounds[3]), min(bottom, pen.bounds[1])
            # The accepted overshoot of tools/vertical.py reaches past the line metrics.
            if name.split(".")[0] not in vertical.OVERSHOOT["SemaronKuriale"]:
                band = min(band, pen.bounds[1])
    # The catch where it stands on a base: its own bounds moved to the base's anchor.
    pen = BoundsPen(glyphs)
    glyphs["grave"].draw(pen)
    for sub in (s for lk in font["GPOS"].table.LookupList.Lookup for s in lk.SubTable if s.LookupType == 4):
        for record in sub.BaseArray.BaseRecord:
            for anchor in record.BaseAnchor:
                if anchor is not None:
                    top = max(top, anchor.YCoordinate + pen.bounds[3])
                    bottom = min(bottom, anchor.YCoordinate + pen.bounds[1])
                    band = min(band, anchor.YCoordinate + pen.bounds[1])
    if hhea.ascent < top or hhea.descent > band:
        problems.append(f"the line metrics {hhea.ascent}/{hhea.descent} do not clear the ink {top}/{band}")
    if os2.usWinAscent < top or os2.usWinDescent < -bottom:
        problems.append(f"the Windows metrics {os2.usWinAscent}/{os2.usWinDescent} do not clear the ink {top}/{bottom}")
    names = {n.nameID: n.toUnicode() for n in font["name"].names if n.platformID == 3}
    expect = {
        1: "Semaron Kuriale",
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
    elif TTFont(str(woff2)).getGlyphOrder() != font.getGlyphOrder():
        problems.append("woff2 glyph order differs from the ttf")
    print(f"{path}: {len(cmap)} code points mapped over {len(order)} glyphs, {len(BASES)} bases anchored for the catch")
    return problems


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "fonts" / "SemaronKuriale-Regular.ttf"
    problems = check(path)
    for p in problems:
        print(f"{path}: error: {p}")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
