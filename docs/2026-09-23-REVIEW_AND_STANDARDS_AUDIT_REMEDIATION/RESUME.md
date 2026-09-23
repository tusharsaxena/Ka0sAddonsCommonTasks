# RESUME — how to pick this plan up from any point

This plan is long: 384 items across 14 repos, run as multi-hour workflows. It is built so that **git is the
only state**. A crashed session, a killed workflow or a new conversation loses nothing that was committed,
and at most one item per repo of uncommitted work.

## 1. Where are we?

    ./resume-state.sh        # per-milestone counts, RESUME list, unreviewed items, dirty trees, branch check
    ./resume-state.sh -v     # plus every remaining id

- An item is **done** when a commit whose subject starts `<ID>: ` exists in its repo (the remediation branch
  or the default branch). A commit may carry several ids: `LK-01 + LK-02: …`.
- An item is **closed** when one of its commits carries a `refs/notes/ka0s-review` note, written by its
  independent review. "Landed, review not recorded" means the review has to run again. The executor does
  that on its own.
- `checkpoints.tsv` is the milestone log. Its last line is the last milestone that passed its checkpoint and
  was pushed.

## 2. Before resuming, clean up an interrupted item

Items run one at a time per repo, so a repo's dirty tree is a single interrupted item.

    for r in WowAddonStandards LibKa0s wow-addon AbsorbTracker AuraMaster BankLedger ConsumableMaster \
             KickCD LootHistory MultiMeters PanelMaster PartyFrameEnhanced PrettyChat WhatGroup; do
      echo "== $r $(git -C ../../../$r branch --show-current)"; git -C ../../../$r status --short; done

You can leave it: the executor's implementer detects a dirty tree, continues it if it is that item's partial
work, and otherwise stashes it (`git stash list` names it). Never `reset --hard` or `checkout .` work you
have not read.

## 3. Relaunch

1. Pick the milestone from `./resume-state.sh`. Milestones run in order M1 → M2 → M3, and M2 starts only
   once M1 has passed its checkpoint (§4). M4 waits for the owner to merge WowAddonStandards.
2. Build the arguments. They hold only the items that have not landed, and dependencies that have already
   landed are dropped:

       python3 plan-data/tools/next_args.py M3 > /tmp/args.json      # optionally --repo X --repo Y

3. Run the Workflow tool with the script body of `plan-data/tools/execute_milestone.js`, passed inline, and
   `args` = the JSON above (as an object, not a string). The script is idempotent: an item that has already
   landed and been reviewed is skipped, and one that has landed but is unreviewed is reviewed.
4. If the session that launched a run is still alive, `Workflow({scriptPath, resumeFromRunId})` replays
   the run's finished agents from cache. The git-based relaunch in step 3 works from any session.

Runs so far are recorded in `plan-data/runs/` (the results JSON of each finished workflow).

## 4. Milestone checkpoint (after M1, after M2, after each addon's M3 items, after M4)

1. `./resume-state.sh <M>` reports the milestone COMPLETE, with no unreviewed items and no dirty trees.
2. In every repo the milestone touched, the full battery is green, run through the bounded runner:
   `/home/tushar/.claude/wow-addon/bin/ka0s-bounded luacheck .`, `… lua5.1 tests/run.lua`, `… lizard` (CCN ≤ 15),
   and the 1500-line cap. The one sanctioned exception: reds listed in an RV commit body may carry from M2
   into M3.
3. M1 only: `git -C ../../../LibKa0s tag -l v1.56.0` exists **locally**, on LK-33's commit.
4. Push each touched repo's `feat/2026-09-23-review-audit-remediation` to origin, together with
   `refs/notes/ka0s-review` (`git push origin refs/notes/ka0s-review`). **Never** merge, and **never** push
   the `v1.56.0` tag, without the owner's go-ahead.
5. Append a line to `checkpoints.tsv`: date, checkpoint, evidence (the test totals and the pushed heads).
   Commit it in Ka0sAddonsCommonTasks.

## 5. What only the owner can do

- Merge any remediation branch into master/main.
- Push the `v1.56.0` tag, which happens with the LibKa0s merge.
- Merge WowAddonStandards, which unblocks M4.
- Run the in-client sessions in `06_SMOKE_TESTS.md`.
- Bump addon versions and cut releases. Neither is in this plan.
