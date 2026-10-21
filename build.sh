#!/bin/sh
# Build every font from their UFO sources into fonts/, then write fonts.css, fonts.json, keyboards/ and charts/.
# Khelathi Zethu Glyphs then takes its quadrat and cartouche layout from tools/khelathi-zethu-glyphs/layout.py.
# The timestamp is fixed, so a build is byte-for-byte reproducible. fontmake writes
# the Windows name records only, so tools/add_mac_names.py adds the Macintosh ones.
#
#     .venv/bin/... on PATH, or run:  PATH=.venv/bin:$PATH ./build.sh
set -eu
cd "$(dirname "$0")"
export SOURCE_DATE_EPOCH="${SOURCE_DATE_EPOCH:-1767225600}"

build() {
    ufo="$1"
    out="$2"
    fontmake -u "$ufo" -o ttf --keep-overlaps --no-production-names --output-path "$out"
    if [ "$ufo" = sources/KhelathiZethuGlyphs.ufo ]; then
        python tools/khelathi-zethu-glyphs/layout.py "$out"
    fi
    python tools/add_mac_names.py "$out"
    fonttools ttLib.woff2 compress -o "${out%.ttf}.woff2" "$out"
}

build sources/PirzathCarved.ufo fonts/PirzathCarved-Regular.ttf
build sources/PirzathHand.ufo fonts/PirzathHand-Regular.ttf
build sources/ThuravarkCarved.ufo fonts/ThuravarkCarved-Regular.ttf
build sources/QalezuHand.ufo fonts/QalezuHand-Regular.ttf
build sources/KhelathiZethuGlyphs.ufo fonts/KhelathiZethuGlyphs-Regular.ttf
build sources/SemaronKuriale.ufo fonts/SemaronKuriale-Regular.ttf

python tools/write_css.py
python tools/keyboards.py
python tools/charts.py
