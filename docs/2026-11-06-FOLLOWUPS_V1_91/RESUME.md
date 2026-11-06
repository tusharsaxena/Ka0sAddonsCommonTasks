# Resuming the v1.91.0 follow-ups

1. Run `bash docs/2026-11-06-FOLLOWUPS_V1_91/plan-data/resume-state.sh`. It prints the OPEN items, the
   total, and any repo that is DIRTY or on another branch. An item is done when its repo has a commit
   whose subject starts `<ID>: `.
2. In a DIRTY repo, read the diff first. A half-copied re-vendor can be redone, because the copy is
   idempotent. Never `reset --hard` work you have not read.
3. Relaunch the OPEN items per `00_PLAN.md`. Checkpoint per milestone: re-gate, add review notes, push
   the branches and `refs/notes/ka0s-review`, and log a row in `checkpoints.tsv`. The v1.91.0 tag
   stays local until the finalize.
4. Finish only on the owner's go-ahead: run the finalize, then delete every run branch, stash and
   worktree.
