# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Confirm that the sound layouts type what the encodings spell, and nothing else.

    .venv/bin/python tools/keyboards_guard.py [--encoding SCRIPT=FILE]

- **The key map.** Every key of tools/sound_keys.json is a key, no key or chord carries
  two sounds, a capital sits on Shift and the key of its small sound, the Emacs Option
  prefix carries no sound, the open and close quotes sit on Shift+, and Shift+., and
  keyboards/sounds.json lists exactly the key map's sounds with their spellings, so
  every sound has a key. The key map's markup lists every character Markdown and a
  span need, each on the key that types it on a US keyboard, and no key carries both
  a sound and markup. The key map's signs, the keys that are not sounds, each sit on a
  key no sound, markup or other sign carries, name a script with a layout, and type a
  code point that script's face draws.
- **The layouts.** The macOS, Windows, Linux and Emacs files of HL Semaron, HL Pirzath,
  HL Thuravark, HL Qalezu, HL Veldikko and HL Vedyakshara are read back. On each key each must type exactly the
  code points keyboards/sounds.json gives that key's sound in the script, or the sign
  the key map puts there for that script, or nothing
  where the script does not spell the sound or the platform cannot carry the output
  (tools/keyboards.py ``carries``), and no key but a key of markup may type a character
  below U+0080. Each key of markup types itself on every platform. The
  Khelathi Zethu Glyphs input method must type every sign on its sign id.
- **The cheatsheets.** keyboards/<script>.md, .svg and .png exist for every layout, and
  every key the macOS layout types has a row in the sheet's tables, with the code points
  the layout types, and a ``data-key`` entry on the printable keyboard picture. A script
  added to ``keyboards.SCRIPTS`` is covered with no change here.
- **The encodings.** keyboards/sounds.json is written afresh by tools/sounds.py from
  ``encodings/<script>.json`` (or the file ``--encoding SCRIPT=FILE`` names for a script)
  and must equal the committed file.
"""

import argparse
import html
import importlib.util
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import keyboard_keys as kk  # noqa: E402
import keyboards  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
KEYBOARDS = ROOT / "keyboards"
LAYERS = [(False, False), (True, False), (False, True), (True, True)]
SCRIPT_KEYS = [s["key"] for s in keyboards.SCRIPTS]

# The characters the key map must list as markup. # is not among them: Shift+3 is Pirzath's eleven,
# and a sound keeps its key.
MARKUP = list("*_[]{}()=:|\\~`")
# The keys of the quotes.
QUOTE_KEYS = {"open quote": "shift+,", "close quote": "shift+."}


# -- The key map ---------------------------------------------------------------------------


def keymap_problems(keymap: list[dict], sounds: list[dict]) -> list[str]:
    problems = []
    owner: dict[str, str] = {}
    by_sound = {e["sound"]: e for e in keymap}
    for entry in keymap:
        key, sound = entry["key"], entry["sound"]
        if kk.parse(key) is None:
            problems.append(f"tools/sound_keys.json: error: {sound}: {key!r} is not a key")
            continue
        if key in owner:
            problems.append(f"tools/sound_keys.json: error: {sound} and {owner[key]} both sit on {key}")
        owner.setdefault(key, sound)
        if kk.parse(key)[2] == "\\" and not kk.parse(key)[0]:
            problems.append(f"tools/sound_keys.json: error: {sound} sits on {key}, the Emacs Option prefix")
        small = entry.get("capital of")
        if small is not None:
            if small not in by_sound:
                problems.append(f"tools/sound_keys.json: error: {sound} is the capital of {small}, which has no key")
            else:
                shift, option, base = kk.parse(by_sound[small]["key"])
                if shift or kk.spell(True, option, base) != key:
                    problems.append(f"tools/sound_keys.json: error: {sound} sits on {key}, not on Shift and the key of {small}")
        elif any(c.isupper() for c in entry["spelling"]):
            problems.append(f"tools/sound_keys.json: error: {sound} is spelled {entry['spelling']!r}, a capital that names no small sound")
    for sound, key in QUOTE_KEYS.items():
        if sound in by_sound and by_sound[sound]["key"] != key:
            problems.append(f"tools/sound_keys.json: error: the {sound} sits on {by_sound[sound]['key']}, not {key}")
    problems += markup_problems(owner)
    problems += sign_problems(owner)
    listed = {s["sound"]: s["spelling"] for s in sounds}
    wanted = {e["sound"]: e["spelling"] for e in keymap}
    for sound in sorted(listed.keys() - wanted.keys()):
        problems.append(f"keyboards/sounds.json: error: {sound} has no key in tools/sound_keys.json")
    for sound in sorted(wanted.keys() - listed.keys()):
        problems.append(f"keyboards/sounds.json: error: {sound} of tools/sound_keys.json is missing; run tools/sounds.py --write")
    for sound in sorted(listed.keys() & wanted.keys()):
        if listed[sound] != wanted[sound]:
            problems.append(f"keyboards/sounds.json: error: {sound} is spelled {listed[sound]!r}, not {wanted[sound]!r}")
    for s in sounds:
        if set(s["scripts"]) != set(SCRIPT_KEYS):
            problems.append(f"keyboards/sounds.json: error: {s['sound']} lists the scripts {sorted(s['scripts'])}")
    return problems


def markup_problems(owner: dict[str, str]) -> list[str]:
    """Where the key map's markup misses a character, names one no key types, or shares a key with a sound."""
    problems = []
    listed = kk.load().get("markup", [])
    for char in MARKUP:
        if char not in listed:
            problems.append(f"tools/sound_keys.json: error: markup lacks {char}")
    for char in listed:
        key = kk.markup_key(char)
        if key is None:
            problems.append(f"tools/sound_keys.json: error: markup lists {char}, which no key of a US keyboard types")
        elif key in owner:
            problems.append(f"tools/sound_keys.json: error: markup lists {char}, on {key}, which carries the sound {owner[key]}")
    return problems


def unwritten(sound: str, script: str) -> bool:
    """Whether a script does not write a sound, so that its key types nothing there and a sign may sit on it."""
    entry = next((s for s in keyboards.sounds_table() if s["sound"] == sound), None)
    return entry is not None and "unmapped" in entry["scripts"].get(script, {})


def sign_problems(owner: dict[str, str]) -> list[str]:
    """Where a sign of the key map sits on a key that carries a sound, markup or another sign,
    names a script with no layout, or types a code point its face does not draw."""
    problems = []
    faces = {f["name"]: {r["codepoint"] for r in f["codepoints"] if "codepoint" in r} for f in keyboards.manifest()["families"]}
    seen: dict[tuple[str, str], str] = {}
    if tuple(kk.LAYOUT_SCRIPTS) != tuple(SCRIPT_KEYS):
        problems.append("tools/keyboard_keys.py: error: LAYOUT_SCRIPTS differs from keyboards.SCRIPTS")
    for sign in kk.signs():
        name, key = sign["sign"], sign["key"]
        script = next((s for s in keyboards.SCRIPTS if s["key"] == sign["script"]), None)
        if kk.parse(key) is None:
            problems.append(f"tools/sound_keys.json: error: the sign {name}: {key!r} is not a key")
            continue
        if script is None:
            problems.append(f"tools/sound_keys.json: error: the sign {name} names the script {sign['script']}, which has no layout")
        elif not sign.get("literal") and sign["codepoint"] not in faces.get(script["faces"][0], set()):
            problems.append(f"tools/sound_keys.json: error: the sign {name} types {sign['codepoint']}, which {script['faces'][0]} does not draw")
        if key in owner and not unwritten(owner[key], sign["script"]):
            problems.append(f"tools/sound_keys.json: error: the sign {name} sits on {key}, which carries the sound {owner[key]}")
        if key in kk.markup():
            problems.append(f"tools/sound_keys.json: error: the sign {name} sits on {key}, which types markup")
        if kk.parse(key)[2] == "\\":
            problems.append(f"tools/sound_keys.json: error: the sign {name} sits on {key}, the Emacs Option prefix")
        if (key, sign["script"]) in seen:
            problems.append(f"tools/sound_keys.json: error: the signs {name} and {seen[(key, sign['script'])]} both sit on {key}")
        seen.setdefault((key, sign["script"]), name)
    return problems


# -- Reading the layouts back --------------------------------------------------------------


def read_macos(text: str) -> dict[str, list[int]]:
    """key -> code points, for every main-block key of the four sound layers."""
    codes = {v: k for k, v in kk.MAC_CODES.items()}
    out = {}
    for index, body in re.findall(r'<keyMap index="(\d)">(.*?)</keyMap>', text, re.S):
        if int(index) > 3:
            continue
        shift, option = LAYERS[int(index)]
        for code, output in re.findall(r'<key code="(\d+)" output="([^"]*)"/>', body):
            base = codes.get(int(code))
            if base is not None:
                out[kk.spell(shift, option, base)] = [int(h, 16) for h in re.findall(r"&#x([0-9A-Fa-f]+);", output)]
    return out


def _join(code_units: list[int]) -> list[int]:
    text = b"".join(u.to_bytes(2, "little") for u in code_units).decode("utf-16-le")
    return [ord(c) for c in text]


def read_windows(data: bytes) -> dict[str, list[int]]:
    text = data.decode("utf-16").replace("\r\n", "\n")
    layout, ligatures = text.split("\nLIGATURE\n", 1)
    lig = {}
    for line in ligatures.split("\n"):
        parts = line.split("\t")
        if len(parts) >= 3 and not line.startswith("//") and re.fullmatch(r"[0-9a-f]{4}", parts[2]):
            lig[(parts[0], int(parts[1]))] = _join([int(p, 16) for p in parts[2:] if p])
    by_vk = {vk: base for base, (_, vk) in keyboards.WIN_KEYS.items()}
    out = {}
    for line in layout.split("\n"):
        parts = line.split("\t")
        if len(parts) < 9 or not re.fullmatch(r"[0-9a-f]{2}", parts[0]) or parts[1] not in by_vk:
            continue
        base = by_vk[parts[1]]
        for (state, layer), cell in zip(keyboards.WIN_STATES, parts[4:9]):
            if layer is None:
                continue
            shift, option = LAYERS[layer]
            if cell == "%%":
                out[kk.spell(shift, option, base)] = lig.get((parts[1], state), [])
            elif cell != "-1":
                out[kk.spell(shift, option, base)] = [int(cell, 16)]
    return out


KEYSYM_CHARS = {name: char for char, name in keyboards.KEYSYMS.items()}


def read_xkb(text: str) -> dict[str, list[int]]:
    by_name = {v: k for k, v in keyboards.XKB_KEYS.items()}
    out = {}
    for name, symbols in re.findall(r"key <(\w+)> \{.*?symbols\[Group1\] = \[ ([^\]]*) \] \};", text):
        for layer, symbol in enumerate(s.strip() for s in symbols.split(",")):
            if symbol == "VoidSymbol":
                continue
            shift, option = LAYERS[layer]
            cps = [int(symbol[1:], 16)] if re.fullmatch(r"U[0-9A-F]+", symbol) else [ord(KEYSYM_CHARS[symbol])]
            out[kk.spell(shift, option, by_name[name])] = cps
    return out


def read_emacs(text: str) -> dict[str, list[int]]:
    """quail sequence -> code points; a sequence that types nothing maps to []."""
    rules = text.split("(quail-define-rules", 1)[1]
    out = {}
    for seq, single, vector in re.findall(r'\("((?:[^"\\]|\\.)*)" (?:#x([0-9A-F]+)|\["((?:[^"\\]|\\.)*)"\])\)', rules):
        seq = re.sub(r"\\(.)", r"\1", seq)
        if single:
            out[seq] = [int(single, 16)]
        else:
            out[seq] = [int(h, 16) for h in re.findall(r"\\U([0-9A-F]{8})", vector)]
            if re.sub(r"\\U[0-9A-F]{8}", "", vector):
                out[seq] = [ord(c) for c in vector]
    return out


def read_layouts(key: str) -> dict[str, str | bytes]:
    texts = {"emacs": (KEYBOARDS / "emacs" / f"heroiclands-{key}.el").read_text(encoding="utf-8")}
    if key != "zethu":
        script = next(s for s in keyboards.SCRIPTS if s["key"] == key)
        base = KEYBOARDS / "macos" / keyboards.BUNDLE / "Contents" / "Resources"
        texts["macos"] = (base / keyboards.layout_file(script)).read_text(encoding="utf-8")
        texts["windows"] = (KEYBOARDS / "windows" / f"{key}.klc").read_bytes()
        texts["linux"] = (KEYBOARDS / "linux" / f"hl_{key}").read_text(encoding="utf-8")
    return texts


def read_back(texts: dict) -> dict[str, dict[str, list[int]]]:
    """platform -> key -> code points typed, with keys that type nothing left out."""
    got = {
        "macos": read_macos(texts["macos"]),
        "windows": read_windows(texts["windows"]),
        "linux": read_xkb(texts["linux"]),
    }
    emacs = read_emacs(texts["emacs"])
    # A key of markup with no rule is typed by Quail as itself; the backslash key always has its rule.
    markup = {k: [ord(c)] for k, c in kk.markup().items() if k != "\\"}
    got["emacs"] = {key: emacs[kk.quail_sequence(key)] for key in kk.every_key() if kk.quail_sequence(key) in emacs}
    missing = [k for k in kk.every_key() if kk.quail_sequence(k) not in emacs and k not in markup]
    got["emacs"].update({k: v for k, v in markup.items() if kk.quail_sequence(k) not in emacs})
    if missing or kk.OPTION_PREFIX not in emacs:
        got["emacs"]["(unruled)"] = missing or [kk.OPTION_PREFIX]
    return {p: {k: v for k, v in m.items() if v} for p, m in got.items()}


def layout_problems(script: str, keymap: list[dict], sounds: list[dict], texts: dict) -> list[str]:
    """Where a layout file disagrees with sounds.json, or types a roman character."""
    problems = []
    got = read_back(texts)
    for platform in keyboards.PLATFORMS:
        expected = keyboards.platform_keys(script, platform, keymap, sounds)
        typed = got[platform]
        if "(unruled)" in typed:
            problems.append(f"keyboards: error: {script}: the emacs input method leaves {', '.join(map(str, typed.pop('(unruled)')))} to type itself")
        for k in sorted(expected.keys() - typed.keys()):
            problems.append(f"keyboards: error: {script}: the {platform} layout types nothing on {k}, not {keyboards.code_list(expected[k])}")
        for k in sorted(typed.keys() - expected.keys()):
            problems.append(f"keyboards: error: {script}: the {platform} layout types {keyboards.code_list(typed[k])} on {k}, which carries nothing")
        for k in sorted(typed.keys() & expected.keys()):
            if typed[k] != expected[k]:
                problems.append(f"keyboards: error: {script}: the {platform} layout types {keyboards.code_list(typed[k])} on {k}, not {keyboards.code_list(expected[k])}")
        for k, cps in sorted(typed.items()):
            if any(p < 0x80 for p in cps) and k not in kk.markup():
                problems.append(f"keyboards: error: {script}: the {platform} layout types a roman character on {k}")
    return problems


CELL = re.compile(r"^\| (?:(`+) (.+?) \1|(`)([^`]+)`) \|")
IMAGE = re.compile(r"!\[[^\]]*\]\([^)]*\)")
ROW_CODES = re.compile(r"U\+[0-9A-F]{4,6}")


def read_cheatsheet(script: str) -> tuple[str, str]:
    return ((KEYBOARDS / f"{script}.md").read_text(encoding="utf-8"), (KEYBOARDS / f"{script}.svg").read_text(encoding="utf-8"))


def sheet_keys(sheet: str) -> dict[str, list[str]]:
    """key -> the code points of its row, for every table row whose first cell is a key."""
    out: dict[str, list[str]] = {}
    for line in sheet.splitlines():
        m = CELL.match(line)
        if m:
            key = (m.group(2) or m.group(4)).replace("\\|", "|")
            codes = ROW_CODES.findall(IMAGE.sub("", line))
            if codes or key not in out:
                out[key] = codes
    return out


def cheatsheet_problems(script: str, keymap: list[dict], sounds: list[dict], sheet: str, svg: str) -> list[str]:
    """Where a layout key has no entry on the script's cheatsheet, or the entry types something else."""
    problems = []
    typed = keyboards.platform_keys(script, "macos", keymap, sounds)
    rows = sheet_keys(sheet)
    pictured = {html.unescape(k) for k in re.findall(r'data-key="([^"]+)"', svg)}
    for key, cps in sorted(typed.items()):
        if key not in rows:
            problems.append(f"keyboards/{script}.md: error: the layout types {keyboards.code_list(cps)} on {key}, which has no row on the cheatsheet")
        elif key not in kk.markup() and rows[key] != [f"U+{p:04X}" for p in cps]:
            problems.append(f"keyboards/{script}.md: error: the row of {key} lists {' '.join(rows[key])}, not {keyboards.code_list(cps)}")
        if key not in pictured:
            problems.append(f"keyboards/{script}.svg: error: {key} is not on the printed keyboard")
    for key in sorted(pictured - typed.keys()):
        problems.append(f"keyboards/{script}.svg: error: {key} is on the printed keyboard but the layout types nothing there")
    if f"]({script}.png)" not in sheet:
        problems.append(f"keyboards/{script}.md: error: the sheet does not show {script}.png")
    if not (KEYBOARDS / f"{script}.png").exists():
        problems.append(f"keyboards/{script}.png: error: missing")
    return problems


def zethu_problems(table: list[dict]) -> list[str]:
    got = read_emacs(read_layouts("zethu")["emacs"])
    want = {r["key"]: [int(r["codepoint"][2:], 16)] for r in table if "key" in r}
    problems = [f"keyboards: error: zethu: the emacs input method has no rule for {k}" for k in sorted(want.keys() - got.keys())]
    problems += [f"keyboards: error: zethu: the emacs input method types {got[k]} on {k}, which is no sign" for k in sorted(got.keys() - want.keys())]
    problems += [f"keyboards: error: zethu: {k} types {got[k]}, not {want[k]}" for k in sorted(got.keys() & want.keys()) if got[k] != want[k]]
    return problems


def encoding_problems(committed: dict, files: dict[str, str] | None = None) -> list[str]:
    """Where keyboards/sounds.json differs from what the encodings spell."""
    sounds = load_module("sounds", ROOT / "tools" / "sounds.py")
    fresh = sounds.build(files)
    problems = []
    if fresh["source"] != committed["source"]:
        problems.append("keyboards/sounds.json: error: the encodings or their faces differ from the file's source")
    old = {s["sound"]: s for s in committed["sounds"]}
    for s in fresh["sounds"]:
        if s != old.get(s["sound"]):
            problems.append(f"keyboards/sounds.json: error: {s['sound']}: the encodings spell {json.dumps(s['scripts'], ensure_ascii=False)}")
    if [s["sound"] for s in fresh["sounds"]] != [s["sound"] for s in committed["sounds"]]:
        problems.append("keyboards/sounds.json: error: the sounds differ from tools/sound_keys.json's")
    return problems


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def committed_sounds() -> dict:
    return json.loads((KEYBOARDS / "sounds.json").read_text(encoding="utf-8"))


def check(files: dict[str, str] | None = None) -> list[str]:
    keymap = kk.load()["sounds"]
    committed = committed_sounds()
    sounds = committed["sounds"]
    problems = keymap_problems(keymap, sounds)
    for script in SCRIPT_KEYS:
        problems += layout_problems(script, keymap, sounds, read_layouts(script))
        problems += cheatsheet_problems(script, keymap, sounds, *read_cheatsheet(script))
    zethu = next(f for f in keyboards.manifest()["families"] if f["name"] == "Khelathi Zethu Glyphs")
    problems += zethu_problems(zethu["codepoints"])
    problems += encoding_problems(committed, files)
    return problems


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--encoding", action="append", default=[], metavar="SCRIPT=FILE",
                    help="apply an encoding file for a script instead of encodings/<script>.json, such as vedyakshara=FILE")
    args = ap.parse_args()
    problems = check(dict(entry.split("=", 1) for entry in args.encoding))
    print(f"keyboards: {len(kk.load()['sounds'])} sounds on {len(SCRIPT_KEYS)} layouts and 4 platforms, " + (f"{len(problems)} problems" if problems else "ok"))
    for line in problems[:40]:
        print(line)
    sys.exit(bool(problems))


if __name__ == "__main__":
    main()
