# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Render the specimen sheets to PNG.

    .venv/bin/python tools/pirzath/specimens.py [--font fonts/PirzathCarved-Regular.ttf] [--out specimens/pirzath]

Six sheets: the glyph chart, the Khazari texts over their Latin at reading and
display size, the numerals, a paragraph of lexicon words, and the seventeen
lost letters with the spelling that types each.
"""

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from mapped import Mapping, MappedRenderer  # noqa: E402
from render import Renderer, label_font  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent
PAPER = (248, 244, 236)
INK = (28, 24, 20)
GREY = (120, 112, 104)
RULE = (205, 198, 186)

# The seventeen lost letters, each by the spelling that types it. A y types the
# glide only before a vowel, so it is shaped before one and shown alone.
LOST_LETTERS = [
    ("sh", "sh"), ("zh", "zh"), ("ch", "ch"), ("j", "j"), ("ts", "ts"),
    ("q", "q"), ("ng", "ng"), ("ny", "ny"), ("hl", "hl"), ("w", "w"),
    ("' or ’", "'"), ("y before a vowel", "ya"),
    ("ai", "ai"), ("au", "au"), ("ei", "ei"), ("oi", "oi"), ("ou", "ou"),
]
SHOW_FIRST_ONLY = {"ya"}

# Invented spellings that use the lost letters, for display only: they are not
# Khazari words. Each shows the letters in several positions, ay as the pair ai,
# and the glide y.
LOST_WORDS = [
    "shalmai", "zhoulin", "chembai", "jorqen", "tsaleik", "ngathu",
    "nyolwen", "hlanoi", "ya'ath", "waynor", "qashur", "jeinyok",
]

# The glyph chart: each glyph by the Latin that types it.
CHART = [
    ("p", "p"), ("b", "b"), ("f", "f"), ("v", "v"), ("m", "m"),
    ("t", "t"), ("d", "d"), ("th", "th"), ("dh", "dh"), ("n", "n"),
    ("k", "k"), ("g", "g"), ("kh", "kh"), ("gh", "gh"), ("h", "h"),
    ("s", "s"), ("z", "z"), ("l", "l"), ("r", "r"), (".notdef", "ȷ"),
    ("a", "a"), ("e", "e"), ("i", "i"), ("o", "o"), ("u", "u"),
    ("á", "á"), ("é", "é"), ("í", "í"), ("ó", "ó"), ("ú", "ú"),
    ("-", "-"), (".", "."), (",", ","), ("!", "!"), ("space", " "),
    ('“ opening', '“'), ('” closing', 'a”'), ("ll (doubled)", "ll"), ("tth (doubled)", "tth"),
    ("gh beside closing", "gh”"),
    *LOST_LETTERS,
]

# The texts, under the headings the language and culture notes use.
TEXTS = [
    ("The gate-cry", [
        "Thiz durákh tanv.",
        "Gazn.Gazn durákh tanv.",
        "Dalk.Bant.Tanv-guráz.",
    ]),
    ("The epitaph", [
        "Tanvan Ramk-sumád",
        "Vog narv dulák",
        "Narv zuvák, vog dubáz",
        "Mardh nabít",
    ]),
    ("The forge oath", [
        "Farz sudháv, dalk sudháv.",
        "Gaz bunát, bant durákh.",
        "Hiz bant hulágh, galdod thufár mardh.",
        "Dalík bant, maríg bant.",
    ]),
    ("The maker's mark", [
        "Galdan Gald-vulád",
        "Kedz savadh zatíg",
        "Gaz bumár, gaz fuvád",
    ]),
    ("The toast", [
        "Bamr bamír.",
        "Gatharir tamík.",
        "Gazn gulák nuv gatharir.",
    ]),
    ("The mastery frame, doubled", [
        "Vog dalkir, vog rummák ramk.",
        "Gaz thumár, ves zummád.",
        "Dulkun putthák, Rinit dullák.",
    ]),
    ("A record quoting an oath", [
        'Galdan bunát, “Dalík bant, maríg bant”.',
        "Lukum, “Narv zuvák, vog dubáz”.",
        "Guruz, “Gaz thurágh” gaz munád.",
        "Rinit, “!Ves durám”.",
        "!Ves durám bep gunádh nuv gaz.",
    ]),
    ("Phrasebook", [
        "Dalk tasím.",
        "Ramk tasím.",
        "Ves mulágh nuv gazn zef.",
        "Gaz huváz.",
        "Dalk durákh.",
        "Gaz Guruz, Tanv-guráz.",
    ]),
]

NUMERAL_SAMPLES = [("1@", "26"), ("25", "37, zik girm bep zop"), ("135", "309, the year of the finding")]

PARAGRAPH = (
    "dalk dalík dalkir dulák dullák ramk thamr bant varn vald dank tanv narv "
    "madak lubáz magar zagar gharp naghal hutabar khatab filnath mazadh zalm "
    "makas mullán galdod farz savadh halz girm bamr gatharir huzafal milgath "
    "mardh nefk khozm vunth thulk Khazár tob bozd Dalk-thumár Khalv-gunáv "
    "putthák gummáth purráz dunnák"
)


def typed(r: Renderer, text: str):
    """The text as the font shapes it; a lone glide keeps only its first glyph."""
    shaped = r.shape(text)
    if text in SHOW_FIRST_ONLY:
        shaped.glyphs = shaped.glyphs[:1]
        shaped.advance = shaped.glyphs[0][3]
    return shaped


def page(width, height):
    img = Image.new("RGB", (width, height), PAPER)
    return img, ImageDraw.Draw(img)


def glyph_chart(r: Renderer, out: Path):
    cols, cell_w, cell_h = 5, 230, 250
    rows = (len(CHART) + cols - 1) // cols
    margin = 40
    img, d = page(margin * 2 + cols * cell_w, margin * 2 + rows * cell_h + 60)
    d.text((margin, 18), "Pirzath Carved — glyph chart, by the Latin that types it", fill=GREY,
           font=label_font(22))
    lab = label_font(20)
    size = 130
    for i, (label, text) in enumerate(CHART):
        if not label:
            continue
        cx = margin + (i % cols) * cell_w
        cy = margin + 60 + (i // cols) * cell_h
        d.rectangle([cx, cy, cx + cell_w - 1, cy + cell_h - 1], outline=RULE)
        baseline = cy + 170
        d.line([cx + 10, baseline, cx + cell_w - 10, baseline], fill=RULE)
        if label == ".notdef":
            shaped = r.shape("ȷ")
        elif label == '" closing':
            # The closing form needs a letter before it; draw the mark alone.
            shaped = r.shape(text)
            _, dx, _, _ = shaped.glyphs[1]
            shaped.glyphs = [(g, x - dx, y, adv) for g, x, y, adv in shaped.glyphs[1:]]
            shaped.advance -= dx
        else:
            shaped = typed(r, text)
        w = shaped.advance * size / r.upem
        r.draw(img, cx + (cell_w - w) / 2, baseline, shaped, size, INK)
        d.text((cx + 12, cy + cell_h - 34), label, fill=GREY, font=lab)
    img.save(out)


def lost_letters(r: Renderer, out: Path):
    cols, cell_w, cell_h = 6, 230, 250
    rows = (len(LOST_LETTERS) + cols - 1) // cols
    margin = 40
    block_h = rows * cell_h
    word_size, word_h = 80, 150
    width = margin * 2 + cols * cell_w
    height = margin + 60 + block_h + 70 + 4 * word_h + 40
    img, d = page(width, height)
    d.text((margin, 18), "The seventeen lost letters, each over the spelling that types it",
           fill=GREY, font=label_font(22))
    lab = label_font(20)
    size = 130
    for i, (label, text) in enumerate(LOST_LETTERS):
        cx = margin + (i % cols) * cell_w
        cy = margin + 60 + (i // cols) * cell_h
        d.rectangle([cx, cy, cx + cell_w - 1, cy + cell_h - 1], outline=RULE)
        baseline = cy + 170
        d.line([cx + 10, baseline, cx + cell_w - 10, baseline], fill=RULE)
        shaped = typed(r, text)
        w = shaped.advance * size / r.upem
        r.draw(img, cx + (cell_w - w) / 2, baseline, shaped, size, INK)
        d.text((cx + 12, cy + cell_h - 34), label, fill=GREY, font=lab)
    y = margin + 60 + block_h + 30
    d.text((margin, y), "Invented spellings for display only, not Khazari words", fill=GREY,
           font=label_font(22))
    y += 40
    per_row = 3
    col_w = (width - 2 * margin) // per_row
    for i, word in enumerate(LOST_WORDS):
        x = margin + (i % per_row) * col_w
        base = y + (i // per_row) * word_h + int(word_size * 0.8)
        r.text(img, x, base, word, word_size, INK)
        d.text((x, base + 14), word, fill=GREY, font=lab)
    img.save(out)


def texts(r: Renderer, out: Path, size: int, title: str):
    lab_size = max(13, int(size * 0.42))
    lab = label_font(lab_size)
    head = label_font(int(lab_size * 1.1))
    line_h = int(size * 1.15)
    block_h = line_h + lab_size + 14
    longest = max(r.width(line, size) for _, lines in TEXTS for line in lines)
    width = int(max(longest, max(label_font(lab_size).getlength(l) for _, ls in TEXTS for l in ls)) + 130)
    total = 90
    for _, lines in TEXTS:
        total += int(lab_size * 1.6) + int(size * 0.15) + len(lines) * block_h + 20
    img, d = page(width, total)
    d.text((40, 20), title, fill=GREY, font=label_font(22))
    y = 80
    for heading, lines in TEXTS:
        d.text((40, y), heading, fill=INK, font=head)
        y += int(lab_size * 1.6) + int(size * 0.15)
        for line in lines:
            baseline = y + int(size * 0.78)
            r.text(img, 60, baseline, line, size, INK)
            d.text((60, baseline + 10), line, fill=GREY, font=lab)
            y += block_h
        y += 20
    img.save(out)


def numerals(r: Renderer, out: Path):
    size = 110
    img, d = page(1500, 720)
    d.text((40, 20), "Numerals: nought to fifteen, typed 0-9 and @ # $ % ^ &, then numbers",
           fill=GREY, font=label_font(22))
    lab = label_font(20)
    x = 60
    for v in range(16):
        s = "0123456789@#$%^&"[v]
        baseline = 240
        w = r.text(img, x, baseline, s, size, INK)
        d.text((x + 4, baseline + 12), f"{v} ({s})", fill=GREY, font=lab)
        x += max(w, 70) + 16
    x = 60
    baseline = 540
    for s, meaning in NUMERAL_SAMPLES:
        w = r.text(img, x, baseline, s, size, INK)
        d.text((x + 4, baseline + 12), f"{s} = {meaning}", fill=GREY, font=lab)
        x += max(w, lab.getlength(f"{s} = {meaning}")) + 60
    # A number beside a word.
    s = "girm 10 bep tob 1"
    baseline = 680
    r.text(img, 60, baseline - 30, s, 60, INK)
    d.text((60, baseline - 10), s, fill=GREY, font=lab)
    img.save(out)


def paragraph(r: Renderer, out: Path, size: int = 40):
    width, margin = 1300, 60
    words = PARAGRAPH.split()
    space_w = r.width(" ", size)
    lines, line, x = [], [], 0
    for w in words:
        ww = r.width(w, size)
        if line and x + ww > width - 2 * margin:
            lines.append(" ".join(line))
            line, x = [], 0
        line.append(w)
        x += ww + space_w
    lines.append(" ".join(line))
    line_h = int(size * 1.5)
    img, d = page(width, 100 + line_h * len(lines) + 60 + 30 * ((len(words) + 7) // 8))
    d.text((40, 20), "Lexicon words in running text, reading size", fill=GREY, font=label_font(22))
    y = 70
    for ln in lines:
        r.text(img, margin, y + int(size * 0.8), ln, size, INK)
        y += line_h
    lab = label_font(18)
    y += 20
    for i in range(0, len(words), 8):
        d.text((margin, y), "  ".join(words[i : i + 8]), fill=GREY, font=lab)
        y += 30
    img.save(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--font", default=str(ROOT / "fonts" / "PirzathCarved-Regular.ttf"))
    ap.add_argument("--out", default=str(ROOT / "specimens" / "pirzath"))
    ap.add_argument("--thalorna", default=str(Path.home() / "dev/HeroicLands/thalorna"),
                    help="the checkout whose mapping notes write the roman texts")
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    r = MappedRenderer(Renderer(Path(args.font)), Mapping("pirzath", thalorna=Path(args.thalorna), face="pirzath-carved"))
    glyph_chart(r, out / "01-glyph-chart.png")
    texts(r, out / "02-texts-reading.png", 36, "The Khazari texts at reading size")
    texts(r, out / "03-texts-display.png", 96, "The Khazari texts at display size")
    numerals(r, out / "04-numerals.png")
    paragraph(r, out / "05-paragraph.png")
    lost_letters(r, out / "06-lost-letters.png")
    for p in sorted(out.glob("*.png")):
        print(p)


if __name__ == "__main__":
    main()
