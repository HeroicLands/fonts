# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Load the built font and confirm it matches tools/qalezu/encoding.json.

    .venv/bin/python tools/qalezu/check_font.py [fonts/Qalezu-Regular.ttf]

The cmap is exactly the encoding: the signs, digits and marks on their
right-to-left code points, the space, and the default-ignorable characters on
one empty glyph, and every code point of the Latin ranges on the box
(tools/notdef_box.py), so a Latin letter prints the box. Every drawn glyph has an outline,
the unencoded bar, dab and catchdots components have zero advance, every doubled
consonant is its sign with the bar drawn in, the win metrics enclose every glyph
(the box guard checks it), and every catch-before form is its
sign or doubled sign with three more dabs drawn above it, all at the sign's own
advance, so no mark positioning is needed. The ignorables shape to nothing. The name table carries the licence, and the .woff2
beside the .ttf carries the same glyphs.
"""

import json
import sys
from pathlib import Path

import uharfbuzz as hb
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.ttLib import TTFont

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import notdef_box  # noqa: E402

ENCODING = Path(__file__).resolve().parent / "encoding.json"
COMPONENTS = {"doubling", "dab", "catchdots"}
EMPTY_BY_DESIGN = {"space", "ignorable", "ignorable.sub"}


def expected_cmap() -> dict[int, str]:
    enc = json.loads(ENCODING.read_text(encoding="utf-8"))
    cmap = {int(g["codepoint"][2:], 16): g["glyph"] for g in enc["glyphs"]}
    cmap[int(enc["space"]["codepoint"][2:], 16)] = enc["space"]["glyph"]
    ign = enc["ignorables"]
    for cp in ign["codepoints"]:
        cmap[int(cp[2:], 16)] = ign["glyph"]
    for cp in notdef_box.codepoints():
        cmap.setdefault(cp, notdef_box.BOX)
    return cmap


def shape(font_bytes: bytes, text: str, order: list[str]) -> list[tuple[str, int]]:
    font = hb.Font(hb.Face(font_bytes))
    font.scale = (1000, 1000)
    buf = hb.Buffer()
    buf.add_str(text)
    buf.direction = "rtl"
    buf.script = "Zyyy"
    hb.shape(font, buf)
    return [(order[i.codepoint], p.x_advance) for i, p in zip(buf.glyph_infos, buf.glyph_positions)]


def check(path: Path) -> list[str]:
    problems = []
    font = TTFont(str(path))
    order = font.getGlyphOrder()
    glyf = font["glyf"]
    cmap = font.getBestCmap()
    want = expected_cmap()
    for cp in sorted(set(want) | set(cmap)):
        if cmap.get(cp) != want.get(cp):
            problems.append(f"U+{cp:04X} maps to {cmap.get(cp)}, expected {want.get(cp)}")
    for ch in "AZaz'’":
        if cmap.get(ord(ch)) != notdef_box.BOX:
            problems.append(f"{ch!r} is {cmap.get(ord(ch))}; Latin text and the apostrophe must be {notdef_box.BOX}")
    problems += [line.split(": error: ", 1)[1] for line in notdef_box.check(path)]

    for name in order:
        if name in (".notdef", notdef_box.BOX) or name in EMPTY_BY_DESIGN:
            continue
        if glyf[name].numberOfContours == 0:
            problems.append(f"{name} has no outline")
    for name in EMPTY_BY_DESIGN - {"space"}:
        if glyf[name].numberOfContours != 0 or font["hmtx"][name][0] != 0:
            problems.append(f"{name} must be empty with zero advance")
    for name in COMPONENTS:
        if font["hmtx"][name][0] != 0:
            problems.append(f"{name} has advance {font['hmtx'][name][0]}, expected 0")
    classes = font["GDEF"].table.GlyphClassDef.classDefs if "GDEF" in font else {}
    for name in COMPONENTS:
        if classes.get(name) != 3:
            problems.append(f"{name} is not a mark in GDEF")

    enc = json.loads(ENCODING.read_text(encoding="utf-8"))
    glyphs = font.getGlyphSet()

    def bounds(name: str):
        pen = BoundsPen(glyphs)
        glyphs[name].draw(pen)
        return pen.bounds

    def contours(name: str) -> int:
        pen = DecomposingRecordingPen(glyphs)
        glyphs[name].draw(pen)
        return sum(1 for op, _ in pen.value if op == "closePath")

    for g in enc["glyphs"]:
        if g["kind"] != "doubled":
            continue
        name, base = g["glyph"], g["base"]
        if name not in order:
            problems.append(f"the doubled sign {name} is missing")
            continue
        if font["hmtx"][name][0] != font["hmtx"][base][0]:
            problems.append(f"{name} has advance {font['hmtx'][name][0]}, its sign {base} has {font['hmtx'][base][0]}")
        if contours(name) <= contours(base):
            problems.append(f"{name} draws no bar beyond {base}")
    for g in enc["glyphs"]:
        if g["kind"] != "catchbefore":
            continue
        name, base = g["glyph"], g["base"]
        if name not in order:
            problems.append(f"the catch-before form {name} is missing")
            continue
        if font["hmtx"][name][0] != font["hmtx"][base][0]:
            problems.append(f"{name} has advance {font['hmtx'][name][0]}, its sign {base} has {font['hmtx'][base][0]}")
        if contours(name) != contours(base) + 3:
            problems.append(f"{name} draws {contours(name)} contours, expected the {contours(base)} of {base} and three dabs")
        if bounds(name)[3] <= bounds(base)[3]:
            problems.append(f"{name} draws nothing above {base}")
    if "GPOS" in font:
        problems.append("the font carries mark positioning; no sign should need it")

    data = path.read_bytes()
    ign = enc["ignorables"]
    text = "".join(chr(int(c[2:], 16)) for c in ign["codepoints"])
    for glyph, advance in shape(data, text, order):
        if glyph == "space" or advance != 0 or glyf[glyph].numberOfContours != 0:
            problems.append(f"a default-ignorable shapes to {glyph} with advance {advance}")
    sample = "".join(chr(int(g["codepoint"][2:], 16)) for g in enc["glyphs"])
    shaped = [g for g, _ in shape(data, sample, order)]
    if ".notdef" in shaped or len(shaped) != len(sample):
        problems.append("a mapped sign shapes to .notdef or changes the glyph count")

    names = {n.nameID: n.toUnicode() for n in font["name"].names if n.platformID == 3}
    expect = {
        1: "Qalezu",
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
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else (
        Path(__file__).resolve().parent.parent.parent / "fonts" / "Qalezu-Regular.ttf"
    )
    problems = check(path)
    for p in problems:
        print(f"{path}: error: {p}")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
