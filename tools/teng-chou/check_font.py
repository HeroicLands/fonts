# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Load the built Teng Chou font and confirm its characters, signs, outlines and metrics.

    .venv/bin/python tools/teng-chou/check_font.py [fonts/TengChou-Regular.ttf]

The font draws one character per Tantsou morpheme of ``characters.py`` and one sign
per Jurthati syllable of ``syllabary.py``. The checks:

- every character and sign is in the font, on the code point
  ``tools/codepoint_order.py`` gives it, and draws; the space and the
  default-ignorables draw nothing;
- every outline is fitted with curves: no contour runs a straight edge shorter than
  ``SHORT`` units more than ``MAX_SHORT`` times, the mark of an unfitted brush polygon;
- the box (tools/notdef_box.py), the names and OS/2 declarations
  (tools/font_names.py) and the vertical metrics, columns included
  (tools/vertical.py), pass;
- the .woff2 beside the .ttf opens and carries the same glyphs.
"""

import math
import sys
from pathlib import Path

from fontTools.ttLib import TTFont

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))
import codepoint_order  # noqa: E402
import font_names  # noqa: E402
import notdef_box  # noqa: E402
import vertical  # noqa: E402

ROOT = HERE.parent.parent
FONT = ROOT / "fonts" / "TengChou-Regular.ttf"
EMPTY = {"space", "ignorable", "ignorable.sub"}
IGNORABLES = [*range(0x200B, 0x2010), *range(0x202A, 0x202F), *range(0x2066, 0x206A), 0xFEFF]
SHORT = 3.0
MAX_SHORT = 40


def short_edges(glyf, name) -> int:
    """Straight on-curve edges shorter than SHORT units in a glyph."""
    g = glyf[name]
    coords, flags, ends = g.coordinates, g.flags, g.endPtsOfContours
    count, start = 0, 0
    for end in ends:
        pts = [(coords[i], flags[i] & 1) for i in range(start, end + 1)]
        for (a, on_a), (b, on_b) in zip(pts, pts[1:] + pts[:1]):
            if on_a and on_b and math.dist(a, b) < SHORT:
                count += 1
        start = end + 1
    return count


def check(path: Path) -> list[str]:
    problems = []
    font = TTFont(str(path))
    order = set(font.getGlyphOrder())
    cmap = font.getBestCmap()
    glyf = font["glyf"]
    rows = codepoint_order.ltr_table("TengChou-Regular")
    for row in rows:
        code, name = int(row["codepoint"][2:], 16), row["glyph"]
        if cmap.get(code) != name:
            problems.append(f"{row['codepoint']} maps to {cmap.get(code)}, not {name}")
        if name not in order or glyf[name].numberOfContours <= 0:
            problems.append(f"{name} is missing or draws nothing")
        elif short_edges(glyf, name) > MAX_SHORT:
            problems.append(f"{name} has {short_edges(glyf, name)} edges under {SHORT:g} units: its outline is not fitted")
    for name in EMPTY:
        if name not in order or glyf[name].numberOfContours != 0:
            problems.append(f"{name} must be in the font and draw nothing")
    if cmap.get(0x20) != "space":
        problems.append("the space is not on U+0020")
    for cp in IGNORABLES:
        if cmap.get(cp) != "ignorable":
            problems.append(f"U+{cp:04X} must map to the empty glyph 'ignorable'")
    problems += [line.split(": error: ", 1)[1] for line in notdef_box.check(path)]
    problems += [line.split(": error: ", 1)[1] for line in font_names.check(path)]
    problems += [line.split(": error: ", 1)[1] for line in vertical.check(path)]
    woff2 = path.with_suffix(".woff2")
    if not woff2.exists():
        problems.append(f"{woff2.name} is missing")
    elif TTFont(str(woff2)).getGlyphOrder() != font.getGlyphOrder():
        problems.append(f"{woff2.name} does not carry the same glyphs")
    return [f"{path}: error: {p}" for p in problems]


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else FONT
    problems = check(path)
    rows = codepoint_order.ltr_table("TengChou-Regular")
    kinds = {k: sum(1 for r in rows if r["kind"] == k) for k in ("character", "syllable")}
    for p in problems:
        print(p)
    print(f"{path}: {kinds['character']} characters, {kinds['syllable']} signs: "
          + ("ok" if not problems else f"{len(problems)} problems"))
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
