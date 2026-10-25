# Ch'alish P'ilam — design notes

The writing of the Ki'ich'chik city-states in thalorna. It has two hands, which
share their readings and are drawn in different ways: the **common hand**,
built from a small fixed set of strokes, and the **ceremonial hand**, in which
every sign is a picture of its own.

## The two hands

|              | Common hand                                                                                                     | Ceremonial hand                                                                                                                |
| ------------ | --------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| Construction | Strokes make components; components combine into signs, as Teng Chou's do                                       | Every sign an individual picture, as Khelathi Zethu Glyphs' are                                                                |
| The cell     | Square, and never drawn: the spacing implies it                                                                 | A grid of square blocks; a glyph fills a half, full or double footprint, in a cushion, a round cartouche or its own silhouette |
| Line         | One even line; weight never tells two signs apart                                                               | Meticulous, painted or carved; the picture is the point                                                                        |
| Writers      | Priests and scribes write it; miners and craftsmen know its numbers and the signs of their work                 | Priests and scribes                                                                                                            |
| Surfaces     | Chalk on a shaft wall or a slate, a point on a wooden palette, a stylus on bark paper, a pen or brush on vellum | Temple walls, monuments, pyramids, posts around a village common, painted codices                                              |

A scribe writing the common hand on vellum writes it as calligraphy, neat and
even. That is a finer version of the same signs, not a different set.

## Reading order

Glyphs are read in rows of two, left to right, down a column two cells wide;
then down the next column. Every common sign takes one advance, so a column two
advances wide wraps a run of signs into rows of two by ordinary line breaking,
and a page of such columns is set by the page, not by the font.

Neither hand marks sentences, pauses or speech. Ki'i'chek puts its verb last, so
the verb closes each clause, and speech is reported with words. Text runs on from
row to row and column to column without a break.

## The common hand

### Layer 1: the strokes

The common hand is drawn with one even line, 50 units on a 1000-unit em. A
cell stands 730 units, Latin's cap height, on the line, and every sign takes an
advance of 850 units: the cell and its gutter. The ink keeps 80 units clear of
the cell's edge.

The strokes are the stem, the bar, the slash, the fall, the corner, the tick,
the dot, the ring, the arc, the hook, the curl and the wave.
`tools/chalish-pilam/strokes.py` draws them, and
`tools/chalish-pilam/strokes_sheet.py` renders
`specimens/chalish-pilam/strokes.png`.

Numbers are written in bars and dots: a bar for each five, stacked from the
bottom, and a dot for each one above them.

### Layer 2: the glyphs

A glyph is a skeleton ideogram built from the strokes, filling a whole cell. **Keep
it simple**: a glyph is a few strokes, written fast in chalk, and carries nothing
beyond what tells it from its neighbours. A glyph is an ideograph, not a picture:
it need only evoke its concept, so MOUTH is a plain ring.

**Size.** A glyph's ink fills its cell, from the line to cap height, so a run of
glyphs stands as tall as Latin capitals beside it. Glyphs are drawn inside an 80-unit
margin and grown by 1.25 about the cell's centre (`GROW` in `glyphs.py`); the line
keeps its 50-unit width. The shell for zero, nothing, is the one small glyph: it
sits on the line and stands to Latin's x-height, as a small letter does. Each
glyph is a **concept**, the thing its picture shows, named by a Ki'i'chek word, and
has a **sound**: that word's opening consonant and vowel, its catch left out. Two
glyphs may share a sound.

**The core.** Twenty-four core glyphs carry the script, and nearly everyone knows
them:

| Category     | Glyphs                     |
| ------------ | -------------------------- |
| The cosmos   | SUN, MOON, SKY, STAR       |
| The world    | WATER, FIRE, EARTH, STONE  |
| Living       | MAN, WOMAN, PLANT, BEAST   |
| The quarters | EAST, WEST, NORTH, SOUTH   |
| Relations    | HIGH, LOW, INSIDE, OUTSIDE |
| Human life   | HOUSE, HAND, EYE, MOUTH    |

MAN is the unmarked person, and MAN with MAN is people.

**The quarters are two axes.** EAST and WEST are time: the sun's path across the day
and a life's path from birth to death. NORTH and SOUTH are the vertical axis of being:
NORTH is the zenith, the world above, the gods and the honoured dead, the noon sun at
its height; SOUTH is the nadir, the world below, _Ch'al Ts'umaq_ beneath every cenote,
the night sun's hidden journey and the soul's trials. Read in order, EAST, NORTH,
WEST, SOUTH is the whole round: the sun rises, stands at noon, sets and travels under
the world, as a soul is born, lives at its height, dies, passes the trials below and
is born again. Their drawings make one family: the sun rising and setting on the
horizon, and the sun at the top and at the foot of the cross of the quarters. Where
context calls for it, NORTH and SOUTH are also the plain directions. Many more glyphs lie beyond
the core, and literacy is a sliding scale: most people know the core and a few
glyphs of their trade, many know a good number of two-glyph compounds and a couple
of three-glyph ones, and scribes know the four- and five-glyph compounds, the
lesser-known glyphs and the sound of every glyph. Priests know fewer glyphs than
scribes, but all the sacred ones. Each glyph's tier, `core`, `general`, `sacred` or
`trade:<occupation>`, is recorded with it.

A word is written with one glyph, or with two or more that together make a concept
of their own: MAN with INSIDE is a kinsman, HOUSE with OUTSIDE a village, HAND with
EYE writing, MOUTH with SKY prayer. The first glyph is usually the head, and those
after it modify it, as Ki'i'chek puts adjectives after the noun; order matters, so
EAST with WEST is a lifetime and WEST with EAST rebirth. A run may group several
ways: MAN, HIGH, HOUSE is the elder of the household, a man of the great house, the
conventional compound for a patriarch, or a man on his roof. A glyph may also stand for its sound. Context decides how each glyph
is read and how many glyphs make a word, and a run may mean one thing by its
pictures and another by its sounds at once.

Text runs two glyphs to a row; rows are layout only, and a word may begin in either
cell and run on into the next row.

**Sounds.** Every syllable Ki'i'chek uses is written by at least one glyph. A glyph's
sound is usually the opening consonant and vowel of the word that names it, its catch
left out. No Ki'i'chek word opens on seventeen of the syllables (_la, ba, ta, le, me,
mi, yi, yu, tu, te, ya, ye, bi, lo, hi, he, be_), so the glyphs that write them carry
**traditional sounds**: the sounds of the first codex, which Ish'ilan Ch'alish
composed in the language of the stars. Nothing in a modern word gives them away;
scribes simply know them. `SYLLABLES` in `tools/chalish-pilam/glyphs.py` lists
the 63 syllables the lexicon uses, and the glyph sheet shows the glyphs that write
each. The seven syllables Ki'i'chek never uses (_cho, mo, bo, bu,
ho, yo_ and a bare _e_) have no glyph, and a scribe writes a foreign name with the
nearest sound.

**The script has no spelling.** It writes concepts. The roman transcription records
every spoken sound, so that a reader can say a word; the native script does not have
to. A name is written in sounds as Maya scribes wrote them: a closing consonant is
written with a syllable whose vowel is silent, usually an echo of the vowel before
it, so _Ch'akul_ is _cha-ku-lu_, and a catch is left to the reader.

**Meaning, not words.** A text records what happened or what was meant, not the
words said. Nobody is quoted exactly, and grammar is never written out. Endings such
as _-ok_ and _-bal_ are sounds, and a glyph may write one, but context usually
carries them instead. So a passage is composed from its meaning, never converted
from the roman word by word, and no encoding writes roman into this script.

**No diacritics.** A glyph is always drawn whole and the same. No mark is ever added
to a glyph or taken from it.

**Encoding.** Each glyph is one character. A compound is a sequence of glyphs, and
the font knows nothing of words: which glyphs write a word is the lexicon's to say.
The common hand's block is U+F3000 to U+F3FFF. The numbers sit at U+F3000: zero, the
shell, then 1 to 19 in bar and dot, then the places of the count at U+F3014 to
U+F3017, a diamond holding one bar for 20, two for 400, three for 8,000 and four for
160,000. A number is written as Ki'i'chek says it: three, 400, six, 20, five is
1,325. The 24 core glyphs take U+F3020 to U+F3037 in the
order of the table above. Every other glyph takes the next free code point in the
order it is added, so none is renumbered; a glyph removed keeps
its row in `tools/chalish-pilam/encoding.json`, marked `retired`, and its code point
is never reused.

### Layer 3: the font

Chalish Pilam Common is generated by `tools/chalish-pilam/build_ufo.py` into
`sources/ChalishPilamCommon.ufo`. Every glyph takes one advance, 850 units: the
730-unit cell and a 60-unit gutter each side. The space is one empty cell. Because
the advance never varies, a column two advances wide wraps a run into rows of two by
line breaking alone.

`tools/chalish-pilam/font_sheets.py` shapes a passage through the built font with
HarfBuzz and renders `specimens/chalish-pilam/text.png`: a night's entry at the
sighting stones, as the Faith of Ish'ilan Ch'alish keeps one every night.

`tools/chalish-pilam/glyphs.py` draws the glyphs and the pilot's words, and
`tools/chalish-pilam/glyphs_sheet.py` renders `specimens/chalish-pilam/glyphs.png`.

## The ceremonial hand

**One glyph, one whole concept.** Where the common hand composes a concept from two
or more glyphs, the ceremonial hand draws it as a single glyph: the patriarch, the
death of a man, the rising of the moon over the sacred peak are each one picture. A
block's prefix, superfix, fringe and beads are parts of that one glyph's picture, not
signs of their own.

**Two things at once.** In poetry above all, a scribe's art is to say two things at
once: one by a run's pictures, another by its sounds. No mapping can write that, and
none is kept: a passage in either hand is composed by its writer.

**Precomposed.** A ceremonial glyph is built from components the hand shares, the
heads, eyes, curls, beads, netting, fringes and affixes, but they are not laid over
one another. Each is moved, shifted and reshaped to work with the others as a single
unit: a prefix bends to follow its main sign's curve, a head narrows to leave room for
its headdress, two forms that meet share an outline. Recurring motifs are normal. A finished glyph works as a whole: one bespoke, complex
glyph, still visibly composed of its parts.

**A god is one glyph.** Each god of the pantheon has a single glyph of its own, in both
hands, and a god's glyph may be as complicated as it needs to be.

**Complex, and carvable.** A ceremonial glyph is not meant to be drawn quickly, and is
dense with detail. It is painted in codices and cut in stone, so every glyph must
survive a chisel:

- no line is finer than the detail brush;
- the white between two lines is at least as wide as a line, so a groove can be cut;
- no dot or feature is too small to raise or incise.

`tools/chalish-pilam/carving.py` checks the second rule on every glyph: it finds white
narrower than a groove that forms a channel, as opposed to the tip of a wedge where two
strokes meet at an angle, which every carving has.

**Footprints on the grid.** Inscriptions are laid out on a grid of square blocks,
read in paired columns, and every glyph occupies a footprint on it: a **full** block,
a **half** block (tall and narrow), or a **double** block (wide). In the font these are
three advances.

**Size.** A ceremonial block is a dense picture and wants more height than a letter, so
in the font it spans the whole line, from Latin's descender to its ascender: half again
the common hand's cap height (`FONT_SCALE` and `FONT_DROP` in `ceremonial.py`).

**Outlines.** A glyph's outline is one of three:

- a **cushion**, the rounded oblong most signs stand in;
- a **round cartouche**, kept for one class of sign, the days of the count;
- **its own silhouette**, for heads and animals: snout, jaw and crest are the outline,
  with no frame round them.

**Numbers stand free.** A number counting a sign is set before it as a half-width
coefficient, its dots stacked up the column and its bars upright, in no frame.

**A concept and its syllable signs.** Any ceremonial glyph may carry syllable signs, as
Maya glyphs carry phonetic complements, and a name is built this way. The house's emblem
is the concept glyph of the name's first element, its house name (a jaguar for the
house of Ish'bal, an eagle for Shak'nal). Syllable signs set round it give the rest of
the person's name, and a coefficient before it counts their descent with that name: the
third of the name, the fourth. All of it stands in one block.

**The syllabary.** The ceremonial hand has a syllabary of its own, laid out as consonant
against vowel. Each of the syllables Ki'i'chek uses is written by one or more signs, and
the signs are mostly shaped as affixes: flat oblongs to set above or below a main sign,
tall strips to set before or after it, and a few full signs and heads.

The syllabary is drawn in `tools/chalish-pilam/syllabary.py`: each sign is one motif,
the reduced picture of its source, fitted into a flat oblong three fifths of the block
wide and a third of it high, or a tall one the same turned on end. A picture lies along
its slot, stretched by up to 1.8. A narrow slot has room for fewer parallel strokes, so a
sign of legs, fingers or rays keeps two or three. `tools/chalish-pilam/syllabary_distinct.py`
checks that no two signs of different syllables look alike, and every form passes the
carving check.

**Composed blocks.** A name's syllables cannot be known ahead of time, so a block of a
concept glyph, its syllable signs and a coefficient is composed in the font from format
controls typed between the signs, as Khelathi Zethu Glyphs composes its quadrats. A
concept that is always written the same way stays one precomposed glyph.

**How a block is shared.** A main sign that shares its block takes its compact form, and
is squeezed to fill the room its affixes leave, as Maya scribes squeezed a sign rather
than shrinking it evenly, up to 1.6 times out of its own proportions. A flat affix takes
under a third of the block's height and a tall one under a third of its width. A
coefficient stands upright before the sign it counts. `tools/chalish-pilam/blocks.py`
lays a block out from its codage; the font's layout follows the same geometry, and the
carving check covers composed blocks as well as single glyphs.

**Interlocking stays inside a glyph.** A precomposed glyph may be built of parts that
wrap round one another; two separate glyphs never interlock.

**The canon.** The contour brush draws outlines and the main forms at about 4% of the
block, the detail brush everything inside at about 2.5%, and a slight seeded wobble
keeps any two strokes from being mechanically alike. Heads face the line's start, and
a head's outline is its profile: brow, nose, lips and chin. A kit of recurring parts
gives the hand its look: the comb fringe, rows of dots tracing an outline,
cross-hatched netting, beads, the ear spool, the X, curls, and prefixes and superfixes
grown from the sign they attach to. `tools/chalish-pilam/ceremonial.py` draws
the canon and the kit, and `tools/chalish-pilam/ceremonial_sheet.py` renders
`specimens/chalish-pilam/ceremonial.png`.

One ceremonial glyph means a concept by itself, and can also write a sound. Sounds
are not one to one: several ceremonial glyphs write the same sound, and a reader
must know which. A glyph may say one thing by its picture and another by its sound
at once. This is what makes the temple script inscrutable to anyone but the
priests and scribes trained in it.

The two hands are encoded separately: a ceremonial glyph has no one common glyph
that matches it, and the readings, not the code points, connect them.

Each sign is drawn individually inside its box, by the method of the Khelathi
temple hieroglyphs: a shared drawing canon and kits for heads, hands, figures
and beasts, and signs drawn in batches while looking at their renders.
Originality follows `design/making-fonts.md`: people and animals may follow
their real-world model closely; objects, symbols and religious emblems are the
setting's own; no sign copies a real glyph.

### The font

Chalish Pilam Ceremonial is generated by `tools/chalish-pilam/build_ceremonial_ufo.py`
into `sources/ChalishPilamCeremonial.ufo`, which `build.sh` compiles with the other
fonts; `tools/chalish-pilam/build_ceremonial.sh` regenerates the UFO and compiles it
alone. It is written on code points of its own, U+F4000 to U+F4FFF, from
`tools/chalish-pilam/ceremonial_encoding.json`: the numbers and the places of the count
from U+F4000, the concept glyphs from U+F4020, the syllable signs from U+F4400 and the
two joiners at U+F4FF0 and U+F4FF1. Zero and the places of the count have code points
and no ceremonial drawing, so they print the box. A glyph's advance is its footprint's
width and a 60-unit gutter each side.

Every main sign and syllable sign carries a form for each place it can take in a block,
named `<sign>.<role>` by `tools/chalish-pilam/ceremonial_layout.py`, which also writes
the GSUB lookups that pick them from the joiners. `tools/chalish-pilam/ceremonial_guard.py`
shapes blocks in every layout through the font and compares each with the block
`blocks.py` lays out; `carving.py`, `compact_sweep.py` and `compact_distinct.py` check
the drawings, and `syllabary_distinct.py` the syllable signs.

`tools/chalish-pilam/ceremonial_passage.py` writes a lord's seating in sixteen blocks
through the encoding, shapes it with HarfBuzz and renders
`specimens/chalish-pilam/ceremonial-passage.png` in paired columns.

## Codage

The roman transliteration writes how a word sounds, and it has no single writing in
either hand: one sound has many glyphs, and a glyph is chosen for its meaning. Text is
put into the script with a **codage**, a notation of ASCII codes in the manner of Zethu
Codage and the Manuel de Codage: one code names one glyph, so a sequence of codes always
gives the same glyphs, and the codage is what a Markdown note stores.

**Codes are names.** They are meant to be written and read back by people and by
language models, so they say what the glyph is:

| Writes                       | Code                               | Example                                               |
| ---------------------------- | ---------------------------------- | ----------------------------------------------------- |
| A concept glyph              | its name in capitals               | `SUN`, `MAN`, `HOUSE`, `PATRIARCH`, `SUN_AT_THE_EDGE` |
| A number                     | `n` and its value                  | `n13`, `n20`, `n400`                                  |
| A syllable sign (ceremonial) | the syllable and the sign's number | `ka1`, `ka2`, `la1`                                   |

Codes are separated by spaces, and carry no hyphen, since `-` ends a ceremonial block,
and no apostrophe. A space draws nothing in either hand, since neither has word spaces. The same name may write different glyphs in the two hands; each hand has a
map of its own.

**Blocks (ceremonial).** The ceremonial hand takes Zethu Codage's joiners, so one
convention serves both temple scripts:

| Typed | Means                                                                                                            |
| ----- | ---------------------------------------------------------------------------------------------------------------- |
| `-`   | the end of a block; the next code begins the next block                                                          |
| `:`   | stacks: what is before it stands over what follows, a superfix over its main sign or a main sign over its subfix |
| `*`   | sets side by side: a prefix before its main sign, or a postfix after it                                          |

A coefficient is the first item of its block. A block holds a main sign and at most two
affixes; anything more runs on into the following blocks. `n3*la1:JAGUAR-sho1*bi1` is a
name: the jaguar, the house emblem of Ish'bal, with its coefficient, three, and _la_ over it, then the
rest of the name in the next block. The font composes each block, and a main sign that
shares its block takes its compact form.

Each hand's codage is an encoding: `tools/chalish-pilam/codage.py` writes the common
hand's, `encodings/chalish-common.json`, from `encoding.json`, and
`tools/chalish-pilam/ceremonial_codage.py` writes the ceremonial hand's,
`encodings/chalish-ceremonial.json`, from `ceremonial_encoding.json`, and prints its rows
for thalorna's mapping note, so neither map drifts from its font. In both, a space writes
its invisible mark, and in the ceremonial hand `-` writes its own, so decoding gives the
codage back as typed.
