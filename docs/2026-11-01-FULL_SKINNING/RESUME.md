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

## Where it stands, 2026-11-01, afternoon

M1 passed and is pushed (`checkpoints.tsv`), but v1.85.0 is being re-cut locally before the fan-out. The AbsorbTracker pilot of M2 landed FS-AT-RV, FLIP, FIX and REC and showed library gaps: no gloss primitive, shadows need a font object on a 12.0.7 client, and the record row must be exempt from every Defaults button. These go in LibKa0s as `FS-FIX`, the tag is re-cut, AbsorbTracker moves onto them, then the other 15 addons run, one agent plus an independent review per addon. Nothing past M1 is pushed.

The M2 script is `~/.claude/projects/-mnt-d-Profile-Users-Tushar-Documents-GIT-Ka0sAddonsCommonTasks/d3552dd5-7156-418f-9b72-44be07f9b377/workflows/scripts/full-skinning-m2-addons-wf_dc0be42e-fc6.js`, with `args.addons` as `{repo, p, short}` rows; p is the item prefix, FS-<p>. Item agents skip landed ids.

DpsRace's branch already holds `09f02e7`, the owner's 42-dummy catalog, unrelated to skinning and carried on this branch at the lead's choice. Do not recreate that branch from master.

## Fan-out, 2026-11-01, 14:10

v1.85.0 stays local and is re-cut once more for Toast `d.soundFile` and the Moving-to fixes, then 14 addons run in `full-skinning-m2-fanout`. QuickComms is held out: its #13 and #14 build runs on this branch in its own workflow, and its FS-QC items run after that, through the M2 script with `{repo:"QuickComms",p:"QC",short:"QC"}`. Its #13 rulings are in its `docs/superpowers/specs/2026-11-01-open-close-animations-design.md`.

## M3 from here, 2026-11-01, 17:00

M2 is pushed. Owner's rulings on the triage, 2026-11-01: each skin gets its own values for bar background, bar border, icon border and glow, with Ka0s Default unchanged; a skin's None bar border style defers to the player's Show border and stored style, and a real style in a skin wins; the KC, AM and DW migration overrides are accepted; the Ka0s Default look moves stay, named on the smoke list. M3 adds the library gaps of that triage, re-cuts local v1.85.0, adds a per-addon `FS-<p>-GATE` commit (re-vendor, adoption, kit check, allow-list, leftovers) to every addon, then FS-WS, FS-GATE, FS-REPORT.
