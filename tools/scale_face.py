# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Scale a font source to the shared vertical standard.

    .venv/bin/python tools/scale_face.py sources/<Font>.ufo

The factor comes from tools/vertical.py, which also defines the vertical metrics. The
whole face is multiplied about the origin by that factor:

- every outline point, anchor, component offset and advance width of the glyphs;
- every kerning value and anchor position of ``features.fea``;
- the underline position and thickness;
- the font's xHeight and capHeight, recomputed from the scaled outlines.

Coordinates are rounded to integers, halves upward. The font's hhea and OS/2 vertical
metrics and its ascender and descender take Monaspace Neon's values and OS/2 USE_TYPO_METRICS is set. The files are
edited as text, so everything else in the source is untouched. A source whose
metrics already are Neon's has been scaled and is refused, because a second run
would scale it again.
"""

import math
import re
import sys
from fractions import Fraction
from pathlib import Path

import ufoLib2

sys.path.insert(0, str(Path(__file__).resolve().parent))
import vertical  # noqa: E402

NUMBER = r"-?\d+(?:\.\d+)?"


def scaler(factor: str):
    """A function that multiplies a number written as text and rounds it to an integer."""
    f = Fraction(factor)

    def scale(text: str) -> str:
        return str(math.floor(Fraction(text) * f + Fraction(1, 2)))

    return scale


def scale_tag(text: str, tag: str, attributes: tuple[str, ...], scale) -> str:
    """Scale the named attributes of every ``<tag .../>`` element in a glif."""

    def element(match):
        body = match.group(0)
        for name in attributes:
            body = re.sub(rf'(\b{name}=")({NUMBER})(")', lambda m: m.group(1) + scale(m.group(2)) + m.group(3), body)
        return body

    return re.sub(rf"<{tag}\s[^>]*>", element, text)


def scale_glif(text: str, scale) -> str:
    text = scale_tag(text, "advance", ("width", "height"), scale)
    text = scale_tag(text, "point", ("x", "y"), scale)
    text = scale_tag(text, "anchor", ("x", "y"), scale)
    return scale_tag(text, "component", ("xOffset", "yOffset"), scale)


def scale_features(text: str, scale) -> str:
    """Scale the kerning values and anchors of the feature file; comments stay as written."""
    out = []
    for line in text.split("\n"):
        code, hash_, comment = line.partition("#")
        code = re.sub(
            rf"(<anchor\s+)({NUMBER})(\s+)({NUMBER})(\s*>)",
            lambda m: m.group(1) + scale(m.group(2)) + m.group(3) + scale(m.group(4)) + m.group(5),
            code,
        )
        code = re.sub(
            rf"^(\s*pos\s+\S+\s+\S+\s+)({NUMBER})(\s*;)",
            lambda m: m.group(1) + scale(m.group(2)) + m.group(3),
            code,
        )
        out.append(code + hash_ + comment)
    return "\n".join(out)


def leftover_numbers(text: str) -> list[str]:
    """The numbers of a feature file that scaling left alone, other than ``lookupflag``."""
    found = []
    for line in text.split("\n"):
        code = line.partition("#")[0]
        code = re.sub(r'"[^"]*"', "", code)
        code = re.sub(rf"<anchor\s+{NUMBER}\s+{NUMBER}\s*>", "", code)
        code = re.sub(rf"^\s*pos\s+\S+\s+\S+\s+{NUMBER}\s*;", "", code)
        code = re.sub(r"\blookupflag\s+\d+\s*;", "", code)
        found += re.findall(rf"(?<![\w.@-])({NUMBER})(?![\w.])", code)
    return found


INTEGER_KEYS = {
    "ascender": vertical.ASCENT,
    "descender": vertical.DESCENT,
    "openTypeHheaAscender": vertical.ASCENT,
    "openTypeHheaDescender": vertical.DESCENT,
    "openTypeHheaLineGap": vertical.LINE_GAP,
    "openTypeOS2TypoAscender": vertical.ASCENT,
    "openTypeOS2TypoDescender": vertical.DESCENT,
    "openTypeOS2TypoLineGap": vertical.LINE_GAP,
}


def set_integer(text: str, key: str, value: int) -> str:
    pattern = rf"(<key>{key}</key>\s*<integer>)(-?\d+)(</integer>)"
    if not re.search(pattern, text):
        raise SystemExit(f"error: fontinfo.plist has no {key}")
    return re.sub(pattern, lambda m: m.group(1) + str(value) + m.group(3), text)


def set_selection(text: str) -> str:
    """Add bit 7, USE_TYPO_METRICS, to openTypeOS2Selection."""
    match = re.search(r"(<key>openTypeOS2Selection</key>\s*<array>)(.*?)(\s*</array>)", text, re.S)
    if match:
        bits = {int(b) for b in re.findall(r"<integer>(\d+)</integer>", match.group(2))} | {7}
        items = "".join(f"\n      <integer>{b}</integer>" for b in sorted(bits))
        return text[: match.start()] + match.group(1) + items + match.group(3) + text[match.end() :]
    block = "    <key>openTypeOS2Selection</key>\n    <array>\n      <integer>7</integer>\n    </array>\n"
    marker = "    <key>openTypeOS2Type</key>\n"
    if marker not in text:
        raise SystemExit("error: fontinfo.plist has no openTypeOS2Type to place the selection before")
    return text.replace(marker, block + marker, 1)


def scaled_win(ufo: Path) -> tuple[int, int]:
    """The win ascent and descent: Neon's, or the glyph boxes where they reach farther."""
    font = ufoLib2.Font.open(ufo)
    tops, bottoms = [], []
    for glyph in font:
        b = glyph.getControlBounds(font)
        if b:
            tops.append(b[3])
            bottoms.append(b[1])
    return max(vertical.WIN_ASCENT, math.ceil(max(tops))), max(vertical.WIN_DESCENT, math.ceil(-min(bottoms)))


def design_heights(ufo: Path) -> tuple[int, int]:
    """The font's xHeight and capHeight: the median height of its typical letters."""
    face = ufo.stem
    font = ufoLib2.Font.open(ufo)
    ink = {g.name: b for g in font if (b := g.getBounds(font))}
    return (
        round(vertical.median_height(ink, vertical.typical(face, "x"))),
        round(vertical.median_height(ink, vertical.typical(face, "cap"))),
    )


def apply(ufo: Path) -> None:
    face = ufo.stem
    if face not in vertical.SCALES:
        raise SystemExit(f"error: {ufo} is not a face of tools/vertical.py")
    info_path = ufo / "fontinfo.plist"
    info = info_path.read_text(encoding="utf-8")
    if re.search(rf"<key>openTypeHheaAscender</key>\s*<integer>{vertical.ASCENT}</integer>", info):
        raise SystemExit(f"error: {ufo} already has the shared vertical metrics, so it has been scaled")
    scale = scaler(str(vertical.SCALES[face]))
    for glif in sorted((ufo / "glyphs").glob("*.glif")):
        glif.write_text(scale_glif(glif.read_text(encoding="utf-8"), scale), encoding="utf-8")
    fea_path = ufo / "features.fea"
    fea = scale_features(fea_path.read_text(encoding="utf-8"), scale)
    left = leftover_numbers(fea)
    if left:
        raise SystemExit(f"error: {fea_path} has numbers that scaling did not handle: {left[:5]}")
    fea_path.write_text(fea, encoding="utf-8")
    for key in ("postscriptUnderlinePosition", "postscriptUnderlineThickness"):
        match = re.search(rf"<key>{key}</key>\s*<integer>(-?\d+)</integer>", info)
        if match:
            info = set_integer(info, key, int(scale(match.group(1))))
    for key, value in INTEGER_KEYS.items():
        info = set_integer(info, key, value)
    info = set_selection(info)
    info_path.write_text(info, encoding="utf-8")
    x, cap = design_heights(ufo)
    win_ascent, win_descent = scaled_win(ufo)
    info = info_path.read_text(encoding="utf-8")
    for key, value in (
        ("xHeight", x),
        ("capHeight", cap),
        ("openTypeOS2WinAscent", win_ascent),
        ("openTypeOS2WinDescent", win_descent),
    ):
        info = set_integer(info, key, value)
    info_path.write_text(info, encoding="utf-8")
    print(f"{ufo}: scaled by {vertical.SCALES[face]}; xHeight {x}, capHeight {cap}, win {win_ascent}/{win_descent}")


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    for arg in sys.argv[1:]:
        apply(Path(arg))


if __name__ == "__main__":
    main()
