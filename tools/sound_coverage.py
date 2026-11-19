# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Check the guide's shared invisible characters and declared visible font coverage."""

import argparse
import json
import subprocess
import sys
from pathlib import Path

import yaml
from fontTools.pens.boundsPen import BoundsPen
from fontTools.ttLib import TTFont, TTLibError

import codepoint_order
from write_css import FAMILIES

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = """
import { SHARED_SOUNDS, SHARED_SOUND_CONTROLS, validateGuideSounds }
    from '@heroiclands/package-build/engine/encoding-standard';
let input = ''; for await (const chunk of process.stdin) input += chunk;
const rows = JSON.parse(input);
const errors = validateGuideSounds(rows);
const seen = new Set(rows.map(row => row.ipa));
for (const ipa of Object.keys(SHARED_SOUNDS))
    if (!seen.has(ipa)) errors.push(`guide omits shared sound /${ipa}/`);
console.log(JSON.stringify({errors, points: [
    ...rows.filter(row => SHARED_SOUNDS[row.ipa]).map(row => SHARED_SOUNDS[row.ipa].invisible.codePointAt(0)),
    ...Object.entries(SHARED_SOUND_CONTROLS).filter(([key]) => key !== "legacyShort").map(([, value]) => value.codePointAt(0))
]}));
"""


def guide_points(guide):
    text = guide.read_text(encoding="utf-8")
    if not text.startswith("---\n") or "\n---" not in text[4:]:
        raise ValueError("guide has no frontmatter")
    front = yaml.safe_load(text[4:].split("\n---", 1)[0])
    rows = front["data"]["sounds"]["letters"]
    result = subprocess.run(
        ["node", "--input-type=module", "-e", REGISTRY],
        cwd=ROOT, input=json.dumps(rows), text=True, capture_output=True, check=True,
    )
    data = json.loads(result.stdout)
    if data["errors"]:
        raise ValueError("; ".join(data["errors"]))
    return data["points"]


def sound_files(registry, families=FAMILIES):
    for stem, fact in families.items():
        if fact.get("scriptKind") not in {"sound", "logographic"}:
            raise ValueError(f"{stem}: missing or unknown scriptKind")
    expected = {
        (stem, variant["slug"])
        for stem, fact in families.items()
        for variant in [fact, *fact.get("variants", [])]
    }
    files = {}
    seen = set()
    for variant in registry["families"]:
        stem = Path(variant["files"]["ttf"]).stem
        if stem not in families:
            raise ValueError(f"{stem}: no family declaration")
        slug = variant["class"].removeprefix("hl-")
        key = (stem, slug)
        if key not in expected or key in seen:
            raise ValueError(f"{stem}: unknown or duplicate variant {slug}")
        seen.add(key)
        if families[stem]["scriptKind"] != "sound":
            continue
        for file in variant["files"].values():
            files.setdefault(file, []).extend(codepoint_order.table(stem))
    if missing := expected - seen:
        raise ValueError(f"variants absent from fonts.json: {sorted(missing)}")
    return files


def check_font(file, points, rows):
    findings = []
    with TTFont(file) as font:
        cmap = font.getBestCmap()
        glyphs = font.getGlyphSet()
        for point in sorted(set(points)):
            name = cmap.get(point)
            label = f"U+{point:04X}"
            if name is None or name not in glyphs:
                findings.append(f"{label} has no mapped glyph")
                continue
            if font["hmtx"].metrics[name][0] != 0:
                findings.append(f"{label} has nonzero advance")
            pen = BoundsPen(glyphs)
            glyphs[name].draw(pen)
            if pen.bounds is not None:
                findings.append(f"{label} has ink")
        for row in { (r["codepoint"], r["glyph"]) for r in rows }:
            point, name = row
            if cmap.get(int(point[2:], 16)) != name or name not in glyphs:
                findings.append(f"{point} lacks declared visible glyph {name}")
    return findings


def main():
    parser = argparse.ArgumentParser(description=__doc__, epilog=(
        "Example: .venv/bin/python tools/sound_coverage.py build/Pronouncing_Thalorna.md. "
        "Use the exact guide revision and checksum pinned in CI; the command reads fonts.json "
        "and the built font files from the repository root."))
    parser.add_argument("guide", type=Path, help="pronunciation guide with data.sounds frontmatter")
    args = parser.parse_args()
    try:
        points = guide_points(args.guide)
        files = sound_files(json.loads((ROOT / "fonts.json").read_text(encoding="utf-8")))
    except (OSError, ValueError, KeyError, TypeError, yaml.YAMLError, subprocess.SubprocessError) as error:
        print(f"{args.guide}: error: {error}", file=sys.stderr)
        return 1
    count = 0
    for file, rows in files.items():
        try:
            findings = check_font(ROOT / file, points, rows)
        except (OSError, KeyError, ValueError, TTLibError) as error:
            findings = [str(error)]
        for finding in findings:
            print(f"{file}: error: {finding}", file=sys.stderr)
        count += len(findings)
    return int(count > 0)


if __name__ == "__main__":
    sys.exit(main())
