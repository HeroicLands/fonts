# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Write roman text in a script font's code points by an encoding, and read it back.

    python3 encode.py --encoding pirzath "zaron tholmeza"
    python3 encode.py --encoding pirzath --decode "<the code points>"
    python3 encode.py --encoding encodings/pirzath.json --face pirzath-hand --codepoints -
    python3 encode.py --encoding pirzath --file note.txt
    python3 encode.py --font teng-chou "\u27e6SUN MOON\u27e7"
    python3 encode.py --list

An encoding is one JSON file, ``encodings/<name>.json``:

    {
        "name": "pirzath",
        "fonts": ["pirzath-carved", "pirzath-hand"],
        "extends": "standard",
        "separator": " ",
        "vowels": "aeiou",
        "rows": [
            ["a", "\\uDB80\\uDE30"],
            [".", "\\uDB80\\uDC50"],
            ["?", "\\uDB80\\uDC50\\uDB40\\uDD1F\\uDB40\\uDDEF"],
            ["-", "\\uDB40\\uDD0D"],
            {"from": "y", "to": "\\uDB80\\uDE37", "before": "consonant"}
        ],
        "faces": {"pirzath-hand": {"rows": [["a", "\\uDB80\\uDE31"]]}}
    }

``name``, ``fonts``, ``accepts``, ``separator`` and ``rows`` are required; the rest are
optional.
``fonts`` lists the slugs of the faces the encoding serves.

``groupCase: "initial"`` permits multi-letter alphabetic rows only in lowercase
or with their first letter capitalized. Other case patterns are refused before
single-letter fallback, including inside longer words. Literal spans are unaffected.

``--verse`` (or ``encode(..., verse=True)``) reads verse line endings and blank
lines as the standard line and stanza controls. Prose keeps normal whitespace
normalization. A line containing ``--- {.canto}`` writes the canto control.

``roundTrip`` defaults to ``"exact"``. An encoding may explicitly choose
``"canonical"`` when its orthography permits several Roman spellings for one
output or omits punctuation. In that mode empty outputs and duplicate outputs
are allowed. Decoding ignores empty outputs and chooses the first authored
source for an identical output; the word separator takes precedence over rows
that write the same space. Original spelling and omitted punctuation are not
recoverable, and re-encoding arbitrary decoded output is not guaranteed to
reproduce the original code points. Other encodings retain exact round trips.

``accepts`` declares the characters the encoding accepts as roman: a list of single
characters and of ranges of three characters such as ``"a-z"``. A caseless script lists
``"a-z"`` and its own additions (diacritics, the catch, digits); Semaron and Helonika, the
scripts with case, list ``"a-z"`` and ``"A-Z"``. Besides these the encoding accepts the
characters of the standard's marks and whitespace. Any other character is refused at its
line and column, and every row's ``from`` is made of accepted characters.

``separator`` is what the script writes for a word separator, and is the one place whitespace
is stated. In roman, outside ``\u27e6`` and ``\u27e7``, any run of whitespace (space, tab,
newline, carriage return) is one word separator: it is not a character of the script, and no
row matches it. The encoding writes ``separator`` once for each run. A script that spaces its
words states ``" "``, one U+0020, or the glyph of its own space; a script that sets its
characters beside each other states ``""`` and writes nothing. Decoding writes a single space
for a separator written, and nothing is read from ``""``. So the roman's whitespace is
normalized, and not preserved: ``a  \t\n b`` and ``a b`` encode alike, and decoding gives
``a b``. A line break is only whitespace; the structure of verse (a line end, a stanza end, a
canto end) is written by ``/``, ``//`` and ``***``.

``codage`` names a file beside this one, the script's codage: a file with ``"kind":
"codage"`` that names each sign of the script by a code, such as ``zethu-mdc`` for the
Zethu script. It sets what the literal immutable markers enclose (see below). A codage
file takes only ``name``, ``kind``, ``fonts`` and ``rows``, extends nothing and encodes no
text of its own: it is reached only between the markers of an encoding that states it.
Asking for one as a whole-text encoding is an error that names the encoding to use.

A font that has no encoding file accepts nothing as roman: ``for_font(slug)``, or
``--font slug``, gives a names-only encoding, where text is written only as character
names between the literal markers and anything outside them is refused.

``extends`` names a base file beside the encoding, ``encodings/standard.json`` for
every encoding here: the standard roman encoding, which holds the roman punctuation
every language shares. It has no whitespace rows. A base file holds only ``name`` and ``rows``.
The encoding's rows are the base's rows whose ``from`` no row of the encoding states,
in the base's order, followed by the encoding's own rows. So an encoding whose script
draws a standard mark states a row for it, and every other mark keeps the base's row.
Nothing else is inherited, and once the rows are put together they are the whole
encoding.

Every encoding round-trips both ways: decoding an encoded roman text gives it back with each
run of whitespace outside the markers as one space (nothing for a script that writes none),
and encoding decoded code points gives them back exactly. So no row writes nothing, and
no two rows with different ``from`` write one output. Where a script does not write a
character, or draws two alike, the row says so with a mark of non-writing characters:

- A mark spells a ``from`` in variation selectors VS17 to VS111, U+E0100 to
  U+E015E, which are invisible and default-ignorable: printable ASCII character ``c`` is
  U+E0100 + (``c`` - U+0020), so ``a`` is U+E0141. Reserved low selectors are escaped in generic metadata. Each character of
  ``from`` is spelled as itself when it is printable ASCII other than ``{``, and
  otherwise as ``{``, its code point in lowercase hex, and ``}``: ``á`` is spelled
  ``{e1}``. ``mark`` writes one.
- A row that draws nothing (a vowel in an abjad, an inherent vowel, a quadrat or word
  separator) writes the escaped mark of its ``from``.
- A row writes its drawing, the mark of its ``from`` and the end mark, VS256 U+E01EF,
  when an earlier row with another ``from`` draws the same, when its drawing is a run of
  two or more other rows' drawings, or when it draws what the separator writes. After ``.``, ``?`` writes the glyph of ``.``, U+E0101 and U+E01EF;
  ``cch``, drawn as ``ch`` twice, writes the two glyphs, its mark and the end mark.
  The first row in authored order to draw a drawing keeps it bare, and so does any
  later row with the same ``from``. ``is_run`` tells a run.

The marks are written into the rows; reading a file applies no rule of its own. The
files write the non-writing characters as ``\\u`` escapes, so that they show.

The literal immutable markers, ``\u27e6`` and ``\u27e7``, enclose exact characters, which
no row of the encoding reinterprets. Every encoding supports them:

- Each marker is written as the mark of itself, ``mark("\u27e6")`` and
  ``mark("\u27e7")``, the same invisible sequence in every encoding.
- With no ``codage`` stated, what the markers enclose are character names: each code is a
  character's name in capitals with its spaces written ``_``, as in
  ``\u27e6LATIN_SMALL_LETTER_A_WITH_ACUTE LATIN_SMALL_LETTER_I\u27e7``, which writes ``ái``.
  Codes are separated by whitespace, which writes nothing. A name comes
  from ``encodings/names.json`` for the characters of the script fonts, and from Python's
  ``unicodedata`` for every other character. A name that names no character is refused at
  its position. Decoding names each character between the marker marks, and separates the
  codes with single spaces.
- With a ``codage`` stated, the enclosed text is encoded by that codage and decoded
  through it, so the codes are the codage's own: ``\u27e6WONG_YELLOW\u27e7`` in the Zethu script.
  Only the codage's codes and its own notation are allowed inside, such as Zethu's ``-``
  ``:`` ``*`` ``(`` ``)`` ``<`` ``>`` and ``[ts]``: a standard mark such as ``,`` or ``?``
  is refused at its position, and a code outside the markers is ordinary roman, never read
  as a code.
- Whitespace inside the markers only separates codes: any amount of space, newline or tab is
  a separator and is not saved, so ``\u27e6ONE TWO THREE\u27e7`` and the same codes with runs of spaces, tabs and line breaks
  between them are the same text. Decoding always writes single spaces between codes.
- An unmatched ``\u27e6`` or ``\u27e7``, and a marker inside a span, are refused at the
  offending marker's line and column; decoding refuses the marker marks in the same cases.
- No row states a marker.

Encoding:

- A row is ``[from, to]`` or ``{"from", "to", "before"?, "at"?}``. ``from`` and ``to``
  are each one or more characters.
- The longest ``from`` wins. Among rows of one length, a row with a condition that
  holds comes before a row with none, and otherwise the earlier row wins. A row whose
  condition fails is skipped.
- ``before: vowel`` holds when the next character is one of ``vowels``; ``before:
  consonant`` when it is any other letter. Neither holds at the end of the text.
- ``at: start`` holds at the text's first character or after a boundary; ``at: end``
  at the text's last character or before one. A boundary is whitespace, punctuation
  or a symbol.
- A face's own rows (``faces``) apply when text is set in that face, and are tried
  before the shared rows: a face row that matches wins.
- A character no row matches is refused: encoding stops with an error that names it
  and its line and column in the text. Nothing passes through.

Decoding reads the rows backward, by plain longest match: at each point the longest
``to`` that the code points continue with is read as its row's ``from``. A code point
that begins no ``to`` there is refused in the same way. Text set in a face reads its
face's rows and the shared rows together.

Errors are reported as ``file:line:column: error: message`` and exit non-zero. A text
read with ``--file`` is reported by its path, standard input as ``<stdin>`` and a text
given on the command line as ``<text>``.
"""

import argparse
import json
import os
import re
import sys
import unicodedata
from json.decoder import scanstring

HERE = os.path.dirname(os.path.abspath(__file__))
ENCODINGS = os.path.join(HERE, "encodings")

NAME = re.compile(r"^[a-z0-9-]+$")
CONDITIONS = {"before": ("vowel", "consonant"), "at": ("start", "end", "line-start")}
GENERIC_FAMILIES = ("mono", "serif", "sans")
TOP_KEYS = ("name", "kind", "fonts", "extends", "codage", "accepts", "separator", "vowels", "rows",
            "faces", "roundTrip", "groupCase")
# What a file is: an encoding of a script, or a codage, the notation a script's literal
# spans are written in.
KINDS = ("encoding", "codage")
# The keys a codage takes: its rows draw the script's signs, and it has no roman of its own.
CODAGE_KEYS = ("name", "kind", "fonts", "rows")
# The keys of a base file, which an encoding extends.
BASE_KEYS = ("name", "rows", "controls")
# Keys an encoding does not take, with why.
REFUSED_KEYS = {
    "decode": "decoding reads every output back as its own row's `from`",
    "separators": "a row that draws nothing writes its mark, so decoding restores it",
}
ROW_KEYS = ("from", "to", "before", "at")
FACE_KEYS = ("rows",)
# The standard roman encoding, the base every encoding here extends.
STANDARD = "standard"
# Not encodings, though they sit in encodings/.
NOT_ENCODINGS = ("vectors", "names", STANDARD)
# The names of the characters of the script fonts, shipped beside the encodings.
NAMES = "names"
# The whitespace a roman text is made to separate its words by: one run is one separator.
WHITESPACE = " \t\n\r"
# The literal immutable markers.
OPEN = "\u27e6"
CLOSE = "\u27e7"
# How a text that is not a file is named in a refusal.
TEXT = "<text>"


class EncodingError(Exception):
    """A fault in an encoding file, or in how one was asked for, with its position."""

    def __init__(self, message, file=None, line=None, column=None):
        super().__init__(message)
        self.message = message
        self.file = file
        self.line = line
        self.column = column
        self.faults = [self]

    def __str__(self):
        where = ""
        if self.file is not None:
            where = _shown(self.file) + ":"
            if self.line is not None:
                where += f"{self.line}:"
                if self.column is not None:
                    where += f"{self.column}:"
            where += " "
        else:
            where = "encode.py: "
        return f"{where}error: {self.message}"


def _shown(path):
    """A path relative to the working directory when it lies beneath it."""
    try:
        rel = os.path.relpath(path)
    except ValueError:
        return path
    return path if rel.startswith("..") else rel


# --- reading JSON with positions ---------------------------------------------------

_NUMBER = re.compile(r"-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][-+]?\d+)?")
_SPACE = re.compile(r"[ \t\n\r]*")


def _positions(text):
    """The offset of every value in a JSON text, and of every object key, by path.

    The text is already known to be valid JSON. A path is a tuple of keys and list
    indices; ``(path, "key")`` gives the offset of the key that names ``path``. A key
    stated twice in one object is a fault, since ``json`` keeps the last silently.
    """
    where = {}
    duplicates = []

    def skip(i):
        return _SPACE.match(text, i).end()

    def value(i, path):
        i = skip(i)
        where[path] = i
        c = text[i]
        if c == "{":
            i = skip(i + 1)
            seen = set()
            if text[i] == "}":
                return i + 1
            while True:
                i = skip(i)
                start = i
                key, i = scanstring(text, i + 1)
                if key in seen:
                    duplicates.append((path + (key,), start))
                seen.add(key)
                where[(path + (key,), "key")] = start
                i = skip(i)
                i = value(i + 1, path + (key,))
                i = skip(i)
                if text[i] == "}":
                    return i + 1
                i += 1
        if c == "[":
            i = skip(i + 1)
            if text[i] == "]":
                return i + 1
            n = 0
            while True:
                i = value(i, path + (n,))
                n += 1
                i = skip(i)
                if text[i] == "]":
                    return i + 1
                i += 1
        if c == '"':
            return scanstring(text, i + 1)[1]
        for word in ("true", "false", "null"):
            if text.startswith(word, i):
                return i + len(word)
        return _NUMBER.match(text, i).end()

    value(0, ())
    return where, duplicates


def _line_column(text, offset):
    line = text.count("\n", 0, offset) + 1
    column = offset - (text.rfind("\n", 0, offset) + 1) + 1
    return line, column


# --- the encoding ----------------------------------------------------------------


class Row:
    """One row: what it matches, what it writes, and its conditions.

    ``order`` is the row's place among the rows it is applied with, and ``where`` the
    file it is stated in with its path there, such as ``("rows", 3)``.
    """

    __slots__ = ("source", "target", "before", "at", "order", "where")

    def __init__(self, source, target, before=None, at=None, order=0, where=None):
        self.source = source
        self.target = target
        self.before = before
        self.at = at
        self.order = order
        self.where = where

    @property
    def conditioned(self):
        return bool(self.before or self.at)

    def as_json(self):
        if not self.conditioned:
            return [self.source, self.target]
        out = {"from": self.source, "to": self.target}
        if self.before:
            out["before"] = self.before
        if self.at:
            out["at"] = self.at
        return out

    def __repr__(self):
        return f"Row({self.as_json()!r})"


def _index_rows(rows):
    """Rows by the first character of ``from``: longest first, conditioned before
    plain, then in authored order."""
    by_first = {}
    for row in rows:
        by_first.setdefault(row.source[0], []).append(row)
    for first, group in by_first.items():
        group.sort(key=lambda r: (-len(r.source), not r.conditioned, r.order))
    return by_first


def _readings(rows):
    """The ``from`` each ``to`` reads back as, indexed by the first character of the
    ``to``, longest ``to`` first."""
    table = {}
    for row in rows:
        if row.target:
            table.setdefault(row.target, row.source)
    by_first = {}
    for target, source in table.items():
        by_first.setdefault(target[0], []).append((target, source))
    for group in by_first.values():
        group.sort(key=lambda pair: -len(pair[0]))
    return by_first


class Face:
    __slots__ = ("rows", "by_first", "readings")

    def __init__(self, rows, shared=(), separator=()):
        self.rows = rows
        self.by_first = _index_rows(rows)
        self.readings = _readings(list(separator) + list(rows) + list(shared))


class Encoding:
    """An encoding, read from its file and ready to apply.

    ``rows`` are the rows it applies, its base's first; ``own`` are the rows its file
    states, ``base`` is the path of the file it extends, or ``None``, and ``codage`` is
    the encoding its ``codage`` names, or ``None``.
    """

    def __init__(self, data, path, base=None, codage=None):
        self.path = path
        self.name = data["name"]
        self.round_trip = data.get("roundTrip", "exact")
        self.group_case = data.get("groupCase")
        self.controls = dict(base.controls) if base is not None else {}
        self.kind = data.get("kind", "encoding")
        self.codage = codage
        self.fonts = list(data["fonts"])
        self.vowels = frozenset(data.get("vowels", ""))
        # What the script writes for a word separator, or ``None`` where the encoding
        # takes no whitespace outside the literal markers.
        self.separator = data.get("separator")
        self.separator_row = None
        if self.separator is not None:
            self.separator_row = Row(" ", self.separator, where=(path, ("separator",)))
        self.base = base.path if base is not None else None
        self.own = [_read_row(row, n, (path, ("rows", n))) for n, row in enumerate(data["rows"])]
        stated = {row.source for row in self.own}
        inherited = []
        if base is not None:
            inherited = [
                Row(r.source, r.target, r.before, r.at, where=r.where)
                for r in base.rows
                if r.source not in stated or (r.conditioned and not any(
                    (own.source, own.before, own.at) == (r.source, r.before, r.at)
                    for own in self.own))
            ]
        self.rows = inherited + self.own
        for n, row in enumerate(self.rows):
            row.order = n
        # What the encoding accepts as roman: its declared characters and the characters
        # of the standard's marks and whitespace. A codage accepts the characters of its
        # own codes and notation.
        self.declared = list(data.get("accepts", []))
        self.accepts = accepted(self.declared)
        self.standard_chars = frozenset(c for r in (base.rows if base is not None else ()) for c in r.source)
        if self.kind == "codage":
            self.accepted = frozenset(c for r in self.rows for c in r.source)
        else:
            self.accepted = self.accepts | self.standard_chars
        reads = [self.separator_row] if self.separator else []
        control_rows = [Row("\n\n", self.controls["verseStanza"])] if "verseStanza" in self.controls else []
        if "verseCanto" in self.controls:
            control_rows.append(Row("--- {.canto}", self.controls["verseCanto"]))
        self.shared = Face(self.rows, separator=reads + control_rows)
        self.faces = {}
        for slug, face in data.get("faces", {}).items():
            at = ("faces", slug, "rows")
            rows = [_read_row(row, n, (path, at + (n,))) for n, row in enumerate(face.get("rows", []))]
            self.faces[slug] = Face(rows, self.rows, reads)

    @classmethod
    def names_only(cls, font):
        """The encoding of a font that has none: it accepts no roman at all, so text in
        the font is written only as character names between the literal markers."""
        enc = cls({"name": font, "fonts": [font], "rows": [], "accepts": []}, None)
        enc.font_only = True
        return enc

    font_only = False

    def tiers(self, face):
        if face is not None and face not in self.fonts:
            raise EncodingError(
                f"`{self.name}` serves {', '.join(self.fonts)}, not `{face}`", self.path
            )
        own = self.faces.get(face) if face is not None else None
        return [own, self.shared] if own else [self.shared]

    def __repr__(self):
        return f"Encoding({self.name!r})"


def accepted(spec):
    """The set of characters an ``accepts`` list declares: each item is one character, or
    a range of three characters, ``a-z``."""
    out = set()
    for item in spec:
        if len(item) == 1:
            out.add(item)
        else:
            out.update(chr(c) for c in range(ord(item[0]), ord(item[2]) + 1))
    return frozenset(out)


def _accepts_faults(value, fault):
    if not isinstance(value, list) or not all(isinstance(i, str) for i in value):
        fault(("accepts",), "`accepts` is a list of characters and ranges such as `\"a-z\"`")
        return
    for n, item in enumerate(value):
        if len(item) == 1:
            continue
        if len(item) == 3 and item[1] == "-" and item[0] < item[2]:
            continue
        fault(("accepts", n), f"{json.dumps(item, ensure_ascii=False)} is neither one character "
              "nor a range of two characters joined by `-`, such as `\"a-z\"`")


class Base:
    """A base file, which encodings extend: its name and its rows."""

    def __init__(self, data, path):
        self.path = path
        self.name = data["name"]
        self.controls = dict(data.get("controls", {}))
        self.rows = [_read_row(row, n, (path, ("rows", n))) for n, row in enumerate(data["rows"])]

    def __repr__(self):
        return f"Base({self.name!r})"


def _read_row(row, order, where=None):
    if isinstance(row, list):
        return Row(row[0], row[1], order=order, where=where)
    return Row(row["from"], row["to"], row.get("before"), row.get("at"), order, where)


NOTHING = (
    "writes nothing; a row that draws nothing writes the mark of its `from`, "
    "so that decoding restores it"
)


WHITESPACE_FROM = (
    "has whitespace in its `from`; whitespace is the word separator, stated by `separator`, "
    "and no row matches it"
)


MARKERS = (
    "states a literal immutable marker, \u27e6 or \u27e7; the markers enclose a span of the "
    "codage, and no row matches them"
)


def _check_outputs(enc):
    """No two rows with different ``from`` write one output, among the rows the encoding
    applies or among a face's rows and those. Each fault is at the later row, in the
    file that states it."""
    if enc.round_trip == "canonical":
        return []
    tiers = [enc.rows] + [enc.rows + face.rows for face in enc.faces.values()]
    faults = []
    reported = set()
    for tier in tiers:
        readers = {}
        if enc.separator:
            readers[enc.separator] = enc.separator_row
        for row in tier:
            first = readers.setdefault(row.target, row)
            if first.source != row.source and row.where not in reported:
                reported.add(row.where)
                path, at = first.where
                shown = ".".join(map(str, at))
                if path != row.where[0]:
                    shown = f"{_shown(path)} {shown}"
                faults.append(
                    _fault_at(
                        row.where,
                        f"writes what the row at {shown} writes, for "
                        f"{json.dumps(first.source, ensure_ascii=False)}; a row that draws what an "
                        "earlier row draws adds the mark of its `from` and the end mark",
                    )
                )
    return faults


# The text and value offsets of every file read, by path.
_FILES = {}


def _fault_at(where, message, key=False):
    """An ``EncodingError`` at a path in a file already read."""
    path, at = where
    text, offsets = _FILES[path]
    offset = offsets.get((at, "key") if key else at)
    if offset is None:
        return EncodingError(message, path)
    return EncodingError(message, path, *_line_column(text, offset))


def _rows_faults(rows, at, fault, vowels, allow_empty=False):
    """Every structural fault in a list of rows."""
    if not isinstance(rows, list):
        fault(at, "`rows` is a list of rows")
        return
    for n, row in enumerate(rows):
        here = at + (n,)
        if isinstance(row, list):
            if len(row) != 2 or not all(isinstance(s, str) for s in row):
                fault(here, "a row written as a list is two strings, `[from, to]`")
            elif OPEN in row[0] or CLOSE in row[0]:
                fault(here, MARKERS)
            elif row[0] == "":
                fault(here, "has an empty `from`; a row matches one or more characters")
            elif any(c in WHITESPACE for c in row[0]):
                fault(here, WHITESPACE_FROM)
            elif row[1] == "" and not allow_empty:
                fault(here + (1,), NOTHING)
            continue
        if not isinstance(row, dict):
            fault(here, "a row is `[from, to]` or `{from, to, before?, at?}`")
            continue
        for key in row:
            if key not in ROW_KEYS:
                fault(
                    here + (key,),
                    f"`{key}` is not a row key; a row takes `from`, `to`, `before` and `at`",
                    key=True,
                )
        if isinstance(row.get("from"), str) and (OPEN in row["from"] or CLOSE in row["from"]):
            fault(here + ("from",), MARKERS)
        if not isinstance(row.get("from"), str) or row.get("from") == "":
            fault(here + ("from",) if "from" in row else here,
                  "needs `from`, the one or more characters the row matches")
        elif any(c in WHITESPACE for c in row["from"]):
            fault(here + ("from",), WHITESPACE_FROM)
        if not isinstance(row.get("to"), str):
            fault(here + ("to",) if "to" in row else here,
                  "needs `to`, the one or more characters the row writes")
        elif row["to"] == "" and not allow_empty:
            fault(here + ("to",), NOTHING)
        for condition, allowed in CONDITIONS.items():
            if condition not in row:
                continue
            value = row[condition]
            if value not in allowed:
                fault(
                    here + (condition,),
                    f"`{condition}` is {' or '.join(f'`{a}`' for a in allowed)}, "
                    f"not {json.dumps(value, ensure_ascii=False)}",
                )
            elif condition == "before" and not vowels:
                fault(here + (condition,), "`before` needs the encoding's `vowels` to read by",
                      key=True)


def _faults_of(path, text):
    """A function that records a fault at a path in ``text``, and the list it fills.
    A key stated twice is a fault already in the list."""
    where, duplicates = _positions(text)
    _FILES[path] = (text, where)
    faults = []

    def fault(at, message, key=False):
        faults.append(_fault_at((path, at), message, key))

    for at, _ in duplicates:
        fault(at, f"`{'.'.join(map(str, at))}` is stated twice", key=True)
    return fault, faults


def _check_name(data, path, fault):
    name = data.get("name")
    stem = os.path.splitext(os.path.basename(path))[0]
    if not isinstance(name, str) or not NAME.match(name):
        fault(("name",) if "name" in data else (), "needs `name`: lowercase letters, digits and `-`")
    elif name != stem:
        fault(("name",), f"`name` is `{name}`, and the file is `{stem}.json`; they are the same")


def _check_base(data, text, path):
    """Every structural fault in a base file, each at its position."""
    fault, faults = _faults_of(path, text)
    if not isinstance(data, dict):
        fault((), "a base file is a JSON object")
        return faults
    for key in data:
        if key not in BASE_KEYS:
            fault(
                (key,),
                f"`{key}` is not a key of a base file; a base file takes "
                + ", ".join(f"`{k}`" for k in BASE_KEYS),
                key=True,
            )
    _check_name(data, path, fault)
    if "rows" not in data:
        fault((), "needs `rows`")
    else:
        _rows_faults(data["rows"], ("rows",), fault, "")
    controls = data.get("controls", {})
    allowed = ("verseStanza", "verseCanto", "wordSeparator", "literalOpen", "literalClose")
    if not isinstance(controls, dict):
        fault(("controls",), "`controls` is a map of shared structural marks")
    else:
        for key, value in controls.items():
            if key not in allowed or not isinstance(value, str) or not value:
                fault(("controls", key), "a shared structural control has a known name and a nonempty string")
    return faults


def _check(data, text, path):
    """Every structural fault in an encoding file, each at its position."""
    fault, faults = _faults_of(path, text)
    if not isinstance(data, dict):
        fault((), "an encoding file is a JSON object")
        return faults
    for key in data:
        if key in REFUSED_KEYS:
            fault((key,), f"`{key}` is not an encoding key: {REFUSED_KEYS[key]}", key=True)
        elif key not in TOP_KEYS:
            fault(
                (key,),
                f"`{key}` is not an encoding key; an encoding takes "
                + ", ".join(f"`{k}`" for k in TOP_KEYS),
                key=True,
            )
    _check_name(data, path, fault)
    if "groupCase" in data and data["groupCase"] != "initial":
        fault(("groupCase",), "`groupCase` is `initial` when stated")
    if data.get("roundTrip", "exact") not in ("exact", "canonical"):
        fault(("roundTrip",), "`roundTrip` is `exact` or `canonical`")
    kind = data.get("kind", "encoding")
    if kind not in KINDS:
        fault(("kind",), "`kind` is `encoding` or `codage`")
        kind = "encoding"
    if kind == "codage":
        for key in data:
            if key in TOP_KEYS and key not in CODAGE_KEYS:
                fault((key,), f"`{key}` is not a key of a codage; a codage takes "
                      + ", ".join(f"`{k}`" for k in CODAGE_KEYS), key=True)
    else:
        if "accepts" not in data:
            fault((), "needs `accepts`, the characters the encoding accepts as roman: a list of "
                  'characters and ranges such as `"a-z"`')
        else:
            _accepts_faults(data["accepts"], fault)
        if "separator" not in data:
            fault((), 'needs `separator`, what the script writes for a word separator: `" "` for '
                  'a script that spaces its words, `""` for one that writes nothing')
        elif not isinstance(data["separator"], str) or any(
                c in "\t\n\r" + OPEN + CLOSE for c in data["separator"]):
            fault(("separator",), "`separator` is a string: `\" \"`, the script's space glyph, or "
                  '`""` for a script that writes nothing')
    fonts = data.get("fonts")
    if not isinstance(fonts, list) or not fonts:
        fault(("fonts",) if "fonts" in data else (), "needs `fonts`, the slugs of the faces it serves")
        fonts = []
    else:
        for n, slug in enumerate(fonts):
            if not isinstance(slug, str) or not NAME.match(slug):
                fault(("fonts", n), "a font is its slug: lowercase letters, digits and `-`")
            elif slug in GENERIC_FAMILIES:
                fault(("fonts", n), f"`{slug}` is a generic family; `fonts` lists the faces drawn")
            elif fonts.index(slug) != n:
                fault(("fonts", n), f"`{slug}` is listed twice")
    extends = data.get("extends")
    if "extends" in data and (not isinstance(extends, str) or not NAME.match(extends)):
        fault(("extends",), "`extends` is the name of a base file beside the encoding")
    codage = data.get("codage")
    if "codage" in data and (not isinstance(codage, str) or not NAME.match(codage)):
        fault(("codage",), "`codage` is the name of an encoding beside this one")
    vowels = data.get("vowels", "")
    if not isinstance(vowels, str):
        fault(("vowels",), "`vowels` is a string of the characters `before` reads as vowels")
        vowels = ""
    if "rows" not in data:
        fault((), "needs `rows`")
    else:
        _rows_faults(data["rows"], ("rows",), fault, vowels,
                     allow_empty=data.get("roundTrip") == "canonical")
    faces = data.get("faces", {})
    if not isinstance(faces, dict):
        fault(("faces",), "`faces` maps a face's slug to its own rows")
    else:
        for slug, face in faces.items():
            if slug not in fonts:
                fault(("faces", slug), f"`{slug}` is not one of `fonts`", key=True)
            if not isinstance(face, dict):
                fault(("faces", slug), "a face is `{\"rows\": [...]}`")
                continue
            for key in face:
                if key not in FACE_KEYS:
                    fault(("faces", slug, key), f"`{key}` is not a face key; a face takes `rows`",
                          key=True)
            _rows_faults(face.get("rows", []), ("faces", slug, "rows"), fault, vowels,
                         allow_empty=data.get("roundTrip") == "canonical")
    return faults


def _read(path):
    """The text and data of a JSON file, or an ``EncodingError``."""
    try:
        with open(path, encoding="utf-8") as handle:
            text = handle.read()
    except OSError as error:
        raise EncodingError(error.strerror or str(error), path) from None
    try:
        data = json.loads(text)
    except json.JSONDecodeError as error:
        raise EncodingError(error.msg, path, error.lineno, error.colno) from None
    return text, data


def _raise(faults):
    first = faults[0]
    first.faults = faults
    raise first


_BASES = {}


def load_base(path):
    """Read a base file, which encodings extend. Raises ``EncodingError`` as ``load``."""
    path = os.path.abspath(path)
    if path not in _BASES:
        text, data = _read(path)
        faults = _check_base(data, text, path)
        if faults:
            _raise(faults)
        _BASES[path] = Base(data, path)
    return _BASES[path]


def load(name_or_path, _codage=False):
    """Read an encoding by its name in ``encodings/``, or from a file anywhere, with the
    base file it extends.

    Raises ``EncodingError`` for a file that does not exist, does not parse, or is
    not well formed; the first fault is raised, and its ``faults`` holds every one.
    """
    if isinstance(name_or_path, Encoding):
        return name_or_path
    given = str(name_or_path)
    if os.sep in given or "/" in given or given.endswith(".json"):
        path = given
    elif given == STANDARD:
        raise EncodingError(
            f"`{STANDARD}` is the standard roman encoding, which every encoding extends; "
            "it is not applied alone"
        )
    else:
        path = os.path.join(ENCODINGS, given + ".json")
        if not os.path.exists(path):
            known = ", ".join(names()) or "none"
            raise EncodingError(f"no encoding is named `{given}`; the encodings are {known}")
    text, data = _read(path)
    faults = _check(data, text, path)
    if faults:
        _raise(faults)
    if data.get("kind") == "codage" and not _codage:
        users = [n for n in names() if _stated_codage(n) == data["name"]]
        use = (f"; use `{users[0]}`, the encoding that states it" if len(users) == 1
               else f"; the encodings that state it are {', '.join(users)}" if users else "")
        raise EncodingError(
            f"`{data['name']}` is a codage, the notation of a script's literal spans: it is "
            f"reached only between `{OPEN}` and `{CLOSE}` of an encoding that states it, "
            f"and encodes no text of its own{use}",
            path,
        )
    base = None
    if "extends" in data:
        base_path = os.path.join(os.path.dirname(os.path.abspath(path)), data["extends"] + ".json")
        if not os.path.exists(base_path):
            _raise([_fault_at((path, ("extends",)),
                              f"`{data['extends']}` is not a base file beside the encoding")])
        base = load_base(base_path)
    codage = None
    if "codage" in data:
        codage_path = os.path.join(os.path.dirname(os.path.abspath(path)), data["codage"] + ".json")
        if not os.path.exists(codage_path) or data["codage"] in NOT_ENCODINGS \
                or _read(codage_path)[1].get("kind") != "codage":
            _raise([_fault_at((path, ("codage",)),
                              f"`{data['codage']}` is not a codage beside this encoding; "
                              'a codage is a file with `"kind": "codage"`')])
        codage = load(codage_path, _codage=True)
    enc = Encoding(data, path, base, codage)
    faults = _check_outputs(enc)
    if faults:
        _raise(faults)
    return enc


def _kind_of(path):
    """The ``kind`` a file states, read from its head without parsing it."""
    with open(path, encoding="utf-8") as handle:
        head = handle.read(400)
    found = re.search(r'"kind":\s*"(\w+)"', head)
    return found.group(1) if found else "encoding"


def _stated_codage(name):
    """The codage the encoding ``name`` states, or ``None``."""
    with open(os.path.join(ENCODINGS, name + ".json"), encoding="utf-8") as handle:
        head = handle.read(600)
    found = re.search(r'"codage":\s*"([a-z0-9-]+)"', head)
    return found.group(1) if found else None


def names(directory=None, kind="encoding"):
    """The name of every encoding in ``encodings/``, sorted; ``kind="codage"`` names the
    codages instead."""
    directory = directory or ENCODINGS
    if not os.path.isdir(directory):
        return []
    return sorted(
        f[:-5] for f in os.listdir(directory)
        if f.endswith(".json") and f[:-5] not in NOT_ENCODINGS
        and _kind_of(os.path.join(directory, f)) == kind
    )


def for_font(slug):
    """The encoding that serves a font: the one encoding listing it, or, for a font with
    no encoding, a names-only one that accepts nothing outside the literal markers.
    Several encodings serving one font is an ambiguity the caller resolves by name."""
    fonts_json = os.path.join(HERE, "fonts.json")
    if os.path.exists(fonts_json):
        with open(fonts_json, encoding="utf-8") as handle:
            known = {f["class"][3:] for f in json.load(handle)["families"] if f["class"].startswith("hl-")}
        if slug not in known:
            raise EncodingError(f"no font is named `{slug}`")
    serving = []
    for name in names():
        with open(os.path.join(ENCODINGS, name + ".json"), encoding="utf-8") as handle:
            if slug in json.load(handle).get("fonts", []):
                serving.append(name)
    if len(serving) > 1:
        raise EncodingError(f"the font `{slug}` is served by {', '.join(serving)}; name one with --encoding")
    return load(serving[0]) if serving else Encoding.names_only(slug)


# --- applying it -------------------------------------------------------------------


_LOADED = {}


def _resolve(enc):
    """An encoding given as itself, or by a name or path, read once."""
    if isinstance(enc, Encoding):
        return enc
    if enc not in _LOADED:
        _LOADED[enc] = load(enc)
    return _LOADED[enc]


def _boundary(char):
    return char.isspace() or unicodedata.category(char)[0] in "PS"


def _holds(row, text, start, end, vowels):
    if row.before:
        if end >= len(text):
            return False
        char = text[end]
        vowel = char in vowels
        if row.before == "vowel":
            if not vowel:
                return False
        elif vowel or not unicodedata.category(char).startswith("L"):
            return False
    if row.at == "line-start":
        prefix = text[max(text.rfind("\n", 0, start), text.rfind("/", 0, start)) + 1:start]
        if prefix.strip("^"):
            return False
    if row.at == "start" and start > 0 and not _boundary(text[start - 1]):
        return False
    if row.at == "end" and end < len(text) and not _boundary(text[end]):
        return False
    return True


def _row_at(enc, tiers, text, at):
    for face in tiers:
        for row in face.by_first.get(text[at], ()):
            end = at + len(row.source)
            if text.startswith(row.source, at) and _holds(row, text, at, end, enc.vowels):
                return row
    return None


def _refused(enc, text, at, source, known, what):
    """The error for a character at ``at`` that nothing reads there."""
    char = text[at]
    line, column = _line_column(text, at)
    shown = f"{json.dumps(char, ensure_ascii=False)} (U+{ord(char):04X})"
    noun = "codage" if enc.kind == "codage" else "encoding"
    if known:
        message = f"no row of the `{enc.name}` {noun} {what} {shown} here"
    elif what == "matches":
        message = f"{shown} is not in the `{enc.name}` {noun}"
    else:
        message = f"{shown} is written by no row of the `{enc.name}` {noun}"
    return EncodingError(message, source or TEXT, line, column)


def _error_at(message, text, at, source):
    line, column = _line_column(text, at)
    return EncodingError(message, source or TEXT, line, column)


def _span(text, at, opener, closer, source, what):
    """The offset of the ``closer`` that ends the span ``opener`` begins at ``at``. An
    unmatched opener and a nested one are refused."""
    start = at + len(opener)
    if opener == "\U000E0112":
        cursor = start
        while cursor < len(text):
            # Generic spelling metadata spells hex inside its own brackets.
            # Digits in that metadata are not literal-span boundaries.
            if text[cursor] == "\U000E015B":
                end = text.find("\U000E015D", cursor + 1)
                if end >= 0:
                    cursor = end + 1
                    continue
            if text.startswith(closer, cursor):
                return cursor
            if text.startswith(opener, cursor):
                raise _error_at(f"{what} opens a literal span inside another", text, cursor, source)
            cursor += 1
        raise _error_at(f"{what} opens a literal span that nothing closes", text, at, source)
    close = text.find(closer, start)
    if close < 0:
        raise _error_at(f"{what} opens a literal span that nothing closes", text, at, source)
    nested = text.find(opener, start, close)
    if nested >= 0:
        raise _error_at(f"{what} opens a literal span inside another", text, nested, source)
    return close


_CHARACTERS = {}


def _character_names():
    """The names of the script fonts' characters, ``(name by character, character by
    name)``, from ``encodings/names.json``."""
    if not _CHARACTERS:
        path = os.path.join(ENCODINGS, NAMES + ".json")
        try:
            with open(path, encoding="utf-8") as handle:
                table = json.load(handle)
        except OSError as error:
            raise EncodingError(error.strerror or str(error), path) from None
        by_char = {chr(int(point[2:], 16)): name for point, name in table.items()}
        _CHARACTERS["name"] = by_char
        _CHARACTERS["char"] = {name.replace(" ", "_"): char for char, name in by_char.items()}
    return _CHARACTERS["name"], _CHARACTERS["char"]


def character_name(char):
    """A character's code: its name with spaces written ``_``, or ``None`` when it has none."""
    names, _ = _character_names()
    if char in names:
        return names[char].replace(" ", "_")
    try:
        return unicodedata.name(char).replace(" ", "_")
    except ValueError:
        return None


def character_named(code):
    """The character a code names, or ``None``."""
    _, chars = _character_names()
    if code in chars:
        return chars[code]
    try:
        char = unicodedata.lookup(code.replace("_", " "))
    except KeyError:
        return None
    return char if len(char) == 1 and character_name(char) == code else None


def _name_pieces(text, start, end, strict, source):
    """The pieces of a span of character names: each code is ``(code, character, row)``
    and the space between codes writes nothing."""
    out = []
    at = start
    for found in re.finditer(r"\S+", text[start:end]):
        begin = start + found.start()
        if begin > at:
            gap = text[at:begin]
            out.append((gap, "", Row(gap, "")))
        code = found.group()
        char = character_named(code)
        if char is None:
            if strict:
                odd = next((i for i, c in enumerate(code) if not (c.isalnum() or c in "_-")), 0)
                raise _error_at(f"`{code}` is not the name of a character", text, begin + odd, source)
            out.append((code, code, None))
        else:
            out.append((code, char, Row(code, char)))
        at = begin + len(code)
    if at < end:
        gap = text[at:end]
        out.append((gap, "", Row(gap, "")))
    return out


def _decode_names(text, start, end, source):
    """The codes of the characters between ``start`` and ``end``, one space apart."""
    codes = []
    for at in range(start, end):
        code = character_name(text[at])
        if code is None:
            char = text[at]
            raise _error_at(f"{json.dumps(char, ensure_ascii=False)} (U+{ord(char):04X}) has no "
                            "name", text, at, source)
        codes.append(code)
    return " ".join(codes)


def _inside(error, text, start, source):
    """An error found in the span's own text, placed at its position in the whole text."""
    if error.line is None:
        return error
    inner = text[start:].splitlines(True)
    offset = start + sum(len(line) for line in inner[: error.line - 1]) + error.column - 1
    return _error_at(error.message, text, offset, source)


def _codage_pieces(codage, text, start, end, strict, source):
    """The pieces of a span of a codage's codes. Whitespace only separates codes, so each
    run of non-whitespace is encoded by the codage on its own and the whitespace between
    runs writes nothing. Only the codage's own codes and notation are allowed: a standard
    mark inside the span is refused at its position."""
    out = []
    at = start
    for found in re.finditer(r"\S+", text[start:end]):
        begin = start + found.start()
        if begin > at:
            gap = text[at:begin]
            out.append((gap, "", Row(gap, "")))
        try:
            out += pieces(codage, found.group(), None, strict)
        except EncodingError as error:
            raise _inside(error, text, begin, source) from None
        at = begin + len(found.group())
    if at < end:
        gap = text[at:end]
        out.append((gap, "", Row(gap, "")))
    return out


def pieces(enc, text, face=None, strict=True, source=None, verse=False):
    """The text as encoded, piece by piece: ``(from, to, row)`` for each matched row.

    A character no row matches is refused with an ``EncodingError`` at its line and
    column, ``source`` naming the text (``<text>`` when it is ``None``). With ``strict``
    false it is kept instead, as ``(char, char, None)``, for a tool that sets such a
    character in a font to see what the font draws for it."""
    enc = _resolve(enc)
    tiers = enc.tiers(face)
    out = []
    at = 0
    while at < len(text):
        if text[at] == OPEN:
            close = _span(text, at, OPEN, CLOSE, source, f"`{OPEN}`")
            out.append((OPEN, _OPEN_ROW.target, _OPEN_ROW))
            if enc.codage is None:
                out += _name_pieces(text, at + 1, close, strict, source)
            else:
                out += _codage_pieces(enc.codage, text, at + 1, close, strict, source)
            out.append((CLOSE, _CLOSE_ROW.target, _CLOSE_ROW))
            at = close + 1
            continue
        if text[at] == CLOSE:
            raise _error_at(f"`{CLOSE}` closes no literal span", text, at, source)
        if "verseCanto" in enc.controls and text.startswith("--- {.canto}", at):
            line_start = text.rfind("\n", 0, at) + 1
            if not text[line_start:at].strip():
                token = "--- {.canto}"
                out.append((token, enc.controls["verseCanto"], Row(token, enc.controls["verseCanto"])))
                at += len(token)
                if verse:
                    if text.startswith("\r\n", at):
                        at += 2
                    elif at < len(text) and text[at] in "\r\n":
                        at += 1
                continue
        if verse and text[at] in "\r\n" and "verseStanza" in enc.controls:
            end = at
            while end < len(text) and text[end] in " \t\r\n":
                end += 1
            run = text[at:end].replace("\r\n", "\n").replace("\r", "\n")
            if text.startswith("--- {.canto}", end):
                at = end
                continue
            row = (_row_at(enc, tiers, "/", 0) if run.count("\n") == 1 else
                   Row("\n\n", enc.controls["verseStanza"]))
            out.append((text[at:end], row.target, row))
            at = end
            continue
        if text[at] in WHITESPACE and enc.separator is not None:
            end = at + 1
            while end < len(text) and text[end] in WHITESPACE:
                end += 1
            following = _row_at(enc, tiers, text, end) if end < len(text) else None
            if ("\n" in text[at:end] or "\r" in text[at:end]) and following is not None and following.at == "line-start":
                line = _row_at(enc, tiers, "/", 0)
                out.append((text[at:end], line.target, line))
            else:
                out.append((text[at:end], enc.separator, enc.separator_row))
            at = end
            continue
        if enc.group_case == "initial":
            invalid = next((text[at:at + len(r.source)]
                            for tier in tiers for r in tier.rows
                            if len(r.source) > 1 and r.source.isalpha()
                            and text[at:at + len(r.source)].lower() == r.source.lower()
                            and text[at:at + len(r.source)] not in
                            (r.source.lower(), r.source.lower().capitalize())), None)
            if invalid is not None:
                if strict:
                    lower = invalid.lower()
                    raise _error_at(
                        f"`{invalid}` is an illegal group spelling; use `{lower}` or "
                        f"`{lower.capitalize()}`", text, at, source)
                out.append((invalid, invalid, None))
                at += len(invalid)
                continue
        row = _row_at(enc, tiers, text, at) if text[at] in enc.accepted else None
        if row is not None:
            out.append((row.source, row.target, row))
            at += len(row.source)
        elif strict:
            if enc.font_only:
                raise _error_at(
                    f"{json.dumps(text[at], ensure_ascii=False)} (U+{ord(text[at]):04X}) is outside "
                    f"`{OPEN}` and `{CLOSE}`; the `{enc.name}` font has no encoding, so its text is "
                    "written only as character names between them",
                    text, at, source,
                )
            known = text[at] in enc.accepted and any(text[at] in tier.by_first for tier in tiers)
            raise _refused(enc, text, at, source, known, "matches")
        else:
            out.append((text[at], text[at], None))
            at += 1
    return out


def encode(enc, text, face=None, source=None, verse=False):
    """Roman text written in the encoding's code points. A character no row matches is
    refused with an ``EncodingError`` at its line and column."""
    return "".join(to for _, to, _ in pieces(enc, text, face, source=source, verse=verse))


_SEPARATORS = re.compile("[" + WHITESPACE + "]+|" + OPEN + "[^" + CLOSE + "]*" + CLOSE)


def canonical(enc, text):
    """The roman a text reads back as: each run of whitespace outside the literal markers
    becomes one space, or nothing for a script whose separator writes nothing."""
    enc = _resolve(enc)
    if enc.round_trip == "canonical":
        return decode(enc, encode(enc, text))
    space = "" if enc.separator == "" else " "
    def separator(match):
        if match.group()[0] not in WHITESPACE:
            return match.group()
        following = _row_at(enc, enc.tiers(None), text, match.end()) if match.end() < len(text) else None
        if ("\n" in match.group() or "\r" in match.group()) and following is not None and following.at == "line-start":
            return "/"
        return space
    return _SEPARATORS.sub(separator, text)


def _wordy(char):
    return char.isalnum() or char == "_"


def _join_codes(sources):
    """A codage's codes written one space apart where two codes meet, and run together
    where notation joins them: whitespace in a span only separates codes, so decoding
    always writes the single space."""
    out = ""
    for piece in sources:
        if out and _wordy(out[-1]) and _wordy(piece[0]):
            out += " "
        out += piece
    return out


def _read_rows(enc, text, face, source=None):
    """The ``from`` of each row a text of code points reads as, by plain longest match."""
    readings = enc.tiers(face)[0].readings
    out = []
    at = 0
    while at < len(text):
        for target, source_text in readings.get(text[at], ()):
            if text.startswith(target, at):
                out.append(source_text)
                at += len(target)
                break
        else:
            raise _refused(enc, text, at, source, text[at] in readings, "writes")
    return out


def decode(enc, text, face=None, source=None):
    """Code points read back as roman text, by plain longest match: at each point the
    longest ``to`` the code points continue with is read as its row's ``from``. A code
    point that begins no ``to`` there is refused with an ``EncodingError`` at its line and
    column."""
    enc = _resolve(enc)
    readings = enc.tiers(face)[0].readings
    out = []
    at = 0
    while at < len(text):
        if text.startswith(_OPEN_ROW.target, at):
            close = _span(text, at, _OPEN_ROW.target, _CLOSE_ROW.target, source,
                          "the mark of `\u27e6`")
            start = at + len(_OPEN_ROW.target)
            if enc.codage is None:
                inner = _decode_names(text, start, close, source)
            else:
                try:
                    inner = _join_codes(_read_rows(enc.codage, text[start:close], None))
                except EncodingError as error:
                    raise _inside(error, text, start, source) from None
            out.append(OPEN + inner + CLOSE)
            at = close + len(_CLOSE_ROW.target)
            continue
        if text.startswith(_CLOSE_ROW.target, at):
            raise _error_at("the mark of `\u27e7` closes no literal span", text, at, source)
        for target, source_text in readings.get(text[at], ()):
            if text.startswith(target, at):
                out.append(source_text)
                at += len(target)
                break
        else:
            known = text[at] in readings
            raise _refused(enc, text, at, source, known, "writes")
    return "".join(out)


# --- non-writing marks -------------------------------------------------------------

# Variation selectors VS17 to VS256: invisible and default-ignorable, and, unlike the
# tag characters, skipped by OpenType substitutions, so a mark between two glyphs leaves
# their ligatures and contextual forms as they are.
MARK_BASE = 0xE0100
END_MARK = "\U000E01EF"


def is_mark(char):
    """Whether a character is one of the non-writing characters a mark is made of."""
    return 0xE0100 <= ord(char) <= 0xE01EF


def mark(source):
    """The non-writing characters that stand for ``source``.

    Each character of ``source`` is spelled as itself when it is printable ASCII other
    than ``{``, and otherwise as ``{``, its code point in lowercase hex, and ``}``. A
    spelled character ``c`` is written as variation selector U+E0100 + (``c`` - U+0020):
    ``a`` is U+E0141, and ``á``, spelled ``{e1}``, is U+E015B U+E0145 U+E0111 U+E015D.
    """
    if source in _STANDARD_MARKS:
        return _STANDARD_MARKS[source]
    # Low selectors are reserved for punctuation and structural controls.
    # Generic spelling metadata starts with a braced code-point spelling when
    # its old ASCII form would be mistaken for one of those controls.
    force_hex = bool(source and " " <= source[0] <= "4")
    out = []
    for char in source:
        spelled = char if not force_hex and " " <= char <= "~" and char != "{" else "{%x}" % ord(char)
        out.extend(chr(MARK_BASE + ord(c) - 0x20) for c in spelled)
    return "".join(out)


# Read explicit punctuation assignments from the shared standard.
with open(os.path.join(ENCODINGS, "standard.json"), encoding="utf-8") as _standard_file:
    _standard_data = json.load(_standard_file)
_STANDARD_MARKS = {(r[0] if isinstance(r, list) else r["from"]):
                   (r[1] if isinstance(r, list) else r["to"])
                   for r in _standard_data["rows"]}
_STANDARD_MARKS[OPEN] = _standard_data.get("controls", {}).get("literalOpen", "\U000E0112")
_STANDARD_MARKS[CLOSE] = _standard_data.get("controls", {}).get("literalClose", "\U000E0113")

# Literal markers use the shared structural assignments.
_OPEN_ROW = Row(OPEN, mark(OPEN))
_CLOSE_ROW = Row(CLOSE, mark(CLOSE))


def is_run(drawing, drawings):
    """Whether a drawing is a run of two or more of ``drawings``, the drawings of other
    rows, one after another."""
    ends = {0: 0}
    for start in range(len(drawing)):
        if start not in ends:
            continue
        for end in range(start + 1, len(drawing) + 1):
            piece = drawing[start:end]
            if piece in drawings and piece != drawing:
                count = ends[start] + 1
                ends[end] = max(ends.get(end, 0), count)
    return ends.get(len(drawing), 0) >= 2


# --- writing an encoding file ------------------------------------------------------


def _escape_marks(text):
    """JSON text with each non-writing character written as its ``\\u`` escape."""
    out = []
    for char in text:
        if is_mark(char):
            low = ord(char) - 0x10000
            out.append("\\u%04X\\u%04X" % (0xD800 + (low >> 10), 0xDC00 + (low & 0x3FF)))
        else:
            out.append(char)
    return "".join(out)


def dumps(data):
    """An encoding as its file is laid out: one row to a line, characters as written
    except the non-writing ones, which are escaped so that they show."""
    def one(value):
        return _escape_marks(json.dumps(value, ensure_ascii=False))

    lines = ["{"]
    keys = [k for k in TOP_KEYS if k in data]
    for n, key in enumerate(keys):
        comma = "," if n < len(keys) - 1 else ""
        value = data[key]
        if key == "rows" and value:
            lines.append(f"    {one(key)}: [")
            lines += [f"        {one(r)}," for r in value[:-1]] + [f"        {one(r)}" for r in value[-1:]]
            lines.append(f"    ]{comma}")
        elif key == "faces":
            lines.append(f"    {one(key)}: {{")
            slugs = list(value)
            for m, slug in enumerate(slugs):
                rows = value[slug].get("rows", [])
                lines.append(f"        {one(slug)}: {{")
                lines.append('            "rows": [')
                lines += [f"                {one(r)}," for r in rows[:-1]]
                lines += [f"                {one(r)}" for r in rows[-1:]]
                lines.append("            ]")
                lines.append("        }" + ("," if m < len(slugs) - 1 else ""))
            lines.append(f"    }}{comma}")
        else:
            lines.append(f"    {one(key)}: {one(value)}{comma}")
    lines.append("}")
    return "\n".join(lines) + "\n"


# --- the command -------------------------------------------------------------------


class _Parser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write(f"encode.py: error: {message}\n")
        sys.exit(2)


def main(argv=None):
    parser = _Parser(
        prog="encode.py",
        description="Write roman text in a script font's code points by an encoding, or read it back.",
    )
    parser.add_argument("--encoding", help="an encoding's name, or the path of an encoding file")
    parser.add_argument("--font", help="a font's slug: its encoding, or, for a font with none, "
                        "the names-only encoding that accepts text only between the literal markers")
    parser.add_argument("--decode", action="store_true", help="read code points back as roman")
    parser.add_argument("--face", help="the face the text is set in, whose own rows apply")
    parser.add_argument("--codepoints", action="store_true", help="print the result as U+XXXX values")
    parser.add_argument("--list", action="store_true", help="name the encodings and stop")
    parser.add_argument("--file", help="read the text from this file")
    parser.add_argument("--verse", action="store_true", help="encode verse line and stanza boundaries")
    parser.add_argument("text", nargs="?", help="the text; standard input when absent or `-`")
    args = parser.parse_args(argv)
    try:
        if args.list:
            for name in names():
                print(name)
            return 0
        if bool(args.encoding) == bool(args.font):
            parser.error("give --encoding or --font, one of them")
        enc = load(args.encoding) if args.encoding else for_font(args.font)
        if args.file is not None:
            if args.text is not None:
                parser.error("give the text or --file, not both")
            try:
                with open(args.file, encoding="utf-8") as handle:
                    text = handle.read()
            except OSError as error:
                raise EncodingError(error.strerror or str(error), args.file) from None
            source, end = args.file, ""
        elif args.text is None or args.text == "-":
            text = sys.stdin.read()
            source, end = "<stdin>", ""
        else:
            text = args.text
            source, end = TEXT, "\n"
        result = (decode(enc, text, args.face, source) if args.decode else
                  encode(enc, text, args.face, source, verse=args.verse))
    except EncodingError as error:
        for fault in error.faults:
            sys.stderr.write(f"{fault}\n")
        return 1
    if args.codepoints:
        sys.stdout.write(" ".join(f"U+{ord(c):04X}" for c in result) + "\n")
    else:
        sys.stdout.write(result + end)
    return 0


if __name__ == "__main__":
    sys.exit(main())
