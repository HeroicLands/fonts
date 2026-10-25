# semaron encoding

Semaron Kuriale is an alphabet of capital and small letters, written left to right. This encoding writes a roman spelling in its letters: `th` is one letter, `ch` is written with the letters for t, s and h, a doubled `a`, `i` or `u` is a long vowel, `q` is written as `k`, and `y` before a vowel is a glide. An apostrophe or hyphen after a letter writes the catch, a mark on the letter before it.

## Fonts

- Semaron Kuriale (`semaron-kuriale`), written left to right.

## Running it

`encode.py` needs only Python 3.9 or later. From a checkout, or from `node_modules/@heroiclands/fonts`:

```sh
python3 encode.py --encoding semaron "thalen kaa"
python3 encode.py --encoding semaron --decode "󰉐󰈰󰈺󰈳󰈼 󰈹󰉈"
```

The first command writes `󰉐󰈰󰈺󰈳󰈼 󰈹󰉈`, and the second reads it back as `thalen kaa`. `--codepoints` prints the result as `U+XXXX` values, and the text may come from standard input.

From Python:

```python
import encode

text = encode.encode("semaron", "thalen kaa")
roman = encode.decode("semaron", text)
```

## Vowels and conditions

The vowels are `AEIOUaeiouÀÁÉËÍÓÚàáéëíóú`.

A row marked _before a vowel_ applies when the next character is a vowel.

Where several rows begin with the same roman, the longest wins, and among rows of one length a row whose condition holds comes before a row with none. A row whose condition fails is skipped.

## Rows

The rows are in the order the file states them.

| Roman | Character | Code points | When |
| --- | --- | --- | --- |
| `tà` | `󰉁󰉰󰈰󠅔󠅛󠅅󠄐󠅝󠇯` | U+F0241 U+F0270 U+F0230 U+E0154 U+E015B U+E0145 U+E0110 U+E015D U+E01EF | always |
| `tÀ` | `󰉁󰉰󰈀󠅔󠅛󠅃󠄐󠅝󠇯` | U+F0241 U+F0270 U+F0200 U+E0154 U+E015B U+E0143 U+E0110 U+E015D U+E01EF | always |
| `Tà` | `󰈑󰉰󰈰󠄴󠅛󠅅󠄐󠅝󠇯` | U+F0211 U+F0270 U+F0230 U+E0134 U+E015B U+E0145 U+E0110 U+E015D U+E01EF | always |
| `TÀ` | `󰈑󰉰󰈀󠄴󠅛󠅃󠄐󠅝󠇯` | U+F0211 U+F0270 U+F0200 U+E0134 U+E015B U+E0143 U+E0110 U+E015D U+E01EF | always |
| `kà` | `󰈹󰉰󰈰󠅋󠅛󠅅󠄐󠅝󠇯` | U+F0239 U+F0270 U+F0230 U+E014B U+E015B U+E0145 U+E0110 U+E015D U+E01EF | always |
| `kÀ` | `󰈹󰉰󰈀󠅋󠅛󠅃󠄐󠅝󠇯` | U+F0239 U+F0270 U+F0200 U+E014B U+E015B U+E0143 U+E0110 U+E015D U+E01EF | always |
| `Kà` | `󰈉󰉰󰈰󠄫󠅛󠅅󠄐󠅝󠇯` | U+F0209 U+F0270 U+F0230 U+E012B U+E015B U+E0145 U+E0110 U+E015D U+E01EF | always |
| `KÀ` | `󰈉󰉰󰈀󠄫󠅛󠅃󠄐󠅝󠇯` | U+F0209 U+F0270 U+F0200 U+E012B U+E015B U+E0143 U+E0110 U+E015D U+E01EF | always |
| `dà` | `󰈲󰉰󰈰󠅄󠅛󠅅󠄐󠅝󠇯` | U+F0232 U+F0270 U+F0230 U+E0144 U+E015B U+E0145 U+E0110 U+E015D U+E01EF | always |
| `dÀ` | `󰈲󰉰󰈀󠅄󠅛󠅃󠄐󠅝󠇯` | U+F0232 U+F0270 U+F0200 U+E0144 U+E015B U+E0143 U+E0110 U+E015D U+E01EF | always |
| `Dà` | `󰈂󰉰󰈰󠄤󠅛󠅅󠄐󠅝󠇯` | U+F0202 U+F0270 U+F0230 U+E0124 U+E015B U+E0145 U+E0110 U+E015D U+E01EF | always |
| `DÀ` | `󰈂󰉰󰈀󠄤󠅛󠅃󠄐󠅝󠇯` | U+F0202 U+F0270 U+F0200 U+E0124 U+E015B U+E0143 U+E0110 U+E015D U+E01EF | always |
| `gà` | `󰈵󰉰󰈰󠅇󠅛󠅅󠄐󠅝󠇯` | U+F0235 U+F0270 U+F0230 U+E0147 U+E015B U+E0145 U+E0110 U+E015D U+E01EF | always |
| `gÀ` | `󰈵󰉰󰈀󠅇󠅛󠅃󠄐󠅝󠇯` | U+F0235 U+F0270 U+F0200 U+E0147 U+E015B U+E0143 U+E0110 U+E015D U+E01EF | always |
| `Gà` | `󰈅󰉰󰈰󠄧󠅛󠅅󠄐󠅝󠇯` | U+F0205 U+F0270 U+F0230 U+E0127 U+E015B U+E0145 U+E0110 U+E015D U+E01EF | always |
| `GÀ` | `󰈅󰉰󰈀󠄧󠅛󠅃󠄐󠅝󠇯` | U+F0205 U+F0270 U+F0200 U+E0127 U+E015B U+E0143 U+E0110 U+E015D U+E01EF | always |
| `à` | `󰈰󰉰󠅛󠅅󠄐󠅝󠇯` | U+F0230 U+F0270 U+E015B U+E0145 U+E0110 U+E015D U+E01EF | always |
| `À` | `󰈀󰉰󠅛󠅃󠄐󠅝󠇯` | U+F0200 U+F0270 U+E015B U+E0143 U+E0110 U+E015D U+E01EF | always |
| `a` | `󰈰` | U+F0230 | always |
| `A` | `󰈀` | U+F0200 | always |
| `b` | `󰈱` | U+F0231 | always |
| `B` | `󰈁` | U+F0201 | always |
| `d` | `󰈲` | U+F0232 | always |
| `D` | `󰈂` | U+F0202 | always |
| `e` | `󰈳` | U+F0233 | always |
| `ë` | `󰈳󠅛󠅅󠅂󠅝󠇯` | U+F0233 U+E015B U+E0145 U+E0142 U+E015D U+E01EF | always |
| `E` | `󰈃` | U+F0203 | always |
| `Ë` | `󰈃󠅛󠅃󠅂󠅝󠇯` | U+F0203 U+E015B U+E0143 U+E0142 U+E015D U+E01EF | always |
| `f` | `󰈴` | U+F0234 | always |
| `F` | `󰈄` | U+F0204 | always |
| `g` | `󰈵` | U+F0235 | always |
| `G` | `󰈅` | U+F0205 | always |
| `h` | `󰈶` | U+F0236 | always |
| `H` | `󰈆` | U+F0206 | always |
| `i` | `󰈷` | U+F0237 | always |
| `I` | `󰈇` | U+F0207 | always |
| `j` | `󰈸` | U+F0238 | always |
| `J` | `󰈈` | U+F0208 | always |
| `k` | `󰈹` | U+F0239 | always |
| `K` | `󰈉` | U+F0209 | always |
| `l` | `󰈺` | U+F023A | always |
| `L` | `󰈊` | U+F020A | always |
| `m` | `󰈻` | U+F023B | always |
| `M` | `󰈋` | U+F020B | always |
| `n` | `󰈼` | U+F023C | always |
| `N` | `󰈌` | U+F020C | always |
| `o` | `󰈽` | U+F023D | always |
| `O` | `󰈍` | U+F020D | always |
| `p` | `󰈾` | U+F023E | always |
| `P` | `󰈎` | U+F020E | always |
| `q` | `󰈹󠅑󠇯` | U+F0239 U+E0151 U+E01EF | always |
| `Q` | `󰈉󠄱󠇯` | U+F0209 U+E0131 U+E01EF | always |
| `r` | `󰈿` | U+F023F | always |
| `R` | `󰈏` | U+F020F | always |
| `s` | `󰉀` | U+F0240 | always |
| `S` | `󰈐` | U+F0210 | always |
| `t` | `󰉁` | U+F0241 | always |
| `T` | `󰈑` | U+F0211 | always |
| `u` | `󰉂` | U+F0242 | always |
| `U` | `󰈒` | U+F0212 | always |
| `v` | `󰉃` | U+F0243 | always |
| `V` | `󰈓` | U+F0213 | always |
| `w` | `󰉄` | U+F0244 | always |
| `W` | `󰈔` | U+F0214 | always |
| `z` | `󰉆` | U+F0246 | always |
| `Z` | `󰈖` | U+F0216 | always |
| `á` | `󰈰󠅛󠅅󠄑󠅝󠇯` | U+F0230 U+E015B U+E0145 U+E0111 U+E015D U+E01EF | always |
| `Á` | `󰈀󠅛󠅃󠄑󠅝󠇯` | U+F0200 U+E015B U+E0143 U+E0111 U+E015D U+E01EF | always |
| `é` | `󰈳󠅛󠅅󠄙󠅝󠇯` | U+F0233 U+E015B U+E0145 U+E0119 U+E015D U+E01EF | always |
| `É` | `󰈃󠅛󠅃󠄙󠅝󠇯` | U+F0203 U+E015B U+E0143 U+E0119 U+E015D U+E01EF | always |
| `í` | `󰈷󠅛󠅅󠅄󠅝󠇯` | U+F0237 U+E015B U+E0145 U+E0144 U+E015D U+E01EF | always |
| `Í` | `󰈇󠅛󠅃󠅄󠅝󠇯` | U+F0207 U+E015B U+E0143 U+E0144 U+E015D U+E01EF | always |
| `ó` | `󰈽󠅛󠅆󠄓󠅝󠇯` | U+F023D U+E015B U+E0146 U+E0113 U+E015D U+E01EF | always |
| `Ó` | `󰈍󠅛󠅄󠄓󠅝󠇯` | U+F020D U+E015B U+E0144 U+E0113 U+E015D U+E01EF | always |
| `ú` | `󰉂󠅛󠅆󠅁󠅝󠇯` | U+F0242 U+E015B U+E0146 U+E0141 U+E015D U+E01EF | always |
| `Ú` | `󰈒󠅛󠅄󠅁󠅝󠇯` | U+F0212 U+E015B U+E0144 U+E0141 U+E015D U+E01EF | always |
| `th` | `󰉐` | U+F0250 | always |
| `tH` | `󰉐󠅔󠄨󠇯` | U+F0250 U+E0154 U+E0128 U+E01EF | always |
| `Th` | `󰉑` | U+F0251 | always |
| `TH` | `󰉑󠄴󠄨󠇯` | U+F0251 U+E0134 U+E0128 U+E01EF | always |
| `ch` | `󰉁󰉀󰈶󠅃󠅈󠇯` | U+F0241 U+F0240 U+F0236 U+E0143 U+E0148 U+E01EF | always |
| `cH` | `󰉁󰉀󰈶󠅃󠄨󠇯` | U+F0241 U+F0240 U+F0236 U+E0143 U+E0128 U+E01EF | always |
| `Ch` | `󰈑󰉀󰈶󠄣󠅈󠇯` | U+F0211 U+F0240 U+F0236 U+E0123 U+E0148 U+E01EF | always |
| `CH` | `󰈑󰉀󰈶󠄣󠄨󠇯` | U+F0211 U+F0240 U+F0236 U+E0123 U+E0128 U+E01EF | always |
| `aa` | `󰉈` | U+F0248 | always |
| `aA` | `󰉈󠅁󠄡󠇯` | U+F0248 U+E0141 U+E0121 U+E01EF | always |
| `aá` | `󰉈󠅁󠅛󠅅󠄑󠅝󠇯` | U+F0248 U+E0141 U+E015B U+E0145 U+E0111 U+E015D U+E01EF | always |
| `aÁ` | `󰉈󠅁󠅛󠅃󠄑󠅝󠇯` | U+F0248 U+E0141 U+E015B U+E0143 U+E0111 U+E015D U+E01EF | always |
| `áa` | `󰉈󠅛󠅅󠄑󠅝󠅁󠇯` | U+F0248 U+E015B U+E0145 U+E0111 U+E015D U+E0141 U+E01EF | always |
| `áA` | `󰉈󠅛󠅅󠄑󠅝󠄡󠇯` | U+F0248 U+E015B U+E0145 U+E0111 U+E015D U+E0121 U+E01EF | always |
| `áá` | `󰉈󠅛󠅅󠄑󠅝󠅛󠅅󠄑󠅝󠇯` | U+F0248 U+E015B U+E0145 U+E0111 U+E015D U+E015B U+E0145 U+E0111 U+E015D U+E01EF | always |
| `áÁ` | `󰉈󠅛󠅅󠄑󠅝󠅛󠅃󠄑󠅝󠇯` | U+F0248 U+E015B U+E0145 U+E0111 U+E015D U+E015B U+E0143 U+E0111 U+E015D U+E01EF | always |
| `Aa` | `󰈠` | U+F0220 | always |
| `AA` | `󰈠󠄡󠄡󠇯` | U+F0220 U+E0121 U+E0121 U+E01EF | always |
| `Aá` | `󰈠󠄡󠅛󠅅󠄑󠅝󠇯` | U+F0220 U+E0121 U+E015B U+E0145 U+E0111 U+E015D U+E01EF | always |
| `AÁ` | `󰈠󠄡󠅛󠅃󠄑󠅝󠇯` | U+F0220 U+E0121 U+E015B U+E0143 U+E0111 U+E015D U+E01EF | always |
| `Áa` | `󰈠󠅛󠅃󠄑󠅝󠅁󠇯` | U+F0220 U+E015B U+E0143 U+E0111 U+E015D U+E0141 U+E01EF | always |
| `ÁA` | `󰈠󠅛󠅃󠄑󠅝󠄡󠇯` | U+F0220 U+E015B U+E0143 U+E0111 U+E015D U+E0121 U+E01EF | always |
| `Áá` | `󰈠󠅛󠅃󠄑󠅝󠅛󠅅󠄑󠅝󠇯` | U+F0220 U+E015B U+E0143 U+E0111 U+E015D U+E015B U+E0145 U+E0111 U+E015D U+E01EF | always |
| `ÁÁ` | `󰈠󠅛󠅃󠄑󠅝󠅛󠅃󠄑󠅝󠇯` | U+F0220 U+E015B U+E0143 U+E0111 U+E015D U+E015B U+E0143 U+E0111 U+E015D U+E01EF | always |
| `ii` | `󰉊` | U+F024A | always |
| `iI` | `󰉊󠅉󠄩󠇯` | U+F024A U+E0149 U+E0129 U+E01EF | always |
| `ií` | `󰉊󠅉󠅛󠅅󠅄󠅝󠇯` | U+F024A U+E0149 U+E015B U+E0145 U+E0144 U+E015D U+E01EF | always |
| `iÍ` | `󰉊󠅉󠅛󠅃󠅄󠅝󠇯` | U+F024A U+E0149 U+E015B U+E0143 U+E0144 U+E015D U+E01EF | always |
| `íi` | `󰉊󠅛󠅅󠅄󠅝󠅉󠇯` | U+F024A U+E015B U+E0145 U+E0144 U+E015D U+E0149 U+E01EF | always |
| `íI` | `󰉊󠅛󠅅󠅄󠅝󠄩󠇯` | U+F024A U+E015B U+E0145 U+E0144 U+E015D U+E0129 U+E01EF | always |
| `íí` | `󰉊󠅛󠅅󠅄󠅝󠅛󠅅󠅄󠅝󠇯` | U+F024A U+E015B U+E0145 U+E0144 U+E015D U+E015B U+E0145 U+E0144 U+E015D U+E01EF | always |
| `íÍ` | `󰉊󠅛󠅅󠅄󠅝󠅛󠅃󠅄󠅝󠇯` | U+F024A U+E015B U+E0145 U+E0144 U+E015D U+E015B U+E0143 U+E0144 U+E015D U+E01EF | always |
| `Ii` | `󰈢` | U+F0222 | always |
| `II` | `󰈢󠄩󠄩󠇯` | U+F0222 U+E0129 U+E0129 U+E01EF | always |
| `Ií` | `󰈢󠄩󠅛󠅅󠅄󠅝󠇯` | U+F0222 U+E0129 U+E015B U+E0145 U+E0144 U+E015D U+E01EF | always |
| `IÍ` | `󰈢󠄩󠅛󠅃󠅄󠅝󠇯` | U+F0222 U+E0129 U+E015B U+E0143 U+E0144 U+E015D U+E01EF | always |
| `Íi` | `󰈢󠅛󠅃󠅄󠅝󠅉󠇯` | U+F0222 U+E015B U+E0143 U+E0144 U+E015D U+E0149 U+E01EF | always |
| `ÍI` | `󰈢󠅛󠅃󠅄󠅝󠄩󠇯` | U+F0222 U+E015B U+E0143 U+E0144 U+E015D U+E0129 U+E01EF | always |
| `Íí` | `󰈢󠅛󠅃󠅄󠅝󠅛󠅅󠅄󠅝󠇯` | U+F0222 U+E015B U+E0143 U+E0144 U+E015D U+E015B U+E0145 U+E0144 U+E015D U+E01EF | always |
| `ÍÍ` | `󰈢󠅛󠅃󠅄󠅝󠅛󠅃󠅄󠅝󠇯` | U+F0222 U+E015B U+E0143 U+E0144 U+E015D U+E015B U+E0143 U+E0144 U+E015D U+E01EF | always |
| `uu` | `󰉌` | U+F024C | always |
| `uU` | `󰉌󠅕󠄵󠇯` | U+F024C U+E0155 U+E0135 U+E01EF | always |
| `uú` | `󰉌󠅕󠅛󠅆󠅁󠅝󠇯` | U+F024C U+E0155 U+E015B U+E0146 U+E0141 U+E015D U+E01EF | always |
| `uÚ` | `󰉌󠅕󠅛󠅄󠅁󠅝󠇯` | U+F024C U+E0155 U+E015B U+E0144 U+E0141 U+E015D U+E01EF | always |
| `úu` | `󰉌󠅛󠅆󠅁󠅝󠅕󠇯` | U+F024C U+E015B U+E0146 U+E0141 U+E015D U+E0155 U+E01EF | always |
| `úU` | `󰉌󠅛󠅆󠅁󠅝󠄵󠇯` | U+F024C U+E015B U+E0146 U+E0141 U+E015D U+E0135 U+E01EF | always |
| `úú` | `󰉌󠅛󠅆󠅁󠅝󠅛󠅆󠅁󠅝󠇯` | U+F024C U+E015B U+E0146 U+E0141 U+E015D U+E015B U+E0146 U+E0141 U+E015D U+E01EF | always |
| `úÚ` | `󰉌󠅛󠅆󠅁󠅝󠅛󠅄󠅁󠅝󠇯` | U+F024C U+E015B U+E0146 U+E0141 U+E015D U+E015B U+E0144 U+E0141 U+E015D U+E01EF | always |
| `Uu` | `󰈤` | U+F0224 | always |
| `UU` | `󰈤󠄵󠄵󠇯` | U+F0224 U+E0135 U+E0135 U+E01EF | always |
| `Uú` | `󰈤󠄵󠅛󠅆󠅁󠅝󠇯` | U+F0224 U+E0135 U+E015B U+E0146 U+E0141 U+E015D U+E01EF | always |
| `UÚ` | `󰈤󠄵󠅛󠅄󠅁󠅝󠇯` | U+F0224 U+E0135 U+E015B U+E0144 U+E0141 U+E015D U+E01EF | always |
| `Úu` | `󰈤󠅛󠅄󠅁󠅝󠅕󠇯` | U+F0224 U+E015B U+E0144 U+E0141 U+E015D U+E0155 U+E01EF | always |
| `ÚU` | `󰈤󠅛󠅄󠅁󠅝󠄵󠇯` | U+F0224 U+E015B U+E0144 U+E0141 U+E015D U+E0135 U+E01EF | always |
| `Úú` | `󰈤󠅛󠅄󠅁󠅝󠅛󠅆󠅁󠅝󠇯` | U+F0224 U+E015B U+E0144 U+E0141 U+E015D U+E015B U+E0146 U+E0141 U+E015D U+E01EF | always |
| `ÚÚ` | `󰈤󠅛󠅄󠅁󠅝󠅛󠅄󠅁󠅝󠇯` | U+F0224 U+E015B U+E0144 U+E0141 U+E015D U+E015B U+E0144 U+E0141 U+E015D U+E01EF | always |
| `y` | `󰉅` | U+F0245 | before a vowel |
| `y` | `󰈷󠅙󠇯` | U+F0237 U+E0159 U+E01EF | always |
| `Y` | `󰈕` | U+F0215 | before a vowel |
| `Y` | `󰈇󠄹󠇯` | U+F0207 U+E0139 U+E01EF | always |
| `ý` | `󰉅󠅛󠅆󠅄󠅝󠇯` | U+F0245 U+E015B U+E0146 U+E0144 U+E015D U+E01EF | before a vowel |
| `ý` | `󰈷󠅛󠅆󠅄󠅝󠇯` | U+F0237 U+E015B U+E0146 U+E0144 U+E015D U+E01EF | always |
| `Ý` | `󰈕󠅛󠅄󠅄󠅝󠇯` | U+F0215 U+E015B U+E0144 U+E0144 U+E015D U+E01EF | before a vowel |
| `Ý` | `󰈇󠅛󠅄󠅄󠅝󠇯` | U+F0207 U+E015B U+E0144 U+E0144 U+E015D U+E01EF | always |
| `'` | `󰉰` | U+F0270 | always |
| `’` | `󰉰󠅛󠄒󠄐󠄑󠄙󠅝󠇯` | U+F0270 U+E015B U+E0112 U+E0110 U+E0111 U+E0119 U+E015D U+E01EF | always |
| `` ` `` | `󰉰󠅀󠇯` | U+F0270 U+E0140 U+E01EF | always |
| `-` | `󰉰󠄍󠇯` | U+F0270 U+E010D U+E01EF | always |
| `.` | `󰉨` | U+F0268 | always |
| `0` | `󰉘` | U+F0258 | always |
| `1` | `󰉙` | U+F0259 | always |
| `2` | `󰉚` | U+F025A | always |
| `3` | `󰉛` | U+F025B | always |
| `4` | `󰉜` | U+F025C | always |
| `5` | `󰉝` | U+F025D | always |
| `6` | `󰉞` | U+F025E | always |
| `7` | `󰉟` | U+F025F | always |
| `8` | `󰉠` | U+F0260 | always |
| `9` | `󰉡` | U+F0261 | always |

## Round trip

Every encoding round-trips exactly: decoding the code points that encoding wrote gives back the roman text, and encoding that gives the same code points. The Code points column shows every character a row writes, including any that is invisible.

This page is written from `encodings/semaron.json` by `tools/encoding_docs.py`.
