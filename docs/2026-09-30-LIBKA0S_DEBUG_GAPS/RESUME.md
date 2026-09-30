# Resuming the LibKa0s debug-gaps run (G1-G5)

The plan (`03_EXECUTION_PLAN.md`) is frozen once execution starts. This file tells a fresh session how
to find where the run stands and pick it up from any point.

## State lives in git

- **An item is done when a commit whose subject starts `<ID>: ` exists in the repo `items.tsv` names**,
  on `feat/2026-09-30-libka0s-debug-gaps` or that repo's default branch. `<ID>R: ` is a review fix on
  a done item. Nothing else is state.
- An item is **reviewed** when its commit (or its last `<ID>R:` fix) carries a `refs/notes/ka0s-review`
  note starting `OK <ID>`.
- An item that legitimately lands with no commit goes in `exceptions.tsv` (create it) as
  `<ID>\t<reason and a command that proves it>`.
- Milestones are recorded in `checkpoints.tsv` when closed.

## Find where it stands

```sh
cd /mnt/d/Profile/Users/Tushar/Documents/GIT/Ka0sAddonsCommonTasks/docs/2026-09-30-LIBKA0S_DEBUG_GAPS
./resume-state.sh -v
```

It prints each milestone's done/reviewed count, the READY items (every dependency done **and
reviewed**), whether the LibKa0s `v1.65.0` tag exists locally, and each repo's branch, dirty state and
ahead-of-origin count.

## Clean up an interrupted item

- A dirty tree is the partial work of that repo's next item. Read the diff, then continue it or
  `git stash push -m "<ID> interrupted"` and restart. **Never** `git reset --hard` or `git checkout .`
  work you have not read.
- A half-copied re-vendor is safe to finish: rerun the copy from the tag (idempotent).
- Line endings: addon files are CRLF. A file the kit's eol test names was written with LF: convert it
  (`sed -i 's/\r*$/\r/' <file>` on a file that is entirely LF) and re-run the gate. Python edits must
  open files with `newline=''`.

## Rules that do not change on resume

- No merge to any `master`, no pushed tag, until the owner says so. Branches are pushed at milestone ends.
- Never bump an addon's version. Heavy runs (tests, luacheck, lizard) go through `ka0s-bounded`.
