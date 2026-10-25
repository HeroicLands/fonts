# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Render Semaron Kuriale's specimen sheets to PNG.

    .venv/bin/python tools/semaron-kuriale/specimens.py [--font fonts/SemaronKuriale-Regular.ttf]
                                                     [--out specimens/semaron-kuriale]

Three sheets, each drawn from the built font's own outlines:

- ``00-capitals.png``: all 24 majuscules, large, one to a cell and labelled, for review;
- ``01-glyph-chart.png``: each letter's majuscule above its minuscule, the long vowels,
  the numerals and the marks;
- ``02-texts.png``: the Vylari texts at display size and at 18 and 24 px.
"""

import argparse
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from encoded import Encoded, EncodedRenderer  # noqa: E402
from render import Renderer, label_font  # noqa: E402
from PIL import ImageDraw  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent
PAPER = (250, 247, 240)
INK = (28, 26, 24)
GREY = (110, 106, 100)
RULE = (214, 207, 194)

LETTERS = ["a", "b", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "th", "u",
           "v", "w", "y", "z"]
TEXTS = [
    ("The oath", "Ulthandoi okointor denon zaron ul kalmetharen."),
    ("The morning call", "Daimela orfenamen."),
    ("A question, eza", "Eza à daimela falvator."),
    ("A question expecting yes", "Areza à thelmos lokator."),
    ("A command, voza", "Voza lokathen."),
    ("A prohibition", "Ar voza lokathen."),
    ("Reported speech, vethor", "Daimela vethor orfenamen."),
    ("An exclamation, aia", "Aia theson."),
    ("Names", "Eltheza Solterates. Kalmethis. Hiltheris. Tholmarar."),
    ("The long vowels and the numerals", "Daamela. viir. kuun. 0123456789. 12. 2026."),
    ("Period alone writes the pause point", "Daimela vethor orfenamen. theson."),
    ("The Vylari catch, on its ancient stop or article", "kàralzon. kàrthorgila. à. À."),
    ("Other tongues' catch spellings", "Au'Khelathu. Zeghet'Nelgu. Amqel'Uqa. selth-kelmeza."),
]


def text(draw, xy, s, size=14, color=GREY):
    draw.text(xy, s, font=label_font(size), fill=color)


def capitals(r: Renderer, out: Path):
    cols, rows = 6, 4
    cell_w, cell_h = 300, 330
    em = 300
    img = Image.new("RGB", (cols * cell_w + 80, rows * cell_h + 120), PAPER)
    d = ImageDraw.Draw(img)
    text(d, (40, 24), "Semaron Kuriale: the 24 majuscules, one to a cell", 22, INK)
    for i, name in enumerate(LETTERS):
        col, row = i % cols, i // cols
        x0, y0 = 40 + col * cell_w, 80 + row * cell_h
        d.rectangle([x0, y0, x0 + cell_w - 10, y0 + cell_h - 10], outline=RULE)
        typed = name.capitalize()
        # a y before a vowel is the glide; alone it types the vowel i, so the glide is shown from "Ya"
        shaped = r.shape("Ya" if name == "y" else typed)
        shaped.glyphs = shaped.glyphs[:1]
        shaped.advance = shaped.glyphs[0][3]
        width = shaped.advance * em / r.upem
        base = y0 + 240
        d.line([x0 + 8, base, x0 + cell_w - 18, base], fill=RULE)
        r.draw(img, x0 + (cell_w - 10 - width) / 2, base, shaped, em, INK)
        glyph = r.order[shaped.glyphs[0][0]]
        text(d, (x0 + 12, y0 + cell_h - 40), f"{typed}{'a' if name == 'y' else ''}   glyph {glyph}", 15, INK)
    img.save(out / "00-capitals.png")


def glyph_chart(r: Renderer, out: Path):
    cols = 8
    cell_w, cell_h, em = 200, 250, 130
    groups = [
        ("Letters: majuscule above minuscule", [(n.capitalize(), n) for n in LETTERS]),
        ("Long vowels: a doubled vowel types the curl", [(v.capitalize() + v, v + v) for v in "aiu"]),
        ("Numerals", [(str(i), None) for i in range(10)]),
        ("Marks: period writes the point; the catch stands on its base", [
            (".", None), ("à", None), ("À", None), ("kà", None), ("l'", None), ("Aa'", None), ("th'", None), ("'", None),
            ("x?", None)]),
    ]
    rows = sum((len(items) + cols - 1) // cols for _, items in groups)
    img = Image.new("RGB", (cols * cell_w + 80, rows * cell_h + len(groups) * 50 + 100), PAPER)
    d = ImageDraw.Draw(img)
    text(d, (40, 24), "Semaron Kuriale: the glyph chart", 22, INK)
    y = 80
    for heading, items in groups:
        text(d, (40, y), heading, 16, INK)
        y += 34
        for i, (top, bottom) in enumerate(items):
            col, row = i % cols, i // cols
            x0, y0 = 40 + col * cell_w, y + row * cell_h
            d.rectangle([x0, y0, x0 + cell_w - 10, y0 + cell_h - 10], outline=RULE)
            if bottom is None:
                lines = [(top, 150, top)]
            else:
                lines = [(top, 100, top), (bottom, 200, bottom)]
            for typed, offset, label in lines:
                shaped = r.shape(typed)
                width = shaped.advance * em / r.upem
                r.draw(img, x0 + (cell_w - 10 - width) / 2, y0 + offset, shaped, em, INK)
            label = "  ".join(t for t, _, _ in lines)
            text(d, (x0 + 10, y0 + cell_h - 40), label, 14, GREY)
        y += ((len(items) + cols - 1) // cols) * cell_h + 16
    img.crop((0, 0, img.width, y + 20)).save(out / "01-glyph-chart.png")


def texts(r: Renderer, out: Path):
    width = int(max(r.width(s, 96) for _, s in TEXTS)) + 100
    img = Image.new("RGB", (width, 5200), PAPER)
    d = ImageDraw.Draw(img)
    text(d, (40, 24), "Semaron Kuriale: Vylari sentences at display size (96 px), then at 18 and 24 px", 22, INK)
    y = 70
    for heading, s in TEXTS:
        text(d, (40, y), heading, 14, INK)
        base = y + 20 + 96 * 0.75
        r.text(img, 40, base, s, 96, INK)
        text(d, (40, base + 0.45 * 96), s, 13)
        y = base + 0.45 * 96 + 34
    for size in (18, 24):
        y += 12
        text(d, (40, y), f"{size} px", 14, INK)
        y += 22
        for _, s in TEXTS:
            base = y + 0.8 * size
            r.text(img, 40, base, s, size, INK)
            y = base + 0.55 * size + 6
    img.crop((0, 0, width, int(y + 20))).save(out / "02-texts.png")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--font", default=str(ROOT / "fonts" / "SemaronKuriale-Regular.ttf"))
    ap.add_argument("--out", default=str(ROOT / "specimens" / "semaron-kuriale"))
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    r = EncodedRenderer(Renderer(Path(args.font)), Encoded("semaron-kuriale"))
    capitals(r, out)
    glyph_chart(r, out)
    texts(r, out)
    print(f"{out}: 00-capitals.png, 01-glyph-chart.png, 02-texts.png")


if __name__ == "__main__":
    main()
