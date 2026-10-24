# RESUME — how to pick this run up from any point

**Git is the only state.** The branch in every repo is `feat/2026-10-25-skinning`.

## 1. Where are we?

    cd /mnt/d/Profile/Users/Tushar/Documents/GIT/Ka0sAddonsCommonTasks/docs/2026-10-25-SKINNING
    ./resume-state.sh        # per-milestone counts, RESUME list, unreviewed items, tag, dirty trees, branch check
    ./resume-state.sh -v     # plus every remaining id

- An item is **done** when a commit whose subject starts `<ID>: ` exists in its repo among the run branch's commits on
  top of that repo's default branch. A commit may carry several ids, joined as `A + B: …`.
- An item is **closed** when one of its commits carries a `refs/notes/ka0s-review` note.
- `checkpoints.tsv` is the milestone log. `exceptions.tsv` lists items that land with no commit, each with a proof command.

## 2. Clean up an interrupted item

Items run one at a time per repo, so a dirty tree is one interrupted item. The implementer continues it, or stashes it
under a named message. **Never** `reset --hard` or `checkout .` work you have not read.

## 3. Relaunch

1. **M1**: `python3 plan-data/tools/next_args.py M1 > <scratch>/m1.json`, then run Workflow with `scriptPath:
   plan-data/tools/execute_milestone.js` and `args` set to that JSON.
2. **M2**: only after the M1 checkpoint (§4) and the LOCAL tag `v1.78.0` exists (LK-90). `next_args.py M2`.
3. **M3**: CT-01 by the lead, then stop for the owner's smoke test.

## 4. Milestone checkpoint

1. `./resume-state.sh` shows the milestone COMPLETE and nothing "landed, review not recorded".
2. Every touched repo's gate is green on the run branch (use `/home/tushar/.claude/dev-copilot/bin/ka0s-bounded`).
3. Push the branch and notes for each touched repo: `git push -u origin feat/2026-10-25-skinning && git push origin refs/notes/ka0s-review`.
   **Never push the v1.78.0 tag before the owner's merge go-ahead.** The lead runs pushes; workflow agents only commit locally.
4. Append a `checkpoints.tsv` row and commit it here.

## 5. A library gap (a LootHistory item returns `blocked` with a `library_gap`)

Add an additive LibKa0s item `LK-91…` in `plan-data/addendum-NN.json` and `.tsv`, with a test. Re-run LK-90's gates
and move the local tag (`git tag -f -a v1.78.0`). Record the old and new sha in `99_EXECUTION_RECORD.md`, add an
`LH-RV2` item, then resume.

## 6. Finalize (owner go-ahead only)

Run `/dev-copilot:finalize` in this order: WowAddonStandards → LibKa0s (then `git push origin v1.78.0`) → LootHistory →
Ka0sAddonsCommonTasks. Merge `--no-ff`, push, and delete the branch locally and on origin. Then check `git stash list`
and `git worktree list` in every repo and remove anything this run created.
