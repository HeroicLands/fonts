# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Write every Tantsou lexicon form in Teng Chou and assert the font sets it.

    .venv/bin/python tools/teng-chou/guard.py [--font fonts/TengChou-Regular.ttf]
                                             [--thalorna ~/dev/HeroicLands/thalorna | --note FILE | --fixtures-only]

The forms come from the ``words`` list in the frontmatter of
``assets/content/Skills/Languages/Tantsou.md`` on the thalorna repository's
``origin/main``; the body of the note is never read. A form is one morpheme or a
compound written solid, and Teng Chou writes it one character per morpheme, so a
form fails when

- it cannot be cut into morphemes that each have a character;
- its characters, shaped in a horizontal run and in a vertical one, do not yield
  exactly their glyphs, one each, or a glyph draws the box.

The fixtures are the specimen passages of ``texts.py``, Tantsou and Jurthati, so
``--fixtures-only`` needs no thalorna checkout.
"""

import argparse
import subprocess
import sys
from pathlib import Path

import uharfbuzz as hb
import yaml

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))
import codepoint_order  # noqa: E402
import texts  # noqa: E402

ROOT = HERE.parent.parent
NOTE = "assets/content/Skills/Languages/Tantsou.md"
FONT = ROOT / "fonts" / "TengChou-Regular.ttf"


def table() -> dict[str, str]:
    """Glyph name -> its character."""
    return {r["glyph"]: chr(int(r["codepoint"][2:], 16)) for r in codepoint_order.ltr_table("TengChou-Regular")}


def morphemes(form: str, known: set[str]) -> list[str] | None:
    """The form cut into known morphemes, fewest first, or None."""
    form = form.lower().replace("-", "").replace(" ", "")
    best: list[list[str] | None] = [None] * (len(form) + 1)
    best[0] = []
    for i in range(len(form)):
        if best[i] is None:
            continue
        for j in range(i + 1, min(len(form), i + 6) + 1):
            piece = form[i:j]
            if piece in known and (best[j] is None or len(best[i]) + 1 < len(best[j])):
                best[j] = best[i] + [piece]
    return best[len(form)]


def lexicon_forms(thalorna: Path | None, note: Path | None) -> list[str]:
    if note:
        text = note.read_text(encoding="utf-8")
    else:
        text = subprocess.run(
            ["git", "-C", str(thalorna), "show", f"origin/main:{NOTE}"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout
    front = yaml.safe_load(text.split("\n---\n", 1)[0].lstrip("-\n"))
    forms = [w["form"] for w in front["data"]["words"]]
    if not forms:
        raise SystemExit("the words list is empty")
    return forms


def shape(font: hb.Font, text: str, direction: str) -> list[int]:
    buf = hb.Buffer()
    buf.add_str(text)
    buf.direction = direction
    buf.script = "Zyyy"
    buf.guess_segment_properties()
    hb.shape(font, buf, {})
    return [i.codepoint for i in buf.glyph_infos]


def run(path: Path, forms: list[str]) -> list[str]:
    data = path.read_bytes()
    font = hb.Font(hb.Face(data))
    from fontTools.ttLib import TTFont

    order = TTFont(str(path)).getGlyphOrder()
    chars = table()
    known = {name[3:] for name in chars if name.startswith("tc.") and not name.startswith("tc.tally")}
    failures = []
    lines = [(form, morphemes(form, known)) for form in forms]
    lines += [(" ".join(line), line) for line in texts.TANTSOU]
    lines += [(" ".join(line), line) for line in texts.JURTHATI]
    for label, parts in lines:
        if parts is None:
            failures.append(f"{label}: no cut into morphemes that each have a character")
            continue
        want = [f"js.{p[1:]}" if p.startswith("=") else f"tc.{p}" for p in parts]
        missing = [w for w in want if w not in chars]
        if missing:
            failures.append(f"{label}: no character for {', '.join(missing)}")
            continue
        text = "".join(chars[w] for w in want)
        for direction in ("ltr", "ttb"):
            got = [order[g] for g in shape(font, text, direction)]
            if got != want:
                failures.append(f"{label}: set {direction} as {got}, expected {want}")
    return failures


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--font", default=str(FONT))
    ap.add_argument("--thalorna", default=str(Path.home() / "dev" / "HeroicLands" / "thalorna"))
    ap.add_argument("--note")
    ap.add_argument("--fixtures-only", action="store_true")
    a = ap.parse_args()
    forms = [] if a.fixtures_only else lexicon_forms(Path(a.thalorna), Path(a.note) if a.note else None)
    failures = run(Path(a.font), forms)
    for f in failures:
        print(f"{a.font}: error: {f}")
    print(f"{a.font}: {len(forms)} lexicon forms and {len(texts.TANTSOU) + len(texts.JURTHATI)} passages: "
          + ("ok" if not failures else f"{len(failures)} failures"))
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
