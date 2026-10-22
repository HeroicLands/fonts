# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Render the Veldikko letter sheets from the letters.

    .venv/bin/python tools/veldikko/letter_sheets.py [--out specimens/veldikko] [letters|marks|words|closeup ...]

``letters.png`` sets every letter in its isolated form, labelled
with its sound and family; ``marks.png`` sets every letter under every vowel
mark, long and with each pitch; ``words.png`` sets Sinale and
Áelendi words from the lexicons right to left, the letters touching; and
``closeup.png`` sets runs of marked letters at 24 and 20 px, actual size and
enlarged without smoothing, where the marks are judged first.
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
from specimens import GREY, INK, PAPER, RED, RULE, draw_path, font  # noqa: E402

HANDS = (S.HAND,)
FAMILIES = [
    ("the lips: the bud, standing", ["p", "v", "m"]),
    ("the tongue-tip: arches on a floor, standing", ["t", "s", "n"]),
    ("the tongue-tip, voiced: the arches turned over to hang", ["d", "dh"]),
    ("the back: the coil, hanging", ["k", "h", "ng"]),
    ("the back, voiced: the coil turned over to stand (Áelendan)", ["g"]),
    ("outside the families: stemless", ["l", "r", "_"]),
    ("Áelendan aspirates: the breath, h's coil at the head", ["th", "dhA"]),
    ("Áelendan aspirates, the back", ["kh", "gh"]),
    ("Áelendan ejectives: the catch, the bar across the stem", ["t'", "d'"]),
    ("Áelendan ejectives, the back", ["k'", "g'"]),
]


def label(lt):
    if lt.id == "_":
        return "carrier"
    return {"dhA": "dh"}.get(lt.id, lt.id)


def extent(tracks, style):
    xs = [S.to_page(f, y, style)[0] for t in tracks for f, y, _ in t.samples]
    return min(xs), max(xs)


def put(img, tracks, style, cx, oy, scale):
    """Draw tracks centred on cx, the line at oy."""
    lo, hi = extent(tracks, style)
    ox = cx - (lo + hi) / 2 * scale
    draw_path(img, S.outline(tracks, style), ox, oy, scale)


def put_right(img, tracks, style, x1, oy, scale):
    lo, hi = extent(tracks, style)
    ox = x1 - hi * scale
    draw_path(img, S.outline(tracks, style), ox, oy, scale)
    return ox + lo * scale


def tongues(lt):
    return {("sinale",): "Sinale only", ("aelendi",): "Áelendi only"}.get(lt.tongues, "both tongues")


def letters_sheet(out: Path):
    W, cell, sc = 2400, 270, 0.27
    rows = len(FAMILIES)
    H = 260 + rows * 500
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.text((40, 30), "Veldikko — layer 2: the letters", fill=INK, font=font(46))
    d.text((40, 94), "Every letter in its isolated form, in the one hand both tongues are written in. "
           "Grade by the stem: stop raised, fricative level, nasal lowered into a hook.", fill=GREY, font=font(22))
    d.text((40, 126), "Guides: the line and the bowl height. Labels give the romanized spelling, the sound and who "
           "writes it.", fill=GREY, font=font(22))
    y = 200
    for title, ids in FAMILIES:
        d.text((40, y), title, fill=RED, font=font(26))
        y += 40
        oy = y + S.RISE * sc + 10
        x1 = W - 40
        for lid in ids:
            lt = L.LETTERS[lid]
            pair_w = 2 * cell + 40
            x0 = x1 - pair_w
            for v in (0, S.X):
                d.line([(x0 + 10, oy - v * sc), (x1 - 10, oy - v * sc)], fill=RULE, width=1)
            for k, style in enumerate(HANDS):
                cx = x1 - cell / 2 - k * cell - 10
                put(img, L.glyph(lt, style).tracks, style, cx, oy, sc)
            d.text((x0 + 14, oy + 0.33 * -S.DESC * sc + 70), f"{label(lt)}", fill=INK, font=font(30))
            d.text((x0 + 14, oy + 0.33 * -S.DESC * sc + 112), f"{lt.sound} · {tongues(lt)}", fill=GREY, font=font(18))
            x1 = x0 - 30
        y += 460
    img.save(out)
    return out


MARK_COLS = [("a", "a"), ("o", "o"), ("u", "u"), ("e", "e"), ("i", "i"), ("y", "y"), ("ë", "ë"),
             ("a:", "long a"), ("a/", "a rising"), ("a\\", "a falling"), ("ai", "ai"), ("a!", "a, emphasis")]


def marks_sheet(out: Path):
    ids = [i for _, ids in FAMILIES for i in ids]
    cw, rh, sc = 150, 210, 0.19
    block = len(ids) * rh + 120
    W = len(MARK_COLS) * cw + 260
    H = 160 + 2 * block + 40
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.text((40, 30), "Veldikko — layer 2: every letter under every mark", fill=INK, font=font(40))
    d.text((40, 86), "Columns read from the right: the seven vowels, then a "
           "long, rising, falling, the diphthong ai and emphasis.", fill=GREY, font=font(20))
    x_right = W - 40
    for b, style in enumerate(HANDS):
        y0 = 140 + b * block
        d.text((40, y0), style.name, fill=RED, font=font(30))
        for c, (_, head) in enumerate(MARK_COLS):
            cx = x_right - 140 - c * cw - cw / 2
            d.text((cx - 30, y0 + 50), head, fill=GREY, font=font(18))
        for r, lid in enumerate(ids):
            lt = L.LETTERS[lid]
            oy = y0 + 100 + r * rh + 0.66 * rh
            d.text((x_right - 90, oy - 40), label(lt), fill=INK, font=font(28))
            for c, (m, _) in enumerate(MARK_COLS):
                cx = x_right - 140 - c * cw - cw / 2
                put(img, L.glyph(lt, style, m).tracks, style, cx, oy, sc)
            d.line([(40, oy + 62), (x_right, oy + 62)], fill=RULE)
    img.save(out)
    return out


SINALE_WORDS = [
    ("nuuva", "starlight", "n+u: v+a"),
    ("mollu", "deep pool", "m+o l=+u"),
    ("molu", "the colour of a deep pool", "m+o l+u"),
    ("kalpi", "pale wood", "k+a l p+i"),
    ("halpi", "pale wood, worn", "h+a l p+i"),
    ("eilava", "the wide sky", "_+ei l+a v+a"),
    ("aamas", "the void", "_+a: m+a s"),
    ("rivy", "the turning leaf", "r+i v+y"),
    ("ennedhi", "a tale", "_+e n=+e dh+i"),
    ("lonku", "the deep wood", "l+o ng k+u\\"),
]
AELENDI_WORDS = [
    ("khalthon", "a lodge", "kh+a l th+o n"),
    ("ghoran", "a head", "gh+o r+a n"),
    ("thidharon", "a mark cut in a boundary stone", "th+i dh+a r+o n"),
    ("gulmesa", "a riding", "g+u l m+e s+a"),
]


def words_sheet(out: Path):
    W, sc = 2400, 0.30
    rows = len(SINALE_WORDS) + len(AELENDI_WORDS)
    H = 240 + rows * 420 + 100
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.text((40, 30), "Veldikko — layer 2: words, right to left", fill=INK, font=font(46))
    d.text((40, 94), "Words from the Sinale and Áelendi lexicons, in the one hand both are written in. "
           "Letters touch floor to floor; joining is layer 3.", fill=GREY, font=font(22))
    d.text((40, 126), "Under each word, its Veldikko spelling: letters right to left as read, = a length bar, + the "
           "marks over the letter, : long, \\ falling, _ the carrier.", fill=GREY, font=font(22))
    y = 190
    for tongue, words in (("sinale", SINALE_WORDS), ("aelendi", AELENDI_WORDS)):
        d.text((40, y), "Sinale" if tongue == "sinale" else "Áelendi", fill=RED, font=font(30))
        y += 50
        for rom, gloss, spell in words:
            oy = y + S.RISE * sc + 30
            d.text((40, y + 40), rom, fill=INK, font=font(34))
            d.text((40, y + 88), gloss, fill=GREY, font=font(20))
            d.text((40, y + 118), spell, fill=GREY, font=font(18))
            for k, style in enumerate(HANDS):
                x1 = W - 60 - k * 900
                put_right(img, L.word(spell, style, tongue), style, x1, oy, sc)
            y += 420
    img = img.crop((0, 0, W, y + 30))
    img.save(out)
    return out


CLOSEUP_RUNS = [
    ("the seven vowels", "t+a t+o t+u t+e t+i t+y t+ë"),
    ("over hanging forms", "k+a k+o k+u d+e d+i k+y k+ë"),
    ("long, rising, falling", "s+a: s+a/ s+a\\ s+e: s+i/ s+u\\ s+o:/"),
    ("diphthongs and emphasis", "p+ai p+ei p+oi p+ui m+a! n+e! _+uo"),
    ("words", "n+u: v+a _+ei l+a v+a m+o l=+u"),
]


def render_px(spell, style, px, tongue="sinale"):
    """A run set at ``px`` pixels to the em, on its own small image."""
    tracks = L.word(spell, style, tongue)
    lo, hi = extent(tracks, style)
    sc = px / 1000
    w = int((hi - lo) * sc) + 8
    h = int(px * 1.6) + 6
    img = Image.new("RGB", (w, h), PAPER)
    draw_path(img, S.outline(tracks, style), 4 - lo * sc, int(px * 1.0) + 2, sc)
    return img


def closeup_sheet(out: Path, zoom=8):
    """Runs of marked letters at 24 and 20 px: actual size, and enlarged without smoothing
    so each pixel can be read; then the same runs at display size."""
    W = 2400
    blocks = []
    for px in (24, 20):
        for style in HANDS:
            for name, spell in CLOSEUP_RUNS:
                blocks.append((px, style, name, spell))
    H = 200 + len(blocks) * (int(24 * 1.6 * zoom) + 40) + len(CLOSEUP_RUNS) * 2 * 330 + 200
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.text((40, 30), "Veldikko — layer 2: the marks at text size", fill=INK, font=font(46))
    d.text((40, 94), "Each run read from the right. Left of the label, actual size; right, the same pixels enlarged "
           f"{zoom}x without smoothing. Then each run at display size.", fill=GREY, font=font(22))
    y = 160
    for px, style, name, spell in blocks:
        small = render_px(spell, style, px)
        big = small.resize((small.width * zoom, small.height * zoom), Image.NEAREST)
        img.paste(big, (W - 40 - big.width, y))
        img.paste(small, (40, y + 10))
        d.text((40, y + small.height + 16), f"{px} px · {style.name} · {name}", fill=GREY, font=font(18))
        y += big.height + 40
    y += 20
    for style in HANDS:
        for name, spell in CLOSEUP_RUNS:
            d.text((40, y + 20), f"{style.name} · {name}", fill=GREY, font=font(20))
            put_right(img, L.word(spell, style), style, W - 60, y + 230, 0.22)
            y += 330
    img = img.crop((0, 0, W, y + 20))
    img.save(out)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=ROOT / "specimens/veldikko")
    ap.add_argument("only", nargs="*", help="the sheets to render: letters, marks, words, closeup; all by default")
    out = ap.parse_args().out
    out.mkdir(parents=True, exist_ok=True)
    only = ap.parse_args().only
    sheets = {"letters": letters_sheet, "marks": marks_sheet, "words": words_sheet, "closeup": closeup_sheet}
    for name, make in sheets.items():
        if only and name not in only:
            continue
        f = make(out / f"{name}.png")
        print(f)


if __name__ == "__main__":
    main()
