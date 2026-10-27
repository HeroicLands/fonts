# Developing the fonts

How the fonts are built, checked and published. Users of the fonts want [the README](README.md).

## Code point blocks

Every script draws on a block of code points of its own, and every face of a script draws its script's block: Pirzath Carved and Pirzath Hand share the Pirzath block, so changing the face changes only the look. The blocks are registered in `BLOCKS` in `tools/codepoint_order.py`; `tools/codepoints.py` checks that every face's code points lie in its registered blocks, that no two blocks overlap, and that this table is the registry's.

| Range             | Use                                                                                                                             | Direction     |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------- | ------------- |
| U+13430–U+1343F   | Egyptian Hieroglyph Format Controls, Unicode's own: Khelathi Zethu Glyphs' quadrat and cartouche controls                       | left to right |
| U+1E960–U+1E9FF   | Khelathi Zethu Glyphs, overflow beyond its main block                                                                           | right to left |
| U+1EA00–U+1EA3F   | Qalezu: signs, digits and punctuation                                                                                           | right to left |
| U+1EA40–U+1EC6F   | Khelathi Zethu Glyphs: signs, and its format controls at U+1EC60–U+1EC6F                                                        | right to left |
| U+1ED50–U+1EDFF   | Veldikko: letters, vowel marks and the signs of length, pitch, emphasis and doubling                                            | right to left |
| U+F0000–U+F00FF   | Pirzath                                                                                                                         | left to right |
| U+F0100–U+F01FF   | Thuravark                                                                                                                       | left to right |
| U+F0200–U+F02FF   | Semaron                                                                                                                         | left to right |
| U+F0300–U+F03FF   | Helónika: capitals, small letters, the kh and zh letters, long vowels, digits, the raised dot, the register-mark and the accent | left to right |
| U+F0400–U+F04FF   | Vedyakshara: consonants, independent vowels, vowel signs, the cut, the soft dot, digits and bars                                | left to right |
| U+F0500–U+F0FFF   | Reserved for the remaining alphabets and syllabaries, 256 code points each as they are assigned                                 | left to right |
| U+F1000–U+F1FFF   | Teng Chou: characters, one per morpheme, in the order they are added                                                            | left to right |
| U+F2000–U+F20FF   | Teng Chou: the Jurthati syllabary                                                                                               | left to right |
| U+F2100–U+F2FFF   | Reserved for Teng Chou                                                                                                          | left to right |
| U+F3000–U+F3FFF   | Chalish Pilam Common: the numbers and the places of the count, then the glyphs, in the order they are added                     | left to right |
| U+F4000–U+F4FFF   | Chalish Pilam Ceremonial: the numbers, the concept glyphs, the syllable signs from U+F4400 and the joiners at U+F4FF0           | left to right |
| U+100000–U+10FFFD | Plane 16, unassigned                                                                                                            | –             |

- **Left-to-right scripts** (Pirzath, Thuravark, Semaron, Helónika, Vedyakshara) sit in plane 15, the Supplementary Private Use Area-A, whose characters are left to right by default. Each takes 256 code points. U+F0500 to U+F0FFF is reserved for the remaining alphabets and syllabaries, 256 code points each as they are assigned. Teng Chou takes U+F1000 to U+F2FFF: its characters from U+F1000, one per morpheme in the order they are added so that none is renumbered, its Jurthati syllabary from U+F2000, and the rest reserved. Teng Chou is written in columns; its characters are left to right where an inline span sets them along a line.
- **Right-to-left scripts** (Qalezu, Khelathi Zethu Glyphs and Veldikko) sit in unassigned code points of plane 1 whose default bidi class is right to left. That is why their text runs right to left in any editor, browser or typesetter, mixed with English and with no controls. Because the code points are unassigned rather than private, Unicode could in principle assign them to a script later. Qalezu takes U+1EA00 to U+1EA3F for its signs, doubled consonants, digits and punctuation. Khelathi Zethu Glyphs takes U+1EA40 to U+1EC6F with U+1E960 to U+1E9FF as overflow, 720 code points together. Veldikko takes U+1ED50 to U+1EDFF: its letters from U+1ED50, its vowel marks from U+1ED70 and its signs of length, pitch, emphasis and doubling from U+1ED78.
- **Plane 16** is unassigned.

## Package contents and the manifest

The fonts are published to npm as `@heroiclands/fonts`. The package holds each font as WOFF2 and TrueType, `fonts.css` with one `@font-face` rule and one `hl-<font>` class per family, `fonts.json`, the manifest of the families, and `charts/`, the cheatsheet of each font.

`fonts.json` states, for each entry, its `name` (unique across the manifest), its `family` (the font-family), its `hl-<font>` class, its `files`, its `direction`, its OpenType `features` and its `codepoints`: every character the font draws, each with its code point, character name where the script's name table gives one, [glyph code](#glyph-codes), glyph name and kind; Khelathi Zethu Glyphs' format controls are of kind `control`. The class sets the family's `font-family`, `font-feature-settings` and, for a right-to-left family, `direction`. Pirzath Hand's joined form needs `ss01`, which its class turns on; Pirzath Hand Lifted is the same font with `ss01` turned off. Thuravark Carved Bound is Thuravark Carved with `ss01` turned on, which binds common pairs of staves on one stem.

Text in one of these fonts is the font's own code points, inserted from the charts. How a language is written in a font belongs to the thalorna repository, which names each character by its glyph code.

The fonts are licensed under the SIL Open Font License 1.1, which `LICENSE` carries in the package.

## Helonika Book

**Helonika Book.** It is the book hand of the Helónika, the alphabet of Helionis: upright geometric capitals, the inscription brought onto the page, over a round broad-pen minuscule of its own, written left to right with a flat reed. It is written on code points of its own, U+F0300 to U+F03FF: the twenty-four letters in both cases, _ē_ and _ō_ among them, the _kh_ and _zh_ letters, the long _ā_, _ī_ and _ū_ with their length bar, the ten digits, the raised dot that ends a sentence, the register-mark, and the accent, a mark that stands over the vowel before it. An accent after anything else is the box. `tools/helonika/encoding.json` is the one table of the code points; `design/helonika.md` gives the system.

## Vedyakshara Classical

**Vedyakshara Classical.** It is the classical hand of the Vedyari syllabary: every sign hangs from a headline, so a line of Vedyari reads as a rope with the words strung beneath it, written left to right with a steep square-cut reed. It is written on code points of its own, U+F0400 to U+F04FF: each consonant carries the vowel _a_; another vowel follows it as a vowel sign, a flag above the headline or a hook below the sign; and the cut after a consonant takes the vowel away. The font draws the rest from those characters: a consonant with the cut before another as its half form or, for the nineteen commonest pairs, as one fused sign, before _r_ with the r-foot, and at the end of a word as its final form, the headline turned down; _pa_ with the soft dot as _fa_. `tools/vedyakshara/encoding.json` is the one table of the code points; `design/vedyakshara.md` gives the system.

## Veldikko

**Veldikko.** It is the starlight-hand of the Sinale, in which both the Sinale and the Áelendi write: a flowing calligraphy written right to left, its letters joined by hairlines along the line and its vowel marks floating above, in one face for both tongues. It is written on code points of its own, U+1ED50 to U+1EDFF: a letter, then the length bar if the consonant is doubled, then each vowel mark, each followed by its signs of length, pitch and emphasis. The font joins each letter to its neighbours, folds a vowel and its signs into one mark and stands the marks over their letter. Its bowls stand at the x-height Semaron Kuriale and Latin text stand at, and its risers and tails reach well beyond, so a block of Veldikko wants a line height of about 2.4 em from the page's style sheet; a Veldikko word inside an English line leaves the line spacing even. `tools/veldikko/encoding.json` is the one table of what each code point is; `design/veldikko.md` gives the system.

## Chalish Pilam Common

**Chalish Pilam Common.** It is the common hand of Ch'alish P'ilam, the Ki'ich'chik writing: a logographic script in which each glyph is a concept, drawn in one even line, written left to right and read two glyphs to a row down a column. Every glyph takes one fixed advance, a square cell and a gutter either side, so a column two advances wide wraps a run into rows of two by ordinary line breaking; the font does nothing else to place them. Glyphs are inserted from [the chart](charts/chalish-pilam.md). It is written on code points of its own, U+F3000 to U+F3FFF: the numbers from zero (the shell) and the places of the count first, then the glyphs, each after the last in the order it is added, so no glyph is renumbered. `tools/chalish-pilam/encoding.json` is the one table of the code points and `design/chalish-pilam.md` gives the system. `tools/chalish-pilam/build_ufo.py` writes its UFO, and `tools/chalish_names.py` writes its character names from `encoding.json`.

## Chalish Pilam Ceremonial

**Chalish Pilam Ceremonial.** It is the ceremonial hand of Ch'alish P'ilam, carved and painted: concept glyphs, numbers and syllable signs, composed into blocks of a main sign and at most two affixes and read in paired columns. The font lays out a block from two invisible joiners typed between its glyphs, U+F4FF0 to set two items side by side and U+F4FF1 to stack the first over the second, picking each sign's form for its place by GSUB. A sign takes its block's advance, its footprint's width and a gutter either side, and an affix in a block takes none. It is written on code points of its own, U+F4000 to U+F4FFF: the numbers and the places of the count from U+F4000, the concept glyphs from U+F4020, the syllable signs from U+F4400 and the joiners at U+F4FF0. Zero and the places of the count have code points and no drawing, so they print the box. `tools/chalish-pilam/ceremonial_encoding.json` is the one table of the code points and `design/chalish-pilam.md` gives the system. `tools/chalish-pilam/build_ceremonial_ufo.py` writes its UFO and `tools/chalish_names.py` writes its character names. Glyphs and joiners are inserted from [the chart](charts/chalish-pilam-ceremonial.md): a block is its glyphs with `JOINER_BESIDE` or `JOINER_STACK` between two of them.

## Glyph codes

Every character of every face has a code, a short name: a letter its name (`PARGH`, `CHEROLA_MIN`, `LONG_E_MAJ`), a vowel sign `SIGN_I`, a doubled letter `LAGUN_DBL`, a digit `DIGIT_ZERO`, a mark or a point what it does (`STOP`, `PAUSE`, `LONG`, `CATCH`, `JOINER_BESIDE`), a Khelathi Zethu Glyphs sign its sense (`SAIL`, `WEST`) and a Teng Chou character its morpheme (`HO`, `TENG`). A code matches `^[A-Za-z0-9_]+$`, is unique within its script and is case-sensitive: Teng Chou's `KA` and `ka` are two characters, a character and a syllable sign. A script's faces share its codes, as they share its code points.

`tools/codes/<script>.json` is the one table of a script's codes, a JSON object of `"U+XXXX": "CODE"` pairs beside `tools/names/<script>.json`. `tools/write_css.py` writes each code into `fonts.json`, and the charts show it. `tools/codes.py` reads the tables: `codes.text(script, "DALK A LADHAV KAMV")` gives the characters a sequence of codes names, with `U+XXXX` for a character the script has no code for, such as the space `U+0020`. `tools/codes_guard.py` checks that every character of every face has exactly one code, that the codes are well formed and unique within each face, that every code in a table belongs to a character a face draws, and that the codes the Khelathi Zethu Glyphs and Chalish Pilam Ceremonial build tables state agree with the tables. A character added to a face gets its code in the same change, or the guard fails.

## Cheatsheets

Each font has a cheatsheet of every character it draws, in `charts/`; [`charts/index.md`](charts/index.md) links them all. A sheet holds two views:

- **A code chart**, laid out like Unicode's charts: columns headed by the code point without its last hex digit, rows `0` to `F`, each cell holding the glyph above its code point, and a code point the font does not draw hatched. The grid runs left to right in every font. A long range is split into pages of eight columns, and a column with no character is left out.
- **A table** of Character Name, Code (the [glyph code](#glyph-codes)), Character, Code Point (`U+05DC`), Entity (`&#1500;`) and Hex Entity (`&#x05DC;`), in code point order and grouped by kind.

The glyphs are outlines taken from the font, so a sheet reads without the font installed: `charts/<face folder>/chart-<n>.svg` and `.png` are the chart pages, `charts/<face folder>/glyphs/U+XXXX.svg` is one glyph for the table, and `charts/<face folder>.md` embeds both. Pirzath Hand Lifted is drawn with `ss01` off, and Thuravark Carved Bound with it on. Character names are Unicode-style (uppercase ASCII letters, digits, spaces and hyphens) and come from `tools/names/<script>.json`, one JSON object per script of `"U+XXXX": "NAME"` pairs, which `tools/write_css.py` writes into `fonts.json`. A script without that file has no names, and its table shows an empty Character Name cell. Khelathi Zethu Glyphs names a sign `ZETHU CHARACTER <n>`, where n is its code point's position in the font's code point space: U+1EA40 is `ZETHU CHARACTER 001`, and the overflow block U+1E960 to U+1E9FF continues after the main block. A format control takes Unicode's name at its Unicode code point, `EGYPTIAN HIEROGLYPH VERTICAL JOINER`, and the font's own at its twin, `ZETHU VERTICAL JOINER`. `tools/zethu_names.py` writes `tools/names/zethu.json`, so drawing a sign renames no other.

## Setting up

The font toolchain runs on **Python 3.13**. Python 3.15 corrupts long drawing runs, so a virtual environment is never built on it. Install the dependencies, which also activates the repository's git hooks and installs Liberation Mono, the Latin face the sheets set beside each script (from `@betteroffice/fonts`):

```sh
npm ci
```

Create the virtual environment:

```sh
python3.13 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

The source of each font is a UFO under `sources/`: `PirzathCarved.ufo`, `PirzathHand.ufo`, `ThuravarkCarved.ufo`, `QalezuHand.ufo`, `KhelathiZethuGlyphs.ufo`, `SemaronKuriale.ufo`, `TengChou.ufo`, `ChalishPilamCommon.ufo`, `ChalishPilamCeremonial.ufo`, `Veldikko.ufo`, `VedyaksharaClassical.ufo` and `HelonikaBook.ufo`. Open one in FontForge, Glyphs or RoboFont to edit it. `TengChou.ufo` is generated from its data by `tools/teng-chou/build_ufo.py`: an edit to a Teng Chou character belongs in `tools/teng-chou/`, and the script is run after it, before the build. `SemaronKuriale.ufo` is generated by `tools/semaron-kuriale/build_ufo.py`, from the drawing kit `tools/semaron-kuriale/kit.py`: an edit to a Semaron letter belongs in the kit, and the script is run after it. `Veldikko.ufo` is generated the same way by `tools/veldikko/build_ufo.py`, from the letters and the joining in `tools/veldikko/`, `VedyaksharaClassical.ufo` by `tools/vedyakshara/build_ufo.py`, from the signs in `tools/vedyakshara/`, `HelonikaBook.ufo` by `tools/helonika/build_ufo.py`, from the letters in `tools/helonika/`, `PirzathHand.ufo` by `tools/pirzath-hand/build_ufo.py`, from the signs in `tools/pirzath-hand/`, and `ChalishPilamCeremonial.ufo` by `tools/chalish-pilam/build_ceremonial_ufo.py`, from the drawings and block layout in `tools/chalish-pilam/`; `tools/chalish-pilam/build_ceremonial.sh` regenerates it and compiles the font alone. The UFO carries the outlines, the character map, the metrics and `features.fea`, which holds every OpenType feature. Every glyph's advance is its ink width plus one sidebearing a side, the same across its face; `tools/respace.py` sets a UFO to that rule, and `design/making-fonts.md` gives each face's sidebearing.

Build the fonts into `fonts/`. The build is reproducible, so the committed fonts match a fresh build byte for byte:

```sh
PATH=.venv/bin:$PATH ./build.sh
```

`build.sh` runs `fontmake` and compresses the `.woff2`, once per font (`PirzathCarved` shown), adding Khelathi Zethu Glyphs' quadrat layout between the two with `tools/khelathi-zethu-glyphs/layout.py`, then runs `tools/write_css.py`, which writes `fonts.css` and `fonts.json` from the built fonts' name tables, the name and code tables and one table of per-family facts. `tools/charts.py` then writes `charts/` from `fonts.json` and the built fonts, and rasterizes the chart pages with `resvg-py`, pinned in `requirements.txt`:

```sh
export SOURCE_DATE_EPOCH=1767225600
fontmake -u sources/PirzathCarved.ufo -o ttf --keep-overlaps --no-production-names \
    --output-path fonts/PirzathCarved-Regular.ttf
fonttools ttLib.woff2 compress -o fonts/PirzathCarved-Regular.woff2 fonts/PirzathCarved-Regular.ttf
```

Check the package holds exactly what it should, and that the formatting is clean:

```sh
npm run check:package
npm run format:check
```

Check the built fonts and prove that each guard fails a broken font:

```sh
.venv/bin/python tools/check.py                              # every check, in parallel
.venv/bin/python tools/check.py --font ChalishPilamCeremonial  # one font's checks and proof
.venv/bin/python tools/check.py --list                       # the commands, run nothing
```

`tools/check.py` holds the one table of checks: each built font's own font check, its shaping guard and its other guards, and the checks that read every font (`tools/notdef_box.py`, `tools/vertical.py`, `tools/spacing.py`, `tools/font_names.py`, `tools/codepoints.py`, `tools/codes_guard.py`, `tools/charts_guard.py` and `tools/specimen_pages.py --check`). Each font's part of `tools/prove_guards.py` runs as its own command, `--font fonts/<Family>-Regular.ttf`, and the rest as `--shared`. CI runs the script as its check step. It refuses to run when a built font has no entry, when an entry has no built font, or when a font check, guard or distinctness check under `tools/` is in no command, so a new font or a new check is added to its table and nowhere else. Each check also runs alone, as its command in the table.

Render the specimens:

```sh
.venv/bin/python tools/codepoints_chart.py         # specimens/<face>/codepoints.png
.venv/bin/python tools/pirzath/specimens.py       # specimens/pirzath/
.venv/bin/python tools/pirzath-hand/strokes_sheet.py   # specimens/pirzath-hand/strokes.png, the strokes
.venv/bin/python tools/pirzath-hand/letter_sheets.py   # specimens/pirzath-hand/letters.png, the signs
.venv/bin/python tools/thuravark-carved/specimens.py     # specimens/thuravark-carved/
.venv/bin/python tools/qalezu-hand/specimens.py        # specimens/qalezu-hand/
.venv/bin/python tools/khelathi-zethu-glyphs/specimens.py         # specimens/khelathi-zethu-glyphs/
.venv/bin/python tools/semaron-kuriale/specimens.py     # specimens/semaron-kuriale/
.venv/bin/python tools/teng-chou/character_specimens.py   # specimens/teng-chou/characters.png
.venv/bin/python tools/teng-chou/character_specimens.py --name syllabary.png
.venv/bin/python tools/teng-chou/text_specimen.py     # specimens/teng-chou/text.png, text-vertical.png and tally.png
.venv/bin/python tools/chalish-pilam/strokes_sheet.py   # specimens/chalish-pilam/strokes.png
.venv/bin/python tools/chalish-pilam/glyphs_sheet.py    # specimens/chalish-pilam/glyphs.png
.venv/bin/python tools/chalish-pilam/font_sheets.py     # specimens/chalish-pilam/text.png
.venv/bin/python tools/chalish-pilam/ceremonial_sheet.py     # specimens/chalish-pilam/ceremonial.png
.venv/bin/python tools/chalish-pilam/ceremonial_passage.py   # specimens/chalish-pilam/ceremonial-passage.png
.venv/bin/python tools/veldikko/font_sheets.py        # specimens/veldikko/forms.png, joined.png, verse.png, sizes.png and beside.png
.venv/bin/python tools/vedyakshara/font_sheets.py     # specimens/vedyakshara/text.png
.venv/bin/python tools/helonika/font_sheets.py        # specimens/helonika/text.png
.venv/bin/python tools/pirzath-hand/font_sheets.py    # specimens/pirzath-hand/text.png
```

`tools/codepoints.py` is the code-point guard. Every face, shaped from its own code points, must yield exactly the glyphs `fonts.json` lists for them, and its cmap may map nothing else but the space (U+0020 and U+00A0), the default-ignorables and the box, so every other code point, Latin included, prints the box. No substitution may write a character it did not read: a face's substitutions are its contextual forms and marks, never a spelling rule that turns one character into another. A few sequences that a spelling rule would rewrite, such as Pirzath's glide _y_ before a vowel pair and Semaron's _i_ twice, must shape as written.

Each font's shaping guard, `tools/<font>/guard.py`, shapes the fixtures in its `fixtures.json` and asserts the glyphs the font gives them. A fixture is a sequence of the script's [glyph codes](#glyph-codes), with `U+XXXX` for a character the script has no code for, and the glyphs it must shape to, so a guard proves what the font draws from its code points and nothing about how a language is spelled. Pirzath Carved's and Pirzath Hand's fixtures cover the numerals, the quotation marks, the marks between words, the doubled letters, the diphthongs and the lost letters; Pirzath Hand's also seat the length mark above a vowel pair and leave the letters round a default-ignorable character as they are. Thuravark Carved's cover every stave, the numerals, the crowned names and the bound runes with `ss01` on and off, and its guard also checks a crowned name's rails and the stave design. Semaron Kuriale's cover both cases, the digraph letters, the long vowels and the catch on every kind of base, set as wide as the line without it. Qalezu Hand's, Vedyakshara Classical's and Helonika Book's also check each fixture against the face's rules for what its code points draw (`drawn`): Qalezu's catch-before forms, Vedyakshara's fused, half, final and r-foot forms and its vowel signs, and Helónika's accent; Helonika Book's `spaces` fixtures give the advance of each space. Veldikko's give the letter forms each place takes and where each mark stands. Teng Chou's guard sets its passages along a line and down a column, Chalish Pilam Common's sets its night entry and every glyph, and Khelathi Zethu Glyphs' sets the sample inscriptions kept in `tools/khelathi-zethu-glyphs/samples.json`.

```sh
.venv/bin/python tools/pirzath/guard.py
.venv/bin/python tools/veldikko/guard.py --font /path/to/Veldikko-Regular.ttf
```

The specimens set texts of the setting. The specimen sheets and `tools/spacing.py` take each text's code points from `tools/texts/<face>.json`, where each text is stored as its roman spelling and its sequence of glyph codes, so no tool reads a language or another repository.

Qalezu's character map, its doubled and catch-before composites and the `rlig` substitution that draws a catch and its sign as the catch-before form follow from `encoding.json`; after editing that file, `.venv/bin/python tools/qalezu-hand/apply_encoding.py` rewrites them in the UFO, and `--check` reports a disagreement.

Every drawn Zethu sign has a paint map in `tools/khelathi-zethu-glyphs/paint.json`: each enclosed region of the sign, named by a seed point in glyph units, and its colour category, such as `skin-male`, `linen` or `water`, so a banner, a stele or the book paints the sign the conventional way. `tools/khelathi-zethu-glyphs/paint.py` finds the regions and writes the painted contact sheets to `specimens/khelathi-zethu-glyphs/paint/`; a renderer imports it to find the same regions. `paint_guard.py` fails when a drawn sign has no map or a seed misses its region:

```sh
.venv/bin/python tools/khelathi-zethu-glyphs/paint_guard.py
.venv/bin/python tools/khelathi-zethu-glyphs/paint.py
```

**Quadrats and cartouches.** Khelathi Zethu Glyphs lays out quadrats and cartouches itself from format controls typed between its signs: the vertical and horizontal joiners, the four corner insertions, begin and end segment, and begin and end enclosure, the cartouche. Each control is mapped at its Unicode code point, U+13430 to U+1343D, and at the same offset from U+1EC60 in the font's own block; `tools/khelathi-zethu-glyphs/controls.json` lists them. Notes and text store the font's own controls, U+1EC60 to U+1EC6D, the recommended form. The font accepts the Unicode controls so that text pasted from standard Egyptian text shapes in HarfBuzz tools, but a browser shapes a run of one script at a time and the Unicode controls belong to the Egyptian script, so in a browser they fall out of the run of signs and the quadrat comes apart. In a page, text in the font needs no markup and no feature turned on:

```html
<span class="hl-khelathi-zethu-glyphs">&#x1EA41;&#x1EC60;&#x1EA42;</span>
```

sets sign 01-002 over sign 01-003. `build.sh` adds the layout to the built font with `tools/khelathi-zethu-glyphs/layout.py`, and `tools/khelathi-zethu-glyphs/quadrats.py` shapes the fixtures of `quadrats.json`, the samples written with joiners, runs of quadrats and a seeded sweep of random ones, and asserts where every sign lands. The layout works in a horizontal line; a column is laid out by the page. `design/khelathi-zethu-glyphs.md` gives the controls, the layout and its limits, and `specimens/khelathi-zethu-glyphs/quadrats/` shows them.

```sh
.venv/bin/python tools/khelathi-zethu-glyphs/quadrats.py
```

See `design/khelathi-zethu-glyphs.md`.

## Using the fonts from a program

**Foundry VTT.** A module ships the files it needs from its own folder, then registers each family either by importing `fonts.css` from its stylesheet or through `CONFIG.fontDefinitions`, so every client loads it:

```js
CONFIG.fontDefinitions["Pirzath Carved"] = {
  editor: true,
  fonts: [{ urls: ["modules/<module id>/fonts/PirzathCarved-Regular.woff2"] }],
};
```

**Typst.** Point the compiler's font path at the package's `fonts/` folder, and name the family in `#set text(font: "Qalezu Hand")`:

```sh
typst compile --font-path node_modules/@heroiclands/fonts/fonts book.typ
```

The jsDelivr form is `https://cdn.jsdelivr.net/npm/@heroiclands/fonts@<version>/<file>`. A rule's URLs are relative, so every file resolves beside the stylesheet.

## README samples and specimen pages

`tools/readme_samples.py` writes the one-line sample image of each font that the README shows, to `specimens/readme/`. The README names each image by its absolute URL on the GitHub mirror, `https://raw.githubusercontent.com/HeroicLands/fonts/main/specimens/readme/<class>.png`, because Gitea and npm resolve no relative image inside a table, and links it to the font's specimen page.

Each font has a specimen page, `specimens/<class>.md`, that shows the script at work: its letters, a sample of its marks on a few letters, and a passage of thalorna in the script, its lines numbered, with each line's English and its roman spelling under it. Teng Chou and Khelathi Zethu Glyphs show a sample of their characters and link the full chart, and Khelathi Zethu Glyphs shows the Khelathu banner with its English text in place of a passage. Chalish Pilam Common and Chalish Pilam Ceremonial record meaning rather than spelling, so their pages show the committed sheets of `specimens/chalish-pilam/`, written by the hand's own sheet tools, and list their passage line by line. `tools/specimen_pages.py` renders the images into `specimens/pages/` from the built fonts, shaping every line with HarfBuzz, writes the pages, and writes each font's Sample cell in the README; a README it rewrites wants `npm run format` to align the table. The texts are `specimens/texts.json`: each font's source note and, for each line, its glyph codes, roman spelling and English, as the source note writes them:

```sh
.venv/bin/python tools/specimen_pages.py            # the pages, their images and the README cells
.venv/bin/python tools/specimen_pages.py --check    # fails on a missing or out-of-date page, image or README cell
```

Both scripts run in `build.sh`. A font added to `fonts.json` gets its sample on the next build; the README then needs one row in its table, and `specimens/texts.json` an entry for its page. The pages and their images are not in the npm package; the README on npm links to them on GitHub.
