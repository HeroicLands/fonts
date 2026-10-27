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
not the word space ``SPACING`` in tools/respace.py states for the face. A face set
open on purpose takes its own limits in ``OPEN``: Pirzath Hand is a printed working
hand, read in poor light, and stands every letter clear of the next, with 70 units of
white either side; its largest gap is held to the shared limit. Chalish Pilam Common sets every glyph in one
fixed cell and takes a largest gap of its own, and so does Chalish Pilam Ceremonial, which sets every sign
in its block's advance.

The sample lines are the texts of each face's specimens: the Khazari texts for
the Pirzath faces, the Nordmal lines for Thuravark Carved and the Vylari texts for
Semaron Kuriale, each as the code points stored for it in ``tools/texts/``; Qalezu Hand's fixtures, written in the
signs the fixtures name, a catch-before form as the catch and its sign; the sample inscriptions of Khelathi Zethu Glyphs, set as one
strip of signs; Teng Chou's Tantsou and Jurthati passages, each line one run
of characters; Chalish Pilam Common's night entry, each phrase one word; the glyphs of Chalish Pilam
Ceremonial's passage, each in its plain form, set as one strip; and the guard fixtures of
Veldikko, Vedyakshara Classical and Helonika Book, each a sequence of glyph codes. A joined face (Veldikko)
meets its neighbours at the join, and Vedyakshara's signs meet in one headline,
so their gaps are at most zero.
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
import codes  # noqa: E402
import respace  # noqa: E402

MAX_BLANK = 0.14
MAX_MEAN_GAP = 0.08
MAX_GAP = 0.22
# Faces set open on purpose: (median blank share, mean gap), in place of the shared limits,
# and optionally a largest gap in place of MAX_GAP. Chalish Pilam Common sets every glyph
# in one fixed cell with a gutter either side, so a narrow glyph leaves white beside it.
# Chalish Pilam Ceremonial sets every sign in its block's advance, so a number or a flat
# syllable sign standing alone, outside the block it is composed into, leaves most of the
# block white.
OPEN = {
    "PirzathHand": (0.30, 0.15),
    "ChalishPilamCommon": (0.25, 0.25, 0.40),
    "ChalishPilamCeremonial": (0.36, 0.35, 1.05),
}

SKIP = {".notdef", "notdef.box"}


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _pirzath_texts() -> list[str]:
    texts = _load("pirzath_specimens", TOOLS / "pirzath" / "specimens.py").TEXTS
    return [line for _, lines in texts for line in lines]


def _thuravark_texts() -> list[str]:
    return [line for _, line in _load("thuravark_specimens", TOOLS / "thuravark-carved" / "specimens.py").LINES]


def _semaron_texts() -> list[str]:
    return [line for _, line in _load("semaron_specimens", TOOLS / "semaron-kuriale" / "specimens.py").TEXTS]


def _written(face: str, texts: list[str]) -> list[str]:
    """The roman sample lines as the code points stored for them in ``tools/texts/<face>.json``."""
    return codes.Written(face).write(texts)


def _fixture_lines(folder: str, script: str, per_line: int) -> list[str]:
    """The code sequences of a face's guard fixtures, ``per_line`` words to a line."""
    fixtures = json.loads((TOOLS / folder / "fixtures.json").read_text(encoding="utf-8"))["fixtures"]
    words = [codes.text(script, f["codes"]) for f in fixtures]
    return [" ".join(words[i:i + per_line]) for i in range(0, len(words), per_line)]


def _pirzath_lines(face: str = "pirzath-carved") -> list[str]:
    return _written(face, _pirzath_texts())


def _thuravark_lines() -> list[str]:
    return _written("thuravark-carved", _thuravark_texts())


def _semaron_lines() -> list[str]:
    return _written("semaron-kuriale", _semaron_texts())


def _qalezu_lines() -> list[str]:
    enc = json.loads((TOOLS / "qalezu-hand" / "encoding.json").read_text(encoding="utf-8"))
    by_glyph = {g["glyph"]: chr(int(g["codepoint"][2:], 16)) for g in enc["glyphs"]}
    catch = next(g["glyph"] for g in enc["glyphs"] if "'" in g.get("typing", []))
    # A catch-before form has no code point: the catch and its sign are drawn as it.
    for form in enc["forms"]:
        by_glyph[form["glyph"]] = by_glyph[catch] + by_glyph[form["base"]]
    fixtures = json.loads((TOOLS / "qalezu-hand" / "fixtures.json").read_text(encoding="utf-8"))["fixtures"]
    words = ["".join(by_glyph[g] for g in f["signs"]) for f in fixtures if f["signs"] and all(g in by_glyph for g in f["signs"])]
    return [" ".join(words[i:i + 8]) for i in range(0, len(words), 8)]


def _zethu_lines() -> list[str]:
    guard = _load("zethu_guard", TOOLS / "khelathi-zethu-glyphs" / "guard.py")
    enc = json.loads((TOOLS / "khelathi-zethu-glyphs" / "encoding.json").read_text(encoding="utf-8"))
    cp = {e["id"]: chr(int(e["codepoint"][2:], 16)) for e in enc["signs"] if e.get("drawn")}
    return ["".join(cp[i] for i in ids if i in cp) for _, ids in guard.sample_lists()]


def _veldikko_lines() -> list[str]:
    return _fixture_lines("veldikko", "veldikko", 6)


def _vedyakshara_lines() -> list[str]:
    return _fixture_lines("vedyakshara", "vedyakshara", 6)


def _helonika_lines() -> list[str]:
    return _fixture_lines("helonika", "helonika", 6)


def _teng_chou_lines() -> list[str]:
    return _load("teng_chou_texts", TOOLS / "teng-chou" / "texts.py").lines()


def _chalish_lines() -> list[str]:
    """The night entry of tools/chalish-pilam/glyphs.py, one word to a phrase."""
    here = str(TOOLS / "chalish-pilam")
    sys.path.insert(0, here)
    for name in ("build_ufo", "glyphs", "strokes"):
        sys.modules.pop(name, None)
    try:
        import build_ufo
        import glyphs

        enc = json.loads((TOOLS / "chalish-pilam" / "encoding.json").read_text(encoding="utf-8"))["glyphs"]
        point = {e["glyph"]: chr(int(e["codepoint"][2:], 16)) for e in enc}
        return [" ".join("".join(point[build_ufo.glyph_name(g)] for g in gs) for _, gs in glyphs.PASSAGE)]
    finally:
        sys.path.remove(here)
        for name in ("build_ufo", "glyphs", "strokes"):
            sys.modules.pop(name, None)


def _ceremonial_lines() -> list[str]:
    """The glyphs of the passage of tools/chalish-pilam/ceremonial_passage.py with no joiner,
    so each glyph stands in its own plain form, set as one strip as an inscription runs on.
    A composed block sets its affixes with no advance of their own, so the strip measures
    the signs themselves."""
    passage = _load("ceremonial_passage", TOOLS / "chalish-pilam" / "ceremonial_passage.py")
    glyphs = [t for block, _ in passage.PASSAGE for t in block.split() if not t.startswith("JOINER_")]
    return [codes.text("chalishceremonial", " ".join(glyphs))]


# Each face: its sample lines, its direction and the features its class turns on.
FACES = {
    "PirzathCarved": (_pirzath_lines, "ltr", {}),
    "PirzathHand": (lambda: _pirzath_lines("pirzath-hand"), "ltr", {}),
    "ThuravarkCarved": (_thuravark_lines, "ltr", {}),
    "SemaronKuriale": (_semaron_lines, "ltr", {}),
    "QalezuHand": (_qalezu_lines, "rtl", {}),
    "KhelathiZethuGlyphs": (_zethu_lines, "rtl", {}),
    "TengChou": (_teng_chou_lines, "ltr", {}),
    "ChalishPilamCommon": (_chalish_lines, "ltr", {}),
    "ChalishPilamCeremonial": (_ceremonial_lines, "ltr", {}),
    "Veldikko": (_veldikko_lines, "rtl", {}),
    "VedyaksharaClassical": (_vedyakshara_lines, "ltr", {}),
    "HelonikaBook": (_helonika_lines, "ltr", {}),
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
    max_blank, max_mean, *rest = OPEN.get(path.name.split("-")[0], (MAX_BLANK, MAX_MEAN_GAP))
    max_gap = rest[0] if rest else MAX_GAP
    if m["blank"] > max_blank:
        out.append(f"{path}: error: the median blank share is {m['blank']:.1%}, above {max_blank:.0%}")
    if m["mean_gap"] > max_mean:
        out.append(f"{path}: error: the mean gap between signs is {m['mean_gap']:.3f} em, above {max_mean} em")
    if m["max_gap"] > max_gap:
        out.append(f"{path}: error: the largest gap between signs is {m['max_gap']:.3f} em, above {max_gap} em")
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
