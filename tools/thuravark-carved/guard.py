# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Shape Thuravark Carved's fixtures and assert the font renders each one rightly.

    .venv/bin/python tools/thuravark-carved/guard.py [--font fonts/ThuravarkCarved-Regular.ttf]

Each fixture in ``fixtures.json`` is a sequence of Thuravark's glyph codes
(``tools/codes/thuravark.json``), with ``U+XXXX`` for a character the script has no
code for, the features it is shaped with, and the glyphs the font must shape it to.
They cover every stave of the row, the acute mark drawn as the stave again
(``a.acute``), the numerals, the full stop and the space, and characters the font lacks,
which print the box. The imperial recension's fixtures cover the three diphthong staves;
a crowned name, whose every glyph takes its crowned form between the opened and the
closed post; an open with no close, and a close with no open, which stay bare posts with
the staves beside them unchanged; a crown longer than the font frames; and the bound
runes with ``ss01`` on, and the same text unchanged with it off. A rendered crowned
name's rails are checked for a break.

A geometry section asserts the stave design: 31 distinct staves and ten bound
runes, each bound rune the two staves' branches on one stem by the rules of
``tools/thuravark-carved/staves.py``, no horizontal edge in any of them,
numerals taller than the staves, and every pair visibly apart at reading size.
"""

import argparse
import itertools
import json
import sys
from pathlib import Path

from fontTools.pens.recordingPen import RecordingPen
from fontTools.ttLib import TTFont
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import codes  # noqa: E402
from render import Renderer, Shaped  # noqa: E402

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SCRIPT = "thuravark"


# Each stave's branches, by the design: the side a branch leaves the stem on (F forward,
# B back), the level it leaves from and the level it ends at (T top, M middle, 0 foot).
BRANCHES = {
    'a': 'F0T',
    'e': 'FTM BTM',
    'i': '',
    'o': 'FTM F0M BTM B0M',
    'u': 'B0T',
    'p': 'FT0 BT0',
    'b': 'FT0 BT0 B0M',
    'f': 'FT0 BT0 FMT',
    'v': 'FT0 BT0 B0M FMT',
    't': 'F0T B0T',
    'd': 'F0T B0T BTM',
    'th': 'F0T B0T FMT',
    'dh': 'F0T B0T BTM FMT',
    'k': 'FTM F0M',
    'g': 'FTM F0M BM0',
    'kh': 'FTM F0M FMT',
    'gh': 'FTM F0M BM0 FMT',
    's': 'FTM BM0',
    'z': 'FT0 B0T',
    'h': 'BM0 FMT',
    'l': 'FM0',
    'r': 'BTM B0M',
    'hl': 'FM0 FMT',
    'm': 'FT0 BM0',
    'n': 'F0T BMT',
    'ng': 'FTM F0M FMT FM0',
    'j': 'FMT',
    'w': 'BMT',
    # The imperial recension's diphthong staves.
    'ai': 'F0T FMT',
    'au': 'F0T B0M',
    'oi': 'BTM B0M FMT',
}

# The bound runes of the recension: two staves on one stem, set by ss01.
BOUND = {
    'e_n': ('e', 'n'),
    'e_l': ('e', 'l'),
    'a_r': ('a', 'r'),
    'a_l': ('a', 'l'),
    'm_a': ('m', 'a'),
    'z_a': ('z', 'a'),
    'k_a': ('k', 'a'),
    'u_r': ('u', 'r'),
    'l_m': ('l', 'm'),
    'l_th': ('l', 'th'),
}

# The 28 staves of the row, by the glyph name the font gives each, and the recension's three.
ROW = ("a e i o u p b f v t d th dh k g kh gh s z h l r hl m n ng j w").split()
RECENSION = "ai au oi".split()
STAVES = ROW + RECENSION

FIXTURES = [
    (f["codes"], {tag: True for tag in f.get("features", [])}, f["glyphs"])
    for f in json.loads((HERE / "fixtures.json").read_text(encoding="utf-8"))["fixtures"]
]
# A crowned name; without its last character, the close, it is an open with no close.
CROWNED = "CROWN_OPEN THRESK I LA A NELTH DRESK U+0020 THRESK A U RELTH A SVELD CROWN_CLOSE"


def shaping(font: Path) -> list[str]:
    r = Renderer(font)
    failures = []
    for sequence, features, want in FIXTURES:
        got = [r.order[g[0]] for g in r.shape(codes.text(SCRIPT, sequence), features).glyphs]
        if got != want:
            failures.append(f"{sequence} {features}: shaped {got}, expected {want}")
    failures += frame_problems(r)
    print(f"{font}: {len(FIXTURES)} fixtures, {len(failures)} failures")
    return failures


def frame_problems(r: Renderer) -> list[str]:
    """A rendered crowned name's rails run unbroken from post to post, and an open with
    no close draws nothing but its post."""
    problems = []
    size = 48
    crowned = codes.text(SCRIPT, CROWNED)
    for label, text, framed in (("crowned", crowned, True), ("unclosed", crowned[:-1], False)):
        shaped = r.shape(text)
        width = int(shaped.advance * size / r.upem) + 40
        img = Image.new("RGB", (width, 100), "white")
        r.draw(img, 20, 70, shaped, size, "black")
        px = img.convert("L").load()
        for rail in (838, -105):  # the middle of the top rail (817 to 859) and of the bottom (-126 to -84)
            y = round(70 - rail * size / r.upem)
            inked = [x for x in range(width) if px[x, y] < 128]
            if framed:
                gaps = [x for x in range(inked[0], inked[-1] + 1) if px[x, y] >= 128] if inked else []
                if not inked or gaps:
                    problems.append(f"{label}: the rail at {rail} is broken at {gaps[:5]}")
            elif len(inked) > 2 * STEM_W * size / r.upem:
                problems.append(f"{label}: ink along the rail line at {rail} beyond the post")
    return problems


# --- the design -------------------------------------------------------------


def edges(font: TTFont, name: str):
    """The straight edges of a glyph's outline, as (x1, y1, x2, y2)."""
    pen = RecordingPen()
    font.getGlyphSet()[name].draw(pen)
    out = []
    for op, args in pen.value:
        if op == "moveTo":
            start = cur = args[0]
        elif op == "lineTo":
            out.append((*cur, *args[0]))
            cur = args[0]
        elif op == "closePath" and cur != start:
            out.append((*cur, *start))
    return out


def bound_branches(name: str) -> tuple[str, str | None]:
    """A bound rune's branches, and what breaks the system's rule for binding, if anything."""
    first, second = BOUND[name]
    a, b = set(BRANCHES[first].split()), set(BRANCHES[second].split())
    joined = " ".join(sorted(a | b))
    if a & b:
        return joined, f"{first} and {second} share a branch"
    if len(a | b) > 4:
        return joined, "more than four branches"
    if any(sum(1 for br in a | b if br[1] == level) > 2 for level in "0MT"):
        return joined, "three branches leave the stem at one level"
    return joined, None


def geometry(path: Path) -> list[str]:
    problems = []
    if list(BRANCHES) != STAVES:
        problems.append(f"the staves are {list(BRANCHES)}, expected the 28 of the row and the recension's three")
    sets = {}
    drawn = dict(BRANCHES)
    for name in BOUND:
        drawn[name], why = bound_branches(name)
        if why:
            problems.append(f"{name}: {why}")
    for name, spec in drawn.items():
        key = frozenset(spec.split())
        if key in sets:
            problems.append(f"{name} and {sets[key]} have the same branches")
        sets[key] = name
        for b in spec.split():
            if b[1] == b[2]:
                problems.append(f"{name}: branch {b} is horizontal")
        if len(spec.split()) > 4:
            problems.append(f"{name} has more than four branches")
    font = TTFont(str(path))
    # No stave runs along the line of text.
    for name in list(drawn):
        for e in edges(font, name):
            if e[1] == e[3]:
                problems.append(f"{name}: a horizontal edge")
    glyf = font["glyf"]
    stave_top = max(glyf[n].yMax for n in STAVES)
    numeral_bottom = min(glyf[f"num.{i}"].yMax for i in range(10))
    if numeral_bottom <= stave_top:
        problems.append("the numerals are not taller than the staves")
    # Every pair of staves, and nought against i, differs at reading size.
    r = Renderer(path)
    size = 36
    masks = {}
    for name in STAVES + list(BOUND) + ["num.0"]:
        masks[name] = ink(r, name, size)
    worst = []
    for a, b in itertools.combinations(masks, 2):
        diff = pixel_difference(masks[a], masks[b])
        worst.append((diff, a, b))
    worst.sort()
    for diff, a, b in worst:
        if diff < MIN_DIFFERENCE:
            problems.append(f"{a} and {b} differ by only {diff} pixels at {size} px")
    print(f"{path}: {len(masks)} forms, closest pairs at {size} px: "
          + ", ".join(f"{a}/{b} {d}" for d, a, b in worst[:6]))
    return problems


MIN_DIFFERENCE = 20


STEM_H = 733  # every stave stands this tall
STEM_W = 84  # stroke weight of stems and branches
BEARING = 65  # room between the ink of one stave and the next
LONG_RUN = STEM_H / 2.73  # horizontal run of a branch that spans the whole stem
HALF_RUN = (STEM_H / 2) / 0.86  # horizontal run of a branch that spans half of it
NUMERAL_LIMB_RUN = 220  # the limb of nought runs this far to each side of its stem


def stem_x(name: str) -> float:
    """The column of a glyph's stem, from the design's bearing and its longest back branch."""
    if name == "num.0":
        return BEARING + NUMERAL_LIMB_RUN
    spec = BRANCHES[name] if name in BRANCHES else bound_branches(name)[0]
    back = [
        LONG_RUN if {b[1], b[2]} == {"T", "0"} else HALF_RUN
        for b in spec.split()
        if b[0] == "B"
    ]
    return BEARING + max(back + [STEM_W / 2])


def ink(r: Renderer, name: str, size: int):
    """The glyph's ink at `size`, with its stem on a fixed column."""
    gid = r.order.index(name)
    shaped = Shaped([(gid, 0, 0, r.tt["hmtx"][name][0])], r.tt["hmtx"][name][0])
    img = Image.new("RGB", (160, 100), "white")
    r.draw(img, 70 - stem_x(name) * size / r.upem, 80, shaped, size, "black")
    return img.convert("L").point(lambda v: 1 if v < 128 else 0)


def pixel_difference(a, b):
    pa, pb = a.load(), b.load()
    w, h = a.size
    return sum(1 for x in range(w) for y in range(h) if pa[x, y] != pb[x, y])


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--font", default=str(ROOT / "fonts" / "ThuravarkCarved-Regular.ttf"))
    args = ap.parse_args()
    font = Path(args.font)
    failures = shaping(font) + geometry(font)
    for f in failures[:40]:
        print(f"{font}: error: {f}")
    if len(failures) > 40:
        print(f"{font}: error: ... and {len(failures) - 40} more")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
