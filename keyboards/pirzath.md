# Pirzath keyboard

Faces: Pirzath Carved, Pirzath Hand, Pirzath Hand Lifted. The faces share code points, so one layout types for every face.

- Emacs input method: `keyboards/emacs/heroiclands-pirzath.el`, named `heroiclands-pirzath`.
- macOS layout: `keyboards/macos/HeroicLands.bundle`, input source **HL Pirzath**.
- Windows layout: `keyboards/windows/pirzath.klc`, the Microsoft Keyboard Layout Creator source of **HL Pirzath**.
- Linux layout: `keyboards/linux/hl_pirzath`, the XKB symbols of **HL Pirzath**.
- Keyboard grid: [keyboard.png](https://github.com/HeroicLands/fonts/blob/main/specimens/pirzath/keyboard.png), every key beside its glyph in each face.

## Layout

- Letters sit on their roman keys, and the catch on `'`.
- The digraph letters and the diphthongs sit on Shift, on the first letter of the digraph where that key is free: Shift+S `sh`, Shift+T `th`. Where it is taken, the nearest free key: `ts` on Shift+X, `ny` on Shift+Y, and `ou` on Shift+W.
- Numerals zero to nine sit on the digit row; numerals ten to fifteen on Option and the digits 0 to 5.
- The length mark sits on Option+E. Points sit on their roman keys; the opening and closing quotation marks on `<` and `>`.
- In Emacs, Option has no key: Option+x is typed `\` and then the key x types, so Option+E is `\e` and Option+Shift+E is `\E`.

## Keys

| Key | Emacs | Code point | Glyph | Kind |
| --- | --- | --- | --- | --- |
| a | `a` | U+F0000 | a | letter |
| e | `e` | U+F0001 | e | letter |
| i | `i` | U+F0002 | i | letter |
| o | `o` | U+F0003 | o | letter |
| u | `u` | U+F0004 | u | letter |
| p | `p` | U+F0005 | p | letter |
| b | `b` | U+F0006 | b | letter |
| f | `f` | U+F0007 | f | letter |
| v | `v` | U+F0008 | v | letter |
| m | `m` | U+F0009 | m | letter |
| t | `t` | U+F000A | t | letter |
| d | `d` | U+F000B | d | letter |
| n | `n` | U+F000C | n | letter |
| k | `k` | U+F000D | k | letter |
| g | `g` | U+F000E | g | letter |
| s | `s` | U+F000F | s | letter |
| z | `z` | U+F0010 | z | letter |
| h | `h` | U+F0011 | h | letter |
| l | `l` | U+F0012 | l | letter |
| r | `r` | U+F0013 | r | letter |
| j | `j` | U+F0014 | j | letter |
| q | `q` | U+F0015 | q | letter |
| w | `w` | U+F0016 | w | letter |
| y | `y` | U+F0017 | y | letter |
| ' | `'` | U+F0018 | catch | letter |
| shift+t | `T` | U+F0020 | t_h | digraph |
| shift+d | `D` | U+F0021 | d_h | digraph |
| shift+k | `K` | U+F0022 | k_h | digraph |
| shift+g | `G` | U+F0023 | g_h | digraph |
| shift+s | `S` | U+F0024 | sh | digraph |
| shift+z | `Z` | U+F0025 | zh | digraph |
| shift+x | `X` | U+F0026 | ts | digraph |
| shift+c | `C` | U+F0027 | ch | digraph |
| shift+n | `N` | U+F0028 | ng | digraph |
| shift+y | `Y` | U+F0029 | ny | digraph |
| shift+h | `H` | U+F002A | hl | digraph |
| shift+a | `A` | U+F0030 | ai | diphthong |
| shift+u | `U` | U+F0031 | au | diphthong |
| shift+e | `E` | U+F0032 | ei | diphthong |
| shift+o | `O` | U+F0033 | oi | diphthong |
| shift+w | `W` | U+F0034 | ou | diphthong |
| 0 | `0` | U+F0040 | num.0 | numeral |
| 1 | `1` | U+F0041 | num.1 | numeral |
| 2 | `2` | U+F0042 | num.2 | numeral |
| 3 | `3` | U+F0043 | num.3 | numeral |
| 4 | `4` | U+F0044 | num.4 | numeral |
| 5 | `5` | U+F0045 | num.5 | numeral |
| 6 | `6` | U+F0046 | num.6 | numeral |
| 7 | `7` | U+F0047 | num.7 | numeral |
| 8 | `8` | U+F0048 | num.8 | numeral |
| 9 | `9` | U+F0049 | num.9 | numeral |
| option+0 | `\0` | U+F004A | num.10 | numeral |
| option+1 | `\1` | U+F004B | num.11 | numeral |
| option+2 | `\2` | U+F004C | num.12 | numeral |
| option+3 | `\3` | U+F004D | num.13 | numeral |
| option+4 | `\4` | U+F004E | num.14 | numeral |
| option+5 | `\5` | U+F004F | num.15 | numeral |
| . | `.` | U+F0050 | period | point |
| , | `,` | U+F0051 | comma | point |
| shift+1 | `!` | U+F0052 | exclam | point |
| - | `-` | U+F0053 | hyphen | point |
| shift+, | `<` | U+F0054 | quote.open | point |
| shift+. | `>` | U+F0055 | quote.close | point |
| option+e | `\e` | U+F0060 | lengthmark | mark |
