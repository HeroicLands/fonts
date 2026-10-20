# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Give a font source its box glyph and map every unused character to it.

    .venv/bin/python tools/apply_notdef_box.py sources/<Font>.ufo [--retarget GLYPH ...]
        [--drop GLYPH ...] [--ignorables]

The rule lives in tools/notdef_box.py. This script writes it into a UFO, and the
font generators call ``apply`` after they write theirs, so a regeneration keeps it.

- ``notdef.box`` is a copy of ``.notdef``, placed right after it in the glyph order.
- Every code point of the checked ranges that no glyph maps goes to ``notdef.box``.
- ``--retarget`` names glyphs whose code points in the ranges move to the box.
- ``--drop`` deletes glyphs, once nothing maps to them.
- ``--ignorables`` adds the two empty glyphs and the ``ccmp`` substitution for the
  default-ignorable characters, in a font that has none.
- The kerning, the contextual classes and the GDEF base class treat the box as they
  treat ``.notdef``.

Running it twice changes nothing. It edits the files as text, so a UFO's other
glyphs, and their formatting, are untouched.
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from notdef_box import BOX, codepoints  # noqa: E402

IGNORABLES = [
    *range(0x200B, 0x2010),
    *range(0x202A, 0x202F),
    *range(0x2066, 0x206A),
    0xFEFF,
]
UNICODE = re.compile(r'^\s*<unicode hex="([0-9A-Fa-f]+)"/>\n', re.M)


def glif_path(ufo: Path, name: str) -> Path:
    """The glif file of a glyph, from contents.plist."""
    text = (ufo / "glyphs" / "contents.plist").read_text(encoding="utf-8")
    match = re.search(rf"<key>{re.escape(name)}</key>\s*<string>([^<]+)</string>", text)
    if not match:
        raise KeyError(name)
    return ufo / "glyphs" / match.group(1)


def mapping(ufo: Path) -> dict[int, str]:
    out = {}
    contents = (ufo / "glyphs" / "contents.plist").read_text(encoding="utf-8")
    for name, file in re.findall(r"<key>([^<]+)</key>\s*<string>([^<]+)</string>", contents):
        for hexval in UNICODE.findall((ufo / "glyphs" / file).read_text(encoding="utf-8")):
            out[int(hexval, 16)] = name
    return out


def set_unicodes(text: str, cps) -> str:
    """Replace a glif's unicode lines with these code points, kept sorted."""
    text = UNICODE.sub("", text)
    lines = "".join(f'  <unicode hex="{cp:04X}"/>\n' for cp in sorted(set(cps)))
    return re.sub(r"(  <advance [^>]*/>\n)", lambda m: m.group(1) + lines, text, count=1)


def unicodes_of(text: str) -> list[int]:
    return [int(h, 16) for h in UNICODE.findall(text)]


def add_glyph(ufo: Path, name: str, glif_text: str):
    """Write a new glyph's file and list it in contents.plist."""
    file = f"{name}.glif"
    (ufo / "glyphs" / file).write_text(glif_text, encoding="utf-8")
    path = ufo / "glyphs" / "contents.plist"
    text = path.read_text(encoding="utf-8")
    entries = re.findall(r"    <key>([^<]+)</key>\n    <string>([^<]+)</string>\n", text)
    entries.append((name, file))
    entries.sort()
    head = text[: text.index("<dict>") + len("<dict>\n")]
    body = "".join(f"    <key>{k}</key>\n    <string>{v}</string>\n" for k, v in entries)
    path.write_text(head + body + "  </dict>\n</plist>\n", encoding="utf-8")


def drop_glyph(ufo: Path, name: str):
    file = glif_path(ufo, name)
    path = ufo / "glyphs" / "contents.plist"
    text = path.read_text(encoding="utf-8")
    text = re.sub(rf"    <key>{re.escape(name)}</key>\n    <string>[^<]+</string>\n", "", text)
    path.write_text(text, encoding="utf-8")
    file.unlink()
    lib = ufo / "lib.plist"
    ltext = lib.read_text(encoding="utf-8")
    ltext = re.sub(rf"      <string>{re.escape(name)}</string>\n", "", ltext)
    ltext = re.sub(rf"      <key>{re.escape(name)}</key>\n      <string>[^<]+</string>\n", "", ltext)
    lib.write_text(ltext, encoding="utf-8")


def add_to_order(ufo: Path, name: str, after: str):
    lib = ufo / "lib.plist"
    text = lib.read_text(encoding="utf-8")
    if f"<string>{name}</string>" in text:
        return
    text = text.replace(
        f"      <string>{after}</string>\n", f"      <string>{after}</string>\n      <string>{name}</string>\n", 1
    )
    lib.write_text(text, encoding="utf-8")


def add_category(ufo: Path, name: str, category: str):
    lib = ufo / "lib.plist"
    text = lib.read_text(encoding="utf-8")
    if "<key>public.openTypeCategories</key>" not in text or f"<key>{name}</key>" in text:
        return
    start = text.index("<key>public.openTypeCategories</key>")
    head, tail = text[:start], text[start:]
    block_start = tail.index("<dict>\n") + len("<dict>\n")
    block_end = tail.index("    </dict>")
    entries = re.findall(r"      <key>([^<]+)</key>\n      <string>([^<]+)</string>\n", tail[block_start:block_end])
    entries.append((name, category))
    entries.sort()
    body = "".join(f"      <key>{k}</key>\n      <string>{v}</string>\n" for k, v in entries)
    lib.write_text(head + tail[:block_start] + body + tail[block_end:], encoding="utf-8")


def edit_features(ufo: Path, ignorables: bool):
    path = ufo / "features.fea"
    text = path.read_text(encoding="utf-8")
    if f"{BOX}" not in text:
        text = re.sub(r"(@AFTER = \[)\.notdef ", rf"\1.notdef {BOX} ", text)
        text = re.sub(r"(GlyphClassDef \[)\.notdef ", rf"\1.notdef {BOX} ", text)
        out = []
        for line in text.split("\n"):
            out.append(line)
            m = re.match(r"^(\s*pos )(\S+) (\S+) (-?\d+;)$", line)
            if m and ".notdef" in (m.group(2), m.group(3)):
                a, b = m.group(2), m.group(3)
                swap = lambda g, box: BOX if g == ".notdef" and box else g
                for left, right in ((True, False), (False, True), (True, True)):
                    if (left and a != ".notdef") or (right and b != ".notdef"):
                        continue
                    out.append(f"{m.group(1)}{swap(a, left)} {swap(b, right)} {m.group(4)}")
        text = "\n".join(out)
    if ignorables and "ignorable.sub" not in text:
        lookup = (
            "  # HarfBuzz replaces a default-ignorable character the font maps directly with\n"
            "  # the space glyph. A glyph that a lookup substitutes is left alone, so each\n"
            "  # ignorable is substituted once, to a second empty glyph.\n"
            "  lookup ccmp_ignorable {\n    sub ignorable by ignorable.sub;\n  } ccmp_ignorable;\n"
        )
        if "feature ccmp {\n" in text:
            text = text.replace("feature ccmp {\n", "feature ccmp {\n" + lookup, 1)
        else:
            text = text.replace("\nfeature ", "\nfeature ccmp {\n" + lookup + "} ccmp;\n\nfeature ", 1)
        text = re.sub(r"(GlyphClassDef \[)", r"\1ignorable ignorable.sub ", text, count=1)
    path.write_text(text, encoding="utf-8")


def apply(ufo: Path, retarget=(), drop=(), ignorables=False):
    ufo = Path(ufo)
    cmap = mapping(ufo)
    wanted = set(codepoints())

    notdef = glif_path(ufo, ".notdef").read_text(encoding="utf-8")
    box_file = ufo / "glyphs" / f"{BOX}.glif"
    if not box_file.exists():
        box = UNICODE.sub("", notdef).replace('name=".notdef"', f'name="{BOX}"')
        add_glyph(ufo, BOX, box)
        add_to_order(ufo, BOX, ".notdef")
        add_category(ufo, BOX, "base")

    if ignorables and "ignorable" not in {v for v in cmap.values()}:
        empty = '<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n<glyph name="{n}" format="2">\n  <advance width="0"/>\n  <outline>\n  </outline>\n</glyph>\n'
        add_glyph(ufo, "ignorable", empty.format(n="ignorable"))
        add_glyph(ufo, "ignorable.sub", empty.format(n="ignorable.sub"))
        file = ufo / "glyphs" / "ignorable.glif"
        file.write_text(set_unicodes(file.read_text(encoding="utf-8"), IGNORABLES), encoding="utf-8")
        add_to_order(ufo, "ignorable", "space")
        add_to_order(ufo, "ignorable.sub", "ignorable")
        add_category(ufo, "ignorable", "base")
        add_category(ufo, "ignorable.sub", "base")
        cmap = mapping(ufo)

    for name in retarget:
        file = glif_path(ufo, name)
        text = file.read_text(encoding="utf-8")
        have = unicodes_of(text)
        file.write_text(set_unicodes(text, [c for c in have if c not in wanted]), encoding="utf-8")
    cmap = mapping(ufo)

    on_box = [c for c, n in cmap.items() if n == BOX]
    new = [c for c in sorted(wanted) if c not in cmap]
    text = box_file.read_text(encoding="utf-8")
    box_file.write_text(set_unicodes(text, on_box + new), encoding="utf-8")

    for name in drop:
        drop_glyph(ufo, name)
    edit_features(ufo, ignorables)
    return len(new)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("ufo")
    ap.add_argument("--retarget", nargs="*", default=[])
    ap.add_argument("--drop", nargs="*", default=[])
    ap.add_argument("--ignorables", action="store_true")
    args = ap.parse_args()
    n = apply(Path(args.ufo), args.retarget, args.drop, args.ignorables)
    print(f"{args.ufo}: {n} code points newly mapped to {BOX}")


if __name__ == "__main__":
    main()
