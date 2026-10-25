# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Check that no two syllable signs of the ceremonial hand look alike.

    .venv/bin/python tools/chalish-pilam/syllabary_distinct.py

Each sign's flat form is rendered small, its motif alone and softened slightly, and
compared with every other sign's. Two signs of different syllables
whose renders overlap above ``LIMIT`` (intersection over union) are reported, and the
script exits 1. Two signs of one syllable may look alike: either reads the same.
"""

import io
import itertools
import sys
from pathlib import Path

import numpy as np
import resvg_py
from PIL import Image, ImageFilter

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ceremonial as R  # noqa: E402
import syllabary as Y  # noqa: E402
from strokes_sheet import svg_path  # noqa: E402

LIMIT = 0.66  # above this, the pictures themselves agree, not only their frames
SCALE = 0.25


def render(sign) -> np.ndarray:
    parts = [(pen, ps) for pen, ps in sign.flat() if pen is R.DETAIL]
    path = R.ink(parts, seed=0)
    w, h = int(Y.B * Y.SPAN * SCALE) + 8, int(Y.B * Y.AFFIX * SCALE) + 8
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}"><rect width="100%" height="100%" fill="white"/>'
           f'<path d="{svg_path(path, 4, h - 4, SCALE)}" fill="black"/></svg>')
    img = Image.open(io.BytesIO(bytes(resvg_py.svg_to_bytes(svg_string=svg)))).convert("L").filter(ImageFilter.GaussianBlur(0.6))
    return np.asarray(img) < 200


def main():
    renders = {code: render(s) for code, s in Y.SIGNS.items()}
    bad = 0
    for (a, ra), (b, rb) in itertools.combinations(renders.items(), 2):
        if Y.SIGNS[a].syllable == Y.SIGNS[b].syllable:
            continue
        iou = (ra & rb).sum() / max((ra | rb).sum(), 1)
        if iou > LIMIT:
            bad += 1
            print(f"{a} and {b} look alike: overlap {iou:.0%}")
    print(f"{len(renders)} signs compared: {bad} pair(s) alike")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
