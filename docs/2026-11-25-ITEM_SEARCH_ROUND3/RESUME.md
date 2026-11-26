# Resume

1. **Get the state.**
   - While the work is still in the clones, run
     `docs/2026-11-25-ITEM_SEARCH_ROUND3/plan-data/resume-state.sh`. It defaults to
     `KA0S_GIT=~/ka0s-scratch/isr3`. ISR3-PLAN is always read from this repo.
   - Once the branches are live, run it as
     `KA0S_GIT=/mnt/d/Profile/Users/Tushar/Documents/GIT docs/2026-11-25-ITEM_SEARCH_ROUND3/plan-data/resume-state.sh`.
2. **Clean up an interrupted item.**
   - In its clone, run `git status`. Read any uncommitted work, then continue it or stash it. Never
     `reset --hard` or `checkout .` work you haven't read.
   - If the complexity suite left a `docs/automated-tests/<stamp>/` bundle or a `RESULTS.md` change
     outside ISR3-LK-REL, restore it.
3. **Relaunch.**
   - Re-invoke the workflow with `resumeFromRunId`. The run id is in `EXECUTION_RECORD.md` once it is
     written.
   - Or brief a fresh builder from `03_SPEC.md` for just the missing ids, in `plan-data/items.tsv`
     order. ISR3-DW-00 needs the local `v1.117.0` tag in the LibKa0s clone (`git -C
     ~/ka0s-scratch/isr3/LibKa0s tag -l v1.117.0`).
4. **Checkpoint.** Run the milestone's checkpoint from `04_EXECUTION_PLAN.md`. Then append a row to
   `plan-data/checkpoints.tsv` with the test totals and the heads.
5. **After the merge,** delete `~/ka0s-scratch/isr3/`, the feature branches (local and origin) and any
   stashes.
