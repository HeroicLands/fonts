# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Write roman text in a face's code points by its encoding.

    from encoded import Encoded
    semaron = Encoded("semaron-kuriale")
    semaron.write(["zaron tholmeza"])          # the code points, one string per text

A face draws its own code points and nothing else, so a guard or a specimen that
starts from roman text writes it through the face's encoding first. ``encode.py``
refuses a character no row matches; here it is kept as it is and reported in
``unencoded``, because a guard sets such characters in the font to see the box. The encoding is
``encodings/<name>.json`` applied by ``encode.py``, for the face it serves. The
guards' ``--encoding FILE`` option names an encoding file to apply instead.
"""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import encode as E  # noqa: E402

# Each face the tools write roman text for: the encoding that writes it, and the
# face the encoding is applied for. A face drawn in another tongue's encoding names
# that encoding.
FACES = {
    "semaron-kuriale": ("semaron", "semaron-kuriale"),
    "pirzath-carved": ("pirzath", "pirzath-carved"),
    "pirzath-hand": ("pirzath", "pirzath-hand"),
    "thuravark-carved": ("thuravark", "thuravark-carved"),
    "qalezu-hand": ("qalezu", "qalezu-hand"),
    "vedyakshara-classical": ("vedyakshara", "vedyakshara-classical"),
    "helonika-book": ("helonika", "helonika-book"),
    "helonika-bizarian": ("helonika-bizarian", "helonika-book"),
    "helonika-bethuan": ("helonika-bethuan", "helonika-book"),
}


def is_ignorable(char: str) -> bool:
    """Whether a character is one of the default-ignorable marks the encoding writes."""
    return E.is_mark(char)


def visible(text: str) -> str:
    """The text without its default-ignorable characters: what the face draws."""
    return "".join(c for c in text if not is_ignorable(c))


def drawn_glyphs(renderer, text: str, direction=None, features=None):
    """``(index, gid)`` for each glyph that shaping ``text`` draws, in visual order, where
    ``index`` is the glyph's position in the full shaping.

    A glyph whose cluster starts at a default-ignorable character counts as nothing,
    whatever its name: HarfBuzz gives such a character the space glyph. A real space starts
    a cluster of its own at a visible character and stays.
    """
    shaped = renderer.shape(text, features, direction=direction)
    return [
        (i, glyph[0])
        for i, (glyph, cluster) in enumerate(zip(shaped.glyphs, shaped.clusters))
        if not is_ignorable(text[cluster])
    ]


def drawn_names(renderer, text: str, direction=None, features=None) -> list[str]:
    """The names of the glyphs ``drawn_glyphs`` finds."""
    return [renderer.order[g] for _, g in drawn_glyphs(renderer, text, direction, features)]


class Encoded:
    """The encoding of one face, applied to roman text."""

    def __init__(self, face: str, encoding=None):
        """``face`` is a key of ``FACES``; ``encoding`` is an encoding file to apply instead
        of the face's own."""
        name, self.face = FACES[face]
        self.key = face
        self.encoding = E.load(encoding or name)

    def records(self, texts: list[str]) -> list[dict]:
        """``{"text": ..., "unencoded": [...]?}`` for each text: its code points, and the
        characters no row matched, which are kept as they are, where there are any."""
        out = []
        for text in texts:
            pieces = E.pieces(self.encoding, text, self.face, strict=False)
            record = {"text": "".join(to for _, to, _ in pieces)}
            unencoded = [source for source, _, row in pieces if row is None]
            if unencoded:
                record["unencoded"] = unencoded
            out.append(record)
        return out

    def write(self, texts: list[str]) -> list[str]:
        return [r["text"] for r in self.records(texts)]

    def one(self, text: str) -> str:
        return self.write([text])[0]


class EncodedRenderer:
    """A Renderer whose text is roman, written in code points before it is shaped.

    ``shape``, ``glyph_names``, ``text`` and ``width`` take roman text; everything
    else is the wrapped Renderer's.
    """

    def __init__(self, renderer, encoded: Encoded):
        self.renderer = renderer
        self.encoded = encoded

    def __getattr__(self, name):
        return getattr(self.renderer, name)

    def shape(self, text: str, *args, **kwargs):
        return self.renderer.shape(self.encoded.one(text), *args, **kwargs)

    def glyph_names(self, text: str, direction=None):
        return drawn_names(self.renderer, self.encoded.one(text), direction)

    def text(self, img, x, baseline, text, size, color, features=None, direction=None, script="Zyyy"):
        return self.renderer.text(img, x, baseline, self.encoded.one(text), size, color, features, direction, script)

    def width(self, text, size, features=None, direction=None):
        return self.renderer.width(self.encoded.one(text), size, features, direction)
