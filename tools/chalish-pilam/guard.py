# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Shape fixtures through Chalish Pilam Common and assert the font sets them.

    .venv/bin/python tools/chalish-pilam/guard.py [--font fonts/ChalishPilamCommon-Regular.ttf]

The fixtures are a night's entry at the sighting stones
(``glyphs.passage_glyphs()``) and every glyph once. Each is written as the code points of
``encoding.json`` and shaped by HarfBuzz, and a fixture fails when it does not yield
exactly its glyphs, one each, or a glyph is ``.notdef`` or the box.
"""

import argparse
import json
import sys
from pathlib import Path

import uharfbuzz as hb
from fontTools.ttLib import TTFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent

FONT = ROOT / "fonts" / "ChalishPilamCommon-Regular.ttf"
BAD = {".notdef", "notdef.box"}


def table() -> dict[str, str]:
    """Glyph name -> its character."""
    rows = json.loads((HERE / "encoding.json").read_text(encoding="utf-8"))["glyphs"]
    return {r["glyph"]: chr(int(r["codepoint"][2:], 16)) for r in rows if not r.get("retired")}


def passage() -> list[str]:
    """The glyph names of the night entry. The drawing modules are imported afresh and
    dropped again, since other faces' tools share their names."""
    sys.path.insert(0, str(HERE))
    for name in ("build_ufo", "glyphs", "strokes"):
        sys.modules.pop(name, None)
    try:
        import build_ufo
        import glyphs

        return [build_ufo.glyph_name(g) for g in glyphs.passage_glyphs()]
    finally:
        sys.path.remove(str(HERE))
        for name in ("build_ufo", "glyphs", "strokes"):
            sys.modules.pop(name, None)


def fixtures() -> list[tuple[str, list[str]]]:
    """(label, glyph names): the night entry, then every glyph on its own."""
    out = [("the night entry", passage())]
    out += [(name, [name]) for name in table()]
    return out


def run(path: Path) -> list[str]:
    font = hb.Font(hb.Face(path.read_bytes()))
    order = TTFont(str(path)).getGlyphOrder()
    chars = table()
    failures = []
    for label, want in fixtures():
        missing = [w for w in want if w not in chars]
        if missing:
            failures.append(f"{label}: no code point for {', '.join(missing)}")
            continue
        buf = hb.Buffer()
        buf.add_str("".join(chars[w] for w in want))
        buf.direction = "ltr"
        buf.script = "Zyyy"
        hb.shape(font, buf, {})
        got = [order[i.codepoint] for i in buf.glyph_infos]
        if any(g in BAD for g in got):
            failures.append(f"{label}: shaped to {got}, which draws the box")
        elif got != want:
            failures.append(f"{label}: shaped to {got}, expected {want}")
    return failures


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--font", default=str(FONT))
    a = ap.parse_args()
    failures = run(Path(a.font))
    for f in failures:
        print(f"{a.font}: error: {f}")
    print(f"{a.font}: {len(fixtures())} fixtures: " + ("ok" if not failures else f"{len(failures)} failures"))
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
