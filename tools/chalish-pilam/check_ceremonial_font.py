# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Load the built Chalish Pilam Ceremonial font and confirm its glyphs, names and metrics.

    .venv/bin/python tools/chalish-pilam/check_ceremonial_font.py [fonts/ChalishPilamCeremonial-Regular.ttf]

The checks:

- every glyph of ``ceremonial_encoding.json`` that is neither retired nor pending is in
  the font, on its code point, and draws; a sign takes its block's advance, its
  footprint's width and a gutter either side, and a joiner takes none and draws nothing;
- a pending row's code point maps to the box, and the cmap holds nothing else of the
  block;
- the space is one empty full block on U+0020, and the default-ignorables draw nothing;
- every character the face does not write maps to the box, never to ``.notdef``
  (tools/notdef_box.py);
- the name table carries the family, the SIL Open Font License 1.1 and a copyright
  line, and no trademark (tools/font_names.py checks the rest);
- the vertical metrics (tools/vertical.py) pass;
- the .woff2 beside the .ttf opens and carries the same glyphs.

How the font lays out a block is checked by ``ceremonial_guard.py``.
"""

import json
import sys
from pathlib import Path

from fontTools.ttLib import TTFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "tools"))
import ceremonial_layout as L  # noqa: E402
import font_names  # noqa: E402
import notdef_box  # noqa: E402
import vertical  # noqa: E402

FONT = ROOT / "fonts" / "ChalishPilamCeremonial-Regular.ttf"
FAMILY = "Chalish Pilam Ceremonial"
BLOCK = (0xF4000, 0xF4FFF)
BOX = notdef_box.BOX
EMPTY = {"space", "ignorable", "ignorable.sub"}
IGNORABLES = [*range(0x200B, 0x2010), *range(0x202A, 0x202F), *range(0x2066, 0x206A), 0xFEFF]


def rows() -> list[dict]:
    table = json.loads((HERE / "ceremonial_encoding.json").read_text(encoding="utf-8"))["glyphs"]
    return [r for r in table if not r.get("retired")]


def advance(row: dict) -> int:
    """The advance a character takes: none for a joiner, else its block's."""
    if row["kind"] == "joiner":
        return 0
    return round(L.block_advance(row.get("footprint", "full")))


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
        if row.get("pending"):
            if cmap.get(code) != BOX:
                problems.append(f"{row['codepoint']} is pending and maps to {cmap.get(code)}, not the box")
            continue
        if cmap.get(code) != name:
            problems.append(f"{row['codepoint']} maps to {cmap.get(code)}, not {name}")
        if name not in order:
            problems.append(f"{name} is missing")
            continue
        draws = glyf[name].numberOfContours != 0
        if draws != (row["kind"] != "joiner"):
            problems.append(f"{name} {'draws' if draws else 'draws nothing'}")
        if hmtx[name][0] != advance(row):
            problems.append(f"{name} has the advance {hmtx[name][0]}, not {advance(row)}")
    for code in sorted(c for c in cmap if BLOCK[0] <= c <= BLOCK[1] and c not in listed):
        problems.append(f"U+{code:05X} maps to {cmap[code]}, which ceremonial_encoding.json does not list")
    for name in EMPTY:
        if name not in order or glyf[name].numberOfContours != 0:
            problems.append(f"{name} must be in the font and draw nothing")
    full = round(L.block_advance("full"))
    if cmap.get(0x20) != "space":
        problems.append("the space is not on U+0020")
    elif hmtx["space"][0] != full:
        problems.append(f"the space has the advance {hmtx['space'][0]}, not {full}")
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
