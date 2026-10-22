# Thuravark Carved

The rune-row of the Nordmen of thalorna, the reduced daughter of Pirzath
Carved. Twenty-eight staves, ten numerals and one mark, all straight.

## Source

The source of the font is the UFO `sources/ThuravarkCarved.ufo`: the outlines,
the character map, the metrics and `features.fea`. The design is settled. The UFO
is edited in a font editor and built with `fontmake`; `./build.sh` at the
repository root builds both fonts.

## The staves

Every stave is one upright stem, 733 units tall, with up to four straight
branches. A branch is written side, level it leaves from, level it ends at: `F`
forward or `B` back; `T` top, `M` middle, `0` foot. Two lengths exist. A long
branch spans the whole stem over a short run at slope 2.73, the angle of
Pirzath's tent and trough arms. A half branch spans half the stem over a longer
run at slope 0.86, the angle of Pirzath's point arms. No branch has another
slope and none is horizontal. The strokes are Pirzath's graver grooves, united
into one outline.

A tent or trough arm passes 134 units from the stem at the middle level, so a
half branch leaving there on the arm's side has no daylight against it. The
voicing branch of b and d leaves at the end of the stem the arm does not, from
the foot under the tent and from the top over the trough, and crosses the arm
where the two are 268 units apart. The nasals are one long arm of their family
and one half branch leaving at the middle on the other side: m falls, n rises.
No stave has more than two branches meeting at one point.

Each stave stands at its ink with 34 units of white a side, the font's spacing
rule (see `design/making-fonts.md`), and carries its own room: the font has no
kerning and no mark positioning. The branch of each stave is in the guard's table, `tools/thuravark-carved/guard.py`, which
follows the inventory table row for row.

The face draws each stave, numeral and mark from its own code point, U+F0100 to
U+F01FF, and from nothing else: a Latin letter, digit or mark draws the box. Its
one contextual form is the acute mark after a vowel, which draws that vowel's
stave again (`a.acute`), so a long vowel is the stave twice. A note writes
Nordmal in roman, and thalorna's `thuravark` mapping note turns the spelling
into these code points:

| Spelled                                        | Written                                             |
| ---------------------------------------------- | --------------------------------------------------- |
| the 22 single letters, and `th dh kh gh ng hl` | their stave; each of the six digraphs is one stave  |
| `ngh`                                          | n and gh                                            |
| `j`, and `y` before a vowel                    | the glide, a half branch rising from the middle     |
| `y` anywhere else                              | the stave i                                         |
| `á é í ó ú`                                    | the vowel and the acute mark: the vowel stave twice |
| a doubled vowel letter                         | the stave twice                                     |
| a doubled consonant, `tth ddh kkh ggh hhl nng` | two staves, two digraph staves                      |
| `q`, `ë`                                       | the staves k and e                                  |
| `0`-`9`                                        | the numerals                                        |
| `.`                                            | a short horizontal dash, the row's one horizontal   |
| `-`                                            | nothing; the space draws nothing too                |
| `c x` and every other punctuation key          | passed through, so the face prints the box          |

## Numerals

A stem 891 tall, taller than any stave, with up to four tally limbs worth 8,
4, 2 and 1. Limbs fall outward from the stem at slope 1.5, a slope no stave has,
over a run of 220, and leave it at heights no stave branch leaves from; the
lowest ends on the baseline. No two value limbs leave at one height, so nought
carries the one pair that does: two limbs of the same length rising from 149,
a cup no value makes and no stave has.

## Checks

`tools/thuravark-carved/guard.py` writes every Nordmal form on thalorna `origin/main` (words,
affixes, elements, given and clan names) and a set of fixtures through the `thuravark`
mapping note, shapes them and asserts the glyphs the spelling demands, and asserts the
stave design: 28 distinct branch sets, no horizontal edge in any stave,
numerals taller than staves, and every pair of staves at least 20 pixels apart
at 36 px. `tools/thuravark-carved/check_font.py`
checks the cmap, Latin text on the box, the empty glyphs, the name table and the
`.woff2`. `tools/prove_guards.py` removes the GSUB table from the built font, which
drops the acute mark's stave, and the guard must fail on it.

## The visual loop

Specimens are `specimens/thuravark-carved/01-glyph-chart.png`, `02-nordmal.png`,
`03-numerals.png` and `04-descent.png` (each stave beside its Pirzath parent,
then the same words in both fonts).

## Flagged for a designer pass

- **Width.** Kept at the inventory's slopes, a half branch spans half the stem
  over a run of 426, wider than it is tall, so e, o, s, k, ng, m and n are not
  narrower than Pirzath's letters; only the long-branch staves and the bare i
  are. The brief's "taller and narrower" and the slopes cannot both hold for
  these. A designer should choose between shortening the half branches and
  steeper half slopes.
- **o.** A wide closed diamond on a tall stem, the widest stave in the row.
- **k and r.** Mirror triangles; distinct by direction only.
- **t/th and d/dh** stay apart only by the one half branch, at 34 and 35 pixels.

## Licence

SIL Open Font License 1.1, the same licence and copyright as Pirzath Carved.

## Showing the script

A handout, a shield device, a banner or a logo shows a whole word or a name in this script, never a single stave standing alone. Several staves, seen on their own, share their shape with runes that are used as hate symbols; inside a word they read as letters.

The sentence end is always the last mark of a sentence, outside a closing quotation mark or any other mark: _Galdan bunát, "Dalík bant, maríg bant"._
