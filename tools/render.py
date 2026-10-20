# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Shape text with HarfBuzz and rasterize the font's own outlines with Pillow.

Nothing here reads the glyph source: what is drawn is what the built font
carries, so a specimen shows the font as a page or a sheet shows it.
"""

from pathlib import Path

import uharfbuzz as hb
from fontTools.pens.recordingPen import RecordingPen
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

SUPERSAMPLE = 4
LABEL_FONT = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"


class Shaped:
    def __init__(self, glyphs, advance):
        self.glyphs = glyphs  # (gid, x_offset, y_offset, x_advance) in font units
        self.advance = advance


class Renderer:
    def __init__(self, font_path: Path):
        data = Path(font_path).read_bytes()
        self.tt = TTFont(str(font_path))
        self.upem = self.tt["head"].unitsPerEm
        self.order = self.tt.getGlyphOrder()
        self.hb_font = hb.Font(hb.Face(data))
        self.hb_font.scale = (self.upem, self.upem)
        self._contours = {}

    # -- shaping ------------------------------------------------------------

    def shape(self, text: str, features=None) -> Shaped:
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(self.hb_font, buf, features or {})
        glyphs = []
        pen_x = 0
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            glyphs.append((info.codepoint, pen_x + pos.x_offset, pos.y_offset, pos.x_advance))
            pen_x += pos.x_advance
        return Shaped(glyphs, pen_x)

    def glyph_names(self, text: str):
        return [self.order[g[0]] for g in self.shape(text).glyphs]

    # -- outlines -----------------------------------------------------------

    def contours(self, gid: int):
        """The glyph's contours as point lists, largest first."""
        if gid in self._contours:
            return self._contours[gid]
        name = self.order[gid]
        pen = RecordingPen()
        self.tt.getGlyphSet()[name].draw(pen)
        contours, current = [], []
        for op, args in pen.value:
            if op == "moveTo":
                current = [args[0]]
            elif op == "lineTo":
                current.append(args[0])
            elif op == "qCurveTo":
                current.extend(flatten_quadratic(current[-1], args))
            elif op == "closePath" and current:
                contours.append(current)
                current = []
        result = sorted(
            ((signed_area(c), c) for c in contours), key=lambda ac: -abs(ac[0])
        )
        self._contours[gid] = result
        return result

    # -- drawing ------------------------------------------------------------

    def draw(self, img: Image.Image, x: float, baseline: float, shaped: Shaped, size: float,
             color="black"):
        """Draw shaped glyphs at pixel size `size` per em, baseline at pixel `baseline`."""
        scale = size / self.upem * SUPERSAMPLE
        w, h = img.size
        layer = Image.new("L", (w * SUPERSAMPLE, h * SUPERSAMPLE), 0)
        d = ImageDraw.Draw(layer)
        for gid, gx, gy, _ in shaped.glyphs:
            ox = (x + 0) * SUPERSAMPLE + gx * scale
            oy = baseline * SUPERSAMPLE - gy * scale
            for area, pts in self.contours(gid):
                poly = [(ox + px * scale, oy - py * scale) for px, py in pts]
                # TrueType outer contours run clockwise in y-up coordinates,
                # which is a negative signed area; holes run the other way.
                d.polygon(poly, fill=255 if area < 0 else 0)
        mask = layer.resize((w, h), Image.LANCZOS)
        img.paste(Image.new("RGB", (w, h), color), (0, 0), mask)

    def text(self, img, x, baseline, text, size, color="black", features=None):
        shaped = self.shape(text, features)
        self.draw(img, x, baseline, shaped, size, color)
        return shaped.advance * size / self.upem

    def width(self, text, size, features=None):
        return self.shape(text, features).advance * size / self.upem


def flatten_quadratic(start, args, steps=32):
    """The points along a TrueType quadratic run: off-curve points, then the on-curve end.

    Consecutive off-curve points imply an on-curve point midway between them.
    """
    offs, end = list(args[:-1]), args[-1]
    ons = [((a[0] + b[0]) / 2, (a[1] + b[1]) / 2) for a, b in zip(offs, offs[1:])] + [end]
    out, p0 = [], start
    for c, p1 in zip(offs, ons):
        for s in range(1, steps + 1):
            t = s / steps
            u = 1 - t
            out.append((u * u * p0[0] + 2 * u * t * c[0] + t * t * p1[0],
                        u * u * p0[1] + 2 * u * t * c[1] + t * t * p1[1]))
        p0 = p1
    if not offs:
        out.append(end)
    return out


def signed_area(pts):
    a = 0.0
    for (x1, y1), (x2, y2) in zip(pts, pts[1:] + pts[:1]):
        a += x1 * y2 - x2 * y1
    return a / 2


def label_font(size):
    try:
        return ImageFont.truetype(LABEL_FONT, int(size))
    except OSError:
        return ImageFont.load_default()
