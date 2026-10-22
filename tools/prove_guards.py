# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Prove that each guard passes a built font and fails the same font broken.

    .venv/bin/python tools/prove_guards.py

The broken Pirzath and Thuravark fonts are the built .ttf with the GSUB table
removed, so no ligature, decomposition or contextual rule applies. The broken
Qalezu Hand font has one sign, the th, removed from its cmap. Khelathi Zethu Glyphs is broken
twice: once with one sign, the crocodile-hunt house 11-001, removed from its cmap,
and once with the GSUB table removed so that no second or third form is reachable. Its
quadrat guard (tools/khelathi-zethu-glyphs/quadrats.py) is proved four times: with the
lookup that sums a row's widths taken out of the features, with the GPOS table removed,
with the vertical joiner in the font's own block unmapped, and with the lookup that lays
the cord along a cartouche taken out.
Teng Chou is broken three times: its lexicon guard (tools/teng-chou/guard.py) and its font
check (tools/teng-chou/check_font.py) on the font with the character for teng removed from
its cmap, and the font check on the font without its vertical metrics; and the vertical
guard is proved on its columns with one character's vertical advance off the em, and with
every vertical advance 825 units, even but not one em. Its
stroke-mix guard (tools/teng-chou/stroke_mix.py) is proved on its data with water written in
six dabs, and with the syllabary sign ka kept to one stroke.
Semaron Kuriale is broken twice: with the GSUB table removed, so that no
th, long vowel or spelled-out ch applies, and with the GPOS table removed, so that no catch stands on its
base. Veldikko's guard (tools/veldikko/guard.py) and its font check
(tools/veldikko/check_font.py) are each proved twice: with the GSUB table removed, so that no
letter joins and no vowel takes its signs, and with the GPOS table removed, so that no mark
stands over its letter; and the vertical guard is proved on Veldikko with its Windows ascent and
descent cut to the shared line box, so that its risers and tails would be clipped. The box guard (tools/notdef_box.py) is proved on every font twice: with the question
mark removed from the cmap, and with it pointed at glyph 0. The name guard
(tools/font_names.py) is proved on every font twice: with the Macintosh full name
removed, and with the Basic Latin range declared. The vertical guard (tools/vertical.py) is proved on every font three times: with the hhea ascent changed,
with USE_TYPO_METRICS cleared, and with one glyph lifted out of the band. The code-point guard (tools/codepoints.py)
is proved on every font with the first code point of its fonts.json table removed from the cmap, and on every left-to-right font
with an entry in the Basic Multilingual Plane's Private Use Area. Its key rules are proved
on altered fonts.json tables: a Khelathi Zethu Glyphs sign without a key, two signs on one key, and a key on a character of a script
typed by sound. Its block registry is proved on a code point outside its family's blocks, two overlapping blocks and a README table that
differs from the registry. The spacing guard (tools/spacing.py) is proved on every font with every advance widened by 120 units,
half on each side of the ink, and on Khelathi Zethu Glyphs and Qalezu Hand with the space widened by 100 units. The default-ignorable check of the box guard is proved on every font with the glyph of the ignorables drawing the box, and on
Pirzath Carved with the GSUB table removed. The keyboard guard (tools/keyboards_guard.py) is proved on a key map with
two sounds on one key, with a sound removed, with a capital off Shift, with a quote off Shift+, and Shift+., with a markup character missing and with a
markup character on a key that carries a sound; on layouts with a macOS output cut short, a Linux key
line removed, an Emacs rule removed and a Windows key typing a roman letter, and with a key of markup typing
nothing on each platform; and, where a thalorna checkout exists, on a sounds.json
that thalorna's mapping notes no longer spell. The cheatsheet guard (tools/charts_guard.py) is proved on a sheet with a table row removed, with a wrong Code Point cell, with a chart cell removed, with a glyph image removed, with a
lowercase name and with a Zethu name that is not its code point's position. The paint guard
(tools/khelathi-zethu-glyphs/paint_guard.py) is proved on a map without the 11-001 sign's entry and on a
map with a seed of 01-008 moved onto its outline, on a map with one region of the oxen 05-004
left without a seed, and on a map without the closing segments of the river 10-001. The guards run on their
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


def _mentions(table, glyph: str) -> bool:
    """Whether a lookup subtable names `glyph` in a coverage, a class definition or a mapping."""
    table = getattr(table, "ExtSubTable", table)
    for attr in ("Coverage", "InputCoverage", "BacktrackCoverage", "LookAheadCoverage"):
        value = getattr(table, attr, None)
        for cov in value if isinstance(value, list) else [value] if value is not None else []:
            if glyph in cov.glyphs:
                return True
    for attr in ("InputClassDef", "BacktrackClassDef", "LookAheadClassDef", "ClassDef"):
        value = getattr(table, attr, None)
        if value is not None and glyph in value.classDefs:
            return True
    return glyph in (getattr(table, "mapping", None) or {})


def without_lookup(glyph: str):
    """A breaker that takes out of the font's features every substitution lookup whose
    context names `glyph`."""

    def broken(font: Path, out: Path) -> Path:
        f = TTFont(str(font))
        gsub = f["GSUB"].table
        drop = {
            i
            for i, lookup in enumerate(gsub.LookupList.Lookup)
            if any(type(getattr(st, "ExtSubTable", st)).__name__.startswith("Chain") and _mentions(st, glyph) for st in lookup.SubTable)
        }
        for record in gsub.FeatureList.FeatureRecord:
            record.Feature.LookupListIndex = [i for i in record.Feature.LookupListIndex if i not in drop]
            record.Feature.LookupCount = len(record.Feature.LookupListIndex)
        f.save(str(out))
        return out

    return broken


def without_twin(font: Path, out: Path) -> Path:
    """The vertical joiner in the font's own block unmapped."""
    f = TTFont(str(font))
    for table in f["cmap"].tables:
        table.cmap.pop(0x1EC60, None)
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


def without_vmtx(font: Path, out: Path) -> Path:
    """The font without its vertical metrics, so it no longer stands in a column."""
    f = TTFont(str(font))
    del f["vmtx"]
    del f["vhea"]
    f.save(str(out))
    return out


def off_column(font: Path, out: Path) -> Path:
    """One character's vertical advance one unit longer than the em."""
    f = TTFont(str(font))
    height, tsb = f["vmtx"]["tc.teng"]
    f["vmtx"]["tc.teng"] = (height + 1, tsb)
    f.save(str(out))
    return out


def column_825(font: Path, out: Path) -> Path:
    """Every vertical advance and the vhea span 825 units: even columns, but not one em."""
    f = TTFont(str(font))
    for name, (height, tsb) in list(f["vmtx"].metrics.items()):
        f["vmtx"][name] = (825, tsb - 88)
    f["vhea"].ascent, f["vhea"].descent = 412, -413
    f.save(str(out))
    return out


def without_teng(font: Path, out: Path) -> Path:
    """The character for teng, heaven, removed from the cmap."""
    f = TTFont(str(font))
    for table in f["cmap"].tables:
        for code in [c for c, g in table.cmap.items() if g == "tc.teng"]:
            del table.cmap[code]
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


def win_to_line_box(font: Path, out: Path) -> Path:
    """Cut the Windows ascent and descent to the shared table, inside a face's long extenders."""
    f = TTFont(str(font))
    f["OS/2"].usWinAscent, f["OS/2"].usWinDescent = 945, 250
    f.save(str(out))
    return out


def loosened(font: Path, out: Path) -> Path:
    """Widen every advance by 120 units, half on each side of the ink, and on Khelathi Zethu Glyphs and Qalezu Hand with the space widened by 100 units."""
    f = TTFont(str(font))
    hmtx, glyf = f["hmtx"].metrics, f["glyf"]
    moved = {n for n, (adv, _) in hmtx.items() if adv > 0 and (glyf[n].numberOfContours > 0 or glyf[n].isComposite())}
    for name in moved:
        glyph = glyf[name]
        if glyph.isComposite():
            for component in glyph.components:
                if component.glyphName not in moved:
                    component.x += 60
        else:
            glyph.coordinates.translate((60, 0))
        glyph.recalcBounds(glyf)
        adv, lsb = hmtx[name]
        hmtx[name] = (adv + 120, lsb + 60)
    f.save(str(out))
    return out


def wide_space(font: Path, out: Path) -> Path:
    f = TTFont(str(font))
    space = f.getBestCmap()[0x20]
    adv, lsb = f["hmtx"][space]
    f["hmtx"][space] = (adv + 100, lsb)
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
        del entry(manifest, "Khelathi Zethu Glyphs")["codepoints"][0]["key"]

    def share_key(manifest):
        rows = entry(manifest, "Khelathi Zethu Glyphs")["codepoints"]
        rows[1]["key"] = rows[0]["key"]

    def sound_script_key(manifest):
        entry(manifest, "Semaron Kuriale")["codepoints"][0]["key"] = "a"

    cases = [
        ("Khelathi Zethu Glyphs", "KhelathiZethuGlyphs-Regular.ttf", lose_key, "with a sign without a key", "has no key"),
        ("Khelathi Zethu Glyphs", "KhelathiZethuGlyphs-Regular.ttf", share_key, "with two signs on one key", "share the key"),
        ("Semaron Kuriale", "SemaronKuriale-Regular.ttf", sound_script_key, "with a key on a character typed by sound", "typed by sound"),
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
    """Prove that the keyboard guard fails a broken key map, a layout that types the wrong
    thing or a roman letter, and a sounds.json that differs from thalorna's mapping notes."""
    guard = load("keyboards_guard", ROOT / "tools" / "keyboards_guard.py")
    keymap = guard.kk.load()["sounds"]
    committed = guard.committed_sounds()
    sounds = committed["sounds"]
    script = "semaron"
    layouts = guard.read_layouts(script)

    def on_layouts(texts):
        return len(guard.layout_problems(script, keymap, sounds, texts))

    def on_keymap(altered):
        return len(guard.keymap_problems(altered, sounds))

    kk = guard.kk
    real_load = kk.load

    def on_markup(change):
        """Problems of the key map with its markup list altered."""
        data = real_load()
        change(data["markup"])
        kk.load = lambda: data
        try:
            return on_keymap(keymap)
        finally:
            kk.load = real_load

    def keymap_with(change):
        altered = copy.deepcopy(keymap)
        change(altered)
        return altered

    def entry(rows, sound):
        return next(e for e in rows if e["sound"] == sound)

    def share(rows):
        entry(rows, "th")["key"] = entry(rows, "ch")["key"]

    def drop(rows):
        rows.remove(entry(rows, "th"))

    def unshifted(rows):
        entry(rows, "Th")["key"] = "option+q"

    ch = "&#xF0241;&#xF0240;&#xF0236;"
    macos = layouts["macos"].replace(ch, "&#xF0241;", 1)
    linux = "\n".join(line for line in layouts["linux"].split("\n") if "<AC03>" not in line)
    emacs = "\n".join(line for line in layouts["emacs"].split("\n") if not line.startswith(' ("q" '))
    windows = layouts["windows"].decode("utf-16").replace("\r\n10\tQ\t\t0\t-1", "\r\n10\tQ\t\t0\t0071")
    windows = b"\xff\xfe" + windows.encode("utf-16-le")
    def quotes_old(rows):
        entry(rows, "open quote")["key"] = "["
        entry(rows, "close quote")["key"] = "]"

    star = layouts["macos"].replace('<key code="28" output="&#x002A;"/>', "", 1)
    underscore = layouts["linux"].replace("underscore", "VoidSymbol", 1)
    equal = layouts["emacs"].replace("(quail-define-rules\n", '(quail-define-rules\n ("=" [""])\n', 1)
    colon = layouts["windows"].decode("utf-16").replace("\r\n27\tOEM_1\t\t0\t-1\t003a", "\r\n27\tOEM_1\t\t0\t-1\t-1")
    colon = b"\xff\xfe" + colon.encode("utf-16-le")
    good = on_layouts(layouts) + on_keymap(keymap)
    cases = [
        ("with two sounds on one key", on_keymap(keymap_with(share))),
        ("with a sound without a key", on_keymap(keymap_with(drop))),
        ("with a capital off Shift", on_keymap(keymap_with(unshifted))),
        ("with the quotes back on [ and ]", on_keymap(keymap_with(quotes_old))),
        ("with a markup character missing", on_markup(lambda m: m.remove("*"))),
        ("with # listed as markup, on Shift+3, the key of eleven", on_markup(lambda m: m.append("#"))),
        ("with a markup character no key types", on_markup(lambda m: m.append("é"))),
        ("with a macOS key of markup typing nothing", on_layouts({**layouts, "macos": star})),
        ("with a Linux key of markup typing nothing", on_layouts({**layouts, "linux": underscore})),
        ("with an Emacs key of markup given an empty rule", on_layouts({**layouts, "emacs": equal})),
        ("with a Windows key of markup typing nothing", on_layouts({**layouts, "windows": colon})),
        ("with a macOS output cut short", on_layouts({**layouts, "macos": macos})),
        ("with a Linux key line removed", on_layouts({**layouts, "linux": linux})),
        ("with an Emacs rule removed, so the key types itself", on_layouts({**layouts, "emacs": emacs})),
        ("with a Windows key typing a roman letter", on_layouts({**layouts, "windows": windows})),
    ]
    thalorna = Path.home() / "dev/HeroicLands/thalorna"
    if thalorna.exists():
        stale = copy.deepcopy(committed)
        entry(stale["sounds"], "th")["scripts"][script] = {"codepoints": "U+F0241 U+F0236"}
        good += len(guard.thalorna_problems(thalorna, committed))
        cases.append(("with a sounds.json that thalorna no longer spells", len(guard.thalorna_problems(thalorna, stale))))
    else:
        print(f"keyboards: no thalorna checkout at {thalorna}, so the sounds.json proof is skipped")
    status = 0
    for how, bad in cases:
        print(f"keyboards: {good} failures on the layouts, {bad} on the layouts {how}")
        if good or not bad:
            print("tools/keyboards_guard.py: error: the keyboard guard must pass the layouts and fail the altered ones")
            status = 1
    return status


def prove_charts() -> int:
    """Prove that the cheatsheet guard fails a table that loses a row, a chart that loses a cell and a badly written name."""
    guard = load("charts_guard", ROOT / "tools" / "charts_guard.py")
    manifest = json.loads((ROOT / "fonts.json").read_text(encoding="utf-8"))
    entry = next(f for f in manifest["families"] if f["name"] == "Khelathi Zethu Glyphs")
    folder = guard.charts.FOLDERS[entry["class"]]
    base = ROOT / "charts" / folder
    md = (ROOT / "charts" / f"{folder}.md").read_text(encoding="utf-8")
    svgs = {p.name: p.read_text(encoding="utf-8") for p in base.glob("chart-*.svg")}
    glyphs = {p.name for p in (base / "glyphs").glob("*.svg")}
    pngs = {p.name for p in base.glob("chart-*.png")}
    first = entry["codepoints"][0]
    cp, hex_ = guard.charts.code(first), guard.charts.hexcode(first)

    def count(*args):
        return len(guard.sheet_problems(entry, *args))

    def named(rows_name):
        altered = copy.deepcopy(manifest["families"])
        next(f for f in altered if f["name"] == entry["name"])["codepoints"][0]["name"] = rows_name
        return len(guard.name_problems(altered)[0])

    good = count(md, svgs, glyphs, pngs) + named(first["name"])
    cases = [
        ("with a table row removed", count(md.replace(f"`&#{cp};`", ""), svgs, glyphs, pngs)),
        ("with a Code Point cell wrong", count(md.replace(f"| {first['codepoint']} |", "| U+0000 |"), svgs, glyphs, pngs)),
        ("with a chart cell removed", count(md, {k: v.replace(f'id="cp-{hex_}"', 'id="cp-0"') for k, v in svgs.items()}, glyphs, pngs)),
        ("with a glyph image removed", count(md, svgs, glyphs - {f"U+{hex_}.svg"}, pngs)),
        ("with a lowercase name", named(first["name"].lower())),
        ("with a name that is not its code point's position", named("ZETHU CHARACTER 999")),
    ]
    status = 0
    for how, bad in cases:
        print(f"charts: {good} failures on the sheet, {bad} on the sheet {how}")
        if good or not bad:
            print("tools/charts_guard.py: error: the cheatsheet guard must pass the sheet and fail the altered sheet")
            status = 1
    return status


def prove_paint() -> int:
    """Prove that the paint guard fails a map that loses a drawn sign, one with a seed on the outline and one with a figure region unseeded."""
    guard = load("paint_guard", ROOT / "tools" / "khelathi-zethu-glyphs" / "paint_guard.py")
    paint = guard.paint
    data = paint.load()
    enc = paint.encoding()
    glyphs = paint.Glyphs()
    good = guard.check(data, enc, glyphs)

    dropped = copy.deepcopy(data)
    del dropped["signs"]["11-001"]

    on_line = copy.deepcopy(data)
    sid = "01-008"
    seed = on_line["signs"][sid]["regions"][0]
    regions = paint.Regions(glyphs, enc[sid]["glyph"])
    row, col = regions.to_px(*seed["seed"])
    while not regions.ink[row, col]:
        col -= 1
    seed["seed"] = list(regions.to_units(row, col))

    unseeded = copy.deepcopy(data)
    unseeded["signs"]["05-004"]["regions"].pop()

    unclosed = copy.deepcopy(data)
    del unclosed["signs"]["10-001"]["close"]

    status = 0
    for how, bad in (("without the 11-001 map", guard.check(dropped, enc, glyphs)),
                     ("with a seed of 01-008 moved onto its outline", guard.check(on_line, enc, glyphs)),
                     ("with one region of 05-004 left without a seed", guard.check(unseeded, enc, glyphs)),
                     ("without the closing segments of 10-001", guard.check(unclosed, enc, glyphs))):
        print(f"paint: {len(good)} failures on the map, {len(bad)} on the map {how}")
        if good or not bad:
            print("tools/khelathi-zethu-glyphs/paint_guard.py: error: the paint guard must pass the map and fail the altered map")
            status = 1
    return status


STROKE_MIX_PROOF = """
import sys
sys.path.insert(0, "tools/teng-chou")
import characters, components, stroke_mix, syllabary
good = stroke_mix.run()
water = components.COMPONENTS["water"].forms["S"]
water.strokes = [components.Stroke.parse(f"dot {x} {y} l=100") for x, y in
                 ((200, 800), (500, 900), (700, 800), (300, 500), (600, 450), (450, 250))]
dabbed = stroke_mix.run([characters.BY_MORPHEME["shou"]], [])
sign = syllabary.BY_SYLLABLE["ka"]
sign.picks = (0,)
speck = stroke_mix.run([], [sign])
print(len(good), len(dabbed), len(speck))
"""


def prove_stroke_mix() -> int:
    """The stroke-mix guard passes the data and fails water written in dabs, and a
    syllabary sign kept to one stroke. It runs in its own interpreter, since the Teng
    Chou modules share names with other faces' tools."""
    import subprocess

    result = subprocess.run([sys.executable, "-c", STROKE_MIX_PROOF], cwd=ROOT, capture_output=True, text=True)
    try:
        good, dabbed, speck = map(int, result.stdout.split())
    except ValueError:
        print(result.stderr)
        print("tools/teng-chou/stroke_mix.py: error: the proof did not run")
        return 1
    print(f"Teng Chou stroke mix: {good} failures on the data, {dabbed} with water written in dabs, "
          f"{speck} with the sign ka kept to one stroke")
    if good or not dabbed or not speck:
        print("tools/teng-chou/stroke_mix.py: error: the guard must pass the data and fail the altered data")
        return 1
    return 0


def main():
    pirzath = load("pirzath_guard", ROOT / "tools" / "pirzath" / "guard.py")
    hand = load("pirzath_hand_guard", ROOT / "tools" / "pirzath-hand" / "guard.py")
    thuravark = load("thuravark_guard", ROOT / "tools" / "thuravark-carved" / "guard.py")
    qalezu = load("qalezu_guard", ROOT / "tools" / "qalezu-hand" / "guard.py")
    zethu = load("zethu_guard", ROOT / "tools" / "khelathi-zethu-glyphs" / "guard.py")
    quadrats = load("zethu_quadrats", ROOT / "tools" / "khelathi-zethu-glyphs" / "quadrats.py")
    semaron = load("semaron_guard", ROOT / "tools" / "semaron-kuriale" / "guard.py")
    teng_chou = load("teng_chou_guard", ROOT / "tools" / "teng-chou" / "guard.py")
    teng_chou_check = load("teng_chou_check", ROOT / "tools" / "teng-chou" / "check_font.py")
    teng_chou_font = ROOT / "fonts" / "TengChou-Regular.ttf"
    veldikko = load("veldikko_guard", ROOT / "tools" / "veldikko" / "guard.py")
    veldikko_check = load("veldikko_check", ROOT / "tools" / "veldikko" / "check_font.py")
    veldikko_font = ROOT / "fonts" / "Veldikko-Regular.ttf"
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
        ("Veldikko", veldikko_font, lambda p: veldikko.run(p, []), stripped, "without GSUB"),
        ("Veldikko", veldikko_font, lambda p: veldikko.run(p, []), without_gpos, "without GPOS"),
        ("Veldikko", veldikko_font, veldikko_check.check, stripped, "without GSUB"),
        ("Veldikko", veldikko_font, veldikko_check.check, without_gpos, "without GPOS"),
        ("Veldikko", veldikko_font, load("vertical_win", ROOT / "tools" / "vertical.py").check, win_to_line_box,
         "with its Windows ascent and descent cut to the shared line box, inside its risers and tails"),
        ("Teng Chou", teng_chou_font, lambda p: teng_chou.run(p, []), without_teng, "without the character teng"),
        ("Teng Chou", teng_chou_font, teng_chou_check.check, without_teng, "without the character teng"),
        ("Teng Chou", teng_chou_font, teng_chou_check.check, without_vmtx, "without vertical metrics"),
        ("Teng Chou columns", teng_chou_font, load("vertical_columns", ROOT / "tools" / "vertical.py").check, off_column,
         "with one character's vertical advance off the em"),
        ("Teng Chou columns", teng_chou_font, load("vertical_em", ROOT / "tools" / "vertical.py").check, column_825,
         "with every vertical advance 825 units"),
        ("Khelathi Zethu Glyphs", zethu_font, zethu.run, without_sign, "without the 11-001 sign"),
        ("Khelathi Zethu Glyphs", zethu_font, zethu.run, stripped, "without GSUB"),
        ("Khelathi Zethu Glyphs quadrats", zethu_font, quadrats.run, without_lookup("qxf0.p"), "without the lookup that sums a row's widths"),
        ("Khelathi Zethu Glyphs quadrats", zethu_font, quadrats.run, without_gpos, "without GPOS"),
        ("Khelathi Zethu Glyphs quadrats", zethu_font, quadrats.run, without_twin, "without the vertical joiner in its own block"),
        ("Khelathi Zethu Glyphs quadrats", zethu_font, quadrats.run, without_lookup("qcap.l"), "without the cartouche's cord"),
    ]
    codepoints = load("codepoints", ROOT / "tools" / "codepoints.py")
    notdef = load("notdef_box", ROOT / "tools" / "notdef_box.py")
    names = load("font_names", ROOT / "tools" / "font_names.py")
    vertical = load("vertical", ROOT / "tools" / "vertical.py")
    spacing = load("spacing", ROOT / "tools" / "spacing.py")
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
        cases.append((label, font, spacing.check, loosened, "with every advance widened by 120 units"))
        if label in ("KhelathiZethuGlyphs", "QalezuHand"):
            cases.append((label, font, spacing.check, wide_space, "with the space widened by 100 units"))
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
    status |= prove_charts()
    status |= prove_paint()
    status |= prove_stroke_mix()
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
