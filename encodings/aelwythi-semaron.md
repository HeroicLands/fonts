# aelwythi-semaron encoding

Aelwythi has its own encoding in the Semaron Kuriale hand. Coined words use the fixed Aelwythi letter groups: ch, sh, th, dh, kh, gh, zh, ts and ng have dedicated signs, and ny takes its dedicated sign before a vowel. A group is lowercase, as in ch, or initial-uppercase, as in Ch; CH and cH are illegal. The letter q has its own sign, and y is always a consonant. There are no automatic c or x substitutions.

An acute vowel writes its ordinary vowel sign followed by the non-printing stress modifier U+E0114. Stress does not change vowel sound or length. Coined words use no diaeresis or grave accent. Doubled vowels remain two written signs.

Only a period draws the pause point. Quotation marks and apostrophes draw nothing, and a hyphen writes a space. Decoding returns a conventional Roman spelling: omitted punctuation is not restored, and a hyphen reads back as a word space. Other Semaron encodings keep their own rules.

The twenty newly assigned consonant glyph designs are pending. Their code-point assignments are reserved, and native rendering remains blocked until the drawings are supplied.

## Fonts

- Semaron Kuriale (`semaron-kuriale`), written left to right.

## Running it

`encode.py` needs only Python 3.9 or later. From a checkout, or from `node_modules/@heroiclands/fonts`:

```sh
python3 encode.py --encoding aelwythi-semaron "thalen kal"
python3 encode.py --encoding aelwythi-semaron --decode "󰉐󰈰󰈺󰈳󰈼 󰈹󰈰󰈺"
```

The first command writes `󰉐󰈰󰈺󰈳󰈼 󰈹󰈰󰈺`, and the second reads it back as `thalen kal`. `--codepoints` prints the result as `U+XXXX` values, and the text may come from standard input.

From Python:

```python
import encode

text = encode.encode("aelwythi-semaron", "thalen kal")
roman = encode.decode("aelwythi-semaron", text)
```

## Accepted characters

This encoding accepts `a-z`, `A-Z`, `0-9`, `'`, `-`, `` ` ``, `Á`, `É`, `Í`, `Ó`, `Ú`, `á`, `é`, `í`, `ó`, `ú`, `‐`, `‑`, `’`, `.`, `"`, `“`, `”`, `«`, `»`, `‘`, and the standard's marks and whitespace. Any other character is refused at its line and column.

## Punctuation

This encoding inherits punctuation rows from standard.json, with the replacements listed below. A replacement may omit a mark; decoding then cannot restore it. The shared assignments are defined in [standard.md](standard.md).

| Mark | Meaning | Written | Code points |
| --- | --- | --- | --- |
| `.` | completes a declarative sentence, terminal | drawn, `󰉨` | U+F0268 |
| `?` | completes an interrogative sentence, terminal | invisible | U+E0101 |
| `‼` | completes an imperative sentence, terminal | invisible | U+E0102 |
| `!` | completes an exclamative sentence, terminal | invisible | U+E0103 |
| `^` | at the beginning of a line, indents one level | invisible | U+E0104 |
| `,` | a pause that does not end the sentence | invisible | U+E0105 |
| `«` | opens an outer quotation | invisible | (none) |
| `»` | closes an outer quotation | invisible | (none) |
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

The vowels are `AEIOUaeiouÁÉÍÓÚáéíóú`.

A row marked _before a vowel_ applies when the next character is a vowel.

Where several rows begin with the same roman, the longest wins, and among rows of one length a row whose condition holds comes before a row with none. A row whose condition fails is skipped.

## Rows

The rows are in the order the file states them. A row here for a standard mark replaces the standard's row for it.

| Roman | Character | Code points | When |
| --- | --- | --- | --- |
| `ny` | `󰊐` | U+F0290 | before a vowel |
| `Ny` | `󰊑` | U+F0291 | before a vowel |
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
| `a` | `󰈰` | U+F0230 | always |
| `A` | `󰈀` | U+F0200 | always |
| `b` | `󰈱` | U+F0231 | always |
| `B` | `󰈁` | U+F0201 | always |
| `d` | `󰈲` | U+F0232 | always |
| `D` | `󰈂` | U+F0202 | always |
| `e` | `󰈳` | U+F0233 | always |
| `E` | `󰈃` | U+F0203 | always |
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
| `q` | `󰉇` | U+F0247 | always |
| `Q` | `󰈗` | U+F0217 | always |
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
| `y` | `󰉅` | U+F0245 | always |
| `Y` | `󰈕` | U+F0215 | always |
| `z` | `󰉆` | U+F0246 | always |
| `Z` | `󰈖` | U+F0216 | always |
| `á` | `󰈰󠄔` | U+F0230 U+E0114 | always |
| `Á` | `󰈀󠄔` | U+F0200 U+E0114 | always |
| `é` | `󰈳󠄔` | U+F0233 U+E0114 | always |
| `É` | `󰈃󠄔` | U+F0203 U+E0114 | always |
| `í` | `󰈷󠄔` | U+F0237 U+E0114 | always |
| `Í` | `󰈇󠄔` | U+F0207 U+E0114 | always |
| `ó` | `󰈽󠄔` | U+F023D U+E0114 | always |
| `Ó` | `󰈍󠄔` | U+F020D U+E0114 | always |
| `ú` | `󰉂󠄔` | U+F0242 U+E0114 | always |
| `Ú` | `󰈒󠄔` | U+F0212 U+E0114 | always |
| `.` | `󰉨` | U+F0268 | always |
| `"` | (nothing) | (none) | always |
| `“` | (nothing) | (none) | always |
| `”` | (nothing) | (none) | always |
| `«` | (nothing) | (none) | always |
| `»` | (nothing) | (none) | always |
| `'` | (nothing) | (none) | always |
| `’` | (nothing) | (none) | always |
| `‘` | (nothing) | (none) | always |
| `` ` `` | (nothing) | (none) | always |
| `-` | (space) | U+0020 | always |
| `‐` | (space) | U+0020 | always |
| `‑` | (space) | U+0020 | always |
| `ch` | `󰊌` | U+F028C | always |
| `Ch` | `󰊍` | U+F028D | always |
| `sh` | `󰊆` | U+F0286 | always |
| `Sh` | `󰊇` | U+F0287 | always |
| `th` | `󰉐` | U+F0250 | always |
| `Th` | `󰉑` | U+F0251 | always |
| `dh` | `󰊀` | U+F0280 | always |
| `Dh` | `󰊁` | U+F0281 | always |
| `kh` | `󰊂` | U+F0282 | always |
| `Kh` | `󰊃` | U+F0283 | always |
| `gh` | `󰊄` | U+F0284 | always |
| `Gh` | `󰊅` | U+F0285 | always |
| `zh` | `󰊈` | U+F0288 | always |
| `Zh` | `󰊉` | U+F0289 | always |
| `ts` | `󰊊` | U+F028A | always |
| `Ts` | `󰊋` | U+F028B | always |
| `ng` | `󰊎` | U+F028E | always |
| `Ng` | `󰊏` | U+F028F | always |

## Round trip

This encoding decodes to a conventional Roman spelling. Omitted punctuation is not restored, and rows that write the word separator decode as a space. It does not preserve the exact source spelling or promise an exact code-point round trip. The Code points column shows every character each row writes.

This page is written from `encodings/aelwythi-semaron.json` by `tools/encoding_docs.py`.
