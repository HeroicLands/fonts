# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Confirm that every face shares one vertical standard, Monaspace Neon's.

    .venv/bin/python tools/vertical.py [font ...]

A page that mixes roman text and a script must show each script as large as the
roman beside it, and no glyph may reach into the line above or below. Every face
therefore takes Monaspace Neon's vertical metrics at 1000 units to the em, and is
scaled so that its typical letters stand as tall as Neon's x-height or cap height. A
font fails when

- its hhea or OS/2 typographic ascender, descender or line gap differs from the
  table below;
- its OS/2 winAscent or winDescent is smaller than the table or than the glyph boxes
  need, or larger than either by more than 2 units: each is the larger of the table
  value and the extent of the glyph boxes, so that Windows never clips a glyph;
- USE_TYPO_METRICS (OS/2 fsSelection bit 7) is clear;
- the ascender and descender of the face's source, ``sources/<Face>.ufo``, differ from
  the table;
- the median height of its typical letters, measured from the outlines, differs by
  more than 2% from its target, Neon's x-height (0.5135 em) or cap height (0.73 em);
- its OS/2 sxHeight or sCapHeight differs by more than 2 units from the median
  height of its typical x-height letters or capitals;
- a glyph's ink leaves the band between the ascent and the descent, other than
  the accepted overshoot: Semaron Kuriale's ``f j p s g``, whose descenders reach below
  it, and Veldikko's raised stops, its riser _l_ and its nasals in every form,
  whose stems and tails reach past both edges, and its length bar: Veldikko's
  bowls, not its extenders, stand at the x-height. Vedyakshara Classical's hooks,
  r-foot and fused r reach below it, on every sign that carries them; its body
  stands at the x-height under the headline, and its digits, which stand free of
  the headline exactly as tall as the body, are its typical letters. Helonika Book's
  _f_, _g_ and _j_ turn their tails back just below it.

Each face has one set of typical letters for each of the two heights; a script with
a single height uses one set for both.

A script with no capitals is measured against the height a line of Latin is read at.
Pirzath Hand has no capitals and few extenders, so nearly all of its ink stands in
one band: its consonants are its typical letters and stand at the cap height, as
Pirzath Carved's consonants do, and its vowels are its x-height letters.

A face written in columns (``COLUMNS``: Teng Chou) also carries vertical metrics, and
fails when

- it has no ``vhea`` or ``vmtx`` table;
- its ``vhea`` ascent and descent together are not one em, or a character's or
  sign's vertical advance is not exactly one em, so a column of N characters
  would not be N em tall;
- its vertical origin, the top of its ink plus its top side bearing, differs from
  the other glyphs', so the characters would not stand evenly down a column;
- its ink is not centred, within 2 units, on its horizontal advance, which is the
  column's axis, or its ink leaves the square it stands in.
"""

import json
import math
import plistlib
import statistics
import sys
from pathlib import Path

from fontTools.pens.boundsPen import BoundsPen
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent

# Monaspace Neon Regular at 2000 units to the em, halved to 1000.
ASCENT, DESCENT, LINE_GAP = 945, -200, 100
WIN_ASCENT, WIN_DESCENT = 945, 250
X_HEIGHT, CAP_HEIGHT = 0.5135, 0.73
TOLERANCE = 0.02
TYPO_METRICS_BIT = 1 << 7

# The scale each face took: the factor that brings its target height to Neon's.
SCALES = {
    "SemaronKuriale": 1.02,
    "PirzathCarved": 1.04,
    "PirzathHand": 1.0,
    "ThuravarkCarved": 0.99,
    "QalezuHand": 0.99,
    "KhelathiZethuGlyphs": 0.77,
    "TengChou": 0.81,
    "Veldikko": 1.72,
    "VedyaksharaClassical": 1.0,
    "HelonikaBook": 1.0,
}

CONSONANTS = (
    "b d f g h hl j k l m n ng ny p q r s sh t ts v w y z zh ch".split()
)
# Pirzath Hand's consonants that stand from the line to the body, with no extender and
# no arm worn short, and its vowels that stand from the line to the vowel height.
HAND_CONSONANTS = "p b f v t d k g m n s sh z zh r ts ch q".split()
HAND_VOWELS = "a e i u".split()
VOWELS = "a aacute ai au e ei i o oi ou u".split()
SEMARON_MINUSCULES = "a b c d e g i j k m n o p r s w y z".split()
SEMARON_CAPITALS = "A B C D E F G H I J K L M N O P R S T TH U V W Y Z".split()
QALEZU = "b d f g gh h k kh l m n p q r s sh t th tj w y z".split()
VELDIKKO_STOPS = "p t k d".split()
VELDIKKO_BODY = ["r"]  # the crozier, the one letter standing at the bowls' height alone
THURAVARK = "a ai au b d dh e f g gh h hl i j k kh l m n ng o oi p r s t th u v w y z".split()
HELONIKA_X = "b e e.long o s u".split()  # the minuscules that stand on the body, line to x-height, with no tail
HELONIKA_CAPS = "A B E F G H I J K M N P R S T".split()
# Vedyakshara's signs hang from a headline above the x-height; its digits stand free of
# it, exactly as tall as the body, so they are its typical x-height letters.
VEDYAKSHARA_DIGITS = [f"num.{d}" for d in range(10)]
VEDYAKSHARA_SIGNS = "ka ga ja ta da na pa ba ma ya ra la va sa ha".split()


def vedyakshara_low() -> set[str]:
    """Vedyakshara's glyphs that reach below the line: every sign, by the r-foot, the
    r-stem of a fused r or a hook under it, and the hooks themselves."""
    enc = json.loads((ROOT / "tools" / "vedyakshara" / "encoding.json").read_text(encoding="utf-8"))
    names = {g["glyph"] for g in enc["glyphs"] if g["kind"] in ("consonant", "vowel")}
    return names | {f["glyph"] for f in enc["fused"]} | {"fa", "vs", "hook"}

# Each face: the glyphs whose median height is x-height, those for cap height, and the
# target. Zethu names its standing signs from its encoding table.
FACES = {
    "SemaronKuriale": {"x": SEMARON_MINUSCULES, "cap": SEMARON_CAPITALS, "target": "x"},
    "PirzathCarved": {"x": VOWELS, "cap": CONSONANTS, "target": "cap"},
    "PirzathHand": {"x": HAND_VOWELS, "cap": HAND_CONSONANTS, "target": "cap"},
    "ThuravarkCarved": {"x": THURAVARK, "cap": THURAVARK, "target": "cap"},
    "QalezuHand": {"x": QALEZU, "cap": QALEZU, "target": "x"},
    "KhelathiZethuGlyphs": {"x": None, "cap": None, "target": "cap"},
    "TengChou": {"x": "characters", "cap": "characters", "target": "cap"},
    "Veldikko": {"x": VELDIKKO_BODY, "cap": VELDIKKO_STOPS, "target": "x"},
    "VedyaksharaClassical": {"x": VEDYAKSHARA_DIGITS, "cap": VEDYAKSHARA_SIGNS, "target": "x"},
    "HelonikaBook": {"x": HELONIKA_X, "cap": HELONIKA_CAPS, "target": "x"},
}

# Glyphs allowed to leave the band, by face: the first part of the glyph name, before
# any ``.init``, ``.medi`` or ``.fina`` suffix.
OVERSHOOT = {
    "SemaronKuriale": {"f", "j", "p", "s", "g"},
    # the raised stems, the riser and the nasals' tails reach well past Semaron's
    # extenders by design; the bowls stand at the x-height
    "Veldikko": set("p t k d g th dhasp kh gh tej dej kej gej l m n ng bar".split()),
    # the hooks, the r-foot and a fused r's stem hang below the line
    "VedyaksharaClassical": vedyakshara_low(),
    # the tails of the descending minuscules turn back a little below the descent
    "HelonikaBook": {"f", "g", "j"},
}


def stem(path: Path) -> str:
    return path.name.split("-")[0]


def standing_signs() -> list[str]:
    """The Zethu signs that stand a full quadrat tall: the typical height of the script."""
    enc = json.loads((ROOT / "tools" / "khelathi-zethu-glyphs" / "encoding.json").read_text(encoding="utf-8"))
    return [e["glyph"] for e in enc["signs"] if e["drawn"] and e["box"]["a"][1] >= 99]


def bounds(font: TTFont) -> dict[str, tuple]:
    """The ink bounds of every glyph that draws, by name."""
    glyphs = font.getGlyphSet()
    out = {}
    for name in font.getGlyphOrder():
        pen = BoundsPen(glyphs)
        glyphs[name].draw(pen)
        if pen.bounds:
            out[name] = pen.bounds
    return out


def median_height(ink: dict[str, tuple], names: list[str]) -> float:
    found = [ink[n][3] - ink[n][1] for n in names if n in ink]
    return statistics.median(found) if found else 0.0


def teng_chou_characters() -> list[str]:
    """Teng Chou's characters, which fill the square; the syllabary sits smaller."""
    sys.path.insert(0, str(ROOT / "tools"))
    import codepoint_order

    return [r["glyph"] for r in codepoint_order.ltr_table("TengChou-Regular") if r["kind"] == "character"]


def typical(face: str, kind: str) -> list[str]:
    names = FACES[face][kind]
    if names == "characters":
        return teng_chou_characters()
    return standing_signs() if names is None else names


def target_units(face: str, upem: int) -> float:
    return (X_HEIGHT if FACES[face]["target"] == "x" else CAP_HEIGHT) * upem


def check(path: Path) -> list[str]:
    """Return the problems of the built font at path, each ``path: error: message``."""
    face = stem(path)
    font = TTFont(str(path))
    upem = font["head"].unitsPerEm
    hhea, os2 = font["hhea"], font["OS/2"]
    ink = bounds(font)
    problems = []

    def err(message: str):
        problems.append(f"{path}: error: {message}")

    if upem != 1000:
        err(f"unitsPerEm is {upem}, not 1000")
    for label, got, want in (
        ("hhea ascent", hhea.ascent, ASCENT),
        ("hhea descent", hhea.descent, DESCENT),
        ("hhea lineGap", hhea.lineGap, LINE_GAP),
        ("OS/2 typoAscender", os2.sTypoAscender, ASCENT),
        ("OS/2 typoDescender", os2.sTypoDescender, DESCENT),
        ("OS/2 typoLineGap", os2.sTypoLineGap, LINE_GAP),
    ):
        if got != want:
            err(f"{label} is {got}, not {want}")
    info_path = ROOT / "sources" / f"{face}.ufo" / "fontinfo.plist"
    if info_path.exists():
        info = plistlib.loads(info_path.read_bytes())
        for key, want in (("ascender", ASCENT), ("descender", DESCENT)):
            if info.get(key) != want:
                err(f"the source's {key} is {info.get(key)}, not {want}")
    if not os2.fsSelection & TYPO_METRICS_BIT:
        err("USE_TYPO_METRICS (fsSelection bit 7) is not set")

    allowed = OVERSHOOT.get(face, set())
    glyf = font["glyf"]
    boxes = [glyf[n] for n in font.getGlyphOrder() if glyf[n].numberOfContours]
    top = max((g.yMax for g in boxes), default=0)
    bottom = min((g.yMin for g in boxes), default=0)
    for label, got, want in (
        ("OS/2 winAscent", os2.usWinAscent, max(WIN_ASCENT, math.ceil(top))),
        ("OS/2 winDescent", os2.usWinDescent, max(WIN_DESCENT, math.ceil(-bottom))),
    ):
        if not want <= got <= want + 2:
            err(f"{label} is {got}, not {want}, the larger of the table and the glyph boxes")

    target = target_units(face, upem)
    body = median_height(ink, typical(face, FACES[face]["target"]))
    if not body or abs(body - target) > TOLERANCE * target:
        err(f"the typical letters stand {body:g} tall, not within 2% of {target:g}")
    for label, got, kind in (("sxHeight", os2.sxHeight, "x"), ("sCapHeight", os2.sCapHeight, "cap")):
        want = median_height(ink, typical(face, kind))
        if abs(got - want) > 2:
            err(f"OS/2 {label} is {got}, but its typical letters stand {want:g} tall")

    for name, (_, low, _, high) in sorted(ink.items()):
        if name.split(".")[0] in allowed:
            continue
        if high > ASCENT:
            err(f"{name} reaches y {high:g}, above the ascent {ASCENT}")
        if low < DESCENT:
            err(f"{name} reaches y {low:g}, below the descent {DESCENT}")
    problems += column_problems(path, font)
    return problems


# Faces written in vertical columns, with the prefixes of the glyphs that stand in them.
COLUMNS = {"TengChou": ("tc.", "js.")}


def column_problems(path: Path, font: TTFont) -> list[str]:
    """What is wrong with the vertical metrics of a face written in columns."""
    face = stem(path)
    if face not in COLUMNS:
        return []
    if "vhea" not in font or "vmtx" not in font:
        return [f"{path}: error: a face written in columns has no vhea or vmtx table"]
    out = []
    vhea, vmtx, glyf, hmtx = font["vhea"], font["vmtx"], font["glyf"], font["hmtx"]
    ink = bounds(font)
    upem = font["head"].unitsPerEm
    square = vhea.ascent - vhea.descent
    if square != upem:
        out.append(f"{path}: error: the vhea ascent and descent span {square} units, not the em, {upem}")
    origins = {}
    for name in font.getGlyphOrder():
        if not name.startswith(COLUMNS[face]):
            continue
        g = glyf[name]
        height, tsb = vmtx[name]
        if height != upem:
            out.append(f"{path}: error: {name} has the vertical advance {height}, not one em, {upem}")
        if not g.numberOfContours:
            continue
        origins[name] = g.yMax + tsb
        width = hmtx[name][0]
        left, low, right, _ = ink[name]
        if abs(left - (width - right)) > 2:
            out.append(f"{path}: error: {name} is not centred on its advance: {left:.0f} left, {width - right:.0f} right")
        top = g.yMax + tsb
        if low < top - upem:
            out.append(f"{path}: error: {name} reaches below the square it stands in")
    if origins:
        common = statistics.mode(origins.values())
        for name, origin in origins.items():
            if origin != common:
                out.append(f"{path}: error: {name} has its vertical origin at {origin}, not {common}")
    return out


def main():
    paths = [Path(a) for a in sys.argv[1:]] or sorted((ROOT / "fonts").glob("*-Regular.ttf"))
    status = 0
    for p in paths:
        problems = check(p)
        print(f"{p}: ok" if not problems else f"{p}: {len(problems)} problems")
        for line in problems[:10]:
            print(line)
        if len(problems) > 10:
            print(f"{p}: error: ... and {len(problems) - 10} more")
        status |= bool(problems)
    sys.exit(status)


if __name__ == "__main__":
    main()
