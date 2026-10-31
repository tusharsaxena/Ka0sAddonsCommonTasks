# Resume: full skinning

A fresh session picks up from any point with this file.

0. **Prerequisite.** Everything on `feat/2026-10-31-findings-remediation` merged, with v1.84.0 pushed. Check: `git -C ../../../LibKa0s ls-remote --tags origin v1.84.0` prints a line and that branch is gone from origin. If not, finish it first: the owner gave the go-ahead on 2026-11-01. Order is WowAddonStandards, LibKa0s (push v1.82.0 is done, push v1.84.0), LibKa0sSkinTester, addons, Ka0sAddonsCommonTasks; `--no-ff`, gate on the merge, delete the remote branch first. In DpsRace also delete `feat/2026-10-31-dpsrace-bar-styling` and `feat/2026-10-31-dpsrace-test-live-parity`. Close LibKa0s #59, #66, #67, #68, #69, #73, ConsumableMaster #42, #43 and MultiMeters #54, spaced at least 20 s apart.
1. **State.** `./resume-state.sh`. Git is the only state.
2. **Interrupted item.** Read `git status` and the diff in the owning repo; finish it or `git stash push -m "<ID> interrupted"`. Never reset unread work.
3. **Relaunch.** Branch `feat/2026-11-01-full-skinning` from master in each repo, created in the checkout the game loads. M1 in id order, one agent at a time in LibKa0s. M2 only after M1's checkpoint, one agent per addon, each skipping landed ids. Rulings are in `00_PLAN.md`; causes in `inputs/SKIN_CAUSES.md`.
4. **Checkpoint.** At each milestone: gates green, then push branches and `refs/notes/ka0s-review`, append `checkpoints.tsv`, commit it here and push. Tag v1.85.0 stays local.
5. **Stop.** Do not merge this run; the owner smokes it first. A full client restart is needed if files were added.
