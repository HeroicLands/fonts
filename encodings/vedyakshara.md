# vedyakshara encoding

Vedyakshara Classical is a left-to-right script in which each consonant carries the vowel `a`. This encoding writes a roman spelling in it: a consonant before a vowel is the bare consonant followed by that vowel's sign, a consonant elsewhere is the consonant with the cut that takes the vowel away, and `a` draws no sign of its own and is written as an invisible mark.

## Fonts

- Vedyakshara Classical (`vedyakshara-classical`), written left to right.

## Running it

`encode.py` needs only Python 3.9 or later. From a checkout, or from `node_modules/@heroiclands/fonts`:

```sh
python3 encode.py --encoding vedyakshara "kithe"
python3 encode.py --encoding vedyakshara --decode "󰐀󰐰󰐈󰐸󠅔󠇯󰐕󰐱"
```

The first command writes `󰐀󰐰󰐈󰐸󠅔󠇯󰐕󰐱`, and the second reads it back as `kithe`. `--codepoints` prints the result as `U+XXXX` values, and the text may come from standard input.

From Python:

```python
import encode

text = encode.encode("vedyakshara", "kithe")
roman = encode.decode("vedyakshara", text)
```

## Vowels and conditions

The vowels are `AEIOUaeiou`.

A row marked _before a vowel_ applies when the next character is a vowel.

A row marked _at the start of a word_ applies at the first character of the text or after whitespace, punctuation or a symbol.

Where several rows begin with the same roman, the longest wins, and among rows of one length a row whose condition holds comes before a row with none. A row whose condition fails is skipped.

## Rows

The rows are in the order the file states them.

| Roman | Character | Code points | When |
| --- | --- | --- | --- |
| `k` | `󰐀󰐸󠅋󠇯` | U+F0400 U+F0438 U+E014B U+E01EF | always |
| `k` | `󰐀` | U+F0400 | before a vowel |
| `K` | `󰐀󰐸󠄫󠇯` | U+F0400 U+F0438 U+E012B U+E01EF | always |
| `K` | `󰐀󠄫󠇯` | U+F0400 U+E012B U+E01EF | before a vowel |
| `kh` | `󰐁󰐸󠅋󠅈󠇯` | U+F0401 U+F0438 U+E014B U+E0148 U+E01EF | always |
| `kh` | `󰐁` | U+F0401 | before a vowel |
| `Kh` | `󰐁󰐸󠄫󠅈󠇯` | U+F0401 U+F0438 U+E012B U+E0148 U+E01EF | always |
| `Kh` | `󰐁󠄫󠅈󠇯` | U+F0401 U+E012B U+E0148 U+E01EF | before a vowel |
| `g` | `󰐂󰐸󠅇󠇯` | U+F0402 U+F0438 U+E0147 U+E01EF | always |
| `g` | `󰐂` | U+F0402 | before a vowel |
| `G` | `󰐂󰐸󠄧󠇯` | U+F0402 U+F0438 U+E0127 U+E01EF | always |
| `G` | `󰐂󠄧󠇯` | U+F0402 U+E0127 U+E01EF | before a vowel |
| `gh` | `󰐃󰐸󠅇󠅈󠇯` | U+F0403 U+F0438 U+E0147 U+E0148 U+E01EF | always |
| `gh` | `󰐃` | U+F0403 | before a vowel |
| `Gh` | `󰐃󰐸󠄧󠅈󠇯` | U+F0403 U+F0438 U+E0127 U+E0148 U+E01EF | always |
| `Gh` | `󰐃󠄧󠅈󠇯` | U+F0403 U+E0127 U+E0148 U+E01EF | before a vowel |
| `ng` | `󰐄󰐸󠅎󠅇󠇯` | U+F0404 U+F0438 U+E014E U+E0147 U+E01EF | always |
| `ng` | `󰐄` | U+F0404 | before a vowel |
| `Ng` | `󰐄󰐸󠄮󠅇󠇯` | U+F0404 U+F0438 U+E012E U+E0147 U+E01EF | always |
| `Ng` | `󰐄󠄮󠅇󠇯` | U+F0404 U+E012E U+E0147 U+E01EF | before a vowel |
| `ch` | `󰐅󰐸󠅃󠅈󠇯` | U+F0405 U+F0438 U+E0143 U+E0148 U+E01EF | always |
| `ch` | `󰐅` | U+F0405 | before a vowel |
| `Ch` | `󰐅󰐸󠄣󠅈󠇯` | U+F0405 U+F0438 U+E0123 U+E0148 U+E01EF | always |
| `Ch` | `󰐅󠄣󠅈󠇯` | U+F0405 U+E0123 U+E0148 U+E01EF | before a vowel |
| `j` | `󰐆󰐸󠅊󠇯` | U+F0406 U+F0438 U+E014A U+E01EF | always |
| `j` | `󰐆` | U+F0406 | before a vowel |
| `J` | `󰐆󰐸󠄪󠇯` | U+F0406 U+F0438 U+E012A U+E01EF | always |
| `J` | `󰐆󠄪󠇯` | U+F0406 U+E012A U+E01EF | before a vowel |
| `ny` | `󰐇󰐸󠅎󠅙󠇯` | U+F0407 U+F0438 U+E014E U+E0159 U+E01EF | always |
| `ny` | `󰐇` | U+F0407 | before a vowel |
| `Ny` | `󰐇󰐸󠄮󠅙󠇯` | U+F0407 U+F0438 U+E012E U+E0159 U+E01EF | always |
| `Ny` | `󰐇󠄮󠅙󠇯` | U+F0407 U+E012E U+E0159 U+E01EF | before a vowel |
| `t` | `󰐈󰐸󠅔󠇯` | U+F0408 U+F0438 U+E0154 U+E01EF | always |
| `t` | `󰐈` | U+F0408 | before a vowel |
| `T` | `󰐈󰐸󠄴󠇯` | U+F0408 U+F0438 U+E0134 U+E01EF | always |
| `T` | `󰐈󠄴󠇯` | U+F0408 U+E0134 U+E01EF | before a vowel |
| `d` | `󰐉󰐸󠅄󠇯` | U+F0409 U+F0438 U+E0144 U+E01EF | always |
| `d` | `󰐉` | U+F0409 | before a vowel |
| `D` | `󰐉󰐸󠄤󠇯` | U+F0409 U+F0438 U+E0124 U+E01EF | always |
| `D` | `󰐉󠄤󠇯` | U+F0409 U+E0124 U+E01EF | before a vowel |
| `n` | `󰐊󰐸󠅎󠇯` | U+F040A U+F0438 U+E014E U+E01EF | always |
| `n` | `󰐊` | U+F040A | before a vowel |
| `N` | `󰐊󰐸󠄮󠇯` | U+F040A U+F0438 U+E012E U+E01EF | always |
| `N` | `󰐊󠄮󠇯` | U+F040A U+E012E U+E01EF | before a vowel |
| `p` | `󰐋󰐸󠅐󠇯` | U+F040B U+F0438 U+E0150 U+E01EF | always |
| `p` | `󰐋` | U+F040B | before a vowel |
| `P` | `󰐋󰐸󠄰󠇯` | U+F040B U+F0438 U+E0130 U+E01EF | always |
| `P` | `󰐋󠄰󠇯` | U+F040B U+E0130 U+E01EF | before a vowel |
| `b` | `󰐌󰐸󠅂󠇯` | U+F040C U+F0438 U+E0142 U+E01EF | always |
| `b` | `󰐌` | U+F040C | before a vowel |
| `B` | `󰐌󰐸󠄢󠇯` | U+F040C U+F0438 U+E0122 U+E01EF | always |
| `B` | `󰐌󠄢󠇯` | U+F040C U+E0122 U+E01EF | before a vowel |
| `bh` | `󰐍󰐸󠅂󠅈󠇯` | U+F040D U+F0438 U+E0142 U+E0148 U+E01EF | always |
| `bh` | `󰐍` | U+F040D | before a vowel |
| `Bh` | `󰐍󰐸󠄢󠅈󠇯` | U+F040D U+F0438 U+E0122 U+E0148 U+E01EF | always |
| `Bh` | `󰐍󠄢󠅈󠇯` | U+F040D U+E0122 U+E0148 U+E01EF | before a vowel |
| `m` | `󰐎󰐸󠅍󠇯` | U+F040E U+F0438 U+E014D U+E01EF | always |
| `m` | `󰐎` | U+F040E | before a vowel |
| `M` | `󰐎󰐸󠄭󠇯` | U+F040E U+F0438 U+E012D U+E01EF | always |
| `M` | `󰐎󠄭󠇯` | U+F040E U+E012D U+E01EF | before a vowel |
| `y` | `󰐏󰐸󠅙󠇯` | U+F040F U+F0438 U+E0159 U+E01EF | always |
| `y` | `󰐏` | U+F040F | before a vowel |
| `Y` | `󰐏󰐸󠄹󠇯` | U+F040F U+F0438 U+E0139 U+E01EF | always |
| `Y` | `󰐏󠄹󠇯` | U+F040F U+E0139 U+E01EF | before a vowel |
| `r` | `󰐐󰐸󠅒󠇯` | U+F0410 U+F0438 U+E0152 U+E01EF | always |
| `r` | `󰐐` | U+F0410 | before a vowel |
| `R` | `󰐐󰐸󠄲󠇯` | U+F0410 U+F0438 U+E0132 U+E01EF | always |
| `R` | `󰐐󠄲󠇯` | U+F0410 U+E0132 U+E01EF | before a vowel |
| `l` | `󰐑󰐸󠅌󠇯` | U+F0411 U+F0438 U+E014C U+E01EF | always |
| `l` | `󰐑` | U+F0411 | before a vowel |
| `L` | `󰐑󰐸󠄬󠇯` | U+F0411 U+F0438 U+E012C U+E01EF | always |
| `L` | `󰐑󠄬󠇯` | U+F0411 U+E012C U+E01EF | before a vowel |
| `v` | `󰐒󰐸󠅖󠇯` | U+F0412 U+F0438 U+E0156 U+E01EF | always |
| `v` | `󰐒` | U+F0412 | before a vowel |
| `V` | `󰐒󰐸󠄶󠇯` | U+F0412 U+F0438 U+E0136 U+E01EF | always |
| `V` | `󰐒󠄶󠇯` | U+F0412 U+E0136 U+E01EF | before a vowel |
| `sh` | `󰐓󰐸󠅓󠅈󠇯` | U+F0413 U+F0438 U+E0153 U+E0148 U+E01EF | always |
| `sh` | `󰐓` | U+F0413 | before a vowel |
| `Sh` | `󰐓󰐸󠄳󠅈󠇯` | U+F0413 U+F0438 U+E0133 U+E0148 U+E01EF | always |
| `Sh` | `󰐓󠄳󠅈󠇯` | U+F0413 U+E0133 U+E0148 U+E01EF | before a vowel |
| `s` | `󰐔󰐸󠅓󠇯` | U+F0414 U+F0438 U+E0153 U+E01EF | always |
| `s` | `󰐔` | U+F0414 | before a vowel |
| `S` | `󰐔󰐸󠄳󠇯` | U+F0414 U+F0438 U+E0133 U+E01EF | always |
| `S` | `󰐔󠄳󠇯` | U+F0414 U+E0133 U+E01EF | before a vowel |
| `h` | `󰐕󰐸󠅈󠇯` | U+F0415 U+F0438 U+E0148 U+E01EF | always |
| `h` | `󰐕` | U+F0415 | before a vowel |
| `H` | `󰐕󰐸󠄨󠇯` | U+F0415 U+F0438 U+E0128 U+E01EF | always |
| `H` | `󰐕󠄨󠇯` | U+F0415 U+E0128 U+E01EF | before a vowel |
| `f` | `󰐋󰐹󰐸󠅆󠇯` | U+F040B U+F0439 U+F0438 U+E0146 U+E01EF | always |
| `f` | `󰐋󰐹` | U+F040B U+F0439 | before a vowel |
| `F` | `󰐋󰐹󰐸󠄦󠇯` | U+F040B U+F0439 U+F0438 U+E0126 U+E01EF | always |
| `F` | `󰐋󰐹󠄦󠇯` | U+F040B U+F0439 U+E0126 U+E01EF | before a vowel |
| `a` | `󠅁` | U+E0141 | always |
| `a` | `󰐠` | U+F0420 | at the start of a word |
| `A` | `󰐠󠄡󠇯` | U+F0420 U+E0121 U+E01EF | always |
| `i` | `󰐰` | U+F0430 | always |
| `i` | `󰐡` | U+F0421 | at the start of a word |
| `I` | `󰐡󠄩󠇯` | U+F0421 U+E0129 U+E01EF | always |
| `u` | `󰐳` | U+F0433 | always |
| `u` | `󰐢` | U+F0422 | at the start of a word |
| `U` | `󰐢󠄵󠇯` | U+F0422 U+E0135 U+E01EF | always |
| `e` | `󰐱` | U+F0431 | always |
| `e` | `󰐣` | U+F0423 | at the start of a word |
| `E` | `󰐣󠄥󠇯` | U+F0423 U+E0125 U+E01EF | always |
| `o` | `󰐴` | U+F0434 | always |
| `o` | `󰐤` | U+F0424 | at the start of a word |
| `O` | `󰐤󠄯󠇯` | U+F0424 U+E012F U+E01EF | always |
| `ai` | `󰐲` | U+F0432 | always |
| `ai` | `󰐥` | U+F0425 | at the start of a word |
| `Ai` | `󰐥󠄡󠅉󠇯` | U+F0425 U+E0121 U+E0149 U+E01EF | always |
| `au` | `󰐵` | U+F0435 | always |
| `au` | `󰐦` | U+F0426 | at the start of a word |
| `Au` | `󰐦󠄡󠅕󠇯` | U+F0426 U+E0121 U+E0155 U+E01EF | always |
| `0` | `󰑀` | U+F0440 | always |
| `1` | `󰑁` | U+F0441 | always |
| `2` | `󰑂` | U+F0442 | always |
| `3` | `󰑃` | U+F0443 | always |
| `4` | `󰑄` | U+F0444 | always |
| `5` | `󰑅` | U+F0445 | always |
| `6` | `󰑆` | U+F0446 | always |
| `7` | `󰑇` | U+F0447 | always |
| `8` | `󰑈` | U+F0448 | always |
| `9` | `󰑉` | U+F0449 | always |
| `,` | `󰑐` | U+F0450 | always |
| `.` | `󰑑` | U+F0451 | always |
| `?` | `󠄟` | U+E011F | always |
| `!` | `󠄁` | U+E0101 | always |
| `-` | `󠄍` | U+E010D | always |
| `'` | `󰐸` | U+F0438 | always |
| `’` | `󰐸󠅛󠄒󠄐󠄑󠄙󠅝󠇯` | U+F0438 U+E015B U+E0112 U+E0110 U+E0111 U+E0119 U+E015D U+E01EF | always |

## Round trip

Every encoding round-trips exactly: decoding the code points that encoding wrote gives back the roman text, and encoding that gives the same code points. The Code points column shows every character a row writes, including any that is invisible.

This page is written from `encodings/vedyakshara.json` by `tools/encoding_docs.py`.
