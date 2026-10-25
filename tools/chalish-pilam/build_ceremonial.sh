#!/bin/sh
# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
# Build Chalish Pilam Ceremonial: its UFO from the drawing modules, then the TrueType and WOFF2 fonts.
#
#     PATH=.venv/bin:$PATH tools/chalish-pilam/build_ceremonial.sh
set -eu
cd "$(dirname "$0")/../.."

case "$(python -c 'import sys; print("%d.%d" % sys.version_info[:2])')" in
    3.15)
        echo "build_ceremonial.sh: error: Python 3.15 corrupts font drawing; build in a Python 3.13 virtual environment" >&2
        exit 1
        ;;
esac
export SOURCE_DATE_EPOCH="${SOURCE_DATE_EPOCH:-1767225600}"

ufo=sources/ChalishPilamCeremonial.ufo
out=fonts/ChalishPilamCeremonial-Regular.ttf
python tools/chalish-pilam/build_ceremonial_ufo.py --out "$ufo"
fontmake -u "$ufo" -o ttf --keep-overlaps --no-production-names --output-path "$out"
python tools/add_mac_names.py "$out"
fonttools ttLib.woff2 compress -o "${out%.ttf}.woff2" "$out"
