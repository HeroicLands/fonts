# Khelathi Zethu Glyphs — design notes

The temple hieroglyphs of the Khelathi of thalorna: the signs cut and painted on
walls, stelae and tomb doors. One font carries every drawn sign, each in up to
three forms, on a block of its own.

## The drawing

Every sign is a **hairline silhouette**: a closed outline of the thing, drawn
as a contour of one weight, with interior lines at the same weight and a few
small regions filled solid (a pupil, a knot, the sun's disk). Parts are drawn
back to front, and each part knocks out the ink of the parts behind it inside
its own outline, so an overlapping arm, a rope across a post or a hand over a
jar reads as one drawing with nothing showing through.

The hairline is about one and a half percent of a quadrat, 12 units of 770. Signs
keep their own box scale: a sign half a quadrat wide is drawn half as wide, and
the same hairline serves both.

### The figure canon

A standing figure is twenty units from sole to crown on a quadrat of a hundred:
knee 6, fork 9.5, waist and elbow 12.5, armpit 14.5, shoulder 16.5, chin 17,
crown 20. The head is three units from crown to chin. A man's frontal shoulders
are six units across and a woman's five. A figure kneeling back on its heels
stands fourteen units. Every figure is scaled so that its own height fills most of
its quadrat. The pose vocabulary is a profile head facing right with a frontal
eye, frontal shoulders, a profile torso below the armpit, and profile legs and
feet. Every sign faces right.

## The groups

| Group | Contents                    |
| ----- | --------------------------- |
| 1     | Men                         |
| 2     | Women                       |
| 3     | Gods and their attributes   |
| 4     | The body                    |
| 5     | Beasts                      |
| 6     | Birds                       |
| 7     | River creatures             |
| 8     | Plants and grain            |
| 9     | Sky, sun and stars          |
| 10    | Land, water and the river   |
| 11    | Buildings                   |
| 12    | Boats                       |
| 13    | Tools, weapons and measures |
| 14    | Vessels and offerings       |
| 15    | Cloth, crowns and adornment |
| 16    | Strokes and figures         |

A sign's id is its group and its number in the group, `01-002`. The id is the
sign's name everywhere: in `tools/khelathi-zethu-glyphs/encoding.json`, in the glyph names, and in
the specimen pages.

## Variants

A sign has a default form, `.a`, and up to two others. `.b` and `.c` are drawn
for the same sign in a different hand: a quick cut with fewer interior lines, a
different pose of the same figure, or a simpler outline. Only `.a` has a code
point. The others are reached by substitution:

| Feature | Effect                                                                                    |
| ------- | ----------------------------------------------------------------------------------------- |
| `ss01`  | every sign that has a `.b` takes it                                                       |
| `ss02`  | every sign that has a `.c` takes it                                                       |
| `salt`  | the first alternate is the `.b`, the second the `.c`; `salt` with a value of 2 takes `.c` |

In CSS, `font-feature-settings: "ss01"` or `"salt" 2`. The substitutions are
single and context-free: no rule looks at a neighbour, because renderers do not
agree on the order of contextual rules for these code points. A sign without
the requested form keeps `.a`.

## The encoding

The block runs from U+1EA40 to U+1EC6F. The code points there are unassigned and
default to right to left, so text in them runs right to left in browsers, Foundry
and Typst with no control characters. Each sign of the inventory has one code
point, in inventory order from U+1EA40, so a sign that is not yet drawn keeps its
place and a later sign drops in without renumbering. `tools/khelathi-zethu-glyphs/encoding.json`
is the table: each entry gives the id, the code point, the subject, the consonant
value, the god, the forms drawn, whether the sign is drawn and the box of each
form.

The font also maps the space and the default-ignorable controls (U+200B to
U+200F, U+202A to U+202E, U+2066 to U+2069 and U+FEFF). The controls draw
nothing: HarfBuzz would otherwise replace each with the space glyph, so a
`ccmp` substitution takes the one empty glyph to a second empty glyph, which is
left alone.

Every Latin character maps to the box, so stray text prints boxes.

## Right to left, and columns

An inscription is written in a line read right to left, or in a column read top
down; the signs face the way the line is read, toward its beginning. Shaped as
text the font gives a right-to-left line. A column is laid out by the page, one
quadrat to a row.

## Quadrats and the royal oval

A **quadrat** is a square of one sign, or of two or more signs stacked or set
side by side to fill it. The font draws signs, not quadrats, and the royal oval
is not a sign in a line. The build lays both out:

- two flat signs stack;
- a low flat sign stacks under a sign no taller than about two thirds of a quadrat;
- two narrow, tall signs stand side by side;
- anything else fills a quadrat alone.

The **cord oval** is the knotted cord round a king's name, a stadium fitted to
the signs inside so that the cord stays three hairlines clear of them, tied at the
left in a line and at the foot in a column. Signs 16-011 and 16-012 are the oval
itself as a sign, in its two orientations. `tools/khelathi-zethu-glyphs/specimens.py` carries a
copy of the rules and sets the sample inscriptions from the font.

## Metrics

One quadrat is 770 units. A sign sits with the bottom of its box on the baseline and
the box centred in its advance. The advance is the box width with
31 units of side-bearing a side, and at most 770, so a full sign is 770 wide.
The ascender holds the tallest ink above a full quadrat and the descender
holds the ink that dips below the baseline; both are Monaspace Neon's.

## Numerals and the empty pan

Numbers use strokes: group 16 draws one to nine as upright strokes, grouped as
the scribes grouped them (a row up to four, then two rows, nine as three rows of
three), with the same stroke length in every count. Ten, the weight-piece, the
hundred's grain measure and the regnal year have signs of their own, and a number
is its signs set side by side, hundreds first. The **empty pan**, a balance pan
hung on its cords with nothing in it, writes a level account: nothing remains.

## The gods' signs

Group 3 draws a god by an attribute: a flame over water, a jackal's head in a
crescent, a seed-sheaf on a staff, an arrowhead in a ring. The `god` field of
`encoding.json` names the god each sign belongs to. Signs of other groups carry
the same field where the god owns the thing drawn, as the crocodile belongs to
Chelsur.

Each god has one sign of their own. Where the god's attribute is a creature or a
thing drawn in another group, that sign is theirs: Chelsur's is the crocodile
seen from above (07-001), Uqa'a's the rayed disk on the horizon (09-002) and
Shebazet's the coiled cobra (07-009).

## Writing a name

A name is spelled in the sound signs, the signs with a single consonant value, by
the same rule as Qalezu:

- only the consonants are written;
- each apostrophe is the catch (16-001), and so is a vowel that begins a word;
  every other vowel is left unwritten;
- `th`, `sh`, `kh` and `gh` are one sign each, and `ch` and `tj` are one and the
  same sign;
- a doubled consonant writes its sign once: Zethu leaves doubling to the reader.

A god's name ends with the god's sign, which closes it as a determinative closes a
word. In everyday temple writing the god's sign stands alone for the name, and
the spelled form is kept for the formal record: a dedication, a decree, a royal
name.

Shebazet, formally, is four sound signs and her cobra, read from the right:

| Reading order | Sign                               | Writes   |
| ------------- | ---------------------------------- | -------- |
| 1             | 08-001, the drooping papyrus umbel | `sh`     |
| 2             | 12-004, the raft with a load       | `b`      |
| 3             | 12-006, the furled sail            | `z`      |
| 4             | 13-005, the grain scoop            | `t`      |
| 5             | 07-009, the coiled cobra           | her sign |

The two vowels of _Shebazet_ are not written. In everyday writing she is the
cobra, 07-009, alone.

These are rules of writing, not of the font: the font sets whatever signs are
typed, and the writer chooses the signs.

## Building and checking

The drawing source lives outside the tree, in the author's local `nogit/zethu`:
a library of splines and kits and one module per group. A generator there writes
`sources/KhelathiZethuGlyphs.ufo`, `tools/khelathi-zethu-glyphs/encoding.json` and
`tools/khelathi-zethu-glyphs/samples.json`. The UFO is the source in the repository: edit
outlines in it, and `features.fea` for the substitutions.

```sh
PATH=.venv/bin:$PATH ./build.sh
.venv/bin/python tools/khelathi-zethu-glyphs/check_font.py   # cmap, glyph set, metrics, features, names
.venv/bin/python tools/khelathi-zethu-glyphs/guard.py        # shapes every sample inscription and every variant
.venv/bin/python tools/khelathi-zethu-glyphs/specimens.py    # specimens/khelathi-zethu-glyphs/
.venv/bin/python tools/prove_guards.py       # the guard fails a font with a sign or the GSUB removed
```

`samples.json` holds the inscriptions of the setting's scenes and the date and
number samples beside them; the guard shapes every one right to left.
