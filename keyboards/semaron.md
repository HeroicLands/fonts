# Semaron keyboard

Faces: Semaron Kuriale. The faces share code points, so one layout types for every face.

- Emacs input method: `keyboards/emacs/heroiclands-semaron.el`, named `heroiclands-semaron`.
- macOS layout: `keyboards/macos/HeroicLands.bundle`, input source **HL Semaron**.
- Windows layout: `keyboards/windows/semaron.klc`, the Microsoft Keyboard Layout Creator source of **HL Semaron**.
- Linux layout: `keyboards/linux/hl_semaron`, the XKB symbols of **HL Semaron**.
- Keyboard grid: [keyboard.png](https://github.com/HeroicLands/fonts/blob/main/specimens/semaron-kuriale/keyboard.png), every key beside its glyph in each face.

## Layout

- Small letters sit on their roman keys and capitals on Shift.
- `th` and `TH`, and the ten long vowels, sit on Option: Option+vowel for the small long vowel and Option+Shift+vowel for the capital.
- Numerals sit on the digit row, the point on `.` and the grave on `` ` ``.
- In Emacs, Option has no key: Option+x is typed `\` and then the key x types, so Option+E is `\e` and Option+Shift+E is `\E`.

## Keys

| Key | Emacs | Code point | Glyph | Kind |
| --- | --- | --- | --- | --- |
| shift+a | `A` | U+F0200 | A | letter |
| shift+b | `B` | U+F0201 | B | letter |
| shift+d | `D` | U+F0202 | D | letter |
| shift+e | `E` | U+F0203 | E | letter |
| shift+f | `F` | U+F0204 | F | letter |
| shift+g | `G` | U+F0205 | G | letter |
| shift+h | `H` | U+F0206 | H | letter |
| shift+i | `I` | U+F0207 | I | letter |
| shift+j | `J` | U+F0208 | J | letter |
| shift+k | `K` | U+F0209 | K | letter |
| shift+l | `L` | U+F020A | L | letter |
| shift+m | `M` | U+F020B | M | letter |
| shift+n | `N` | U+F020C | N | letter |
| shift+o | `O` | U+F020D | O | letter |
| shift+p | `P` | U+F020E | P | letter |
| shift+r | `R` | U+F020F | R | letter |
| shift+s | `S` | U+F0210 | S | letter |
| shift+t | `T` | U+F0211 | T | letter |
| shift+u | `U` | U+F0212 | U | letter |
| shift+v | `V` | U+F0213 | V | letter |
| shift+w | `W` | U+F0214 | W | letter |
| shift+y | `Y` | U+F0215 | Y | letter |
| shift+z | `Z` | U+F0216 | Z | letter |
| option+shift+a | `\A` | U+F0220 | A.long | letter |
| option+shift+e | `\E` | U+F0221 | E.long | letter |
| option+shift+i | `\I` | U+F0222 | I.long | letter |
| option+shift+o | `\O` | U+F0223 | O.long | letter |
| option+shift+u | `\U` | U+F0224 | U.long | letter |
| a | `a` | U+F0230 | a | letter |
| b | `b` | U+F0231 | b | letter |
| d | `d` | U+F0232 | d | letter |
| e | `e` | U+F0233 | e | letter |
| f | `f` | U+F0234 | f | letter |
| g | `g` | U+F0235 | g | letter |
| h | `h` | U+F0236 | h | letter |
| i | `i` | U+F0237 | i | letter |
| j | `j` | U+F0238 | j | letter |
| k | `k` | U+F0239 | k | letter |
| l | `l` | U+F023A | l | letter |
| m | `m` | U+F023B | m | letter |
| n | `n` | U+F023C | n | letter |
| o | `o` | U+F023D | o | letter |
| p | `p` | U+F023E | p | letter |
| r | `r` | U+F023F | r | letter |
| s | `s` | U+F0240 | s | letter |
| t | `t` | U+F0241 | t | letter |
| u | `u` | U+F0242 | u | letter |
| v | `v` | U+F0243 | v | letter |
| w | `w` | U+F0244 | w | letter |
| y | `y` | U+F0245 | y | letter |
| z | `z` | U+F0246 | z | letter |
| option+a | `\a` | U+F0248 | a.long | letter |
| option+e | `\e` | U+F0249 | e.long | letter |
| option+i | `\i` | U+F024A | i.long | letter |
| option+o | `\o` | U+F024B | o.long | letter |
| option+u | `\u` | U+F024C | u.long | letter |
| option+t | `\t` | U+F0250 | th | digraph |
| option+shift+t | `\T` | U+F0251 | TH | digraph |
| 0 | `0` | U+F0258 | num.0 | numeral |
| 1 | `1` | U+F0259 | num.1 | numeral |
| 2 | `2` | U+F025A | num.2 | numeral |
| 3 | `3` | U+F025B | num.3 | numeral |
| 4 | `4` | U+F025C | num.4 | numeral |
| 5 | `5` | U+F025D | num.5 | numeral |
| 6 | `6` | U+F025E | num.6 | numeral |
| 7 | `7` | U+F025F | num.7 | numeral |
| 8 | `8` | U+F0260 | num.8 | numeral |
| 9 | `9` | U+F0261 | num.9 | numeral |
| . | `.` | U+F0268 | point | point |
| ` | `` ` `` | U+F0270 | grave | mark |
