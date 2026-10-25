# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Write the character names of Ch'alish P'ilam's two hands: tools/names/chalish.json for
Chalish Pilam Common and tools/names/chalishceremonial.json for Chalish Pilam Ceremonial.

    .venv/bin/python tools/chalish_names.py

A name derives from the glyph name in the hand's table, tools/chalish-pilam/encoding.json
or tools/chalish-pilam/ceremonial_encoding.json, so drawing another glyph renames nothing.

- Common: zero and the numbers to 19 are ``CHALISH NUMBER <n>``, the places of the count
  are ``CHALISH PLACE <n>``, and every other glyph is ``CHALISH GLYPH <NAME>``.
- Ceremonial: a number is ``CHALISH CEREMONIAL NUMBER <n>``, a syllable sign ``CHALISH
  CEREMONIAL SYLLABLE <SYLLABLE>-<n>`` (``ka1`` is ``KA-1``), a joiner ``CHALISH CEREMONIAL
  JOINER BESIDE`` or ``STACK``, and every other glyph ``CHALISH CEREMONIAL GLYPH <NAME>``.

A retired row keeps no name, and neither does a pending ceremonial row, which the font
does not draw.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TABLES = ROOT / "tools" / "chalish-pilam"


def name(glyph: str) -> str:
    if m := re.fullmatch(r"n(\d+)", glyph):
        return f"CHALISH NUMBER {m[1]}"
    if m := re.fullmatch(r"p(\d+)", glyph):
        return f"CHALISH PLACE {m[1]}"
    if not re.fullmatch(r"[a-z]+(?:[._][a-z]+)*", glyph):
        raise SystemExit(f"tools/chalish-pilam/encoding.json: error: glyph {glyph!r} has no Unicode-style name")
    return "CHALISH GLYPH " + re.sub(r"[._]", " ", glyph).upper()


def ceremonial_name(row: dict) -> str:
    glyph, kind = row["glyph"], row["kind"]
    if kind == "number" and (m := re.fullmatch(r"n(\d+)", glyph)):
        return f"CHALISH CEREMONIAL NUMBER {m[1]}"
    if kind == "syllable" and (m := re.fullmatch(r"([a-z]+)(\d+)", glyph)):
        return f"CHALISH CEREMONIAL SYLLABLE {m[1].upper()}-{m[2]}"
    if kind == "joiner" and (m := re.fullmatch(r"join_([a-z]+)", glyph)):
        return f"CHALISH CEREMONIAL JOINER {m[1].upper()}"
    if kind == "concept" and re.fullmatch(r"[a-z0-9]+(?:_[a-z0-9]+)*", glyph):
        return "CHALISH CEREMONIAL GLYPH " + glyph.replace("_", " ").upper()
    raise SystemExit(f"tools/chalish-pilam/ceremonial_encoding.json: error: glyph {glyph!r} has no Unicode-style name")


def write(table: str, out: str, namer, skip) -> None:
    rows = json.loads((TABLES / table).read_text(encoding="utf-8"))["glyphs"]
    names = {r["codepoint"]: namer(r) for r in sorted(rows, key=lambda r: r["codepoint"]) if not skip(r)}
    if len(set(names.values())) != len(names):
        sys.exit(f"tools/chalish-pilam/{table}: error: two glyphs take one name")
    (ROOT / "tools" / "names" / out).write_text(json.dumps(names, indent=4) + "\n", encoding="utf-8")


def main() -> None:
    write("encoding.json", "chalish.json", lambda r: name(r["glyph"]), lambda r: r.get("retired"))
    write("ceremonial_encoding.json", "chalishceremonial.json", ceremonial_name,
          lambda r: r.get("retired") or r.get("pending"))


if __name__ == "__main__":
    main()
