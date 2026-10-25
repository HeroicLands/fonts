// Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
// SPDX-License-Identifier: OFL-1.1

/**
 * Converts romanized Sinale to the code points of the Veldikko.
 *
 *     import { convertVeldikko } from "./convert.mjs";
 *     convertVeldikko("nuuva");
 *
 * An internal tool of the Veldikko guard, not shipped; `convert("Veldikko",
 * text)` in `../convert.mjs` reaches it. The code points come from
 * `encoding.json` beside it. The rules:
 *
 * - a consonant is its letter, and `dh` and `ng` are one letter each; `n` before
 *   `k` is `ng`, since Sinale says _nk_ with the back nasal;
 * - a consonant written twice is its letter once with the length bar after it;
 * - the vowels after a letter are its marks: a vowel written twice is one mark
 *   with the length sign after it, and `eë` is the long _ë_, one curl with the
 *   length sign; a diphthong of the language (`ai`, `au`,
 *   `ia`, `eo`, `oi`, `ou`, `ui`, `uo`, `ei`, `ie`, `yi`, `ye`) is two marks in
 *   the order said;
 * - a vowel at the start of a word, and a vowel sounded apart from the one before
 *   it, rides on the carrier;
 * - a space or a hyphen is a word space, and a hyphen with nothing after it writes
 *   nothing; case is ignored.
 *
 * The romanization writes no pitch and no emphasis, so neither is produced. Any
 * other character is refused with an {@link Unmappable} error naming it.
 *
 * @module
 */

import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

import { Unmappable } from "../convert.mjs";

const HERE = dirname(fileURLToPath(import.meta.url));
const VOWELS = new Set(["a", "e", "i", "o", "u", "y", "ë"]);
const DIPHTHONGS = new Set([
    "ai",
    "au",
    "ia",
    "eo",
    "oi",
    "ou",
    "ui",
    "uo",
    "ei",
    "ie",
    "yi",
    "ye",
]);
const DIGRAPHS = new Set(["dh", "ng"]);
const BREAKS = new Set([" ", "\t", "\n", "-"]);

let table;

function veldikkoTable() {
    if (table) return table;
    const enc = JSON.parse(readFileSync(join(HERE, "encoding.json"), "utf8"));
    const point = (row) => String.fromCodePoint(parseInt(row.codepoint.slice(2), 16));
    const letters = new Map();
    const vowels = new Map();
    const signs = new Map();
    for (const row of enc.glyphs) {
        if (row.kind === "letter" && row.tongue === "sinale") letters.set(row.spelling, point(row));
        else if (row.kind === "vowel") vowels.set(row.vowel, point(row));
        else signs.set(row.glyph, point(row));
    }
    table = { letters, vowels, signs };
    return table;
}

/**
 * The Veldikko code points a romanized Sinale text is written with.
 *
 * @param {string} text - The romanized spelling.
 * @returns {string} The code points, in logical order.
 * @throws {Unmappable} When a character has no sign.
 */
export function convertVeldikko(text) {
    const { letters, vowels, signs } = veldikkoTable();
    const s = Array.from(text.normalize("NFC").toLowerCase());
    const out = [];
    let wordStart = true;
    let afterNucleus = false; // the last thing written was a vowel nucleus
    let i = 0;
    while (i < s.length) {
        const ch = s[i];
        if (BREAKS.has(ch)) {
            if (out.length && out[out.length - 1] !== " ") out.push(" ");
            wordStart = true;
            afterNucleus = false;
            i += 1;
            continue;
        }
        if (VOWELS.has(ch)) {
            if (wordStart || afterNucleus) out.push(letters.get(""));
            const next = s[i + 1];
            if (next === ch || (ch === "e" && next === "ë")) {
                // a doubled vowel is one mark drawn long; eë is the long ë
                const vowel = next;
                out.push(vowels.get(vowel), signs.get("long"));
                i += 2;
            } else if (next && DIPHTHONGS.has(ch + next)) {
                out.push(vowels.get(ch), vowels.get(next));
                i += 2;
            } else {
                out.push(vowels.get(ch));
                i += 1;
            }
            wordStart = false;
            afterNucleus = true;
            continue;
        }
        const two = s.slice(i, i + 2).join("");
        let spelling;
        let step;
        if (DIGRAPHS.has(two)) {
            spelling = two;
            step = 2;
        } else if (ch === "n" && s[i + 1] === "k") {
            spelling = "ng";
            step = 1;
        } else if (letters.has(ch) && ch !== "") {
            spelling = ch;
            step = 1;
        } else {
            throw new Unmappable(ch, i);
        }
        out.push(letters.get(spelling));
        i += step;
        const again = s.slice(i, i + step).join("");
        if (again === spelling) {
            out.push(signs.get("bar"));
            i += step;
        }
        wordStart = false;
        afterNucleus = false;
    }
    while (out.length && out[out.length - 1] === " ") out.pop();
    return out.join("");
}
