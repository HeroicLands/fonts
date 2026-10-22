# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Draw the staves of the imperial recension into the Thuravark Carved source.

    .venv/bin/python tools/thuravark-carved/staves.py [--ufo sources/ThuravarkCarved.ufo] [--check]

The three diphthong staves, the ten bound runes and the two crown marks are drawn
from the stave system's own constants and written into the UFO, run by hand after
a change to the tables here; ``--check`` draws them afresh and reports any glyph
of the source that differs. The twenty-eight staves of the row are the settled
source and are not written, but ``--check`` draws them too and reports how far
the construction here stands from each, as a measure of the construction.

**The construction.** In the design space a stem is 740 units tall and 85 wide,
and every stroke, stem or branch, is one tapered groove: a parallel-sided cut
whose two ends come to a point 59 units long. A long branch runs from one end of
the stem to the other level at slope 2.73; a half branch runs between the middle
and one end at slope 0.86. The stem and its branches are united into one outline,
scaled by the face's factor (``tools/vertical.py``), rounded to units, and stood
at the face's sidebearing with the advance the spacing rule gives.

**A bound rune** is the two staves' branches on one stem. The system allows it
when the pair shares no branch, the union has at most four, no more than two
leave the stem at one level, and the set matches no stave and no other bound
rune. ``tools/thuravark-carved/guard.py`` asserts the same of the built font.

**The crown marks** are the two posts of the crowned frame: a square-ended cut
of half the stem's weight, standing a stroke below the baseline and a stroke
above the staves' tops, which ``crown.py`` joins with rails at build time.
"""

import argparse
import math
import sys
from pathlib import Path

import pathops
from fontTools.misc import plistlib

ROOT = Path(__file__).resolve().parent.parent.parent
UFO = ROOT / "sources" / "ThuravarkCarved.ufo"

# The design space.
STEM = 740.0  # the stem's height
WEIGHT = 85.0  # the width of every groove
TIP = 59.0  # the length of a groove's pointed end
LONG_SLOPE = 2.73  # a branch spanning the whole stem
HALF_SLOPE = 0.86  # a branch spanning half of it
SCALE = 0.99  # the face's factor, tools/vertical.py
SIDEBEARING = 34  # tools/respace.py
LEVEL = {"0": 0.0, "M": STEM / 2, "T": STEM}

# The frame's measures, in font units after scaling: the posts and rails are half
# a stroke thick, and stand one stroke clear of the staves above and below.
STROKE = 84
FRAME_WEIGHT = STROKE // 2  # 42
STAVE_TOP = 733
FRAME_TOP = STAVE_TOP + STROKE + FRAME_WEIGHT  # 859
FRAME_BOTTOM = -STROKE - FRAME_WEIGHT  # -126
POST_ADVANCE = SIDEBEARING + FRAME_WEIGHT + 50  # a post, its sidebearing, and a stroke of room before the first stave

# Each stave's branches: the side a branch leaves the stem on (F forward, B back),
# the level it leaves from and the level it ends at (T top, M middle, 0 foot).
BRANCHES = {
    "a": "F0T",
    "e": "FTM BTM",
    "i": "",
    "o": "FTM F0M BTM B0M",
    "u": "B0T",
    "p": "FT0 BT0",
    "b": "FT0 BT0 B0M",
    "f": "FT0 BT0 FMT",
    "v": "FT0 BT0 B0M FMT",
    "t": "F0T B0T",
    "d": "F0T B0T BTM",
    "th": "F0T B0T FMT",
    "dh": "F0T B0T BTM FMT",
    "k": "FTM F0M",
    "g": "FTM F0M BM0",
    "kh": "FTM F0M FMT",
    "gh": "FTM F0M BM0 FMT",
    "s": "FTM BM0",
    "z": "FT0 B0T",
    "h": "BM0 FMT",
    "l": "FM0",
    "r": "BTM B0M",
    "hl": "FM0 FMT",
    "m": "FT0 BM0",
    "n": "F0T BMT",
    "ng": "FTM F0M FMT FM0",
    "j": "FMT",
    "w": "BMT",
    # The imperial recension's diphthong staves: the first vowel's stave with the
    # off-glide's branch. The i-glide is the glide's own branch, a half branch
    # rising forward from the middle; the u-glide is u's branch at half length,
    # rising back from the foot. o's diamond keeps its back half, so that the
    # forward side is free for the glide.
    "ai": "F0T FMT",
    "au": "F0T B0M",
    "oi": "BTM B0M FMT",
}

# The staves of the row, in the inventory's order, and the recension's three.
ROW = "a e i o u p b f v t d th dh k g kh gh s z h l r hl m n ng j w".split()
DIPHTHONGS = {"ai": 0xF0128, "au": 0xF0129, "oi": 0xF012A}

# The bound runes: each pair of staves on one stem, by its glyph name. ss01 sets them.
BOUND = {
    "e_n": ("e", "n"),
    "e_l": ("e", "l"),
    "a_r": ("a", "r"),
    "a_l": ("a", "l"),
    "m_a": ("m", "a"),
    "z_a": ("z", "a"),
    "k_a": ("k", "a"),
    "u_r": ("u", "r"),
    "l_m": ("l", "m"),
    "l_th": ("l", "th"),
}

CROWN = {"crown.open": 0xF0150, "crown.close": 0xF0151}


def bound_branches(name: str) -> str:
    """The branch set of a bound rune, and the rule that allows it."""
    first, second = BOUND[name]
    a, b = set(BRANCHES[first].split()), set(BRANCHES[second].split())
    if a & b:
        raise ValueError(f"{name}: {first} and {second} share a branch")
    joined = a | b
    if len(joined) > 4:
        raise ValueError(f"{name}: more than four branches")
    for level in "0MT":
        if sum(1 for br in joined if br[1] == level) > 2:
            raise ValueError(f"{name}: three branches leave the stem at one level")
    return " ".join(sorted(joined))


def all_branch_sets() -> dict[str, frozenset]:
    sets = {n: frozenset(s.split()) for n, s in BRANCHES.items()}
    for name in BOUND:
        sets[name] = frozenset(bound_branches(name).split())
    seen: dict[frozenset, str] = {}
    for name, s in sets.items():
        if s in seen:
            raise ValueError(f"{name} and {seen[s]} have the same branches")
        seen[s] = name
    return sets


# --- drawing ---------------------------------------------------------------------


def groove(p0, p1):
    """One tapered groove from p0 to p1, both ends pointed."""
    (x0, y0), (x1, y1) = p0, p1
    dx, dy = x1 - x0, y1 - y0
    length = math.hypot(dx, dy)
    ux, uy = dx / length, dy / length
    nx, ny = -uy, ux
    h = WEIGHT / 2
    pts = [
        (x0, y0),
        (x0 + TIP * ux + h * nx, y0 + TIP * uy + h * ny),
        (x1 - TIP * ux + h * nx, y1 - TIP * uy + h * ny),
        (x1, y1),
        (x1 - TIP * ux - h * nx, y1 - TIP * uy - h * ny),
        (x0 + TIP * ux - h * nx, y0 + TIP * uy - h * ny),
    ]
    path = pathops.Path()
    path.moveTo(*pts[0])
    for q in pts[1:]:
        path.lineTo(*q)
    path.close()
    return path


def branch(spec: str):
    side, leave, end = spec[0], spec[1], spec[2]
    y0, y1 = LEVEL[leave], LEVEL[end]
    span = abs(y1 - y0)
    run = span / (LONG_SLOPE if span == STEM else HALF_SLOPE)
    sign = 1 if side == "F" else -1
    return groove((0.0, y0), (sign * run, y1))


def stave(branches: str):
    """The stave's contours, each a list of integer points, and its advance.

    Outer contours run counter-clockwise and holes clockwise, as the source's do.
    """
    paths = [groove((0.0, 0.0), (0.0, STEM))] + [branch(b) for b in branches.split()]
    union = pathops.Path()
    pathops.union(paths, union.getPen())
    union = union.transform(SCALE, 0, 0, SCALE, 0, 0)
    contours = []
    for contour in union.contours:
        pts = []
        for verb, args in contour:
            if verb in (pathops.PathVerb.MOVE, pathops.PathVerb.LINE):
                pts.append(args[0])
            elif verb != pathops.PathVerb.CLOSE:
                raise ValueError(f"a curve in a stave: {verb}")
        pts = [(round(x), round(y)) for x, y in pts]
        pts = [p for i, p in enumerate(pts) if p != pts[i - 1]]
        contours.append(pts)
    return _stand(contours)


def _stand(contours):
    min_x = min(x for c in contours for x, _ in c)
    max_x = max(x for c in contours for x, _ in c)
    shift = SIDEBEARING - min_x
    contours = [[(x + shift, y) for x, y in c] for c in contours]
    advance = max_x + shift + SIDEBEARING
    out = []
    for c in contours:
        depth = sum(1 for d in contours if d is not c and _contains(d, c[0]))
        if (_area(c) > 0) != (depth % 2 == 0):
            c = c[::-1]
        out.append(c)
    return out, advance


def _area(pts):
    a = 0.0
    for (x1, y1), (x2, y2) in zip(pts, pts[1:] + pts[:1]):
        a += x1 * y2 - x2 * y1
    return a / 2


def _contains(poly, pt):
    x, y = pt
    inside = False
    n = len(poly)
    for k in range(n):
        x1, y1 = poly[k]
        x2, y2 = poly[(k + 1) % n]
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
            inside = not inside
    return inside


def post(name: str):
    """A crown mark: the post alone, square-ended, half a stroke thick, standing from
    the frame's bottom to its top. The open post stands at the sidebearing with a stroke
    of room after it; the close post stands a stroke in, with the sidebearing after."""
    x0 = SIDEBEARING if name == "crown.open" else POST_ADVANCE - SIDEBEARING - FRAME_WEIGHT
    x1 = x0 + FRAME_WEIGHT
    contour = [(x0, FRAME_BOTTOM), (x1, FRAME_BOTTOM), (x1, FRAME_TOP), (x0, FRAME_TOP)]
    return [contour], POST_ADVANCE


def glif(name: str, contours, advance: int, unicode: int | None = None) -> str:
    lines = [
        "<?xml version='1.0' encoding='UTF-8'?>",
        f'<glyph name="{name}" format="2">',
        f'  <advance width="{advance}"/>',
    ]
    if unicode is not None:
        lines.append(f'  <unicode hex="{unicode:04X}"/>')
    lines.append("  <outline>")
    for c in contours:
        lines.append("    <contour>")
        for x, y in c:
            lines.append(f'      <point x="{x}" y="{y}" type="line"/>')
        lines.append("    </contour>")
    lines += ["  </outline>", "</glyph>", ""]
    return "\n".join(lines)


def drawings() -> dict[str, tuple[list, int, int | None]]:
    """Every glyph this tool writes: name -> (contours, advance, code point)."""
    out = {}
    for name, cp in DIPHTHONGS.items():
        contours, advance = stave(BRANCHES[name])
        out[name] = (contours, advance, cp)
    for name in BOUND:
        contours, advance = stave(bound_branches(name))
        out[name] = (contours, advance, None)
    for name, cp in CROWN.items():
        contours, advance = post(name)
        out[name] = (contours, advance, cp)
    return out


def glif_name(name: str) -> str:
    return name.replace(".", "_") + ".glif" if name.startswith(".") else name + ".glif"


def write(ufo: Path) -> list[str]:
    all_branch_sets()
    glyphs = ufo / "glyphs"
    contents = plistlib.loads((glyphs / "contents.plist").read_bytes())
    lib = plistlib.loads((ufo / "lib.plist").read_bytes())
    order = list(lib["public.glyphOrder"])
    written = []
    for name, (contours, advance, cp) in drawings().items():
        file = glif_name(name)
        (glyphs / file).write_text(glif(name, contours, advance, cp), encoding="utf-8")
        contents[name] = file
        if name not in order:
            order.append(name)
        written.append(name)
    lib["public.glyphOrder"] = order
    (glyphs / "contents.plist").write_bytes(plistlib.dumps(contents))
    (ufo / "lib.plist").write_bytes(plistlib.dumps(lib))
    return written


def read_glif(path: Path):
    import xml.etree.ElementTree as ET

    root = ET.parse(path).getroot()
    advance = int(root.find("advance").get("width"))
    contours = [[(int(p.get("x")), int(p.get("y"))) for p in c.findall("point")] for c in root.iter("contour")]
    return contours, advance


def deviation(mine, theirs) -> int | None:
    """The largest distance between the two drawings' points, or None when they differ in count."""
    a = sorted(p for c in mine for p in c)
    b = sorted(p for c in theirs for p in c)
    if len(a) != len(b):
        return None
    return max(max(abs(p[0] - q[0]), abs(p[1] - q[1])) for p, q in zip(a, b))


def check(ufo: Path) -> list[str]:
    all_branch_sets()
    problems = []
    for name, (contours, advance, _) in drawings().items():
        path = ufo / "glyphs" / glif_name(name)
        if not path.exists():
            problems.append(f"{path}: error: {name} is not drawn; run tools/thuravark-carved/staves.py")
            continue
        theirs, their_advance = read_glif(path)
        if deviation(contours, theirs) != 0 or advance != their_advance:
            problems.append(f"{path}: error: {name} differs from its construction; run tools/thuravark-carved/staves.py")
    worst = 0
    for name in ROW:
        theirs, _ = read_glif(ufo / "glyphs" / f"{name}.glif")
        d = deviation(stave(BRANCHES[name])[0], theirs)
        worst = max(worst, d if d is not None else 0)
    print(f"{ufo}: the row's staves stand within {worst} units of the construction")
    return problems


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--ufo", default=str(UFO))
    ap.add_argument("--check", action="store_true", help="report glyphs that differ from their construction")
    args = ap.parse_args()
    ufo = Path(args.ufo)
    if args.check:
        problems = check(ufo)
        for p in problems:
            print(p)
        sys.exit(1 if problems else 0)
    for name in write(ufo):
        print(f"{ufo}: wrote {name}")


if __name__ == "__main__":
    main()
