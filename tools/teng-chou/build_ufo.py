# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Write sources/TengChou.ufo from the Teng Chou data.

    .venv/bin/python tools/teng-chou/build_ufo.py [--out sources/TengChou.ufo]

Every character of ``characters.py`` is laid out by ``layout.py``, and every stage
of the tally (``tally.py``) and every sign of ``syllabary.py`` drawn, outlined with the brush, fitted with cubic curves
(``fit.py``) and written as one glyph, ``tc.<morpheme>`` or ``js.<syllable>``, on the
code point ``tools/codepoint_order.py`` assigns it. The UFO is generated: an edit
belongs in the data, and this script is run after it, before ``build.sh`` compiles
the UFO. The UFO is committed, so the build compiles the same source on every
platform. The character names, ``tools/names/tengchou.json``, are written beside it.

**Metrics.** Each glyph is the 1000-unit square of the layout scaled by ``SCALE``,
which brings the median height of the characters to the cap height every face
shares (tools/vertical.py). Along a line, an inline span, a glyph's advance is its
ink width and ``SIDEBEARING`` a side, as every face of the repository is spaced.
Down a column, the vertical advance of every character and sign is exactly one em,
with the square centred in it and the vertical origin half an em above the
square's centre, so a column of N characters is N em tall and each sits centred on
the column's axis. The square's centre stands ``CENTRE`` units above the baseline.

The notdef and its box are Khelathi Zethu Glyphs', and the box takes every Latin and
punctuation code point (tools/notdef_box.py); the default-ignorables draw nothing.
"""

from __future__ import annotations

import argparse
import json
import shutil
import statistics
import sys
from pathlib import Path

import ufoLib2
from ufoLib2.objects import Glyph
from ufoLib2.objects.contour import Contour
from ufoLib2.objects.point import Point

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))
import characters as C  # noqa: E402
import codepoint_order  # noqa: E402
import fit  # noqa: E402
import layout as Y  # noqa: E402
import notdef_box  # noqa: E402
import strokes as S  # noqa: E402
import syllabary as J  # noqa: E402
import tally as T  # noqa: E402

FAMILY = "Teng Chou"
CAP = 730  # the cap height every face shares, which the characters' median ink height meets
CENTRE = 355  # the square's centre above the baseline
UPM = 1000
SPACE = 250  # the space between inline words of a roman text
SIDEBEARING = 30  # each side of the ink, along a line
ASCENT, DESCENT, LINE_GAP = 945, -200, 100
WIN_ASCENT, WIN_DESCENT = 945, 250

FEATURES = """languagesystem DFLT dflt;

# HarfBuzz replaces a default-ignorable character the font maps directly with
# the space glyph. A glyph that a lookup substitutes is left alone, so each
# ignorable is substituted once, to a second empty glyph.
feature ccmp {
  sub ignorable by ignorable.sub;
} ccmp;
"""


def outlines():
    """Every glyph's polygons on the layout's 1000-unit square, by glyph name, in code point order."""
    out = {}
    for ch in C.CHARACTERS:
        out[ch.glyph] = S.contours(Y.render(ch.formula, ch.overrides))
    for stage in T.STAGES.values():
        out[stage.glyph] = S.contours(T.render(stage.count))
    for sign in J.SIGNS:
        out[sign.glyph] = S.contours(J.render(sign.syllable))
    return out


def scale_for(polys_by_glyph) -> float:
    heights = []
    for name, polys in polys_by_glyph.items():
        if name.startswith("tc."):
            ys = [y for p in polys for _, y in p]
            heights.append(max(ys) - min(ys))
    return round(CAP / statistics.median(heights), 4)


def draw(glyph: Glyph, polys, k: float, dy: float, dx: float = 0.0):
    for start, segs in fit.fit([[(x * k + dx, y * k + dy) for x, y in p] for p in polys]):
        contour = Contour()
        for seg in segs:
            if seg[0] == "line":
                contour.points.append(Point(round(seg[1][0]), round(seg[1][1]), "line"))
            else:
                _, c1, c2, end = seg
                contour.points.append(Point(round(c1[0]), round(c1[1])))
                contour.points.append(Point(round(c2[0]), round(c2[1])))
                contour.points.append(Point(round(end[0]), round(end[1]), "curve"))
        if len(contour.points) >= 2:
            glyph.contours.append(contour)


def build(out: Path) -> Path:
    polys = outlines()
    k = scale_for(polys)
    advance = round(Y.EM * k)
    dy = CENTRE - Y.EM / 2 * k
    # down a column every glyph takes one em, its square centred in it, so N characters are N em
    origin = round(CENTRE + UPM / 2)

    font = ufoLib2.Font()
    info = font.info
    info.familyName = FAMILY
    info.styleName = "Regular"
    info.styleMapFamilyName = FAMILY
    info.styleMapStyleName = "regular"
    info.copyright = 'Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>'
    info.unitsPerEm = 1000
    info.ascender, info.descender = ASCENT, DESCENT
    info.openTypeHheaAscender, info.openTypeHheaDescender, info.openTypeHheaLineGap = ASCENT, DESCENT, LINE_GAP
    info.openTypeOS2TypoAscender, info.openTypeOS2TypoDescender, info.openTypeOS2TypoLineGap = ASCENT, DESCENT, LINE_GAP
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
        "Teng Chou, the Celestial Record: the characters of Tantsou and Jenchai in thalorna, "
        "with the Jurthati syllabary, in a brushed regular script."
    )
    info.openTypeNameLicense = "SIL Open Font License 1.1"
    info.openTypeNameLicenseURL = "https://openfontlicense.org"
    info.openTypeNameUniqueID = "TengChou-Regular;0.1"
    info.openTypeNameVersion = "Version 0.1"
    info.versionMajor, info.versionMinor = 0, 100
    info.postscriptFontName = "TengChou-Regular"
    info.postscriptUnderlinePosition = -80
    info.postscriptUnderlineThickness = 36
    # a column: each glyph's vertical advance is the square, centred on the column's axis
    info.openTypeVheaVertTypoAscender = UPM // 2
    info.openTypeVheaVertTypoDescender = -(UPM - UPM // 2)
    info.openTypeVheaVertTypoLineGap = 0

    zethu = ufoLib2.Font.open(ROOT / "sources" / "KhelathiZethuGlyphs.ufo")
    order = [".notdef", notdef_box.BOX, "space", "ignorable", "ignorable.sub"]
    for name in (".notdef", notdef_box.BOX):
        g = font.newGlyph(name)
        src = zethu[name]
        g.width = src.width
        for c in src.contours:
            g.contours.append(Contour([Point(p.x, p.y, p.segmentType) for p in c.points]))
    font[notdef_box.BOX].unicodes = notdef_box.codepoints()
    font.newGlyph("space").width = SPACE
    font["space"].unicodes = [0x20, 0xA0]
    for name in ("ignorable", "ignorable.sub"):
        font.newGlyph(name).width = 0
    font["ignorable"].unicodes = [*range(0x200B, 0x2010), *range(0x202A, 0x202F), *range(0x2066, 0x206A), 0xFEFF]
    # the box takes no code point that the space or the ignorables draw
    taken = set(font["space"].unicodes) | set(font["ignorable"].unicodes)
    font[notdef_box.BOX].unicodes = [c for c in font[notdef_box.BOX].unicodes if c not in taken]

    rows = codepoint_order.ltr_table("TengChou-Regular")
    for row in rows:
        name = row["glyph"]
        g = font.newGlyph(name)
        xs = [x for p in polys[name] for x, _ in p]
        dx = SIDEBEARING - min(xs) * k
        draw(g, polys[name], k, dy, dx)
        b = g.getBounds(font)
        shift = SIDEBEARING - b.xMin  # rounding moves the ink by a unit at most
        if shift:
            g.move((shift, 0))
        g.width = round(b.xMax - b.xMin) + 2 * SIDEBEARING
        g.height = UPM
        g.lib["public.verticalOrigin"] = origin
        g.unicodes = [int(row["codepoint"][2:], 16)]
        order.append(name)
    for name in (".notdef", notdef_box.BOX, "space", "ignorable", "ignorable.sub"):
        font[name].height = UPM
        font[name].lib["public.verticalOrigin"] = origin

    heights = []
    for row in rows:
        if row["glyph"].startswith("tc."):
            b = font[row["glyph"]].getBounds(font)
            heights.append(b.yMax - b.yMin)
    info.capHeight = info.xHeight = round(statistics.median(heights))
    font.lib["public.glyphOrder"] = order
    font.features.text = FEATURES

    if out.exists():
        shutil.rmtree(out)
    font.save(out)
    return out


def write_names(path: Path = ROOT / "tools" / "names" / "tengchou.json") -> Path:
    """The character names: ``TENG CHOU CHARACTER <MORPHEME>``, ``TENG CHOU TALLY ONE`` to
    ``FIVE`` for the stages of the tally, and, for a sign of the Jurthati syllabary,
    ``TENG CHOU SYLLABLE <SYLLABLE>``."""
    names = {}
    for row in codepoint_order.ltr_table("TengChou-Regular"):
        kind, _, value = row["glyph"].partition(".")
        stage = next((s for s in T.STAGES.values() if s.glyph == row["glyph"]), None)
        if stage:
            names[row["codepoint"]] = stage.name
            continue
        label = "CHARACTER" if kind == "tc" else "SYLLABLE"
        names[row["codepoint"]] = f"TENG CHOU {label} {value.upper()}"
    path.write_text(json.dumps(names, indent=4, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default=str(ROOT / "sources" / "TengChou.ufo"))
    a = ap.parse_args()
    print(build(Path(a.out)))
    print(write_names())


if __name__ == "__main__":
    main()
