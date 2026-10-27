# Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
# SPDX-License-Identifier: OFL-1.1
"""Conformance of the self-contained published encoding contract."""
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest import mock
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import encode as E

class PublishedEncodings(unittest.TestCase):

    def test_every_published_encoding_is_independent(self):
        vectors = json.loads((ROOT / 'encodings/vectors.json').read_text())
        self.assertTrue(vectors)
        for name in E.names():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / (name + '.json')
                shutil.copyfile(ROOT / 'encodings' / (name + '.json'), path)
                data = json.loads(path.read_text())
                self.assertNotIn('extends', data)
                self.assertNotIn('codage', data)
                self.assertIsInstance(data['codes'], list)
                self.assertFalse(any(('\\U' in r[1] for r in data['codes'] if isinstance(r, list))))
                enc = E.load(path)
                with mock.patch('builtins.open', side_effect=AssertionError('external read')):
                    output = E.encode(enc, '⟦U+00E1⟧')
                    self.assertEqual(E.decode(enc, output), '⟦U+00E1⟧')

    def test_whitespace_class(self):
        enc = E.load('qalezu')
        for char in E.WHITESPACE:
            self.assertEqual(E.encode(enc, 'a' + char + 'b'), E.encode(enc, 'a b'))
        for char in ['\x85', '\u2028', '\u2029']:
            with self.assertRaises(E.EncodingError):
                E.encode(enc, 'a' + char + 'b')

    def test_unicode_forms_in_every_encoding(self):
        for name in E.names():
            enc = E.load(name)
            for code in ['U+0000', 'U+00E1', 'U+10FFFF', 'U+E0112', 'U+E0113', 'U+E0115', 'U+E015B']:
                with self.subTest(name=name, code=code):
                    value = E.encode(enc, '⟦' + code + '⟧')
                    self.assertEqual(E.encode(enc, E.decode(enc, value)), value)
            for code in ['U+110000', 'U+D800', 'U+00e1', 'U+123', 'LATIN_SMALL_LETTER_A_WITH_ACUTE']:
                with self.subTest(name=name, code=code):
                    with self.assertRaises(E.EncodingError) as caught:
                        E.encode(enc, '⟦' + code + '⟧')
                    self.assertEqual((caught.exception.line, caught.exception.column), (1, 2))

    def test_literal_escape_preserves_reserved_payloads_and_named_codes(self):
        for name in E.names():
            enc = E.load(name)
            escape = enc.controls['literalEscape']
            for text in ['⟦U+E0112 U+E0113 U+E0115 U+E015B⟧', '⟦U+E015B U+E0112 U+E015D⟧', '⟦U+E015B U+E0113 U+E0115 U+E0112 U+E0115 U+E0113⟧']:
                output = E.encode(enc, text)
                self.assertEqual(E.encode(enc, E.decode(enc, output)), output)
            reserved = {escape, E.mark(E.OPEN), E.mark(E.CLOSE)}
            code = next((row.source for row in enc.codage.rows
                         if any(char in reserved for char in row.target)), None)
            if code:
                text = '⟦' + code + '⟧'
                self.assertEqual(E.decode(enc, E.encode(enc, text)), text)
            for broken, column in [(E.mark(E.OPEN) + escape + 'a' + E.mark(E.CLOSE), 2), (E.mark(E.OPEN) + escape, 2)]:
                with self.assertRaises(E.EncodingError) as caught:
                    E.decode(enc, broken)
                self.assertEqual((caught.exception.line, caught.exception.column), (1, column))

    def test_references_are_refused_at_their_key(self):
        for key, value in [('extends', 'missing'), ('codage', 'missing')]:
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / 'bad.json'
                path.write_text(json.dumps({'name': 'bad', 'fonts': ['face'], 'accepts': ['a'], 'separator': ' ', 'rows': [['a', 'A']], key: value}, indent=4))
                with self.assertRaises(E.EncodingError) as caught:
                    E.load(path)
                self.assertIn(key, caught.exception.message)
                self.assertIsNotNone(caught.exception.line)
if __name__ == '__main__':
    unittest.main()
