# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Write the Chalish Common Codage, ``encodings/chalish-common.json``, from encoding.json.

    .venv/bin/python tools/chalish-pilam/codage.py           # write the file
    .venv/bin/python tools/chalish-pilam/codage.py --check   # check it

Every glyph of Chalish Pilam Common has one code: a concept glyph its name in capitals
(``SUN``, ``MAN``, ``HIGH``), a number ``n`` and its value (``n13``, ``n400``). Codes are
separated by spaces. The script has no word spaces, so a space writes its mark, the
invisible variation selector U+E0100, and decoding restores it. The encoding is generated, so it never
drifts from the font: run this after a glyph is added.
"""

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
OUT = ROOT / "encodings" / "chalish-common.json"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT))
import encode as E  # noqa: E402
import glyphs as K  # noqa: E402

VALUES = {g.name: int(g.meaning.replace(",", "")) for g in K.NUMERALS + K.PLACES}


def code(row: dict) -> str:
    """The code that types a glyph."""
    name = row["glyph"]
    if row["kind"] == "number":
        if name == "n0":
            return "n0"
        upper = name.upper()
        return f"n{VALUES[upper]}" if upper in VALUES else name
    return name.upper()


def rows() -> list:
    table = json.loads((HERE / "encoding.json").read_text(encoding="utf-8"))["glyphs"]
    out = [[code(r), chr(int(r["codepoint"][2:], 16))] for r in table if not r.get("retired")]
    codes = [c for c, _ in out]
    if len(set(codes)) != len(codes):
        raise SystemExit("tools/chalish-pilam/encoding.json: error: two glyphs share a code")
    return out + [[" ", E.mark(" ")]]


def text() -> str:
    return E.dumps(
        {"name": "chalish-common", "fonts": ["chalish-pilam-common"], "rows": rows()}
    )


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="check the file rather than write it")
    if ap.parse_args().check:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != text():
            print(f"{OUT.relative_to(ROOT)}: error: differs from encoding.json; run codage.py")
            return 1
        return 0
    OUT.write_text(text(), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
