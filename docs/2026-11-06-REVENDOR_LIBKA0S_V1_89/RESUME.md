# Resuming the v1.89.0 re-vendor run

1. **State.** `bash docs/2026-11-06-REVENDOR_LIBKA0S_V1_89/plan-data/resume-state.sh` prints each `OPEN`
   item, `TOTAL done/total`, and any repo that is `DIRTY` or on a `BRANCH` other than the run branch or
   master. Git is the only state: an item is done when its repo carries a commit whose subject starts
   `<ID>: `.
2. **An interrupted item.** In a `DIRTY` repo, read the diff before doing anything. A half-copied payload
   is safe to redo: re-extract `v1.89.0` and re-copy, because the copy is idempotent. Never
   `reset --hard` or `checkout .` work you have not read. Stash it with a `v89-` message, or continue it.
3. **Relaunch.** Re-run the item per `00_PLAN.md` (*Per-item procedure* or *Adoptions*). The workflow
   script can be resumed with `resumeFromRunId` in the same session. In a fresh session, launch a new
   workflow over the `OPEN` items only.
4. **Checkpoint.** When every item of a milestone is done: rerun each touched repo's gate, add the
   review note, push the run branch (`git push -u origin feat/2026-11-06-revendor-libka0s-v1-89`, plus
   `git push origin refs/notes/ka0s-review`), and append the row to `checkpoints.tsv`.
5. **Finish** only on the owner's go-ahead: `/dev-copilot:finalize`, then delete every run branch,
   stash and worktree.
