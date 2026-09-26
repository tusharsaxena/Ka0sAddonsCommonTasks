# Resuming the automated-tests sweep

`01_EXECUTION_PLAN.md` is frozen once execution starts. This file tells a fresh session how to find
where the run stands and how to pick it up.

## State lives in git

- **An item is done when a commit whose subject starts `<ID>: ` exists in the repo that `items.tsv`
  names**, on `feat/2026-09-26-automated-tests-sweep` or on the repo's default branch. A subject of
  `<ID> + <ID>: ...` counts for both ids. `<ID>R: ` is a review fix on an item that is already done.
- An M1 or M2 item is **closed** when its commit carries a `refs/notes/ka0s-review` note. If
  `resume-state.sh` lists an item under "LANDED, REVIEW NOT RECORDED", its review must run again.
- An item that lands with no commit goes in `exceptions.tsv` as `<ID>\t<reason + proving command>`.
- `checkpoints.tsv` holds one row per milestone that passed its checkpoint and was pushed.

## Find where it stands

```sh
cd /mnt/d/Profile/Users/Tushar/Documents/GIT/Ka0sAddonsCommonTasks/docs/2026-09-26-AUTOMATED_TESTS_SWEEP
./resume-state.sh -v
```

## Clean up an interrupted item

Items run one at a time per repo, so a dirty tree holds one interrupted item. Read the diff first.
Then either continue the item from where the diff stops, or stash it with
`git stash push -m "<ID> interrupted"` and start the item again. **Never** `reset --hard` or
`checkout .` work you have not read. A perf bisect runs in a throwaway worktree
(`git worktree list`). Remove a stale one with `git worktree remove`; it never holds branch work.

## Relaunch

- Milestones run in order: M0, then M1, then M2, then M3. M2 starts once LK-ATS-10 has landed and the
  local tag `v1.62.0` resolves. The AM-ATS-01 and CM-ATS-01 perf bisects may start earlier, because they
  depend only on M0.
- Each milestone runs as a Workflow. It gets one implementer and one independent reviewer per item, and
  one pipeline per repo. From the session that launched it, relaunch with
  `Workflow({scriptPath, resumeFromRunId})`. From any other session, launch the milestone again: each
  implementer runs `resume-state.sh` first and skips any item that git already records as done.
- A red gate stops that repo's chain. Fix the cause, then relaunch.

## Checkpoints and pushes

- At the end of each milestone, run its checkpoint from `01_EXECUTION_PLAN.md` and append a row to
  `checkpoints.tsv`. The row's evidence is the test totals and the pushed heads.
- Push **feature branches only**, together with the notes:
  `git push origin feat/2026-09-26-automated-tests-sweep refs/notes/ka0s-review`.
- Merging happens only in M4's ATS-FIN, through `/wow-addon:finalize`, which the owner asked for as the
  final step. No addon version is bumped and no release is cut.
- The owner files no GitHub issues for this sweep. Existing issues close through `Fixes #N` in commit
  bodies when the owner merges.

## The executor

`plan-data/execute_chains.js` is the Workflow script. Pass its body inline (or as `scriptPath`) with
`args = {"chains": [{"repo": "<Repo>", "items": ["<ID>", ...]}, ...]}`. Chains run in parallel, and
the items in a chain run in order. List only the items that have not landed; the implementer also skips
any item that git already records. Each item runs implement → independent review (with the note
written) → up to two `<ID>R` fix rounds. A failed item stops its chain.
