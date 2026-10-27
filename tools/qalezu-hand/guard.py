# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Shape Qalezu Hand's fixtures and assert the font draws each one rightly.

    .venv/bin/python tools/qalezu-hand/guard.py [--font fonts/QalezuHand-Regular.ttf]

The font draws each code point as its sign, with one contextual form: a catch
followed by a consonant sign or a doubled sign is drawn as that sign's
catch-before form (``<sign>.catch``, three reed dabs in a triangle over the
sign), which has no code point of its own. Two identical consonant signs stay
two signs; a doubled consonant is its own character. So the glyphs a sequence must
shape to follow from its code points (``drawn``), with each catch and the sign after
it fused, in reverse order for the visual run, and none ``.notdef`` or the box.

Each fixture in ``fixtures.json`` is a sequence of Qalezu's glyph codes
(``tools/codes/qalezu.json``), with ``U+0020`` for the space, and the signs it is drawn
with, in reading order. The guard asserts that ``drawn`` gives those signs and that the
font, shaping the sequence right to left, gives them too. Targets come from
``encoding.json``, the table of the font's code points.
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import codes  # noqa: E402
from render import Renderer  # noqa: E402

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
ENCODING = HERE / "encoding.json"
FIXTURE_FILE = HERE / "fixtures.json"
SCRIPT = "qalezu"
BOX = "notdef.box"
SPACE = " "


def load_encoding():
    enc = json.loads(ENCODING.read_text(encoding="utf-8"))
    name_of = {chr(int(g["codepoint"][2:], 16)): g["glyph"] for g in enc["glyphs"]}
    fused = {f["base"]: f["glyph"] for f in enc["forms"]}
    return name_of, fused, name_of[codes.characters(SCRIPT)["CATCH"]]


NAME_OF, FUSED, CATCH = load_encoding()


def drawn(text: str) -> list[str]:
    """The glyphs, in reading order, that the face draws for a string of code points."""
    names = ["space" if c == SPACE else NAME_OF.get(c, BOX) for c in text]
    out: list[str] = []
    for name in names:
        if out and out[-1] == CATCH and name in FUSED:
            out[-1] = FUSED[name]
        else:
            out.append(name)
    return out


# Each fixture: a sequence of codes and the signs it is drawn with, in reading order.
FIXTURES = [(f["codes"], f["signs"]) for f in json.loads(FIXTURE_FILE.read_text(encoding="utf-8"))["fixtures"]]


def run(font: Path) -> list[str]:
    r = Renderer(font)
    failures = []
    for sequence, want in FIXTURES:
        text = codes.text(SCRIPT, sequence)
        if drawn(text) != want:
            failures.append(f"{sequence}: drawn as {drawn(text)}, expected {want}")
        got = r.glyph_names(text, direction="rtl")
        if got != want[::-1]:
            failures.append(f"{sequence}: shaped {got}, expected {want[::-1]}")
    print(f"{font}: {len(FIXTURES)} fixtures, {len(failures)} failures")
    return failures


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--font", default=str(ROOT / "fonts" / "QalezuHand-Regular.ttf"))
    args = ap.parse_args()
    failures = run(Path(args.font))
    for f in failures[:40]:
        print(f"{args.font}: error: {f}")
    if len(failures) > 40:
        print(f"{args.font}: error: ... and {len(failures) - 40} more")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
