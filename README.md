# heroiclands-fonts

Fonts for the scripts of the HeroicLands settings, drawn from scratch so that a setting's inscriptions can be shown in their own letters on the sites, in the books and in Foundry.

Each font draws its script over the setting's Latin spelling. Text stays plain, readable and searchable, and a passage switches to the script by its font alone. A letter pair that the spelling uses for one sound, such as _th_ or _kh_, draws the single letter for that sound.

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

The source of each font is a UFO under `sources/`: `PirzathCarved.ufo` and `ThuravarkRunic.ufo`. Open one in FontForge, Glyphs or RoboFont to edit it. The UFO carries the outlines, the character map, the metrics and `features.fea`, which holds every OpenType feature.

Build both fonts into `fonts/` and `thuravark/fonts/`. The build is reproducible, so the committed fonts match a fresh build byte for byte:

```sh
PATH=.venv/bin:$PATH ./build.sh
```

`build.sh` runs `fontmake` and compresses the `.woff2`, once per font:

```sh
export SOURCE_DATE_EPOCH=1767225600
fontmake -u sources/PirzathCarved.ufo -o ttf --keep-overlaps --no-production-names \
    --output-path fonts/PirzathCarved-Regular.ttf
fonttools ttLib.woff2 compress -o fonts/PirzathCarved-Regular.woff2 fonts/PirzathCarved-Regular.ttf
```

Check the built fonts, render the specimens, and prove that each guard fails a font without its layout:

```sh
.venv/bin/python src/check_font.py
.venv/bin/python thuravark/src/check_font.py
.venv/bin/python src/specimens.py            # specimens/pirzath/
.venv/bin/python thuravark/src/specimens.py  # specimens/thuravark/
.venv/bin/python src/prove_guards.py
```

The guard shapes every form of the Khazari lexicon and asserts the font renders it rightly. It reads the lexicon from the `origin/main` of a local thalorna checkout, `~/dev/HeroicLands/thalorna` by default:

```sh
.venv/bin/python src/guard.py --thalorna /path/to/thalorna
.venv/bin/python thuravark/src/guard.py --thalorna /path/to/thalorna
```
