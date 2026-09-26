# Resuming the NavRail adoption

The plan (`03_EXECUTION_PLAN.md`) is frozen once execution starts. This file tells a fresh session
how to find where the run stands and pick it up from any point.

## State lives in git

- **An item is done when a commit whose subject starts `<ID>: ` exists in the repo `items.tsv`
  names**, on `feat/2026-09-26-navrail-adoption` or that repo's default branch. `<ID> + <ID>: ...`
  counts for both ids, and `<ID>R: ` is a review fix on a done item. Nothing else is state: not this
  file, not a status table, not a session's memory.
- Every item is one commit. None needs a tag or a push to count as done.
- An item that legitimately lands with no commit goes in `exceptions.tsv` (create it) as
  `<ID>\t<reason and a command that proves it>`.
- Independent reviews are `refs/notes/ka0s-review` git notes on the item's commit.

## Find where it stands

```sh
cd /mnt/d/Profile/Users/Tushar/Documents/GIT/Ka0sAddonsCommonTasks/docs/2026-09-26-NAVRAIL_ADOPTION
./resume-state.sh -v
```

It prints each milestone's count, the READY items (every dependency done), whether LibKa0s's
`v1.61.0` tag resolves locally, and each repo's branch, dirty state and whether its
`libs/LibKa0s/OptionsNav.lua` exists (the v1.61.0 payload is in).

## Clean up an interrupted item

- A dirty tree in one of the ten addons is the partial work of that repo's next item. Read the diff.
  Then either **continue** it, finishing the item's steps from where the diff shows it stopped, or
  `git stash push -m "<ID> interrupted"` it and restart the item. **Never** `git reset --hard` or
  `git checkout .` work you have not read.
- A half-copied re-vendor (some of `libs/LibKa0s` changed, the rest not) is safe to finish: rerun
  the item's copy step. The copy is idempotent, because it copies from the tag and never from a
  working tree.
- A branch that does not exist yet: cut it from `master` as the item's Step 1 says, but only when no
  item in that repo has landed.
- Line endings: every file the addon items write is CRLF (`* text=auto eol=crlf`). A file that the
  kit's eol gate (`test_eol`) names was written with LF. Run the plan's `crlf` shorthand on it; do
  not revert it.

## Relaunch

- The run is a Workflow with one implementer and one independent reviewer per task. Relaunch it with
  its script path and `resumeFromRunId` when the session that ran it is still available. From any
  other session, relaunch from scratch: every implementer first runs `resume-state.sh` and skips an
  item git already records.
- First, the bundle commit (`03_EXECUTION_PLAN.md`, "Before M1"). If
  `git -C ../.. log --oneline main -- docs/2026-09-26-NAVRAIL_ADOPTION/03_EXECUTION_PLAN.md` prints
  nothing, the bundle is not committed yet: commit it before any item.
- Order: M1's ten items are independent, one per repo, and may run in parallel. In M2, MultiMeters
  (NR-MM-02 -> 03 -> 04) and KickCD (NR-KC-02 -> 03 -> 04) run in parallel, each chain strictly in
  order in its own tree, and each starts only when its own NR-XX-01 is done. NR-REC-01 runs last, on
  `main` here.
- A red gate stops that repo's chain. Fix the problem, then relaunch.

## Checkpoints and pushes

- At the end of each milestone, run the checkpoint in `03_EXECUTION_PLAN.md` and append its row to
  `checkpoints.tsv` (`when`, `checkpoint`, `evidence`) as the milestone passes, not afterwards.
- **No pushes in this run.** The owner has not authorized pushing these branches. Record that in the
  M1 row. Nothing is merged, no tag is made, and no addon's version moves. `/wow-addon:finalize`
  runs later, on the owner's go-ahead.
- In-client smoke checks (`06_SMOKE_TESTS.md`) are the owner's. Never mark one passed.

## Scope guard

The ten addons in `items.tsv` and this bundle only. AuraMaster is done (it re-vendored v1.61.0 in
SR-AM-01 and shipped its Containers page) and is not touched. LibKa0s and WowAddonStandards are read
only: the tag `v1.61.0` and standard v2.69.0 are already published. Only MultiMeters and KickCD get
a rail. The other eight addons get the library copy and the `NavRail` stub no-op (ConsumableMaster: its
Options inventory instead, `02_SPEC.md` R18), and nothing else.
