# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Write every Helonic and Valtari lexicon form in the Helónika and assert the font shapes it rightly.

    .venv/bin/python tools/helonika/guard.py [--font fonts/HelonikaBook-Regular.ttf]
                                       [--thalorna ~/dev/HeroicLands/thalorna]
                                       [--map-note FILE | --fixtures-only]

The forms are the ``words``, ``affixes`` and ``names`` of the frontmatter of
``assets/content/Skills/Languages/Helonic.md`` and ``Valtari.md``, and each note's
``register`` entries in its own tongue, on the thalorna repository's
``origin/main``. Each form is written in the Helónika's code points by thalorna's
``helonika`` mapping note (``assets/content/Lore/Scripts/Helonika_Spelling.md`` on
``origin/main``, or the file ``--map-note`` names), as a run marked
``map=helonika`` is, and shaped left to right.

What a form must shape to follows from the code points the mapping wrote: each is
its own glyph, the space is the space, and the accent after anything but a vowel is
the box. No form may shape to the notdef or the box.

The fixtures in ``fixtures.json`` give a roman spelling and the glyphs it is drawn
with, and are written through the mapping and shaped too, so the guard checks the
mapping and the face together. A character the mapping has no row for passes
through it and prints the box: the guard lists the forms that hold one, and its
``unmappable`` fixtures assert both.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from mapped import Mapping  # noqa: E402
from render import Renderer  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent
NOTES = {"helonic": "assets/content/Skills/Languages/Helonic.md", "valtari": "assets/content/Skills/Languages/Valtari.md"}
HERE = Path(__file__).resolve().parent
FACE = "helonika-book"
BOX = "notdef.box"
SPACE = " "

ENC = json.loads((HERE / "encoding.json").read_text(encoding="utf-8"))
NAME_OF = {chr(int(g["codepoint"][2:], 16)): g["glyph"] for g in ENC["glyphs"]}
VOWELS = {v for v in "A E E.long I O O.long U A.macron I.macron U.macron".split()}
VOWELS |= {v.lower() for v in VOWELS}


def drawn(text: str) -> list[str]:
    """The glyphs, in reading order, that the face draws for a string of code points."""
    g = ["space" if c == SPACE else NAME_OF.get(c, BOX) for c in text]
    return [BOX if n == "accent" and i and g[i - 1] not in VOWELS else n for i, n in enumerate(g)]


_fixtures = json.loads((HERE / "fixtures.json").read_text(encoding="utf-8"))
FIXTURES = [(f["latin"], f["glyphs"]) for f in _fixtures["fixtures"]]
UNMAPPABLE = [(f["latin"], f["letter"]) for f in _fixtures["unmappable"]]


def fixture_texts() -> list[str]:
    """Every roman text the fixtures write through the mapping."""
    return [t for t, _ in FIXTURES] + [t for t, _ in UNMAPPABLE]


def lexicon(thalorna: Path, note: str) -> dict:
    """The ``data`` of a language note's frontmatter."""
    text = subprocess.run(["git", "-C", str(thalorna), "show", f"origin/main:{note}"],
                          check=True, capture_output=True, text=True).stdout
    return yaml.safe_load(text.split("\n---\n", 1)[0].lstrip("-\n"))["data"]


def lexicon_forms(thalorna: Path) -> list[str]:
    forms = []
    for tongue, note in NOTES.items():
        data = lexicon(thalorna, note)
        forms += [w["form"] for w in data["words"]] + [a["form"] for a in data["affixes"]]
        forms += [r["name"] for r in data.get("register", []) if r.get("tongue") == tongue]

        def walk(x):
            if isinstance(x, str):
                forms.append(x)
            elif isinstance(x, list):
                for i in x:
                    walk(i)
            elif isinstance(x, dict):
                for v in x.values():
                    walk(v)

        walk({k: v for k, v in data["names"].items() if k != "pattern"})
    forms = list(dict.fromkeys(str(f) for f in forms))
    if not forms:
        raise SystemExit("the lexicon is empty")
    return forms


def run(font: Path, forms: list[str], mapping: Mapping | None = None) -> list[str]:
    r = Renderer(font)
    m = mapping or Mapping.offline(FACE)
    records = m.records(forms + fixture_texts())
    # The space has no row: it passes through, and the face draws it.
    for rec in records:
        if rec.get("unmapped"):
            rec["unmapped"] = [c for c in rec["unmapped"] if c != SPACE]
    written = dict(zip(forms + fixture_texts(), records))
    failures = []
    shaped, glyphs, unmapped = 0, 0, []
    for form in forms:
        rec = written[form]
        if rec.get("unmapped"):
            unmapped.append((form, rec["unmapped"]))
            continue
        want = drawn(rec["text"])
        got = r.glyph_names(rec["text"], direction="ltr")
        shaped += 1
        glyphs += len(want)
        if ".notdef" in got or BOX in got:
            failures.append(f"{form}: .notdef or the box in {got}")
        elif got != want:
            failures.append(f"{form}: shaped {got}, expected {want}")
    for latin, want in FIXTURES:
        rec = written[latin]
        if rec.get("unmapped"):
            failures.append(f"{latin!r}: the mapping has no row for {rec['unmapped']}, expected {want}")
            continue
        if drawn(rec["text"]) != want:
            failures.append(f"{latin!r}: written as {drawn(rec['text'])}, expected {want}")
        got = r.glyph_names(rec["text"], direction="ltr")
        if got != want:
            failures.append(f"{latin!r}: shaped {got}, expected {want}")
    for latin, letter in UNMAPPABLE:
        rec = written[latin]
        if letter not in rec.get("unmapped", []):
            failures.append(f"{latin!r}: written as {drawn(rec['text'])}, expected no row for {letter!r}")
        elif BOX not in r.glyph_names(rec["text"], direction="ltr"):
            failures.append(f"{latin!r}: {letter!r} does not print the box")
    for form, letters in unmapped:
        print(f"{NOTES['helonic']}: warning: the form {form!r} has {', '.join(map(repr, letters))}, "
              "which the helonika mapping does not write")
    print(
        f"{font}: {len(forms)} forms, {shaped} written and shaped with {glyphs} glyphs, "
        f"{len(unmapped)} with a character the mapping does not write, {len(FIXTURES) + len(UNMAPPABLE)} fixtures, "
        f"{len(failures)} failures"
    )
    return failures


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--font", default=str(ROOT / "fonts" / "HelonikaBook-Regular.ttf"))
    ap.add_argument("--thalorna", default=str(Path.home() / "dev/HeroicLands/thalorna"))
    ap.add_argument("--map-note", help="read the helonika mapping note from this file instead of git")
    ap.add_argument("--fixtures-only", action="store_true",
                    help="shape the fixtures alone, written as tools/mapped.json records them")
    args = ap.parse_args()
    if args.fixtures_only:
        forms, mapping = [], Mapping.offline(FACE)
    else:
        forms = lexicon_forms(Path(args.thalorna))
        mapping = Mapping("helonika", thalorna=Path(args.thalorna), note=args.map_note, face=FACE)
    failures = run(Path(args.font), forms, mapping)
    for f in failures[:40]:
        print(f"{args.font}: error: {f}")
    if len(failures) > 40:
        print(f"{args.font}: error: ... and {len(failures) - 40} more")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
