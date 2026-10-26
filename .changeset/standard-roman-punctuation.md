---
"@heroiclands/fonts": minor
---

- **One roman punctuation.** Every encoding shares the standard roman marks: `.` `?` `!` `!!` `,`, the quotation marks `« »` and `‹ ›`, `—`, `…`, `/`, `//` and `***` for verse line, stanza and canto ends, and `{ }` around a name. A mark a script does not draw is kept as invisible characters, so decoding gives it back.
- **Whitespace.** In roman, any run of spaces, tabs and line breaks is one word separator. A script that spaces its words writes one space for it; Khelathi Zethu, which sets its signs beside each other, writes nothing, and decoding gives one space.
- **Sentence ends.** Pirzath, Thuravark, Helónika, Qalezu and Vedyakshara draw `?`, `!` and `!!` as their one sentence end, as Semaron draws its point for every sentence end and pause.
- **Script marks.** Pirzath's `!` draws the sentence end, its quotation marks are typed `« »`, and Qalezu's verse dot is typed `/`, or `//` at a stanza end.
- **Capitals.** Semaron Kuriale and Helónika have case: their encodings write a capital letter as its majuscule, and HL Semaron and HL Helónika type it on Shift. Every other script is caseless and accepts only lowercase roman, refusing a capital, names included; the Zethu and Ch'alish codages keep their capital codes.
- **Literal characters.** Every encoding writes exact characters between `⟦` and `⟧`, named by their Unicode names in capitals with `_` for spaces, or by a script's own codes where the encoding states a codage; whitespace between codes only separates them, a standard mark inside is refused, and decoding gives the span back with single spaces. A font with no encoding accepts text only between the markers.
- **Unknown characters are refused.** `encode.py` stops at a character its encoding does not know and reports its line and column, rather than passing it through.
- **Typing the markers.** Every layout types `⟦` and `⟧` on Option+Shift+W and Option+Shift+L, and HL Vedyakshara types the independent vowels on Shift and the vowel key.
- **Keyboards.** Shift on a letter key types the majuscule in HL Semaron and HL Helónika and nothing in the caseless layouts, and the Semaron comma key types the point.
