# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Resolve encoding sources into independent published JSON files.

    python3 tools/publish_encodings.py [--check]

Only this generator reads source references. Readers of encodings/ need one file.
"""
import argparse
import json
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import encode as E
SOURCES = ROOT / 'tools/encodings'
OUT = ROOT / 'encodings'

def build():
    families = json.loads((ROOT / 'fonts.json').read_text())['families']
    by_slug = {f['class'][3:]: f for f in families}
    out = {}
    for path in sorted(SOURCES.glob('*.json')):
        data = json.loads(path.read_text())
        if data.get('kind') == 'codage' or 'fonts' not in data:
            continue
        base = None
        if 'extends' in data:
            base_path = SOURCES / (data['extends'] + '.json')
            base = E.Base(json.loads(base_path.read_text()), str(base_path))
        codage = None
        if 'codage' in data:
            codage_path = SOURCES / (data['codage'] + '.json')
            codes = json.loads(codage_path.read_text())
            codage = E.Encoding(codes, str(codage_path))
        enc = E.Encoding(data, str(path), base, codage)
        published = {k: v for k, v in data.items() if k not in ('extends', 'codage')}
        published['controls'] = enc.controls
        published['accepts'] = list(data['accepts']) + sorted((enc.standard_chars | {' '}) - E.accepted(data['accepts']))
        published['rows'] = [r.as_json() for r in enc.rows] + [[' ', enc.separator]]
        if codage:
            published['codes'] = [r.as_json() for r in codage.rows]
        else:
            seen = set()
            rows = []
            for slug in data['fonts']:
                for point in by_slug[slug]['codepoints']:
                    name = point['name'].replace(' ', '_')
                    char = chr(int(point['codepoint'][2:], 16))
                    if name not in seen:
                        rows.append([name, char])
                        seen.add(name)
            published['codes'] = rows
        out[path.name] = E.dumps(published)
    return out

def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    failures = []
    for name, text in build().items():
        path = OUT / name
        if path.exists() and path.read_text() == text:
            continue
        if args.check:
            failures.append(f'{path}: error: differs from resolved source; run tools/publish_encodings.py')
        else:
            path.write_text(text)
    for failure in failures:
        print(failure, file=sys.stderr)
    return bool(failures)
if __name__ == '__main__':
    sys.exit(main())
