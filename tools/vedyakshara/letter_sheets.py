# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Render the Vedyakshara letter sheet from the sign module.

    .venv/bin/python tools/vedyakshara/letter_sheets.py [--out specimens/vedyakshara/letters.png]

The sheet has five parts: every consonant and fused sign large in its four forms
(full, half, final, r-foot); the independent vowels, the vowel signs on a few
signs, _fa_ with the soft dot, the digits and the bars; the signs run on at 48
and 24 px after Liberation Mono; real Vedyari words and the sample phrases at
display size; and the same words at 48, 24 and 20 px after their roman spelling.
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
from specimens import BLUE, FAINT, GREY, INK, PAPER, RED, RULE, draw_path, font  # noqa: E402
from render import latin_font  # noqa: E402

WORDS = ["Vedyara", "dvarna", "Suryadvar", "Rajepur", "chendra", "karmija", "shroshta", "ikshva", "smiriti",
         "Padmavali", "purnakala", "Adanshreni", "foshu", "aisu", "Ganoka-shalda"]
PHRASES = ["Agarana dulipati, vandikana", "Vastuna karmata vanisa", "Rituta samarvana ushti",
           "Bhaktir ushtami dulitara"]


def bounds(tracks):
    xs = [f for t in tracks for f, _, _ in t.samples]
    return min(xs), max(xs)


def guides(d, x0, x1, oy, sc):
    for v, c in ((0, RULE), (S.X, RULE), (S.HEAD, FAINT), (S.FLAG, FAINT), (S.HOOK, FAINT)):
        d.line([(x0, oy - v * sc), (x1, oy - v * sc)], fill=c)


def put(img, tracks, x, oy, sc):
    draw_path(img, S.outline(tracks), x, oy, sc)


def phrase(text):
    """A phrase set word by word, a word space between, the pause bar for a comma."""
    out, x = [], 0.0
    for raw in text.split():
        comma = raw.endswith(",")
        run = L.write(raw.strip(",?").lower())
        out += [S.Shape([t], (0, 0, 0), (0, 0, 0)).moved(x, 0).tracks[0] for t in run.tracks]
        x += run.width
        if comma:
            b = L.point(1)
            out += [S.Shape([t], (0, 0, 0), (0, 0, 0)).moved(x + 40, 0).tracks[0] for t in b.tracks]
            x += b.adv + 40
        x += 260
    return out, x - 260


def sheet(out: Path):
    W = 2400
    img = Image.new("RGB", (W, 16000), PAPER)
    d = ImageDraw.Draw(img)
    d.text((40, 30), "Vedyakshara Classical — layer 2: the signs", fill=INK, font=font(46))
    d.text((40, 94), "Drawn from tools/vedyakshara/letters.py on the reed strokes of strokes.py. Each sign: full · half · "
           "final · r-foot. Guides: the line, the x-height, and faint, the headline top, the flag head, the hook foot.",
           fill=GREY, font=font(22))
    d.text((40, 126), "Twenty-two consonants and nineteen fused clusters, seven independent vowels (29 + 19 = 48), fa with "
           "the soft dot, the vowel signs, the reed digits and the bars.", fill=GREY, font=font(22))
    y = 190

    # -- part 1: every consonant and fused sign in its four forms
    sc = 0.2
    names = list(L.CONSONANTS) + ["fa"] + L.FUSED
    col_w = W // 2
    row_h = 250
    for i, n in enumerate(names):
        cx = 30 + (i % 2) * col_w
        cy = y + (i // 2) * row_h
        oy = cy + 170
        d.text((cx, cy + 20), n, fill=INK, font=font(30))
        d.text((cx, cy + 58), "fused" if n in L.FUSED else ("soft dot" if n == "fa" else "consonant"), fill=GREY,
               font=font(16))
        x = cx + 140
        guides(d, x - 10, cx + col_w - 30, oy, sc)
        for form in ("full", "half", "final", "rfoot"):
            if form == "rfoot" and n in L.FUSED and n.endswith("ra"):
                continue  # the r is in the sign already
            g = L.sign(n, form=form)
            put(img, g.tracks, x, oy, sc)
            x += max(g.adv, 420) * sc + 50
    y += -(-len(names) // 2) * row_h + 40

    # -- part 2: vowels, vowel signs, digits, bars
    def row(title, glyphs, labels, sc=0.2, step=None):
        nonlocal y
        d.text((40, y), title, fill=INK, font=font(30))
        y += 50
        oy = y + 180
        x = 60
        guides(d, 40, W - 40, oy, sc)
        for g, lab in zip(glyphs, labels):
            put(img, g.tracks, x, oy, sc)
            d.text((x, oy + 70), lab, fill=GREY, font=font(18))
            x += (step or g.adv * sc + 60)
        y += 300

    row("Independent vowels", [L.sign(v) for v in L.INDEPENDENT], list(L.INDEPENDENT))
    vs = [None] + list(L.VOWEL_SIGNS)
    row("ka with each vowel sign: ka ki ke kai ku ko kau", [L.sign("ka", vowel=v) for v in vs],
        ["k" + (v or "a") for v in vs])
    row("The vowel signs on other signs", [L.sign(n, vowel=v) for n, v in
                                          (("ra", "i"), ("ra", "u"), ("ja", "e"), ("ma", "o"), ("nda", "i"),
                                           ("tra", "u"), ("ksha", "au"), ("va", "o"), ("sha", "ai"), ("da", "u"))],
        ["ri", "ru", "je", "mo", "ndi", "tru", "kshau", "vo", "shai", "du"])
    row("The reed digits 0–9, and the bars: plain, the pause, the end of a sentence",
        [L.digit(c) for c in L.DIGITS] + [L.point(k) for k in (0, 1, 2)], list(L.DIGITS) + ["bar", "pause", "end"])

    # -- part 3: the signs at text size after Liberation Mono
    d.text((40, y), "The signs at 48 and 24 px, after Liberation Mono at the same size; faint rule: the shared x-height",
           fill=INK, font=font(30))
    y += 60
    lines = [("base", [L.sign(n) for n in list(L.CONSONANTS) + list(L.INDEPENDENT)]),
             ("fused", [L.sign(n) for n in L.FUSED + ["fa"]] + [L.digit(c) for c in L.DIGITS])]
    for px in (48, 24):
        s = px / 1000
        for _, gl in lines:
            oy = y + px * 1.2
            d.line([(40, oy - S.X * s), (W - 40, oy - S.X * s)], fill=FAINT)
            d.text((60, oy), "xhn", fill=BLUE, font=latin_font(px), anchor="ls")
            x = 60 + px * 2.4
            for g in gl:
                if x + g.adv * s > W - 40:
                    break
                put(img, g.tracks, x, oy, s)
                x += g.adv * s + px * 0.25
            y += px * 1.9
        y += 20

    # -- part 4: words and phrases at display size
    y += 30
    d.text((40, y), "Vedyari words from the note, compounds solid; and the sample phrases", fill=INK, font=font(30))
    y += 50
    sc = 0.12
    x = 60
    for wd in WORDS:
        run = L.write(wd)
        if x + run.width * sc > W - 40:
            x = 60
            y += 200
        oy = y + 120
        put(img, run.tracks, x, oy, sc)
        d.text((x, oy + 40), wd, fill=GREY, font=font(18))
        x += run.width * sc + 70
    y += 220
    for p in PHRASES:
        tr, wd = phrase(p)
        oy = y + 120
        put(img, tr, 60, oy, sc)
        d.text((60, oy + 40), p, fill=GREY, font=font(18))
        y += 200

    # -- part 5: words at text size
    d.text((40, y), "The same at 48, 24 and 20 px, after the roman spelling in Liberation Mono", fill=INK, font=font(30))
    y += 60
    texts = [" ".join(WORDS[:5]), " ".join(WORDS[5:10]), " ".join(WORDS[10:]), PHRASES[0], PHRASES[1]]
    for px in (48, 24, 20):
        s = px / 1000
        for t in texts:
            oy = y + px * 1.2
            d.line([(40, oy - S.X * s), (W - 40, oy - S.X * s)], fill=FAINT)
            d.text((60, oy), t, fill=BLUE, font=latin_font(px), anchor="ls")
            x = 60 + d.textlength(t, font=latin_font(px)) + px
            tr, wd = phrase(t)
            if x + wd * s > W - 40:
                y += px * 1.6
                oy = y + px * 1.2
                x = 60
            put(img, tr, x, oy, s)
            y += px * 1.9
        d.text((40, y), f"{px} px", fill=GREY, font=font(18))
        y += 40
    d.text((40, y + 10), "The signs are drawn, not shaped: the specimen splits the roman spelling itself. Layer 3 builds "
           "the font and its rules.", fill=RED, font=font(20))
    img = img.crop((0, 0, W, int(y + 60)))
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=ROOT / "specimens/vedyakshara/letters.png")
    print(sheet(ap.parse_args().out))


if __name__ == "__main__":
    main()
