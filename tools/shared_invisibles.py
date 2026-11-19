# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Read shared sound metadata code points from the published registry."""

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = """
import { SHARED_SOUNDS, SHARED_SOUND_CONTROLS }
    from '@heroiclands/package-build/engine/encoding-standard';
console.log(JSON.stringify([
    ...Object.values(SHARED_SOUNDS).map(value => value.invisible.codePointAt(0)),
    ...Object.entries(SHARED_SOUND_CONTROLS)
        .filter(([key]) => key !== 'legacyShort')
        .map(([, value]) => value.codePointAt(0))
]));
"""


def codepoints():
    result = subprocess.run(
        ["node", "--input-type=module", "-e", REGISTRY],
        cwd=ROOT, text=True, capture_output=True, check=True,
    )
    return set(json.loads(result.stdout))


def prepare(font, family):
    """Add the metadata glyphs and filter them from adjacent shaping lookups."""
    points = codepoints()
    old = font["ignorable"]
    old.unicodes = sorted(set(old.unicodes) - points)
    for name in ("shared.invisible", "shared.invisible.sub"):
        glyph = font.newGlyph(name)
        glyph.width = 0
    font["shared.invisible"].unicodes = sorted(points)
    order = list(font.lib["public.glyphOrder"])
    order.extend(["shared.invisible", "shared.invisible.sub"])
    font.lib["public.glyphOrder"] = order
    categories = font.lib.setdefault("public.openTypeCategories", {})
    marks = sorted(name for name, category in categories.items() if category == "mark")
    categories["shared.invisible"] = "base"
    categories["shared.invisible.sub"] = "mark"
    text = font.features.text.replace(
        "sub ignorable by ignorable.sub;",
        "sub ignorable by ignorable.sub;\n  sub shared.invisible by shared.invisible.sub;",
        1,
    )
    if "GlyphClassDef" in text:
        text = text.replace("[grave], ;", "[grave shared.invisible.sub], ;")
        text = text.replace("[lengthmark doubling], ;", "[lengthmark doubling shared.invisible.sub], ;")
    flag = "lookupflag IgnoreMarks;" if not marks else "lookupflag UseMarkFilteringSet @SHARED_RETAINED_MARKS;"
    if marks:
        lines = text.splitlines(keepends=True)
        last = max(i for i, line in enumerate(lines) if line.startswith("languagesystem "))
        lines.insert(last + 1, "@SHARED_RETAINED_MARKS = [" + " ".join(marks) + "];\n")
        text = "".join(lines)
    selectors = {
        "HelonikaBook": ("lookup strays {", "feature kern {"),
        "PirzathCarved": ("feature rlig {", "feature kern {"),
        "PirzathHand": ("feature liga {", "feature rlig {"),
        "QalezuHand": ("feature rlig {",),
        "SemaronKuriale": ("lookup ccmp_catch {",),
        "ThuravarkCarved": ("lookup ccmp_acute {", "feature ss01 {"),
        "VedyaksharaClassical": tuple("lookup " + name + " {" for name in
            ("softdot", "fused", "rhalf", "rfinal", "rfoot", "half", "final", "vowels", "strays")),
        "Veldikko": ("lookup vowels {",),
    }
    for selector in selectors[family]:
        if text.count(selector) != 1:
            raise ValueError(f"{family}: expected one {selector}")
        text = text.replace(selector, selector + "\n  " + flag, 1)
    font.features.text = text
