# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Render the hand's specimen sheets to PNG.

    .venv/bin/python tools/pirzath-hand/specimens.py [--font fonts/PirzathHand-Regular.ttf]
                                                  [--out specimens/pirzath-hand]

Five sheets: the glyph chart; the Khazari texts, each line lifted and then
joined; the owner's handwritten alphabet beside the font's glyphs, cell by
cell; one line at reading size, lifted and joined; and the owner's sheet of
changes beside the font's glyphs, cell by cell.
"""

import argparse
import importlib.util
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from render import Renderer, label_font  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent
PAPER = (248, 244, 236)
INK = (28, 24, 20)
GREY = (120, 112, 104)
RULE = (205, 198, 186)
JOINED = {"ss01": True}
OWNER_SHEET = ROOT / "design" / "pirzath-hand" / "owner-alphabet.jpg"
CHANGES_SHEET = ROOT / "design" / "pirzath-hand" / "owner-changes-1.jpg"


def _carved_specimens():
    spec = importlib.util.spec_from_file_location("pirzath_specimens", ROOT / "tools" / "pirzath" / "specimens.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CARVED = _carved_specimens()

# The texts shown in the hand, by their headings in the carved specimens.
TEXT_HEADINGS = ["The gate-cry", "The epitaph", "The forge oath", "The toast", "Phrasebook"]
TEXTS = [(h, lines) for h, lines in CARVED.TEXTS if h in TEXT_HEADINGS]

# The glyph chart: each glyph by the Latin that types it.
CHART = [
    ("p", "p"), ("b", "b"), ("f", "f"), ("v", "v"), ("m", "m"), ("t", "t"),
    ("d", "d"), ("th", "th"), ("dh", "dh"), ("n", "n"), ("k", "k"), ("g", "g"),
    ("kh", "kh"), ("gh", "gh"), ("h", "h"), ("s", "s"), ("z", "z"), ("l", "l"),
    ("r", "r"), ("a", "a"), ("e", "e"), ("i", "i"), ("o", "o"), ("u", "u"),
    ("á", "á"), ("é", "é"), ("í", "í"), ("ó", "ó"), ("ú", "ú"), ("ll (doubled)", "ll"),
    ("tth (doubled)", "tth"), ("kk (doubled)", "kk"),
    *CARVED.LOST_LETTERS,
    ("- dash", "-"), (". sentence end", "."), (", pause", ","), ("! or ¡", "!"),
    ('" opening', '"'), ('" closing', 'a"'), (".notdef", "?"),
    *[(f"{v} ({k})", k) for v, k in enumerate("0123456789@#$%^&")],
]

# The owner's sheet: each cell's box in the photo (x0, y0, x1, y1) and the Latin that types the
# font's glyph for it. The rows follow the carved glyph chart.
OWNER = [
    ("p", (160, 105, 265, 200), "p"), ("b", (295, 105, 408, 200), "b"), ("f", (430, 105, 556, 200), "f"),
    ("v", (580, 105, 694, 200), "v"), ("m", (712, 105, 822, 200), "m"),
    ("t", (145, 205, 250, 312), "t"), ("d", (268, 205, 385, 312), "d"), ("th", (405, 205, 508, 312), "th"),
    ("dh", (555, 205, 682, 312), "dh"), ("n", (712, 205, 798, 312), "n"),
    ("k", (136, 330, 204, 432), "k"), ("g", (224, 330, 320, 432), "g"), ("kh", (398, 325, 492, 432), "kh"),
    ("gh", (544, 330, 672, 432), "gh"), ("h", (712, 340, 772, 432), "h"),
    ("s", (125, 440, 218, 562), "s"), ("z", (243, 470, 342, 548), "z"), ("l", (388, 455, 470, 552), "l"),
    ("r", (568, 445, 634, 532), "r"), (".notdef", (700, 445, 762, 530), "?"),
    ("a", (130, 610, 194, 680), "a"), ("e", (252, 612, 326, 666), "e"), ("i", (368, 605, 412, 656), "i"),
    ("o", (543, 605, 597, 650), "o"), ("u", (672, 575, 748, 646), "u"),
    ("á", (110, 690, 188, 790), "á"), ("é", (242, 690, 333, 772), "é"), ("í", (362, 683, 420, 762), "í"),
    ("ó", (529, 690, 582, 748), "ó"), ("ú", (660, 662, 724, 756), "ú"),
    ("- dash", (100, 838, 156, 896), "-"), (". (sheet: —)", (250, 830, 312, 858), "."),
    (", pause", (366, 812, 412, 856), ","), ("! (sheet: =)", (510, 795, 572, 836), "!"),
    ("• (not used)", (672, 786, 699, 810), None),
    ('" opening', (96, 918, 170, 1012), '"'), ('" closing', (232, 895, 338, 982), 'a"'),
    ("ll", (366, 885, 456, 1014), "ll"), ("tth", (489, 893, 587, 1006), "tth"),
    ("sh", (96, 1045, 198, 1132), "sh"), ("zh", (224, 1035, 338, 1114), "zh"), ("ch", (366, 1030, 457, 1128), "ch"),
]

# The owner's sheet of changes: each cell's box under its label, and the Latin that types the
# font's glyph for it. Struck-out cells are left out.
CHANGES = [
    ("p", (150, 90, 270, 190), "p"), ("b", (320, 85, 440, 190), "b"), ("f", (480, 85, 600, 190), "f"),
    ("v", (630, 85, 740, 190), "v"), ("th", (770, 80, 920, 160), "th"), ("dh", (960, 80, 1070, 160), "dh"),
    ("k", (140, 270, 280, 380), "k"), ("g", (460, 280, 560, 350), "g"), ("kh", (580, 270, 690, 350), "kh"),
    ("gh", (740, 270, 860, 350), "gh"), ("s", (1000, 250, 1110, 330), "s"),
    ("z", (140, 430, 280, 520), "z"), ("h", (310, 430, 420, 520), "h"), ("a", (460, 430, 570, 520), "a"),
    ("e", (580, 420, 700, 500), "e"), ("i", (720, 420, 790, 500), "i"), ("o", (840, 410, 950, 490), "o"),
    ("u", (960, 410, 1050, 490), "u"), ("the catch", (1180, 390, 1250, 460), "'"),
    ("á", (140, 600, 290, 690), "á"), ("é", (310, 600, 420, 690), "é"), ("í", (450, 600, 540, 690), "í"),
    ("ó", (550, 600, 640, 690), "ó"), ("ú", (640, 600, 750, 690), "ú"), ("y before a", (1160, 520, 1270, 610), "ya"),
    ("sh", (120, 740, 240, 830), "sh"), ("zh", (270, 740, 390, 830), "zh"), ("j", (540, 700, 650, 830), "j"),
    ("q", (780, 700, 890, 840), "q"), ("ng", (910, 700, 1020, 820), "ng"), ("hl", (1050, 700, 1170, 800), "hl"),
    ("w", (1170, 700, 1280, 800), "w"),
    ('" opening', (290, 860, 420, 940), '"'), ('" closing', (560, 860, 700, 940), 'a"'),
]

READING = "Gaz thumár, ves zummád.Dalk tasím.Ves mulágh nuv gazn zef.Thiz durákh tanv."


def page(width, height):
    img = Image.new("RGB", (width, height), PAPER)
    return img, ImageDraw.Draw(img)


def shaped_for(r: Renderer, text: str, features=None):
    """The text as the font shapes it. A closing quote is shown alone, and a lone glide keeps its first glyph."""
    shaped = r.shape(text, features)
    if text == 'a"' or text in CARVED.SHOW_FIRST_ONLY:
        keep = shaped.glyphs[1:] if text == 'a"' else shaped.glyphs[:1]
        dx = keep[0][1]
        shaped.glyphs = [(g, x - dx, y, adv) for g, x, y, adv in keep]
        shaped.advance = sum(g[3] for g in shaped.glyphs)
    return shaped


def glyph_chart(r: Renderer, out: Path):
    cols, cell_w, cell_h = 6, 230, 270
    rows = (len(CHART) + cols - 1) // cols
    margin = 40
    img, d = page(margin * 2 + cols * cell_w, margin * 2 + rows * cell_h + 60)
    d.text((margin, 18), "Pirzath Hand — glyph chart, by the Latin that types it", fill=GREY, font=label_font(22))
    lab = label_font(18)
    size = 150
    for i, (label, text) in enumerate(CHART):
        cx = margin + (i % cols) * cell_w
        cy = margin + 60 + (i // cols) * cell_h
        d.rectangle([cx, cy, cx + cell_w - 1, cy + cell_h - 1], outline=RULE)
        baseline = cy + 160
        d.line([cx + 10, baseline, cx + cell_w - 10, baseline], fill=RULE)
        shaped = shaped_for(r, text)
        w = shaped.advance * size / r.upem
        r.draw(img, cx + (cell_w - w) / 2, baseline, shaped, size, INK)
        d.text((cx + 10, cy + cell_h - 30), label, fill=GREY, font=lab)
    img.save(out)


def texts(r: Renderer, out: Path, size: int = 72):
    lab = label_font(20)
    head = label_font(24)
    line_h = int(size * 1.25)
    block = 2 * line_h + 36
    longest = max(max(r.width(ln, size), r.width(ln, size, JOINED)) for _, lines in TEXTS for ln in lines)
    width = int(longest + 220)
    total = 90 + sum(50 + len(lines) * block + 20 for _, lines in TEXTS)
    img, d = page(width, total)
    d.text((40, 20), "The Khazari texts, each line lifted and then joined (ss01)", fill=GREY, font=label_font(22))
    y = 80
    for heading, lines in TEXTS:
        d.text((40, y), heading, fill=INK, font=head)
        y += 50
        for ln in lines:
            for feats, tag in ((None, "lifted"), (JOINED, "joined")):
                base = y + int(size * 0.85)
                d.text((40, base - 22), tag, fill=GREY, font=label_font(15))
                r.text(img, 130, base, ln, size, INK, feats)
                y += line_h
            d.text((130, y - 8), ln, fill=GREY, font=lab)
            y += 36
        y += 20
    img.save(out)


def owner_alphabet(r: Renderer, out: Path, sheet=OWNER_SHEET, cells=OWNER,
                   title="The owner's alphabet, cell by cell, beside the font's glyph"):
    photo = Image.open(sheet).convert("RGB")
    cols, cell_w, cell_h = 5, 330, 230
    rows = (len(cells) + cols - 1) // cols
    margin = 40
    img, d = page(margin * 2 + cols * cell_w, margin * 2 + rows * cell_h + 60)
    d.text((margin, 18), title, fill=GREY, font=label_font(22))
    lab = label_font(18)
    size = 150
    for i, (label, box, text) in enumerate(cells):
        cx = margin + (i % cols) * cell_w
        cy = margin + 60 + (i // cols) * cell_h
        d.rectangle([cx, cy, cx + cell_w - 1, cy + cell_h - 1], outline=RULE)
        crop = photo.crop(box)
        k = min(140 / crop.width, 160 / crop.height, 1.6)
        crop = crop.resize((max(1, int(crop.width * k)), max(1, int(crop.height * k))))
        img.paste(crop, (cx + 8, cy + 8 + (160 - crop.height) // 2))
        if text is not None:
            shaped = shaped_for(r, text)
            w = shaped.advance * size / r.upem
            r.draw(img, cx + 160 + (cell_w - 170 - w) / 2, cy + 140, shaped, size, INK)
        d.text((cx + 10, cy + cell_h - 30), label, fill=GREY, font=lab)
    img.save(out)


def reading(r: Renderer, out: Path):
    sizes = [27, 36]
    width = int(max(r.width(READING, s, f) for s in sizes for f in (None, JOINED)) + 200)
    img, d = page(width, 70 + len(sizes) * 2 * 60 + 60)
    d.text((40, 20), "One line at reading size (consonants 18 px and 24 px tall), lifted and joined", fill=GREY,
           font=label_font(20))
    y = 90
    for s in sizes:
        for feats, tag in ((None, "lifted"), (JOINED, "joined")):
            d.text((40, y - 14), f"{tag}", fill=GREY, font=label_font(14))
            r.text(img, 120, y + 6, READING, s, INK, feats)
            y += 60
    d.text((120, y), READING, fill=GREY, font=label_font(16))
    img.save(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--font", default=str(ROOT / "fonts" / "PirzathHand-Regular.ttf"))
    ap.add_argument("--out", default=str(ROOT / "specimens" / "pirzath-hand"))
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    r = Renderer(Path(args.font))
    glyph_chart(r, out / "01-glyph-chart.png")
    texts(r, out / "02-texts.png")
    owner_alphabet(r, out / "03-owner-alphabet.png")
    reading(r, out / "04-reading-size.png")
    owner_alphabet(r, out / "05-owner-changes.png", CHANGES_SHEET, CHANGES,
                   "The owner's sheet of changes, cell by cell, beside the font's glyph")
    for p in sorted(out.glob("*.png")):
        print(p)


if __name__ == "__main__":
    main()
