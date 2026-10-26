# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""The code points of every character each face draws, in the order they are assigned.

A left-to-right face draws each of its characters on a code point of its own in a
block of plane 15, the Supplementary Private Use Area-A: Pirzath from U+F0000,
Thuravark from U+F0100, Semaron from U+F0200, Helónika from U+F0300, Vedyakshara
from U+F0400, Teng
Chou's characters from U+F1000 and its Jurthati syllabary from U+F2000, Chalish
Pilam Common's numbers and glyphs from U+F3000, and Chalish Pilam Ceremonial's numbers,
glyphs, syllable signs and joiners from U+F4000. Within a block, characters are
assigned in groups: capitals (each followed by its own long-vowel group where the face
has one), small letters, digraphs, diphthongs, numerals, points, marks, and format
controls. A group
starts on a fixed code point and the gaps between groups leave room for later letters. tools/write_css.py
writes the resulting table to fonts.json, and tools/codepoints.py checks the built
fonts against it.

A contextual form a face draws from the characters around it is not a character and
has no code point: joined and doubled forms, the doubling mark, Pirzath Hand's long
vowels drawn from a vowel and its length mark, Thuravark's acute mark drawn as a
second stave, Qalezu Hand's catch-before forms, and Vedyakshara's fused, half, final
and r-foot forms and its placed vowel signs. Vedyakshara's groups follow
tools/vedyakshara/encoding.json: consonants, independent vowels, vowel signs and its
other marks, numerals and points. Helónika's follow tools/helonika/encoding.json:
capitals, the capital additions and long vowels, small letters, the small additions
and long vowels, numerals, points and the accent. The space stays U+0020.

A row also carries a ``name``, in Unicode's style, read from the script's name table in
``tools/names/<script>.json`` (see ``names``). A row the table does not name has no ``name``.

The Qalezu Hand, Khelathi Zethu Glyphs and Veldikko tables are read from their
encoding.json.
A Khelathi Zethu Glyphs row also carries its sign id as the ``key`` that types it in
its Emacs input method. The other scripts are typed by sound (tools/sound_keys.json),
so a character of theirs has no key of its own.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

ROOT = Path(__file__).resolve().parent.parent

# The registry of code point blocks. A block lists the families that draw on it; a
# block with no families is reserved or unassigned. Ranges do not overlap, and the
# DEVELOPING.md's "Code point blocks" table is rendered from this list (readme_table).
BLOCKS = [
    {
        "start": 0xF0000,
        "end": 0xF00FF,
        "use": "Pirzath",
        "direction": "left to right",
        "families": ["Pirzath Carved", "Pirzath Hand"],
    },
    {
        "start": 0xF0100,
        "end": 0xF01FF,
        "use": "Thuravark",
        "direction": "left to right",
        "families": ["Thuravark Carved", "Thuravark Carved Bound"],
    },
    {"start": 0xF0200, "end": 0xF02FF, "use": "Semaron", "direction": "left to right", "families": ["Semaron Kuriale"]},
    {
        "start": 0xF0300,
        "end": 0xF03FF,
        "use": "Helónika: capitals, small letters, the kh and zh letters, long vowels, digits, the raised dot, the register-mark and the accent",
        "direction": "left to right",
        "families": ["Helonika Book"],
    },
    {
        "start": 0xF0400,
        "end": 0xF04FF,
        "use": "Vedyakshara: consonants, independent vowels, vowel signs, the cut, the soft dot, digits and bars",
        "direction": "left to right",
        "families": ["Vedyakshara Classical"],
    },
    {
        "start": 0xF0500,
        "end": 0xF0FFF,
        "use": "Reserved for the remaining alphabets and syllabaries, 256 code points each as they are assigned",
        "direction": "left to right",
        "families": [],
    },
    {
        "start": 0xF1000,
        "end": 0xF1FFF,
        "use": "Teng Chou: characters, one per morpheme, in the order they are added",
        "direction": "left to right",
        "families": ["Teng Chou"],
    },
    {
        "start": 0xF2000,
        "end": 0xF20FF,
        "use": "Teng Chou: the Jurthati syllabary",
        "direction": "left to right",
        "families": ["Teng Chou"],
    },
    {"start": 0xF2100, "end": 0xF2FFF, "use": "Reserved for Teng Chou", "direction": "left to right", "families": []},
    {
        "start": 0xF3000,
        "end": 0xF3FFF,
        "use": "Chalish Pilam Common: the numbers and the places of the count, then the glyphs, in the order they are added",
        "direction": "left to right",
        "families": ["Chalish Pilam Common"],
    },
    {
        "start": 0xF4000,
        "end": 0xF4FFF,
        "use": "Chalish Pilam Ceremonial: the numbers, the concept glyphs, the syllable signs from U+F4400 and the joiners at U+F4FF0",
        "direction": "left to right",
        "families": ["Chalish Pilam Ceremonial"],
    },
    {
        "start": 0x1E960,
        "end": 0x1E9FF,
        "use": "Khelathi Zethu Glyphs, overflow beyond its main block",
        "direction": "right to left",
        "families": ["Khelathi Zethu Glyphs"],
    },
    {
        "start": 0x13430,
        "end": 0x1343F,
        "use": "Egyptian Hieroglyph Format Controls, Unicode's own: Khelathi Zethu Glyphs' quadrat and cartouche controls",
        "direction": "left to right",
        "families": ["Khelathi Zethu Glyphs"],
        "unicode": True,
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
        "use": "Khelathi Zethu Glyphs: signs, and its format controls at U+1EC60–U+1EC6F",
        "direction": "right to left",
        "families": ["Khelathi Zethu Glyphs"],
    },
    {
        "start": 0x1ED50,
        "end": 0x1EDFF,
        "use": "Veldikko: letters, vowel marks and the signs of length, pitch, emphasis and doubling",
        "direction": "right to left",
        "families": ["Veldikko"],
    },
    {"start": 0x100000, "end": 0x10FFFD, "use": "Plane 16, unassigned", "direction": "", "families": []},
]


def readme_table() -> str:
    """The Markdown table of BLOCKS that the DEVELOPING.md's "Code point blocks" section carries."""
    lines = ["| Range | Use | Direction |", "| --- | --- | --- |"]
    for b in sorted(BLOCKS, key=lambda b: b["start"]):
        lines.append(f"| U+{b['start']:04X}\u2013U+{b['end']:04X} | {b['use']} | {b['direction'] or '\u2013'} |")
    return "\n".join(lines)


# Face -> (block start, block end, groups). A group is (kind, first code point, glyphs).
SEMARON = (
    0xF0200,
    0xF02FF,
    [
        ("letter", 0xF0200, "A B D E F G H I J K L M N O P R S T U V W Y Z Q".split()),
        ("letter", 0xF0220, "A.long E.long I.long O.long U.long".split()),
        ("letter", 0xF0230, "a b d e f g h i j k l m n o p r s t u v w y z q".split()),
        ("letter", 0xF0248, "a.long e.long i.long o.long u.long".split()),
        ("digraph", 0xF0250, ["th", "TH"]),
        ("numeral", 0xF0258, [f"num.{i}" for i in range(10)]),
        ("point", 0xF0268, ["point"]),
        ("mark", 0xF0270, ["grave"]),
        ("digraph", 0xF0280, "dh DH kh KH gh GH sh SH zh ZH ts TS ch CH ng NG ny NY".split()),
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
        ("diphthong", 0xF0128, "ai au oi".split()),
        ("numeral", 0xF0130, [f"num.{i}" for i in range(10)]),
        ("point", 0xF0140, ["period"]),
        ("mark", 0xF0148, ["acutecomb"]),
        ("control", 0xF0150, ["crown.open", "crown.close"]),
    ],
)

def _teng_chou():
    """Teng Chou's characters from U+F1000, in the order of tools/teng-chou/characters.py
    and then the five stages of the tally (tools/teng-chou/tally.py), and the Jurthati
    signs from U+F2000, in the order of tools/teng-chou/syllabary.py. A character or sign
    is added at the end of its list, so none is renumbered."""
    sys.path.insert(0, str(ROOT / "tools" / "teng-chou"))
    import characters  # noqa: E402
    import syllabary  # noqa: E402
    import tally  # noqa: E402

    return (
        0xF1000,
        0xF20FF,
        [
            ("character", 0xF1000, [c.glyph for c in characters.CHARACTERS] + [s.glyph for s in tally.STAGES.values()]),
            ("syllable", 0xF2000, [s.glyph for s in syllabary.SIGNS]),
        ],
    )


TENGCHOU = _teng_chou()

VEDYAKSHARA_KINDS = {"consonant": "letter", "vowel": "letter", "vowel sign": "mark", "sign": "mark",
                     "digit": "numeral", "point": "point"}


def _vedyakshara():
    """Vedyakshara Classical's block from tools/vedyakshara/encoding.json: each run of
    consecutive code points of one kind is a group."""
    enc = json.loads((ROOT / "tools" / "vedyakshara" / "encoding.json").read_text(encoding="utf-8"))
    groups = []
    for e in enc["glyphs"]:
        point, kind = int(e["codepoint"][2:], 16), VEDYAKSHARA_KINDS[e["kind"]]
        last = groups[-1] if groups else None
        if last and last[0] == kind and last[1] + len(last[2]) == point:
            last[2].append(e["glyph"])
        else:
            groups.append((kind, point, [e["glyph"]]))
    return int(enc["block"]["start"][2:], 16), int(enc["block"]["end"][2:], 16), groups


VEDYAKSHARA = _vedyakshara()

HELONIKA_KINDS = {"capital": "letter", "small": "letter", "digit": "numeral", "point": "point", "mark": "mark"}


def _helonika():
    """Helonika Book's block from tools/helonika/encoding.json: each run of consecutive
    code points of one kind is a group."""
    enc = json.loads((ROOT / "tools" / "helonika" / "encoding.json").read_text(encoding="utf-8"))
    groups = []
    for e in enc["glyphs"]:
        point, kind = int(e["codepoint"][2:], 16), HELONIKA_KINDS[e["kind"]]
        last = groups[-1] if groups else None
        if last and last[0] == kind and last[1] + len(last[2]) == point:
            last[2].append(e["glyph"])
        else:
            groups.append((kind, point, [e["glyph"]]))
    return int(enc["block"]["start"][2:], 16), int(enc["block"]["end"][2:], 16), groups


HELONIKA = _helonika()

CHALISH_KINDS = {"number": "numeral", "concept": "character"}


def _chalish():
    """Chalish Pilam Common's block from tools/chalish-pilam/encoding.json: each run of
    consecutive code points of one kind is a group. A retired row keeps its code point
    and draws nothing."""
    enc = json.loads((ROOT / "tools" / "chalish-pilam" / "encoding.json").read_text(encoding="utf-8"))
    groups = []
    for e in enc["glyphs"]:
        if e.get("retired"):
            continue
        point, kind = int(e["codepoint"][2:], 16), CHALISH_KINDS[e["kind"]]
        last = groups[-1] if groups else None
        if last and last[0] == kind and last[1] + len(last[2]) == point:
            last[2].append(e["glyph"])
        else:
            groups.append((kind, point, [e["glyph"]]))
    return 0xF3000, 0xF3FFF, groups


CHALISH = _chalish()

CEREMONIAL_KINDS = {"number": "numeral", "concept": "character", "syllable": "syllable", "joiner": "control"}


def _ceremonial():
    """Chalish Pilam Ceremonial's block from tools/chalish-pilam/ceremonial_encoding.json:
    each run of consecutive code points of one kind is a group. A pending row (zero and the
    places of the count) keeps its code point and has no drawing, so it draws the box and
    is not listed."""
    enc = json.loads((ROOT / "tools" / "chalish-pilam" / "ceremonial_encoding.json").read_text(encoding="utf-8"))
    groups = []
    for e in enc["glyphs"]:
        if e.get("retired") or e.get("pending"):
            continue
        point, kind = int(e["codepoint"][2:], 16), CEREMONIAL_KINDS[e["kind"]]
        last = groups[-1] if groups else None
        if last and last[0] == kind and last[1] + len(last[2]) == point:
            last[2].append(e["glyph"])
        else:
            groups.append((kind, point, [e["glyph"]]))
    return 0xF4000, 0xF4FFF, groups


CEREMONIAL = _ceremonial()

# Font file stem -> block.
LTR = {
    "SemaronKuriale-Regular": SEMARON,
    "PirzathCarved-Regular": PIRZATH,
    "PirzathHand-Regular": PIRZATH,
    "ThuravarkCarved-Regular": THURAVARK,
    "TengChou-Regular": TENGCHOU,
    "ChalishPilamCommon-Regular": CHALISH,
    "ChalishPilamCeremonial-Regular": CEREMONIAL,
    "VedyaksharaClassical-Regular": VEDYAKSHARA,
    "HelonikaBook-Regular": HELONIKA,
}


def ltr_table(stem: str) -> list[dict]:
    """The table of a left-to-right face: code point, glyph name and kind per character."""
    _, _, groups = LTR[stem]
    rows = []
    for kind, start, glyphs in groups:
        for offset, glyph in enumerate(glyphs):
            rows.append({"codepoint": f"U+{start + offset:04X}", "glyph": glyph, "kind": kind})
    return rows


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
    return sorted(rows, key=lambda r: int(r["codepoint"][2:], 16))


VELDIKKO_KINDS = {"letter": "letter", "vowel": "mark", "modifier": "mark", "bar": "mark"}


def veldikko_table() -> list[dict]:
    """Veldikko's table, from tools/veldikko/encoding.json, in code point order."""
    enc = json.loads((ROOT / "tools" / "veldikko" / "encoding.json").read_text(encoding="utf-8"))
    rows = [{"codepoint": e["codepoint"], "glyph": e["glyph"], "kind": VELDIKKO_KINDS[e["kind"]]} for e in enc["glyphs"]]
    return sorted(rows, key=lambda r: int(r["codepoint"][2:], 16))


def zethu_controls() -> list[dict]:
    """Khelathi Zethu Glyphs' format controls, from tools/khelathi-zethu-glyphs/controls.json."""
    path = ROOT / "tools" / "khelathi-zethu-glyphs" / "controls.json"
    return json.loads(path.read_text(encoding="utf-8"))["controls"]


def zethu_table() -> list[dict]:
    """Khelathi Zethu Glyphs' table: each drawn sign's default form, then each format
    control at its own code point in the font's block and at its Unicode code point.
    A control has no key: the Emacs input method types signs by id."""
    enc = json.loads((ROOT / "tools" / "khelathi-zethu-glyphs" / "encoding.json").read_text(encoding="utf-8"))
    rows = [
        {"codepoint": e["codepoint"], "glyph": e["glyph"], "kind": "sign", "key": e["id"]}
        for e in enc["signs"]
        if e["drawn"]
    ]
    controls = zethu_controls()
    rows += [{"codepoint": c["twin"], "glyph": c["glyph"], "kind": "control"} for c in controls]
    rows += [{"codepoint": c["codepoint"], "glyph": c["glyph"], "kind": "control"} for c in controls]
    return rows


# Font file stem -> script, the key of its name table.
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


def names(script: str) -> dict[str, str]:
    """The character names of a script, by code point, from ``tools/names/<script>.json``.

    The file is one JSON object of ``"U+XXXX": "NAME"`` pairs, a name written in
    Unicode's style: uppercase ASCII letters, digits, spaces and hyphens. A script
    without a file has no names, and its rows carry no ``name``.
    """
    path = ROOT / "tools" / "names" / f"{script}.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def named(stem: str, rows: list[dict]) -> list[dict]:
    """The rows with a ``name`` after the code point wherever the script's table names it."""
    table_names = names(SCRIPTS[stem])
    out = []
    for row in rows:
        new = {"codepoint": row["codepoint"]}
        if row["codepoint"] in table_names:
            new["name"] = table_names[row["codepoint"]]
        new.update({k: v for k, v in row.items() if k != "codepoint"})
        out.append(new)
    return out


def zethu_number(point: int) -> int:
    """The position of a code point in Khelathi Zethu Glyphs' code point space, counting from 1.

    The main block of tools/khelathi-zethu-glyphs/encoding.json comes first and the other
    blocks BLOCKS registers for the font follow in code point order, Unicode's own format
    controls apart, so a sign's number
    depends on its code point alone and never changes when another sign is drawn.
    """
    enc = json.loads((ROOT / "tools" / "khelathi-zethu-glyphs" / "encoding.json").read_text(encoding="utf-8"))
    main = (int(enc["block"]["start"][2:], 16), int(enc["block"]["end"][2:], 16))
    spans = [main] + sorted(
        (b["start"], b["end"])
        for b in BLOCKS
        if "Khelathi Zethu Glyphs" in b["families"] and (b["start"], b["end"]) != main and not b.get("unicode")
    )
    before = 0
    for start, end in spans:
        if start <= point <= end:
            return before + point - start + 1
        before += end - start + 1
    raise ValueError(f"U+{point:04X} is outside Khelathi Zethu Glyphs' blocks")


def zethu_name(point: int) -> str:
    """A sign's name, ``ZETHU CHARACTER <n>``; a format control's name, Unicode's at its
    Unicode code point and the font's own at its twin."""
    for c in zethu_controls():
        if point == int(c["codepoint"][2:], 16):
            return c["name"]
        if point == int(c["twin"][2:], 16):
            return c["twin_name"]
    return f"ZETHU CHARACTER {zethu_number(point):03d}"


def table(stem: str) -> list[dict]:
    if stem in LTR:
        return named(stem, ltr_table(stem))
    if stem == "QalezuHand-Regular":
        return named(stem, qalezu_table())
    if stem == "KhelathiZethuGlyphs-Regular":
        return named(stem, zethu_table())
    if stem == "Veldikko-Regular":
        return named(stem, veldikko_table())
    raise KeyError(stem)
