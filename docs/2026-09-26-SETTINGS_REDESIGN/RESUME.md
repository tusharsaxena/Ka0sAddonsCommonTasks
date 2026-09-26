# Resuming the AuraMaster settings redesign (#6)

The plan (`03_EXECUTION_PLAN.md`) is frozen once execution starts. This file tells a fresh session
how to find where the run stands and pick it up from any point.

## State lives in git

- **An item is done when a commit whose subject starts `<ID>: ` exists in the repo `items.tsv`
  names**, on `feat/2026-09-26-settings-redesign` or that repo's default branch. `<ID> + <ID>: ...`
  counts for both ids, and `<ID>R: ` is a review fix on a done item. Nothing else is state: not this
  file, not a status table, not a session's memory.
- `SR-LK-03` makes two commits (`docs/releasing.md` step 7) and then the local annotated tag
  `v1.61.0`. **It is done only when the tag exists**, not at its first commit: `resume-state.sh`
  checks `git -C ../../../LibKa0s rev-parse v1.61.0^{}`, keeps SR-LK-03 out of the done set until the
  tag resolves, and prints `IN PROGRESS: SR-LK-03 …` meanwhile, so SR-AM-01 is never READY before
  the release battery, the ANALYSIS commit and the tag exist. Resume a half-done release at SR-LK-03
  Step 4 (the battery) if only the first commit landed, or Step 6 (the tag) if both did.
- An item that legitimately lands with no commit goes in `exceptions.tsv` (create it) as
  `<ID>\t<reason and a command that proves it>`.
- Independent reviews are `refs/notes/ka0s-review` git notes on the item's commit.

## Find where it stands

```sh
cd /mnt/d/Profile/Users/Tushar/Documents/GIT/Ka0sAddonsCommonTasks/docs/2026-09-26-SETTINGS_REDESIGN
./resume-state.sh -v
```

It prints each milestone's count, the READY items (every dependency done), each repo's branch and
dirty state, and whether the local tag `v1.61.0` exists.

## Clean up an interrupted item

- A dirty tree in WowAddonStandards, LibKa0s or AuraMaster is the partial work of that repo's next
  item. Read the diff. Then either **continue** it, finishing the item's steps from where the diff
  shows it stopped, or `git stash push -m "<ID> interrupted"` it and restart the item. **Never**
  `git reset --hard` or `git checkout .` work you have not read.
- A branch that does not exist yet: cut it from `master` as the item's Step 1 says, but only when no
  item in that repo has landed.
- In LibKa0s, a red gate after `SR-LK-03`'s first commit means the release run found something. Fix it
  in an `SR-LK-0nR` commit and re-run from SR-LK-03 Step 3's gate. **Never re-cut `v1.61.0`** once it
  exists. A defect found after the tag ships as `v1.61.1`, and AuraMaster re-vendors that tag.

## Relaunch

- The run is a Workflow with one implementer and one independent reviewer per task. Relaunch it with
  its script path and `resumeFromRunId` when the session that ran it is still available. From any
  other session, relaunch from scratch: every implementer first runs `resume-state.sh` and skips an
  item git already records.
- Order: M1's two repos run in parallel (SR-WS-01 -> SR-WS-02, and SR-LK-01 -> SR-LK-02). SR-LK-03
  waits for both. M2 runs strictly in order, SR-AM-01 through SR-AM-06, one at a time in the one
  AuraMaster tree. SR-REC-01 runs last, on `main` here.
- A red gate stops that repo's chain. Fix the problem, then relaunch.

## Checkpoints and pushes

- At the end of each milestone, run the checkpoint in `03_EXECUTION_PLAN.md` and append its row to
  `checkpoints.tsv` (`when`, `checkpoint`, `evidence`).
- **Push only if the owner authorized pushes when reviewing the plan.** Record that authorization
  (or its absence) in the M1 row. Push feature branches and `refs/notes/ka0s-review` only, **never a
  tag**, and never merge. `/wow-addon:finalize` runs later, on the owner's go-ahead.
- In-client smoke checks (`06_SMOKE_TESTS.md`) are the owner's. Never mark one passed.

## Scope guard

AuraMaster only. MultiMeters (#55) and KickCD (#33) are later, separate work. Do not touch them, and
do not re-vendor v1.61.0 into any other addon.
