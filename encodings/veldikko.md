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

## Accepted characters

This encoding accepts `a-z`, `-`, `á`, `â`, `é`, `ê`, `ë`, `í`, `î`, `ó`, `ô`, `ú`, `û`, `ý`, `ě`, `ŷ`, `ǎ`, `ǐ`, `ǒ`, `ǔ`, `◌́`, `◌̂`, `◌̈`, `◌̌`, `ấ`, `ế`, `ố`, (space), `!`, `,`, `.`, `/`, `?`, `^`, `{`, `}`, `«`, `»`, `—`, `…`, `‹`, `›`, `‼`, and the standard's marks and whitespace. Any other character is refused at its line and column.

## Punctuation

This encoding includes the [standard roman punctuation](standard.md), which every language's roman shares. The table shows how this script writes each standard mark. A mark the script draws writes its glyph; a mark it does not draw writes the standard's invisible mark, the same in every encoding, so decoding restores it.

| Mark | Meaning | Written | Code points |
| --- | --- | --- | --- |
| `.` | completes a declarative sentence, terminal | invisible | U+E0100 |
| `?` | completes an interrogative sentence, terminal | invisible | U+E0101 |
| `‼` | completes an imperative sentence, terminal | invisible | U+E0102 |
| `!` | completes an exclamative sentence, terminal | invisible | U+E0103 |
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

A row marked _at the start of a word_ applies at the first character of the text or after whitespace, punctuation or a symbol.

A row marked _at the end of a word_ applies at the last character of the text or before whitespace, punctuation or a symbol.

Where several rows begin with the same roman, the longest wins, and among rows of one length a row whose condition holds comes before a row with none. A row whose condition fails is skipped.

## Rows

Its rows are generated from a small number of parts, so the complete table is too long to read. Every consonant is a single letter; a roman letter the script lacks (`b`, `f`, `w`, `z`, `c`, `q`, `g`) is written as the nearest letter, and `x` is written as two letters. A vowel is its vowel sign, and a vowel at the start of a word is written after the carrier letter. A doubled vowel adds the long sign. The accents circumflex, caron and acute, typed on a vowel or after it, add the rise, fall and emphasis signs. A doubled consonant adds the doubling bar.

The rows below are the rows of a single character, then a few longer rows of each length.

### Rows of a single character

| Roman | Character | Code points | When |
| --- | --- | --- | --- |
| `.` | `󠄀` | U+E0100 | always |
| `?` | `󠄁` | U+E0101 | always |
| `‼` | `󠄂` | U+E0102 | always |
| `!` | `󠄃` | U+E0103 | always |
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
| `x` | `𞵘𞵔󠅘󠇯` | U+1ED58 U+1ED54 U+E0158 U+E01EF | always |
| `p` | `𞵐` | U+1ED50 | always |
| `v` | `𞵑` | U+1ED51 | always |
| `m` | `𞵒` | U+1ED52 | always |
| `t` | `𞵓` | U+1ED53 | always |
| `s` | `𞵔` | U+1ED54 | always |
| `n` | `𞵕` | U+1ED55 | always |
| `d` | `𞵖` | U+1ED56 | always |
| `k` | `𞵘󠅋󠇯` | U+1ED58 U+E014B U+E01EF | always |
| `h` | `𞵙` | U+1ED59 | always |
| `l` | `𞵛` | U+1ED5B | always |
| `r` | `𞵜` | U+1ED5C | always |
| `b` | `𞵐󠅂󠇯` | U+1ED50 U+E0142 U+E01EF | always |
| `f` | `𞵑󠅆󠇯` | U+1ED51 U+E0146 U+E01EF | always |
| `w` | `𞵑󠅗󠇯` | U+1ED51 U+E0157 U+E01EF | always |
| `z` | `𞵔󠅚󠇯` | U+1ED54 U+E015A U+E01EF | always |
| `c` | `𞵘󠅃󠇯` | U+1ED58 U+E0143 U+E01EF | always |
| `q` | `𞵘󠅑󠇯` | U+1ED58 U+E0151 U+E01EF | always |
| `g` | `𞵘󠅇󠇯` | U+1ED58 U+E0147 U+E01EF | always |
| `-` | `󠅛󠄒󠅄󠅝` | U+E015B U+E0112 U+E0144 U+E015D | at the start of a word |
| `-` | `󠅛󠄒󠅄󠅝` | U+E015B U+E0112 U+E0144 U+E015D | at the end of a word |
| `-` | ` 󠅛󠄒󠅄󠅝󠇯` | U+0020 U+E015B U+E0112 U+E0144 U+E015D U+E01EF | always |
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
| `i` | `𞵝𞵴` | U+1ED5D U+1ED74 | at the start of a word |
| `i` | `𞵴` | U+1ED74 | always |
| `î` | `𞵝𞵴𞵹󠅛󠅅󠅅󠅝󠇯` | U+1ED5D U+1ED74 U+1ED79 U+E015B U+E0145 U+E0145 U+E015D U+E01EF | at the start of a word |
| `î` | `𞵴𞵹󠅛󠅅󠅅󠅝󠇯` | U+1ED74 U+1ED79 U+E015B U+E0145 U+E0145 U+E015D U+E01EF | always |
| `ǐ` | `𞵝𞵴𞵺󠅛󠄑󠅄󠄐󠅝󠇯` | U+1ED5D U+1ED74 U+1ED7A U+E015B U+E0111 U+E0144 U+E0110 U+E015D U+E01EF | at the start of a word |
| `ǐ` | `𞵴𞵺󠅛󠄑󠅄󠄐󠅝󠇯` | U+1ED74 U+1ED7A U+E015B U+E0111 U+E0144 U+E0110 U+E015D U+E01EF | always |
| `í` | `𞵝𞵴𞵻󠅛󠅅󠅄󠅝󠇯` | U+1ED5D U+1ED74 U+1ED7B U+E015B U+E0145 U+E0144 U+E015D U+E01EF | at the start of a word |
| `í` | `𞵴𞵻󠅛󠅅󠅄󠅝󠇯` | U+1ED74 U+1ED7B U+E015B U+E0145 U+E0144 U+E015D U+E01EF | always |
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
| `u` | `𞵝𞵲` | U+1ED5D U+1ED72 | at the start of a word |
| `u` | `𞵲` | U+1ED72 | always |
| `û` | `𞵝𞵲𞵹󠅛󠅆󠅂󠅝󠇯` | U+1ED5D U+1ED72 U+1ED79 U+E015B U+E0146 U+E0142 U+E015D U+E01EF | at the start of a word |
| `û` | `𞵲𞵹󠅛󠅆󠅂󠅝󠇯` | U+1ED72 U+1ED79 U+E015B U+E0146 U+E0142 U+E015D U+E01EF | always |
| `ǔ` | `𞵝𞵲𞵺󠅛󠄑󠅄󠄔󠅝󠇯` | U+1ED5D U+1ED72 U+1ED7A U+E015B U+E0111 U+E0144 U+E0114 U+E015D U+E01EF | at the start of a word |
| `ǔ` | `𞵲𞵺󠅛󠄑󠅄󠄔󠅝󠇯` | U+1ED72 U+1ED7A U+E015B U+E0111 U+E0144 U+E0114 U+E015D U+E01EF | always |
| `ú` | `𞵝𞵲𞵻󠅛󠅆󠅁󠅝󠇯` | U+1ED5D U+1ED72 U+1ED7B U+E015B U+E0146 U+E0141 U+E015D U+E01EF | at the start of a word |
| `ú` | `𞵲𞵻󠅛󠅆󠅁󠅝󠇯` | U+1ED72 U+1ED7B U+E015B U+E0146 U+E0141 U+E015D U+E01EF | always |
| `y` | `𞵝𞵵` | U+1ED5D U+1ED75 | at the start of a word |
| `y` | `𞵵` | U+1ED75 | always |
| `ŷ` | `𞵝𞵵𞵹󠅛󠄑󠄗󠄗󠅝󠇯` | U+1ED5D U+1ED75 U+1ED79 U+E015B U+E0111 U+E0117 U+E0117 U+E015D U+E01EF | at the start of a word |
| `ŷ` | `𞵵𞵹󠅛󠄑󠄗󠄗󠅝󠇯` | U+1ED75 U+1ED79 U+E015B U+E0111 U+E0117 U+E0117 U+E015D U+E01EF | always |
| `ý` | `𞵝𞵵𞵻󠅛󠅆󠅄󠅝󠇯` | U+1ED5D U+1ED75 U+1ED7B U+E015B U+E0146 U+E0144 U+E015D U+E01EF | at the start of a word |
| `ý` | `𞵵𞵻󠅛󠅆󠅄󠅝󠇯` | U+1ED75 U+1ED7B U+E015B U+E0146 U+E0144 U+E015D U+E01EF | always |
| `ë` | `𞵝𞵶` | U+1ED5D U+1ED76 | at the start of a word |
| `ë` | `𞵶` | U+1ED76 | always |
| `j` | `𞵝𞵵󠅊󠇯` | U+1ED5D U+1ED75 U+E014A U+E01EF | at the start of a word |
| `j` | `𞵵󠅊󠇯` | U+1ED75 U+E014A U+E01EF | always |
| (space) | (space) | U+0020 | always |

### Longer rows

A few rows of each length show the pattern; every longer row is built in the same way.

| Roman | Character | Code points | When |
| --- | --- | --- | --- |
| `ng` | `𞵚` | U+1ED5A | always |
| `dh` | `𞵗` | U+1ED57 | always |
| `nk` | `𞵚𞵘󠅎󠅋󠇯` | U+1ED5A U+1ED58 U+E014E U+E014B U+E01EF | always |
| `ấ` | `𞵝𞵰𞵹𞵻󠅁󠅛󠄓󠄐󠄒󠅝󠅛󠄓󠄐󠄑󠅝󠇯` | U+1ED5D U+1ED70 U+1ED79 U+1ED7B U+E0141 U+E015B U+E0113 U+E0110 U+E0112 U+E015D U+E015B U+E0113 U+E0110 U+E0111 U+E015D U+E01EF | at the start of a word |
| `ấ` | `𞵰𞵹𞵻󠅁󠅛󠄓󠄐󠄒󠅝󠅛󠄓󠄐󠄑󠅝󠇯` | U+1ED70 U+1ED79 U+1ED7B U+E0141 U+E015B U+E0113 U+E0110 U+E0112 U+E015D U+E015B U+E0113 U+E0110 U+E0111 U+E015D U+E01EF | always |
| `ǎ́` | `𞵝𞵰𞵺𞵻󠅁󠅛󠄓󠄐󠅃󠅝󠅛󠄓󠄐󠄑󠅝󠇯` | U+1ED5D U+1ED70 U+1ED7A U+1ED7B U+E0141 U+E015B U+E0113 U+E0110 U+E0143 U+E015D U+E015B U+E0113 U+E0110 U+E0111 U+E015D U+E01EF | at the start of a word |
| `ngng` | `𞵚𞵼` | U+1ED5A U+1ED7C | always |
| `dhdh` | `𞵗𞵼` | U+1ED57 U+1ED7C | always |
| `ë̂́` | `𞵝𞵶𞵹𞵻󠅅󠅛󠄓󠄐󠄘󠅝󠅛󠄓󠄐󠄒󠅝󠅛󠄓󠄐󠄑󠅝󠇯` | U+1ED5D U+1ED76 U+1ED79 U+1ED7B U+E0145 U+E015B U+E0113 U+E0110 U+E0118 U+E015D U+E015B U+E0113 U+E0110 U+E0112 U+E015D U+E015B U+E0113 U+E0110 U+E0111 U+E015D U+E01EF | at the start of a word |
| `aë̂́` | `𞵝𞵰𞵝𞵶𞵹𞵻󠅁󠅅󠅛󠄓󠄐󠄘󠅝󠅛󠄓󠄐󠄒󠅝󠅛󠄓󠄐󠄑󠅝󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED76 U+1ED79 U+1ED7B U+E0141 U+E0145 U+E015B U+E0113 U+E0110 U+E0118 U+E015D U+E015B U+E0113 U+E0110 U+E0112 U+E015D U+E015B U+E0113 U+E0110 U+E0111 U+E015D U+E01EF | at the start of a word |
| `aë̂́` | `𞵰𞵝𞵶𞵹𞵻󠅁󠅅󠅛󠄓󠄐󠄘󠅝󠅛󠄓󠄐󠄒󠅝󠅛󠄓󠄐󠄑󠅝󠇯` | U+1ED70 U+1ED5D U+1ED76 U+1ED79 U+1ED7B U+E0141 U+E0145 U+E015B U+E0113 U+E0110 U+E0118 U+E015D U+E015B U+E0113 U+E0110 U+E0112 U+E015D U+E015B U+E0113 U+E0110 U+E0111 U+E015D U+E01EF | always |
| `aë̌́` | `𞵝𞵰𞵝𞵶𞵺𞵻󠅁󠅅󠅛󠄓󠄐󠄘󠅝󠅛󠄓󠄐󠅃󠅝󠅛󠄓󠄐󠄑󠅝󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED76 U+1ED7A U+1ED7B U+E0141 U+E0145 U+E015B U+E0113 U+E0110 U+E0118 U+E015D U+E015B U+E0113 U+E0110 U+E0143 U+E015D U+E015B U+E0113 U+E0110 U+E0111 U+E015D U+E01EF | at the start of a word |
| `ëë̂́` | `𞵝𞵶𞵸𞵹𞵻󠅅󠅛󠄓󠄐󠄘󠅝󠅅󠅛󠄓󠄐󠄘󠅝󠅛󠄓󠄐󠄒󠅝󠅛󠄓󠄐󠄑󠅝󠇯` | U+1ED5D U+1ED76 U+1ED78 U+1ED79 U+1ED7B U+E0145 U+E015B U+E0113 U+E0110 U+E0118 U+E015D U+E0145 U+E015B U+E0113 U+E0110 U+E0118 U+E015D U+E015B U+E0113 U+E0110 U+E0112 U+E015D U+E015B U+E0113 U+E0110 U+E0111 U+E015D U+E01EF | at the start of a word |
| `ëë̂́` | `𞵶𞵸𞵹𞵻󠅅󠅛󠄓󠄐󠄘󠅝󠅅󠅛󠄓󠄐󠄘󠅝󠅛󠄓󠄐󠄒󠅝󠅛󠄓󠄐󠄑󠅝󠇯` | U+1ED76 U+1ED78 U+1ED79 U+1ED7B U+E0145 U+E015B U+E0113 U+E0110 U+E0118 U+E015D U+E0145 U+E015B U+E0113 U+E0110 U+E0118 U+E015D U+E015B U+E0113 U+E0110 U+E0112 U+E015D U+E015B U+E0113 U+E0110 U+E0111 U+E015D U+E01EF | always |
| `ëë̌́` | `𞵝𞵶𞵸𞵺𞵻󠅅󠅛󠄓󠄐󠄘󠅝󠅅󠅛󠄓󠄐󠄘󠅝󠅛󠄓󠄐󠅃󠅝󠅛󠄓󠄐󠄑󠅝󠇯` | U+1ED5D U+1ED76 U+1ED78 U+1ED7A U+1ED7B U+E0145 U+E015B U+E0113 U+E0110 U+E0118 U+E015D U+E0145 U+E015B U+E0113 U+E0110 U+E0118 U+E015D U+E015B U+E0113 U+E0110 U+E0143 U+E015D U+E015B U+E0113 U+E0110 U+E0111 U+E015D U+E01EF | at the start of a word |

## Round trip

Every encoding round-trips exactly: decoding the code points that encoding wrote gives back the roman text, and encoding that gives the same code points. The Code points column shows every character a row writes, including any that is invisible.

This page is written from `encodings/veldikko.json` by `tools/encoding_docs.py`.
