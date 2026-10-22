// Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
// SPDX-License-Identifier: OFL-1.1

/**
 * Writes `keyboards/sounds.json`: what each sound of `tools/sound_keys.json` is in
 * each script that has a keyboard layout.
 *
 *     node tools/sounds.mjs --thalorna ~/dev/HeroicLands/thalorna          # print
 *     node tools/sounds.mjs --thalorna ~/dev/HeroicLands/thalorna --write  # write the file
 *     node tools/sounds.mjs --thalorna ~/dev/HeroicLands/thalorna --map-note vedyakshara=FILE
 *
 * A sound's output is its spelling run through the script's mapping note,
 * `assets/content/Lore/Scripts/<Script>_Spelling.md` on the thalorna checkout's
 * `origin/main`, or the file `--map-note <script>=<file>` names for a script, by
 * package-build's own `compileMap` and `applyMap`, the rules a
 * run marked `map=` is set by. A sound with a `context` is mapped inside it
 * (`context: ["t", "t"]` maps `tat` for `a`), and its output is the pieces that
 * lie within the sound; a piece that runs across the sound's edge is an error. A
 * script whose mapping needs another context for a sound names it in the sound's
 * `contexts`, keyed by script.
 *
 * A sound is unmapped in a script, and its key types nothing there, when a
 * character of it passes through the mapping unchanged (`"no row"`) or when the
 * mapping writes it as nothing (`"writes nothing"`). Every face a mapping lists
 * must give the same output.
 *
 * @module
 */

import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

import { applyMap } from "@heroiclands/package-build/engine/text-maps";

import { NOTES, readMap, SCRIPTS } from "./mapping.mjs";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const OUT = join(ROOT, "keyboards", "sounds.json");

export { SCRIPTS };

const hex = (text) =>
    Array.from(text, (c) => `U+${c.codePointAt(0).toString(16).toUpperCase().padStart(4, "0")}`);

/** `{codepoints}` or `{unmapped}` for one sound under one face. */
function spell(map, face, sound, script) {
    const [before, after] = sound.contexts?.[script] ?? sound.context ?? ["", ""];
    const start = before.length;
    const end = start + sound.spelling.length;
    const { pieces } = applyMap(map, before + sound.spelling + after, { font: face });
    const within = pieces.filter((p) => p.at < end && p.at + p.from.length > start);
    for (const p of within)
        if (p.at < start || p.at + p.from.length > end)
            throw new Error(
                `${sound.sound}: the row ${JSON.stringify(p.from)} runs across the edge of the sound in ${JSON.stringify(before + sound.spelling + after)}`,
            );
    if (within.some((p) => !p.row)) return { unmapped: "no row" };
    const to = within.map((p) => p.to).join("");
    if (!to) return { unmapped: "writes nothing" };
    return { codepoints: hex(to).join(" ") };
}

/**
 * The `sounds.json` document.
 *
 * @param {string} thalorna - The thalorna checkout, whose `origin/main` holds the notes.
 * @param {Record<string, string>} [notes] - A file to read a script's note from instead, by script.
 * @returns {object} The document.
 */
export function build(thalorna, notes = {}) {
    const keys = JSON.parse(readFileSync(join(ROOT, "tools", "sound_keys.json"), "utf8"));
    const maps = Object.fromEntries(
        SCRIPTS.map(([script, file]) => [
            script,
            { file, ...readMap({ thalorna, note: notes[script] }, file) },
        ]),
    );
    const sounds = keys.sounds.map((sound) => {
        const scripts = {};
        for (const [script, { map, faces }] of Object.entries(maps)) {
            const each = faces.map((face) => spell(map, face, sound, script));
            const first = JSON.stringify(each[0]);
            if (each.some((e) => JSON.stringify(e) !== first))
                throw new Error(`${sound.sound}: the faces of ${script} disagree`);
            scripts[script] = each[0];
        }
        return { sound: sound.sound, spelling: sound.spelling, scripts };
    });
    return {
        source: Object.fromEntries(
            Object.entries(maps).map(([script, m]) => [
                script,
                { map: m.name, note: `${NOTES}/${m.file}`, faces: m.faces },
            ]),
        ),
        sounds,
    };
}

/** The document as written to disk: one sound per line. */
export const serialise = (doc) => {
    const lines = ["{", `  "source": ${JSON.stringify(doc.source)},`, '  "sounds": ['];
    doc.sounds.forEach((s, i) =>
        lines.push(`    ${JSON.stringify(s)}${i < doc.sounds.length - 1 ? "," : ""}`),
    );
    lines.push("  ]", "}", "");
    return lines.join("\n");
};

if (process.argv[1] === fileURLToPath(import.meta.url)) {
    const args = process.argv.slice(2);
    const at = args.indexOf("--thalorna");
    if (at < 0 || !args[at + 1]) {
        console.error("tools/sounds.mjs: error: --thalorna <path> is required");
        process.exit(2);
    }
    const notes = {};
    args.forEach((a, i) => {
        if (a === "--map-note") {
            const [script, file] = args[i + 1].split("=");
            notes[script] = file;
        }
    });
    const text = serialise(build(args[at + 1], notes));
    if (args.includes("--write")) writeFileSync(OUT, text);
    else process.stdout.write(text);
}
