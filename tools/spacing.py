# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Confirm that every face sets its text at a natural spacing.

    .venv/bin/python tools/spacing.py [--report] [font ...]

Two measures are taken from each built font:

- **The blank share** of a glyph is its advance less its ink width, over its
  advance. The median is taken over the glyphs the character map reaches, leaving
  out the notdef, the box, the space and every glyph with no advance or no ink.
- **Run-text tightness** is read from the font's sample lines, shaped with
  HarfBuzz in the font's direction and features. Within a word, the gap between
  two neighbouring signs is the distance, in ems, from the right edge of one
  sign's ink to the left edge of the next sign's ink. A mark with no advance is
  not a neighbour. A space, any glyph on U+0020, the box and the notdef end a
  word: a letter the script does not write takes the box. The mean and the
  largest gap are reported, with the bare-ground share of the words: the part
  of each word's extent, from its first ink to its last, that no ink covers.

A font fails when its median blank share is above ``MAX_BLANK``, its mean gap
above ``MAX_MEAN_GAP`` or its largest gap above ``MAX_GAP``, or when its space is
not the word space ``SPACING`` in tools/respace.py states for the face. A joined face
(Pirzath Hand with ``ss01``) overlaps its signs, so its gaps are negative and
pass.

The sample lines are the texts of each face's specimens: the Khazari texts for
the Pirzath faces, the Nordmal lines for Thuravark Carved and the Vylari texts for
Semaron Kuriale; Qalezu Hand's converter fixtures, written in the glyphs the
fixtures name; the sample inscriptions of Khelathi Zethu Glyphs, set as one
strip of signs; and Teng Chou's Tantsou and Jurthati passages, each line one run
of characters. None needs a thalorna checkout.
"""

import importlib.util
import json
import statistics
import sys
from pathlib import Path

import uharfbuzz as hb
from fontTools.pens.boundsPen import BoundsPen
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))
import respace  # noqa: E402

MAX_BLANK = 0.14
MAX_MEAN_GAP = 0.08
MAX_GAP = 0.22

SKIP = {".notdef", "notdef.box"}


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _pirzath_lines() -> list[str]:
    texts = _load("pirzath_specimens", TOOLS / "pirzath" / "specimens.py").TEXTS
    return [line for _, lines in texts for line in lines]


def _thuravark_lines() -> list[str]:
    return [line for _, line in _load("thuravark_specimens", TOOLS / "thuravark-carved" / "specimens.py").LINES]


def _semaron_lines() -> list[str]:
    return [line for _, line in _load("semaron_specimens", TOOLS / "semaron-kuriale" / "specimens.py").TEXTS]


def _qalezu_lines() -> list[str]:
    enc = json.loads((TOOLS / "qalezu-hand" / "encoding.json").read_text(encoding="utf-8"))
    by_glyph = {}

    def walk(node):
        if isinstance(node, dict):
            if "glyph" in node and "codepoint" in node:
                by_glyph[node["glyph"]] = chr(int(node["codepoint"][2:], 16))
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)

    walk(enc)
    fixtures = json.loads((TOOLS / "qalezu-hand" / "fixtures.json").read_text(encoding="utf-8"))["fixtures"]
    words = ["".join(by_glyph[g] for g in f["signs"]) for f in fixtures if f["signs"] and all(g in by_glyph for g in f["signs"])]
    return [" ".join(words[i:i + 8]) for i in range(0, len(words), 8)]


def _zethu_lines() -> list[str]:
    guard = _load("zethu_guard", TOOLS / "khelathi-zethu-glyphs" / "guard.py")
    enc = json.loads((TOOLS / "khelathi-zethu-glyphs" / "encoding.json").read_text(encoding="utf-8"))
    cp = {e["id"]: chr(int(e["codepoint"][2:], 16)) for e in enc["signs"] if e.get("drawn")}
    return ["".join(cp[i] for i in ids if i in cp) for _, ids in guard.sample_lists()]


def _teng_chou_lines() -> list[str]:
    return _load("teng_chou_texts", TOOLS / "teng-chou" / "texts.py").lines()


# Each face: its sample lines, its direction and the features its class turns on.
FACES = {
    "PirzathCarved": (_pirzath_lines, "ltr", {}),
    "PirzathHand": (_pirzath_lines, "ltr", {"ss01": True}),
    "ThuravarkCarved": (_thuravark_lines, "ltr", {}),
    "SemaronKuriale": (_semaron_lines, "ltr", {}),
    "QalezuHand": (_qalezu_lines, "rtl", {}),
    "KhelathiZethuGlyphs": (_zethu_lines, "rtl", {}),
    "TengChou": (_teng_chou_lines, "ltr", {}),
}


class Face:
    def __init__(self, path: Path):
        self.path = path
        self.tt = TTFont(str(path))
        self.upem = self.tt["head"].unitsPerEm
        self.order = self.tt.getGlyphOrder()
        self.glyphs = self.tt.getGlyphSet()
        self.hmtx = self.tt["hmtx"].metrics
        self.cmap = self.tt.getBestCmap()
        self.space = self.cmap.get(0x20)
        self.hb = hb.Font(hb.Face(path.read_bytes()))
        self._ink = {}

    def ink(self, name: str):
        """The glyph's ink as (left, right) in font units, or None."""
        if name not in self._ink:
            pen = BoundsPen(self.glyphs)
            self.glyphs[name].draw(pen)
            self._ink[name] = (pen.bounds[0], pen.bounds[2]) if pen.bounds else None
        return self._ink[name]

    def gap(self, a, b) -> float:
        """The distance, in font units, from the ink of one placed sign to the next, each (x, glyph)."""
        (xa, ga), (xb, gb) = a, b
        return xb + self.ink(gb)[0] - (xa + self.ink(ga)[1])

    def blank_shares(self) -> list[float]:
        shares = []
        for name in sorted(set(self.cmap.values())):
            adv = self.hmtx[name][0]
            ink = self.ink(name)
            if name in SKIP or name == self.space or adv <= 0 or ink is None:
                continue
            shares.append((adv - (ink[1] - ink[0])) / adv)
        return shares

    def words(self, text: str, direction: str, features: dict) -> list[list[tuple[float, str]]]:
        """Each word of the shaped text as its signs, (x, glyph), left to right in font units."""
        buf = hb.Buffer()
        buf.add_str(text)
        buf.direction = direction
        buf.script = "Zyyy"
        buf.guess_segment_properties()
        hb.shape(self.hb, buf, features)
        words, current, pen_x = [], [], 0
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            name = self.order[info.codepoint]
            ink = self.ink(name)
            if name == self.space or name in SKIP or text[info.cluster] == " ":
                if current:
                    words.append(current)
                current = []
            elif pos.x_advance > 0 and ink is not None:
                current.append((pen_x + pos.x_offset, name))
            pen_x += pos.x_advance
        if current:
            words.append(current)
        return words


def measure(path: Path) -> dict:
    face = Face(path)
    lines, direction, features = FACES[path.name.split("-")[0]]
    gaps, extent, bare = [], 0.0, 0.0
    for text in lines():
        for word in face.words(text, direction, features):
            gaps += [face.gap(a, b) / face.upem for a, b in zip(word, word[1:])]
            spans = [(x + face.ink(g)[0], x + face.ink(g)[1]) for x, g in word]
            left, right = min(i[0] for i in spans), max(i[1] for i in spans)
            covered, reach = 0.0, left
            for lo, hi in sorted(spans):
                if hi > reach:
                    covered += hi - max(lo, reach)
                    reach = hi
            extent += right - left
            bare += (right - left) - covered
    shares = face.blank_shares()
    return {
        "glyphs": len(shares),
        "blank": statistics.median(shares),
        "gaps": len(gaps),
        "mean_gap": statistics.mean(gaps),
        "max_gap": max(gaps),
        "bare": bare / extent if extent else 0.0,
    }


def describe(m: dict) -> str:
    return (f"median blank share {m['blank']:.1%} over {m['glyphs']} glyphs; "
            f"{m['gaps']} gaps in run text, mean {m['mean_gap']:.3f} em, largest {m['max_gap']:.3f} em; "
            f"bare ground {m['bare']:.1%}")


def check(path: Path) -> list[str]:
    m = measure(path)
    out = []
    if m["blank"] > MAX_BLANK:
        out.append(f"{path}: error: the median blank share is {m['blank']:.1%}, above {MAX_BLANK:.0%}")
    if m["mean_gap"] > MAX_MEAN_GAP:
        out.append(f"{path}: error: the mean gap between signs is {m['mean_gap']:.3f} em, above {MAX_MEAN_GAP} em")
    if m["max_gap"] > MAX_GAP:
        out.append(f"{path}: error: the largest gap between signs is {m['max_gap']:.3f} em, above {MAX_GAP} em")
    want = respace.SPACING.get(path.name.split("-")[0], {}).get("space")
    if want is not None:
        font = TTFont(str(path))
        have = font["hmtx"][font.getBestCmap()[0x20]][0]
        if have != want:
            out.append(f"{path}: error: the space is {have} units, expected {want}")
    return out


def main():
    args = sys.argv[1:]
    report = "--report" in args
    paths = [Path(a) for a in args if a != "--report"] or sorted((ROOT / "fonts").glob("*-Regular.ttf"))
    status = 0
    for p in paths:
        problems = check(p)
        if report or not problems:
            print(f"{p}: {describe(measure(p))}")
        for line in problems:
            print(line)
        status |= bool(problems)
    sys.exit(status)


if __name__ == "__main__":
    main()
