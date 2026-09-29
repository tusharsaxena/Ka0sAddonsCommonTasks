# Execution plan

Frozen once execution starts; progress lives in git (see `RESUME.md`). Branch in every touched repo:
`feat/2026-09-29-smoke-and-profile`.

## Milestones

| M | What | Items | Runs as |
|---|---|---|---|
| M0 | Plan bundle committed | SP-PLAN-01 | inline |
| M1 | LibKa0s v1.63.0 (`CliProfile`) + profile support in the four addons without it | SP-LIB-01; SP-PC-01, SP-WG-01, SP-BL-01, SP-LH-01 | one workflow, 5 repos in parallel, each item adversarially reviewed |
| M2 | Re-vendor v1.63.0 + `profile` verb in all eleven | SP-<XX>-02 ×11 | one workflow, 11 repos in parallel, reviewed |
| M3 | Smoke-test rework in all eleven + plugin citation | SP-<XX>-03 ×11; SP-PLUG-01 | one workflow per batch, reviewed against the coverage map |
| M4 | Doc sync, gates, record | SP-FIN-01 | workflow + inline |

## Order and dependencies

- SP-LIB-01 has no dependency. SP-PC/WG/BL/LH-01 have none (they do not use `CliProfile`); they run in
  parallel with SP-LIB-01.
- SP-<XX>-02 needs SP-LIB-01 (the tag) and, for PC/WG/BL/LH, that repo's -01.
- SP-<XX>-03 needs that repo's -02 (the smoke doc gains PROFILE checks and quotes the new verb count).
- SP-PLUG-01 needs SP-CM-03 and SP-KC-03 (the LOC-1 targets exist).
- SP-FIN-01 needs everything.

## Per item

1. Read `02_SPEC.md` § for the item and the repo's `CLAUDE.md`.
2. Branch (first item in the repo cuts it from `master`).
3. Implement, test first where the item adds behavior.
4. Gate green (bounded runner). Fix moved citations, regenerate test-cases/badge if the count moved.
5. Commit `<ID>: ...`.
6. Independent review: a separate agent re-reads the diff against the spec and the standard, runs the
   gate, and either signs off (git note `refs/notes/ka0s-review`, "OK <ID>") or lists defects. Defects
   are fixed as `<ID>R: ...` commits and re-reviewed.

## Checkpoints and pushes

At the end of each milestone: every touched repo clean, gate green, a row appended to
`checkpoints.tsv` (evidence: heads, test counts, luacheck), and **the feature branches pushed to
origin** (`git push -u origin feat/2026-09-29-smoke-and-profile`). The LibKa0s tag is not pushed. No
merge to any master until the owner says so; at that point the finalize procedure (merge `--no-ff`,
gate on the merge, push master, push the tag, delete branches) runs per repo, LibKa0s first.

## Stops

A red gate, a spec/standard conflict, a merge conflict, or a finding that needs an owner decision stops
that repo's chain (others continue) and is reported. Nothing is forced.
