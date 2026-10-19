# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Load the built font and confirm every mapped character has a glyph.

    .venv/bin/python thuravark/src/check_font.py [thuravark/fonts/ThuravarkRunic-Regular.ttf]

Every code point in the cmap must name a glyph in the glyph order, and the glyph
must carry an outline unless it is one of the few that draw nothing by design.
The name table must carry the family, version and licence, and the .woff2 beside
the .ttf must open and carry the same glyphs.
"""

import sys
from pathlib import Path

from fontTools.ttLib import TTFont

HERE = Path(__file__).resolve().parent.parent
EMPTY_BY_DESIGN = {"space", "hyphen", "blank", "acutecomb"}

# What the owner's rulings say these keys type, independent of the glyph source.
RULED = {
    **{str(i): f"num.{i}" for i in range(10)},
    " ": "space",
    "-": "hyphen",
    ".": "period",
    **{k: "blank" for k in ",!?;:\"'()<>[]@#$%^&"},
    "j": "j",
    "y": "y",
    "J": "j",
    "Y": "y",
    "w": "w",
    "c": "stele",
    "q": "stele",
    "x": "stele",
    "́": "acutecomb",
    **dict(zip("áéíóú", ["aacute", "eacute", "iacute", "oacute", "uacute"])),
}
RULED.update({ch: ch for ch in "abdefghiklmnoprstuvz"})
STAVES = ("a e i o u p b f v t d th dh k g kh gh s z h l r hl m n ng j w").split()


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
    for ch, name in RULED.items():
        if cmap.get(ord(ch)) != name:
            problems.append(f"{ch!r} should type {name}, types {cmap.get(ord(ch))}")
    for name in STAVES:
        if name not in order or glyf[name].numberOfContours == 0:
            problems.append(f"the stave {name} is missing or draws nothing")
    for name in EMPTY_BY_DESIGN:
        if name not in order:
            problems.append(f"{name} is missing")
        elif glyf[name].numberOfContours != 0:
            problems.append(f"{name} draws something")
    hmtx = font["hmtx"]
    for name in ("space", "hyphen", "blank"):
        if hmtx[name][0] != 0:
            problems.append(f"{name} has width {hmtx[name][0]}, expected 0")
    for name in ("GSUB",):
        if name not in font:
            problems.append(f"no {name} table")
    names = {n.nameID: n.toUnicode() for n in font["name"].names if n.platformID == 3}
    expect = {
        1: "Thuravark Runic",
        2: "Regular",
        4: "Thuravark Runic Regular",
        5: "Version 0.1",
        6: "ThuravarkRunic-Regular",
        13: "SIL Open Font License 1.1",
        14: "https://openfontlicense.org",
    }
    for nid, value in expect.items():
        if names.get(nid) != value:
            problems.append(f"name {nid} is {names.get(nid)!r}, expected {value!r}")
    copyright_line = (HERE.parent / "LICENSE").read_text(encoding="utf-8").splitlines()[0].strip()
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
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "fonts" / "ThuravarkRunic-Regular.ttf"
    problems = check(path)
    for p in problems:
        print(f"{path}: error: {p}")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
