// Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
// SPDX-License-Identifier: OFL-1.1

/**
 * Converts text to the code points of a right-to-left font of this package.
 *
 *     import { convert } from "./convert.mjs";
 *     convert("Qalezu Hand", "Anlagh");
 *     convert("Khelathi Zethu Glyphs", "01-002 01-003");
 *
 * An internal tool of the Qalezu guard, not shipped. The code points come from
 * the `encoding.json` beside each font's tools.
 *
 * Qalezu Hand takes a Latin spelling and writes it by the script's rules:
 *
 * - a consonant letter is its sign, and `th`, `sh`, `kh`, `gh` and `ch` or `tj`
 *   are one sign each, `ch` and `tj` the same sign;
 * - `'` is the catch;
 * - a vowel at the start of a word, or after a space, a hyphen or other mark, is
 *   the catch, and every other vowel draws nothing;
 * - a catch whose next sign, with the silent vowels skipped, is a consonant sign
 *   or a doubled sign is written with that sign as one character, its
 *   catch-before form; any other catch (at the end of a word, before a mark,
 *   before another catch, or in a word with no consonant after it) is the
 *   standalone catch;
 * - a consonant written twice with no vowel between is that sign's doubled form,
 *   and so is a letter doubled before a digraph that begins with it (`tth`);
 * - a hyphen is a word space, and a hyphen with nothing after it writes nothing;
 * - digits, `.` and `,` are their own signs, and case is ignored.
 *
 * A letter with no sign (`c` outside `ch`, `j`, `v`, `x`, or any other character)
 * is refused with an {@link Unmappable} error naming the letter and its position.
 *
 * Khelathi Zethu Glyphs takes sign ids separated by spaces, such as `01-002`.
 *
 * @module
 */

import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const TOOLS = join(dirname(fileURLToPath(import.meta.url)), "..");

const readTable = (name) => JSON.parse(readFileSync(join(TOOLS, name, "encoding.json"), "utf8"));
const point = (codepoint) => String.fromCodePoint(parseInt(codepoint.slice(2), 16));

/** A character the script has no sign for. */
export class Unmappable extends Error {
    /**
     * @param {string} letter - The character with no sign.
     * @param {number} index - Its position in the text, in characters.
     */
    constructor(letter, index) {
        super(`${JSON.stringify(letter)} has no sign`);
        this.name = "Unmappable";
        this.letter = letter;
        this.index = index;
    }
}

const VOWELS = new Set("aeiou");
const SPACES = new Set([" ", "\t", "\n", " "]);
const BOUNDARY = new Set([..." \t\n -.,", ..."0123456789"]);
const LETTER = /^\p{L}$/u;

let qalezu;

function qalezuTable() {
    if (qalezu) return qalezu;
    const typing = new Map();
    const glyphPoint = new Map();
    const doubled = new Map();
    const catchBefore = new Map();
    for (const glyph of readTable("qalezu-hand").glyphs) {
        if (glyph.kind === "doubled") doubled.set(glyph.base, glyph.glyph);
        if (glyph.kind === "catchbefore") catchBefore.set(glyph.base, glyph.glyph);
        glyphPoint.set(glyph.glyph, point(glyph.codepoint));
        if (glyph.kind !== "doubled" && glyph.kind !== "catchbefore") {
            for (const typed of glyph.typing) typing.set(typed, glyph.glyph);
        }
    }
    const digraphs = new Set(
        [...typing.keys()].filter((typed) => typed.length === 2 && /^\p{L}+$/u.test(typed)),
    );
    qalezu = { typing, glyphPoint, doubled, catchBefore, digraphs, catchSign: typing.get("'") };
    return qalezu;
}

const SPACE = " ";
const HYPHEN = "-";

/**
 * The Qalezu Hand code points a Latin Khelathi word is written with.
 *
 * @param {string} word - The Latin spelling.
 * @returns {string} The code points, in logical order.
 * @throws {Unmappable} When a character has no sign.
 */
export function convertQalezu(word) {
    const { typing, glyphPoint, doubled, catchBefore, digraphs, catchSign } = qalezuTable();
    const s = Array.from(word.toLowerCase());
    const out = [];
    let prev = null;
    let initial = true;
    let i = 0;
    while (i < s.length) {
        const ch = s[i];
        const two = s.slice(i, i + 2).join("");
        if (VOWELS.has(ch)) {
            if (initial) out.push(catchSign);
            initial = false;
            prev = null;
            i += 1;
        } else if (ch === "'" || ch === "’") {
            out.push(catchSign);
            initial = false;
            prev = null;
            i += 1;
        } else if (BOUNDARY.has(ch)) {
            if (ch === HYPHEN) out.push(HYPHEN);
            else if (SPACES.has(ch)) out.push(SPACE);
            else out.push(typing.get(ch));
            initial = true;
            prev = null;
            i += 1;
        } else if (LETTER.test(ch)) {
            const pair = s.slice(i + 1, i + 3).join("");
            if (s.length > i + 2 && s[i + 1] === ch && digraphs.has(pair)) {
                out.push(doubled.get(typing.get(pair)));
                initial = false;
                prev = null;
                i += 3;
                continue;
            }
            let sign;
            let step;
            if (digraphs.has(two)) {
                sign = typing.get(two);
                step = 2;
            } else if (typing.has(ch)) {
                sign = typing.get(ch);
                step = 1;
            } else {
                throw new Unmappable(ch, i);
            }
            if (prev === sign) {
                out[out.length - 1] = doubled.get(sign);
                prev = null;
            } else {
                out.push(sign);
                prev = sign;
            }
            initial = false;
            i += step;
        } else {
            throw new Unmappable(ch, i);
        }
    }
    while (out.length && out[out.length - 1] === HYPHEN) out.pop();
    const spaced = out.map((glyph) => (glyph === HYPHEN ? SPACE : glyph));
    const fused = [];
    for (const glyph of spaced) {
        if (fused.length && fused[fused.length - 1] === catchSign && catchBefore.has(glyph)) {
            fused[fused.length - 1] = catchBefore.get(glyph);
        } else {
            fused.push(glyph);
        }
    }
    return fused.map((glyph) => (glyph === SPACE ? SPACE : glyphPoint.get(glyph))).join("");
}

let zethu;

/**
 * The Khelathi Zethu Glyphs code point of a sign id.
 *
 * @param {string} id - A sign id such as `01-002`.
 * @returns {string} The sign's character.
 * @throws {Error} When the id is unknown or its sign is not drawn.
 */
export function zethuSign(id) {
    zethu ??= new Map(readTable("khelathi-zethu-glyphs").signs.map((sign) => [sign.id, sign]));
    const sign = zethu.get(id);
    if (!sign) throw new Error(`the Zethu sign ${JSON.stringify(id)} is unknown`);
    if (!sign.drawn) throw new Error(`the Zethu sign ${id} is not drawn`);
    return point(sign.codepoint);
}

/**
 * The code points of a text in a family's script.
 *
 * @param {string} family - A `family` of `fonts.json` whose `input` is `convert`.
 * @param {string} text - The Latin spelling for Qalezu Hand, or sign ids
 *   separated by spaces for Khelathi Zethu Glyphs.
 * @returns {string} The code points, in logical order.
 * @throws {Error} When the family has no converter or the text cannot be converted.
 */
export function convert(family, text) {
    if (family === "Qalezu Hand") return convertQalezu(text);
    if (family === "Khelathi Zethu Glyphs") {
        return text
            .split(/\s+/)
            .filter(Boolean)
            .map((id) => zethuSign(id))
            .join("");
    }
    throw new Error(`no converter for the family ${JSON.stringify(family)}`);
}
