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

## Accepted characters

This encoding accepts `a-z`, `0-9`, `'`, `-`, `’`, and the standard's marks and whitespace. Any other character is refused at its line and column.

## Punctuation

This encoding extends the [standard roman encoding](standard.md), which every language's roman shares. The table shows how this script writes each standard mark. A mark the script draws writes its glyph; a mark it does not draw writes the standard's invisible mark, the same in every encoding, so decoding restores it.

| Mark | Meaning | Written | Code points |
| --- | --- | --- | --- |
| `.` | completes a declarative sentence, terminal | drawn, `󰑑` | U+F0451 |
| `?` | completes an interrogative sentence, terminal | drawn, `󰑑` | U+F0451 U+E011F U+E01EF |
| `!` | completes an imperative sentence, terminal | drawn, `󰑑` | U+F0451 U+E0101 U+E01EF |
| `!!` | completes an exclamative sentence, terminal | drawn, `󰑑` | U+F0451 U+E0101 U+E0101 U+E01EF |
| `,` | a pause that does not end the sentence | drawn, `󰑐` | U+F0450 |
| `«` | opens a quotation of one or more terminated sentences | invisible | U+E015B U+E0141 U+E0142 U+E015D |
| `»` | closes a quotation opened by `«` | invisible | U+E015B U+E0142 U+E0142 U+E015D |
| `‹` | opens a quotation nested inside `«` `»`, alternating with them at any depth | invisible | U+E015B U+E0112 U+E0110 U+E0113 U+E0119 U+E015D |
| `›` | closes a quotation opened by `‹` | invisible | U+E015B U+E0112 U+E0110 U+E0113 U+E0141 U+E015D |
| `—` | interrupts a sentence, non-terminal, immediately followed by a terminal | invisible | U+E015B U+E0112 U+E0110 U+E0111 U+E0114 U+E015D |
| `…` | abandons a sentence, non-terminal and immediately followed by a terminal; at a sentence's start, resumes one | invisible | U+E015B U+E0112 U+E0110 U+E0112 U+E0116 U+E015D |
| `/` | verse line end | invisible | U+E010F |
| `//` | verse stanza end | invisible | U+E010F U+E010F |
| `***` | verse canto end | invisible | U+E010A U+E010A U+E010A |
| `{` | opens a name | invisible | U+E015B U+E0117 U+E0142 U+E015D |
| `}` | closes a name opened by `{` | invisible | U+E015D |

## Whitespace

In roman, outside `⟦` and `⟧`, any run of spaces, tabs and line breaks is one word separator. It is not a character of the script, and no row matches it.

This script spaces its words, so its `separator` is one space, U+0020: a separator writes one space, and decoding writes one space.

The separator is normalized on input, not preserved: `a  b` and `a\n\tb` encode as `a b` does, and decoding writes a single space.

A character that no row matches is refused: `encode.py` reports it with its line and column, and writes nothing.

## Literal spans

`⟦` and `⟧` enclose character names, as the [standard](standard.md) describes: `⟦LATIN_SMALL_LETTER_A_WITH_ACUTE⟧` writes `á`. Whitespace between names only separates them.

## Vowels and conditions

The vowels are `aeiou`.

A row marked _before a vowel_ applies when the next character is a vowel.

A row marked _at the start of a word_ applies at the first character of the text or after whitespace, punctuation or a symbol.

Where several rows begin with the same roman, the longest wins, and among rows of one length a row whose condition holds comes before a row with none. A row whose condition fails is skipped.

## Rows

The rows are in the order the file states them. A row here for a standard mark replaces the standard's row for it.

| Roman | Character | Code points | When |
| --- | --- | --- | --- |
| `k` | `󰐀󰐸󠅋󠇯` | U+F0400 U+F0438 U+E014B U+E01EF | always |
| `k` | `󰐀` | U+F0400 | before a vowel |
| `kh` | `󰐁󰐸󠅋󠅈󠇯` | U+F0401 U+F0438 U+E014B U+E0148 U+E01EF | always |
| `kh` | `󰐁` | U+F0401 | before a vowel |
| `g` | `󰐂󰐸󠅇󠇯` | U+F0402 U+F0438 U+E0147 U+E01EF | always |
| `g` | `󰐂` | U+F0402 | before a vowel |
| `gh` | `󰐃󰐸󠅇󠅈󠇯` | U+F0403 U+F0438 U+E0147 U+E0148 U+E01EF | always |
| `gh` | `󰐃` | U+F0403 | before a vowel |
| `ng` | `󰐄󰐸󠅎󠅇󠇯` | U+F0404 U+F0438 U+E014E U+E0147 U+E01EF | always |
| `ng` | `󰐄` | U+F0404 | before a vowel |
| `ch` | `󰐅󰐸󠅃󠅈󠇯` | U+F0405 U+F0438 U+E0143 U+E0148 U+E01EF | always |
| `ch` | `󰐅` | U+F0405 | before a vowel |
| `j` | `󰐆󰐸󠅊󠇯` | U+F0406 U+F0438 U+E014A U+E01EF | always |
| `j` | `󰐆` | U+F0406 | before a vowel |
| `ny` | `󰐇󰐸󠅎󠅙󠇯` | U+F0407 U+F0438 U+E014E U+E0159 U+E01EF | always |
| `ny` | `󰐇` | U+F0407 | before a vowel |
| `t` | `󰐈󰐸󠅔󠇯` | U+F0408 U+F0438 U+E0154 U+E01EF | always |
| `t` | `󰐈` | U+F0408 | before a vowel |
| `d` | `󰐉󰐸󠅄󠇯` | U+F0409 U+F0438 U+E0144 U+E01EF | always |
| `d` | `󰐉` | U+F0409 | before a vowel |
| `n` | `󰐊󰐸󠅎󠇯` | U+F040A U+F0438 U+E014E U+E01EF | always |
| `n` | `󰐊` | U+F040A | before a vowel |
| `p` | `󰐋󰐸󠅐󠇯` | U+F040B U+F0438 U+E0150 U+E01EF | always |
| `p` | `󰐋` | U+F040B | before a vowel |
| `b` | `󰐌󰐸󠅂󠇯` | U+F040C U+F0438 U+E0142 U+E01EF | always |
| `b` | `󰐌` | U+F040C | before a vowel |
| `bh` | `󰐍󰐸󠅂󠅈󠇯` | U+F040D U+F0438 U+E0142 U+E0148 U+E01EF | always |
| `bh` | `󰐍` | U+F040D | before a vowel |
| `m` | `󰐎󰐸󠅍󠇯` | U+F040E U+F0438 U+E014D U+E01EF | always |
| `m` | `󰐎` | U+F040E | before a vowel |
| `y` | `󰐏󰐸󠅙󠇯` | U+F040F U+F0438 U+E0159 U+E01EF | always |
| `y` | `󰐏` | U+F040F | before a vowel |
| `r` | `󰐐󰐸󠅒󠇯` | U+F0410 U+F0438 U+E0152 U+E01EF | always |
| `r` | `󰐐` | U+F0410 | before a vowel |
| `l` | `󰐑󰐸󠅌󠇯` | U+F0411 U+F0438 U+E014C U+E01EF | always |
| `l` | `󰐑` | U+F0411 | before a vowel |
| `v` | `󰐒󰐸󠅖󠇯` | U+F0412 U+F0438 U+E0156 U+E01EF | always |
| `v` | `󰐒` | U+F0412 | before a vowel |
| `sh` | `󰐓󰐸󠅓󠅈󠇯` | U+F0413 U+F0438 U+E0153 U+E0148 U+E01EF | always |
| `sh` | `󰐓` | U+F0413 | before a vowel |
| `s` | `󰐔󰐸󠅓󠇯` | U+F0414 U+F0438 U+E0153 U+E01EF | always |
| `s` | `󰐔` | U+F0414 | before a vowel |
| `h` | `󰐕󰐸󠅈󠇯` | U+F0415 U+F0438 U+E0148 U+E01EF | always |
| `h` | `󰐕` | U+F0415 | before a vowel |
| `f` | `󰐋󰐹󰐸󠅆󠇯` | U+F040B U+F0439 U+F0438 U+E0146 U+E01EF | always |
| `f` | `󰐋󰐹` | U+F040B U+F0439 | before a vowel |
| `a` | `󠅁` | U+E0141 | always |
| `a` | `󰐠` | U+F0420 | at the start of a word |
| `i` | `󰐰` | U+F0430 | always |
| `i` | `󰐡` | U+F0421 | at the start of a word |
| `u` | `󰐳` | U+F0433 | always |
| `u` | `󰐢` | U+F0422 | at the start of a word |
| `e` | `󰐱` | U+F0431 | always |
| `e` | `󰐣` | U+F0423 | at the start of a word |
| `o` | `󰐴` | U+F0434 | always |
| `o` | `󰐤` | U+F0424 | at the start of a word |
| `ai` | `󰐲` | U+F0432 | always |
| `ai` | `󰐥` | U+F0425 | at the start of a word |
| `au` | `󰐵` | U+F0435 | always |
| `au` | `󰐦` | U+F0426 | at the start of a word |
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
| `?` | `󰑑󠄟󠇯` | U+F0451 U+E011F U+E01EF | always |
| `!` | `󰑑󠄁󠇯` | U+F0451 U+E0101 U+E01EF | always |
| `!!` | `󰑑󠄁󠄁󠇯` | U+F0451 U+E0101 U+E0101 U+E01EF | always |
| `-` | `󠄍` | U+E010D | always |
| `'` | `󰐸` | U+F0438 | always |
| `’` | `󰐸󠅛󠄒󠄐󠄑󠄙󠅝󠇯` | U+F0438 U+E015B U+E0112 U+E0110 U+E0111 U+E0119 U+E015D U+E01EF | always |

## Round trip

Every encoding round-trips exactly: decoding the code points that encoding wrote gives back the roman text, and encoding that gives the same code points. The Code points column shows every character a row writes, including any that is invisible.

This page is written from `encodings/vedyakshara.json` by `tools/encoding_docs.py`.
