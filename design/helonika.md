# Helónika Book — design notes

The Helónika is the eastern alphabet of thalorna: the letters of theatre, verse
and the ledger in Helionis. Helonic, Bizarian and Bethuan are written in it, and
Valtari in the northern ports through the Helonic spelling. Its first face is the
**book hand**, _Helonika Book_: upright, evenly spaced and slow, the hand a
copyist uses for a page that will be read aloud.

The font is built in layers, each generated from data and approved on its own
sheet before the next is drawn: the pen strokes, then the letters, then the
font. This note covers layer 1, the pen strokes, layer 2, the letters, and layer 3, the font.

## The rulings

- **Twenty-four letters, cased.** Seven vowels, _a e ē i o ō u_, where _ē_ is
  spelled _ei_ and _ō_ is spelled _ou_; seventeen consonants, _b d f g h j k l m
  n p r s t th v z_. Bizarian and Bethuan add one _kh_ letter, and Bizarian a
  _zh_ letter. Each letter has a majuscule and a minuscule.
- **A Greek sibling at a glance, never a copy.** Six letters echo Greek, each
  writing the same sound as its Greek kin: _o_ (the round), _th_ (Θ), _ō_ (Ω),
  _p_ (Π), _d_ (Δ) and _l_ (Λ). Every other letter is the script's own: no
  letter takes the shape of a Greek letter that writes another sound, and no
  majuscule matches a Latin capital, the round excepted.
- **Left to right**, with spaces between words.
- **One accent mark**, for Bethuan pitch and Bizarian stress.
- **The raised dot ends a sentence.** Light pauses and the hyphen write nothing.
- **Ten digits of the script's own**, base ten.
- **The shared vertical standard**: the minuscule body at the shared x-height,
  0.5135 em, on the shared line metrics.

## The target

**Geometric capitals over a round book minuscule.** The majuscules are the civic
inscription brought onto the page, built from circle, triangle and gate: the
rounds (_o_, _th_, _ō_) are full circles nearly as wide as they are tall, the
gate and triangle letters (_p_, _d_, _l_) a little narrower, the stem letters
narrow. The minuscules are the reed's own letters, not shrunken capitals:
round-bowled, single-storey and open, few rising above the body and a good
number falling below it. That descending habit gives a Greek page its rhythm,
and it gives the Helónika its family look without borrowing a letter.

**Vertical stress.** The weight sits on the uprights and on the sides of the
rounds; the heads and feet of the rounds and every crossbar are hairlines. This
is the stress of a classical Greek book majuscule.

**Square cuts and small wedges.** Every stroke begins and ends with the reed's
own square cut. A hairline's free end finishes in a small wedge the reed makes
as it lifts, never in a hook or a curl.

**Readable aloud.** Counters stay open, no letter depends on a hairline alone
for its identity, and the face holds at 18 px.

**Nothing like Semaron.** Semaron Kuriale is a chancery hand slanted 12°,
written with a nib at 30° that puts the weight on the diagonals, built from
staves and an oval of 0.82 and set close. The Helónika stands upright, its nib
nearly flat, its bowls full circles, its letters set apart.

## The nib

**A broad reed cut square, its edge held nearly flat, at 10° to the line**, for
both cases. Weight follows the stroke's direction and nothing else; there is no
pressure. Three things follow:

- **Uprights are the fullest stroke.** A stroke pulled straight down runs across
  the edge and is about 81 units thick, the whole edge.
- **Level strokes are hairlines.** A stroke drawn along the line runs nearly
  along the edge and is about 26 units thick: the reed's thickness and the edge's
  10° rise. Uprights to crossbars is about 3 : 1.
- **Diagonals fall between, and the rising one is lighter.** A diagonal rising
  forward at 60° is about 69 units; one falling forward at 60° is about 79. A Δ
  or Λ is light on its left and full on its right.

The 10° also turns the rounds' stress a little: their thinnest points lie just
left of the head and just right of the foot, as a flat reed leaves them.

The reed is canon's tool: a Bethuan letter of credit is a sealed papyrus in
Bethuan letters.

## How a stroke is drawn

`tools/helonika/strokes.py` is the generator. A stroke is one or more _tracks_:
a path the reed follows, sampled every four units. At each sample the reed
leaves a flat footprint with slightly softened corners, its edge at 10°. The
outline is the union of the convex hulls of neighbouring footprints, unioned
again with `skia-pathops` into clean contours.

**The page frame.** The generator draws in font units on the page, left to
right, the line at 0, and at the face's own size: the minuscule body is 513
units, so no scale is applied afterwards. Unless a stroke says otherwise, its
origin is the left foot of its ink on the line.

**Ink edges, not centrelines.** A stroke's parameters name where its ink ends: a
stem with `top=513` has its ink at the x-height, and a round with `w=513` is 513
units wide in ink. The skeletons inset by the reed's half extents, `HALF_W`
(about 40, across) and `HALF_H` (about 13, up).

**The knob is the one manipulation.** A sample may shorten the edge that
touches the page, as the copyist does by letting only the reed's corner bear.
Only the `knob` does so: it is drawn a short way off the end of a hairline while
the edge shortens toward nothing, which leaves a small wedge. Every other stroke
is written with the whole edge.

### Metrics

Units are thousandths of the em, the line at 0.

| Constant   | Value | What it governs                                                     |
| ---------- | ----- | ------------------------------------------------------------------- |
| `X`        | 513   | The minuscule body: the shared x-height.                            |
| `CAP`      | 730   | The majuscules and the numerals: the shared cap height.             |
| `ASC`      | 600   | The head of an ascending minuscule, inside 1.2× the body.           |
| `DESC`     | −190  | The foot of a descending minuscule, inside the descent of 200.      |
| `OVER`     | 10    | How far a round passes the line and its height, to look as tall.    |
| `DOT_Y`    | 513   | The top of the raised dot.                                          |
| `ACCENT_Y` | 583   | The foot of the accent over a minuscule.                            |
| `BEARING`  | 30    | The white either side of a letter's ink: the hand is evenly spaced. |
| `SPACE`    | 200   | The word space, a real gap.                                         |
| `KNOB_IN`  | 14    | How far inside a hairline's ink end its knob is set.                |

| Reed       | Edge | Thickness | Edge angle | Upright | Level | Slant |
| ---------- | ---- | --------- | ---------- | ------- | ----- | ----- |
| `REED`     | 80   | 12        | 10°        | 81      | 26    | 0°    |
| `REED_MIN` | 67   | 11        | 10°        | 68      | 23    | 0°    |

The face takes the shared line metrics of `tools/vertical.py` unchanged: ascent
945, descent 200, line gap 100, window ascent 945 and window descent 250.

### Using the generator

```python
import strokes as S

stem = S.shape("stem", 40, 0, top=S.ASC)          # an upright, its centre at x = 40
arch = S.shape("arch", 40, 0)                     # the shoulder springing from it
path = S.outline(stem.tracks + arch.tracks)       # a pathops.Path, font units, y up
S.contours(path)                                  # polygons
S.weight(90)                                      # the thickness of an upright: about 81
```

`STROKES[id].params` gives each parameter's minimum, default and maximum, and
`shape` refuses a value outside them, naming the stroke, the parameter and the
range. `tools/helonika/sketches.py` sets strokes together into the rough letter
skeletons and the stroke tests, and draws each entry once, moving it into place
wherever it is set. `tools/helonika/specimens.py` renders
`specimens/helonika/strokes.png`:

```sh
.venv/bin/python tools/helonika/specimens.py
```

## The stroke inventory

Twenty-two strokes in ten kinds. Lengths are font units, and every length is the
ink's.

| Id          | Kind      | Skeleton                                                                                                                         | Fullest at                   | Permitted                                                                         |
| ----------- | --------- | -------------------------------------------------------------------------------------------------------------------------------- | ---------------------------- | --------------------------------------------------------------------------------- |
| `stem`      | stem      | an upright, set down square and pulled straight down to a square foot                                                            | all of it                    | top 120–730, foot 0–300                                                           |
| `descender` | descender | an upright carried below the line, ending square, turned back under itself, or turned forward, a knob on a turn                  | the upright                  | top 200–600, foot −190 to −80, tail 0–2, reach 0.5–1.6                            |
| `round`     | bowl      | a full round in two strokes from the head: the left side down to the foot, then the right side                                   | the sides                    | w 257–730, h 257–730, over 0–20                                                   |
| `arc`       | bowl      | part of the round, from a start angle through a sweep: the general bowl                                                          | where it runs upright        | w 205–730, h 205–730, start −180–360, sweep −360–360, over 0–20                   |
| `crescent`  | bowl      | a round left open on the right, written from the upper end round to the lower, a knob at each end                                | the back                     | w 257–730, h 257–730, open 60–160, over 0–20                                      |
| `hood`      | bowl      | a round left open at the foot, in two strokes from the head down each side                                                       | the sides                    | w 257–730, h 257–730, open 40–140, over 0–20                                      |
| `cup`       | bowl      | a half-round foot with its sides carried straight up, each side to its own height                                                | the sides                    | w 180–513, h 154–513, left 0.4–1, right 0.4–1, over 0–20                          |
| `arch`      | bowl      | a shoulder springing from inside a stem, over in a half-round and down a straight right leg                                      | the right leg                | w 231–462, h 257–730, spring 0.4–0.85, foot −190–0                                |
| `lobe`      | bowl      | a bowl closed against a stem: out from it at the head, round, and back into it at the foot, on either side                       | the far side                 | top 205–730, bottom −190–308, w 154–410, side −1 or 1                             |
| `diagonal`  | diagonal  | a straight diagonal across its box, rising or falling forward, its ends the reed's 10° cuts                                      | the falling one              | w 146–657, h 257–790, rise −1 or 1                                                |
| `bar`       | bar       | a level hairline, the reed drawn along its edge, bare or with a knob at one or both ends                                         | nowhere: the hairline        | w 100–730, at 0–730, knobs 0–2, tilt −8–8                                         |
| `beam`      | bar       | the gate's head: a hairline along the head of two stems and run past them, a knob dropping from each end                         | the knobs                    | w 219–730, at 513–730, overhang 0–80                                              |
| `neck`      | ascender  | a stroke rising back out of a bowl's head and turning forward over itself into a hairline and a knob                             | the climb                    | h 573–730, base 257–513, lean 0–1, curl 0.2–1                                     |
| `foot`      | terminal  | an exit: a stem's foot turned forward along the line and up into a hairline                                                      | the turn                     | reach 30–110, lift 20–80                                                          |
| `lead`      | terminal  | an entry: a short hairline flag drawn along the reed's edge into an upright's head                                               | nowhere: the hairline        | length 20–90, rise −40–20                                                         |
| `knob`      | terminal  | a hairline's finish: the reed's corner drawn a short way off the line and lifted, a small wedge, never a hook                    | the wedge's root             | size 0.6–1.4, drop −1 or 1, side −1 or 1                                          |
| `dot`       | point     | the raised dot: the reed set down and drawn down its own width, a square-shouldered point, its top at the body                   | all of it                    | size 0.6–1.2, at 308–553                                                          |
| `accent`    | mark      | the accent: one stroke rising forward from its foot                                                                              | even, lighter than a stem    | length 70–150, angle 40–75°, at 513–790                                           |
| `swing`     | curve     | a curved stroke between two points, bowed to one side, either end finished in a flourish: the minuscule's stem, diagonal and bar | where it runs upright        | dx −700–700, dy −900–900, bow −0.25–0.25, head and tail −240–240, r 25–90         |
| `hooked`    | curve     | the minuscule's stem: a small entry hairline rising into its head, a bowed fall, a foot turned into a tail                       | the fall                     | top 205–600, foot −190–257, bow −0.25–0.25, entry 0–120, tail −1, 0 or 1, r 30–90 |
| `flourish`  | terminal  | a free end carried on and turned into a hook by the reed, swelling where it runs upright                                         | the upright part of the turn | toward −180–360, turn −240–240, r 25–90                                           |
| `length`    | mark      | the length bar: a level hairline over a vowel with a knob hanging from each end                                                  | the knobs                    | w 100–260, at 543–790                                                             |

The round is written as a copyist writes an omicron, in two strokes from the
head, so its two halves meet at the head and the foot as hairlines. The `arc`
cuts any part of the same round, and the `crescent`, `hood` and `cup` are the
parts the letters use most, named so a letter reads as its strokes. A
capital's descender turn and free crossbar ends finish in a `knob`; a stem never
does, because its head and foot are the reed's square cut. The minuscule draws
its stems as `hooked`, its other strokes as a `swing`, and finishes its free ends
in a `flourish`.

## The specimen

`specimens/helonika/strokes.png` holds:

- every stroke large, with the line, the body, the ascender, the cap height and
  the descender as guides, the pen's entry marked green and its exit blue; a
  stroke that grows from another is shown beside it in grey;
- each stroke across its permitted ranges;
- every stroke at 24 px to the em;
- rough skeletons of the six letters that echo Greek, in both cases, and the
  raised dot;
- stroke tests: strokes set together to show how they sit, not letters of the
  script;
- the skeletons run on as lines at 48, 24 and 18 px;
- the minuscule skeletons beside Semaron Kuriale and Latin (Monaspace Neon) at
  one size, on one line, with the line and 0.5135 em ruled;
- three skeletons drawn over their own centrelines.

The skeletons are rough studies of the reed, the proportions and the terminals.
The letters themselves are set out in [Layer 2: the letters](#layer-2-the-letters).

**What the sheet shows.** The capitals read as an inscription: full rounds, a
gate with an overhanging beam, triangles light on the left and full on the
right. The minuscules stand on the shared x-height beside Semaron and Latin,
round where Semaron is oval and upright where it leans. At 24 and 18 px the
hairlines hold as continuous lines and the counters stay open; the wedges at
the hairline ends are below a pixel there, so the letters do not depend on them.

## Layer 2: the letters

`tools/helonika/letters.py` builds every sign from the stroke inventory, and
`tools/helonika/letter_sheets.py` renders `specimens/helonika/letters.png`:

```sh
.venv/bin/python tools/helonika/letter_sheets.py
```

Each sign is named as the font names its glyph: the capitals `A` to `Z`, `TH`,
`E.long` and `O.long` (the letters _ē_ and _ō_), `KH`, `ZH`, `A.macron`,
`I.macron` and `U.macron`; the minuscules by the same names in lower case; the
digits `num.0` to `num.9`; and `raisedDot`, `registerMark` and `accent`.
`L.glyph(name)` gives a sign's outline and ink extent, drawn once and only moved
into place wherever it is set, and `L.setting(names)` sets a run with `BEARING`
either side of each sign's ink.

### The rules

- **The capitals are the inscription; the minuscules are the pen.** A capital
  stands at `CAP`, built from straight strokes and rounds. The minuscules are a
  round book hand of their own on the body, `X`, and need not follow their
  capitals, as Greek α, γ, η, ν and ω differ from Α, Γ, Η, Ν and Ω. They are
  built from bowls, arches, cups and hooked stems; a stem is a curve set going by
  a small entry and ending in a turned tail (`hooked`), a gate is a hump arching
  from a stem (`arch`), and a free end turns into a `flourish`. The broad reed
  keeps its contrast: the bowls swell at their sides and the bars and tails run
  thin.
- **The minuscules are lighter.** They are written with `REED_MIN`, the same cut
  and angle with an edge a sixth narrower (67), so the running hand is lighter
  than the inscriptional capitals, and a word that opens with a capital opens on
  a heavier letter. The raised dot, the register-mark and the accent, which sit in
  running text, take the same reed; the digits take the capitals'.
- **The hand's signature: bars curl up.** Wherever a minuscule has a bar, its free
  ends turn upward: the head of _p_ carried past its right shoulder, the crosses
  of _f_, _t_ and _kh_, the arm of _h_ and the bars of _ē_ and _zh_. A Greek pen turns the
  same ends down, so _p_ beside _π_ reads as a sibling and never as the same
  letter. The one exception is _u_, whose rim tips curl down because they are
  tips, not bars.
- **A sibling, never a copy.** Only the six echoes resemble their Greek letters.
  Every other minuscule is checked against the Greek and Latin lowercase alphabets
  and resembles no Greek letter; where one comes near a Latin letter, the Latin
  letter writes the same sound.
- **Identified by the heavy strokes.** A letter is told apart by its stems, bowls
  and arches, never by a hairline alone, and every minuscule is distinct from every
  other at 18 and 24 px.
- **The capitals' families.** _G_ is _K_ with its two strokes rounded into a bowl;
  _KH_ is _K_ with a bar struck through its stem, and _ZH_ is _Z_ with a bar struck
  through; _Ē_ is _E_ with a bar to its back; _U_ is _Ō_ turned over; _J_ and _N_
  are the gate with one leg and both legs splayed; _B_ carries _R_'s bowl with a
  second bowl at its foot. The minuscule additions follow their letters: _kh_ is
  _k_ with a bar, _zh_ is _z_ with a bar, _ē_ is _e_ with a bar.
- **Nothing that misleads.** No capital is a Latin capital, the round excepted,
  and no letter takes the shape of a Greek letter that writes another sound.
  Where a capital is a Greek letter mirrored, _K_ and _R_, it writes the sound of
  the letter it mirrors.
- **The minuscules leave the body.** _d k kh l t th_ rise to the ascender, and
  _f g j z zh_ fall to the descender.
- **The long vowels** are _a_, _i_ and _u_ with the length bar over them, 40
  units above a capital and 60 above the body.

### The inventory

| Letter | Capital                                                                                     | Minuscule                                                                                                                                                                                                   |
| ------ | ------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| _a_    | a tripod: two strokes meeting at the head, a stem let fall from the meeting point           | a round bowl standing against a stem on its left, the stem set going by an entry and turned forward at its foot                                                                                             |
| _b_    | a stem with a bowl on the left at its head and a bowl on the right at its foot              | a bowed stem with a small bowl on the left at its head and a larger bowl on the right at its foot                                                                                                           |
| _d_    | **echo**: the triangle on a base                                                            | **echo**: a round with a neck rising from its head, turned down over the round in a flourish                                                                                                                |
| _e_    | the round open on the left                                                                  | the round open on the left, each end turned in on a flourish                                                                                                                                                |
| _ē_    | the _e_ with a bar from its open side to its back                                           | the _e_ with a bowed bar to its back, curled up at its free end                                                                                                                                             |
| _f_    | half a triangle: a stroke rising from the line to the head of a stem                        | a stem from the body's head to the descender, its head hooked forward and its foot turned back, crossed by a bar curled up at both ends                                                                     |
| _g_    | a stem on the right closing a bowl on the left                                              | a bowl closed against a stem on its right, the stem falling to the descender and turning back                                                                                                               |
| _h_    | a stem with a short bar on the right at its middle                                          | a hooked stem with an arm springing from its middle and curling up                                                                                                                                          |
| _i_    | a stem standing on a short base                                                             | a short hooked stem, its foot turned back                                                                                                                                                                   |
| _j_    | the gate with its left leg splayed outward                                                  | a hooked stem falling to the descender and turning back into a wide tail                                                                                                                                    |
| _k_    | a stem met at its middle by two strokes from the left, one from the head, one from the foot | a hooked ascender met at the body's middle by two curves from the left, their free ends curled                                                                                                              |
| _kh_   | the _k_ with a bar through its stem above the meeting point                                 | the _k_ with a bowed bar through its ascender, curled up at both ends                                                                                                                                       |
| _l_    | **echo**: two strokes meeting at the head, the short stopping inside the long               | **echo**: the long stroke swung from the ascender, hooked at the head and kicked forward at the foot, the short leg swung out                                                                               |
| _m_    | the gate on three legs                                                                      | a hooked stem with two humps arching from it and from each other, each foot turned forward                                                                                                                  |
| _n_    | the gate on two legs splayed outward                                                        | a bell: one arch from the line over the body and back to the line, each foot flicked outward                                                                                                                |
| _o_    | **echo**: the round                                                                         | **echo**: the round                                                                                                                                                                                         |
| _ō_    | **echo**: the round open at its foot on two feet                                            | **echo**: two cups round at the foot sharing a shorter middle, their outer heads turned in                                                                                                                  |
| _p_    | **echo**: the gate                                                                          | **echo**: the gate rounded: a hump between two legs, its head carried past the left leg as an entry and past the right shoulder in a curl turned up, the left foot turned back and the right turned outward |
| _r_    | a stem with a bowl on the left at its head                                                  | a hooked stem with a bowl on the left at its head, its foot turned into a tail                                                                                                                              |
| _s_    | the round struck through by a stroke falling from its upper left to its lower right         | the round struck through by a swung stroke                                                                                                                                                                  |
| _t_    | a stem crossed high by a bar                                                                | a hooked ascender crossed at the body's head by a bowed bar curled up at both ends                                                                                                                          |
| _th_   | **echo**: the round barred across                                                           | **echo**: a tall narrow round barred at its middle, rising to the ascender                                                                                                                                  |
| _u_    | the _Ō_ turned over: the round open at its head, a level foot turned outward from each end  | a single round cup open at its head, like an omega turned over, each rim tip flicked outward and curled down in a short turn of the reed                                                                    |
| _v_    | a round on the line carrying a stem up to the cap height                                    | two closed rounds side by side, sharing their meeting side                                                                                                                                                  |
| _z_    | a beam, a stroke falling from its right end, and a bowl open on the left                    | two bowls open on the left, the lower hanging to the descender, each free end on a flourish                                                                                                                 |
| _zh_   | the _z_ with a bar through it                                                               | the _z_ with a bowed bar through it, curled up at its free end                                                                                                                                              |

### Digits, points and marks

The digits stand at the cap height and are built from strokes no letter uses
alone: the diamond, the lone diagonal, the bracket and the open point.

| Digit | Sign                                                      |
| ----- | --------------------------------------------------------- |
| 0     | a diamond                                                 |
| 1     | one rising stroke on a short foot                         |
| 2     | a bracket open on the left                                |
| 3     | an angle: a base and a stroke rising from its left end    |
| 4     | a point turned to the left                                |
| 5     | a bracket open on the right: the 2 turned to face forward |
| 6     | a diamond carried on a short stem                         |
| 7     | two rising strokes side by side                           |
| 8     | two rounds side by side at the middle of the height       |
| 9     | a point turned to the right: the 4 turned to face forward |

- **The raised dot** is the `dot` stroke, its top at the body: the end of a
  sentence, and the strong pause.
- **The register-mark** is a short wave at body height, over and under, a knob at
  each end.
- **The accent** is the `accent` stroke. It takes no room of its own: the
  specimens set it over the middle of the sign before it.

### The specimen

`specimens/helonika/letters.png` holds:

- every capital, minuscule, digit and point large, each in a cell with the line,
  the body and, faintly, the ascender, the cap height and the descender, the six
  echoes tagged;
- each capital beside its minuscule at 72 px, and the digits and points;
- a Helonic line beside Semaron Kuriale and Latin (Monaspace Neon) at 48 and
  24 px, with the line and 0.5135 em ruled across all three;
- Helonic words from thalorna, large, each with its roman spelling and gloss;
- the same words run on as text at 48, 24 and 18 px.

`L.spell` writes the specimens' Helonic by the Helonic spelling: _th_ is one
letter, _ei_ is _ē_ and _ou_ is _ō_; the other aspirates are a stop and _h_;
_y_ and _w_ are _i_ and _u_; Helonic writes no accent; `.` `;` `:` are the raised
dot, and the comma, the dashes and the hyphen write nothing.

## Layer 3: the font

`tools/helonika/build_ufo.py` writes `sources/HelonikaBook.ufo` from the letters, and
`build.sh` compiles it to `fonts/HelonikaBook-Regular.ttf` and `.woff2`. The UFO is
generated: an edit belongs in the strokes or the letters, and the script is run after
it, before the build.

```sh
.venv/bin/python tools/helonika/build_ufo.py
```

### The characters

The face draws its own code points, U+F0300 to U+F03FF, and nothing else: a Latin
letter, digit or mark draws the box. `tools/helonika/encoding.json` is the one table
of them, and `tools/names/helonika.json` names them in Unicode's style.

| Range           | Characters                                                            |
| --------------- | --------------------------------------------------------------------- |
| U+F0300–U+F0317 | the capitals of the twenty-four letters, _Ē_, _Ō_ and _TH_ among them |
| U+F0318–U+F0319 | the capitals _KH_ and _ZH_                                            |
| U+F0320–U+F0322 | the long capitals _Ā_, _Ī_ and _Ū_                                    |
| U+F0330–U+F0347 | the small letters, in the same order                                  |
| U+F0348–U+F0349 | the small _kh_ and _zh_                                               |
| U+F0350–U+F0352 | the long small _ā_, _ī_ and _ū_                                       |
| U+F0360–U+F0369 | the digits 0 to 9                                                     |
| U+F0370–U+F0371 | the raised dot and the register-mark                                  |
| U+F0378         | the accent, a combining mark                                          |

The capitals and the digits are written with the book reed and the rest with the
lighter minuscule reed. Every advance is the ink with `BEARING` either side; the
word space is `SPACE`.

### The features

- **`ccmp`** empties the default-ignorables.
- **`rclt`** draws the accent as the box wherever it follows anything that is not a
  vowel: a consonant, a digit, a point, a space or another accent. Standing first in
  a run, with nothing before it, it is drawn as itself.
- **`mark`** sets the accent over the middle of the vowel before it: over a
  minuscule as drawn, over a capital raised by the difference between the cap
  height and the body, and over a long vowel raised again, clear of its length bar.
- **`kern`** takes the whole advance of a space that follows the raised dot directly,
  or past the invisible marks that `?`, `!` and `!!` add. The dot's advance already
  holds a word space with its ink centred, so the dot sits close to the next word
  while the text keeps the dot and one ordinary U+0020. It is a positioning rule on
  the space, not a substitution, so the glyphs are unchanged and the sequence
  decodes as written. A space anywhere else keeps `SPACE`.

The face substitutes nothing else: _ei_ written as two letters stays two letters, and
_th_ written as _t_ and _h_ stays _t_ and _h_.

### Metrics

The face is drawn at its own size. Its minuscules that stand on the body, _b e ē o s
u_, measure the shared x-height, and its straight capitals the shared cap height. A minuscule round passes the line and the body by 6 units (`MOVER`), less than a capital round's 10, so the body measures the x-height. Its
line metrics are the shared ones, 945, −200 and 100, with USE_TYPO_METRICS set. The
tails of _f_, _g_ and _j_ turn back just below the descent, and the Windows descent
of 250 holds them.

### Writing and typing

the `helonika` encoding (`encodings/helonika.json`) writes
Helonic's roman spelling in these characters, and Valtari's where it is written in
the Helónika. The Helónika has case, so the three encodings write a lowercase letter as its minuscule and a capital as its majuscule, with no mark for case; a pair such as _Th_ or _Ch_ is its first letter's majuscule, and an all-capital pair draws the two letters' majuscules. Every terminal, `.`, `?`, `!` and `!!`, draws the raised dot,
each after the first adding invisible marks so that decoding tells them apart. Helonic writes _kh_, _sh_ and _zh_ as two letters, no accent and no
length, so the _kh_ and _zh_ letters, the long vowels, the accent and the
register-mark are drawn for the recensions of Bizarian and Bethuan and reached from
their code points.

HL Helónika types by sound through the same note. The register-mark has a key of its
own, Option+Shift+R.

### Checks

- `tools/helonika/check_font.py` confirms the character map, the outlines, the
  accent over every vowel and the box after anything else, the ignorables, the name
  table and the `.woff2`.
- `tools/helonika/guard.py` writes every Helonic, Valtari, Bizarian and Bethuan lexicon
  form through its encoding, shapes it, and asserts the glyphs, with no notdef or
  box; `--note` takes language note files, so a pull request's own notes are checked;
  `tools/helonika/fixtures.json` holds a fixture for each spelling rule.
- `tools/prove_guards.py` proves the guard fails the font with the small letter _th_
  removed, and the font check fails it with its GSUB removed and with its GPOS
  removed.

### The specimen

`tools/helonika/font_sheets.py` renders `specimens/helonika/text.png`: Helonic
words from thalorna, written by the encoding and shaped by HarfBuzz from the
built font, at display size and at 48, 24 and 20 px beside their roman spelling in
Monaspace Neon, with the shared x-height ruled across both.
