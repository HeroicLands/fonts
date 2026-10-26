# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Shape every Khazari lexicon form in the hand and assert the result.

    .venv/bin/python tools/pirzath-hand/guard.py [--font fonts/PirzathHand-Regular.ttf]
                                              [--thalorna ~/dev/HeroicLands/thalorna | --note FILE]
                                              [--encoding FILE | --fixtures-only]

The hand draws the same code points as the carved face, and every form is
written through the same ``pirzath`` encoding, so the lexicon, the expected
spelling of each form and the carved face's fixtures (numerals, quotation
marks, the marks between words, doubling and the seventeen lost letters) come
from ``tools/pirzath/guard.py`` and must shape here the same way. The hand
draws a long vowel and a doubled consonant as one glyph each, so the carved
sequence ``vowel, lengthmark`` is the long-vowel glyph and ``consonant,
doubling`` is the doubled glyph (``p_p``, ``t_h_t_h``). A length mark left on a
vowel pair stays a separate mark above the pair.

The hand is one printed face: every letter is drawn as itself, whatever stands
beside it, and no feature joins letters. The hand's own fixtures cover the marks
between words, numerals and quotation marks, the box, the lost letters, the long
vowels and doubled letters in a word, the default-ignorable characters, and the
position of the length mark above a pair.
"""

import argparse
import importlib.util
import sys
from pathlib import Path

from fontTools.pens.boundsPen import BoundsPen

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from encoded import Encoded, EncodedRenderer  # noqa: E402
from render import Renderer  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent


def _carved_guard():
    spec = importlib.util.spec_from_file_location("pirzath_guard", ROOT / "tools" / "pirzath" / "guard.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CARVED = _carved_guard()

VOWELS = {"a": "aacute", "e": "eacute", "i": "iacute", "o": "oacute", "u": "uacute"}
EMPTY = {"ignorable", "ignorable.sub"}


def collapse(glyphs: list[str]) -> list[str]:
    """The hand's glyphs for a carved sequence or fixture: a vowel and its length mark are the
    long-vowel glyph, a consonant and its doubling mark are the doubled glyph, and the carved
    face's space.dot is the hand's space."""
    out: list[str] = []
    for g in glyphs:
        if g in ("lengthmark", "doubling"):
            k = len(out) - 1
            if g == "doubling":
                out[k] = f"{out[k]}_{out[k]}"
            elif out[k] in VOWELS:
                out[k] = VOWELS[out[k]]
            else:
                out.append(g)
        else:
            out.append("space" if g == "space.dot" else g)
    return out


# The hand's own fixtures, written as the carved face shapes them, with a separate length mark
# and doubling mark; collapse() turns each into the hand's glyphs.
HAND_CARVED = [
    ("dalk", ["d", "a", "l", "k"]),
    ("dulák", ["d", "u", "l", "a", "lengthmark", "k"]),
    ("dullák", ["d", "u", "l", "doubling", "a", "lengthmark", "k"]),
    ("putthák", ["p", "u", "t_h", "doubling", "a", "lengthmark", "k"]),
    ("dalk-thumár", ["d", "a", "l", "k", "hyphen", "t_h", "u", "m", "a", "lengthmark", "r"]),
    ("gaz dalk.", ["g", "a", "z", "space", "d", "a", "l", "k", "period"]),
    ("gaz.dalk", ["g", "a", "z", "period", "d", "a", "l", "k"]),
    ("dalk, bant!", ["d", "a", "l", "k", "comma", "space", "b", "a", "n", "t", "period"]),
    ("¡ves durám.", ["notdef.box", "v", "e", "s", "space", "d", "u", "r", "a", "lengthmark", "m", "period"]),
    ("!ves", ["period", "v", "e", "s"]),
    ('"dalk"', ["notdef.box", "d", "a", "l", "k", "notdef.box"]),
    ("«dalk»", ["quote.open", "d", "a", "l", "k", "quote.close"]),
    ("‹dalk›", ["quote.open", "d", "a", "l", "k", "quote.close"]),
    ("“dalk”", ["notdef.box", "d", "a", "l", "k", "notdef.box"]),
    ("«thurágh»", ["quote.open", "t_h", "u", "r", "a", "lengthmark", "g_h", "quote.close"]),
    ("girm 10 bep", ["g", "i", "r", "m", "space", "num.1", "num.0", "space", "b", "e", "p"]),
    ("dalk1", ["d", "a", "l", "k", "num.1"]),
    ("tanvc", ["t", "a", "n", "v", "notdef.box"]),
    ("shalmai", ["sh", "a", "l", "m", "ai"]),
    ("jorqen", ["j", "o", "r", "q", "e", "n"]),
    ("ya'ath", ["y", "a", "catch", "a", "t_h"]),
    ("hlanoi", ["hl", "a", "n", "oi"]),
    ("tsaleik", ["ts", "a", "l", "ei", "k"]),
    ("nyolwen", ["ny", "o", "l", "w", "e", "n"]),
    ("zhoulin", ["zh", "ou", "l", "i", "n"]),
    ("chembai", ["ch", "e", "m", "b", "ai"]),
    ("ngathu", ["ng", "a", "t_h", "u"]),
    ("báy", ["b", "ai", "lengthmark"]),
    ("báyk", ["b", "ai", "lengthmark", "k"]),
    ("annghab", ["a", "n", "doubling", "g_h", "a", "b"]),
    ("akka", ["a", "k", "doubling", "a"]),
]
HAND_FIXTURES = [(text, collapse(fixture)) for text, fixture in HAND_CARVED]

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


def bare(text: str) -> str:
    """The text without its default-ignorable characters."""
    return "".join(ch for ch in text if not (0x200B <= ord(ch) <= 0x200F or 0x2066 <= ord(ch) <= 0x2069
                                             or ord(ch) == 0xFEFF))


def ignorable_failures(r: Renderer) -> list[str]:
    failures = []
    for text in IGNORABLE_FIXTURES:
        plain = bare(text)
        shaped = r.shape(text)
        names = [r.order[g[0]] for g in shaped.glyphs]
        if any(g[3] for n, g in zip(names, shaped.glyphs) if n in EMPTY):
            failures.append(f"{text!r}: an ignorable has an advance")
        if "space" in names or ".notdef" in names or "notdef.box" in names:
            failures.append(f"{text!r}: shaped {names}, which draws a space, .notdef or the box")
        kept = [n for n in names if n not in EMPTY]
        alone = [r.order[g[0]] for g in r.shape(plain).glyphs]
        if kept != alone:
            failures.append(f"{text!r}: shaped {kept}, expected {alone}")
    return failures


def fixture_texts() -> list[str]:
    """Every roman text the fixtures write through the encoding."""
    return ([t for t, _ in CARVED.FIXTURES + CARVED.LOST_FIXTURES + HAND_FIXTURES]
            + [t for t, _, _ in MARK_FIXTURES] + IGNORABLE_FIXTURES + [bare(t) for t in IGNORABLE_FIXTURES])


def run(font: Path, forms: list[str], encoded: Encoded | None = None) -> list[str]:
    r = EncodedRenderer(Renderer(font), encoded or Encoded("pirzath-hand"))
    failures = []
    digraphs = acutes = doubled = 0
    for form in forms:
        carved = CARVED.expected_glyphs(form)
        want = collapse(carved)
        got = r.glyph_names(form)
        doubled += "doubling" in carved
        if ".notdef" in got or "notdef.box" in got:
            failures.append(f"{form}: .notdef or the box in {got}")
        elif got != want:
            failures.append(f"{form}: shaped {got}, expected {want}")
        digraphs += sum(1 for g in carved if g in CARVED.DIGRAPHS.values())
        acutes += carved.count("lengthmark")
    fixtures = [(t, collapse(w)) for t, w in CARVED.FIXTURES + CARVED.LOST_FIXTURES] + HAND_FIXTURES
    for text, want in fixtures:
        got = r.glyph_names(text)
        if got != want:
            failures.append(f"{text!r}: shaped {got}, expected {want}")
    failures += mark_failures(r)
    failures += ignorable_failures(r)
    total = len(fixtures) + len(MARK_FIXTURES) + len(IGNORABLE_FIXTURES)
    print(
        f"{font}: {len(forms)} forms shaped, {digraphs} digraphs, {acutes} long vowels and "
        f"{doubled} doubled forms expected, {total} fixtures, {len(failures)} failures"
    )
    return failures


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--font", default=str(ROOT / "fonts" / "PirzathHand-Regular.ttf"))
    ap.add_argument("--thalorna", default=str(Path.home() / "dev/HeroicLands/thalorna"))
    ap.add_argument("--note", help="read the language note from this file instead of git")
    ap.add_argument("--encoding", help="apply this encoding file instead of encodings/pirzath.json")
    ap.add_argument("--fixtures-only", action="store_true",
                    help="shape the fixtures alone and read no lexicon")
    args = ap.parse_args()
    forms = [] if args.fixtures_only else CARVED.lexicon_forms(Path(args.thalorna), Path(args.note) if args.note else None)
    encoded = Encoded("pirzath-hand", args.encoding)
    failures = run(Path(args.font), forms, encoded)
    for f in failures[:40]:
        print(f"{args.font}: error: {f}")
    if len(failures) > 40:
        print(f"{args.font}: error: ... and {len(failures) - 40} more")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
