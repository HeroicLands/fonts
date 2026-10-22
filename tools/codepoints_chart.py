# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Draw each left-to-right face's code-point chart from fonts.json and the built font.

    .venv/bin/python tools/codepoints_chart.py [--out specimens]

One PNG per face, ``specimens/<face>/codepoints.png``: a grid of every character's
glyph with its code point and glyph name beneath. Each group of the face's table
(capitals, small letters, digraphs, and so on) starts a new row. The glyphs are drawn
from the built font's own outlines. The script asserts that every listed character
has a cell, that a glyph with an outline leaves ink in its cell, and that the chart
lists each code point once.
"""

import argparse
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
import codepoint_order  # noqa: E402
from render import Renderer, Shaped, label_font  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
PAPER = (250, 247, 240)
INK = (28, 26, 24)
GREY = (110, 106, 100)
RULE = (214, 207, 194)

COLUMNS = 8
CELL_W, CELL_H = 132, 176
GLYPH_SIZE = 84
BASELINE = 104
MARGIN = 24

# The specimen folder of each family, by manifest class.
FOLDERS = {
    "hl-semaron-kuriale": "semaron-kuriale",
    "hl-pirzath-carved": "pirzath",
    "hl-pirzath-hand": "pirzath-hand",
    "hl-thuravark-carved": "thuravark-carved",
    "hl-teng-chou": "teng-chou",
}


def rows_by_group(stem: str, table: list[dict]) -> list[list[dict]]:
    """The table split at the start of each group of codepoint_order."""
    starts = {start for _, start, _ in codepoint_order.LTR[stem][2]}
    groups: list[list[dict]] = []
    for row in table:
        if int(row["codepoint"][2:], 16) in starts or not groups:
            groups.append([])
        groups[-1].append(row)
    return groups


def draw_chart(family: dict) -> tuple[Image.Image, int]:
    ttf = ROOT / family["files"]["ttf"]
    stem = ttf.stem
    renderer = Renderer(ttf)
    glyph_id = {name: i for i, name in enumerate(renderer.order)}
    groups = rows_by_group(stem, family["codepoints"])
    height = MARGIN * 2 + CELL_H * sum(-(-len(g) // COLUMNS) for g in groups)
    img = Image.new("RGB", (MARGIN * 2 + CELL_W * COLUMNS, height), PAPER)
    draw = ImageDraw.Draw(img)
    small, tiny = label_font(15), label_font(13)
    scale = GLYPH_SIZE / renderer.upem
    drawn = 0
    y = MARGIN
    for group in groups:
        for index, row in enumerate(group):
            col, line = index % COLUMNS, index // COLUMNS
            x0, y0 = MARGIN + col * CELL_W, y + line * CELL_H
            draw.rectangle([x0, y0, x0 + CELL_W - 8, y0 + CELL_H - 8], outline=RULE)
            gid = glyph_id[row["glyph"]]
            advance = renderer.tt["hmtx"][row["glyph"]][0]
            contours = renderer.contours(gid)
            if advance:
                offset = x0 + (CELL_W - 8) / 2 - advance * scale / 2
            elif contours:
                xs = [px for _, pts in contours for px, _ in pts]
                offset = x0 + (CELL_W - 8) / 2 - (min(xs) + max(xs)) * scale / 2
            else:
                offset = x0
            before = img.copy().crop((x0 + 1, y0 + 1, x0 + CELL_W - 9, y0 + BASELINE + 40))
            renderer.draw(img, offset, y0 + BASELINE, Shaped([(gid, 0, 0, advance)], advance), GLYPH_SIZE, INK)
            after = img.crop((x0 + 1, y0 + 1, x0 + CELL_W - 9, y0 + BASELINE + 40))
            inked = before.tobytes() != after.tobytes()
            assert inked == bool(contours), f"{ttf.name}: {row['glyph']} {'left no ink' if contours else 'drew ink'}"
            draw.text((x0 + 8, y0 + 138), row["codepoint"], font=small, fill=INK)
            draw.text((x0 + 8, y0 + 156), row["glyph"], font=tiny, fill=GREY)
            drawn += 1
        y += CELL_H * -(-len(group) // COLUMNS)
    assert drawn == len(family["codepoints"]), f"{ttf.name}: {drawn} cells for {len(family['codepoints'])} characters"
    assert len({r["codepoint"] for r in family["codepoints"]}) == drawn, f"{ttf.name}: a code point is listed twice"
    return img, drawn


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(ROOT / "specimens"))
    args = parser.parse_args()
    manifest = json.loads((ROOT / "fonts.json").read_text(encoding="utf-8"))
    for family in manifest["families"]:
        folder = FOLDERS.get(family["class"])
        if folder is None:
            continue
        img, count = draw_chart(family)
        target = Path(args.out) / folder / "codepoints.png"
        target.parent.mkdir(parents=True, exist_ok=True)
        img.save(target, optimize=True)
        print(f"{target}: {count} characters")


if __name__ == "__main__":
    main()
