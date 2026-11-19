# Resuming this run

1. Run `bash docs/2026-11-19-ADOPTION_FEEDBACK/plan-data/resume-state.sh`. It reads git only: an item is done when a
   commit whose subject starts `<ID>: ` exists on the run branch or, after the merge, on the default branch, or when
   the item has a row in `plan-data/exceptions.tsv`.
2. In a repo with a dirty tree, read `git status` and `git diff` first. Finish the item's half-done work and commit it
   with the item's id, or `git stash push -m "<ID> partial"`. Never `reset --hard` or `checkout .` unread work.
3. M1 runs before M2, because the addons re-vendor LibKa0s v1.107.0 from its local tag. Relaunch the milestone's
   workflow from `plan-data/` (resume from its run id in the same session, or start it fresh). Agents skip the items
   they find committed.
4. Checkpoint CP-1: re-gate every touched repo under each client it ships and push the run branches. Then add a row
   to `checkpoints.tsv`, write `SMOKE.md` and update `99_EXECUTION_RECORD.md`.
5. Merging needs the owner's go-ahead. Then run `/dev-copilot:finalize`, push the LibKa0s v1.107.0 tag and the
   standard's tag, archive DpsRace and rename the `main` defaults to `master`. Delete the run branches, stashes and
   worktrees.
