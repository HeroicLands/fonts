# HL Vedyakshara cheatsheet

HL Vedyakshara types Vedyakshara Classical by sound. It is a US keyboard that writes the Vedyakshara script: the key for a sound types that sound's Vedyakshara character, so `t` types the script's t and Option+T types its th. You type the sounds of a word one after another, as you would in English.

![HL Vedyakshara on an ANSI keyboard](vedyakshara.png)

A printable copy is [vedyakshara.svg](vedyakshara.svg) and [vedyakshara.png](vedyakshara.png).

## Reading the keys

- `t` is the key alone. `shift+t` is Shift and the key.
- `option+t` is Option and the key on a Mac, and AltGr and the key on Windows and Linux. AltGr is the right Alt key (on a keyboard without one, hold Ctrl and Alt together). `option+shift+t` adds Shift.
- The Sound column is the roman spelling of the sound a key stands for. A key marked _nothing_ types nothing in this script.
- Character names and code points identify each character exactly, for a program or a character viewer.
- The Emacs column is what to type in the Emacs input method `heroiclands-vedyakshara`, where Option is a backslash.

## Installing the layout

The layout is a file per platform, named below. [The README](../README.md#installing-a-keyboard-layout) walks through installing each.

- macOS: `keyboards/macos/HeroicLands.bundle`, input source **HL Vedyakshara**.
- Windows: `keyboards/windows/vedyakshara.klc`, the Microsoft Keyboard Layout Creator source of **HL Vedyakshara**.
- Linux: `keyboards/linux/hl_vedyakshara`, the XKB symbols of **HL Vedyakshara**.
- Emacs: `keyboards/emacs/heroiclands-vedyakshara.el`, the input method `heroiclands-vedyakshara`.

## Signs

These keys type no sound. They type in HL Vedyakshara alone.

| Key | Emacs | Sign | Layout | Glyph | Code point | Name |
| --- | --- | --- | --- | --- | --- | --- |
| `shift+a` | `A` | independent a | HL Vedyakshara | ![U+F0420](../charts/vedyakshara-classical/glyphs/U+F0420.svg) | U+F0420 | VEDYAKSHARA LETTER A |
| `shift+i` | `I` | independent i | HL Vedyakshara | ![U+F0421](../charts/vedyakshara-classical/glyphs/U+F0421.svg) | U+F0421 | VEDYAKSHARA LETTER I |
| `shift+u` | `U` | independent u | HL Vedyakshara | ![U+F0422](../charts/vedyakshara-classical/glyphs/U+F0422.svg) | U+F0422 | VEDYAKSHARA LETTER U |
| `shift+e` | `E` | independent e | HL Vedyakshara | ![U+F0423](../charts/vedyakshara-classical/glyphs/U+F0423.svg) | U+F0423 | VEDYAKSHARA LETTER E |
| `shift+o` | `O` | independent o | HL Vedyakshara | ![U+F0424](../charts/vedyakshara-classical/glyphs/U+F0424.svg) | U+F0424 | VEDYAKSHARA LETTER O |
| `option+shift+w` | `\W` | literal open | HL Vedyakshara | ⟦ | U+27E6 | LEFT WHITE SQUARE BRACKET |
| `option+shift+l` | `\L` | literal close | HL Vedyakshara | ⟧ | U+27E7 | RIGHT WHITE SQUARE BRACKET |

## Keys a platform cannot carry

A Windows key holds at most four UTF-16 code units and a Linux key one character, so a sound this script spells with more types nothing there. macOS and Emacs carry every key.

| Key | Sound | Script | Platform | Why |
| --- | --- | --- | --- | --- |
| `f` | `f` | Vedyakshara | Linux | 2 code points; an XKB key types one |
| `option+t` | `th` | Vedyakshara | Windows | 6 UTF-16 code units; an MSKLC ligature holds 4 |
| `option+t` | `th` | Vedyakshara | Linux | 3 code points; an XKB key types one |
| `option+d` | `dh` | Vedyakshara | Windows | 6 UTF-16 code units; an MSKLC ligature holds 4 |
| `option+d` | `dh` | Vedyakshara | Linux | 3 code points; an XKB key types one |
| `option+p` | `ph` | Vedyakshara | Windows | 6 UTF-16 code units; an MSKLC ligature holds 4 |
| `option+p` | `ph` | Vedyakshara | Linux | 3 code points; an XKB key types one |
| `option+x` | `ts` | Vedyakshara | Windows | 6 UTF-16 code units; an MSKLC ligature holds 4 |
| `option+x` | `ts` | Vedyakshara | Linux | 3 code points; an XKB key types one |
| `option+h` | `hl` | Vedyakshara | Windows | 6 UTF-16 code units; an MSKLC ligature holds 4 |
| `option+h` | `hl` | Vedyakshara | Linux | 3 code points; an XKB key types one |
| `option+2` | `ee` | Vedyakshara | Linux | 2 code points; an XKB key types one |
| `option+3` | `ii` | Vedyakshara | Linux | 2 code points; an XKB key types one |
| `option+4` | `oo` | Vedyakshara | Linux | 2 code points; an XKB key types one |
| `option+5` | `uu` | Vedyakshara | Linux | 2 code points; an XKB key types one |
| `option+8` | `ei` | Vedyakshara | Linux | 2 code points; an XKB key types one |
| `option+9` | `oi` | Vedyakshara | Linux | 2 code points; an XKB key types one |
| `option+0` | `ou` | Vedyakshara | Linux | 2 code points; an XKB key types one |
| `option+-` | `ie` | Vedyakshara | Linux | 2 code points; an XKB key types one |
| `option+=` | `uo` | Vedyakshara | Linux | 2 code points; an XKB key types one |

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
| `b` | ![U+F040C](../charts/vedyakshara-classical/glyphs/U+F040C.svg) | U+F040C | VEDYAKSHARA LETTER BA | `b` | `b` |
| `shift+b` |  | nothing: this script has no character for the sound |  | `B` | `B` |
| `d` | ![U+F0409](../charts/vedyakshara-classical/glyphs/U+F0409.svg) | U+F0409 | VEDYAKSHARA LETTER DA | `d` | `d` |
| `shift+d` |  | nothing: this script has no character for the sound |  | `D` | `D` |
| `e` | ![U+F0431](../charts/vedyakshara-classical/glyphs/U+F0431.svg) | U+F0431 | VEDYAKSHARA VOWEL SIGN E | `e` | `e` |
| `shift+e` |  | nothing: this script has no character for the sound |  | `E` | `E` |
| `f` | ![U+F040B](../charts/vedyakshara-classical/glyphs/U+F040B.svg) ![U+F0439](../charts/vedyakshara-classical/glyphs/U+F0439.svg) | U+F040B U+F0439 | VEDYAKSHARA LETTER PA; VEDYAKSHARA SIGN SOFT DOT | `f` | `f` |
| `shift+f` |  | nothing: this script has no character for the sound |  | `F` | `F` |
| `g` | ![U+F0402](../charts/vedyakshara-classical/glyphs/U+F0402.svg) | U+F0402 | VEDYAKSHARA LETTER GA | `g` | `g` |
| `shift+g` |  | nothing: this script has no character for the sound |  | `G` | `G` |
| `h` | ![U+F0415](../charts/vedyakshara-classical/glyphs/U+F0415.svg) | U+F0415 | VEDYAKSHARA LETTER HA | `h` | `h` |
| `shift+h` |  | nothing: this script has no character for the sound |  | `H` | `H` |
| `i` | ![U+F0430](../charts/vedyakshara-classical/glyphs/U+F0430.svg) | U+F0430 | VEDYAKSHARA VOWEL SIGN I | `i` | `i` |
| `shift+i` |  | nothing: this script has no character for the sound |  | `I` | `I` |
| `j` | ![U+F0406](../charts/vedyakshara-classical/glyphs/U+F0406.svg) | U+F0406 | VEDYAKSHARA LETTER JA | `j` | `j` |
| `shift+j` |  | nothing: this script has no character for the sound |  | `J` | `J` |
| `k` | ![U+F0400](../charts/vedyakshara-classical/glyphs/U+F0400.svg) | U+F0400 | VEDYAKSHARA LETTER KA | `k` | `k` |
| `shift+k` |  | nothing: this script has no character for the sound |  | `K` | `K` |
| `l` | ![U+F0411](../charts/vedyakshara-classical/glyphs/U+F0411.svg) | U+F0411 | VEDYAKSHARA LETTER LA | `l` | `l` |
| `shift+l` |  | nothing: this script has no character for the sound |  | `L` | `L` |
| `m` | ![U+F040E](../charts/vedyakshara-classical/glyphs/U+F040E.svg) | U+F040E | VEDYAKSHARA LETTER MA | `m` | `m` |
| `shift+m` |  | nothing: this script has no character for the sound |  | `M` | `M` |
| `n` | ![U+F040A](../charts/vedyakshara-classical/glyphs/U+F040A.svg) | U+F040A | VEDYAKSHARA LETTER NA | `n` | `n` |
| `shift+n` |  | nothing: this script has no character for the sound |  | `N` | `N` |
| `o` | ![U+F0434](../charts/vedyakshara-classical/glyphs/U+F0434.svg) | U+F0434 | VEDYAKSHARA VOWEL SIGN O | `o` | `o` |
| `shift+o` |  | nothing: this script has no character for the sound |  | `O` | `O` |
| `p` | ![U+F040B](../charts/vedyakshara-classical/glyphs/U+F040B.svg) | U+F040B | VEDYAKSHARA LETTER PA | `p` | `p` |
| `shift+p` |  | nothing: this script has no character for the sound |  | `P` | `P` |
| `q` |  | nothing: this script has no character for the sound |  | `q` | `q` |
| `shift+q` |  | nothing: this script has no character for the sound |  | `Q` | `Q` |
| `r` | ![U+F0410](../charts/vedyakshara-classical/glyphs/U+F0410.svg) | U+F0410 | VEDYAKSHARA LETTER RA | `r` | `r` |
| `shift+r` |  | nothing: this script has no character for the sound |  | `R` | `R` |
| `s` | ![U+F0414](../charts/vedyakshara-classical/glyphs/U+F0414.svg) | U+F0414 | VEDYAKSHARA LETTER SA | `s` | `s` |
| `shift+s` |  | nothing: this script has no character for the sound |  | `S` | `S` |
| `t` | ![U+F0408](../charts/vedyakshara-classical/glyphs/U+F0408.svg) | U+F0408 | VEDYAKSHARA LETTER TA | `t` | `t` |
| `shift+t` |  | nothing: this script has no character for the sound |  | `T` | `T` |
| `u` | ![U+F0433](../charts/vedyakshara-classical/glyphs/U+F0433.svg) | U+F0433 | VEDYAKSHARA VOWEL SIGN U | `u` | `u` |
| `shift+u` |  | nothing: this script has no character for the sound |  | `U` | `U` |
| `v` | ![U+F0412](../charts/vedyakshara-classical/glyphs/U+F0412.svg) | U+F0412 | VEDYAKSHARA LETTER VA | `v` | `v` |
| `shift+v` |  | nothing: this script has no character for the sound |  | `V` | `V` |
| `w` |  | nothing: this script has no character for the sound |  | `w` | `w` |
| `shift+w` |  | nothing: this script has no character for the sound |  | `W` | `W` |
| `y` | ![U+F040F](../charts/vedyakshara-classical/glyphs/U+F040F.svg) | U+F040F | VEDYAKSHARA LETTER YA | `y` | `y` |
| `shift+y` |  | nothing: this script has no character for the sound |  | `Y` | `Y` |
| `z` |  | nothing: this script has no character for the sound |  | `z` | `z` |
| `shift+z` |  | nothing: this script has no character for the sound |  | `Z` | `Z` |
| `option+c` | ![U+F0405](../charts/vedyakshara-classical/glyphs/U+F0405.svg) | U+F0405 | VEDYAKSHARA LETTER CHA | `ch` | `\c` |
| `option+shift+c` |  | nothing: this script has no character for the sound |  | `Ch` | `\C` |
| `option+s` | ![U+F0413](../charts/vedyakshara-classical/glyphs/U+F0413.svg) | U+F0413 | VEDYAKSHARA LETTER SHA | `sh` | `\s` |
| `option+shift+s` |  | nothing: this script has no character for the sound |  | `Sh` | `\S` |
| `option+t` | ![U+F0408](../charts/vedyakshara-classical/glyphs/U+F0408.svg) ![U+F0438](../charts/vedyakshara-classical/glyphs/U+F0438.svg) ![U+F0415](../charts/vedyakshara-classical/glyphs/U+F0415.svg) | U+F0408 U+F0438 U+F0415 | VEDYAKSHARA LETTER TA; VEDYAKSHARA SIGN CUT; VEDYAKSHARA LETTER HA | `th` | `\t` |
| `option+shift+t` |  | nothing: this script has no character for the sound |  | `Th` | `\T` |
| `option+d` | ![U+F0409](../charts/vedyakshara-classical/glyphs/U+F0409.svg) ![U+F0438](../charts/vedyakshara-classical/glyphs/U+F0438.svg) ![U+F0415](../charts/vedyakshara-classical/glyphs/U+F0415.svg) | U+F0409 U+F0438 U+F0415 | VEDYAKSHARA LETTER DA; VEDYAKSHARA SIGN CUT; VEDYAKSHARA LETTER HA | `dh` | `\d` |
| `option+shift+d` |  | nothing: this script has no character for the sound |  | `Dh` | `\D` |
| `option+k` | ![U+F0401](../charts/vedyakshara-classical/glyphs/U+F0401.svg) | U+F0401 | VEDYAKSHARA LETTER KHA | `kh` | `\k` |
| `option+shift+k` |  | nothing: this script has no character for the sound |  | `Kh` | `\K` |
| `option+g` | ![U+F0403](../charts/vedyakshara-classical/glyphs/U+F0403.svg) | U+F0403 | VEDYAKSHARA LETTER GHA | `gh` | `\g` |
| `option+shift+g` |  | nothing: this script has no character for the sound |  | `Gh` | `\G` |
| `option+z` |  | nothing: this script has no character for the sound |  | `zh` | `\z` |
| `option+shift+z` |  | nothing: this script has no character for the sound |  | `Zh` | `\Z` |
| `option+p` | ![U+F040B](../charts/vedyakshara-classical/glyphs/U+F040B.svg) ![U+F0438](../charts/vedyakshara-classical/glyphs/U+F0438.svg) ![U+F0415](../charts/vedyakshara-classical/glyphs/U+F0415.svg) | U+F040B U+F0438 U+F0415 | VEDYAKSHARA LETTER PA; VEDYAKSHARA SIGN CUT; VEDYAKSHARA LETTER HA | `ph` | `\p` |
| `option+shift+p` |  | nothing: this script has no character for the sound |  | `Ph` | `\P` |
| `option+n` | ![U+F0404](../charts/vedyakshara-classical/glyphs/U+F0404.svg) | U+F0404 | VEDYAKSHARA LETTER NGA | `ng` | `\n` |
| `option+shift+n` |  | nothing: this script has no character for the sound |  | `Ng` | `\N` |
| `option+y` | ![U+F0407](../charts/vedyakshara-classical/glyphs/U+F0407.svg) | U+F0407 | VEDYAKSHARA LETTER NYA | `ny` | `\y` |
| `option+shift+y` |  | nothing: this script has no character for the sound |  | `Ny` | `\Y` |
| `option+x` | ![U+F0408](../charts/vedyakshara-classical/glyphs/U+F0408.svg) ![U+F0438](../charts/vedyakshara-classical/glyphs/U+F0438.svg) ![U+F0414](../charts/vedyakshara-classical/glyphs/U+F0414.svg) | U+F0408 U+F0438 U+F0414 | VEDYAKSHARA LETTER TA; VEDYAKSHARA SIGN CUT; VEDYAKSHARA LETTER SA | `ts` | `\x` |
| `option+shift+x` |  | nothing: this script has no character for the sound |  | `Ts` | `\X` |
| `option+h` | ![U+F0415](../charts/vedyakshara-classical/glyphs/U+F0415.svg) ![U+F0438](../charts/vedyakshara-classical/glyphs/U+F0438.svg) ![U+F0411](../charts/vedyakshara-classical/glyphs/U+F0411.svg) | U+F0415 U+F0438 U+F0411 | VEDYAKSHARA LETTER HA; VEDYAKSHARA SIGN CUT; VEDYAKSHARA LETTER LA | `hl` | `\h` |
| `option+shift+h` |  | nothing: this script has no character for the sound |  | `Hl` | `\H` |
| `option+b` | ![U+F040D](../charts/vedyakshara-classical/glyphs/U+F040D.svg) | U+F040D | VEDYAKSHARA LETTER BHA | `bh` | `\b` |
| `option+shift+b` |  | nothing: this script has no character for the sound |  | `Bh` | `\B` |
| `option+1` |  | nothing: this script has no character for the sound |  | `aa` | `\1` |
| `option+shift+1` |  | nothing: this script has no character for the sound |  | `Aa` | `\!` |
| `option+2` | ![U+F0431](../charts/vedyakshara-classical/glyphs/U+F0431.svg) ![U+F0431](../charts/vedyakshara-classical/glyphs/U+F0431.svg) | U+F0431 U+F0431 | VEDYAKSHARA VOWEL SIGN E; VEDYAKSHARA VOWEL SIGN E | `ee` | `\2` |
| `option+shift+2` |  | nothing: this script has no character for the sound |  | `Ee` | `\@` |
| `option+3` | ![U+F0430](../charts/vedyakshara-classical/glyphs/U+F0430.svg) ![U+F0430](../charts/vedyakshara-classical/glyphs/U+F0430.svg) | U+F0430 U+F0430 | VEDYAKSHARA VOWEL SIGN I; VEDYAKSHARA VOWEL SIGN I | `ii` | `\3` |
| `option+shift+3` |  | nothing: this script has no character for the sound |  | `Ii` | `\#` |
| `option+4` | ![U+F0434](../charts/vedyakshara-classical/glyphs/U+F0434.svg) ![U+F0434](../charts/vedyakshara-classical/glyphs/U+F0434.svg) | U+F0434 U+F0434 | VEDYAKSHARA VOWEL SIGN O; VEDYAKSHARA VOWEL SIGN O | `oo` | `\4` |
| `option+shift+4` |  | nothing: this script has no character for the sound |  | `Oo` | `\$` |
| `option+5` | ![U+F0433](../charts/vedyakshara-classical/glyphs/U+F0433.svg) ![U+F0433](../charts/vedyakshara-classical/glyphs/U+F0433.svg) | U+F0433 U+F0433 | VEDYAKSHARA VOWEL SIGN U; VEDYAKSHARA VOWEL SIGN U | `uu` | `\5` |
| `option+shift+5` |  | nothing: this script has no character for the sound |  | `Uu` | `\%` |
| `option+6` | ![U+F0432](../charts/vedyakshara-classical/glyphs/U+F0432.svg) | U+F0432 | VEDYAKSHARA VOWEL SIGN AI | `ai` | `\6` |
| `option+shift+6` |  | nothing: this script has no character for the sound |  | `Ai` | `\^` |
| `option+7` | ![U+F0435](../charts/vedyakshara-classical/glyphs/U+F0435.svg) | U+F0435 | VEDYAKSHARA VOWEL SIGN AU | `au` | `\7` |
| `option+shift+7` |  | nothing: this script has no character for the sound |  | `Au` | `\&` |
| `option+8` | ![U+F0431](../charts/vedyakshara-classical/glyphs/U+F0431.svg) ![U+F0430](../charts/vedyakshara-classical/glyphs/U+F0430.svg) | U+F0431 U+F0430 | VEDYAKSHARA VOWEL SIGN E; VEDYAKSHARA VOWEL SIGN I | `ei` | `\8` |
| `option+shift+8` |  | nothing: this script has no character for the sound |  | `Ei` | `\*` |
| `option+9` | ![U+F0434](../charts/vedyakshara-classical/glyphs/U+F0434.svg) ![U+F0430](../charts/vedyakshara-classical/glyphs/U+F0430.svg) | U+F0434 U+F0430 | VEDYAKSHARA VOWEL SIGN O; VEDYAKSHARA VOWEL SIGN I | `oi` | `\9` |
| `option+shift+9` |  | nothing: this script has no character for the sound |  | `Oi` | `\(` |
| `option+0` | ![U+F0434](../charts/vedyakshara-classical/glyphs/U+F0434.svg) ![U+F0433](../charts/vedyakshara-classical/glyphs/U+F0433.svg) | U+F0434 U+F0433 | VEDYAKSHARA VOWEL SIGN O; VEDYAKSHARA VOWEL SIGN U | `ou` | `\0` |
| `option+shift+0` |  | nothing: this script has no character for the sound |  | `Ou` | `\)` |
| `option+-` | ![U+F0430](../charts/vedyakshara-classical/glyphs/U+F0430.svg) ![U+F0431](../charts/vedyakshara-classical/glyphs/U+F0431.svg) | U+F0430 U+F0431 | VEDYAKSHARA VOWEL SIGN I; VEDYAKSHARA VOWEL SIGN E | `ie` | `\-` |
| `option+shift+-` |  | nothing: this script has no character for the sound |  | `Ie` | `\_` |
| `option+=` | ![U+F0433](../charts/vedyakshara-classical/glyphs/U+F0433.svg) ![U+F0434](../charts/vedyakshara-classical/glyphs/U+F0434.svg) | U+F0433 U+F0434 | VEDYAKSHARA VOWEL SIGN U; VEDYAKSHARA VOWEL SIGN O | `uo` | `\=` |
| `option+shift+=` |  | nothing: this script has no character for the sound |  | `Uo` | `\+` |
| `option+[` | ![U+F0431](../charts/vedyakshara-classical/glyphs/U+F0431.svg) | U+F0431 | VEDYAKSHARA VOWEL SIGN E | `ae` | `\[` |
| `option+shift+[` |  | nothing: this script has no character for the sound |  | `Ae` | `\{` |
| `option+]` | ![U+F0431](../charts/vedyakshara-classical/glyphs/U+F0431.svg) | U+F0431 | VEDYAKSHARA VOWEL SIGN E | `ea` | `\]` |
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
| `'` | ![U+F0438](../charts/vedyakshara-classical/glyphs/U+F0438.svg) | U+F0438 | VEDYAKSHARA SIGN CUT | `catch` | `'` |
| `.` | ![U+F0451](../charts/vedyakshara-classical/glyphs/U+F0451.svg) | U+F0451 | VEDYAKSHARA FULL STOP | `stop` | `.` |
| `,` | ![U+F0450](../charts/vedyakshara-classical/glyphs/U+F0450.svg) | U+F0450 | VEDYAKSHARA PAUSE | `pause` | `,` |
| `shift+,` |  | nothing: this script has no character for the sound |  | `open quote` | `<` |
| `shift+.` |  | nothing: this script has no character for the sound |  | `close quote` | `>` |
| `0` | ![U+F0440](../charts/vedyakshara-classical/glyphs/U+F0440.svg) | U+F0440 | VEDYAKSHARA DIGIT ZERO | `0` | `0` |
| `1` | ![U+F0441](../charts/vedyakshara-classical/glyphs/U+F0441.svg) | U+F0441 | VEDYAKSHARA DIGIT ONE | `1` | `1` |
| `2` | ![U+F0442](../charts/vedyakshara-classical/glyphs/U+F0442.svg) | U+F0442 | VEDYAKSHARA DIGIT TWO | `2` | `2` |
| `3` | ![U+F0443](../charts/vedyakshara-classical/glyphs/U+F0443.svg) | U+F0443 | VEDYAKSHARA DIGIT THREE | `3` | `3` |
| `4` | ![U+F0444](../charts/vedyakshara-classical/glyphs/U+F0444.svg) | U+F0444 | VEDYAKSHARA DIGIT FOUR | `4` | `4` |
| `5` | ![U+F0445](../charts/vedyakshara-classical/glyphs/U+F0445.svg) | U+F0445 | VEDYAKSHARA DIGIT FIVE | `5` | `5` |
| `6` | ![U+F0446](../charts/vedyakshara-classical/glyphs/U+F0446.svg) | U+F0446 | VEDYAKSHARA DIGIT SIX | `6` | `6` |
| `7` | ![U+F0447](../charts/vedyakshara-classical/glyphs/U+F0447.svg) | U+F0447 | VEDYAKSHARA DIGIT SEVEN | `7` | `7` |
| `8` | ![U+F0448](../charts/vedyakshara-classical/glyphs/U+F0448.svg) | U+F0448 | VEDYAKSHARA DIGIT EIGHT | `8` | `8` |
| `9` | ![U+F0449](../charts/vedyakshara-classical/glyphs/U+F0449.svg) | U+F0449 | VEDYAKSHARA DIGIT NINE | `9` | `9` |
| `shift+2` |  | nothing: this script has no character for the sound |  | `ten` | `@` |
| `shift+3` |  | nothing: this script has no character for the sound |  | `eleven` | `#` |
| `shift+4` |  | nothing: this script has no character for the sound |  | `twelve` | `$` |
| `shift+5` |  | nothing: this script has no character for the sound |  | `thirteen` | `%` |
| `shift+6` |  | nothing: this script has no character for the sound |  | `fourteen` | `^` |
| `shift+7` |  | nothing: this script has no character for the sound |  | `fifteen` | `&` |
