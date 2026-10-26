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

## Accepted characters

This encoding accepts `a-z`, `-`, `á`, `é`, `ë`, `í`, `ó`, `ú`, `ý`, and the standard's marks and whitespace. Any other character is refused at its line and column.

## Punctuation

This encoding extends the [standard roman encoding](standard.md), which every language's roman shares. The table shows how this script writes each standard mark. A mark the script draws writes its glyph; a mark it does not draw writes the standard's invisible mark, the same in every encoding, so decoding restores it.

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

`⟦` and `⟧` enclose character names, as the [standard](standard.md) describes: `⟦LATIN_SMALL_LETTER_A_WITH_ACUTE⟧` writes `á`. Whitespace between names only separates them.

## Vowels and conditions

A row marked _at the start of a word_ applies at the first character of the text or after whitespace, punctuation or a symbol.

A row marked _at the end of a word_ applies at the last character of the text or before whitespace, punctuation or a symbol.

Where several rows begin with the same roman, the longest wins, and among rows of one length a row whose condition holds comes before a row with none. A row whose condition fails is skipped.

## Rows

The rows are in the order the file states them. A row here for a standard mark replaces the standard's row for it.

| Roman | Character | Code points | When |
| --- | --- | --- | --- |
| `ng` | `𞵚` | U+1ED5A | always |
| `dh` | `𞵢` | U+1ED62 | always |
| `th` | `𞵡` | U+1ED61 | always |
| `kh` | `𞵣` | U+1ED63 | always |
| `gh` | `𞵤` | U+1ED64 | always |
| `nk` | `𞵚𞵘󠅎󠅋󠇯` | U+1ED5A U+1ED58 U+E014E U+E014B U+E01EF | always |
| `ch` | `𞵘` | U+1ED58 | always |
| `sh` | `𞵔` | U+1ED54 | always |
| `x` | `𞵘𞵔󠅘󠇯` | U+1ED58 U+1ED54 U+E0158 U+E01EF | always |
| `p` | `𞵐` | U+1ED50 | always |
| `v` | `𞵑` | U+1ED51 | always |
| `m` | `𞵒` | U+1ED52 | always |
| `t` | `𞵓` | U+1ED53 | always |
| `s` | `𞵔󠅓󠇯` | U+1ED54 U+E0153 U+E01EF | always |
| `n` | `𞵕` | U+1ED55 | always |
| `d` | `𞵖` | U+1ED56 | always |
| `k` | `𞵘󠅋󠇯` | U+1ED58 U+E014B U+E01EF | always |
| `h` | `𞵙` | U+1ED59 | always |
| `l` | `𞵛` | U+1ED5B | always |
| `r` | `𞵜` | U+1ED5C | always |
| `g` | `𞵠` | U+1ED60 | always |
| `b` | `𞵐󠅂󠇯` | U+1ED50 U+E0142 U+E01EF | always |
| `f` | `𞵑󠅆󠇯` | U+1ED51 U+E0146 U+E01EF | always |
| `w` | `𞵑󠅗󠇯` | U+1ED51 U+E0157 U+E01EF | always |
| `z` | `𞵔󠅚󠇯` | U+1ED54 U+E015A U+E01EF | always |
| `c` | `𞵘󠅃󠇯` | U+1ED58 U+E0143 U+E01EF | always |
| `q` | `𞵘󠅑󠇯` | U+1ED58 U+E0151 U+E01EF | always |
| `pp` | `𞵐𞵼` | U+1ED50 U+1ED7C | always |
| `vv` | `𞵑𞵼` | U+1ED51 U+1ED7C | always |
| `mm` | `𞵒𞵼` | U+1ED52 U+1ED7C | always |
| `tt` | `𞵓𞵼` | U+1ED53 U+1ED7C | always |
| `ss` | `𞵔𞵼` | U+1ED54 U+1ED7C | always |
| `nn` | `𞵕𞵼` | U+1ED55 U+1ED7C | always |
| `dd` | `𞵖𞵼` | U+1ED56 U+1ED7C | always |
| `kk` | `𞵘𞵼` | U+1ED58 U+1ED7C | always |
| `hh` | `𞵙𞵼` | U+1ED59 U+1ED7C | always |
| `ll` | `𞵛𞵼` | U+1ED5B U+1ED7C | always |
| `rr` | `𞵜𞵼` | U+1ED5C U+1ED7C | always |
| `gg` | `𞵠𞵼` | U+1ED60 U+1ED7C | always |
| `ngng` | `𞵚𞵼` | U+1ED5A U+1ED7C | always |
| `dhdh` | `𞵢𞵼` | U+1ED62 U+1ED7C | always |
| `thth` | `𞵡𞵼` | U+1ED61 U+1ED7C | always |
| `khkh` | `𞵣𞵼` | U+1ED63 U+1ED7C | always |
| `ghgh` | `𞵤𞵼` | U+1ED64 U+1ED7C | always |
| `-` | `󠅛󠄒󠅄󠅝` | U+E015B U+E0112 U+E0144 U+E015D | at the start of a word |
| `-` | `󠅛󠄒󠅄󠅝` | U+E015B U+E0112 U+E0144 U+E015D | at the end of a word |
| `-` | ` 󠅛󠄒󠅄󠅝󠇯` | U+0020 U+E015B U+E0112 U+E0144 U+E015D U+E01EF | always |
| `a` | `𞵝𞵰` | U+1ED5D U+1ED70 | at the start of a word |
| `a` | `𞵰` | U+1ED70 | always |
| `á` | `𞵝𞵰󠅛󠅅󠄑󠅝󠇯` | U+1ED5D U+1ED70 U+E015B U+E0145 U+E0111 U+E015D U+E01EF | at the start of a word |
| `á` | `𞵰󠅛󠅅󠄑󠅝󠇯` | U+1ED70 U+E015B U+E0145 U+E0111 U+E015D U+E01EF | always |
| `e` | `𞵝𞵳` | U+1ED5D U+1ED73 | at the start of a word |
| `e` | `𞵳` | U+1ED73 | always |
| `é` | `𞵝𞵳󠅛󠅅󠄙󠅝󠇯` | U+1ED5D U+1ED73 U+E015B U+E0145 U+E0119 U+E015D U+E01EF | at the start of a word |
| `é` | `𞵳󠅛󠅅󠄙󠅝󠇯` | U+1ED73 U+E015B U+E0145 U+E0119 U+E015D U+E01EF | always |
| `i` | `𞵝𞵴` | U+1ED5D U+1ED74 | at the start of a word |
| `i` | `𞵴` | U+1ED74 | always |
| `í` | `𞵝𞵴󠅛󠅅󠅄󠅝󠇯` | U+1ED5D U+1ED74 U+E015B U+E0145 U+E0144 U+E015D U+E01EF | at the start of a word |
| `í` | `𞵴󠅛󠅅󠅄󠅝󠇯` | U+1ED74 U+E015B U+E0145 U+E0144 U+E015D U+E01EF | always |
| `o` | `𞵝𞵱` | U+1ED5D U+1ED71 | at the start of a word |
| `o` | `𞵱` | U+1ED71 | always |
| `ó` | `𞵝𞵱󠅛󠅆󠄓󠅝󠇯` | U+1ED5D U+1ED71 U+E015B U+E0146 U+E0113 U+E015D U+E01EF | at the start of a word |
| `ó` | `𞵱󠅛󠅆󠄓󠅝󠇯` | U+1ED71 U+E015B U+E0146 U+E0113 U+E015D U+E01EF | always |
| `u` | `𞵝𞵲` | U+1ED5D U+1ED72 | at the start of a word |
| `u` | `𞵲` | U+1ED72 | always |
| `ú` | `𞵝𞵲󠅛󠅆󠅁󠅝󠇯` | U+1ED5D U+1ED72 U+E015B U+E0146 U+E0141 U+E015D U+E01EF | at the start of a word |
| `ú` | `𞵲󠅛󠅆󠅁󠅝󠇯` | U+1ED72 U+E015B U+E0146 U+E0141 U+E015D U+E01EF | always |
| `y` | `𞵝𞵵` | U+1ED5D U+1ED75 | at the start of a word |
| `y` | `𞵵` | U+1ED75 | always |
| `ý` | `𞵝𞵵󠅛󠅆󠅄󠅝󠇯` | U+1ED5D U+1ED75 U+E015B U+E0146 U+E0144 U+E015D U+E01EF | at the start of a word |
| `ý` | `𞵵󠅛󠅆󠅄󠅝󠇯` | U+1ED75 U+E015B U+E0146 U+E0144 U+E015D U+E01EF | always |
| `ë` | `𞵝𞵶` | U+1ED5D U+1ED76 | at the start of a word |
| `ë` | `𞵶` | U+1ED76 | always |
| `j` | `𞵝𞵵󠅊󠇯` | U+1ED5D U+1ED75 U+E014A U+E01EF | at the start of a word |
| `j` | `𞵵󠅊󠇯` | U+1ED75 U+E014A U+E01EF | always |
| `aa` | `𞵝𞵰𞵸` | U+1ED5D U+1ED70 U+1ED78 | at the start of a word |
| `aa` | `𞵰𞵸` | U+1ED70 U+1ED78 | always |
| `aá` | `𞵝𞵰𞵸󠅁󠅛󠅅󠄑󠅝󠇯` | U+1ED5D U+1ED70 U+1ED78 U+E0141 U+E015B U+E0145 U+E0111 U+E015D U+E01EF | at the start of a word |
| `aá` | `𞵰𞵸󠅁󠅛󠅅󠄑󠅝󠇯` | U+1ED70 U+1ED78 U+E0141 U+E015B U+E0145 U+E0111 U+E015D U+E01EF | always |
| `áa` | `𞵝𞵰𞵸󠅛󠅅󠄑󠅝󠅁󠇯` | U+1ED5D U+1ED70 U+1ED78 U+E015B U+E0145 U+E0111 U+E015D U+E0141 U+E01EF | at the start of a word |
| `áa` | `𞵰𞵸󠅛󠅅󠄑󠅝󠅁󠇯` | U+1ED70 U+1ED78 U+E015B U+E0145 U+E0111 U+E015D U+E0141 U+E01EF | always |
| `áá` | `𞵝𞵰𞵸󠅛󠅅󠄑󠅝󠅛󠅅󠄑󠅝󠇯` | U+1ED5D U+1ED70 U+1ED78 U+E015B U+E0145 U+E0111 U+E015D U+E015B U+E0145 U+E0111 U+E015D U+E01EF | at the start of a word |
| `áá` | `𞵰𞵸󠅛󠅅󠄑󠅝󠅛󠅅󠄑󠅝󠇯` | U+1ED70 U+1ED78 U+E015B U+E0145 U+E0111 U+E015D U+E015B U+E0145 U+E0111 U+E015D U+E01EF | always |
| `ae` | `𞵝𞵰𞵝𞵳󠅁󠅅󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED73 U+E0141 U+E0145 U+E01EF | at the start of a word |
| `ae` | `𞵰𞵝𞵳󠅁󠅅󠇯` | U+1ED70 U+1ED5D U+1ED73 U+E0141 U+E0145 U+E01EF | always |
| `aé` | `𞵝𞵰𞵝𞵳󠅁󠅛󠅅󠄙󠅝󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED73 U+E0141 U+E015B U+E0145 U+E0119 U+E015D U+E01EF | at the start of a word |
| `aé` | `𞵰𞵝𞵳󠅁󠅛󠅅󠄙󠅝󠇯` | U+1ED70 U+1ED5D U+1ED73 U+E0141 U+E015B U+E0145 U+E0119 U+E015D U+E01EF | always |
| `áe` | `𞵝𞵰𞵝𞵳󠅛󠅅󠄑󠅝󠅅󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED73 U+E015B U+E0145 U+E0111 U+E015D U+E0145 U+E01EF | at the start of a word |
| `áe` | `𞵰𞵝𞵳󠅛󠅅󠄑󠅝󠅅󠇯` | U+1ED70 U+1ED5D U+1ED73 U+E015B U+E0145 U+E0111 U+E015D U+E0145 U+E01EF | always |
| `áé` | `𞵝𞵰𞵝𞵳󠅛󠅅󠄑󠅝󠅛󠅅󠄙󠅝󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED73 U+E015B U+E0145 U+E0111 U+E015D U+E015B U+E0145 U+E0119 U+E015D U+E01EF | at the start of a word |
| `áé` | `𞵰𞵝𞵳󠅛󠅅󠄑󠅝󠅛󠅅󠄙󠅝󠇯` | U+1ED70 U+1ED5D U+1ED73 U+E015B U+E0145 U+E0111 U+E015D U+E015B U+E0145 U+E0119 U+E015D U+E01EF | always |
| `ao` | `𞵝𞵰𞵝𞵱󠅁󠅏󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED71 U+E0141 U+E014F U+E01EF | at the start of a word |
| `ao` | `𞵰𞵝𞵱󠅁󠅏󠇯` | U+1ED70 U+1ED5D U+1ED71 U+E0141 U+E014F U+E01EF | always |
| `aó` | `𞵝𞵰𞵝𞵱󠅁󠅛󠅆󠄓󠅝󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED71 U+E0141 U+E015B U+E0146 U+E0113 U+E015D U+E01EF | at the start of a word |
| `aó` | `𞵰𞵝𞵱󠅁󠅛󠅆󠄓󠅝󠇯` | U+1ED70 U+1ED5D U+1ED71 U+E0141 U+E015B U+E0146 U+E0113 U+E015D U+E01EF | always |
| `áo` | `𞵝𞵰𞵝𞵱󠅛󠅅󠄑󠅝󠅏󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED71 U+E015B U+E0145 U+E0111 U+E015D U+E014F U+E01EF | at the start of a word |
| `áo` | `𞵰𞵝𞵱󠅛󠅅󠄑󠅝󠅏󠇯` | U+1ED70 U+1ED5D U+1ED71 U+E015B U+E0145 U+E0111 U+E015D U+E014F U+E01EF | always |
| `áó` | `𞵝𞵰𞵝𞵱󠅛󠅅󠄑󠅝󠅛󠅆󠄓󠅝󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED71 U+E015B U+E0145 U+E0111 U+E015D U+E015B U+E0146 U+E0113 U+E015D U+E01EF | at the start of a word |
| `áó` | `𞵰𞵝𞵱󠅛󠅅󠄑󠅝󠅛󠅆󠄓󠅝󠇯` | U+1ED70 U+1ED5D U+1ED71 U+E015B U+E0145 U+E0111 U+E015D U+E015B U+E0146 U+E0113 U+E015D U+E01EF | always |
| `ay` | `𞵝𞵰𞵝𞵵󠅁󠅙󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED75 U+E0141 U+E0159 U+E01EF | at the start of a word |
| `ay` | `𞵰𞵝𞵵󠅁󠅙󠇯` | U+1ED70 U+1ED5D U+1ED75 U+E0141 U+E0159 U+E01EF | always |
| `aý` | `𞵝𞵰𞵝𞵵󠅁󠅛󠅆󠅄󠅝󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED75 U+E0141 U+E015B U+E0146 U+E0144 U+E015D U+E01EF | at the start of a word |
| `aý` | `𞵰𞵝𞵵󠅁󠅛󠅆󠅄󠅝󠇯` | U+1ED70 U+1ED5D U+1ED75 U+E0141 U+E015B U+E0146 U+E0144 U+E015D U+E01EF | always |
| `áy` | `𞵝𞵰𞵝𞵵󠅛󠅅󠄑󠅝󠅙󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED75 U+E015B U+E0145 U+E0111 U+E015D U+E0159 U+E01EF | at the start of a word |
| `áy` | `𞵰𞵝𞵵󠅛󠅅󠄑󠅝󠅙󠇯` | U+1ED70 U+1ED5D U+1ED75 U+E015B U+E0145 U+E0111 U+E015D U+E0159 U+E01EF | always |
| `áý` | `𞵝𞵰𞵝𞵵󠅛󠅅󠄑󠅝󠅛󠅆󠅄󠅝󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED75 U+E015B U+E0145 U+E0111 U+E015D U+E015B U+E0146 U+E0144 U+E015D U+E01EF | at the start of a word |
| `áý` | `𞵰𞵝𞵵󠅛󠅅󠄑󠅝󠅛󠅆󠅄󠅝󠇯` | U+1ED70 U+1ED5D U+1ED75 U+E015B U+E0145 U+E0111 U+E015D U+E015B U+E0146 U+E0144 U+E015D U+E01EF | always |
| `aë` | `𞵝𞵰𞵝𞵶󠅁󠅛󠅅󠅂󠅝󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED76 U+E0141 U+E015B U+E0145 U+E0142 U+E015D U+E01EF | at the start of a word |
| `aë` | `𞵰𞵝𞵶󠅁󠅛󠅅󠅂󠅝󠇯` | U+1ED70 U+1ED5D U+1ED76 U+E0141 U+E015B U+E0145 U+E0142 U+E015D U+E01EF | always |
| `áë` | `𞵝𞵰𞵝𞵶󠅛󠅅󠄑󠅝󠅛󠅅󠅂󠅝󠇯` | U+1ED5D U+1ED70 U+1ED5D U+1ED76 U+E015B U+E0145 U+E0111 U+E015D U+E015B U+E0145 U+E0142 U+E015D U+E01EF | at the start of a word |
| `áë` | `𞵰𞵝𞵶󠅛󠅅󠄑󠅝󠅛󠅅󠅂󠅝󠇯` | U+1ED70 U+1ED5D U+1ED76 U+E015B U+E0145 U+E0111 U+E015D U+E015B U+E0145 U+E0142 U+E015D U+E01EF | always |
| `ea` | `𞵝𞵳𞵝𞵰󠅅󠅁󠇯` | U+1ED5D U+1ED73 U+1ED5D U+1ED70 U+E0145 U+E0141 U+E01EF | at the start of a word |
| `ea` | `𞵳𞵝𞵰󠅅󠅁󠇯` | U+1ED73 U+1ED5D U+1ED70 U+E0145 U+E0141 U+E01EF | always |
| `eá` | `𞵝𞵳𞵝𞵰󠅅󠅛󠅅󠄑󠅝󠇯` | U+1ED5D U+1ED73 U+1ED5D U+1ED70 U+E0145 U+E015B U+E0145 U+E0111 U+E015D U+E01EF | at the start of a word |
| `eá` | `𞵳𞵝𞵰󠅅󠅛󠅅󠄑󠅝󠇯` | U+1ED73 U+1ED5D U+1ED70 U+E0145 U+E015B U+E0145 U+E0111 U+E015D U+E01EF | always |
| `éa` | `𞵝𞵳𞵝𞵰󠅛󠅅󠄙󠅝󠅁󠇯` | U+1ED5D U+1ED73 U+1ED5D U+1ED70 U+E015B U+E0145 U+E0119 U+E015D U+E0141 U+E01EF | at the start of a word |
| `éa` | `𞵳𞵝𞵰󠅛󠅅󠄙󠅝󠅁󠇯` | U+1ED73 U+1ED5D U+1ED70 U+E015B U+E0145 U+E0119 U+E015D U+E0141 U+E01EF | always |
| `éá` | `𞵝𞵳𞵝𞵰󠅛󠅅󠄙󠅝󠅛󠅅󠄑󠅝󠇯` | U+1ED5D U+1ED73 U+1ED5D U+1ED70 U+E015B U+E0145 U+E0119 U+E015D U+E015B U+E0145 U+E0111 U+E015D U+E01EF | at the start of a word |
| `éá` | `𞵳𞵝𞵰󠅛󠅅󠄙󠅝󠅛󠅅󠄑󠅝󠇯` | U+1ED73 U+1ED5D U+1ED70 U+E015B U+E0145 U+E0119 U+E015D U+E015B U+E0145 U+E0111 U+E015D U+E01EF | always |
| `ee` | `𞵝𞵳𞵸` | U+1ED5D U+1ED73 U+1ED78 | at the start of a word |
| `ee` | `𞵳𞵸` | U+1ED73 U+1ED78 | always |
| `eé` | `𞵝𞵳𞵸󠅅󠅛󠅅󠄙󠅝󠇯` | U+1ED5D U+1ED73 U+1ED78 U+E0145 U+E015B U+E0145 U+E0119 U+E015D U+E01EF | at the start of a word |
| `eé` | `𞵳𞵸󠅅󠅛󠅅󠄙󠅝󠇯` | U+1ED73 U+1ED78 U+E0145 U+E015B U+E0145 U+E0119 U+E015D U+E01EF | always |
| `ée` | `𞵝𞵳𞵸󠅛󠅅󠄙󠅝󠅅󠇯` | U+1ED5D U+1ED73 U+1ED78 U+E015B U+E0145 U+E0119 U+E015D U+E0145 U+E01EF | at the start of a word |
| `ée` | `𞵳𞵸󠅛󠅅󠄙󠅝󠅅󠇯` | U+1ED73 U+1ED78 U+E015B U+E0145 U+E0119 U+E015D U+E0145 U+E01EF | always |
| `éé` | `𞵝𞵳𞵸󠅛󠅅󠄙󠅝󠅛󠅅󠄙󠅝󠇯` | U+1ED5D U+1ED73 U+1ED78 U+E015B U+E0145 U+E0119 U+E015D U+E015B U+E0145 U+E0119 U+E015D U+E01EF | at the start of a word |
| `éé` | `𞵳𞵸󠅛󠅅󠄙󠅝󠅛󠅅󠄙󠅝󠇯` | U+1ED73 U+1ED78 U+E015B U+E0145 U+E0119 U+E015D U+E015B U+E0145 U+E0119 U+E015D U+E01EF | always |
| `eu` | `𞵝𞵳𞵝𞵲󠅅󠅕󠇯` | U+1ED5D U+1ED73 U+1ED5D U+1ED72 U+E0145 U+E0155 U+E01EF | at the start of a word |
| `eu` | `𞵳𞵝𞵲󠅅󠅕󠇯` | U+1ED73 U+1ED5D U+1ED72 U+E0145 U+E0155 U+E01EF | always |
| `eú` | `𞵝𞵳𞵝𞵲󠅅󠅛󠅆󠅁󠅝󠇯` | U+1ED5D U+1ED73 U+1ED5D U+1ED72 U+E0145 U+E015B U+E0146 U+E0141 U+E015D U+E01EF | at the start of a word |
| `eú` | `𞵳𞵝𞵲󠅅󠅛󠅆󠅁󠅝󠇯` | U+1ED73 U+1ED5D U+1ED72 U+E0145 U+E015B U+E0146 U+E0141 U+E015D U+E01EF | always |
| `éu` | `𞵝𞵳𞵝𞵲󠅛󠅅󠄙󠅝󠅕󠇯` | U+1ED5D U+1ED73 U+1ED5D U+1ED72 U+E015B U+E0145 U+E0119 U+E015D U+E0155 U+E01EF | at the start of a word |
| `éu` | `𞵳𞵝𞵲󠅛󠅅󠄙󠅝󠅕󠇯` | U+1ED73 U+1ED5D U+1ED72 U+E015B U+E0145 U+E0119 U+E015D U+E0155 U+E01EF | always |
| `éú` | `𞵝𞵳𞵝𞵲󠅛󠅅󠄙󠅝󠅛󠅆󠅁󠅝󠇯` | U+1ED5D U+1ED73 U+1ED5D U+1ED72 U+E015B U+E0145 U+E0119 U+E015D U+E015B U+E0146 U+E0141 U+E015D U+E01EF | at the start of a word |
| `éú` | `𞵳𞵝𞵲󠅛󠅅󠄙󠅝󠅛󠅆󠅁󠅝󠇯` | U+1ED73 U+1ED5D U+1ED72 U+E015B U+E0145 U+E0119 U+E015D U+E015B U+E0146 U+E0141 U+E015D U+E01EF | always |
| `ey` | `𞵝𞵳𞵝𞵵󠅅󠅙󠇯` | U+1ED5D U+1ED73 U+1ED5D U+1ED75 U+E0145 U+E0159 U+E01EF | at the start of a word |
| `ey` | `𞵳𞵝𞵵󠅅󠅙󠇯` | U+1ED73 U+1ED5D U+1ED75 U+E0145 U+E0159 U+E01EF | always |
| `eý` | `𞵝𞵳𞵝𞵵󠅅󠅛󠅆󠅄󠅝󠇯` | U+1ED5D U+1ED73 U+1ED5D U+1ED75 U+E0145 U+E015B U+E0146 U+E0144 U+E015D U+E01EF | at the start of a word |
| `eý` | `𞵳𞵝𞵵󠅅󠅛󠅆󠅄󠅝󠇯` | U+1ED73 U+1ED5D U+1ED75 U+E0145 U+E015B U+E0146 U+E0144 U+E015D U+E01EF | always |
| `éy` | `𞵝𞵳𞵝𞵵󠅛󠅅󠄙󠅝󠅙󠇯` | U+1ED5D U+1ED73 U+1ED5D U+1ED75 U+E015B U+E0145 U+E0119 U+E015D U+E0159 U+E01EF | at the start of a word |
| `éy` | `𞵳𞵝𞵵󠅛󠅅󠄙󠅝󠅙󠇯` | U+1ED73 U+1ED5D U+1ED75 U+E015B U+E0145 U+E0119 U+E015D U+E0159 U+E01EF | always |
| `éý` | `𞵝𞵳𞵝𞵵󠅛󠅅󠄙󠅝󠅛󠅆󠅄󠅝󠇯` | U+1ED5D U+1ED73 U+1ED5D U+1ED75 U+E015B U+E0145 U+E0119 U+E015D U+E015B U+E0146 U+E0144 U+E015D U+E01EF | at the start of a word |
| `éý` | `𞵳𞵝𞵵󠅛󠅅󠄙󠅝󠅛󠅆󠅄󠅝󠇯` | U+1ED73 U+1ED5D U+1ED75 U+E015B U+E0145 U+E0119 U+E015D U+E015B U+E0146 U+E0144 U+E015D U+E01EF | always |
| `eë` | `𞵝𞵶𞵸` | U+1ED5D U+1ED76 U+1ED78 | at the start of a word |
| `eë` | `𞵶𞵸` | U+1ED76 U+1ED78 | always |
| `éë` | `𞵝𞵶𞵸󠅛󠅅󠄙󠅝󠅛󠅅󠅂󠅝󠇯` | U+1ED5D U+1ED76 U+1ED78 U+E015B U+E0145 U+E0119 U+E015D U+E015B U+E0145 U+E0142 U+E015D U+E01EF | at the start of a word |
| `éë` | `𞵶𞵸󠅛󠅅󠄙󠅝󠅛󠅅󠅂󠅝󠇯` | U+1ED76 U+1ED78 U+E015B U+E0145 U+E0119 U+E015D U+E015B U+E0145 U+E0142 U+E015D U+E01EF | always |
| `ii` | `𞵝𞵴𞵸` | U+1ED5D U+1ED74 U+1ED78 | at the start of a word |
| `ii` | `𞵴𞵸` | U+1ED74 U+1ED78 | always |
| `ií` | `𞵝𞵴𞵸󠅉󠅛󠅅󠅄󠅝󠇯` | U+1ED5D U+1ED74 U+1ED78 U+E0149 U+E015B U+E0145 U+E0144 U+E015D U+E01EF | at the start of a word |
| `ií` | `𞵴𞵸󠅉󠅛󠅅󠅄󠅝󠇯` | U+1ED74 U+1ED78 U+E0149 U+E015B U+E0145 U+E0144 U+E015D U+E01EF | always |
| `íi` | `𞵝𞵴𞵸󠅛󠅅󠅄󠅝󠅉󠇯` | U+1ED5D U+1ED74 U+1ED78 U+E015B U+E0145 U+E0144 U+E015D U+E0149 U+E01EF | at the start of a word |
| `íi` | `𞵴𞵸󠅛󠅅󠅄󠅝󠅉󠇯` | U+1ED74 U+1ED78 U+E015B U+E0145 U+E0144 U+E015D U+E0149 U+E01EF | always |
| `íí` | `𞵝𞵴𞵸󠅛󠅅󠅄󠅝󠅛󠅅󠅄󠅝󠇯` | U+1ED5D U+1ED74 U+1ED78 U+E015B U+E0145 U+E0144 U+E015D U+E015B U+E0145 U+E0144 U+E015D U+E01EF | at the start of a word |
| `íí` | `𞵴𞵸󠅛󠅅󠅄󠅝󠅛󠅅󠅄󠅝󠇯` | U+1ED74 U+1ED78 U+E015B U+E0145 U+E0144 U+E015D U+E015B U+E0145 U+E0144 U+E015D U+E01EF | always |
| `io` | `𞵝𞵴𞵝𞵱󠅉󠅏󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED71 U+E0149 U+E014F U+E01EF | at the start of a word |
| `io` | `𞵴𞵝𞵱󠅉󠅏󠇯` | U+1ED74 U+1ED5D U+1ED71 U+E0149 U+E014F U+E01EF | always |
| `ió` | `𞵝𞵴𞵝𞵱󠅉󠅛󠅆󠄓󠅝󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED71 U+E0149 U+E015B U+E0146 U+E0113 U+E015D U+E01EF | at the start of a word |
| `ió` | `𞵴𞵝𞵱󠅉󠅛󠅆󠄓󠅝󠇯` | U+1ED74 U+1ED5D U+1ED71 U+E0149 U+E015B U+E0146 U+E0113 U+E015D U+E01EF | always |
| `ío` | `𞵝𞵴𞵝𞵱󠅛󠅅󠅄󠅝󠅏󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED71 U+E015B U+E0145 U+E0144 U+E015D U+E014F U+E01EF | at the start of a word |
| `ío` | `𞵴𞵝𞵱󠅛󠅅󠅄󠅝󠅏󠇯` | U+1ED74 U+1ED5D U+1ED71 U+E015B U+E0145 U+E0144 U+E015D U+E014F U+E01EF | always |
| `íó` | `𞵝𞵴𞵝𞵱󠅛󠅅󠅄󠅝󠅛󠅆󠄓󠅝󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED71 U+E015B U+E0145 U+E0144 U+E015D U+E015B U+E0146 U+E0113 U+E015D U+E01EF | at the start of a word |
| `íó` | `𞵴𞵝𞵱󠅛󠅅󠅄󠅝󠅛󠅆󠄓󠅝󠇯` | U+1ED74 U+1ED5D U+1ED71 U+E015B U+E0145 U+E0144 U+E015D U+E015B U+E0146 U+E0113 U+E015D U+E01EF | always |
| `iu` | `𞵝𞵴𞵝𞵲󠅉󠅕󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED72 U+E0149 U+E0155 U+E01EF | at the start of a word |
| `iu` | `𞵴𞵝𞵲󠅉󠅕󠇯` | U+1ED74 U+1ED5D U+1ED72 U+E0149 U+E0155 U+E01EF | always |
| `iú` | `𞵝𞵴𞵝𞵲󠅉󠅛󠅆󠅁󠅝󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED72 U+E0149 U+E015B U+E0146 U+E0141 U+E015D U+E01EF | at the start of a word |
| `iú` | `𞵴𞵝𞵲󠅉󠅛󠅆󠅁󠅝󠇯` | U+1ED74 U+1ED5D U+1ED72 U+E0149 U+E015B U+E0146 U+E0141 U+E015D U+E01EF | always |
| `íu` | `𞵝𞵴𞵝𞵲󠅛󠅅󠅄󠅝󠅕󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED72 U+E015B U+E0145 U+E0144 U+E015D U+E0155 U+E01EF | at the start of a word |
| `íu` | `𞵴𞵝𞵲󠅛󠅅󠅄󠅝󠅕󠇯` | U+1ED74 U+1ED5D U+1ED72 U+E015B U+E0145 U+E0144 U+E015D U+E0155 U+E01EF | always |
| `íú` | `𞵝𞵴𞵝𞵲󠅛󠅅󠅄󠅝󠅛󠅆󠅁󠅝󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED72 U+E015B U+E0145 U+E0144 U+E015D U+E015B U+E0146 U+E0141 U+E015D U+E01EF | at the start of a word |
| `íú` | `𞵴𞵝𞵲󠅛󠅅󠅄󠅝󠅛󠅆󠅁󠅝󠇯` | U+1ED74 U+1ED5D U+1ED72 U+E015B U+E0145 U+E0144 U+E015D U+E015B U+E0146 U+E0141 U+E015D U+E01EF | always |
| `iy` | `𞵝𞵴𞵝𞵵󠅉󠅙󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED75 U+E0149 U+E0159 U+E01EF | at the start of a word |
| `iy` | `𞵴𞵝𞵵󠅉󠅙󠇯` | U+1ED74 U+1ED5D U+1ED75 U+E0149 U+E0159 U+E01EF | always |
| `iý` | `𞵝𞵴𞵝𞵵󠅉󠅛󠅆󠅄󠅝󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED75 U+E0149 U+E015B U+E0146 U+E0144 U+E015D U+E01EF | at the start of a word |
| `iý` | `𞵴𞵝𞵵󠅉󠅛󠅆󠅄󠅝󠇯` | U+1ED74 U+1ED5D U+1ED75 U+E0149 U+E015B U+E0146 U+E0144 U+E015D U+E01EF | always |
| `íy` | `𞵝𞵴𞵝𞵵󠅛󠅅󠅄󠅝󠅙󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED75 U+E015B U+E0145 U+E0144 U+E015D U+E0159 U+E01EF | at the start of a word |
| `íy` | `𞵴𞵝𞵵󠅛󠅅󠅄󠅝󠅙󠇯` | U+1ED74 U+1ED5D U+1ED75 U+E015B U+E0145 U+E0144 U+E015D U+E0159 U+E01EF | always |
| `íý` | `𞵝𞵴𞵝𞵵󠅛󠅅󠅄󠅝󠅛󠅆󠅄󠅝󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED75 U+E015B U+E0145 U+E0144 U+E015D U+E015B U+E0146 U+E0144 U+E015D U+E01EF | at the start of a word |
| `íý` | `𞵴𞵝𞵵󠅛󠅅󠅄󠅝󠅛󠅆󠅄󠅝󠇯` | U+1ED74 U+1ED5D U+1ED75 U+E015B U+E0145 U+E0144 U+E015D U+E015B U+E0146 U+E0144 U+E015D U+E01EF | always |
| `ië` | `𞵝𞵴𞵝𞵶󠅉󠅛󠅅󠅂󠅝󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED76 U+E0149 U+E015B U+E0145 U+E0142 U+E015D U+E01EF | at the start of a word |
| `ië` | `𞵴𞵝𞵶󠅉󠅛󠅅󠅂󠅝󠇯` | U+1ED74 U+1ED5D U+1ED76 U+E0149 U+E015B U+E0145 U+E0142 U+E015D U+E01EF | always |
| `íë` | `𞵝𞵴𞵝𞵶󠅛󠅅󠅄󠅝󠅛󠅅󠅂󠅝󠇯` | U+1ED5D U+1ED74 U+1ED5D U+1ED76 U+E015B U+E0145 U+E0144 U+E015D U+E015B U+E0145 U+E0142 U+E015D U+E01EF | at the start of a word |
| `íë` | `𞵴𞵝𞵶󠅛󠅅󠅄󠅝󠅛󠅅󠅂󠅝󠇯` | U+1ED74 U+1ED5D U+1ED76 U+E015B U+E0145 U+E0144 U+E015D U+E015B U+E0145 U+E0142 U+E015D U+E01EF | always |
| `oa` | `𞵝𞵱𞵝𞵰󠅏󠅁󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED70 U+E014F U+E0141 U+E01EF | at the start of a word |
| `oa` | `𞵱𞵝𞵰󠅏󠅁󠇯` | U+1ED71 U+1ED5D U+1ED70 U+E014F U+E0141 U+E01EF | always |
| `oá` | `𞵝𞵱𞵝𞵰󠅏󠅛󠅅󠄑󠅝󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED70 U+E014F U+E015B U+E0145 U+E0111 U+E015D U+E01EF | at the start of a word |
| `oá` | `𞵱𞵝𞵰󠅏󠅛󠅅󠄑󠅝󠇯` | U+1ED71 U+1ED5D U+1ED70 U+E014F U+E015B U+E0145 U+E0111 U+E015D U+E01EF | always |
| `óa` | `𞵝𞵱𞵝𞵰󠅛󠅆󠄓󠅝󠅁󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED70 U+E015B U+E0146 U+E0113 U+E015D U+E0141 U+E01EF | at the start of a word |
| `óa` | `𞵱𞵝𞵰󠅛󠅆󠄓󠅝󠅁󠇯` | U+1ED71 U+1ED5D U+1ED70 U+E015B U+E0146 U+E0113 U+E015D U+E0141 U+E01EF | always |
| `óá` | `𞵝𞵱𞵝𞵰󠅛󠅆󠄓󠅝󠅛󠅅󠄑󠅝󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED70 U+E015B U+E0146 U+E0113 U+E015D U+E015B U+E0145 U+E0111 U+E015D U+E01EF | at the start of a word |
| `óá` | `𞵱𞵝𞵰󠅛󠅆󠄓󠅝󠅛󠅅󠄑󠅝󠇯` | U+1ED71 U+1ED5D U+1ED70 U+E015B U+E0146 U+E0113 U+E015D U+E015B U+E0145 U+E0111 U+E015D U+E01EF | always |
| `oe` | `𞵝𞵱𞵝𞵳󠅏󠅅󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED73 U+E014F U+E0145 U+E01EF | at the start of a word |
| `oe` | `𞵱𞵝𞵳󠅏󠅅󠇯` | U+1ED71 U+1ED5D U+1ED73 U+E014F U+E0145 U+E01EF | always |
| `oé` | `𞵝𞵱𞵝𞵳󠅏󠅛󠅅󠄙󠅝󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED73 U+E014F U+E015B U+E0145 U+E0119 U+E015D U+E01EF | at the start of a word |
| `oé` | `𞵱𞵝𞵳󠅏󠅛󠅅󠄙󠅝󠇯` | U+1ED71 U+1ED5D U+1ED73 U+E014F U+E015B U+E0145 U+E0119 U+E015D U+E01EF | always |
| `óe` | `𞵝𞵱𞵝𞵳󠅛󠅆󠄓󠅝󠅅󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED73 U+E015B U+E0146 U+E0113 U+E015D U+E0145 U+E01EF | at the start of a word |
| `óe` | `𞵱𞵝𞵳󠅛󠅆󠄓󠅝󠅅󠇯` | U+1ED71 U+1ED5D U+1ED73 U+E015B U+E0146 U+E0113 U+E015D U+E0145 U+E01EF | always |
| `óé` | `𞵝𞵱𞵝𞵳󠅛󠅆󠄓󠅝󠅛󠅅󠄙󠅝󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED73 U+E015B U+E0146 U+E0113 U+E015D U+E015B U+E0145 U+E0119 U+E015D U+E01EF | at the start of a word |
| `óé` | `𞵱𞵝𞵳󠅛󠅆󠄓󠅝󠅛󠅅󠄙󠅝󠇯` | U+1ED71 U+1ED5D U+1ED73 U+E015B U+E0146 U+E0113 U+E015D U+E015B U+E0145 U+E0119 U+E015D U+E01EF | always |
| `oo` | `𞵝𞵱𞵸` | U+1ED5D U+1ED71 U+1ED78 | at the start of a word |
| `oo` | `𞵱𞵸` | U+1ED71 U+1ED78 | always |
| `oó` | `𞵝𞵱𞵸󠅏󠅛󠅆󠄓󠅝󠇯` | U+1ED5D U+1ED71 U+1ED78 U+E014F U+E015B U+E0146 U+E0113 U+E015D U+E01EF | at the start of a word |
| `oó` | `𞵱𞵸󠅏󠅛󠅆󠄓󠅝󠇯` | U+1ED71 U+1ED78 U+E014F U+E015B U+E0146 U+E0113 U+E015D U+E01EF | always |
| `óo` | `𞵝𞵱𞵸󠅛󠅆󠄓󠅝󠅏󠇯` | U+1ED5D U+1ED71 U+1ED78 U+E015B U+E0146 U+E0113 U+E015D U+E014F U+E01EF | at the start of a word |
| `óo` | `𞵱𞵸󠅛󠅆󠄓󠅝󠅏󠇯` | U+1ED71 U+1ED78 U+E015B U+E0146 U+E0113 U+E015D U+E014F U+E01EF | always |
| `óó` | `𞵝𞵱𞵸󠅛󠅆󠄓󠅝󠅛󠅆󠄓󠅝󠇯` | U+1ED5D U+1ED71 U+1ED78 U+E015B U+E0146 U+E0113 U+E015D U+E015B U+E0146 U+E0113 U+E015D U+E01EF | at the start of a word |
| `óó` | `𞵱𞵸󠅛󠅆󠄓󠅝󠅛󠅆󠄓󠅝󠇯` | U+1ED71 U+1ED78 U+E015B U+E0146 U+E0113 U+E015D U+E015B U+E0146 U+E0113 U+E015D U+E01EF | always |
| `oy` | `𞵝𞵱𞵝𞵵󠅏󠅙󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED75 U+E014F U+E0159 U+E01EF | at the start of a word |
| `oy` | `𞵱𞵝𞵵󠅏󠅙󠇯` | U+1ED71 U+1ED5D U+1ED75 U+E014F U+E0159 U+E01EF | always |
| `oý` | `𞵝𞵱𞵝𞵵󠅏󠅛󠅆󠅄󠅝󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED75 U+E014F U+E015B U+E0146 U+E0144 U+E015D U+E01EF | at the start of a word |
| `oý` | `𞵱𞵝𞵵󠅏󠅛󠅆󠅄󠅝󠇯` | U+1ED71 U+1ED5D U+1ED75 U+E014F U+E015B U+E0146 U+E0144 U+E015D U+E01EF | always |
| `óy` | `𞵝𞵱𞵝𞵵󠅛󠅆󠄓󠅝󠅙󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED75 U+E015B U+E0146 U+E0113 U+E015D U+E0159 U+E01EF | at the start of a word |
| `óy` | `𞵱𞵝𞵵󠅛󠅆󠄓󠅝󠅙󠇯` | U+1ED71 U+1ED5D U+1ED75 U+E015B U+E0146 U+E0113 U+E015D U+E0159 U+E01EF | always |
| `óý` | `𞵝𞵱𞵝𞵵󠅛󠅆󠄓󠅝󠅛󠅆󠅄󠅝󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED75 U+E015B U+E0146 U+E0113 U+E015D U+E015B U+E0146 U+E0144 U+E015D U+E01EF | at the start of a word |
| `óý` | `𞵱𞵝𞵵󠅛󠅆󠄓󠅝󠅛󠅆󠅄󠅝󠇯` | U+1ED71 U+1ED5D U+1ED75 U+E015B U+E0146 U+E0113 U+E015D U+E015B U+E0146 U+E0144 U+E015D U+E01EF | always |
| `oë` | `𞵝𞵱𞵝𞵶󠅏󠅛󠅅󠅂󠅝󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED76 U+E014F U+E015B U+E0145 U+E0142 U+E015D U+E01EF | at the start of a word |
| `oë` | `𞵱𞵝𞵶󠅏󠅛󠅅󠅂󠅝󠇯` | U+1ED71 U+1ED5D U+1ED76 U+E014F U+E015B U+E0145 U+E0142 U+E015D U+E01EF | always |
| `óë` | `𞵝𞵱𞵝𞵶󠅛󠅆󠄓󠅝󠅛󠅅󠅂󠅝󠇯` | U+1ED5D U+1ED71 U+1ED5D U+1ED76 U+E015B U+E0146 U+E0113 U+E015D U+E015B U+E0145 U+E0142 U+E015D U+E01EF | at the start of a word |
| `óë` | `𞵱𞵝𞵶󠅛󠅆󠄓󠅝󠅛󠅅󠅂󠅝󠇯` | U+1ED71 U+1ED5D U+1ED76 U+E015B U+E0146 U+E0113 U+E015D U+E015B U+E0145 U+E0142 U+E015D U+E01EF | always |
| `ua` | `𞵝𞵲𞵝𞵰󠅕󠅁󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED70 U+E0155 U+E0141 U+E01EF | at the start of a word |
| `ua` | `𞵲𞵝𞵰󠅕󠅁󠇯` | U+1ED72 U+1ED5D U+1ED70 U+E0155 U+E0141 U+E01EF | always |
| `uá` | `𞵝𞵲𞵝𞵰󠅕󠅛󠅅󠄑󠅝󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED70 U+E0155 U+E015B U+E0145 U+E0111 U+E015D U+E01EF | at the start of a word |
| `uá` | `𞵲𞵝𞵰󠅕󠅛󠅅󠄑󠅝󠇯` | U+1ED72 U+1ED5D U+1ED70 U+E0155 U+E015B U+E0145 U+E0111 U+E015D U+E01EF | always |
| `úa` | `𞵝𞵲𞵝𞵰󠅛󠅆󠅁󠅝󠅁󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED70 U+E015B U+E0146 U+E0141 U+E015D U+E0141 U+E01EF | at the start of a word |
| `úa` | `𞵲𞵝𞵰󠅛󠅆󠅁󠅝󠅁󠇯` | U+1ED72 U+1ED5D U+1ED70 U+E015B U+E0146 U+E0141 U+E015D U+E0141 U+E01EF | always |
| `úá` | `𞵝𞵲𞵝𞵰󠅛󠅆󠅁󠅝󠅛󠅅󠄑󠅝󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED70 U+E015B U+E0146 U+E0141 U+E015D U+E015B U+E0145 U+E0111 U+E015D U+E01EF | at the start of a word |
| `úá` | `𞵲𞵝𞵰󠅛󠅆󠅁󠅝󠅛󠅅󠄑󠅝󠇯` | U+1ED72 U+1ED5D U+1ED70 U+E015B U+E0146 U+E0141 U+E015D U+E015B U+E0145 U+E0111 U+E015D U+E01EF | always |
| `ue` | `𞵝𞵲𞵝𞵳󠅕󠅅󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED73 U+E0155 U+E0145 U+E01EF | at the start of a word |
| `ue` | `𞵲𞵝𞵳󠅕󠅅󠇯` | U+1ED72 U+1ED5D U+1ED73 U+E0155 U+E0145 U+E01EF | always |
| `ué` | `𞵝𞵲𞵝𞵳󠅕󠅛󠅅󠄙󠅝󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED73 U+E0155 U+E015B U+E0145 U+E0119 U+E015D U+E01EF | at the start of a word |
| `ué` | `𞵲𞵝𞵳󠅕󠅛󠅅󠄙󠅝󠇯` | U+1ED72 U+1ED5D U+1ED73 U+E0155 U+E015B U+E0145 U+E0119 U+E015D U+E01EF | always |
| `úe` | `𞵝𞵲𞵝𞵳󠅛󠅆󠅁󠅝󠅅󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED73 U+E015B U+E0146 U+E0141 U+E015D U+E0145 U+E01EF | at the start of a word |
| `úe` | `𞵲𞵝𞵳󠅛󠅆󠅁󠅝󠅅󠇯` | U+1ED72 U+1ED5D U+1ED73 U+E015B U+E0146 U+E0141 U+E015D U+E0145 U+E01EF | always |
| `úé` | `𞵝𞵲𞵝𞵳󠅛󠅆󠅁󠅝󠅛󠅅󠄙󠅝󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED73 U+E015B U+E0146 U+E0141 U+E015D U+E015B U+E0145 U+E0119 U+E015D U+E01EF | at the start of a word |
| `úé` | `𞵲𞵝𞵳󠅛󠅆󠅁󠅝󠅛󠅅󠄙󠅝󠇯` | U+1ED72 U+1ED5D U+1ED73 U+E015B U+E0146 U+E0141 U+E015D U+E015B U+E0145 U+E0119 U+E015D U+E01EF | always |
| `uu` | `𞵝𞵲𞵸` | U+1ED5D U+1ED72 U+1ED78 | at the start of a word |
| `uu` | `𞵲𞵸` | U+1ED72 U+1ED78 | always |
| `uú` | `𞵝𞵲𞵸󠅕󠅛󠅆󠅁󠅝󠇯` | U+1ED5D U+1ED72 U+1ED78 U+E0155 U+E015B U+E0146 U+E0141 U+E015D U+E01EF | at the start of a word |
| `uú` | `𞵲𞵸󠅕󠅛󠅆󠅁󠅝󠇯` | U+1ED72 U+1ED78 U+E0155 U+E015B U+E0146 U+E0141 U+E015D U+E01EF | always |
| `úu` | `𞵝𞵲𞵸󠅛󠅆󠅁󠅝󠅕󠇯` | U+1ED5D U+1ED72 U+1ED78 U+E015B U+E0146 U+E0141 U+E015D U+E0155 U+E01EF | at the start of a word |
| `úu` | `𞵲𞵸󠅛󠅆󠅁󠅝󠅕󠇯` | U+1ED72 U+1ED78 U+E015B U+E0146 U+E0141 U+E015D U+E0155 U+E01EF | always |
| `úú` | `𞵝𞵲𞵸󠅛󠅆󠅁󠅝󠅛󠅆󠅁󠅝󠇯` | U+1ED5D U+1ED72 U+1ED78 U+E015B U+E0146 U+E0141 U+E015D U+E015B U+E0146 U+E0141 U+E015D U+E01EF | at the start of a word |
| `úú` | `𞵲𞵸󠅛󠅆󠅁󠅝󠅛󠅆󠅁󠅝󠇯` | U+1ED72 U+1ED78 U+E015B U+E0146 U+E0141 U+E015D U+E015B U+E0146 U+E0141 U+E015D U+E01EF | always |
| `uy` | `𞵝𞵲𞵝𞵵󠅕󠅙󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED75 U+E0155 U+E0159 U+E01EF | at the start of a word |
| `uy` | `𞵲𞵝𞵵󠅕󠅙󠇯` | U+1ED72 U+1ED5D U+1ED75 U+E0155 U+E0159 U+E01EF | always |
| `uý` | `𞵝𞵲𞵝𞵵󠅕󠅛󠅆󠅄󠅝󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED75 U+E0155 U+E015B U+E0146 U+E0144 U+E015D U+E01EF | at the start of a word |
| `uý` | `𞵲𞵝𞵵󠅕󠅛󠅆󠅄󠅝󠇯` | U+1ED72 U+1ED5D U+1ED75 U+E0155 U+E015B U+E0146 U+E0144 U+E015D U+E01EF | always |
| `úy` | `𞵝𞵲𞵝𞵵󠅛󠅆󠅁󠅝󠅙󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED75 U+E015B U+E0146 U+E0141 U+E015D U+E0159 U+E01EF | at the start of a word |
| `úy` | `𞵲𞵝𞵵󠅛󠅆󠅁󠅝󠅙󠇯` | U+1ED72 U+1ED5D U+1ED75 U+E015B U+E0146 U+E0141 U+E015D U+E0159 U+E01EF | always |
| `úý` | `𞵝𞵲𞵝𞵵󠅛󠅆󠅁󠅝󠅛󠅆󠅄󠅝󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED75 U+E015B U+E0146 U+E0141 U+E015D U+E015B U+E0146 U+E0144 U+E015D U+E01EF | at the start of a word |
| `úý` | `𞵲𞵝𞵵󠅛󠅆󠅁󠅝󠅛󠅆󠅄󠅝󠇯` | U+1ED72 U+1ED5D U+1ED75 U+E015B U+E0146 U+E0141 U+E015D U+E015B U+E0146 U+E0144 U+E015D U+E01EF | always |
| `uë` | `𞵝𞵲𞵝𞵶󠅕󠅛󠅅󠅂󠅝󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED76 U+E0155 U+E015B U+E0145 U+E0142 U+E015D U+E01EF | at the start of a word |
| `uë` | `𞵲𞵝𞵶󠅕󠅛󠅅󠅂󠅝󠇯` | U+1ED72 U+1ED5D U+1ED76 U+E0155 U+E015B U+E0145 U+E0142 U+E015D U+E01EF | always |
| `úë` | `𞵝𞵲𞵝𞵶󠅛󠅆󠅁󠅝󠅛󠅅󠅂󠅝󠇯` | U+1ED5D U+1ED72 U+1ED5D U+1ED76 U+E015B U+E0146 U+E0141 U+E015D U+E015B U+E0145 U+E0142 U+E015D U+E01EF | at the start of a word |
| `úë` | `𞵲𞵝𞵶󠅛󠅆󠅁󠅝󠅛󠅅󠅂󠅝󠇯` | U+1ED72 U+1ED5D U+1ED76 U+E015B U+E0146 U+E0141 U+E015D U+E015B U+E0145 U+E0142 U+E015D U+E01EF | always |
| `ya` | `𞵝𞵵𞵝𞵰󠅙󠅁󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED70 U+E0159 U+E0141 U+E01EF | at the start of a word |
| `ya` | `𞵵𞵝𞵰󠅙󠅁󠇯` | U+1ED75 U+1ED5D U+1ED70 U+E0159 U+E0141 U+E01EF | always |
| `yá` | `𞵝𞵵𞵝𞵰󠅙󠅛󠅅󠄑󠅝󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED70 U+E0159 U+E015B U+E0145 U+E0111 U+E015D U+E01EF | at the start of a word |
| `yá` | `𞵵𞵝𞵰󠅙󠅛󠅅󠄑󠅝󠇯` | U+1ED75 U+1ED5D U+1ED70 U+E0159 U+E015B U+E0145 U+E0111 U+E015D U+E01EF | always |
| `ýa` | `𞵝𞵵𞵝𞵰󠅛󠅆󠅄󠅝󠅁󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED70 U+E015B U+E0146 U+E0144 U+E015D U+E0141 U+E01EF | at the start of a word |
| `ýa` | `𞵵𞵝𞵰󠅛󠅆󠅄󠅝󠅁󠇯` | U+1ED75 U+1ED5D U+1ED70 U+E015B U+E0146 U+E0144 U+E015D U+E0141 U+E01EF | always |
| `ýá` | `𞵝𞵵𞵝𞵰󠅛󠅆󠅄󠅝󠅛󠅅󠄑󠅝󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED70 U+E015B U+E0146 U+E0144 U+E015D U+E015B U+E0145 U+E0111 U+E015D U+E01EF | at the start of a word |
| `ýá` | `𞵵𞵝𞵰󠅛󠅆󠅄󠅝󠅛󠅅󠄑󠅝󠇯` | U+1ED75 U+1ED5D U+1ED70 U+E015B U+E0146 U+E0144 U+E015D U+E015B U+E0145 U+E0111 U+E015D U+E01EF | always |
| `yo` | `𞵝𞵵𞵝𞵱󠅙󠅏󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED71 U+E0159 U+E014F U+E01EF | at the start of a word |
| `yo` | `𞵵𞵝𞵱󠅙󠅏󠇯` | U+1ED75 U+1ED5D U+1ED71 U+E0159 U+E014F U+E01EF | always |
| `yó` | `𞵝𞵵𞵝𞵱󠅙󠅛󠅆󠄓󠅝󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED71 U+E0159 U+E015B U+E0146 U+E0113 U+E015D U+E01EF | at the start of a word |
| `yó` | `𞵵𞵝𞵱󠅙󠅛󠅆󠄓󠅝󠇯` | U+1ED75 U+1ED5D U+1ED71 U+E0159 U+E015B U+E0146 U+E0113 U+E015D U+E01EF | always |
| `ýo` | `𞵝𞵵𞵝𞵱󠅛󠅆󠅄󠅝󠅏󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED71 U+E015B U+E0146 U+E0144 U+E015D U+E014F U+E01EF | at the start of a word |
| `ýo` | `𞵵𞵝𞵱󠅛󠅆󠅄󠅝󠅏󠇯` | U+1ED75 U+1ED5D U+1ED71 U+E015B U+E0146 U+E0144 U+E015D U+E014F U+E01EF | always |
| `ýó` | `𞵝𞵵𞵝𞵱󠅛󠅆󠅄󠅝󠅛󠅆󠄓󠅝󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED71 U+E015B U+E0146 U+E0144 U+E015D U+E015B U+E0146 U+E0113 U+E015D U+E01EF | at the start of a word |
| `ýó` | `𞵵𞵝𞵱󠅛󠅆󠅄󠅝󠅛󠅆󠄓󠅝󠇯` | U+1ED75 U+1ED5D U+1ED71 U+E015B U+E0146 U+E0144 U+E015D U+E015B U+E0146 U+E0113 U+E015D U+E01EF | always |
| `yu` | `𞵝𞵵𞵝𞵲󠅙󠅕󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED72 U+E0159 U+E0155 U+E01EF | at the start of a word |
| `yu` | `𞵵𞵝𞵲󠅙󠅕󠇯` | U+1ED75 U+1ED5D U+1ED72 U+E0159 U+E0155 U+E01EF | always |
| `yú` | `𞵝𞵵𞵝𞵲󠅙󠅛󠅆󠅁󠅝󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED72 U+E0159 U+E015B U+E0146 U+E0141 U+E015D U+E01EF | at the start of a word |
| `yú` | `𞵵𞵝𞵲󠅙󠅛󠅆󠅁󠅝󠇯` | U+1ED75 U+1ED5D U+1ED72 U+E0159 U+E015B U+E0146 U+E0141 U+E015D U+E01EF | always |
| `ýu` | `𞵝𞵵𞵝𞵲󠅛󠅆󠅄󠅝󠅕󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED72 U+E015B U+E0146 U+E0144 U+E015D U+E0155 U+E01EF | at the start of a word |
| `ýu` | `𞵵𞵝𞵲󠅛󠅆󠅄󠅝󠅕󠇯` | U+1ED75 U+1ED5D U+1ED72 U+E015B U+E0146 U+E0144 U+E015D U+E0155 U+E01EF | always |
| `ýú` | `𞵝𞵵𞵝𞵲󠅛󠅆󠅄󠅝󠅛󠅆󠅁󠅝󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED72 U+E015B U+E0146 U+E0144 U+E015D U+E015B U+E0146 U+E0141 U+E015D U+E01EF | at the start of a word |
| `ýú` | `𞵵𞵝𞵲󠅛󠅆󠅄󠅝󠅛󠅆󠅁󠅝󠇯` | U+1ED75 U+1ED5D U+1ED72 U+E015B U+E0146 U+E0144 U+E015D U+E015B U+E0146 U+E0141 U+E015D U+E01EF | always |
| `yy` | `𞵝𞵵𞵸` | U+1ED5D U+1ED75 U+1ED78 | at the start of a word |
| `yy` | `𞵵𞵸` | U+1ED75 U+1ED78 | always |
| `yý` | `𞵝𞵵𞵸󠅙󠅛󠅆󠅄󠅝󠇯` | U+1ED5D U+1ED75 U+1ED78 U+E0159 U+E015B U+E0146 U+E0144 U+E015D U+E01EF | at the start of a word |
| `yý` | `𞵵𞵸󠅙󠅛󠅆󠅄󠅝󠇯` | U+1ED75 U+1ED78 U+E0159 U+E015B U+E0146 U+E0144 U+E015D U+E01EF | always |
| `ýy` | `𞵝𞵵𞵸󠅛󠅆󠅄󠅝󠅙󠇯` | U+1ED5D U+1ED75 U+1ED78 U+E015B U+E0146 U+E0144 U+E015D U+E0159 U+E01EF | at the start of a word |
| `ýy` | `𞵵𞵸󠅛󠅆󠅄󠅝󠅙󠇯` | U+1ED75 U+1ED78 U+E015B U+E0146 U+E0144 U+E015D U+E0159 U+E01EF | always |
| `ýý` | `𞵝𞵵𞵸󠅛󠅆󠅄󠅝󠅛󠅆󠅄󠅝󠇯` | U+1ED5D U+1ED75 U+1ED78 U+E015B U+E0146 U+E0144 U+E015D U+E015B U+E0146 U+E0144 U+E015D U+E01EF | at the start of a word |
| `ýý` | `𞵵𞵸󠅛󠅆󠅄󠅝󠅛󠅆󠅄󠅝󠇯` | U+1ED75 U+1ED78 U+E015B U+E0146 U+E0144 U+E015D U+E015B U+E0146 U+E0144 U+E015D U+E01EF | always |
| `yë` | `𞵝𞵵𞵝𞵶󠅙󠅛󠅅󠅂󠅝󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED76 U+E0159 U+E015B U+E0145 U+E0142 U+E015D U+E01EF | at the start of a word |
| `yë` | `𞵵𞵝𞵶󠅙󠅛󠅅󠅂󠅝󠇯` | U+1ED75 U+1ED5D U+1ED76 U+E0159 U+E015B U+E0145 U+E0142 U+E015D U+E01EF | always |
| `ýë` | `𞵝𞵵𞵝𞵶󠅛󠅆󠅄󠅝󠅛󠅅󠅂󠅝󠇯` | U+1ED5D U+1ED75 U+1ED5D U+1ED76 U+E015B U+E0146 U+E0144 U+E015D U+E015B U+E0145 U+E0142 U+E015D U+E01EF | at the start of a word |
| `ýë` | `𞵵𞵝𞵶󠅛󠅆󠅄󠅝󠅛󠅅󠅂󠅝󠇯` | U+1ED75 U+1ED5D U+1ED76 U+E015B U+E0146 U+E0144 U+E015D U+E015B U+E0145 U+E0142 U+E015D U+E01EF | always |
| `ëa` | `𞵝𞵶𞵝𞵰󠅛󠅅󠅂󠅝󠅁󠇯` | U+1ED5D U+1ED76 U+1ED5D U+1ED70 U+E015B U+E0145 U+E0142 U+E015D U+E0141 U+E01EF | at the start of a word |
| `ëa` | `𞵶𞵝𞵰󠅛󠅅󠅂󠅝󠅁󠇯` | U+1ED76 U+1ED5D U+1ED70 U+E015B U+E0145 U+E0142 U+E015D U+E0141 U+E01EF | always |
| `ëá` | `𞵝𞵶𞵝𞵰󠅛󠅅󠅂󠅝󠅛󠅅󠄑󠅝󠇯` | U+1ED5D U+1ED76 U+1ED5D U+1ED70 U+E015B U+E0145 U+E0142 U+E015D U+E015B U+E0145 U+E0111 U+E015D U+E01EF | at the start of a word |
| `ëá` | `𞵶𞵝𞵰󠅛󠅅󠅂󠅝󠅛󠅅󠄑󠅝󠇯` | U+1ED76 U+1ED5D U+1ED70 U+E015B U+E0145 U+E0142 U+E015D U+E015B U+E0145 U+E0111 U+E015D U+E01EF | always |
| `ëe` | `𞵝𞵶𞵝𞵳󠅛󠅅󠅂󠅝󠅅󠇯` | U+1ED5D U+1ED76 U+1ED5D U+1ED73 U+E015B U+E0145 U+E0142 U+E015D U+E0145 U+E01EF | at the start of a word |
| `ëe` | `𞵶𞵝𞵳󠅛󠅅󠅂󠅝󠅅󠇯` | U+1ED76 U+1ED5D U+1ED73 U+E015B U+E0145 U+E0142 U+E015D U+E0145 U+E01EF | always |
| `ëé` | `𞵝𞵶𞵝𞵳󠅛󠅅󠅂󠅝󠅛󠅅󠄙󠅝󠇯` | U+1ED5D U+1ED76 U+1ED5D U+1ED73 U+E015B U+E0145 U+E0142 U+E015D U+E015B U+E0145 U+E0119 U+E015D U+E01EF | at the start of a word |
| `ëé` | `𞵶𞵝𞵳󠅛󠅅󠅂󠅝󠅛󠅅󠄙󠅝󠇯` | U+1ED76 U+1ED5D U+1ED73 U+E015B U+E0145 U+E0142 U+E015D U+E015B U+E0145 U+E0119 U+E015D U+E01EF | always |
| `ëi` | `𞵝𞵶𞵝𞵴󠅛󠅅󠅂󠅝󠅉󠇯` | U+1ED5D U+1ED76 U+1ED5D U+1ED74 U+E015B U+E0145 U+E0142 U+E015D U+E0149 U+E01EF | at the start of a word |
| `ëi` | `𞵶𞵝𞵴󠅛󠅅󠅂󠅝󠅉󠇯` | U+1ED76 U+1ED5D U+1ED74 U+E015B U+E0145 U+E0142 U+E015D U+E0149 U+E01EF | always |
| `ëí` | `𞵝𞵶𞵝𞵴󠅛󠅅󠅂󠅝󠅛󠅅󠅄󠅝󠇯` | U+1ED5D U+1ED76 U+1ED5D U+1ED74 U+E015B U+E0145 U+E0142 U+E015D U+E015B U+E0145 U+E0144 U+E015D U+E01EF | at the start of a word |
| `ëí` | `𞵶𞵝𞵴󠅛󠅅󠅂󠅝󠅛󠅅󠅄󠅝󠇯` | U+1ED76 U+1ED5D U+1ED74 U+E015B U+E0145 U+E0142 U+E015D U+E015B U+E0145 U+E0144 U+E015D U+E01EF | always |
| `ëo` | `𞵝𞵶𞵝𞵱󠅛󠅅󠅂󠅝󠅏󠇯` | U+1ED5D U+1ED76 U+1ED5D U+1ED71 U+E015B U+E0145 U+E0142 U+E015D U+E014F U+E01EF | at the start of a word |
| `ëo` | `𞵶𞵝𞵱󠅛󠅅󠅂󠅝󠅏󠇯` | U+1ED76 U+1ED5D U+1ED71 U+E015B U+E0145 U+E0142 U+E015D U+E014F U+E01EF | always |
| `ëó` | `𞵝𞵶𞵝𞵱󠅛󠅅󠅂󠅝󠅛󠅆󠄓󠅝󠇯` | U+1ED5D U+1ED76 U+1ED5D U+1ED71 U+E015B U+E0145 U+E0142 U+E015D U+E015B U+E0146 U+E0113 U+E015D U+E01EF | at the start of a word |
| `ëó` | `𞵶𞵝𞵱󠅛󠅅󠅂󠅝󠅛󠅆󠄓󠅝󠇯` | U+1ED76 U+1ED5D U+1ED71 U+E015B U+E0145 U+E0142 U+E015D U+E015B U+E0146 U+E0113 U+E015D U+E01EF | always |
| `ëu` | `𞵝𞵶𞵝𞵲󠅛󠅅󠅂󠅝󠅕󠇯` | U+1ED5D U+1ED76 U+1ED5D U+1ED72 U+E015B U+E0145 U+E0142 U+E015D U+E0155 U+E01EF | at the start of a word |
| `ëu` | `𞵶𞵝𞵲󠅛󠅅󠅂󠅝󠅕󠇯` | U+1ED76 U+1ED5D U+1ED72 U+E015B U+E0145 U+E0142 U+E015D U+E0155 U+E01EF | always |
| `ëú` | `𞵝𞵶𞵝𞵲󠅛󠅅󠅂󠅝󠅛󠅆󠅁󠅝󠇯` | U+1ED5D U+1ED76 U+1ED5D U+1ED72 U+E015B U+E0145 U+E0142 U+E015D U+E015B U+E0146 U+E0141 U+E015D U+E01EF | at the start of a word |
| `ëú` | `𞵶𞵝𞵲󠅛󠅅󠅂󠅝󠅛󠅆󠅁󠅝󠇯` | U+1ED76 U+1ED5D U+1ED72 U+E015B U+E0145 U+E0142 U+E015D U+E015B U+E0146 U+E0141 U+E015D U+E01EF | always |
| `ëy` | `𞵝𞵶𞵝𞵵󠅛󠅅󠅂󠅝󠅙󠇯` | U+1ED5D U+1ED76 U+1ED5D U+1ED75 U+E015B U+E0145 U+E0142 U+E015D U+E0159 U+E01EF | at the start of a word |
| `ëy` | `𞵶𞵝𞵵󠅛󠅅󠅂󠅝󠅙󠇯` | U+1ED76 U+1ED5D U+1ED75 U+E015B U+E0145 U+E0142 U+E015D U+E0159 U+E01EF | always |
| `ëý` | `𞵝𞵶𞵝𞵵󠅛󠅅󠅂󠅝󠅛󠅆󠅄󠅝󠇯` | U+1ED5D U+1ED76 U+1ED5D U+1ED75 U+E015B U+E0145 U+E0142 U+E015D U+E015B U+E0146 U+E0144 U+E015D U+E01EF | at the start of a word |
| `ëý` | `𞵶𞵝𞵵󠅛󠅅󠅂󠅝󠅛󠅆󠅄󠅝󠇯` | U+1ED76 U+1ED5D U+1ED75 U+E015B U+E0145 U+E0142 U+E015D U+E015B U+E0146 U+E0144 U+E015D U+E01EF | always |
| `ëë` | `𞵝𞵶𞵸󠅛󠅅󠅂󠅝󠅛󠅅󠅂󠅝󠇯` | U+1ED5D U+1ED76 U+1ED78 U+E015B U+E0145 U+E0142 U+E015D U+E015B U+E0145 U+E0142 U+E015D U+E01EF | at the start of a word |
| `ëë` | `𞵶𞵸󠅛󠅅󠅂󠅝󠅛󠅅󠅂󠅝󠇯` | U+1ED76 U+1ED78 U+E015B U+E0145 U+E0142 U+E015D U+E015B U+E0145 U+E0142 U+E015D U+E01EF | always |

## Round trip

Every encoding round-trips exactly: decoding the code points that encoding wrote gives back the roman text, and encoding that gives the same code points. The Code points column shows every character a row writes, including any that is invisible.

This page is written from `encodings/veldikko-aelendi.json` by `tools/encoding_docs.py`.
