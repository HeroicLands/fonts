# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Convert every Khelathi lexicon form to Qalezu and assert the font shapes it rightly.

    .venv/bin/python tools/qalezu-hand/guard.py [--font fonts/QalezuHand-Regular.ttf]
                                         [--thalorna ~/dev/HeroicLands/thalorna | --note FILE]

The forms come from the ``words`` forms and the ``names`` of the frontmatter of
``assets/content/Skills/Languages/Khelathi.md`` on the thalorna repository's
``origin/main``. The converter from a Latin Khelathi word to the string of Qalezu
code points is ``convert.mjs`` beside it, called through ``node`` in one
batch, and the rules live there alone:

- a consonant letter is its sign, and ``th``, ``sh``, ``kh``, ``gh`` and ``ch``
  or ``tj`` are one sign each, ``ch`` and ``tj`` the same sign;
- ``'`` is the catch;
- a vowel at the start of a word, or after a space, a hyphen or other mark, is the
  catch, and every other vowel draws nothing;
- a catch whose next sign, with the silent vowels skipped, is a consonant sign or a
  doubled sign is written with that sign as one character, its catch-before form
  (``<sign>.catch``, three reed dabs in a triangle over the sign); any other catch
  (at the end of a word, before a mark, before another catch, or in a word with
  no consonant after it) is the standalone catch;
- a consonant written twice with no vowel between is that sign's doubled form, one
  character, and so is a letter doubled before a digraph that begins with it
  (``tth``);
- a hyphen is a word space: ``Gar-Qethar`` is two words, and a hyphen with nothing after
  it, as in the prefix forms ``Gar-`` and ``Lut-``, writes nothing;
- digits, ``.`` and ``,`` are their own signs, and case is ignored.

A letter with no sign (``c`` outside ``ch``, ``j``, ``v``, ``x``, or any other
character) is never invented a mapping: the converter refuses it, and the guard
lists the form with the letter. Every other form is shaped right to left, and
the glyphs must be the signs the converter wrote, in reverse order for the
visual run, with none ``.notdef`` or box. Targets come from ``encoding.json``.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from render import Renderer  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent
NOTE = "assets/content/Skills/Languages/Khelathi.md"
ENCODING = Path(__file__).resolve().parent / "encoding.json"
FIXTURE_FILE = Path(__file__).resolve().parent / "fixtures.json"
CONVERTER = ROOT / "tools" / "convert_batch.mjs"


class Unmappable(Exception):
    def __init__(self, letter: str):
        super().__init__(letter)
        self.letter = letter


def load_encoding():
    enc = json.loads(ENCODING.read_text(encoding="utf-8"))
    point, name_of = {}, {}
    for g in enc["glyphs"]:
        cp = int(g["codepoint"][2:], 16)
        point[g["glyph"]] = chr(cp)
        name_of[chr(cp)] = g["glyph"]
    return point, name_of


POINT, NAME_OF = load_encoding()
SPACE = " "


def convert_all(words: list[str]) -> list[str | Unmappable]:
    """The Qalezu code points of each Latin word, or the Unmappable naming its letter.

    One ``node`` process converts the whole list through ``convert.mjs``.
    """
    result = subprocess.run(
        ["node", str(CONVERTER), "Qalezu Hand"],
        input=json.dumps(words),
        check=True,
        capture_output=True,
        text=True,
    )
    return [Unmappable(r["letter"]) if "letter" in r else r["text"] for r in json.loads(result.stdout)]


def glyphs_of(text: str) -> list[str]:
    return ["space" if c == SPACE else NAME_OF[c] for c in text]


# Each fixture: the Latin and the signs it writes, in reading order. The fixtures and the
# characters the alphabet has no sign for are data, shared with the converter's own tests.
_fixtures = json.loads(FIXTURE_FILE.read_text(encoding="utf-8"))
FIXTURES = [(f["latin"], f["signs"]) for f in _fixtures["fixtures"]]
UNMAPPABLE = [(f["latin"], f["letter"]) for f in _fixtures["unmappable"]]


def lexicon(thalorna: Path | None, note: Path | None) -> dict:
    """The ``data`` of the Khelathi note's frontmatter."""
    if note:
        text = note.read_text(encoding="utf-8")
    else:
        text = subprocess.run(
            ["git", "-C", str(thalorna), "show", f"origin/main:{NOTE}"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout
    return yaml.safe_load(text.split("\n---\n", 1)[0].lstrip("-\n"))["data"]


def lexicon_forms(thalorna: Path | None, note: Path | None) -> list[str]:
    data = lexicon(thalorna, note)
    forms = [w["form"] for w in data["words"]]
    names = data["names"]
    for group in names["given"].values():
        forms += group
    forms += names["house"] + names["place"]
    if not forms:
        raise SystemExit("the lexicon is empty")
    return forms


def run(font: Path, forms: list[str]) -> list[str]:
    r = Renderer(font)
    failures = []
    converted, signs, unmappable = 0, 0, []
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
        want = glyphs_of(text)
        got = r.glyph_names(text, direction="rtl")
        converted += 1
        signs += len(text)
        if ".notdef" in got or "notdef.box" in got:
            failures.append(f"{form}: .notdef or the box in {got}")
        elif len(got) != len(text):
            failures.append(f"{form}: {len(got)} glyphs for {len(text)} signs")
        elif got != want[::-1]:
            failures.append(f"{form}: shaped {got}, expected {want[::-1]}")
    for (latin, want), text in zip(FIXTURES, fixture_results):
        if isinstance(text, Unmappable):
            failures.append(f"{latin!r}: refused {text.letter!r}, expected {want}")
            continue
        if glyphs_of(text) != want:
            failures.append(f"{latin!r}: converted to {glyphs_of(text)}, expected {want}")
        got = r.glyph_names(text, direction="rtl")
        if got != want[::-1]:
            failures.append(f"{latin!r}: shaped {got}, expected {want[::-1]}")
    for (latin, letter), text in zip(UNMAPPABLE, refused_results):
        if not isinstance(text, Unmappable):
            failures.append(f"{latin!r}: converted, expected no sign for {letter!r}")
        elif text.letter != letter:
            failures.append(f"{latin!r}: refused {text.letter!r}, expected {letter!r}")
    for form, letter in unmappable:
        print(f"{NOTE}: warning: the form {form!r} has the letter {letter!r}, which Qalezu has no sign for")
    print(
        f"{font}: {len(forms)} forms, {converted} converted and shaped with {signs} signs, "
        f"{len(unmappable)} with a letter Qalezu has no sign for, {len(FIXTURES)} fixtures, "
        f"{len(failures)} failures"
    )
    return failures


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--font", default=str(ROOT / "fonts" / "QalezuHand-Regular.ttf"))
    ap.add_argument("--thalorna", default=str(Path.home() / "dev/HeroicLands/thalorna"))
    ap.add_argument("--note", help="read the language note from this file instead of git")
    args = ap.parse_args()
    forms = lexicon_forms(Path(args.thalorna), Path(args.note) if args.note else None)
    failures = run(Path(args.font), forms)
    for f in failures[:40]:
        print(f"{args.font}: error: {f}")
    if len(failures) > 40:
        print(f"{args.font}: error: ... and {len(failures) - 40} more")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
