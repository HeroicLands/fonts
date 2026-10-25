# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Render the Ch'alish P'ilam common hand's glyph sheet.

    .venv/bin/python tools/chalish-pilam/glyphs_sheet.py [--out specimens/chalish-pilam/glyphs.png]

The sheet has six parts: the 24 core glyphs by category, each with its concepts, the
word that names it and its sound; the glyphs beyond the core, with the tier that knows
them; the numbers; the compounds, two or three glyphs making a concept of their own;
one run of glyphs read several ways; and names written in sounds.
"""

import argparse
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
import glyphs as K  # noqa: E402
import strokes as S  # noqa: E402
from strokes_sheet import ADVANCE, GREY, INK, RED, Sheet  # noqa: E402

B = S.BLOCK


def glyph_at(sh, g, x, base, sc, cell=True):
    if cell:
        sh.cell(x, base, sc)
    sh.ink(f"glyph:{g.name}", g.draw, x, base, sc)


def card(sh, g, x, base, sc, tier=False):
    glyph_at(sh, g, x, base, sc)
    sh.text(x, base + 22, g.name, 14, INK, weight="bold")
    sh.text(x + B * sc - 4, base + 22, g.sound or "—", 17, RED, weight="bold", anchor="end")
    lines = g.meaning.split("; ")
    sh.text(x, base + 40, lines[0], 12, INK)
    if len(lines) > 1:
        sh.text(x, base + 55, "; ".join(lines[1:]), 11, GREY)
    sh.text(x, base + 70, (g.word or "(no word yet)") + (f" · {g.tier}" if tier else ""), 11, GREY)


def compound(sh, w, x, base, sc):
    for i, g in enumerate(w.glyphs):
        glyph_at(sh, g, x + i * ADVANCE * sc, base, sc)
    tx = x + max(3, len(w.glyphs)) * ADVANCE * sc + 10
    sh.text(tx, base - B * sc + 16, w.word, 14, INK, weight="bold")
    sh.text(tx, base - B * sc + 33, " + ".join(g.name for g in w.glyphs), 11, GREY)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "specimens/chalish-pilam/glyphs.png"))
    args = ap.parse_args()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    W = 2400
    sh = Sheet(W)
    sh.y = 50
    sh.text(40, sh.y, "Ch'alish P'ilam, the common hand — layer 2: the glyphs", 36)
    sh.y += 34
    for line in [
        "Every glyph is built from the strokes of layer 1, in one even line. A glyph is a concept; two or more together make "
        "another, the first usually the head and the rest modifying it. Context decides.",
        "Nearly everyone knows the 24 core glyphs, and a few more of their trade. Scribes know many more, the long compounds "
        "and the sound of every glyph; priests know the sacred glyphs.",
        "A glyph's sound is the opening consonant and vowel of the word that names it, its catch left out. Drawn from "
        "tools/chalish-pilam/glyphs.py.",
    ]:
        sh.text(40, sh.y, line, 15, GREY)
        sh.y += 21

    # -- part 1: the core
    sh.heading("The 24 core glyphs")
    sc = 0.24
    cw = B * sc
    for half in (K.CATEGORIES[:3], K.CATEGORIES[3:]):
        base = sh.y + cw + 34
        x = 40
        for cat, gs in half:
            sh.text(x, sh.y + 18, cat, 15, INK, weight="bold")
            for g in gs:
                card(sh, g, x, base, sc)
                x += 185
            x += 45
        sh.y = base + 90

    # -- part 2: beyond the core
    sh.heading("Beyond the core: glyphs of a trade, of the scribes, and of the priests")
    x = 40
    base = sh.y + cw + 10
    for i, g in enumerate(K.OUTER):
        if i and i % 11 == 0:
            base += cw + 100
            x = 40
        card(sh, g, x, base, sc, tier=True)
        x += 210
    sh.y = base + 90

    # -- part 2b: the sound glyphs
    for title, gs in (("Glyphs whose sound is their word's opening", [K.METAL] + K.FROM_WORDS),
                      ("Glyphs with traditional sounds: the sounds of the first codex, known to scribes", K.TRADITIONAL)):
        sh.heading(title)
        x = 40
        base = sh.y + cw + 10
        for i, g in enumerate(gs):
            if i and i % 11 == 0:
                base += cw + 100
                x = 40
            card(sh, g, x, base, sc, tier=True)
            x += 210
        sh.y = base + 90

    # -- part 2c: coverage
    sh.heading("Every syllable Ki'i'chek uses, and the glyphs that write it")
    by_sound = {}
    for g in K.GLYPHS + K.NUMERALS + K.PLACES:
        if g.sound:
            by_sound.setdefault(g.sound, []).append(g.name)
    per_col = 16
    for i, syl in enumerate(K.SYLLABLES):
        col, row = divmod(i, per_col)
        x, y = 40 + col * 590, sh.y + 20 + row * 21
        names = by_sound.get(syl, [])
        sh.text(x, y, syl, 14, RED if not names else INK, weight="bold")
        sh.text(x + 50, y, ", ".join(names) if names else "— none", 12, RED if not names else GREY)
    sh.y += 20 + per_col * 21 + 10
    missing = [syl for syl in K.SYLLABLES if syl not in by_sound]
    sh.text(40, sh.y, f"{len(K.SYLLABLES) - len(missing)} of {len(K.SYLLABLES)} syllables written"
            + (f"; missing: {' '.join(missing)}" if missing else ""), 14, RED if missing else INK, weight="bold")
    sh.y += 10

    # -- part 3: the numbers
    sh.heading("The numbers: the shell for zero, then bar and dot; then the places of the count")
    sc2 = 0.085
    base = sh.y + B * sc2 + 10
    for n, g in enumerate([K.ZERO] + K.NUMERALS + K.PLACES):
        x = 40 + n * (ADVANCE * sc2 + 22)
        glyph_at(sh, g, x, base, sc2)
        sh.text(x + B * sc2 / 2, base + 20, str(n) if n < 20 else g.meaning, 12, GREY, anchor="middle")
    sh.y = base + 40

    # -- part 4: compounds
    sh.heading("Compounds: the first glyph is usually the head, and those after it modify it")
    sc3 = 0.1
    per_row = 5
    pitch = (W - 80) / per_row
    for i, w in enumerate(K.COMPOUNDS):
        col, row = i % per_row, i // per_row
        if col == 0 and row:
            sh.y += B * sc3 + 30
        compound(sh, w, 40 + col * pitch, sh.y + B * sc3 + 10, sc3)
    sh.y += B * sc3 + 50

    # -- part 5: one run, several readings
    sh.heading("One run, several readings: context decides how the glyphs group")
    sc4 = 0.16
    base = sh.y + B * sc4 + 10
    for i, g in enumerate((K.MAN, K.HIGH, K.HOUSE)):
        glyph_at(sh, g, 40 + i * ADVANCE * sc4, base, sc4)
    tx = 40 + 3 * ADVANCE * sc4 + 30
    for j, (group, reading) in enumerate([
        ("(MAN + HIGH) + HOUSE", "the elder man of the household"),
        ("MAN + (HIGH + HOUSE)", "a man of the great house: a nobleman"),
        ("MAN + HIGH + HOUSE", "the conventional compound: the patriarch"),
        ("or, plainly", "a man standing on the roof of his house"),
    ]):
        sh.text(tx, sh.y + 22 + j * 20, group, 13, RED)
        sh.text(tx + 230, sh.y + 22 + j * 20, reading, 13, GREY)
    sh.y = base + 40

    # -- part 6: names in sounds
    sh.heading("Names written in sounds, a scribe's skill: a closing consonant takes a syllable whose vowel is silent")
    base = sh.y + B * sc4 + 10
    for i, w in enumerate(K.SPELLINGS):
        x = 40 + i * 900
        for k, g in enumerate(w.glyphs):
            glyph_at(sh, g, x + k * ADVANCE * sc4, base, sc4)
        tx = x + 3 * ADVANCE * sc4 + 20
        sh.text(tx, sh.y + 26, w.word, 15, INK, weight="bold")
        sh.text(tx, sh.y + 44, w.gloss, 12, GREY)
        sh.text(tx, sh.y + 62, w.why, 13, RED)
    sh.y = base + 40

    height = int(sh.y + 30)
    svg_file = out.with_suffix(".svg")
    svg_file.write_text(sh.svg(height))
    subprocess.run(["rsvg-convert", "-o", str(out), str(svg_file)], check=True)
    print(out)


if __name__ == "__main__":
    main()
