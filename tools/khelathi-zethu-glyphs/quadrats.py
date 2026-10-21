# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Shape quadrats, insertions, segments and cartouches and assert where every sign lands.

    .venv/bin/python tools/khelathi-zethu-glyphs/quadrats.py [--font fonts/KhelathiZethuGlyphs-Regular.ttf]

The texts are written with the format controls in the font's own block (controls.json),
shaped right to left with HarfBuzz, and compared with ``layout.reference``, the same
layout computed in Python. The guard fails when

- a fixture of ``quadrats.json`` or a sample of ``samples.json`` written with joiners
  shapes to other signs, at another scale step or with another advance than the reference,
  or puts a sign's ink centre more than ``TOLERANCE`` units from where the reference puts it;
- the same text with the controls at their Unicode code points shapes differently;
- a run of several quadrats, with spaces and lone signs between them, lays any of them
  out differently from the quadrat alone;
- a seeded sweep of random quadrats, nested to the font's depth and within its largest
  size, disagrees with the reference;
- a cartouche does not open with the tied end and close with the round end, or a sign,
  quadrat or space inside it is not followed by a piece of cord as long as its advance;
- a control with no sign beside it is changed.

A sample's signs are grouped into quadrats by the rules ``specimens.py`` states, and the
signs after a cord-oval sign go into a cartouche in place of the oval.
"""

import argparse
import json
import random
import sys
from pathlib import Path

import uharfbuzz as hb
from fontTools.ttLib import TTFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
import layout  # noqa: E402

FIXTURES = HERE / "quadrats.json"
SAMPLES = HERE / "samples.json"
TOLERANCE = 24  # font units, about 3% of a quadrat: the rounding of the offsets
SWEEP = 200
SEED = 37


def load_fixtures():
    return json.loads(FIXTURES.read_text(encoding="utf-8"))


class Text:
    """Sign ids, control keys and ``sp`` for a space, as text the font shapes."""

    def __init__(self, enc):
        self.code = {e["id"]: int(e["codepoint"][2:], 16) for e in enc["signs"] if e["drawn"]}
        self.glyph = {e["id"]: e["glyph"] for e in enc["signs"] if e["drawn"]}
        self.box = {e["id"]: e["box"]["a"] for e in enc["signs"] if e["drawn"]}
        controls = layout.load_controls()
        self.twin = {c["key"]: int(c["twin"][2:], 16) for c in controls}
        self.unicode = {c["key"]: int(c["codepoint"][2:], 16) for c in controls}

    def string(self, items, unicode=False):
        ctl = self.unicode if unicode else self.twin
        return "".join(" " if t == "sp" else chr(ctl[t] if t in ctl else self.code[t]) for t in items)

    def glyphs(self, items):
        """The quadrat's items as the reference reads them: glyph names and control keys."""
        return [t if t in layout.CONTROL_NAMES else self.glyph[t] for t in items]


class Shaper:
    def __init__(self, path: Path):
        self.font = TTFont(str(path))
        self.order = self.font.getGlyphOrder()
        self.hb = hb.Font(hb.Face(path.read_bytes()))

    def shape(self, text: str):
        """(glyph, x, y, advance) for each glyph in visual order, x and y the pen plus offset."""
        buf = hb.Buffer()
        buf.add_str(text)
        buf.direction = "rtl"
        buf.script = "Zyyy"
        hb.shape(self.hb, buf, {})
        out, x = [], 0
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            out.append((self.order[info.codepoint], x + pos.x_offset, pos.y_offset, pos.x_advance))
            x += pos.x_advance
        return out, x


def drawn(shaped):
    """The signs drawn in a shaped run: (form, step, centre x, centre y)."""
    out = []
    for g, x, y, _ in shaped:
        if g.startswith("z") and ".s" in g:
            form, step = g.rsplit(".s", 1)
            out.append((form, int(step), x, layout.CENTRE_Y + y))
    return out


def compare(label, items, shaper, text, signs) -> list[str]:
    """Shape one quadrat and compare it with the reference."""
    try:
        ref = layout.reference(text.glyphs(items), signs)
    except ValueError as e:
        return [f"{label}: the text does not parse: {e}"]
    shaped, advance = shaper.shape(text.string(items))
    got = drawn(shaped)
    want = [(g, j, x, y) for g, x, y, j in ref["signs"]]
    problems = []
    if advance != ref["advance"]:
        problems.append(f"{label}: advance {advance}, expected {ref['advance']}")
    if len(got) != len(want):
        return problems + [f"{label}: {len(got)} signs laid out, expected {len(want)}: {[g for g, *_ in shaped]}"]
    left = list(got)
    for form, step, x, y in want:
        same = [g for g in left if g[0] == form]
        if not same:
            problems.append(f"{label}: {form} is not laid out")
            continue
        g = min(same, key=lambda g: abs(g[2] - x) + abs(g[3] - y))
        left.remove(g)
        if g[1] != step:
            problems.append(f"{label}: {form} is drawn at step {g[1]}, expected {step}")
        if max(abs(g[2] - x), abs(g[3] - y)) > TOLERANCE:
            problems.append(f"{label}: {form} stands at ({g[2]}, {g[3]:.0f}), expected ({x:.0f}, {y:.0f})")
    unicode_run, _ = shaper.shape(text.string(items, unicode=True))
    if [s[:3] for s in unicode_run] != [s[:3] for s in shaped]:
        problems.append(f"{label}: the Unicode controls shape differently from the font's own")
    return problems


def quadrats_of(text_items):
    """Split a line of items at spaces into its words."""
    words, cur = [], []
    for t in text_items:
        if t == "sp":
            words.append(cur)
            cur = []
        else:
            cur.append(t)
    words.append(cur)
    return [w for w in words if w]


def group(ids, box):
    """Group a sample's signs into quadrats by the specimen rules; each quadrat as items."""
    out, i = [], 0
    flat = lambda s: box[s][1] <= 60  # noqa: E731
    narrow = lambda s: box[s][0] <= 50 and box[s][1] > 60  # noqa: E731
    while i < len(ids):
        a = ids[i]
        b = ids[i + 1] if i + 1 < len(ids) else None
        if b is not None and (a, b) == ("11-001", "11-002"):
            out.append([a, "vj", b])
            i += 2
        elif b is not None and flat(a) and flat(b) and box[a][1] + box[b][1] <= 104:
            out.append([a, "vj", b])
            i += 2
        elif b is not None and box[b][1] <= 40 and box[a][1] <= 64:
            out.append([a, "vj", b])
            i += 2
        elif b is not None and narrow(a) and narrow(b):
            out.append([a, "hj", b])
            i += 2
        else:
            out.append([a])
            i += 1
    return out


def samples(text):
    """Every sample of samples.json as (label, title, its quadrats, the line written with
    joiners): each quadrat a list of items, the line their items with cartouches round
    the framed ones."""
    data = json.loads(SAMPLES.read_text(encoding="utf-8"))
    out = []
    for sc in data["scenes"]:
        for k, s in enumerate(sc["samples"], 1):
            ids = s["ids"]
            if "16-011" in ids:
                at = ids.index("16-011")
                qs = [(q, False) for q in group(ids[:at], text.box)]
                qs += [(q, True) for q in group(ids[at + 1 :], text.box)]
            else:
                qs = [(q, False) for q in group(ids, text.box)]
            out.append((f"{sc['scene']} sample {k}", f"{s['reading']}: {s['gloss']}", qs))
    for ex in data["extra"]:
        qs = []
        for q in ex["quadrats"]:
            items = []
            for r, row in enumerate(q["rows"]):
                if r:
                    items.append("vj")
                for c, sid in enumerate(row):
                    if c:
                        items.append("hj")
                    items.append(sid)
            qs.append((items, q["frame"]))
        out.append((ex["name"], ex["title"], qs))
    return [(label, title, [q for q, _ in qs], line(qs)) for label, title, qs in out]


def line(qs):
    """A sample's quadrats as one line of items: framed quadrats inside one cartouche."""
    items, inside = [], False
    for q, framed in qs:
        if framed and not inside:
            items.append("be")
            inside = True
        if not framed and inside:
            items.append("ee")
            inside = False
        items += q
    if inside:
        items.append("ee")
    return items


def cartouche_problems(label, items, shaper, text) -> list[str]:
    shaped, _ = shaper.shape(text.string(items))
    problems = []
    names = [g for g, *_ in shaped]
    opens = [i for i, g in enumerate(names) if g == "qcap.l"]
    closes = [i for i, g in enumerate(names) if g == "qcap.r"]
    if len(opens) != items.count("ee") or len(closes) != items.count("be"):
        return [f"{label}: {len(opens)} tied ends and {len(closes)} round ends, expected {items.count('ee')} and {items.count('be')}"]
    for a, b in zip(opens, closes):
        if a > b:
            problems.append(f"{label}: a cartouche closes before it opens")
            continue
        x = shaped[a][1] + shaped[a][3]
        end = shaped[b][1]
        cover = x
        for i in range(a + 1, b):
            g, gx, _, adv = shaped[i]
            if g.startswith("qcord."):
                n = int(g.split(".")[1])
                if gx - n > cover + 1:
                    problems.append(f"{label}: the cord breaks at {cover}")
                cover = max(cover, gx)
            elif adv and not names[i + 1].startswith("qcord."):
                problems.append(f"{label}: {g} has no cord after it")
        if abs(cover - end) > layout.CORD_STEP:
            problems.append(f"{label}: the cord runs to {cover}, not to the round end at {end}")
    return problems


def sweep_items(rng, ids, signs, text):
    """A random quadrat as items, nested to the font's depth."""

    def vgroup(depth):
        rows = rng.choice([1, 1, 2, 2, 3] if depth == 0 else [1, 2])
        out = []
        for r in range(rows):
            if r:
                out.append("vj")
            out += hgroup(depth, rows == 1)
        return out

    def hgroup(depth, alone):
        n = rng.choice([2, 3]) if alone else rng.choice([1, 2, 2, 3])
        out = []
        for i in range(n):
            if i:
                out.append("hj")
            out += item(depth)
        return out

    def item(depth):
        r = rng.random()
        if depth < layout.DEPTH - 1 and r < 0.25:
            return ["bs"] + vgroup(depth + 1) + ["es"]
        if r < 0.4:
            return [rng.choice(ids), rng.choice(layout.INSERTS), rng.choice(ids)]
        return [rng.choice(ids)]

    def fits(node):
        if node[0] in ("h", "v"):
            sizes = [natural(n) for n in node[1]]
            w = sum(a for a, _ in sizes) if node[0] == "h" else max(a for a, _ in sizes)
            h = max(b for _, b in sizes) if node[0] == "h" else sum(b for _, b in sizes)
            return w <= layout.MAX and h <= layout.MAX and all(fits(n) for n in node[1])
        return fits(node[1]) if node[0] == "seg" else True

    def natural(node):
        if node[0] == "sign":
            return signs[node[1]].w, signs[node[1]].h
        if node[0] == "seg":
            return natural(node[1])
        if node[0] == "ins":
            return natural(node[2])
        sizes = [natural(n) for n in node[1]]
        if node[0] == "h":
            return sum(a for a, _ in sizes), max(b for _, b in sizes)
        return max(a for a, _ in sizes), sum(b for _, b in sizes)

    while True:
        items = vgroup(0)
        if len(items) > 1 and fits(layout.parse(text.glyphs(items))):
            return items


def run(path: Path, report=None) -> list[str]:
    enc = layout.load_encoding()
    shaper = Shaper(path)
    text = Text(enc)
    signs = layout.signs_of(shaper.font, enc)
    data = load_fixtures()
    problems = []
    counts = {"fixtures": 0, "samples": 0, "sweep": 0, "runs": 0, "cartouches": 0}
    for fx in data["fixtures"]:
        counts["fixtures"] += 1
        problems += compare(fx["name"], fx["text"].split(), shaper, text, signs)
    for label, _, qs, items in samples(text):
        counts["samples"] += 1
        for q in qs:
            if len(q) > 1:
                problems += compare(f"{label} quadrat {' '.join(q)}", q, shaper, text, signs)
        if "be" in items:
            problems += cartouche_problems(label, items, shaper, text)
    for fx in data["cartouches"]:
        counts["cartouches"] += 1
        items = fx["text"].split()
        problems += cartouche_problems(fx["name"], items, shaper, text)
    # a run of quadrats lays each out as it lies alone
    rng = random.Random(SEED)
    ids = sorted(text.code)
    for _ in range(SWEEP // 4):
        counts["runs"] += 1
        words = [sweep_items(rng, ids, signs, text) for _ in range(3)]
        seps = [rng.choice([[], ["sp"], [rng.choice(ids)]]) for _ in range(2)]
        whole = words[0] + seps[0] + words[1] + seps[1] + words[2]
        got, advance = shaper.shape(text.string(whole))
        parts, x0 = [], advance
        for i, part in enumerate([words[0], seps[0], words[1], seps[1], words[2]]):
            if not part:
                continue
            alone, width = shaper.shape(text.string(part))
            x0 -= width
            parts += [(g, x + x0, y) for g, x, y, _ in alone if g.startswith("z")]
        if sorted(parts) != sorted((g, x, y) for g, x, y, _ in got if g.startswith("z")):
            problems.append(f"run {' '.join(whole)}: a quadrat is laid out differently in the run")
    for _ in range(SWEEP):
        counts["sweep"] += 1
        items = sweep_items(rng, ids, signs, text)
        problems += compare(f"sweep {' '.join(items)}", items, shaper, text, signs)
    for c in layout.load_controls():
        lone, _ = shaper.shape(chr(int(c["twin"][2:], 16)))
        want = {"be": "qcap.r", "ee": "qcap.l"}.get(c["key"], c["glyph"])
        if [g for g, *_ in lone] != [want]:
            problems.append(f"{c['twin']} alone shapes to {[g for g, *_ in lone]}, expected {want}")
    if report is not None:
        report.update(counts)
    return problems


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--font", default=str(ROOT / "fonts" / "KhelathiZethuGlyphs-Regular.ttf"))
    args = ap.parse_args()
    counts = {}
    problems = run(Path(args.font), counts)
    for p in problems:
        print(f"{args.font}: error: {p}")
    print(
        f"{args.font}: {counts['fixtures']} fixtures, {counts['samples']} samples, {counts['cartouches']} cartouches, "
        f"{counts['runs']} runs and {counts['sweep']} random quadrats shaped, {len(problems)} failures"
    )
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
