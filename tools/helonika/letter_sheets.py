# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Render the Helónika letter sheet from the letters module.

    .venv/bin/python tools/helonika/letter_sheets.py [--out specimens/helonika/letters.png]

The sheet shows every sign large, the capitals and minuscules in pairs, the
signs at 48 and 24 px beside Semaron Kuriale and Latin with the x-height ruled,
and real Helonic words from thalorna, large with their glosses and run on at
24 and 18 px.
"""

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
import letters as L  # noqa: E402
import strokes as S  # noqa: E402
from specimens import (FAINT, GREY, INK, LATIN_FONT, PAPER, RULE, SEMARON_FONT, draw_path,  # noqa: E402
                       font, guides, semaron)

ROSE = (222, 170, 160)

# Helonic words from the thalorna language note, with their glosses.
WORDS = [
    ("Sothira", "wisdom"), ("kosamir", "world, order"), ("harmodhin", "harmony, balance"),
    ("therin", "contemplation"), ("kléandir", "a hero"), ("kumethos", "the chorus"),
    ("agelon", "the assembly of the citizens"), ("fótamir", "river"), ("zefaris", "air as a principle"),
    ("teikhir", "a wall, the city's"), ("koum", "and"), ("bulos", "a councillor"), ("vesmor", "four"),
    ("Epistémion", "the place of knowledge"), ("dramin", "a play"), ("thásira", "goddess"),
    ("Jumina", "a woman's name"),
]
RUN = ("Sothira koum harmodhin. Kléandir, kumethos, agelon; teikhir koum fótamir. "
       "Bulos vesmor zefaris dramin thásira. Epistémion koum therin.")
SEMARON_RUN = "selan vyra tolde kuria semar"
LATIN_RUN = "the book hand of the copyists"


def cell_grid(img, d, names, y, scale, cell_w, cell_h, oy_frac, full=True, label=True):
    """Each sign in a cell with guides; returns the y below the grid."""
    W = img.width
    cols = (W - 40) // cell_w
    for i, n in enumerate(names):
        cx = 20 + (i % cols) * cell_w
        cy = y + (i // cols) * (cell_h + 46)
        d.rectangle([cx + 6, cy, cx + cell_w - 6, cy + cell_h], outline=RULE)
        oy = cy + cell_h * oy_frac
        guides(d, cx + 8, cx + cell_w - 8, oy, scale, caps=full)
        if n == "accent":  # shown over a grey round
            draw_path(img, L.glyph("o")[0], cx + cell_w / 2 - S.X / 2 * scale, oy, scale, color=(190, 182, 166))
        path, lo, hi = L.glyph(n)
        ox = cx + cell_w / 2 - (lo + hi) / 2 * scale
        draw_path(img, path, ox, oy, scale)
        if label:
            tag = "  echo" if n.upper() in L.ECHOES or n in L.ECHOES else ""
            d.text((cx + 10, cy + cell_h + 4), L.roman(n), fill=INK, font=font(22))
            d.text((cx + 10 + 26 * len(L.roman(n)) + 6, cy + cell_h + 10), f"{n}{tag}", fill=GREY, font=font(14))
    rows = -(-len(names) // cols)
    return y + rows * (cell_h + 46) + 20


def run(img, placed, x, oy, scale):
    for path, dx in placed:
        draw_path(img, path, x + dx * scale, oy, scale)


def wrap(names, max_units):
    """Break a run of sign names at word spaces into lines no wider than ``max_units``."""
    words, cur = [], []
    for n in names + [" "]:
        if n == " ":
            if cur:
                words.append(cur)
            cur = []
        else:
            cur.append(n)
    lines, line = [], []
    for w in words:
        trial = line + ([" "] if line else []) + w
        if line and L.setting(trial)[1] > max_units:
            lines.append(line)
            line = list(w)
        else:
            line = trial
    if line:
        lines.append(line)
    return lines


def sheet(out: Path):
    W = 2400
    H = 9000
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.text((40, 30), "Helónika Book — layer 2: the letters", fill=INK, font=font(46))
    d.text((40, 94), "Every sign, drawn from tools/helonika/letters.py over the accepted strokes: 24 letters and the "
           "additions kh and zh in both cases, the long vowels, the ten digits, the raised dot, the register-mark "
           "and the accent.", fill=GREY, font=font(22))
    d.text((40, 126), "Guides: the line, the body (513), and faintly the ascender (600, rose), the cap height (730) and the "
           "descender (−190). The six echoes of Greek are tagged; every other letter is the script's own.",
           fill=GREY, font=font(22))
    y = 190

    d.text((40, y), "Capitals", fill=INK, font=font(32))
    y = cell_grid(img, d, L.CAPITALS, y + 50, 0.24, 236, 250, 0.84)
    d.text((40, y), "Minuscules", fill=INK, font=font(32))
    y = cell_grid(img, d, L.MINUSCULES, y + 50, 0.24, 236, 250, 0.72)
    d.text((40, y), "Digits, at the cap height", fill=INK, font=font(32))
    y = cell_grid(img, d, L.DIGITS, y + 50, 0.24, 236, 250, 0.84)
    d.text((40, y), "The raised dot, the register-mark, and the accent (over a grey o)", fill=INK, font=font(32))
    y = cell_grid(img, d, L.POINTS, y + 50, 0.24, 236, 250, 0.72)

    # -- pairs
    d.text((40, y), "Capital and minuscule in pairs, 72 px", fill=INK, font=font(32))
    y += 60
    pairs = []
    for c, s in zip(L.CAPITALS, L.MINUSCULES):
        pairs += [c, s, " "]
    sc = 0.072
    for line in wrap(pairs, (W - 120) / sc):
        oy = y + 62
        for v, col in ((0, RULE), (S.X, RULE), (S.CAP, FAINT)):
            d.line([(40, oy - v * sc), (W - 40, oy - v * sc)], fill=col)
        run(img, L.setting(line)[0], 60, oy, sc)
        y += 110
    pairs = []
    for n in L.DIGITS + ["raisedDot", "registerMark"]:
        pairs += [n, " "]
    oy = y + 62
    run(img, L.setting(pairs)[0], 60, oy, sc)
    y += 130

    # -- beside Semaron and Latin
    d.text((40, y), "One x-height: Helónika, then Semaron Kuriale, then Latin (Monaspace Neon), at 48 and 24 px; "
           "rose rules at the line and 0.5135 em", fill=INK, font=font(32))
    y += 60
    hel = L.spell("Sothira koum harmodhin. Kosamir;")
    for px in (48, 24):
        sc = px / 1000
        oy = y + int(px * 0.9) + 8
        for v in (0, S.X):
            d.line([(40, oy - v * sc), (W - 40, oy - v * sc)], fill=ROSE, width=1)
        placed, adv = L.setting(hel)
        x = 60
        run(img, placed, x, oy, sc)
        x += adv * sc + px
        for word in SEMARON_RUN.split():
            d.text((x, oy), semaron(word), fill=INK, font=font(px, SEMARON_FONT), anchor="ls")
            x += d.textlength(semaron(word), font=font(px, SEMARON_FONT)) + S.SPACE * sc
        x += px
        d.text((x, oy), LATIN_RUN, fill=INK, font=font(px, LATIN_FONT), anchor="ls")
        y += int(px * 1.6) + 20
    y += 20

    # -- words
    d.text((40, y), "Helonic words from thalorna, written by the Helonic spelling", fill=INK, font=font(32))
    y += 60
    sc = 0.11
    x = 60
    row_h = 210
    for word, gloss in WORDS:
        placed, adv = L.setting(L.spell(word))
        if x + adv * sc > W - 60:
            x = 60
            y += row_h
        oy = y + 110
        d.line([(x, oy), (x + adv * sc, oy)], fill=RULE)
        run(img, placed, x, oy, sc)
        d.text((x, oy + 34), word, fill=INK, font=font(20))
        d.text((x, oy + 60), gloss, fill=GREY, font=font(16))
        x += max(adv * sc, 200) + 70
    y += row_h + 20

    d.text((40, y), "The same words run on as text at 48, 24 and 18 px", fill=INK, font=font(32))
    y += 50
    d.text((40, y), RUN, fill=GREY, font=font(18))
    y += 40
    names = L.spell(RUN)
    for px in (48, 24, 18):
        sc = px / 1000
        d.text((40, y), f"{px} px", fill=GREY, font=font(16))
        for line in wrap(names, (W - 200) / sc):
            oy = y + px + 4
            run(img, L.setting(line)[0], 120, oy, sc)
            y += px * 1.7
        y += 24

    img = img.crop((0, 0, W, int(y + 30)))
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=ROOT / "specimens/helonika/letters.png")
    print(sheet(ap.parse_args().out))


if __name__ == "__main__":
    main()
