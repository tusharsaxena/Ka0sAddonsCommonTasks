# Resume: skin fonts and feedback

## 1. Find the state

```
./resume-state.sh -v
```

Git is the only state. An item is done when a commit whose subject starts `<ID>: ` is on
`feat/2026-10-30-skin-fonts-feedback` in the repo `items.tsv` names, or when `exceptions.tsv` lists it with a proof
command (every IS-* item: the issue or comment URL, proven by `gh issue view`). `checkpoints.tsv` records the
milestones that passed and were pushed.

## 2. Clean up an interrupted item

In the repo that owns it: `git status`. A dirty tree belongs to the item the log does not show yet. Read the diff
and either finish the item or `git stash push -m "<ID> interrupted"`. Never `reset --hard` or `checkout .` work you
have not read. Every stash the run makes is dropped at M5.

## 3. Relaunch

- **M1**: LibKa0s items in id order, one implementer at a time; WS-01 may run alongside. LK-90 after LK-13, ST-01
  after LK-90. Each implementer reads `./resume-state.sh -v` and skips landed ids.
- **M2**: only after the M1 checkpoint. One agent per addon, ids in order, XX-01 first. Relaunch the workflow
  (`scriptPath` = the persisted script, `resumeFromRunId` when known, else fresh: landed ids are skipped).
- **M3**: issues one at a time, at least 20 s apart. Before writing, search for a duplicate (`gh issue list --search`).
- **M4**: the lead writes `99_REPORT.md` and `06_SMOKE_TESTS.md`, then stops for the owner.

## 4. Milestone checkpoint

1. `./resume-state.sh` shows the milestone COMPLETE and no unreviewed branch.
2. Every touched repo's gate is green on the run branch (through the bounded runner), against
   `plan-data/baselines.tsv`.
3. The LEAD pushes each touched repo: `git push -u origin feat/2026-10-30-skin-fonts-feedback && git push origin
   refs/notes/ka0s-review`. Workflow agents only commit locally. **Never push the tag before the owner's go-ahead.**
4. Append a `checkpoints.tsv` row and commit it here.

## 5. A library gap found in M2

Compose it from existing primitives if possible and record it in the report. Otherwise stop the item with
`blocked: library_gap`. The lead adds an `LK-A<n>` row in `plan-data/addendum-NN.tsv`, lands it, re-cuts the local
tag after a clean release run, re-vendors the blocked addon (`XX-RV2`) and resumes. Record each re-cut in
`99_REPORT.md`.

## 6. Finalize (owner go-ahead only)

In order: WowAddonStandards → LibKa0s (then push tag v1.82.0) → LibKa0sSkinTester → the addons →
Ka0sAddonsCommonTasks. Merge `--no-ff`, push, delete the remote branch **before** `git branch -d` (the local branch
tracks an older remote head). A vendored copy differs from LibKa0s only by the declared icon prune
(`Only in .../media/icons*`); anything else is drift. Then `git stash list` and `git worktree list` in every repo, and
remove anything this run created.
