# @heroiclands/fonts

## 1.0.0

### Major Changes

- The fonts reach their first stable release. Within a major version a character keeps its code point, so text typed in these fonts keeps its meaning across updates.

### Minor Changes

- **Helonika Book** is a new font for the Helónika, the eastern alphabet of Helonic, Bizarian and Bethuan: upright geometric capitals over a round, flowing book minuscule.
- It has its own digits, the raised dot that ends a sentence, and an accent that sits over its vowel.
- The HL Helónika keyboard layout types it by sound on macOS, Windows, Linux and Emacs.
- **Vedyakshara Classical** is a new font for the Vedyari syllabary: every sign hangs from a headline, with half forms, fused clusters, final forms and vowel signs drawn as the text is typed.
- The HL Vedyakshara keyboard layout types it by sound on macOS, Windows, Linux and Emacs.

### Patch Changes

- Every keyboard layout has a printable cheatsheet: a picture of the keyboard showing the character each key types plain, with Shift, with Option (AltGr) and with both, and a table of each key's glyph, code points and name.
- The README walks through downloading a font, installing it and each keyboard layout on macOS, Windows and Linux, and using the fonts in Word, LibreOffice and Pages.
- Teng Chou and Khelathi Zethu Glyphs, which have no keyboard, are explained with how to insert their characters by code point.
- The README shows a sample of every font.
- Thuravark Carved writes the Tharavarkon, imperial Vylaria's carved recension, with staves for the diphthongs _ai_, _au_ and _oi_.
- A pair of crown marks cuts a frame of straight grooves around the name of a god, a founder or an emperor.
- Bound runes set a common pair of staves on one stem; they sit behind the stylistic set `ss01`, which the class `hl-thuravark-carved-bound` turns on, so plain Thuravark text is unchanged.
- A Veldikko keyboard layout, HL Veldikko, types the Sinale hand by sound on macOS, Windows, Linux and in Emacs, with keys for the carrier, the long sign, the doubling bar, the rise, the fall and the emphasis.

## 0.2.0

### Minor Changes

- Typing roman text in a script font no longer converts it: each script font draws only its own characters, and every other character, Latin included, prints the box.
- Roman text is written in a script through thalorna's mapping notes, as a passage marked with a mapping is, or typed with the keyboard layouts.
- Qalezu Hand draws a catch before a sign as that sign's catch-before form from the two characters, so the catch-before forms no longer have characters of their own.

### Patch Changes

- The Semaron, Pirzath, Thuravark and Qalezu keyboards type the letters j, q, v and ë wherever the script spells them: q and ë in Semaron and Thuravark, ë in Pirzath, and j and v in Qalezu.
- Every release offers each font to download from GitHub, as TrueType and WOFF2.

## 0.1.5

### Patch Changes

- **Veldikko** is available: the Sinale starlight-hand, a flowing right-to-left calligraphy whose letters join along the line and whose vowels float above as marks, in one face for Sinale and Áelendi.
- Its letters set at the same size as Semaron and Latin text, with long risers and tails; give a block of it a generous line height.

## 0.1.4

### Patch Changes

**Teng Chou**

- Teng Chou, the Celestial Record of Tantsou and Jenchai, has a font: its characters for the core vocabulary and the Jurthati syllabary, written with a broad brush.
- Text set in vertical columns stands evenly, each character centred on the column; an inline span sets the characters left to right.
- A tally of five keeps a running count, one stroke per item, with a character for each stage from one to five.

## 0.1.3

### Patch Changes

**Every script**

- Script text sits at a natural spacing instead of widely spaced, and each hieroglyph takes the width of its own drawing.
- Bold or italic text in a script font keeps the font's one style instead of smearing or slanting its letters.

**Keyboards and cheatsheets**

- The keyboard layouts type by sound: each sound of the spelling guide sits on one key, the same key in every script, and types that script's own letters.
- The characters Markdown and a `[text]{font=…}` span need type themselves on every layout, so markup is written without switching layouts; Pirzath's quotes move to Shift+`,` and Shift+`.`.
- Each font has a cheatsheet, a code chart and a table of every character's glyph, name and code point, and one more draws the shared sound keys on a keyboard.

**Khelathi Zethu Glyphs**

- Signs stack into quadrats from joiners, segments and corner insertions typed between them, each quadrat scaled to fit one sign's square.
- A royal name typed between the enclosure controls is drawn inside a knotted cord, tied at the left, and stays whole on one line.
- Type the controls at the font's own code points, U+1EC60 to U+1EC6D, which work in browsers and Foundry; the Unicode controls work in HarfBuzz tools only.
- New signs write captives led and bound, the states of a temple entry, giving and taking, priests, envoys, the quarters, the sea and the wild beasts.
- Solid ink no longer fills gaps inside some signs, such as the cut loaf, the empty pan and the level tablets.

## 0.1.2

### Patch Changes

- Every character of every font has a code point of its own.
- The package carries keyboard layouts for macOS, Emacs input methods and cheatsheets for typing in each font.
- Each script is sized to stand as tall as the roman beside it, and the fonts share one line spacing.
- The package lists its fonts and their characters in `fonts.json`, with one CSS class per font.

## 0.1.1

### Patch Changes

The package gains Semaron Kuriale, the Vylarian chancery hand, with majuscules, minuscules, long-vowel curls and the catch mark.
