---
"@heroiclands/fonts": minor
---

- **Shared punctuation.** Every encoding follows the same punctuation assignments, including `‼` for an imperative sentence and `!` for an exclamation. Invisible marks preserve sentence types, quotations and name boundaries when a script does not draw them.
- **Verse and spacing.** Ordinary whitespace becomes one word separator. Verse mode writes distinct line and stanza controls, `--- {.canto}` marks a canto boundary, and `^` supplies indentation.
- **Script punctuation.** Scripts retain their own visible sentence-end forms while sharing the punctuation meanings. Generic invisible spelling metadata remains distinct from the shared structural controls.
- **Capitals and keyboards.** Semaron Kuriale and Helónika write capitals as majuscules; other scripts accept lowercase Roman text, while codages retain their capital codes. Their layouts type capitals on Shift, the Semaron comma key types the point, and the caseless layouts leave shifted letter keys empty.
- **Literal characters.** All encodings accept exact characters between `⟦` and `⟧`, using shared non-printing boundaries and the active encoding's character names or codage. Whitespace separates codes, and a font without a Roman encoding accepts only literal spans.
- **Input and typing.** Unknown characters are refused at their line and column. All layouts type the literal markers on Option+Shift+W and Option+Shift+L, and HL Vedyakshara types independent vowels on Shift and the vowel key.
