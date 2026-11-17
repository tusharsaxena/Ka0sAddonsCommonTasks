# Resuming this run

1. Run `bash docs/2026-11-17-LIBKA0S_V1_105_ADOPTION/plan-data/resume-state.sh`. It reads git only.
2. In a repo with a dirty tree, read `git status` and `git diff` first. Finish the item's own half-done work and commit
   it with the item's id, or `git stash push -m "<ID> partial"`. Never `reset --hard` or `checkout .` unread work.
3. Relaunch the wave's workflow from `plan-data/` (resume from its run id in the same session, or fresh). Each
   addon agent skips the items it finds committed.
4. Checkpoint: re-gate every touched addon under every client it ships, push the run branches, add a row to
   `checkpoints.tsv`, and write the wave's smoke sheet (`A_SMOKE.md`, ...).
5. Merging needs the owner's go-ahead. Then run `/dev-copilot:finalize` and close or comment the adoption issues.
   Delete the run branches, stashes and worktrees.
