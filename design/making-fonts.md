# Making the script fonts

This guide is for anyone, person or agent, who draws, builds or extends a font in this repository. It covers:

- the fonts that exist;
- how they are drawn, built, checked and delivered;
- the rules that keep a new font consistent with them.

Each font's own design note in `design/` holds its letter-by-letter detail. This guide holds what they share.

## The fonts

| Font                      | Script and setting                                                                                                  | Direction                                                        | Drawn as                                                                                                                                                              | Glyphs                                                               | Encoding                                                                                          |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| **Pirzath Carved**        | Pirzath, the Khazari carved row                                                                                     | left to right                                                    | graver cuts: straight tapered grooves and drilled dots, united into one outline per glyph                                                                             | 70                                                                   | U+F0000, its own code points only                                                                 |
| **Thuravark Carved**      | Thuravark, the Nordmen rune-row, the reduced daughter of Pirzath, and its imperial recension, the Tharavarkon       | left to right                                                    | 28 staves: one upright stem with up to four straight branches at two fixed slopes; the recension's three staves, ten bound runes and crowned frame on the same system | 128, the crowned forms among them                                    | U+F0100, its own code points only                                                                 |
| **Pirzath Hand**          | the everyday printed Pirzath, the Khazari working hand                                                              | left to right                                                    | a blunt square tool, chalk or a carpenter's pencil, at 45° with mild contrast, generated from strokes and signs (see `design/pirzath-hand.md`)                        | the full alphabet, printed, with its long vowels and doubled letters | shares Pirzath Carved's encoding                                                                  |
| **Qalezu Hand**           | the Khelathi everyday alphabet, consonants only                                                                     | right to left                                                    | a broad reed nib at 30°, swept along centrelines                                                                                                                      | 109                                                                  | U+1EA00–U+1EA38, natively right to left; the catch-before forms drawn from the catch and the sign |
| **Khelathi Zethu Glyphs** | the Khelathi temple hieroglyphs                                                                                     | right to left, or top-down columns                               | hairline silhouettes of pictures                                                                                                                                      | 304 signs, 695 glyphs with variants                                  | U+1EA40 + inventory row; rendered from composition markup                                         |
| **Semaron Kuriale**       | the Vylarian alphabet, majuscule and minuscule, first hand Kuriale                                                  | left to right                                                    | a broad nib at 30°, derived from Thuravark's staves; its own system, not Pirzath Hand's look                                                                          | 75                                                                   | U+F0200, its own code points only                                                                 |
| **Helonika Book**         | the Helónika, the Helonic alphabet, its book hand: geometric capitals over a round broad-pen minuscule              | left to right                                                    | a flat reed at 10°, lighter for the minuscules, generated from strokes and letters (see `design/helonika.md`)                                                         | 71 characters                                                        | U+F0300, its own code points only                                                                 |
| **Veldikko**              | the Veldikko, the Sinale starlight-hand, in which the Sinale and the Áelendi write: featural, vowels as marks above | right to left, joined                                            | a narrow qalam-cut nib at 62°, generated from strokes, letters and joins (see `design/veldikko.md`)                                                                   | 23 letters in four forms, 84 vowel marks                             | U+1ED50, letters, marks and signs                                                                 |
| **Vedyakshara Classical** | the Vedyakshara, the Vedyari syllabary, its classical temple hand: every sign hung from a headline                  | left to right                                                    | a steep square-cut reed at 75°, generated from strokes and signs (see `design/vedyakshara.md`)                                                                        | 29 signs, 19 fused, and their half, final and r-foot forms           | U+F0400, signs, marks, digits and bars                                                            |
| **Teng Chou**             | the Celestial Record of Tantsou and Jenchai, logographic, with the Jurthati syllabary                               | top-down columns from the right; left to right in an inline span | a brush, generated from strokes, components and IDC layouts (see `design/teng-chou.md`)                                                                               | 213 characters, 87 syllabary signs                                   | U+F1000 characters, U+F2000 syllabary                                                             |

A font's family name is its script followed by how the script is made: **Carved**, **Hand** or **Glyphs**. A script with more than one canon hand uses the name of the hand instead, as Semaron Kuriale does. The file name is the family name without spaces, then `-Regular`, and the PostScript name is the same. The npm manifest (`fonts.json`) may name several variants from one font file, differing in the OpenType features turned on: Thuravark Carved Bound is the same file as Thuravark Carved, with the `ss01` bound runes turned on.

Scripts that are not here are varieties of one of these fonts. They write with the same glyphs, perhaps with a few additions or different sound values, as many tongues share the Latin alphabet:

- **Tharavarkon and Thurarth** are varieties of Thuravark.
- **Okhatha-zethu and Merazan** are varieties of Qalezu.

Ch'alish P'ilam has an issue in this repository and no font.

## The repository

| Path                                                                                                                                            | Holds                                                                                                                                                                                                               |
| ----------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `sources/<Font>.ufo`                                                                                                                            | The source of each font: outlines, cmap, metrics, `features.fea`, GDEF categories and glyph order. The UFO is the source of truth.                                                                                  |
| `fonts/<Font>-Regular.ttf` and `.woff2`                                                                                                         | The built fonts, committed. CI rebuilds them and fails if they differ.                                                                                                                                              |
| `specimens/<font>/`                                                                                                                             | The specimen sheets.                                                                                                                                                                                                |
| `design/<font>.md`                                                                                                                              | The design note, present tense: the system, the letters, the characters and their forms, the rounds.                                                                                                                |
| `tools/<font>/`                                                                                                                                 | `check_font.py`, `guard.py` and `specimens.py` for each font, plus any encoding table such as `encoding.json`.                                                                                                      |
| `tools/render.py`, `tools/prove_guards.py`, `tools/notdef_box.py`, `tools/apply_notdef_box.py`, `tools/font_names.py`, `tools/add_mac_names.py` | Shared tools. `render.py` sets shaped text in a font for specimens. `prove_guards.py` proves each guard fails a broken font. `notdef_box.py` is the box guard, and `apply_notdef_box.py` writes the box into a UFO. |
| `build.sh`                                                                                                                                      | Builds every font, reproducibly.                                                                                                                                                                                    |
| `nogit/`                                                                                                                                        | Generators and scratch. Not committed.                                                                                                                                                                              |

### The toolchain

Tool versions are pinned in `requirements.txt` (fontTools, fontmake, ufoLib2, skia-pathops, uharfbuzz, Pillow, brotli, PyYAML). Create `.venv` from it. Use `rsvg-convert` to render SVG sheets.

`build.sh` runs fontmake on each UFO, adds the Macintosh copy of the name records with `tools/add_mac_names.py`, and compresses the WOFF2:

```sh
export SOURCE_DATE_EPOCH=1767225600
fontmake -u sources/<Font>.ufo -o ttf --keep-overlaps --no-production-names \
    --output-path fonts/<Font>-Regular.ttf
python tools/add_mac_names.py fonts/<Font>-Regular.ttf
fonttools ttLib.woff2 compress -o fonts/<Font>-Regular.woff2 fonts/<Font>-Regular.ttf
```

- **Reproducibility.** The fixed `SOURCE_DATE_EPOCH` sets the `head` timestamps, so two builds are byte-identical and CI can diff the committed fonts.
- **`--keep-overlaps`.** Use it where a glyph's contours overlap by design and removing the overlap would merge something that should stay separate.
- **TrueType outlines.** The fonts are OpenType fonts with TrueType (quadratic) outlines, shipped as `.ttf` and `.woff2`. fontmake converts the generators' cubic curves to quadratics within about one unit, which is invisible. TrueType outlines compress better in WOFF2 and render the same in browsers, Foundry and Typst. A CFF-outline `.otf` (`fontmake -o otf`) can be added for desktop or print users if one is ever wanted. The layout features are identical either way.
- **Never edit a built font by hand.** Change the UFO, or regenerate it.

### Generators, then UFO

A font starts as a Python generator in `nogit/<font>/`. The generator does three things:

1. draws every glyph as code;
2. runs the checks;
3. writes `sources/<Font>.ufo`.

Generators live outside the tree because they are one-off drawing tools. The committed UFO is what a font editor opens and what fontmake builds. Once a design is settled it is edited as a UFO, in FontForge, Glyphs or RoboFont, and the generator is kept only as a record.

### One vertical standard

Every face takes Monaspace Neon's vertical metrics at 1000 units to the em: ascent 945, descent 200, line gap 100, window ascent 945 and window descent 250 (larger where a glyph reaches farther), with USE_TYPO_METRICS set. Each face is also scaled about the origin by one factor, so that its typical letters stand as tall as Neon's x-height (0.5135 em) or cap height (0.73 em) beside them. `tools/vertical.py` holds the metrics, the factors and the typical letters of each face, and checks them on the built font. A generator draws at its own design size and its output is multiplied by the face's factor; `tools/scale_face.py` does that to a UFO. Veldikko's bowls stand at the x-height and its risers, raised stems and tails reach well past the ascent and descent, which is the hand's look: its window ascent and descent cover them, so nothing is clipped, while its line-spacing metrics stay the shared ones, so a Veldikko word in a line of other text keeps the lines even. `tools/vertical.py` names the glyphs allowed past the band.

### One spacing rule

Every glyph with ink and an advance stands at its ink: its advance is its ink width plus one sidebearing on each side, the same for every glyph of the face. The notdef and the box keep their own widths, and a mark has no advance. The space is the face's word space.

| Face                  | Sidebearing | Space          | Notes                                                                                                          |
| --------------------- | ----------- | -------------- | -------------------------------------------------------------------------------------------------------------- |
| Pirzath Carved        | 26          | 499, a dot     | The kerning sets each pair to one optical gap.                                                                 |
| Thuravark Carved      | 34          | 0              | No kerning; the staves run on.                                                                                 |
| Semaron Kuriale       | 12          | 24             | A close book hand.                                                                                             |
| Qalezu Hand           | 28          | 200            | A doubled sign and a catch-before form take their sign's advance.                                              |
| Khelathi Zethu Glyphs | 31          | 62, the gutter | A sign's width follows its drawing; its box scale is unchanged. A phrase runs on.                              |
| Pirzath Hand          | 70          | 500            | A printed working hand, set open so letters never touch in low light; `tools/spacing.py` holds its own limits. |
| Veldikko              | 41          | 400            | Joined: a side that joins ends at the join point, half a gap beyond the ink, so it is exempt.                  |
| Teng Chou             | 30          | 250            | Set by its generator, `tools/teng-chou/build_ufo.py`; down a column every glyph takes exactly one em.          |

Well-set text leaves about a tenth of each advance blank. `tools/respace.py` applies the rule to a UFO, carrying anchors, components, mark positions and kerning with each glyph, and keeps each face's sidebearing, and the word space of Qalezu Hand and Khelathi Zethu Glyphs, in `SPACING`; a generator's output is respaced with it after scaling. `tools/spacing.py` measures the built fonts and holds those spaces.

## Who does what

| Work                                                                                      | Who                                      | Why                                                                                                                                    |
| ----------------------------------------------------------------------------------------- | ---------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| Letter design: the system, the letterforms                                                | Fable, which may look at its own renders | Its letter design is the strongest, and the owner prefers it. It is expensive, so give it drawing only.                                |
| Figurative signs (hieroglyphs, picture-glyphs, icons)                                     | Opus, looking at its own renders         | Pictures must be judged by eye. Opus drawing with eyes produced the accepted hieroglyphs; Fable drawing blind produced crude sketches. |
| Plumbing: UFO, `features.fea`, encoding, build, checks, guard, specimens, CI, design note | Sonnet                                   | Mechanical, and checkable by the gates.                                                                                                |
| Inventories (what a script writes)                                                        | Sonnet, report only                      | Derived from canon; the owner rules on it.                                                                                             |

**Viewing rune-like images can trip safety filters.** It flagged Fable twice. For any rune row or angular stave script:

- the drawing agent works blind, in code;
- or it views only its own non-runic renders;
- the coordinator looks at the rune sheets.

**If viewing is interrupted, the agent stops and reports.** It does not work around the filter.

## The workflow for a new font

1. **Inventory (report only).** Write it in thalorna's `nogit/` as `design-<script>-inventory.md`. It fixes:
   - each sign, its sound and what types it;
   - case and direction;
   - numerals and punctuation;
   - the descent from any parent script;
   - every place canon and spelling disagree.

   The owner rules, and those rulings are recorded in the inventory.

2. **The owner's sketches, if any.** The owner may draw a sheet. **A sketch fixes a letter's identity, not its finished form**: its topology, its strokes, its marks. Do not transcribe a quick sketch's proportions and wobbles. Where the owner's later written word and a sheet disagree, the later word wins. Note any conflict and ask.
3. **System-first pilot.** Draw a small set, the letters of one sample sentence, on a stated system (below), and set them in text. The owner reviews the pilot, usually on a published page, often with marked-up screenshots.
4. **Iterate on the pilot.** Fix the system, not single letters, so every later letter inherits the fix.
5. **The full set,** on the approved system.
6. **Plumbing** into the UFO, build, checks, guard, specimens, CI and design note. The UFO carries `notdef.box` and maps every unused character to it (below). Open the PR as a draft, read CI once, then mark it ready.
7. **Encoding and typing** (below), if not already set.

## The hand: a written script

The method behind a written hand drawn on a measured system. Semaron follows it.

### The system comes first

Write the system as named constants at the top of the generator, and build every letter from them, never freehand:

- **Heights.** The body (consonant) height, the vowel height if vowels are smaller, the ascender and the descender. **No letter is taller than 1.2× the body.** Tall ascenders, such as the 2.2× of a Latin school cursive, do not suit these scripts.
- **One slant.** It is 12° for Semaron.
- **One pen.** A pointed pen with a gentle swell is heavy on falling strokes and light on rising strokes and turns, following the real stroke direction. A broad-nib chancery pen with real contrast is a different, equally valid choice.
- **Shapes.** One oval (a width : height ratio, its axis at the slant), one arch and one bowl (halves of the oval), and three or four standard letter widths.
- **One entry, one exit and one join,** at fixed angles, the entry steeper than the exit. The join between them is one concave curve, so it never lines up with the stroke it feeds.
- **One mark weight** for poles, notches, strikes, doubling lines and quotation lines, all straight.

### Lessons learned the hard way

Each of these was a visible fault in an earlier round:

- **Measure the slant on the rendered strokes,** never trust the shear constant alone. A stem refitted together with its head hook and foot turn as one smooth curve bows, and its lean drifts from 12° to 4° or 15°. Make stems explicit straight lines, and let the turns ease into them.
- **No jogs at a letter's start.** An entry that rises, steepens, then turns through a small hook makes two bends within a few pixels, and it reads as a kink. An entry is one straight run, or one gentle turn, into the first stroke.
- **A straight entry meets a round bowl smoothly at only one point:** where the bowl runs at the entry's angle. On a wide oval that point is far from the start, and the letter balloons. Use a gently curving entry, one curvature sign and a radius above about 500 units, so it meets the bowl sooner.
- **Straight joins read as strikes.** A straight join collinear with the next letter's straight entry forms one long slash. Curve the join so it leaves shallow and arrives steep.
- **No curls at terminals.** Lifted letters end in short straight strokes on the join angle. A lifted line is the joined line with the bridges cut.
- **One drawing per letter.** The isolated glyph, the lifted text and the joined text must be identical. Only the connector differs. Build each letter once and only translate it into place. Never rescale or re-stroke it in context.
- **The text is the test.** If a letter looks wrong in a word, change the letter, then make the isolated glyph match.
- **Families share parts exactly.** A letter that adds a mark to another is that letter's drawing plus the mark, and a mark two letters share stands in the same place on both.
- **Marks are attached and straight,** placed where the owner draws them. Never float a mark clear of its letter unless told to.
- **Smoothness is visible, so make it measurable.** Fit few-knot cubic centrelines with Hobby's algorithm, stroke them with skia-pathops, union the result, and refit smooth runs to long cubics. Then check for tangent breaks, curvature ripples and edge waviness.

### The checks for a hand

Run these on every glyph before a sheet goes to the owner:

- **Identity:** every occurrence of a letter in the text lines is polygon-equal to its isolated glyph, and family members equal their shared parts (for example, gh = g + strike).
- **Stem angle:** every straight stem measures the slant to within 1°.
- **Entry, exit and connector:** within the first and last 20% of every entry, exit and join there is no kink (a tangent jump of 6–90°) and no wiggle (adjacent bends of opposite sign).
- **Distinctness:** render every pair at an 18 px body, and look at the closest pairs yourself.
- **Look:** render the glyph row, the text lifted and joined at display size, and the text at 18 and 24 px. Judge first against the owner's reference fonts for proportion and rhythm, then letter by letter. Copy no letterform from a reference.

## Carved and runic scripts

Pirzath Carved and Thuravark Carved are drawn as tool marks, not pen strokes:

- **Strokes.** A cut is a straight groove, full width in the middle and tapering to a point at each end, or a drilled octagonal dot. A glyph is the union of its cuts.
- **Orientation.** No cut runs along the line, because the stone splits along the grain. The one exception is the sentence end. Arms follow a small set of fixed slopes; Thuravark has exactly two.
- **Proportions.** Consonants are larger than vowels, so the skeleton is read first on worn stone. Pirzath Carved uses a 541 × 728 box at weight 108 for consonants, and 312 × 458 at weight 85 for vowels.
- **Spacing.** Each glyph follows the spacing rule above. Pirzath Carved derives its kerning from the outlines: each glyph's left and right profile is measured in bands, and every pair is kerned to the same optical gap. Thuravark's staves carry their own room, so it has no kerning.

## Figurative scripts: the hieroglyphs

Khelathi Zethu Glyphs was drawn by Opus, looking at its renders, in batches of 30–50 signs. The batches shared a drawing library: `lib.py` holds the parts model, the stroker, the figure canon and the kits. Each group of signs is a module under `signs/`.

- **Silhouettes, not stick figures.** Every sign is a closed silhouette traced by a hairline, 1.5% of the quadrat (stroked at 12 units on a 1000 em). Fine interior detail uses the same weight. Solid fill only where it means something. A skeleton drawn with a fat pen looks like a child's drawing.
- **One proportion canon** for every figure: profile head, frontal eye and shoulders, legs in profile, and one head-to-body ratio. Shared kits (head, hands, feet, torso, garments, beasts, birds, props) keep the figures consistent. Never change a kit's output for signs already drawn without re-rendering and comparing them.
- **Variants.** Each sign has two or three: `.a` the full form, `.b` a quicker cut, `.c` a changed attribute. A variant is the same sign, never a different subject.
- **Coverage comes from scenes.** Write the scenes canon describes (a hunt, a harvest, a decree), list the signs each needs, and set a sample inscription for each. Spelling signs ensure any name can be written.
- **Quadrats and cartouches are the font's; columns are the page's.** Khelathi Zethu Glyphs stacks signs into quadrats and draws the cord round a royal name from Unicode's Egyptian Hieroglyph Format Controls, typed at their twins in the font's own block so that a browser shapes them in one run with the signs. The layout reads the run in the visual order every HarfBuzz-based shaper gives it, and works in horizontal text only, so a column is laid out by the page. `design/khelathi-zethu-glyphs.md` gives the controls, the model and its limits.
- **Two-person signs face each other.** The first faces the line's start, and the second is its mirror.

### Originality and licensing

These rules apply to every font, and above all to figurative ones:

- **Draw every outline from scratch.** Never trace chart images (the Unicode code charts are "all rights reserved") or any font's outlines. Following an ancient sign's pose and convention is fine; copying a modern drawing's contours is not.
- **People, animals and ordinary work** (fishing, threshing, rowing) may follow their real-world model closely. **Objects, symbols and royal or religious emblems must be the setting's own.**
- **Banned for the Khelathi script:** the ankh, the djed, the was-sceptre, the eye of Horus, the scarab, the uraeus, the double crown, the pyramid, the obelisk, the royal crook and flail, and royal regalia generally. The cartouche-like oval is allowed, with its own knotted-cord tie.
- **Check every sign** against the runes used as hate symbols, swastika-like forms and sun-wheels. A display, handout or device shows a whole word or name, never a lone stave.
- **Every font is SIL OFL 1.1,** and its UFO's `fontinfo` carries the copyright, licence and licence URL.

## Icons drawn from the script

The Khelathi god icons are each god's own hieroglyph, coloured, on the culture's lapis background. They are generated in code from the sign drawings, not by an image model.

- **Palette.** Flat, saturated, Egyptian: red ochre, gold, amber, turquoise, malachite, white, black. No blue on a blue ground. No gradients, glow or texture.
- **Design for the smallest size.** Foundry shows icons at 48 px in the directory and compendium lists, and at 80 px in the SoHL item-sheet header, the largest they ever appear. So:
  - make the black outline about 1.5–2 px at 48 (34 px at 1024);
  - add a cream keyline (26 px at 1024) with a narrow dark separation, so the sign stands clear of a busy background;
  - make the sign about 85–90% of the tile;
  - start from the sign's quick cut, and drop detail that cannot survive 48 px.
- **Background.** Soften a busy one, blurred lightly and its contrast halved toward its mean colour, rather than lightening it.
- **Format.** Ship icons in thalorna as 512 × 512 WebP under `assets/icons/affiliation/<culture>/`. An icon resolves by its basename, so the folder can change without breaking references. `assets/icons/provenance.yaml` records the licence.

## Encoding: what each glyph is in the text

### Left-to-right scripts

A font draws code points and states no spelling. Each character of a script, a letter, a digraph letter, a long vowel, a numeral, a point or a mark, is one code point, and the font draws it from that code point alone; every other character, Latin included, prints the box (see [For every font](#for-every-font)). A font's substitutions are its contextual forms only: a joined form, a doubled consonant's form, a fused form, a mark's form, the box for a mark with no letter before it, the empty glyph of an ignorable. A substitution never turns one character into another, which would be a spelling built into the font.

Spelling lives in the consuming build. Notes write names in the setting's roman spelling, and a run marked `map=` is written in a script's code points by that script's mapping note, a thalorna note whose `data.map` states the spelling as rows. The keyboard layouts type the code points directly.

Each left-to-right script has its own **block of 256 code points** in plane 15, the Supplementary Private Use Area-A:

| Block           | Script                             |
| --------------- | ---------------------------------- |
| U+F0000–U+F00FF | Pirzath (Carved and Hand share it) |
| U+F0100–U+F01FF | Thuravark                          |
| U+F0200–U+F02FF | Semaron                            |
| U+F0300–U+F03FF | Helónika                           |
| U+F0400–U+F04FF | Vedyakshara                        |

U+F0500–U+F0FFF is reserved for the remaining alphabets and syllabaries. Teng Chou takes U+F1000–U+F2FFF: its characters from U+F1000 and its Jurthati syllabary from U+F2000, each in the order its data adds them, and the rest reserved. The README's "Code point blocks" section lists every block, and `BLOCKS` in `tools/codepoint_order.py` registers them.

### Right-to-left scripts

Latin forced right to left with the bidi override characters works, but HarfBuzz reverses a run whose direction opposes its script before GSUB runs. Every digraph rule then needs a reversed copy (`rtla`), which is fragile. So the right-to-left scripts use their own code points instead:

- **The blocks.** They are **unassigned code points whose default bidi class is R**:
  - Qalezu: U+1EA00–U+1EA3F;
  - Khelathi Zethu Glyphs: U+1EA40–U+1EC6F, with U+1E960–U+1E9FF as overflow;
  - Veldikko: U+1ED50–U+1EDFF.

  Text in them runs right to left natively in Chrome, Foundry and Typst, mixed with English, digits included.

- **The table.** One file per font, `tools/<font>/encoding.json`, holds glyph, code point and sound, and for Qalezu Hand the catch-before forms, which have no code point.
- **Converting the notes.** A mapping in the consuming build converts a note's roman spelling to these code points. Qalezu's `qalezu` mapping note drops the vowels, writes a word-initial vowel as the catch, a digraph as one sign and a doubled consonant as its doubled sign; the Qalezu guard writes the lexicon through it. Khelathi Zethu Glyphs and Veldikko, which no mapping note writes yet, have converters in `tools/convert.mjs` and `tools/veldikko/convert.mjs`, which are not shipped.
- **No mark-to-base attachment on these code points.** HarfBuzz, and so Chrome, Foundry and Typst, shapes script-less right-to-left code points in visual order, the run reversed, so a mark that follows its sign in the text stands before it in the run, and a mark-to-base lookup, which looks backward, attaches it to the wrong sign. Either precompose, or place the mark from the sign after it in the run:
  - Qalezu precomposes: each doubled consonant has its own code point, with the bar drawn in, and the font draws a catch before a consonant as that consonant's catch-before glyph, with three dabs drawn over it, by a ligature that reads the run in visual order, sign first;
  - Veldikko has too many vowel marks to precompose, so a chained positioning lookup moves each mark to the point its letter states, reading the letter that follows the mark in the run, and its joining rules read a word from its last letter. `design/veldikko.md` gives the lookups.
- **Variants** use only context-free substitutions: `ss01` and `ss02` single substitutions, and an alternate substitution in `salt`.

### For every font

- **Every character the script does not use prints a visible box.** Stray characters in a text must be obvious. The box is the glyph `notdef.box`, a copy of `.notdef` with the same outline and advance, and every font maps to it every code point of these ranges that it does not draw:
  - U+0021–007E Basic Latin;
  - U+00A1–00FF Latin-1 Supplement;
  - U+0100–017F Latin Extended-A;
  - U+2010–205E General Punctuation.

  The space (U+0020) and the no-break space (U+00A0) stay spaces, and the default-ignorables stay empty. The apostrophe follows the rule in a script that has none.

- **Why a glyph of its own.** A code point missing from the cmap makes a browser, Foundry or Typst fall back to the next font in the stack, so the stray character prints as an ordinary Latin glyph. A cmap entry that points at glyph 0 is treated as missing, and falls back the same way. So the box is a separate glyph that is never glyph 0, and a substitution that wants `.notdef` substitutes `notdef.box`.
- **The box behaves as `.notdef` does.** It is in the contextual classes, the GDEF base class and the kerning that mention `.notdef`, and it has no joined forms.
- **Where it is written.** `tools/apply_notdef_box.py` writes the glyph, the mappings and the feature entries into a UFO and does nothing on a second run. A generator calls it after it writes its UFO. A font that sets only its own code points, such as Qalezu, lists the box's code points in the script that derives its cmap.
- **The guard.** `tools/notdef_box.py` walks the ranges on a built font and fails when a code point is unmapped, maps to glyph 0 or maps to anything but the box without being a used code point. A used code point is one whose cmap entry reaches another glyph that draws, or the glyph of the space, the hyphen-minus or the default-ignorables. Each `check_font.py` runs it.

- **Default-ignorables draw nothing.** Map U+200B–200F, U+202A–202E, U+2066–2069 and U+FEFF to an empty glyph, and add a `ccmp` single substitution to a second empty glyph. A cmap entry alone fails, because HarfBuzz swaps an ignorable for the `space` glyph, and Pirzath's space is a visible dot.
- **Keyboard layouts** give each glyph exactly one keystroke: the base letter on its key, the paired sound on Shift, and the extras on Option/AltGr or spare symbol keys. Each layout ships for macOS, Windows and Linux. A printable cheat sheet is generated from the same table.

## Checks and gates

| Check                                     | What it proves                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| ----------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `tools/font_names.py`                     | Every font carries name IDs 1 to 6 on both the Windows and the Macintosh platform, the same on each; the family name is the one in its table; the PostScript name has no spaces; the OS/2 Unicode ranges and code pages name only the font's own script, never Latin. Runs in CI.                                                                                                                                                                                                |
| `tools/<font>/check_font.py`              | The cmap matches the encoding; the name table carries the OFL; every glyph has outlines; marks have zero advance; features reach every variant; every unused character maps to the box. Runs in CI.                                                                                                                                                                                                                                                                              |
| `tools/vertical.py`                       | Every face has Monaspace Neon's vertical metrics with USE_TYPO_METRICS set, its typical letters stand within 2% of Neon's x-height or cap height, its sxHeight and sCapHeight match them, and no ink leaves the band between the ascent and the descent except the accepted overshoot. A face written in columns (Teng Chou) also carries `vhea` and `vmtx`, every character on a vertical advance of exactly one em and one vertical origin, centred on its horizontal advance. |
| `tools/spacing.py`                        | Every face sets its text at a natural spacing: the median blank share of its advances is at most 14%, and in its sample lines the mean gap between the inks of neighbouring signs is at most 0.08 em and the largest at most 0.22 em; the word space of Qalezu Hand and Khelathi Zethu Glyphs is the one in `SPACING`. Runs in CI.                                                                                                                                               |
| `tools/codepoints.py`                     | Each face, shaped from its own code points, yields exactly the glyphs `fonts.json` lists; its cmap maps nothing else but the space, the default-ignorables and the box; and no substitution writes a character it did not read, so the font states no spelling. Runs in CI.                                                                                                                                                                                                      |
| `tools/notdef_box.py`                     | Every code point of the Latin and punctuation ranges is mapped, and every one the face does not draw is on `notdef.box`, never glyph 0. Runs in CI.                                                                                                                                                                                                                                                                                                                              |
| `tools/khelathi-zethu-glyphs/quadrats.py` | Shapes Khelathi Zethu Glyphs' quadrat and cartouche fixtures, its samples written with joiners, runs of quadrats and a seeded sweep of random ones, and asserts each sign's scale and place against the layout computed in Python, and the cord round each cartouche. Reads no lexicon.                                                                                                                                                                                          |
| `tools/<font>/guard.py`                   | Writes every lexicon form through the script's mapping note, or takes every sample inscription, shapes it through the built font with uharfbuzz and asserts the right glyphs and neither `.notdef` nor the box. It reads thalorna's lexicon and mapping notes from a local checkout; with `--fixtures-only` it shapes its fixtures alone, written as `tools/mapped.json` records them, and runs in CI.                                                                           |
| `tools/prove_guards.py`                   | Each guard fails a deliberately broken font: a sign removed from the cmap, GSUB stripped, the box guard's question mark unmapped or put on glyph 0, or every advance widened. A guard that cannot fail proves nothing.                                                                                                                                                                                                                                                           |
| `tools/<font>/specimens.py`               | Renders the sheets in `specimens/<font>/`. Look at every page.                                                                                                                                                                                                                                                                                                                                                                                                                   |
| CI (`.gitea/workflows/ci.yml`)            | Builds every font, runs each `check_font.py`, and fails if the committed fonts, `fonts.css` or `fonts.json` differ from the build. Also checks the formatting and the npm package. Also runs the hooks, the attribution check and the TODO check.                                                                                                                                                                                                                                |

## Delivering the fonts

Readers install nothing.

- **Web.** The site serves each font as WOFF2 through `@font-face`, and a script span carries the font's class.
- **Foundry VTT.** The package ships the font files and registers them in its stylesheet, or through `CONFIG.fontDefinitions`, so every client loads them. Foundry v14's ProseMirror editor keeps `dir`, `class`, `lang`, `style` and invisible control characters through a save, but strips `<bdo>` and `<bdi>` to bare text. Never emit those two elements.
- **PDF (Typst).** Typst embeds the font in the PDF.
  - A right-to-left block uses `#set text(dir: rtl)`.
  - Typst honours RLI, RLO, PDF and PDI only when they sit in the same text element as the run.
  - Typst has no vertical writing mode, so the build stacks a column's signs itself.
- **Right-to-left blocks** use a right-to-left container (`dir="rtl"`) for alignment, in every target.
- **Columns** (the temple hieroglyphs) use `writing-mode: vertical-rl` with `text-orientation: upright` in HTML, one quadrat to a row laid out by the build.
- **One build rule for every target.** package-build marks text as a script, sets it in the script's font, converts right-to-left scripts to their code points, and lays out columns. Quadrats and cartouches in a line are the font's.
- **npm.** The fonts are published as `@heroiclands/fonts`: `fonts/*.woff2`, `fonts/*.ttf`, `fonts.css`, `fonts.json`, `keyboards/`, `LICENSE` and `README.md`, and nothing else (`npm run check:package` asserts it).
  - `build.sh` writes `fonts.css` and `fonts.json` after the fonts, and CI fails when either differs from a fresh build.
  - A change a user of a font meets gets a changeset. Merging it to `main` opens the Version Packages pull request, and merging that tags `v<version>` on Gitea.
  - The push mirror carries the tag to GitHub, where `.github/workflows/release.yml` publishes to npm under Trusted Publishing and cuts the GitHub Release.
- **Licence.** The OFL lets a font be embedded in pages, documents and books, and bundled with software, without that work taking on the font's licence.

## Working with the owner

- **Publish pilots and rounds on a page,** with the owner's sketch beside each glyph where one exists.
- **Read marked-up screenshots literally.** Circles mark faults; green lines show the intended stroke. Look at the screenshot itself.
- **Fix the system, not the instance.** One reported fault usually stands for a family, so apply the fix to every member.
- **Write each ruling into the design note,** and into the packet for any later batch, so later rounds cannot drift from it.
