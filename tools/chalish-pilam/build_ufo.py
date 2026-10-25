# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Write ``sources/ChalishPilamCommon.ufo`` from the glyphs of ``glyphs.py``.

    .venv/bin/python tools/chalish-pilam/build_ufo.py [--out sources/ChalishPilamCommon.ufo]

**The encoding.** ``tools/chalish-pilam/encoding.json`` is the one table of code
points. The numbers sit at U+F3000: zero (the shell) first, then 1 to 19, then the
places of the count, 20, 400, 8,000 and 160,000. The 24 core
glyphs take U+F3020 to U+F3037. Every other glyph takes the next free code point in
the order it is added, so no
glyph is ever renumbered: this script appends a glyph it does not find in the table
and never moves one it does. A glyph removed from ``glyphs.py`` keeps its row, marked
``retired``, so its code point is never reused.

**The cell.** Every glyph is drawn in a square cell ``BLOCK`` units high standing on the
line, and every glyph takes one advance, the cell and its gutter, whatever its ink:
the cell is implied, so the advance is the same for all. A column two advances wide
therefore wraps a run into rows of two by ordinary line breaking. The space is one
empty cell.
"""

import argparse
import json
import shutil
import sys
from pathlib import Path

import ufoLib2
from fontTools.pens.pointPen import SegmentToPointPen
from ufoLib2.objects import Contour, Point

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "tools"))
import glyphs as K  # noqa: E402
import notdef_box  # noqa: E402
import strokes as S  # noqa: E402

FAMILY = "Chalish Pilam Common"
STEM = "ChalishPilamCommon"
ENCODING = HERE / "encoding.json"
NUMBERS = 0xF3000  # zero, then 1 to 19
CONCEPTS = 0xF3020  # every other glyph, in the order it is added
GUTTER = 60.0  # the white each side of the cell
ADVANCE = S.BLOCK + 2 * GUTTER
WIN_ASCENT, WIN_DESCENT = 945, 250
IGNORABLES = [*range(0x200B, 0x2010), *range(0x202A, 0x202F), *range(0x2066, 0x206A), 0xFEFF]

FEATURES = """\
# HarfBuzz replaces a default-ignorable character the font maps directly with
# the space glyph, so it draws nothing only when it is substituted. Each
# ignorable is substituted once, to a second empty glyph.
feature ccmp {
  sub ignorable by ignorable.sub;
} ccmp;
"""


def glyph_name(g) -> str:
    if g is K.ZERO:
        return "n0"
    return g.name.lower()


def numbers():
    """Zero, 1 to 19, then the places of the count, in code point order from U+F3000."""
    return [K.ZERO] + K.NUMERALS + K.PLACES


def all_glyphs():
    """Zero and the numbers, then the core in its order, then every other glyph."""
    return numbers() + [g for g in K.GLYPHS if g is not K.ZERO]


def encoding() -> list[dict]:
    """The encoding table, with any glyph not yet in it appended."""
    rows = json.loads(ENCODING.read_text())["glyphs"] if ENCODING.exists() else []
    by_name = {r["glyph"]: r for r in rows}
    used = {int(r["codepoint"][2:], 16) for r in rows}
    current = set()
    for g in all_glyphs():
        name = glyph_name(g)
        current.add(name)
        if name in by_name:
            r = by_name[name]
        else:
            if g in numbers():
                cp = NUMBERS + numbers().index(g)
            elif g in K.CORE:
                cp = CONCEPTS + K.CORE.index(g)
            else:
                cp = CONCEPTS + len(K.CORE)
                while cp in used:
                    cp += 1
            used.add(cp)
            r = {"glyph": name, "codepoint": f"U+{cp:05X}"}
            rows.append(r)
            by_name[name] = r
        r.update({"concept": g.meaning, "word": g.word, "sound": g.sound,
                  "kind": "number" if g in numbers() else "concept", "tier": g.tier})
        if g.traditional:
            r["traditional"] = True
        r.pop("retired", None)
        if g in K.CORE and int(r["codepoint"][2:], 16) != CONCEPTS + K.CORE.index(g):
            raise SystemExit(f"{ENCODING.name}: error: core glyph {name} is not at U+{CONCEPTS + K.CORE.index(g):05X}")
    for r in rows:
        if r["glyph"] not in current:
            r["retired"] = True
    rows.sort(key=lambda r: int(r["codepoint"][2:], 16))
    ENCODING.write_text(json.dumps({"glyphs": rows}, indent=2, ensure_ascii=False) + "\n")
    return rows


def draw(glyph, path):
    """Draw a pathops path into a UFO glyph, shifted right by the gutter."""
    pen = SegmentToPointPen(glyph.getPointPen())
    shifted = path.__class__()
    tp = shifted.getPen()

    class Shift:
        def moveTo(self, p):
            tp.moveTo((p[0] + GUTTER, p[1]))

        def lineTo(self, p):
            tp.lineTo((p[0] + GUTTER, p[1]))

        def qCurveTo(self, *ps):
            tp.qCurveTo(*[(x + GUTTER, y) for x, y in ps])

        def curveTo(self, *ps):
            tp.curveTo(*[(x + GUTTER, y) for x, y in ps])

        def closePath(self):
            tp.closePath()

        def endPath(self):
            tp.endPath()

    path.draw(Shift())
    shifted.draw(pen)


def build(out: Path) -> Path:
    rows = encoding()
    by_name = {glyph_name(g): g for g in all_glyphs()}

    font = ufoLib2.Font()
    info = font.info
    info.familyName = FAMILY
    info.styleName = "Regular"
    info.styleMapFamilyName = FAMILY
    info.styleMapStyleName = "regular"
    info.copyright = 'Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>'
    info.unitsPerEm = 1000
    info.ascender, info.descender = S.ASCENT, S.DESCENT
    info.openTypeHheaAscender, info.openTypeHheaDescender, info.openTypeHheaLineGap = S.ASCENT, S.DESCENT, S.LINE_GAP
    info.openTypeOS2TypoAscender, info.openTypeOS2TypoDescender = S.ASCENT, S.DESCENT
    info.openTypeOS2TypoLineGap = S.LINE_GAP
    info.openTypeOS2WinAscent, info.openTypeOS2WinDescent = WIN_ASCENT, WIN_DESCENT
    info.openTypeOS2Selection = [7]
    info.openTypeOS2Type = []
    info.openTypeOS2UnicodeRanges = []
    info.openTypeOS2CodePageRanges = []
    info.openTypeOS2VendorID = "HRLD"
    info.openTypeHeadCreated = "2026/01/01 00:00:00"
    info.openTypeHeadFlags = [0, 3]
    info.openTypeHeadLowestRecPPEM = 3
    info.openTypeNameDescription = (
        "Chalish Pilam Common, the common hand of the Ki'ich'chik writing in thalorna: skeleton ideograms in one "
        "even line, each in a square cell that is never drawn, read two to a row down a column."
    )
    info.openTypeNameLicense = "SIL Open Font License 1.1"
    info.openTypeNameLicenseURL = "https://openfontlicense.org"
    info.openTypeNameUniqueID = f"{STEM}-Regular;0.1"
    info.openTypeNameVersion = "Version 0.1"
    info.versionMajor, info.versionMinor = 0, 100
    info.postscriptFontName = f"{STEM}-Regular"
    info.postscriptUnderlinePosition = -100
    info.postscriptUnderlineThickness = 40
    info.capHeight = round(S.BLOCK)
    info.xHeight = round(S.BLOCK)

    zethu = ufoLib2.Font.open(ROOT / "sources" / "KhelathiZethuGlyphs.ufo")
    order = [".notdef", notdef_box.BOX, "space", "ignorable", "ignorable.sub"]
    for name in (".notdef", notdef_box.BOX):
        g = font.newGlyph(name)
        src = zethu[name]
        g.width = src.width
        for c in src.contours:
            g.contours.append(Contour([Point(p.x, p.y, p.segmentType) for p in c.points]))
    font.newGlyph("space").width = ADVANCE
    font["space"].unicodes = [0x20, 0xA0]
    for name in ("ignorable", "ignorable.sub"):
        font.newGlyph(name).width = 0
    font["ignorable"].unicodes = IGNORABLES
    taken = set(font["space"].unicodes) | set(IGNORABLES)
    font[notdef_box.BOX].unicodes = [c for c in notdef_box.codepoints() if c not in taken]

    for r in rows:
        if r.get("retired"):
            continue
        name = r["glyph"]
        g = font.newGlyph(name)
        draw(g, S.ink(by_name[name].draw(), S.COMMON))
        g.width = ADVANCE
        g.unicodes = [int(r["codepoint"][2:], 16)]
        order.append(name)

    font.lib["public.glyphOrder"] = order
    font.lib["public.openTypeCategories"] = {n: "base" for n in order if n not in ("ignorable", "ignorable.sub")}
    font.features.text = FEATURES
    if out.exists():
        shutil.rmtree(out)
    font.save(out)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "sources" / f"{STEM}.ufo"))
    args = ap.parse_args()
    print(build(Path(args.out)))


if __name__ == "__main__":
    main()
