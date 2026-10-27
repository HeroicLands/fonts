# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Check that every encoding is well formed, serves real faces and round-trips exactly.

    python3 tools/encodings_guard.py [--encodings DIR] [--fonts fonts.json] [--require-fonts]

Every encoding round-trips both ways: decoding an encoded roman text gives the text
back with each run of whitespace outside the literal markers as one space (nothing for a
script that writes none), and encoding decoded code points gives the code points back. For every encoding
file in ``encodings/`` it checks that

- the standard roman encoding, ``tools/encodings/standard.json``, gives each of its marks
  the mark of the mark's own characters, and has no row for whitespace;
- the file is well formed and contains the resolved standard rows, and every font it lists is a face
  in ``fonts.json``; no row of its own repeats a row of the standard;
- whitespace is one word separator: any run of space, tab, newline and carriage return
  outside the literal markers encodes as exactly the encoding's ``separator``, and no row
  matches whitespace; a script that spaces its words states a separator that is not empty,
  and a script that sets its characters directly beside each other (Zethu, Teng Chou) states
  ``""`` and writes no U+0020;
- it declares the characters it accepts (``accepts``), every ``from`` of its rows is made
  of declared characters or the standard's, a caseless script accepts ``a-z`` and no
  capital (and refuses one at its position), and Semaron and Helonika, the scripts with
  case, accept ``a-z`` and ``A-Z``;
- every standard mark round-trips, alone and inside a sentence, in the shared rows and
  in each face; a mark the script does not draw writes the standard's mark, so its
  sequence is identical in every encoding;
- a character outside the encoding is refused at its line and column, and so is a
  code point that no row writes;
- no row writes nothing, and no two rows with different ``from`` write one output;
- every row's output follows the mark rule: a row that draws nothing writes the mark of
  its ``from``, and a row writes its drawing, the mark of its ``from`` and the end mark
  when an earlier row with another ``from`` draws the same, when its drawing is a run
  of two or more other rows' drawings, or when it draws what the separator writes
  (``encode.mark`` spells a mark, and ``encode.is_run`` tells a run);
- every row round-trips in the shortest text found in which it applies (see
  ``tools/encoding_vectors.py``), and so does every row beside every row that draws
  nothing, before it and after it;
- the literal immutable markers ``\u27e6`` and ``\u27e7`` round-trip in every encoding, with
  mixed content around and between spans, writing the same marker marks in every encoding:
  character names where it states no ``codage``, and the codage's codes where it does;
  whitespace of any amount between codes only separates them, and decoding writes single
  spaces; an unmatched or nested marker, a code that names nothing and a standard mark
  inside a span are refused at their line and column, and a code outside the markers is
  ordinary roman, refused where the script does not accept it; every code of a codage
  round-trips between the markers of the script that states it, and the codage, a file of
  kind ``codage``, is refused as a whole-text encoding with the script's name in the
  error; a script encoding built beside each codage proves a stated codage where no
  shipped script states one;
- every published file includes its own code names and works in an empty directory;
- seeded random roman texts over the encoding's ``from`` alphabet round-trip, and so do
  random sequences of outputs, wherever encoding their ``from``s applies those rows;
- every sample text round-trips; a sample with a character outside the encoding, which a font guard sets
  to see the box, is refused;
- in every font an encoding lists, every non-writing character draws no ink and adds no
  advance: each text set with its marks shapes exactly as it does without them, and a
  row that draws nothing shapes to nothing;
- ``vectors.json`` beside the encodings is the one ``tools/encoding_vectors.py`` writes.

The font check needs uharfbuzz, and is skipped with a note under a Python without it
unless ``--require-fonts`` is given. Everything else runs under any Python 3.9 or later
with the standard library alone. A finding is ``file:line:column: error: message`` and
the exit status is 1.
"""

import argparse
import json
import os
import random
import string
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)
import encode as E  # noqa: E402
import encoding_vectors as V  # noqa: E402

FONTS = os.path.join(ROOT, "fonts.json")
# Random texts and random output sequences tried per encoding.
SWEEP = 400
# The most tokens in one random text.
LONGEST = 8


def families(path):
    """Every face in ``fonts.json`` by its slug, its class without ``hl-``."""
    with open(path, encoding="utf-8") as handle:
        listed = json.load(handle)["families"]
    return {f["class"][3:]: f for f in listed if f["class"].startswith("hl-")}


def _show(text):
    return json.dumps(text, ensure_ascii=False)


def _codepoints(text):
    return " ".join(f"U+{ord(c):04X}" for c in text)


class Report:
    def __init__(self):
        self.findings = []
        self.files = {}

    def add(self, enc, where, message):
        """A finding at a path in the encoding's file, or at a row in the file that
        states it."""
        path = enc.path
        if isinstance(where, E.Row):
            path, where = where.where
        line = column = None
        if path not in self.files:
            with open(path, encoding="utf-8") as handle:
                text = handle.read()
            self.files[path] = (text, E._positions(text)[0])
        text, offsets = self.files[path]
        offset = offsets.get(where)
        if offset is not None:
            line, column = E._line_column(text, offset)
        self.findings.append(str(E.EncodingError(message, path, line, column)))


def row_lists(enc):
    """Each list of rows with its face and its path in the file."""
    return [(None, ("rows",), enc.rows)] + [
        (slug, ("faces", slug, "rows"), face.rows) for slug, face in enc.faces.items()
    ]


def drawing(target):
    """What an output draws: the output without its trailing non-writing characters."""
    end = len(target)
    while end and E.is_mark(target[end - 1]):
        end -= 1
    return target[:end]


# The scripts with case: Semaron Kuriale and Helonika and the recensions that write them.
# Every other script is caseless.
CASED = ("semaron", "aelwythi-semaron", "helonika", "helonika-bethuan", "helonika-bizarian")


# Scripts whose characters are set directly beside each other: their separator is empty and
# no encoding output holds U+0020. Every other script spaces its words.
NO_SPACES = ("zethu", "teng-chou")

# Runs of whitespace, each one separator.
RUNS = (" ", "  ", "\t", "\n", "\r\n", " \t\n\r ", "\n\n\n")


def check_separator(report, enc):
    """Whitespace is one word separator: each run encodes as exactly the separator, a
    script that spaces its words has a separator, and one that does not writes no U+0020."""
    where = ("separator",)
    separator = enc.separator
    if separator is None:
        report.add(enc, where, f"`{enc.name}` states no `separator`")
        return
    if enc.name in NO_SPACES:
        if separator != "":
            report.add(enc, where, f"`{enc.name}` sets its characters beside each other, so its "
                       f"separator is empty, not {_show(separator)}")
    elif separator == "":
        report.add(enc, where, f"`{enc.name}` spaces its words, so its separator is not empty")
    for run in RUNS:
        try:
            written = E.encode(enc, run)
        except E.EncodingError as error:
            report.add(enc, where, f"the whitespace {_show(run)} is refused: {error.message}")
            continue
        if written != separator:
            report.add(enc, where, f"the whitespace {_show(run)} encodes to {_codepoints(written)}, "
                       f"not the separator {_codepoints(separator)}")
        if separator and E.decode(enc, written) != " ":
            report.add(enc, where, f"the separator {_codepoints(separator)} does not read back as a "
                       "single space")
        if enc.name in NO_SPACES and " " in written:
            report.add(enc, where, f"`{enc.name}` writes no spaces, yet {_show(run)} encodes to "
                       f"{_codepoints(written)}, which holds U+0020")
    unit = word_of(enc)
    if unit is None and enc.codage is not None:
        code = word_of(enc.codage)
        unit = f"{E.OPEN}{code}{E.CLOSE}" if code else None
    if unit is None:
        return
    single = E.encode(enc, unit)
    for run in RUNS:
        text = unit + run + unit
        try:
            written = E.encode(enc, text)
        except E.EncodingError as error:
            report.add(enc, where, f"{_show(text)} is refused: {error.message}")
            continue
        if written != single + separator + single:
            report.add(enc, where, f"{_show(text)} encodes to {_codepoints(written)}, not the word, "
                       f"one separator and the word")
        if enc.name in NO_SPACES and " " in written:
            report.add(enc, where, f"`{enc.name}` writes no spaces, yet {_show(text)} encodes to "
                       f"{_codepoints(written)}, which holds U+0020")
        read = E.decode(enc, written)
        if read != E.canonical(enc, text):
            report.add(enc, where, f"{_show(text)} reads back as {_show(read)}, not "
                       f"{_show(E.canonical(enc, text))}")


def check_accepted(report, enc):
    """The encoding declares what it accepts; every ``from`` is made of accepted
    characters; a caseless script accepts no capital and a script with case accepts both."""
    declared = enc.accepts | enc.standard_chars
    for face, at, rows in row_lists(enc):
        for row in rows:
            if row.where is not None and row.where[0] != enc.path:
                continue
            bad = sorted({c for c in row.source if c not in declared})
            if bad:
                report.add(enc, row, f"row {_show(row.source)} uses {_show(''.join(bad))}, which "
                           "`accepts` does not declare")
    if enc.codage is not None and not any(c.isalpha() for c in enc.accepts):
        return
    lower, upper = set(string.ascii_lowercase), set(string.ascii_uppercase)
    if not lower <= enc.accepts:
        report.add(enc, ("accepts",), "`accepts` lists `a-z`")
    if enc.name in CASED:
        if not upper <= enc.accepts:
            report.add(enc, ("accepts",), f"`{enc.name}` has case, so `accepts` lists `A-Z`")
    elif upper & enc.accepts:
        report.add(enc, ("accepts",), f"`{enc.name}` is caseless, so it accepts only lowercase "
                   "roman and no capital")


# --- what the rows write -------------------------------------------------------------


def check_outputs(report, enc):
    """No row writes nothing, no output reads back as two romans, and every output
    follows the mark rule."""
    if enc.round_trip == "canonical":
        # The loader validates structure; aliases and omitted marks are intentional.
        return
    for face, at, rows in row_lists(enc):
        firsts = {enc.separator: " "} if enc.separator else {}
        pool = rows + (enc.rows if face is not None else [])
        drawings = {drawing(r.target) for r in pool} - {""}
        for row in rows:
            where = row
            if row.source == " ":
                continue
            if enc.kind == "codage" and all(E.is_mark(c) for c in row.target):
                continue
            if row.target == "":
                report.add(
                    enc,
                    where,
                    f"row {_show(row.source)} writes nothing; a character the script does not "
                    f"write writes its mark, {_codepoints(E.mark(row.source))}",
                )
                continue
            drawn = drawing(row.target)
            if drawn == "":
                expected = E.mark(row.source)
            else:
                first = firsts.setdefault(drawn, row.source)
                if first == row.source and not E.is_run(drawn, drawings):
                    expected = drawn
                else:
                    expected = drawn + E.mark(row.source) + E.END_MARK
            if row.target != expected:
                report.add(
                    enc,
                    where,
                    f"row {_show(row.source)} writes {_codepoints(row.target)}; by the mark "
                    f"rule it writes {_codepoints(expected)}",
                )
    tiers = [(None, enc.rows)] + [(slug, enc.rows + f.rows) for slug, f in enc.faces.items()]
    for face, rows in tiers:
        readers = {}
        for row in rows:
            if row.target == "":
                continue
            other = readers.setdefault(row.target, row)
            if other.source != row.source:
                report.add(
                    enc,
                    row,
                    f"row {_show(row.source)} writes {_codepoints(row.target)}, which row "
                    f"{_show(other.source)} also writes, so decoding cannot tell them apart",
                )


# --- round trips -----------------------------------------------------------------------


def round_trip(report, enc, where, label, roman, face=None):
    """Whether ``roman`` reads back as its canonical form (each run of whitespace one
    space), and its code points encode back exactly."""
    try:
        unicode = E.encode(enc, roman, face)
    except E.EncodingError as error:
        report.add(enc, where, f"{label} {_show(roman)} is refused: {error.message}")
        return False
    try:
        read = E.decode(enc, unicode, face)
    except E.EncodingError as error:
        report.add(
            enc,
            where,
            f"{label} {_show(roman)} encodes to {_codepoints(unicode)}, which is refused in "
            f"decoding: {error.message}",
        )
        return False
    ok = True
    if read != E.canonical(enc, roman):
        report.add(
            enc,
            where,
            f"{label} {_show(roman)} encodes to {_codepoints(unicode)}, which reads back as "
            f"{_show(read)}, not {_show(E.canonical(enc, roman))}",
        )
        ok = False
    if enc.round_trip == "canonical":
        return ok
    again = E.encode(enc, read, face)
    if again != unicode:
        report.add(
            enc,
            where,
            f"{label} {_show(roman)} encodes to {_codepoints(unicode)}, which reads back as "
            f"{_show(read)}, which encodes to {_codepoints(again)}",
        )
        ok = False
    return ok


def check_rows(report, enc):
    """Every row round-trips where it applies, alone and beside a row that draws nothing."""
    for face, at, rows in row_lists(enc):
        silent = sorted({r.source for r in rows if r.target and drawing(r.target) == ""})
        for row in rows:
            where = row
            text = V.witness(enc, row, face)
            if text is None:
                report.add(
                    enc,
                    where,
                    f"row {_show(row.source)} applies in no text tried; another row shadows it",
                )
                continue
            if not round_trip(report, enc, where, "the row's text", text, face):
                continue
            for other in silent:
                for pair in (text + other, other + text):
                    # Joining rows can invalidate a positional rule, such as
                    # moving line-start indentation into the middle of a line.
                    if refused(enc, pair, face):
                        continue
                    if not round_trip(report, enc, where, "the row beside a silent row", pair, face):
                        break


def alphabet(enc, rows):
    """What a random roman text is made of: every ``from``, every character of one, and
    a space."""
    tokens = {r.source for r in rows} | {c for r in rows for c in r.source} | {" ", "\n"}
    return sorted(tokens)


def check_sweep(report, enc):
    """Seeded random roman texts, and random sequences of outputs, round-trip."""
    for face, at, rows in row_lists(enc):
        chooser = random.Random(f"{enc.name}:{face}")
        tokens = alphabet(enc, rows)
        failed = 0
        for _ in range(SWEEP):
            roman = "".join(chooser.choice(tokens) for _ in range(chooser.randint(1, LONGEST)))
            if refused(enc, roman, face):
                continue
            if not round_trip(report, enc, at, "the random text", roman, face):
                failed += 1
                if failed >= 3:
                    break
        failed = 0
        for _ in range(SWEEP):
            chosen = [chooser.choice(rows) for _ in range(chooser.randint(1, LONGEST))]
            roman = "".join(r.source for r in chosen)
            applied = [row for _, _, row in E.pieces(enc, roman, face, strict=False)]
            if [id(r) for r in applied] != [id(r) for r in chosen]:
                continue
            unicode = "".join(r.target for r in chosen)
            read = E.decode(enc, unicode, face)
            if enc.round_trip == "canonical":
                expected = E.canonical(enc, roman)
                wrong = read != expected
            else:
                wrong = read != E.canonical(enc, roman) or E.encode(enc, read, face) != unicode
            if wrong:
                report.add(
                    enc,
                    at,
                    f"the outputs {_codepoints(unicode)} of rows "
                    f"{', '.join(_show(r.source) for r in chosen)} read back as {_show(read)}, "
                    f"which encodes to {_codepoints(E.encode(enc, read, face))}",
                )
                failed += 1
                if failed >= 3:
                    break


def refused(enc, roman, face=None):
    """Whether encoding refuses ``roman``, which holds a character outside the encoding."""
    try:
        E.encode(enc, roman, face)
    except E.EncodingError:
        return True
    return False


def check_samples(report, enc):
    """Every sample round-trips, unless it holds a character no row matches: a font
    guard's text for the box, which encoding refuses."""
    for text in V.samples(enc):
        if all(row is not None for _, _, row in E.pieces(enc, text, strict=False)):
            round_trip(report, enc, ("rows",), "the sample", text)
        elif not refused(enc, text):
            report.add(enc, ("rows",), f"the sample {_show(text)} holds a character no row "
                       "matches, and encoding does not refuse it")


# --- the standard ------------------------------------------------------------------


def check_standard(report, directory):
    """The standard roman encoding: each mark writes the mark of its own characters, and
    it has no row for whitespace. Its marks, or ``None`` when it cannot be read."""
    path = V.standard_path(directory)
    try:
        standard = E.load_base(path)
    except E.EncodingError as error:
        report.findings += [str(f) for f in error.faults]
        return None
    marks = []
    for row in standard.rows:
        if row.conditioned and not (row.source == "^" and row.at == "line-start" and not row.before):
            report.add(standard, row, f"the standard's row {_show(row.source)} takes a condition; "
                       "the standard's rows apply everywhere")
        expected = E.mark(row.source)
        marks.append(row)
        if row.target != expected:
            report.add(standard, row, f"the standard's row {_show(row.source)} writes "
                       f"{_codepoints(row.target)}; it writes {_codepoints(expected)}")
    return marks


def word_of(enc):
    """A word of the encoding to set a mark beside: the ``from`` of its first row of
    letters alone that applies by itself."""
    for row in enc.own:
        if row.source.replace("_", "").isalnum() and V.witness(enc, row) == row.source:
            return row.source
    return None


def check_marks(report, enc, standard, marks):
    """The encoding extends the standard, repeats none of its rows, and round-trips
    every standard mark, alone and in a sentence. A mark it does not draw writes the
    standard's mark."""
    word = word_of(enc)
    verse = [m.source for m in marks if m.source in ("/", "//", "***")]
    for face, at, _ in row_lists(enc):
        # Verse marks that begin alike are matched longest first, whatever stands beside them.
        for first in verse:
            for second in verse:
                for text in (first + second, first + second + first, f"{first}\n{second}"):
                    round_trip(report, enc, at, "the verse marks", text, face)
        for mark in marks:
            texts = [mark.source]
            if word is not None and mark.source != "^":
                texts += [
                    word + mark.source,
                    mark.source + word,
                    f"{word} {word}{mark.source} {word}",
                    f"{word} {mark.source} {word}",
                ]
            for text in texts:
                if not round_trip(report, enc, at, f"the standard mark {_show(mark.source)} in",
                                  text, face):
                    break
            try:
                written = E.encode(enc, mark.source, face)
            except E.EncodingError:
                continue
            if enc.round_trip != "canonical" and drawing(written) == "" and written != mark.target:
                row = E.pieces(enc, mark.source, face)[0][2]
                report.add(
                    enc,
                    row,
                    f"the standard mark {_show(mark.source)}, which the script does not draw, "
                    f"writes {_codepoints(written)}; every encoding writes the standard's "
                    f"{_codepoints(mark.target)}",
                )


# Characters tried as ones outside an encoding, and code points no encoding writes.
STRANGERS = ("\u2603", ";", "\u00a0", "~")
UNWRITTEN = ("\U0010FFFD", E.END_MARK)


def check_refusal(report, enc):
    """A character outside the encoding is refused at its line and column, in encoding
    and in decoding."""
    word = word_of(enc) or ""
    firsts = {r.source[0] for r in enc.rows}
    for char in STRANGERS:
        if char in firsts or char in E.WHITESPACE:
            continue
        text = f"{word}\n{word}{char}"
        try:
            E.encode(enc, text)
        except E.EncodingError as error:
            if (error.line, error.column) != (2, len(word) + 1):
                report.add(enc, ("rows",), f"{_show(text)} is refused at {error.line}:"
                           f"{error.column}, not at 2:{len(word) + 1}")
        else:
            report.add(enc, ("rows",), f"{_show(text)} holds {_show(char)}, which no row "
                       "matches, and encoding does not refuse it")
    for char in string.ascii_uppercase:
        if char in enc.accepted:
            continue
        if not refuses_at(enc, E.encode, f"{word}{char}", 1, len(word) + 1):
            report.add(enc, ("accepts",), f"the capital {_show(char)} is not refused at 1:{len(word) + 1}")
    targets = {r.target[0] for r in enc.rows if r.target}
    for char in UNWRITTEN:
        if char in targets:
            continue
        try:
            E.decode(enc, char)
        except E.EncodingError as error:
            if (error.line, error.column) != (1, 1):
                report.add(enc, ("rows",), f"{_codepoints(char)} is refused in decoding at "
                           f"{error.line}:{error.column}, not at 1:1")
        else:
            report.add(enc, ("rows",), f"{_codepoints(char)}, which no row writes, is not "
                       "refused in decoding")


# --- the literal immutable markers ----------------------------------------------------

# Codes of characters every Python 3.9 or later names.
NAMES = ("U+00E1", "U+0069", "U+006D")


def refuses_at(enc, run, text, line, column, face=None):
    """Whether ``run`` (``E.encode`` or ``E.decode``) refuses ``text`` at the position."""
    try:
        run(enc, text, face)
    except E.EncodingError as error:
        return (error.line, error.column) == (line, column)
    return False


def named_code(enc):
    """A code of the script fonts' own characters: the name of the first character an
    encoding's rows write alone, or ``None``."""
    for row in enc.rows:
        if len(row.target) == 1 and E.character_name(row.target, enc) and not E.is_mark(row.target):
            return E.character_name(row.target, enc)
    return None


def check_markers(report, enc):
    """The literal immutable markers: with a codage stated they enclose its codes, and
    otherwise character names. They round-trip with mixed content, write the shared
    marker marks, and are refused where unmatched, nested or naming nothing."""
    where = ("rows",)
    word = word_of(enc) or ""
    opening, closing = E.mark(E.OPEN), E.mark(E.CLOSE)
    if enc.codage is not None:
        codes = word_of(enc.codage)
        if codes is None:
            report.add(enc, where, "its codage has no row of letters to try a span with")
            return
        pair = codes
        refused_code = "\u2603"
    else:
        codes = " ".join(NAMES)
        own = named_code(enc)
        pair = codes + (" " + own if own else "")
        codes = pair
        refused_code = "ACCUTE"
    span = f"{E.OPEN}{codes}{E.CLOSE}"
    texts = [
        span,
        f"{E.OPEN}{E.CLOSE}",
        f"{word}{span}",
        f"{span}{word}",
        f"{word} {span} {word}",
        f"{word}\n{span}\n{word}",
        f"{span}{span}",
        f"{word}{span}{word}{span}{word}",
    ]
    for text in texts:
        round_trip(report, enc, where, "the literal span text", text)
    unicode = E.encode(enc, span)
    if not (unicode.startswith(opening) and unicode.endswith(closing)):
        report.add(enc, where, f"{_show(span)} is not written between the marker marks "
                   f"{_codepoints(opening)} and {_codepoints(closing)}")
    inner = unicode[len(opening): len(unicode) - len(closing)]
    unmatched = (
        (f"{word}{E.OPEN}{codes}", 1, len(word) + 1),
        (E.CLOSE, 1, 1),
        (f"{word}{E.CLOSE}", 1, len(word) + 1),
        (f"{E.OPEN}{E.OPEN}{codes}{E.CLOSE}{E.CLOSE}", 1, 2),
        (f"{E.OPEN}{refused_code}{E.CLOSE}", 1, 2),
        (f"{word}\n{E.OPEN}{codes} {refused_code}{E.CLOSE}", 2, len(codes) + 3),
    )
    for text, line, column in unmatched:
        if not refuses_at(enc, E.encode, text, line, column):
            report.add(enc, where, f"{_show(text)} is not refused at {line}:{column}")
    decoding = (
        (closing + inner, 1, 1),
        (opening + inner, 1, 1),
        (opening + opening + inner + closing + closing, 1, len(opening) + 1),
    )
    for text, line, column in decoding:
        if not refuses_at(enc, E.decode, text, line, column):
            report.add(enc, where, f"{_codepoints(text)} is not refused in decoding at "
                       f"{line}:{column}")
    if E.decode(enc, unicode) != span:
        report.add(enc, where, f"{_show(span)} does not read back as itself")
    # Whitespace between codes only separates them; decoding writes the single space.
    loose = f"{E.OPEN}  {codes.replace(' ', '  ' + chr(10) + chr(9) + '  ')}\n{E.CLOSE}"
    if E.encode(enc, loose) != unicode:
        report.add(enc, where, f"{_show(loose)} does not encode as {_show(span)} does: whitespace "
                   "between codes is only a separator")
    if E.decode(enc, E.encode(enc, loose)) != span:
        report.add(enc, where, f"{_show(loose)} does not read back with single spaces")
    # No standard mark is allowed inside a span.
    for mark_char in (",", "?", "."):
        text = f"{E.OPEN}{codes}{mark_char}{E.CLOSE}"
        if not refuses_at(enc, E.encode, text, 1, len(codes) + 2):
            report.add(enc, where, f"{_show(text)} is not refused at 1:{len(codes) + 2}: a standard "
                       "mark is not allowed inside a span")
    # A code outside the markers is ordinary roman.
    if enc.codage is not None and not refused(enc, codes):
        report.add(enc, where, f"the code {_show(codes)} is read outside the markers; a codage is "
                   "recognized only between them")


def check_codage(report, enc, faces, shaping):
    """A codage, a file of kind ``codage``: it follows the mark rule, each code
    round-trips between the markers of the script that states it, shapes with marks that
    draw nothing, and the file is refused as a whole-text encoding."""
    codage = enc.codage
    check_outputs(report, codage)
    for row in codage.rows:
        round_trip(report, enc, row, "the code", f"{E.OPEN}{row.source}{E.CLOSE}")
    if shaping:
        check_fonts(report, codage, faces)


# --- in the fonts ----------------------------------------------------------------------


class Shaper:
    """Text shaped in one font by HarfBuzz, as a browser shapes it."""

    def __init__(self, path):
        import uharfbuzz as hb

        self.hb = hb
        with open(path, "rb") as handle:
            blob = hb.Blob(handle.read())
        self.font = hb.Font(hb.Face(blob))
        self.inked = {}

    def ink(self, glyph):
        if glyph not in self.inked:
            extents = self.font.get_glyph_extents(glyph)
            self.inked[glyph] = bool(extents and (extents.width or extents.height))
        return self.inked[glyph]

    def run(self, text):
        """The inked glyphs with their pen positions, and the total advance."""
        if text == "":
            return [], 0
        buf = self.hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        self.hb.shape(self.font, buf)
        x = 0
        out = []
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            if self.ink(info.codepoint):
                out.append((info.codepoint, x + pos.x_offset, pos.y_offset))
            x += pos.x_advance
        return out, x


def font_texts(enc, face):
    """The texts an encoding is shaped in: each row's text, and each sample."""
    texts = []
    rows = enc.rows + (enc.faces[face].rows if face in enc.faces else [])
    for row in rows:
        text = V.witness(enc, row, face)
        if text is not None and text not in texts:
            texts.append(text)
    texts += [t for t in V.samples(enc) if t not in texts]
    return texts


def check_fonts(report, enc, faces):
    for n, slug in enumerate(enc.fonts):
        listed = faces.get(slug)
        if listed is None:
            continue
        path = os.path.join(ROOT, listed["files"]["ttf"])
        shaper = Shaper(path)
        face = slug if slug in enc.faces else None
        failed = 0
        for text in font_texts(enc, face):
            if refused(enc, text, face):
                continue
            unicode = E.encode(enc, text, face)
            bare = "".join(c for c in unicode if not E.is_mark(c))
            if bare == unicode:
                continue
            marked, plain = shaper.run(unicode), shaper.run(bare)
            if marked != plain:
                report.add(
                    enc,
                    ("fonts", n),
                    f"in `{slug}`, {_show(text)} encodes to {_codepoints(unicode)}, which "
                    f"shapes to {len(marked[0])} inked glyphs and an advance of {marked[1]}; "
                    f"without its marks it shapes to {len(plain[0])} and {plain[1]}",
                )
                failed += 1
                if failed >= 3:
                    break
        for _, at, rows in row_lists(enc):
            for row in rows:
                if row.target and drawing(row.target) == "":
                    glyphs, advance = shaper.run(row.target)
                    if glyphs or advance:
                        report.add(
                            enc,
                            row,
                            f"in `{slug}`, the mark {_codepoints(row.target)} of "
                            f"{_show(row.source)} shapes to {len(glyphs)} inked glyphs and an "
                            f"advance of {advance}",
                        )


def can_shape():
    try:
        import uharfbuzz  # noqa: F401
    except ImportError:
        return False
    return True


# --- the whole ------------------------------------------------------------------------


def check(directory, fonts, require_fonts=False):
    report = Report()
    try:
        faces = families(fonts)
    except (OSError, ValueError, KeyError) as error:
        return [f"{E._shown(fonts)}: error: cannot read the faces: {error}"], False
    marks = check_standard(report, directory)
    standard = E.load_base(V.standard_path(directory)) if marks is not None else None
    encodings = []
    for name in V._names(directory):
        try:
            encodings.append(E.load(os.path.join(directory, f"{name}.json")))
        except E.EncodingError as error:
            report.findings += [str(f) for f in error.faults]
    shaping = can_shape()
    if require_fonts and not shaping:
        report.findings.append("encodings_guard.py: error: the font check needs uharfbuzz")
    for enc in encodings:
        for n, slug in enumerate(enc.fonts):
            if slug not in faces:
                report.add(enc, ("fonts", n), f"`{slug}` is not a face in {os.path.basename(fonts)}")
        check_outputs(report, enc)
        check_accepted(report, enc)
        check_separator(report, enc)
        if enc.codage is not None:
            check_codage(report, enc, faces, shaping)
        if standard is not None:
            check_marks(report, enc, standard, marks)
        check_refusal(report, enc)
        check_markers(report, enc)
        check_rows(report, enc)
        check_sweep(report, enc)
        check_samples(report, enc)
        if shaping:
            check_fonts(report, enc, faces)
    # Every published file must work with no neighbour available.
    import publish_encodings as P
    for enc in encodings:
        with tempfile.TemporaryDirectory() as tmp:
            standalone = os.path.join(tmp, enc.name + ".json")
            shutil.copy(enc.path, standalone)
            try:
                isolated = E.load(standalone)
                for value in V.build([enc])[enc.name]:
                    roman = value["roman"]
                    if "refused" in value:
                        if not refuses_at(isolated, E.encode, roman, *value["refused"], face=value.get("face")):
                            report.add(enc, ("rows",), "an isolated vector has a different refusal")
                    elif E.encode(isolated, roman, value.get("face")) != value["unicode"] or E.decode(isolated, value["unicode"], value.get("face")) != value["decoded"]:
                        report.add(enc, ("rows",), "an isolated vector has a different result")
            except E.EncodingError as error:
                report.findings.append(str(error))
    for name, expected in P.build().items():
        path = os.path.join(directory, name)
        if not os.path.exists(path) or open(path, encoding="utf-8").read() != expected:
            report.findings.append(f"{path}: error: differs from resolved sources; run tools/publish_encodings.py")
    if not report.findings:
        expected = V.dumps(V.build(encodings))
        path = V.vectors_path(directory)
        try:
            with open(path, encoding="utf-8") as handle:
                current = handle.read()
        except OSError:
            current = None
        if current != expected:
            report.findings.append(
                f"{E._shown(path)}: error: the vectors differ from the encodings; "
                "run python3 tools/encoding_vectors.py --write"
            )
    return report.findings, shaping


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--encodings", default=E.ENCODINGS, help="the directory of encodings")
    parser.add_argument("--fonts", default=FONTS, help="the font manifest")
    parser.add_argument(
        "--require-fonts", action="store_true", help="fail rather than skip the font check"
    )
    args = parser.parse_args(argv)
    findings, shaped = check(args.encodings, args.fonts, args.require_fonts)
    for finding in findings:
        print(finding, file=sys.stderr)
    count = len(V._names(args.encodings)) if os.path.isdir(args.encodings) else 0
    if not shaped:
        print("encodings_guard.py: the font check needs uharfbuzz, and is skipped")
    print(
        f"{E._shown(args.encodings)}: {count} encodings: "
        + ("ok" if not findings else f"{len(findings)} findings")
    )
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
