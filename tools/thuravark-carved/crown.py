# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Add the crowned frame of the imperial recension to a built Thuravark Carved font.

    .venv/bin/python tools/thuravark-carved/crown.py fonts/ThuravarkCarved-Regular.ttf

``build.sh`` runs this on the font fontmake writes, before the Macintosh names and
the WOFF2. The result depends only on the font it reads, so a build is reproducible.

**The text.** A crowned name is typed between the two crown marks, ``crown.open``
(U+F0150) and ``crown.close`` (U+F0151). Between them the font cuts a frame of
straight grooves round the run: a post at each end and a rail above and below,
all of half the stem's weight. An open with no close within ``LONGEST`` glyphs, or a
close with no open, stays a bare post, a visible mark, and nothing else changes.

**The glyphs.** The two marks are drawn in the source as bare posts. This tool
reads the frame's measures from the open post, its bottom, its top and its
weight, and adds

- ``crown.open.rail`` and ``crown.close.rail``, each post joined to the rails
  over its own advance;
- ``<glyph>.crown`` for every glyph a name may hold (every glyph but the notdef,
  the box and the two marks): the glyph's own outline with the rails over its
  own advance, so the rails meet end to end whatever the frame holds. A glyph
  with no advance keeps no rails.

**The shaping**, in ``rclt``, which every shaper applies and no style sheet turns
off, reading the run left to right: the open becomes the opened post when a
close follows within ``LONGEST`` glyphs of the frame's kind; a glyph after the
opened post or a crowned glyph takes its crowned form; the close after either
becomes the closed post. A crowned run can only begin at an opened post, and the
closed post ends it, so no rule needs to look past the next glyph but the
open's.
"""

import sys
from pathlib import Path

from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
FEATURES = ROOT / "sources" / "ThuravarkCarved.ufo" / "features.fea"

OPEN, CLOSE = "crown.open", "crown.close"
RAIL = ".rail"  # a post joined to the rails
CROWNED = ".crown"  # a glyph's form inside the frame
LONGEST = 40  # the most glyphs a crown holds
OUTSIDE = {".notdef", "notdef.box", OPEN, CLOSE}


def inside(order: list[str]) -> list[str]:
    """The glyphs a crown may hold, in glyph order."""
    return [g for g in order if g not in OUTSIDE and not g.endswith((RAIL, CROWNED))]


def crowned_names(order: list[str]) -> list[str]:
    return [g + CROWNED for g in inside(order)]


def not_characters(order: list[str]) -> dict[str, str]:
    """The glyphs this tool adds, with why each is not a character."""
    out = {OPEN + RAIL: "the open crown mark joined to the frame's rails", CLOSE + RAIL: "the close crown mark joined to the frame's rails"}
    out.update({g + CROWNED: "the glyph inside a crowned frame, with the rails over its advance" for g in inside(order)})
    return out


# --- the drawing -----------------------------------------------------------------


def measures(font: TTFont) -> tuple[float, float, float]:
    """The frame's bottom, its top and its weight, from the open post."""
    g = font["glyf"][OPEN]
    return g.yMin, g.yMax, g.xMax - g.xMin


def bands(font: TTFont):
    bottom, top, weight = measures(font)
    return (bottom, bottom + weight), (top - weight, top)


def clockwise(points):
    """TrueType outer contours run clockwise in y-up coordinates."""
    area = 0.0
    for (x1, y1), (x2, y2) in zip(points, points[1:] + points[:1]):
        area += x1 * y2 - x2 * y1
    return points[::-1] if area > 0 else points


def rectangle(x0, x1, y0, y1):
    return clockwise([(x0, y0), (x1, y0), (x1, y1), (x0, y1)])


def draw(contours, components_from=None):
    pen = TTGlyphPen(components_from)
    for c in contours:
        pen.moveTo(c[0])
        for p in c[1:]:
            pen.lineTo(p)
        pen.closePath()
    return pen


def outline(font: TTFont, name: str) -> list[list[tuple]]:
    """The glyph's straight-edged contours, every component drawn in."""
    glyphs = font.getGlyphSet()
    pen = DecomposingRecordingPen(glyphs)
    glyphs[name].draw(pen)
    contours, current = [], []
    for op, args in pen.value:
        if op == "moveTo":
            current = [args[0]]
        elif op == "lineTo":
            current.append(args[0])
        elif op == "closePath":
            if current:
                contours.append(current)
            current = []
        else:
            raise ValueError(f"{name}: a {op} in a straight-cut glyph")
    return contours


def crowned(font: TTFont, name: str):
    """The glyph's outline with the rails over its advance."""
    advance = font["hmtx"][name][0]
    contours = outline(font, name)
    if advance > 0:
        for y0, y1 in bands(font):
            contours.append(rectangle(0, advance, y0, y1))
    return draw(contours).glyph(), advance


def opened_post(font: TTFont):
    """The open post with the rails running on to its advance edge: one groove."""
    g = font["glyf"][OPEN]
    advance = font["hmtx"][OPEN][0]
    (b0, b1), (t0, t1) = bands(font)
    x0, x1 = g.xMin, g.xMax
    points = [(x0, b0), (advance, b0), (advance, b1), (x1, b1), (x1, t0), (advance, t0), (advance, t1), (x0, t1)]
    return draw([clockwise(points)]).glyph(), advance


def closed_post(font: TTFont):
    """The close post with the rails running in from its origin: one groove."""
    g = font["glyf"][CLOSE]
    advance = font["hmtx"][CLOSE][0]
    (b0, b1), (t0, t1) = bands(font)
    x0, x1 = g.xMin, g.xMax
    points = [(0, b0), (x1, b0), (x1, t1), (0, t1), (0, t0), (x0, t0), (x0, b1), (0, b1)]
    return draw([clockwise(points)]).glyph(), advance


# --- the shaping -----------------------------------------------------------------


def features(order: list[str]) -> str:
    held = inside(order)
    forms = crowned_names(order)
    lines = [
        "# The crowned frame, written by tools/thuravark-carved/crown.py.",
        f"@CROWN_IN = [{' '.join(held)}];",
        f"@CROWN_FORM = [{' '.join(forms)}];",
        "lookup crown_form {",
        "  sub @CROWN_IN by @CROWN_FORM;",
        "} crown_form;",
        "lookup crown_open {",
        f"  sub {OPEN} by {OPEN}{RAIL};",
        "} crown_open;",
        "lookup crown_close {",
        f"  sub {CLOSE} by {CLOSE}{RAIL};",
        "} crown_close;",
        "feature rclt {",
        "  lookup crown {",
    ]
    for k in range(LONGEST):
        ahead = " ".join(["@CROWN_IN"] * k + [CLOSE])
        lines.append(f"    sub {OPEN}' lookup crown_open {ahead};")
    lines += [
        f"    sub [{OPEN}{RAIL} @CROWN_FORM] @CROWN_IN' lookup crown_form;",
        f"    sub [{OPEN}{RAIL} @CROWN_FORM] {CLOSE}' lookup crown_close;",
        "  } crown;",
        "} rclt;",
        "",
    ]
    return "\n".join(lines)


def apply(path: Path) -> None:
    font = TTFont(str(path))
    order = list(font.getGlyphOrder())
    glyf, hmtx = font["glyf"], font["hmtx"]
    new = {OPEN + RAIL: opened_post(font), CLOSE + RAIL: closed_post(font)}
    for name in inside(order):
        new[name + CROWNED] = crowned(font, name)
    for name, (glyph, advance) in new.items():
        order.append(name)
        glyf.glyphs[name] = glyph
        hmtx.metrics[name] = (advance, 0)
    font.setGlyphOrder(order)
    glyf.glyphOrder = order
    for name in new:
        g = glyf[name]
        g.recalcBounds(glyf)
        hmtx.metrics[name] = (hmtx.metrics[name][0], g.xMin if g.numberOfContours else 0)
    font["maxp"].numGlyphs = len(order)
    if font["post"].formatType == 2.0:
        font["post"].extraNames = []
        font["post"].mapping = {}
    # The source's features are compiled again with the frame's lookups after them,
    # so their feature names are written once.
    font["name"].names = [n for n in font["name"].names if n.nameID < 256]
    for tag in ("GSUB", "GPOS", "GDEF"):
        if tag in font:
            del font[tag]
    fea = FEATURES.read_text(encoding="utf-8") + "\n" + features(order)
    addOpenTypeFeaturesFromString(font, fea, filename=str(FEATURES))
    font.save(str(path))


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "fonts" / "ThuravarkCarved-Regular.ttf"
    apply(path)
    print(f"{path}: the crowned frame added")


if __name__ == "__main__":
    main()
