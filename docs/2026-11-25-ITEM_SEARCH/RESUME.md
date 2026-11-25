# Resume

1. **Get the state.**
   - While the work is still in the clones, run
     `KA0S_GIT=~/ka0s-scratch/itemsearch docs/2026-11-25-ITEM_SEARCH/plan-data/resume-state.sh`.
   - Once the branches are live, run it with no `KA0S_GIT`.
2. **Clean up an interrupted item.** In its clone, run `git status`. Read any uncommitted work, then continue it or
   stash it. Never `reset --hard` work you haven't read.
3. **Relaunch.** Re-invoke the workflow with `resumeFromRunId`; the run id is in `EXECUTION_RECORD.md` once written. Or
   brief a fresh builder from `03_SPEC.md` for just the missing ids.
4. **Checkpoint.** Run the milestone's checkpoint from `04_EXECUTION_PLAN.md`, then append a row to
   `plan-data/checkpoints.tsv`.
5. **After the merge,** delete `~/ka0s-scratch/itemsearch/`, the feature branches (local and origin) and any stashes.
