# Pirzath Carved — design notes

The carved form of Pirzath, the script of the Khazari of thalorna: letters cut
by a graver in stone and metal. One font covers the plain and the monumental
cutting, because the characters are identical and the monumental variant only
cuts deeper.

## The stroke

Every glyph is a set of cuts, and a cut is one of two things a graver makes
cleanly: a **stroke**, a straight groove that is full width in the middle and
tapers to a point at either end where the tool enters and leaves the stone, and
a **drilled dot**, an octagon a little wider than a stroke. Strokes are united
into one outline per glyph, so overlapping cuts read as one carving.

No letter's cut runs along the line of text. The grain of the stone runs with
the seam an inscription follows, and a cut along it splits the stone, so every
stroke of a letter is vertical or diagonal, and the breath notch (below) is
scored across the arm it marks at a steep angle for the same reason. The one
deliberate exception is the sentence end: a short cut made along the grain,
the cut that closes a thought. The imperative doubles it.

Consonants stand in a box 520 wide by 700 tall at a stroke weight of 104 units
on a 1000-unit em; the cuts of the skeleton are the deep ones. Vowels are
scored small, 300 by 440 at a weight of 82, because carved Pirzath cuts the
three consonants of a skeleton larger than the vowels of the frame, and a
worn inscription is read from its skeleton first. The length mark is a drilled
dot in the headroom above the vowel it lengthens, so a long vowel is still
shorter than the consonants around it.

Each letter stands separate. Spacing is derived from the outlines: the build
measures each glyph's left and right profile in 25-unit bands and sets a kern
for every pair so that the closest approach of two inks is the same optical
gap, tightening by at most 110 units and loosening by at most 40. A small vowel
therefore tucks under the arm of a tall consonant without touching it, and a
word reads as one interlocking carving with its letters still apart.

## The letters

Three families of consonant share a **frame**, and inside a family two
modifiers recur: the **voiced** letter adds a pole, a short upright cut inside
the frame, and the **breathed** letter adds a notch, a short cut scored across
one arm.

| Frame                 | plain | voiced (pole)       | breathed (notch) | voiced and breathed |
| --------------------- | ----- | ------------------- | ---------------- | ------------------- |
| the tent, apex up     | p     | b                   | f                | v                   |
| the trough, apex down | t     | d                   | th               | dh                  |
| the point, apex ahead | k     | g (closed by a bar) | kh               | gh                  |

The nasals are the frame doubled: m is the tent twice (M), n the trough twice
(W). The sibilants are the two closed or crossing shapes, s a tall lozenge and
z a cross. The liquids are l, a long forward cut with a branch falling from its
middle, and r, the point turned to open forward, the one letter of the row that
does. h is the breath on its own: the notch that marks it on a consonant,
scored across a bare stem, the one letter that stands on a stave.

The vowels are scored lines: a is a forward cut, u a back cut, i an upright.
The two rare vowels are built, e a small tent and o a small lozenge. A long
vowel is the vowel with the drilled dot above it; the dot is a mark, not a
letter, and the vowel is never doubled.

A doubled consonant is the letter once with the **doubling mark**: a short
forward cut hung under the letter's centre, below the baseline. Below is where
nothing else of the script sits, so the mark cannot be taken for the length dot
over a vowel, the pole or the notch inside a letter, the dividing dot at mid
height or the sentence end along the grain; and a mark under the letter leaves
the letter's own cuts, which carry the skeleton, untouched. A doubled digraph
carries the same mark on the digraph's one letter.

Numerals are a stem with up to four tally limbs at fixed places: a limb high on
the forward side is worth 8, one lower on the forward side 4, one high on the
back side 2 and one low on the back side 1, so the sixteen signs are nought,
the bare stem, to fifteen, the stem with all four. A number is read in place
order, sixteens first.

The marks between words are in the carver's vocabulary and look nothing like
English punctuation. **Word division** is a drilled dot at mid height with room
either side, typed with the space key; it stands lower than the length mark,
which sits over a vowel. **The sentence end** is a short cut along the grain at
mid height, typed `.`. **The imperative** is two such cuts stacked at mid
height, typed `!`; Khazari verbs never change form, so writing is the only
place an imperative can show. **The pause** inside a sentence is a short back
cut at mid height, typed `,`; its slant keeps it apart from the sentence end,
and it slants the other way from the dash. **The dash** of a built name is a
short forward cut at mid height between the two parts. **A quotation** is
enclosed by two marks built on g, the way « » enclose: the opening mark is g
with two notches across its forward arm, the closing mark g with two notches
across its back arm, after the way gh is g with one notch across the back arm.
The closing mark differs from gh only by its second notch, so the pair stands
on the apex half of the arm, well apart, cut lighter than the breath notch, and
clear of the bar and the cap height. There is no interrogative mark, because a Khazari question ends in the
particle _zef_, which marks it, and there is no semicolon and no colon: the
`?`, `;` and `:` keys map to the box, so a stray mark shows on the page. Every character the typing does not use maps to the box, which is a copy of `.notdef`: a blank stele, a stem with a
drill mark either side.

## The seventeen lost letters

The full row is forty-one. Seventeen letters write sounds the old row had and
Khazari has lost, which the Pelwar tongues kept. Each fills an empty cell of
the system above, placed by its sound, in the same cuts, so it is a member of
the row and not an addition to it.

| Letter    | Where it sits           | The cut                                                                                                                          |
| --------- | ----------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| sh        | beside s                | the lozenge with the breath notch across its upper forward side                                                                  |
| zh        | beside z                | the cross with the breath notch across the lower half of its back arm                                                            |
| ts        | a stop released into s  | the K: a stem with two arms meeting at its middle, forward                                                                       |
| ch        | a stop released into sh | the mirrored K, its arms back                                                                                                    |
| j         | the voiced ch           | the Y: a stem from the baseline to mid height, with two arms rising from it to the corners of the cap, beside the K of ts and ch |
| q         | the deep stop           | the Y upside down: a stem from mid height to the cap, with two arms falling from it to the corners of the baseline               |
| ng        | with the nasals         | the point doubled, as m doubles the tent and n the trough                                                                        |
| ny        | with the nasals         | the doubled trough with the hanging pole                                                                                         |
| the catch | a throat letter         | the stem with the breath notch low, where h carries it high                                                                      |
| w         | a glide                 | the back cut of u at consonant size, with the pole through it                                                                    |
| y         | a glide                 | the forward cut of a at consonant size, with the pole through it                                                                 |
| hl        | with l                  | l with the breath notch across its long cut                                                                                      |
| ai, ei    | vowel pairs             | the first vowel with i joined as an upright                                                                                      |
| oi        | a vowel pair            | ei turned over: the small trough with i's upright rising from its apex                                                           |
| au, ou    | vowel pairs             | a and u joined into the small trough; o with the back cut of u through it                                                        |

Typing them is set out in the next section. The remaining empty cells are a bar closing a frame other than the point, a
notch on the other arm of a frame, and a pole from the opposite end.

## Typing the lost letters

Each of the seventeen is typed by its spelling, and the longest spelling wins.

| Glyph                      | Typed                          |
| -------------------------- | ------------------------------ |
| sh, zh, ch, ts, ng, ny, hl | the two letters, as a ligature |
| j, q, w                    | the letter                     |
| the catch                  | `'` or `’`                     |
| y (the glide)              | `y` before a vowel             |
| ai, au, ei, oi, ou         | the two vowels                 |

- **ngh is n and gh.** The four digraphs th, dh, kh and gh ligate before the
  lost ones, so _ngh_ shapes as `n` + `gh`, never `ng` + `h`; the lexicon's
  _zangh_ and _huzangh_ depend on it. _nngh_ is `n`, the doubling mark, `gh`.
- **y not before a vowel** is the spelling guide's vowel _y_, said _i_. It
  draws the `i` glyph, and after a vowel it forms the pair the guide reads
  alike: `ay` is `ai`, `ey` is `ei`, `oy` is `oi`; `uy` is `u` + `i`. This
  reading is the owner's to confirm. A final `y` is therefore never the glide.
- **Doubling** works as for the other consonants: `shsh` and `ssh` both draw
  `sh` and the mark, as `tth` draws `th` and the mark, and likewise `zzh`,
  `tts`, `nng`, `nny`, `hhl` and `cch`; `jj`, `qq`, `ww` and `''` double the
  single letters.
- **A long vowel pair** carries the length mark when an acute falls on either
  vowel: `aí` and `ái` both draw `ai` with the mark.
- **A lexicon form is unchanged.** No Khazari form contains a lost spelling,
  and the guard asserts the glyph sequence of every form against the Khazari
  alphabet alone.

## How Thuravark descends from it

Thuravark's twenty-eight staves, all straight, with no horizontal strokes and
no curves, are what a work-row cut down from this one for a Pelwar mouth would
keep. The frames collapse to a stave with branches: the tent and trough each
become a stave with two arms, the point a stave with one, so the three families
fold into one stem-and-branch pattern and the pole, the notch and the bar
become branches of the same kind. The breath notch on h is already a stave
with a branch. The sibilant cross and lozenge lose their closed sides and the
liquids straighten. The vowels, which Khazari scores small because they carry
only frame and no skeleton, are promoted to full staves, because Nordmal has no
skeleton to pick out and a Nordman's staves all stand equal; and with the
vowel at full size the length mark goes, and a long vowel is marked by doubling
the stave. The numerals' tally stem and limbs pass across unchanged. What is
lost is the depth of cut, the small vowels and the closed shapes; what is kept
is angle for angle and notch for notch.

## Typing it

The font draws Pirzath over the setting's Latin spelling. The four digraphs
_th_, _dh_, _kh_ and _gh_ are one glyph each by ligature. An acute vowel,
precomposed or as the vowel plus U+0301, is decomposed to the vowel and the
length mark, which mark positioning seats above it. A consonant typed twice,
_ll_, _mm_, _kk_, shapes to the letter and the doubling mark, and a doubled
digraph typed as the spelling writes it, _tth_, _ddh_, _kkh_, _ggh_, shapes to
the digraph's letter and the mark. Capitals draw the lowercase letter; the
script has no case. The digits `0` to `9` draw the numerals nought
to nine and `@ # $ % ^ &` draw ten to fifteen, so twenty-six is typed `1@` and
three hundred and nine is `135`; the letters a to f are always letters. The
letter c has no Pirzath form and draws the box. A quotation is typed with
`“ ”` or `« »` directly, with `<<` and `>>`, which ligate to the marks, or with
a straight `"`, which `calt` resolves: it opens at the start of the text or
after a space and closes anywhere else. A single `<` or `>` draws the box.

## The rounds

1. First build. The pipeline runs end to end. The texture is coherent and
   angular, but chevron-heavy because a and u are small chevrons; the long
   pointed tapers read as thorns at reading size; the nested-chevron breathed
   letters clog into a wedge at 36 px; h as one bare back cut is weak and
   rhymes with z; r's short zigzag reads as a curly S; the kerning tucks too
   far and the word space is too small, so words run together; the numeral
   notches crossing the stem are hard to count; headings overlap the display
   lines.
2. Vowels become scored lines (a forward, u back, i upright); strokes heavier
   with a shorter taper; the breath becomes a notch scored across one arm
   instead of a nested chevron; z becomes the cross, h a long back cut with a
   short one beside it, r three staggered cuts; numerals get one-sided tally
   limbs at four fixed places; kerning tightens less and the word gap widens;
   the specimen layout bugs are fixed.
3. The breath notch is lengthened to 380 units so th, dh, kh, gh, f and v
   read as themselves at reading size; r becomes the forward-open point; s
   becomes the tall lozenge, because two parallel cuts beside the vowel a's
   single cut made an ambiguous row of slashes; `.notdef` becomes the blank
   stele.
4. h becomes a stem with the breath notch scored across it, because h followed
   by u gave the place-frame prefix _hu-_ three back cuts in a row.
5. The notch on h is made diagonal; a notch scored perpendicular to a vertical
   stem is horizontal, and the script makes no horizontal cut.
6. The owner's rulings: numerals are typed directly, the digits for nought to
   nine and `@ # $ % ^ &` for ten to fifteen, with no markers and no hex
   letters, so a to f are always letters; quotation marks are added as two
   pairs of cuts leaning in toward the quoted words, with `calt` choosing the
   form of a straight quote by context. The texts specimen gains a record
   quoting an oath, typed once with straight quotes and once with curly ones.
7. The display sheet is sized to its longest line; it clipped the forge oath's
   third line and both quoted lines on the right.
8. The owner's rulings on the marks between words: the `?` key draws nothing,
   the sentence end is a short cut along the grain at mid height, and word
   division is a drilled dot at mid height; with the coordinator's imperative
   (two such cuts stacked) and pause (a short slanted cut), and `;` and `:`
   drawing nothing. The pause slants back, because a forward cut at mid height
   is already the dash of a built name.
9. The sentence end and the imperative lengthen from 200 to 260 units; at
   36 px a 200-unit cut is seven pixels and too slight beside the dividing
   dot.
10. The owner's ruling on doubling: a consonant written twice is the letter
    once with a doubling mark, and a doubled digraph the digraph's letter with
    the mark. The mark is a short forward cut hung under the letter, seated by
    mark positioning; the descender deepens to 250 to hold it. The texts
    specimen gains the mastery frame, and the paragraph four doubled words.
11. The doubling mark lengthens from 130 to 150 units, within the descender;
    at 36 px it was under five pixels tall.
12. The owner's ruling on quotation: the marks are g with two notches across
    the forward arm (opening) or the back arm (closing), typed `"`, `“ ”`,
    `« »`, `<<` and `>>`. Notches at 0.3 and 0.7 of the arm poke past the cap
    height and into the bar, so both marks read as a cluttered g.
13. The notches move to the apex half of the arm, 0.4 of its length apart,
    shorten to 280 units and thin to 84, so each clears the bar and the cap
    and the two resolve as a pair at 36 px beside gh's one centred notch. The
    texts specimen puts gh right before a closing quote from « » and shows
    `<<` `>>`; the chart shows gh beside a closing quote.
14. The owner's ruling on the lost seventeen: twelve consonants and five vowel
    pairs drawn into the empty cells by their sounds, shown on the chart by
    glyph name. The stop pole of ts and ch rises from the bottom vertex, since
    hanging from the top it crowded the hush notch.
15. ts and ch become the K and its mirror, a stem with two arms meeting at
    its middle; y and w take the pole through their middle, because a tall
    a or u told from the vowel by height alone fails at 36 px.

16. The lost seventeen are typed: ligatures for the two-letter spellings, the
    glide `y` before a vowel and the vowel `i` elsewhere, the vowel pairs read
    through a length mark, and doubling extended to every new consonant. A
    sixth specimen sheet shows them over their spellings.
17. The owner's rulings on j and q: j is the Y and q the Y upside down, with
    ts and ch the stem-and-arm family; their arms meet the stem exactly at mid
    height and run to the corners of the box, so neither is a numeral, whose
    full stem the limbs fall away from, and q is not the tent, whose apex is at
    the cap. The poles of w and y run from baseline to cap and the cuts take
    the vowels' own slant, because a pole stopped inside the cut vanished at
    36 px. oi becomes ei turned over, the small trough with the upright rising
    from its apex, because the upright inside the small lozenge was lost at
    vowel height.
18. The three cuts of j and q are driven past their junction, so their tapers
    are buried in one another's ink and each letter reads as one Y with a
    solid join and three free ends, where three cuts meeting point to point
    left a gap at mid height. w and y widen to a box 720 wide with the cut
    corner to corner, so the pole stands about 160 units clear of the cut at
    either end, where in the consonant box the two overlapped for most of
    their length and read as one mass.

## Checks

- `tools/pirzath/check_font.py` loads the built font, confirms every mapped code point
  names a glyph with an outline, checks that `?`, `;` and `:` map to the box, checks that the digits, `@ # $ % ^ &`,
  the quotation inputs (`"`, `“ ”`, `« »`, `[ ]` and `<<` `>>`), the space, `.`, `!`, `,`, `-` and a to f type
  what the rulings say, checks the name table and opens the `.woff2`.
- `tools/pirzath/guard.py` shapes every form in the `words` list of the Khazari language
  note on thalorna's `origin/main` and asserts the shaped glyph sequence is the
  one the spelling demands: no `.notdef`, each digraph one glyph, each acute
  vowel its vowel followed by the length mark, each doubled consonant or
  digraph the letter once with the doubling mark. A set of fixtures covers the
  numerals, a number beside words, the letters a to f, the quotation marks
  opening and closing from every input (`"`, `“ ”`, `« »`, `<<` `>>`) with gh
  right before the closing mark in each, the four marks between words, the
  three keys that draw nothing, every consonant and every digraph doubled, and
  four doubled lexicon words. A second set of fixtures types the seventeen
  lost letters initial, medial and final where each can occur, with _zangh_,
  _huzangh_, `ay`, `ey` and `oy`, `y` before a vowel and between consonants,
  both apostrophes, the pairs with an acute on either vowel and the doubled lost
  consonants. `tools/prove_guards.py` removes the GSUB table from the built font,
  which drops the ligature, decomposition, quotation and lost-letter features,
  and the guard fails on it.

## Source

The source of the font is the UFO `sources/PirzathCarved.ufo`: the outlines,
the character map, the metrics and `features.fea` with every OpenType feature.
The design is settled. The UFO is edited in a font editor and built with
`fontmake`.

## Building

```sh
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
PATH=.venv/bin:$PATH ./build.sh      # fonts/PirzathCarved-Regular.ttf and .woff2
.venv/bin/python tools/pirzath/specimens.py    # specimens/pirzath/*.png
.venv/bin/python tools/pirzath/check_font.py
.venv/bin/python tools/prove_guards.py
.venv/bin/python tools/pirzath/guard.py        # needs ~/dev/HeroicLands/thalorna, or --note FILE
```

## Showing the script

A handout, a shield device, a banner or a logo shows a whole word or a name in this script, never a single letter standing alone. Several letters, seen on their own, share their shape with runes that are used as hate symbols; inside a word they read as letters.

The sentence end is always the last mark of a sentence, outside a closing quotation mark or any other mark: _Galdan bunát, "Dalík bant, maríg bant"._ The imperative mark (`!` or `¡`) stands at the start of what it governs: before the first word of the sentence, or just inside the opening quotation mark when it governs only the quotation. It is not a sentence end, and the sentence still closes with the sentence-end cut.
