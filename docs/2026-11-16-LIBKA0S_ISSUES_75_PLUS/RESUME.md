# Resuming this run

1. **Find where it stands.** Run `bash docs/2026-11-16-LIBKA0S_ISSUES_75_PLUS/plan-data/resume-state.sh`. It reads
   git only.
2. **Clean up an interrupted item.** In its repo, run `git status` and `git diff`, and read the work before touching
   it.
   - If it is the item's own half-done work, finish it and commit it with the item's id.
   - Otherwise run `git stash push -m "<ID> partial"`.

   Never `reset --hard` or `checkout .` work you have not read. DropWatcher's main checkout belongs to another
   session: never touch it. This run's DropWatcher work lives in `../.worktrees/DropWatcher-75plus` when that
   worktree exists.
3. **Relaunch.** Resume the workflow from its run id in the same session, or start it fresh. Every item checks for
   its own commit and skips itself when it finds one.
4. **Run the checkpoint.** Run the milestone's gate from `01_EXECUTION_PLAN.md`, then push the run branches (never
   the tag before finalize). Then add a row to `checkpoints.tsv` with the milestone, date, totals and heads.
5. **After the owner's smoke and go-ahead,** in this order:
   - Run `git fetch` in WowAddonStandards and renumber v2.113.0 if another session released that number (memory
     `standard-version-collisions`).
   - Run `/dev-copilot:finalize` in dependency order: LibKa0s, then the 19 addons, then WowAddonStandards and
     dev-copilot, then Ka0sAddonsCommonTasks. Merge with `--no-ff`.
   - Push the `v1.105.0` tag.
   - Close the issues the run built: #75, #78 (its library part; note the leftovers), #79, #80, #81, #82, #84,
     #86, #87, #90 and #92. Close each one only if its acceptance is met without phase [3]. Otherwise comment
     what shipped and leave it open for adoption (#79, #86, #88, #89 and #92 have adoption checklists).
   - Delete every run branch, local and remote. Remove the DropWatcher worktree. Drop any stash the run created.
