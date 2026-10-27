# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Prove that each guard passes a built font and fails the same font broken.

    .venv/bin/python tools/prove_guards.py [--font FONT | --shared]

``--font FONT`` proves only the guards broken on that built font, and ``--shared`` only
the proofs that break no font, so that the two together, over every font, are the whole
proof; ``tools/check.py`` runs them that way, in parallel.

The broken Pirzath and Thuravark fonts are the built .ttf with the GSUB table
removed, so no ligature, decomposition or contextual rule applies. Pirzath Hand's
font check (tools/pirzath-hand/check_font.py) is proved with the GPOS table removed,
so that no length mark stands over its vowel pair. Thuravark's
guard is also proved without the lookup that frames a crowned name, without the
bound runes of ``ss01``, and with the bound runes on in plain text; its font check
is proved without ``ss01``. The broken
Qalezu Hand font has one sign, the th, removed from its cmap; its guard and its font
check are also each proved on it with the GSUB table removed, so that no catch fuses
with the sign after it. Khelathi Zethu Glyphs is broken
twice: once with one sign, the crocodile-hunt house 11-001, removed from its cmap,
and once with the GSUB table removed so that no second or third form is reachable. Its
quadrat guard (tools/khelathi-zethu-glyphs/quadrats.py) is proved four times: with the
lookup that sums a row's widths taken out of the features, with the GPOS table removed,
with the vertical joiner in the font's own block unmapped, and with the lookup that lays
the cord along a cartouche taken out.
Teng Chou is broken three times: its guard (tools/teng-chou/guard.py) and its font
check (tools/teng-chou/check_font.py) on the font with the character for teng removed from
its cmap, and the font check on the font without its vertical metrics; and the vertical
guard is proved on its columns with one character's vertical advance off the em, and with
every vertical advance 825 units, even but not one em. Its
stroke-mix guard (tools/teng-chou/stroke_mix.py) is proved on its data with water written in
six dabs, and with the syllabary sign ka kept to one stroke.
Chalish Pilam Common is broken three times: its guard (tools/chalish-pilam/guard.py) and its
font check (tools/chalish-pilam/check_font.py) on the font with the glyph for the sun removed
from its cmap, and the font check on the font with one glyph's advance off the cell.
Chalish Pilam Ceremonial's font check (tools/chalish-pilam/check_ceremonial_font.py) is
broken twice: with the glyph for the sun removed from its cmap, and with one glyph's
advance off its block's.
Semaron Kuriale is broken twice: with the GSUB table removed, so that no
th, long vowel or spelled-out ch applies, and with the GPOS table removed, so that no catch stands on its
base. Veldikko's guard (tools/veldikko/guard.py) and its font check
(tools/veldikko/check_font.py) are each proved twice: with the GSUB table removed, so that no
letter joins and no vowel takes its signs, and with the GPOS table removed, so that no mark
stands over its letter; and the vertical guard is proved on Veldikko with its Windows ascent and
descent cut to the shared line box, so that its risers and tails would be clipped.
Vedyakshara Classical's guard (tools/vedyakshara/guard.py) is proved with the GSUB table
removed, so that no form is drawn, and its font check (tools/vedyakshara/check_font.py)
with the GSUB table removed and with the GPOS table removed, so that no vowel sign
stands on its anchor; and the vertical guard is proved on it with its Windows ascent and
descent cut to the shared line box, so that its hooks would be clipped. Helonika Book's
guard (tools/helonika/guard.py) is proved with the small letter th removed from the cmap, and again
with the small letter kh removed, and its font check (tools/helonika/check_font.py) with the GSUB table removed, so that a
stray accent is not the box, and with the GPOS table removed, so that the accent does
not stand over its vowel. The box guard (tools/notdef_box.py) is proved on every font twice: with the question
mark removed from the cmap, and with it pointed at glyph 0. The name guard
(tools/font_names.py) is proved on every font twice: with the Macintosh full name
removed, and with the Basic Latin range declared. The vertical guard (tools/vertical.py) is proved on every font three times: with the hhea ascent changed,
with USE_TYPO_METRICS cleared, and with one glyph lifted out of the band. The code-point guard (tools/codepoints.py)
is proved on every font with the first code point of its fonts.json table removed from the cmap, with the Latin a mapped
to its first character, and with a ligature that writes its third character from its first two, a spelling rule; and on
every left-to-right font with an entry in the Basic Multilingual Plane's Private Use Area. Its block registry is proved on a code point outside its family's blocks, two overlapping blocks and a DEVELOPING.md table that
differs from the registry. The spacing guard (tools/spacing.py) is proved on every font with every advance widened by 120 units,
half on each side of the ink, and on Khelathi Zethu Glyphs and Qalezu Hand with the space widened by 100 units. The default-ignorable check of the box guard is proved on every font with the glyph of the ignorables drawing the box, and on
Pirzath Carved without GSUB and with its space glyph drawing the dot. The code guard (tools/codes_guard.py) is proved on
a fonts.json with one character's code removed, with a code that is not the code table's, with a code outside
``[A-Za-z0-9_]``, and with two characters of a face on one code, and on code tables with two code points on one code, with a
code point no face draws, and with a Zethu sign's code differing from the font's build table; and it passes Teng Chou's
``KA`` and ``ka``, two codes that differ in case alone. The cheatsheet guard (tools/charts_guard.py) is proved on a sheet with a table row removed, with a wrong Code Point cell, with a wrong Code cell, with a chart cell removed, with a glyph image removed, with a
lowercase name and with a Zethu name that is not its code point's position. The paint guard
(tools/khelathi-zethu-glyphs/paint_guard.py) is proved on a map without the 11-001 sign's entry and on a
map with a seed of 01-008 moved onto its outline, on a map with one region of the oxen 05-004
left without a seed, and on a map without the closing segments of the river 10-001. The specimen-page check (tools/specimen_pages.py --check) is proved on
Qalezu Hand's page with a line's roman spelling changed, with a line's glyph codes changed, on a family
with no page, and with its README sample cell an unlinked relative image.
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


def dotted_space(font: Path, out: Path) -> Path:
    """Pirzath Carved without GSUB and with its space glyph drawing the dot, as space.dot
    does, so that HarfBuzz draws an unsubstituted ignorable as the dot."""
    f = TTFont(str(font))
    del f["GSUB"]
    f["glyf"]["space"] = f["glyf"]["space.dot"]
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
    """Whether a lookup subtable names `glyph` in a coverage, a class definition or an alternate map."""
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


def without_feature(tag: str):
    """A breaker that empties the feature `tag`, so none of its lookups applies."""

    def broken(font: Path, out: Path) -> Path:
        f = TTFont(str(font))
        for record in f["GSUB"].table.FeatureList.FeatureRecord:
            if record.FeatureTag == tag:
                record.Feature.LookupListIndex = []
                record.Feature.LookupCount = 0
        f.save(str(out))
        return out

    return broken


def always_on(tag: str):
    """A breaker that adds the lookups of the feature `tag` to ccmp, which every shaper
    applies, so the feature is on with no request."""

    def broken(font: Path, out: Path) -> Path:
        f = TTFont(str(font))
        records = f["GSUB"].table.FeatureList.FeatureRecord
        indices = [i for r in records if r.FeatureTag == tag for i in r.Feature.LookupListIndex]
        for record in records:
            if record.FeatureTag == "ccmp":
                record.Feature.LookupListIndex = sorted(set(record.Feature.LookupListIndex) | set(indices))
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


def without_sun(font: Path, out: Path) -> Path:
    """Chalish Pilam Common's glyph for the sun removed from the cmap."""
    f = TTFont(str(font))
    for table in f["cmap"].tables:
        for code in [c for c, g in table.cmap.items() if g == "sun"]:
            del table.cmap[code]
    f.save(str(out))
    return out


def off_cell(font: Path, out: Path) -> Path:
    """One glyph of Chalish Pilam Common given an advance other than the cell's."""
    f = TTFont(str(font))
    width, bearing = f["hmtx"]["moon"]
    f["hmtx"]["moon"] = (width + 10, bearing)
    f.save(str(out))
    return out


def off_block(font: Path, out: Path) -> Path:
    """One glyph of Chalish Pilam Ceremonial given an advance other than its block's."""
    f = TTFont(str(font))
    width, bearing = f["hmtx"]["moon"]
    f["hmtx"]["moon"] = (width + 10, bearing)
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


def _listed(font: Path) -> list[dict]:
    return next(f for f in json.loads((ROOT / "fonts.json").read_text(encoding="utf-8"))["families"]
                if Path(f["files"]["ttf"]).name == font.name)["codepoints"]


def latin_drawn(font: Path, out: Path) -> Path:
    """The Latin letter a mapped to the face's first character, as a typing rule would."""
    glyph = _listed(font)[0]["glyph"]
    f = TTFont(str(font))
    for table in f["cmap"].tables:
        if table.isUnicode():
            table.cmap[0x61] = glyph
    f.save(str(out))
    return out


def spelling_rule(font: Path, out: Path) -> Path:
    """A ligature that writes the face's third character from its first two, a spelling rule."""
    from fontTools.otlLib.builder import buildLigatureSubstSubtable, buildLookup

    rows = [r for r in _listed(font) if r["kind"] != "control"]
    a, b, c = (r["glyph"] for r in rows[:3])
    f = TTFont(str(font))
    gsub = f["GSUB"].table
    gsub.LookupList.Lookup.append(buildLookup([buildLigatureSubstSubtable({(a, b): c})]))
    gsub.LookupList.LookupCount = len(gsub.LookupList.Lookup)
    index = len(gsub.LookupList.Lookup) - 1
    for record in gsub.FeatureList.FeatureRecord:
        record.Feature.LookupListIndex.append(index)
        record.Feature.LookupCount = len(record.Feature.LookupListIndex)
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


def without_th(font: Path, out: Path) -> Path:
    """The glyph th removed from the cmap: Helonika Book's small letter th or Qalezu Hand's sign th,
    so a word with it prints the box."""
    f = TTFont(str(font))
    for table in f["cmap"].tables:
        for code in [c for c, g in table.cmap.items() if g == "th"]:
            del table.cmap[code]
    f.save(str(out))
    return out


def without_kh(font: Path, out: Path) -> Path:
    """Helonika Book's small letter kh removed from the cmap, so a Bizarian or Bethuan word with it prints the box."""
    f = TTFont(str(font))
    for table in f["cmap"].tables:
        for code in [c for c, g in table.cmap.items() if g == "kh"]:
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
    run("with a table in DEVELOPING.md that differs", "table differs", readme)
    return status


def prove_codes() -> int:
    """Prove that the code guard fails a fonts.json or a code table that breaks a rule, and passes
    codes that differ in case alone."""
    guard = load("codes_guard", ROOT / "tools" / "codes_guard.py")
    doc, tables, stated = guard.manifest(), guard.tables(), guard.build_codes()

    def family(manifest, name):
        return next(f for f in manifest["families"] if f["name"] == name)

    def on_manifest(change):
        altered = copy.deepcopy(doc)
        change(altered)
        return len(guard.problems(altered, tables, stated))

    def on_tables(change):
        altered = copy.deepcopy(tables)
        change(altered)
        return len(guard.problems(doc, altered, stated))

    def lose(m):
        del family(m, "Pirzath Carved")["codepoints"][0]["code"]

    def other(m):
        family(m, "Pirzath Carved")["codepoints"][0]["code"] = "OTHER"

    def badly_written(m):
        family(m, "Qalezu Hand")["codepoints"][0]["code"] = "LA-GUN"

    def shared(m):
        rows = family(m, "Helonika Book")["codepoints"]
        rows[1]["code"] = rows[0]["code"]

    def shared_table(t):
        first = next(iter(t["veldikko"]))
        second = list(t["veldikko"])[1]
        t["veldikko"][second] = t["veldikko"][first]

    def undrawn(t):
        t["thuravark"]["U+F01FF"] = "UNDRAWN"

    def unstated():
        altered = copy.deepcopy(stated)
        point = next(iter(altered["zethu"]))
        altered["zethu"][point] = "OTHER"
        return len(guard.problems(doc, tables, altered))

    teng_chou = set(tables["tengchou"].values())
    good = len(guard.problems(doc, tables, stated))
    cases = [
        ("with one character's code removed", on_manifest(lose)),
        ("with a code that is not the code table's", on_manifest(other)),
        ("with a code outside [A-Za-z0-9_]", on_manifest(badly_written)),
        ("with two characters of a face on one code", on_manifest(shared)),
        ("with two code points of a table on one code", on_tables(shared_table)),
        ("with a code point no face draws", on_tables(undrawn)),
        ("with a Zethu sign's code differing from the build table", unstated()),
    ]
    status = 0
    if not {"KA", "ka"} <= teng_chou:
        print("tools/codes/tengchou.json: error: the proof needs Teng Chou's KA and ka, two codes that differ in case alone")
        status = 1
    for how, bad in cases:
        print(f"glyph codes: {good} failures on the tables, {bad} on the tables {how}")
        if good or not bad:
            print("tools/codes_guard.py: error: the code guard must pass the tables and fail the altered ones")
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
        ("with a Code cell wrong", count(md.replace(f"| `{first['code']}` |", "| `OTHER` |"), svgs, glyphs, pngs)),
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


def prove_specimen_pages() -> int:
    """Prove that the specimen-page check fails a page or image out of date with its texts,
    a family with no page, and a README sample cell that is not the absolute URL linked to its page."""
    pages = load("specimen_pages", ROOT / "tools" / "specimen_pages.py")
    texts = json.loads(pages.TEXTS.read_text(encoding="utf-8"))
    family = next(f for f in pages.manifest() if f["class"] == "hl-qalezu-hand")
    real_rows = pages.readme_rows

    def count(families, altered=texts):
        return len(pages.check(families, altered))

    def roman_changed():
        altered = copy.deepcopy(texts)
        altered["families"]["hl-qalezu-hand"]["lines"][0]["roman"] = "Shelmu zetem"
        return count([family], altered)

    def codes_changed():
        altered = copy.deepcopy(texts)
        line = altered["families"]["hl-qalezu-hand"]["lines"][0]
        line["codes"] = altered["families"]["hl-qalezu-hand"]["lines"][1]["codes"]
        return count([family], altered)

    def no_page():
        extra = {**family, "class": "hl-qalezu-proof"}
        altered = copy.deepcopy(texts)
        altered["families"]["hl-qalezu-proof"] = altered["families"]["hl-qalezu-hand"]
        return count([extra], altered)

    def relative_cell():
        rows = real_rows()
        rows[family["name"]][3] = f"![{family['name']}](specimens/readme/{family['class']}.png)"
        pages.readme_rows = lambda: rows
        try:
            return count([family])
        finally:
            pages.readme_rows = real_rows

    good = count([family])
    status = 0
    for how, bad in (
        ("with a line's roman spelling changed", roman_changed()),
        ("with a line's glyph codes changed", codes_changed()),
        ("with a family that has no page", no_page()),
        ("with a README sample cell by relative path, unlinked", relative_cell()),
    ):
        print(f"specimen pages: {good} failures on the pages, {bad} on the pages {how}")
        if good or not bad:
            print("tools/specimen_pages.py: error: the specimen-page check must pass the pages and fail the altered ones")
            status = 1
    return status


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
    vedyakshara = load("vedyakshara_guard", ROOT / "tools" / "vedyakshara" / "guard.py")
    vedyakshara_check = load("vedyakshara_check", ROOT / "tools" / "vedyakshara" / "check_font.py")
    vedyakshara_font = ROOT / "fonts" / "VedyaksharaClassical-Regular.ttf"
    chalish = load("chalish_guard", ROOT / "tools" / "chalish-pilam" / "guard.py")
    chalish_check = load("chalish_check", ROOT / "tools" / "chalish-pilam" / "check_font.py")
    chalish_font = ROOT / "fonts" / "ChalishPilamCommon-Regular.ttf"
    # The ceremonial hand's modules share names such as strokes and syllabary with other
    # scripts' tools, so its font check is loaded with no script's modules cached, and
    # theirs are put back after.
    scripts = ROOT / "tools"
    shared = {
        n: sys.modules.pop(n) for n, m in list(sys.modules.items())
        if Path(getattr(m, "__file__", None) or "/").parent.parent == scripts
    }
    ceremonial_check = load("ceremonial_check", ROOT / "tools" / "chalish-pilam" / "check_ceremonial_font.py")
    sys.modules.update(shared)
    ceremonial_font = ROOT / "fonts" / "ChalishPilamCeremonial-Regular.ttf"
    helonika = load("helonika_guard", ROOT / "tools" / "helonika" / "guard.py")
    helonika_check = load("helonika_check", ROOT / "tools" / "helonika" / "check_font.py")
    helonika_font = ROOT / "fonts" / "HelonikaBook-Regular.ttf"
    zethu_font = ROOT / "fonts" / "KhelathiZethuGlyphs-Regular.ttf"
    cases = [
        (
            "Pirzath Carved",
            ROOT / "fonts" / "PirzathCarved-Regular.ttf",
            pirzath.run,
            stripped,
            "without GSUB",
        ),
        (
            "Pirzath Hand",
            ROOT / "fonts" / "PirzathHand-Regular.ttf",
            hand.run,
            stripped,
            "without GSUB",
        ),
        (
            "Pirzath Hand",
            ROOT / "fonts" / "PirzathHand-Regular.ttf",
            load("pirzath_hand_check", ROOT / "tools" / "pirzath-hand" / "check_font.py").check,
            without_gpos,
            "without GPOS, so that no length mark stands over its pair",
        ),
        (
            "Thuravark Carved",
            ROOT / "fonts" / "ThuravarkCarved-Regular.ttf",
            thuravark.shaping,
            stripped,
            "without GSUB",
        ),
        (
            "Thuravark Carved",
            ROOT / "fonts" / "ThuravarkCarved-Regular.ttf",
            thuravark.shaping,
            without_lookup("crown.open"),
            "without the lookup that frames a crowned name",
        ),
        (
            "Thuravark Carved",
            ROOT / "fonts" / "ThuravarkCarved-Regular.ttf",
            thuravark.shaping,
            without_feature("ss01"),
            "without the bound runes",
        ),
        (
            "Thuravark Carved",
            ROOT / "fonts" / "ThuravarkCarved-Regular.ttf",
            thuravark.shaping,
            always_on("ss01"),
            "with the bound runes on in plain text",
        ),
        (
            "Thuravark Carved",
            ROOT / "fonts" / "ThuravarkCarved-Regular.ttf",
            load("thuravark_check", ROOT / "tools" / "thuravark-carved" / "check_font.py").check,
            without_feature("ss01"),
            "without ss01",
        ),
        (
            "Qalezu Hand",
            ROOT / "fonts" / "QalezuHand-Regular.ttf",
            qalezu.run,
            without_th,
            "without the th sign",
        ),
        (
            "Qalezu Hand",
            ROOT / "fonts" / "QalezuHand-Regular.ttf",
            qalezu.run,
            stripped,
            "without GSUB, so that no catch fuses with its sign",
        ),
        (
            "Qalezu Hand",
            ROOT / "fonts" / "QalezuHand-Regular.ttf",
            load("qalezu_check", ROOT / "tools" / "qalezu-hand" / "check_font.py").check,
            stripped,
            "without GSUB, so that no catch fuses with its sign",
        ),
        (
            "Semaron Kuriale",
            ROOT / "fonts" / "SemaronKuriale-Regular.ttf",
            semaron.run,
            stripped,
            "without GSUB",
        ),
        (
            "Semaron Kuriale",
            ROOT / "fonts" / "SemaronKuriale-Regular.ttf",
            semaron.run,
            without_gpos,
            "without GPOS",
        ),
        ("Veldikko", veldikko_font, veldikko.run, stripped, "without GSUB"),
        ("Veldikko", veldikko_font, veldikko.run, without_gpos, "without GPOS"),
        ("Veldikko", veldikko_font, veldikko_check.check, stripped, "without GSUB"),
        ("Veldikko", veldikko_font, veldikko_check.check, without_gpos, "without GPOS"),
        ("Veldikko", veldikko_font, load("vertical_win", ROOT / "tools" / "vertical.py").check, win_to_line_box,
         "with its Windows ascent and descent cut to the shared line box, inside its risers and tails"),
        ("Vedyakshara Classical", vedyakshara_font, vedyakshara.run, stripped, "without GSUB"),
        ("Vedyakshara Classical", vedyakshara_font, vedyakshara_check.check, stripped, "without GSUB"),
        ("Vedyakshara Classical", vedyakshara_font, vedyakshara_check.check, without_gpos, "without GPOS"),
        ("Vedyakshara Classical", vedyakshara_font, load("vertical_ved", ROOT / "tools" / "vertical.py").check,
         win_to_line_box, "with its Windows ascent and descent cut to the shared line box, inside its hooks"),
        ("Helonika Book", helonika_font, helonika.run, without_th, "without the small letter th"),
        ("Helonika Book", helonika_font, helonika.run, without_kh, "without the small letter kh"),
        ("Helonika Book", helonika_font, helonika.run, without_gpos, "without GPOS, so a space after the raised dot keeps its advance"),
        ("Helonika Book", helonika_font, helonika_check.check, stripped, "without GSUB"),
        ("Helonika Book", helonika_font, helonika_check.check, without_gpos, "without GPOS"),
        ("Teng Chou", teng_chou_font, teng_chou.run, without_teng, "without the character teng"),
        ("Teng Chou", teng_chou_font, teng_chou_check.check, without_teng, "without the character teng"),
        ("Teng Chou", teng_chou_font, teng_chou_check.check, without_vmtx, "without vertical metrics"),
        ("Teng Chou columns", teng_chou_font, load("vertical_columns", ROOT / "tools" / "vertical.py").check, off_column,
         "with one character's vertical advance off the em"),
        ("Teng Chou columns", teng_chou_font, load("vertical_em", ROOT / "tools" / "vertical.py").check, column_825,
         "with every vertical advance 825 units"),
        ("Chalish Pilam Common", chalish_font, chalish.run, without_sun, "without the glyph sun"),
        ("Chalish Pilam Common", chalish_font, chalish_check.check, without_sun, "without the glyph sun"),
        ("Chalish Pilam Common", chalish_font, chalish_check.check, off_cell, "with the advance of moon off the cell"),
        ("Chalish Pilam Ceremonial", ceremonial_font, ceremonial_check.check, without_sun, "without the glyph sun"),
        ("Chalish Pilam Ceremonial", ceremonial_font, ceremonial_check.check, off_block,
         "with the advance of moon off its block"),
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
        cases.append((label, font, codepoints.check, latin_drawn, "with the Latin a drawn as its first character"))
        cases.append((label, font, codepoints.check, spelling_rule, "with a ligature that writes one character from two"))
        if font.name.split("-")[0] in ("PirzathCarved", "PirzathHand", "ThuravarkCarved", "SemaronKuriale", "VedyaksharaClassical", "HelonikaBook"):
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
    only = next((Path(sys.argv[i + 1]).resolve() for i, arg in enumerate(sys.argv[:-1]) if arg == "--font"), None)
    shared = "--shared" in sys.argv[1:]
    if only is not None:
        cases = [case for case in cases if case[1].resolve() == only]
        if not cases:
            print(f"{only}: error: no guard is proved on this font")
            sys.exit(1)
    if shared:
        cases = []
    status = 0
    with tempfile.TemporaryDirectory() as tmp:
        passed = {}  # a guard's findings on an unbroken font, which several breakings share
        for label, font, guard, break_font, how in cases:
            if (guard, font) not in passed:
                passed[(guard, font)] = guard(font)
            good = passed[(guard, font)]
            bad = guard(break_font(font, Path(tmp) / font.name))
            ok = not good and bad
            print(f"{label}: {len(good)} failures on the font, {len(bad)} on the font {how}")
            if not ok:
                print(f"{font}: error: the guard must pass the font and fail the broken font")
                status = 1
    if only is not None:
        sys.exit(status)
    status |= prove_registry(codepoints)
    status |= prove_codes()
    status |= prove_charts()
    status |= prove_paint()
    status |= prove_stroke_mix()
    status |= prove_specimen_pages()
    pirzath_font = ROOT / "fonts" / "PirzathCarved-Regular.ttf"
    with tempfile.TemporaryDirectory() as tmp:
        good, bad = notdef.check(pirzath_font), notdef.check(dotted_space(pirzath_font, Path(tmp) / pirzath_font.name))
        print(f"Pirzath Carved: {len(good)} failures on the font, {len(bad)} on the font without GSUB whose space glyph draws the dot, which an ignorable then draws")
        if good or not bad:
            print(f"{pirzath_font}: error: the ignorable check must pass the font and fail the font without GSUB whose space glyph draws the dot")
            status = 1
    sys.exit(status)


if __name__ == "__main__":
    main()
