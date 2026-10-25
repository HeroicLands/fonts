#!/bin/sh
# Build every font from their UFO sources into fonts/, then write fonts.css, fonts.json, keyboards/, charts/, the README samples and the specimen pages.
# Khelathi Zethu Glyphs then takes its quadrat and cartouche layout from tools/khelathi-zethu-glyphs/layout.py,
# and Thuravark Carved its crowned frame from tools/thuravark-carved/crown.py.
# Teng Chou's UFO is generated from its data by tools/teng-chou/build_ufo.py and Chalish
# Pilam Common's from its glyphs by tools/chalish-pilam/build_ufo.py, each run by hand
# after a data change, so the build compiles the committed source on every platform alike;
# Veldikko's is generated from its letters and joining by tools/veldikko/build_ufo.py,
# Vedyakshara Classical's from its signs by tools/vedyakshara/build_ufo.py, Helonika
# Book's from its letters by tools/helonika/build_ufo.py, Pirzath Hand's from its
# signs by tools/pirzath-hand/build_ufo.py, and Chalish Pilam Ceremonial's from its
# drawings and block layout by tools/chalish-pilam/build_ceremonial_ufo.py, in the same way.
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

# The fonts compile at once, each in its own process; the build fails if any of them does.
pids=""
for family in PirzathCarved PirzathHand ThuravarkCarved QalezuHand \
    KhelathiZethuGlyphs SemaronKuriale TengChou ChalishPilamCommon \
    ChalishPilamCeremonial Veldikko VedyaksharaClassical HelonikaBook; do
    build "sources/$family.ufo" "fonts/$family-Regular.ttf" &
    pids="$pids $!"
done
failed=0
for pid in $pids; do
    wait "$pid" || failed=1
done
if [ "$failed" -ne 0 ]; then
    echo "build.sh: error: a font failed to build" >&2
    exit 1
fi

python tools/write_css.py
python tools/keyboards.py
python tools/charts.py
python tools/readme_samples.py
python tools/specimen_pages.py
