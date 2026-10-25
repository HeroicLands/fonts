// Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
// SPDX-License-Identifier: OFL-1.1

/**
 * Converts text to the code points of a right-to-left font of this package:
 * sign ids for Khelathi Zethu Glyphs, romanized Sinale for Veldikko.
 *
 *     import { convert } from "./convert.mjs";
 *     convert("Khelathi Zethu Glyphs", "01-002 01-003");
 *     convert("Veldikko", "nuuva");
 *
 * An internal tool of the guards and specimens, not shipped. The code points
 * come from the `encoding.json` beside each font's tools.
 *
 * Khelathi Zethu Glyphs takes sign ids separated by spaces, such as `01-002`.
 *
 * Veldikko takes romanized Sinale, by the rules of `./veldikko/convert.mjs`.
 *
 * A character with no sign is refused with an {@link Unmappable} error naming
 * it and its position.
 *
 * @module
 */

import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

import { convertVeldikko } from "./veldikko/convert.mjs";

const TOOLS = dirname(fileURLToPath(import.meta.url));

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
 * @param {string} text - Sign ids separated by spaces for Khelathi Zethu
 *   Glyphs, or romanized Sinale for Veldikko.
 * @returns {string} The code points, in logical order.
 * @throws {Error} When the family has no converter or the text cannot be converted.
 */
export function convert(family, text) {
    if (family === "Veldikko") return convertVeldikko(text);
    if (family === "Khelathi Zethu Glyphs") {
        return text
            .split(/\s+/)
            .filter(Boolean)
            .map((id) => zethuSign(id))
            .join("");
    }
    throw new Error(`no converter for the family ${JSON.stringify(family)}`);
}
