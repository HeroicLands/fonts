# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Write sources/SemaronKuriale.ufo from the drawing kit.

    .venv/bin/python tools/semaron-kuriale/build_ufo.py [--out sources/SemaronKuriale.ufo]

``kit.py`` draws every letter. Each glyph's outline is the contours the kit composes,
rounded to the font's grid and then scaled by the face's factor in ``tools/vertical.py``,
so the letters stand at the shared x-height and cap height. The advance of a letter is
its ink and one sidebearing either side, as the kit sets it; the space takes the word space. The catch is a zero-advance mark whose head is its origin;
each base carries an anchor where the catch stands. Each character stands on the code
point ``tools/codepoint_order.py`` gives it, and every other character prints the box
(``tools/apply_notdef_box.py``). The UFO is generated: an edit to a letter belongs in
``kit.py``, and this script is run after it, before ``build.sh`` compiles the UFO.

The features. ``ccmp`` empties the default-ignorables and draws a catch with no letter
before it as the box. ``mark`` sets the catch over the base it follows.
"""

import argparse
import math
import statistics
import sys
from fractions import Fraction
from pathlib import Path

import ufoLib2

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "tools"))
import apply_notdef_box  # noqa: E402
import codepoint_order  # noqa: E402
import kit as K  # noqa: E402
import vertical  # noqa: E402

STEM = "SemaronKuriale"
SCALE = Fraction(str(vertical.SCALES[STEM]))
SPACE = 24
IGNORABLES = [*range(0x200B, 0x2010), *range(0x202A, 0x202F), *range(0x2066, 0x206A), 0xFEFF]

# The glyphs the kit draws, in glyph order, then the font's own.
LONGS = [f"{v}.long" for v in K.VOWELS]
MAJ_LONGS = [f"{v.upper()}.long" for v in K.VOWELS]
NUMERALS = [f"num.{i}" for i in range(10)]
LETTERS = [g for pair in K.ALPHABET for g in (pair[1], pair[0])]
CATCH_LETTERS = [g for pair in K.ALPHABET for g in (pair[1],)] + [pair[0] for pair in K.ALPHABET]
ORDER = [".notdef", "space", *LETTERS, *LONGS, *MAJ_LONGS, *NUMERALS, "point", "grave",
         "ignorable", "ignorable.sub"]
BASES = sorted(K.BASES)


def _r(v):
    return int(math.floor(v + 0.5))


def _scaled(v):
    return int(math.floor(Fraction(v) * SCALE + Fraction(1, 2)))


def contours_of(g):
    """The glyph's contours rounded to the grid and scaled, outer contours counter-clockwise, as the UFO wants them."""
    out = []
    flip = bool(g.contours) and g.contours[0][0] < 0
    for _, c in g.contours:
        pts = []
        for x, y in c:
            p = (_scaled(_r(x)), _scaled(_r(y)))
            if not pts or pts[-1] != p:
                pts.append(p)
        if len(pts) > 1 and pts[0] == pts[-1]:
            pts.pop()
        if len(pts) < 3:
            continue
        out.append(pts[::-1] if flip else pts)
    return out


def draw(glyph, contours):
    pen = glyph.getPen()
    for pts in contours:
        pen.moveTo(pts[0])
        for p in pts[1:]:
            pen.lineTo(p)
        pen.closePath()


def features(anchors):
    bases = [g for g in ORDER if g != "grave"] + ["notdef.box"]
    catch_bases = CATCH_LETTERS + LONGS + MAJ_LONGS
    lines = [
        "languagesystem DFLT dflt;",
        "languagesystem latn dflt;",
        "",
        "# The glyphs a catch can stand on.",
        f"@BASE = [{' '.join(catch_bases)}];",
        "",
        "# The face draws each character from its own code point. HarfBuzz replaces a",
        "# default-ignorable character the font maps directly with the space glyph, so each",
        "# ignorable is substituted once, to a second empty glyph; and a catch with no",
        "# letter before it is the box.",
        "feature ccmp {",
        "lookup ccmp_ignorable {",
        "  sub ignorable by ignorable.sub;",
        "} ccmp_ignorable;",
        "lookup ccmp_catch {",
        "  ignore sub @BASE grave';",
        "  sub grave' by notdef.box;",
        "} ccmp_catch;",
        "} ccmp;",
        "",
        "table GDEF {",
        f"  GlyphClassDef [{' '.join(bases)}], , [grave], ;",
        "} GDEF;",
        "",
        "markClass grave <anchor 0 0> @CATCH;",
        "",
        "# The catch stands over an x-height letter, at the upper right of a tall stem and to the right of a",
        "# long vowel's curl.",
        "feature mark {",
    ]
    for g in LETTERS + LONGS + MAJ_LONGS:
        x, y = anchors[g]
        lines.append(f"  pos base {g} <anchor {x} {y}> mark @CATCH;")
    lines += ["} mark;", ""]
    return "\n".join(lines)


def build(out: Path) -> Path:
    font = ufoLib2.Font()
    info = font.info
    info.familyName = "Semaron Kuriale"
    info.styleName = "Regular"
    info.styleMapFamilyName = "Semaron Kuriale"
    info.styleMapStyleName = "regular"
    info.versionMajor, info.versionMinor = 0, 100
    info.copyright = 'Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>'
    info.openTypeNameDescription = (
        "The Kuriale hand of Semaron, the Vylarian alphabet of thalorna, written with a broad nib."
    )
    info.openTypeNameLicense = "SIL Open Font License 1.1"
    info.openTypeNameLicenseURL = "https://openfontlicense.org"
    info.openTypeNameUniqueID = f"{STEM}-Regular;0.1"
    info.openTypeNameVersion = "Version 0.1"
    info.openTypeHeadCreated = "2026/01/01 00:00:00"
    info.openTypeHeadFlags = [0, 3]
    info.openTypeHeadLowestRecPPEM = 3
    info.openTypeOS2Type = []
    info.openTypeOS2VendorID = "HRLD"
    info.openTypeOS2Selection = [7]
    info.openTypeOS2UnicodeRanges = []
    info.openTypeOS2CodePageRanges = []
    info.postscriptFontName = f"{STEM}-Regular"
    info.unitsPerEm = K.EM
    info.ascender, info.descender = vertical.ASCENT, vertical.DESCENT
    info.openTypeHheaAscender, info.openTypeHheaDescender = vertical.ASCENT, vertical.DESCENT
    info.openTypeHheaLineGap = vertical.LINE_GAP
    info.openTypeOS2TypoAscender, info.openTypeOS2TypoDescender = vertical.ASCENT, vertical.DESCENT
    info.openTypeOS2TypoLineGap = vertical.LINE_GAP
    info.italicAngle = -K.SLANT
    info.openTypeHheaCaretSlopeRise, info.openTypeHheaCaretSlopeRun = 1000, round(1000 * K.TAN)
    info.postscriptUnderlinePosition = _scaled(-80)
    info.postscriptUnderlineThickness = _scaled(K.HAIR)

    unis = {}
    for row in codepoint_order.ltr_table(f"{STEM}-Regular"):
        unis.setdefault(row["glyph"], []).append(int(row["codepoint"][2:], 16))
    unis["space"] = [0x20, 0xA0]
    unis["ignorable"] = IGNORABLES

    shapes, widths, anchors = {}, {}, {}
    for name in ORDER:
        if name in ("ignorable", "ignorable.sub"):
            shapes[name], widths[name] = [], 0
            continue
        g = K.glyph(name)
        shapes[name] = contours_of(g)
        if g.anchor is not None:
            anchors[name] = (_scaled(_r(g.anchor[0])), _scaled(_r(g.anchor[1])))
        widths[name] = _scaled(_r(g.adv))
    widths["space"] = SPACE
    assert set(anchors) == set(BASES), set(BASES) ^ set(anchors)

    for name in ORDER:
        glyph = font.newGlyph(name)
        glyph.width = widths[name]
        glyph.unicodes = sorted(unis.get(name, []))
        draw(glyph, shapes[name])
        if name in anchors:
            glyph.appendAnchor({"name": "top", "x": anchors[name][0], "y": anchors[name][1]})
    font["grave"].appendAnchor({"name": "_top", "x": 0, "y": 0})
    font.glyphOrder = ORDER
    font.lib["public.glyphOrder"] = ORDER
    font.lib["public.openTypeCategories"] = dict(sorted(
        {nm: ("mark" if nm == "grave" else "base") for nm in ORDER}.items()))
    font.features.text = features(anchors)

    def median_height(names):
        hs = []
        for n in names:
            b = font[n].getBounds(font) if n in font else None
            if b:
                hs.append(b.yMax - b.yMin)
        return round(statistics.median(hs))

    info.xHeight = median_height(vertical.typical(STEM, "x"))
    info.capHeight = median_height(vertical.typical(STEM, "cap"))
    tops, bottoms = [], []
    for glyph in font:
        b = glyph.getControlBounds(font)
        if b:
            tops.append(b[3])
            bottoms.append(b[1])
    info.openTypeOS2WinAscent = max(vertical.WIN_ASCENT, math.ceil(max(tops)))
    info.openTypeOS2WinDescent = max(vertical.WIN_DESCENT, math.ceil(-min(bottoms)))

    font.save(out, overwrite=True)
    apply_notdef_box.apply(out)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default=str(ROOT / "sources" / f"{STEM}.ufo"))
    print(build(Path(ap.parse_args().out)))


if __name__ == "__main__":
    main()
