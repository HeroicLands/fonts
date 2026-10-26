# Standard punctuation encoding

Every encoding follows this punctuation standard. It defines sentence endings,
pauses, quotation boundaries, verse separators, indentation, word spacing,
name boundaries and literal-span boundaries. The meanings and non-printing
code points are shared across encodings.

Each encoding defines its own letters, numerals, case forms, pronunciation
modifiers and codage. Those definitions belong in the individual encoding.

## Marks

| Mark | Meaning | Shared code point |
| --- | --- | --- |
| `.` | completes a declarative sentence, terminal | `\U000E0100` |
| `?` | completes an interrogative sentence, terminal | `\U000E0101` |
| `‼` | completes an imperative sentence, terminal | `\U000E0102` |
| `!` | completes an exclamative sentence, terminal | `\U000E0103` |
| `^` | at the beginning of a line, indents one level; repeat for further levels | `\U000E0104` |
| `,` | a pause that does not end the sentence | `\U000E0105` |
| `«` | opens an outer quotation | `\U000E0106` |
| `»` | closes the quotation opened by `«` | `\U000E0107` |
| `‹` | opens a quotation nested inside `«` and `»`; alternate pairs at further depths | `\U000E0108` |
| `›` | closes the quotation opened by `‹` | `\U000E0109` |
| `—` | interrupts a sentence; non-terminal and immediately followed by a terminal | `\U000E010A` |
| `…` | abandons a sentence; non-terminal and immediately followed by a terminal; at the start of a sentence, resumes one | `\U000E010B` |
| `/` or a verse line ending | separates verse lines | `\U000E010C` |
| a blank line in verse | separates verse stanzas | `\U000E010D` |
| `--- {.canto}` | separates verse cantos | `\U000E010E` |
| a run of word-separating whitespace | separates words | `\U00000020` |
| `{` | opens a name | `\U000E0110` |
| `}` | closes a name | `\U000E0111` |
| `⟦` | opens an immutable literal span | `\U000E0112` |
| `⟧` | closes an immutable literal span | `\U000E0113` |

The code points in this table are explicit assignments. An encoder does not
calculate them from the input mark's character code. Except for the word
space, they are non-printing structural marks.

## Sentence boundaries and quotation

A terminal records the kind of sentence it completes. A comma, interruption
mark, ellipsis or closing quotation mark does not replace a terminal.
The ellipsis is `…`, never three periods. An interruption or abandonment
mark is followed immediately by the appropriate terminal.

Quotation pairs must balance and nest. Alternate `« »` and `‹ ›` at successive
depths. A quotation may contain complete sentences. A quoted span that closes
without a terminal resumes as the same sentence in the next quoted span.
Closing a quotation does not terminate the surrounding sentence.

Name boundaries use `{` and `}`. They identify the extent of a name without
assigning its letters, capitalization or pronunciation.

## Whitespace, indentation and verse

Outside literal spans, a run of spaces or tabs between words represents one
word separator. A line ending in ordinary prose also represents word-separating
whitespace. Its original width and whitespace characters are not preserved.

In verse, a line ending represents a verse line separator, and a blank line
represents a stanza separator. An explicit `/` represents a verse line separator
in inline verse. A line containing `--- {.canto}` represents a canto separator.
These structural boundaries take precedence over ordinary whitespace
normalization; the line ending or blank line that supplies a separator does
not also supply a word separator.

At the beginning of a line, each `^` adds one indentation level. Indentation
uses its own mark, rather than periods or repeated word spaces. A line boundary
before indentation is retained as the line-separator control; its decoded
inline form is `/^`, so normalization does not discard the indentation context.

## Literal-span boundaries

`⟦` and `⟧` enclose an immutable literal span. The active encoding interprets
the enclosed codes according to its own codage or character-name rules.
This standard assigns the boundaries and leaves the enclosed character
inventory and notation to that encoding.

Inside a literal span, only that encoding's literal codes and notation are
allowed. Ordinary punctuation rules do not interpret its contents. Whitespace
between codes separates them; decoding uses single spaces between codes.
Outside a literal span, codage codes have no special meaning.

## Requirements for individual encodings

Every encoding accepts these punctuation and structural marks. An encoding
may provide a visible script-specific form for a mark, or carry its shared
non-printing code point. Its definition states which marks it draws and how
it preserves their meanings. When several marks share a visible form, the
encoded text must retain enough information to distinguish them on decoding.

An encoding's letter and numeral rows must preserve these punctuation
meanings. A language's writing conventions may use only a subset of the
marks; that usage does not change the shared standard.
