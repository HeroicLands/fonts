# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Set the Teng Chou passages from the built font.

    .venv/bin/python tools/teng-chou/text_specimen.py [--font fonts/TengChou-Regular.ttf]

``specimens/teng-chou/text.png`` sets the Tantsou and Jurthati passages of
``texts.py`` along a line, as an inline span sets them, at display size and at body
size, each line over its transliteration. ``text-vertical.png`` sets them as Teng
Chou is written: in columns of ten, read from the right, shaped top to bottom by
HarfBuzz from the font's vertical metrics, on a ruled grid of one-em cells that
shows a column of ten is ten em. ``tally.png`` sets the
five stages of the tally and counts kept with it, along a line and in columns.
"""

import argparse
import sys
from pathlib import Path

import uharfbuzz as hb
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))
import texts  # noqa: E402
from render import Renderer, Shaped, label_font  # noqa: E402

PAPER = (244, 238, 224)
INK = (24, 21, 19)
GREY = (118, 110, 98)
RULE = (205, 192, 165)


def roman(line) -> str:
    return " ".join(t[1:].upper() if t.startswith("=") else t for t in line)


def horizontal(r: Renderer, out: Path):
    W = 2400
    passages = [("Tantsou", texts.TANTSOU), ("Jurthati, its particles and endings in the syllabary", texts.JURTHATI)]
    H = 220 + sum(80 + (len(lines) + 1) // 2 * 150 + 4 * 46 + 100 for _, lines in passages) + 200
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.text((40, 30), "Teng Chou — set from the font, along a line", fill=INK, font=label_font(46))
    d.text((40, 92), "As an inline span sets the characters: left to right. Each sentence at 72 px over its "
           "transliteration (signs of the syllabary in capitals); then the passage run on at 32, 20 and 14 px.",
           fill=GREY, font=label_font(22))
    y = 170
    for title, lines in passages:
        d.text((40, y), title, fill=INK, font=label_font(30))
        y += 60
        for i, line in enumerate(lines):
            x = 40 if i % 2 == 0 else W // 2
            r.text(img, x, y + 72, texts.text(line), 72, color=INK)
            d.text((x, y + 96), roman(line), fill=GREY, font=label_font(20))
            if i % 2 == 1 or i == len(lines) - 1:
                y += 150
        run = "".join(texts.text(line) for line in lines)
        for px in (32, 20, 14):
            d.text((40, y + px - 14), f"{px} px", fill=GREY, font=label_font(16))
            r.text(img, 110, y + px, run * (3 if px < 30 else 2), px, color=INK)
            y += px + 30
        y += 60
    img.crop((0, 0, W, y + 20)).save(out)
    return out


def column(r: Renderer, text: str) -> Shaped:
    """The text shaped top to bottom: each glyph at (x, y) from the column's axis and top."""
    buf = hb.Buffer()
    buf.add_str(text)
    buf.direction = "ttb"
    buf.script = "Zyyy"
    buf.guess_segment_properties()
    hb.shape(r.hb_font, buf, {})
    glyphs, pen_y = [], 0
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        glyphs.append((info.codepoint, pos.x_offset, pen_y + pos.y_offset, pos.y_advance))
        pen_y += pos.y_advance
    return Shaped(glyphs, -pen_y)


def grid_block(r: Renderer, img, d, text: str, right: int, top: int, size: int, per: int = 10, cols: int | None = None):
    """``text`` in columns of ``per`` characters, read from the right, each column on a
    ruled grid of one-em cells, so a column of ``per`` characters is ``per`` em tall."""
    columns = [text[i:i + per] for i in range(0, len(text), per)][:cols]
    x = right
    for col in columns:
        left = x - size / 2
        for k in range(per + 1):
            d.line([(left, top + k * size), (left + size, top + k * size)], fill=RULE, width=1)
        d.line([(left, top), (left, top + per * size)], fill=RULE, width=1)
        d.line([(left + size, top), (left + size, top + per * size)], fill=RULE, width=1)
        r.draw(img, x, top, column(r, col), size, color=INK)
        x -= size
    return x, len(columns)


def vertical(r: Renderer, out: Path, size=96, body=32):
    run = "".join(texts.text(line) for line in texts.TANTSOU + texts.JURTHATI)
    per = 10
    big_cols = -(-len(run) // per)
    W = max(1400, 140 + big_cols * size + 160)
    H = 200 + per * size + 140 + per * body + 120
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.text((40, 30), "Teng Chou — set from the font, in columns", fill=INK, font=label_font(40))
    d.text((40, 84), f"Read from the right. Every character takes exactly one em down the column, so a column of {per} "
           f"is {per} em: each ruled cell is one em, at {size} px.", fill=GREY, font=label_font(20))
    top = 170
    right = W - 120 - size // 2
    x, n = grid_block(r, img, d, run, right, top, size, per, big_cols)
    # a measure beside the first column: ten em
    mx = right + size / 2 + 30
    d.line([(mx, top), (mx, top + per * size)], fill=GREY, width=2)
    for yy in (top, top + per * size):
        d.line([(mx - 8, yy), (mx + 8, yy)], fill=GREY, width=2)
    d.text((mx + 12, top + per * size / 2 - 12), f"{per} em", fill=GREY, font=label_font(20))
    y0 = top + per * size + 90
    d.text((40, y0 - 44), f"The same passages run on at {body} px, columns of {per} on the same one-em grid.",
           fill=GREY, font=label_font(18))
    grid_block(r, img, d, run * 2, W - 120 - body // 2, y0, body, per, (W - 200) // body)
    img.crop((0, 0, W, y0 + per * body + 40)).save(out)
    return out


def tally_sheet(r: Renderer, out: Path):
    """The five stages of the tally large, then counts kept with it: rows of finished
    tallies with one partial at the end, along a line and in columns."""
    cp = {row["glyph"]: chr(int(row["codepoint"][2:], 16)) for row in texts.codepoint_order.ltr_table("TengChou-Regular")}
    stage = [cp[f"tc.tally{n}"] for n in range(1, 6)]
    counts = [23, 17, 9, 31]
    W, H = 2000, 1300
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.text((40, 30), "Teng Chou — the tally of five", fill=INK, font=label_font(40))
    d.text((40, 84), "One stroke for each item, in this order; a finished tally is five. Set from the font.",
           fill=GREY, font=label_font(20))
    for i, ch in enumerate(stage):
        x = 60 + i * 300
        r.text(img, x, 400, ch, 260, color=INK)
        d.text((x, 420), f"{i + 1}", fill=GREY, font=label_font(24))
    y = 520
    d.text((40, y), "Counts of " + ", ".join(map(str, counts)) + ", along a line at 48 px:", fill=GREY, font=label_font(20))
    for n in counts:
        y += 70
        line = stage[4] * (n // 5) + (stage[n % 5 - 1] if n % 5 else "")
        r.text(img, 60, y + 48, line, 48, color=INK)
        d.text((60 + r.width(line, 48) + 30, y + 20), str(n), fill=GREY, font=label_font(22))
    d.text((1180, 520), "The same counts in columns, from the right:", fill=GREY, font=label_font(20))
    x = W - 100
    for n in counts:
        line = stage[4] * (n // 5) + (stage[n % 5 - 1] if n % 5 else "")
        r.draw(img, x, 570, column(r, line), 48, color=INK)
        d.text((x - 20, 570 + 7 * 48 + 20), str(n), fill=GREY, font=label_font(22))
        x -= 110
    img.crop((0, 0, W, 1060)).save(out)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--font", default=str(ROOT / "fonts" / "TengChou-Regular.ttf"))
    ap.add_argument("--out", default=str(ROOT / "specimens" / "teng-chou"))
    a = ap.parse_args()
    r = Renderer(Path(a.font))
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    print(horizontal(r, out / "text.png"))
    print(vertical(r, out / "text-vertical.png"))
    print(tally_sheet(r, out / "tally.png"))


if __name__ == "__main__":
    main()
