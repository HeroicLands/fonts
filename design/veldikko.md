# Veldikko — design notes

The Veldikko, the starlight-hand, is the script of the Sinale in thalorna: a
flowing calligraphy in which writing a thing and making it are held to be one
act. The Sinale write their own language in it, and the Áelendi write theirs in
it, so the ancient texts of Élavendre are Áelendi in Veldikko.

The font is built in layers, each generated from data and approved on its own
sheet before the next is drawn: the pen strokes, then the letters, then the
joining, then the font. This note covers layer 1, the pen strokes, layer 2, the
letters and their marks, and layer 3, the joining and the font, Veldikko.

## The rulings

- **Featural, with vowel marks.** Each of the three places of articulation has
  its own family of letter shapes, and within a family the stop, the fricative
  and the nasal are one shape varied three ways. Vowels are marks above the
  consonant they follow, carrying length and pitch. The Sinale language note's
  encoding governs the letter inventory.
- **Right to left.** The pen travels leftward.
- **A blend of Tengwar and Arabic calligraphy, copying neither.** From Tengwar
  the hand takes its principles: letters built from a stem and bowls, arches
  standing on a floor, a strong baseline that comes from the letters
  themselves, grades shown by the stem, stems dropping below the line into
  hooked tails, a cursive z, and vowels written as small dots and dabs above.
  From Arabic calligraphy it takes the direction, the slant, the rhythm of tall
  arcing stems against wide bowls, long tails below the line, and the light,
  flowing, calligraphic pen. No letter reproduces a Tengwa or an Arabic letter;
  a chance resemblance of one shape is no defect, and taking a letter whole is.
- **No drawn baseline.** Letters stand on an implied line, made by the floors of
  their bowls and the feet of their stems. A hairline flows from most letters
  into the next, so a word reads as one connected shape, but nothing runs along
  the line from letter to letter.
- **Elegant, refined and firm.** The hand is laid on with a firm nib: clear
  hairlines that hold at text size, slender thick strokes, tapers that trail
  away to nothing, and generous space inside and between letters.
- **One face for both tongues.** The Sinale and the Áelendi write the same
  letters in one hand at one weight: the firm Áelendan nib, with the Sinale
  slant and full curls and flourishes. Áelendi's own letters are further glyphs of the same face, which
  Sinale text never uses. An ornate sacred hand is a stylistic variant over the
  same letters.

## The target

**A stem and a bowl that sweeps past it.** A letter is a slender stem and a
bowl lying forward of it. The bowl is wider than it is tall and does not hug its
stem: it comes in from behind the stem, so its floor crosses the stem's foot and
runs on forward along the line. The floors are the heaviest strokes on the page,
and together they make the line the letters stand on.

**Standing forms and hanging forms.** A bowl either stands on the line or hangs
from its stem, and each kind does its own work:

- **the standing forms** close on the line and make it. The lips' bowl closes on
  the line and opens toward its stem; the tongue-tip's form is round arches
  standing on a floor, like an _m_ with a line under it.
- **the hanging forms** are the same skeletons turned over. A heavy arch runs out
  from near the stem's head, curves down and round, and leaves the counter open
  at the foot. They give the line an upper rhythm, a row of arched heads above
  the floors, as Tengwar's arch-headed letters do. The back of the mouth's form
  hangs: an arch from the stem's head winding down into a spiral.

**Arches on a floor give the line its weight.** Arches standing on one long
floor put more ink on the line than any other letter, and their upright legs
set a beat along it. They belong to the commonest consonants, so a page is
anchored by them, and the standing forms outnumber the hanging ones on any page,
so the unseen line holds.

**Arcing stems, long tails.** Stems lean forward 12° and bow into a shallow arc,
so they read as drawn rather than ruled. A stem carried below the line runs out
into a tail, and the tails vary: a hook turning back and up like a _j_, its tip
curled; an ezh, a cursive _z_ hung from the line; or a long bowl swept forward
under the letter.

**Vine and water at the ends.** Where Tengwar ends a stem square, the Veldikko
ends every stroke in a curl or a taper:

- **the vine's growing tip**, a small curl turned forward at the head of every
  stem;
- **the seed, the curled leg and the spiral**, the three ways a bowl ends,
  standing or hanging;
- **the hook and the ezh**, the tails below the line;
- **lifted ends**, every tail and curl trailing away to nothing.

**Flow.** A touch runs from the end of one letter's floor, near the line, up
into the next letter where its own floor begins behind its stem, so the eye
travels from letter to letter along the bottom of a word. The touches are
hairlines, arched a little above the line, and they stop at each letter rather
than running on: a word reads as a connected shape and the line stays implied.

**A slow, careful pen.** The Veldikko is written slowly; a hurried hand is held
to be incorrect, as an off-note is. No stroke depends on speed for its shape,
and every terminal is set down from nothing, lifted to nothing, or wound into
the heart of a curl.

**Nothing like Semaron.** Semaron Kuriale is an upright chancery hand of stems
and straight branches, written left to right with a broad nib at 30°. The
Veldikko runs the other way, leans and arcs, builds its letters from bowls
rather than branches, ends every stroke in a curl, and weights the line.

## The nib

**A narrow, obliquely cut nib, held firmly.** It is a flat nib, as a qalam is,
cut so that its edge lies at 62° on the page when the hand travels leftward.
Three things follow:

- **The weight falls on the line.** A level stroke runs across the edge and is
  the fullest the pen makes, so the floor of every bowl is its heaviest part,
  and the floors together make the implied line. A stem runs nearly along the
  edge and is slender. A stroke falling forward, down and to the left, runs
  along the edge and is a hairline.
- **The nib is narrow.** At full pressure its edge is about a twentieth of the
  bowls' em, so the thick strokes are slender, and its thickness keeps the
  hairlines clear.
- **It flexes a little and lifts.** Pressure lengthens the edge; at none the edge
  is a little over half its full length. A tail that lifts off
  the page shrinks the footprint to nothing, so tapers trail away rather than
  stopping square.

The cut follows from the direction. Writing right to left with the pen in the
right hand, a scribe cuts the nib obliquely so the edge stands steep, which puts
the weight on the level strokes. A square-cut nib held at 30° to 45°, the cut of
a left-to-right hand, would weight the stems instead.

A pointed pen was weighed and set aside. It swells on the stroke pulled toward
the writer, which puts the weight on the stems: the opposite of the rhythm the
ruling asks for.

The hand leans 12°, and its curls, seeds, spirals and tails are drawn at full
size, so the firm nib carries the Sinale flourish.

## How a stroke is drawn

`tools/veldikko/strokes.py` is the generator. A stroke is one or more _tracks_:
a path the nib follows, sampled every four units, with a _pressure_ at every
sample. At each sample the nib leaves a flat footprint with softened corners,
its edge held at the nib's angle and its length set by the pressure; a negative
pressure is the pen lifting, and shrinks the footprint toward nothing. The
outline is the union of the convex hulls of neighbouring footprints, unioned
again with `skia-pathops` into clean contours.

**The forward frame.** Every skeleton is written with `f` running the way the
pen travels and `y` up; `to_page` turns `f` leftward and applies the slant. A
stem's origin is its foot on the line; a bowl's origin is the foot of the stem it
grows from, the bowl lying forward of it.

**The style is separate from the skeletons.** `Style` holds the nib, the slant,
the flourish (which scales the curls, seeds, spirals and tails) and an
overall pressure. `HAND` is the one style every text is written in, and the
ornate sacred hand is a second `Style` over the same stroke calls.

### Metrics

Units are thousandths of the em, the line at 0.

| Constant | Value | What it governs                           |
| -------- | ----- | ----------------------------------------- |
| `X`      | 270   | The height of a bowl above the line.      |
| `ASC`    | 680   | The head of a raised stem.                |
| `DESC`   | −280  | The foot of a lowered stem.               |
| `MARK`   | 400   | The floor of the vowel marks over a bowl. |
| `HANG`   | 310   | The height a hanging form hangs from.     |
| `BAR`    | −90   | The length bar's place beneath the line.  |
| `SPACE`  | 104   | The distance between the dots of a mark.  |
| `RISE`   | 840   | The head of the riser, _l_.               |

A level stem's head stands 60 units above the bowl, so even a fricative's stem
rises clear of its bowl.

| Style  | Nib edge | Nib thickness | Edge angle | Flex | Slant | Flourish |
| ------ | -------- | ------------- | ---------- | ---- | ----- | -------- |
| `HAND` | 54       | 11            | 62°        | 0.45 | 12°   | 1.0      |

These are the generator's units, in which a bowl stands 270 high; the font
scales them so the bowls stand at the shared x-height ([The font](#the-font)).

### Using the generator

```python
import strokes as S

stem = S.shape("stem", 0, 0, top=S.ASC)          # a raised stem, its foot at the origin
bowl = S.shape("arches", 0, 0)                    # the arches on a floor that grow from it
path = S.outline(stem.tracks + bowl.tracks, S.HAND)   # a pathops.Path, font units, y up
S.contours(path)                                  # polygons
```

`STROKES[id].params` gives each parameter's minimum, default and maximum, and
`shape` refuses a value outside them, naming the stroke, the parameter and the
range. `tools/veldikko/tests.py` sets strokes side by side into test sequences,
and `tools/veldikko/specimens.py` renders `specimens/veldikko/strokes.png`:

```sh
.venv/bin/python tools/veldikko/specimens.py
```

## The stroke inventory

Nineteen strokes in six kinds. Lengths are font units.

| Id            | Kind    | Skeleton                                                                                                                                   | Fullest at                             | Permitted                                                         |
| ------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------- | ----------------------------------------------------------------- |
| `stem`        | stem    | a curl turned forward at the head, a long fall bowed into a shallow arc; below the line, a hook, an ezh or a forward sweep                 | near the foot, and the floor of a tail | top 290–760, foot −340–0, arc −0.04–0.14, tail 0–2, reach 0.4–1.8 |
| `bud`         | bowl    | single, open toward the stem: in from behind the stem, a floor, up the far side, back over the top, down to a seed short of the stem       | the floor on the line                  | w 240–380, h 200–300, seed 0–1, sweep 0–1                         |
| `arches`      | bowl    | arches on a floor: in from behind the stem, one long floor, up the front, back over round arches on near-upright legs, the last curling in | the floor and the legs                 | w 260–480, h 220–300, n 1–3, curl 0–1                             |
| `coil`        | bowl    | a tendril: in from behind the stem, a floor, up the far side, back over the top, winding into a spiral that fills the counter              | the floor on the line                  | w 240–380, h 220–310, turn 0.5–1.4                                |
| `hung-bud`    | hanging | the bud turned over: a heavy arch from near the stem's head, down the far side, back under and up toward the stem, ending in a seed        | the arch at the top                    | as `bud`                                                          |
| `hung-arches` | hanging | the arches turned over: one heavy arch from near the stem's head with lobes hanging under it, open toward the line                         | the arch and the legs                  | as `arches`                                                       |
| `hung-coil`   | hanging | the coil turned over: a heavy arch from near the stem's head, down the far side and winding back up into a spiral                          | the arch at the top                    | as `coil`                                                         |
| `riser`       | letter  | one tall stroke with no bowl: an open tendril turned back over its head, a long fall bowed gently forward, a soft foot on the line         | the fall, and the foot on the line     | h 760–900, arc −0.02–0.10, curl 0.4–1.3                           |
| `crook`       | letter  | a crozier with no stem: a full foot on the line, a climb forward, a fern's head rolled back over                                           | the foot and the roll                  | w 150–240, h 220–330, roll 0–1                                    |
| `carrier`     | letter  | a short arcing stem with a curled head                                                                                                     | the fall                               | h 150–240, arc −0.04–0.14                                         |
| `touch`       | join    | a flowing hairline from one letter to the next, arched above the line or dipped toward it                                                  | nowhere: a faint swell                 | df 60–520, dy −160–160, sag −0.5–0.5                              |
| `bar`         | mark    | a short fallen leaf beneath the line, pointed at both ends                                                                                 | the middle                             | l 60–130, tilt −45 to −10                                         |
| `one`         | mark    | _a_: one dot                                                                                                                               | the dot                                | long 1–2, pitch −1–1                                              |
| `two`         | mark    | _o_: two dots side by side                                                                                                                 | the dots                               | long 1–2, pitch −1–1                                              |
| `three`       | mark    | _u_: three dots in a triangle standing on its point, two above and one below                                                               | the dots                               | long 1–2, pitch −1–1                                              |
| `dab`         | mark    | _e_: a long dab rising forward, pointed at both ends                                                                                       | the middle                             | long 1–2, pitch −1–1                                              |
| `backdab`     | mark    | _i_: a long dab lying nearly level, pointed at both ends                                                                                   | the middle                             | long 1–2, pitch −1–1                                              |
| `hook`        | mark    | _y_: a fall whose foot turns forward and up                                                                                                | the fall                               | long 1–2, pitch −1–1                                              |
| `curl`        | mark    | _ë_: a fall whose foot climbs back up into an open loop                                                                                    | the fall                               | long 1–2, pitch −1–1                                              |

The marks are sized for text: at 24 px to the em a dot is more than a pixel
across with a dot's width clear between neighbours, a dab is four pixels long, and
the hook and the curl are as wide as they are deep. A dot is the pen set down and
turned once in a tight circle, so it is round. Every vowel mark takes the same two parameters. `long` draws
the mark on into a hairline running forward from it, for a long vowel. `pitch`
adds a tail at its forward end: above zero a hairline flick upward for a rise,
below zero a fuller flick downward for a fall, and at zero no tail, for level
speech. In a cluster the most forward dot carries both.

## The plan for the letters

Layer 2 draws the letters from these strokes on this plan, and
[Layer 2: the letters](#layer-2-the-letters) sets out the inventory it gives.

**Three bowls, one per place of articulation.** Every consonant of a family is a
stem with that family's bowl:

| Place          | Consonants     | Bowl        | Its form                                                |
| -------------- | -------------- | ----------- | ------------------------------------------------------- |
| the lips       | _p_, _v_, _m_  | `bud`       | a single bowl, closed on the line, open toward the stem |
| the tongue-tip | _t_, _s_, _n_  | `arches`    | round arches standing on a floor                        |
| the back       | _k_, _h_, _ng_ | `hung-coil` | an arch hung from the stem, winding down into a spiral  |

**How the arches are mapped.** Arches on a floor are the tongue-tip family's
form, for two reasons. They belong to the family's own image, a train of waves
on the water; and _t_, _s_ and _n_ are the commonest consonants of Sinale, so
the arched form is the commonest letter on a page and carries the heaviest share
of the implied line. A voiced-partner encoding was weighed and set aside: Sinale
has almost no voiced partners, so it would put the form on two rare letters. The
stroke takes one to three arches; the letters use two. Tengwar gives its double bow to the lips; the Veldikko does
not.

**Voicing turns a letter over.** Each family's form either stands or hangs, and
a voiced partner is the same form turned over. Sinale's only voiced consonants
are _d_ and _dh_, both tongue-tip sounds, so they are the arches hung from the
stem: _d_ with the stem raised, as a stop, and _dh_ with it level, as a
fricative. A reader who knows _t_ and _s_ reads _d_ and _dh_ at once, as the same
letters turned over. The rule is drawn for every family, so the standing coil and
the hanging bud complete it; Sinale has no voiced lips or back sounds and uses
neither.

**Why the back family hangs.** The hanging forms are given a whole family so that
they are common enough to set an upper rhythm, and the back family is the one to
give: _k_ is frequent, so arched heads recur along a line, while the lips and the
tongue-tip, together with the stemless _l_, _r_ and carrier, keep most letters
standing on the line. A contrast within every family, voiced against voiceless,
was weighed and set aside as the main use: Sinale has almost no voiced
consonants, so the hanging forms would hardly appear.

**Three grades, one stroke changed.** The stem carries the grade:

| Grade     | The stem                                                   | Consonants     |
| --------- | ---------------------------------------------------------- | -------------- |
| stop      | raised: its head stands far above the bowl                 | _p_, _t_, _k_  |
| fricative | level: its head just clears the bowl, its foot on the line | _v_, _s_, _h_  |
| nasal     | lowered: carried below the line into a hooked tail         | _m_, _n_, _ng_ |

So the grades stand at three heights: raised, on the line, lowered. This is the
Sinale note's "one letter lowered": wearing takes a stop to the fricative of its
own place, and in the hand that is the stem worn down to its bowl, the same
letter left standing on the line. A worn word is visibly the same word with its
first stem cut down, and no worn form opens on a raised stem.

**The tails.** The lowered grade's own tail is the hook, the stem turning back
and up below the line like a _j_. The ezh and the forward sweep are the same
grade drawn with a longer tail: the scribe may use them at the end of a word or
of a line, where there is room below, and the font offers them on a word's last
nasal ([The long tails](#the-long-tails)). A tail never changes which letter it
is.

**The letters outside the families.** _l_ is the `riser` and _r_ the `crook`, both
stemless, so they stand apart from the family letters at a glance. The carrier
is the `carrier`, a short stem with no bowl. _d_ and _dh_ are the hanging
arches, as above.

**Length.** A doubled consonant is one letter with the `bar` beneath it. A long
vowel is its mark drawn on into a hairline.

**The vowel marks keep the harmony sets.** The sets map cleanly onto the three
kinds of mark:

| Set     | Kind of mark | Vowels                                    |
| ------- | ------------ | ----------------------------------------- |
| back    | dots         | _a_ one dot, _o_ two dots, _u_ three dots |
| neutral | dabs         | _e_ a dab rising, _i_ a dab lying level   |
| front   | hooks        | _y_ a hook, _ë_ a curl                    |

The Sinale rule that a word never holds a back vowel and a front one together is
visible at a glance: a word's marks are dots and dabs, or hooks and dabs, never
dots and hooks together. The check that catches most copyists is a check of
shape. The hooks are the only curved marks, and they belong to the rarest
vowels.

**How the marks sit.** A mark floats over the bowl of the consonant it follows,
clear of a raised stem. A word that opens on a vowel carries its mark on the
carrier. A diphthong is two marks over one consonant or carrier, in the order
they are said, so from right to left.

**Where letters touch.** Most letters touch the next: a `touch` flows from the
end of one floor up into the next letter's floor, a hairline arched above the
line, never a line drawn along it. [Layer 3: joining](#layer-3-joining) sets out
which letters touch and how.

## The specimen

`specimens/veldikko/strokes.png` holds:

- every stroke large, a bowl shown with its stem in grey,
  with guides in these cells only;
- each stroke across its permitted ranges;
- seven test sequences at display size, read from the right, with no line
  drawn, among them standing and
  hanging forms side by side and a run mixing the two;
- the same tests run on as lines at 48, 24 and 20 px to the em;
- one test drawn over its own skeleton, the skeleton a red line under the ink.

The tests set strokes side by side to test how they sit together. They are not
letters or words of the script.

**What the tests show.** With no line drawn, the floors of the standing forms make
the line by themselves, the arches weight it most, the hanging forms set a row of
arched heads above it, and the touches carry the eye along each word. At 24 and
20 px the hairlines hold as continuous lines, the forms stay distinct by the way they open, and the dots and dabs remain
separate marks.

## Layer 2: the letters

`tools/veldikko/letters.py` holds the letters as data over the strokes, and an
assembler that builds a letter with its marks, or a word with its letters set
right to left. A letter names its form (the bowl or stemless stroke), its grade
(the stem), whether it is voiced, and the two Áelendan ligatures, so every
letter is the rules applied to one row of data:

```python
import letters as L

g = L.glyph("t", L.S.HAND, marks="a:")           # t with a long a over it
w = L.word("k+a l p+i", L.S.HAND)              # kalpi, right to left, touching
path = L.S.outline(w, L.S.HAND)                # a pathops.Path
```

`tools/veldikko/letter_sheets.py` renders the letters, marks, words and close-up
sheets, or the ones named; `tools/veldikko/l_options.py` renders the _l_
candidates:

```sh
.venv/bin/python tools/veldikko/letter_sheets.py            # all four
.venv/bin/python tools/veldikko/letter_sheets.py closeup    # one
.venv/bin/python tools/veldikko/l_options.py
```

### The inventory

The consonants come from Sinale's sound data: the onsets _p t k v s h m n l r_,
the clusters, which add _d_ and _ng_, and _dh_, which stands between vowels.

| Letter | Sound                    | Form          | Stem    | Writes it          |
| ------ | ------------------------ | ------------- | ------- | ------------------ |
| _p_    | lips, stop               | `bud`         | raised  | both               |
| _v_    | lips, fricative          | `bud`         | level   | Sinale             |
| _m_    | lips, nasal              | `bud`         | lowered | both               |
| _t_    | tongue-tip, stop         | `arches`      | raised  | both               |
| _s_    | tongue-tip, fricative    | `arches`      | level   | both               |
| _n_    | tongue-tip, nasal        | `arches`      | lowered | both               |
| _d_    | tongue-tip, voiced stop  | `hung-arches` | raised  | both               |
| _dh_   | tongue-tip, voiced fric. | `hung-arches` | level   | Sinale             |
| _k_    | back, stop               | `hung-coil`   | raised  | both               |
| _h_    | back, fricative          | `hung-coil`   | level   | Sinale             |
| _ng_   | back, nasal              | `hung-coil`   | lowered | both               |
| _l_    | liquid                   | `riser`       | none    | both               |
| _r_    | liquid                   | `crook`       | none    | both               |
| —      | the carrier, no sound    | `carrier`     | short   | both               |
| _g_    | back, voiced stop        | `coil`        | raised  | Áelendan           |
| _th_   | tongue-tip, aspirate     | `arches`      | raised  | Áelendan, ligature |
| _dh_   | tongue-tip, voiced asp.  | `hung-arches` | raised  | Áelendan, ligature |
| _kh_   | back, aspirate           | `hung-coil`   | raised  | Áelendan, ligature |
| _gh_   | back, voiced aspirate    | `coil`        | raised  | Áelendan, ligature |
| _t'_   | tongue-tip, ejective     | `arches`      | raised  | Áelendan, ligature |
| _d'_   | tongue-tip, voiced ejec. | `hung-arches` | raised  | Áelendan, ligature |
| _k'_   | back, ejective           | `hung-coil`   | raised  | Áelendan, ligature |
| _g'_   | back, voiced ejective    | `coil`        | raised  | Áelendan, ligature |

The lowered stem ends in the hook. The voicing rule leaves one form unused: the
hanging bud, a voiced lip sound, which neither tongue has.

### The rules

- **The form is the place, the stem is the grade.** The lips stand as the bud,
  the tongue-tip as arches on a floor, the back hangs as the coil. A stop's stem
  is raised, a fricative's level, a nasal's lowered into the hook. A worn word
  is the same letter with its stem cut down to the bowl.
- **Voicing turns a form over.** _d_ and _dh_ are the arches hung; _g_ is the
  coil stood on the line. In the back family the turn runs the other way from
  the tongue-tip's, because the back family's voiceless form is the one that
  hangs.
- **_l_, _r_ and the carrier are stemless**: the riser, the crozier and the
  short curled stem. The riser is the tallest stroke in the hand, clear above
  every raised stem, and its head is an open tendril turned back, where a stem's
  vine curl is small and turned forward. It never has a bowl, and the carrier
  is less than a quarter of its height.
- **A doubled consonant takes the bar** beneath it, under the bowl's middle.
  Sinale doubles _p t k s m n l r_.
- **The vowel marks follow the harmony sets**: the back vowels are dots (_a_
  one, _o_ two, _u_ three), the neutral vowels dabs (_e_ rising, _i_ level), the
  front vowels hooks (_y_ the hook, _ë_ the curl). A long vowel, written
  doubled in the romanization (_aa_, _uu_, and _eë_ for the long _ë_), is one
  mark drawn on into a hairline; pitch is the flick at the forward end, up for a
  rise, down for a fall, none for level speech.
- **A diphthong is two marks over one letter**, in the order said, so the
  first is the right-hand one. A word that opens on a vowel, and a vowel that
  stands apart from the one before it, neither a diphthong nor a long vowel,
  carries its mark on the carrier.
- **A mark sits over the middle of the bowl**, at the mark line or a clear
  gap above the bowl's top, whichever is higher. Over a standing bowl that is
  the mark line; over a hanging form it is a little higher, clear of the heavy
  arch. The riser passes through the mark line, so its mark stands forward of it
  at the line, where a bowl's would be. A raised stem stands behind the mark,
  never through it. Two marks over one letter stand a clear gap apart.
- **Letters touch floor to floor** with the hairline touch, as
  [Layer 3: joining](#layer-3-joining) sets out.

### Additions to the plan

- **Emphasis.** Sinale stress never moves, so a mark over a later syllable is
  emphasis, and the Veldikko note gives the marks "poetic emphasis". The brow,
  the touch stroke arched over a vowel mark, is that emphasis. It reuses an
  approved stroke rather than adding one.
- **_nk_ is _ng_ and _k_.** Sinale says _nk_ with the back nasal, and the hand
  writes the sound, so _lonku_ is _l_, _ng_, _k_. The lowered hanging coil
  before the raised one shows the pair as one place.
- **The carrier inside a word**, for a vowel sounded apart.

### Áelendi's letters

Áelendi keeps three stop series where Sinale has one, and its own note states
that its scribes write the aspirates and ejectives as ligatures. Its letters are
the Áelendan adaptation of the hand, by the same rules:

- **_g_** is the coil stood on the line with a raised stem: the voicing rule
  applied to the back family, a letter rather than a ligature, since _g_ is a
  plain stop.
- **The aspirates _th_, _kh_, _dh_ and _gh_** are the plain stop with the
  breath: _h_'s hanging coil, drawn small, in place of the vine curl at the
  head of the stem. It is the stop and _h_ written as one sign, and it puts the
  ligature where nothing else in the hand stands, above the marks.
- **The ejectives _t'_, _d'_, _k'_ and _g'_** are the plain stop with the catch:
  the length bar laid across the stem two thirds up. The bar under a letter
  holds the consonant; across the stem it holds the throat. The romanization
  writes no ejective, so these letters reach a page only from a source that
  marks them.
- **Áelendi's _dh_ is a stop**, the voiced aspirate, so it is written with the
  breath on _d_ and never with Sinale's _dh_, the voiced fricative. The spelling
  table resolves _dh_ by tongue.

Áelendi has no _v_, _h_ or front vowel of its own; its loans from Sinale bring
_p_. The Sinale letters for _v_, _h_ and _dh_ and the hooks therefore appear in
Áelendi text only for Sinale words.

### The specimens

- `specimens/veldikko/letters.png`: every letter in its isolated form, labelled
  with the spelling, the sound, and who writes it.
- `specimens/veldikko/marks.png`: every letter under each of the seven vowel
  marks, long, rising, falling, the diphthong _ai_ and emphasis.
- `specimens/veldikko/closeup.png`: runs of marked letters at 24 and 20 px, at
  actual size and enlarged without smoothing, then at display
  size. The marks are judged here first.
- `specimens/veldikko/l-options.png`: the riser beside two shorter forms
  weighed for _l_, the loop and the sprout, each beside _r_, the carrier, _k_
  and _t_ and in words at display size and 24 px. The loop and the sprout stand
  at the bowls' height and close into blots at 24 px, and the sprout reads as
  _r_; the riser stays distinct at every size.
- `specimens/veldikko/words.png`: _nuuva_, _mollu_ beside _molu_, _kalpi_ beside
  its worn _halpi_, _eilava_, _aamas_, _rivy_, _ennedhi_ and _lonku_ in Sinale,
  and _khalthon_, _ghoran_, _thidharon_ and _gulmesa_ in Áelendi, right to left,
  each with its letter-by-letter spelling.

## Layer 3: joining

`tools/veldikko/joining.py` turns each letter into its contextual forms, and
`tools/veldikko/build_ufo.py` writes them, with the marks, into
`sources/Veldikko.ufo`, the source of the font **Veldikko**, one face in the one
hand for Sinale and Áelendi alike. The letters are the approved drawings of layer
2, never redrawn: a form is the letter with the halves of the `touch` added on
the sides that join. Lengths in this section are the generator's units, in which
a bowl stands 270 high; the font scales them ([The font](#the-font)).

```python
import joining as J

f = J.form("t", "medi")                   # t joined on both sides
f.tracks, f.advance, f.mark, f.bar         # forward-frame tracks; metrics in unscaled font units
tracks, width = J.setting("k+a l p+i")     # kalpi, set from its forms as the font sets it
```

### The forms

**Every letter joins on both sides.** The touch runs from the end of a letter's
floor to the back of the next letter, and every letter has both: the standing
bowls end their floor forward on the line, the hanging forms their open foot,
the riser its soft foot, the crozier its foot, and the carrier the foot of its
stem. So a word is one connected shape from its first letter to its last, and only
a space breaks it. A letter has four forms, as a right-to-left joining script's
letters have:

| Form     | Where                               | Joins                           |
| -------- | ----------------------------------- | ------------------------------- |
| isolated | a word of one letter                | neither side                    |
| initial  | a word's first letter, on the right | forward, to the letter after it |
| medial   | between two letters                 | both sides                      |
| final    | a word's last letter, on the left   | back, from the letter before it |

**A touch is cut in two at the join point.** The join point stands at a letter's
advance edge, 72 units above the line, where the touch runs level at its faint
swell. The leaving half sets down from nothing at the end of the floor, rises at
35° and levels off into the join point; the entering half runs on level from the
join point and falls at 28° into the next letter just behind its stem, a quarter
of the bowl's height up, where it lifts to nothing. Every form meets every other
at the same point, heading and pressure, so any two letters make one unbroken
hairline, arched a little above the line and never drawn along it.

**Spacing comes from the ink above the line.** A side that joins stands 50 units
beyond the letter's ink above the line, so two joined letters stand 100 apart, the
gap of the layer 2 words. A side that does not join stands 24 units clear of all
the letter's ink. Below the line nothing is spaced: a nasal's hooked tail turns
back under the letter before it, as a long tail does in Arabic calligraphy, and
the gaps above the line stay even.

**The stretch.** A letter that carries a long vowel, a pitched vowel or a
diphthong, and joins forward, takes its stretched form, whose leaving half is 130
units longer. The mark's hairline and flick run on forward of the bowl, and the
drawn-out join gives them room before the next letter, as a calligrapher draws
out a join to make space.

### The long tails

The hook is every nasal's tail. A word's last nasal, isolated or final, may take
one of the long tails in its place, because the room below the line is at a
word's end: `ss01` gives it the forward sweep under the letter, `ss02` the ezh,
and `salt` offers both. A font cannot see where a line ends, so the scribe, or the
page, chooses the long tail where a line ends. A hanging form ends a word in its
own open foot and takes no tail.

### The marks over joined letters

The marks sit over a joined letter exactly as over the isolated one: the mark
point of layer 2 travels with the letter into each of its forms. A lone mark
stands with its middle on that point; the two marks of a diphthong stand 56 units
apart, the pair centred on it, the first said on the right; the length bar stands
under the bowl's middle, or under the riser's foot. A vowel's length, pitch and
emphasis are drawn into its mark, so a vowel and its signs make one mark.

### The encoding

Veldikko draws the Veldikko's block, U+1ED50 to U+1EDFF, unassigned code
points of plane 1 whose default direction is right to left, so its text runs right
to left in any editor, browser or typesetter with no controls.
`tools/veldikko/encoding.json` is the table:

| Code points     | What                                                                                   |
| --------------- | -------------------------------------------------------------------------------------- |
| U+1ED50–U+1ED5D | the Sinale letters, _p v m t s n d dh k h ng l r_, and the carrier                     |
| U+1ED60–U+1ED68 | the Áelendan letters, _g_, the aspirates _th dh kh gh_ and the ejectives _t' d' k' g'_ |
| U+1ED70–U+1ED76 | the vowel marks, _a o u e i y ë_                                                       |
| U+1ED78–U+1ED7C | the signs: long, rising, falling, emphasis, and the length bar                         |

A word is typed as it is said: a letter, then the bar if its consonant is doubled,
then each vowel mark in the order said, each followed by its signs. _mollu_ is
_m_, _o_, _l_, bar, _u_; _nuuva_ is _n_, _u_, long, _v_, _a_.

`tools/veldikko/convert.mjs` converts romanized Sinale by the Sinale encoding, and
the guard and the specimens use it. A doubled consonant is the letter and the bar;
_n_ before _k_ is _ng_; a doubled vowel is one mark with the long sign, and
_eë_ is the long _ë_, so _leësy_ is _l_, _ë_, long, _s_, _y_; a diphthong of the
language is two marks; a vowel at a word's start, and any other vowel sounded
apart from the one before it, rides on the carrier. The romanization writes no pitch or emphasis, so the converter writes
neither, and it writes Sinale only: Áelendi wants its own convention.

### The font

HarfBuzz, and so Chrome, Foundry and Typst, shapes these code points in visual
order, because they belong to no script: a run is reversed before shaping, a
word's last letter first. So every rule reads a word from the left. A letter's
neighbour on the left is the letter after it, and a vowel mark, which follows its
letter in the text, stands before it in the run. The lookups sit in `rclt` and
`mark`, which every HarfBuzz shaper applies to horizontal text, in this order:

1. a vowel and the signs after it, in any order, become one precomposed mark;
2. each letter takes its form from its neighbours, marks ignored;
3. an initial or medial letter under a long or pitched vowel, or a diphthong,
   takes its stretched form;
4. `ss01`, `ss02` and `salt` give a word's last nasal its long tail;
5. each vowel mark moves to the mark point of the letter after it in the run, the
   second mark of a diphthong beside the first, and the bar to the bar point.

Mark-to-base attachment looks backward through the run and would put each mark
on the letter after its own, so step 5 is a chained positioning lookup keyed on
the letter that follows the mark. Each letter form carries its mark point and bar
point as the UFO anchors `mark` and `bar`, and the guard checks the shaped marks
against them.

**Size: the bowls stand at the x-height.** The outlines are scaled by 1.7157,
which brings the crozier _r_, the one letter that stands at the bowls' height
alone, to the x-height every face shares, 0.5135 em, where Semaron Kuriale's
minuscules stand. So a Veldikko word sets at the same size as Semaron or Latin
text at the same font size. The extenders keep their length, which is part of
the look: the riser _l_ reaches 1.46 em above the line and the raised stems
1.21 em, where Semaron's tallest letter reaches 0.75 em; the nasals' tails reach
0.53 em below it, where Semaron's reach 0.26 em. `tools/vertical.py` accepts the
raised stops, the riser, the nasals and the length bar past the shared band.
`specimens/veldikko/beside.png` sets Veldikko beside Semaron Kuriale and Latin at
20, 24 and 48 px.

**Line spacing is tight; clipping is not.** The line-spacing metrics, `hhea` and
the `OS/2` typographic ascender, descender and line gap with `USE_TYPO_METRICS`
set, are the shared ones every face takes, Semaron Kuriale's line box, so a
Veldikko word inside an English line leaves the line spacing even, and its risers
and tails reach into the space between lines. The `OS/2` Windows ascent and
descent cover the full ink of every glyph, so nothing is clipped. A block of
Veldikko, verse, a sample or a scroll, wants generous line height from the page's
own style sheet: 2.4 em keeps one line's risers clear of the tails above.

The word space is 400 units.

### Building and checking

```sh
.venv/bin/python tools/veldikko/build_ufo.py      # sources/Veldikko.ufo and tools/names/veldikko.json
PATH=.venv/bin:$PATH ./build.sh                   # the fonts, fonts.css, fonts.json, keyboards and charts
.venv/bin/python tools/veldikko/check_font.py     # the cmap, the forms and the features reaching them
.venv/bin/python tools/veldikko/guard.py          # every Sinale lexicon form, joined, with its marks placed
.venv/bin/python tools/veldikko/font_sheets.py    # the layer 3 sheets, through the built font
```

`tools/veldikko/guard.py` converts every word and name of the Sinale note, and its
fixtures (`tools/veldikko/fixtures.json`), shapes each right to left, and asserts
each letter's form, each folded mark, and where each mark and bar stands.
`--fixtures-only` needs no thalorna checkout, and CI runs it.

### The specimens

- `specimens/veldikko/forms.png`: every letter in its four forms and its two
  stretched forms, with each advance ruled beneath, then the nasals' hooks and
  long tails;
- `specimens/veldikko/joined.png`: the words of `words.png`, joined, set by the
  font at display size and at 48 px, the Sinale words converted from their
  romanization and the Áelendi words from their spelling;
- `specimens/veldikko/verse.png`: the Sinale sample phrases as a right-aligned
  block at a line height of 2.4 em, the same lines with the pitch the
  romanization drops, and Veldikko words inside an English paragraph at its own
  line height of 1.5 em;
- `specimens/veldikko/sizes.png`: the verse at 48, 32, 24 and 20 px, and enlarged
  without smoothing;
- `specimens/veldikko/beside.png`: one line in Veldikko, Semaron Kuriale and a
  Latin face at 20, 24 and 48 px on one baseline, the x-height ruled: the bowls
  stand at the x-height, the extenders beyond.

## Open questions

- **Where pitch is written.** On every word's last mark, or only where speech
  rises or falls against the level of a list.
- **Áelendan vowels.** Áelendi has eight vowel positions with length, and its
  scribes spend the pitch marks on them; which flick marks which vowel is the
  Áelendi encoding's to settle.
- **Ejectives in a romanized source.** The romanization writes none, so whether
  the encoding ever produces the catch, or leaves it to transcriptions of old
  pages, is open.
