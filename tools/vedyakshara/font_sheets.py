# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Render the built Vedyakshara Classical on real Vedyari words.

    .venv/bin/python tools/vedyakshara/font_sheets.py [--font fonts/VedyaksharaClassical-Regular.ttf]

``specimens/vedyakshara/text.png``: words and sample phrases from the Vedyari note,
their code points stored in ``tools/texts/vedyakshara-classical.json``, shaped by HarfBuzz from the
built font, at display size and at 48, 24 and 20 px, each after its roman spelling
in Liberation Mono at the same size, with the shared x-height ruled across both.
Nothing here draws from the generator: what is shown is the font.
"""

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE.parent))
from codes import Written, WrittenRenderer  # noqa: E402
from render import Renderer, latin_font  # noqa: E402

PAPER = (243, 239, 228)
INK = (28, 34, 40)
GREY = (118, 112, 100)
BLUE = (40, 90, 170)
FAINT = (222, 212, 192)
X_HEIGHT = 0.5135
LABEL_FONT = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"

WORDS = ["vedyara", "dvarna", "suryadvar", "rajepur", "chendra", "karmija", "shroshta", "ikshva", "smiriti",
         "padmavali", "purnakala", "adanshreni", "foshu", "aisu", "ganoka-shalda"]
PHRASES = ["agarana dulipati, vandikana.", "vedyaram tivayu, tarajisum.", "vastuna karmata vanisa?",
           "rituta samarvana ushti.", "bhaktir ushtami dulitara."]


def font(size, path=LABEL_FONT):
    try:
        return ImageFont.truetype(str(path), size)
    except OSError:
        return ImageFont.load_default()


def sheet(out: Path, r: WrittenRenderer) -> Path:
    W = 2400
    img = Image.new("RGB", (W, 3000), PAPER)
    d = ImageDraw.Draw(img)
    d.text((40, 30), "Vedyakshara Classical — the built font", fill=INK, font=font(46))
    d.text((40, 94), "Vedyari words and the sample phrases of the Vedyari note, written in glyph codes "
           "and shaped by HarfBuzz from fonts/VedyaksharaClassical-Regular.ttf.", fill=GREY, font=font(22))
    texts = [" ".join(WORDS[:5]), " ".join(WORDS[5:10]), " ".join(WORDS[10:])] + PHRASES
    y = 170
    size = 96
    x = 60
    for w in WORDS:
        width = r.width(w, size, direction="ltr")
        if x + width > W - 60:
            x, y = 60, y + 210
        r.text(img, x, y + size, w, size, INK, direction="ltr")
        d.text((x, y + size + 70), w, fill=GREY, font=font(20))
        x += width + 80
    y += 260
    for px in (48, 24, 20):
        for t in texts:
            base = y + px * 1.2
            d.line([(40, base - X_HEIGHT * px), (W - 40, base - X_HEIGHT * px)], fill=FAINT)
            latin = latin_font(px)
            d.text((60, base), t, fill=BLUE, font=latin, anchor="ls")
            x = 60 + d.textlength(t, font=latin) + px
            if x + r.width(t, px, direction="ltr") > W - 40:
                y += px * 1.7
                base = y + px * 1.2
                x = 60
            r.text(img, x, base, t, px, INK, direction="ltr")
            y += px * 2.0
        d.text((40, y), f"{px} px", fill=GREY, font=font(18))
        y += 50
    img = img.crop((0, 0, W, int(y + 20)))
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--font", default=str(ROOT / "fonts" / "VedyaksharaClassical-Regular.ttf"))
    ap.add_argument("--out", default=str(ROOT / "specimens" / "vedyakshara" / "text.png"))
    a = ap.parse_args()
    print(sheet(Path(a.out), WrittenRenderer(Renderer(Path(a.font)), Written("vedyakshara-classical"))))


if __name__ == "__main__":
    main()
