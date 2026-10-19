# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Shape every Nordmal form and assert Thuravark Runic renders it rightly.

    .venv/bin/python thuravark/src/guard.py [--font thuravark/fonts/ThuravarkRunic-Regular.ttf]
                                            [--thalorna ~/dev/HeroicLands/thalorna | --note FILE]

The forms come from the frontmatter of ``assets/content/Skills/Languages/Nordmal.md``
on the thalorna repository's ``origin/main``: the ``words``, ``affixes`` and
``elements`` forms and every given name and clan name. The expected glyph
sequence is derived from the spelling by the rules below, written here and not
read from the font source:

- a digraph (th dh kh gh ng hl) is one stave, and ngh is n and gh;
- an acute vowel, and a doubled vowel letter, is the stave twice;
- a doubled consonant is two staves, a doubled digraph two digraph staves;
- j, and y before a vowel, is the glide; any other y is the vowel i;
- the space, the hyphen and every punctuation key but the full stop draw nothing;
- nothing is .notdef.

Fixtures cover the fillers, the numerals, the full stop and the empty keys. A
geometry section asserts the stave design: 28 distinct staves, no horizontal
stroke but the full stop, only the two branch slopes, and every pair of staves
visibly apart at reading size.
"""

import argparse
import itertools
import subprocess
import sys
from pathlib import Path

import yaml
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import staves as G  # noqa: E402
from render import Renderer  # noqa: E402

HERE = Path(__file__).resolve().parent.parent
NOTE = "assets/content/Skills/Languages/Nordmal.md"

# The 28 staves, by the glyph name the font gives each.
STAVES = ("a e i o u p b f v t d th dh k g kh gh s z h l r hl m n ng j w").split()
DIGRAPHS = ("th", "dh", "kh", "gh", "ng", "hl")
VOWELS = "aeiou"
ACUTE = {"á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u"}
NOTHING = {"space", "hyphen", "blank"}

FIXTURES = [
    # Every stave from its typed input.
    *[(s, [s]) for s in STAVES if s not in ("j",)],
    ("j", ["j"]),
    ("y", ["i"]),
    ("ya", ["j", "a"]),
    ("yu", ["j", "u"]),
    ("bjarn", ["b", "j", "a", "r", "n"]),
    ("ey", ["e", "i"]),
    ("by", ["b", "i"]),
    ("yy", ["i", "i"]),
    # Long vowels: the stave twice, three ways.
    ("á", ["a", "a"]), ("é", ["e", "e"]), ("í", ["i", "i"]), ("ó", ["o", "o"]), ("ú", ["u", "u"]),
    ("Á", ["a", "a"]),
    ("aa", ["a", "a"]), ("ii", ["i", "i"]), ("uu", ["u", "u"]),
    ("á", ["a", "a"]),
    ("rún", ["r", "u", "u", "n"]),
    # Doubled consonants: two staves.
    ("nn", ["n", "n"]), ("ll", ["l", "l"]), ("tt", ["t", "t"]), ("kk", ["k", "k"]),
    ("rr", ["r", "r"]), ("pp", ["p", "p"]),
    ("tth", ["th", "th"]), ("hhl", ["hl", "hl"]), ("nng", ["ng", "ng"]),
    # Digraphs and the cases that look like them.
    ("ngh", ["n", "gh"]), ("hr", ["h", "r"]), ("hn", ["h", "n"]), ("sh", ["s", "h"]),
    ("th", ["th"]), ("TH", ["th"]), ("Hlarth", ["hl", "a", "r", "th"]),
    # The fillers: staves Nordmal does not write.
    ("dh", ["dh"]), ("kh", ["kh"]), ("gh", ["gh"]), ("z", ["z"]), ("w", ["w"]),
    ("ddh", ["dh", "dh"]), ("kkh", ["kh", "kh"]),
    # The hyphen draws nothing and breaks a ligature.
    ("skald-hringr", ["s", "k", "a", "l", "d", "hyphen", "h", "r", "i", "ng", "r"]),
    ("t-h", ["t", "hyphen", "h"]),
    # Numerals.
    ("0123456789", [f"num.{i}" for i in range(10)]),
    ("128", ["num.1", "num.2", "num.8"]),
    ("0i0", ["num.0", "i", "num.0"]),
    # The full stop draws the dash; the space and other punctuation draw nothing.
    ("rún.", ["r", "u", "u", "n", "period"]),
    ("a b", ["a", "space", "b"]),
    ("a b", ["a", "space", "b"]),
    (",!?;:", ["blank"] * 5),
    ('"\'()', ["blank"] * 4),
    ("“a”", ["blank", "a", "blank"]),
    ("a«b»", ["a", "blank", "b", "blank"]),
    ("<>[]", ["blank"] * 4),
    ("@#$%^&", ["blank"] * 6),
    # No stave: the blank stele, never .notdef.
    ("cqx", ["stele", "stele", "stele"]),
]


def forms_of(front) -> list[str]:
    d = front["data"]
    forms = [w["form"] for w in d["words"]]
    forms += [a["form"] for a in d.get("affixes", [])]
    forms += [e["form"] for e in d.get("elements", [])]
    for group in d["names"]["given"].values():
        forms += group
    forms += d["names"]["clan"]
    return forms


def lexicon_forms(thalorna: Path | None, note: Path | None) -> list[str]:
    if note:
        text = note.read_text(encoding="utf-8")
    else:
        text = subprocess.run(
            ["git", "-C", str(thalorna), "show", f"origin/main:{NOTE}"],
            check=True, capture_output=True, text=True,
        ).stdout
    front = yaml.safe_load(text.split("\n---\n", 1)[0].lstrip("-\n"))
    forms = forms_of(front)
    if not forms:
        raise SystemExit("the forms list is empty")
    return forms


def expected_glyphs(form: str) -> list[str]:
    s = form.lower()
    out: list[str] = []
    i = 0
    while i < len(s):
        ch = s[i]
        if ch in ACUTE:
            out += [ACUTE[ch]] * 2
            i += 1
            continue
        if ch == "y":
            out.append("j" if i + 1 < len(s) and s[i + 1] in VOWELS + "áéíóú" else "i")
            i += 1
            continue
        if ch in "-‐‑":
            out.append("hyphen")
        elif ch == " ":
            out.append("space")
        elif ch == ".":
            out.append("period")
        elif ch in "cqx":
            out.append("stele")
        elif s[i : i + 3] == "nng":
            out += ["ng", "ng"]
            i += 3
            continue
        elif s[i : i + 2] == "ng" and s[i : i + 3] != "ngh":
            out.append("ng")
            i += 2
            continue
        elif s[i : i + 2] in DIGRAPHS and s[i : i + 2] != "ng":
            out.append(s[i : i + 2])
            i += 2
            continue
        elif ch in "abdefghijklmnoprstuvwz":
            out.append(ch)
        else:
            out.append("blank")
        i += 1
    return out


def shaping(font: Path, forms: list[str]) -> list[str]:
    r = Renderer(font)
    failures = []
    digraphs = long_vowels = doubled = 0
    for form in forms:
        got = r.glyph_names(form)
        want = expected_glyphs(form)
        digraphs += sum(1 for g in want if g in DIGRAPHS)
        long_vowels += sum(1 for a, b in zip(want, want[1:]) if a == b and a in VOWELS)
        doubled += sum(1 for a, b in zip(want, want[1:]) if a == b and a not in VOWELS)
        if ".notdef" in got or "stele" in got:
            failures.append(f"{form}: .notdef or stele in {got}")
        elif got != want:
            failures.append(f"{form}: shaped {got}, expected {want}")
    for text, want in FIXTURES:
        got = r.glyph_names(text)
        if got != want:
            failures.append(f"{text!r}: shaped {got}, expected {want}")
    print(
        f"{font}: {len(forms)} forms shaped, {digraphs} digraph staves, {long_vowels} doubled "
        f"vowels and {doubled} doubled consonants expected, {len(FIXTURES)} fixtures, "
        f"{len(failures)} failures"
    )
    return failures


# --- the design -------------------------------------------------------------


def geometry(font: Path) -> list[str]:
    problems = []
    rows = G.STAVE_TABLE
    if len(rows) != 28 or [row[0] for row in rows] != STAVES:
        problems.append(f"the staves are {[row[0] for row in rows]}, expected the 28 of the inventory")
    sets = {}
    for row in rows:
        key = frozenset(row[4].split())
        if key in sets:
            problems.append(f"{row[0]} and {sets[key]} have the same branches")
        sets[key] = row[0]
        for b in row[4].split():
            x1, y1, x2, y2 = G.branch(b)
            if y1 == y2:
                problems.append(f"{row[0]}: branch {b} is horizontal")
            slope = round(abs((y2 - y1) / (x2 - x1)), 2)
            if slope not in (G.LONG_SLOPE, G.HALF_SLOPE):
                problems.append(f"{row[0]}: branch {b} has slope {slope}")
        if len(row[4].split()) > 4:
            problems.append(f"{row[0]} has more than four branches")
    for g in G.STAVES:
        for c in g.cuts:
            if abs(c.y2 - c.y1) < 1 and g.name != "period":
                problems.append(f"{g.name}: a horizontal cut")
    if G.NUM_H <= G.STEM_H:
        problems.append("the numerals are not taller than the staves")
    slopes = {round(abs((c.y2 - c.y1) / (c.x2 - c.x1)), 2)
              for n in G.NUMERALS for c in n.cuts[1:]}
    if slopes & {G.LONG_SLOPE, G.HALF_SLOPE}:
        problems.append(f"a numeral limb has a stave slope: {slopes}")
    # Every pair of staves, and nought against i, differs at reading size.
    r = Renderer(font)
    size = 36
    masks = {}
    for name in G.STAVE_NAMES + ["num.0"]:
        masks[name] = ink(r, name, size)
    worst = []
    for a, b in itertools.combinations(masks, 2):
        diff = pixel_difference(masks[a], masks[b])
        worst.append((diff, a, b))
    worst.sort()
    for diff, a, b in worst:
        if diff < MIN_DIFFERENCE:
            problems.append(f"{a} and {b} differ by only {diff} pixels at {size} px")
    print(f"{font}: {len(masks)} forms, closest pairs at {size} px: "
          + ", ".join(f"{a}/{b} {d}" for d, a, b in worst[:6]))
    return problems


MIN_DIFFERENCE = 20


def ink(r: Renderer, name: str, size: int):
    """The glyph's ink at `size`, with its stem on a fixed column."""
    key = "0" if name == "num.0" else name
    shaped = r.shape(key if name != "j" else "j")
    stem_x = G.GLYPHS[name].cuts[0].x1 * size / r.upem
    img = Image.new("RGB", (160, 100), "white")
    r.draw(img, 60 - stem_x, 80, shaped, size, "black")
    return img.convert("L").point(lambda v: 1 if v < 128 else 0)


def pixel_difference(a, b):
    pa, pb = a.load(), b.load()
    w, h = a.size
    return sum(1 for x in range(w) for y in range(h) if pa[x, y] != pb[x, y])


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--font", default=str(HERE / "fonts" / "ThuravarkRunic-Regular.ttf"))
    ap.add_argument("--thalorna", default=str(Path.home() / "dev/HeroicLands/thalorna"))
    ap.add_argument("--note", help="read the language note from this file instead of git")
    args = ap.parse_args()
    forms = lexicon_forms(Path(args.thalorna), Path(args.note) if args.note else None)
    font = Path(args.font)
    failures = shaping(font, forms) + geometry(font)
    for f in failures[:40]:
        print(f"{font}: error: {f}")
    if len(failures) > 40:
        print(f"{font}: error: ... and {len(failures) - 40} more")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
