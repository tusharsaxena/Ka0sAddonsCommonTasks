# RESUME — how to pick this plan up from any point

**Git is the only state.** A crashed session, a killed workflow or a new conversation loses nothing that was
committed, and at most one item per repo of uncommitted work. Branch in every repo:
`feat/2026-10-07-review-audit-remediation`.

## 1. Where are we?

    ./resume-state.sh        # per-milestone counts, RESUME list, unreviewed items, dirty trees, branch check
    ./resume-state.sh -v     # plus every remaining id

- An item is **done** when a commit whose subject starts `<ID>: ` exists in its repo (the remediation branch
  or the default branch). A commit may carry several ids: `LK-01 + LK-02: …`.
- An item is **closed** when one of its commits carries a `refs/notes/ka0s-review` note, written by its
  independent review. "Landed, review not recorded" means the review has to run again; the executor does
  that on its own.
- `checkpoints.tsv` is the milestone log. Its last line is the last milestone that passed its checkpoint and
  was pushed.
- Items that legitimately land with no commit go in `exceptions.tsv`, with a command proving the claim.

## 2. Before resuming, clean up an interrupted item

Items run one at a time per repo, so a repo's dirty tree is a single interrupted item.

    for r in WowAddonStandards LibKa0s dev-copilot AbsorbTracker AuraMaster BankLedger ConsumableMaster \
             KickCD LootHistory MultiMeters PanelMaster PartyFrameEnhanced PrettyChat WhatGroup; do
      echo "== $r $(git -C ../../../$r branch --show-current)"; git -C ../../../$r status --short; done

You can leave it: the implementer detects a dirty tree, continues it if it is that item's partial work, and
otherwise stashes it (`git stash list` names it). Never `reset --hard` or `checkout .` work you have not read.

## 3. Relaunch

1. Pick the milestone from `./resume-state.sh`. Milestones run in order: **M1** (upstream: WowAddonStandards,
   LibKa0s, dev-copilot) → **M2** (re-vendor LibKa0s v1.71.0 into the 11 addons; starts once LibKa0s's release
   item has landed and the local tag exists) → **M3** (addon items, serial within a repo, parallel across repos).
2. Build the arguments (only items not yet landed; landed dependencies are dropped):

       python3 plan-data/tools/next_args.py M1 > /tmp/claude-1000/args.json          # explicit deps

   Use the explicit-deps form for **every** milestone, M3 included: `--order` drops cross-repo dependencies,
   and M3 has one (PC-06 waits for LootHistory's LH-01). The scheduler still runs one item per repo at a time.
   **Exclude DC-14** (deleting dev-copilot's stale `origin/main`): it is outward-facing and irreversible, so it
   runs only on the owner's go-ahead. Filter it out of the args before launching.

3. Run the Workflow tool with `scriptPath` = `plan-data/tools/execute_milestone.js` (absolute path) and `args` =
   the JSON above (as an object, not a string). The script is idempotent: an item already landed and reviewed is
   skipped; one landed but unreviewed is reviewed.
4. If the launching session is alive, `Workflow({scriptPath, resumeFromRunId})` replays finished agents from
   cache. The git-based relaunch in step 3 works from any session.

Finished runs' results are saved to `plan-data/runs/`.

## 4. Milestone checkpoint

1. `./resume-state.sh <M>` reports the milestone COMPLETE, no unreviewed items, no dirty trees.
2. Every repo the milestone touched has a green gate, run through
   `/home/tushar/.claude/dev-copilot/bin/ka0s-bounded`: `luacheck .` (0/0), `lua tests/run.lua` (or the repo's
   own runner), `lizard -l lua -x "./libs/*" -x "./tests/_kit/*" .` (no function above CCN 15), and the
   1500-line cap. dev-copilot and WowAddonStandards run their own CLAUDE.md gates.
3. M1 only: `git -C ../../../LibKa0s tag -l v1.71.0` exists **locally**, on the release item's commit.
4. Push each touched repo's feature branch to origin, plus `refs/notes/ka0s-review`
   (`git push origin refs/notes/ka0s-review`). **Never** merge, and **never** push the `v1.71.0` tag, without the
   owner's go-ahead.
5. Append a line to `checkpoints.tsv` (date, checkpoint, evidence: test totals and pushed heads) and commit it
   in Ka0sAddonsCommonTasks.

## 5. What only the owner can do

- Approve the merge (`/dev-copilot:finalize`, dependency order: WowAddonStandards, LibKa0s, dev-copilot, the
  addons, this repo) and the push of the LibKa0s `v1.71.0` tag.
- Run the in-client checks in `06_SMOKE_TESTS.md` and record the results.
- Bump addon versions and cut releases. Neither is part of this plan.

After the merge: delete every `feat/2026-10-07-review-audit-remediation` branch (local and origin), and any
stash or worktree this run created.
