# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Write ``keyboards/sounds.json``: what each sound of ``tools/sound_keys.json`` is in each script that has a keyboard layout.

    python3 tools/sounds.py                       # print
    python3 tools/sounds.py --write               # write the file
    python3 tools/sounds.py --encoding vedyakshara=FILE

A sound's output is its spelling run through the script's encoding, ``encodings/<script>.json``
or the file ``--encoding <script>=<file>`` names for a script, by ``encode.py``. A sound with
a ``context`` is encoded inside it (``context: ["t", "t"]`` encodes ``tat`` for ``a``), and its
output is the pieces that lie within the sound; a piece that runs across the sound's edge is an
error. A script whose encoding needs another context for a sound names it in the sound's
``contexts``, keyed by script.

A sound is unmapped in a script, and its key types nothing there, when a character of it
passes through the encoding unchanged (``"no row"``) or when the encoding writes it only as
non-writing marks (``"writes nothing"``). A key never types a mark. Every face an encoding lists must give the same output.
"""

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
import encode as E  # noqa: E402

OUT = os.path.join(ROOT, "keyboards", "sounds.json")
# The scripts with a keyboard layout, by the key the tools use and the encoding that writes each.
SCRIPTS = ["semaron", "pirzath", "thuravark", "qalezu", "veldikko", "vedyakshara", "helonika"]


def hexes(text):
    return " ".join(f"U+{ord(c):04X}" for c in text)


def spell(enc, face, sound, script):
    """``{"codepoints"}`` or ``{"unmapped"}`` for one sound under one face."""
    before, after = sound.get("contexts", {}).get(script) or sound.get("context") or ["", ""]
    start = len(before)
    end = start + len(sound["spelling"])
    text = before + sound["spelling"] + after
    within = []
    at = 0
    for source, target, row in E.pieces(enc, text, face, strict=False):
        if at < end and at + len(source) > start:
            if at < start or at + len(source) > end:
                raise SystemExit(
                    f"tools/sounds.py: error: {sound['sound']}: the row {json.dumps(source, ensure_ascii=False)} "
                    f"runs across the edge of the sound in {json.dumps(text, ensure_ascii=False)}"
                )
            within.append((target, row))
        at += len(source)
    if any(row is None for _, row in within):
        return {"unmapped": "no row"}
    # A key types what the script draws. The non-writing marks an encoding adds keep roman
    # text intact across a round trip; typed text has no roman to keep.
    out = "".join(c for target, _ in within for c in target if not E.is_mark(c))
    if not out:
        return {"unmapped": "writes nothing"}
    return {"codepoints": hexes(out)}


def build(files=None):
    """The ``sounds.json`` document. ``files`` names an encoding file to read for a script instead."""
    files = files or {}
    with open(os.path.join(HERE, "sound_keys.json"), encoding="utf-8") as handle:
        keys = json.load(handle)
    encodings = {script: E.load(files.get(script) or script) for script in SCRIPTS}
    sounds = []
    for sound in keys["sounds"]:
        scripts = {}
        for script, enc in encodings.items():
            each = [spell(enc, face, sound, script) for face in enc.fonts]
            if any(e != each[0] for e in each):
                raise SystemExit(f"tools/sounds.py: error: {sound['sound']}: the faces of {script} disagree")
            scripts[script] = each[0]
        sounds.append({"sound": sound["sound"], "spelling": sound["spelling"], "scripts": scripts})
    source = {script: {"encoding": enc.name, "faces": list(enc.fonts)} for script, enc in encodings.items()}
    return {"source": source, "sounds": sounds}


def serialise(doc):
    """The document as written to disk: one sound per line."""
    one = lambda value: json.dumps(value, ensure_ascii=False, separators=(",", ":"))  # noqa: E731
    lines = ["{", f'  "source": {one(doc["source"])},', '  "sounds": [']
    for n, sound in enumerate(doc["sounds"]):
        lines.append(f"    {one(sound)}" + ("," if n < len(doc["sounds"]) - 1 else ""))
    lines += ["  ]", "}", ""]
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--write", action="store_true", help="write keyboards/sounds.json")
    parser.add_argument("--encoding", action="append", default=[], metavar="SCRIPT=FILE",
                        help="apply an encoding file for a script instead of encodings/<script>.json")
    args = parser.parse_args(argv)
    try:
        text = serialise(build(dict(entry.split("=", 1) for entry in args.encoding)))
    except E.EncodingError as error:
        for fault in error.faults:
            print(fault, file=sys.stderr)
        return 1
    if args.write:
        with open(OUT, "w", encoding="utf-8") as handle:
            handle.write(text)
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
