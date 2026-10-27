# semaron encoding

Semaron Kuriale is an alphabet of capital and small letters, written left to right. This encoding writes a roman spelling in its small letters, and a capital letter in its majuscule: `th`, `dh`, `kh`, `gh`, `sh`, `zh`, `ts`, `ch` and `ng` are each one letter, read left to right, so `tch` is t and `ch` and `ngh` is `ng` and h; `ny` before a vowel is one letter and anywhere else is n and the vowel i; `q` is a letter of its own; a doubled `a`, `i` or `u` is a long vowel; and `y` before a vowel is a glide. An apostrophe or hyphen after a letter writes the catch, a mark on the letter before it.

## Fonts

- Semaron Kuriale (`semaron-kuriale`), written left to right.

## Running it

`encode.py` needs only Python 3.9 or later. From a checkout, or from `node_modules/@heroiclands/fonts`:

```sh
python3 encode.py --encoding semaron "thalen kaa"
python3 encode.py --encoding semaron --decode "󰉐󰈰󰈺󰈳󰈼 󰈹󰉈"
```

The first command writes `󰉐󰈰󰈺󰈳󰈼 󰈹󰉈`, and the second reads it back as `thalen kaa`. `--codepoints` prints the result as `U+XXXX` values, and the text may come from standard input.

From Python:

```python
import encode

text = encode.encode("semaron", "thalen kaa")
roman = encode.decode("semaron", text)
```

## Accepted characters

This encoding accepts `a-z`, `A-Z`, `0-9`, `'`, `-`, `` ` ``, `À`, `Á`, `É`, `Ë`, `Í`, `Ó`, `Ú`, `Ý`, `à`, `á`, `é`, `ë`, `í`, `ó`, `ú`, `ý`, `’`, (space), `!`, `,`, `.`, `/`, `?`, `^`, `{`, `}`, `«`, `»`, `—`, `…`, `‹`, `›`, `‼`, and the standard's marks and whitespace. Any other character is refused at its line and column.

## Punctuation

This encoding includes the [standard roman punctuation](standard.md), which every language's roman shares. The table shows how this script writes each standard mark. A mark the script draws writes its glyph; a mark it does not draw writes the standard's invisible mark, the same in every encoding, so decoding restores it.

| Mark | Meaning | Written | Code points |
| --- | --- | --- | --- |
| `.` | completes a declarative sentence, terminal | drawn, `󰉨` | U+F0268 |
| `?` | completes an interrogative sentence, terminal | drawn, `󰉨` | U+F0268 U+E0101 U+E01EF |
| `‼` | completes an imperative sentence, terminal | drawn, `󰉨` | U+F0268 U+E0102 U+E01EF |
| `!` | completes an exclamative sentence, terminal | drawn, `󰉨` | U+F0268 U+E0103 U+E01EF |
| `^` | at the beginning of a line, indents one level | invisible | U+E0104 |
| `,` | a pause that does not end the sentence | drawn, `󰉨` | U+F0268 U+E0105 U+E01EF |
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

This script spaces its words, so its `separator` is one space, U+0020: a separator writes one space, and decoding writes one space.

The separator is normalized on input, not preserved: `a  b` and `a\n\tb` encode as `a b` does, and decoding writes a single space.

With `--verse` or `encode(..., verse=True)`, a line ending writes the shared verse line control and a blank line writes the stanza control. `--- {.canto}` writes the canto control. See [standard.md](standard.md) for the structural assignments.

A character that no row matches is refused: `encode.py` reports it with its line and column, and writes nothing.

## Literal spans

`⟦` and `⟧` enclose this encoding's own codes or `U+XXXX` code points: `⟦U+00E1⟧` writes `á`. A scalar has four to six uppercase hexadecimal digits. `controls.literalEscape` quotes literal open, close and escape controls inside the payload. The file's `codes` rows give its named signs and notation; whitespace between codes only separates them. Other names and standard punctuation are refused.

## Vowels and conditions

The vowels are `AEIOUaeiouÀÁÉËÍÓÚàáéëíóú`.

A row marked _before a vowel_ applies when the next character is a vowel.

Where several rows begin with the same roman, the longest wins, and among rows of one length a row whose condition holds comes before a row with none. A row whose condition fails is skipped.

## Rows

The rows are in the order the file states them. A row here for a standard mark replaces the standard's row for it.

| Roman | Character | Code points | When |
| --- | --- | --- | --- |
| `^` | `󠄄` | U+E0104 | at the beginning of a line |
| `«` | `󠄆` | U+E0106 | always |
| `»` | `󠄇` | U+E0107 | always |
| `‹` | `󠄈` | U+E0108 | always |
| `›` | `󠄉` | U+E0109 | always |
| `—` | `󠄊` | U+E010A | always |
| `…` | `󠄋` | U+E010B | always |
| `/` | `󠄌` | U+E010C | always |
| `{` | `󠄐` | U+E0110 | always |
| `}` | `󠄑` | U+E0111 | always |
| `tà` | `󰉁󰉰󰈰󠅔󠅛󠅅󠄐󠅝󠇯` | U+F0241 U+F0270 U+F0230 U+E0154 U+E015B U+E0145 U+E0110 U+E015D U+E01EF | always |
| `tÀ` | `󰉁󰉰󰈀󠅔󠅛󠅃󠄐󠅝󠇯` | U+F0241 U+F0270 U+F0200 U+E0154 U+E015B U+E0143 U+E0110 U+E015D U+E01EF | always |
| `Tà` | `󰈑󰉰󰈰󠄴󠅛󠅅󠄐󠅝󠇯` | U+F0211 U+F0270 U+F0230 U+E0134 U+E015B U+E0145 U+E0110 U+E015D U+E01EF | always |
| `TÀ` | `󰈑󰉰󰈀󠄴󠅛󠅃󠄐󠅝󠇯` | U+F0211 U+F0270 U+F0200 U+E0134 U+E015B U+E0143 U+E0110 U+E015D U+E01EF | always |
| `kà` | `󰈹󰉰󰈰󠅋󠅛󠅅󠄐󠅝󠇯` | U+F0239 U+F0270 U+F0230 U+E014B U+E015B U+E0145 U+E0110 U+E015D U+E01EF | always |
| `kÀ` | `󰈹󰉰󰈀󠅋󠅛󠅃󠄐󠅝󠇯` | U+F0239 U+F0270 U+F0200 U+E014B U+E015B U+E0143 U+E0110 U+E015D U+E01EF | always |
| `Kà` | `󰈉󰉰󰈰󠄫󠅛󠅅󠄐󠅝󠇯` | U+F0209 U+F0270 U+F0230 U+E012B U+E015B U+E0145 U+E0110 U+E015D U+E01EF | always |
| `KÀ` | `󰈉󰉰󰈀󠄫󠅛󠅃󠄐󠅝󠇯` | U+F0209 U+F0270 U+F0200 U+E012B U+E015B U+E0143 U+E0110 U+E015D U+E01EF | always |
| `dà` | `󰈲󰉰󰈰󠅄󠅛󠅅󠄐󠅝󠇯` | U+F0232 U+F0270 U+F0230 U+E0144 U+E015B U+E0145 U+E0110 U+E015D U+E01EF | always |
| `dÀ` | `󰈲󰉰󰈀󠅄󠅛󠅃󠄐󠅝󠇯` | U+F0232 U+F0270 U+F0200 U+E0144 U+E015B U+E0143 U+E0110 U+E015D U+E01EF | always |
| `Dà` | `󰈂󰉰󰈰󠄤󠅛󠅅󠄐󠅝󠇯` | U+F0202 U+F0270 U+F0230 U+E0124 U+E015B U+E0145 U+E0110 U+E015D U+E01EF | always |
| `DÀ` | `󰈂󰉰󰈀󠄤󠅛󠅃󠄐󠅝󠇯` | U+F0202 U+F0270 U+F0200 U+E0124 U+E015B U+E0143 U+E0110 U+E015D U+E01EF | always |
| `gà` | `󰈵󰉰󰈰󠅇󠅛󠅅󠄐󠅝󠇯` | U+F0235 U+F0270 U+F0230 U+E0147 U+E015B U+E0145 U+E0110 U+E015D U+E01EF | always |
| `gÀ` | `󰈵󰉰󰈀󠅇󠅛󠅃󠄐󠅝󠇯` | U+F0235 U+F0270 U+F0200 U+E0147 U+E015B U+E0143 U+E0110 U+E015D U+E01EF | always |
| `Gà` | `󰈅󰉰󰈰󠄧󠅛󠅅󠄐󠅝󠇯` | U+F0205 U+F0270 U+F0230 U+E0127 U+E015B U+E0145 U+E0110 U+E015D U+E01EF | always |
| `GÀ` | `󰈅󰉰󰈀󠄧󠅛󠅃󠄐󠅝󠇯` | U+F0205 U+F0270 U+F0200 U+E0127 U+E015B U+E0143 U+E0110 U+E015D U+E01EF | always |
| `à` | `󰈰󰉰󠅛󠅅󠄐󠅝󠇯` | U+F0230 U+F0270 U+E015B U+E0145 U+E0110 U+E015D U+E01EF | always |
| `À` | `󰈀󰉰󠅛󠅃󠄐󠅝󠇯` | U+F0200 U+F0270 U+E015B U+E0143 U+E0110 U+E015D U+E01EF | always |
| `a` | `󰈰` | U+F0230 | always |
| `A` | `󰈀` | U+F0200 | always |
| `b` | `󰈱` | U+F0231 | always |
| `B` | `󰈁` | U+F0201 | always |
| `d` | `󰈲` | U+F0232 | always |
| `D` | `󰈂` | U+F0202 | always |
| `e` | `󰈳` | U+F0233 | always |
| `ë` | `󰈳󠅛󠅅󠅂󠅝󠇯` | U+F0233 U+E015B U+E0145 U+E0142 U+E015D U+E01EF | always |
| `E` | `󰈃` | U+F0203 | always |
| `Ë` | `󰈃󠅛󠅃󠅂󠅝󠇯` | U+F0203 U+E015B U+E0143 U+E0142 U+E015D U+E01EF | always |
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
| `z` | `󰉆` | U+F0246 | always |
| `Z` | `󰈖` | U+F0216 | always |
| `á` | `󰈰󠅛󠅅󠄑󠅝󠇯` | U+F0230 U+E015B U+E0145 U+E0111 U+E015D U+E01EF | always |
| `Á` | `󰈀󠅛󠅃󠄑󠅝󠇯` | U+F0200 U+E015B U+E0143 U+E0111 U+E015D U+E01EF | always |
| `é` | `󰈳󠅛󠅅󠄙󠅝󠇯` | U+F0233 U+E015B U+E0145 U+E0119 U+E015D U+E01EF | always |
| `É` | `󰈃󠅛󠅃󠄙󠅝󠇯` | U+F0203 U+E015B U+E0143 U+E0119 U+E015D U+E01EF | always |
| `í` | `󰈷󠅛󠅅󠅄󠅝󠇯` | U+F0237 U+E015B U+E0145 U+E0144 U+E015D U+E01EF | always |
| `Í` | `󰈇󠅛󠅃󠅄󠅝󠇯` | U+F0207 U+E015B U+E0143 U+E0144 U+E015D U+E01EF | always |
| `ó` | `󰈽󠅛󠅆󠄓󠅝󠇯` | U+F023D U+E015B U+E0146 U+E0113 U+E015D U+E01EF | always |
| `Ó` | `󰈍󠅛󠅄󠄓󠅝󠇯` | U+F020D U+E015B U+E0144 U+E0113 U+E015D U+E01EF | always |
| `ú` | `󰉂󠅛󠅆󠅁󠅝󠇯` | U+F0242 U+E015B U+E0146 U+E0141 U+E015D U+E01EF | always |
| `Ú` | `󰈒󠅛󠅄󠅁󠅝󠇯` | U+F0212 U+E015B U+E0144 U+E0141 U+E015D U+E01EF | always |
| `th` | `󰉐` | U+F0250 | always |
| `Th` | `󰉑` | U+F0251 | always |
| `ch` | `󰊌` | U+F028C | always |
| `Ch` | `󰊍` | U+F028D | always |
| `dh` | `󰊀` | U+F0280 | always |
| `Dh` | `󰊁` | U+F0281 | always |
| `kh` | `󰊂` | U+F0282 | always |
| `Kh` | `󰊃` | U+F0283 | always |
| `gh` | `󰊄` | U+F0284 | always |
| `Gh` | `󰊅` | U+F0285 | always |
| `sh` | `󰊆` | U+F0286 | always |
| `Sh` | `󰊇` | U+F0287 | always |
| `zh` | `󰊈` | U+F0288 | always |
| `Zh` | `󰊉` | U+F0289 | always |
| `ts` | `󰊊` | U+F028A | always |
| `Ts` | `󰊋` | U+F028B | always |
| `ng` | `󰊎` | U+F028E | always |
| `Ng` | `󰊏` | U+F028F | always |
| `ny` | `󰊐` | U+F0290 | before a vowel |
| `Ny` | `󰊑` | U+F0291 | before a vowel |
| `aa` | `󰉈` | U+F0248 | always |
| `aá` | `󰉈󠅁󠅛󠅅󠄑󠅝󠇯` | U+F0248 U+E0141 U+E015B U+E0145 U+E0111 U+E015D U+E01EF | always |
| `áa` | `󰉈󠅛󠅅󠄑󠅝󠅁󠇯` | U+F0248 U+E015B U+E0145 U+E0111 U+E015D U+E0141 U+E01EF | always |
| `áá` | `󰉈󠅛󠅅󠄑󠅝󠅛󠅅󠄑󠅝󠇯` | U+F0248 U+E015B U+E0145 U+E0111 U+E015D U+E015B U+E0145 U+E0111 U+E015D U+E01EF | always |
| `Aa` | `󰈠` | U+F0220 | always |
| `Aá` | `󰈠󠄡󠅛󠅅󠄑󠅝󠇯` | U+F0220 U+E0121 U+E015B U+E0145 U+E0111 U+E015D U+E01EF | always |
| `Áa` | `󰈠󠅛󠅃󠄑󠅝󠅁󠇯` | U+F0220 U+E015B U+E0143 U+E0111 U+E015D U+E0141 U+E01EF | always |
| `Áá` | `󰈠󠅛󠅃󠄑󠅝󠅛󠅅󠄑󠅝󠇯` | U+F0220 U+E015B U+E0143 U+E0111 U+E015D U+E015B U+E0145 U+E0111 U+E015D U+E01EF | always |
| `ii` | `󰉊` | U+F024A | always |
| `ií` | `󰉊󠅉󠅛󠅅󠅄󠅝󠇯` | U+F024A U+E0149 U+E015B U+E0145 U+E0144 U+E015D U+E01EF | always |
| `íi` | `󰉊󠅛󠅅󠅄󠅝󠅉󠇯` | U+F024A U+E015B U+E0145 U+E0144 U+E015D U+E0149 U+E01EF | always |
| `íí` | `󰉊󠅛󠅅󠅄󠅝󠅛󠅅󠅄󠅝󠇯` | U+F024A U+E015B U+E0145 U+E0144 U+E015D U+E015B U+E0145 U+E0144 U+E015D U+E01EF | always |
| `Ii` | `󰈢` | U+F0222 | always |
| `Ií` | `󰈢󠄩󠅛󠅅󠅄󠅝󠇯` | U+F0222 U+E0129 U+E015B U+E0145 U+E0144 U+E015D U+E01EF | always |
| `Íi` | `󰈢󠅛󠅃󠅄󠅝󠅉󠇯` | U+F0222 U+E015B U+E0143 U+E0144 U+E015D U+E0149 U+E01EF | always |
| `Íí` | `󰈢󠅛󠅃󠅄󠅝󠅛󠅅󠅄󠅝󠇯` | U+F0222 U+E015B U+E0143 U+E0144 U+E015D U+E015B U+E0145 U+E0144 U+E015D U+E01EF | always |
| `uu` | `󰉌` | U+F024C | always |
| `uú` | `󰉌󠅕󠅛󠅆󠅁󠅝󠇯` | U+F024C U+E0155 U+E015B U+E0146 U+E0141 U+E015D U+E01EF | always |
| `úu` | `󰉌󠅛󠅆󠅁󠅝󠅕󠇯` | U+F024C U+E015B U+E0146 U+E0141 U+E015D U+E0155 U+E01EF | always |
| `úú` | `󰉌󠅛󠅆󠅁󠅝󠅛󠅆󠅁󠅝󠇯` | U+F024C U+E015B U+E0146 U+E0141 U+E015D U+E015B U+E0146 U+E0141 U+E015D U+E01EF | always |
| `Uu` | `󰈤` | U+F0224 | always |
| `Uú` | `󰈤󠄵󠅛󠅆󠅁󠅝󠇯` | U+F0224 U+E0135 U+E015B U+E0146 U+E0141 U+E015D U+E01EF | always |
| `Úu` | `󰈤󠅛󠅄󠅁󠅝󠅕󠇯` | U+F0224 U+E015B U+E0144 U+E0141 U+E015D U+E0155 U+E01EF | always |
| `Úú` | `󰈤󠅛󠅄󠅁󠅝󠅛󠅆󠅁󠅝󠇯` | U+F0224 U+E015B U+E0144 U+E0141 U+E015D U+E015B U+E0146 U+E0141 U+E015D U+E01EF | always |
| `y` | `󰉅` | U+F0245 | before a vowel |
| `y` | `󰈷󠅙󠇯` | U+F0237 U+E0159 U+E01EF | always |
| `Y` | `󰈕` | U+F0215 | before a vowel |
| `Y` | `󰈇󠄹󠇯` | U+F0207 U+E0139 U+E01EF | always |
| `ý` | `󰉅󠅛󠅆󠅄󠅝󠇯` | U+F0245 U+E015B U+E0146 U+E0144 U+E015D U+E01EF | before a vowel |
| `ý` | `󰈷󠅛󠅆󠅄󠅝󠇯` | U+F0237 U+E015B U+E0146 U+E0144 U+E015D U+E01EF | always |
| `Ý` | `󰈕󠅛󠅄󠅄󠅝󠇯` | U+F0215 U+E015B U+E0144 U+E0144 U+E015D U+E01EF | before a vowel |
| `Ý` | `󰈇󠅛󠅄󠅄󠅝󠇯` | U+F0207 U+E015B U+E0144 U+E0144 U+E015D U+E01EF | always |
| `'` | `󰉰` | U+F0270 | always |
| `’` | `󰉰󠅛󠄒󠄐󠄑󠄙󠅝󠇯` | U+F0270 U+E015B U+E0112 U+E0110 U+E0111 U+E0119 U+E015D U+E01EF | always |
| `` ` `` | `󰉰󠅀󠇯` | U+F0270 U+E0140 U+E01EF | always |
| `-` | `󰉰󠅛󠄒󠅄󠅝󠇯` | U+F0270 U+E015B U+E0112 U+E0144 U+E015D U+E01EF | always |
| `.` | `󰉨` | U+F0268 | always |
| `?` | `󰉨󠄁󠇯` | U+F0268 U+E0101 U+E01EF | always |
| `‼` | `󰉨󠄂󠇯` | U+F0268 U+E0102 U+E01EF | always |
| `!` | `󰉨󠄃󠇯` | U+F0268 U+E0103 U+E01EF | always |
| `,` | `󰉨󠄅󠇯` | U+F0268 U+E0105 U+E01EF | always |
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
| (space) | (space) | U+0020 | always |

## Round trip

Every encoding round-trips exactly: decoding the code points that encoding wrote gives back the roman text, and encoding that gives the same code points. The Code points column shows every character a row writes, including any that is invisible.

This page is written from `encodings/semaron.json` by `tools/encoding_docs.py`.
