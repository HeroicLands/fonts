# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Check that every main sign stays carvable in every layout a block can give it.

    .venv/bin/python tools/chalish-pilam/compact_sweep.py [CODE ...]
    .venv/bin/python tools/chalish-pilam/compact_sweep.py --fit CODE ...

Each main sign is composed alone and in the layouts that squeeze it: with a coefficient,
a superfix, a subfix, both, a coefficient and a superfix, and two leads. A sign that
breaks the carving rule in any of them is listed with the layouts it fails, and the
script exits 1. With codes, only those signs are swept. ``--fit`` tries each named sign's
motif at a range of scales and prints the largest that passes every layout, for
``_SCALES`` in blocks.py; for a head glyph, its token's size, for ``_HEAD_SIZES``.
"""

import os
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import blocks as Q  # noqa: E402
import carving  # noqa: E402
import ceremonial as R  # noqa: E402

LAYOUTS = ("{}", "n3*{}", "la1:{}", "{}:bi1", "la1:{}:bi1", "n13*la1:{}", "n13*la1*{}")


def failures(code):
    g = Q.MAINS[code]
    out = []
    for lay in LAYOUTS:
        b = lay.format(code)
        img = carving.raster(R.Glyph(b, "", "", (lambda b=b: Q.compose(b)), g.footprint))
        if carving.narrow(img).sum():
            out.append(lay.replace("{}", "M"))
    return out


FIT = (1.05, 0.95, 0.9, 0.85, 0.8, 0.75, 0.7, 0.65, 0.6)
FIT_HEAD = (0.26, 0.24, 0.22, 0.2, 0.18, 0.16, 0.14)


def fit(code):
    import compact as M
    if Q._HEADS.get(code):
        for k in FIT_HEAD:
            Q.COMPACT[code] = M.compact(Q.MAINS[code], getattr(M, Q._HEADS[code]), head=True, size=k)
            if not failures(code):
                return k
        return None
    for k in FIT:
        Q.COMPACT[code] = M.motif_compact(Q.MAINS[code], getattr(Q.Y, Q._MOTIFS[code]), k)
        if not failures(code):
            return k
    return None


def main():
    if sys.argv[1:2] == ["--fit"]:
        for c in sys.argv[2:]:
            print(f'"{c}": {fit(c)},')
        return 0
    codes = sys.argv[1:] or list(Q.MAINS)
    bad = 0
    with ProcessPoolExecutor(min(8, os.process_cpu_count() or 1)) as pool:
        swept = list(pool.map(failures, codes))
    for c, f in zip(codes, swept):
        if f:
            bad += 1
            print(f"{c}: {' '.join(f)}")
    print(f"{len(codes)} main signs swept: {bad} fail")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
