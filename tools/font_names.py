# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Confirm that every font is listed by the right name and declares only its own script.

    .venv/bin/python tools/font_names.py [font ...]

An application's font list reads the name table, and Word and LibreOffice consult
the OS/2 support declarations to decide whether to draw a font's name in the font
itself. A font fails when

- name IDs 1, 2, 3, 4, 5 and 6 are missing on the Windows platform (3, 1, 0x409) or
  the Macintosh platform (1, 0, 0), or the two platforms disagree;
- the family name is not the one FAMILIES gives it, in ID 1 or in ID 16;
- ID 1 differs from the family name and IDs 16 and 17 are missing;
- ID 4 is not the family name followed by ``Regular``;
- ID 6 is not the family name without spaces, then ``-Regular``;
- ``ulUnicodeRange1-4`` differs from the bits of the ranges that the font's own
  script code points fall in. A code point belongs to the script when it is
  assigned and its script is not Latin, Common or Inherited, so a font whose script
  sits on unassigned or private-use code points declares no range at all, and a
  Latin range (Basic Latin, Latin-1 and every other Latin or IPA bit) is never set;
- ``ulCodePageRange1-2`` sets a Latin code page.

The fonts map Latin code points only to print the box (tools/notdef_box.py); they
do not support Latin, and declare nothing that says they do.
"""

import sys
import unicodedata
from pathlib import Path

from fontTools.ttLib import TTFont
from fontTools.ttLib.tables.O_S_2f_2 import OS2_UNICODE_RANGES, intersectUnicodeRanges
from fontTools.unicodedata import script

ROOT = Path(__file__).resolve().parent.parent

# The family name of each built font, by file name.
FAMILIES = {
    "PirzathCarved-Regular.ttf": "Pirzath Carved",
    "PirzathHand-Regular.ttf": "Pirzath Hand",
    "ThuravarkCarved-Regular.ttf": "Thuravark Carved",
    "QalezuHand-Regular.ttf": "Qalezu Hand",
    "KhelathiZethuGlyphs-Regular.ttf": "Khelathi Zethu Glyphs",
}

WINDOWS = (3, 1, 0x409)
MACINTOSH = (1, 0, 0)
REQUIRED = (1, 2, 3, 4, 5, 6)
NOT_SCRIPT = {"Latn", "Zyyy", "Zinh"}

# Bits of ulCodePageRange1 and ulCodePageRange2 (numbered 0-63) for code pages that
# serve Latin text.
LATIN_CODE_PAGES = {0, 1, 4, 7, 8, 29, 50, 52, 54, 55, 56, 58, 59, 62, 63}

def range_name(bit: int) -> str:
    return " / ".join(name for name, _ in OS2_UNICODE_RANGES[bit])


LATIN_RANGE_BITS = {bit for bit in range(len(OS2_UNICODE_RANGES)) if "Latin" in range_name(bit) or "IPA" in range_name(bit)}


def expected_unicode_bits(cmap) -> set[int]:
    own = {
        cp
        for cp in cmap
        if unicodedata.category(chr(cp)) not in ("Cn", "Co", "Cs", "Cc")
        and script(chr(cp)) not in NOT_SCRIPT
    }
    return intersectUnicodeRanges(own) if own else set()


def declared_bits(words) -> set[int]:
    return {i * 32 + b for i, word in enumerate(words) for b in range(32) if word >> b & 1}


def records(font: TTFont, platform: tuple) -> dict[int, str]:
    return {
        n.nameID: n.toUnicode() for n in font["name"].names if (n.platformID, n.platEncID, n.langID) == platform
    }


def check(path: Path) -> list[str]:
    path = Path(path)
    family = FAMILIES.get(path.name)
    if family is None:
        return [f"{path}: error: no family name is recorded for {path.name}; add it to FAMILIES in tools/font_names.py"]
    font = TTFont(str(path))
    out = []

    def problem(message: str):
        out.append(f"{path}: error: {message}")

    windows = records(font, WINDOWS)
    mac = records(font, MACINTOSH)
    for label, table in (("Windows", windows), ("Macintosh", mac)):
        for nid in REQUIRED:
            if not table.get(nid):
                problem(f"name {nid} is missing on the {label} platform")
    for nid in REQUIRED + (16, 17):
        if windows.get(nid) != mac.get(nid) and windows.get(nid) and mac.get(nid):
            problem(f"name {nid} is {windows[nid]!r} on Windows and {mac[nid]!r} on the Macintosh")
        elif nid in (16, 17) and (nid in windows) != (nid in mac):
            problem(f"name {nid} is on one platform only")

    postscript = family.replace(" ", "") + "-Regular"
    for label, table in (("Windows", windows), ("Macintosh", mac)):
        if table.get(1) != family and table.get(16) != family:
            problem(f"the {label} family name is {table.get(16) or table.get(1)!r}, expected {family!r}")
        if table.get(1) != family and not (table.get(16) and table.get(17)):
            problem(f"name 1 on the {label} platform is not the family name and names 16 and 17 are missing")
        if table.get(16) is not None and table.get(16) != family:
            problem(f"name 16 on the {label} platform is {table.get(16)!r}, expected {family!r}")
        if table.get(4) and table.get(4) != f"{family} Regular":
            problem(f"name 4 on the {label} platform is {table.get(4)!r}, expected {family + ' Regular'!r}")
        if table.get(6) and table.get(6) != postscript:
            problem(f"name 6 on the {label} platform is {table.get(6)!r}, expected {postscript!r}")

    os2 = font["OS/2"]
    declared = declared_bits([os2.ulUnicodeRange1, os2.ulUnicodeRange2, os2.ulUnicodeRange3, os2.ulUnicodeRange4])
    expected = expected_unicode_bits(font.getBestCmap())
    for bit in sorted(declared & LATIN_RANGE_BITS):
        problem(f"ulUnicodeRange sets bit {bit}, {range_name(bit)}, a Latin range")
    for bit in sorted(declared - expected - LATIN_RANGE_BITS):
        problem(f"ulUnicodeRange sets bit {bit}, {range_name(bit)}, which no code point of the script is in")
    for bit in sorted(expected - declared):
        problem(f"ulUnicodeRange leaves bit {bit} clear, {range_name(bit)}, which a code point of the script is in")
    for bit in sorted(declared_bits([os2.ulCodePageRange1, os2.ulCodePageRange2]) & LATIN_CODE_PAGES):
        problem(f"ulCodePageRange sets bit {bit}, a Latin code page")
    return out


def summary(path: Path) -> str:
    os2 = TTFont(str(path))["OS/2"]
    bits = sorted(declared_bits([os2.ulUnicodeRange1, os2.ulUnicodeRange2, os2.ulUnicodeRange3, os2.ulUnicodeRange4]))
    pages = sorted(declared_bits([os2.ulCodePageRange1, os2.ulCodePageRange2]))
    return f"{path}: names complete on both platforms, unicode range bits {bits or 'none'}, code page bits {pages or 'none'}"


def main():
    paths = [Path(a) for a in sys.argv[1:]] or sorted((ROOT / "fonts").glob("*-Regular.ttf"))
    status = 0
    for p in paths:
        problems = check(p)
        print(summary(p) if not problems else f"{p}: {len(problems)} problems")
        for line in problems:
            print(line)
        status |= bool(problems)
    sys.exit(status)


if __name__ == "__main__":
    main()
