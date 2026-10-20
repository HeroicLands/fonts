# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Confirm that each family's keyboard layouts type every character, and every lexicon form.

    .venv/bin/python tools/keyboards_guard.py [--thalorna ~/dev/HeroicLands/thalorna | --fixtures-only]

Two things are checked for each family.

- **The layouts agree with the table.** The macOS, Windows, Linux and Emacs files in
  ``keyboards/`` are read back, and each must put every character of the family's
  ``codepoints`` table on the key the table names, and nothing else. Khelathi Zethu
  Glyphs has an Emacs input method only.
- **The layout reaches the lexicon.** Every form is shaped with the font's Latin typing
  rules, each resulting glyph is mapped to its code point, and every code point must have
  a key in the family's table. A glyph that is not a character (a spelling helper, the
  doubling mark, the space) needs none. Qalezu's Latin forms go through the guard's
  converter first, and Khelathi Zethu Glyphs is checked on the sign ids of its sample
  inscriptions.

The forms are the lexicon of each language note on the ``origin/main`` of a thalorna
checkout, plus the fixtures of each family's own guard. ``--fixtures-only`` reads the
fixtures alone, which needs no thalorna checkout.
"""

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import codepoints  # noqa: E402
import keyboard_keys as kk  # noqa: E402
import keyboards  # noqa: E402
from render import Renderer  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
KEYBOARDS = ROOT / "keyboards"

# Family key -> manifest name of its table, the fonts it shapes with and the guard that reads its lexicon.
FAMILIES = {
    "semaron": ("Semaron Kuriale", ["SemaronKuriale-Regular"], "semaron-kuriale"),
    "pirzath": ("Pirzath Carved", ["PirzathCarved-Regular", "PirzathHand-Regular"], "pirzath"),
    "thuravark": ("Thuravark Carved", ["ThuravarkCarved-Regular"], "thuravark-carved"),
    "qalezu": ("Qalezu Hand", ["QalezuHand-Regular"], "qalezu-hand"),
    "zethu": ("Khelathi Zethu Glyphs", ["KhelathiZethuGlyphs-Regular"], "khelathi-zethu-glyphs"),
}
LAYERS = [(False, False), (True, False), (False, True), (True, True)]


def load(name: str):
    path = ROOT / "tools" / name / "guard.py"
    spec = importlib.util.spec_from_file_location(name.replace("-", "_") + "_guard", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def table_of(name: str) -> list[dict]:
    families = json.loads((ROOT / "fonts.json").read_text(encoding="utf-8"))["families"]
    return next(f for f in families if f["name"] == name)["codepoints"]


def spelled(shift: bool, option: bool, base: str) -> str:
    return kk.spell(shift, option, base)


# -- Reading the layouts back --------------------------------------------------------------


def read_macos(text: str) -> dict[str, int]:
    """key -> code point for every output that is not the key's own character."""
    codes = {v: k for k, v in kk.MAC_CODES.items()}
    out = {}
    for index, body in re.findall(r'<keyMap index="(\d)">(.*?)</keyMap>', text, re.S):
        shift, option = LAYERS[int(index)]
        for code, output in re.findall(r'<key code="(\d+)" output="([^"]*)"/>', body):
            base = codes.get(int(code))
            chars = [int(h, 16) for h in re.findall(r"&#x([0-9A-Fa-f]+);", output)]
            if base is None or len(chars) != 1 or chars[0] < 0xE000:
                continue
            out[spelled(shift, option, base)] = chars[0]
    return out


def read_windows(data: bytes) -> dict[str, int]:
    text = data.decode("utf-16").replace("\r\n", "\n")
    layout, ligatures = text.split("\nLIGATURE\n", 1)
    units = {}
    for line in ligatures.split("\n"):
        parts = line.split("\t")
        if len(parts) >= 3 and not line.startswith("//") and re.fullmatch(r"[0-9a-f]{4}", parts[2]):
            vk, state = parts[0], int(parts[1])
            chars = [int(p, 16) for p in parts[2:] if p]
            units[(vk, state)] = _join(chars)
    by_vk = {vk: base for base, (_, vk) in keyboards.WIN_KEYS.items()}
    out = {}
    for line in layout.split("\n"):
        parts = line.split("\t")
        if len(parts) < 9 or not re.fullmatch(r"[0-9a-f]{2}", parts[0]) or parts[1] not in by_vk:
            continue
        base = by_vk[parts[1]]
        for (state, layer), cell in zip(keyboards.WIN_STATES, parts[4:9]):
            if cell == "%%":
                shift, option = LAYERS[layer]
                out[spelled(shift, option, base)] = units[(parts[1], state)]
    return out


def _join(units: list[int]) -> int:
    if len(units) == 1:
        return units[0]
    high, low = units
    return 0x10000 + ((high - 0xD800) << 10) + (low - 0xDC00)


def read_xkb(text: str) -> dict[str, int]:
    by_name = {v: k for k, v in keyboards.XKB_KEYS.items()}
    out = {}
    for name, symbols in re.findall(r"key <(\w+)> \{.*?symbols\[Group1\] = \[ ([^\]]*) \] \};", text):
        for layer, symbol in enumerate(s.strip() for s in symbols.split(",")):
            if re.fullmatch(r"U[0-9A-F]+", symbol):
                shift, option = LAYERS[layer]
                out[spelled(shift, option, by_name[name])] = int(symbol[1:], 16)
    return out


def read_emacs(text: str) -> dict[str, int]:
    """quail sequence -> code point."""
    rules = text.split("(quail-define-rules", 1)[1]
    return {
        re.sub(r"\\(.)", r"\1", seq): int(code, 16)
        for seq, code in re.findall(r'\("((?:[^"\\]|\\.)*)" #x([0-9A-F]+)\)', rules)
    }


def read_layouts(key: str) -> dict[str, str | bytes]:
    texts = {"emacs": (KEYBOARDS / "emacs" / f"heroiclands-{key}.el").read_text(encoding="utf-8")}
    if key != "zethu":
        label = next(f for f in keyboards.FAMILIES if f["key"] == key)["layout"]
        base = KEYBOARDS / "macos" / keyboards.BUNDLE / "Contents" / "Resources"
        texts["macos"] = (base / f"{label}.keylayout").read_text(encoding="utf-8")
        texts["windows"] = (KEYBOARDS / "windows" / f"{key}.klc").read_bytes()
        texts["linux"] = (KEYBOARDS / "linux" / f"hl_{key}").read_text(encoding="utf-8")
    return texts


def layout_problems(key: str, table: list[dict], texts: dict) -> list[str]:
    """Where a layout file disagrees with the family's table."""
    problems = []
    if key == "zethu":
        want = {r["key"]: int(r["codepoint"][2:], 16) for r in table}
        got = read_emacs(texts["emacs"])
        platforms = {"emacs": got}
        wants = {"emacs": want}
    else:
        want = {kk.spell(*kk.parse(r["key"])): int(r["codepoint"][2:], 16) for r in table if "key" in r}
        platforms = {
            "macos": read_macos(texts["macos"]),
            "windows": read_windows(texts["windows"]),
            "linux": read_xkb(texts["linux"]),
            "emacs": read_emacs(texts["emacs"]),
        }
        wants = {p: want for p in platforms}
        wants["emacs"] = {kk.quail_sequence(k): c for k, c in want.items()}
    for platform, got in platforms.items():
        expected = wants[platform]
        for k in sorted(expected.keys() - got.keys()):
            problems.append(f"keyboards: error: {key}: the {platform} layout has no output on {k}")
        for k in sorted(got.keys() - expected.keys()):
            problems.append(f"keyboards: error: {key}: the {platform} layout types U+{got[k]:04X} on {k}, which the table lacks")
        for k in sorted(got.keys() & expected.keys()):
            if got[k] != expected[k]:
                problems.append(f"keyboards: error: {key}: the {platform} layout types U+{got[k]:04X} on {k}, not U+{expected[k]:04X}")
    return problems


# -- Typing the lexicon --------------------------------------------------------------------


def typing_problems(key: str, table: list[dict], glyph_runs: list[tuple[str, list[str]]]) -> list[str]:
    """Every glyph of every run is a character with a key, or is not a character."""
    stem = FAMILIES[key][1][0]
    typed = {r["glyph"] for r in table if isinstance(r.get("key"), str) and r["key"]}
    listed = {r["glyph"] for r in table}
    exempt = set(codepoints.NOT_CHARACTERS.get(stem, {}))
    problems, seen = [], set()
    for text, glyphs in glyph_runs:
        for glyph in glyphs:
            if glyph in typed or glyph in exempt or codepoints.is_structural(glyph, listed):
                continue
            if (glyph, "k") in seen:
                continue
            seen.add((glyph, "k"))
            why = "has no key" if glyph in listed else "has no code point"
            problems.append(f"keyboards: error: {key}: {glyph} (in {text!r}) {why}")
    return problems


def latin_runs(key: str, texts: list[str]) -> list[tuple[str, list[str]]]:
    runs = []
    for stem in FAMILIES[key][1]:
        r = Renderer(ROOT / "fonts" / f"{stem}.ttf")
        runs += [(t, r.glyph_names(t)) for t in texts]
    return runs


def fixture_texts(key: str) -> list[str]:
    guard = load(FAMILIES[key][2])
    if key == "pirzath":
        return [t for t, _ in guard.FIXTURES + guard.LOST_FIXTURES]
    if key == "qalezu":
        return [latin for latin, _ in guard.FIXTURES]
    return [t for t, _ in guard.FIXTURES]


def lexicon_texts(key: str, thalorna: Path) -> list[str]:
    return load(FAMILIES[key][2]).lexicon_forms(thalorna, None)


def runs_for(key: str, texts: list[str]) -> list[tuple[str, list[str]]]:
    """The glyphs each text shapes to; Qalezu's Latin is converted to its signs first."""
    if key != "qalezu":
        return latin_runs(key, texts)
    guard = load(FAMILIES[key][2])
    names = {int(r["codepoint"][2:], 16): r["glyph"] for r in table_of("Qalezu Hand")}
    runs = []
    for latin, signs in zip(texts, guard.convert_all(texts)):
        if isinstance(signs, str):
            runs.append((latin, ["space" if c == " " else names.get(ord(c), f"U+{ord(c):04X}") for c in signs]))
    return runs


def zethu_runs() -> list[tuple[str, list[str]]]:
    guard = load("khelathi-zethu-glyphs")
    return [(label, ["sign " + i for i in ids]) for label, ids in guard.sample_lists()]


def zethu_problems(table: list[dict]) -> list[str]:
    """Every sign id of the sample inscriptions is the key of a drawn sign."""
    keys = {r["key"] for r in table}
    problems, seen = [], set()
    for label, glyphs in zethu_runs():
        for glyph in glyphs:
            sid = glyph[5:]
            if sid not in keys and sid not in seen:
                seen.add(sid)
                problems.append(f"keyboards: error: zethu: the sign {sid} (in {label!r}) has no key")
    return problems


def check(key: str, table: list[dict], thalorna: Path | None) -> tuple[list[str], int]:
    """The problems of a family, and how many texts were typed through its layout."""
    problems = layout_problems(key, table, read_layouts(key))
    if key == "zethu":
        return problems + zethu_problems(table), len(zethu_runs())
    texts = fixture_texts(key)
    if thalorna is not None:
        texts = texts + lexicon_texts(key, thalorna)
    return problems + typing_problems(key, table, runs_for(key, texts)), len(texts)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--thalorna", default=str(Path.home() / "dev/HeroicLands/thalorna"))
    ap.add_argument("--fixtures-only", action="store_true", help="read the guards' fixtures and no lexicon")
    args = ap.parse_args()
    thalorna = None if args.fixtures_only else Path(args.thalorna)
    status = 0
    for key, (name, _, _) in FAMILIES.items():
        problems, count = check(key, table_of(name), thalorna)
        print(f"{key}: {count} texts typed, " + (f"{len(problems)} problems" if problems else "ok"))
        for line in problems[:20]:
            print(line)
        status |= bool(problems)
    sys.exit(status)


if __name__ == "__main__":
    main()
