# aelwythi-semaron encoding

A second roman spelling for Semaron Kuriale, which draws the same letters as the semaron encoding. It takes each roman letter on its own where semaron joins them: a doubled vowel is two vowels, `c` is written as s before `e`, `i` and `y` and as k elsewhere, and `ch` and `tch` are written with the letters for t, s and h. The apostrophe and the quotation mark draw nothing and are written as invisible marks, and a hyphen draws a space and carries a mark.

## Fonts

- Semaron Kuriale (`semaron-kuriale`), written left to right.

## Running it

`encode.py` needs only Python 3.9 or later. From a checkout, or from `node_modules/@heroiclands/fonts`:

```sh
python3 encode.py --encoding aelwythi-semaron "thalen kal"
python3 encode.py --encoding aelwythi-semaron --decode "󰉐󰈰󰈺󰈳󰈼 󰈹󠅋󠇯󰈰󰈺"
```

The first command writes `󰉐󰈰󰈺󰈳󰈼 󰈹󠅋󠇯󰈰󰈺`, and the second reads it back as `thalen kal`. `--codepoints` prints the result as `U+XXXX` values, and the text may come from standard input.

From Python:

```python
import encode

text = encode.encode("aelwythi-semaron", "thalen kal")
roman = encode.decode("aelwythi-semaron", text)
```

## Vowels and conditions

The vowels are `AEIOUYaeiouy`.

## Rows

The rows are in the order the file states them.

| Roman | Character | Code points |
| --- | --- | --- |
| `tch` | `󰉁󰉀󰈶󠅔󠅃󠅈󠇯` | U+F0241 U+F0240 U+F0236 U+E0154 U+E0143 U+E0148 U+E01EF |
| `tcH` | `󰉁󰉀󰈶󠅔󠅃󠄨󠇯` | U+F0241 U+F0240 U+F0236 U+E0154 U+E0143 U+E0128 U+E01EF |
| `tCh` | `󰉁󰉀󰈶󠅔󠄣󠅈󠇯` | U+F0241 U+F0240 U+F0236 U+E0154 U+E0123 U+E0148 U+E01EF |
| `tCH` | `󰉁󰉀󰈶󠅔󠄣󠄨󠇯` | U+F0241 U+F0240 U+F0236 U+E0154 U+E0123 U+E0128 U+E01EF |
| `Tch` | `󰈑󰉀󰈶󠄴󠅃󠅈󠇯` | U+F0211 U+F0240 U+F0236 U+E0134 U+E0143 U+E0148 U+E01EF |
| `TcH` | `󰈑󰉀󰈶󠄴󠅃󠄨󠇯` | U+F0211 U+F0240 U+F0236 U+E0134 U+E0143 U+E0128 U+E01EF |
| `TCh` | `󰈑󰉀󰈶󠄴󠄣󠅈󠇯` | U+F0211 U+F0240 U+F0236 U+E0134 U+E0123 U+E0148 U+E01EF |
| `TCH` | `󰈑󰉀󰈶󠄴󠄣󠄨󠇯` | U+F0211 U+F0240 U+F0236 U+E0134 U+E0123 U+E0128 U+E01EF |
| `ch` | `󰉁󰉀󰈶󠅃󠅈󠇯` | U+F0241 U+F0240 U+F0236 U+E0143 U+E0148 U+E01EF |
| `cH` | `󰉁󰉀󰈶󠅃󠄨󠇯` | U+F0241 U+F0240 U+F0236 U+E0143 U+E0128 U+E01EF |
| `Ch` | `󰈑󰉀󰈶󠄣󠅈󠇯` | U+F0211 U+F0240 U+F0236 U+E0123 U+E0148 U+E01EF |
| `CH` | `󰈑󰉀󰈶󠄣󠄨󠇯` | U+F0211 U+F0240 U+F0236 U+E0123 U+E0128 U+E01EF |
| `qu` | `󰈹󰉄󠅑󠅕󠇯` | U+F0239 U+F0244 U+E0151 U+E0155 U+E01EF |
| `qU` | `󰈹󰉄󠅑󠄵󠇯` | U+F0239 U+F0244 U+E0151 U+E0135 U+E01EF |
| `Qu` | `󰈉󰉄󠄱󠅕󠇯` | U+F0209 U+F0244 U+E0131 U+E0155 U+E01EF |
| `QU` | `󰈉󰈔󠄱󠄵󠇯` | U+F0209 U+F0214 U+E0131 U+E0135 U+E01EF |
| `th` | `󰉐` | U+F0250 |
| `tH` | `󰉐󠅔󠄨󠇯` | U+F0250 U+E0154 U+E0128 U+E01EF |
| `Th` | `󰉑` | U+F0251 |
| `TH` | `󰉑󠄴󠄨󠇯` | U+F0251 U+E0134 U+E0128 U+E01EF |
| `ce` | `󰉀󰈳󠅃󠅅󠇯` | U+F0240 U+F0233 U+E0143 U+E0145 U+E01EF |
| `cE` | `󰉀󰈃󠅃󠄥󠇯` | U+F0240 U+F0203 U+E0143 U+E0125 U+E01EF |
| `Ce` | `󰈐󰈳󠄣󠅅󠇯` | U+F0210 U+F0233 U+E0123 U+E0145 U+E01EF |
| `CE` | `󰈐󰈃󠄣󠄥󠇯` | U+F0210 U+F0203 U+E0123 U+E0125 U+E01EF |
| `ci` | `󰉀󰈷󠅃󠅉󠇯` | U+F0240 U+F0237 U+E0143 U+E0149 U+E01EF |
| `cI` | `󰉀󰈇󠅃󠄩󠇯` | U+F0240 U+F0207 U+E0143 U+E0129 U+E01EF |
| `Ci` | `󰈐󰈷󠄣󠅉󠇯` | U+F0210 U+F0237 U+E0123 U+E0149 U+E01EF |
| `CI` | `󰈐󰈇󠄣󠄩󠇯` | U+F0210 U+F0207 U+E0123 U+E0129 U+E01EF |
| `cy` | `󰉀󰉅󠅃󠅙󠇯` | U+F0240 U+F0245 U+E0143 U+E0159 U+E01EF |
| `cY` | `󰉀󰈕󠅃󠄹󠇯` | U+F0240 U+F0215 U+E0143 U+E0139 U+E01EF |
| `Cy` | `󰈐󰉅󠄣󠅙󠇯` | U+F0210 U+F0245 U+E0123 U+E0159 U+E01EF |
| `CY` | `󰈐󰈕󠄣󠄹󠇯` | U+F0210 U+F0215 U+E0123 U+E0139 U+E01EF |
| `a` | `󰈰` | U+F0230 |
| `A` | `󰈀` | U+F0200 |
| `b` | `󰈱` | U+F0231 |
| `B` | `󰈁` | U+F0201 |
| `c` | `󰈹` | U+F0239 |
| `C` | `󰈉` | U+F0209 |
| `d` | `󰈲` | U+F0232 |
| `D` | `󰈂` | U+F0202 |
| `e` | `󰈳` | U+F0233 |
| `E` | `󰈃` | U+F0203 |
| `f` | `󰈴` | U+F0234 |
| `F` | `󰈄` | U+F0204 |
| `g` | `󰈵` | U+F0235 |
| `G` | `󰈅` | U+F0205 |
| `h` | `󰈶` | U+F0236 |
| `H` | `󰈆` | U+F0206 |
| `i` | `󰈷` | U+F0237 |
| `I` | `󰈇` | U+F0207 |
| `j` | `󰈸` | U+F0238 |
| `J` | `󰈈` | U+F0208 |
| `k` | `󰈹󠅋󠇯` | U+F0239 U+E014B U+E01EF |
| `K` | `󰈉󠄫󠇯` | U+F0209 U+E012B U+E01EF |
| `l` | `󰈺` | U+F023A |
| `L` | `󰈊` | U+F020A |
| `m` | `󰈻` | U+F023B |
| `M` | `󰈋` | U+F020B |
| `n` | `󰈼` | U+F023C |
| `N` | `󰈌` | U+F020C |
| `o` | `󰈽` | U+F023D |
| `O` | `󰈍` | U+F020D |
| `p` | `󰈾` | U+F023E |
| `P` | `󰈎` | U+F020E |
| `q` | `󰈹󠅑󠇯` | U+F0239 U+E0151 U+E01EF |
| `Q` | `󰈉󠄱󠇯` | U+F0209 U+E0131 U+E01EF |
| `r` | `󰈿` | U+F023F |
| `R` | `󰈏` | U+F020F |
| `s` | `󰉀` | U+F0240 |
| `S` | `󰈐` | U+F0210 |
| `t` | `󰉁` | U+F0241 |
| `T` | `󰈑` | U+F0211 |
| `u` | `󰉂` | U+F0242 |
| `U` | `󰈒` | U+F0212 |
| `v` | `󰉃` | U+F0243 |
| `V` | `󰈓` | U+F0213 |
| `w` | `󰉄` | U+F0244 |
| `W` | `󰈔` | U+F0214 |
| `x` | `󰈹󰉀󠅘󠇯` | U+F0239 U+F0240 U+E0158 U+E01EF |
| `X` | `󰈉󰈐󠄸󠇯` | U+F0209 U+F0210 U+E0138 U+E01EF |
| `y` | `󰉅` | U+F0245 |
| `Y` | `󰈕` | U+F0215 |
| `z` | `󰉆` | U+F0246 |
| `Z` | `󰈖` | U+F0216 |
| `á` | `󰈰󠅛󠅅󠄑󠅝󠇯` | U+F0230 U+E015B U+E0145 U+E0111 U+E015D U+E01EF |
| `Á` | `󰈀󠅛󠅃󠄑󠅝󠇯` | U+F0200 U+E015B U+E0143 U+E0111 U+E015D U+E01EF |
| `é` | `󰈳󠅛󠅅󠄙󠅝󠇯` | U+F0233 U+E015B U+E0145 U+E0119 U+E015D U+E01EF |
| `É` | `󰈃󠅛󠅃󠄙󠅝󠇯` | U+F0203 U+E015B U+E0143 U+E0119 U+E015D U+E01EF |
| `í` | `󰈷󠅛󠅅󠅄󠅝󠇯` | U+F0237 U+E015B U+E0145 U+E0144 U+E015D U+E01EF |
| `Í` | `󰈇󠅛󠅃󠅄󠅝󠇯` | U+F0207 U+E015B U+E0143 U+E0144 U+E015D U+E01EF |
| `ó` | `󰈽󠅛󠅆󠄓󠅝󠇯` | U+F023D U+E015B U+E0146 U+E0113 U+E015D U+E01EF |
| `Ó` | `󰈍󠅛󠅄󠄓󠅝󠇯` | U+F020D U+E015B U+E0144 U+E0113 U+E015D U+E01EF |
| `ú` | `󰉂󠅛󠅆󠅁󠅝󠇯` | U+F0242 U+E015B U+E0146 U+E0141 U+E015D U+E01EF |
| `Ú` | `󰈒󠅛󠅄󠅁󠅝󠇯` | U+F0212 U+E015B U+E0144 U+E0141 U+E015D U+E01EF |
| `ë` | `󰈳󠅛󠅅󠅂󠅝󠇯` | U+F0233 U+E015B U+E0145 U+E0142 U+E015D U+E01EF |
| `Ë` | `󰈃󠅛󠅃󠅂󠅝󠇯` | U+F0203 U+E015B U+E0143 U+E0142 U+E015D U+E01EF |
| `0` | `󰉘` | U+F0258 |
| `1` | `󰉙` | U+F0259 |
| `2` | `󰉚` | U+F025A |
| `3` | `󰉛` | U+F025B |
| `4` | `󰉜` | U+F025C |
| `5` | `󰉝` | U+F025D |
| `6` | `󰉞` | U+F025E |
| `7` | `󰉟` | U+F025F |
| `8` | `󰉠` | U+F0260 |
| `9` | `󰉡` | U+F0261 |
| `.` | `󰉨` | U+F0268 |
| `"` | `󠄂` | U+E0102 |
| `“` | `󠅛󠄒󠄐󠄑󠅃󠅝` | U+E015B U+E0112 U+E0110 U+E0111 U+E0143 U+E015D |
| `”` | `󠅛󠄒󠄐󠄑󠅄󠅝` | U+E015B U+E0112 U+E0110 U+E0111 U+E0144 U+E015D |
| `«` | `󠅛󠅁󠅂󠅝` | U+E015B U+E0141 U+E0142 U+E015D |
| `»` | `󠅛󠅂󠅂󠅝` | U+E015B U+E0142 U+E0142 U+E015D |
| `'` | `󠄇` | U+E0107 |
| `’` | `󠅛󠄒󠄐󠄑󠄙󠅝` | U+E015B U+E0112 U+E0110 U+E0111 U+E0119 U+E015D |
| `‘` | `󠅛󠄒󠄐󠄑󠄘󠅝` | U+E015B U+E0112 U+E0110 U+E0111 U+E0118 U+E015D |
| `` ` `` | `󠅀` | U+E0140 |
| `-` | ` 󠄍󠇯` | U+0020 U+E010D U+E01EF |
| `‐` | ` 󠅛󠄒󠄐󠄑󠄐󠅝󠇯` | U+0020 U+E015B U+E0112 U+E0110 U+E0111 U+E0110 U+E015D U+E01EF |
| `‑` | ` 󠅛󠄒󠄐󠄑󠄑󠅝󠇯` | U+0020 U+E015B U+E0112 U+E0110 U+E0111 U+E0111 U+E015D U+E01EF |

## Round trip

Every encoding round-trips exactly: decoding the code points that encoding wrote gives back the roman text, and encoding that gives the same code points. The Code points column shows every character a row writes, including any that is invisible.

This page is written from `encodings/aelwythi-semaron.json` by `tools/encoding_docs.py`.
