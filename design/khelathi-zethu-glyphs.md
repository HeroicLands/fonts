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
single and context-free: no rule looks at a neighbour, so a sign takes its form
whatever order a renderer shapes the run in. A sign without the requested form
keeps `.a`, and a sign in a quadrat or a cartouche takes its form there too.

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

The format controls of [Quadrats and cartouches](#quadrats-and-cartouches) are mapped
twice: at the same offsets from U+1EC60, at the end of the font's block, which is the
form notes store, and at their own Unicode code points, U+13430 to U+1343D, for
compatibility with HarfBuzz tools. `tools/khelathi-zethu-glyphs/controls.json` lists
them. The signs of the inventory stop short of U+1EC60.

## Right to left, and columns

An inscription is written in a line read right to left, or in a column read top
down; the signs face the way the line is read, toward its beginning. Shaped as
text the font gives a right-to-left line, with its quadrats and cartouches laid out.
A column is laid out by the page, one quadrat to a row: the font's layout works in a
horizontal line only, and in vertical text its controls draw nothing.

## Quadrats and cartouches

A **quadrat** is a square of one sign, or of two or more signs stacked or set side by
side to fill it. A **cartouche** is the knotted cord round a king's name. The font
lays out both itself, from format controls typed between the signs, so a note stores
only signs and controls, the font's own twins of Unicode's Egyptian Hieroglyph Format
Controls:

| Control                | Unicode | Font's own | Notation | Effect                                                    |
| ---------------------- | ------- | ---------- | -------- | --------------------------------------------------------- |
| vertical joiner        | U+13430 | U+1EC60    | `:`      | stacks what is before it over what is after it            |
| horizontal joiner      | U+13431 | U+1EC61    | `*`      | sets what is before it to the right of what is after it   |
| insert at top start    | U+13432 | U+1EC62    | `[ts]`   | sets the next sign in the core's top right corner         |
| insert at bottom start | U+13433 | U+1EC63    | `[bs]`   | in its bottom right corner                                |
| insert at top end      | U+13434 | U+1EC64    | `[te]`   | in its top left corner                                    |
| insert at bottom end   | U+13435 | U+1EC65    | `[be]`   | in its bottom left corner                                 |
| begin segment          | U+13437 | U+1EC67    | `(`      | opens a group that stands as one item, like a parenthesis |
| end segment            | U+13438 | U+1EC68    | `)`      | closes it                                                 |
| begin enclosure        | U+1343C | U+1EC6C    | `<`      | opens a cartouche                                         |
| end enclosure          | U+1343D | U+1EC6D    | `>`      | closes it                                                 |

The start of a right-to-left line is its right, so a start corner is a right corner.
An insertion binds tightest, then the horizontal joiner, then the vertical joiner, as
Unicode defines them: `A * B : C` is the pair `A * B` over `C`, and `A * (B : C)` is `A`
beside the stacked pair. The notation column is the one the specimens print.

**Which code points to type.** Notes and text store the font's own controls,
U+1EC60 to U+1EC6D; they are the recommended form. A browser shapes a run of one script
at a time. The Unicode controls belong to the Egyptian script and are left to right,
while Zethu's signs belong to no script and are right to left, so in a browser each
Unicode control is shaped apart from the signs and the quadrat falls apart. The font's
own controls are right to left and belong to no script, like the signs, and reach the
same shaping run: text meant for a browser, Foundry or any HarfBuzz-based renderer
types them. The font also maps the Unicode controls, so that text pasted from standard
Egyptian text shapes in a HarfBuzz tool given a whole run directly, as the guard does,
and lays out the same way. A browser cannot shape them.

**The layout.** Each sign has a natural size in eighths of a quadrat: its ink's width
and height, with 35 units of margin, rounded up. A horizontal group is its items side by
side, as wide as their widths together and as tall as the tallest; a vertical group is
its rows one above another, as wide as the widest. A segment is one item of the size of
the group inside it. A corner insertion scales its sign into the quarter of the core's
cell at that corner and sets it in the corner; the pair is the core's size. The quadrat
is then scaled as a whole, every proportion kept, to fit a square of one quadrat, and is
never enlarged. Items are centred across their group, and the quadrat on its square,
whose centre stands at half a quadrat above the baseline. A sign is drawn at the scale
nearest below its own, from thirteen steps of a sixth of an octave, from the whole sign
down to a quarter of it. A quadrat's advance is its width plus the sidebearing a side,
so it is spaced like a sign.

The layout reaches a segment inside a segment inside the quadrat, and quadrats up to
three quadrats wide or tall before they are scaled; an insertion's core and argument
are each one sign, and a core takes one insertion. The font has no data on which
corner of a sign is empty: the writer chooses the corner, as a scribe did.

**The cartouche.** OpenType cannot stretch a glyph, so the cord is built of pieces. The
end enclosure, first in the line as it is seen, becomes the tied end: a half ellipse of
cord, the seal-knot and the two loose ends, at the left. The begin enclosure becomes the
round end at the right. Every glyph between them that advances, a sign, a quadrat's
carrier or a space, is followed by a piece of cord as long as its advance, drawn back
over it: the top and bottom bands, three hairlines clear of the tallest and lowest ink of
any sign. The pieces meet end to end, so the cord runs unbroken whatever the cartouche
holds. A line breaks only at a space, so a cartouche with no space inside stays on one
line.

Signs 16-011 and 16-012 are the oval itself as a sign, in its two orientations.

**How the font does it.** `tools/khelathi-zethu-glyphs/layout.py` adds the layout when the
font is built: it adds the controls, a copy of every form at each drawn scale, empty
tokens that carry the arithmetic, and the lookups, and compiles them with the source's
`features.fea`. The lookups sit in `rclt` and `dist`, which every HarfBuzz shaper applies
to horizontal text and no style sheet turns off. HarfBuzz shapes these code points in
visual order, because their script, if any, runs left to right, so every rule reads the
run left to right: a vertical group from its bottom row up, a segment from its end control
to its begin control. Each pass of the layout reads only its own tokens through a mark
filtering set, so a sign's tokens follow it without getting in each other's way; the
deepest segment is measured first, so a group knows its size before its parent lays it
out. Positioning then moves each sign's copy by the offsets its tokens carry. The
generator's docstring gives the passes in order, and `reference()` there computes the same
layout in Python, which the guard compares with the shaped text.

`tools/khelathi-zethu-glyphs/specimens.py` also sets the sample inscriptions in a line and
in a column by the setting's own grouping rules, which the build uses to choose quadrats:

- two flat signs stack;
- a low flat sign stacks under a sign no taller than about two thirds of a quadrat;
- two narrow, tall signs stand side by side;
- anything else fills a quadrat alone.

The cord oval there is a stadium fitted to the signs inside, tied at the left in a line
and at the foot in a column.

## Metrics

One quadrat is 770 units. A sign sits with the bottom of its box on the baseline,
and its drawing keeps its own box scale. Its width follows its drawing: the
advance is the ink width with 31 units of white a side, so the ink stands
centred in the advance, a quadrat layout centres the sign's box there, and a
narrow sign takes a narrow advance in a line. This is the font's spacing rule (see `design/making-fonts.md`). The space is
62 units, the gutter between two signs: an inscription has no word spaces, so a
phrase runs on as one line of signs.
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

## The paint map

Large Zethu is painted: on banners, stelae, god emblems and in the book. How a
sign is painted is a fact about the sign, as its meaning is, so every surface
paints it the same way. `tools/khelathi-zethu-glyphs/paint.json` records it: for
every drawn sign, the colour of each enclosed region of its default form, `.a`.
An excerpt, with fewer seeds than the real entry for the spearman 01-057:

```json
{
  "categories": [
    "skin-male",
    "skin-female",
    "linen",
    "hair",
    "red",
    "pottery",
    "gold",
    "faience",
    "water",
    "plant",
    "cord",
    "stone",
    "wood",
    "ground"
  ],
  "defaults": { "01": "skin-male", "02": "skin-female", "03": "gold" },
  "signs": {
    "01-057": {
      "regions": [
        { "seed": [105, 690], "paint": "hair" },
        { "seed": [241, 518], "paint": "red" },
        { "seed": [313, 434], "paint": "wood" },
        { "seed": [93, 440], "paint": "linen" },
        { "seed": [125, 78], "paint": "ground" }
      ]
    },
    "09-002": { "outline": "red", "regions": [{ "seed": [53, 113], "paint": "pottery" }] }
  }
}
```

A region is named by a **seed**, a point in glyph units on the built font's
outline of the sign, and takes the seed's **paint**. A region no seed names takes
the sign's `default`, or else its group's entry in `defaults`. A sign may give an
`outline` category, and its outline is then drawn in a dark tone of that colour
rather than the ink of the drawing.

### The categories

The map records categories, not colours: each surface sets its own palette, and
the contact sheets use a reference one. Each category is a pigment of the
Egyptian painter, named for its commonest use:

| Category      | Pigment      | Paints                                                                   |
| ------------- | ------------ | ------------------------------------------------------------------------ |
| `skin-male`   | red ochre    | a man's skin, a red ox, the lips of a mouth                              |
| `skin-female` | yellow ochre | a woman's skin, a hound, a horse, a buff breast or a yellow beak         |
| `linen`       | white        | kilts, robes, sails, wrapping, the moon, smoke, bone, salt               |
| `hair`        | black        | wigs, beards, side-locks, a jackal of the god, black silt                |
| `red`         | red          | painted cloth and leather: a headband, a shield's rims, a streamer, meat |
| `pottery`     | terracotta   | fired clay, and earth: banks, fields, mounds                             |
| `gold`        | gold         | gold, the sun and stars, a god's emblem, bronze                          |
| `faience`     | turquoise    | faience, a god's wig, lapis inlay, a blue lotus, plumage                 |
| `water`       | blue         | water and the sky                                                        |
| `plant`       | green        | leaves, reeds, papyrus, a crocodile, a serpent                           |
| `cord`        | straw        | rope and cord, basketry, ripe grain, bread                               |
| `stone`       | grey         | stone, and a blade of metal or flint                                     |
| `wood`        | brown        | wood, a bird's brown plumage                                             |
| `ground`      | none         | negative space, left as bare wall                                        |

`ground` paints nothing: the region shows the wall or page behind the sign. It
marks the air a drawing encloses: between a bow and its string, between an arm
and the body, between a figure's legs below the kilt hem, inside a loop of
rope, between the strings of a lyre and the meshes of a net.

The conventions the map follows: a man's skin is red ochre and a woman's yellow
ochre; kilts and linen are white; wigs are black, and a god's wig is blue; the
sun and gold are gold; water and the sky are blue; plants are green; a vessel is
pottery unless its subject makes it faience or gold; beasts and birds take their
natural colours. Every region of a figure's kilt is `linen`, including each
piece a crossing arm, tool or shield cuts it into.

### Group defaults

| Group | Default       | Group | Default   |
| ----- | ------------- | ----- | --------- |
| 1     | `skin-male`   | 9     | `gold`    |
| 2     | `skin-female` | 10    | `pottery` |
| 3     | `gold`        | 11    | `stone`   |
| 4     | `skin-male`   | 12    | `wood`    |
| 5     | `skin-female` | 13    | `wood`    |
| 6     | `skin-female` | 14    | `pottery` |
| 7     | `plant`       | 15    | `linen`   |
| 8     | `plant`       | 16    | `hair`    |

In groups 1 to 6, the people, women, gods, the body, beasts and birds, every region has a seed of its own and the default is never used: a figure encloses air between its arms, legs, cords and tools, and no default can tell that air from skin. Where two beasts overlap, the one behind takes a colour of its own, as the rear ox of the yoked pair is `wood` against the front ox's red.
An object's default is its commonest material, and a sign of another material
states its own `default`: a reed boat is `plant`, a sealed roll `linen`.

### The region rule

`tools/khelathi-zethu-glyphs/paint.py` finds the regions, and the guard, the
contact sheets and any renderer import it, so they all find the same ones:

1. The sign's `.a` is rasterized from the built font at half a pixel to the
   font unit (`K`), and a pixel more than half covered is ink.
2. A gap in the outline narrower than about one hairline is closed: the ink is
   closed with a disc of four tenths of a hairline (`SEAL`). This parts a
   figure's leg from the space between its legs where the leg's line stops
   short of the kilt.
3. The open ground is whatever a ball of radius 1.15 hairlines (`BALL`) can
   reach rolling in from outside the sign. An outline left open by a hairline
   or two, an ankle short of its foot or a leg meeting a hip, still closes.
4. Every other connected white area is a region, except a speck smaller than
   1.2 hairlines square (`SPECK`) and a sliver the ball leaves in an outer
   corner, smaller than six square hairlines (`SLIVER`). A speck or sliver is painted as the
   region nearest it, so no paper shows inside the outline: an ear, a heel or a toe takes the
   skin around it.
5. Regions are numbered in scan order, top to bottom and left to right. A gap
   the seal closed is painted as the region beside it.

A seed must fall inside a region at that scale, never on the outline. The seeds
in the map are each region's point farthest from its edge, so a renderer at
another scale finds the same region under them.

### Contact sheets and the guard

`.venv/bin/python tools/khelathi-zethu-glyphs/paint.py` writes one contact sheet
per group to `specimens/khelathi-zethu-glyphs/paint/`, every sign painted with
the reference palette, and `figures-check.png`, every man and woman on their
feet drawn larger, for checking kilts, legs and the ground between the legs, and
`kneeling-seated-beasts.png`, every kneeling or seated figure and every beast.
With `--regions DIR` it writes the authoring sheets instead: each sign with its
regions tinted and numbered, and `centres.json`, each region's seed point.

`tools/khelathi-zethu-glyphs/paint_guard.py` fails when a drawn sign has no map,
when a map names a sign that is undrawn or not in the encoding, when a category
is unknown, when a group of drawn signs has no default, when a seed falls on the
outline or outside every region, when two seeds fall in one region, and when a pixel inside
a sign's outline belongs to no region. A sign
is not drawn until it is painted. The guard also fails when a region of a sign in groups 1 to 6 has no seed. It runs in CI and in
`tools/prove_guards.py`.

## Building and checking

The drawing source lives outside the tree, in the author's local `nogit/zethu`:
a library of splines and kits and one module per group. A generator there writes
`sources/KhelathiZethuGlyphs.ufo`, `tools/khelathi-zethu-glyphs/encoding.json` and
`tools/khelathi-zethu-glyphs/samples.json`. Its output is set to the spacing rule with
`tools/respace.py`. The UFO is the source in the repository: edit
outlines in it, and `features.fea` for the substitutions. The quadrat and cartouche
layout is not in the UFO: `layout.py` adds it to the built font from the font's own
signs, so a regenerated UFO keeps it with nothing to copy across.

```sh
PATH=.venv/bin:$PATH ./build.sh                              # runs layout.py on the built font
.venv/bin/python tools/khelathi-zethu-glyphs/check_font.py   # cmap, glyph set, metrics, features, names
.venv/bin/python tools/khelathi-zethu-glyphs/guard.py        # shapes every sample inscription and every variant
.venv/bin/python tools/khelathi-zethu-glyphs/quadrats.py     # shapes quadrats and cartouches against the reference
.venv/bin/python tools/khelathi-zethu-glyphs/specimens.py    # specimens/khelathi-zethu-glyphs/, quadrats/ among them
.venv/bin/python tools/khelathi-zethu-glyphs/paint_guard.py  # every drawn sign has a paint map whose seeds land in its regions
.venv/bin/python tools/khelathi-zethu-glyphs/paint.py        # specimens/khelathi-zethu-glyphs/paint/
.venv/bin/python tools/prove_guards.py       # each guard fails a broken font
```

`samples.json` holds the inscriptions of the setting's scenes and the date and
number samples beside them; the guard shapes every one right to left.

`quadrats.json` holds the quadrat and cartouche fixtures. `quadrats.py` shapes each, every
sample of `samples.json` written with joiners, runs of several quadrats and a seeded sweep
of random quadrats, and asserts that each sign is drawn at the reference's scale and stands
within 24 units of the reference's place; `tools/prove_guards.py` proves it fails a font
without the lookup that sums a row's widths, without positioning, without the font's own
vertical joiner and without the cartouche's cord.
