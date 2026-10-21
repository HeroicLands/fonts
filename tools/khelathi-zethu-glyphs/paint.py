# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""The paint map of Khelathi Zethu Glyphs: each drawn sign's enclosed regions and their colours.

    .venv/bin/python tools/khelathi-zethu-glyphs/paint.py [--out specimens/khelathi-zethu-glyphs/paint]
    .venv/bin/python tools/khelathi-zethu-glyphs/paint.py --regions DIR [--ids 01-002 ...]

`paint.json` gives, per sign id, the enclosed regions of the sign's default form, each by a
seed point in glyph units and a colour category. This module finds the regions, so every
reader of the map (the guard, the contact sheets, a renderer) finds the same ones:

- the sign's default form is rasterized from the built font at `K` pixels per font unit, and a
  pixel whose coverage passes one half is ink;
- a gap inside the outline narrower than about a hairline is closed with a disc of radius `SEAL`
  hairlines, so a leg whose line stops short of the kilt parts from the space between the legs;
- the open ground is whatever a ball of radius `BALL` hairlines can reach rolling in from
  outside the sign, so an outline left open by a hairline or two (a leg meeting a hip, an ankle
  short of its foot) still closes;
- every other connected white area is a region, except a speck smaller than `SPECK` hairlines
  square and a sliver the ball leaves in an outer corner, smaller than `SLIVER` square hairlines;
  a speck or sliver is painted as the region nearest it, so no paper shows inside the outline;
- regions are numbered in scan order, top to bottom and left to right, and a gap the seal closed
  is painted as the region beside it.

A region holding a seed takes the seed's category. A region with no seed takes the sign's
`default`, or else its group's entry in `defaults`; in the figure groups (`SEEDED_GROUPS`)
every region has a seed, and the default is never used.

Run as a script, it writes one contact sheet per group, each sign rendered large and painted
with a reference palette, to `specimens/khelathi-zethu-glyphs/paint/`, and `figures-check.png`,
every man and woman on their feet drawn larger, for checking kilts, legs and the ground
between the legs, and `kneeling-seated-beasts.png`, every kneeling or seated figure and every
beast. With `--regions` it writes the authoring sheets instead: each sign with its
regions tinted and numbered, and `centres.json`, the seed point of every region.
"""

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np
import pathops
from fontTools.pens.basePen import BasePen
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw
from scipy import ndimage

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE.parent))
from render import label_font  # noqa: E402

PAINT = HERE / "paint.json"
ENCODING = HERE / "encoding.json"
FONT = ROOT / "fonts" / "KhelathiZethuGlyphs-Regular.ttf"

HAIR = 12.0  # the drawn hairline, in font units
K = 0.5  # pixels per font unit at which regions are found
SEAL = 0.4  # the radius of the disc that closes a gap inside the outline, in hairlines
BALL = 1.15  # the radius of the ball that finds the open ground, in hairlines
SPECK = 1.2  # a region narrower than this many hairlines square is dropped
SLIVER = 6.0  # a region touching the open ground and under this many square hairlines is dropped
SS = 4  # supersampling of the raster
# Groups whose every region carries its own seed: a figure encloses air between its limbs, so no
# default can stand for an unnamed region.
SEEDED_GROUPS = ("01", "02", "03", "04", "05", "06")

# A reference palette for the contact sheets; each surface sets its own.
PALETTE = {
    "skin-male": (174, 56, 34),
    "skin-female": (222, 168, 88),
    "linen": (252, 251, 247),
    "hair": (32, 27, 26),
    "pottery": (178, 94, 50),
    "gold": (226, 180, 72),
    "faience": (36, 128, 168),
    "water": (30, 86, 170),
    "plant": (36, 124, 84),
    "red": (196, 52, 40),
    "cord": (196, 160, 96),
    "stone": (200, 192, 176),
    "wood": (140, 90, 44),
    "ground": (222, 206, 172),
}
INK = (59, 36, 20)
PAPER = (222, 206, 172)


def gname(sid: str) -> str:
    return "z" + sid.replace("-", "_") + ".a"


def load(path: Path = PAINT) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def encoding(path: Path = ENCODING) -> dict:
    return {e["id"]: e for e in json.loads(Path(path).read_text(encoding="utf-8"))["signs"]}


# -- the raster --------------------------------------------------------------------------------


class _PathPen(BasePen):
    """Draws a glyph into a skia path, curves flattened by skia itself."""

    def __init__(self, glyphs, path):
        super().__init__(glyphs)
        self.path = path

    def _moveTo(self, p):
        self.path.moveTo(*p)

    def _lineTo(self, p):
        self.path.lineTo(*p)

    def _qCurveToOne(self, c, p):
        self.path.quadTo(*c, *p)

    def _curveToOne(self, c1, c2, p):
        self.path.cubicTo(*c1, *c2, *p)

    def _closePath(self):
        self.path.close()

    _endPath = _closePath


class _Flatten(BasePen):
    def __init__(self):
        super().__init__(None)
        self.contours, self.cur = [], None

    def _moveTo(self, p):
        self.cur = [p]

    def _lineTo(self, p):
        self.cur.append(p)

    def _qCurveToOne(self, c, p):
        a = self._getCurrentPoint()
        n = max(4, int(math.hypot(p[0] - a[0], p[1] - a[1]) / 4) + 2)
        for i in range(1, n + 1):
            t = i / n
            m = 1 - t
            self.cur.append((m * m * a[0] + 2 * m * t * c[0] + t * t * p[0], m * m * a[1] + 2 * m * t * c[1] + t * t * p[1]))

    def _curveToOne(self, c1, c2, p):
        a = self._getCurrentPoint()
        n = 16
        for i in range(1, n + 1):
            t = i / n
            m = 1 - t
            self.cur.append(tuple(m ** 3 * a[j] + 3 * m * m * t * c1[j] + 3 * m * t * t * c2[j] + t ** 3 * p[j] for j in (0, 1)))

    def _closePath(self):
        if self.cur and len(self.cur) > 2:
            self.contours.append(self.cur)
        self.cur = None

    _endPath = _closePath


class Glyphs:
    """The built font's outlines, as the union of each glyph's contours under the nonzero rule."""

    def __init__(self, font: Path = FONT):
        self.tt = TTFont(str(font))
        self.gs = self.tt.getGlyphSet()
        self._contours = {}

    def __contains__(self, name):
        return name in self.gs

    def contours(self, name):
        if name not in self._contours:
            path = pathops.Path()
            self.gs[name].draw(_PathPen(self.gs, path))
            path.simplify(fix_winding=True)
            pen = _Flatten()
            path.draw(pen)
            self._contours[name] = pen.contours
        return self._contours[name]

    def bounds(self, name):
        pts = [p for c in self.contours(name) for p in c]
        if not pts:
            return 0, 0, 0, 0
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        return min(xs), min(ys), max(xs), max(ys)

    def raster(self, name, k, pad):
        """Coverage of the glyph's ink at k pixels per font unit, its bounds padded by pad pixels."""
        x0, y0, x1, y1 = self.bounds(name)
        w = int(math.ceil((x1 - x0) * k)) + 2 * pad
        h = int(math.ceil((y1 - y0) * k)) + 2 * pad
        acc = np.zeros((h * SS, w * SS), bool)
        for c in self.contours(name):
            m = Image.new("1", (w * SS, h * SS), 0)
            ImageDraw.Draw(m).polygon(
                [((x - x0) * k * SS + pad * SS, (h - pad) * SS - (y - y0) * k * SS) for x, y in c], fill=1)
            acc ^= np.array(m, bool)
        return acc.reshape(h, SS, w, SS).mean(axis=(1, 3))


def disk(r):
    yy, xx = np.mgrid[-r:r + 1, -r:r + 1]
    return (xx * xx + yy * yy) <= r * r


class Regions:
    """A sign's ink and its enclosed regions at k pixels per font unit.

    `ink` and `labels` are arrays of rows top down; `labels` is 0 on ink and open ground and
    1..n on the regions. `to_px` takes a point in glyph units to (row, column), and `to_units`
    takes a pixel back."""

    def __init__(self, glyphs: Glyphs, glyph: str, k: float = K):
        self.k = k
        self.hair = max(2.0, HAIR * k)
        r = max(2, int(math.ceil(self.hair * BALL)))
        self.pad = pad = r + 4
        self.x0, self.y0, _, _ = glyphs.bounds(glyph)
        self.coverage = glyphs.raster(glyph, k, pad)
        self.ink = self.coverage > 0.5
        rs = max(1, int(round(self.hair * SEAL)))
        sealed = ndimage.binary_closing(np.pad(self.ink, rs + 1), structure=disk(rs))[rs + 1:-rs - 1, rs + 1:-rs - 1]
        ink = sealed | self.ink
        bg = np.pad(~ink, r + 2, constant_values=True)
        core = ndimage.binary_erosion(bg, structure=disk(r), border_value=1)
        lab0, _ = ndimage.label(core)
        edge = np.unique(np.concatenate([lab0[0], lab0[-1], lab0[:, 0], lab0[:, -1]]))
        reach = ndimage.binary_dilation(np.isin(lab0, edge[edge > 0]), structure=disk(r))
        self.open = reach = reach[r + 2:-r - 2, r + 2:-r - 2]
        labels, n = ndimage.label(~ink & ~reach)
        keep = np.zeros(n + 1, bool)
        if n:
            areas = ndimage.sum_labels(np.ones_like(labels), labels, index=np.arange(n + 1))
            touch = np.zeros(n + 1, bool)
            touch[np.unique(labels[ndimage.binary_dilation(reach) & (labels > 0)])] = True
            keep = (areas >= max(4.0, (self.hair * SPECK) ** 2)) & ~(touch & (areas < SLIVER * self.hair ** 2))
            keep[0] = False
        labels, self.n = ndimage.label(keep[labels])
        # A gap the seal closed is painted as the region beside it, so it shows no seam.
        seam = ink & ~self.ink & ~reach
        if self.n and seam.any():
            dist, (rows, cols) = ndimage.distance_transform_edt(labels == 0, return_indices=True)
            seam &= dist <= rs + 1
            labels[seam] = labels[rows[seam], cols[seam]]
        # A speck or sliver too small to be a region is painted as the region nearest it, so no
        # paper shows inside the outline.
        specks = ~self.ink & ~reach & (labels == 0)
        if self.n and specks.any():
            _, (rows, cols) = ndimage.distance_transform_edt(labels == 0, return_indices=True)
            labels[specks] = labels[rows[specks], cols[specks]]
        self.labels = labels

    def unpainted(self):
        """Pixels inside the outline that belong to no region: paper that would show through.

        A sign with no region at all is drawn solid and has nothing to paint."""
        return 0 if not self.n else int((~self.ink & ~self.open & (self.labels == 0)).sum())

    def to_px(self, x, y):
        h = self.labels.shape[0]
        return int(round(h - 1 - ((y - self.y0) * self.k + self.pad))), int(round((x - self.x0) * self.k + self.pad))

    def to_units(self, row, col):
        h = self.labels.shape[0]
        return round((col - self.pad) / self.k + self.x0), round((h - 1 - row - self.pad) / self.k + self.y0)

    def at(self, x, y):
        """The region under a point: its number, or 0 with "ink", "open" or "outside"."""
        row, col = self.to_px(x, y)
        if not (0 <= row < self.labels.shape[0] and 0 <= col < self.labels.shape[1]):
            return 0, "outside"
        if self.labels[row, col]:
            return int(self.labels[row, col]), ""
        if self.ink[row, col]:
            return 0, "ink"
        return 0, "open"

    def centres(self):
        """The point of each region farthest from its edge, in glyph units, by region number."""
        out = {}
        for i, sl in enumerate(ndimage.find_objects(self.labels), start=1):
            if sl is None:
                continue
            m = np.pad(self.labels[sl] == i, 1)
            dt = ndimage.distance_transform_edt(m)
            row, col = np.unravel_index(dt.argmax(), dt.shape)
            out[i] = self.to_units(row - 1 + sl[0].start, col - 1 + sl[1].start)
        return out


def paints(paint: dict, sid: str, regions: Regions) -> dict:
    """The category of each region of a sign, by region number."""
    entry = paint["signs"][sid]
    default = entry.get("default") or paint["defaults"][sid[:2]]
    out = {i: default for i in range(1, regions.n + 1)}
    for reg in entry.get("regions", []):
        i, _ = regions.at(*reg["seed"])
        if i:
            out[i] = reg["paint"]
    return out


# -- the sheets --------------------------------------------------------------------------------


def outline_colour(category):
    if not category or category == "default":
        return INK
    return tuple(int(c * 0.45) for c in PALETTE[category])


def painted(regions: Regions, cats: dict, outline=None, scale=1):
    """An RGB image of the sign painted by category, its outline in ink."""
    img = np.empty(regions.labels.shape + (3,), np.uint8)
    img[:] = PAPER
    for i, cat in cats.items():
        img[regions.labels == i] = PALETTE[cat]
    a = regions.coverage[..., None]
    img = (img * (1 - a) + np.array(outline_colour(outline)) * a).astype(np.uint8)
    im = Image.fromarray(img)
    if scale != 1:
        im = im.resize((im.width * scale, im.height * scale), Image.LANCZOS)
    return im


def numbered(regions: Regions, scale=2):
    """An RGB image of the sign with each region tinted and numbered at its centre."""
    rng = np.random.default_rng(7)
    img = np.full(regions.labels.shape + (3,), 250, np.uint8)
    for i in range(1, regions.n + 1):
        img[regions.labels == i] = rng.integers(150, 236, 3)
    img[regions.open] = (255, 255, 255)
    img[regions.ink] = (0, 0, 0)
    im = Image.fromarray(img).resize((regions.labels.shape[1] * scale, regions.labels.shape[0] * scale), Image.NEAREST)
    d = ImageDraw.Draw(im)
    f = label_font(16)
    for i, (x, y) in regions.centres().items():
        row, col = regions.to_px(x, y)
        d.text((col * scale, row * scale), str(i), fill=(200, 0, 0), font=f, anchor="mm",
               stroke_width=2, stroke_fill=(255, 255, 255))
    return im


def sheet(tiles, cols, title, cell, out: Path):
    """Lay out (image, caption) tiles in a grid under a title, each fitted to a cell wide square."""
    fitted = []
    for im, caption in tiles:
        s = min(1.0, (cell - 12) / max(im.width, im.height))
        if s < 1:
            im = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.LANCZOS)
        fitted.append((im, caption))
    rows = [fitted[i:i + cols] for i in range(0, len(fitted), cols)]
    heights = [max(im.height for im, _ in row) + 30 for row in rows]
    head = 50
    page = Image.new("RGB", (cols * cell, head + sum(heights)), (250, 247, 240))
    d = ImageDraw.Draw(page)
    d.text((16, 12), title, fill=(30, 30, 30), font=label_font(24))
    cap = label_font(13)
    y = head
    for row, h in zip(rows, heights):
        for c, (im, caption) in enumerate(row):
            x = c * cell
            page.paste(im, (x + (cell - im.width) // 2, y + (h - 30 - im.height)))
            d.text((x + 6, y + h - 26), caption, fill=(60, 60, 60), font=cap)
        y += h
    page.quantize(64, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE).save(out, optimize=True)


GROUPS = [
    "Men", "Women", "Gods and their attributes", "The body", "Beasts", "Birds",
    "River creatures", "Plants and grain", "Sky, sun and stars", "Land, water and the river",
    "Buildings", "Boats", "Tools, weapons and measures", "Vessels and offerings",
    "Cloth, crowns and adornment", "Strokes and figures",
]


def slug(text: str) -> str:
    return "".join(c if c.isalnum() else "-" for c in text.lower()).strip("-").replace("--", "-")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--font", type=Path, default=FONT)
    ap.add_argument("--paint", type=Path, default=PAINT)
    ap.add_argument("--out", type=Path, default=ROOT / "specimens" / "khelathi-zethu-glyphs" / "paint")
    ap.add_argument("--regions", type=Path, help="write numbered authoring sheets to this directory instead")
    ap.add_argument("--ids", nargs="*", help="only these sign ids (or group numbers, such as 01)")
    ap.add_argument("--per", type=int, default=12, help="signs to an authoring sheet")
    args = ap.parse_args()
    glyphs = Glyphs(args.font)
    enc = encoding()
    ids = [s for s, e in enc.items() if e["drawn"]]
    if args.ids:
        ids = [s for s in ids if s in args.ids or s[:2] in args.ids]
    if args.regions:
        args.regions.mkdir(parents=True, exist_ok=True)
        dump = {}
        for j in range(0, len(ids), args.per):
            chunk = ids[j:j + args.per]
            tiles = []
            for sid in chunk:
                reg = Regions(glyphs, enc[sid]["glyph"])
                tiles.append((numbered(reg), f"{sid} {enc[sid]['subject'][:44]}"))
                dump[sid] = {str(i): xy for i, xy in reg.centres().items()}
            sheet(tiles, 4, f"regions {chunk[0]} to {chunk[-1]}", 420, args.regions / f"regions-{chunk[0]}.png")
        (args.regions / "centres.json").write_text(json.dumps(dump, indent=1), encoding="utf-8")
        return
    paint = load(args.paint)
    args.out.mkdir(parents=True, exist_ok=True)
    for g, name in enumerate(GROUPS, start=1):
        group = [s for s in ids if int(s[:2]) == g and s in paint["signs"]]
        if not group:
            continue
        tiles = []
        for sid in group:
            reg = Regions(glyphs, enc[sid]["glyph"])
            im = painted(reg, paints(paint, sid, reg), paint["signs"][sid].get("outline"), scale=1)
            tiles.append((im, f"{sid} {enc[sid]['subject'][:30]}"))
        sheet(tiles, 6, f"{g:02d} {name}: paint", 260, args.out / f"{g:02d}-{slug(name)}.png")
    figures = [s for s in ids if s[:2] in ("01", "02") and s in paint["signs"] and upright(enc[s]["subject"])]
    if figures:
        tiles = []
        for sid in figures:
            reg = Regions(glyphs, enc[sid]["glyph"])
            im = painted(reg, paints(paint, sid, reg), paint["signs"][sid].get("outline"), scale=2)
            tiles.append((im, f"{sid} {enc[sid]['subject'][:44]}"))
        sheet(tiles, 4, "Standing, walking and bending figures: kilt, legs and the ground between them", 480,
              args.out / "figures-check.png")
    low = [s for s in ids if s in paint["signs"] and (s[:2] == "05" or (s[:2] in ("01", "02", "03") and not upright(enc[s]["subject"])))]
    if low:
        tiles = []
        for sid in low:
            reg = Regions(glyphs, enc[sid]["glyph"])
            im = painted(reg, paints(paint, sid, reg), paint["signs"][sid].get("outline"), scale=2)
            tiles.append((im, f"{sid} {enc[sid]['subject'][:44]}"))
        sheet(tiles, 4, "Kneeling and seated figures, and beasts: the air under knees, arms and bellies", 480,
              args.out / "kneeling-seated-beasts.png")


SITTING = ("seated", "kneeling", "lying", "prostrate")


def upright(subject: str) -> bool:
    """A figure on its feet: the signs whose kilt and legs the figures sheet shows."""
    return not any(word in subject for word in SITTING)


if __name__ == "__main__":
    main()
