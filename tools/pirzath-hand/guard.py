# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Shape every Khazari lexicon form in the hand, lifted and joined, and assert the result.

    .venv/bin/python tools/pirzath-hand/guard.py [--font fonts/PirzathHand-Regular.ttf]
                                              [--thalorna ~/dev/HeroicLands/thalorna | --note FILE]

The hand types exactly as the carved face does, so the lexicon, the expected
spelling of each form and the carved face's fixtures (numerals, quotation
marks, the marks between words, doubling and the seventeen lost letters) come
from ``tools/pirzath/guard.py`` and must shape here the same way. The hand
draws a long vowel and a doubled consonant as one glyph each, so the carved
sequence ``vowel, lengthmark`` is the long-vowel glyph and ``consonant,
doubling`` is the doubled glyph (``p_p``, ``t_h_t_h``). A length mark left on a
vowel pair stays a separate mark above the pair.

The hand adds the joined look. With ``ss01`` on, every form must shape to the
same letters, each joining letter in the form that its neighbours call for:
``.init`` (a long exit) when the next letter, skipping marks, also joins,
``.fina`` (a long entry) when the previous one does, ``.medi`` when both do,
and the plain letter, short at both ends, when neither does; nothing else
changes. The hand's own fixtures cover the joined look across the length mark
of a pair, the marks between words, numerals and quotation marks breaking the
line, ``¡`` and the lost letters joined, the default-ignorable characters, and
the position of the length mark above a pair.
"""

import argparse
import importlib.util
import sys
from pathlib import Path

from fontTools.pens.boundsPen import BoundsPen

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from render import Renderer  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent


def _carved_guard():
    spec = importlib.util.spec_from_file_location("pirzath_guard", ROOT / "tools" / "pirzath" / "guard.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CARVED = _carved_guard()

LETTERS = [
    "p", "b", "f", "v", "m", "t", "d", "t_h", "d_h", "n", "k", "g", "k_h", "g_h", "s", "z", "h", "l", "r",
    "sh", "zh", "ts", "ch", "j", "q", "ng", "ny", "catch", "w", "y", "hl",
]
VOWELS = {"a": "aacute", "e": "eacute", "i": "iacute", "o": "oacute", "u": "uacute"}
PAIRS = ["ai", "au", "ei", "oi", "ou"]
JOINING = {*LETTERS, *(f"{c}_{c}" for c in LETTERS), *VOWELS, *VOWELS.values(), *PAIRS}
MARKS = {"lengthmark"}
EMPTY = {"ignorable", "ignorable.sub"}
SS01 = {"ss01": True}
C = "+"  # in a fixture: the letter before joins the next letter


def form(g: str, entry: bool, exit_: bool) -> str:
    """The joined form of a joining letter with a long entry and/or a long exit."""
    return g + {(False, True): ".init", (True, True): ".medi", (True, False): ".fina"}.get((entry, exit_), "")


def joined(glyphs: list[str]) -> list[str]:
    """The glyphs in their joined forms: each joining letter takes a long exit when the next
    non-mark glyph joins and a long entry when the previous one does."""
    out = []
    for i, g in enumerate(glyphs):
        if g not in JOINING:
            out.append(g)
            continue
        nxt = next((h for h in glyphs[i + 1:] if h not in MARKS), None)
        prv = next((h for h in reversed(glyphs[:i]) if h not in MARKS), None)
        out.append(form(g, prv in JOINING, nxt in JOINING))
    return out


def collapse(glyphs: list[str]) -> list[str]:
    """The hand's glyphs for a carved sequence or fixture: a vowel and its length mark are the long-vowel
    glyph, a consonant and its doubling mark are the doubled glyph, and a join token stays where it is."""
    out: list[str] = []
    for g in glyphs:
        if g in ("lengthmark", "doubling"):
            k = max(i for i, h in enumerate(out) if h != C)
            if g == "doubling":
                out[k] = f"{out[k]}_{out[k]}"
            elif out[k] in VOWELS:
                out[k] = VOWELS[out[k]]
            else:
                out.append(g)
        else:
            out.append(g)
    return out


def spelled(fixture: list[str]) -> list[str]:
    """A fixture's joined glyphs: a letter followed by C takes a long exit, and the next letter
    after it, skipping marks, a long entry."""
    out, entry = [], False
    for i, g in enumerate(fixture):
        if g == C:
            continue
        if g in MARKS or g not in JOINING:
            out.append(g)
            if g not in MARKS:
                entry = False
            continue
        exit_ = i + 1 < len(fixture) and fixture[i + 1] == C
        out.append(form(g, entry, exit_))
        entry = exit_
    return out


# The joined look, spelled out: C marks each join. The carved spelling is written as the carved face
# shapes it, with a separate length mark and doubling mark, and collapse() turns it into the hand's glyphs.
SS01_CARVED = [
    ("dalk", ["d", C, "a", C, "l", C, "k"]),
    ("dulák", ["d", C, "u", C, "l", C, "a", C, "lengthmark", "k"]),
    ("dullák", ["d", C, "u", C, "l", C, "doubling", "a", C, "lengthmark", "k"]),
    ("putthák", ["p", C, "u", C, "t_h", C, "doubling", "a", C, "lengthmark", "k"]),
    ("Dalk-thumár", ["d", C, "a", C, "l", C, "k", "hyphen", "t_h", C, "u", C, "m", C, "a", C, "lengthmark", "r"]),
    ("gaz dalk.", ["g", C, "a", C, "z", "space", "d", C, "a", C, "l", C, "k", "period"]),
    ("gaz.dalk", ["g", C, "a", C, "z", "period", "d", C, "a", C, "l", C, "k"]),
    ("dalk, bant!", ["d", C, "a", C, "l", C, "k", "comma", "space", "b", C, "a", C, "n", C, "t", "exclam"]),
    ("¡ves durám.", ["exclam", "v", C, "e", C, "s", "space", "d", C, "u", C, "r", C, "a", C, "lengthmark", "m",
                     "period"]),
    ("!ves", ["exclam", "v", C, "e", C, "s"]),
    ('"dalk"', ["quote.open", "d", C, "a", C, "l", C, "k", "quote.close"]),
    ("«thurágh»", ["quote.open", "t_h", C, "u", C, "r", C, "a", C, "lengthmark", "g_h", "quote.close"]),
    ("girm 10 bep", ["g", C, "i", C, "r", C, "m", "space", "num.1", "num.0", "space", "b", C, "e", C, "p"]),
    ("dalk1", ["d", C, "a", C, "l", C, "k", "num.1"]),
    ("tanvc", ["t", C, "a", C, "n", C, "v", "c"]),
    ("shalmai", ["sh", C, "a", C, "l", C, "m", C, "ai"]),
    ("jorqen", ["j", C, "o", C, "r", C, "q", C, "e", C, "n"]),
    ("ya'ath", ["y", C, "a", C, "catch", C, "a", C, "t_h"]),
    ("hlanoi", ["hl", C, "a", C, "n", C, "oi"]),
    ("tsaleik", ["ts", C, "a", C, "l", C, "ei", C, "k"]),
    ("nyolwen", ["ny", C, "o", C, "l", C, "w", C, "e", C, "n"]),
    ("zhoulin", ["zh", C, "ou", C, "l", C, "i", C, "n"]),
    ("chembai", ["ch", C, "e", C, "m", C, "b", C, "ai"]),
    ("ngathu", ["ng", C, "a", C, "t_h", C, "u"]),
    ("báy", ["b", C, "ai", "lengthmark"]),
    ("báyk", ["b", C, "ai", C, "lengthmark", "k"]),
    ("annghab", ["a", C, "n", C, "doubling", "g_h", C, "a", C, "b"]),
    ("akka", ["a", C, "k", C, "doubling", "a"]),
]
SS01_FIXTURES = [(text, collapse(fixture)) for text, fixture in SS01_CARVED]

# Mark positions: (text, index of the mark in the lifted glyphs, index of its base). A length mark
# on a vowel pair is the one mark the hand still draws apart from its base.
MARK_FIXTURES = [
    ("bái", 2, 1),
    ("báy", 2, 1),
    ("báu", 2, 1),
]


def mark_failures(r: Renderer) -> list[str]:
    failures = []
    for text, mi, bi in MARK_FIXTURES:
        shaped = r.shape(text)
        gid_m, mx, my, madv = shaped.glyphs[mi]
        gid_b, bx, _, badv = shaped.glyphs[bi]
        name = r.order[gid_m]
        pen = BoundsPen(r.tt.getGlyphSet())
        r.tt.getGlyphSet()[name].draw(pen)
        x0, y0, x1, y1 = pen.bounds
        lo = my + y0
        cx = mx + (x0 + x1) / 2
        if name != "lengthmark":
            failures.append(f"{text!r}: glyph {mi} is {name}, not the length mark")
        if madv != 0:
            failures.append(f"{text!r}: {name} has an advance of {madv}")
        if lo < 300:
            failures.append(f"{text!r}: {name} is not above its pair (its ink reaches down to {lo})")
        if not (bx - 40 <= cx <= bx + badv + 80):
            failures.append(f"{text!r}: {name} is not seated on {r.order[gid_b]} (centre {cx:.0f}, base {bx}..{bx + badv})")
    return failures


# The default-ignorable characters draw nothing and leave the letters round them alone.
IGNORABLE_FIXTURES = ["da\u200bk", "da\u200dk", "d\u2066a\u2069k", "\ufeffdalk"]


def ignorable_failures(r: Renderer) -> list[str]:
    failures = []
    for text in IGNORABLE_FIXTURES:
        plain = "".join(ch for ch in text if not (0x200B <= ord(ch) <= 0x200F or 0x2066 <= ord(ch) <= 0x2069
                                                   or ord(ch) == 0xFEFF))
        for feats in (None, SS01):
            shaped = r.shape(text, feats)
            names = [r.order[g[0]] for g in shaped.glyphs]
            if any(g[3] for n, g in zip(names, shaped.glyphs) if n in EMPTY):
                failures.append(f"{text!r}: an ignorable has an advance")
            if "space" in names or ".notdef" in names:
                failures.append(f"{text!r}: shaped {names}, which draws a space or .notdef")
            kept = [n for n in names if n not in EMPTY]
            bare = [r.order[g[0]] for g in r.shape(plain, feats).glyphs]
            if feats is None and kept != bare:
                failures.append(f"{text!r}: shaped {kept}, expected {bare}")
    return failures


def run(font: Path, forms: list[str]) -> list[str]:
    r = Renderer(font)
    failures = []
    digraphs = acutes = doubled = 0
    for form in forms:
        carved = CARVED.expected_glyphs(form)
        want = collapse(carved)
        got = r.glyph_names(form)
        doubled += "doubling" in carved
        if ".notdef" in got or "c" in got:
            failures.append(f"{form}: .notdef in {got}")
        elif got != want:
            failures.append(f"{form}: shaped {got}, expected {want}")
        got_j = [r.order[g[0]] for g in r.shape(form, SS01).glyphs]
        if got_j != joined(want):
            failures.append(f"{form} (ss01): shaped {got_j}, expected {joined(want)}")
        digraphs += sum(1 for g in carved if g in CARVED.DIGRAPHS.values())
        acutes += carved.count("lengthmark")
    carved_fixtures = CARVED.FIXTURES + CARVED.LOST_FIXTURES
    for text, want in carved_fixtures:
        want = collapse(want)
        got = r.glyph_names(text)
        if got != want:
            failures.append(f"{text!r}: shaped {got}, expected {want}")
        got_j = [r.order[g[0]] for g in r.shape(text, SS01).glyphs]
        if got_j != joined(want):
            failures.append(f"{text!r} (ss01): shaped {got_j}, expected {joined(want)}")
    for text, fixture in SS01_FIXTURES:
        want = spelled(fixture)
        got = [r.order[g[0]] for g in r.shape(text, SS01).glyphs]
        if got != want:
            failures.append(f"{text!r} (ss01): shaped {got}, expected {want}")
        lifted = [g for g in fixture if g != C]
        if r.glyph_names(text) != lifted:
            failures.append(f"{text!r}: shaped {r.glyph_names(text)}, expected {lifted}")
    failures += mark_failures(r)
    failures += ignorable_failures(r)
    total = len(carved_fixtures) + len(SS01_FIXTURES) + len(MARK_FIXTURES) + len(IGNORABLE_FIXTURES)
    print(
        f"{font}: {len(forms)} forms shaped lifted and joined, {digraphs} digraphs, {acutes} long vowels and "
        f"{doubled} doubled forms expected, {total} fixtures, {len(failures)} failures"
    )
    return failures


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--font", default=str(ROOT / "fonts" / "PirzathHand-Regular.ttf"))
    ap.add_argument("--thalorna", default=str(Path.home() / "dev/HeroicLands/thalorna"))
    ap.add_argument("--note", help="read the language note from this file instead of git")
    args = ap.parse_args()
    forms = CARVED.lexicon_forms(Path(args.thalorna), Path(args.note) if args.note else None)
    failures = run(Path(args.font), forms)
    for f in failures[:40]:
        print(f"{args.font}: error: {f}")
    if len(failures) > 40:
        print(f"{args.font}: error: ... and {len(failures) - 40} more")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
