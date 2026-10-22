# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Load the built font and confirm every mapped character has a glyph.

    .venv/bin/python tools/thuravark-carved/check_font.py [fonts/ThuravarkCarved-Regular.ttf]

Every code point in the cmap must name a glyph in the glyph order, and the glyph
must carry an outline unless it is one of the few that draw nothing by design.
Every other character, Latin included, must map to the box (tools/notdef_box.py):
the face draws its own code points alone, which tools/codepoints.py checks.
The name table must carry the family, version and licence, and the .woff2 beside
the .ttf must open and carry the same glyphs. The imperial recension is present:
the three diphthong staves and the two crown marks draw, every glyph a crown may
hold has its crowned form and each post its joined form, the bound runes draw,
and the GSUB carries ``ss01`` and ``rclt``.
"""

import sys
from pathlib import Path

from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import crown  # noqa: E402
import font_names  # noqa: E402
import notdef_box  # noqa: E402

EMPTY_BY_DESIGN = {"space", "acutecomb", "ignorable", "ignorable.sub"}
IGNORABLES = [*range(0x200B, 0x2010), *range(0x202A, 0x202F), *range(0x2066, 0x206A), 0xFEFF]

# Latin text is not the face's: every Latin letter, digit and mark draws the box,
# and the space is the only character the face shares with it.
LATIN = "0123456789-.,!?;:\"'()<>[]@#$%^&abdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZáéíóú"
STAVES = ("a e i o u p b f v t d th dh k g kh gh s z h l r hl m n ng j w ai au oi").split()
BOUND = "e_n e_l a_r a_l m_a z_a k_a u_r l_m l_th".split()
CROWN = {0xF0150: "crown.open", 0xF0151: "crown.close"}


def check(path: Path) -> list[str]:
    problems = []
    font = TTFont(str(path))
    order = set(font.getGlyphOrder())
    glyf = font["glyf"]
    cmap = font.getBestCmap()
    if not cmap:
        return ["no Unicode cmap"]
    for cp, name in sorted(cmap.items()):
        if name not in order:
            problems.append(f"U+{cp:04X} maps to {name}, which is not in the font")
        elif name not in EMPTY_BY_DESIGN and glyf[name].numberOfContours == 0:
            problems.append(f"U+{cp:04X} maps to {name}, which has no outline")
    if cmap.get(0x20) != "space":
        problems.append(f"U+0020 maps to {cmap.get(0x20)}, not space")
    for ch in LATIN:
        if cmap.get(ord(ch)) != notdef_box.BOX:
            problems.append(f"{ch!r} maps to {cmap.get(ord(ch))}; Latin text draws {notdef_box.BOX}")
    for name in STAVES:
        if name not in order or glyf[name].numberOfContours == 0:
            problems.append(f"the stave {name} is missing or draws nothing")
    for name in BOUND:
        if name not in order or glyf[name].numberOfContours == 0:
            problems.append(f"the bound rune {name} is missing or draws nothing")
    for cp, name in CROWN.items():
        if cmap.get(cp) != name:
            problems.append(f"U+{cp:04X} maps to {cmap.get(cp)}, not {name}")
        if name + crown.RAIL not in order or glyf.get(name + crown.RAIL) is None or glyf[name + crown.RAIL].numberOfContours == 0:
            problems.append(f"{name + crown.RAIL} is missing or draws nothing")
    for name in crown.inside(font.getGlyphOrder()):
        if name + crown.CROWNED not in order:
            problems.append(f"{name} has no crowned form {name + crown.CROWNED}")
    tags = {r.FeatureTag for r in font["GSUB"].table.FeatureList.FeatureRecord} if "GSUB" in font else set()
    for tag in ("ss01", "rclt"):
        if tag not in tags:
            problems.append(f"no {tag} feature")
    for name in EMPTY_BY_DESIGN:
        if name not in order:
            problems.append(f"{name} is missing")
        elif glyf[name].numberOfContours != 0:
            problems.append(f"{name} draws something")
    hmtx = font["hmtx"]
    for name in ("space", "acutecomb", "ignorable", "ignorable.sub"):
        if hmtx[name][0] != 0:
            problems.append(f"{name} has width {hmtx[name][0]}, expected 0")
    for cp in IGNORABLES:
        if cmap.get(cp) != "ignorable":
            problems.append(f"U+{cp:04X} must map to the empty glyph 'ignorable'")
    problems += [line.split(": error: ", 1)[1] for line in notdef_box.check(path)]
    problems += [line.split(": error: ", 1)[1] for line in font_names.check(path)]
    for name in ("GSUB",):
        if name not in font:
            problems.append(f"no {name} table")
    names = {n.nameID: n.toUnicode() for n in font["name"].names if n.platformID == 3}
    expect = {
        1: "Thuravark Carved",
        2: "Regular",
        4: "Thuravark Carved Regular",
        5: "Version 0.1",
        6: "ThuravarkCarved-Regular",
        13: "SIL Open Font License 1.1",
        14: "https://openfontlicense.org",
    }
    for nid, value in expect.items():
        if names.get(nid) != value:
            problems.append(f"name {nid} is {names.get(nid)!r}, expected {value!r}")
    copyright_line = (ROOT / "LICENSE").read_text(encoding="utf-8").splitlines()[0].strip()
    if names.get(0) != copyright_line:
        problems.append(f"name 0 is {names.get(0)!r}, expected {copyright_line!r}")
    if 7 in names:
        problems.append("name table carries a trademark")
    woff2 = path.with_suffix(".woff2")
    if not woff2.exists():
        problems.append(f"{woff2} missing")
    else:
        w = TTFont(str(woff2))
        if w.getGlyphOrder() != font.getGlyphOrder():
            problems.append("woff2 glyph order differs from the ttf")
        if w.getBestCmap() != cmap:
            problems.append("woff2 cmap differs from the ttf")
    print(f"{path}: {len(cmap)} code points mapped over {len(order)} glyphs")
    return problems


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "fonts" / "ThuravarkCarved-Regular.ttf"
    problems = check(path)
    for p in problems:
        print(f"{path}: error: {p}")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
