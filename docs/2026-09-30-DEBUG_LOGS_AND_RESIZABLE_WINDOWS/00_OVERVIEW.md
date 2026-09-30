# Better debug logs and resizable debug windows (2026-09-30)

Two collection-wide items across the eleven Ka0s addons (the list is
`../WowAddonStandards/standards/ADDONS.md`), plus LibKa0s and WowAddonStandards.

- **060** Better debug logs: the log covers every important event and everything that helps diagnose a
  user's issue, without being spammy.
- **090** The debug console and every variant of it (its copy windows, the perf panel) are resizable. The
  size is kept per addon, for the session only, and the default size is today's.

## Owner decisions (2026-09-30)

| # | Question | Decision |
|---|---|---|
| D1 | 060 scope | **All eleven addons.** |
| D2 | 090 windows | **The console, every CopyWindow, and the perf panel.** Each window has its own size. |
| D3 | "Per session" | **Lost on /reload.** The size lives in Lua memory on the window; no SavedVariables. |
| D4 | 060 approach | **Standard first, then audit.** debug-logging §8 gains a diagnosis checklist and §9 a quiet-steady-state rule; each addon is audited and filled against them, with a coverage map. |
| D5 | Execution | Resumable, checkpointed plan; work on a branch, commit incrementally; push the feature branches to origin after major milestones; **no merge to master (and no pushed tag) without the owner's go-ahead**; ultracode dynamic workflows. "Push to master" in the brief is read as *push the feature branch*, since a push to master is a merge. |
| D6 | Judgment calls | The owner delegated the rest ("use your best judgement"). Calls made are recorded in `02_SPEC.md` as J-rows. |

## Standard position

- A size only a resize sets is **named non-setting state** (architecture-§5): it MAY persist and is not
  required to, so session-only complies. The standard's "What the library guarantees" (debug-logging-§1)
  states the console as **700 × 344**; that sentence changes to "700 × 344 by default, resizable, the size
  kept for the session". performance-§4's panel description changes the same way.
- debug-logging-§8 (coverage) and §9 (coalescing) exist; 060 extends them rather than adding a section.

## Files

- `02_SPEC.md` the contract for every item.
- `03_EXECUTION_PLAN.md` milestones, order, gates, pushes.
- `items.tsv` the manifest; `checkpoints.tsv` the milestone record; `RESUME.md` + `resume-state.sh` resume.
- `coverage-maps/<Addon>.md` the 060 audit per addon (M3).
- `IN_GAME_CHECKS.md` what only the client can confirm (M4); `99_REPORT.md` the execution record (M4).
