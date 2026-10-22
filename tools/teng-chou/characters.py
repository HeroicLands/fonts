# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""The Teng Chou characters: one per Tantsou morpheme, each as an IDC formula.

    import characters as C

    C.CHARACTERS[0]              # Character("ho", "fire", "{fire}", ...)
    C.BY_MORPHEME["wong"].formula

A row is ``(morpheme, gloss, formula)``, with ``translit=True`` for a root that
exists to write foreign names, and ``overrides`` where the formula alone does not
fit the character well (see ``layout.py``: ``split``, ``first``, ``second``,
``inner``, ``scale``). The order is the order of the code points, so a new
character is added at the end and no character is renumbered. The glosses are the
Tantsou lexicon's.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import layout


@dataclass
class Character:
    morpheme: str
    gloss: str
    formula: str
    translit: bool = False
    overrides: dict = field(default_factory=dict)

    @property
    def kind(self) -> str:
        tree = layout.parse(self.formula)
        if isinstance(tree, layout.Leaf):
            return "meaning compound" if layout.K.COMPONENTS[tree.cid].idc else "pictograph"
        if any(isinstance(k, layout.Leaf) and k.sound for k in tree.kids):
            return "meaning and sound"
        return "meaning compound"

    @property
    def glyph(self) -> str:
        return f"tc.{self.morpheme}"


ROWS = [
    ('ho', 'fire', '{fire}'),
    ('jing', 'metal, gold', '{metal}'),
    ('mou', 'wood', '{wood}'),
    ('shou', 'water, river', '{water}'),
    ('tou', 'earth, soil', '{earth}'),
    ('weng', 'wind', '⿵{wind}‹teng›'),
    ('chai', 'mountain, peak, place', '{mountain}'),
    ('yan', 'cloud', '{cloud}'),
    ('zhi', 'star', '⿰{sun}‹zhei›'),
    ('you', 'moon, month', '{moon}'),
    ('luo', 'flower, lotus', '⿱{plant}‹huo›'),
    ('nou', 'field, garden', '{field}'),
    ('wong', 'sea, ocean', '⿰{water}‹mong›'),
    ('zhen', 'snow', '⿱{rain}{ice}'),
    ('chuen', 'frost', '⿰{ice}‹zhuen›'),
    ('rao', 'thunder', '⿱{rain}{field}'),
    ('la', 'lightning', '⿱{rain}‹ha›'),
    ('tui', 'iron', '⿰{metal}‹shui›'),
    ('wei', 'jade', '⿰{jade}‹mei›'),
    ('teng', 'heaven, the sky; celestial', '{sky}'),
    ('tan', 'celestial, of heaven', '⿱{sky}{sun}'),
    ('muo', 'green', '⿱{plant}‹mou›'),
    ('zhou', 'blue, azure; flowing', '⿰{water}‹you›'),
    ('rin', 'red, vermilion', '⿱{sun}{fire}'),
    ('bui', 'white, silver', '⿰{sun}‹shui›'),
    ('ha', 'dark, black, hidden; shadow', '⿱{cover}{sun}'),
    ('leng', 'bright, radiant; dawn', '⿰{sun}{moon}'),
    ('jen', 'nine', '⿰{count}‹zhen›'),
    ('wuen', 'five', '⿰{count}‹wen›'),
    ('wai', 'ten', '⿻{one}{one}'),
    ('rong', 'ten thousand, a myriad', '⿳{person}{person}{person}'),
    ('chen', 'emperor, king', '⿱{sky}‹zhen›'),
    ('zhuo', 'lord, sovereign', '⿰{person}‹zho›'),
    ('nei', 'sovereign, ruler', '⿰{person}‹zhei›'),
    ('gui', 'official, minister', '⿱{brush}‹shui›'),
    ('gen', 'master, teacher', '⿰{person}‹tsen›'),
    ('wuo', 'warrior, soldier', '⿰‹huo›{blade}'),
    ('chei', 'scholar, sage', '⿱{brush}‹zhei›'),
    ('yai', 'healer, physician', '⿸{sickness}‹chai›'),
    ('zhei', 'son, child', '{child}'),
    ('nong', 'person, folk', '{person}'),
    ('nui', 'bound, enslaved', '⿰{thread}‹shui›'),
    ('tsou', 'tribe, group, people', '⿰{person}‹shou›'),
    ('zhao', 'house, clan, family', '⿱{roof}‹rao›'),
    ('ken', 'hearth, household', '⿱‹sen›{fire}'),
    ('shuo', 'trade', '⿰{wealth}‹shou›'),
    ('ja', 'blade', '{blade}'),
    ('huo', 'hand', '{hand}'),
    ('wen', 'centre, middle', '⿴{enclosure}{one}'),
    ('wou', 'court, palace, hall', '⿱{roof}‹mou›'),
    ('wo', 'divine, sacred', '⿰{sacred}‹ho›'),
    ('lei', 'breath, spirit', '⿱{spirit}‹len›'),
    ('sei', 'bureau, office, ministry', '⿸{shelter}‹mei›'),
    ('lou', 'law, rule', '⿰{step}‹nou›'),
    ('dou', 'path, road, journey', '⿺{motion}{foot}'),
    ('hou', 'balance, harmony, calm', '⿰{person}{person}'),
    ('tsai', 'creation, craft', '⿰{hand}‹wai›'),
    ('huen', 'chaos, disorder', '⿰{water}‹zhuen›'),
    ('sing', 'death', '⿰{death}{person}'),
    ('zha', 'life, birth', '⿱{plant}{earth}'),
    ('nuo', 'decay, rot', '⿰{death}‹nou›'),
    ('fa', 'wealth, fortune', '⿰{wealth}‹ja›'),
    ('chou', 'knowledge, lore, record', '⿰{speech}‹you›'),
    ('duo', 'sorcery, magic', '⿱{spirit}‹dou›'),
    ('rui', 'ritual, ceremony, dance', '⿰{sacred}‹shui›'),
    ('jui', 'festival', '⿰{sun}‹shui›'),
    ('tsei', 'self, own', '⿱‹tsi›{heart}'),
    ('wan', 'account, reckoning, tally', '⿰{count}‹yan›'),
    ('nie', 'year', '⿱{grain}{person}'),
    ('mei', 'dream', '⿱{moon}{eye}'),
    ('zho', 'dragon', '{dragon}'),
    ('hen', 'tiger', '⿰{beast}‹hin›'),
    ('zhai', 'bird, phoenix, crane', '{bird}'),
    ('gwo', 'tortoise', '⿰{crawler}‹ho›'),
    ('sou', 'serpent', '⿰{crawler}‹tou›'),
    ('mai', 'horse', '{horse}'),
    ('bei', 'ape', '⿰{beast}‹mei›'),
    ('zhin', 'boar', '⿰{beast}‹rin›'),
    ('yo', 'demon, fiend', '⿱{spirit}‹zho›'),
    ('jei', 'a horned beast of good omen', '⿰{beast}‹zhei›'),
    ('cheng', 'to rise, to ascend', '⿺{motion}‹leng›'),
    ('jong', 'to fall, to descend', '⿰{foot}‹rong›'),
    ('chiao', 'to freeze; winter', '⿰{ice}{water}'),
    ('wa', 'to answer, to echo', '⿰{mouth}‹zha›'),
    ('dao', 'great, supreme', '⿱{one}{person}'),
    ('kuo', 'old, ancient, eternal', '⿱{old}‹huo›'),
    ('shui', 'new, lesser, small', '⿱{small}{mark}'),
    ('hing', 'to see, to look', '⿰{eye}‹jing›'),
    ('jie', 'sight, view; what is seen', '⿱{light}‹nie›'),
    ('ten', 'to hear, to listen', '⿰{ear}‹tan›'),
    ('yong', 'sound, voice', '⿰{mouth}‹nong›'),
    ('sin', 'to smell', '⿰{nose}‹sing›'),
    ('fai', 'smell, scent, odour', '⿱{plant}‹mai›'),
    ('tsie', 'to taste', '⿰{mouth}‹ha›'),
    ('ruo', 'taste, flavour', '⿰{food}‹huo›'),
    ('gai', 'to touch, to feel with the hand', '⿰{hand}‹zhai›'),
    ('tsen', 'heart; seat of feeling', '{heart}'),
    ('hin', 'love, to cherish', '⿰{heart}{hand}'),
    ('yei', 'to want, to desire', '⿱‹zhei›{heart}'),
    ('hao', 'head', '⿰‹hou›{head}'),
    ('sao', 'hair of the head', '⿰‹dao›{hair}'),
    ('lan', 'face', '⿰‹yan›{head}'),
    ('ching', 'eye', '{eye}'),
    ('lui', 'ear', '⿰{ear}‹leng›'),
    ('fong', 'nose', '⿰{nose}‹mong›'),
    ('tsong', 'mouth', '{mouth}'),
    ('ga', 'tooth', '⿱‹ha›{tooth}'),
    ('lie', 'tongue', '⿰{mouth}‹nie›'),
    ('beng', 'neck, throat', '⿰{flesh}‹teng›'),
    ('kong', 'shoulder', '⿰{flesh}‹tsong›'),
    ('bin', 'arm', '⿰{flesh}‹rin›'),
    ('jeng', 'joint, knot; where a limb bends', '⿰{bone}‹jing›'),
    ('ting', 'finger', '⿰{hand}‹ching›'),
    ('hong', 'chest, breast-bone', '⿰{flesh}‹rong›'),
    ('nen', 'breast', '⿰{woman}‹len›'),
    ('tuo', 'belly', '⿰{flesh}‹tou›'),
    ('shai', 'back', '⿰{flesh}‹chai›'),
    ('kuen', 'hip', '⿰{flesh}‹zhuen›'),
    ('jo', 'leg', '⿰{foot}‹zho›'),
    ('dai', 'foot', '{foot}'),
    ('lo', 'skin, hide', '⿰‹ho›{skin}'),
    ('ko', 'bone', '⿰{bone}‹ho›'),
    ('chui', 'blood', '⿱‹shui›{vessel}'),
    ('muen', 'flesh, meat', '⿰{flesh}‹zhuen›'),
    ('mi', 'woman; female', '{woman}'),
    ('chan', 'man; male', '⿰‹yan›{strength}'),
    ('sho', 'to eat', '⿰{food}‹zho›'),
    ('ta', 'food, meal', '⿰{food}‹tao›'),
    ('hui', 'to drink', '⿰{water}‹hou›'),
    ('sa', 'drink', '⿱‹ja›{water}'),
    ('fou', 'to breathe', '⿰{nose}‹mou›'),
    ('min', 'to sleep', '⿰{eye}‹mi›'),
    ('liao', 'urine', '⿰{water}‹chiao›'),
    ('bou', 'dung, excrement', '⿰{earth}‹mou›'),
    ('jin', 'warmth; warm', '⿱‹hin›{fire}'),
    ('gan', 'table', '⿰{wood}‹tan›'),
    ('tong', 'floor', '⿰{stone}‹nong›'),
    ('zheng', 'wall', '⿰{earth}‹zhen›'),
    ('zhuen', 'roof', '{roof}'),
    ('zhong', 'house, home, abode', '⿱{roof}‹tsong›'),
    ('sen', 'door, gate', '{door}'),
    ('kin', 'lock; to lock', '⿰{metal}‹hin›'),
    ('ling', 'cup', '⿱‹sing›{vessel}'),
    ('gwou', 'bowl', '⿱‹hou›{vessel}'),
    ('rai', 'spoon', '⿰{metal}‹dai›'),
    ('ban', 'pot', '⿱‹tan›{earth}'),
    ('shen', 'cloth', '⿰{thread}‹zhen›'),
    ('tsi', 'one', '{one}'),
    ('len', 'two', '⿱{one}{one}'),
    ('tao', 'three', '⿳{one}{one}{one}'),
    ('fei', 'four', '⿰{count}‹mei›'),
    ('jou', 'six', '⿰{count}‹shou›'),
    ('tai', 'seven', '⿰{count}‹dai›'),
    ('mo', 'eight', '⿰{count}‹mong›'),
    ('gou', 'hundred', '⿰{count}‹hou›'),
    ('keng', 'thousand', '⿰{count}‹teng›'),
    ('chuo', 'rank, place in order', '⿰{step}‹huo›'),
    ('tsan', 'half', '⿰‹tsen›{blade}'),
    ('chong', 'many, much', '⿰{person}‹rong›'),
    ('bo', 'few, little', '⿱{small}‹ho›'),
    ('mong', 'none, nothing; not', '⿱{cover}{person}'),
    ('jao', 'yellow', '⿰{field}‹rao›'),
    ('kui', 'grey, ash-coloured', '⿱‹shui›{fire}'),
    ('jan', 'brown', '⿰{earth}‹yan›'),
    ('na', 'mother', '⿰{woman}‹zha›'),
    ('to', 'father', '⿰{hand}‹tou›'),
    ('dong', 'brother', '⿰{person}‹dou›'),
    ('nin', 'sister', '⿰{woman}‹rin›'),
    ('dei', 'to be', '⿰{mouth}‹dai›'),
    ('kai', 'to have', '⿰{hand}‹wai›'),
    ('rou', 'to go', '⿺{motion}‹nou›'),
    ('nao', 'to come', '⿺{motion}‹rao›'),
    ('zhan', 'to give', '⿰{hand}‹yan›'),
    ('dui', 'to take', '⿰{hand}‹dao›'),
    ('shao', 'to make', '⿰‹tao›{strike}'),
    ('tsiao', 'to do', '⿰‹huo›{strike}'),
    ('ya', 'to say', '⿰{mouth}‹ja›'),
    ('tsuen', 'to speak, to talk', '⿰{speech}‹tsen›'),
    ('tsing', 'to know', '⿱‹sing›{heart}'),
    ('sai', 'to think', '⿱‹zhai›{heart}'),
    ('shan', 'to live', '⿰{person}‹yan›'),
    ('fen', 'to die', '⿰{death}‹wen›'),
    ('tuen', 'to walk', '⿰{step}‹zhuen›'),
    ('ruen', 'to run', '⿰{foot}‹zhuen›'),
    ('den', 'to sit', '⿰{earth}‹sen›'),
    ('ki', 'to stand', '⿰{person}‹mi›'),
    ('yuen', 'to lie down', '⿱{roof}‹you›'),
    ('gwen', 'to hold', '⿰{hand}‹wen›'),
    ('hai', 'to bring, to carry', '⿺{motion}‹mai›'),
    ('ra', 'to put, to set down', '⿰{hand}‹zha›'),
    ('zhing', 'to find', '⿰{eye}‹jing›'),
    ('shin', 'to lose', '⿰{step}‹rin›'),
    ('ka', 'to open', '⿵{door}‹ha›'),
    ('seng', 'to close, to shut', '⿵{door}‹leng›'),
    ('chao', 'to begin', '⿰{sun}‹chiao›'),
    ('luen', 'to end, to finish', '⿰{thread}‹len›'),
    ('si', 'pearl', '⿰{jade}‹tsi›', True),
    ('do', 'pine', '⿰{wood}‹dou›', True),
    ('ri', 'sail', '⿰{thread}‹mi›', True),
    ('ma', 'song', '⿰{mouth}‹mai›', True),
    ('da', 'feather', '⿰‹dao›{bird}', True),
    ('rei', 'dew', '⿱{rain}‹mei›', True),
    ('di', 'drum', '⿰‹tsi›{strike}', True),
    ('tei', 'ink', '⿰{water}‹zhei›', True),
    ('go', 'gourd', '⿱{plant}‹ho›', True),
    ('ti', 'bell', '⿰{metal}‹mi›', True),
    ('ro', 'reed', '⿱{plant}‹rong›', True),
    ('ni', 'willow', '⿰{wood}‹nie›', True),
    ('ba', 'plum', '⿰{wood}‹ja›', True),
    ('li', 'silk', '⿰{thread}‹tsi›', True),
    ('no', 'honey', '⿰{food}‹nong›', True),
    ('ran', 'lacquer', '⿰{wood}‹tan›', True),
    ('shi', 'comb', '⿰{wood}‹mi›', True),]

# Hand-tuned overrides, by morpheme: where the formula's default fit is not good enough.
OVERRIDES: dict[str, dict] = {
    # ice's three short strokes take a narrow column, so water has the room
    "chiao": {"split": 0.3},
    # fire's two tallies drawn under a narrow top would stand apart from it
    "ken": {"split": 0.64, "second": {"slot": (170, 70, 830, 330), "grow": 1.8}},
    "kui": {"split": 0.62, "second": {"slot": (150, 70, 850, 340), "grow": 1.8}},
    # chiao, itself two columns, takes the room it needs as a sound component
    "chao": {"split": 0.28},
    "jin": {"split": 0.64, "second": {"slot": (150, 70, 850, 330), "grow": 1.8}},
}


def _build():
    out = []
    for row in ROWS:
        morpheme, gloss, formula, *rest = row
        out.append(Character(morpheme, gloss, formula, bool(rest and rest[0]), OVERRIDES.get(morpheme, {})))
    return out


CHARACTERS = _build()
BY_MORPHEME = {c.morpheme: c for c in CHARACTERS}
