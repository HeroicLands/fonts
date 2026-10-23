# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Write roman text in a script's code points by thalorna's mapping notes.

    from mapped import Mapping
    semaron = Mapping("semaron", thalorna=Path("~/dev/HeroicLands/thalorna"))
    semaron.write(["Zaron tholmeza"])          # the code points, one string per text

The fonts convert no spelling: a face draws its own code points and nothing
else. A guard or a specimen that starts from roman text therefore writes it
through the script's mapping note first, as a run marked ``map=`` is written.
The conversion is ``tools/mapping.mjs`` under ``node``, which reads the note
from the thalorna checkout's ``origin/main``, or from the file ``note`` names,
and applies package-build's own mapping rules. One ``node`` process converts a
whole list, and each text is converted once.

The guards' fixtures and the specimens' sample lines are also written once into
``tools/mapped.json``, so that the fixtures, the guard proofs and the spacing
guard run with no thalorna checkout (``Mapping.offline``):

    .venv/bin/python tools/mapped.py --thalorna ~/dev/HeroicLands/thalorna --write   # write the file
    .venv/bin/python tools/mapped.py --thalorna ~/dev/HeroicLands/thalorna           # check it

``--map-note SCRIPT=FILE`` reads one script's mapping note from a file instead, as
the guards' ``--map-note`` does.

Without ``--write`` the file is written afresh in memory and compared, and any
text that differs is reported, so a change to a mapping note that a fixture
meets is found.
"""

import argparse
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOL = ROOT / "tools" / "mapping.mjs"
THALORNA = Path.home() / "dev/HeroicLands/thalorna"
CACHE = ROOT / "tools" / "mapped.json"
NOTES = "assets/content/Lore/Scripts"
# The faces whose fixtures and samples are cached, with their script.
FACES = {
    "semaron-kuriale": "semaron",
    "pirzath-carved": "pirzath",
    "pirzath-hand": "pirzath",
    "thuravark-carved": "thuravark",
    "qalezu-hand": "qalezu",
    "vedyakshara-classical": "vedyakshara",
    "helonika-book": "helonika",
    "helonika-bizarian": "bizarian",
    "helonika-bethuan": "bethuan",
}
# A cache key that is a face written by another tongue's mapping note: the face it is drawn in.
DRAWN_IN = {"helonika-bizarian": "helonika-book", "helonika-bethuan": "helonika-book"}


class Mapping:
    """The mapping note of one script, applied for one face."""

    def __init__(self, script: str, thalorna: Path | None = None, note: Path | None = None, face: str | None = None):
        self.script = script
        self.thalorna = Path(thalorna) if thalorna else THALORNA
        self.note = Path(note) if note else None
        self.face = face
        self._done: dict[str, dict] = {}
        self._offline = False

    @classmethod
    def offline(cls, face: str) -> "Mapping":
        """The mapping of a face as tools/mapped.json records it, for its fixtures and samples alone."""
        m = cls(FACES[face], face=face)
        m._offline = True
        cache = json.loads(CACHE.read_text(encoding="utf-8"))
        m._done = {t: dict(r) for t, r in cache["faces"][face].items()}
        return m

    def records(self, texts: list[str]) -> list[dict]:
        """``{"text": ..., "unmapped": [...]?}`` for each text, as tools/mapping.mjs writes it."""
        todo = sorted({t for t in texts if t not in self._done})
        if todo and self._offline:
            raise SystemExit(
                f"tools/mapped.json: error: {self.face}: {todo[0]!r} is not recorded; "
                "run tools/mapped.py --thalorna <checkout> --write"
            )
        if todo:
            source = ["--note", str(self.note)] if self.note else ["--thalorna", str(self.thalorna)]
            args = ["node", str(TOOL), *source, self.script, *([self.face] if self.face else [])]
            run = subprocess.run(args, input=json.dumps(todo), capture_output=True, text=True, cwd=ROOT)
            if run.returncode:
                raise SystemExit(f"tools/mapping.mjs: error: {run.stderr.strip()}")
            self._done.update(zip(todo, json.loads(run.stdout)))
        return [self._done[t] for t in texts]

    def write(self, texts: list[str]) -> list[str]:
        return [r["text"] for r in self.records(texts)]

    def one(self, text: str) -> str:
        return self.write([text])[0]


class MappedRenderer:
    """A Renderer whose text is roman, written through a mapping before it is shaped.

    ``shape``, ``glyph_names``, ``text`` and ``width`` take roman text; everything
    else is the wrapped Renderer's.
    """

    def __init__(self, renderer, mapping: Mapping):
        self.renderer = renderer
        self.mapping = mapping

    def __getattr__(self, name):
        return getattr(self.renderer, name)

    def prepare(self, texts: list[str]) -> None:
        """Write a list of texts in one ``node`` process, ahead of shaping them."""
        self.mapping.write(list(texts))

    def shape(self, text: str, *args, **kwargs):
        return self.renderer.shape(self.mapping.one(text), *args, **kwargs)

    def glyph_names(self, text: str, direction=None):
        return [self.renderer.order[g[0]] for g in self.shape(text, direction=direction).glyphs]

    def text(self, img, x, baseline, text, size, color, features=None, direction=None, script="Zyyy"):
        return self.renderer.text(img, x, baseline, self.mapping.one(text), size, color, features, direction, script)

    def width(self, text, size, features=None, direction=None):
        return self.renderer.width(self.mapping.one(text), size, features, direction)


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def wanted() -> dict[str, list[str]]:
    """Every roman text a face's fixtures or sample lines write, by face."""
    tools = ROOT / "tools"
    semaron = _load("semaron_guard", tools / "semaron-kuriale" / "guard.py")
    pirzath = _load("pirzath_guard", tools / "pirzath" / "guard.py")
    hand = _load("pirzath_hand_guard", tools / "pirzath-hand" / "guard.py")
    thuravark = _load("thuravark_guard", tools / "thuravark-carved" / "guard.py")
    qalezu = _load("qalezu_guard", tools / "qalezu-hand" / "guard.py")
    vedyakshara = _load("vedyakshara_guard", tools / "vedyakshara" / "guard.py")
    helonika = _load("helonika_guard", tools / "helonika" / "guard.py")
    lines = _load("spacing", tools / "spacing.py")
    return {
        "semaron-kuriale": semaron.fixture_texts() + lines._semaron_texts(),
        "pirzath-carved": pirzath.fixture_texts() + lines._pirzath_texts(),
        "pirzath-hand": hand.fixture_texts() + lines._pirzath_texts(),
        "thuravark-carved": thuravark.fixture_texts() + lines._thuravark_texts(),
        "qalezu-hand": qalezu.fixture_texts(),
        "vedyakshara-classical": vedyakshara.fixture_texts() + lines._vedyakshara_texts(),
        "helonika-book": helonika.fixture_texts() + lines._helonika_texts(),
        "helonika-bizarian": helonika.fixture_texts("bizarian"),
        "helonika-bethuan": helonika.fixture_texts("bethuan"),
    }


def build(thalorna: Path, notes: dict[str, Path] | None = None) -> dict:
    """The document tools/mapped.json holds, written afresh from the checkout's mapping notes,
    or, for a script ``notes`` names, from that file."""
    notes = notes or {}
    faces = {}
    for face, texts in wanted().items():
        texts = sorted(set(texts))
        m = Mapping(FACES[face], thalorna=thalorna, note=notes.get(FACES[face]), face=DRAWN_IN.get(face, face))
        faces[face] = dict(zip(texts, m.records(texts)))
    source = {face: f"{NOTES}/{script.capitalize()}_Spelling.md" for face, script in FACES.items()}
    return {"source": source, "faces": faces}


def serialise(doc: dict) -> str:
    """One text to a line, so a change reads as a diff of the texts it touches."""
    out = ["{", f'  "source": {json.dumps(doc["source"], ensure_ascii=False)},', '  "faces": {']
    faces = list(doc["faces"].items())
    for i, (face, texts) in enumerate(faces):
        out.append(f"    {json.dumps(face)}: {{")
        rows = list(texts.items())
        for j, (text, rec) in enumerate(rows):
            comma = "," if j < len(rows) - 1 else ""
            out.append(f"      {json.dumps(text, ensure_ascii=False)}: {json.dumps(rec, ensure_ascii=False)}{comma}")
        out.append("    }" + ("," if i < len(faces) - 1 else ""))
    out += ["  }", "}", ""]
    return "\n".join(out)


def stale(thalorna: Path, notes: dict[str, Path] | None = None) -> list[str]:
    """The texts tools/mapped.json records differently from the checkout's mapping notes."""
    fresh = build(thalorna, notes)
    if not CACHE.exists():
        return [f"{CACHE.relative_to(ROOT)}: error: the file is missing; run tools/mapped.py --write"]
    old = json.loads(CACHE.read_text(encoding="utf-8"))
    problems = []
    for face, texts in fresh["faces"].items():
        recorded = old.get("faces", {}).get(face, {})
        for text, rec in texts.items():
            if recorded.get(text) != rec:
                problems.append(f"tools/mapped.json: error: {face}: {text!r} is written {rec}, not {recorded.get(text)}")
        for text in recorded.keys() - texts.keys():
            problems.append(f"tools/mapped.json: error: {face}: {text!r} is recorded but no fixture or sample writes it")
    return problems


def main():
    ap = argparse.ArgumentParser(description="Write or check tools/mapped.json.")
    ap.add_argument("--thalorna", default=str(THALORNA))
    ap.add_argument("--map-note", action="append", default=[], metavar="SCRIPT=FILE",
                    help="read a script's mapping note from a file instead of git, such as vedyakshara=FILE")
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    notes = dict(n.split("=", 1) for n in args.map_note)
    if args.write:
        CACHE.write_text(serialise(build(Path(args.thalorna), notes)), encoding="utf-8")
        print(f"{CACHE.relative_to(ROOT)}: written")
        return
    problems = stale(Path(args.thalorna), notes)
    for line in problems[:40]:
        print(line)
    print(f"{CACHE.relative_to(ROOT)}: {len(problems)} problems" if problems else f"{CACHE.relative_to(ROOT)}: ok")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
