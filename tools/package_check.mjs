// Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
// SPDX-License-Identifier: OFL-1.1

/**
 * Confirms that `npm pack` ships exactly the published font package.
 *
 *     node tools/package_check.mjs
 *
 * It runs `npm pack --dry-run --json` and fails when
 *
 * - a `files` entry in package.json packs nothing;
 * - a packed path is not a font (`fonts/*.woff2`, `fonts/*.ttf`), `fonts.css`,
 *   a code-point table (`encoding/*.json`), `LICENSE`, `README.md` or
 *   `package.json`;
 * - `fonts.css` names a URL that is not packed;
 * - a font in `fonts/` has no `@font-face` rule that names it.
 *
 * @module
 */

import { execFileSync } from "node:child_process";
import { readdirSync, readFileSync } from "node:fs";
import { dirname, join, posix } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");

/** The globs a packed path may match. */
export const ALLOWED = [
    "fonts/*.woff2",
    "fonts/*.ttf",
    "fonts.css",
    "encoding/*.json",
    "LICENSE",
    "README.md",
    "package.json",
];

/**
 * The relative URLs a stylesheet names, in `url(...)` references.
 *
 * @param {string} css - The stylesheet text.
 * @returns {string[]} Each URL as written, without quotes.
 */
export function cssUrls(css) {
    return [...css.matchAll(/url\(\s*(["']?)([^"')]+)\1\s*\)/g)].map((match) => match[2]);
}

/**
 * The findings for one package.
 *
 * @param {object} input
 * @param {string[]} input.packed - Every path `npm pack` would ship.
 * @param {string[]} input.files - The `files` entries of package.json.
 * @param {string|undefined} input.css - The text of `fonts.css`, when it exists.
 * @param {string[]} input.fontFiles - The font files in `fonts/` on disk.
 * @returns {string[]} One message per finding; empty when the package is sound.
 */
export function findings({ packed, files, css, fontFiles }) {
    const found = [];
    for (const entry of files) {
        const hit = packed.some(
            (path) => posix.matchesGlob(path, entry) || path.startsWith(`${entry}/`),
        );
        if (!hit) found.push(`package.json: files entry "${entry}" packs nothing`);
    }
    for (const path of packed) {
        if (!ALLOWED.some((glob) => posix.matchesGlob(path, glob))) {
            found.push(`${path}: packed but outside the font package`);
        }
    }
    const named = new Set();
    if (css !== undefined) {
        for (const url of cssUrls(css)) {
            const path = posix.normalize(url);
            named.add(path);
            if (!packed.includes(path)) {
                found.push(`fonts.css: names "${url}", which is not packed`);
            }
        }
    }
    for (const file of fontFiles) {
        if (!named.has(`fonts/${file}`)) {
            found.push(`fonts/${file}: no @font-face rule in fonts.css names it`);
        }
    }
    return found;
}

function main() {
    const pkg = JSON.parse(readFileSync(join(ROOT, "package.json"), "utf8"));
    const report = JSON.parse(
        execFileSync("npm", ["pack", "--dry-run", "--json"], {
            cwd: ROOT,
            encoding: "utf8",
            stdio: ["ignore", "pipe", "ignore"],
        }),
    );
    let css;
    try {
        css = readFileSync(join(ROOT, "fonts.css"), "utf8");
    } catch {
        css = undefined;
    }
    const result = findings({
        packed: report[0].files.map((file) => file.path),
        files: pkg.files,
        css,
        fontFiles: readdirSync(join(ROOT, "fonts")).filter((name) => /\.(woff2|ttf)$/.test(name)),
    });
    for (const message of result) console.error(`${message}`);
    if (result.length) process.exit(1);
    console.log(`package ok: ${report[0].files.length} files`);
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
    main();
}
