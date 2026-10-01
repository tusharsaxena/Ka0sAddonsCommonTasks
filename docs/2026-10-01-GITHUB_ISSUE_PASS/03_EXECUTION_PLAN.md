# Execution plan

Frozen once execution starts. Progress lives in git (see `RESUME.md`), and `items.tsv` is the manifest.

| M | What | Items | Runs as |
|---|---|---|---|
| M0 | Plan bundle | GI-PLAN-01 | inline |
| M1 | LibKa0s v1.66.0 → standard v2.74.0 → wow-addon | GI-LK-01…12, GI-STD-01, GI-PLUG-01 | one workflow. LibKa0s items run serially in five implement→review batches (tests peels; Slash + Widgets + RenderGrid + Tabs; Perf ×3; kit 35 + CCN; release). STD-01 starts once LK-10 is reviewed, PLUG-01 after STD-01 |
| M2 | Re-vendor + addon items | GI-<XX>-RV ×11, then 29 items | one workflow. Eleven repo pipelines in parallel, each serial inside. Every pipeline is implement → independent review → up to two `R` fix rounds. KickCD runs as three batches (peels; #9; #10 + CCN) |
| M3 | Census, record, push | GI-LK-13, GI-FIN-01 | workflow agent for the census, then inline |

## Per item

1. Read the spec rows (`02_SPEC.md`, `02a_ISSUE_DESIGNS.md`) and the repo's `CLAUDE.md`.
2. Be on `feat/2026-10-01-github-issue-pass` (create it from `master` if missing).
3. Test first (red), or record identical totals for a pure move.
4. Make the change and move the docs with it.
5. Green gate through `ka0s-bounded`.
6. Commit `<ID>: ...`.
7. Review: the note `OK <ID>`, or `<ID>R:` fixes.

## Checkpoints

- **M1 end:** LibKa0s suite totals, luacheck, the sighted complexity result, and tag `v1.66.0` present locally.
  Standard and plugin heads. A `checkpoints.tsv` row. Push the three feature branches and their notes.
- **M2 end:** per addon: suite totals, luacheck, sighted max CCN, `diff -r` vendor parity. A
  `checkpoints.tsv` row. Push all eleven feature branches and their notes.
- **M3 end:** `99_REPORT.md`, every actioned issue commented, and the bundle branch pushed. Then stop and ask
  the owner for the merge go-ahead (`/wow-addon:finalize`). At finalize: close the fixed issues, push the tag.

## Out of scope

The 74 open issues without an owner action, any addon version bump, any merge to `master`, and any in-client
smoke result (those are the owner's).
