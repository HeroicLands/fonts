# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Confirm that the Teng Chou characters are distinct from each other at body size.

    .venv/bin/python tools/teng-chou/character_distinct.py [--report]

Each character is rendered as it stands in a line of text, with the measure of
``syllabary_distinct.py``: ``PX`` pixels to the em, softened by a pixel, two
characters compared by the cosine of their images. Characters that share a
component, as most do, are alike by construction; ``LIMIT`` sits above the closest
pair of distinct characters, so a pair above it is two characters drawn the same.
"""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import characters as C  # noqa: E402
import layout as Y  # noqa: E402
import syllabary_distinct as D  # noqa: E402

LIMIT = 0.97


def images() -> dict:
    return {c.morpheme: D.image(Y.render_char(c.morpheme)) for c in C.CHARACTERS}


def alike() -> tuple[list, list]:
    """Every pair of characters by similarity, and the pairs above ``LIMIT``."""
    found = D.pairs(images())
    return found, [p for p in found if p[0] > LIMIT]


def main():
    found, bad = alike()
    if "--report" in sys.argv[1:]:
        for sim, a, b in found[:25]:
            print(f"{a:>6} {b:>6} {sim:.3f}")
    for sim, a, b in bad:
        print(f"tools/teng-chou/characters.py:{C.row_line(b)}:1: error: the characters {a} and {b} are alike at {D.PX} px ({sim:.3f} > {LIMIT})")
    print(f"{len(C.CHARACTERS)} characters: " + ("ok" if not bad else f"{len(bad)} pairs alike"))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
