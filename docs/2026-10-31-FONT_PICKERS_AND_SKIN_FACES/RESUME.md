# Resume: font pickers and skin faces

1. **State.** `./resume-state.sh -v`. Git is the only state: an item is done when a `<ID>: ` commit is on `feat/2026-10-31-font-pickers-skin-faces` past the base in `bases.tsv`.
2. **Interrupted item.** In the owning repo read `git status` and the diff; finish it or `git stash push -m "<ID> interrupted"`. Never `reset --hard` or `checkout .` unread work.
3. **Relaunch.** M1: LK-F in id order, skipping landed ids; ST-F01 after LK-F90. M2: only after the M1 checkpoint, one agent per addon. Relaunch the persisted workflow script, or a fresh one: landed ids are skipped.
4. **Checkpoint.** Milestone complete, no unreviewed branch, gates green, then the LEAD runs `git push -u origin <branch> && git push origin refs/notes/ka0s-review` per repo and appends `checkpoints.tsv`. Never push a tag before the go-ahead.
5. **Library gap in M2.** Add an `LK-A<n>` row in `plan-data/addendum-NN.tsv`, land it, re-cut local v1.83.0 after a clean release run, re-vendor the blocked addon (`XX-RV2`).
6. **Finalize, owner go-ahead only.** First the 2026-10-30 run's RESUME §6 ordering applies to both runs: this branch contains that one, so merge this branch `--no-ff` in WowAddonStandards → LibKa0s (push tags v1.82.0 and v1.83.0) → LibKa0sSkinTester → addons → this repo. Delete both run branches, remote first, then check `git stash list` and `git worktree list` everywhere.
