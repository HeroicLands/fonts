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
 *   `fonts.json`, a font cheatsheet (`charts/`), a keyboard
 *   cheatsheet, Emacs input method, or macOS, Windows or Linux layout (`keyboards/`), an
 *   encoding or its test vectors (`encodings/*.json`), `encode.py`, `LICENSE`, `README.md`
 *   or `package.json`;
 * - `fonts.css` names a URL that is not packed;
 * - a font in `fonts/` has no `@font-face` rule that names it;
 * - a family's class in `fonts.css` is missing or lacks `font-synthesis: none`, so a
 *   bold or italic run would be synthesized;
 * - `fonts.json` names a font file that is not packed, or a
 *   package export names a file that is not packed.
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
    "fonts.json",
    "charts/*.md",
    "charts/*/chart-*.svg",
    "charts/*/chart-*.png",
    "charts/*/glyphs/*.svg",
    "keyboards/*.md",
    "keyboards/sounds.json",
    "keyboards/*.svg",
    "keyboards/*.png",
    "keyboards/emacs/*.el",
    "keyboards/linux/hl_*",
    "keyboards/windows/*.klc",
    "keyboards/macos/HeroicLands.bundle/Contents/Info.plist",
    "keyboards/macos/HeroicLands.bundle/Contents/Resources/*.keylayout",
    "encodings/*.json",
    "encodings/*.md",
    "encodings/*.yaml",
    "encode.py",
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
 * @param {object|undefined} [input.manifest] - The parsed `fonts.json`, when it exists.
 * @param {Record<string, string>} [input.exports] - The `exports` map of package.json.
 * @returns {string[]} One message per finding; empty when the package is sound.
 */
export function findings({ packed, files, css, fontFiles, manifest, exports = {} }) {
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
    if (css !== undefined && manifest !== undefined) {
        for (const entry of manifest.families ?? []) {
            const rule = css.match(new RegExp(`\\.${entry.class}\\s*\\{([^}]*)\\}`));
            if (!rule) found.push(`fonts.css: no .${entry.class} rule for ${entry.name}`);
            else if (!/font-synthesis:\s*none\s*;/.test(rule[1])) {
                found.push(`fonts.css: .${entry.class} lacks font-synthesis: none`);
            }
        }
    }
    if (manifest !== undefined) {
        for (const entry of manifest.families ?? []) {
            for (const path of Object.values(entry.files ?? {})) {
                if (!packed.includes(path)) {
                    found.push(`fonts.json: ${entry.family} names "${path}", which is not packed`);
                }
            }
        }
    }
    for (const [key, target] of Object.entries(exports)) {
        if (typeof target !== "string" || /[*]/.test(target)) continue;
        const path = posix.normalize(target);
        if (!packed.includes(path))
            found.push(`package.json: export "${key}" names "${target}", which is not packed`);
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
    let manifest;
    try {
        manifest = JSON.parse(readFileSync(join(ROOT, "fonts.json"), "utf8"));
    } catch {
        manifest = undefined;
    }
    const result = findings({
        manifest,
        exports: pkg.exports,
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
