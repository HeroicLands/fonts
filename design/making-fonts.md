# Making the script fonts

This guide is for anyone, person or agent, who draws, builds or extends a font in this repository. It covers:

- the fonts that exist;
- how they are drawn, built, checked and delivered;
- the rules that keep a new font consistent with them.

Each font's own design note in `design/` holds its letter-by-letter detail. This guide holds what they share.

## The fonts

| Font | Script and setting | Direction | Drawn as | Glyphs | Encoding |
| --- | --- | --- | --- | --- | --- |
| **Pirzath Carved** | Pirzath, the Khazari carved row | left to right | graver cuts: straight tapered grooves and drilled dots, united into one outline per glyph | 76 | Latin spelling, through GSUB; private-use block U+F0000 planned |
| **Thuravark Runic** | Thuravark, the Nordmen rune-row, the reduced daughter of Pirzath | left to right | 28 staves: one upright stem with up to four straight branches at two fixed slopes | 51 | Latin spelling; U+F0100 planned |
| **Pirzath Hand** | the everyday written Pirzath | left to right | a pointed pen with a gentle swell, on a measured system (see [The hand](#the-hand-a-written-script)) | the full alphabet, lifted and joined | shares Pirzath Carved's encoding |
| **Qalezu** | the Khelathi everyday alphabet, consonants only | right to left | a broad reed nib at 30°, swept along centrelines | 109 | U+1EA00–U+1EA38 and U+1ECC0–U+1ECEB, natively right to left |
| **Khelathi Zethu** | the Khelathi temple hieroglyphs | right to left, or top-down columns | hairline silhouettes of pictures | 304 signs, 695 glyphs with variants | U+1EA40 + inventory row |
| **Semaron** | the Vylarian alphabet, majuscule and minuscule, first hand Kuriale | left to right | derived from Thuravark, rounded by reed and quill; its own system, not Pirzath Hand's look | in progress | U+F0200 planned |

Scripts that are not here are varieties of one of these fonts. They write with the same glyphs, perhaps with a few additions or different sound values, as many tongues share the Latin alphabet:

- **Tharavarkon and Thurarth** are varieties of Thuravark.
- **Okhatha-zethu and Merazan** are varieties of Qalezu.
- **Veldikko** is a variety of Semaron.

Fonts still to come are Helónika, Teng Chou, Vedyakshara and Ch'alish P'ilam. Each is an issue in this repository.

## The repository

| Path | Holds |
| --- | --- |
| `sources/<Font>.ufo` | The source of each font: outlines, cmap, metrics, `features.fea`, GDEF categories and glyph order. The UFO is the source of truth. |
| `fonts/<Font>-Regular.ttf` and `.woff2` | The built fonts, committed. CI rebuilds them and fails if they differ. |
| `specimens/<font>/` | The specimen sheets. |
| `design/<font>.md` | The design note, present tense: the system, the letters, the typing, the rounds. |
| `tools/<font>/` | `check_font.py`, `guard.py` and `specimens.py` for each font, plus any encoding table such as `encoding.json`. |
| `tools/render.py`, `tools/prove_guards.py`, `tools/notdef_box.py`, `tools/apply_notdef_box.py` | Shared tools. `render.py` sets shaped text in a font for specimens. `prove_guards.py` proves each guard fails a broken font. `notdef_box.py` is the box guard, and `apply_notdef_box.py` writes the box into a UFO. |
| `build.sh` | Builds every font, reproducibly. |
| `nogit/` | Generators and scratch. Not committed. |

### The toolchain

Tool versions are pinned in `requirements.txt` (fontTools, fontmake, ufoLib2, skia-pathops, uharfbuzz, Pillow, brotli, PyYAML). Create `.venv` from it. Use `rsvg-convert` to render SVG sheets.

`build.sh` runs fontmake on each UFO and compresses the WOFF2:

```sh
export SOURCE_DATE_EPOCH=1767225600
fontmake -u sources/<Font>.ufo -o ttf --keep-overlaps --no-production-names \
    --output-path fonts/<Font>-Regular.ttf
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

## Who does what

| Work | Who | Why |
| --- | --- | --- |
| Letter design: the system, the letterforms | Fable, which may look at its own renders | Its letter design is the strongest, and the owner prefers it. It is expensive, so give it drawing only. |
| Figurative signs (hieroglyphs, picture-glyphs, icons) | Opus, looking at its own renders | Pictures must be judged by eye. Opus drawing with eyes produced the accepted hieroglyphs; Fable drawing blind produced crude sketches. |
| Plumbing: UFO, `features.fea`, encoding, build, checks, guard, specimens, CI, design note | Sonnet | Mechanical, and checkable by the gates. |
| Inventories (what a script writes) | Sonnet, report only | Derived from canon; the owner rules on it. |

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

The method that produced an approved written hand. Pirzath Hand followed it, and Semaron follows it with its own look.

### The system comes first

Write the system as named constants at the top of the generator, and build every letter from them, never freehand:

- **Heights.** The body (consonant) height, the vowel height if vowels are smaller, the ascender and the descender. **No letter is taller than 1.2× the body.** Tall ascenders, such as the 2.2× of a Latin school cursive, do not suit these scripts.
- **One slant.** It is 12° for both Pirzath Hand and Semaron.
- **One pen.** Pirzath Hand uses a pointed pen with a gentle swell (thin 26, thick 48 on a 1000 em with body 400): heavy on falling strokes, light on rising strokes and turns, following the real stroke direction. A broad-nib chancery pen with real contrast is a different, equally valid choice.
- **Shapes.** One oval (a width : height ratio, its axis at the slant), one arch and one bowl (halves of the oval), and three or four standard letter widths.
- **One entry, one exit and one join,** at fixed angles. Pirzath Hand exits at 30° and enters at 50°. The join between them is one concave curve, so it never lines up with the stroke it feeds.
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
- **Families share parts exactly.**
  - g and gh are one drawing, and gh adds the strike.
  - kh and gh carry the same strike, in the same place.
  - A quotation mark is the g drawing plus two parallel lines.
  - m and n are mirrors.
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

Pirzath Carved and Thuravark Runic are drawn as tool marks, not pen strokes:

- **Strokes.** A cut is a straight groove, full width in the middle and tapering to a point at each end, or a drilled octagonal dot. A glyph is the union of its cuts.
- **Orientation.** No cut runs along the line, because the stone splits along the grain. The one exception is the sentence end. Arms follow a small set of fixed slopes; Thuravark has exactly two.
- **Proportions.** Consonants are larger than vowels, so the skeleton is read first on worn stone. Pirzath Carved uses a 520 × 700 box at weight 104 for consonants, and 300 × 440 at weight 82 for vowels.
- **Spacing.** Derive it from the outlines: measure each glyph's left and right profile in bands, and set kerning so every pair has the same optical gap. Thuravark's staves carry their own room, so it has no kerning.

## Figurative scripts: the hieroglyphs

Khelathi Zethu was drawn by Opus, looking at its renders, in batches of 30–50 signs. The batches shared a drawing library: `lib.py` holds the parts model, the stroker, the figure canon and the kits. Each group of signs is a module under `signs/`.

- **Silhouettes, not stick figures.** Every sign is a closed silhouette traced by a hairline, 1.5% of the quadrat (stroked at 15 units on a 1000 em). Fine interior detail uses the same weight. Solid fill only where it means something. A skeleton drawn with a fat pen looks like a child's drawing.
- **One proportion canon** for every figure: profile head, frontal eye and shoulders, legs in profile, and one head-to-body ratio. Shared kits (head, hands, feet, torso, garments, beasts, birds, props) keep the figures consistent. Never change a kit's output for signs already drawn without re-rendering and comparing them.
- **Variants.** Each sign has two or three: `.a` the full form, `.b` a quicker cut, `.c` a changed attribute. A variant is the same sign, never a different subject.
- **Coverage comes from scenes.** Write the scenes canon describes (a hunt, a harvest, a decree), list the signs each needs, and set a sample inscription for each. Spelling signs ensure any name can be written.
- **Layout is the build's job, not the font's.** Stacking signs into quadrats and drawing the royal-name oval around a name are layout, done by the specimen tool and by package-build, because renderers apply font composition rules inconsistently.
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

Notes write names in the setting's Latin spelling. A left-to-right script font draws that spelling through its own GSUB rules:

- digraphs to one glyph;
- an acute to the long-vowel mark;
- doubled letters to the doubling mark;
- `!` and `¡` to the imperative;
- `?`, `;` and `:` to the box, as every other character the typing does not use (see [For every font](#for-every-font)).

Passages switch to the script by font alone, and the text stays plain, searchable Latin.

Each script also has its own **private-use block** in plane 15, for typing script directly with a keyboard layout:

| Block | Script |
| --- | --- |
| U+F0000 | Pirzath (Carved and Hand share it) |
| U+F0100 | Thuravark |
| U+F0200 | Semaron |

### Right-to-left scripts

Latin forced right to left with the bidi override characters works, but HarfBuzz reverses a run whose direction opposes its script before GSUB runs. Every digraph rule then needs a reversed copy (`rtla`), which is fragile. So the right-to-left scripts use their own code points instead:

- **The blocks.** They are **unassigned code points whose default bidi class is R**:
  - Qalezu: U+1EA00–U+1EA3F, and its catch-before forms U+1ECC0–U+1ECFF;
  - Khelathi Zethu: U+1EA40–U+1EC6F.

  Text in them runs right to left natively in Chrome, Foundry and Typst, mixed with English, digits included.
- **The table.** One file per font, `tools/<font>/encoding.json`, holds glyph, code point, sound and Latin typing. The keyboard layout and package-build's converter read it too.
- **Converting the notes.** The build converts a note's Latin spelling to these code points. The converter applies the script's rules: no vowels, a word-initial vowel becomes the catch, a catch before a consonant is written over that consonant as its catch-before form, digraphs become one sign, doubling marks a doubled consonant. `tools/qalezu/guard.py` holds the reference converter.
- **No marks on these code points.** Chrome shapes script-less right-to-left code points in reverse order, so a combining mark attaches to the wrong sign. Precompose instead: Qalezu gives each doubled consonant its own code point, with the bar drawn in, and each consonant a catch-before code point, with three dabs drawn over it.
- **Variants** use only context-free substitutions: `ss01` and `ss02` single substitutions, and an alternate substitution in `salt`.

### For every font

- **Every character the script does not use prints a visible box.** Stray characters in a text must be obvious. The box is the glyph `notdef.box`, a copy of `.notdef` with the same outline and advance, and every font maps to it every code point of these ranges that its typing does not use:
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

| Check | What it proves |
| --- | --- |
| `tools/<font>/check_font.py` | The cmap matches the encoding; the name table carries the OFL; every glyph has outlines; marks have zero advance; features reach every variant; every unused character maps to the box. Runs in CI. |
| `tools/notdef_box.py` | Every code point of the Latin and punctuation ranges is mapped, and every one the typing does not use is on `notdef.box`, never glyph 0. Runs in CI. |
| `tools/<font>/guard.py` | Shapes every lexicon form, or every sample inscription, through the built font with uharfbuzz and asserts the right glyphs and neither `.notdef` nor the box. It reads thalorna's lexicon from a local checkout, so it does not run in CI, where thalorna is private. |
| `tools/prove_guards.py` | Each guard fails a deliberately broken font: a sign removed from the cmap, GSUB stripped, or the box guard's question mark unmapped or put on glyph 0. A guard that cannot fail proves nothing. |
| `tools/<font>/specimens.py` | Renders the sheets in `specimens/<font>/`. Look at every page. |
| CI (`.gitea/workflows/ci.yml`) | Builds every font, runs each `check_font.py`, and fails if the committed fonts differ from the build. Also runs the hooks, the attribution check and the TODO check. |

## Delivering the fonts

Readers install nothing.

- **Web.** The site serves each font as WOFF2 through `@font-face`, and a script span carries the font's class.
- **Foundry VTT.** The package ships the font files and registers them in its stylesheet, or through `CONFIG.fontDefinitions`, so every client loads them. Foundry v14's ProseMirror editor keeps `dir`, `class`, `lang`, `style` and invisible control characters through a save, but strips `<bdo>` and `<bdi>` to bare text. Never emit those two elements.
- **PDF (Typst).** Typst embeds the font in the PDF.
  - A right-to-left block uses `#set text(dir: rtl)`.
  - Typst honours RLI, RLO, PDF and PDI only when they sit in the same text element as the run.
  - Typst has no vertical writing mode, so the build stacks a column's signs itself.
- **Right-to-left blocks** use a right-to-left container (`dir="rtl"`) for alignment, in every target.
- **Columns** (the temple hieroglyphs) use `writing-mode: vertical-rl` with `text-orientation: upright` in HTML. The royal-name oval is drawn by the build around a name's signs.
- **One build rule for every target.** package-build marks text as a script, sets it in the script's font, converts right-to-left scripts to their code points, and lays out quadrats and columns.
- **Licence.** The OFL lets a font be embedded in pages, documents and books, and bundled with software, without that work taking on the font's licence.

## Working with the owner

- **Publish pilots and rounds on a page,** with the owner's sketch beside each glyph where one exists.
- **Read marked-up screenshots literally.** Circles mark faults; green lines show the intended stroke. Look at the screenshot itself.
- **Fix the system, not the instance.** One reported fault usually stands for a family, so apply the fix to every member.
- **Write each ruling into the design note,** and into the packet for any later batch, so later rounds cannot drift from it.
