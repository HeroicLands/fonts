# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Set every glyph of a font source to its ink width and one sidebearing.

    .venv/bin/python tools/respace.py sources/<Font>.ufo [--sidebearing N] [--tighten N] [--space N]

Each glyph with an advance and ink is moved so that its ink starts ``SIDEBEARING``
units from its origin, and its advance becomes its ink width plus that sidebearing
on each side. The ink is measured with every component drawn in. The notdef and
the box keep their own advance, and so does every glyph with no advance or no
ink, such as a mark. The space takes the face's word space, ``SPACE``, where
``SPACING`` states one, and keeps its own advance otherwise.

What depends on a glyph's position moves with it:

- its anchors;
- each component it holds, so that the component's ink moves as the glyph's does;
- every ``pos base <glyph> <anchor x y>`` of ``features.fea``.

**Kerning.** In a face with a ``kern`` feature, each pair is rewritten so that the
two inks stand exactly ``TIGHTEN`` units closer than they stood before, and a pair of
respaced glyphs that had no kern is given one, so the optical spacing the kerning
holds is kept and tightened evenly.

**Followers.** A Qalezu Hand doubled sign or catch-before form (``<sign>.dbl``,
``<sign>.catch``, ``<sign>.dbl.catch``) moves with its sign and takes the sign's
advance; ``tools/qalezu-hand/apply_encoding.py`` writes those composites again
from the moved sign and must find nothing to change.

A source whose glyphs already all stand at the sidebearing is left as it is, apart
from its space, because a second run would tighten its kerning again. The files are edited as text, so
everything else in the source is untouched.

``SPACING`` holds each face's sidebearing, tightening and word space. Pirzath Hand's
generator, tools/pirzath-hand/build_ufo.py, spaces it at the sidebearing given here.
"""

import argparse
import plistlib
import re
import sys
from pathlib import Path

import ufoLib2
from fontTools.pens.boundsPen import BoundsPen

ROOT = Path(__file__).resolve().parent.parent
NUMBER = r"-?\d+(?:\.\d+)?"

# Each face's sidebearing, how many units its kerning tightens every pair, and its
# word space where the face sets one. Zethu's space is the gutter between two signs,
# so a phrase runs on as an inscription does.
SPACING = {
    "KhelathiZethuGlyphs": {"sidebearing": 31, "tighten": 0, "space": 62},
    "QalezuHand": {"sidebearing": 28, "tighten": 0, "space": 200},
    "ThuravarkCarved": {"sidebearing": 34, "tighten": 0},
    "PirzathCarved": {"sidebearing": 26, "tighten": 60},
    "SemaronKuriale": {"sidebearing": 12, "tighten": 0},
    "PirzathHand": {"sidebearing": 70, "tighten": 0, "space": 500},
}

KEEP = {".notdef", "notdef.box", "space"}
TOLERANCE = 1


def leader(face: str, name: str) -> str | None:
    """The glyph a follower moves with, or None."""
    if face == "QalezuHand" and (name.endswith(".dbl") or name.endswith(".catch")):
        return name.split(".")[0]
    return None


def ink(font: ufoLib2.Font, name: str):
    pen = BoundsPen(font)
    font[name].draw(pen)
    return pen.bounds


def plan(ufo: Path, sidebearing: int):
    """{glyph: (shift, new advance)} for every glyph that moves, and the old sidebearings."""
    face = ufo.stem
    font = ufoLib2.Font.open(ufo)
    moves, sides = {}, {}
    for glyph in font:
        b = ink(font, glyph.name)
        if b is None or glyph.width <= 0 or glyph.name in KEEP or leader(face, glyph.name):
            continue
        shift = round(sidebearing - b[0])
        moves[glyph.name] = (shift, round(b[2] + shift) + sidebearing)
        sides[glyph.name] = (b[0], glyph.width - b[2])
    for glyph in font:
        lead = leader(face, glyph.name)
        if lead and lead in moves:
            b = ink(font, lead)
            moves[glyph.name] = moves[lead]
            sides[glyph.name] = (b[0], font[lead].width - b[2])
    return font, moves, sides


def shift_attr(body: str, name: str, by: float) -> str:
    def repl(m):
        v = float(m.group(2)) + by
        return m.group(1) + (str(int(v)) if v == int(v) else f"{v:g}") + m.group(3)

    return re.sub(rf'(\b{name}=")({NUMBER})(")', repl, body)


def respace_glif(text: str, shift: int, advance: int, component_shift) -> str:
    text = re.sub(r'<advance\b[^>]*\bwidth="[^"]*"', lambda m: re.sub(r'width="[^"]*"', f'width="{advance}"', m.group(0)), text)
    text = re.sub(r"<point\s[^>]*>", lambda m: shift_attr(m.group(0), "x", shift), text)
    text = re.sub(r"<anchor\s[^>]*>", lambda m: shift_attr(m.group(0), "x", shift), text)

    def component(m):
        body = m.group(0)
        by = shift - component_shift(re.search(r'base="([^"]+)"', body).group(1))
        if not by:
            return body
        if "xOffset=" not in body:
            body = body.replace("<component ", '<component xOffset="0" ', 1)
        return shift_attr(body, "xOffset", by)

    return re.sub(r"<component\s[^>]*>", component, text)


def respace_features(text: str, moves, sides, sidebearing: int, tighten: int, glyph_names) -> str:
    shift = lambda g: moves.get(g, (0, 0))[0]  # noqa: E731

    text = re.sub(
        rf"(pos\s+base\s+(?:\S+)\s+<anchor\s+)({NUMBER})(\s+{NUMBER}\s*>)",
        lambda m: m.group(1) + str(round(float(m.group(2)) + shift(re.search(r"pos\s+base\s+(\S+)", m.group(0)).group(1)))) + m.group(3),
        text,
    )
    match = re.search(r"feature kern \{\n(.*?)\n\} kern;", text, re.S)
    if not match:
        return text

    def gain(a, b):
        """How many units closer the two inks stand once both glyphs are at the sidebearing."""
        right = sides[a][1] - sidebearing if a in moves else 0
        left = sides[b][0] - sidebearing if b in moves else 0
        return right + left

    pairs, lines = {}, []
    for line in match.group(1).split("\n"):
        m = re.match(rf"^(\s*)pos\s+(\S+)\s+(\S+)\s+({NUMBER})\s*;\s*$", line)
        if not m:
            lines.append(line)
            continue
        pairs[(m.group(2), m.group(3))] = float(m.group(4))
    names = [g for g in glyph_names if g in moves]
    for a in names:
        for b in names:
            pairs.setdefault((a, b), 0)
    out = []
    for (a, b), value in pairs.items():
        new = value + gain(a, b) - (tighten if a in moves and b in moves else 0)
        if round(new):
            out.append(f"  pos {a} {b} {round(new)};")
    body = "\n".join(lines + out)
    return text[: match.start(1)] + body + text[match.end(1):]


def set_space(files: dict, width: int, ufo: Path) -> None:
    path = files["space"]
    text = path.read_text(encoding="utf-8")
    path.write_text(re.sub(r'(<advance\b[^>]*\bwidth=")[^"]*(")', rf"\g<1>{width}\2", text), encoding="utf-8")
    print(f"{ufo}: the space is {width} units")


def apply(ufo: Path, sidebearing: int, tighten: int, space: int | None = None) -> None:
    font, moves, sides = plan(ufo, sidebearing)
    glyphs = ufo / "glyphs"
    files = {name: glyphs / f for name, f in plistlib.loads((glyphs / "contents.plist").read_bytes()).items()}
    if space is not None:
        set_space(files, space, ufo)
    if all(abs(s[0] - sidebearing) <= TOLERANCE and abs(s[1] - sidebearing) <= TOLERANCE
           for g, s in sides.items() if not leader(ufo.stem, g)):
        print(f"{ufo}: every glyph already stands at {sidebearing} units, so its glyphs are left as they are")
        return
    for name, path in files.items():
        if name not in moves:
            continue
        shift, advance = moves[name]
        text = path.read_text(encoding="utf-8")
        path.write_text(respace_glif(text, shift, advance, lambda b: moves.get(b, (0, 0))[0]), encoding="utf-8")
    fea = ufo / "features.fea"
    if fea.exists():
        fea.write_text(respace_features(fea.read_text(encoding="utf-8"), moves, sides, sidebearing, tighten, list(font.keys())), encoding="utf-8")
    print(f"{ufo}: {len(moves)} glyphs set to their ink and {sidebearing} units a side"
          + (f", kerning tightened by {tighten}" if tighten else ""))


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("ufo", nargs="+", type=Path)
    parser.add_argument("--sidebearing", type=int)
    parser.add_argument("--tighten", type=int)
    parser.add_argument("--space", type=int)
    args = parser.parse_args()
    for ufo in args.ufo:
        face = SPACING.get(ufo.stem)
        if face is None and args.sidebearing is None:
            raise SystemExit(f"error: {ufo} has no spacing in SPACING")
        sb = args.sidebearing if args.sidebearing is not None else face["sidebearing"]
        tighten = args.tighten if args.tighten is not None else (face or {}).get("tighten", 0)
        space = args.space if args.space is not None else (face or {}).get("space")
        apply(ufo, sb, tighten, space)


if __name__ == "__main__":
    sys.exit(main())
