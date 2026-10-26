# HL Thuravark cheatsheet

HL Thuravark types Thuravark Carved and Thuravark Carved Bound by sound. It is a US keyboard that writes the Thuravark script: the key for a sound types that sound's Thuravark character, so `t` types the script's t and Option+T types its th. You type the sounds of a word one after another, as you would in English.

![HL Thuravark on an ANSI keyboard](thuravark.png)

A printable copy is [thuravark.svg](thuravark.svg) and [thuravark.png](thuravark.png).

## Reading the keys

- `t` is the key alone. `shift+t` is Shift and the key.
- `option+t` is Option and the key on a Mac, and AltGr and the key on Windows and Linux. AltGr is the right Alt key (on a keyboard without one, hold Ctrl and Alt together). `option+shift+t` adds Shift.
- The Sound column is the roman spelling of the sound a key stands for. A key marked _nothing_ types nothing in this script.
- Character names and code points identify each character exactly, for a program or a character viewer.
- The Emacs column is what to type in the Emacs input method `heroiclands-thuravark`, where Option is a backslash.

## Installing the layout

The layout is a file per platform, named below. [The README](../README.md#installing-a-keyboard-layout) walks through installing each.

- macOS: `keyboards/macos/HeroicLands.bundle`, input source **HL Thuravark**.
- Windows: `keyboards/windows/thuravark.klc`, the Microsoft Keyboard Layout Creator source of **HL Thuravark**.
- Linux: `keyboards/linux/hl_thuravark`, the XKB symbols of **HL Thuravark**.
- Emacs: `keyboards/emacs/heroiclands-thuravark.el`, the input method `heroiclands-thuravark`.

## Signs

These keys type no sound. They type in HL Thuravark alone.

| Key | Emacs | Sign | Layout | Glyph | Code point | Name |
| --- | --- | --- | --- | --- | --- | --- |
| `option+shift+w` | `\W` | literal open | HL Thuravark | ⟦ | U+27E6 | LEFT WHITE SQUARE BRACKET |
| `option+shift+l` | `\L` | literal close | HL Thuravark | ⟧ | U+27E7 | RIGHT WHITE SQUARE BRACKET |

## Keys a platform cannot carry

A Windows key holds at most four UTF-16 code units and a Linux key one character, so a sound this script spells with more types nothing there. macOS and Emacs carry every key.

| Key | Sound | Script | Platform | Why |
| --- | --- | --- | --- | --- |
| `option+s` | `sh` | Thuravark | Linux | 2 code points; an XKB key types one |
| `option+z` | `zh` | Thuravark | Linux | 2 code points; an XKB key types one |
| `option+p` | `ph` | Thuravark | Linux | 2 code points; an XKB key types one |
| `option+y` | `ny` | Thuravark | Linux | 2 code points; an XKB key types one |
| `option+x` | `ts` | Thuravark | Linux | 2 code points; an XKB key types one |
| `option+b` | `bh` | Thuravark | Linux | 2 code points; an XKB key types one |
| `option+1` | `aa` | Thuravark | Linux | 2 code points; an XKB key types one |
| `option+2` | `ee` | Thuravark | Linux | 2 code points; an XKB key types one |
| `option+3` | `ii` | Thuravark | Linux | 2 code points; an XKB key types one |
| `option+4` | `oo` | Thuravark | Linux | 2 code points; an XKB key types one |
| `option+5` | `uu` | Thuravark | Linux | 2 code points; an XKB key types one |
| `option+6` | `ai` | Thuravark | Linux | 2 code points; an XKB key types one |
| `option+7` | `au` | Thuravark | Linux | 2 code points; an XKB key types one |
| `option+8` | `ei` | Thuravark | Linux | 2 code points; an XKB key types one |
| `option+9` | `oi` | Thuravark | Linux | 2 code points; an XKB key types one |
| `option+0` | `ou` | Thuravark | Linux | 2 code points; an XKB key types one |
| `option+-` | `ie` | Thuravark | Linux | 2 code points; an XKB key types one |
| `option+=` | `uo` | Thuravark | Linux | 2 code points; an XKB key types one |
| `option+[` | `ae` | Thuravark | Linux | 2 code points; an XKB key types one |
| `option+]` | `ea` | Thuravark | Linux | 2 code points; an XKB key types one |
| `option+a` | `á` | Thuravark | Linux | 2 code points; an XKB key types one |
| `option+e` | `é` | Thuravark | Linux | 2 code points; an XKB key types one |
| `option+i` | `í` | Thuravark | Linux | 2 code points; an XKB key types one |
| `option+o` | `ó` | Thuravark | Linux | 2 code points; an XKB key types one |
| `option+u` | `ú` | Thuravark | Linux | 2 code points; an XKB key types one |

## Markup

These keys type themselves, as plain ASCII, in every layout, so Markdown and similar markup are written without switching layouts.

| Key | Types |
| --- | --- |
| `shift+8` | `*` |
| `shift+-` | `_` |
| `[` | `[` |
| `]` | `]` |
| `shift+[` | `{` |
| `shift+]` | `}` |
| `shift+9` | `(` |
| `shift+0` | `)` |
| `=` | `=` |
| `shift+;` | `:` |
| `shift+\` | `\|` |
| `\` | `\` |
| `` shift+` `` | `~` |
| `` ` `` | `` ` `` |

## Keys

Every sound key, in keyboard order. Example: `t` types the sound `t`.

| Key | Glyphs | Code points | Names | Sound | Emacs |
| --- | --- | --- | --- | --- | --- |
| `a` | ![U+F0100](../charts/thuravark-carved/glyphs/U+F0100.svg) | U+F0100 | THURAVARK LETTER A | `a` | `a` |
| `shift+a` |  | nothing: this script has no character for the sound |  | `A` | `A` |
| `b` | ![U+F0105](../charts/thuravark-carved/glyphs/U+F0105.svg) | U+F0105 | THURAVARK LETTER BRELD | `b` | `b` |
| `shift+b` |  | nothing: this script has no character for the sound |  | `B` | `B` |
| `d` | ![U+F0106](../charts/thuravark-carved/glyphs/U+F0106.svg) | U+F0106 | THURAVARK LETTER DRESK | `d` | `d` |
| `shift+d` |  | nothing: this script has no character for the sound |  | `D` | `D` |
| `e` | ![U+F0101](../charts/thuravark-carved/glyphs/U+F0101.svg) | U+F0101 | THURAVARK LETTER E | `e` | `e` |
| `shift+e` |  | nothing: this script has no character for the sound |  | `E` | `E` |
| `f` | ![U+F0107](../charts/thuravark-carved/glyphs/U+F0107.svg) | U+F0107 | THURAVARK LETTER FOSK | `f` | `f` |
| `shift+f` |  | nothing: this script has no character for the sound |  | `F` | `F` |
| `g` | ![U+F0108](../charts/thuravark-carved/glyphs/U+F0108.svg) | U+F0108 | THURAVARK LETTER GELDRA | `g` | `g` |
| `shift+g` |  | nothing: this script has no character for the sound |  | `G` | `G` |
| `h` | ![U+F0109](../charts/thuravark-carved/glyphs/U+F0109.svg) | U+F0109 | THURAVARK LETTER HVELM | `h` | `h` |
| `shift+h` |  | nothing: this script has no character for the sound |  | `H` | `H` |
| `i` | ![U+F0102](../charts/thuravark-carved/glyphs/U+F0102.svg) | U+F0102 | THURAVARK LETTER I | `i` | `i` |
| `shift+i` |  | nothing: this script has no character for the sound |  | `I` | `I` |
| `j` | ![U+F010A](../charts/thuravark-carved/glyphs/U+F010A.svg) | U+F010A | THURAVARK LETTER JA | `j` | `j` |
| `shift+j` |  | nothing: this script has no character for the sound |  | `J` | `J` |
| `k` | ![U+F010B](../charts/thuravark-carved/glyphs/U+F010B.svg) | U+F010B | THURAVARK LETTER KNERV | `k` | `k` |
| `shift+k` |  | nothing: this script has no character for the sound |  | `K` | `K` |
| `l` | ![U+F010C](../charts/thuravark-carved/glyphs/U+F010C.svg) | U+F010C | THURAVARK LETTER LA | `l` | `l` |
| `shift+l` |  | nothing: this script has no character for the sound |  | `L` | `L` |
| `m` | ![U+F010D](../charts/thuravark-carved/glyphs/U+F010D.svg) | U+F010D | THURAVARK LETTER MERV | `m` | `m` |
| `shift+m` |  | nothing: this script has no character for the sound |  | `M` | `M` |
| `n` | ![U+F010E](../charts/thuravark-carved/glyphs/U+F010E.svg) | U+F010E | THURAVARK LETTER NELTH | `n` | `n` |
| `shift+n` |  | nothing: this script has no character for the sound |  | `N` | `N` |
| `o` | ![U+F0103](../charts/thuravark-carved/glyphs/U+F0103.svg) | U+F0103 | THURAVARK LETTER ODEL | `o` | `o` |
| `shift+o` |  | nothing: this script has no character for the sound |  | `O` | `O` |
| `p` | ![U+F010F](../charts/thuravark-carved/glyphs/U+F010F.svg) | U+F010F | THURAVARK LETTER PA | `p` | `p` |
| `shift+p` |  | nothing: this script has no character for the sound |  | `P` | `P` |
| `q` | ![U+F010B](../charts/thuravark-carved/glyphs/U+F010B.svg) | U+F010B | THURAVARK LETTER KNERV | `q` | `q` |
| `shift+q` |  | nothing: this script has no character for the sound |  | `Q` | `Q` |
| `r` | ![U+F0110](../charts/thuravark-carved/glyphs/U+F0110.svg) | U+F0110 | THURAVARK LETTER RELTH | `r` | `r` |
| `shift+r` |  | nothing: this script has no character for the sound |  | `R` | `R` |
| `s` | ![U+F0111](../charts/thuravark-carved/glyphs/U+F0111.svg) | U+F0111 | THURAVARK LETTER SVELD | `s` | `s` |
| `shift+s` |  | nothing: this script has no character for the sound |  | `S` | `S` |
| `t` | ![U+F0112](../charts/thuravark-carved/glyphs/U+F0112.svg) | U+F0112 | THURAVARK LETTER TING | `t` | `t` |
| `shift+t` |  | nothing: this script has no character for the sound |  | `T` | `T` |
| `u` | ![U+F0104](../charts/thuravark-carved/glyphs/U+F0104.svg) | U+F0104 | THURAVARK LETTER U | `u` | `u` |
| `shift+u` |  | nothing: this script has no character for the sound |  | `U` | `U` |
| `v` | ![U+F0113](../charts/thuravark-carved/glyphs/U+F0113.svg) | U+F0113 | THURAVARK LETTER VULD | `v` | `v` |
| `shift+v` |  | nothing: this script has no character for the sound |  | `V` | `V` |
| `w` | ![U+F0114](../charts/thuravark-carved/glyphs/U+F0114.svg) | U+F0114 | THURAVARK LETTER WA | `w` | `w` |
| `shift+w` |  | nothing: this script has no character for the sound |  | `W` | `W` |
| `y` | ![U+F010A](../charts/thuravark-carved/glyphs/U+F010A.svg) | U+F010A | THURAVARK LETTER JA | `y` | `y` |
| `shift+y` |  | nothing: this script has no character for the sound |  | `Y` | `Y` |
| `z` | ![U+F0115](../charts/thuravark-carved/glyphs/U+F0115.svg) | U+F0115 | THURAVARK LETTER ZA | `z` | `z` |
| `shift+z` |  | nothing: this script has no character for the sound |  | `Z` | `Z` |
| `option+c` |  | nothing: this script has no character for the sound |  | `ch` | `\c` |
| `option+shift+c` |  | nothing: this script has no character for the sound |  | `Ch` | `\C` |
| `option+s` | ![U+F0111](../charts/thuravark-carved/glyphs/U+F0111.svg) ![U+F0109](../charts/thuravark-carved/glyphs/U+F0109.svg) | U+F0111 U+F0109 | THURAVARK LETTER SVELD; THURAVARK LETTER HVELM | `sh` | `\s` |
| `option+shift+s` |  | nothing: this script has no character for the sound |  | `Sh` | `\S` |
| `option+t` | ![U+F0120](../charts/thuravark-carved/glyphs/U+F0120.svg) | U+F0120 | THURAVARK LETTER THRESK | `th` | `\t` |
| `option+shift+t` |  | nothing: this script has no character for the sound |  | `Th` | `\T` |
| `option+d` | ![U+F0121](../charts/thuravark-carved/glyphs/U+F0121.svg) | U+F0121 | THURAVARK LETTER DHA | `dh` | `\d` |
| `option+shift+d` |  | nothing: this script has no character for the sound |  | `Dh` | `\D` |
| `option+k` | ![U+F0122](../charts/thuravark-carved/glyphs/U+F0122.svg) | U+F0122 | THURAVARK LETTER KHA | `kh` | `\k` |
| `option+shift+k` |  | nothing: this script has no character for the sound |  | `Kh` | `\K` |
| `option+g` | ![U+F0123](../charts/thuravark-carved/glyphs/U+F0123.svg) | U+F0123 | THURAVARK LETTER GHA | `gh` | `\g` |
| `option+shift+g` |  | nothing: this script has no character for the sound |  | `Gh` | `\G` |
| `option+z` | ![U+F0115](../charts/thuravark-carved/glyphs/U+F0115.svg) ![U+F0109](../charts/thuravark-carved/glyphs/U+F0109.svg) | U+F0115 U+F0109 | THURAVARK LETTER ZA; THURAVARK LETTER HVELM | `zh` | `\z` |
| `option+shift+z` |  | nothing: this script has no character for the sound |  | `Zh` | `\Z` |
| `option+p` | ![U+F010F](../charts/thuravark-carved/glyphs/U+F010F.svg) ![U+F0109](../charts/thuravark-carved/glyphs/U+F0109.svg) | U+F010F U+F0109 | THURAVARK LETTER PA; THURAVARK LETTER HVELM | `ph` | `\p` |
| `option+shift+p` |  | nothing: this script has no character for the sound |  | `Ph` | `\P` |
| `option+n` | ![U+F0125](../charts/thuravark-carved/glyphs/U+F0125.svg) | U+F0125 | THURAVARK LETTER NGA | `ng` | `\n` |
| `option+shift+n` |  | nothing: this script has no character for the sound |  | `Ng` | `\N` |
| `option+y` | ![U+F010E](../charts/thuravark-carved/glyphs/U+F010E.svg) ![U+F0102](../charts/thuravark-carved/glyphs/U+F0102.svg) | U+F010E U+F0102 | THURAVARK LETTER NELTH; THURAVARK LETTER I | `ny` | `\y` |
| `option+shift+y` |  | nothing: this script has no character for the sound |  | `Ny` | `\Y` |
| `option+x` | ![U+F0112](../charts/thuravark-carved/glyphs/U+F0112.svg) ![U+F0111](../charts/thuravark-carved/glyphs/U+F0111.svg) | U+F0112 U+F0111 | THURAVARK LETTER TING; THURAVARK LETTER SVELD | `ts` | `\x` |
| `option+shift+x` |  | nothing: this script has no character for the sound |  | `Ts` | `\X` |
| `option+h` | ![U+F0124](../charts/thuravark-carved/glyphs/U+F0124.svg) | U+F0124 | THURAVARK LETTER HLA | `hl` | `\h` |
| `option+shift+h` |  | nothing: this script has no character for the sound |  | `Hl` | `\H` |
| `option+b` | ![U+F0105](../charts/thuravark-carved/glyphs/U+F0105.svg) ![U+F0109](../charts/thuravark-carved/glyphs/U+F0109.svg) | U+F0105 U+F0109 | THURAVARK LETTER BRELD; THURAVARK LETTER HVELM | `bh` | `\b` |
| `option+shift+b` |  | nothing: this script has no character for the sound |  | `Bh` | `\B` |
| `option+1` | ![U+F0100](../charts/thuravark-carved/glyphs/U+F0100.svg) ![U+F0100](../charts/thuravark-carved/glyphs/U+F0100.svg) | U+F0100 U+F0100 | THURAVARK LETTER A; THURAVARK LETTER A | `aa` | `\1` |
| `option+shift+1` |  | nothing: this script has no character for the sound |  | `Aa` | `\!` |
| `option+2` | ![U+F0101](../charts/thuravark-carved/glyphs/U+F0101.svg) ![U+F0101](../charts/thuravark-carved/glyphs/U+F0101.svg) | U+F0101 U+F0101 | THURAVARK LETTER E; THURAVARK LETTER E | `ee` | `\2` |
| `option+shift+2` |  | nothing: this script has no character for the sound |  | `Ee` | `\@` |
| `option+3` | ![U+F0102](../charts/thuravark-carved/glyphs/U+F0102.svg) ![U+F0102](../charts/thuravark-carved/glyphs/U+F0102.svg) | U+F0102 U+F0102 | THURAVARK LETTER I; THURAVARK LETTER I | `ii` | `\3` |
| `option+shift+3` |  | nothing: this script has no character for the sound |  | `Ii` | `\#` |
| `option+4` | ![U+F0103](../charts/thuravark-carved/glyphs/U+F0103.svg) ![U+F0103](../charts/thuravark-carved/glyphs/U+F0103.svg) | U+F0103 U+F0103 | THURAVARK LETTER ODEL; THURAVARK LETTER ODEL | `oo` | `\4` |
| `option+shift+4` |  | nothing: this script has no character for the sound |  | `Oo` | `\$` |
| `option+5` | ![U+F0104](../charts/thuravark-carved/glyphs/U+F0104.svg) ![U+F0104](../charts/thuravark-carved/glyphs/U+F0104.svg) | U+F0104 U+F0104 | THURAVARK LETTER U; THURAVARK LETTER U | `uu` | `\5` |
| `option+shift+5` |  | nothing: this script has no character for the sound |  | `Uu` | `\%` |
| `option+6` | ![U+F0100](../charts/thuravark-carved/glyphs/U+F0100.svg) ![U+F0102](../charts/thuravark-carved/glyphs/U+F0102.svg) | U+F0100 U+F0102 | THURAVARK LETTER A; THURAVARK LETTER I | `ai` | `\6` |
| `option+shift+6` |  | nothing: this script has no character for the sound |  | `Ai` | `\^` |
| `option+7` | ![U+F0100](../charts/thuravark-carved/glyphs/U+F0100.svg) ![U+F0104](../charts/thuravark-carved/glyphs/U+F0104.svg) | U+F0100 U+F0104 | THURAVARK LETTER A; THURAVARK LETTER U | `au` | `\7` |
| `option+shift+7` |  | nothing: this script has no character for the sound |  | `Au` | `\&` |
| `option+8` | ![U+F0101](../charts/thuravark-carved/glyphs/U+F0101.svg) ![U+F0102](../charts/thuravark-carved/glyphs/U+F0102.svg) | U+F0101 U+F0102 | THURAVARK LETTER E; THURAVARK LETTER I | `ei` | `\8` |
| `option+shift+8` |  | nothing: this script has no character for the sound |  | `Ei` | `\*` |
| `option+9` | ![U+F0103](../charts/thuravark-carved/glyphs/U+F0103.svg) ![U+F0102](../charts/thuravark-carved/glyphs/U+F0102.svg) | U+F0103 U+F0102 | THURAVARK LETTER ODEL; THURAVARK LETTER I | `oi` | `\9` |
| `option+shift+9` |  | nothing: this script has no character for the sound |  | `Oi` | `\(` |
| `option+0` | ![U+F0103](../charts/thuravark-carved/glyphs/U+F0103.svg) ![U+F0104](../charts/thuravark-carved/glyphs/U+F0104.svg) | U+F0103 U+F0104 | THURAVARK LETTER ODEL; THURAVARK LETTER U | `ou` | `\0` |
| `option+shift+0` |  | nothing: this script has no character for the sound |  | `Ou` | `\)` |
| `option+-` | ![U+F0102](../charts/thuravark-carved/glyphs/U+F0102.svg) ![U+F0101](../charts/thuravark-carved/glyphs/U+F0101.svg) | U+F0102 U+F0101 | THURAVARK LETTER I; THURAVARK LETTER E | `ie` | `\-` |
| `option+shift+-` |  | nothing: this script has no character for the sound |  | `Ie` | `\_` |
| `option+=` | ![U+F0104](../charts/thuravark-carved/glyphs/U+F0104.svg) ![U+F0103](../charts/thuravark-carved/glyphs/U+F0103.svg) | U+F0104 U+F0103 | THURAVARK LETTER U; THURAVARK LETTER ODEL | `uo` | `\=` |
| `option+shift+=` |  | nothing: this script has no character for the sound |  | `Uo` | `\+` |
| `option+[` | ![U+F0100](../charts/thuravark-carved/glyphs/U+F0100.svg) ![U+F0101](../charts/thuravark-carved/glyphs/U+F0101.svg) | U+F0100 U+F0101 | THURAVARK LETTER A; THURAVARK LETTER E | `ae` | `\[` |
| `option+shift+[` |  | nothing: this script has no character for the sound |  | `Ae` | `\{` |
| `option+]` | ![U+F0101](../charts/thuravark-carved/glyphs/U+F0101.svg) ![U+F0100](../charts/thuravark-carved/glyphs/U+F0100.svg) | U+F0101 U+F0100 | THURAVARK LETTER E; THURAVARK LETTER A | `ea` | `\]` |
| `option+shift+]` |  | nothing: this script has no character for the sound |  | `Ea` | `\}` |
| `option+a` | ![U+F0100](../charts/thuravark-carved/glyphs/U+F0100.svg) ![U+F0148](../charts/thuravark-carved/glyphs/U+F0148.svg) | U+F0100 U+F0148 | THURAVARK LETTER A; THURAVARK ACUTE | `á` | `\a` |
| `option+shift+a` |  | nothing: this script has no character for the sound |  | `Á` | `\A` |
| `option+e` | ![U+F0101](../charts/thuravark-carved/glyphs/U+F0101.svg) ![U+F0148](../charts/thuravark-carved/glyphs/U+F0148.svg) | U+F0101 U+F0148 | THURAVARK LETTER E; THURAVARK ACUTE | `é` | `\e` |
| `option+shift+e` |  | nothing: this script has no character for the sound |  | `É` | `\E` |
| `option+i` | ![U+F0102](../charts/thuravark-carved/glyphs/U+F0102.svg) ![U+F0148](../charts/thuravark-carved/glyphs/U+F0148.svg) | U+F0102 U+F0148 | THURAVARK LETTER I; THURAVARK ACUTE | `í` | `\i` |
| `option+shift+i` |  | nothing: this script has no character for the sound |  | `Í` | `\I` |
| `option+o` | ![U+F0103](../charts/thuravark-carved/glyphs/U+F0103.svg) ![U+F0148](../charts/thuravark-carved/glyphs/U+F0148.svg) | U+F0103 U+F0148 | THURAVARK LETTER ODEL; THURAVARK ACUTE | `ó` | `\o` |
| `option+shift+o` |  | nothing: this script has no character for the sound |  | `Ó` | `\O` |
| `option+u` | ![U+F0104](../charts/thuravark-carved/glyphs/U+F0104.svg) ![U+F0148](../charts/thuravark-carved/glyphs/U+F0148.svg) | U+F0104 U+F0148 | THURAVARK LETTER U; THURAVARK ACUTE | `ú` | `\u` |
| `option+shift+u` |  | nothing: this script has no character for the sound |  | `Ú` | `\U` |
| `option+;` |  | nothing: this script has no character for the sound |  | `ä` | `\;` |
| `option+shift+;` |  | nothing: this script has no character for the sound |  | `Ä` | `\:` |
| `option+'` | ![U+F0101](../charts/thuravark-carved/glyphs/U+F0101.svg) | U+F0101 | THURAVARK LETTER E | `ë` | `\'` |
| `option+shift+'` |  | nothing: this script has no character for the sound |  | `Ë` | `\"` |
| `option+,` |  | nothing: this script has no character for the sound |  | `ï` | `\,` |
| `option+shift+,` |  | nothing: this script has no character for the sound |  | `Ï` | `\<` |
| `option+.` |  | nothing: this script has no character for the sound |  | `ö` | `\.` |
| `option+shift+.` |  | nothing: this script has no character for the sound |  | `Ö` | `\>` |
| `option+/` |  | nothing: this script has no character for the sound |  | `ü` | `\/` |
| `option+shift+/` |  | nothing: this script has no character for the sound |  | `Ü` | `\?` |
| `'` |  | nothing: this script has no character for the sound |  | `catch` | `'` |
| `.` | ![U+F0140](../charts/thuravark-carved/glyphs/U+F0140.svg) | U+F0140 | THURAVARK FULL STOP | `stop` | `.` |
| `,` |  | nothing: this script has no character for the sound |  | `pause` | `,` |
| `shift+,` |  | nothing: this script has no character for the sound |  | `open quote` | `<` |
| `shift+.` |  | nothing: this script has no character for the sound |  | `close quote` | `>` |
| `0` | ![U+F0130](../charts/thuravark-carved/glyphs/U+F0130.svg) | U+F0130 | THURAVARK DIGIT ZERO | `0` | `0` |
| `1` | ![U+F0131](../charts/thuravark-carved/glyphs/U+F0131.svg) | U+F0131 | THURAVARK DIGIT ONE | `1` | `1` |
| `2` | ![U+F0132](../charts/thuravark-carved/glyphs/U+F0132.svg) | U+F0132 | THURAVARK DIGIT TWO | `2` | `2` |
| `3` | ![U+F0133](../charts/thuravark-carved/glyphs/U+F0133.svg) | U+F0133 | THURAVARK DIGIT THREE | `3` | `3` |
| `4` | ![U+F0134](../charts/thuravark-carved/glyphs/U+F0134.svg) | U+F0134 | THURAVARK DIGIT FOUR | `4` | `4` |
| `5` | ![U+F0135](../charts/thuravark-carved/glyphs/U+F0135.svg) | U+F0135 | THURAVARK DIGIT FIVE | `5` | `5` |
| `6` | ![U+F0136](../charts/thuravark-carved/glyphs/U+F0136.svg) | U+F0136 | THURAVARK DIGIT SIX | `6` | `6` |
| `7` | ![U+F0137](../charts/thuravark-carved/glyphs/U+F0137.svg) | U+F0137 | THURAVARK DIGIT SEVEN | `7` | `7` |
| `8` | ![U+F0138](../charts/thuravark-carved/glyphs/U+F0138.svg) | U+F0138 | THURAVARK DIGIT EIGHT | `8` | `8` |
| `9` | ![U+F0139](../charts/thuravark-carved/glyphs/U+F0139.svg) | U+F0139 | THURAVARK DIGIT NINE | `9` | `9` |
| `shift+2` |  | nothing: this script has no character for the sound |  | `ten` | `@` |
| `shift+3` |  | nothing: this script has no character for the sound |  | `eleven` | `#` |
| `shift+4` |  | nothing: this script has no character for the sound |  | `twelve` | `$` |
| `shift+5` |  | nothing: this script has no character for the sound |  | `thirteen` | `%` |
| `shift+6` |  | nothing: this script has no character for the sound |  | `fourteen` | `^` |
| `shift+7` |  | nothing: this script has no character for the sound |  | `fifteen` | `&` |
