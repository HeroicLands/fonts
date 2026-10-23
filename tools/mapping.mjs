// Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
// SPDX-License-Identifier: OFL-1.1

/**
 * Reads thalorna's mapping notes and writes roman text in a script's code
 * points by them, for the guards and the keyboards.
 *
 *     node tools/mapping.mjs --thalorna ~/dev/HeroicLands/thalorna <script> [<face>] < words.json
 *     node tools/mapping.mjs --note Qalezu_Spelling.md <script> [<face>] < words.json
 *
 * `<script>` is `semaron`, `pirzath`, `thuravark`, `qalezu`, `veldikko`, `vedyakshara`, `helonika`, `bizarian` or `bethuan`. The mapping note is
 * `assets/content/Lore/Scripts/<Script>_Spelling.md` on the thalorna checkout's
 * `origin/main`, or the file `--note` names. Standard input is a JSON array of
 * strings; standard output is a JSON array with one record per string:
 * `{"text": "..."}`, the code points package-build's `compileMap` and `applyMap`
 * write for it, the rules a run marked `map=` is set by, and `"unmapped"`, the
 * characters no row matched and that passed through as they are, where there is
 * one. `<face>` picks a face's own rows; without it, the shared rows alone apply.
 *
 * @module
 */

import { execFileSync } from "node:child_process";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";

import { splitFrontmatter } from "@heroiclands/package-build/engine/diagnostics";
import { applyMap, compileMap } from "@heroiclands/package-build/engine/text-maps";
import YAML from "yaml";

/** The scripts with a mapping note, by the key the tools use, and their notes. */
export const SCRIPTS = [
    ["semaron", "Semaron_Spelling.md"],
    ["pirzath", "Pirzath_Spelling.md"],
    ["thuravark", "Thuravark_Spelling.md"],
    ["qalezu", "Qalezu_Spelling.md"],
    ["veldikko", "Veldikko_Spelling.md"],
    ["vedyakshara", "Vedyakshara_Spelling.md"],
    ["helonika", "Helonika_Spelling.md"],
];

/** The mapping notes the Helónika guard also reads: the same face, written by another tongue's rules. */
export const TONGUE_MAPS = [
    ["bizarian", "Bizarian_Spelling.md"],
    ["bethuan", "Bethuan_Spelling.md"],
];
export const NOTES = "assets/content/Lore/Scripts";

/**
 * A mapping note's map, its name and the faces it lists.
 *
 * @param {{thalorna?: string, note?: string}} source - The thalorna checkout,
 *   whose `origin/main` holds the note, or the note's file.
 * @param {string} file - The note's file name under {@link NOTES}.
 * @returns {{map: object, name: string, faces: Array<string|undefined>, path: string}}
 */
export function readMap({ thalorna, note }, file) {
    const path = note ?? `${NOTES}/${file}`;
    const raw =
        note ?
            readFileSync(note, "utf8")
        :   execFileSync("git", ["-C", thalorna, "show", `origin/main:${NOTES}/${file}`], {
                encoding: "utf8",
                maxBuffer: 64 * 1024 * 1024,
            });
    const split = splitFrontmatter(raw);
    if (!split) throw new Error(`${path}: no frontmatter`);
    const data = YAML.parse(split.yaml)?.data;
    const map = compileMap(data?.map);
    if (!map) throw new Error(`${path}: no data.map`);
    const faces = (data.map.fonts ?? []).map((f) => f.font);
    return { map, name: data.map.name, faces: faces.length ? faces : [undefined], path };
}

/**
 * One text written by a map.
 *
 * @param {object} map - A compiled map.
 * @param {string} text - The roman text.
 * @param {string} [face] - The face whose own rows are tried first.
 * @returns {{text: string, unmapped?: string[]}}
 */
export function write(map, text, face) {
    const { text: out, pieces } = applyMap(map, text, { font: face });
    const unmapped = pieces.filter((p) => !p.row).map((p) => p.from);
    return unmapped.length ? { text: out, unmapped } : { text: out };
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
    const args = process.argv.slice(2);
    const source = {};
    const rest = [];
    for (let i = 0; i < args.length; i++) {
        if (args[i] === "--thalorna") source.thalorna = args[++i];
        else if (args[i] === "--note") source.note = args[++i];
        else rest.push(args[i]);
    }
    const [script, face] = rest;
    const entry = [...SCRIPTS, ...TONGUE_MAPS].find(([key]) => key === script);
    if (!entry || !(source.thalorna || source.note)) {
        console.error(
            "tools/mapping.mjs: error: usage: --thalorna <path> | --note <file>, then <script> [<face>]",
        );
        process.exit(2);
    }
    const { map } = readMap(source, entry[1]);
    const words = JSON.parse(readFileSync(0, "utf8"));
    process.stdout.write(JSON.stringify(words.map((word) => write(map, word, face))));
}
