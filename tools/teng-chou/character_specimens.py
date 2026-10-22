# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Render the Teng Chou layer 3 sheets from the character data.

    .venv/bin/python tools/teng-chou/character_specimens.py [--only wong,hin] [--out DIR]

``characters.png`` draws every character large, each labelled with its morpheme,
its gloss, its formula and its stroke count. ``syllabary.png`` sets each Jurthati
sign beside the character it is simplified from. Both are drawn from the data
through the layout engine; ``text.png``, set from the built font, is written by
``text_specimen.py``.
"""

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
import characters as C  # noqa: E402
import layout as Y  # noqa: E402
import syllabary as J  # noqa: E402
import specimens as SP  # noqa: E402

PAPER, INK, GREY, RULE, RED = SP.PAPER, SP.INK, SP.GREY, SP.RULE, SP.RED
font = SP.font


OP_NAMES = {"⿰": "lr ", "⿱": "tb ", "⿲": "lmr ", "⿳": "tmb ", "⿴": "in ", "⿵": "open-b ", "⿶": "open-t ",
            "⿷": "open-r ", "⿸": "ul ", "⿹": "ur ", "⿺": "ll ", "⿻": "over "}


def readable(formula: str) -> str:
    """The formula with its operators spelled, for a label font without the IDC glyphs."""
    return "".join(OP_NAMES.get(ch, ch) for ch in formula)


def cell(img, d, path, x, y, size, frame=True):
    if frame:
        d.rectangle([x, y, x + size, y + size], outline=RULE, width=1)
    SP.draw_path(img, path, x, y + size, size / 1000)


def characters_sheet(out: Path, only=None, cols=8, size=250):
    chars = [c for c in C.CHARACTERS if not only or c.morpheme in only]
    pad_x, pad_y = 30, 92
    W = 40 + cols * (size + pad_x)
    rows = -(-len(chars) // cols)
    H = 150 + rows * (size + pad_y)
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.text((40, 30), "Teng Chou — layer 3: the characters", fill=INK, font=font(46))
    d.text((40, 92), f"{len(chars)} characters, one per Tantsou morpheme, each laid out from its formula. "
           "Morpheme, gloss, formula and stroke count under each; a red morpheme carries a hand-tuned override.",
           fill=GREY, font=font(22))
    for i, ch in enumerate(chars):
        x = 40 + (i % cols) * (size + pad_x)
        y = 150 + (i // cols) * (size + pad_y)
        tracks, parts, count = Y.tracks_of(ch.formula, ch.overrides)
        path = Y.render(ch.formula, ch.overrides)
        cell(img, d, path, x, y, size)
        d.text((x, y + size + 6), f"{ch.morpheme} · {count}", fill=RED if ch.overrides else INK, font=font(19))
        d.text((x, y + size + 30), ch.gloss[:34], fill=GREY, font=font(15))
        d.text((x, y + size + 50), readable(ch.formula), fill=GREY, font=font(15))
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)
    return out


def syllabary_sheet(out: Path, only=None, cols=6, size=170):
    signs = [g for g in J.SIGNS if not only or g.syllable in only]
    pair_w = 2 * size + 60
    W = 40 + cols * pair_w
    rows = -(-len(signs) // cols)
    H = 150 + rows * (size + 70) + 260
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.text((40, 30), "Teng Chou — the Jurthati syllabary", fill=INK, font=font(46))
    d.text((40, 92), f"{len(signs)} signs, each beside the character it is simplified from. "
           "Under each: the syllable, the source morpheme and the simplification.", fill=GREY, font=font(22))
    for i, g in enumerate(signs):
        x = 40 + (i % cols) * pair_w
        y = 150 + (i // cols) * (size + 70)
        cell(img, d, J.render(g.syllable), x, y, size)
        ch = C.BY_MORPHEME[g.source]
        cell(img, d, Y.render(ch.formula, ch.overrides), x + size + 8, y, size)
        d.text((x, y + size + 6), g.syllable, fill=RED if g.picks else INK, font=font(24))
        d.text((x + 60, y + size + 10), f"< {g.source} · {g.method}", fill=GREY, font=font(16))
    y = 150 + rows * (size + 70) + 20
    d.text((40, y), "All signs at 48 and 24 px:", fill=GREY, font=font(20))
    for k, px in enumerate((48, 24)):
        for i, g in enumerate(signs):
            SP.draw_path(img, J.render(g.syllable), 40 + i * px * 1.02 % (W - 80),
                         y + 40 + k * 110 + (int(i * px * 1.02 // (W - 80))) * (px + 6) + px, px / 1000)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only")
    ap.add_argument("--out", default=str(ROOT / "specimens" / "teng-chou"))
    ap.add_argument("--cols", type=int, default=8)
    ap.add_argument("--size", type=int, default=250)
    ap.add_argument("--name", default="characters.png")
    a = ap.parse_args()
    only = set(a.only.split(",")) if a.only else None
    out = Path(a.out)
    if a.name.startswith("syllabary"):
        print(syllabary_sheet(out / a.name, only))
    else:
        print(characters_sheet(out / a.name, only, a.cols, a.size))


if __name__ == "__main__":
    main()
