# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Confirm that every character a font does not use prints the box.

    .venv/bin/python tools/notdef_box.py [font ...]

A missing cmap entry makes a browser, Foundry or Typst fall back to the next font
in the stack, and an entry that points at glyph 0 is treated as missing, so a
stray character prints as an ordinary Latin glyph. Each font therefore carries
the glyph ``notdef.box``, a copy of ``.notdef``, and maps to it every code point
of these ranges that its typing does not use:

- U+0021-007E Basic Latin;
- U+00A1-00FF Latin-1 Supplement;
- U+0100-017F Latin Extended-A;
- U+2010-205E General Punctuation.

The typing is read from the font: a code point is used when its cmap entry reaches
a glyph other than the box. A used code point must reach a glyph that draws, except
the glyphs that deliberately draw nothing: the one the font gives space, the one it
gives the default-ignorables, and the one it gives the hyphen-minus.

A font fails when

- a code point of the ranges is unmapped;
- a code point maps to glyph 0;
- ``notdef.box`` is missing, is glyph 0, or differs from ``.notdef`` in outline or
  advance;
- a default-ignorable of the ranges (U+202A-202E) does not map to an empty glyph;
- a used code point reaches a glyph that draws nothing and is none of the three
  exceptions;
- the OS/2 winAscent or winDescent is smaller than the highest or lowest ink of any
  glyph, which Windows clips.
"""

import sys
from pathlib import Path

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
BOX = "notdef.box"
RANGES = [(0x21, 0x7E), (0xA1, 0xFF), (0x100, 0x17F), (0x2010, 0x205E)]
# The default-ignorable characters inside the ranges.
IGNORABLE = range(0x202A, 0x202F)
SPACE = 0x20
HYPHEN = 0x2D


def codepoints() -> list[int]:
    return [cp for lo, hi in RANGES for cp in range(lo, hi + 1)]


def outline(font: TTFont, name: str):
    pen = DecomposingRecordingPen(font.getGlyphSet())
    font.getGlyphSet()[name].draw(pen)
    return pen.value


def draws(font: TTFont, name: str) -> bool:
    return bool(outline(font, name))


def check(path: Path) -> list[str]:
    """Return the problems of the built font at path, each ``path: message``."""
    font = TTFont(str(path))
    cmap = font.getBestCmap()
    order = font.getGlyphOrder()
    problems = []
    if BOX not in order:
        problems.append(f"{path}: error: the font has no {BOX} glyph")
    else:
        if order[0] == BOX:
            problems.append(f"{path}: error: {BOX} is glyph 0; it must be a separate glyph")
        if font["hmtx"][BOX][0] != font["hmtx"][".notdef"][0]:
            problems.append(f"{path}: error: {BOX} and .notdef differ in advance")
        if outline(font, BOX) != outline(font, ".notdef"):
            problems.append(f"{path}: error: {BOX} and .notdef differ in outline")
        if not draws(font, BOX):
            problems.append(f"{path}: error: {BOX} draws nothing")
    quiet = {cmap.get(SPACE), cmap.get(HYPHEN)} - {None}
    unmapped, glyph0, empty_ignorable, silent = [], [], [], []
    for cp in codepoints():
        name = cmap.get(cp)
        if name is None:
            unmapped.append(cp)
        elif name == order[0]:
            glyph0.append(cp)
        elif cp in IGNORABLE:
            if draws(font, name):
                empty_ignorable.append(cp)
        elif name != BOX and not draws(font, name) and name not in quiet:
            silent.append(cp)
    for label, found in (
        ("is unmapped, so a fallback font draws it", unmapped),
        ("maps to glyph 0, which engines treat as missing", glyph0),
        ("is a default-ignorable that draws", empty_ignorable),
        ("is used by the typing but draws nothing", silent),
    ):
        for cp in found:
            problems.append(f"{path}: error: U+{cp:04X} {label}")
    problems += metrics(path, font)
    return problems


def metrics(path: Path, font: TTFont) -> list[str]:
    """The glyphs whose ink lies outside the OS/2 win metrics, as ``path: error: ...`` lines."""
    glyphs = font.getGlyphSet()
    os2 = font["OS/2"]
    top, bottom, high, low = None, None, os2.usWinAscent, os2.usWinDescent
    for name in font.getGlyphOrder():
        pen = BoundsPen(glyphs)
        glyphs[name].draw(pen)
        if pen.bounds is None:
            continue
        if top is None or pen.bounds[3] > top[1]:
            top = (name, pen.bounds[3])
        if bottom is None or pen.bounds[1] < bottom[1]:
            bottom = (name, pen.bounds[1])
    out = []
    if top and top[1] > high:
        out.append(f"{path}: error: {top[0]} reaches y {top[1]:g}, above winAscent {high}")
    if bottom and -bottom[1] > low:
        out.append(f"{path}: error: {bottom[0]} reaches y {bottom[1]:g}, below -winDescent {low}")
    return out


def summary(path: Path) -> str:
    font = TTFont(str(path))
    cmap = font.getBestCmap()
    cps = codepoints()
    boxed = sum(1 for cp in cps if cmap.get(cp) == BOX)
    return f"{path}: {len(cps)} code points walked, {boxed} on {BOX}, {len(cps) - boxed} used by the typing"


def main():
    paths = [Path(a) for a in sys.argv[1:]] or sorted((ROOT / "fonts").glob("*-Regular.ttf"))
    status = 0
    for p in paths:
        problems = check(p)
        print(summary(p) if not problems else f"{p}: {len(problems)} problems")
        for line in problems[:10]:
            print(line)
        if len(problems) > 10:
            print(f"{p}: error: ... and {len(problems) - 10} more")
        status |= bool(problems)
    sys.exit(status)


if __name__ == "__main__":
    main()
