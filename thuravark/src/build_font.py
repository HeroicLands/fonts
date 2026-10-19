# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Build ThuravarkRunic-Regular.ttf and .woff2 from the stave source.

The strokes, their outlines and their union come from Pirzath Carved's build.
The layout is written as a feature file: ``ccmp`` to turn an acute vowel into
the stave twice and a doubled digraph into two digraph staves, and ``liga`` for
the digraphs, for ``y`` before a vowel as the glide and ``y`` elsewhere as the
vowel ``i``. Nothing is kerned and nothing is positioned: each stave carries
its own room.

    .venv/bin/python thuravark/src/build_font.py [--out thuravark/fonts] [--broken]
"""

import argparse
import os
import sys
from pathlib import Path

import pathops
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
from fontTools.fontBuilder import FontBuilder
from fontTools.misc.timeTools import epoch_diff

sys.path.insert(0, str(Path(__file__).resolve().parent))
import staves as G  # noqa: E402  (also puts Pirzath's src on the path)
from build import outline, tt_glyph  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent
HERE = Path(__file__).resolve().parent.parent
UPM = 1000
ASCENDER = 960
DESCENDER = -180
FAMILY = "Thuravark Runic"
STYLE = "Regular"
PS_NAME = "ThuravarkRunic-Regular"
VERSION = 0.1


def feature_text(broken=False):
    comb = "\n".join(f"  sub {v} acutecomb by {v}acute;" for v in G.VOWELS)
    long_vowels = "\n".join(f"  sub {v}acute by {v} {v};" for v in G.VOWELS)
    doubled = "\n".join(f"  sub {k[0]}' {k[0]} {k[1]} by {v};" for k, v in G.DIGRAPHS.items())
    doubled += "\n  sub h' h l by hl;\n  ignore sub n' n g h;\n  sub n' n g by ng;"
    digraphs = "\n".join(f"  sub {k[0]} {k[1]} by {v};" for k, v in G.DIGRAPHS.items())
    other = "\n".join(f"  sub {k[0]} {k[1]} by {v};" for k, v in G.OTHER_DIGRAPHS.items())
    if broken:
        # The deliberately broken build the guard must catch: long vowels stay
        # precomposed, digraphs stay two staves and y never becomes the vowel.
        comb = long_vowels = doubled = digraphs = other = ""
    glide = "" if broken else "  ignore sub y' @VOWEL;\n  sub y' by i;"
    glide2 = "" if broken else "  sub y by j;"
    return f"""
languagesystem DFLT dflt;
languagesystem latn dflt;

# The vowels a glide y stands before.
@VOWEL = [a e i o u];

# An acute vowel is the stave twice, and so is a vowel followed by U+0301. The
# first letter of a doubled digraph (tth, ddh, kkh, ggh, hhl, nng) becomes the
# digraph itself, so the ligatures below see two digraphs; ngh is n and gh.
feature ccmp {{
lookup ccmp_comb {{
{comb}
}} ccmp_comb;
lookup ccmp_long {{
{long_vowels}
}} ccmp_long;
lookup ccmp_doubled {{
{doubled}
}} ccmp_doubled;
}} ccmp;

# The lookups run in order, so the longest spelling wins: th dh kh gh first,
# which makes ngh the letter n and gh, then ng and hl. A y not before a vowel
# is the vowel i; any other y is the glide.
feature liga {{
lookup liga_digraphs {{
{digraphs}
}} liga_digraphs;
lookup liga_other {{
{other}
}} liga_other;
lookup liga_y {{
{glide}
}} liga_y;
lookup liga_glide {{
{glide2}
}} liga_glide;
}} liga;
"""


def copyright_line():
    return (ROOT / "LICENSE").read_text(encoding="utf-8").splitlines()[0].strip()


def build(out_dir: Path, break_it: bool = False):
    order = [g.name for g in G.ALL_GLYPHS]
    outlines = {g.name: outline(g) if g.cuts else pathops.Path() for g in G.ALL_GLYPHS}
    glyf = {name: tt_glyph(path) for name, path in outlines.items()}
    metrics = {g.name: (g.width, 0) for g in G.ALL_GLYPHS}

    fb = FontBuilder(UPM, isTTF=True)
    fb.setupGlyphOrder(order)
    fb.setupCharacterMap(G.cmap())
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
            "description": "The rune-row of the Nordmen of thalorna, cut as straight staves.",
        }
    )
    fb.setupOS2(
        sTypoAscender=ASCENDER,
        sTypoDescender=DESCENDER,
        sTypoLineGap=0,
        usWinAscent=ASCENDER + 40,
        usWinDescent=-DESCENDER,
        sxHeight=G.STEM_H,
        sCapHeight=G.STEM_H,
        fsType=0,
        achVendID="HRLD",
    )
    fb.setupPost()
    fb.font["head"].fontRevision = VERSION
    fb.font["head"].flags |= 0x0008
    # A fixed timestamp makes the build reproducible; SOURCE_DATE_EPOCH overrides it.
    stamp = int(os.environ.get("SOURCE_DATE_EPOCH", "1767225600")) - epoch_diff
    fb.font["head"].created = fb.font["head"].modified = stamp
    fb.font.recalcTimestamp = False

    fea = feature_text(broken=break_it)
    addOpenTypeFeaturesFromString(fb.font, fea)

    out_dir.mkdir(parents=True, exist_ok=True)
    (ROOT / "build").mkdir(exist_ok=True)
    (ROOT / "build" / "thuravark-features.fea").write_text(fea, encoding="utf-8")
    ttf = out_dir / f"{PS_NAME}.ttf"
    fb.save(str(ttf))
    fb.font.flavor = "woff2"
    fb.save(str(out_dir / f"{PS_NAME}.woff2"))
    return ttf


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default=str(HERE / "fonts"))
    ap.add_argument("--broken", action="store_true",
                    help="build without ligatures or decomposition, to prove the guard fails")
    args = ap.parse_args()
    ttf = build(Path(args.out), break_it=args.broken)
    print(f"{ttf}: {len(G.ALL_GLYPHS)} glyphs")


if __name__ == "__main__":
    main()
