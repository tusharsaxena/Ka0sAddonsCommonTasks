# RESUME: picking this run up from any point

**Git is the only state.** The branch in every repo the run touches is `feat/2026-10-29-skinning-rollout`.

## 1. Where are we?

    cd /mnt/d/Profile/Users/Tushar/Documents/GIT/Ka0sAddonsCommonTasks/docs/2026-10-29-SKINNING_ROLLOUT
    ./resume-state.sh        # per-milestone counts, the RESUME list, unreviewed branches, the tag, dirty trees
    ./resume-state.sh -v     # plus every remaining id

- An item is **done** when a commit whose subject starts `<ID>: ` is among the run branch's commits on top of the
  repo's default branch. One commit may carry several ids: `AT-01 + AT-02: ...`.
- A repo is **reviewed** when a commit on its run branch carries a `refs/notes/ka0s-review` note.
- `exceptions.tsv` lists items that land with no commit, each with a proof command. `checkpoints.tsv` is the
  milestone log.

## 2. Clean up an interrupted item

Each repo has one implementer at a time, so a dirty tree is one interrupted item. Read it; continue it, or stash it
under a named message (`git stash push -m "skinning-rollout: <ID> interrupted"`). **Never** `reset --hard` or
`checkout .` work you have not read. Any stash the run makes is dropped at M4.

## 3. Relaunch

- **M0** (inventory, read-only): rerun the M0 workflow for the addons with no `inputs/inventory/<Addon>.md`.
- **M1**: the LK / ST / WS items in `plan-data/addendum-*.tsv`. Lead-run or a small workflow.
- **M2**: only after the M1 checkpoint. Relaunch the M2 workflow (`Workflow` with `scriptPath` = the persisted
  script, `resumeFromRunId` if the run id is known, else fresh): each per-addon implementer reads
  `./resume-state.sh -v` and skips ids already landed, so a fresh launch is safe.
- **M3**: lead writes `99_REPORT.md` and `06_SMOKE_TESTS.md`, then stops for the owner.

## 4. Milestone checkpoint

1. `./resume-state.sh` shows the milestone COMPLETE and no unreviewed branch.
2. Every touched repo's gate is green on the run branch (through `~/.claude/dev-copilot/bin/ka0s-bounded`).
3. The LEAD pushes each touched repo: `git push -u origin feat/2026-10-29-skinning-rollout && git push origin
   refs/notes/ka0s-review`. Workflow agents only commit locally. **Never push a tag before the owner's go-ahead.**
4. Append a `checkpoints.tsv` row and commit it here.

## 5. A library gap found in M2

An addon implementer that hits a gap M0 missed composes it from existing primitives if it can (gap policy rung 1)
and records it in its report. If it cannot, it stops that item with `blocked: library_gap`. The lead adds an
`LK-A<n>` item in `plan-data/addendum-NN.tsv`, lands it, re-cuts the local tag after a clean-tree release run,
re-vendors the blocked addon (`XX-RV2`) and resumes. Record each re-cut in `99_REPORT.md`.

## 6. Finalize (owner go-ahead only)

`/dev-copilot:finalize` in order: WowAddonStandards → LibKa0s (then push its tag) → LibKa0sSkinTester → the
fourteen addons → Ka0sAddonsCommonTasks. Merge `--no-ff`, push, delete the branch locally and on origin. Then
`git stash list` and `git worktree list` in every repo, and remove anything this run created.
