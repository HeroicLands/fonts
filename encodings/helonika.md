# helonika encoding

Helonika Book is an alphabet of capital and small letters, written left to right. This encoding writes a roman spelling in its small letters, and a capital letter in its majuscule: `ei` and `ou` are the single letters for the long vowels, while `kh`, `zh` and doubled vowels are written as two letters.

## Fonts

- Helonika Book (`helonika-book`), written left to right.

## Running it

`encode.py` needs only Python 3.9 or later. From a checkout, or from `node_modules/@heroiclands/fonts`:

```sh
python3 encode.py --encoding helonika "kela"
python3 encode.py --encoding helonika --decode "󰌺󰌳󰌻󰌰"
```

The first command writes `󰌺󰌳󰌻󰌰`, and the second reads it back as `kela`. `--codepoints` prints the result as `U+XXXX` values, and the text may come from standard input.

From Python:

```python
import encode

text = encode.encode("helonika", "kela")
roman = encode.decode("helonika", text)
```

## Accepted characters

This encoding accepts `a-z`, `A-Z`, `0-9`, `-`, `Á`, `Ä`, `É`, `Ë`, `Í`, `Ï`, `Ó`, `Ö`, `Ú`, `Ü`, `á`, `ä`, `é`, `ë`, `í`, `ï`, `ó`, `ö`, `ú`, `ü`, and the standard's marks and whitespace. Any other character is refused at its line and column.

## Punctuation

This encoding extends the [standard roman encoding](standard.md), which every language's roman shares. The table shows how this script writes each standard mark. A mark the script draws writes its glyph; a mark it does not draw writes the standard's invisible mark, the same in every encoding, so decoding restores it.

| Mark | Meaning | Written | Code points |
| --- | --- | --- | --- |
| `.` | completes a declarative sentence, terminal | drawn, `󰍰` | U+F0370 |
| `?` | completes an interrogative sentence, terminal | drawn, `󰍰` | U+F0370 U+E0101 U+E01EF |
| `‼` | completes an imperative sentence, terminal | drawn, `󰍰` | U+F0370 U+E0102 U+E01EF |
| `!` | completes an exclamative sentence, terminal | drawn, `󰍰` | U+F0370 U+E0103 U+E01EF |
| `^` | at the beginning of a line, indents one level | invisible | U+E0104 |
| `,` | a pause that does not end the sentence | invisible | U+E0105 |
| `«` | opens an outer quotation | invisible | U+E0106 |
| `»` | closes an outer quotation | invisible | U+E0107 |
| `‹` | opens a nested quotation | invisible | U+E0108 |
| `›` | closes a nested quotation | invisible | U+E0109 |
| `—` | interrupts a sentence, non-terminal | invisible | U+E010A |
| `…` | abandons or resumes a sentence, non-terminal | invisible | U+E010B |
| `/` | verse line separator | invisible | U+E010C |
| `{` | opens a name | invisible | U+E0110 |
| `}` | closes a name | invisible | U+E0111 |

## Whitespace

In roman, outside `⟦` and `⟧`, any run of spaces, tabs and line breaks is one word separator. It is not a character of the script, and no row matches it.

This script spaces its words, so its `separator` is one space, U+0020: a separator writes one space, and decoding writes one space.

The separator is normalized on input, not preserved: `a  b` and `a\n\tb` encode as `a b` does, and decoding writes a single space.

With `--verse` or `encode(..., verse=True)`, a line ending writes the shared verse line control and a blank line writes the stanza control. `--- {.canto}` writes the canto control. See [standard.md](standard.md) for the structural assignments.

A character that no row matches is refused: `encode.py` reports it with its line and column, and writes nothing.

## Literal spans

`⟦` and `⟧` enclose character names, as the [standard](standard.md) describes: `⟦LATIN_SMALL_LETTER_A_WITH_ACUTE⟧` writes `á`. Whitespace between names only separates them.

## Vowels and conditions

The vowels are `AEIOUaeiouÁÄÉËÍÏÓÖÚÜáäéëíïóöúü`.

Where several rows begin with the same roman, the longest wins, and among rows of one length a row whose condition holds comes before a row with none. A row whose condition fails is skipped.

## Rows

The rows are in the order the file states them. A row here for a standard mark replaces the standard's row for it.

| Roman | Character | Code points |
| --- | --- | --- |
| `a` | `󰌰` | U+F0330 |
| `A` | `󰌀` | U+F0300 |
| `á` | `󰌰󠅛󠅅󠄑󠅝󠇯` | U+F0330 U+E015B U+E0145 U+E0111 U+E015D U+E01EF |
| `Á` | `󰌀󠅛󠅃󠄑󠅝󠇯` | U+F0300 U+E015B U+E0143 U+E0111 U+E015D U+E01EF |
| `ä` | `󰌰󠅛󠅅󠄔󠅝󠇯` | U+F0330 U+E015B U+E0145 U+E0114 U+E015D U+E01EF |
| `Ä` | `󰌀󠅛󠅃󠄔󠅝󠇯` | U+F0300 U+E015B U+E0143 U+E0114 U+E015D U+E01EF |
| `b` | `󰌱` | U+F0331 |
| `B` | `󰌁` | U+F0301 |
| `d` | `󰌲` | U+F0332 |
| `D` | `󰌂` | U+F0302 |
| `e` | `󰌳` | U+F0333 |
| `E` | `󰌃` | U+F0303 |
| `é` | `󰌳󠅛󠅅󠄙󠅝󠇯` | U+F0333 U+E015B U+E0145 U+E0119 U+E015D U+E01EF |
| `É` | `󰌃󠅛󠅃󠄙󠅝󠇯` | U+F0303 U+E015B U+E0143 U+E0119 U+E015D U+E01EF |
| `ë` | `󰌳󠅛󠅅󠅂󠅝󠇯` | U+F0333 U+E015B U+E0145 U+E0142 U+E015D U+E01EF |
| `Ë` | `󰌃󠅛󠅃󠅂󠅝󠇯` | U+F0303 U+E015B U+E0143 U+E0142 U+E015D U+E01EF |
| `f` | `󰌵` | U+F0335 |
| `F` | `󰌅` | U+F0305 |
| `g` | `󰌶` | U+F0336 |
| `G` | `󰌆` | U+F0306 |
| `h` | `󰌷` | U+F0337 |
| `H` | `󰌇` | U+F0307 |
| `i` | `󰌸` | U+F0338 |
| `I` | `󰌈` | U+F0308 |
| `í` | `󰌸󠅛󠅅󠅄󠅝󠇯` | U+F0338 U+E015B U+E0145 U+E0144 U+E015D U+E01EF |
| `Í` | `󰌈󠅛󠅃󠅄󠅝󠇯` | U+F0308 U+E015B U+E0143 U+E0144 U+E015D U+E01EF |
| `ï` | `󰌸󠅛󠅅󠅆󠅝󠇯` | U+F0338 U+E015B U+E0145 U+E0146 U+E015D U+E01EF |
| `Ï` | `󰌈󠅛󠅃󠅆󠅝󠇯` | U+F0308 U+E015B U+E0143 U+E0146 U+E015D U+E01EF |
| `j` | `󰌹` | U+F0339 |
| `J` | `󰌉` | U+F0309 |
| `k` | `󰌺` | U+F033A |
| `K` | `󰌊` | U+F030A |
| `l` | `󰌻` | U+F033B |
| `L` | `󰌋` | U+F030B |
| `m` | `󰌼` | U+F033C |
| `M` | `󰌌` | U+F030C |
| `n` | `󰌽` | U+F033D |
| `N` | `󰌍` | U+F030D |
| `o` | `󰌾` | U+F033E |
| `O` | `󰌎` | U+F030E |
| `ó` | `󰌾󠅛󠅆󠄓󠅝󠇯` | U+F033E U+E015B U+E0146 U+E0113 U+E015D U+E01EF |
| `Ó` | `󰌎󠅛󠅄󠄓󠅝󠇯` | U+F030E U+E015B U+E0144 U+E0113 U+E015D U+E01EF |
| `ö` | `󰌾󠅛󠅆󠄖󠅝󠇯` | U+F033E U+E015B U+E0146 U+E0116 U+E015D U+E01EF |
| `Ö` | `󰌎󠅛󠅄󠄖󠅝󠇯` | U+F030E U+E015B U+E0144 U+E0116 U+E015D U+E01EF |
| `p` | `󰍀` | U+F0340 |
| `P` | `󰌐` | U+F0310 |
| `r` | `󰍁` | U+F0341 |
| `R` | `󰌑` | U+F0311 |
| `s` | `󰍂` | U+F0342 |
| `S` | `󰌒` | U+F0312 |
| `t` | `󰍃` | U+F0343 |
| `T` | `󰌓` | U+F0313 |
| `u` | `󰍅` | U+F0345 |
| `U` | `󰌕` | U+F0315 |
| `ú` | `󰍅󠅛󠅆󠅁󠅝󠇯` | U+F0345 U+E015B U+E0146 U+E0141 U+E015D U+E01EF |
| `Ú` | `󰌕󠅛󠅄󠅁󠅝󠇯` | U+F0315 U+E015B U+E0144 U+E0141 U+E015D U+E01EF |
| `ü` | `󰍅󠅛󠅆󠅃󠅝󠇯` | U+F0345 U+E015B U+E0146 U+E0143 U+E015D U+E01EF |
| `Ü` | `󰌕󠅛󠅄󠅃󠅝󠇯` | U+F0315 U+E015B U+E0144 U+E0143 U+E015D U+E01EF |
| `v` | `󰍆` | U+F0346 |
| `V` | `󰌖` | U+F0316 |
| `z` | `󰍇` | U+F0347 |
| `Z` | `󰌗` | U+F0317 |
| `q` | `󰌺󠅑󠇯` | U+F033A U+E0151 U+E01EF |
| `Q` | `󰌊󠄱󠇯` | U+F030A U+E0131 U+E01EF |
| `y` | `󰌸󠅙󠇯` | U+F0338 U+E0159 U+E01EF |
| `Y` | `󰌈󠄹󠇯` | U+F0308 U+E0139 U+E01EF |
| `w` | `󰍅󠅗󠇯` | U+F0345 U+E0157 U+E01EF |
| `W` | `󰌕󠄷󠇯` | U+F0315 U+E0137 U+E01EF |
| `th` | `󰍄` | U+F0344 |
| `Th` | `󰌔` | U+F0314 |
| `ph` | `󰌵󠅐󠅈󠇯` | U+F0335 U+E0150 U+E0148 U+E01EF |
| `Ph` | `󰌅󠄰󠅈󠇯` | U+F0305 U+E0130 U+E0148 U+E01EF |
| `ch` | `󰍃󰍂󰌷󠅃󠅈󠇯` | U+F0343 U+F0342 U+F0337 U+E0143 U+E0148 U+E01EF |
| `Ch` | `󰌓󰍂󰌷󠄣󠅈󠇯` | U+F0313 U+F0342 U+F0337 U+E0123 U+E0148 U+E01EF |
| `ei` | `󰌴` | U+F0334 |
| `eí` | `󰌴󠅅󠅛󠅅󠅄󠅝󠇯` | U+F0334 U+E0145 U+E015B U+E0145 U+E0144 U+E015D U+E01EF |
| `éi` | `󰌴󠅛󠅅󠄙󠅝󠅉󠇯` | U+F0334 U+E015B U+E0145 U+E0119 U+E015D U+E0149 U+E01EF |
| `éí` | `󰌴󠅛󠅅󠄙󠅝󠅛󠅅󠅄󠅝󠇯` | U+F0334 U+E015B U+E0145 U+E0119 U+E015D U+E015B U+E0145 U+E0144 U+E015D U+E01EF |
| `Ei` | `󰌄` | U+F0304 |
| `Eí` | `󰌄󠄥󠅛󠅅󠅄󠅝󠇯` | U+F0304 U+E0125 U+E015B U+E0145 U+E0144 U+E015D U+E01EF |
| `Éi` | `󰌄󠅛󠅃󠄙󠅝󠅉󠇯` | U+F0304 U+E015B U+E0143 U+E0119 U+E015D U+E0149 U+E01EF |
| `Éí` | `󰌄󠅛󠅃󠄙󠅝󠅛󠅅󠅄󠅝󠇯` | U+F0304 U+E015B U+E0143 U+E0119 U+E015D U+E015B U+E0145 U+E0144 U+E015D U+E01EF |
| `ou` | `󰌿` | U+F033F |
| `oú` | `󰌿󠅏󠅛󠅆󠅁󠅝󠇯` | U+F033F U+E014F U+E015B U+E0146 U+E0141 U+E015D U+E01EF |
| `óu` | `󰌿󠅛󠅆󠄓󠅝󠅕󠇯` | U+F033F U+E015B U+E0146 U+E0113 U+E015D U+E0155 U+E01EF |
| `óú` | `󰌿󠅛󠅆󠄓󠅝󠅛󠅆󠅁󠅝󠇯` | U+F033F U+E015B U+E0146 U+E0113 U+E015D U+E015B U+E0146 U+E0141 U+E015D U+E01EF |
| `Ou` | `󰌏` | U+F030F |
| `Oú` | `󰌏󠄯󠅛󠅆󠅁󠅝󠇯` | U+F030F U+E012F U+E015B U+E0146 U+E0141 U+E015D U+E01EF |
| `Óu` | `󰌏󠅛󠅄󠄓󠅝󠅕󠇯` | U+F030F U+E015B U+E0144 U+E0113 U+E015D U+E0155 U+E01EF |
| `Óú` | `󰌏󠅛󠅄󠄓󠅝󠅛󠅆󠅁󠅝󠇯` | U+F030F U+E015B U+E0144 U+E0113 U+E015D U+E015B U+E0146 U+E0141 U+E015D U+E01EF |
| `.` | `󰍰` | U+F0370 |
| `?` | `󰍰󠄁󠇯` | U+F0370 U+E0101 U+E01EF |
| `‼` | `󰍰󠄂󠇯` | U+F0370 U+E0102 U+E01EF |
| `!` | `󰍰󠄃󠇯` | U+F0370 U+E0103 U+E01EF |
| `-` | `󠅛󠄒󠅄󠅝` | U+E015B U+E0112 U+E0144 U+E015D |
| `0` | `󰍠` | U+F0360 |
| `1` | `󰍡` | U+F0361 |
| `2` | `󰍢` | U+F0362 |
| `3` | `󰍣` | U+F0363 |
| `4` | `󰍤` | U+F0364 |
| `5` | `󰍥` | U+F0365 |
| `6` | `󰍦` | U+F0366 |
| `7` | `󰍧` | U+F0367 |
| `8` | `󰍨` | U+F0368 |
| `9` | `󰍩` | U+F0369 |

## Round trip

Every encoding round-trips exactly: decoding the code points that encoding wrote gives back the roman text, and encoding that gives the same code points. The Code points column shows every character a row writes, including any that is invisible.

This page is written from `encodings/helonika.json` by `tools/encoding_docs.py`.
