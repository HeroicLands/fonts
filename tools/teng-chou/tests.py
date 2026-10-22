# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Made-up test characters for the stroke sheet, placed by hand on a 1000-unit em.

They exercise the strokes in combination: weight against weight, terminal against
terminal, and the density of a full square. They are tests, not characters of
the script, and none is a real Chinese character.
"""

import strokes as S

TESTS = [
    # left and right: a narrow rod column beside a coiled frame
    ("test A", [
        ("rods", 70, 870, {"l": 240, "gap": 54}),
        ("needle", 175, 745, {"l": 620}),
        ("rise", 60, 300, {"l": 230, "a": 30}),
        ("coil", 390, 860, {"l1": 520, "l2": 720, "r": 70}),
        ("horizontal", 470, 650, {"l": 300}),
        ("scale", 480, 480, {"l": 190, "a": -12}),
        ("barb-dot", 590, 340, {"l": 80}),
    ]),
    # top and bottom: a tallied lid over a closed frame and a bent foot
    ("test B", [
        ("tally", 170, 940, {"l": 190}),
        ("barb-dot", 640, 950, {"l": 90}),
        ("horizontal", 90, 790, {"l": 820, "rise": 3.5}),
        ("vertical", 260, 700, {"l": 300}),
        ("turn", 260, 710, {"l1": 480, "l2": 300}),
        ("rods", 330, 580, {"l": 300, "gap": 50}),
        ("horizontal", 270, 420, {"l": 460, "rise": 2.5}),
        ("sweep-turn", 330, 330, {"l1": 130, "l2": 260, "rise": 14}),
        ("bend-spur", 560, 360, {"l1": 240, "l2": 360, "r": 70, "spur": 85}),
    ]),
    # dense left and right
    ("test C", [
        ("dot", 150, 930, {"l": 80}),
        ("rods", 60, 800, {"l": 260, "gap": 50}),
        ("vertical-spur", 170, 690, {"l": 560, "spur": 75}),
        ("tally", 40, 520, {"l": 130}),
        ("rise", 40, 260, {"l": 150, "a": 34}),
        ("scale", 400, 930, {"l": 150, "a": -20}),
        ("scale", 560, 900, {"l": 150, "a": -20}),
        ("scale", 720, 870, {"l": 150, "a": -20}),
        ("vertical", 400, 770, {"l": 420}),
        ("turn-spur", 400, 780, {"l1": 480, "l2": 440, "spur": 75}),
        ("horizontal", 450, 650, {"l": 360}),
        ("horizontal", 450, 520, {"l": 360}),
        ("needle", 640, 870, {"l": 600}),
        ("horizontal", 330, 310, {"l": 600, "rise": 3}),
        ("dot-left", 470, 230, {"l": 100}),
        ("tally", 640, 240, {"l": 190}),
    ]),
    # the wind frame: a sweep and a coil round an inner part
    ("test D", [
        ("sweep", 210, 860, {"l": 760, "a": -105, "curl": 0.15}),
        ("coil", 220, 870, {"l1": 560, "l2": 720, "r": 70}),
        ("barb-dot", 470, 780, {"l": 80}),
        ("rods", 340, 640, {"l": 320, "gap": 52}),
        ("needle", 480, 520, {"l": 300}),
        ("scale", 330, 470, {"l": 130, "a": -25}),
        ("tally", 520, 420, {"l": 160}),
        ("fall-flat", 300, 290, {"l": 440}),
    ]),
    # from the lower left: a long flat fall under an inner part
    ("test E", [
        ("tally", 80, 900, {"l": 180}),
        ("sweep-turn", 150, 700, {"l1": 150, "l2": 200, "rise": 20}),
        ("barb-dot", 110, 480, {"l": 90}),
        ("dot-left", 190, 360, {"l": 90}),
        ("turn-sweep", 360, 860, {"l1": 420, "l2": 260}),
        ("horizontal", 360, 680, {"l": 480}),
        ("vertical", 540, 760, {"l": 360}),
        ("corner", 420, 560, {"l1": 180, "l2": 360}),
        ("scale", 640, 520, {"l": 130}),
        ("fall-flat", 60, 250, {"l": 900, "a": -8}),
    ]),
]


def assemble(parts):
    return S.union([S.stroke(sid, x, y, **params) for sid, x, y, params in parts])


def count(parts):
    return len(parts)
