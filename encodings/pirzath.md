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

## Accepted characters

This encoding accepts `a-z`, `0-9`, `#`, `$`, `%`, `&`, `'`, `-`, `@`, `^`, `á`, `é`, `ë`, `í`, `ó`, `ú`, `’`, and the standard's marks and whitespace. Any other character is refused at its line and column.

## Punctuation

This encoding extends the [standard roman encoding](standard.md), which every language's roman shares. The table shows how this script writes each standard mark. A mark the script draws writes its glyph; a mark it does not draw writes the standard's invisible mark, the same in every encoding, so decoding restores it.

| Mark | Meaning | Written | Code points |
| --- | --- | --- | --- |
| `.` | completes a declarative sentence, terminal | drawn, `󰁐` | U+F0050 |
| `?` | completes an interrogative sentence, terminal | drawn, `󰁐` | U+F0050 U+E0101 U+E01EF |
| `‼` | completes an imperative sentence, terminal | drawn, `󰁐` | U+F0050 U+E0102 U+E01EF |
| `!` | completes an exclamative sentence, terminal | drawn, `󰁐` | U+F0050 U+E0103 U+E01EF |
| `^` | at the beginning of a line, indents one level | invisible | U+E0104 |
| `,` | a pause that does not end the sentence | drawn, `󰁑` | U+F0051 |
| `«` | opens an outer quotation | drawn, `󰁔` | U+F0054 |
| `»` | closes an outer quotation | drawn, `󰁕` | U+F0055 |
| `‹` | opens a nested quotation | drawn, `󰁔` | U+F0054 U+E0108 U+E01EF |
| `›` | closes a nested quotation | drawn, `󰁕` | U+F0055 U+E0109 U+E01EF |
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

The vowels are `aeiouáéëíóú`.

A row marked _before a vowel_ applies when the next character is a vowel.

A row marked _before a consonant_ applies when the next character is a letter that is not a vowel.

A row marked _at the end of a word_ applies at the last character of the text or before whitespace, punctuation or a symbol.

Where several rows begin with the same roman, the longest wins, and among rows of one length a row whose condition holds comes before a row with none. A row whose condition fails is skipped.

## Rows

The rows are in the order the file states them. A row here for a standard mark replaces the standard's row for it.

| Roman | Character | Code points | When |
| --- | --- | --- | --- |
| `a` | `󰀀` | U+F0000 | always |
| `e` | `󰀁` | U+F0001 | always |
| `ë` | `󰀁󠅛󠅅󠅂󠅝󠇯` | U+F0001 U+E015B U+E0145 U+E0142 U+E015D U+E01EF | always |
| `i` | `󰀂` | U+F0002 | always |
| `o` | `󰀃` | U+F0003 | always |
| `u` | `󰀄` | U+F0004 | always |
| `p` | `󰀅` | U+F0005 | always |
| `b` | `󰀆` | U+F0006 | always |
| `f` | `󰀇` | U+F0007 | always |
| `v` | `󰀈` | U+F0008 | always |
| `m` | `󰀉` | U+F0009 | always |
| `t` | `󰀊` | U+F000A | always |
| `d` | `󰀋` | U+F000B | always |
| `n` | `󰀌` | U+F000C | always |
| `k` | `󰀍` | U+F000D | always |
| `g` | `󰀎` | U+F000E | always |
| `s` | `󰀏` | U+F000F | always |
| `z` | `󰀐` | U+F0010 | always |
| `h` | `󰀑` | U+F0011 | always |
| `l` | `󰀒` | U+F0012 | always |
| `r` | `󰀓` | U+F0013 | always |
| `j` | `󰀔` | U+F0014 | always |
| `q` | `󰀕` | U+F0015 | always |
| `w` | `󰀖` | U+F0016 | always |
| `á` | `󰀀󰁠` | U+F0000 U+F0060 | always |
| `é` | `󰀁󰁠` | U+F0001 U+F0060 | always |
| `í` | `󰀂󰁠` | U+F0002 U+F0060 | always |
| `ó` | `󰀃󰁠` | U+F0003 U+F0060 | always |
| `ú` | `󰀄󰁠` | U+F0004 U+F0060 | always |
| `'` | `󰀘` | U+F0018 | always |
| `’` | `󰀘󠅛󠄒󠄐󠄑󠄙󠅝󠇯` | U+F0018 U+E015B U+E0112 U+E0110 U+E0111 U+E0119 U+E015D U+E01EF | always |
| `th` | `󰀠` | U+F0020 | always |
| `dh` | `󰀡` | U+F0021 | always |
| `kh` | `󰀢` | U+F0022 | always |
| `gh` | `󰀣` | U+F0023 | always |
| `sh` | `󰀤` | U+F0024 | always |
| `zh` | `󰀥` | U+F0025 | always |
| `ch` | `󰀧` | U+F0027 | always |
| `ts` | `󰀦` | U+F0026 | always |
| `ng` | `󰀨` | U+F0028 | always |
| `ny` | `󰀩` | U+F0029 | always |
| `hl` | `󰀪` | U+F002A | always |
| `ngh` | `󰀌󰀣󠅎󠅇󠅈󠇯` | U+F000C U+F0023 U+E014E U+E0147 U+E0148 U+E01EF | always |
| `tth` | `󰀠󰀠󠅔󠅔󠅈󠇯` | U+F0020 U+F0020 U+E0154 U+E0154 U+E0148 U+E01EF | always |
| `ddh` | `󰀡󰀡󠅄󠅄󠅈󠇯` | U+F0021 U+F0021 U+E0144 U+E0144 U+E0148 U+E01EF | always |
| `kkh` | `󰀢󰀢󠅋󠅋󠅈󠇯` | U+F0022 U+F0022 U+E014B U+E014B U+E0148 U+E01EF | always |
| `ggh` | `󰀣󰀣󠅇󠅇󠅈󠇯` | U+F0023 U+F0023 U+E0147 U+E0147 U+E0148 U+E01EF | always |
| `ssh` | `󰀤󰀤󠅓󠅓󠅈󠇯` | U+F0024 U+F0024 U+E0153 U+E0153 U+E0148 U+E01EF | always |
| `zzh` | `󰀥󰀥󠅚󠅚󠅈󠇯` | U+F0025 U+F0025 U+E015A U+E015A U+E0148 U+E01EF | always |
| `cch` | `󰀧󰀧󠅃󠅃󠅈󠇯` | U+F0027 U+F0027 U+E0143 U+E0143 U+E0148 U+E01EF | always |
| `tts` | `󰀦󰀦󠅔󠅔󠅓󠇯` | U+F0026 U+F0026 U+E0154 U+E0154 U+E0153 U+E01EF | always |
| `nng` | `󰀨󰀨󠅎󠅎󠅇󠇯` | U+F0028 U+F0028 U+E014E U+E014E U+E0147 U+E01EF | always |
| `nny` | `󰀩󰀩󠅎󠅎󠅙󠇯` | U+F0029 U+F0029 U+E014E U+E014E U+E0159 U+E01EF | always |
| `hhl` | `󰀪󰀪󠅈󠅈󠅌󠇯` | U+F002A U+F002A U+E0148 U+E0148 U+E014C U+E01EF | always |
| `nngh` | `󰀌󰀌󰀣󠅎󠅎󠅇󠅈󠇯` | U+F000C U+F000C U+F0023 U+E014E U+E014E U+E0147 U+E0148 U+E01EF | always |
| `ai` | `󰀰` | U+F0030 | always |
| `aí` | `󰀰󰁠` | U+F0030 U+F0060 | always |
| `ái` | `󰀰󰁠󠅛󠅅󠄑󠅝󠅉󠇯` | U+F0030 U+F0060 U+E015B U+E0145 U+E0111 U+E015D U+E0149 U+E01EF | always |
| `áí` | `󰀰󰁠󰁠` | U+F0030 U+F0060 U+F0060 | always |
| `au` | `󰀱` | U+F0031 | always |
| `aú` | `󰀱󰁠` | U+F0031 U+F0060 | always |
| `áu` | `󰀱󰁠󠅛󠅅󠄑󠅝󠅕󠇯` | U+F0031 U+F0060 U+E015B U+E0145 U+E0111 U+E015D U+E0155 U+E01EF | always |
| `áú` | `󰀱󰁠󰁠` | U+F0031 U+F0060 U+F0060 | always |
| `ei` | `󰀲` | U+F0032 | always |
| `ëi` | `󰀲󠅛󠅅󠅂󠅝󠅉󠇯` | U+F0032 U+E015B U+E0145 U+E0142 U+E015D U+E0149 U+E01EF | always |
| `eí` | `󰀲󰁠` | U+F0032 U+F0060 | always |
| `ëí` | `󰀲󰁠󠅛󠅅󠅂󠅝󠅛󠅅󠅄󠅝󠇯` | U+F0032 U+F0060 U+E015B U+E0145 U+E0142 U+E015D U+E015B U+E0145 U+E0144 U+E015D U+E01EF | always |
| `éi` | `󰀲󰁠󠅛󠅅󠄙󠅝󠅉󠇯` | U+F0032 U+F0060 U+E015B U+E0145 U+E0119 U+E015D U+E0149 U+E01EF | always |
| `éí` | `󰀲󰁠󰁠` | U+F0032 U+F0060 U+F0060 | always |
| `oi` | `󰀳` | U+F0033 | always |
| `oí` | `󰀳󰁠` | U+F0033 U+F0060 | always |
| `ói` | `󰀳󰁠󠅛󠅆󠄓󠅝󠅉󠇯` | U+F0033 U+F0060 U+E015B U+E0146 U+E0113 U+E015D U+E0149 U+E01EF | always |
| `óí` | `󰀳󰁠󰁠` | U+F0033 U+F0060 U+F0060 | always |
| `ou` | `󰀴` | U+F0034 | always |
| `oú` | `󰀴󰁠` | U+F0034 U+F0060 | always |
| `óu` | `󰀴󰁠󠅛󠅆󠄓󠅝󠅕󠇯` | U+F0034 U+F0060 U+E015B U+E0146 U+E0113 U+E015D U+E0155 U+E01EF | always |
| `óú` | `󰀴󰁠󰁠` | U+F0034 U+F0060 U+F0060 | always |
| `ay` | `󰀰󠅁󠅙󠇯` | U+F0030 U+E0141 U+E0159 U+E01EF | before a consonant |
| `ay` | `󰀰󠅁󠅙󠇯` | U+F0030 U+E0141 U+E0159 U+E01EF | at the end of a word |
| `áy` | `󰀰󰁠󠅛󠅅󠄑󠅝󠅙󠇯` | U+F0030 U+F0060 U+E015B U+E0145 U+E0111 U+E015D U+E0159 U+E01EF | before a consonant |
| `áy` | `󰀰󰁠󠅛󠅅󠄑󠅝󠅙󠇯` | U+F0030 U+F0060 U+E015B U+E0145 U+E0111 U+E015D U+E0159 U+E01EF | at the end of a word |
| `ey` | `󰀲󠅅󠅙󠇯` | U+F0032 U+E0145 U+E0159 U+E01EF | before a consonant |
| `ëy` | `󰀲󠅛󠅅󠅂󠅝󠅙󠇯` | U+F0032 U+E015B U+E0145 U+E0142 U+E015D U+E0159 U+E01EF | before a consonant |
| `ey` | `󰀲󠅅󠅙󠇯` | U+F0032 U+E0145 U+E0159 U+E01EF | at the end of a word |
| `ëy` | `󰀲󠅛󠅅󠅂󠅝󠅙󠇯` | U+F0032 U+E015B U+E0145 U+E0142 U+E015D U+E0159 U+E01EF | at the end of a word |
| `éy` | `󰀲󰁠󠅛󠅅󠄙󠅝󠅙󠇯` | U+F0032 U+F0060 U+E015B U+E0145 U+E0119 U+E015D U+E0159 U+E01EF | before a consonant |
| `éy` | `󰀲󰁠󠅛󠅅󠄙󠅝󠅙󠇯` | U+F0032 U+F0060 U+E015B U+E0145 U+E0119 U+E015D U+E0159 U+E01EF | at the end of a word |
| `oy` | `󰀳󠅏󠅙󠇯` | U+F0033 U+E014F U+E0159 U+E01EF | before a consonant |
| `oy` | `󰀳󠅏󠅙󠇯` | U+F0033 U+E014F U+E0159 U+E01EF | at the end of a word |
| `óy` | `󰀳󰁠󠅛󠅆󠄓󠅝󠅙󠇯` | U+F0033 U+F0060 U+E015B U+E0146 U+E0113 U+E015D U+E0159 U+E01EF | before a consonant |
| `óy` | `󰀳󰁠󠅛󠅆󠄓󠅝󠅙󠇯` | U+F0033 U+F0060 U+E015B U+E0146 U+E0113 U+E015D U+E0159 U+E01EF | at the end of a word |
| `y` | `󰀗` | U+F0017 | before a vowel |
| `y` | `󰀂󠅙󠇯` | U+F0002 U+E0159 U+E01EF | always |
| `«` | `󰁔` | U+F0054 | always |
| `»` | `󰁕` | U+F0055 | always |
| `‹` | `󰁔󠄈󠇯` | U+F0054 U+E0108 U+E01EF | always |
| `›` | `󰁕󠄉󠇯` | U+F0055 U+E0109 U+E01EF | always |
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
| `?` | `󰁐󠄁󠇯` | U+F0050 U+E0101 U+E01EF | always |
| `‼` | `󰁐󠄂󠇯` | U+F0050 U+E0102 U+E01EF | always |
| `!` | `󰁐󠄃󠇯` | U+F0050 U+E0103 U+E01EF | always |
| `,` | `󰁑` | U+F0051 | always |
| `-` | `󰁓` | U+F0053 | always |

## Round trip

Every encoding round-trips exactly: decoding the code points that encoding wrote gives back the roman text, and encoding that gives the same code points. The Code points column shows every character a row writes, including any that is invisible.

This page is written from `encodings/pirzath.json` by `tools/encoding_docs.py`.
