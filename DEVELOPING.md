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

The fonts are published to npm as `@heroiclands/fonts`. The package holds each font as WOFF2 and TrueType, `fonts.css` with one `@font-face` rule and one `hl-<font>` class per family, `fonts.json`, the manifest of the families, `keyboards/`, the keyboard layouts, Emacs input methods and cheatsheets for typing in them, and `charts/`, the cheatsheet of each font.

`fonts.json` states, for each entry, its `name` (unique across the manifest), its `family` (the font-family), its `hl-<font>` class, its `files`, its `direction`, its OpenType `features` and its `codepoints`: every character the font draws, each with its code point, character name where the script's name table gives one, glyph name and kind, and for a sign of Khelathi Zethu Glyphs the sign id that types it; that font's format controls are of kind `control`. The class sets the family's `font-family`, `font-feature-settings` and, for a right-to-left family, `direction`. Pirzath Hand's joined form needs `ss01`, which its class turns on; Pirzath Hand Lifted is the same font with `ss01` turned off. Thuravark Carved Bound is Thuravark Carved with `ss01` turned on, which binds common pairs of staves on one stem.

A note's text in one of these fonts is the font's own code points. They are typed with the keyboard layouts in `keyboards/`, or produced by an [encoding](#encodings).

The fonts are licensed under the SIL Open Font License 1.1, which `LICENSE` carries in the package.

## Helonika Book

**Helonika Book.** It is the book hand of the Helónika, the alphabet of Helionis: upright geometric capitals, the inscription brought onto the page, over a round broad-pen minuscule of its own, written left to right with a flat reed. It is written on code points of its own, U+F0300 to U+F03FF: the twenty-four letters in both cases, _ē_ and _ō_ among them, the _kh_ and _zh_ letters, the long _ā_, _ī_ and _ū_ with their length bar, the ten digits, the raised dot that ends a sentence, the register-mark, and the accent, a mark that stands over the vowel before it. An accent after anything else is the box. the `helonika` encoding writes Helonic's roman spelling in these characters. `tools/helonika/encoding.json` is the one table of the code points; `design/helonika.md` gives the system.

## Vedyakshara Classical

**Vedyakshara Classical.** It is the classical hand of the Vedyari syllabary: every sign hangs from a headline, so a line of Vedyari reads as a rope with the words strung beneath it, written left to right with a steep square-cut reed. It is written on code points of its own, U+F0400 to U+F04FF: each consonant carries the vowel _a_; another vowel follows it as a vowel sign, a flag above the headline or a hook below the sign; and the cut after a consonant takes the vowel away. The font draws the rest from those characters: a consonant with the cut before another as its half form or, for the nineteen commonest pairs, as one fused sign, before _r_ with the r-foot, and at the end of a word as its final form, the headline turned down; _pa_ with the soft dot as _fa_. the `vedyakshara` encoding writes Vedyari's roman spelling in these characters. `tools/vedyakshara/encoding.json` is the one table of the code points; `design/vedyakshara.md` gives the system.

## Veldikko

**Veldikko.** It is the starlight-hand of the Sinale, in which both the Sinale and the Áelendi write: a flowing calligraphy written right to left, its letters joined by hairlines along the line and its vowel marks floating above, in one face for both tongues. It is written on code points of its own, U+1ED50 to U+1EDFF: a letter, then the length bar if the consonant is doubled, then each vowel mark, each followed by its signs of length, pitch and emphasis. The font joins each letter to its neighbours, folds a vowel and its signs into one mark and stands the marks over their letter. Its bowls stand at the x-height Semaron Kuriale and Latin text stand at, and its risers and tails reach well beyond, so a block of Veldikko wants a line height of about 2.4 em from the page's style sheet; a Veldikko word inside an English line leaves the line spacing even. `tools/veldikko/encoding.json` is the one table of what each code point is, and `encodings/veldikko.json` writes romanized Sinale in those code points; `design/veldikko.md` gives the system.

## Chalish Pilam Common

**Chalish Pilam Common.** It is the common hand of Ch'alish P'ilam, the Ki'ich'chik writing: a logographic script in which each glyph is a concept, drawn in one even line, written left to right and read two glyphs to a row down a column. Every glyph takes one fixed advance, a square cell and a gutter either side, so a column two advances wide wraps a run into rows of two by ordinary line breaking; the font does nothing else to place them. It has no keyboard layout: glyphs are inserted from [the chart](charts/chalish-pilam.md). It is written on code points of its own, U+F3000 to U+F3FFF: the numbers from zero (the shell) and the places of the count first, then the glyphs, each after the last in the order it is added, so no glyph is renumbered. `tools/chalish-pilam/encoding.json` is the one table of the code points and `design/chalish-pilam.md` gives the system. The font carries meaning, not spelling, so it has no encoding: `tools/chalish-pilam/build_ufo.py` writes its UFO, and `tools/chalish_names.py` writes its character names from `encoding.json`.

## Chalish Pilam Ceremonial

**Chalish Pilam Ceremonial.** It is the ceremonial hand of Ch'alish P'ilam, carved and painted: concept glyphs, numbers and syllable signs, composed into blocks of a main sign and at most two affixes and read in paired columns. The font lays out a block from two invisible joiners typed between its glyphs, U+F4FF0 to set two items side by side and U+F4FF1 to stack the first over the second, picking each sign's form for its place by GSUB. A sign takes its block's advance, its footprint's width and a gutter either side, and an affix in a block takes none. It is written on code points of its own, U+F4000 to U+F4FFF: the numbers and the places of the count from U+F4000, the concept glyphs from U+F4020, the syllable signs from U+F4400 and the joiners at U+F4FF0. Zero and the places of the count have code points and no drawing, so they print the box. `tools/chalish-pilam/ceremonial_encoding.json` is the one table of the code points and `design/chalish-pilam.md` gives the system. `tools/chalish-pilam/build_ceremonial_ufo.py` writes its UFO, `tools/chalish-pilam/ceremonial_codage.py` writes its encoding, `encodings/chalish-ceremonial.json`, and `tools/chalish_names.py` writes its character names. It has no keyboard layout: blocks are typed through the encoding, or glyphs inserted from [the chart](charts/chalish-pilam-ceremonial.md).

## Encodings

An encoding is `encodings/<name>.json`: the `name`, the `fonts` it serves (slugs of `fonts.json`), `"extends": "standard"`, `accepts`, the characters it accepts as roman (a list of characters and ranges such as `"a-z"`: a caseless script lists `a-z` and its own additions, Semaron and Helónika list `a-z` and `A-Z`), the `vowels` that `before: vowel` tests, the `rows` as `[roman, code points]` or `{from, to, before?, at?}`, and optionally per-face `faces`, and optionally a `codage`, the name of the codage file that reads what lies between the literal immutable markers `⟦` and `⟧`. A codage is a file in `encodings/` with `"kind": "codage"`, taking only `name`, `kind`, `fonts` and `rows`; it extends nothing, is reached only through the encoding that states it, and `names()` lists it apart (`names(kind="codage")`). Zethu and Ch'alish are scripts whose roman is written by other encoders, so their encodings accept no letters and read codes between the markers. `encode.py` documents the format and the rules, applies an encoding in either direction, and is the only implementation; it needs Python 3.9 or later and the standard library alone, and ships in the npm package beside `encodings/`. Every encoding is documented in `encodings/<name>.md`.

**The standard roman encoding**, `encodings/standard.json`, is the base every encoding extends: a file of `name` and `rows` alone, holding the roman punctuation every language shares (`.` `?` `!` `!!` `,` `«` `»` `‹` `›` `—` `…` `/` `//` `***` `{` `}`), each written as the invisible mark of its own characters; it has no row for whitespace. Outside the markers any run of space, tab, newline and carriage return is one word separator, which `encode.py` handles before any row applies and writes as the encoding's required `separator` (`" "`, or `""` for a script with no spaces); decoding writes one space. An encoding's rows are the standard's rows whose `from` it does not state, in the standard's order, then its own. So a script that draws a standard mark states a row for it, drawing its glyph (with the mark of its `from` and the end mark where an earlier row draws the same glyph, as Semaron's five sentence marks share its point), and a script that does not draw it states nothing and keeps the standard's invisible mark, which is then the same in every encoding. A row of its own that repeats the standard's is a guard finding. **The literal immutable markers** `⟦` `⟧` (U+27E6, U+27E7) work in every encoding, and are handled by `encode.py` before any row applies. Each is written as the mark of itself. Between them the text is a list of codes separated by whitespace. With no `codage` a code is a character's name with spaces written `_`: `encodings/names.json` names the script fonts' characters (written by `python3 tools/encoding_names.py` from `tools/names/*.json`, and checked by the guard, because `tools/` does not ship), and `unicodedata` names every other. A space between codes writes nothing, and decoding separates codes with single spaces. With `"codage": "<name>"` the span is encoded and decoded by that encoding, which has no codage of its own; `chalish-common` and `zethu-mdc` are codages and name themselves. No row may state a marker. A name that names no character, an unmatched marker and a nested one are refused at their position. `tools/encodings_guard.py` proves, in every encoding, that spans round-trip among other text and write the same marker marks, and builds a script beside each codage to prove a stated one. The standard is documented in `encodings/standard.md`, with the meaning of each mark from `tools/encoding_docs.json`.

**A character no row matches is refused.** `encode.encode` and `encode.decode` raise `EncodingError` at the character's line and column, and `encode.py` prints it as `file:line:column: error:` (the `--file` path, `<stdin>` or `<text>`) and exits 1. Only a tool that sets such characters in a font on purpose, to see the box, keeps them: `encode.pieces(..., strict=False)`, which `tools/encoded.py` uses and reports in each record's `unencoded`.

To add or change an encoding, edit its JSON (the Ch'alish, Teng Chou and Zethu codages and script encodings are written by `tools/chalish-pilam/codage.py`, `tools/chalish-pilam/ceremonial_codage.py --write`, `tools/teng-chou/codage.py` and `tools/khelathi-zethu-glyphs/encoding_file.py`, so change their sources), then run, in order:

```sh
python3 tools/encoding_vectors.py --write   # encodings/vectors.json
python3 tools/encoding_docs.py              # encodings/<name>.md
python3 tools/encodings_guard.py            # the guard
python3 -m unittest tools/encode_test.py    # the format's own tests
```

A new encoding also gets an entry in `tools/encoding_docs.json`: a `title`, an `intro`, an `example` roman text, and for an encoding too large to read as one table, `"summary": true` with a `structure` that explains how its rows are built.

- **The guard**, `tools/encodings_guard.py`, checks that every file is well formed, extends the standard and serves faces of `fonts.json`; that every row and every sample text round-trips; that every standard mark round-trips alone and inside a sentence, and that a mark the script does not draw writes the standard's invisible mark, so its sequence is identical in every encoding; that a character outside an encoding is refused at its line and column, in encoding and in decoding; and that `vectors.json` is the one `tools/encoding_vectors.py` writes. It runs on the standard library alone.
- **The vectors**, `encodings/vectors.json`, give roman and Unicode pairs for every encoding. A row's vector is the first text found in which the row applies, the standard's rows included; the sample texts are those of `tools/sample_texts.json` and the Khelathi Zethu scenes of `tools/khelathi-zethu-glyphs/samples.json`. A sample holding a character outside the encoding is `{"roman", "refused": [line, column]}`. Another implementation tests itself against them.
- **The pages**, `encodings/<name>.md` and `encodings/standard.md`, are written by `tools/encoding_docs.py` from the JSON and the authored text in `tools/encoding_docs.json`; each encoding's page shows how its script writes every standard mark, and `--check` fails where one is out of date. A summarised page lists the single-character rows and a few longer ones, because a table of every row is too long to read.
- **The tools** reach an encoding through `tools/encoded.py`, which names the encoding each face is written by.

## Keyboard layouts

A note records Unicode characters, so typing in these fonts needs a keyboard layout that produces their code points. HL Semaron, HL Pirzath, HL Thuravark, HL Qalezu, HL Veldikko, HL Vedyakshara and HL Helónika type by sound: every sound of thalorna's spelling guide, _Pronouncing Thalorna_, sits on one key or chord, and that key is the same in every layout. Each layout types its script's own characters for the sound, exactly as the script's encoding spells it, so one key may type several code points: in HL Semaron, `a` types U+F0230, Shift+A U+F0200, Option+T (_th_) U+F0250 and Option+C (_ch_) U+F0241 U+F0240 U+F0236. A key whose sound the script does not write types nothing in that layout, and no key types a roman letter, except the keys of markup described below. A script's faces share its code points, so the Pirzath layout types Pirzath Carved, Pirzath Hand and Pirzath Hand Lifted alike.

[`keyboards/index.md`](keyboards/index.md) is the shared cheatsheet: a diagram of the shared keys on an ANSI keyboard, the principles of the key map, and a table of every key or chord, its sound and each script's output as glyphs, code points and character names. Every script in `SCRIPTS` in `tools/keyboards.py` also gets its own self-contained cheatsheet, `keyboards/<script>.md` with a printable `keyboards/<script>.svg` and `.png` that draw each key's character on the plain, Shift, Option and Option+Shift layers in the script's own glyphs; adding a script to `SCRIPTS` and regenerating writes its sheet. `tools/keyboards_guard.py` fails when a key a layout types has no row on its sheet or no entry on its picture, or the row lists other code points.

**The key map.** Letters sit on their roman keys. A capital sits on Shift and the key of its small sound, and a pair's capital on Option+Shift: Shift+A is _A_, Option+Shift+T is _Th_. Only Semaron Kuriale and Helónika have case, so a capital types its majuscule in HL Semaron and HL Helónika and nothing in the caseless layouts. A consonant pair sits on Option and its first letter (Option+T _th_, Option+C _ch_), with _ny_ on Option+Y and _ts_ on Option+X. An acute vowel sits on Option and its vowel. The vowel pairs sit on Option and the digit row: the long vowels _aa ee ii oo uu_ on 1 to 5, then _ai au ei oi ou_ on 6 to 0, and _ie uo ae ea_ on `-`, `=`, `[` and `]`. The diaeresis vowels sit on Option and `;`, `'`, `,`, `.` and `/`. The catch is `'`, the stop `.`, the pause `,`, and the open and close quotes Shift+`,` and Shift+`.`, the keys of `<` and `>`; only Pirzath writes quotation marks, so those keys type nothing in the other layouts. Digits sit on the digit row, and Pirzath's numerals ten to fifteen on Shift+2 to Shift+7.

**Signs.** Six Veldikko signs are not sounds, so they sit on keys of their own and type in HL Veldikko alone, as the quote keys do outside Pirzath: the carrier on `x`, and on Option the long sign on `L`, the bar of a doubled consonant on `W`, the rise on `R`, the fall on `F` and the emphasis on `M`. In the other layouts those keys type nothing. A long vowel or a diphthong typed from its Option key already carries its length mark, and a doubled consonant is typed with the bar after it. The Helónika's register-mark sits on Option+Shift+R and types in HL Helónika alone.

**Markup types itself.** In every layout on every platform, the characters Markdown and a span's `[text]{font=…}` need type themselves, as plain ASCII, at their U.S. positions: `` * _ [ ] { } ( ) = : | \ ~ ` ``. A note's markup is written without switching layouts, and no script draws it. `#` is not among them, because Shift+3 is Pirzath's numeral eleven. In Emacs the backslash key is the prefix of the Option chords, so a backslash is typed twice.

**Where the outputs come from.** `tools/sound_keys.json` puts each sound on its key and states the principles. `keyboards/sounds.json` gives each sound's output in each script; `tools/sounds.py` writes it by running each sound's spelling through the seven encodings `encodings/semaron.json`, `pirzath.json`, `thuravark.json`, `qalezu.json`, `veldikko.json`, `vedyakshara.json` and `helonika.json` with `encode.py`; `--encoding <script>=<file>` reads one encoding from a file instead. A vowel is spelled inside a word, between two _t_'s, and _y_ before an _a_, where it is the glide; so a vowel in Qalezu, which writes consonants only, types nothing. HL Veldikko types a vowel as its mark over a consonant, with no carrier; the carrier has a key of its own. In HL Vedyakshara a consonant is spelled before an _a_, so its key types the bare consonant, which carries _a_; the _a_ key types nothing, and another vowel key types its vowel sign. Vedyari writes no catch, and its encoding writes an apostrophe as the cut, so `'` types the cut: _suryadvar_ is typed s, u, r, `'`, y, a, d, `'`, v, a, r, `'`. HL Helónika types Helonic as its encoding spells it: Option+8 (_ei_) types _ē_ and Option+0 (_ou_) _ō_, Option+T types _th_, and Option+K types _k_ and _h_, since Helonic writes _kh_ as two letters. The letters no sound key types are signs of HL Helónika: Option+Q and Option+J type the _kh_ and _zh_ letters, Option+V, Option+`and C the barred _aa_, _ii_ and _uu_, each capital on Shift, and Option+Shift+M the accent.`tools/keyboards.py` writes the layouts from those two files, and the fonts build needs no thalorna checkout:

```sh
python3 tools/sounds.py --write
.venv/bin/python tools/keyboards.py
```

**What a platform cannot carry.** A Windows layout types at most four UTF-16 code units from one key, the limit Microsoft Keyboard Layout Creator puts on a ligature, so Semaron's _ch_ and _Ch_, three plane-15 characters each, type nothing on Windows. An XKB key types one keysym, so every sound a script writes with more than one code point types nothing on Linux. macOS and Emacs carry every output. The cheatsheet lists each of these keys.

## Cheatsheets

Each font has a cheatsheet of every character it draws, in `charts/`; [`charts/index.md`](charts/index.md) links them all. A sheet holds two views:

- **A code chart**, laid out like Unicode's charts: columns headed by the code point without its last hex digit, rows `0` to `F`, each cell holding the glyph above its code point, and a code point the font does not draw hatched. The grid runs left to right in every font. A long range is split into pages of eight columns, and a column with no character is left out.
- **A table** of Character Name, Character, Code Point (`U+05DC`), Entity (`&#1500;`) and Hex Entity (`&#x05DC;`), in code point order and grouped by kind.

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

The source of each font is a UFO under `sources/`: `PirzathCarved.ufo`, `PirzathHand.ufo`, `ThuravarkCarved.ufo`, `QalezuHand.ufo`, `KhelathiZethuGlyphs.ufo`, `SemaronKuriale.ufo`, `TengChou.ufo`, `ChalishPilamCommon.ufo`, `ChalishPilamCeremonial.ufo`, `Veldikko.ufo`, `VedyaksharaClassical.ufo` and `HelonikaBook.ufo`. Open one in FontForge, Glyphs or RoboFont to edit it. `TengChou.ufo` is generated from its data by `tools/teng-chou/build_ufo.py`: an edit to a Teng Chou character belongs in `tools/teng-chou/`, and the script is run after it, before the build. `Veldikko.ufo` is generated the same way by `tools/veldikko/build_ufo.py`, from the letters and the joining in `tools/veldikko/`, `VedyaksharaClassical.ufo` by `tools/vedyakshara/build_ufo.py`, from the signs in `tools/vedyakshara/`, `HelonikaBook.ufo` by `tools/helonika/build_ufo.py`, from the letters in `tools/helonika/`, `PirzathHand.ufo` by `tools/pirzath-hand/build_ufo.py`, from the signs in `tools/pirzath-hand/`, and `ChalishPilamCeremonial.ufo` by `tools/chalish-pilam/build_ceremonial_ufo.py`, from the drawings and block layout in `tools/chalish-pilam/`; `tools/chalish-pilam/build_ceremonial.sh` regenerates it and compiles the font alone. The UFO carries the outlines, the character map, the metrics and `features.fea`, which holds every OpenType feature. Every glyph's advance is its ink width plus one sidebearing a side, the same across its face; `tools/respace.py` sets a UFO to that rule, and `design/making-fonts.md` gives each face's sidebearing.

Build the fonts into `fonts/`. The build is reproducible, so the committed fonts match a fresh build byte for byte:

```sh
PATH=.venv/bin:$PATH ./build.sh
```

`build.sh` runs `fontmake` and compresses the `.woff2`, once per font (`PirzathCarved` shown), adding Khelathi Zethu Glyphs' quadrat layout between the two with `tools/khelathi-zethu-glyphs/layout.py`, then runs `tools/write_css.py`, which writes `fonts.css` and `fonts.json` from the built fonts' name tables and one table of per-family facts. `tools/keyboards.py` then writes `keyboards/` from `tools/sound_keys.json` and `keyboards/sounds.json` (see [Keyboard layouts](#keyboard-layouts)). `tools/charts.py` last writes `charts/` from `fonts.json` and the built fonts, and rasterizes the chart pages with `resvg-py`, pinned in `requirements.txt`:

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

`tools/check.py` holds the one table of checks: each built font's own font check, lexicon guard on its fixtures and other guards, and the checks that read every font (`tools/notdef_box.py`, `tools/vertical.py`, `tools/spacing.py`, `tools/font_names.py`, `tools/codepoints.py`, `tools/keyboards_guard.py`, `tools/charts_guard.py`, `tools/sample_texts.py`, `tools/encodings_guard.py --require-fonts` and `tools/specimen_pages.py --check`). Each font's part of `tools/prove_guards.py` runs as its own command, `--font fonts/<Family>-Regular.ttf`, and the rest as `--shared`. CI runs the script as its check step. It refuses to run when a built font has no entry, when an entry has no built font, or when a font check, guard or distinctness check under `tools/` is in no command, so a new font or a new check is added to its table and nowhere else. Each check also runs alone, as its command in the table.

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

Each lexicon guard shapes every form of its lexicon and asserts the font renders it rightly; the Pirzath guards read the Khazari lexicon, the Thuravark guard the Nordmal one, Semaron Kuriale's the Vylari one, Qalezu's the Khelathi one, Vedyakshara Classical's the Vedyari one, Helonika Book's the Helonic and Valtari ones, Teng Chou's the Tantsou one (each form cut into morphemes and set one character to each, along a line and down a column), and Veldikko's encodes the Sinale lexicon and asserts each letter's form and where each mark stands. The Semaron, Pirzath, Thuravark, Qalezu, Vedyakshara, Veldikko and Helónika guards first write each form in the script's code points by its encoding (`encodings/<name>.json`) with `encode.py`; `--encoding FILE` applies an encoding file instead. Each reads its lexicon from the `origin/main` of a local thalorna checkout, `~/dev/HeroicLands/thalorna` by default:

```sh
.venv/bin/python tools/pirzath/guard.py --thalorna /path/to/thalorna
.venv/bin/python tools/pirzath-hand/guard.py --thalorna /path/to/thalorna
.venv/bin/python tools/thuravark-carved/guard.py --thalorna /path/to/thalorna
.venv/bin/python tools/qalezu-hand/guard.py --thalorna /path/to/thalorna
.venv/bin/python tools/semaron-kuriale/guard.py --thalorna /path/to/thalorna
.venv/bin/python tools/teng-chou/guard.py --thalorna /path/to/thalorna
.venv/bin/python tools/veldikko/guard.py --thalorna /path/to/thalorna
.venv/bin/python tools/vedyakshara/guard.py --thalorna /path/to/thalorna
.venv/bin/python tools/helonika/guard.py --thalorna /path/to/thalorna
# a bare --encoding FILE is helonika=FILE
.venv/bin/python tools/helonika/guard.py --note Bizarian.md --note Bethuan.md --encoding bizarian=helonika-bizarian.json --encoding bethuan=helonika-bethuan.json   # a pull request's own language notes and encodings
```

The guards use the standard roman punctuation: Semaron draws `.` `?` `!` `!!` and `,` as its point, Pirzath, Thuravark, Helónika, Qalezu and Vedyakshara draw `.` `?` `!` and `!!` as their sentence end, Pirzath writes its quotation pair from `«` `»` and `‹` `›`, and Qalezu its verse dot from `/` and `//`; each script's other standard marks shape to nothing. Characters outside the encoding, such as `;`, `:` and the English quotation marks, are negative fixtures: the guard sets them in the font, where they draw the box, so a row restored for one fails the guard; a capital is one of them in every caseless script, since a caseless script accepts only lowercase roman. Semaron and Helónika have case, and their guards set capitals as positive fixtures. Semaron also checks Vylari `à`, including the catch on the preceding ancient stop in `kàralzon` and `kàrthorgila`, its zero advance and its placement on the native base. Other tongues' catch inputs remain separate shared-map fixtures; they do not authorize apostrophes in Vylari.

The guards' fixtures, and the sample lines of the specimens that `tools/spacing.py` measures, are written through the encodings, so that `--fixtures-only`, `tools/prove_guards.py` and `tools/spacing.py` need no thalorna checkout. `tools/sample_texts.json` lists every roman text they write, and the sample texts of `encodings/vectors.json` come from it; `tools/sample_texts.py` checks the file against the fixtures and sample lines, and `--write` rewrites it:

```sh
.venv/bin/python tools/sample_texts.py --write
.venv/bin/python tools/sample_texts.py
```

The specimens of the Semaron, Pirzath and Thuravark faces and of Qalezu Hand write their roman texts through the same encodings.

`tools/keyboards_guard.py` checks the key map (no key or chord carries two sounds, every sound has a key, a capital sits on Shift and the key of its small sound) and reads every layout and input method back: each key must type exactly the code points `keyboards/sounds.json` gives its sound in the script, or nothing where the script does not write the sound or the platform cannot carry it, and no key may type a character below U+0080. It also writes `keyboards/sounds.json` afresh from the encodings, through `tools/sounds.py`, and fails where the committed file differs.

```sh
.venv/bin/python tools/keyboards_guard.py --thalorna /path/to/thalorna
```

Qalezu's character map, its doubled and catch-before composites and the `rlig` substitution that draws a catch and its sign as the catch-before form follow from `encoding.json`; after editing that file, `.venv/bin/python tools/qalezu-hand/apply_encoding.py` rewrites them in the UFO, and `--check` reports a disagreement.

Khelathi Zethu Glyphs is the temple hieroglyphs of the Khelathi, on U+1EA40 to U+1EC6F and written right to left. Its guard reads no lexicon: it shapes the sample inscriptions kept in `tools/khelathi-zethu-glyphs/samples.json`.

```sh
.venv/bin/python tools/khelathi-zethu-glyphs/guard.py
```

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

Each font has a specimen page, `specimens/<class>.md`, that shows the script at work: its letters, a sample of its marks on a few letters, and a passage of thalorna in the script, its lines numbered, with each line's English and its roman spelling under it. Teng Chou and Khelathi Zethu Glyphs show a sample of their characters and link the full chart, and Khelathi Zethu Glyphs shows the Khelathu banner with its English text in place of a passage. Chalish Pilam Common and Chalish Pilam Ceremonial record meaning rather than spelling, so their pages show the committed sheets of `specimens/chalish-pilam/`, written by the hand's own sheet tools, and list their passage line by line. `tools/specimen_pages.py` renders the images into `specimens/pages/` from the built fonts, shaping every line with HarfBuzz, writes the pages, and writes each font's Sample cell in the README; a README it rewrites wants `npm run format` to align the table. The texts are `specimens/texts.json`: each font's source note and, for each line, its code points, roman spelling and English. They are written once from a thalorna checkout, each roman line through the script's encoding (`--encoding SCRIPT=FILE` applies a file instead), and every roman and English line must stand in its source note as written; the passages chosen are in `PASSAGES` in the tool. Building the pages needs no thalorna checkout:

```sh
.venv/bin/python tools/specimen_pages.py --write-texts --thalorna /path/to/thalorna
.venv/bin/python tools/specimen_pages.py            # the pages, their images and the README cells
.venv/bin/python tools/specimen_pages.py --check    # fails on a missing or out-of-date page, image or README cell
```

Both scripts run in `build.sh`. A font added to `fonts.json` gets its sample on the next build; the README then needs one row in its table, and `PASSAGES` an entry for its page. The pages and their images are not in the npm package; the README on npm links to them on GitHub.
