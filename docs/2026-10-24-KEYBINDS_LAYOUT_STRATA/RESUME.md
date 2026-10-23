# RESUME — how to pick this run up from any point

**Git is the only state.** The branch in every repo is `feat/2026-10-24-keybinds-layout-strata`.

## 1. Where are we?

    cd /mnt/d/Profile/Users/Tushar/Documents/GIT/Ka0sAddonsCommonTasks/docs/2026-10-24-KEYBINDS_LAYOUT_STRATA
    ./resume-state.sh        # per-milestone counts, RESUME list, unreviewed items, tag, plugin version, dirty trees, branch check
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
2. **Before M2**: the local tag `v1.77.0` exists (LK-90), and the M1 checkpoint (§4) is done. Export the owner's
   decisions (ArtifactData `list` on https://claude.ai/artifact/3iN2yVj3u9rrV9ndLB5PU8, collection `decisions`,
   `query.limit` 1000, `out_dir` `plan-data/decisions-export`), then run `python3 plan-data/tools/make_accepted.py` and
   commit `plan-data/accepted.json`. M2 is `next_args.py M2 --order` (serial RV → KB → ZS per repo).
3. **M3**: only after the owner says the preview review is done. Re-export, re-run `make_accepted.py`, and design
   addendum-01 (see `04_EXECUTION_PLAN.md`).
4. **M4**: CT-01 by the lead. **CT-02 only on the owner's explicit merge go-ahead.**

## 4. Milestone checkpoint

1. `./resume-state.sh` shows the milestone COMPLETE and nothing "landed, review not recorded".
2. Every touched repo's gate is green on the run branch (use `/home/tushar/.claude/dev-copilot/bin/ka0s-bounded`).
3. Push the branch and notes for each touched repo: `git push -u origin feat/2026-10-24-keybinds-layout-strata && git push origin refs/notes/ka0s-review`.
   **Never push the v1.77.0 tag before CT-02.** The lead runs pushes; workflow agents only commit locally.
4. Append a `checkpoints.tsv` row and commit it here.

## 5. A library gap (an addon item returns `blocked` with a `library_gap`)

Add an additive LibKa0s item `LK-91…` in `plan-data/addendum-NN.json` and `.tsv`, with a test. Re-run LK-90's gates
and move the local tag (`git tag -f -a v1.77.0`). Record the old and new sha in `99_EXECUTION_RECORD.md`, give each
re-vendored addon a `<PFX>-RV2` item, then resume.

## 6. Finalize (CT-02, owner go-ahead only)

Run `/dev-copilot:finalize` in this order: WowAddonStandards → LibKa0s (then `git push origin v1.77.0`) → dev-copilot →
15 addons → Ka0sAddonsCommonTasks. Merge `--no-ff`, push, and delete the branch locally and on origin. Then check
`git stash list` and `git worktree list` in every repo and remove anything this run created.
