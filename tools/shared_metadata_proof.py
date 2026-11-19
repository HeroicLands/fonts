# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Prove metadata transparency, control preservation and compiled lookup scope in CI."""

import argparse
from collections import Counter, defaultdict, deque
import hashlib
from io import BytesIO
import json
from pathlib import Path
import subprocess
import sys
import traceback

from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.ttLib import TTFont
import uharfbuzz as hb

import codes
from layout_evidence import PIN, digest, tables, value
from write_css import FAMILIES

ROOT = Path(__file__).resolve().parent.parent
INPUT, OUTPUT = "shared.invisible", "shared.invisible.sub"
ADDITIONS = frozenset((INPUT, OUTPUT, INPUT + ".crown", OUTPUT + ".crown"))
FIXTURES = {
    "PirzathCarved": "pirzath", "PirzathHand": "pirzath-hand",
    "QalezuHand": "qalezu-hand", "SemaronKuriale": "semaron-kuriale",
    "VedyaksharaClassical": "vedyakshara", "HelonikaBook": "helonika",
    "Veldikko": "veldikko", "ThuravarkCarved": "thuravark-carved",
}
# These are source blocks, never compiled lookup positions.
SCOPES = {
    "PirzathCarved": {("FeatureBlock", "rlig"), ("FeatureBlock", "kern")},
    "PirzathHand": {("FeatureBlock", "liga"), ("FeatureBlock", "rlig")},
    "QalezuHand": {("FeatureBlock", "rlig")},
    "SemaronKuriale": {("LookupBlock", "ccmp_catch")},
    "VedyaksharaClassical": {("LookupBlock", name) for name in
        ("softdot", "fused", "rhalf", "rfinal", "rfoot", "half", "final", "vowels", "strays")},
    "HelonikaBook": {("LookupBlock", "strays"), ("FeatureBlock", "kern")},
    "Veldikko": {("LookupBlock", "vowels")},
    "ThuravarkCarved": {("LookupBlock", "ccmp_acute"), ("FeatureBlock", "ss01"), ("LookupBlock", "crown")},
}
REGISTRY = """
import {SHARED_SOUNDS, SHARED_SOUND_CONTROLS} from '@heroiclands/package-build/engine/encoding-standard';
console.log(JSON.stringify({
 sounds: Object.values(SHARED_SOUNDS).map(x => x.invisible.codePointAt(0)),
 controls: Object.fromEntries(Object.entries(SHARED_SOUND_CONTROLS).map(([k,v]) => [k,v.codePointAt(0)]))
}));
"""


class Report:
    def __init__(self, out, mode="metadata"):
        self.mode = mode
        self.out = out
        out.mkdir(parents=True, exist_ok=True)
        self.stream = (out / "failures.jsonl").open("w")
        self.counts = Counter()
        self.failures = Counter()
        self.faces = {}

    def check(self, condition, kind, **detail):
        self.counts[kind] += 1
        if not condition:
            self.failures[kind] += 1
            self.stream.write(json.dumps({"check": kind, **detail}) + "\n")
            self.stream.flush()
        return condition

    def finish(self):
        self.stream.close()
        result = {"mode": self.mode, "checks": dict(self.counts), "failures": dict(self.failures), "faces": self.faces}
        (self.out / "report.json").write_text(json.dumps(result, indent=2) + "\n")
        print(f"Shared metadata proof: {sum(self.counts.values())} checks, {sum(self.failures.values())} failures")
        if self.failures:
            print("tools/shared_metadata_proof.py: error: shared metadata proof fails; see shaping/failures.jsonl", file=sys.stderr)
        return bool(self.failures)


def registry():
    data = json.loads(subprocess.check_output(["node", "--input-type=module", "-e", REGISTRY], cwd=ROOT, text=True))
    controls = data["controls"]
    points = {p: "sound" for p in data["sounds"]}
    points.update({p: name for name, p in controls.items() if name != "legacyShort"})
    if not data["sounds"] or not controls or len(points) != len(data["sounds"]) + len(controls) - 1:
        raise ValueError("empty or overlapping shared metadata registry")
    return points, controls


def fixtures(family):
    source = ROOT / "tools" / FIXTURES[family] / "fixtures.json"
    rows = json.loads(source.read_text())
    for kind in ("fixtures", "spaces", "marks", "ignorables"):
        for index, row in enumerate(rows.get(kind, [])):
            sequence = row if isinstance(row, str) else row.get("codes")
            if sequence:
                features = {} if isinstance(row, str) else {name: True for name in row.get("features", [])}
                yield {"fixture": f"{kind}[{index}]", "codes": sequence, "features": features,
                       "text": codes.text(codes.SCRIPTS[family + "-Regular"], sequence)}


class Face:
    def __init__(self, path):
        self.path = path
        self.font = TTFont(path)
        self.order = self.font.getGlyphOrder()
        self.cmap = self.font.getBestCmap()
        # HarfBuzz consumes sfnt bytes; FontTools and brotli decode WOFF2.
        self.font.flavor = None
        raw = BytesIO()
        self.font.save(raw)
        self.hb = hb.Font(hb.Face(raw.getvalue()))
        self.glyphs = self.font.getGlyphSet()
        for tag in ("GSUB", "GPOS", "GDEF"):
            if tag in self.font:
                self.font[tag].table.ensureDecompiled(recurse=True)

    def shape(self, text, direction, features):
        buffer = hb.Buffer()
        buffer.add_str(text)
        buffer.direction = direction
        buffer.script = "Zyyy"
        buffer.guess_segment_properties()
        hb.shape(self.hb, buffer, features)
        return [(self.order[g.codepoint], p.x_advance, p.y_advance, p.x_offset, p.y_offset)
                for g, p in zip(buffer.glyph_infos, buffer.glyph_positions)]

    def outline(self, name):
        pen = DecomposingRecordingPen(self.glyphs)
        self.glyphs[name].draw(pen)
        return pen.value


def classes(font, key="GlyphClassDef"):
    table = getattr(font["GDEF"].table, key, None) if "GDEF" in font else None
    return table.classDefs if table is not None else {}


def mark_sets(font):
    table = getattr(font["GDEF"].table, "MarkGlyphSetsDef", None) if "GDEF" in font else None
    return [frozenset(coverage.glyphs) for coverage in table.Coverage] if table else []


def filtering(font, lookup):
    flag = lookup.LookupFlag
    marks = mark_sets(font)
    return (flag, sorted(marks[lookup.MarkFilteringSet]) if flag & 16 else None)


def lookup_signatures(font, tag, filters=None):
    lookups = font[tag].table.LookupList.Lookup if tag in font else []
    cache, active = {}, set()

    def signature(index):
        if isinstance(index, list):
            return [signature(i) for i in index]
        if index in active:
            raise ValueError(f"{tag}: recursive contextual lookup cannot be proved")
        if index not in cache:
            active.add(index)
            rules = value(lookups[index], ("LookupFlag", "MarkFilteringSet"), signature, ADDITIONS)
            cache[index] = digest(rules if filters is None else {"rules": rules, "filter": filters[index]})
            active.remove(index)
        return cache[index]

    return lookups, signature


def metadata_references(item):
    if isinstance(item, str):
        return {item} & ADDITIONS
    if isinstance(item, (list, tuple)):
        return set().union(*(metadata_references(child) for child in item))
    if isinstance(item, dict):
        return set().union(*(metadata_references(child) for pair in item.items() for child in pair))
    if item is None or isinstance(item, (int, float, bool, bytes)):
        return set()
    return metadata_references(vars(item))


def metadata_rules_allowed(lookup, identity, family, tag):
    references = metadata_references(lookup)
    if not references:
        return True
    if tag != "GSUB":
        return False
    blocks = {tuple(block) for block in identity["blocks"]}
    if ("FeatureBlock", "ccmp") in blocks and lookup.LookupType == 1:
        mappings = [getattr(table, "mapping", {}) for table in lookup.SubTable]
        entries = {key: child for mapping in mappings for key, child in mapping.items() if key in ADDITIONS}
        return references == {INPUT, OUTPUT} and entries == {INPUT: OUTPUT}
    if family != "ThuravarkCarved":
        return False
    if ("LookupBlock", "crown_form") in blocks and lookup.LookupType == 1:
        mappings = [getattr(table, "mapping", {}) for table in lookup.SubTable]
        entries = {key: child for mapping in mappings for key, child in mapping.items() if key in ADDITIONS}
        return entries == {INPUT: INPUT + ".crown", OUTPUT: OUTPUT + ".crown"}
    return ("LookupBlock", "crown") in blocks and lookup.LookupType == 6


def verify_scope(before, after, capture, family, report):
    context = {"face": family, "format": after.path.suffix}
    if not report.check(capture["fontTools"] == PIN and capture["tables"] == tables(after.font),
                        "compiled-capture", **context):
        return
    old_classes, new_classes = classes(before.font), classes(after.font)
    report.check(all(new_classes.get(name, 0) != 3 for name in ADDITIONS - {OUTPUT}) and new_classes.get(OUTPUT) == 3,
                 "metadata-classes", **context)
    for name in before.order:
        report.check(old_classes.get(name, 0) == new_classes.get(name, 0), "existing-classes", glyph=name, **context)
    report.check(classes(before.font, "MarkAttachClassDef") == classes(after.font, "MarkAttachClassDef"),
                 "mark-attachment-classes", **context)
    old_sets, new_sets = mark_sets(before.font), mark_sets(after.font)
    report.check(not (Counter(old_sets) - Counter(new_sets)), "retained-mark-sets", **context)
    retained = sorted(name for name, category in old_classes.items() if category == 3)
    expected_filter = (16, retained) if retained else (8, None)
    covered = Counter()
    mapping = []
    for tag in ("GSUB", "GPOS"):
        old, old_signature = lookup_signatures(before.font, tag)
        new, new_signature = lookup_signatures(after.font, tag)
        rows = capture["lookups"].get(tag, {})
        report.check(set(rows) == {str(i) for i in range(len(new))}, "complete-source-map", table=tag, **context)
        by_rules = defaultdict(list)
        old_filters = {index: filtering(before.font, lookup) for index, lookup in enumerate(old)}
        for index in range(len(old)):
            by_rules[old_signature(index)].append(index)
        comparison_filters, identities = {}, {}
        for index, lookup in enumerate(new):
            identity = rows.get(str(index))
            if not report.check(identity is not None, "source-identity", table=tag, lookup=index, **context):
                continue
            report.check(metadata_rules_allowed(lookup, identity, family, tag), "metadata-rule-scope",
                         table=tag, lookup=index, source=identity, **context)
            matches = by_rules[new_signature(index)]
            if not report.check(bool(matches), "lookup-semantics", table=tag, lookup=index, source=identity, **context):
                continue
            selected = SCOPES[family] & {tuple(block) for block in identity["blocks"]}
            covered.update(selected)
            new_filter = filtering(after.font, lookup)
            candidates = {digest(old_filters[i]): old_filters[i] for i in matches}
            # An approved filter change requires one provable original filter.
            # Other lookups retain their own filter, even when their rules coincide.
            if not selected and digest(new_filter) in candidates:
                original_filter = new_filter
            elif report.check(len(candidates) == 1, "unambiguous-baseline-filter", table=tag,
                              lookup=index, source=identity, filters=list(candidates.values()), **context):
                original_filter = next(iter(candidates.values()))
            else:
                continue
            expected = expected_filter if selected else original_filter
            report.check(new_filter == expected, "lookup-filter-scope", table=tag, lookup=index,
                         source=identity, expected=expected, actual=new_filter, **context)
            comparison_filters[index] = original_filter
            identities[index] = {"table": tag, "lookup": index, "source": identity,
                                 "selected": sorted(selected), "filter": new_filter}
        if not report.check(len(comparison_filters) == len(new), "complete-lookup-pairing", table=tag, **context):
            continue
        # Recursive identities retain every referenced lookup's original filter.
        # Only approved local filter changes normalize to their baseline value.
        _, old_routing = lookup_signatures(before.font, tag, old_filters)
        _, new_routing = lookup_signatures(after.font, tag, comparison_filters)
        available = defaultdict(deque)
        for index in range(len(old)):
            available[old_routing(index)].append(index)
        for index in range(len(new)):
            matches = available[new_routing(index)]
            if report.check(bool(matches), "lookup-routing", table=tag, lookup=index,
                            source=rows[str(index)], **context):
                mapping.append({**identities[index], "baseline_lookup": matches.popleft()})
        report.check(not any(available.values()), "all-baseline-lookups", table=tag, **context)
        for member in ("ScriptList", "FeatureList"):
            old_member = getattr(before.font[tag].table, member) if tag in before.font else None
            new_member = getattr(after.font[tag].table, member) if tag in after.font else None
            report.check(value(old_member, lookup=old_routing) == value(new_member, lookup=new_routing),
                         "feature-routing", table=tag, member=member, **context)
    report.check(set(covered) == SCOPES[family], "nonempty-source-scope", covered=[list(k) for k in covered], **context)
    (report.out / f"{family}{after.path.suffix}-lookups.json").write_text(json.dumps(mapping, indent=2) + "\n")


def verify_metadata_scope(after, capture, family, report):
    """Check current metadata rules without freezing unrelated glyphs or lookups."""
    context = {"face": family, "format": after.path.suffix}
    if not report.check(capture["fontTools"] == PIN and capture["tables"] == tables(after.font),
                        "compiled-capture", **context):
        return
    current_classes = classes(after.font)
    report.check(all(current_classes.get(name, 0) != 3 for name in ADDITIONS - {OUTPUT})
                 and current_classes.get(OUTPUT) == 3, "metadata-classes", **context)
    retained = sorted(name for name, category in current_classes.items() if category == 3 and name != OUTPUT)
    expected_filter = (16, retained) if retained else (8, None)
    covered = set()
    for tag in ("GSUB", "GPOS"):
        lookups = after.font[tag].table.LookupList.Lookup if tag in after.font else []
        rows = capture["lookups"].get(tag, {})
        report.check(set(rows) == {str(i) for i in range(len(lookups))}, "complete-source-map", table=tag, **context)
        for index, lookup in enumerate(lookups):
            identity = rows.get(str(index))
            if not report.check(identity is not None, "source-identity", table=tag, lookup=index, **context):
                continue
            report.check(metadata_rules_allowed(lookup, identity, family, tag), "metadata-rule-scope",
                         table=tag, lookup=index, source=identity, **context)
            selected = SCOPES[family] & {tuple(block) for block in identity["blocks"]}
            covered.update(selected)
            if selected:
                report.check(filtering(after.font, lookup) == expected_filter, "lookup-filter-scope",
                             table=tag, lookup=index, source=identity, expected=expected_filter,
                             actual=filtering(after.font, lookup), **context)
    report.check(covered == SCOPES[family], "nonempty-source-scope", covered=[list(k) for k in covered], **context)


def metadata_geometry(after, report, context):
    report.check({INPUT, OUTPUT} <= set(after.order), "metadata-glyph-pair", **context)
    for name in set(after.order) & ADDITIONS:
        report.check(not after.outline(name) and after.font["hmtx"][name][0] == 0,
                     "empty-metadata-glyph", glyph=name, **context)


def metadata_cmap(face, points, report, context):
    report.check({cp for cp, name in face.cmap.items() if name in ADDITIONS} == set(points),
                 "exclusive-metadata-cmap", **context)
    for cp in points:
        report.check(face.cmap.get(cp) == INPUT, "shared-cmap", codepoint=f"U+{cp:04X}", **context)


def geometry(before, after, report, context):
    report.check(set(after.order) - set(before.order) <= ADDITIONS, "only-metadata-glyphs", **context)
    report.check({INPUT, OUTPUT}.isdisjoint(before.order), "baseline-without-metadata", **context)
    for name in before.order:
        present = name in after.glyphs
        report.check(present and before.outline(name) == after.outline(name), "existing-outlines", glyph=name, **context)
        report.check(present and before.font["hmtx"][name] == after.font["hmtx"][name], "existing-metrics", glyph=name, **context)
    metadata_geometry(after, report, context)


def without_metadata(shape):
    return [row for row in shape if row[0] != OUTPUT]


def compare_shape(report, expected, actual, kind, **context):
    report.check(expected == actual, kind, expected=expected, actual=actual, **context)


def select_capture(paths, expected_tables, report, family):
    matches, observed = [], []
    for path in sorted(paths):
        capture = json.loads(path.read_text())
        matched = capture["tables"] == expected_tables
        observed.append({"path": str(path), "tables": sorted(capture["tables"]), "matches": matched})
        if matched:
            matches.append(capture)
    # Analysis-only compilations are evidence, but cannot identify the final font.
    if report.check(len(matches) == 1, "matching-compilation-capture", face=family, captures=observed):
        return matches[0]
    return None


def prove_face(family, args, points, controls, report):
    stem = family + "-Regular"
    direction = FAMILIES[stem]["direction"]
    candidates = {ext: Face(args.built / f"{stem}.{ext}") for ext in ("ttf", "woff2")}
    baselines = {ext: Face(args.baseline / f"{stem}.{ext}") for ext in ("ttf", "woff2")} if args.baseline else {}
    stage = "crown" if family == "ThuravarkCarved" else "fontmake"
    captures = list((args.layout / stem / stage).glob("*.json"))
    capture = select_capture(captures, tables(candidates["ttf"].font), report, family)
    counts = Counter()
    control_face = baselines.get("ttf", candidates["ttf"])
    old_controls = {cp for cp, name in control_face.cmap.items()
                    if name in {"ignorable", "ignorable.sub"} and cp != controls["stress"]}
    report.check(bool(old_controls), "nonempty-legacy-controls", face=family)
    for ext, face in candidates.items():
        baseline = baselines.get(ext)
        context = {"face": family, "format": ext}
        metadata_geometry(face, report, context)
        if capture:
            verify_metadata_scope(face, capture, family, report)
        if baseline:
            geometry(baseline, face, report, context)
            if capture:
                verify_scope(baseline, face, capture, family, report)
            report.check(set(face.cmap) - set(baseline.cmap) == set(points) - set(baseline.cmap),
                         "only-metadata-cmap-additions", **context)
        metadata_cmap(face, points, report, context)
        for cp, name in (baseline.cmap.items() if baseline else []):
            if cp != controls["stress"]:
                report.check(face.cmap.get(cp) == name, "existing-cmap", codepoint=f"U+{cp:04X}", **context)
        for cp in points:
            standalone = face.shape(chr(cp), direction, {})
            report.check(bool(standalone) and all(row[0] == OUTPUT and row[1:3] == (0, 0) for row in standalone),
                         "standalone-metadata", codepoint=f"U+{cp:04X}", actual=standalone, **context)
    for group, fonts in (("built", candidates), ("baseline", baselines)):
        if not fonts:
            continue
        ttf, woff = fonts["ttf"], fonts["woff2"]
        report.check(ttf.cmap == woff.cmap and ttf.order == woff.order, "format-mapped-data", face=family, group=group)
        report.check(tables(ttf.font) == tables(woff.font), "format-layout", face=family, group=group)
        for name in ttf.order:
            report.check(ttf.outline(name) == woff.outline(name) and ttf.font["hmtx"][name] == woff.font["hmtx"][name],
                         "format-glyphs", face=family, group=group, glyph=name)
    for fixture in fixtures(family):
        text = fixture["text"]
        features = fixture["features"]
        context = {"face": family, "direction": direction, **{k: v for k, v in fixture.items() if k != "text"}}
        plain = {ext: face.shape(text, direction, features) for ext, face in candidates.items()}
        base = {ext: face.shape(text, direction, features) for ext, face in baselines.items()}
        compare_shape(report, plain["ttf"], plain["woff2"], "plain-format-shaping", **context)
        if baselines:
            compare_shape(report, base["ttf"], base["woff2"], "baseline-format-shaping", **context)
        if baselines and chr(controls["stress"]) not in text:
            for ext in candidates:
                compare_shape(report, base[ext], plain[ext], "native-shaping", format=ext, **context)
        counts["fixtures"] += 1
        for boundary in range(1, len(text)):
            counts["boundaries"] += 1
            if family == "Veldikko" and direction == "rtl":
                counts["rtl-joining"] += 1
            if family == "ThuravarkCarved" and features.get("ss01"):
                counts["bound-style"] += 1
            if family == "ThuravarkCarved" and "CROWN" in fixture["codes"]:
                counts["crown"] += 1
            for cp, category in points.items():
                marked = text[:boundary] + chr(cp) + text[boundary:]
                results = {}
                for ext, face in candidates.items():
                    actual = face.shape(marked, direction, features)
                    results[ext] = actual
                    details = {**context, "format": ext, "boundary": boundary, "codepoint": f"U+{cp:04X}"}
                    compare_shape(report, without_metadata(plain[ext]), without_metadata(actual), "metadata-shaping", **details)
                    report.check(all(row[1:3] == (0, 0) for row in actual if row[0] == OUTPUT)
                                 and all(row[0] != INPUT for row in actual), "metadata-output", actual=actual, **details)
                    # Invalid-input fixtures can already contain a box; equality prohibits a new one.
                    bad = lambda rows: Counter(row[0] for row in rows if row[0] in {".notdef", "notdef.box"})
                    report.check(bad(actual) == bad(plain[ext]), "no-introduced-box", **details)
                compare_shape(report, results["ttf"], results["woff2"], "metadata-format-shaping", boundary=boundary, codepoint=f"U+{cp:04X}", **context)
                counts[f"metadata:{category}"] += 1
                if family == "SemaronKuriale" and fixture["codes"] == "ANKRON_MAJ CATCH" and boundary == 1 and cp == controls["stress"]:
                    counts["stress-after-vowel-before-catch"] += 1
                    report.check(not any(row[0] in {".notdef", "notdef.box"} for row in results["ttf"])
                                 and any(row[0] == "grave" for row in results["ttf"]),
                                 "semaron-stress-catch", built=results["ttf"], **context)
                    if baselines:
                        corrected = baselines["ttf"].shape(marked, direction, features)
                        report.check(any(row[0] == "notdef.box" for row in corrected),
                                     "semaron-stress-baseline", baseline=corrected, **context)
            for cp in old_controls:
                marked = text[:boundary] + chr(cp) + text[boundary:]
                results = {}
                for ext, face in candidates.items():
                    results[ext] = face.shape(marked, direction, features)
                    if baselines:
                        expected = baselines[ext].shape(marked, direction, features)
                        compare_shape(report, expected, results[ext], "legacy-shaping", format=ext,
                                      boundary=boundary, codepoint=f"U+{cp:04X}", **context)
                compare_shape(report, results["ttf"], results["woff2"], "legacy-format-shaping", boundary=boundary, codepoint=f"U+{cp:04X}", **context)
                counts["legacy"] += 1
                if cp == controls["legacyShort"]:
                    counts["legacy-short"] += 1
    required = {"fixtures", "boundaries", "legacy", *{f"metadata:{category}" for category in points.values()}}
    if family == "Veldikko":
        required.add("rtl-joining")
    if family == "ThuravarkCarved":
        required.update(("bound-style", "crown"))
    if family == "SemaronKuriale":
        required.update(("stress-after-vowel-before-catch", "legacy-short"))
    for key in required:
        report.check(counts[key] > 0, "nonempty-shaping-coverage", face=family, category=key)
    report.faces[family] = dict(counts)


def verify_baseline(args, report):
    manifest = json.loads((ROOT / "tools/shared-metadata/baseline.json").read_text())
    report.check((args.baseline.parent / "source-sha.txt").read_text().strip() == manifest["source"], "baseline-source")
    actual = {p.name for p in args.baseline.iterdir() if p.suffix in {".ttf", ".woff2"}}
    report.check(actual == set(manifest["files"]), "baseline-files")
    for name, expected in manifest["files"].items():
        path = args.baseline / name
        report.check(path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == expected,
                     "baseline-hash", file=name, expected=expected)
    for stem, family in FAMILIES.items():
        if family["scriptKind"] == "logographic":
            for ext in ("ttf", "woff2"):
                name = f"{stem}.{ext}"
                report.check((args.baseline / name).read_bytes() == (args.built / name).read_bytes(), "logographic-bytes", file=name)
    report.check(set(FIXTURES) == {stem.removesuffix("-Regular") for stem, fact in FAMILIES.items() if fact["scriptKind"] == "sound"},
                 "all-sound-families")


def main():
    parser = argparse.ArgumentParser(description=__doc__, epilog=(
        "Example: .venv/bin/python tools/shared_metadata_proof.py --built fonts "
        "--layout build/evidence/layout --out build/evidence/shaping. "
        "Add --baseline build/baseline/fonts for the immutable transition comparison; "
        "its parent must contain source-sha.txt matching tools/shared-metadata/baseline.json."))
    parser.add_argument("--baseline", type=Path, help="enable the strict transition comparison against the pinned pre-metadata fonts")
    parser.add_argument("--built", type=Path, required=True, help="directory of candidate TTF and WOFF2 files")
    parser.add_argument("--layout", type=Path, required=True, help="compiler captures produced by HL_LAYOUT_EVIDENCE_DIR")
    parser.add_argument("--out", type=Path, required=True, help="directory for report.json, failures.jsonl and transition lookup maps")
    args = parser.parse_args()
    report = Report(args.out, "transition" if args.baseline else "metadata")
    try:
        report.check(set(FIXTURES) == {stem.removesuffix("-Regular") for stem, fact in FAMILIES.items() if fact["scriptKind"] == "sound"},
                     "all-sound-families")
        if args.baseline:
            verify_baseline(args, report)
        points, controls = registry()
        for family in FIXTURES:
            try:
                prove_face(family, args, points, controls, report)
            except Exception:
                report.check(False, "face-proof-exception", face=family, error=traceback.format_exc())
    except Exception:
        report.check(False, "proof-exception", error=traceback.format_exc())
    return report.finish()


if __name__ == "__main__":
    sys.exit(main())
