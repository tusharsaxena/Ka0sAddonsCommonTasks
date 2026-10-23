# 2026-10-23 — Sim auto-run, QuickComms preview selector, mode strips, MultiMeters and KickCD simulators

A cross-repo run over WowAddonStandards, LibKa0s, dev-copilot and the 14 roster addons. Branch
`feat/2026-10-23-sim-preview-mode-strips` in every repo it touches.

| Read | File |
|---|---|
| The owner's request and answers (binding) | `inputs/OWNER_SCOPE.md` |
| Design notes, one per area | `inputs/design-{autorun,strips,qc-preview,mm-sim,kc-sim,upstream-note}.md` |
| The end state and the lead's decisions | `03_SPEC.md` |
| Milestones, order, checkpoints | `04_EXECUTION_PLAN.md` |
| Items (manifest / full specs) | `items.tsv` / `plan-data/items.json` |
| Smoke checks (owner-run) | `06_SMOKE_TESTS.md` |
| Picking the run up | `RESUME.md`, `./resume-state.sh` |
| What happened | `99_EXECUTION_RECORD.md` (written during execution) |

Planning: six parallel design agents (one per area) wrote the design notes and proposed items. A cross-check critic
read them all and raised 13 problems and 3 gaps. Each one is resolved in the item it names as a
`PLAN-REVIEW RESOLUTION` paragraph (`plan-data/tools/assemble.py`, `RES`). The raw output is in
`plan-data/design-workflow.json`.
