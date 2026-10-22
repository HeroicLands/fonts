# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Render the candidates for the letter _l_ side by side.

    .venv/bin/python tools/veldikko/l_options.py [--out specimens/veldikko/l-options.png]

Three stemless forms in the hand's curved vocabulary: the riser, which the letters
use, and two shorter forms weighed against it. Each is shown large
beside the letters it must not be taken for, then in words at display size and at
24 px.
"""

import argparse
import dataclasses
import sys
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
import letter_sheets as LS  # noqa: E402
import letters as L  # noqa: E402
import strokes as S  # noqa: E402
from specimens import GREY, INK, PAPER, RED, RULE, draw_path, font  # noqa: E402


def s_loop(f, y, fl=1.0, w=170, h=250):
    """A looped _l_ at the bowls' height: from the line the pen climbs forward, rounds
    over the top, comes back down across its own climb, and its foot turns forward
    into a tendril."""
    t = S.Track(f - 10, y + 0.12 * h, -0.4)
    t.curve((f + 0.25 * w, y + 0.30 * h), (f + 0.70 * w, y + 0.70 * h), f + 0.55 * w, y + 0.96 * h, 0.30)
    t.curve((f + 0.42 * w, y + 1.10 * h), (f + 0.10 * w, y + 0.98 * h), f + 0.16 * w, y + 0.70 * h, 0.45)
    t.curve((f + 0.22 * w, y + 0.36 * h), (f + 0.20 * w, y + 0.04 * h), f + 0.52 * w, y + 0.02 * h, 0.90)
    t.curve((f + 0.90 * w, y), (f + 1.10 * w, y + 0.20 * h), f + 0.98 * w, y + 0.36 * h, 0.35)
    t.spiral(f + 0.88 * w, y + 0.26 * h, 240 * (0.5 + 0.5 * fl), 0.5, 0.25)
    S._lift(t, 0.18)
    return S.Shape([t], (f - 10, y + 0.12 * h, 40), (f + w, y, 0))


def s_sprout(f, y, fl=1.0, w=180, h=250):
    """A seed on the line with a tendril sprouting from it: the pen rounds a small seed
    on the line and climbs out of its top into a tendril curled forward."""
    t = S.Track(f + 0.30 * w, y + 0.34 * h, -0.4)
    t.curve((f + 0.05 * w, y + 0.30 * h), (f + 0.02 * w, y), f + 0.36 * w, y, 0.90)
    t.curve((f + 0.70 * w, y), (f + 0.74 * w, y + 0.34 * h), f + 0.46 * w, y + 0.40 * h, 0.40)
    t.curve((f + 0.30 * w, y + 0.56 * h), (f + 0.40 * w, y + 0.90 * h), f + 0.70 * w, y + 0.98 * h, 0.30)
    t.spiral(f + 0.74 * w, y + 0.80 * h, -260 * (0.5 + 0.5 * fl), 0.45, 0.25)
    S._lift(t, 0.18)
    return S.Shape([t], (f + 0.30 * w, y + 0.34 * h, 180), (f + w, y, 0))


CANDIDATES = [
    ("A · the riser (chosen)", "riser"),
    ("B · the loop", "l-loop"),
    ("C · the sprout", "l-sprout"),
]
S.STROKES["l-loop"] = S.StrokeType("l-loop", "Loop", "letter", s_loop, {}, "", "", "", "")
S.STROKES["l-sprout"] = S.StrokeType("l-sprout", "Sprout", "letter", s_sprout, {}, "", "", "", "")
L.WIDTH.update({"l-loop": 170, "l-sprout": 180})
L.ANCHOR.update({"l-loop": 0.45, "l-sprout": 0.45})

WORDS = [("mollu", "m+o l=+u", "sinale"), ("kalpi", "k+a l p+i", "sinale"), ("eilava", "_+ei l+a v+a", "sinale"),
         ("khalthon", "kh+a l th+o n", "aelendi")]
NEIGHBOURS = ["r", "_", "k", "t"]


def with_l(form):
    original = L.LETTERS["l"]
    L.LETTERS["l"] = dataclasses.replace(original, form=form)
    return original


def sheet(out: Path):
    W = 2400
    H = 200 + len(CANDIDATES) * 1500
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.text((40, 30), "Veldikko — candidates for l", fill=INK, font=font(46))
    d.text((40, 94), "Each candidate large beside r, the carrier, k and t; then in words at display size "
           "and at 24 px (actual size, and enlarged 6x). Read from the right.", fill=GREY, font=font(22))
    y = 160
    for title, form in CANDIDATES:
        original = with_l(form)
        try:
            d.text((40, y), title, fill=RED, font=font(32))
            y += 50
            oy = y + 0.9 * S.RISE * 0.32 + 20
            x1 = W - 40
            for style in LS.HANDS:
                for lid in ["l"] + NEIGHBOURS:
                    tracks = L.glyph(lid, style, "a").tracks
                    left = LS.put_right(img, tracks, style, x1, oy, 0.32)
                    d.text(((left + x1) / 2 - 10, oy + 110), LS.label(L.LETTERS[lid]), fill=GREY, font=font(20))
                    x1 = left - 60
                x1 -= 120
            d.line([(40, oy), (W - 40, oy)], fill=RULE)
            y = int(oy + 160)
            for k, (rom, spell, tongue) in enumerate(WORDS):
                x1 = W - 60 - k * 560
                style = S.HAND if tongue == "sinale" else S.HAND
                LS.put_right(img, L.word(spell, style, tongue), style, x1, y + 300, 0.22)
                d.text((x1 - 300, y + 380), rom, fill=GREY, font=font(20))
            y += 430
            for k, (rom, spell, tongue) in enumerate(WORDS):
                style = S.HAND if tongue == "sinale" else S.HAND
                small = LS.render_px(spell, style, 24, tongue)
                big = small.resize((small.width * 6, small.height * 6), Image.NEAREST)
                x1 = W - 60 - k * 560
                img.paste(big, (x1 - big.width, y))
                img.paste(small, (x1 - big.width - small.width - 20, y + 60))
            y += 300
        finally:
            L.LETTERS["l"] = original
    img = img.crop((0, 0, W, y + 20))
    img.save(out)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=ROOT / "specimens/veldikko/l-options.png")
    print(sheet(ap.parse_args().out))


if __name__ == "__main__":
    main()
