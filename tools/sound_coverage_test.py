# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Mutation proofs for sound coverage against temporary copies of a real font."""

import contextlib
import io
import json
import os
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont

import sound_coverage as guard


class CoverageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.points = guard.guide_points(Path(os.environ["SOUND_COVERAGE_GUIDE"]))
        registry = json.loads((guard.ROOT / "fonts.json").read_text())
        cls.files = guard.sound_files(registry)
        cls.file = next(file for file in cls.files if file.endswith(".ttf"))
        cls.rows = cls.files[cls.file]

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "copy.ttf"
        with TTFont(guard.ROOT / self.file) as font:
            for table in font["cmap"].tables:
                if table.isUnicode() and table.format in (12, 13):
                    for point in self.points:
                        table.cmap[point] = "ignorable"
            font.save(self.path)

    def mutate(self, change):
        with TTFont(self.path) as font:
            change(font)
            font.save(self.path)
        return guard.check_font(self.path, self.points, self.rows)

    def test_complete_copy(self):
        self.assertEqual(guard.check_font(self.path, self.points, self.rows), [])

    def test_missing_mapping(self):
        point = self.points[0]
        def remove(font):
            for table in font["cmap"].tables:
                if table.isUnicode():
                    table.cmap.pop(point, None)
        self.assertTrue(any("has no mapped glyph" in item for item in self.mutate(remove)))

    def test_nonzero_advance(self):
        def widen(font):
            font["hmtx"].metrics["ignorable"] = (50, 0)
        self.assertTrue(any("nonzero advance" in item for item in self.mutate(widen)))

    def test_ink(self):
        def draw(font):
            pen = TTGlyphPen(None)
            pen.moveTo((0, 0)); pen.lineTo((40, 0)); pen.lineTo((40, 40)); pen.closePath()
            font["glyf"]["ignorable"] = pen.glyph()
        self.assertTrue(any("has ink" in item for item in self.mutate(draw)))

    def test_missing_visible(self):
        row = self.rows[0]
        point = int(row["codepoint"][2:], 16)
        def remove(font):
            for table in font["cmap"].tables:
                if table.isUnicode():
                    table.cmap.pop(point, None)
        self.assertTrue(any("lacks declared visible glyph" in item for item in self.mutate(remove)))

    def test_guide_inventory_is_checked_independent_of_order(self):
        import yaml

        source = Path(os.environ["SOUND_COVERAGE_GUIDE"]).read_text()
        front = yaml.safe_load(source[4:].split("\n---", 1)[0])
        rows = front["data"]["sounds"]["letters"]
        rows.reverse()
        guide = Path(self.temp.name) / "guide.md"
        guide.write_text("---\n" + yaml.safe_dump(front, allow_unicode=True) + "---\n")
        self.assertEqual(set(guard.guide_points(guide)), set(self.points))
        rows.pop()
        guide.write_text("---\n" + yaml.safe_dump(front, allow_unicode=True) + "---\n")
        with self.assertRaisesRegex(ValueError, "omits shared sound"):
            guard.guide_points(guide)

    def test_source_glyph_is_required_when_manifest_row_is_missing(self):
        registry = json.loads((guard.ROOT / "fonts.json").read_text())
        target = next(v for v in registry["families"] if v["files"]["ttf"] == self.file)
        row = target["codepoints"].pop(0)
        point = int(row["codepoint"][2:], 16)
        def remove(font):
            for table in font["cmap"].tables:
                if table.isUnicode():
                    table.cmap.pop(point, None)
        with TTFont(self.path) as font:
            remove(font)
            font.save(self.path)
        rows = guard.sound_files(registry)[self.file]
        findings = guard.check_font(self.path, self.points, rows)
        self.assertTrue(any("lacks declared visible glyph" in item for item in findings))

    def test_invalid_font_reports_file_first(self):
        root = Path(self.temp.name)
        (root / "fonts.json").write_text("{}")
        (root / "broken.ttf").write_bytes(b"not a font")
        stderr = io.StringIO()
        with (
            patch.object(guard, "ROOT", root),
            patch.object(guard, "guide_points", return_value=self.points),
            patch.object(guard, "sound_files", return_value={"broken.ttf": []}),
            patch("sys.argv", ["sound_coverage.py", "guide.md"]),
            contextlib.redirect_stderr(stderr),
        ):
            self.assertEqual(guard.main(), 1)
        self.assertTrue(stderr.getvalue().startswith("broken.ttf: error: "))

    def test_classification_is_closed(self):
        registry = json.loads((guard.ROOT / "fonts.json").read_text())
        with self.assertRaises(ValueError):
            guard.sound_files(registry, {"unknown": {"scriptKind": "other"}})
        registry["families"].pop()
        with self.assertRaisesRegex(ValueError, "variants absent"):
            guard.sound_files(registry)


if __name__ == "__main__":
    unittest.main()
