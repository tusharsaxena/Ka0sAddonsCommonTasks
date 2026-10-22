# RESUME — how to pick this run up from any point

**Git is the only state.** A crashed session, a killed workflow or a new conversation loses nothing that was committed.
It loses at most one item's uncommitted work per repo. The branch in every repo is `feat/2026-10-22-libka0s-issues-45-58`.

## 1. Where are we?

    cd /mnt/d/Profile/Users/Tushar/Documents/GIT/Ka0sAddonsCommonTasks/docs/2026-10-22-LIBKA0S_ISSUES_45_58
    ./resume-state.sh        # per-milestone counts, RESUME list, unreviewed items, tag, plugin version, dirty trees, branch check
    ./resume-state.sh -v     # plus every remaining id

- An item is **done** when a commit whose subject starts `<ID>: ` exists in its repo, among the run branch's commits on top of
  that repo's default branch. PGFE's default branch is `main`, and the scripts detect it. A commit may carry several ids:
  `LK-01 + LK-02: …`. Items whose spec says "TWO commits" (DW-02, LH-10) or "(1/2)" (LK-22) land as more than one commit.
  The implementer continues from where the last one stopped.
- An item is **closed** when one of its commits carries a `refs/notes/ka0s-review` note, which its independent review writes.
- `checkpoints.tsv` is the milestone log, and `exceptions.tsv` holds items that land with no commit, each with a proof command.
- `99_EXECUTION_RECORD.md` (written during execution) records LK-11's outcome, every local-tag move and the deviations.

## 2. Clean up an interrupted item

Items run one at a time per repo, so a dirty tree is one interrupted item. You can leave it: the implementer continues it if it is
that item's work and otherwise stashes it under a named message. **Never** `reset --hard` or `checkout .` work you have not read.

    for r in WowAddonStandards LibKa0s dev-copilot AbsorbTracker AuraMaster BankLedger ConsumableMaster DropWatcher KickCD \
             LootHistory MultiMeters PanelMaster PartyFrameEnhanced PremadeGroupsFilterExtension PrettyChat QuickComms WhatGroup; do
      echo "== $r $(git -C ../../../$r branch --show-current)"; git -C ../../../$r status --short; done

## 3. Relaunch

Milestones run in order. Within a milestone, items run serially per repo and in parallel across repos, with
cross-repo dependencies honoured by the scheduler.

1. **M1** (WowAddonStandards, LibKa0s, dev-copilot):

       python3 plan-data/tools/next_args.py M1 > /tmp/claude-1000/m1.json

   Run the Workflow tool with `scriptPath: plan-data/tools/execute_milestone.js` and `args` set to that JSON. The executor
   creates the run branch in each repo from its default branch on first touch.
2. **Between M1 and M2:**
   - Confirm LK-11's outcome is recorded.
   - Confirm the local tag `v1.75.0` exists.
   - Run the M1 checkpoint (§4).
   - The **owner updates and reloads dev-copilot to 2.4.0** (`resume-state.sh` prints the installed version).
3. **M2:** `next_args.py M2`. Each addon's RV item depends on LK-22, WS-11 and DC-04.
4. **M3:** `next_args.py M3 --order > args.json` (a soft serial chain per repo; each implementer checks its real `depends_on` in git).
   Run DropWatcher's DW-01..05 first, or at least let them finish before LH-10 and BL-08 start. The scheduler's deps enforce this.
5. **M4:** run CT-01, then wait. **CT-02 runs only on the owner's explicit merge go-ahead.** The GitHub closure items run after
   it, spaced out.

## 4. Milestone checkpoint

At the end of each milestone:

1. `./resume-state.sh` shows the milestone COMPLETE and nothing "landed, review not recorded".
2. Every touched repo's gate is green on the run branch (its CLAUDE.md names it; use `/home/tushar/.claude/dev-copilot/bin/ka0s-bounded`).
3. Push the feature branch and the review notes for every repo the milestone touched:
   `git push -u origin feat/2026-10-22-libka0s-issues-45-58 && git push origin refs/notes/ka0s-review`.
   **Never push the v1.75.0 tag before CT-02.**
4. Append a row to `checkpoints.tsv` (date, milestone, evidence: test totals and pushed heads) and commit it here.

## 5. A library gap found in M3 (OWNER_SCOPE B)

When an addon item returns `blocked` with `library_gap`:

1. Add an additive LibKa0s fix as a new item `LK-26`, `LK-27`, … (append it to `plan-data/items.json` via an addendum file, not by
   editing the frozen plan), with a test.
2. Re-run LK-22's gate. Move the local tag with `git tag -f -a v1.75.0`, and record the old and new sha in `99_EXECUTION_RECORD.md`.
3. Give each addon that already re-vendored a refresh item `<PFX>-RV2` (the same copy-and-prune from the moved tag), then resume the
   blocked item.

## 6. Finalize (CT-02, on the owner's go-ahead only)

`/dev-copilot:finalize` in dependency order: WowAddonStandards → LibKa0s (then `git push origin v1.75.0`) → dev-copilot →
the 14 addons → Ka0sAddonsCommonTasks. Merge `--no-ff`, push, and delete the branch locally and on origin. Then, in every repo,
check `git stash list` and `git worktree list` and remove anything this run created. Record it all, then run the M4 GitHub items.

## 7. State at CT-01 (2026-10-23)

- M1 38/38, M2 14/14 and M3 78/78 have landed, the M3 count including the 19 items of addenda 01-03. M4 has LK-23
  and CT-01; WS-12, LK-24, the addon closure items and CT-02 remain.
- LibKa0s v1.75.0 is a **local** tag at `9e5c4e2`, its final position. Every roster addon vendors that payload.
- The owner's merge go-ahead for this plan is recorded in `99_EXECUTION_RECORD.md`, so CT-02 follows without a stop.
  Pushing the v1.75.0 tag is part of CT-02.
- The M3 checkpoint (push the M3 heads and notes, add the `checkpoints.tsv` row) is run by the lead.
- Every smoke check in `06_SMOKE_TESTS.md` is still `owed`.
