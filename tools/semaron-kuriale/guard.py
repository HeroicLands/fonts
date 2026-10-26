# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Shape every Vylari lexicon form in Semaron Kuriale and assert the result.

    .venv/bin/python tools/semaron-kuriale/guard.py [--font fonts/SemaronKuriale-Regular.ttf]
                                                 [--thalorna ~/dev/HeroicLands/thalorna | --note FILE]
                                                 [--encoding FILE | --fixtures-only]

The forms come from the ``words`` list in the frontmatter of
``assets/content/Skills/Languages/Vylari.md`` on the thalorna repository's
``origin/main``; the body of the note is never read. Roman is lowercase, so each
form is lowercased, then written in
Semaron's code points by the ``semaron`` encoding (``encodings/semaron.json``, or
the file ``--encoding`` names), and the result is shaped. The expected glyph
sequence is derived from the spelling rules below, which the guard owns and which read neither the font nor the encoding:

- Semaron has case: a capital letter writes its majuscule, and ``th`` is one letter,
  ``Th`` its majuscule; ``tH`` and ``TH`` are the letters t and H, and T and H;
- ``ch`` types the letters t, s and h, because the script has no c;
- a doubled ``a``, ``i`` or ``u`` is the long vowel; ``ee`` and ``oo`` are two plain vowels;
- an acute vowel is the plain vowel, because Semaron writes no stress, and ``ë``
  is ``e``;
- ``q`` is ``k``, because the script has no q;
- ``y`` before a vowel is the glide y, and anywhere else the vowel i;
- ``.``, ``?``, ``!``, ``!!`` and ``,`` write the point, told apart by invisible marks;
  the other standard marks, the quotation marks, the dash, the ellipsis, the verse
  ends and the braces of a name, draw nothing; colons, semicolons and the en dash print the box;
- Vylari ``à`` writes a and the catch. After an ancient t, k, d or g, the catch
  stands on that stop before the a;
- ``'``, ``’``, a grave accent and a hyphen-minus after a letter are the catch, a mark
  that takes no room; with no letter before them they print the box, and the
  Unicode hyphens U+2010 and U+2011 are characters the script lacks;
- ``c``, ``x``, the English quotation marks, ``¡`` and every other character the
  script lacks are outside the encoding; the guard sets them in the font, where they
  print the box;
- otherwise only the default-ignorable characters draw nothing.

Fixtures cover each rule, the catch on an x-height letter, a tall letter and
after a long vowel, the numerals, and the sample lines of the specimens. They
are written through the encoding and shaped too, so the guard checks the encoding
and the face together.
"""

import argparse
import subprocess
import sys
from pathlib import Path

import yaml
from fontTools.pens.boundsPen import BoundsPen

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from encoded import Encoded, drawn_glyphs, drawn_names  # noqa: E402
from render import Renderer  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent
NOTE = "assets/content/Skills/Languages/Vylari.md"

BOX = "notdef.box"
BOX_GLYPHS = {BOX}
EMPTY = {"ignorable", "ignorable.sub"}

LETTERS = "abdefghijklmnoprstuvwz"
VOWELS = "aeiou"
LONG_VOWELS = "aiu"
ACUTES = {"á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u", "ë": "e", "q": "k",
          "Á": "A", "É": "E", "Í": "I", "Ó": "O", "Ú": "U", "Ë": "E", "Q": "K"}
# The standard marks that draw the point: the four terminals and the pause, told apart
# by invisible marks. The other standard marks write invisible marks alone. Two-character
# marks come first, as the encoding matches them.
PAUSES = ("!!", ".", "?", "!", ",")
UNDRAWN = ("//", "«", "»", "‹", "›", "—", "…", "/", "{", "}")
CATCHES = "'’`-"
SILENT = "​‌‍‎‏‪‫‬‭‮⁦⁧⁨⁩﻿"
NUMERALS = [f"num.{i}" for i in range(10)]
# The glyphs a catch can sit on.
BASES = {
    *LETTERS, *LETTERS.upper(), "th", "TH",
    *(f"{v}.long" for v in VOWELS), *(f"{v.upper()}.long" for v in VOWELS),
}


def expected_glyphs(text: str) -> list[str]:
    """The glyph names a line must shape to, from the spelling rules alone."""
    t = "".join(ACUTES.get(ch, ch) for ch in text)
    out: list[str] = []
    i = 0
    while i < len(t):
        ch = t[i]
        pair = t[i : i + 2]
        pause = next((m for m in PAUSES if t.startswith(m, i)), None)
        if pause:
            out.append("point")
            i += len(pause)
            continue
        undrawn = next((m for m in UNDRAWN if t.startswith(m, i)), None)
        if undrawn:
            i += len(undrawn)
            continue
        low = ch.lower()
        if low in "tkdg" and i + 1 < len(t) and t[i + 1] in "àÀ":
            out += [ch, "grave", "A" if t[i + 1].isupper() else "a"]
            i += 2
            continue
        if ch in "àÀ":
            out += ["A" if ch.isupper() else "a", "grave"]
            i += 1
            continue
        if pair in ("th", "Th"):
            out.append("TH" if ch.isupper() else "th")
            i += 2
            continue
        if pair in ("ch", "Ch"):
            out += ["T" if ch.isupper() else "t", "s", "h"]
            i += 2
            continue
        if low in LONG_VOWELS and pair in (low + low, low.upper() + low):
            out.append((low.upper() if ch.isupper() else low) + ".long")
            i += 2
            continue
        if low == "y":
            following = t[i + 1].lower() if i + 1 < len(t) else ""
            name = "y" if following and following in VOWELS + "à" else "i"
            out.append(name.upper() if ch.isupper() else name)
        elif low in LETTERS and ch.isascii():
            out.append(ch)
        elif ch.isascii() and ch.isdigit():
            out.append(f"num.{ch}")
        elif ch == " ":
            out.append("space")
        elif ch in CATCHES:
            out.append("grave" if out and out[-1] in BASES else BOX)
        elif ch in SILENT:
            pass
        else:
            out.append(BOX)
        i += 1
    return out


def normalized(names: list[str]) -> list[str]:
    """Shaped glyph names with the empty ignorables dropped and every copy of the box named as it."""
    return [BOX if n in BOX_GLYPHS else n for n in names if n not in EMPTY]


# The fixtures spell out what each rule gives, so the derivation above is checked against the rulings
# themselves and not against itself.
FIXTURES: list[tuple[str, list[str]]] = [
    # roman is lowercase: a capital is outside the encoding and prints the box
    ("a", ["a"]), ("daamela", ["d", "a.long", "m", "e", "l", "a"]), ("fa", ["f", "a"]),
    *[(c, [c]) for c in "abdefghjklmnoprstuvwz"],
    # a capital writes its majuscule, with no mark for case
    *[(c.upper(), [c.upper()]) for c in "abdefghjklmnoprstuvwz"],
    ("Daamela", ["D", "a.long", "m", "e", "l", "a"]), ("DAAMELA", ["D", "A", "A", "M", "E", "L", "A"]),
    ("Th", ["TH"]), ("TH", ["T", "H"]), ("tH", ["t", "H"]), ("Athu", ["A", "th", "u"]),
    ("Ch", ["T", "s", "h"]), ("CH", [BOX, "H"]), ("cH", [BOX, "H"]),
    ("Aa", ["A.long"]), ("aA", ["a", "A"]), ("Ii", ["I.long"]), ("Uu", ["U.long"]), ("Ee", ["E", "e"]), ("Oo", ["O", "o"]),
    ("Á", ["A"]), ("É", ["E"]), ("Í", ["I"]), ("Ó", ["O"]), ("Ú", ["U"]), ("Ë", ["E"]), ("Q", ["K"]), ("Meqes", ["M", "e", "k", "e", "s"]),
    ("Aá", ["A.long"]), ("Áa", ["A.long"]), ("Áá", ["A.long"]), ("AÁ", ["A", "A"]),
    ("Ya", ["Y", "a"]), ("Y", ["I"]), ("Y ", ["I", "space"]),
    *[(f"K{c}", ["K", "grave"]) for c in CATCHES],
    ("À", ["A", "grave"]), ("Kà", ["K", "grave", "a"]), ("kÀ", ["k", "grave", "A"]), ("KÀ", ["K", "grave", "A"]),
    ("TÀ", ["T", "grave", "A"]), ("YÀ", ["Y", "A", "grave"]),
    ("Au'Khelathu", ["A", "u", "grave", "K", "h", "e", "l", "a", "th", "u"]),
    # th is one letter
    ("th", ["th"]), ("thh", ["th", "h"]), ("tth", ["t", "th"]), ("athu", ["a", "th", "u"]),
    # ch types t, s, h
    ("ch", ["t", "s", "h"]), ("tch", ["t", "t", "s", "h"]), ("chh", ["t", "s", "h", "h"]), ("cth", [BOX, "th"]),
    # a doubled vowel is the curl
    ("aa", ["a.long"]), ("ii", ["i.long"]), ("uu", ["u.long"]),
    ("aaa", ["a.long", "a"]), ("aaaa", ["a.long", "a.long"]), ("ee", ["e", "e"]), ("oo", ["o", "o"]),
    ("viir", ["v", "i.long", "r"]), ("kuun", ["k", "u.long", "n"]),
    # an acute gives the plain vowel
    ("á", ["a"]), ("é", ["e"]), ("í", ["i"]), ("ó", ["o"]), ("ú", ["u"]),
    ("áa", ["a.long"]), ("aá", ["a.long"]), ("ái", ["a", "i"]), ("dáamela", ["d", "a.long", "m", "e", "l", "a"]),
    # y before a vowel is the glide, elsewhere the vowel i
    ("ya", ["y", "a"]), ("yá", ["y", "a"]), ("yaa", ["y", "a.long"]), ("yi", ["y", "i"]),
    ("ty", ["t", "i"]), ("y", ["i"]), ("yy", ["i", "i"]), ("yya", ["i", "y", "a"]),
    ("yth", ["i", "th"]), ("y'", ["i", "grave"]), ("y ", ["i", "space"]), ("dayos", ["d", "a", "y", "o", "s"]),
    # the catch, on every input
    *[(f"a{c}", ["a", "grave"]) for c in CATCHES],
    *[(f"l{c}", ["l", "grave"]) for c in CATCHES],
    *[(f"aa{c}", ["a.long", "grave"]) for c in CATCHES],
    *[(f"k{c}", ["k", "grave"]) for c in CATCHES],
    *[(f"th{c}", ["th", "grave"]) for c in CATCHES],
    *[(f"uu{c}k", ["u.long", "grave", "k"]) for c in CATCHES],
    # a catch with no letter before it is the box
    *[(c, [BOX]) for c in CATCHES],
    *[(f" {c}", ["space", BOX]) for c in CATCHES],
    *[(f"1{c}", ["num.1", BOX]) for c in CATCHES],
    *[(f".{c}", ["point", BOX]) for c in CATCHES],
    ("a''", ["a", "grave", BOX]), ("a'-", ["a", "grave", BOX]), ("c'", [BOX, BOX]),
    # Vylari's precomposed catch keeps its original base.
    ("kàralzon", ["k", "grave", "a", "r", "a", "l", "z", "o", "n"]),
    ("kàrthorgila", ["k", "grave", "a", "r", "th", "o", "r", "g", "i", "l", "a"]),
    ("à", ["a", "grave"]),
    ("kà", ["k", "grave", "a"]), ("tà", ["t", "grave", "a"]), ("dà", ["d", "grave", "a"]), ("gà", ["g", "grave", "a"]),
    ("yà", ["y", "a", "grave"]),
    # Other tongues retain their own catch spellings in the shared encoding.
    ("au'khelathu", ["a", "u", "grave", "k", "h", "e", "l", "a", "th", "u"]),
    ("zeghet'nelgu", ["z", "e", "g", "h", "e", "t", "grave", "n", "e", "l", "g", "u"]),
    ("amqel'uqa", ["a", "m", "k", "e", "l", "grave", "u", "k", "a"]),
    ("selth-kelmeza", ["s", "e", "l", "th", "grave", "k", "e", "l", "m", "e", "z", "a"]),
    # The terminals and the pause write the point; the other standard marks draw nothing,
    # and any other punctuation is outside the encoding and prints the box.
    *[(c, ["point"]) for c in PAUSES],
    *[(c, []) for c in UNDRAWN],
    ("a!!a", ["a", "point", "a"]), ("a, a? a!", ["a", "point", "space", "a", "point", "space", "a", "point"]),
    ("«a ‹a›» a— a…", ["a", "space", "a", "space", "a", "space", "a"]),
    ("{daimela} a", ["d", "a", "i", "m", "e", "l", "a", "space", "a"]),
    *[(c, [BOX]) for c in ";:–"],
    ("daimela vethor orfenamen. theson.",
     ["d", "a", "i", "m", "e", "l", "a", "space", "v", "e", "th", "o", "r", "space",
      "o", "r", "f", "e", "n", "a", "m", "e", "n", "point", "space", "th", "e", "s", "o", "n", "point"]),
    # the marks the script lacks, c and x print the box; q is k and ë is e
    *[(c, [BOX]) for c in '"“”¡()[]<>@#$%&*+=\\|_~^‘'],
    *[(c, [BOX]) for c in "cxCX"],
    ("a‐", ["a", BOX]), ("a‑", ["a", BOX]), ("q", ["k"]), ("meqes", ["m", "e", "k", "e", "s"]), ("ë", ["e"]),
    ("eza à daimela falvator.",
     ["e", "z", "a", "space", "a", "grave", "space", "d", "a", "i", "m", "e", "l", "a", "space", "f", "a", "l",
      "v", "a", "t", "o", "r", "point"]),
    # the numerals
    ("0123456789", NUMERALS),
    ("2026", ["num.2", "num.0", "num.2", "num.6"]),
    ("daamela. viir. kuun. 0123456789. 12. 2026.",
     ["d", "a.long", "m", "e", "l", "a", "point", "space", "v", "i.long", "r", "point", "space", "k", "u.long",
      "n", "point", "space", *NUMERALS, "point", "space", "num.1", "num.2", "point", "space", "num.2", "num.0",
      "num.2", "num.6", "point"]),
    # space, and the default-ignorables that draw nothing
    ("a b", ["a", "space", "b"]),
    ("da​k", ["d", "a", "k"]), ("da‍k", ["d", "a", "k"]), ("d⁦a⁩k", ["d", "a", "k"]),
    ("﻿dalk", ["d", "a", "l", "k"]),
]

# Pairs of lines the catch must set exactly as wide as the line without it.
WIDTH_PAIRS = [("kàralzon", "karalzon"), ("kàrthorgila", "karthorgila"), ("à", "a"),
               ("zeghet'nelgu", "zeghetnelgu"), ("selth-kelmeza", "selthkelmeza"),
               ("daa'", "daa"), ("a`l’k", "alk")]
# The catch sits over, beside or at the right of its base: these lines place one.
MARK_FIXTURES = ["a'", "e'", "o'", "k'", "m'", "v'", "l'", "h'", "t'", "th'", "aa'", "ii'",
                 "uu'", "k-a", "a’k", "à", "kàralzon", "kàrthorgila", "kà", "tà"]


def fixture_texts() -> list[str]:
    """Every roman text the fixtures write through the encoding."""
    return [t for t, _ in FIXTURES] + [t for pair in WIDTH_PAIRS for t in pair] + MARK_FIXTURES


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
    front = yaml.safe_load(text.split("\n---\n", 1)[0].lstrip("-\n"))
    forms = [w["form"].lower() for w in front["data"]["words"]]
    if not forms:
        raise SystemExit("the words list is empty")
    return forms


def mark_failures(r: Renderer, m: Encoded) -> list[str]:
    """Each catch takes no room and stands on its base."""
    failures = []
    glyphset = r.tt.getGlyphSet()
    for text in MARK_FIXTURES:
        shaped = r.shape(m.one(text))
        kept = [i for i, _ in drawn_glyphs(r, m.one(text))]
        names = [r.order[shaped.glyphs[i][0]] for i in kept]
        pen_x = 0
        base = None
        for name, (gid, gx, gy, adv) in zip(names, [shaped.glyphs[i] for i in kept]):
            if name != "grave":
                base = (name, pen_x, adv)
                pen_x += adv
                continue
            if base is None:
                failures.append(f"{text!r}: a catch has no base")
                continue
            bounds = BoundsPen(glyphset)
            glyphset[name].draw(bounds)
            x0, y0, x1, y1 = bounds.bounds
            if adv != 0:
                failures.append(f"{text!r}: the catch has an advance of {adv}")
            centre = gx + (x0 + x1) / 2
            if not (base[1] - 40 <= centre <= base[1] + base[2] + 140):
                failures.append(f"{text!r}: the catch is not seated on {base[0]} (centre {centre:.0f}, base {base[1]}..{base[1] + base[2]})")
            if gy + y0 < 200:
                failures.append(f"{text!r}: the catch sits too low on {base[0]} (its ink reaches down to {gy + y0:.0f})")
    return failures


def run(font: Path, forms: list[str], encoded: Encoded | None = None) -> list[str]:
    r = Renderer(font)
    m = encoded or Encoded("semaron-kuriale")
    m.write(forms + fixture_texts())
    failures = []
    digraphs = longs = catches = 0
    for form in forms:
        want = expected_glyphs(form)
        got = normalized(drawn_names(r, m.one(form)))
        if BOX in got and BOX not in want:
            failures.append(f"{form}: the box in {got}")
        elif got != want:
            failures.append(f"{form}: shaped {got}, expected {want}")
        digraphs += want.count("th")
        longs += sum(1 for g in want if g.endswith(".long"))
        catches += want.count("grave")
    for text, want in FIXTURES:
        derived = expected_glyphs(text)
        if derived != want:
            failures.append(f"{text!r}: the guard derives {derived} but the fixture says {want}")
        got = normalized(drawn_names(r, m.one(text)))
        if got != want:
            failures.append(f"{text!r}: shaped {got}, expected {want}")
    for text, plain in WIDTH_PAIRS:
        wide, narrow = r.shape(m.one(text)).advance, r.shape(m.one(plain)).advance
        if wide != narrow:
            failures.append(f"{text!r} sets {wide} wide, {plain!r} sets {narrow}")
    failures += mark_failures(r, m)
    print(
        f"{font}: {len(forms)} forms shaped, {digraphs} th, {longs} long vowels and {catches} catches expected, "
        f"{len(FIXTURES)} fixtures, {len(WIDTH_PAIRS)} width pairs, {len(MARK_FIXTURES)} mark placements, "
        f"{len(failures)} failures"
    )
    return failures


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--font", default=str(ROOT / "fonts" / "SemaronKuriale-Regular.ttf"))
    ap.add_argument("--thalorna", default=str(Path.home() / "dev/HeroicLands/thalorna"))
    ap.add_argument("--note", help="read the language note from this file instead of git")
    ap.add_argument("--encoding", help="apply this encoding file instead of encodings/semaron.json")
    ap.add_argument("--fixtures-only", action="store_true",
                    help="shape the fixtures alone and read no lexicon")
    args = ap.parse_args()
    if not Path(args.font).exists():
        print(f"{args.font}: error: the font does not exist")
        sys.exit(1)
    forms = [] if args.fixtures_only else lexicon_forms(Path(args.thalorna), Path(args.note) if args.note else None)
    encoded = Encoded("semaron-kuriale", args.encoding)
    failures = run(Path(args.font), forms, encoded)
    for f in failures[:40]:
        print(f"{args.font}: error: {f}")
    if len(failures) > 40:
        print(f"{args.font}: error: ... and {len(failures) - 40} more")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
