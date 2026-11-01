# Resume: full skinning

A fresh session picks up from any point with this file.

0. **Prerequisite.** Everything on `feat/2026-10-31-findings-remediation` merged, with v1.84.0 pushed. Check: `git -C ../../../LibKa0s ls-remote --tags origin v1.84.0` prints a line and that branch is gone from origin. If not, finish it first: the owner gave the go-ahead on 2026-11-01. Order is WowAddonStandards, LibKa0s (push v1.82.0 is done, push v1.84.0), LibKa0sSkinTester, addons, Ka0sAddonsCommonTasks; `--no-ff`, gate on the merge, delete the remote branch first. In DpsRace also delete `feat/2026-10-31-dpsrace-bar-styling` and `feat/2026-10-31-dpsrace-test-live-parity`. Close LibKa0s #59, #66, #67, #68, #69, #73, ConsumableMaster #42, #43 and MultiMeters #54, spaced at least 20 s apart.
1. **State.** `./resume-state.sh`. Git is the only state.
2. **Interrupted item.** Read `git status` and the diff in the owning repo; finish it or `git stash push -m "<ID> interrupted"`. Never reset unread work.
3. **Relaunch.** Branch `feat/2026-11-01-full-skinning` from master in each repo, created in the checkout the game loads. M1 in id order, one agent at a time in LibKa0s. M2 only after M1's checkpoint, one agent per addon, each skipping landed ids. Rulings are in `00_PLAN.md`; causes in `inputs/SKIN_CAUSES.md`.
4. **Checkpoint.** At each milestone: gates green, then push branches and `refs/notes/ka0s-review`, append `checkpoints.tsv`, commit it here and push. Tag v1.85.0 stays local.
5. **Stop.** Do not merge this run; the owner smokes it first. A full client restart is needed if files were added.

## Where it stopped, 2026-11-01

The owner restarted the PC during M1's independent review. Landed and pushed: FS-L1 to FS-L9, FS-D1, FS-T1, FS-A4 (LibKa0s `fd5635f`). Not done: the review, any repairs, FS-REL.

To continue: `./resume-state.sh`, check LibKa0s is clean on the branch, then rerun M1. The persisted script is `~/.claude/projects/-mnt-d-Profile-Users-Tushar-Documents-GIT-Ka0sAddonsCommonTasks/81d18148-7543-4f61-b2a2-70352f1a0364/workflows/scripts/full-skinning-m1-library-wf_b51f4cb6-19e.js`, run `wf_b51f4cb6-19e`: resume with `resumeFromRunId` in the same session, where the 12 items replay from cache and only the review onward runs live. In a new session, rerun the review and release stages by hand from that script. Its item agents skip landed ids. Then M2, M3 and M4 per `00_PLAN.md`; the owner smokes before any merge.
