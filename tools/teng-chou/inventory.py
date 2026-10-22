# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""The Teng Chou component inventory: every component as strokes, in stroke order.

Each form is drawn in its own box (``box``: width, height; the standalone box is
the 1000-unit em). See ``components.py`` for the stroke notation and the assembler.
"""

from components import COMPONENTS, define

L = (420, 1000)
R = (460, 1000)
T = (1000, 440)
B = (1000, 440)

# -- the elements and the weather -------------------------------------------------------------

define("water", "water, liquid", "meaning", "shou", positions="L B", lookalike="水, 氵", forms={
    "S": {"strokes": [
        "horizontal 130 775 l=273 rise=6",
        "needle 500 910 l=800",
        "horizontal 600 584 l=286 rise=6",
        "sweep-short 400 400 l=220 a=-150",
        "fall 640 330 l=240 a=-50 foot=0.22",
    ]},
    "L": {"box": L, "strokes": [
        "sweep-short 200 880 l=200 a=-145",
        "sweep 300 640 l=230 a=-125 curl=0.1",
        "rise 50 250 l=280 a=42",
    ]},
    "B": {"box": B, "strokes": [
        "sweep-short 300 400 l=200 a=-145",
        "sweep-short 740 400 l=200 a=-145",
        "fall-flat 100 190 l=800 a=-6",
    ]},
})

define("fire", "fire, heat", "meaning", "ho", positions="L B", lookalike="火, 灬", forms={
    "S": {"strokes": [
        "sweep 300 800 l=230 a=-125 curl=0.1",
        "sweep 470 900 l=660 a=-120 curl=0.3",
        "slant-spur 520 860 l=640 a=-64 spur=80",
        "horizontal 380 420 l=221 rise=6",
    ]},
    "L": {"box": L, "strokes": [
        "sweep 120 800 l=230 a=-125 curl=0.1",
        "sweep 230 900 l=640 a=-112 curl=0.2",
        "horizontal 230 542 l=200 rise=6",
        "rise 60 260 l=200 a=40",
    ]},
    "B": {"box": B, "strokes": [
        "sweep-short 250 380 l=200 a=-145",
        "fall 330 380 l=240 a=-52 foot=0.2",
        "fall 540 380 l=240 a=-52 foot=0.2",
        "fall 740 380 l=240 a=-52 foot=0.2",
    ]},
})

define("wood", "wood, tree", "meaning", "mou", positions="L T B", lookalike="木", forms={
    "S": {"strokes": [
        "sweep-short 534 950 l=200 a=-145",
        "vertical-spur 500 860 l=760 spur=90",
        "sweep-short 470 700 l=240 a=-150",
        "fall 560 600 l=240 a=-40 foot=0.22",
        "sweep-short 470 450 l=220 a=-155",
        "fall 560 360 l=240 a=-40 foot=0.22",
    ]},
    "L": {"box": L, "strokes": [
        "sweep-short 246 950 l=200 a=-145",
        "vertical-spur 240 860 l=760 spur=80",
        "sweep-short 220 700 l=170 a=-150",
        "fall 280 600 l=240 a=-40 foot=0.22",
        "sweep-short 220 450 l=160 a=-155",
    ]},
    "T": {"box": T, "strokes": [
        "sweep-short 530 430 l=200 a=-145",
        "vertical 500 330 l=300",
        "sweep-short 470 260 l=220 a=-160",
        "fall 560 230 l=240 a=-40 foot=0.22",
        "sweep-short 470 140 l=200 a=-160",
    ]},
    "B": {"box": B, "strokes": [
        "sweep-short 530 430 l=200 a=-145",
        "vertical-spur 500 330 l=300 spur=80",
        "sweep-short 470 260 l=220 a=-160",
        "fall 560 230 l=240 a=-40 foot=0.22",
    ]},
})

define("earth", "earth, soil, ground", "meaning", "tou", positions="L B", lookalike="土", forms={
    "S": {"strokes": [
        "sweep 360 800 l=230 a=-125 curl=0.1",
        "vertical-spur 500 880 l=580 spur=80",
        "horizontal 590 600 l=221 rise=6",
        "fall-flat 110 200 l=800",
    ]},
    "L": {"box": L, "strokes": [
        "sweep 120 800 l=230 a=-125 curl=0.1",
        "vertical 210 880 l=600",
        "horizontal 250 623 l=200 rise=6",
        "rise 40 230 l=300 a=30",
    ]},
    "B": {"box": B, "strokes": [
        "sweep 380 400 l=230 a=-125 curl=0.1",
        "vertical 500 430 l=240",
        "horizontal 570 321 l=208 rise=6",
        "fall-flat 80 110 l=840",
    ]},
})

define("metal", "metal, gold", "meaning", "jing", positions="L B", lookalike="金", forms={
    "S": {"strokes": [
        "horizontal 140 820 l=720",
        "needle 220 820 l=640 lean=-20",
        "vertical-spur 760 820 l=640 spur=90",
        "horizontal 360 676 l=260 rise=6",
        "horizontal 380 476 l=260 rise=6",
        "fall-flat 110 160 l=800",
    ]},
    "L": {"box": L, "strokes": [
        "horizontal 50 840 l=330",
        "needle 90 840 l=600 lean=-14",
        "vertical-spur 330 840 l=620 spur=60",
        "horizontal 130 702 l=200 rise=6",
        "horizontal 130 502 l=200 rise=6",
        "rise 40 200 l=320 a=28",
    ]},
    "B": {"box": B, "strokes": [
        "horizontal 140 410 l=720",
        "needle 220 410 l=300 lean=-14",
        "vertical-spur 760 410 l=300 spur=80",
        "horizontal 360 306 l=260 rise=6",
        "fall-flat 100 80 l=800",
    ]},
})

define("mountain", "mountain, height", "meaning", "chai", positions="T L", lookalike="山", forms={
    "S": {"strokes": [
        "needle 500 920 l=760",
        "rise 130 260 l=320 a=48",
        "fall 560 640 l=360 a=-52",
        "fall-flat 100 180 l=820",
    ]},
    "T": {"box": T, "strokes": [
        "needle 500 430 l=330",
        "rise 160 110 l=260 a=40",
        "fall 560 330 l=300 a=-34",
        "horizontal 100 90 l=800 rise=2",
    ]},
    "L": {"box": L, "strokes": [
        "needle 210 920 l=760",
        "rise 40 300 l=240 a=48",
        "fall 230 640 l=240 a=-42 foot=0.2",
        "rise 40 160 l=320 a=26",
    ]},
})

define("sky", "heaven, the vault of the sky", "meaning", "teng", positions="T", lookalike="天", forms={
    "S": {"strokes": [
        "horizontal 110 860 l=780",
        "vertical 220 720 l=440",
        "turn-spur 220 730 l1=560 l2=560 spur=100",
        "horizontal 380 596 l=260 rise=6",
    ]},
    "T": {"box": T, "strokes": [
        "horizontal 100 410 l=800",
        "vertical 220 320 l=220",
        "turn-spur 220 330 l1=560 l2=260 spur=90",
        "horizontal 390 246 l=260 rise=6",
    ]},
})

define("sun", "sun, day, light of day", "meaning", None, positions="L T B", lookalike="日", forms={
    "B": {"box": B, "strokes": [
        "vertical 320 410 l=300",
        "turn-spur 320 420 l1=380 l2=330 spur=80",
        "fall 470 300 l=240 a=-55 foot=0.22",
        "horizontal 340 140 l=340",
        "rise 180 90 l=180 a=26",
    ]},
    "S": {"strokes": [
        "vertical 280 800 l=600",
        "turn-spur 280 810 l1=460 l2=660 spur=100",
        "fall 460 560 l=240 a=-55 foot=0.22",
        "horizontal 300 230 l=420",
        "rise 120 160 l=240 a=30",
    ]},
    "L": {"box": L, "strokes": [
        "vertical 90 800 l=560",
        "turn-spur 90 810 l1=260 l2=620 spur=80",
        "fall 180 560 l=240 a=-55 foot=0.22",
        "horizontal 110 270 l=240",
        "rise 30 180 l=160 a=34",
    ]},
    "T": {"box": T, "strokes": [
        "vertical 320 410 l=300",
        "turn-spur 320 420 l1=380 l2=330 spur=80",
        "fall 470 300 l=240 a=-55 foot=0.22",
        "horizontal 340 140 l=340",
        "rise 180 90 l=180 a=26",
    ]},
})

define("moon", "moon, month, night", "meaning", "you", positions="L R", lookalike="月", forms={
    "S": {"strokes": [
        "sweep-short 610 950 l=200 a=-145",
        "sweep 400 860 l=740 a=-118 curl=0.7",
        "scale 450 650 l=220 a=-20 sag=0.42",
        "scale 470 420 l=220 a=-20 sag=0.42",
    ]},
    "L": {"box": L, "strokes": [
        "sweep-short 289 950 l=200 a=-145",
        "sweep 180 860 l=780 a=-100 curl=0.6",
        "scale 210 680 l=170 a=-25 sag=0.42",
        "scale 220 440 l=160 a=-25 sag=0.42",
    ]},
    "R": {"box": R, "strokes": [
        "sweep-short 316 950 l=200 a=-145",
        "sweep 200 860 l=800 a=-100 curl=0.6",
        "scale 230 680 l=190 a=-25 sag=0.42",
        "scale 250 440 l=180 a=-25 sag=0.42",
    ]},
})

define("cloud", "cloud, vapour", "meaning", "yan", positions="T", lookalike="云", forms={
    "S": {"strokes": [
        "sweep-short 310 860 l=200 a=-145",
        "sweep-short 740 880 l=200 a=-145",
        "turn-sweep 260 680 l1=480 l2=360 a=-128",
        "fall-flat 160 260 l=720",
    ]},
    "T": {"box": T, "strokes": [
        "sweep-short 306 430 l=200 a=-145",
        "sweep-short 746 430 l=200 a=-145",
        "turn-sweep 300 320 l1=420 l2=200 a=-140",
        "fall-flat 160 110 l=700",
    ]},
})

define("rain", "rain, weather", "meaning", None, positions="T", lookalike="雨", forms={
    "T": {"box": T, "strokes": [
        "horizontal 100 400 l=800",
        "vertical 180 330 l=270",
        "turn 180 330 l1=640 l2=270",
        "sweep-short 420 280 l=220 a=-140",
        "sweep-short 650 270 l=220 a=-140",
        "sweep-short 540 170 l=220 a=-140",
    ]},
})

define("wind", "wind, air in motion", "meaning", None, positions="⿵", lookalike="風's frame 𠘨",
       novel="coil", forms={
    "⿵": {"inner": (300, 120, 740, 760), "strokes": [
        "sweep 220 880 l=780 a=-104 curl=0.15",
        "coil 230 890 l1=560 l2=760 r=70",
    ]},
})

define("ice", "ice, cold", "meaning", None, positions="L B", lookalike="冫", forms={
    "B": {"box": B, "strokes": [
        "sweep-short 380 420 l=180 a=-150",
        "sweep-short 640 400 l=180 a=-150",
        "rise 160 100 l=240 a=24",
    ]},
    "L": {"box": L, "strokes": [
        "fall 130 800 l=280 a=-50 foot=0.22",
        "fall 150 580 l=280 a=-50 foot=0.22",
        "rise 60 280 l=300 a=44",
    ]},
})

define("stone", "stone, rock", "meaning", None, positions="L B", lookalike="石", forms={
    "S": {"strokes": [
        "horizontal 140 800 l=720",
        "sweep 420 800 l=600 a=-125 curl=0.3",
        "horizontal 470 565 l=273 rise=6",
        "fall-flat 340 280 l=500",
    ]},
    "L": {"box": L, "strokes": [
        "horizontal 50 820 l=330",
        "sweep 220 820 l=620 a=-112 curl=0.3",
        "horizontal 180 582 l=200 rise=6",
        "rise 150 270 l=220 a=24",
    ]},
    "B": {"box": B, "strokes": [
        "horizontal 140 400 l=720",
        "sweep 420 400 l=320 a=-140 curl=0.2",
        "horizontal 470 296 l=260 rise=6",
        "fall-flat 340 110 l=500",
    ]},
})

define("plant", "plant, grass, herb", "meaning", None, positions="T", lookalike="艹", forms={
    "T": {"box": T, "strokes": [
        "rise 140 130 l=240 a=44",
        "rise 400 120 l=280 a=46",
        "rise 680 130 l=220 a=42",
        "horizontal 100 80 l=800 rise=2",
    ]},
})

define("grain", "grain, harvest", "meaning", None, positions="L T", lookalike="禾", forms={
    "T": {"box": T, "strokes": [
        "sweep-short 520 440 l=200 a=-145",
        "sweep-short 640 400 l=180 a=-150",
        "vertical-spur 500 360 l=300 spur=70",
        "horizontal 250 230 l=221 rise=6",
        "horizontal 140 200 l=720",
    ]},
    "L": {"box": L, "strokes": [
        "sweep-short 250 960 l=200 a=-145",
        "sweep-short 340 860 l=200 a=-150",
        "vertical-spur 210 820 l=740 spur=70",
        "horizontal 40 502 l=200 rise=6",
    ]},
})

define("field", "field, cultivated land", "meaning", "nou", positions="L B T", lookalike="田", forms={
    "S": {"strokes": [
        "corner 200 840 l1=640 l2=640",
        "horizontal 300 660 l=460",
        "horizontal 300 450 l=460",
        "needle 540 880 l=560",
    ]},
    "L": {"box": L, "strokes": [
        "corner 70 840 l1=620 l2=300",
        "horizontal 130 660 l=240",
        "horizontal 130 450 l=240",
        "needle 250 880 l=560",
    ]},
    "B": {"box": B, "strokes": [
        "corner 200 400 l1=300 l2=640",
        "horizontal 300 320 l=460",
        "horizontal 300 210 l=460",
        "needle 540 420 l=300",
    ]},
    "T": {"box": T, "strokes": [
        "corner 200 420 l1=320 l2=640",
        "horizontal 300 330 l=460",
        "horizontal 300 210 l=460",
        "needle 540 430 l=320",
    ]},
})

define("jade", "jade, precious stone", "meaning", None, positions="L", lookalike="王, 玉", forms={
    "L": {"box": L, "strokes": [
        "horizontal 50 860 l=320 rise=4",
        "vertical 210 900 l=640",
        "horizontal 70 600 l=260 rise=4",
        "scale 250 470 l=150 a=-30",
        "rise 40 220 l=320 a=26",
    ]},
})

# -- the body --------------------------------------------------------------------------------

define("person", "person, human act", "meaning", "nong", positions="L T", lookalike="人, 亻", forms={
    "S": {"strokes": [
        "sweep-short 600 950 l=190 a=-150",
        "sweep-turn 500 830 l1=320 l2=200 rise=26",
        "slant-spur 520 640 l=480 a=-60 spur=80",
    ]},
    "L": {"box": L, "strokes": [
        "sweep 320 940 l=230 a=-125 curl=0.1",
        "sweep-turn 290 840 l1=200 l2=170 rise=28",
        "vertical-spur 230 680 l=620 spur=70",
    ]},
    "T": {"box": T, "strokes": [
        "sweep-short 620 440 l=190 a=-150",
        "sweep-turn 500 380 l1=220 l2=160 rise=20",
        "fall-flat 520 330 l=380 a=-12",
    ]},
})

define("woman", "woman, female", "meaning", "mi", positions="L B", lookalike="女", forms={
    "S": {"strokes": [
        "sweep-short 600 960 l=190 a=-150",
        "sweep-turn 470 840 l1=300 l2=400 rise=22",
        "sweep 720 720 l=560 a=-125 curl=0.3",
        "horizontal 300 356 l=260 rise=6",
    ]},
    "L": {"box": L, "strokes": [
        "sweep-short 340 960 l=190 a=-150",
        "sweep-turn 230 860 l1=240 l2=220 rise=26",
        "sweep 360 760 l=560 a=-112 curl=0.3",
        "horizontal 50 362 l=200 rise=6",
    ]},
    "B": {"box": B, "strokes": [
        "sweep-short 600 440 l=190 a=-150",
        "sweep-turn 460 380 l1=200 l2=400 rise=14",
        "sweep 720 330 l=300 a=-140 curl=0.3",
        "horizontal 300 98 l=234 rise=6",
    ]},
})

define("child", "child, offspring", "meaning", "zhei", positions="L B", lookalike="子", forms={
    "S": {"strokes": [
        "sweep-short 650 950 l=190 a=-150",
        "sweep-turn 470 840 l1=260 l2=380 rise=24",
        "vertical-spur 520 620 l=480 spur=90",
        "horizontal 640 540 l=221 rise=6",
    ]},
    "L": {"box": L, "strokes": [
        "sweep-short 350 960 l=190 a=-150",
        "sweep-turn 230 860 l1=180 l2=220 rise=24",
        "vertical-spur 230 660 l=560 spur=70",
    ]},
    "B": {"box": B, "strokes": [
        "sweep-short 630 440 l=190 a=-150",
        "sweep-turn 460 380 l1=150 l2=360 rise=18",
        "vertical-spur 520 290 l=240 spur=70",
        "horizontal 640 241 l=208 rise=6",
    ]},
})

define("hand", "hand, handling", "meaning", "huo", positions="L B", lookalike="手, 扌", forms={
    "S": {"strokes": [
        "sweep-short 494 940 l=200 a=-145",
        "turn-spur 280 790 l1=460 l2=660 spur=100",
        "sweep 220 560 l=230 a=-125 curl=0.1",
        "rise 560 300 l=260 a=30",
    ]},
    "L": {"box": L, "strokes": [
        "sweep-short 250 950 l=200 a=-145",
        "turn-spur 100 810 l1=240 l2=720 spur=80",
        "sweep 90 560 l=230 a=-125 curl=0.1",
        "rise 230 330 l=150 a=34",
    ]},
    "B": {"box": B, "strokes": [
        "sweep-short 470 440 l=200 a=-145",
        "turn-spur 280 350 l1=460 l2=280 spur=90",
        "sweep 220 230 l=230 a=-125 curl=0.1",
        "rise 600 110 l=200 a=26",
    ]},
})

define("foot", "foot, standing, stepping", "meaning", "dai", positions="L B", lookalike="足, 止", forms={
    "S": {"strokes": [
        "sweep 620 900 l=230 a=-125 curl=0.1",
        "bend-spur 300 860 l1=540 l2=520 r=120 spur=80",
        "horizontal 380 596 l=260 rise=6",
        "needle 620 760 l=620",
    ]},
    "L": {"box": L, "strokes": [
        "sweep 300 900 l=230 a=-125 curl=0.1",
        "bend-spur 100 880 l1=640 l2=240 r=80 spur=70",
        "horizontal 150 542 l=200 rise=6",
    ]},
    "B": {"box": B, "strokes": [
        "sweep 620 430 l=230 a=-125 curl=0.1",
        "bend-spur 200 420 l1=260 l2=600 r=80 spur=80",
        "horizontal 380 276 l=260 rise=6",
    ]},
})

define("heart", "heart, feeling, thought", "meaning", "tsen", positions="L B", lookalike="心, 忄", forms={
    "S": {"strokes": [
        "sweep-short 340 880 l=200 a=-145",
        "fall 600 900 l=240 a=-50 foot=0.2",
        "bend-spur 250 700 l1=320 l2=540 r=110 spur=90",
        "scale 420 560 l=200 a=-8 sag=0.4",
    ]},
    "L": {"box": L, "strokes": [
        "sweep-short 145 920 l=200 a=-145",
        "sweep 120 720 l=230 a=-112 curl=0.1",
        "needle 290 940 l=860",
        "sweep-short 410 720 l=180 a=-160",
    ]},
    "B": {"box": B, "strokes": [
        "sweep-short 320 430 l=190 a=-145",
        "fall 560 430 l=240 a=-40 foot=0.2",
        "bend-spur 220 330 l1=180 l2=560 r=70 spur=80",
        "scale 430 200 l=200 a=-8 sag=0.4",
    ]},
})

define("eye", "eye, seeing", "meaning", "ching", positions="L T", lookalike="目, 罒", forms={
    "S": {"strokes": [
        "sweep-short 534 860 l=200 a=-145",
        "vertical 160 680 l=300",
        "turn-spur 160 690 l1=680 l2=330 spur=90",
        "fall 470 600 l=240 a=-55 foot=0.22",
        "horizontal 180 400 l=640",
    ]},
    "L": {"box": L, "strokes": [
        "sweep-short 236 940 l=200 a=-145",
        "vertical 70 800 l=560",
        "turn-spur 70 810 l1=280 l2=580 spur=70",
        "fall 170 600 l=240 a=-55 foot=0.22",
        "horizontal 90 270 l=260",
    ]},
    "T": {"box": T, "strokes": [
        "sweep-short 530 440 l=200 a=-145",
        "vertical 180 330 l=220",
        "turn-spur 180 340 l1=640 l2=240 spur=80",
        "fall 470 280 l=240 a=-55 foot=0.22",
        "horizontal 200 120 l=600",
    ]},
})

define("mouth", "mouth, speaking, eating", "meaning", "tsong", positions="L B", lookalike="口", forms={
    "S": {"strokes": [
        "vertical 260 740 l=460",
        "turn-spur 260 750 l1=480 l2=470 spur=100",
        "sweep 470 470 l=230 a=-125 curl=0.1",
    ]},
    "L": {"box": L, "strokes": [
        "vertical 60 740 l=460",
        "turn-spur 60 750 l1=280 l2=470 spur=70",
        "sweep 190 470 l=230 a=-125 curl=0.1",
    ]},
    "B": {"box": B, "strokes": [
        "vertical 280 390 l=280",
        "turn-spur 280 400 l1=440 l2=290 spur=90",
        "sweep 480 250 l=230 a=-125 curl=0.1",
    ]},
})

define("ear", "ear, hearing", "meaning", None, positions="L R", lookalike="耳", forms={
    "S": {"strokes": [
        "turn-spur 220 860 l1=440 l2=640 spur=90",
        "scale 300 680 l=200 a=-40 sag=0.4",
        "horizontal 230 400 l=221 rise=6",
    ]},
    "L": {"box": L, "strokes": [
        "turn-spur 70 880 l1=260 l2=700 spur=70",
        "scale 100 720 l=150 a=-40 sag=0.4",
        "horizontal 60 383 l=200 rise=6",
    ]},
    "R": {"box": R, "strokes": [
        "turn-spur 80 880 l1=290 l2=720 spur=80",
        "scale 110 720 l=160 a=-40 sag=0.4",
        "horizontal 70 382 l=200 rise=6",
    ]},
})

define("nose", "nose, smelling, breath", "meaning", None, positions="L T", lookalike="自, 鼻", forms={
    "S": {"strokes": [
        "fall 460 920 l=240 a=-55 foot=0.22",
        "needle 500 830 l=480 lean=-12",
        "sweep-turn 470 380 l1=180 l2=380 rise=20",
        "sweep 330 440 l=230 a=-125 curl=0.1",
    ]},
    "L": {"box": L, "strokes": [
        "fall 180 940 l=240 a=-55 foot=0.22",
        "needle 220 860 l=520 lean=-12",
        "sweep-turn 200 340 l1=150 l2=220 rise=22",
        "sweep 110 420 l=230 a=-125 curl=0.1",
    ]},
    "T": {"box": T, "strokes": [
        "fall 460 440 l=240 a=-55 foot=0.22",
        "needle 500 400 l=300 lean=-12",
        "sweep-turn 480 120 l1=120 l2=300 rise=16",
        "sweep 340 170 l=230 a=-125 curl=0.1",
    ]},
})

define("tooth", "tooth, biting", "meaning", None, positions="B L", lookalike="牙, 齒", forms={
    "B": {"box": B, "strokes": [
        "horizontal 120 400 l=760",
        "sweep-short 330 370 l=140 a=-140",
        "sweep-short 560 370 l=140 a=-140",
        "fall 690 360 l=240 a=-55 foot=0.22",
        "fall-flat 150 100 l=700",
    ]},
    "L": {"box": L, "strokes": [
        "horizontal 50 860 l=330",
        "sweep-short 160 820 l=110 a=-140",
        "fall 260 820 l=240 a=-58 foot=0.22",
        "sweep-short 160 640 l=110 a=-140",
        "fall 260 640 l=240 a=-58 foot=0.22",
        "fall-flat 50 300 l=340 a=-6",
    ]},
})

define("head", "head, face", "meaning", None, positions="R", lookalike="頁", forms={
    "R": {"box": R, "strokes": [
        "sweep 240 960 l=230 a=-125 curl=0.1",
        "turn-spur 60 860 l1=330 l2=540 spur=80",
        "horizontal 70 658 l=234 rise=6",
        "sweep-turn 180 450 l1=130 l2=200 rise=20",
        "fall-flat 40 160 l=380 a=-6",
    ]},
})

define("hair", "hair, pattern of lines", "meaning", None, positions="R T", lookalike="彡", forms={
    "R": {"box": R, "strokes": [
        "needle 110 930 l=840 lean=-12",
        "fall 150 840 l=260 a=-40",
        "fall 150 600 l=260 a=-40",
        "fall 150 360 l=260 a=-40",
    ]},
    "T": {"box": T, "strokes": [
        "horizontal 100 400 l=800",
        "fall 150 330 l=240 a=-38",
        "fall 400 330 l=240 a=-38",
        "fall 650 330 l=240 a=-38",
    ]},
})

define("flesh", "flesh, part of the body", "meaning", None, positions="L", lookalike="⺼ (月)", forms={
    "L": {"box": L, "strokes": [
        "fall 300 940 l=240 a=-55 foot=0.22",
        "vertical 120 880 l=780 lean=-10",
        "horizontal 160 741 l=208 rise=6",
        "horizontal 160 501 l=208 rise=6",
        "rise 160 290 l=200 a=34",
    ]},
})

define("bone", "bone, frame", "meaning", None, positions="L", lookalike="骨", forms={
    "L": {"box": L, "strokes": [
        "tally 250 960 l=150",
        "vertical-spur 230 830 l=640 spur=70 lean=-14",
        "sweep 340 600 l=230 a=-125 curl=0.1",
        "horizontal 40 306 l=260 rise=6",
    ]},
})

define("skin", "skin, hide, surface", "meaning", None, positions="R", lookalike="皮", forms={
    "R": {"box": R, "strokes": [
        "horizontal 60 860 l=340",
        "sweep 160 920 l=760 a=-100 curl=0.3",
        "horizontal 190 616 l=260 rise=6",
        "fall-flat 170 340 l=300 a=-10",
    ]},
})

define("spirit", "spirit, breath of life", "meaning", None, positions="T", lookalike="none close", forms={
    "T": {"box": T, "strokes": [
        "sweep-turn 300 430 l1=140 l2=240 rise=24",
        "sweep-turn 620 430 l1=140 l2=240 rise=24",
        "horizontal 380 144 l=286 rise=6",
    ]},
})

define("sacred", "altar, the sacred", "meaning", None, positions="L", lookalike="礻, 示", forms={
    "L": {"box": L, "strokes": [
        "sweep-short 230 960 l=200 a=-145",
        "horizontal 50 780 l=330",
        "vertical-spur 210 780 l=700 spur=70",
        "scale 40 560 l=140 a=-30",
        "rise 250 420 l=120 a=40",
    ]},
})

define("death", "death, ruin", "meaning", None, positions="L", lookalike="歹", forms={
    "L": {"box": L, "strokes": [
        "horizontal 50 860 l=330",
        "needle 120 860 l=640 lean=-20",
        "scale 170 620 l=170 a=-35 sag=0.36",
        "sweep 340 420 l=230 a=-125 curl=0.1",
        "rise 160 220 l=200 a=30",
    ]},
})

define("beast", "beast, four-footed animal", "meaning", None, positions="L", lookalike="犭, 豸", forms={
    "L": {"box": L, "strokes": [
        "sweep 300 950 l=230 a=-125 curl=0.1",
        "sweep 340 880 l=440 a=-128 curl=0.3",
        "slant-spur 120 700 l=480 a=-66 spur=60",
        "sweep-short 340 460 l=180 a=-150",
        "fall 50 330 l=240 a=-55 foot=0.22",
    ]},
})

define("bird", "bird, winged thing", "meaning", "zhai", positions="R B", lookalike="鳥, 隹", forms={
    "S": {"strokes": [
        "sweep 380 940 l=230 a=-125 curl=0.1",
        "sweep 600 870 l=620 a=-145 curl=0.4",
        "fall-flat 220 570 l=620 a=-10",
        "vertical-spur 500 500 l=320 spur=80",
        "horizontal 600 228 l=234 rise=6",
    ]},
    "R": {"box": R, "strokes": [
        "sweep 160 950 l=230 a=-125 curl=0.1",
        "sweep 340 880 l=380 a=-140 curl=0.4",
        "fall-flat 60 600 l=360 a=-10",
        "vertical-spur 220 520 l=360 spur=70",
        "horizontal 260 241 l=208 rise=6",
    ]},
    "B": {"box": B, "strokes": [
        "sweep 380 440 l=230 a=-125 curl=0.1",
        "sweep 600 410 l=300 a=-150 curl=0.4",
        "fall-flat 220 260 l=620 a=-8",
        "horizontal 600 128 l=234 rise=6",
    ]},
})

define("dragon", "dragon, scaled power", "meaning", "zho", positions="R L", lookalike="龍", novel="scale", forms={
    "S": {"strokes": [
        "sweep 700 930 l=230 a=-125 curl=0.1",
        "horizontal 160 830 l=680",
        "slant-spur 300 810 l=760 a=-60 bow=0.12 spur=100",
        "scale 140 640 l=180 a=-25",
        "scale 280 460 l=180 a=-25",
        "scale 600 700 l=170 a=-20",
    ]},
    "R": {"box": R, "strokes": [
        "sweep 340 950 l=230 a=-125 curl=0.1",
        "horizontal 50 860 l=360",
        "slant-spur 120 840 l=780 a=-70 bow=0.1 spur=80",
        "scale 40 640 l=140 a=-25",
        "scale 150 440 l=140 a=-25",
        "scale 300 680 l=120 a=-20",
    ]},
    "L": {"box": L, "strokes": [
        "sweep 330 950 l=230 a=-125 curl=0.1",
        "horizontal 50 860 l=330",
        "slant-spur 100 840 l=760 a=-70 bow=0.1 spur=70",
        "scale 30 640 l=130 a=-25",
        "scale 140 440 l=130 a=-25",
        "scale 280 680 l=110 a=-20",
    ]},
})

define("horse", "horse, riding", "meaning", "mai", positions="L", lookalike="馬", forms={
    "S": {"strokes": [
        "sweep 640 920 l=230 a=-125 curl=0.1",
        "turn-sweep 260 840 l1=420 l2=500 a=-118",
        "vertical-spur 560 560 l=420 spur=80",
        "horizontal 200 276 l=260 rise=6",
        "horizontal 600 236 l=260 rise=6",
    ]},
    "L": {"box": L, "strokes": [
        "sweep 330 940 l=230 a=-125 curl=0.1",
        "turn-sweep 70 850 l1=260 l2=420 a=-118",
        "vertical-spur 240 560 l=460 spur=60",
        "horizontal 50 300 l=221 rise=6",
    ]},
})

define("crawler", "crawling thing: serpent, insect", "meaning", None, positions="L", lookalike="虫", novel="scale", forms={
    "L": {"box": L, "strokes": [
        "sweep 330 950 l=820 a=-104 curl=0.8",
        "scale 20 860 l=190 a=-35 sag=0.38",
        "scale 230 680 l=180 a=-40 sag=0.38",
        "scale 20 500 l=180 a=-35 sag=0.38",
    ]},
})

# -- the house, the office and the altar ----------------------------------------------------

define("roof", "roof, house", "meaning", "zhuen", positions="T", lookalike="宀, 冖", forms={
    "S": {"strokes": [
        "sweep-short 544 920 l=200 a=-145",
        "sweep-turn 230 780 l1=120 l2=160 rise=30",
        "horizontal 240 760 l=560 rise=2",
        "rise 790 720 l=150 a=40",
        "needle 500 700 l=440",
        "fall-flat 160 220 l=700",
    ]},
    "T": {"box": T, "strokes": [
        "sweep-short 544 440 l=200 a=-145",
        "sweep-turn 230 300 l1=120 l2=160 rise=30",
        "horizontal 240 280 l=560 rise=2",
        "rise 790 240 l=150 a=40",
    ]},
})

define("shelter", "lean-to, office, sheltered place", "meaning", None, positions="⿸", lookalike="广, 厂", forms={
    "⿸": {"inner": (320, 100, 920, 760), "strokes": [
        "horizontal 90 860 l=820",
        "sweep-short 700 960 l=200 a=-145",
        "needle 230 930 l=840 lean=-20",
    ]},
})

define("sickness", "sickness, healing", "meaning", None, positions="⿸", lookalike="疒", forms={
    "⿸": {"inner": (340, 100, 920, 760), "strokes": [
        "horizontal 110 860 l=820",
        "vertical-spur 260 930 l=830 spur=90",
        "horizontal 50 680 l=221 rise=6",
        "fall 600 960 l=240 a=-55 foot=0.22",
    ]},
})

define("enclosure", "enclosure, bounds", "meaning", None, positions="⿴", lookalike="囗", forms={
    "⿴": {"inner": (230, 230, 760, 760), "strokes": [
        "sweep 170 880 l=760 a=-100 curl=0.1",
        "turn-spur 150 880 l1=700 l2=760 spur=110",
        "fall-flat 60 140 l=880 a=-5",
    ]},
})

define("door", "door, gate, opening", "meaning", "sen", positions="⿵", lookalike="門, 冂", forms={
    "S": {"strokes": [
        "horizontal 90 880 l=820",
        "horizontal 390 774 l=286 rise=6",
        "needle 210 870 l=780",
        "vertical-spur 790 870 l=780 spur=90",
    ]},
    "⿵": {"inner": (300, 100, 720, 700), "strokes": [
        "horizontal 90 880 l=820",
        "horizontal 390 774 l=286 rise=6",
        "needle 210 870 l=780",
        "vertical-spur 790 870 l=780 spur=90",
    ]},
})

define("motion", "motion along a road", "meaning", None, positions="⿺", lookalike="辶, 廴", forms={
    "⿺": {"inner": (360, 280, 960, 960), "strokes": [
        "sweep-short 190 950 l=200 a=-145",
        "needle 170 820 l=480 lean=-12",
        "fall 240 480 l=240 a=-55 foot=0.22",
        "fall-flat 200 210 l=760 a=-5",
    ]},
})

define("step", "step, going, conduct", "meaning", None, positions="L", lookalike="彳", forms={
    "L": {"box": L, "strokes": [
        "tally 40 950 l=200",
        "horizontal 170 716 l=260 rise=6",
        "horizontal 40 506 l=260 rise=6",
        "rise 60 260 l=300 a=30",
    ]},
})

define("speech", "speech, words", "meaning", None, positions="L", lookalike="言, 讠", forms={
    "L": {"box": L, "strokes": [
        "fall 60 950 l=260 a=-35",
        "fall 60 780 l=260 a=-35",
        "vertical 70 560 l=380",
        "turn-spur 70 570 l1=280 l2=400 spur=60",
        "sweep 190 380 l=230 a=-125 curl=0.1",
    ]},
})

define("blade", "blade, cutting", "meaning", "ja", positions="R", lookalike="刀, 刂", forms={
    "S": {"strokes": [
        "sweep-short 700 960 l=200 a=-145",
        "sweep 640 880 l=820 a=-112 curl=0.6",
        "horizontal 360 700 l=440 rise=6",
    ]},
    "R": {"box": R, "strokes": [
        "sweep-short 326 960 l=200 a=-145",
        "sweep 360 880 l=820 a=-102 curl=0.6",
        "horizontal 130 700 l=300 rise=6",
    ]},
})

define("thread", "thread, silk, binding", "meaning", None, positions="L", lookalike="糸", forms={
    "L": {"box": L, "strokes": [
        "needle 210 960 l=860",
        "tally 70 860 l=200",
        "horizontal 70 616 l=260 rise=6",
        "horizontal 70 396 l=260 rise=6",
    ]},
})

define("vessel", "vessel, dish, container", "meaning", None, positions="B", lookalike="皿", forms={
    "B": {"box": B, "strokes": [
        "horizontal 120 410 l=760",
        "sweep 220 350 l=230 a=-125 curl=0.1",
        "scale 390 300 l=220 a=-5 sag=0.42",
        "fall 760 340 l=240 a=-50 foot=0.22",
        "fall-flat 260 90 l=480",
    ]},
})

define("food", "food, eating", "meaning", None, positions="L", lookalike="飠, 食", forms={
    "L": {"box": L, "strokes": [
        "sweep-short 300 950 l=180 a=-150",
        "turn-spur 60 820 l1=270 l2=460 spur=70",
        "horizontal 70 660 l=221 rise=6",
        "rise 40 260 l=320 a=30",
    ]},
})

define("wealth", "cowrie, wealth, value", "meaning", None, positions="L B", lookalike="貝", forms={
    "S": {"strokes": [
        "sweep-short 544 940 l=200 a=-145",
        "needle 300 800 l=560",
        "vertical-spur 700 800 l=600 spur=90",
        "scale 390 660 l=220 a=-5 sag=0.4",
        "scale 390 460 l=220 a=-5 sag=0.4",
        "rise 160 180 l=320 a=20",
    ]},
    "L": {"box": L, "strokes": [
        "sweep-short 240 950 l=200 a=-145",
        "needle 70 820 l=560",
        "vertical-spur 330 820 l=600 spur=60",
        "scale 110 680 l=180 a=-5 sag=0.4",
        "scale 110 480 l=180 a=-5 sag=0.4",
        "rise 40 160 l=300 a=24",
    ]},
    "B": {"box": B, "strokes": [
        "sweep-short 544 440 l=200 a=-145",
        "needle 300 360 l=300",
        "vertical-spur 700 360 l=300 spur=80",
        "scale 390 280 l=220 a=-5 sag=0.4",
        "rise 160 60 l=320 a=18",
    ]},
})

define("brush", "brush, writing, office", "meaning", None, positions="T", lookalike="聿, ⺮", forms={
    "T": {"box": T, "strokes": [
        "sweep-short 400 440 l=140 a=-150",
        "needle 520 440 l=360",
        "horizontal 140 300 l=720",
        "horizontal 600 126 l=260 rise=6",
    ]},
})

define("strike", "striking hand, action done", "meaning", None, positions="R", lookalike="攵, 殳", forms={
    "R": {"box": R, "strokes": [
        "fall 160 950 l=240 a=-55 foot=0.22",
        "turn-sweep 60 830 l1=300 l2=360 a=-118",
        "slant-spur 170 600 l=500 a=-60 spur=70",
        "rise 40 340 l=260 a=34",
    ]},
})

define("strength", "strength, effort", "meaning", None, positions="R B", lookalike="力", forms={
    "R": {"box": R, "strokes": [
        "sweep 330 930 l=820 a=-112 curl=0.3",
        "bend-spur 110 720 l1=380 l2=260 r=70 spur=70",
        "fall 330 640 l=240 a=-55 foot=0.22",
    ]},
    "B": {"box": B, "strokes": [
        "sweep 560 430 l=380 a=-140 curl=0.3",
        "bend-spur 260 400 l1=240 l2=480 r=70 spur=70",
        "fall 640 330 l=240 a=-55 foot=0.22",
    ]},
})

define("cover", "cover, hiding", "meaning", None, positions="T", lookalike="冖", forms={
    "T": {"box": T, "strokes": [
        "sweep-short 544 430 l=200 a=-145",
        "fall-flat 100 250 l=800 a=-4",
    ]},
})

define("one", "one, a single line", "structural", "tsi", positions="T B", lookalike="一", novel="barb-dot", forms={
    "S": {"strokes": [
        "barb-dot 180 660 l=90",
        "horizontal 120 500 l=760",
    ]},
    "T": {"box": T, "strokes": [
        "barb-dot 180 400 l=80",
        "horizontal 120 220 l=760",
    ]},
    "B": {"box": B, "strokes": [
        "barb-dot 180 360 l=80",
        "horizontal 120 180 l=760",
    ]},
})

define("count", "counting-rod, number", "meaning", None, positions="L", lookalike="none close", novel="rods", forms={
    "L": {"box": L, "strokes": [
        "rods 30 920 l=280",
        "rods 100 690 l=280",
        "vertical-spur 210 520 l=440 spur=70",
    ]},
})

define("old", "age, the elders", "meaning", None, positions="T", lookalike="耂", forms={
    "T": {"box": T, "strokes": [
        "sweep 300 440 l=230 a=-125 curl=0.1",
        "bend-spur 300 380 l1=260 l2=440 r=80 spur=70",
        "sweep 760 440 l=440 a=-128",
    ]},
})

define("small", "small, a little", "meaning", None, positions="T", lookalike="小, ⺌", forms={
    "T": {"box": T, "strokes": [
        "sweep 380 400 l=230 a=-125 curl=0.1",
        "vertical-spur 500 430 l=360 spur=90",
        "sweep-short 685 380 l=200 a=-145",
    ]},
})

define("light", "rays, light", "meaning", None, positions="T", lookalike="⺌, 光", forms={
    "T": {"box": T, "strokes": [
        "sweep 320 400 l=230 a=-125 curl=0.1",
        "fall 500 430 l=240 a=-58 foot=0.22",
        "fall 700 400 l=240 a=-40 foot=0.22",
        "fall-flat 140 160 l=720",
    ]},
})

define("mark", "a dot or stroke marking a place", "structural", None, positions="T B", lookalike="丶", novel="barb-dot", forms={
    "T": {"box": T, "strokes": ["barb-dot 450 360 l=110"]},
    "B": {"box": B, "strokes": ["barb-dot 450 330 l=110"]},
})


# -- sound components that are whole characters ----------------------------------------------
#
# The pictographs above are sound components as they stand. These are the meaning
# compounds, composed from the components above; their layout is the proposal's.

M = 60  # margin of the em


def compound(cid, gloss, idc, parts=(), strokes=(), lookalike=""):
    form = {"parts": list(parts)}
    if strokes:
        form["strokes"] = list(strokes)
    define(cid, gloss, "sound", cid, {"S": form}, lookalike=lookalike, sound=cid, idc=idc,
           positions="R B")


compound("zhen", "snow", "⿱{rain}{ice}", [("rain", "T", (M, 520, 1000 - M, 960)), ("ice", "B", (M, 60, 1000 - M, 500))])
compound("rao", "thunder", "⿱{rain}{field}", [("rain", "T", (M, 560, 1000 - M, 960)), ("field", "B", (M, 60, 1000 - M, 540))])
compound("tan", "celestial", "⿱{sky}{sun}", [("sky", "T", (M, 520, 1000 - M, 960)), ("sun", "B", (120, 60, 880, 500))])
compound("rin", "red", "⿱{sun}{fire}", [("sun", "T", (120, 470, 880, 960)), ("fire", "B", (M, 60, 1000 - M, 440))])
compound("ha", "dark", "⿱{cover}{sun}", [("cover", "T", (M, 620, 1000 - M, 960)), ("sun", "B", (100, 60, 900, 600))])
compound("leng", "bright", "⿰{sun}{moon}", [("sun", "L", (M, 120, 440, 900)), ("moon", "R", (480, 60, 1000 - M, 960))])
compound("wai", "ten", "⿻{one}{one}", strokes=[
    "barb-dot 200 760 l=90",
    "horizontal 120 560 l=760",
    "vertical-spur 500 900 l=780 spur=100",
    "barb-dot 640 420 l=90",
], lookalike="十")
compound("rong", "ten thousand", "⿳{person}{person}{person}", [
    ("person", "T", (M + 40, 690, 1000 - M - 40, 970)),
    ("person", "T", (M + 40, 380, 1000 - M - 40, 660)),
    ("person", "T", (M + 40, 70, 1000 - M - 40, 350))])
compound("wen", "centre", "⿴{enclosure}{one}", [("enclosure", "⿴", (M, M, 1000 - M, 1000 - M)), ("one", "S", (260, 260, 760, 760))])
compound("dou", "path", "⿺{motion}{foot}", [("motion", "⿺", (M, M, 1000 - M, 1000 - M)), ("foot", "S", (370, 300, 950, 950))])
compound("hou", "balance", "⿰{person}{person}", [("person", "L", (M, 60, 420, 960)), ("person", "S", (440, 60, 1000 - M, 960))])
compound("sing", "death", "⿰{death}{person}", [("death", "L", (M, 60, 420, 960)), ("person", "S", (440, 60, 1000 - M, 960))])
compound("zha", "life", "⿱{plant}{earth}", [("plant", "T", (M, 560, 1000 - M, 960)), ("earth", "B", (M, 60, 1000 - M, 520))])
compound("chiao", "to freeze", "⿰{ice}{water}", [("ice", "L", (M, 60, 330, 960)), ("water", "S", (360, 60, 1000 - M, 960))])
compound("dao", "great", "⿱{one}{person}", [("one", "T", (M, 640, 1000 - M, 960)), ("person", "S", (120, 40, 880, 640))])
compound("shui", "new, small", "⿱{small}{mark}", [("small", "T", (M, 400, 1000 - M, 960)), ("mark", "B", (M, 60, 1000 - M, 420))])
compound("hin", "love", "⿰{heart}{hand}", [("heart", "L", (M, 60, 400, 960)), ("hand", "S", (440, 60, 1000 - M, 960))])
compound("mei", "dream", "⿱{moon}{eye}", [("moon", "S", (160, 470, 840, 960)), ("eye", "T", (M, 60, 1000 - M, 460))])
compound("nie", "year", "⿱{grain}{person}", [("grain", "T", (M, 540, 1000 - M, 960)), ("person", "S", (140, 40, 860, 540))])
compound("len", "two", "⿱{one}{one}", [("one", "T", (M, 520, 1000 - M, 900)), ("one", "B", (M, 100, 1000 - M, 480))])
compound("tao", "three", "⿳{one}{one}{one}", [
    ("one", "T", (M, 680, 1000 - M, 960)), ("one", "T", (M, 390, 1000 - M, 670)), ("one", "B", (M, 60, 1000 - M, 380))])
compound("mong", "none, not", "⿱{cover}{person}", [("cover", "T", (M, 620, 1000 - M, 960)), ("person", "S", (140, 40, 860, 620))])

# the pictographs are sound components too: each gives its own reading
for _c in list(COMPONENTS.values()):
    if _c.char and _c.role != "sound":
        _c.sound = _c.char
