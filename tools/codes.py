# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""The glyph codes of each script, and text written as a sequence of them.

    import codes
    codes.text("pirzath", "DALK A LADHAV KAMV U+0020 STOP")   # the characters
    codes.spell("pirzath", "\\U000F000B\\U000F0000")             # "DALK A"

Every character a face draws has a short code, unique within its script: a letter its
name (``PARGH``, ``CHEROLA_MIN``), a digit ``DIGIT_ZERO``, a mark or a point what it
does (``STOP``, ``LONG``, ``CATCH``). ``tools/codes/<script>.json`` is the one table of
them, a JSON object of ``"U+XXXX": "CODE"`` pairs, and tools/write_css.py writes each
code into fonts.json beside its code point and name. A code matches
``^[A-Za-z0-9_]+$`` and is case-sensitive: Teng Chou's ``KA`` and ``ka`` are two
characters.

A sequence is codes separated by whitespace. A token ``U+XXXX``, four to six hexadecimal
digits, is a character the script has no code for, such as the space ``U+0020``.

The specimens set texts of the setting in a face. Each face's texts are stored in
``tools/texts/<face>.json``, each its roman spelling and its sequence of codes, and
``Written`` gives a text's characters by its roman spelling; ``WrittenRenderer`` is a
Renderer that takes the roman spelling and shapes the stored characters.
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CODES = ROOT / "tools" / "codes"
CODE = re.compile(r"^[A-Za-z0-9_]+$")
POINT = re.compile(r"^U\+([0-9A-F]{4,6})$")

# Font file stem -> script, the key of its code table and its name table.
SCRIPTS = {
    "SemaronKuriale-Regular": "semaron",
    "PirzathCarved-Regular": "pirzath",
    "PirzathHand-Regular": "pirzath",
    "ThuravarkCarved-Regular": "thuravark",
    "QalezuHand-Regular": "qalezu",
    "KhelathiZethuGlyphs-Regular": "zethu",
    "TengChou-Regular": "tengchou",
    "ChalishPilamCommon-Regular": "chalish",
    "ChalishPilamCeremonial-Regular": "chalishceremonial",
    "Veldikko-Regular": "veldikko",
    "VedyaksharaClassical-Regular": "vedyakshara",
    "HelonikaBook-Regular": "helonika",
}

_tables: dict[str, dict[str, str]] = {}


def table(script: str) -> dict[str, str]:
    """The codes of a script by code point, ``"U+XXXX": "CODE"``, from ``tools/codes/<script>.json``."""
    if script not in _tables:
        _tables[script] = json.loads((CODES / f"{script}.json").read_text(encoding="utf-8"))
    return _tables[script]


def characters(script: str) -> dict[str, str]:
    """Each code of a script and the character it names."""
    return {code: chr(int(point[2:], 16)) for point, code in table(script).items()}


def text(script: str, sequence: str) -> str:
    """The characters a sequence of codes names."""
    chars = characters(script)
    out = []
    for token in sequence.split():
        point = POINT.match(token)
        if point:
            out.append(chr(int(point.group(1), 16)))
        elif token in chars:
            out.append(chars[token])
        else:
            raise KeyError(f"{script} has no code {token!r}")
    return "".join(out)


def spell(script: str, characters_: str) -> str:
    """A string of characters as a sequence of the script's codes."""
    by_point = table(script)
    return " ".join(by_point.get(f"U+{ord(c):04X}", f"U+{ord(c):04X}") for c in characters_)


class Written:
    """The stored texts of one face, ``tools/texts/<face>.json``, by their roman spelling."""

    def __init__(self, face: str):
        self.path = ROOT / "tools" / "texts" / f"{face}.json"
        data = json.loads(self.path.read_text(encoding="utf-8"))
        self.script = data["script"]
        self.texts = {t["roman"]: t["codes"] for t in data["texts"]}

    def one(self, roman: str) -> str:
        """The characters of the text stored for ``roman``."""
        if roman not in self.texts:
            raise KeyError(f"{self.path.relative_to(ROOT)}: no text {roman!r}")
        return text(self.script, self.texts[roman])

    def write(self, romans: list[str]) -> list[str]:
        return [self.one(r) for r in romans]


class WrittenRenderer:
    """A Renderer whose text is a roman spelling, set as the characters stored for it.

    ``shape``, ``glyph_names``, ``text`` and ``width`` take the roman spelling; everything
    else is the wrapped Renderer's.
    """

    def __init__(self, renderer, written: Written):
        self.renderer = renderer
        self.written = written

    def __getattr__(self, name):
        return getattr(self.renderer, name)

    def shape(self, roman: str, *args, **kwargs):
        return self.renderer.shape(self.written.one(roman), *args, **kwargs)

    def glyph_names(self, roman: str, direction=None):
        return self.renderer.glyph_names(self.written.one(roman), direction)

    def text(self, img, x, baseline, roman, size, color, features=None, direction=None, script="Zyyy"):
        return self.renderer.text(img, x, baseline, self.written.one(roman), size, color, features, direction, script)

    def width(self, roman, size, features=None, direction=None):
        return self.renderer.width(self.written.one(roman), size, features, direction)
