# Pirzath Hand — design notes

Pirzath Hand is the everyday printed hand of Pirzath, _milgath_, the script of
the Khazari of thalorna: the working hand of engineers, miners and smiths,
written in chalk on a shaft wall, on a slab of slate, or in pencil on a scrap
of paper. It writes the same letters as Pirzath Carved, on the same code points;
the two faces differ in how the letters are made, never in which letters there
are. It is one printed face: every letter stands apart, and there is no joined
form.

The font is built in three layers, each generated from data and approved on its
own sheet before the next is drawn: the strokes (`tools/pirzath-hand/strokes.py`),
the signs built from them (`tools/pirzath-hand/letters.py`), and the font
(`tools/pirzath-hand/build_ufo.py`). The sections below take them in turn.

## The characters and the forms

The hand draws the same characters, on the same code points, as the carved face,
and nothing else: a Latin letter, digit or mark draws the box. A note writes
Pirzath in roman, and the `pirzath` encoding turns the spelling into
these code points, by the same rows for both faces. What the hand draws beyond
its characters is contextual:

- A vowel and the length mark after it are drawn as one long-vowel glyph. A
  length mark on a vowel pair is a separate mark above the pair.
- A consonant or digraph letter written twice is its doubled glyph.
- The default-ignorable characters draw nothing: they map to an empty glyph,
  and a `ccmp` substitution turns that into a second empty glyph, so the
  shaper does not replace them with the space.

The sentence end stands with no space on either side; the next sentence begins
straight after it. That is how Pirzath is written, not a rule of the font: a
space written there is drawn.

## Layer 1: the strokes

The hand is the hand of daily work: the writing of engineers, miners and
smiths, marked on a timber, a tally board, a slate in a shaft, a work order, a
crate label or a measurement on a plan. It has been written daily for four to
five thousand years and has worn as far as any script ever has, so its letters
keep little of the carved runes beyond their angular character. Each
letter is the simplest form that stays distinct. Its virtues are those of the
work:

- **It reads at a glance in poor light.** The strokes are heavy, the counters
  open, and nothing stands inside a counter.
- **It is written fast by a hand that also swings a hammer.** A letter is one
  or two quick movements, three at most, and no movement needs a careful small
  turn.
- **It survives a blunt tool on rough rock.** Every stroke is a straight line
  or the one plain curve, the round. A letter changes direction only at a clear
  corner where two straight runs meet, never inside a run, because in chalk on
  uneven rock a small change of direction is lost or turns into a wobble. There
  are no fine details, no small closed shapes and no fine marks.
- **The test.** A miner can write every letter with a stub of chalk on uneven
  rock by lamplight, and another miner reads it at a glance. A form that fails
  this goes.
- **It leaves no ambiguity between letters, and none between digits.** The
  digits are the plainest and most distinct signs in the hand.

It is plain and economical, never ornamental: no flourish, no swash, no tall
riser, no floating mark. A mark is written only where a sound would otherwise be
unwritable, as one plain full stroke, and a letter given its own form needs no
mark. The contrast is what the tool gives and nothing more.

**Every part is full-size or absent.** Each part of a letter is a stroke of real
length, at least half the body, that a hurried hand still makes deliberately,
or it is not there. There are no flicks, ticks, stubs or short heels: writing
in chalk on the ground, a hand drops them. Each form is tested both ways: if its
smallest part were left off and it stayed distinct, the part goes; if it would
no longer be distinct, the part is made full-size.

**It is printed, never joined.** Each letter stands apart, made in its own
strokes, with generous room between letters and a clear word space, so letters
never touch in low light. There is no joining line: the hand is one face with
no `ss01` set and no lifted variant.

This section covers layer 1, the strokes.

### The size

The hand has no capitals and few extenders, so nearly all of its ink stands in
one band, the body. A line of Latin is read at the size its capitals and
ascenders give it, not at its x-height, so the body stands at Latin's cap
height, 0.73 em, the shared cap height and the height of Pirzath
Carved's consonants. Set at one font size, a line of the hand, a mixed-case
Latin sentence and the carved face read as one size of text. A vowel stands at
0.46 em, near Latin's x-height, as the carved face scores its vowels small. The
few extenders stay short against the body.

### The tool

The hand is written in chalk on a shaft wall, on a slab of slate, or in pencil
on a scrap of paper kept in a pocket. Its tool is blunt: **the squared end of a
chalk stick or a broad carpenter's pencil, 74 by 46 units, held at 45° to the
line, upright.**

- **Monoline at heart.** The end is only a little wider than it is thick, so a
  stroke's weight follows its direction mildly: a forward fall (`\`), an
  upright and a level stroke are the fullest, a stroke rising at the tool's own
  angle the lightest, and the two differ by about 1.7 to 1. Every letter reads
  as if written with an even stroke; contrast never tells two letters apart.
- **A solid weight.** Strokes are as heavy as the carved face's cuts, so a line
  reads on a wall in lamplight, neither spindly nor black.
- **Blunt ends.** The end's corners are soft, so a stroke ends square with
  softened corners.
- **Small, blunt turns.** Where a stroke changes direction, the tool pivots
  through a turn of radius 18: decisive, as a chalk point makes it, never a
  needle-sharp angle and never a loop. The one curve is the round.

### Metrics

Units are thousandths of the em, the line at 0. The line metrics are the shared
standard of `tools/vertical.py`: ascender 945, descender −200, line gap 100.
The strokes are drawn at the font's own size, so the font takes the outlines
unscaled. The body is the face's cap height, so the vertical guard measures
the hand against the shared cap height.

| Constant   | Value | What it governs                                                       |
| ---------- | ----- | --------------------------------------------------------------------- |
| `BODY`     | 730   | A consonant's body: Latin's cap height, 0.73 em.                      |
| `VOWEL`    | 460   | A vowel's body, 0.63 of a consonant's.                                |
| `LATIN_X`  | 513.5 | The shared x-height, 0.5135 em: a guide, which the vowels stand near. |
| `ASC`      | 870   | The head of a rising stroke: a fifth of the body above it.            |
| `DESC`     | −175  | The foot of a descending stroke, inside the shared descent.           |
| `LENGTH_Y` | 580   | The height of the length bar over a vowel.                            |
| `FULL`     | 365   | The shortest part a letter may have: half the body.                   |
| `MID`      | 328.5 | The height the marks between words stand at.                          |
| `TURN`     | 18    | The radius the tool pivots on in a turn.                              |
| `HEEL`     | 365   | The length of a heel: a full base along the line.                     |

| End width | Thickness | Angle | Flex | Corner softness | Slant |
| --------- | --------- | ----- | ---- | --------------- | ----- |
| 74        | 46        | 45°   | 0.10 | 0.5             | 0°    |

Measured across the stroke, a forward fall is 76 units, a level stroke and a
stem 72, a back fall 59 and a stroke at the tool's angle 46. A stem is about
one tenth of the body.

### Using the generator

```python
import strokes as S

tent = S.shape("tent", 0, 0, heel=1)          # a Shape: tracks, entry and exit
roof = S.shape("roof", 560, 0)                # one movement: along the top, pivot, down
path = S.outline(tent.tracks + roof.tracks)   # a pathops.Path, font units, y up
S.contours(path)                              # polygons
```

`STROKES[id].params` gives each parameter's minimum, default and maximum, and
`shape` refuses a value outside them, naming the stroke, the parameter and the
range. `tools/pirzath-hand/strokes_sheet.py` renders
`specimens/pirzath-hand/strokes.png`:

```sh
.venv/bin/python tools/pirzath-hand/strokes_sheet.py
```

### The stroke inventory

Eleven strokes in three kinds. Lengths are font units; `peak`, `base`,
`rise`, `at`, `left` and `lean` are shares.

| Id       | Kind  | Skeleton                                                                                               | Fullest at              | Permitted                                                                                                      |
| -------- | ----- | ------------------------------------------------------------------------------------------------------ | ----------------------- | -------------------------------------------------------------------------------------------------------------- |
| `stem`   | stem  | an upright pulled straight down, to the ascender or the descender if need be                           | all of it               | top 292–870, foot −175–694, heel 0 or 1, side −1 or 1                                                          |
| `cut`    | frame | a straight diagonal from its head down, falling forward or back                                        | the forward fall        | w 73–584, h 219–1045, top 219–870, fall −1 or 1, heel 0 or 1, side −1 or 1                                     |
| `tent`   | frame | up to an apex set back of centre, pivot, and down a forward fall                                       | the right leg           | w 292–657, h 230–870, peak 0.3–0.6, turn 0–30, left 0.5–1, heel 0 or 1, side −1 or 1                           |
| `trough` | frame | down a forward fall to a point, pivot, and up a shorter, lighter arm                                   | the left arm            | w 328–657, h 230–870, base 0.15–0.6, rise 0.5–1, turn 0–30                                                     |
| `point`  | frame | down to a point at the fore (or back) side, pivot, and down again, standing narrow                     | the upper arm of `>`    | w 219–511, h 230–1045, at 0.4–0.7, side −1 or 1, turn 0–30, heel 0 or 1, upper 0.5–1, lower 0.5–1, away 0 or 1 |
| `roof`   | frame | one movement: along the top from the left, pivot, and down to the foot                                 | the head and the fall   | w 219–584, h 230–870, lean −0.3–0.3, turn 0–30, heel 0 or 1, side −1 or 1, hand −1 or 1, foot −175–0           |
| `zigzag` | frame | one movement of angular turns between the line and the head                                            | the forward falls       | w 365–803, h 230–870, turns 2–4, start −1 or 1, turn 0–30                                                      |
| `round`  | frame | a plain oval in one movement from the head: the only closed shape                                      | the back and fore sides | w 255–620, h 230–730, square 0–0.4                                                                             |
| `cross`  | frame | two diagonals crossing: the forward fall, then the back fall over it                                   | the forward fall        | w 255–584, h 230–870, lean −0.3–0.3                                                                            |
| `notch`  | mark  | a free straight cut, full-size: a digit's tally strokes, the doubling mark laid shallow under a letter | the whole cut           | length 365–511, angle 0–175°, at −175–870                                                                      |
| `bar`    | mark  | a level stroke drawn forward: the sentence end, the dash, the length bar over a vowel                  | the whole stroke        | w 365–584, at 0–870, tilt −20–20°                                                                              |

- **Marks live in the strokes.** A `heel` turns a foot through a clear corner
  into a full base along the line, half the body long, forward on a tent so it
  never closes the shape. It distinguishes letters inside their own strokes.
  Only the length bar, the doubling mark and a digit's tally strokes stand
  apart, and each is a full stroke: the length bar is a level stroke over the
  vowel, the doubling mark a shallow stroke laid under the letter.
- **Worn forms.** `roof`, `zigzag`, the tent's `left` (the left leg cut to half
  its length, still a full stroke) and a trough whose right arm stands half
  height are the movements thousands of years of daily writing leave: a frame
  and a pole, or two frames, become one movement.
- **The digits stand a little shorter.** A digit's stem is 0.85 of the body,
  standing on the line, so a digit is never taken for a letter. Each tally
  stroke is full-size, half the body long and as heavy as the stem, starting at
  the stem and running out at 60°: 8 from the head down forward, 4 from the
  middle down forward, 2 from the middle up back and 1 from the line up back.
  Only their places count.

### The specimen

`specimens/pirzath-hand/strokes.png` holds:

- every stroke large, against the line, the body and, faint, the vowel height,
  the ascender and the descender, a mark shown on a letter in grey;
- every stroke at 24 and 48 px to the em, after _xhn_ in Liberation Mono at the
  same size;
- rough skeletons built from the strokes at display size, the heel shown on a
  tent, a point and a roof;
- worn forms: a carved frame as the hand first writes it, in grey, beside the
  settled form, one or two movements;
- the tally test: a short stem with up to four full-size strokes, 0 to 15, at display size and at
  48 and 24 px;
- one skeleton drawn over its own track, the track a red line under the ink;
- skeletons written with the tool at 30°, 40°, 50° and 60°, for comparison;
- the worn forms run on as printed words at 96, 48 and 24 px, a letter's white
  70 units a side and the word space half an em, beside the mixed-case
  sentence _Gaz Guruz, Tanv-guráz._ in Liberation Mono and the same words in
  Pirzath Carved, all three at one font size.

The skeletons, the worn forms and the tally test test the strokes. They are not
letters or numerals of the script.

## Layer 2: the signs

`tools/pirzath-hand/letters.py` builds every sign the hand encodes from the
strokes of layer 1, and `tools/pirzath-hand/letter_sheets.py` renders
`specimens/pirzath-hand/letters.png`:

```sh
.venv/bin/python tools/pirzath-hand/letter_sheets.py
```

Every sign is one, two or at most three pen movements, every part of it is a
full stroke, and the hand is one printed face: no joined forms, no `ss01`.
Each sign stands apart with 70 units of white either side of its ink, and the
word space is half an em. The code points are those of the characters above.

### The consonants

A consonant of the carved row keeps its family's frame, worn to the simplest
stroke, and the carved modifiers become full strokes inside the sign.

| Frame          | plain | voiced: a stem in the frame | breathed: an arm worn to half | voiced and breathed |
| -------------- | ----- | --------------------------- | ----------------------------- | ------------------- |
| the tent, `Λ`  | _p_   | _b_                         | _f_, the left leg             | _v_                 |
| the trough `V` | _t_   | _d_                         | _th_, the right arm           | _dh_                |
| the point `>`  | _k_   | _g_                         | _kh_, the lower arm           | _gh_                |

The voiced stem stands from the tent's apex to the line, from the trough's base
to the head, and from the point's vertex to the line.

| Letter    | Sign                                                             |
| --------- | ---------------------------------------------------------------- |
| _m_       | the roof with a heel back: `]`                                   |
| _n_       | the roof run back with a heel forward: `[`                       |
| _ng_      | _m_ carried below the line                                       |
| _ny_      | _n_ carried below the line                                       |
| _s_       | the forward fall with a heel back under it                       |
| _sh_      | the back fall with a heel forward under it                       |
| _z_       | a forward fall crossed high by a full back cut                   |
| _zh_      | _z_ with a heel forward on the fall                              |
| _l_       | a tall back fall to the ascender, a forward fall from its middle |
| _hl_      | _l_ with a heel forward on the branch                            |
| _r_       | the point opening forward: `<`                                   |
| _h_       | _r_ with its lower arm worn to half                              |
| the catch | a long back fall from the head into the descender                |
| _ts_      | the point with a heel turned out behind it                       |
| _ch_      | _r_ with a heel turned out ahead of it                           |
| _j_       | a long forward fall from the ascender into the descender         |
| _q_       | the back fall with a heel turned out behind it                   |
| _w_       | the point with its upper arm worn to half                        |
| _y_       | the point with its lower arm carried into the descender          |

### The vowels and the pairs

The vowels stand at the vowel height, smaller than the consonants: _a_ a back
fall, _u_ a forward fall, _i_ an upright, _e_ a small tent, _o_ a small round.
A long vowel carries the length bar, a full level stroke, over it. A pair is
one sign: _ai_ the back fall and the upright meeting at the head, _au_ a small
trough, _ei_ the small tent with the upright close beside it, _oi_ a small round
with the upright rising from its head, _ou_ the round with the forward fall
from its side.

### The marks and the points

A doubled consonant is the letter once with the doubling stroke laid shallow
under it; under a descender the stroke stands beside it. The sentence end is a
level stroke at mid height, the imperative two, the pause a level stroke on the
line, the name dash a level stroke rising at mid height. The opening quotation
mark is drawn as the vowel _u_ (`\`) and the closing mark as _a_ (`/`), each set
against its word with no more than the letter spacing, so a quotation reads
`\word/` and each mark leans into its word at the foot. No Khazari word begins
or ends with a vowel, and a Khazari speaker drops the opening vowel of a foreign
name (_Árdavon_ is said _rdavon_), so a _u_ sign right before a word can only
open a quotation and an _a_ sign right after a word can only close one. The
marks keep their own code points. The box is a plain cross.

### The digits

A digit stands at 0.85 of the body, on the line: a stem with one full stroke,
or two for 12 to 15. A stroke is a limb running out from the stem at 60°, a
level bar from or across it, or a shallow cut across it at 30°, at the head,
the middle or the foot. 12 to 15 carry two strokes across the stem, so none of
them can be taken for a digit with one limb: a misread number is the costliest
error the hand can make. No letter is a lone stem with one stroke, and no digit is a Latin letter
or digit.

| Value | Stroke                              | Value | Stroke                                            |
| ----- | ----------------------------------- | ----- | ------------------------------------------------- |
| 0     | a bar across the middle             | 8     | a limb down forward from the head                 |
| 1     | a limb up back from the foot        | 9     | a bar across the foot                             |
| 2     | a limb up forward from the foot     | 10    | a shallow cut rising across the middle            |
| 3     | a limb down back from the middle    | 11    | a shallow cut falling across the middle           |
| 4     | a limb down forward from the middle | 12    | two shallow cuts rising across it                 |
| 5     | a bar back from the middle          | 13    | two shallow cuts falling across it                |
| 6     | a bar forward from the middle       | 14    | two bars across it                                |
| 7     | a bar forward from the head         | 15    | a rising and a falling cut crossing at the middle |

1, 4 and 8 keep the places of the carved tally's limbs.

### The specimen

`specimens/pirzath-hand/letters.png` holds every sign large, with the roman
that writes it and its number of pen movements; the sixteen digits together at
display size, 48 and 24 px; every sign at 48 and 24 px after _xhn_ in
Liberation Mono; the sample texts written through the `pirzath` encoding
beside the same text in Liberation Mono and in Pirzath Carved, all at one font
size; and the first word forms of the Khazari note at 48 and 24 px.

## Layer 3: the font

`tools/pirzath-hand/build_ufo.py` writes `sources/PirzathHand.ufo` from the
signs, and `build.sh` compiles it to `fonts/PirzathHand-Regular.ttf` and
`.woff2`:

```sh
.venv/bin/python tools/pirzath-hand/build_ufo.py
PATH=.venv/bin:$PATH ./build.sh
```

The UFO is generated: an edit belongs in the strokes or the signs, and the
generator is run after it. The outlines are fitted with cubic curves by Teng
Chou's `fit.py`, and fontmake writes them as TrueType quadratics.

### The glyphs

Every character of the Pirzath block that the hand draws keeps its code point
and its glyph name: the letters, the digraph letters, the vowel pairs, the
sixteen digits, the points and the length mark. Beside them stand the five
long vowels (`aacute` to `uacute`) and the thirty-one doubled consonants
(`p_p`, `t_h_t_h`), which have no code point; the space; the two empty glyphs
of the default-ignorables; `.notdef`, the hand's plain cross; and
`notdef.box`, a copy of it that takes every Latin and punctuation code point.

### The features

| Feature | What it does                                                         |
| ------- | -------------------------------------------------------------------- |
| `ccmp`  | Turns the default-ignorables' empty glyph into a second one.         |
| `liga`  | Draws a vowel and the length mark after it as the long vowel.        |
| `rlig`  | Draws a consonant written twice as its doubled sign.                 |
| `mark`  | Sets a length mark left on a vowel pair over the middle of the pair. |

There is no `ss01`, no joined form and no kerning.

### The metrics

- **The body stands at Latin's cap height,** 0.73 em, so `tools/vertical.py`
  measures the hand's consonants against the shared cap height and its
  vowels against the shared x-height. The OS/2 cap height is the median height of
  the consonants that stand from the line to the body, 730, and the x-height
  that of the vowels _a e i u_, 460.
- **The line metrics are the shared ones,** ascender 945, descender −200 and
  line gap 100, with USE_TYPO_METRICS set. No glyph's ink leaves the band, and
  the Windows ascent and descent are 945 and 250.
- **Spacing.** Every glyph with ink and an advance stands at its ink with 70
  units of white either side; the length mark has no advance; the notdef and the
  box keep their own width; and the word space is half an em, 500.
  `tools/spacing.py` holds the hand to its own limits for a face set open on
  purpose: a median blank share of at most 30% and a mean gap of at most
  0.15 em, with the shared largest gap of 0.22 em.

### The checks

- `tools/pirzath-hand/check_font.py` confirms the character map by the carved
  face's rules, Latin text on the box, the outlines of every mapped glyph, the
  long vowels and doubled consonants, the empty ignorables, the zero-advance
  length mark, the name table, the line metrics, the spacing of every glyph, and
  that no `ss01`, joined form or kerning is present.
- `tools/pirzath-hand/guard.py` writes every Khazari lexicon form and the
  fixtures through the `pirzath` encoding, shapes them, and asserts the
  glyph sequence and the length mark's seat over a pair.
- `tools/prove_guards.py` proves the guard fails the font without its GSUB
  table, and the font check fails it without its GPOS table.

### The specimen

`tools/pirzath-hand/font_sheets.py` renders `specimens/pirzath-hand/text.png`
from the built font: Khazari words at display size and the Khazari texts at 48,
24 and 20 px, each after its roman spelling in Liberation Mono at the same size,
with the shared x-height and cap height ruled across both. The chart, the README
sample and the specimen page, `specimens/hl-pirzath-hand.md`, are written by
the build.

```sh
.venv/bin/python tools/pirzath-hand/font_sheets.py
```
