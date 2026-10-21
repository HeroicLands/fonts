# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Check the paint map of Khelathi Zethu Glyphs against the built font.

    .venv/bin/python tools/khelathi-zethu-glyphs/paint_guard.py [--font fonts/KhelathiZethuGlyphs-Regular.ttf]

It fails when a drawn sign has no map, when a map names a sign that is not drawn or not in the
encoding, when a category is not one of the map's `categories` (in `defaults`, a sign's
`default` or `outline`, or a region), when a group of drawn signs has no default, when a seed
falls on the outline or outside every region, when two seeds fall in one region, and when a
region of a sign in a figure group (`paint.SEEDED_GROUPS`: people, women, gods, the body,
beasts and birds) has no seed of its own, and when any pixel inside a sign's outline belongs to no region. Regions
are found by `paint.py`, at its scale `K`, exactly as the contact sheets find them.
"""

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import paint  # noqa: E402

ROOT = HERE.parent.parent


def where(text: str, sid: str, needle: str = "") -> str:
    """The line of a sign's entry in paint.json, or of the first line holding `needle` after it."""
    lines = text.splitlines()
    start = next((i for i, line in enumerate(lines) if line.strip().startswith(f'"{sid}"')), None)
    if start is None:
        return ""
    if needle:
        for i in range(start, len(lines)):
            if needle in lines[i]:
                return f"{i + 1}:"
    return f"{start + 1}:"


def check(data: dict, enc: dict, glyphs: paint.Glyphs, text: str = "") -> list:
    """Every finding about the map `data`, as `paint.json:line: error: message` lines."""
    rel = paint.PAINT.relative_to(ROOT) if paint.PAINT.is_relative_to(ROOT) else paint.PAINT
    out = []

    def err(sid, msg, needle=""):
        out.append(f"{rel}:{where(text, sid, needle) if sid else ''} error: {msg}")

    cats = set(data.get("categories", []))
    defaults = data.get("defaults", {})
    signs = data.get("signs", {})
    for group, cat in defaults.items():
        if cat not in cats:
            err("", f"group {group} defaults to unknown category {cat!r}")
    drawn = [sid for sid, e in enc.items() if e["drawn"]]
    for sid in drawn:
        if sid not in signs:
            err("", f"drawn sign {sid} has no paint map")
        if sid[:2] not in defaults:
            err("", f"group {sid[:2]} of drawn sign {sid} has no default")
    for sid, entry in signs.items():
        if sid not in enc:
            err(sid, f"{sid} is not a sign of the encoding")
            continue
        if not enc[sid]["drawn"]:
            err(sid, f"{sid} is not drawn, so it has no regions to paint")
            continue
        if "default" in entry and entry["default"] not in cats:
            err(sid, f"{sid}: default {entry['default']!r} is not a category", '"default"')
        if "outline" in entry and (entry["outline"] not in cats or entry["outline"] == "ground"):
            err(sid, f"{sid}: outline {entry['outline']!r} is not a colour category", '"outline"')
        regions = paint.Regions(glyphs, enc[sid]["glyph"])
        if regions.unpainted():
            err(sid, f"{sid}: {regions.unpainted()} pixels inside the outline belong to no region")
        taken = {}
        for reg in entry.get("regions", []):
            x, y = reg["seed"]
            needle = f"[{x}, {y}]"
            if reg.get("paint") not in cats:
                err(sid, f"{sid}: seed {needle} paints unknown category {reg.get('paint')!r}", needle)
            i, why = regions.at(x, y)
            if why == "ink":
                err(sid, f"{sid}: seed {needle} falls on the outline", needle)
            elif not i:
                err(sid, f"{sid}: seed {needle} falls outside every region", needle)
            elif i in taken:
                err(sid, f"{sid}: seeds {taken[i]} and {needle} fall in one region", needle)
            else:
                taken[i] = needle
        if sid[:2] in paint.SEEDED_GROUPS:
            for i in range(1, regions.n + 1):
                if i not in taken:
                    x, y = regions.centres()[i]
                    err(sid, f"{sid}: region {i} near [{x}, {y}] has no seed; every region of a figure is painted explicitly")
    return out


def run(font: Path = paint.FONT, path: Path = paint.PAINT) -> list:
    text = Path(path).read_text(encoding="utf-8")
    return check(paint.load(path), paint.encoding(), paint.Glyphs(font), text)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--font", type=Path, default=paint.FONT)
    ap.add_argument("--paint", type=Path, default=paint.PAINT)
    args = ap.parse_args()
    problems = run(args.font, args.paint)
    for p in problems:
        print(p, file=sys.stderr)
    data = paint.load(args.paint)
    print(f"paint: {len(data['signs'])} signs mapped, {sum(len(e.get('regions', [])) for e in data['signs'].values())} seeds, "
          f"{len(problems)} problems")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
