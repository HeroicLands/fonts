// Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
// SPDX-License-Identifier: OFL-1.1

/**
 * Tests `convert.mjs`: the Khelathi Zethu sign lookup, the Veldikko fixtures and the letters the
 * Veldikko has no sign for, and `fonts.json`.
 *
 *     npm test
 *
 * @module
 */

import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { test } from "node:test";
import { fileURLToPath } from "node:url";

import { convert, Unmappable, zethuSign } from "./convert.mjs";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const readJson = (...path) => JSON.parse(readFileSync(join(ROOT, ...path), "utf8"));

test("a Khelathi Zethu id is its code point", () => {
    assert.equal(zethuSign("01-002"), "\u{1EA41}");
    assert.equal(convert("Khelathi Zethu Glyphs", "01-002 01-003"), "\u{1EA41}\u{1EA42}");
});

test("an unknown or undrawn Zethu id is refused", () => {
    assert.throws(() => zethuSign("99-999"), /unknown/);
    assert.throws(() => zethuSign("01-001"), /not drawn/);
});

const VELDIKKO = "Veldikko";
const veldikko = readJson("tools", "veldikko", "encoding.json");
const veldikkoName = new Map(
    veldikko.glyphs.map((glyph) => [
        String.fromCodePoint(parseInt(glyph.codepoint.slice(2), 16)),
        glyph.glyph,
    ]),
);
const veldikkoGlyphs = (text) =>
    Array.from(text, (char) => (char === " " ? "space" : veldikkoName.get(char)));
const veldikkoFixtures = readJson("tools", "veldikko", "fixtures.json");

test("each Veldikko fixture converts to its letters and marks", () => {
    for (const { latin, glyphs } of veldikkoFixtures.fixtures) {
        assert.deepEqual(veldikkoGlyphs(convert(VELDIKKO, latin)), glyphs, latin);
    }
});

test("a character the Veldikko has no sign for is refused, naming it", () => {
    for (const { latin, letter } of veldikkoFixtures.unmappable) {
        assert.throws(
            () => convert(VELDIKKO, latin),
            (error) => error instanceof Unmappable && error.letter === letter,
            latin,
        );
    }
});

test("an unknown family is refused", () => {
    assert.throws(() => convert("Pirzath Hand", "x"), /no converter/);
});

test("fonts.json names the families of the built fonts", () => {
    const manifest = readJson("fonts.json");
    assert.equal(manifest.version, 1);
    const byName = new Map(manifest.families.map((entry) => [entry.name, entry]));
    assert.equal(byName.get("Pirzath Hand").class, "hl-pirzath-hand");
    assert.deepEqual(byName.get("Pirzath Hand").features, []);
    assert.equal(byName.has("Pirzath Hand Lifted"), false);
    assert.equal(byName.get("Qalezu Hand").direction, "rtl");
    assert.equal(byName.get("Semaron Kuriale").direction, "ltr");
    assert.equal(byName.get(VELDIKKO).direction, "rtl");
});

test("fonts.json entries have unique name keys", () => {
    const manifest = readJson("fonts.json");
    const names = manifest.families.map((entry) => entry.name);
    const uniqueNames = new Set(names);
    assert.equal(
        names.length,
        uniqueNames.size,
        `Duplicate names found: ${names.filter((name, idx) => names.indexOf(name) !== idx)}`,
    );
});

test("all entry classes have rules in fonts.css", () => {
    const manifest = readJson("fonts.json");
    const css = readFileSync(join(ROOT, "fonts.css"), "utf8");
    for (const entry of manifest.families) {
        assert(css.includes(`.${entry.class} {`), `No CSS rule found for .${entry.class}`);
    }
});
