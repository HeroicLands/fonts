# Teng Chou — design notes

Teng Chou, the Celestial Record, is the logographic writing of Tantsou and
Jenchai in thalorna: one character to one morpheme, read alike by people who
cannot speak to one another. Its characters are built in three layers, as
Chinese characters are: strokes make components, components combine in
layouts, and layouts nest inside a fixed square. Each layer is generated from
data and approved on its own sheet before the next is drawn.

This note covers layer 1, the strokes, layer 2, the components, and layer 3,
the layouts, with the full character set, the Jurthati syllabary and the font.

## The target

**Regular script, in a square frame, at traditional density.** The model is
regular script: square, balanced characters built from a small vocabulary of
brushed strokes, with the full, unabbreviated components of traditional
writing. A common character carries twelve to twenty strokes, and every
character fills the same square whatever its count. The formal hand of canon,
"precise angular strokes, the full character, nothing elided", is this one;
the running hand, Dou Chou, is a later variant drawn over the same skeletons.

**Brushed, not geometric.** Every stroke keeps the brush logic of regular
script: a pressed, angled entry; horizontals thinner than verticals; a waist
in a long stroke; a pause at a blunt end; a shoulder where a turn lifts and
presses again; horizontals rising a few degrees to the right; long strokes
bowed slightly. A uniform line with square corners is the commonest failure of
an invented Chinese-like script, and nothing in the generator draws one.

**Not Chinese.** A reader of Chinese sees East Asian logographic writing and
reads none of it. The script departs from Chinese at the stroke level in four
ways, each drawn from what the Tantsou and Jenchai cultures care about:

- **The hook is a barb.** A Chinese hook is a short flick that doubles back
  sharply: up and to the left at about 45 degrees from a vertical, straight up
  from a level run. A Teng Chou hook, the _spur_, seats a heel and leaves at a
  shallower turn and a greater length, so it lies low along the stroke it
  leaves: 20 degrees above level from a vertical, 55 degrees from a level run,
  62 degrees from a slanting fall. Every hooked stroke carries it, so the
  difference repeats across a page. The Jenchai hold the blade beside the
  formal hand among the made things they value, and the spur is cut like one.
- **Two strokes carry beads and rods instead of separate dots and bars.** The
  _tally_ is two beads on one stroke joined by a hairline: the entry and its
  check, which a ledger keeps in pairs. The _rods_ are two short level rods
  from one press, the brush pressed until its hairs part: the counting-rod
  bundle. Both come from the ledger, and in Tantsou thinking the ledger is how
  the sorted world is kept; heaven audits, and writing is how the audit is
  filed.
- **One stroke winds back on itself.** The _coil_ is a turn whose leg curls
  inward under itself into an open spiral. Chinese regular script has no
  stroke that closes a curve, so the coil marks the wind enclosure, and with
  it the air that circles the sorted world, as nothing Chinese.
- **Two strokes are marked at both ends or at the foot.** The _scale_ is a
  crescent pointed at both ends, which starts and ends in the air, as no
  Chinese stroke does: the scale of the Celestial Dragon, Tanzho, the First
  Classifier. The _barb dot_ is a dot whose foot flicks back to the left, so it
  points at what it marks; it is the stroke of the mark component, which makes
  the indicatives.

Every other stroke type has a Chinese counterpart and keeps its behaviour,
except that its hook, where it has one, is the spur.

## How a stroke is drawn

`tools/teng-chou/strokes.py` is the generator. A stroke is one or more
_tracks_: a path the brush tip follows, sampled every five units, with a
_pressure_ at every sample. At each sample the brush leaves an elliptical
footprint whose size is the pressure and whose long axis is held at a fixed
slant (30 degrees below level, its short axis 0.4 of its long). The outline is
the union of the convex hulls of neighbouring footprints, unioned again with
`skia-pathops` into clean contours.

The held slant is what makes a horizontal thinner than a vertical, and it
gives a horizontal's ends their slanted cut. The pressure gives everything
else: the entry press is a footprint heavier than the body, a waist is a dip
in pressure, a pause is a press down and to the right at the end, a shoulder
is a lift over the corner and a press down, a taper is pressure easing to a
point.

The style is separate from the skeletons. `Style` holds the footprint's
weight, aspect and slant; a bolder face or a seal-like variant is a different
`Style` over the same stroke calls.

**The brush face is the primary face.** Teng Chou is written in ink on paper by
clerks with a loaded brush, so the regular `Style` is broad: the footprint's long
axis is 92 units at full pressure, with the swell, the taper and the entry press
of a brush. Every character is judged first at display size, 64 to 128 pixels
and in columns, and must be writable in stroke order with a brush, with no
detail a brush could not lay down and no strokes so close that they would bleed
together. A fine pen for tiny writing is a second `Style` over the same strokes.

The terminals are shared functions, so a terminal is drawn the same way
wherever it appears:

| Terminal     | Drawn as                                                                  |
| ------------ | ------------------------------------------------------------------------- |
| angled press | the tip lands up and to the left and is pushed down-right into the stroke |
| soft landing | the tip lands lightly, with no press                                      |
| pause        | a press down and to the right at the end, then a lift back inward         |
| dew          | a vertical's blunt end: a slight swell, the tip drawn back up             |
| taper        | pressure easing steadily to a point                                       |
| spur         | a heel seated at the end, then a long low barb lifting to a point         |
| shoulder     | at a turn, a lift over the corner and a press down into the descent       |

### Using the generator

```python
import strokes as S

path = S.stroke("turn-spur", 200, 800, l1=500, l2=560)   # a pathops.Path
glyph = S.union([path, S.stroke("rods", 260, 640, l=300)])
S.contours(glyph)   # polygons, font units, y up
S.svg_path(glyph)   # SVG path data
```

Coordinates are font units on a 1000-unit em, y up. A stroke is placed by its
start point; its other parameters are its own. `STROKES[id].params` gives each
parameter's minimum, default and maximum, and `stroke` refuses a value outside
them, naming the stroke, the parameter and the range.

`tools/teng-chou/specimens.py` renders `specimens/teng-chou/strokes.png`:
every stroke large, each stroke across its parameter ranges, and a test set of
made-up characters at display size and set as text at 64, 32, 20 and 14
pixels. `tools/teng-chou/tests.py` holds the test set. Each test character
carries at least one of the novel strokes, so none can be a real Chinese
character; they test the strokes and are not characters of the script.

```sh
.venv/bin/python tools/teng-chou/specimens.py
```

## The stroke inventory

Twenty-three strokes: eighteen with a Chinese counterpart and five that Chinese
lacks. Lengths are font units; angles are degrees, 0 to the right and positive
upward.

| Id              | Name          | Skeleton                                                              | Width along the path                                                  | Entry               | Exit                            | Permitted                                                         | Not to be confused with                                                                                |
| --------------- | ------------- | --------------------------------------------------------------------- | --------------------------------------------------------------------- | ------------------- | ------------------------------- | ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| `dot`           | Dot           | a short arc falling to the right                                      | fine at the head, full at the foot                                    | soft landing        | rounded, tip drawn back         | length 50–120, angle −75 to −35                                   | `dot-left` falls the other way; `barb-dot` flicks back at the foot; `tally` is two beads on a hairline |
| `dot-left`      | Left dot      | a short arc falling to the left                                       | fine at the head, full at the foot                                    | soft landing        | rounded, tip drawn back         | length 50–120, angle −145 to −105                                 | `dot` falls right; `sweep-short` is longer and ends in a point                                         |
| `horizontal`    | Horizontal    | a line rising to the right, arched very slightly                      | pressed head, thin waist before the middle, filling to the pause      | angled press        | pause                           | length 120–820, rise 2–7, arch 0–0.03                             | `rise` climbs steeply to a point; `rods` is two short rods from one press                              |
| `vertical`      | Vertical      | a line falling straight, bowed slightly left                          | pressed head, slight waist, swelling at the foot                      | angled press        | dew                             | length 140–860, lean −30 to 30, bow 0–0.025                       | `needle` ends in a point; `vertical-spur` ends in a heel and a barb                                    |
| `needle`        | Needle        | a line falling straight                                               | full to past the middle, then lifting to a point                      | angled press        | taper                           | length 300–860, lean −20 to 20                                    | `vertical` ends blunt; `sweep` curves away left                                                        |
| `sweep`         | Sweep         | falls almost straight, then curves away down-left                     | full from the press, lifting steadily to a point                      | angled press        | taper                           | length 220–820, angle −150 to −100, curl 0–0.8                    | `sweep-short` is short and nearly flat; `needle` stays straight                                        |
| `sweep-short`   | Short sweep   | a short, nearly flat stroke to the left                               | pressed head, lifting fast to a point                                 | angled press        | taper                           | length 80–240, angle −170 to −140                                 | `dot-left` ends in a bead; `sweep` falls before it curves                                              |
| `fall`          | Fall          | a gently waved line falling right, flattening at the foot             | fine at the head, swelling to the heaviest point of any stroke        | soft landing        | foot: flat, tapering to a point | length 240–720, angle −58 to −32, foot 0.2–0.4                    | `fall-flat` runs nearly level; `dot` is short and ends in a bead                                       |
| `fall-flat`     | Flat fall     | a long, nearly level wave, dipping to the foot                        | light at the head, swelling to the foot, then a long taper            | light press         | foot                            | length 300–920, angle −14 to −4, foot 0.2–0.4                     | `fall` drops steeply; `horizontal` ends in a pause                                                     |
| `rise`          | Rise          | a short straight climb to the right                                   | heavy press, lifting at once to a point                               | heavy press         | taper                           | length 80–320, angle 18–48                                        | `horizontal` is nearly level and blunt; `sweep-turn` climbs only after a fall                          |
| `vertical-spur` | Vertical spur | a vertical, then a low barb to the left                               | as a vertical; a heel, the barb lifting to a point                    | angled press        | spur at 160                     | length 200–860, spur 60–140, lean −20 to 20                       | `vertical` ends blunt; the Chinese vertical hook flicks up at about 45 degrees and is short            |
| `turn`          | Turn          | a horizontal, a shoulder, a vertical leaning slightly inward          | thin across, full down, the shoulder pressed                          | angled press        | dew                             | across 120–800, down 120–820, rise 2–6, slope −98 to −88          | `corner` turns at the bottom left; `turn-spur` adds the barb; `coil` curls                             |
| `turn-spur`     | Turn spur     | a turn, then a low barb to the left                                   | as a turn; heel and barb at the foot                                  | angled press        | spur at 160                     | across 120–800, down 160–860, spur 60–140                         | `turn` ends blunt; `coil` curls instead of barbing                                                     |
| `corner`        | Corner        | a vertical, a pressed corner, a horizontal to the right               | full down, thinner across                                             | angled press        | pause                           | down 100–760, across 120–800, rise 1.5–5                          | `bend-spur` rounds its corner and barbs; `turn` has its corner at the top right                        |
| `bend-spur`     | Bend spur     | a vertical, a rounded bend, a level run, a barb up and forward        | full down, thinning in the bend, swelling to the heel                 | angled press        | spur at 55                      | down 160–700, across 200–760, radius 40–160, spur 60–130          | `corner` turns square and pauses; the Chinese vertical-bend hook ends straight up                      |
| `turn-sweep`    | Turn sweep    | a short horizontal, a shoulder, a sweep down-left                     | thin across, pressed at the shoulder, lifting to a point              | angled press        | taper                           | across 100–600, down 180–600, angle −140 to −105                  | `turn` descends straight and ends blunt; `sweep` has no horizontal                                     |
| `slant-spur`    | Slant spur    | a long curve falling right, bowed outward, a barb up and forward      | full and even, a waist past the middle, a heel                        | angled press        | spur at 62                      | length 360–860, angle −70 to −52, bow 0.04–0.16, spur 60–130      | `fall` ends in a flat foot; the Chinese slant hook flicks straight up                                  |
| `sweep-turn`    | Sweep turn    | a short sweep down-left, a sharp turn, a climb to the right           | full, easing into the turn, pressed, lifting to a point               | angled press        | taper                           | sweep 100–320, climb 140–400, angle −140 to −110, rise 8–30       | `rise` has no fall before it; `corner` turns square and runs level                                     |
| `tally`         | Tally         | two beads, the second lower, joined by a sagging hairline             | a bead, a hairline, a heavier bead                                    | soft landing        | rounded, tip drawn back         | length 110–220, sag 0.10–0.34                                     | two separate dots have no hairline; `dot` is one bead                                                  |
| `rods`          | Rods          | one press, and from it two short level rods, the upper shorter        | a heavy shared head, thin rods, each ending in a small pause          | heavy press, shared | two small pauses                | length 140–400, gap 44–80, rise 2–6                               | two horizontals start apart, each with its own press; `horizontal` is one rod                          |
| `barb-dot`      | Barb dot      | a dot falling right, its foot flicking back to the left               | fine at the head, full at the foot, the barb lifting to a point       | soft landing        | barb at 168                     | length 60–130, angle −70 to −40, barb 45–100                      | `dot` ends rounded; `rise` climbs right, not left                                                      |
| `coil`          | Coil          | a turn whose leg curls inward, under and back up, into an open spiral | as a turn; the curl lifting as it winds in, a small press at its tail | angled press        | the curl's tail                 | across 200–760, down 260–800, radius 50–110, curl 210–280 degrees | `turn-spur` barbs outward; `bend-spur` rounds a corner and runs on                                     |
| `scale`         | Scale         | a shallow crescent, bowed downward                                    | pointed at both ends, full in the middle                              | in the air, a point | in the air, a point             | length 80–220, angle −40 to 10, sag 0.18–0.42                     | `sweep-short` is pointed at one end only; `fall-flat` is long and swells at its foot                   |

### The novel strokes, and the components that need them

The Tantsou core proposal in thalorna names three meaning components that
need a stroke Chinese lacks, and a fourth that wants one. Each is covered:

| Component | Stroke     | Why                                                                                 |
| --------- | ---------- | ----------------------------------------------------------------------------------- |
| `count`   | `rods`     | the counting-rod bundle; a short doubled horizontal from one press                  |
| `wind`    | `coil`     | the enclosure's right side curls inward, so the frame is not the Chinese wind frame |
| `mark`    | `barb-dot` | a hooked dot, so the indicatives (_shui_, small) are not a Chinese dot              |
| `dragon`  | `scale`    | the scale-hook the commonest beast component wants                                  |

The `tally` is the fifth: the ledger bead, one in each of `step`, `thread` and
`bone`, where the component keeps a count.

## Deviations from Chinese, in brief

- Hooks are spurs: a heel and a long low barb, at a shallower turn than any
  Chinese hook.
- Five strokes Chinese lacks: `tally`, `rods`, `barb-dot`, `coil`, `scale`.
- No compound stroke beyond one turn: Teng Chou has no stroke with two turns
  (the Chinese horizontal-turn-turn-sweep of the movement radical, or the
  horizontal-turn-bend-hook). A component that needs that shape draws it from
  two strokes, which changes the stroke count and the joins.
- The flat fall closes the lower-left enclosure, as in Chinese, but the
  enclosure itself is a layer 2 component (`motion`) and is drawn from Teng
  Chou strokes, not from the Chinese movement radical.

## Layer 2: the components

A component is a group of strokes that recurs: a meaning component (water,
hand, roof), a sound component (a whole character used for its reading) or a
structural one (the single line, the mark). Teng Chou has 87 components:

| Role       | Count | What it is                                                                           |
| ---------- | ----: | ------------------------------------------------------------------------------------ |
| meaning    |    63 | a component that carries a sense; 24 of them are also characters on their own        |
| structural |     2 | `one`, the single line of the numbers, and `mark`, the hooked dot of the indicatives |
| sound      |    22 | a meaning compound (two or three components) used whole for its reading              |

The 25 pictographs and the 22 meaning compounds are the 47 sound components:
each gives its own reading to the meaning-and-sound characters that take it.

### The inventory

The meaning and structural components. _Root_ is the morpheme the component writes alone; a component with a root is also a sound component. _Forms_ lists the forms drawn: a bound component has no standalone form. _Strokes_ and _complexity_ are those of the standalone or citation form.

| Id          | Meaning                          | Role       | Root    | Forms                         | Strokes | Complexity | Novel strokes | Nearest Chinese |
| ----------- | -------------------------------- | ---------- | ------- | ----------------------------- | ------: | ---------: | ------------- | --------------- |
| `water`     | water, liquid                    | meaning    | _shou_  | standalone, left, bottom      |       5 |        4.8 | —             | 水, 氵          |
| `fire`      | fire, heat                       | meaning    | _ho_    | standalone, left, bottom      |       4 |        4.0 | —             | 火, 灬          |
| `wood`      | wood, tree                       | meaning    | _mou_   | standalone, left, top, bottom |       6 |        5.4 | —             | 木              |
| `earth`     | earth, soil, ground              | meaning    | _tou_   | standalone, left, bottom      |       4 |        4.0 | —             | 土              |
| `metal`     | metal, gold                      | meaning    | _jing_  | standalone, left, bottom      |       6 |        6.0 | —             | 金              |
| `mountain`  | mountain, height                 | meaning    | _chai_  | standalone, left, top         |       4 |        3.8 | —             | 山              |
| `sky`       | heaven, the vault of the sky     | meaning    | _teng_  | standalone, top               |       4 |        4.4 | —             | 天              |
| `sun`       | sun, day, light of day           | meaning    | —       | standalone, left, top, bottom |       5 |        5.2 | —             | 日              |
| `moon`      | moon, month, night               | meaning    | _you_   | standalone, left, right       |       4 |        3.0 | `scale`       | 月              |
| `cloud`     | cloud, vapour                    | meaning    | _yan_   | standalone, top               |       4 |        4.0 | —             | 云              |
| `rain`      | rain, weather                    | meaning    | —       | top                           |       6 |        5.8 | —             | 雨              |
| `wind`      | wind, air in motion              | meaning    | —       | frame, open below             |       2 |        2.6 | `coil`        | 風's frame 𠘨   |
| `ice`       | ice, cold                        | meaning    | —       | left, bottom                  |       3 |        2.4 | —             | 冫              |
| `stone`     | stone, rock                      | meaning    | —       | standalone, left, bottom      |       4 |        4.0 | —             | 石              |
| `plant`     | plant, grass, herb               | meaning    | —       | top                           |       4 |        3.4 | —             | 艹              |
| `grain`     | grain, harvest                   | meaning    | —       | left, top                     |       5 |        4.6 | —             | 禾              |
| `field`     | field, cultivated land           | meaning    | _nou_   | standalone, left, top, bottom |       4 |        4.4 | —             | 田              |
| `jade`      | jade, precious stone             | meaning    | —       | left                          |       5 |        4.4 | `scale`       | 王, 玉          |
| `person`    | person, human act                | meaning    | _nong_  | standalone, left, top         |       3 |        3.1 | —             | 人, 亻          |
| `woman`     | woman, female                    | meaning    | _mi_    | standalone, left, bottom      |       4 |        4.1 | —             | 女              |
| `child`     | child, offspring                 | meaning    | _zhei_  | standalone, left, bottom      |       4 |        4.1 | —             | 子              |
| `hand`      | hand, handling                   | meaning    | _huo_   | standalone, left, bottom      |       4 |        4.0 | —             | 手, 扌          |
| `foot`      | foot, standing, stepping         | meaning    | _dai_   | standalone, left, bottom      |       4 |        4.4 | —             | 足, 止          |
| `heart`     | heart, feeling, thought          | meaning    | _tsen_  | standalone, left, bottom      |       4 |        3.8 | `scale`       | 心, 忄          |
| `eye`       | eye, seeing                      | meaning    | _ching_ | standalone, left, top         |       5 |        5.2 | —             | 目, 罒          |
| `mouth`     | mouth, speaking, eating          | meaning    | _tsong_ | standalone, left, bottom      |       3 |        3.4 | —             | 口              |
| `ear`       | ear, hearing                     | meaning    | —       | standalone, left, right       |       3 |        3.0 | `scale`       | 耳              |
| `nose`      | nose, smelling, breath           | meaning    | —       | standalone, left, top         |       4 |        4.3 | —             | 自, 鼻          |
| `tooth`     | tooth, biting                    | meaning    | —       | left, bottom                  |       5 |        4.6 | —             | 牙, 齒          |
| `head`      | head, face                       | meaning    | —       | right                         |       5 |        5.7 | —             | 頁              |
| `hair`      | hair, pattern of lines           | meaning    | —       | right, top                    |       4 |        4.0 | —             | 彡              |
| `flesh`     | flesh, part of the body          | meaning    | —       | left                          |       5 |        4.8 | —             | ⺼ (月)         |
| `bone`      | bone, frame                      | meaning    | —       | left                          |       4 |        4.2 | `tally`       | 骨              |
| `skin`      | skin, hide, surface              | meaning    | —       | right                         |       4 |        4.0 | —             | 皮              |
| `spirit`    | spirit, breath of life           | meaning    | —       | top                           |       3 |        3.6 | —             | none close      |
| `sacred`    | altar, the sacred                | meaning    | —       | left                          |       5 |        4.2 | `scale`       | 礻, 示          |
| `death`     | death, ruin                      | meaning    | —       | left                          |       5 |        4.4 | `scale`       | 歹              |
| `beast`     | beast, four-footed animal        | meaning    | —       | left                          |       5 |        4.8 | —             | 犭, 豸          |
| `bird`      | bird, winged thing               | meaning    | _zhai_  | standalone, right, bottom     |       5 |        5.0 | —             | 鳥, 隹          |
| `dragon`    | dragon, scaled power             | meaning    | _zho_   | standalone, left, right       |       6 |        4.8 | `scale`       | 龍              |
| `horse`     | horse, riding                    | meaning    | _mai_   | standalone, left              |       5 |        5.4 | —             | 馬              |
| `crawler`   | crawling thing: serpent, insect  | meaning    | —       | left                          |       4 |        2.8 | `scale`       | 虫              |
| `roof`      | roof, house                      | meaning    | _zhuen_ | standalone, top               |       6 |        5.9 | —             | 宀, 冖          |
| `shelter`   | lean-to, office, sheltered place | meaning    | —       | frame, upper left             |       3 |        2.8 | —             | 广, 厂          |
| `sickness`  | sickness, healing                | meaning    | —       | frame, upper left             |       4 |        4.0 | —             | 疒              |
| `enclosure` | enclosure, bounds                | meaning    | —       | frame, all round              |       3 |        3.4 | —             | 囗              |
| `door`      | door, gate, opening              | meaning    | _sen_   | standalone, frame, open below |       4 |        4.0 | —             | 門, 冂          |
| `motion`    | motion along a road              | meaning    | —       | frame, lower left             |       4 |        3.8 | —             | 辶, 廴          |
| `step`      | step, going, conduct             | meaning    | —       | left                          |       4 |        4.0 | `tally`       | 彳              |
| `speech`    | speech, words                    | meaning    | —       | left                          |       5 |        5.4 | —             | 言, 讠          |
| `blade`     | blade, cutting                   | meaning    | _ja_    | standalone, right             |       3 |        2.8 | —             | 刀, 刂          |
| `thread`    | thread, silk, binding            | meaning    | —       | left                          |       4 |        4.2 | `tally`       | 糸              |
| `vessel`    | vessel, dish, container          | meaning    | —       | bottom                        |       5 |        4.6 | `scale`       | 皿              |
| `food`      | food, eating                     | meaning    | —       | left                          |       4 |        4.0 | —             | 飠, 食          |
| `wealth`    | cowrie, wealth, value            | meaning    | —       | standalone, left, bottom      |       6 |        4.8 | `scale`       | 貝              |
| `brush`     | brush, writing, office           | meaning    | —       | top                           |       4 |        3.8 | —             | 聿, ⺮          |
| `strike`    | striking hand, action done       | meaning    | —       | right                         |       4 |        4.2 | —             | 攵, 殳          |
| `strength`  | strength, effort                 | meaning    | —       | right, bottom                 |       3 |        3.4 | —             | 力              |
| `cover`     | cover, hiding                    | meaning    | —       | top                           |       2 |        1.8 | —             | 冖              |
| `one`       | one, a single line               | structural | _tsi_   | standalone, top, bottom       |       2 |        1.7 | `barb-dot`    | 一              |
| `count`     | counting-rod, number             | meaning    | —       | left                          |       3 |        4.0 | `rods`        | none close      |
| `old`       | age, the elders                  | meaning    | —       | top                           |       3 |        3.4 | —             | 耂              |
| `small`     | small, a little                  | meaning    | —       | top                           |       3 |        2.8 | —             | 小, ⺌          |
| `light`     | rays, light                      | meaning    | —       | top                           |       4 |        4.0 | —             | ⺌, 光          |
| `mark`      | a dot or stroke marking a place  | structural | —       | top, bottom                   |       1 |        0.7 | `barb-dot`    | 丶              |

The sound components that are meaning compounds, with the layout the proposal gives each:

| Id      | Gloss        | Layout                       | Strokes | Complexity |
| ------- | ------------ | ---------------------------- | ------: | ---------: |
| _zhen_  | snow         | `⿱{rain}{ice}`              |       9 |        8.2 |
| _rao_   | thunder      | `⿱{rain}{field}`            |      10 |       10.2 |
| _tan_   | celestial    | `⿱{sky}{sun}`               |       9 |        9.6 |
| _rin_   | red          | `⿱{sun}{fire}`              |       9 |        9.0 |
| _ha_    | dark         | `⿱{cover}{sun}`             |       7 |        7.0 |
| _leng_  | bright       | `⿰{sun}{moon}`              |       9 |        8.2 |
| _wai_   | ten          | `⿻{one}{one}`               |       4 |        3.4 |
| _rong_  | ten thousand | `⿳{person}{person}{person}` |       9 |        9.3 |
| _wen_   | centre       | `⿴{enclosure}{one}`         |       5 |        5.1 |
| _dou_   | path         | `⿺{motion}{foot}`           |       8 |        8.2 |
| _hou_   | balance      | `⿰{person}{person}`         |       6 |        6.4 |
| _sing_  | death        | `⿰{death}{person}`          |       8 |        7.5 |
| _zha_   | life         | `⿱{plant}{earth}`           |       8 |        7.4 |
| _chiao_ | to freeze    | `⿰{ice}{water}`             |       8 |        7.6 |
| _dao_   | great        | `⿱{one}{person}`            |       5 |        4.8 |
| _shui_  | new, small   | `⿱{small}{mark}`            |       4 |        3.5 |
| _hin_   | love         | `⿰{heart}{hand}`            |       8 |        7.6 |
| _mei_   | dream        | `⿱{moon}{eye}`              |       9 |        8.2 |
| _nie_   | year         | `⿱{grain}{person}`          |       8 |        7.7 |
| _len_   | two          | `⿱{one}{one}`               |       4 |        3.4 |
| _tao_   | three        | `⿳{one}{one}{one}`          |       6 |        5.1 |
| _mong_  | none, not    | `⿱{cover}{person}`          |       5 |        4.9 |

### How a component is defined

`tools/teng-chou/inventory.py` holds the inventory and
`tools/teng-chou/components.py` assembles it. Each component has an id, its
meaning, its role, the root it writes alone where it has one, the nearest
Chinese look-alike, and one or more _forms_: its standalone form and one per
position. Each form is drawn in its own box, as a list of Layer 1 strokes in
stroke order, each written with its start point in that box and its own
parameters:

```python
define("water", "water, liquid", "meaning", "shou", positions="L B", lookalike="水, 氵", forms={
    "S": {"strokes": ["tally 130 800 l=210 sag=0.26", "needle 500 910 l=800", ...]},
    "L": {"box": L, "strokes": ["tally 60 880 l=200", "dot-left 300 640 l=100", "rise 50 250 l=280 a=42"]},
    "B": {"box": B, "strokes": [...]},
})
```

Every stroke parameter is checked against the Layer 1 ranges when the
inventory loads, and a value outside them stops the load naming the
component, the form, the stroke and the range.

A sound component that is a meaning compound is _composed_: its form is a list
of parts, each a component, the form it takes there and the part's box, so a
change to a component reaches every compound that uses it. The component sheet
draws a compound from these boxes; a character, and every character that takes
the compound as its sound component, lays it out from its formula with the layer
3 engine instead, so the two are one drawing in the font.

```python
compound("leng", "bright", "⿰{sun}{moon}", [("sun", "L", (60, 120, 440, 900)), ("moon", "R", (480, 60, 940, 960))])
```

### Positions and boxes

| Position          | Box (units) | Used for                                                   |
| ----------------- | ----------- | ---------------------------------------------------------- |
| standalone        | 1000 × 1000 | the component written alone, as a character                |
| left (L)          | 420 × 1000  | the meaning side of a left-right character                 |
| right (R)         | 460 × 1000  | a meaning component whose place is the right               |
| top (T)           | 1000 × 440  | the upper part of a top-bottom character                   |
| bottom (B)        | 1000 × 440  | the lower part                                             |
| frame, upper left | 1000 × 1000 | `shelter`, `sickness`; the open area is the form's `inner` |
| frame, open below | 1000 × 1000 | `wind`, `door`                                             |
| frame, lower left | 1000 × 1000 | `motion`                                                   |
| frame, all round  | 1000 × 1000 | `enclosure`                                                |

A _bound_ component has no standalone form: it is written only in its
positions, as the Chinese roof and movement radicals are, and its first form
is its citation form. Thirty components have a standalone form; the inventory
draws 128 forms in all.

**Fitting a form to a box.** `components.render(id, position, box)` maps each
stroke's brush path from the form's box to the target box, x and y apart, and
only then lays the brush footprint along it. A form squeezed into a narrower
box keeps its stroke weight: its strokes close up, they do not thin. The brush
is one per character, so every component of a character is written with the
same weight; `components.weight_for(n)` gives a slightly finer brush to a
dense character.

**Complexity.** `components.complexity(id, position)` is the room a form asks
for: its strokes, each weighted by the ground it covers (a dot 0.6, a
straight stroke 1, a turning stroke 1.4, rods 1.5, a coil 1.6). The layout
divides the square between parts by it.

### The variant rules

A positional form is redrawn, not shrunk. The redraw follows the brief's
contextual rules, in Teng Chou's own strokes:

- **On the left, the last horizontal rises.** A component that closes on a
  horizontal or a flat fall when standalone closes on a `rise` on the left
  (`earth`, `metal`, `jade`, `food`, `wealth`, `woman`), so it leans into
  its partner.
- **On the left, a right-reaching stroke shortens.** A fall or a dot that
  reaches right in the standalone form becomes a short dot or is dropped
  (`wood`).
- **The body is strokes; a dab is an accent.** Where a Chinese component sets
  dots, Teng Chou writes real strokes of modest length: a short sweep, a short
  fall, a short horizontal. Fire at the bottom is four short strokes, a sweep and
  three falls; water opens with two short horizontals; the heart is a short
  sweep, a short fall and the long bend that cradles it, with one scale inside
  as its accent. A dab stays only where it marks something: the barbed dot of
  `mark` and `one`, the ledger bead of `step`, `thread` and `bone`, the scales of
  the scaled beasts. `tools/teng-chou/stroke_mix.py` holds every character to it
  (see [The stroke mix](#the-stroke-mix)).
- **At the top and bottom, a component flattens.** Verticals shorten,
  horizontals keep their length, and a long falling stroke becomes a short one
  (`wood`, `field`, `mountain`, `person`, `heart`).
- **A sound component is narrowed, not redrawn.** A whole character used for
  its reading is fitted to the right-hand or bottom box by the squeeze above,
  as Chinese narrows its phonetics; the sheet shows each one fitted.

### The novel strokes in the components

| Stroke     | Components                                                                                                                                    |
| ---------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `rods`     | `count`: two bundles of counting rods over a spur                                                                                             |
| `coil`     | `wind`: the right side of the frame                                                                                                           |
| `barb-dot` | `mark` and `one` only, so a hooked dot always marks a place or a count                                                                        |
| `scale`    | `dragon` and `crawler`, the scaled beasts; one crescent as an accent in `moon`, `heart`, `ear`, `vessel`, `wealth`, `jade`, `death`, `sacred` |
| `tally`    | the ledger bead of `step`, `thread` and `bone`, where the component keeps a count                                                             |

### Diverging from Chinese

Every component was drawn, rendered and read against its nearest Chinese
component, and redrawn where it read as that component or as another real
character. The rules that came out of it:

- No component is a Chinese radical with one stroke changed. Each differs in
  topology (which strokes cross, which corners close) as well as in stroke.
- No component closes a box with a bar across it. `sun` is a closed box with a
  dot and a ray, `eye` a wide box under a tally, `mouth` a frame open below
  with a dot, and none reads as 日, 目 or 口 in running text.
- The movement frame is not 辶: `motion` is a tally, a post, a step dot and a
  separate flat fall that runs under the inner part. Nothing zigzags.
- Shapes that read as kana or Latin letters were redrawn: a corner crossed by
  a vertical (4), a horizontal crossed by a bend (セ), a horizontal over a
  sweep (ア), three falls in a column (ミ).

Two shapes in the proposal's own compounds stay close to Chinese: `len` and
`tao` are two and three marked lines, 二 and 三 with a hooked dot on each, and
`chiao`, `⿰{ice}{water}`, is built as 冰 is.

### Using the assembler and the sheets

```python
import components as K

K.render("water", "L", (60, 70, 380, 930))      # a pathops.Path in font units
K.render_parts([("water", "L", (70, 70, 360, 930)),
                ("moon", "R", (380, 70, 930, 930))], K.weight_for(8))
K.complexity("metal", "L")
```

```sh
.venv/bin/python tools/teng-chou/component_specimens.py
```

It writes `specimens/teng-chou/components.png`, every component in each of
its forms and every sound component fitted to the right and the bottom, and
`specimens/teng-chou/components-in-use.png`, characters of the core vocabulary
assembled by a plain left-right or top-bottom split and set as text at 64, 32,
20 and 14 pixels. `--only water,fire` draws a subset.

## Layer 3: the layouts

A character is one Tantsou morpheme, written as an IDC formula over the
components: `{fire}` is a pictograph, `⿰{sun}{moon}` a meaning compound,
`⿰{water}‹mong›` a meaning component beside a sound component. The layout engine,
`tools/teng-chou/layout.py`, reads the formula, divides the square between its
parts, fits each part to its share, applies the contextual stroke rules and lays
the brush along the result. `tools/teng-chou/characters.py` holds the 213
characters as formulas, with the Tantsou lexicon's gloss for each, in the order of
their code points.

```python
import layout as Y

path = Y.render("⿰{water}‹mong›")      # a pathops.Path on the 1000-unit square
Y.describe("⿰{water}‹mong›")           # each part, its form, its slot, any rule applied
Y.render_char("wong")                  # the same, by morpheme, with its overrides
```

### The operators

Twelve Ideographic Description Characters are read, and nest to any depth:

| Operator | Layout              | Operator | Layout                     |
| -------- | ------------------- | -------- | -------------------------- |
| ⿰       | left and right      | ⿵       | frame open below           |
| ⿱       | top and bottom      | ⿶       | frame open above           |
| ⿲       | left, middle, right | ⿷       | frame open at the right    |
| ⿳       | top, middle, bottom | ⿸       | frame from the upper left  |
| ⿴       | full enclosure      | ⿹       | frame from the upper right |
| ⿻       | overlaid            | ⿺       | frame from the lower left  |

A formula that is a meaning compound's own formula is that compound, so _leng_ is
drawn the same alone and inside _seng_ and _re_. A compound drawn stroke by stroke,
_wai_ (ten), stands as its own drawing.

The 213 characters use these layouts: ⿰ 129 (124 meaning and sound, 5 meaning
compounds), ⿱ 45, a single component 25, ⿺ 5, ⿵ 3, ⿳ 2, ⿸ 2, ⿴ 1 and ⿻ 1.
Left-right and top-bottom carry 82% of the set, and every enclosure is rare.

### Boxes

The square is the 1000-unit em less a margin of 40 units at the sides and 52 at
the top and bottom. Each operator divides its box, and its parts' inks stand
`GAP`, 46 units, apart.

- **A two-way split** (⿰, ⿱) gives the first part a share of the box: half the
  share of its role and half the share its complexity asks for. A meaning
  component beside a sound component has the role share 0.38, a sound component
  beside a meaning component 0.62, and two meaning components 0.5. The complexity
  share is the parts' complexities, each raised to the power 0.75, in proportion.
  The share is held between 0.30 and 0.62. So _wong_, water (complexity 2.9) beside
  the whole of _mong_ (5.1), gives water about a third of the width.
- **A three-way split** (⿲, ⿳) shares the box by complexity alone.
- **An enclosure** gives its frame the whole box and its contents the frame's
  inner area, as the component's drawing marks it.
- **Overlaid** parts share the whole box.

**Optical balance.** A part's ink, not its drawing box, is fitted to its slot, so
the white between two parts is the same in every character, however much margin a
component's own drawing leaves. Where a slot is a different shape from the part,
the part is narrowed or flattened by at most 1.9 against its height, and past that
keeps its proportions; a part is never enlarged past 1.3 times its drawing's own
scale, so a sparse component keeps the room it was drawn with. A part smaller than
its slot sits a little above the slot's middle, and the whole character sits 10
units above the square's centre, where the eye puts the middle. A character of few
strokes is drawn smaller in its square, as regular script draws it:

| Strokes | 1    | 2    | 3    | 4    | 5    | 6    | 7 and more |
| ------- | ---- | ---- | ---- | ---- | ---- | ---- | ---------- |
| Scale   | 0.72 | 0.78 | 0.84 | 0.88 | 0.92 | 0.96 | 1          |

**One brush.** Every part's brush path is mapped into its slot first, and the
brush is then laid along it, so a narrowed part keeps the character's weight; its
strokes close up rather than thin. The character's brush is `weight_for` its
stroke count, a little finer for a dense character.

### Forms and the contextual rules

A part takes the form its component draws for its place: the left form on the
left, the right form on the right, the top or bottom form above or below. Where a
component has no form for a row of a column, the middle of ⿳ or the foot, it takes
the flat form it has for the other row; otherwise it takes its standalone form,
narrowed. **A sound component is always its whole character**, narrowed, never a
radical form: the fire under _ken_ (hearth) is the meaning radical, four short
strokes, but the fire under _bo_ (few), which gives the reading _ho_, is the
whole fire.

A part fitted to a place it has no drawing for follows the rules regular script
uses, applied to its strokes before the brush is laid:

- **On the left, the lowest horizontal rises.** When nothing lies below it, it
  becomes a rise from the same start, half its length (at most 320 units), at 26
  degrees, leaning into the part beside it: the _one_ of _di_ (drum).
- **Crowded on the left or in the middle, a fall becomes a dot.** A fall or flat
  fall that reaches the right edge of its part shrinks to a dot at its head.
- **Below another part, a part flattens.** The fit does this itself: a slot wider
  than tall flattens its part, and its verticals shorten while its horizontals
  keep their length.

The weight never changes with the rules. A rule changes which strokes are drawn,
not how heavy they are.

### Stroke order

Strokes are written as the components carry them, each in its own stroke order,
and the parts in the order of the formula: left before right, top before bottom,
outside before inside. A frame that closes the character from below, ⿺ (the road
of motion) and ⿶, is written after its contents. The order decides which stroke
lies over which where two meet, and it numbers the strokes a syllabary sign keeps.

### Overrides

A character the default fit does not set well carries an override in
`OVERRIDES` in `characters.py`: a fixed split, or a fixed slot and a larger
enlargement for one part. Five characters carry one:

| Character      | Override                                                                         | Why                                                                      |
| -------------- | -------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| _chiao_ freeze | the left share 0.30                                                              | ice's three short strokes take a narrow column, so water has the room    |
| _ken_ hearth   | the door 0.64 of the height; the fire's bottom form in a narrower slot, enlarged | keeps the fire's four strokes close under the narrow door frame          |
| _kui_ grey     | _shui_ 0.62 of the height; the fire's bottom form narrower, enlarged             | keeps the fire close under the small sound component                     |
| _chao_ begin   | the left share 0.28                                                              | _chiao_, itself two columns, has the room to keep its strokes as strokes |
| _jin_ warmth   | _hin_ 0.64 of the height; the fire's bottom form narrower, enlarged              | as _ken_                                                                 |

Two characters are set by their data rather than by an override:

- **_chiao_, to freeze**, is `⿰{ice}{water}`, and ice's left form is compact: two
  short falls over a rise, in a narrow column beside the whole of water. Frost
  (_chuen_) takes the same left form; snow (_zhen_) takes ice's bottom form.
  `specimens/teng-chou/chiao-options.png` sets the arrangements weighed.
- **_hin_, love**, is `⿰{heart}{hand}`, the heart's left form beside the whole
  hand: love is a feeling, so the heart stands as its radical. Tiger (_hen_), lock
  (_kin_) and warmth (_jin_) take _hin_ as their sound component.
  `specimens/teng-chou/hin-options.png` sets the arrangements weighed.

### The character set

213 characters: the 87 roots Tantsou had, the 109 roots of the core vocabulary
and 17 roots that exist to write foreign names. By kind, 25 are pictographs, 22
meaning compounds and 166 a meaning component with a sound component. A
character carries 2 to 15 strokes, 9 at the median. `tools/teng-chou/guard.py`
writes every form of the Tantsou lexicon, compounds included, one character per
morpheme, and fails a form it cannot write.

`tools/teng-chou/character_specimens.py` writes `specimens/teng-chou/characters.png`,
every character large with its morpheme, gloss, formula and stroke count.

## The Jurthati syllabary

Jurthati writes its content words with the Teng Chou character for their meaning,
and its particles, verb endings and island words in a syllabary of 87 signs, one
per syllable. Each sign is a simplified character whose reading is close to the
syllable, and is drawn from that character's own strokes, so a sign is never a
shape of its own invention. `tools/teng-chou/syllabary.py` holds the signs, each
with its source and its simplification:

| Simplification | Signs | What it keeps                                                                                                                                 |
| -------------- | ----: | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `cut`          |    16 | a pictograph's first three strokes, the third ending in a point (a horizontal as a flat fall, a vertical as a needle, a turn as a turn sweep) |
| `sound`        |    30 | the sound component alone, its three or four longest strokes in stroke order                                                                  |
| `whole`        |    30 | the whole character, its three or four longest strokes in stroke order                                                                        |
| `part:<id>`    |    11 | the whole character, the named component cut to its longest stroke and the rest to its outline                                                |

A source of eight strokes or more keeps four, a lighter one three.

**Lighter and smaller.** A sign is written with 0.8 of a character's brush and
stands at most 0.8 of the square, as kana stand beside kanji, centred in the same
square so that a column of mixed characters and signs runs even.

**Distinct at body size.** `tools/teng-chou/syllabary_distinct.py` renders every
sign at 24 pixels to the em, softens it by a pixel and compares every pair by the
cosine of their images; a pair above 0.86 fails. Where the rule's strokes left
two signs alike (_ka_ and _ha_, both from _ha_; _sa_ and _ja_, both from the
blade), the later sign keeps a different set of its source's strokes, written in
`PICKS`. `--search` proposes the set: of the sets clear of every other sign by
0.06, one of three strokes if there is one, then four, then two, covering the
most ground, and never a set the stroke-mix guard would refuse. Sixteen signs carry
picks: _ka ke ko gu sa sha she sho ju to tso da do mo ya ru_.

**The source of _tsa_.** No Tantsou morpheme is read _tsa_, so the sign takes
_tsai_ (creation, `⿰{hand}‹wai›`), whose Tantsou reading opens with the syllable,
as _sha_ takes _shai_. _di_ keeps the outline of its whole character, since
its sound component _tsi_ is one line and a mark, too little to make a sign of
strokes.

`specimens/teng-chou/syllabary.png` sets every sign beside its source character.

## The font

`tools/teng-chou/build_ufo.py` writes `sources/TengChou.ufo` from the data, and
`build.sh` compiles it as it compiles every face. The UFO is generated and
committed: an edit belongs in `tools/teng-chou/`, and the script is run after it.

- **Curves.** A brush outline is a union of footprint hulls, a polygon with a
  point every few units. `tools/teng-chou/fit.py` cuts each contour at its corners
  and fits each run between them with as few cubic curves as keep every point
  within 1.2 units, about a fifth of the points the polygon had.
- **Code points.** Characters from U+F1000, the five stages of the tally after
  them, and the syllabary from U+F2000, each in the order of its data file, so a
  new character or sign is added at the end and none is renumbered. Glyphs are
  `tc.<morpheme>`, `tc.tally1` to `tc.tally5` and `js.<syllable>`; names are
  `TENG CHOU CHARACTER SHOU`, `TENG CHOU TALLY ONE` and `TENG CHOU SYLLABLE KA`.
- **Size.** The square is scaled so the characters' median ink height is the cap
  height every face shares, 730 units; the square is then 825 units.
- **Along a line.** In an inline span a glyph's advance is its ink and 30 units a
  side, as every face here is spaced.
- **Down a column.** Teng Chou is written in columns read from the right. Every
  character, sign and stage of the tally has a vertical advance of exactly one em,
  1000 units, so a column of N characters is N em tall; the 825-unit square is
  centred in that em, and every glyph shares one vertical origin, half an em above
  the square's centre, in `vhea` and `vmtx`. Each glyph's ink is centred on its
  horizontal advance, which is the column's axis. HarfBuzz sets a
  column top to bottom from these. A TrueType font carries no `VORG`, so a shaper
  reads the origin from each glyph's top side bearing. `tools/vertical.py` checks
  all of it.
- **Typing.** The characters and signs are typed by code point, or written by a
  encoding in the consuming build; Teng Chou has no keyboard layout.

`tools/teng-chou/text_specimen.py` sets the Tantsou and Jurthati passages of
`tools/teng-chou/texts.py` from the built font: `text.png` along a line at display
and body sizes, and `text-vertical.png` in columns of ten, read from the right, on a
ruled grid of one-em cells.

```sh
.venv/bin/python tools/teng-chou/build_ufo.py
PATH=.venv/bin:$PATH ./build.sh
.venv/bin/python tools/teng-chou/check_font.py
.venv/bin/python tools/teng-chou/guard.py
.venv/bin/python tools/teng-chou/syllabary_distinct.py
.venv/bin/python tools/teng-chou/character_specimens.py
.venv/bin/python tools/teng-chou/character_specimens.py --name syllabary.png
.venv/bin/python tools/teng-chou/text_specimen.py
```

## The stroke mix

The body of a character is strokes; dabs are accents on it. A dab is real, and
Chinese characters carry dabs all the time, but a character built mostly from
them reads sparse and is no pleasure to write. `tools/teng-chou/stroke_mix.py`
classes every stroke of every laid-out character by the length of its brush
path on the 1000-unit em:

| Class | Rule                                                                                    |
| ----- | --------------------------------------------------------------------------------------- |
| long  | 350 units (0.35 em) or longer                                                           |
| short | 150 to 350 units: a real stroke of modest length                                        |
| dab   | under 150 units, or a bead (`dot`, `dot-left`, `barb-dot`, `tally`) whatever its length |

A character fails with more than five dabs, or with more dabs than long and short
strokes together. A syllabary sign fails with more dabs than strokes, or with
fewer than two strokes that are not dabs. The tally of five fails on any dab.
Measured on the laid-out character, so a component's short stroke that a layout
narrows below 150 units counts as a dab there: a sound component drawn small
must still be written in strokes.

Across the 213 characters the mean is 3.4 long, 4.8 short and 0.5 dabs; across
the syllabary, 2.5 long, 0.9 short and under 0.1 dabs.

## The tally of five

Clerks, temple scribes and quartermasters keep a running count with the tally:
one stroke for each item, in a fixed order, so a finished tally means five and
the first one to four strokes are a partial count. It is five strokes of the
body, broad and long, with no dab, built from Teng Chou's own strokes:

1. the left post, a vertical spur, its barb the script's own;
2. the lintel, a long horizontal from the post's head;
3. the right post, a needle hanging from the lintel's end;
4. the entry, a short horizontal inside under the lintel, the line of the ledger;
5. the audit, a fall across the frame from its upper left, which closes the count.

Every stage is drawn on the finished tally's square, so the strokes stand where
they will stand in the five as the count grows. The five stages are their own
characters, U+F10D5 to U+F10D9, `TENG CHOU TALLY ONE` to `TENG CHOU TALLY FIVE`;
the last also writes "five; a tally of five". `tools/teng-chou/tally.py` holds
them, and `specimens/teng-chou/tally.png` sets the stages and counts kept with
them, along a line and in columns.
