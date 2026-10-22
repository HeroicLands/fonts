# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Write sources/HelonikaBook.ufo from the Helónika signs.

    .venv/bin/python tools/helonika/build_ufo.py [--out sources/HelonikaBook.ufo]

Every character of ``encoding.json`` is drawn on its code point by ``letters.py``:
the capitals in the book reed (``strokes.REED``), the minuscules, the points and
the accent in the lighter minuscule reed (``strokes.REED_MIN``), and the digits in
the capitals' reed. The outlines are fitted with cubic curves by Teng Chou's
``fit.py``. The UFO is generated: an edit belongs in the strokes or the letters,
and this script is run after it, before ``build.sh`` compiles the UFO. The
character names, ``tools/names/helonika.json``, are written beside it.

**Spacing.** Every glyph's advance is its ink and ``strokes.BEARING`` either side, except
the raised dot, whose advance is a space plus its ink, centred;
the accent has no advance.

**The features.** ``ccmp`` empties the default-ignorables. ``rclt`` draws the
accent as the box wherever it follows a glyph that is not a vowel; standing first
in a run, with nothing before it, it is drawn as itself. ``mark`` sets the accent
over the middle of the vowel before it: over a minuscule as it is drawn, and over a
capital raised by the difference between the cap height and the body, and over a
long vowel raised again, clear of the length bar.

**Metrics.** The letters are drawn at the font's size: the minuscule body is the
shared x-height and the capitals stand at the shared cap height. The line metrics
are the shared ones; the ``OS/2`` Windows ascent and descent grow to hold any ink
past them. The notdef and its box are Khelathi Zethu Glyphs', and the box takes
every Latin and punctuation code point (``tools/notdef_box.py``).
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
import statistics
import sys
from pathlib import Path

import ufoLib2
from ufoLib2.objects.contour import Contour
from ufoLib2.objects.point import Point

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
sys.path.insert(1, str(HERE.parent))
import letters as L  # noqa: E402
import notdef_box  # noqa: E402
import strokes as S  # noqa: E402

_spec = importlib.util.spec_from_file_location("teng_chou_fit", HERE.parent / "teng-chou" / "fit.py")
fit = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(fit)

FAMILY = "Helonika Book"
STEM = "HelonikaBook"
ENCODING = HERE / "encoding.json"
ASCENT, DESCENT, LINE_GAP = 945, -200, 100
WIN_ASCENT, WIN_DESCENT = 945, 250
FIT_SLACK = 12  # how far a fitted curve may run outside its polygon's box
X_TYPICAL = "b e e.long o s u".split()  # minuscules that stand on the body, line to x-height, with no tail
CAP_TYPICAL = "A B E F G H I J K M N P R S T".split()  # capitals with no round to overshoot
VOWELS = "A E E.long I O O.long U A.macron I.macron U.macron".split()
VOWELS += [v.lower() for v in VOWELS]
ACCENT_RISE = round(S.CAP - S.X)  # how much higher the accent stands over a capital
LENGTH_CLEAR = 70  # how much higher again it stands over a long vowel, above the length bar

FEATURE_HEAD = """languagesystem DFLT dflt;

# HarfBuzz replaces a default-ignorable character the font maps directly with
# the space glyph. A glyph that a lookup substitutes is left alone, so each
# ignorable is substituted once, to a second empty glyph.
feature ccmp {
  sub ignorable by ignorable.sub;
} ccmp;
"""


def encoding() -> dict:
    return json.loads(ENCODING.read_text(encoding="utf-8"))


def reed_for(name: str) -> S.Reed:
    """The capitals and the digits are written with the book reed; the minuscules, the
    points and the accent with the lighter minuscule reed."""
    return S.REED_MIN if name in L.MIN or name in L.POINTS else S.REED


def draw(glyph, polys):
    """Fit each polygon with cubic curves, wound as a UFO wants (outer counter-clockwise,
    holes clockwise); where a fitted curve runs outside the polygon's own box, the
    polygon is kept as straight lines."""
    polys = [p for p in (fit._dedupe(list(map(tuple, q))) for q in polys) if len(p) >= 3 and abs(fit._area(p)) > 4]
    for i, poly in enumerate(polys):
        depth = sum(1 for j, other in enumerate(polys) if j != i and fit._inside(poly[0], other))
        if (fit._area(poly) > 0) != (depth % 2 == 0):
            poly = poly[::-1]
        start, segs = fit._fit_contour(poly)
        x0, x1 = min(x for x, _ in poly) - FIT_SLACK, max(x for x, _ in poly) + FIT_SLACK
        y0, y1 = min(y for _, y in poly) - FIT_SLACK, max(y for _, y in poly) + FIT_SLACK
        if all(x0 <= x <= x1 and y0 <= y <= y1 for x, y in _curve_points(start, segs)):
            contour = Contour()
            for seg in segs:
                if seg[0] == "line":
                    contour.points.append(Point(round(seg[1][0]), round(seg[1][1]), "line"))
                else:
                    _, c1, c2, end = seg
                    contour.points.append(Point(round(c1[0]), round(c1[1])))
                    contour.points.append(Point(round(c2[0]), round(c2[1])))
                    contour.points.append(Point(round(end[0]), round(end[1]), "curve"))
        else:
            contour = Contour([Point(round(x), round(y), "line") for x, y in poly])
        if len(contour.points) >= 2:
            glyph.contours.append(contour)


def _curve_points(start, segs, steps=8):
    out, p0 = [], start
    for seg in segs:
        if seg[0] == "line":
            p0 = seg[1]
            out.append(p0)
            continue
        _, c1, c2, end = seg
        for i in range(1, steps + 1):
            u = i / steps
            a, b, c, d = (1 - u) ** 3, 3 * u * (1 - u) ** 2, 3 * u * u * (1 - u), u ** 3
            out.append((a * p0[0] + b * c1[0] + c * c2[0] + d * end[0], a * p0[1] + b * c1[1] + c * c2[1] + d * end[1]))
        p0 = end
    return out


DOT_INK = 82  # the raised dot's drawn width, which its advance adds to the space


def polygons(name: str):
    """The sign's outline as polygons, moved so its left ink stands at the bearing; and
    the middle of its ink, after the move."""
    path = S.outline(L.tracks(name), reed_for(name))
    polys = S.contours(path)
    xs = [x for p in polys for x, _ in p]
    lo, hi = min(xs), max(xs)
    if name == "accent":
        mid = (lo + hi) / 2
        return [[(x - mid, y) for x, y in p] for p in polys], 0.0, 0
    if name == "raisedDot":
        # The dot stands where the space after a sentence stood: its advance is a
        # space plus its ink, the ink centred.
        width = round(S.SPACE + DOT_INK)
        dx = width / 2 - (lo + hi) / 2
        return [[(x + dx, y) for x, y in p] for p in polys], (lo + hi) / 2 + dx, width
    dx = S.BEARING - lo
    return [[(x + dx, y) for x, y in p] for p in polys], (lo + hi) / 2 + dx, round(hi - lo + 2 * S.BEARING)


def compiled_extent(font) -> tuple[int, int]:
    """The highest and lowest point of the glyph boxes, as fontmake compiles them."""
    import ufo2ft

    tt = ufo2ft.compileTTF(font, removeOverlaps=False, useProductionNames=False)
    glyf = tt["glyf"]
    boxes = [glyf[n] for n in tt.getGlyphOrder() if glyf[n].numberOfContours]
    return max(g.yMax for g in boxes), min(g.yMin for g in boxes)


def build(out: Path) -> Path:
    enc = encoding()

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
    info.openTypeOS2Selection = [7]
    info.openTypeOS2Type = []
    info.openTypeOS2UnicodeRanges = []
    info.openTypeOS2CodePageRanges = []
    info.openTypeOS2VendorID = "HRLD"
    info.openTypeHeadCreated = "2026/01/01 00:00:00"
    info.openTypeHeadFlags = [0, 3]
    info.openTypeHeadLowestRecPPEM = 3
    info.openTypeNameDescription = (
        "Helonika Book, the book hand of the Helónika in thalorna: upright geometric capitals over a round "
        "broad-pen minuscule, written left to right with a flat reed."
    )
    info.openTypeNameLicense = "SIL Open Font License 1.1"
    info.openTypeNameLicenseURL = "https://openfontlicense.org"
    info.openTypeNameUniqueID = f"{STEM}-Regular;0.1"
    info.openTypeNameVersion = "Version 0.1"
    info.versionMajor, info.versionMinor = 0, 100
    info.postscriptFontName = f"{STEM}-Regular"
    info.postscriptUnderlinePosition = -100
    info.postscriptUnderlineThickness = 40

    zethu = ufoLib2.Font.open(ROOT / "sources" / "KhelathiZethuGlyphs.ufo")
    order = [".notdef", notdef_box.BOX, "space", "ignorable", "ignorable.sub"]
    for name in (".notdef", notdef_box.BOX):
        g = font.newGlyph(name)
        src = zethu[name]
        g.width = src.width
        for c in src.contours:
            g.contours.append(Contour([Point(p.x, p.y, p.segmentType) for p in c.points]))
    font.newGlyph("space").width = S.SPACE
    font["space"].unicodes = [0x20, 0xA0]
    for name in ("ignorable", "ignorable.sub"):
        font.newGlyph(name).width = 0
    font["ignorable"].unicodes = [int(c[2:], 16) for c in enc["ignorables"]["codepoints"]]
    taken = set(font["space"].unicodes) | set(font["ignorable"].unicodes)
    font[notdef_box.BOX].unicodes = [c for c in notdef_box.codepoints() if c not in taken]
    categories = {name: "base" for name in (".notdef", notdef_box.BOX)}

    middles = {}
    for r in enc["glyphs"]:
        name = r["glyph"]
        polys, mid, width = polygons(name)
        g = font.newGlyph(name)
        draw(g, polys)
        g.width = width
        g.unicodes = [int(r["codepoint"][2:], 16)]
        categories[name] = "mark" if r["kind"] == "mark" else "base"
        middles[name] = mid
        order.append(name)

    def median_height(names):
        hs = []
        for n in names:
            b = font[n].getBounds(font)
            hs.append(b.yMax - b.yMin)
        return round(statistics.median(hs))

    info.xHeight = median_height(X_TYPICAL)
    info.capHeight = median_height(CAP_TYPICAL)
    font.lib["public.glyphOrder"] = order
    font.lib["public.openTypeCategories"] = dict(sorted(categories.items()))
    font.features.text = features(enc, middles)
    top, bottom = compiled_extent(font)
    info.openTypeOS2WinAscent = max(WIN_ASCENT, top)
    info.openTypeOS2WinDescent = max(WIN_DESCENT, -bottom)

    if out.exists():
        shutil.rmtree(out)
    font.save(out)
    return out


def features(enc: dict, middles: dict) -> str:
    """The accent's features: a stray accent is the box, and an accent after a vowel
    stands over its middle."""
    names = [r["glyph"] for r in enc["glyphs"] if r["kind"] != "mark"]
    others = [n for n in names if n not in VOWELS]
    lines = [
        FEATURE_HEAD,
        f"@VOWEL = [{' '.join(VOWELS)}];",
        f"@OTHER = [space {' '.join(others)} accent notdef.box];",
        "",
        "lookup strays {",
        "  ignore sub @VOWEL accent';",
        "  sub @OTHER accent' by notdef.box;",
        "} strays;",
        "",
        "feature rclt {",
        "  lookup strays;",
        "} rclt;",
        "",
        "markClass accent <anchor 0 0> @TOP;",
        "",
        "feature mark {",
    ]
    for v in VOWELS:
        rise = (ACCENT_RISE if v[0].isupper() else 0) + (LENGTH_CLEAR if v.endswith(".macron") else 0)
        lines.append(f"  pos base {v} <anchor {round(middles[v])} {rise}> mark @TOP;")
    lines += ["} mark;", ""]
    return "\n".join(lines)


def write_names(path: Path = ROOT / "tools" / "names" / "helonika.json") -> Path:
    """The character names, in Unicode's style: ``HELONIKA CAPITAL LETTER A``,
    ``HELONIKA SMALL LETTER LONG E``, ``HELONIKA SMALL LETTER TH``, ``HELONIKA SMALL
    LETTER A WITH LENGTH BAR``, ``HELONIKA DIGIT ZERO``, ``HELONIKA RAISED DOT``,
    ``HELONIKA REGISTER MARK`` and ``HELONIKA COMBINING ACCENT``."""
    digits = "ZERO ONE TWO THREE FOUR FIVE SIX SEVEN EIGHT NINE".split()
    names = {}
    for r in encoding()["glyphs"]:
        kind, g = r["kind"], r["glyph"]
        if kind in ("capital", "small"):
            case = "CAPITAL" if kind == "capital" else "SMALL"
            base = g.split(".")[0].upper()
            if g.endswith(".long"):
                letter = f"LONG {base}"
            elif g.endswith(".macron"):
                letter = f"{base} WITH LENGTH BAR"
            else:
                letter = base
            label = f"{case} LETTER {letter}"
        elif kind == "digit":
            label = f"DIGIT {digits[int(r['spelling'])]}"
        else:
            label = {"raisedDot": "RAISED DOT", "registerMark": "REGISTER MARK", "accent": "COMBINING ACCENT"}[g]
        names[r["codepoint"]] = f"HELONIKA {label}"
    path.write_text(json.dumps(names, indent=4, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default=str(ROOT / "sources" / f"{STEM}.ufo"))
    a = ap.parse_args()
    print(build(Path(a.out)))
    print(write_names())


if __name__ == "__main__":
    main()
