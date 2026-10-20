# Qalezu keyboard

Faces: Qalezu Hand. The faces share code points, so one layout types for every face.

- Emacs input method: `keyboards/emacs/heroiclands-qalezu.el`, named `heroiclands-qalezu`.
- macOS layout: `keyboards/macos/HeroicLands.bundle`, input source **HL Qalezu**.
- Windows layout: `keyboards/windows/qalezu.klc`, the Microsoft Keyboard Layout Creator source of **HL Qalezu**.
- Linux layout: `keyboards/linux/hl_qalezu`, the XKB symbols of **HL Qalezu**.
- Keyboard grid: [keyboard.png](https://github.com/HeroicLands/fonts/blob/main/specimens/qalezu-hand/keyboard.png), every key beside its glyph in each face.

## Layout

- Consonant signs sit on the key of their usual roman letter, and the catch on `'`.
- The digraph signs `th kh gh sh tj` sit on Shift and the first letter (`tj` on Shift+C).
- A doubled sign sits on Option and its letter. A sign written after a catch sits on Option+Shift and its letter. The remaining doubled digraph signs and the signs after a catch that are doubled or digraphs take the next free keys in code point order: the Shift letters, then the Option+Shift letters, then the Option+Shift digits.
- Numerals sit on the digit row; the point and comma on `.` and `,`.
- In Emacs, Option has no key: Option+x is typed `\` and then the key x types, so Option+E is `\e` and Option+Shift+E is `\E`.

## Keys

| Key | Emacs | Code point | Glyph | Kind |
| --- | --- | --- | --- | --- |
| l | `l` | U+1EA00 | l | letter |
| r | `r` | U+1EA01 | r | letter |
| t | `t` | U+1EA02 | t | letter |
| d | `d` | U+1EA03 | d | letter |
| z | `z` | U+1EA04 | z | letter |
| s | `s` | U+1EA05 | s | letter |
| g | `g` | U+1EA06 | g | letter |
| k | `k` | U+1EA07 | k | letter |
| n | `n` | U+1EA08 | n | letter |
| shift+t | `T` | U+1EA09 | th | letter |
| m | `m` | U+1EA0A | m | letter |
| q | `q` | U+1EA0B | q | letter |
| shift+k | `K` | U+1EA0C | kh | letter |
| shift+g | `G` | U+1EA0D | gh | letter |
| h | `h` | U+1EA0E | h | letter |
| shift+s | `S` | U+1EA0F | sh | letter |
| p | `p` | U+1EA10 | p | letter |
| b | `b` | U+1EA11 | b | letter |
| f | `f` | U+1EA12 | f | letter |
| w | `w` | U+1EA13 | w | letter |
| y | `y` | U+1EA14 | y | letter |
| ' | `'` | U+1EA15 | catch | letter |
| shift+c | `C` | U+1EA16 | tj | letter |
| option+l | `\l` | U+1EA17 | l.dbl | doubled |
| option+r | `\r` | U+1EA18 | r.dbl | doubled |
| option+t | `\t` | U+1EA19 | t.dbl | doubled |
| option+d | `\d` | U+1EA1A | d.dbl | doubled |
| option+z | `\z` | U+1EA1B | z.dbl | doubled |
| option+s | `\s` | U+1EA1C | s.dbl | doubled |
| option+g | `\g` | U+1EA1D | g.dbl | doubled |
| option+k | `\k` | U+1EA1E | k.dbl | doubled |
| option+n | `\n` | U+1EA1F | n.dbl | doubled |
| shift+a | `A` | U+1EA20 | th.dbl | doubled |
| option+m | `\m` | U+1EA21 | m.dbl | doubled |
| option+q | `\q` | U+1EA22 | q.dbl | doubled |
| shift+b | `B` | U+1EA23 | kh.dbl | doubled |
| shift+d | `D` | U+1EA24 | gh.dbl | doubled |
| option+h | `\h` | U+1EA25 | h.dbl | doubled |
| shift+e | `E` | U+1EA26 | sh.dbl | doubled |
| option+p | `\p` | U+1EA27 | p.dbl | doubled |
| option+b | `\b` | U+1EA28 | b.dbl | doubled |
| option+f | `\f` | U+1EA29 | f.dbl | doubled |
| option+w | `\w` | U+1EA2A | w.dbl | doubled |
| option+y | `\y` | U+1EA2B | y.dbl | doubled |
| shift+f | `F` | U+1EA2C | tj.dbl | doubled |
| 0 | `0` | U+1EA2D | zero | numeral |
| 1 | `1` | U+1EA2E | one | numeral |
| 2 | `2` | U+1EA2F | two | numeral |
| 3 | `3` | U+1EA30 | three | numeral |
| 4 | `4` | U+1EA31 | four | numeral |
| 5 | `5` | U+1EA32 | five | numeral |
| 6 | `6` | U+1EA33 | six | numeral |
| 7 | `7` | U+1EA34 | seven | numeral |
| 8 | `8` | U+1EA35 | eight | numeral |
| 9 | `9` | U+1EA36 | nine | numeral |
| . | `.` | U+1EA37 | period | point |
| , | `,` | U+1EA38 | comma | point |
| option+shift+l | `\L` | U+1ECC0 | l.catch | catchbefore |
| option+shift+r | `\R` | U+1ECC1 | r.catch | catchbefore |
| option+shift+t | `\T` | U+1ECC2 | t.catch | catchbefore |
| option+shift+d | `\D` | U+1ECC3 | d.catch | catchbefore |
| option+shift+z | `\Z` | U+1ECC4 | z.catch | catchbefore |
| option+shift+s | `\S` | U+1ECC5 | s.catch | catchbefore |
| option+shift+g | `\G` | U+1ECC6 | g.catch | catchbefore |
| option+shift+k | `\K` | U+1ECC7 | k.catch | catchbefore |
| option+shift+n | `\N` | U+1ECC8 | n.catch | catchbefore |
| shift+h | `H` | U+1ECC9 | th.catch | catchbefore |
| option+shift+m | `\M` | U+1ECCA | m.catch | catchbefore |
| option+shift+q | `\Q` | U+1ECCB | q.catch | catchbefore |
| shift+i | `I` | U+1ECCC | kh.catch | catchbefore |
| shift+j | `J` | U+1ECCD | gh.catch | catchbefore |
| option+shift+h | `\H` | U+1ECCE | h.catch | catchbefore |
| shift+l | `L` | U+1ECCF | sh.catch | catchbefore |
| option+shift+p | `\P` | U+1ECD0 | p.catch | catchbefore |
| option+shift+b | `\B` | U+1ECD1 | b.catch | catchbefore |
| option+shift+f | `\F` | U+1ECD2 | f.catch | catchbefore |
| option+shift+w | `\W` | U+1ECD3 | w.catch | catchbefore |
| option+shift+y | `\Y` | U+1ECD4 | y.catch | catchbefore |
| shift+m | `M` | U+1ECD5 | tj.catch | catchbefore |
| shift+n | `N` | U+1ECD6 | l.dbl.catch | catchbefore |
| shift+o | `O` | U+1ECD7 | r.dbl.catch | catchbefore |
| shift+p | `P` | U+1ECD8 | t.dbl.catch | catchbefore |
| shift+q | `Q` | U+1ECD9 | d.dbl.catch | catchbefore |
| shift+r | `R` | U+1ECDA | z.dbl.catch | catchbefore |
| shift+u | `U` | U+1ECDB | s.dbl.catch | catchbefore |
| shift+v | `V` | U+1ECDC | g.dbl.catch | catchbefore |
| shift+w | `W` | U+1ECDD | k.dbl.catch | catchbefore |
| shift+x | `X` | U+1ECDE | n.dbl.catch | catchbefore |
| shift+y | `Y` | U+1ECDF | th.dbl.catch | catchbefore |
| shift+z | `Z` | U+1ECE0 | m.dbl.catch | catchbefore |
| option+shift+a | `\A` | U+1ECE1 | q.dbl.catch | catchbefore |
| option+shift+c | `\C` | U+1ECE2 | kh.dbl.catch | catchbefore |
| option+shift+e | `\E` | U+1ECE3 | gh.dbl.catch | catchbefore |
| option+shift+i | `\I` | U+1ECE4 | h.dbl.catch | catchbefore |
| option+shift+j | `\J` | U+1ECE5 | sh.dbl.catch | catchbefore |
| option+shift+o | `\O` | U+1ECE6 | p.dbl.catch | catchbefore |
| option+shift+u | `\U` | U+1ECE7 | b.dbl.catch | catchbefore |
| option+shift+v | `\V` | U+1ECE8 | f.dbl.catch | catchbefore |
| option+shift+x | `\X` | U+1ECE9 | w.dbl.catch | catchbefore |
| option+shift+0 | `\)` | U+1ECEA | y.dbl.catch | catchbefore |
| option+shift+1 | `\!` | U+1ECEB | tj.dbl.catch | catchbefore |
