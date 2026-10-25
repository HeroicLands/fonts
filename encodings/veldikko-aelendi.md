# veldikko-aelendi encoding

A second roman spelling for Veldikko, with the same letters and marks. It writes the consonant digraphs such as `th`, `dh`, `kh` and `ng` as single letters.

## Fonts

- Veldikko (`veldikko`), written right to left.

## Running it

`encode.py` needs only Python 3.9 or later. From a checkout, or from `node_modules/@heroiclands/fonts`:

```sh
python3 encode.py --encoding veldikko-aelendi "tanu"
python3 encode.py --encoding veldikko-aelendi --decode "𞵓𞵰𞵕𞵲"
```

The first command writes `𞵓𞵰𞵕𞵲`, and the second reads it back as `tanu`. `--codepoints` prints the result as `U+XXXX` values, and the text may come from standard input.

From Python:

```python
import encode

text = encode.encode("veldikko-aelendi", "tanu")
roman = encode.decode("veldikko-aelendi", text)
```

## Vowels and conditions

A row marked _at the start of a word_ applies at the first character of the text or after whitespace, punctuation or a symbol.

A row marked _at the end of a word_ applies at the last character of the text or before whitespace, punctuation or a symbol.

Where several rows begin with the same roman, the longest wins, and among rows of one length a row whose condition holds comes before a row with none. A row whose condition fails is skipped.

## Rows

The rows are in the order the file states them.

| Roman | Character | Code points | When |
| --- | --- | --- | --- |
| `ng` | `𞵚` | U+1ED5A | always |
| `nG` | `𞵚󠅎󠄧󠇯` | U+1ED5A U+E014E U+E0127 U+E01EF | always |
| `Ng` | `𞵚󠄮󠅇󠇯` | U+1ED5A U+E012E U+E0147 U+E01EF | always |
| `NG` | `𞵚󠄮󠄧󠇯` | U+1ED5A U+E012E U+E0127 U+E01EF | always |
| `dh` | `𞵢` | U+1ED62 | always |
| `dH` | `𞵢󠅄󠄨󠇯` | U+1ED62 U+E0144 U+E0128 U+E01EF | always |
| `Dh` | `𞵢󠄤󠅈󠇯` | U+1ED62 U+E0124 U+E0148 U+E01EF | always |
| `DH` | `𞵢󠄤󠄨󠇯` | U+1ED62 U+E0124 U+E0128 U+E01EF | always |
| `th` | `𞵡` | U+1ED61 | always |
| `tH` | `𞵡󠅔󠄨󠇯` | U+1ED61 U+E0154 U+E0128 U+E01EF | always |
| `Th` | `𞵡󠄴󠅈󠇯` | U+1ED61 U+E0134 U+E0148 U+E01EF | always |
| `TH` | `𞵡󠄴󠄨󠇯` | U+1ED61 U+E0134 U+E0128 U+E01EF | always |
| `kh` | `𞵣` | U+1ED63 | always |
| `kH` | `𞵣󠅋󠄨󠇯` | U+1ED63 U+E014B U+E0128 U+E01EF | always |
| `Kh` | `𞵣󠄫󠅈󠇯` | U+1ED63 U+E012B U+E0148 U+E01EF | always |
| `KH` | `𞵣󠄫󠄨󠇯` | U+1ED63 U+E012B U+E0128 U+E01EF | always |
| `gh` | `𞵤` | U+1ED64 | always |
| `gH` | `𞵤󠅇󠄨󠇯` | U+1ED64 U+E0147 U+E0128 U+E01EF | always |
| `Gh` | `𞵤󠄧󠅈󠇯` | U+1ED64 U+E0127 U+E0148 U+E01EF | always |
| `GH` | `𞵤󠄧󠄨󠇯` | U+1ED64 U+E0127 U+E0128 U+E01EF | always |
| `nk` | `𞵚𞵘󠅎󠅋󠇯` | U+1ED5A U+1ED58 U+E014E U+E014B U+E01EF | always |
| `nK` | `𞵚𞵘󠅎󠄫󠇯` | U+1ED5A U+1ED58 U+E014E U+E012B U+E01EF | always |
| `Nk` | `𞵚𞵘󠄮󠅋󠇯` | U+1ED5A U+1ED58 U+E012E U+E014B U+E01EF | always |
| `NK` | `𞵚𞵘󠄮󠄫󠇯` | U+1ED5A U+1ED58 U+E012E U+E012B U+E01EF | always |
| `ch` | `𞵘` | U+1ED58 | always |
| `cH` | `𞵘󠅃󠄨󠇯` | U+1ED58 U+E0143 U+E0128 U+E01EF | always |
| `Ch` | `𞵘󠄣󠅈󠇯` | U+1ED58 U+E0123 U+E0148 U+E01EF | always |
| `CH` | `𞵘󠄣󠄨󠇯` | U+1ED58 U+E0123 U+E0128 U+E01EF | always |
| `sh` | `𞵔` | U+1ED54 | always |
| `sH` | `𞵔󠅓󠄨󠇯` | U+1ED54 U+E0153 U+E0128 U+E01EF | always |
| `Sh` | `𞵔󠄳󠅈󠇯` | U+1ED54 U+E0133 U+E0148 U+E01EF | always |
| `SH` | `𞵔󠄳󠄨󠇯` | U+1ED54 U+E0133 U+E0128 U+E01EF | always |
| `x` | `𞵘𞵔󠅘󠇯` | U+1ED58 U+1ED54 U+E0158 U+E01EF | always |
| `X` | `𞵘𞵔󠄸󠇯` | U+1ED58 U+1ED54 U+E0138 U+E01EF | always |
| `p` | `𞵐` | U+1ED50 | always |
| `P` | `𞵐󠄰󠇯` | U+1ED50 U+E0130 U+E01EF | always |
| `v` | `𞵑` | U+1ED51 | always |
| `V` | `𞵑󠄶󠇯` | U+1ED51 U+E0136 U+E01EF | always |
| `m` | `𞵒` | U+1ED52 | always |
| `M` | `𞵒󠄭󠇯` | U+1ED52 U+E012D U+E01EF | always |
| `t` | `𞵓` | U+1ED53 | always |
| `T` | `𞵓󠄴󠇯` | U+1ED53 U+E0134 U+E01EF | always |
| `s` | `𞵔󠅓󠇯` | U+1ED54 U+E0153 U+E01EF | always |
| `S` | `𞵔󠄳󠇯` | U+1ED54 U+E0133 U+E01EF | always |
| `n` | `𞵕` | U+1ED55 | always |
| `N` | `𞵕󠄮󠇯` | U+1ED55 U+E012E U+E01EF | always |
| `d` | `𞵖` | U+1ED56 | always |
| `D` | `𞵖󠄤󠇯` | U+1ED56 U+E0124 U+E01EF | always |
| `k` | `𞵘󠅋󠇯` | U+1ED58 U+E014B U+E01EF | always |
| `K` | `𞵘󠄫󠇯` | U+1ED58 U+E012B U+E01EF | always |
| `h` | `𞵙` | U+1ED59 | always |
| `H` | `𞵙󠄨󠇯` | U+1ED59 U+E0128 U+E01EF | always |
| `l` | `𞵛` | U+1ED5B | always |
| `L` | `𞵛󠄬󠇯` | U+1ED5B U+E012C U+E01EF | always |
| `r` | `𞵜` | U+1ED5C | always |
| `R` | `𞵜󠄲󠇯` | U+1ED5C U+E0132 U+E01EF | always |
| `g` | `𞵠` | U+1ED60 | always |
| `G` | `𞵠󠄧󠇯` | U+1ED60 U+E0127 U+E01EF | always |
| `b` | `𞵐󠅂󠇯` | U+1ED50 U+E0142 U+E01EF | always |
| `B` | `𞵐󠄢󠇯` | U+1ED50 U+E0122 U+E01EF | always |
| `f` | `𞵑󠅆󠇯` | U+1ED51 U+E0146 U+E01EF | always |
| `F` | `𞵑󠄦󠇯` | U+1ED51 U+E0126 U+E01EF | always |
| `w` | `𞵑󠅗󠇯` | U+1ED51 U+E0157 U+E01EF | always |
| `W` | `𞵑󠄷󠇯` | U+1ED51 U+E0137 U+E01EF | always |
| `z` | `𞵔󠅚󠇯` | U+1ED54 U+E015A U+E01EF | always |
| `Z` | `𞵔󠄺󠇯` | U+1ED54 U+E013A U+E01EF | always |
| `c` | `𞵘󠅃󠇯` | U+1ED58 U+E0143 U+E01EF | always |
| `C` | `𞵘󠄣󠇯` | U+1ED58 U+E0123 U+E01EF | always |
| `q` | `𞵘󠅑󠇯` | U+1ED58 U+E0151 U+E01EF | always |
| `Q` | `𞵘󠄱󠇯` | U+1ED58 U+E0131 U+E01EF | always |
| `pp` | `𞵐𞵼` | U+1ED50 U+1ED7C | always |
| `pP` | `𞵐𞵼󠅐󠄰󠇯` | U+1ED50 U+1ED7C U+E0150 U+E0130 U+E01EF | always |
| `Pp` | `𞵐𞵼󠄰󠅐󠇯` | U+1ED50 U+1ED7C U+E0130 U+E0150 U+E01EF | always |
| `PP` | `𞵐𞵼󠄰󠄰󠇯` | U+1ED50 U+1ED7C U+E0130 U+E0130 U+E01EF | always |
| `vv` | `𞵑𞵼` | U+1ED51 U+1ED7C | always |
| `vV` | `𞵑𞵼󠅖󠄶󠇯` | U+1ED51 U+1ED7C U+E0156 U+E0136 U+E01EF | always |
| `Vv` | `𞵑𞵼󠄶󠅖󠇯` | U+1ED51 U+1ED7C U+E0136 U+E0156 U+E01EF | always |
| `VV` | `𞵑𞵼󠄶󠄶󠇯` | U+1ED51 U+1ED7C U+E0136 U+E0136 U+E01EF | always |
| `mm` | `𞵒𞵼` | U+1ED52 U+1ED7C | always |
| `mM` | `𞵒𞵼󠅍󠄭󠇯` | U+1ED52 U+1ED7C U+E014D U+E012D U+E01EF | always |
| `Mm` | `𞵒𞵼󠄭󠅍󠇯` | U+1ED52 U+1ED7C U+E012D U+E014D U+E01EF | always |
| `MM` | `𞵒𞵼󠄭󠄭󠇯` | U+1ED52 U+1ED7C U+E012D U+E012D U+E01EF | always |
| `tt` | `𞵓𞵼` | U+1ED53 U+1ED7C | always |
| `tT` | `𞵓𞵼󠅔󠄴󠇯` | U+1ED53 U+1ED7C U+E0154 U+E0134 U+E01EF | always |
| `Tt` | `𞵓𞵼󠄴󠅔󠇯` | U+1ED53 U+1ED7C U+E0134 U+E0154 U+E01EF | always |
| `TT` | `𞵓𞵼󠄴󠄴󠇯` | U+1ED53 U+1ED7C U+E0134 U+E0134 U+E01EF | always |
| `ss` | `𞵔𞵼` | U+1ED54 U+1ED7C | always |
| `sS` | `𞵔𞵼󠅓󠄳󠇯` | U+1ED54 U+1ED7C U+E0153 U+E0133 U+E01EF | always |
| `Ss` | `𞵔𞵼󠄳󠅓󠇯` | U+1ED54 U+1ED7C U+E0133 U+E0153 U+E01EF | always |
| `SS` | `𞵔𞵼󠄳󠄳󠇯` | U+1ED54 U+1ED7C U+E0133 U+E0133 U+E01EF | always |
| `nn` | `𞵕𞵼` | U+1ED55 U+1ED7C | always |
| `nN` | `𞵕𞵼󠅎󠄮󠇯` | U+1ED55 U+1ED7C U+E014E U+E012E U+E01EF | always |
| `Nn` | `𞵕𞵼󠄮󠅎󠇯` | U+1ED55 U+1ED7C U+E012E U+E014E U+E01EF | always |
| `NN` | `𞵕𞵼󠄮󠄮󠇯` | U+1ED55 U+1ED7C U+E012E U+E012E U+E01EF | always |
| `dd` | `𞵖𞵼` | U+1ED56 U+1ED7C | always |
| `dD` | `𞵖𞵼󠅄󠄤󠇯` | U+1ED56 U+1ED7C U+E0144 U+E0124 U+E01EF | always |
| `Dd` | `𞵖𞵼󠄤󠅄󠇯` | U+1ED56 U+1ED7C U+E0124 U+E0144 U+E01EF | always |
| `DD` | `𞵖𞵼󠄤󠄤󠇯` | U+1ED56 U+1ED7C U+E0124 U+E0124 U+E01EF | always |
| `kk` | `𞵘𞵼` | U+1ED58 U+1ED7C | always |
| `kK` | `𞵘𞵼󠅋󠄫󠇯` | U+1ED58 U+1ED7C U+E014B U+E012B U+E01EF | always |
| `Kk` | `𞵘𞵼󠄫󠅋󠇯` | U+1ED58 U+1ED7C U+E012B U+E014B U+E01EF | always |
| `KK` | `𞵘𞵼󠄫󠄫󠇯` | U+1ED58 U+1ED7C U+E012B U+E012B U+E01EF | always |
| `hh` | `𞵙𞵼` | U+1ED59 U+1ED7C | always |
| `hH` | `𞵙𞵼󠅈󠄨󠇯` | U+1ED59 U+1ED7C U+E0148 U+E0128 U+E01EF | always |
| `Hh` | `𞵙𞵼󠄨󠅈󠇯` | U+1ED59 U+1ED7C U+E0128 U+E0148 U+E01EF | always |
| `HH` | `𞵙𞵼󠄨󠄨󠇯` | U+1ED59 U+1ED7C U+E0128 U+E0128 U+E01EF | always |
| `ll` | `𞵛𞵼` | U+1ED5B U+1ED7C | always |
| `lL` | `𞵛𞵼󠅌󠄬󠇯` | U+1ED5B U+1ED7C U+E014C U+E012C U+E01EF | always |
| `Ll` | `𞵛𞵼󠄬󠅌󠇯` | U+1ED5B U+1ED7C U+E012C U+E014C U+E01EF | always |
| `LL` | `𞵛𞵼󠄬󠄬󠇯` | U+1ED5B U+1ED7C U+E012C U+E012C U+E01EF | always |
| `rr` | `𞵜𞵼` | U+1ED5C U+1ED7C | always |
| `rR` | `𞵜𞵼󠅒󠄲󠇯` | U+1ED5C U+1ED7C U+E0152 U+E0132 U+E01EF | always |
| `Rr` | `𞵜𞵼󠄲󠅒󠇯` | U+1ED5C U+1ED7C U+E0132 U+E0152 U+E01EF | always |
| `RR` | `𞵜𞵼󠄲󠄲󠇯` | U+1ED5C U+1ED7C U+E0132 U+E0132 U+E01EF | always |
| `gg` | `𞵠𞵼` | U+1ED60 U+1ED7C | always |
| `gG` | `𞵠𞵼󠅇󠄧󠇯` | U+1ED60 U+1ED7C U+E0147 U+E0127 U+E01EF | always |
| `Gg` | `𞵠𞵼󠄧󠅇󠇯` | U+1ED60 U+1ED7C U+E0127 U+E0147 U+E01EF | always |
| `GG` | `𞵠𞵼󠄧󠄧󠇯` | U+1ED60 U+1ED7C U+E0127 U+E0127 U+E01EF | always |
| `ngng` | `𞵚𞵼` | U+1ED5A U+1ED7C | always |
| `ngnG` | `𞵚𞵼󠅎󠅇󠅎󠄧󠇯` | U+1ED5A U+1ED7C U+E014E U+E0147 U+E014E U+E0127 U+E01EF | always |
| `ngNg` | `𞵚𞵼󠅎󠅇󠄮󠅇󠇯` | U+1ED5A U+1ED7C U+E014E U+E0147 U+E012E U+E0147 U+E01EF | always |
| `ngNG` | `𞵚𞵼󠅎󠅇󠄮󠄧󠇯` | U+1ED5A U+1ED7C U+E014E U+E0147 U+E012E U+E0127 U+E01EF | always |
| `nGng` | `𞵚𞵼󠅎󠄧󠅎󠅇󠇯` | U+1ED5A U+1ED7C U+E014E U+E0127 U+E014E U+E0147 U+E01EF | always |
| `nGnG` | `𞵚𞵼󠅎󠄧󠅎󠄧󠇯` | U+1ED5A U+1ED7C U+E014E U+E0127 U+E014E U+E0127 U+E01EF | always |
| `nGNg` | `𞵚𞵼󠅎󠄧󠄮󠅇󠇯` | U+1ED5A U+1ED7C U+E014E U+E0127 U+E012E U+E0147 U+E01EF | always |
| `nGNG` | `𞵚𞵼󠅎󠄧󠄮󠄧󠇯` | U+1ED5A U+1ED7C U+E014E U+E0127 U+E012E U+E0127 U+E01EF | always |
| `Ngng` | `𞵚𞵼󠄮󠅇󠅎󠅇󠇯` | U+1ED5A U+1ED7C U+E012E U+E0147 U+E014E U+E0147 U+E01EF | always |
| `NgnG` | `𞵚𞵼󠄮󠅇󠅎󠄧󠇯` | U+1ED5A U+1ED7C U+E012E U+E0147 U+E014E U+E0127 U+E01EF | always |
| `NgNg` | `𞵚𞵼󠄮󠅇󠄮󠅇󠇯` | U+1ED5A U+1ED7C U+E012E U+E0147 U+E012E U+E0147 U+E01EF | always |
| `NgNG` | `𞵚𞵼󠄮󠅇󠄮󠄧󠇯` | U+1ED5A U+1ED7C U+E012E U+E0147 U+E012E U+E0127 U+E01EF | always |
| `NGng` | `𞵚𞵼󠄮󠄧󠅎󠅇󠇯` | U+1ED5A U+1ED7C U+E012E U+E0127 U+E014E U+E0147 U+E01EF | always |
| `NGnG` | `𞵚𞵼󠄮󠄧󠅎󠄧󠇯` | U+1ED5A U+1ED7C U+E012E U+E0127 U+E014E U+E0127 U+E01EF | always |
| `NGNg` | `𞵚𞵼󠄮󠄧󠄮󠅇󠇯` | U+1ED5A U+1ED7C U+E012E U+E0127 U+E012E U+E0147 U+E01EF | always |
| `NGNG` | `𞵚𞵼󠄮󠄧󠄮󠄧󠇯` | U+1ED5A U+1ED7C U+E012E U+E0127 U+E012E U+E0127 U+E01EF | always |
| `dhdh` | `𞵢𞵼` | U+1ED62 U+1ED7C | always |
| `dhdH` | `𞵢𞵼󠅄󠅈󠅄󠄨󠇯` | U+1ED62 U+1ED7C U+E0144 U+E0148 U+E0144 U+E0128 U+E01EF | always |
| `dhDh` | `𞵢𞵼󠅄󠅈󠄤󠅈󠇯` | U+1ED62 U+1ED7C U+E0144 U+E0148 U+E0124 U+E0148 U+E01EF | always |
| `dhDH` | `𞵢𞵼󠅄󠅈󠄤󠄨󠇯` | U+1ED62 U+1ED7C U+E0144 U+E0148 U+E0124 U+E0128 U+E01EF | always |
| `dHdh` | `𞵢𞵼󠅄󠄨󠅄󠅈󠇯` | U+1ED62 U+1ED7C U+E0144 U+E0128 U+E0144 U+E0148 U+E01EF | always |
| `dHdH` | `𞵢𞵼󠅄󠄨󠅄󠄨󠇯` | U+1ED62 U+1ED7C U+E0144 U+E0128 U+E0144 U+E0128 U+E01EF | always |
| `dHDh` | `𞵢𞵼󠅄󠄨󠄤󠅈󠇯` | U+1ED62 U+1ED7C U+E0144 U+E0128 U+E0124 U+E0148 U+E01EF | always |
| `dHDH` | `𞵢𞵼󠅄󠄨󠄤󠄨󠇯` | U+1ED62 U+1ED7C U+E0144 U+E0128 U+E0124 U+E0128 U+E01EF | always |
| `Dhdh` | `𞵢𞵼󠄤󠅈󠅄󠅈󠇯` | U+1ED62 U+1ED7C U+E0124 U+E0148 U+E0144 U+E0148 U+E01EF | always |
| `DhdH` | `𞵢𞵼󠄤󠅈󠅄󠄨󠇯` | U+1ED62 U+1ED7C U+E0124 U+E0148 U+E0144 U+E0128 U+E01EF | always |
| `DhDh` | `𞵢𞵼󠄤󠅈󠄤󠅈󠇯` | U+1ED62 U+1ED7C U+E0124 U+E0148 U+E0124 U+E0148 U+E01EF | always |
| `DhDH` | `𞵢𞵼󠄤󠅈󠄤󠄨󠇯` | U+1ED62 U+1ED7C U+E0124 U+E0148 U+E0124 U+E0128 U+E01EF | always |
| `DHdh` | `𞵢𞵼󠄤󠄨󠅄󠅈󠇯` | U+1ED62 U+1ED7C U+E0124 U+E0128 U+E0144 U+E0148 U+E01EF | always |
| `DHdH` | `𞵢𞵼󠄤󠄨󠅄󠄨󠇯` | U+1ED62 U+1ED7C U+E0124 U+E0128 U+E0144 U+E0128 U+E01EF | always |
| `DHDh` | `𞵢𞵼󠄤󠄨󠄤󠅈󠇯` | U+1ED62 U+1ED7C U+E0124 U+E0128 U+E0124 U+E0148 U+E01EF | always |
| `DHDH` | `𞵢𞵼󠄤󠄨󠄤󠄨󠇯` | U+1ED62 U+1ED7C U+E0124 U+E0128 U+E0124 U+E0128 U+E01EF | always |
| `thth` | `𞵡𞵼` | U+1ED61 U+1ED7C | always |
| `thtH` | `𞵡𞵼󠅔󠅈󠅔󠄨󠇯` | U+1ED61 U+1ED7C U+E0154 U+E0148 U+E0154 U+E0128 U+E01EF | always |
| `thTh` | `𞵡𞵼󠅔󠅈󠄴󠅈󠇯` | U+1ED61 U+1ED7C U+E0154 U+E0148 U+E0134 U+E0148 U+E01EF | always |
| `thTH` | `𞵡𞵼󠅔󠅈󠄴󠄨󠇯` | U+1ED61 U+1ED7C U+E0154 U+E0148 U+E0134 U+E0128 U+E01EF | always |
| `tHth` | `𞵡𞵼󠅔󠄨󠅔󠅈󠇯` | U+1ED61 U+1ED7C U+E0154 U+E0128 U+E0154 U+E0148 U+E01EF | always |
| `tHtH` | `𞵡𞵼󠅔󠄨󠅔󠄨󠇯` | U+1ED61 U+1ED7C U+E0154 U+E0128 U+E0154 U+E0128 U+E01EF | always |
| `tHTh` | `𞵡𞵼󠅔󠄨󠄴󠅈󠇯` | U+1ED61 U+1ED7C U+E0154 U+E0128 U+E0134 U+E0148 U+E01EF | always |
| `tHTH` | `𞵡𞵼󠅔󠄨󠄴󠄨󠇯` | U+1ED61 U+1ED7C U+E0154 U+E0128 U+E0134 U+E0128 U+E01EF | always |
| `Thth` | `𞵡𞵼󠄴󠅈󠅔󠅈󠇯` | U+1ED61 U+1ED7C U+E0134 U+E0148 U+E0154 U+E0148 U+E01EF | always |
| `ThtH` | `𞵡𞵼󠄴󠅈󠅔󠄨󠇯` | U+1ED61 U+1ED7C U+E0134 U+E0148 U+E0154 U+E0128 U+E01EF | always |
| `ThTh` | `𞵡𞵼󠄴󠅈󠄴󠅈󠇯` | U+1ED61 U+1ED7C U+E0134 U+E0148 U+E0134 U+E0148 U+E01EF | always |
| `ThTH` | `𞵡𞵼󠄴󠅈󠄴󠄨󠇯` | U+1ED61 U+1ED7C U+E0134 U+E0148 U+E0134 U+E0128 U+E01EF | always |
| `THth` | `𞵡𞵼󠄴󠄨󠅔󠅈󠇯` | U+1ED61 U+1ED7C U+E0134 U+E0128 U+E0154 U+E0148 U+E01EF | always |
| `THtH` | `𞵡𞵼󠄴󠄨󠅔󠄨󠇯` | U+1ED61 U+1ED7C U+E0134 U+E0128 U+E0154 U+E0128 U+E01EF | always |
| `THTh` | `𞵡𞵼󠄴󠄨󠄴󠅈󠇯` | U+1ED61 U+1ED7C U+E0134 U+E0128 U+E0134 U+E0148 U+E01EF | always |
| `THTH` | `𞵡𞵼󠄴󠄨󠄴󠄨󠇯` | U+1ED61 U+1ED7C U+E0134 U+E0128 U+E0134 U+E0128 U+E01EF | always |
| `khkh` | `𞵣𞵼` | U+1ED63 U+1ED7C | always |
| `khkH` | `𞵣𞵼󠅋󠅈󠅋󠄨󠇯` | U+1ED63 U+1ED7C U+E014B U+E0148 U+E014B U+E0128 U+E01EF | always |
| `khKh` | `𞵣𞵼󠅋󠅈󠄫󠅈󠇯` | U+1ED63 U+1ED7C U+E014B U+E0148 U+E012B U+E0148 U+E01EF | always |
| `khKH` | `𞵣𞵼󠅋󠅈󠄫󠄨󠇯` | U+1ED63 U+1ED7C U+E014B U+E0148 U+E012B U+E0128 U+E01EF | always |
| `kHkh` | `𞵣𞵼󠅋󠄨󠅋󠅈󠇯` | U+1ED63 U+1ED7C U+E014B U+E0128 U+E014B U+E0148 U+E01EF | always |
| `kHkH` | `𞵣𞵼󠅋󠄨󠅋󠄨󠇯` | U+1ED63 U+1ED7C U+E014B U+E0128 U+E014B U+E0128 U+E01EF | always |
| `kHKh` | `𞵣𞵼󠅋󠄨󠄫󠅈󠇯` | U+1ED63 U+1ED7C U+E014B U+E0128 U+E012B U+E0148 U+E01EF | always |
| `kHKH` | `𞵣𞵼󠅋󠄨󠄫󠄨󠇯` | U+1ED63 U+1ED7C U+E014B U+E0128 U+E012B U+E0128 U+E01EF | always |
| `Khkh` | `𞵣𞵼󠄫󠅈󠅋󠅈󠇯` | U+1ED63 U+1ED7C U+E012B U+E0148 U+E014B U+E0148 U+E01EF | always |
| `KhkH` | `𞵣𞵼󠄫󠅈󠅋󠄨󠇯` | U+1ED63 U+1ED7C U+E012B U+E0148 U+E014B U+E0128 U+E01EF | always |
| `KhKh` | `𞵣𞵼󠄫󠅈󠄫󠅈󠇯` | U+1ED63 U+1ED7C U+E012B U+E0148 U+E012B U+E0148 U+E01EF | always |
| `KhKH` | `𞵣𞵼󠄫󠅈󠄫󠄨󠇯` | U+1ED63 U+1ED7C U+E012B U+E0148 U+E012B U+E0128 U+E01EF | always |
| `KHkh` | `𞵣𞵼󠄫󠄨󠅋󠅈󠇯` | U+1ED63 U+1ED7C U+E012B U+E0128 U+E014B U+E0148 U+E01EF | always |
| `KHkH` | `𞵣𞵼󠄫󠄨󠅋󠄨󠇯` | U+1ED63 U+1ED7C U+E012B U+E0128 U+E014B U+E0128 U+E01EF | always |
| `KHKh` | `𞵣𞵼󠄫󠄨󠄫󠅈󠇯` | U+1ED63 U+1ED7C U+E012B U+E0128 U+E012B U+E0148 U+E01EF | always |
| `KHKH` | `𞵣𞵼󠄫󠄨󠄫󠄨󠇯` | U+1ED63 U+1ED7C U+E012B U+E0128 U+E012B U+E0128 U+E01EF | always |
| `ghgh` | `𞵤𞵼` | U+1ED64 U+1ED7C | always |
| `ghgH` | `𞵤𞵼󠅇󠅈󠅇󠄨󠇯` | U+1ED64 U+1ED7C U+E0147 U+E0148 U+E0147 U+E0128 U+E01EF | always |
| `ghGh` | `𞵤𞵼󠅇󠅈󠄧󠅈󠇯` | U+1ED64 U+1ED7C U+E0147 U+E0148 U+E0127 U+E0148 U+E01EF | always |
| `ghGH` | `𞵤𞵼󠅇󠅈󠄧󠄨󠇯` | U+1ED64 U+1ED7C U+E0147 U+E0148 U+E0127 U+E0128 U+E01EF | always |
| `gHgh` | `𞵤𞵼󠅇󠄨󠅇󠅈󠇯` | U+1ED64 U+1ED7C U+E0147 U+E0128 U+E0147 U+E0148 U+E01EF | always |
| `gHgH` | `𞵤𞵼󠅇󠄨󠅇󠄨󠇯` | U+1ED64 U+1ED7C U+E0147 U+E0128 U+E0147 U+E0128 U+E01EF | always |
| `gHGh` | `𞵤𞵼󠅇󠄨󠄧󠅈󠇯` | U+1ED64 U+1ED7C U+E0147 U+E0128 U+E0127 U+E0148 U+E01EF | always |
| `gHGH` | `𞵤𞵼󠅇󠄨󠄧󠄨󠇯` | U+1ED64 U+1ED7C U+E0147 U+E0128 U+E0127 U+E0128 U+E01EF | always |
| `Ghgh` | `𞵤𞵼󠄧󠅈󠅇󠅈󠇯` | U+1ED64 U+1ED7C U+E0127 U+E0148 U+E0147 U+E0148 U+E01EF | always |
| `GhgH` | `𞵤𞵼󠄧󠅈󠅇󠄨󠇯` | U+1ED64 U+1ED7C U+E0127 U+E0148 U+E0147 U+E0128 U+E01EF | always |
| `GhGh` | `𞵤𞵼󠄧󠅈󠄧󠅈󠇯` | U+1ED64 U+1ED7C U+E0127 U+E0148 U+E0127 U+E0148 U+E01EF | always |
| `GhGH` | `𞵤𞵼󠄧󠅈󠄧󠄨󠇯` | U+1ED64 U+1ED7C U+E0127 U+E0148 U+E0127 U+E0128 U+E01EF | always |
| `GHgh` | `𞵤𞵼󠄧󠄨󠅇󠅈󠇯` | U+1ED64 U+1ED7C U+E0127 U+E0128 U+E0147 U+E0148 U+E01EF | always |
| `GHgH` | `𞵤𞵼󠄧󠄨󠅇󠄨󠇯` | U+1ED64 U+1ED7C U+E0127 U+E0128 U+E0147 U+E0128 U+E01EF | always |
| `GHGh` | `𞵤𞵼󠄧󠄨󠄧󠅈󠇯` | U+1ED64 U+1ED7C U+E0127 U+E0128 U+E0127 U+E0148 U+E01EF | always |
| `GHGH` | `𞵤𞵼󠄧󠄨󠄧󠄨󠇯` | U+1ED64 U+1ED7C U+E0127 U+E0128 U+E0127 U+E0128 U+E01EF | always |
| `-` | `󠄍` | U+E010D | at the start of a word |
| `-` | `󠄍` | U+E010D | at the end of a word |
| `-` | ` 󠄍󠇯` | U+0020 U+E010D U+E01EF | always |
| `a` | `𞵝𞵰` | U+1ED5D U+1ED70 | at the start of a word |
| `a` | `𞵰` | U+1ED70 | always |
| `A` | `𞵝𞵰󠄡󠇯` | U+1ED5D U+1ED70 U+E0121 U+E01EF | at the start of a word |
| `A` | `𞵰󠄡󠇯` | U+1ED70 U+E0121 U+E01EF | always |
| `á` | `𞵝𞵰󠅛󠅅󠄑󠅝󠇯` | U+1ED5D U+1ED70 U+E015B U+E0145 U+E0111 U+E015D U+E01EF | at the start of a word |
| `á` | `𞵰󠅛󠅅󠄑󠅝󠇯` | U+1ED70 U+E015B U+E0145 U+E0111 U+E015D U+E01EF | always |
| `Á` | `𞵝𞵰󠅛󠅃󠄑󠅝󠇯` | U+1ED5D U+1ED70 U+E015B U+E0143 U+E0111 U+E015D U+E01EF | at the start of a word |
| `Á` | `𞵰󠅛󠅃󠄑󠅝󠇯` | U+1ED70 U+E015B U+E0143 U+E0111 U+E015D U+E01EF | always |
| `e` | `𞵝𞵳` | U+1ED5D U+1ED73 | at the start of a word |
| `e` | `𞵳` | U+1ED73 | always |
| `E` | `𞵝𞵳󠄥󠇯` | U+1ED5D U+1ED73 U+E0125 U+E01EF | at the start of a word |
| `E` | `𞵳󠄥󠇯` | U+1ED73 U+E0125 U+E01EF | always |
| `é` | `𞵝𞵳󠅛󠅅󠄙󠅝󠇯` | U+1ED5D U+1ED73 U+E015B U+E0145 U+E0119 U+E015D U+E01EF | at the start of a word |
| `é` | `𞵳󠅛󠅅󠄙󠅝󠇯` | U+1ED73 U+E015B U+E0145 U+E0119 U+E015D U+E01EF | always |
| `É` | `𞵝𞵳󠅛󠅃󠄙󠅝󠇯` | U+1ED5D U+1ED73 U+E015B U+E0143 U+E0119 U+E015D U+E01EF | at the start of a word |
| `É` | `𞵳󠅛󠅃󠄙󠅝󠇯` | U+1ED73 U+E015B U+E0143 U+E0119 U+E015D U+E01EF | always |
| `i` | `𞵝𞵴` | U+1ED5D U+1ED74 | at the start of a word |
| `i` | `𞵴` | U+1ED74 | always |
| `I` | `𞵝𞵴󠄩󠇯` | U+1ED5D U+1ED74 U+E0129 U+E01EF | at the start of a word |
| `I` | `𞵴󠄩󠇯` | U+1ED74 U+E0129 U+E01EF | always |
| `í` | `𞵝𞵴󠅛󠅅󠅄󠅝󠇯` | U+1ED5D U+1ED74 U+E015B U+E0145 U+E0144 U+E015D U+E01EF | at the start of a word |
| `í` | `𞵴󠅛󠅅󠅄󠅝󠇯` | U+1ED74 U+E015B U+E0145 U+E0144 U+E015D U+E01EF | always |
| `Í` | `𞵝𞵴󠅛󠅃󠅄󠅝󠇯` | U+1ED5D U+1ED74 U+E015B U+E0143 U+E0144 U+E015D U+E01EF | at the start of a word |
| `Í` | `𞵴󠅛󠅃󠅄󠅝󠇯` | U+1ED74 U+E015B U+E0143 U+E0144 U+E015D U+E01EF | always |
| `o` | `𞵝𞵱` | U+1ED5D U+1ED71 | at the start of a word |
| `o` | `𞵱` | U+1ED71 | always |
| `O` | `𞵝𞵱󠄯󠇯` | U+1ED5D U+1ED71 U+E012F U+E01EF | at the start of a word |
| `O` | `𞵱󠄯󠇯` | U+1ED71 U+E012F U+E01EF | always |
| `ó` | `𞵝𞵱󠅛󠅆󠄓󠅝󠇯` | U+1ED5D U+1ED71 U+E015B U+E0146 U+E0113 U+E015D U+E01EF | at the start of a word |
| `ó` | `𞵱󠅛󠅆󠄓󠅝󠇯` | U+1ED71 U+E015B U+E0146 U+E0113 U+E015D U+E01EF | always |
| `Ó` | `𞵝𞵱󠅛󠅄󠄓󠅝󠇯` | U+1ED5D U+1ED71 U+E015B U+E0144 U+E0113 U+E015D U+E01EF | at the start of a word |
| `Ó` | `𞵱󠅛󠅄󠄓󠅝󠇯` | U+1ED71 U+E015B U+E0144 U+E0113 U+E015D U+E01EF | always |
| `u` | `𞵝𞵲` | U+1ED5D U+1ED72 | at the start of a word |
| `u` | `𞵲` | U+1ED72 | always |
| `U` | `𞵝𞵲󠄵󠇯` | U+1ED5D U+1ED72 U+E0135 U+E01EF | at the start of a word |
| `U` | `𞵲󠄵󠇯` | U+1ED72 U+E0135 U+E01EF | always |
| `ú` | `𞵝𞵲󠅛󠅆󠅁󠅝󠇯` | U+1ED5D U+1ED72 U+E015B U+E0146 U+E0141 U+E015D U+E01EF | at the start of a word |
| `ú` | `𞵲󠅛󠅆󠅁󠅝󠇯` | U+1ED72 U+E015B U+E0146 U+E0141 U+E015D U+E01EF | always |
| `Ú` | `𞵝𞵲󠅛󠅄󠅁󠅝󠇯` | U+1ED5D U+1ED72 U+E015B U+E0144 U+E0141 U+E015D U+E01EF | at the start of a word |
| `Ú` | `𞵲󠅛󠅄󠅁󠅝󠇯` | U+1ED72 U+E015B U+E0144 U+E0141 U+E015D U+E01EF | always |
| `y` | `𞵝𞵵` | U+1ED5D U+1ED75 | at the start of a word |
| `y` | `𞵵` | U+1ED75 | always |
| `Y` | `𞵝𞵵󠄹󠇯` | U+1ED5D U+1ED75 U+E0139 U+E01EF | at the start of a word |
| `Y` | `𞵵󠄹󠇯` | U+1ED75 U+E0139 U+E01EF | always |
| `ý` | `𞵝𞵵󠅛󠅆󠅄󠅝󠇯` | U+1ED5D U+1ED75 U+E015B U+E0146 U+E0144 U+E015D U+E01EF | at the start of a word |
| `ý` | `𞵵󠅛󠅆󠅄󠅝󠇯` | U+1ED75 U+E015B U+E0146 U+E0144 U+E015D U+E01EF | always |
| `Ý` | `𞵝𞵵󠅛󠅄󠅄󠅝󠇯` | U+1ED5D U+1ED75 U+E015B U+E0144 U+E0144 U+E015D U+E01EF | at the start of a word |
| `Ý` | `𞵵󠅛󠅄󠅄󠅝󠇯` | U+1ED75 U+E015B U+E0144 U+E0144 U+E015D U+E01EF | always |
| `ë` | `𞵝𞵶` | U+1ED5D U+1ED76 | at the start of a word |
| `ë` | `𞵶` | U+1ED76 | always |
| `Ë` | `𞵝𞵶󠅛󠅃󠅂󠅝󠇯` | U+1ED5D U+1ED76 U+E015B U+E0143 U+E0142 U+E015D U+E01EF | at the start of a word |
| `Ë` | `𞵶󠅛󠅃󠅂󠅝󠇯` | U+1ED76 U+E015B U+E0143 U+E0142 U+E015D U+E01EF | always |
| `j` | `𞵝𞵵󠅊󠇯` | U+1ED5D U+1ED75 U+E014A U+E01EF | at the start of a word |
| `j` | `𞵵󠅊󠇯` | U+1ED75 U+E014A U+E01EF | always |
| `J` | `𞵝𞵵󠄪󠇯` | U+1ED5D U+1ED75 U+E012A U+E01EF | at the start of a word |
| `J` | `𞵵󠄪󠇯` | U+1ED75 U+E012A U+E01EF | always |
| `aa` | `𞵝𞵰𞵸` | U+1ED5D U+1ED70 U+1ED78 | at the start of a word |
| `aa` | `𞵰𞵸` | U+1ED70 U+1ED78 | always |
| `aA` | `𞵝𞵰𞵸󠅁󠄡󠇯` | U+1ED5D U+1ED70 U+1ED78 U+E0141 U+E0121 U+E01EF | at the start of a word |
| `aA` | `𞵰𞵸󠅁󠄡󠇯` | U+1ED70 U+1ED78 U+E0141 U+E0121 U+E01EF | always |
| `aá` | `𞵝𞵰𞵸󠅁󠅛󠅅󠄑󠅝󠇯` | U+1ED5D U+1ED70 U+1ED78 U+E0141 U+E015B U+E0145 U+E0111 U+E015D U+E01EF | at the start of a word |
| `aá` | `𞵰𞵸󠅁󠅛󠅅󠄑󠅝󠇯` | U+1ED70 U+1ED78 U+E0141 U+E015B U+E0145 U+E0111 U+E015D U+E01EF | always |
| `aÁ` | `𞵝𞵰𞵸󠅁󠅛󠅃󠄑󠅝󠇯` | U+1ED5D U+1ED70 U+1ED78 U+E0141 U+E015B U+E0143 U+E0111 U+E015D U+E01EF | at the start of a word |
| `aÁ` | `𞵰𞵸󠅁󠅛󠅃󠄑󠅝󠇯` | U+1ED70 U+1ED78 U+E0141 U+E015B U+E0143 U+E0111 U+E015D U+E01EF | always |
| `Aa` | `𞵝𞵰𞵸󠄡󠅁󠇯` | U+1ED5D U+1ED70 U+1ED78 U+E0121 U+E0141 U+E01EF | at the start of a word |
| `Aa` | `𞵰𞵸󠄡󠅁󠇯` | U+1ED70 U+1ED78 U+E0121 U+E0141 U+E01EF | always |
| `AA` | `𞵝𞵰𞵸󠄡󠄡󠇯` | U+1ED5D U+1ED70 U+1ED78 U+E0121 U+E0121 U+E01EF | at the start of a word |
| `AA` | `𞵰𞵸󠄡󠄡󠇯` | U+1ED70 U+1ED78 U+E0121 U+E0121 U+E01EF | always |
| `Aá` | `𞵝𞵰𞵸󠄡󠅛󠅅󠄑󠅝󠇯` | U+1ED5D U+1ED70 U+1ED78 U+E0121 U+E015B U+E0145 U+E0111 U+E015D U+E01EF | at the start of a word |
| `Aá` | `𞵰𞵸󠄡󠅛󠅅󠄑󠅝󠇯` | U+1ED70 U+1ED78 U+E0121 U+E015B U+E0145 U+E0111 U+E015D U+E01EF | always |
| `AÁ` | `𞵝𞵰𞵸󠄡󠅛󠅃󠄑󠅝󠇯` | U+1ED5D U+1ED70 U+1ED78 U+E0121 U+E015B U+E0143 U+E0111 U+E015D U+E01EF | at the start of a word |
| `AÁ` | `𞵰𞵸󠄡󠅛󠅃󠄑󠅝󠇯` | U+1ED70 U+1ED78 U+E0121 U+E015B U+E0143 U+E0111 U+E015D U+E01EF | always |
| `áa` | `𞵝𞵰𞵸󠅛󠅅󠄑󠅝󠅁󠇯` | U+1ED5D U+1ED70 U+1ED78 U+E015B U+E0145 U+E0111 U+E015D U+E0141 U+E01EF | at the start of a word |
| `áa` | `𞵰𞵸󠅛󠅅󠄑󠅝󠅁󠇯` | U+1ED70 U+1ED78 U+E015B U+E0145 U+E0111 U+E015D U+E0141 U+E01EF | always |
| `áA` | `𞵝𞵰𞵸󠅛󠅅󠄑󠅝󠄡󠇯` | U+1ED5D U+1ED70 U+1ED78 U+E015B U+E0145 U+E0111 U+E015D U+E0121 U+E01EF | at the start of a word |
| `áA` | `𞵰𞵸󠅛󠅅󠄑󠅝󠄡󠇯` | U+1ED70 U+1ED78 U+E015B U+E0145 U+E0111 U+E015D U+E0121 U+E01EF | always |
| `áá` | `𞵝𞵰𞵸󠅛󠅅󠄑󠅝󠅛󠅅󠄑󠅝󠇯` | U+1ED5D U+1ED70 U+1ED78 U+E015B U+E0145 U+E0111 U+E015D U+E015B U+E0145 U+E0111 U+E015D U+E01EF | at the start of a word |
| `áá` | `𞵰𞵸󠅛󠅅󠄑󠅝󠅛󠅅󠄑󠅝󠇯` | U+1ED70 U+1ED78 U+E015B U+E0145 U+E0111 U+E015D U+E015B U+E0145 U+E0111 U+E015D U+E01EF | always |
| `áÁ` | `𞵝𞵰𞵸󠅛󠅅󠄑󠅝󠅛󠅃󠄑󠅝󠇯` | U+1ED5D U+1ED70 U+1ED78 U+E015B U+E0145 U+E0111 U+E015D U+E015B U+E0143 U+E0111 U+E015D U+E01EF | at the start of a word |
| `áÁ` | `𞵰𞵸󠅛󠅅󠄑󠅝󠅛󠅃󠄑󠅝󠇯` | U+1ED70 U+1ED78 U+E015B U+E0145 U+E0111 U+E015D U+E015B U+E0143 U+E0111 U+E015D U+E01EF | always |
| `Áa` | `𞵝𞵰𞵸󠅛󠅃󠄑󠅝󠅁󠇯` | U+1ED5D U+1ED70 U+1ED78 U+E015B U+E0143 U+E0111 U+E015D U+E0141 U+E01EF | at the start of a word |
| `Áa` | `𞵰𞵸󠅛󠅃󠄑󠅝󠅁󠇯` | U+1ED70 U+1ED78 U+E015B U+E0143 U+E0111 U+E015D U+E0141 U+E01EF | always |
| `ÁA` | `𞵝𞵰𞵸󠅛󠅃󠄑󠅝󠄡󠇯` | U+1ED5D U+1ED70 U+1ED78 U+E015B U+E0143 U+E0111 U+E015D U+E0121 U+E01EF | at the start of a word |
| `ÁA` | `𞵰𞵸󠅛󠅃󠄑󠅝󠄡󠇯` | U+1ED70 U+1ED78 U+E015B U+E0143 U+E0111 U+E015D U+E0121 U+E01EF | always |
| `Áá` | `𞵝𞵰𞵸󠅛󠅃󠄑󠅝󠅛󠅅󠄑󠅝󠇯` | U+1ED5D U+1ED70 U+1ED78 U+E015B U+E0143 U+E0111 U+E015D U+E015B U+E0145 U+E0111 U+E015D U+E01EF | at the start of a word |
| `Áá` | `𞵰𞵸󠅛󠅃󠄑󠅝󠅛󠅅󠄑󠅝󠇯` | U+1ED70 U+1ED78 U+E015B U+E0143 U+E0111 U+E015D U+E015B U+E0145 U+E0111 U+E015D U+E01EF | always |
| `ÁÁ` | `𞵝𞵰𞵸󠅛󠅃󠄑󠅝󠅛󠅃󠄑󠅝󠇯` | U+1ED5D U+1ED70 U+1ED78 U+E015B U+E0143 U+E0111 U+E015D U+E015B U+E0143 U+E0111 U+E015D U+E01EF | at the start of a word |
| `ÁÁ` | `𞵰𞵸󠅛󠅃󠄑󠅝󠅛󠅃󠄑󠅝󠇯` | U+1ED70 U+1ED78 U+E015B U+E0143 U+E0111 U+E015D U+E015B U+E0143 U+E0111 U+E015D U+E01EF | always |
| `ae` | `𞵝𞵰𞵝𞵳󠅁󠅅󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED73 U+E0141 U+E0145 U+E01EF | at the start of a word |
| `ae` | `𞵰𞵝𞵳󠅁󠅅󠇯` | U+1ED70 U+1ED5D U+1ED73 U+E0141 U+E0145 U+E01EF | always |
| `aE` | `𞵝𞵰𞵝𞵳󠅁󠄥󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED73 U+E0141 U+E0125 U+E01EF | at the start of a word |
| `aE` | `𞵰𞵝𞵳󠅁󠄥󠇯` | U+1ED70 U+1ED5D U+1ED73 U+E0141 U+E0125 U+E01EF | always |
| `aé` | `𞵝𞵰𞵝𞵳󠅁󠅛󠅅󠄙󠅝󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED73 U+E0141 U+E015B U+E0145 U+E0119 U+E015D U+E01EF | at the start of a word |
| `aé` | `𞵰𞵝𞵳󠅁󠅛󠅅󠄙󠅝󠇯` | U+1ED70 U+1ED5D U+1ED73 U+E0141 U+E015B U+E0145 U+E0119 U+E015D U+E01EF | always |
| `aÉ` | `𞵝𞵰𞵝𞵳󠅁󠅛󠅃󠄙󠅝󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED73 U+E0141 U+E015B U+E0143 U+E0119 U+E015D U+E01EF | at the start of a word |
| `aÉ` | `𞵰𞵝𞵳󠅁󠅛󠅃󠄙󠅝󠇯` | U+1ED70 U+1ED5D U+1ED73 U+E0141 U+E015B U+E0143 U+E0119 U+E015D U+E01EF | always |
| `Ae` | `𞵝𞵰𞵝𞵳󠄡󠅅󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED73 U+E0121 U+E0145 U+E01EF | at the start of a word |
| `Ae` | `𞵰𞵝𞵳󠄡󠅅󠇯` | U+1ED70 U+1ED5D U+1ED73 U+E0121 U+E0145 U+E01EF | always |
| `AE` | `𞵝𞵰𞵝𞵳󠄡󠄥󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED73 U+E0121 U+E0125 U+E01EF | at the start of a word |
| `AE` | `𞵰𞵝𞵳󠄡󠄥󠇯` | U+1ED70 U+1ED5D U+1ED73 U+E0121 U+E0125 U+E01EF | always |
| `Aé` | `𞵝𞵰𞵝𞵳󠄡󠅛󠅅󠄙󠅝󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED73 U+E0121 U+E015B U+E0145 U+E0119 U+E015D U+E01EF | at the start of a word |
| `Aé` | `𞵰𞵝𞵳󠄡󠅛󠅅󠄙󠅝󠇯` | U+1ED70 U+1ED5D U+1ED73 U+E0121 U+E015B U+E0145 U+E0119 U+E015D U+E01EF | always |
| `AÉ` | `𞵝𞵰𞵝𞵳󠄡󠅛󠅃󠄙󠅝󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED73 U+E0121 U+E015B U+E0143 U+E0119 U+E015D U+E01EF | at the start of a word |
| `AÉ` | `𞵰𞵝𞵳󠄡󠅛󠅃󠄙󠅝󠇯` | U+1ED70 U+1ED5D U+1ED73 U+E0121 U+E015B U+E0143 U+E0119 U+E015D U+E01EF | always |
| `áe` | `𞵝𞵰𞵝𞵳󠅛󠅅󠄑󠅝󠅅󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED73 U+E015B U+E0145 U+E0111 U+E015D U+E0145 U+E01EF | at the start of a word |
| `áe` | `𞵰𞵝𞵳󠅛󠅅󠄑󠅝󠅅󠇯` | U+1ED70 U+1ED5D U+1ED73 U+E015B U+E0145 U+E0111 U+E015D U+E0145 U+E01EF | always |
| `áE` | `𞵝𞵰𞵝𞵳󠅛󠅅󠄑󠅝󠄥󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED73 U+E015B U+E0145 U+E0111 U+E015D U+E0125 U+E01EF | at the start of a word |
| `áE` | `𞵰𞵝𞵳󠅛󠅅󠄑󠅝󠄥󠇯` | U+1ED70 U+1ED5D U+1ED73 U+E015B U+E0145 U+E0111 U+E015D U+E0125 U+E01EF | always |
| `áé` | `𞵝𞵰𞵝𞵳󠅛󠅅󠄑󠅝󠅛󠅅󠄙󠅝󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED73 U+E015B U+E0145 U+E0111 U+E015D U+E015B U+E0145 U+E0119 U+E015D U+E01EF | at the start of a word |
| `áé` | `𞵰𞵝𞵳󠅛󠅅󠄑󠅝󠅛󠅅󠄙󠅝󠇯` | U+1ED70 U+1ED5D U+1ED73 U+E015B U+E0145 U+E0111 U+E015D U+E015B U+E0145 U+E0119 U+E015D U+E01EF | always |
| `áÉ` | `𞵝𞵰𞵝𞵳󠅛󠅅󠄑󠅝󠅛󠅃󠄙󠅝󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED73 U+E015B U+E0145 U+E0111 U+E015D U+E015B U+E0143 U+E0119 U+E015D U+E01EF | at the start of a word |
| `áÉ` | `𞵰𞵝𞵳󠅛󠅅󠄑󠅝󠅛󠅃󠄙󠅝󠇯` | U+1ED70 U+1ED5D U+1ED73 U+E015B U+E0145 U+E0111 U+E015D U+E015B U+E0143 U+E0119 U+E015D U+E01EF | always |
| `Áe` | `𞵝𞵰𞵝𞵳󠅛󠅃󠄑󠅝󠅅󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED73 U+E015B U+E0143 U+E0111 U+E015D U+E0145 U+E01EF | at the start of a word |
| `Áe` | `𞵰𞵝𞵳󠅛󠅃󠄑󠅝󠅅󠇯` | U+1ED70 U+1ED5D U+1ED73 U+E015B U+E0143 U+E0111 U+E015D U+E0145 U+E01EF | always |
| `ÁE` | `𞵝𞵰𞵝𞵳󠅛󠅃󠄑󠅝󠄥󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED73 U+E015B U+E0143 U+E0111 U+E015D U+E0125 U+E01EF | at the start of a word |
| `ÁE` | `𞵰𞵝𞵳󠅛󠅃󠄑󠅝󠄥󠇯` | U+1ED70 U+1ED5D U+1ED73 U+E015B U+E0143 U+E0111 U+E015D U+E0125 U+E01EF | always |
| `Áé` | `𞵝𞵰𞵝𞵳󠅛󠅃󠄑󠅝󠅛󠅅󠄙󠅝󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED73 U+E015B U+E0143 U+E0111 U+E015D U+E015B U+E0145 U+E0119 U+E015D U+E01EF | at the start of a word |
| `Áé` | `𞵰𞵝𞵳󠅛󠅃󠄑󠅝󠅛󠅅󠄙󠅝󠇯` | U+1ED70 U+1ED5D U+1ED73 U+E015B U+E0143 U+E0111 U+E015D U+E015B U+E0145 U+E0119 U+E015D U+E01EF | always |
| `ÁÉ` | `𞵝𞵰𞵝𞵳󠅛󠅃󠄑󠅝󠅛󠅃󠄙󠅝󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED73 U+E015B U+E0143 U+E0111 U+E015D U+E015B U+E0143 U+E0119 U+E015D U+E01EF | at the start of a word |
| `ÁÉ` | `𞵰𞵝𞵳󠅛󠅃󠄑󠅝󠅛󠅃󠄙󠅝󠇯` | U+1ED70 U+1ED5D U+1ED73 U+E015B U+E0143 U+E0111 U+E015D U+E015B U+E0143 U+E0119 U+E015D U+E01EF | always |
| `ao` | `𞵝𞵰𞵝𞵱󠅁󠅏󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED71 U+E0141 U+E014F U+E01EF | at the start of a word |
| `ao` | `𞵰𞵝𞵱󠅁󠅏󠇯` | U+1ED70 U+1ED5D U+1ED71 U+E0141 U+E014F U+E01EF | always |
| `aO` | `𞵝𞵰𞵝𞵱󠅁󠄯󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED71 U+E0141 U+E012F U+E01EF | at the start of a word |
| `aO` | `𞵰𞵝𞵱󠅁󠄯󠇯` | U+1ED70 U+1ED5D U+1ED71 U+E0141 U+E012F U+E01EF | always |
| `aó` | `𞵝𞵰𞵝𞵱󠅁󠅛󠅆󠄓󠅝󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED71 U+E0141 U+E015B U+E0146 U+E0113 U+E015D U+E01EF | at the start of a word |
| `aó` | `𞵰𞵝𞵱󠅁󠅛󠅆󠄓󠅝󠇯` | U+1ED70 U+1ED5D U+1ED71 U+E0141 U+E015B U+E0146 U+E0113 U+E015D U+E01EF | always |
| `aÓ` | `𞵝𞵰𞵝𞵱󠅁󠅛󠅄󠄓󠅝󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED71 U+E0141 U+E015B U+E0144 U+E0113 U+E015D U+E01EF | at the start of a word |
| `aÓ` | `𞵰𞵝𞵱󠅁󠅛󠅄󠄓󠅝󠇯` | U+1ED70 U+1ED5D U+1ED71 U+E0141 U+E015B U+E0144 U+E0113 U+E015D U+E01EF | always |
| `Ao` | `𞵝𞵰𞵝𞵱󠄡󠅏󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED71 U+E0121 U+E014F U+E01EF | at the start of a word |
| `Ao` | `𞵰𞵝𞵱󠄡󠅏󠇯` | U+1ED70 U+1ED5D U+1ED71 U+E0121 U+E014F U+E01EF | always |
| `AO` | `𞵝𞵰𞵝𞵱󠄡󠄯󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED71 U+E0121 U+E012F U+E01EF | at the start of a word |
| `AO` | `𞵰𞵝𞵱󠄡󠄯󠇯` | U+1ED70 U+1ED5D U+1ED71 U+E0121 U+E012F U+E01EF | always |
| `Aó` | `𞵝𞵰𞵝𞵱󠄡󠅛󠅆󠄓󠅝󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED71 U+E0121 U+E015B U+E0146 U+E0113 U+E015D U+E01EF | at the start of a word |
| `Aó` | `𞵰𞵝𞵱󠄡󠅛󠅆󠄓󠅝󠇯` | U+1ED70 U+1ED5D U+1ED71 U+E0121 U+E015B U+E0146 U+E0113 U+E015D U+E01EF | always |
| `AÓ` | `𞵝𞵰𞵝𞵱󠄡󠅛󠅄󠄓󠅝󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED71 U+E0121 U+E015B U+E0144 U+E0113 U+E015D U+E01EF | at the start of a word |
| `AÓ` | `𞵰𞵝𞵱󠄡󠅛󠅄󠄓󠅝󠇯` | U+1ED70 U+1ED5D U+1ED71 U+E0121 U+E015B U+E0144 U+E0113 U+E015D U+E01EF | always |
| `áo` | `𞵝𞵰𞵝𞵱󠅛󠅅󠄑󠅝󠅏󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED71 U+E015B U+E0145 U+E0111 U+E015D U+E014F U+E01EF | at the start of a word |
| `áo` | `𞵰𞵝𞵱󠅛󠅅󠄑󠅝󠅏󠇯` | U+1ED70 U+1ED5D U+1ED71 U+E015B U+E0145 U+E0111 U+E015D U+E014F U+E01EF | always |
| `áO` | `𞵝𞵰𞵝𞵱󠅛󠅅󠄑󠅝󠄯󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED71 U+E015B U+E0145 U+E0111 U+E015D U+E012F U+E01EF | at the start of a word |
| `áO` | `𞵰𞵝𞵱󠅛󠅅󠄑󠅝󠄯󠇯` | U+1ED70 U+1ED5D U+1ED71 U+E015B U+E0145 U+E0111 U+E015D U+E012F U+E01EF | always |
| `áó` | `𞵝𞵰𞵝𞵱󠅛󠅅󠄑󠅝󠅛󠅆󠄓󠅝󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED71 U+E015B U+E0145 U+E0111 U+E015D U+E015B U+E0146 U+E0113 U+E015D U+E01EF | at the start of a word |
| `áó` | `𞵰𞵝𞵱󠅛󠅅󠄑󠅝󠅛󠅆󠄓󠅝󠇯` | U+1ED70 U+1ED5D U+1ED71 U+E015B U+E0145 U+E0111 U+E015D U+E015B U+E0146 U+E0113 U+E015D U+E01EF | always |
| `áÓ` | `𞵝𞵰𞵝𞵱󠅛󠅅󠄑󠅝󠅛󠅄󠄓󠅝󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED71 U+E015B U+E0145 U+E0111 U+E015D U+E015B U+E0144 U+E0113 U+E015D U+E01EF | at the start of a word |
| `áÓ` | `𞵰𞵝𞵱󠅛󠅅󠄑󠅝󠅛󠅄󠄓󠅝󠇯` | U+1ED70 U+1ED5D U+1ED71 U+E015B U+E0145 U+E0111 U+E015D U+E015B U+E0144 U+E0113 U+E015D U+E01EF | always |
| `Áo` | `𞵝𞵰𞵝𞵱󠅛󠅃󠄑󠅝󠅏󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED71 U+E015B U+E0143 U+E0111 U+E015D U+E014F U+E01EF | at the start of a word |
| `Áo` | `𞵰𞵝𞵱󠅛󠅃󠄑󠅝󠅏󠇯` | U+1ED70 U+1ED5D U+1ED71 U+E015B U+E0143 U+E0111 U+E015D U+E014F U+E01EF | always |
| `ÁO` | `𞵝𞵰𞵝𞵱󠅛󠅃󠄑󠅝󠄯󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED71 U+E015B U+E0143 U+E0111 U+E015D U+E012F U+E01EF | at the start of a word |
| `ÁO` | `𞵰𞵝𞵱󠅛󠅃󠄑󠅝󠄯󠇯` | U+1ED70 U+1ED5D U+1ED71 U+E015B U+E0143 U+E0111 U+E015D U+E012F U+E01EF | always |
| `Áó` | `𞵝𞵰𞵝𞵱󠅛󠅃󠄑󠅝󠅛󠅆󠄓󠅝󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED71 U+E015B U+E0143 U+E0111 U+E015D U+E015B U+E0146 U+E0113 U+E015D U+E01EF | at the start of a word |
| `Áó` | `𞵰𞵝𞵱󠅛󠅃󠄑󠅝󠅛󠅆󠄓󠅝󠇯` | U+1ED70 U+1ED5D U+1ED71 U+E015B U+E0143 U+E0111 U+E015D U+E015B U+E0146 U+E0113 U+E015D U+E01EF | always |
| `ÁÓ` | `𞵝𞵰𞵝𞵱󠅛󠅃󠄑󠅝󠅛󠅄󠄓󠅝󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED71 U+E015B U+E0143 U+E0111 U+E015D U+E015B U+E0144 U+E0113 U+E015D U+E01EF | at the start of a word |
| `ÁÓ` | `𞵰𞵝𞵱󠅛󠅃󠄑󠅝󠅛󠅄󠄓󠅝󠇯` | U+1ED70 U+1ED5D U+1ED71 U+E015B U+E0143 U+E0111 U+E015D U+E015B U+E0144 U+E0113 U+E015D U+E01EF | always |
| `ay` | `𞵝𞵰𞵝𞵵󠅁󠅙󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED75 U+E0141 U+E0159 U+E01EF | at the start of a word |
| `ay` | `𞵰𞵝𞵵󠅁󠅙󠇯` | U+1ED70 U+1ED5D U+1ED75 U+E0141 U+E0159 U+E01EF | always |
| `aY` | `𞵝𞵰𞵝𞵵󠅁󠄹󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED75 U+E0141 U+E0139 U+E01EF | at the start of a word |
| `aY` | `𞵰𞵝𞵵󠅁󠄹󠇯` | U+1ED70 U+1ED5D U+1ED75 U+E0141 U+E0139 U+E01EF | always |
| `aý` | `𞵝𞵰𞵝𞵵󠅁󠅛󠅆󠅄󠅝󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED75 U+E0141 U+E015B U+E0146 U+E0144 U+E015D U+E01EF | at the start of a word |
| `aý` | `𞵰𞵝𞵵󠅁󠅛󠅆󠅄󠅝󠇯` | U+1ED70 U+1ED5D U+1ED75 U+E0141 U+E015B U+E0146 U+E0144 U+E015D U+E01EF | always |
| `aÝ` | `𞵝𞵰𞵝𞵵󠅁󠅛󠅄󠅄󠅝󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED75 U+E0141 U+E015B U+E0144 U+E0144 U+E015D U+E01EF | at the start of a word |
| `aÝ` | `𞵰𞵝𞵵󠅁󠅛󠅄󠅄󠅝󠇯` | U+1ED70 U+1ED5D U+1ED75 U+E0141 U+E015B U+E0144 U+E0144 U+E015D U+E01EF | always |
| `Ay` | `𞵝𞵰𞵝𞵵󠄡󠅙󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED75 U+E0121 U+E0159 U+E01EF | at the start of a word |
| `Ay` | `𞵰𞵝𞵵󠄡󠅙󠇯` | U+1ED70 U+1ED5D U+1ED75 U+E0121 U+E0159 U+E01EF | always |
| `AY` | `𞵝𞵰𞵝𞵵󠄡󠄹󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED75 U+E0121 U+E0139 U+E01EF | at the start of a word |
| `AY` | `𞵰𞵝𞵵󠄡󠄹󠇯` | U+1ED70 U+1ED5D U+1ED75 U+E0121 U+E0139 U+E01EF | always |
| `Aý` | `𞵝𞵰𞵝𞵵󠄡󠅛󠅆󠅄󠅝󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED75 U+E0121 U+E015B U+E0146 U+E0144 U+E015D U+E01EF | at the start of a word |
| `Aý` | `𞵰𞵝𞵵󠄡󠅛󠅆󠅄󠅝󠇯` | U+1ED70 U+1ED5D U+1ED75 U+E0121 U+E015B U+E0146 U+E0144 U+E015D U+E01EF | always |
| `AÝ` | `𞵝𞵰𞵝𞵵󠄡󠅛󠅄󠅄󠅝󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED75 U+E0121 U+E015B U+E0144 U+E0144 U+E015D U+E01EF | at the start of a word |
| `AÝ` | `𞵰𞵝𞵵󠄡󠅛󠅄󠅄󠅝󠇯` | U+1ED70 U+1ED5D U+1ED75 U+E0121 U+E015B U+E0144 U+E0144 U+E015D U+E01EF | always |
| `áy` | `𞵝𞵰𞵝𞵵󠅛󠅅󠄑󠅝󠅙󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED75 U+E015B U+E0145 U+E0111 U+E015D U+E0159 U+E01EF | at the start of a word |
| `áy` | `𞵰𞵝𞵵󠅛󠅅󠄑󠅝󠅙󠇯` | U+1ED70 U+1ED5D U+1ED75 U+E015B U+E0145 U+E0111 U+E015D U+E0159 U+E01EF | always |
| `áY` | `𞵝𞵰𞵝𞵵󠅛󠅅󠄑󠅝󠄹󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED75 U+E015B U+E0145 U+E0111 U+E015D U+E0139 U+E01EF | at the start of a word |
| `áY` | `𞵰𞵝𞵵󠅛󠅅󠄑󠅝󠄹󠇯` | U+1ED70 U+1ED5D U+1ED75 U+E015B U+E0145 U+E0111 U+E015D U+E0139 U+E01EF | always |
| `áý` | `𞵝𞵰𞵝𞵵󠅛󠅅󠄑󠅝󠅛󠅆󠅄󠅝󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED75 U+E015B U+E0145 U+E0111 U+E015D U+E015B U+E0146 U+E0144 U+E015D U+E01EF | at the start of a word |
| `áý` | `𞵰𞵝𞵵󠅛󠅅󠄑󠅝󠅛󠅆󠅄󠅝󠇯` | U+1ED70 U+1ED5D U+1ED75 U+E015B U+E0145 U+E0111 U+E015D U+E015B U+E0146 U+E0144 U+E015D U+E01EF | always |
| `áÝ` | `𞵝𞵰𞵝𞵵󠅛󠅅󠄑󠅝󠅛󠅄󠅄󠅝󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED75 U+E015B U+E0145 U+E0111 U+E015D U+E015B U+E0144 U+E0144 U+E015D U+E01EF | at the start of a word |
| `áÝ` | `𞵰𞵝𞵵󠅛󠅅󠄑󠅝󠅛󠅄󠅄󠅝󠇯` | U+1ED70 U+1ED5D U+1ED75 U+E015B U+E0145 U+E0111 U+E015D U+E015B U+E0144 U+E0144 U+E015D U+E01EF | always |
| `Áy` | `𞵝𞵰𞵝𞵵󠅛󠅃󠄑󠅝󠅙󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED75 U+E015B U+E0143 U+E0111 U+E015D U+E0159 U+E01EF | at the start of a word |
| `Áy` | `𞵰𞵝𞵵󠅛󠅃󠄑󠅝󠅙󠇯` | U+1ED70 U+1ED5D U+1ED75 U+E015B U+E0143 U+E0111 U+E015D U+E0159 U+E01EF | always |
| `ÁY` | `𞵝𞵰𞵝𞵵󠅛󠅃󠄑󠅝󠄹󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED75 U+E015B U+E0143 U+E0111 U+E015D U+E0139 U+E01EF | at the start of a word |
| `ÁY` | `𞵰𞵝𞵵󠅛󠅃󠄑󠅝󠄹󠇯` | U+1ED70 U+1ED5D U+1ED75 U+E015B U+E0143 U+E0111 U+E015D U+E0139 U+E01EF | always |
| `Áý` | `𞵝𞵰𞵝𞵵󠅛󠅃󠄑󠅝󠅛󠅆󠅄󠅝󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED75 U+E015B U+E0143 U+E0111 U+E015D U+E015B U+E0146 U+E0144 U+E015D U+E01EF | at the start of a word |
| `Áý` | `𞵰𞵝𞵵󠅛󠅃󠄑󠅝󠅛󠅆󠅄󠅝󠇯` | U+1ED70 U+1ED5D U+1ED75 U+E015B U+E0143 U+E0111 U+E015D U+E015B U+E0146 U+E0144 U+E015D U+E01EF | always |
| `ÁÝ` | `𞵝𞵰𞵝𞵵󠅛󠅃󠄑󠅝󠅛󠅄󠅄󠅝󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED75 U+E015B U+E0143 U+E0111 U+E015D U+E015B U+E0144 U+E0144 U+E015D U+E01EF | at the start of a word |
| `ÁÝ` | `𞵰𞵝𞵵󠅛󠅃󠄑󠅝󠅛󠅄󠅄󠅝󠇯` | U+1ED70 U+1ED5D U+1ED75 U+E015B U+E0143 U+E0111 U+E015D U+E015B U+E0144 U+E0144 U+E015D U+E01EF | always |
| `aë` | `𞵝𞵰𞵝𞵶󠅁󠅛󠅅󠅂󠅝󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED76 U+E0141 U+E015B U+E0145 U+E0142 U+E015D U+E01EF | at the start of a word |
| `aë` | `𞵰𞵝𞵶󠅁󠅛󠅅󠅂󠅝󠇯` | U+1ED70 U+1ED5D U+1ED76 U+E0141 U+E015B U+E0145 U+E0142 U+E015D U+E01EF | always |
| `aË` | `𞵝𞵰𞵝𞵶󠅁󠅛󠅃󠅂󠅝󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED76 U+E0141 U+E015B U+E0143 U+E0142 U+E015D U+E01EF | at the start of a word |
| `aË` | `𞵰𞵝𞵶󠅁󠅛󠅃󠅂󠅝󠇯` | U+1ED70 U+1ED5D U+1ED76 U+E0141 U+E015B U+E0143 U+E0142 U+E015D U+E01EF | always |
| `Aë` | `𞵝𞵰𞵝𞵶󠄡󠅛󠅅󠅂󠅝󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED76 U+E0121 U+E015B U+E0145 U+E0142 U+E015D U+E01EF | at the start of a word |
| `Aë` | `𞵰𞵝𞵶󠄡󠅛󠅅󠅂󠅝󠇯` | U+1ED70 U+1ED5D U+1ED76 U+E0121 U+E015B U+E0145 U+E0142 U+E015D U+E01EF | always |
| `AË` | `𞵝𞵰𞵝𞵶󠄡󠅛󠅃󠅂󠅝󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED76 U+E0121 U+E015B U+E0143 U+E0142 U+E015D U+E01EF | at the start of a word |
| `AË` | `𞵰𞵝𞵶󠄡󠅛󠅃󠅂󠅝󠇯` | U+1ED70 U+1ED5D U+1ED76 U+E0121 U+E015B U+E0143 U+E0142 U+E015D U+E01EF | always |
| `áë` | `𞵝𞵰𞵝𞵶󠅛󠅅󠄑󠅝󠅛󠅅󠅂󠅝󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED76 U+E015B U+E0145 U+E0111 U+E015D U+E015B U+E0145 U+E0142 U+E015D U+E01EF | at the start of a word |
| `áë` | `𞵰𞵝𞵶󠅛󠅅󠄑󠅝󠅛󠅅󠅂󠅝󠇯` | U+1ED70 U+1ED5D U+1ED76 U+E015B U+E0145 U+E0111 U+E015D U+E015B U+E0145 U+E0142 U+E015D U+E01EF | always |
| `áË` | `𞵝𞵰𞵝𞵶󠅛󠅅󠄑󠅝󠅛󠅃󠅂󠅝󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED76 U+E015B U+E0145 U+E0111 U+E015D U+E015B U+E0143 U+E0142 U+E015D U+E01EF | at the start of a word |
| `áË` | `𞵰𞵝𞵶󠅛󠅅󠄑󠅝󠅛󠅃󠅂󠅝󠇯` | U+1ED70 U+1ED5D U+1ED76 U+E015B U+E0145 U+E0111 U+E015D U+E015B U+E0143 U+E0142 U+E015D U+E01EF | always |
| `Áë` | `𞵝𞵰𞵝𞵶󠅛󠅃󠄑󠅝󠅛󠅅󠅂󠅝󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED76 U+E015B U+E0143 U+E0111 U+E015D U+E015B U+E0145 U+E0142 U+E015D U+E01EF | at the start of a word |
| `Áë` | `𞵰𞵝𞵶󠅛󠅃󠄑󠅝󠅛󠅅󠅂󠅝󠇯` | U+1ED70 U+1ED5D U+1ED76 U+E015B U+E0143 U+E0111 U+E015D U+E015B U+E0145 U+E0142 U+E015D U+E01EF | always |
| `ÁË` | `𞵝𞵰𞵝𞵶󠅛󠅃󠄑󠅝󠅛󠅃󠅂󠅝󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED76 U+E015B U+E0143 U+E0111 U+E015D U+E015B U+E0143 U+E0142 U+E015D U+E01EF | at the start of a word |
| `ÁË` | `𞵰𞵝𞵶󠅛󠅃󠄑󠅝󠅛󠅃󠅂󠅝󠇯` | U+1ED70 U+1ED5D U+1ED76 U+E015B U+E0143 U+E0111 U+E015D U+E015B U+E0143 U+E0142 U+E015D U+E01EF | always |
| `ea` | `𞵝𞵳𞵝𞵰󠅅󠅁󠇯` | U+1ED5D U+1ED73 U+1ED5D U+1ED70 U+E0145 U+E0141 U+E01EF | at the start of a word |
| `ea` | `𞵳𞵝𞵰󠅅󠅁󠇯` | U+1ED73 U+1ED5D U+1ED70 U+E0145 U+E0141 U+E01EF | always |
| `eA` | `𞵝𞵳𞵝𞵰󠅅󠄡󠇯` | U+1ED5D U+1ED73 U+1ED5D U+1ED70 U+E0145 U+E0121 U+E01EF | at the start of a word |
| `eA` | `𞵳𞵝𞵰󠅅󠄡󠇯` | U+1ED73 U+1ED5D U+1ED70 U+E0145 U+E0121 U+E01EF | always |
| `eá` | `𞵝𞵳𞵝𞵰󠅅󠅛󠅅󠄑󠅝󠇯` | U+1ED5D U+1ED73 U+1ED5D U+1ED70 U+E0145 U+E015B U+E0145 U+E0111 U+E015D U+E01EF | at the start of a word |
| `eá` | `𞵳𞵝𞵰󠅅󠅛󠅅󠄑󠅝󠇯` | U+1ED73 U+1ED5D U+1ED70 U+E0145 U+E015B U+E0145 U+E0111 U+E015D U+E01EF | always |
| `eÁ` | `𞵝𞵳𞵝𞵰󠅅󠅛󠅃󠄑󠅝󠇯` | U+1ED5D U+1ED73 U+1ED5D U+1ED70 U+E0145 U+E015B U+E0143 U+E0111 U+E015D U+E01EF | at the start of a word |
| `eÁ` | `𞵳𞵝𞵰󠅅󠅛󠅃󠄑󠅝󠇯` | U+1ED73 U+1ED5D U+1ED70 U+E0145 U+E015B U+E0143 U+E0111 U+E015D U+E01EF | always |
| `Ea` | `𞵝𞵳𞵝𞵰󠄥󠅁󠇯` | U+1ED5D U+1ED73 U+1ED5D U+1ED70 U+E0125 U+E0141 U+E01EF | at the start of a word |
| `Ea` | `𞵳𞵝𞵰󠄥󠅁󠇯` | U+1ED73 U+1ED5D U+1ED70 U+E0125 U+E0141 U+E01EF | always |
| `EA` | `𞵝𞵳𞵝𞵰󠄥󠄡󠇯` | U+1ED5D U+1ED73 U+1ED5D U+1ED70 U+E0125 U+E0121 U+E01EF | at the start of a word |
| `EA` | `𞵳𞵝𞵰󠄥󠄡󠇯` | U+1ED73 U+1ED5D U+1ED70 U+E0125 U+E0121 U+E01EF | always |
| `Eá` | `𞵝𞵳𞵝𞵰󠄥󠅛󠅅󠄑󠅝󠇯` | U+1ED5D U+1ED73 U+1ED5D U+1ED70 U+E0125 U+E015B U+E0145 U+E0111 U+E015D U+E01EF | at the start of a word |
| `Eá` | `𞵳𞵝𞵰󠄥󠅛󠅅󠄑󠅝󠇯` | U+1ED73 U+1ED5D U+1ED70 U+E0125 U+E015B U+E0145 U+E0111 U+E015D U+E01EF | always |
| `EÁ` | `𞵝𞵳𞵝𞵰󠄥󠅛󠅃󠄑󠅝󠇯` | U+1ED5D U+1ED73 U+1ED5D U+1ED70 U+E0125 U+E015B U+E0143 U+E0111 U+E015D U+E01EF | at the start of a word |
| `EÁ` | `𞵳𞵝𞵰󠄥󠅛󠅃󠄑󠅝󠇯` | U+1ED73 U+1ED5D U+1ED70 U+E0125 U+E015B U+E0143 U+E0111 U+E015D U+E01EF | always |
| `éa` | `𞵝𞵳𞵝𞵰󠅛󠅅󠄙󠅝󠅁󠇯` | U+1ED5D U+1ED73 U+1ED5D U+1ED70 U+E015B U+E0145 U+E0119 U+E015D U+E0141 U+E01EF | at the start of a word |
| `éa` | `𞵳𞵝𞵰󠅛󠅅󠄙󠅝󠅁󠇯` | U+1ED73 U+1ED5D U+1ED70 U+E015B U+E0145 U+E0119 U+E015D U+E0141 U+E01EF | always |
| `éA` | `𞵝𞵳𞵝𞵰󠅛󠅅󠄙󠅝󠄡󠇯` | U+1ED5D U+1ED73 U+1ED5D U+1ED70 U+E015B U+E0145 U+E0119 U+E015D U+E0121 U+E01EF | at the start of a word |
| `éA` | `𞵳𞵝𞵰󠅛󠅅󠄙󠅝󠄡󠇯` | U+1ED73 U+1ED5D U+1ED70 U+E015B U+E0145 U+E0119 U+E015D U+E0121 U+E01EF | always |
| `éá` | `𞵝𞵳𞵝𞵰󠅛󠅅󠄙󠅝󠅛󠅅󠄑󠅝󠇯` | U+1ED5D U+1ED73 U+1ED5D U+1ED70 U+E015B U+E0145 U+E0119 U+E015D U+E015B U+E0145 U+E0111 U+E015D U+E01EF | at the start of a word |
| `éá` | `𞵳𞵝𞵰󠅛󠅅󠄙󠅝󠅛󠅅󠄑󠅝󠇯` | U+1ED73 U+1ED5D U+1ED70 U+E015B U+E0145 U+E0119 U+E015D U+E015B U+E0145 U+E0111 U+E015D U+E01EF | always |
| `éÁ` | `𞵝𞵳𞵝𞵰󠅛󠅅󠄙󠅝󠅛󠅃󠄑󠅝󠇯` | U+1ED5D U+1ED73 U+1ED5D U+1ED70 U+E015B U+E0145 U+E0119 U+E015D U+E015B U+E0143 U+E0111 U+E015D U+E01EF | at the start of a word |
| `éÁ` | `𞵳𞵝𞵰󠅛󠅅󠄙󠅝󠅛󠅃󠄑󠅝󠇯` | U+1ED73 U+1ED5D U+1ED70 U+E015B U+E0145 U+E0119 U+E015D U+E015B U+E0143 U+E0111 U+E015D U+E01EF | always |
| `Éa` | `𞵝𞵳𞵝𞵰󠅛󠅃󠄙󠅝󠅁󠇯` | U+1ED5D U+1ED73 U+1ED5D U+1ED70 U+E015B U+E0143 U+E0119 U+E015D U+E0141 U+E01EF | at the start of a word |
| `Éa` | `𞵳𞵝𞵰󠅛󠅃󠄙󠅝󠅁󠇯` | U+1ED73 U+1ED5D U+1ED70 U+E015B U+E0143 U+E0119 U+E015D U+E0141 U+E01EF | always |
| `ÉA` | `𞵝𞵳𞵝𞵰󠅛󠅃󠄙󠅝󠄡󠇯` | U+1ED5D U+1ED73 U+1ED5D U+1ED70 U+E015B U+E0143 U+E0119 U+E015D U+E0121 U+E01EF | at the start of a word |
| `ÉA` | `𞵳𞵝𞵰󠅛󠅃󠄙󠅝󠄡󠇯` | U+1ED73 U+1ED5D U+1ED70 U+E015B U+E0143 U+E0119 U+E015D U+E0121 U+E01EF | always |
| `Éá` | `𞵝𞵳𞵝𞵰󠅛󠅃󠄙󠅝󠅛󠅅󠄑󠅝󠇯` | U+1ED5D U+1ED73 U+1ED5D U+1ED70 U+E015B U+E0143 U+E0119 U+E015D U+E015B U+E0145 U+E0111 U+E015D U+E01EF | at the start of a word |
| `Éá` | `𞵳𞵝𞵰󠅛󠅃󠄙󠅝󠅛󠅅󠄑󠅝󠇯` | U+1ED73 U+1ED5D U+1ED70 U+E015B U+E0143 U+E0119 U+E015D U+E015B U+E0145 U+E0111 U+E015D U+E01EF | always |
| `ÉÁ` | `𞵝𞵳𞵝𞵰󠅛󠅃󠄙󠅝󠅛󠅃󠄑󠅝󠇯` | U+1ED5D U+1ED73 U+1ED5D U+1ED70 U+E015B U+E0143 U+E0119 U+E015D U+E015B U+E0143 U+E0111 U+E015D U+E01EF | at the start of a word |
| `ÉÁ` | `𞵳𞵝𞵰󠅛󠅃󠄙󠅝󠅛󠅃󠄑󠅝󠇯` | U+1ED73 U+1ED5D U+1ED70 U+E015B U+E0143 U+E0119 U+E015D U+E015B U+E0143 U+E0111 U+E015D U+E01EF | always |
| `ee` | `𞵝𞵳𞵸` | U+1ED5D U+1ED73 U+1ED78 | at the start of a word |
| `ee` | `𞵳𞵸` | U+1ED73 U+1ED78 | always |
| `eE` | `𞵝𞵳𞵸󠅅󠄥󠇯` | U+1ED5D U+1ED73 U+1ED78 U+E0145 U+E0125 U+E01EF | at the start of a word |
| `eE` | `𞵳𞵸󠅅󠄥󠇯` | U+1ED73 U+1ED78 U+E0145 U+E0125 U+E01EF | always |
| `eé` | `𞵝𞵳𞵸󠅅󠅛󠅅󠄙󠅝󠇯` | U+1ED5D U+1ED73 U+1ED78 U+E0145 U+E015B U+E0145 U+E0119 U+E015D U+E01EF | at the start of a word |
| `eé` | `𞵳𞵸󠅅󠅛󠅅󠄙󠅝󠇯` | U+1ED73 U+1ED78 U+E0145 U+E015B U+E0145 U+E0119 U+E015D U+E01EF | always |
| `eÉ` | `𞵝𞵳𞵸󠅅󠅛󠅃󠄙󠅝󠇯` | U+1ED5D U+1ED73 U+1ED78 U+E0145 U+E015B U+E0143 U+E0119 U+E015D U+E01EF | at the start of a word |
| `eÉ` | `𞵳𞵸󠅅󠅛󠅃󠄙󠅝󠇯` | U+1ED73 U+1ED78 U+E0145 U+E015B U+E0143 U+E0119 U+E015D U+E01EF | always |
| `Ee` | `𞵝𞵳𞵸󠄥󠅅󠇯` | U+1ED5D U+1ED73 U+1ED78 U+E0125 U+E0145 U+E01EF | at the start of a word |
| `Ee` | `𞵳𞵸󠄥󠅅󠇯` | U+1ED73 U+1ED78 U+E0125 U+E0145 U+E01EF | always |
| `EE` | `𞵝𞵳𞵸󠄥󠄥󠇯` | U+1ED5D U+1ED73 U+1ED78 U+E0125 U+E0125 U+E01EF | at the start of a word |
| `EE` | `𞵳𞵸󠄥󠄥󠇯` | U+1ED73 U+1ED78 U+E0125 U+E0125 U+E01EF | always |
| `Eé` | `𞵝𞵳𞵸󠄥󠅛󠅅󠄙󠅝󠇯` | U+1ED5D U+1ED73 U+1ED78 U+E0125 U+E015B U+E0145 U+E0119 U+E015D U+E01EF | at the start of a word |
| `Eé` | `𞵳𞵸󠄥󠅛󠅅󠄙󠅝󠇯` | U+1ED73 U+1ED78 U+E0125 U+E015B U+E0145 U+E0119 U+E015D U+E01EF | always |
| `EÉ` | `𞵝𞵳𞵸󠄥󠅛󠅃󠄙󠅝󠇯` | U+1ED5D U+1ED73 U+1ED78 U+E0125 U+E015B U+E0143 U+E0119 U+E015D U+E01EF | at the start of a word |
| `EÉ` | `𞵳𞵸󠄥󠅛󠅃󠄙󠅝󠇯` | U+1ED73 U+1ED78 U+E0125 U+E015B U+E0143 U+E0119 U+E015D U+E01EF | always |
| `ée` | `𞵝𞵳𞵸󠅛󠅅󠄙󠅝󠅅󠇯` | U+1ED5D U+1ED73 U+1ED78 U+E015B U+E0145 U+E0119 U+E015D U+E0145 U+E01EF | at the start of a word |
| `ée` | `𞵳𞵸󠅛󠅅󠄙󠅝󠅅󠇯` | U+1ED73 U+1ED78 U+E015B U+E0145 U+E0119 U+E015D U+E0145 U+E01EF | always |
| `éE` | `𞵝𞵳𞵸󠅛󠅅󠄙󠅝󠄥󠇯` | U+1ED5D U+1ED73 U+1ED78 U+E015B U+E0145 U+E0119 U+E015D U+E0125 U+E01EF | at the start of a word |
| `éE` | `𞵳𞵸󠅛󠅅󠄙󠅝󠄥󠇯` | U+1ED73 U+1ED78 U+E015B U+E0145 U+E0119 U+E015D U+E0125 U+E01EF | always |
| `éé` | `𞵝𞵳𞵸󠅛󠅅󠄙󠅝󠅛󠅅󠄙󠅝󠇯` | U+1ED5D U+1ED73 U+1ED78 U+E015B U+E0145 U+E0119 U+E015D U+E015B U+E0145 U+E0119 U+E015D U+E01EF | at the start of a word |
| `éé` | `𞵳𞵸󠅛󠅅󠄙󠅝󠅛󠅅󠄙󠅝󠇯` | U+1ED73 U+1ED78 U+E015B U+E0145 U+E0119 U+E015D U+E015B U+E0145 U+E0119 U+E015D U+E01EF | always |
| `éÉ` | `𞵝𞵳𞵸󠅛󠅅󠄙󠅝󠅛󠅃󠄙󠅝󠇯` | U+1ED5D U+1ED73 U+1ED78 U+E015B U+E0145 U+E0119 U+E015D U+E015B U+E0143 U+E0119 U+E015D U+E01EF | at the start of a word |
| `éÉ` | `𞵳𞵸󠅛󠅅󠄙󠅝󠅛󠅃󠄙󠅝󠇯` | U+1ED73 U+1ED78 U+E015B U+E0145 U+E0119 U+E015D U+E015B U+E0143 U+E0119 U+E015D U+E01EF | always |
| `Ée` | `𞵝𞵳𞵸󠅛󠅃󠄙󠅝󠅅󠇯` | U+1ED5D U+1ED73 U+1ED78 U+E015B U+E0143 U+E0119 U+E015D U+E0145 U+E01EF | at the start of a word |
| `Ée` | `𞵳𞵸󠅛󠅃󠄙󠅝󠅅󠇯` | U+1ED73 U+1ED78 U+E015B U+E0143 U+E0119 U+E015D U+E0145 U+E01EF | always |
| `ÉE` | `𞵝𞵳𞵸󠅛󠅃󠄙󠅝󠄥󠇯` | U+1ED5D U+1ED73 U+1ED78 U+E015B U+E0143 U+E0119 U+E015D U+E0125 U+E01EF | at the start of a word |
| `ÉE` | `𞵳𞵸󠅛󠅃󠄙󠅝󠄥󠇯` | U+1ED73 U+1ED78 U+E015B U+E0143 U+E0119 U+E015D U+E0125 U+E01EF | always |
| `Éé` | `𞵝𞵳𞵸󠅛󠅃󠄙󠅝󠅛󠅅󠄙󠅝󠇯` | U+1ED5D U+1ED73 U+1ED78 U+E015B U+E0143 U+E0119 U+E015D U+E015B U+E0145 U+E0119 U+E015D U+E01EF | at the start of a word |
| `Éé` | `𞵳𞵸󠅛󠅃󠄙󠅝󠅛󠅅󠄙󠅝󠇯` | U+1ED73 U+1ED78 U+E015B U+E0143 U+E0119 U+E015D U+E015B U+E0145 U+E0119 U+E015D U+E01EF | always |
| `ÉÉ` | `𞵝𞵳𞵸󠅛󠅃󠄙󠅝󠅛󠅃󠄙󠅝󠇯` | U+1ED5D U+1ED73 U+1ED78 U+E015B U+E0143 U+E0119 U+E015D U+E015B U+E0143 U+E0119 U+E015D U+E01EF | at the start of a word |
| `ÉÉ` | `𞵳𞵸󠅛󠅃󠄙󠅝󠅛󠅃󠄙󠅝󠇯` | U+1ED73 U+1ED78 U+E015B U+E0143 U+E0119 U+E015D U+E015B U+E0143 U+E0119 U+E015D U+E01EF | always |
| `eu` | `𞵝𞵳𞵝𞵲󠅅󠅕󠇯` | U+1ED5D U+1ED73 U+1ED5D U+1ED72 U+E0145 U+E0155 U+E01EF | at the start of a word |
| `eu` | `𞵳𞵝𞵲󠅅󠅕󠇯` | U+1ED73 U+1ED5D U+1ED72 U+E0145 U+E0155 U+E01EF | always |
| `eU` | `𞵝𞵳𞵝𞵲󠅅󠄵󠇯` | U+1ED5D U+1ED73 U+1ED5D U+1ED72 U+E0145 U+E0135 U+E01EF | at the start of a word |
| `eU` | `𞵳𞵝𞵲󠅅󠄵󠇯` | U+1ED73 U+1ED5D U+1ED72 U+E0145 U+E0135 U+E01EF | always |
| `eú` | `𞵝𞵳𞵝𞵲󠅅󠅛󠅆󠅁󠅝󠇯` | U+1ED5D U+1ED73 U+1ED5D U+1ED72 U+E0145 U+E015B U+E0146 U+E0141 U+E015D U+E01EF | at the start of a word |
| `eú` | `𞵳𞵝𞵲󠅅󠅛󠅆󠅁󠅝󠇯` | U+1ED73 U+1ED5D U+1ED72 U+E0145 U+E015B U+E0146 U+E0141 U+E015D U+E01EF | always |
| `eÚ` | `𞵝𞵳𞵝𞵲󠅅󠅛󠅄󠅁󠅝󠇯` | U+1ED5D U+1ED73 U+1ED5D U+1ED72 U+E0145 U+E015B U+E0144 U+E0141 U+E015D U+E01EF | at the start of a word |
| `eÚ` | `𞵳𞵝𞵲󠅅󠅛󠅄󠅁󠅝󠇯` | U+1ED73 U+1ED5D U+1ED72 U+E0145 U+E015B U+E0144 U+E0141 U+E015D U+E01EF | always |
| `Eu` | `𞵝𞵳𞵝𞵲󠄥󠅕󠇯` | U+1ED5D U+1ED73 U+1ED5D U+1ED72 U+E0125 U+E0155 U+E01EF | at the start of a word |
| `Eu` | `𞵳𞵝𞵲󠄥󠅕󠇯` | U+1ED73 U+1ED5D U+1ED72 U+E0125 U+E0155 U+E01EF | always |
| `EU` | `𞵝𞵳𞵝𞵲󠄥󠄵󠇯` | U+1ED5D U+1ED73 U+1ED5D U+1ED72 U+E0125 U+E0135 U+E01EF | at the start of a word |
| `EU` | `𞵳𞵝𞵲󠄥󠄵󠇯` | U+1ED73 U+1ED5D U+1ED72 U+E0125 U+E0135 U+E01EF | always |
| `Eú` | `𞵝𞵳𞵝𞵲󠄥󠅛󠅆󠅁󠅝󠇯` | U+1ED5D U+1ED73 U+1ED5D U+1ED72 U+E0125 U+E015B U+E0146 U+E0141 U+E015D U+E01EF | at the start of a word |
| `Eú` | `𞵳𞵝𞵲󠄥󠅛󠅆󠅁󠅝󠇯` | U+1ED73 U+1ED5D U+1ED72 U+E0125 U+E015B U+E0146 U+E0141 U+E015D U+E01EF | always |
| `EÚ` | `𞵝𞵳𞵝𞵲󠄥󠅛󠅄󠅁󠅝󠇯` | U+1ED5D U+1ED73 U+1ED5D U+1ED72 U+E0125 U+E015B U+E0144 U+E0141 U+E015D U+E01EF | at the start of a word |
| `EÚ` | `𞵳𞵝𞵲󠄥󠅛󠅄󠅁󠅝󠇯` | U+1ED73 U+1ED5D U+1ED72 U+E0125 U+E015B U+E0144 U+E0141 U+E015D U+E01EF | always |
| `éu` | `𞵝𞵳𞵝𞵲󠅛󠅅󠄙󠅝󠅕󠇯` | U+1ED5D U+1ED73 U+1ED5D U+1ED72 U+E015B U+E0145 U+E0119 U+E015D U+E0155 U+E01EF | at the start of a word |
| `éu` | `𞵳𞵝𞵲󠅛󠅅󠄙󠅝󠅕󠇯` | U+1ED73 U+1ED5D U+1ED72 U+E015B U+E0145 U+E0119 U+E015D U+E0155 U+E01EF | always |
| `éU` | `𞵝𞵳𞵝𞵲󠅛󠅅󠄙󠅝󠄵󠇯` | U+1ED5D U+1ED73 U+1ED5D U+1ED72 U+E015B U+E0145 U+E0119 U+E015D U+E0135 U+E01EF | at the start of a word |
| `éU` | `𞵳𞵝𞵲󠅛󠅅󠄙󠅝󠄵󠇯` | U+1ED73 U+1ED5D U+1ED72 U+E015B U+E0145 U+E0119 U+E015D U+E0135 U+E01EF | always |
| `éú` | `𞵝𞵳𞵝𞵲󠅛󠅅󠄙󠅝󠅛󠅆󠅁󠅝󠇯` | U+1ED5D U+1ED73 U+1ED5D U+1ED72 U+E015B U+E0145 U+E0119 U+E015D U+E015B U+E0146 U+E0141 U+E015D U+E01EF | at the start of a word |
| `éú` | `𞵳𞵝𞵲󠅛󠅅󠄙󠅝󠅛󠅆󠅁󠅝󠇯` | U+1ED73 U+1ED5D U+1ED72 U+E015B U+E0145 U+E0119 U+E015D U+E015B U+E0146 U+E0141 U+E015D U+E01EF | always |
| `éÚ` | `𞵝𞵳𞵝𞵲󠅛󠅅󠄙󠅝󠅛󠅄󠅁󠅝󠇯` | U+1ED5D U+1ED73 U+1ED5D U+1ED72 U+E015B U+E0145 U+E0119 U+E015D U+E015B U+E0144 U+E0141 U+E015D U+E01EF | at the start of a word |
| `éÚ` | `𞵳𞵝𞵲󠅛󠅅󠄙󠅝󠅛󠅄󠅁󠅝󠇯` | U+1ED73 U+1ED5D U+1ED72 U+E015B U+E0145 U+E0119 U+E015D U+E015B U+E0144 U+E0141 U+E015D U+E01EF | always |
| `Éu` | `𞵝𞵳𞵝𞵲󠅛󠅃󠄙󠅝󠅕󠇯` | U+1ED5D U+1ED73 U+1ED5D U+1ED72 U+E015B U+E0143 U+E0119 U+E015D U+E0155 U+E01EF | at the start of a word |
| `Éu` | `𞵳𞵝𞵲󠅛󠅃󠄙󠅝󠅕󠇯` | U+1ED73 U+1ED5D U+1ED72 U+E015B U+E0143 U+E0119 U+E015D U+E0155 U+E01EF | always |
| `ÉU` | `𞵝𞵳𞵝𞵲󠅛󠅃󠄙󠅝󠄵󠇯` | U+1ED5D U+1ED73 U+1ED5D U+1ED72 U+E015B U+E0143 U+E0119 U+E015D U+E0135 U+E01EF | at the start of a word |
| `ÉU` | `𞵳𞵝𞵲󠅛󠅃󠄙󠅝󠄵󠇯` | U+1ED73 U+1ED5D U+1ED72 U+E015B U+E0143 U+E0119 U+E015D U+E0135 U+E01EF | always |
| `Éú` | `𞵝𞵳𞵝𞵲󠅛󠅃󠄙󠅝󠅛󠅆󠅁󠅝󠇯` | U+1ED5D U+1ED73 U+1ED5D U+1ED72 U+E015B U+E0143 U+E0119 U+E015D U+E015B U+E0146 U+E0141 U+E015D U+E01EF | at the start of a word |
| `Éú` | `𞵳𞵝𞵲󠅛󠅃󠄙󠅝󠅛󠅆󠅁󠅝󠇯` | U+1ED73 U+1ED5D U+1ED72 U+E015B U+E0143 U+E0119 U+E015D U+E015B U+E0146 U+E0141 U+E015D U+E01EF | always |
| `ÉÚ` | `𞵝𞵳𞵝𞵲󠅛󠅃󠄙󠅝󠅛󠅄󠅁󠅝󠇯` | U+1ED5D U+1ED73 U+1ED5D U+1ED72 U+E015B U+E0143 U+E0119 U+E015D U+E015B U+E0144 U+E0141 U+E015D U+E01EF | at the start of a word |
| `ÉÚ` | `𞵳𞵝𞵲󠅛󠅃󠄙󠅝󠅛󠅄󠅁󠅝󠇯` | U+1ED73 U+1ED5D U+1ED72 U+E015B U+E0143 U+E0119 U+E015D U+E015B U+E0144 U+E0141 U+E015D U+E01EF | always |
| `ey` | `𞵝𞵳𞵝𞵵󠅅󠅙󠇯` | U+1ED5D U+1ED73 U+1ED5D U+1ED75 U+E0145 U+E0159 U+E01EF | at the start of a word |
| `ey` | `𞵳𞵝𞵵󠅅󠅙󠇯` | U+1ED73 U+1ED5D U+1ED75 U+E0145 U+E0159 U+E01EF | always |
| `eY` | `𞵝𞵳𞵝𞵵󠅅󠄹󠇯` | U+1ED5D U+1ED73 U+1ED5D U+1ED75 U+E0145 U+E0139 U+E01EF | at the start of a word |
| `eY` | `𞵳𞵝𞵵󠅅󠄹󠇯` | U+1ED73 U+1ED5D U+1ED75 U+E0145 U+E0139 U+E01EF | always |
| `eý` | `𞵝𞵳𞵝𞵵󠅅󠅛󠅆󠅄󠅝󠇯` | U+1ED5D U+1ED73 U+1ED5D U+1ED75 U+E0145 U+E015B U+E0146 U+E0144 U+E015D U+E01EF | at the start of a word |
| `eý` | `𞵳𞵝𞵵󠅅󠅛󠅆󠅄󠅝󠇯` | U+1ED73 U+1ED5D U+1ED75 U+E0145 U+E015B U+E0146 U+E0144 U+E015D U+E01EF | always |
| `eÝ` | `𞵝𞵳𞵝𞵵󠅅󠅛󠅄󠅄󠅝󠇯` | U+1ED5D U+1ED73 U+1ED5D U+1ED75 U+E0145 U+E015B U+E0144 U+E0144 U+E015D U+E01EF | at the start of a word |
| `eÝ` | `𞵳𞵝𞵵󠅅󠅛󠅄󠅄󠅝󠇯` | U+1ED73 U+1ED5D U+1ED75 U+E0145 U+E015B U+E0144 U+E0144 U+E015D U+E01EF | always |
| `Ey` | `𞵝𞵳𞵝𞵵󠄥󠅙󠇯` | U+1ED5D U+1ED73 U+1ED5D U+1ED75 U+E0125 U+E0159 U+E01EF | at the start of a word |
| `Ey` | `𞵳𞵝𞵵󠄥󠅙󠇯` | U+1ED73 U+1ED5D U+1ED75 U+E0125 U+E0159 U+E01EF | always |
| `EY` | `𞵝𞵳𞵝𞵵󠄥󠄹󠇯` | U+1ED5D U+1ED73 U+1ED5D U+1ED75 U+E0125 U+E0139 U+E01EF | at the start of a word |
| `EY` | `𞵳𞵝𞵵󠄥󠄹󠇯` | U+1ED73 U+1ED5D U+1ED75 U+E0125 U+E0139 U+E01EF | always |
| `Eý` | `𞵝𞵳𞵝𞵵󠄥󠅛󠅆󠅄󠅝󠇯` | U+1ED5D U+1ED73 U+1ED5D U+1ED75 U+E0125 U+E015B U+E0146 U+E0144 U+E015D U+E01EF | at the start of a word |
| `Eý` | `𞵳𞵝𞵵󠄥󠅛󠅆󠅄󠅝󠇯` | U+1ED73 U+1ED5D U+1ED75 U+E0125 U+E015B U+E0146 U+E0144 U+E015D U+E01EF | always |
| `EÝ` | `𞵝𞵳𞵝𞵵󠄥󠅛󠅄󠅄󠅝󠇯` | U+1ED5D U+1ED73 U+1ED5D U+1ED75 U+E0125 U+E015B U+E0144 U+E0144 U+E015D U+E01EF | at the start of a word |
| `EÝ` | `𞵳𞵝𞵵󠄥󠅛󠅄󠅄󠅝󠇯` | U+1ED73 U+1ED5D U+1ED75 U+E0125 U+E015B U+E0144 U+E0144 U+E015D U+E01EF | always |
| `éy` | `𞵝𞵳𞵝𞵵󠅛󠅅󠄙󠅝󠅙󠇯` | U+1ED5D U+1ED73 U+1ED5D U+1ED75 U+E015B U+E0145 U+E0119 U+E015D U+E0159 U+E01EF | at the start of a word |
| `éy` | `𞵳𞵝𞵵󠅛󠅅󠄙󠅝󠅙󠇯` | U+1ED73 U+1ED5D U+1ED75 U+E015B U+E0145 U+E0119 U+E015D U+E0159 U+E01EF | always |
| `éY` | `𞵝𞵳𞵝𞵵󠅛󠅅󠄙󠅝󠄹󠇯` | U+1ED5D U+1ED73 U+1ED5D U+1ED75 U+E015B U+E0145 U+E0119 U+E015D U+E0139 U+E01EF | at the start of a word |
| `éY` | `𞵳𞵝𞵵󠅛󠅅󠄙󠅝󠄹󠇯` | U+1ED73 U+1ED5D U+1ED75 U+E015B U+E0145 U+E0119 U+E015D U+E0139 U+E01EF | always |
| `éý` | `𞵝𞵳𞵝𞵵󠅛󠅅󠄙󠅝󠅛󠅆󠅄󠅝󠇯` | U+1ED5D U+1ED73 U+1ED5D U+1ED75 U+E015B U+E0145 U+E0119 U+E015D U+E015B U+E0146 U+E0144 U+E015D U+E01EF | at the start of a word |
| `éý` | `𞵳𞵝𞵵󠅛󠅅󠄙󠅝󠅛󠅆󠅄󠅝󠇯` | U+1ED73 U+1ED5D U+1ED75 U+E015B U+E0145 U+E0119 U+E015D U+E015B U+E0146 U+E0144 U+E015D U+E01EF | always |
| `éÝ` | `𞵝𞵳𞵝𞵵󠅛󠅅󠄙󠅝󠅛󠅄󠅄󠅝󠇯` | U+1ED5D U+1ED73 U+1ED5D U+1ED75 U+E015B U+E0145 U+E0119 U+E015D U+E015B U+E0144 U+E0144 U+E015D U+E01EF | at the start of a word |
| `éÝ` | `𞵳𞵝𞵵󠅛󠅅󠄙󠅝󠅛󠅄󠅄󠅝󠇯` | U+1ED73 U+1ED5D U+1ED75 U+E015B U+E0145 U+E0119 U+E015D U+E015B U+E0144 U+E0144 U+E015D U+E01EF | always |
| `Éy` | `𞵝𞵳𞵝𞵵󠅛󠅃󠄙󠅝󠅙󠇯` | U+1ED5D U+1ED73 U+1ED5D U+1ED75 U+E015B U+E0143 U+E0119 U+E015D U+E0159 U+E01EF | at the start of a word |
| `Éy` | `𞵳𞵝𞵵󠅛󠅃󠄙󠅝󠅙󠇯` | U+1ED73 U+1ED5D U+1ED75 U+E015B U+E0143 U+E0119 U+E015D U+E0159 U+E01EF | always |
| `ÉY` | `𞵝𞵳𞵝𞵵󠅛󠅃󠄙󠅝󠄹󠇯` | U+1ED5D U+1ED73 U+1ED5D U+1ED75 U+E015B U+E0143 U+E0119 U+E015D U+E0139 U+E01EF | at the start of a word |
| `ÉY` | `𞵳𞵝𞵵󠅛󠅃󠄙󠅝󠄹󠇯` | U+1ED73 U+1ED5D U+1ED75 U+E015B U+E0143 U+E0119 U+E015D U+E0139 U+E01EF | always |
| `Éý` | `𞵝𞵳𞵝𞵵󠅛󠅃󠄙󠅝󠅛󠅆󠅄󠅝󠇯` | U+1ED5D U+1ED73 U+1ED5D U+1ED75 U+E015B U+E0143 U+E0119 U+E015D U+E015B U+E0146 U+E0144 U+E015D U+E01EF | at the start of a word |
| `Éý` | `𞵳𞵝𞵵󠅛󠅃󠄙󠅝󠅛󠅆󠅄󠅝󠇯` | U+1ED73 U+1ED5D U+1ED75 U+E015B U+E0143 U+E0119 U+E015D U+E015B U+E0146 U+E0144 U+E015D U+E01EF | always |
| `ÉÝ` | `𞵝𞵳𞵝𞵵󠅛󠅃󠄙󠅝󠅛󠅄󠅄󠅝󠇯` | U+1ED5D U+1ED73 U+1ED5D U+1ED75 U+E015B U+E0143 U+E0119 U+E015D U+E015B U+E0144 U+E0144 U+E015D U+E01EF | at the start of a word |
| `ÉÝ` | `𞵳𞵝𞵵󠅛󠅃󠄙󠅝󠅛󠅄󠅄󠅝󠇯` | U+1ED73 U+1ED5D U+1ED75 U+E015B U+E0143 U+E0119 U+E015D U+E015B U+E0144 U+E0144 U+E015D U+E01EF | always |
| `eë` | `𞵝𞵶𞵸` | U+1ED5D U+1ED76 U+1ED78 | at the start of a word |
| `eë` | `𞵶𞵸` | U+1ED76 U+1ED78 | always |
| `eË` | `𞵝𞵶𞵸󠅅󠅛󠅃󠅂󠅝󠇯` | U+1ED5D U+1ED76 U+1ED78 U+E0145 U+E015B U+E0143 U+E0142 U+E015D U+E01EF | at the start of a word |
| `eË` | `𞵶𞵸󠅅󠅛󠅃󠅂󠅝󠇯` | U+1ED76 U+1ED78 U+E0145 U+E015B U+E0143 U+E0142 U+E015D U+E01EF | always |
| `Eë` | `𞵝𞵶𞵸󠄥󠅛󠅅󠅂󠅝󠇯` | U+1ED5D U+1ED76 U+1ED78 U+E0125 U+E015B U+E0145 U+E0142 U+E015D U+E01EF | at the start of a word |
| `Eë` | `𞵶𞵸󠄥󠅛󠅅󠅂󠅝󠇯` | U+1ED76 U+1ED78 U+E0125 U+E015B U+E0145 U+E0142 U+E015D U+E01EF | always |
| `EË` | `𞵝𞵶𞵸󠄥󠅛󠅃󠅂󠅝󠇯` | U+1ED5D U+1ED76 U+1ED78 U+E0125 U+E015B U+E0143 U+E0142 U+E015D U+E01EF | at the start of a word |
| `EË` | `𞵶𞵸󠄥󠅛󠅃󠅂󠅝󠇯` | U+1ED76 U+1ED78 U+E0125 U+E015B U+E0143 U+E0142 U+E015D U+E01EF | always |
| `éë` | `𞵝𞵶𞵸󠅛󠅅󠄙󠅝󠅛󠅅󠅂󠅝󠇯` | U+1ED5D U+1ED76 U+1ED78 U+E015B U+E0145 U+E0119 U+E015D U+E015B U+E0145 U+E0142 U+E015D U+E01EF | at the start of a word |
| `éë` | `𞵶𞵸󠅛󠅅󠄙󠅝󠅛󠅅󠅂󠅝󠇯` | U+1ED76 U+1ED78 U+E015B U+E0145 U+E0119 U+E015D U+E015B U+E0145 U+E0142 U+E015D U+E01EF | always |
| `éË` | `𞵝𞵶𞵸󠅛󠅅󠄙󠅝󠅛󠅃󠅂󠅝󠇯` | U+1ED5D U+1ED76 U+1ED78 U+E015B U+E0145 U+E0119 U+E015D U+E015B U+E0143 U+E0142 U+E015D U+E01EF | at the start of a word |
| `éË` | `𞵶𞵸󠅛󠅅󠄙󠅝󠅛󠅃󠅂󠅝󠇯` | U+1ED76 U+1ED78 U+E015B U+E0145 U+E0119 U+E015D U+E015B U+E0143 U+E0142 U+E015D U+E01EF | always |
| `Éë` | `𞵝𞵶𞵸󠅛󠅃󠄙󠅝󠅛󠅅󠅂󠅝󠇯` | U+1ED5D U+1ED76 U+1ED78 U+E015B U+E0143 U+E0119 U+E015D U+E015B U+E0145 U+E0142 U+E015D U+E01EF | at the start of a word |
| `Éë` | `𞵶𞵸󠅛󠅃󠄙󠅝󠅛󠅅󠅂󠅝󠇯` | U+1ED76 U+1ED78 U+E015B U+E0143 U+E0119 U+E015D U+E015B U+E0145 U+E0142 U+E015D U+E01EF | always |
| `ÉË` | `𞵝𞵶𞵸󠅛󠅃󠄙󠅝󠅛󠅃󠅂󠅝󠇯` | U+1ED5D U+1ED76 U+1ED78 U+E015B U+E0143 U+E0119 U+E015D U+E015B U+E0143 U+E0142 U+E015D U+E01EF | at the start of a word |
| `ÉË` | `𞵶𞵸󠅛󠅃󠄙󠅝󠅛󠅃󠅂󠅝󠇯` | U+1ED76 U+1ED78 U+E015B U+E0143 U+E0119 U+E015D U+E015B U+E0143 U+E0142 U+E015D U+E01EF | always |
| `ii` | `𞵝𞵴𞵸` | U+1ED5D U+1ED74 U+1ED78 | at the start of a word |
| `ii` | `𞵴𞵸` | U+1ED74 U+1ED78 | always |
| `iI` | `𞵝𞵴𞵸󠅉󠄩󠇯` | U+1ED5D U+1ED74 U+1ED78 U+E0149 U+E0129 U+E01EF | at the start of a word |
| `iI` | `𞵴𞵸󠅉󠄩󠇯` | U+1ED74 U+1ED78 U+E0149 U+E0129 U+E01EF | always |
| `ií` | `𞵝𞵴𞵸󠅉󠅛󠅅󠅄󠅝󠇯` | U+1ED5D U+1ED74 U+1ED78 U+E0149 U+E015B U+E0145 U+E0144 U+E015D U+E01EF | at the start of a word |
| `ií` | `𞵴𞵸󠅉󠅛󠅅󠅄󠅝󠇯` | U+1ED74 U+1ED78 U+E0149 U+E015B U+E0145 U+E0144 U+E015D U+E01EF | always |
| `iÍ` | `𞵝𞵴𞵸󠅉󠅛󠅃󠅄󠅝󠇯` | U+1ED5D U+1ED74 U+1ED78 U+E0149 U+E015B U+E0143 U+E0144 U+E015D U+E01EF | at the start of a word |
| `iÍ` | `𞵴𞵸󠅉󠅛󠅃󠅄󠅝󠇯` | U+1ED74 U+1ED78 U+E0149 U+E015B U+E0143 U+E0144 U+E015D U+E01EF | always |
| `Ii` | `𞵝𞵴𞵸󠄩󠅉󠇯` | U+1ED5D U+1ED74 U+1ED78 U+E0129 U+E0149 U+E01EF | at the start of a word |
| `Ii` | `𞵴𞵸󠄩󠅉󠇯` | U+1ED74 U+1ED78 U+E0129 U+E0149 U+E01EF | always |
| `II` | `𞵝𞵴𞵸󠄩󠄩󠇯` | U+1ED5D U+1ED74 U+1ED78 U+E0129 U+E0129 U+E01EF | at the start of a word |
| `II` | `𞵴𞵸󠄩󠄩󠇯` | U+1ED74 U+1ED78 U+E0129 U+E0129 U+E01EF | always |
| `Ií` | `𞵝𞵴𞵸󠄩󠅛󠅅󠅄󠅝󠇯` | U+1ED5D U+1ED74 U+1ED78 U+E0129 U+E015B U+E0145 U+E0144 U+E015D U+E01EF | at the start of a word |
| `Ií` | `𞵴𞵸󠄩󠅛󠅅󠅄󠅝󠇯` | U+1ED74 U+1ED78 U+E0129 U+E015B U+E0145 U+E0144 U+E015D U+E01EF | always |
| `IÍ` | `𞵝𞵴𞵸󠄩󠅛󠅃󠅄󠅝󠇯` | U+1ED5D U+1ED74 U+1ED78 U+E0129 U+E015B U+E0143 U+E0144 U+E015D U+E01EF | at the start of a word |
| `IÍ` | `𞵴𞵸󠄩󠅛󠅃󠅄󠅝󠇯` | U+1ED74 U+1ED78 U+E0129 U+E015B U+E0143 U+E0144 U+E015D U+E01EF | always |
| `íi` | `𞵝𞵴𞵸󠅛󠅅󠅄󠅝󠅉󠇯` | U+1ED5D U+1ED74 U+1ED78 U+E015B U+E0145 U+E0144 U+E015D U+E0149 U+E01EF | at the start of a word |
| `íi` | `𞵴𞵸󠅛󠅅󠅄󠅝󠅉󠇯` | U+1ED74 U+1ED78 U+E015B U+E0145 U+E0144 U+E015D U+E0149 U+E01EF | always |
| `íI` | `𞵝𞵴𞵸󠅛󠅅󠅄󠅝󠄩󠇯` | U+1ED5D U+1ED74 U+1ED78 U+E015B U+E0145 U+E0144 U+E015D U+E0129 U+E01EF | at the start of a word |
| `íI` | `𞵴𞵸󠅛󠅅󠅄󠅝󠄩󠇯` | U+1ED74 U+1ED78 U+E015B U+E0145 U+E0144 U+E015D U+E0129 U+E01EF | always |
| `íí` | `𞵝𞵴𞵸󠅛󠅅󠅄󠅝󠅛󠅅󠅄󠅝󠇯` | U+1ED5D U+1ED74 U+1ED78 U+E015B U+E0145 U+E0144 U+E015D U+E015B U+E0145 U+E0144 U+E015D U+E01EF | at the start of a word |
| `íí` | `𞵴𞵸󠅛󠅅󠅄󠅝󠅛󠅅󠅄󠅝󠇯` | U+1ED74 U+1ED78 U+E015B U+E0145 U+E0144 U+E015D U+E015B U+E0145 U+E0144 U+E015D U+E01EF | always |
| `íÍ` | `𞵝𞵴𞵸󠅛󠅅󠅄󠅝󠅛󠅃󠅄󠅝󠇯` | U+1ED5D U+1ED74 U+1ED78 U+E015B U+E0145 U+E0144 U+E015D U+E015B U+E0143 U+E0144 U+E015D U+E01EF | at the start of a word |
| `íÍ` | `𞵴𞵸󠅛󠅅󠅄󠅝󠅛󠅃󠅄󠅝󠇯` | U+1ED74 U+1ED78 U+E015B U+E0145 U+E0144 U+E015D U+E015B U+E0143 U+E0144 U+E015D U+E01EF | always |
| `Íi` | `𞵝𞵴𞵸󠅛󠅃󠅄󠅝󠅉󠇯` | U+1ED5D U+1ED74 U+1ED78 U+E015B U+E0143 U+E0144 U+E015D U+E0149 U+E01EF | at the start of a word |
| `Íi` | `𞵴𞵸󠅛󠅃󠅄󠅝󠅉󠇯` | U+1ED74 U+1ED78 U+E015B U+E0143 U+E0144 U+E015D U+E0149 U+E01EF | always |
| `ÍI` | `𞵝𞵴𞵸󠅛󠅃󠅄󠅝󠄩󠇯` | U+1ED5D U+1ED74 U+1ED78 U+E015B U+E0143 U+E0144 U+E015D U+E0129 U+E01EF | at the start of a word |
| `ÍI` | `𞵴𞵸󠅛󠅃󠅄󠅝󠄩󠇯` | U+1ED74 U+1ED78 U+E015B U+E0143 U+E0144 U+E015D U+E0129 U+E01EF | always |
| `Íí` | `𞵝𞵴𞵸󠅛󠅃󠅄󠅝󠅛󠅅󠅄󠅝󠇯` | U+1ED5D U+1ED74 U+1ED78 U+E015B U+E0143 U+E0144 U+E015D U+E015B U+E0145 U+E0144 U+E015D U+E01EF | at the start of a word |
| `Íí` | `𞵴𞵸󠅛󠅃󠅄󠅝󠅛󠅅󠅄󠅝󠇯` | U+1ED74 U+1ED78 U+E015B U+E0143 U+E0144 U+E015D U+E015B U+E0145 U+E0144 U+E015D U+E01EF | always |
| `ÍÍ` | `𞵝𞵴𞵸󠅛󠅃󠅄󠅝󠅛󠅃󠅄󠅝󠇯` | U+1ED5D U+1ED74 U+1ED78 U+E015B U+E0143 U+E0144 U+E015D U+E015B U+E0143 U+E0144 U+E015D U+E01EF | at the start of a word |
| `ÍÍ` | `𞵴𞵸󠅛󠅃󠅄󠅝󠅛󠅃󠅄󠅝󠇯` | U+1ED74 U+1ED78 U+E015B U+E0143 U+E0144 U+E015D U+E015B U+E0143 U+E0144 U+E015D U+E01EF | always |
| `io` | `𞵝𞵴𞵝𞵱󠅉󠅏󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED71 U+E0149 U+E014F U+E01EF | at the start of a word |
| `io` | `𞵴𞵝𞵱󠅉󠅏󠇯` | U+1ED74 U+1ED5D U+1ED71 U+E0149 U+E014F U+E01EF | always |
| `iO` | `𞵝𞵴𞵝𞵱󠅉󠄯󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED71 U+E0149 U+E012F U+E01EF | at the start of a word |
| `iO` | `𞵴𞵝𞵱󠅉󠄯󠇯` | U+1ED74 U+1ED5D U+1ED71 U+E0149 U+E012F U+E01EF | always |
| `ió` | `𞵝𞵴𞵝𞵱󠅉󠅛󠅆󠄓󠅝󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED71 U+E0149 U+E015B U+E0146 U+E0113 U+E015D U+E01EF | at the start of a word |
| `ió` | `𞵴𞵝𞵱󠅉󠅛󠅆󠄓󠅝󠇯` | U+1ED74 U+1ED5D U+1ED71 U+E0149 U+E015B U+E0146 U+E0113 U+E015D U+E01EF | always |
| `iÓ` | `𞵝𞵴𞵝𞵱󠅉󠅛󠅄󠄓󠅝󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED71 U+E0149 U+E015B U+E0144 U+E0113 U+E015D U+E01EF | at the start of a word |
| `iÓ` | `𞵴𞵝𞵱󠅉󠅛󠅄󠄓󠅝󠇯` | U+1ED74 U+1ED5D U+1ED71 U+E0149 U+E015B U+E0144 U+E0113 U+E015D U+E01EF | always |
| `Io` | `𞵝𞵴𞵝𞵱󠄩󠅏󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED71 U+E0129 U+E014F U+E01EF | at the start of a word |
| `Io` | `𞵴𞵝𞵱󠄩󠅏󠇯` | U+1ED74 U+1ED5D U+1ED71 U+E0129 U+E014F U+E01EF | always |
| `IO` | `𞵝𞵴𞵝𞵱󠄩󠄯󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED71 U+E0129 U+E012F U+E01EF | at the start of a word |
| `IO` | `𞵴𞵝𞵱󠄩󠄯󠇯` | U+1ED74 U+1ED5D U+1ED71 U+E0129 U+E012F U+E01EF | always |
| `Ió` | `𞵝𞵴𞵝𞵱󠄩󠅛󠅆󠄓󠅝󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED71 U+E0129 U+E015B U+E0146 U+E0113 U+E015D U+E01EF | at the start of a word |
| `Ió` | `𞵴𞵝𞵱󠄩󠅛󠅆󠄓󠅝󠇯` | U+1ED74 U+1ED5D U+1ED71 U+E0129 U+E015B U+E0146 U+E0113 U+E015D U+E01EF | always |
| `IÓ` | `𞵝𞵴𞵝𞵱󠄩󠅛󠅄󠄓󠅝󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED71 U+E0129 U+E015B U+E0144 U+E0113 U+E015D U+E01EF | at the start of a word |
| `IÓ` | `𞵴𞵝𞵱󠄩󠅛󠅄󠄓󠅝󠇯` | U+1ED74 U+1ED5D U+1ED71 U+E0129 U+E015B U+E0144 U+E0113 U+E015D U+E01EF | always |
| `ío` | `𞵝𞵴𞵝𞵱󠅛󠅅󠅄󠅝󠅏󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED71 U+E015B U+E0145 U+E0144 U+E015D U+E014F U+E01EF | at the start of a word |
| `ío` | `𞵴𞵝𞵱󠅛󠅅󠅄󠅝󠅏󠇯` | U+1ED74 U+1ED5D U+1ED71 U+E015B U+E0145 U+E0144 U+E015D U+E014F U+E01EF | always |
| `íO` | `𞵝𞵴𞵝𞵱󠅛󠅅󠅄󠅝󠄯󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED71 U+E015B U+E0145 U+E0144 U+E015D U+E012F U+E01EF | at the start of a word |
| `íO` | `𞵴𞵝𞵱󠅛󠅅󠅄󠅝󠄯󠇯` | U+1ED74 U+1ED5D U+1ED71 U+E015B U+E0145 U+E0144 U+E015D U+E012F U+E01EF | always |
| `íó` | `𞵝𞵴𞵝𞵱󠅛󠅅󠅄󠅝󠅛󠅆󠄓󠅝󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED71 U+E015B U+E0145 U+E0144 U+E015D U+E015B U+E0146 U+E0113 U+E015D U+E01EF | at the start of a word |
| `íó` | `𞵴𞵝𞵱󠅛󠅅󠅄󠅝󠅛󠅆󠄓󠅝󠇯` | U+1ED74 U+1ED5D U+1ED71 U+E015B U+E0145 U+E0144 U+E015D U+E015B U+E0146 U+E0113 U+E015D U+E01EF | always |
| `íÓ` | `𞵝𞵴𞵝𞵱󠅛󠅅󠅄󠅝󠅛󠅄󠄓󠅝󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED71 U+E015B U+E0145 U+E0144 U+E015D U+E015B U+E0144 U+E0113 U+E015D U+E01EF | at the start of a word |
| `íÓ` | `𞵴𞵝𞵱󠅛󠅅󠅄󠅝󠅛󠅄󠄓󠅝󠇯` | U+1ED74 U+1ED5D U+1ED71 U+E015B U+E0145 U+E0144 U+E015D U+E015B U+E0144 U+E0113 U+E015D U+E01EF | always |
| `Ío` | `𞵝𞵴𞵝𞵱󠅛󠅃󠅄󠅝󠅏󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED71 U+E015B U+E0143 U+E0144 U+E015D U+E014F U+E01EF | at the start of a word |
| `Ío` | `𞵴𞵝𞵱󠅛󠅃󠅄󠅝󠅏󠇯` | U+1ED74 U+1ED5D U+1ED71 U+E015B U+E0143 U+E0144 U+E015D U+E014F U+E01EF | always |
| `ÍO` | `𞵝𞵴𞵝𞵱󠅛󠅃󠅄󠅝󠄯󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED71 U+E015B U+E0143 U+E0144 U+E015D U+E012F U+E01EF | at the start of a word |
| `ÍO` | `𞵴𞵝𞵱󠅛󠅃󠅄󠅝󠄯󠇯` | U+1ED74 U+1ED5D U+1ED71 U+E015B U+E0143 U+E0144 U+E015D U+E012F U+E01EF | always |
| `Íó` | `𞵝𞵴𞵝𞵱󠅛󠅃󠅄󠅝󠅛󠅆󠄓󠅝󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED71 U+E015B U+E0143 U+E0144 U+E015D U+E015B U+E0146 U+E0113 U+E015D U+E01EF | at the start of a word |
| `Íó` | `𞵴𞵝𞵱󠅛󠅃󠅄󠅝󠅛󠅆󠄓󠅝󠇯` | U+1ED74 U+1ED5D U+1ED71 U+E015B U+E0143 U+E0144 U+E015D U+E015B U+E0146 U+E0113 U+E015D U+E01EF | always |
| `ÍÓ` | `𞵝𞵴𞵝𞵱󠅛󠅃󠅄󠅝󠅛󠅄󠄓󠅝󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED71 U+E015B U+E0143 U+E0144 U+E015D U+E015B U+E0144 U+E0113 U+E015D U+E01EF | at the start of a word |
| `ÍÓ` | `𞵴𞵝𞵱󠅛󠅃󠅄󠅝󠅛󠅄󠄓󠅝󠇯` | U+1ED74 U+1ED5D U+1ED71 U+E015B U+E0143 U+E0144 U+E015D U+E015B U+E0144 U+E0113 U+E015D U+E01EF | always |
| `iu` | `𞵝𞵴𞵝𞵲󠅉󠅕󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED72 U+E0149 U+E0155 U+E01EF | at the start of a word |
| `iu` | `𞵴𞵝𞵲󠅉󠅕󠇯` | U+1ED74 U+1ED5D U+1ED72 U+E0149 U+E0155 U+E01EF | always |
| `iU` | `𞵝𞵴𞵝𞵲󠅉󠄵󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED72 U+E0149 U+E0135 U+E01EF | at the start of a word |
| `iU` | `𞵴𞵝𞵲󠅉󠄵󠇯` | U+1ED74 U+1ED5D U+1ED72 U+E0149 U+E0135 U+E01EF | always |
| `iú` | `𞵝𞵴𞵝𞵲󠅉󠅛󠅆󠅁󠅝󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED72 U+E0149 U+E015B U+E0146 U+E0141 U+E015D U+E01EF | at the start of a word |
| `iú` | `𞵴𞵝𞵲󠅉󠅛󠅆󠅁󠅝󠇯` | U+1ED74 U+1ED5D U+1ED72 U+E0149 U+E015B U+E0146 U+E0141 U+E015D U+E01EF | always |
| `iÚ` | `𞵝𞵴𞵝𞵲󠅉󠅛󠅄󠅁󠅝󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED72 U+E0149 U+E015B U+E0144 U+E0141 U+E015D U+E01EF | at the start of a word |
| `iÚ` | `𞵴𞵝𞵲󠅉󠅛󠅄󠅁󠅝󠇯` | U+1ED74 U+1ED5D U+1ED72 U+E0149 U+E015B U+E0144 U+E0141 U+E015D U+E01EF | always |
| `Iu` | `𞵝𞵴𞵝𞵲󠄩󠅕󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED72 U+E0129 U+E0155 U+E01EF | at the start of a word |
| `Iu` | `𞵴𞵝𞵲󠄩󠅕󠇯` | U+1ED74 U+1ED5D U+1ED72 U+E0129 U+E0155 U+E01EF | always |
| `IU` | `𞵝𞵴𞵝𞵲󠄩󠄵󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED72 U+E0129 U+E0135 U+E01EF | at the start of a word |
| `IU` | `𞵴𞵝𞵲󠄩󠄵󠇯` | U+1ED74 U+1ED5D U+1ED72 U+E0129 U+E0135 U+E01EF | always |
| `Iú` | `𞵝𞵴𞵝𞵲󠄩󠅛󠅆󠅁󠅝󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED72 U+E0129 U+E015B U+E0146 U+E0141 U+E015D U+E01EF | at the start of a word |
| `Iú` | `𞵴𞵝𞵲󠄩󠅛󠅆󠅁󠅝󠇯` | U+1ED74 U+1ED5D U+1ED72 U+E0129 U+E015B U+E0146 U+E0141 U+E015D U+E01EF | always |
| `IÚ` | `𞵝𞵴𞵝𞵲󠄩󠅛󠅄󠅁󠅝󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED72 U+E0129 U+E015B U+E0144 U+E0141 U+E015D U+E01EF | at the start of a word |
| `IÚ` | `𞵴𞵝𞵲󠄩󠅛󠅄󠅁󠅝󠇯` | U+1ED74 U+1ED5D U+1ED72 U+E0129 U+E015B U+E0144 U+E0141 U+E015D U+E01EF | always |
| `íu` | `𞵝𞵴𞵝𞵲󠅛󠅅󠅄󠅝󠅕󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED72 U+E015B U+E0145 U+E0144 U+E015D U+E0155 U+E01EF | at the start of a word |
| `íu` | `𞵴𞵝𞵲󠅛󠅅󠅄󠅝󠅕󠇯` | U+1ED74 U+1ED5D U+1ED72 U+E015B U+E0145 U+E0144 U+E015D U+E0155 U+E01EF | always |
| `íU` | `𞵝𞵴𞵝𞵲󠅛󠅅󠅄󠅝󠄵󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED72 U+E015B U+E0145 U+E0144 U+E015D U+E0135 U+E01EF | at the start of a word |
| `íU` | `𞵴𞵝𞵲󠅛󠅅󠅄󠅝󠄵󠇯` | U+1ED74 U+1ED5D U+1ED72 U+E015B U+E0145 U+E0144 U+E015D U+E0135 U+E01EF | always |
| `íú` | `𞵝𞵴𞵝𞵲󠅛󠅅󠅄󠅝󠅛󠅆󠅁󠅝󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED72 U+E015B U+E0145 U+E0144 U+E015D U+E015B U+E0146 U+E0141 U+E015D U+E01EF | at the start of a word |
| `íú` | `𞵴𞵝𞵲󠅛󠅅󠅄󠅝󠅛󠅆󠅁󠅝󠇯` | U+1ED74 U+1ED5D U+1ED72 U+E015B U+E0145 U+E0144 U+E015D U+E015B U+E0146 U+E0141 U+E015D U+E01EF | always |
| `íÚ` | `𞵝𞵴𞵝𞵲󠅛󠅅󠅄󠅝󠅛󠅄󠅁󠅝󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED72 U+E015B U+E0145 U+E0144 U+E015D U+E015B U+E0144 U+E0141 U+E015D U+E01EF | at the start of a word |
| `íÚ` | `𞵴𞵝𞵲󠅛󠅅󠅄󠅝󠅛󠅄󠅁󠅝󠇯` | U+1ED74 U+1ED5D U+1ED72 U+E015B U+E0145 U+E0144 U+E015D U+E015B U+E0144 U+E0141 U+E015D U+E01EF | always |
| `Íu` | `𞵝𞵴𞵝𞵲󠅛󠅃󠅄󠅝󠅕󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED72 U+E015B U+E0143 U+E0144 U+E015D U+E0155 U+E01EF | at the start of a word |
| `Íu` | `𞵴𞵝𞵲󠅛󠅃󠅄󠅝󠅕󠇯` | U+1ED74 U+1ED5D U+1ED72 U+E015B U+E0143 U+E0144 U+E015D U+E0155 U+E01EF | always |
| `ÍU` | `𞵝𞵴𞵝𞵲󠅛󠅃󠅄󠅝󠄵󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED72 U+E015B U+E0143 U+E0144 U+E015D U+E0135 U+E01EF | at the start of a word |
| `ÍU` | `𞵴𞵝𞵲󠅛󠅃󠅄󠅝󠄵󠇯` | U+1ED74 U+1ED5D U+1ED72 U+E015B U+E0143 U+E0144 U+E015D U+E0135 U+E01EF | always |
| `Íú` | `𞵝𞵴𞵝𞵲󠅛󠅃󠅄󠅝󠅛󠅆󠅁󠅝󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED72 U+E015B U+E0143 U+E0144 U+E015D U+E015B U+E0146 U+E0141 U+E015D U+E01EF | at the start of a word |
| `Íú` | `𞵴𞵝𞵲󠅛󠅃󠅄󠅝󠅛󠅆󠅁󠅝󠇯` | U+1ED74 U+1ED5D U+1ED72 U+E015B U+E0143 U+E0144 U+E015D U+E015B U+E0146 U+E0141 U+E015D U+E01EF | always |
| `ÍÚ` | `𞵝𞵴𞵝𞵲󠅛󠅃󠅄󠅝󠅛󠅄󠅁󠅝󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED72 U+E015B U+E0143 U+E0144 U+E015D U+E015B U+E0144 U+E0141 U+E015D U+E01EF | at the start of a word |
| `ÍÚ` | `𞵴𞵝𞵲󠅛󠅃󠅄󠅝󠅛󠅄󠅁󠅝󠇯` | U+1ED74 U+1ED5D U+1ED72 U+E015B U+E0143 U+E0144 U+E015D U+E015B U+E0144 U+E0141 U+E015D U+E01EF | always |
| `iy` | `𞵝𞵴𞵝𞵵󠅉󠅙󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED75 U+E0149 U+E0159 U+E01EF | at the start of a word |
| `iy` | `𞵴𞵝𞵵󠅉󠅙󠇯` | U+1ED74 U+1ED5D U+1ED75 U+E0149 U+E0159 U+E01EF | always |
| `iY` | `𞵝𞵴𞵝𞵵󠅉󠄹󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED75 U+E0149 U+E0139 U+E01EF | at the start of a word |
| `iY` | `𞵴𞵝𞵵󠅉󠄹󠇯` | U+1ED74 U+1ED5D U+1ED75 U+E0149 U+E0139 U+E01EF | always |
| `iý` | `𞵝𞵴𞵝𞵵󠅉󠅛󠅆󠅄󠅝󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED75 U+E0149 U+E015B U+E0146 U+E0144 U+E015D U+E01EF | at the start of a word |
| `iý` | `𞵴𞵝𞵵󠅉󠅛󠅆󠅄󠅝󠇯` | U+1ED74 U+1ED5D U+1ED75 U+E0149 U+E015B U+E0146 U+E0144 U+E015D U+E01EF | always |
| `iÝ` | `𞵝𞵴𞵝𞵵󠅉󠅛󠅄󠅄󠅝󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED75 U+E0149 U+E015B U+E0144 U+E0144 U+E015D U+E01EF | at the start of a word |
| `iÝ` | `𞵴𞵝𞵵󠅉󠅛󠅄󠅄󠅝󠇯` | U+1ED74 U+1ED5D U+1ED75 U+E0149 U+E015B U+E0144 U+E0144 U+E015D U+E01EF | always |
| `Iy` | `𞵝𞵴𞵝𞵵󠄩󠅙󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED75 U+E0129 U+E0159 U+E01EF | at the start of a word |
| `Iy` | `𞵴𞵝𞵵󠄩󠅙󠇯` | U+1ED74 U+1ED5D U+1ED75 U+E0129 U+E0159 U+E01EF | always |
| `IY` | `𞵝𞵴𞵝𞵵󠄩󠄹󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED75 U+E0129 U+E0139 U+E01EF | at the start of a word |
| `IY` | `𞵴𞵝𞵵󠄩󠄹󠇯` | U+1ED74 U+1ED5D U+1ED75 U+E0129 U+E0139 U+E01EF | always |
| `Iý` | `𞵝𞵴𞵝𞵵󠄩󠅛󠅆󠅄󠅝󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED75 U+E0129 U+E015B U+E0146 U+E0144 U+E015D U+E01EF | at the start of a word |
| `Iý` | `𞵴𞵝𞵵󠄩󠅛󠅆󠅄󠅝󠇯` | U+1ED74 U+1ED5D U+1ED75 U+E0129 U+E015B U+E0146 U+E0144 U+E015D U+E01EF | always |
| `IÝ` | `𞵝𞵴𞵝𞵵󠄩󠅛󠅄󠅄󠅝󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED75 U+E0129 U+E015B U+E0144 U+E0144 U+E015D U+E01EF | at the start of a word |
| `IÝ` | `𞵴𞵝𞵵󠄩󠅛󠅄󠅄󠅝󠇯` | U+1ED74 U+1ED5D U+1ED75 U+E0129 U+E015B U+E0144 U+E0144 U+E015D U+E01EF | always |
| `íy` | `𞵝𞵴𞵝𞵵󠅛󠅅󠅄󠅝󠅙󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED75 U+E015B U+E0145 U+E0144 U+E015D U+E0159 U+E01EF | at the start of a word |
| `íy` | `𞵴𞵝𞵵󠅛󠅅󠅄󠅝󠅙󠇯` | U+1ED74 U+1ED5D U+1ED75 U+E015B U+E0145 U+E0144 U+E015D U+E0159 U+E01EF | always |
| `íY` | `𞵝𞵴𞵝𞵵󠅛󠅅󠅄󠅝󠄹󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED75 U+E015B U+E0145 U+E0144 U+E015D U+E0139 U+E01EF | at the start of a word |
| `íY` | `𞵴𞵝𞵵󠅛󠅅󠅄󠅝󠄹󠇯` | U+1ED74 U+1ED5D U+1ED75 U+E015B U+E0145 U+E0144 U+E015D U+E0139 U+E01EF | always |
| `íý` | `𞵝𞵴𞵝𞵵󠅛󠅅󠅄󠅝󠅛󠅆󠅄󠅝󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED75 U+E015B U+E0145 U+E0144 U+E015D U+E015B U+E0146 U+E0144 U+E015D U+E01EF | at the start of a word |
| `íý` | `𞵴𞵝𞵵󠅛󠅅󠅄󠅝󠅛󠅆󠅄󠅝󠇯` | U+1ED74 U+1ED5D U+1ED75 U+E015B U+E0145 U+E0144 U+E015D U+E015B U+E0146 U+E0144 U+E015D U+E01EF | always |
| `íÝ` | `𞵝𞵴𞵝𞵵󠅛󠅅󠅄󠅝󠅛󠅄󠅄󠅝󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED75 U+E015B U+E0145 U+E0144 U+E015D U+E015B U+E0144 U+E0144 U+E015D U+E01EF | at the start of a word |
| `íÝ` | `𞵴𞵝𞵵󠅛󠅅󠅄󠅝󠅛󠅄󠅄󠅝󠇯` | U+1ED74 U+1ED5D U+1ED75 U+E015B U+E0145 U+E0144 U+E015D U+E015B U+E0144 U+E0144 U+E015D U+E01EF | always |
| `Íy` | `𞵝𞵴𞵝𞵵󠅛󠅃󠅄󠅝󠅙󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED75 U+E015B U+E0143 U+E0144 U+E015D U+E0159 U+E01EF | at the start of a word |
| `Íy` | `𞵴𞵝𞵵󠅛󠅃󠅄󠅝󠅙󠇯` | U+1ED74 U+1ED5D U+1ED75 U+E015B U+E0143 U+E0144 U+E015D U+E0159 U+E01EF | always |
| `ÍY` | `𞵝𞵴𞵝𞵵󠅛󠅃󠅄󠅝󠄹󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED75 U+E015B U+E0143 U+E0144 U+E015D U+E0139 U+E01EF | at the start of a word |
| `ÍY` | `𞵴𞵝𞵵󠅛󠅃󠅄󠅝󠄹󠇯` | U+1ED74 U+1ED5D U+1ED75 U+E015B U+E0143 U+E0144 U+E015D U+E0139 U+E01EF | always |
| `Íý` | `𞵝𞵴𞵝𞵵󠅛󠅃󠅄󠅝󠅛󠅆󠅄󠅝󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED75 U+E015B U+E0143 U+E0144 U+E015D U+E015B U+E0146 U+E0144 U+E015D U+E01EF | at the start of a word |
| `Íý` | `𞵴𞵝𞵵󠅛󠅃󠅄󠅝󠅛󠅆󠅄󠅝󠇯` | U+1ED74 U+1ED5D U+1ED75 U+E015B U+E0143 U+E0144 U+E015D U+E015B U+E0146 U+E0144 U+E015D U+E01EF | always |
| `ÍÝ` | `𞵝𞵴𞵝𞵵󠅛󠅃󠅄󠅝󠅛󠅄󠅄󠅝󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED75 U+E015B U+E0143 U+E0144 U+E015D U+E015B U+E0144 U+E0144 U+E015D U+E01EF | at the start of a word |
| `ÍÝ` | `𞵴𞵝𞵵󠅛󠅃󠅄󠅝󠅛󠅄󠅄󠅝󠇯` | U+1ED74 U+1ED5D U+1ED75 U+E015B U+E0143 U+E0144 U+E015D U+E015B U+E0144 U+E0144 U+E015D U+E01EF | always |
| `ië` | `𞵝𞵴𞵝𞵶󠅉󠅛󠅅󠅂󠅝󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED76 U+E0149 U+E015B U+E0145 U+E0142 U+E015D U+E01EF | at the start of a word |
| `ië` | `𞵴𞵝𞵶󠅉󠅛󠅅󠅂󠅝󠇯` | U+1ED74 U+1ED5D U+1ED76 U+E0149 U+E015B U+E0145 U+E0142 U+E015D U+E01EF | always |
| `iË` | `𞵝𞵴𞵝𞵶󠅉󠅛󠅃󠅂󠅝󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED76 U+E0149 U+E015B U+E0143 U+E0142 U+E015D U+E01EF | at the start of a word |
| `iË` | `𞵴𞵝𞵶󠅉󠅛󠅃󠅂󠅝󠇯` | U+1ED74 U+1ED5D U+1ED76 U+E0149 U+E015B U+E0143 U+E0142 U+E015D U+E01EF | always |
| `Ië` | `𞵝𞵴𞵝𞵶󠄩󠅛󠅅󠅂󠅝󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED76 U+E0129 U+E015B U+E0145 U+E0142 U+E015D U+E01EF | at the start of a word |
| `Ië` | `𞵴𞵝𞵶󠄩󠅛󠅅󠅂󠅝󠇯` | U+1ED74 U+1ED5D U+1ED76 U+E0129 U+E015B U+E0145 U+E0142 U+E015D U+E01EF | always |
| `IË` | `𞵝𞵴𞵝𞵶󠄩󠅛󠅃󠅂󠅝󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED76 U+E0129 U+E015B U+E0143 U+E0142 U+E015D U+E01EF | at the start of a word |
| `IË` | `𞵴𞵝𞵶󠄩󠅛󠅃󠅂󠅝󠇯` | U+1ED74 U+1ED5D U+1ED76 U+E0129 U+E015B U+E0143 U+E0142 U+E015D U+E01EF | always |
| `íë` | `𞵝𞵴𞵝𞵶󠅛󠅅󠅄󠅝󠅛󠅅󠅂󠅝󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED76 U+E015B U+E0145 U+E0144 U+E015D U+E015B U+E0145 U+E0142 U+E015D U+E01EF | at the start of a word |
| `íë` | `𞵴𞵝𞵶󠅛󠅅󠅄󠅝󠅛󠅅󠅂󠅝󠇯` | U+1ED74 U+1ED5D U+1ED76 U+E015B U+E0145 U+E0144 U+E015D U+E015B U+E0145 U+E0142 U+E015D U+E01EF | always |
| `íË` | `𞵝𞵴𞵝𞵶󠅛󠅅󠅄󠅝󠅛󠅃󠅂󠅝󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED76 U+E015B U+E0145 U+E0144 U+E015D U+E015B U+E0143 U+E0142 U+E015D U+E01EF | at the start of a word |
| `íË` | `𞵴𞵝𞵶󠅛󠅅󠅄󠅝󠅛󠅃󠅂󠅝󠇯` | U+1ED74 U+1ED5D U+1ED76 U+E015B U+E0145 U+E0144 U+E015D U+E015B U+E0143 U+E0142 U+E015D U+E01EF | always |
| `Íë` | `𞵝𞵴𞵝𞵶󠅛󠅃󠅄󠅝󠅛󠅅󠅂󠅝󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED76 U+E015B U+E0143 U+E0144 U+E015D U+E015B U+E0145 U+E0142 U+E015D U+E01EF | at the start of a word |
| `Íë` | `𞵴𞵝𞵶󠅛󠅃󠅄󠅝󠅛󠅅󠅂󠅝󠇯` | U+1ED74 U+1ED5D U+1ED76 U+E015B U+E0143 U+E0144 U+E015D U+E015B U+E0145 U+E0142 U+E015D U+E01EF | always |
| `ÍË` | `𞵝𞵴𞵝𞵶󠅛󠅃󠅄󠅝󠅛󠅃󠅂󠅝󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED76 U+E015B U+E0143 U+E0144 U+E015D U+E015B U+E0143 U+E0142 U+E015D U+E01EF | at the start of a word |
| `ÍË` | `𞵴𞵝𞵶󠅛󠅃󠅄󠅝󠅛󠅃󠅂󠅝󠇯` | U+1ED74 U+1ED5D U+1ED76 U+E015B U+E0143 U+E0144 U+E015D U+E015B U+E0143 U+E0142 U+E015D U+E01EF | always |
| `oa` | `𞵝𞵱𞵝𞵰󠅏󠅁󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED70 U+E014F U+E0141 U+E01EF | at the start of a word |
| `oa` | `𞵱𞵝𞵰󠅏󠅁󠇯` | U+1ED71 U+1ED5D U+1ED70 U+E014F U+E0141 U+E01EF | always |
| `oA` | `𞵝𞵱𞵝𞵰󠅏󠄡󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED70 U+E014F U+E0121 U+E01EF | at the start of a word |
| `oA` | `𞵱𞵝𞵰󠅏󠄡󠇯` | U+1ED71 U+1ED5D U+1ED70 U+E014F U+E0121 U+E01EF | always |
| `oá` | `𞵝𞵱𞵝𞵰󠅏󠅛󠅅󠄑󠅝󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED70 U+E014F U+E015B U+E0145 U+E0111 U+E015D U+E01EF | at the start of a word |
| `oá` | `𞵱𞵝𞵰󠅏󠅛󠅅󠄑󠅝󠇯` | U+1ED71 U+1ED5D U+1ED70 U+E014F U+E015B U+E0145 U+E0111 U+E015D U+E01EF | always |
| `oÁ` | `𞵝𞵱𞵝𞵰󠅏󠅛󠅃󠄑󠅝󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED70 U+E014F U+E015B U+E0143 U+E0111 U+E015D U+E01EF | at the start of a word |
| `oÁ` | `𞵱𞵝𞵰󠅏󠅛󠅃󠄑󠅝󠇯` | U+1ED71 U+1ED5D U+1ED70 U+E014F U+E015B U+E0143 U+E0111 U+E015D U+E01EF | always |
| `Oa` | `𞵝𞵱𞵝𞵰󠄯󠅁󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED70 U+E012F U+E0141 U+E01EF | at the start of a word |
| `Oa` | `𞵱𞵝𞵰󠄯󠅁󠇯` | U+1ED71 U+1ED5D U+1ED70 U+E012F U+E0141 U+E01EF | always |
| `OA` | `𞵝𞵱𞵝𞵰󠄯󠄡󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED70 U+E012F U+E0121 U+E01EF | at the start of a word |
| `OA` | `𞵱𞵝𞵰󠄯󠄡󠇯` | U+1ED71 U+1ED5D U+1ED70 U+E012F U+E0121 U+E01EF | always |
| `Oá` | `𞵝𞵱𞵝𞵰󠄯󠅛󠅅󠄑󠅝󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED70 U+E012F U+E015B U+E0145 U+E0111 U+E015D U+E01EF | at the start of a word |
| `Oá` | `𞵱𞵝𞵰󠄯󠅛󠅅󠄑󠅝󠇯` | U+1ED71 U+1ED5D U+1ED70 U+E012F U+E015B U+E0145 U+E0111 U+E015D U+E01EF | always |
| `OÁ` | `𞵝𞵱𞵝𞵰󠄯󠅛󠅃󠄑󠅝󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED70 U+E012F U+E015B U+E0143 U+E0111 U+E015D U+E01EF | at the start of a word |
| `OÁ` | `𞵱𞵝𞵰󠄯󠅛󠅃󠄑󠅝󠇯` | U+1ED71 U+1ED5D U+1ED70 U+E012F U+E015B U+E0143 U+E0111 U+E015D U+E01EF | always |
| `óa` | `𞵝𞵱𞵝𞵰󠅛󠅆󠄓󠅝󠅁󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED70 U+E015B U+E0146 U+E0113 U+E015D U+E0141 U+E01EF | at the start of a word |
| `óa` | `𞵱𞵝𞵰󠅛󠅆󠄓󠅝󠅁󠇯` | U+1ED71 U+1ED5D U+1ED70 U+E015B U+E0146 U+E0113 U+E015D U+E0141 U+E01EF | always |
| `óA` | `𞵝𞵱𞵝𞵰󠅛󠅆󠄓󠅝󠄡󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED70 U+E015B U+E0146 U+E0113 U+E015D U+E0121 U+E01EF | at the start of a word |
| `óA` | `𞵱𞵝𞵰󠅛󠅆󠄓󠅝󠄡󠇯` | U+1ED71 U+1ED5D U+1ED70 U+E015B U+E0146 U+E0113 U+E015D U+E0121 U+E01EF | always |
| `óá` | `𞵝𞵱𞵝𞵰󠅛󠅆󠄓󠅝󠅛󠅅󠄑󠅝󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED70 U+E015B U+E0146 U+E0113 U+E015D U+E015B U+E0145 U+E0111 U+E015D U+E01EF | at the start of a word |
| `óá` | `𞵱𞵝𞵰󠅛󠅆󠄓󠅝󠅛󠅅󠄑󠅝󠇯` | U+1ED71 U+1ED5D U+1ED70 U+E015B U+E0146 U+E0113 U+E015D U+E015B U+E0145 U+E0111 U+E015D U+E01EF | always |
| `óÁ` | `𞵝𞵱𞵝𞵰󠅛󠅆󠄓󠅝󠅛󠅃󠄑󠅝󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED70 U+E015B U+E0146 U+E0113 U+E015D U+E015B U+E0143 U+E0111 U+E015D U+E01EF | at the start of a word |
| `óÁ` | `𞵱𞵝𞵰󠅛󠅆󠄓󠅝󠅛󠅃󠄑󠅝󠇯` | U+1ED71 U+1ED5D U+1ED70 U+E015B U+E0146 U+E0113 U+E015D U+E015B U+E0143 U+E0111 U+E015D U+E01EF | always |
| `Óa` | `𞵝𞵱𞵝𞵰󠅛󠅄󠄓󠅝󠅁󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED70 U+E015B U+E0144 U+E0113 U+E015D U+E0141 U+E01EF | at the start of a word |
| `Óa` | `𞵱𞵝𞵰󠅛󠅄󠄓󠅝󠅁󠇯` | U+1ED71 U+1ED5D U+1ED70 U+E015B U+E0144 U+E0113 U+E015D U+E0141 U+E01EF | always |
| `ÓA` | `𞵝𞵱𞵝𞵰󠅛󠅄󠄓󠅝󠄡󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED70 U+E015B U+E0144 U+E0113 U+E015D U+E0121 U+E01EF | at the start of a word |
| `ÓA` | `𞵱𞵝𞵰󠅛󠅄󠄓󠅝󠄡󠇯` | U+1ED71 U+1ED5D U+1ED70 U+E015B U+E0144 U+E0113 U+E015D U+E0121 U+E01EF | always |
| `Óá` | `𞵝𞵱𞵝𞵰󠅛󠅄󠄓󠅝󠅛󠅅󠄑󠅝󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED70 U+E015B U+E0144 U+E0113 U+E015D U+E015B U+E0145 U+E0111 U+E015D U+E01EF | at the start of a word |
| `Óá` | `𞵱𞵝𞵰󠅛󠅄󠄓󠅝󠅛󠅅󠄑󠅝󠇯` | U+1ED71 U+1ED5D U+1ED70 U+E015B U+E0144 U+E0113 U+E015D U+E015B U+E0145 U+E0111 U+E015D U+E01EF | always |
| `ÓÁ` | `𞵝𞵱𞵝𞵰󠅛󠅄󠄓󠅝󠅛󠅃󠄑󠅝󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED70 U+E015B U+E0144 U+E0113 U+E015D U+E015B U+E0143 U+E0111 U+E015D U+E01EF | at the start of a word |
| `ÓÁ` | `𞵱𞵝𞵰󠅛󠅄󠄓󠅝󠅛󠅃󠄑󠅝󠇯` | U+1ED71 U+1ED5D U+1ED70 U+E015B U+E0144 U+E0113 U+E015D U+E015B U+E0143 U+E0111 U+E015D U+E01EF | always |
| `oe` | `𞵝𞵱𞵝𞵳󠅏󠅅󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED73 U+E014F U+E0145 U+E01EF | at the start of a word |
| `oe` | `𞵱𞵝𞵳󠅏󠅅󠇯` | U+1ED71 U+1ED5D U+1ED73 U+E014F U+E0145 U+E01EF | always |
| `oE` | `𞵝𞵱𞵝𞵳󠅏󠄥󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED73 U+E014F U+E0125 U+E01EF | at the start of a word |
| `oE` | `𞵱𞵝𞵳󠅏󠄥󠇯` | U+1ED71 U+1ED5D U+1ED73 U+E014F U+E0125 U+E01EF | always |
| `oé` | `𞵝𞵱𞵝𞵳󠅏󠅛󠅅󠄙󠅝󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED73 U+E014F U+E015B U+E0145 U+E0119 U+E015D U+E01EF | at the start of a word |
| `oé` | `𞵱𞵝𞵳󠅏󠅛󠅅󠄙󠅝󠇯` | U+1ED71 U+1ED5D U+1ED73 U+E014F U+E015B U+E0145 U+E0119 U+E015D U+E01EF | always |
| `oÉ` | `𞵝𞵱𞵝𞵳󠅏󠅛󠅃󠄙󠅝󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED73 U+E014F U+E015B U+E0143 U+E0119 U+E015D U+E01EF | at the start of a word |
| `oÉ` | `𞵱𞵝𞵳󠅏󠅛󠅃󠄙󠅝󠇯` | U+1ED71 U+1ED5D U+1ED73 U+E014F U+E015B U+E0143 U+E0119 U+E015D U+E01EF | always |
| `Oe` | `𞵝𞵱𞵝𞵳󠄯󠅅󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED73 U+E012F U+E0145 U+E01EF | at the start of a word |
| `Oe` | `𞵱𞵝𞵳󠄯󠅅󠇯` | U+1ED71 U+1ED5D U+1ED73 U+E012F U+E0145 U+E01EF | always |
| `OE` | `𞵝𞵱𞵝𞵳󠄯󠄥󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED73 U+E012F U+E0125 U+E01EF | at the start of a word |
| `OE` | `𞵱𞵝𞵳󠄯󠄥󠇯` | U+1ED71 U+1ED5D U+1ED73 U+E012F U+E0125 U+E01EF | always |
| `Oé` | `𞵝𞵱𞵝𞵳󠄯󠅛󠅅󠄙󠅝󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED73 U+E012F U+E015B U+E0145 U+E0119 U+E015D U+E01EF | at the start of a word |
| `Oé` | `𞵱𞵝𞵳󠄯󠅛󠅅󠄙󠅝󠇯` | U+1ED71 U+1ED5D U+1ED73 U+E012F U+E015B U+E0145 U+E0119 U+E015D U+E01EF | always |
| `OÉ` | `𞵝𞵱𞵝𞵳󠄯󠅛󠅃󠄙󠅝󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED73 U+E012F U+E015B U+E0143 U+E0119 U+E015D U+E01EF | at the start of a word |
| `OÉ` | `𞵱𞵝𞵳󠄯󠅛󠅃󠄙󠅝󠇯` | U+1ED71 U+1ED5D U+1ED73 U+E012F U+E015B U+E0143 U+E0119 U+E015D U+E01EF | always |
| `óe` | `𞵝𞵱𞵝𞵳󠅛󠅆󠄓󠅝󠅅󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED73 U+E015B U+E0146 U+E0113 U+E015D U+E0145 U+E01EF | at the start of a word |
| `óe` | `𞵱𞵝𞵳󠅛󠅆󠄓󠅝󠅅󠇯` | U+1ED71 U+1ED5D U+1ED73 U+E015B U+E0146 U+E0113 U+E015D U+E0145 U+E01EF | always |
| `óE` | `𞵝𞵱𞵝𞵳󠅛󠅆󠄓󠅝󠄥󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED73 U+E015B U+E0146 U+E0113 U+E015D U+E0125 U+E01EF | at the start of a word |
| `óE` | `𞵱𞵝𞵳󠅛󠅆󠄓󠅝󠄥󠇯` | U+1ED71 U+1ED5D U+1ED73 U+E015B U+E0146 U+E0113 U+E015D U+E0125 U+E01EF | always |
| `óé` | `𞵝𞵱𞵝𞵳󠅛󠅆󠄓󠅝󠅛󠅅󠄙󠅝󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED73 U+E015B U+E0146 U+E0113 U+E015D U+E015B U+E0145 U+E0119 U+E015D U+E01EF | at the start of a word |
| `óé` | `𞵱𞵝𞵳󠅛󠅆󠄓󠅝󠅛󠅅󠄙󠅝󠇯` | U+1ED71 U+1ED5D U+1ED73 U+E015B U+E0146 U+E0113 U+E015D U+E015B U+E0145 U+E0119 U+E015D U+E01EF | always |
| `óÉ` | `𞵝𞵱𞵝𞵳󠅛󠅆󠄓󠅝󠅛󠅃󠄙󠅝󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED73 U+E015B U+E0146 U+E0113 U+E015D U+E015B U+E0143 U+E0119 U+E015D U+E01EF | at the start of a word |
| `óÉ` | `𞵱𞵝𞵳󠅛󠅆󠄓󠅝󠅛󠅃󠄙󠅝󠇯` | U+1ED71 U+1ED5D U+1ED73 U+E015B U+E0146 U+E0113 U+E015D U+E015B U+E0143 U+E0119 U+E015D U+E01EF | always |
| `Óe` | `𞵝𞵱𞵝𞵳󠅛󠅄󠄓󠅝󠅅󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED73 U+E015B U+E0144 U+E0113 U+E015D U+E0145 U+E01EF | at the start of a word |
| `Óe` | `𞵱𞵝𞵳󠅛󠅄󠄓󠅝󠅅󠇯` | U+1ED71 U+1ED5D U+1ED73 U+E015B U+E0144 U+E0113 U+E015D U+E0145 U+E01EF | always |
| `ÓE` | `𞵝𞵱𞵝𞵳󠅛󠅄󠄓󠅝󠄥󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED73 U+E015B U+E0144 U+E0113 U+E015D U+E0125 U+E01EF | at the start of a word |
| `ÓE` | `𞵱𞵝𞵳󠅛󠅄󠄓󠅝󠄥󠇯` | U+1ED71 U+1ED5D U+1ED73 U+E015B U+E0144 U+E0113 U+E015D U+E0125 U+E01EF | always |
| `Óé` | `𞵝𞵱𞵝𞵳󠅛󠅄󠄓󠅝󠅛󠅅󠄙󠅝󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED73 U+E015B U+E0144 U+E0113 U+E015D U+E015B U+E0145 U+E0119 U+E015D U+E01EF | at the start of a word |
| `Óé` | `𞵱𞵝𞵳󠅛󠅄󠄓󠅝󠅛󠅅󠄙󠅝󠇯` | U+1ED71 U+1ED5D U+1ED73 U+E015B U+E0144 U+E0113 U+E015D U+E015B U+E0145 U+E0119 U+E015D U+E01EF | always |
| `ÓÉ` | `𞵝𞵱𞵝𞵳󠅛󠅄󠄓󠅝󠅛󠅃󠄙󠅝󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED73 U+E015B U+E0144 U+E0113 U+E015D U+E015B U+E0143 U+E0119 U+E015D U+E01EF | at the start of a word |
| `ÓÉ` | `𞵱𞵝𞵳󠅛󠅄󠄓󠅝󠅛󠅃󠄙󠅝󠇯` | U+1ED71 U+1ED5D U+1ED73 U+E015B U+E0144 U+E0113 U+E015D U+E015B U+E0143 U+E0119 U+E015D U+E01EF | always |
| `oo` | `𞵝𞵱𞵸` | U+1ED5D U+1ED71 U+1ED78 | at the start of a word |
| `oo` | `𞵱𞵸` | U+1ED71 U+1ED78 | always |
| `oO` | `𞵝𞵱𞵸󠅏󠄯󠇯` | U+1ED5D U+1ED71 U+1ED78 U+E014F U+E012F U+E01EF | at the start of a word |
| `oO` | `𞵱𞵸󠅏󠄯󠇯` | U+1ED71 U+1ED78 U+E014F U+E012F U+E01EF | always |
| `oó` | `𞵝𞵱𞵸󠅏󠅛󠅆󠄓󠅝󠇯` | U+1ED5D U+1ED71 U+1ED78 U+E014F U+E015B U+E0146 U+E0113 U+E015D U+E01EF | at the start of a word |
| `oó` | `𞵱𞵸󠅏󠅛󠅆󠄓󠅝󠇯` | U+1ED71 U+1ED78 U+E014F U+E015B U+E0146 U+E0113 U+E015D U+E01EF | always |
| `oÓ` | `𞵝𞵱𞵸󠅏󠅛󠅄󠄓󠅝󠇯` | U+1ED5D U+1ED71 U+1ED78 U+E014F U+E015B U+E0144 U+E0113 U+E015D U+E01EF | at the start of a word |
| `oÓ` | `𞵱𞵸󠅏󠅛󠅄󠄓󠅝󠇯` | U+1ED71 U+1ED78 U+E014F U+E015B U+E0144 U+E0113 U+E015D U+E01EF | always |
| `Oo` | `𞵝𞵱𞵸󠄯󠅏󠇯` | U+1ED5D U+1ED71 U+1ED78 U+E012F U+E014F U+E01EF | at the start of a word |
| `Oo` | `𞵱𞵸󠄯󠅏󠇯` | U+1ED71 U+1ED78 U+E012F U+E014F U+E01EF | always |
| `OO` | `𞵝𞵱𞵸󠄯󠄯󠇯` | U+1ED5D U+1ED71 U+1ED78 U+E012F U+E012F U+E01EF | at the start of a word |
| `OO` | `𞵱𞵸󠄯󠄯󠇯` | U+1ED71 U+1ED78 U+E012F U+E012F U+E01EF | always |
| `Oó` | `𞵝𞵱𞵸󠄯󠅛󠅆󠄓󠅝󠇯` | U+1ED5D U+1ED71 U+1ED78 U+E012F U+E015B U+E0146 U+E0113 U+E015D U+E01EF | at the start of a word |
| `Oó` | `𞵱𞵸󠄯󠅛󠅆󠄓󠅝󠇯` | U+1ED71 U+1ED78 U+E012F U+E015B U+E0146 U+E0113 U+E015D U+E01EF | always |
| `OÓ` | `𞵝𞵱𞵸󠄯󠅛󠅄󠄓󠅝󠇯` | U+1ED5D U+1ED71 U+1ED78 U+E012F U+E015B U+E0144 U+E0113 U+E015D U+E01EF | at the start of a word |
| `OÓ` | `𞵱𞵸󠄯󠅛󠅄󠄓󠅝󠇯` | U+1ED71 U+1ED78 U+E012F U+E015B U+E0144 U+E0113 U+E015D U+E01EF | always |
| `óo` | `𞵝𞵱𞵸󠅛󠅆󠄓󠅝󠅏󠇯` | U+1ED5D U+1ED71 U+1ED78 U+E015B U+E0146 U+E0113 U+E015D U+E014F U+E01EF | at the start of a word |
| `óo` | `𞵱𞵸󠅛󠅆󠄓󠅝󠅏󠇯` | U+1ED71 U+1ED78 U+E015B U+E0146 U+E0113 U+E015D U+E014F U+E01EF | always |
| `óO` | `𞵝𞵱𞵸󠅛󠅆󠄓󠅝󠄯󠇯` | U+1ED5D U+1ED71 U+1ED78 U+E015B U+E0146 U+E0113 U+E015D U+E012F U+E01EF | at the start of a word |
| `óO` | `𞵱𞵸󠅛󠅆󠄓󠅝󠄯󠇯` | U+1ED71 U+1ED78 U+E015B U+E0146 U+E0113 U+E015D U+E012F U+E01EF | always |
| `óó` | `𞵝𞵱𞵸󠅛󠅆󠄓󠅝󠅛󠅆󠄓󠅝󠇯` | U+1ED5D U+1ED71 U+1ED78 U+E015B U+E0146 U+E0113 U+E015D U+E015B U+E0146 U+E0113 U+E015D U+E01EF | at the start of a word |
| `óó` | `𞵱𞵸󠅛󠅆󠄓󠅝󠅛󠅆󠄓󠅝󠇯` | U+1ED71 U+1ED78 U+E015B U+E0146 U+E0113 U+E015D U+E015B U+E0146 U+E0113 U+E015D U+E01EF | always |
| `óÓ` | `𞵝𞵱𞵸󠅛󠅆󠄓󠅝󠅛󠅄󠄓󠅝󠇯` | U+1ED5D U+1ED71 U+1ED78 U+E015B U+E0146 U+E0113 U+E015D U+E015B U+E0144 U+E0113 U+E015D U+E01EF | at the start of a word |
| `óÓ` | `𞵱𞵸󠅛󠅆󠄓󠅝󠅛󠅄󠄓󠅝󠇯` | U+1ED71 U+1ED78 U+E015B U+E0146 U+E0113 U+E015D U+E015B U+E0144 U+E0113 U+E015D U+E01EF | always |
| `Óo` | `𞵝𞵱𞵸󠅛󠅄󠄓󠅝󠅏󠇯` | U+1ED5D U+1ED71 U+1ED78 U+E015B U+E0144 U+E0113 U+E015D U+E014F U+E01EF | at the start of a word |
| `Óo` | `𞵱𞵸󠅛󠅄󠄓󠅝󠅏󠇯` | U+1ED71 U+1ED78 U+E015B U+E0144 U+E0113 U+E015D U+E014F U+E01EF | always |
| `ÓO` | `𞵝𞵱𞵸󠅛󠅄󠄓󠅝󠄯󠇯` | U+1ED5D U+1ED71 U+1ED78 U+E015B U+E0144 U+E0113 U+E015D U+E012F U+E01EF | at the start of a word |
| `ÓO` | `𞵱𞵸󠅛󠅄󠄓󠅝󠄯󠇯` | U+1ED71 U+1ED78 U+E015B U+E0144 U+E0113 U+E015D U+E012F U+E01EF | always |
| `Óó` | `𞵝𞵱𞵸󠅛󠅄󠄓󠅝󠅛󠅆󠄓󠅝󠇯` | U+1ED5D U+1ED71 U+1ED78 U+E015B U+E0144 U+E0113 U+E015D U+E015B U+E0146 U+E0113 U+E015D U+E01EF | at the start of a word |
| `Óó` | `𞵱𞵸󠅛󠅄󠄓󠅝󠅛󠅆󠄓󠅝󠇯` | U+1ED71 U+1ED78 U+E015B U+E0144 U+E0113 U+E015D U+E015B U+E0146 U+E0113 U+E015D U+E01EF | always |
| `ÓÓ` | `𞵝𞵱𞵸󠅛󠅄󠄓󠅝󠅛󠅄󠄓󠅝󠇯` | U+1ED5D U+1ED71 U+1ED78 U+E015B U+E0144 U+E0113 U+E015D U+E015B U+E0144 U+E0113 U+E015D U+E01EF | at the start of a word |
| `ÓÓ` | `𞵱𞵸󠅛󠅄󠄓󠅝󠅛󠅄󠄓󠅝󠇯` | U+1ED71 U+1ED78 U+E015B U+E0144 U+E0113 U+E015D U+E015B U+E0144 U+E0113 U+E015D U+E01EF | always |
| `oy` | `𞵝𞵱𞵝𞵵󠅏󠅙󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED75 U+E014F U+E0159 U+E01EF | at the start of a word |
| `oy` | `𞵱𞵝𞵵󠅏󠅙󠇯` | U+1ED71 U+1ED5D U+1ED75 U+E014F U+E0159 U+E01EF | always |
| `oY` | `𞵝𞵱𞵝𞵵󠅏󠄹󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED75 U+E014F U+E0139 U+E01EF | at the start of a word |
| `oY` | `𞵱𞵝𞵵󠅏󠄹󠇯` | U+1ED71 U+1ED5D U+1ED75 U+E014F U+E0139 U+E01EF | always |
| `oý` | `𞵝𞵱𞵝𞵵󠅏󠅛󠅆󠅄󠅝󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED75 U+E014F U+E015B U+E0146 U+E0144 U+E015D U+E01EF | at the start of a word |
| `oý` | `𞵱𞵝𞵵󠅏󠅛󠅆󠅄󠅝󠇯` | U+1ED71 U+1ED5D U+1ED75 U+E014F U+E015B U+E0146 U+E0144 U+E015D U+E01EF | always |
| `oÝ` | `𞵝𞵱𞵝𞵵󠅏󠅛󠅄󠅄󠅝󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED75 U+E014F U+E015B U+E0144 U+E0144 U+E015D U+E01EF | at the start of a word |
| `oÝ` | `𞵱𞵝𞵵󠅏󠅛󠅄󠅄󠅝󠇯` | U+1ED71 U+1ED5D U+1ED75 U+E014F U+E015B U+E0144 U+E0144 U+E015D U+E01EF | always |
| `Oy` | `𞵝𞵱𞵝𞵵󠄯󠅙󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED75 U+E012F U+E0159 U+E01EF | at the start of a word |
| `Oy` | `𞵱𞵝𞵵󠄯󠅙󠇯` | U+1ED71 U+1ED5D U+1ED75 U+E012F U+E0159 U+E01EF | always |
| `OY` | `𞵝𞵱𞵝𞵵󠄯󠄹󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED75 U+E012F U+E0139 U+E01EF | at the start of a word |
| `OY` | `𞵱𞵝𞵵󠄯󠄹󠇯` | U+1ED71 U+1ED5D U+1ED75 U+E012F U+E0139 U+E01EF | always |
| `Oý` | `𞵝𞵱𞵝𞵵󠄯󠅛󠅆󠅄󠅝󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED75 U+E012F U+E015B U+E0146 U+E0144 U+E015D U+E01EF | at the start of a word |
| `Oý` | `𞵱𞵝𞵵󠄯󠅛󠅆󠅄󠅝󠇯` | U+1ED71 U+1ED5D U+1ED75 U+E012F U+E015B U+E0146 U+E0144 U+E015D U+E01EF | always |
| `OÝ` | `𞵝𞵱𞵝𞵵󠄯󠅛󠅄󠅄󠅝󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED75 U+E012F U+E015B U+E0144 U+E0144 U+E015D U+E01EF | at the start of a word |
| `OÝ` | `𞵱𞵝𞵵󠄯󠅛󠅄󠅄󠅝󠇯` | U+1ED71 U+1ED5D U+1ED75 U+E012F U+E015B U+E0144 U+E0144 U+E015D U+E01EF | always |
| `óy` | `𞵝𞵱𞵝𞵵󠅛󠅆󠄓󠅝󠅙󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED75 U+E015B U+E0146 U+E0113 U+E015D U+E0159 U+E01EF | at the start of a word |
| `óy` | `𞵱𞵝𞵵󠅛󠅆󠄓󠅝󠅙󠇯` | U+1ED71 U+1ED5D U+1ED75 U+E015B U+E0146 U+E0113 U+E015D U+E0159 U+E01EF | always |
| `óY` | `𞵝𞵱𞵝𞵵󠅛󠅆󠄓󠅝󠄹󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED75 U+E015B U+E0146 U+E0113 U+E015D U+E0139 U+E01EF | at the start of a word |
| `óY` | `𞵱𞵝𞵵󠅛󠅆󠄓󠅝󠄹󠇯` | U+1ED71 U+1ED5D U+1ED75 U+E015B U+E0146 U+E0113 U+E015D U+E0139 U+E01EF | always |
| `óý` | `𞵝𞵱𞵝𞵵󠅛󠅆󠄓󠅝󠅛󠅆󠅄󠅝󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED75 U+E015B U+E0146 U+E0113 U+E015D U+E015B U+E0146 U+E0144 U+E015D U+E01EF | at the start of a word |
| `óý` | `𞵱𞵝𞵵󠅛󠅆󠄓󠅝󠅛󠅆󠅄󠅝󠇯` | U+1ED71 U+1ED5D U+1ED75 U+E015B U+E0146 U+E0113 U+E015D U+E015B U+E0146 U+E0144 U+E015D U+E01EF | always |
| `óÝ` | `𞵝𞵱𞵝𞵵󠅛󠅆󠄓󠅝󠅛󠅄󠅄󠅝󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED75 U+E015B U+E0146 U+E0113 U+E015D U+E015B U+E0144 U+E0144 U+E015D U+E01EF | at the start of a word |
| `óÝ` | `𞵱𞵝𞵵󠅛󠅆󠄓󠅝󠅛󠅄󠅄󠅝󠇯` | U+1ED71 U+1ED5D U+1ED75 U+E015B U+E0146 U+E0113 U+E015D U+E015B U+E0144 U+E0144 U+E015D U+E01EF | always |
| `Óy` | `𞵝𞵱𞵝𞵵󠅛󠅄󠄓󠅝󠅙󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED75 U+E015B U+E0144 U+E0113 U+E015D U+E0159 U+E01EF | at the start of a word |
| `Óy` | `𞵱𞵝𞵵󠅛󠅄󠄓󠅝󠅙󠇯` | U+1ED71 U+1ED5D U+1ED75 U+E015B U+E0144 U+E0113 U+E015D U+E0159 U+E01EF | always |
| `ÓY` | `𞵝𞵱𞵝𞵵󠅛󠅄󠄓󠅝󠄹󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED75 U+E015B U+E0144 U+E0113 U+E015D U+E0139 U+E01EF | at the start of a word |
| `ÓY` | `𞵱𞵝𞵵󠅛󠅄󠄓󠅝󠄹󠇯` | U+1ED71 U+1ED5D U+1ED75 U+E015B U+E0144 U+E0113 U+E015D U+E0139 U+E01EF | always |
| `Óý` | `𞵝𞵱𞵝𞵵󠅛󠅄󠄓󠅝󠅛󠅆󠅄󠅝󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED75 U+E015B U+E0144 U+E0113 U+E015D U+E015B U+E0146 U+E0144 U+E015D U+E01EF | at the start of a word |
| `Óý` | `𞵱𞵝𞵵󠅛󠅄󠄓󠅝󠅛󠅆󠅄󠅝󠇯` | U+1ED71 U+1ED5D U+1ED75 U+E015B U+E0144 U+E0113 U+E015D U+E015B U+E0146 U+E0144 U+E015D U+E01EF | always |
| `ÓÝ` | `𞵝𞵱𞵝𞵵󠅛󠅄󠄓󠅝󠅛󠅄󠅄󠅝󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED75 U+E015B U+E0144 U+E0113 U+E015D U+E015B U+E0144 U+E0144 U+E015D U+E01EF | at the start of a word |
| `ÓÝ` | `𞵱𞵝𞵵󠅛󠅄󠄓󠅝󠅛󠅄󠅄󠅝󠇯` | U+1ED71 U+1ED5D U+1ED75 U+E015B U+E0144 U+E0113 U+E015D U+E015B U+E0144 U+E0144 U+E015D U+E01EF | always |
| `oë` | `𞵝𞵱𞵝𞵶󠅏󠅛󠅅󠅂󠅝󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED76 U+E014F U+E015B U+E0145 U+E0142 U+E015D U+E01EF | at the start of a word |
| `oë` | `𞵱𞵝𞵶󠅏󠅛󠅅󠅂󠅝󠇯` | U+1ED71 U+1ED5D U+1ED76 U+E014F U+E015B U+E0145 U+E0142 U+E015D U+E01EF | always |
| `oË` | `𞵝𞵱𞵝𞵶󠅏󠅛󠅃󠅂󠅝󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED76 U+E014F U+E015B U+E0143 U+E0142 U+E015D U+E01EF | at the start of a word |
| `oË` | `𞵱𞵝𞵶󠅏󠅛󠅃󠅂󠅝󠇯` | U+1ED71 U+1ED5D U+1ED76 U+E014F U+E015B U+E0143 U+E0142 U+E015D U+E01EF | always |
| `Oë` | `𞵝𞵱𞵝𞵶󠄯󠅛󠅅󠅂󠅝󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED76 U+E012F U+E015B U+E0145 U+E0142 U+E015D U+E01EF | at the start of a word |
| `Oë` | `𞵱𞵝𞵶󠄯󠅛󠅅󠅂󠅝󠇯` | U+1ED71 U+1ED5D U+1ED76 U+E012F U+E015B U+E0145 U+E0142 U+E015D U+E01EF | always |
| `OË` | `𞵝𞵱𞵝𞵶󠄯󠅛󠅃󠅂󠅝󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED76 U+E012F U+E015B U+E0143 U+E0142 U+E015D U+E01EF | at the start of a word |
| `OË` | `𞵱𞵝𞵶󠄯󠅛󠅃󠅂󠅝󠇯` | U+1ED71 U+1ED5D U+1ED76 U+E012F U+E015B U+E0143 U+E0142 U+E015D U+E01EF | always |
| `óë` | `𞵝𞵱𞵝𞵶󠅛󠅆󠄓󠅝󠅛󠅅󠅂󠅝󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED76 U+E015B U+E0146 U+E0113 U+E015D U+E015B U+E0145 U+E0142 U+E015D U+E01EF | at the start of a word |
| `óë` | `𞵱𞵝𞵶󠅛󠅆󠄓󠅝󠅛󠅅󠅂󠅝󠇯` | U+1ED71 U+1ED5D U+1ED76 U+E015B U+E0146 U+E0113 U+E015D U+E015B U+E0145 U+E0142 U+E015D U+E01EF | always |
| `óË` | `𞵝𞵱𞵝𞵶󠅛󠅆󠄓󠅝󠅛󠅃󠅂󠅝󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED76 U+E015B U+E0146 U+E0113 U+E015D U+E015B U+E0143 U+E0142 U+E015D U+E01EF | at the start of a word |
| `óË` | `𞵱𞵝𞵶󠅛󠅆󠄓󠅝󠅛󠅃󠅂󠅝󠇯` | U+1ED71 U+1ED5D U+1ED76 U+E015B U+E0146 U+E0113 U+E015D U+E015B U+E0143 U+E0142 U+E015D U+E01EF | always |
| `Óë` | `𞵝𞵱𞵝𞵶󠅛󠅄󠄓󠅝󠅛󠅅󠅂󠅝󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED76 U+E015B U+E0144 U+E0113 U+E015D U+E015B U+E0145 U+E0142 U+E015D U+E01EF | at the start of a word |
| `Óë` | `𞵱𞵝𞵶󠅛󠅄󠄓󠅝󠅛󠅅󠅂󠅝󠇯` | U+1ED71 U+1ED5D U+1ED76 U+E015B U+E0144 U+E0113 U+E015D U+E015B U+E0145 U+E0142 U+E015D U+E01EF | always |
| `ÓË` | `𞵝𞵱𞵝𞵶󠅛󠅄󠄓󠅝󠅛󠅃󠅂󠅝󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED76 U+E015B U+E0144 U+E0113 U+E015D U+E015B U+E0143 U+E0142 U+E015D U+E01EF | at the start of a word |
| `ÓË` | `𞵱𞵝𞵶󠅛󠅄󠄓󠅝󠅛󠅃󠅂󠅝󠇯` | U+1ED71 U+1ED5D U+1ED76 U+E015B U+E0144 U+E0113 U+E015D U+E015B U+E0143 U+E0142 U+E015D U+E01EF | always |
| `ua` | `𞵝𞵲𞵝𞵰󠅕󠅁󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED70 U+E0155 U+E0141 U+E01EF | at the start of a word |
| `ua` | `𞵲𞵝𞵰󠅕󠅁󠇯` | U+1ED72 U+1ED5D U+1ED70 U+E0155 U+E0141 U+E01EF | always |
| `uA` | `𞵝𞵲𞵝𞵰󠅕󠄡󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED70 U+E0155 U+E0121 U+E01EF | at the start of a word |
| `uA` | `𞵲𞵝𞵰󠅕󠄡󠇯` | U+1ED72 U+1ED5D U+1ED70 U+E0155 U+E0121 U+E01EF | always |
| `uá` | `𞵝𞵲𞵝𞵰󠅕󠅛󠅅󠄑󠅝󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED70 U+E0155 U+E015B U+E0145 U+E0111 U+E015D U+E01EF | at the start of a word |
| `uá` | `𞵲𞵝𞵰󠅕󠅛󠅅󠄑󠅝󠇯` | U+1ED72 U+1ED5D U+1ED70 U+E0155 U+E015B U+E0145 U+E0111 U+E015D U+E01EF | always |
| `uÁ` | `𞵝𞵲𞵝𞵰󠅕󠅛󠅃󠄑󠅝󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED70 U+E0155 U+E015B U+E0143 U+E0111 U+E015D U+E01EF | at the start of a word |
| `uÁ` | `𞵲𞵝𞵰󠅕󠅛󠅃󠄑󠅝󠇯` | U+1ED72 U+1ED5D U+1ED70 U+E0155 U+E015B U+E0143 U+E0111 U+E015D U+E01EF | always |
| `Ua` | `𞵝𞵲𞵝𞵰󠄵󠅁󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED70 U+E0135 U+E0141 U+E01EF | at the start of a word |
| `Ua` | `𞵲𞵝𞵰󠄵󠅁󠇯` | U+1ED72 U+1ED5D U+1ED70 U+E0135 U+E0141 U+E01EF | always |
| `UA` | `𞵝𞵲𞵝𞵰󠄵󠄡󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED70 U+E0135 U+E0121 U+E01EF | at the start of a word |
| `UA` | `𞵲𞵝𞵰󠄵󠄡󠇯` | U+1ED72 U+1ED5D U+1ED70 U+E0135 U+E0121 U+E01EF | always |
| `Uá` | `𞵝𞵲𞵝𞵰󠄵󠅛󠅅󠄑󠅝󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED70 U+E0135 U+E015B U+E0145 U+E0111 U+E015D U+E01EF | at the start of a word |
| `Uá` | `𞵲𞵝𞵰󠄵󠅛󠅅󠄑󠅝󠇯` | U+1ED72 U+1ED5D U+1ED70 U+E0135 U+E015B U+E0145 U+E0111 U+E015D U+E01EF | always |
| `UÁ` | `𞵝𞵲𞵝𞵰󠄵󠅛󠅃󠄑󠅝󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED70 U+E0135 U+E015B U+E0143 U+E0111 U+E015D U+E01EF | at the start of a word |
| `UÁ` | `𞵲𞵝𞵰󠄵󠅛󠅃󠄑󠅝󠇯` | U+1ED72 U+1ED5D U+1ED70 U+E0135 U+E015B U+E0143 U+E0111 U+E015D U+E01EF | always |
| `úa` | `𞵝𞵲𞵝𞵰󠅛󠅆󠅁󠅝󠅁󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED70 U+E015B U+E0146 U+E0141 U+E015D U+E0141 U+E01EF | at the start of a word |
| `úa` | `𞵲𞵝𞵰󠅛󠅆󠅁󠅝󠅁󠇯` | U+1ED72 U+1ED5D U+1ED70 U+E015B U+E0146 U+E0141 U+E015D U+E0141 U+E01EF | always |
| `úA` | `𞵝𞵲𞵝𞵰󠅛󠅆󠅁󠅝󠄡󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED70 U+E015B U+E0146 U+E0141 U+E015D U+E0121 U+E01EF | at the start of a word |
| `úA` | `𞵲𞵝𞵰󠅛󠅆󠅁󠅝󠄡󠇯` | U+1ED72 U+1ED5D U+1ED70 U+E015B U+E0146 U+E0141 U+E015D U+E0121 U+E01EF | always |
| `úá` | `𞵝𞵲𞵝𞵰󠅛󠅆󠅁󠅝󠅛󠅅󠄑󠅝󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED70 U+E015B U+E0146 U+E0141 U+E015D U+E015B U+E0145 U+E0111 U+E015D U+E01EF | at the start of a word |
| `úá` | `𞵲𞵝𞵰󠅛󠅆󠅁󠅝󠅛󠅅󠄑󠅝󠇯` | U+1ED72 U+1ED5D U+1ED70 U+E015B U+E0146 U+E0141 U+E015D U+E015B U+E0145 U+E0111 U+E015D U+E01EF | always |
| `úÁ` | `𞵝𞵲𞵝𞵰󠅛󠅆󠅁󠅝󠅛󠅃󠄑󠅝󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED70 U+E015B U+E0146 U+E0141 U+E015D U+E015B U+E0143 U+E0111 U+E015D U+E01EF | at the start of a word |
| `úÁ` | `𞵲𞵝𞵰󠅛󠅆󠅁󠅝󠅛󠅃󠄑󠅝󠇯` | U+1ED72 U+1ED5D U+1ED70 U+E015B U+E0146 U+E0141 U+E015D U+E015B U+E0143 U+E0111 U+E015D U+E01EF | always |
| `Úa` | `𞵝𞵲𞵝𞵰󠅛󠅄󠅁󠅝󠅁󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED70 U+E015B U+E0144 U+E0141 U+E015D U+E0141 U+E01EF | at the start of a word |
| `Úa` | `𞵲𞵝𞵰󠅛󠅄󠅁󠅝󠅁󠇯` | U+1ED72 U+1ED5D U+1ED70 U+E015B U+E0144 U+E0141 U+E015D U+E0141 U+E01EF | always |
| `ÚA` | `𞵝𞵲𞵝𞵰󠅛󠅄󠅁󠅝󠄡󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED70 U+E015B U+E0144 U+E0141 U+E015D U+E0121 U+E01EF | at the start of a word |
| `ÚA` | `𞵲𞵝𞵰󠅛󠅄󠅁󠅝󠄡󠇯` | U+1ED72 U+1ED5D U+1ED70 U+E015B U+E0144 U+E0141 U+E015D U+E0121 U+E01EF | always |
| `Úá` | `𞵝𞵲𞵝𞵰󠅛󠅄󠅁󠅝󠅛󠅅󠄑󠅝󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED70 U+E015B U+E0144 U+E0141 U+E015D U+E015B U+E0145 U+E0111 U+E015D U+E01EF | at the start of a word |
| `Úá` | `𞵲𞵝𞵰󠅛󠅄󠅁󠅝󠅛󠅅󠄑󠅝󠇯` | U+1ED72 U+1ED5D U+1ED70 U+E015B U+E0144 U+E0141 U+E015D U+E015B U+E0145 U+E0111 U+E015D U+E01EF | always |
| `ÚÁ` | `𞵝𞵲𞵝𞵰󠅛󠅄󠅁󠅝󠅛󠅃󠄑󠅝󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED70 U+E015B U+E0144 U+E0141 U+E015D U+E015B U+E0143 U+E0111 U+E015D U+E01EF | at the start of a word |
| `ÚÁ` | `𞵲𞵝𞵰󠅛󠅄󠅁󠅝󠅛󠅃󠄑󠅝󠇯` | U+1ED72 U+1ED5D U+1ED70 U+E015B U+E0144 U+E0141 U+E015D U+E015B U+E0143 U+E0111 U+E015D U+E01EF | always |
| `ue` | `𞵝𞵲𞵝𞵳󠅕󠅅󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED73 U+E0155 U+E0145 U+E01EF | at the start of a word |
| `ue` | `𞵲𞵝𞵳󠅕󠅅󠇯` | U+1ED72 U+1ED5D U+1ED73 U+E0155 U+E0145 U+E01EF | always |
| `uE` | `𞵝𞵲𞵝𞵳󠅕󠄥󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED73 U+E0155 U+E0125 U+E01EF | at the start of a word |
| `uE` | `𞵲𞵝𞵳󠅕󠄥󠇯` | U+1ED72 U+1ED5D U+1ED73 U+E0155 U+E0125 U+E01EF | always |
| `ué` | `𞵝𞵲𞵝𞵳󠅕󠅛󠅅󠄙󠅝󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED73 U+E0155 U+E015B U+E0145 U+E0119 U+E015D U+E01EF | at the start of a word |
| `ué` | `𞵲𞵝𞵳󠅕󠅛󠅅󠄙󠅝󠇯` | U+1ED72 U+1ED5D U+1ED73 U+E0155 U+E015B U+E0145 U+E0119 U+E015D U+E01EF | always |
| `uÉ` | `𞵝𞵲𞵝𞵳󠅕󠅛󠅃󠄙󠅝󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED73 U+E0155 U+E015B U+E0143 U+E0119 U+E015D U+E01EF | at the start of a word |
| `uÉ` | `𞵲𞵝𞵳󠅕󠅛󠅃󠄙󠅝󠇯` | U+1ED72 U+1ED5D U+1ED73 U+E0155 U+E015B U+E0143 U+E0119 U+E015D U+E01EF | always |
| `Ue` | `𞵝𞵲𞵝𞵳󠄵󠅅󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED73 U+E0135 U+E0145 U+E01EF | at the start of a word |
| `Ue` | `𞵲𞵝𞵳󠄵󠅅󠇯` | U+1ED72 U+1ED5D U+1ED73 U+E0135 U+E0145 U+E01EF | always |
| `UE` | `𞵝𞵲𞵝𞵳󠄵󠄥󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED73 U+E0135 U+E0125 U+E01EF | at the start of a word |
| `UE` | `𞵲𞵝𞵳󠄵󠄥󠇯` | U+1ED72 U+1ED5D U+1ED73 U+E0135 U+E0125 U+E01EF | always |
| `Ué` | `𞵝𞵲𞵝𞵳󠄵󠅛󠅅󠄙󠅝󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED73 U+E0135 U+E015B U+E0145 U+E0119 U+E015D U+E01EF | at the start of a word |
| `Ué` | `𞵲𞵝𞵳󠄵󠅛󠅅󠄙󠅝󠇯` | U+1ED72 U+1ED5D U+1ED73 U+E0135 U+E015B U+E0145 U+E0119 U+E015D U+E01EF | always |
| `UÉ` | `𞵝𞵲𞵝𞵳󠄵󠅛󠅃󠄙󠅝󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED73 U+E0135 U+E015B U+E0143 U+E0119 U+E015D U+E01EF | at the start of a word |
| `UÉ` | `𞵲𞵝𞵳󠄵󠅛󠅃󠄙󠅝󠇯` | U+1ED72 U+1ED5D U+1ED73 U+E0135 U+E015B U+E0143 U+E0119 U+E015D U+E01EF | always |
| `úe` | `𞵝𞵲𞵝𞵳󠅛󠅆󠅁󠅝󠅅󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED73 U+E015B U+E0146 U+E0141 U+E015D U+E0145 U+E01EF | at the start of a word |
| `úe` | `𞵲𞵝𞵳󠅛󠅆󠅁󠅝󠅅󠇯` | U+1ED72 U+1ED5D U+1ED73 U+E015B U+E0146 U+E0141 U+E015D U+E0145 U+E01EF | always |
| `úE` | `𞵝𞵲𞵝𞵳󠅛󠅆󠅁󠅝󠄥󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED73 U+E015B U+E0146 U+E0141 U+E015D U+E0125 U+E01EF | at the start of a word |
| `úE` | `𞵲𞵝𞵳󠅛󠅆󠅁󠅝󠄥󠇯` | U+1ED72 U+1ED5D U+1ED73 U+E015B U+E0146 U+E0141 U+E015D U+E0125 U+E01EF | always |
| `úé` | `𞵝𞵲𞵝𞵳󠅛󠅆󠅁󠅝󠅛󠅅󠄙󠅝󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED73 U+E015B U+E0146 U+E0141 U+E015D U+E015B U+E0145 U+E0119 U+E015D U+E01EF | at the start of a word |
| `úé` | `𞵲𞵝𞵳󠅛󠅆󠅁󠅝󠅛󠅅󠄙󠅝󠇯` | U+1ED72 U+1ED5D U+1ED73 U+E015B U+E0146 U+E0141 U+E015D U+E015B U+E0145 U+E0119 U+E015D U+E01EF | always |
| `úÉ` | `𞵝𞵲𞵝𞵳󠅛󠅆󠅁󠅝󠅛󠅃󠄙󠅝󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED73 U+E015B U+E0146 U+E0141 U+E015D U+E015B U+E0143 U+E0119 U+E015D U+E01EF | at the start of a word |
| `úÉ` | `𞵲𞵝𞵳󠅛󠅆󠅁󠅝󠅛󠅃󠄙󠅝󠇯` | U+1ED72 U+1ED5D U+1ED73 U+E015B U+E0146 U+E0141 U+E015D U+E015B U+E0143 U+E0119 U+E015D U+E01EF | always |
| `Úe` | `𞵝𞵲𞵝𞵳󠅛󠅄󠅁󠅝󠅅󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED73 U+E015B U+E0144 U+E0141 U+E015D U+E0145 U+E01EF | at the start of a word |
| `Úe` | `𞵲𞵝𞵳󠅛󠅄󠅁󠅝󠅅󠇯` | U+1ED72 U+1ED5D U+1ED73 U+E015B U+E0144 U+E0141 U+E015D U+E0145 U+E01EF | always |
| `ÚE` | `𞵝𞵲𞵝𞵳󠅛󠅄󠅁󠅝󠄥󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED73 U+E015B U+E0144 U+E0141 U+E015D U+E0125 U+E01EF | at the start of a word |
| `ÚE` | `𞵲𞵝𞵳󠅛󠅄󠅁󠅝󠄥󠇯` | U+1ED72 U+1ED5D U+1ED73 U+E015B U+E0144 U+E0141 U+E015D U+E0125 U+E01EF | always |
| `Úé` | `𞵝𞵲𞵝𞵳󠅛󠅄󠅁󠅝󠅛󠅅󠄙󠅝󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED73 U+E015B U+E0144 U+E0141 U+E015D U+E015B U+E0145 U+E0119 U+E015D U+E01EF | at the start of a word |
| `Úé` | `𞵲𞵝𞵳󠅛󠅄󠅁󠅝󠅛󠅅󠄙󠅝󠇯` | U+1ED72 U+1ED5D U+1ED73 U+E015B U+E0144 U+E0141 U+E015D U+E015B U+E0145 U+E0119 U+E015D U+E01EF | always |
| `ÚÉ` | `𞵝𞵲𞵝𞵳󠅛󠅄󠅁󠅝󠅛󠅃󠄙󠅝󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED73 U+E015B U+E0144 U+E0141 U+E015D U+E015B U+E0143 U+E0119 U+E015D U+E01EF | at the start of a word |
| `ÚÉ` | `𞵲𞵝𞵳󠅛󠅄󠅁󠅝󠅛󠅃󠄙󠅝󠇯` | U+1ED72 U+1ED5D U+1ED73 U+E015B U+E0144 U+E0141 U+E015D U+E015B U+E0143 U+E0119 U+E015D U+E01EF | always |
| `uu` | `𞵝𞵲𞵸` | U+1ED5D U+1ED72 U+1ED78 | at the start of a word |
| `uu` | `𞵲𞵸` | U+1ED72 U+1ED78 | always |
| `uU` | `𞵝𞵲𞵸󠅕󠄵󠇯` | U+1ED5D U+1ED72 U+1ED78 U+E0155 U+E0135 U+E01EF | at the start of a word |
| `uU` | `𞵲𞵸󠅕󠄵󠇯` | U+1ED72 U+1ED78 U+E0155 U+E0135 U+E01EF | always |
| `uú` | `𞵝𞵲𞵸󠅕󠅛󠅆󠅁󠅝󠇯` | U+1ED5D U+1ED72 U+1ED78 U+E0155 U+E015B U+E0146 U+E0141 U+E015D U+E01EF | at the start of a word |
| `uú` | `𞵲𞵸󠅕󠅛󠅆󠅁󠅝󠇯` | U+1ED72 U+1ED78 U+E0155 U+E015B U+E0146 U+E0141 U+E015D U+E01EF | always |
| `uÚ` | `𞵝𞵲𞵸󠅕󠅛󠅄󠅁󠅝󠇯` | U+1ED5D U+1ED72 U+1ED78 U+E0155 U+E015B U+E0144 U+E0141 U+E015D U+E01EF | at the start of a word |
| `uÚ` | `𞵲𞵸󠅕󠅛󠅄󠅁󠅝󠇯` | U+1ED72 U+1ED78 U+E0155 U+E015B U+E0144 U+E0141 U+E015D U+E01EF | always |
| `Uu` | `𞵝𞵲𞵸󠄵󠅕󠇯` | U+1ED5D U+1ED72 U+1ED78 U+E0135 U+E0155 U+E01EF | at the start of a word |
| `Uu` | `𞵲𞵸󠄵󠅕󠇯` | U+1ED72 U+1ED78 U+E0135 U+E0155 U+E01EF | always |
| `UU` | `𞵝𞵲𞵸󠄵󠄵󠇯` | U+1ED5D U+1ED72 U+1ED78 U+E0135 U+E0135 U+E01EF | at the start of a word |
| `UU` | `𞵲𞵸󠄵󠄵󠇯` | U+1ED72 U+1ED78 U+E0135 U+E0135 U+E01EF | always |
| `Uú` | `𞵝𞵲𞵸󠄵󠅛󠅆󠅁󠅝󠇯` | U+1ED5D U+1ED72 U+1ED78 U+E0135 U+E015B U+E0146 U+E0141 U+E015D U+E01EF | at the start of a word |
| `Uú` | `𞵲𞵸󠄵󠅛󠅆󠅁󠅝󠇯` | U+1ED72 U+1ED78 U+E0135 U+E015B U+E0146 U+E0141 U+E015D U+E01EF | always |
| `UÚ` | `𞵝𞵲𞵸󠄵󠅛󠅄󠅁󠅝󠇯` | U+1ED5D U+1ED72 U+1ED78 U+E0135 U+E015B U+E0144 U+E0141 U+E015D U+E01EF | at the start of a word |
| `UÚ` | `𞵲𞵸󠄵󠅛󠅄󠅁󠅝󠇯` | U+1ED72 U+1ED78 U+E0135 U+E015B U+E0144 U+E0141 U+E015D U+E01EF | always |
| `úu` | `𞵝𞵲𞵸󠅛󠅆󠅁󠅝󠅕󠇯` | U+1ED5D U+1ED72 U+1ED78 U+E015B U+E0146 U+E0141 U+E015D U+E0155 U+E01EF | at the start of a word |
| `úu` | `𞵲𞵸󠅛󠅆󠅁󠅝󠅕󠇯` | U+1ED72 U+1ED78 U+E015B U+E0146 U+E0141 U+E015D U+E0155 U+E01EF | always |
| `úU` | `𞵝𞵲𞵸󠅛󠅆󠅁󠅝󠄵󠇯` | U+1ED5D U+1ED72 U+1ED78 U+E015B U+E0146 U+E0141 U+E015D U+E0135 U+E01EF | at the start of a word |
| `úU` | `𞵲𞵸󠅛󠅆󠅁󠅝󠄵󠇯` | U+1ED72 U+1ED78 U+E015B U+E0146 U+E0141 U+E015D U+E0135 U+E01EF | always |
| `úú` | `𞵝𞵲𞵸󠅛󠅆󠅁󠅝󠅛󠅆󠅁󠅝󠇯` | U+1ED5D U+1ED72 U+1ED78 U+E015B U+E0146 U+E0141 U+E015D U+E015B U+E0146 U+E0141 U+E015D U+E01EF | at the start of a word |
| `úú` | `𞵲𞵸󠅛󠅆󠅁󠅝󠅛󠅆󠅁󠅝󠇯` | U+1ED72 U+1ED78 U+E015B U+E0146 U+E0141 U+E015D U+E015B U+E0146 U+E0141 U+E015D U+E01EF | always |
| `úÚ` | `𞵝𞵲𞵸󠅛󠅆󠅁󠅝󠅛󠅄󠅁󠅝󠇯` | U+1ED5D U+1ED72 U+1ED78 U+E015B U+E0146 U+E0141 U+E015D U+E015B U+E0144 U+E0141 U+E015D U+E01EF | at the start of a word |
| `úÚ` | `𞵲𞵸󠅛󠅆󠅁󠅝󠅛󠅄󠅁󠅝󠇯` | U+1ED72 U+1ED78 U+E015B U+E0146 U+E0141 U+E015D U+E015B U+E0144 U+E0141 U+E015D U+E01EF | always |
| `Úu` | `𞵝𞵲𞵸󠅛󠅄󠅁󠅝󠅕󠇯` | U+1ED5D U+1ED72 U+1ED78 U+E015B U+E0144 U+E0141 U+E015D U+E0155 U+E01EF | at the start of a word |
| `Úu` | `𞵲𞵸󠅛󠅄󠅁󠅝󠅕󠇯` | U+1ED72 U+1ED78 U+E015B U+E0144 U+E0141 U+E015D U+E0155 U+E01EF | always |
| `ÚU` | `𞵝𞵲𞵸󠅛󠅄󠅁󠅝󠄵󠇯` | U+1ED5D U+1ED72 U+1ED78 U+E015B U+E0144 U+E0141 U+E015D U+E0135 U+E01EF | at the start of a word |
| `ÚU` | `𞵲𞵸󠅛󠅄󠅁󠅝󠄵󠇯` | U+1ED72 U+1ED78 U+E015B U+E0144 U+E0141 U+E015D U+E0135 U+E01EF | always |
| `Úú` | `𞵝𞵲𞵸󠅛󠅄󠅁󠅝󠅛󠅆󠅁󠅝󠇯` | U+1ED5D U+1ED72 U+1ED78 U+E015B U+E0144 U+E0141 U+E015D U+E015B U+E0146 U+E0141 U+E015D U+E01EF | at the start of a word |
| `Úú` | `𞵲𞵸󠅛󠅄󠅁󠅝󠅛󠅆󠅁󠅝󠇯` | U+1ED72 U+1ED78 U+E015B U+E0144 U+E0141 U+E015D U+E015B U+E0146 U+E0141 U+E015D U+E01EF | always |
| `ÚÚ` | `𞵝𞵲𞵸󠅛󠅄󠅁󠅝󠅛󠅄󠅁󠅝󠇯` | U+1ED5D U+1ED72 U+1ED78 U+E015B U+E0144 U+E0141 U+E015D U+E015B U+E0144 U+E0141 U+E015D U+E01EF | at the start of a word |
| `ÚÚ` | `𞵲𞵸󠅛󠅄󠅁󠅝󠅛󠅄󠅁󠅝󠇯` | U+1ED72 U+1ED78 U+E015B U+E0144 U+E0141 U+E015D U+E015B U+E0144 U+E0141 U+E015D U+E01EF | always |
| `uy` | `𞵝𞵲𞵝𞵵󠅕󠅙󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED75 U+E0155 U+E0159 U+E01EF | at the start of a word |
| `uy` | `𞵲𞵝𞵵󠅕󠅙󠇯` | U+1ED72 U+1ED5D U+1ED75 U+E0155 U+E0159 U+E01EF | always |
| `uY` | `𞵝𞵲𞵝𞵵󠅕󠄹󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED75 U+E0155 U+E0139 U+E01EF | at the start of a word |
| `uY` | `𞵲𞵝𞵵󠅕󠄹󠇯` | U+1ED72 U+1ED5D U+1ED75 U+E0155 U+E0139 U+E01EF | always |
| `uý` | `𞵝𞵲𞵝𞵵󠅕󠅛󠅆󠅄󠅝󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED75 U+E0155 U+E015B U+E0146 U+E0144 U+E015D U+E01EF | at the start of a word |
| `uý` | `𞵲𞵝𞵵󠅕󠅛󠅆󠅄󠅝󠇯` | U+1ED72 U+1ED5D U+1ED75 U+E0155 U+E015B U+E0146 U+E0144 U+E015D U+E01EF | always |
| `uÝ` | `𞵝𞵲𞵝𞵵󠅕󠅛󠅄󠅄󠅝󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED75 U+E0155 U+E015B U+E0144 U+E0144 U+E015D U+E01EF | at the start of a word |
| `uÝ` | `𞵲𞵝𞵵󠅕󠅛󠅄󠅄󠅝󠇯` | U+1ED72 U+1ED5D U+1ED75 U+E0155 U+E015B U+E0144 U+E0144 U+E015D U+E01EF | always |
| `Uy` | `𞵝𞵲𞵝𞵵󠄵󠅙󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED75 U+E0135 U+E0159 U+E01EF | at the start of a word |
| `Uy` | `𞵲𞵝𞵵󠄵󠅙󠇯` | U+1ED72 U+1ED5D U+1ED75 U+E0135 U+E0159 U+E01EF | always |
| `UY` | `𞵝𞵲𞵝𞵵󠄵󠄹󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED75 U+E0135 U+E0139 U+E01EF | at the start of a word |
| `UY` | `𞵲𞵝𞵵󠄵󠄹󠇯` | U+1ED72 U+1ED5D U+1ED75 U+E0135 U+E0139 U+E01EF | always |
| `Uý` | `𞵝𞵲𞵝𞵵󠄵󠅛󠅆󠅄󠅝󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED75 U+E0135 U+E015B U+E0146 U+E0144 U+E015D U+E01EF | at the start of a word |
| `Uý` | `𞵲𞵝𞵵󠄵󠅛󠅆󠅄󠅝󠇯` | U+1ED72 U+1ED5D U+1ED75 U+E0135 U+E015B U+E0146 U+E0144 U+E015D U+E01EF | always |
| `UÝ` | `𞵝𞵲𞵝𞵵󠄵󠅛󠅄󠅄󠅝󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED75 U+E0135 U+E015B U+E0144 U+E0144 U+E015D U+E01EF | at the start of a word |
| `UÝ` | `𞵲𞵝𞵵󠄵󠅛󠅄󠅄󠅝󠇯` | U+1ED72 U+1ED5D U+1ED75 U+E0135 U+E015B U+E0144 U+E0144 U+E015D U+E01EF | always |
| `úy` | `𞵝𞵲𞵝𞵵󠅛󠅆󠅁󠅝󠅙󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED75 U+E015B U+E0146 U+E0141 U+E015D U+E0159 U+E01EF | at the start of a word |
| `úy` | `𞵲𞵝𞵵󠅛󠅆󠅁󠅝󠅙󠇯` | U+1ED72 U+1ED5D U+1ED75 U+E015B U+E0146 U+E0141 U+E015D U+E0159 U+E01EF | always |
| `úY` | `𞵝𞵲𞵝𞵵󠅛󠅆󠅁󠅝󠄹󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED75 U+E015B U+E0146 U+E0141 U+E015D U+E0139 U+E01EF | at the start of a word |
| `úY` | `𞵲𞵝𞵵󠅛󠅆󠅁󠅝󠄹󠇯` | U+1ED72 U+1ED5D U+1ED75 U+E015B U+E0146 U+E0141 U+E015D U+E0139 U+E01EF | always |
| `úý` | `𞵝𞵲𞵝𞵵󠅛󠅆󠅁󠅝󠅛󠅆󠅄󠅝󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED75 U+E015B U+E0146 U+E0141 U+E015D U+E015B U+E0146 U+E0144 U+E015D U+E01EF | at the start of a word |
| `úý` | `𞵲𞵝𞵵󠅛󠅆󠅁󠅝󠅛󠅆󠅄󠅝󠇯` | U+1ED72 U+1ED5D U+1ED75 U+E015B U+E0146 U+E0141 U+E015D U+E015B U+E0146 U+E0144 U+E015D U+E01EF | always |
| `úÝ` | `𞵝𞵲𞵝𞵵󠅛󠅆󠅁󠅝󠅛󠅄󠅄󠅝󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED75 U+E015B U+E0146 U+E0141 U+E015D U+E015B U+E0144 U+E0144 U+E015D U+E01EF | at the start of a word |
| `úÝ` | `𞵲𞵝𞵵󠅛󠅆󠅁󠅝󠅛󠅄󠅄󠅝󠇯` | U+1ED72 U+1ED5D U+1ED75 U+E015B U+E0146 U+E0141 U+E015D U+E015B U+E0144 U+E0144 U+E015D U+E01EF | always |
| `Úy` | `𞵝𞵲𞵝𞵵󠅛󠅄󠅁󠅝󠅙󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED75 U+E015B U+E0144 U+E0141 U+E015D U+E0159 U+E01EF | at the start of a word |
| `Úy` | `𞵲𞵝𞵵󠅛󠅄󠅁󠅝󠅙󠇯` | U+1ED72 U+1ED5D U+1ED75 U+E015B U+E0144 U+E0141 U+E015D U+E0159 U+E01EF | always |
| `ÚY` | `𞵝𞵲𞵝𞵵󠅛󠅄󠅁󠅝󠄹󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED75 U+E015B U+E0144 U+E0141 U+E015D U+E0139 U+E01EF | at the start of a word |
| `ÚY` | `𞵲𞵝𞵵󠅛󠅄󠅁󠅝󠄹󠇯` | U+1ED72 U+1ED5D U+1ED75 U+E015B U+E0144 U+E0141 U+E015D U+E0139 U+E01EF | always |
| `Úý` | `𞵝𞵲𞵝𞵵󠅛󠅄󠅁󠅝󠅛󠅆󠅄󠅝󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED75 U+E015B U+E0144 U+E0141 U+E015D U+E015B U+E0146 U+E0144 U+E015D U+E01EF | at the start of a word |
| `Úý` | `𞵲𞵝𞵵󠅛󠅄󠅁󠅝󠅛󠅆󠅄󠅝󠇯` | U+1ED72 U+1ED5D U+1ED75 U+E015B U+E0144 U+E0141 U+E015D U+E015B U+E0146 U+E0144 U+E015D U+E01EF | always |
| `ÚÝ` | `𞵝𞵲𞵝𞵵󠅛󠅄󠅁󠅝󠅛󠅄󠅄󠅝󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED75 U+E015B U+E0144 U+E0141 U+E015D U+E015B U+E0144 U+E0144 U+E015D U+E01EF | at the start of a word |
| `ÚÝ` | `𞵲𞵝𞵵󠅛󠅄󠅁󠅝󠅛󠅄󠅄󠅝󠇯` | U+1ED72 U+1ED5D U+1ED75 U+E015B U+E0144 U+E0141 U+E015D U+E015B U+E0144 U+E0144 U+E015D U+E01EF | always |
| `uë` | `𞵝𞵲𞵝𞵶󠅕󠅛󠅅󠅂󠅝󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED76 U+E0155 U+E015B U+E0145 U+E0142 U+E015D U+E01EF | at the start of a word |
| `uë` | `𞵲𞵝𞵶󠅕󠅛󠅅󠅂󠅝󠇯` | U+1ED72 U+1ED5D U+1ED76 U+E0155 U+E015B U+E0145 U+E0142 U+E015D U+E01EF | always |
| `uË` | `𞵝𞵲𞵝𞵶󠅕󠅛󠅃󠅂󠅝󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED76 U+E0155 U+E015B U+E0143 U+E0142 U+E015D U+E01EF | at the start of a word |
| `uË` | `𞵲𞵝𞵶󠅕󠅛󠅃󠅂󠅝󠇯` | U+1ED72 U+1ED5D U+1ED76 U+E0155 U+E015B U+E0143 U+E0142 U+E015D U+E01EF | always |
| `Uë` | `𞵝𞵲𞵝𞵶󠄵󠅛󠅅󠅂󠅝󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED76 U+E0135 U+E015B U+E0145 U+E0142 U+E015D U+E01EF | at the start of a word |
| `Uë` | `𞵲𞵝𞵶󠄵󠅛󠅅󠅂󠅝󠇯` | U+1ED72 U+1ED5D U+1ED76 U+E0135 U+E015B U+E0145 U+E0142 U+E015D U+E01EF | always |
| `UË` | `𞵝𞵲𞵝𞵶󠄵󠅛󠅃󠅂󠅝󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED76 U+E0135 U+E015B U+E0143 U+E0142 U+E015D U+E01EF | at the start of a word |
| `UË` | `𞵲𞵝𞵶󠄵󠅛󠅃󠅂󠅝󠇯` | U+1ED72 U+1ED5D U+1ED76 U+E0135 U+E015B U+E0143 U+E0142 U+E015D U+E01EF | always |
| `úë` | `𞵝𞵲𞵝𞵶󠅛󠅆󠅁󠅝󠅛󠅅󠅂󠅝󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED76 U+E015B U+E0146 U+E0141 U+E015D U+E015B U+E0145 U+E0142 U+E015D U+E01EF | at the start of a word |
| `úë` | `𞵲𞵝𞵶󠅛󠅆󠅁󠅝󠅛󠅅󠅂󠅝󠇯` | U+1ED72 U+1ED5D U+1ED76 U+E015B U+E0146 U+E0141 U+E015D U+E015B U+E0145 U+E0142 U+E015D U+E01EF | always |
| `úË` | `𞵝𞵲𞵝𞵶󠅛󠅆󠅁󠅝󠅛󠅃󠅂󠅝󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED76 U+E015B U+E0146 U+E0141 U+E015D U+E015B U+E0143 U+E0142 U+E015D U+E01EF | at the start of a word |
| `úË` | `𞵲𞵝𞵶󠅛󠅆󠅁󠅝󠅛󠅃󠅂󠅝󠇯` | U+1ED72 U+1ED5D U+1ED76 U+E015B U+E0146 U+E0141 U+E015D U+E015B U+E0143 U+E0142 U+E015D U+E01EF | always |
| `Úë` | `𞵝𞵲𞵝𞵶󠅛󠅄󠅁󠅝󠅛󠅅󠅂󠅝󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED76 U+E015B U+E0144 U+E0141 U+E015D U+E015B U+E0145 U+E0142 U+E015D U+E01EF | at the start of a word |
| `Úë` | `𞵲𞵝𞵶󠅛󠅄󠅁󠅝󠅛󠅅󠅂󠅝󠇯` | U+1ED72 U+1ED5D U+1ED76 U+E015B U+E0144 U+E0141 U+E015D U+E015B U+E0145 U+E0142 U+E015D U+E01EF | always |
| `ÚË` | `𞵝𞵲𞵝𞵶󠅛󠅄󠅁󠅝󠅛󠅃󠅂󠅝󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED76 U+E015B U+E0144 U+E0141 U+E015D U+E015B U+E0143 U+E0142 U+E015D U+E01EF | at the start of a word |
| `ÚË` | `𞵲𞵝𞵶󠅛󠅄󠅁󠅝󠅛󠅃󠅂󠅝󠇯` | U+1ED72 U+1ED5D U+1ED76 U+E015B U+E0144 U+E0141 U+E015D U+E015B U+E0143 U+E0142 U+E015D U+E01EF | always |
| `ya` | `𞵝𞵵𞵝𞵰󠅙󠅁󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED70 U+E0159 U+E0141 U+E01EF | at the start of a word |
| `ya` | `𞵵𞵝𞵰󠅙󠅁󠇯` | U+1ED75 U+1ED5D U+1ED70 U+E0159 U+E0141 U+E01EF | always |
| `yA` | `𞵝𞵵𞵝𞵰󠅙󠄡󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED70 U+E0159 U+E0121 U+E01EF | at the start of a word |
| `yA` | `𞵵𞵝𞵰󠅙󠄡󠇯` | U+1ED75 U+1ED5D U+1ED70 U+E0159 U+E0121 U+E01EF | always |
| `yá` | `𞵝𞵵𞵝𞵰󠅙󠅛󠅅󠄑󠅝󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED70 U+E0159 U+E015B U+E0145 U+E0111 U+E015D U+E01EF | at the start of a word |
| `yá` | `𞵵𞵝𞵰󠅙󠅛󠅅󠄑󠅝󠇯` | U+1ED75 U+1ED5D U+1ED70 U+E0159 U+E015B U+E0145 U+E0111 U+E015D U+E01EF | always |
| `yÁ` | `𞵝𞵵𞵝𞵰󠅙󠅛󠅃󠄑󠅝󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED70 U+E0159 U+E015B U+E0143 U+E0111 U+E015D U+E01EF | at the start of a word |
| `yÁ` | `𞵵𞵝𞵰󠅙󠅛󠅃󠄑󠅝󠇯` | U+1ED75 U+1ED5D U+1ED70 U+E0159 U+E015B U+E0143 U+E0111 U+E015D U+E01EF | always |
| `Ya` | `𞵝𞵵𞵝𞵰󠄹󠅁󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED70 U+E0139 U+E0141 U+E01EF | at the start of a word |
| `Ya` | `𞵵𞵝𞵰󠄹󠅁󠇯` | U+1ED75 U+1ED5D U+1ED70 U+E0139 U+E0141 U+E01EF | always |
| `YA` | `𞵝𞵵𞵝𞵰󠄹󠄡󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED70 U+E0139 U+E0121 U+E01EF | at the start of a word |
| `YA` | `𞵵𞵝𞵰󠄹󠄡󠇯` | U+1ED75 U+1ED5D U+1ED70 U+E0139 U+E0121 U+E01EF | always |
| `Yá` | `𞵝𞵵𞵝𞵰󠄹󠅛󠅅󠄑󠅝󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED70 U+E0139 U+E015B U+E0145 U+E0111 U+E015D U+E01EF | at the start of a word |
| `Yá` | `𞵵𞵝𞵰󠄹󠅛󠅅󠄑󠅝󠇯` | U+1ED75 U+1ED5D U+1ED70 U+E0139 U+E015B U+E0145 U+E0111 U+E015D U+E01EF | always |
| `YÁ` | `𞵝𞵵𞵝𞵰󠄹󠅛󠅃󠄑󠅝󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED70 U+E0139 U+E015B U+E0143 U+E0111 U+E015D U+E01EF | at the start of a word |
| `YÁ` | `𞵵𞵝𞵰󠄹󠅛󠅃󠄑󠅝󠇯` | U+1ED75 U+1ED5D U+1ED70 U+E0139 U+E015B U+E0143 U+E0111 U+E015D U+E01EF | always |
| `ýa` | `𞵝𞵵𞵝𞵰󠅛󠅆󠅄󠅝󠅁󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED70 U+E015B U+E0146 U+E0144 U+E015D U+E0141 U+E01EF | at the start of a word |
| `ýa` | `𞵵𞵝𞵰󠅛󠅆󠅄󠅝󠅁󠇯` | U+1ED75 U+1ED5D U+1ED70 U+E015B U+E0146 U+E0144 U+E015D U+E0141 U+E01EF | always |
| `ýA` | `𞵝𞵵𞵝𞵰󠅛󠅆󠅄󠅝󠄡󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED70 U+E015B U+E0146 U+E0144 U+E015D U+E0121 U+E01EF | at the start of a word |
| `ýA` | `𞵵𞵝𞵰󠅛󠅆󠅄󠅝󠄡󠇯` | U+1ED75 U+1ED5D U+1ED70 U+E015B U+E0146 U+E0144 U+E015D U+E0121 U+E01EF | always |
| `ýá` | `𞵝𞵵𞵝𞵰󠅛󠅆󠅄󠅝󠅛󠅅󠄑󠅝󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED70 U+E015B U+E0146 U+E0144 U+E015D U+E015B U+E0145 U+E0111 U+E015D U+E01EF | at the start of a word |
| `ýá` | `𞵵𞵝𞵰󠅛󠅆󠅄󠅝󠅛󠅅󠄑󠅝󠇯` | U+1ED75 U+1ED5D U+1ED70 U+E015B U+E0146 U+E0144 U+E015D U+E015B U+E0145 U+E0111 U+E015D U+E01EF | always |
| `ýÁ` | `𞵝𞵵𞵝𞵰󠅛󠅆󠅄󠅝󠅛󠅃󠄑󠅝󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED70 U+E015B U+E0146 U+E0144 U+E015D U+E015B U+E0143 U+E0111 U+E015D U+E01EF | at the start of a word |
| `ýÁ` | `𞵵𞵝𞵰󠅛󠅆󠅄󠅝󠅛󠅃󠄑󠅝󠇯` | U+1ED75 U+1ED5D U+1ED70 U+E015B U+E0146 U+E0144 U+E015D U+E015B U+E0143 U+E0111 U+E015D U+E01EF | always |
| `Ýa` | `𞵝𞵵𞵝𞵰󠅛󠅄󠅄󠅝󠅁󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED70 U+E015B U+E0144 U+E0144 U+E015D U+E0141 U+E01EF | at the start of a word |
| `Ýa` | `𞵵𞵝𞵰󠅛󠅄󠅄󠅝󠅁󠇯` | U+1ED75 U+1ED5D U+1ED70 U+E015B U+E0144 U+E0144 U+E015D U+E0141 U+E01EF | always |
| `ÝA` | `𞵝𞵵𞵝𞵰󠅛󠅄󠅄󠅝󠄡󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED70 U+E015B U+E0144 U+E0144 U+E015D U+E0121 U+E01EF | at the start of a word |
| `ÝA` | `𞵵𞵝𞵰󠅛󠅄󠅄󠅝󠄡󠇯` | U+1ED75 U+1ED5D U+1ED70 U+E015B U+E0144 U+E0144 U+E015D U+E0121 U+E01EF | always |
| `Ýá` | `𞵝𞵵𞵝𞵰󠅛󠅄󠅄󠅝󠅛󠅅󠄑󠅝󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED70 U+E015B U+E0144 U+E0144 U+E015D U+E015B U+E0145 U+E0111 U+E015D U+E01EF | at the start of a word |
| `Ýá` | `𞵵𞵝𞵰󠅛󠅄󠅄󠅝󠅛󠅅󠄑󠅝󠇯` | U+1ED75 U+1ED5D U+1ED70 U+E015B U+E0144 U+E0144 U+E015D U+E015B U+E0145 U+E0111 U+E015D U+E01EF | always |
| `ÝÁ` | `𞵝𞵵𞵝𞵰󠅛󠅄󠅄󠅝󠅛󠅃󠄑󠅝󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED70 U+E015B U+E0144 U+E0144 U+E015D U+E015B U+E0143 U+E0111 U+E015D U+E01EF | at the start of a word |
| `ÝÁ` | `𞵵𞵝𞵰󠅛󠅄󠅄󠅝󠅛󠅃󠄑󠅝󠇯` | U+1ED75 U+1ED5D U+1ED70 U+E015B U+E0144 U+E0144 U+E015D U+E015B U+E0143 U+E0111 U+E015D U+E01EF | always |
| `yo` | `𞵝𞵵𞵝𞵱󠅙󠅏󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED71 U+E0159 U+E014F U+E01EF | at the start of a word |
| `yo` | `𞵵𞵝𞵱󠅙󠅏󠇯` | U+1ED75 U+1ED5D U+1ED71 U+E0159 U+E014F U+E01EF | always |
| `yO` | `𞵝𞵵𞵝𞵱󠅙󠄯󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED71 U+E0159 U+E012F U+E01EF | at the start of a word |
| `yO` | `𞵵𞵝𞵱󠅙󠄯󠇯` | U+1ED75 U+1ED5D U+1ED71 U+E0159 U+E012F U+E01EF | always |
| `yó` | `𞵝𞵵𞵝𞵱󠅙󠅛󠅆󠄓󠅝󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED71 U+E0159 U+E015B U+E0146 U+E0113 U+E015D U+E01EF | at the start of a word |
| `yó` | `𞵵𞵝𞵱󠅙󠅛󠅆󠄓󠅝󠇯` | U+1ED75 U+1ED5D U+1ED71 U+E0159 U+E015B U+E0146 U+E0113 U+E015D U+E01EF | always |
| `yÓ` | `𞵝𞵵𞵝𞵱󠅙󠅛󠅄󠄓󠅝󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED71 U+E0159 U+E015B U+E0144 U+E0113 U+E015D U+E01EF | at the start of a word |
| `yÓ` | `𞵵𞵝𞵱󠅙󠅛󠅄󠄓󠅝󠇯` | U+1ED75 U+1ED5D U+1ED71 U+E0159 U+E015B U+E0144 U+E0113 U+E015D U+E01EF | always |
| `Yo` | `𞵝𞵵𞵝𞵱󠄹󠅏󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED71 U+E0139 U+E014F U+E01EF | at the start of a word |
| `Yo` | `𞵵𞵝𞵱󠄹󠅏󠇯` | U+1ED75 U+1ED5D U+1ED71 U+E0139 U+E014F U+E01EF | always |
| `YO` | `𞵝𞵵𞵝𞵱󠄹󠄯󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED71 U+E0139 U+E012F U+E01EF | at the start of a word |
| `YO` | `𞵵𞵝𞵱󠄹󠄯󠇯` | U+1ED75 U+1ED5D U+1ED71 U+E0139 U+E012F U+E01EF | always |
| `Yó` | `𞵝𞵵𞵝𞵱󠄹󠅛󠅆󠄓󠅝󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED71 U+E0139 U+E015B U+E0146 U+E0113 U+E015D U+E01EF | at the start of a word |
| `Yó` | `𞵵𞵝𞵱󠄹󠅛󠅆󠄓󠅝󠇯` | U+1ED75 U+1ED5D U+1ED71 U+E0139 U+E015B U+E0146 U+E0113 U+E015D U+E01EF | always |
| `YÓ` | `𞵝𞵵𞵝𞵱󠄹󠅛󠅄󠄓󠅝󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED71 U+E0139 U+E015B U+E0144 U+E0113 U+E015D U+E01EF | at the start of a word |
| `YÓ` | `𞵵𞵝𞵱󠄹󠅛󠅄󠄓󠅝󠇯` | U+1ED75 U+1ED5D U+1ED71 U+E0139 U+E015B U+E0144 U+E0113 U+E015D U+E01EF | always |
| `ýo` | `𞵝𞵵𞵝𞵱󠅛󠅆󠅄󠅝󠅏󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED71 U+E015B U+E0146 U+E0144 U+E015D U+E014F U+E01EF | at the start of a word |
| `ýo` | `𞵵𞵝𞵱󠅛󠅆󠅄󠅝󠅏󠇯` | U+1ED75 U+1ED5D U+1ED71 U+E015B U+E0146 U+E0144 U+E015D U+E014F U+E01EF | always |
| `ýO` | `𞵝𞵵𞵝𞵱󠅛󠅆󠅄󠅝󠄯󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED71 U+E015B U+E0146 U+E0144 U+E015D U+E012F U+E01EF | at the start of a word |
| `ýO` | `𞵵𞵝𞵱󠅛󠅆󠅄󠅝󠄯󠇯` | U+1ED75 U+1ED5D U+1ED71 U+E015B U+E0146 U+E0144 U+E015D U+E012F U+E01EF | always |
| `ýó` | `𞵝𞵵𞵝𞵱󠅛󠅆󠅄󠅝󠅛󠅆󠄓󠅝󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED71 U+E015B U+E0146 U+E0144 U+E015D U+E015B U+E0146 U+E0113 U+E015D U+E01EF | at the start of a word |
| `ýó` | `𞵵𞵝𞵱󠅛󠅆󠅄󠅝󠅛󠅆󠄓󠅝󠇯` | U+1ED75 U+1ED5D U+1ED71 U+E015B U+E0146 U+E0144 U+E015D U+E015B U+E0146 U+E0113 U+E015D U+E01EF | always |
| `ýÓ` | `𞵝𞵵𞵝𞵱󠅛󠅆󠅄󠅝󠅛󠅄󠄓󠅝󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED71 U+E015B U+E0146 U+E0144 U+E015D U+E015B U+E0144 U+E0113 U+E015D U+E01EF | at the start of a word |
| `ýÓ` | `𞵵𞵝𞵱󠅛󠅆󠅄󠅝󠅛󠅄󠄓󠅝󠇯` | U+1ED75 U+1ED5D U+1ED71 U+E015B U+E0146 U+E0144 U+E015D U+E015B U+E0144 U+E0113 U+E015D U+E01EF | always |
| `Ýo` | `𞵝𞵵𞵝𞵱󠅛󠅄󠅄󠅝󠅏󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED71 U+E015B U+E0144 U+E0144 U+E015D U+E014F U+E01EF | at the start of a word |
| `Ýo` | `𞵵𞵝𞵱󠅛󠅄󠅄󠅝󠅏󠇯` | U+1ED75 U+1ED5D U+1ED71 U+E015B U+E0144 U+E0144 U+E015D U+E014F U+E01EF | always |
| `ÝO` | `𞵝𞵵𞵝𞵱󠅛󠅄󠅄󠅝󠄯󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED71 U+E015B U+E0144 U+E0144 U+E015D U+E012F U+E01EF | at the start of a word |
| `ÝO` | `𞵵𞵝𞵱󠅛󠅄󠅄󠅝󠄯󠇯` | U+1ED75 U+1ED5D U+1ED71 U+E015B U+E0144 U+E0144 U+E015D U+E012F U+E01EF | always |
| `Ýó` | `𞵝𞵵𞵝𞵱󠅛󠅄󠅄󠅝󠅛󠅆󠄓󠅝󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED71 U+E015B U+E0144 U+E0144 U+E015D U+E015B U+E0146 U+E0113 U+E015D U+E01EF | at the start of a word |
| `Ýó` | `𞵵𞵝𞵱󠅛󠅄󠅄󠅝󠅛󠅆󠄓󠅝󠇯` | U+1ED75 U+1ED5D U+1ED71 U+E015B U+E0144 U+E0144 U+E015D U+E015B U+E0146 U+E0113 U+E015D U+E01EF | always |
| `ÝÓ` | `𞵝𞵵𞵝𞵱󠅛󠅄󠅄󠅝󠅛󠅄󠄓󠅝󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED71 U+E015B U+E0144 U+E0144 U+E015D U+E015B U+E0144 U+E0113 U+E015D U+E01EF | at the start of a word |
| `ÝÓ` | `𞵵𞵝𞵱󠅛󠅄󠅄󠅝󠅛󠅄󠄓󠅝󠇯` | U+1ED75 U+1ED5D U+1ED71 U+E015B U+E0144 U+E0144 U+E015D U+E015B U+E0144 U+E0113 U+E015D U+E01EF | always |
| `yu` | `𞵝𞵵𞵝𞵲󠅙󠅕󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED72 U+E0159 U+E0155 U+E01EF | at the start of a word |
| `yu` | `𞵵𞵝𞵲󠅙󠅕󠇯` | U+1ED75 U+1ED5D U+1ED72 U+E0159 U+E0155 U+E01EF | always |
| `yU` | `𞵝𞵵𞵝𞵲󠅙󠄵󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED72 U+E0159 U+E0135 U+E01EF | at the start of a word |
| `yU` | `𞵵𞵝𞵲󠅙󠄵󠇯` | U+1ED75 U+1ED5D U+1ED72 U+E0159 U+E0135 U+E01EF | always |
| `yú` | `𞵝𞵵𞵝𞵲󠅙󠅛󠅆󠅁󠅝󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED72 U+E0159 U+E015B U+E0146 U+E0141 U+E015D U+E01EF | at the start of a word |
| `yú` | `𞵵𞵝𞵲󠅙󠅛󠅆󠅁󠅝󠇯` | U+1ED75 U+1ED5D U+1ED72 U+E0159 U+E015B U+E0146 U+E0141 U+E015D U+E01EF | always |
| `yÚ` | `𞵝𞵵𞵝𞵲󠅙󠅛󠅄󠅁󠅝󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED72 U+E0159 U+E015B U+E0144 U+E0141 U+E015D U+E01EF | at the start of a word |
| `yÚ` | `𞵵𞵝𞵲󠅙󠅛󠅄󠅁󠅝󠇯` | U+1ED75 U+1ED5D U+1ED72 U+E0159 U+E015B U+E0144 U+E0141 U+E015D U+E01EF | always |
| `Yu` | `𞵝𞵵𞵝𞵲󠄹󠅕󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED72 U+E0139 U+E0155 U+E01EF | at the start of a word |
| `Yu` | `𞵵𞵝𞵲󠄹󠅕󠇯` | U+1ED75 U+1ED5D U+1ED72 U+E0139 U+E0155 U+E01EF | always |
| `YU` | `𞵝𞵵𞵝𞵲󠄹󠄵󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED72 U+E0139 U+E0135 U+E01EF | at the start of a word |
| `YU` | `𞵵𞵝𞵲󠄹󠄵󠇯` | U+1ED75 U+1ED5D U+1ED72 U+E0139 U+E0135 U+E01EF | always |
| `Yú` | `𞵝𞵵𞵝𞵲󠄹󠅛󠅆󠅁󠅝󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED72 U+E0139 U+E015B U+E0146 U+E0141 U+E015D U+E01EF | at the start of a word |
| `Yú` | `𞵵𞵝𞵲󠄹󠅛󠅆󠅁󠅝󠇯` | U+1ED75 U+1ED5D U+1ED72 U+E0139 U+E015B U+E0146 U+E0141 U+E015D U+E01EF | always |
| `YÚ` | `𞵝𞵵𞵝𞵲󠄹󠅛󠅄󠅁󠅝󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED72 U+E0139 U+E015B U+E0144 U+E0141 U+E015D U+E01EF | at the start of a word |
| `YÚ` | `𞵵𞵝𞵲󠄹󠅛󠅄󠅁󠅝󠇯` | U+1ED75 U+1ED5D U+1ED72 U+E0139 U+E015B U+E0144 U+E0141 U+E015D U+E01EF | always |
| `ýu` | `𞵝𞵵𞵝𞵲󠅛󠅆󠅄󠅝󠅕󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED72 U+E015B U+E0146 U+E0144 U+E015D U+E0155 U+E01EF | at the start of a word |
| `ýu` | `𞵵𞵝𞵲󠅛󠅆󠅄󠅝󠅕󠇯` | U+1ED75 U+1ED5D U+1ED72 U+E015B U+E0146 U+E0144 U+E015D U+E0155 U+E01EF | always |
| `ýU` | `𞵝𞵵𞵝𞵲󠅛󠅆󠅄󠅝󠄵󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED72 U+E015B U+E0146 U+E0144 U+E015D U+E0135 U+E01EF | at the start of a word |
| `ýU` | `𞵵𞵝𞵲󠅛󠅆󠅄󠅝󠄵󠇯` | U+1ED75 U+1ED5D U+1ED72 U+E015B U+E0146 U+E0144 U+E015D U+E0135 U+E01EF | always |
| `ýú` | `𞵝𞵵𞵝𞵲󠅛󠅆󠅄󠅝󠅛󠅆󠅁󠅝󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED72 U+E015B U+E0146 U+E0144 U+E015D U+E015B U+E0146 U+E0141 U+E015D U+E01EF | at the start of a word |
| `ýú` | `𞵵𞵝𞵲󠅛󠅆󠅄󠅝󠅛󠅆󠅁󠅝󠇯` | U+1ED75 U+1ED5D U+1ED72 U+E015B U+E0146 U+E0144 U+E015D U+E015B U+E0146 U+E0141 U+E015D U+E01EF | always |
| `ýÚ` | `𞵝𞵵𞵝𞵲󠅛󠅆󠅄󠅝󠅛󠅄󠅁󠅝󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED72 U+E015B U+E0146 U+E0144 U+E015D U+E015B U+E0144 U+E0141 U+E015D U+E01EF | at the start of a word |
| `ýÚ` | `𞵵𞵝𞵲󠅛󠅆󠅄󠅝󠅛󠅄󠅁󠅝󠇯` | U+1ED75 U+1ED5D U+1ED72 U+E015B U+E0146 U+E0144 U+E015D U+E015B U+E0144 U+E0141 U+E015D U+E01EF | always |
| `Ýu` | `𞵝𞵵𞵝𞵲󠅛󠅄󠅄󠅝󠅕󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED72 U+E015B U+E0144 U+E0144 U+E015D U+E0155 U+E01EF | at the start of a word |
| `Ýu` | `𞵵𞵝𞵲󠅛󠅄󠅄󠅝󠅕󠇯` | U+1ED75 U+1ED5D U+1ED72 U+E015B U+E0144 U+E0144 U+E015D U+E0155 U+E01EF | always |
| `ÝU` | `𞵝𞵵𞵝𞵲󠅛󠅄󠅄󠅝󠄵󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED72 U+E015B U+E0144 U+E0144 U+E015D U+E0135 U+E01EF | at the start of a word |
| `ÝU` | `𞵵𞵝𞵲󠅛󠅄󠅄󠅝󠄵󠇯` | U+1ED75 U+1ED5D U+1ED72 U+E015B U+E0144 U+E0144 U+E015D U+E0135 U+E01EF | always |
| `Ýú` | `𞵝𞵵𞵝𞵲󠅛󠅄󠅄󠅝󠅛󠅆󠅁󠅝󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED72 U+E015B U+E0144 U+E0144 U+E015D U+E015B U+E0146 U+E0141 U+E015D U+E01EF | at the start of a word |
| `Ýú` | `𞵵𞵝𞵲󠅛󠅄󠅄󠅝󠅛󠅆󠅁󠅝󠇯` | U+1ED75 U+1ED5D U+1ED72 U+E015B U+E0144 U+E0144 U+E015D U+E015B U+E0146 U+E0141 U+E015D U+E01EF | always |
| `ÝÚ` | `𞵝𞵵𞵝𞵲󠅛󠅄󠅄󠅝󠅛󠅄󠅁󠅝󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED72 U+E015B U+E0144 U+E0144 U+E015D U+E015B U+E0144 U+E0141 U+E015D U+E01EF | at the start of a word |
| `ÝÚ` | `𞵵𞵝𞵲󠅛󠅄󠅄󠅝󠅛󠅄󠅁󠅝󠇯` | U+1ED75 U+1ED5D U+1ED72 U+E015B U+E0144 U+E0144 U+E015D U+E015B U+E0144 U+E0141 U+E015D U+E01EF | always |
| `yy` | `𞵝𞵵𞵸` | U+1ED5D U+1ED75 U+1ED78 | at the start of a word |
| `yy` | `𞵵𞵸` | U+1ED75 U+1ED78 | always |
| `yY` | `𞵝𞵵𞵸󠅙󠄹󠇯` | U+1ED5D U+1ED75 U+1ED78 U+E0159 U+E0139 U+E01EF | at the start of a word |
| `yY` | `𞵵𞵸󠅙󠄹󠇯` | U+1ED75 U+1ED78 U+E0159 U+E0139 U+E01EF | always |
| `yý` | `𞵝𞵵𞵸󠅙󠅛󠅆󠅄󠅝󠇯` | U+1ED5D U+1ED75 U+1ED78 U+E0159 U+E015B U+E0146 U+E0144 U+E015D U+E01EF | at the start of a word |
| `yý` | `𞵵𞵸󠅙󠅛󠅆󠅄󠅝󠇯` | U+1ED75 U+1ED78 U+E0159 U+E015B U+E0146 U+E0144 U+E015D U+E01EF | always |
| `yÝ` | `𞵝𞵵𞵸󠅙󠅛󠅄󠅄󠅝󠇯` | U+1ED5D U+1ED75 U+1ED78 U+E0159 U+E015B U+E0144 U+E0144 U+E015D U+E01EF | at the start of a word |
| `yÝ` | `𞵵𞵸󠅙󠅛󠅄󠅄󠅝󠇯` | U+1ED75 U+1ED78 U+E0159 U+E015B U+E0144 U+E0144 U+E015D U+E01EF | always |
| `Yy` | `𞵝𞵵𞵸󠄹󠅙󠇯` | U+1ED5D U+1ED75 U+1ED78 U+E0139 U+E0159 U+E01EF | at the start of a word |
| `Yy` | `𞵵𞵸󠄹󠅙󠇯` | U+1ED75 U+1ED78 U+E0139 U+E0159 U+E01EF | always |
| `YY` | `𞵝𞵵𞵸󠄹󠄹󠇯` | U+1ED5D U+1ED75 U+1ED78 U+E0139 U+E0139 U+E01EF | at the start of a word |
| `YY` | `𞵵𞵸󠄹󠄹󠇯` | U+1ED75 U+1ED78 U+E0139 U+E0139 U+E01EF | always |
| `Yý` | `𞵝𞵵𞵸󠄹󠅛󠅆󠅄󠅝󠇯` | U+1ED5D U+1ED75 U+1ED78 U+E0139 U+E015B U+E0146 U+E0144 U+E015D U+E01EF | at the start of a word |
| `Yý` | `𞵵𞵸󠄹󠅛󠅆󠅄󠅝󠇯` | U+1ED75 U+1ED78 U+E0139 U+E015B U+E0146 U+E0144 U+E015D U+E01EF | always |
| `YÝ` | `𞵝𞵵𞵸󠄹󠅛󠅄󠅄󠅝󠇯` | U+1ED5D U+1ED75 U+1ED78 U+E0139 U+E015B U+E0144 U+E0144 U+E015D U+E01EF | at the start of a word |
| `YÝ` | `𞵵𞵸󠄹󠅛󠅄󠅄󠅝󠇯` | U+1ED75 U+1ED78 U+E0139 U+E015B U+E0144 U+E0144 U+E015D U+E01EF | always |
| `ýy` | `𞵝𞵵𞵸󠅛󠅆󠅄󠅝󠅙󠇯` | U+1ED5D U+1ED75 U+1ED78 U+E015B U+E0146 U+E0144 U+E015D U+E0159 U+E01EF | at the start of a word |
| `ýy` | `𞵵𞵸󠅛󠅆󠅄󠅝󠅙󠇯` | U+1ED75 U+1ED78 U+E015B U+E0146 U+E0144 U+E015D U+E0159 U+E01EF | always |
| `ýY` | `𞵝𞵵𞵸󠅛󠅆󠅄󠅝󠄹󠇯` | U+1ED5D U+1ED75 U+1ED78 U+E015B U+E0146 U+E0144 U+E015D U+E0139 U+E01EF | at the start of a word |
| `ýY` | `𞵵𞵸󠅛󠅆󠅄󠅝󠄹󠇯` | U+1ED75 U+1ED78 U+E015B U+E0146 U+E0144 U+E015D U+E0139 U+E01EF | always |
| `ýý` | `𞵝𞵵𞵸󠅛󠅆󠅄󠅝󠅛󠅆󠅄󠅝󠇯` | U+1ED5D U+1ED75 U+1ED78 U+E015B U+E0146 U+E0144 U+E015D U+E015B U+E0146 U+E0144 U+E015D U+E01EF | at the start of a word |
| `ýý` | `𞵵𞵸󠅛󠅆󠅄󠅝󠅛󠅆󠅄󠅝󠇯` | U+1ED75 U+1ED78 U+E015B U+E0146 U+E0144 U+E015D U+E015B U+E0146 U+E0144 U+E015D U+E01EF | always |
| `ýÝ` | `𞵝𞵵𞵸󠅛󠅆󠅄󠅝󠅛󠅄󠅄󠅝󠇯` | U+1ED5D U+1ED75 U+1ED78 U+E015B U+E0146 U+E0144 U+E015D U+E015B U+E0144 U+E0144 U+E015D U+E01EF | at the start of a word |
| `ýÝ` | `𞵵𞵸󠅛󠅆󠅄󠅝󠅛󠅄󠅄󠅝󠇯` | U+1ED75 U+1ED78 U+E015B U+E0146 U+E0144 U+E015D U+E015B U+E0144 U+E0144 U+E015D U+E01EF | always |
| `Ýy` | `𞵝𞵵𞵸󠅛󠅄󠅄󠅝󠅙󠇯` | U+1ED5D U+1ED75 U+1ED78 U+E015B U+E0144 U+E0144 U+E015D U+E0159 U+E01EF | at the start of a word |
| `Ýy` | `𞵵𞵸󠅛󠅄󠅄󠅝󠅙󠇯` | U+1ED75 U+1ED78 U+E015B U+E0144 U+E0144 U+E015D U+E0159 U+E01EF | always |
| `ÝY` | `𞵝𞵵𞵸󠅛󠅄󠅄󠅝󠄹󠇯` | U+1ED5D U+1ED75 U+1ED78 U+E015B U+E0144 U+E0144 U+E015D U+E0139 U+E01EF | at the start of a word |
| `ÝY` | `𞵵𞵸󠅛󠅄󠅄󠅝󠄹󠇯` | U+1ED75 U+1ED78 U+E015B U+E0144 U+E0144 U+E015D U+E0139 U+E01EF | always |
| `Ýý` | `𞵝𞵵𞵸󠅛󠅄󠅄󠅝󠅛󠅆󠅄󠅝󠇯` | U+1ED5D U+1ED75 U+1ED78 U+E015B U+E0144 U+E0144 U+E015D U+E015B U+E0146 U+E0144 U+E015D U+E01EF | at the start of a word |
| `Ýý` | `𞵵𞵸󠅛󠅄󠅄󠅝󠅛󠅆󠅄󠅝󠇯` | U+1ED75 U+1ED78 U+E015B U+E0144 U+E0144 U+E015D U+E015B U+E0146 U+E0144 U+E015D U+E01EF | always |
| `ÝÝ` | `𞵝𞵵𞵸󠅛󠅄󠅄󠅝󠅛󠅄󠅄󠅝󠇯` | U+1ED5D U+1ED75 U+1ED78 U+E015B U+E0144 U+E0144 U+E015D U+E015B U+E0144 U+E0144 U+E015D U+E01EF | at the start of a word |
| `ÝÝ` | `𞵵𞵸󠅛󠅄󠅄󠅝󠅛󠅄󠅄󠅝󠇯` | U+1ED75 U+1ED78 U+E015B U+E0144 U+E0144 U+E015D U+E015B U+E0144 U+E0144 U+E015D U+E01EF | always |
| `yë` | `𞵝𞵵𞵝𞵶󠅙󠅛󠅅󠅂󠅝󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED76 U+E0159 U+E015B U+E0145 U+E0142 U+E015D U+E01EF | at the start of a word |
| `yë` | `𞵵𞵝𞵶󠅙󠅛󠅅󠅂󠅝󠇯` | U+1ED75 U+1ED5D U+1ED76 U+E0159 U+E015B U+E0145 U+E0142 U+E015D U+E01EF | always |
| `yË` | `𞵝𞵵𞵝𞵶󠅙󠅛󠅃󠅂󠅝󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED76 U+E0159 U+E015B U+E0143 U+E0142 U+E015D U+E01EF | at the start of a word |
| `yË` | `𞵵𞵝𞵶󠅙󠅛󠅃󠅂󠅝󠇯` | U+1ED75 U+1ED5D U+1ED76 U+E0159 U+E015B U+E0143 U+E0142 U+E015D U+E01EF | always |
| `Yë` | `𞵝𞵵𞵝𞵶󠄹󠅛󠅅󠅂󠅝󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED76 U+E0139 U+E015B U+E0145 U+E0142 U+E015D U+E01EF | at the start of a word |
| `Yë` | `𞵵𞵝𞵶󠄹󠅛󠅅󠅂󠅝󠇯` | U+1ED75 U+1ED5D U+1ED76 U+E0139 U+E015B U+E0145 U+E0142 U+E015D U+E01EF | always |
| `YË` | `𞵝𞵵𞵝𞵶󠄹󠅛󠅃󠅂󠅝󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED76 U+E0139 U+E015B U+E0143 U+E0142 U+E015D U+E01EF | at the start of a word |
| `YË` | `𞵵𞵝𞵶󠄹󠅛󠅃󠅂󠅝󠇯` | U+1ED75 U+1ED5D U+1ED76 U+E0139 U+E015B U+E0143 U+E0142 U+E015D U+E01EF | always |
| `ýë` | `𞵝𞵵𞵝𞵶󠅛󠅆󠅄󠅝󠅛󠅅󠅂󠅝󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED76 U+E015B U+E0146 U+E0144 U+E015D U+E015B U+E0145 U+E0142 U+E015D U+E01EF | at the start of a word |
| `ýë` | `𞵵𞵝𞵶󠅛󠅆󠅄󠅝󠅛󠅅󠅂󠅝󠇯` | U+1ED75 U+1ED5D U+1ED76 U+E015B U+E0146 U+E0144 U+E015D U+E015B U+E0145 U+E0142 U+E015D U+E01EF | always |
| `ýË` | `𞵝𞵵𞵝𞵶󠅛󠅆󠅄󠅝󠅛󠅃󠅂󠅝󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED76 U+E015B U+E0146 U+E0144 U+E015D U+E015B U+E0143 U+E0142 U+E015D U+E01EF | at the start of a word |
| `ýË` | `𞵵𞵝𞵶󠅛󠅆󠅄󠅝󠅛󠅃󠅂󠅝󠇯` | U+1ED75 U+1ED5D U+1ED76 U+E015B U+E0146 U+E0144 U+E015D U+E015B U+E0143 U+E0142 U+E015D U+E01EF | always |
| `Ýë` | `𞵝𞵵𞵝𞵶󠅛󠅄󠅄󠅝󠅛󠅅󠅂󠅝󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED76 U+E015B U+E0144 U+E0144 U+E015D U+E015B U+E0145 U+E0142 U+E015D U+E01EF | at the start of a word |
| `Ýë` | `𞵵𞵝𞵶󠅛󠅄󠅄󠅝󠅛󠅅󠅂󠅝󠇯` | U+1ED75 U+1ED5D U+1ED76 U+E015B U+E0144 U+E0144 U+E015D U+E015B U+E0145 U+E0142 U+E015D U+E01EF | always |
| `ÝË` | `𞵝𞵵𞵝𞵶󠅛󠅄󠅄󠅝󠅛󠅃󠅂󠅝󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED76 U+E015B U+E0144 U+E0144 U+E015D U+E015B U+E0143 U+E0142 U+E015D U+E01EF | at the start of a word |
| `ÝË` | `𞵵𞵝𞵶󠅛󠅄󠅄󠅝󠅛󠅃󠅂󠅝󠇯` | U+1ED75 U+1ED5D U+1ED76 U+E015B U+E0144 U+E0144 U+E015D U+E015B U+E0143 U+E0142 U+E015D U+E01EF | always |
| `ëa` | `𞵝𞵶𞵝𞵰󠅛󠅅󠅂󠅝󠅁󠇯` | U+1ED5D U+1ED76 U+1ED5D U+1ED70 U+E015B U+E0145 U+E0142 U+E015D U+E0141 U+E01EF | at the start of a word |
| `ëa` | `𞵶𞵝𞵰󠅛󠅅󠅂󠅝󠅁󠇯` | U+1ED76 U+1ED5D U+1ED70 U+E015B U+E0145 U+E0142 U+E015D U+E0141 U+E01EF | always |
| `ëA` | `𞵝𞵶𞵝𞵰󠅛󠅅󠅂󠅝󠄡󠇯` | U+1ED5D U+1ED76 U+1ED5D U+1ED70 U+E015B U+E0145 U+E0142 U+E015D U+E0121 U+E01EF | at the start of a word |
| `ëA` | `𞵶𞵝𞵰󠅛󠅅󠅂󠅝󠄡󠇯` | U+1ED76 U+1ED5D U+1ED70 U+E015B U+E0145 U+E0142 U+E015D U+E0121 U+E01EF | always |
| `ëá` | `𞵝𞵶𞵝𞵰󠅛󠅅󠅂󠅝󠅛󠅅󠄑󠅝󠇯` | U+1ED5D U+1ED76 U+1ED5D U+1ED70 U+E015B U+E0145 U+E0142 U+E015D U+E015B U+E0145 U+E0111 U+E015D U+E01EF | at the start of a word |
| `ëá` | `𞵶𞵝𞵰󠅛󠅅󠅂󠅝󠅛󠅅󠄑󠅝󠇯` | U+1ED76 U+1ED5D U+1ED70 U+E015B U+E0145 U+E0142 U+E015D U+E015B U+E0145 U+E0111 U+E015D U+E01EF | always |
| `ëÁ` | `𞵝𞵶𞵝𞵰󠅛󠅅󠅂󠅝󠅛󠅃󠄑󠅝󠇯` | U+1ED5D U+1ED76 U+1ED5D U+1ED70 U+E015B U+E0145 U+E0142 U+E015D U+E015B U+E0143 U+E0111 U+E015D U+E01EF | at the start of a word |
| `ëÁ` | `𞵶𞵝𞵰󠅛󠅅󠅂󠅝󠅛󠅃󠄑󠅝󠇯` | U+1ED76 U+1ED5D U+1ED70 U+E015B U+E0145 U+E0142 U+E015D U+E015B U+E0143 U+E0111 U+E015D U+E01EF | always |
| `Ëa` | `𞵝𞵶𞵝𞵰󠅛󠅃󠅂󠅝󠅁󠇯` | U+1ED5D U+1ED76 U+1ED5D U+1ED70 U+E015B U+E0143 U+E0142 U+E015D U+E0141 U+E01EF | at the start of a word |
| `Ëa` | `𞵶𞵝𞵰󠅛󠅃󠅂󠅝󠅁󠇯` | U+1ED76 U+1ED5D U+1ED70 U+E015B U+E0143 U+E0142 U+E015D U+E0141 U+E01EF | always |
| `ËA` | `𞵝𞵶𞵝𞵰󠅛󠅃󠅂󠅝󠄡󠇯` | U+1ED5D U+1ED76 U+1ED5D U+1ED70 U+E015B U+E0143 U+E0142 U+E015D U+E0121 U+E01EF | at the start of a word |
| `ËA` | `𞵶𞵝𞵰󠅛󠅃󠅂󠅝󠄡󠇯` | U+1ED76 U+1ED5D U+1ED70 U+E015B U+E0143 U+E0142 U+E015D U+E0121 U+E01EF | always |
| `Ëá` | `𞵝𞵶𞵝𞵰󠅛󠅃󠅂󠅝󠅛󠅅󠄑󠅝󠇯` | U+1ED5D U+1ED76 U+1ED5D U+1ED70 U+E015B U+E0143 U+E0142 U+E015D U+E015B U+E0145 U+E0111 U+E015D U+E01EF | at the start of a word |
| `Ëá` | `𞵶𞵝𞵰󠅛󠅃󠅂󠅝󠅛󠅅󠄑󠅝󠇯` | U+1ED76 U+1ED5D U+1ED70 U+E015B U+E0143 U+E0142 U+E015D U+E015B U+E0145 U+E0111 U+E015D U+E01EF | always |
| `ËÁ` | `𞵝𞵶𞵝𞵰󠅛󠅃󠅂󠅝󠅛󠅃󠄑󠅝󠇯` | U+1ED5D U+1ED76 U+1ED5D U+1ED70 U+E015B U+E0143 U+E0142 U+E015D U+E015B U+E0143 U+E0111 U+E015D U+E01EF | at the start of a word |
| `ËÁ` | `𞵶𞵝𞵰󠅛󠅃󠅂󠅝󠅛󠅃󠄑󠅝󠇯` | U+1ED76 U+1ED5D U+1ED70 U+E015B U+E0143 U+E0142 U+E015D U+E015B U+E0143 U+E0111 U+E015D U+E01EF | always |
| `ëe` | `𞵝𞵶𞵝𞵳󠅛󠅅󠅂󠅝󠅅󠇯` | U+1ED5D U+1ED76 U+1ED5D U+1ED73 U+E015B U+E0145 U+E0142 U+E015D U+E0145 U+E01EF | at the start of a word |
| `ëe` | `𞵶𞵝𞵳󠅛󠅅󠅂󠅝󠅅󠇯` | U+1ED76 U+1ED5D U+1ED73 U+E015B U+E0145 U+E0142 U+E015D U+E0145 U+E01EF | always |
| `ëE` | `𞵝𞵶𞵝𞵳󠅛󠅅󠅂󠅝󠄥󠇯` | U+1ED5D U+1ED76 U+1ED5D U+1ED73 U+E015B U+E0145 U+E0142 U+E015D U+E0125 U+E01EF | at the start of a word |
| `ëE` | `𞵶𞵝𞵳󠅛󠅅󠅂󠅝󠄥󠇯` | U+1ED76 U+1ED5D U+1ED73 U+E015B U+E0145 U+E0142 U+E015D U+E0125 U+E01EF | always |
| `ëé` | `𞵝𞵶𞵝𞵳󠅛󠅅󠅂󠅝󠅛󠅅󠄙󠅝󠇯` | U+1ED5D U+1ED76 U+1ED5D U+1ED73 U+E015B U+E0145 U+E0142 U+E015D U+E015B U+E0145 U+E0119 U+E015D U+E01EF | at the start of a word |
| `ëé` | `𞵶𞵝𞵳󠅛󠅅󠅂󠅝󠅛󠅅󠄙󠅝󠇯` | U+1ED76 U+1ED5D U+1ED73 U+E015B U+E0145 U+E0142 U+E015D U+E015B U+E0145 U+E0119 U+E015D U+E01EF | always |
| `ëÉ` | `𞵝𞵶𞵝𞵳󠅛󠅅󠅂󠅝󠅛󠅃󠄙󠅝󠇯` | U+1ED5D U+1ED76 U+1ED5D U+1ED73 U+E015B U+E0145 U+E0142 U+E015D U+E015B U+E0143 U+E0119 U+E015D U+E01EF | at the start of a word |
| `ëÉ` | `𞵶𞵝𞵳󠅛󠅅󠅂󠅝󠅛󠅃󠄙󠅝󠇯` | U+1ED76 U+1ED5D U+1ED73 U+E015B U+E0145 U+E0142 U+E015D U+E015B U+E0143 U+E0119 U+E015D U+E01EF | always |
| `Ëe` | `𞵝𞵶𞵝𞵳󠅛󠅃󠅂󠅝󠅅󠇯` | U+1ED5D U+1ED76 U+1ED5D U+1ED73 U+E015B U+E0143 U+E0142 U+E015D U+E0145 U+E01EF | at the start of a word |
| `Ëe` | `𞵶𞵝𞵳󠅛󠅃󠅂󠅝󠅅󠇯` | U+1ED76 U+1ED5D U+1ED73 U+E015B U+E0143 U+E0142 U+E015D U+E0145 U+E01EF | always |
| `ËE` | `𞵝𞵶𞵝𞵳󠅛󠅃󠅂󠅝󠄥󠇯` | U+1ED5D U+1ED76 U+1ED5D U+1ED73 U+E015B U+E0143 U+E0142 U+E015D U+E0125 U+E01EF | at the start of a word |
| `ËE` | `𞵶𞵝𞵳󠅛󠅃󠅂󠅝󠄥󠇯` | U+1ED76 U+1ED5D U+1ED73 U+E015B U+E0143 U+E0142 U+E015D U+E0125 U+E01EF | always |
| `Ëé` | `𞵝𞵶𞵝𞵳󠅛󠅃󠅂󠅝󠅛󠅅󠄙󠅝󠇯` | U+1ED5D U+1ED76 U+1ED5D U+1ED73 U+E015B U+E0143 U+E0142 U+E015D U+E015B U+E0145 U+E0119 U+E015D U+E01EF | at the start of a word |
| `Ëé` | `𞵶𞵝𞵳󠅛󠅃󠅂󠅝󠅛󠅅󠄙󠅝󠇯` | U+1ED76 U+1ED5D U+1ED73 U+E015B U+E0143 U+E0142 U+E015D U+E015B U+E0145 U+E0119 U+E015D U+E01EF | always |
| `ËÉ` | `𞵝𞵶𞵝𞵳󠅛󠅃󠅂󠅝󠅛󠅃󠄙󠅝󠇯` | U+1ED5D U+1ED76 U+1ED5D U+1ED73 U+E015B U+E0143 U+E0142 U+E015D U+E015B U+E0143 U+E0119 U+E015D U+E01EF | at the start of a word |
| `ËÉ` | `𞵶𞵝𞵳󠅛󠅃󠅂󠅝󠅛󠅃󠄙󠅝󠇯` | U+1ED76 U+1ED5D U+1ED73 U+E015B U+E0143 U+E0142 U+E015D U+E015B U+E0143 U+E0119 U+E015D U+E01EF | always |
| `ëi` | `𞵝𞵶𞵝𞵴󠅛󠅅󠅂󠅝󠅉󠇯` | U+1ED5D U+1ED76 U+1ED5D U+1ED74 U+E015B U+E0145 U+E0142 U+E015D U+E0149 U+E01EF | at the start of a word |
| `ëi` | `𞵶𞵝𞵴󠅛󠅅󠅂󠅝󠅉󠇯` | U+1ED76 U+1ED5D U+1ED74 U+E015B U+E0145 U+E0142 U+E015D U+E0149 U+E01EF | always |
| `ëI` | `𞵝𞵶𞵝𞵴󠅛󠅅󠅂󠅝󠄩󠇯` | U+1ED5D U+1ED76 U+1ED5D U+1ED74 U+E015B U+E0145 U+E0142 U+E015D U+E0129 U+E01EF | at the start of a word |
| `ëI` | `𞵶𞵝𞵴󠅛󠅅󠅂󠅝󠄩󠇯` | U+1ED76 U+1ED5D U+1ED74 U+E015B U+E0145 U+E0142 U+E015D U+E0129 U+E01EF | always |
| `ëí` | `𞵝𞵶𞵝𞵴󠅛󠅅󠅂󠅝󠅛󠅅󠅄󠅝󠇯` | U+1ED5D U+1ED76 U+1ED5D U+1ED74 U+E015B U+E0145 U+E0142 U+E015D U+E015B U+E0145 U+E0144 U+E015D U+E01EF | at the start of a word |
| `ëí` | `𞵶𞵝𞵴󠅛󠅅󠅂󠅝󠅛󠅅󠅄󠅝󠇯` | U+1ED76 U+1ED5D U+1ED74 U+E015B U+E0145 U+E0142 U+E015D U+E015B U+E0145 U+E0144 U+E015D U+E01EF | always |
| `ëÍ` | `𞵝𞵶𞵝𞵴󠅛󠅅󠅂󠅝󠅛󠅃󠅄󠅝󠇯` | U+1ED5D U+1ED76 U+1ED5D U+1ED74 U+E015B U+E0145 U+E0142 U+E015D U+E015B U+E0143 U+E0144 U+E015D U+E01EF | at the start of a word |
| `ëÍ` | `𞵶𞵝𞵴󠅛󠅅󠅂󠅝󠅛󠅃󠅄󠅝󠇯` | U+1ED76 U+1ED5D U+1ED74 U+E015B U+E0145 U+E0142 U+E015D U+E015B U+E0143 U+E0144 U+E015D U+E01EF | always |
| `Ëi` | `𞵝𞵶𞵝𞵴󠅛󠅃󠅂󠅝󠅉󠇯` | U+1ED5D U+1ED76 U+1ED5D U+1ED74 U+E015B U+E0143 U+E0142 U+E015D U+E0149 U+E01EF | at the start of a word |
| `Ëi` | `𞵶𞵝𞵴󠅛󠅃󠅂󠅝󠅉󠇯` | U+1ED76 U+1ED5D U+1ED74 U+E015B U+E0143 U+E0142 U+E015D U+E0149 U+E01EF | always |
| `ËI` | `𞵝𞵶𞵝𞵴󠅛󠅃󠅂󠅝󠄩󠇯` | U+1ED5D U+1ED76 U+1ED5D U+1ED74 U+E015B U+E0143 U+E0142 U+E015D U+E0129 U+E01EF | at the start of a word |
| `ËI` | `𞵶𞵝𞵴󠅛󠅃󠅂󠅝󠄩󠇯` | U+1ED76 U+1ED5D U+1ED74 U+E015B U+E0143 U+E0142 U+E015D U+E0129 U+E01EF | always |
| `Ëí` | `𞵝𞵶𞵝𞵴󠅛󠅃󠅂󠅝󠅛󠅅󠅄󠅝󠇯` | U+1ED5D U+1ED76 U+1ED5D U+1ED74 U+E015B U+E0143 U+E0142 U+E015D U+E015B U+E0145 U+E0144 U+E015D U+E01EF | at the start of a word |
| `Ëí` | `𞵶𞵝𞵴󠅛󠅃󠅂󠅝󠅛󠅅󠅄󠅝󠇯` | U+1ED76 U+1ED5D U+1ED74 U+E015B U+E0143 U+E0142 U+E015D U+E015B U+E0145 U+E0144 U+E015D U+E01EF | always |
| `ËÍ` | `𞵝𞵶𞵝𞵴󠅛󠅃󠅂󠅝󠅛󠅃󠅄󠅝󠇯` | U+1ED5D U+1ED76 U+1ED5D U+1ED74 U+E015B U+E0143 U+E0142 U+E015D U+E015B U+E0143 U+E0144 U+E015D U+E01EF | at the start of a word |
| `ËÍ` | `𞵶𞵝𞵴󠅛󠅃󠅂󠅝󠅛󠅃󠅄󠅝󠇯` | U+1ED76 U+1ED5D U+1ED74 U+E015B U+E0143 U+E0142 U+E015D U+E015B U+E0143 U+E0144 U+E015D U+E01EF | always |
| `ëo` | `𞵝𞵶𞵝𞵱󠅛󠅅󠅂󠅝󠅏󠇯` | U+1ED5D U+1ED76 U+1ED5D U+1ED71 U+E015B U+E0145 U+E0142 U+E015D U+E014F U+E01EF | at the start of a word |
| `ëo` | `𞵶𞵝𞵱󠅛󠅅󠅂󠅝󠅏󠇯` | U+1ED76 U+1ED5D U+1ED71 U+E015B U+E0145 U+E0142 U+E015D U+E014F U+E01EF | always |
| `ëO` | `𞵝𞵶𞵝𞵱󠅛󠅅󠅂󠅝󠄯󠇯` | U+1ED5D U+1ED76 U+1ED5D U+1ED71 U+E015B U+E0145 U+E0142 U+E015D U+E012F U+E01EF | at the start of a word |
| `ëO` | `𞵶𞵝𞵱󠅛󠅅󠅂󠅝󠄯󠇯` | U+1ED76 U+1ED5D U+1ED71 U+E015B U+E0145 U+E0142 U+E015D U+E012F U+E01EF | always |
| `ëó` | `𞵝𞵶𞵝𞵱󠅛󠅅󠅂󠅝󠅛󠅆󠄓󠅝󠇯` | U+1ED5D U+1ED76 U+1ED5D U+1ED71 U+E015B U+E0145 U+E0142 U+E015D U+E015B U+E0146 U+E0113 U+E015D U+E01EF | at the start of a word |
| `ëó` | `𞵶𞵝𞵱󠅛󠅅󠅂󠅝󠅛󠅆󠄓󠅝󠇯` | U+1ED76 U+1ED5D U+1ED71 U+E015B U+E0145 U+E0142 U+E015D U+E015B U+E0146 U+E0113 U+E015D U+E01EF | always |
| `ëÓ` | `𞵝𞵶𞵝𞵱󠅛󠅅󠅂󠅝󠅛󠅄󠄓󠅝󠇯` | U+1ED5D U+1ED76 U+1ED5D U+1ED71 U+E015B U+E0145 U+E0142 U+E015D U+E015B U+E0144 U+E0113 U+E015D U+E01EF | at the start of a word |
| `ëÓ` | `𞵶𞵝𞵱󠅛󠅅󠅂󠅝󠅛󠅄󠄓󠅝󠇯` | U+1ED76 U+1ED5D U+1ED71 U+E015B U+E0145 U+E0142 U+E015D U+E015B U+E0144 U+E0113 U+E015D U+E01EF | always |
| `Ëo` | `𞵝𞵶𞵝𞵱󠅛󠅃󠅂󠅝󠅏󠇯` | U+1ED5D U+1ED76 U+1ED5D U+1ED71 U+E015B U+E0143 U+E0142 U+E015D U+E014F U+E01EF | at the start of a word |
| `Ëo` | `𞵶𞵝𞵱󠅛󠅃󠅂󠅝󠅏󠇯` | U+1ED76 U+1ED5D U+1ED71 U+E015B U+E0143 U+E0142 U+E015D U+E014F U+E01EF | always |
| `ËO` | `𞵝𞵶𞵝𞵱󠅛󠅃󠅂󠅝󠄯󠇯` | U+1ED5D U+1ED76 U+1ED5D U+1ED71 U+E015B U+E0143 U+E0142 U+E015D U+E012F U+E01EF | at the start of a word |
| `ËO` | `𞵶𞵝𞵱󠅛󠅃󠅂󠅝󠄯󠇯` | U+1ED76 U+1ED5D U+1ED71 U+E015B U+E0143 U+E0142 U+E015D U+E012F U+E01EF | always |
| `Ëó` | `𞵝𞵶𞵝𞵱󠅛󠅃󠅂󠅝󠅛󠅆󠄓󠅝󠇯` | U+1ED5D U+1ED76 U+1ED5D U+1ED71 U+E015B U+E0143 U+E0142 U+E015D U+E015B U+E0146 U+E0113 U+E015D U+E01EF | at the start of a word |
| `Ëó` | `𞵶𞵝𞵱󠅛󠅃󠅂󠅝󠅛󠅆󠄓󠅝󠇯` | U+1ED76 U+1ED5D U+1ED71 U+E015B U+E0143 U+E0142 U+E015D U+E015B U+E0146 U+E0113 U+E015D U+E01EF | always |
| `ËÓ` | `𞵝𞵶𞵝𞵱󠅛󠅃󠅂󠅝󠅛󠅄󠄓󠅝󠇯` | U+1ED5D U+1ED76 U+1ED5D U+1ED71 U+E015B U+E0143 U+E0142 U+E015D U+E015B U+E0144 U+E0113 U+E015D U+E01EF | at the start of a word |
| `ËÓ` | `𞵶𞵝𞵱󠅛󠅃󠅂󠅝󠅛󠅄󠄓󠅝󠇯` | U+1ED76 U+1ED5D U+1ED71 U+E015B U+E0143 U+E0142 U+E015D U+E015B U+E0144 U+E0113 U+E015D U+E01EF | always |
| `ëu` | `𞵝𞵶𞵝𞵲󠅛󠅅󠅂󠅝󠅕󠇯` | U+1ED5D U+1ED76 U+1ED5D U+1ED72 U+E015B U+E0145 U+E0142 U+E015D U+E0155 U+E01EF | at the start of a word |
| `ëu` | `𞵶𞵝𞵲󠅛󠅅󠅂󠅝󠅕󠇯` | U+1ED76 U+1ED5D U+1ED72 U+E015B U+E0145 U+E0142 U+E015D U+E0155 U+E01EF | always |
| `ëU` | `𞵝𞵶𞵝𞵲󠅛󠅅󠅂󠅝󠄵󠇯` | U+1ED5D U+1ED76 U+1ED5D U+1ED72 U+E015B U+E0145 U+E0142 U+E015D U+E0135 U+E01EF | at the start of a word |
| `ëU` | `𞵶𞵝𞵲󠅛󠅅󠅂󠅝󠄵󠇯` | U+1ED76 U+1ED5D U+1ED72 U+E015B U+E0145 U+E0142 U+E015D U+E0135 U+E01EF | always |
| `ëú` | `𞵝𞵶𞵝𞵲󠅛󠅅󠅂󠅝󠅛󠅆󠅁󠅝󠇯` | U+1ED5D U+1ED76 U+1ED5D U+1ED72 U+E015B U+E0145 U+E0142 U+E015D U+E015B U+E0146 U+E0141 U+E015D U+E01EF | at the start of a word |
| `ëú` | `𞵶𞵝𞵲󠅛󠅅󠅂󠅝󠅛󠅆󠅁󠅝󠇯` | U+1ED76 U+1ED5D U+1ED72 U+E015B U+E0145 U+E0142 U+E015D U+E015B U+E0146 U+E0141 U+E015D U+E01EF | always |
| `ëÚ` | `𞵝𞵶𞵝𞵲󠅛󠅅󠅂󠅝󠅛󠅄󠅁󠅝󠇯` | U+1ED5D U+1ED76 U+1ED5D U+1ED72 U+E015B U+E0145 U+E0142 U+E015D U+E015B U+E0144 U+E0141 U+E015D U+E01EF | at the start of a word |
| `ëÚ` | `𞵶𞵝𞵲󠅛󠅅󠅂󠅝󠅛󠅄󠅁󠅝󠇯` | U+1ED76 U+1ED5D U+1ED72 U+E015B U+E0145 U+E0142 U+E015D U+E015B U+E0144 U+E0141 U+E015D U+E01EF | always |
| `Ëu` | `𞵝𞵶𞵝𞵲󠅛󠅃󠅂󠅝󠅕󠇯` | U+1ED5D U+1ED76 U+1ED5D U+1ED72 U+E015B U+E0143 U+E0142 U+E015D U+E0155 U+E01EF | at the start of a word |
| `Ëu` | `𞵶𞵝𞵲󠅛󠅃󠅂󠅝󠅕󠇯` | U+1ED76 U+1ED5D U+1ED72 U+E015B U+E0143 U+E0142 U+E015D U+E0155 U+E01EF | always |
| `ËU` | `𞵝𞵶𞵝𞵲󠅛󠅃󠅂󠅝󠄵󠇯` | U+1ED5D U+1ED76 U+1ED5D U+1ED72 U+E015B U+E0143 U+E0142 U+E015D U+E0135 U+E01EF | at the start of a word |
| `ËU` | `𞵶𞵝𞵲󠅛󠅃󠅂󠅝󠄵󠇯` | U+1ED76 U+1ED5D U+1ED72 U+E015B U+E0143 U+E0142 U+E015D U+E0135 U+E01EF | always |
| `Ëú` | `𞵝𞵶𞵝𞵲󠅛󠅃󠅂󠅝󠅛󠅆󠅁󠅝󠇯` | U+1ED5D U+1ED76 U+1ED5D U+1ED72 U+E015B U+E0143 U+E0142 U+E015D U+E015B U+E0146 U+E0141 U+E015D U+E01EF | at the start of a word |
| `Ëú` | `𞵶𞵝𞵲󠅛󠅃󠅂󠅝󠅛󠅆󠅁󠅝󠇯` | U+1ED76 U+1ED5D U+1ED72 U+E015B U+E0143 U+E0142 U+E015D U+E015B U+E0146 U+E0141 U+E015D U+E01EF | always |
| `ËÚ` | `𞵝𞵶𞵝𞵲󠅛󠅃󠅂󠅝󠅛󠅄󠅁󠅝󠇯` | U+1ED5D U+1ED76 U+1ED5D U+1ED72 U+E015B U+E0143 U+E0142 U+E015D U+E015B U+E0144 U+E0141 U+E015D U+E01EF | at the start of a word |
| `ËÚ` | `𞵶𞵝𞵲󠅛󠅃󠅂󠅝󠅛󠅄󠅁󠅝󠇯` | U+1ED76 U+1ED5D U+1ED72 U+E015B U+E0143 U+E0142 U+E015D U+E015B U+E0144 U+E0141 U+E015D U+E01EF | always |
| `ëy` | `𞵝𞵶𞵝𞵵󠅛󠅅󠅂󠅝󠅙󠇯` | U+1ED5D U+1ED76 U+1ED5D U+1ED75 U+E015B U+E0145 U+E0142 U+E015D U+E0159 U+E01EF | at the start of a word |
| `ëy` | `𞵶𞵝𞵵󠅛󠅅󠅂󠅝󠅙󠇯` | U+1ED76 U+1ED5D U+1ED75 U+E015B U+E0145 U+E0142 U+E015D U+E0159 U+E01EF | always |
| `ëY` | `𞵝𞵶𞵝𞵵󠅛󠅅󠅂󠅝󠄹󠇯` | U+1ED5D U+1ED76 U+1ED5D U+1ED75 U+E015B U+E0145 U+E0142 U+E015D U+E0139 U+E01EF | at the start of a word |
| `ëY` | `𞵶𞵝𞵵󠅛󠅅󠅂󠅝󠄹󠇯` | U+1ED76 U+1ED5D U+1ED75 U+E015B U+E0145 U+E0142 U+E015D U+E0139 U+E01EF | always |
| `ëý` | `𞵝𞵶𞵝𞵵󠅛󠅅󠅂󠅝󠅛󠅆󠅄󠅝󠇯` | U+1ED5D U+1ED76 U+1ED5D U+1ED75 U+E015B U+E0145 U+E0142 U+E015D U+E015B U+E0146 U+E0144 U+E015D U+E01EF | at the start of a word |
| `ëý` | `𞵶𞵝𞵵󠅛󠅅󠅂󠅝󠅛󠅆󠅄󠅝󠇯` | U+1ED76 U+1ED5D U+1ED75 U+E015B U+E0145 U+E0142 U+E015D U+E015B U+E0146 U+E0144 U+E015D U+E01EF | always |
| `ëÝ` | `𞵝𞵶𞵝𞵵󠅛󠅅󠅂󠅝󠅛󠅄󠅄󠅝󠇯` | U+1ED5D U+1ED76 U+1ED5D U+1ED75 U+E015B U+E0145 U+E0142 U+E015D U+E015B U+E0144 U+E0144 U+E015D U+E01EF | at the start of a word |
| `ëÝ` | `𞵶𞵝𞵵󠅛󠅅󠅂󠅝󠅛󠅄󠅄󠅝󠇯` | U+1ED76 U+1ED5D U+1ED75 U+E015B U+E0145 U+E0142 U+E015D U+E015B U+E0144 U+E0144 U+E015D U+E01EF | always |
| `Ëy` | `𞵝𞵶𞵝𞵵󠅛󠅃󠅂󠅝󠅙󠇯` | U+1ED5D U+1ED76 U+1ED5D U+1ED75 U+E015B U+E0143 U+E0142 U+E015D U+E0159 U+E01EF | at the start of a word |
| `Ëy` | `𞵶𞵝𞵵󠅛󠅃󠅂󠅝󠅙󠇯` | U+1ED76 U+1ED5D U+1ED75 U+E015B U+E0143 U+E0142 U+E015D U+E0159 U+E01EF | always |
| `ËY` | `𞵝𞵶𞵝𞵵󠅛󠅃󠅂󠅝󠄹󠇯` | U+1ED5D U+1ED76 U+1ED5D U+1ED75 U+E015B U+E0143 U+E0142 U+E015D U+E0139 U+E01EF | at the start of a word |
| `ËY` | `𞵶𞵝𞵵󠅛󠅃󠅂󠅝󠄹󠇯` | U+1ED76 U+1ED5D U+1ED75 U+E015B U+E0143 U+E0142 U+E015D U+E0139 U+E01EF | always |
| `Ëý` | `𞵝𞵶𞵝𞵵󠅛󠅃󠅂󠅝󠅛󠅆󠅄󠅝󠇯` | U+1ED5D U+1ED76 U+1ED5D U+1ED75 U+E015B U+E0143 U+E0142 U+E015D U+E015B U+E0146 U+E0144 U+E015D U+E01EF | at the start of a word |
| `Ëý` | `𞵶𞵝𞵵󠅛󠅃󠅂󠅝󠅛󠅆󠅄󠅝󠇯` | U+1ED76 U+1ED5D U+1ED75 U+E015B U+E0143 U+E0142 U+E015D U+E015B U+E0146 U+E0144 U+E015D U+E01EF | always |
| `ËÝ` | `𞵝𞵶𞵝𞵵󠅛󠅃󠅂󠅝󠅛󠅄󠅄󠅝󠇯` | U+1ED5D U+1ED76 U+1ED5D U+1ED75 U+E015B U+E0143 U+E0142 U+E015D U+E015B U+E0144 U+E0144 U+E015D U+E01EF | at the start of a word |
| `ËÝ` | `𞵶𞵝𞵵󠅛󠅃󠅂󠅝󠅛󠅄󠅄󠅝󠇯` | U+1ED76 U+1ED5D U+1ED75 U+E015B U+E0143 U+E0142 U+E015D U+E015B U+E0144 U+E0144 U+E015D U+E01EF | always |
| `ëë` | `𞵝𞵶𞵸󠅛󠅅󠅂󠅝󠅛󠅅󠅂󠅝󠇯` | U+1ED5D U+1ED76 U+1ED78 U+E015B U+E0145 U+E0142 U+E015D U+E015B U+E0145 U+E0142 U+E015D U+E01EF | at the start of a word |
| `ëë` | `𞵶𞵸󠅛󠅅󠅂󠅝󠅛󠅅󠅂󠅝󠇯` | U+1ED76 U+1ED78 U+E015B U+E0145 U+E0142 U+E015D U+E015B U+E0145 U+E0142 U+E015D U+E01EF | always |
| `ëË` | `𞵝𞵶𞵸󠅛󠅅󠅂󠅝󠅛󠅃󠅂󠅝󠇯` | U+1ED5D U+1ED76 U+1ED78 U+E015B U+E0145 U+E0142 U+E015D U+E015B U+E0143 U+E0142 U+E015D U+E01EF | at the start of a word |
| `ëË` | `𞵶𞵸󠅛󠅅󠅂󠅝󠅛󠅃󠅂󠅝󠇯` | U+1ED76 U+1ED78 U+E015B U+E0145 U+E0142 U+E015D U+E015B U+E0143 U+E0142 U+E015D U+E01EF | always |
| `Ëë` | `𞵝𞵶𞵸󠅛󠅃󠅂󠅝󠅛󠅅󠅂󠅝󠇯` | U+1ED5D U+1ED76 U+1ED78 U+E015B U+E0143 U+E0142 U+E015D U+E015B U+E0145 U+E0142 U+E015D U+E01EF | at the start of a word |
| `Ëë` | `𞵶𞵸󠅛󠅃󠅂󠅝󠅛󠅅󠅂󠅝󠇯` | U+1ED76 U+1ED78 U+E015B U+E0143 U+E0142 U+E015D U+E015B U+E0145 U+E0142 U+E015D U+E01EF | always |
| `ËË` | `𞵝𞵶𞵸󠅛󠅃󠅂󠅝󠅛󠅃󠅂󠅝󠇯` | U+1ED5D U+1ED76 U+1ED78 U+E015B U+E0143 U+E0142 U+E015D U+E015B U+E0143 U+E0142 U+E015D U+E01EF | at the start of a word |
| `ËË` | `𞵶𞵸󠅛󠅃󠅂󠅝󠅛󠅃󠅂󠅝󠇯` | U+1ED76 U+1ED78 U+E015B U+E0143 U+E0142 U+E015D U+E015B U+E0143 U+E0142 U+E015D U+E01EF | always |

## Round trip

Every encoding round-trips exactly: decoding the code points that encoding wrote gives back the roman text, and encoding that gives the same code points. The Code points column shows every character a row writes, including any that is invisible.

This page is written from `encodings/veldikko-aelendi.json` by `tools/encoding_docs.py`.
