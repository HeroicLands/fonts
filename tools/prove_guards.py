# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Prove that each guard passes a built font and fails the same font broken.

    .venv/bin/python tools/prove_guards.py

The broken Pirzath and Thuravark fonts are the built .ttf with the GSUB table
removed, so no ligature, decomposition or contextual rule applies. The broken
Qalezu Hand font has one sign, the th, removed from its cmap. Khelathi Zethu Glyphs is broken
twice: once with one sign, the crocodile-hunt house 11-001, removed from its cmap,
and once with the GSUB table removed so that no second or third form is reachable.
Semaron Kuriale is broken twice: with the GSUB table removed, so that no
th, long vowel or spelled-out ch applies, and with the GPOS table removed, so that no catch stands on its
base. The box guard (tools/notdef_box.py) is proved on every font twice: with the question
mark removed from the cmap, and with it pointed at glyph 0. The name guard
(tools/font_names.py) is proved on every font twice: with the Macintosh full name
removed, and with the Basic Latin range declared. The vertical guard (tools/vertical.py) is proved on every font three times: with the hhea ascent changed,
with USE_TYPO_METRICS cleared, and with one glyph lifted out of the band. The code-point guard (tools/codepoints.py)
is proved on every font with the first code point of its fonts.json table removed from the cmap, and on every left-to-right font
with an entry in the Basic Multilingual Plane's Private Use Area. Its key rules are proved
on altered fonts.json tables: a character without a key, two characters on one key, and a Pirzath Hand key that differs from Pirzath
Carved's. Its block registry is proved on a code point outside its family's blocks, two overlapping blocks and a README table that
differs from the registry. The default-ignorable check of the box guard is proved on every font with the glyph of the ignorables drawing the box, and on
Pirzath Carved with the GSUB table removed. The keyboard guard (tools/keyboards_guard.py) is proved on a table with a
character's key removed, with a character's row removed and on a Linux layout with a key line removed. The guards run on their
fixtures alone, so the proof needs no lexicon.
"""

import copy
import importlib.util
import json
import sys
import tempfile
from pathlib import Path

from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def stripped(font: Path, out: Path) -> Path:
    f = TTFont(str(font))
    del f["GSUB"]
    f.save(str(out))
    return out


def without_gpos(font: Path, out: Path) -> Path:
    f = TTFont(str(font))
    del f["GPOS"]
    f.save(str(out))
    return out


def without_sign(font: Path, out: Path) -> Path:
    enc = json.loads((ROOT / "tools" / "khelathi-zethu-glyphs" / "encoding.json").read_text(encoding="utf-8"))
    cp = next(int(e["codepoint"][2:], 16) for e in enc["signs"] if e["id"] == "11-001")
    f = TTFont(str(font))
    for table in f["cmap"].tables:
        table.cmap.pop(cp, None)
    f.save(str(out))
    return out


def without_th(font: Path, out: Path) -> Path:
    f = TTFont(str(font))
    for table in f["cmap"].tables:
        table.cmap.pop(0x1EA09, None)
    f.save(str(out))
    return out


def without_codepoint(font: Path, out: Path) -> Path:
    first = next(f for f in json.loads((ROOT / "fonts.json").read_text(encoding="utf-8"))["families"]
                 if Path(f["files"]["ttf"]).name == font.name)["codepoints"][0]["codepoint"]
    f = TTFont(str(font))
    for table in f["cmap"].tables:
        table.cmap.pop(int(first[2:], 16), None)
    f.save(str(out))
    return out


def with_bmp_private(font: Path, out: Path) -> Path:
    f = TTFont(str(font))
    glyph = next(n for n in f.getGlyphOrder() if n not in (".notdef", "notdef.box"))
    for table in f["cmap"].tables:
        if table.isUnicode():
            table.cmap[0xE000] = glyph
    f.save(str(out))
    return out


def ignorable_drawn(font: Path, out: Path) -> Path:
    """The glyph every default-ignorable shapes to draws the box."""
    f = TTFont(str(font))
    f["glyf"]["ignorable.sub"] = f["glyf"]["notdef.box"]
    f.save(str(out))
    return out


def wrong_ascent(font: Path, out: Path) -> Path:
    f = TTFont(str(font))
    f["hhea"].ascent -= 1
    f.save(str(out))
    return out


def no_typo_metrics(font: Path, out: Path) -> Path:
    f = TTFont(str(font))
    f["OS/2"].fsSelection &= ~(1 << 7)
    f.save(str(out))
    return out


def lifted_glyph(font: Path, out: Path) -> Path:
    """Lift the box glyph 600 units, past the ascent of any face."""
    f = TTFont(str(font))
    glyph = f["glyf"]["notdef.box"]
    glyph.coordinates.translate((0, 600))
    glyph.recalcBounds(f["glyf"])
    f.save(str(out))
    return out


def box_unmapped(font: Path, out: Path) -> Path:
    f = TTFont(str(font))
    for table in f["cmap"].tables:
        table.cmap.pop(ord("?"), None)
    f.save(str(out))
    return out


def box_glyph0(font: Path, out: Path) -> Path:
    f = TTFont(str(font))
    for table in f["cmap"].tables:
        table.cmap[ord("?")] = ".notdef"
    f.save(str(out))
    return out


def without_name(font: Path, out: Path) -> Path:
    f = TTFont(str(font))
    f["name"].removeNames(nameID=4, platformID=1)
    f.save(str(out))
    return out


def latin_declared(font: Path, out: Path) -> Path:
    f = TTFont(str(font))
    f["OS/2"].ulUnicodeRange1 |= 1
    f.save(str(out))
    return out


def prove_keys(codepoints) -> int:
    """Prove the key rules of the code-point guard on altered copies of fonts.json."""
    original = codepoints.manifest
    base = original()

    def entry(manifest, name):
        return next(f for f in manifest["families"] if f["name"] == name)

    def lose_key(manifest):
        del entry(manifest, "Semaron Kuriale")["codepoints"][0]["key"]

    def share_key(manifest):
        rows = entry(manifest, "Semaron Kuriale")["codepoints"]
        rows[1]["key"] = rows[0]["key"]

    def hand_differs(manifest):
        entry(manifest, "Pirzath Hand")["codepoints"][0]["key"] = "option+shift+x"

    cases = [
        ("Semaron Kuriale", "SemaronKuriale-Regular.ttf", lose_key, "with a character without a key", "has no key"),
        ("Semaron Kuriale", "SemaronKuriale-Regular.ttf", share_key, "with two characters on one key", "share the key"),
        ("Pirzath Hand", "PirzathHand-Regular.ttf", hand_differs, "with a key that differs from Pirzath Carved's", "the keys differ"),
    ]
    status = 0
    for label, name, mutate, how, expect in cases:
        font = ROOT / "fonts" / name
        good = [p for p in codepoints.check(font) if "key" in p]
        altered = copy.deepcopy(base)
        mutate(altered)
        codepoints.manifest = lambda altered=altered: altered
        try:
            bad = [p for p in codepoints.check(font) if expect in p]
        finally:
            codepoints.manifest = original
        print(f"{label}: {len(good)} key failures on the table, {len(bad)} on the table {how}")
        if good or not bad:
            print(f"{font}: error: the key guard must pass the table and fail the altered table")
            status = 1
    return status


def prove_registry(codepoints) -> int:
    """Prove the block registry rules of the code-point guard."""
    order = codepoints.codepoint_order
    original_manifest, original_blocks, original_table = codepoints.manifest, order.BLOCKS, order.readme_table
    status = 0

    def run(how, expect, setup):
        nonlocal status
        good = [p for p in codepoints.registry_problems() + codepoints.check(ROOT / "fonts" / "PirzathCarved-Regular.ttf") if expect in p]
        setup()
        try:
            bad = [p for p in codepoints.registry_problems() + codepoints.check(ROOT / "fonts" / "PirzathCarved-Regular.ttf") if expect in p]
        finally:
            codepoints.manifest, order.BLOCKS, order.readme_table = original_manifest, original_blocks, original_table
        print(f"block registry: {len(good)} failures on the registry, {len(bad)} on the registry {how}")
        if good or not bad:
            print(f"tools/codepoint_order.py: error: the registry guard must pass the registry and fail it {how}")
            status = 1

    def outside():
        altered = copy.deepcopy(original_manifest())
        next(f for f in altered["families"] if f["name"] == "Pirzath Carved")["codepoints"][0]["codepoint"] = "U+F0300"
        codepoints.manifest = lambda: altered

    def overlap():
        order.BLOCKS = [*original_blocks, {**original_blocks[0], "start": original_blocks[0]["end"], "end": original_blocks[0]["end"] + 1}]

    def readme():
        order.readme_table = lambda: original_table() + "\n| extra |"

    run("with a code point outside its family's blocks", "outside the blocks registered", outside)
    run("with two blocks overlapping", "overlap", overlap)
    run("with a README table that differs", "table differs", readme)
    return status


def prove_keyboards() -> int:
    """Prove that the keyboard guard fails a table that loses a key or a row, and a layout that loses a key."""
    guard = load("keyboards_guard", ROOT / "tools" / "keyboards_guard.py")
    key = "pirzath"
    table = guard.table_of("Pirzath Carved")
    texts = guard.fixture_texts(key)
    status = 0

    def count(rows, layouts=None):
        problems = guard.typing_problems(key, rows, guard.runs_for(key, texts))
        return len(problems) + len(guard.layout_problems(key, rows, layouts or guard.read_layouts(key)))

    def without_key(rows):
        rows = copy.deepcopy(rows)
        del next(r for r in rows if r["glyph"] == "sh")["key"]
        return rows

    def without_row(rows):
        return [r for r in rows if r["glyph"] != "sh"]

    layouts = guard.read_layouts(key)
    linux = "\n".join(line for line in layouts["linux"].split("\n") if "<AC03>" not in line)
    good = count(table)
    cases = [
        ("with the key of sh removed", count(without_key(table))),
        ("with the row of sh removed", count(without_row(table))),
        ("with a Linux key line removed", count(table, {**layouts, "linux": linux})),
    ]
    for how, bad in cases:
        print(f"keyboards: {good} failures on the table, {bad} on the table {how}")
        if good or not bad:
            print("tools/keyboards_guard.py: error: the keyboard guard must pass the table and fail the altered table")
            status = 1
    return status


def main():
    pirzath = load("pirzath_guard", ROOT / "tools" / "pirzath" / "guard.py")
    hand = load("pirzath_hand_guard", ROOT / "tools" / "pirzath-hand" / "guard.py")
    thuravark = load("thuravark_guard", ROOT / "tools" / "thuravark-carved" / "guard.py")
    qalezu = load("qalezu_guard", ROOT / "tools" / "qalezu-hand" / "guard.py")
    zethu = load("zethu_guard", ROOT / "tools" / "khelathi-zethu-glyphs" / "guard.py")
    semaron = load("semaron_guard", ROOT / "tools" / "semaron-kuriale" / "guard.py")
    zethu_font = ROOT / "fonts" / "KhelathiZethuGlyphs-Regular.ttf"
    cases = [
        (
            "Pirzath Carved",
            ROOT / "fonts" / "PirzathCarved-Regular.ttf",
            lambda p: pirzath.run(p, []),
            stripped,
            "without GSUB",
        ),
        (
            "Pirzath Hand",
            ROOT / "fonts" / "PirzathHand-Regular.ttf",
            lambda p: hand.run(p, []),
            stripped,
            "without GSUB",
        ),
        (
            "Thuravark Carved",
            ROOT / "fonts" / "ThuravarkCarved-Regular.ttf",
            lambda p: thuravark.shaping(p, []),
            stripped,
            "without GSUB",
        ),
        (
            "Qalezu Hand",
            ROOT / "fonts" / "QalezuHand-Regular.ttf",
            lambda p: qalezu.run(p, []),
            without_th,
            "without the th sign",
        ),
        (
            "Semaron Kuriale",
            ROOT / "fonts" / "SemaronKuriale-Regular.ttf",
            lambda p: semaron.run(p, []),
            stripped,
            "without GSUB",
        ),
        (
            "Semaron Kuriale",
            ROOT / "fonts" / "SemaronKuriale-Regular.ttf",
            lambda p: semaron.run(p, []),
            without_gpos,
            "without GPOS",
        ),
        ("Khelathi Zethu Glyphs", zethu_font, zethu.run, without_sign, "without the 11-001 sign"),
        ("Khelathi Zethu Glyphs", zethu_font, zethu.run, stripped, "without GSUB"),
    ]
    codepoints = load("codepoints", ROOT / "tools" / "codepoints.py")
    notdef = load("notdef_box", ROOT / "tools" / "notdef_box.py")
    names = load("font_names", ROOT / "tools" / "font_names.py")
    vertical = load("vertical", ROOT / "tools" / "vertical.py")
    for font in sorted((ROOT / "fonts").glob("*-Regular.ttf")):
        label = font.name.split("-")[0]
        cases.append((label, font, codepoints.check, without_codepoint, "with its first code point unmapped"))
        if font.name.split("-")[0] in ("PirzathCarved", "PirzathHand", "ThuravarkCarved", "SemaronKuriale"):
            cases.append((label, font, codepoints.check, with_bmp_private, "with an entry in the BMP Private Use Area"))
        cases.append((label, font, notdef.check, ignorable_drawn, "with the glyph of the ignorables drawing the box"))
        cases.append((label, font, notdef.check, box_unmapped, "with ? unmapped"))
        cases.append((label, font, notdef.check, box_glyph0, "with ? on glyph 0"))
        cases.append((label, font, vertical.check, wrong_ascent, "with the hhea ascent changed"))
        cases.append((label, font, vertical.check, no_typo_metrics, "without USE_TYPO_METRICS"))
        cases.append((label, font, vertical.check, lifted_glyph, "with a glyph lifted out of the band"))
        cases.append((label, font, names.check, without_name, "with the Macintosh full name removed"))
        cases.append((label, font, names.check, latin_declared, "declaring Basic Latin"))
    status = 0
    with tempfile.TemporaryDirectory() as tmp:
        for label, font, guard, break_font, how in cases:
            good = guard(font)
            bad = guard(break_font(font, Path(tmp) / font.name))
            ok = not good and bad
            print(f"{label}: {len(good)} failures on the font, {len(bad)} on the font {how}")
            if not ok:
                print(f"{font}: error: the guard must pass the font and fail the broken font")
                status = 1
    status |= prove_keys(codepoints)
    status |= prove_registry(codepoints)
    status |= prove_keyboards()
    pirzath_font = ROOT / "fonts" / "PirzathCarved-Regular.ttf"
    with tempfile.TemporaryDirectory() as tmp:
        good, bad = notdef.check(pirzath_font), notdef.check(stripped(pirzath_font, Path(tmp) / pirzath_font.name))
        print(f"Pirzath Carved: {len(good)} failures on the font, {len(bad)} on the font without GSUB, where an ignorable draws the space dot")
        if good or not bad:
            print(f"{pirzath_font}: error: the ignorable check must pass the font and fail the font without GSUB")
            status = 1
    sys.exit(status)


if __name__ == "__main__":
    main()
