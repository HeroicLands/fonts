# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Write ``encodings/names.json``, the names of the script fonts' characters.

    python3 tools/encoding_names.py           # write the file
    python3 tools/encoding_names.py --check   # fail where the file differs

``encode.py`` reads a code between the literal immutable markers as a character's name.
The names of the private-use characters are those of ``tools/names/<script>.json``, which
the charts and the code point tables read; this file gathers them into one table that
ships beside the encodings, since ``tools/`` is not shipped. A code point or a name stated
in two scripts is a finding. It runs under any Python 3.9 or later with the standard
library alone. A finding is ``file:line:column: error: message`` and the exit status is 1.
"""

import argparse
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
import encode as E  # noqa: E402

SOURCES = os.path.join(HERE, "names")


def gather(sources=SOURCES):
    """The names by code point, and the findings. Code points are in order."""
    names = {}
    seen = {}
    findings = []
    for path in sorted(glob.glob(os.path.join(sources, "*.json"))):
        with open(path, encoding="utf-8") as handle:
            table = json.load(handle)
        for point, name in table.items():
            if point in names:
                findings.append(f"{E._shown(path)}: error: {point} is also named in another script")
            elif name in seen:
                findings.append(f"{E._shown(path)}: error: {name} also names {seen[name]}")
            else:
                names[point] = name
                seen[name] = point
    return dict(sorted(names.items(), key=lambda pair: int(pair[0][2:], 16))), findings


def dumps(names):
    """The table as its file is laid out: one name to a line."""
    lines = [f"    {json.dumps(p)}: {json.dumps(n)}" for p, n in names.items()]
    return "{\n" + ",\n".join(lines) + "\n}\n"


def path_of(directory=E.ENCODINGS):
    return os.path.join(directory, E.NAMES + ".json")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="check the file rather than write it")
    args = parser.parse_args(argv)
    names, findings = gather()
    path = path_of()
    text = dumps(names)
    try:
        with open(path, encoding="utf-8") as handle:
            current = handle.read()
    except OSError:
        current = None
    if current != text:
        if args.check:
            findings.append(f"{E._shown(path)}: error: the names differ from tools/names; "
                            "run python3 tools/encoding_names.py")
        else:
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(text)
    for finding in findings:
        print(finding, file=sys.stderr)
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
