# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Write what sources/Qalezu.ufo derives from tools/qalezu/encoding.json.

    .venv/bin/python tools/qalezu/apply_encoding.py [--check]

Three things follow from the encoding, and nothing else in the UFO is touched, so
no drawn outline changes: each glyph's <unicode> lines; one composite ``<sign>.dbl``
per doubled consonant, the sign with the ``doubling`` component set at the sign's
``doubling`` anchor; the two empty glyphs that default-ignorable characters
map to with their ``ccmp`` substitution; and the code points of ``notdef.box``,
which are every code point of the ranges in tools/notdef_box.py that the encoding
leaves free. The box glyph itself comes from tools/apply_notdef_box.py.

--check reports a disagreement and writes nothing.
"""

import json
import plistlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import notdef_box  # noqa: E402

UFO = ROOT / "sources" / "Qalezu.ufo"
GLYPHS = UFO / "glyphs"
ENCODING = Path(__file__).resolve().parent / "encoding.json"

HEADER = """<?xml version='1.0' encoding='UTF-8'?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
"""

FEATURES = """languagesystem DFLT dflt;

# HarfBuzz replaces a default-ignorable character the font maps directly with
# the space glyph. A glyph that a lookup substitutes is left alone, so each
# ignorable is substituted once, to a second empty glyph.
feature ccmp {{
  sub {ignorable} by {substitute};
}} ccmp;
"""


def load():
    enc = json.loads(ENCODING.read_text(encoding="utf-8"))
    unicodes = {g["glyph"]: [int(g["codepoint"][2:], 16)] for g in enc["glyphs"]}
    unicodes[enc["space"]["glyph"]] = [int(enc["space"]["codepoint"][2:], 16)]
    ign = enc["ignorables"]
    unicodes[ign["glyph"]] = [int(c[2:], 16) for c in ign["codepoints"]]
    unicodes[ign["substitute"]] = []
    taken = {cp for cps in unicodes.values() for cp in cps}
    unicodes[notdef_box.BOX] = [cp for cp in notdef_box.codepoints() if cp not in taken]
    doubled = {g["glyph"]: g["base"] for g in enc["glyphs"] if g["kind"] == "doubled"}
    return enc, unicodes, doubled


def with_unicodes(text: str, cps: list[int]) -> str:
    stripped = re.sub(r"[ \t]*<unicode hex=\"[0-9A-Fa-f]+\"/>\n", "", text)
    lines = "".join(f'  <unicode hex="{cp:04X}"/>\n' for cp in cps)
    if not lines:
        return stripped
    m = re.search(r"  <advance [^>]*/>\n", stripped) or re.search(r"<glyph [^>]*>\n", stripped)
    return stripped[: m.end()] + lines + stripped[m.end():]


def plist_text(value) -> str:
    body = plistlib.dumps(value, sort_keys=False).decode("utf-8")
    body = body.split("<plist", 1)[1]
    body = re.sub(r"^(\t*)(?=<)", lambda m: "  " * (len(m.group(1)) + 1), "<plist" + body, flags=re.M)
    body = body.replace('  <plist version="1.0">', '<plist version="1.0">').replace("  </plist>", "</plist>")
    return HEADER + body


def anchor_and_width(name: str) -> tuple[tuple[str, str], str]:
    text = (GLYPHS / f"{name}.glif").read_text(encoding="utf-8")
    a = re.search(r'<anchor x="([^"]+)" y="([^"]+)" name="doubling"/>', text)
    w = re.search(r'<advance width="([^"]+)"/>', text)
    return (a.group(1), a.group(2)), w.group(1)


def composite(name: str, base: str, cps: list[int]) -> str:
    (ax, ay), width = anchor_and_width(base)
    source = (GLYPHS / f"{base}.glif").read_text(encoding="utf-8")
    parts = re.findall(r"    <component [^>]*/>\n", source) or [f'    <component base="{base}"/>\n']
    return with_unicodes(f"""<?xml version='1.0' encoding='UTF-8'?>
<glyph name="{name}" format="2">
  <advance width="{width}"/>
  <outline>
{"".join(parts)}    <component base="doubling" xOffset="{ax}" yOffset="{ay}"/>
  </outline>
</glyph>
""", cps)


def empty(name: str) -> str:
    return f"""<?xml version='1.0' encoding='UTF-8'?>
<glyph name="{name}" format="2">
  <advance width="0"/>
  <outline>
  </outline>
</glyph>
"""


def main():
    check = "--check" in sys.argv
    enc, unicodes, doubled = load()
    ign = enc["ignorables"]
    outputs: dict[Path, str] = {}

    empties = [ign["glyph"], ign["substitute"]]
    dbl = list(doubled)
    for name, base in doubled.items():
        outputs[GLYPHS / f"{name}.glif"] = composite(name, base, unicodes[name])
    for name in empties:
        outputs[GLYPHS / f"{name}.glif"] = with_unicodes(empty(name), unicodes[name])

    contents = plistlib.loads((GLYPHS / "contents.plist").read_bytes())
    for name in empties + dbl:
        contents[name] = f"{name}.glif"
    contents = dict(sorted(contents.items()))
    outputs[GLYPHS / "contents.plist"] = plist_text(contents)

    for name in set(contents) - set(empties) - set(dbl):
        path = GLYPHS / contents[name]
        outputs[path] = with_unicodes(path.read_text(encoding="utf-8"), unicodes.get(name, []))
    missing = set(unicodes) - set(contents)
    for name in sorted(missing):
        print(f"{UFO}: error: encoding.json names {name}, which is not a glyph")
        sys.exit(1)

    lib = plistlib.loads((UFO / "lib.plist").read_bytes())
    order = [n for n in lib["public.glyphOrder"] if n not in empties and n not in dbl] + empties + dbl
    lib["public.glyphOrder"] = order
    cats = dict(lib["public.openTypeCategories"])
    cats.update({n: "base" for n in empties + dbl})
    lib["public.openTypeCategories"] = dict(sorted(cats.items()))
    outputs[UFO / "lib.plist"] = plist_text(lib)

    outputs[UFO / "features.fea"] = FEATURES.format(
        ignorable=ign["glyph"], substitute=ign["substitute"]
    )

    status = 0
    for path, new in outputs.items():
        old = path.read_text(encoding="utf-8") if path.exists() else None
        if new != old:
            if check:
                print(f"{path}: error: differs from what encoding.json derives")
                status = 1
            else:
                path.write_text(new, encoding="utf-8")
    sys.exit(status)


if __name__ == "__main__":
    main()
