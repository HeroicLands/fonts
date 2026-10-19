# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Build PirzathCarved-Regular.ttf and .woff2 from the glyph source.

Each cut in ``glyphs.py`` becomes a polygon: a stroke is a groove that tapers
to a point at both ends, a dot is a drilled octagon. The polygons of a glyph
are united into one outline, and the OpenType layout is written as a feature
file: ``calt`` to open or close a straight quotation mark by context, ``ccmp``
to split a precomposed long vowel into vowel and length mark, ``liga`` for the
four digraphs and the lost letters, ``rlig`` to turn a doubled consonant into
the letter and the doubling mark, ``mark`` to seat both marks, and ``kern`` derived from the outlines'
profiles.

    .venv/bin/python src/build.py [--out fonts]
"""

import argparse
import math
import os
import sys
from pathlib import Path

import pathops
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
from fontTools.fontBuilder import FontBuilder
from fontTools.misc.timeTools import epoch_diff
from fontTools.pens.ttGlyphPen import TTGlyphPen

sys.path.insert(0, str(Path(__file__).parent))
import glyphs as G  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
UPM = 1000
ASCENDER = 800
DESCENDER = -250
FAMILY = "Pirzath Carved"
STYLE = "Regular"
PS_NAME = "PirzathCarved-Regular"
VERSION = 0.1

# Kerning: the optical gap the auto-kerner aims for between two inks, and how
# far it may tighten or loosen the default spacing to get there.
KERN_TARGET = 165
KERN_MAX_TIGHT = 110
KERN_MAX_LOOSE = 40
BAND = 25


# --- outlines ---------------------------------------------------------------


def stroke_polygon(s: G.S, weight: float):
    """A graver groove: full width in the middle, a point at either end."""
    dx, dy = s.x2 - s.x1, s.y2 - s.y1
    length = math.hypot(dx, dy)
    ux, uy = dx / length, dy / length
    nx, ny = -uy, ux
    half = weight / 2
    taper = min(weight * 0.7, length * 0.45)
    p1 = (s.x1, s.y1)
    p2 = (s.x1 + ux * taper + nx * half, s.y1 + uy * taper + ny * half)
    p3 = (s.x2 - ux * taper + nx * half, s.y2 - uy * taper + ny * half)
    p4 = (s.x2, s.y2)
    p5 = (s.x2 - ux * taper - nx * half, s.y2 - uy * taper - ny * half)
    p6 = (s.x1 + ux * taper - nx * half, s.y1 + uy * taper - ny * half)
    return [p1, p2, p3, p4, p5, p6]


def dot_polygon(d: G.D, weight: float):
    """A drilled dot: an octagon a little wider than a stroke."""
    r = weight * 0.62
    return [
        (d.x + r * math.cos(a), d.y + r * math.sin(a))
        for a in (math.pi / 8 + i * math.pi / 4 for i in range(8))
    ]


def signed_area(poly):
    a = 0.0
    for (x1, y1), (x2, y2) in zip(poly, poly[1:] + poly[:1]):
        a += x1 * y2 - x2 * y1
    return a / 2


def polygons(glyph: G.Glyph):
    polys = []
    for cut in glyph.cuts:
        if isinstance(cut, G.S):
            polys.append(stroke_polygon(cut, cut.w or glyph.weight))
        else:
            polys.append(dot_polygon(cut, glyph.weight))
    # One winding direction for all, so the union does not cancel overlaps.
    return [p if signed_area(p) > 0 else list(reversed(p)) for p in polys]


def outline(glyph: G.Glyph) -> pathops.Path:
    path = pathops.Path()
    for poly in polygons(glyph):
        path.moveTo(*poly[0])
        for pt in poly[1:]:
            path.lineTo(*pt)
        path.close()
    return pathops.simplify(path, fix_winding=True, clockwise=True)


def tt_glyph(path: pathops.Path):
    pen = TTGlyphPen(None)
    path.draw(pen)
    return pen.glyph()


# --- kerning ----------------------------------------------------------------


def profile(path: pathops.Path, advance: int):
    """Per band of height BAND, the leftmost and rightmost ink of a glyph."""
    edges = []
    for contour in path.contours:
        pts = [pt for verb, pts in contour for pt in pts]
        for (x1, y1), (x2, y2) in zip(pts, pts[1:] + pts[:1]):
            if y1 != y2:
                edges.append((x1, y1, x2, y2))
    bands = {}
    y = -200 + BAND / 2
    while y < ASCENDER:
        xs = []
        for x1, y1, x2, y2 in edges:
            if (y1 <= y < y2) or (y2 <= y < y1):
                xs.append(x1 + (y - y1) * (x2 - x1) / (y2 - y1))
        if xs:
            bands[round(y)] = (min(xs), advance - max(xs))
        y += BAND
    return bands


def auto_kern(outlines, names):
    """Kerning that gives every pair the same optical gap at its closest approach."""
    profiles = {n: profile(outlines[n], G.GLYPHS[n].width) for n in names}
    pairs = {}
    for left in names:
        lp = profiles[left]
        if not lp:
            continue
        for right in names:
            rp = profiles[right]
            if not rp:
                continue
            gap = None
            for y, (_, right_sb) in lp.items():
                for dy in (-2 * BAND, -BAND, 0, BAND, 2 * BAND):
                    other = rp.get(y + dy)
                    if other is None:
                        continue
                    g = right_sb + other[0] + abs(dy) * 0.6
                    gap = g if gap is None else min(gap, g)
            if gap is None:
                continue
            kern = max(-KERN_MAX_TIGHT, min(KERN_MAX_LOOSE, KERN_TARGET - gap))
            kern = int(round(kern / 5.0)) * 5
            if abs(kern) >= 10:
                pairs[(left, right)] = kern
    return pairs


# --- features ---------------------------------------------------------------


def feature_text(kern_pairs, broken=False):
    quote_names = {q.name for q in G.QUOTES}
    after = " ".join(g.name for g in G.ALL_GLYPHS if g.name not in quote_names | {"space"})
    ccmp = "\n".join(f"  sub {name} by {name[0]} lengthmark;" for name in G.ACUTES.values())
    old_digraphs = list(G.DIGRAPHS.items())
    lost_digraphs = list(G.LOST_CONSONANT_DIGRAPHS.items())
    digraph_first = "\n".join(f"  sub {k[0]}' {k[0]} {k[1]} by {v};" for k, v in old_digraphs)
    # A doubled lost digraph, ssh, zzh, tts, nng: the first letter becomes the
    # digraph and the ligature takes the rest. nngh is n, n, gh.
    lost_first = "\n".join(
        ("  ignore sub n' n g h;\n" if k == "ng" else "") + f"  sub {k[0]}' {k[0]} {k[1]} by {v};"
        for k, v in lost_digraphs
    )
    liga = "\n".join(f"  sub {k[0]} {k[1]} by {v};" for k, v in old_digraphs)
    liga += "\n  sub less less by quote.open;\n  sub greater greater by quote.close;"
    liga_lost = "\n".join(f"  sub {k[0]} {k[1]} by {v};" for k, v in lost_digraphs)
    liga_y = "  ignore sub y' @VOWEL;\n  sub y' by i;"
    liga_pairs = "\n".join(f"  sub {k[0]} {k[1]} by {v};" for k, v in G.LOST_VOWEL_PAIRS.items())
    marks = "\n".join(
        f"  pos base {v.name} <anchor {int(v.anchor[0])} {int(v.anchor[1])}> mark @LEN;"
        for v in G.VOWELS + G.LOST_VOWELS
    )
    marks += "\n" + "\n".join(
        f"  pos base {c.name} <anchor {int(c.below[0])} {int(c.below[1])}> mark @DBL;"
        for c in G.ALL_CONSONANTS
    )
    bases = " ".join(g.name for g in G.ALL_GLYPHS if g.cuts and g.kind != "mark")
    doubling = "\n".join(f"  sub {c.name} {c.name}' by doubling;" for c in G.ALL_CONSONANTS)
    kern = "\n".join(f"  pos {a} {b} {k};" for (a, b), k in sorted(kern_pairs.items()))
    quotes = """  sub @AFTER quotedbl' by quote.close;
  sub quotedbl' by quote.open;"""
    vowels = " ".join(v.name for v in G.VOWELS)
    if broken:
        # The deliberately broken build the guard must catch: the long vowels
        # stay precomposed, the digraphs stay two letters, the lost letters
        # have no spelling but their own keys, and a straight quote never
        # closes.
        ccmp = liga = quotes = digraph_first = doubling = ""
        lost_first = liga_lost = liga_y = liga_pairs = ""
    return f"""
languagesystem DFLT dflt;
languagesystem latn dflt;

# Everything a closing quotation mark can follow: any glyph but a space or
# another quotation mark.
@AFTER = [{after}];

# The vowels a glide y stands before.
@VOWEL = [{vowels}];

# A straight quotation mark opens after a space or at the start of the text,
# and closes elsewhere.
feature calt {{
{quotes}
}} calt;

# A precomposed long vowel is the vowel and its length mark, and the first
# letter of a doubled digraph (tth, ddh, kkh, ggh, ssh, zzh, tts, nng, nny,
# hhl, cch) is the digraph itself, so that the ligature and the doubling rule
# below see two of the same letter.
feature ccmp {{
lookup ccmp_long {{
{ccmp}
}} ccmp_long;
lookup ccmp_doubled {{
{digraph_first}
{lost_first}
}} ccmp_doubled;
}} ccmp;

# The lookups run in order, so the longest spelling wins. The four digraphs
# come first, which makes ngh the letter n and gh; << and >> are the quotation
# marks. Then the lost consonants, then a y not before a vowel becomes the
# vowel i, then the five vowel pairs, which read through a length mark between
# their vowels; ay, ey and oy are the pairs ai, ei and oi.
feature liga {{
lookup liga_digraphs {{
{liga}
}} liga_digraphs;
lookup liga_lost {{
{liga_lost}
}} liga_lost;
lookup liga_y {{
{liga_y}
}} liga_y;
lookup liga_pairs {{
  lookupflag IgnoreMarks;
{liga_pairs}
}} liga_pairs;
}} liga;

# A consonant written twice is the letter once with the doubling mark.
feature rlig {{
{doubling}
}} rlig;

table GDEF {{
  GlyphClassDef [{bases}], , [lengthmark doubling], ;
}} GDEF;

markClass lengthmark <anchor 0 0> @LEN;
markClass doubling <anchor 0 0> @DBL;

feature mark {{
{marks}
}} mark;

feature kern {{
{kern}
}} kern;
"""


# --- the font ---------------------------------------------------------------


def copyright_line():
    return (ROOT / "LICENSE").read_text(encoding="utf-8").splitlines()[0].strip()


def build(out_dir: Path, break_it: bool = False):
    order = [g.name for g in G.ALL_GLYPHS]
    outlines = {g.name: outline(g) if g.cuts else pathops.Path() for g in G.ALL_GLYPHS}
    glyf = {name: tt_glyph(path) for name, path in outlines.items()}
    metrics = {g.name: (g.width, 0) for g in G.ALL_GLYPHS}
    cmap = G.cmap()

    fb = FontBuilder(UPM, isTTF=True)
    fb.setupGlyphOrder(order)
    fb.setupCharacterMap(cmap)
    fb.setupGlyf(glyf)
    glyf_table = fb.font["glyf"]
    for name in order:
        g = glyf_table[name]
        g.recalcBounds(glyf_table)
        xmin = getattr(g, "xMin", 0) if g.numberOfContours else 0
        metrics[name] = (metrics[name][0], xmin)
    fb.setupHorizontalMetrics(metrics)
    fb.setupHorizontalHeader(ascent=ASCENDER, descent=DESCENDER)
    fb.setupNameTable(
        {
            "copyright": copyright_line(),
            "familyName": FAMILY,
            "styleName": STYLE,
            "uniqueFontIdentifier": f"{PS_NAME};{VERSION}",
            "fullName": f"{FAMILY} {STYLE}",
            "version": f"Version {VERSION}",
            "psName": PS_NAME,
            "licenseDescription": "SIL Open Font License 1.1",
            "licenseInfoURL": "https://openfontlicense.org",
            "description": "The carved form of Pirzath, the script of the Khazari of thalorna.",
        }
    )
    fb.setupOS2(
        sTypoAscender=ASCENDER,
        sTypoDescender=DESCENDER,
        sTypoLineGap=0,
        usWinAscent=ASCENDER + 50,
        usWinDescent=-DESCENDER,
        sxHeight=G.VOW_H,
        sCapHeight=G.CONS_H,
        fsType=0,
        achVendID="HRLD",
    )
    fb.setupPost()
    fb.font["head"].fontRevision = VERSION
    # Overlapping-free outlines; the flag says a renderer need not expect them.
    fb.font["head"].flags |= 0x0008
    # A fixed timestamp makes the build reproducible, so CI can check that the
    # committed fonts match their source. SOURCE_DATE_EPOCH overrides it.
    stamp = int(os.environ.get("SOURCE_DATE_EPOCH", "1767225600")) - epoch_diff
    fb.font["head"].created = fb.font["head"].modified = stamp
    fb.font.recalcTimestamp = False

    # The word-dividing dot keeps its fixed room and is not kerned.
    ink = [g.name for g in G.ALL_GLYPHS if g.cuts and g.kind != "mark" and g.name != "space"]
    kern_pairs = auto_kern(outlines, ink)
    fea = feature_text(kern_pairs, broken=break_it)
    addOpenTypeFeaturesFromString(fb.font, fea)

    out_dir.mkdir(parents=True, exist_ok=True)
    (ROOT / "build").mkdir(exist_ok=True)
    (ROOT / "build" / "features.fea").write_text(fea, encoding="utf-8")
    ttf = out_dir / f"{PS_NAME}.ttf"
    fb.save(str(ttf))
    fb.font.flavor = "woff2"
    fb.save(str(out_dir / f"{PS_NAME}.woff2"))
    return ttf, len(kern_pairs)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default=str(ROOT / "fonts"))
    ap.add_argument(
        "--broken",
        action="store_true",
        help="build without ligatures, decomposition or the lost-letter rules, to prove the guard fails",
    )
    args = ap.parse_args()
    ttf, kerns = build(Path(args.out), break_it=args.broken)
    print(f"{ttf}: {len(G.ALL_GLYPHS)} glyphs, {kerns} kern pairs")


if __name__ == "__main__":
    main()
