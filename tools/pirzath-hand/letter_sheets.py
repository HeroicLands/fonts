# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Render the Pirzath Hand letter sheet from the letters module.

    .venv/bin/python tools/pirzath-hand/letter_sheets.py [--out specimens/pirzath-hand/letters.png]
                                                         [--thalorna ~/dev/HeroicLands/thalorna]

The sheet shows every sign large with the roman that writes it; the sixteen digits
together; every sign at 24 and 48 px after Liberation Mono's "xhn"; and Khazari words
and the sample texts, written through the ``pirzath`` encoding, beside the
same words in a mixed-case Liberation Mono line and in Pirzath Carved, all at one font
size. The words come from the Khazari language note on thalorna's ``origin/main``.
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "tools"))
import letters as L  # noqa: E402
import strokes as S  # noqa: E402
from encoded import Encoded  # noqa: E402
from render import Renderer, latin_font  # noqa: E402
from strokes_sheet import BLUE, FAINT, GREY, INK, PAPER, RED, RULE, draw_path, font  # noqa: E402

CARVED_FONT = ROOT / "fonts/PirzathCarved-Regular.ttf"
KHAZARI = "assets/content/Skills/Languages/Khazari.md"
SAMPLES = [
    "thiz durákh tanv.",
    "gazn.gazn durákh tanv.",
    "dalk.bant.tanv-guráz.",
    "vog narv dulák",
    "gaz bunát, bant durákh.",
    "ves mulágh nuv gazn zef.",
    "gaz thumár, ves zummád.",
    "galdan bunát, \"dalík bant, maríg bant\".",
]
LONG_OF = {"a": "a", "e": "e", "i": "i", "o": "o", "u": "u"}


def glyph_names():
    """Code point to glyph name, as fonts.json lists them for the hand."""
    doc = json.loads((ROOT / "fonts.json").read_text(encoding="utf-8"))
    fam = next(f for f in doc["families"] if f["class"] == "hl-pirzath-hand")
    return {int(c["codepoint"][2:], 16): c["glyph"] for c in fam["codepoints"]}


GLYPHS = glyph_names()


def signs_of(cps: str):
    """The signs a written text is drawn with: a vowel and the length mark after it are
    one long vowel, a consonant written twice is its doubled sign, a space is a word
    space, and a character the hand does not draw is the box."""
    names = []
    for ch in cps:
        if ch == " ":
            names.append(None)
            continue
        g = GLYPHS.get(ord(ch), ".notdef")
        if g == "lengthmark" and names and names[-1] in L.VOWELS:
            names[-1] = names[-1] + ".long"
            continue
        if names and names[-1] == g and g in L.CONSONANTS:
            names[-1] = g + ".double"
            continue
        if g not in L.SIGNS:
            g = ".notdef"
        names.append(g)
    return names


def lexicon_words(thalorna: Path, n: int):
    """The first ``n`` distinct word forms of the Khazari note on ``origin/main``."""
    text = subprocess.run(["git", "-C", str(thalorna), "show", f"origin/main:{KHAZARI}"], capture_output=True,
                          text=True, check=True).stdout
    forms = []
    for m in re.finditer(r"(?:^|\{|\s)form:\s*\"?([^,\"}\n]+)", text):
        w = m.group(1).strip()
        if w not in forms:
            forms.append(w)
    return forms[:n]


def carved_image(r: Renderer, cps: str, px: float):
    w = int(r.width(cps, px)) + 20
    img = Image.new("RGB", (w, int(px * 1.5)), PAPER)
    r.text(img, 10, int(px * 1.1), cps, px, color=INK)
    return img, int(px * 1.1)


def sheet(out: Path, thalorna: Path):
    WIDTH = 2400
    hand = Encoded("pirzath-hand")
    carved = Encoded("pirzath-carved")
    words = lexicon_words(thalorna, 48)
    carved_r = Renderer(CARVED_FONT)

    order = (list(L.VOWELS) + list(L.LONG) + list(L.DIPHTHONGS) + list(L.CONSONANTS) + list(L.POINTS)
             + ["l.double", "t.double", "ng.double"])
    cell = 290
    cols = (WIDTH - 40) // cell
    rows = -(-len(order) // cols)
    H = 300 + rows * (cell + 60) + 700 + 2 * 200 + 3000
    img = Image.new("RGB", (WIDTH, H), PAPER)
    d = ImageDraw.Draw(img)
    d.text((40, 30), "Pirzath Hand — layer 2: the signs", fill=INK, font=font(46))
    d.text((40, 94), "Every sign built from the layer 1 strokes, at most three movements, every part full-size. "
           "Guides: the line, the vowel height, the digit height and the body; faint, the ascender and the descender.",
           fill=GREY, font=font(22))
    d.text((40, 126), "Printed: each sign stands apart. Under each sign, the roman that writes it and the number of "
           "pen movements.", fill=GREY, font=font(22))

    def guides(x0, x1, oy, sc):
        for v, c in ((0, RULE), (L.V, FAINT), (L.DIGIT, FAINT), (L.B, RULE), (S.ASC, FAINT), (S.DESC, FAINT)):
            d.line([(x0, oy - v * sc), (x1, oy - v * sc)], fill=c)

    # -- every sign large
    y = 190
    sc = 0.24
    for i, name in enumerate(order):
        cx = 20 + (i % cols) * cell
        cy = y + (i // cols) * (cell + 60)
        d.rectangle([cx + 6, cy, cx + cell - 6, cy + cell], outline=RULE)
        tr, adv = L.draw(name)
        oy = cy + cell * 0.74
        ox = cx + cell / 2 - adv * sc / 2
        guides(cx + 8, cx + cell - 8, oy, sc)
        draw_path(img, S.outline(tr), ox, oy, sc)
        sign = L.SIGNS[name]
        d.text((cx + 12, cy + cell + 6), f"{sign.label}   ·  {L.strokes_in(name)}", fill=INK, font=font(22))
        d.text((cx + cell - 12, cy + cell + 10), name, fill=GREY, font=font(15), anchor="ra")
    y += rows * (cell + 60) + 30

    # -- the digits
    d.text((40, y), "The sixteen digits, 0 to 15, a little shorter than the body; a stem with one full stroke, "
           "two for 12 to 15",
           fill=INK, font=font(32))
    y += 60
    sc = 0.26
    oy = y + 260
    x = 60
    guides(40, WIDTH - 40, oy, sc)
    for v in range(16):
        tr, adv = L.draw(f"num.{v}")
        draw_path(img, S.outline(tr), x, oy, sc)
        d.text((x + adv * sc / 2, oy + 70), str(v), fill=GREY, font=font(22), anchor="ma")
        x += adv * sc + 12
    y = oy + 120
    for px in (48, 24):
        scale = px / 1000
        oy = y + px
        x = 60
        names = [f"num.{v}" for v in range(16)]
        tr, wd = L.write(names)
        draw_path(img, S.outline(tr), x, oy, scale)
        d.text((x + wd * scale + 30, oy - px * 0.3), f"{px} px", fill=GREY, font=font(18))
        y = oy + 30
    # 3 and 4 beside 10 to 15, at 48 and 24 px, each labelled
    d.text((60, y), "3 and 4 beside 10 to 15, at 48 and 24 px", fill=INK, font=font(24))
    y += 40
    for px in (48, 24):
        scale = px / 1000
        oy = y + px
        x = 60
        for v in (3, 4, 10, 11, 12, 13, 14, 15):
            tr, adv = L.draw(f"num.{v}")
            draw_path(img, S.outline(tr), x, oy, scale)
            d.text((x + adv * scale / 2, oy + 8), str(v), fill=GREY, font=font(14), anchor="ma")
            x += adv * scale + px * 0.6
        y = oy + 40
    y += 30

    # -- every sign at 24 and 48 px
    d.text((40, y), "Every sign at 48 and 24 px to the em, after Liberation Mono's “xhn” at the same size",
           fill=INK, font=font(32))
    y += 60
    allnames = order + [f"num.{v}" for v in range(16)]
    for px in (48, 24):
        scale = px / 1000
        x = 60
        oy = y + px * 1.2
        d.text((x, oy), "xhn", fill=BLUE, font=latin_font(px), anchor="ls")
        x += px * 2.3
        for name in allnames:
            tr, adv = L.draw(name)
            if x + adv * scale > WIDTH - 40:
                x = 60
                oy += px * 1.9
            draw_path(img, S.outline(tr), x, oy, scale)
            x += adv * scale
        y = oy + px * 1.2 + 30

    # -- words and texts
    d.text((40, y), "Khazari words and texts, written through the pirzath encoding: Liberation Mono, Pirzath Carved and "
           "the hand at one font size", fill=INK, font=font(32))
    y += 60
    px = 40
    scale = px / 1000
    for text in SAMPLES:
        oy = int(y + px * 1.1)
        for v in (S.LATIN_X, L.B):
            d.line([(40, oy - v * scale), (WIDTH - 40, oy - v * scale)], fill=FAINT)
        d.text((60, oy), text, fill=BLUE, font=latin_font(px), anchor="ls")
        tr, wd = L.write(signs_of(hand.one(text)))
        x = max(60 + 760, 60 + d.textlength(text, font=latin_font(px)) + 50)
        if x + wd * scale > WIDTH - 20:
            y += px * 1.8
            oy = int(y + px * 1.1)
            x = 60 + 760
        draw_path(img, S.outline(tr), x, oy, scale)
        cimg, base = carved_image(carved_r, carved.one(text), px)
        cx = int(x + wd * scale + 50)
        if cx + cimg.width > WIDTH - 20:
            y += px * 1.8
            oy = int(y + px * 1.1)
            cx = x
        img.paste(cimg, (int(cx), int(oy - base)))
        y += px * 2.0
    y += 20
    for px in (48, 24):
        scale = px / 1000
        x = 60
        oy = y + px * 1.2
        for w in words:
            tr, wd = L.write(signs_of(hand.one(w)))
            if x + wd * scale > WIDTH - 60:
                x = 60
                oy += px * 2.0
            draw_path(img, S.outline(tr), x, oy, scale)
            x += wd * scale + L.WORD * scale
        d.text((40, oy + px * 0.7), f"{px} px: the first {len(words)} word forms of the Khazari note", fill=GREY,
               font=font(18))
        y = oy + px * 1.4 + 20

    img = img.crop((0, 0, WIDTH, int(y + 30)))
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=ROOT / "specimens/pirzath-hand/letters.png")
    ap.add_argument("--thalorna", type=Path, default=Path.home() / "dev/HeroicLands/thalorna")
    a = ap.parse_args()
    print(sheet(a.out, a.thalorna))


if __name__ == "__main__":
    main()
