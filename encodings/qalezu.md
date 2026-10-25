# qalezu encoding

Qalezu Hand is a right-to-left script with one sign for each consonant. This encoding writes a roman spelling in them: a vowel draws nothing except at the start of a word, where it draws the catch sign; elsewhere it is written as an invisible mark, so decoding restores it, and a digraph such as `kh` is a single sign.

## Fonts

- Qalezu Hand (`qalezu-hand`), written right to left.

## Running it

`encode.py` needs only Python 3.9 or later. From a checkout, or from `node_modules/@heroiclands/fonts`:

```sh
python3 encode.py --encoding qalezu "lrtk"
python3 encode.py --encoding qalezu --decode "𞨀𞨁𞨂𞨇"
```

The first command writes `𞨀𞨁𞨂𞨇`, and the second reads it back as `lrtk`. `--codepoints` prints the result as `U+XXXX` values, and the text may come from standard input.

From Python:

```python
import encode

text = encode.encode("qalezu", "lrtk")
roman = encode.decode("qalezu", text)
```

## Vowels and conditions

A row marked _at the start of a word_ applies at the first character of the text or after whitespace, punctuation or a symbol.

A row marked _at the end of a word_ applies at the last character of the text or before whitespace, punctuation or a symbol.

Where several rows begin with the same roman, the longest wins, and among rows of one length a row whose condition holds comes before a row with none. A row whose condition fails is skipped.

## Rows

The rows are in the order the file states them.

| Roman | Character | Code points | When |
| --- | --- | --- | --- |
| `l` | `𞨀` | U+1EA00 | always |
| `L` | `𞨀󠄬󠇯` | U+1EA00 U+E012C U+E01EF | always |
| `r` | `𞨁` | U+1EA01 | always |
| `R` | `𞨁󠄲󠇯` | U+1EA01 U+E0132 U+E01EF | always |
| `t` | `𞨂` | U+1EA02 | always |
| `T` | `𞨂󠄴󠇯` | U+1EA02 U+E0134 U+E01EF | always |
| `d` | `𞨃` | U+1EA03 | always |
| `D` | `𞨃󠄤󠇯` | U+1EA03 U+E0124 U+E01EF | always |
| `z` | `𞨄` | U+1EA04 | always |
| `Z` | `𞨄󠄺󠇯` | U+1EA04 U+E013A U+E01EF | always |
| `s` | `𞨅` | U+1EA05 | always |
| `S` | `𞨅󠄳󠇯` | U+1EA05 U+E0133 U+E01EF | always |
| `g` | `𞨆` | U+1EA06 | always |
| `G` | `𞨆󠄧󠇯` | U+1EA06 U+E0127 U+E01EF | always |
| `k` | `𞨇` | U+1EA07 | always |
| `K` | `𞨇󠄫󠇯` | U+1EA07 U+E012B U+E01EF | always |
| `n` | `𞨈` | U+1EA08 | always |
| `N` | `𞨈󠄮󠇯` | U+1EA08 U+E012E U+E01EF | always |
| `m` | `𞨊` | U+1EA0A | always |
| `M` | `𞨊󠄭󠇯` | U+1EA0A U+E012D U+E01EF | always |
| `q` | `𞨋` | U+1EA0B | always |
| `Q` | `𞨋󠄱󠇯` | U+1EA0B U+E0131 U+E01EF | always |
| `h` | `𞨎` | U+1EA0E | always |
| `H` | `𞨎󠄨󠇯` | U+1EA0E U+E0128 U+E01EF | always |
| `p` | `𞨐` | U+1EA10 | always |
| `P` | `𞨐󠄰󠇯` | U+1EA10 U+E0130 U+E01EF | always |
| `b` | `𞨑` | U+1EA11 | always |
| `B` | `𞨑󠄢󠇯` | U+1EA11 U+E0122 U+E01EF | always |
| `f` | `𞨒` | U+1EA12 | always |
| `v` | `𞨒󠅖󠇯` | U+1EA12 U+E0156 U+E01EF | always |
| `F` | `𞨒󠄦󠇯` | U+1EA12 U+E0126 U+E01EF | always |
| `V` | `𞨒󠄶󠇯` | U+1EA12 U+E0136 U+E01EF | always |
| `w` | `𞨓` | U+1EA13 | always |
| `W` | `𞨓󠄷󠇯` | U+1EA13 U+E0137 U+E01EF | always |
| `y` | `𞨔` | U+1EA14 | always |
| `Y` | `𞨔󠄹󠇯` | U+1EA14 U+E0139 U+E01EF | always |
| `th` | `𞨉` | U+1EA09 | always |
| `tH` | `𞨉󠅔󠄨󠇯` | U+1EA09 U+E0154 U+E0128 U+E01EF | always |
| `Th` | `𞨉󠄴󠅈󠇯` | U+1EA09 U+E0134 U+E0148 U+E01EF | always |
| `TH` | `𞨉󠄴󠄨󠇯` | U+1EA09 U+E0134 U+E0128 U+E01EF | always |
| `sh` | `𞨏` | U+1EA0F | always |
| `sH` | `𞨏󠅓󠄨󠇯` | U+1EA0F U+E0153 U+E0128 U+E01EF | always |
| `Sh` | `𞨏󠄳󠅈󠇯` | U+1EA0F U+E0133 U+E0148 U+E01EF | always |
| `SH` | `𞨏󠄳󠄨󠇯` | U+1EA0F U+E0133 U+E0128 U+E01EF | always |
| `kh` | `𞨌` | U+1EA0C | always |
| `kH` | `𞨌󠅋󠄨󠇯` | U+1EA0C U+E014B U+E0128 U+E01EF | always |
| `Kh` | `𞨌󠄫󠅈󠇯` | U+1EA0C U+E012B U+E0148 U+E01EF | always |
| `KH` | `𞨌󠄫󠄨󠇯` | U+1EA0C U+E012B U+E0128 U+E01EF | always |
| `gh` | `𞨍` | U+1EA0D | always |
| `gH` | `𞨍󠅇󠄨󠇯` | U+1EA0D U+E0147 U+E0128 U+E01EF | always |
| `Gh` | `𞨍󠄧󠅈󠇯` | U+1EA0D U+E0127 U+E0148 U+E01EF | always |
| `GH` | `𞨍󠄧󠄨󠇯` | U+1EA0D U+E0127 U+E0128 U+E01EF | always |
| `ch` | `𞨖` | U+1EA16 | always |
| `J` | `𞨖󠄪󠇯` | U+1EA16 U+E012A U+E01EF | always |
| `j` | `𞨖󠅊󠇯` | U+1EA16 U+E014A U+E01EF | always |
| `cH` | `𞨖󠅃󠄨󠇯` | U+1EA16 U+E0143 U+E0128 U+E01EF | always |
| `Ch` | `𞨖󠄣󠅈󠇯` | U+1EA16 U+E0123 U+E0148 U+E01EF | always |
| `CH` | `𞨖󠄣󠄨󠇯` | U+1EA16 U+E0123 U+E0128 U+E01EF | always |
| `tj` | `𞨖󠅔󠅊󠇯` | U+1EA16 U+E0154 U+E014A U+E01EF | always |
| `tJ` | `𞨖󠅔󠄪󠇯` | U+1EA16 U+E0154 U+E012A U+E01EF | always |
| `Tj` | `𞨖󠄴󠅊󠇯` | U+1EA16 U+E0134 U+E014A U+E01EF | always |
| `TJ` | `𞨖󠄴󠄪󠇯` | U+1EA16 U+E0134 U+E012A U+E01EF | always |
| `ll` | `𞨗` | U+1EA17 | always |
| `lL` | `𞨗󠅌󠄬󠇯` | U+1EA17 U+E014C U+E012C U+E01EF | always |
| `Ll` | `𞨗󠄬󠅌󠇯` | U+1EA17 U+E012C U+E014C U+E01EF | always |
| `LL` | `𞨗󠄬󠄬󠇯` | U+1EA17 U+E012C U+E012C U+E01EF | always |
| `rr` | `𞨘` | U+1EA18 | always |
| `rR` | `𞨘󠅒󠄲󠇯` | U+1EA18 U+E0152 U+E0132 U+E01EF | always |
| `Rr` | `𞨘󠄲󠅒󠇯` | U+1EA18 U+E0132 U+E0152 U+E01EF | always |
| `RR` | `𞨘󠄲󠄲󠇯` | U+1EA18 U+E0132 U+E0132 U+E01EF | always |
| `tt` | `𞨙` | U+1EA19 | always |
| `tT` | `𞨙󠅔󠄴󠇯` | U+1EA19 U+E0154 U+E0134 U+E01EF | always |
| `Tt` | `𞨙󠄴󠅔󠇯` | U+1EA19 U+E0134 U+E0154 U+E01EF | always |
| `TT` | `𞨙󠄴󠄴󠇯` | U+1EA19 U+E0134 U+E0134 U+E01EF | always |
| `dd` | `𞨚` | U+1EA1A | always |
| `dD` | `𞨚󠅄󠄤󠇯` | U+1EA1A U+E0144 U+E0124 U+E01EF | always |
| `Dd` | `𞨚󠄤󠅄󠇯` | U+1EA1A U+E0124 U+E0144 U+E01EF | always |
| `DD` | `𞨚󠄤󠄤󠇯` | U+1EA1A U+E0124 U+E0124 U+E01EF | always |
| `zz` | `𞨛` | U+1EA1B | always |
| `zZ` | `𞨛󠅚󠄺󠇯` | U+1EA1B U+E015A U+E013A U+E01EF | always |
| `Zz` | `𞨛󠄺󠅚󠇯` | U+1EA1B U+E013A U+E015A U+E01EF | always |
| `ZZ` | `𞨛󠄺󠄺󠇯` | U+1EA1B U+E013A U+E013A U+E01EF | always |
| `ss` | `𞨜` | U+1EA1C | always |
| `sS` | `𞨜󠅓󠄳󠇯` | U+1EA1C U+E0153 U+E0133 U+E01EF | always |
| `Ss` | `𞨜󠄳󠅓󠇯` | U+1EA1C U+E0133 U+E0153 U+E01EF | always |
| `SS` | `𞨜󠄳󠄳󠇯` | U+1EA1C U+E0133 U+E0133 U+E01EF | always |
| `gg` | `𞨝` | U+1EA1D | always |
| `gG` | `𞨝󠅇󠄧󠇯` | U+1EA1D U+E0147 U+E0127 U+E01EF | always |
| `Gg` | `𞨝󠄧󠅇󠇯` | U+1EA1D U+E0127 U+E0147 U+E01EF | always |
| `GG` | `𞨝󠄧󠄧󠇯` | U+1EA1D U+E0127 U+E0127 U+E01EF | always |
| `kk` | `𞨞` | U+1EA1E | always |
| `kK` | `𞨞󠅋󠄫󠇯` | U+1EA1E U+E014B U+E012B U+E01EF | always |
| `Kk` | `𞨞󠄫󠅋󠇯` | U+1EA1E U+E012B U+E014B U+E01EF | always |
| `KK` | `𞨞󠄫󠄫󠇯` | U+1EA1E U+E012B U+E012B U+E01EF | always |
| `nn` | `𞨟` | U+1EA1F | always |
| `nN` | `𞨟󠅎󠄮󠇯` | U+1EA1F U+E014E U+E012E U+E01EF | always |
| `Nn` | `𞨟󠄮󠅎󠇯` | U+1EA1F U+E012E U+E014E U+E01EF | always |
| `NN` | `𞨟󠄮󠄮󠇯` | U+1EA1F U+E012E U+E012E U+E01EF | always |
| `mm` | `𞨡` | U+1EA21 | always |
| `mM` | `𞨡󠅍󠄭󠇯` | U+1EA21 U+E014D U+E012D U+E01EF | always |
| `Mm` | `𞨡󠄭󠅍󠇯` | U+1EA21 U+E012D U+E014D U+E01EF | always |
| `MM` | `𞨡󠄭󠄭󠇯` | U+1EA21 U+E012D U+E012D U+E01EF | always |
| `qq` | `𞨢` | U+1EA22 | always |
| `qQ` | `𞨢󠅑󠄱󠇯` | U+1EA22 U+E0151 U+E0131 U+E01EF | always |
| `Qq` | `𞨢󠄱󠅑󠇯` | U+1EA22 U+E0131 U+E0151 U+E01EF | always |
| `QQ` | `𞨢󠄱󠄱󠇯` | U+1EA22 U+E0131 U+E0131 U+E01EF | always |
| `hh` | `𞨥` | U+1EA25 | always |
| `hH` | `𞨥󠅈󠄨󠇯` | U+1EA25 U+E0148 U+E0128 U+E01EF | always |
| `Hh` | `𞨥󠄨󠅈󠇯` | U+1EA25 U+E0128 U+E0148 U+E01EF | always |
| `HH` | `𞨥󠄨󠄨󠇯` | U+1EA25 U+E0128 U+E0128 U+E01EF | always |
| `pp` | `𞨧` | U+1EA27 | always |
| `pP` | `𞨧󠅐󠄰󠇯` | U+1EA27 U+E0150 U+E0130 U+E01EF | always |
| `Pp` | `𞨧󠄰󠅐󠇯` | U+1EA27 U+E0130 U+E0150 U+E01EF | always |
| `PP` | `𞨧󠄰󠄰󠇯` | U+1EA27 U+E0130 U+E0130 U+E01EF | always |
| `bb` | `𞨨` | U+1EA28 | always |
| `bB` | `𞨨󠅂󠄢󠇯` | U+1EA28 U+E0142 U+E0122 U+E01EF | always |
| `Bb` | `𞨨󠄢󠅂󠇯` | U+1EA28 U+E0122 U+E0142 U+E01EF | always |
| `BB` | `𞨨󠄢󠄢󠇯` | U+1EA28 U+E0122 U+E0122 U+E01EF | always |
| `ff` | `𞨩` | U+1EA29 | always |
| `fv` | `𞨩󠅆󠅖󠇯` | U+1EA29 U+E0146 U+E0156 U+E01EF | always |
| `vf` | `𞨩󠅖󠅆󠇯` | U+1EA29 U+E0156 U+E0146 U+E01EF | always |
| `vv` | `𞨩󠅖󠅖󠇯` | U+1EA29 U+E0156 U+E0156 U+E01EF | always |
| `fF` | `𞨩󠅆󠄦󠇯` | U+1EA29 U+E0146 U+E0126 U+E01EF | always |
| `fV` | `𞨩󠅆󠄶󠇯` | U+1EA29 U+E0146 U+E0136 U+E01EF | always |
| `vF` | `𞨩󠅖󠄦󠇯` | U+1EA29 U+E0156 U+E0126 U+E01EF | always |
| `vV` | `𞨩󠅖󠄶󠇯` | U+1EA29 U+E0156 U+E0136 U+E01EF | always |
| `Ff` | `𞨩󠄦󠅆󠇯` | U+1EA29 U+E0126 U+E0146 U+E01EF | always |
| `Fv` | `𞨩󠄦󠅖󠇯` | U+1EA29 U+E0126 U+E0156 U+E01EF | always |
| `Vf` | `𞨩󠄶󠅆󠇯` | U+1EA29 U+E0136 U+E0146 U+E01EF | always |
| `Vv` | `𞨩󠄶󠅖󠇯` | U+1EA29 U+E0136 U+E0156 U+E01EF | always |
| `FF` | `𞨩󠄦󠄦󠇯` | U+1EA29 U+E0126 U+E0126 U+E01EF | always |
| `FV` | `𞨩󠄦󠄶󠇯` | U+1EA29 U+E0126 U+E0136 U+E01EF | always |
| `VF` | `𞨩󠄶󠄦󠇯` | U+1EA29 U+E0136 U+E0126 U+E01EF | always |
| `VV` | `𞨩󠄶󠄶󠇯` | U+1EA29 U+E0136 U+E0136 U+E01EF | always |
| `ww` | `𞨪` | U+1EA2A | always |
| `wW` | `𞨪󠅗󠄷󠇯` | U+1EA2A U+E0157 U+E0137 U+E01EF | always |
| `Ww` | `𞨪󠄷󠅗󠇯` | U+1EA2A U+E0137 U+E0157 U+E01EF | always |
| `WW` | `𞨪󠄷󠄷󠇯` | U+1EA2A U+E0137 U+E0137 U+E01EF | always |
| `yy` | `𞨫` | U+1EA2B | always |
| `yY` | `𞨫󠅙󠄹󠇯` | U+1EA2B U+E0159 U+E0139 U+E01EF | always |
| `Yy` | `𞨫󠄹󠅙󠇯` | U+1EA2B U+E0139 U+E0159 U+E01EF | always |
| `YY` | `𞨫󠄹󠄹󠇯` | U+1EA2B U+E0139 U+E0139 U+E01EF | always |
| `tth` | `𞨠` | U+1EA20 | always |
| `ttH` | `𞨠󠅔󠅔󠄨󠇯` | U+1EA20 U+E0154 U+E0154 U+E0128 U+E01EF | always |
| `tTh` | `𞨠󠅔󠄴󠅈󠇯` | U+1EA20 U+E0154 U+E0134 U+E0148 U+E01EF | always |
| `tTH` | `𞨠󠅔󠄴󠄨󠇯` | U+1EA20 U+E0154 U+E0134 U+E0128 U+E01EF | always |
| `Tth` | `𞨠󠄴󠅔󠅈󠇯` | U+1EA20 U+E0134 U+E0154 U+E0148 U+E01EF | always |
| `TtH` | `𞨠󠄴󠅔󠄨󠇯` | U+1EA20 U+E0134 U+E0154 U+E0128 U+E01EF | always |
| `TTh` | `𞨠󠄴󠄴󠅈󠇯` | U+1EA20 U+E0134 U+E0134 U+E0148 U+E01EF | always |
| `TTH` | `𞨠󠄴󠄴󠄨󠇯` | U+1EA20 U+E0134 U+E0134 U+E0128 U+E01EF | always |
| `ssh` | `𞨦` | U+1EA26 | always |
| `ssH` | `𞨦󠅓󠅓󠄨󠇯` | U+1EA26 U+E0153 U+E0153 U+E0128 U+E01EF | always |
| `sSh` | `𞨦󠅓󠄳󠅈󠇯` | U+1EA26 U+E0153 U+E0133 U+E0148 U+E01EF | always |
| `sSH` | `𞨦󠅓󠄳󠄨󠇯` | U+1EA26 U+E0153 U+E0133 U+E0128 U+E01EF | always |
| `Ssh` | `𞨦󠄳󠅓󠅈󠇯` | U+1EA26 U+E0133 U+E0153 U+E0148 U+E01EF | always |
| `SsH` | `𞨦󠄳󠅓󠄨󠇯` | U+1EA26 U+E0133 U+E0153 U+E0128 U+E01EF | always |
| `SSh` | `𞨦󠄳󠄳󠅈󠇯` | U+1EA26 U+E0133 U+E0133 U+E0148 U+E01EF | always |
| `SSH` | `𞨦󠄳󠄳󠄨󠇯` | U+1EA26 U+E0133 U+E0133 U+E0128 U+E01EF | always |
| `kkh` | `𞨣` | U+1EA23 | always |
| `kkH` | `𞨣󠅋󠅋󠄨󠇯` | U+1EA23 U+E014B U+E014B U+E0128 U+E01EF | always |
| `kKh` | `𞨣󠅋󠄫󠅈󠇯` | U+1EA23 U+E014B U+E012B U+E0148 U+E01EF | always |
| `kKH` | `𞨣󠅋󠄫󠄨󠇯` | U+1EA23 U+E014B U+E012B U+E0128 U+E01EF | always |
| `Kkh` | `𞨣󠄫󠅋󠅈󠇯` | U+1EA23 U+E012B U+E014B U+E0148 U+E01EF | always |
| `KkH` | `𞨣󠄫󠅋󠄨󠇯` | U+1EA23 U+E012B U+E014B U+E0128 U+E01EF | always |
| `KKh` | `𞨣󠄫󠄫󠅈󠇯` | U+1EA23 U+E012B U+E012B U+E0148 U+E01EF | always |
| `KKH` | `𞨣󠄫󠄫󠄨󠇯` | U+1EA23 U+E012B U+E012B U+E0128 U+E01EF | always |
| `ggh` | `𞨤` | U+1EA24 | always |
| `ggH` | `𞨤󠅇󠅇󠄨󠇯` | U+1EA24 U+E0147 U+E0147 U+E0128 U+E01EF | always |
| `gGh` | `𞨤󠅇󠄧󠅈󠇯` | U+1EA24 U+E0147 U+E0127 U+E0148 U+E01EF | always |
| `gGH` | `𞨤󠅇󠄧󠄨󠇯` | U+1EA24 U+E0147 U+E0127 U+E0128 U+E01EF | always |
| `Ggh` | `𞨤󠄧󠅇󠅈󠇯` | U+1EA24 U+E0127 U+E0147 U+E0148 U+E01EF | always |
| `GgH` | `𞨤󠄧󠅇󠄨󠇯` | U+1EA24 U+E0127 U+E0147 U+E0128 U+E01EF | always |
| `GGh` | `𞨤󠄧󠄧󠅈󠇯` | U+1EA24 U+E0127 U+E0127 U+E0148 U+E01EF | always |
| `GGH` | `𞨤󠄧󠄧󠄨󠇯` | U+1EA24 U+E0127 U+E0127 U+E0128 U+E01EF | always |
| `cch` | `𞨬` | U+1EA2C | always |
| `JJ` | `𞨬󠄪󠄪󠇯` | U+1EA2C U+E012A U+E012A U+E01EF | always |
| `Jj` | `𞨬󠄪󠅊󠇯` | U+1EA2C U+E012A U+E014A U+E01EF | always |
| `jJ` | `𞨬󠅊󠄪󠇯` | U+1EA2C U+E014A U+E012A U+E01EF | always |
| `jj` | `𞨬󠅊󠅊󠇯` | U+1EA2C U+E014A U+E014A U+E01EF | always |
| `ccH` | `𞨬󠅃󠅃󠄨󠇯` | U+1EA2C U+E0143 U+E0143 U+E0128 U+E01EF | always |
| `cCh` | `𞨬󠅃󠄣󠅈󠇯` | U+1EA2C U+E0143 U+E0123 U+E0148 U+E01EF | always |
| `cCH` | `𞨬󠅃󠄣󠄨󠇯` | U+1EA2C U+E0143 U+E0123 U+E0128 U+E01EF | always |
| `Cch` | `𞨬󠄣󠅃󠅈󠇯` | U+1EA2C U+E0123 U+E0143 U+E0148 U+E01EF | always |
| `CcH` | `𞨬󠄣󠅃󠄨󠇯` | U+1EA2C U+E0123 U+E0143 U+E0128 U+E01EF | always |
| `CCh` | `𞨬󠄣󠄣󠅈󠇯` | U+1EA2C U+E0123 U+E0123 U+E0148 U+E01EF | always |
| `CCH` | `𞨬󠄣󠄣󠄨󠇯` | U+1EA2C U+E0123 U+E0123 U+E0128 U+E01EF | always |
| `ttj` | `𞨬󠅔󠅔󠅊󠇯` | U+1EA2C U+E0154 U+E0154 U+E014A U+E01EF | always |
| `ttJ` | `𞨬󠅔󠅔󠄪󠇯` | U+1EA2C U+E0154 U+E0154 U+E012A U+E01EF | always |
| `tTj` | `𞨬󠅔󠄴󠅊󠇯` | U+1EA2C U+E0154 U+E0134 U+E014A U+E01EF | always |
| `tTJ` | `𞨬󠅔󠄴󠄪󠇯` | U+1EA2C U+E0154 U+E0134 U+E012A U+E01EF | always |
| `Ttj` | `𞨬󠄴󠅔󠅊󠇯` | U+1EA2C U+E0134 U+E0154 U+E014A U+E01EF | always |
| `TtJ` | `𞨬󠄴󠅔󠄪󠇯` | U+1EA2C U+E0134 U+E0154 U+E012A U+E01EF | always |
| `TTj` | `𞨬󠄴󠄴󠅊󠇯` | U+1EA2C U+E0134 U+E0134 U+E014A U+E01EF | always |
| `TTJ` | `𞨬󠄴󠄴󠄪󠇯` | U+1EA2C U+E0134 U+E0134 U+E012A U+E01EF | always |
| `thth` | `𞨠󠅔󠅈󠅔󠅈󠇯` | U+1EA20 U+E0154 U+E0148 U+E0154 U+E0148 U+E01EF | always |
| `thtH` | `𞨠󠅔󠅈󠅔󠄨󠇯` | U+1EA20 U+E0154 U+E0148 U+E0154 U+E0128 U+E01EF | always |
| `thTh` | `𞨠󠅔󠅈󠄴󠅈󠇯` | U+1EA20 U+E0154 U+E0148 U+E0134 U+E0148 U+E01EF | always |
| `thTH` | `𞨠󠅔󠅈󠄴󠄨󠇯` | U+1EA20 U+E0154 U+E0148 U+E0134 U+E0128 U+E01EF | always |
| `tHth` | `𞨠󠅔󠄨󠅔󠅈󠇯` | U+1EA20 U+E0154 U+E0128 U+E0154 U+E0148 U+E01EF | always |
| `tHtH` | `𞨠󠅔󠄨󠅔󠄨󠇯` | U+1EA20 U+E0154 U+E0128 U+E0154 U+E0128 U+E01EF | always |
| `tHTh` | `𞨠󠅔󠄨󠄴󠅈󠇯` | U+1EA20 U+E0154 U+E0128 U+E0134 U+E0148 U+E01EF | always |
| `tHTH` | `𞨠󠅔󠄨󠄴󠄨󠇯` | U+1EA20 U+E0154 U+E0128 U+E0134 U+E0128 U+E01EF | always |
| `Thth` | `𞨠󠄴󠅈󠅔󠅈󠇯` | U+1EA20 U+E0134 U+E0148 U+E0154 U+E0148 U+E01EF | always |
| `ThtH` | `𞨠󠄴󠅈󠅔󠄨󠇯` | U+1EA20 U+E0134 U+E0148 U+E0154 U+E0128 U+E01EF | always |
| `ThTh` | `𞨠󠄴󠅈󠄴󠅈󠇯` | U+1EA20 U+E0134 U+E0148 U+E0134 U+E0148 U+E01EF | always |
| `ThTH` | `𞨠󠄴󠅈󠄴󠄨󠇯` | U+1EA20 U+E0134 U+E0148 U+E0134 U+E0128 U+E01EF | always |
| `THth` | `𞨠󠄴󠄨󠅔󠅈󠇯` | U+1EA20 U+E0134 U+E0128 U+E0154 U+E0148 U+E01EF | always |
| `THtH` | `𞨠󠄴󠄨󠅔󠄨󠇯` | U+1EA20 U+E0134 U+E0128 U+E0154 U+E0128 U+E01EF | always |
| `THTh` | `𞨠󠄴󠄨󠄴󠅈󠇯` | U+1EA20 U+E0134 U+E0128 U+E0134 U+E0148 U+E01EF | always |
| `THTH` | `𞨠󠄴󠄨󠄴󠄨󠇯` | U+1EA20 U+E0134 U+E0128 U+E0134 U+E0128 U+E01EF | always |
| `shsh` | `𞨦󠅓󠅈󠅓󠅈󠇯` | U+1EA26 U+E0153 U+E0148 U+E0153 U+E0148 U+E01EF | always |
| `shsH` | `𞨦󠅓󠅈󠅓󠄨󠇯` | U+1EA26 U+E0153 U+E0148 U+E0153 U+E0128 U+E01EF | always |
| `shSh` | `𞨦󠅓󠅈󠄳󠅈󠇯` | U+1EA26 U+E0153 U+E0148 U+E0133 U+E0148 U+E01EF | always |
| `shSH` | `𞨦󠅓󠅈󠄳󠄨󠇯` | U+1EA26 U+E0153 U+E0148 U+E0133 U+E0128 U+E01EF | always |
| `sHsh` | `𞨦󠅓󠄨󠅓󠅈󠇯` | U+1EA26 U+E0153 U+E0128 U+E0153 U+E0148 U+E01EF | always |
| `sHsH` | `𞨦󠅓󠄨󠅓󠄨󠇯` | U+1EA26 U+E0153 U+E0128 U+E0153 U+E0128 U+E01EF | always |
| `sHSh` | `𞨦󠅓󠄨󠄳󠅈󠇯` | U+1EA26 U+E0153 U+E0128 U+E0133 U+E0148 U+E01EF | always |
| `sHSH` | `𞨦󠅓󠄨󠄳󠄨󠇯` | U+1EA26 U+E0153 U+E0128 U+E0133 U+E0128 U+E01EF | always |
| `Shsh` | `𞨦󠄳󠅈󠅓󠅈󠇯` | U+1EA26 U+E0133 U+E0148 U+E0153 U+E0148 U+E01EF | always |
| `ShsH` | `𞨦󠄳󠅈󠅓󠄨󠇯` | U+1EA26 U+E0133 U+E0148 U+E0153 U+E0128 U+E01EF | always |
| `ShSh` | `𞨦󠄳󠅈󠄳󠅈󠇯` | U+1EA26 U+E0133 U+E0148 U+E0133 U+E0148 U+E01EF | always |
| `ShSH` | `𞨦󠄳󠅈󠄳󠄨󠇯` | U+1EA26 U+E0133 U+E0148 U+E0133 U+E0128 U+E01EF | always |
| `SHsh` | `𞨦󠄳󠄨󠅓󠅈󠇯` | U+1EA26 U+E0133 U+E0128 U+E0153 U+E0148 U+E01EF | always |
| `SHsH` | `𞨦󠄳󠄨󠅓󠄨󠇯` | U+1EA26 U+E0133 U+E0128 U+E0153 U+E0128 U+E01EF | always |
| `SHSh` | `𞨦󠄳󠄨󠄳󠅈󠇯` | U+1EA26 U+E0133 U+E0128 U+E0133 U+E0148 U+E01EF | always |
| `SHSH` | `𞨦󠄳󠄨󠄳󠄨󠇯` | U+1EA26 U+E0133 U+E0128 U+E0133 U+E0128 U+E01EF | always |
| `khkh` | `𞨣󠅋󠅈󠅋󠅈󠇯` | U+1EA23 U+E014B U+E0148 U+E014B U+E0148 U+E01EF | always |
| `khkH` | `𞨣󠅋󠅈󠅋󠄨󠇯` | U+1EA23 U+E014B U+E0148 U+E014B U+E0128 U+E01EF | always |
| `khKh` | `𞨣󠅋󠅈󠄫󠅈󠇯` | U+1EA23 U+E014B U+E0148 U+E012B U+E0148 U+E01EF | always |
| `khKH` | `𞨣󠅋󠅈󠄫󠄨󠇯` | U+1EA23 U+E014B U+E0148 U+E012B U+E0128 U+E01EF | always |
| `kHkh` | `𞨣󠅋󠄨󠅋󠅈󠇯` | U+1EA23 U+E014B U+E0128 U+E014B U+E0148 U+E01EF | always |
| `kHkH` | `𞨣󠅋󠄨󠅋󠄨󠇯` | U+1EA23 U+E014B U+E0128 U+E014B U+E0128 U+E01EF | always |
| `kHKh` | `𞨣󠅋󠄨󠄫󠅈󠇯` | U+1EA23 U+E014B U+E0128 U+E012B U+E0148 U+E01EF | always |
| `kHKH` | `𞨣󠅋󠄨󠄫󠄨󠇯` | U+1EA23 U+E014B U+E0128 U+E012B U+E0128 U+E01EF | always |
| `Khkh` | `𞨣󠄫󠅈󠅋󠅈󠇯` | U+1EA23 U+E012B U+E0148 U+E014B U+E0148 U+E01EF | always |
| `KhkH` | `𞨣󠄫󠅈󠅋󠄨󠇯` | U+1EA23 U+E012B U+E0148 U+E014B U+E0128 U+E01EF | always |
| `KhKh` | `𞨣󠄫󠅈󠄫󠅈󠇯` | U+1EA23 U+E012B U+E0148 U+E012B U+E0148 U+E01EF | always |
| `KhKH` | `𞨣󠄫󠅈󠄫󠄨󠇯` | U+1EA23 U+E012B U+E0148 U+E012B U+E0128 U+E01EF | always |
| `KHkh` | `𞨣󠄫󠄨󠅋󠅈󠇯` | U+1EA23 U+E012B U+E0128 U+E014B U+E0148 U+E01EF | always |
| `KHkH` | `𞨣󠄫󠄨󠅋󠄨󠇯` | U+1EA23 U+E012B U+E0128 U+E014B U+E0128 U+E01EF | always |
| `KHKh` | `𞨣󠄫󠄨󠄫󠅈󠇯` | U+1EA23 U+E012B U+E0128 U+E012B U+E0148 U+E01EF | always |
| `KHKH` | `𞨣󠄫󠄨󠄫󠄨󠇯` | U+1EA23 U+E012B U+E0128 U+E012B U+E0128 U+E01EF | always |
| `ghgh` | `𞨤󠅇󠅈󠅇󠅈󠇯` | U+1EA24 U+E0147 U+E0148 U+E0147 U+E0148 U+E01EF | always |
| `ghgH` | `𞨤󠅇󠅈󠅇󠄨󠇯` | U+1EA24 U+E0147 U+E0148 U+E0147 U+E0128 U+E01EF | always |
| `ghGh` | `𞨤󠅇󠅈󠄧󠅈󠇯` | U+1EA24 U+E0147 U+E0148 U+E0127 U+E0148 U+E01EF | always |
| `ghGH` | `𞨤󠅇󠅈󠄧󠄨󠇯` | U+1EA24 U+E0147 U+E0148 U+E0127 U+E0128 U+E01EF | always |
| `gHgh` | `𞨤󠅇󠄨󠅇󠅈󠇯` | U+1EA24 U+E0147 U+E0128 U+E0147 U+E0148 U+E01EF | always |
| `gHgH` | `𞨤󠅇󠄨󠅇󠄨󠇯` | U+1EA24 U+E0147 U+E0128 U+E0147 U+E0128 U+E01EF | always |
| `gHGh` | `𞨤󠅇󠄨󠄧󠅈󠇯` | U+1EA24 U+E0147 U+E0128 U+E0127 U+E0148 U+E01EF | always |
| `gHGH` | `𞨤󠅇󠄨󠄧󠄨󠇯` | U+1EA24 U+E0147 U+E0128 U+E0127 U+E0128 U+E01EF | always |
| `Ghgh` | `𞨤󠄧󠅈󠅇󠅈󠇯` | U+1EA24 U+E0127 U+E0148 U+E0147 U+E0148 U+E01EF | always |
| `GhgH` | `𞨤󠄧󠅈󠅇󠄨󠇯` | U+1EA24 U+E0127 U+E0148 U+E0147 U+E0128 U+E01EF | always |
| `GhGh` | `𞨤󠄧󠅈󠄧󠅈󠇯` | U+1EA24 U+E0127 U+E0148 U+E0127 U+E0148 U+E01EF | always |
| `GhGH` | `𞨤󠄧󠅈󠄧󠄨󠇯` | U+1EA24 U+E0127 U+E0148 U+E0127 U+E0128 U+E01EF | always |
| `GHgh` | `𞨤󠄧󠄨󠅇󠅈󠇯` | U+1EA24 U+E0127 U+E0128 U+E0147 U+E0148 U+E01EF | always |
| `GHgH` | `𞨤󠄧󠄨󠅇󠄨󠇯` | U+1EA24 U+E0127 U+E0128 U+E0147 U+E0128 U+E01EF | always |
| `GHGh` | `𞨤󠄧󠄨󠄧󠅈󠇯` | U+1EA24 U+E0127 U+E0128 U+E0127 U+E0148 U+E01EF | always |
| `GHGH` | `𞨤󠄧󠄨󠄧󠄨󠇯` | U+1EA24 U+E0127 U+E0128 U+E0127 U+E0128 U+E01EF | always |
| `chch` | `𞨬󠅃󠅈󠅃󠅈󠇯` | U+1EA2C U+E0143 U+E0148 U+E0143 U+E0148 U+E01EF | always |
| `Jch` | `𞨬󠄪󠅃󠅈󠇯` | U+1EA2C U+E012A U+E0143 U+E0148 U+E01EF | always |
| `chJ` | `𞨬󠅃󠅈󠄪󠇯` | U+1EA2C U+E0143 U+E0148 U+E012A U+E01EF | always |
| `chj` | `𞨬󠅃󠅈󠅊󠇯` | U+1EA2C U+E0143 U+E0148 U+E014A U+E01EF | always |
| `jch` | `𞨬󠅊󠅃󠅈󠇯` | U+1EA2C U+E014A U+E0143 U+E0148 U+E01EF | always |
| `chcH` | `𞨬󠅃󠅈󠅃󠄨󠇯` | U+1EA2C U+E0143 U+E0148 U+E0143 U+E0128 U+E01EF | always |
| `JcH` | `𞨬󠄪󠅃󠄨󠇯` | U+1EA2C U+E012A U+E0143 U+E0128 U+E01EF | always |
| `jcH` | `𞨬󠅊󠅃󠄨󠇯` | U+1EA2C U+E014A U+E0143 U+E0128 U+E01EF | always |
| `chCh` | `𞨬󠅃󠅈󠄣󠅈󠇯` | U+1EA2C U+E0143 U+E0148 U+E0123 U+E0148 U+E01EF | always |
| `JCh` | `𞨬󠄪󠄣󠅈󠇯` | U+1EA2C U+E012A U+E0123 U+E0148 U+E01EF | always |
| `jCh` | `𞨬󠅊󠄣󠅈󠇯` | U+1EA2C U+E014A U+E0123 U+E0148 U+E01EF | always |
| `chCH` | `𞨬󠅃󠅈󠄣󠄨󠇯` | U+1EA2C U+E0143 U+E0148 U+E0123 U+E0128 U+E01EF | always |
| `JCH` | `𞨬󠄪󠄣󠄨󠇯` | U+1EA2C U+E012A U+E0123 U+E0128 U+E01EF | always |
| `jCH` | `𞨬󠅊󠄣󠄨󠇯` | U+1EA2C U+E014A U+E0123 U+E0128 U+E01EF | always |
| `cHch` | `𞨬󠅃󠄨󠅃󠅈󠇯` | U+1EA2C U+E0143 U+E0128 U+E0143 U+E0148 U+E01EF | always |
| `cHJ` | `𞨬󠅃󠄨󠄪󠇯` | U+1EA2C U+E0143 U+E0128 U+E012A U+E01EF | always |
| `cHj` | `𞨬󠅃󠄨󠅊󠇯` | U+1EA2C U+E0143 U+E0128 U+E014A U+E01EF | always |
| `cHcH` | `𞨬󠅃󠄨󠅃󠄨󠇯` | U+1EA2C U+E0143 U+E0128 U+E0143 U+E0128 U+E01EF | always |
| `cHCh` | `𞨬󠅃󠄨󠄣󠅈󠇯` | U+1EA2C U+E0143 U+E0128 U+E0123 U+E0148 U+E01EF | always |
| `cHCH` | `𞨬󠅃󠄨󠄣󠄨󠇯` | U+1EA2C U+E0143 U+E0128 U+E0123 U+E0128 U+E01EF | always |
| `Chch` | `𞨬󠄣󠅈󠅃󠅈󠇯` | U+1EA2C U+E0123 U+E0148 U+E0143 U+E0148 U+E01EF | always |
| `ChJ` | `𞨬󠄣󠅈󠄪󠇯` | U+1EA2C U+E0123 U+E0148 U+E012A U+E01EF | always |
| `Chj` | `𞨬󠄣󠅈󠅊󠇯` | U+1EA2C U+E0123 U+E0148 U+E014A U+E01EF | always |
| `ChcH` | `𞨬󠄣󠅈󠅃󠄨󠇯` | U+1EA2C U+E0123 U+E0148 U+E0143 U+E0128 U+E01EF | always |
| `ChCh` | `𞨬󠄣󠅈󠄣󠅈󠇯` | U+1EA2C U+E0123 U+E0148 U+E0123 U+E0148 U+E01EF | always |
| `ChCH` | `𞨬󠄣󠅈󠄣󠄨󠇯` | U+1EA2C U+E0123 U+E0148 U+E0123 U+E0128 U+E01EF | always |
| `CHch` | `𞨬󠄣󠄨󠅃󠅈󠇯` | U+1EA2C U+E0123 U+E0128 U+E0143 U+E0148 U+E01EF | always |
| `CHJ` | `𞨬󠄣󠄨󠄪󠇯` | U+1EA2C U+E0123 U+E0128 U+E012A U+E01EF | always |
| `CHj` | `𞨬󠄣󠄨󠅊󠇯` | U+1EA2C U+E0123 U+E0128 U+E014A U+E01EF | always |
| `CHcH` | `𞨬󠄣󠄨󠅃󠄨󠇯` | U+1EA2C U+E0123 U+E0128 U+E0143 U+E0128 U+E01EF | always |
| `CHCh` | `𞨬󠄣󠄨󠄣󠅈󠇯` | U+1EA2C U+E0123 U+E0128 U+E0123 U+E0148 U+E01EF | always |
| `CHCH` | `𞨬󠄣󠄨󠄣󠄨󠇯` | U+1EA2C U+E0123 U+E0128 U+E0123 U+E0128 U+E01EF | always |
| `chtj` | `𞨬󠅃󠅈󠅔󠅊󠇯` | U+1EA2C U+E0143 U+E0148 U+E0154 U+E014A U+E01EF | always |
| `Jtj` | `𞨬󠄪󠅔󠅊󠇯` | U+1EA2C U+E012A U+E0154 U+E014A U+E01EF | always |
| `jtj` | `𞨬󠅊󠅔󠅊󠇯` | U+1EA2C U+E014A U+E0154 U+E014A U+E01EF | always |
| `chtJ` | `𞨬󠅃󠅈󠅔󠄪󠇯` | U+1EA2C U+E0143 U+E0148 U+E0154 U+E012A U+E01EF | always |
| `JtJ` | `𞨬󠄪󠅔󠄪󠇯` | U+1EA2C U+E012A U+E0154 U+E012A U+E01EF | always |
| `jtJ` | `𞨬󠅊󠅔󠄪󠇯` | U+1EA2C U+E014A U+E0154 U+E012A U+E01EF | always |
| `chTj` | `𞨬󠅃󠅈󠄴󠅊󠇯` | U+1EA2C U+E0143 U+E0148 U+E0134 U+E014A U+E01EF | always |
| `JTj` | `𞨬󠄪󠄴󠅊󠇯` | U+1EA2C U+E012A U+E0134 U+E014A U+E01EF | always |
| `jTj` | `𞨬󠅊󠄴󠅊󠇯` | U+1EA2C U+E014A U+E0134 U+E014A U+E01EF | always |
| `chTJ` | `𞨬󠅃󠅈󠄴󠄪󠇯` | U+1EA2C U+E0143 U+E0148 U+E0134 U+E012A U+E01EF | always |
| `JTJ` | `𞨬󠄪󠄴󠄪󠇯` | U+1EA2C U+E012A U+E0134 U+E012A U+E01EF | always |
| `jTJ` | `𞨬󠅊󠄴󠄪󠇯` | U+1EA2C U+E014A U+E0134 U+E012A U+E01EF | always |
| `cHtj` | `𞨬󠅃󠄨󠅔󠅊󠇯` | U+1EA2C U+E0143 U+E0128 U+E0154 U+E014A U+E01EF | always |
| `cHtJ` | `𞨬󠅃󠄨󠅔󠄪󠇯` | U+1EA2C U+E0143 U+E0128 U+E0154 U+E012A U+E01EF | always |
| `cHTj` | `𞨬󠅃󠄨󠄴󠅊󠇯` | U+1EA2C U+E0143 U+E0128 U+E0134 U+E014A U+E01EF | always |
| `cHTJ` | `𞨬󠅃󠄨󠄴󠄪󠇯` | U+1EA2C U+E0143 U+E0128 U+E0134 U+E012A U+E01EF | always |
| `Chtj` | `𞨬󠄣󠅈󠅔󠅊󠇯` | U+1EA2C U+E0123 U+E0148 U+E0154 U+E014A U+E01EF | always |
| `ChtJ` | `𞨬󠄣󠅈󠅔󠄪󠇯` | U+1EA2C U+E0123 U+E0148 U+E0154 U+E012A U+E01EF | always |
| `ChTj` | `𞨬󠄣󠅈󠄴󠅊󠇯` | U+1EA2C U+E0123 U+E0148 U+E0134 U+E014A U+E01EF | always |
| `ChTJ` | `𞨬󠄣󠅈󠄴󠄪󠇯` | U+1EA2C U+E0123 U+E0148 U+E0134 U+E012A U+E01EF | always |
| `CHtj` | `𞨬󠄣󠄨󠅔󠅊󠇯` | U+1EA2C U+E0123 U+E0128 U+E0154 U+E014A U+E01EF | always |
| `CHtJ` | `𞨬󠄣󠄨󠅔󠄪󠇯` | U+1EA2C U+E0123 U+E0128 U+E0154 U+E012A U+E01EF | always |
| `CHTj` | `𞨬󠄣󠄨󠄴󠅊󠇯` | U+1EA2C U+E0123 U+E0128 U+E0134 U+E014A U+E01EF | always |
| `CHTJ` | `𞨬󠄣󠄨󠄴󠄪󠇯` | U+1EA2C U+E0123 U+E0128 U+E0134 U+E012A U+E01EF | always |
| `tjch` | `𞨬󠅔󠅊󠅃󠅈󠇯` | U+1EA2C U+E0154 U+E014A U+E0143 U+E0148 U+E01EF | always |
| `tjJ` | `𞨬󠅔󠅊󠄪󠇯` | U+1EA2C U+E0154 U+E014A U+E012A U+E01EF | always |
| `tjj` | `𞨬󠅔󠅊󠅊󠇯` | U+1EA2C U+E0154 U+E014A U+E014A U+E01EF | always |
| `tjcH` | `𞨬󠅔󠅊󠅃󠄨󠇯` | U+1EA2C U+E0154 U+E014A U+E0143 U+E0128 U+E01EF | always |
| `tjCh` | `𞨬󠅔󠅊󠄣󠅈󠇯` | U+1EA2C U+E0154 U+E014A U+E0123 U+E0148 U+E01EF | always |
| `tjCH` | `𞨬󠅔󠅊󠄣󠄨󠇯` | U+1EA2C U+E0154 U+E014A U+E0123 U+E0128 U+E01EF | always |
| `tJch` | `𞨬󠅔󠄪󠅃󠅈󠇯` | U+1EA2C U+E0154 U+E012A U+E0143 U+E0148 U+E01EF | always |
| `tJJ` | `𞨬󠅔󠄪󠄪󠇯` | U+1EA2C U+E0154 U+E012A U+E012A U+E01EF | always |
| `tJj` | `𞨬󠅔󠄪󠅊󠇯` | U+1EA2C U+E0154 U+E012A U+E014A U+E01EF | always |
| `tJcH` | `𞨬󠅔󠄪󠅃󠄨󠇯` | U+1EA2C U+E0154 U+E012A U+E0143 U+E0128 U+E01EF | always |
| `tJCh` | `𞨬󠅔󠄪󠄣󠅈󠇯` | U+1EA2C U+E0154 U+E012A U+E0123 U+E0148 U+E01EF | always |
| `tJCH` | `𞨬󠅔󠄪󠄣󠄨󠇯` | U+1EA2C U+E0154 U+E012A U+E0123 U+E0128 U+E01EF | always |
| `Tjch` | `𞨬󠄴󠅊󠅃󠅈󠇯` | U+1EA2C U+E0134 U+E014A U+E0143 U+E0148 U+E01EF | always |
| `TjJ` | `𞨬󠄴󠅊󠄪󠇯` | U+1EA2C U+E0134 U+E014A U+E012A U+E01EF | always |
| `Tjj` | `𞨬󠄴󠅊󠅊󠇯` | U+1EA2C U+E0134 U+E014A U+E014A U+E01EF | always |
| `TjcH` | `𞨬󠄴󠅊󠅃󠄨󠇯` | U+1EA2C U+E0134 U+E014A U+E0143 U+E0128 U+E01EF | always |
| `TjCh` | `𞨬󠄴󠅊󠄣󠅈󠇯` | U+1EA2C U+E0134 U+E014A U+E0123 U+E0148 U+E01EF | always |
| `TjCH` | `𞨬󠄴󠅊󠄣󠄨󠇯` | U+1EA2C U+E0134 U+E014A U+E0123 U+E0128 U+E01EF | always |
| `TJch` | `𞨬󠄴󠄪󠅃󠅈󠇯` | U+1EA2C U+E0134 U+E012A U+E0143 U+E0148 U+E01EF | always |
| `TJJ` | `𞨬󠄴󠄪󠄪󠇯` | U+1EA2C U+E0134 U+E012A U+E012A U+E01EF | always |
| `TJj` | `𞨬󠄴󠄪󠅊󠇯` | U+1EA2C U+E0134 U+E012A U+E014A U+E01EF | always |
| `TJcH` | `𞨬󠄴󠄪󠅃󠄨󠇯` | U+1EA2C U+E0134 U+E012A U+E0143 U+E0128 U+E01EF | always |
| `TJCh` | `𞨬󠄴󠄪󠄣󠅈󠇯` | U+1EA2C U+E0134 U+E012A U+E0123 U+E0148 U+E01EF | always |
| `TJCH` | `𞨬󠄴󠄪󠄣󠄨󠇯` | U+1EA2C U+E0134 U+E012A U+E0123 U+E0128 U+E01EF | always |
| `tjtj` | `𞨬󠅔󠅊󠅔󠅊󠇯` | U+1EA2C U+E0154 U+E014A U+E0154 U+E014A U+E01EF | always |
| `tjtJ` | `𞨬󠅔󠅊󠅔󠄪󠇯` | U+1EA2C U+E0154 U+E014A U+E0154 U+E012A U+E01EF | always |
| `tjTj` | `𞨬󠅔󠅊󠄴󠅊󠇯` | U+1EA2C U+E0154 U+E014A U+E0134 U+E014A U+E01EF | always |
| `tjTJ` | `𞨬󠅔󠅊󠄴󠄪󠇯` | U+1EA2C U+E0154 U+E014A U+E0134 U+E012A U+E01EF | always |
| `tJtj` | `𞨬󠅔󠄪󠅔󠅊󠇯` | U+1EA2C U+E0154 U+E012A U+E0154 U+E014A U+E01EF | always |
| `tJtJ` | `𞨬󠅔󠄪󠅔󠄪󠇯` | U+1EA2C U+E0154 U+E012A U+E0154 U+E012A U+E01EF | always |
| `tJTj` | `𞨬󠅔󠄪󠄴󠅊󠇯` | U+1EA2C U+E0154 U+E012A U+E0134 U+E014A U+E01EF | always |
| `tJTJ` | `𞨬󠅔󠄪󠄴󠄪󠇯` | U+1EA2C U+E0154 U+E012A U+E0134 U+E012A U+E01EF | always |
| `Tjtj` | `𞨬󠄴󠅊󠅔󠅊󠇯` | U+1EA2C U+E0134 U+E014A U+E0154 U+E014A U+E01EF | always |
| `TjtJ` | `𞨬󠄴󠅊󠅔󠄪󠇯` | U+1EA2C U+E0134 U+E014A U+E0154 U+E012A U+E01EF | always |
| `TjTj` | `𞨬󠄴󠅊󠄴󠅊󠇯` | U+1EA2C U+E0134 U+E014A U+E0134 U+E014A U+E01EF | always |
| `TjTJ` | `𞨬󠄴󠅊󠄴󠄪󠇯` | U+1EA2C U+E0134 U+E014A U+E0134 U+E012A U+E01EF | always |
| `TJtj` | `𞨬󠄴󠄪󠅔󠅊󠇯` | U+1EA2C U+E0134 U+E012A U+E0154 U+E014A U+E01EF | always |
| `TJtJ` | `𞨬󠄴󠄪󠅔󠄪󠇯` | U+1EA2C U+E0134 U+E012A U+E0154 U+E012A U+E01EF | always |
| `TJTj` | `𞨬󠄴󠄪󠄴󠅊󠇯` | U+1EA2C U+E0134 U+E012A U+E0134 U+E014A U+E01EF | always |
| `TJTJ` | `𞨬󠄴󠄪󠄴󠄪󠇯` | U+1EA2C U+E0134 U+E012A U+E0134 U+E012A U+E01EF | always |
| `ttth` | `𞨂𞨠󠅔󠅔󠅔󠅈󠇯` | U+1EA02 U+1EA20 U+E0154 U+E0154 U+E0154 U+E0148 U+E01EF | always |
| `tttH` | `𞨂𞨠󠅔󠅔󠅔󠄨󠇯` | U+1EA02 U+1EA20 U+E0154 U+E0154 U+E0154 U+E0128 U+E01EF | always |
| `ttTh` | `𞨂𞨠󠅔󠅔󠄴󠅈󠇯` | U+1EA02 U+1EA20 U+E0154 U+E0154 U+E0134 U+E0148 U+E01EF | always |
| `ttTH` | `𞨂𞨠󠅔󠅔󠄴󠄨󠇯` | U+1EA02 U+1EA20 U+E0154 U+E0154 U+E0134 U+E0128 U+E01EF | always |
| `tTth` | `𞨂𞨠󠅔󠄴󠅔󠅈󠇯` | U+1EA02 U+1EA20 U+E0154 U+E0134 U+E0154 U+E0148 U+E01EF | always |
| `tTtH` | `𞨂𞨠󠅔󠄴󠅔󠄨󠇯` | U+1EA02 U+1EA20 U+E0154 U+E0134 U+E0154 U+E0128 U+E01EF | always |
| `tTTh` | `𞨂𞨠󠅔󠄴󠄴󠅈󠇯` | U+1EA02 U+1EA20 U+E0154 U+E0134 U+E0134 U+E0148 U+E01EF | always |
| `tTTH` | `𞨂𞨠󠅔󠄴󠄴󠄨󠇯` | U+1EA02 U+1EA20 U+E0154 U+E0134 U+E0134 U+E0128 U+E01EF | always |
| `Ttth` | `𞨂𞨠󠄴󠅔󠅔󠅈󠇯` | U+1EA02 U+1EA20 U+E0134 U+E0154 U+E0154 U+E0148 U+E01EF | always |
| `TttH` | `𞨂𞨠󠄴󠅔󠅔󠄨󠇯` | U+1EA02 U+1EA20 U+E0134 U+E0154 U+E0154 U+E0128 U+E01EF | always |
| `TtTh` | `𞨂𞨠󠄴󠅔󠄴󠅈󠇯` | U+1EA02 U+1EA20 U+E0134 U+E0154 U+E0134 U+E0148 U+E01EF | always |
| `TtTH` | `𞨂𞨠󠄴󠅔󠄴󠄨󠇯` | U+1EA02 U+1EA20 U+E0134 U+E0154 U+E0134 U+E0128 U+E01EF | always |
| `TTth` | `𞨂𞨠󠄴󠄴󠅔󠅈󠇯` | U+1EA02 U+1EA20 U+E0134 U+E0134 U+E0154 U+E0148 U+E01EF | always |
| `TTtH` | `𞨂𞨠󠄴󠄴󠅔󠄨󠇯` | U+1EA02 U+1EA20 U+E0134 U+E0134 U+E0154 U+E0128 U+E01EF | always |
| `TTTh` | `𞨂𞨠󠄴󠄴󠄴󠅈󠇯` | U+1EA02 U+1EA20 U+E0134 U+E0134 U+E0134 U+E0148 U+E01EF | always |
| `TTTH` | `𞨂𞨠󠄴󠄴󠄴󠄨󠇯` | U+1EA02 U+1EA20 U+E0134 U+E0134 U+E0134 U+E0128 U+E01EF | always |
| `sssh` | `𞨅𞨦󠅓󠅓󠅓󠅈󠇯` | U+1EA05 U+1EA26 U+E0153 U+E0153 U+E0153 U+E0148 U+E01EF | always |
| `sssH` | `𞨅𞨦󠅓󠅓󠅓󠄨󠇯` | U+1EA05 U+1EA26 U+E0153 U+E0153 U+E0153 U+E0128 U+E01EF | always |
| `ssSh` | `𞨅𞨦󠅓󠅓󠄳󠅈󠇯` | U+1EA05 U+1EA26 U+E0153 U+E0153 U+E0133 U+E0148 U+E01EF | always |
| `ssSH` | `𞨅𞨦󠅓󠅓󠄳󠄨󠇯` | U+1EA05 U+1EA26 U+E0153 U+E0153 U+E0133 U+E0128 U+E01EF | always |
| `sSsh` | `𞨅𞨦󠅓󠄳󠅓󠅈󠇯` | U+1EA05 U+1EA26 U+E0153 U+E0133 U+E0153 U+E0148 U+E01EF | always |
| `sSsH` | `𞨅𞨦󠅓󠄳󠅓󠄨󠇯` | U+1EA05 U+1EA26 U+E0153 U+E0133 U+E0153 U+E0128 U+E01EF | always |
| `sSSh` | `𞨅𞨦󠅓󠄳󠄳󠅈󠇯` | U+1EA05 U+1EA26 U+E0153 U+E0133 U+E0133 U+E0148 U+E01EF | always |
| `sSSH` | `𞨅𞨦󠅓󠄳󠄳󠄨󠇯` | U+1EA05 U+1EA26 U+E0153 U+E0133 U+E0133 U+E0128 U+E01EF | always |
| `Sssh` | `𞨅𞨦󠄳󠅓󠅓󠅈󠇯` | U+1EA05 U+1EA26 U+E0133 U+E0153 U+E0153 U+E0148 U+E01EF | always |
| `SssH` | `𞨅𞨦󠄳󠅓󠅓󠄨󠇯` | U+1EA05 U+1EA26 U+E0133 U+E0153 U+E0153 U+E0128 U+E01EF | always |
| `SsSh` | `𞨅𞨦󠄳󠅓󠄳󠅈󠇯` | U+1EA05 U+1EA26 U+E0133 U+E0153 U+E0133 U+E0148 U+E01EF | always |
| `SsSH` | `𞨅𞨦󠄳󠅓󠄳󠄨󠇯` | U+1EA05 U+1EA26 U+E0133 U+E0153 U+E0133 U+E0128 U+E01EF | always |
| `SSsh` | `𞨅𞨦󠄳󠄳󠅓󠅈󠇯` | U+1EA05 U+1EA26 U+E0133 U+E0133 U+E0153 U+E0148 U+E01EF | always |
| `SSsH` | `𞨅𞨦󠄳󠄳󠅓󠄨󠇯` | U+1EA05 U+1EA26 U+E0133 U+E0133 U+E0153 U+E0128 U+E01EF | always |
| `SSSh` | `𞨅𞨦󠄳󠄳󠄳󠅈󠇯` | U+1EA05 U+1EA26 U+E0133 U+E0133 U+E0133 U+E0148 U+E01EF | always |
| `SSSH` | `𞨅𞨦󠄳󠄳󠄳󠄨󠇯` | U+1EA05 U+1EA26 U+E0133 U+E0133 U+E0133 U+E0128 U+E01EF | always |
| `kkkh` | `𞨇𞨣󠅋󠅋󠅋󠅈󠇯` | U+1EA07 U+1EA23 U+E014B U+E014B U+E014B U+E0148 U+E01EF | always |
| `kkkH` | `𞨇𞨣󠅋󠅋󠅋󠄨󠇯` | U+1EA07 U+1EA23 U+E014B U+E014B U+E014B U+E0128 U+E01EF | always |
| `kkKh` | `𞨇𞨣󠅋󠅋󠄫󠅈󠇯` | U+1EA07 U+1EA23 U+E014B U+E014B U+E012B U+E0148 U+E01EF | always |
| `kkKH` | `𞨇𞨣󠅋󠅋󠄫󠄨󠇯` | U+1EA07 U+1EA23 U+E014B U+E014B U+E012B U+E0128 U+E01EF | always |
| `kKkh` | `𞨇𞨣󠅋󠄫󠅋󠅈󠇯` | U+1EA07 U+1EA23 U+E014B U+E012B U+E014B U+E0148 U+E01EF | always |
| `kKkH` | `𞨇𞨣󠅋󠄫󠅋󠄨󠇯` | U+1EA07 U+1EA23 U+E014B U+E012B U+E014B U+E0128 U+E01EF | always |
| `kKKh` | `𞨇𞨣󠅋󠄫󠄫󠅈󠇯` | U+1EA07 U+1EA23 U+E014B U+E012B U+E012B U+E0148 U+E01EF | always |
| `kKKH` | `𞨇𞨣󠅋󠄫󠄫󠄨󠇯` | U+1EA07 U+1EA23 U+E014B U+E012B U+E012B U+E0128 U+E01EF | always |
| `Kkkh` | `𞨇𞨣󠄫󠅋󠅋󠅈󠇯` | U+1EA07 U+1EA23 U+E012B U+E014B U+E014B U+E0148 U+E01EF | always |
| `KkkH` | `𞨇𞨣󠄫󠅋󠅋󠄨󠇯` | U+1EA07 U+1EA23 U+E012B U+E014B U+E014B U+E0128 U+E01EF | always |
| `KkKh` | `𞨇𞨣󠄫󠅋󠄫󠅈󠇯` | U+1EA07 U+1EA23 U+E012B U+E014B U+E012B U+E0148 U+E01EF | always |
| `KkKH` | `𞨇𞨣󠄫󠅋󠄫󠄨󠇯` | U+1EA07 U+1EA23 U+E012B U+E014B U+E012B U+E0128 U+E01EF | always |
| `KKkh` | `𞨇𞨣󠄫󠄫󠅋󠅈󠇯` | U+1EA07 U+1EA23 U+E012B U+E012B U+E014B U+E0148 U+E01EF | always |
| `KKkH` | `𞨇𞨣󠄫󠄫󠅋󠄨󠇯` | U+1EA07 U+1EA23 U+E012B U+E012B U+E014B U+E0128 U+E01EF | always |
| `KKKh` | `𞨇𞨣󠄫󠄫󠄫󠅈󠇯` | U+1EA07 U+1EA23 U+E012B U+E012B U+E012B U+E0148 U+E01EF | always |
| `KKKH` | `𞨇𞨣󠄫󠄫󠄫󠄨󠇯` | U+1EA07 U+1EA23 U+E012B U+E012B U+E012B U+E0128 U+E01EF | always |
| `gggh` | `𞨆𞨤󠅇󠅇󠅇󠅈󠇯` | U+1EA06 U+1EA24 U+E0147 U+E0147 U+E0147 U+E0148 U+E01EF | always |
| `gggH` | `𞨆𞨤󠅇󠅇󠅇󠄨󠇯` | U+1EA06 U+1EA24 U+E0147 U+E0147 U+E0147 U+E0128 U+E01EF | always |
| `ggGh` | `𞨆𞨤󠅇󠅇󠄧󠅈󠇯` | U+1EA06 U+1EA24 U+E0147 U+E0147 U+E0127 U+E0148 U+E01EF | always |
| `ggGH` | `𞨆𞨤󠅇󠅇󠄧󠄨󠇯` | U+1EA06 U+1EA24 U+E0147 U+E0147 U+E0127 U+E0128 U+E01EF | always |
| `gGgh` | `𞨆𞨤󠅇󠄧󠅇󠅈󠇯` | U+1EA06 U+1EA24 U+E0147 U+E0127 U+E0147 U+E0148 U+E01EF | always |
| `gGgH` | `𞨆𞨤󠅇󠄧󠅇󠄨󠇯` | U+1EA06 U+1EA24 U+E0147 U+E0127 U+E0147 U+E0128 U+E01EF | always |
| `gGGh` | `𞨆𞨤󠅇󠄧󠄧󠅈󠇯` | U+1EA06 U+1EA24 U+E0147 U+E0127 U+E0127 U+E0148 U+E01EF | always |
| `gGGH` | `𞨆𞨤󠅇󠄧󠄧󠄨󠇯` | U+1EA06 U+1EA24 U+E0147 U+E0127 U+E0127 U+E0128 U+E01EF | always |
| `Gggh` | `𞨆𞨤󠄧󠅇󠅇󠅈󠇯` | U+1EA06 U+1EA24 U+E0127 U+E0147 U+E0147 U+E0148 U+E01EF | always |
| `GggH` | `𞨆𞨤󠄧󠅇󠅇󠄨󠇯` | U+1EA06 U+1EA24 U+E0127 U+E0147 U+E0147 U+E0128 U+E01EF | always |
| `GgGh` | `𞨆𞨤󠄧󠅇󠄧󠅈󠇯` | U+1EA06 U+1EA24 U+E0127 U+E0147 U+E0127 U+E0148 U+E01EF | always |
| `GgGH` | `𞨆𞨤󠄧󠅇󠄧󠄨󠇯` | U+1EA06 U+1EA24 U+E0127 U+E0147 U+E0127 U+E0128 U+E01EF | always |
| `GGgh` | `𞨆𞨤󠄧󠄧󠅇󠅈󠇯` | U+1EA06 U+1EA24 U+E0127 U+E0127 U+E0147 U+E0148 U+E01EF | always |
| `GGgH` | `𞨆𞨤󠄧󠄧󠅇󠄨󠇯` | U+1EA06 U+1EA24 U+E0127 U+E0127 U+E0147 U+E0128 U+E01EF | always |
| `GGGh` | `𞨆𞨤󠄧󠄧󠄧󠅈󠇯` | U+1EA06 U+1EA24 U+E0127 U+E0127 U+E0127 U+E0148 U+E01EF | always |
| `GGGH` | `𞨆𞨤󠄧󠄧󠄧󠄨󠇯` | U+1EA06 U+1EA24 U+E0127 U+E0127 U+E0127 U+E0128 U+E01EF | always |
| `tttj` | `𞨂𞨬󠅔󠅔󠅔󠅊󠇯` | U+1EA02 U+1EA2C U+E0154 U+E0154 U+E0154 U+E014A U+E01EF | always |
| `tttJ` | `𞨂𞨬󠅔󠅔󠅔󠄪󠇯` | U+1EA02 U+1EA2C U+E0154 U+E0154 U+E0154 U+E012A U+E01EF | always |
| `ttTj` | `𞨂𞨬󠅔󠅔󠄴󠅊󠇯` | U+1EA02 U+1EA2C U+E0154 U+E0154 U+E0134 U+E014A U+E01EF | always |
| `ttTJ` | `𞨂𞨬󠅔󠅔󠄴󠄪󠇯` | U+1EA02 U+1EA2C U+E0154 U+E0154 U+E0134 U+E012A U+E01EF | always |
| `tTtj` | `𞨂𞨬󠅔󠄴󠅔󠅊󠇯` | U+1EA02 U+1EA2C U+E0154 U+E0134 U+E0154 U+E014A U+E01EF | always |
| `tTtJ` | `𞨂𞨬󠅔󠄴󠅔󠄪󠇯` | U+1EA02 U+1EA2C U+E0154 U+E0134 U+E0154 U+E012A U+E01EF | always |
| `tTTj` | `𞨂𞨬󠅔󠄴󠄴󠅊󠇯` | U+1EA02 U+1EA2C U+E0154 U+E0134 U+E0134 U+E014A U+E01EF | always |
| `tTTJ` | `𞨂𞨬󠅔󠄴󠄴󠄪󠇯` | U+1EA02 U+1EA2C U+E0154 U+E0134 U+E0134 U+E012A U+E01EF | always |
| `Tttj` | `𞨂𞨬󠄴󠅔󠅔󠅊󠇯` | U+1EA02 U+1EA2C U+E0134 U+E0154 U+E0154 U+E014A U+E01EF | always |
| `TttJ` | `𞨂𞨬󠄴󠅔󠅔󠄪󠇯` | U+1EA02 U+1EA2C U+E0134 U+E0154 U+E0154 U+E012A U+E01EF | always |
| `TtTj` | `𞨂𞨬󠄴󠅔󠄴󠅊󠇯` | U+1EA02 U+1EA2C U+E0134 U+E0154 U+E0134 U+E014A U+E01EF | always |
| `TtTJ` | `𞨂𞨬󠄴󠅔󠄴󠄪󠇯` | U+1EA02 U+1EA2C U+E0134 U+E0154 U+E0134 U+E012A U+E01EF | always |
| `TTtj` | `𞨂𞨬󠄴󠄴󠅔󠅊󠇯` | U+1EA02 U+1EA2C U+E0134 U+E0134 U+E0154 U+E014A U+E01EF | always |
| `TTtJ` | `𞨂𞨬󠄴󠄴󠅔󠄪󠇯` | U+1EA02 U+1EA2C U+E0134 U+E0134 U+E0154 U+E012A U+E01EF | always |
| `TTTj` | `𞨂𞨬󠄴󠄴󠄴󠅊󠇯` | U+1EA02 U+1EA2C U+E0134 U+E0134 U+E0134 U+E014A U+E01EF | always |
| `TTTJ` | `𞨂𞨬󠄴󠄴󠄴󠄪󠇯` | U+1EA02 U+1EA2C U+E0134 U+E0134 U+E0134 U+E012A U+E01EF | always |
| `a` | `𞨕` | U+1EA15 | at the start of a word |
| `a` | `󠅁` | U+E0141 | always |
| `A` | `𞨕󠄡󠇯` | U+1EA15 U+E0121 U+E01EF | at the start of a word |
| `A` | `󠄡` | U+E0121 | always |
| `e` | `𞨕󠅅󠇯` | U+1EA15 U+E0145 U+E01EF | at the start of a word |
| `ë` | `𞨕󠅛󠅅󠅂󠅝󠇯` | U+1EA15 U+E015B U+E0145 U+E0142 U+E015D U+E01EF | at the start of a word |
| `e` | `󠅅` | U+E0145 | always |
| `ë` | `󠅛󠅅󠅂󠅝` | U+E015B U+E0145 U+E0142 U+E015D | always |
| `E` | `𞨕󠄥󠇯` | U+1EA15 U+E0125 U+E01EF | at the start of a word |
| `Ë` | `𞨕󠅛󠅃󠅂󠅝󠇯` | U+1EA15 U+E015B U+E0143 U+E0142 U+E015D U+E01EF | at the start of a word |
| `E` | `󠄥` | U+E0125 | always |
| `Ë` | `󠅛󠅃󠅂󠅝` | U+E015B U+E0143 U+E0142 U+E015D | always |
| `i` | `𞨕󠅉󠇯` | U+1EA15 U+E0149 U+E01EF | at the start of a word |
| `i` | `󠅉` | U+E0149 | always |
| `I` | `𞨕󠄩󠇯` | U+1EA15 U+E0129 U+E01EF | at the start of a word |
| `I` | `󠄩` | U+E0129 | always |
| `o` | `𞨕󠅏󠇯` | U+1EA15 U+E014F U+E01EF | at the start of a word |
| `o` | `󠅏` | U+E014F | always |
| `O` | `𞨕󠄯󠇯` | U+1EA15 U+E012F U+E01EF | at the start of a word |
| `O` | `󠄯` | U+E012F | always |
| `u` | `𞨕󠅕󠇯` | U+1EA15 U+E0155 U+E01EF | at the start of a word |
| `u` | `󠅕` | U+E0155 | always |
| `U` | `𞨕󠄵󠇯` | U+1EA15 U+E0135 U+E01EF | at the start of a word |
| `U` | `󠄵` | U+E0135 | always |
| `'` | `𞨕󠄇󠇯` | U+1EA15 U+E0107 U+E01EF | always |
| `'a` | `𞨕󠄇󠅁󠇯` | U+1EA15 U+E0107 U+E0141 U+E01EF | always |
| `'A` | `𞨕󠄇󠄡󠇯` | U+1EA15 U+E0107 U+E0121 U+E01EF | always |
| `'e` | `𞨕󠄇󠅅󠇯` | U+1EA15 U+E0107 U+E0145 U+E01EF | always |
| `'ë` | `𞨕󠄇󠅛󠅅󠅂󠅝󠇯` | U+1EA15 U+E0107 U+E015B U+E0145 U+E0142 U+E015D U+E01EF | always |
| `'E` | `𞨕󠄇󠄥󠇯` | U+1EA15 U+E0107 U+E0125 U+E01EF | always |
| `'Ë` | `𞨕󠄇󠅛󠅃󠅂󠅝󠇯` | U+1EA15 U+E0107 U+E015B U+E0143 U+E0142 U+E015D U+E01EF | always |
| `'i` | `𞨕󠄇󠅉󠇯` | U+1EA15 U+E0107 U+E0149 U+E01EF | always |
| `'I` | `𞨕󠄇󠄩󠇯` | U+1EA15 U+E0107 U+E0129 U+E01EF | always |
| `'o` | `𞨕󠄇󠅏󠇯` | U+1EA15 U+E0107 U+E014F U+E01EF | always |
| `'O` | `𞨕󠄇󠄯󠇯` | U+1EA15 U+E0107 U+E012F U+E01EF | always |
| `'u` | `𞨕󠄇󠅕󠇯` | U+1EA15 U+E0107 U+E0155 U+E01EF | always |
| `'U` | `𞨕󠄇󠄵󠇯` | U+1EA15 U+E0107 U+E0135 U+E01EF | always |
| `’` | `𞨕󠅛󠄒󠄐󠄑󠄙󠅝󠇯` | U+1EA15 U+E015B U+E0112 U+E0110 U+E0111 U+E0119 U+E015D U+E01EF | always |
| `’a` | `𞨕󠅛󠄒󠄐󠄑󠄙󠅝󠅁󠇯` | U+1EA15 U+E015B U+E0112 U+E0110 U+E0111 U+E0119 U+E015D U+E0141 U+E01EF | always |
| `’A` | `𞨕󠅛󠄒󠄐󠄑󠄙󠅝󠄡󠇯` | U+1EA15 U+E015B U+E0112 U+E0110 U+E0111 U+E0119 U+E015D U+E0121 U+E01EF | always |
| `’e` | `𞨕󠅛󠄒󠄐󠄑󠄙󠅝󠅅󠇯` | U+1EA15 U+E015B U+E0112 U+E0110 U+E0111 U+E0119 U+E015D U+E0145 U+E01EF | always |
| `’ë` | `𞨕󠅛󠄒󠄐󠄑󠄙󠅝󠅛󠅅󠅂󠅝󠇯` | U+1EA15 U+E015B U+E0112 U+E0110 U+E0111 U+E0119 U+E015D U+E015B U+E0145 U+E0142 U+E015D U+E01EF | always |
| `’E` | `𞨕󠅛󠄒󠄐󠄑󠄙󠅝󠄥󠇯` | U+1EA15 U+E015B U+E0112 U+E0110 U+E0111 U+E0119 U+E015D U+E0125 U+E01EF | always |
| `’Ë` | `𞨕󠅛󠄒󠄐󠄑󠄙󠅝󠅛󠅃󠅂󠅝󠇯` | U+1EA15 U+E015B U+E0112 U+E0110 U+E0111 U+E0119 U+E015D U+E015B U+E0143 U+E0142 U+E015D U+E01EF | always |
| `’i` | `𞨕󠅛󠄒󠄐󠄑󠄙󠅝󠅉󠇯` | U+1EA15 U+E015B U+E0112 U+E0110 U+E0111 U+E0119 U+E015D U+E0149 U+E01EF | always |
| `’I` | `𞨕󠅛󠄒󠄐󠄑󠄙󠅝󠄩󠇯` | U+1EA15 U+E015B U+E0112 U+E0110 U+E0111 U+E0119 U+E015D U+E0129 U+E01EF | always |
| `’o` | `𞨕󠅛󠄒󠄐󠄑󠄙󠅝󠅏󠇯` | U+1EA15 U+E015B U+E0112 U+E0110 U+E0111 U+E0119 U+E015D U+E014F U+E01EF | always |
| `’O` | `𞨕󠅛󠄒󠄐󠄑󠄙󠅝󠄯󠇯` | U+1EA15 U+E015B U+E0112 U+E0110 U+E0111 U+E0119 U+E015D U+E012F U+E01EF | always |
| `’u` | `𞨕󠅛󠄒󠄐󠄑󠄙󠅝󠅕󠇯` | U+1EA15 U+E015B U+E0112 U+E0110 U+E0111 U+E0119 U+E015D U+E0155 U+E01EF | always |
| `’U` | `𞨕󠅛󠄒󠄐󠄑󠄙󠅝󠄵󠇯` | U+1EA15 U+E015B U+E0112 U+E0110 U+E0111 U+E0119 U+E015D U+E0135 U+E01EF | always |
| `-` | `󠄍` | U+E010D | at the end of a word |
| `-` | ` 󠄍󠇯` | U+0020 U+E010D U+E01EF | always |
| `0` | `𞨭` | U+1EA2D | always |
| `1` | `𞨮` | U+1EA2E | always |
| `2` | `𞨯` | U+1EA2F | always |
| `3` | `𞨰` | U+1EA30 | always |
| `4` | `𞨱` | U+1EA31 | always |
| `5` | `𞨲` | U+1EA32 | always |
| `6` | `𞨳` | U+1EA33 | always |
| `7` | `𞨴` | U+1EA34 | always |
| `8` | `𞨵` | U+1EA35 | always |
| `9` | `𞨶` | U+1EA36 | always |
| `.` | `𞨷` | U+1EA37 | always |
| `,` | `𞨸` | U+1EA38 | always |
| `·` | `𞨹` | U+1EA39 | always |

## Round trip

Every encoding round-trips exactly: decoding the code points that encoding wrote gives back the roman text, and encoding that gives the same code points. The Code points column shows every character a row writes, including any that is invisible.

This page is written from `encodings/qalezu.json` by `tools/encoding_docs.py`.
