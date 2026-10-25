# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Render the built Pirzath Hand on real Khazari text.

    .venv/bin/python tools/pirzath-hand/font_sheets.py [--font fonts/PirzathHand-Regular.ttf]
                                                [--encoding FILE]

``specimens/pirzath-hand/text.png``: Khazari words and the Khazari texts of the
carved specimens, written through the ``pirzath`` encoding and shaped by HarfBuzz
from the built font, at display size and at 48, 24 and 20 px, each after its roman
spelling in Monaspace Neon at the same size, with Neon's x-height and cap height
ruled across both. Nothing here draws from the generator: what is shown is the font.
"""

import argparse
import importlib.util
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE.parent))
from encoded import Encoded, EncodedRenderer  # noqa: E402
from render import Renderer  # noqa: E402

PAPER = (243, 239, 228)
INK = (28, 34, 40)
GREY = (118, 112, 100)
BLUE = (40, 90, 170)
FAINT = (222, 212, 192)
X_HEIGHT, CAP_HEIGHT = 0.5135, 0.73
LABEL_FONT = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
LATIN_FONT = Path.home() / "Library/Fonts/MonaspaceNeon-Regular.otf"

WORDS = ["dalk", "dulák", "dullák", "durákh", "tanv", "bant", "gazn", "narv", "zuvák", "dubáz", "thumár",
         "zummád", "galdod", "thufár", "mardh", "putthák", "Ramk-sumád"]


def _carved_texts() -> list[str]:
    spec = importlib.util.spec_from_file_location("pirzath_specimens", ROOT / "tools" / "pirzath" / "specimens.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return [line for _, lines in module.TEXTS for line in lines]


def font(size, path=LABEL_FONT):
    try:
        return ImageFont.truetype(str(path), size)
    except OSError:
        return ImageFont.load_default()


def sheet(out: Path, r: EncodedRenderer) -> Path:
    W = 2400
    img = Image.new("RGB", (W, 9000), PAPER)
    d = ImageDraw.Draw(img)
    d.text((40, 30), "Pirzath Hand — the built font", fill=INK, font=font(46))
    d.text((40, 94), "Khazari words and texts, written by the pirzath encoding and shaped by HarfBuzz from "
           "fonts/PirzathHand-Regular.ttf, after Monaspace Neon at the same size; faint rules: Neon's x-height and "
           "cap height.", fill=GREY, font=font(22))
    texts = _carved_texts()
    y = 170
    size = 96
    x = 60
    for w in WORDS:
        width = r.width(w, size, direction="ltr")
        if x + width > W - 60:
            x, y = 60, y + 200
        r.text(img, x, y + size, w, size, INK, direction="ltr")
        d.text((x, y + size + 50), w, fill=GREY, font=font(20))
        x += width + 80
    y += 250
    for px in (48, 24, 20):
        for t in texts:
            base = y + px * 1.2
            for h in (X_HEIGHT, CAP_HEIGHT):
                d.line([(40, base - h * px), (W - 40, base - h * px)], fill=FAINT)
            latin = font(px, LATIN_FONT)
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
    ap.add_argument("--font", default=str(ROOT / "fonts" / "PirzathHand-Regular.ttf"))
    ap.add_argument("--encoding", help="apply this encoding file instead of encodings/pirzath.json")
    ap.add_argument("--out", default=str(ROOT / "specimens" / "pirzath-hand" / "text.png"))
    a = ap.parse_args()
    print(sheet(Path(a.out), EncodedRenderer(Renderer(Path(a.font)), Encoded("pirzath-hand", a.encoding))))


if __name__ == "__main__":
    main()
