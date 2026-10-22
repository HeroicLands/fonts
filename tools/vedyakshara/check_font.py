# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Load the built font and confirm it matches tools/vedyakshara/encoding.json.

    .venv/bin/python tools/vedyakshara/check_font.py [fonts/VedyaksharaClassical-Regular.ttf]

- **The character map** is exactly the encoding: the consonants, the independent
  vowels, the vowel signs, the cut, the soft dot, the digits and the two bars on
  their code points, the space, the default-ignorables on one empty glyph, and
  every code point of the Latin ranges on the box (tools/notdef_box.py), so a Latin
  letter prints the box.
- **The glyphs.** Every glyph but the space and the ignorables has an outline.
  Every consonant, _fa_ and fused sign has its half and final forms, and every one
  but _ra_, the fused signs ending in _r_ and the consonants that fuse with _r_ its
  r-foot form; every mark has no
  advance and is a mark in GDEF, every sign and form a base.
- **The features reach every glyph.** Each form is what shaping gives its sign in
  its place: _fa_ from _pa_ and the soft dot, a fused sign from its pair and the
  cut, the half form before a consonant, the final form at the end, the r-foot
  form before _ra_. Each flag and hook stands at its sign's anchor, and each hook's
  neck reaches the lowest ink of the body above it. A vowel sign, the cut or the
  soft dot after a space is the box. The ignorables shape to nothing.
- **The name table** carries the licence, and the .woff2 beside the .ttf carries
  the same glyphs.
"""

import json
import sys
from pathlib import Path

import uharfbuzz as hb
from fontTools.pens.pointInsidePen import PointInsidePen
from fontTools.ttLib import TTFont

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import font_names  # noqa: E402
import notdef_box  # noqa: E402

ENCODING = HERE / "encoding.json"
FAMILY = "Vedyakshara Classical"
EMPTY_BY_DESIGN = {"space", "ignorable", "ignorable.sub"}
MARK_PREFIXES = ("vs.", "flag.", "hook.")


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
    return [(order[i.codepoint], p.x_offset, p.x_advance) for i, p in zip(buf.glyph_infos, buf.glyph_positions)]


def names(font, order, text):
    return [n for n, _, _ in shape(font, order, text)]


def touches(glyphset, name, x, y) -> bool:
    """Whether the sign's ink covers a point within a reed's half-width of (x, y)."""
    for dy in range(-8, 28, 4):
        pen = PointInsidePen(glyphset, (x, y + dy))
        glyphset[name].draw(pen)
        if pen.getResult():
            return True
    return False


def check(path: Path) -> list[str]:
    problems = []
    enc = json.loads(ENCODING.read_text(encoding="utf-8"))
    font = TTFont(str(path))
    order = font.getGlyphOrder()
    present = set(order)
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

    cons = [g["glyph"] for g in enc["glyphs"] if g["kind"] == "consonant"]
    fused = {f["glyph"]: f["parts"] for f in enc["fused"]}
    bases = cons + ["fa"] + list(fused)
    c_r = {f for f, (a, b) in fused.items() if b == "ra"}
    rfoot = [b for b in bases if b != "ra" and b not in c_r and f"{b[:-1]}ra" not in c_r]
    marks = [n for n in order if n.startswith(MARK_PREFIXES) or n in ("cut", "dot")]
    classes = font["GDEF"].table.GlyphClassDef.classDefs if "GDEF" in font else {}
    for name in marks:
        if hmtx[name][0] != 0:
            problems.append(f"{name} has advance {hmtx[name][0]}, expected 0")
        if classes.get(name) != 3:
            problems.append(f"{name} is not a mark in GDEF")
    forms = bases + [f"{b}.{f}" for b in bases for f in ("half", "final")] + [f"{b}.rfoot" for b in rfoot]
    for name in forms:
        if name not in present:
            problems.append(f"the form {name} is missing")
        elif classes.get(name) != 1:
            problems.append(f"{name} is not a base in GDEF")
    for table in ("GSUB", "GPOS"):
        if table not in font:
            problems.append(f"the font has no {table}; the forms and the marks need it")
    if problems:
        return problems

    hbf = hb.Font(hb.Face(path.read_bytes()))
    gs = font.getGlyphSet()
    char = {g["glyph"]: chr(int(g["codepoint"][2:], 16)) for g in enc["glyphs"]}
    cut, ja, ra = char["cut"], char["ja"], char["ra"]

    def text_of(base: str) -> str:
        if base == "fa":
            return char["pa"] + char["dot"]
        if base in fused:
            a, b = fused[base]
            return char[a] + cut + char[b]
        return char[base]

    for b in bases:
        t = text_of(b)
        cases = [(t, [b]), (t + cut + ja, [f"{b}.half", "ja"]), (t + cut, [f"{b}.final"])]
        if b in rfoot:
            cases.append((t + cut + ra, [f"{b}.rfoot"]))
        for text, expect in cases:
            got = names(hbf, order, text)
            if got != expect:
                problems.append(f"{b} in place shapes to {got}, expected {expect}")

    # the vowel signs on every sign that carries them
    gpos = {}
    for b in bases + [f"{x}.rfoot" for x in rfoot]:
        t = text_of(b.split(".")[0]) + (cut + ra if b.endswith(".rfoot") else "")
        for v, parts in (("vs.i", ["flag.i"]), ("vs.e", ["flag.e"]), ("vs.u", ["hook.u"]), ("vs.o", ["hook.o"]),
                         ("vs.ai", ["flag.e", "flag.i"]), ("vs.au", ["hook.o", "hook.u"])):
            run = shape(hbf, order, t + char[v])
            got = [n for n, _, _ in run]
            if got[0] != b or len(got) != 1 + len(parts):
                problems.append(f"{b} with {v} shapes to {got}")
                continue
            adv = run[0][2]
            for (name, off, _), part in zip(run[1:], parts):
                x = off + adv  # the mark's place on its sign
                if x > adv - 10:
                    problems.append(f"{b} with {v}: {name} stands at x {x}, at the end of its sign, not on its anchor")
                    continue
                if v in ("vs.i", "vs.e"):
                    if name != v:
                        problems.append(f"{b} with {v} shapes to {got}")
                    continue
                if not name.startswith(part):
                    problems.append(f"{b} with {v} shapes to {got}, expected {part}")
                    continue
                gpos[(b, name.split(".")[1])] = x
                if part.startswith("hook"):
                    neck = int(name.rsplit(".", 1)[1])
                    if not touches(gs, b, x, neck):
                        problems.append(f"{b}: the {part} neck starts at {neck}, clear of the body's ink at x {x}")

    # a mark with nothing to carry it, after a space, is the box
    for m in ("vs.i", "vs.u", "vs.ai", "cut", "dot"):
        got = names(hbf, order, " " + char[m])
        if got != ["space", notdef_box.BOX]:
            problems.append(f"{m} after a space shapes to {got}, expected the box")

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
    print(f"{path}: {len(cmap)} code points mapped over {len(order)} glyphs, {len(gpos)} vowel places")
    return problems


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE.parent.parent / "fonts" / "VedyaksharaClassical-Regular.ttf"
    problems = check(path)
    for p in problems:
        print(f"{path}: error: {p}")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
