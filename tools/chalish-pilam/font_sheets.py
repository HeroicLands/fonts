# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Render the Ch'alish P'ilam common hand's passage through the built font.

    .venv/bin/python tools/chalish-pilam/font_sheets.py [--out specimens/chalish-pilam/text.png]

The passage, a night's entry at the sighting stones, is written as code points from
``encoding.json``, shaped by HarfBuzz through ``fonts/ChalishPilamCommon-Regular.ttf``
and drawn from the font's own outlines. A page is set as a browser sets it: the text
runs in a column two advances wide and wraps by line breaking alone, so the rows of two
come from the advance, not from the sheet. The sheet shows the page at display size
with each glyph's concept beside it, the page at reading sizes, and a run of the
script inside a line of Latin. Shaping fails the run if any glyph comes back as the
box or ``.notdef``.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
import glyphs as K  # noqa: E402
from build_ufo import glyph_name  # noqa: E402
from strokes_sheet import BLUE, GREY, INK, RED, Sheet  # noqa: E402

FONT = ROOT / "fonts" / "ChalishPilamCommon-Regular.ttf"


class Face:
    def __init__(self, path):
        self.tt = TTFont(str(path))
        self.gs = self.tt.getGlyphSet()
        self.order = self.tt.getGlyphOrder()
        blob = hb.Blob.from_file_path(str(path))
        self.hb = hb.Font(hb.Face(blob))
        self.upem = self.tt["head"].unitsPerEm
        self.paths = {}

    def shape(self, text):
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(self.hb, buf, {})
        out = []
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            name = self.order[info.codepoint]
            if name in (".notdef", "notdef.box"):
                raise SystemExit(f"{FONT.relative_to(ROOT)}: error: U+{ord(text[info.cluster]):05X} shapes to {name}")
            out.append((name, pos.x_advance))
        return out

    def path(self, name):
        if name not in self.paths:
            pen = SVGPathPen(self.gs)
            self.gs[name].draw(pen)
            self.paths[name] = pen.getCommands()
        return self.paths[name]


def codepoints():
    return {r["glyph"]: chr(int(r["codepoint"][2:], 16))
            for r in json.loads((HERE / "encoding.json").read_text())["glyphs"]}


def set_column(sh, face, shaped, x, top, px, rows, colgap, labels=None):
    """Set shaped glyphs as a browser sets them in columns two advances wide: each line
    holds what fits in two advances, ``rows`` lines to a column. Return the bottom."""
    sc = px / face.upem
    width = 2 * face.tt["hmtx"]["space"][0]
    line_h = px * (1.5 if labels else 1.1)
    col_w = width * sc + colgap
    lines, cur, used = [], [], 0
    for name, adv in shaped:
        if used + adv > width and cur:
            lines.append(cur)
            cur, used = [], 0
        cur.append((name, adv))
        used += adv
    if cur:
        lines.append(cur)
    bottom = top
    for i, line in enumerate(lines):
        col, row = divmod(i, rows)
        base = top + (row + 1) * line_h
        xx = x + col * col_w
        for name, adv in line:
            sh.out.append(f'<path d="{face.path(name)}" fill="{INK}" '
                          f'transform="matrix({sc} 0 0 {-sc} {xx:.2f} {base:.2f})"/>')
            if labels:
                sh.text(xx + adv * sc / 2, base + 14, labels.pop(0), 10, GREY, anchor="middle")
            xx += adv * sc
        bottom = max(bottom, base)
    return bottom


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "specimens/chalish-pilam/text.png"))
    args = ap.parse_args()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    face = Face(FONT)
    cps = codepoints()
    glyphs = K.passage_glyphs()
    text = "".join(cps[glyph_name(g)] for g in glyphs)
    shaped = face.shape(text)

    W = 2400
    sh = Sheet(W)
    sh.y = 50
    sh.text(40, sh.y, "Ch'alish P'ilam, the common hand — layer 3: the font", 36)
    sh.y += 34
    for line in [
        "A night's entry at the sighting stones, as the Faith of Ish'ilan Ch'alish keeps one every night whether or not "
        "anything happens. A record of meaning, not of words.",
        f"Shaped by HarfBuzz through {FONT.relative_to(ROOT)} and drawn from its outlines. Each column is two advances "
        "wide and wraps by line breaking alone; nothing in the sheet places the rows.",
    ]:
        sh.text(40, sh.y, line, 15, GREY)
        sh.y += 21
    sh.y += 10

    sh.heading("The entry at display size, each glyph's concept under it; read two to a row, down each column")
    labels = []
    for gloss, gs in K.PASSAGE:
        for g in gs:
            labels.append(g.meaning.split(";")[0].removeprefix("a ").removeprefix("the "))
    bottom = set_column(sh, face, shaped, 40, sh.y, 110, rows=7, colgap=70, labels=labels)
    sh.y = bottom + 50
    sh.text(40, sh.y, "The meaning, phrase by phrase:", 15, INK, weight="bold")
    sh.y += 22
    for gloss, gs in K.PASSAGE:
        sh.text(60, sh.y, f"{gloss}", 14, GREY)
        sh.text(460, sh.y, " · ".join(g.name for g in gs), 13, RED)
        sh.y += 19
    sh.y += 10

    sh.heading("The page at 32, 24 and 16 px to the em")
    for px in (32, 24, 16):
        sh.text(40, sh.y + 16, f"{px} px", 13, GREY)
        sh.y = set_column(sh, face, shaped, 120, sh.y, px, rows=10, colgap=px * 1.4) + 30

    sh.heading("Inline: a run of the script inside a line of Latin, both at 32 px")
    px = 32
    base = sh.y + px
    x = 40 + sh.latin(40, base, "The scribe wrote ", px, BLUE)
    sc = px / face.upem
    for name, adv in face.shape("".join(cps[glyph_name(g)] for g in (K.ZERO,))):
        sh.out.append(f'<path d="{face.path(name)}" fill="{INK}" transform="matrix({sc} 0 0 {-sc} {x:.2f} {base:.2f})"/>')
        x += adv * sc
    x += sh.latin(x, base, " — nothing happened — and the night went on.", px, BLUE)
    sh.y = base + 40

    height = int(sh.y + 30)
    svg_file = out.with_suffix(".svg")
    svg_file.write_text(sh.svg(height))
    subprocess.run(["rsvg-convert", "-o", str(out), str(svg_file)], check=True)
    print(out)


if __name__ == "__main__":
    main()
