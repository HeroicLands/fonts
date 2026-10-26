# chalish-pilam-ceremonial encoding

Chalish Pilam Ceremonial is the carved hand of Ch'alish P'ilam, a logographic script whose glyphs compose into blocks. This encoding accepts no roman letters: a glyph or a block is written by its codes between `⟦` and `⟧`, in the notation of the [chalish-ceremonial codage](chalish-ceremonial.md). Its word separator is one space, an empty block.

## Fonts

- Chalish Pilam Ceremonial (`chalish-pilam-ceremonial`), written left to right.

## Running it

`encode.py` needs only Python 3.9 or later. From a checkout, or from `node_modules/@heroiclands/fonts`:

```sh
python3 encode.py --encoding chalish-pilam-ceremonial "⟦n13*TQAN DAWN⟧"
python3 encode.py --encoding chalish-pilam-ceremonial --decode "󠅛󠄒󠄗󠅅󠄖󠅝󴀍󴿰󴀧󴂄󠅛󠄒󠄗󠅅󠄗󠅝"
```

The first command writes `󠅛󠄒󠄗󠅅󠄖󠅝󴀍󴿰󴀧󴂄󠅛󠄒󠄗󠅅󠄗󠅝`, and the second reads it back as `⟦n13*TQAN DAWN⟧`. `--codepoints` prints the result as `U+XXXX` values, and the text may come from standard input.

From Python:

```python
import encode

text = encode.encode("chalish-pilam-ceremonial", "⟦n13*TQAN DAWN⟧")
roman = encode.decode("chalish-pilam-ceremonial", text)
```

## Accepted characters

This encoding accepts no roman letters, only the standard's marks and whitespace. Anything else outside `⟦` and `⟧` is refused at its line and column.

## Punctuation

This encoding extends the [standard roman encoding](standard.md), which every language's roman shares. The table shows how this script writes each standard mark. A mark the script draws writes its glyph; a mark it does not draw writes the standard's invisible mark, the same in every encoding, so decoding restores it.

| Mark | Meaning | Written | Code points |
| --- | --- | --- | --- |
| `.` | completes a declarative sentence, terminal | invisible | U+E010E |
| `?` | completes an interrogative sentence, terminal | invisible | U+E011F |
| `!` | completes an imperative sentence, terminal | invisible | U+E0101 |
| `!!` | completes an exclamative sentence, terminal | invisible | U+E0101 U+E0101 |
| `,` | a pause that does not end the sentence | invisible | U+E010C |
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

`⟦` and `⟧` enclose codes of the [chalish-ceremonial codage](chalish-ceremonial.md), which encodes and decodes the span, as the [standard](standard.md) describes. Only the codage's codes and its notation are allowed inside, no standard mark, and whitespace between codes only separates them. A code outside the markers is ordinary roman.

## Rows

The encoding states no rows of its own: the standard's rows are the whole encoding.

## Round trip

Every encoding round-trips exactly: decoding the code points that encoding wrote gives back the roman text, and encoding that gives the same code points. The Code points column shows every character a row writes, including any that is invisible.

This page is written from `encodings/chalish-pilam-ceremonial.json` by `tools/encoding_docs.py`.
