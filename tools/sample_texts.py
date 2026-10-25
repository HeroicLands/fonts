# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""The roman texts the guards' fixtures and the specimens' sample lines write, ``tools/sample_texts.json``.

    .venv/bin/python tools/sample_texts.py --write   # write the file
    .venv/bin/python tools/sample_texts.py           # check it

The file lists, for each face, every roman text its fixtures and sample lines write
through the face's encoding. ``tools/encoding_vectors.py`` takes them as the sample
texts of the encodings, and the check finds a fixture the file does not list, and a
text it lists that no fixture writes.
"""

import argparse
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILE = ROOT / "tools" / "sample_texts.json"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def wanted() -> dict[str, list[str]]:
    """Every roman text a face's fixtures or sample lines write, by face."""
    tools = ROOT / "tools"
    sys.path.insert(0, str(tools))
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


def build() -> dict:
    return {"faces": {face: sorted(set(texts)) for face, texts in wanted().items()}}


def serialise(doc: dict) -> str:
    """One text to a line, so a change reads as a diff of the texts it touches."""
    out = ["{", '  "faces": {']
    faces = list(doc["faces"].items())
    for i, (face, texts) in enumerate(faces):
        out.append(f"    {json.dumps(face)}: [")
        for j, text in enumerate(texts):
            out.append(f"      {json.dumps(text, ensure_ascii=False)}" + ("," if j < len(texts) - 1 else ""))
        out.append("    ]" + ("," if i < len(faces) - 1 else ""))
    out += ["  }", "}", ""]
    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    text = serialise(build())
    name = FILE.relative_to(ROOT)
    if args.write:
        FILE.write_text(text, encoding="utf-8")
        print(f"{name}: written")
        return
    if not FILE.exists() or FILE.read_text(encoding="utf-8") != text:
        print(f"{name}: error: the file differs from the texts the fixtures and sample lines write; run tools/sample_texts.py --write")
        sys.exit(1)
    print(f"{name}: ok")


if __name__ == "__main__":
    main()
