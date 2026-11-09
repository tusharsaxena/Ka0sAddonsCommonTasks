# Execution plan

The design is `00_DESIGN.md`. The manifest is `plan-data/items.tsv`, with ids, dependencies and the design
sections each item traces to. This file says how the run goes, and it is frozen once execution starts.

## Branch and state

`feat/2026-11-10-quickcomms-forever-emotes` in QuickComms, LibKa0s, LibKa0sSkinTester, WowAddonStandards and
Ka0sAddonsCommonTasks. Each branch is checked out in the main repo folder, because the game loads those folders.
**Git is the only state**: an item is done when a commit on that branch has a subject starting `<ID>: `.
`plan-data/resume-state.sh` prints progress, and `plan-data/exceptions.tsv` holds items done without a commit
(QFE-ISS: the issues), each with a proof command.

## Baseline (2026-11-10, master, before any change)

QuickComms vendors LibKa0s v1.93.0. LibKa0s is at v1.94.0. Skin Tester is already Retail · Forever. Recorded by
the first item in each repo, via the bounded runner (both kit profiles where the repo has them, plus luacheck).

## Milestones

| M | Items | Checkpoint (before the push) |
|---|---|---|
| M0 | QFE-REC, QFE-ISS | Bundle committed; 3 issues exist |
| M1 | QFE-LK1, QFE-LK2 | LibKa0s suite green on both profiles, luacheck 0/0; tag v1.95.0 **local only**; branch pushed |
| M2 | QFE-ST1, QFE-ST2 | Skin Tester green on both profiles, luacheck 0/0; branch pushed |
| M3 | QFE-F1..F5 | QuickComms green on both profiles, luacheck 0/0, 1500-line cap; branch pushed |
| M4 | QFE-E1..E3 | as M3; branch pushed |
| M5 | QFE-DOCS, QFE-REV, QFE-STD | Review findings fixed or recorded; standard branch green; all branches pushed |
| M6 | QFE-SMOKE | The owner's smoke on Retail and Forever; then finalize on the owner's go-ahead |

Each milestone that passes goes on a row in `checkpoints.tsv`, with its test totals and the pushed heads.

## Rules for every item

- Follow the owning repo's `CLAUDE.md` (its gate, its commit rules, its standards). Never edit `libs/` or
  `tests/_kit/` in an addon; re-vendor instead.
- Write the test first where behavior changes, then the change. Commit only on a green gate, with the subject
  `<ID>: <what>` and the session's trailers.
- Edits keep each file's line endings (some repos are CRLF, checked by an eol test).
- No version bumps. No pushed tags. No merges.
- If an item turns up something that is not minimal, or contradicts the design, it stops and reports.

## Orchestration

A Workflow runs M1 to M5. LibKa0s goes first, and QuickComms waits for v1.95.0. Skin Tester runs beside them. In
QuickComms, F3 and F4 touch the same files, so the QuickComms items run one after another. Each item skips itself
when its commit already exists, so a rerun resumes. Pushes, GitHub writes and anything on master are the lead's,
not the agents' (subagent-push-refused).
