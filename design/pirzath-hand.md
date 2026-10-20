# Pirzath Hand — design notes

The hand form of Pirzath, _milgath_: the everyday writing of the Khazari of
thalorna, flowing, slanted and joined, in ink, chalk or scratched with a
stylus. The hand writes the same letters as the carved face, as a cursive Latin
hand writes the Roman capitals: the forms differ in how the letters are made,
never in which letters there are. One font serves every medium.

The design sources are the owner's handwritten alphabet,
`design/pirzath-hand/owner-alphabet.jpg`, and the owner's sheet of changes,
`design/pirzath-hand/owner-changes-1.jpg`, which governs for every letter it
shows. A sketch fixes a letter's identity — its topology, its strokes, its
marks — and the finished form follows the system below.

## The system

Every letter is built from a few named constants, never freehand. Units are
thousandths of the em; the font has 1000 units to the em.

| Constant      | Value                                      | What it governs                                                                                              |
| ------------- | ------------------------------------------ | ------------------------------------------------------------------------------------------------------------ |
| Body          | 400                                        | The height of a consonant, the script's x-height.                                                            |
| Vowel         | 260                                        | The height of a vowel, 0.65 of the body.                                                                     |
| Ascender      | 480                                        | The looped heads of _l_ and _r_: 1.2 of the body, the tallest any letter stands.                             |
| Descender     | −300                                       | The loops of _ng_ and _j_ below the line.                                                                    |
| Slant         | 12°                                        | One slant for every stroke.                                                                                  |
| Pen           | thin 26, thick 48                          | A pointed pen with a gentle swell: thick on a stroke falling along the slant, thin on a rising or level one. |
| Mark weight   | 34                                         | One middle weight for every straight mark, so it survives reading size.                                      |
| Oval          | width : height 0.70                        | One proportion for every bowl; arches and bowls are its halves.                                              |
| Widths        | round 280, trough 240, cup 180, narrow 150 | The standard widths from which every curve is cut at the oval's proportion.                                  |
| Join heights  | exit 40, entry 140                         | Where the connector leaves one letter and enters the next.                                                   |
| Join headings | exit 30°, entry 50°                        | The angles of the join, upright.                                                                             |
| Space         | 230                                        | The width of a space.                                                                                        |

The vertical metrics follow the system: ascender 480, descender −300, with the
line gap and the window metrics clearing the ink of the dots and loops.

## The method

- **Measured slant.** Every straight stem is an explicit straight line, and the
  turns ease into it, so each stem leans the slant to within a degree. Curves
  are never refitted together with the stems they feed.
- **No jogs.** An entry is one straight run or one gentle turn into the first
  stroke; an entry never rises, steepens and turns through a second bend.
- **Curved joins.** The connector is one concave curve that leaves a letter at
  30° and arrives at the next at 50°, so it never lines up with the stroke it
  feeds and never reads as a strike.
- **One drawing per letter.** The isolated glyph, the lifted letter and the
  joined letter are the same drawing; only the connector differs. A letter is
  drawn once and moved into place, never rescaled or re-stroked in context.
- **Families share parts exactly.** _g_ and _gh_ are one drawing and _gh_ adds
  the strike; _kh_ carries the same strike in the same place; a quotation mark
  is the _g_ drawing plus two parallel lines; _m_ and _n_ are mirrors.
- **Smooth outlines.** Each stroke is a centreline through a few knots with
  directions, run through Hobby's algorithm, refitted as one curvature-
  continuous B-spline and stroked with the pen. The stroked outlines are united
  and refitted with a few long cubics, then written as quadratic curves on the
  integer grid, with the points beside each straight edge kept on its tangent.

## The letters

- **The tent family:** _p_, _b_, _f_, _v_ share one arch and one foot; _b_ adds
  a pole inside it, _f_ a notch on its fore side, _v_ both.
- **The trough family:** _t_, _d_, _th_, _dh_ share the trough, a cursive u;
  they differ by a pole, a notch or the right angle of _dh_.
- **The cups:** _n_ and _m_ are mirrors, rounded like a cursive w; _ny_ is _n_
  with a stroke.
- **The ovals:** _g_, _gh_, _k_, _kh_, _s_, _sh_ and _z_, _zh_ are cut from the
  system oval. _gh_ and _kh_ add the same strike to _g_ and _k_; _z_ is a plain
  cursive x; _zh_ adds a mark to it.
- **The looped heads:** _l_, _r_, _h_, _hl_, _ch_ rise to the ascender.
- **The vowels:** _a_, _e_, _i_, _o_, _u_ stand at vowel height. A long vowel is
  the same vowel with one dot above; a pair (_ai_, _au_, _ei_, _oi_, _ou_) is
  two vowels joined on the line inside one glyph.
- **The lost letters:** _ts_, _j_, _q_, _ng_, the catch, _w_ and _y_ have their
  own drawings. _j_ and _ng_ loop below the line; _q_ stands apart from _ng_.
- **Doubled consonants:** every consonant has a doubled glyph, the letter once
  with a straight line beneath it; on a descender the line stands beside the
  loop.

## The marks

- The sentence end is a wave at mark weight; _!_ is two waves; the pause and
  the dash are two straight strokes at opposite slopes.
- The opening and closing quotation marks are the _g_ drawing with two
  parallel lines, rising across the bowl's upper right to open and falling
  across its lower right to close. Each stands off the join line and keeps a
  fixed room between itself and the word. Each is one connected drawing.
- The numerals 0 to 15 are a stem standing off the line with tally ticks: 8 high
  on the fore side, 4 lower on the fore side, 2 on the back side and 1 at the
  back of the foot; the bare stem is nought.
- `.notdef`, and the box that every character the typing does not use maps to, is the cursive _l_ between two dots.

## The joined forms

Lifted writing ends each letter in a short straight terminal on the join angle.
With the stylistic set `ss01`, the concave connector runs from the exit of one
letter to the entry of the next, and the same drawing carries on across it.

The connector is cut at the advance edge that the two letters share. A joining
letter has three joined forms beside its plain one, all with the same advance:

| Form    | Entry | Exit  |
| ------- | ----- | ----- |
| plain   | short | short |
| `.init` | short | long  |
| `.medi` | long  | long  |
| `.fina` | long  | short |

A long end carries its half of the connector and runs a couple of units past
the edge, so two neighbouring glyphs meet without a gap and without a bump. A
joined line shaped by HarfBuzz matches the composed joined line of the drawing
to within about one unit, with the whole-unit advances the only difference.
Letters that stand off the line — the marks, the quotation marks, the numerals,
the space and the box — have no joined forms and break the join.

## The typing

The hand types as the carved face does, in the Latin spelling of the setting: _ngh_ is _n_ and _gh_, _ay_, _ey_ and _oy_ are the vowel pairs, and a length mark on a pair is a dot positioned over the pair.

- Digraphs read longest first: _th_, _dh_, _kh_, _gh_, then _sh_, _zh_, _ch_,
  _ts_, _ng_, _ny_, _hl_. A _gh_ wins over _ng_ before an _h_, so _ngh_ is _n_
  and _gh_.
- An acute vowel is the long-vowel glyph, from the precomposed letter or the
  vowel with a combining acute. An acute left on a vowel pair is a separate
  length mark above the pair.
- A consonant or digraph written twice is its doubled glyph; the first letter of
  a doubled digraph (_tth_, _ddh_, _kkh_, _ggh_, _ssh_, _zzh_, _cch_, _tts_,
  _nng_, _nny_, _hhl_) counts as the digraph.
- _y_ is the glide before a vowel and the vowel _i_ elsewhere; _ay_, _ey_ and
  _oy_ are the pairs _ai_, _ei_ and _oi_. `'` and `’` are the catch.
- `"` opens after a space or at the start and closes elsewhere; `[`, `«`, `“` and
  `<<` open; `]`, `»`, `”` and `>>` close. `!` and `¡` are the imperative.
- `0`–`9` and `@ # $ % ^ &` are the numerals 0–15. `?`, `;` and `:` draw the
  box, as does every other character the typing does not use.
- The default-ignorable characters draw nothing: they map to an empty glyph,
  and a `ccmp` substitution turns that into a second empty glyph, so the
  shaper does not replace them with the visible space.

The sentence end stands with no space on either side; the next sentence begins
straight after it. That is how Pirzath is written, not a rule of the font: a
space typed there is drawn.

## The checks

- `tools/pirzath-hand/check_font.py` confirms the character map against the
  carved face's rulings, the outlines of every mapped glyph, the empty
  ignorables, the zero-advance length mark, the name table, the line metrics
  and, for every joining letter, the four forms with one advance and one
  connector face at the advance edge.
- `tools/pirzath-hand/guard.py` shapes every Khazari lexicon form and the
  fixtures, lifted and joined, and asserts the glyph sequence and the joined
  form of each letter.
- `tools/prove_guards.py` proves the guard fails the font without its layout.
- `tools/pirzath-hand/specimens.py` renders the glyph chart, the texts lifted
  and joined, the reading-size line and the owner's sheets beside the font's
  glyphs; look at every sheet.
