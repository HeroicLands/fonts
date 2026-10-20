# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Write fonts.css and encoding/ for the npm package.

    .venv/bin/python tools/write_css.py

fonts.css holds one @font-face rule per built font, named from the font's own
name table (ID 16 when present, else ID 1), with relative URLs so a stylesheet
imported from node_modules or a CDN finds the files beside it. encoding/ holds a
copy of each right-to-left font's code-point table, so a consumer reads it
without the tools directory.
"""

import shutil
from pathlib import Path

from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent

# The code-point tables the package ships, by the name they ship under.
ENCODINGS = {
    "qalezu-hand": ROOT / "tools" / "qalezu-hand" / "encoding.json",
    "khelathi-zethu-glyphs": ROOT / "tools" / "khelathi-zethu-glyphs" / "encoding.json",
}


def family_name(path: Path) -> str:
    names = TTFont(path)["name"]
    for name_id in (16, 1):
        record = names.getName(name_id, 3, 1, 0x409)
        if record is not None:
            return record.toUnicode()
    raise SystemExit(f"{path}: no Windows family name (ID 16 or 1)")


def font_face(ttf: Path) -> str:
    stem = ttf.stem
    return (
        "@font-face {\n"
        f'    font-family: "{family_name(ttf)}";\n'
        f'    src: url("fonts/{stem}.woff2") format("woff2"),\n'
        f'        url("fonts/{stem}.ttf") format("truetype");\n'
        "    font-display: swap;\n"
        "}\n"
    )


def main() -> None:
    fonts = sorted((ROOT / "fonts").glob("*.ttf"))
    rules = "\n".join(font_face(ttf) for ttf in fonts)
    (ROOT / "fonts.css").write_text(rules, encoding="utf-8")
    encoding = ROOT / "encoding"
    encoding.mkdir(exist_ok=True)
    for name, source in ENCODINGS.items():
        shutil.copyfile(source, encoding / f"{name}.json")


if __name__ == "__main__":
    main()
