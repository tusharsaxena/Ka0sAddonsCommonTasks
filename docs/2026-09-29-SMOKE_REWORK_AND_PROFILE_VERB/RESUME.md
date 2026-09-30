# Resuming the smoke-test rework and `profile` verb run

The plan (`03_EXECUTION_PLAN.md`) is frozen once execution starts. This file tells a fresh session how
to find where the run stands and pick it up from any point.

## State lives in git

- **An item is done when a commit whose subject starts `<ID>: ` exists in the repo `items.tsv` names**,
  on `feat/2026-09-29-smoke-and-profile` or that repo's default branch. `<ID>R: ` is a review fix on a
  done item. Nothing else is state: not this file, not a status table, not a session's memory.
- An item is **reviewed** when its commit (or its last `<ID>R:` fix) carries a `refs/notes/ka0s-review`
  note starting `OK <ID>`.
- An item that legitimately lands with no commit goes in `exceptions.tsv` (create it) as
  `<ID>\t<reason and a command that proves it>`.
- Milestones are recorded in `checkpoints.tsv` when closed.

## Find where it stands

```sh
cd /mnt/d/Profile/Users/Tushar/Documents/GIT/Ka0sAddonsCommonTasks/docs/2026-09-29-SMOKE_REWORK_AND_PROFILE_VERB
./resume-state.sh -v
```

It prints each milestone's done/reviewed count, the READY items (every dependency done **and
reviewed**; an item never starts on unreviewed work), whether the
LibKa0s `v1.63.0` tag exists locally, and each repo's branch, dirty state and ahead-of-origin count
(`never-pushed` when the branch has no origin copy yet: a push is owed at the milestone end).

## Clean up an interrupted item

- A dirty tree is the partial work of that repo's next item. Read the diff, then either continue it or
  `git stash push -m "<ID> interrupted"` and restart. **Never** `git reset --hard` or `git checkout .`
  work you have not read.
- A half-copied re-vendor is safe to finish: rerun the copy from the tag (idempotent).
- Line endings: addon files are CRLF. A file the kit's eol test names was written with LF: convert it
  (`sed -i 's/\r*$/\r/' <file>` on a file that is entirely LF) and re-run the gate.

## Rules that do not change on resume

- No merge to any `master`, no pushed tag, until the owner says so. Branches are pushed at milestone ends.
- Every Lua / luacheck run goes through `~/.claude/wow-addon/bin/ka0s-bounded`.
- `libs/` and `tests/_kit/` change only by the re-vendor copy step.
