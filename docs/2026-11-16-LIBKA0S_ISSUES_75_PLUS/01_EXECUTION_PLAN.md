# Execution plan

The manifest is `plan-data/items.tsv` and the design is `00_DESIGN.md`. Git is the only state: an item is done when a
commit whose subject starts `<ID>: ` exists on `feat/2026-11-16-libka0s-75-plus` in its repo (`plan-data/resume-state.sh`).
Items that land without a commit go in `plan-data/exceptions.tsv`, each with a command that proves the claim.

## Rules for every item

- Work on the run branch in the item's repo. Create the branch from the repo's **detected** default branch, which is
  `main` for CombatTrail and SkillMaster. Follow that repo's `CLAUDE.md`.
- **TDD.** A red test comes first for every behavior change. Peels change no behavior and keep the suite green.
- **Gate after every commit** (LibKa0s):
  - `~/.claude/dev-copilot/bin/ka0s-bounded lua tests/run.lua` passes, with no test skipped that was not skipped before.
  - `~/.claude/dev-copilot/bin/ka0s-bounded luacheck .` reports 0 warnings and 0 errors.
  - Every file is 1500 lines or fewer, and every size trigger is respected.
  - `diff -r testkit tests/_kit` is empty when the kit moved.
- **Bump each file's LibStub minor once per release.** Later items in the same file reuse the bump: check
  `git diff master -- <file>` for a bump already on the branch.
- **Independent review.** Each LibKa0s item gets a fresh reviewer agent that never saw the implementation. It
  reads the design section and the diff, and records a verdict as a `refs/notes/ka0s-review` note on the item's
  commit. Findings are fixed in a follow-up commit `<ID>: review fixes`.
- **No pushes, tags or GitHub writes from agents.** The lead does every push, every GitHub write and the local tag.

## Milestones

| M | Items | Where | How |
|---|---|---|---|
| M0 | REC-00, ISS-00 | CommonTasks, GitHub | The lead does them directly. |
| M1 | LK-P1, LK-P2, LK-P3 | LibKa0s | Sequential, by one agent. |
| M2 | LK-75, LK-78, LK-82 | LibKa0s | Sequential, each with a review. |
| M3 | LK-79, LK-90 | LibKa0s | Sequential, with one console review across both. |
| M4 | LK-92A, LK-92B | LibKa0s | Sequential. First re-read DropWatcher's merged `RowTooltip.lua` on `master` as prior art. |
| M5 | LK-86, LK-81 | LibKa0s | Sequential. |
| M6 | LK-80, LK-87 | LibKa0s | Sequential. |
| M7 | LK-REL, then STD-01, STD-02 and DC-78 in parallel | LibKa0s, WowAddonStandards, dev-copilot | The lead cuts the local tag `v1.105.0` after LK-REL's gate. |
| **CP-A** | | | **Checkpoint A:** the full LibKa0s gate plus the release battery (four suites, 0 over CCN 15). Push the run branches of LibKa0s, WowAddonStandards and dev-copilot (**not the tag**). Add a row to `checkpoints.tsv`. |
| M8 | RV-* for 18 addons in parallel, then RV-DW, then ST-82 | each addon | One agent per addon (§Re-vendor). |
| **CP-B** | | | **Checkpoint B:** re-run every addon's gate from the lead. Push every addon's run branch and CommonTasks. Add a row to `checkpoints.tsv`. Write `07_EXECUTION_RECORD.md`. |
| M9 | owner smoke, then finalize on the owner's go-ahead | all | `06_SMOKE_TESTS.md`, then `RESUME.md` step 5. |

## Re-vendor procedure (each RV-* item)

1. Create the run branch from the default branch.
   - **DropWatcher:** if its checkout is not on its default branch with a clean tree, use
     `git -C ../DropWatcher worktree add ../.worktrees/DropWatcher-75plus -b feat/2026-11-16-libka0s-75-plus master`.
     Never touch the other session's branch or its tree.
2. Follow the installed `/dev-copilot:wow-revendor-libka0s` (2.10.0) **copy and bundle half** from the local
   v1.105.0 tag:
   - Copy both payloads whole.
   - Roll the provenance line.
   - Run the icon and sound prune with the tag's `tools/prune-icons.lua`.
   - Write the delta report and the `docs/revendor/2026-11-16-v1.105.0/` bundle (and the span bundle where one is
     owed).

   **Skip the adoption interview and every issue filing.** List the adoption candidates in the bundle as owed in
   phase [3], with their issue numbers.
3. Run the gate. Fix what goes red, using design §5's list of expected fixes. Diagnose anything else before
   changing it. Never weaken or skip a test.
   - If the cause is in the library, stop that addon and report it to the lead, who fixes LibKa0s
     (`LK-FIX-<n>: ...`), re-cuts the local tag and re-copies.
4. Commit once: `RV-<ABBR>: Re-vendor LibKa0s v1.105.0 (kit 57): <fixes>`. Include the trailers.
5. Return the gate totals: tests run, failed, skipped per profile, and luacheck.

## Recovery

See `RESUME.md`. Never `reset --hard` or `checkout .` work you have not read.
