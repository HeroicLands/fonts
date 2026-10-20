# fonts

Fonts for the scripts of the HeroicLands settings, drawn from scratch so that a setting's inscriptions can be shown in their own letters on the sites, in the books and in Foundry.

Pirzath Carved and Thuravark Carved draw their script over the setting's Latin spelling. Text stays plain, readable and searchable, and a passage switches to the script by its font alone. A letter pair that the spelling uses for one sound, such as _th_ or _kh_, draws the single letter for that sound.

Qalezu, the Khelathi alphabet, is written right to left on code points of its own, U+1EA00 to U+1EA3F, with the catch-before forms in U+1ECC0 to U+1ECFF. A converter turns Latin Khelathi into those code points, and the font draws them; `tools/qalezu-hand/encoding.json` is the one table of what each code point is, its sound and the Latin that types it.

## Licence

The fonts are licensed under the SIL Open Font License 1.1; see `LICENSE`. Under it they may be embedded in web pages, documents and books, and bundled with software, without that work taking on the font's licence.

## Installing and using the fonts

The fonts are published to npm as `@heroiclands/fonts`. The package holds each font as WOFF2 and TrueType, `fonts.css` with one `@font-face` rule per family, and `encoding/`, the code-point tables of the right-to-left fonts.

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

The right-to-left fonts take their text as code points of their own; `encoding/<font>.json` is the table of what each code point is.

The fonts are licensed under the SIL Open Font License 1.1, which `LICENSE` carries in the package.

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

The source of each font is a UFO under `sources/`: `PirzathCarved.ufo`, `PirzathHand.ufo`, `ThuravarkCarved.ufo`, `QalezuHand.ufo` and `KhelathiZethuGlyphs.ufo`. Open one in FontForge, Glyphs or RoboFont to edit it. The UFO carries the outlines, the character map, the metrics and `features.fea`, which holds every OpenType feature.

Build the fonts into `fonts/`. The build is reproducible, so the committed fonts match a fresh build byte for byte:

```sh
PATH=.venv/bin:$PATH ./build.sh
```

`build.sh` runs `fontmake` and compresses the `.woff2`, once per font (`PirzathCarved` shown), then runs `tools/write_css.py`, which writes `fonts.css` from the built fonts' name tables and copies the right-to-left fonts' `encoding.json` into `encoding/`:

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
.venv/bin/python tools/notdef_box.py
.venv/bin/python tools/font_names.py
.venv/bin/python tools/pirzath/specimens.py       # specimens/pirzath/
.venv/bin/python tools/pirzath-hand/specimens.py  # specimens/pirzath-hand/
.venv/bin/python tools/thuravark-carved/specimens.py     # specimens/thuravark-carved/
.venv/bin/python tools/qalezu-hand/specimens.py        # specimens/qalezu-hand/
.venv/bin/python tools/khelathi-zethu-glyphs/specimens.py         # specimens/khelathi-zethu-glyphs/
.venv/bin/python tools/prove_guards.py
```

Each guard shapes every form of its lexicon and asserts the font renders it rightly; the Pirzath guards read the Khazari lexicon, the Thuravark guard the Nordmal one, and Qalezu's converts the Khelathi lexicon from Latin first. Each reads its lexicon from the `origin/main` of a local thalorna checkout, `~/dev/HeroicLands/thalorna` by default:

```sh
.venv/bin/python tools/pirzath/guard.py --thalorna /path/to/thalorna
.venv/bin/python tools/pirzath-hand/guard.py --thalorna /path/to/thalorna
.venv/bin/python tools/thuravark-carved/guard.py --thalorna /path/to/thalorna
.venv/bin/python tools/qalezu-hand/guard.py --thalorna /path/to/thalorna
```

Qalezu's character map follows from `encoding.json`; after editing that file, `.venv/bin/python tools/qalezu-hand/apply_encoding.py` rewrites the UFO's code points, and `--check` reports a disagreement.

Khelathi Zethu Glyphs is the temple hieroglyphs of the Khelathi, on U+1EA40 to U+1EC6F and written right to left. Its guard reads no lexicon: it shapes the sample inscriptions kept in `tools/khelathi-zethu-glyphs/samples.json`.

```sh
.venv/bin/python tools/khelathi-zethu-glyphs/guard.py
```

See `design/khelathi-zethu-glyphs.md`.
