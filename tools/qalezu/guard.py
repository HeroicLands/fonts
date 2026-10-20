# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Convert every Khelathi lexicon form to Qalezu and assert the font shapes it rightly.

    .venv/bin/python tools/qalezu/guard.py [--font fonts/Qalezu-Regular.ttf]
                                         [--thalorna ~/dev/HeroicLands/thalorna | --note FILE]

The forms come from the ``words`` forms and the ``names`` of the frontmatter of
``assets/content/Skills/Languages/Khelathi.md`` on the thalorna repository's
``origin/main``. ``convert`` is the reference converter from a Latin Khelathi
word to the string of Qalezu code points, and the rules live here alone:

- a consonant letter is its sign, and ``th``, ``sh``, ``kh``, ``gh`` and ``ch``
  or ``tj`` are one sign each, ``ch`` and ``tj`` the same sign;
- ``'`` is the catch;
- a vowel at the start of a word, or after a space, hyphen or other mark, is the
  catch, and every other vowel draws nothing;
- a consonant written twice with no vowel between is that sign's doubled form, one
  character, and so is a letter doubled before a digraph that begins with it
  (``tth``);
- digits, ``.``, ``,`` and ``-`` are their own signs, and case is ignored.

A letter with no sign (``c`` outside ``ch``, ``j``, ``v``, ``x``, or any other
character) is never invented a mapping: ``convert`` refuses it, and the guard
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

VOWELS = set("aeiou")


class Unmappable(Exception):
    def __init__(self, letter: str):
        super().__init__(letter)
        self.letter = letter


def load_encoding():
    enc = json.loads(ENCODING.read_text(encoding="utf-8"))
    typing, point, name_of, double = {}, {}, {}, {}
    for g in enc["glyphs"]:
        if g["kind"] == "doubled":
            double[g["base"]] = g["glyph"]
        cp = int(g["codepoint"][2:], 16)
        point[g["glyph"]] = chr(cp)
        name_of[chr(cp)] = g["glyph"]
        if g["kind"] != "doubled":
            for t in g["typing"]:
                typing[t] = g["glyph"]
    return typing, point, name_of, double


TYPING, POINT, NAME_OF, DOUBLE = load_encoding()
DIGRAPHS = {t for t in TYPING if len(t) == 2 and t.isalpha()}
CATCH = TYPING["'"]
SPACE = " "
# Typed characters that mark a word boundary: the next vowel is word-initial.
BOUNDARY = set(" \t\n -.,") | set("0123456789")


def convert(word: str) -> str:
    """The Qalezu code points a Latin Khelathi word is written with."""
    s = word.lower()
    out: list[str] = []  # glyph names, logical order
    prev = None  # the consonant sign just written with no vowel since, else None
    initial = True  # the next vowel is word-initial
    i = 0
    while i < len(s):
        ch = s[i]
        two = s[i : i + 2]
        if ch in VOWELS:
            if initial:
                out.append(CATCH)
            initial, prev = False, None
            i += 1
        elif ch in ("'", "’"):
            out.append(CATCH)
            initial, prev = False, None
            i += 1
        elif ch in BOUNDARY:
            if ch == SPACE or ch == " ":
                out.append(SPACE)
            else:
                out.append(TYPING[ch])
            initial, prev = True, None
            i += 1
        elif ch.isalpha():
            # A letter doubled before a digraph that begins with it: tth, kkh.
            if len(s) > i + 2 and s[i + 1] == ch and (s[i + 1 : i + 3]) in DIGRAPHS:
                out.append(DOUBLE[TYPING[s[i + 1 : i + 3]]])
                initial, prev = False, None
                i += 3
                continue
            if two in DIGRAPHS:
                sign, step = TYPING[two], 2
            elif ch in TYPING and len(ch) == 1:
                sign, step = TYPING[ch], 1
            else:
                raise Unmappable(ch)
            if prev == sign:
                out[-1] = DOUBLE[sign]
                prev = None
            else:
                out.append(sign)
                prev = sign
            initial = False
            i += step
        else:
            raise Unmappable(ch)
    return "".join(SPACE if g == SPACE else POINT[g] for g in out)


def glyphs_of(text: str) -> list[str]:
    return ["space" if c == SPACE else NAME_OF[c] for c in text]


# Each fixture: the Latin and the signs it writes, in reading order.
FIXTURES = [
    ("Anlagh", ["catch", "n", "l", "gh"]),  # a word-initial vowel draws the catch, others nothing
    ("Qe'aret", ["q", "catch", "r", "t"]),  # a vowel after the apostrophe draws nothing
    ("Au'Khelathu", ["catch", "catch", "kh", "l", "th"]),
    ("Gar-Anlagh", ["g", "r", "hyphen", "catch", "n", "l", "gh"]),  # the dash starts a word
    ("Gith’el", ["g", "th", "catch", "l"]),  # the curly apostrophe is the catch
    ("kala", ["k", "l"]),  # a word-final vowel draws nothing
    ("ku", ["k"]),
    ("thal", ["th", "l"]),
    ("shal", ["sh", "l"]),
    ("khal", ["kh", "l"]),
    ("ghal", ["gh", "l"]),
    ("chal", ["tj", "l"]),
    ("tjal", ["tj", "l"]),  # ch and tj type the same sign
    ("TJAL", ["tj", "l"]),  # case is ignored
    ("lenni", ["l", "n.dbl"]),  # a doubled consonant is the doubled sign
    ("gerra", ["g", "r.dbl"]),
    ("lanal", ["l", "n", "l"]),  # a vowel between two of the same is no doubling
    ("tthal", ["th.dbl", "l"]),  # a doubled digraph
    ("thth", ["th.dbl"]),
    ("sshal", ["sh.dbl", "l"]),
    ("ll", ["l.dbl"]),
    ("kkhal", ["kh.dbl", "l"]),
    ("tjtj", ["tj.dbl"]),
    ("chch", ["tj.dbl"]),
    ("ttj", ["tj.dbl"]),
    ("Linnuseret", ["l", "n.dbl", "s", "r", "t"]),
    ("lll", ["l.dbl", "l"]),
    ("''", ["catch", "catch"]),  # the catch is not doubled
    ("Zel ez Qar", ["z", "l", "space", "catch", "z", "space", "q", "r"]),
    ("1234567890", ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "zero"]),
    ("zeret 305, 14.", ["z", "r", "t", "space", "three", "zero", "five", "comma", "space", "one", "four", "period"]),
]

# Characters the alphabet has no sign for.
UNMAPPABLE = [("c", "c"), ("cal", "c"), ("jal", "j"), ("val", "v"), ("xal", "x"), ("l?", "?"), ("l;", ";")]


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
    for form in forms:
        try:
            text = convert(form)
        except Unmappable as e:
            unmappable.append((form, e.letter))
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
    for latin, want in FIXTURES:
        text = convert(latin)
        if glyphs_of(text) != want:
            failures.append(f"{latin!r}: converted to {glyphs_of(text)}, expected {want}")
        got = r.glyph_names(text, direction="rtl")
        if got != want[::-1]:
            failures.append(f"{latin!r}: shaped {got}, expected {want[::-1]}")
    for latin, letter in UNMAPPABLE:
        try:
            convert(latin)
            failures.append(f"{latin!r}: converted, expected no sign for {letter!r}")
        except Unmappable as e:
            if e.letter != letter:
                failures.append(f"{latin!r}: refused {e.letter!r}, expected {letter!r}")
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
    ap.add_argument("--font", default=str(ROOT / "fonts" / "Qalezu-Regular.ttf"))
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
