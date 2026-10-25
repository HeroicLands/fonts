# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Check that no two compact forms of one outline look alike.

    .venv/bin/python tools/chalish-pilam/compact_distinct.py

A compact form is a sign's outline and one token or motif (compact.py), so two signs that
share an outline differ only in what stands inside it. Each compact form is rendered
small, its frame (the outline, and a head's eye) and its inside apart. Each frame is
put in the family of the outline it is nearest: the cushion, the round cartouche, the
roof or the head, whatever its width. Insides are scaled to fill one square, so that shape
is compared rather than size, and if two insides of one family have edges that overlap above ``LIMIT``
(intersection over union) the pair is reported and the script exits 1.
"""

import io
import itertools
import sys
from pathlib import Path

import numpy as np
import resvg_py
from PIL import Image, ImageDraw, ImageFilter

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import blocks as Q  # noqa: E402
import ceremonial as R  # noqa: E402
from strokes_sheet import svg_path  # noqa: E402

LIMIT = 0.78  # a shared enclosing ring or square alone scores up to here
SCALE = 0.2
SIDE = 32
FINE = 0.6  # insides are rendered larger, so their shapes are not lost to the blur


def render(parts, scale=SCALE) -> np.ndarray:
    path = R.ink(parts, seed=0)
    w = int(R.WIDTH["double"] * scale) + 8
    h = int(R.B * R.FONT_SCALE * scale) + 8
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}"><rect width="100%" height="100%" fill="white"/>'
           f'<path d="{svg_path(path, 4, h - 4, scale)}" fill="black"/></svg>')
    img = Image.open(io.BytesIO(bytes(resvg_py.svg_to_bytes(svg_string=svg)))).convert("L").filter(ImageFilter.GaussianBlur(0.6))
    return np.asarray(img) < 200


def shape(img) -> np.ndarray:
    """``img`` cropped to its ink and scaled, keeping its proportions, to fill a square."""
    ys, xs = np.nonzero(img)
    if not len(ys):
        return np.zeros((SIDE, SIDE), bool)
    crop = img[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    h, w = crop.shape
    side = max(h, w)
    sq = np.zeros((side, side), bool)
    sq[(side - h) // 2:(side - h) // 2 + h, (side - w) // 2:(side - w) // 2 + w] = crop
    fill = np.asarray(Image.fromarray(sq).resize((SIDE, SIDE), Image.BILINEAR)) > 0
    # its edge, thickened a little: two solid shapes of one size share most of their area
    # however different their silhouettes, so the edges are what is compared
    pad = np.pad(fill, 1)
    inner = pad[:-2, 1:-1] & pad[2:, 1:-1] & pad[1:-1, :-2] & pad[1:-1, 2:] & fill
    edge = Image.fromarray(fill & ~inner).filter(ImageFilter.MaxFilter(3))
    return np.asarray(edge) > 0


def iou(a, b):
    return (a & b).sum() / max((a | b).sum(), 1)


# A sign drawn in each family's outline, at full width.
FAMILIES = {"cushion": "EARTH", "cartouche": "TQAN", "roof": "MATRIARCH", "head": "MAN"}


def frame_of(draw) -> np.ndarray:
    """A frame's silhouette: everything its outline encloses, scaled to fill a square."""
    *frame, _ = draw()
    img = Image.fromarray(render(frame, FINE).astype(np.uint8) * 255).copy()
    ImageDraw.floodfill(img, (0, 0), 128)
    sil = np.asarray(img) != 128
    ys, xs = np.nonzero(sil)
    crop = Image.fromarray(sil[ys.min():ys.max() + 1, xs.min():xs.max() + 1])
    return np.asarray(crop.resize((SIDE, SIDE), Image.BILINEAR)) > 0


def main():
    canon = {f: frame_of(Q.COMPACT[c]) for f, c in FAMILIES.items()}
    forms = {}
    for code, draw in Q.COMPACT.items():
        frame = frame_of(draw)
        family = max(canon, key=lambda f: iou(frame, canon[f]))
        forms[code] = (family, shape(render([draw()[-1]], FINE)))
    bad = 0
    for (a, (fa, ia)), (b, (fb, ib)) in itertools.combinations(forms.items(), 2):
        if fa == fb and iou(ia, ib) > LIMIT:
            bad += 1
            print(f"{a} and {b} look alike: overlap {iou(ia, ib):.0%}")
    print(f"{len(forms)} compact forms compared: {bad} pair(s) alike")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
