# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""CI rejection checks for source identities and compiled layout filtering."""

from io import BytesIO
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from fontTools.feaLib.builder import Builder, addOpenTypeFeaturesFromString
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont

import shared_metadata_proof as proof
from layout_evidence import install_capture, tables, value
from shared_metadata_proof import (Face, Report, metadata_cmap, metadata_geometry,
                                   select_capture, verify_metadata_scope, verify_scope)


SOURCE = """
languagesystem DFLT dflt;
feature ccmp {
 lookup ccmp_ignorable {
  sub ignorable by ignorable.sub;
  METADATA_SUBSTITUTION
 } ccmp_ignorable;
 lookup ccmp_catch {
  METADATA_FILTER
  ignore sub a grave';
  sub grave' by notdef.box;
 } ccmp_catch;
} ccmp;
table GDEF {
 GlyphClassDef [a ignorable ignorable.sub notdef.box], , [grave METADATA_MARK], ;
} GDEF;
"""


def font(metadata, extra=""):
    order = [".notdef", "a", "grave", "notdef.box", "ignorable", "ignorable.sub"]
    if metadata:
        order += ["shared.invisible", "shared.invisible.sub"]
    builder = FontBuilder(1000, isTTF=True)
    builder.setupGlyphOrder(order)
    builder.setupCharacterMap({97: "a"})
    builder.setupGlyf({name: TTGlyphPen(None).glyph() for name in order})
    builder.setupHorizontalMetrics({name: (0, 0) for name in order})
    builder.setupHorizontalHeader(ascent=800, descent=-200)
    builder.setupNameTable({"familyName": "Proof", "styleName": "Regular"})
    builder.setupOS2()
    builder.setupPost()
    source = SOURCE.replace("METADATA_SUBSTITUTION", "sub shared.invisible by shared.invisible.sub;" if metadata else "")
    source = source.replace("METADATA_FILTER", "lookupflag UseMarkFilteringSet [grave];" if metadata else "")
    source = source.replace("METADATA_MARK", "shared.invisible.sub" if metadata else "")
    addOpenTypeFeaturesFromString(builder.font, source + extra)
    return SimpleNamespace(font=builder.font, order=order, path=Path("Proof.ttf"))


class LookupProofTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name)
        self.before = font(False)
        with patch.object(Builder, "build", Builder.build):
            install_capture(self.path / "capture")
            self.after = font(True)
        self.capture = json.loads((self.path / "capture/1.json").read_text())
        self.report = Report(self.path / "report")
        self.addCleanup(self.report.stream.close)

    def verify(self):
        verify_scope(self.before, self.after, self.capture, "SemaronKuriale", self.report)

    def test_real_source_mapping_accepts_scoped_filter(self):
        self.verify()
        self.assertFalse(self.report.failures)
        self.assertGreater(self.report.counts["lookup-filter-scope"], 0)

    def test_capture_keeps_compiled_tables_unchanged(self):
        ordinary = font(True)
        self.assertNotIn("Debg", self.after.font)
        for tag in ("GSUB", "GPOS", "GDEF"):
            if tag in ordinary.font:
                self.assertEqual(ordinary.font[tag].compile(ordinary.font), self.after.font[tag].compile(self.after.font))

    def test_normalizing_ligatures_keeps_comparison_objects_unchanged(self):
        candidate = font(True, "feature liga { sub a a by notdef.box; } liga;")
        before = value(candidate.font["GSUB"].table)
        tables(candidate.font)
        self.assertEqual(before, value(candidate.font["GSUB"].table))

    def test_decoded_ligatures_keep_their_baseline_identity(self):
        extra = "feature liga { sub a a by notdef.box; } liga;"
        self.before = font(False, extra)
        with patch.object(Builder, "build", Builder.build):
            install_capture(self.path / "ligature-capture")
            self.after = font(True, extra)
        self.capture = json.loads((self.path / "ligature-capture/1.json").read_text())
        for candidate in (self.before, self.after):
            raw = BytesIO()
            candidate.font.save(raw)
            candidate.font = TTFont(BytesIO(raw.getvalue()))
            for tag in ("GSUB", "GPOS", "GDEF"):
                if tag in candidate.font:
                    candidate.font[tag].table.ensureDecompiled(recurse=True)
        self.verify()
        self.assertFalse(self.report.failures)

    def test_intermediate_capture_cannot_replace_final_tables(self):
        partial = {**self.capture, "tables": {"GSUB": self.capture["tables"]["GSUB"]}}
        path = self.path / "capture/2.json"
        path.write_text(json.dumps(partial))
        capture = select_capture((self.path / "capture").glob("*.json"), tables(self.after.font), self.report, "Proof")
        self.assertEqual(capture, self.capture)
        self.assertFalse(self.report.failures)

    def test_analysis_capture_without_final_tables_fails(self):
        partial = {**self.capture, "tables": {"GSUB": self.capture["tables"]["GSUB"]}}
        path = self.path / "partial.json"
        path.write_text(json.dumps(partial))
        self.assertIsNone(select_capture([path], tables(self.after.font), self.report, "Proof"))
        self.assertEqual(self.report.failures["matching-compilation-capture"], 1)

    def test_ambiguous_final_captures_fail(self):
        path = self.path / "capture/2.json"
        path.write_text(json.dumps(self.capture))
        self.assertIsNone(select_capture((self.path / "capture").glob("*.json"), tables(self.after.font), self.report, "Proof"))
        self.assertEqual(self.report.failures["matching-compilation-capture"], 1)

    def test_compiled_font_change_rejects_capture(self):
        self.after.font["GSUB"].table.LookupList.Lookup[0].LookupFlag = 8
        self.verify()
        self.assertEqual(self.report.failures["compiled-capture"], 1)

    def test_filter_outside_source_scope_fails(self):
        self.after.font["GSUB"].table.LookupList.Lookup[0].LookupFlag = 8
        self.capture["tables"] = tables(self.after.font)
        self.verify()
        self.assertGreater(self.report.failures["lookup-filter-scope"], 0)

    def test_missing_compiler_identity_fails(self):
        self.capture["lookups"]["GSUB"].pop("0")
        self.verify()
        self.assertGreater(self.report.failures["complete-source-map"], 0)
        self.assertGreater(self.report.failures["source-identity"], 0)

    def test_context_rule_change_fails(self):
        lookup = self.after.font["GSUB"].table.LookupList.Lookup[0]
        lookup.SubTable[0].mapping["ignorable"] = "a"
        self.capture["tables"] = tables(self.after.font)
        self.verify()
        self.assertGreater(self.report.failures["lookup-semantics"], 0)

    def test_metadata_substitution_to_visible_glyph_fails(self):
        lookup = self.after.font["GSUB"].table.LookupList.Lookup[0]
        lookup.SubTable[0].mapping["shared.invisible"] = "a"
        self.capture["tables"] = tables(self.after.font)
        self.verify()
        self.assertGreater(self.report.failures["metadata-rule-scope"], 0)

    def test_missing_expected_scope_fails(self):
        for row in self.capture["lookups"]["GSUB"].values():
            row["blocks"] = []
        self.verify()
        self.assertGreater(self.report.failures["nonempty-source-scope"], 0)


class PermanentMetadataTests(unittest.TestCase):
    """The permanent contract permits ordinary font changes and rejects metadata damage."""

    def verify(self):
        verify_metadata_scope(self.after, self.capture, "SemaronKuriale", self.report)

    setUp = LookupProofTests.setUp

    test_compiled_font_change_rejects_capture = LookupProofTests.test_compiled_font_change_rejects_capture
    test_missing_compiler_identity_fails = LookupProofTests.test_missing_compiler_identity_fails
    test_metadata_substitution_to_visible_glyph_fails = LookupProofTests.test_metadata_substitution_to_visible_glyph_fails
    test_missing_expected_scope_fails = LookupProofTests.test_missing_expected_scope_fails

    def test_ordinary_glyph_and_lookup_changes_are_not_a_transition(self):
        with patch.object(Builder, "build", Builder.build):
            install_capture(self.path / "ordinary-capture")
            self.after = font(True, "feature liga { sub a a by notdef.box; } liga;")
        # A new visible glyph with its own cmap, ink and advance is ordinary font work.
        added = "new.visible"
        order = [*self.after.order, added]
        pen = TTGlyphPen(None)
        pen.moveTo((0, 0)); pen.lineTo((10, 0)); pen.lineTo((10, 10)); pen.closePath()
        self.after.font["glyf"][added] = pen.glyph()
        self.after.font.setGlyphOrder(order)
        self.after.order = order
        self.after.font["hmtx"].metrics[added] = (500, 0)
        for table in self.after.font["cmap"].tables:
            table.cmap[98] = added
        self.capture = json.loads((self.path / "ordinary-capture/1.json").read_text())
        self.verify()
        path = self.path / "ordinary.ttf"
        self.after.font.save(path)
        metadata_geometry(Face(path), self.report, {})
        self.assertFalse(self.report.failures)

    def test_selected_filter_must_exclude_metadata_and_keep_visible_marks(self):
        lookup = self.after.font["GSUB"].table.LookupList.Lookup[1]
        lookup.LookupFlag = 8
        self.capture["tables"] = tables(self.after.font)
        self.verify()
        self.assertGreater(self.report.failures["lookup-filter-scope"], 0)

    def test_metadata_output_class_is_required(self):
        self.after.font["GDEF"].table.GlyphClassDef.classDefs["shared.invisible.sub"] = 1
        self.capture["tables"] = tables(self.after.font)
        self.verify()
        self.assertGreater(self.report.failures["metadata-classes"], 0)

    def test_metadata_input_cannot_be_a_mark(self):
        self.after.font["GDEF"].table.GlyphClassDef.classDefs["shared.invisible"] = 3
        self.capture["tables"] = tables(self.after.font)
        self.verify()
        self.assertGreater(self.report.failures["metadata-classes"], 0)

    def test_metadata_width_is_rejected(self):
        self.after.font["hmtx"].metrics["shared.invisible.sub"] = (1, 0)
        path = self.path / "wide.ttf"
        self.after.font.save(path)
        metadata_geometry(Face(path), self.report, {})
        self.assertGreater(self.report.failures["empty-metadata-glyph"], 0)

    def test_metadata_ink_is_rejected(self):
        pen = TTGlyphPen(None)
        pen.moveTo((0, 0)); pen.lineTo((10, 0)); pen.lineTo((10, 10)); pen.closePath()
        self.after.font["glyf"]["shared.invisible.sub"] = pen.glyph()
        path = self.path / "ink.ttf"
        self.after.font.save(path)
        metadata_geometry(Face(path), self.report, {})
        self.assertGreater(self.report.failures["empty-metadata-glyph"], 0)

    def test_unrelated_cmap_addition_is_allowed(self):
        face = SimpleNamespace(cmap={1: "shared.invisible", 2: "a", 3: "new.visible"})
        metadata_cmap(face, {1}, self.report, {})
        self.assertFalse(self.report.failures)

    def test_visible_character_cannot_map_to_metadata(self):
        face = SimpleNamespace(cmap={1: "shared.invisible", 2: "shared.invisible.sub"})
        metadata_cmap(face, {1}, self.report, {})
        self.assertGreater(self.report.failures["exclusive-metadata-cmap"], 0)

    def test_required_mapping_cannot_use_old_ignorable(self):
        face = SimpleNamespace(cmap={1: "ignorable"})
        metadata_cmap(face, {1}, self.report, {})
        self.assertGreater(self.report.failures["shared-cmap"], 0)


class ProofModeTests(unittest.TestCase):
    def test_permanent_mode_does_not_load_the_transition_baseline(self):
        self.check_mode(False)

    def test_explicit_transition_runs_baseline_validation(self):
        self.check_mode(True)

    def test_baseline_failure_is_not_retried_as_permanent_success(self):
        self.check_mode(True, invalid=True)

    def check_mode(self, transition, invalid=False):
        with TemporaryDirectory() as temp:
            out = Path(temp) / "report"
            args = ["shared_metadata_proof.py", "--built", "fonts", "--layout", "layout", "--out", str(out)]
            if transition:
                args += ["--baseline", "baseline/fonts"]
            def validate(args, report):
                if invalid:
                    raise ValueError("baseline hash mismatch")
            with (patch("sys.argv", args), patch.object(proof, "registry", return_value=({}, {})),
                  patch.object(proof, "verify_baseline", side_effect=validate) as baseline,
                  patch.object(proof, "prove_face") as face):
                self.assertEqual(proof.main(), int(invalid))
            self.assertEqual(baseline.call_count, int(transition))
            self.assertEqual(face.call_count, 0 if invalid else len(proof.FIXTURES))
            report = json.loads((out / "report.json").read_text())
            self.assertEqual(report["mode"], "transition" if transition else "metadata")
            self.assertEqual(bool(report["failures"]), invalid)


ROUTING_SOURCE = """
lookup sub_plain { lookupflag 0; sub a by notdef.box; } sub_plain;
lookup sub_filtered { lookupflag IgnoreMarks; sub a by notdef.box; } sub_filtered;
feature liga { lookup sub_plain; } liga;
feature calt {
 lookup sub_context_plain { sub grave a' lookup sub_plain; } sub_context_plain;
 lookup sub_context_filtered { sub a a' lookup sub_filtered; } sub_context_filtered;
} calt;
lookup pos_plain { lookupflag 0; pos a 17; } pos_plain;
lookup pos_filtered { lookupflag IgnoreMarks; pos a 17; } pos_filtered;
feature kern { lookup pos_plain; } kern;
feature dist {
 lookup pos_context_plain { pos grave a' lookup pos_plain; } pos_context_plain;
 lookup pos_context_filtered { pos a a' lookup pos_filtered; } pos_context_filtered;
} dist;
"""


def rewrite_lookup_references(item, indices):
    if isinstance(item, (list, tuple)):
        for child in item:
            rewrite_lookup_references(child, indices)
    elif isinstance(item, dict):
        for child in item.values():
            rewrite_lookup_references(child, indices)
    elif hasattr(item, "__dict__"):
        for key, child in vars(item).items():
            if key == "LookupListIndex":
                setattr(item, key, [indices[i] for i in child] if isinstance(child, list) else indices[child])
            else:
                rewrite_lookup_references(child, indices)


class LookupRoutingProofTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name)
        self.before = font(False, ROUTING_SOURCE)
        with patch.object(Builder, "build", Builder.build):
            install_capture(self.path / "capture")
            self.after = font(True, ROUTING_SOURCE)
        self.capture = json.loads((self.path / "capture/1.json").read_text())
        self.report = Report(self.path / "report")
        self.addCleanup(self.report.stream.close)

    def index(self, tag, name):
        matches = [int(index) for index, row in self.capture["lookups"][tag].items() if row["name"] == name]
        self.assertEqual(len(matches), 1, (tag, name))
        return matches[0]

    def verify(self):
        self.capture["tables"] = tables(self.after.font)
        verify_scope(self.before, self.after, self.capture, "SemaronKuriale", self.report)

    def swap_feature(self, tag, feature, name):
        records = self.after.font[tag].table.FeatureList.FeatureRecord
        matches = [row.Feature for row in records if row.FeatureTag == feature]
        self.assertEqual(len(matches), 1)
        self.assertEqual(len(matches[0].LookupListIndex), 1)
        matches[0].LookupListIndex = [self.index(tag, name)]
        self.verify()
        self.assertEqual(self.report.failures["lookup-filter-scope"], 0)
        self.assertGreater(self.report.failures["feature-routing"], 0)

    def swap_context(self, tag, prefix):
        lookups = self.after.font[tag].table.LookupList.Lookup
        old = self.index(tag, prefix + "_plain")
        new = self.index(tag, prefix + "_filtered")
        rewrite_lookup_references(lookups[self.index(tag, prefix + "_context_plain")],
                                  {index: new if index == old else index for index in range(len(lookups))})
        self.verify()
        self.assertEqual(self.report.failures["lookup-filter-scope"], 0)
        self.assertGreater(self.report.failures["lookup-routing"], 0)

    def test_equal_rules_with_different_filters_are_valid(self):
        self.verify()
        self.assertFalse(self.report.failures)

    def test_gsub_feature_cannot_switch_filter(self):
        self.swap_feature("GSUB", "liga", "sub_filtered")

    def test_gpos_feature_cannot_switch_filter(self):
        self.swap_feature("GPOS", "kern", "pos_filtered")

    def test_gsub_context_cannot_switch_filter(self):
        self.swap_context("GSUB", "sub")

    def test_gpos_context_cannot_switch_filter(self):
        self.swap_context("GPOS", "pos")

    def test_consistent_lookup_renumbering_preserves_routing(self):
        for tag in ("GSUB", "GPOS"):
            table = self.after.font[tag].table
            lookups = table.LookupList.Lookup
            indices = {old: len(lookups) - old - 1 for old in range(len(lookups))}
            rewrite_lookup_references(table.FeatureList, indices)
            rewrite_lookup_references(lookups, indices)
            table.LookupList.Lookup = list(reversed(lookups))
            self.capture["lookups"][tag] = {str(indices[int(index)]): row
                                             for index, row in self.capture["lookups"][tag].items()}
        self.verify()
        self.assertFalse(self.report.failures)
        self.assertGreater(self.report.counts["lookup-routing"], 0)

    def test_approved_change_with_ambiguous_original_filter_fails(self):
        row = self.capture["lookups"]["GSUB"][str(self.index("GSUB", "sub_plain"))]
        row["blocks"] = [["LookupBlock", "ccmp_catch"]]
        self.verify()
        self.assertGreater(self.report.failures["unambiguous-baseline-filter"], 0)


if __name__ == "__main__":
    unittest.main()
