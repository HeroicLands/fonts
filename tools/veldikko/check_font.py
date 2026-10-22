# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Load the built font and confirm it matches tools/veldikko/encoding.json.

    .venv/bin/python tools/veldikko/check_font.py [fonts/Veldikko-Regular.ttf]

- **The character map** is exactly the encoding: the letters, the vowel marks and
  the signs of length, pitch, emphasis and doubling on their right-to-left code
  points, the space, the default-ignorables on one empty glyph, and every code point
  of the Latin ranges on the box (tools/notdef_box.py), so a Latin letter prints the
  box.
- **The glyphs.** Every glyph but the space and the ignorables has an outline. Every
  letter has its isolated, initial, medial and final forms and its stretched
  initial and medial, and a nasal its long tails; every mark has no advance and is
  a mark in GDEF, every letter form a base.
- **The features reach every glyph.** Each form is what shaping gives the letter in
  its place: medial between two letters, initial before one, final after one, and
  stretched under a long vowel; each tail is what ``ss01`` or ``ss02`` gives a
  word's last nasal; each precomposed vowel is what a vowel and its signs shape to.
  The ignorables shape to nothing.
- **The name table** carries the licence, and the .woff2 beside the .ttf carries
  the same glyphs.
"""

import json
import sys
from pathlib import Path

import uharfbuzz as hb
from fontTools.ttLib import TTFont

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import font_names  # noqa: E402
import notdef_box  # noqa: E402

ENCODING = HERE / "encoding.json"
EMPTY_BY_DESIGN = {"space", "ignorable", "ignorable.sub"}
FORMS = ("init", "medi", "fina", "init.wide", "medi.wide")
NASALS = ("m", "n", "ng")
TAILS = {"sweep": "ss01", "ezh": "ss02"}
MODIFIERS = ("long", "rise", "fall", "emph")


def expected_cmap(enc) -> dict[int, str]:
    cmap = {int(g["codepoint"][2:], 16): g["glyph"] for g in enc["glyphs"]}
    cmap[0x20] = cmap[0xA0] = enc["space"]["glyph"]
    for cp in enc["ignorables"]["codepoints"]:
        cmap[int(cp[2:], 16)] = enc["ignorables"]["glyph"]
    for cp in notdef_box.codepoints():
        cmap.setdefault(cp, notdef_box.BOX)
    return cmap


def shape(font: hb.Font, order, text: str, features=None) -> list[str]:
    buf = hb.Buffer()
    buf.add_str(text)
    buf.direction = "rtl"
    buf.script = "Zyyy"
    hb.shape(font, buf, features or {})
    return [order[i.codepoint] for i in buf.glyph_infos]


def check(path: Path) -> list[str]:
    problems = []
    enc = json.loads(ENCODING.read_text(encoding="utf-8"))
    font = TTFont(str(path))
    order = font.getGlyphOrder()
    names = set(order)
    glyf, hmtx = font["glyf"], font["hmtx"]
    cmap = font.getBestCmap()
    want = expected_cmap(enc)
    for cp in sorted(set(want) | set(cmap)):
        if cmap.get(cp) != want.get(cp):
            problems.append(f"U+{cp:04X} maps to {cmap.get(cp)}, expected {want.get(cp)}")
    for ch in "AZaz'’":
        if cmap.get(ord(ch)) != notdef_box.BOX:
            problems.append(f"{ch!r} is {cmap.get(ord(ch))}; Latin text and the apostrophe must be {notdef_box.BOX}")
    problems += [line.split(": error: ", 1)[1] for line in notdef_box.check(path)]
    problems += [line.split(": error: ", 1)[1] for line in font_names.check(path)]

    for name in order:
        if name in (".notdef", notdef_box.BOX) or name in EMPTY_BY_DESIGN:
            continue
        if glyf[name].numberOfContours == 0:
            problems.append(f"{name} has no outline")
    for name in EMPTY_BY_DESIGN - {"space"}:
        if glyf[name].numberOfContours != 0 or hmtx[name][0] != 0:
            problems.append(f"{name} must be empty with zero advance")

    letters = [g for g in enc["glyphs"] if g["kind"] == "letter"]
    marks = [n for n in order if n.startswith("vowel.") or n in MODIFIERS or n == "bar"]
    classes = font["GDEF"].table.GlyphClassDef.classDefs if "GDEF" in font else {}
    for name in marks:
        if hmtx[name][0] != 0:
            problems.append(f"{name} has advance {hmtx[name][0]}, expected 0")
        if classes.get(name) != 3:
            problems.append(f"{name} is not a mark in GDEF")
    for g in letters:
        forms = [g["glyph"]] + [f"{g['glyph']}.{f}" for f in FORMS]
        if g["glyph"] in NASALS:
            forms += [f"{g['glyph']}{part}.{t}" for t in TAILS for part in ("", ".fina")]
        for name in forms:
            if name not in names:
                problems.append(f"the form {name} is missing")
            elif classes.get(name) != 1:
                problems.append(f"{name} is not a base in GDEF")
    for table in ("GSUB", "GPOS"):
        if table not in font:
            problems.append(f"the font has no {table}; the joining and the marks need it")
    if problems:
        return problems

    hbf = hb.Font(hb.Face(path.read_bytes()))
    char = {g["glyph"]: chr(int(g["codepoint"][2:], 16)) for g in enc["glyphs"]}
    t, a = char["t"], char["vowel.a"]
    for g in letters:
        c = char[g["glyph"]]
        n = g["glyph"]
        # In the run a word's last letter comes first.
        cases = [
            (c + t, ["t.fina", f"{n}.init"]),
            (t + c + t, ["t.fina", f"{n}.medi", "t.init"]),
            (t + c, [f"{n}.fina", "t.init"]),
            (c + a + char["long"] + t, ["t.fina", "vowel.a.long", f"{n}.init.wide"]),
            (t + c + a + char["rise"] + t, ["t.fina", "vowel.a.rise", f"{n}.medi.wide", "t.init"]),
        ]
        for text, expect in cases:
            got = shape(hbf, order, text)
            if got != expect:
                problems.append(f"{n} in place shapes to {got}, expected {expect}")
        if n in NASALS:
            for tail, tag in TAILS.items():
                for text, expect in ((c, [f"{n}.{tail}"]), (t + c, [f"{n}.fina.{tail}", "t.init"])):
                    got = shape(hbf, order, text, {tag: True})
                    if got != expect:
                        problems.append(f"{n} with {tag} shapes to {got}, expected {expect}")
    vowels = [g for g in enc["glyphs"] if g["kind"] == "vowel"]
    for v in vowels:
        for name in order:
            if not name.startswith(v["glyph"] + ".") or name == v["glyph"]:
                continue
            mods = name[len(v["glyph"]) + 1:].split(".")
            text = t + char[v["glyph"]] + "".join(char[m] for m in mods)
            got = shape(hbf, order, text)
            if got != [name, "t"]:
                problems.append(f"{v['glyph']} with {', '.join(mods)} shapes to {got}, expected {name}")

    ign = "".join(chr(int(c[2:], 16)) for c in enc["ignorables"]["codepoints"])
    buf = hb.Buffer()
    buf.add_str(ign)
    buf.direction = "rtl"
    buf.script = "Zyyy"
    hb.shape(hbf, buf)
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        name = order[info.codepoint]
        if name == "space" or pos.x_advance != 0 or glyf[name].numberOfContours != 0:
            problems.append(f"a default-ignorable shapes to {name} with advance {pos.x_advance}")

    table = {n.nameID: n.toUnicode() for n in font["name"].names if n.platformID == 3}
    for nid, value in {1: "Veldikko", 13: "SIL Open Font License 1.1", 14: "https://openfontlicense.org"}.items():
        if table.get(nid) != value:
            problems.append(f"name {nid} is {table.get(nid)!r}, expected {value!r}")
    if 7 in table:
        problems.append("name table carries a trademark")
    if not table.get(0, "").startswith("Copyright"):
        problems.append("name table carries no copyright line")

    woff2 = path.with_suffix(".woff2")
    if not woff2.exists():
        problems.append(f"{woff2} missing")
    elif TTFont(str(woff2)).getGlyphOrder() != order:
        problems.append("woff2 glyph order differs from the ttf")
    print(f"{path}: {len(cmap)} code points mapped over {len(order)} glyphs")
    return problems


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE.parent.parent / "fonts" / "Veldikko-Regular.ttf"
    problems = check(path)
    for p in problems:
        print(f"{path}: error: {p}")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
