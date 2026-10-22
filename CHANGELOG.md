# @heroiclands/fonts

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
