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

This encoding accepts `a-z`, `A-Z`, `0-9`, `-`, `Á`, `Ä`, `É`, `Ë`, `Í`, `Ï`, `Ó`, `Ö`, `Ú`, `Ü`, `á`, `ä`, `é`, `ë`, `í`, `ï`, `ó`, `ö`, `ú`, `ü`, (space), `!`, `,`, `.`, `/`, `?`, `^`, `{`, `}`, `«`, `»`, `—`, `…`, `‹`, `›`, `‼`, and the standard's marks and whitespace. Any other character is refused at its line and column.

## Punctuation

This encoding includes the [standard roman punctuation](standard.md), which every language's roman shares. The table shows how this script writes each standard mark. A mark the script draws writes its glyph; a mark it does not draw writes the standard's invisible mark, the same in every encoding, so decoding restores it.

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

`⟦` and `⟧` enclose this encoding's own codes or `U+XXXX` code points: `⟦U+00E1⟧` writes `á`. A scalar has four to six uppercase hexadecimal digits. `controls.literalEscape` quotes literal open, close and escape controls inside the payload. The file's `codes` rows give its named signs and notation; whitespace between codes only separates them. Other names and standard punctuation are refused.

## Vowels and conditions

The vowels are `AEIOUaeiouÁÄÉËÍÏÓÖÚÜáäéëíïóöúü`.

Where several rows begin with the same roman, the longest wins, and among rows of one length a row whose condition holds comes before a row with none. A row whose condition fails is skipped.

## Rows

The rows are in the order the file states them. A row here for a standard mark replaces the standard's row for it.

| Roman | Character | Code points | When |
| --- | --- | --- | --- |
| `^` | `󠄄` | U+E0104 | at the beginning of a line |
| `,` | `󠄅` | U+E0105 | always |
| `«` | `󠄆` | U+E0106 | always |
| `»` | `󠄇` | U+E0107 | always |
| `‹` | `󠄈` | U+E0108 | always |
| `›` | `󠄉` | U+E0109 | always |
| `—` | `󠄊` | U+E010A | always |
| `…` | `󠄋` | U+E010B | always |
| `/` | `󠄌` | U+E010C | always |
| `{` | `󠄐` | U+E0110 | always |
| `}` | `󠄑` | U+E0111 | always |
| `a` | `󰌰` | U+F0330 | always |
| `A` | `󰌀` | U+F0300 | always |
| `á` | `󰌰󠅛󠅅󠄑󠅝󠇯` | U+F0330 U+E015B U+E0145 U+E0111 U+E015D U+E01EF | always |
| `Á` | `󰌀󠅛󠅃󠄑󠅝󠇯` | U+F0300 U+E015B U+E0143 U+E0111 U+E015D U+E01EF | always |
| `ä` | `󰌰󠅛󠅅󠄔󠅝󠇯` | U+F0330 U+E015B U+E0145 U+E0114 U+E015D U+E01EF | always |
| `Ä` | `󰌀󠅛󠅃󠄔󠅝󠇯` | U+F0300 U+E015B U+E0143 U+E0114 U+E015D U+E01EF | always |
| `b` | `󰌱` | U+F0331 | always |
| `B` | `󰌁` | U+F0301 | always |
| `d` | `󰌲` | U+F0332 | always |
| `D` | `󰌂` | U+F0302 | always |
| `e` | `󰌳` | U+F0333 | always |
| `E` | `󰌃` | U+F0303 | always |
| `é` | `󰌳󠅛󠅅󠄙󠅝󠇯` | U+F0333 U+E015B U+E0145 U+E0119 U+E015D U+E01EF | always |
| `É` | `󰌃󠅛󠅃󠄙󠅝󠇯` | U+F0303 U+E015B U+E0143 U+E0119 U+E015D U+E01EF | always |
| `ë` | `󰌳󠅛󠅅󠅂󠅝󠇯` | U+F0333 U+E015B U+E0145 U+E0142 U+E015D U+E01EF | always |
| `Ë` | `󰌃󠅛󠅃󠅂󠅝󠇯` | U+F0303 U+E015B U+E0143 U+E0142 U+E015D U+E01EF | always |
| `f` | `󰌵` | U+F0335 | always |
| `F` | `󰌅` | U+F0305 | always |
| `g` | `󰌶` | U+F0336 | always |
| `G` | `󰌆` | U+F0306 | always |
| `h` | `󰌷` | U+F0337 | always |
| `H` | `󰌇` | U+F0307 | always |
| `i` | `󰌸` | U+F0338 | always |
| `I` | `󰌈` | U+F0308 | always |
| `í` | `󰌸󠅛󠅅󠅄󠅝󠇯` | U+F0338 U+E015B U+E0145 U+E0144 U+E015D U+E01EF | always |
| `Í` | `󰌈󠅛󠅃󠅄󠅝󠇯` | U+F0308 U+E015B U+E0143 U+E0144 U+E015D U+E01EF | always |
| `ï` | `󰌸󠅛󠅅󠅆󠅝󠇯` | U+F0338 U+E015B U+E0145 U+E0146 U+E015D U+E01EF | always |
| `Ï` | `󰌈󠅛󠅃󠅆󠅝󠇯` | U+F0308 U+E015B U+E0143 U+E0146 U+E015D U+E01EF | always |
| `j` | `󰌹` | U+F0339 | always |
| `J` | `󰌉` | U+F0309 | always |
| `k` | `󰌺` | U+F033A | always |
| `K` | `󰌊` | U+F030A | always |
| `l` | `󰌻` | U+F033B | always |
| `L` | `󰌋` | U+F030B | always |
| `m` | `󰌼` | U+F033C | always |
| `M` | `󰌌` | U+F030C | always |
| `n` | `󰌽` | U+F033D | always |
| `N` | `󰌍` | U+F030D | always |
| `o` | `󰌾` | U+F033E | always |
| `O` | `󰌎` | U+F030E | always |
| `ó` | `󰌾󠅛󠅆󠄓󠅝󠇯` | U+F033E U+E015B U+E0146 U+E0113 U+E015D U+E01EF | always |
| `Ó` | `󰌎󠅛󠅄󠄓󠅝󠇯` | U+F030E U+E015B U+E0144 U+E0113 U+E015D U+E01EF | always |
| `ö` | `󰌾󠅛󠅆󠄖󠅝󠇯` | U+F033E U+E015B U+E0146 U+E0116 U+E015D U+E01EF | always |
| `Ö` | `󰌎󠅛󠅄󠄖󠅝󠇯` | U+F030E U+E015B U+E0144 U+E0116 U+E015D U+E01EF | always |
| `p` | `󰍀` | U+F0340 | always |
| `P` | `󰌐` | U+F0310 | always |
| `r` | `󰍁` | U+F0341 | always |
| `R` | `󰌑` | U+F0311 | always |
| `s` | `󰍂` | U+F0342 | always |
| `S` | `󰌒` | U+F0312 | always |
| `t` | `󰍃` | U+F0343 | always |
| `T` | `󰌓` | U+F0313 | always |
| `u` | `󰍅` | U+F0345 | always |
| `U` | `󰌕` | U+F0315 | always |
| `ú` | `󰍅󠅛󠅆󠅁󠅝󠇯` | U+F0345 U+E015B U+E0146 U+E0141 U+E015D U+E01EF | always |
| `Ú` | `󰌕󠅛󠅄󠅁󠅝󠇯` | U+F0315 U+E015B U+E0144 U+E0141 U+E015D U+E01EF | always |
| `ü` | `󰍅󠅛󠅆󠅃󠅝󠇯` | U+F0345 U+E015B U+E0146 U+E0143 U+E015D U+E01EF | always |
| `Ü` | `󰌕󠅛󠅄󠅃󠅝󠇯` | U+F0315 U+E015B U+E0144 U+E0143 U+E015D U+E01EF | always |
| `v` | `󰍆` | U+F0346 | always |
| `V` | `󰌖` | U+F0316 | always |
| `z` | `󰍇` | U+F0347 | always |
| `Z` | `󰌗` | U+F0317 | always |
| `q` | `󰌺󠅑󠇯` | U+F033A U+E0151 U+E01EF | always |
| `Q` | `󰌊󠄱󠇯` | U+F030A U+E0131 U+E01EF | always |
| `y` | `󰌸󠅙󠇯` | U+F0338 U+E0159 U+E01EF | always |
| `Y` | `󰌈󠄹󠇯` | U+F0308 U+E0139 U+E01EF | always |
| `w` | `󰍅󠅗󠇯` | U+F0345 U+E0157 U+E01EF | always |
| `W` | `󰌕󠄷󠇯` | U+F0315 U+E0137 U+E01EF | always |
| `th` | `󰍄` | U+F0344 | always |
| `Th` | `󰌔` | U+F0314 | always |
| `ph` | `󰌵󠅐󠅈󠇯` | U+F0335 U+E0150 U+E0148 U+E01EF | always |
| `Ph` | `󰌅󠄰󠅈󠇯` | U+F0305 U+E0130 U+E0148 U+E01EF | always |
| `ch` | `󰍃󰍂󰌷󠅃󠅈󠇯` | U+F0343 U+F0342 U+F0337 U+E0143 U+E0148 U+E01EF | always |
| `Ch` | `󰌓󰍂󰌷󠄣󠅈󠇯` | U+F0313 U+F0342 U+F0337 U+E0123 U+E0148 U+E01EF | always |
| `ei` | `󰌴` | U+F0334 | always |
| `eí` | `󰌴󠅅󠅛󠅅󠅄󠅝󠇯` | U+F0334 U+E0145 U+E015B U+E0145 U+E0144 U+E015D U+E01EF | always |
| `éi` | `󰌴󠅛󠅅󠄙󠅝󠅉󠇯` | U+F0334 U+E015B U+E0145 U+E0119 U+E015D U+E0149 U+E01EF | always |
| `éí` | `󰌴󠅛󠅅󠄙󠅝󠅛󠅅󠅄󠅝󠇯` | U+F0334 U+E015B U+E0145 U+E0119 U+E015D U+E015B U+E0145 U+E0144 U+E015D U+E01EF | always |
| `Ei` | `󰌄` | U+F0304 | always |
| `Eí` | `󰌄󠄥󠅛󠅅󠅄󠅝󠇯` | U+F0304 U+E0125 U+E015B U+E0145 U+E0144 U+E015D U+E01EF | always |
| `Éi` | `󰌄󠅛󠅃󠄙󠅝󠅉󠇯` | U+F0304 U+E015B U+E0143 U+E0119 U+E015D U+E0149 U+E01EF | always |
| `Éí` | `󰌄󠅛󠅃󠄙󠅝󠅛󠅅󠅄󠅝󠇯` | U+F0304 U+E015B U+E0143 U+E0119 U+E015D U+E015B U+E0145 U+E0144 U+E015D U+E01EF | always |
| `ou` | `󰌿` | U+F033F | always |
| `oú` | `󰌿󠅏󠅛󠅆󠅁󠅝󠇯` | U+F033F U+E014F U+E015B U+E0146 U+E0141 U+E015D U+E01EF | always |
| `óu` | `󰌿󠅛󠅆󠄓󠅝󠅕󠇯` | U+F033F U+E015B U+E0146 U+E0113 U+E015D U+E0155 U+E01EF | always |
| `óú` | `󰌿󠅛󠅆󠄓󠅝󠅛󠅆󠅁󠅝󠇯` | U+F033F U+E015B U+E0146 U+E0113 U+E015D U+E015B U+E0146 U+E0141 U+E015D U+E01EF | always |
| `Ou` | `󰌏` | U+F030F | always |
| `Oú` | `󰌏󠄯󠅛󠅆󠅁󠅝󠇯` | U+F030F U+E012F U+E015B U+E0146 U+E0141 U+E015D U+E01EF | always |
| `Óu` | `󰌏󠅛󠅄󠄓󠅝󠅕󠇯` | U+F030F U+E015B U+E0144 U+E0113 U+E015D U+E0155 U+E01EF | always |
| `Óú` | `󰌏󠅛󠅄󠄓󠅝󠅛󠅆󠅁󠅝󠇯` | U+F030F U+E015B U+E0144 U+E0113 U+E015D U+E015B U+E0146 U+E0141 U+E015D U+E01EF | always |
| `.` | `󰍰` | U+F0370 | always |
| `?` | `󰍰󠄁󠇯` | U+F0370 U+E0101 U+E01EF | always |
| `‼` | `󰍰󠄂󠇯` | U+F0370 U+E0102 U+E01EF | always |
| `!` | `󰍰󠄃󠇯` | U+F0370 U+E0103 U+E01EF | always |
| `-` | `󠅛󠄒󠅄󠅝` | U+E015B U+E0112 U+E0144 U+E015D | always |
| `0` | `󰍠` | U+F0360 | always |
| `1` | `󰍡` | U+F0361 | always |
| `2` | `󰍢` | U+F0362 | always |
| `3` | `󰍣` | U+F0363 | always |
| `4` | `󰍤` | U+F0364 | always |
| `5` | `󰍥` | U+F0365 | always |
| `6` | `󰍦` | U+F0366 | always |
| `7` | `󰍧` | U+F0367 | always |
| `8` | `󰍨` | U+F0368 | always |
| `9` | `󰍩` | U+F0369 | always |
| (space) | (space) | U+0020 | always |

## Round trip

Every encoding round-trips exactly: decoding the code points that encoding wrote gives back the roman text, and encoding that gives the same code points. The Code points column shows every character a row writes, including any that is invisible.

This page is written from `encodings/helonika.json` by `tools/encoding_docs.py`.
