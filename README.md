# fonts

Fonts for the scripts of the HeroicLands settings, drawn from scratch so that a setting's inscriptions can be shown in their own letters on the sites, in the books and in Foundry.

Pirzath Carved and Thuravark Carved draw their script over the setting's Latin spelling. Text stays plain, readable and searchable, and a passage switches to the script by its font alone. A letter pair that the spelling uses for one sound, such as _th_ or _kh_, draws the single letter for that sound.

Semaron Kuriale, the Vylarian chancery hand, draws the Vylari spelling in majuscules and minuscules: a doubled vowel types the long vowel's curl, a catch after a letter types the grave over it, and every pause types the one point.

Each left-to-right face also draws every one of its characters on a code point of its own in plane 15, the Supplementary Private Use Area-A: the Pirzath faces on U+F0000, Thuravark Carved on U+F0100 and Semaron Kuriale on U+F0200 (see [Code point blocks](#code-point-blocks)). `fonts.json` lists each face's characters under `codepoints`, and `specimens/<face>/codepoints.png` charts them.

Qalezu, the Khelathi alphabet, is written right to left on code points of its own, U+1EA00 to U+1EA3F, with the catch-before forms in U+1ECC0 to U+1ECFF. A converter turns Latin Khelathi into those code points, and the font draws them; `tools/qalezu-hand/encoding.json` is the one table of what each code point is, its sound and the Latin that types it.

## Code point blocks

Every script draws on a block of code points of its own, and every face of a script draws its script's block: Pirzath Carved, Pirzath Hand and Pirzath Hand Lifted share the Pirzath block, so changing the face changes only the look. The blocks are registered in `BLOCKS` in `tools/codepoint_order.py`; `tools/codepoints.py` checks that every face's code points lie in its registered blocks, that no two blocks overlap, and that this table is the registry's.

| Range             | Use                                                                                             | Direction     |
| ----------------- | ----------------------------------------------------------------------------------------------- | ------------- |
| U+1E960–U+1E9FF   | Khelathi Zethu Glyphs, overflow beyond its main block                                           | right to left |
| U+1EA00–U+1EA3F   | Qalezu: signs, digits and punctuation                                                           | right to left |
| U+1EA40–U+1EC6F   | Khelathi Zethu Glyphs                                                                           | right to left |
| U+1ECC0–U+1ECFF   | Qalezu: a sign with a catch before it                                                           | right to left |
| U+F0000–U+F00FF   | Pirzath                                                                                         | left to right |
| U+F0100–U+F01FF   | Thuravark                                                                                       | left to right |
| U+F0200–U+F02FF   | Semaron                                                                                         | left to right |
| U+F0300–U+F0FFF   | Reserved for the remaining alphabets and syllabaries, 256 code points each as they are assigned | left to right |
| U+F1000–U+F2FFF   | Reserved for Teng Chou                                                                          | left to right |
| U+100000–U+10FFFD | Plane 16, unassigned                                                                            | –             |

- **Left-to-right scripts** (Pirzath, Thuravark, Semaron) sit in plane 15, the Supplementary Private Use Area-A, whose characters are left to right by default. Each takes 256 code points. U+F0300 to U+F0FFF is reserved for the remaining alphabets and syllabaries, 256 code points each as they are assigned, and U+F1000 to U+F2FFF for Teng Chou.
- **Right-to-left scripts** (Qalezu and Khelathi Zethu Glyphs) sit in unassigned code points of plane 1 whose default bidi class is right to left. That is why their text runs right to left in any editor, browser or typesetter, mixed with English and with no controls. Because the code points are unassigned rather than private, Unicode could in principle assign them to a script later. Qalezu takes U+1EA00 to U+1EA3F for its signs, digits and punctuation and U+1ECC0 to U+1ECFF for a sign with a catch before it. Khelathi Zethu Glyphs takes U+1EA40 to U+1EC6F with U+1E960 to U+1E9FF as overflow, 720 code points together. U+1ED50 to U+1EDFF is the remaining free right-to-left range, kept for a further right-to-left script.
- **Plane 16** is unassigned.

## Licence

The fonts are licensed under the SIL Open Font License 1.1; see `LICENSE`. Under it they may be embedded in web pages, documents and books, and bundled with software, without that work taking on the font's licence.

## Installing and using the fonts

The fonts are published to npm as `@heroiclands/fonts`. The package holds each font as WOFF2 and TrueType, `fonts.css` with one `@font-face` rule and one `hl-<font>` class per family, `fonts.json`, the manifest of the families, and `keyboards/`, the keyboard layouts, Emacs input methods and cheatsheets for typing in them.

```sh
npm install @heroiclands/fonts
```

**Web.** Import the stylesheet from a bundler or a stylesheet, or link it:

```css
@import "@heroiclands/fonts/fonts.css";
```

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@heroiclands/fonts@0/fonts.css" />
```

The jsDelivr form is `https://cdn.jsdelivr.net/npm/@heroiclands/fonts@<version>/<file>`. `@0` follows the newest 0.x release, and a full version pins one. A rule's URLs are relative, so every file resolves beside the stylesheet. A family is named by its font-family, such as `font-family: "Pirzath Carved"`.

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

`fonts.json` states, for each entry, its `name` (unique across the manifest), its `family` (the font-family), its `hl-<font>` class, its `files`, its `direction`, its OpenType `features` and its `codepoints`: every character the font draws, each with its code point, glyph name, kind and the key that types it. The class sets the family's `font-family`, `font-feature-settings` and, for a right-to-left family, `direction`. Pirzath Hand's joined form needs `ss01`, which its class turns on; Pirzath Hand Lifted is the same font with `ss01` turned off.

A note's text in one of these fonts is the font's own code points. They are typed with the keyboard layouts in `keyboards/`, or produced by a mapping in the consuming build.

The fonts are licensed under the SIL Open Font License 1.1, which `LICENSE` carries in the package.

## Typing in the fonts

A note records Unicode characters, so typing in a family's fonts needs a keyboard layout that produces its code points. Each family has one, and the faces of a family share their code points, so one layout types for every face: the three Pirzath faces share the Pirzath layout. The layouts come from the `key` of each row of `fonts.json`'s `codepoints` tables, and `keyboards/` carries them:

- **macOS layouts.** `keyboards/macos/HeroicLands.bundle` holds one layout for Semaron, Pirzath, Thuravark and Qalezu: HL Semaron, HL Pirzath, HL Thuravark and HL Qalezu. Copy the bundle to `~/Library/Keyboard Layouts/`, log out and back in, then add each layout under System Settings → Keyboard → Text Input → Input Sources, where the layouts appear under the language English. Letters sit on their roman keys and numerals on the digit row; Shift types capitals or digraph letters, and Option types what is left: Semaron's `th` and long vowels, Pirzath's numerals ten to fifteen and the length mark, Qalezu's doubled signs and the signs after a catch.
- **Windows layouts.** `keyboards/windows/<family>.klc` is the Microsoft Keyboard Layout Creator source of HL Semaron, HL Pirzath, HL Thuravark and HL Qalezu, saved as UTF-16 with a byte order mark. Option is the right Alt key (AltGr). A character of plane 15 is a ligature entry holding its surrogate pair, which Windows delivers as one character. MSKLC builds the installer on Windows only: open the `.klc` in Microsoft Keyboard Layout Creator, choose Project, Build DLL and Setup Package, and run the `setup.exe` it writes. Then add the layout under Settings, Time & language, Language & region, English (United States), Keyboard.
- **Linux layouts.** `keyboards/linux/hl_<family>` is an XKB symbols file for each of the four families, with a `U<hex>` keysym for every character. Option is the third level, reached with the right Alt key. Copy the files to `~/.config/xkb/symbols/`, then run `setxkbmap -I$HOME/.config/xkb -layout hl_pirzath` under X11; a desktop that reads `~/.config/xkb` lists them as custom layouts. `setxkbmap us` returns to the usual layout.
- **Emacs input methods.** `keyboards/emacs/heroiclands-<family>.el` defines a Quail input method per family. Put the directory on `load-path`, evaluate `(require 'heroiclands-semaron)`, then `M-x set-input-method RET heroiclands-semaron`. Shift is the shifted character. Emacs has no Option key, so Option+x is typed `\` and then the key x types: Option+E is `\e` and Option+Shift+A is `\A`.
- **Khelathi Zethu Glyphs.** It has far more signs than a keyboard has keys, so it has an Emacs input method only, typed by sign id: `08-001` inserts that sign.
- **Cheatsheets.** `keyboards/<family>.md` lists every key beside its Emacs sequence, code point and glyph, and `specimens/<face folder>/keyboard.png` draws each key beside its glyph in every face of the family, Pirzath's three faces side by side.

## Setting up

Install the dependencies, which also activates the repository's git hooks:

```sh
npm ci
```

Create the virtual environment:

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

The source of each font is a UFO under `sources/`: `PirzathCarved.ufo`, `PirzathHand.ufo`, `ThuravarkCarved.ufo`, `QalezuHand.ufo`, `KhelathiZethuGlyphs.ufo` and `SemaronKuriale.ufo`. Open one in FontForge, Glyphs or RoboFont to edit it. The UFO carries the outlines, the character map, the metrics and `features.fea`, which holds every OpenType feature.

Build the fonts into `fonts/`. The build is reproducible, so the committed fonts match a fresh build byte for byte:

```sh
PATH=.venv/bin:$PATH ./build.sh
```

`build.sh` runs `fontmake` and compresses the `.woff2`, once per font (`PirzathCarved` shown), then runs `tools/write_css.py`, which writes `fonts.css` and `fonts.json` from the built fonts' name tables and one table of per-family facts. `tools/keyboards.py` then writes `keyboards/` and each family's `specimens/<face folder>/keyboard.png` from `fonts.json`; `tools/keyboard_keys.py` is the one place that assigns a key to each character:

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
.venv/bin/python tools/notdef_box.py
.venv/bin/python tools/vertical.py
.venv/bin/python tools/font_names.py
.venv/bin/python tools/codepoints.py
.venv/bin/python tools/keyboards_guard.py --fixtures-only   # the layouts type every character
.venv/bin/python tools/codepoints_chart.py         # specimens/<face>/codepoints.png
.venv/bin/python tools/pirzath/specimens.py       # specimens/pirzath/
.venv/bin/python tools/pirzath-hand/specimens.py  # specimens/pirzath-hand/
.venv/bin/python tools/thuravark-carved/specimens.py     # specimens/thuravark-carved/
.venv/bin/python tools/qalezu-hand/specimens.py        # specimens/qalezu-hand/
.venv/bin/python tools/khelathi-zethu-glyphs/specimens.py         # specimens/khelathi-zethu-glyphs/
.venv/bin/python tools/semaron-kuriale/specimens.py     # specimens/semaron-kuriale/
.venv/bin/python tools/prove_guards.py
```

Each guard shapes every form of its lexicon and asserts the font renders it rightly; the Pirzath guards read the Khazari lexicon, the Thuravark guard the Nordmal one, Semaron Kuriale's the Vylari one, and Qalezu's converts the Khelathi lexicon from Latin first, through `tools/qalezu-hand/convert.mjs`, an internal tool of that guard, under `node`. Each reads its lexicon from the `origin/main` of a local thalorna checkout, `~/dev/HeroicLands/thalorna` by default:

```sh
.venv/bin/python tools/pirzath/guard.py --thalorna /path/to/thalorna
.venv/bin/python tools/pirzath-hand/guard.py --thalorna /path/to/thalorna
.venv/bin/python tools/thuravark-carved/guard.py --thalorna /path/to/thalorna
.venv/bin/python tools/qalezu-hand/guard.py --thalorna /path/to/thalorna
.venv/bin/python tools/semaron-kuriale/guard.py --thalorna /path/to/thalorna
```

`tools/keyboards_guard.py` also reads the layouts back and asserts that each puts every character of its family on the key `fonts.json` names. Without `--fixtures-only` it shapes every lexicon form of the families above with the fonts' Latin typing rules, maps each glyph to its code point, and asserts that the family's layout has a key for it; it reads thalorna the same way, through `--thalorna`. Qalezu's forms go through its converter first, and Khelathi Zethu Glyphs is checked on the sign ids of its sample inscriptions.

```sh
.venv/bin/python tools/keyboards_guard.py --thalorna /path/to/thalorna
```

Qalezu's character map follows from `encoding.json`; after editing that file, `.venv/bin/python tools/qalezu-hand/apply_encoding.py` rewrites the UFO's code points, and `--check` reports a disagreement.

Khelathi Zethu Glyphs is the temple hieroglyphs of the Khelathi, on U+1EA40 to U+1EC6F and written right to left. Its guard reads no lexicon: it shapes the sample inscriptions kept in `tools/khelathi-zethu-glyphs/samples.json`.

```sh
.venv/bin/python tools/khelathi-zethu-glyphs/guard.py
```

See `design/khelathi-zethu-glyphs.md`.
