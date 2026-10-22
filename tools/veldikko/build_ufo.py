# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Write sources/Veldikko.ufo from the Veldikko letters and their joining.

    .venv/bin/python tools/veldikko/build_ufo.py [--out sources/Veldikko.ufo]

Every letter of ``encoding.json``, Sinale's and Áelendi's, is drawn in the one hand
(``strokes.HAND``) in each of its forms
(``joining.py``): isolated on its code point, and initial, medial and final, the
initial and medial also stretched, and a nasal's isolated and final forms with the
two long tails. Every vowel mark is drawn alone on its code point and precomposed
with each combination of length, pitch and emphasis. The outlines are fitted with
cubic curves by Teng Chou's ``fit.py``. The UFO is generated: an edit belongs in the
letters or the joining, and this script is run after it, before ``build.sh``
compiles the UFO. The UFO is committed, so the build compiles the same source on
every platform. The character names, ``tools/names/veldikko.json``, are written
beside it.

**Visual order.** The Veldikko's code points are unassigned characters of plane 1,
right to left by default. HarfBuzz shapes a run of them in visual order, left to
right on the page, because they have no script of their own, so every rule here
reads a word from its last letter to its first: a letter's neighbour on the left
is the letter after it, and a vowel mark, which follows its letter in the text,
stands before it in the run. That is why the marks are placed by contextual
positioning from the letter that follows them in the run, not by mark-to-base
attachment, which looks backward.

**The features.** ``ccmp`` empties the default-ignorables. The rest sit in
``rclt`` and ``mark``, which every HarfBuzz shaper applies to horizontal text:

1. a vowel and the length, pitch and emphasis signs after it become one
   precomposed mark;
2. each letter takes its form from its neighbours, marks ignored: medial between
   two letters, initial with only a letter after it, final with only one before;
3. an initial or medial letter carrying a long or pitched vowel, or a diphthong,
   takes its stretched form;
4. ``ss01`` gives a word's last nasal the forward sweep, ``ss02`` the ezh, and
   ``salt`` offers both;
5. a vowel mark stands over the letter it follows, at the point that letter's form
   states, and the second mark of a diphthong beside the first; the length bar
   stands beneath its letter.

**Metrics.** Every outline is scaled by the factor that brings the body, the height
of the bowls, to the x-height every face shares (``tools/vertical.py``), measured on
the crozier _r_, the one letter that stands at the bowls' height alone. The
risers, raised stems and tails keep their length beyond it, so they reach past the
shared ascent and descent; the ``OS/2`` Windows metrics grow to hold them. A
side that joins ends at the join point, so a joined word is one connected line; a
side that does not join stands ``joining.SIDEBEARING`` clear of its ink. The notdef
and its box are Khelathi Zethu Glyphs', and the box takes every Latin and
punctuation code point (``tools/notdef_box.py``).
"""

from __future__ import annotations

import argparse
import importlib.util
import itertools
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
import joining as J  # noqa: E402
import letters as L  # noqa: E402
import notdef_box  # noqa: E402
import strokes as S  # noqa: E402

_spec = importlib.util.spec_from_file_location("teng_chou_fit", HERE.parent / "teng-chou" / "fit.py")
fit = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(fit)

FAMILY = "Veldikko"
STEM = "Veldikko"
STYLE = S.HAND
ENCODING = HERE / "encoding.json"
BODY = 513.5  # the x-height every face shares, which the bowls' height meets
BODIES = ("r",)  # the crozier, the one letter standing at the bowls' height alone
CAPS = ("p", "t", "k", "d")  # the raised stops: the typical tall letters
SPACE = 400  # the word space, in font units
ASCENT, DESCENT, LINE_GAP = 945, -200, 100
WIN_ASCENT, WIN_DESCENT = 945, 250

VOWELS = ("a", "o", "u", "e", "i", "y", "ë")
PITCH = {"": 0.0, "rise": 1.0, "fall": -1.0}
MODIFIERS = ("long", "rise", "fall", "emph")

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


def vowel_name(v: str, long: bool = False, pitch: str = "", emph: bool = False) -> str:
    base = {"ë": "edieresis"}.get(v, v)
    parts = [f"vowel.{base}"] + (["long"] if long else []) + ([pitch] if pitch else []) + (["emph"] if emph else [])
    return ".".join(parts)


def vowel_variants():
    """Every precomposed vowel mark: (name, vowel, long, pitch, emphasis)."""
    for v in VOWELS:
        for long, pitch, emph in itertools.product((False, True), ("", "rise", "fall"), (False, True)):
            yield vowel_name(v, long, pitch, emph), v, long, pitch, emph


def stretches(name: str, long: bool, pitch: str) -> bool:
    return long or bool(pitch)


def letter_forms(row: dict):
    """Every form of one letter: (glyph name, form, tail, stretched)."""
    g = row["glyph"]
    yield g, "isol", None, False
    for nm in ("init", "medi", "fina"):
        yield f"{g}.{nm}", nm, None, False
    for nm in ("init", "medi"):
        yield f"{g}.{nm}.wide", nm, None, True
    if row["letter"] in J.NASALS:
        for tail in J.TAILS:
            yield f"{g}.{tail}", "isol", tail, False
            yield f"{g}.fina.{tail}", "fina", tail, False


# -- drawing -------------------------------------------------------------------------------------


def outline_polys(tracks) -> list:
    return S.contours(S.outline(tracks, STYLE))


def draw(glyph, polys, k: float):
    for _, segs in fit.fit([[(x * k, y * k) for x, y in p] for p in polys]):
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


def mark_tracks(v, long, pitch, emph):
    m = L.Mark(v, long, PITCH[pitch], emph)
    return J.page_tracks(L._marks([m], 0.0, 0.0, STYLE), STYLE)


def modifier_tracks(name: str):
    """A length, pitch or emphasis sign standing alone, as it is drawn on a vowel."""
    if name == "emph":
        return J.page_tracks(L._brow(85.0, 60.0, STYLE), STYLE)
    t = S.Track(-40.0, 24.0, 0.0)
    S._tail(t, 2.0 if name == "long" else 1.0, PITCH.get(name, 0.0))
    return J.page_tracks([t], STYLE)


def compiled_extent(font) -> tuple[int, int]:
    """The highest and lowest point of the glyph boxes, as the build compiles them:
    the outlines converted to TrueType curves by ufo2ft, as fontmake converts them,
    with every point counted, as the ``glyf`` table counts them."""
    import ufo2ft

    tt = ufo2ft.compileTTF(font, removeOverlaps=False, useProductionNames=False)
    glyf = tt["glyf"]
    boxes = [glyf[n] for n in tt.getGlyphOrder() if glyf[n].numberOfContours]
    return max(g.yMax for g in boxes), min(g.yMin for g in boxes)


def f_width(tracks) -> float:
    fs = [f for t in tracks for f, _, _ in t.samples]
    return max(fs) - min(fs)


def build(out: Path) -> tuple[Path, dict]:
    enc = encoding()
    letters = [r for r in enc["glyphs"] if r["kind"] == "letter"]

    # The letters' forms, in the forward frame, with their metrics.
    forms = {}
    for row in letters:
        lt = L.LETTERS[row["letter"]]
        for name, nm, tail, wide in letter_forms(row):
            forms[name] = J.form(lt, nm, STYLE, tail=tail, stretch=wide)
    polys = {name: outline_polys(J.page_tracks(f.tracks, STYLE, f.left_pe)) for name, f in forms.items()}

    def height(name):
        ys = [y for p in polys[name] for _, y in p]
        return max(ys) - min(ys)

    k = round(BODY / statistics.median(height(g) for g in BODIES), 4)

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
        "Veldikko, the starlight-hand of the Sinale in thalorna, in which the Sinale and the Aelendi write: "
        "a flowing, joined calligraphy written right to left, with its vowels as marks above."
    )
    info.openTypeNameLicense = "SIL Open Font License 1.1"
    info.openTypeNameLicenseURL = "https://openfontlicense.org"
    info.openTypeNameUniqueID = f"{STEM}-Regular;0.1"
    info.openTypeNameVersion = "Version 0.1"
    info.versionMajor, info.versionMinor = 0, 100
    info.postscriptFontName = f"{STEM}-Regular"
    info.postscriptUnderlinePosition = -80
    info.postscriptUnderlineThickness = 36

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

    cps = {r["glyph"]: int(r["codepoint"][2:], 16) for r in enc["glyphs"]}
    categories = {}

    for name, f in forms.items():
        g = font.newGlyph(name)
        draw(g, polys[name], k)
        g.width = round(f.advance * k)
        # where the marks over the letter and the bar beneath it stand; the mark
        # feature is written from the same points, and the guard reads them back
        g.appendAnchor({"name": "mark", "x": round(f.mark[0] * k), "y": round(f.mark[1] * k)})
        g.appendAnchor({"name": "bar", "x": round(f.bar * k), "y": round(S.BAR * k)})
        if name in cps:
            g.unicodes = [cps[name]]
        categories[name] = "base"
        order.append(name)

    marks = {}
    for name, v, long, pitch, emph in vowel_variants():
        tracks = mark_tracks(v, long, pitch, emph)
        marks[name] = tracks
    for name in MODIFIERS:
        marks[name] = modifier_tracks(name)
    marks["bar"] = J.page_tracks(S.shape("bar", 0, 0, STYLE).tracks, STYLE, 0.0, S.BAR)
    for name, tracks in marks.items():
        g = font.newGlyph(name)
        draw(g, outline_polys(tracks), k)
        g.width = 0
        if name in cps:
            g.unicodes = [cps[name]]
        categories[name] = "mark"
        order.append(name)

    for name in (".notdef", notdef_box.BOX, "space", "ignorable", "ignorable.sub"):
        categories.setdefault(name, "base" if name in (".notdef", notdef_box.BOX) else "unassigned")

    def median_height(names):
        hs = []
        for n in names:
            b = font[n].getBounds(font)
            hs.append(b.yMax - b.yMin)
        return round(statistics.median(hs))

    info.capHeight = median_height(CAPS)
    info.xHeight = median_height(BODIES)
    font.lib["public.glyphOrder"] = order
    font.lib["public.openTypeCategories"] = {n: c for n, c in sorted(categories.items()) if c != "unassigned"}
    widths = {n: f_width(t) * k for n, t in marks.items() if n.startswith("vowel.") or n in MODIFIERS}
    font.features.text = features(letters, forms, widths, k)
    top, bottom = compiled_extent(font)
    info.openTypeOS2WinAscent = max(WIN_ASCENT, top)
    info.openTypeOS2WinDescent = max(WIN_DESCENT, -bottom)

    if out.exists():
        shutil.rmtree(out)
    font.save(out)
    return out, {"scale": k}


# -- the features --------------------------------------------------------------------------------


def _cls(names) -> str:
    return "[" + " ".join(names) + "]"


def features(letters, forms, widths, k) -> str:
    base = [r["glyph"] for r in letters]
    nasal = [r["glyph"] for r in letters if r["letter"] in J.NASALS]
    vowels = [n for n, *_ in vowel_variants()]
    marks_v = vowels + list(MODIFIERS)
    stretchy = [n for n, v, long, pitch, emph in vowel_variants() if stretches(n, long, pitch)]
    lines = [FEATURE_HEAD]
    lines.append(f"@LET = {_cls(base)};")
    for nm in ("init", "medi", "fina"):
        lines.append(f"@LET_{nm} = {_cls(f'{g}.{nm}' for g in base)};")
    for nm in ("init", "medi"):
        lines.append(f"@LET_{nm}_wide = {_cls(f'{g}.{nm}.wide' for g in base)};")
    lines.append(f"@ANY = {_cls(forms)};")
    lines.append(f"@V = {_cls(marks_v)};")
    lines.append(f"@VSTRETCH = {_cls(stretchy)};")
    lines.append("@BAR = [bar];")
    lines.append("")

    # 1. a vowel and the signs after it, in either order, become one mark; in the run
    # the signs stand before the vowel.
    lig = ["lookup vowels {"]
    rules = []
    for n, v, long, pitch, emph in vowel_variants():
        mods = (["long"] if long else []) + ([pitch] if pitch else []) + (["emph"] if emph else [])
        if not mods:
            continue
        for perm in itertools.permutations(mods):
            seq = list(reversed(perm)) + [vowel_name(v)]
            rules.append((len(seq), f"  sub {' '.join(seq)} by {n};"))
    lig += [r for _, r in sorted(rules, key=lambda x: -x[0])]
    lig.append("} vowels;")

    # 2. joining, in visual order: the letter after a letter stands to its left.
    join = [
        "lookup forms {",
        "  lookupflag IgnoreMarks;",
        "  sub @ANY @LET' @ANY by @LET_medi;",
        "  sub @ANY @LET' by @LET_init;",
        "  sub @LET' @ANY by @LET_fina;",
        "} forms;",
    ]
    # 3. the stretch, for a letter whose mark needs room ahead of it.
    stretch = [
        "lookup stretch {",
        "  lookupflag UseMarkFilteringSet @V;",
        "  sub @V @V [@LET_init @LET_medi]' by [@LET_init_wide @LET_medi_wide];",
        "  sub @VSTRETCH [@LET_init @LET_medi]' by [@LET_init_wide @LET_medi_wide];",
        "} stretch;",
    ]
    lines += lig + [""] + join + [""] + stretch + [""]
    lines += ["feature rclt {", "  lookup vowels;", "  lookup forms;", "  lookup stretch;", "} rclt;", ""]

    # 4. the long tails of a word's last nasal.
    fin = [g for g in nasal] + [f"{g}.fina" for g in nasal]
    for tag, tail in (("ss01", "sweep"), ("ss02", "ezh")):
        to = [f"{g}.{tail}" for g in nasal] + [f"{g}.fina.{tail}" for g in nasal]
        lines += [f"feature {tag} {{", f"  sub {_cls(fin)} by {_cls(to)};", f"}} {tag};", ""]
    lines.append("feature salt {")
    for g in fin:
        head, _, rest = g.partition(".")
        stem = f"{head}.{rest}." if rest else f"{head}."
        lines.append(f"  sub {g} from [{stem}sweep {stem}ezh];")
    lines += ["} salt;", ""]

    # 5. positioning, from the letter after the marks in the run.
    groups: dict[tuple, list] = {}
    bars: dict[int, list] = {}
    for name, f in forms.items():
        groups.setdefault((round(f.mark[0] * k), round(f.mark[1] * k)), []).append(name)
        bars.setdefault(round(f.bar * k), []).append(name)
    place = ["lookup vowelplace {", "  lookupflag UseMarkFilteringSet @V;"]
    for (x, y), names in sorted(groups.items()):
        place.append(f"  pos @V' <{x} {y} 0 0> @V {_cls(names)};")
        place.append(f"  pos @V' <{x} {y} 0 0> {_cls(names)};")
    place.append("} vowelplace;")

    # The two marks of a diphthong stand MARK_SEP apart, the pair centred where one would be.
    buckets: dict[int, list] = {}
    for n, w in widths.items():
        buckets.setdefault(int(round(w / 10.0)) * 10, []).append(n)
    sep = L.MARK_SEP * k
    pair = ["lookup diphthong {", "  lookupflag UseMarkFilteringSet @V;"]
    for w2, n2 in sorted(buckets.items()):  # the second mark said, first in the run
        for w1, n1 in sorted(buckets.items()):
            pair.append(f"  pos {_cls(n2)} <{-round((w1 + sep) / 2)} 0 0 0> {_cls(n1)} <{round((w2 + sep) / 2)} 0 0 0>;")
    pair.append("} diphthong;")

    bar = ["lookup barplace {", "  lookupflag UseMarkFilteringSet @BAR;"]
    for x, names in sorted(bars.items()):
        bar.append(f"  pos bar' <{x} 0 0 0> {_cls(names)};")
    bar.append("} barplace;")
    lines += place + [""] + pair + [""] + bar + [""]
    lines += ["feature mark {", "  lookup vowelplace;", "  lookup diphthong;", "  lookup barplace;", "} mark;", ""]
    return "\n".join(lines)


def write_names(path: Path = ROOT / "tools" / "names" / "veldikko.json") -> Path:
    """The character names: ``VELDIKKO LETTER <SPELLING>``, ``VELDIKKO LETTER CARRIER``,
    ``VELDIKKO VOWEL SIGN <VOWEL>`` and ``VELDIKKO SIGN <NAME>``."""
    names = {}
    signs = {"long": "LONG", "rise": "RISE", "fall": "FALL", "emph": "EMPHASIS", "bar": "DOUBLING BAR"}
    for r in encoding()["glyphs"]:
        if r["kind"] == "letter":
            if r["glyph"] == "carrier":
                label = "CARRIER"
            else:
                sp = r["spelling"].upper()
                label = sp.replace("'", " EJECTIVE")
                if r["glyph"] == "dhasp":
                    label = "AELENDI DH"
            names[r["codepoint"]] = f"VELDIKKO LETTER {label}"
        elif r["kind"] == "vowel":
            v = {"ë": "E WITH DIAERESIS"}.get(r["vowel"], r["vowel"].upper())
            names[r["codepoint"]] = f"VELDIKKO VOWEL SIGN {v}"
        else:
            names[r["codepoint"]] = f"VELDIKKO SIGN {signs[r['glyph']]}"
    path.write_text(json.dumps(names, indent=4, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default=str(ROOT / "sources" / f"{STEM}.ufo"))
    a = ap.parse_args()
    path, facts = build(Path(a.out))
    print(f"{path}: scale {facts['scale']}")
    print(write_names())


if __name__ == "__main__":
    main()
