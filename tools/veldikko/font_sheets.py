# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Render the Veldikko joining sheets through the built font.

    .venv/bin/python tools/veldikko/font_sheets.py [--font fonts/Veldikko-Regular.ttf]
                                             [--out specimens/veldikko] [forms|joined|verse|sizes|beside ...]

Everything here is shaped by HarfBuzz from the font's code points and drawn from
its own outlines (``tools/render.py``), so a sheet shows what a page shows.

- ``forms.png``: every letter in its four forms, isolated, initial, medial and
  final, then the stretched forms and the long tails;
- ``joined.png``: the words of ``words.png`` set by the font, Sinale and Áelendi;
- ``verse.png``: the Sinale sample phrases as a verse block at generous line
  height, the marks of pitch and emphasis, and Veldikko words inside a paragraph
  of English at its own line height;
- ``sizes.png``: running text at 48, 32, 24 and 20 px to the em;
- ``beside.png``: a line of Veldikko beside the same words in Semaron Kuriale and in
  a Latin face, at 20, 24 and 48 px to the em, on one baseline, with the shared
  x-height ruled at 48 px: the bowls stand at the x-height, the extenders beyond.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(1, str(HERE))
from render import Renderer, label_font  # noqa: E402

PAPER = (243, 239, 228)
INK = (28, 34, 40)
GREY = (118, 112, 100)
RED = (176, 48, 36)
RULE = (212, 202, 180)
ENC = json.loads((HERE / "encoding.json").read_text(encoding="utf-8"))
BY_LETTER = {r["letter"]: chr(int(r["codepoint"][2:], 16)) for r in ENC["glyphs"] if r["kind"] == "letter"}
BY_GLYPH = {r["glyph"]: chr(int(r["codepoint"][2:], 16)) for r in ENC["glyphs"]}
VOWEL = {r["vowel"]: chr(int(r["codepoint"][2:], 16)) for r in ENC["glyphs"] if r["kind"] == "vowel"}
SIGN = {":": BY_GLYPH["long"], "/": BY_GLYPH["rise"], "\\": BY_GLYPH["fall"], "!": BY_GLYPH["emph"]}
SPELLING = {"aelendi": {"dh": "dhA"}}


def spelled(spelling: str, tongue: str = "sinale") -> str:
    """Code points from a letter-by-letter spelling, as ``letters.parse_word`` reads it:
    ``"k+a l p+i"`` is _kalpi_; ``=`` after a letter is the bar; ``:`` long, ``/``
    rising, ``\\`` falling and ``!`` emphasis follow their vowel; ``|`` is a word space."""
    out = []
    for tok in spelling.split():
        if tok == "|":
            out.append(" ")
            continue
        head, _, marks = tok.partition("+")
        bar = head.endswith("=")
        head = head.rstrip("=")
        out.append(BY_LETTER[SPELLING.get(tongue, {}).get(head, head)])
        if bar:
            out.append(BY_GLYPH["bar"])
        out += [VOWEL.get(c) or SIGN[c] for c in marks]
    return "".join(out)


def convert(words: list[str]) -> list[str]:
    result = subprocess.run(["node", str(ROOT / "tools" / "convert_batch.mjs"), "Veldikko"],
                            input=json.dumps(words), check=True, capture_output=True, text=True)
    out = []
    for w, r in zip(words, json.loads(result.stdout)):
        if "letter" in r:
            raise SystemExit(f"{w!r}: the Veldikko has no sign for {r['letter']!r}")
        out.append(r["text"])
    return out


def put(r: Renderer, img, text, size, right, baseline, features=None, color=INK):
    """Set text right-aligned at ``right``; returns its left edge."""
    shaped = r.shape(text, features, direction="rtl")
    w = shaped.advance * size / r.upem
    r.draw(img, right - w, baseline, shaped, size, color)
    return right - w


def glyph_row(r: Renderer, img, names, size, right, baseline, gap):
    """Draw named glyphs right to left, each in its own cell."""
    x = right
    for name in names:
        gid = r.order.index(name)
        adv = r.tt["hmtx"][name][0]
        from render import Shaped
        r.draw(img, x - adv * size / r.upem, baseline, Shaped([(gid, 0, 0, adv)], adv), size)
        x -= adv * size / r.upem + gap
    return x


LETTERS = ["p", "v", "m", "t", "s", "n", "d", "dh", "k", "h", "ng", "l", "r", "carrier",
           "g", "th", "dhasp", "kh", "gh", "tej", "dej", "kej", "gej"]


def forms_sheet(r: Renderer, out: Path):
    W, size = 2400, 150
    rows = len(LETTERS)
    H = 230 + rows * 330 + 1200
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.text((40, 30), "Veldikko — layer 3: every letter in its four forms", fill=INK, font=label_font(46))
    d.text((40, 94), "Read from the right: isolated, initial, medial, final, then the initial and medial stretched. "
           "A grey rule marks each form's advance; the joins meet at its edges.", fill=GREY, font=label_font(22))
    heads = ["isolated", "initial", "medial", "final", "initial, stretched", "medial, stretched"]
    xs = [W - 60 - i * 380 for i in range(6)]
    for x, h in zip(xs, heads):
        d.text((x - 340, 150), h, fill=RED, font=label_font(22))
    y = 200
    for g in LETTERS:
        base = y + 250
        names = [g, f"{g}.init", f"{g}.medi", f"{g}.fina", f"{g}.init.wide", f"{g}.medi.wide"]
        for x, name in zip(xs, names):
            adv = r.tt["hmtx"][name][0] * size / r.upem
            d.line([(x - adv, base + 40), (x, base + 40)], fill=RULE, width=2)
            d.line([(x - adv, base + 30), (x - adv, base + 50)], fill=RULE, width=2)
            d.line([(x, base + 30), (x, base + 50)], fill=RULE, width=2)
            glyph_row(r, img, [name], size, x, base, 0)
        d.text((40, base - 40), {"carrier": "carrier", "dhasp": "dh (Áelendi)", "tej": "t'", "dej": "d'",
                                 "kej": "k'", "gej": "g'"}.get(g, g), fill=INK, font=label_font(30))
        y += 330
    d.text((40, y + 20), "The long tails of a word's last nasal: hook, sweep (ss01), ezh (ss02); isolated, then final",
           fill=RED, font=label_font(24))
    y += 80
    for g in ("m", "n", "ng"):
        base = y + 230
        names = [g, f"{g}.sweep", f"{g}.ezh", f"{g}.fina", f"{g}.fina.sweep", f"{g}.fina.ezh"]
        for x, name in zip(xs, names):
            glyph_row(r, img, [name], size, x, base, 0)
        d.text((40, base - 40), g, fill=INK, font=label_font(30))
        y += 340
    img.crop((0, 0, W, y + 30)).save(out)
    return out


SINALE_WORDS = [
    ("nuuva", "starlight"), ("mollu", "deep pool"), ("molu", "the colour of a deep pool"),
    ("kalpi", "pale wood"), ("halpi", "pale wood, worn"), ("eilava", "the wide sky"), ("aamas", "the void"),
    ("rivy", "the turning leaf"), ("ennedhi", "a tale"), ("lonku", "the deep wood"), ("leësy", "a path"),
    ("huoma", "the first warmth"),
]
AELENDI_WORDS = [
    ("khalthon", "a lodge", "kh+a l th+o n"),
    ("ghoran", "a head", "gh+o r+a n"),
    ("thidharon", "a mark cut in a boundary stone", "th+i dh+a r+o n"),
    ("gulmesa", "a riding", "g+u l m+e s+a"),
]


def joined_sheet(r: Renderer, out: Path):
    W, size = 2400, 130
    rows = len(SINALE_WORDS) + len(AELENDI_WORDS)
    img = Image.new("RGB", (W, 260 + rows * 300 + 120), PAPER)
    d = ImageDraw.Draw(img)
    d.text((40, 30), "Veldikko — layer 3: words, joined, set by the font", fill=INK, font=label_font(46))
    d.text((40, 94), "The words of the letters sheet, shaped right to left from their code points. Right: display size; "
           "left of it: 48 px. Each Sinale word converted from its romanization.", fill=GREY, font=label_font(22))
    y = 170
    texts = convert([w for w, _ in SINALE_WORDS])
    d.text((40, y), "Sinale", fill=RED, font=label_font(30))
    y += 40
    for (rom, gloss), text in zip(SINALE_WORDS, texts):
        base = y + 200
        put(r, img, text, size, W - 80, base)
        put(r, img, text, 48, W - 1000, base)
        d.text((40, y + 90), rom, fill=INK, font=label_font(34))
        d.text((40, y + 138), gloss, fill=GREY, font=label_font(20))
        y += 300
    d.text((40, y), "Áelendi, from its letter-by-letter spelling", fill=RED, font=label_font(30))
    y += 40
    for rom, gloss, sp in AELENDI_WORDS:
        base = y + 200
        text = spelled(sp, "aelendi")
        put(r, img, text, size, W - 80, base)
        put(r, img, text, 48, W - 1000, base)
        d.text((40, y + 90), rom, fill=INK, font=label_font(34))
        d.text((40, y + 138), gloss, fill=GREY, font=label_font(20))
        d.text((40, y + 168), sp, fill=GREY, font=label_font(18))
        y += 300
    img.crop((0, 0, W, y + 20)).save(out)
    return out


VERSE = [
    ("Luuro nuuva liseriho", "Starlight sings on still water"),
    ("Li-setty lenti talveho", "The tall grass stands in the low fog"),
    ("Ha-tupe tilvai hyssen", "The seam of light has held the breath"),
]
# The same lines with the pitch the romanization drops: level through the line, falling
# at its close; and one word given emphasis.
TUNED = [
    ("l+u: r+o | n+u: v+a | l+i s+e r+i h+o\\", "falling at the close"),
    ("l+u: r+o | n+u:! v+a | l+i s+e r+i h+o/", "nuuva emphasised, rising at the close: a question"),
]


BLOCK_LEADING = 2.4  # a verse block's line height, in ems, room for the risers and tails
PARAGRAPH = [
    ["The Sinale call their script ", "veldikko", ", the gathered hand, and a page of it is"],
    ["read slowly. A greeting between friends, ", "luuro nuuva liseriho", ", is the commonest line"],
    ["a traveller meets, written above a door or across the foot of a letter."],
]


def verse_sheet(r: Renderer, out: Path):
    W = 2400
    img = Image.new("RGB", (W, 2800), PAPER)
    d = ImageDraw.Draw(img)
    d.text((40, 30), "Veldikko — layer 3: verse", fill=INK, font=label_font(46))
    d.text((40, 94), f"Sample phrases of the Sinale note as a right-aligned block at 64 px, line height {BLOCK_LEADING} em; "
           "then at 40 px with the English beside them; then Veldikko words inside an English paragraph.",
           fill=GREY, font=label_font(22))
    y = 180
    texts = convert([v for v, _ in VERSE])
    for text in texts:
        put(r, img, text, 64, W - 80, y + BLOCK_LEADING * 64 * 0.62)
        y += BLOCK_LEADING * 64
    y += 40
    for (rom, eng), text in zip(VERSE, texts):
        put(r, img, text, 40, W - 80, y + 40)
        d.text((40, y), f"{rom} — “{eng}”", fill=GREY, font=label_font(22))
        y += 100
    y += 40
    d.text((40, y), "Pitch and emphasis, which the romanization drops", fill=RED, font=label_font(28))
    y += 60
    for sp, what in TUNED:
        put(r, img, spelled(sp), 64, W - 80, y + 110)
        d.text((40, y + 40), what, fill=GREY, font=label_font(22))
        y += 190
    y += 30
    d.text((40, y), "Inline in an English paragraph: 36 px, line height 1.5 em, the lines evenly spaced", fill=RED,
           font=label_font(28))
    y += 80
    px, pitch = 36, 54
    font = label_font(px)
    words = convert([part for line in PARAGRAPH for part in line[1:2]])
    k = 0
    for line in PARAGRAPH:
        base = y + px
        x = 40.0
        for n, part in enumerate(line):
            if n == 1:
                text = words[k]
                k += 1
                w = r.width(text, px, direction="rtl")
                put(r, img, text, px, x + w, base)
                x += w
            else:
                d.text((x, base), part, fill=INK, font=font, anchor="ls")
                x += d.textlength(part, font=font)
        y += pitch
    img.crop((0, 0, W, int(y + 60))).save(out)
    return out


def sizes_sheet(r: Renderer, out: Path, zoom: int = 6):
    W = 2400
    text = "   ".join(convert([v for v, _ in VERSE]))
    img = Image.new("RGB", (W, 1700), PAPER)
    d = ImageDraw.Draw(img)
    d.text((40, 30), "Veldikko — layer 3: text sizes", fill=INK, font=label_font(46))
    d.text((40, 94), f"The verse at 48, 32, 24 and 20 px to the em; then 24 and 20 px enlarged {zoom}x without "
           "smoothing.", fill=GREY, font=label_font(22))
    y = 170
    for px in (48, 32, 24, 20):
        put(r, img, text, px, W - 60, y + px * 1.5)
        d.text((40, y), f"{px} px", fill=GREY, font=label_font(20))
        y += int(px * 2.2) + 30
    for px in (24, 20):
        w = int(r.width(text, px, direction="rtl")) + 8
        small = Image.new("RGB", (w, int(px * 2.2)), PAPER)
        put(r, small, text, px, w - 4, int(px * 1.55))
        part = small.crop((max(0, w - (W - 80) // zoom), 0, w, small.height))
        big = part.resize((part.width * zoom, part.height * zoom), Image.NEAREST)
        img.paste(big, (W - 40 - big.width, y))
        d.text((40, y), f"{px} px, enlarged", fill=GREY, font=label_font(20))
        y += big.height + 30
    img.crop((0, 0, W, y + 20)).save(out)
    return out


BESIDE = "luuro nuuva liseriho"


def beside_sheet(r: Renderer, out: Path):
    W = 2400
    semaron = Renderer(ROOT / "fonts" / "SemaronKuriale-Regular.ttf")
    text = convert([BESIDE])[0]
    img = Image.new("RGB", (W, 1400), PAPER)
    d = ImageDraw.Draw(img)
    d.text((40, 30), "Veldikko beside Semaron Kuriale and Latin", fill=INK, font=label_font(46))
    d.text((40, 94), f"“{BESIDE}” set at one size in each: right, Veldikko; middle, Semaron Kuriale; left, a Latin face. "
           "The bowls stand at the shared x-height; the risers, stems and tails reach beyond it.", fill=GREY,
           font=label_font(22))
    y = 230
    for px in (20, 24, 48):
        base = y + px * 1.5
        if px >= 24:
            xh = base - 0.5135 * px
            for level in (base, xh):
                d.line([(40, level), (W - 40, level)], fill=RULE, width=1)
            d.text((W * 0.62, xh - 22), "x-height", fill=GREY, font=label_font(16))
        put(r, img, text, px, W - 60, base)
        w = semaron.width(BESIDE, px, direction="ltr")
        semaron.draw(img, W * 0.42, base, semaron.shape(BESIDE, direction="ltr"), px)
        latin = label_font(px)
        d.text((140, base), BESIDE, fill=INK, font=latin, anchor="ls")
        d.text((40, y), f"{px} px", fill=GREY, font=label_font(18))
        y += int(px * 2.6) + 60
    img.crop((0, 0, W, y + 20)).save(out)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--font", default=str(ROOT / "fonts" / "Veldikko-Regular.ttf"))
    ap.add_argument("--out", type=Path, default=ROOT / "specimens" / "veldikko")
    ap.add_argument("only", nargs="*", help="forms, joined, verse, sizes, beside; all by default")
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    r = Renderer(Path(a.font))
    sheets = {"forms": forms_sheet, "joined": joined_sheet, "verse": verse_sheet, "sizes": sizes_sheet,
              "beside": beside_sheet}
    for name, make in sheets.items():
        if a.only and name not in a.only:
            continue
        print(make(r, a.out / f"{name}.png"))


if __name__ == "__main__":
    main()
