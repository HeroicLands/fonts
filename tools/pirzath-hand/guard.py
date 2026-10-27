# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Shape Pirzath Hand's fixtures and assert the hand draws each one rightly.

    .venv/bin/python tools/pirzath-hand/guard.py [--font fonts/PirzathHand-Regular.ttf]

The hand draws the same code points as the carved face, so its fixtures in
``fixtures.json`` are sequences of Pirzath's glyph codes (``tools/codes/pirzath.json``),
with ``U+XXXX`` for a character the script has no code for. They cover what the carved
face's fixtures cover, drawn as the hand draws it: a vowel and its length mark are the
long-vowel glyph, and a doubled consonant is the doubled glyph (``p_p``, ``t_h_t_h``).
A length mark left on a vowel pair stays a separate mark above the pair.

The hand is one printed face: every letter is drawn as itself, whatever stands beside
it, and no feature joins letters. Besides the glyphs, the guard asserts

- **the marks**: each ``marks`` fixture names the length mark and the vowel pair it
  stands over, by their places in the shaped run; the mark takes no advance and stands
  above its pair;
- **the default-ignorable characters**: each ``ignorables`` fixture holds one; it draws
  nothing, takes no advance and leaves the letters round it as they are without it.
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
SCRIPT = "pirzath"
EMPTY = {"ignorable", "ignorable.sub"}

_fixtures = json.loads((HERE / "fixtures.json").read_text(encoding="utf-8"))
FIXTURES = [(f["codes"], f["glyphs"]) for f in _fixtures["fixtures"]]
MARK_FIXTURES = [(f["codes"], f["mark"], f["base"]) for f in _fixtures["marks"]]
IGNORABLE_FIXTURES = _fixtures["ignorables"]


def mark_failures(r: Renderer) -> list[str]:
    failures = []
    for sequence, mi, bi in MARK_FIXTURES:
        shaped = r.shape(codes.text(SCRIPT, sequence))
        gid_m, mx, my, madv = shaped.glyphs[mi]
        gid_b, bx, _, badv = shaped.glyphs[bi]
        name = r.order[gid_m]
        pen = BoundsPen(r.tt.getGlyphSet())
        r.tt.getGlyphSet()[name].draw(pen)
        x0, y0, x1, y1 = pen.bounds
        lo = my + y0
        cx = mx + (x0 + x1) / 2
        if name != "lengthmark":
            failures.append(f"{sequence}: glyph {mi} is {name}, not the length mark")
        if madv != 0:
            failures.append(f"{sequence}: {name} has an advance of {madv}")
        if lo < 300:
            failures.append(f"{sequence}: {name} is not above its pair (its ink reaches down to {lo})")
        if not (bx - 40 <= cx <= bx + badv + 80):
            failures.append(f"{sequence}: {name} is not seated on {r.order[gid_b]} (centre {cx:.0f}, base {bx}..{bx + badv})")
    return failures


def bare(text: str) -> str:
    """The text without its default-ignorable characters."""
    return "".join(ch for ch in text if not (0x200B <= ord(ch) <= 0x200F or 0x2066 <= ord(ch) <= 0x2069
                                             or ord(ch) == 0xFEFF))


def ignorable_failures(r: Renderer) -> list[str]:
    failures = []
    for sequence in IGNORABLE_FIXTURES:
        text = codes.text(SCRIPT, sequence)
        shaped = r.shape(text)
        names = [r.order[g[0]] for g in shaped.glyphs]
        if any(g[3] for n, g in zip(names, shaped.glyphs) if n in EMPTY):
            failures.append(f"{sequence}: an ignorable has an advance")
        if "space" in names or ".notdef" in names or "notdef.box" in names:
            failures.append(f"{sequence}: shaped {names}, which draws a space, .notdef or the box")
        kept = [n for n in names if n not in EMPTY]
        alone = [r.order[g[0]] for g in r.shape(bare(text)).glyphs]
        if kept != alone:
            failures.append(f"{sequence}: shaped {kept}, expected {alone}")
    return failures


def run(font: Path) -> list[str]:
    r = Renderer(font)
    failures = []
    for sequence, want in FIXTURES:
        got = r.glyph_names(codes.text(SCRIPT, sequence))
        if got != want:
            failures.append(f"{sequence}: shaped {got}, expected {want}")
    failures += mark_failures(r)
    failures += ignorable_failures(r)
    total = len(FIXTURES) + len(MARK_FIXTURES) + len(IGNORABLE_FIXTURES)
    print(f"{font}: {total} fixtures, {len(failures)} failures")
    return failures


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--font", default=str(ROOT / "fonts" / "PirzathHand-Regular.ttf"))
    args = ap.parse_args()
    failures = run(Path(args.font))
    for f in failures[:40]:
        print(f"{args.font}: error: {f}")
    if len(failures) > 40:
        print(f"{args.font}: error: ... and {len(failures) - 40} more")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
