# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Confirm that every font's cheatsheet lists every character, and that the names are sound.

    .venv/bin/python tools/charts_guard.py

For each family of fonts.json, the files tools/charts.py wrote under ``charts/`` are read
back. A failure is

- a ``codepoints`` row missing from the sheet's table, in either entity form or without its Code Point cell, or from the
  code chart, or without its glyph image, or a chart cell or glyph image for a code point the
  font has no row for;
- a missing chart page PNG, or a sheet missing from ``charts/index.md``;
- a name that is not in Unicode's style (uppercase ASCII letters, digits, spaces and
  hyphens), a name used twice within a script, a Zethu name that is not its code point's position, or a name-table entry for a code point the
  script has no row for.

A row without a name is a finding, not a failure, until the script's name table
(``tools/names/<script>.json``) names it: it prints as a warning and the exit status is 0.
Every message is ``path: severity: message``.
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import charts  # noqa: E402
import codepoint_order  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
NAME = re.compile(r"^[A-Z0-9]+(?:[ -][A-Z0-9]+)*$")


def sheet_problems(entry: dict, md: str, svgs: dict[str, str], glyphs: set[str], pngs: set[str]) -> list[str]:
    """Failures of one family's sheet: its Markdown, chart SVG texts by file name, glyph file names and chart PNG names."""
    folder = charts.FOLDERS[entry["class"]]
    where = f"charts/{folder}.md"
    out = []
    rows = {charts.hexcode(r): r for r in entry["codepoints"]}
    for hex_, row in rows.items():
        cp = charts.code(row)
        cells = [c.strip() for line in md.split("\n") if f"U+{hex_}.svg)" in line for c in line.split("|")]
        if row["codepoint"] not in cells:
            out.append(f"{where}: error: {row['codepoint']} has no Code Point cell {row['codepoint']}")
        for form in (f"`&#{cp};`", f"`&#x{hex_};`"):
            if form not in md:
                out.append(f"{where}: error: {row['codepoint']} has no {form} in the table")
        if f"U+{hex_}.svg" not in glyphs:
            out.append(f"charts/{folder}/glyphs: error: {row['codepoint']} has no glyph image")
        elif f"({folder}/glyphs/U+{hex_}.svg)" not in md:
            out.append(f"{where}: error: {row['codepoint']} shows no glyph image")
    drawn = [h for text in svgs.values() for h in re.findall(r'class="drawn" id="cp-([0-9A-F]+)"', text)]
    for hex_ in rows:
        if hex_ not in drawn:
            out.append(f"charts/{folder}: error: U+{hex_} is not in the code chart")
    for hex_ in set(drawn) - set(rows):
        out.append(f"charts/{folder}: error: the code chart draws U+{hex_}, which the font has no row for")
    for hex_ in {g[2:-4] for g in glyphs} - set(rows):
        out.append(f"charts/{folder}/glyphs: error: a glyph image for U+{hex_}, which the font has no row for")
    for name in svgs:
        if name.replace(".svg", ".png") not in pngs:
            out.append(f"charts/{folder}/{name}: error: no PNG of the chart page")
    return out


def name_problems(entries: list[dict]) -> tuple[list[str], list[str]]:
    """Failures and findings of the names: style, uniqueness within a script, the name tables' keys."""
    failures, findings = [], []
    seen: dict[str, dict[str, str]] = {}
    for entry in entries:
        script = codepoint_order.SCRIPTS[Path(entry["files"]["ttf"]).stem]
        used = seen.setdefault(script, {})
        for row in entry["codepoints"]:
            name = row.get("name")
            if name is None:
                findings.append(
                    f"fonts.json: warning: {entry['name']}: {row['codepoint']} (glyph {row['glyph']}, kind {row['kind']}) has no name"
                )
                continue
            if script == "zethu" and name != codepoint_order.zethu_name(charts.code(row)):
                failures.append(
                    f"fonts.json: error: {entry['name']}: {row['codepoint']} is named {name}, "
                    f"not {codepoint_order.zethu_name(charts.code(row))}, the name of its position"
                )
            if not NAME.match(name):
                failures.append(f"fonts.json: error: {entry['name']}: {row['codepoint']} is named {name!r}, which is not in Unicode's style")
            if used.get(name, row["codepoint"]) != row["codepoint"]:
                failures.append(f"fonts.json: error: {name} names both {used[name]} and {row['codepoint']}")
            used[name] = row["codepoint"]
    rows_by_script: dict[str, set[str]] = {}
    for entry in entries:
        script = codepoint_order.SCRIPTS[Path(entry["files"]["ttf"]).stem]
        rows_by_script.setdefault(script, set()).update(r["codepoint"] for r in entry["codepoints"])
    for script, rows in rows_by_script.items():
        for cp in codepoint_order.names(script):
            if cp not in rows:
                failures.append(f"tools/names/{script}.json: error: {cp} is named but the script has no row for it")
    return failures, findings


def check(manifest: dict) -> tuple[list[str], list[str]]:
    entries = manifest["families"]
    failures, findings = name_problems(entries)
    index = ROOT / "charts" / "index.md"
    index_text = index.read_text(encoding="utf-8") if index.exists() else ""
    for entry in entries:
        folder = charts.FOLDERS[entry["class"]]
        md = ROOT / "charts" / f"{folder}.md"
        if not md.exists():
            failures.append(f"charts/{folder}.md: error: the sheet is missing; run tools/charts.py")
            continue
        base = ROOT / "charts" / folder
        svgs = {p.name: p.read_text(encoding="utf-8") for p in base.glob("chart-*.svg")}
        glyphs = {p.name for p in (base / "glyphs").glob("*.svg")}
        pngs = {p.name for p in base.glob("chart-*.png")}
        failures += sheet_problems(entry, md.read_text(encoding="utf-8"), svgs, glyphs, pngs)
        if f"]({folder}.md)" not in index_text:
            failures.append(f"charts/index.md: error: no link to {folder}.md")
    return failures, findings


def main() -> None:
    failures, findings = check(json.loads((ROOT / "fonts.json").read_text(encoding="utf-8")))
    for line in findings + failures:
        print(line, file=sys.stderr)
    print(f"charts: {len(failures)} failures, {len(findings)} unnamed rows", file=sys.stderr)
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
