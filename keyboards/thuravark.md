# Thuravark keyboard

Faces: Thuravark Carved. The faces share code points, so one layout types for every face.

- Emacs input method: `keyboards/emacs/heroiclands-thuravark.el`, named `heroiclands-thuravark`.
- macOS layout: `keyboards/macos/HeroicLands.bundle`, input source **HL Thuravark**.
- Windows layout: `keyboards/windows/thuravark.klc`, the Microsoft Keyboard Layout Creator source of **HL Thuravark**.
- Linux layout: `keyboards/linux/hl_thuravark`, the XKB symbols of **HL Thuravark**.
- Keyboard grid: [keyboard.png](https://github.com/HeroicLands/fonts/blob/main/specimens/thuravark-carved/keyboard.png), every key beside its glyph in each face.

## Layout

- Letters sit on their roman keys.
- The digraph letters `th dh kh gh hl ng` sit on Shift and the first letter of the digraph.
- Numerals sit on the digit row, the point on `.` and the acute mark on Option+E.
- In Emacs, Option has no key: Option+x is typed `\` and then the key x types, so Option+E is `\e` and Option+Shift+E is `\E`.

## Keys

| Key | Emacs | Code point | Glyph | Kind |
| --- | --- | --- | --- | --- |
| a | `a` | U+F0100 | a | letter |
| e | `e` | U+F0101 | e | letter |
| i | `i` | U+F0102 | i | letter |
| o | `o` | U+F0103 | o | letter |
| u | `u` | U+F0104 | u | letter |
| b | `b` | U+F0105 | b | letter |
| d | `d` | U+F0106 | d | letter |
| f | `f` | U+F0107 | f | letter |
| g | `g` | U+F0108 | g | letter |
| h | `h` | U+F0109 | h | letter |
| j | `j` | U+F010A | j | letter |
| k | `k` | U+F010B | k | letter |
| l | `l` | U+F010C | l | letter |
| m | `m` | U+F010D | m | letter |
| n | `n` | U+F010E | n | letter |
| p | `p` | U+F010F | p | letter |
| r | `r` | U+F0110 | r | letter |
| s | `s` | U+F0111 | s | letter |
| t | `t` | U+F0112 | t | letter |
| v | `v` | U+F0113 | v | letter |
| w | `w` | U+F0114 | w | letter |
| z | `z` | U+F0115 | z | letter |
| shift+t | `T` | U+F0120 | th | digraph |
| shift+d | `D` | U+F0121 | dh | digraph |
| shift+k | `K` | U+F0122 | kh | digraph |
| shift+g | `G` | U+F0123 | gh | digraph |
| shift+h | `H` | U+F0124 | hl | digraph |
| shift+n | `N` | U+F0125 | ng | digraph |
| 0 | `0` | U+F0130 | num.0 | numeral |
| 1 | `1` | U+F0131 | num.1 | numeral |
| 2 | `2` | U+F0132 | num.2 | numeral |
| 3 | `3` | U+F0133 | num.3 | numeral |
| 4 | `4` | U+F0134 | num.4 | numeral |
| 5 | `5` | U+F0135 | num.5 | numeral |
| 6 | `6` | U+F0136 | num.6 | numeral |
| 7 | `7` | U+F0137 | num.7 | numeral |
| 8 | `8` | U+F0138 | num.8 | numeral |
| 9 | `9` | U+F0139 | num.9 | numeral |
| . | `.` | U+F0140 | period | point |
| option+e | `\e` | U+F0148 | acutecomb | mark |
