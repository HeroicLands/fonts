# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Write the Teng Chou codage, ``tools/encodings/teng-chou-codes.json``, and the Teng Chou script encoding that states it, ``tools/encodings/teng-chou.json``, from the code point table.

    .venv/bin/python tools/teng-chou/codage.py           # write the files
    .venv/bin/python tools/teng-chou/codage.py --check   # check them

Every character of the face has one code: a character its morpheme in capitals (``HO``,
``WONG``), a stage of the tally ``TALLY1`` to ``TALLY5``, and a sign of the Jurthati
syllabary its syllable in lowercase (``ka``, ``tsa``). Case separates a character from a
sign that shares its spelling, so ``KA`` and ``ka`` write different characters. Codes are
separated by whitespace, which only separates and writes nothing. The codage is a file of
kind ``codage``: it extends nothing and is reached only between the literal markers of
``teng-chou``. The script encoding extends the standard roman encoding,
``tools/encodings/standard.json``, and accepts nothing else as roman: Tantsou words are turned into
characters by the language-aware encoder. The script has no spaces, its characters set
directly beside each other, so its separator is empty and no output holds U+0020. The files
are generated, so they never drift from the font: run this after a character is added.
"""

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
OUT = ROOT / "tools" / "encodings" / "teng-chou-codes.json"
SCRIPT = ROOT / "tools" / "encodings" / "teng-chou.json"
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(ROOT))
import codepoint_order  # noqa: E402
import encode as E  # noqa: E402

TALLY = "tc.tally"


def code(glyph: str) -> str:
    """The code that types a glyph."""
    kind, _, value = glyph.partition(".")
    if glyph.startswith(TALLY):
        return "TALLY" + glyph[len(TALLY):]
    return value.upper() if kind == "tc" else value


def rows() -> list:
    out = [
        [code(r["glyph"]), chr(int(r["codepoint"][2:], 16))]
        for r in codepoint_order.ltr_table("TengChou-Regular")
    ]
    codes = [c for c, _ in out]
    if len(set(codes)) != len(codes):
        raise SystemExit("tools/codepoint_order.py: error: two Teng Chou glyphs share a code")
    return out


def text() -> str:
    return E.dumps(
        {"name": "teng-chou-codes", "kind": "codage", "fonts": ["teng-chou"], "rows": rows()}
    )


def script_text() -> str:
    return E.dumps(
        {
            "name": "teng-chou",
            "fonts": ["teng-chou"],
            "extends": E.STANDARD,
            "codage": "teng-chou-codes",
            "accepts": [],
            "separator": "",
            "rows": [],
        }
    )


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="check the files rather than write them")
    if ap.parse_args().check:
        for path, want in ((OUT, text()), (SCRIPT, script_text())):
            if not path.exists() or path.read_text(encoding="utf-8") != want:
                print(f"{path.relative_to(ROOT)}: error: differs from the code point table; run codage.py")
                return 1
        return 0
    OUT.write_text(text(), encoding="utf-8")
    SCRIPT.write_text(script_text(), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
