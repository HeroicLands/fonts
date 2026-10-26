# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Write every Vedyari lexicon form in the Vedyakshara and assert the font shapes it rightly.

    .venv/bin/python tools/vedyakshara/guard.py [--font fonts/VedyaksharaClassical-Regular.ttf]
                                         [--thalorna ~/dev/HeroicLands/thalorna | --note FILE]
                                         [--encoding FILE | --fixtures-only]

The forms are the ``words``, ``affixes``, ``names`` and ``elements`` of the
frontmatter of ``assets/content/Skills/Languages/Vedyari.md``, and its
``register`` entries in Vedyari, on the thalorna repository's ``origin/main``, or
in the file ``--note`` names. Roman is lowercase, so each form is lowercased, then
written in the Vedyakshara's code points by the ``vedyakshara`` encoding
(``encodings/vedyakshara.json``, or the file ``--encoding`` names), and shaped left
to right.

What a form must shape to follows from the code points the encoding wrote, by the
face's rules taken in order (``drawn``): _pa_ and the soft dot are _fa_; a fused
pair with the cut between is its fused sign, the leftmost first; _ra_ with the cut
is its half form before a consonant and its final form otherwise; a sign, the cut
and _ra_ are the sign's r-foot form; a sign with the cut is its half form before a
consonant and its final form otherwise; after a sign, _ai_ is the _e_ and _i_
flags and _au_ the _o_ and _u_ hooks; and a vowel sign, the cut or the soft dot
after anything that cannot carry it is the box. A hook is compared by its kind,
since the neck it takes is the sign's (``check_font.py`` checks the necks).

The fixtures in ``fixtures.json`` give a roman spelling and the glyphs it is drawn
with, and are written through the encoding and shaped too, so the guard checks the
encoding and the face together. A character the encoding has no row for passes
through it and prints the box: the guard lists the forms that hold one, and its
``unencodable`` fixtures assert both.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from encoded import Encoded, drawn_names, visible  # noqa: E402
from render import Renderer  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent
NOTE = "assets/content/Skills/Languages/Vedyari.md"
HERE = Path(__file__).resolve().parent
FACE = "vedyakshara-classical"
BOX = "notdef.box"
SPACE = " "

ENC = json.loads((HERE / "encoding.json").read_text(encoding="utf-8"))
NAME_OF = {chr(int(g["codepoint"][2:], 16)): g["glyph"] for g in ENC["glyphs"]}
CONSONANTS = [g["glyph"] for g in ENC["glyphs"] if g["kind"] == "consonant"]
SIGNS = {g["glyph"] for g in ENC["glyphs"] if g["kind"] == "vowel sign"}
FUSED = {tuple(f["parts"]): f["glyph"] for f in ENC["fused"]}
C_R = {g for (a, b), g in FUSED.items() if b == "ra"}
BASES = set(CONSONANTS) | {"fa"} | set(FUSED.values())
RFOOT = {b for b in BASES if b != "ra" and b not in C_R and f"{b[:-1]}ra" not in C_R}
STARTS = BASES | {f"{b}.rfoot" for b in RFOOT} | {"ra.half", "ra.final"}  # what a half form stands before
CARRIERS = BASES | {f"{b}.rfoot" for b in RFOOT}  # what carries a vowel sign
SPLIT = {"vs.ai": ["flag.e", "flag.i"], "vs.au": ["hook.o", "hook.u"], "vs.u": ["hook.u"], "vs.o": ["hook.o"]}


def drawn(text: str) -> list[str]:
    """The glyphs, in reading order, that the face draws for a string of code points."""
    g = ["space" if c == SPACE else NAME_OF.get(c, BOX) for c in visible(text)]

    def pairs(rule):
        out, i = [], 0
        while i < len(g):
            got = rule(i)
            if got:
                n, new = got
                out.append(new)
                i += n
            else:
                out.append(g[i])
                i += 1
        return out

    g = pairs(lambda i: (2, "fa") if g[i:i + 2] == ["pa", "dot"] else None)
    g = pairs(lambda i: (3, FUSED[(g[i], g[i + 2])]) if i + 2 < len(g) and g[i + 1] == "cut" and (g[i], g[i + 2]) in FUSED else None)
    g = pairs(lambda i: (2, "ra.half" if i + 2 < len(g) and g[i + 2] in STARTS else "ra.final")
              if g[i:i + 2] == ["ra", "cut"] else None)
    g = pairs(lambda i: (3, f"{g[i]}.rfoot") if g[i] in RFOOT and g[i + 1:i + 3] == ["cut", "ra"] else None)
    g = pairs(lambda i: (2, f"{g[i]}.half") if g[i] in BASES and i + 2 < len(g) and g[i + 1] == "cut" and g[i + 2] in STARTS else None)
    g = pairs(lambda i: (2, f"{g[i]}.final") if g[i] in BASES and g[i + 1:i + 2] == ["cut"] else None)
    out = []
    for i, name in enumerate(g):
        if name in SIGNS and i and g[i - 1] in CARRIERS:
            out += SPLIT.get(name, [name])
        elif name in SIGNS | {"cut", "dot"} and i:
            out.append(BOX)
        else:
            out.append(name)
    return out


def plain(names: list[str]) -> list[str]:
    """A hook named by its kind alone: ``hook.u.230`` is ``hook.u``."""
    return [".".join(n.split(".")[:2]) if n.startswith("hook.") else n for n in names]


_fixtures = json.loads((HERE / "fixtures.json").read_text(encoding="utf-8"))
FIXTURES = [(f["latin"], f["glyphs"]) for f in _fixtures["fixtures"]]
UNENCODABLE = [(f["latin"], f["letter"]) for f in _fixtures["unencodable"]]


def fixture_texts() -> list[str]:
    """Every roman text the fixtures write through the encoding."""
    return [t for t, _ in FIXTURES] + [t for t, _ in UNENCODABLE]


def lexicon(thalorna: Path | None, note: Path | None) -> dict:
    """The ``data`` of the Vedyari note's frontmatter."""
    if note:
        text = note.read_text(encoding="utf-8")
    else:
        text = subprocess.run(["git", "-C", str(thalorna), "show", f"origin/main:{NOTE}"],
                              check=True, capture_output=True, text=True).stdout
    return yaml.safe_load(text.split("\n---\n", 1)[0].lstrip("-\n"))["data"]


def lexicon_forms(thalorna: Path | None, note: Path | None) -> list[str]:
    data = lexicon(thalorna, note)
    forms = [w["form"] for w in data["words"]] + [a["form"] for a in data["affixes"]]
    forms += [e["form"] for e in data["elements"]]
    forms += [r["name"] for r in data["register"] if r.get("tongue") == "vedyari"]

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
    forms = list(dict.fromkeys(str(f).lower() for f in forms))
    if not forms:
        raise SystemExit("the lexicon is empty")
    return forms


def run(font: Path, forms: list[str], encoded: Encoded | None = None) -> list[str]:
    r = Renderer(font)
    m = encoded or Encoded(FACE)
    records = m.records(forms + fixture_texts())
    # The space has no row: it passes through, and the face draws it.
    for rec in records:
        if rec.get("unencoded"):
            rec["unencoded"] = [c for c in rec["unencoded"] if c != SPACE]
    written = dict(zip(forms + fixture_texts(), records))
    failures = []
    shaped, glyphs, unencoded = 0, 0, []
    for form in forms:
        rec = written[form]
        if rec.get("unencoded"):
            unencoded.append((form, rec["unencoded"]))
            continue
        want = drawn(rec["text"])
        got = plain(drawn_names(r, rec["text"], direction="ltr"))
        shaped += 1
        glyphs += len(want)
        if ".notdef" in got or BOX in got:
            failures.append(f"{form}: .notdef or the box in {got}")
        elif got != want:
            failures.append(f"{form}: shaped {got}, expected {want}")
    for latin, want in FIXTURES:
        rec = written[latin]
        if rec.get("unencoded"):
            failures.append(f"{latin!r}: the encoding has no row for {rec['unencoded']}, expected {want}")
            continue
        if drawn(rec["text"]) != want:
            failures.append(f"{latin!r}: written as {drawn(rec['text'])}, expected {want}")
        got = plain(drawn_names(r, rec["text"], direction="ltr"))
        if got != want:
            failures.append(f"{latin!r}: shaped {got}, expected {want}")
    for latin, letter in UNENCODABLE:
        rec = written[latin]
        if letter not in rec.get("unencoded", []):
            failures.append(f"{latin!r}: written as {drawn(rec['text'])}, expected no row for {letter!r}")
        elif BOX not in drawn_names(r, rec["text"], direction="ltr"):
            failures.append(f"{latin!r}: {letter!r} does not print the box")
    for form, letters in unencoded:
        print(f"{NOTE}: warning: the form {form!r} has {', '.join(map(repr, letters))}, "
              "which the vedyakshara encoding does not write")
    print(
        f"{font}: {len(forms)} forms, {shaped} written and shaped with {glyphs} glyphs, "
        f"{len(unencoded)} with a character the encoding does not write, {len(FIXTURES) + len(UNENCODABLE)} fixtures, "
        f"{len(failures)} failures"
    )
    return failures


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--font", default=str(ROOT / "fonts" / "VedyaksharaClassical-Regular.ttf"))
    ap.add_argument("--thalorna", default=str(Path.home() / "dev/HeroicLands/thalorna"))
    ap.add_argument("--note", help="read the language note from this file instead of git")
    ap.add_argument("--encoding", help="apply this encoding file instead of encodings/vedyakshara.json")
    ap.add_argument("--fixtures-only", action="store_true",
                    help="shape the fixtures alone and read no lexicon")
    args = ap.parse_args()
    forms = [] if args.fixtures_only else lexicon_forms(Path(args.thalorna), Path(args.note) if args.note else None)
    encoded = Encoded(FACE, args.encoding)
    failures = run(Path(args.font), forms, encoded)
    for f in failures[:40]:
        print(f"{args.font}: error: {f}")
    if len(failures) > 40:
        print(f"{args.font}: error: ... and {len(failures) - 40} more")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
