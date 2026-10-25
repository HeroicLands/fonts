# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Composed blocks of the Ch'alish P'ilam ceremonial hand: compact forms, syllable signs,
and the layout of a block from the codage.

    import blocks as Q

    parts = Q.compose("n3*la1:JAGUAR")       # [(pen, parts), ...] filling one block

A block holds a main sign and at most two affixes. In the codage, ``*`` sets what is
before it ahead of what follows (a prefix or a coefficient before the main sign) and
``:`` stacks what is before it over what follows (a superfix over the main sign, or the
main sign over a subfix). A main
sign that shares its block takes its **compact form**, drawn with less interior detail so
it can be carved at the smaller size. Syllable signs are simple shapes, drawn **flat**
for above or below a sign and **tall** for before or after it.

This module is the geometry the font's block layout follows, worked out where it can be
drawn and checked.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable

import ceremonial as R
import strokes as S
import syllabary as Y
from ceremonial import CONTOUR, DETAIL, B, C

# How much of the block an affix takes: a flat affix's height, a tall affix's width.
AFFIX = 0.34
# The white a subfix keeps above the block's foot, so its line stays inside the font's
# descent.
FLOOR = 14.0
# How far a main sign may be squeezed out of its own proportions to fill its slot, as Maya
# scribes squeezed a sign to share its block rather than shrinking it evenly.
SQUEEZE = 1.6
GAP = R.GAP + R.CONTOUR.full


# -- syllable signs: the syllabary, drawn in syllabary.py -------------------------------------------

SIGNS = Y.SIGNS


# -- compact forms -------------------------------------------------------------------------------


def _jaguar_compact():
    # the jaguar's head reduced for a shared block: its outline, a single open eye and two
    # spots; everything that crowds once the head is squeezed is left out
    contour, _ = R.head(R.CX0, R.CY0, R.CX1, R.CY1 - 60, eye_kind="spiral", spool=False, band=False)
    eye = S.dot(R.CX0 + 0.3 * R.CW, R.CY0 + 0.56 * (R.CH - 60), 40)
    spots = S.ring(R.CX0 + 0.6 * R.CW, R.CY0 + 0.6 * (R.CH - 60), 56) + \
        S.ring(R.CX0 + 0.7 * R.CW, R.CY0 + 0.36 * (R.CH - 60), 56)
    return [(CONTOUR, contour), (DETAIL, eye + spots)]


def code(glyph) -> str:
    """A glyph's codage: its name in capitals, a hyphen written as an underscore, since
    ``-`` ends a block, and an apostrophe left out."""
    return glyph.name.upper().replace("-", "_").replace("'", "")


def _concepts():
    import compounds as X
    import core as Z
    import cosmos as K
    import events as E
    import gods as G
    import kin as N
    import places as PL
    import ranks as T
    import senses as V
    import turnings as W
    return [g for g in R.PILOT + Z.CORE + G.GODS + T.RANKS + E.EVENTS + K.COSMOS + PL.PLACES + X.COMPOUNDS
            + W.TURNINGS + N.KIN + V.SENSES if not g.name[1:].isdigit()]


# Every concept glyph drawn so far, by its code. A glyph with no compact form of its own
# uses its full form when it shares a block.
MAINS = {code(g): g for g in _concepts()}
# A part of the detail smaller than this, across its larger side, is left out of a compact
# form: dots, beads, small rings and fine curls are what crowd once a sign is squeezed.
SMALL = 0.2 * B


def _extent(part):
    xs = [x for x, _ in part.pts]
    ys = [y for _, y in part.pts]
    return max(max(xs) - min(xs), max(ys) - min(ys))


def compact_of(glyph, keep=1):
    """A glyph's compact form by rule: its outline, and at most its ``keep`` largest other
    forms; everything small enough to crowd once the sign is squeezed is left out."""
    def draw():
        parts = [(pen, p) for pen, ps in glyph.draw() for p in ps]
        outline, rest = parts[0], parts[1:]
        big = sorted((x for x in rest if _extent(x[1]) >= SMALL), key=lambda x: -_extent(x[1]))[:keep]
        out = {}
        for pen, p in [outline] + big:
            out.setdefault(pen, []).append(p)
        return list(out.items())
    return draw


# Each main sign's compact form: its outline and one solid token (compact.py). Head glyphs
# keep their profile and a solid eye, with their token in the head.
_HEADS = {
    "LORD": "three_dots", "JAGUAR": "paw", "SERPENT": "wave", "MAN": None, "WOMAN": "drop",
    "DEATH_JAGUAR": "skull", "STORM_SERPENT": "bolt",
    "OVERLORD": "star", "KING": "disk", "PRINCE": "half_up", "NOBLE_LORD": "flower", "SEATED_LORD": "square",
    "LADY": "crescent", "LANDHOLDER": "roof", "KNIGHT": "cross", "WAR_LEADER": "triangle", "SUN_PRIEST": "diamond",
    "PRIEST": "peak", "SCRIBE": "eye", "HERALD": "x_cross", "MASTER_MERCHANT": "bundle", "GUILDSMAN": "hand",
    "FREEMAN": "bird", "SERF": "stair", "SLAVE": "half_down", "PEOPLE": "two_bars", "WOMEN": "two_drops",
}
# A head token's size, as a fraction of the head's shorter side: the largest that stays
# carvable in every layout, at most 0.24 so the tokens read as one set.
_HEAD_SIZES = {
    "LORD": 0.24, "JAGUAR": 0.24, "SERPENT": 0.24, "WOMAN": 0.2, "DEATH_JAGUAR": 0.24, "STORM_SERPENT": 0.24,
    "OVERLORD": 0.22, "KING": 0.24, "PRINCE": 0.24, "NOBLE_LORD": 0.2, "SEATED_LORD": 0.18, "LADY": 0.24,
    "LANDHOLDER": 0.2, "KNIGHT": 0.14, "WAR_LEADER": 0.24, "SUN_PRIEST": 0.2, "PRIEST": 0.24, "SCRIBE": 0.22,
    "HERALD": 0.14, "MASTER_MERCHANT": 0.24, "GUILDSMAN": 0.16, "FREEMAN": 0.24, "SERF": 0.22, "SLAVE": 0.16,
    "PEOPLE": 0.14, "WOMEN": 0.14,
}
# The rest take the syllabary's line motif of their concept; signs that share an outline
# take different motifs, so no two compact forms of one outline are alike.
_MOTIFS = {
    "SUN": "sun", "MOON": "crescent", "WATER": "river", "PEAK": "peaks", "TQAN": "ring_dot", "PATRIARCH": "lord",
    "SKY": "vault", "STAR": "star4", "FIRE": "flaming_coal", "EARTH": "furrows", "STONE": "cracked_stone",
    "PLANT": "sprout_seed", "BEAST": "legs", "EAST": "horizon_sun", "WEST": "dome_night", "NORTH": "supreme",
    "SOUTH": "bowl", "HIGH": "above", "LOW": "low", "INSIDE": "room", "OUTSIDE": "open_room", "HOUSE": "roof_dot",
    "HAND": "palm", "EYE": "almond_eye", "MOUTH": "mouth",
    "SUN_AT_THE_EDGE": "day", "SACRED_STAR": "key", "GOLDEN_GIVER": "seed", "SACRED_FLAME": "drop",
    "PEAK_BUILDER": "mesa", "PATH_WALKER": "footprint", "MOON_DREAMER": "hanging_cords",
    "LIVING_BLOSSOM": "three_plumes", "FALLEN_OWL": "bat",
    "BIRTH": "womb", "SEATING": "mat", "DEATH": "black_mirror", "BURIAL": "burial", "MARRIAGE": "pierced_beads",
    "CAPTURE": "capture", "WAR": "crossed", "CONQUEST": "conquest", "TRIBUTE": "tied", "FOUNDATION": "table",
    "DEDICATION": "doorway", "OFFERING": "cup", "ECLIPSE": "obsidian_mirror", "PILGRIMAGE": "print_on_road",
    "ERAS_END": "eras_end", "BALL_GAME": "spiral_ball",
    "UNDERWORLD": "shell", "HEAVEN": "sky", "FIFTH_AGE": "quincunx", "LIVING_FLAME": "incense",
    "SOLAR_COUNT": "sun", "LUNAR_COUNT": "crescent", "STELLAR_COUNT": "star4",
    "ISHILANKUL": "star4", "KANKUL": "ring_dot", "NEOK_BAATE": "river", "SHELEM": "bird", "ISHBAL_TSAKU": "spots",
    "KUSHI_ISHBAL": "two_prints", "QAPTEL_TSAKUL": "corner_dot", "SHELEM_ISHBAL": "heap",
    "MATRIARCH": "womb", "SON": "you", "DAUGHTER": "rattle", "FAMILY": "pierced_beads",
    "BIRTH_OF_A_BOY": "self_", "BIRTH_OF_A_GIRL": "pot", "DEATH_OF_A_MAN": "blade", "DEATH_OF_A_WOMAN": "carapace",
    "HOUSEHOLD_FOUNDED": "horizon_sun", "HOUSEHOLD_ENDED": "dome_night",
    "DAWN": "light", "SUNSET": "drops3", "NOON": "sun", "MIDNIGHT": "mask", "GERMINATION": "tree",
    "HARVEST": "tufts", "LIFETIME": "plume", "REBIRTH": "soul",
    "PASSAGE_OF_THE_DEAD": "chevron",
    "KINSMAN": "heart", "STRANGER": "shield", "HOME": "ember", "VILLAGE": "posted_house", "BOY": "hummingbird",
    "GIRL": "needle", "ELDER": "throne", "ELDER_WOMAN": "tripod", "GOD": "three_dots_ring", "EXALTED_ANCESTOR": "eagle",
    "SOUL_AMONG_THE_DEAD": "worm",
    "MEMORY": "door", "OBSERVATION": "hand_mirror", "SECRET": "bundle_x", "PROCLAMATION": "scroll", "THE_UNKNOWN": "nested_diamond",
    "WRITING": "quill", "PRAYER": "drum", "CENOTE": "jar", "CAUTION": "ears",
}


# A motif's scale where the default does not leave it carvable in every layout.
_SCALES = {
    "TQAN": 0.9, "WEST": 0.8, "INSIDE": 0.75, "LIVING_BLOSSOM": 1.05,
    "KUSHI_ISHBAL": 0.7, "HOUSEHOLD_ENDED": 0.8, "VILLAGE": 1.05, "THE_UNKNOWN": 0.65, "CENOTE": 1.05,
    "CAUTION": 1.05,
}
# Signs whose motif cannot be carved at any scale in some layout take a solid token instead,
_TOKENS = {
    "SUN": "disk", "WATER": "wave", "BALL_GAME": "bar", "DAUGHTER": "drop", "NEOK_BAATE": "diamond",
    # and signs whose motif is too near another's in the same outline
    "DEATH": "skull", "DEATH_OF_A_WOMAN": "half_down", "SACRED_FLAME": "flame", "HEAVEN": "triangle",
    "ISHILANKUL": "x_cross", "KANKUL": "stair", "SEED_SOWN": "three_dots", "OUT_OF_THE_TRIALS": "half_up",
    "WHOLE_ROUND": "cross", "ERA_BEGINS": "flower",
}


def _compact_forms():
    import compact as M
    out = {}
    for c, g in MAINS.items():
        if c in _TOKENS:
            out[c] = M.compact(g, getattr(M, _TOKENS[c]))
        elif c in _HEADS:
            tok = _HEADS[c]
            out[c] = M.compact(g, getattr(M, tok) if tok else None, head=True, size=_HEAD_SIZES.get(c, 0.22))
        else:
            out[c] = M.motif_compact(g, getattr(Y, _MOTIFS[c]), _SCALES.get(c, 0.95))
    return out


COMPACT = _compact_forms()


# -- layout --------------------------------------------------------------------------------------


def _place(parts, box_w, box_h, x0, y0, x1, y1, squeeze=1.0):
    """Parts drawn in a box ``box_w`` by ``box_h`` scaled into (x0, y0)–(x1, y1) and
    centred. Their proportions may change by up to ``squeeze`` to fill the slot. The
    brushes keep their widths."""
    kx, ky = (x1 - x0) / box_w, (y1 - y0) / box_h
    if kx > ky * squeeze:
        kx = ky * squeeze
    elif ky > kx * squeeze:
        ky = kx * squeeze
    ox = x0 + ((x1 - x0) - box_w * kx) / 2
    oy = y0 + ((y1 - y0) - box_h * ky) / 2
    out = []
    for pen, ps in parts:
        moved = []
        for p in ps:
            pts = [(ox + x * kx, oy + y * ky) for x, y in p.pts]
            moved.append(S.Fill(pts) if isinstance(p, S.Fill) else S.Track(pts, closed=p.closed, weight=p.weight))
        out.append((pen, moved))
    return out


PLACES = {20: 1, 400: 2, 8000: 3, 160000: 4}  # a place of the count, and the bars in its diamond


def _coefficient(n, x0, y0, x1, y1):
    """A number in a slot. One to nineteen stand as a coefficient, bars upright and dots
    stacked; zero is the shell, an empty thing; a place of the count is a diamond holding
    one bar for twenty, two for four hundred, three for eight thousand, four for a hundred
    and sixty thousand."""
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    r = min(x1 - x0, y1 - y0) / 2 - 20
    if n == 0:
        bowl = S.arc(cx, cy + r * 0.25, r * 0.9, r * 0.95, 200, 340)
        lid = S.arc(cx, cy - r * 0.15, r * 0.9, r * 0.5, 20, 160)
        ribs = S.bar(cx - r * 0.35, cy - r * 0.05, cx - r * 0.4, cy - r * 0.5) + S.bar(cx + r * 0.35, cy - r * 0.05, cx + r * 0.4, cy - r * 0.5)
        return [(CONTOUR, bowl + lid), (DETAIL, ribs)]
    if n in PLACES:
        k = PLACES[n]
        dy = (y1 - y0) / 2 - 20
        dx = min((x1 - x0) / 2 - 20, dy)
        out = S.poly([(cx, cy + dy), (cx + dx, cy), (cx, cy - dy), (cx - dx, cy), (cx, cy + dy)])
        for i in range(k):
            y = cy + dy * 0.5 * (1 - 2 * (i + 0.5) / k) if k > 1 else cy
            w = dx * (1 - abs(y - cy) / dy) * 0.55
            out.append(S.Fill(S._capsule(cx - w, y, cx + w, y, 14)))
        return [(CONTOUR, out)]
    bars, dots = divmod(n, 5)
    out = []
    x = x1 - 40
    for _ in range(bars):
        out.append(S.Fill(S._capsule(x, y0 + 40, x, y1 - 40, 28)))
        x -= 80
    if dots:
        step = min(110.0, (y1 - y0 - 80) / max(dots, 1))
        ys = [(y0 + y1) / 2 + (i - (dots - 1) / 2) * step for i in range(dots)]
        out += [f for y in ys for f in S.dot(x - 24, y, 34)]
    return [(CONTOUR, out)]


def _item(code, slot, x0, y0, x1, y1, shared):
    """Draw one code into a slot: ``main``, ``tall`` or ``flat``."""
    if code.startswith("n") and code[1:].isdigit():
        return _coefficient(int(code[1:]), x0, y0, x1, y1)
    if code in SIGNS:
        sign = SIGNS[code]
        if slot == "flat":
            return _place(sign.flat(), B * Y.SPAN, B * Y.AFFIX, x0, y0, x1, y1)
        return _place(sign.tall(), B * Y.AFFIX, B * Y.SPAN, x0, y0, x1, y1)
    draw = COMPACT[code] if shared and code in COMPACT else MAINS[code].draw
    placed = _place(draw(), R.WIDTH[MAINS[code].footprint], B, x0, y0, x1, y1, SQUEEZE)
    if shared:
        # A main sign that shares its block draws its outlines with the detail brush, never
        # finer, so its grooves keep a chisel's width at the smaller size.
        placed = [(R.DETAIL if pen is CONTOUR else pen, ps) for pen, ps in placed]
    return placed


def compose(block: str) -> list:
    """One block of codage, as ``n3*la1:JAGUAR`` or ``sho1*bi1``, laid out in a whole block.

    Items joined by ``*`` stand side by side; the leading ones before the main sign take
    tall slots at the block's start. Items joined by ``:`` stack, the first over the
    second: a syllable sign before the main sign's ``:`` is its superfix, one after it its
    subfix. Syllable signs alone in a block stand side by side, sharing it equally."""
    out = []
    parts = block.split("*")
    lead, last = parts[:-1], parts[-1]
    stack = last.split(":")
    mains = [c for c in stack if c in MAINS]
    if not mains:
        codes = lead + stack
        w = B / len(codes)
        for i, c in enumerate(codes):
            out += _item(c, "tall", i * w + GAP / 2, 0, (i + 1) * w - GAP / 2, B, True)
        return out
    main = mains[0]
    width = R.WIDTH[MAINS[main].footprint]  # a double-wide main makes a double-wide block
    at = stack.index(main)
    over, under = stack[:at], stack[at + 1:]
    shared = bool(lead or over or under)
    x = 0.0
    for c in lead:
        out += _item(c, "tall", x, 0, x + B * AFFIX, B, True)
        x += B * AFFIX + GAP / 2
    top, bottom = B, FLOOR
    for c in over:
        out += _item(c, "flat", x, top - B * AFFIX, width, top, True)
        top -= B * AFFIX + GAP / 2
    for c in under:
        out += _item(c, "flat", x, bottom, width, bottom + B * AFFIX, True)
        bottom += B * AFFIX + GAP / 2
    out += _item(main, "main", x, bottom if under else 0.0, width, top, shared)
    return out


def compose_name(codage: str) -> list[list]:
    """A run of blocks separated by ``-``."""
    return [compose(b) for b in codage.split("-")]
