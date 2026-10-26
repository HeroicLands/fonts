# standard roman encoding

Roman transliteration has one standard punctuation, used by every language, scripted or not. Its marks record the type of a sentence, the bounds of a quotation and the ends of verse lines and stanzas. Every encoding extends this one, `encodings/standard.json`, and adds its script's letters, numerals and the other characters its language writes.

Roman is typed in lowercase, and a caseless script accepts only lowercase: its encoding refuses a capital letter, names included. Semaron Kuriale and Helónika are the two scripts with case, and their encodings write a capital letter as its majuscule, with no mark for case. A codage, which names each sign by a code, keeps its codes in capitals. `{` and `}` surround a name, and a script may mark the name in its own way. `…` is the ellipsis character, never three periods. A quoted span that closes without a terminal is resumed by the next span as the same sentence, and a closing quote never terminates the outer sentence. In verse, a line beginning with `.` is indented one level per period.

## Marks

| Mark | Meaning | Invisible mark |
| --- | --- | --- |
| `.` | completes a declarative sentence, terminal | U+E010E |
| `?` | completes an interrogative sentence, terminal | U+E011F |
| `!` | completes an imperative sentence, terminal | U+E0101 |
| `!!` | completes an exclamative sentence, terminal | U+E0101 U+E0101 |
| `,` | a pause that does not end the sentence | U+E010C |
| `«` | opens a quotation of one or more terminated sentences | U+E015B U+E0141 U+E0142 U+E015D |
| `»` | closes a quotation opened by `«` | U+E015B U+E0142 U+E0142 U+E015D |
| `‹` | opens a quotation nested inside `«` `»`, alternating with them at any depth | U+E015B U+E0112 U+E0110 U+E0113 U+E0119 U+E015D |
| `›` | closes a quotation opened by `‹` | U+E015B U+E0112 U+E0110 U+E0113 U+E0141 U+E015D |
| `—` | interrupts a sentence, non-terminal, immediately followed by a terminal | U+E015B U+E0112 U+E0110 U+E0111 U+E0114 U+E015D |
| `…` | abandons a sentence, non-terminal and immediately followed by a terminal; at a sentence's start, resumes one | U+E015B U+E0112 U+E0110 U+E0112 U+E0116 U+E015D |
| `/` | verse line end | U+E010F |
| `//` | verse stanza end | U+E010F U+E010F |
| `***` | verse canto end | U+E010A U+E010A U+E010A |
| `{` | opens a name | U+E015B U+E0117 U+E0142 U+E015D |
| `}` | closes a name opened by `{` | U+E015D |

Each invisible mark is the mark rule's spelling of the mark's own characters, in the variation selectors U+E0100 to U+E015E: a printable ASCII character `c` is U+E0100 + (`c` − U+0020), and any other character is spelled as `{`, its code point in lowercase hex, and `}`. A script that does not draw a mark writes this sequence, so the mark is written alike in every encoding and decoding restores it. A script that draws a mark replaces the row with its own.

Where two marks begin alike, the longer is matched first: `!!` before `!`, and `//` before `/`. `***`, the canto end, is an invisible mark by default, and a script draws it only where its design note says so.

## Literal spans

`⟦` and `⟧` (U+27E6, U+27E7) are the literal immutable markers. What they enclose names exact characters, which no encoder reinterprets, so a writer can force one character, such as a homophone the lexicon would not choose. Every encoding supports them. Each marker is written as the invisible mark of itself, U+E015B U+E0112 U+E0117 U+E0145 U+E0116 U+E015D and U+E015B U+E0112 U+E0117 U+E0145 U+E0117 U+E015D, the same in every encoding.

Without a `codage`, the codes are character names in capitals, with each space of a name written `_`, separated by whitespace: `⟦LATIN_SMALL_LETTER_A_WITH_ACUTE LATIN_SMALL_LETTER_I LATIN_SMALL_LETTER_M⟧` writes `áim`. The names of the script fonts' characters are in `encodings/names.json`, written by `tools/encoding_names.py` from `tools/names`; every other character is named by Unicode. Decoding names each character between the marker marks and separates the codes with single spaces.

An encoding that states `"codage": "<name>"` encodes and decodes the span through that codage instead, so the codes are the codage's own, as `⟦WONG_YELLOW⟧` in the Zethu script. A codage is a file of kind `codage`, `encodings/<name>.json`: it extends nothing, encodes no text of its own and is reached only through the markers of the encoding that states it. Inside the markers only the codes and the codage's own notation are allowed (Zethu's joiners `-` `:` `*`, its brackets and `[ts]`), never a standard mark: a `,` or `?` inside is an error at its position. A code outside the markers is ordinary roman, never read as a code.

Whitespace inside the markers is ignored. Any amount of space, newline or tab between codes is a separator only and is not saved, so `⟦ONE TWO THREE⟧` and the same codes with runs of whitespace between them are the same text. Decoding always writes single spaces between codes. This is the normalization, not a loss.

A name that names no character, an unmatched `⟦` or `⟧`, and a marker inside a span are refused at the offending position, as are a marker mark in the same cases in decoding.

A script with no encoding file accepts no roman at all: its text is written only as character names between the markers, and anything outside them is an error. `encode.py --font <slug>` addresses such a font.

## Whitespace

In roman, outside `⟦` and `⟧`, any run of whitespace (space, tab, newline, carriage return) is one word separator. It is not a character of the script and has no row: the standard states none. `this      is \t\t\n\t a   test` encodes like `this is a test`.

Each encoding states how its script writes the separator with `separator`, a required string:

- A script that spaces its words (Semaron Kuriale, Helónika, Pirzath, Qalezu, Thuravark, Vedyakshara, Veldikko and Ch'alish Pilam) states `" "`, one U+0020 for each separator. Ch'alish writes its space as one empty cell. A script with a glyph of its own for the word space may state that glyph.
- A script that sets its characters beside each other states `""` and writes nothing. Khelathi Zethu is one: it accepts nothing outside `⟦` and `⟧`, so its decoding gives the `⟦…⟧` codage alone. Teng Chou is the other: it has no encoding file, it writes nothing for a separator, and its decoding puts a space after each character's word, since one character is a word or a phrase.

The separator is normalized on input, not preserved. Encoding writes it once for a whole run, and decoding writes a single space (nothing for an empty separator), so a round trip gives the roman back with each run of whitespace as one space. Whitespace inside `⟦` and `⟧` only separates codes, and decoding writes single spaces there too.

A newline is only whitespace in the encodings. The structure of verse is the work of the build that reads a verse fence: inside it a newline is `/`, a blank line is `//`, and a line of only `***` is a canto break, `***`. Outside verse, verse quoted in prose writes `/`, `//` and `***` explicitly.

## Extending it

An encoding builds on the standard with `"extends": "standard"`. Its rows are the standard's rows whose roman it does not state, in the standard's order, followed by its own rows. Nothing else is inherited, so the two files together are the whole encoding, and any implementation can apply it from them alone.

An encoding declares the characters it accepts as roman with `accepts`, a list of characters and ranges such as `"a-z"`. A caseless script lists `a-z` and its own additions, and Semaron and Helónika, the scripts with case, list `a-zA-Z` and theirs. The standard's marks and whitespace are accepted besides, and every `from` is made of accepted characters.

A character that is in neither the standard nor the encoding's rows is refused: `encode.py` reports it as `file:line:column: error:` and exits non-zero, and decoding refuses a code point no row writes in the same way.

This page is written from `encodings/standard.json` by `tools/encoding_docs.py`.
