# Thuravark Carved

The rune-row of the Nordmen of thalorna, the reduced daughter of Pirzath
Carved. Twenty-eight staves, ten numerals and one mark, all straight; and the
imperial recension of Vylaria, the Tharavarkon, which adds three staves, two
crown marks and ten bound runes to the same row.

## Source

The source of the font is the UFO `sources/ThuravarkCarved.ufo`: the outlines,
the character map, the metrics and `features.fea`. The design is settled. The UFO
is edited in a font editor and built with `fontmake`; `./build.sh` at the
repository root builds both fonts. The recension's glyphs are drawn into the UFO
by `tools/thuravark-carved/staves.py` from the stave system's constants, and the
crowned frame is added to the built font by `tools/thuravark-carved/crown.py`,
which `build.sh` runs.

## The staves

Every stave is one upright stem, 733 units tall, with up to four straight
branches. A branch is written side, level it leaves from, level it ends at: `F`
forward or `B` back; `T` top, `M` middle, `0` foot. Two lengths exist. A long
branch spans the whole stem over a short run at slope 2.73, the angle of
Pirzath's tent and trough arms. A half branch spans half the stem over a longer
run at slope 0.86, the angle of Pirzath's point arms. No branch has another
slope and none is horizontal. The strokes are Pirzath's graver grooves, united
into one outline.

In the design space a stem is 740 units tall and 85 wide, and every stroke, stem
or branch, is one tapered groove: a parallel-sided cut whose two ends come to a
point 59 units long. The union of the stem and its branches is scaled by the
face's factor of 0.99 (`tools/vertical.py`), rounded, and stood at the
sidebearing. `tools/thuravark-carved/staves.py` holds the construction; the
settled staves of the row stand within three units of it.

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
follows the inventory table row for row; the typed input of each stave is in the
specimen table in `tools/thuravark-carved/specimens.py`.

| Typed                                            | Draws                                             |
| ------------------------------------------------ | ------------------------------------------------- |
| the 22 single letters, and `th dh kh gh ng hl`   | their stave; the six digraphs are ligatures       |
| `ngh`                                            | n and gh                                          |
| `j`, and `y` before a vowel                      | the glide, a half branch rising from the middle   |
| `y` anywhere else                                | the stave i                                       |
| `q`                                              | the stave k                                       |
| `á é í ó ú`, or a vowel then U+0301              | the vowel stave twice                             |
| a doubled vowel letter                           | the stave twice                                   |
| a doubled consonant, `tth ddh kkh ggh hhl nng`   | two staves, two digraph staves                    |
| `0`-`9`                                          | the numerals                                      |
| `.` `?` `!` `!!`                                 | a short horizontal dash, the row's one horizontal |
| space and `-`                                    | nothing; the hyphen breaks a ligature             |
| the other standard roman marks                   | nothing: invisible marks alone                    |
| `c x`, a capital and every other punctuation key | the box, a copy of `.notdef`                      |

The table is how Nordmal is written in the staves; thalorna states it. The
recension's characters, `ai`, `au` and `oi`, draw their own staves, and the crown
marks stand around a name.

## Numerals

A stem 891 tall, taller than any stave, with up to four tally limbs worth 8,
4, 2 and 1. Limbs fall outward from the stem at slope 1.5, a slope no stave has,
over a run of 220, and leave it at heights no stave branch leaves from; the
lowest ends on the baseline. No two value limbs leave at one height, so nought
carries the one pair that does: two limbs of the same length rising from 149,
a cup no value makes and no stave has.

## The imperial recension

Tharavarkon, the carved script of imperial Vylaria, is written in Thuravark's
staves and adds three things to the row: three characters for sounds the row has
no stave for, crowned runes, and bound runes for the architrave. All three are in
Thuravark Carved, on Thuravark's block.

### The three staves

The three characters are the sounds Vylari writes that the row cannot. Vylari's
consonants, _p t k b d g f th s z v h m n l r_ and the glide _y_, each have a
stave, and so do its five vowels; a long vowel is written double, which is the
row's own rule. What Vylari's spelling declares and the row lacks is its three
diphthongs, **_ai_, _au_ and _oi_**, each one syllable in Vylari and written in
Thuravark as two staves that read as two. Pirzath, the parent row, has letters
for five diphthongs; the Nordmen dropped them, since Nordmal has none, and the
recension keeps the three Vylari uses. The gap is exactly three.

Each diphthong stave is the first vowel's stave with the off-glide's branch:

| Stave | Branches      | Built as                                                                                                     |
| ----- | ------------- | ------------------------------------------------------------------------------------------------------------ |
| ai    | `F0T FMT`     | a, with the glide's own branch, a half branch rising forward from the middle, as j                           |
| au    | `F0T B0M`     | a, with u's branch at half length, rising back from the foot                                                 |
| oi    | `BTM B0M FMT` | o's diamond keeps its back half, so that the forward side is free for the glide; the glide's branch is added |

They sit at U+F0128 to U+F012A, a diphthong group after the digraphs. No set
matches a stave of the row, and each is at least 35 pixels from its nearest
neighbour at 36 px (a and ai are the closest pair). The recension writes no
catch: imperial Vylari has none, and these three are its whole gap.

### Crowned runes

A crown is cut around the name of a god, a founder or a reigning emperor. The
font draws it from a pair of format controls on Thuravark's block, as Khelathi
Zethu Glyphs draws its cartouche: **crown open** (U+F0150) before the name and
**crown close** (U+F0151) after it. Between them the font cuts a frame of
straight grooves of half the stem's weight, 42 units, so the frame reads lighter
than the name it holds: a post at each end and a rail above and below, the rails
one stroke clear of the staves' tops and of the baseline, from −126 to 859,
inside the line box. A numeral, taller than a stave, stands into the top rail.

The two marks are drawn in the source as bare posts, square-ended. At build time
`crown.py` reads the frame's bottom, top and weight from the open post and adds
the posts joined to the rails over their own advance, and for every glyph a name
may hold its crowned form: the glyph's outline with the rails over its own
advance, so the rails meet end to end whatever the frame holds, a space or a
bound rune included. The shaping sits in `rclt`, which every shaper applies and
no style sheet turns off, and reads the run left to right: the open becomes the
opened post when a close follows within forty glyphs; a glyph after the opened
post or a crowned glyph takes its crowned form; the close after either becomes
the closed post. An open with no close, a close with no open, a crown longer
than forty glyphs, and a crown holding a character with no stave each leave the
marks as bare posts, a visible mark, with the staves beside them unchanged: the
font never draws a broken frame. The frame is shaped by GSUB alone; the font has
no GPOS.

### Bound runes

A bound rune sets two staves on one stem, so a long dedication fits a fixed
architrave. The system allows a pair when the two staves share no branch, the
union has at most four, no more than two leave the stem at one level, and the
set matches no stave and no other bound rune. The ten most frequent stave pairs
of the Vylari lexicon that the system allows are bound, in the order of their
frequency: **en, el, ar, al, ma, za, ka, ur, lm, lth**. The commonest pairs the
system refuses are _os_, _the_, _on_ and _or_, each sharing a branch or wanting
more than four.

The bound runes sit behind the stylistic set `ss01`, named "Bound runes", so
plain Thuravark text is unchanged; the class `hl-thuravark-carved-bound` sets the
font with it on, as `fonts.json` lists it. A bound rune has no code point. It
is a ligature of the two staves' characters, drawn by `staves.py` from the union
of their branches, and inside a crown it takes a crowned form like any glyph.

## Checks

`tools/thuravark-carved/guard.py` shapes the fixtures of `fixtures.json`, sequences of
glyph codes, and asserts the glyphs each gives, and asserts the
stave design: 31 distinct staves and ten bound runes, each bound rune within the
binding rule, no horizontal edge in any of them, numerals taller than staves,
and every pair at least 20 pixels apart at 36 px. The recension's fixtures cover
the three staves, crowned names, an unclosed open and a stray close, a crown of forty-one
glyphs, and the bound runes with `ss01` on and the same text unchanged with it
off; a rendered crowned name's rails are checked for a break.
`tools/thuravark-carved/check_font.py`
checks the cmap, the empty glyphs, the name table, the recension's glyphs and
features, and the `.woff2`. `tools/thuravark-carved/staves.py --check` draws
the recension's glyphs afresh and reports any that differ from the source.
`tools/prove_guards.py` removes the GSUB table from the built
font, which drops the ligatures and decomposition, and the guard must fail on it;
it also takes out the lookup that frames a crown, empties `ss01`, and turns
`ss01` on in plain text, and the guard must fail on each.

## The visual loop

Specimens are `specimens/thuravark-carved/01-glyph-chart.png`, `02-nordmal.png`,
`03-numerals.png`, `04-descent.png` (each stave beside its Pirzath parent,
then the same words in both fonts) and `05-recension.png` (the three staves
beside the vowels written apart, crowned names, an unclosed open, and each bound
rune beside the pair it binds).

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
- **a and ai** stay apart by the glide's branch alone, at 35 pixels; the glide's
  branch crosses a's long branch near the stem, as kh's two forward branches
  cross.
- **The frame's weight.** The crown's posts and rails are half the stem's
  weight. The weight is read from the open post, so changing the two marks in
  the source changes the whole frame.

## Licence

SIL Open Font License 1.1, the same licence and copyright as Pirzath Carved.

## Showing the script

A handout, a shield device, a banner or a logo shows a whole word or a name in this script, never a single stave standing alone. Several staves, seen on their own, share their shape with runes that are used as hate symbols; inside a word they read as letters.

The sentence end is always the last mark of a sentence, outside a closing quotation mark or any other mark: _Galdan bunát, "Dalík bant, maríg bant"._
