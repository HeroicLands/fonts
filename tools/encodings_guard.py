# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Check that every encoding is well formed, serves real faces and round-trips exactly.

    python3 tools/encodings_guard.py [--encodings DIR] [--fonts fonts.json] [--require-fonts]

Every encoding round-trips both ways: decoding an encoded roman text gives the text
back, and encoding decoded code points gives the code points back. For every encoding
file in ``encodings/`` it checks that

- the file is well formed, and every font it lists is a face in ``fonts.json``;
- no row writes nothing, and no two rows with different ``from`` write one output;
- every row's output follows the mark rule: a row that draws nothing writes the mark of
  its ``from``, and a row writes its drawing, the mark of its ``from`` and the end mark
  when an earlier row with another ``from`` draws the same, when its drawing is a run
  of two or more other rows' drawings, or when it draws whitespace that no row reads
  and so passes through (``encode.mark`` spells a mark, and ``encode.is_run`` tells a
  run);
- every row round-trips in the shortest text found in which it applies (see
  ``tools/encoding_vectors.py``), and so does every row beside every row that draws
  nothing, before it and after it;
- seeded random roman texts over the encoding's ``from`` alphabet round-trip, and so do
  random sequences of outputs, wherever encoding their ``from``s applies those rows;
- every sample text round-trips, and encoding the encoded text again leaves it unchanged;
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
import sys

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
        """A finding at a path in the encoding's file."""
        line = column = None
        if enc.path not in self.files:
            with open(enc.path, encoding="utf-8") as handle:
                text = handle.read()
            self.files[enc.path] = (text, E._positions(text)[0])
        text, offsets = self.files[enc.path]
        offset = offsets.get(where)
        if offset is not None:
            line, column = E._line_column(text, offset)
        self.findings.append(str(E.EncodingError(message, enc.path, line, column)))


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


def passes_through(enc, text):
    """Whether text is whitespace that no row's ``from`` begins with, which a roman text
    writes by passing it through."""
    firsts = {r.source[0] for r in enc.rows} | {
        r.source[0] for f in enc.faces.values() for r in f.rows
    }
    return text != "" and all(c.isspace() and c not in firsts for c in text)


# --- what the rows write -------------------------------------------------------------


def check_outputs(report, enc):
    """No row writes nothing, no output reads back as two romans, and every output
    follows the mark rule."""
    for face, at, rows in row_lists(enc):
        firsts = {}
        pool = rows + (enc.rows if face is not None else [])
        drawings = {drawing(r.target) for r in pool} - {""}
        for row in rows:
            where = at + (row.order,)
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
                if (first == row.source and not passes_through(enc, drawn)
                        and not E.is_run(drawn, drawings)):
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
                at = ("rows",) if face is None or row in enc.rows else ("faces", face, "rows")
                report.add(
                    enc,
                    at + (row.order,),
                    f"row {_show(row.source)} writes {_codepoints(row.target)}, which row "
                    f"{_show(other.source)} also writes, so decoding cannot tell them apart",
                )


# --- round trips -----------------------------------------------------------------------


def round_trip(report, enc, where, label, roman, face=None):
    """Whether ``roman`` reads back exactly, and its code points encode back exactly."""
    unicode = E.encode(enc, roman, face)
    read = E.decode(enc, unicode, face)
    ok = True
    if read != roman:
        report.add(
            enc,
            where,
            f"{label} {_show(roman)} encodes to {_codepoints(unicode)}, which reads back as "
            f"{_show(read)}",
        )
        ok = False
    again = E.encode(enc, read, face)
    if again != unicode:
        report.add(
            enc,
            where,
            f"{label} {_show(roman)} encodes to {_codepoints(unicode)}, which reads back as "
            f"{_show(read)}, which encodes to {_codepoints(again)}",
        )
        ok = False
    twice = E.encode(enc, unicode, face)
    if twice != unicode:
        report.add(
            enc,
            where,
            f"{label} {_show(roman)} encodes to {_codepoints(unicode)}, and encoding that "
            f"again gives {_codepoints(twice)}",
        )
        ok = False
    return ok


def check_rows(report, enc):
    """Every row round-trips where it applies, alone and beside a row that draws nothing."""
    for face, at, rows in row_lists(enc):
        silent = sorted({r.source for r in rows if r.target and drawing(r.target) == ""})
        for row in rows:
            where = at + (row.order,)
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
                    if not round_trip(report, enc, where, "the row beside a silent row", pair, face):
                        break


def alphabet(enc, rows):
    """What a random roman text is made of: every ``from``, every character of one, and
    a space."""
    tokens = {r.source for r in rows} | {c for r in rows for c in r.source} | {" "}
    return sorted(tokens)


def check_sweep(report, enc):
    """Seeded random roman texts, and random sequences of outputs, round-trip."""
    for face, at, rows in row_lists(enc):
        chooser = random.Random(f"{enc.name}:{face}")
        tokens = alphabet(enc, rows)
        failed = 0
        for _ in range(SWEEP):
            roman = "".join(chooser.choice(tokens) for _ in range(chooser.randint(1, LONGEST)))
            if not round_trip(report, enc, at, "the random text", roman, face):
                failed += 1
                if failed >= 3:
                    break
        failed = 0
        for _ in range(SWEEP):
            chosen = [chooser.choice(rows) for _ in range(chooser.randint(1, LONGEST))]
            roman = "".join(r.source for r in chosen)
            applied = [row for _, _, row in E.pieces(enc, roman, face)]
            if [id(r) for r in applied] != [id(r) for r in chosen]:
                continue
            unicode = "".join(r.target for r in chosen)
            read = E.decode(enc, unicode, face)
            if read != roman or E.encode(enc, read, face) != unicode:
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


def check_samples(report, enc):
    for text in V.samples(enc):
        round_trip(report, enc, ("rows",), "the sample", text)


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
                            at + (row.order,),
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
        check_rows(report, enc)
        check_sweep(report, enc)
        check_samples(report, enc)
        if shaping:
            check_fonts(report, enc, faces)
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
