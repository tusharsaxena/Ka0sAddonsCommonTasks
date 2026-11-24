# Resume

1. **Get the state.** Run
   `KA0S_GIT=~/ka0s-scratch/seeds docs/2026-11-25-SEEDS_AND_FOREVERDB/plan-data/resume-state.sh` while the work is
   in the clones, and with no `KA0S_GIT` once the branches are live.
2. **Clean up an interrupted item.** In its clone, run `git status`. Read any uncommitted work, then continue it or
   `git stash` it. Never `reset --hard` work you have not read.
3. **Relaunch.** Re-invoke the workflow with `resumeFromRunId` (the run id is in `EXECUTION_RECORD.md` once
   written), or brief a fresh builder from `03_SPEC.md` for just the missing ids.
4. **Checkpoint.** Run each milestone's checkpoint as `04_EXECUTION_PLAN.md` describes, then append a row to
   `plan-data/checkpoints.tsv` with the test totals and heads.
5. **Clean up after the merge.** Delete `~/ka0s-scratch/seeds/`, the feature branches (local and origin) and any
   stashes.
