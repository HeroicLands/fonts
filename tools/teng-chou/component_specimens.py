# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Render the Teng Chou component sheets from the inventory.

    .venv/bin/python tools/teng-chou/component_specimens.py [--only water,fire] [--out DIR]

``components.png`` shows every component: its standalone form and each positional
form, each in its own box, labelled with id, meaning, role and stroke count.
``components-in-use.png`` sets characters of the core vocabulary, assembled by a
plain ⿰ or ⿱ split, large and as running text.
"""

import argparse
import random
import sys
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
import components as K  # noqa: E402
import specimens as SP  # noqa: E402
import strokes as S  # noqa: E402

PAPER, INK, GREY, RULE, RED = SP.PAPER, SP.INK, SP.GREY, SP.RULE, SP.RED
BLUE = (40, 70, 140)
font = SP.font

ORDER = ("S", "L", "R", "T", "B", "⿸", "⿵", "⿺", "⿴")
LABEL = {"S": "standalone", "L": "left", "R": "right", "T": "top", "B": "bottom",
         "⿸": "frame, upper left", "⿵": "frame, open below", "⿺": "frame, lower left", "⿴": "frame, all round"}


def draw_form(img, d, cid, pos, x, y, scale):
    """Draw one form in its own box with its top left at pixel (x, y); return its width."""
    form = K.COMPONENTS[cid].forms[pos]
    w, h = form.w * scale, form.h * scale
    d.rectangle([x, y, x + w, y + h], outline=RULE, width=1)
    if form.inner:
        a0, b0, a1, b1 = form.inner
        d.rectangle([x + a0 * scale, y + h - b1 * scale, x + a1 * scale, y + h - b0 * scale],
                    outline=(225, 205, 170), width=1)
    path = K.render(cid, pos)
    SP.draw_path(img, path, x, y + h, scale)
    d.text((x, y + h + 4), LABEL[pos], fill=GREY, font=font(15))
    return w


def draw_squeezed(img, d, cid, pos, w, h, x, y, scale):
    """A sound component fitted to a right or bottom box, as a layout would set it."""
    d.rectangle([x, y, x + w * scale, y + h * scale], outline=RULE, width=1)
    path = K.render(cid, "S", (0, 0, w, h))
    SP.draw_path(img, path, x, y + h * scale, scale)
    d.text((x, y + h * scale + 4), "as sound, " + LABEL[pos], fill=GREY, font=font(15))
    return w * scale


def components_sheet(out: Path, only=None):
    ids = [c for c in K.COMPONENTS if not only or c in only]
    W = 2400
    scale = 0.2
    block_w, block_h = 790, 330
    cols = 3
    groups = [("Meaning and structural components", [c for c in ids if K.COMPONENTS[c].role != "sound"]),
              ("Sound components that are whole characters (composed from the components above)",
               [c for c in ids if K.COMPONENTS[c].role == "sound"])]
    rows = sum(-(-len(g) // cols) for _, g in groups if g)
    H = 170 + rows * block_h + 90 * len(groups)
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.text((40, 30), "Teng Chou — layer 2: the components", fill=INK, font=font(46))
    d.text((40, 92), f"{len(ids)} components, each in its own box: the standalone form, then each "
           "positional form. Red ids carry a stroke Chinese lacks. Drawn from tools/teng-chou/inventory.py.",
           fill=GREY, font=font(22))
    y0 = 150
    for title, group in groups:
        if not group:
            continue
        d.text((40, y0), title, fill=INK, font=font(30))
        y0 += 50
        for i, cid in enumerate(group):
            c = K.COMPONENTS[cid]
            bx = 30 + (i % cols) * block_w
            by = y0 + (i // cols) * block_h
            d.line([(bx, by - 8), (bx + block_w - 30, by - 8)], fill=RULE)
            novel = any(S.STROKES[s.sid].novel for f in c.forms.values() for s in f.strokes)
            head = cid + (f"  ‹{c.char}›" if c.char else "")
            d.text((bx, by), head, fill=RED if novel else (BLUE if c.role == "sound" else INK), font=font(24))
            sub = f"{c.meaning} · {c.role} · {c.standalone.count} strokes · complexity {K.complexity(cid)}"
            d.text((bx, by + 30), sub[:90], fill=GREY, font=font(16))
            x = bx
            for pos in ORDER:
                if pos in c.forms:
                    x += draw_form(img, d, cid, pos, x, by + 58, scale) + 16
            if c.role == "sound":
                for pos, (w, h) in (("R", (460, 1000)), ("B", (1000, 440))):
                    x += draw_squeezed(img, d, cid, pos, w, h, x, by + 58, scale) + 16
        y0 += -(-len(group) // cols) * block_h + 30
    img = img.crop((0, 0, W, int(y0 + 20)))
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)
    return out


# -- characters in use -------------------------------------------------------------------------

# characters of the core vocabulary, from the proposal's IDC table: (morpheme, gloss, layout,
# first, second), each part a (component, position) pair. A sound component is named by
# the component that is its character.
IN_USE = [
    ("shou", "water", None, ("water", "S"), None),
    ("wong", "sea", "⿰", ("water", "L"), ("mong", "R")),
    ("zhou", "blue", "⿰", ("water", "L"), ("moon", "R")),
    ("leng", "bright", "⿰", ("sun", "L"), ("moon", "R")),
    ("tan", "celestial", "⿱", ("sky", "T"), ("sun", "B")),
    ("zhen", "snow", "⿱", ("rain", "T"), ("ice", "B")),
    ("hing", "to see", "⿰", ("eye", "L"), ("metal", "R")),
    ("gen", "master", "⿰", ("person", "L"), ("heart", "R")),
    ("hin", "love", "⿱", ("hand", "T"), ("heart", "B")),
    ("tsai", "craft", "⿰", ("hand", "L"), ("wai", "R")),
    ("jen", "nine", "⿰", ("count", "L"), ("zhen", "R")),
    ("na", "mother", "⿰", ("woman", "L"), ("zha", "R")),
    ("ken", "hearth", "⿱", ("door", "T"), ("fire", "B")),
    ("wuo", "warrior", "⿰", ("hand", "S"), ("blade", "R")),
    ("zhao", "house", "⿱", ("roof", "T"), ("rao", "B")),
    ("muen", "flesh", "⿰", ("flesh", "L"), ("roof", "R")),
    ("kin", "lock", "⿰", ("metal", "L"), ("hin", "R")),
    ("sho", "to eat", "⿰", ("food", "L"), ("dragon", "R")),
    ("ya", "to say", "⿰", ("mouth", "L"), ("blade", "S")),
    ("rou", "to go", "⿺", ("motion", "⿺"), ("field", "S")),
    ("weng", "wind", "⿵", ("wind", "⿵"), ("sky", "S")),
    ("chuo", "rank", "⿰", ("step", "L"), ("hand", "R")),
    ("ling", "cup", "⿱", ("sing", "T"), ("vessel", "B")),
    ("wan", "tally", "⿰", ("count", "L"), ("cloud", "R")),
]


LAYOUT_NAME = {None: "alone", "⿰": "left-right", "⿱": "top-bottom", "⿺": "lower-left frame",
               "⿵": "frame open below", "⿸": "upper-left frame", "⿴": "full frame"}


def place(layout, first, second, split):
    """A plain split of the em: ⿰ left/right, ⿱ top/bottom, or an enclosure's inner box."""
    m, top, bot = 70, 930, 70
    if layout is None:
        return [(first[0], first[1], (90, 90, 910, 910))]
    if layout == "⿰":
        xm = m + (1000 - 2 * m) * split
        return [(first[0], first[1], (m, bot, xm - 10, top)), (second[0], second[1], (xm + 10, bot, 1000 - m, top))]
    if layout == "⿱":
        ym = bot + (top - bot) * (1 - split)
        return [(first[0], first[1], (m, ym + 10, 1000 - m, top)), (second[0], second[1], (m, bot, 1000 - m, ym - 10))]
    form, _ = K.form_of(*first)
    a0, b0, a1, b1 = form.inner
    return [(first[0], first[1], (m, bot, 1000 - m, top)),
            (second[0], second[1], (m + a0 * 0.86, bot + b0 * 0.86, m + a1 * 0.86, bot + b1 * 0.86))]


def assemble(layout, first, second):
    if layout is None:
        n = K.stroke_count(*first)
        return K.render_parts(place(None, first, None, 0), K.weight_for(n)), n
    w1 = K.complexity(*first) if first[1] in K.COMPONENTS[first[0]].forms else K.complexity(first[0])
    w2 = K.complexity(second[0], second[1])
    if layout == "⿰":
        split = min(0.46, max(0.32, 0.30 + 0.25 * w1 / (w1 + w2)))
    else:
        split = min(0.52, max(0.30, 0.22 + 0.5 * w1 / (w1 + w2)))
    n = K.stroke_count(*first) + K.stroke_count(*second)
    return K.render_parts(place(layout, first, second, split), K.weight_for(n)), n


def in_use_sheet(out: Path):
    W = 2400
    big = 330
    cols = 6
    rows = -(-len(IN_USE) // cols)
    H = 170 + rows * (big + 110) + 900
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.text((40, 30), "Teng Chou — layer 2: components in use", fill=INK, font=font(46))
    d.text((40, 92), "Characters of the core vocabulary, assembled by a plain left-right or top-bottom split of the em "
           "(the layout engine is layer 3). Morpheme, gloss and stroke count under each.", fill=GREY, font=font(22))
    y = 150
    shapes = []
    for i, (morph, gloss, layout, a, b) in enumerate(IN_USE):
        x = 40 + (i % cols) * (big + 64)
        yy = y + (i // cols) * (big + 110)
        SP.em_box(d, x, yy, big)
        path, n = assemble(layout, a, b)
        shapes.append(path)
        SP.draw_path(img, path, x, yy + big, big / 1000)
        d.text((x, yy + big + 8), f"{morph} · {gloss} · {n}", fill=GREY, font=font(20))
        d.text((x, yy + big + 34), f"{LAYOUT_NAME[layout]}: {a[0]}{' + ' + b[0] if b else ''}", fill=GREY, font=font(16))
    y += rows * (big + 110) + 20
    order = random.Random(12)
    for px, lines in ((64, 2), (32, 3), (20, 4), (14, 4)):
        d.text((40, y + px * 0.3), f"{px} px", fill=GREY, font=font(18))
        for _ in range(lines):
            x = 130
            while x + px < W - 40:
                SP.draw_path(img, order.choice(shapes), x, y + px, px / 1000)
                x += px * 1.06
            y += px * 1.55
        y += 24
    img = img.crop((0, 0, W, int(y + 30)))
    img.save(out)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=ROOT / "specimens/teng-chou")
    ap.add_argument("--only", default="")
    ap.add_argument("--no-in-use", action="store_true")
    args = ap.parse_args()
    only = set(filter(None, args.only.split(",")))
    print(components_sheet(args.out / "components.png", only or None))
    if not args.no_in_use:
        print(in_use_sheet(args.out / "components-in-use.png"))


if __name__ == "__main__":
    main()
