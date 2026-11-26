# Resume

1. **State.** Run `plan-data/resume-state.sh`. It reads git in `~/ka0s-scratch/r4/<Repo>`; set `KA0S_GIT` to the live GIT
   folder once the branches are fetched there. An item is done when its `<ID>: ` commit exists on
   `feat/2026-11-26-owner-feedback-round4`, or on master after the merge.
2. **Clones.** If `~/ka0s-scratch/r4/<Repo>` is missing, clone the live repo, set `origin` to the GitHub URL, add the live
   repo as remote `live`, and check out the branch (fetch it from origin if it was pushed). LibKa0s's tag v1.118.0 is local
   until the merge; if the clone is lost, re-cut it on the R4-LK-01 release commit.
3. **An interrupted item.** In its clone, read `git status` and `git diff`. Finish or stash the work; never `reset --hard`
   work you have not read. Then re-run the gate (00_PLAN.md) before committing.
4. **Relaunch.** Build the remaining items in manifest order. Chains: LibKa0s → DropWatcher; CombatTrail; RangeMaster.
   Then review per repo, then fix.
5. **Checkpoint M3.** The lead re-gates every clone, pushes each branch (`git -C <live> fetch <clone> +B:B`, then
   `git push -u origin B`), and appends a row to `plan-data/checkpoints.tsv` with the totals and heads.
6. **Merge.** Only on the owner's go-ahead: merge `--no-ff` in each clone onto `live/master`, re-gate, fast-forward the
   live repo, push, push tag v1.118.0, then delete the branches and `~/ka0s-scratch/r4`.
