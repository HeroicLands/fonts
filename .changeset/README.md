# Changesets

Every pull request that changes what a user of the fonts meets declares its
intended version bump here, as a file, before it merges. That declaration is the
whole release process: merging it to `main` opens a **Version Packages** pull
request, and merging _that_ versions the package, rewrites `CHANGELOG.md`, tags
the commit, cuts the GitHub Release, and publishes to npm. Nothing is run by hand.

## Adding one

```bash
npx changeset              # pick major / minor / patch, write the summary
npx changeset add --empty  # this change ships nothing a user can see
```

Nothing requires one: a pull request that changes no font, no stylesheet and no
code-point table carries no changeset at all.

## Which bump

Read the bump from the point of view of someone who installs the package.

| Bump      | What it means here                                                                                         |
| --------- | ---------------------------------------------------------------------------------------------------------- |
| **major** | Only on the owner's direct instruction.                                                                    |
| **minor** | A change every user of a font meets: a glyph drawn differently, a font added or removed, a family renamed. |
| **patch** | Everything else, including a new glyph nobody meets without looking for it.                                |

## Writing the summary

The summary becomes the `CHANGELOG.md` entry and the GitHub Release body, so write
it for someone deciding whether to upgrade: what changed for them, not what the
patch touched. One to six one-sentence bullets, symptom rather than mechanism, no
verification, no commit hashes or issue and pull-request numbers. Do not use `#`
headings inside a summary: it is wrapped into a list item, so a heading breaks the
document outline.

`package-build changelog check` lints a pending changeset against these rules
before it merges.
