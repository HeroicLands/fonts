# teng-chou encoding

Teng Chou is a logographic script of the Tantsou: one character for each morpheme, with a syllabary of 87 signs for particles, verb endings and island words. Its characters are set directly beside each other, with nothing between them. This encoding accepts no roman letters: Tantsou words are turned into characters by the language-aware encoder, and a character is written by its code between `⟦` and `⟧`, in the notation of the [teng-chou-codes codage](teng-chou-codes.md). Its word separator is empty: whitespace in roman draws nothing and writes nothing, so no output contains U+0020.

## Fonts

- Teng Chou (`teng-chou`), written left to right.

## Running it

`encode.py` needs only Python 3.9 or later. From a checkout, or from `node_modules/@heroiclands/fonts`:

```sh
python3 encode.py --encoding teng-chou "⟦WONG TALLY3 ka⟧"
python3 encode.py --encoding teng-chou --decode "󠄒󱀌󱃗󲀅󠄓"
```

The first command writes `󠄒󱀌󱃗󲀅󠄓`, and the second reads it back as `⟦WONG TALLY3 ka⟧`. `--codepoints` prints the result as `U+XXXX` values, and the text may come from standard input.

From Python:

```python
import encode

text = encode.encode("teng-chou", "⟦WONG TALLY3 ka⟧")
roman = encode.decode("teng-chou", text)
```

## Accepted characters

This encoding accepts no roman letters, only the standard's marks and whitespace. Anything else outside `⟦` and `⟧` is refused at its line and column.

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

This script sets its characters beside each other, so its `separator` is empty: a separator writes nothing. Decoding gives no space, only what the characters read as.

The separator is normalized on input, not preserved: `a  b` and `a\n\tb` encode as `a b` does, and decoding writes a single space.

With `--verse` or `encode(..., verse=True)`, a line ending writes the shared verse line control and a blank line writes the stanza control. `--- {.canto}` writes the canto control. See [standard.md](standard.md) for the structural assignments.

A character that no row matches is refused: `encode.py` reports it with its line and column, and writes nothing.

## Literal spans

`⟦` and `⟧` enclose codes of the [teng-chou-codes codage](teng-chou-codes.md), which encodes and decodes the span, as the [standard](standard.md) describes. Only the codage's codes and its notation are allowed inside, no standard mark, and whitespace between codes only separates them. A code outside the markers is ordinary roman.

## Vowels and conditions

Where several rows begin with the same roman, the longest wins, and among rows of one length a row whose condition holds comes before a row with none. A row whose condition fails is skipped.

## Rows

The encoding states no rows of its own: the standard's rows are the whole encoding.

## Round trip

Every encoding round-trips exactly: decoding the code points that encoding wrote gives back the roman text, and encoding that gives the same code points. The Code points column shows every character a row writes, including any that is invisible.

This page is written from `encodings/teng-chou.json` by `tools/encoding_docs.py`.
