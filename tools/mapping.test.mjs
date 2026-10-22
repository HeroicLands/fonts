// Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
// SPDX-License-Identifier: OFL-1.1

/**
 * Tests `mapping.mjs`: a text written by a map, and the characters no row writes.
 *
 *     npm test
 *
 * @module
 */

import assert from "node:assert/strict";
import { test } from "node:test";

import { compileMap } from "@heroiclands/package-build/engine/text-maps";

import { SCRIPTS, write } from "./mapping.mjs";

const map = compileMap({
    name: "test",
    vowels: "ai",
    rows: [
        ["a", "\u{F0000}"],
        ["th", "\u{F0020}"],
        { from: "y", to: "\u{F0017}", before: "vowel" },
        ["y", "\u{F0002}"],
    ],
    fonts: [{ font: "pirzath-carved" }],
});

test("a text is written by the rows, longest first and by condition", () => {
    assert.deepEqual(write(map, "tha"), { text: "\u{F0020}\u{F0000}" });
    assert.deepEqual(write(map, "ya"), { text: "\u{F0017}\u{F0000}" });
    assert.deepEqual(write(map, "y"), { text: "\u{F0002}" });
});

test("a character no row writes passes through and is named", () => {
    assert.deepEqual(write(map, "ac"), { text: "\u{F0000}c", unmapped: ["c"] });
});

test("every script with a keyboard layout has a mapping note", () => {
    assert.deepEqual(
        SCRIPTS.map(([script]) => script),
        ["semaron", "pirzath", "thuravark", "qalezu", "veldikko", "vedyakshara", "helonika"],
    );
});
