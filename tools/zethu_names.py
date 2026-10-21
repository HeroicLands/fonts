# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Write tools/names/zethu.json, the character names of Khelathi Zethu Glyphs.

    .venv/bin/python tools/zethu_names.py

Each drawn sign is ``ZETHU CHARACTER <n>``, where n is the position of its code point in
the font's code point space (``zethu_number`` in tools/codepoint_order.py), padded to three
digits. A name depends on the code point alone, so drawing another sign renames nothing.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import codepoint_order  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    rows = sorted(codepoint_order.zethu_table(), key=lambda r: int(r["codepoint"][2:], 16))
    names = {r["codepoint"]: codepoint_order.zethu_name(int(r["codepoint"][2:], 16)) for r in rows}
    (ROOT / "tools" / "names" / "zethu.json").write_text(json.dumps(names, indent=4) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
