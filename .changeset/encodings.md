---
"@heroiclands/fonts": patch
---

- **Encodings.** The package ships an encoding for each script font in `encodings/`, with a page describing each one. `encode.py` turns roman text into a font's characters and reads them back exactly, needing only Python 3.9 or later.
- **Khelathi Zethu codes.** Every Khelathi Zethu sign has a code naming its sense, such as `SAIL` or `REGNAL_YEAR`. Its encoding is typed with these codes instead of sign numbers.
- **Keyboards.** The Semaron comma key types nothing. In Veldikko, the sh key types two letters, and an accented vowel types the emphasis sign with its vowel.
