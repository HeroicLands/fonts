#!/bin/sh
# Build every font from their UFO sources into fonts/.
# The timestamp is fixed, so a build is byte-for-byte reproducible.
#
#     .venv/bin/... on PATH, or run:  PATH=.venv/bin:$PATH ./build.sh
set -eu
cd "$(dirname "$0")"
export SOURCE_DATE_EPOCH="${SOURCE_DATE_EPOCH:-1767225600}"

build() {
    ufo="$1"
    out="$2"
    fontmake -u "$ufo" -o ttf --keep-overlaps --no-production-names --output-path "$out"
    fonttools ttLib.woff2 compress -o "${out%.ttf}.woff2" "$out"
}

build sources/PirzathCarved.ufo fonts/PirzathCarved-Regular.ttf
build sources/PirzathHand.ufo fonts/PirzathHand-Regular.ttf
build sources/ThuravarkRunic.ufo fonts/ThuravarkRunic-Regular.ttf
build sources/Qalezu.ufo fonts/Qalezu-Regular.ttf
build sources/KhelathiZethu.ufo fonts/KhelathiZethu-Regular.ttf
