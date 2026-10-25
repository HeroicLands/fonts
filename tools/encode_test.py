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
        path = os.path.join(self.dir, f"{name}.json")
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(text if text is not None else json.dumps(data, ensure_ascii=False, indent=4))
        return path

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
            [["a", "A"], ["ab", "X"]],
            faces={"face-two": {"rows": [["a", "2"]]}},
        )
        self.assertEqual(E.encode(enc, "ab"), "X")
        self.assertEqual(E.encode(enc, "ab", face="face-one"), "X")
        self.assertEqual(E.encode(enc, "ab", face="face-two"), "2b")
        self.assertEqual(E.decode(enc, "2b", face="face-two"), "ab")

    def test_a_face_the_encoding_does_not_serve_is_refused(self):
        enc = self.encoding([["a", "A"]])
        with self.assertRaises(E.EncodingError):
            E.encode(enc, "a", face="face-three")


class PassThrough(Case):
    def test_an_unmatched_character_passes_through(self):
        enc = self.encoding([["a", "A"]])
        self.assertEqual(E.encode(enc, "a b!"), "A b!")
        self.assertEqual(E.decode(enc, "A b!"), "a b!")


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
        self.assertEqual(E.encode(enc, "a-b"), "A\U000E010DB")
        self.assertEqual(E.decode(enc, "A\U000E010DB"), "a-b")

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
        self.assertEqual(E.decode(enc, "2B"), "2b")


class Marks(Case):
    def test_printable_ascii_is_a_variation_selector_of_its_own(self):
        self.assertEqual(E.mark("a"), "\U000E0141")
        self.assertEqual(E.mark(" -"), "\U000E0100\U000E010D")
        self.assertTrue(all(E.is_mark(c) for c in E.mark("~ {")))

    def test_any_other_character_is_spelled_by_its_code_point(self):
        self.assertEqual(E.mark("á"), "".join(chr(0xE0100 + ord(c) - 0x20) for c in "{e1}"))
        self.assertEqual(E.mark("{"), "".join(chr(0xE0100 + ord(c) - 0x20) for c in "{7b}"))
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
            '{\n    "name": "bad",\n    "fonts": ["face"],\n    "rows": [\n'
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
                "`name`, `fonts`, `vowels`, `rows`, `faces`",
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
        text = '{"name": "bad", "fonts": ["f"], "rows": [["a", "A"]],\n "separators": ["-"], "decode": []}'
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
        text = '{"name": "bad", "fonts": ["f"], "rows": [\n ["a", ""],\n {"from": "b", "to": ""}]}'
        path = self.write(None, name="bad", text=text)
        shown = E._shown(path)
        message = (
            "error: writes nothing; a row that draws nothing writes the mark of its `from`, "
            "so that decoding restores it"
        )
        self.assertEqual(self.faults(path), [f"{shown}:2:8: {message}", f"{shown}:3:22: {message}"])

    def test_two_froms_writing_one_output_are_refused_at_the_later(self):
        text = '{"name": "bad", "fonts": ["f"], "rows": [\n ["a", "X"],\n ["A", "X"],\n ["b", "B"]]}'
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

    def test_encode_and_decode_by_path(self):
        path = self.write({"name": "test", "fonts": ["f"], "rows": [["a", "\U000F0230"]]})
        self.assertEqual(self.run_main("--encoding", path, "aa"), (0, "\U000F0230\U000F0230\n", ""))
        self.assertEqual(self.run_main("--encoding", path, "--codepoints", "a"), (0, "U+F0230\n", ""))
        self.assertEqual(self.run_main("--encoding", path, "--decode", "-", stdin="\U000F0230\n"), (0, "a\n", ""))

    def test_a_faulty_file_exits_non_zero(self):
        path = self.write({"name": "test", "rows": []})
        status, _, err = self.run_main("--encoding", path, "a")
        self.assertEqual(status, 1)
        self.assertIn("error: needs `fonts`", err)


if __name__ == "__main__":
    unittest.main()
