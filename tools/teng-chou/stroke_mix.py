# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Confirm that every Teng Chou character and sign is written in strokes, not dabs.

    .venv/bin/python tools/teng-chou/stroke_mix.py [--report] [--components]

Every stroke of a laid-out character is measured along its brush path, in the
1000-unit em it is drawn on, and is

- a **dab** when it is a bead (``dot``, ``dot-left``, ``barb-dot``, ``tally``),
  whatever its length, or its path is shorter than ``DAB`` (0.15 em);
- **long** when its path is ``LONG`` (0.35 em) or longer;
- **short** otherwise: a real stroke of modest length, between a dab and a long stroke.

A character fails when it has more than ``MAX_DABS`` (5) dabs, or more dabs than
long and short strokes together. A sign of the Jurthati syllabary fails when it
has more dabs than long and short strokes together, or fewer than two strokes that
are not dabs. The tally of five (``tally.py``) fails on any dab. ``--report`` prints the mix of every character and sign, the means
and the worst; ``--components`` prints each component's standalone mix.
"""

from __future__ import annotations

import math
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import characters as C  # noqa: E402
import components as K  # noqa: E402
import layout as Y  # noqa: E402
import syllabary as J  # noqa: E402
import tally as T  # noqa: E402

DAB = 150  # units of the 1000-unit em
LONG = 350
MAX_DABS = 5
BEADS = {"dot", "dot-left", "barb-dot", "tally"}


def length(tracks) -> float:
    """The length of a stroke's brush path: its longest track, the one the brush runs."""
    best = 0.0
    for t in tracks:
        best = max(best, sum(math.dist(a[:2], b[:2]) for a, b in zip(t.samples, t.samples[1:])))
    return best


def kind(sid: str, tracks) -> str:
    n = length(tracks)
    if sid in BEADS or n < DAB:
        return "dab"
    return "long" if n >= LONG else "short"


def mix(strokes) -> dict[str, int]:
    """``{"long": n, "short": n, "dab": n}`` for ``[(part, stroke, tracks), ...]``."""
    out = {"long": 0, "short": 0, "dab": 0}
    for _, st, g in strokes:
        out[kind(st.sid, g)] += 1
    return out


def character_mix(ch: C.Character) -> dict[str, int]:
    strokes, _, _ = Y.strokes_of(ch.formula, ch.overrides)
    return mix(strokes)


def sign_mix(sign: J.Sign) -> dict[str, int]:
    """A sign's strokes, measured on the source character's em, as they were chosen."""
    return mix(J.chosen(sign))


def character_problems(m: dict[str, int]) -> list[str]:
    out = []
    if m["dab"] > MAX_DABS:
        out.append(f"{m['dab']} dabs, more than {MAX_DABS}")
    if m["dab"] > m["long"] + m["short"]:
        out.append(f"{m['dab']} dabs against {m['long'] + m['short']} long and short strokes")
    return out


def sign_problems(m: dict[str, int]) -> list[str]:
    out = []
    if m["dab"] > m["long"] + m["short"]:
        out.append(f"{m['dab']} dabs against {m['long'] + m['short']} long and short strokes")
    if m["long"] + m["short"] < 2:
        out.append(f"{m['long'] + m['short']} strokes that are not dabs, fewer than 2")
    return out


def run(characters=None, signs=None) -> list[str]:
    characters = C.CHARACTERS if characters is None else characters
    signs = J.SIGNS if signs is None else signs
    out = []
    for ch in characters:
        m = character_mix(ch)
        out += [f"tools/teng-chou/characters.py: error: {ch.morpheme}: {p} ({fmt(m)})" for p in character_problems(m)]
    for stage in T.STAGES.values():
        m = mix(T.strokes_of(stage.count))
        if stage.count == 5:
            out += [f"tools/teng-chou/tally.py: error: the tally: {p} ({fmt(m)})" for p in character_problems(m)]
            if m["dab"]:
                out.append(f"tools/teng-chou/tally.py: error: the tally has {m['dab']} dabs; it is written in strokes alone")
    for sign in signs:
        m = sign_mix(sign)
        out += [f"tools/teng-chou/syllabary.py: error: {sign.syllable}: {p} ({fmt(m)})" for p in sign_problems(m)]
    return out


def fmt(m) -> str:
    return f"{m['long']} long, {m["short"]} short, {m['dab']} dabs"


def report():
    rows = [(ch.morpheme, character_mix(ch)) for ch in C.CHARACTERS]
    for key in ("long", "short", "dab"):
        print(f"characters: mean {key} {statistics.mean(m[key] for _, m in rows):.2f}")
    worst = sorted(rows, key=lambda r: (r[1]["dab"] - r[1]["long"] - r[1]["short"], r[1]["dab"]), reverse=True)[:15]
    print("most dabs against strokes: " + "; ".join(f"{k} {fmt(m)}" for k, m in worst))
    srows = [(s.syllable, sign_mix(s)) for s in J.SIGNS]
    for key in ("long", "short", "dab"):
        print(f"signs: mean {key} {statistics.mean(m[key] for _, m in srows):.2f}")
    worst = sorted(srows, key=lambda r: (r[1]["dab"] - r[1]["long"] - r[1]["short"], r[1]["dab"]), reverse=True)[:10]
    print("signs, most dabs: " + "; ".join(f"{k} {fmt(m)}" for k, m in worst))


def components_report():
    for cid, comp in K.COMPONENTS.items():
        formula = comp.idc or "{" + cid + "}"
        strokes, _, _ = Y.strokes_of(formula)
        print(f"{cid:10} {fmt(mix(strokes))}")


def main():
    args = sys.argv[1:]
    if "--components" in args:
        components_report()
        return
    if "--report" in args:
        report()
    problems = run()
    for p in problems:
        print(p)
    print(f"{len(C.CHARACTERS)} characters and {len(J.SIGNS)} signs: "
          + ("ok" if not problems else f"{len(problems)} problems"))
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
