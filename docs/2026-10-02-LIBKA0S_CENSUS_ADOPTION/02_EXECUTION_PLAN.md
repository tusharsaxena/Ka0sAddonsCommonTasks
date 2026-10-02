# Execution plan

Frozen once execution starts. Progress lives in git (see `RESUME.md`). `items.tsv` is the manifest, and
`plan-data/design-scout.json` holds each item's file:line plan.

| M | What | Items | Runs as |
|---|---|---|---|
| M0 | Plan bundle | CA-PLAN-01 | inline |
| M1 | LibKa0s v1.67.0 and standard v2.75.0 | CA-LK-01, -02, -03; CA-STD-01 | one workflow. LibKa0s runs serially (Core 10 → Options 28 / IdList 3 → release); STD-01 runs beside it. Each item is implement → independent review → up to two `R` fix rounds |
| M2 | Re-vendor, `addonName`, adoptions | 11 × RV, 11 × NM, 9 adoption items | one workflow, eleven repo pipelines in parallel, each serial inside, the same review loop |
| M3 | Census, record | CA-LK-04, CA-FIN-01 | a workflow agent for the census, then inline |

## Per item

1. Read the item's rows in `01_DESIGN.md` and its scout entry in `plan-data/design-scout.json`, and the repo's
   `CLAUDE.md`.
2. Be on `feat/2026-10-02-libka0s-census-adoption` (create it from `master` if missing).
3. Characterization test first (green on today's code), or red-first for new behaviour. A pure move records
   identical totals.
4. Make the change and move the docs with it: test inventory, README badge, smoke rows, citations.
5. Green gate through `ka0s-bounded`: the suite, `luacheck .` 0/0, vendor parity. Lizard sighted ≤ 15 at the
   milestone checkpoint.
6. Commit `<ID>: ...`, named files only.
7. Review: an independent agent adds the note `OK <ID>` (`refs/notes/ka0s-review`) or asks for `<ID>R:` fixes.

The re-vendor (RV) copies `libs/LibKa0s` and `tests/_kit` whole from tag `v1.67.0` and rolls the CLAUDE.md
provenance line in the same commit. NM is the two-token Options descriptor change plus its test (AuraMaster's
test pins the visible art path).

## Checkpoints

- **M1 end:** LibKa0s totals, luacheck, sighted complexity, tag `v1.67.0` local; standard head. A
  `checkpoints.tsv` row. Push the two feature branches and their notes.
- **M2 end:** per addon: suite totals, luacheck, sighted max CCN, vendor `diff -r` parity. A row. Push all
  eleven feature branches and their notes.
- **M3 end:** `99_REPORT.md`, each issue commented with its commits, this branch pushed. Then stop for the
  owner's smoke run and merge go-ahead. At finalize: close the nine issues and push the tag.
