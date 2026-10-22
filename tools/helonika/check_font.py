# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Load the built font and confirm it matches tools/helonika/encoding.json.

    .venv/bin/python tools/helonika/check_font.py [fonts/HelonikaBook-Regular.ttf]

- **The character map** is exactly the encoding: the capitals, the small letters,
  the long vowels, the digits, the raised dot, the register-mark and the accent on
  their code points, the space, the default-ignorables on one empty glyph, and
  every code point of the Latin ranges on the box (tools/notdef_box.py), so a Latin
  letter prints the box.
- **The glyphs.** Every glyph but the space and the ignorables has an outline. The
  accent has no advance and is a mark in GDEF; every other character is a base.
- **The accent.** After every vowel, capital or small, it stands over the vowel's
  ink, higher over a capital than over a minuscule. After a consonant, a digit, a
  point or a space it is the box. The ignorables shape to nothing.
- **The name table** carries the licence, and the .woff2 beside the .ttf carries
  the same glyphs.
"""

import json
import sys
from pathlib import Path

import uharfbuzz as hb
from fontTools.pens.boundsPen import BoundsPen
from fontTools.ttLib import TTFont

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import font_names  # noqa: E402
import notdef_box  # noqa: E402

ENCODING = HERE / "encoding.json"
FAMILY = "Helonika Book"
EMPTY_BY_DESIGN = {"space", "ignorable", "ignorable.sub"}
VOWELS = "A E E.long I O O.long U A.macron I.macron U.macron".split()
VOWELS += [v.lower() for v in VOWELS]


def expected_cmap(enc) -> dict[int, str]:
    cmap = {int(g["codepoint"][2:], 16): g["glyph"] for g in enc["glyphs"]}
    cmap[0x20] = cmap[0xA0] = enc["space"]["glyph"]
    for cp in enc["ignorables"]["codepoints"]:
        cmap[int(cp[2:], 16)] = enc["ignorables"]["glyph"]
    for cp in notdef_box.codepoints():
        cmap.setdefault(cp, notdef_box.BOX)
    return cmap


def shape(font: hb.Font, order, text: str):
    buf = hb.Buffer()
    buf.add_str(text)
    buf.direction = "ltr"
    buf.script = "Zyyy"
    hb.shape(font, buf, {})
    return [(order[i.codepoint], p.x_offset, p.y_offset, p.x_advance) for i, p in zip(buf.glyph_infos, buf.glyph_positions)]


def ink(glyphset, name):
    pen = BoundsPen(glyphset)
    glyphset[name].draw(pen)
    return pen.bounds


def check(path: Path) -> list[str]:
    problems = []
    enc = json.loads(ENCODING.read_text(encoding="utf-8"))
    font = TTFont(str(path))
    order = font.getGlyphOrder()
    glyf, hmtx = font["glyf"], font["hmtx"]
    cmap = font.getBestCmap()
    want = expected_cmap(enc)
    for cp in sorted(set(want) | set(cmap)):
        if cmap.get(cp) != want.get(cp):
            problems.append(f"U+{cp:04X} maps to {cmap.get(cp)}, expected {want.get(cp)}")
    for ch in "AZaz'’?!§":
        if cmap.get(ord(ch)) != notdef_box.BOX:
            problems.append(f"{ch!r} is {cmap.get(ord(ch))}; Latin text and punctuation must be {notdef_box.BOX}")
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

    classes = font["GDEF"].table.GlyphClassDef.classDefs if "GDEF" in font else {}
    for r in enc["glyphs"]:
        name = r["glyph"]
        if r["kind"] == "mark":
            if hmtx[name][0] != 0:
                problems.append(f"{name} has advance {hmtx[name][0]}, expected 0")
            if classes.get(name) != 3:
                problems.append(f"{name} is not a mark in GDEF")
        elif classes.get(name) != 1:
            problems.append(f"{name} is not a base in GDEF")
    for table in ("GSUB", "GPOS"):
        if table not in font:
            problems.append(f"the font has no {table}; the accent needs it")
    if problems:
        return problems

    hbf = hb.Font(hb.Face(path.read_bytes()))
    gs = font.getGlyphSet()
    char = {g["glyph"]: chr(int(g["codepoint"][2:], 16)) for g in enc["glyphs"]}
    accent = char["accent"]
    acc_box = ink(gs, "accent")
    placed = 0
    for v in VOWELS:
        run = shape(hbf, order, char[v] + accent)
        got = [n for n, *_ in run]
        if got != [v, "accent"]:
            problems.append(f"{v} with the accent shapes to {got}")
            continue
        _, x_off, y_off, adv = run[1]
        base = ink(gs, v)
        x = run[0][3] + x_off  # the accent's origin, relative to the vowel's: the pen stands past the vowel
        mid = (acc_box[0] + acc_box[2]) / 2 + x
        if not base[0] <= mid <= base[2]:
            problems.append(f"{v}: the accent's middle stands at x {mid:.0f}, off the vowel's ink {base[0]:.0f}..{base[2]:.0f}")
        bottom = acc_box[1] + y_off
        if bottom < base[3] + 10:
            problems.append(f"{v}: the accent's foot at y {bottom:.0f} is not clear above the vowel's ink at {base[3]:.0f}")
        placed += 1
    for other in ("k", "T", "num.3", "raisedDot", "registerMark"):
        got = [n for n, *_ in shape(hbf, order, char[other] + accent)]
        if got != [other, notdef_box.BOX]:
            problems.append(f"the accent after {other} shapes to {got}, expected the box")
    got = [n for n, *_ in shape(hbf, order, " " + accent)]
    if got != ["space", notdef_box.BOX]:
        problems.append(f"the accent after a space shapes to {got}, expected the box")

    ign = "".join(chr(int(c[2:], 16)) for c in enc["ignorables"]["codepoints"])
    buf = hb.Buffer()
    buf.add_str(ign)
    buf.direction = "ltr"
    buf.script = "Zyyy"
    hb.shape(hbf, buf)
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        name = order[info.codepoint]
        if name == "space" or pos.x_advance != 0 or glyf[name].numberOfContours != 0:
            problems.append(f"a default-ignorable shapes to {name} with advance {pos.x_advance}")

    table = {n.nameID: n.toUnicode() for n in font["name"].names if n.platformID == 3}
    for nid, value in {1: FAMILY, 13: "SIL Open Font License 1.1", 14: "https://openfontlicense.org"}.items():
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
    print(f"{path}: {len(cmap)} code points mapped over {len(order)} glyphs, the accent placed on {placed} vowels")
    return problems


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE.parent.parent / "fonts" / "HelonikaBook-Regular.ttf"
    problems = check(path)
    for p in problems:
        print(f"{path}: error: {p}")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
