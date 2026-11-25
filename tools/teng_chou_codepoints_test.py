# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""The Teng Chou code points stay put as characters are added, and no two characters share a formula."""

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "teng-chou"))
import characters  # noqa: E402
import codepoint_order  # noqa: E402


def table(extra=()):
    chars = characters.CHARACTERS + [characters.Character(m, "test", f) for m, f in extra]
    with patch.object(characters, "CHARACTERS", chars):
        _, _, groups = codepoint_order._teng_chou()
    return {glyph: start + i for _, start, glyphs in groups for i, glyph in enumerate(glyphs)}


class PinningTest(unittest.TestCase):
    def test_tally_stands_at_its_code_points(self):
        rows = table()
        stages = [g for g in rows if g.startswith("tc.tally")]
        self.assertEqual(sorted(rows[g] for g in stages), list(range(0xF10D5, 0xF10DA)))

    def test_added_characters_take_code_points_from_f10da(self):
        before = table()
        after = table([("zz1", "{fire}"), ("zz2", "{water}")])
        self.assertEqual({g: cp for g, cp in after.items() if g in before}, before)
        self.assertEqual(after["tc.zz1"], 0xF10DA)
        self.assertEqual(after["tc.zz2"], 0xF10DB)

    def test_characters_before_the_tally_keep_their_order(self):
        rows = table()
        first = characters.CHARACTERS[0].glyph
        last_below = characters.CHARACTERS[0xF10D4 - 0xF1000].glyph
        self.assertEqual(rows[first], 0xF1000)
        self.assertEqual(rows[last_below], 0xF10D4)


class FormulaTest(unittest.TestCase):
    def test_a_shared_formula_names_both_morphemes(self):
        rows = [("aa", "one", "{fire}"), ("bb", "two", "{fire}")]
        with patch.object(characters, "ROWS", rows), self.assertRaisesRegex(ValueError, r"characters\.py:\d+:1: error: .*aa and bb"):
            characters._build()

    def test_the_lexicon_has_no_shared_formula(self):
        formulas = [c.formula for c in characters.CHARACTERS]
        self.assertEqual(len(formulas), len(set(formulas)))


if __name__ == "__main__":
    unittest.main()
