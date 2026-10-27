# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Shape Pirzath Carved's fixtures and assert the font draws each one rightly.

    .venv/bin/python tools/pirzath/guard.py [--font fonts/PirzathCarved-Regular.ttf]

Each fixture in ``fixtures.json`` is a sequence of Pirzath's glyph codes
(``tools/codes/pirzath.json``), with ``U+XXXX`` for a character the script has no code
for, and the glyphs the font must shape it to. The fixtures cover the numerals, the
quotation marks, nested ones included, the marks between words, a doubled letter or
digraph drawn once with the doubling mark, the seventeen lost letters in every
position they occupy, the diphthongs with and without the length mark, and characters
the font lacks, which print the box.
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
SCRIPT = "pirzath"
FIXTURES = [(f["codes"], f["glyphs"]) for f in json.loads((HERE / "fixtures.json").read_text(encoding="utf-8"))["fixtures"]]


def run(font: Path) -> list[str]:
    r = Renderer(font)
    failures = []
    for sequence, want in FIXTURES:
        got = r.glyph_names(codes.text(SCRIPT, sequence))
        if got != want:
            failures.append(f"{sequence}: shaped {got}, expected {want}")
    print(f"{font}: {len(FIXTURES)} fixtures, {len(failures)} failures")
    return failures


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--font", default=str(ROOT / "fonts" / "PirzathCarved-Regular.ttf"))
    args = ap.parse_args()
    failures = run(Path(args.font))
    for f in failures[:40]:
        print(f"{args.font}: error: {f}")
    if len(failures) > 40:
        print(f"{args.font}: error: ... and {len(failures) - 40} more")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
