# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Shape Helonika Book's fixtures and assert the font draws each one rightly.

    .venv/bin/python tools/helonika/guard.py [--font fonts/HelonikaBook-Regular.ttf]

What a sequence of code points must shape to follows from them (``drawn``): each is its
own glyph, the space is the space, and the accent after anything but a vowel is the box.

Each fixture in ``fixtures.json`` is a sequence of the Helónika's glyph codes
(``tools/codes/helonika.json``), with ``U+0020`` for the space, and the glyphs it is
drawn with. The guard asserts that ``drawn`` gives those glyphs and that the font,
shaping the sequence left to right, gives them too. Each ``spaces`` fixture gives the
advance of every space it shapes to: a space after the raised dot of a sentence end has
none.
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import codes  # noqa: E402
from render import Renderer  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent
HERE = Path(__file__).resolve().parent
SCRIPT = "helonika"
BOX = "notdef.box"
SPACE = " "

ENC = json.loads((HERE / "encoding.json").read_text(encoding="utf-8"))
NAME_OF = {chr(int(g["codepoint"][2:], 16)): g["glyph"] for g in ENC["glyphs"]}
VOWELS = {v for v in "A E E.long I O O.long U A.macron I.macron U.macron".split()}
VOWELS |= {v.lower() for v in VOWELS}


def drawn(text: str) -> list[str]:
    """The glyphs, in reading order, that the face draws for a string of code points."""
    g = ["space" if c == SPACE else NAME_OF.get(c, BOX) for c in text]
    return [BOX if n == "accent" and i and g[i - 1] not in VOWELS else n for i, n in enumerate(g)]


_fixtures = json.loads((HERE / "fixtures.json").read_text(encoding="utf-8"))
FIXTURES = [(f["codes"], f["glyphs"]) for f in _fixtures["fixtures"]]
# The advance of each space glyph a sequence shapes to.
SPACES = [(f["codes"], f["advances"]) for f in _fixtures["spaces"]]


def run(font: Path) -> list[str]:
    r = Renderer(font)
    failures = []
    for sequence, want in FIXTURES:
        text = codes.text(SCRIPT, sequence)
        if drawn(text) != want:
            failures.append(f"{sequence}: drawn as {drawn(text)}, expected {want}")
        got = r.glyph_names(text, direction="ltr")
        if got != want:
            failures.append(f"{sequence}: shaped {got}, expected {want}")
    for sequence, want in SPACES:
        text = codes.text(SCRIPT, sequence)
        shaped = r.shape(text, direction="ltr")
        got = [g[3] for g, c in zip(shaped.glyphs, shaped.clusters) if text[c] == SPACE]
        if got != want:
            failures.append(f"{sequence}: the spaces advance {got}, expected {want}")
    print(f"{font}: {len(FIXTURES) + len(SPACES)} fixtures, {len(failures)} failures")
    return failures


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--font", default=str(ROOT / "fonts" / "HelonikaBook-Regular.ttf"))
    args = ap.parse_args()
    failures = run(Path(args.font))
    for f in failures[:40]:
        print(f"{args.font}: error: {f}")
    if len(failures) > 40:
        print(f"{args.font}: error: ... and {len(failures) - 40} more")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
