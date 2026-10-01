# Resuming the 2026-10-01 GitHub issue pass

The plan (`03_EXECUTION_PLAN.md`) is frozen once execution starts. This file tells a fresh session how to find
where the run stands and pick it up from any point.

## State lives in git

- **An item is done when a commit whose subject starts `<ID>: `** (or names it in `A + <ID>: `) exists in the
  repo `items.tsv` names, on `feat/2026-10-01-github-issue-pass` or that repo's default branch. `<ID>R: ` is a
  review fix on a done item.
- An item is **reviewed** when its commit (or its last `<ID>R:` fix) carries a `refs/notes/ka0s-review` note
  starting `OK <ID>`.
- An item that legitimately lands with no commit goes in `exceptions.tsv` as `<ID>\t<reason and a command that
  proves it>`.
- Milestones are recorded in `checkpoints.tsv` when closed.

## Find where it stands

```sh
cd /mnt/d/Profile/Users/Tushar/Documents/GIT/Ka0sAddonsCommonTasks/docs/2026-10-01-GITHUB_ISSUE_PASS
./resume-state.sh -v
```

It prints each milestone's done/reviewed count, the READY items, whether tag `v1.66.0` exists in LibKa0s,
and each repo's branch, dirty state and unpushed count.

## Clean up an interrupted item

- A dirty tree is the partial work of that repo's next item. Read the diff, then continue it or
  `git stash push -m "<ID> interrupted"` and restart. **Never** `git reset --hard` or `git checkout .` work you
  have not read.
- A half-copied re-vendor is safe to finish: rerun the copy from the tag (idempotent).
- Line endings: addon files are CRLF. If the kit's eol test names a file written with LF, convert it and re-run.

## Relaunch

Relaunch the milestone's workflow with the same script and `resumeFromRunId` when the session still has it.
Otherwise write a new workflow over the READY items only. The per-item recipe is in `03_EXECUTION_PLAN.md`.

## Rules that do not change on resume

- No merge to any `master`, no pushed tag, until the owner says so. Feature branches are pushed at milestone ends.
- Never bump an addon's version. Heavy runs go through `ka0s-bounded`.
- GitHub writes are throttled (a few seconds apart).
