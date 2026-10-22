# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Write fonts.css and fonts.json for the npm package.

    .venv/bin/python tools/write_css.py

fonts.css holds one @font-face rule per built font, named from the font's own
name table (ID 16 when present, else ID 1), with relative URLs so a stylesheet
imported from node_modules or a CDN finds the files beside it. After the rules,
each family has a class, ``hl-<font>``, that sets its ``font-family``,
``font-feature-settings``, ``font-synthesis: none`` (a script face is Regular only, so
bold or italic text in it stays Regular rather than being smeared or slanted) and, for a
right-to-left family, ``direction``.
fonts.json states the same facts for a consumer that reads data: per family the
name, the class, the files, the direction, the OpenType features and ``codepoints``, the table of
every character the face draws (tools/codepoint_order.py defines it). fonts.json is
written in the layout Prettier gives it, so formatting it changes nothing. Both files come from the one table below, so a class and its
features cannot disagree.
"""

import json
import sys
from pathlib import Path

from fontTools.ttLib import TTFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
import codepoint_order  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
WIDTH = 80

# The facts about each font that its file does not state, by file stem. ``features``
# are the OpenType features a run turns on.
# Each entry can have multiple variants (with different names, features, etc.) that share the same TTF file.
FAMILIES = {
    "KhelathiZethuGlyphs-Regular": {
        "slug": "khelathi-zethu-glyphs",
        "direction": "rtl",
        "features": [],
    },
    "PirzathCarved-Regular": {
        "slug": "pirzath-carved",
        "direction": "ltr",
        "features": [],
    },
    "PirzathHand-Regular": {
        "slug": "pirzath-hand",
        "direction": "ltr",
        "features": ["ss01"],
        "variants": [
            {
                "name": "Pirzath Hand Lifted",
                "slug": "pirzath-hand-lifted",
                "features": [],
            },
        ],
    },
    "QalezuHand-Regular": {
        "slug": "qalezu-hand",
        "direction": "rtl",
        "features": [],
    },
    "SemaronKuriale-Regular": {
        "slug": "semaron-kuriale",
        "direction": "ltr",
        "features": [],
    },
    "TengChou-Regular": {
        "slug": "teng-chou",
        "direction": "ltr",
        "features": [],
    },
    "ThuravarkCarved-Regular": {
        "slug": "thuravark-carved",
        "direction": "ltr",
        "features": [],
    },
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


def facts(ttf: Path) -> dict:
    try:
        return FAMILIES[ttf.stem]
    except KeyError:
        raise SystemExit(f"{ttf}: no entry in FAMILIES in tools/write_css.py") from None


def class_rule(ttf: Path) -> str:
    fact = facts(ttf)
    features = ", ".join(f'"{tag}"' for tag in fact["features"]) or "normal"
    lines = [
        f".hl-{fact['slug']} {{",
        f'    font-family: "{family_name(ttf)}";',
        f"    font-feature-settings: {features};",
        "    font-synthesis: none;",
    ]
    if fact["direction"] == "rtl":
        lines.append("    direction: rtl;")
    lines.append("}")
    return "\n".join(lines) + "\n"


def manifest_entry(ttf: Path, variant: dict | None = None) -> dict:
    fact = facts(ttf)

    # For variants, use variant-specific values where provided
    if variant is not None:
        name = variant.get("name", fact.get("name", family_name(ttf)))
        slug = variant.get("slug", fact["slug"])
        features = variant.get("features", fact["features"])
    else:
        name = fact.get("name", family_name(ttf))
        slug = fact["slug"]
        features = fact["features"]

    entry = {
        "name": name,
        "family": family_name(ttf),
        "class": f"hl-{slug}",
        "files": {
            "woff2": f"fonts/{ttf.stem}.woff2",
            "ttf": f"fonts/{ttf.stem}.ttf",
        },
        "direction": fact["direction"],
        "features": features,
    }
    entry["codepoints"] = codepoint_order.table(ttf.stem)
    return entry


def dump(value, level: int = 0, trailing: int = 0) -> str:
    """Serialize as Prettier lays JSON out: four-space indents, and an object or array
    on one line when it fits in 80 columns with its trailing comma."""
    pad = " " * (4 * level)
    inner = " " * (4 * (level + 1))
    if isinstance(value, dict):
        flat = "{ " + ", ".join(f"{json.dumps(k)}: {dump(v)}" for k, v in value.items()) + " }"
        if level > 0 and all(not isinstance(v, (dict, list)) for v in value.values()) and len(pad) + len(flat) + trailing <= WIDTH:
            return flat
        items = [f"{inner}{json.dumps(k)}: {dump(v, level + 1, 1)}" for k, v in value.items()]
        return "{\n" + ",\n".join(items) + f"\n{pad}}}"
    if isinstance(value, list):
        if all(not isinstance(v, (dict, list)) for v in value):
            return "[" + ", ".join(json.dumps(v, ensure_ascii=False) for v in value) + "]"
        items = [f"{inner}{dump(v, level + 1, 1)}" for v in value]
        return "[\n" + ",\n".join(items) + f"\n{pad}]"
    return json.dumps(value, ensure_ascii=False)


def variant_class_rule(ttf: Path, variant: dict) -> str:
    fact = facts(ttf)
    slug = variant.get("slug", fact["slug"])
    features = variant.get("features", fact["features"])
    name = family_name(ttf)
    lines = [
        f".hl-{slug} {{",
        f'    font-family: "{name}";',
    ]
    feature_str = ", ".join(f'"{tag}"' for tag in features) or "normal"
    lines.append(f"    font-feature-settings: {feature_str};")
    lines.append("    font-synthesis: none;")
    if fact["direction"] == "rtl":
        lines.append("    direction: rtl;")
    lines.append("}")
    return "\n".join(lines) + "\n"


def main() -> None:
    fonts = sorted((ROOT / "fonts").glob("*.ttf"))
    rules = "\n".join(font_face(ttf) for ttf in fonts)

    # Generate class rules for main entries and variants
    class_rules = []
    for ttf in fonts:
        class_rules.append(class_rule(ttf))
        fact = facts(ttf)
        if "variants" in fact:
            for variant in fact["variants"]:
                class_rules.append(variant_class_rule(ttf, variant))
    classes = "\n".join(class_rules)

    (ROOT / "fonts.css").write_text(rules + "\n" + classes, encoding="utf-8")

    # Generate manifest entries for main entries and variants
    manifest_entries = []
    for ttf in fonts:
        manifest_entries.append(manifest_entry(ttf))
        fact = facts(ttf)
        if "variants" in fact:
            for variant in fact["variants"]:
                manifest_entries.append(manifest_entry(ttf, variant))

    manifest = {"version": 1, "families": manifest_entries}
    (ROOT / "fonts.json").write_text(dump(manifest) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
