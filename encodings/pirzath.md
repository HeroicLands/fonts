# pirzath encoding

Pirzath is a script of letters read left to right, drawn carved in Pirzath Carved and in a hand in Pirzath Hand on the same code points. This encoding writes a roman spelling in them: a digraph such as `th` or `kh` is a single letter, and `ay` before a consonant or at the end of a word is the single letter for the diphthong.

## Fonts

- Pirzath Carved (`pirzath-carved`), written left to right.
- Pirzath Hand (`pirzath-hand`), written left to right.

## Running it

`encode.py` needs only Python 3.9 or later. From a checkout, or from `node_modules/@heroiclands/fonts`:

```sh
python3 encode.py --encoding pirzath "kitha"
python3 encode.py --encoding pirzath --decode "󰀍󰀂󰀠󰀀"
```

The first command writes `󰀍󰀂󰀠󰀀`, and the second reads it back as `kitha`. `--codepoints` prints the result as `U+XXXX` values, and the text may come from standard input.

From Python:

```python
import encode

text = encode.encode("pirzath", "kitha")
roman = encode.decode("pirzath", text)
```

## Vowels and conditions

The vowels are `AEIOUaeiouÁÉËÍÓÚáéëíóú`.

A row marked _before a vowel_ applies when the next character is a vowel.

A row marked _before a consonant_ applies when the next character is a letter that is not a vowel.

A row marked _at the end of a word_ applies at the last character of the text or before whitespace, punctuation or a symbol.

Where several rows begin with the same roman, the longest wins, and among rows of one length a row whose condition holds comes before a row with none. A row whose condition fails is skipped.

## Rows

The rows are in the order the file states them.

| Roman | Character | Code points | When |
| --- | --- | --- | --- |
| `a` | `󰀀` | U+F0000 | always |
| `A` | `󰀀󠄡󠇯` | U+F0000 U+E0121 U+E01EF | always |
| `e` | `󰀁` | U+F0001 | always |
| `ë` | `󰀁󠅛󠅅󠅂󠅝󠇯` | U+F0001 U+E015B U+E0145 U+E0142 U+E015D U+E01EF | always |
| `E` | `󰀁󠄥󠇯` | U+F0001 U+E0125 U+E01EF | always |
| `Ë` | `󰀁󠅛󠅃󠅂󠅝󠇯` | U+F0001 U+E015B U+E0143 U+E0142 U+E015D U+E01EF | always |
| `i` | `󰀂` | U+F0002 | always |
| `I` | `󰀂󠄩󠇯` | U+F0002 U+E0129 U+E01EF | always |
| `o` | `󰀃` | U+F0003 | always |
| `O` | `󰀃󠄯󠇯` | U+F0003 U+E012F U+E01EF | always |
| `u` | `󰀄` | U+F0004 | always |
| `U` | `󰀄󠄵󠇯` | U+F0004 U+E0135 U+E01EF | always |
| `p` | `󰀅` | U+F0005 | always |
| `P` | `󰀅󠄰󠇯` | U+F0005 U+E0130 U+E01EF | always |
| `b` | `󰀆` | U+F0006 | always |
| `B` | `󰀆󠄢󠇯` | U+F0006 U+E0122 U+E01EF | always |
| `f` | `󰀇` | U+F0007 | always |
| `F` | `󰀇󠄦󠇯` | U+F0007 U+E0126 U+E01EF | always |
| `v` | `󰀈` | U+F0008 | always |
| `V` | `󰀈󠄶󠇯` | U+F0008 U+E0136 U+E01EF | always |
| `m` | `󰀉` | U+F0009 | always |
| `M` | `󰀉󠄭󠇯` | U+F0009 U+E012D U+E01EF | always |
| `t` | `󰀊` | U+F000A | always |
| `T` | `󰀊󠄴󠇯` | U+F000A U+E0134 U+E01EF | always |
| `d` | `󰀋` | U+F000B | always |
| `D` | `󰀋󠄤󠇯` | U+F000B U+E0124 U+E01EF | always |
| `n` | `󰀌` | U+F000C | always |
| `N` | `󰀌󠄮󠇯` | U+F000C U+E012E U+E01EF | always |
| `k` | `󰀍` | U+F000D | always |
| `K` | `󰀍󠄫󠇯` | U+F000D U+E012B U+E01EF | always |
| `g` | `󰀎` | U+F000E | always |
| `G` | `󰀎󠄧󠇯` | U+F000E U+E0127 U+E01EF | always |
| `s` | `󰀏` | U+F000F | always |
| `S` | `󰀏󠄳󠇯` | U+F000F U+E0133 U+E01EF | always |
| `z` | `󰀐` | U+F0010 | always |
| `Z` | `󰀐󠄺󠇯` | U+F0010 U+E013A U+E01EF | always |
| `h` | `󰀑` | U+F0011 | always |
| `H` | `󰀑󠄨󠇯` | U+F0011 U+E0128 U+E01EF | always |
| `l` | `󰀒` | U+F0012 | always |
| `L` | `󰀒󠄬󠇯` | U+F0012 U+E012C U+E01EF | always |
| `r` | `󰀓` | U+F0013 | always |
| `R` | `󰀓󠄲󠇯` | U+F0013 U+E0132 U+E01EF | always |
| `j` | `󰀔` | U+F0014 | always |
| `J` | `󰀔󠄪󠇯` | U+F0014 U+E012A U+E01EF | always |
| `q` | `󰀕` | U+F0015 | always |
| `Q` | `󰀕󠄱󠇯` | U+F0015 U+E0131 U+E01EF | always |
| `w` | `󰀖` | U+F0016 | always |
| `W` | `󰀖󠄷󠇯` | U+F0016 U+E0137 U+E01EF | always |
| `á` | `󰀀󰁠` | U+F0000 U+F0060 | always |
| `Á` | `󰀀󰁠󠅛󠅃󠄑󠅝󠇯` | U+F0000 U+F0060 U+E015B U+E0143 U+E0111 U+E015D U+E01EF | always |
| `é` | `󰀁󰁠` | U+F0001 U+F0060 | always |
| `É` | `󰀁󰁠󠅛󠅃󠄙󠅝󠇯` | U+F0001 U+F0060 U+E015B U+E0143 U+E0119 U+E015D U+E01EF | always |
| `í` | `󰀂󰁠` | U+F0002 U+F0060 | always |
| `Í` | `󰀂󰁠󠅛󠅃󠅄󠅝󠇯` | U+F0002 U+F0060 U+E015B U+E0143 U+E0144 U+E015D U+E01EF | always |
| `ó` | `󰀃󰁠` | U+F0003 U+F0060 | always |
| `Ó` | `󰀃󰁠󠅛󠅄󠄓󠅝󠇯` | U+F0003 U+F0060 U+E015B U+E0144 U+E0113 U+E015D U+E01EF | always |
| `ú` | `󰀄󰁠` | U+F0004 U+F0060 | always |
| `Ú` | `󰀄󰁠󠅛󠅄󠅁󠅝󠇯` | U+F0004 U+F0060 U+E015B U+E0144 U+E0141 U+E015D U+E01EF | always |
| `'` | `󰀘` | U+F0018 | always |
| `’` | `󰀘󠅛󠄒󠄐󠄑󠄙󠅝󠇯` | U+F0018 U+E015B U+E0112 U+E0110 U+E0111 U+E0119 U+E015D U+E01EF | always |
| `th` | `󰀠` | U+F0020 | always |
| `tH` | `󰀠󠅔󠄨󠇯` | U+F0020 U+E0154 U+E0128 U+E01EF | always |
| `Th` | `󰀠󠄴󠅈󠇯` | U+F0020 U+E0134 U+E0148 U+E01EF | always |
| `TH` | `󰀠󠄴󠄨󠇯` | U+F0020 U+E0134 U+E0128 U+E01EF | always |
| `dh` | `󰀡` | U+F0021 | always |
| `dH` | `󰀡󠅄󠄨󠇯` | U+F0021 U+E0144 U+E0128 U+E01EF | always |
| `Dh` | `󰀡󠄤󠅈󠇯` | U+F0021 U+E0124 U+E0148 U+E01EF | always |
| `DH` | `󰀡󠄤󠄨󠇯` | U+F0021 U+E0124 U+E0128 U+E01EF | always |
| `kh` | `󰀢` | U+F0022 | always |
| `kH` | `󰀢󠅋󠄨󠇯` | U+F0022 U+E014B U+E0128 U+E01EF | always |
| `Kh` | `󰀢󠄫󠅈󠇯` | U+F0022 U+E012B U+E0148 U+E01EF | always |
| `KH` | `󰀢󠄫󠄨󠇯` | U+F0022 U+E012B U+E0128 U+E01EF | always |
| `gh` | `󰀣` | U+F0023 | always |
| `gH` | `󰀣󠅇󠄨󠇯` | U+F0023 U+E0147 U+E0128 U+E01EF | always |
| `Gh` | `󰀣󠄧󠅈󠇯` | U+F0023 U+E0127 U+E0148 U+E01EF | always |
| `GH` | `󰀣󠄧󠄨󠇯` | U+F0023 U+E0127 U+E0128 U+E01EF | always |
| `sh` | `󰀤` | U+F0024 | always |
| `sH` | `󰀤󠅓󠄨󠇯` | U+F0024 U+E0153 U+E0128 U+E01EF | always |
| `Sh` | `󰀤󠄳󠅈󠇯` | U+F0024 U+E0133 U+E0148 U+E01EF | always |
| `SH` | `󰀤󠄳󠄨󠇯` | U+F0024 U+E0133 U+E0128 U+E01EF | always |
| `zh` | `󰀥` | U+F0025 | always |
| `zH` | `󰀥󠅚󠄨󠇯` | U+F0025 U+E015A U+E0128 U+E01EF | always |
| `Zh` | `󰀥󠄺󠅈󠇯` | U+F0025 U+E013A U+E0148 U+E01EF | always |
| `ZH` | `󰀥󠄺󠄨󠇯` | U+F0025 U+E013A U+E0128 U+E01EF | always |
| `ch` | `󰀧` | U+F0027 | always |
| `cH` | `󰀧󠅃󠄨󠇯` | U+F0027 U+E0143 U+E0128 U+E01EF | always |
| `Ch` | `󰀧󠄣󠅈󠇯` | U+F0027 U+E0123 U+E0148 U+E01EF | always |
| `CH` | `󰀧󠄣󠄨󠇯` | U+F0027 U+E0123 U+E0128 U+E01EF | always |
| `ts` | `󰀦` | U+F0026 | always |
| `tS` | `󰀦󠅔󠄳󠇯` | U+F0026 U+E0154 U+E0133 U+E01EF | always |
| `Ts` | `󰀦󠄴󠅓󠇯` | U+F0026 U+E0134 U+E0153 U+E01EF | always |
| `TS` | `󰀦󠄴󠄳󠇯` | U+F0026 U+E0134 U+E0133 U+E01EF | always |
| `ng` | `󰀨` | U+F0028 | always |
| `nG` | `󰀨󠅎󠄧󠇯` | U+F0028 U+E014E U+E0127 U+E01EF | always |
| `Ng` | `󰀨󠄮󠅇󠇯` | U+F0028 U+E012E U+E0147 U+E01EF | always |
| `NG` | `󰀨󠄮󠄧󠇯` | U+F0028 U+E012E U+E0127 U+E01EF | always |
| `ny` | `󰀩` | U+F0029 | always |
| `nY` | `󰀩󠅎󠄹󠇯` | U+F0029 U+E014E U+E0139 U+E01EF | always |
| `Ny` | `󰀩󠄮󠅙󠇯` | U+F0029 U+E012E U+E0159 U+E01EF | always |
| `NY` | `󰀩󠄮󠄹󠇯` | U+F0029 U+E012E U+E0139 U+E01EF | always |
| `hl` | `󰀪` | U+F002A | always |
| `hL` | `󰀪󠅈󠄬󠇯` | U+F002A U+E0148 U+E012C U+E01EF | always |
| `Hl` | `󰀪󠄨󠅌󠇯` | U+F002A U+E0128 U+E014C U+E01EF | always |
| `HL` | `󰀪󠄨󠄬󠇯` | U+F002A U+E0128 U+E012C U+E01EF | always |
| `ngh` | `󰀌󰀣󠅎󠅇󠅈󠇯` | U+F000C U+F0023 U+E014E U+E0147 U+E0148 U+E01EF | always |
| `ngH` | `󰀌󰀣󠅎󠅇󠄨󠇯` | U+F000C U+F0023 U+E014E U+E0147 U+E0128 U+E01EF | always |
| `nGh` | `󰀌󰀣󠅎󠄧󠅈󠇯` | U+F000C U+F0023 U+E014E U+E0127 U+E0148 U+E01EF | always |
| `nGH` | `󰀌󰀣󠅎󠄧󠄨󠇯` | U+F000C U+F0023 U+E014E U+E0127 U+E0128 U+E01EF | always |
| `Ngh` | `󰀌󰀣󠄮󠅇󠅈󠇯` | U+F000C U+F0023 U+E012E U+E0147 U+E0148 U+E01EF | always |
| `NgH` | `󰀌󰀣󠄮󠅇󠄨󠇯` | U+F000C U+F0023 U+E012E U+E0147 U+E0128 U+E01EF | always |
| `NGh` | `󰀌󰀣󠄮󠄧󠅈󠇯` | U+F000C U+F0023 U+E012E U+E0127 U+E0148 U+E01EF | always |
| `NGH` | `󰀌󰀣󠄮󠄧󠄨󠇯` | U+F000C U+F0023 U+E012E U+E0127 U+E0128 U+E01EF | always |
| `tth` | `󰀠󰀠󠅔󠅔󠅈󠇯` | U+F0020 U+F0020 U+E0154 U+E0154 U+E0148 U+E01EF | always |
| `ttH` | `󰀠󰀠󠅔󠅔󠄨󠇯` | U+F0020 U+F0020 U+E0154 U+E0154 U+E0128 U+E01EF | always |
| `tTh` | `󰀠󰀠󠅔󠄴󠅈󠇯` | U+F0020 U+F0020 U+E0154 U+E0134 U+E0148 U+E01EF | always |
| `tTH` | `󰀠󰀠󠅔󠄴󠄨󠇯` | U+F0020 U+F0020 U+E0154 U+E0134 U+E0128 U+E01EF | always |
| `Tth` | `󰀠󰀠󠄴󠅔󠅈󠇯` | U+F0020 U+F0020 U+E0134 U+E0154 U+E0148 U+E01EF | always |
| `TtH` | `󰀠󰀠󠄴󠅔󠄨󠇯` | U+F0020 U+F0020 U+E0134 U+E0154 U+E0128 U+E01EF | always |
| `TTh` | `󰀠󰀠󠄴󠄴󠅈󠇯` | U+F0020 U+F0020 U+E0134 U+E0134 U+E0148 U+E01EF | always |
| `TTH` | `󰀠󰀠󠄴󠄴󠄨󠇯` | U+F0020 U+F0020 U+E0134 U+E0134 U+E0128 U+E01EF | always |
| `ddh` | `󰀡󰀡󠅄󠅄󠅈󠇯` | U+F0021 U+F0021 U+E0144 U+E0144 U+E0148 U+E01EF | always |
| `ddH` | `󰀡󰀡󠅄󠅄󠄨󠇯` | U+F0021 U+F0021 U+E0144 U+E0144 U+E0128 U+E01EF | always |
| `dDh` | `󰀡󰀡󠅄󠄤󠅈󠇯` | U+F0021 U+F0021 U+E0144 U+E0124 U+E0148 U+E01EF | always |
| `dDH` | `󰀡󰀡󠅄󠄤󠄨󠇯` | U+F0021 U+F0021 U+E0144 U+E0124 U+E0128 U+E01EF | always |
| `Ddh` | `󰀡󰀡󠄤󠅄󠅈󠇯` | U+F0021 U+F0021 U+E0124 U+E0144 U+E0148 U+E01EF | always |
| `DdH` | `󰀡󰀡󠄤󠅄󠄨󠇯` | U+F0021 U+F0021 U+E0124 U+E0144 U+E0128 U+E01EF | always |
| `DDh` | `󰀡󰀡󠄤󠄤󠅈󠇯` | U+F0021 U+F0021 U+E0124 U+E0124 U+E0148 U+E01EF | always |
| `DDH` | `󰀡󰀡󠄤󠄤󠄨󠇯` | U+F0021 U+F0021 U+E0124 U+E0124 U+E0128 U+E01EF | always |
| `kkh` | `󰀢󰀢󠅋󠅋󠅈󠇯` | U+F0022 U+F0022 U+E014B U+E014B U+E0148 U+E01EF | always |
| `kkH` | `󰀢󰀢󠅋󠅋󠄨󠇯` | U+F0022 U+F0022 U+E014B U+E014B U+E0128 U+E01EF | always |
| `kKh` | `󰀢󰀢󠅋󠄫󠅈󠇯` | U+F0022 U+F0022 U+E014B U+E012B U+E0148 U+E01EF | always |
| `kKH` | `󰀢󰀢󠅋󠄫󠄨󠇯` | U+F0022 U+F0022 U+E014B U+E012B U+E0128 U+E01EF | always |
| `Kkh` | `󰀢󰀢󠄫󠅋󠅈󠇯` | U+F0022 U+F0022 U+E012B U+E014B U+E0148 U+E01EF | always |
| `KkH` | `󰀢󰀢󠄫󠅋󠄨󠇯` | U+F0022 U+F0022 U+E012B U+E014B U+E0128 U+E01EF | always |
| `KKh` | `󰀢󰀢󠄫󠄫󠅈󠇯` | U+F0022 U+F0022 U+E012B U+E012B U+E0148 U+E01EF | always |
| `KKH` | `󰀢󰀢󠄫󠄫󠄨󠇯` | U+F0022 U+F0022 U+E012B U+E012B U+E0128 U+E01EF | always |
| `ggh` | `󰀣󰀣󠅇󠅇󠅈󠇯` | U+F0023 U+F0023 U+E0147 U+E0147 U+E0148 U+E01EF | always |
| `ggH` | `󰀣󰀣󠅇󠅇󠄨󠇯` | U+F0023 U+F0023 U+E0147 U+E0147 U+E0128 U+E01EF | always |
| `gGh` | `󰀣󰀣󠅇󠄧󠅈󠇯` | U+F0023 U+F0023 U+E0147 U+E0127 U+E0148 U+E01EF | always |
| `gGH` | `󰀣󰀣󠅇󠄧󠄨󠇯` | U+F0023 U+F0023 U+E0147 U+E0127 U+E0128 U+E01EF | always |
| `Ggh` | `󰀣󰀣󠄧󠅇󠅈󠇯` | U+F0023 U+F0023 U+E0127 U+E0147 U+E0148 U+E01EF | always |
| `GgH` | `󰀣󰀣󠄧󠅇󠄨󠇯` | U+F0023 U+F0023 U+E0127 U+E0147 U+E0128 U+E01EF | always |
| `GGh` | `󰀣󰀣󠄧󠄧󠅈󠇯` | U+F0023 U+F0023 U+E0127 U+E0127 U+E0148 U+E01EF | always |
| `GGH` | `󰀣󰀣󠄧󠄧󠄨󠇯` | U+F0023 U+F0023 U+E0127 U+E0127 U+E0128 U+E01EF | always |
| `ssh` | `󰀤󰀤󠅓󠅓󠅈󠇯` | U+F0024 U+F0024 U+E0153 U+E0153 U+E0148 U+E01EF | always |
| `ssH` | `󰀤󰀤󠅓󠅓󠄨󠇯` | U+F0024 U+F0024 U+E0153 U+E0153 U+E0128 U+E01EF | always |
| `sSh` | `󰀤󰀤󠅓󠄳󠅈󠇯` | U+F0024 U+F0024 U+E0153 U+E0133 U+E0148 U+E01EF | always |
| `sSH` | `󰀤󰀤󠅓󠄳󠄨󠇯` | U+F0024 U+F0024 U+E0153 U+E0133 U+E0128 U+E01EF | always |
| `Ssh` | `󰀤󰀤󠄳󠅓󠅈󠇯` | U+F0024 U+F0024 U+E0133 U+E0153 U+E0148 U+E01EF | always |
| `SsH` | `󰀤󰀤󠄳󠅓󠄨󠇯` | U+F0024 U+F0024 U+E0133 U+E0153 U+E0128 U+E01EF | always |
| `SSh` | `󰀤󰀤󠄳󠄳󠅈󠇯` | U+F0024 U+F0024 U+E0133 U+E0133 U+E0148 U+E01EF | always |
| `SSH` | `󰀤󰀤󠄳󠄳󠄨󠇯` | U+F0024 U+F0024 U+E0133 U+E0133 U+E0128 U+E01EF | always |
| `zzh` | `󰀥󰀥󠅚󠅚󠅈󠇯` | U+F0025 U+F0025 U+E015A U+E015A U+E0148 U+E01EF | always |
| `zzH` | `󰀥󰀥󠅚󠅚󠄨󠇯` | U+F0025 U+F0025 U+E015A U+E015A U+E0128 U+E01EF | always |
| `zZh` | `󰀥󰀥󠅚󠄺󠅈󠇯` | U+F0025 U+F0025 U+E015A U+E013A U+E0148 U+E01EF | always |
| `zZH` | `󰀥󰀥󠅚󠄺󠄨󠇯` | U+F0025 U+F0025 U+E015A U+E013A U+E0128 U+E01EF | always |
| `Zzh` | `󰀥󰀥󠄺󠅚󠅈󠇯` | U+F0025 U+F0025 U+E013A U+E015A U+E0148 U+E01EF | always |
| `ZzH` | `󰀥󰀥󠄺󠅚󠄨󠇯` | U+F0025 U+F0025 U+E013A U+E015A U+E0128 U+E01EF | always |
| `ZZh` | `󰀥󰀥󠄺󠄺󠅈󠇯` | U+F0025 U+F0025 U+E013A U+E013A U+E0148 U+E01EF | always |
| `ZZH` | `󰀥󰀥󠄺󠄺󠄨󠇯` | U+F0025 U+F0025 U+E013A U+E013A U+E0128 U+E01EF | always |
| `cch` | `󰀧󰀧󠅃󠅃󠅈󠇯` | U+F0027 U+F0027 U+E0143 U+E0143 U+E0148 U+E01EF | always |
| `ccH` | `󰀧󰀧󠅃󠅃󠄨󠇯` | U+F0027 U+F0027 U+E0143 U+E0143 U+E0128 U+E01EF | always |
| `cCh` | `󰀧󰀧󠅃󠄣󠅈󠇯` | U+F0027 U+F0027 U+E0143 U+E0123 U+E0148 U+E01EF | always |
| `cCH` | `󰀧󰀧󠅃󠄣󠄨󠇯` | U+F0027 U+F0027 U+E0143 U+E0123 U+E0128 U+E01EF | always |
| `Cch` | `󰀧󰀧󠄣󠅃󠅈󠇯` | U+F0027 U+F0027 U+E0123 U+E0143 U+E0148 U+E01EF | always |
| `CcH` | `󰀧󰀧󠄣󠅃󠄨󠇯` | U+F0027 U+F0027 U+E0123 U+E0143 U+E0128 U+E01EF | always |
| `CCh` | `󰀧󰀧󠄣󠄣󠅈󠇯` | U+F0027 U+F0027 U+E0123 U+E0123 U+E0148 U+E01EF | always |
| `CCH` | `󰀧󰀧󠄣󠄣󠄨󠇯` | U+F0027 U+F0027 U+E0123 U+E0123 U+E0128 U+E01EF | always |
| `tts` | `󰀦󰀦󠅔󠅔󠅓󠇯` | U+F0026 U+F0026 U+E0154 U+E0154 U+E0153 U+E01EF | always |
| `ttS` | `󰀦󰀦󠅔󠅔󠄳󠇯` | U+F0026 U+F0026 U+E0154 U+E0154 U+E0133 U+E01EF | always |
| `tTs` | `󰀦󰀦󠅔󠄴󠅓󠇯` | U+F0026 U+F0026 U+E0154 U+E0134 U+E0153 U+E01EF | always |
| `tTS` | `󰀦󰀦󠅔󠄴󠄳󠇯` | U+F0026 U+F0026 U+E0154 U+E0134 U+E0133 U+E01EF | always |
| `Tts` | `󰀦󰀦󠄴󠅔󠅓󠇯` | U+F0026 U+F0026 U+E0134 U+E0154 U+E0153 U+E01EF | always |
| `TtS` | `󰀦󰀦󠄴󠅔󠄳󠇯` | U+F0026 U+F0026 U+E0134 U+E0154 U+E0133 U+E01EF | always |
| `TTs` | `󰀦󰀦󠄴󠄴󠅓󠇯` | U+F0026 U+F0026 U+E0134 U+E0134 U+E0153 U+E01EF | always |
| `TTS` | `󰀦󰀦󠄴󠄴󠄳󠇯` | U+F0026 U+F0026 U+E0134 U+E0134 U+E0133 U+E01EF | always |
| `nng` | `󰀨󰀨󠅎󠅎󠅇󠇯` | U+F0028 U+F0028 U+E014E U+E014E U+E0147 U+E01EF | always |
| `nnG` | `󰀨󰀨󠅎󠅎󠄧󠇯` | U+F0028 U+F0028 U+E014E U+E014E U+E0127 U+E01EF | always |
| `nNg` | `󰀨󰀨󠅎󠄮󠅇󠇯` | U+F0028 U+F0028 U+E014E U+E012E U+E0147 U+E01EF | always |
| `nNG` | `󰀨󰀨󠅎󠄮󠄧󠇯` | U+F0028 U+F0028 U+E014E U+E012E U+E0127 U+E01EF | always |
| `Nng` | `󰀨󰀨󠄮󠅎󠅇󠇯` | U+F0028 U+F0028 U+E012E U+E014E U+E0147 U+E01EF | always |
| `NnG` | `󰀨󰀨󠄮󠅎󠄧󠇯` | U+F0028 U+F0028 U+E012E U+E014E U+E0127 U+E01EF | always |
| `NNg` | `󰀨󰀨󠄮󠄮󠅇󠇯` | U+F0028 U+F0028 U+E012E U+E012E U+E0147 U+E01EF | always |
| `NNG` | `󰀨󰀨󠄮󠄮󠄧󠇯` | U+F0028 U+F0028 U+E012E U+E012E U+E0127 U+E01EF | always |
| `nny` | `󰀩󰀩󠅎󠅎󠅙󠇯` | U+F0029 U+F0029 U+E014E U+E014E U+E0159 U+E01EF | always |
| `nnY` | `󰀩󰀩󠅎󠅎󠄹󠇯` | U+F0029 U+F0029 U+E014E U+E014E U+E0139 U+E01EF | always |
| `nNy` | `󰀩󰀩󠅎󠄮󠅙󠇯` | U+F0029 U+F0029 U+E014E U+E012E U+E0159 U+E01EF | always |
| `nNY` | `󰀩󰀩󠅎󠄮󠄹󠇯` | U+F0029 U+F0029 U+E014E U+E012E U+E0139 U+E01EF | always |
| `Nny` | `󰀩󰀩󠄮󠅎󠅙󠇯` | U+F0029 U+F0029 U+E012E U+E014E U+E0159 U+E01EF | always |
| `NnY` | `󰀩󰀩󠄮󠅎󠄹󠇯` | U+F0029 U+F0029 U+E012E U+E014E U+E0139 U+E01EF | always |
| `NNy` | `󰀩󰀩󠄮󠄮󠅙󠇯` | U+F0029 U+F0029 U+E012E U+E012E U+E0159 U+E01EF | always |
| `NNY` | `󰀩󰀩󠄮󠄮󠄹󠇯` | U+F0029 U+F0029 U+E012E U+E012E U+E0139 U+E01EF | always |
| `hhl` | `󰀪󰀪󠅈󠅈󠅌󠇯` | U+F002A U+F002A U+E0148 U+E0148 U+E014C U+E01EF | always |
| `hhL` | `󰀪󰀪󠅈󠅈󠄬󠇯` | U+F002A U+F002A U+E0148 U+E0148 U+E012C U+E01EF | always |
| `hHl` | `󰀪󰀪󠅈󠄨󠅌󠇯` | U+F002A U+F002A U+E0148 U+E0128 U+E014C U+E01EF | always |
| `hHL` | `󰀪󰀪󠅈󠄨󠄬󠇯` | U+F002A U+F002A U+E0148 U+E0128 U+E012C U+E01EF | always |
| `Hhl` | `󰀪󰀪󠄨󠅈󠅌󠇯` | U+F002A U+F002A U+E0128 U+E0148 U+E014C U+E01EF | always |
| `HhL` | `󰀪󰀪󠄨󠅈󠄬󠇯` | U+F002A U+F002A U+E0128 U+E0148 U+E012C U+E01EF | always |
| `HHl` | `󰀪󰀪󠄨󠄨󠅌󠇯` | U+F002A U+F002A U+E0128 U+E0128 U+E014C U+E01EF | always |
| `HHL` | `󰀪󰀪󠄨󠄨󠄬󠇯` | U+F002A U+F002A U+E0128 U+E0128 U+E012C U+E01EF | always |
| `nngh` | `󰀌󰀌󰀣󠅎󠅎󠅇󠅈󠇯` | U+F000C U+F000C U+F0023 U+E014E U+E014E U+E0147 U+E0148 U+E01EF | always |
| `nngH` | `󰀌󰀌󰀣󠅎󠅎󠅇󠄨󠇯` | U+F000C U+F000C U+F0023 U+E014E U+E014E U+E0147 U+E0128 U+E01EF | always |
| `nnGh` | `󰀌󰀌󰀣󠅎󠅎󠄧󠅈󠇯` | U+F000C U+F000C U+F0023 U+E014E U+E014E U+E0127 U+E0148 U+E01EF | always |
| `nnGH` | `󰀌󰀌󰀣󠅎󠅎󠄧󠄨󠇯` | U+F000C U+F000C U+F0023 U+E014E U+E014E U+E0127 U+E0128 U+E01EF | always |
| `nNgh` | `󰀌󰀌󰀣󠅎󠄮󠅇󠅈󠇯` | U+F000C U+F000C U+F0023 U+E014E U+E012E U+E0147 U+E0148 U+E01EF | always |
| `nNgH` | `󰀌󰀌󰀣󠅎󠄮󠅇󠄨󠇯` | U+F000C U+F000C U+F0023 U+E014E U+E012E U+E0147 U+E0128 U+E01EF | always |
| `nNGh` | `󰀌󰀌󰀣󠅎󠄮󠄧󠅈󠇯` | U+F000C U+F000C U+F0023 U+E014E U+E012E U+E0127 U+E0148 U+E01EF | always |
| `nNGH` | `󰀌󰀌󰀣󠅎󠄮󠄧󠄨󠇯` | U+F000C U+F000C U+F0023 U+E014E U+E012E U+E0127 U+E0128 U+E01EF | always |
| `Nngh` | `󰀌󰀌󰀣󠄮󠅎󠅇󠅈󠇯` | U+F000C U+F000C U+F0023 U+E012E U+E014E U+E0147 U+E0148 U+E01EF | always |
| `NngH` | `󰀌󰀌󰀣󠄮󠅎󠅇󠄨󠇯` | U+F000C U+F000C U+F0023 U+E012E U+E014E U+E0147 U+E0128 U+E01EF | always |
| `NnGh` | `󰀌󰀌󰀣󠄮󠅎󠄧󠅈󠇯` | U+F000C U+F000C U+F0023 U+E012E U+E014E U+E0127 U+E0148 U+E01EF | always |
| `NnGH` | `󰀌󰀌󰀣󠄮󠅎󠄧󠄨󠇯` | U+F000C U+F000C U+F0023 U+E012E U+E014E U+E0127 U+E0128 U+E01EF | always |
| `NNgh` | `󰀌󰀌󰀣󠄮󠄮󠅇󠅈󠇯` | U+F000C U+F000C U+F0023 U+E012E U+E012E U+E0147 U+E0148 U+E01EF | always |
| `NNgH` | `󰀌󰀌󰀣󠄮󠄮󠅇󠄨󠇯` | U+F000C U+F000C U+F0023 U+E012E U+E012E U+E0147 U+E0128 U+E01EF | always |
| `NNGh` | `󰀌󰀌󰀣󠄮󠄮󠄧󠅈󠇯` | U+F000C U+F000C U+F0023 U+E012E U+E012E U+E0127 U+E0148 U+E01EF | always |
| `NNGH` | `󰀌󰀌󰀣󠄮󠄮󠄧󠄨󠇯` | U+F000C U+F000C U+F0023 U+E012E U+E012E U+E0127 U+E0128 U+E01EF | always |
| `ai` | `󰀰` | U+F0030 | always |
| `aI` | `󰀰󠅁󠄩󠇯` | U+F0030 U+E0141 U+E0129 U+E01EF | always |
| `Ai` | `󰀰󠄡󠅉󠇯` | U+F0030 U+E0121 U+E0149 U+E01EF | always |
| `AI` | `󰀰󠄡󠄩󠇯` | U+F0030 U+E0121 U+E0129 U+E01EF | always |
| `aí` | `󰀰󰁠` | U+F0030 U+F0060 | always |
| `aÍ` | `󰀰󰁠󠅁󠅛󠅃󠅄󠅝󠇯` | U+F0030 U+F0060 U+E0141 U+E015B U+E0143 U+E0144 U+E015D U+E01EF | always |
| `Aí` | `󰀰󰁠󠄡󠅛󠅅󠅄󠅝󠇯` | U+F0030 U+F0060 U+E0121 U+E015B U+E0145 U+E0144 U+E015D U+E01EF | always |
| `AÍ` | `󰀰󰁠󠄡󠅛󠅃󠅄󠅝󠇯` | U+F0030 U+F0060 U+E0121 U+E015B U+E0143 U+E0144 U+E015D U+E01EF | always |
| `ái` | `󰀰󰁠󠅛󠅅󠄑󠅝󠅉󠇯` | U+F0030 U+F0060 U+E015B U+E0145 U+E0111 U+E015D U+E0149 U+E01EF | always |
| `áI` | `󰀰󰁠󠅛󠅅󠄑󠅝󠄩󠇯` | U+F0030 U+F0060 U+E015B U+E0145 U+E0111 U+E015D U+E0129 U+E01EF | always |
| `Ái` | `󰀰󰁠󠅛󠅃󠄑󠅝󠅉󠇯` | U+F0030 U+F0060 U+E015B U+E0143 U+E0111 U+E015D U+E0149 U+E01EF | always |
| `ÁI` | `󰀰󰁠󠅛󠅃󠄑󠅝󠄩󠇯` | U+F0030 U+F0060 U+E015B U+E0143 U+E0111 U+E015D U+E0129 U+E01EF | always |
| `áí` | `󰀰󰁠󰁠` | U+F0030 U+F0060 U+F0060 | always |
| `áÍ` | `󰀰󰁠󰁠󠅛󠅅󠄑󠅝󠅛󠅃󠅄󠅝󠇯` | U+F0030 U+F0060 U+F0060 U+E015B U+E0145 U+E0111 U+E015D U+E015B U+E0143 U+E0144 U+E015D U+E01EF | always |
| `Áí` | `󰀰󰁠󰁠󠅛󠅃󠄑󠅝󠅛󠅅󠅄󠅝󠇯` | U+F0030 U+F0060 U+F0060 U+E015B U+E0143 U+E0111 U+E015D U+E015B U+E0145 U+E0144 U+E015D U+E01EF | always |
| `ÁÍ` | `󰀰󰁠󰁠󠅛󠅃󠄑󠅝󠅛󠅃󠅄󠅝󠇯` | U+F0030 U+F0060 U+F0060 U+E015B U+E0143 U+E0111 U+E015D U+E015B U+E0143 U+E0144 U+E015D U+E01EF | always |
| `au` | `󰀱` | U+F0031 | always |
| `aU` | `󰀱󠅁󠄵󠇯` | U+F0031 U+E0141 U+E0135 U+E01EF | always |
| `Au` | `󰀱󠄡󠅕󠇯` | U+F0031 U+E0121 U+E0155 U+E01EF | always |
| `AU` | `󰀱󠄡󠄵󠇯` | U+F0031 U+E0121 U+E0135 U+E01EF | always |
| `aú` | `󰀱󰁠` | U+F0031 U+F0060 | always |
| `aÚ` | `󰀱󰁠󠅁󠅛󠅄󠅁󠅝󠇯` | U+F0031 U+F0060 U+E0141 U+E015B U+E0144 U+E0141 U+E015D U+E01EF | always |
| `Aú` | `󰀱󰁠󠄡󠅛󠅆󠅁󠅝󠇯` | U+F0031 U+F0060 U+E0121 U+E015B U+E0146 U+E0141 U+E015D U+E01EF | always |
| `AÚ` | `󰀱󰁠󠄡󠅛󠅄󠅁󠅝󠇯` | U+F0031 U+F0060 U+E0121 U+E015B U+E0144 U+E0141 U+E015D U+E01EF | always |
| `áu` | `󰀱󰁠󠅛󠅅󠄑󠅝󠅕󠇯` | U+F0031 U+F0060 U+E015B U+E0145 U+E0111 U+E015D U+E0155 U+E01EF | always |
| `áU` | `󰀱󰁠󠅛󠅅󠄑󠅝󠄵󠇯` | U+F0031 U+F0060 U+E015B U+E0145 U+E0111 U+E015D U+E0135 U+E01EF | always |
| `Áu` | `󰀱󰁠󠅛󠅃󠄑󠅝󠅕󠇯` | U+F0031 U+F0060 U+E015B U+E0143 U+E0111 U+E015D U+E0155 U+E01EF | always |
| `ÁU` | `󰀱󰁠󠅛󠅃󠄑󠅝󠄵󠇯` | U+F0031 U+F0060 U+E015B U+E0143 U+E0111 U+E015D U+E0135 U+E01EF | always |
| `áú` | `󰀱󰁠󰁠` | U+F0031 U+F0060 U+F0060 | always |
| `áÚ` | `󰀱󰁠󰁠󠅛󠅅󠄑󠅝󠅛󠅄󠅁󠅝󠇯` | U+F0031 U+F0060 U+F0060 U+E015B U+E0145 U+E0111 U+E015D U+E015B U+E0144 U+E0141 U+E015D U+E01EF | always |
| `Áú` | `󰀱󰁠󰁠󠅛󠅃󠄑󠅝󠅛󠅆󠅁󠅝󠇯` | U+F0031 U+F0060 U+F0060 U+E015B U+E0143 U+E0111 U+E015D U+E015B U+E0146 U+E0141 U+E015D U+E01EF | always |
| `ÁÚ` | `󰀱󰁠󰁠󠅛󠅃󠄑󠅝󠅛󠅄󠅁󠅝󠇯` | U+F0031 U+F0060 U+F0060 U+E015B U+E0143 U+E0111 U+E015D U+E015B U+E0144 U+E0141 U+E015D U+E01EF | always |
| `ei` | `󰀲` | U+F0032 | always |
| `ëi` | `󰀲󠅛󠅅󠅂󠅝󠅉󠇯` | U+F0032 U+E015B U+E0145 U+E0142 U+E015D U+E0149 U+E01EF | always |
| `eI` | `󰀲󠅅󠄩󠇯` | U+F0032 U+E0145 U+E0129 U+E01EF | always |
| `ëI` | `󰀲󠅛󠅅󠅂󠅝󠄩󠇯` | U+F0032 U+E015B U+E0145 U+E0142 U+E015D U+E0129 U+E01EF | always |
| `Ei` | `󰀲󠄥󠅉󠇯` | U+F0032 U+E0125 U+E0149 U+E01EF | always |
| `Ëi` | `󰀲󠅛󠅃󠅂󠅝󠅉󠇯` | U+F0032 U+E015B U+E0143 U+E0142 U+E015D U+E0149 U+E01EF | always |
| `EI` | `󰀲󠄥󠄩󠇯` | U+F0032 U+E0125 U+E0129 U+E01EF | always |
| `ËI` | `󰀲󠅛󠅃󠅂󠅝󠄩󠇯` | U+F0032 U+E015B U+E0143 U+E0142 U+E015D U+E0129 U+E01EF | always |
| `eí` | `󰀲󰁠` | U+F0032 U+F0060 | always |
| `ëí` | `󰀲󰁠󠅛󠅅󠅂󠅝󠅛󠅅󠅄󠅝󠇯` | U+F0032 U+F0060 U+E015B U+E0145 U+E0142 U+E015D U+E015B U+E0145 U+E0144 U+E015D U+E01EF | always |
| `eÍ` | `󰀲󰁠󠅅󠅛󠅃󠅄󠅝󠇯` | U+F0032 U+F0060 U+E0145 U+E015B U+E0143 U+E0144 U+E015D U+E01EF | always |
| `ëÍ` | `󰀲󰁠󠅛󠅅󠅂󠅝󠅛󠅃󠅄󠅝󠇯` | U+F0032 U+F0060 U+E015B U+E0145 U+E0142 U+E015D U+E015B U+E0143 U+E0144 U+E015D U+E01EF | always |
| `Eí` | `󰀲󰁠󠄥󠅛󠅅󠅄󠅝󠇯` | U+F0032 U+F0060 U+E0125 U+E015B U+E0145 U+E0144 U+E015D U+E01EF | always |
| `Ëí` | `󰀲󰁠󠅛󠅃󠅂󠅝󠅛󠅅󠅄󠅝󠇯` | U+F0032 U+F0060 U+E015B U+E0143 U+E0142 U+E015D U+E015B U+E0145 U+E0144 U+E015D U+E01EF | always |
| `EÍ` | `󰀲󰁠󠄥󠅛󠅃󠅄󠅝󠇯` | U+F0032 U+F0060 U+E0125 U+E015B U+E0143 U+E0144 U+E015D U+E01EF | always |
| `ËÍ` | `󰀲󰁠󠅛󠅃󠅂󠅝󠅛󠅃󠅄󠅝󠇯` | U+F0032 U+F0060 U+E015B U+E0143 U+E0142 U+E015D U+E015B U+E0143 U+E0144 U+E015D U+E01EF | always |
| `éi` | `󰀲󰁠󠅛󠅅󠄙󠅝󠅉󠇯` | U+F0032 U+F0060 U+E015B U+E0145 U+E0119 U+E015D U+E0149 U+E01EF | always |
| `éI` | `󰀲󰁠󠅛󠅅󠄙󠅝󠄩󠇯` | U+F0032 U+F0060 U+E015B U+E0145 U+E0119 U+E015D U+E0129 U+E01EF | always |
| `Éi` | `󰀲󰁠󠅛󠅃󠄙󠅝󠅉󠇯` | U+F0032 U+F0060 U+E015B U+E0143 U+E0119 U+E015D U+E0149 U+E01EF | always |
| `ÉI` | `󰀲󰁠󠅛󠅃󠄙󠅝󠄩󠇯` | U+F0032 U+F0060 U+E015B U+E0143 U+E0119 U+E015D U+E0129 U+E01EF | always |
| `éí` | `󰀲󰁠󰁠` | U+F0032 U+F0060 U+F0060 | always |
| `éÍ` | `󰀲󰁠󰁠󠅛󠅅󠄙󠅝󠅛󠅃󠅄󠅝󠇯` | U+F0032 U+F0060 U+F0060 U+E015B U+E0145 U+E0119 U+E015D U+E015B U+E0143 U+E0144 U+E015D U+E01EF | always |
| `Éí` | `󰀲󰁠󰁠󠅛󠅃󠄙󠅝󠅛󠅅󠅄󠅝󠇯` | U+F0032 U+F0060 U+F0060 U+E015B U+E0143 U+E0119 U+E015D U+E015B U+E0145 U+E0144 U+E015D U+E01EF | always |
| `ÉÍ` | `󰀲󰁠󰁠󠅛󠅃󠄙󠅝󠅛󠅃󠅄󠅝󠇯` | U+F0032 U+F0060 U+F0060 U+E015B U+E0143 U+E0119 U+E015D U+E015B U+E0143 U+E0144 U+E015D U+E01EF | always |
| `oi` | `󰀳` | U+F0033 | always |
| `oI` | `󰀳󠅏󠄩󠇯` | U+F0033 U+E014F U+E0129 U+E01EF | always |
| `Oi` | `󰀳󠄯󠅉󠇯` | U+F0033 U+E012F U+E0149 U+E01EF | always |
| `OI` | `󰀳󠄯󠄩󠇯` | U+F0033 U+E012F U+E0129 U+E01EF | always |
| `oí` | `󰀳󰁠` | U+F0033 U+F0060 | always |
| `oÍ` | `󰀳󰁠󠅏󠅛󠅃󠅄󠅝󠇯` | U+F0033 U+F0060 U+E014F U+E015B U+E0143 U+E0144 U+E015D U+E01EF | always |
| `Oí` | `󰀳󰁠󠄯󠅛󠅅󠅄󠅝󠇯` | U+F0033 U+F0060 U+E012F U+E015B U+E0145 U+E0144 U+E015D U+E01EF | always |
| `OÍ` | `󰀳󰁠󠄯󠅛󠅃󠅄󠅝󠇯` | U+F0033 U+F0060 U+E012F U+E015B U+E0143 U+E0144 U+E015D U+E01EF | always |
| `ói` | `󰀳󰁠󠅛󠅆󠄓󠅝󠅉󠇯` | U+F0033 U+F0060 U+E015B U+E0146 U+E0113 U+E015D U+E0149 U+E01EF | always |
| `óI` | `󰀳󰁠󠅛󠅆󠄓󠅝󠄩󠇯` | U+F0033 U+F0060 U+E015B U+E0146 U+E0113 U+E015D U+E0129 U+E01EF | always |
| `Ói` | `󰀳󰁠󠅛󠅄󠄓󠅝󠅉󠇯` | U+F0033 U+F0060 U+E015B U+E0144 U+E0113 U+E015D U+E0149 U+E01EF | always |
| `ÓI` | `󰀳󰁠󠅛󠅄󠄓󠅝󠄩󠇯` | U+F0033 U+F0060 U+E015B U+E0144 U+E0113 U+E015D U+E0129 U+E01EF | always |
| `óí` | `󰀳󰁠󰁠` | U+F0033 U+F0060 U+F0060 | always |
| `óÍ` | `󰀳󰁠󰁠󠅛󠅆󠄓󠅝󠅛󠅃󠅄󠅝󠇯` | U+F0033 U+F0060 U+F0060 U+E015B U+E0146 U+E0113 U+E015D U+E015B U+E0143 U+E0144 U+E015D U+E01EF | always |
| `Óí` | `󰀳󰁠󰁠󠅛󠅄󠄓󠅝󠅛󠅅󠅄󠅝󠇯` | U+F0033 U+F0060 U+F0060 U+E015B U+E0144 U+E0113 U+E015D U+E015B U+E0145 U+E0144 U+E015D U+E01EF | always |
| `ÓÍ` | `󰀳󰁠󰁠󠅛󠅄󠄓󠅝󠅛󠅃󠅄󠅝󠇯` | U+F0033 U+F0060 U+F0060 U+E015B U+E0144 U+E0113 U+E015D U+E015B U+E0143 U+E0144 U+E015D U+E01EF | always |
| `ou` | `󰀴` | U+F0034 | always |
| `oU` | `󰀴󠅏󠄵󠇯` | U+F0034 U+E014F U+E0135 U+E01EF | always |
| `Ou` | `󰀴󠄯󠅕󠇯` | U+F0034 U+E012F U+E0155 U+E01EF | always |
| `OU` | `󰀴󠄯󠄵󠇯` | U+F0034 U+E012F U+E0135 U+E01EF | always |
| `oú` | `󰀴󰁠` | U+F0034 U+F0060 | always |
| `oÚ` | `󰀴󰁠󠅏󠅛󠅄󠅁󠅝󠇯` | U+F0034 U+F0060 U+E014F U+E015B U+E0144 U+E0141 U+E015D U+E01EF | always |
| `Oú` | `󰀴󰁠󠄯󠅛󠅆󠅁󠅝󠇯` | U+F0034 U+F0060 U+E012F U+E015B U+E0146 U+E0141 U+E015D U+E01EF | always |
| `OÚ` | `󰀴󰁠󠄯󠅛󠅄󠅁󠅝󠇯` | U+F0034 U+F0060 U+E012F U+E015B U+E0144 U+E0141 U+E015D U+E01EF | always |
| `óu` | `󰀴󰁠󠅛󠅆󠄓󠅝󠅕󠇯` | U+F0034 U+F0060 U+E015B U+E0146 U+E0113 U+E015D U+E0155 U+E01EF | always |
| `óU` | `󰀴󰁠󠅛󠅆󠄓󠅝󠄵󠇯` | U+F0034 U+F0060 U+E015B U+E0146 U+E0113 U+E015D U+E0135 U+E01EF | always |
| `Óu` | `󰀴󰁠󠅛󠅄󠄓󠅝󠅕󠇯` | U+F0034 U+F0060 U+E015B U+E0144 U+E0113 U+E015D U+E0155 U+E01EF | always |
| `ÓU` | `󰀴󰁠󠅛󠅄󠄓󠅝󠄵󠇯` | U+F0034 U+F0060 U+E015B U+E0144 U+E0113 U+E015D U+E0135 U+E01EF | always |
| `óú` | `󰀴󰁠󰁠` | U+F0034 U+F0060 U+F0060 | always |
| `óÚ` | `󰀴󰁠󰁠󠅛󠅆󠄓󠅝󠅛󠅄󠅁󠅝󠇯` | U+F0034 U+F0060 U+F0060 U+E015B U+E0146 U+E0113 U+E015D U+E015B U+E0144 U+E0141 U+E015D U+E01EF | always |
| `Óú` | `󰀴󰁠󰁠󠅛󠅄󠄓󠅝󠅛󠅆󠅁󠅝󠇯` | U+F0034 U+F0060 U+F0060 U+E015B U+E0144 U+E0113 U+E015D U+E015B U+E0146 U+E0141 U+E015D U+E01EF | always |
| `ÓÚ` | `󰀴󰁠󰁠󠅛󠅄󠄓󠅝󠅛󠅄󠅁󠅝󠇯` | U+F0034 U+F0060 U+F0060 U+E015B U+E0144 U+E0113 U+E015D U+E015B U+E0144 U+E0141 U+E015D U+E01EF | always |
| `ay` | `󰀰󠅁󠅙󠇯` | U+F0030 U+E0141 U+E0159 U+E01EF | before a consonant |
| `ay` | `󰀰󠅁󠅙󠇯` | U+F0030 U+E0141 U+E0159 U+E01EF | at the end of a word |
| `aY` | `󰀰󠅁󠄹󠇯` | U+F0030 U+E0141 U+E0139 U+E01EF | before a consonant |
| `aY` | `󰀰󠅁󠄹󠇯` | U+F0030 U+E0141 U+E0139 U+E01EF | at the end of a word |
| `Ay` | `󰀰󠄡󠅙󠇯` | U+F0030 U+E0121 U+E0159 U+E01EF | before a consonant |
| `Ay` | `󰀰󠄡󠅙󠇯` | U+F0030 U+E0121 U+E0159 U+E01EF | at the end of a word |
| `AY` | `󰀰󠄡󠄹󠇯` | U+F0030 U+E0121 U+E0139 U+E01EF | before a consonant |
| `AY` | `󰀰󠄡󠄹󠇯` | U+F0030 U+E0121 U+E0139 U+E01EF | at the end of a word |
| `áy` | `󰀰󰁠󠅛󠅅󠄑󠅝󠅙󠇯` | U+F0030 U+F0060 U+E015B U+E0145 U+E0111 U+E015D U+E0159 U+E01EF | before a consonant |
| `áy` | `󰀰󰁠󠅛󠅅󠄑󠅝󠅙󠇯` | U+F0030 U+F0060 U+E015B U+E0145 U+E0111 U+E015D U+E0159 U+E01EF | at the end of a word |
| `áY` | `󰀰󰁠󠅛󠅅󠄑󠅝󠄹󠇯` | U+F0030 U+F0060 U+E015B U+E0145 U+E0111 U+E015D U+E0139 U+E01EF | before a consonant |
| `áY` | `󰀰󰁠󠅛󠅅󠄑󠅝󠄹󠇯` | U+F0030 U+F0060 U+E015B U+E0145 U+E0111 U+E015D U+E0139 U+E01EF | at the end of a word |
| `Áy` | `󰀰󰁠󠅛󠅃󠄑󠅝󠅙󠇯` | U+F0030 U+F0060 U+E015B U+E0143 U+E0111 U+E015D U+E0159 U+E01EF | before a consonant |
| `Áy` | `󰀰󰁠󠅛󠅃󠄑󠅝󠅙󠇯` | U+F0030 U+F0060 U+E015B U+E0143 U+E0111 U+E015D U+E0159 U+E01EF | at the end of a word |
| `ÁY` | `󰀰󰁠󠅛󠅃󠄑󠅝󠄹󠇯` | U+F0030 U+F0060 U+E015B U+E0143 U+E0111 U+E015D U+E0139 U+E01EF | before a consonant |
| `ÁY` | `󰀰󰁠󠅛󠅃󠄑󠅝󠄹󠇯` | U+F0030 U+F0060 U+E015B U+E0143 U+E0111 U+E015D U+E0139 U+E01EF | at the end of a word |
| `ey` | `󰀲󠅅󠅙󠇯` | U+F0032 U+E0145 U+E0159 U+E01EF | before a consonant |
| `ëy` | `󰀲󠅛󠅅󠅂󠅝󠅙󠇯` | U+F0032 U+E015B U+E0145 U+E0142 U+E015D U+E0159 U+E01EF | before a consonant |
| `ey` | `󰀲󠅅󠅙󠇯` | U+F0032 U+E0145 U+E0159 U+E01EF | at the end of a word |
| `ëy` | `󰀲󠅛󠅅󠅂󠅝󠅙󠇯` | U+F0032 U+E015B U+E0145 U+E0142 U+E015D U+E0159 U+E01EF | at the end of a word |
| `eY` | `󰀲󠅅󠄹󠇯` | U+F0032 U+E0145 U+E0139 U+E01EF | before a consonant |
| `ëY` | `󰀲󠅛󠅅󠅂󠅝󠄹󠇯` | U+F0032 U+E015B U+E0145 U+E0142 U+E015D U+E0139 U+E01EF | before a consonant |
| `eY` | `󰀲󠅅󠄹󠇯` | U+F0032 U+E0145 U+E0139 U+E01EF | at the end of a word |
| `ëY` | `󰀲󠅛󠅅󠅂󠅝󠄹󠇯` | U+F0032 U+E015B U+E0145 U+E0142 U+E015D U+E0139 U+E01EF | at the end of a word |
| `Ey` | `󰀲󠄥󠅙󠇯` | U+F0032 U+E0125 U+E0159 U+E01EF | before a consonant |
| `Ëy` | `󰀲󠅛󠅃󠅂󠅝󠅙󠇯` | U+F0032 U+E015B U+E0143 U+E0142 U+E015D U+E0159 U+E01EF | before a consonant |
| `Ey` | `󰀲󠄥󠅙󠇯` | U+F0032 U+E0125 U+E0159 U+E01EF | at the end of a word |
| `Ëy` | `󰀲󠅛󠅃󠅂󠅝󠅙󠇯` | U+F0032 U+E015B U+E0143 U+E0142 U+E015D U+E0159 U+E01EF | at the end of a word |
| `EY` | `󰀲󠄥󠄹󠇯` | U+F0032 U+E0125 U+E0139 U+E01EF | before a consonant |
| `ËY` | `󰀲󠅛󠅃󠅂󠅝󠄹󠇯` | U+F0032 U+E015B U+E0143 U+E0142 U+E015D U+E0139 U+E01EF | before a consonant |
| `EY` | `󰀲󠄥󠄹󠇯` | U+F0032 U+E0125 U+E0139 U+E01EF | at the end of a word |
| `ËY` | `󰀲󠅛󠅃󠅂󠅝󠄹󠇯` | U+F0032 U+E015B U+E0143 U+E0142 U+E015D U+E0139 U+E01EF | at the end of a word |
| `éy` | `󰀲󰁠󠅛󠅅󠄙󠅝󠅙󠇯` | U+F0032 U+F0060 U+E015B U+E0145 U+E0119 U+E015D U+E0159 U+E01EF | before a consonant |
| `éy` | `󰀲󰁠󠅛󠅅󠄙󠅝󠅙󠇯` | U+F0032 U+F0060 U+E015B U+E0145 U+E0119 U+E015D U+E0159 U+E01EF | at the end of a word |
| `éY` | `󰀲󰁠󠅛󠅅󠄙󠅝󠄹󠇯` | U+F0032 U+F0060 U+E015B U+E0145 U+E0119 U+E015D U+E0139 U+E01EF | before a consonant |
| `éY` | `󰀲󰁠󠅛󠅅󠄙󠅝󠄹󠇯` | U+F0032 U+F0060 U+E015B U+E0145 U+E0119 U+E015D U+E0139 U+E01EF | at the end of a word |
| `Éy` | `󰀲󰁠󠅛󠅃󠄙󠅝󠅙󠇯` | U+F0032 U+F0060 U+E015B U+E0143 U+E0119 U+E015D U+E0159 U+E01EF | before a consonant |
| `Éy` | `󰀲󰁠󠅛󠅃󠄙󠅝󠅙󠇯` | U+F0032 U+F0060 U+E015B U+E0143 U+E0119 U+E015D U+E0159 U+E01EF | at the end of a word |
| `ÉY` | `󰀲󰁠󠅛󠅃󠄙󠅝󠄹󠇯` | U+F0032 U+F0060 U+E015B U+E0143 U+E0119 U+E015D U+E0139 U+E01EF | before a consonant |
| `ÉY` | `󰀲󰁠󠅛󠅃󠄙󠅝󠄹󠇯` | U+F0032 U+F0060 U+E015B U+E0143 U+E0119 U+E015D U+E0139 U+E01EF | at the end of a word |
| `oy` | `󰀳󠅏󠅙󠇯` | U+F0033 U+E014F U+E0159 U+E01EF | before a consonant |
| `oy` | `󰀳󠅏󠅙󠇯` | U+F0033 U+E014F U+E0159 U+E01EF | at the end of a word |
| `oY` | `󰀳󠅏󠄹󠇯` | U+F0033 U+E014F U+E0139 U+E01EF | before a consonant |
| `oY` | `󰀳󠅏󠄹󠇯` | U+F0033 U+E014F U+E0139 U+E01EF | at the end of a word |
| `Oy` | `󰀳󠄯󠅙󠇯` | U+F0033 U+E012F U+E0159 U+E01EF | before a consonant |
| `Oy` | `󰀳󠄯󠅙󠇯` | U+F0033 U+E012F U+E0159 U+E01EF | at the end of a word |
| `OY` | `󰀳󠄯󠄹󠇯` | U+F0033 U+E012F U+E0139 U+E01EF | before a consonant |
| `OY` | `󰀳󠄯󠄹󠇯` | U+F0033 U+E012F U+E0139 U+E01EF | at the end of a word |
| `óy` | `󰀳󰁠󠅛󠅆󠄓󠅝󠅙󠇯` | U+F0033 U+F0060 U+E015B U+E0146 U+E0113 U+E015D U+E0159 U+E01EF | before a consonant |
| `óy` | `󰀳󰁠󠅛󠅆󠄓󠅝󠅙󠇯` | U+F0033 U+F0060 U+E015B U+E0146 U+E0113 U+E015D U+E0159 U+E01EF | at the end of a word |
| `óY` | `󰀳󰁠󠅛󠅆󠄓󠅝󠄹󠇯` | U+F0033 U+F0060 U+E015B U+E0146 U+E0113 U+E015D U+E0139 U+E01EF | before a consonant |
| `óY` | `󰀳󰁠󠅛󠅆󠄓󠅝󠄹󠇯` | U+F0033 U+F0060 U+E015B U+E0146 U+E0113 U+E015D U+E0139 U+E01EF | at the end of a word |
| `Óy` | `󰀳󰁠󠅛󠅄󠄓󠅝󠅙󠇯` | U+F0033 U+F0060 U+E015B U+E0144 U+E0113 U+E015D U+E0159 U+E01EF | before a consonant |
| `Óy` | `󰀳󰁠󠅛󠅄󠄓󠅝󠅙󠇯` | U+F0033 U+F0060 U+E015B U+E0144 U+E0113 U+E015D U+E0159 U+E01EF | at the end of a word |
| `ÓY` | `󰀳󰁠󠅛󠅄󠄓󠅝󠄹󠇯` | U+F0033 U+F0060 U+E015B U+E0144 U+E0113 U+E015D U+E0139 U+E01EF | before a consonant |
| `ÓY` | `󰀳󰁠󠅛󠅄󠄓󠅝󠄹󠇯` | U+F0033 U+F0060 U+E015B U+E0144 U+E0113 U+E015D U+E0139 U+E01EF | at the end of a word |
| `y` | `󰀗` | U+F0017 | before a vowel |
| `y` | `󰀂󠅙󠇯` | U+F0002 U+E0159 U+E01EF | always |
| `Y` | `󰀗󠄹󠇯` | U+F0017 U+E0139 U+E01EF | before a vowel |
| `Y` | `󰀂󠄹󠇯` | U+F0002 U+E0139 U+E01EF | always |
| `“` | `󰁔` | U+F0054 | always |
| `”` | `󰁕` | U+F0055 | always |
| `0` | `󰁀` | U+F0040 | always |
| `1` | `󰁁` | U+F0041 | always |
| `2` | `󰁂` | U+F0042 | always |
| `3` | `󰁃` | U+F0043 | always |
| `4` | `󰁄` | U+F0044 | always |
| `5` | `󰁅` | U+F0045 | always |
| `6` | `󰁆` | U+F0046 | always |
| `7` | `󰁇` | U+F0047 | always |
| `8` | `󰁈` | U+F0048 | always |
| `9` | `󰁉` | U+F0049 | always |
| `@` | `󰁊` | U+F004A | always |
| `#` | `󰁋` | U+F004B | always |
| `$` | `󰁌` | U+F004C | always |
| `%` | `󰁍` | U+F004D | always |
| `^` | `󰁎` | U+F004E | always |
| `&` | `󰁏` | U+F004F | always |
| `.` | `󰁐` | U+F0050 | always |
| `,` | `󰁑` | U+F0051 | always |
| `!` | `󰁒` | U+F0052 | always |
| `-` | `󰁓` | U+F0053 | always |

## Round trip

Every encoding round-trips exactly: decoding the code points that encoding wrote gives back the roman text, and encoding that gives the same code points. The Code points column shows every character a row writes, including any that is invisible.

This page is written from `encodings/pirzath.json` by `tools/encoding_docs.py`.
