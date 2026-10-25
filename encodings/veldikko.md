# veldikko encoding

Veldikko is a right-to-left calligraphy whose letters join along the line, with vowel marks that float above them. This encoding writes a roman spelling in its code points: a letter, then the doubling bar if the consonant is doubled, then each vowel mark followed by its signs of length, pitch and emphasis.

## Fonts

- Veldikko (`veldikko`), written right to left.

## Running it

`encode.py` needs only Python 3.9 or later. From a checkout, or from `node_modules/@heroiclands/fonts`:

```sh
python3 encode.py --encoding veldikko "tanu"
python3 encode.py --encoding veldikko --decode "𞵓𞵰𞵕𞵲"
```

The first command writes `𞵓𞵰𞵕𞵲`, and the second reads it back as `tanu`. `--codepoints` prints the result as `U+XXXX` values, and the text may come from standard input.

From Python:

```python
import encode

text = encode.encode("veldikko", "tanu")
roman = encode.decode("veldikko", text)
```

## Vowels and conditions

A row marked _at the start of a word_ applies at the first character of the text or after whitespace, punctuation or a symbol.

A row marked _at the end of a word_ applies at the last character of the text or before whitespace, punctuation or a symbol.

Where several rows begin with the same roman, the longest wins, and among rows of one length a row whose condition holds comes before a row with none. A row whose condition fails is skipped.

## Rows

Its rows are generated from a small number of parts, so the complete table is too long to read. Every consonant is a single letter; a roman letter the script lacks (`b`, `f`, `w`, `z`, `c`, `q`, `g`) is written as the nearest letter, and `x` is written as two letters. A vowel is its vowel sign, and a vowel at the start of a word is written after the carrier letter. A doubled vowel adds the long sign. The accents circumflex, caron and acute, typed on a vowel or after it, add the rise, fall and emphasis signs. A doubled consonant adds the doubling bar. A capital draws the same letters as its small form and carries a mark that decoding reads back as the capital.

The rows below are the rows of a single character, then a few longer rows of each length.

### Rows of a single character

| Roman | Character | Code points | When |
| --- | --- | --- | --- |
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
| `s` | `𞵔` | U+1ED54 | always |
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
| `g` | `𞵘󠅇󠇯` | U+1ED58 U+E0147 U+E01EF | always |
| `G` | `𞵘󠄧󠇯` | U+1ED58 U+E0127 U+E01EF | always |
| `-` | `󠄍` | U+E010D | at the start of a word |
| `-` | `󠄍` | U+E010D | at the end of a word |
| `-` | ` 󠄍󠇯` | U+0020 U+E010D U+E01EF | always |
| `◌̂` | `𞵹` | U+1ED79 | always |
| `◌̌` | `𞵺` | U+1ED7A | always |
| `◌́` | `𞵻` | U+1ED7B | always |
| `a` | `𞵝𞵰` | U+1ED5D U+1ED70 | at the start of a word |
| `a` | `𞵰` | U+1ED70 | always |
| `â` | `𞵝𞵰𞵹󠅛󠅅󠄒󠅝󠇯` | U+1ED5D U+1ED70 U+1ED79 U+E015B U+E0145 U+E0112 U+E015D U+E01EF | at the start of a word |
| `â` | `𞵰𞵹󠅛󠅅󠄒󠅝󠇯` | U+1ED70 U+1ED79 U+E015B U+E0145 U+E0112 U+E015D U+E01EF | always |
| `ǎ` | `𞵝𞵰𞵺󠅛󠄑󠅃󠅅󠅝󠇯` | U+1ED5D U+1ED70 U+1ED7A U+E015B U+E0111 U+E0143 U+E0145 U+E015D U+E01EF | at the start of a word |
| `ǎ` | `𞵰𞵺󠅛󠄑󠅃󠅅󠅝󠇯` | U+1ED70 U+1ED7A U+E015B U+E0111 U+E0143 U+E0145 U+E015D U+E01EF | always |
| `á` | `𞵝𞵰𞵻󠅛󠅅󠄑󠅝󠇯` | U+1ED5D U+1ED70 U+1ED7B U+E015B U+E0145 U+E0111 U+E015D U+E01EF | at the start of a word |
| `á` | `𞵰𞵻󠅛󠅅󠄑󠅝󠇯` | U+1ED70 U+1ED7B U+E015B U+E0145 U+E0111 U+E015D U+E01EF | always |
| `ấ` | `𞵝𞵰𞵹𞵻󠅛󠄑󠅅󠅁󠄕󠅝󠇯` | U+1ED5D U+1ED70 U+1ED79 U+1ED7B U+E015B U+E0111 U+E0145 U+E0141 U+E0115 U+E015D U+E01EF | at the start of a word |
| `ấ` | `𞵰𞵹𞵻󠅛󠄑󠅅󠅁󠄕󠅝󠇯` | U+1ED70 U+1ED79 U+1ED7B U+E015B U+E0111 U+E0145 U+E0141 U+E0115 U+E015D U+E01EF | always |
| `A` | `𞵝𞵰󠄡󠇯` | U+1ED5D U+1ED70 U+E0121 U+E01EF | at the start of a word |
| `A` | `𞵰󠄡󠇯` | U+1ED70 U+E0121 U+E01EF | always |
| `Â` | `𞵝𞵰𞵹󠅛󠅃󠄒󠅝󠇯` | U+1ED5D U+1ED70 U+1ED79 U+E015B U+E0143 U+E0112 U+E015D U+E01EF | at the start of a word |
| `Â` | `𞵰𞵹󠅛󠅃󠄒󠅝󠇯` | U+1ED70 U+1ED79 U+E015B U+E0143 U+E0112 U+E015D U+E01EF | always |
| `Ǎ` | `𞵝𞵰𞵺󠅛󠄑󠅃󠅄󠅝󠇯` | U+1ED5D U+1ED70 U+1ED7A U+E015B U+E0111 U+E0143 U+E0144 U+E015D U+E01EF | at the start of a word |
| `Ǎ` | `𞵰𞵺󠅛󠄑󠅃󠅄󠅝󠇯` | U+1ED70 U+1ED7A U+E015B U+E0111 U+E0143 U+E0144 U+E015D U+E01EF | always |
| `Á` | `𞵝𞵰𞵻󠅛󠅃󠄑󠅝󠇯` | U+1ED5D U+1ED70 U+1ED7B U+E015B U+E0143 U+E0111 U+E015D U+E01EF | at the start of a word |
| `Á` | `𞵰𞵻󠅛󠅃󠄑󠅝󠇯` | U+1ED70 U+1ED7B U+E015B U+E0143 U+E0111 U+E015D U+E01EF | always |
| `Ấ` | `𞵝𞵰𞵹𞵻󠅛󠄑󠅅󠅁󠄔󠅝󠇯` | U+1ED5D U+1ED70 U+1ED79 U+1ED7B U+E015B U+E0111 U+E0145 U+E0141 U+E0114 U+E015D U+E01EF | at the start of a word |
| `Ấ` | `𞵰𞵹𞵻󠅛󠄑󠅅󠅁󠄔󠅝󠇯` | U+1ED70 U+1ED79 U+1ED7B U+E015B U+E0111 U+E0145 U+E0141 U+E0114 U+E015D U+E01EF | always |
| `e` | `𞵝𞵳` | U+1ED5D U+1ED73 | at the start of a word |
| `e` | `𞵳` | U+1ED73 | always |
| `ê` | `𞵝𞵳𞵹󠅛󠅅󠅁󠅝󠇯` | U+1ED5D U+1ED73 U+1ED79 U+E015B U+E0145 U+E0141 U+E015D U+E01EF | at the start of a word |
| `ê` | `𞵳𞵹󠅛󠅅󠅁󠅝󠇯` | U+1ED73 U+1ED79 U+E015B U+E0145 U+E0141 U+E015D U+E01EF | always |
| `ě` | `𞵝𞵳𞵺󠅛󠄑󠄑󠅂󠅝󠇯` | U+1ED5D U+1ED73 U+1ED7A U+E015B U+E0111 U+E0111 U+E0142 U+E015D U+E01EF | at the start of a word |
| `ě` | `𞵳𞵺󠅛󠄑󠄑󠅂󠅝󠇯` | U+1ED73 U+1ED7A U+E015B U+E0111 U+E0111 U+E0142 U+E015D U+E01EF | always |
| `é` | `𞵝𞵳𞵻󠅛󠅅󠄙󠅝󠇯` | U+1ED5D U+1ED73 U+1ED7B U+E015B U+E0145 U+E0119 U+E015D U+E01EF | at the start of a word |
| `é` | `𞵳𞵻󠅛󠅅󠄙󠅝󠇯` | U+1ED73 U+1ED7B U+E015B U+E0145 U+E0119 U+E015D U+E01EF | always |
| `ế` | `𞵝𞵳𞵹𞵻󠅛󠄑󠅅󠅂󠅆󠅝󠇯` | U+1ED5D U+1ED73 U+1ED79 U+1ED7B U+E015B U+E0111 U+E0145 U+E0142 U+E0146 U+E015D U+E01EF | at the start of a word |
| `ế` | `𞵳𞵹𞵻󠅛󠄑󠅅󠅂󠅆󠅝󠇯` | U+1ED73 U+1ED79 U+1ED7B U+E015B U+E0111 U+E0145 U+E0142 U+E0146 U+E015D U+E01EF | always |
| `E` | `𞵝𞵳󠄥󠇯` | U+1ED5D U+1ED73 U+E0125 U+E01EF | at the start of a word |
| `E` | `𞵳󠄥󠇯` | U+1ED73 U+E0125 U+E01EF | always |
| `Ê` | `𞵝𞵳𞵹󠅛󠅃󠅁󠅝󠇯` | U+1ED5D U+1ED73 U+1ED79 U+E015B U+E0143 U+E0141 U+E015D U+E01EF | at the start of a word |
| `Ê` | `𞵳𞵹󠅛󠅃󠅁󠅝󠇯` | U+1ED73 U+1ED79 U+E015B U+E0143 U+E0141 U+E015D U+E01EF | always |
| `Ě` | `𞵝𞵳𞵺󠅛󠄑󠄑󠅁󠅝󠇯` | U+1ED5D U+1ED73 U+1ED7A U+E015B U+E0111 U+E0111 U+E0141 U+E015D U+E01EF | at the start of a word |
| `Ě` | `𞵳𞵺󠅛󠄑󠄑󠅁󠅝󠇯` | U+1ED73 U+1ED7A U+E015B U+E0111 U+E0111 U+E0141 U+E015D U+E01EF | always |
| `É` | `𞵝𞵳𞵻󠅛󠅃󠄙󠅝󠇯` | U+1ED5D U+1ED73 U+1ED7B U+E015B U+E0143 U+E0119 U+E015D U+E01EF | at the start of a word |
| `É` | `𞵳𞵻󠅛󠅃󠄙󠅝󠇯` | U+1ED73 U+1ED7B U+E015B U+E0143 U+E0119 U+E015D U+E01EF | always |
| `Ế` | `𞵝𞵳𞵹𞵻󠅛󠄑󠅅󠅂󠅅󠅝󠇯` | U+1ED5D U+1ED73 U+1ED79 U+1ED7B U+E015B U+E0111 U+E0145 U+E0142 U+E0145 U+E015D U+E01EF | at the start of a word |
| `Ế` | `𞵳𞵹𞵻󠅛󠄑󠅅󠅂󠅅󠅝󠇯` | U+1ED73 U+1ED79 U+1ED7B U+E015B U+E0111 U+E0145 U+E0142 U+E0145 U+E015D U+E01EF | always |
| `i` | `𞵝𞵴` | U+1ED5D U+1ED74 | at the start of a word |
| `i` | `𞵴` | U+1ED74 | always |
| `î` | `𞵝𞵴𞵹󠅛󠅅󠅅󠅝󠇯` | U+1ED5D U+1ED74 U+1ED79 U+E015B U+E0145 U+E0145 U+E015D U+E01EF | at the start of a word |
| `î` | `𞵴𞵹󠅛󠅅󠅅󠅝󠇯` | U+1ED74 U+1ED79 U+E015B U+E0145 U+E0145 U+E015D U+E01EF | always |
| `ǐ` | `𞵝𞵴𞵺󠅛󠄑󠅄󠄐󠅝󠇯` | U+1ED5D U+1ED74 U+1ED7A U+E015B U+E0111 U+E0144 U+E0110 U+E015D U+E01EF | at the start of a word |
| `ǐ` | `𞵴𞵺󠅛󠄑󠅄󠄐󠅝󠇯` | U+1ED74 U+1ED7A U+E015B U+E0111 U+E0144 U+E0110 U+E015D U+E01EF | always |
| `í` | `𞵝𞵴𞵻󠅛󠅅󠅄󠅝󠇯` | U+1ED5D U+1ED74 U+1ED7B U+E015B U+E0145 U+E0144 U+E015D U+E01EF | at the start of a word |
| `í` | `𞵴𞵻󠅛󠅅󠅄󠅝󠇯` | U+1ED74 U+1ED7B U+E015B U+E0145 U+E0144 U+E015D U+E01EF | always |
| `I` | `𞵝𞵴󠄩󠇯` | U+1ED5D U+1ED74 U+E0129 U+E01EF | at the start of a word |
| `I` | `𞵴󠄩󠇯` | U+1ED74 U+E0129 U+E01EF | always |
| `Î` | `𞵝𞵴𞵹󠅛󠅃󠅅󠅝󠇯` | U+1ED5D U+1ED74 U+1ED79 U+E015B U+E0143 U+E0145 U+E015D U+E01EF | at the start of a word |
| `Î` | `𞵴𞵹󠅛󠅃󠅅󠅝󠇯` | U+1ED74 U+1ED79 U+E015B U+E0143 U+E0145 U+E015D U+E01EF | always |
| `Ǐ` | `𞵝𞵴𞵺󠅛󠄑󠅃󠅆󠅝󠇯` | U+1ED5D U+1ED74 U+1ED7A U+E015B U+E0111 U+E0143 U+E0146 U+E015D U+E01EF | at the start of a word |
| `Ǐ` | `𞵴𞵺󠅛󠄑󠅃󠅆󠅝󠇯` | U+1ED74 U+1ED7A U+E015B U+E0111 U+E0143 U+E0146 U+E015D U+E01EF | always |
| `Í` | `𞵝𞵴𞵻󠅛󠅃󠅄󠅝󠇯` | U+1ED5D U+1ED74 U+1ED7B U+E015B U+E0143 U+E0144 U+E015D U+E01EF | at the start of a word |
| `Í` | `𞵴𞵻󠅛󠅃󠅄󠅝󠇯` | U+1ED74 U+1ED7B U+E015B U+E0143 U+E0144 U+E015D U+E01EF | always |
| `o` | `𞵝𞵱` | U+1ED5D U+1ED71 | at the start of a word |
| `o` | `𞵱` | U+1ED71 | always |
| `ô` | `𞵝𞵱𞵹󠅛󠅆󠄔󠅝󠇯` | U+1ED5D U+1ED71 U+1ED79 U+E015B U+E0146 U+E0114 U+E015D U+E01EF | at the start of a word |
| `ô` | `𞵱𞵹󠅛󠅆󠄔󠅝󠇯` | U+1ED71 U+1ED79 U+E015B U+E0146 U+E0114 U+E015D U+E01EF | always |
| `ǒ` | `𞵝𞵱𞵺󠅛󠄑󠅄󠄒󠅝󠇯` | U+1ED5D U+1ED71 U+1ED7A U+E015B U+E0111 U+E0144 U+E0112 U+E015D U+E01EF | at the start of a word |
| `ǒ` | `𞵱𞵺󠅛󠄑󠅄󠄒󠅝󠇯` | U+1ED71 U+1ED7A U+E015B U+E0111 U+E0144 U+E0112 U+E015D U+E01EF | always |
| `ó` | `𞵝𞵱𞵻󠅛󠅆󠄓󠅝󠇯` | U+1ED5D U+1ED71 U+1ED7B U+E015B U+E0146 U+E0113 U+E015D U+E01EF | at the start of a word |
| `ó` | `𞵱𞵻󠅛󠅆󠄓󠅝󠇯` | U+1ED71 U+1ED7B U+E015B U+E0146 U+E0113 U+E015D U+E01EF | always |
| `ố` | `𞵝𞵱𞵹𞵻󠅛󠄑󠅅󠅄󠄑󠅝󠇯` | U+1ED5D U+1ED71 U+1ED79 U+1ED7B U+E015B U+E0111 U+E0145 U+E0144 U+E0111 U+E015D U+E01EF | at the start of a word |
| `ố` | `𞵱𞵹𞵻󠅛󠄑󠅅󠅄󠄑󠅝󠇯` | U+1ED71 U+1ED79 U+1ED7B U+E015B U+E0111 U+E0145 U+E0144 U+E0111 U+E015D U+E01EF | always |
| `O` | `𞵝𞵱󠄯󠇯` | U+1ED5D U+1ED71 U+E012F U+E01EF | at the start of a word |
| `O` | `𞵱󠄯󠇯` | U+1ED71 U+E012F U+E01EF | always |
| `Ô` | `𞵝𞵱𞵹󠅛󠅄󠄔󠅝󠇯` | U+1ED5D U+1ED71 U+1ED79 U+E015B U+E0144 U+E0114 U+E015D U+E01EF | at the start of a word |
| `Ô` | `𞵱𞵹󠅛󠅄󠄔󠅝󠇯` | U+1ED71 U+1ED79 U+E015B U+E0144 U+E0114 U+E015D U+E01EF | always |
| `Ǒ` | `𞵝𞵱𞵺󠅛󠄑󠅄󠄑󠅝󠇯` | U+1ED5D U+1ED71 U+1ED7A U+E015B U+E0111 U+E0144 U+E0111 U+E015D U+E01EF | at the start of a word |
| `Ǒ` | `𞵱𞵺󠅛󠄑󠅄󠄑󠅝󠇯` | U+1ED71 U+1ED7A U+E015B U+E0111 U+E0144 U+E0111 U+E015D U+E01EF | always |
| `Ó` | `𞵝𞵱𞵻󠅛󠅄󠄓󠅝󠇯` | U+1ED5D U+1ED71 U+1ED7B U+E015B U+E0144 U+E0113 U+E015D U+E01EF | at the start of a word |
| `Ó` | `𞵱𞵻󠅛󠅄󠄓󠅝󠇯` | U+1ED71 U+1ED7B U+E015B U+E0144 U+E0113 U+E015D U+E01EF | always |
| `Ố` | `𞵝𞵱𞵹𞵻󠅛󠄑󠅅󠅄󠄐󠅝󠇯` | U+1ED5D U+1ED71 U+1ED79 U+1ED7B U+E015B U+E0111 U+E0145 U+E0144 U+E0110 U+E015D U+E01EF | at the start of a word |
| `Ố` | `𞵱𞵹𞵻󠅛󠄑󠅅󠅄󠄐󠅝󠇯` | U+1ED71 U+1ED79 U+1ED7B U+E015B U+E0111 U+E0145 U+E0144 U+E0110 U+E015D U+E01EF | always |
| `u` | `𞵝𞵲` | U+1ED5D U+1ED72 | at the start of a word |
| `u` | `𞵲` | U+1ED72 | always |
| `û` | `𞵝𞵲𞵹󠅛󠅆󠅂󠅝󠇯` | U+1ED5D U+1ED72 U+1ED79 U+E015B U+E0146 U+E0142 U+E015D U+E01EF | at the start of a word |
| `û` | `𞵲𞵹󠅛󠅆󠅂󠅝󠇯` | U+1ED72 U+1ED79 U+E015B U+E0146 U+E0142 U+E015D U+E01EF | always |
| `ǔ` | `𞵝𞵲𞵺󠅛󠄑󠅄󠄔󠅝󠇯` | U+1ED5D U+1ED72 U+1ED7A U+E015B U+E0111 U+E0144 U+E0114 U+E015D U+E01EF | at the start of a word |
| `ǔ` | `𞵲𞵺󠅛󠄑󠅄󠄔󠅝󠇯` | U+1ED72 U+1ED7A U+E015B U+E0111 U+E0144 U+E0114 U+E015D U+E01EF | always |
| `ú` | `𞵝𞵲𞵻󠅛󠅆󠅁󠅝󠇯` | U+1ED5D U+1ED72 U+1ED7B U+E015B U+E0146 U+E0141 U+E015D U+E01EF | at the start of a word |
| `ú` | `𞵲𞵻󠅛󠅆󠅁󠅝󠇯` | U+1ED72 U+1ED7B U+E015B U+E0146 U+E0141 U+E015D U+E01EF | always |
| `U` | `𞵝𞵲󠄵󠇯` | U+1ED5D U+1ED72 U+E0135 U+E01EF | at the start of a word |
| `U` | `𞵲󠄵󠇯` | U+1ED72 U+E0135 U+E01EF | always |
| `Û` | `𞵝𞵲𞵹󠅛󠅄󠅂󠅝󠇯` | U+1ED5D U+1ED72 U+1ED79 U+E015B U+E0144 U+E0142 U+E015D U+E01EF | at the start of a word |
| `Û` | `𞵲𞵹󠅛󠅄󠅂󠅝󠇯` | U+1ED72 U+1ED79 U+E015B U+E0144 U+E0142 U+E015D U+E01EF | always |
| `Ǔ` | `𞵝𞵲𞵺󠅛󠄑󠅄󠄓󠅝󠇯` | U+1ED5D U+1ED72 U+1ED7A U+E015B U+E0111 U+E0144 U+E0113 U+E015D U+E01EF | at the start of a word |
| `Ǔ` | `𞵲𞵺󠅛󠄑󠅄󠄓󠅝󠇯` | U+1ED72 U+1ED7A U+E015B U+E0111 U+E0144 U+E0113 U+E015D U+E01EF | always |
| `Ú` | `𞵝𞵲𞵻󠅛󠅄󠅁󠅝󠇯` | U+1ED5D U+1ED72 U+1ED7B U+E015B U+E0144 U+E0141 U+E015D U+E01EF | at the start of a word |
| `Ú` | `𞵲𞵻󠅛󠅄󠅁󠅝󠇯` | U+1ED72 U+1ED7B U+E015B U+E0144 U+E0141 U+E015D U+E01EF | always |
| `y` | `𞵝𞵵` | U+1ED5D U+1ED75 | at the start of a word |
| `y` | `𞵵` | U+1ED75 | always |
| `ŷ` | `𞵝𞵵𞵹󠅛󠄑󠄗󠄗󠅝󠇯` | U+1ED5D U+1ED75 U+1ED79 U+E015B U+E0111 U+E0117 U+E0117 U+E015D U+E01EF | at the start of a word |
| `ŷ` | `𞵵𞵹󠅛󠄑󠄗󠄗󠅝󠇯` | U+1ED75 U+1ED79 U+E015B U+E0111 U+E0117 U+E0117 U+E015D U+E01EF | always |
| `ý` | `𞵝𞵵𞵻󠅛󠅆󠅄󠅝󠇯` | U+1ED5D U+1ED75 U+1ED7B U+E015B U+E0146 U+E0144 U+E015D U+E01EF | at the start of a word |
| `ý` | `𞵵𞵻󠅛󠅆󠅄󠅝󠇯` | U+1ED75 U+1ED7B U+E015B U+E0146 U+E0144 U+E015D U+E01EF | always |
| `Y` | `𞵝𞵵󠄹󠇯` | U+1ED5D U+1ED75 U+E0139 U+E01EF | at the start of a word |
| `Y` | `𞵵󠄹󠇯` | U+1ED75 U+E0139 U+E01EF | always |
| `Ŷ` | `𞵝𞵵𞵹󠅛󠄑󠄗󠄖󠅝󠇯` | U+1ED5D U+1ED75 U+1ED79 U+E015B U+E0111 U+E0117 U+E0116 U+E015D U+E01EF | at the start of a word |
| `Ŷ` | `𞵵𞵹󠅛󠄑󠄗󠄖󠅝󠇯` | U+1ED75 U+1ED79 U+E015B U+E0111 U+E0117 U+E0116 U+E015D U+E01EF | always |
| `Ý` | `𞵝𞵵𞵻󠅛󠅄󠅄󠅝󠇯` | U+1ED5D U+1ED75 U+1ED7B U+E015B U+E0144 U+E0144 U+E015D U+E01EF | at the start of a word |
| `Ý` | `𞵵𞵻󠅛󠅄󠅄󠅝󠇯` | U+1ED75 U+1ED7B U+E015B U+E0144 U+E0144 U+E015D U+E01EF | always |
| `ë` | `𞵝𞵶` | U+1ED5D U+1ED76 | at the start of a word |
| `ë` | `𞵶` | U+1ED76 | always |
| `Ë` | `𞵝𞵶󠅛󠅃󠅂󠅝󠇯` | U+1ED5D U+1ED76 U+E015B U+E0143 U+E0142 U+E015D U+E01EF | at the start of a word |
| `Ë` | `𞵶󠅛󠅃󠅂󠅝󠇯` | U+1ED76 U+E015B U+E0143 U+E0142 U+E015D U+E01EF | always |
| `j` | `𞵝𞵵󠅊󠇯` | U+1ED5D U+1ED75 U+E014A U+E01EF | at the start of a word |
| `j` | `𞵵󠅊󠇯` | U+1ED75 U+E014A U+E01EF | always |
| `J` | `𞵝𞵵󠄪󠇯` | U+1ED5D U+1ED75 U+E012A U+E01EF | at the start of a word |
| `J` | `𞵵󠄪󠇯` | U+1ED75 U+E012A U+E01EF | always |

### Longer rows

A few rows of each length show the pattern; every longer row is built in the same way.

| Roman | Character | Code points | When |
| --- | --- | --- | --- |
| `ng` | `𞵚` | U+1ED5A | always |
| `nG` | `𞵚󠅎󠄧󠇯` | U+1ED5A U+E014E U+E0127 U+E01EF | always |
| `Ng` | `𞵚󠄮󠅇󠇯` | U+1ED5A U+E012E U+E0147 U+E01EF | always |
| `ấ` | `𞵝𞵰𞵹𞵻󠅁󠅛󠄓󠄐󠄒󠅝󠅛󠄓󠄐󠄑󠅝󠇯` | U+1ED5D U+1ED70 U+1ED79 U+1ED7B U+E0141 U+E015B U+E0113 U+E0110 U+E0112 U+E015D U+E015B U+E0113 U+E0110 U+E0111 U+E015D U+E01EF | at the start of a word |
| `ấ` | `𞵰𞵹𞵻󠅁󠅛󠄓󠄐󠄒󠅝󠅛󠄓󠄐󠄑󠅝󠇯` | U+1ED70 U+1ED79 U+1ED7B U+E0141 U+E015B U+E0113 U+E0110 U+E0112 U+E015D U+E015B U+E0113 U+E0110 U+E0111 U+E015D U+E01EF | always |
| `ǎ́` | `𞵝𞵰𞵺𞵻󠅁󠅛󠄓󠄐󠅃󠅝󠅛󠄓󠄐󠄑󠅝󠇯` | U+1ED5D U+1ED70 U+1ED7A U+1ED7B U+E0141 U+E015B U+E0113 U+E0110 U+E0143 U+E015D U+E015B U+E0113 U+E0110 U+E0111 U+E015D U+E01EF | at the start of a word |
| `ngng` | `𞵚𞵼` | U+1ED5A U+1ED7C | always |
| `ngnG` | `𞵚𞵼󠅎󠅇󠅎󠄧󠇯` | U+1ED5A U+1ED7C U+E014E U+E0147 U+E014E U+E0127 U+E01EF | always |
| `ngNg` | `𞵚𞵼󠅎󠅇󠄮󠅇󠇯` | U+1ED5A U+1ED7C U+E014E U+E0147 U+E012E U+E0147 U+E01EF | always |
| `aë̂́` | `𞵝𞵰𞵝𞵶𞵹𞵻󠅁󠅅󠅛󠄓󠄐󠄘󠅝󠅛󠄓󠄐󠄒󠅝󠅛󠄓󠄐󠄑󠅝󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED76 U+1ED79 U+1ED7B U+E0141 U+E0145 U+E015B U+E0113 U+E0110 U+E0118 U+E015D U+E015B U+E0113 U+E0110 U+E0112 U+E015D U+E015B U+E0113 U+E0110 U+E0111 U+E015D U+E01EF | at the start of a word |
| `aë̂́` | `𞵰𞵝𞵶𞵹𞵻󠅁󠅅󠅛󠄓󠄐󠄘󠅝󠅛󠄓󠄐󠄒󠅝󠅛󠄓󠄐󠄑󠅝󠇯` | U+1ED70 U+1ED5D U+1ED76 U+1ED79 U+1ED7B U+E0141 U+E0145 U+E015B U+E0113 U+E0110 U+E0118 U+E015D U+E015B U+E0113 U+E0110 U+E0112 U+E015D U+E015B U+E0113 U+E0110 U+E0111 U+E015D U+E01EF | always |
| `aë̌́` | `𞵝𞵰𞵝𞵶𞵺𞵻󠅁󠅅󠅛󠄓󠄐󠄘󠅝󠅛󠄓󠄐󠅃󠅝󠅛󠄓󠄐󠄑󠅝󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED76 U+1ED7A U+1ED7B U+E0141 U+E0145 U+E015B U+E0113 U+E0110 U+E0118 U+E015D U+E015B U+E0113 U+E0110 U+E0143 U+E015D U+E015B U+E0113 U+E0110 U+E0111 U+E015D U+E01EF | at the start of a word |
| `ëë̂́` | `𞵝𞵶𞵸𞵹𞵻󠅅󠅛󠄓󠄐󠄘󠅝󠅅󠅛󠄓󠄐󠄘󠅝󠅛󠄓󠄐󠄒󠅝󠅛󠄓󠄐󠄑󠅝󠇯` | U+1ED5D U+1ED76 U+1ED78 U+1ED79 U+1ED7B U+E0145 U+E015B U+E0113 U+E0110 U+E0118 U+E015D U+E0145 U+E015B U+E0113 U+E0110 U+E0118 U+E015D U+E015B U+E0113 U+E0110 U+E0112 U+E015D U+E015B U+E0113 U+E0110 U+E0111 U+E015D U+E01EF | at the start of a word |
| `ëë̂́` | `𞵶𞵸𞵹𞵻󠅅󠅛󠄓󠄐󠄘󠅝󠅅󠅛󠄓󠄐󠄘󠅝󠅛󠄓󠄐󠄒󠅝󠅛󠄓󠄐󠄑󠅝󠇯` | U+1ED76 U+1ED78 U+1ED79 U+1ED7B U+E0145 U+E015B U+E0113 U+E0110 U+E0118 U+E015D U+E0145 U+E015B U+E0113 U+E0110 U+E0118 U+E015D U+E015B U+E0113 U+E0110 U+E0112 U+E015D U+E015B U+E0113 U+E0110 U+E0111 U+E015D U+E01EF | always |
| `ëë̌́` | `𞵝𞵶𞵸𞵺𞵻󠅅󠅛󠄓󠄐󠄘󠅝󠅅󠅛󠄓󠄐󠄘󠅝󠅛󠄓󠄐󠅃󠅝󠅛󠄓󠄐󠄑󠅝󠇯` | U+1ED5D U+1ED76 U+1ED78 U+1ED7A U+1ED7B U+E0145 U+E015B U+E0113 U+E0110 U+E0118 U+E015D U+E0145 U+E015B U+E0113 U+E0110 U+E0118 U+E015D U+E015B U+E0113 U+E0110 U+E0143 U+E015D U+E015B U+E0113 U+E0110 U+E0111 U+E015D U+E01EF | at the start of a word |

## Round trip

Every encoding round-trips exactly: decoding the code points that encoding wrote gives back the roman text, and encoding that gives the same code points. The Code points column shows every character a row writes, including any that is invisible.

This page is written from `encodings/veldikko.json` by `tools/encoding_docs.py`.
