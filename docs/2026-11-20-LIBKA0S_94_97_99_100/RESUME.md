# Resuming this run

1. Run `bash docs/2026-11-20-LIBKA0S_94_97_99_100/plan-data/resume-state.sh`. It reads git only: an item is done when
   a commit whose subject starts `<ID>: ` exists on the run branch or, after the merge, on the default branch, or when
   the item has a row in `plan-data/exceptions.tsv`.
2. In a repo with a dirty tree, read `git status` and `git diff` first. Finish the item's half-done work and commit it
   with the item's id, or `git stash push -m "<ID> partial"`. Never `reset --hard` or `checkout .` unread work.
3. Order: M0 (audit) and SD-LK-94/99/100 together; SD-RULE (owner's calls on UNCLEAR rows) before SD-LK-97 and the
   SD-SK items; SD-LK-REL tags v1.108.0 locally before any SD-RV item copies it. Relaunch the milestone's workflow
   (resume from its run id in the same session, or start fresh). Agents skip items they find committed.
4. CP-1: re-gate every touched repo under each client it ships, push the run branches and `refs/notes/ka0s-review`,
   add a `checkpoints.tsv` row, write `SMOKE.md` and `99_EXECUTION_RECORD.md`.
5. Merging needs the owner's go-ahead. Then `/dev-copilot:finalize`, push LibKa0s v1.108.0 and the standard's tag
   (fetch and renumber first if another session released it), close #94 #97 #99 #100, delete the run's branches,
   stashes and worktrees.
