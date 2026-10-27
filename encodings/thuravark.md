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

## Accepted characters

This encoding accepts `a-z`, `0-9`, `-`, `á`, `é`, `ë`, `í`, `ó`, `ú`, (space), `!`, `,`, `.`, `/`, `?`, `^`, `{`, `}`, `«`, `»`, `—`, `…`, `‹`, `›`, `‼`, and the standard's marks and whitespace. Any other character is refused at its line and column.

## Punctuation

This encoding includes the [standard roman punctuation](standard.md), which every language's roman shares. The table shows how this script writes each standard mark. A mark the script draws writes its glyph; a mark it does not draw writes the standard's invisible mark, the same in every encoding, so decoding restores it.

| Mark | Meaning | Written | Code points |
| --- | --- | --- | --- |
| `.` | completes a declarative sentence, terminal | drawn, `󰅀` | U+F0140 |
| `?` | completes an interrogative sentence, terminal | drawn, `󰅀` | U+F0140 U+E0101 U+E01EF |
| `‼` | completes an imperative sentence, terminal | drawn, `󰅀` | U+F0140 U+E0102 U+E01EF |
| `!` | completes an exclamative sentence, terminal | drawn, `󰅀` | U+F0140 U+E0103 U+E01EF |
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

The vowels are `aeiouáéëíóú`.

A row marked _before a vowel_ applies when the next character is a vowel.

Where several rows begin with the same roman, the longest wins, and among rows of one length a row whose condition holds comes before a row with none. A row whose condition fails is skipped.

## Rows

The rows are in the order the file states them. A row here for a standard mark replaces the standard's row for it.

| Roman | Character | Code points | When |
| --- | --- | --- | --- |
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
| `a` | `󰄀` | U+F0100 | always |
| `e` | `󰄁` | U+F0101 | always |
| `ë` | `󰄁󠅛󠅅󠅂󠅝󠇯` | U+F0101 U+E015B U+E0145 U+E0142 U+E015D U+E01EF | always |
| `i` | `󰄂` | U+F0102 | always |
| `o` | `󰄃` | U+F0103 | always |
| `u` | `󰄄` | U+F0104 | always |
| `b` | `󰄅` | U+F0105 | always |
| `d` | `󰄆` | U+F0106 | always |
| `f` | `󰄇` | U+F0107 | always |
| `g` | `󰄈` | U+F0108 | always |
| `h` | `󰄉` | U+F0109 | always |
| `j` | `󰄊` | U+F010A | always |
| `k` | `󰄋` | U+F010B | always |
| `q` | `󰄋󠅑󠇯` | U+F010B U+E0151 U+E01EF | always |
| `l` | `󰄌` | U+F010C | always |
| `m` | `󰄍` | U+F010D | always |
| `n` | `󰄎` | U+F010E | always |
| `p` | `󰄏` | U+F010F | always |
| `r` | `󰄐` | U+F0110 | always |
| `s` | `󰄑` | U+F0111 | always |
| `t` | `󰄒` | U+F0112 | always |
| `v` | `󰄓` | U+F0113 | always |
| `w` | `󰄔` | U+F0114 | always |
| `z` | `󰄕` | U+F0115 | always |
| `á` | `󰄀󰅈` | U+F0100 U+F0148 | always |
| `é` | `󰄁󰅈` | U+F0101 U+F0148 | always |
| `í` | `󰄂󰅈` | U+F0102 U+F0148 | always |
| `ó` | `󰄃󰅈` | U+F0103 U+F0148 | always |
| `ú` | `󰄄󰅈` | U+F0104 U+F0148 | always |
| `th` | `󰄠` | U+F0120 | always |
| `dh` | `󰄡` | U+F0121 | always |
| `kh` | `󰄢` | U+F0122 | always |
| `gh` | `󰄣` | U+F0123 | always |
| `ng` | `󰄥` | U+F0125 | always |
| `hl` | `󰄤` | U+F0124 | always |
| `ngh` | `󰄎󰄣󠅎󠅇󠅈󠇯` | U+F010E U+F0123 U+E014E U+E0147 U+E0148 U+E01EF | always |
| `tth` | `󰄠󰄠󠅔󠅔󠅈󠇯` | U+F0120 U+F0120 U+E0154 U+E0154 U+E0148 U+E01EF | always |
| `ddh` | `󰄡󰄡󠅄󠅄󠅈󠇯` | U+F0121 U+F0121 U+E0144 U+E0144 U+E0148 U+E01EF | always |
| `kkh` | `󰄢󰄢󠅋󠅋󠅈󠇯` | U+F0122 U+F0122 U+E014B U+E014B U+E0148 U+E01EF | always |
| `ggh` | `󰄣󰄣󠅇󠅇󠅈󠇯` | U+F0123 U+F0123 U+E0147 U+E0147 U+E0148 U+E01EF | always |
| `nng` | `󰄥󰄥󠅎󠅎󠅇󠇯` | U+F0125 U+F0125 U+E014E U+E014E U+E0147 U+E01EF | always |
| `hhl` | `󰄤󰄤󠅈󠅈󠅌󠇯` | U+F0124 U+F0124 U+E0148 U+E0148 U+E014C U+E01EF | always |
| `nngh` | `󰄎󰄎󰄣󠅎󠅎󠅇󠅈󠇯` | U+F010E U+F010E U+F0123 U+E014E U+E014E U+E0147 U+E0148 U+E01EF | always |
| `y` | `󰄊󠅙󠇯` | U+F010A U+E0159 U+E01EF | before a vowel |
| `y` | `󰄂󠅙󠇯` | U+F0102 U+E0159 U+E01EF | always |
| `.` | `󰅀` | U+F0140 | always |
| `?` | `󰅀󠄁󠇯` | U+F0140 U+E0101 U+E01EF | always |
| `‼` | `󰅀󠄂󠇯` | U+F0140 U+E0102 U+E01EF | always |
| `!` | `󰅀󠄃󠇯` | U+F0140 U+E0103 U+E01EF | always |
| `-` | `󠅛󠄒󠅄󠅝` | U+E015B U+E0112 U+E0144 U+E015D | always |
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
| (space) | (space) | U+0020 | always |

## Round trip

Every encoding round-trips exactly: decoding the code points that encoding wrote gives back the roman text, and encoding that gives the same code points. The Code points column shows every character a row writes, including any that is invisible.

This page is written from `encodings/thuravark.json` by `tools/encoding_docs.py`.
