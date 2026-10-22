# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Sample passages for the Teng Chou specimens and the spacing guard, written in the
lexicons' words.

A Tantsou line is its morphemes, each one character, subject, object and verb in
that order. A Jurthati line takes the character for each content word, by its
meaning, and writes its particles and verb endings in the syllabary: a token
``=ku`` is a sign, any other a character. ``text(line)`` gives the code points.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import codepoint_order  # noqa: E402

# The emperor sees the record of heaven. The people go along the road. Snow on the
# mountain; the water freezes. The master scholar speaks of lore. The warrior has a
# blade in hand. The mother loves the child. The bright moon of the first year.
# The bird of heaven rises.
TANTSOU = [
    "chen teng chou hing".split(),
    "tan tsou dou rou".split(),
    "chai zhen shou chiao".split(),
    "gen chei chou tsuen".split(),
    "wuo huo ja kai".split(),
    "na zhei hin".split(),
    "tsi nie leng you".split(),
    "teng zhai cheng".split(),
    "dao zhuo wou zhong ka".split(),
    "rong tsou wen sing fen".split(),
]

# This unworthy one humbly answers. The emperor sees the record of heaven. The
# warrior has a blade. The mother loves the child, politely said. The bird rises
# from the mountain.
JURTHATI = [
    "=ko =be =i =ku wa =nu =re".split(),
    "chen =ku teng =ri chou =u =n hing =da =n".split(),
    "wuo =ku ja =u =n kai =re".split(),
    "na =ku zhei =u =n hin =re".split(),
    "zhai =ku chai =da =ri cheng =wu".split(),
]


def _points():
    rows = codepoint_order.ltr_table("TengChou-Regular")
    return {r["glyph"]: chr(int(r["codepoint"][2:], 16)) for r in rows}


def text(line) -> str:
    cp = _points()
    return "".join(cp[f"js.{t[1:]}"] if t.startswith("=") else cp[f"tc.{t}"] for t in line)


def lines() -> list[str]:
    return [text(line) for line in TANTSOU + JURTHATI]
