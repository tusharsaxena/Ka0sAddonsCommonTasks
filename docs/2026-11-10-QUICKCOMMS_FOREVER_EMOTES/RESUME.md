# Resuming this run

1. **Where it stands:** `bash docs/2026-11-10-QUICKCOMMS_FOREVER_EMOTES/plan-data/resume-state.sh`. It reads git only.
2. **An interrupted item:** in its repo, `git status` and `git diff`. Read the work before touching it. If it is the
   item's own half-done work, finish it and commit it with the item's id. Otherwise `git stash push -m "<ID> partial"`.
   Never `reset --hard` or `checkout .` work you have not read.
3. **Relaunch:** rerun the workflow (resume from its run id in the same session, or launch it fresh). Every item
   checks for its commit and skips itself when it exists.
4. **Checkpoint:** run the milestone's gate from `01_EXECUTION_PLAN.md`, push the branches, then add a row to
   `checkpoints.tsv` (milestone, date, totals, heads).
5. **After the owner's smoke and go-ahead:** `/dev-copilot:finalize` in dependency order (LibKa0s, then
   LibKa0sSkinTester, QuickComms, WowAddonStandards, Ka0sAddonsCommonTasks). Push the v1.95.0 tag, then delete this
   run's branches, stashes and worktrees.
