# RESUME — how to pick this run up from any point

**Git is the only state.** A crashed session, a killed workflow or a new conversation loses nothing that was committed.
It loses at most one item's uncommitted work per repo. The branch in every repo is `feat/2026-10-23-sim-preview-mode-strips`.

## 1. Where are we?

    cd /mnt/d/Profile/Users/Tushar/Documents/GIT/Ka0sAddonsCommonTasks/docs/2026-10-23-SIM_PREVIEW_MODE_STRIPS
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

Milestones run in order. Within a milestone, items run serially per repo and in parallel across repos.

1. **M1**: `python3 plan-data/tools/next_args.py M1 > <scratch>/m1.json`. Then run Workflow with
   `scriptPath: plan-data/tools/execute_milestone.js` and `args` set to that JSON. The executor creates the run
   branch in each repo on first touch.
2. **Between M1 and M2**: the local tag `v1.76.0` exists (LK-90), and the M1 checkpoint (§4) is done.
3. **M2**: `next_args.py M2` (each `<PFX>-RV` depends on LK-90 and WS-90).
4. **M3**: `next_args.py M3` (three chains: QuickComms, MultiMeters, KickCD).
5. **M4**: CT-01 by the lead. **CT-02 only on the owner's explicit merge go-ahead.**

## 4. Milestone checkpoint

1. `./resume-state.sh` shows the milestone COMPLETE and nothing "landed, review not recorded".
2. Every touched repo's gate is green on the run branch (use `/home/tushar/.claude/dev-copilot/bin/ka0s-bounded`).
3. Push the branch and notes for each touched repo: `git push -u origin feat/2026-10-23-sim-preview-mode-strips && git push origin refs/notes/ka0s-review`.
   **Never push the v1.76.0 tag before CT-02.** The lead runs pushes; workflow agents only commit locally.
4. Append a `checkpoints.tsv` row and commit it here.

## 5. A library gap (addon item returns `blocked` + `library_gap`)

Add an additive LibKa0s item `LK-91…` in `plan-data/addendum-NN.json` + `.tsv` with a test. Re-run LK-90's gates, move the local tag
(`git tag -f -a v1.76.0`), record old/new sha in `99_EXECUTION_RECORD.md`, give re-vendored addons a `<PFX>-RV2`
item, then resume.

## 6. Finalize (CT-02, owner go-ahead only)

`/dev-copilot:finalize` in order WowAddonStandards → LibKa0s (then `git push origin v1.76.0`) → dev-copilot → 14 addons →
Ka0sAddonsCommonTasks. Merge `--no-ff`, push, delete the branch locally and on origin; check `git stash list` and
`git worktree list` everywhere and remove anything this run created. Confirm MultiMeters#60 and KickCD#38 closed.
