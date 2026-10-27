# zethu encoding

Khelathi Zethu Glyphs is a right-to-left script of signs, set directly beside each other with nothing between them. This encoding accepts no roman letters: Khelathi words are written by the language-aware encoder, and a sign is written by its code between `⟦` and `⟧`, in the notation of the [zethu-mdc codage](zethu-mdc.md). Its word separator is empty: whitespace in roman draws nothing and writes nothing, so no output contains U+0020, and decoding gives the `⟦…⟧` codage alone.

## Fonts

- Khelathi Zethu Glyphs (`khelathi-zethu-glyphs`), written right to left.

## Running it

`encode.py` needs only Python 3.9 or later. From a checkout, or from `node_modules/@heroiclands/fonts`:

```sh
python3 encode.py --encoding zethu "⟦SERVANT SPEAK⟧"
python3 encode.py --encoding zethu --decode "󠄒𞩁𞩂󠄓"
```

The first command writes `󠄒𞩁𞩂󠄓`, and the second reads it back as `⟦SERVANT SPEAK⟧`. `--codepoints` prints the result as `U+XXXX` values, and the text may come from standard input.

From Python:

```python
import encode

text = encode.encode("zethu", "⟦SERVANT SPEAK⟧")
roman = encode.decode("zethu", text)
```

## Accepted characters

This encoding accepts (space), `!`, `,`, `.`, `/`, `?`, `^`, `{`, `}`, `«`, `»`, `—`, `…`, `‹`, `›`, `‼`, and the standard's marks and whitespace. Any other character is refused at its line and column.

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

This script sets its characters beside each other, so its `separator` is empty: a separator writes nothing. Decoding gives no space, only what the characters read as.

The separator is normalized on input, not preserved: `a  b` and `a\n\tb` encode as `a b` does, and decoding writes a single space.

With `--verse` or `encode(..., verse=True)`, a line ending writes the shared verse line control and a blank line writes the stanza control. `--- {.canto}` writes the canto control. See [standard.md](standard.md) for the structural assignments.

A character that no row matches is refused: `encode.py` reports it with its line and column, and writes nothing.

## Literal spans

`⟦` and `⟧` enclose this encoding's own codes or `U+XXXX` code points: `⟦U+00E1⟧` writes `á`. A scalar has four to six uppercase hexadecimal digits. `controls.literalEscape` quotes literal open, close and escape controls inside the payload. The file's `codes` rows give its named signs and notation; whitespace between codes only separates them. Other names and standard punctuation are refused.

## Vowels and conditions

Where several rows begin with the same roman, the longest wins, and among rows of one length a row whose condition holds comes before a row with none. A row whose condition fails is skipped.

## Rows

The rows are in the order the file states them. A row here for a standard mark replaces the standard's row for it.

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
| (space) | (nothing) | (none) | always |

## Round trip

Every encoding round-trips exactly: decoding the code points that encoding wrote gives back the roman text, and encoding that gives the same code points. The Code points column shows every character a row writes, including any that is invisible.

This page is written from `encodings/zethu.json` by `tools/encoding_docs.py`.
