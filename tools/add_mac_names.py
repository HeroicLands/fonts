# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Give a built font the Macintosh copy of its name records.

    .venv/bin/python tools/add_mac_names.py font.ttf [font.ttf ...]

fontmake writes the name table for the Windows platform (3, 1, 0x409) alone. Font
lists on macOS, and applications that read the Macintosh platform, find a font by
the records of platform (1, 0, 0), so each name ID that the Windows platform holds
is copied there. Running it twice changes nothing. tools/font_names.py checks the
result.
"""

import sys
from pathlib import Path

from fontTools.ttLib import TTFont

# The IDs a font list reads: copyright, family, subfamily, unique ID, full name,
# version, PostScript name, description, licence and licence URL, and the
# typographic family and subfamily.
COPIED = (0, 1, 2, 3, 4, 5, 6, 10, 13, 14, 16, 17)


def add(path: Path):
    font = TTFont(str(path), recalcTimestamp=False)
    table = font["name"]
    windows = {n.nameID: n.toUnicode() for n in table.names if (n.platformID, n.platEncID, n.langID) == (3, 1, 0x409)}
    for nid in COPIED:
        if nid in windows:
            table.setName(windows[nid], nid, 1, 0, 0)
    font.save(str(path))


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        add(Path(arg))
