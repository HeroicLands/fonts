# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Shape Semaron Kuriale's fixtures and assert the font draws each one rightly.

    .venv/bin/python tools/semaron-kuriale/guard.py [--font fonts/SemaronKuriale-Regular.ttf]

Each fixture in ``fixtures.json`` is a sequence of Semaron's glyph codes
(``tools/codes/semaron.json``), with ``U+XXXX`` for a character the script has no code
for, and the glyphs the font must shape it to; the empty glyphs of the
default-ignorables are left out, and every copy of the box is named as the box. The
fixtures cover every letter in both cases, the digraph letters, the long vowels, the
numerals, the point, the space, the catch on every kind of base and with no base,
where it prints the box, the default-ignorable characters, which draw nothing, and
characters the font lacks, which print the box. Besides the glyphs, the guard asserts

- **the widths**: each ``widths`` pair sets as wide with the catch as without it;
- **the marks**: in each ``marks`` fixture every catch takes no advance and is seated
  on its base, high enough to clear it.
"""

import argparse
import json
import sys
from pathlib import Path

from fontTools.pens.boundsPen import BoundsPen

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import codes  # noqa: E402
from render import Renderer  # noqa: E402

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SCRIPT = "semaron"

BOX = "notdef.box"
BOX_GLYPHS = {BOX}
EMPTY = {"ignorable", "ignorable.sub"}

_fixtures = json.loads((HERE / "fixtures.json").read_text(encoding="utf-8"))
FIXTURES = [(f["codes"], f["glyphs"]) for f in _fixtures["fixtures"]]
# Pairs of lines the catch must set exactly as wide as the line without it.
WIDTH_PAIRS = [tuple(pair) for pair in _fixtures["widths"]]
# The catch sits over, beside or at the right of its base: these lines place one.
MARK_FIXTURES = _fixtures["marks"]


def normalized(names: list[str]) -> list[str]:
    """Shaped glyph names with the empty ignorables dropped and every copy of the box named as it."""
    return [BOX if n in BOX_GLYPHS else n for n in names if n not in EMPTY]


def mark_failures(r: Renderer) -> list[str]:
    """Each catch takes no room and stands on its base."""
    failures = []
    glyphset = r.tt.getGlyphSet()
    for text in MARK_FIXTURES:
        shaped = r.shape(codes.text(SCRIPT, text))
        names = [r.order[g[0]] for g in shaped.glyphs]
        pen_x = 0
        base = None
        for name, (gid, gx, gy, adv) in zip(names, shaped.glyphs):
            if name != "grave":
                base = (name, pen_x, adv)
                pen_x += adv
                continue
            if base is None:
                failures.append(f"{text}: a catch has no base")
                continue
            bounds = BoundsPen(glyphset)
            glyphset[name].draw(bounds)
            x0, y0, x1, y1 = bounds.bounds
            if adv != 0:
                failures.append(f"{text}: the catch has an advance of {adv}")
            centre = gx + (x0 + x1) / 2
            if not (base[1] - 40 <= centre <= base[1] + base[2] + 140):
                failures.append(f"{text}: the catch is not seated on {base[0]} (centre {centre:.0f}, base {base[1]}..{base[1] + base[2]})")
            if gy + y0 < 200:
                failures.append(f"{text}: the catch sits too low on {base[0]} (its ink reaches down to {gy + y0:.0f})")
    return failures


def run(font: Path) -> list[str]:
    r = Renderer(font)
    failures = []
    for text, want in FIXTURES:
        got = normalized([r.order[g[0]] for g in r.shape(codes.text(SCRIPT, text)).glyphs])
        if got != want:
            failures.append(f"{text}: shaped {got}, expected {want}")
    for text, plain in WIDTH_PAIRS:
        wide, narrow = r.shape(codes.text(SCRIPT, text)).advance, r.shape(codes.text(SCRIPT, plain)).advance
        if wide != narrow:
            failures.append(f"{text} sets {wide} wide, {plain} sets {narrow}")
    failures += mark_failures(r)
    print(
        f"{font}: {len(FIXTURES)} fixtures, {len(WIDTH_PAIRS)} width pairs, {len(MARK_FIXTURES)} mark placements, "
        f"{len(failures)} failures"
    )
    return failures


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--font", default=str(ROOT / "fonts" / "SemaronKuriale-Regular.ttf"))
    args = ap.parse_args()
    if not Path(args.font).exists():
        print(f"{args.font}: error: the font does not exist")
        sys.exit(1)
    failures = run(Path(args.font))
    for f in failures[:40]:
        print(f"{args.font}: error: {f}")
    if len(failures) > 40:
        print(f"{args.font}: error: ... and {len(failures) - 40} more")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
