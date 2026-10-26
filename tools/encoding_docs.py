# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Write each encoding page, ``encodings/<name>.md``, from its JSON.

The shared punctuation specification, ``encodings/standard.md``, is authored
separately and is never overwritten by this generator.

    python3 tools/encoding_docs.py            # write the pages
    python3 tools/encoding_docs.py --check    # fail where a page is missing or out of date

A page gives the encoding's introduction (``tools/encoding_docs.json``), the fonts it
serves, how to run it, how its script writes each mark of the standard, its vowels and
conditions in plain words, the table of its own rows, and the guarantee that it
round-trips exactly. The tables come from the encoding file and the standard alone; an
encoding is deterministic and structural, so a page names no setting.

The ``standard.marks`` entry of ``tools/encoding_docs.json`` holds the meaning
of each punctuation row in ``encodings/standard.json``. The authored standard
page also describes its structural controls.

``tools/encoding_docs.json`` holds, for each encoding, a ``title``, an ``intro`` (a list of
paragraphs), an ``example`` roman text, and for an encoding too large to read as one
table, ``"summary": true`` with a ``structure`` (a list of paragraphs) that explains how
its rows are built. A summarised page lists the rows of a single character, a few longer
rows of each length.

It runs under any Python 3.9 or later with the standard library alone. A finding is
``file:line:column: error: message`` and the exit status is 1.
"""

import argparse
import json
import os
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
import encode as E  # noqa: E402

DATA = os.path.join(HERE, "encoding_docs.json")
FONTS = os.path.join(ROOT, "fonts.json")
# How many examples a summarised page shows of each kind.
SAMPLE = 12

WORDS = {
    "before": {"vowel": "before a vowel", "consonant": "before a consonant"},
    "at": {"start": "at the start of a word", "end": "at the end of a word", "line-start": "at the beginning of a line"},
}
DIRECTIONS = {"ltr": "left to right", "rtl": "right to left"}


def code(text):
    """A Markdown code span for ``text``, safe inside a table cell."""
    if text == "":
        return "(nothing)"
    if text == " ":
        return "(space)"
    shown = text.replace("|", "\\|")
    if unicodedata.combining(text[0]):
        shown = "◌" + shown
    longest = run = 0
    for char in shown:
        run = run + 1 if char == "`" else 0
        longest = max(longest, run)
    ticks = "`" * (longest + 1)
    pad = " " if shown.startswith("`") or shown.endswith("`") else ""
    return f"{ticks}{pad}{shown}{pad}{ticks}"


def points(text):
    return " ".join(f"U+{ord(c):04X}" for c in text) if text else "(none)"


def when(row):
    parts = []
    if row.before:
        parts.append(WORDS["before"][row.before])
    if row.at:
        parts.append(WORDS["at"][row.at])
    return ", ".join(parts)


def table(headers, rows):
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    lines += ["| " + " | ".join(cells) + " |" for cells in rows]
    return lines


def row_cells(row, with_when):
    cells = [code(row.source), code(row.target), points(row.target)]
    if with_when:
        cells.append(when(row) or "always")
    return cells


def row_table(rows):
    with_when = any(r.conditioned for r in rows)
    headers = ["Roman", "Character", "Code points"] + (["When"] if with_when else [])
    return table(headers, [row_cells(r, with_when) for r in rows])


def families():
    with open(FONTS, encoding="utf-8") as handle:
        manifest = json.load(handle)
    return {f["class"][3:]: f for f in manifest["families"]}


def paragraph_lines(paragraphs):
    out = []
    for text in paragraphs:
        out += [text, ""]
    return out


def marks_of(standard):
    """The standard's rows, every one a mark: the standard has no row for whitespace."""
    return list(standard.rows)


def separator_section(enc):
    """What the encoding writes for a word separator."""
    lines = [
        "## Whitespace",
        "",
        "In roman, outside `⟦` and `⟧`, any run of spaces, tabs and line breaks is one word separator. "
        "It is not a character of the script, and no row matches it.",
        "",
    ]
    if enc.separator == "":
        lines.append(
            "This script sets its characters beside each other, so its `separator` is empty: a separator "
            "writes nothing. Decoding gives no space, only what the characters read as."
        )
    elif enc.separator == " ":
        lines.append(
            "This script spaces its words, so its `separator` is one space, U+0020: a separator writes "
            "one space, and decoding writes one space."
        )
    else:
        lines.append(
            f"This script spaces its words, so its `separator` is {points(enc.separator)}: a separator "
            "writes it, and decoding writes one space."
        )
    lines += [
        "",
        "The separator is normalized on input, not preserved: `a  b` and `a\\n\\tb` encode as `a b` does, and "
        "decoding writes a single space.",
        "",
    ]
    lines += [
        "With `--verse` or `encode(..., verse=True)`, a line ending writes the shared verse "
        "line control and a blank line writes the stanza control. `--- {.canto}` writes "
        "the canto control. See [standard.md](standard.md) for the structural assignments.",
        "",
    ]
    return lines


def marks_section(enc, standard, meanings):
    """How the encoding writes each mark of the standard."""
    lines = [
        "## Punctuation",
        "",
        "This encoding extends the [standard roman encoding](standard.md), which every "
        "language's roman shares. The table shows how this script writes each standard mark. "
        "A mark the script draws writes its glyph; a mark it does not draw writes the "
        "standard's invisible mark, the same in every encoding, so decoding restores it.",
        "",
    ]
    if enc.round_trip == "canonical":
        lines[2] = ("This encoding inherits punctuation rows from standard.json, with the replacements "
                    "listed below. A replacement may omit a mark; decoding then cannot restore it. "
                    "The shared assignments are defined in [standard.md](standard.md).")
    rows = []
    for mark in marks_of(standard):
        written = E.encode(enc, mark.source)
        drawn = "".join(c for c in written if not E.is_mark(c))
        how = f"drawn, {code(drawn)}" if drawn else "invisible"
        rows.append([code(mark.source), meanings[mark.source], how, points(written)])
    lines += table(["Mark", "Meaning", "Written", "Code points"], rows) + [""]
    lines += separator_section(enc)
    lines += [
        "A character that no row matches is refused: `encode.py` reports it with its line and "
        "column, and writes nothing.",
        "",
    ]
    return lines


def accepted_words(enc):
    """The characters an encoding declares, as the file states them."""
    return ", ".join(code(item) for item in enc.declared)


def accepts_section(enc):
    """The characters the encoding accepts as roman."""
    if not enc.declared:
        return [
            "## Accepted characters", "",
            "This encoding accepts no roman letters, only the standard's marks and whitespace. Anything "
            "else outside `⟦` and `⟧` is refused at its line and column.", "",
        ]
    return [
        "## Accepted characters", "",
        f"This encoding accepts {accepted_words(enc)}, and the standard's marks and whitespace. Any "
        "other character is refused at its line and column.", "",
    ]


def codage_page(enc, entry, fonts):
    lines = [f"# {entry['title']}", ""]
    lines += paragraph_lines(entry["intro"])
    lines += ["## Fonts", ""]
    for slug in enc.fonts:
        family = fonts[slug]
        lines.append(f"- {family['name']} (`{slug}`), written {DIRECTIONS[family['direction']]}.")
    lines.append("")
    lines += [
        "## Using it", "",
        "A codage is a file of kind `codage`: it extends nothing and takes no text of its own. A script "
        "encoding states it with `\"codage\": \"" + enc.name + "\"`, and its codes are written between `⟦` "
        "and `⟧`. Whitespace between codes only separates them, and decoding writes single spaces. Inside "
        "the markers only this codage's codes and notation are allowed, so a standard mark such as `,` is "
        "refused at its position. Outside them a code is ordinary roman. Asking for the codage as a "
        "whole-text encoding is an error that names the script encoding to use.", "",
    ]
    lines += ["## Rows", ""]
    if entry.get("summary"):
        lines += paragraph_lines(entry["structure"])
        singles = [r for r in enc.own if len(r.source) == 1]
        lines += ["### Rows of a single character", ""] + row_table(singles) + [""]
        lines += ["### Longer rows", "", "A few rows of each length show the pattern; every longer row is built in the same way.", ""]
        longer = []
        for size in sorted({len(r.source) for r in enc.own if len(r.source) > 1}):
            longer += [r for r in enc.own if len(r.source) == size][:3]
        lines += row_table(longer) + [""]
    else:
        lines += row_table(enc.own) + [""]
    lines += [f"This page is written from `encodings/{enc.name}.json` by `tools/encoding_docs.py`.", ""]
    return "\n".join(lines)


def page(enc, entry, fonts, standard=None, meanings=None):
    name = enc.name
    summary = bool(entry.get("summary"))
    lines = [f"# {entry['title']}", ""]
    lines += paragraph_lines(entry["intro"])

    lines += ["## Fonts", ""]
    for slug in enc.fonts:
        family = fonts[slug]
        lines.append(f"- {family['name']} (`{slug}`), written {DIRECTIONS[family['direction']]}.")
    lines.append("")

    sample = entry["example"]
    encoded = E.encode(enc, sample)
    decoded = E.decode(enc, encoded)
    lines += [
        "## Running it",
        "",
        "`encode.py` needs only Python 3.9 or later. From a checkout, or from `node_modules/@heroiclands/fonts`:",
        "",
        "```sh",
        f'python3 encode.py --encoding {name} "{sample}"',
        f'python3 encode.py --encoding {name} --decode "{encoded}"',
        "```",
        "",
        f"The first command writes {code(encoded)}, and the second reads it back as {code(decoded)}. "
        "`--codepoints` prints the result as `U+XXXX` values, and the text may come from standard input.",
        "",
    ]
    if enc.faces:
        slugs = ", ".join(f"`{s}`" for s in enc.faces)
        lines += [
            f"`--face SLUG` applies the rows of one face ({slugs}), which are tried before the shared rows.",
            "",
        ]
    lines += [
        "From Python:",
        "",
        "```python",
        "import encode",
        "",
        f'text = encode.encode("{name}", "{sample}")',
        f'roman = encode.decode("{name}", text)',
        "```",
        "",
    ]

    if standard is not None:
        lines += accepts_section(enc)
        lines += marks_section(enc, standard, meanings)

    if standard is not None:
        if enc.codage is None:
            lines += ["## Literal spans", "",
                      "`⟦` and `⟧` enclose character names, as the [standard](standard.md) describes: "
                      "`⟦LATIN_SMALL_LETTER_A_WITH_ACUTE⟧` writes `á`. Whitespace between names only "
                      "separates them.", ""]
        else:
            lines += ["## Literal spans", "",
                      f"`⟦` and `⟧` enclose codes of the [{enc.codage.name} codage]({enc.codage.name}.md), "
                      "which encodes and decodes the span, as the [standard](standard.md) describes. "
                      "Only the codage's codes and its notation are allowed inside, no standard mark, "
                      "and whitespace between codes only separates them. A code outside the markers is "
                      "ordinary roman.", ""]

    conditions = {(r.before, r.at) for r in enc.rows if r.conditioned}
    if enc.vowels or conditions:
        lines += ["## Vowels and conditions", ""]
        if enc.vowels:
            lines += [f"The vowels are {code(''.join(sorted(enc.vowels)))}.", ""]
        used = sorted({r.before for r in enc.rows if r.before} | {r.at for r in enc.rows if r.at})
        meanings = {
            "vowel": "A row marked _before a vowel_ applies when the next character is a vowel.",
            "consonant": "A row marked _before a consonant_ applies when the next character is a letter that is not a vowel.",
            "start": "A row marked _at the start of a word_ applies at the first character of the text or after whitespace, punctuation or a symbol.",
            "end": "A row marked _at the end of a word_ applies at the last character of the text or before whitespace, punctuation or a symbol.",
            "line-start": "A row marked _at the beginning of a line_ applies before any other text on that line; preceding indentation carets are allowed.",
        }
        for key in ("vowel", "consonant", "start", "end"):
            if key in used:
                lines += [meanings[key], ""]
        if used:
            lines += [
                "Where several rows begin with the same roman, the longest wins, and among rows of one length a row whose "
                "condition holds comes before a row with none. A row whose condition fails is skipped.",
                "",
            ]

    lines += ["## Rows", ""]
    if summary:
        lines += paragraph_lines(entry["structure"])
        singles = [r for r in enc.own if len(r.source) == 1]
        lines += ["### Rows of a single character", ""] + row_table(singles) + [""]
        lines += ["### Longer rows", ""]
        lines += [
            "A few rows of each length show the pattern; every longer row is built in the same way.",
            "",
        ]
        longer = []
        for size in sorted({len(r.source) for r in enc.own if len(r.source) > 1}):
            longer += [r for r in enc.own if len(r.source) == size][:3]
        lines += row_table(longer) + [""]
    else:
        if enc.own:
            lines += ["The rows are in the order the file states them. A row here for a standard mark replaces "
                      "the standard's row for it."]
            lines += [""] + row_table(enc.own) + [""]
        else:
            lines += ["The encoding states no rows of its own: the standard's rows are the whole encoding.", ""]
    for slug, face in enc.faces.items():
        lines += [f"### Rows of `{slug}`", "", "These rows apply only to text set in this face, and are tried first.", ""]
        lines += row_table(face.rows) + [""]

    round_trip = (
        "This encoding decodes to a conventional Roman spelling. Omitted punctuation is not restored, "
        "and rows that write the word separator decode as a space. It does not preserve the exact "
        "source spelling or promise an exact code-point round trip. The Code points column shows "
        "every character each row writes."
        if enc.round_trip == "canonical" else
        "Every encoding round-trips exactly: decoding the code points that encoding wrote gives back the roman "
        "text, and encoding that gives the same code points. The Code points column shows every character a row "
        "writes, including any that is invisible."
    )
    lines += [
        "## Round trip",
        "",
        round_trip,
        "",
    ]

    lines += [f"This page is written from `encodings/{name}.json` by `tools/encoding_docs.py`.", ""]
    return "\n".join(lines)



def pages():
    with open(DATA, encoding="utf-8") as handle:
        data = json.load(handle)
    fonts = families()
    standard = E.load_base(os.path.join(E.ENCODINGS, f"{E.STANDARD}.json"))
    entry = data.get(E.STANDARD)
    if entry is None:
        raise SystemExit(f"{os.path.relpath(DATA)}: error: `{E.STANDARD}` has no entry")
    meanings = entry.get("marks", {})
    stated = [r.source for r in marks_of(standard)]
    missing = [m for m in stated if m not in meanings]
    extra = [m for m in meanings if m not in stated]
    if missing or extra:
        raise SystemExit(
            f"{os.path.relpath(DATA)}: error: `{E.STANDARD}.marks` gives the meaning of every mark "
            f"of the standard; missing {missing or 'none'}, not in the standard {extra or 'none'}"
        )
    out = {}  # standard.md is the authored punctuation specification.
    for name in E.names():
        if name not in data:
            raise SystemExit(f"{os.path.relpath(DATA)}: error: `{name}` has no entry")
        enc = E.load(name)
        out[os.path.join(E.ENCODINGS, f"{name}.md")] = page(enc, data[name], fonts, standard, meanings)
    for name in E.names(kind="codage"):
        if name not in data:
            raise SystemExit(f"{os.path.relpath(DATA)}: error: `{name}` has no entry")
        enc = E.load(os.path.join(E.ENCODINGS, f"{name}.json"), _codage=True)
        out[os.path.join(E.ENCODINGS, f"{name}.md")] = codage_page(enc, data[name], fonts)
    for name in data:
        if name not in E.names() + E.names(kind="codage") and name != E.STANDARD:
            raise SystemExit(f"{os.path.relpath(DATA)}: error: `{name}` is not an encoding")
    return out


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="fail where a page is missing or out of date")
    args = parser.parse_args(argv)
    try:
        written = pages()
    except E.EncodingError as error:
        for fault in error.faults:
            print(fault, file=sys.stderr)
        return 1
    problems = []
    for path, text in written.items():
        try:
            with open(path, encoding="utf-8") as handle:
                current = handle.read()
        except OSError:
            current = None
        if args.check:
            if current != text:
                state = "is missing" if current is None else "differs from the encoding"
                problems.append(f"{E._shown(path)}: error: the page {state}; run python3 tools/encoding_docs.py")
        elif current != text:
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(text)
            print(E._shown(path))
    stale = [
        f for f in os.listdir(E.ENCODINGS)
        if f.endswith(".md") and f != "standard.md" and os.path.join(E.ENCODINGS, f) not in written
    ]
    for f in stale:
        problems.append(f"{E._shown(os.path.join(E.ENCODINGS, f))}: error: no encoding has this page")
    for line in problems:
        print(line, file=sys.stderr)
    if args.check and not problems:
        print(f"{E._shown(E.ENCODINGS)}: {len(written)} pages: ok")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
