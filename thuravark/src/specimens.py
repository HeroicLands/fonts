# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Render the Thuravark Runic specimen sheets to PNG.

    .venv/bin/python thuravark/src/specimens.py [--font thuravark/fonts/ThuravarkRunic-Regular.ttf]
                                                [--pirzath fonts/PirzathCarved-Regular.ttf]
                                                [--out specimens/thuravark]

Four sheets: the glyph chart with each stave's typed input and sound, Nordmal
text set continuously over its Latin, the numerals with sample numbers, and
each stave beside the Pirzath letter it descends from.
"""

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))
from render import Renderer, label_font  # noqa: E402

HERE = Path(__file__).resolve().parent.parent
ROOT = HERE.parent
PAPER = (248, 244, 236)
INK = (28, 24, 20)
GREY = (120, 112, 104)
RULE = (205, 198, 186)
RED = (150, 40, 30)

# Each stave: glyph name, sound, the Latin that types it, and the Pirzath letter it descends from.
STAVE_TABLE = [
    ('a', 'a', 'a', 'a'),
    ('e', 'e', 'e', 'e'),
    ('i', 'i', 'i, y not before a vowel', 'i'),
    ('o', 'o', 'o', 'o'),
    ('u', 'u', 'u', 'u'),
    ('p', 'p', 'p', 'p'),
    ('b', 'b', 'b', 'b'),
    ('f', 'f', 'f', 'f'),
    ('v', 'v', 'v', 'v'),
    ('t', 't', 't', 't'),
    ('d', 'd', 'd', 'd'),
    ('th', 'th', 'th', 'th'),
    ('dh', 'dh', 'dh', 'dh'),
    ('k', 'k', 'k', 'k'),
    ('g', 'g', 'g', 'g'),
    ('kh', 'kh', 'kh', 'kh'),
    ('gh', 'gh', 'gh', 'gh'),
    ('s', 's', 's', 's'),
    ('z', 'z', 'z', 'z'),
    ('h', 'h', 'h', 'h'),
    ('l', 'l', 'l', 'l'),
    ('r', 'r', 'r', 'r'),
    ('hl', 'hl', 'hl', 'hl'),
    ('m', 'm', 'm', 'm'),
    ('n', 'n', 'n', 'n'),
    ('ng', 'ng', 'ng', 'ng'),
    ('j', 'y (glide)', 'j, y before a vowel', 'y'),
    ('w', 'w', 'w', 'w'),
]

# The fillers are staves Nordmal does not write.
FILLERS = {"dh", "kh", "gh", "z", "w"}

# Lines of real Nordmal: lexicon words, given names and clan names. Each word is
# typed with spaces, which draw nothing, so the runes run on.
LINES = [
    ("A saga, a praise-poem, a lament", "storald geldra hnura"),
    ("A king, a high seat, a seat at the ting", "Hringsveld hofudsveld tingsveld"),
    ("Women's names", "Hlarthrinna Hvalgselda Dvarnthira Druskinda"),
    ("Men's names", "Dvalgmil Braldvir Draskmil Bruldthann"),
    ("Clan names", "Althendik Braldaruk Druskidrok Dvulgumak"),
    ("A whale, a seal, the ice-edge, a rookery", "hvelm dvon skelfr dvonvangr"),
    ("Death, a grave, a pyre, a ship-burial", "svelth dulm eldsdulm skipsdulm"),
    ("The glide and the long vowels", "bjarn bjart jel járn skjálf hrúmverdir nágengir"),
]

NUMBER_SAMPLES = [
    ("10", "ten"), ("26", "twenty-six"), ("128", "128 in tens"),
    ("905", "nine hundred five"), ("2026", "two thousand twenty-six"),
    ("0i0", "nought, i, nought"),
]

# What each stave descends from, as typed in Pirzath Carved.
PARENT_TEXT = {"j": "ya"}
SHOW_FIRST_ONLY = {"ya"}

WORDS = ["dalk", "hrum", "bant", "narv", "thulm", "gnarth", "svelth", "hvelm"]


def page(width, height):
    img = Image.new("RGB", (width, height), PAPER)
    return img, ImageDraw.Draw(img)


def centred(r, img, cx, baseline, text, size, color=INK, first_only=False):
    shaped = r.shape(text)
    if first_only:
        shaped.glyphs = shaped.glyphs[:1]
        shaped.advance = shaped.glyphs[0][3]
    w = shaped.advance * size / r.upem
    r.draw(img, cx - w / 2, baseline, shaped, size, color)


def glyph_chart(r: Renderer, out: Path):
    cols, cell_w, cell_h = 7, 210, 330
    cells = [(row[0], row[2], row[1]) for row in STAVE_TABLE]
    extras = [
        (".", ". sentence end", ""), ("aa", "aa long vowel", "a twice"),
        ("á", "á long vowel", "a twice"), ("nn", "nn doubled", "n twice"),
        ("th th", "tth doubled", "th twice"), ("c", "c, q, x no stave", "blank stele"),
        ("a-r", "- draws nothing", "breaks a ligature"),
    ]
    rows = (len(cells) + len(extras) + cols - 1) // cols
    margin = 40
    img, d = page(margin * 2 + cols * cell_w, margin * 2 + rows * cell_h + 60)
    d.text((margin, 18), "Thuravark Runic — the 28 staves, by the Latin that types each",
           fill=GREY, font=label_font(22))
    lab = label_font(19)
    small = label_font(16)
    size = 170
    items = [(g, f"typed {t.split(',')[0]}", f"sound {s}", g in FILLERS) for g, t, s in cells]
    for (key, label, sub) in extras:
        text = {"th th": "tth", "a-r": "a-r"}.get(key, key)
        items.append((text, label, sub, False))
    for i, (key, label, sub, filler) in enumerate(items):
        cx = margin + (i % cols) * cell_w
        cy = margin + 60 + (i // cols) * cell_h
        d.rectangle([cx, cy, cx + cell_w - 1, cy + cell_h - 1], outline=RULE)
        baseline = cy + 235
        d.line([cx + 10, baseline, cx + cell_w - 10, baseline], fill=RULE)
        centred(r, img, cx + cell_w / 2, baseline, key, size if len(key) < 3 and key != 'nn' else 100)
        d.text((cx + 12, cy + cell_h - 62), label, fill=INK, font=lab)
        d.text((cx + 12, cy + cell_h - 34), sub + ("  · filler" if filler else ""),
               fill=RED if filler else GREY, font=small)
    img.save(out)


def texts(r: Renderer, out: Path, size: int = 64):
    lab = label_font(24)
    head = label_font(20)
    line_h = int(size * 1.3)
    longest = max(r.width(t, size) for _, t in LINES)
    width = int(max(longest, 900) + 180)
    img, d = page(width, 100 + len(LINES) * (line_h + 70))
    d.text((40, 20), "Nordmal in Thuravark Runic, set continuously, with the Latin under each line",
           fill=GREY, font=label_font(22))
    y = 80
    for heading, text in LINES:
        d.text((60, y), heading, fill=GREY, font=head)
        baseline = y + 30 + int(size * 0.98)
        r.text(img, 60, baseline, text, size, INK)
        d.text((60, baseline + 22), text, fill=INK, font=lab)
        y += line_h + 70
    img.save(out)


def numerals(r: Renderer, out: Path):
    size = 150
    img, d = page(1500, 760)
    d.text((40, 20), "Numerals 0-9, typed with the digits, taller than the staves, then numbers",
           fill=GREY, font=label_font(22))
    lab = label_font(22)
    x, baseline = 70, 260
    for v in range(10):
        w = r.text(img, x, baseline, str(v), size, INK)
        d.text((x + 4, baseline + 16), f"{v}", fill=GREY, font=lab)
        x += max(w, 90) + 40
    d.line([50, baseline, 1450, baseline], fill=RULE)
    x, baseline = 70, 520
    for s, meaning in NUMBER_SAMPLES:
        w = r.text(img, x, baseline, s, 120, INK)
        d.text((x + 4, baseline + 16), f"{s}  {meaning}", fill=GREY, font=label_font(17))
        x += max(w, 330) + 50
    d.line([50, baseline, 1450, baseline], fill=RULE)
    # Nought beside the stave i, and the numerals beside the full-height staves.
    r.text(img, 70, 700, "i0i 1i2i 3a4u 5i6i 7a8u9", 90, INK)
    d.text((70, 716), "i0i 1i2i 3a4u 5i6i 7a8u9", fill=GREY, font=label_font(17))
    img.save(out)


def descent(r: Renderer, p: Renderer, out: Path):
    cols, cell_w, cell_h = 7, 230, 330
    rows = (len(STAVE_TABLE) + cols - 1) // cols
    margin = 40
    word_h = 150
    img, d = page(margin * 2 + cols * cell_w,
                  margin * 2 + 60 + rows * cell_h + 80 + ((len(WORDS) + 3) // 4) * word_h * 2)
    d.text((margin, 18), "Each stave beside the Pirzath Carved letter it descends from",
           fill=GREY, font=label_font(22))
    lab = label_font(19)
    for i, row in enumerate(STAVE_TABLE):
        name, sound, typed, parent = row[0], row[1], row[2], row[3]
        cx = margin + (i % cols) * cell_w
        cy = margin + 60 + (i // cols) * cell_h
        d.rectangle([cx, cy, cx + cell_w - 1, cy + cell_h - 1], outline=RULE)
        baseline = cy + 235
        d.line([cx + 10, baseline, cx + cell_w - 10, baseline], fill=RULE)
        centred(r, img, cx + cell_w * 0.30, baseline, name, 150)
        ptext = PARENT_TEXT.get(name, parent)
        centred(p, img, cx + cell_w * 0.74, baseline, ptext, 110, INK, ptext in SHOW_FIRST_ONLY)
        d.text((cx + cell_w * 0.47, baseline - 150), "←", fill=GREY, font=lab)
        d.text((cx + 12, cy + cell_h - 34), f"{sound}   (typed {typed.split(',')[0]})", fill=GREY,
               font=label_font(17))
    y = margin + 60 + rows * cell_h + 40
    d.text((margin, y), "The same words: Thuravark over Pirzath Carved", fill=GREY, font=label_font(22))
    y += 40
    per = 4
    col_w = (img.size[0] - 2 * margin) // per
    for i, w in enumerate(WORDS):
        x = margin + (i % per) * col_w
        by = y + (i // per) * word_h * 2 + 80
        r.text(img, x, by, w, 80, INK)
        p.text(img, x, by + 80, w, 60, INK)
        d.text((x, by + 98), w, fill=GREY, font=label_font(17))
    img.save(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--font", default=str(HERE / "fonts" / "ThuravarkRunic-Regular.ttf"))
    ap.add_argument("--pirzath", default=str(ROOT / "fonts" / "PirzathCarved-Regular.ttf"))
    ap.add_argument("--out", default=str(ROOT / "specimens" / "thuravark"))
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    r = Renderer(Path(args.font))
    p = Renderer(Path(args.pirzath))
    glyph_chart(r, out / "01-glyph-chart.png")
    texts(r, out / "02-nordmal.png")
    numerals(r, out / "03-numerals.png")
    descent(r, p, out / "04-descent.png")
    for f in sorted(out.glob("*.png")):
        print(f)


if __name__ == "__main__":
    main()
