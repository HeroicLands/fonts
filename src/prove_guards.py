# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Prove that each guard passes a built font and fails the same font without its layout.

    .venv/bin/python src/prove_guards.py

The broken font is the built .ttf with its GSUB table removed, so no ligature,
decomposition or contextual rule applies. The guards run on their fixtures
alone, so the proof needs no lexicon.
"""

import importlib.util
import sys
import tempfile
from pathlib import Path

from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))


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


def main():
    pirzath = load("pirzath_guard", ROOT / "src" / "guard.py")
    thuravark = load("thuravark_guard", ROOT / "thuravark" / "src" / "guard.py")
    cases = [
        ("Pirzath Carved", ROOT / "fonts" / "PirzathCarved-Regular.ttf", lambda p: pirzath.run(p, [])),
        (
            "Thuravark Runic",
            ROOT / "thuravark" / "fonts" / "ThuravarkRunic-Regular.ttf",
            lambda p: thuravark.shaping(p, []),
        ),
    ]
    status = 0
    with tempfile.TemporaryDirectory() as tmp:
        for label, font, guard in cases:
            good = guard(font)
            bad = guard(stripped(font, Path(tmp) / font.name))
            ok = not good and bad
            print(f"{label}: {len(good)} failures on the font, {len(bad)} on the font without GSUB")
            if not ok:
                print(f"{font}: error: the guard must pass the font and fail the stripped font")
                status = 1
    sys.exit(status)


if __name__ == "__main__":
    main()
