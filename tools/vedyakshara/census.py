# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Count the consonant pairs of Vedyari, to choose the fused signs.

    .venv/bin/python tools/vedyakshara/census.py PATH/TO/Skills/Languages/Vedyari.md

Reads the note's frontmatter: the words, the affixes, the given and clan names,
the elements and the register entries tagged ``vedyari``. A digraph (ch sh kh gh
bh ny ng, and th dh ts) and the pairs ai and au count as one unit; a compound's
parts are counted as separate forms. Prints each pair with the number of times
it occurs across the distinct forms, commonest first, and the lexicon's own
count, which breaks a tie at the foot of the fused list.
"""

import collections
import re
import sys

import yaml

DIGRAPHS = ["ch", "sh", "kh", "gh", "bh", "ny", "ng", "th", "dh", "ts", "ai", "au"]
VOWELS = {"a", "e", "i", "o", "u", "ai", "au"}


def units(word):
    out, i = [], 0
    while i < len(word):
        if word[i:i + 2] in DIGRAPHS:
            out.append(word[i:i + 2])
            i += 2
        else:
            out.append(word[i])
            i += 1
    return out


def pairs(word):
    u = units(word)
    return [a + b for a, b in zip(u, u[1:]) if a not in VOWELS and b not in VOWELS]


def forms(data):
    found = set()

    def add(s):
        for w in re.split(r"[\s\-']+", str(s)):
            w = re.sub(r"[^a-zA-Z]", "", w).lower()
            if w:
                found.add(w)

    def walk(x):
        if isinstance(x, str):
            add(x)
        elif isinstance(x, list):
            for i in x:
                walk(i)
        elif isinstance(x, dict):
            for v in x.values():
                walk(v)

    for w in data["words"]:
        add(w["form"])
    for a in data["affixes"]:
        add(a["form"])
    walk({k: v for k, v in data["names"].items() if k != "pattern"})
    for e in data["elements"]:
        add(e["form"])
    for r in data["register"]:
        if r.get("tongue") == "vedyari":
            add(r["name"])
    lexicon = {re.sub(r"[^a-z]", "", w["form"].lower()) for w in data["words"]}
    return found, lexicon


def main():
    text = open(sys.argv[1], encoding="utf-8").read()
    data = yaml.safe_load(text.split("\n---", 1)[0].lstrip("-\n"))["data"]
    every, lexicon = forms(data)
    count = collections.Counter(p for w in every for p in pairs(w))
    lex = collections.Counter(p for w in lexicon for p in pairs(w))
    print(f"{len(every)} forms, {len(count)} distinct pairs, {sum(count.values())} occurrences")
    for i, (p, n) in enumerate(sorted(count.items(), key=lambda kv: (-kv[1], -lex[kv[0]])), 1):
        print(f"{i:3} {p:5} {n:4}  lexicon {lex[p]}")
        if i == 30:
            break


if __name__ == "__main__":
    main()
