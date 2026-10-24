# Qalezu Hand — design notes

The everyday alphabet of the Khelathi of thalorna: signs written fast with a reed on papyrus, one sign for each consonant. It is written right to left, draws no vowel except at the start of a word, and is written from the setting's roman spelling by thalorna's `qalezu` mapping note, not by the font.

## The reed nib

Every stroke is a centreline swept by one broad reed nib: a thin rounded slab 99 units long and 14 thick on a 1000-unit em, held at 30 degrees from the horizontal. A pull straight across the nib's edge is the full width; a pull along the edge is a hairline. The contrast of the script is that, and nothing else: thick where the pen moves across its edge, a hair where it moves along it. The ends and the thin crossings are rounded by the nib's own radius, never cusped.

A sign stands on the line in a body 495 units tall, with the dab above it and the doubling bar below. Each sign is entered from the right, because the pen travels right to left. Signs stand apart, with no joining and no contextual forms; the reed-cursive look is the stroke contrast and the entry flick. The spacing is the advance each sign carries: its ink width with 28 units of white a side, the font's spacing rule (see `design/making-fonts.md`). A doubled sign and a catch-before form take their sign's advance, so the bar or the dabs may reach a little into that white.

## The signs

Each sign descends from the temple script's picture-sign for a word that begins with the sound; the scribes kept the picture's first consonant and reduced the picture to what a reed draws fast. The pictures are drawn from the setting's own river, harvest, tax and barge world.

| Sign     | Sound            | Ancestor picture                                   | Reduction                                                             |
| -------- | ---------------- | -------------------------------------------------- | --------------------------------------------------------------------- |
| l        | l                | plumb-line with its bob                            | a vertical pull ending in a small hook                                |
| r        | r                | punting pole with a forked foot                    | a slant pull ending in two prongs                                     |
| t        | t                | grain scoop                                        | a shallow bowl and a short rising handle                              |
| d        | d                | the scoop heaped                                   | t plus a dab                                                          |
| z        | z                | furled sail's tuck                                 | s plus a dab                                                          |
| s        | s                | sail on its spar                                   | a long low pull with one diagonal tuck                                |
| g        | g                | the sickle with its sheaf                          | k plus a dab                                                          |
| k        | k                | sickle                                             | a hooked crescent open to the left                                    |
| n        | n                | net float on its cord                              | a small loop on a low pull                                            |
| th       | th               | mooring post with a rope turn                      | an upright with one slanted wrap                                      |
| m        | m                | weigh-beam on its post                             | a broad shallow peak over a short upright                             |
| q        | q                | surveyor's peg with its cord                       | a short upright, looped head, trailing cord to the right              |
| kh       | kh               | flood-gauge staff                                  | an upright with three nicks on the left                               |
| gh       | gh               | the gauge with its float                           | kh plus a dab                                                         |
| h        | h                | smoke over a hearth                                | a rising wisp over a flat base                                        |
| sh       | sh               | papyrus umbel                                      | a stem under a cap that curls both ways                               |
| p        | p                | papyrus raft                                       | a flat base with upturned ends                                        |
| b        | b                | the raft loaded                                    | p plus a dab                                                          |
| f        | f                | winnowing fan                                      | a swelling arc with a short stem                                      |
| w        | w                | well bucket on its hook                            | a hanging bowl under a short cap                                      |
| y        | y                | fish leister with one barb                         | a stem with one barb on the right                                     |
| catch    | the glottal stop | the cut of a reed pen                              | a short slanted nick above the line                                   |
| tj       | tj, ch           | the t scoop with the umbel's stem rising out of it | t and sh drawn as one sign                                            |
| doubling | gemination       | the scribe's under-stroke                          | a short bar written under the sign and typed as one character with it |

The doubling bar is the 24th sign of the alphabet, drawn as part of the doubled sign (below). `tj` is the one fused sign. `ch` and `tj` are two spellings of it.

## The voicing dab

A voiced sign is its voiceless partner plus one reed dab over it: p and b, t and d, k and g, s and z, kh and gh. The dab is a mark of its own with no code point. Each voiced glyph is built as a composite of the voiceless glyph and the dab, so a voiced sign cannot be typed apart from its pair, and the dab sits at the same place over each partner.

## The doubled signs

A consonant written twice, as in _Lenni_ or _Gerra_, is one character: the doubled sign, the sign with the doubling bar drawn under it. Every consonant sign has a doubled form, `<sign>.dbl`, on a code point of its own; the catch has none, and neither does it have a catch-before form. A doubled digraph (_tth_, _thth_) is the digraph's doubled sign.

The doubled glyph is a composite of the sign and the unencoded `doubling` component, set at the sign's `doubling` anchor, a fixed distance below its lowest ink. The doubled glyph has the sign's advance. The bar has no code point, no positioning feature and no role in shaping, so every shaper draws a doubled sign the same way. `doubling`, `dab` and `catchdots` are components only; none can be typed.

## The catch and the vowel rule

Qalezu records no vowel. A vowel at the start of a word, which in Khelathi is marked by the glottal stop, draws the catch; every other vowel draws nothing. A word starts at the beginning of the text and after a space, a hyphen or any mark. A hyphen in the Latin spelling is a word space, since Qalezu has no sign for it: _Gar-Qethar_ and _Khelathi-zethu_ are each two words, _Gar-Au_ is g, r, a space and the standalone catch, and a hyphen at the end of a prefix form (_Gar-_, _Lut-_) writes nothing. A vowel after a letter, another vowel or the apostrophe is silent. The apostrophe is the catch wherever it stands.

**A catch before a consonant is three reed dabs over that consonant.** The three dabs stand in a triangle, one on top and two below, apart from one another and never touching. The consonant is the next sign after the catch, with the silent vowels between them skipped. The text stores the catch and the consonant as two characters, and the font draws them as one glyph, the consonant's catch-before form, the way an Arabic font draws its ligatures. On a voiced sign the triangle stands clearly above the voicing dab, so the plain sign (no dab), the voiced sign (one dab) and the catch-before form (three dabs) differ at body-text sizes.

**A catch with no consonant after it is the standalone catch,** the sign of its own: at the end of a word, before a mark, before another catch, or in a word with no consonant. The standalone catch is never combined with a following catch.

Examples, each in reading order:

| Latin         | Written                                                                                      |
| ------------- | -------------------------------------------------------------------------------------------- |
| _Uqa'a_       | the triangle over q, then the standalone catch                                               |
| _Au'Khelathu_ | the standalone catch (the first catch meets another catch), the triangle over kh, then l, th |
| _Qe'aret_     | q, the triangle over r, t                                                                    |
| _Anlagh_      | the triangle over n, then l, gh                                                              |
| _Lem'_        | l, m, the standalone catch                                                                   |
| _Au_          | the standalone catch                                                                         |
| _'nna_        | the triangle over the doubled n                                                              |

A doubled consonant keeps its doubling bar under the sign; a catch before it puts the triangle over the doubled sign, whose bar stays below.

The font draws each code point as its sign, and a catch followed by a consonant sign or a doubled sign as that sign's catch-before form. Two identical consonant signs stay two signs: a doubled consonant is a character of its own, written only where the spelling doubles the consonant, so a consonant, a silent vowel and the same consonant (_zelalgit_) is two signs. Which vowels vanish, which letters are one sign and where a consonant is doubled is the spelling, which thalorna's `qalezu` mapping note writes; the fixtures are in `tools/qalezu-hand/fixtures.json`.

## Right to left

The script is written right to left and has no case and no quotation marks. Its code points are unassigned in Unicode and default to the right-to-left bidirectional class, so browsers, Foundry and Typst lay a run of them out right to left, mix them with English and wrap them without a control character. A block of lines takes a right-to-left container (`dir="rtl"` in HTML, right-to-left text direction in Typst) to be right-aligned.

Numerals run right to left with the script, most significant digit first in the text, so the largest place is at the right.

No sign needs mark positioning. HarfBuzz, and so Chrome, Foundry and Typst, shapes these code points in visual order, because they belong to no script: a run is reversed before shaping. The substitution that fuses a catch with its sign therefore reads the sign first and the catch after it.

## The encoding

`tools/qalezu-hand/encoding.json` is the one table: for each character its glyph name, its code point in U+1EA00–U+1EA3F, its sound and the roman spelling of it, and under `forms` each catch-before form. The signs run from U+1EA00 (the catch is U+1EA15 and `tj` U+1EA16), their doubled forms from U+1EA17, the digits from U+1EA2D and punctuation from U+1EA37 through U+1EA39; the remaining code points in the block are free. Each doubled entry names its sign in a `base` field.

The catch-before forms have no code point. The 22 consonant signs' forms are listed in sign order, and their doubled signs' forms follow; each entry's `base` names the sign or doubled sign it carries the triangle over. The space stays U+0020. Everything else reads the table: `tools/qalezu-hand/apply_encoding.py` writes the UFO's character map, the composites and the `rlig` substitution that draws a catch and its sign as the form, `check_font.py` compares the built cmap with it and shapes each catch and sign, and `guard.py` takes the glyph of each code point and each form from it. Every Latin character, the apostrophe included, maps to the box, so stray text prints boxes.

## The catch-before forms

Each consonant sign and each doubled sign has a catch-before form, `<sign>.catch` or `<sign>.dbl.catch`: the sign (or doubled sign) plus the unencoded `catchdots` component, set at the sign's `catch` anchor. `catchdots` is three `dab` components in a triangle, and the `catch` anchor sits a fixed distance above the sign's highest ink, above the voicing dab on a voiced sign. The glyph has the sign's own advance. The font's ascender, descender and Windows ascent and descent enclose every glyph, so no catch-before form or doubling bar is clipped; the box guard checks it for every font. Like the doubled signs they are precomposed glyphs rather than a positioned mark, because Chrome attaches a positioned mark to the wrong base on script-less right-to-left code points.

## The ignorables

The controls that browsers and Typst insert around right-to-left runs (U+200B–U+200F, U+202A–U+202E, U+2066–U+2069 and U+FEFF) draw nothing. They map to an empty glyph with zero advance, and a `ccmp` single substitution turns that glyph into a second empty one. A cmap entry alone is not enough: HarfBuzz replaces a default-ignorable character that the font maps directly with the space glyph, and leaves a glyph a lookup has substituted.

## The numerals

Base ten, place order, ten independent signs from the counting-house tradition, each standing lower than a letter: the empty pan (0), the tally (1), the cord (2), the knotted cord (3), the sealed bundle (4), the hanging stone (5), the full pan (6), the heap (7), the two stones (8) and the tied sack (9). A date in the Qet Telgu count is the digits and the letters _s_ and _t_.

## The punctuation

| Mark  | Role          | Shape                                                |
| ----- | ------------- | ---------------------------------------------------- |
| `.`   | sentence end  | a short stroke on the line, hooking down at its end  |
| `·`   | verse end     | a heavy reed-formed dot high in the character space  |
| `,`   | pause         | a short low dash                                     |
| space | word division | 200 units, a gap several times the gap between signs |

The low sentence-end stroke and the high verse-end dot are separate punctuation. Roman spelling uses U+00B7 MIDDLE DOT (`·`) for the verse end; a physical line break alone does not add it. There is no hyphen, exclamation mark, question mark, semicolon, colon or quotation mark. A hyphen between the parts of a name is written as the space between two words.

## Building and checking

The UFO `sources/QalezuHand.ufo` is the source. A generator outside this repository drew the outlines and wrote the `catchdots` component and the `catch` anchors; `apply_encoding.py` then derives the doubled and catch-before composites and the substitution that draws the catch-before forms. The UFO is the source that is edited and built, and the generator is not part of the build.

```sh
PATH=.venv/bin:$PATH ./build.sh                          # fonts/QalezuHand-Regular.ttf and .woff2
.venv/bin/python tools/qalezu-hand/apply_encoding.py --check  # the UFO's code points follow encoding.json
.venv/bin/python tools/qalezu-hand/check_font.py
.venv/bin/python tools/qalezu-hand/specimens.py               # specimens/qalezu-hand/*.png
.venv/bin/python tools/qalezu-hand/guard.py                   # needs ~/dev/HeroicLands/thalorna; or --fixtures-only
.venv/bin/python tools/prove_guards.py
```

- `check_font.py` confirms the cmap is `encoding.json` plus the box, which takes every code point of the Latin ranges that the encoding leaves free to the box, that every sign shaped alone is its glyph and every catch shaped before a sign is that sign's catch-before form, that every glyph has an outline, that the bar, dab and catchdots components have zero advance, that every doubled glyph is its sign with the bar drawn in at the sign's advance, that every catch-before glyph is its sign with three more dabs drawn above it at the sign's advance, and that the font carries no mark positioning, that the default-ignorables shape to zero advance and no ink, and that the name table carries the licence.
- `guard.py` writes every form of the Khelathi lexicon, the `words` forms and the `names`, through thalorna's `qalezu` mapping note, shapes the result right to left and asserts no glyph is `.notdef` or the box and that the glyphs are the signs of the code points the mapping wrote, each catch fused with the sign after it. It reports every form that holds a character the mapping does not write (`c` outside `ch`, `x`). Fixtures cover the word-initial vowel, the apostrophe, each digraph, `ch` and `tj` giving one sign, doubled consonants and doubled digraphs, a number and a word-final vowel, and the catch before a consonant, before a doubled consonant, before another catch, at the end of a word and across a mark.
- `prove_guards.py` removes the th sign from the built font's character map, and the GSUB table from the built font, and the guard fails on each; `check_font.py` fails on the font without GSUB too.
