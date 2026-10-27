# Fantasy script fonts

Open-source fonts for invented writing systems, free to use in your own campaign, game, book or website. They were built for the [HeroicLands Thalorna](https://www.heroiclands.org/thalorna/) setting, and anyone may use them.

| Font                     | What it is                                                                                | Direction                                      | Sample                                                                                                                                                                             | Chart                                                          |
| ------------------------ | ----------------------------------------------------------------------------------------- | ---------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| Pirzath Carved           | Khazari (dwarven) runic lapidary                                                          | Left to right                                  | [![Pirzath Carved](https://raw.githubusercontent.com/HeroicLands/fonts/main/specimens/readme/hl-pirzath-carved.png)](specimens/hl-pirzath-carved.md)                               | [Pirzath Carved](charts/pirzath.md)                            |
| Pirzath Hand             | Khazari (dwarven) common hand, the modern script                                          | Left to right                                  | [![Pirzath Hand](https://raw.githubusercontent.com/HeroicLands/fonts/main/specimens/readme/hl-pirzath-hand.png)](specimens/hl-pirzath-hand.md)                                     | [Pirzath Hand](charts/pirzath-hand.md)                         |
| Thuravark Carved         | Proto-Pelwar (human) runic lapidary, derived from Pirzath, with the Tharavarkon recension | Left to right                                  | [![Thuravark Carved](https://raw.githubusercontent.com/HeroicLands/fonts/main/specimens/readme/hl-thuravark-carved.png)](specimens/hl-thuravark-carved.md)                         | [Thuravark Carved](charts/thuravark-carved.md)                 |
| Semaron Kuriale          | Vylarian (human) chancery hand                                                            | Left to right                                  | [![Semaron Kuriale](https://raw.githubusercontent.com/HeroicLands/fonts/main/specimens/readme/hl-semaron-kuriale.png)](specimens/hl-semaron-kuriale.md)                            | [Semaron Kuriale](charts/semaron-kuriale.md)                   |
| Helonika Book            | Helonic (human) book hand, geometric capitals over a round minuscule                      | Left to right                                  | [![Helonika Book](https://raw.githubusercontent.com/HeroicLands/fonts/main/specimens/readme/hl-helonika-book.png)](specimens/hl-helonika-book.md)                                  | [Helonika Book](charts/helonika-book.md)                       |
| Vedyakshara Classical    | Vedyari (human) temple syllabary, hung from a headline                                    | Left to right                                  | [![Vedyakshara Classical](https://raw.githubusercontent.com/HeroicLands/fonts/main/specimens/readme/hl-vedyakshara-classical.png)](specimens/hl-vedyakshara-classical.md)          | [Vedyakshara Classical](charts/vedyakshara-classical.md)       |
| Veldikko                 | Sinale (elvish) joined calligraphic hand                                                  | Right to left                                  | [![Veldikko](https://raw.githubusercontent.com/HeroicLands/fonts/main/specimens/readme/hl-veldikko.png)](specimens/hl-veldikko.md)                                                 | [Veldikko](charts/veldikko.md)                                 |
| Qalezu Hand              | Au'Khelathu merchants' script                                                             | Right to left                                  | [![Qalezu Hand](https://raw.githubusercontent.com/HeroicLands/fonts/main/specimens/readme/hl-qalezu-hand.png)](specimens/hl-qalezu-hand.md)                                        | [Qalezu Hand](charts/qalezu-hand.md)                           |
| Khelathi Zethu Glyphs    | Au'Khelathu temple hieroglyphs                                                            | Right to left                                  | [![Khelathi Zethu Glyphs](https://raw.githubusercontent.com/HeroicLands/fonts/main/specimens/readme/hl-khelathi-zethu-glyphs.png)](specimens/hl-khelathi-zethu-glyphs.md)          | [Khelathi Zethu Glyphs](charts/khelathi-zethu-glyphs.md)       |
| Teng Chou                | Tantsou (human) logographic script                                                        | Vertical, top to bottom                        | [![Teng Chou](https://raw.githubusercontent.com/HeroicLands/fonts/main/specimens/readme/hl-teng-chou.png)](specimens/hl-teng-chou.md)                                              | [Teng Chou](charts/teng-chou.md)                               |
| Chalish Pilam Common     | Ki'ich'chik everyday logographic hand                                                     | Left to right, read two to a row down a column | [![Chalish Pilam Common](https://raw.githubusercontent.com/HeroicLands/fonts/main/specimens/readme/hl-chalish-pilam-common.png)](specimens/hl-chalish-pilam-common.md)             | [Chalish Pilam Common](charts/chalish-pilam.md)                |
| Chalish Pilam Ceremonial | Ki'ich'chik carved logographic hand, glyphs and syllable signs composed into blocks       | Left to right, read in paired columns          | [![Chalish Pilam Ceremonial](https://raw.githubusercontent.com/HeroicLands/fonts/main/specimens/readme/hl-chalish-pilam-ceremonial.png)](specimens/hl-chalish-pilam-ceremonial.md) | [Chalish Pilam Ceremonial](charts/chalish-pilam-ceremonial.md) |

Each font draws only its own characters, on code points of its own, so ordinary English text typed in one shows empty boxes. You insert characters by code point from the font's chart, which lists every character with its code point, its name and its code, a short name such as `PARGH` or `DIGIT_ZERO`.

## Download

Every font is a TrueType file (`.ttf`, for documents and desktop apps) and a WOFF2 file (`.woff2`, for websites). Download them from the [latest release](https://github.com/HeroicLands/fonts/releases/latest), which also holds `charts.zip` (the character charts). Programs can take everything from npm instead; see [For programs](#for-programs).

## Install a font

Install the `.ttf` file. Close and reopen a program that was running, so it sees the new font.

- **macOS.** Double-click the `.ttf`, then choose Install Font in the Font Book window.
- **Windows.** Right-click the `.ttf` and choose Install, or Install for all users.
- **Linux.** Copy the `.ttf` to `~/.local/share/fonts/`, then run `fc-cache -f`.

## Use a font in a document

Choose the font by its name, such as `Pirzath Carved`, in the font box of your word processor.

- **Microsoft Word, LibreOffice Writer and Apple Pages** use an installed font directly. Word, LibreOffice and Pages all shape OpenType text, which the joined scripts need: Veldikko's letters join along the line and its vowel marks stand over them only in an app that shapes text this way.
- **Web apps such as Google Docs cannot use a font installed on your computer.** Use a desktop app, or put the text in a picture.
- **Right-to-left scripts** (Veldikko, Qalezu Hand and Khelathi Zethu Glyphs) run right to left on their own, mixed with English, with no setting to change.
- **Veldikko** has tall risers and long tails. Set its paragraphs to a line height of about 2.4 times the font size so lines do not collide.
- **Thuravark Carved** has an optional form, the OpenType stylistic set `ss01`. Turned on, it binds common pairs of staves onto one stem. In LibreOffice, write the font name as `Thuravark Carved:ss01`.
- **Teng Chou** is written in columns. Set it as ordinary text on a line, or use your app's vertical text direction for columns.
- **Chalish Pilam Common** is written left to right and read two glyphs to a row, down a column two glyphs wide. Set it in a column that wide and the line wraps into rows of two by itself.
- **Chalish Pilam Ceremonial** composes its glyphs into blocks: a main sign with a number or syllable signs set beside it, over it or under it. The font lays out a block from the invisible joiners between its glyphs: `JOINER_BESIDE` (U+F4FF0) sets the glyphs either side of it side by side, and `JOINER_STACK` (U+F4FF1) stacks the first over the second. So `n13`, `JOINER_BESIDE`, `TQAN` sets the number thirteen beside the day sign, and `la1`, `JOINER_STACK`, `SUN` stacks a syllable sign over the sun. Blocks are read in paired columns: across each pair, then down.

## Insert characters

Open the font's chart from the table above, find the character, and insert it by its code point, such as `U+1EA41`:

- **Word on Windows, and LibreOffice:** type the hex digits (`1EA41`) with the cursor after them and press Alt+X. The digits become the character.
- **macOS:** choose Edit, Emoji & Symbols to open the Character Viewer, search for the code point, and double-click the character. The Unicode Hex Input source also types a code point with Option and four hex digits.
- **Linux:** press Ctrl+Shift+U, type the hex digits, and press Enter.

Set the character's font to the matching font, or it shows as an empty box. To type the characters you use most, set up a layout or input method of your own from the chart.

## For programs

The fonts are on npm as `@heroiclands/fonts`, with the font files, `fonts.css`, the `fonts.json` manifest and the charts. The manifest lists every character of every font with its code point, name and code:

```sh
npm install @heroiclands/fonts
```

On a web page, import the stylesheet and name a family:

```css
@import "@heroiclands/fonts/fonts.css";
```

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@heroiclands/fonts@0/fonts.css" />
```

`@0` follows the newest 0.x release, and a full version pins one. A family is named by its font-family, such as `font-family: "Pirzath Carved"`, or by the `hl-<font>` class in `fonts.css`, which also turns on any OpenType feature the family needs and sets right-to-left families to run right to left.

For Foundry VTT, Typst and the manifest's contents, see [DEVELOPING.md](DEVELOPING.md).

## Licence

The fonts are licensed under the SIL Open Font License 1.1; see `LICENSE`. Under it they may be used, embedded in web pages, documents and books, and bundled with software, without that work taking on the font's licence.

## Developing

To build the fonts, run the checks or add a font, see [DEVELOPING.md](DEVELOPING.md).
