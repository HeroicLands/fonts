# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Write the keyboard layouts, Emacs input methods and cheatsheets of each font family.

    .venv/bin/python tools/keyboards.py

Everything is read from the ``codepoints`` tables of fonts.json, whose rows carry the
``key`` that types each character (tools/keyboard_keys.py assigns them), and from the
built fonts. A family's faces share one table, so one layout types for every face.

- ``keyboards/macos/HeroicLands.bundle``: one macOS ``.keylayout`` per family but
  Khelathi Zethu Glyphs, whose signs outnumber the keys.
- ``keyboards/windows/<family>.klc``: one Microsoft Keyboard Layout Creator source per
  family but Khelathi Zethu Glyphs. A code point of plane 15 is a ligature entry holding
  its surrogate pair; Option is AltGr.
- ``keyboards/linux/hl_<family>``: one XKB symbols file per family but Khelathi Zethu
  Glyphs, with a ``U<hex>`` keysym per character. Option is the third level.
- ``keyboards/emacs/heroiclands-<family>.el``: one Quail input method per family.
  Option has no Emacs key, so Option+x is typed as ``\\`` and then the character
  that x types. Khelathi Zethu Glyphs is typed by sign id.
- ``keyboards/<family>.md`` and ``specimens/<face folder>/keyboard.png``: the
  cheatsheet of the family, as a table and as a grid of every key beside its glyph in
  each face of the family. The script asserts that each cell's glyph is the glyph the
  table lists for the code point, and that a glyph with an outline leaves ink in its
  cell.
"""

import json
import plistlib
import sys
from pathlib import Path

from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
import keyboard_keys as kk  # noqa: E402
from render import Renderer, Shaped, label_font  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
BUNDLE = "HeroicLands.bundle"
BUNDLE_ID = "org.heroiclands.keyboardlayout"
MIRROR = "https://github.com/HeroicLands/fonts/blob/main"

FAMILIES = [
    {
        "key": "semaron",
        "title": "Semaron",
        "faces": ["Semaron Kuriale"],
        "specimens": "semaron-kuriale",
        "layout": "HL Semaron",
        "klc": "hlsemaro",
        "id": -26101,
        "scheme": [
            "Small letters sit on their roman keys and capitals on Shift.",
            "`th` and `TH`, and the ten long vowels, sit on Option: Option+vowel for the "
            "small long vowel and Option+Shift+vowel for the capital.",
            "Numerals sit on the digit row, the point on `.` and the grave on `` ` ``.",
        ],
    },
    {
        "key": "pirzath",
        "title": "Pirzath",
        "faces": ["Pirzath Carved", "Pirzath Hand", "Pirzath Hand Lifted"],
        "specimens": "pirzath",
        "layout": "HL Pirzath",
        "klc": "hlpirzat",
        "id": -26102,
        "scheme": [
            "Letters sit on their roman keys, and the catch on `'`.",
            "The digraph letters and the diphthongs sit on Shift, on the first letter of "
            "the digraph where that key is free: Shift+S `sh`, Shift+T `th`. Where it is "
            "taken, the nearest free key: `ts` on Shift+X, `ny` on Shift+Y, and `ou` on "
            "Shift+W.",
            "Numerals zero to nine sit on the digit row; numerals ten to fifteen on "
            "Option and the digits 0 to 5.",
            "The length mark sits on Option+E. Points sit on their roman keys; the "
            "opening and closing quotation marks on `<` and `>`.",
        ],
    },
    {
        "key": "thuravark",
        "title": "Thuravark",
        "faces": ["Thuravark Carved"],
        "specimens": "thuravark-carved",
        "layout": "HL Thuravark",
        "klc": "hlthurav",
        "id": -26103,
        "scheme": [
            "Letters sit on their roman keys.",
            "The digraph letters `th dh kh gh hl ng` sit on Shift and the first letter of "
            "the digraph.",
            "Numerals sit on the digit row, the point on `.` and the acute mark on Option+E.",
        ],
    },
    {
        "key": "qalezu",
        "title": "Qalezu",
        "faces": ["Qalezu Hand"],
        "specimens": "qalezu-hand",
        "layout": "HL Qalezu",
        "klc": "hlqalezu",
        "id": -26104,
        "scheme": [
            "Consonant signs sit on the key of their usual roman letter, and the catch on `'`.",
            "The digraph signs `th kh gh sh tj` sit on Shift and the first letter (`tj` on Shift+C).",
            "A doubled sign sits on Option and its letter. A sign written after a catch sits "
            "on Option+Shift and its letter. The remaining doubled digraph signs and the "
            "signs after a catch that are doubled or digraphs take the next free keys in "
            "code point order: the Shift letters, then the Option+Shift letters, then the "
            "Option+Shift digits.",
            "Numerals sit on the digit row; the point and comma on `.` and `,`.",
        ],
    },
    {
        "key": "zethu",
        "title": "Zethu",
        "faces": ["Khelathi Zethu Glyphs"],
        "specimens": "khelathi-zethu-glyphs",
        "layout": None,
        "id": None,
        "scheme": [
            "The signs far outnumber the keys of a keyboard, so there is no macOS layout. "
            "The Emacs input method is typed by sign id, such as `08-001`.",
        ],
    },
]

# Cheatsheet image
PAPER = (250, 247, 240)
INK = (28, 26, 24)
GREY = (110, 106, 100)
RULE = (214, 207, 194)
MARGIN = 24
SLOT = 72
GLYPH_PX = 60
TITLE_H = 44
CELL_H = 124
SHEET_W = 1500
LAYER_TITLES = {"": "Plain keys", "shift": "Shift", "option": "Option", "option+shift": "Option+Shift"}


def manifest() -> dict:
    return json.loads((ROOT / "fonts.json").read_text(encoding="utf-8"))


def family_faces(family: dict, faces: dict) -> tuple[list[dict], list[dict]]:
    """The manifest entries of a family's faces, and the one table they share."""
    entries = [faces[name] for name in family["faces"]]
    table = entries[0]["codepoints"]
    for entry in entries:
        assert entry["codepoints"] == table, f"{entry['name']}: the table differs from {entries[0]['name']}'s"
    return entries, table


def code(row: dict) -> int:
    return int(row["codepoint"][2:], 16)


# -- macOS --------------------------------------------------------------------------------

CONTROL_KEYS = {
    36: 0x0D, 48: 0x09, 49: 0x20, 51: 0x08, 52: 0x03, 53: 0x1B, 76: 0x03, 115: 0x01, 116: 0x0B,
    117: 0x7F, 119: 0x04, 121: 0x0C, 123: 0x1C, 124: 0x1D, 125: 0x1F, 126: 0x1E,
}  # fmt: skip


def ref(text: str) -> str:
    """Numeric character references for every character, so no escaping is needed."""
    return "".join(f"&#x{ord(c):04X};" for c in text)


def keylayout(family: dict, table: list[dict]) -> str:
    maps: list[dict[int, str]] = [{}, {}, {}, {}]
    for base in kk.BASE_KEYS:
        maps[0][kk.MAC_CODES[base]] = base
        maps[1][kk.MAC_CODES[base]] = kk.SHIFTED[base]
    for row in table:
        shift, option, base = kk.parse(row["key"])
        maps[int(shift) + 2 * int(option)][kk.MAC_CODES[base]] = chr(code(row))
    for m in maps:
        m.update({k: chr(v) for k, v in CONTROL_KEYS.items()})
    maxout = max(len(c.encode("utf-16-le")) // 2 for m in maps for c in m.values())
    selects = [
        (0, ["", "command", "control", "command control"]),
        (1, ["anyShift", "caps", "anyShift caps", "anyShift command"]),
        (2, ["anyOption"]),
        (3, ["anyShift anyOption", "anyShift anyOption caps"]),
    ]
    out = [
        '<?xml version="1.1" encoding="UTF-8"?>',
        '<!DOCTYPE keyboard SYSTEM "file://localhost/System/Library/DTDs/KeyboardLayout.dtd">',
        f'<keyboard group="126" id="{family["id"]}" name="{family["layout"]}" maxout="{maxout}">',
        '    <layouts>',
        '        <layout first="0" last="255" modifiers="Modifiers" mapSet="Keys"/>',
        '    </layouts>',
        '    <modifierMap id="Modifiers" defaultIndex="0">',
    ]
    for index, mods in selects:
        out.append(f'        <keyMapSelect mapIndex="{index}">')
        out += [f'            <modifier keys="{m}"/>' for m in mods]
        out.append("        </keyMapSelect>")
    out += ["    </modifierMap>", '    <keyMapSet id="Keys">']
    for index, m in enumerate(maps):
        out.append(f'        <keyMap index="{index}">')
        out += [f'            <key code="{k}" output="{ref(m[k])}"/>' for k in sorted(m)]
        out.append("        </keyMap>")
    out += ["    </keyMapSet>", "</keyboard>"]
    return "\n".join(out) + "\n"


def info_plist(layouts: list[dict]) -> bytes:
    version = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))["version"]
    plist = {
        "CFBundleIdentifier": f"{BUNDLE_ID}.fonts",
        "CFBundleName": "HeroicLands",
        "CFBundlePackageType": "BNDL",
        "CFBundleShortVersionString": version,
        "CFBundleVersion": version,
    }
    for family in layouts:
        plist[f"KLInfo_{family['layout']}"] = {
            "TISInputSourceID": f"{BUNDLE_ID}.{family['key']}",
            "TISIntendedLanguage": "en",
        }
    return plistlib.dumps(plist, sort_keys=False)


def write_macos(out: Path, tables: dict[str, list[dict]]) -> list[Path]:
    resources = out / "macos" / BUNDLE / "Contents" / "Resources"
    resources.mkdir(parents=True, exist_ok=True)
    layouts = [f for f in FAMILIES if f["layout"]]
    written = []
    path = out / "macos" / BUNDLE / "Contents" / "Info.plist"
    path.write_bytes(info_plist(layouts))
    written.append(path)
    for family in layouts:
        path = resources / f"{family['layout']}.keylayout"
        path.write_text(keylayout(family, tables[family["key"]]), encoding="utf-8")
        written.append(path)
    return written


# -- Windows ------------------------------------------------------------------------------

# ANSI scan code and MSKLC virtual key name of each base key.
WIN_KEYS = {
    "`": (0x29, "OEM_3"), "-": (0x0C, "OEM_MINUS"), "=": (0x0D, "OEM_PLUS"),
    "[": (0x1A, "OEM_4"), "]": (0x1B, "OEM_6"), "\\": (0x2B, "OEM_5"),
    ";": (0x27, "OEM_1"), "'": (0x28, "OEM_7"), ",": (0x33, "OEM_COMMA"),
    ".": (0x34, "OEM_PERIOD"), "/": (0x35, "OEM_2"),
    **{d: (0x02 + (int(d) - 1) % 10, d) for d in "1234567890"},
    **{c: (sc, c.upper()) for c, sc in zip(
        "qwertyuiop" "asdfghjkl" "zxcvbnm",
        [*range(0x10, 0x1A), *range(0x1E, 0x27), *range(0x2C, 0x33)],
    )},
}  # fmt: skip
WIN_STATES = [(0, 0), (1, 1), (2, None), (6, 2), (7, 3)]  # (shift state, layer) of each column
WIN_CTRL = {**{c: ord(c) - 96 for c in kk.LETTERS}, "[": 0x1B, "\\": 0x1C, "]": 0x1D}


def typed_chars(table: list[dict]) -> dict[tuple[int, str], int]:
    """(layer, base key) -> code point, with layer 0 plain, 1 Shift, 2 Option and 3 Option+Shift."""
    out = {}
    for row in table:
        shift, option, base = kk.parse(row["key"])
        out[(int(shift) + 2 * int(option), base)] = code(row)
    return out


def surrogates(point: int) -> tuple[int, int]:
    point -= 0x10000
    return 0xD800 + (point >> 10), 0xDC00 + (point & 0x3FF)


def klc(family: dict, table: list[dict]) -> str:
    typed = typed_chars(table)
    rows, ligatures = [], []
    order = sorted(WIN_KEYS, key=lambda b: WIN_KEYS[b][0])
    for base in order:
        sc, vk = WIN_KEYS[base]
        cells = []
        for state, layer in WIN_STATES:
            if layer is None:
                ctrl = WIN_CTRL.get(base)
                cells.append("-1" if ctrl is None else f"{ctrl:04x}")
            elif (layer, base) in typed:
                cells.append("%%")
                ligatures.append((vk, state, typed[(layer, base)]))
            elif layer < 2:
                cells.append(f"{ord(kk.typed(bool(layer), base)):04x}")
            else:
                cells.append("-1")
        rows.append(f"{sc:02x}\t{vk}\t\t0\t" + "\t".join(cells))
    rows.append("39\tSPACE\t\t0\t0020\t0020\t0020\t-1\t-1")
    name = family["layout"]
    out = [
        f'KBD\t{family["klc"]}\t"{name}"',
        "",
        'COPYRIGHT\t"(c) 2026 Tom Rodriguez"',
        "",
        'COMPANY\t"HeroicLands"',
        "",
        'LOCALENAME\t"en-US"',
        "",
        'LOCALEID\t"00000409"',
        "",
        "VERSION\t1.0",
        "",
        "SHIFTSTATE",
        "",
        "0\t//Column 4",
        "1\t//Column 5 : Shft",
        "2\t//Column 6 :       Ctrl",
        "6\t//Column 7 :       Ctrl Alt",
        "7\t//Column 8 : Shft  Ctrl Alt",
        "",
        "LAYOUT\t\t;an extra '@' at the end is a dead key",
        "",
        "//SC\tVK_\t\tCap\t0\t1\t2\t6\t7",
        "//--\t----\t\t----\t----\t----\t----\t----\t----",
        "",
        *rows,
        "",
        "LIGATURE",
        "",
        "//VK_\tMod#\tChar0\tChar1\tChar2\tChar3",
        "//----\t----\t-----\t-----\t-----\t-----",
        "",
    ]
    for vk, state, point in ligatures:
        units = [point] if point < 0x10000 else list(surrogates(point))
        out.append(f"{vk}\t{state}\t" + "\t".join(f"{u:04x}" for u in units))
    out += ["", "DESCRIPTIONS", "", f"0409\t{name}", "", "LANGUAGENAMES", "", "0409\tEnglish (United States)", "", "ENDKBD", ""]
    return "\r\n".join(out)


def write_windows(out: Path, tables: dict[str, list[dict]]) -> list[Path]:
    folder = out / "windows"
    folder.mkdir(parents=True, exist_ok=True)
    written = []
    for family in FAMILIES:
        if not family["layout"]:
            continue
        path = folder / f"{family['key']}.klc"
        # MSKLC reads a Unicode text file: UTF-16, little endian, with a byte order mark.
        path.write_bytes(b"\xff\xfe" + klc(family, tables[family["key"]]).encode("utf-16-le"))
        written.append(path)
    return written


# -- Linux --------------------------------------------------------------------------------

XKB_KEYS = {
    "`": "TLDE", "-": "AE11", "=": "AE12", "[": "AD11", "]": "AD12", "\\": "BKSL",
    ";": "AC10", "'": "AC11", ",": "AB08", ".": "AB09", "/": "AB10",
    **{d: f"AE{i:02d}" for i, d in enumerate("1234567890", 1)},
    **{c: f"AD{i:02d}" for i, c in enumerate("qwertyuiop", 1)},
    **{c: f"AC{i:02d}" for i, c in enumerate("asdfghjkl", 1)},
    **{c: f"AB{i:02d}" for i, c in enumerate("zxcvbnm", 1)},
}  # fmt: skip
XKB_NAMES = {
    **dict(zip("`-=[]\\;',./", "grave minus equal bracketleft bracketright backslash semicolon apostrophe comma period slash".split())),
    **dict(zip("~_+{}|:\"<>?", "asciitilde underscore plus braceleft braceright bar colon quotedbl less greater question".split())),
    **dict(zip(")!@#$%^&*(", "parenright exclam at numbersign dollar percent asciicircum ampersand asterisk parenleft".split())),
}  # fmt: skip


def xkb_keysym(char: str) -> str:
    return XKB_NAMES.get(char, char)


def xkb(family: dict, table: list[dict]) -> str:
    typed = typed_chars(table)
    lines = [
        f"// {family['layout']}: Type {family['title']} with the same keys as the macOS layout.",
        "// Generated by tools/keyboards.py from fonts.json. Option is the third level,",
        "// reached with the right Alt key.",
        "default partial alphanumeric_keys",
        'xkb_symbols "basic" {',
        '    include "us(basic)"',
        '    include "level3(ralt_switch)"',
        f'    name[Group1] = "{family["layout"]}";',
        "",
    ]
    for base in sorted(XKB_KEYS, key=lambda b: kk.KEY_ORDER.index(b)):
        if not any((layer, base) in typed for layer in range(4)):
            continue
        symbols = []
        for layer in range(4):
            if (layer, base) in typed:
                symbols.append(f"U{typed[(layer, base)]:X}")
            elif layer < 2:
                symbols.append(xkb_keysym(kk.typed(bool(layer), base)))
            else:
                symbols.append("NoSymbol")
        lines.append(f'    key <{XKB_KEYS[base]}> {{ type[Group1] = "FOUR_LEVEL", symbols[Group1] = [ {", ".join(symbols)} ] }};')
    lines += ["};", ""]
    return "\n".join(lines)


def write_linux(out: Path, tables: dict[str, list[dict]]) -> list[Path]:
    folder = out / "linux"
    folder.mkdir(parents=True, exist_ok=True)
    written = []
    for family in FAMILIES:
        if not family["layout"]:
            continue
        path = folder / f"hl_{family['key']}"
        path.write_text(xkb(family, tables[family["key"]]), encoding="utf-8")
        written.append(path)
    return written


# -- Emacs --------------------------------------------------------------------------------


def lisp(text: str) -> str:
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


def emacs_method(family: dict, face_names: list[str], table: list[dict]) -> str:
    name = f"heroiclands-{family['key']}"
    title = "HL-" + family["title"][:3]
    zethu = family["layout"] is None
    if zethu:
        how = [
            "Type a sign's id, such as 08-001, to insert the sign. Every id has the form",
            "two digits, a hyphen and three digits.",
        ]
    else:
        how = [
            "A letter types itself, Shift types the capital or the digraph on that key,",
            f"and Option has no Emacs key: Option+x is {kk.OPTION_PREFIX} and then the key",
            "that x types, so Option+Shift+a is \\A.",
        ]
    doc = [f"Type {', '.join(face_names)} with the same keys as the macOS layout."] + how
    doc.append(f"The cheatsheet keyboards/{family['key']}.md lists every key.")
    rules = "\n".join(f" ({lisp(kk.quail_sequence(r['key']))} #x{code(r):X})" for r in table)
    body = [
        f";;; {name}.el --- Type {family['title']} with Quail  -*- lexical-binding: t; -*-",
        "",
        ';; Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>',
        ";; SPDX-License-Identifier: OFL-1.1",
        "",
        ";;; Commentary:",
        "",
        f";; An input method for the code points of {', '.join(face_names)}.",
        ";; Generated by tools/keyboards.py from fonts.json. Put this directory on",
        f";; `load-path', evaluate (require '{name}), then M-x set-input-method.",
        "",
        ";;; Code:",
        "",
        "(require 'quail)",
        "",
        "(quail-define-package",
        f" {lisp(name)} {lisp(family['title'])} {lisp(title)} t",
        f" {lisp(chr(10).join(doc))}",
        " nil t nil nil nil nil nil nil nil nil t)",
        "",
        "(quail-define-rules",
        rules + ")",
        "",
        f"(provide '{name})",
        "",
        f";;; {name}.el ends here",
    ]
    return "\n".join(body) + "\n"


def write_emacs(out: Path, tables: dict[str, list[dict]]) -> list[Path]:
    folder = out / "emacs"
    folder.mkdir(parents=True, exist_ok=True)
    written = []
    for family in FAMILIES:
        path = folder / f"heroiclands-{family['key']}.el"
        path.write_text(emacs_method(family, family["faces"], tables[family["key"]]), encoding="utf-8")
        written.append(path)
    return written


# -- Cheatsheets --------------------------------------------------------------------------


def md_code(text: str) -> str:
    text = text.replace("|", "\\|")
    if "`" in text:
        return f"`` {text} ``"
    return f"`{text}`"


def cheatsheet(family: dict, table: list[dict]) -> str:
    zethu = family["layout"] is None
    lines = [
        f"# {family['title']} keyboard",
        "",
        f"Faces: {', '.join(family['faces'])}. The faces share code points, so one layout types for every face.",
        "",
        "- Emacs input method: "
        f"`keyboards/emacs/heroiclands-{family['key']}.el`, named `heroiclands-{family['key']}`.",
    ]
    if zethu:
        lines.append("- macOS, Windows and Linux layouts: none.")
    else:
        lines.append(f"- macOS layout: `keyboards/macos/{BUNDLE}`, input source **{family['layout']}**.")
        lines.append(f"- Windows layout: `keyboards/windows/{family['key']}.klc`, the Microsoft Keyboard Layout Creator source of **{family['layout']}**.")
        lines.append(f"- Linux layout: `keyboards/linux/hl_{family['key']}`, the XKB symbols of **{family['layout']}**.")
    lines += [
        f"- Keyboard grid: [keyboard.png]({MIRROR}/specimens/{family['specimens']}/keyboard.png), every key beside its glyph in each face.",
        "",
        "## Layout",
        "",
    ]
    lines += [f"- {text}" for text in family["scheme"]]
    if not zethu:
        lines += [
            f"- In Emacs, Option has no key: Option+x is typed {md_code(kk.OPTION_PREFIX)} and then the key x types, "
            "so Option+E is "
            f"{md_code(kk.OPTION_PREFIX + 'e')} and Option+Shift+E is {md_code(kk.OPTION_PREFIX + 'E')}.",
        ]
    lines += ["", "## Keys", ""]
    if zethu:
        lines += ["| Sign id | Code point | Glyph |", "| --- | --- | --- |"]
        lines += [f"| {md_code(r['key'])} | {r['codepoint']} | {r['glyph']} |" for r in table]
    else:
        lines += ["| Key | Emacs | Code point | Glyph | Kind |", "| --- | --- | --- | --- | --- |"]
        lines += [
            f"| {r['key']} | {md_code(kk.quail_sequence(r['key']))} | {r['codepoint']} | {r['glyph']} | {r['kind']} |"
            for r in table
        ]
    return "\n".join(lines) + "\n"


def write_cheatsheets(out: Path, tables: dict[str, list[dict]]) -> list[Path]:
    written = []
    for family in FAMILIES:
        path = out / f"{family['key']}.md"
        path.write_text(cheatsheet(family, tables[family["key"]]), encoding="utf-8")
        written.append(path)
    return written


def ink_box(renderer: Renderer, glyph: str) -> tuple[float, float, float, float] | None:
    gid = renderer.order.index(glyph)
    points = [p for _, pts in renderer.contours(gid) for p in pts]
    if not points:
        return None
    xs, ys = [p[0] for p in points], [p[1] for p in points]
    return min(xs), min(ys), max(xs), max(ys)


def sheet(family: dict, entries: list[dict], table: list[dict]) -> tuple[Image.Image, int]:
    zethu = family["layout"] is None
    renderers = {}
    for entry in entries:
        ttf = ROOT / entry["files"]["ttf"]
        renderers[entry["name"]] = (Renderer(ttf), TTFont(str(ttf)).getBestCmap())
    # The glyph size: a face's em, or for signs the size at which the tallest sign fits.
    size = float(GLYPH_PX)
    if zethu:
        renderer, _ = renderers[entries[0]["name"]]
        extent = max(
            max(b[2] - b[0], b[3] - b[1])
            for r in table
            if (b := ink_box(renderer, r["glyph"])) is not None
        )
        size = GLYPH_PX * renderer.upem / extent

    cell_w = max(112, SLOT * len(entries) + 16)
    columns = max(1, (SHEET_W - 2 * MARGIN) // cell_w)
    if zethu:
        groups = [("Sign id", sorted(table, key=lambda r: r["key"]))]
    else:
        groups = []
        for name in kk.LAYERS:
            rows = [r for r in table if kk.layer(r["key"]) == name]
            rows.sort(key=lambda r: kk.KEY_ORDER.index(kk.parse(r["key"])[2]))
            if rows:
                groups.append((LAYER_TITLES[name], rows))
    height = MARGIN * 2 + sum(TITLE_H + CELL_H * -(-len(rows) // columns) for _, rows in groups)
    img = Image.new("RGB", (MARGIN * 2 + cell_w * columns, height), PAPER)
    draw = ImageDraw.Draw(img)
    heading, small, tiny = label_font(22), label_font(15), label_font(12)
    drawn = 0
    y = MARGIN
    for title, rows in groups:
        draw.text((MARGIN, y + 8), title, font=heading, fill=INK)
        y += TITLE_H
        for index, row in enumerate(rows):
            col, line = index % columns, index // columns
            x0, y0 = MARGIN + col * cell_w, y + line * CELL_H
            draw.rectangle([x0, y0, x0 + cell_w - 8, y0 + CELL_H - 8], outline=RULE)
            draw.text((x0 + 8, y0 + 6), row["key"], font=small, fill=INK)
            for slot, entry in enumerate(entries):
                renderer, cmap = renderers[entry["name"]]
                assert cmap.get(code(row)) == row["glyph"], (
                    f"{entry['name']}: {row['codepoint']} maps to {cmap.get(code(row))}, not {row['glyph']}"
                )
                gid = renderer.order.index(row["glyph"])
                advance = renderer.tt["hmtx"][row["glyph"]][0]
                scale = size / renderer.upem
                box = ink_box(renderer, row["glyph"])
                sx = x0 + 8 + slot * SLOT
                if zethu:
                    baseline = y0 + 30 + GLYPH_PX / 2
                    if box:
                        offset = sx + SLOT / 2 - (box[0] + box[2]) * scale / 2
                        baseline = y0 + 30 + GLYPH_PX / 2 + (box[1] + box[3]) * scale / 2
                    else:
                        offset = sx
                else:
                    baseline = y0 + 30 + GLYPH_PX * 0.8
                    if advance:
                        offset = sx + SLOT / 2 - advance * scale / 2
                    elif box:
                        offset = sx + SLOT / 2 - (box[0] + box[2]) * scale / 2
                    else:
                        offset = sx
                span = (sx, y0 + 26, sx + SLOT, y0 + 30 + GLYPH_PX + 16)
                before = img.crop(span).tobytes()
                renderer.draw(img, offset, baseline, Shaped([(gid, 0, 0, advance)], advance), size, INK)
                inked = img.crop(span).tobytes() != before
                assert inked == (box is not None), (
                    f"{entry['name']}: {row['glyph']} {'left no ink' if box else 'drew ink'}"
                )
            draw.text((x0 + 8, y0 + CELL_H - 28), row["glyph"], font=tiny, fill=GREY)
            drawn += 1
        y += CELL_H * -(-len(rows) // columns)
    assert drawn == len(table), f"{family['key']}: {drawn} cells for {len(table)} characters"
    return img, drawn


def write_sheets(tables_and_entries: dict, specimens: Path) -> list[Path]:
    written = []
    for family in FAMILIES:
        entries, table = tables_and_entries[family["key"]]
        img, _ = sheet(family, entries, table)
        path = specimens / family["specimens"] / "keyboard.png"
        path.parent.mkdir(parents=True, exist_ok=True)
        img.save(path, optimize=True)
        written.append(path)
    return written


def main() -> None:
    faces = {f["name"]: f for f in manifest()["families"]}
    found = {}
    for family in FAMILIES:
        found[family["key"]] = family_faces(family, faces)
        keys = [r["key"] for r in found[family["key"]][1]]
        assert len(set(keys)) == len(keys), f"{family['key']}: a key is used twice"
    tables = {k: v[1] for k, v in found.items()}
    out = ROOT / "keyboards"
    written = write_macos(out, tables) + write_windows(out, tables) + write_linux(out, tables)
    written += write_emacs(out, tables) + write_cheatsheets(out, tables)
    written += write_sheets(found, ROOT / "specimens")
    for path in written:
        print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
