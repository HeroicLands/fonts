# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Load the built font and confirm it matches tools/khelathi-zethu-glyphs/encoding.json.

    .venv/bin/python tools/khelathi-zethu-glyphs/check_font.py [fonts/KhelathiZethuGlyphs-Regular.ttf]

- The cmap is exactly the encoding: each drawn sign's default form on its code point,
  the space, the default-ignorable characters on one empty glyph, and every code
  point of the Latin ranges on the box (tools/notdef_box.py), so a Latin letter
  prints the box.
- The glyph set is exactly the encoding's forms, the notdef, the box, the space and
  the two empty glyphs, and every glyph but the empty ones has an outline whose outer contour
  runs clockwise.
- Each advance is the scaled min(1000, round(10 * box width) + 80), the font holds a full
  quadrat between its ascender and descender, and no ink leaves the win metrics. The
  scale is the one of tools/vertical.py.
- Every second form (.b) and third form (.c) is reached by a single substitution
  in salt, ss01 or ss02, and the font carries no other feature, no contextual lookup
  and no positioning.
- The default-ignorable characters shape to nothing.
- The name table carries the licence and the .woff2 beside the .ttf carries the same
  glyphs.
"""

import json
import math
import sys
from fractions import Fraction
from pathlib import Path

import uharfbuzz as hb
from fontTools.ttLib import TTFont

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import font_names  # noqa: E402
import notdef_box  # noqa: E402
import vertical  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent
ENCODING = Path(__file__).resolve().parent / "encoding.json"
EMPTY = {"ignorable", "ignorable.sub"}
FEATURES = {"ccmp", "salt", "ss01", "ss02"}


def scaled(units: int) -> int:
    """A length of the sign grid after the face's scale, rounded half upward."""
    return math.floor(units * Fraction(str(vertical.SCALES["KhelathiZethuGlyphs"])) + Fraction(1, 2))


def cp(text: str) -> int:
    return int(text[2:], 16)


def load():
    return json.loads(ENCODING.read_text(encoding="utf-8"))


def gname(sid: str, v: str) -> str:
    return "z" + sid.replace("-", "_") + "." + v


def expected_cmap(enc) -> dict[int, str]:
    out = {cp(e["codepoint"]): e["glyph"] for e in enc["signs"] if e["drawn"]}
    out[cp(enc["space"]["codepoint"])] = enc["space"]["glyph"]
    for c in enc["ignorables"]["codepoints"]:
        out[cp(c)] = enc["ignorables"]["glyph"]
    for c in notdef_box.codepoints():
        out.setdefault(c, notdef_box.BOX)
    return out


def shape(font_bytes: bytes, text: str, order: list[str], features=None):
    font = hb.Font(hb.Face(font_bytes))
    font.scale = (1000, 1000)
    buf = hb.Buffer()
    buf.add_str(text)
    buf.direction = "rtl"
    buf.script = "Zyyy"
    hb.shape(font, buf, features or {})
    return [(order[i.codepoint], p.x_advance) for i, p in zip(buf.glyph_infos, buf.glyph_positions)]


def area(coords, ends):
    """Signed areas (y up) of the contours of a TrueType glyph, by its control points."""
    out, first = [], 0
    for last in ends:
        pts = coords[first : last + 1]
        a = 0.0
        for (x1, y1), (x2, y2) in zip(pts, pts[1:] + pts[:1]):
            a += x1 * y2 - x2 * y1
        out.append(a / 2)
        first = last + 1
    return out


def lookup_maps(font):
    """{feature tag: {glyph: [substitutes]}} for the font's single and alternate lookups."""
    gsub = font["GSUB"].table
    maps, problems = {}, []
    for rec in gsub.FeatureList.FeatureRecord:
        tag = rec.FeatureTag
        if tag not in FEATURES:
            problems.append(f"the font carries the feature {tag}")
        m = maps.setdefault(tag, {})
        for li in rec.Feature.LookupListIndex:
            lookup = gsub.LookupList.Lookup[li]
            for st in lookup.SubTable:
                if type(st).__name__ == "ExtensionSubst":
                    st = st.ExtSubTable
                name = type(st).__name__
                if name == "SingleSubst":
                    for a, b in st.mapping.items():
                        m.setdefault(a, []).append(b)
                elif name == "AlternateSubst":
                    for a, alts in st.alternates.items():
                        m.setdefault(a, []).extend(alts)
                else:
                    problems.append(f"{tag} has a {name} lookup; only single and alternate substitutions are allowed")
    return maps, problems


def check(path: Path) -> list[str]:
    problems = []
    enc = load()
    font = TTFont(str(path))
    order = font.getGlyphOrder()
    glyf = font["glyf"]
    cmap = font.getBestCmap()
    want = expected_cmap(enc)
    for c in sorted(set(want) | set(cmap)):
        if cmap.get(c) != want.get(c):
            problems.append(f"U+{c:04X} maps to {cmap.get(c)}, expected {want.get(c)}")
    for ch in "AZaz'’":
        if cmap.get(ord(ch)) != notdef_box.BOX:
            problems.append(f"{ch!r} is {cmap.get(ord(ch))}; Latin text and the apostrophe must be {notdef_box.BOX}")
    problems += [line.split(": error: ", 1)[1] for line in notdef_box.check(path)]
    problems += [line.split(": error: ", 1)[1] for line in font_names.check(path)]

    forms = {}
    for e in enc["signs"]:
        for v in e["variants"]:
            forms[gname(e["id"], v)] = (e, v)
    glyphs = {".notdef", notdef_box.BOX, enc["space"]["glyph"], *EMPTY, *forms}
    if set(order) != glyphs:
        extra, missing = sorted(set(order) - glyphs), sorted(glyphs - set(order))
        problems.append(f"glyph set differs from the encoding: extra {extra[:5]}, missing {missing[:5]}")

    if font["head"].unitsPerEm != 1000:
        problems.append(f"unitsPerEm is {font['head'].unitsPerEm}, expected 1000")
    hhea, os2 = font["hhea"], font["OS/2"]
    quadrat = scaled(1000)
    if hhea.ascent < quadrat or hhea.descent >= 0:
        problems.append(f"the vertical metrics {hhea.ascent}/{hhea.descent} do not hold one quadrat of {quadrat}")
    for name, (adv, _) in font["hmtx"].metrics.items():
        if name in forms:
            e, v = forms[name]
            bw = e["box"][v][0]
            want = scaled(min(1000, round(10 * bw) + 80))
            if adv != want:
                problems.append(f"{name} has advance {adv}, expected {want}")
        elif name in EMPTY and adv != 0:
            problems.append(f"{name} must have zero advance")

    for name in order:
        g = glyf[name]
        if name in EMPTY or name == enc["space"]["glyph"]:
            if g.numberOfContours != 0:
                problems.append(f"{name} must be empty")
            continue
        if g.numberOfContours <= 0:
            problems.append(f"{name} has no outline")
            continue
        areas = area(list(g.coordinates), list(g.endPtsOfContours))
        if max(areas, key=abs) >= 0:
            problems.append(f"{name} has an outer contour that does not run clockwise")
        if g.yMax > os2.usWinAscent or -g.yMin > os2.usWinDescent:
            problems.append(f"{name} leaves the win metrics")

    maps, bad = lookup_maps(font)
    problems += bad
    if "GPOS" in font:
        problems.append("the font carries positioning; no sign should need it")
    for name, (e, v) in forms.items():
        if v == "a":
            continue
        base = gname(e["id"], "a")
        tag = "ss01" if v == "b" else "ss02"
        if name not in maps.get(tag, {}).get(base, []):
            problems.append(f"{name} is not reached from {base} by {tag}")
        if name not in maps.get("salt", {}).get(base, []):
            problems.append(f"{name} is not reached from {base} by salt")
    for tag in ("ss01", "ss02"):
        for base, subs in maps.get(tag, {}).items():
            if len(subs) != 1:
                problems.append(f"{tag} has {len(subs)} substitutions for {base}")
    if maps.get("ccmp") != {"ignorable": ["ignorable.sub"]}:
        problems.append("ccmp is not the single ignorable substitution")

    data = path.read_bytes()
    text = "".join(chr(cp(c)) for c in enc["ignorables"]["codepoints"])
    for glyph, advance in shape(data, text, order):
        if glyph == enc["space"]["glyph"] or advance != 0 or glyf[glyph].numberOfContours != 0:
            problems.append(f"a default-ignorable shapes to {glyph} with advance {advance}")

    names = {n.nameID: n.toUnicode() for n in font["name"].names if n.platformID == 3}
    expect = {
        1: "Khelathi Zethu Glyphs",
        13: "SIL Open Font License 1.1",
        14: "https://openfontlicense.org",
    }
    for nid, value in expect.items():
        if names.get(nid) != value:
            problems.append(f"name {nid} is {names.get(nid)!r}, expected {value!r}")
    if 7 in names:
        problems.append("name table carries a trademark")
    if not names.get(0, "").startswith("Copyright"):
        problems.append("name table carries no copyright line")

    woff2 = path.with_suffix(".woff2")
    if not woff2.exists():
        problems.append(f"{woff2} missing")
    elif TTFont(str(woff2)).getGlyphOrder() != order:
        problems.append("woff2 glyph order differs from the ttf")
    print(f"{path}: {len(cmap)} code points mapped over {len(order)} glyphs")
    return problems


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "fonts" / "KhelathiZethuGlyphs-Regular.ttf"
    problems = check(path)
    for p in problems:
        print(f"{path}: error: {p}")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
