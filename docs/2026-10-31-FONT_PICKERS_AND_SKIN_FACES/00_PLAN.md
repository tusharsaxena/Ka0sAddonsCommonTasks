# Plan: font pickers and skin faces (LibKa0s v1.83.0, standard v2.94.0)

The owner's batch is `inputs/OWNER_FEEDBACK.md`; calls taken are `DECISIONS.md`; the manifest is `items.tsv`; `./resume-state.sh` reads progress from git; `RESUME.md` restarts a crashed run.

| # | Owner item | Items |
|---|---|---|
| 1 | Preview pickers, standard, every addon | LK-F03, WS-F01, every XX-F02, ST-F01 |
| 2 | DpsRace headers and HUD tooltips | DR-F03, DR-F04 |
| 3 | Obsidian title, new faces, normalization, licensing | LK-F01, LK-F02, LK-F06, every XX-F01 |
| 4 | Skin's default | LK-F04 |
| 5 | Outline default | LK-F05, every XX-F01 |

## Milestones

- **M0.** This bundle.
- **M1, library and standard.** LK-F items in order with one writer and an independent review and fix round, then LK-F90: release battery and a LOCAL tag v1.83.0. WS-F01 alongside; ST-F01 after. Checkpoint: gates green, branches and notes pushed, tag not pushed.
- **M2, addons.** 15 in parallel, one agent per repo, XX-F01 first, each reviewed. Checkpoint as M1.
- **M3, report.** `99_REPORT.md` and `06_SMOKE_TESTS.md`, then stop for the owner.
- **M4, finalize on the go-ahead only.** The 2026-10-30 run and this one land together per RESUME §6.

## Rules

Main checkout (the game loads `GIT/<Addon>`), one repo one writer. Subjects start `<ID>: `, session trailers. Agents never push, merge or tag a remote; the lead pushes. Gate through `~/.claude/dev-copilot/bin/ka0s-bounded`: `lua tests/run.lua`, `luacheck .` 0/0, 1500-line cap, CCN 15. Never edit `libs/` or `tests/_kit/` except by re-vendoring the tag. Tests first where behavior changes. No smoke check is marked passed by the run.
