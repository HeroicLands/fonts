# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Write sources/VedyaksharaClassical.ufo from the Vedyakshara signs.

    .venv/bin/python tools/vedyakshara/build_ufo.py [--out sources/VedyaksharaClassical.ufo]

Every character of ``encoding.json`` is drawn on its code point by ``letters.py``
in the one reed (``strokes.HAND``): the consonants, the independent vowels, the
vowel signs, the cut, the soft dot, the digits and the two bars. The forms the
face draws from the characters around them have no code point: _fa_, the fused
signs (``encoding.json``'s ``fused``), the half and final form of every
consonant, of _fa_ and of every fused sign, the r-foot form of each of them that
can meet an _r_, and the vowel signs' placed parts. The outlines are fitted with cubic curves by Teng Chou's ``fit.py``. The
UFO is generated: an edit belongs in the strokes or the signs, and this script is
run after it, before ``build.sh`` compiles the UFO. The character names,
``tools/names/vedyakshara.json``, are written beside it.

**The features.** ``ccmp`` empties the default-ignorables. ``rclt``, which every
HarfBuzz shaper applies, draws the forms, in this order:

1. _pa_ and the soft dot become _fa_;
2. a consonant, the cut and a consonant that make one of the fused pairs become
   the fused sign, the leftmost pair first;
3. _ra_ with the cut becomes its half form before a consonant and its final form
   otherwise, so that an _r_ starting a cluster never takes the r-foot;
4. a sign, the cut and _ra_ become the sign's r-foot form;
5. a sign with the cut becomes its half form before a consonant,
6. and its final form anywhere else;
7. after a sign, _ai_ and _au_ become their two parts, and each hook takes the
   neck that reaches the lowest ink of the body above it;
8. a vowel sign, the cut or the soft dot after a glyph that cannot carry it is
   the box. Standing first in a run, with nothing before it, it is drawn as
   itself.

``mark`` places each flag and hook on the anchor of its sign: the _i_ flag over
the right end, the _e_ flag over the middle, the _u_ hook under the right and
the _o_ hook under the middle.

**Metrics.** The signs are drawn at the font's size, the body hanging from the
underside of the headline at the shared x-height. The digits stand on the line
exactly as tall as the body, and are the face's typical x-height letters. The
flags rise inside the shared ascent; the hooks, the r-foot and the r-stem reach
past the shared descent, and the ``OS/2`` Windows descent grows to hold them.
Every sign's headline runs over its whole advance, so the signs of a word meet in
one rope. The notdef and its box are Khelathi Zethu Glyphs', and the box takes
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

FAMILY = "Vedyakshara Classical"
STEM = "VedyaksharaClassical"
ENCODING = HERE / "encoding.json"
SPACE = 320  # the word space, in font units: the rope breaks
ASCENT, DESCENT, LINE_GAP = 945, -200, 100
WIN_ASCENT, WIN_DESCENT = 945, 250
CAPS = "ka ga ja ta da na pa ba ma ya ra la va sa ha".split()  # the plain signs, rope and all
FIT_SLACK = 12  # how far a fitted curve may run outside its polygon's box
NECK_STEP = 10  # a hook's neck is drawn to the nearest NECK_STEP units

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


# -- the glyph inventory -------------------------------------------------------------------------


def inventory(enc: dict):
    """The sign glyphs: (consonants, bases, fused C + r, r-foot bases). A consonant that
    fuses with _r_ never meets the r-foot, and neither does _ra_ or a fused C + r sign."""
    cons = [g["glyph"] for g in enc["glyphs"] if g["kind"] == "consonant"]
    fused = [f["glyph"] for f in enc["fused"]]
    bases = cons + ["fa"] + fused
    c_r = [f["glyph"] for f in enc["fused"] if f["parts"][1] == "ra"]
    rfoot = [b for b in bases if b != "ra" and b not in c_r and f"{b[:-1]}ra" not in c_r]
    return cons, bases, c_r, rfoot


def neck(y: float) -> int:
    return int(round(max(0.0, y) / NECK_STEP) * NECK_STEP)


# -- drawing -------------------------------------------------------------------------------------


def outline_polys(tracks) -> list:
    return S.contours(S.outline(tracks, S.HAND))


def _curve_points(start, segs, steps=8):
    """Points along a fitted contour, the curves sampled, to test where the ink runs."""
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


def draw(glyph, polys):
    """Fit each polygon with cubic curves, wound as a UFO wants (outer counter-clockwise,
    holes clockwise); where a fitted curve runs outside the polygon's own box, as it can
    at a sharp joint, the polygon is kept as straight lines."""
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


def hook(y: float, side: int = 1):
    """A back-vowel hook with its neck from ``y``, the lowest ink above it, its anchor at x 0."""
    return S.s_hook(0, y - 16, d=y - 16 - S.HOOK, side=side).tracks


def flag():
    return S.s_flag(0, 0).tracks


MARK_DRAWINGS = {
    "vs.i": lambda: flag(),
    "vs.e": lambda: flag(),
    "vs.ai": lambda: S.s_flag(-90, 0).tracks + S.s_flag(60, 0).tracks,
    "vs.u": lambda: hook(0),
    "vs.o": lambda: hook(0),
    "vs.au": lambda: [t for x in (-80, 80) for t in S.Shape(hook(0), (0, 0, 0), (0, 0, 0)).moved(x, 0).tracks],
    "cut": lambda: S.s_cut(0, 0).tracks,
    "dot": lambda: S.s_dot(0, 0.5 * S.X, size=1.2).tracks,
    "flag.i": lambda: flag(),
    "flag.e": lambda: flag(),
}


def placements(bases, rfoot):
    """Each base that carries vowel signs, with its anchors and the necks its hooks take:
    {glyph: (sign, anchors, neck under the right, neck under the middle)}."""
    out = {}
    for b in bases:
        for form in ("full", "rfoot"):
            if form == "rfoot" and b not in rfoot:
                continue
            g = L.sign(b, form=form)
            name = b if form == "full" else f"{b}.rfoot"
            right, mid = g.anchors["right"], g.anchors["mid"]
            out[name] = (g, {"right": round(right), "mid": round(mid), "emid": round(mid - 30)},
                         neck(L._bottom(g.tracks, right)), neck(L._bottom(g.tracks, mid)))
    return out


def compiled_extent(font) -> tuple[int, int]:
    """The highest and lowest point of the glyph boxes, as fontmake compiles them."""
    import ufo2ft

    tt = ufo2ft.compileTTF(font, removeOverlaps=False, useProductionNames=False)
    glyf = tt["glyf"]
    boxes = [glyf[n] for n in tt.getGlyphOrder() if glyf[n].numberOfContours]
    return max(g.yMax for g in boxes), min(g.yMin for g in boxes)


def build(out: Path) -> Path:
    enc = encoding()
    cons, bases, c_r, rfoot = inventory(enc)
    cps = {r["glyph"]: int(r["codepoint"][2:], 16) for r in enc["glyphs"]}

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
        "Vedyakshara Classical, the temple hand of the Vedyari syllabary in thalorna: every sign hangs from "
        "a headline, written left to right with a steep square-cut reed."
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
    font.newGlyph("space").width = SPACE
    font["space"].unicodes = [0x20, 0xA0]
    for name in ("ignorable", "ignorable.sub"):
        font.newGlyph(name).width = 0
    font["ignorable"].unicodes = [int(c[2:], 16) for c in enc["ignorables"]["codepoints"]]
    taken = set(font["space"].unicodes) | set(font["ignorable"].unicodes)
    font[notdef_box.BOX].unicodes = [c for c in notdef_box.codepoints() if c not in taken]
    categories = {}

    def put(name, glyph, category):
        g = font.newGlyph(name)
        draw(g, outline_polys(glyph.tracks))
        g.width = round(glyph.adv)
        if name in cps:
            g.unicodes = [cps[name]]
        categories[name] = category
        order.append(name)

    # the signs on their code points, then the forms with none
    for r in enc["glyphs"]:
        name, kind = r["glyph"], r["kind"]
        if kind in ("consonant", "vowel"):
            put(name, L.sign(name), "base")
        elif kind == "digit":
            put(name, L.digit(name.split(".")[1]), "base")
        elif kind == "point":
            put(name, L.point(1 if name == "pause" else 2), "base")
    for b in ["fa"] + [f["glyph"] for f in enc["fused"]]:
        put(b, L.sign(b), "base")
    for b in bases:
        put(f"{b}.half", L.sign(b, form="half"), "base")
        put(f"{b}.final", L.sign(b, form="final"), "base")
    for b in rfoot:
        put(f"{b}.rfoot", L.sign(b, form="rfoot"), "base")

    places = placements(bases, rfoot)
    necks = sorted({n for _, _, nr, nm in places.values() for n in (nr, nm)})
    marks = dict(MARK_DRAWINGS)
    for n in necks:
        marks[f"hook.u.{n}"] = lambda n=n: hook(n)
        marks[f"hook.o.{n}"] = lambda n=n: hook(n)
    for name, make in marks.items():
        put(name, L.Glyph(name, make(), 0), "mark")

    for name in (".notdef", notdef_box.BOX):
        categories[name] = "base"

    def median_height(names):
        hs = []
        for n in names:
            b = font[n].getBounds(font)
            hs.append(b.yMax - b.yMin)
        return round(statistics.median(hs))

    info.xHeight = median_height([f"num.{d}" for d in range(10)])
    info.capHeight = median_height(CAPS)
    font.lib["public.glyphOrder"] = order
    font.lib["public.openTypeCategories"] = dict(sorted(categories.items()))
    font.features.text = features(enc, places)
    top, bottom = compiled_extent(font)
    info.openTypeOS2WinAscent = max(WIN_ASCENT, top)
    info.openTypeOS2WinDescent = max(WIN_DESCENT, -bottom)

    if out.exists():
        shutil.rmtree(out)
    font.save(out)
    return out


# -- the features --------------------------------------------------------------------------------


def _cls(names) -> str:
    return "[" + " ".join(names) + "]"


def features(enc: dict, places: dict) -> str:
    cons, bases, c_r, rfoot = inventory(enc)
    fused = enc["fused"]
    signs = [g["glyph"] for g in enc["glyphs"] if g["kind"] == "vowel sign"]
    nxt = bases + [f"{b}.rfoot" for b in rfoot] + ["ra.half", "ra.final"]
    lines = [FEATURE_HEAD, f"@NEXT = {_cls(nxt)};", f"@VBASE = {_cls(places)};",
             f"@VSIGN = {_cls(signs)};", ""]
    lk = []
    lk += ["lookup softdot {", "  sub pa dot by fa;", "} softdot;", ""]
    lk += ["lookup fused {"] + [f"  sub {f['parts'][0]} cut {f['parts'][1]} by {f['glyph']};" for f in fused]
    lk += ["} fused;", ""]
    lk += ["lookup rhalf {", "  sub ra' cut' @NEXT by ra.half;", "} rhalf;", ""]
    lk += ["lookup rfinal {", "  sub ra cut by ra.final;", "} rfinal;", ""]
    lk += ["lookup rfoot {"] + [f"  sub {b} cut ra by {b}.rfoot;" for b in rfoot] + ["} rfoot;", ""]
    lk += ["lookup half {"] + [f"  sub {b}' cut' @NEXT by {b}.half;" for b in bases if b != "ra"]
    lk += ["} half;", ""]
    lk += ["lookup final {"] + [f"  sub {b} cut by {b}.final;" for b in bases if b != "ra"] + ["} final;", ""]

    # 7. the vowel signs' parts: a hook takes the neck its base asks for
    by_right: dict[int, list] = {}
    by_mid: dict[int, list] = {}
    by_pair: dict[tuple, list] = {}
    for name, (_, _, nr, nm) in places.items():
        by_right.setdefault(nr, []).append(name)
        by_mid.setdefault(nm, []).append(name)
        by_pair.setdefault((nm, nr), []).append(name)
    vow = ["lookup vowels {", f"  sub @VBASE vs.ai' by flag.e flag.i;"]
    for (nm, nr), names in sorted(by_pair.items()):
        vow.append(f"  sub {_cls(names)} vs.au' by hook.o.{nm} hook.u.{nr};")
    for n, names in sorted(by_right.items()):
        vow.append(f"  sub {_cls(names)} vs.u' by hook.u.{n};")
    for n, names in sorted(by_mid.items()):
        vow.append(f"  sub {_cls(names)} vs.o' by hook.o.{n};")
    vow += ["} vowels;", ""]
    lk += vow
    # 8. strays: a mark with no sign to carry it, after a glyph, is the box
    lk += ["lookup strays {", "  ignore sub @VBASE @VSIGN';", "  ignore sub pa dot';",
           f"  sub {_cls(['space'] + [g for g in _all_bases(enc, places)] + signs + ['cut', 'dot', 'flag.i', 'flag.e'] + _hooks(places))} "
           f"[@VSIGN cut dot]' by notdef.box;", "} strays;", ""]
    names = ["softdot", "fused", "rhalf", "rfinal", "rfoot", "half", "final", "vowels", "strays"]
    lines += lk + ["feature rclt {"] + [f"  lookup {n};" for n in names] + ["} rclt;", ""]

    # mark positioning
    hooks_u = sorted({f"hook.u.{nr}" for _, _, nr, _ in places.values()} | {f"hook.u.{nm}" for _, _, _, nm in places.values()})
    hooks_o = sorted({f"hook.o.{nm}" for _, _, _, nm in places.values()} | {f"hook.o.{nr}" for _, _, nr, _ in places.values()})
    lines += [
        "markClass [vs.i flag.i] <anchor 0 0> @TOP_RIGHT;",
        "markClass [vs.e flag.e] <anchor 0 0> @TOP_MID;",
        f"markClass {_cls(hooks_u)} <anchor 0 0> @FOOT_RIGHT;",
        f"markClass {_cls(hooks_o)} <anchor 0 0> @FOOT_MID;",
        "",
        "feature mark {",
    ]
    for name, (_, a, _, _) in places.items():
        lines.append(f"  pos base {name} <anchor {a['right']} 0> mark @TOP_RIGHT <anchor {a['emid']} 0> mark @TOP_MID "
                     f"<anchor {a['right']} 0> mark @FOOT_RIGHT <anchor {a['mid']} 0> mark @FOOT_MID;")
    lines += ["} mark;", ""]
    return "\n".join(lines)


def _all_bases(enc, places) -> list[str]:
    """Every glyph that stands on the line: the characters and the forms, but not the marks."""
    cons, bases, c_r, rfoot = inventory(enc)
    out = [g["glyph"] for g in enc["glyphs"] if g["kind"] in ("consonant", "vowel", "digit", "point")]
    out += ["fa"] + [f["glyph"] for f in enc["fused"]]
    out += [f"{b}.{form}" for b in bases for form in ("half", "final")]
    out += [f"{b}.rfoot" for b in rfoot]
    return list(dict.fromkeys(out))


def _hooks(places) -> list[str]:
    ns = sorted({n for _, _, nr, nm in places.values() for n in (nr, nm)})
    return [f"hook.{p}.{n}" for p in ("u", "o") for n in ns]


def write_names(path: Path = ROOT / "tools" / "names" / "vedyakshara.json") -> Path:
    """The character names: ``VEDYAKSHARA LETTER <SPELLING>``, ``VEDYAKSHARA VOWEL SIGN
    <VOWEL>``, ``VEDYAKSHARA SIGN CUT``, ``VEDYAKSHARA SIGN SOFT DOT``,
    ``VEDYAKSHARA DIGIT <NUMBER>``, ``VEDYAKSHARA PAUSE`` and ``VEDYAKSHARA FULL STOP``."""
    digits = "ZERO ONE TWO THREE FOUR FIVE SIX SEVEN EIGHT NINE".split()
    names = {}
    for r in encoding()["glyphs"]:
        kind, g = r["kind"], r["glyph"]
        if kind in ("consonant", "vowel"):
            label = f"LETTER {g.upper()}"
        elif kind == "vowel sign":
            label = f"VOWEL SIGN {r['spelling'].upper()}"
        elif kind == "digit":
            label = f"DIGIT {digits[int(r['spelling'])]}"
        elif g == "cut":
            label = "SIGN CUT"
        elif g == "dot":
            label = "SIGN SOFT DOT"
        else:
            label = {"pause": "PAUSE", "stop": "FULL STOP"}[g]
        names[r["codepoint"]] = f"VEDYAKSHARA {label}"
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
