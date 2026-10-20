# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Prove that each guard passes a built font and fails the same font broken.

    .venv/bin/python tools/prove_guards.py

The broken Pirzath and Thuravark fonts are the built .ttf with the GSUB table
removed, so no ligature, decomposition or contextual rule applies. The broken
Qalezu font has one sign, the th, removed from its cmap. Khelathi Zethu is broken
twice: once with one sign, the crocodile-hunt house 11-001, removed from its cmap,
and once with the GSUB table removed so that no second or third form is reachable.
The guards run on their fixtures alone, so the proof needs no lexicon.
"""

import importlib.util
import json
import sys
import tempfile
from pathlib import Path

from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def stripped(font: Path, out: Path) -> Path:
    f = TTFont(str(font))
    del f["GSUB"]
    f.save(str(out))
    return out


def without_sign(font: Path, out: Path) -> Path:
    enc = json.loads((ROOT / "tools" / "zethu" / "encoding.json").read_text(encoding="utf-8"))
    cp = next(int(e["codepoint"][2:], 16) for e in enc["signs"] if e["id"] == "11-001")
    f = TTFont(str(font))
    for table in f["cmap"].tables:
        table.cmap.pop(cp, None)
    f.save(str(out))
    return out


def without_th(font: Path, out: Path) -> Path:
    f = TTFont(str(font))
    for table in f["cmap"].tables:
        table.cmap.pop(0x1EA09, None)
    f.save(str(out))
    return out


def main():
    pirzath = load("pirzath_guard", ROOT / "tools" / "pirzath" / "guard.py")
    hand = load("pirzath_hand_guard", ROOT / "tools" / "pirzath-hand" / "guard.py")
    thuravark = load("thuravark_guard", ROOT / "tools" / "thuravark" / "guard.py")
    qalezu = load("qalezu_guard", ROOT / "tools" / "qalezu" / "guard.py")
    zethu = load("zethu_guard", ROOT / "tools" / "zethu" / "guard.py")
    zethu_font = ROOT / "fonts" / "KhelathiZethu-Regular.ttf"
    cases = [
        (
            "Pirzath Carved",
            ROOT / "fonts" / "PirzathCarved-Regular.ttf",
            lambda p: pirzath.run(p, []),
            stripped,
            "without GSUB",
        ),
        (
            "Pirzath Hand",
            ROOT / "fonts" / "PirzathHand-Regular.ttf",
            lambda p: hand.run(p, []),
            stripped,
            "without GSUB",
        ),
        (
            "Thuravark Runic",
            ROOT / "fonts" / "ThuravarkRunic-Regular.ttf",
            lambda p: thuravark.shaping(p, []),
            stripped,
            "without GSUB",
        ),
        (
            "Qalezu",
            ROOT / "fonts" / "Qalezu-Regular.ttf",
            lambda p: qalezu.run(p, []),
            without_th,
            "without the th sign",
        ),
        ("Khelathi Zethu", zethu_font, zethu.run, without_sign, "without the 11-001 sign"),
        ("Khelathi Zethu", zethu_font, zethu.run, stripped, "without GSUB"),
    ]
    status = 0
    with tempfile.TemporaryDirectory() as tmp:
        for label, font, guard, break_font, how in cases:
            good = guard(font)
            bad = guard(break_font(font, Path(tmp) / font.name))
            ok = not good and bad
            print(f"{label}: {len(good)} failures on the font, {len(bad)} on the font {how}")
            if not ok:
                print(f"{font}: error: the guard must pass the font and fail the broken font")
                status = 1
    sys.exit(status)


if __name__ == "__main__":
    main()
