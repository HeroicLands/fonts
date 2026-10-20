# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Render the specimen sheets to PNG.

    .venv/bin/python tools/qalezu/specimens.py [--font fonts/Qalezu-Regular.ttf] [--out specimens/qalezu]
                                            [--thalorna ~/dev/HeroicLands/thalorna | --note FILE]

Three sheets: the glyph chart, a dozen Khelathi words and names converted and
shaped right to left beside their Latin and gloss, and an English sentence with
a Qalezu name followed by a right-aligned block of Qalezu lines.

Text is shaped with a right-to-left direction and no script hint.
"""

import argparse
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from render import Renderer, label_font  # noqa: E402
import guard  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent
PAPER = (248, 244, 236)
INK = (28, 24, 20)
GREY = (120, 112, 104)
RULE = (205, 198, 186)

WORDS = [
    "Au'Khelathu", "Khelathu", "Khelathi-zethu", "Qalezu", "Nelgir", "Halzi",
    "Weth'ur", "Qe'aret", "Uqa'a", "Igelnaru", "Genzet", "Lenni",
]
NAMES = {"Lenni": "a given name, with the n doubled"}
BLOCK = ["Gar-Qethar", "Zel-Qar", "Lut-Psaqa"]
SENTENCE = ("The scribes of the delta write ", "Khelathu", " with a reed on papyrus.")


def page(width, height):
    img = Image.new("RGB", (width, height), PAPER)
    return img, ImageDraw.Draw(img)


def shaped(r: Renderer, text: str):
    return r.shape(text, direction="rtl")


def glyph_chart(r: Renderer, out: Path):
    enc = json.loads(guard.ENCODING.read_text(encoding="utf-8"))
    cells = [(g["glyph"], g["sound"], g["codepoint"], chr(int(g["codepoint"][2:], 16)))
             for g in enc["glyphs"]]
    cols, cell_w, cell_h = 8, 210, 270
    rows = (len(cells) + cols - 1) // cols
    margin = 40
    img, d = page(margin * 2 + cols * cell_w, margin * 2 + rows * cell_h + 60)
    d.text((margin, 18), "Qalezu: every glyph, with its name, sound and code point", fill=GREY,
           font=label_font(22))
    lab = label_font(19)
    size = 130
    for i, (name, sound, cp, ch) in enumerate(cells):
        cx = margin + (i % cols) * cell_w
        cy = margin + 60 + (i // cols) * cell_h
        d.rectangle([cx, cy, cx + cell_w - 1, cy + cell_h - 1], outline=RULE)
        baseline = cy + 150
        d.line([cx + 10, baseline, cx + cell_w - 10, baseline], fill=RULE)
        s = shaped(r, ch)
        w = s.advance * size / r.upem
        r.draw(img, cx + (cell_w - w) / 2, baseline, s, size, INK)
        d.text((cx + 12, cy + cell_h - 78), name, fill=INK, font=lab)
        d.text((cx + 12, cy + cell_h - 54), sound, fill=GREY, font=lab)
        d.text((cx + 12, cy + cell_h - 30), cp, fill=GREY, font=lab)
    img.save(out)


def gloss_of(data: dict) -> dict[str, str]:
    out = {}
    for w in data["words"]:
        g = w["gloss"]
        g = g[0] if isinstance(g, list) else g
        for sep in (", ", "; ", " —", "—"):
            g = g.split(sep, 1)[0]
        out[w["form"]] = g
    return out


def words(r: Renderer, data: dict, out: Path):
    gloss = {**gloss_of(data), **NAMES}
    width, margin, row_h = 1500, 40, 190
    img, d = page(width, margin * 2 + 60 + len(WORDS) * row_h)
    d.text((margin, 18), "Khelathi words and names in Qalezu, written right to left", fill=GREY,
           font=label_font(22))
    big, lab = 130, label_font(26)
    for i, word in enumerate(WORDS):
        y = margin + 60 + i * row_h
        d.line([margin, y + row_h - 8, width - margin, y + row_h - 8], fill=RULE)
        s = shaped(r, guard.convert(word))
        right = width - margin - 520
        x = right - s.advance * big / r.upem
        r.draw(img, x, y + 125, s, big, INK)
        d.text((width - margin - 500, y + 50), word, fill=INK, font=label_font(34))
        d.text((width - margin - 500, y + 100), gloss.get(word, ""), fill=GREY, font=lab)
    img.save(out)


def mixed(r: Renderer, out: Path):
    width, margin = 1500, 50
    size, line_h = 100, 150
    img, d = page(width, 660)
    text = label_font(44)
    d.text((margin, 18), "A Qalezu name inside English, and a right-aligned block", fill=GREY,
           font=label_font(22))
    before, name, after = SENTENCE
    base = 150
    x = margin
    d.text((x, base - 52), before, fill=INK, font=text)
    x += d.textlength(before, font=text)
    s = shaped(r, guard.convert(name))
    r.draw(img, x, base + 5, s, size, INK)
    x += s.advance * size / r.upem + 8
    d.text((x, base - 52), after, fill=INK, font=text)
    d.line([margin, 215, width - margin, 215], fill=RULE)
    for i, line in enumerate(BLOCK):
        s = shaped(r, guard.convert(line))
        right = width - margin
        r.draw(img, right - s.advance * size / r.upem, 200 + i * line_h + 100, s, size, INK)
        d.text((margin, 200 + i * line_h + 60), line, fill=GREY, font=label_font(26))
    img.save(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--font", default=str(ROOT / "fonts" / "Qalezu-Regular.ttf"))
    ap.add_argument("--out", default=str(ROOT / "specimens" / "qalezu"))
    ap.add_argument("--thalorna", default=str(Path.home() / "dev/HeroicLands/thalorna"))
    ap.add_argument("--note", help="read the language note from this file instead of git")
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    r = Renderer(Path(args.font))
    data = guard.lexicon(Path(args.thalorna), Path(args.note) if args.note else None)
    glyph_chart(r, out / "01-glyph-chart.png")
    words(r, data, out / "02-words.png")
    mixed(r, out / "03-mixed.png")


if __name__ == "__main__":
    main()
