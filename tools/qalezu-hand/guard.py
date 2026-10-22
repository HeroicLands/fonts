# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Write every Khelathi lexicon form in Qalezu and assert the font shapes it rightly.

    .venv/bin/python tools/qalezu-hand/guard.py [--font fonts/QalezuHand-Regular.ttf]
                                         [--thalorna ~/dev/HeroicLands/thalorna | --note FILE]
                                         [--map-note FILE | --fixtures-only]

The forms come from the ``words`` forms and the ``names`` of the frontmatter of
``assets/content/Skills/Languages/Khelathi.md`` on the thalorna repository's
``origin/main``. Each form is written in Qalezu's code points by thalorna's
``qalezu`` mapping note (``assets/content/Lore/Scripts/Qalezu_Spelling.md`` on
``origin/main``, or the file ``--map-note`` names), as a run marked
``map=qalezu`` is, and the result is shaped right to left.

The font draws each code point as its sign, with one contextual form: a catch
followed by a consonant sign or a doubled sign is drawn as that sign's
catch-before form (``<sign>.catch``, three reed dabs in a triangle over the
sign), which has no code point of its own. Two identical consonant signs stay
two signs; a doubled consonant is its own character, which the mapping writes.
So the glyphs a form must shape to follow from the code points the mapping
wrote, with each catch and the sign after it fused, in reverse order for the
visual run, and none ``.notdef`` or the box.

The fixtures in ``fixtures.json`` give a roman spelling and the signs it is
drawn with, in reading order, and are written through the mapping and shaped
too, so the guard checks the mapping and the face together. A character the
mapping has no row for (``c`` outside ``ch``, ``x``, or a mark the script lacks)
passes through it and prints the box: the guard lists the forms that hold one,
and its ``unmappable`` fixtures assert both. Targets come from ``encoding.json``.
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
NOTE = "assets/content/Skills/Languages/Khelathi.md"
ENCODING = Path(__file__).resolve().parent / "encoding.json"
FIXTURE_FILE = Path(__file__).resolve().parent / "fixtures.json"
FACE = "qalezu-hand"
BOX = "notdef.box"


def load_encoding():
    enc = json.loads(ENCODING.read_text(encoding="utf-8"))
    name_of = {chr(int(g["codepoint"][2:], 16)): g["glyph"] for g in enc["glyphs"]}
    fused = {f["base"]: f["glyph"] for f in enc["forms"]}
    catch = next(g["glyph"] for g in enc["glyphs"] if "'" in g.get("typing", []))
    return name_of, fused, catch


NAME_OF, FUSED, CATCH = load_encoding()
SPACE = " "


def drawn(text: str) -> list[str]:
    """The glyphs, in reading order, that the face draws for a string of code points."""
    names = ["space" if c == SPACE else NAME_OF.get(c, BOX) for c in text]
    out: list[str] = []
    for name in names:
        if out and out[-1] == CATCH and name in FUSED:
            out[-1] = FUSED[name]
        else:
            out.append(name)
    return out


# Each fixture: the roman spelling and the signs it is drawn with, in reading order.
_fixtures = json.loads(FIXTURE_FILE.read_text(encoding="utf-8"))
FIXTURES = [(f["latin"], f["signs"]) for f in _fixtures["fixtures"]]
UNMAPPABLE = [(f["latin"], f["letter"]) for f in _fixtures["unmappable"]]


def fixture_texts() -> list[str]:
    """Every roman text the fixtures write through the mapping."""
    return [t for t, _ in FIXTURES] + [t for t, _ in UNMAPPABLE]


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
    shaped, signs, unmapped = 0, 0, []
    for form in forms:
        rec = written[form]
        if rec.get("unmapped"):
            unmapped.append((form, rec["unmapped"]))
            continue
        want = drawn(rec["text"])
        got = r.glyph_names(rec["text"], direction="rtl")
        shaped += 1
        signs += len(want)
        if ".notdef" in got or BOX in got:
            failures.append(f"{form}: .notdef or the box in {got}")
        elif got != want[::-1]:
            failures.append(f"{form}: shaped {got}, expected {want[::-1]}")
    for latin, want in FIXTURES:
        rec = written[latin]
        if rec.get("unmapped"):
            failures.append(f"{latin!r}: the mapping has no row for {rec['unmapped']}, expected {want}")
            continue
        if drawn(rec["text"]) != want:
            failures.append(f"{latin!r}: written as {drawn(rec['text'])}, expected {want}")
        got = r.glyph_names(rec["text"], direction="rtl")
        if got != want[::-1]:
            failures.append(f"{latin!r}: shaped {got}, expected {want[::-1]}")
    for latin, letter in UNMAPPABLE:
        rec = written[latin]
        if letter not in rec.get("unmapped", []):
            failures.append(f"{latin!r}: written as {drawn(rec['text'])}, expected no row for {letter!r}")
        elif BOX not in r.glyph_names(rec["text"], direction="rtl"):
            failures.append(f"{latin!r}: {letter!r} does not print the box")
    for form, letters in unmapped:
        print(f"{NOTE}: warning: the form {form!r} has {', '.join(map(repr, letters))}, which the qalezu mapping does not write")
    print(
        f"{font}: {len(forms)} forms, {shaped} written and shaped with {signs} signs, "
        f"{len(unmapped)} with a character the mapping does not write, {len(FIXTURES) + len(UNMAPPABLE)} fixtures, "
        f"{len(failures)} failures"
    )
    return failures


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--font", default=str(ROOT / "fonts" / "QalezuHand-Regular.ttf"))
    ap.add_argument("--thalorna", default=str(Path.home() / "dev/HeroicLands/thalorna"))
    ap.add_argument("--note", help="read the language note from this file instead of git")
    ap.add_argument("--map-note", help="read the qalezu mapping note from this file instead of git")
    ap.add_argument("--fixtures-only", action="store_true",
                    help="shape the fixtures alone, written as tools/mapped.json records them")
    args = ap.parse_args()
    if args.fixtures_only:
        forms, mapping = [], Mapping.offline(FACE)
    else:
        forms = lexicon_forms(Path(args.thalorna), Path(args.note) if args.note else None)
        mapping = Mapping("qalezu", thalorna=Path(args.thalorna), note=args.map_note, face=FACE)
    failures = run(Path(args.font), forms, mapping)
    for f in failures[:40]:
        print(f"{args.font}: error: {f}")
    if len(failures) > 40:
        print(f"{args.font}: error: ... and {len(failures) - 40} more")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
