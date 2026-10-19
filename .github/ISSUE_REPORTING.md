# Issue Reporting — heroiclands-fonts

This document defines how issues are created and classified in the
**`heroiclands-fonts`** repository, which ships the fonts for the scripts of the
HeroicLands settings, their specimens and the build that makes them.

**This repository is its own tracker.** File font, specimen and build work here,
not in the system or setting repositories. See §7 for where a given piece of work
belongs.

The core discipline is simple — three axes, each answering a different question:

- **Type** — _"what shape of work is this?"_ One per issue, from a closed set of five.
- **Priority** — _"how soon and how badly does this need doing?"_ A GitHub issue field, one value, defaults to Medium.
- **Labels** — _"what is this about?"_ Categorization only, chosen **only** from the organization set in §3. Never invent a label.

Type and priority are structured single values (one each). Labels stack. Keep the
roles separate: do not encode priority or work-shape as a label, and do not encode
subject matter as a type.

**There are no milestones here.** An empty milestone set is better than a
decorative one.

## 1. Issue types

Exactly **one** type per issue. Do not leave an issue untyped.

Issue types are **organization-level** in the `HeroicLands` org, so the same five
types — and their definitions — are shared with every other repository in the
project. They are not redefined here.

| Type        | Use it when…                                                                                                                        | Do **not** use it for…                                                 |
| ----------- | ----------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| **bug**     | A shipped font is wrong — a glyph is drawn badly, a ligature or mark does not form, spacing or kerning is off, the build or check fails. | A missing letter or script (a _feature_); a chore.                     |
| **feature** | A new capability, such as a font for another script or a new specimen, deliverable as one shippable unit.                           | Anything broken (_bug_); work needing many sub-issues (_epic_).        |
| **epic**    | A body of work that only makes sense decomposed into sub-issues.                                                                    | Anything shippable as a single issue. No sub-issues means not an epic. |
| **task**    | Necessary work that is neither defect nor new capability: chores, refactors, CI, docs, releases.                                    | Exploratory work with an uncertain outcome (_spike_).                  |
| **spike**   | A **timeboxed** investigation whose deliverable is a decision or recommendation — not shipped fonts.                                | Work whose steps are already known (a _task_).                         |

**Type rules**

- **MUST** assign exactly one type.
- A **bug** is _broken_; a **feature** is _missing_. Decide which word fits first.
- An **epic** MUST link its sub-issues and SHOULD carry little implementation
  detail of its own.
- A **spike** MUST state the question it answers and its timebox.
- A **refactor** changing no external behaviour is a **task**, tagged `flag/tech-debt`.

**What "broken" means here.** A font fails in a particular text, so the most
valuable bug reports give **the exact text** (the spelling as typed, not a
screenshot alone), **where it was shown** (browser and version, a PDF, Foundry),
and **what the letters should have been**. A word that renders without error but
in the wrong letters is a bug worth filing even though nothing failed.

## 2. Priority (GitHub issue field)

Priority is a native **Priority** field on the issue — an organization-level issue
field, **not** a label. Set it in the issue sidebar; the issue list filters on it
(`field.priority:high,medium`). One value per issue, from: **Urgent · High ·
Medium · Low**.

| Priority   | Means                                                                       |
| ---------- | --------------------------------------------------------------------------- |
| **Urgent** | A shipped font is unusable, or the build cannot produce one. Drop other work. |
| **High**   | A common letter or word renders wrongly, with no reasonable workaround.     |
| **Medium** | The default. Worth doing; nothing is on fire.                               |
| **Low**    | Nice to have; polish, or a rare edge.                                       |

## 3. Labels — organization-level

Labels are defined once for the whole organization, in `labels.yml` of
`HeroicLands/.github`. This repository keeps no registry of its own and never
creates a label here; a gap in the set is raised in `HeroicLands/.github`.

| Group         | Labels                                                                                     |
| ------------- | ------------------------------------------------------------------------------------------ |
| `type/`       | `type/bug`, `type/feature`, `type/epic`, `type/task`, `type/spike` (exactly one per issue) |
| `area/`       | `area/documentation`, `area/devops`, `area/tests`, `area/content`, `area/system`, `area/site`, `area/layout`, `area/styling` |
| `flag/`       | `flag/breaking-change`, `flag/security`, `flag/regression`, `flag/tech-debt`               |
| `status/`     | `status/blocked`, `status/question`                                                        |
| `resolution/` | `resolution/duplicate`, `resolution/wontfix`                                               |
| `ci/`         | `ci/e2e`                                                                                   |

**When to use them in this repository**

- `area/documentation` — the README, the design document, process.
- `area/devops` — build, tooling, CI, release, repository configuration.
- `area/content` — the letters, ligatures, marks and specimens themselves.
- `flag/tech-debt` — restructuring or cleanup of working code; refactors.
- `flag/regression` — something that worked and stopped; pairs with type **bug**.
- `flag/breaking-change` — alters a font's file name, family name, code points or the mapping from spelling to letters.
- `status/blocked` — cannot proceed until an external dependency or another issue clears.
- `resolution/duplicate`, `resolution/wontfix`, `status/question` — as their names say.

There is **no** `bug` or `enhancement` label — work shape is a _type_, so
filtering on such a label returns nothing. System and site areas do not apply to
a font repository.

## 4. Body structure by type

### Bug

```text
## Summary
## Text and where it was shown
## Expected vs. actual
## Environment      (font file and commit, browser or application and version, OS)
## Notes
```

### Feature

```text
## Problem / motivation
## Proposed solution
## Acceptance criteria
```

### Task

```text
## What needs doing
## Why
## Acceptance criteria
```

### Spike

```text
## Question
## Timebox
## What a conclusion looks like
```

**Root cause goes in a comment, not the body.** The body is the problem
statement — symptoms, reproduction, expectation. What is actually wrong, and the
proposed fix, belong in a comment, so the issue reads as a report rather than as a
half-finished diagnosis.

## 5. Pull requests

- Branch as `<type>/<issue_#>_<short-kebab-summary>`, or `chore/<slug>` for
  issue-free housekeeping.
- `main` is protected: pull request, one approving review, **squash merge only**.
- The PR description says what changed and why; it becomes the squash commit
  message.
- **No AI or assistant attribution** in a commit message, PR title, or PR body.
  The `.githooks/commit-msg` hook refuses such a commit locally (activate with
  `git config core.hooksPath .githooks`), and the **No Attribution** check fails
  the pull request.

## 6. Verification

"Done" is what the build and its checks assert:

- `python src/build.py` — builds the fonts into `fonts/`
- `python src/check_font.py` — checks the built font
- `python src/guard.py` — shapes every lexicon form against a local thalorna checkout

A change to a font commits the rebuilt files in `fonts/` with it, and a change to
the design updates `DESIGN.md`.

## 7. Which repository does an issue belong in?

File where the diff will land, not where the symptom shows.

| The change is to…                                                                  | File it in                         |
| ---------------------------------------------------------------------------------- | ---------------------------------- |
| A glyph, ligature, mark, kerning, a specimen, the build or its checks               | **here**                           |
| A script's letter inventory, its canon, or the text of a note                      | `HeroicLands/thalorna`             |
| The shared build, the Hugo theme or the way a site loads a font                     | `HeroicLands/package-build`        |
| System code, sheets, rules automation                                              | `Song-of-Heroic-Lands-FoundryVTT`  |

A letter drawn wrongly is **here**; a letter that is missing from the script, or
a word spelled wrongly, is thalorna.

Exploitable weaknesses are reported privately as a security advisory, never as a
public issue.
