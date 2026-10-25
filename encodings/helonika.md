# helonika encoding

Helonika Book is an alphabet of capital and small letters, written left to right. This encoding writes a roman spelling in its letters: `ei` and `ou` are the single letters for the long vowels, while `kh`, `zh` and doubled vowels are written as two letters.

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

## Vowels and conditions

The vowels are `AEIOUaeiouÁÄÉËÍÏÓÖÚÜáäéëíïóöúü`.

## Rows

The rows are in the order the file states them.

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
| `tH` | `󰍄󠅔󠄨󠇯` | U+F0344 U+E0154 U+E0128 U+E01EF |
| `Th` | `󰌔` | U+F0314 |
| `TH` | `󰌔󠄴󠄨󠇯` | U+F0314 U+E0134 U+E0128 U+E01EF |
| `ph` | `󰌵󠅐󠅈󠇯` | U+F0335 U+E0150 U+E0148 U+E01EF |
| `pH` | `󰌵󠅐󠄨󠇯` | U+F0335 U+E0150 U+E0128 U+E01EF |
| `Ph` | `󰌅󠄰󠅈󠇯` | U+F0305 U+E0130 U+E0148 U+E01EF |
| `PH` | `󰌅󠄰󠄨󠇯` | U+F0305 U+E0130 U+E0128 U+E01EF |
| `ch` | `󰍃󰍂󰌷󠅃󠅈󠇯` | U+F0343 U+F0342 U+F0337 U+E0143 U+E0148 U+E01EF |
| `cH` | `󰍃󰍂󰌷󠅃󠄨󠇯` | U+F0343 U+F0342 U+F0337 U+E0143 U+E0128 U+E01EF |
| `Ch` | `󰌓󰍂󰌷󠄣󠅈󠇯` | U+F0313 U+F0342 U+F0337 U+E0123 U+E0148 U+E01EF |
| `CH` | `󰌓󰍂󰌷󠄣󠄨󠇯` | U+F0313 U+F0342 U+F0337 U+E0123 U+E0128 U+E01EF |
| `ei` | `󰌴` | U+F0334 |
| `eí` | `󰌴󠅅󠅛󠅅󠅄󠅝󠇯` | U+F0334 U+E0145 U+E015B U+E0145 U+E0144 U+E015D U+E01EF |
| `eI` | `󰌴󠅅󠄩󠇯` | U+F0334 U+E0145 U+E0129 U+E01EF |
| `eÍ` | `󰌴󠅅󠅛󠅃󠅄󠅝󠇯` | U+F0334 U+E0145 U+E015B U+E0143 U+E0144 U+E015D U+E01EF |
| `éi` | `󰌴󠅛󠅅󠄙󠅝󠅉󠇯` | U+F0334 U+E015B U+E0145 U+E0119 U+E015D U+E0149 U+E01EF |
| `éí` | `󰌴󠅛󠅅󠄙󠅝󠅛󠅅󠅄󠅝󠇯` | U+F0334 U+E015B U+E0145 U+E0119 U+E015D U+E015B U+E0145 U+E0144 U+E015D U+E01EF |
| `éI` | `󰌴󠅛󠅅󠄙󠅝󠄩󠇯` | U+F0334 U+E015B U+E0145 U+E0119 U+E015D U+E0129 U+E01EF |
| `éÍ` | `󰌴󠅛󠅅󠄙󠅝󠅛󠅃󠅄󠅝󠇯` | U+F0334 U+E015B U+E0145 U+E0119 U+E015D U+E015B U+E0143 U+E0144 U+E015D U+E01EF |
| `Ei` | `󰌄` | U+F0304 |
| `Eí` | `󰌄󠄥󠅛󠅅󠅄󠅝󠇯` | U+F0304 U+E0125 U+E015B U+E0145 U+E0144 U+E015D U+E01EF |
| `EI` | `󰌄󠄥󠄩󠇯` | U+F0304 U+E0125 U+E0129 U+E01EF |
| `EÍ` | `󰌄󠄥󠅛󠅃󠅄󠅝󠇯` | U+F0304 U+E0125 U+E015B U+E0143 U+E0144 U+E015D U+E01EF |
| `Éi` | `󰌄󠅛󠅃󠄙󠅝󠅉󠇯` | U+F0304 U+E015B U+E0143 U+E0119 U+E015D U+E0149 U+E01EF |
| `Éí` | `󰌄󠅛󠅃󠄙󠅝󠅛󠅅󠅄󠅝󠇯` | U+F0304 U+E015B U+E0143 U+E0119 U+E015D U+E015B U+E0145 U+E0144 U+E015D U+E01EF |
| `ÉI` | `󰌄󠅛󠅃󠄙󠅝󠄩󠇯` | U+F0304 U+E015B U+E0143 U+E0119 U+E015D U+E0129 U+E01EF |
| `ÉÍ` | `󰌄󠅛󠅃󠄙󠅝󠅛󠅃󠅄󠅝󠇯` | U+F0304 U+E015B U+E0143 U+E0119 U+E015D U+E015B U+E0143 U+E0144 U+E015D U+E01EF |
| `ou` | `󰌿` | U+F033F |
| `oú` | `󰌿󠅏󠅛󠅆󠅁󠅝󠇯` | U+F033F U+E014F U+E015B U+E0146 U+E0141 U+E015D U+E01EF |
| `oU` | `󰌿󠅏󠄵󠇯` | U+F033F U+E014F U+E0135 U+E01EF |
| `oÚ` | `󰌿󠅏󠅛󠅄󠅁󠅝󠇯` | U+F033F U+E014F U+E015B U+E0144 U+E0141 U+E015D U+E01EF |
| `óu` | `󰌿󠅛󠅆󠄓󠅝󠅕󠇯` | U+F033F U+E015B U+E0146 U+E0113 U+E015D U+E0155 U+E01EF |
| `óú` | `󰌿󠅛󠅆󠄓󠅝󠅛󠅆󠅁󠅝󠇯` | U+F033F U+E015B U+E0146 U+E0113 U+E015D U+E015B U+E0146 U+E0141 U+E015D U+E01EF |
| `óU` | `󰌿󠅛󠅆󠄓󠅝󠄵󠇯` | U+F033F U+E015B U+E0146 U+E0113 U+E015D U+E0135 U+E01EF |
| `óÚ` | `󰌿󠅛󠅆󠄓󠅝󠅛󠅄󠅁󠅝󠇯` | U+F033F U+E015B U+E0146 U+E0113 U+E015D U+E015B U+E0144 U+E0141 U+E015D U+E01EF |
| `Ou` | `󰌏` | U+F030F |
| `Oú` | `󰌏󠄯󠅛󠅆󠅁󠅝󠇯` | U+F030F U+E012F U+E015B U+E0146 U+E0141 U+E015D U+E01EF |
| `OU` | `󰌏󠄯󠄵󠇯` | U+F030F U+E012F U+E0135 U+E01EF |
| `OÚ` | `󰌏󠄯󠅛󠅄󠅁󠅝󠇯` | U+F030F U+E012F U+E015B U+E0144 U+E0141 U+E015D U+E01EF |
| `Óu` | `󰌏󠅛󠅄󠄓󠅝󠅕󠇯` | U+F030F U+E015B U+E0144 U+E0113 U+E015D U+E0155 U+E01EF |
| `Óú` | `󰌏󠅛󠅄󠄓󠅝󠅛󠅆󠅁󠅝󠇯` | U+F030F U+E015B U+E0144 U+E0113 U+E015D U+E015B U+E0146 U+E0141 U+E015D U+E01EF |
| `ÓU` | `󰌏󠅛󠅄󠄓󠅝󠄵󠇯` | U+F030F U+E015B U+E0144 U+E0113 U+E015D U+E0135 U+E01EF |
| `ÓÚ` | `󰌏󠅛󠅄󠄓󠅝󠅛󠅄󠅁󠅝󠇯` | U+F030F U+E015B U+E0144 U+E0113 U+E015D U+E015B U+E0144 U+E0141 U+E015D U+E01EF |
| `. ` | `󰍰` | U+F0370 |
| `.` | `󰍰󠄎󠇯` | U+F0370 U+E010E U+E01EF |
| `,` | `󠄌` | U+E010C |
| `—` | `󠅛󠄒󠄐󠄑󠄔󠅝` | U+E015B U+E0112 U+E0110 U+E0111 U+E0114 U+E015D |
| `–` | `󠅛󠄒󠄐󠄑󠄓󠅝` | U+E015B U+E0112 U+E0110 U+E0111 U+E0113 U+E015D |
| `-` | `󠄍` | U+E010D |
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
