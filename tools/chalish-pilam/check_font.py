# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Load the built Chalish Pilam Common font and confirm its glyphs, names and metrics.

    .venv/bin/python tools/chalish-pilam/check_font.py [fonts/ChalishPilamCommon-Regular.ttf]

The checks:

- every glyph of ``encoding.json`` that is not retired is in the font, on its code
  point, draws, and takes the one advance of the face; the cmap holds nothing else of
  the block;
- the space is one empty cell on U+0020, and the default-ignorables draw nothing;
- every character the face does not write maps to the box, never to ``.notdef``
  (tools/notdef_box.py);
- the name table carries the family, the SIL Open Font License 1.1 and a copyright
  line, and no trademark (tools/font_names.py checks the rest);
- the vertical metrics (tools/vertical.py) pass;
- the .woff2 beside the .ttf opens and carries the same glyphs.
"""

import json
import sys
from pathlib import Path

from fontTools.ttLib import TTFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import font_names  # noqa: E402
import notdef_box  # noqa: E402
import vertical  # noqa: E402

FONT = ROOT / "fonts" / "ChalishPilamCommon-Regular.ttf"
FAMILY = "Chalish Pilam Common"
ADVANCE = 850
BLOCK = (0xF3000, 0xF3FFF)
EMPTY = {"space", "ignorable", "ignorable.sub"}
IGNORABLES = [*range(0x200B, 0x2010), *range(0x202A, 0x202F), *range(0x2066, 0x206A), 0xFEFF]


def rows() -> list[dict]:
    return [r for r in json.loads((HERE / "encoding.json").read_text(encoding="utf-8"))["glyphs"] if not r.get("retired")]


def check(path: Path) -> list[str]:
    problems = []
    font = TTFont(str(path))
    order = set(font.getGlyphOrder())
    cmap = font.getBestCmap()
    glyf, hmtx = font["glyf"], font["hmtx"]
    listed = {}
    for row in rows():
        code, name = int(row["codepoint"][2:], 16), row["glyph"]
        listed[code] = name
        if cmap.get(code) != name:
            problems.append(f"{row['codepoint']} maps to {cmap.get(code)}, not {name}")
        if name not in order or glyf[name].numberOfContours == 0:
            problems.append(f"{name} is missing or draws nothing")
        elif hmtx[name][0] != ADVANCE:
            problems.append(f"{name} has the advance {hmtx[name][0]}, not {ADVANCE}")
    for code in sorted(c for c in cmap if BLOCK[0] <= c <= BLOCK[1] and c not in listed):
        problems.append(f"U+{code:05X} maps to {cmap[code]}, which encoding.json does not list")
    for name in EMPTY:
        if name not in order or glyf[name].numberOfContours != 0:
            problems.append(f"{name} must be in the font and draw nothing")
    if cmap.get(0x20) != "space":
        problems.append("the space is not on U+0020")
    elif hmtx["space"][0] != ADVANCE:
        problems.append(f"the space has the advance {hmtx['space'][0]}, not {ADVANCE}")
    for cp in IGNORABLES:
        if cmap.get(cp) != "ignorable":
            problems.append(f"U+{cp:04X} must map to the empty glyph 'ignorable'")
    problems += [line.split(": error: ", 1)[1] for line in notdef_box.check(path)]
    problems += [line.split(": error: ", 1)[1] for line in font_names.check(path)]
    problems += [line.split(": error: ", 1)[1] for line in vertical.check(path)]
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
        problems.append(f"{woff2.name} is missing")
    elif TTFont(str(woff2)).getGlyphOrder() != font.getGlyphOrder():
        problems.append(f"{woff2.name} does not carry the same glyphs")
    return [f"{path}: error: {p}" for p in problems]


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else FONT
    problems = check(path)
    for p in problems:
        print(p)
    print(f"{path}: {len(rows())} glyphs: " + ("ok" if not problems else f"{len(problems)} problems"))
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
