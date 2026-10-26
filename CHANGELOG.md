# @heroiclands/fonts

## 1.3.0

### Minor Changes

**Semaron Kuriale**

- Gains letters for ch, sh, kh, gh, dh, zh, ts, ng, ny and q, in both cases, so text that spelled these with two letters now writes one.
- The aspirate hook on f, th and the new aspirates is bolder and reads at text size.

- **Shared punctuation.** Every encoding follows the same punctuation assignments, including `‼` for an imperative sentence and `!` for an exclamation. Invisible marks preserve sentence types, quotations and name boundaries when a script does not draw them.
- **Verse and spacing.** Ordinary whitespace becomes one word separator. Verse mode writes distinct line and stanza controls, `--- {.canto}` marks a canto boundary, and `^` supplies indentation.
- **Script punctuation.** Scripts retain their own visible sentence-end forms while sharing the punctuation meanings. Generic invisible spelling metadata remains distinct from the shared structural controls.
- **Capitals and keyboards.** Semaron Kuriale and Helónika write capitals as majuscules; other scripts accept lowercase Roman text, while codages retain their capital codes. Their layouts type capitals on Shift, the Semaron comma key types the point, and the caseless layouts leave shifted letter keys empty.
- **Literal characters.** All encodings accept exact characters between `⟦` and `⟧`, using shared non-printing boundaries and the active encoding's character names or codage. Whitespace separates codes, and a font without a Roman encoding accepts only literal spans.
- **Input and typing.** Unknown characters are refused at their line and column. All layouts type the literal markers on Option+Shift+W and Option+Shift+L, and HL Vedyakshara types independent vowels on Shift and the vowel key.

### Patch Changes

- Aelwythi has its own Semaron encoding with dedicated consonant assignments and a non-printing stress modifier. Consonant groups accept only lowercase or initial-uppercase forms, and decoding returns a conventional spelling without restoring omitted punctuation.
- **Chalish Pilam Ceremonial house emblems.** Every Ki'ich'chik house has its emblem, so a name can open with its house's picture, such as `n3*SHAKNAL:la1` for the third of the eagle house. The nineteen new emblems include the golden, silver and serpent seats, the censer, the plumed crown, the ceiba and the conch.
- **Chalish Pilam Ceremonial.** The carved temple hand of the Ki'ich'chik writing joins the fonts, with its character chart, a specimen page and its encoding. It writes concept glyphs, numbers and syllable signs, and composes them into blocks typed through the `chalish-ceremonial` encoding, such as `n13*TQAN` for the number thirteen beside the day sign.
- **Encodings.** The package ships an encoding for each script font in `encodings/`, with a page describing each one. `encode.py` turns roman text into a font's characters and reads them back exactly, needing only Python 3.9 or later.
- **Khelathi Zethu codes.** Every Khelathi Zethu sign has a code naming its sense, such as `SAIL` or `REGNAL_YEAR`. Its encoding is typed with these codes instead of sign numbers.
- **Keyboards.** In Veldikko, the sh key types two letters, and an accented vowel types the emphasis sign with its vowel.
- **Helónika Book.** The space after a sentence-end dot closes up, so the dot sits close to the next word.
- Invisible characters, such as variation selectors, no longer show as the word-divider dot in Pirzath Carved.
- **Teng Chou codes.** Every Teng Chou character has a code: a character its morpheme in capitals, such as `WONG`, a stage of the tally `TALLY1` to `TALLY5`, and a Jurthati syllable sign its syllable in lowercase, such as `ka`. The `teng-chou` encoding writes them between `⟦` and `⟧`, so `⟦WONG TALLY3 ka⟧` types three characters.
- Khelathi Zethu Glyphs draws every sign of its inventory, so no sign prints as a box. The new drawings include the seated man and woman, parts of the body, beasts, birds and river fish, plants, tools, vessels and adornment.

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
