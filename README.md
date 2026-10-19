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

Build a font into `fonts/` and check it:

```sh
.venv/bin/python src/build.py
.venv/bin/python src/check_font.py
```

The guard shapes every form of the Khazari lexicon and asserts the font renders it rightly. It reads the lexicon from the `origin/main` of a local thalorna checkout, `~/dev/HeroicLands/thalorna` by default:

```sh
.venv/bin/python src/guard.py --thalorna /path/to/thalorna
```
