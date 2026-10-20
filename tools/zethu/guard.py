# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Shape every sign of every scene inscription right to left and assert the font draws it.

    .venv/bin/python tools/zethu/guard.py [--font fonts/KhelathiZethu-Regular.ttf]

``samples.json`` holds the sample inscriptions of the setting's scenes and the dates and
numbers beside them, each a list of sign ids. The guard writes each as the string of its
signs' code points, shapes it with HarfBuzz in a right-to-left run and asserts that:

- every sign gives its own default glyph, in reverse order for the visual run, never
  ``.notdef`` or the box;
- every form of every sign gives its glyph through the features: ``ss01`` and the first
  alternate of ``salt`` give the second form, ``ss02`` and the second alternate of ``salt``
  give the third, and a sign without that form keeps its default;
- the default-ignorable characters between signs shape to nothing and leave the signs
  unchanged.

The guard reads no lexicon: the samples and the encoding are in this directory.
"""

import argparse
import json
import sys
from pathlib import Path

import uharfbuzz as hb
from fontTools.ttLib import TTFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
ENCODING = HERE / "encoding.json"
SAMPLES = HERE / "samples.json"


def cp(text: str) -> int:
    return int(text[2:], 16)


def gname(sid: str, v: str) -> str:
    return "z" + sid.replace("-", "_") + "." + v


def sample_lists():
    """[(label, [sign ids])] for every scene sample and every extra sample."""
    data = json.loads(SAMPLES.read_text(encoding="utf-8"))
    out = []
    for sc in data["scenes"]:
        for k, s in enumerate(sc["samples"], 1):
            out.append((f"{sc['scene']} sample {k}: {s['reading']}", s["ids"]))
    for ex in data["extra"]:
        ids = [i for q in ex["quadrats"] for row in q["rows"] for i in row]
        out.append((ex["name"], ids))
    return out


class Shaper:
    def __init__(self, path: Path):
        self.data = path.read_bytes()
        self.order = TTFont(str(path)).getGlyphOrder()
        self.font = hb.Font(hb.Face(self.data))
        self.font.scale = (1000, 1000)

    def shape(self, text: str, features=None):
        buf = hb.Buffer()
        buf.add_str(text)
        buf.direction = "rtl"
        buf.script = "Zyyy"
        hb.shape(self.font, buf, features or {})
        return [
            (self.order[i.codepoint], p.x_advance)
            for i, p in zip(buf.glyph_infos, buf.glyph_positions)
        ]


def run(path: Path, report=None) -> list[str]:
    """Every failure of the font at `path`; `report`, if given, collects the counts."""
    enc = json.loads(ENCODING.read_text(encoding="utf-8"))
    code = {e["id"]: cp(e["codepoint"]) for e in enc["signs"] if e["drawn"]}
    variants = {e["id"]: e["variants"] for e in enc["signs"] if e["drawn"]}
    shaper = Shaper(path)
    failures = []
    counts = {"samples": 0, "signs": 0, "variant shapings": 0}

    for label, ids in sample_lists():
        counts["samples"] += 1
        missing = [i for i in ids if i not in code]
        if missing:
            failures.append(f"{label}: the signs {missing} are not in the encoding")
            continue
        text = "".join(chr(code[i]) for i in ids)
        want = [gname(i, "a") for i in ids][::-1]
        got = [g for g, _ in shaper.shape(text)]
        counts["signs"] += len(ids)
        if ".notdef" in got or "notdef.box" in got or got != want:
            failures.append(f"{label}: shaped {got}, expected {want}")
        # ignorables between the signs draw nothing and change nothing
        spaced = "‏".join(chr(code[i]) for i in ids)
        got = [g for g, adv in shaper.shape(spaced) if g not in ("ignorable", "ignorable.sub")]
        if got != want:
            failures.append(f"{label}: the signs change when separated by ignorables")

    every = "".join(chr(c) for c in code.values())
    ids = list(code)
    cases = [
        ({"ss01": True}, lambda i: "b" if "b" in variants[i] else "a"),
        ({"ss02": True}, lambda i: "c" if "c" in variants[i] else "a"),
        ({"salt": 1}, lambda i: "b" if "b" in variants[i] else "a"),
        ({"salt": 2}, lambda i: "c" if "c" in variants[i] else "a"),
        ({}, lambda i: "a"),
    ]
    for features, pick in cases:
        counts["variant shapings"] += 1
        got = [g for g, _ in shaper.shape(every, features)]
        want = [gname(i, pick(i)) for i in ids][::-1]
        if ".notdef" in got or "notdef.box" in got or got != want:
            bad = [(w, g) for w, g in zip(want, got) if w != g][:3]
            failures.append(f"features {features or 'none'}: forms differ, first {bad}")
    if report is not None:
        report.update(counts)
    return failures


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--font", default=str(ROOT / "fonts" / "KhelathiZethu-Regular.ttf"))
    args = ap.parse_args()
    counts = {}
    failures = run(Path(args.font), counts)
    for f in failures:
        print(f"{args.font}: error: {f}")
    print(
        f"{args.font}: {counts['samples']} samples, {counts['signs']} signs shaped, "
        f"{counts['variant shapings']} variant shapings, {len(failures)} failures"
    )
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
