// Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
// SPDX-License-Identifier: OFL-1.1

/**
 * Tests `convert.mjs`: the Qalezu fixtures, the letters Qalezu has no sign for,
 * the Khelathi Zethu sign lookup and `fonts.json`.
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

import { convert, Unmappable, zethuSign } from "./qalezu-hand/convert.mjs";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const readJson = (...path) => JSON.parse(readFileSync(join(ROOT, ...path), "utf8"));

const QALEZU = "Qalezu Hand";
const encoding = readJson("tools", "qalezu-hand", "encoding.json");
const nameOf = new Map(
    encoding.glyphs.map((glyph) => [
        String.fromCodePoint(parseInt(glyph.codepoint.slice(2), 16)),
        glyph.glyph,
    ]),
);
const glyphsOf = (text) => Array.from(text, (char) => (char === " " ? "space" : nameOf.get(char)));

const { fixtures, unmappable } = readJson("tools", "qalezu-hand", "fixtures.json");

test("each Qalezu fixture converts to its signs", () => {
    for (const { latin, signs } of fixtures) {
        assert.deepEqual(glyphsOf(convert(QALEZU, latin)), signs, latin);
    }
});

test("a letter with no sign is refused, naming the letter", () => {
    for (const { latin, letter } of unmappable) {
        assert.throws(
            () => convert(QALEZU, latin),
            (error) => error instanceof Unmappable && error.letter === letter,
            latin,
        );
    }
});

test("a Khelathi Zethu id is its code point", () => {
    assert.equal(zethuSign("01-002"), "\u{1EA41}");
    assert.equal(convert("Khelathi Zethu Glyphs", "01-002 01-003"), "\u{1EA41}\u{1EA42}");
});

test("an unknown or undrawn Zethu id is refused", () => {
    assert.throws(() => zethuSign("99-999"), /unknown/);
    assert.throws(() => zethuSign("01-001"), /not drawn/);
});

test("an unknown family is refused", () => {
    assert.throws(() => convert("Pirzath Hand", "x"), /no converter/);
});

test("fonts.json names the families of the built fonts", () => {
    const manifest = readJson("fonts.json");
    assert.equal(manifest.version, 1);
    const byName = new Map(manifest.families.map((entry) => [entry.name, entry]));
    assert.equal(byName.get("Pirzath Hand").class, "hl-pirzath-hand");
    assert.deepEqual(byName.get("Pirzath Hand").features, ["ss01"]);
    assert.equal(byName.get("Pirzath Hand Lifted").class, "hl-pirzath-hand-lifted");
    assert.deepEqual(byName.get("Pirzath Hand Lifted").features, []);
    assert.equal(byName.get(QALEZU).direction, "rtl");
    assert.equal(byName.get("Semaron Kuriale").direction, "ltr");
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
