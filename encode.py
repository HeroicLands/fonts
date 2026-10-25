# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Write roman text in a script font's code points by an encoding, and read it back.

    python3 encode.py --encoding pirzath "Zaron tholmeza"
    python3 encode.py --encoding pirzath --decode "<the code points>"
    python3 encode.py --encoding encodings/pirzath.json --face pirzath-hand --codepoints -
    python3 encode.py --list

An encoding is one JSON file, ``encodings/<name>.json``:

    {
        "name": "pirzath",
        "fonts": ["pirzath-carved", "pirzath-hand"],
        "vowels": "aeiouAEIOU",
        "rows": [
            ["a", "\\uDB80\\uDE30"],
            ["A", "\\uDB80\\uDE30\\uDB40\\uDD21\\uDB40\\uDDEF"],
            ["-", "\\uDB40\\uDD0D"],
            {"from": "y", "to": "\\uDB80\\uDE37", "before": "consonant"}
        ],
        "faces": {"pirzath-hand": {"rows": [["a", "\\uDB80\\uDE31"]]}}
    }

``name``, ``fonts`` and ``rows`` are required; the rest are optional. ``fonts`` lists
the slugs of the faces the encoding serves.

Every encoding round-trips exactly, both ways: decoding an encoded roman text gives it
back, and encoding decoded code points gives them back. So no row writes nothing, and
no two rows with different ``from`` write one output. Where a script does not write a
character, or draws two alike, the row says so with a mark of non-writing characters:

- A mark spells a ``from`` in variation selectors VS17 to VS111, U+E0100 to
  U+E015E, which are invisible and default-ignorable: printable ASCII character ``c`` is
  U+E0100 + (``c`` - U+0020), so ``-`` is U+E010D and ``a`` U+E0141. Each character of
  ``from`` is spelled as itself when it is printable ASCII other than ``{``, and
  otherwise as ``{``, its code point in lowercase hex, and ``}``: ``á`` is spelled
  ``{e1}``. ``mark`` writes one.
- A row that draws nothing (a vowel in an abjad, an inherent vowel, a quadrat or word
  separator) writes the mark of its ``from``: ``-`` writes U+E010D.
- A row writes its drawing, the mark of its ``from`` and the end mark, VS256 U+E01EF,
  when an earlier row with another ``from`` draws the same, when its drawing is a run of
  two or more other rows' drawings, or when it draws whitespace that no row reads and so
  passes through. After ``a``, ``A`` writes the glyph of ``a``, U+E0121 and U+E01EF;
  ``cch``, drawn as ``ch`` twice, writes the two glyphs, its mark and the end mark.
  The first row in authored order to draw a drawing keeps it bare, and so does any
  later row with the same ``from``. ``is_run`` tells a run.

The marks are written into the rows; reading a file applies no rule of its own. The
files write the non-writing characters as ``\\u`` escapes, so that they show.

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
- A character no row matches passes through unchanged.

Decoding reads the rows backward, by plain longest match: at each point the longest
``to`` that the code points continue with is read as its row's ``from``, and a
character that begins no ``to`` passes through as itself. Text set in a face reads its
face's rows and the shared rows together.

Errors are reported as ``file:line:column: error: message`` and exit non-zero.
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
CONDITIONS = {"before": ("vowel", "consonant"), "at": ("start", "end")}
GENERIC_FAMILIES = ("mono", "serif", "sans")
TOP_KEYS = ("name", "fonts", "vowels", "rows", "faces")
# Keys an encoding does not take, with why.
REFUSED_KEYS = {
    "decode": "decoding reads every output back as its own row's `from`",
    "separators": "a row that draws nothing writes its mark, so decoding restores it",
}
ROW_KEYS = ("from", "to", "before", "at")
FACE_KEYS = ("rows",)
# Not encodings, though they sit in encodings/.
NOT_ENCODINGS = ("vectors",)


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
    """One row: what it matches, what it writes, and its conditions."""

    __slots__ = ("source", "target", "before", "at", "order")

    def __init__(self, source, target, before=None, at=None, order=0):
        self.source = source
        self.target = target
        self.before = before
        self.at = at
        self.order = order

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
        table.setdefault(row.target, row.source)
    by_first = {}
    for target, source in table.items():
        by_first.setdefault(target[0], []).append((target, source))
    for group in by_first.values():
        group.sort(key=lambda pair: -len(pair[0]))
    return by_first


class Face:
    __slots__ = ("rows", "by_first", "readings")

    def __init__(self, rows, shared=()):
        self.rows = rows
        self.by_first = _index_rows(rows)
        self.readings = _readings(list(rows) + list(shared))


class Encoding:
    """An encoding, read from its file and ready to apply."""

    def __init__(self, data, path):
        self.path = path
        self.name = data["name"]
        self.fonts = list(data["fonts"])
        self.vowels = frozenset(data.get("vowels", ""))
        self.rows = [_read_row(row, n) for n, row in enumerate(data["rows"])]
        self.shared = Face(self.rows)
        self.faces = {}
        for slug, face in data.get("faces", {}).items():
            rows = [_read_row(row, n) for n, row in enumerate(face.get("rows", []))]
            self.faces[slug] = Face(rows, self.rows)

    def tiers(self, face):
        if face is not None and face not in self.fonts:
            raise EncodingError(
                f"`{self.name}` serves {', '.join(self.fonts)}, not `{face}`", self.path
            )
        own = self.faces.get(face) if face is not None else None
        return [own, self.shared] if own else [self.shared]

    def __repr__(self):
        return f"Encoding({self.name!r})"


def _read_row(row, order):
    if isinstance(row, list):
        return Row(row[0], row[1], order=order)
    return Row(row["from"], row["to"], row.get("before"), row.get("at"), order)


NOTHING = (
    "writes nothing; a row that draws nothing writes the mark of its `from`, "
    "so that decoding restores it"
)


def _check_outputs(data, fault):
    """No two rows with different ``from`` write one output, among the shared rows or
    among a face's rows and the shared rows."""

    def rows_of(rows, at):
        out = []
        for n, row in enumerate(rows):
            source, target = (row[0], row[1]) if isinstance(row, list) else (row["from"], row["to"])
            out.append((source, target, at + (n,)))
        return out

    shared = rows_of(data["rows"], ("rows",))
    tiers = [shared] + [
        shared + rows_of(face.get("rows", []), ("faces", slug, "rows"))
        for slug, face in data.get("faces", {}).items()
    ]
    reported = set()
    for tier in tiers:
        readers = {}
        for source, target, at in tier:
            first = readers.setdefault(target, (source, at))
            if first[0] != source and at not in reported:
                reported.add(at)
                fault(
                    at,
                    f"writes what the row at {'.'.join(map(str, first[1]))} writes, for "
                    f"{json.dumps(first[0], ensure_ascii=False)}; a row that draws what an "
                    "earlier row draws adds the mark of its `from` and the end mark",
                )


def _check(data, text, path):
    """Every structural fault in an encoding file, each at its position."""
    where, duplicates = _positions(text)
    faults = []

    def fault(at, message, key=False):
        offset = where.get((at, "key") if key else at)
        if offset is None:
            faults.append(EncodingError(message, path))
        else:
            faults.append(EncodingError(message, path, *_line_column(text, offset)))

    for at, _ in duplicates:
        fault(at, f"`{'.'.join(map(str, at))}` is stated twice", key=True)
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
    name = data.get("name")
    stem = os.path.splitext(os.path.basename(path))[0]
    if not isinstance(name, str) or not NAME.match(name):
        fault(("name",) if "name" in data else (), "needs `name`: lowercase letters, digits and `-`")
    elif name != stem:
        fault(("name",), f"`name` is `{name}`, and the file is `{stem}.json`; they are the same")
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
    vowels = data.get("vowels", "")
    if not isinstance(vowels, str):
        fault(("vowels",), "`vowels` is a string of the characters `before` reads as vowels")
        vowels = ""

    def rows_at(rows, at):
        if not isinstance(rows, list):
            fault(at, "`rows` is a list of rows")
            return
        for n, row in enumerate(rows):
            here = at + (n,)
            if isinstance(row, list):
                if len(row) != 2 or not all(isinstance(s, str) for s in row):
                    fault(here, "a row written as a list is two strings, `[from, to]`")
                elif row[0] == "":
                    fault(here, "has an empty `from`; a row matches one or more characters")
                elif row[1] == "":
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
            if not isinstance(row.get("from"), str) or row.get("from") == "":
                fault(here + ("from",) if "from" in row else here,
                      "needs `from`, the one or more characters the row matches")
            if not isinstance(row.get("to"), str):
                fault(here + ("to",) if "to" in row else here,
                      "needs `to`, the one or more characters the row writes")
            elif row["to"] == "":
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

    if "rows" not in data:
        fault((), "needs `rows`")
    else:
        rows_at(data["rows"], ("rows",))
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
            rows_at(face.get("rows", []), ("faces", slug, "rows"))
    if not faults:
        _check_outputs(data, fault)
    return faults


def load(name_or_path):
    """Read an encoding by its name in ``encodings/``, or from a file anywhere.

    Raises ``EncodingError`` for a file that does not exist, does not parse, or is
    not well formed; the first fault is raised, and its ``faults`` holds every one.
    """
    if isinstance(name_or_path, Encoding):
        return name_or_path
    given = str(name_or_path)
    if os.sep in given or "/" in given or given.endswith(".json"):
        path = given
    else:
        path = os.path.join(ENCODINGS, given + ".json")
        if not os.path.exists(path):
            known = ", ".join(names()) or "none"
            raise EncodingError(f"no encoding is named `{given}`; the encodings are {known}")
    try:
        with open(path, encoding="utf-8") as handle:
            text = handle.read()
    except OSError as error:
        raise EncodingError(error.strerror or str(error), path) from None
    try:
        data = json.loads(text)
    except json.JSONDecodeError as error:
        raise EncodingError(error.msg, path, error.lineno, error.colno) from None
    faults = _check(data, text, path)
    if faults:
        first = faults[0]
        first.faults = faults
        raise first
    return Encoding(data, path)


def names():
    """The name of every encoding in ``encodings/``, sorted."""
    if not os.path.isdir(ENCODINGS):
        return []
    return sorted(
        f[:-5] for f in os.listdir(ENCODINGS)
        if f.endswith(".json") and f[:-5] not in NOT_ENCODINGS
    )


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


def pieces(enc, text, face=None):
    """The text as encoded, piece by piece: ``(from, to, row)`` for each matched row,
    and ``(char, char, None)`` for each character that passed through."""
    enc = _resolve(enc)
    tiers = enc.tiers(face)
    out = []
    at = 0
    while at < len(text):
        row = _row_at(enc, tiers, text, at)
        if row is not None:
            out.append((row.source, row.target, row))
            at += len(row.source)
        else:
            out.append((text[at], text[at], None))
            at += 1
    return out


def encode(enc, text, face=None):
    """Roman text written in the encoding's code points."""
    return "".join(to for _, to, _ in pieces(enc, text, face))


def decode(enc, text, face=None):
    """Code points read back as roman text, by plain longest match: at each point the
    longest ``to`` the code points continue with is read as its row's ``from``, and a
    character that begins no ``to`` passes through as itself."""
    enc = _resolve(enc)
    readings = enc.tiers(face)[0].readings
    out = []
    at = 0
    while at < len(text):
        for target, source in readings.get(text[at], ()):
            if text.startswith(target, at):
                out.append(source)
                at += len(target)
                break
        else:
            out.append(text[at])
            at += 1
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
    out = []
    for char in source:
        spelled = char if " " <= char <= "~" and char != "{" else "{%x}" % ord(char)
        out.extend(chr(MARK_BASE + ord(c) - 0x20) for c in spelled)
    return "".join(out)


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
    parser.add_argument("--decode", action="store_true", help="read code points back as roman")
    parser.add_argument("--face", help="the face the text is set in, whose own rows apply")
    parser.add_argument("--codepoints", action="store_true", help="print the result as U+XXXX values")
    parser.add_argument("--list", action="store_true", help="name the encodings and stop")
    parser.add_argument("text", nargs="?", help="the text; standard input when absent or `-`")
    args = parser.parse_args(argv)
    try:
        if args.list:
            for name in names():
                print(name)
            return 0
        if not args.encoding:
            parser.error("--encoding is required")
        enc = load(args.encoding)
        if args.text is None or args.text == "-":
            text = sys.stdin.read()
            end = ""
        else:
            text = args.text
            end = "\n"
        result = (decode if args.decode else encode)(enc, text, args.face)
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
