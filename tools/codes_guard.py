# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Confirm that every character of every face has exactly one glyph code.

    .venv/bin/python tools/codes_guard.py

``tools/codes/<script>.json`` is the one table of each script's codes, and
tools/write_css.py writes each code into fonts.json. A face fails when

- a character of its fonts.json table has no ``code``, or a code that is not the one
  its script's table gives the code point;
- a code does not match ``^[A-Za-z0-9_]+$``;
- two characters of the face share a code. Codes are case-sensitive, so ``KA`` and
  ``ka`` are two codes;

and a code table fails when it gives two code points one code, or names a code point
that no face of its script draws,
when a face's file stem has no script, or when a table belongs to no script. Where the
Khelathi Zethu Glyphs or Chalish Pilam Ceremonial build table states a sign's code,
it must be the code the script's table gives.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import codes  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


def manifest() -> dict:
    return json.loads((ROOT / "fonts.json").read_text(encoding="utf-8"))


def tables() -> dict[str, dict[str, str]]:
    """Every code table under tools/codes/, by script."""
    return {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in sorted(codes.CODES.glob("*.json"))}


def build_codes() -> dict[str, dict[str, str]]:
    """The codes the build tables of Khelathi Zethu Glyphs and Chalish Pilam Ceremonial state, by
    script and code point: every drawn Zethu sign, and every ceremonial glyph but the joiners."""
    zethu = json.loads((ROOT / "tools" / "khelathi-zethu-glyphs" / "encoding.json").read_text(encoding="utf-8"))
    ceremonial = json.loads((ROOT / "tools" / "chalish-pilam" / "ceremonial_encoding.json").read_text(encoding="utf-8"))
    return {
        "zethu": {s["codepoint"]: s["code"] for s in zethu["signs"] if s.get("drawn")},
        "chalishceremonial": {
            g["codepoint"]: g["code"]
            for g in ceremonial["glyphs"]
            if g["kind"] != "joiner" and not g.get("retired") and not g.get("pending")
        },
    }


def problems(doc: dict, by_script: dict[str, dict[str, str]], stated: dict[str, dict[str, str]]) -> list[str]:
    found = []
    drawn: dict[str, set[str]] = {}
    for family in doc["families"]:
        label = family["name"]
        stem = Path(family["files"]["ttf"]).stem
        script = codes.SCRIPTS.get(stem)
        if script is None:
            found.append(f"tools/codes.py: error: {label}: {stem} has no script in SCRIPTS")
            continue
        table = by_script.get(script)
        if table is None:
            found.append(f"tools/codes/{script}.json: error: {label}: the script has no code table")
            continue
        drawn.setdefault(script, set())
        owner: dict[str, str] = {}
        for row in family["codepoints"]:
            point, code = row["codepoint"], row.get("code")
            drawn[script].add(point)
            if not code:
                found.append(f"fonts.json: error: {label}: {point} has no code")
                continue
            if not codes.CODE.match(code):
                found.append(f"fonts.json: error: {label}: {point} has the code {code!r}, which is not [A-Za-z0-9_]+")
            if table.get(point) != code:
                found.append(f"fonts.json: error: {label}: {point} has the code {code!r}, "
                             f"not {table.get(point)!r} as tools/codes/{script}.json gives it")
            if code in owner:
                found.append(f"fonts.json: error: {label}: {point} and {owner[code]} share the code {code}")
            else:
                owner[code] = point
    for script, table in by_script.items():
        path = f"tools/codes/{script}.json"
        if script not in drawn:
            found.append(f"{path}: error: no face of fonts.json is written in the script {script}")
            continue
        seen: dict[str, str] = {}
        for point, code in table.items():
            if code in seen:
                found.append(f"{path}: error: {point} and {seen[code]} share the code {code}")
            seen.setdefault(code, point)
            if point not in drawn[script]:
                found.append(f"{path}: error: {point} ({code}) is a code point no face of the script draws")
            if not codes.CODE.match(code):
                found.append(f"{path}: error: {point} has the code {code!r}, which is not [A-Za-z0-9_]+")
    for script, points in stated.items():
        table = by_script.get(script, {})
        for point, code in points.items():
            if point in table and table[point] != code:
                found.append(f"tools/codes/{script}.json: error: {point} is {table[point]!r}, "
                             f"but the font's build table gives it the code {code!r}")
    return found


def main():
    doc = manifest()
    found = problems(doc, tables(), build_codes())
    for p in found:
        print(p)
    count = sum(len(f["codepoints"]) for f in doc["families"])
    print(f"glyph codes: {count} characters of {len(doc['families'])} faces, "
          + (f"{len(found)} problems" if found else "ok"))
    sys.exit(1 if found else 0)


if __name__ == "__main__":
    main()
