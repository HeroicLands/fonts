# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Shape Veldikko's fixtures and assert the font sets each one rightly.

    .venv/bin/python tools/veldikko/guard.py [--font fonts/Veldikko-Regular.ttf]

Each fixture in ``fixtures.json`` is a sequence of Veldikko's glyph codes
(``tools/codes/veldikko.json``), with ``U+0020`` for the space: a letter, then the
doubling bar if the consonant is doubled, then each vowel mark, each followed by its
signs of length, pitch and emphasis. It is shaped right to left, and the guard asserts
what the font must do with it:

- **the glyphs.** The run is the sequence in visual order, a word's last
  letter first, with neither ``.notdef`` nor the box. Each letter is in the form
  its place gives it: isolated alone, initial first, final last, medial between,
  the initial and medial stretched (``.wide``) when the letter carries a long or
  pitched vowel or a diphthong. Each vowel is one mark with its length, pitch and
  emphasis signs folded in;
- **the marks.** A lone vowel mark stands at the ``mark`` anchor its letter's
  form carries in ``sources/Veldikko.ufo``; the two marks of a diphthong
  stand centred on it, the first said to the right; the length bar stands at the
  ``bar`` anchor. Two units of rounding are allowed.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import ufoLib2
from fontTools.pens.boundsPen import BoundsPen

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE.parent))
import codes  # noqa: E402
from render import Renderer  # noqa: E402

ENCODING = HERE / "encoding.json"
FIXTURE_FILE = HERE / "fixtures.json"
SOURCE = ROOT / "sources" / "Veldikko.ufo"
SCRIPT = "veldikko"
TOLERANCE = 2
DIPHTHONG_GAP = 15  # the least clear space between the two marks of a diphthong
DIPHTHONG_SLACK = 40  # how far a diphthong's ink may stand off its letter's mark point, for the slant
MODIFIERS = ("long", "rise", "fall", "emph")


def load_encoding():
    enc = json.loads(ENCODING.read_text(encoding="utf-8"))
    name_of = {chr(int(g["codepoint"][2:], 16)): g for g in enc["glyphs"]}
    return name_of


NAME_OF = load_encoding()
FIXTURES = [f["codes"] for f in json.loads(FIXTURE_FILE.read_text(encoding="utf-8"))["fixtures"]]


def glyphs_of(text: str) -> list[str]:
    return ["space" if c == " " else NAME_OF[c]["glyph"] for c in text]


def vowel_name(base: str, mods: set[str]) -> str:
    parts = [base] + [m for m in MODIFIERS if m in mods]
    return ".".join(parts)


def expected(glyphs: list[str]) -> list[str]:
    """The glyph run the font must give a text, in visual order."""
    kinds = {g["glyph"]: g["kind"] for g in NAME_OF.values()}
    out = []
    for word in " ".join(glyphs).split(" space "):
        items = word.split()
        clusters = []  # [letter, [marks as typed]]
        for g in items:
            if kinds.get(g) == "letter" or not clusters:
                clusters.append([g, []])
            else:
                clusters[-1][1].append(g)
        letters = [c for c in clusters if kinds.get(c[0]) == "letter"]
        n = len(letters)
        seq = []
        index = 0
        for head, marks in clusters:
            folded, current = [], None
            for m in marks:
                if kinds.get(m) == "vowel":
                    current = [m, set()]
                    folded.append(current)
                elif m in MODIFIERS and current is not None:
                    current[1].add(m)
                else:
                    folded.append([m, None])
            vowels = [f for f in folded if f[1] is not None]
            if kinds.get(head) == "letter":
                form = "isol" if n == 1 else "init" if index == 0 else "fina" if index == n - 1 else "medi"
                index += 1
                name = head if form == "isol" else f"{head}.{form}"
                if form in ("init", "medi") and (
                    len(vowels) > 1 or any({"long", "rise", "fall"} & mods for _, mods in vowels)
                ):
                    name += ".wide"
                seq.append(name)
            else:
                seq.append(head)
            seq += [vowel_name(m, mods) if mods is not None else m for m, mods in folded]
        out.append(seq)
    run = []
    for i, seq in enumerate(out):
        if i:
            run.append("space")
        run += seq
    return run[::-1]


def anchors() -> dict[str, dict[str, tuple[int, int]]]:
    """The ``mark`` and ``bar`` anchors of every letter form in the source."""
    font = ufoLib2.Font.open(SOURCE, lazy=True)
    return {g.name: {a.name: (a.x, a.y) for a in g.anchors} for g in font if g.anchors}


def placement(names: list[str], shaped, points, ink) -> list[str]:
    """What is wrong with where the marks of a shaped run stand. ``ink`` gives a
    glyph's ink as (left, right)."""
    problems = []
    glyphs = [(names[i], x, y) for i, (_, x, y, _) in enumerate(shaped.glyphs)]
    i = 0
    while i < len(glyphs):
        j = i
        while j < len(glyphs) and glyphs[j][0] not in points:
            j += 1
        if j == len(glyphs):
            break
        base, bx, _ = glyphs[j]
        run = glyphs[i:j]
        vowels = [g for g in run if g[0] != "bar" and g[0] != "space"]
        mx, my = points[base]["mark"]
        if len(vowels) == 1:
            _, x, y = vowels[0]
            if abs(x - bx - mx) > TOLERANCE or abs(y - my) > TOLERANCE:
                problems.append(f"{vowels[0][0]} over {base} at ({x - bx}, {y}), expected ({mx}, {my})")
        elif len(vowels) == 2:
            (g2, x2, y2), (g1, x1, y1) = vowels
            left, right = ink(g2), ink(g1)
            gap = (x1 + right[0]) - (x2 + left[1])
            middle = ((x2 + left[0]) + (x1 + right[1])) / 2 - bx
            if abs(y1 - my) > TOLERANCE or abs(y2 - my) > TOLERANCE:
                problems.append(f"the diphthong over {base} stands at y {y1} and {y2}, expected {my}")
            if gap < DIPHTHONG_GAP:
                problems.append(f"the diphthong over {base}: the first mark said is {gap:g} units right of the "
                                f"second, expected at least {DIPHTHONG_GAP}")
            if abs(middle - mx) > DIPHTHONG_SLACK:
                problems.append(f"the diphthong over {base} is centred at {middle:g}, expected {mx}")
        for g, x, y in run:
            if g == "bar":
                ax, _ = points[base]["bar"]
                if abs(x - bx - ax) > TOLERANCE or y != 0:
                    problems.append(f"the bar under {base} at ({x - bx}, {y}), expected ({ax}, 0)")
        i = j + 1
    return problems


def check_one(r: Renderer, points, label: str, text: str) -> list[str]:
    want = expected(glyphs_of(text))
    shaped = r.shape(text, direction="rtl")
    got = [r.order[g[0]] for g in shaped.glyphs]
    if ".notdef" in got or "notdef.box" in got:
        return [f"{label}: .notdef or the box in {got}"]
    if got != want:
        return [f"{label}: shaped {got}, expected {want}"]
    return [f"{label}: {p}" for p in placement(got, shaped, points, r.ink)]


class Shaper(Renderer):
    def __init__(self, path: Path):
        super().__init__(path)
        self._ink = {}

    def ink(self, name: str) -> tuple[float, float]:
        if name not in self._ink:
            glyphs = self.tt.getGlyphSet()
            pen = BoundsPen(glyphs)
            glyphs[name].draw(pen)
            self._ink[name] = (pen.bounds[0], pen.bounds[2]) if pen.bounds else (0.0, 0.0)
        return self._ink[name]


def run(font: Path) -> list[str]:
    r = Shaper(font)
    points = anchors()
    failures = []
    for sequence in FIXTURES:
        failures += check_one(r, points, sequence, codes.text(SCRIPT, sequence))
    print(f"{font}: {len(FIXTURES)} fixtures, {len(failures)} failures")
    return failures


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--font", default=str(ROOT / "fonts" / "Veldikko-Regular.ttf"))
    args = ap.parse_args()
    failures = run(Path(args.font))
    for f in failures[:40]:
        print(f"{args.font}: error: {f}")
    if len(failures) > 40:
        print(f"{args.font}: error: ... and {len(failures) - 40} more")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
