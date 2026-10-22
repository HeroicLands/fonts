# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Write the one-line sample image of each font that the README shows.

    .venv/bin/python tools/readme_samples.py

Each font's first characters, in code point order, are set in the font itself and
written to specimens/readme/<class>.png. Every family of fonts.json that is its own
font file gets one; a variant that shares another family's file has none.
"""

import json
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from render import Renderer  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "specimens" / "readme"
KINDS = {"letter", "character", "sign"}
COUNT = 10
SIZE = 72
PAD = 18
INK = (22, 20, 18)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    seen = set()
    for family in json.loads((ROOT / "fonts.json").read_text(encoding="utf-8"))["families"]:
        path = family["files"]["ttf"]
        if path in seen:
            continue
        seen.add(path)
        chars = [chr(int(c["codepoint"][2:], 16)) for c in family["codepoints"] if c["kind"] in KINDS][:COUNT]
        font = Renderer(ROOT / path)
        direction = "rtl" if family["direction"] == "rtl" else "ltr"
        features = {f: True for f in family["features"]}
        text = "".join(chars)
        width = int(font.width(text, SIZE, features, direction)) + 2 * PAD
        img = Image.new("RGB", (width, int(SIZE * 1.9) + 2 * PAD), "white")
        font.text(img, PAD, PAD + SIZE * 1.3, text, SIZE, INK, features, direction)
        target = OUT / f"{family['class']}.png"
        img.save(target, optimize=True)
        print(target.relative_to(ROOT))


if __name__ == "__main__":
    main()
