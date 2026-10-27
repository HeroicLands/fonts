# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Write the Chalish Ceremonial Codage, ``tools/encodings/chalish-ceremonial.json``, the script
encoding that states it, ``tools/encodings/chalish-pilam-ceremonial.json``, and the rows of
thalorna's mapping note, from ceremonial_encoding.json.

    .venv/bin/python tools/chalish-pilam/ceremonial_codage.py --write   # write both files
    .venv/bin/python tools/chalish-pilam/ceremonial_codage.py --check   # check them
    .venv/bin/python tools/chalish-pilam/ceremonial_codage.py > rows.yaml

Every character of Chalish Pilam Ceremonial has one code: a concept glyph its name in
capitals (``SUN``, ``KING``), a syllable sign its syllable and number (``ka1``, ``la1``),
a number ``n`` and its value (``n13``, ``n400``). ``*`` writes the joiner that sets
items side by side and ``:`` the one that stacks the first over the second. ``-`` ends a
block and writes nothing, since a block ends wherever no joiner follows; whitespace only
separates codes and writes nothing. The rows are generated, so the map never drifts from the font: run this
after a glyph is added, write the encoding, and paste the printed rows into the note's
``data.map.rows``.

The codage is a file of kind ``codage``: it extends nothing and is reached only between
the literal markers of ``chalish-pilam-ceremonial``. In it, ``-`` writes its invisible
mark (``encode.mark``), so decoding restores it. The script encoding extends the
standard roman encoding, ``tools/encodings/standard.json``, and accepts nothing else as roman,
since the hand writes no sounds; its separator is one space, an empty block. Zero and the places of the count have codes and code points
but no ceremonial drawing, so they print the box; the encoding keeps their rows, so a
text written today keeps its code points when they are drawn, and the note's rows say
that they print the box.
"""

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
OUT = ROOT / "tools" / "encodings" / "chalish-ceremonial.json"
SCRIPT = ROOT / "tools" / "encodings" / "chalish-pilam-ceremonial.json"
sys.path.insert(0, str(ROOT))
import encode as E  # noqa: E402


def table() -> list[dict]:
    return [r for r in json.loads((HERE / "ceremonial_encoding.json").read_text(encoding="utf-8"))["glyphs"]
            if not r.get("retired")]


def rows() -> list[tuple[str, str, bool]]:
    """(code, code point, pending) for every live glyph, in code point order."""
    out = [(r["code"], r["codepoint"], bool(r.get("pending"))) for r in table()]
    codes = [c for c, _, _ in out]
    if len(set(codes)) != len(codes):
        raise SystemExit("ceremonial_codage: error: two glyphs share a code")
    return out


def characters() -> dict[str, str]:
    """Code -> the character that types it, with ``-`` and the space writing nothing."""
    chars = {code: chr(int(cp[2:], 16)) for code, cp, _ in rows()}
    chars["-"] = ""
    chars[" "] = ""
    return chars


def to_text(codage: str) -> str:
    """A codage string as the characters it writes. Codes are separated by ``*``, ``:``,
    ``-`` and spaces."""
    chars = characters()
    out, code = [], ""
    for ch in codage + " ":
        if ch in "*: -":
            if code:
                if code not in chars:
                    raise KeyError(f"no code {code!r}")
                out.append(chars[code])
                code = ""
            out.append(chars[ch])
        else:
            code += ch
    return "".join(out)


def encoding_text() -> str:
    """The codage file: every code, then ``-`` writing its mark."""
    rows_ = [[code, chr(int(cp[2:], 16))] for code, cp, _ in rows()]
    rows_ += [["-", E.mark("-")]]
    return E.dumps({"name": "chalish-ceremonial", "kind": "codage", "fonts": ["chalish-pilam-ceremonial"], "rows": rows_})


def script_text() -> str:
    return E.dumps(
        {
            "name": "chalish-pilam-ceremonial",
            "fonts": ["chalish-pilam-ceremonial"],
            "extends": E.STANDARD,
            "codage": "chalish-ceremonial",
            "accepts": [],
            "separator": " ",
            "rows": [],
        }
    )


def note_rows():
    for code, cp, pending in rows():
        char = chr(int(cp[2:], 16))
        note = " pending: draws the box" if pending else ""
        print(f'      - ["{code}", "{char}"] # {cp}{note}')
    print('      - ["-", ""]')


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    group = ap.add_mutually_exclusive_group()
    group.add_argument("--write", action="store_true", help="write the codage and the script encoding")
    group.add_argument("--check", action="store_true", help="check the codage and the script encoding")
    args = ap.parse_args()
    files = ((OUT, encoding_text()), (SCRIPT, script_text()))
    if args.check:
        for path, want in files:
            if not path.exists() or path.read_text(encoding="utf-8") != want:
                print(f"{path.relative_to(ROOT)}: error: differs from ceremonial_encoding.json; run ceremonial_codage.py --write")
                return 1
        return 0
    if args.write:
        for path, want in files:
            path.write_text(want, encoding="utf-8")
        return 0
    note_rows()
    return 0


if __name__ == "__main__":
    sys.exit(main())
