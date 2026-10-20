# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""The code points of every character each face draws, in the order they are assigned.

A left-to-right face draws each of its characters on a code point of its own in a
block of plane 15, the Supplementary Private Use Area-A: Pirzath from U+F0000,
Thuravark from U+F0100 and Semaron from U+F0200. Within a block, characters are
assigned in groups: capitals (each followed by its own long-vowel group where the face
has one), small letters, digraphs, diphthongs, numerals, points, and marks. A group
starts on a fixed code point and the gaps between groups leave room for later letters. tools/write_css.py
writes the resulting table to fonts.json, and tools/codepoints.py checks the built
fonts against it.

A glyph the face substitutes for a spelling is not a character and has no code point:
joined, initial and doubled forms, the doubling mark, precomposed long vowels in
Pirzath and Thuravark, the letters c and C that only spell ch, y in Thuravark, and the
straight quotation mark. The space stays U+0020.

The Qalezu Hand and Khelathi Zethu Glyphs tables are read from their encoding.json.
Every row also carries the ``key`` that types it, which tools/keyboard_keys.py assigns.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import keyboard_keys  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

# The registry of code point blocks. A block lists the families that draw on it; a
# block with no families is reserved or unassigned. Ranges do not overlap, and the
# README's "Code point blocks" table is rendered from this list (readme_table).
BLOCKS = [
    {
        "start": 0xF0000,
        "end": 0xF00FF,
        "use": "Pirzath",
        "direction": "left to right",
        "families": ["Pirzath Carved", "Pirzath Hand", "Pirzath Hand Lifted"],
    },
    {"start": 0xF0100, "end": 0xF01FF, "use": "Thuravark", "direction": "left to right", "families": ["Thuravark Carved"]},
    {"start": 0xF0200, "end": 0xF02FF, "use": "Semaron", "direction": "left to right", "families": ["Semaron Kuriale"]},
    {
        "start": 0xF0300,
        "end": 0xF0FFF,
        "use": "Reserved for the remaining alphabets and syllabaries, 256 code points each as they are assigned",
        "direction": "left to right",
        "families": [],
    },
    {"start": 0xF1000, "end": 0xF2FFF, "use": "Reserved for Teng Chou", "direction": "left to right", "families": []},
    {
        "start": 0x1E960,
        "end": 0x1E9FF,
        "use": "Khelathi Zethu Glyphs, overflow beyond its main block",
        "direction": "right to left",
        "families": ["Khelathi Zethu Glyphs"],
    },
    {
        "start": 0x1EA00,
        "end": 0x1EA3F,
        "use": "Qalezu: signs, digits and punctuation",
        "direction": "right to left",
        "families": ["Qalezu Hand"],
    },
    {
        "start": 0x1EA40,
        "end": 0x1EC6F,
        "use": "Khelathi Zethu Glyphs",
        "direction": "right to left",
        "families": ["Khelathi Zethu Glyphs"],
    },
    {
        "start": 0x1ECC0,
        "end": 0x1ECFF,
        "use": "Qalezu: a sign with a catch before it",
        "direction": "right to left",
        "families": ["Qalezu Hand"],
    },
    {"start": 0x100000, "end": 0x10FFFD, "use": "Plane 16, unassigned", "direction": "", "families": []},
]


def readme_table() -> str:
    """The Markdown table of BLOCKS that the README's "Code point blocks" section carries."""
    lines = ["| Range | Use | Direction |", "| --- | --- | --- |"]
    for b in sorted(BLOCKS, key=lambda b: b["start"]):
        lines.append(f"| U+{b['start']:04X}\u2013U+{b['end']:04X} | {b['use']} | {b['direction'] or '\u2013'} |")
    return "\n".join(lines)


# Face -> (block start, block end, groups). A group is (kind, first code point, glyphs).
SEMARON = (
    0xF0200,
    0xF027F,
    [
        ("letter", 0xF0200, "A B D E F G H I J K L M N O P R S T U V W Y Z".split()),
        ("letter", 0xF0220, "A.long E.long I.long O.long U.long".split()),
        ("letter", 0xF0230, "a b d e f g h i j k l m n o p r s t u v w y z".split()),
        ("letter", 0xF0248, "a.long e.long i.long o.long u.long".split()),
        ("digraph", 0xF0250, ["th", "TH"]),
        ("numeral", 0xF0258, [f"num.{i}" for i in range(10)]),
        ("point", 0xF0268, ["point"]),
        ("mark", 0xF0270, ["grave"]),
    ],
)

PIRZATH = (
    0xF0000,
    0xF007F,
    [
        ("letter", 0xF0000, "a e i o u p b f v m t d n k g s z h l r j q w y catch".split()),
        ("digraph", 0xF0020, "t_h d_h k_h g_h sh zh ts ch ng ny hl".split()),
        ("diphthong", 0xF0030, "ai au ei oi ou".split()),
        ("numeral", 0xF0040, [f"num.{i}" for i in range(16)]),
        ("point", 0xF0050, "period comma exclam hyphen quote.open quote.close".split()),
        ("mark", 0xF0060, ["lengthmark"]),
    ],
)

THURAVARK = (
    0xF0100,
    0xF017F,
    [
        ("letter", 0xF0100, "a e i o u b d f g h j k l m n p r s t v w z".split()),
        ("digraph", 0xF0120, "th dh kh gh hl ng".split()),
        ("numeral", 0xF0130, [f"num.{i}" for i in range(10)]),
        ("point", 0xF0140, ["period"]),
        ("mark", 0xF0148, ["acutecomb"]),
    ],
)

# Font file stem -> block. Pirzath Hand and Pirzath Hand Lifted are one file.
LTR = {
    "SemaronKuriale-Regular": SEMARON,
    "PirzathCarved-Regular": PIRZATH,
    "PirzathHand-Regular": PIRZATH,
    "ThuravarkCarved-Regular": THURAVARK,
}


def ltr_table(stem: str) -> list[dict]:
    """The table of a left-to-right face: code point, glyph name and kind per character."""
    _, _, groups = LTR[stem]
    rows = []
    for kind, start, glyphs in groups:
        for offset, glyph in enumerate(glyphs):
            rows.append({"codepoint": f"U+{start + offset:04X}", "glyph": glyph, "kind": kind})
    return keyboard_keys.assign(stem, rows)


def block(stem: str) -> tuple[int, int]:
    start, end, _ = LTR[stem]
    return start, end


QALEZU_KINDS = {"sign": "letter", "digit": "numeral", "punctuation": "point"}


def qalezu_table() -> list[dict]:
    """Qalezu Hand's table, from its encoding.json, in code point order."""
    enc = json.loads((ROOT / "tools" / "qalezu-hand" / "encoding.json").read_text(encoding="utf-8"))
    rows = [
        {"codepoint": e["codepoint"], "glyph": e["glyph"], "kind": QALEZU_KINDS.get(e["kind"], e["kind"])}
        for e in enc["glyphs"]
    ]
    return keyboard_keys.assign("QalezuHand-Regular", sorted(rows, key=lambda r: int(r["codepoint"][2:], 16)))


def zethu_table() -> list[dict]:
    """Khelathi Zethu Glyphs' table: each drawn sign's default form."""
    enc = json.loads((ROOT / "tools" / "khelathi-zethu-glyphs" / "encoding.json").read_text(encoding="utf-8"))
    return [
        {"codepoint": e["codepoint"], "glyph": e["glyph"], "kind": "sign", "key": e["id"]}
        for e in enc["signs"]
        if e["drawn"]
    ]


def table(stem: str) -> list[dict]:
    if stem in LTR:
        return ltr_table(stem)
    if stem == "QalezuHand-Regular":
        return qalezu_table()
    if stem == "KhelathiZethuGlyphs-Regular":
        return zethu_table()
    raise KeyError(stem)
