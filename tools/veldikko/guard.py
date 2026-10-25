# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Convert every Sinale lexicon form to the Veldikko and assert the font sets it rightly.

    .venv/bin/python tools/veldikko/guard.py [--font fonts/Veldikko-Regular.ttf]
                                       [--thalorna ~/dev/HeroicLands/thalorna | --note FILE | --fixtures-only]

The forms are the ``words`` forms and every name of the frontmatter of
``assets/content/Skills/Languages/Sinale.md`` on the thalorna repository's
``origin/main``, and the fixtures in ``fixtures.json``. The converter from
romanized Sinale to the Veldikko's code points is ``convert.mjs`` beside it,
called through ``node`` in one batch, and the converter's rules live there alone.

Each converted form is shaped right to left, and the guard asserts what the font
must do with it:

- **the glyphs.** The run is the converted text in visual order, a word's last
  letter first, with neither ``.notdef`` nor the box. Each letter is in the form
  its place gives it: isolated alone, initial first, final last, medial between,
  the initial and medial stretched (``.wide``) when the letter carries a long or
  pitched vowel or a diphthong. Each vowel is one mark with its length, pitch and
  emphasis signs folded in;
- **the marks.** A lone vowel mark stands at the ``mark`` anchor its letter's
  form carries in ``sources/Veldikko.ufo``; the two marks of a diphthong
  stand centred on it, the first said to the right; the length bar stands at the
  ``bar`` anchor. Two units of rounding are allowed.

The converter refuses a character with no sign, and the guard reports the form
with the character.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import ufoLib2
import yaml
from fontTools.pens.boundsPen import BoundsPen

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE.parent))
from render import Renderer  # noqa: E402

NOTE = "assets/content/Skills/Languages/Sinale.md"
ENCODING = HERE / "encoding.json"
FIXTURE_FILE = HERE / "fixtures.json"
CONVERTER = ROOT / "tools" / "convert_batch.mjs"
SOURCE = ROOT / "sources" / "Veldikko.ufo"
FAMILY = "Veldikko"
TOLERANCE = 2
DIPHTHONG_GAP = 15  # the least clear space between the two marks of a diphthong
DIPHTHONG_SLACK = 40  # how far a diphthong's ink may stand off its letter's mark point, for the slant
MODIFIERS = ("long", "rise", "fall", "emph")


class Unmappable(Exception):
    def __init__(self, letter: str):
        super().__init__(letter)
        self.letter = letter


def load_encoding():
    enc = json.loads(ENCODING.read_text(encoding="utf-8"))
    name_of = {chr(int(g["codepoint"][2:], 16)): g for g in enc["glyphs"]}
    return name_of


NAME_OF = load_encoding()
_fixtures = json.loads(FIXTURE_FILE.read_text(encoding="utf-8"))
FIXTURES = [(f["latin"], f["glyphs"]) for f in _fixtures["fixtures"]]
UNMAPPABLE = [(f["latin"], f["letter"]) for f in _fixtures["unmappable"]]


def convert_all(words: list[str]) -> list[str | Unmappable]:
    """The Veldikko code points of each romanized word, or the Unmappable naming its
    character. One ``node`` process converts the whole list."""
    result = subprocess.run(
        ["node", str(CONVERTER), FAMILY], input=json.dumps(words), check=True, capture_output=True, text=True
    )
    return [Unmappable(r["letter"]) if "letter" in r else r["text"] for r in json.loads(result.stdout)]


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


def lexicon(thalorna: Path | None, note: Path | None) -> dict:
    if note:
        text = note.read_text(encoding="utf-8")
    else:
        text = subprocess.run(
            ["git", "-C", str(thalorna), "show", f"origin/main:{NOTE}"], check=True, capture_output=True, text=True
        ).stdout
    return yaml.safe_load(text.split("\n---\n", 1)[0].lstrip("-\n"))["data"]


def _strings(node) -> list[str]:
    if isinstance(node, str):
        return [node]
    if isinstance(node, list):
        return [s for v in node for s in _strings(v)]
    if isinstance(node, dict):
        return [s for v in node.values() for s in _strings(v)]
    return []


def lexicon_forms(thalorna: Path | None, note: Path | None) -> list[str]:
    data = lexicon(thalorna, note)
    forms = [w["form"] for w in data["words"]]
    names = data.get("names", {})
    forms += _strings(names.get("given", {})) + _strings(names.get("lineage", {}))
    if not forms:
        raise SystemExit("the lexicon is empty")
    return forms


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


def run(font: Path, forms: list[str]) -> list[str]:
    r = Shaper(font)
    points = anchors()
    failures, unmappable, converted = [], [], 0
    fixture_words = [latin for latin, _ in FIXTURES]
    refused_words = [latin for latin, _ in UNMAPPABLE]
    results = convert_all(forms + fixture_words + refused_words)
    form_results = results[: len(forms)]
    fixture_results = results[len(forms) : len(forms) + len(fixture_words)]
    refused_results = results[len(forms) + len(fixture_words) :]
    for form, text in zip(forms, form_results):
        if isinstance(text, Unmappable):
            unmappable.append((form, text.letter))
            continue
        converted += 1
        failures += check_one(r, points, form, text)
    for (latin, want), text in zip(FIXTURES, fixture_results):
        if isinstance(text, Unmappable):
            failures.append(f"{latin!r}: refused {text.letter!r}, expected {want}")
            continue
        if glyphs_of(text) != want:
            failures.append(f"{latin!r}: converted to {glyphs_of(text)}, expected {want}")
        failures += check_one(r, points, repr(latin), text)
    for (latin, letter), text in zip(UNMAPPABLE, refused_results):
        if not isinstance(text, Unmappable):
            failures.append(f"{latin!r}: converted, expected no sign for {letter!r}")
        elif text.letter != letter:
            failures.append(f"{latin!r}: refused {text.letter!r}, expected {letter!r}")
    for form, letter in unmappable:
        print(f"{NOTE}: warning: the form {form!r} has the character {letter!r}, which the Veldikko has no sign for")
    print(
        f"{font}: {len(forms)} forms, {converted} converted and shaped, {len(unmappable)} with a character "
        f"the Veldikko has no sign for, {len(FIXTURES)} fixtures, {len(failures)} failures"
    )
    return failures


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--font", default=str(ROOT / "fonts" / "Veldikko-Regular.ttf"))
    ap.add_argument("--thalorna", default=str(Path.home() / "dev/HeroicLands/thalorna"))
    ap.add_argument("--note", help="read the language note from this file instead of git")
    ap.add_argument("--fixtures-only", action="store_true", help="shape the fixtures alone, with no lexicon")
    args = ap.parse_args()
    forms = [] if args.fixtures_only else lexicon_forms(Path(args.thalorna), Path(args.note) if args.note else None)
    failures = run(Path(args.font), forms)
    for f in failures[:40]:
        print(f"{args.font}: error: {f}")
    if len(failures) > 40:
        print(f"{args.font}: error: ... and {len(failures) - 40} more")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
