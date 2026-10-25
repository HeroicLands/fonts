# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Write ``sources/ChalishPilamCeremonial.ufo`` from the glyphs of the ceremonial hand.

    .venv/bin/python tools/chalish-pilam/build_ceremonial_ufo.py [--out sources/ChalishPilamCeremonial.ufo]

**The encoding.** ``tools/chalish-pilam/ceremonial_encoding.json`` is the one table of
code points. The numbers sit at U+F4000: zero, 1 to 19, then the places of the count,
20, 400, 8,000 and 160,000. The concept glyphs follow from U+F4020, in the order of
``blocks.MAINS``, the syllable signs from U+F4400 in the order of ``syllabary.SIGNS``,
and the two joiners sit at U+F4FF0 (``*``) and U+F4FF1 (``:``). This script appends a
glyph it does not find in the table and never moves one it does. A glyph removed from
the drawing modules keeps its row, marked ``retired``, so its code point is never
reused. Zero and the places have no ceremonial drawing: their rows are marked
``pending`` and their code points print the box.

**The layout.** ``ceremonial_layout.py`` generates every item already placed for each
layout a block can take, and the feature file that chooses among them. Outlines are
drawn at ``ceremonial.FONT_SCALE`` and shifted down by ``ceremonial.FONT_DROP`` so a
block spans descender to ascender. Every variant is drawn from the block's left edge,
inside a gutter of ``GUTTER`` units on each side of the block.
"""

import argparse
import json
import math
import shutil
import statistics
import sys
from pathlib import Path

import ufoLib2
from fontTools.pens.pointPen import SegmentToPointPen
from fontTools.pens.transformPen import TransformPen
from ufoLib2.objects import Contour, Point

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "tools"))
import blocks as Q  # noqa: E402
import ceremonial as R  # noqa: E402
import ceremonial_layout as L  # noqa: E402
import notdef_box  # noqa: E402
import strokes as S  # noqa: E402

FAMILY = "Chalish Pilam Ceremonial"
STEM = "ChalishPilamCeremonial"
ENCODING = HERE / "ceremonial_encoding.json"
NUMBERS = 0xF4000
CONCEPTS = 0xF4020
CONCEPTS_END = 0xF43FF
SYLLABLES = 0xF4400
SYLLABLES_END = 0xF4FEF
JOINER_CODEPOINTS = {"*": 0xF4FF0, ":": 0xF4FF1}
IGNORABLES = [*range(0x200B, 0x2010), *range(0x202A, 0x202F), *range(0x2066, 0x206A), 0xFEFF]
EMPTY = {"space", "ignorable", "ignorable.sub", *L.JOINERS.values()}


def current_rows() -> list[dict]:
    """Every glyph the drawing modules define, in code order, with its row data."""
    rows = []
    for v in L.NUMBER_VALUES:
        row = {"glyph": f"n{v}", "code": f"n{v}", "kind": "number", "concept": f"{v:,}"}
        if v not in L.DRAWN_NUMBERS:
            row["pending"] = True
        rows.append(row)
    for code, g in Q.MAINS.items():
        rows.append({"glyph": L.base_name(code), "code": code, "kind": "concept", "concept": g.meaning,
                     "footprint": g.footprint})
    for code, sign in Q.SIGNS.items():
        rows.append({"glyph": code, "code": code, "kind": "syllable", "syllable": sign.syllable,
                     "source": sign.source})
    for joiner, name in L.JOINERS.items():
        rows.append({"glyph": name, "code": joiner, "kind": "joiner"})
    return rows


def encoding() -> list[dict]:
    """The encoding table, with any glyph not yet in it appended."""
    stored = json.loads(ENCODING.read_text())["glyphs"] if ENCODING.exists() else []
    by_glyph = {r["glyph"]: r for r in stored}
    used = {int(r["codepoint"][2:], 16) for r in stored}
    rows = list(stored)
    current = set()
    for new in current_rows():
        name = new["glyph"]
        current.add(name)
        if name not in by_glyph:
            if new["kind"] == "number":
                cp = NUMBERS + L.NUMBER_VALUES.index(int(name[1:]))
            elif new["kind"] == "joiner":
                cp = JOINER_CODEPOINTS[new["code"]]
            else:
                lo, hi = (CONCEPTS, CONCEPTS_END) if new["kind"] == "concept" else (SYLLABLES, SYLLABLES_END)
                taken = [u for u in used if lo <= u <= hi]
                cp = max(taken) + 1 if taken else lo
                if cp > hi:
                    raise SystemExit(f"{ENCODING.name}: error: no code point left for {name}")
            if cp in used:
                raise SystemExit(f"{ENCODING.name}: error: U+{cp:05X} is taken, so {name} cannot sit there")
            used.add(cp)
            row = {"glyph": name, "codepoint": f"U+{cp:05X}"}
            rows.append(row)
            by_glyph[name] = row
        row = by_glyph[name]
        for key in ("pending", "footprint", "concept", "syllable", "source"):
            row.pop(key, None)
        row.update(new)
        row.pop("retired", None)
    for row in rows:
        if row["glyph"] not in current:
            row["retired"] = True
    rows.sort(key=lambda r: int(r["codepoint"][2:], 16))
    ENCODING.write_text(json.dumps({"glyphs": rows}, indent=2, ensure_ascii=False) + "\n")
    return rows


def draw(glyph, path):
    """Draw a pathops path into a UFO glyph at font scale, shifted right by the gutter and down by the drop."""
    pen = SegmentToPointPen(glyph.getPointPen())
    path.draw(TransformPen(pen, (L.SCALE, 0, 0, L.SCALE, L.GUTTER, L.DROP)))


def new_font() -> ufoLib2.Font:
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
    info.openTypeOS2Selection = [7]
    info.openTypeOS2Type = []
    info.openTypeOS2UnicodeRanges = []
    info.openTypeOS2CodePageRanges = []
    info.openTypeOS2VendorID = "HRLD"
    info.openTypeHeadCreated = "2026/01/01 00:00:00"
    info.openTypeHeadFlags = [0, 3]
    info.openTypeHeadLowestRecPPEM = 3
    info.openTypeNameDescription = (
        "Chalish Pilam Ceremonial, the ceremonial hand of the Ki'ich'chik writing in thalorna: carved blocks, "
        "each a main sign with at most two affixes, laid out by the font from the codage's joiners."
    )
    info.openTypeNameLicense = "SIL Open Font License 1.1"
    info.openTypeNameLicenseURL = "https://openfontlicense.org"
    info.openTypeNameUniqueID = f"{STEM}-Regular;0.1"
    info.openTypeNameVersion = "Version 0.1"
    info.versionMajor, info.versionMinor = 0, 100
    info.postscriptFontName = f"{STEM}-Regular"
    info.postscriptUnderlinePosition = -100
    info.postscriptUnderlineThickness = 40
    return font


def add_glyph(font, order, name, path, advance, unicodes=()):
    g = font.newGlyph(name)
    if path is not None and list(path):
        draw(g, path)
    g.width = advance
    g.unicodes = list(unicodes)
    order.append(name)
    return g




def build(out: Path) -> Path:
    rows = [r for r in encoding() if not r.get("retired")]
    font = new_font()

    zethu = ufoLib2.Font.open(ROOT / "sources" / "KhelathiZethuGlyphs.ufo")
    order = [".notdef", notdef_box.BOX, "space", "ignorable", "ignorable.sub"]
    for name in (".notdef", notdef_box.BOX):
        g = font.newGlyph(name)
        src = zethu[name]
        g.width = src.width
        for c in src.contours:
            g.contours.append(Contour([Point(p.x, p.y, p.segmentType) for p in c.points]))
    full = L.block_advance("full")
    font.newGlyph("space").width = full
    font["space"].unicodes = [0x20, 0xA0]
    for name in ("ignorable", "ignorable.sub"):
        font.newGlyph(name).width = 0
    font["ignorable"].unicodes = IGNORABLES
    taken = set(font["space"].unicodes) | set(IGNORABLES)
    pending = [int(r["codepoint"][2:], 16) for r in rows if r.get("pending")]
    font[notdef_box.BOX].unicodes = [c for c in notdef_box.codepoints() if c not in taken] + pending

    for r in rows:
        if r["kind"] == "joiner":
            add_glyph(font, order, r["glyph"], None, 0, [int(r["codepoint"][2:], 16)])
    for r in rows:
        if r["kind"] == "joiner" or r.get("pending"):
            continue
        code = r["code"]
        cp = int(r["codepoint"][2:], 16)
        path = R.ink(L.plain_parts(code), L.INK_SEED)
        add_glyph(font, order, r["glyph"], path, L.block_advance(L.footprint_of(code)), [cp])

    for role in L.ROLES:
        for code in L.role_codes(role):
            path = R.ink(L.parts_of(role, code), L.INK_SEED)
            add_glyph(font, order, L.variant_name(code, role.suffix), path, L.role_advance(role, code))

    top = bottom = 0.0
    for g in font:
        b = g.getBounds(font)
        if b is not None:
            top, bottom = max(top, b[3]), min(bottom, b[1])
    info = font.info
    # The script has one height: the median of the concept glyphs that fill a full block,
    # most of them standing in its cushion.
    typical = [r["glyph"] for r in rows if r["kind"] == "concept" and r.get("footprint") == "full"]
    info.capHeight = info.xHeight = round(statistics.median(
        font[n].getBounds(font).yMax - font[n].getBounds(font).yMin for n in typical))
    info.openTypeOS2WinAscent = max(945, math.ceil(top))
    info.openTypeOS2WinDescent = max(250, math.ceil(-bottom))

    font.lib["public.glyphOrder"] = order
    font.lib["public.openTypeCategories"] = {n: "base" for n in order if n not in EMPTY}
    font.features.text = L.features()
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
