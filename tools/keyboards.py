# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Write the keyboard layouts, Emacs input methods and cheatsheets.

    .venv/bin/python tools/keyboards.py

The layouts type by sound. tools/sound_keys.json puts every sound of the spelling
guide on one key or chord, the same in every script, and keyboards/sounds.json
(written by tools/sounds.mjs from thalorna's mapping notes) gives what each sound is
in each script. A layout's key types its sound's output, as many code points as the
mapping writes; a key whose sound the mapping cannot spell, and a key that carries no
sound, types nothing. No key types a roman letter.

- ``keyboards/macos/HeroicLands.bundle``: HL Semaron, HL Pirzath, HL Thuravark and
  HL Qalezu as macOS ``.keylayout`` files. Command and Control chords type the US
  keys, so shortcuts keep working.
- ``keyboards/windows/<script>.klc``: the Microsoft Keyboard Layout Creator source
  of each layout. Option is AltGr. Every output is a ligature entry of UTF-16 code
  units, a character outside the Basic Multilingual Plane being its surrogate pair;
  MSKLC refuses a ligature of more than four code units, so a longer output leaves
  its key empty on Windows.
- ``keyboards/linux/hl_<script>``: one XKB symbols file per layout. Option is the
  third level. An XKB key types one keysym, so a sound written with more than one
  code point leaves its key empty on Linux.
- ``keyboards/emacs/heroiclands-<script>.el``: one Quail input method per layout, and
  ``heroiclands-zethu.el``, Khelathi Zethu Glyphs typed by sign id. Option has no
  Emacs key, so Option+x is typed as ``\\`` and then the character that x types.
- ``keyboards/keyboard.svg`` and ``keyboard.png``: the shared key map on an ANSI
  keyboard, every key's sound on each layer.
- ``keyboards/index.md``: the cheatsheet, with the diagram and a table of every key,
  its sound and each script's output: glyphs, code points and character names.
- ``keyboards/<script>.md``: one script's layout and table; ``zethu.md`` lists the
  sign ids.
"""

import html
import json
import plistlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import keyboard_keys as kk  # noqa: E402
from charts import rasterize  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "keyboards"
BUNDLE = "HeroicLands.bundle"
BUNDLE_ID = "org.heroiclands.keyboardlayout"

# The scripts typed by sound, in the order of sounds.json. ``chart`` is the charts/ folder
# whose glyph images the cheatsheet shows.
SCRIPTS = [
    {"key": "semaron", "title": "Semaron", "faces": ["Semaron Kuriale"], "chart": "semaron-kuriale",
     "layout": "HL Semaron", "klc": "hlsemaro", "id": -26101},
    {"key": "pirzath", "title": "Pirzath", "faces": ["Pirzath Carved", "Pirzath Hand", "Pirzath Hand Lifted"],
     "chart": "pirzath", "layout": "HL Pirzath", "klc": "hlpirzat", "id": -26102},
    {"key": "thuravark", "title": "Thuravark", "faces": ["Thuravark Carved"], "chart": "thuravark-carved",
     "layout": "HL Thuravark", "klc": "hlthurav", "id": -26103},
    {"key": "qalezu", "title": "Qalezu", "faces": ["Qalezu Hand"], "chart": "qalezu-hand",
     "layout": "HL Qalezu", "klc": "hlqalezu", "id": -26104},
]  # fmt: skip
ZETHU = {"key": "zethu", "title": "Zethu", "faces": ["Khelathi Zethu Glyphs"]}
PLATFORMS = ["macos", "windows", "linux", "emacs"]
PLATFORM_TITLES = {"macos": "macOS", "windows": "Windows", "linux": "Linux", "emacs": "Emacs"}
WINDOWS_UNITS = 4  # MSKLC's limit on a ligature, in UTF-16 code units


def manifest() -> dict:
    return json.loads((ROOT / "fonts.json").read_text(encoding="utf-8"))


def sounds_table() -> list[dict]:
    return json.loads((OUT / "sounds.json").read_text(encoding="utf-8"))["sounds"]


def points(text: str) -> list[int]:
    return [int(p[2:], 16) for p in text.split()]


def units(cps: list[int]) -> int:
    return sum(2 if p > 0xFFFF else 1 for p in cps)


def carries(platform: str, cps: list[int]) -> bool:
    """Whether a platform's layout can type the code points from one key."""
    if platform == "windows":
        return units(cps) <= WINDOWS_UNITS
    if platform == "linux":
        return len(cps) == 1
    return True


def why_not(platform: str, cps: list[int]) -> str:
    if platform == "windows":
        return f"{units(cps)} UTF-16 code units; an MSKLC ligature holds {WINDOWS_UNITS}"
    return f"{len(cps)} code points; an XKB key types one"


def outputs(script: str, keymap: list[dict], sounds: list[dict]) -> dict[str, list[int]]:
    """key -> the code points it types in a script, for every key whose sound the script spells."""
    by_sound = {s["sound"]: s for s in sounds}
    out = {}
    for entry in keymap:
        result = by_sound[entry["sound"]]["scripts"][script]
        if "codepoints" in result:
            out[entry["key"]] = points(result["codepoints"])
    return out


def platform_keys(script: str, platform: str, keymap: list[dict], sounds: list[dict]) -> dict[str, list[int]]:
    return {k: cps for k, cps in outputs(script, keymap, sounds).items() if carries(platform, cps)}


def code_list(cps: list[int]) -> str:
    return " ".join(f"U+{p:04X}" for p in cps)


# -- macOS --------------------------------------------------------------------------------

CONTROL_KEYS = {
    36: 0x0D, 48: 0x09, 49: 0x20, 51: 0x08, 52: 0x03, 53: 0x1B, 76: 0x03, 115: 0x01, 116: 0x0B,
    117: 0x7F, 119: 0x04, 121: 0x0C, 123: 0x1C, 124: 0x1D, 125: 0x1F, 126: 0x1E,
}  # fmt: skip
LAYER_INDEX = {"": 0, "shift": 1, "option": 2, "option+shift": 3}


def ref(text: str) -> str:
    """Numeric character references for every character, so no escaping is needed."""
    return "".join(f"&#x{ord(c):04X};" for c in text)


def keylayout(script: dict, keys: dict[str, list[int]]) -> str:
    # 0-3: the four sound layers; 4 and 5: the US keys, for Command and Control chords.
    maps: list[dict[int, str]] = [{} for _ in range(6)]
    for key, cps in keys.items():
        shift, option, base = kk.parse(key)
        maps[int(shift) + 2 * int(option)][kk.MAC_CODES[base]] = "".join(map(chr, cps))
    for base in kk.BASE_KEYS:
        maps[4][kk.MAC_CODES[base]] = base
        maps[5][kk.MAC_CODES[base]] = kk.SHIFTED[base]
    for m in maps:
        m.update({k: chr(v) for k, v in CONTROL_KEYS.items()})
    maxout = max(len(c.encode("utf-16-le")) // 2 for m in maps for c in m.values())
    selects = [
        (0, [""]),
        (1, ["anyShift", "caps", "anyShift caps"]),
        (2, ["anyOption", "anyOption caps"]),
        (3, ["anyShift anyOption", "anyShift anyOption caps"]),
        (4, ["command", "control", "command control", "command anyOption", "control anyOption", "caps command", "caps control"]),
        (5, ["anyShift command", "anyShift control", "anyShift command control", "anyShift command anyOption"]),
    ]
    out = [
        '<?xml version="1.1" encoding="UTF-8"?>',
        '<!DOCTYPE keyboard SYSTEM "file://localhost/System/Library/DTDs/KeyboardLayout.dtd">',
        f'<keyboard group="126" id="{script["id"]}" name="{script["layout"]}" maxout="{maxout}">',
        "    <layouts>",
        '        <layout first="0" last="255" modifiers="Modifiers" mapSet="Keys"/>',
        "    </layouts>",
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


def info_plist() -> bytes:
    version = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))["version"]
    plist = {
        "CFBundleIdentifier": f"{BUNDLE_ID}.fonts",
        "CFBundleName": "HeroicLands",
        "CFBundlePackageType": "BNDL",
        "CFBundleShortVersionString": version,
        "CFBundleVersion": version,
    }
    for script in SCRIPTS:
        plist[f"KLInfo_{script['layout']}"] = {
            "TISInputSourceID": f"{BUNDLE_ID}.{script['key']}",
            "TISIntendedLanguage": "en",
        }
    return plistlib.dumps(plist, sort_keys=False)


def write_macos(layouts: dict[str, dict]) -> list[Path]:
    resources = OUT / "macos" / BUNDLE / "Contents" / "Resources"
    resources.mkdir(parents=True, exist_ok=True)
    path = OUT / "macos" / BUNDLE / "Contents" / "Info.plist"
    path.write_bytes(info_plist())
    written = [path]
    for script in SCRIPTS:
        path = resources / f"{script['layout']}.keylayout"
        path.write_text(keylayout(script, layouts[script["key"]]["macos"]), encoding="utf-8")
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


def by_layer(keys: dict[str, list[int]]) -> dict[tuple[int, str], list[int]]:
    """(layer, base key) -> code points, with layer 0 plain, 1 Shift, 2 Option and 3 Option+Shift."""
    out = {}
    for key, cps in keys.items():
        shift, option, base = kk.parse(key)
        out[(int(shift) + 2 * int(option), base)] = cps
    return out


def surrogates(point: int) -> tuple[int, int]:
    point -= 0x10000
    return 0xD800 + (point >> 10), 0xDC00 + (point & 0x3FF)


def utf16(cps: list[int]) -> list[int]:
    return [u for p in cps for u in ([p] if p < 0x10000 else surrogates(p))]


def klc(script: dict, keys: dict[str, list[int]]) -> str:
    typed = by_layer(keys)
    rows, ligatures = [], []
    for base in sorted(WIN_KEYS, key=lambda b: WIN_KEYS[b][0]):
        sc, vk = WIN_KEYS[base]
        cells = []
        for state, layer in WIN_STATES:
            if layer is None:
                ctrl = WIN_CTRL.get(base)
                cells.append("-1" if ctrl is None else f"{ctrl:04x}")
            elif (layer, base) in typed:
                cells.append("%%")
                ligatures.append((vk, state, utf16(typed[(layer, base)])))
            else:
                cells.append("-1")
        rows.append(f"{sc:02x}\t{vk}\t\t0\t" + "\t".join(cells))
    rows.append("39\tSPACE\t\t0\t0020\t0020\t0020\t-1\t-1")
    name = script["layout"]
    out = [
        f'KBD\t{script["klc"]}\t"{name}"',
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
    for vk, state, code_units in ligatures:
        out.append(f"{vk}\t{state}\t" + "\t".join(f"{u:04x}" for u in code_units))
    out += ["", "DESCRIPTIONS", "", f"0409\t{name}", "", "LANGUAGENAMES", "", "0409\tEnglish (United States)", "", "ENDKBD", ""]
    return "\r\n".join(out)


def write_windows(layouts: dict[str, dict]) -> list[Path]:
    folder = OUT / "windows"
    folder.mkdir(parents=True, exist_ok=True)
    written = []
    for script in SCRIPTS:
        path = folder / f"{script['key']}.klc"
        # MSKLC reads a Unicode text file: UTF-16, little endian, with a byte order mark.
        path.write_bytes(b"\xff\xfe" + klc(script, layouts[script["key"]]["windows"]).encode("utf-16-le"))
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


def xkb(script: dict, keys: dict[str, list[int]]) -> str:
    typed = by_layer(keys)
    lines = [
        f"// {script['layout']}: type {script['title']} by sound, with the same keys as the macOS layout.",
        "// Generated by tools/keyboards.py. Option is the third level, reached with the",
        "// right Alt key. A key with no sound in this script types nothing (VoidSymbol).",
        "default partial alphanumeric_keys",
        'xkb_symbols "basic" {',
        '    include "us(basic)"',
        '    include "level3(ralt_switch)"',
        f'    name[Group1] = "{script["layout"]}";',
        "",
    ]
    for base in sorted(XKB_KEYS, key=lambda b: kk.KEY_ORDER.index(b)):
        symbols = [f"U{typed[(layer, base)][0]:X}" if (layer, base) in typed else "VoidSymbol" for layer in range(4)]
        lines.append(f'    key <{XKB_KEYS[base]}> {{ type[Group1] = "FOUR_LEVEL", symbols[Group1] = [ {", ".join(symbols)} ] }};')
    lines += ["};", ""]
    return "\n".join(lines)


def write_linux(layouts: dict[str, dict]) -> list[Path]:
    folder = OUT / "linux"
    folder.mkdir(parents=True, exist_ok=True)
    written = []
    for script in SCRIPTS:
        path = folder / f"hl_{script['key']}"
        path.write_text(xkb(script, layouts[script["key"]]["linux"]), encoding="utf-8")
        written.append(path)
    return written


# -- Emacs --------------------------------------------------------------------------------


def lisp(text: str) -> str:
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


def lisp_chars(cps: list[int]) -> str:
    """A Lisp string of the code points, each written as a ``\\U`` escape."""
    return '"' + "".join(f"\\U{p:08X}" for p in cps) + '"'


def translation(cps: list[int] | None) -> str:
    """A Quail translation: one character, a vector holding one string (the whole string is
    the one candidate), or an empty string, so that the key types nothing."""
    if not cps:
        return '[""]'
    if len(cps) == 1:
        return f"#x{cps[0]:X}"
    return f"[{lisp_chars(cps)}]"


def quail_rules(keys: dict[str, list[int]]) -> list[tuple[str, list[int] | None]]:
    """Every key sequence of the four layers with what it types, and the Option prefix
    alone, which types nothing."""
    rules = [(kk.OPTION_PREFIX, None)]
    for key in kk.every_key():
        rules.append((kk.quail_sequence(key), keys.get(key)))
    return rules


def emacs_header(name: str, title: str, doc: list[str], what: str) -> list[str]:
    return [
        f";;; {name}.el --- Type {title} with Quail  -*- lexical-binding: t; -*-",
        "",
        ';; Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>',
        ";; SPDX-License-Identifier: OFL-1.1",
        "",
        ";;; Commentary:",
        "",
        f";; {what}",
        ";; Generated by tools/keyboards.py. Put this directory on `load-path',",
        f";; evaluate (require '{name}), then M-x set-input-method.",
        "",
        ";;; Code:",
        "",
        "(require 'quail)",
        "",
        "(quail-define-package",
        f" {lisp(name)} {lisp(title)} {lisp('HL-' + title[:3])} t",
        f" {lisp(chr(10).join(doc))}",
        " nil t nil nil nil nil nil nil nil nil t)",
        "",
    ]


def emacs_method(script: dict, keys: dict[str, list[int]]) -> str:
    name = f"heroiclands-{script['key']}"
    doc = [
        f"Type {', '.join(script['faces'])} by sound, with the same keys as the {script['layout']} layout.",
        "Each key types its sound in the script, and a key whose sound the script",
        f"does not write types nothing. Option has no Emacs key: Option+x is {kk.OPTION_PREFIX} and",
        "then the key that x types, so Option+t (th) is \\t and Option+Shift+t (Th) is \\T.",
        "The cheatsheet keyboards/index.md lists every key.",
    ]
    rules = "\n".join(f" ({lisp(seq)} {translation(cps)})" for seq, cps in quail_rules(keys))
    body = emacs_header(name, script["title"], doc, f"A sound input method for {', '.join(script['faces'])}.")
    body += ["(quail-define-rules", rules + ")", "", f"(provide '{name})", "", f";;; {name}.el ends here"]
    return "\n".join(body) + "\n"


def zethu_method(table: list[dict]) -> str:
    name = "heroiclands-zethu"
    doc = [
        "Type Khelathi Zethu Glyphs by sign id: 08-001 inserts that sign. Every id has the",
        "form two digits, a hyphen and three digits.",
        "The cheatsheet keyboards/zethu.md lists every sign.",
    ]
    rules = "\n".join(f" ({lisp(r['key'])} #x{int(r['codepoint'][2:], 16):X})" for r in table)
    body = emacs_header(name, ZETHU["title"], doc, "An input method for the code points of Khelathi Zethu Glyphs.")
    body += ["(quail-define-rules", rules + ")", "", f"(provide '{name})", "", f";;; {name}.el ends here"]
    return "\n".join(body) + "\n"


def write_emacs(layouts: dict[str, dict], zethu: list[dict]) -> list[Path]:
    folder = OUT / "emacs"
    folder.mkdir(parents=True, exist_ok=True)
    written = []
    for script in SCRIPTS:
        path = folder / f"heroiclands-{script['key']}.el"
        path.write_text(emacs_method(script, layouts[script["key"]]["emacs"]), encoding="utf-8")
        written.append(path)
    path = folder / "heroiclands-zethu.el"
    path.write_text(zethu_method(zethu), encoding="utf-8")
    return written + [path]


# -- The keyboard diagram ------------------------------------------------------------------

UNIT = 74
GAP = 6
PAD = 20
TITLE_H = 74
LEGEND_H = 40
SANS = "Helvetica, Arial, sans-serif"
INK, GREY, OPTION, KEYFACE, KEYEDGE = "#161412", "#8a847b", "#1f5fa8", "#ffffff", "#7a756d"
SHORT = {"catch": "'", "stop": ".", "pause": ",", "open quote": "“", "close quote": "”",
         "ten": "10", "eleven": "11", "twelve": "12", "thirteen": "13", "fourteen": "14", "fifteen": "15"}  # fmt: skip

# The ANSI rows: (base key or a label, width in units).
ROWS = [
    [*[(k, 1) for k in "`1234567890-="], ("delete", 2)],
    [("tab", 1.5), *[(k, 1) for k in "qwertyuiop[]"], ("\\", 1.5)],
    [("caps lock", 1.75), *[(k, 1) for k in "asdfghjkl;'"], ("return", 2.25)],
    [("shift", 2.25), *[(k, 1) for k in "zxcvbnm,./"], ("shift", 2.75)],
    [("control", 1.25), ("option", 1.25), ("command", 1.25), ("space", 6.25), ("command", 1.25), ("option", 1.25), ("", 1.25), ("control", 1.25)],
]  # fmt: skip


def label(entry: dict) -> str:
    return SHORT.get(entry["sound"], entry["sound"])


def text(x: float, y: float, s: str, size: int, fill: str, anchor: str = "start", weight: str = "normal") -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="{SANS}" font-size="{size}" font-weight="{weight}" '
        f'text-anchor="{anchor}" fill="{fill}">{html.escape(s)}</text>'
    )


def diagram_svg(keymap: list[dict]) -> str:
    on = {e["key"]: e for e in keymap}
    width = int(PAD * 2 + 15 * UNIT)
    height = int(PAD * 2 + TITLE_H + 5 * UNIT + LEGEND_H)
    o = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        "<title>Sound keys of HL Semaron, HL Pirzath, HL Thuravark and HL Qalezu</title>",
        f'<rect width="{width}" height="{height}" fill="#ffffff"/>',
        text(PAD, PAD + 24, "Sound keys", 24, INK),
        text(PAD, PAD + 50, "Each key types the same sound in HL Semaron, HL Pirzath, HL Thuravark and HL Qalezu, "
             "in that script's own letters.", 15, GREY),
    ]  # fmt: skip
    y = PAD + TITLE_H
    for row in ROWS:
        x = PAD
        for name, w in row:
            kw, kh = w * UNIT - GAP, UNIT - GAP
            o.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{kw:.1f}" height="{kh:.1f}" rx="7" fill="{KEYFACE}" stroke="{KEYEDGE}" stroke-width="1.2"/>')
            if name in kk.BASE_KEYS and len(name) == 1:
                o.append(text(x + kw / 2, y + kh / 2 + 5, name, 13, GREY, "middle"))
                corners = [
                    ("", x + 8, y + kh - 10, "start", INK),
                    ("shift", x + 8, y + 22, "start", INK),
                    ("option", x + kw - 8, y + kh - 10, "end", OPTION),
                    ("option+shift", x + kw - 8, y + 22, "end", OPTION),
                ]
                for layer, cx, cy, anchor, fill in corners:
                    key = (layer + "+" if layer else "") + name
                    if key in on:
                        o.append(text(cx, cy, label(on[key]), 18, fill, anchor, "bold"))
            elif name:
                o.append(text(x + 9, y + kh - 11, name, 12, GREY))
            x += w * UNIT
        y += UNIT
    legend = [
        (INK, "bottom left: the key", "top left: with Shift"),
        (OPTION, "bottom right: with Option (AltGr; \\ then the key in Emacs)", "top right: with Option+Shift"),
    ]
    lx = PAD
    for fill, a, b in legend:
        o.append(text(lx, y + 24, f"{a} · {b}", 14, fill))
        lx += 15 * UNIT / 2 - 40
    o.append("</svg>")
    return "\n".join(o) + "\n"


def write_diagram(keymap: list[dict]) -> list[Path]:
    svg = OUT / "keyboard.svg"
    svg.write_text(diagram_svg(keymap), encoding="utf-8")
    png = svg.with_suffix(".png")
    rasterize(svg, png)
    return [svg, png]


# -- Cheatsheets --------------------------------------------------------------------------


def md_code(s: str) -> str:
    s = s.replace("|", "\\|")
    if "`" in s:
        return f"`` {s} ``"
    return f"`{s}`"


def glyph_cells(script: dict, cps: list[int], names: dict[int, str]) -> tuple[str, str, str]:
    """The glyph images, code points and character names of an output."""
    images = []
    for p in cps:
        path = ROOT / "charts" / script["chart"] / "glyphs" / f"U+{p:04X}.svg"
        assert path.exists(), f"{script['key']}: U+{p:04X} has no glyph image at {path.relative_to(ROOT)}"
        images.append(f"![U+{p:04X}](../charts/{script['chart']}/glyphs/U+{p:04X}.svg)")
    named = [names[p] for p in cps if p in names]
    return " ".join(images), code_list(cps), "; ".join(named) if len(named) == len(cps) else ""


def none_cell(reason: str) -> str:
    return "none: the mapping " + ("has no row for it" if reason == "no row" else "writes it as nothing")


def gaps(keymap: list[dict], sounds: list[dict]) -> list[tuple[dict, dict, str, str]]:
    """(key map entry, script, platform, why) for every output a platform cannot carry."""
    out = []
    for script in SCRIPTS:
        for key, cps in outputs(script["key"], keymap, sounds).items():
            entry = next(e for e in keymap if e["key"] == key)
            for platform in PLATFORMS:
                if not carries(platform, cps):
                    out.append((entry, script, platform, why_not(platform, cps)))
    return out


def gap_table(rows: list[tuple[dict, dict, str, str]]) -> list[str]:
    if not rows:
        return ["Every platform carries every output."]
    lines = ["| Key | Sound | Script | Platform | Why |", "| --- | --- | --- | --- | --- |"]
    for entry, script, platform, why in rows:
        lines.append(f"| {md_code(entry['key'])} | {md_code(entry['sound'])} | {script['title']} | {PLATFORM_TITLES[platform]} | {why} |")
    return lines


def name_tables(faces: dict) -> dict[str, dict[int, str]]:
    return {
        s["key"]: {int(r["codepoint"][2:], 16): r["name"] for r in faces[s["faces"][0]]["codepoints"] if "name" in r}
        for s in SCRIPTS
    }


def index_sheet(keymap: list[dict], sounds: list[dict], principles: list[str], names: dict) -> str:
    by_sound = {s["sound"]: s for s in sounds}
    lines = [
        "# Sound keys",
        "",
        "HL Semaron, HL Pirzath, HL Thuravark and HL Qalezu type by sound. Every sound of the spelling guide, "
        "_Pronouncing Thalorna_, sits on one key or chord, the same in every script, and the key types that "
        "script's own characters for the sound, as many as its mapping note spells it with. A key whose sound "
        "a script does not write types nothing in that script, and no key types a roman letter. The README's "
        "\"Typing in the fonts\" says how to install the layouts.",
        "",
        "![The sound keys on an ANSI keyboard](keyboard.png)",
        "",
        "## The key map",
        "",
        *[f"- {p}" for p in principles],
        "",
        "## Keys a platform cannot carry",
        "",
        "Where a platform cannot type a sound's output from one key, the key types nothing on that platform alone.",
        "",
        *gap_table(gaps(keymap, sounds)),
        "",
        "## Keys",
        "",
        "Emacs types Option+x as `\\` and then the character x types. Glyphs and code points are in typing order. "
        "Character names come from `tools/names/`, and a script without a name table there has none yet.",
        "",
    ]
    head = ["Key", "Emacs", "Sound"]
    for s in SCRIPTS:
        head += [s["title"], f"{s['title']} code points", f"{s['title']} names"]
    lines += ["| " + " | ".join(head) + " |", "| " + " | ".join("---" for _ in head) + " |"]
    for entry in keymap:
        cells = [md_code(entry["key"]), md_code(kk.quail_sequence(entry["key"])), md_code(entry["sound"])]
        for s in SCRIPTS:
            result = by_sound[entry["sound"]]["scripts"][s["key"]]
            if "codepoints" in result:
                cells += glyph_cells(s, points(result["codepoints"]), names[s["key"]])
            else:
                cells += ["", none_cell(result["unmapped"]), ""]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines) + "\n"


def script_sheet(script: dict, keymap: list[dict], sounds: list[dict], names: dict) -> str:
    by_sound = {s["sound"]: s for s in sounds}
    k = script["key"]
    lines = [
        f"# {script['title']} keyboard",
        "",
        f"{script['layout']} types {', '.join(script['faces'])} by sound. The keys are the shared sound keys of "
        "[the cheatsheet](index.md), which draws them on a keyboard and gives their principles; this sheet "
        f"lists what each key types in {script['title']}.",
        "",
        f"- macOS layout: `keyboards/macos/{BUNDLE}`, input source **{script['layout']}**.",
        f"- Windows layout: `keyboards/windows/{k}.klc`, the Microsoft Keyboard Layout Creator source of **{script['layout']}**.",
        f"- Linux layout: `keyboards/linux/hl_{k}`, the XKB symbols of **{script['layout']}**.",
        f"- Emacs input method: `keyboards/emacs/heroiclands-{k}.el`, named `heroiclands-{k}`.",
        "",
        "## Keys a platform cannot carry",
        "",
        *gap_table([g for g in gaps(keymap, sounds) if g[1] is script]),
        "",
        "## Keys",
        "",
        "| Key | Emacs | Sound | Glyphs | Code points | Names |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for entry in keymap:
        result = by_sound[entry["sound"]]["scripts"][k]
        if "codepoints" in result:
            cells = glyph_cells(script, points(result["codepoints"]), names[k])
        else:
            cells = ("", none_cell(result["unmapped"]), "")
        lines.append(f"| {md_code(entry['key'])} | {md_code(kk.quail_sequence(entry['key']))} | {md_code(entry['sound'])} | " + " | ".join(cells) + " |")
    return "\n".join(lines) + "\n"


def zethu_sheet(table: list[dict]) -> str:
    lines = [
        "# Zethu keyboard",
        "",
        "Faces: Khelathi Zethu Glyphs. The signs far outnumber the keys of a keyboard, so there is no macOS, "
        "Windows or Linux layout.",
        "",
        "- Emacs input method: `keyboards/emacs/heroiclands-zethu.el`, named `heroiclands-zethu`, typed by sign id, such as `08-001`.",
        "",
        "## Keys",
        "",
        "| Sign id | Code point | Glyph |",
        "| --- | --- | --- |",
    ]
    lines += [f"| {md_code(r['key'])} | {r['codepoint']} | {r['glyph']} |" for r in table]
    return "\n".join(lines) + "\n"


def write_cheatsheets(keymap: list[dict], sounds: list[dict], principles: list[str], faces: dict) -> list[Path]:
    names = name_tables(faces)
    written = []
    path = OUT / "index.md"
    path.write_text(index_sheet(keymap, sounds, principles, names), encoding="utf-8")
    written.append(path)
    for script in SCRIPTS:
        path = OUT / f"{script['key']}.md"
        path.write_text(script_sheet(script, keymap, sounds, names), encoding="utf-8")
        written.append(path)
    path = OUT / "zethu.md"
    path.write_text(zethu_sheet(faces[ZETHU["faces"][0]]["codepoints"]), encoding="utf-8")
    return written + [path]


def layouts_of(keymap: list[dict], sounds: list[dict]) -> dict[str, dict[str, dict[str, list[int]]]]:
    """script -> platform -> key -> the code points the key types there."""
    return {s["key"]: {p: platform_keys(s["key"], p, keymap, sounds) for p in PLATFORMS} for s in SCRIPTS}


def main() -> None:
    data = kk.load()
    keymap, sounds = data["sounds"], sounds_table()
    faces = {f["name"]: f for f in manifest()["families"]}
    layouts = layouts_of(keymap, sounds)
    written = write_macos(layouts) + write_windows(layouts) + write_linux(layouts)
    written += write_emacs(layouts, faces[ZETHU["faces"][0]]["codepoints"])
    written += write_diagram(keymap) + write_cheatsheets(keymap, sounds, data["principles"], faces)
    for path in written:
        print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
