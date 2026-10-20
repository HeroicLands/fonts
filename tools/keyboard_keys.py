# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""The key of every character, for the keyboard layouts, input methods and cheatsheets.

A key is a string: a base key with its modifiers, ``"a"``, ``"shift+s"``, ``"option+a"``
or ``"option+shift+a"``. The base key is a letter, a digit or one of the punctuation
keys of the main block of a US keyboard. Khelathi Zethu Glyphs has more signs than a
keyboard has keys, so its key is the sign's id, ``"08-001"``, typed as those characters.

tools/codepoint_order.py puts ``assign``'s result in every row of the ``codepoints``
tables, tools/write_css.py writes it to fonts.json, and tools/keyboards.py reads it
from fonts.json to write the layouts, input methods and cheatsheets. A family's
faces share one table, so one layout types for each of them.

The schemes, by family. Letters sit on their roman keys and numerals on the digit row.

- Semaron: small letters plain, capitals with Shift, ``th`` and ``TH`` and the long
  vowels with Option (Option+Shift for the capitals).
- Pirzath: letters plain, with Shift the digraph letters (on the first letter of the
  digraph, or the nearest free key) and the diphthongs. The numerals ten to fifteen
  sit on Option and the digits 0 to 5.
- Thuravark: letters plain, the digraph letters with Shift on their first letter.
- Qalezu: consonant signs plain, the digraph signs with Shift, the doubled signs with
  Option, and the signs written after a catch with Option+Shift on the single signs.
  The characters then left over take the first free keys of ``QALEZU_POOL``.
- Option+E is the acute mark in the families that have one.
"""

import re

OPTION_PREFIX = "\\"

# Base keys of the main block of a US keyboard, with the unshifted and shifted character.
LETTERS = "abcdefghijklmnopqrstuvwxyz"
DIGITS = "0123456789"
PUNCTUATION = "`-=[]\\;',./"
BASE_KEYS = LETTERS + DIGITS + PUNCTUATION
SHIFTED = {
    **{c: c.upper() for c in LETTERS},
    **dict(zip(DIGITS, ")!@#$%^&*(")),
    **dict(zip(PUNCTUATION, "~_+{}|:\"<>?")),
}

# macOS virtual key code of each base key on an ANSI keyboard.
MAC_CODES = {
    "a": 0, "s": 1, "d": 2, "f": 3, "h": 4, "g": 5, "z": 6, "x": 7, "c": 8, "v": 9,
    "b": 11, "q": 12, "w": 13, "e": 14, "r": 15, "y": 16, "t": 17,
    "1": 18, "2": 19, "3": 20, "4": 21, "6": 22, "5": 23, "=": 24, "9": 25, "7": 26,
    "-": 27, "8": 28, "0": 29, "]": 30, "o": 31, "u": 32, "[": 33, "i": 34, "p": 35,
    "l": 37, "j": 38, "'": 39, "k": 40, ";": 41, "\\": 42, ",": 43, "/": 44, "n": 45,
    "m": 46, ".": 47, "`": 50,
}  # fmt: skip

# The physical order of the keys, rows from the top, for cheatsheets.
KEY_ORDER = "`1234567890-=" + "qwertyuiop[]\\" + "asdfghjkl;'" + "zxcvbnm,./"

LAYERS = ["", "shift", "option", "option+shift"]
ZETHU_KEY = re.compile(r"^\d\d-\d{3}$")


def parse(key: str) -> tuple[bool, bool, str] | None:
    """(shift, option, base key) of a key string, or None when it is not a key."""
    parts = key.split("+")
    base, mods = parts[-1], parts[:-1]
    if base not in BASE_KEYS or len(base) != 1:
        return None
    if mods not in ([], ["shift"], ["option"], ["option", "shift"]):
        return None
    return "shift" in mods, "option" in mods, base


def spell(shift: bool, option: bool, base: str) -> str:
    return "+".join((["option"] if option else []) + (["shift"] if shift else []) + [base])


def layer(key: str) -> str:
    shift, option, _ = parse(key)
    return spell(shift, option, "")[:-1]


def typed(shift: bool, base: str) -> str:
    return SHIFTED[base] if shift else base


def quail_sequence(key: str) -> str:
    """The characters typed in Emacs for a key. Option has no Emacs key, so it is the
    prefix ``\\`` before the character the rest of the key types."""
    if ZETHU_KEY.match(key):
        return key
    shift, option, base = parse(key)
    return (OPTION_PREFIX if option else "") + typed(shift, base)


def is_zethu(key: str) -> bool:
    return bool(ZETHU_KEY.match(key))


def check_scheme(keys: dict[str, str]) -> None:
    """Refuse an assignment where two glyphs share a key or a key is not a key."""
    seen: dict[str, str] = {}
    for glyph, key in keys.items():
        if parse(key) is None:
            raise ValueError(f"{glyph}: {key!r} is not a key")
        if key in seen:
            raise ValueError(f"{glyph} and {seen[key]} both want {key}")
        seen[key] = glyph


# -- Semaron ----------------------------------------------------------------------------


def semaron(rows: list[dict]) -> dict[str, str]:
    keys = {}
    for row in rows:
        glyph = row["glyph"]
        if glyph.endswith(".long"):
            vowel = glyph[0]
            keys[glyph] = ("option+shift+" if vowel.isupper() else "option+") + vowel.lower()
        elif glyph in ("th", "TH"):
            keys[glyph] = ("option+shift+" if glyph == "TH" else "option+") + "t"
        elif row["kind"] == "letter":
            keys[glyph] = ("shift+" + glyph.lower()) if glyph.isupper() else glyph
        elif glyph.startswith("num."):
            keys[glyph] = glyph[4:]
        elif glyph == "point":
            keys[glyph] = "."
        elif glyph == "grave":
            keys[glyph] = "`"
        else:
            raise KeyError(f"Semaron: no key rule for {glyph}")
    return keys


# -- Pirzath ----------------------------------------------------------------------------

PIRZATH_SHIFT = {
    # digraph letters: the first letter, else the nearest free key
    "t_h": "shift+t",
    "d_h": "shift+d",
    "k_h": "shift+k",
    "g_h": "shift+g",
    "sh": "shift+s",
    "zh": "shift+z",
    "ts": "shift+x",
    "ch": "shift+c",
    "ng": "shift+n",
    "ny": "shift+y",
    "hl": "shift+h",
    # diphthongs: the first vowel, except ou, whose second letter is the w of "ow"
    "ai": "shift+a",
    "ei": "shift+e",
    "oi": "shift+o",
    "au": "shift+u",
    "ou": "shift+w",
}
PIRZATH_POINTS = {
    "period": ".",
    "comma": ",",
    "exclam": "shift+1",
    "hyphen": "-",
    "quote.open": "shift+,",
    "quote.close": "shift+.",
    "lengthmark": "option+e",
    "catch": "'",
}


def pirzath(rows: list[dict]) -> dict[str, str]:
    keys = {}
    for row in rows:
        glyph = row["glyph"]
        if glyph in PIRZATH_SHIFT:
            keys[glyph] = PIRZATH_SHIFT[glyph]
        elif glyph in PIRZATH_POINTS:
            keys[glyph] = PIRZATH_POINTS[glyph]
        elif glyph.startswith("num."):
            n = int(glyph[4:])
            keys[glyph] = str(n) if n < 10 else f"option+{n - 10}"
        elif row["kind"] == "letter" and len(glyph) == 1:
            keys[glyph] = glyph
        else:
            raise KeyError(f"Pirzath: no key rule for {glyph}")
    return keys


# -- Thuravark --------------------------------------------------------------------------


def thuravark(rows: list[dict]) -> dict[str, str]:
    keys = {}
    for row in rows:
        glyph = row["glyph"]
        if row["kind"] == "digraph":
            keys[glyph] = "shift+" + glyph[0]
        elif glyph.startswith("num."):
            keys[glyph] = glyph[4:]
        elif glyph == "period":
            keys[glyph] = "."
        elif glyph == "acutecomb":
            keys[glyph] = "option+e"
        elif row["kind"] == "letter" and len(glyph) == 1:
            keys[glyph] = glyph
        else:
            raise KeyError(f"Thuravark: no key rule for {glyph}")
    return keys


# -- Qalezu -----------------------------------------------------------------------------

QALEZU_DIGRAPH = {"th": "shift+t", "kh": "shift+k", "gh": "shift+g", "sh": "shift+s", "tj": "shift+c"}
DIGIT_OF = dict(zip("zero one two three four five six seven eight nine".split(), DIGITS))

# The keys that characters without a rule of their own take, in this order: the Shift
# letters, then Option+Shift letters, then Option+Shift digits.
QALEZU_POOL = (
    [f"shift+{c}" for c in LETTERS]
    + [f"option+shift+{c}" for c in LETTERS]
    + [f"option+shift+{c}" for c in DIGITS]
)


def qalezu(rows: list[dict]) -> dict[str, str]:
    keys: dict[str, str] = {}
    left = []
    for row in rows:
        glyph, kind = row["glyph"], row["kind"]
        if glyph in DIGIT_OF:
            keys[glyph] = DIGIT_OF[glyph]
        elif glyph == "period":
            keys[glyph] = "."
        elif glyph == "comma":
            keys[glyph] = ","
        elif glyph == "catch":
            keys[glyph] = "'"
        elif glyph in QALEZU_DIGRAPH:
            keys[glyph] = QALEZU_DIGRAPH[glyph]
        elif kind == "letter" and len(glyph) == 1:
            keys[glyph] = glyph
        elif glyph.endswith(".dbl") and len(glyph) == 5:
            keys[glyph] = "option+" + glyph[0]
        elif glyph.endswith(".catch") and len(glyph) == 7 and glyph[0] in LETTERS:
            keys[glyph] = "option+shift+" + glyph[0]
        else:
            left.append(glyph)
    free = [k for k in QALEZU_POOL if k not in set(keys.values())]
    if len(left) > len(free):
        raise ValueError(f"Qalezu: {len(left)} characters left over and {len(free)} free keys")
    keys.update(zip(left, free))
    return keys


SCHEMES = {
    "SemaronKuriale-Regular": semaron,
    "PirzathCarved-Regular": pirzath,
    "PirzathHand-Regular": pirzath,
    "ThuravarkCarved-Regular": thuravark,
    "QalezuHand-Regular": qalezu,
}


def assign(stem: str, rows: list[dict]) -> list[dict]:
    """The rows with a ``key`` added to each. Khelathi Zethu Glyphs rows carry their own
    sign id as the key, so they are not assigned here."""
    keys = SCHEMES[stem](rows)
    check_scheme(keys)
    missing = [r["glyph"] for r in rows if r["glyph"] not in keys]
    if missing:
        raise ValueError(f"{stem}: no key for {', '.join(missing)}")
    return [{**row, "key": keys[row["glyph"]]} for row in rows]
