# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Unit tests of encode.py.

    python3 -m unittest tools/encode_test.py
"""

import contextlib
import io
import json
import os
import shutil
import sys
import tempfile
import unittest
from unittest import mock

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import encode as E  # noqa: E402


class Case(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.dir)

    def write(self, data, name=None, text=None):
        name = name or data["name"]
        if text is None and isinstance(data, dict) and "fonts" in data and "accepts" not in data and data.get("kind") != "codage":
            data = {**data, "accepts": self.declared(data)}
        if (text is None and isinstance(data, dict) and "fonts" in data and "separator" not in data
                and data.get("kind") != "codage"):
            data = {**data, "separator": " "}
        path = os.path.join(self.dir, f"{name}.json")
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(text if text is not None else json.dumps(data, ensure_ascii=False, indent=4))
        return path

    @staticmethod
    def declared(data):
        """An ``accepts`` list of the characters the rows of a test encoding state."""
        chars = set()
        for row in list(data.get("rows", [])) + [r for f in data.get("faces", {}).values() for r in f.get("rows", [])]:
            source = row[0] if isinstance(row, list) and row else row.get("from") if isinstance(row, dict) else None
            if isinstance(source, str):
                chars |= set(source)
        return sorted(chars - {E.OPEN, E.CLOSE} - set(E.WHITESPACE))

    def encoding(self, rows, **more):
        data = {"name": "test", "fonts": ["face-one", "face-two"], "rows": rows}
        data.update(more)
        return E.load(self.write(data))


class LongestMatch(Case):
    def test_the_longest_from_wins(self):
        enc = self.encoding([["s", "S"], ["h", "H"], ["sh", "X"], ["shh", "Y"]])
        self.assertEqual(E.encode(enc, "sh"), "X")
        self.assertEqual(E.encode(enc, "shh"), "Y")
        self.assertEqual(E.encode(enc, "shs"), "XS")
        self.assertEqual(E.encode(enc, "hs"), "HS")

    def test_the_earlier_of_two_rows_of_one_length_wins(self):
        enc = self.encoding([["k", "K"], ["k", "Q"]])
        self.assertEqual(E.encode(enc, "k"), "K")

    def test_a_condition_that_holds_comes_before_a_row_with_none(self):
        enc = self.encoding([["n", "n"], {"from": "n", "to": "N", "at": "end"}])
        self.assertEqual(E.encode(enc, "nn"), "nN")


class Conditions(Case):
    def setUp(self):
        super().setUp()
        self.enc = self.encoding(
            [
                ["a", "A"],
                ["b", "B"],
                {"from": "y", "to": "V", "before": "vowel"},
                {"from": "y", "to": "C", "before": "consonant"},
                ["y", "Y"],
                {"from": "q", "to": "<", "at": "start"},
                {"from": "q", "to": ">", "at": "end"},
                ["q", "Q"],
                ["-", "-"],
                [".", "."],
                ["!", "!"],
                ["1", "1"],
            ],
            vowels="a",
        )

    def test_before_vowel(self):
        self.assertEqual(E.encode(self.enc, "ya"), "VA")

    def test_before_consonant(self):
        self.assertEqual(E.encode(self.enc, "yb"), "CB")

    def test_before_holds_at_neither_the_end_nor_a_non_letter(self):
        self.assertEqual(E.encode(self.enc, "y"), "Y")
        self.assertEqual(E.encode(self.enc, "y."), "Y.")
        self.assertEqual(E.encode(self.enc, "y1"), "Y1")

    def test_at_start(self):
        self.assertEqual(E.encode(self.enc, "qa"), "<A")
        self.assertEqual(E.encode(self.enc, "b qa"), "B <A")
        self.assertEqual(E.encode(self.enc, "b-qa"), "B-<A")

    def test_at_end(self):
        self.assertEqual(E.encode(self.enc, "aq"), "A>")
        self.assertEqual(E.encode(self.enc, "aq b"), "A> B")
        self.assertEqual(E.encode(self.enc, "aq!"), "A>!")

    def test_neither_edge(self):
        self.assertEqual(E.encode(self.enc, "aqa"), "AQA")


class Faces(Case):
    def test_a_face_row_applies_in_its_face_alone_and_wins_there(self):
        enc = self.encoding(
            [["a", "A"], ["b", "B"], ["ab", "X"]],
            faces={"face-two": {"rows": [["a", "2"]]}},
        )
        self.assertEqual(E.encode(enc, "ab"), "X")
        self.assertEqual(E.encode(enc, "ab", face="face-one"), "X")
        self.assertEqual(E.encode(enc, "ab", face="face-two"), "2B")
        self.assertEqual(E.decode(enc, "2B", face="face-two"), "ab")

    def test_a_face_the_encoding_does_not_serve_is_refused(self):
        enc = self.encoding([["a", "A"]])
        with self.assertRaises(E.EncodingError):
            E.encode(enc, "a", face="face-three")


class Refusal(Case):
    def refusal(self, call, *args, **kwargs):
        with self.assertRaises(E.EncodingError) as caught:
            call(*args, **kwargs)
        return str(caught.exception)

    def test_an_unmatched_character_is_refused_at_its_line_and_column(self):
        enc = self.encoding([["a", "A"]])
        self.assertEqual(
            self.refusal(E.encode, enc, "a a\naa!"),
            '<text>:2:3: error: "!" (U+0021) is not in the `test` encoding',
        )
        self.assertEqual(
            self.refusal(E.encode, enc, "a;", source="note.md"),
            'note.md:1:2: error: ";" (U+003B) is not in the `test` encoding',
        )

    def test_a_character_no_row_matches_where_it_stands_is_refused(self):
        enc = self.encoding([["a", "A"], {"from": "-", "to": E.mark("-"), "at": "end"}])
        self.assertEqual(E.encode(enc, "a-"), "A" + E.mark("-"))
        self.assertEqual(
            self.refusal(E.encode, enc, "-a"),
            '<text>:1:1: error: no row of the `test` encoding matches "-" (U+002D) here',
        )

    def test_a_code_point_no_row_writes_is_refused_in_decoding(self):
        enc = self.encoding([["a", "A"], ["á", "A" + E.mark("á") + E.END_MARK]])
        self.assertEqual(
            self.refusal(E.decode, enc, "AB"),
            '<text>:1:2: error: "B" (U+0042) is written by no row of the `test` encoding',
        )
        self.assertIn(
            "(U+E01EF) is written by no row of the `test` encoding",
            self.refusal(E.decode, enc, E.END_MARK),
        )
        enc = self.encoding([["a", "XY"]])
        self.assertEqual(
            self.refusal(E.decode, enc, "XYXZ"),
            '<text>:1:3: error: no row of the `test` encoding writes "X" (U+0058) here',
        )

    def test_a_tool_may_keep_an_unmatched_character(self):
        enc = self.encoding([["a", "A"]])
        self.assertEqual(
            E.pieces(enc, "ab", strict=False),
            [("a", "A", enc.rows[0]), ("b", "b", None)],
        )


class Extends(Case):
    def base(self, rows, name="base"):
        return self.write({"name": name, "rows": rows})

    def test_the_rows_are_the_base_s_unstated_rows_then_the_encoding_s(self):
        self.base([[".", E.mark(".")], ["?", E.mark("?")]])
        enc = self.encoding([["a", "A"], [".", "P"]], extends="base")
        self.assertEqual([r.source for r in enc.rows], ["?", "a", "."])
        self.assertEqual(E.encode(enc, "a. a?"), "AP A" + E.mark("?"))
        self.assertEqual(E.decode(enc, "AP A" + E.mark("?")), "a. a?")

    def test_a_row_of_the_encoding_replaces_every_base_row_of_its_from(self):
        self.base([["-", E.mark("-")]])
        enc = self.encoding([{"from": "-", "to": " " + E.mark("-") + E.END_MARK, "at": "end"},
                             ["-", E.mark("-")]], extends="base")
        self.assertEqual([r.source for r in enc.rows], ["-", "-"])

    def test_an_inherited_row_reports_at_the_base_file(self):
        base = self.base([["?", "X"]])
        path = self.write({"name": "test", "fonts": ["f"], "extends": "base", "rows": [["a", "X"]]})
        with self.assertRaises(E.EncodingError) as caught:
            E.load(path)
        self.assertIn(f"writes what the row at {E._shown(base)} rows.0 writes", str(caught.exception))

    def test_a_missing_base_is_a_fault_at_extends(self):
        path = self.write({"name": "test", "fonts": ["f"], "extends": "absent", "rows": []})
        with self.assertRaises(E.EncodingError) as caught:
            E.load(path)
        self.assertIn("`absent` is not a base file beside the encoding", str(caught.exception))

    def test_a_base_file_takes_only_name_and_rows(self):
        self.write({"name": "base", "fonts": ["f"], "rows": []})
        path = self.write({"name": "test", "fonts": ["f"], "extends": "base", "rows": []})
        with self.assertRaises(E.EncodingError) as caught:
            E.load(path)
        self.assertIn("`fonts` is not a key of a base file", str(caught.exception))

    def test_the_standard_is_not_applied_alone(self):
        with self.assertRaises(E.EncodingError) as caught:
            E.load("standard")
        self.assertIn("is not applied alone", str(caught.exception))


class Decoding(Case):
    def test_the_longest_to_is_read_first(self):
        enc = self.encoding([["s", "S"], ["h", "H"], ["sh", "X"], ["shh", "XH"]])
        self.assertEqual(E.decode(enc, "XS"), "shs")
        self.assertEqual(E.decode(enc, "XHS"), "shhs")
        self.assertEqual(E.decode(enc, "HS"), "hs")

    def test_a_row_writing_one_character_reads_back_as_its_whole_from(self):
        enc = self.encoding([["c", "C"], ["h", "H"], ["ch", "X"]])
        self.assertEqual(E.decode(enc, "X"), "ch")
        self.assertEqual(E.decode(enc, "CH"), "ch")
        self.assertEqual(E.encode(enc, "ch"), "X")

    def test_a_row_that_draws_nothing_is_restored(self):
        enc = self.encoding([["a", "A"], ["-", E.mark("-")], ["b", "B"]])
        self.assertEqual(E.encode(enc, "a-b"), "A" + E.mark("-") + "B")
        self.assertEqual(E.decode(enc, "A" + E.mark("-") + "B"), "a-b")

    def test_an_inherent_vowel_is_restored(self):
        enc = self.encoding(
            [["k", "K+"], {"from": "k", "to": "K", "before": "vowel"}, ["a", E.mark("a")], ["i", "i"]],
            vowels="ai",
        )
        for roman in ("ka", "ki", "k", "kak"):
            self.assertEqual(E.decode(enc, E.encode(enc, roman)), roman)

    def test_rows_drawn_alike_are_told_apart_by_the_mark(self):
        enc = self.encoding([["a", "X"], ["A", "X" + E.mark("A") + E.END_MARK]])
        self.assertEqual(E.encode(enc, "aA"), "XX\U000E0121\U000E01EF")
        self.assertEqual(E.decode(enc, "XX\U000E0121\U000E01EF"), "aA")

    def test_a_face_reads_its_rows_and_the_shared_rows(self):
        enc = self.encoding([["a", "A"], ["b", "B"]], faces={"face-two": {"rows": [["a", "2"]]}})
        self.assertEqual(E.decode(enc, "2B", face="face-two"), "ab")
        self.assertEqual(E.decode(enc, "AB", face="face-two"), "ab")
        with self.assertRaises(E.EncodingError):
            E.decode(enc, "2B")


class CanonicalEncoding(Case):
    def test_omitted_marks_aliases_and_spaces_use_conventional_reading(self):
        enc = self.encoding([["a", "A"], ["b", "B"], ["x", "A"],
                             ["'", ""], ["-", " "]], roundTrip="canonical")
        self.assertEqual(E.encode(enc, "x'-b"), "A B")
        self.assertEqual(E.decode(enc, "A B"), "a b")
        self.assertEqual(E.canonical(enc, "x'-b"), "a b")

    def test_unknown_modes_are_refused(self):
        with self.assertRaises(E.EncodingError):
            self.encoding([["a", "A"]], roundTrip="anything")
        with self.assertRaises(E.EncodingError):
            self.encoding([["a", "A"]], groupCase="anything")


class AelwythiEncoding(unittest.TestCase):
    def setUp(self):
        self.enc = E.load("aelwythi-semaron")

    def test_dedicated_groups_have_only_minuscule_and_majuscule_forms(self):
        for group, point in [("ch", 0xF028C), ("sh", 0xF0286), ("th", 0xF0250),
                             ("dh", 0xF0280), ("kh", 0xF0282), ("gh", 0xF0284),
                             ("zh", 0xF0288), ("ts", 0xF028A), ("ng", 0xF028E)]:
            for spelling, value in [(group, point), (group.capitalize(), point + 1)]:
                with self.subTest(spelling=spelling):
                    self.assertEqual(E.encode(self.enc, spelling), chr(value))
                    self.assertEqual(E.decode(self.enc, chr(value)), spelling)
            for illegal in [group.upper(), group[0] + group[1].upper()]:
                for text in [illegal, "a" + illegal + "a"]:
                    with self.subTest(illegal=text), self.assertRaises(E.EncodingError):
                        E.encode(self.enc, text)

    def test_contextual_ny_stress_and_consonant_y(self):
        for text, expected in [("nya", "\U000F0290\U000F0230"),
                               ("Nyá", "\U000F0291\U000F0230\U000E0114"),
                               ("ny", "\U000F023C\U000F0245"),
                               ("y", "\U000F0245"), ("i", "\U000F0237"),
                               ("q", "\U000F0247"), ("Q", "\U000F0217"),
                               ("á", "\U000F0230\U000E0114"),
                               ("Á", "\U000F0200\U000E0114")]:
            with self.subTest(text=text):
                self.assertEqual(E.encode(self.enc, text), expected)
                self.assertEqual(E.decode(self.enc, expected), text)
        for illegal in ["NYa", "nYa", "ë", "aë", "à", "c", "x"]:
            with self.subTest(illegal=illegal), self.assertRaises(E.EncodingError):
                E.encode(self.enc, illegal)

    def test_punctuation_normalizes_without_extra_metadata(self):
        text = "'a-b'."
        encoded = E.encode(self.enc, text)
        self.assertEqual(encoded, "\U000F0230 \U000F0231\U000F0268")
        self.assertEqual(E.decode(self.enc, encoded), "a b.")

    def test_other_semaron_encoding_is_unchanged(self):
        enc = E.load("semaron")
        self.assertEqual(enc.round_trip, "exact")
        self.assertIsNone(enc.group_case)
        text = "thalen kaa"
        self.assertEqual(E.decode(enc, E.encode(enc, text)), text)


class SharedIndentation(unittest.TestCase):
    def test_indentation_is_reserved_at_line_start(self):
        for name in ["aelwythi-semaron", "semaron", "pirzath"]:
            enc = E.load(name)
            self.assertEqual(E.encode(enc, "^^"), "\U000E0104\U000E0104")
            self.assertEqual(E.encode(enc, "a\n^"), E.encode(enc, "a/") + "\U000E0104")

    def test_indented_line_boundaries_round_trip(self):
        for name in ["helonika", "pirzath", "semaron", "aelwythi-semaron"]:
            enc = E.load(name)
            encoded = E.encode(enc, "a\n^^a")
            decoded = E.decode(enc, encoded)
            self.assertEqual(decoded, "a/^^a")
            self.assertEqual(E.encode(enc, decoded), encoded)
            self.assertEqual(E.canonical(enc, "a\n^^a"), decoded)

    def test_an_indent_inside_ordinary_text_is_refused(self):
        for name in ["semaron", "helonika", "aelwythi-semaron"]:
            with self.assertRaises(E.EncodingError):
                E.encode(name, "a^a")

    def test_pirzath_fourteenth_digit_keeps_its_numeric_context(self):
        enc = E.load("pirzath")
        self.assertEqual(E.encode(enc, "0^"), "\U000F0040\U000F004E")
        self.assertEqual(E.decode(enc, "\U000F0040\U000F004E"), "0^")


class Marks(Case):
    def test_printable_ascii_is_a_variation_selector_of_its_own(self):
        self.assertEqual(E.mark("a"), "\U000E0141")
        self.assertTrue(E.mark(" -").startswith("\U000E015B"))
        self.assertTrue(all(E.is_mark(c) for c in E.mark("~ {")))

    def test_any_other_character_is_spelled_by_its_code_point(self):
        self.assertEqual(E.mark("á"), "".join(chr(0xE0100 + ord(c) - 0x20) for c in "{e1}"))
        self.assertEqual(E.mark("{"), "\U000E0110")
        self.assertNotEqual(E.mark("á"), E.mark("a"))

    def test_a_run_is_two_or_more_other_drawings(self):
        self.assertTrue(E.is_run("XX", {"X", "XX"}))
        self.assertTrue(E.is_run("XY", {"X", "Y", "XY"}))
        self.assertFalse(E.is_run("X", {"X"}))
        self.assertFalse(E.is_run("XY", {"X", "XY"}))


class Loading(Case):
    def faults(self, path):
        with self.assertRaises(E.EncodingError) as caught:
            E.load(path)
        return [str(f) for f in caught.exception.faults]

    def test_faults_are_reported_at_their_line_and_column(self):
        text = (
            '{\n    "name": "bad",\n    "fonts": ["face"], "accepts": ["a", "y"], "separator": " ",\n    "rows": [\n'
            '        {"from": "y", "to": "Y", "before": "vowl"},\n'
            '        {"to": "Z"},\n'
            '        ["a"]\n'
            '    ],\n    "colour": "red"\n}\n'
        )
        path = self.write(None, name="bad", text=text)
        shown = E._shown(path)
        self.assertEqual(
            self.faults(path),
            [
                f"{shown}:9:5: error: `colour` is not an encoding key; an encoding takes "
                "`name`, `kind`, `fonts`, `extends`, `codage`, `accepts`, `separator`, `vowels`, `rows`, `faces`, `roundTrip`, `groupCase`",
                f'{shown}:5:44: error: `before` is `vowel` or `consonant`, not "vowl"',
                f"{shown}:6:9: error: needs `from`, the one or more characters the row matches",
                f"{shown}:7:9: error: a row written as a list is two strings, `[from, to]`",
            ],
        )

    def test_a_syntax_error_gives_its_position(self):
        path = self.write(None, name="bad", text='{"name": "bad",\n  "rows": [}\n')
        self.assertTrue(self.faults(path)[0].startswith(f"{E._shown(path)}:2:"))

    def test_a_key_stated_twice_is_a_fault(self):
        path = self.write(None, name="bad", text='{"name": "bad", "name": "bad", "fonts": ["f"], "rows": []}')
        self.assertIn("stated twice", self.faults(path)[0])

    def test_the_name_is_the_file_s(self):
        path = self.write({"name": "other", "fonts": ["f"], "rows": []}, name="bad")
        self.assertIn("the file is `bad.json`", self.faults(path)[0])

    def test_separators_and_decode_are_refused(self):
        text = '{"name": "bad", "fonts": ["f"], "accepts": ["a"], "separator": " ", "rows": [["a", "A"]],\n "separators": ["-"], "decode": []}'
        path = self.write(None, name="bad", text=text)
        shown = E._shown(path)
        self.assertEqual(
            self.faults(path),
            [
                f"{shown}:2:2: error: `separators` is not an encoding key: a row that draws "
                "nothing writes its mark, so decoding restores it",
                f"{shown}:2:23: error: `decode` is not an encoding key: decoding reads every "
                "output back as its own row's `from`",
            ],
        )

    def test_a_row_that_writes_nothing_is_refused_at_its_to(self):
        text = '{"name": "bad", "fonts": ["f"], "accepts": ["a", "b"], "separator": " ", "rows": [\n ["a", ""],\n {"from": "b", "to": ""}]}'
        path = self.write(None, name="bad", text=text)
        shown = E._shown(path)
        message = (
            "error: writes nothing; a row that draws nothing writes the mark of its `from`, "
            "so that decoding restores it"
        )
        self.assertEqual(self.faults(path), [f"{shown}:2:8: {message}", f"{shown}:3:22: {message}"])

    def test_two_froms_writing_one_output_are_refused_at_the_later(self):
        text = '{"name": "bad", "fonts": ["f"], "accepts": ["a", "A", "b"], "separator": " ", "rows": [\n ["a", "X"],\n ["A", "X"],\n ["b", "B"]]}'
        path = self.write(None, name="bad", text=text)
        self.assertEqual(
            self.faults(path),
            [
                f"{E._shown(path)}:3:2: error: writes what the row at rows.0 writes, for \"a\"; "
                "a row that draws what an earlier row draws adds the mark of its `from` and the "
                "end mark"
            ],
        )

    def test_one_from_may_write_one_output_under_two_conditions(self):
        path = self.write(
            {
                "name": "fine",
                "fonts": ["f"],
                "rows": [
                    {"from": "-", "to": E.mark("-"), "at": "start"},
                    {"from": "-", "to": E.mark("-"), "at": "end"},
                ],
            }
        )
        self.assertEqual(E.load(path).name, "fine")

    def test_a_face_row_may_not_write_what_a_shared_row_of_another_from_writes(self):
        path = self.write(
            {"name": "bad", "fonts": ["f"], "rows": [["a", "A"]], "faces": {"f": {"rows": [["b", "A"]]}}}
        )
        self.assertIn("writes what the row at rows.0 writes", self.faults(path)[0])

    def test_an_unknown_name_names_the_encodings(self):
        with self.assertRaises(E.EncodingError) as caught:
            E.load("no-such-encoding")
        self.assertIn("no encoding is named", str(caught.exception))


class Whitespace(Case):
    """Whitespace is one word separator, stated by the encoding."""

    def setUp(self):
        super().setUp()
        self.spaced = self.encoding([["a", "A"], ["/", "|"], ["//", "||"]])
        self.bare = self.encoding([["a", "A"]], separator="")
        self.glyph = self.encoding([["a", "A"]], separator="\u2002")

    def test_a_run_of_whitespace_is_one_separator(self):
        for run in (" ", "  ", "\t", "\n", "\r\n", " \t\n\r  \n"):
            self.assertEqual(E.encode(self.spaced, "a" + run + "a"), "A A")
            self.assertEqual(E.encode(self.glyph, "a" + run + "a"), "A\u2002A")
        self.assertEqual(E.encode(self.spaced, "a      \t\t\n\t   a"), E.encode(self.spaced, "a a"))

    def test_decoding_writes_a_single_space(self):
        self.assertEqual(E.decode(self.spaced, "A A"), "a a")
        self.assertEqual(E.decode(self.glyph, "A\u2002A"), "a a")
        self.assertEqual(E.canonical(self.spaced, " a \n\t a\r\n"), " a a ")

    def test_a_separator_that_is_empty_writes_nothing(self):
        self.assertEqual(E.encode(self.bare, "a \n a"), "AA")
        self.assertEqual(E.encode(self.bare, " "), "")
        self.assertEqual(E.decode(self.bare, "AA"), "aa")
        self.assertEqual(E.canonical(self.bare, " a \n a "), "aa")

    def test_whitespace_in_a_span_is_not_a_separator(self):
        self.assertEqual(E.canonical(self.spaced, "a  \u27e6ONE   TWO\u27e7  a"), "a \u27e6ONE   TWO\u27e7 a")

    def test_only_space_tab_newline_and_return_are_whitespace(self):
        self.assertEqual(self.position(E.encode, self.spaced, "a\u00a0a"), (1, 2))
        self.assertEqual(self.position(E.encode, self.spaced, "a\u000ba"), (1, 2))

    def test_a_newline_is_only_whitespace_beside_the_verse_marks(self):
        self.assertEqual(E.encode(self.spaced, "a/\na//\n\na"), "A| A|| A")

    def test_a_row_may_not_match_whitespace(self):
        path = self.write({"name": "bad", "fonts": ["f"], "accepts": ["a"], "separator": " ",
                           "rows": [["a", "A"], ["a a", "B"]]})
        self.assertIn("whitespace is the word separator", self.faults(path)[0])

    def test_a_row_may_not_write_what_the_separator_writes(self):
        path = self.write({"name": "bad", "fonts": ["f"], "accepts": ["a"], "separator": " ",
                           "rows": [["a", " "]]})
        self.assertIn("writes what the row at separator writes", self.faults(path)[0])

    def test_the_separator_is_required_and_a_string(self):
        path = self.write(None, name="bad", text='{"name": "bad", "fonts": ["f"], "accepts": ["a"], "rows": []}')
        self.assertIn("needs `separator`", self.faults(path)[0])
        path = self.write(None, name="bad", text='{"name": "bad", "fonts": ["f"], "accepts": ["a"], "separator": 1, "rows": []}')
        self.assertIn("`separator` is a string", self.faults(path)[0])

    def test_a_codage_takes_no_separator(self):
        path = self.write(None, name="bad", text='{"name": "bad", "kind": "codage", "fonts": ["f"], "separator": " ", "rows": []}')
        self.assertIn("`separator` is not a key of a codage", self.faults(path)[0])

    def test_a_font_with_no_encoding_refuses_whitespace_outside_the_markers(self):
        self.assertEqual(self.position(E.encode, E.Encoding.names_only("f"), " "), (1, 1))

    def test_the_shared_punctuation_assignments(self):
        std = E.load_base(os.path.join(E.ENCODINGS, "standard.json"))
        targets = {r.source: r.target for r in std.rows}
        for source, point in [(".", 0xE0100), ("?", 0xE0101), ("‼", 0xE0102),
                              ("!", 0xE0103), ("^", 0xE0104), (",", 0xE0105),
                              ("«", 0xE0106), ("»", 0xE0107), ("‹", 0xE0108),
                              ("›", 0xE0109), ("—", 0xE010A), ("…", 0xE010B),
                              ("/", 0xE010C), ("{", 0xE0110), ("}", 0xE0111)]:
            self.assertEqual(targets[source], chr(point))
        self.assertNotIn("!!", targets)
        self.assertNotIn("//", targets)
        self.assertNotIn("***", targets)
        for source in ["?", "‼", "!", "^", ",", "—", "…", "/", "{", "}"]:
            enc = E.load("aelwythi-semaron")
            self.assertEqual(E.encode(enc, source), targets[source])

    def test_shared_verse_controls_and_prose_whitespace(self):
        enc = E.load("aelwythi-semaron")
        self.assertEqual(E.encode(enc, "a\nb", verse=True), "\U000F0230\U000E010C\U000F0231")
        self.assertEqual(E.encode(enc, "a\n\nb", verse=True), "\U000F0230\U000E010D\U000F0231")
        self.assertEqual(E.encode(enc, "--- {.canto}"), "\U000E010E")
        self.assertEqual(E.encode(enc, "a\nb"), "\U000F0230 \U000F0231")
        self.assertEqual(E.decode(enc, "\U000E010D"), "\n\n")
        self.assertEqual(E.encode(enc, "a\n--- {.canto}\nb", verse=True),
                         "\U000F0230\U000E010E\U000F0231")
        self.assertEqual(E.encode(enc, "a\n \nb", verse=True),
                         "\U000F0230\U000E010D\U000F0231")

    def position(self, run, enc, text):
        with self.assertRaises(E.EncodingError) as caught:
            run(enc, text)
        return caught.exception.line, caught.exception.column

    def faults(self, path):
        with self.assertRaises(E.EncodingError) as caught:
            E.load(path)
        return [str(f) for f in caught.exception.faults]


class Literal(Case):
    """The literal immutable markers."""

    def setUp(self):
        super().setUp()
        self.write({"name": "codes", "kind": "codage", "fonts": ["f"], "rows": [
            ["ONE", "\U000F0001"], ["TWO", "\U000F0002"], ["-", E.mark("-")], ["(", "\U000F0003"], [")", "\U000F0004"],
        ]})
        self.write({"name": "script", "fonts": ["f"], "codage": "codes", "rows": [
            ["a", "A"], ["b", "B"],
        ]})
        self.write({"name": "plain", "fonts": ["f"], "rows": [
            ["a", "A"], ["b", "B"],
        ]})
        self.enc = E.load(os.path.join(self.dir, "script.json"))
        self.codes = self.enc.codage
        self.plain = E.load(os.path.join(self.dir, "plain.json"))
        self.open, self.close = E.mark("\u27e6"), E.mark("\u27e7")

    def position(self, run, enc, text):
        with self.assertRaises(E.EncodingError) as caught:
            run(enc, text)
        return caught.exception.line, caught.exception.column

    def test_a_stated_codage_encodes_the_span_between_marker_marks(self):
        self.assertEqual(
            E.encode(self.enc, "a \u27e6ONE TWO\u27e7 b"),
            "A " + self.open + "\U000F0001\U000F0002" + self.close + " B",
        )
        self.assertEqual(E.decode(self.enc, E.encode(self.enc, "a \u27e6ONE TWO\u27e7 b")),
                         "a \u27e6ONE TWO\u27e7 b")

    def test_whitespace_in_a_span_only_separates_codes(self):
        tidy = E.encode(self.enc, "\u27e6ONE TWO\u27e7")
        for loose in ("\u27e6   ONE      TWO \n\t\u27e7", "\u27e6\nONE\tTWO\u27e7"):
            self.assertEqual(E.encode(self.enc, loose), tidy)
            self.assertEqual(E.decode(self.enc, tidy), "\u27e6ONE TWO\u27e7")
        names = "\u27e6LATIN_SMALL_LETTER_I\n\n LATIN_SMALL_LETTER_I\u27e7"
        self.assertEqual(E.encode(self.plain, names),
                         E.encode(self.plain, "\u27e6LATIN_SMALL_LETTER_I LATIN_SMALL_LETTER_I\u27e7"))

    def test_notation_joins_codes_without_spaces_and_decodes_that_way(self):
        text = "\u27e6ONE-TWO(ONE)\u27e7"
        self.assertEqual(E.decode(self.enc, E.encode(self.enc, text)), text)
        self.assertEqual(E.decode(self.enc, E.encode(self.enc, "\u27e6ONETWO\u27e7")), "\u27e6ONE TWO\u27e7")

    def test_a_standard_mark_inside_a_span_is_refused_at_its_position(self):
        self.assertEqual(self.position(E.encode, self.enc, "\u27e6ONE,TWO\u27e7"), (1, 5))
        self.assertEqual(self.position(E.encode, self.enc, "a\n\u27e6ONE TWO?\u27e7"), (2, 9))
        self.assertEqual(self.position(E.encode, self.plain, "\u27e6LATIN_SMALL_LETTER_I.\u27e7"), (1, 22))

    def test_a_code_outside_the_markers_is_ordinary_roman(self):
        self.assertEqual(self.position(E.encode, self.enc, "ONE"), (1, 1))
        self.assertEqual(self.position(E.encode, self.enc, "a ONE"), (1, 3))

    def test_a_codage_is_not_a_whole_text_encoding(self):
        with self.assertRaises(E.EncodingError) as caught:
            E.load(os.path.join(self.dir, "codes.json"))
        self.assertIn("is a codage", caught.exception.message)

    def test_a_character_outside_accepts_is_refused_though_a_row_exists(self):
        path = self.write({"name": "narrow", "fonts": ["f"], "accepts": ["a"], "rows": [["a", "A"], ["b", "B"]]})
        enc = E.load(path)
        self.assertEqual(E.encode(enc, "aa"), "AA")
        self.assertEqual(self.position(E.encode, enc, "ab"), (1, 2))

    def test_accepts_takes_characters_and_ranges(self):
        path = self.write({"name": "wide", "fonts": ["f"], "accepts": ["a-c", "-"],
                           "rows": [["a", "A"], ["b", "B"], ["c", "C"], ["-", "="]]})
        enc = E.load(path)
        self.assertEqual(E.encode(enc, "ab-c"), "AB=C")
        bad = self.write({"name": "bad", "fonts": ["f"], "accepts": ["ab", "c-a"], "rows": [["a", "A"]]})
        with self.assertRaises(E.EncodingError) as caught:
            E.load(bad)
        self.assertEqual(len(caught.exception.faults), 2)

    def test_accepts_is_required(self):
        path = self.write(None, name="bare", text='{"name": "bare", "fonts": ["f"], "rows": [["a", "A"]]}')
        with self.assertRaises(E.EncodingError) as caught:
            E.load(path)
        self.assertIn("needs `accepts`", caught.exception.message)

    def test_a_font_with_no_encoding_accepts_text_only_between_the_markers(self):
        enc = E.Encoding.names_only("some-font")
        self.assertEqual(E.encode(enc, "\u27e6LATIN_SMALL_LETTER_A\u27e7"), self.open + "a" + self.close)
        self.assertEqual(E.decode(enc, self.open + "a" + self.close), "\u27e6LATIN_SMALL_LETTER_A\u27e7")
        for text, at in (("a", (1, 1)), (" ", (1, 1)), ("\u27e6LATIN_SMALL_LETTER_A\u27e7.", (1, 23))):
            self.assertEqual(self.position(E.encode, enc, text), at)
        self.assertEqual(self.position(E.decode, enc, "a"), (1, 1))

    def test_the_marker_marks_are_the_marks_of_the_markers(self):
        self.assertEqual(self.open, "\U000E0112")
        self.assertEqual(self.close, "\U000E0113")
        for enc in (self.enc, self.plain):
            self.assertEqual(E.encode(enc, "\u27e6\u27e7"), self.open + self.close)

    def test_without_a_codage_a_code_is_a_character_name(self):
        text = "a\u27e6LATIN_SMALL_LETTER_A_WITH_ACUTE LATIN_SMALL_LETTER_I  LATIN_SMALL_LETTER_M\u27e7b"
        self.assertEqual(E.encode(self.plain, text), "A" + self.open + "\u00e1im" + self.close + "B")
        self.assertEqual(
            E.decode(self.plain, E.encode(self.plain, text)),
            "a\u27e6LATIN_SMALL_LETTER_A_WITH_ACUTE LATIN_SMALL_LETTER_I LATIN_SMALL_LETTER_M\u27e7b",
        )

    def test_a_name_with_a_space_in_it_is_written_with_underscores(self):
        self.assertEqual(E.encode(self.plain, "\u27e6SPACE\u27e7"), self.open + " " + self.close)
        self.assertEqual(E.decode(self.plain, self.open + " " + self.close), "\u27e6SPACE\u27e7")

    def test_the_private_use_characters_are_named_by_the_names_table(self):
        self.assertEqual(E.encode(self.plain, "\u27e6PIRZATH_LETTER_A\u27e7"), self.open + "\U000F0000" + self.close)
        self.assertEqual(E.decode(self.plain, self.open + "\U000F0000" + self.close), "\u27e6PIRZATH_LETTER_A\u27e7")

    def test_a_misspelled_or_lowercase_name_is_refused_at_its_position(self):
        self.assertEqual(
            self.position(E.encode, self.plain, "a\nb \u27e6LATIN_SMALL_LETTER_I ACCUTE\u27e7"), (2, 25))
        self.assertEqual(self.position(E.encode, self.plain, "\u27e6latin_small_letter_i\u27e7"), (1, 2))
        self.assertEqual(self.position(E.encode, self.plain, "\u27e6LATIN_SMALL_LETTER\u27e7"), (1, 2))

    def test_a_character_with_no_name_is_refused_in_decoding(self):
        self.assertEqual(self.position(E.decode, self.plain, self.open + "\U0010FFFD" + self.close),
                         (1, len(self.open) + 1))

    def test_spans_round_trip_with_mixed_content(self):
        for enc, code in ((self.enc, "ONE"), (self.plain, "LATIN_SMALL_LETTER_I")):
            pieces = "ab "
            for text in (f"\u27e6{code}\u27e7", "\u27e6\u27e7", f"{pieces}\u27e6{code}\u27e7{pieces}",
                         f"{pieces}\u27e6{code}\u27e7\u27e6{code}\u27e7 {pieces}",
                         f"{pieces}\n\u27e6{code}\u27e7\n{pieces}"):
                unicode = E.encode(enc, text)
                self.assertEqual(E.decode(enc, unicode), E.canonical(enc, text))
                self.assertEqual(E.encode(enc, E.decode(enc, unicode)), unicode)

    def test_pieces_cover_the_markers_and_the_codes(self):
        got = E.pieces(self.enc, "a\u27e6ONE\u27e7")
        self.assertEqual([f for f, _, _ in got], ["a", "\u27e6", "ONE", "\u27e7"])
        self.assertEqual("".join(t for _, t, _ in got), E.encode(self.enc, "a\u27e6ONE\u27e7"))
        got = E.pieces(self.plain, "\u27e6LATIN_SMALL_LETTER_I LATIN_SMALL_LETTER_I\u27e7")
        self.assertEqual("".join(f for f, _, _ in got), "\u27e6LATIN_SMALL_LETTER_I LATIN_SMALL_LETTER_I\u27e7")

    def test_an_unmatched_or_nested_marker_is_refused_where_it_is(self):
        for enc in (self.enc, self.plain):
            self.assertEqual(self.position(E.encode, enc, "a\u27e6"), (1, 2))
            self.assertEqual(self.position(E.encode, enc, "ab\u27e7"), (1, 3))
            self.assertEqual(self.position(E.encode, enc, "\u27e6\u27e6\u27e7\u27e7"), (1, 2))
            self.assertEqual(self.position(E.decode, enc, self.open), (1, 1))
            self.assertEqual(self.position(E.decode, enc, "A" + self.close), (1, 2))
            self.assertEqual(
                self.position(E.decode, enc, self.open + self.open + self.close + self.close),
                (1, len(self.open) + 1),
            )

    def test_a_character_the_stated_codage_refuses_is_placed_in_the_whole_text(self):
        self.assertEqual(self.position(E.encode, self.enc, "a\nb \u27e6ONE x\u27e7"), (2, 8))
        self.assertEqual(self.position(E.encode, self.enc, "\u27e6ONE\nx\u27e7"), (2, 1))
        self.assertEqual(self.position(E.decode, self.enc, self.open + "\U0010FFFD" + self.close),
                         (1, len(self.open) + 1))

    def test_a_row_may_not_state_a_marker(self):
        for row in (["\u27e6", "X"], {"from": "a\u27e7", "to": "X"}):
            path = self.write({"name": "bad", "fonts": ["f"], "rows": [row]})
            with self.assertRaises(E.EncodingError) as caught:
                E.load(path)
            self.assertIn("literal immutable marker", caught.exception.message)

    def test_a_codage_names_an_encoding_beside_it_that_has_none_of_its_own(self):
        for codage, message in (("missing", "is not a codage beside"), ("script", "is not a codage beside"),
                                ("standard", "is not a codage beside")):
            path = self.write({"name": "bad", "fonts": ["f"], "codage": codage, "rows": [["a", "A"]]})
            with self.assertRaises(E.EncodingError) as caught:
                E.load(path)
            self.assertIn(message, caught.exception.message)


class Command(Case):
    def run_main(self, *argv, stdin=""):
        out, err = io.StringIO(), io.StringIO()
        old = sys.stdin
        sys.stdin = io.StringIO(stdin)
        try:
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                status = E.main(list(argv))
        finally:
            sys.stdin = old
        return status, out.getvalue(), err.getvalue()

    def test_a_font_with_no_encoding_is_addressed_by_its_slug(self):
        with mock.patch.object(E, "names", return_value=[]):
            status, out, _ = self.run_main("--font", "teng-chou", "\u27e6LATIN_SMALL_LETTER_A\u27e7")
            self.assertEqual((status, out), (0, E.mark("\u27e6") + "a" + E.mark("\u27e7") + "\n"))
            status, out, err = self.run_main("--font", "teng-chou", "a")
            self.assertEqual((status, out), (1, ""))
            self.assertIn("the `teng-chou` font has no encoding", err)

    def test_teng_chou_codes_separate_a_character_from_a_sign_by_case(self):
        enc = E.load("teng-chou")
        both = E.encode(enc, "\u27e6KA ka   TALLY5\u27e7")
        points = [c for c in both if not E.is_mark(c)]
        self.assertEqual(len(points), 3)
        self.assertNotEqual(points[0], points[1])
        self.assertNotIn(" ", both)
        self.assertEqual(E.decode(enc, both), "\u27e6KA ka TALLY5\u27e7")
        with self.assertRaises(E.EncodingError):
            E.encode(enc, "\u27e6NOSUCHCODE\u27e7")

    def test_the_names_are_encodings_and_the_codages_are_listed_apart(self):
        self.assertIn("zethu", E.names())
        self.assertNotIn("zethu-mdc", E.names())
        self.assertEqual(E.names(kind="codage"), ["chalish-ceremonial", "chalish-common", "teng-chou-codes", "zethu-mdc"])
        self.assertEqual(E.for_font("khelathi-zethu-glyphs").name, "zethu")

    def test_encode_and_decode_by_path(self):
        path = self.write(
            {"name": "test", "fonts": ["f"], "rows": [["a", "\U000F0230"]]}
        )
        self.assertEqual(self.run_main("--encoding", path, "aa"), (0, "\U000F0230\U000F0230\n", ""))
        self.assertEqual(self.run_main("--encoding", path, "--codepoints", "a"), (0, "U+F0230\n", ""))
        self.assertEqual(self.run_main("--encoding", path, "-", stdin="a\n\n a"), (0, "\U000F0230 \U000F0230", ""))
        self.assertEqual(self.run_main("--encoding", path, "--decode", "-", stdin="\U000F0230 "), (0, "a ", ""))

    def test_a_refused_character_exits_non_zero_at_its_position(self):
        path = self.write({"name": "test", "fonts": ["f"], "rows": [["a", "A"]]})
        text = os.path.join(self.dir, "note.txt")
        with open(text, "w", encoding="utf-8") as handle:
            handle.write("aa;")
        status, out, err = self.run_main("--encoding", path, "--file", text)
        self.assertEqual((status, out), (1, ""))
        self.assertEqual(err, f'{E._shown(text)}:1:3: error: ";" (U+003B) is not in the `test` encoding\n')
        status, _, err = self.run_main("--encoding", path, "a?")
        self.assertEqual((status, err), (1, '<text>:1:2: error: "?" (U+003F) is not in the `test` encoding\n'))

    def test_a_faulty_file_exits_non_zero(self):
        path = self.write({"name": "test", "rows": []})
        status, _, err = self.run_main("--encoding", path, "a")
        self.assertEqual(status, 1)
        self.assertIn("error: needs `fonts`", err)


if __name__ == "__main__":
    unittest.main()
