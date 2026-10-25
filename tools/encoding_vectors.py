# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Write the test vectors of every encoding, ``encodings/vectors.json``.

    python3 tools/encoding_vectors.py --write   # write the file
    python3 tools/encoding_vectors.py           # check it against the encodings

For each encoding the vectors give a text that each row applies in, then each sample
text, every one as ``{"roman", "unicode", "decoded"}``: encoding ``roman`` gives
``unicode``, and decoding ``unicode`` gives ``decoded``, which is ``roman`` again. A vector of a face's own rows also names its ``face``. Another implementation of
the encodings tests itself against them.

A row's text is the first found in which the row applies: its ``from`` alone, then
preceded by a space, each vowel or each consonant the encoding's rows begin with, then
followed by one, then both, so that a condition holds. A row no such text
applies is shadowed by another, which the guard reports.

Sample texts are the texts of ``tools/sample_texts.json`` under each face whose texts the
encoding writes, and the Khelathi Zethu scenes of ``tools/khelathi-zethu-glyphs/samples.json`` written in
their codes, a quadrat to each sign.
"""

import argparse
import json
import os
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
import encode as E  # noqa: E402

SAMPLES = os.path.join(HERE, "sample_texts.json")
ZETHU = os.path.join(HERE, "khelathi-zethu-glyphs")
# The encoding each face's texts in tools/sample_texts.json are written by.
FACE_ENCODING = {
    "semaron-kuriale": "semaron",
    "pirzath-carved": "pirzath",
    "pirzath-hand": "pirzath",
    "thuravark-carved": "thuravark",
    "qalezu-hand": "qalezu",
    "vedyakshara-classical": "vedyakshara",
    "helonika-book": "helonika",
    "helonika-bizarian": "helonika-bizarian",
    "helonika-bethuan": "helonika-bethuan",
}


_CONTEXTS = {}


def _contexts(enc):
    """The characters tried beside a row's ``from``, so that a condition holds."""
    if id(enc) in _CONTEXTS:
        return _CONTEXTS[id(enc)][1]
    consonants = sorted(
        {
            row.source[0]
            for row in enc.rows
            if unicodedata.category(row.source[0]).startswith("L")
            and row.source[0] not in enc.vowels
        }
    )
    out = ["", " "] + sorted(enc.vowels) + consonants
    _CONTEXTS[id(enc)] = (enc, out)
    return out


def witness(enc, row, face=None):
    """The first text found in which ``row`` applies, or ``None``."""
    contexts = _contexts(enc)[1:]
    tries = [("", "")] + [(c, "") for c in contexts] + [("", c) for c in contexts]
    tries += [(b, a) for b in contexts for a in contexts]
    for before, after in tries:
        text = before + row.source + after
        at = 0
        for _, _, applied in E.pieces(enc, text, face):
            if at >= len(before):
                if at == len(before) and applied is row:
                    return text
                break
            at += len(applied.source) if applied is not None else 1
    return None


def samples(enc):
    """The sample texts of an encoding, in a stable order."""
    texts = []
    if os.path.exists(SAMPLES):
        with open(SAMPLES, encoding="utf-8") as handle:
            faces = json.load(handle)["faces"]
        for face, listed in faces.items():
            if FACE_ENCODING.get(face) == enc.name:
                texts += [t for t in listed if t not in texts]
    if enc.name == "zethu-mdc":
        with open(os.path.join(ZETHU, "encoding.json"), encoding="utf-8") as handle:
            codes = {s["id"]: s["code"] for s in json.load(handle)["signs"] if s.get("drawn")}
        with open(os.path.join(ZETHU, "samples.json"), encoding="utf-8") as handle:
            scenes = json.load(handle)["scenes"]
        for scene in scenes:
            for sample in scene["samples"]:
                if all(i in codes for i in sample["ids"]):
                    text = "-".join(codes[i] for i in sample["ids"])
                    if text not in texts:
                        texts.append(text)
    return texts


def vector(enc, roman, face=None):
    unicode = E.encode(enc, roman, face)
    out = {"roman": roman, "unicode": unicode, "decoded": E.decode(enc, unicode, face)}
    if face is not None:
        out = {"face": face, **out}
    return out


def build(encodings):
    """The vectors of each encoding, by name."""
    out = {}
    for enc in encodings:
        seen = set()
        vectors = []
        lists = [(None, enc.rows)] + [(slug, f.rows) for slug, f in enc.faces.items()]
        for face, rows in lists:
            for row in rows:
                text = witness(enc, row, face)
                if text is not None and (face, text) not in seen:
                    seen.add((face, text))
                    vectors.append(vector(enc, text, face))
        for text in samples(enc):
            if (None, text) not in seen:
                seen.add((None, text))
                vectors.append(vector(enc, text))
        out[enc.name] = vectors
    return out


def dumps(vectors):
    """The vectors as their file is laid out: one vector to a line."""
    def one(value):
        return json.dumps(value, ensure_ascii=False)

    lines = ["{"]
    names = list(vectors)
    for n, name in enumerate(names):
        lines.append(f"    {one(name)}: [")
        rows = [f"        {one(v)}" for v in vectors[name]]
        lines.append(",\n".join(rows))
        lines.append("    ]" + ("," if n < len(names) - 1 else ""))
    lines.append("}")
    return "\n".join(lines) + "\n"


def vectors_path(directory):
    return os.path.join(directory, "vectors.json")


def load_all(directory=E.ENCODINGS):
    return [E.load(os.path.join(directory, f"{name}.json")) for name in _names(directory)]


def _names(directory):
    if not os.path.isdir(directory):
        return []
    return sorted(
        f[:-5]
        for f in os.listdir(directory)
        if f.endswith(".json") and f[:-5] not in E.NOT_ENCODINGS
    )


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--write", action="store_true", help="write the file rather than check it")
    parser.add_argument("--encodings", default=E.ENCODINGS, help="the directory of encodings")
    args = parser.parse_args(argv)
    path = vectors_path(args.encodings)
    try:
        text = dumps(build(load_all(args.encodings)))
    except E.EncodingError as error:
        for fault in error.faults:
            print(fault, file=sys.stderr)
        return 1
    if args.write:
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(text)
        return 0
    try:
        with open(path, encoding="utf-8") as handle:
            current = handle.read()
    except OSError:
        current = None
    if current != text:
        print(
            f"{E._shown(path)}: error: the vectors differ from the encodings; "
            "run python3 tools/encoding_vectors.py --write",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
