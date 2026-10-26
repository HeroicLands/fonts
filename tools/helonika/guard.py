# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Write every Helonic, Valtari, Bizarian and Bethuan lexicon form in the Helónika and assert the font shapes it rightly.

    .venv/bin/python tools/helonika/guard.py [--font fonts/HelonikaBook-Regular.ttf]
                                       [--thalorna ~/dev/HeroicLands/thalorna | --note FILE ...]
                                       [--encoding [NAME=]FILE ... | --fixtures-only]

The forms are the ``words``, ``affixes`` and ``names`` of the frontmatter of
``assets/content/Skills/Languages/Helonic.md``, ``Valtari.md``, ``Byzarian.md`` and
``Bethuan.md``, and each note's ``register`` entries in its own tongue, on the
thalorna repository's ``origin/main``, or in the files ``--note`` names (one flag per
file, each a language note written in the Helónika; only those files are read).
Roman is lowercase, so each form is lowercased, then written in the Helónika's code
points by the encoding the language
note's ``writtenIn.map`` names (package-build's key for it), and shaped left to
right. Helonic and Valtari use ``helonika``, Bizarian ``helonika-bizarian`` and
Bethuan ``helonika-bethuan``. The encodings are ``encodings/helonika.json``,
``encodings/helonika-bizarian.json`` and ``encodings/helonika-bethuan.json``, or the
file ``--encoding NAME=FILE`` names for ``helonika``, ``bizarian`` or ``bethuan``; a
bare ``--encoding FILE`` is ``helonika=FILE``.

What a form must shape to follows from the code points the encoding wrote: each is
its own glyph, the space is the space (given no advance when it follows the raised dot of a sentence end,
as the ``spaces`` fixtures assert), and the accent after anything but a vowel is
the box. No form may shape to the notdef or the box.

The fixtures in ``fixtures.json`` give a roman spelling and the glyphs it is drawn
with, for the Helonic map and, under ``bizarian`` and ``bethuan``, for each of the
others. They are written through their encoding and shaped too, so the guard checks
the encodings and the face together. A character the encoding has no row for passes
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
LANGUAGES = "assets/content/Skills/Languages"
# Each tongue's language note, and the encoding each writes its forms by.
NOTES = {
    "helonic": f"{LANGUAGES}/Helonic.md",
    "valtari": f"{LANGUAGES}/Valtari.md",
    "byzarian": f"{LANGUAGES}/Byzarian.md",
    "bethuan": f"{LANGUAGES}/Bethuan.md",
}
# The encoding a language note's ``writtenIn.map`` (package-build's key) names, as the key the tools use
# for it, and the face key of tools/encoded.py it is written for.
SCRIPT_OF = {"helonika": "helonika", "helonika-bizarian": "bizarian", "helonika-bethuan": "bethuan"}
OFFLINE = {"helonika": "helonika-book", "bizarian": "helonika-bizarian", "bethuan": "helonika-bethuan"}
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
    g = ["space" if c == SPACE else NAME_OF.get(c, BOX) for c in visible(text)]
    return [BOX if n == "accent" and i and g[i - 1] not in VOWELS else n for i, n in enumerate(g)]


_fixtures = json.loads((HERE / "fixtures.json").read_text(encoding="utf-8"))


def fixtures(script: str = "helonika") -> tuple[list, list]:
    """The (latin, glyphs) fixtures and the (latin, letter) unencodable ones written by an encoding."""
    doc = _fixtures if script == "helonika" else _fixtures[script]
    return [(f["latin"], f["glyphs"]) for f in doc["fixtures"]], [(f["latin"], f["letter"]) for f in doc.get("unencodable", [])]


def spaces() -> list[tuple[str, list[int]]]:
    """The (latin, advances) fixtures: the advance of each space glyph a roman text shapes to."""
    return [(f["latin"], f["advances"]) for f in _fixtures.get("spaces", [])]


def fixture_texts(script: str = "helonika") -> list[str]:
    """Every roman text the fixtures of an encoding write through it."""
    good, bad = fixtures(script)
    texts = [t for t, _ in good] + [t for t, _ in bad]
    return texts + [t for t, _ in spaces()] if script == "helonika" else texts


def lexicon(thalorna: Path, note: str, file: Path | None = None) -> tuple[dict, str]:
    """The ``data`` of a language note's frontmatter, and the encoding its ``writtenIn`` names."""
    if file:
        text = file.read_text(encoding="utf-8")
    else:
        text = subprocess.run(["git", "-C", str(thalorna), "show", f"origin/main:{note}"],
                              check=True, capture_output=True, text=True).stdout
    data = yaml.safe_load(text.split("\n---\n", 1)[0].lstrip("-\n"))["data"]
    written = data.get("writtenIn", {})
    if written.get("map") not in SCRIPT_OF or written.get("font") != FACE:
        raise SystemExit(f"{file or note}: error: writtenIn is {written}, not a map of {FACE} that this guard reads: "
                         f"{', '.join(SCRIPT_OF)}")
    return data, SCRIPT_OF[written["map"]]


def note_forms(data: dict, tongue: str) -> list[str]:
    forms = [w["form"] for w in data.get("words", [])] + [a["form"] for a in data.get("affixes", [])]
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

    walk({k: v for k, v in data.get("names", {}).items() if k != "pattern"})
    return [str(f).lower() for f in forms]


def lexicon_forms(thalorna: Path, files: list[Path] = ()) -> dict[str, list[str]]:
    """The forms to shape, by the encoding that writes them: those of the files, or of the
    four language notes on thalorna's ``origin/main``. Each file's tongue is its file name."""
    sources = [(f.stem.lower(), NOTES.get(f.stem.lower(), str(f)), f) for f in files] if files else \
        [(tongue, note, None) for tongue, note in NOTES.items()]
    by_script: dict[str, list[str]] = {}
    for tongue, note, file in sources:
        data, script = lexicon(thalorna, note, file)
        by_script.setdefault(script, []).extend(note_forms(data, tongue))
    by_script = {script: list(dict.fromkeys(forms)) for script, forms in by_script.items()}
    if not any(by_script.values()):
        raise SystemExit("the lexicon is empty")
    return by_script


def run(font: Path, groups: dict[str, list[str]], encodings: dict[str, Encoded] | None = None) -> list[str]:
    """Shape every group's forms, written by its encoding, and every encoding's fixtures.

    ``groups`` is the forms by encoding (``helonika``, ``bizarian`` or ``bethuan``); the fixtures
    of all three encodings are shaped whichever groups are given. An encoding not in ``encodings``
    is the face's own."""
    r = Renderer(font)
    encodings = encodings or {}
    failures = []
    shaped = glyphs = nforms = nunencoded = nfixtures = 0
    for script in OFFLINE:
        m = encodings.get(script) or Encoded(OFFLINE[script])
        forms = groups.get(script, [])
        records = m.records(forms + fixture_texts(script))
        # The space has no row: it passes through, and the face draws it.
        for rec in records:
            if rec.get("unencoded"):
                rec["unencoded"] = [c for c in rec["unencoded"] if c != SPACE]
        written = dict(zip(forms + fixture_texts(script), records))
        nforms += len(forms)
        for form in forms:
            rec = written[form]
            if rec.get("unencoded"):
                nunencoded += 1
                print(f"{NOTES['helonic']}: warning: the form {form!r} has "
                      f"{', '.join(map(repr, rec['unencoded']))}, which the {script} encoding does not write")
                continue
            want = drawn(rec["text"])
            got = drawn_names(r, rec["text"], direction="ltr")
            shaped += 1
            glyphs += len(want)
            if ".notdef" in got or BOX in got:
                failures.append(f"{script}: {form}: .notdef or the box in {got}")
            elif got != want:
                failures.append(f"{script}: {form}: shaped {got}, expected {want}")
        good, bad = fixtures(script)
        nfixtures += len(good) + len(bad)
        for latin, want in good:
            rec = written[latin]
            if rec.get("unencoded"):
                failures.append(f"{script}: {latin!r}: the encoding has no row for {rec['unencoded']}, expected {want}")
                continue
            if drawn(rec["text"]) != want:
                failures.append(f"{script}: {latin!r}: written as {drawn(rec['text'])}, expected {want}")
            got = drawn_names(r, rec["text"], direction="ltr")
            if got != want:
                failures.append(f"{script}: {latin!r}: shaped {got}, expected {want}")
        if script == "helonika":
            nfixtures += len(spaces())
            for latin, want in spaces():
                shaped_text = r.shape(written[latin]["text"], direction="ltr")
                text = written[latin]["text"]
                got = [g[3] for g, c in zip(shaped_text.glyphs, shaped_text.clusters) if text[c] == SPACE]
                if got != want:
                    failures.append(f"{script}: {latin!r}: the spaces advance {got}, expected {want}")
        for latin, letter in bad:
            rec = written[latin]
            if letter not in rec.get("unencoded", []):
                failures.append(f"{script}: {latin!r}: written as {drawn(rec['text'])}, expected no row for {letter!r}")
            elif BOX not in drawn_names(r, rec["text"], direction="ltr"):
                failures.append(f"{script}: {latin!r}: {letter!r} does not print the box")
    print(
        f"{font}: {nforms} forms, {shaped} written and shaped with {glyphs} glyphs, "
        f"{nunencoded} with a character the encoding does not write, {nfixtures} fixtures, "
        f"{len(failures)} failures"
    )
    return failures


def encoding_files(entries: list[str]) -> dict[str, str]:
    """Encoding files by script: ``SCRIPT=FILE`` names the script, and a bare ``FILE`` is the helonika encoding."""
    files = {}
    for entry in entries:
        script, eq, file = entry.partition("=")
        if eq and script in OFFLINE:
            files[script] = file
        else:
            files["helonika"] = entry
    return files


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--font", default=str(ROOT / "fonts" / "HelonikaBook-Regular.ttf"))
    ap.add_argument("--thalorna", default=str(Path.home() / "dev/HeroicLands/thalorna"))
    ap.add_argument("--note", action="append", default=[], metavar="FILE",
                    help="read this language note (Helonic, Valtari, Byzarian or Bethuan) from a file instead of git; "
                         "repeat for several, and only those are read")
    ap.add_argument("--encoding", action="append", default=[], metavar="[SCRIPT=]FILE",
                    help="apply an encoding file instead of encodings/<name>.json: helonika=FILE, bizarian=FILE "
                         "or bethuan=FILE; a bare FILE is helonika=FILE")
    ap.add_argument("--fixtures-only", action="store_true",
                    help="shape the fixtures alone and read no lexicon")
    args = ap.parse_args()
    files = encoding_files(args.encoding)
    groups = {} if args.fixtures_only else lexicon_forms(Path(args.thalorna), [Path(n) for n in args.note])
    encodings = {script: Encoded(OFFLINE[script], files.get(script)) for script in OFFLINE}
    failures = run(Path(args.font), groups, encodings)
    for f in failures[:40]:
        print(f"{args.font}: error: {f}")
    if len(failures) > 40:
        print(f"{args.font}: error: ... and {len(failures) - 40} more")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
