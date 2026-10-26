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

## Accepted characters

This encoding accepts `a-z`, `0-9`, `'`, `-`, `ë`, `’`, and the standard's marks and whitespace. Any other character is refused at its line and column.

## Punctuation

This encoding extends the [standard roman encoding](standard.md), which every language's roman shares. The table shows how this script writes each standard mark. A mark the script draws writes its glyph; a mark it does not draw writes the standard's invisible mark, the same in every encoding, so decoding restores it.

| Mark | Meaning | Written | Code points |
| --- | --- | --- | --- |
| `.` | completes a declarative sentence, terminal | drawn, `𞨷` | U+1EA37 |
| `?` | completes an interrogative sentence, terminal | drawn, `𞨷` | U+1EA37 U+E0101 U+E01EF |
| `‼` | completes an imperative sentence, terminal | drawn, `𞨷` | U+1EA37 U+E0102 U+E01EF |
| `!` | completes an exclamative sentence, terminal | drawn, `𞨷` | U+1EA37 U+E0103 U+E01EF |
| `^` | at the beginning of a line, indents one level | invisible | U+E0104 |
| `,` | a pause that does not end the sentence | drawn, `𞨸` | U+1EA38 |
| `«` | opens an outer quotation | invisible | U+E0106 |
| `»` | closes an outer quotation | invisible | U+E0107 |
| `‹` | opens a nested quotation | invisible | U+E0108 |
| `›` | closes a nested quotation | invisible | U+E0109 |
| `—` | interrupts a sentence, non-terminal | invisible | U+E010A |
| `…` | abandons or resumes a sentence, non-terminal | invisible | U+E010B |
| `/` | verse line separator | drawn, `𞨹` | U+1EA39 |
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
| `l` | `𞨀` | U+1EA00 | always |
| `r` | `𞨁` | U+1EA01 | always |
| `t` | `𞨂` | U+1EA02 | always |
| `d` | `𞨃` | U+1EA03 | always |
| `z` | `𞨄` | U+1EA04 | always |
| `s` | `𞨅` | U+1EA05 | always |
| `g` | `𞨆` | U+1EA06 | always |
| `k` | `𞨇` | U+1EA07 | always |
| `n` | `𞨈` | U+1EA08 | always |
| `m` | `𞨊` | U+1EA0A | always |
| `q` | `𞨋` | U+1EA0B | always |
| `h` | `𞨎` | U+1EA0E | always |
| `p` | `𞨐` | U+1EA10 | always |
| `b` | `𞨑` | U+1EA11 | always |
| `f` | `𞨒` | U+1EA12 | always |
| `v` | `𞨒󠅖󠇯` | U+1EA12 U+E0156 U+E01EF | always |
| `w` | `𞨓` | U+1EA13 | always |
| `y` | `𞨔` | U+1EA14 | always |
| `th` | `𞨉` | U+1EA09 | always |
| `sh` | `𞨏` | U+1EA0F | always |
| `kh` | `𞨌` | U+1EA0C | always |
| `gh` | `𞨍` | U+1EA0D | always |
| `ch` | `𞨖` | U+1EA16 | always |
| `j` | `𞨖󠅊󠇯` | U+1EA16 U+E014A U+E01EF | always |
| `tj` | `𞨖󠅔󠅊󠇯` | U+1EA16 U+E0154 U+E014A U+E01EF | always |
| `ll` | `𞨗` | U+1EA17 | always |
| `rr` | `𞨘` | U+1EA18 | always |
| `tt` | `𞨙` | U+1EA19 | always |
| `dd` | `𞨚` | U+1EA1A | always |
| `zz` | `𞨛` | U+1EA1B | always |
| `ss` | `𞨜` | U+1EA1C | always |
| `gg` | `𞨝` | U+1EA1D | always |
| `kk` | `𞨞` | U+1EA1E | always |
| `nn` | `𞨟` | U+1EA1F | always |
| `mm` | `𞨡` | U+1EA21 | always |
| `qq` | `𞨢` | U+1EA22 | always |
| `hh` | `𞨥` | U+1EA25 | always |
| `pp` | `𞨧` | U+1EA27 | always |
| `bb` | `𞨨` | U+1EA28 | always |
| `ff` | `𞨩` | U+1EA29 | always |
| `fv` | `𞨩󠅆󠅖󠇯` | U+1EA29 U+E0146 U+E0156 U+E01EF | always |
| `vf` | `𞨩󠅖󠅆󠇯` | U+1EA29 U+E0156 U+E0146 U+E01EF | always |
| `vv` | `𞨩󠅖󠅖󠇯` | U+1EA29 U+E0156 U+E0156 U+E01EF | always |
| `ww` | `𞨪` | U+1EA2A | always |
| `yy` | `𞨫` | U+1EA2B | always |
| `tth` | `𞨠` | U+1EA20 | always |
| `ssh` | `𞨦` | U+1EA26 | always |
| `kkh` | `𞨣` | U+1EA23 | always |
| `ggh` | `𞨤` | U+1EA24 | always |
| `cch` | `𞨬` | U+1EA2C | always |
| `jj` | `𞨬󠅊󠅊󠇯` | U+1EA2C U+E014A U+E014A U+E01EF | always |
| `ttj` | `𞨬󠅔󠅔󠅊󠇯` | U+1EA2C U+E0154 U+E0154 U+E014A U+E01EF | always |
| `thth` | `𞨠󠅔󠅈󠅔󠅈󠇯` | U+1EA20 U+E0154 U+E0148 U+E0154 U+E0148 U+E01EF | always |
| `shsh` | `𞨦󠅓󠅈󠅓󠅈󠇯` | U+1EA26 U+E0153 U+E0148 U+E0153 U+E0148 U+E01EF | always |
| `khkh` | `𞨣󠅋󠅈󠅋󠅈󠇯` | U+1EA23 U+E014B U+E0148 U+E014B U+E0148 U+E01EF | always |
| `ghgh` | `𞨤󠅇󠅈󠅇󠅈󠇯` | U+1EA24 U+E0147 U+E0148 U+E0147 U+E0148 U+E01EF | always |
| `chch` | `𞨬󠅃󠅈󠅃󠅈󠇯` | U+1EA2C U+E0143 U+E0148 U+E0143 U+E0148 U+E01EF | always |
| `chj` | `𞨬󠅃󠅈󠅊󠇯` | U+1EA2C U+E0143 U+E0148 U+E014A U+E01EF | always |
| `jch` | `𞨬󠅊󠅃󠅈󠇯` | U+1EA2C U+E014A U+E0143 U+E0148 U+E01EF | always |
| `chtj` | `𞨬󠅃󠅈󠅔󠅊󠇯` | U+1EA2C U+E0143 U+E0148 U+E0154 U+E014A U+E01EF | always |
| `jtj` | `𞨬󠅊󠅔󠅊󠇯` | U+1EA2C U+E014A U+E0154 U+E014A U+E01EF | always |
| `tjch` | `𞨬󠅔󠅊󠅃󠅈󠇯` | U+1EA2C U+E0154 U+E014A U+E0143 U+E0148 U+E01EF | always |
| `tjj` | `𞨬󠅔󠅊󠅊󠇯` | U+1EA2C U+E0154 U+E014A U+E014A U+E01EF | always |
| `tjtj` | `𞨬󠅔󠅊󠅔󠅊󠇯` | U+1EA2C U+E0154 U+E014A U+E0154 U+E014A U+E01EF | always |
| `ttth` | `𞨂𞨠󠅔󠅔󠅔󠅈󠇯` | U+1EA02 U+1EA20 U+E0154 U+E0154 U+E0154 U+E0148 U+E01EF | always |
| `sssh` | `𞨅𞨦󠅓󠅓󠅓󠅈󠇯` | U+1EA05 U+1EA26 U+E0153 U+E0153 U+E0153 U+E0148 U+E01EF | always |
| `kkkh` | `𞨇𞨣󠅋󠅋󠅋󠅈󠇯` | U+1EA07 U+1EA23 U+E014B U+E014B U+E014B U+E0148 U+E01EF | always |
| `gggh` | `𞨆𞨤󠅇󠅇󠅇󠅈󠇯` | U+1EA06 U+1EA24 U+E0147 U+E0147 U+E0147 U+E0148 U+E01EF | always |
| `tttj` | `𞨂𞨬󠅔󠅔󠅔󠅊󠇯` | U+1EA02 U+1EA2C U+E0154 U+E0154 U+E0154 U+E014A U+E01EF | always |
| `a` | `𞨕` | U+1EA15 | at the start of a word |
| `a` | `󠅁` | U+E0141 | always |
| `e` | `𞨕󠅅󠇯` | U+1EA15 U+E0145 U+E01EF | at the start of a word |
| `ë` | `𞨕󠅛󠅅󠅂󠅝󠇯` | U+1EA15 U+E015B U+E0145 U+E0142 U+E015D U+E01EF | at the start of a word |
| `e` | `󠅅` | U+E0145 | always |
| `ë` | `󠅛󠅅󠅂󠅝` | U+E015B U+E0145 U+E0142 U+E015D | always |
| `i` | `𞨕󠅉󠇯` | U+1EA15 U+E0149 U+E01EF | at the start of a word |
| `i` | `󠅉` | U+E0149 | always |
| `o` | `𞨕󠅏󠇯` | U+1EA15 U+E014F U+E01EF | at the start of a word |
| `o` | `󠅏` | U+E014F | always |
| `u` | `𞨕󠅕󠇯` | U+1EA15 U+E0155 U+E01EF | at the start of a word |
| `u` | `󠅕` | U+E0155 | always |
| `'` | `𞨕󠅛󠄒󠄗󠅝󠇯` | U+1EA15 U+E015B U+E0112 U+E0117 U+E015D U+E01EF | always |
| `'a` | `𞨕󠅛󠄒󠄗󠅝󠅛󠄖󠄑󠅝󠇯` | U+1EA15 U+E015B U+E0112 U+E0117 U+E015D U+E015B U+E0116 U+E0111 U+E015D U+E01EF | always |
| `'e` | `𞨕󠅛󠄒󠄗󠅝󠅛󠄖󠄕󠅝󠇯` | U+1EA15 U+E015B U+E0112 U+E0117 U+E015D U+E015B U+E0116 U+E0115 U+E015D U+E01EF | always |
| `'ë` | `𞨕󠅛󠄒󠄗󠅝󠅛󠅅󠅂󠅝󠇯` | U+1EA15 U+E015B U+E0112 U+E0117 U+E015D U+E015B U+E0145 U+E0142 U+E015D U+E01EF | always |
| `'i` | `𞨕󠅛󠄒󠄗󠅝󠅛󠄖󠄙󠅝󠇯` | U+1EA15 U+E015B U+E0112 U+E0117 U+E015D U+E015B U+E0116 U+E0119 U+E015D U+E01EF | always |
| `'o` | `𞨕󠅛󠄒󠄗󠅝󠅛󠄖󠅆󠅝󠇯` | U+1EA15 U+E015B U+E0112 U+E0117 U+E015D U+E015B U+E0116 U+E0146 U+E015D U+E01EF | always |
| `'u` | `𞨕󠅛󠄒󠄗󠅝󠅛󠄗󠄕󠅝󠇯` | U+1EA15 U+E015B U+E0112 U+E0117 U+E015D U+E015B U+E0117 U+E0115 U+E015D U+E01EF | always |
| `’` | `𞨕󠅛󠄒󠄐󠄑󠄙󠅝󠇯` | U+1EA15 U+E015B U+E0112 U+E0110 U+E0111 U+E0119 U+E015D U+E01EF | always |
| `’a` | `𞨕󠅛󠄒󠄐󠄑󠄙󠅝󠅁󠇯` | U+1EA15 U+E015B U+E0112 U+E0110 U+E0111 U+E0119 U+E015D U+E0141 U+E01EF | always |
| `’e` | `𞨕󠅛󠄒󠄐󠄑󠄙󠅝󠅅󠇯` | U+1EA15 U+E015B U+E0112 U+E0110 U+E0111 U+E0119 U+E015D U+E0145 U+E01EF | always |
| `’ë` | `𞨕󠅛󠄒󠄐󠄑󠄙󠅝󠅛󠅅󠅂󠅝󠇯` | U+1EA15 U+E015B U+E0112 U+E0110 U+E0111 U+E0119 U+E015D U+E015B U+E0145 U+E0142 U+E015D U+E01EF | always |
| `’i` | `𞨕󠅛󠄒󠄐󠄑󠄙󠅝󠅉󠇯` | U+1EA15 U+E015B U+E0112 U+E0110 U+E0111 U+E0119 U+E015D U+E0149 U+E01EF | always |
| `’o` | `𞨕󠅛󠄒󠄐󠄑󠄙󠅝󠅏󠇯` | U+1EA15 U+E015B U+E0112 U+E0110 U+E0111 U+E0119 U+E015D U+E014F U+E01EF | always |
| `’u` | `𞨕󠅛󠄒󠄐󠄑󠄙󠅝󠅕󠇯` | U+1EA15 U+E015B U+E0112 U+E0110 U+E0111 U+E0119 U+E015D U+E0155 U+E01EF | always |
| `-` | `󠅛󠄒󠅄󠅝` | U+E015B U+E0112 U+E0144 U+E015D | at the end of a word |
| `-` | ` 󠅛󠄒󠅄󠅝󠇯` | U+0020 U+E015B U+E0112 U+E0144 U+E015D U+E01EF | always |
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
| `?` | `𞨷󠄁󠇯` | U+1EA37 U+E0101 U+E01EF | always |
| `‼` | `𞨷󠄂󠇯` | U+1EA37 U+E0102 U+E01EF | always |
| `!` | `𞨷󠄃󠇯` | U+1EA37 U+E0103 U+E01EF | always |
| `,` | `𞨸` | U+1EA38 | always |
| `/` | `𞨹` | U+1EA39 | always |

## Round trip

Every encoding round-trips exactly: decoding the code points that encoding wrote gives back the roman text, and encoding that gives the same code points. The Code points column shows every character a row writes, including any that is invisible.

This page is written from `encodings/qalezu.json` by `tools/encoding_docs.py`.
