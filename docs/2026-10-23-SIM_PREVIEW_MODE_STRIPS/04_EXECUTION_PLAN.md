# 04 — Execution plan

Git is the state (`./resume-state.sh`). Items run through `plan-data/tools/execute_milestone.js`, a Workflow
executor: serial per repo, parallel across repos, honoring dependencies. Each item is implemented test-first,
committed as `<ID>: …`, independently reviewed (a `refs/notes/ka0s-review` note), and given one fix round if the
review finds problems.

| Milestone | Repos | Items | Checkpoint |
|---|---|---|---|
| M1 upstream | WowAddonStandards, LibKa0s, dev-copilot | WS-00..90, LK-00..90 (local tag v1.76.0), DC-00..01 | gates green; push branches + notes; owner updates dev-copilot to 2.5.0 (needed only for its own smoke SM-DC-*) |
| M2 re-vendor + strips + auto-run fallout | all 14 addons | `<PFX>-RV`, BL-01/10, DW-01/10, LH-01/10, MM-01 | gates green; push |
| M3 new features | QuickComms, MultiMeters, KickCD | QC-01..04, MM-10..20, KC-01..10 | gates green; push; owner smoke |
| M4 closeout | Ka0sAddonsCommonTasks (+ all, at CT-02) | CT-01, CT-02 on the owner's go-ahead | — |

Library gap found in M2/M3: an additive LibKa0s fix as an addendum item (`plan-data/addendum-NN.json/.tsv`), the
local tag moved with `git tag -f -a v1.76.0` (old/new sha recorded in 99), and affected addons re-vendor through
`<PFX>-RV2`.
