# HL Qalezu cheatsheet

HL Qalezu types Qalezu Hand by sound. It is a US keyboard that writes the Qalezu script: the key for a sound types that sound's Qalezu character, so `t` types the script's t, Option+T types its th, and Shift makes a capital. You type the sounds of a word one after another, as you would in English.

![HL Qalezu on an ANSI keyboard](qalezu.png)

A printable copy is [qalezu.svg](qalezu.svg) and [qalezu.png](qalezu.png).

## Reading the keys

- `t` is the key alone. `shift+t` is Shift and the key.
- `option+t` is Option and the key on a Mac, and AltGr and the key on Windows and Linux. AltGr is the right Alt key (on a keyboard without one, hold Ctrl and Alt together). `option+shift+t` adds Shift.
- The Sound column is the roman spelling of the sound a key stands for. A key marked _nothing_ types nothing in this script.
- Character names and code points identify each character exactly, for a program or a character viewer.
- The Emacs column is what to type in the Emacs input method `heroiclands-qalezu`, where Option is a backslash.

In Roman spelling, U+00B7 MIDDLE DOT (`·`) writes the verse-end dot. `option+shift+f` types it directly in HL Qalezu; a physical line break does not add it.

## Installing the layout

The layout is a file per platform, named below. [The README](../README.md#installing-a-keyboard-layout) walks through installing each.

- macOS: `keyboards/macos/HeroicLands.bundle`, input source **HL Qalezu**.
- Windows: `keyboards/windows/qalezu.klc`, the Microsoft Keyboard Layout Creator source of **HL Qalezu**.
- Linux: `keyboards/linux/hl_qalezu`, the XKB symbols of **HL Qalezu**.
- Emacs: `keyboards/emacs/heroiclands-qalezu.el`, the input method `heroiclands-qalezu`.

## Signs

These keys type no sound. They type in HL Qalezu alone.

| Key | Emacs | Sign | Layout | Glyph | Code point | Name |
| --- | --- | --- | --- | --- | --- | --- |
| `option+shift+f` | `\F` | verse end | HL Qalezu | ![U+1EA39](../charts/qalezu-hand/glyphs/U+1EA39.svg) | U+1EA39 | QALEZU VERSE END |

## Keys a platform cannot carry

A Windows key holds at most four UTF-16 code units and a Linux key one character, so a sound this script spells with more types nothing there. macOS and Emacs carry every key.

| Key | Sound | Script | Platform | Why |
| --- | --- | --- | --- | --- |
| `option+d` | `dh` | Qalezu | Linux | 2 code points; an XKB key types one |
| `option+shift+d` | `Dh` | Qalezu | Linux | 2 code points; an XKB key types one |
| `option+z` | `zh` | Qalezu | Linux | 2 code points; an XKB key types one |
| `option+shift+z` | `Zh` | Qalezu | Linux | 2 code points; an XKB key types one |
| `option+p` | `ph` | Qalezu | Linux | 2 code points; an XKB key types one |
| `option+shift+p` | `Ph` | Qalezu | Linux | 2 code points; an XKB key types one |
| `option+n` | `ng` | Qalezu | Linux | 2 code points; an XKB key types one |
| `option+shift+n` | `Ng` | Qalezu | Linux | 2 code points; an XKB key types one |
| `option+y` | `ny` | Qalezu | Linux | 2 code points; an XKB key types one |
| `option+shift+y` | `Ny` | Qalezu | Linux | 2 code points; an XKB key types one |
| `option+x` | `ts` | Qalezu | Linux | 2 code points; an XKB key types one |
| `option+shift+x` | `Ts` | Qalezu | Linux | 2 code points; an XKB key types one |
| `option+h` | `hl` | Qalezu | Linux | 2 code points; an XKB key types one |
| `option+shift+h` | `Hl` | Qalezu | Linux | 2 code points; an XKB key types one |
| `option+b` | `bh` | Qalezu | Linux | 2 code points; an XKB key types one |
| `option+shift+b` | `Bh` | Qalezu | Linux | 2 code points; an XKB key types one |

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
| `a` |  | nothing: this script has no character for the sound |  | `a` | `a` |
| `shift+a` |  | nothing: this script has no character for the sound |  | `A` | `A` |
| `b` | ![U+1EA11](../charts/qalezu-hand/glyphs/U+1EA11.svg) | U+1EA11 | QALEZU LETTER BA | `b` | `b` |
| `shift+b` | ![U+1EA11](../charts/qalezu-hand/glyphs/U+1EA11.svg) | U+1EA11 | QALEZU LETTER BA | `B` | `B` |
| `d` | ![U+1EA03](../charts/qalezu-hand/glyphs/U+1EA03.svg) | U+1EA03 | QALEZU LETTER DURAS | `d` | `d` |
| `shift+d` | ![U+1EA03](../charts/qalezu-hand/glyphs/U+1EA03.svg) | U+1EA03 | QALEZU LETTER DURAS | `D` | `D` |
| `e` |  | nothing: this script has no character for the sound |  | `e` | `e` |
| `shift+e` |  | nothing: this script has no character for the sound |  | `E` | `E` |
| `f` | ![U+1EA12](../charts/qalezu-hand/glyphs/U+1EA12.svg) | U+1EA12 | QALEZU LETTER FA | `f` | `f` |
| `shift+f` | ![U+1EA12](../charts/qalezu-hand/glyphs/U+1EA12.svg) | U+1EA12 | QALEZU LETTER FA | `F` | `F` |
| `g` | ![U+1EA06](../charts/qalezu-hand/glyphs/U+1EA06.svg) | U+1EA06 | QALEZU LETTER GITHAR | `g` | `g` |
| `shift+g` | ![U+1EA06](../charts/qalezu-hand/glyphs/U+1EA06.svg) | U+1EA06 | QALEZU LETTER GITHAR | `G` | `G` |
| `h` | ![U+1EA0E](../charts/qalezu-hand/glyphs/U+1EA0E.svg) | U+1EA0E | QALEZU LETTER HALZI | `h` | `h` |
| `shift+h` | ![U+1EA0E](../charts/qalezu-hand/glyphs/U+1EA0E.svg) | U+1EA0E | QALEZU LETTER HALZI | `H` | `H` |
| `i` |  | nothing: this script has no character for the sound |  | `i` | `i` |
| `shift+i` |  | nothing: this script has no character for the sound |  | `I` | `I` |
| `j` | ![U+1EA16](../charts/qalezu-hand/glyphs/U+1EA16.svg) | U+1EA16 | QALEZU LETTER TJA | `j` | `j` |
| `shift+j` | ![U+1EA16](../charts/qalezu-hand/glyphs/U+1EA16.svg) | U+1EA16 | QALEZU LETTER TJA | `J` | `J` |
| `k` | ![U+1EA07](../charts/qalezu-hand/glyphs/U+1EA07.svg) | U+1EA07 | QALEZU LETTER KA | `k` | `k` |
| `shift+k` | ![U+1EA07](../charts/qalezu-hand/glyphs/U+1EA07.svg) | U+1EA07 | QALEZU LETTER KA | `K` | `K` |
| `l` | ![U+1EA00](../charts/qalezu-hand/glyphs/U+1EA00.svg) | U+1EA00 | QALEZU LETTER LAGUN | `l` | `l` |
| `shift+l` | ![U+1EA00](../charts/qalezu-hand/glyphs/U+1EA00.svg) | U+1EA00 | QALEZU LETTER LAGUN | `L` | `L` |
| `m` | ![U+1EA0A](../charts/qalezu-hand/glyphs/U+1EA0A.svg) | U+1EA0A | QALEZU LETTER MELNU | `m` | `m` |
| `shift+m` | ![U+1EA0A](../charts/qalezu-hand/glyphs/U+1EA0A.svg) | U+1EA0A | QALEZU LETTER MELNU | `M` | `M` |
| `n` | ![U+1EA08](../charts/qalezu-hand/glyphs/U+1EA08.svg) | U+1EA08 | QALEZU LETTER NELGIR | `n` | `n` |
| `shift+n` | ![U+1EA08](../charts/qalezu-hand/glyphs/U+1EA08.svg) | U+1EA08 | QALEZU LETTER NELGIR | `N` | `N` |
| `o` |  | nothing: this script has no character for the sound |  | `o` | `o` |
| `shift+o` |  | nothing: this script has no character for the sound |  | `O` | `O` |
| `p` | ![U+1EA10](../charts/qalezu-hand/glyphs/U+1EA10.svg) | U+1EA10 | QALEZU LETTER PA | `p` | `p` |
| `shift+p` | ![U+1EA10](../charts/qalezu-hand/glyphs/U+1EA10.svg) | U+1EA10 | QALEZU LETTER PA | `P` | `P` |
| `q` | ![U+1EA0B](../charts/qalezu-hand/glyphs/U+1EA0B.svg) | U+1EA0B | QALEZU LETTER QENUWA | `q` | `q` |
| `shift+q` | ![U+1EA0B](../charts/qalezu-hand/glyphs/U+1EA0B.svg) | U+1EA0B | QALEZU LETTER QENUWA | `Q` | `Q` |
| `r` | ![U+1EA01](../charts/qalezu-hand/glyphs/U+1EA01.svg) | U+1EA01 | QALEZU LETTER RETHU | `r` | `r` |
| `shift+r` | ![U+1EA01](../charts/qalezu-hand/glyphs/U+1EA01.svg) | U+1EA01 | QALEZU LETTER RETHU | `R` | `R` |
| `s` | ![U+1EA05](../charts/qalezu-hand/glyphs/U+1EA05.svg) | U+1EA05 | QALEZU LETTER SELQUR | `s` | `s` |
| `shift+s` | ![U+1EA05](../charts/qalezu-hand/glyphs/U+1EA05.svg) | U+1EA05 | QALEZU LETTER SELQUR | `S` | `S` |
| `t` | ![U+1EA02](../charts/qalezu-hand/glyphs/U+1EA02.svg) | U+1EA02 | QALEZU LETTER TULAZ | `t` | `t` |
| `shift+t` | ![U+1EA02](../charts/qalezu-hand/glyphs/U+1EA02.svg) | U+1EA02 | QALEZU LETTER TULAZ | `T` | `T` |
| `u` |  | nothing: this script has no character for the sound |  | `u` | `u` |
| `shift+u` |  | nothing: this script has no character for the sound |  | `U` | `U` |
| `v` | ![U+1EA12](../charts/qalezu-hand/glyphs/U+1EA12.svg) | U+1EA12 | QALEZU LETTER FA | `v` | `v` |
| `shift+v` | ![U+1EA12](../charts/qalezu-hand/glyphs/U+1EA12.svg) | U+1EA12 | QALEZU LETTER FA | `V` | `V` |
| `w` | ![U+1EA13](../charts/qalezu-hand/glyphs/U+1EA13.svg) | U+1EA13 | QALEZU LETTER WALIR | `w` | `w` |
| `shift+w` | ![U+1EA13](../charts/qalezu-hand/glyphs/U+1EA13.svg) | U+1EA13 | QALEZU LETTER WALIR | `W` | `W` |
| `y` | ![U+1EA14](../charts/qalezu-hand/glyphs/U+1EA14.svg) | U+1EA14 | QALEZU LETTER YA | `y` | `y` |
| `shift+y` | ![U+1EA14](../charts/qalezu-hand/glyphs/U+1EA14.svg) | U+1EA14 | QALEZU LETTER YA | `Y` | `Y` |
| `z` | ![U+1EA04](../charts/qalezu-hand/glyphs/U+1EA04.svg) | U+1EA04 | QALEZU LETTER ZAGUL | `z` | `z` |
| `shift+z` | ![U+1EA04](../charts/qalezu-hand/glyphs/U+1EA04.svg) | U+1EA04 | QALEZU LETTER ZAGUL | `Z` | `Z` |
| `option+c` | ![U+1EA16](../charts/qalezu-hand/glyphs/U+1EA16.svg) | U+1EA16 | QALEZU LETTER TJA | `ch` | `\c` |
| `option+shift+c` | ![U+1EA16](../charts/qalezu-hand/glyphs/U+1EA16.svg) | U+1EA16 | QALEZU LETTER TJA | `Ch` | `\C` |
| `option+s` | ![U+1EA0F](../charts/qalezu-hand/glyphs/U+1EA0F.svg) | U+1EA0F | QALEZU LETTER SHENULET | `sh` | `\s` |
| `option+shift+s` | ![U+1EA0F](../charts/qalezu-hand/glyphs/U+1EA0F.svg) | U+1EA0F | QALEZU LETTER SHENULET | `Sh` | `\S` |
| `option+t` | ![U+1EA09](../charts/qalezu-hand/glyphs/U+1EA09.svg) | U+1EA09 | QALEZU LETTER THELQEN | `th` | `\t` |
| `option+shift+t` | ![U+1EA09](../charts/qalezu-hand/glyphs/U+1EA09.svg) | U+1EA09 | QALEZU LETTER THELQEN | `Th` | `\T` |
| `option+d` | ![U+1EA03](../charts/qalezu-hand/glyphs/U+1EA03.svg) ![U+1EA0E](../charts/qalezu-hand/glyphs/U+1EA0E.svg) | U+1EA03 U+1EA0E | QALEZU LETTER DURAS; QALEZU LETTER HALZI | `dh` | `\d` |
| `option+shift+d` | ![U+1EA03](../charts/qalezu-hand/glyphs/U+1EA03.svg) ![U+1EA0E](../charts/qalezu-hand/glyphs/U+1EA0E.svg) | U+1EA03 U+1EA0E | QALEZU LETTER DURAS; QALEZU LETTER HALZI | `Dh` | `\D` |
| `option+k` | ![U+1EA0C](../charts/qalezu-hand/glyphs/U+1EA0C.svg) | U+1EA0C | QALEZU LETTER KHA | `kh` | `\k` |
| `option+shift+k` | ![U+1EA0C](../charts/qalezu-hand/glyphs/U+1EA0C.svg) | U+1EA0C | QALEZU LETTER KHA | `Kh` | `\K` |
| `option+g` | ![U+1EA0D](../charts/qalezu-hand/glyphs/U+1EA0D.svg) | U+1EA0D | QALEZU LETTER GHA | `gh` | `\g` |
| `option+shift+g` | ![U+1EA0D](../charts/qalezu-hand/glyphs/U+1EA0D.svg) | U+1EA0D | QALEZU LETTER GHA | `Gh` | `\G` |
| `option+z` | ![U+1EA04](../charts/qalezu-hand/glyphs/U+1EA04.svg) ![U+1EA0E](../charts/qalezu-hand/glyphs/U+1EA0E.svg) | U+1EA04 U+1EA0E | QALEZU LETTER ZAGUL; QALEZU LETTER HALZI | `zh` | `\z` |
| `option+shift+z` | ![U+1EA04](../charts/qalezu-hand/glyphs/U+1EA04.svg) ![U+1EA0E](../charts/qalezu-hand/glyphs/U+1EA0E.svg) | U+1EA04 U+1EA0E | QALEZU LETTER ZAGUL; QALEZU LETTER HALZI | `Zh` | `\Z` |
| `option+p` | ![U+1EA10](../charts/qalezu-hand/glyphs/U+1EA10.svg) ![U+1EA0E](../charts/qalezu-hand/glyphs/U+1EA0E.svg) | U+1EA10 U+1EA0E | QALEZU LETTER PA; QALEZU LETTER HALZI | `ph` | `\p` |
| `option+shift+p` | ![U+1EA10](../charts/qalezu-hand/glyphs/U+1EA10.svg) ![U+1EA0E](../charts/qalezu-hand/glyphs/U+1EA0E.svg) | U+1EA10 U+1EA0E | QALEZU LETTER PA; QALEZU LETTER HALZI | `Ph` | `\P` |
| `option+n` | ![U+1EA08](../charts/qalezu-hand/glyphs/U+1EA08.svg) ![U+1EA06](../charts/qalezu-hand/glyphs/U+1EA06.svg) | U+1EA08 U+1EA06 | QALEZU LETTER NELGIR; QALEZU LETTER GITHAR | `ng` | `\n` |
| `option+shift+n` | ![U+1EA08](../charts/qalezu-hand/glyphs/U+1EA08.svg) ![U+1EA06](../charts/qalezu-hand/glyphs/U+1EA06.svg) | U+1EA08 U+1EA06 | QALEZU LETTER NELGIR; QALEZU LETTER GITHAR | `Ng` | `\N` |
| `option+y` | ![U+1EA08](../charts/qalezu-hand/glyphs/U+1EA08.svg) ![U+1EA14](../charts/qalezu-hand/glyphs/U+1EA14.svg) | U+1EA08 U+1EA14 | QALEZU LETTER NELGIR; QALEZU LETTER YA | `ny` | `\y` |
| `option+shift+y` | ![U+1EA08](../charts/qalezu-hand/glyphs/U+1EA08.svg) ![U+1EA14](../charts/qalezu-hand/glyphs/U+1EA14.svg) | U+1EA08 U+1EA14 | QALEZU LETTER NELGIR; QALEZU LETTER YA | `Ny` | `\Y` |
| `option+x` | ![U+1EA02](../charts/qalezu-hand/glyphs/U+1EA02.svg) ![U+1EA05](../charts/qalezu-hand/glyphs/U+1EA05.svg) | U+1EA02 U+1EA05 | QALEZU LETTER TULAZ; QALEZU LETTER SELQUR | `ts` | `\x` |
| `option+shift+x` | ![U+1EA02](../charts/qalezu-hand/glyphs/U+1EA02.svg) ![U+1EA05](../charts/qalezu-hand/glyphs/U+1EA05.svg) | U+1EA02 U+1EA05 | QALEZU LETTER TULAZ; QALEZU LETTER SELQUR | `Ts` | `\X` |
| `option+h` | ![U+1EA0E](../charts/qalezu-hand/glyphs/U+1EA0E.svg) ![U+1EA00](../charts/qalezu-hand/glyphs/U+1EA00.svg) | U+1EA0E U+1EA00 | QALEZU LETTER HALZI; QALEZU LETTER LAGUN | `hl` | `\h` |
| `option+shift+h` | ![U+1EA0E](../charts/qalezu-hand/glyphs/U+1EA0E.svg) ![U+1EA00](../charts/qalezu-hand/glyphs/U+1EA00.svg) | U+1EA0E U+1EA00 | QALEZU LETTER HALZI; QALEZU LETTER LAGUN | `Hl` | `\H` |
| `option+b` | ![U+1EA11](../charts/qalezu-hand/glyphs/U+1EA11.svg) ![U+1EA0E](../charts/qalezu-hand/glyphs/U+1EA0E.svg) | U+1EA11 U+1EA0E | QALEZU LETTER BA; QALEZU LETTER HALZI | `bh` | `\b` |
| `option+shift+b` | ![U+1EA11](../charts/qalezu-hand/glyphs/U+1EA11.svg) ![U+1EA0E](../charts/qalezu-hand/glyphs/U+1EA0E.svg) | U+1EA11 U+1EA0E | QALEZU LETTER BA; QALEZU LETTER HALZI | `Bh` | `\B` |
| `option+1` |  | nothing: this script has no character for the sound |  | `aa` | `\1` |
| `option+shift+1` |  | nothing: this script has no character for the sound |  | `Aa` | `\!` |
| `option+2` |  | nothing: this script has no character for the sound |  | `ee` | `\2` |
| `option+shift+2` |  | nothing: this script has no character for the sound |  | `Ee` | `\@` |
| `option+3` |  | nothing: this script has no character for the sound |  | `ii` | `\3` |
| `option+shift+3` |  | nothing: this script has no character for the sound |  | `Ii` | `\#` |
| `option+4` |  | nothing: this script has no character for the sound |  | `oo` | `\4` |
| `option+shift+4` |  | nothing: this script has no character for the sound |  | `Oo` | `\$` |
| `option+5` |  | nothing: this script has no character for the sound |  | `uu` | `\5` |
| `option+shift+5` |  | nothing: this script has no character for the sound |  | `Uu` | `\%` |
| `option+6` |  | nothing: this script has no character for the sound |  | `ai` | `\6` |
| `option+shift+6` |  | nothing: this script has no character for the sound |  | `Ai` | `\^` |
| `option+7` |  | nothing: this script has no character for the sound |  | `au` | `\7` |
| `option+shift+7` |  | nothing: this script has no character for the sound |  | `Au` | `\&` |
| `option+8` |  | nothing: this script has no character for the sound |  | `ei` | `\8` |
| `option+shift+8` |  | nothing: this script has no character for the sound |  | `Ei` | `\*` |
| `option+9` |  | nothing: this script has no character for the sound |  | `oi` | `\9` |
| `option+shift+9` |  | nothing: this script has no character for the sound |  | `Oi` | `\(` |
| `option+0` |  | nothing: this script has no character for the sound |  | `ou` | `\0` |
| `option+shift+0` |  | nothing: this script has no character for the sound |  | `Ou` | `\)` |
| `option+-` |  | nothing: this script has no character for the sound |  | `ie` | `\-` |
| `option+shift+-` |  | nothing: this script has no character for the sound |  | `Ie` | `\_` |
| `option+=` |  | nothing: this script has no character for the sound |  | `uo` | `\=` |
| `option+shift+=` |  | nothing: this script has no character for the sound |  | `Uo` | `\+` |
| `option+[` |  | nothing: this script has no character for the sound |  | `ae` | `\[` |
| `option+shift+[` |  | nothing: this script has no character for the sound |  | `Ae` | `\{` |
| `option+]` |  | nothing: this script has no character for the sound |  | `ea` | `\]` |
| `option+shift+]` |  | nothing: this script has no character for the sound |  | `Ea` | `\}` |
| `option+a` |  | nothing: this script has no character for the sound |  | `á` | `\a` |
| `option+shift+a` |  | nothing: this script has no character for the sound |  | `Á` | `\A` |
| `option+e` |  | nothing: this script has no character for the sound |  | `é` | `\e` |
| `option+shift+e` |  | nothing: this script has no character for the sound |  | `É` | `\E` |
| `option+i` |  | nothing: this script has no character for the sound |  | `í` | `\i` |
| `option+shift+i` |  | nothing: this script has no character for the sound |  | `Í` | `\I` |
| `option+o` |  | nothing: this script has no character for the sound |  | `ó` | `\o` |
| `option+shift+o` |  | nothing: this script has no character for the sound |  | `Ó` | `\O` |
| `option+u` |  | nothing: this script has no character for the sound |  | `ú` | `\u` |
| `option+shift+u` |  | nothing: this script has no character for the sound |  | `Ú` | `\U` |
| `option+;` |  | nothing: this script has no character for the sound |  | `ä` | `\;` |
| `option+shift+;` |  | nothing: this script has no character for the sound |  | `Ä` | `\:` |
| `option+'` |  | nothing: this script has no character for the sound |  | `ë` | `\'` |
| `option+shift+'` |  | nothing: this script has no character for the sound |  | `Ë` | `\"` |
| `option+,` |  | nothing: this script has no character for the sound |  | `ï` | `\,` |
| `option+shift+,` |  | nothing: this script has no character for the sound |  | `Ï` | `\<` |
| `option+.` |  | nothing: this script has no character for the sound |  | `ö` | `\.` |
| `option+shift+.` |  | nothing: this script has no character for the sound |  | `Ö` | `\>` |
| `option+/` |  | nothing: this script has no character for the sound |  | `ü` | `\/` |
| `option+shift+/` |  | nothing: this script has no character for the sound |  | `Ü` | `\?` |
| `'` | ![U+1EA15](../charts/qalezu-hand/glyphs/U+1EA15.svg) | U+1EA15 | QALEZU LETTER CATCH | `catch` | `'` |
| `.` | ![U+1EA37](../charts/qalezu-hand/glyphs/U+1EA37.svg) | U+1EA37 | QALEZU SENTENCE END | `stop` | `.` |
| `,` | ![U+1EA38](../charts/qalezu-hand/glyphs/U+1EA38.svg) | U+1EA38 | QALEZU PAUSE | `pause` | `,` |
| `shift+,` |  | nothing: this script has no character for the sound |  | `open quote` | `<` |
| `shift+.` |  | nothing: this script has no character for the sound |  | `close quote` | `>` |
| `0` | ![U+1EA2D](../charts/qalezu-hand/glyphs/U+1EA2D.svg) | U+1EA2D | QALEZU DIGIT ZERO | `0` | `0` |
| `1` | ![U+1EA2E](../charts/qalezu-hand/glyphs/U+1EA2E.svg) | U+1EA2E | QALEZU DIGIT ONE | `1` | `1` |
| `2` | ![U+1EA2F](../charts/qalezu-hand/glyphs/U+1EA2F.svg) | U+1EA2F | QALEZU DIGIT TWO | `2` | `2` |
| `3` | ![U+1EA30](../charts/qalezu-hand/glyphs/U+1EA30.svg) | U+1EA30 | QALEZU DIGIT THREE | `3` | `3` |
| `4` | ![U+1EA31](../charts/qalezu-hand/glyphs/U+1EA31.svg) | U+1EA31 | QALEZU DIGIT FOUR | `4` | `4` |
| `5` | ![U+1EA32](../charts/qalezu-hand/glyphs/U+1EA32.svg) | U+1EA32 | QALEZU DIGIT FIVE | `5` | `5` |
| `6` | ![U+1EA33](../charts/qalezu-hand/glyphs/U+1EA33.svg) | U+1EA33 | QALEZU DIGIT SIX | `6` | `6` |
| `7` | ![U+1EA34](../charts/qalezu-hand/glyphs/U+1EA34.svg) | U+1EA34 | QALEZU DIGIT SEVEN | `7` | `7` |
| `8` | ![U+1EA35](../charts/qalezu-hand/glyphs/U+1EA35.svg) | U+1EA35 | QALEZU DIGIT EIGHT | `8` | `8` |
| `9` | ![U+1EA36](../charts/qalezu-hand/glyphs/U+1EA36.svg) | U+1EA36 | QALEZU DIGIT NINE | `9` | `9` |
| `shift+2` |  | nothing: this script has no character for the sound |  | `ten` | `@` |
| `shift+3` |  | nothing: this script has no character for the sound |  | `eleven` | `#` |
| `shift+4` |  | nothing: this script has no character for the sound |  | `twelve` | `$` |
| `shift+5` |  | nothing: this script has no character for the sound |  | `thirteen` | `%` |
| `shift+6` |  | nothing: this script has no character for the sound |  | `fourteen` | `^` |
| `shift+7` |  | nothing: this script has no character for the sound |  | `fifteen` | `&` |
