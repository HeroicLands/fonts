# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Confirm that the Jurthati signs are distinct from each other at body size.

    .venv/bin/python tools/teng-chou/syllabary_distinct.py [--report] [--search SYLLABLE ...]

Each sign is rendered as it stands in a line of text, ``PX`` pixels to the em,
and softened by a pixel, as an eye reads it; two signs are compared by the
cosine of their images. A pair above ``LIMIT`` fails: at body size the two
would be read as one.

``--search`` proposes strokes for a sign that collides: it tries every set of two
to four of its source's strokes, in stroke order, and prints the set to write into
``PICKS`` in ``syllabary.py``: of the sets clear of every other sign by ``MARGIN``,
one of three strokes if there is one, then of four, then of two, covering the most
ground; or, if none is clear, the set farthest from the others. A set the stroke-mix
guard (``stroke_mix.py``) would refuse, mostly dabs, is never proposed.
"""

from __future__ import annotations

import itertools
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import layout as Y  # noqa: E402
import strokes as S  # noqa: E402
import stroke_mix  # noqa: E402
import syllabary as J  # noqa: E402

PX = 24
SS = 4
LIMIT = 0.86
MARGIN = 0.06  # how far below the limit a proposed set must stand


def image(path) -> np.ndarray:
    size = PX * SS
    img = Image.new("L", (size, size), 0)
    layer_mask = Image.new("1", (size, size), 0)
    for poly in S.contours(path):
        layer = Image.new("1", (size, size), 0)
        pts = [(x / 1000 * size, size - y / 1000 * size) for x, y in poly]
        if len(pts) >= 3:
            ImageDraw.Draw(layer).polygon(pts, fill=1)
        layer_mask = ImageChops.logical_xor(layer_mask, layer)
    img.paste(255, (0, 0), layer_mask)
    img = img.resize((PX, PX), Image.LANCZOS).filter(ImageFilter.GaussianBlur(1))
    a = np.asarray(img, dtype=float).ravel()
    n = np.linalg.norm(a)
    return a / n if n else a


def images() -> dict[str, np.ndarray]:
    return {g.syllable: image(J.render(g.syllable)) for g in J.SIGNS}


def pairs(ims: dict[str, np.ndarray]):
    """Every pair of signs with the cosine of their images, most alike first."""
    keys = list(ims)
    out = [(float(ims[a] @ ims[b]), a, b) for a, b in itertools.combinations(keys, 2)]
    return sorted(out, reverse=True)


def search(syllable: str, ims: dict[str, np.ndarray]):
    sign = J.BY_SYLLABLE[syllable]
    strokes, _ = J.source_strokes(sign)
    others = [v for k, v in ims.items() if k != syllable]
    best = None
    for k in (2, 3, 4):
        for combo in itertools.combinations(range(len(strokes)), k):
            sign.picks = combo
            if stroke_mix.sign_problems(stroke_mix.sign_mix(sign)):
                continue
            try:
                im = image(J.render(syllable))
            except Exception:
                continue
            worst = max(float(im @ o) for o in others)
            extent = sum(J._extent(strokes[i][2]) for i in combo)
            # a set clear of every other sign by MARGIN wins on its strokes, three
            # before four before two, then on the ground it covers
            clear = worst <= LIMIT - MARGIN
            score = (0, {3: 0, 4: 1, 2: 2}[k], -extent) if clear else (1, round(worst, 3), -extent)
            if best is None or score < best[0]:
                best = (score, combo)
    sign.picks = ()
    return best


def main():
    args = sys.argv[1:]
    ims = images()
    if "--search" in args:
        for syl in args[args.index("--search") + 1:]:
            _, combo = search(syl, ims)
            print(f"{syl}: picks {combo}")
        return
    found = pairs(ims)
    bad = [p for p in found if p[0] > LIMIT]
    if "--report" in args:
        for sim, a, b in found[:25]:
            print(f"{a:>4} {b:>4} {sim:.3f}")
    for sim, a, b in bad:
        print(f"tools/teng-chou/syllabary.py: error: the signs {a} and {b} are alike at {PX} px ({sim:.3f} > {LIMIT})")
    print(f"{len(J.SIGNS)} signs: " + ("ok" if not bad else f"{len(bad)} pairs alike"))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
