# Vedyakshara — design notes

The Vedyakshara is the script of the Vedyari in thalorna: a syllabary of
consonant-plus-vowel signs, every sign hanging from a headline, so a line of
Vedyari looks like a rope with the words strung beneath it. The classical hand
is the one the temple scribe is trained in, and writes scripture, legal codes,
land grants, registers and the published calendar.

The face is _Vedyakshara Classical_ (`vedyakshara-classical`), on code points
from U+F0400. It writes 29 base signs, 22 consonants and 7 vowels, and 19 fused
clusters: no long-vowel signs, no vowel _r_, and _f_ written as _pa_ with the
soft dot. The full inventory is on fonts issue 13.

The font is built in layers, each generated from data and approved on its own
sheet before the next is drawn: the pen strokes, then the signs, then the font.
This note covers layer 1, the pen strokes, layer 2, the signs, and layer 3, the
font, Vedyakshara Classical.

## The rulings

- **Left to right.**
- **A Brahmic sibling of Devanagari at a glance, never a copy.** The likeness
  lives in the page texture: a headline every sign hangs from, unbroken across a
  word and broken by a space; vertical stems hanging from it; vowel signs above
  and below; half forms; the bare final marked on the sign itself. The bowls,
  arcs and joins are Vedyakshara's own, and so is the weight: the rope is the
  heaviest stroke, not a light rule over heavy stems.
- **The body stands at the shared x-height.** The hanging part of a sign, from
  the line to the underside of the headline, is 0.5135 em, the x-height of
  `tools/vertical.py`; the headline sits just above it. The line metrics are
  the shared ones, and the Windows ascent and descent cover the flags above and
  the hooks below.
- **The pen is a square-cut reed at about 75°, upright**, the headline the
  heaviest stroke, and the vertical stems are kept.
- **The bodies are broad and round**, as wide as three quarters of their height
  and more, as a Brahmic page sets them under the rope.
- **No repha.** An _r_ before a consonant is an ordinary half form, and the space
  above the headline belongs to the front vowels.
- **The digits are drawn with the same reed.**

## The pen

**A broad reed cut square, its edge held steep at 75° to the line, upright.**

- **The weight is in the rope.** A level pull runs across the edge and is the
  fullest stroke the reed makes, so the headline is the heaviest stroke on the
  page. An upright pull runs nearly along the edge and is a firm thin line, so
  the stems hang light beneath the rope. A body's floors and shoulders, and
  every diagonal falling against the edge, swell between the two.
- **The cut shows.** The reed is cut square, its corners barely softened, so a
  stroke that ends on the reed ends in a crisp edge at the reed's angle: the
  ends of a word's rope stand at 75°, leaning forward, and a stem's foot is
  cut on the same slope.
- **A reed hardly flexes.** The rope is written at full pressure and the
  bodies at `BODY_P`, a lighter hand, which shortens the edge a little; the
  difference is what keeps a body's floor below the rope's weight.
- **Upright, with no slant.** The classical hand is set, not run.

This pen is distinct from every other face in the repository: Semaron Kuriale's
broad nib and Qalezu Hand's reed sit at 30°, Veldikko's qalam at 62° and right
to left, and Teng Chou is brushed.

## How a stroke is drawn

`tools/vedyakshara/strokes.py` is the generator. A stroke is one or more
_tracks_: a path the reed follows, sampled every four units, with a _pressure_
at every sample. At each sample the reed leaves a flat footprint, its edge held
at the reed's angle and its length set by the pressure; a negative pressure is
the reed lifting. The outline is the union of the convex hulls of neighbouring
footprints, unioned again with `skia-pathops` into clean contours.

**The frame.** A skeleton is written with `f` running rightward, the way the pen
travels, and `y` up; the hand is upright, so `to_page` changes nothing while the
slant is zero. A stroke's origin is the left end of the headline it hangs from,
at the line: its `f` is the sign's left edge.

**Strokes fuse into the rope.** A hanging stroke sets down `OVERLAP` units inside
the headline, so a stem, a bowl or a cut and the rope above it are one shape.

**Drawn at the font's size.** The generator works in font units on a 1000-unit
em with the body already at the shared x-height, so the font takes the outlines
unscaled.

### Metrics

Units are thousandths of the em, the line at 0.

| Constant  | Value | What it governs                                                             |
| --------- | ----- | --------------------------------------------------------------------------- |
| `X`       | 514   | The underside of the headline: the body's height, the shared x-height.      |
| `HEAD_W`  | 79    | The headline's weight, measured from the reed: a level pull at full.        |
| `HEAD`    | 593   | The top of the headline, `X + HEAD_W`.                                      |
| `RAIL`    | 605   | The foot of a flag, sunk into the top of the headline.                      |
| `FLAG`    | 800   | The head of a front-vowel flag.                                             |
| `HOOK`    | −230  | The foot of a back-vowel hook and the r-foot.                               |
| `OVERLAP` | 14    | How far a hanging stroke starts inside the headline.                        |
| `BODY_P`  | 0.55  | The pressure the bodies and marks are written at; the rope is written at 1. |

A stem measures 38 units across, half the rope. The flags stay inside the
shared ascent of 945; the hooks and the r-foot reach past the shared
descent of 200, which the Windows descent covers.

| Style  | Reed edge | Reed thickness | Edge angle | Flex | Corner softness | Slant |
| ------ | --------- | -------------- | ---------- | ---- | --------------- | ----- |
| `HAND` | 78        | 22             | 75°        | 0.30 | 0.22            | 0°    |

### Using the generator

```python
import strokes as S

rope = S.shape("headline", 0, 0, w=400)      # the rope over a sign 400 wide
bowl = S.shape("bowl", 44, 0, w=300)          # a bowl hung from it, one sidebearing in
stem = S.shape("stem", 350, 0)                # a stem hung at its right
path = S.outline(rope.tracks + bowl.tracks + stem.tracks)   # a pathops.Path, font units, y up
S.contours(path)                              # polygons
```

`STROKES[id].params` gives each parameter's minimum, default and maximum, and
`shape` refuses a value outside them, naming the stroke, the parameter and the
range. `tools/vedyakshara/specimens.py` renders `specimens/vedyakshara/strokes.png`:

```sh
.venv/bin/python tools/vedyakshara/specimens.py
```

## The stroke inventory

Fifteen strokes in four kinds. Lengths are font units; `h` and `depth` are shares
of the body.

| Id         | Kind  | Skeleton                                                                                          | Fullest at                       | Permitted                                   |
| ---------- | ----- | ------------------------------------------------------------------------------------------------- | -------------------------------- | ------------------------------------------- |
| `headline` | rope  | one level pull along the top of the body, its underside on the x-height, square-cut at both ends  | everywhere: the heaviest stroke  | w 120–900, sag 0–12                         |
| `tick`     | rope  | the final form: the headline running past the stem and turning down and forward at full pressure  | the rope, and half that the tick | w 160–700, drop 120–280                     |
| `stem`     | body  | an upright fall hanging from the headline to the line, ending square or kicked forward            | nowhere: a firm thin line        | depth 0.5–1.25, foot 0–1                    |
| `bowl`     | body  | from under the headline, down the left side, a floor, up the right side and back to the rope      | the floor and the shoulders      | w 200–550, h 0.45–1, close 0.6–1            |
| `arc`      | body  | an open curve from the headline down one side to a floor, open toward one side, turning up it     | the floor                        | w 150–450, h 0.45–1, side −1 or 1, turn 0–1 |
| `cut`      | body  | the half-form cut: a short spur falling from the rope and ending in a level heel pulled forward   | the heel                         | depth 0.25–0.7, lean 0–0.6, heel 0–1.5      |
| `lobe`     | body  | a bowl hung from a stem: from the stem, round back to a floor and return to the stem              | the floor                        | w 150–400, top 0.3–1, bottom 0–0.6          |
| `rung`     | body  | a level pull ending at a stem, inside or below a body                                             | everywhere: near the rope        | w 80–450, at 0.2–0.8                        |
| `rstem`    | body  | the stem a fused _r_ rides: to the line and on down and back below it; or a tail from a floor     | the sweep below the line         | reach 0.6–1.4, top 0–1                      |
| `breath`   | mark  | _kh_, _gh_, _bh_: from the stem, a pull out to the right rolling down and back into an open hook  | the roll                         | size 0.7–1.3, at 0.4–0.8                    |
| `flag`     | mark  | _i_, _e_: a short stroke rising forward from the top of the headline, its head turned forward     | the rise                         | h 140–240, lean 0–120, curl 0–1             |
| `hook`     | mark  | _u_, _o_: a short fall from the body's foot below the line, its end turned aside and up           | the bend                         | d 160–260, turn 0–1, side −1 or 1           |
| `rfoot`    | mark  | _r_ after a consonant: a short stroke from the body's foot, down and back to the left             | the whole stroke                 | l 100–200, angle −150 to −100               |
| `dot`      | mark  | _f_, the soft dot: the reed set down and turned in place, inside a body's counter                 | the dot                          | size 0.7–1.4                                |
| `bar`      | point | a short upright length of rope standing alone on the line, with none, one or two knots tied in it | the knots                        | h 0.7–1, knots 0–2                          |

- **The headline spans the sign's whole advance**, so the signs of a word meet in
  one rope. The body keeps the face's sidebearing inside it.
- **A half form ends on the cut.** Its body stops early on the `cut` spur, without
  its closing stroke, and the rope runs on unbroken into the next sign. The spur
  ends in a level heel, which carries the reed's full width and so reads at 20 px.
- **A bare final ends on the tick.** The sign's own headline runs past its stem
  and turns down and forward at full pressure; nothing is set beneath the sign.
  Falling across the edge, the tick keeps about half the rope's weight.
- **The vowel places.** A flag stands on the headline over the sign's right end
  for _i_ and over its middle for _e_; a hook hangs below the body at the right
  for _u_ and at the middle for _o_. The r-foot takes the body's foot on the
  left, so the hooks keep the middle and the right.

## The specimen

`specimens/vedyakshara/strokes.png` holds:

- every stroke large, against the line, the x-height, the headline's top, the
  flag head and the hook foot, a body or mark shown on its rope or stem in grey;
- every stroke at 24 and 48 px to the em, after _xhn_ in Liberation Mono at the
  same size;
- seven rough sign skeletons hanging from a headline at display size: a bowl
  and stem, an arc and stem with the _i_ flag, a short bowl and stem with the _u_
  hook, a half form running into a sign with the r-foot, the final form, a bowl
  with the soft dot, the _o_ hook and the _e_ flag, and an open arc beside a
  stem kicked forward at its foot;
- one skeleton drawn over its own track, the track a red line under the ink;
- the skeletons run on as words at 48, 24 and 20 px, after a line of Liberation
  Mono at the same size, with the shared x-height ruled across both.

The skeletons test how the strokes sit together. They are not signs of the
script.

**What the sheet shows.** The rope reads as the heaviest stroke at every size,
and at 24 and 20 px a run of words reads as a line of rope with forms hanging
from it. The bodies stand at the shared x-height, the rope above it, so a Vedyakshara
word is as tall as the Latin beside it at the body and taller by the rope. The
stems hold as continuous lines at 24 px.

## Layer 2: the signs

`tools/vedyakshara/letters.py` builds every sign from the strokes, and
`tools/vedyakshara/letter_sheets.py` renders `specimens/vedyakshara/letters.png`:

```sh
.venv/bin/python tools/vedyakshara/letter_sheets.py
```

```python
import letters as L

L.sign("ka")                    # the full sign: a Glyph with tracks, advance and anchors
L.sign("ka", form="half")       # half, final or rfoot
L.sign("dra", vowel="i")        # any sign with a vowel sign: i e ai u o au
L.digit("7"), L.point(2)        # a digit; the bar with two knots
L.write("Ganoka-shalda")        # romanized Vedyari set as one run, for specimens
```

### The inventory

**Forty-eight signs: 29 base signs and 19 fused clusters.** The base signs are the
22 consonants _k kh g gh ng ch j ny t d n p b bh m y r l v sh s h_ and the 7
independent vowels _a i u e o ai au_. _f_ is _pa_ with the soft dot, and is not
counted.

**The fused clusters are the 19 commonest consonant pairs** of the Vedyari note,
counted by `tools/vedyakshara/census.py` over the words, affixes, names,
elements and Vedyari register entries, with the vowel _r_ written _ri_:

| Sign   | Count | Sign   | Count | Sign   | Count | Sign   | Count |
| ------ | ----- | ------ | ----- | ------ | ----- | ------ | ----- |
| _nda_  | 51    | _rta_  | 19    | _dya_  | 13    | _rma_  | 11    |
| _dra_  | 34    | _rsha_ | 15    | _gra_  | 13    | _shra_ | 11    |
| _tra_  | 27    | _vra_  | 14    | _nta_  | 12    | _tka_  | 10    |
| _ksha_ | 25    | _rna_  | 14    | _shta_ | 12    | _rka_  | 10    |
| _pra_  | 23    | _sta_  | 14    | _mra_  | 12    |        |       |

Four pairs tie at 10 for the last two places: _tk_, _rk_, _dv_ and _shv_. The tie
is broken by the lexicon's own words, the vocabulary the names are built from,
where _tk_ stands in 10 words, _rk_ in 8, _dv_ in 4 and _shv_ in 3.

### How a sign is built

A consonant is a **body** and a **right part**. The body is one of ten hanging
shapes; the right part is a stem hanging from the rope at the body's right, a
stem with a rung reaching back into the body, or nothing. The rope runs over
the whole advance.

| Body       | Shape                                                 | Width |
| ---------- | ----------------------------------------------------- | ----- |
| `full`     | a closed bowl the full height of the body             | 375   |
| `open`     | the full bowl left open at its top right              | 375   |
| `short`    | a closed bowl in the upper half                       | 330   |
| `c`        | an arc open to the right, the full height             | 300   |
| `c-short`  | an arc open to the right, in the upper half           | 280   |
| `c-left`   | an arc open to the left, the full height              | 290   |
| `lobe`     | a bowl hung from the stem in the lower body           | 300   |
| `s`        | a bowl in the upper half over an arc open to the left | 330   |
| `twin`     | two small bowls side by side in the upper half        | 420   |
| `two-arcs` | an arc open right beside an arc open left             | 420   |

| Body       | Stem        | Stem and rung | Nothing     |
| ---------- | ----------- | ------------- | ----------- |
| `full`     | _ka_, _kha_ | _ma_          |             |
| `open`     |             |               | _pa_ (_fa_) |
| `short`    | _cha_       | vowel _e_     | _va_        |
| `c`        | _ga_, _gha_ | _nga_         | _ha_        |
| `c-short`  | _na_        | vowel _o_     | _ra_        |
| `c-left`   | _ta_        | _sha_         | _da_        |
| `lobe`     | _ja_        | vowel _i_     |             |
| `s`        | _ya_        | _sa_          | _la_        |
| `twin`     | _ba_, _bha_ | _nya_         | vowel _a_   |
| `two-arcs` |             |               | vowel _u_   |

- **The breath curl** stands on the stem of _ka_, _ga_ and _ba_ to make _kha_,
  _gha_ and _bha_, in the same place on each. Its hook stays open, so at text
  size it reads as a curl and not a dot.
- **_ai_ and _au_** are _e_ with the _i_ flag and _o_ with the _u_ hook.
- **_fa_** is _pa_ with the soft dot in its counter.

### The forms

Every consonant and every fused sign has four forms, each a rule over the build:

- **Full.** The body, the right part and the rope over the whole advance.
- **Half.** The right part goes and the cut stands where the stem stood; a sign
  with no right part keeps its body and ends on the cut at its right edge. The
  rope runs to the cut and on into the next sign.
- **Final.** The rope runs past the stem and turns down in the tick.
- **R-foot.** The r-foot stands at the body's foot on the left, or, where the
  body does not reach the line, at the stem's foot. A fused C + r sign carries its
  _r_ already and has no r-foot form; `sign` refuses one.

### The fused signs

Four rules draw the nineteen:

- **C + r** (_dra tra pra vra gra mra shra_): the r rides the stem, which sweeps
  on down and back below the line. A first sign with no stem of its own takes the
  r as a tail from its body's floor, so _dra_ and _tra_ stay apart.
- **r + C** (_rta rsha rna rma rka_): a small _ra_ is tucked under the rope at the
  left of the second sign.
- **Side by side** (_ksha sta dya_): the first body, narrowed to three quarters,
  runs straight into the full second sign with no cut between. Each of these
  pairs has a two-part body, which stacked at half height closes up at text
  size.
- **Every other pair** (_nda shta nta tka_): the first body stands over the
  second, both at half height, on the second sign's right part.

### The vowel signs and the digits

The vowel signs stand on anchors every sign carries: the _i_ flag over its right
end and the _e_ flag over its middle; the _u_ hook under its right and the _o_
hook under its middle, hung from the lowest ink of the body above it.

The digits stand free of the rope on the line, as tall as the body, written with
the same reed: _0_, _shonya_, a hollow lozenge on its point, _1_ a stem with its head turned back and its
foot kicked forward, _2_ a c over a level foot, _3_ two c's one over the other,
_4_ a level head on two legs, the left one short, _5_ a level head drawn back
into a floor and a rise turned in, _6_ a ring in the upper body with a stem
falling from its left, _7_ a level head and a stem falling from its left end,
_8_ an arch on two legs with the feet turned out, _9_ a stem with two level
strokes reaching back from it, at the head and the middle.

### The specimen

`specimens/vedyakshara/letters.png` holds every consonant, _fa_ and every fused
sign in its forms (four, or three for a fused C + r sign); the independent vowels; _ka_ with each vowel sign and
the vowel signs on other signs; the digits and the bars; every sign at 48 and 24
px after Liberation Mono; fifteen words and four sample phrases from the Vedyari
note at display size, compounds solid; and the same at 48, 24 and 20 px after
their roman spelling. The specimen splits the roman spelling itself; the font
and its rules are layer 3.

## Layer 3: the font

`tools/vedyakshara/build_ufo.py` writes `sources/VedyaksharaClassical.ufo` from the
signs, and `build.sh` compiles it to `fonts/VedyaksharaClassical-Regular.ttf` and
its `.woff2`:

```sh
.venv/bin/python tools/vedyakshara/build_ufo.py
PATH=.venv/bin:$PATH ./build.sh
```

### The encoding

`tools/vedyakshara/encoding.json` is the one table of the code points, U+F0400 to
U+F04FF, left to right. One code point stands for each character of the script:

| Code points     | Characters                                                         |
| --------------- | ------------------------------------------------------------------ |
| U+F0400–U+F0415 | the 22 consonants, _ka_ to _ha_, in the order the chart is recited |
| U+F0420–U+F0426 | the 7 independent vowels, _a i u e o ai au_                        |
| U+F0430–U+F0435 | the vowel signs, _i e ai u o au_                                   |
| U+F0438         | the cut: the consonant before it has no vowel                      |
| U+F0439         | the soft dot: _pa_ softened to _f_                                 |
| U+F0440–U+F0449 | the digits 0 to 9                                                  |
| U+F0450–U+F0451 | the bars: the pause, with one knot, and the full stop, with two    |

The fused signs and the half, final and r-foot forms are not characters. Text holds
the consonants with the cut between them, as Devanagari text does, and the font
draws the forms. `encoding.json` lists the fused signs under `fused`, with the two
consonants each is drawn from. The character names are in `tools/names/vedyakshara.json`.

### The shaping

`rclt` draws the forms, in this order:

1. _pa_ and the soft dot are _fa_.
2. A consonant, the cut and a consonant that make a fused pair are the fused sign.
   The rule reads left to right, so the leftmost pair fuses: _ndr_ is the fused
   _nd_ with the r-foot.
3. _ra_ with the cut is its half form before a consonant and its final form
   otherwise, so an _r_ that starts a cluster never takes the r-foot.
4. A sign, the cut and _ra_ are the sign's r-foot form. A consonant whose pair with
   _r_ is fused never meets this rule, and so has no r-foot form.
5. A sign with the cut is its half form before a consonant,
6. and its final form anywhere else: at the end of a word, or before a space,
   a bar or a digit.
7. After a sign, _ai_ is the _e_ and _i_ flags and _au_ the _o_ and _u_ hooks, and
   each hook takes the neck that reaches the lowest ink of the body above it. The
   necks run in steps of ten units.
8. A vowel sign, the cut or the soft dot after anything that cannot carry it, a
   space, a bar, a digit or an independent vowel, is the box. Standing first in a
   run, with nothing before it, it draws as itself, so a chart shows every sign.

`mark` places each flag and hook by mark-to-base attachment on its sign's anchors:
the _i_ flag over the right end, the _e_ flag over the middle, the _u_ hook under
the right end and the _o_ hook under the middle. The script runs left to right, so
a mark follows its sign in the run and attaches to it directly.

### The metrics

The signs are drawn at the font's size: the body hangs from the underside of the
headline at the shared x-height, so the font takes the outlines unscaled. The
digits stand free of the headline on the line, exactly as tall as the body, and
are the face's typical x-height letters in `tools/vertical.py`. The line metrics
are the shared ones, 945, −200 and 100, with USE_TYPO_METRICS set. The flags rise
inside the ascent; the hooks, the r-foot and a fused _r_ reach past the descent,
and the Windows descent covers them. Every sign's headline runs over its whole
advance, so the signs of a word meet in one rope and the word space, 320 units,
breaks it.

The outlines are fitted with Teng Chou's `fit.py`. Where a fitted curve would run
outside its polygon's box, as it can at a sharp joint of two strokes, the polygon
is kept as straight lines, sampled closely enough to read as curves at every size.

### Writing

A consonant carries _a_; another vowel after it is its vowel sign, a vowel at the
start of a word is its own sign, and the cut after a consonant takes its vowel away.
_pa_ with the soft dot is _fa_. The bar with one knot is the pause, and the bar with
two the full stop. Every character has a glyph code in `tools/codes/vedyakshara.json`:
`KA`, `SIGN_I`, `CUT`, `SOFT_DOT`, `PAUSE` and `STOP` among them. How Vedyari is
written in these characters belongs to thalorna.

### Building and checking

```sh
.venv/bin/python tools/vedyakshara/check_font.py
.venv/bin/python tools/vedyakshara/guard.py
.venv/bin/python tools/vedyakshara/font_sheets.py
```

- `check_font.py` checks the character map against the encoding, that every form
  exists and is reached by its rule, that every flag and hook stands on its
  sign's anchor and every hook's neck meets the body, and that a mark after a
  space is the box.
- `guard.py` writes every form of the Vedyari lexicon through the encoding and
  asserts the glyphs the font shapes it to, from an account of the rules above
  written in Python; its fixtures in `fixtures.json` hold real words and
  phrases, and two forms with letters the script does not write.
- `font_sheets.py` renders `specimens/vedyakshara/text.png`: Vedyari words and
  the sample phrases, shaped by HarfBuzz from the built font, at display size and
  at 48, 24 and 20 px after their roman spelling in Liberation Mono.
- `tools/prove_guards.py` proves the guard and the font check fail the font
  without GSUB, the font check without GPOS, and the vertical guard with the
  Windows metrics cut to the line box.
