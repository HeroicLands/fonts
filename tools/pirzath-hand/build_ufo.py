# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Write sources/PirzathHand.ufo from the Pirzath Hand signs.

    .venv/bin/python tools/pirzath-hand/build_ufo.py [--out sources/PirzathHand.ufo]

Every character the hand draws, on the code points ``fonts.json`` gives it in the
Pirzath block, is drawn by ``letters.py`` from the strokes of ``strokes.py``, and so
are the long vowels and the doubled consonants, which have no code point of their
own. The outlines are fitted with cubic curves by Teng Chou's ``fit.py``. The UFO is
generated: an edit belongs in the strokes or the letters, and this script is run
after it, before ``build.sh`` compiles the UFO.

**One printed face.** Every sign stands apart: its advance is its ink and
``letters.SB`` either side, and the word space is ``letters.WORD``. The length mark
has no advance. There are no joined forms and no kerning.

**The features.** ``ccmp`` empties the default-ignorables. ``liga`` draws a vowel
and the length mark after it as the long vowel, the vowel with the length bar over
it. ``rlig`` draws a consonant written twice as its doubled sign. ``mark`` sets a
length mark left on a vowel pair over the middle of the pair.

**Metrics.** The signs are drawn at the font's size: a consonant's body stands at
the shared cap height, 0.73 em. The line metrics are the shared ones, with
USE_TYPO_METRICS; the ``OS/2`` Windows ascent and descent grow to hold any ink past
them. ``.notdef`` is the hand's plain cross, and the box, ``notdef.box``, is a copy of
it that takes every Latin and punctuation code point (``tools/notdef_box.py``).
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

FAMILY = "Pirzath Hand"
STEM = "PirzathHand"
CLASS = "hl-pirzath-hand"
VERSION = (0, 300, "Version 0.3")
ASCENT, DESCENT, LINE_GAP = 945, -200, 100
WIN_ASCENT, WIN_DESCENT = 945, 250
FIT_SLACK = 12  # how far a fitted curve may run outside its polygon's box
X_TYPICAL = "a e i u".split()  # vowels that stand from the line to the vowel height
CAP_TYPICAL = "p b f v t d k g m n s sh z zh r ts ch q".split()  # consonants from the line to the body
VOWEL_NAMES = "a e i o u".split()
PAIRS = "ai au ei oi ou".split()
LENGTH_CLEAR = {"oi": 40}  # how much higher the length mark stands over a pair whose ink reaches up to it

# The font's glyph names for the signs of letters.py that differ from them.
LONG = {f"{v}.long": f"{v}acute" for v in VOWEL_NAMES}

FEATURE_HEAD = """languagesystem DFLT dflt;
languagesystem latn dflt;

# HarfBuzz replaces a default-ignorable character the font maps directly with
# the space glyph. A glyph that a lookup substitutes is left alone, so each
# ignorable is substituted once, to a second empty glyph.
feature ccmp {
  sub ignorable by ignorable.sub;
} ccmp;
"""


def font_name(sign: str) -> str:
    """The font's glyph name for a sign of letters.py."""
    if sign in LONG:
        return LONG[sign]
    if sign.endswith(".double"):
        base = sign[: -len(".double")]
        return f"{base}_{base}"
    return sign


def encoding() -> dict[str, int]:
    """Glyph name to code point, as fonts.json lists the hand's characters."""
    doc = json.loads((ROOT / "fonts.json").read_text(encoding="utf-8"))
    fam = next(f for f in doc["families"] if f["class"] == CLASS)
    return {c["glyph"]: int(c["codepoint"][2:], 16) for c in fam["codepoints"]}


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


def polygons(sign: str):
    """The sign's outline as polygons, with its ink starting ``SB`` in; its advance; and
    the middle of its ink. The length mark is centred on its origin, with no advance."""
    tracks, advance = L.draw(sign)
    polys = S.contours(S.outline(tracks))
    xs = [x for p in polys for x, _ in p]
    mid = (min(xs) + max(xs)) / 2
    if sign == "lengthmark":
        return [[(x - mid, y) for x, y in p] for p in polys], 0, 0.0
    return polys, round(advance), mid


def compiled_extent(font) -> tuple[int, int]:
    """The highest and lowest point of the glyph boxes, as fontmake compiles them."""
    import ufo2ft

    tt = ufo2ft.compileTTF(font, removeOverlaps=False, useProductionNames=False)
    glyf = tt["glyf"]
    boxes = [glyf[n] for n in tt.getGlyphOrder() if glyf[n].numberOfContours]
    return max(g.yMax for g in boxes), min(g.yMin for g in boxes)


def signs() -> list[str]:
    """Every sign the font draws, in glyph order: the encoded characters as letters.py
    builds them, then the long vowels and the doubled consonants."""
    enc = encoding()
    out = [s for s in L.SIGNS if font_name(s) in enc]
    missing = sorted(set(enc) - {font_name(s) for s in out})
    if missing:
        raise SystemExit(f"tools/pirzath-hand/letters.py: error: no sign for {', '.join(missing)}")
    return out + list(L.LONG) + list(L.DOUBLED)


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
        "Pirzath Hand, the everyday printed hand of Pirzath, the script of the Khazari of thalorna: plain "
        "separate letters in an even stroke, written left to right with chalk or a carpenter's pencil."
    )
    info.openTypeNameLicense = "SIL Open Font License 1.1"
    info.openTypeNameLicenseURL = "https://openfontlicense.org"
    info.openTypeNameUniqueID = f"{STEM}-Regular;0.3"
    info.versionMajor, info.versionMinor, info.openTypeNameVersion = VERSION
    info.postscriptFontName = f"{STEM}-Regular"
    info.postscriptUnderlinePosition = -100
    info.postscriptUnderlineThickness = 40

    order = [".notdef", notdef_box.BOX, "space", "ignorable", "ignorable.sub"]
    polys, width, _ = polygons(".notdef")
    for name in (".notdef", notdef_box.BOX):
        g = font.newGlyph(name)
        draw(g, polys)
        g.width = width
    font.newGlyph("space").width = round(L.WORD)
    font["space"].unicodes = [0x20, 0xA0]
    for name in ("ignorable", "ignorable.sub"):
        font.newGlyph(name).width = 0
    font["ignorable"].unicodes = [*range(0x200B, 0x2010), *range(0x202A, 0x202F), *range(0x2066, 0x206A), 0xFEFF]
    taken = set(font["space"].unicodes) | set(font["ignorable"].unicodes)
    font[notdef_box.BOX].unicodes = [c for c in notdef_box.codepoints() if c not in taken]
    categories = {name: "base" for name in (".notdef", notdef_box.BOX)}

    middles = {}
    for sign in signs():
        if sign == ".notdef":
            continue
        name = font_name(sign)
        polys, width, mid = polygons(sign)
        g = font.newGlyph(name)
        draw(g, polys)
        g.width = width
        if name in enc:
            g.unicodes = [enc[name]]
        categories[name] = "mark" if name == "lengthmark" else "base"
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
    font.features.text = features(middles)
    top, bottom = compiled_extent(font)
    info.openTypeOS2WinAscent = max(WIN_ASCENT, top)
    info.openTypeOS2WinDescent = max(WIN_DESCENT, -bottom)

    if out.exists():
        shutil.rmtree(out)
    font.save(out)
    return out


def features(middles: dict) -> str:
    """The long vowels, the doubled consonants and the length mark over a pair."""
    lines = [
        FEATURE_HEAD,
        "# A vowel and the length mark after it are drawn as the long vowel.",
        "feature liga {",
    ]
    lines += [f"  sub {v} lengthmark by {v}acute;" for v in VOWEL_NAMES]
    lines += ["} liga;", "", "# A consonant written twice is the doubled sign.", "feature rlig {"]
    for sign in L.CONSONANTS:
        lines.append(f"  sub {sign} {sign} by {sign}_{sign};")
    lines += [
        "} rlig;",
        "",
        "markClass lengthmark <anchor 0 0> @LEN;",
        "",
        "# A length mark left on a vowel pair stands over the middle of the pair.",
        "feature mark {",
    ]
    for p in PAIRS:
        lines.append(f"  pos base {p} <anchor {round(middles[p])} {LENGTH_CLEAR.get(p, 0)}> mark @LEN;")
    lines += ["} mark;", ""]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default=str(ROOT / "sources" / f"{STEM}.ufo"))
    a = ap.parse_args()
    print(build(Path(a.out)))


if __name__ == "__main__":
    main()
