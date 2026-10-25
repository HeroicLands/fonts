# @heroiclands/fonts

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
