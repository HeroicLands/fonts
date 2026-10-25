# thuravark encoding

Thuravark Carved is a row of straight staves for letters, numerals and a few marks, read left to right. This encoding writes a roman spelling in them: a digraph such as `th` or `kh` is a single stave, a doubled vowel is the stave twice, and a hyphen draws nothing and is written as an invisible mark.

## Fonts

- Thuravark Carved (`thuravark-carved`), written left to right.

## Running it

`encode.py` needs only Python 3.9 or later. From a checkout, or from `node_modules/@heroiclands/fonts`:

```sh
python3 encode.py --encoding thuravark "kitha"
python3 encode.py --encoding thuravark --decode "󰄋󰄂󰄠󰄀"
```

The first command writes `󰄋󰄂󰄠󰄀`, and the second reads it back as `kitha`. `--codepoints` prints the result as `U+XXXX` values, and the text may come from standard input.

From Python:

```python
import encode

text = encode.encode("thuravark", "kitha")
roman = encode.decode("thuravark", text)
```

## Vowels and conditions

The vowels are `AEIOUaeiouÁÉËÍÓÚáéëíóú`.

A row marked _before a vowel_ applies when the next character is a vowel.

Where several rows begin with the same roman, the longest wins, and among rows of one length a row whose condition holds comes before a row with none. A row whose condition fails is skipped.

## Rows

The rows are in the order the file states them.

| Roman | Character | Code points | When |
| --- | --- | --- | --- |
| `a` | `󰄀` | U+F0100 | always |
| `A` | `󰄀󠄡󠇯` | U+F0100 U+E0121 U+E01EF | always |
| `e` | `󰄁` | U+F0101 | always |
| `ë` | `󰄁󠅛󠅅󠅂󠅝󠇯` | U+F0101 U+E015B U+E0145 U+E0142 U+E015D U+E01EF | always |
| `E` | `󰄁󠄥󠇯` | U+F0101 U+E0125 U+E01EF | always |
| `Ë` | `󰄁󠅛󠅃󠅂󠅝󠇯` | U+F0101 U+E015B U+E0143 U+E0142 U+E015D U+E01EF | always |
| `i` | `󰄂` | U+F0102 | always |
| `I` | `󰄂󠄩󠇯` | U+F0102 U+E0129 U+E01EF | always |
| `o` | `󰄃` | U+F0103 | always |
| `O` | `󰄃󠄯󠇯` | U+F0103 U+E012F U+E01EF | always |
| `u` | `󰄄` | U+F0104 | always |
| `U` | `󰄄󠄵󠇯` | U+F0104 U+E0135 U+E01EF | always |
| `b` | `󰄅` | U+F0105 | always |
| `B` | `󰄅󠄢󠇯` | U+F0105 U+E0122 U+E01EF | always |
| `d` | `󰄆` | U+F0106 | always |
| `D` | `󰄆󠄤󠇯` | U+F0106 U+E0124 U+E01EF | always |
| `f` | `󰄇` | U+F0107 | always |
| `F` | `󰄇󠄦󠇯` | U+F0107 U+E0126 U+E01EF | always |
| `g` | `󰄈` | U+F0108 | always |
| `G` | `󰄈󠄧󠇯` | U+F0108 U+E0127 U+E01EF | always |
| `h` | `󰄉` | U+F0109 | always |
| `H` | `󰄉󠄨󠇯` | U+F0109 U+E0128 U+E01EF | always |
| `j` | `󰄊` | U+F010A | always |
| `J` | `󰄊󠄪󠇯` | U+F010A U+E012A U+E01EF | always |
| `k` | `󰄋` | U+F010B | always |
| `K` | `󰄋󠄫󠇯` | U+F010B U+E012B U+E01EF | always |
| `q` | `󰄋󠅑󠇯` | U+F010B U+E0151 U+E01EF | always |
| `Q` | `󰄋󠄱󠇯` | U+F010B U+E0131 U+E01EF | always |
| `l` | `󰄌` | U+F010C | always |
| `L` | `󰄌󠄬󠇯` | U+F010C U+E012C U+E01EF | always |
| `m` | `󰄍` | U+F010D | always |
| `M` | `󰄍󠄭󠇯` | U+F010D U+E012D U+E01EF | always |
| `n` | `󰄎` | U+F010E | always |
| `N` | `󰄎󠄮󠇯` | U+F010E U+E012E U+E01EF | always |
| `p` | `󰄏` | U+F010F | always |
| `P` | `󰄏󠄰󠇯` | U+F010F U+E0130 U+E01EF | always |
| `r` | `󰄐` | U+F0110 | always |
| `R` | `󰄐󠄲󠇯` | U+F0110 U+E0132 U+E01EF | always |
| `s` | `󰄑` | U+F0111 | always |
| `S` | `󰄑󠄳󠇯` | U+F0111 U+E0133 U+E01EF | always |
| `t` | `󰄒` | U+F0112 | always |
| `T` | `󰄒󠄴󠇯` | U+F0112 U+E0134 U+E01EF | always |
| `v` | `󰄓` | U+F0113 | always |
| `V` | `󰄓󠄶󠇯` | U+F0113 U+E0136 U+E01EF | always |
| `w` | `󰄔` | U+F0114 | always |
| `W` | `󰄔󠄷󠇯` | U+F0114 U+E0137 U+E01EF | always |
| `z` | `󰄕` | U+F0115 | always |
| `Z` | `󰄕󠄺󠇯` | U+F0115 U+E013A U+E01EF | always |
| `á` | `󰄀󰅈` | U+F0100 U+F0148 | always |
| `Á` | `󰄀󰅈󠅛󠅃󠄑󠅝󠇯` | U+F0100 U+F0148 U+E015B U+E0143 U+E0111 U+E015D U+E01EF | always |
| `é` | `󰄁󰅈` | U+F0101 U+F0148 | always |
| `É` | `󰄁󰅈󠅛󠅃󠄙󠅝󠇯` | U+F0101 U+F0148 U+E015B U+E0143 U+E0119 U+E015D U+E01EF | always |
| `í` | `󰄂󰅈` | U+F0102 U+F0148 | always |
| `Í` | `󰄂󰅈󠅛󠅃󠅄󠅝󠇯` | U+F0102 U+F0148 U+E015B U+E0143 U+E0144 U+E015D U+E01EF | always |
| `ó` | `󰄃󰅈` | U+F0103 U+F0148 | always |
| `Ó` | `󰄃󰅈󠅛󠅄󠄓󠅝󠇯` | U+F0103 U+F0148 U+E015B U+E0144 U+E0113 U+E015D U+E01EF | always |
| `ú` | `󰄄󰅈` | U+F0104 U+F0148 | always |
| `Ú` | `󰄄󰅈󠅛󠅄󠅁󠅝󠇯` | U+F0104 U+F0148 U+E015B U+E0144 U+E0141 U+E015D U+E01EF | always |
| `th` | `󰄠` | U+F0120 | always |
| `tH` | `󰄠󠅔󠄨󠇯` | U+F0120 U+E0154 U+E0128 U+E01EF | always |
| `Th` | `󰄠󠄴󠅈󠇯` | U+F0120 U+E0134 U+E0148 U+E01EF | always |
| `TH` | `󰄠󠄴󠄨󠇯` | U+F0120 U+E0134 U+E0128 U+E01EF | always |
| `dh` | `󰄡` | U+F0121 | always |
| `dH` | `󰄡󠅄󠄨󠇯` | U+F0121 U+E0144 U+E0128 U+E01EF | always |
| `Dh` | `󰄡󠄤󠅈󠇯` | U+F0121 U+E0124 U+E0148 U+E01EF | always |
| `DH` | `󰄡󠄤󠄨󠇯` | U+F0121 U+E0124 U+E0128 U+E01EF | always |
| `kh` | `󰄢` | U+F0122 | always |
| `kH` | `󰄢󠅋󠄨󠇯` | U+F0122 U+E014B U+E0128 U+E01EF | always |
| `Kh` | `󰄢󠄫󠅈󠇯` | U+F0122 U+E012B U+E0148 U+E01EF | always |
| `KH` | `󰄢󠄫󠄨󠇯` | U+F0122 U+E012B U+E0128 U+E01EF | always |
| `gh` | `󰄣` | U+F0123 | always |
| `gH` | `󰄣󠅇󠄨󠇯` | U+F0123 U+E0147 U+E0128 U+E01EF | always |
| `Gh` | `󰄣󠄧󠅈󠇯` | U+F0123 U+E0127 U+E0148 U+E01EF | always |
| `GH` | `󰄣󠄧󠄨󠇯` | U+F0123 U+E0127 U+E0128 U+E01EF | always |
| `ng` | `󰄥` | U+F0125 | always |
| `nG` | `󰄥󠅎󠄧󠇯` | U+F0125 U+E014E U+E0127 U+E01EF | always |
| `Ng` | `󰄥󠄮󠅇󠇯` | U+F0125 U+E012E U+E0147 U+E01EF | always |
| `NG` | `󰄥󠄮󠄧󠇯` | U+F0125 U+E012E U+E0127 U+E01EF | always |
| `hl` | `󰄤` | U+F0124 | always |
| `hL` | `󰄤󠅈󠄬󠇯` | U+F0124 U+E0148 U+E012C U+E01EF | always |
| `Hl` | `󰄤󠄨󠅌󠇯` | U+F0124 U+E0128 U+E014C U+E01EF | always |
| `HL` | `󰄤󠄨󠄬󠇯` | U+F0124 U+E0128 U+E012C U+E01EF | always |
| `ngh` | `󰄎󰄣󠅎󠅇󠅈󠇯` | U+F010E U+F0123 U+E014E U+E0147 U+E0148 U+E01EF | always |
| `ngH` | `󰄎󰄣󠅎󠅇󠄨󠇯` | U+F010E U+F0123 U+E014E U+E0147 U+E0128 U+E01EF | always |
| `nGh` | `󰄎󰄣󠅎󠄧󠅈󠇯` | U+F010E U+F0123 U+E014E U+E0127 U+E0148 U+E01EF | always |
| `nGH` | `󰄎󰄣󠅎󠄧󠄨󠇯` | U+F010E U+F0123 U+E014E U+E0127 U+E0128 U+E01EF | always |
| `Ngh` | `󰄎󰄣󠄮󠅇󠅈󠇯` | U+F010E U+F0123 U+E012E U+E0147 U+E0148 U+E01EF | always |
| `NgH` | `󰄎󰄣󠄮󠅇󠄨󠇯` | U+F010E U+F0123 U+E012E U+E0147 U+E0128 U+E01EF | always |
| `NGh` | `󰄎󰄣󠄮󠄧󠅈󠇯` | U+F010E U+F0123 U+E012E U+E0127 U+E0148 U+E01EF | always |
| `NGH` | `󰄎󰄣󠄮󠄧󠄨󠇯` | U+F010E U+F0123 U+E012E U+E0127 U+E0128 U+E01EF | always |
| `tth` | `󰄠󰄠󠅔󠅔󠅈󠇯` | U+F0120 U+F0120 U+E0154 U+E0154 U+E0148 U+E01EF | always |
| `ttH` | `󰄠󰄠󠅔󠅔󠄨󠇯` | U+F0120 U+F0120 U+E0154 U+E0154 U+E0128 U+E01EF | always |
| `tTh` | `󰄠󰄠󠅔󠄴󠅈󠇯` | U+F0120 U+F0120 U+E0154 U+E0134 U+E0148 U+E01EF | always |
| `tTH` | `󰄠󰄠󠅔󠄴󠄨󠇯` | U+F0120 U+F0120 U+E0154 U+E0134 U+E0128 U+E01EF | always |
| `Tth` | `󰄠󰄠󠄴󠅔󠅈󠇯` | U+F0120 U+F0120 U+E0134 U+E0154 U+E0148 U+E01EF | always |
| `TtH` | `󰄠󰄠󠄴󠅔󠄨󠇯` | U+F0120 U+F0120 U+E0134 U+E0154 U+E0128 U+E01EF | always |
| `TTh` | `󰄠󰄠󠄴󠄴󠅈󠇯` | U+F0120 U+F0120 U+E0134 U+E0134 U+E0148 U+E01EF | always |
| `TTH` | `󰄠󰄠󠄴󠄴󠄨󠇯` | U+F0120 U+F0120 U+E0134 U+E0134 U+E0128 U+E01EF | always |
| `ddh` | `󰄡󰄡󠅄󠅄󠅈󠇯` | U+F0121 U+F0121 U+E0144 U+E0144 U+E0148 U+E01EF | always |
| `ddH` | `󰄡󰄡󠅄󠅄󠄨󠇯` | U+F0121 U+F0121 U+E0144 U+E0144 U+E0128 U+E01EF | always |
| `dDh` | `󰄡󰄡󠅄󠄤󠅈󠇯` | U+F0121 U+F0121 U+E0144 U+E0124 U+E0148 U+E01EF | always |
| `dDH` | `󰄡󰄡󠅄󠄤󠄨󠇯` | U+F0121 U+F0121 U+E0144 U+E0124 U+E0128 U+E01EF | always |
| `Ddh` | `󰄡󰄡󠄤󠅄󠅈󠇯` | U+F0121 U+F0121 U+E0124 U+E0144 U+E0148 U+E01EF | always |
| `DdH` | `󰄡󰄡󠄤󠅄󠄨󠇯` | U+F0121 U+F0121 U+E0124 U+E0144 U+E0128 U+E01EF | always |
| `DDh` | `󰄡󰄡󠄤󠄤󠅈󠇯` | U+F0121 U+F0121 U+E0124 U+E0124 U+E0148 U+E01EF | always |
| `DDH` | `󰄡󰄡󠄤󠄤󠄨󠇯` | U+F0121 U+F0121 U+E0124 U+E0124 U+E0128 U+E01EF | always |
| `kkh` | `󰄢󰄢󠅋󠅋󠅈󠇯` | U+F0122 U+F0122 U+E014B U+E014B U+E0148 U+E01EF | always |
| `kkH` | `󰄢󰄢󠅋󠅋󠄨󠇯` | U+F0122 U+F0122 U+E014B U+E014B U+E0128 U+E01EF | always |
| `kKh` | `󰄢󰄢󠅋󠄫󠅈󠇯` | U+F0122 U+F0122 U+E014B U+E012B U+E0148 U+E01EF | always |
| `kKH` | `󰄢󰄢󠅋󠄫󠄨󠇯` | U+F0122 U+F0122 U+E014B U+E012B U+E0128 U+E01EF | always |
| `Kkh` | `󰄢󰄢󠄫󠅋󠅈󠇯` | U+F0122 U+F0122 U+E012B U+E014B U+E0148 U+E01EF | always |
| `KkH` | `󰄢󰄢󠄫󠅋󠄨󠇯` | U+F0122 U+F0122 U+E012B U+E014B U+E0128 U+E01EF | always |
| `KKh` | `󰄢󰄢󠄫󠄫󠅈󠇯` | U+F0122 U+F0122 U+E012B U+E012B U+E0148 U+E01EF | always |
| `KKH` | `󰄢󰄢󠄫󠄫󠄨󠇯` | U+F0122 U+F0122 U+E012B U+E012B U+E0128 U+E01EF | always |
| `ggh` | `󰄣󰄣󠅇󠅇󠅈󠇯` | U+F0123 U+F0123 U+E0147 U+E0147 U+E0148 U+E01EF | always |
| `ggH` | `󰄣󰄣󠅇󠅇󠄨󠇯` | U+F0123 U+F0123 U+E0147 U+E0147 U+E0128 U+E01EF | always |
| `gGh` | `󰄣󰄣󠅇󠄧󠅈󠇯` | U+F0123 U+F0123 U+E0147 U+E0127 U+E0148 U+E01EF | always |
| `gGH` | `󰄣󰄣󠅇󠄧󠄨󠇯` | U+F0123 U+F0123 U+E0147 U+E0127 U+E0128 U+E01EF | always |
| `Ggh` | `󰄣󰄣󠄧󠅇󠅈󠇯` | U+F0123 U+F0123 U+E0127 U+E0147 U+E0148 U+E01EF | always |
| `GgH` | `󰄣󰄣󠄧󠅇󠄨󠇯` | U+F0123 U+F0123 U+E0127 U+E0147 U+E0128 U+E01EF | always |
| `GGh` | `󰄣󰄣󠄧󠄧󠅈󠇯` | U+F0123 U+F0123 U+E0127 U+E0127 U+E0148 U+E01EF | always |
| `GGH` | `󰄣󰄣󠄧󠄧󠄨󠇯` | U+F0123 U+F0123 U+E0127 U+E0127 U+E0128 U+E01EF | always |
| `nng` | `󰄥󰄥󠅎󠅎󠅇󠇯` | U+F0125 U+F0125 U+E014E U+E014E U+E0147 U+E01EF | always |
| `nnG` | `󰄥󰄥󠅎󠅎󠄧󠇯` | U+F0125 U+F0125 U+E014E U+E014E U+E0127 U+E01EF | always |
| `nNg` | `󰄥󰄥󠅎󠄮󠅇󠇯` | U+F0125 U+F0125 U+E014E U+E012E U+E0147 U+E01EF | always |
| `nNG` | `󰄥󰄥󠅎󠄮󠄧󠇯` | U+F0125 U+F0125 U+E014E U+E012E U+E0127 U+E01EF | always |
| `Nng` | `󰄥󰄥󠄮󠅎󠅇󠇯` | U+F0125 U+F0125 U+E012E U+E014E U+E0147 U+E01EF | always |
| `NnG` | `󰄥󰄥󠄮󠅎󠄧󠇯` | U+F0125 U+F0125 U+E012E U+E014E U+E0127 U+E01EF | always |
| `NNg` | `󰄥󰄥󠄮󠄮󠅇󠇯` | U+F0125 U+F0125 U+E012E U+E012E U+E0147 U+E01EF | always |
| `NNG` | `󰄥󰄥󠄮󠄮󠄧󠇯` | U+F0125 U+F0125 U+E012E U+E012E U+E0127 U+E01EF | always |
| `hhl` | `󰄤󰄤󠅈󠅈󠅌󠇯` | U+F0124 U+F0124 U+E0148 U+E0148 U+E014C U+E01EF | always |
| `hhL` | `󰄤󰄤󠅈󠅈󠄬󠇯` | U+F0124 U+F0124 U+E0148 U+E0148 U+E012C U+E01EF | always |
| `hHl` | `󰄤󰄤󠅈󠄨󠅌󠇯` | U+F0124 U+F0124 U+E0148 U+E0128 U+E014C U+E01EF | always |
| `hHL` | `󰄤󰄤󠅈󠄨󠄬󠇯` | U+F0124 U+F0124 U+E0148 U+E0128 U+E012C U+E01EF | always |
| `Hhl` | `󰄤󰄤󠄨󠅈󠅌󠇯` | U+F0124 U+F0124 U+E0128 U+E0148 U+E014C U+E01EF | always |
| `HhL` | `󰄤󰄤󠄨󠅈󠄬󠇯` | U+F0124 U+F0124 U+E0128 U+E0148 U+E012C U+E01EF | always |
| `HHl` | `󰄤󰄤󠄨󠄨󠅌󠇯` | U+F0124 U+F0124 U+E0128 U+E0128 U+E014C U+E01EF | always |
| `HHL` | `󰄤󰄤󠄨󠄨󠄬󠇯` | U+F0124 U+F0124 U+E0128 U+E0128 U+E012C U+E01EF | always |
| `nngh` | `󰄎󰄎󰄣󠅎󠅎󠅇󠅈󠇯` | U+F010E U+F010E U+F0123 U+E014E U+E014E U+E0147 U+E0148 U+E01EF | always |
| `nngH` | `󰄎󰄎󰄣󠅎󠅎󠅇󠄨󠇯` | U+F010E U+F010E U+F0123 U+E014E U+E014E U+E0147 U+E0128 U+E01EF | always |
| `nnGh` | `󰄎󰄎󰄣󠅎󠅎󠄧󠅈󠇯` | U+F010E U+F010E U+F0123 U+E014E U+E014E U+E0127 U+E0148 U+E01EF | always |
| `nnGH` | `󰄎󰄎󰄣󠅎󠅎󠄧󠄨󠇯` | U+F010E U+F010E U+F0123 U+E014E U+E014E U+E0127 U+E0128 U+E01EF | always |
| `nNgh` | `󰄎󰄎󰄣󠅎󠄮󠅇󠅈󠇯` | U+F010E U+F010E U+F0123 U+E014E U+E012E U+E0147 U+E0148 U+E01EF | always |
| `nNgH` | `󰄎󰄎󰄣󠅎󠄮󠅇󠄨󠇯` | U+F010E U+F010E U+F0123 U+E014E U+E012E U+E0147 U+E0128 U+E01EF | always |
| `nNGh` | `󰄎󰄎󰄣󠅎󠄮󠄧󠅈󠇯` | U+F010E U+F010E U+F0123 U+E014E U+E012E U+E0127 U+E0148 U+E01EF | always |
| `nNGH` | `󰄎󰄎󰄣󠅎󠄮󠄧󠄨󠇯` | U+F010E U+F010E U+F0123 U+E014E U+E012E U+E0127 U+E0128 U+E01EF | always |
| `Nngh` | `󰄎󰄎󰄣󠄮󠅎󠅇󠅈󠇯` | U+F010E U+F010E U+F0123 U+E012E U+E014E U+E0147 U+E0148 U+E01EF | always |
| `NngH` | `󰄎󰄎󰄣󠄮󠅎󠅇󠄨󠇯` | U+F010E U+F010E U+F0123 U+E012E U+E014E U+E0147 U+E0128 U+E01EF | always |
| `NnGh` | `󰄎󰄎󰄣󠄮󠅎󠄧󠅈󠇯` | U+F010E U+F010E U+F0123 U+E012E U+E014E U+E0127 U+E0148 U+E01EF | always |
| `NnGH` | `󰄎󰄎󰄣󠄮󠅎󠄧󠄨󠇯` | U+F010E U+F010E U+F0123 U+E012E U+E014E U+E0127 U+E0128 U+E01EF | always |
| `NNgh` | `󰄎󰄎󰄣󠄮󠄮󠅇󠅈󠇯` | U+F010E U+F010E U+F0123 U+E012E U+E012E U+E0147 U+E0148 U+E01EF | always |
| `NNgH` | `󰄎󰄎󰄣󠄮󠄮󠅇󠄨󠇯` | U+F010E U+F010E U+F0123 U+E012E U+E012E U+E0147 U+E0128 U+E01EF | always |
| `NNGh` | `󰄎󰄎󰄣󠄮󠄮󠄧󠅈󠇯` | U+F010E U+F010E U+F0123 U+E012E U+E012E U+E0127 U+E0148 U+E01EF | always |
| `NNGH` | `󰄎󰄎󰄣󠄮󠄮󠄧󠄨󠇯` | U+F010E U+F010E U+F0123 U+E012E U+E012E U+E0127 U+E0128 U+E01EF | always |
| `y` | `󰄊󠅙󠇯` | U+F010A U+E0159 U+E01EF | before a vowel |
| `y` | `󰄂󠅙󠇯` | U+F0102 U+E0159 U+E01EF | always |
| `Y` | `󰄊󠄹󠇯` | U+F010A U+E0139 U+E01EF | before a vowel |
| `Y` | `󰄂󠄹󠇯` | U+F0102 U+E0139 U+E01EF | always |
| `.` | `󰅀` | U+F0140 | always |
| `-` | `󠄍` | U+E010D | always |
| `0` | `󰄰` | U+F0130 | always |
| `1` | `󰄱` | U+F0131 | always |
| `2` | `󰄲` | U+F0132 | always |
| `3` | `󰄳` | U+F0133 | always |
| `4` | `󰄴` | U+F0134 | always |
| `5` | `󰄵` | U+F0135 | always |
| `6` | `󰄶` | U+F0136 | always |
| `7` | `󰄷` | U+F0137 | always |
| `8` | `󰄸` | U+F0138 | always |
| `9` | `󰄹` | U+F0139 | always |

## Round trip

Every encoding round-trips exactly: decoding the code points that encoding wrote gives back the roman text, and encoding that gives the same code points. The Code points column shows every character a row writes, including any that is invisible.

This page is written from `encodings/thuravark.json` by `tools/encoding_docs.py`.
