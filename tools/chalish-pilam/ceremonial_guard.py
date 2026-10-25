# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Shape blocks of codage through Chalish Pilam Ceremonial and assert they are the blocks ``blocks.compose`` lays out.

    .venv/bin/python tools/chalish-pilam/ceremonial_guard.py [--font fonts/ChalishPilamCeremonial-Regular.ttf]
                                                              [--min-iou 0.98] [--limit N]

Each fixture is a run of blocks in codage. It is converted to characters by the rows of
``ceremonial_codage.py``, shaped by HarfBuzz through the font, and rasterized from the
shaped glyphs. The reference is ``blocks.compose`` for the same block, inked,
scaled and shifted as the font sets a block, and rasterized the same way. A fixture
fails when

- a shaped glyph is ``.notdef`` or the box;
- the shaped run's advance is not the sum of its blocks' widths, a block being as wide
  as its main sign's footprint (a full block when it has no main);
- the two rasters differ by more than the pixel intersection over union allows.

Fixtures cover every layout a block can take with every main sign, every syllable sign
in each slot it can take, and every number. A second set is blocks the font rejects:
more than two affixes, or a joiner where no layout has one. They must shape to plain
glyphs only, with no variant, and are listed as rejected.
"""

import argparse
import io
import os
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import resvg_py
from fontTools.misc.bezierTools import calcCubicPoints
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.transformPen import TransformPen
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "tools"))
import blocks as Q  # noqa: E402
import ceremonial as R  # noqa: E402
import ceremonial_codage as C  # noqa: E402
from render import Renderer, flatten_quadratic  # noqa: E402

FONT = ROOT / "fonts" / "ChalishPilamCeremonial-Regular.ttf"
BAD = {".notdef", "notdef.box"}
GUTTER = 60.0
INK_SEED = 0
PX = 0.25  # raster pixels per font unit
LEFT, RIGHT, TOP, BOTTOM = 150, 150, 1050, -300  # the window around the run, in font units
SPECIFIC = [
    "JAGUAR", "n3*JAGUAR", "n3*la1*KING", "la1:JAGUAR", "KING:bi1", "la1:JAGUAR:bi1", "n13*la1:SUN",
    "n3*KING:ka1", "sho1", "sho1*bi1", "ka1*la1*bi1", "la1:KING:bi1", "n3*la1:JAGUAR-sho1*bi1",
    "SUN-KING-ka1*bi1", "SERPENT", "n3*SERPENT", "la1:SERPENT:bi1", "SERPENT:ka1-SUN",
]
REJECTED = [
    "n3*la1*KING*bi1", "la1:KING:bi1:ka2", "SUN*ka1*la1*bi1", "ka1*la1*bi1*ka2", "ka1:bi1", "n3:SUN",
    "SUN*ka1", "ka1:SUN*bi1", "n3*la1*n4*SUN",
]


def fixtures() -> list[str]:
    """The codage of every accepted fixture."""
    out = list(SPECIFIC)
    for main in Q.MAINS:
        out += [main, f"n3*{main}", f"n3*la1*{main}", f"la1:{main}", f"{main}:bi1", f"la1:{main}:bi1",
                f"n3*la1:{main}", f"n3*{main}:ka1", f"ka1*{main}"]
    for s in Q.SIGNS:
        out += [s, f"{s}*SUN", f"n3*{s}*KING", f"{s}:SUN", f"SUN:{s}", f"n3*{s}:SUN", f"n3*SUN:{s}",
                f"SERPENT:{s}", f"{s}*bi1", f"bi1*{s}", f"{s}*bi1*la1", f"bi1*{s}*la1", f"bi1*la1*{s}",
                f"{s}:SUN:ka1", f"ka1:SUN:{s}"]
    for n in range(1, 20):
        out += [f"n{n}", f"n{n}*SUN", f"n3*n{n}*SUN", f"n{n}*la1", f"la1*n{n}", f"n{n}*n3*la1"]
    return list(dict.fromkeys(out))


def blocks_of(codage: str) -> list[str]:
    return codage.split("-")


def block_footprint(block: str) -> str:
    for code in block.replace(":", "*").split("*"):
        if code in Q.MAINS:
            return Q.MAINS[code].footprint
    return "full"


def advance_of(footprint: str) -> float:
    return R.WIDTH[footprint] * R.FONT_SCALE + 2 * GUTTER


def contours_of_path(path, dx: float) -> list[list]:
    """A pathops path drawn at font scale, as flattened contours starting at x ``dx``."""
    pen = RecordingPen()
    path.draw(TransformPen(pen, (R.FONT_SCALE, 0, 0, R.FONT_SCALE, GUTTER + dx, R.FONT_DROP)))
    out, cur = [], []
    for op, args in pen.value:
        if op == "moveTo":
            cur = [args[0]]
        elif op == "lineTo":
            cur.append(args[0])
        elif op == "curveTo":
            p0, p1, p2, p3 = (cur[-1], *args)
            a, b, c, d = calcCubicPoints(p0, p1, p2, p3)
            for i in range(1, 17):
                t = i / 16
                cur.append((((a[0] * t + b[0]) * t + c[0]) * t + d[0], ((a[1] * t + b[1]) * t + c[1]) * t + d[1]))
        elif op == "qCurveTo":
            cur.extend(flatten_quadratic(cur[-1], args))
        elif op in ("closePath", "endPath") and cur:
            out.append(cur)
            cur = []
    return out


def raster(glyphs: list[list[list]], width: float) -> np.ndarray:
    """A boolean mask of the glyphs, each an even-odd fill of its contours, over the window."""
    w, h = (width + LEFT + RIGHT) * PX, (TOP - BOTTOM) * PX
    paths = []
    for contours in glyphs:
        d = " ".join("M" + " L".join(f"{(x + LEFT) * PX:.2f},{(TOP - y) * PX:.2f}" for x, y in c) + "Z" for c in contours)
        if d:
            paths.append(f'<path fill="#000" fill-rule="evenodd" d="{d}"/>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{round(w)}" height="{round(h)}">'
           f'<rect width="100%" height="100%" fill="#fff"/>{"".join(paths)}</svg>')
    png = bytes(resvg_py.svg_to_bytes(svg_string=svg))
    return np.asarray(Image.open(io.BytesIO(png)).convert("L")) < 128


def reference(codage: str):
    """(glyph contours, advance) of the blocks of ``codage`` as ``blocks.compose`` lays them out."""
    glyphs, x = [], 0.0
    for block in blocks_of(codage):
        glyphs.append(contours_of_path(R.ink(Q.compose(block), INK_SEED), x))
        x += advance_of(block_footprint(block))
    return glyphs, x


def iou(a: np.ndarray, b: np.ndarray) -> float:
    if a.shape != b.shape:
        return 0.0
    union = np.logical_or(a, b).sum()
    return 1.0 if union == 0 else float(np.logical_and(a, b).sum() / union)


class Shaper:
    def __init__(self, path: Path):
        self.renderer = Renderer(path)
        self.order = self.renderer.order

    def run(self, text: str):
        """(glyph names, glyph contours placed on the run, advance)."""
        shaped = self.renderer.shape(text, direction="ltr")
        names, glyphs = [], []
        for gid, gx, _, _ in shaped.glyphs:
            names.append(self.order[gid])
            glyphs.append([[(x + gx, y) for x, y in pts] for _, pts in self.renderer.contours(gid)])
        return names, glyphs, shaped.advance


def check(shaper: Shaper, codage: str, min_iou: float):
    """(problem or None, IoU)."""
    names, glyphs, advance = shaper.run(C.to_text(codage))
    bad = [n for n in names if n in BAD]
    if bad:
        return f"shaped to {names}, which draws {bad[0]}", 0.0
    ref, want = reference(codage)
    if abs(advance - want) > 1:
        return f"advance {advance} is not {want}", 0.0
    width = max(want, advance)
    score = iou(raster(glyphs, width), raster(ref, width))
    if score < min_iou:
        return f"IoU {score:.4f} is below {min_iou}; shaped to {names}", score
    return None, score


def check_rejected(shaper: Shaper, codage: str):
    """A rejected fixture shapes to plain glyphs only: every glyph is a character's own."""
    names, _, _ = shaper.run(C.to_text(codage))
    variants = [n for n in names if "." in n and n not in ("ignorable.sub",)]
    if variants:
        return f"is rejected but shaped to variants {variants}"
    if any(n in BAD for n in names):
        return f"shaped to {names}, which draws the box"
    return None


WORKERS = min(8, os.process_cpu_count() or 1)
_worker = None


def _start(font: str, min_iou: float):
    global _worker
    _worker = (Shaper(Path(font)), min_iou)


def _check(codage: str):
    """``check`` in a pool worker, reporting an exception as the fixture's problem."""
    shaper, min_iou = _worker
    try:
        return check(shaper, codage, min_iou)
    except Exception as e:  # report the fixture, not a traceback
        return f"{type(e).__name__}: {e}", 0.0


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--font", default=str(FONT))
    ap.add_argument("--min-iou", type=float, default=0.98)
    ap.add_argument("--limit", type=int, default=0, help="check only the first N accepted fixtures")
    a = ap.parse_args()
    shaper = Shaper(Path(a.font))
    failures, worst = [], (2.0, "")
    todo = fixtures()
    if a.limit:
        todo = todo[: a.limit]
    with ProcessPoolExecutor(WORKERS, initializer=_start, initargs=(a.font, a.min_iou)) as pool:
        results = pool.map(_check, todo, chunksize=16)
        for i, (codage, (problem, score)) in enumerate(zip(todo, results), 1):
            if problem:
                failures.append(f"{a.font}: error: {codage}: {problem}")
            if score < worst[0]:
                worst = (score, codage)
            if i % 250 == 0:
                print(f"{i}/{len(todo)} fixtures", file=sys.stderr)
    for codage in REJECTED:
        problem = check_rejected(shaper, codage)
        if problem:
            failures.append(f"{a.font}: error: {codage}: {problem}")
    for f in failures[:60]:
        print(f)
    if len(failures) > 60:
        print(f"{a.font}: error: {len(failures) - 60} more failures")
    print(f"{a.font}: {len(todo)} blocks and {len(REJECTED)} rejected blocks; worst IoU {worst[0]:.4f} ({worst[1]}); "
          + ("ok" if not failures else f"{len(failures)} failures"))
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
