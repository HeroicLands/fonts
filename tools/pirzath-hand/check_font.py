# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Load the built hand font and confirm its character map, names, outlines and joined forms.

    .venv/bin/python tools/pirzath-hand/check_font.py [fonts/PirzathHand-Regular.ttf]

The hand draws the same code points as the carved face, so the character map is
checked by the same rules, and Latin text draws the box. Every mapped glyph and every lost letter
must carry an outline, the default-ignorable characters must draw nothing, every
other character must map to the box (tools/notdef_box.py),
and the .woff2 beside the .ttf must open and carry the same glyphs.

The joined forms are checked from the outlines. Every joining letter has three
joined forms beside its plain one, with the same advance: .init with a long
exit, .fina with a long entry and .medi with both. The long ends are the two
halves of one connector cut at the advance edge, so the ink where a long exit
meets the edge is the ink where a long entry leaves it: one stroke, at the
same height in every letter. A short end, the plain letter's at both ends,
leaves the edge clear on the join line, so the lifted look keeps its gap.
"""

import importlib.util
import sys
from pathlib import Path

from fontTools.pens.recordingPen import RecordingPen
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent.parent


def _carved_check():
    spec = importlib.util.spec_from_file_location("pirzath_check", ROOT / "tools" / "pirzath" / "check_font.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


sys.path.insert(0, str(ROOT / "tools"))
import vertical  # noqa: E402

CARVED = _carved_check()
font_names = CARVED.font_names
notdef_box = CARVED.notdef_box

CONSONANTS = [
    "p", "b", "f", "v", "m", "t", "d", "t_h", "d_h", "n", "k", "g", "k_h", "g_h", "h", "s", "z", "l", "r",
    "sh", "zh", "ch", "ts", "j", "q", "ng", "ny", "hl", "catch", "w", "y",
]
VOWELS = ["a", "e", "i", "o", "u", "aacute", "eacute", "iacute", "oacute", "uacute", "ai", "au", "ei", "oi", "ou"]
DOUBLED = [f"{c}_{c}" for c in CONSONANTS]
# The letters that take the connector. Everything else stands off the line.
JOINING = CONSONANTS + VOWELS + DOUBLED
MARKS = ["lengthmark"]
FORMS = {".init": (False, True), ".medi": (True, True), ".fina": (True, False)}
IGNORABLES = [*range(0x200B, 0x2010), *range(0x202A, 0x202F), *range(0x2066, 0x206A), 0xFEFF]
EMPTY = {"ignorable", "ignorable.sub"}

# The connector crosses the advance edge about this high. Its cut face is one stroke, THICKNESS thick.
MID = 83
THICKNESS = 54
TOLERANCE = 1.5  # units: the most the two cut faces of a connector may differ in height
PROBE = 0.5  # how far in from the advance edge a face is read
REACH = 20  # units: how far past the advance edge a short exit may run


def contours(glyphset, name):
    pen = RecordingPen()
    glyphset[name].draw(pen)
    out, cur = [], []
    for op, args in pen.value:
        if op == "moveTo":
            cur = [args[0]]
        elif op == "lineTo":
            cur.append(args[0])
        elif op == "qCurveTo":
            offs, end = list(args[:-1]), args[-1]
            ons = [((a[0] + b[0]) / 2, (a[1] + b[1]) / 2) for a, b in zip(offs, offs[1:])] + [end]
            p0 = cur[-1]
            for c, p1 in zip(offs, ons):
                for s in range(1, 17):
                    t, u = s / 16, 1 - s / 16
                    cur.append((u * u * p0[0] + 2 * u * t * c[0] + t * t * p1[0],
                                u * u * p0[1] + 2 * u * t * c[1] + t * t * p1[1]))
                p0 = p1
        elif op in ("closePath", "endPath") and cur:
            out.append(cur)
            cur = []
    return out


def ink_on(cs, x):
    """The heights at which the vertical line at x is inside the glyph, as [(low, high)] by winding."""
    crossings = []
    for c in cs:
        for (x1, y1), (x2, y2) in zip(c, c[1:] + c[:1]):
            if (x1 <= x < x2) or (x2 <= x < x1):
                y = y1 + (y2 - y1) * (x - x1) / (x2 - x1)
                crossings.append((y, 1 if x2 > x1 else -1))
    crossings.sort()
    out, wind, start = [], 0, 0.0
    for y, d in crossings:
        if wind == 0:
            start = y
        wind += d
        if wind == 0:
            out.append((start, y))
    return out


def face(cs, x):
    """The ink of the connector's cut face at x: the interval across the join height, or None."""
    for lo, hi in ink_on(cs, x):
        if lo <= MID <= hi:
            return (lo, hi)
    return None


def join_problems(font: TTFont) -> list[str]:
    problems = []
    glyphset = font.getGlyphSet()
    hmtx = font["hmtx"]
    order = set(font.getGlyphOrder())
    faces = {}
    for name in JOINING:
        if name not in order:
            problems.append(f"{name}: the letter is missing")
            continue
        adv = hmtx[name][0]
        for suffix, (entry, exit_) in [("", (False, False))] + list(FORMS.items()):
            g = name + suffix
            if g not in order:
                problems.append(f"{g}: the joined form is missing")
                continue
            if hmtx[g][0] != adv:
                problems.append(f"{g}: its advance {hmtx[g][0]} differs from {name}'s {adv}")
            cs = contours(glyphset, g)
            for long_, x, what in ((exit_, adv - PROBE, "exit"), (entry, PROBE, "entry")):
                f = face(cs, x)
                if long_:
                    if f is None:
                        problems.append(f"{g}: the long {what} has no ink on the join line at the advance edge")
                    else:
                        faces[g, what] = f
                elif what == "entry" and f is not None:
                    problems.append(f"{g}: the short entry reaches the advance edge")
            if not exit_ and face(cs, adv + REACH) is not None:
                problems.append(f"{g}: the short exit runs more than {REACH} units past the advance edge")
    if faces:
        lows = sorted(f[0] for f in faces.values())
        highs = sorted(f[1] for f in faces.values() if f[1] - f[0] < THICKNESS)
        low, high = lows[len(lows) // 2], highs[len(highs) // 2]
        for (g, what), f in faces.items():
            if abs(f[0] - low) > TOLERANCE or (f[1] - f[0] < THICKNESS and abs(f[1] - high) > TOLERANCE):
                problems.append(f"{g}: the {what} face spans {f[0]:.1f}..{f[1]:.1f}, the connector's is {low:.1f}..{high:.1f}")
    return problems


def check(path: Path) -> list[str]:
    problems = []
    font = TTFont(str(path))
    order = set(font.getGlyphOrder())
    glyf = font["glyf"]
    cmap = font.getBestCmap()
    if not cmap:
        return ["no Unicode cmap"]
    for cp, name in sorted(cmap.items()):
        if name not in order:
            problems.append(f"U+{cp:04X} maps to {name}, which is not in the font")
        elif name != "space" and name not in EMPTY and glyf[name].numberOfContours == 0:
            problems.append(f"U+{cp:04X} maps to {name}, which has no outline")
    problems += CARVED.latin_problems(cmap)
    for name in CARVED.LOST_LETTERS:
        if name not in order or glyf[name].numberOfContours == 0:
            problems.append(f"the lost letter {name} is missing or draws nothing")
    for name in JOINING + ["period", "exclam", "comma", "hyphen", "quote.open", "quote.close", ".notdef"] + \
            [f"num.{i}" for i in range(16)]:
        if name not in order or glyf[name].numberOfContours == 0:
            problems.append(f"{name} is missing or draws nothing")
    if "space" not in order or glyf["space"].numberOfContours != 0:
        problems.append("the space must be in the font and draw nothing")
    for key in "?;:":
        if cmap.get(ord(key)) != notdef_box.BOX:
            problems.append(f"{key!r} is {cmap.get(ord(key))}; it must be {notdef_box.BOX}")
    problems += [line.split(": error: ", 1)[1] for line in notdef_box.check(path)]
    problems += [line.split(": error: ", 1)[1] for line in font_names.check(path)]
    hmtx = font["hmtx"]
    for cp in IGNORABLES:
        if cmap.get(cp) != "ignorable":
            problems.append(f"U+{cp:04X} must map to the empty glyph 'ignorable'")
    for name in EMPTY:
        if name not in order or glyf[name].numberOfContours != 0 or hmtx[name][0] != 0:
            problems.append(f"{name} must be in the font, empty and without advance")
    classes = font["GDEF"].table.GlyphClassDef.classDefs if "GDEF" in font else {}
    for name in MARKS:
        if name not in order or glyf[name].numberOfContours == 0:
            problems.append(f"{name} is missing or draws nothing")
        elif classes.get(name) != 3:
            problems.append(f"{name} is not a mark in GDEF")
        elif hmtx[name][0] != 0:
            problems.append(f"{name} has an advance")
    for name in ("GSUB", "GPOS"):
        if name not in font:
            problems.append(f"no {name} table")
    if "GSUB" in font:
        tags = {fr.FeatureTag for fr in font["GSUB"].table.FeatureList.FeatureRecord}
        for tag in ("ss01", "ccmp", "liga", "rlig"):
            if tag not in tags:
                problems.append(f"no {tag} feature")
    if "GPOS" in font:
        tags = {fr.FeatureTag for fr in font["GPOS"].table.FeatureList.FeatureRecord}
        if "kern" in tags:
            problems.append("a kern feature is present; no kerning moves a join point")
    if font["head"].unitsPerEm != 1000:
        problems.append(f"units per em is {font['head'].unitsPerEm}, expected 1000")
    top = max(b for g in glyf.keys() if glyf[g].numberOfContours for b in [glyf[g].yMax])
    bottom = min(glyf[g].yMin for g in glyf.keys() if glyf[g].numberOfContours)
    # The accepted overshoot of tools/vertical.py reaches past the line metrics.
    band = min(
        glyf[g].yMin
        for g in glyf.keys()
        if glyf[g].numberOfContours and g.split(".")[0] not in vertical.OVERSHOOT["PirzathHand"]
    )
    hhea, os2 = font["hhea"], font["OS/2"]
    if hhea.ascent < top or hhea.descent > band:
        problems.append(f"the line metrics {hhea.ascent}/{hhea.descent} do not clear the ink {top}/{band}")
    if os2.usWinAscent < top or os2.usWinDescent < -bottom:
        problems.append("the Windows metrics do not clear the ink")
    names = {n.nameID: n.toUnicode() for n in font["name"].names if n.platformID == 3}
    expect = {
        1: "Pirzath Hand",
        5: "Version 0.2",
        13: "SIL Open Font License 1.1",
        14: "https://openfontlicense.org",
    }
    for nid, value in expect.items():
        if names.get(nid) != value:
            problems.append(f"name {nid} is {names.get(nid)!r}, expected {value!r}")
    if 7 in names:
        problems.append("name table carries a trademark")
    if not names.get(0, "").startswith("Copyright"):
        problems.append("name table carries no copyright line")
    problems += join_problems(font)

    woff2 = path.with_suffix(".woff2")
    if not woff2.exists():
        problems.append(f"{woff2} missing")
    else:
        w = TTFont(str(woff2))
        if w.getGlyphOrder() != font.getGlyphOrder():
            problems.append("woff2 glyph order differs from the ttf")
    print(f"{path}: {len(cmap)} code points mapped over {len(order)} glyphs, "
          f"{len(JOINING)} joining letters in {len(JOINING) * (len(FORMS) + 1)} forms with matching connector faces")
    return problems


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "fonts" / "PirzathHand-Regular.ttf"
    problems = check(path)
    for p in problems:
        print(f"{path}: error: {p}")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
