# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Write the Zethu codage, ``encodings/zethu-mdc.json``, and the Zethu script encoding that states it, ``encodings/zethu.json``, from encoding.json and controls.json.

    python3 tools/khelathi-zethu-glyphs/encoding_file.py           # write the file
    python3 tools/khelathi-zethu-glyphs/encoding_file.py --check   # check it

Every drawn sign is typed by its code, its sense in capitals (``SAIL``, ``WEST``). The
notation of the Manuel de Codage types the format controls, in the face's own block: ``:``
the vertical joiner, ``*`` the horizontal joiner, ``[ts]``, ``[bs]``, ``[te]`` and
``[be]`` the four insertions, ``(`` and ``)`` a segment, and ``<`` and ``>`` a cartouche.
``-`` ends a quadrat and draws nothing, so it writes its escaped invisible spelling mark, distinct from the shared stanza control,
and decoding restores it. The codage is a file of kind ``codage``: it extends nothing, allows only
its codes and its notation, and is reached only between the literal markers of ``zethu``.

The script encoding ``zethu`` extends the standard roman encoding, ``encodings/standard.json``,
and accepts nothing else as roman: Khelathi words are written by the language-aware encoder, and
a code is read only between ``⟦`` and ``⟧``. The script has no spaces, its signs set directly
beside each other, so its separator is empty: whitespace in the roman writes nothing, and no
encoding output contains U+0020. Decoding gives the ``⟦…⟧`` codage alone. Every standard mark
keeps the standard's invisible mark, since the face draws none of them.
"""

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
OUT = ROOT / "encodings" / "zethu-mdc.json"
SCRIPT = ROOT / "encodings" / "zethu.json"
sys.path.insert(0, str(ROOT))
import encode as E  # noqa: E402

# What the notation types for each control, by its key in controls.json.
NOTATION = {
    "vj": ":",
    "hj": "*",
    "its": "[ts]",
    "ibs": "[bs]",
    "ite": "[te]",
    "ibe": "[be]",
    "bs": "(",
    "es": ")",
    "be": "<",
    "ee": ">",
}


def char(codepoint: str) -> str:
    return chr(int(codepoint[2:], 16))


def rows() -> list:
    signs = json.loads((HERE / "encoding.json").read_text(encoding="utf-8"))["signs"]
    controls = json.loads((HERE / "controls.json").read_text(encoding="utf-8"))["controls"]
    out = [[s["code"], char(s["codepoint"])] for s in signs if s["drawn"]]
    keys = {c["key"] for c in controls}
    if keys != set(NOTATION):
        raise SystemExit(
            "tools/khelathi-zethu-glyphs/controls.json: error: the controls are "
            f"{', '.join(sorted(keys))}, and the notation types {', '.join(sorted(NOTATION))}"
        )
    out += [[NOTATION[c["key"]], char(c["twin"])] for c in controls]
    return out + [["-", E.mark("-")]]


def text() -> str:
    return E.dumps(
        {
            "name": "zethu-mdc",
            "kind": "codage",
            "fonts": ["khelathi-zethu-glyphs"],
            "rows": rows(),
        }
    )


def script_text() -> str:
    return E.dumps(
        {
            "name": "zethu",
            "fonts": ["khelathi-zethu-glyphs"],
            "extends": E.STANDARD,
            "codage": "zethu-mdc",
            "accepts": [],
            "separator": "",
            "rows": [],
        }
    )


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="check the file rather than write it")
    if ap.parse_args().check:
        for path, want in ((OUT, text()), (SCRIPT, script_text())):
            if not path.exists() or path.read_text(encoding="utf-8") != want:
                print(f"{path.relative_to(ROOT)}: error: differs from encoding.json; run encoding_file.py")
                return 1
        return 0
    OUT.write_text(text(), encoding="utf-8")
    SCRIPT.write_text(script_text(), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
