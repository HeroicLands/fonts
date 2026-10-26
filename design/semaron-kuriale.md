# Semaron Kuriale — design notes

The first hand of Semaron, the Vylarian alphabet: _Kuriale_, the chancery hand of
the court and the schools. The font draws the Vylari letters in majuscules and
minuscules, a stave per letter, written with one broad nib, each from a code point
of its own.

## The system

Every letter is built from named constants, never freehand. Units are
thousandths of the em; the font has 1000 units to the em.

| Constant   | Value               | What it governs                                                                                 |
| ---------- | ------------------- | ----------------------------------------------------------------------------------------------- |
| Body       | 449                 | The minuscule's x-height.                                                                       |
| Ascender   | 539                 | The tall minuscules: _l_, _h_, _t_, _th_ and _u_.                                               |
| Descender  | −224                | The foot of _p_, _f_, _j_ and _s_, and _g_'s tail.                                              |
| Cap height | 583                 | Every majuscule and every numeral.                                                              |
| Slant      | 12°                 | One slant for every stroke.                                                                     |
| Nib        | 86 wide, 29 thin    | One broad nib held at 30° to the line; a stroke's weight follows its direction, never pressure. |
| Oval       | width : height 0.82 | One oval, from which every bowl, arch and cup is cut.                                           |
| Reach      | 237                 | How far a branch leaves the stem, long or half.                                                 |
| Bearing    | 12                  | The white either side of a letter's ink: the hand is set close, like a medieval book hand.      |
| Space      | 24                  | The word space, about two stems.                                                                |

The vertical metrics are the shared standard of `tools/vertical.py`, Monaspace Neon's,
with the window metrics enclosing all ink, the catch where it stands on its base included.

## The method

- **A stave per letter.** Each letter is a Thuravark stave read from its branch
  table: one stem and up to four branches, each named by the side it leaves the
  stem on (forward or back), the level it leaves from and the level it ends at.
- **The majuscule** keeps the stave's skeleton at the cap height, its branches
  straight and the pen's rounding limited to the joins.
- **The minuscule** is the full pen form: each branch is a bow of the system
  oval, the stem is lengthened where it is free, and the whole is written with
  one nib at one angle.
- **A free top** starts with a straight hairline wedge. **A free foot** turns
  once into a straight exit. Every other end is the nib's own cut.
- **Unligatured.** Letters stand apart with no joins; the hand is set close and
  a letter's bearing is 12 on each side.
- **Outlines** are the strokes' polygons, united into one outline per glyph and
  rounded to the font's grid.

## The letters

There are 24 letters, each with a majuscule and a minuscule. The branch codes are
the Thuravark stave's: side (F forward, B back), the level it leaves from and the
level it ends at (T top, M middle, 0 foot).

| Letter | Branches    | Letter | Branches        |
| ------ | ----------- | ------ | --------------- |
| a      | F0T         | n      | F0T BMT         |
| b      | FT0 BT0 B0M | o      | FTM F0M BTM B0M |
| d      | F0T B0T BTM | p      | FT0 BT0         |
| e      | FTM BTM     | r      | BTM B0M         |
| f      | FT0 BT0 FMT | s      | FTM BM0         |
| g      | FTM F0M BM0 | t      | F0T B0T         |
| h      | BM0 FMT     | th     | F0T B0T FMT     |
| i      | none        | u      | B0T             |
| j      | FMT BMT     | v      | FT0 BT0 B0M FMT |
| k      | FTM F0M     | w      | BMT             |
| l      | FM0         | y      | FMT             |
| m      | FT0 BM0     | z      | FT0 B0T         |

Each is the Thuravark stave of the same name, with two readings: _y_ is
Thuravark's _j_, the glide, and _j_ is the letter Tharavarkon adds, a stem forking
into two arms. Thuravark's own _y_ is the vowel _i_ here. On _f_ and _th_ the
forward middle-to-top branch is the **aspirate hook**, part of the glyph, not an
arm.

## The marks

- **The curl** marks a long vowel: a small arch of the nib seated on the vowel,
  with hairline feet and a swelling crown. The long _a_, _e_, _i_, _o_ and _u_
  are drawn, each in both cases.
- **The catch** marks a glottal stop: a grave stroke over the letter it follows.
  It has no advance, so it never adds space. It is positioned by a GPOS
  mark-to-base anchor on every base: centred over an x-height letter, at the
  upper right of a tall stem, and to the right of the curl on a long vowel.
- **The point** is the one pause mark: the nib drawn one nib's width straight
  down, a diamond at mid-height.
- **The numerals** 0 to 9 are a stem at the cap height with up to four limbs,
  each a bow falling outward; the limbs are the binary digits 8, 4 (forward) and
  2, 1 (back); nought is the stem with a closed ring at its foot.
- **The box** is `.notdef` and `notdef.box`: a stem between two points.

## The characters

The face draws each letter, long vowel, numeral, the point and the catch from its
own code point, U+F0200 to U+F02FF, and from nothing else: a Latin letter, digit or
mark draws the box. The long vowels are letters in their own right, the curl drawn
into each. The catch is a mark, set by GPOS (`mark`) over the letter before it;
with no letter before it, a `ccmp` substitution draws it as the box. The
default-ignorables map to an empty glyph and draw nothing.

A note writes Vylari in roman, and the `semaron` encoding turns the
spelling into these code points:

| Spelled                            | Written                                                                 |
| ---------------------------------- | ----------------------------------------------------------------------- |
| `a`                                | The minuscule. A capital `A` is the majuscule, with no mark for case.   |
| `th`                               | The one letter _th_.                                                    |
| `ch`                               | The letters _t_, _s_ and _h_, because the script has no _c_.            |
| `aa`, `ii`, `uu`                   | The long vowel.                                                         |
| `ee`, `oo`                         | Two plain vowels.                                                       |
| `á é í ó ú`, `ë`                   | The plain vowel: Semaron writes no stress.                              |
| `q`                                | The letter _k_.                                                         |
| `y` before a vowel                 | The glide _y_. Anywhere else it is the vowel _i_.                       |
| `'`, `’`, `` ` ``, `-`             | The catch, set on the letter before it. With no letter before, the box. |
| `.` `?` `!` `!!` `,`               | The point, each told apart from the others by invisible marks.          |
| `« »` `‹ ›` `—` `…` `/` `//` `{ }` | Nothing: invisible marks alone, so decoding restores them.              |
| `0`–`9`                            | The numerals.                                                           |
| `c`, `x`, and any other character  | Refused by the encoding; set in the face, it prints the box.            |

## The checks

- `tools/semaron-kuriale/check_font.py` loads the built font and confirms the
  character map, the outlines, the names, the box rule, the catch's mark class
  and anchors, the win metrics and the `.woff2`.
- `tools/semaron-kuriale/guard.py` writes every form of the Vylari lexicon, read
  from the frontmatter of the language note, and a set of fixtures for each
  spelling rule through the `semaron` encoding, shapes them, and asserts the
  glyph sequences. `tools/codepoints.py` checks that the face draws its own code
  points and nothing else, and that no substitution turns one character into
  another: _i_ written twice is two _i_.
- `tools/prove_guards.py` proves the guard fails the font with its GSUB removed,
  and with its GPOS removed.
- `tools/notdef_box.py` and `tools/font_names.py` run on the font as on every
  other.
- `tools/semaron-kuriale/specimens.py` renders `specimens/semaron-kuriale/`: the
  24 majuscules one to a cell, the glyph chart, and the Vylari texts at display
  size and at 18 and 24 px.
