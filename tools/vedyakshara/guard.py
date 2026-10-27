# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Shape Vedyakshara Classical's fixtures and assert the font draws each one rightly.

    .venv/bin/python tools/vedyakshara/guard.py [--font fonts/VedyaksharaClassical-Regular.ttf]

What a sequence of code points must shape to follows from them by the face's rules
taken in order (``drawn``): _pa_ and the soft dot are _fa_; a fused pair with the cut
between is its fused sign, the leftmost first; _ra_ with the cut is its half form
before a consonant and its final form otherwise; a sign, the cut and _ra_ are the
sign's r-foot form; a sign with the cut is its half form before a consonant and its
final form otherwise; after a sign, _ai_ is the _e_ and _i_ flags and _au_ the _o_ and
_u_ hooks; and a vowel sign, the cut or the soft dot after anything that cannot carry
it is the box. A hook is compared by its kind, since the neck it takes is the sign's
(``check_font.py`` checks the necks).

Each fixture in ``fixtures.json`` is a sequence of Vedyakshara's glyph codes
(``tools/codes/vedyakshara.json``), with ``U+0020`` for the space, and the glyphs it is
drawn with. The guard asserts that ``drawn`` gives those glyphs and that the font,
shaping the sequence left to right, gives them too.
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import codes  # noqa: E402
from render import Renderer  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent
HERE = Path(__file__).resolve().parent
SCRIPT = "vedyakshara"
BOX = "notdef.box"
SPACE = " "

ENC = json.loads((HERE / "encoding.json").read_text(encoding="utf-8"))
NAME_OF = {chr(int(g["codepoint"][2:], 16)): g["glyph"] for g in ENC["glyphs"]}
CONSONANTS = [g["glyph"] for g in ENC["glyphs"] if g["kind"] == "consonant"]
SIGNS = {g["glyph"] for g in ENC["glyphs"] if g["kind"] == "vowel sign"}
FUSED = {tuple(f["parts"]): f["glyph"] for f in ENC["fused"]}
C_R = {g for (a, b), g in FUSED.items() if b == "ra"}
BASES = set(CONSONANTS) | {"fa"} | set(FUSED.values())
RFOOT = {b for b in BASES if b != "ra" and b not in C_R and f"{b[:-1]}ra" not in C_R}
STARTS = BASES | {f"{b}.rfoot" for b in RFOOT} | {"ra.half", "ra.final"}  # what a half form stands before
CARRIERS = BASES | {f"{b}.rfoot" for b in RFOOT}  # what carries a vowel sign
SPLIT = {"vs.ai": ["flag.e", "flag.i"], "vs.au": ["hook.o", "hook.u"], "vs.u": ["hook.u"], "vs.o": ["hook.o"]}


def drawn(text: str) -> list[str]:
    """The glyphs, in reading order, that the face draws for a string of code points."""
    g = ["space" if c == SPACE else NAME_OF.get(c, BOX) for c in text]

    def pairs(rule):
        out, i = [], 0
        while i < len(g):
            got = rule(i)
            if got:
                n, new = got
                out.append(new)
                i += n
            else:
                out.append(g[i])
                i += 1
        return out

    g = pairs(lambda i: (2, "fa") if g[i:i + 2] == ["pa", "dot"] else None)
    g = pairs(lambda i: (3, FUSED[(g[i], g[i + 2])]) if i + 2 < len(g) and g[i + 1] == "cut" and (g[i], g[i + 2]) in FUSED else None)
    g = pairs(lambda i: (2, "ra.half" if i + 2 < len(g) and g[i + 2] in STARTS else "ra.final")
              if g[i:i + 2] == ["ra", "cut"] else None)
    g = pairs(lambda i: (3, f"{g[i]}.rfoot") if g[i] in RFOOT and g[i + 1:i + 3] == ["cut", "ra"] else None)
    g = pairs(lambda i: (2, f"{g[i]}.half") if g[i] in BASES and i + 2 < len(g) and g[i + 1] == "cut" and g[i + 2] in STARTS else None)
    g = pairs(lambda i: (2, f"{g[i]}.final") if g[i] in BASES and g[i + 1:i + 2] == ["cut"] else None)
    out = []
    for i, name in enumerate(g):
        if name in SIGNS and i and g[i - 1] in CARRIERS:
            out += SPLIT.get(name, [name])
        elif name in SIGNS | {"cut", "dot"} and i:
            out.append(BOX)
        else:
            out.append(name)
    return out


def plain(names: list[str]) -> list[str]:
    """A hook named by its kind alone: ``hook.u.230`` is ``hook.u``."""
    return [".".join(n.split(".")[:2]) if n.startswith("hook.") else n for n in names]


FIXTURES = [(f["codes"], f["glyphs"]) for f in json.loads((HERE / "fixtures.json").read_text(encoding="utf-8"))["fixtures"]]


def run(font: Path) -> list[str]:
    r = Renderer(font)
    failures = []
    for sequence, want in FIXTURES:
        text = codes.text(SCRIPT, sequence)
        if drawn(text) != want:
            failures.append(f"{sequence}: drawn as {drawn(text)}, expected {want}")
        got = plain(r.glyph_names(text, direction="ltr"))
        if got != want:
            failures.append(f"{sequence}: shaped {got}, expected {want}")
    print(f"{font}: {len(FIXTURES)} fixtures, {len(failures)} failures")
    return failures


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--font", default=str(ROOT / "fonts" / "VedyaksharaClassical-Regular.ttf"))
    args = ap.parse_args()
    failures = run(Path(args.font))
    for f in failures[:40]:
        print(f"{args.font}: error: {f}")
    if len(failures) > 40:
        print(f"{args.font}: error: ... and {len(failures) - 40} more")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
