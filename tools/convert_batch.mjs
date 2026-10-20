// Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
// SPDX-License-Identifier: OFL-1.1

/**
 * Converts many words in one process, for the Python guards.
 *
 *     node tools/convert_batch.mjs "Qalezu Hand" < words.json > results.json
 *
 * Reads a JSON array of strings from standard input and writes a JSON array with
 * one record per string: `{"text": "..."}`, or `{"letter": "x", "index": 0}`
 * when the string holds a character with no sign.
 *
 * @module
 */

import { readFileSync } from "node:fs";

import { convert, Unmappable } from "./qalezu-hand/convert.mjs";

const family = process.argv[2];
const words = JSON.parse(readFileSync(0, "utf8"));
const results = words.map((word) => {
    try {
        return { text: convert(family, word) };
    } catch (error) {
        if (!(error instanceof Unmappable)) throw error;
        return { letter: error.letter, index: error.index };
    }
});
process.stdout.write(JSON.stringify(results));
