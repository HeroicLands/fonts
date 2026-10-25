# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Check that every ceremonial glyph can be carved: no white gap inside its cushion is
narrower than one detail line, so a chisel can cut every groove.

    .venv/bin/python tools/chalish-pilam/carving.py [--show DIR]

Each glyph is rasterized at one pixel to two font units, each pixel inked where the
glyph covers half of it or more, measured by rendering four times larger and averaging,
so the result does not turn on a rasterizer's antialiasing. White is too narrow to cut where
an opening by a disc as wide as the narrowest groove removes it; such white counts only
where it forms a channel, larger than the tip of a wedge where two strokes meet at an
angle, which every carving has. Prints each glyph's share of narrow channels and exits 1
when any glyph has one. ``--show`` writes each glyph with its narrow channels in red.
"""

import argparse
import io
import sys
from pathlib import Path

import numpy as np
import resvg_py
from PIL import Image
from scipy import ndimage

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ceremonial as R  # noqa: E402
import blocks as Q  # noqa: E402
import syllabary as Y  # noqa: E402
import strokes as S  # noqa: E402
from strokes_sheet import svg_path  # noqa: E402

SCALE = 0.5  # pixels per font unit
ALLOWANCE = 0.0  # no channel too narrow to cut is allowed
CHANNEL = (R.GAP * SCALE) ** 2 * 1.5  # pixels: a narrow region larger than this is a channel, not a wedge's tip
SUPERSAMPLE = 4  # a pixel's coverage is the mean of this many squared subpixels


def raster(g):
    path = R.ink(g.draw(), seed=0)
    size = int(S.BLOCK * SCALE) + 20
    wide = int(R.WIDTH[g.footprint] * SCALE) + 20 if g.footprint in R.WIDTH else size
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{wide}" height="{size}">'
           f'<rect width="100%" height="100%" fill="white"/>'
           f'<path d="{svg_path(path, 10, size - 10, SCALE)}" fill="black"/></svg>')
    big = Image.open(io.BytesIO(bytes(resvg_py.svg_to_bytes(svg_string=svg, zoom=SUPERSAMPLE)))).convert("L")
    return big.resize((wide, size), Image.BOX).point(lambda v: 255 if v > 127 else 0)


def narrow(img):
    """The white too narrow to cut, as a boolean array: white that an opening by a disc as
    wide as the narrowest groove removes, kept only where it forms a channel, a region
    larger than the tip of a wedge where two strokes meet at an angle."""
    white = np.asarray(img) > 127
    r = R.GAP * SCALE / 2
    k = int(np.ceil(r))
    yy, xx = np.mgrid[-k:k + 1, -k:k + 1]
    disc = xx * xx + yy * yy <= r * r
    outside, _ = ndimage.label(white)
    border = set(np.unique(np.concatenate([outside[0], outside[-1], outside[:, 0], outside[:, -1]]))) - {0}
    inside = white & ~np.isin(outside, list(border))
    thin = inside & ~ndimage.binary_opening(white, structure=disc)
    labels, n = ndimage.label(thin)
    if not n:
        return thin
    sizes = ndimage.sum(thin, labels, range(1, n + 1))
    channel = np.isin(labels, 1 + np.flatnonzero(sizes > CHANNEL))
    return channel


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--show")
    args = ap.parse_args()
    bad = 0
    def footprint(block):
        mains = [c for c in block.replace("*", ":").split(":") if c in Q.MAINS]
        return Q.MAINS[mains[0]].footprint if mains else "full"

    composed = [R.Glyph(b, "a composed block", "", (lambda b=b: Q.compose(b)), footprint(b)) for b in
                ("n3*la1:JAGUAR", "sho1*bi1", "la1:JAGUAR:bi1", "n13*JAGUAR", "n3*SERPENT", "la1:SERPENT:bi1",
                 "n0", "n20", "n400", "n8000", "n160000", "KING:ka1", "n3*la1:STORM_SERPENT")]
    signs = [R.Glyph(f"{c}.{form}", s.source, s.syllable, getattr(s, form)) for c, s in Y.SIGNS.items()
             for form in ("flat", "tall")]
    numbers = [g for g in R.PILOT if g.name[1:].isdigit()]
    for g in numbers + Q._concepts() + composed + signs:
        img = raster(g)
        gaps = narrow(img)
        white = int((np.asarray(img) > 127).sum())  # the share is of all the white, inside and out
        share = gaps.sum() / max(white, 1)
        flag = share > ALLOWANCE
        bad += flag
        print(f"{g.name:10} narrow channels {share:.2%}" + ("  error: a groove too fine to carve" if flag else ""))
        if args.show:
            rgb = np.stack([np.asarray(img)] * 3, axis=-1).copy()
            rgb[gaps] = (220, 0, 0)
            Path(args.show).mkdir(parents=True, exist_ok=True)
            Image.fromarray(rgb).save(Path(args.show) / f"{g.name}.png")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
