# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Shape every Nordmal form and assert Thuravark Carved renders it rightly.

    .venv/bin/python tools/thuravark-carved/guard.py [--font fonts/ThuravarkCarved-Regular.ttf]
                                            [--thalorna ~/dev/HeroicLands/thalorna | --note FILE]
                                            [--map-note FILE | --fixtures-only]

The forms come from the frontmatter of ``assets/content/Skills/Languages/Nordmal.md``
on the thalorna repository's ``origin/main``: the ``words``, ``affixes`` and
``elements`` forms and every given name and clan name. Each form is written in
Thuravark's code points by thalorna's ``thuravark`` mapping note
(``assets/content/Lore/Scripts/Thuravark_Spelling.md`` on ``origin/main``, or the
file ``--map-note`` names), as a run marked ``map=thuravark`` is, and the result
is shaped. The expected glyph sequence is derived from the spelling by the rules
below, written here and read neither from the font source nor from the mapping:

- a digraph (th dh kh gh ng hl) is one stave, and ngh is n and gh;
- an acute vowel is the vowel and the acute mark, which the face draws as the
  stave again (``a.acute``), and a doubled vowel letter is the stave twice;
- a doubled consonant is two staves, a doubled digraph two digraph staves;
- j, and y before a vowel, is the glide; any other y is the vowel i;
- q is the stave k, and ë is e;
- the space draws nothing, the hyphen-minus is written as nothing, and the full
  stop draws the dash;
- every other punctuation key, c and x draw the box;
- nothing is .notdef.

Fixtures, written through the mapping and shaped too, cover the fillers, the
numerals, the full stop and the empty keys.

The imperial recension's fixtures are typed in the font's code points around a
name written through the mapping: the three diphthong staves; a crowned name,
whose every glyph takes its crowned form between the opened and the closed post;
an open with no close, and a close with no open, which stay bare posts with the
staves beside them unchanged; a crown longer than the font frames; the bound
runes with ``ss01`` on, and the same text unchanged with it off. A rendered
crowned name's rails are checked for a break.

A geometry section asserts the stave design: 31 distinct staves and ten bound
runes, each bound rune the two staves' branches on one stem by the rules of
``tools/thuravark-carved/staves.py``, no horizontal edge in any of them,
numerals taller than the staves, and every pair visibly apart at reading size.
"""

import argparse
import itertools
import subprocess
import sys
from pathlib import Path

import yaml
from fontTools.pens.recordingPen import RecordingPen
from fontTools.ttLib import TTFont
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from mapped import Mapping, MappedRenderer  # noqa: E402
from render import Renderer, Shaped  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent
NOTE = "assets/content/Skills/Languages/Nordmal.md"

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
DIGRAPHS = ("th", "dh", "kh", "gh", "ng", "hl")
VOWELS = "aeiou"
ACUTE = {"á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u"}
NOTHING = {"space"}

FIXTURES = [
    # Every stave of the row from its typed input.
    *[(s, [s]) for s in ROW if s not in ("j",)],
    ("j", ["j"]),
    ("y", ["i"]),
    ("ya", ["j", "a"]),
    ("yu", ["j", "u"]),
    ("bjarn", ["b", "j", "a", "r", "n"]),
    ("ey", ["e", "i"]),
    ("by", ["b", "i"]),
    ("yy", ["i", "i"]),
    # Long vowels: the vowel and the acute mark, or the vowel letter doubled.
    ("á", ["a", "a.acute"]), ("é", ["e", "e.acute"]), ("í", ["i", "i.acute"]), ("ó", ["o", "o.acute"]),
    ("ú", ["u", "u.acute"]), ("Á", ["a", "a.acute"]),
    ("aa", ["a", "a"]), ("ii", ["i", "i"]), ("uu", ["u", "u"]),
    ("rún", ["r", "u", "u.acute", "n"]),
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
    # The hyphen is written as nothing and breaks a digraph.
    ("skald-hringr", ["s", "k", "a", "l", "d", "h", "r", "i", "ng", "r"]),
    ("t-h", ["t", "h"]),
    ("t‐h", ["t", "notdef.box", "h"]),
    # Numerals.
    ("0123456789", [f"num.{i}" for i in range(10)]),
    ("128", ["num.1", "num.2", "num.8"]),
    ("0i0", ["num.0", "i", "num.0"]),
    # The full stop draws the dash, the space draws nothing, and other punctuation draws the box.
    ("rún.", ["r", "u", "u.acute", "n", "period"]),
    ("a b", ["a", "space", "b"]),
    ("a b", ["a", "space", "b"]),
    (",!?;:", ["notdef.box"] * 5),
    ('"\'()', ["notdef.box"] * 4),
    ("“a”", ["notdef.box", "a", "notdef.box"]),
    ("a«b»", ["a", "notdef.box", "b", "notdef.box"]),
    ("<>[]", ["notdef.box"] * 4),
    ("@#$%^&", ["notdef.box"] * 6),
    # No stave: the box, never .notdef; q is k and ë is e.
    ("cqx", ["notdef.box", "k", "notdef.box"]),
    ("ë", ["e"]),
]

# The recension: the diphthong staves, the crown marks and the bound runes, typed in
# the font's own code points around a roman text written through the mapping. Each
# fixture is the text before, the roman text, the text after, the features, and the
# glyphs expected.
AI, AU, OI = "\U000F0128", "\U000F0129", "\U000F012A"
OPEN, CLOSE = "\U000F0150", "\U000F0151"
SS01 = {"ss01": True}
LONGEST = 40  # the most glyphs a crown holds


def crowned(names: list[str]) -> list[str]:
    return ["crown.open.rail", *[n + ".crown" for n in names], "crown.close.rail"]


RECENSION_FIXTURES = [
    # The three staves, each its own character.
    (AI, "", "", {}, ["ai"]), (AU, "", "", {}, ["au"]), (OI, "", "", {}, ["oi"]),
    (AI + AU + OI, "", "", {}, ["ai", "au", "oi"]),
    # A crowned name: every glyph between the marks takes its crowned form.
    (OPEN, "Thauras", CLOSE, {}, crowned(["th", "a", "u", "r", "a", "s"])),
    (OPEN, "Thiland Thauras", CLOSE, {}, crowned(["th", "i", "l", "a", "n", "d", "space", "th", "a", "u", "r", "a", "s"])),
    (OPEN, "Árdavon", CLOSE, {}, crowned(["a", "a.acute", "r", "d", "a", "v", "o", "n"])),
    (OPEN, "128", CLOSE, {}, crowned(["num.1", "num.2", "num.8"])),
    (OPEN, "", CLOSE, {}, crowned([])),
    (OPEN + AI, "", AU + CLOSE, {}, crowned(["ai", "au"])),
    # An open with no close, and a close with no open: a bare post, the staves unchanged.
    (OPEN, "Thauras", "", {}, ["crown.open", "th", "a", "u", "r", "a", "s"]),
    ("", "Thauras", CLOSE, {}, ["th", "a", "u", "r", "a", "s", "crown.close"]),
    # A character with no stave breaks the crown: both marks stay bare.
    (OPEN, "a,b", CLOSE, {}, ["crown.open", "a", "notdef.box", "b", "crown.close"]),
    # Two crowns in one run, and an open inside a crown, which opens the inner one.
    (OPEN, "a", CLOSE + OPEN, {}, crowned(["a"]) + ["crown.open"]),
    (OPEN + AI + OPEN, "", AU + CLOSE, {}, ["crown.open", "ai"] + crowned(["au"])),
    # The longest crown the font frames, and one glyph more, which it leaves bare.
    (OPEN + AI * (LONGEST - 1), "", CLOSE, {}, crowned(["ai"] * (LONGEST - 1))),
    (OPEN + AI * LONGEST, "", CLOSE, {}, ["crown.open"] + ["ai"] * LONGEST + ["crown.close"]),
    # The bound runes, with ss01 on; the same text with it off is the staves as written.
    ("", "en el ar al ma za ka ur lm lth", "", SS01,
     ["e_n", "space", "e_l", "space", "a_r", "space", "a_l", "space", "m_a", "space", "z_a", "space", "k_a", "space",
      "u_r", "space", "l_m", "space", "l_th"]),
    ("", "en el ar al ma za ka ur lm lth", "", {},
     ["e", "n", "space", "e", "l", "space", "a", "r", "space", "a", "l", "space", "m", "a", "space", "z", "a", "space",
      "k", "a", "space", "u", "r", "space", "l", "m", "space", "l", "th"]),
    ("", "Marendas", "", SS01, ["m_a", "r", "e_n", "d", "a", "s"]),
    ("", "Marendas", "", {}, ["m", "a", "r", "e", "n", "d", "a", "s"]),
    ("", "Thelvaralon", "", SS01, ["th", "e_l", "v", "a_r", "a_l", "o", "n"]),
    # A bound rune inside a crown takes its crowned form too.
    (OPEN, "Marendas", CLOSE, SS01, crowned(["m_a", "r", "e_n", "d", "a", "s"])),
]


def fixture_texts() -> list[str]:
    """Every roman text the fixtures write through the mapping."""
    return [text for text, _ in FIXTURES] + [roman for _, roman, _, _, _ in RECENSION_FIXTURES if roman]


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
            out += [ACUTE[ch], ACUTE[ch] + ".acute"]
            i += 1
            continue
        if ch == "y":
            out.append("j" if i + 1 < len(s) and s[i + 1] in VOWELS + "áéíóú" else "i")
            i += 1
            continue
        if ch == "-":
            pass
        elif ch == " ":
            out.append("space")
        elif ch == ".":
            out.append("period")
        elif ch == "q":
            out.append("k")
        elif ch == "ë":
            out.append("e")
        elif ch in "cx":
            out.append("notdef.box")
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
            out.append("notdef.box")
        i += 1
    return out


def shaping(font: Path, forms: list[str], mapping: Mapping | None = None) -> list[str]:
    r = MappedRenderer(Renderer(font), mapping or Mapping.offline("thuravark-carved"))
    r.prepare(forms + fixture_texts())
    failures = []
    digraphs = long_vowels = doubled = 0
    for form in forms:
        got = r.glyph_names(form)
        want = expected_glyphs(form)
        digraphs += sum(1 for g in want if g in DIGRAPHS)
        long_vowels += sum(1 for a, b in zip(want, want[1:]) if (a == b or b == a + ".acute") and a in VOWELS)
        doubled += sum(1 for a, b in zip(want, want[1:]) if a == b and a not in VOWELS)
        if ".notdef" in got or "notdef.box" in got:
            failures.append(f"{form}: .notdef or the box in {got}")
        elif got != want:
            failures.append(f"{form}: shaped {got}, expected {want}")
    for text, want in FIXTURES:
        got = r.glyph_names(text)
        if got != want:
            failures.append(f"{text!r}: shaped {got}, expected {want}")
    for before, roman, after, features, want in RECENSION_FIXTURES:
        text = before + (r.mapping.one(roman) if roman else "") + after
        got = [r.order[g[0]] for g in r.renderer.shape(text, features).glyphs]
        if got != want:
            failures.append(f"{before!r} {roman!r} {after!r} {features}: shaped {got}, expected {want}")
    failures += frame_problems(r.renderer, r.mapping)
    print(
        f"{font}: {len(forms)} forms shaped, {digraphs} digraph staves, {long_vowels} doubled "
        f"vowels and {doubled} doubled consonants expected, {len(FIXTURES) + len(RECENSION_FIXTURES)} fixtures, "
        f"{len(failures)} failures"
    )
    return failures


def frame_problems(r: Renderer, mapping: Mapping) -> list[str]:
    """A rendered crowned name's rails run unbroken from post to post, and an open with
    no close draws nothing but its post."""
    problems = []
    size = 48
    name = mapping.one("Thiland Thauras")
    for label, text, framed in (("crowned", OPEN + name + CLOSE, True), ("unclosed", OPEN + name, False)):
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
    ap.add_argument("--thalorna", default=str(Path.home() / "dev/HeroicLands/thalorna"))
    ap.add_argument("--note", help="read the language note from this file instead of git")
    ap.add_argument("--map-note", help="read the thuravark mapping note from this file instead of git")
    ap.add_argument("--fixtures-only", action="store_true",
                    help="shape the fixtures alone, written as tools/mapped.json records them")
    args = ap.parse_args()
    if args.fixtures_only:
        forms, mapping = [], Mapping.offline("thuravark-carved")
    else:
        forms = lexicon_forms(Path(args.thalorna), Path(args.note) if args.note else None)
        mapping = Mapping("thuravark", thalorna=Path(args.thalorna), note=args.map_note, face="thuravark-carved")
    font = Path(args.font)
    failures = shaping(font, forms, mapping) + geometry(font)
    for f in failures[:40]:
        print(f"{font}: error: {f}")
    if len(failures) > 40:
        print(f"{font}: error: ... and {len(failures) - 40} more")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
