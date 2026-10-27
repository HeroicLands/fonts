# @heroiclands/fonts

## 1.4.0

### Minor Changes

- Every character of every font has a short code, such as `PARGH` or `DIGIT_ZERO`, listed in `fonts.json` beside its code point and name and shown on the font's chart.
- The package carries the fonts, `fonts.css`, `fonts.json` and the character charts, and the README links a specimen page for every font.
- The encodings, `encode.py` and the keyboard layouts are no longer part of the package, and a Khelathi Zethu Glyphs sign in `fonts.json` carries its code in place of its `key`.

## 1.3.0

### Minor Changes

**Semaron Kuriale**

- Has letters for ch, sh, kh, gh, dh, zh, ts, ng, ny and q, in small and capital forms, so text that spelled these with two letters writes one.
- The aspirate hook on f, th and the new aspirates is bolder and reads at text size.
- HL Semaron types q on its own key and each new pair on Option and its first letter, with _ts_ on Option+X and _ny_ on Option+Y; capitals add Shift.

**Encodings**

- Every encoding follows one standard set of punctuation marks, so a sentence ending, pause, quotation, name or verse break means the same in every script.
- Where a script does not draw a mark, the encoding keeps its meaning in invisible characters, so decoding restores the text exactly.
- Verse lines, stanzas and cantos are written with `/`, a blank line and `--- {.canto}`, and `^` at the start of a line indents it.
- Between `⟦` and `⟧`, any encoding takes exact characters by name or code, and a font with no roman encoding takes only these.
- Characters an encoding does not accept are refused with their line and column.

### Patch Changes

**New fonts**

- Chalish Pilam Ceremonial, the carved temple hand of the Ki'ich'chik writing, joins the fonts with a character chart, a specimen page and an encoding.
- It writes concept glyphs, numbers and syllable signs, and composes them into blocks, such as `⟦n13*TQAN⟧` for the number thirteen beside the day sign.
- Every Ki'ich'chik house has an emblem, so a name can open with its house's picture, as in `⟦n3*SHAKNAL:la1⟧`.

**Encodings**

- The package ships an encoding for each script font in `encodings/`, and `encode.py` turns roman text into a font's characters and reads them back exactly.
- Aelwythi has its own Semaron encoding, with its own signs for its consonant groups and a non-printing stress mark on acute vowels.
- Teng Chou characters are typed by name between `⟦` and `⟧`: `WONG` for a morpheme, `TALLY1` to `TALLY5` for the tally, `ka` for a syllable sign.
- Khelathi Zethu signs are typed by code, such as `SAIL` or `REGNAL_YEAR`, instead of sign number.

**Keyboards**

- Every layout types `⟦` and `⟧` on Option+Shift+W and Option+Shift+L.
- HL Vedyakshara types an independent vowel on Shift and the vowel key.
- In HL Veldikko, the sh key types both letters, and an accented vowel types the emphasis sign with its vowel.

**Fixes**

- Khelathi Zethu Glyphs draws every sign of its inventory, so no sign prints as a box.
- In Helónika Book the dot that ends a sentence sits close to the next word.
- Invisible characters, such as variation selectors, do not show as the word-divider dot in Pirzath Carved.

## 1.2.1

### Patch Changes

Chalish Pilam Common, the everyday hand of the Ki'ich'chik writing, joins the fonts, with its character chart and a specimen page.

## 1.2.0

### Minor Changes

- Add a high verse-ending dot to Qalezu Hand.

## 1.1.0

### Minor Changes

- Pirzath Hand is redrawn as a plain printed hand that reads at a glance: separate, even-weight letters as tall as Latin capitals, with sixteen new digits that cannot be mistaken for one another.
- Pirzath Hand Lifted and the joining line are gone; Pirzath Hand is one printed face with no stylistic set.

### Patch Changes

The HL Helónika keyboard types the _kh_ and _zh_ letters, the long vowels and the accent, on keys of their own.

## 1.0.1

### Patch Changes

- Each font has a specimen page showing its letters, a sample of its marks, and a short passage in the script with its English translation and roman spelling; click a font's sample in the README to open it.
- The README's font samples show on Gitea and npm as well as GitHub.
- In Helonika Book the raised dot that ends a sentence stands in a space of its own, so the next sentence follows it directly.

## 1.0.0

### Major Changes

**The fonts**

- Left to right: Pirzath Carved and Pirzath Hand, Thuravark Carved, Semaron Kuriale, Helonika Book and Vedyakshara Classical.
- Right to left: Veldikko, Qalezu Hand and Khelathi Zethu Glyphs. Teng Chou is written in vertical columns.
- Each font draws only its own characters, on code points of its own; within a major version a character keeps its code point, so typed text keeps its meaning across updates.
- Every script stands as tall as Latin text beside it, and all of them share one line spacing.
- Veldikko joins its letters with the vowels floating above as marks, Vedyakshara hangs its signs from a headline with fused clusters, and Khelathi Zethu Glyphs stacks its signs into quadrats and cartouches.
- Thuravark Carved writes the Tharavarkon's diphthongs and crown marks; it and Pirzath Hand each have an optional stylistic set, `ss01`, for bound runes and a joining line.
- Teng Chou centres each character in its column and keeps a running tally of five.

**Typing**

- Keyboard layouts for macOS, Windows, Linux and Emacs type each script by sound, with the same key for a sound in every layout, and the characters of markup type themselves.
- Every layout has a printable cheatsheet, and every font a character chart; Teng Chou and Khelathi Zethu Glyphs are typed by code point from their charts.

**Getting them**

- Every release offers each font as TrueType and WOFF2 on GitHub, with the keyboards and charts as zips; programs take them from npm, with `fonts.css` and the `fonts.json` manifest.
- The README walks through installing the fonts and layouts on each platform and using them in Word, LibreOffice and Pages.
