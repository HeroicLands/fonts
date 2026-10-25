# chalish-ceremonial encoding

Chalish Pilam Ceremonial is the carved hand of Ch'alish P'ilam, a logographic script whose glyphs compose into blocks. This encoding writes the named code of a glyph as its code point: a concept glyph by its name in capitals (`SUN`), a syllable sign by its syllable and number (`ka1`), and a number by `n` and its value (`n13`).

Inside a block, `*` writes the joiner that sets two items side by side and `:` the joiner that stacks the first over the second; the font lays the block out from them. A block ends wherever no joiner follows, so `-` and a space each write only their invisible mark. Zero and the places of the count have code points and no ceremonial drawing, so they print the box.

## Fonts

- Chalish Pilam Ceremonial (`chalish-pilam-ceremonial`), written left to right.

## Running it

`encode.py` needs only Python 3.9 or later. From a checkout, or from `node_modules/@heroiclands/fonts`:

```sh
python3 encode.py --encoding chalish-ceremonial "n13*TQAN DAWN"
python3 encode.py --encoding chalish-ceremonial --decode "󴀍󴿰󴀧󠄀󴂄"
```

The first command writes `󴀍󴿰󴀧󠄀󴂄`, and the second reads it back as `n13*TQAN DAWN`. `--codepoints` prints the result as `U+XXXX` values, and the text may come from standard input.

From Python:

```python
import encode

text = encode.encode("chalish-ceremonial", "n13*TQAN DAWN")
roman = encode.decode("chalish-ceremonial", text)
```

## Rows

The rows are in the order the file states them.

| Roman | Character | Code points |
| --- | --- | --- |
| `n0` | `󴀀` | U+F4000 |
| `n1` | `󴀁` | U+F4001 |
| `n2` | `󴀂` | U+F4002 |
| `n3` | `󴀃` | U+F4003 |
| `n4` | `󴀄` | U+F4004 |
| `n5` | `󴀅` | U+F4005 |
| `n6` | `󴀆` | U+F4006 |
| `n7` | `󴀇` | U+F4007 |
| `n8` | `󴀈` | U+F4008 |
| `n9` | `󴀉` | U+F4009 |
| `n10` | `󴀊` | U+F400A |
| `n11` | `󴀋` | U+F400B |
| `n12` | `󴀌` | U+F400C |
| `n13` | `󴀍` | U+F400D |
| `n14` | `󴀎` | U+F400E |
| `n15` | `󴀏` | U+F400F |
| `n16` | `󴀐` | U+F4010 |
| `n17` | `󴀑` | U+F4011 |
| `n18` | `󴀒` | U+F4012 |
| `n19` | `󴀓` | U+F4013 |
| `n20` | `󴀔` | U+F4014 |
| `n400` | `󴀕` | U+F4015 |
| `n8000` | `󴀖` | U+F4016 |
| `n160000` | `󴀗` | U+F4017 |
| `LORD` | `󴀠` | U+F4020 |
| `PATRIARCH` | `󴀡` | U+F4021 |
| `JAGUAR` | `󴀢` | U+F4022 |
| `SUN` | `󴀣` | U+F4023 |
| `MOON` | `󴀤` | U+F4024 |
| `WATER` | `󴀥` | U+F4025 |
| `PEAK` | `󴀦` | U+F4026 |
| `TQAN` | `󴀧` | U+F4027 |
| `SERPENT` | `󴀨` | U+F4028 |
| `SUN_AT_THE_EDGE` | `󴀩` | U+F4029 |
| `DEATH_JAGUAR` | `󴀪` | U+F402A |
| `STORM_SERPENT` | `󴀫` | U+F402B |
| `SACRED_STAR` | `󴀬` | U+F402C |
| `GOLDEN_GIVER` | `󴀭` | U+F402D |
| `SACRED_FLAME` | `󴀮` | U+F402E |
| `PEAK_BUILDER` | `󴀯` | U+F402F |
| `PATH_WALKER` | `󴀰` | U+F4030 |
| `MOON_DREAMER` | `󴀱` | U+F4031 |
| `LIVING_BLOSSOM` | `󴀲` | U+F4032 |
| `FALLEN_OWL` | `󴀳` | U+F4033 |
| `OVERLORD` | `󴀴` | U+F4034 |
| `KING` | `󴀵` | U+F4035 |
| `PRINCE` | `󴀶` | U+F4036 |
| `SEATED_LORD` | `󴀷` | U+F4037 |
| `LADY` | `󴀸` | U+F4038 |
| `LANDHOLDER` | `󴀹` | U+F4039 |
| `KNIGHT` | `󴀺` | U+F403A |
| `WAR_LEADER` | `󴀻` | U+F403B |
| `SUN_PRIEST` | `󴀼` | U+F403C |
| `PRIEST` | `󴀽` | U+F403D |
| `SCRIBE` | `󴀾` | U+F403E |
| `HERALD` | `󴀿` | U+F403F |
| `MASTER_MERCHANT` | `󴁀` | U+F4040 |
| `GUILDSMAN` | `󴁁` | U+F4041 |
| `FREEMAN` | `󴁂` | U+F4042 |
| `SERF` | `󴁃` | U+F4043 |
| `SLAVE` | `󴁄` | U+F4044 |
| `BIRTH` | `󴁅` | U+F4045 |
| `SEATING` | `󴁆` | U+F4046 |
| `DEATH` | `󴁇` | U+F4047 |
| `BURIAL` | `󴁈` | U+F4048 |
| `MARRIAGE` | `󴁉` | U+F4049 |
| `CAPTURE` | `󴁊` | U+F404A |
| `WAR` | `󴁋` | U+F404B |
| `CONQUEST` | `󴁌` | U+F404C |
| `TRIBUTE` | `󴁍` | U+F404D |
| `FOUNDATION` | `󴁎` | U+F404E |
| `DEDICATION` | `󴁏` | U+F404F |
| `OFFERING` | `󴁐` | U+F4050 |
| `ECLIPSE` | `󴁑` | U+F4051 |
| `PILGRIMAGE` | `󴁒` | U+F4052 |
| `ERAS_END` | `󴁓` | U+F4053 |
| `BALL_GAME` | `󴁔` | U+F4054 |
| `SKY` | `󴁕` | U+F4055 |
| `STAR` | `󴁖` | U+F4056 |
| `FIRE` | `󴁗` | U+F4057 |
| `EARTH` | `󴁘` | U+F4058 |
| `STONE` | `󴁙` | U+F4059 |
| `MAN` | `󴁚` | U+F405A |
| `WOMAN` | `󴁛` | U+F405B |
| `PLANT` | `󴁜` | U+F405C |
| `BEAST` | `󴁝` | U+F405D |
| `EAST` | `󴁞` | U+F405E |
| `WEST` | `󴁟` | U+F405F |
| `SOUTH` | `󴁠` | U+F4060 |
| `HIGH` | `󴁡` | U+F4061 |
| `LOW` | `󴁢` | U+F4062 |
| `INSIDE` | `󴁣` | U+F4063 |
| `OUTSIDE` | `󴁤` | U+F4064 |
| `HOUSE` | `󴁥` | U+F4065 |
| `HAND` | `󴁦` | U+F4066 |
| `EYE` | `󴁧` | U+F4067 |
| `MOUTH` | `󴁨` | U+F4068 |
| `UNDERWORLD` | `󴁩` | U+F4069 |
| `HEAVEN` | `󴁪` | U+F406A |
| `FIFTH_AGE` | `󴁫` | U+F406B |
| `LIVING_FLAME` | `󴁬` | U+F406C |
| `SOLAR_COUNT` | `󴁭` | U+F406D |
| `LUNAR_COUNT` | `󴁮` | U+F406E |
| `STELLAR_COUNT` | `󴁯` | U+F406F |
| `ISHILANKUL` | `󴁰` | U+F4070 |
| `KANKUL` | `󴁱` | U+F4071 |
| `SHELEM` | `󴁲` | U+F4072 |
| `ISHBAL_TSAKU` | `󴁳` | U+F4073 |
| `KUSHI_ISHBAL` | `󴁴` | U+F4074 |
| `QAPTEL_TSAKUL` | `󴁵` | U+F4075 |
| `SHELEM_ISHBAL` | `󴁶` | U+F4076 |
| `MATRIARCH` | `󴁷` | U+F4077 |
| `SON` | `󴁸` | U+F4078 |
| `DAUGHTER` | `󴁹` | U+F4079 |
| `FAMILY` | `󴁺` | U+F407A |
| `BIRTH_OF_A_BOY` | `󴁻` | U+F407B |
| `BIRTH_OF_A_GIRL` | `󴁼` | U+F407C |
| `DEATH_OF_A_MAN` | `󴁽` | U+F407D |
| `DEATH_OF_A_WOMAN` | `󴁾` | U+F407E |
| `HOUSEHOLD_FOUNDED` | `󴁿` | U+F407F |
| `HOUSEHOLD_ENDED` | `󴂀` | U+F4080 |
| `NORTH` | `󴂁` | U+F4081 |
| `NOBLE_LORD` | `󴂂` | U+F4082 |
| `NEOK_BAATE` | `󴂃` | U+F4083 |
| `DAWN` | `󴂄` | U+F4084 |
| `SUNSET` | `󴂅` | U+F4085 |
| `NOON` | `󴂆` | U+F4086 |
| `MIDNIGHT` | `󴂇` | U+F4087 |
| `GERMINATION` | `󴂈` | U+F4088 |
| `HARVEST` | `󴂉` | U+F4089 |
| `SEED_SOWN` | `󴂊` | U+F408A |
| `LIFETIME` | `󴂋` | U+F408B |
| `REBIRTH` | `󴂌` | U+F408C |
| `ERA_BEGINS` | `󴂍` | U+F408D |
| `PASSAGE_OF_THE_DEAD` | `󴂎` | U+F408E |
| `OUT_OF_THE_TRIALS` | `󴂏` | U+F408F |
| `WHOLE_ROUND` | `󴂐` | U+F4090 |
| `KINSMAN` | `󴂑` | U+F4091 |
| `STRANGER` | `󴂒` | U+F4092 |
| `HOME` | `󴂓` | U+F4093 |
| `VILLAGE` | `󴂔` | U+F4094 |
| `BOY` | `󴂕` | U+F4095 |
| `GIRL` | `󴂖` | U+F4096 |
| `ELDER` | `󴂗` | U+F4097 |
| `ELDER_WOMAN` | `󴂘` | U+F4098 |
| `PEOPLE` | `󴂙` | U+F4099 |
| `WOMEN` | `󴂚` | U+F409A |
| `GOD` | `󴂛` | U+F409B |
| `EXALTED_ANCESTOR` | `󴂜` | U+F409C |
| `SOUL_AMONG_THE_DEAD` | `󴂝` | U+F409D |
| `MEMORY` | `󴂞` | U+F409E |
| `OBSERVATION` | `󴂟` | U+F409F |
| `SECRET` | `󴂠` | U+F40A0 |
| `PROCLAMATION` | `󴂡` | U+F40A1 |
| `THE_UNKNOWN` | `󴂢` | U+F40A2 |
| `WRITING` | `󴂣` | U+F40A3 |
| `PRAYER` | `󴂤` | U+F40A4 |
| `CENOTE` | `󴂥` | U+F40A5 |
| `CAUTION` | `󴂦` | U+F40A6 |
| `KANKUL_SEAT` | `󴂧` | U+F40A7 |
| `ISHKUL` | `󴂨` | U+F40A8 |
| `CHAKUL` | `󴂩` | U+F40A9 |
| `TSALAM` | `󴂪` | U+F40AA |
| `KUSHI` | `󴂫` | U+F40AB |
| `TSUL` | `󴂬` | U+F40AC |
| `CHALISH` | `󴂭` | U+F40AD |
| `QEMUL` | `󴂮` | U+F40AE |
| `PUQEM` | `󴂯` | U+F40AF |
| `NELUSH` | `󴂰` | U+F40B0 |
| `CHAKAL` | `󴂱` | U+F40B1 |
| `TOSHEL` | `󴂲` | U+F40B2 |
| `SHAKNAL` | `󴂳` | U+F40B3 |
| `TSULTEL` | `󴂴` | U+F40B4 |
| `PENQAL` | `󴂵` | U+F40B5 |
| `SHELEM_BIRD` | `󴂶` | U+F40B6 |
| `ISHTEM` | `󴂷` | U+F40B7 |
| `QAPTEL` | `󴂸` | U+F40B8 |
| `NEOK` | `󴂹` | U+F40B9 |
| `a1` | `󴐀` | U+F4400 |
| `a2` | `󴐁` | U+F4401 |
| `i1` | `󴐂` | U+F4402 |
| `i2` | `󴐃` | U+F4403 |
| `i3` | `󴐄` | U+F4404 |
| `o1` | `󴐅` | U+F4405 |
| `u1` | `󴐆` | U+F4406 |
| `ka1` | `󴐇` | U+F4407 |
| `ka2` | `󴐈` | U+F4408 |
| `ka3` | `󴐉` | U+F4409 |
| `ke1` | `󴐊` | U+F440A |
| `ke2` | `󴐋` | U+F440B |
| `ki1` | `󴐌` | U+F440C |
| `ko1` | `󴐍` | U+F440D |
| `ko2` | `󴐎` | U+F440E |
| `ku1` | `󴐏` | U+F440F |
| `ku2` | `󴐐` | U+F4410 |
| `ku3` | `󴐑` | U+F4411 |
| `cha1` | `󴐒` | U+F4412 |
| `cha2` | `󴐓` | U+F4413 |
| `che1` | `󴐔` | U+F4414 |
| `che2` | `󴐕` | U+F4415 |
| `chi1` | `󴐖` | U+F4416 |
| `chi2` | `󴐗` | U+F4417 |
| `chu1` | `󴐘` | U+F4418 |
| `chu2` | `󴐙` | U+F4419 |
| `tsa1` | `󴐚` | U+F441A |
| `tsa2` | `󴐛` | U+F441B |
| `tse1` | `󴐜` | U+F441C |
| `tse2` | `󴐝` | U+F441D |
| `tsi1` | `󴐞` | U+F441E |
| `tsi2` | `󴐟` | U+F441F |
| `tso1` | `󴐠` | U+F4420 |
| `tso2` | `󴐡` | U+F4421 |
| `tsu1` | `󴐢` | U+F4422 |
| `tsu2` | `󴐣` | U+F4423 |
| `pa1` | `󴐤` | U+F4424 |
| `pa2` | `󴐥` | U+F4425 |
| `pe1` | `󴐦` | U+F4426 |
| `pe2` | `󴐧` | U+F4427 |
| `pi1` | `󴐨` | U+F4428 |
| `pi2` | `󴐩` | U+F4429 |
| `pi3` | `󴐪` | U+F442A |
| `po1` | `󴐫` | U+F442B |
| `pu1` | `󴐬` | U+F442C |
| `pu2` | `󴐭` | U+F442D |
| `qa1` | `󴐮` | U+F442E |
| `qa2` | `󴐯` | U+F442F |
| `qe1` | `󴐰` | U+F4430 |
| `qi1` | `󴐱` | U+F4431 |
| `qo1` | `󴐲` | U+F4432 |
| `qu1` | `󴐳` | U+F4433 |
| `ti1` | `󴐴` | U+F4434 |
| `to1` | `󴐵` | U+F4435 |
| `sha1` | `󴐶` | U+F4436 |
| `sha2` | `󴐷` | U+F4437 |
| `she1` | `󴐸` | U+F4438 |
| `shi1` | `󴐹` | U+F4439 |
| `shi2` | `󴐺` | U+F443A |
| `sho1` | `󴐻` | U+F443B |
| `sho2` | `󴐼` | U+F443C |
| `shu1` | `󴐽` | U+F443D |
| `shu2` | `󴐾` | U+F443E |
| `li1` | `󴐿` | U+F443F |
| `lu1` | `󴑀` | U+F4440 |
| `ma1` | `󴑁` | U+F4441 |
| `mu1` | `󴑂` | U+F4442 |
| `na1` | `󴑃` | U+F4443 |
| `na2` | `󴑄` | U+F4444 |
| `ne1` | `󴑅` | U+F4445 |
| `ne2` | `󴑆` | U+F4446 |
| `ni1` | `󴑇` | U+F4447 |
| `no1` | `󴑈` | U+F4448 |
| `no2` | `󴑉` | U+F4449 |
| `nu1` | `󴑊` | U+F444A |
| `nu2` | `󴑋` | U+F444B |
| `ha1` | `󴑌` | U+F444C |
| `ha2` | `󴑍` | U+F444D |
| `ha3` | `󴑎` | U+F444E |
| `hu1` | `󴑏` | U+F444F |
| `hu2` | `󴑐` | U+F4450 |
| `la1` | `󴑑` | U+F4451 |
| `la2` | `󴑒` | U+F4452 |
| `ba1` | `󴑓` | U+F4453 |
| `ba2` | `󴑔` | U+F4454 |
| `ta1` | `󴑕` | U+F4455 |
| `ta2` | `󴑖` | U+F4456 |
| `le1` | `󴑗` | U+F4457 |
| `le2` | `󴑘` | U+F4458 |
| `me1` | `󴑙` | U+F4459 |
| `me2` | `󴑚` | U+F445A |
| `mi1` | `󴑛` | U+F445B |
| `mi2` | `󴑜` | U+F445C |
| `yi1` | `󴑝` | U+F445D |
| `yi2` | `󴑞` | U+F445E |
| `yu1` | `󴑟` | U+F445F |
| `yu2` | `󴑠` | U+F4460 |
| `tu1` | `󴑡` | U+F4461 |
| `tu2` | `󴑢` | U+F4462 |
| `te1` | `󴑣` | U+F4463 |
| `te2` | `󴑤` | U+F4464 |
| `ya1` | `󴑥` | U+F4465 |
| `ya2` | `󴑦` | U+F4466 |
| `ye1` | `󴑧` | U+F4467 |
| `ye2` | `󴑨` | U+F4468 |
| `bi1` | `󴑩` | U+F4469 |
| `bi2` | `󴑪` | U+F446A |
| `lo1` | `󴑫` | U+F446B |
| `lo2` | `󴑬` | U+F446C |
| `hi1` | `󴑭` | U+F446D |
| `hi2` | `󴑮` | U+F446E |
| `he1` | `󴑯` | U+F446F |
| `he2` | `󴑰` | U+F4470 |
| `be1` | `󴑱` | U+F4471 |
| `be2` | `󴑲` | U+F4472 |
| `*` | `󴿰` | U+F4FF0 |
| `:` | `󴿱` | U+F4FF1 |
| `-` | `󠄍` | U+E010D |
| (space) | `󠄀` | U+E0100 |

## Round trip

Every encoding round-trips exactly: decoding the code points that encoding wrote gives back the roman text, and encoding that gives the same code points. The Code points column shows every character a row writes, including any that is invisible.

This page is written from `encodings/chalish-ceremonial.json` by `tools/encoding_docs.py`.
