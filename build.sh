#!/bin/sh
# Build every font from their UFO sources into fonts/, then write fonts.css, fonts.json, keyboards/, charts/ and the README samples.
# Khelathi Zethu Glyphs then takes its quadrat and cartouche layout from tools/khelathi-zethu-glyphs/layout.py,
# and Thuravark Carved its crowned frame from tools/thuravark-carved/crown.py.
# Teng Chou's UFO is generated from its data by tools/teng-chou/build_ufo.py, run by hand
# after a data change, so the build compiles the committed source on every platform alike;
# Veldikko's is generated from its letters and joining by tools/veldikko/build_ufo.py,
# Vedyakshara Classical's from its signs by tools/vedyakshara/build_ufo.py, and Helonika
# Book's from its letters by tools/helonika/build_ufo.py, in the
# same way.
# The timestamp is fixed, so a build is byte-for-byte reproducible. fontmake writes
# the Windows name records only, so tools/add_mac_names.py adds the Macintosh ones.
#
#     .venv/bin/... on PATH, or run:  PATH=.venv/bin:$PATH ./build.sh
set -eu
cd "$(dirname "$0")"

# Python 3.15 corrupts long drawing runs, so a build refuses it. The toolchain runs on 3.13.
case "$(python -c 'import sys; print("%d.%d" % sys.version_info[:2])')" in
    3.15)
        echo "build.sh: error: Python 3.15 corrupts font drawing; build in a Python 3.13 virtual environment" >&2
        exit 1
        ;;
esac
export SOURCE_DATE_EPOCH="${SOURCE_DATE_EPOCH:-1767225600}"

build() {
    ufo="$1"
    out="$2"
    fontmake -u "$ufo" -o ttf --keep-overlaps --no-production-names --output-path "$out"
    if [ "$ufo" = sources/KhelathiZethuGlyphs.ufo ]; then
        python tools/khelathi-zethu-glyphs/layout.py "$out"
    fi
    if [ "$ufo" = sources/ThuravarkCarved.ufo ]; then
        python tools/thuravark-carved/crown.py "$out"
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
build sources/TengChou.ufo fonts/TengChou-Regular.ttf
build sources/Veldikko.ufo fonts/Veldikko-Regular.ttf
build sources/VedyaksharaClassical.ufo fonts/VedyaksharaClassical-Regular.ttf
build sources/HelonikaBook.ufo fonts/HelonikaBook-Regular.ttf

python tools/write_css.py
python tools/keyboards.py
python tools/charts.py
python tools/readme_samples.py
