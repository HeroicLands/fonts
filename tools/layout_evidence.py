# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Capture source identities from the pinned feature compiler without changing fonts."""

import argparse
from copy import copy, deepcopy
import hashlib
import json
import runpy
import sys
from pathlib import Path

import fontTools
from fontTools.feaLib.builder import Builder
from fontTools.ttLib import newTable

PIN = "4.68.0"
TABLES = ("GSUB", "GPOS", "GDEF")


def value(item, omit=(), lookup=None, drop_glyphs=frozenset()):
    """Describe layout semantics; derived counts and binary offsets are immaterial."""
    if item is None or isinstance(item, (str, int, float, bool)):
        return item
    if isinstance(item, bytes):
        return item.hex()
    if isinstance(item, (list, tuple)):
        return [value(v, omit, lookup, drop_glyphs) for v in item
                if not isinstance(v, str) or v not in drop_glyphs]
    if isinstance(item, dict):
        return {str(k): value(v, omit, lookup, drop_glyphs)
                for k, v in sorted(item.items(), key=lambda pair: str(pair[0]))
                if k not in drop_glyphs}
    attrs = {}
    for key, child in sorted(vars(item).items()):
        if key.startswith("_") or key.endswith("Count") or key in omit:
            continue
        if key == "LookupListIndex" and lookup is not None:
            attrs[key] = lookup(child)
        else:
            attrs[key] = value(child, omit, lookup, drop_glyphs)
    return {"type": type(item).__name__, "fields": attrs}


def digest(item):
    return hashlib.sha256(json.dumps(item, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def tables(font):
    # Compilation adds bookkeeping to layout objects; isolate every layout table.
    isolated = copy(font)
    isolated.tables = dict(font.tables)
    for tag in TABLES:
        if tag in font:
            isolated.tables[tag] = deepcopy(font[tag])
    result = {}
    for tag in TABLES:
        if tag not in isolated:
            continue
        table = newTable(tag)
        table.decompile(isolated[tag].compile(isolated), isolated)
        table.table.ensureDecompiled(recurse=True)
        result[tag] = value(table.table)
    return result


def source_blocks(tree):
    result = {}

    def visit(node, blocks):
        kind = type(node).__name__
        if kind in {"FeatureBlock", "LookupBlock"}:
            blocks = [*blocks, [kind, node.name]]
        location = getattr(node, "location", None)
        if location is not None:
            key = str(location)
            if key in result and result[key] != blocks:
                raise ValueError(f"ambiguous source location {key}")
            result[key] = blocks
        for statement in getattr(node, "statements", []):
            visit(statement, blocks)

    visit(tree, [])
    return result


def install_capture(directory):
    if fontTools.__version__ != PIN:
        raise ValueError(f"lookup capture requires fontTools {PIN}, found {fontTools.__version__}")
    original = Builder.build
    count = 0

    def build(builder, *args, **kwargs):
        nonlocal count
        result = original(builder, *args, **kwargs)
        count += 1
        directory.mkdir(parents=True, exist_ok=True)
        blocks = source_blocks(builder.parseTree)
        mapping = {}
        for tag, rows in builder.lookup_locations.items():
            mapping[tag] = {}
            for index, info in rows.items():
                if info.location not in blocks:
                    raise ValueError(f"{tag} lookup {index}: unmapped source {info.location}")
                mapping[tag][index] = {"location": info.location, "name": info.name,
                                       "feature": info.feature, "blocks": blocks[info.location]}
        report = {"fontTools": fontTools.__version__, "lookups": mapping,
                  "tables": tables(builder.font)}
        (directory / f"{count}.json").write_text(json.dumps(report, indent=2) + "\n")
        (directory / f"{count}.fea").write_text(builder.parseTree.asFea())
        return result

    Builder.build = build


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--module")
    target.add_argument("--script")
    parser.add_argument("arguments", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    install_capture(args.out)
    rest = args.arguments
    if rest and rest[0] == "--":
        rest = rest[1:]
    sys.argv = [args.module or args.script, *rest]
    if args.module:
        runpy.run_module(args.module, run_name="__main__", alter_sys=True)
    else:
        sys.path.insert(0, str(Path(args.script).resolve().parent))
        runpy.run_path(args.script, run_name="__main__")


if __name__ == "__main__":
    main()
