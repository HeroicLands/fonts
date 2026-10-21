// Copyright (c) 2026 Tom Rodriguez ("Toasty") — <toasty@heroiclands.org>
// SPDX-License-Identifier: OFL-1.1

import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";

import { findings } from "./package_check.mjs";

const css = readFileSync(new URL("../fonts.css", import.meta.url), "utf8");
const manifest = JSON.parse(readFileSync(new URL("../fonts.json", import.meta.url), "utf8"));
const check = (text) =>
    findings({ packed: [], files: [], css: text, fontFiles: [], manifest, exports: {} }).filter(
        (message) => message.includes("font-synthesis") || message.includes("rule for"),
    );

test("every family's class turns font synthesis off", () => {
    assert.deepEqual(check(css), []);
});

test("a family that loses font-synthesis: none is a finding", () => {
    const altered = css.replace("    font-synthesis: none;\n", "");
    assert.equal(check(altered).length, 1);
});

test("a family without a class rule is a finding", () => {
    const altered = css.replace(/\.hl-qalezu-hand \{[^}]*\}/, "");
    assert.equal(check(altered).length, 1);
});
