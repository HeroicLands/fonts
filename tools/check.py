# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Check the built fonts, every check at once, as CI does.

    .venv/bin/python tools/check.py [-j N] [--font FAMILY ...] [--list]

``FONTS`` names each built font's own checks and ``SHARED`` the checks that read every
font, each a command run from the repository root. Every font's proof in
``tools/prove_guards.py`` runs as its own command, ``--font`` on that font, and the rest
of the proof as ``--shared``. The commands run in parallel, the longest first, and each
one's output is printed whole when it ends, headed by the command, its time and its exit
status. The script exits 1 when any command fails.

Before running anything it refuses a table out of step with the repository:

- a built font in ``fonts/`` with no entry in ``FONTS``, or an entry with no built font;
- a check script under ``tools/`` that no command runs: a font check (``check_font.py``,
  ``check_*_font.py``), a guard (``guard.py``, ``*_guard.py``) or a distinctness check
  (``*_distinct.py``).

``--font FAMILY`` runs only that font's checks and proof, by its file's family name
(``ChalishPilamCeremonial``); ``--list`` prints the commands and runs nothing.
"""

import argparse
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = sys.executable

# Each font's checks, by the family name of its built font. The slowest come first in
# each list, and the fonts with the slowest checks first in the table, so that the run
# starts on them.
FONTS = {
    "ChalishPilamCeremonial": [
        "tools/chalish-pilam/ceremonial_guard.py",  # every block layout shapes as blocks.py lays it out
        "tools/chalish-pilam/compact_distinct.py",  # no two compact forms look alike
        "tools/chalish-pilam/compact_sweep.py",  # every compact form stays carvable in every layout
        "tools/chalish-pilam/carving.py",  # every ceremonial glyph and composed block can be carved
        "tools/chalish-pilam/syllabary_distinct.py",  # no two syllable signs of different syllables look alike
        "tools/chalish-pilam/check_ceremonial_font.py",
    ],
    "ChalishPilamCommon": [
        "tools/chalish-pilam/check_font.py",
        "tools/chalish-pilam/guard.py --fixtures-only",  # the night entry and every glyph shape to their own glyphs
    ],
    "KhelathiZethuGlyphs": [
        "tools/khelathi-zethu-glyphs/check_font.py",
        "tools/khelathi-zethu-glyphs/guard.py",  # the scene inscriptions shape right to left, every form reachable
        "tools/khelathi-zethu-glyphs/quadrats.py",  # quadrats and cartouches land where the layout puts them
        "tools/khelathi-zethu-glyphs/paint_guard.py",  # every drawn sign has a paint map
    ],
    "TengChou": [
        "tools/teng-chou/syllabary_distinct.py",  # the Jurthati signs stay distinct at body size
        "tools/teng-chou/check_font.py",
        "tools/teng-chou/guard.py --fixtures-only",
        "tools/teng-chou/stroke_mix.py",  # every character's body is strokes, dabs a minority
    ],
    "PirzathCarved": [
        "tools/pirzath/check_font.py",
        "tools/pirzath/guard.py --fixtures-only",
    ],
    "PirzathHand": [
        "tools/pirzath-hand/check_font.py",
        "tools/pirzath-hand/guard.py --fixtures-only",
    ],
    "ThuravarkCarved": [
        "tools/thuravark-carved/check_font.py",
        "tools/thuravark-carved/guard.py --fixtures-only",
    ],
    "QalezuHand": [
        "tools/qalezu-hand/check_font.py",
        "tools/qalezu-hand/guard.py --fixtures-only",
    ],
    "SemaronKuriale": [
        "tools/semaron-kuriale/check_font.py",
        "tools/semaron-kuriale/guard.py --fixtures-only",
    ],
    "Veldikko": [
        "tools/veldikko/check_font.py",
        "tools/veldikko/guard.py --fixtures-only",  # the fixtures join and carry their marks
    ],
    "VedyaksharaClassical": [
        "tools/vedyakshara/check_font.py",
        "tools/vedyakshara/guard.py --fixtures-only",
    ],
    "HelonikaBook": [
        "tools/helonika/check_font.py",
        "tools/helonika/guard.py --fixtures-only",
    ],
}

# The checks that read every font, or none.
SHARED = [
    "tools/prove_guards.py --shared",
    "tools/specimen_pages.py --check",  # every specimen page and README cell match the fonts and specimens/texts.json
    "tools/spacing.py",  # every face is set at a natural spacing; --report prints the measures
    "tools/codepoints.py",  # each face draws its own code points and states no spelling
    "tools/notdef_box.py",
    "tools/vertical.py",
    "tools/font_names.py",
    "tools/encodings_guard.py --require-fonts",
    "tools/keyboards_guard.py",  # the layouts type each sound's output, and nothing else
    "tools/charts_guard.py",  # every character is on its sheet; unnamed rows are listed
    "tools/sample_texts.py",
]

CHECK_SCRIPTS = ("check_font.py", "check_*_font.py", "guard.py", "*_guard.py", "*_distinct.py")


def built() -> set[str]:
    return {p.name.split("-")[0] for p in (ROOT / "fonts").glob("*-Regular.ttf")}


def commands(families) -> list[str]:
    out = []
    for family in families:
        out.append(f"tools/prove_guards.py --font fonts/{family}-Regular.ttf")
        out += FONTS[family]
    return out


def problems() -> list[str]:
    found = []
    fonts = built()
    for family in sorted(fonts - FONTS.keys()):
        found.append(f"fonts/{family}-Regular.ttf: error: a built font with no checks in tools/check.py")
    for family in sorted(FONTS.keys() - fonts):
        found.append(f"tools/check.py: error: {family} has checks but no built font fonts/{family}-Regular.ttf")
    run = {c.split()[0] for c in commands(FONTS) + SHARED}
    for pattern in CHECK_SCRIPTS:
        for script in sorted((ROOT / "tools").rglob(pattern)):
            rel = script.relative_to(ROOT).as_posix()
            if rel not in run:
                found.append(f"{rel}: error: a check that tools/check.py does not run")
    return found


def run(command: str):
    start = time.monotonic()
    done = subprocess.run([PY, *command.split()], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return command, done.returncode, time.monotonic() - start, done.stdout


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("-j", "--jobs", type=int, default=min(8, os.process_cpu_count() or 1))
    ap.add_argument("--font", action="append", metavar="FAMILY", help="run only this font's checks")
    ap.add_argument("--list", action="store_true", help="print the commands and run nothing")
    a = ap.parse_args()
    found = problems()
    for p in found:
        print(p)
    if found:
        return 1
    unknown = [f for f in a.font or [] if f not in FONTS]
    if unknown:
        print(f"tools/check.py: error: no font {', '.join(unknown)}; the fonts are {', '.join(FONTS)}")
        return 1
    todo = commands(a.font) if a.font else commands(FONTS) + SHARED
    if a.list:
        print("\n".join(todo))
        return 0
    failed = []
    start = time.monotonic()
    with ThreadPoolExecutor(a.jobs) as pool:
        for job in as_completed([pool.submit(run, c) for c in todo]):
            command, status, seconds, output = job.result()
            print(f"--- {command} ({seconds:.0f} s, exit {status})", flush=True)
            print(output, end="" if output.endswith("\n") or not output else "\n", flush=True)
            if status:
                failed.append(command)
    print(f"{len(todo)} checks in {time.monotonic() - start:.0f} s: "
          + (f"{len(failed)} failed: {', '.join(failed)}" if failed else "ok"))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
