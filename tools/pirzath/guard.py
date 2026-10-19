# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Shape every Khazari lexicon form and assert the font renders it rightly.

    .venv/bin/python tools/pirzath/guard.py [--font fonts/PirzathCarved-Regular.ttf]
                                         [--thalorna ~/dev/HeroicLands/thalorna | --note FILE]

The forms come from the ``words`` list in the frontmatter of
``assets/content/Skills/Languages/Khazari.md`` on the thalorna repository's
``origin/main``. For each form the expected glyph sequence is derived from the
spelling: a digraph is one ligature glyph, an acute vowel is its vowel followed
by the length mark, a doubled consonant or digraph is the letter once with
the doubling mark, and nothing is .notdef. The shaped sequence must match it
exactly, so a lexicon form shapes with the same glyphs whether or not the font
also types the lost letters. A set of fixtures covers the numerals, the
quotation marks, the marks between words, every doubled letter, and the
seventeen lost letters in every position they occupy.
"""

import argparse
import subprocess
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from render import Renderer  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent
NOTE = "assets/content/Skills/Languages/Khazari.md"

NUMS = [f"num.{i}" for i in range(16)]

# What the owner's rulings say types each letter. The guard owns these tables;
# the font under test is only ever read.
DIGRAPHS = {"th": "t_h", "dh": "d_h", "gh": "g_h", "kh": "k_h"}
ACUTES = {"á": "aacute", "é": "eacute", "í": "iacute", "ó": "oacute", "ú": "uacute"}
LETTERS = {c: c for c in "bdgkptvfzshmnlrcaeiou"}
PUNCT_MAP = {
    "-": "hyphen", ".": "period", ",": "comma", "!": "exclam", "¡": "exclam",
    " ": "space", "\u00a0": "space", "\u2010": "hyphen", "\u2011": "hyphen",
    '"': "quotedbl", "\u201c": "quote.open", "\u201d": "quote.close",
    "«": "quote.open", "»": "quote.close", "[": "quote.open", "]": "quote.close",
    "<": "less", ">": "greater",
}
CONSONANT_NAMES = {
    "p", "b", "f", "v", "m", "t", "d", "t_h", "d_h", "n", "k", "g", "k_h", "g_h", "s", "z", "h",
    "l", "r", "sh", "zh", "ts", "ch", "j", "q", "ng", "ny", "catch", "w", "y", "hl",
}
DOUBLED_DIGRAPHS = {k[0] + k: v for k, v in DIGRAPHS.items()}  # tth, ddh, kkh, ggh

# What the owner's rulings on numerals and quotation marks must shape to.
FIXTURES = [
    ("0123456789", NUMS[:10]),
    ("@#$%^&", NUMS[10:]),
    ("1@", ["num.1", "num.10"]),
    ("girm 10 bep tob 1", ["g", "i", "r", "m", "space", "num.1", "num.0", "space", "b", "e", "p",
                           "space", "t", "o", "b", "space", "num.1"]),
    ("abcdef", ["a", "b", "c", "d", "e", "f"]),
    ('"dalk"', ["quote.open", "d", "a", "l", "k", "quote.close"]),
    ('gaz "dalk" zef', ["g", "a", "z", "space", "quote.open", "d", "a", "l", "k", "quote.close",
                        "space", "z", "e", "f"]),
    ('bant."', ["b", "a", "n", "t", "period", "quote.close"]),
    ("“dalk”", ["quote.open", "d", "a", "l", "k", "quote.close"]),
    ("dalk“", ["d", "a", "l", "k", "quote.open"]),
    ("”dalk", ["quote.close", "d", "a", "l", "k"]),
    ("[dalk]", ["quote.open", "d", "a", "l", "k", "quote.close"]),
    ("gaz [ghulk]", ["g", "a", "z", "space", "quote.open", "g_h", "u", "l", "k", "quote.close"]),
    ("«dalk»", ["quote.open", "d", "a", "l", "k", "quote.close"]),
    ("<<dalk>>", ["quote.open", "d", "a", "l", "k", "quote.close"]),
    ("gaz <<dalk>> zef", ["g", "a", "z", "space", "quote.open", "d", "a", "l", "k", "quote.close",
                          "space", "z", "e", "f"]),
    # gh right before a closing quote, from every input.
    ('"thurágh"', ["quote.open", "t_h", "u", "r", "a", "lengthmark", "g_h", "quote.close"]),
    ("“thurágh”", ["quote.open", "t_h", "u", "r", "a", "lengthmark", "g_h", "quote.close"]),
    ("«thurágh»", ["quote.open", "t_h", "u", "r", "a", "lengthmark", "g_h", "quote.close"]),
    ("<<thurágh>>", ["quote.open", "t_h", "u", "r", "a", "lengthmark", "g_h", "quote.close"]),
    ("?;:", [".notdef", ".notdef", ".notdef"]),
    ("¡ves durám.", ["exclam", "v", "e", "s", "space", "d", "u", "r", "a", "lengthmark", "m", "period"]),
    ("!ves durám.", ["exclam", "v", "e", "s", "space", "d", "u", "r", "a", "lengthmark", "m", "period"]),
    # Doubling: every consonant and every digraph, then the lexicon's own.
    *[(f"a{c}{c}a", ["a", c, "doubling", "a"]) for c in "bdgkptvfzshmnlr"],
    *[(f"a{d[0]}{d}a", ["a", DIGRAPHS[d], "doubling", "a"]) for d in DIGRAPHS],
    ("dullák", ["d", "u", "l", "doubling", "a", "lengthmark", "k"]),
    ("putthák", ["p", "u", "t_h", "doubling", "a", "lengthmark", "k"]),
    ("gummáth", ["g", "u", "m", "doubling", "a", "lengthmark", "t_h"]),
    ("Khubbán", ["k_h", "u", "b", "doubling", "a", "lengthmark", "n"]),
    ("dalk. bant! ramk, tanv?", ["d", "a", "l", "k", "period", "space", "b", "a", "n", "t",
                                  "exclam", "space", "r", "a", "m", "k", "comma", "space",
                                  "t", "a", "n", "v", ".notdef"]),
]


# The seventeen lost letters. Each is typed in the position it can occupy:
# initial, medial and final. A final y is the vowel i, so y has no final form.
LOST_SINGLE = [
    ("sh", "sh"), ("zh", "zh"), ("ch", "ch"), ("j", "j"), ("ts", "ts"), ("q", "q"),
    ("ng", "ng"), ("ny", "ny"), ("hl", "hl"), ("w", "w"), ("'", "catch"), ("\u2019", "catch"),
]
LOST_PAIRS = ["ai", "au", "ei", "oi", "ou"]
ACUTE_OF = {"a": "á", "e": "é", "i": "í", "o": "ó", "u": "ú"}

LOST_FIXTURES = [
    *[(f"{k}a", [g, "a"]) for k, g in LOST_SINGLE],
    *[(f"a{k}a", ["a", g, "a"]) for k, g in LOST_SINGLE],
    *[(f"a{k}", ["a", g]) for k, g in LOST_SINGLE],
    ("ya", ["y", "a"]),
    ("aya", ["a", "y", "a"]),
    ("yub", ["y", "u", "b"]),
    ("kyé", ["k", "y", "e", "lengthmark"]),
    *[(f"{p}b", [p, "b"]) for p in LOST_PAIRS],
    *[(f"b{p}b", ["b", p, "b"]) for p in LOST_PAIRS],
    *[(f"b{p}", ["b", p]) for p in LOST_PAIRS],
    # An acute on either vowel of a pair puts the length mark on the pair.
    *[(f"b{p[0]}{ACUTE_OF[p[1]]}", ["b", p, "lengthmark"]) for p in LOST_PAIRS],
    *[(f"b{ACUTE_OF[p[0]]}{p[1]}", ["b", p, "lengthmark"]) for p in LOST_PAIRS],
    # ngh is n and gh, never ng and h.
    ("zangh", ["z", "a", "n", "g_h"]),
    ("huzangh", ["h", "u", "z", "a", "n", "g_h"]),
    ("anghab", ["a", "n", "g_h", "a", "b"]),
    ("zanga", ["z", "a", "ng", "a"]),
    # A y that is not before a vowel is the vowel i; after a vowel it forms the
    # pair the spelling guide reads alike.
    ("bay", ["b", "ai"]),
    ("bey", ["b", "ei"]),
    ("boy", ["b", "oi"]),
    ("bayb", ["b", "ai", "b"]),
    ("báy", ["b", "ai", "lengthmark"]),
    ("buy", ["b", "u", "i"]),
    ("by", ["b", "i"]),
    ("byb", ["b", "i", "b"]),
    ("y", ["i"]),
    ("Y", ["i"]),
    ("bayab", ["b", "a", "y", "a", "b"]),
    # A doubled lost consonant is the letter once with the doubling mark, from
    # the letter written twice and, for a digraph, from the first letter too.
    *[(f"a{k}{k}a", ["a", g, "doubling", "a"]) for k, g in LOST_SINGLE if len(k) == 1],
    *[(f"a{k}{k}a", ["a", g, "doubling", "a"]) for k, g in LOST_SINGLE if len(k) == 2],
    *[(f"a{k[0]}{k}a", ["a", g, "doubling", "a"]) for k, g in LOST_SINGLE if len(k) == 2],
    ("annghab", ["a", "n", "doubling", "g_h", "a", "b"]),
    # Capitals draw the same letters.
    ("ShaNGa", ["sh", "a", "ng", "a"]),
]


def lexicon_forms(thalorna: Path | None, note: Path | None) -> list[str]:
    if note:
        text = note.read_text(encoding="utf-8")
    else:
        text = subprocess.run(
            ["git", "-C", str(thalorna), "show", f"origin/main:{NOTE}"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout
    body = text.split("\n---\n", 1)[0].lstrip("-\n")
    front = yaml.safe_load(body)
    forms = [w["form"] for w in front["data"]["words"]]
    if not forms:
        raise SystemExit("the words list is empty")
    return forms


def expected_glyphs(form: str) -> list[str]:
    out = []
    i = 0
    s = form.lower()
    while i < len(s):
        three = s[i : i + 3]
        if three in DOUBLED_DIGRAPHS:
            out += [DOUBLED_DIGRAPHS[three], "doubling"]
            i += 3
            continue
        two = s[i : i + 2]
        if two in DIGRAPHS:
            out.append(DIGRAPHS[two])
            i += 2
            continue
        ch = s[i]
        if ch in ACUTES:
            out += [ACUTES[ch][0], "lengthmark"]
        elif ch in LETTERS:
            out.append(LETTERS[ch])
        elif ch in PUNCT_MAP:
            out.append(PUNCT_MAP[ch])
        else:
            out.append(".notdef")
        i += 1
    # A consonant written twice is the letter once with the doubling mark.
    for j in range(1, len(out)):
        if out[j] in CONSONANT_NAMES and out[j] == out[j - 1]:
            out[j] = "doubling"
    return out


def run(font: Path, forms: list[str]) -> list[str]:
    r = Renderer(font)
    failures = []
    digraphs, acutes, doubled = 0, 0, 0
    for form in forms:
        got = r.glyph_names(form)
        want = expected_glyphs(form)
        doubled += "doubling" in want
        if ".notdef" in got or "c" in got:  # c draws as .notdef
            failures.append(f"{form}: .notdef in {got}")
        elif got != want:
            failures.append(f"{form}: shaped {got}, expected {want}")
        digraphs += sum(1 for g in want if g in DIGRAPHS.values())
        acutes += want.count("lengthmark")
    for text, want in FIXTURES + LOST_FIXTURES:
        got = r.glyph_names(text)
        if got != want:
            failures.append(f"{text!r}: shaped {got}, expected {want}")
    print(
        f"{font}: {len(forms)} forms shaped, {digraphs} digraphs, {acutes} long vowels and "
        f"{doubled} doubled forms expected, {len(FIXTURES) + len(LOST_FIXTURES)} fixtures, {len(failures)} failures"
    )
    return failures


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--font", default=str(ROOT / "fonts" / "PirzathCarved-Regular.ttf"))
    ap.add_argument("--thalorna", default=str(Path.home() / "dev/HeroicLands/thalorna"))
    ap.add_argument("--note", help="read the language note from this file instead of git")
    args = ap.parse_args()
    forms = lexicon_forms(Path(args.thalorna), Path(args.note) if args.note else None)
    failures = run(Path(args.font), forms)
    for f in failures[:40]:
        print(f"{args.font}: error: {f}")
    if len(failures) > 40:
        print(f"{args.font}: error: ... and {len(failures) - 40} more")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
