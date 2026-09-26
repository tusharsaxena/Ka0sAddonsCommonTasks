# Resuming the diagnostics rollout

The plan (`03_EXECUTION_PLAN.md`) is frozen; this file records how execution actually runs from M3 on,
so a fresh session can pick it up at any point.

## Where it stands (2026-09-26)

- M0, M1, M2 done and merged to master with the owner's go-ahead: WowAddonStandards v2.68.0, wow-addon,
  LibKa0s v1.60.0 (tag pushed, `bed0eb1`).
- Every addon's `-01` (the v1.60.0 re-vendor) is done, merged to master and pushed, with the owner's
  go-ahead. Those feature branches were deleted after the merge.
- Remaining: the rest of M3 (`-02`..`-06`) and M4 (`-07` per addon, then DR-REC-01), 53 addon items.

## State lives in git

- An item is done when a commit whose subject starts `<ID>: ` (or `<ID> + ...:`, or `<ID>R: ` for a
  review fix) exists on the addon's branch or its master. Nothing else is state.
- Each addon works on a fresh `feat/2026-09-25-diagnostics-rollout`, cut from that addon's current
  master (which already carries its `-01`). If the branch exists locally with commits, continue it.
- Items run in the order `items.tsv` lists them, one at a time per repo. Addons are independent and run
  in parallel.
- Reviews are `refs/notes/ka0s-review` notes on the item's commit.

## Checkpoints and pushes

- Per addon, after its last M3 item: full green gate, clean tree, push the feature branch and the
  review notes (M3 checkpoint). After its `-07`: the same again (M4 checkpoint).
- The owner's rule: push feature branches at milestones, **never merge to master without the owner's
  go-ahead**. No version bumps, no tags.
- DR-REC-01 writes `99_REPORT.md` and appends the M3/M4 rows to `checkpoints.tsv` on `main`.

## Relaunching

- The run is a Workflow script under the session's `workflows/scripts/` (`diag-rollout-m3-m4-*.js`).
  Relaunch it with its `scriptPath` and `resumeFromRunId`: finished agents replay from cache, and every
  implementer first checks git for its item's commit and skips a done item, so a relaunch from scratch
  is also safe.
- A dirty tree in an addon is that item's partial work: continue it, never discard it.
- A red gate stops that addon's chain; the other addons carry on. Fix, then relaunch.

## Relaunch of 2026-09-26 (session 643b5f13)

- M3 stood at 23/55, M4 at 1/13. Seven addons carried interrupted `-03` work in a dirty tree (no process
  running on them): LootHistory, PartyFrameEnhanced, WhatGroup, PanelMaster, KickCD, AbsorbTracker,
  ConsumableMaster.
- The same script, copied with two constants changed (the scratchpad path and the commit trailer's model
  name): `/tmp/claude-1000/-mnt-d-Profile-Users-Tushar-Documents-GIT-Ka0sAddonsCommonTasks/643b5f13-aec3-4d93-a0b4-136f6ee6954c/scratchpad/diag-rollout-m3-m4-resume.js`,
  run `wf_e01f1bcc-33f`. Resume it in that session with that `scriptPath` and `resumeFromRunId`; from any
  other session, relaunch it from scratch (every implementer skips an item git already records).
