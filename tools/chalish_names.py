# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Write tools/names/chalish.json, the character names of Chalish Pilam Common.

    .venv/bin/python tools/chalish_names.py

A name derives from the glyph name in tools/chalish-pilam/encoding.json, so drawing
another glyph renames nothing. Zero and the numbers to 19 are ``CHALISH NUMBER <n>``, the
places of the count are ``CHALISH PLACE <n>``, and every other glyph is ``CHALISH GLYPH
<NAME>``. A retired row keeps no name.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def name(glyph: str) -> str:
    if m := re.fullmatch(r"n(\d+)", glyph):
        return f"CHALISH NUMBER {m[1]}"
    if m := re.fullmatch(r"p(\d+)", glyph):
        return f"CHALISH PLACE {m[1]}"
    if not re.fullmatch(r"[a-z]+(?:[._][a-z]+)*", glyph):
        raise SystemExit(f"tools/chalish-pilam/encoding.json: error: glyph {glyph!r} has no Unicode-style name")
    return "CHALISH GLYPH " + re.sub(r"[._]", " ", glyph).upper()


def main() -> None:
    rows = json.loads((ROOT / "tools" / "chalish-pilam" / "encoding.json").read_text(encoding="utf-8"))["glyphs"]
    names = {r["codepoint"]: name(r["glyph"]) for r in sorted(rows, key=lambda r: r["codepoint"]) if not r.get("retired")}
    if len(set(names.values())) != len(names):
        sys.exit("tools/chalish-pilam/encoding.json: error: two glyphs take one name")
    (ROOT / "tools" / "names" / "chalish.json").write_text(json.dumps(names, indent=4) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
