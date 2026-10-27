# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Set Teng Chou's passages and assert the font sets every character of them.

    .venv/bin/python tools/teng-chou/guard.py [--font fonts/TengChou-Regular.ttf]

The fixtures are the specimen passages of ``texts.py``, Tantsou and Jurthati, each
line a run of characters named by their glyphs. A line fails when a character has no
code point, or its characters, shaped in a horizontal run and in a vertical one, do not
yield exactly their glyphs, one each.
"""

import argparse
import sys
from pathlib import Path

import uharfbuzz as hb

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))
import codepoint_order  # noqa: E402
import texts  # noqa: E402

ROOT = HERE.parent.parent
FONT = ROOT / "fonts" / "TengChou-Regular.ttf"


def table() -> dict[str, str]:
    """Glyph name -> its character."""
    return {r["glyph"]: chr(int(r["codepoint"][2:], 16)) for r in codepoint_order.ltr_table("TengChou-Regular")}


def shape(font: hb.Font, text: str, direction: str) -> list[int]:
    buf = hb.Buffer()
    buf.add_str(text)
    buf.direction = direction
    buf.script = "Zyyy"
    buf.guess_segment_properties()
    hb.shape(font, buf, {})
    return [i.codepoint for i in buf.glyph_infos]


def run(path: Path) -> list[str]:
    data = path.read_bytes()
    font = hb.Font(hb.Face(data))
    from fontTools.ttLib import TTFont

    order = TTFont(str(path)).getGlyphOrder()
    chars = table()
    failures = []
    lines = [(" ".join(line), line) for line in texts.TANTSOU + texts.JURTHATI]
    for label, parts in lines:
        want = [f"js.{p[1:]}" if p.startswith("=") else f"tc.{p}" for p in parts]
        missing = [w for w in want if w not in chars]
        if missing:
            failures.append(f"{label}: no character for {', '.join(missing)}")
            continue
        text = "".join(chars[w] for w in want)
        for direction in ("ltr", "ttb"):
            got = [order[g] for g in shape(font, text, direction)]
            if got != want:
                failures.append(f"{label}: set {direction} as {got}, expected {want}")
    return failures


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--font", default=str(FONT))
    a = ap.parse_args()
    failures = run(Path(a.font))
    for f in failures:
        print(f"{a.font}: error: {f}")
    print(f"{a.font}: {len(texts.TANTSOU) + len(texts.JURTHATI)} passages: "
          + ("ok" if not failures else f"{len(failures)} failures"))
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
