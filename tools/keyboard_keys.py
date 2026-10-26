# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Keys and chords, as the sound key map writes them.

A key is a string: a base key with its modifiers, ``"a"``, ``"shift+s"``, ``"option+a"``
or ``"option+shift+a"``. The base key is a letter, a digit or one of the punctuation
keys of the main block of a US keyboard. Khelathi Zethu Glyphs has more signs than a
keyboard has keys, so its key is the sign's id, ``"08-001"``, typed as those characters.

tools/sound_keys.json puts each sound of the spelling guide on one key, and
tools/keyboards.py writes the layouts, input methods and cheatsheets from it and from
keyboards/sounds.json. Option is AltGr on Windows and the third level on Linux; Emacs
has no Option key, so Option+x is typed ``\\`` and then the character x types.

The key map also lists the characters of markup. Each types itself, as plain ASCII, on
the key that types it on a US keyboard, and the signs: keys that are not sounds, each
typing one code point in the one layout whose script writes it.
"""

import json
import re
from pathlib import Path

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
    prefix ``\\`` before the character the rest of the key types. The backslash key
    is the prefix itself, so it is typed twice, and Option+backslash, which carries
    nothing, shares that sequence."""
    if ZETHU_KEY.match(key):
        return key
    shift, option, base = parse(key)
    if base == "\\" and not shift and not option:
        return OPTION_PREFIX * 2
    return (OPTION_PREFIX if option else "") + typed(shift, base)


def is_zethu(key: str) -> bool:
    return bool(ZETHU_KEY.match(key))


def load() -> dict:
    """tools/sound_keys.json: the principles, and every sound with its spelling and key."""
    return json.loads((Path(__file__).resolve().parent / "sound_keys.json").read_text(encoding="utf-8"))


# The scripts with a layout, as keyboards.SCRIPTS lists them.
LAYOUT_SCRIPTS = ("semaron", "pirzath", "thuravark", "qalezu", "veldikko", "vedyakshara", "helonika")


def signs() -> list[dict]:
    """The signs of tools/sound_keys.json: keys that are not sounds, each typing one code
    point in the one layout whose script writes it, and the literals, which every layout
    types: the literal immutable markers, drawn by no script."""
    data = load()
    literals = [{**sign, "script": script, "literal": True} for script in LAYOUT_SCRIPTS for sign in data.get("literals", [])]
    return data.get("signs", []) + literals


def every_key() -> list[str]:
    """Every key and chord of the four layers, in the physical order of the keys, apart
    from Option+backslash, whose Emacs sequence is the backslash key's."""
    keys = [spell(shift, option, base) for base in KEY_ORDER for option in (False, True) for shift in (False, True)]
    return [k for k in keys if k != "option+\\"]


def markup_key(char: str) -> str | None:
    """The key that types a character on a US keyboard, or None when none does."""
    for base in BASE_KEYS:
        for shift in (False, True):
            if typed(shift, base) == char:
                return spell(shift, False, base)
    return None


def markup() -> dict[str, str]:
    """key -> the ASCII character it types, for every character of markup in the key map."""
    out = {}
    for char in load()["markup"]:
        out[markup_key(char) or f"(no key for {char})"] = char
    return out
