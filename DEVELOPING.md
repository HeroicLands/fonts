# Developing the fonts

How the fonts are built, checked and published. Users of the fonts want [the README](README.md).

## Code point blocks

Every script draws on a block of code points of its own, and every face of a script draws its script's block: Pirzath Carved, Pirzath Hand and Pirzath Hand Lifted share the Pirzath block, so changing the face changes only the look. The blocks are registered in `BLOCKS` in `tools/codepoint_order.py`; `tools/codepoints.py` checks that every face's code points lie in its registered blocks, that no two blocks overlap, and that this table is the registry's.

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
| U+100000–U+10FFFD | Plane 16, unassigned                                                                                                            | –             |

- **Left-to-right scripts** (Pirzath, Thuravark, Semaron, Helónika, Vedyakshara) sit in plane 15, the Supplementary Private Use Area-A, whose characters are left to right by default. Each takes 256 code points. U+F0500 to U+F0FFF is reserved for the remaining alphabets and syllabaries, 256 code points each as they are assigned. Teng Chou takes U+F1000 to U+F2FFF: its characters from U+F1000, one per morpheme in the order they are added so that none is renumbered, its Jurthati syllabary from U+F2000, and the rest reserved. Teng Chou is written in columns; its characters are left to right where an inline span sets them along a line.
- **Right-to-left scripts** (Qalezu, Khelathi Zethu Glyphs and Veldikko) sit in unassigned code points of plane 1 whose default bidi class is right to left. That is why their text runs right to left in any editor, browser or typesetter, mixed with English and with no controls. Because the code points are unassigned rather than private, Unicode could in principle assign them to a script later. Qalezu takes U+1EA00 to U+1EA3F for its signs, doubled consonants, digits and punctuation. Khelathi Zethu Glyphs takes U+1EA40 to U+1EC6F with U+1E960 to U+1E9FF as overflow, 720 code points together. Veldikko takes U+1ED50 to U+1EDFF: its letters from U+1ED50, its vowel marks from U+1ED70 and its signs of length, pitch, emphasis and doubling from U+1ED78.
- **Plane 16** is unassigned.

## Package contents and the manifest

The fonts are published to npm as `@heroiclands/fonts`. The package holds each font as WOFF2 and TrueType, `fonts.css` with one `@font-face` rule and one `hl-<font>` class per family, `fonts.json`, the manifest of the families, `keyboards/`, the keyboard layouts, Emacs input methods and cheatsheets for typing in them, and `charts/`, the cheatsheet of each font.

`fonts.json` states, for each entry, its `name` (unique across the manifest), its `family` (the font-family), its `hl-<font>` class, its `files`, its `direction`, its OpenType `features` and its `codepoints`: every character the font draws, each with its code point, character name where the script's name table gives one, glyph name and kind, and for a sign of Khelathi Zethu Glyphs the sign id that types it; that font's format controls are of kind `control`. The class sets the family's `font-family`, `font-feature-settings` and, for a right-to-left family, `direction`. Pirzath Hand's joined form needs `ss01`, which its class turns on; Pirzath Hand Lifted is the same font with `ss01` turned off. Thuravark Carved Bound is Thuravark Carved with `ss01` turned on, which binds common pairs of staves on one stem.

A note's text in one of these fonts is the font's own code points. They are typed with the keyboard layouts in `keyboards/`, or produced by a mapping in the consuming build.

The fonts are licensed under the SIL Open Font License 1.1, which `LICENSE` carries in the package.

## Helonika Book

**Helonika Book.** It is the book hand of the Helónika, the alphabet of Helionis: upright geometric capitals, the inscription brought onto the page, over a round broad-pen minuscule of its own, written left to right with a flat reed. It is written on code points of its own, U+F0300 to U+F03FF: the twenty-four letters in both cases, _ē_ and _ō_ among them, the _kh_ and _zh_ letters, the long _ā_, _ī_ and _ū_ with their length bar, the ten digits, the raised dot that ends a sentence, the register-mark, and the accent, a mark that stands over the vowel before it. An accent after anything else is the box. thalorna's `helonika` mapping note writes Helonic's roman spelling in these characters. `tools/helonika/encoding.json` is the one table of the code points; `design/helonika.md` gives the system.

## Vedyakshara Classical

**Vedyakshara Classical.** It is the classical hand of the Vedyari syllabary: every sign hangs from a headline, so a line of Vedyari reads as a rope with the words strung beneath it, written left to right with a steep square-cut reed. It is written on code points of its own, U+F0400 to U+F04FF: each consonant carries the vowel _a_; another vowel follows it as a vowel sign, a flag above the headline or a hook below the sign; and the cut after a consonant takes the vowel away. The font draws the rest from those characters: a consonant with the cut before another as its half form or, for the nineteen commonest pairs, as one fused sign, before _r_ with the r-foot, and at the end of a word as its final form, the headline turned down; _pa_ with the soft dot as _fa_. thalorna's `vedyakshara` mapping note writes Vedyari's roman spelling in these characters. `tools/vedyakshara/encoding.json` is the one table of the code points; `design/vedyakshara.md` gives the system.

## Veldikko

**Veldikko.** It is the starlight-hand of the Sinale, in which both the Sinale and the Áelendi write: a flowing calligraphy written right to left, its letters joined by hairlines along the line and its vowel marks floating above, in one face for both tongues. It is written on code points of its own, U+1ED50 to U+1EDFF: a letter, then the length bar if the consonant is doubled, then each vowel mark, each followed by its signs of length, pitch and emphasis. The font joins each letter to its neighbours, folds a vowel and its signs into one mark and stands the marks over their letter. Its bowls stand at the x-height Semaron Kuriale and Latin text stand at, and its risers and tails reach well beyond, so a block of Veldikko wants a line height of about 2.4 em from the page's style sheet; a Veldikko word inside an English line leaves the line spacing even. `tools/veldikko/encoding.json` is the one table of what each code point is, and `tools/veldikko/convert.mjs` turns romanized Sinale into those code points; `design/veldikko.md` gives the system.

## Keyboard layouts

A note records Unicode characters, so typing in these fonts needs a keyboard layout that produces their code points. HL Semaron, HL Pirzath, HL Thuravark, HL Qalezu, HL Veldikko, HL Vedyakshara and HL Helónika type by sound: every sound of thalorna's spelling guide, _Pronouncing Thalorna_, sits on one key or chord, and that key is the same in every layout. Each layout types its script's own characters for the sound, exactly as the script's mapping note spells it, so one key may type several code points: in HL Semaron, `a` types U+F0230, Shift+A U+F0200, Option+T (_th_) U+F0250 and Option+C (_ch_) U+F0241 U+F0240 U+F0236. A key whose sound the script does not write types nothing in that layout, and no key types a roman letter, except the keys of markup described below. A script's faces share its code points, so the Pirzath layout types Pirzath Carved, Pirzath Hand and Pirzath Hand Lifted alike.

[`keyboards/index.md`](keyboards/index.md) is the shared cheatsheet: a diagram of the shared keys on an ANSI keyboard, the principles of the key map, and a table of every key or chord, its sound and each script's output as glyphs, code points and character names. Every script in `SCRIPTS` in `tools/keyboards.py` also gets its own self-contained cheatsheet, `keyboards/<script>.md` with a printable `keyboards/<script>.svg` and `.png` that draw each key's character on the plain, Shift, Option and Option+Shift layers in the script's own glyphs; adding a script to `SCRIPTS` and regenerating writes its sheet. `tools/keyboards_guard.py` fails when a key a layout types has no row on its sheet or no entry on its picture, or the row lists other code points.

**The key map.** Letters sit on their roman keys and capitals on Shift. A consonant pair sits on Option and its first letter (Option+T _th_, Option+C _ch_), with _ny_ on Option+Y and _ts_ on Option+X. An acute vowel sits on Option and its vowel. The vowel pairs sit on Option and the digit row: the long vowels _aa ee ii oo uu_ on 1 to 5, then _ai au ei oi ou_ on 6 to 0, and _ie uo ae ea_ on `-`, `=`, `[` and `]`. The diaeresis vowels sit on Option and `;`, `'`, `,`, `.` and `/`. The catch is `'`, the stop `.`, the pause `,`, and the open and close quotes Shift+`,` and Shift+`.`, the keys of `<` and `>`; only Pirzath writes quotation marks, so those keys type nothing in the other layouts. Digits sit on the digit row, and Pirzath's numerals ten to fifteen on Shift+2 to Shift+7. A capital is always Shift and its small sound's key: Option+Shift+T is _Th_.

**Signs.** Six Veldikko signs are not sounds, so they sit on keys of their own and type in HL Veldikko alone, as the quote keys do outside Pirzath: the carrier on `x`, and on Option the long sign on `L`, the bar of a doubled consonant on `W`, the rise on `R`, the fall on `F` and the emphasis on `M`. In the other layouts those keys type nothing. A long vowel or a diphthong typed from its Option key already carries its length mark, and a doubled consonant is typed with the bar after it. The Helónika's register-mark sits on Option+Shift+R and types in HL Helónika alone.

**Markup types itself.** In every layout on every platform, the characters Markdown and a span's `[text]{font=…}` need type themselves, as plain ASCII, at their U.S. positions: `` * _ [ ] { } ( ) = : | \ ~ ` ``. A note's markup is written without switching layouts, and no script draws it. `#` is not among them, because Shift+3 is Pirzath's numeral eleven. In Emacs the backslash key is the prefix of the Option chords, so a backslash is typed twice.

**Where the outputs come from.** `tools/sound_keys.json` puts each sound on its key and states the principles. `keyboards/sounds.json` gives each sound's output in each script; `tools/sounds.mjs` writes it by running each sound's spelling through the seven mapping notes on thalorna's `origin/main` (`Lore/Scripts/Semaron_Spelling.md`, `Pirzath_Spelling.md`, `Thuravark_Spelling.md`, `Qalezu_Spelling.md`, `Veldikko_Spelling.md`, the Sinale map, `Vedyakshara_Spelling.md` and `Helonika_Spelling.md`) with package-build's own mapping rules, the ones a run marked `map=` is set by; `--map-note <script>=<file>` reads one note from a file instead. A vowel is spelled inside a word, between two _t_'s, and _y_ before an _a_, where it is the glide; so a vowel in Qalezu, which writes consonants only, types nothing. HL Veldikko types a vowel as its mark over a consonant, with no carrier; the carrier has a key of its own. In HL Vedyakshara a consonant is spelled before an _a_, so its key types the bare consonant, which carries _a_; the _a_ key types nothing, another vowel key types its vowel sign, and a capital vowel types the vowel's own sign. Vedyari writes no catch, and its mapping note writes an apostrophe as the cut, so `'` types the cut: _Suryadvar_ is typed S, u, r, `'`, y, a, d, `'`, v, a, r, `'`. HL Helónika types Helonic as its mapping note spells it: Option+8 (_ei_) types _ē_ and Option+0 (_ou_) _ō_, Option+T types _th_, and Option+K types _k_ and _h_, since Helonic writes _kh_ as two letters. `tools/keyboards.py` writes the layouts from those two files, and the fonts build needs no thalorna checkout:

```sh
node tools/sounds.mjs --thalorna ~/dev/HeroicLands/thalorna --write
.venv/bin/python tools/keyboards.py
```

**What a platform cannot carry.** A Windows layout types at most four UTF-16 code units from one key, the limit Microsoft Keyboard Layout Creator puts on a ligature, so Semaron's _ch_ and _Ch_, three plane-15 characters each, type nothing on Windows. An XKB key types one keysym, so every sound a script writes with more than one code point types nothing on Linux. macOS and Emacs carry every output. The cheatsheet lists each of these keys.

## Cheatsheets

Each font has a cheatsheet of every character it draws, in `charts/`; [`charts/index.md`](charts/index.md) links them all. A sheet holds two views:

- **A code chart**, laid out like Unicode's charts: columns headed by the code point without its last hex digit, rows `0` to `F`, each cell holding the glyph above its code point, and a code point the font does not draw hatched. The grid runs left to right in every font. A long range is split into pages of eight columns, and a column with no character is left out.
- **A table** of Character Name, Character, Code Point (`U+05DC`), Entity (`&#1500;`) and Hex Entity (`&#x05DC;`), in code point order and grouped by kind.

The glyphs are outlines taken from the font, so a sheet reads without the font installed: `charts/<face folder>/chart-<n>.svg` and `.png` are the chart pages, `charts/<face folder>/glyphs/U+XXXX.svg` is one glyph for the table, and `charts/<face folder>.md` embeds both. Pirzath Hand Lifted is drawn with `ss01` off, and Thuravark Carved Bound with it on. Character names are Unicode-style (uppercase ASCII letters, digits, spaces and hyphens) and come from `tools/names/<script>.json`, one JSON object per script of `"U+XXXX": "NAME"` pairs, which `tools/write_css.py` writes into `fonts.json`. A script without that file has no names, and its table shows an empty Character Name cell. Khelathi Zethu Glyphs names a sign `ZETHU CHARACTER <n>`, where n is its code point's position in the font's code point space: U+1EA40 is `ZETHU CHARACTER 001`, and the overflow block U+1E960 to U+1E9FF continues after the main block. A format control takes Unicode's name at its Unicode code point, `EGYPTIAN HIEROGLYPH VERTICAL JOINER`, and the font's own at its twin, `ZETHU VERTICAL JOINER`. `tools/zethu_names.py` writes `tools/names/zethu.json`, so drawing a sign renames no other.

## Setting up

The font toolchain runs on **Python 3.13**. Python 3.15 corrupts long drawing runs, so a virtual environment is never built on it. Install the dependencies, which also activates the repository's git hooks:

```sh
npm ci
```

Create the virtual environment:

```sh
python3.13 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

The source of each font is a UFO under `sources/`: `PirzathCarved.ufo`, `PirzathHand.ufo`, `ThuravarkCarved.ufo`, `QalezuHand.ufo`, `KhelathiZethuGlyphs.ufo`, `SemaronKuriale.ufo`, `TengChou.ufo`, `Veldikko.ufo`, `VedyaksharaClassical.ufo` and `HelonikaBook.ufo`. Open one in FontForge, Glyphs or RoboFont to edit it. `TengChou.ufo` is generated from its data by `tools/teng-chou/build_ufo.py`: an edit to a Teng Chou character belongs in `tools/teng-chou/`, and the script is run after it, before the build. `Veldikko.ufo` is generated the same way by `tools/veldikko/build_ufo.py`, from the letters and the joining in `tools/veldikko/`, `VedyaksharaClassical.ufo` by `tools/vedyakshara/build_ufo.py`, from the signs in `tools/vedyakshara/`, and `HelonikaBook.ufo` by `tools/helonika/build_ufo.py`, from the letters in `tools/helonika/`. The UFO carries the outlines, the character map, the metrics and `features.fea`, which holds every OpenType feature. Every glyph's advance is its ink width plus one sidebearing a side, the same across its face; `tools/respace.py` sets a UFO to that rule, and `design/making-fonts.md` gives each face's sidebearing.

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

Check the built fonts, render the specimens, and prove that each guard fails a broken font:

```sh
.venv/bin/python tools/pirzath/check_font.py
.venv/bin/python tools/pirzath-hand/check_font.py
.venv/bin/python tools/thuravark-carved/check_font.py
.venv/bin/python tools/qalezu-hand/check_font.py
.venv/bin/python tools/khelathi-zethu-glyphs/check_font.py
.venv/bin/python tools/semaron-kuriale/check_font.py
.venv/bin/python tools/teng-chou/check_font.py
.venv/bin/python tools/veldikko/check_font.py
.venv/bin/python tools/veldikko/guard.py --fixtures-only   # the converter's fixtures join and carry their marks
.venv/bin/python tools/vedyakshara/check_font.py
.venv/bin/python tools/vedyakshara/guard.py --fixtures-only
.venv/bin/python tools/helonika/check_font.py
.venv/bin/python tools/helonika/guard.py --fixtures-only
.venv/bin/python tools/pirzath/guard.py --fixtures-only        # each lexicon guard's fixtures, written as tools/mapped.json records them
.venv/bin/python tools/pirzath-hand/guard.py --fixtures-only
.venv/bin/python tools/thuravark-carved/guard.py --fixtures-only
.venv/bin/python tools/qalezu-hand/guard.py --fixtures-only
.venv/bin/python tools/semaron-kuriale/guard.py --fixtures-only
.venv/bin/python tools/teng-chou/syllabary_distinct.py   # the Jurthati signs stay distinct at body size
.venv/bin/python tools/teng-chou/stroke_mix.py   # every character's body is strokes, dabs a minority
.venv/bin/python tools/notdef_box.py
.venv/bin/python tools/vertical.py
.venv/bin/python tools/spacing.py                 # every face is set at a natural spacing; --report prints the measures
.venv/bin/python tools/font_names.py
.venv/bin/python tools/codepoints.py              # each face draws its own code points and states no spelling
.venv/bin/python tools/keyboards_guard.py --fixtures-only   # the layouts type each sound's output, and nothing else
.venv/bin/python tools/charts_guard.py            # every character is on its sheet; unnamed rows are listed
.venv/bin/python tools/khelathi-zethu-glyphs/quadrats.py   # quadrats and cartouches land where the layout puts them
.venv/bin/python tools/codepoints_chart.py         # specimens/<face>/codepoints.png
.venv/bin/python tools/pirzath/specimens.py       # specimens/pirzath/
.venv/bin/python tools/pirzath-hand/specimens.py  # specimens/pirzath-hand/
.venv/bin/python tools/thuravark-carved/specimens.py     # specimens/thuravark-carved/
.venv/bin/python tools/qalezu-hand/specimens.py        # specimens/qalezu-hand/
.venv/bin/python tools/khelathi-zethu-glyphs/specimens.py         # specimens/khelathi-zethu-glyphs/
.venv/bin/python tools/khelathi-zethu-glyphs/paint_guard.py       # every drawn sign has a paint map
.venv/bin/python tools/semaron-kuriale/specimens.py     # specimens/semaron-kuriale/
.venv/bin/python tools/teng-chou/character_specimens.py   # specimens/teng-chou/characters.png
.venv/bin/python tools/teng-chou/character_specimens.py --name syllabary.png
.venv/bin/python tools/teng-chou/text_specimen.py     # specimens/teng-chou/text.png, text-vertical.png and tally.png
.venv/bin/python tools/veldikko/font_sheets.py        # specimens/veldikko/forms.png, joined.png, verse.png, sizes.png and beside.png
.venv/bin/python tools/vedyakshara/font_sheets.py     # specimens/vedyakshara/text.png
.venv/bin/python tools/helonika/font_sheets.py        # specimens/helonika/text.png
.venv/bin/python tools/prove_guards.py
```

`tools/codepoints.py` is the code-point guard. Every face, shaped from its own code points, must yield exactly the glyphs `fonts.json` lists for them, and its cmap may map nothing else but the space (U+0020 and U+00A0), the default-ignorables and the box, so every other code point, Latin included, prints the box. No substitution may write a character it did not read: a face's substitutions are its contextual forms and marks, never a spelling rule that turns one character into another. A few sequences that a spelling rule would rewrite, such as Pirzath's glide _y_ before a vowel pair and Semaron's _i_ twice, must shape as written.

Each lexicon guard shapes every form of its lexicon and asserts the font renders it rightly; the Pirzath guards read the Khazari lexicon, the Thuravark guard the Nordmal one, Semaron Kuriale's the Vylari one, Qalezu's the Khelathi one, Vedyakshara Classical's the Vedyari one, Helonika Book's the Helonic and Valtari ones, Teng Chou's the Tantsou one (each form cut into morphemes and set one character to each, along a line and down a column), and Veldikko's converts the Sinale lexicon through `tools/veldikko/convert.mjs` and asserts each letter's form and where each mark stands. The Semaron, Pirzath, Thuravark, Qalezu, Vedyakshara and Helónika guards first write each form in the script's code points by its mapping note on thalorna's `origin/main` (`assets/content/Lore/Scripts/<Script>_Spelling.md`), with package-build's own mapping rules, through `tools/mapping.mjs` under `node`; `--map-note FILE` reads the note from a file instead. Each reads its lexicon from the `origin/main` of a local thalorna checkout, `~/dev/HeroicLands/thalorna` by default:

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
```

The guards' fixtures, and the sample lines of the specimens that `tools/spacing.py` measures, are written once through the mapping notes into `tools/mapped.json`, so that `--fixtures-only`, `tools/prove_guards.py` and `tools/spacing.py` need no thalorna checkout. `tools/mapped.py` writes the file, and without `--write` checks it against thalorna's mapping notes and lists every text they now write differently:

```sh
.venv/bin/python tools/mapped.py --thalorna /path/to/thalorna --write
.venv/bin/python tools/mapped.py --thalorna /path/to/thalorna
```

The specimens of the Semaron, Pirzath and Thuravark faces and of Qalezu Hand write their roman texts through the same mapping notes, so they take `--thalorna` too.

`tools/keyboards_guard.py` checks the key map (no key or chord carries two sounds, every sound has a key, a capital sits on Shift and its small sound's key) and reads every layout and input method back: each key must type exactly the code points `keyboards/sounds.json` gives its sound in the script, or nothing where the script does not write the sound or the platform cannot carry it, and no key may type a character below U+0080. Without `--fixtures-only` it also writes `keyboards/sounds.json` afresh from thalorna's mapping notes, through `tools/sounds.mjs` under `node`, and fails where the committed file differs.

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

## README samples

`tools/readme_samples.py` writes the one-line sample image of each font that the README shows, to `specimens/readme/`. It runs in `build.sh`. A font added to `fonts.json` gets its sample on the next build; the README then needs one row in its table.
