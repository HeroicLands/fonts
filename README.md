# heroiclands-fonts

Fonts for the scripts of the HeroicLands settings, drawn from scratch so that a setting's inscriptions can be shown in their own letters on the sites, in the books and in Foundry.

Pirzath Carved and Thuravark Runic draw their script over the setting's Latin spelling. Text stays plain, readable and searchable, and a passage switches to the script by its font alone. A letter pair that the spelling uses for one sound, such as _th_ or _kh_, draws the single letter for that sound.

Qalezu, the Khelathi alphabet, is written right to left on code points of its own, U+1EA00 to U+1EA3F. A converter turns Latin Khelathi into those code points, and the font draws them; `tools/qalezu/encoding.json` is the one table of what each code point is, its sound and the Latin that types it.

## Licence

The fonts are licensed under the SIL Open Font License 1.1; see `LICENSE`. Under it they may be embedded in web pages, documents and books, and bundled with software, without that work taking on the font's licence.

## Setting up

Activate the repository's git hooks once per clone:

```sh
git config core.hooksPath .githooks
```

Create the virtual environment:

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

The source of each font is a UFO under `sources/`: `PirzathCarved.ufo`, `PirzathHand.ufo`, `ThuravarkRunic.ufo`, `Qalezu.ufo` and `KhelathiZethu.ufo`. Open one in FontForge, Glyphs or RoboFont to edit it. The UFO carries the outlines, the character map, the metrics and `features.fea`, which holds every OpenType feature.

Build the fonts into `fonts/`. The build is reproducible, so the committed fonts match a fresh build byte for byte:

```sh
PATH=.venv/bin:$PATH ./build.sh
```

`build.sh` runs `fontmake` and compresses the `.woff2`, once per font (`PirzathCarved` shown):

```sh
export SOURCE_DATE_EPOCH=1767225600
fontmake -u sources/PirzathCarved.ufo -o ttf --keep-overlaps --no-production-names \
    --output-path fonts/PirzathCarved-Regular.ttf
fonttools ttLib.woff2 compress -o fonts/PirzathCarved-Regular.woff2 fonts/PirzathCarved-Regular.ttf
```

Check the built fonts, render the specimens, and prove that each guard fails a broken font:

```sh
.venv/bin/python tools/pirzath/check_font.py
.venv/bin/python tools/pirzath-hand/check_font.py
.venv/bin/python tools/thuravark/check_font.py
.venv/bin/python tools/qalezu/check_font.py
.venv/bin/python tools/zethu/check_font.py
.venv/bin/python tools/pirzath/specimens.py       # specimens/pirzath/
.venv/bin/python tools/pirzath-hand/specimens.py  # specimens/pirzath-hand/
.venv/bin/python tools/thuravark/specimens.py     # specimens/thuravark/
.venv/bin/python tools/qalezu/specimens.py        # specimens/qalezu/
.venv/bin/python tools/zethu/specimens.py         # specimens/khelathi-zethu/
.venv/bin/python tools/prove_guards.py
```

Each guard shapes every form of its lexicon and asserts the font renders it rightly; the Pirzath guards read the Khazari lexicon, the Thuravark guard the Nordmal one, and Qalezu's converts the Khelathi lexicon from Latin first. Each reads its lexicon from the `origin/main` of a local thalorna checkout, `~/dev/HeroicLands/thalorna` by default:

```sh
.venv/bin/python tools/pirzath/guard.py --thalorna /path/to/thalorna
.venv/bin/python tools/pirzath-hand/guard.py --thalorna /path/to/thalorna
.venv/bin/python tools/thuravark/guard.py --thalorna /path/to/thalorna
.venv/bin/python tools/qalezu/guard.py --thalorna /path/to/thalorna
```

Qalezu's character map follows from `encoding.json`; after editing that file, `.venv/bin/python tools/qalezu/apply_encoding.py` rewrites the UFO's code points, and `--check` reports a disagreement.

Khelathi Zethu is the temple hieroglyphs of the Khelathi, on U+1EA40 to U+1EC6F and written right to left. Its guard reads no lexicon: it shapes the sample inscriptions kept in `tools/zethu/samples.json`.

```sh
.venv/bin/python tools/zethu/guard.py
```

See `design/khelathi-zethu.md`.
