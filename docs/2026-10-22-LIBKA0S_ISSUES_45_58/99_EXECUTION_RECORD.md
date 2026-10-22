# 99 — Execution record: LibKa0s issues #45-#58

Written during execution. The plan files are frozen; later developments are recorded here.

## LK-11 spike outcome: B (W.StepPanel is Sim-private)

- **Outcome: B.** `W.StepPanel` is **not** public. LK-10's payload (`07dfb7c`) is reverted inside the
  LK-11 commit: `WidgetsStepPanel.lua`, `tests/test_widgets_step_panel.lua`, its majors/xml rows, its
  CHANGELOG section and the Widgets key rename all leave, and the Widgets key is back to 13.1.4.3.2.
  Proof: `test ! -f LibKa0s/WidgetsStepPanel.lua` (in `../LibKa0s`). LK-10 is noted in `exceptions.tsv`.
- **Why.** Rebuilding `PerfPanel.lua` on `W.StepPanel` would have needed edits to five existing suite
  cases: `tests/test_perf_command.lua:279` and `tests/test_perf_isolation.lua:264`, `:272`, `:277`
  load `PerfPanel.lua` without Widgets, and `tests/test_resize_windows.lua:432` caught
  `WidgetsStepPanel.lua` calling `core.MakeResizable` unguarded. The proof required zero test edits.
- **What LK-11 shipped.** `PerfPanel.lua` gains one header comment naming the deliberate duplication
  with Sim's private renderer; `PANEL_MINOR` 6 -> 7 (comment-only); Perf key 15.1.1.6 -> 15.1.1.7
  (15.1.1.6 Superseded).
- **Downstream.** LK-16, LK-18, LK-20, WS-08, WS-09, DW-04 and DC-* take the outcome-B branch.
  LK-16 builds the renderer library-private inside `SimPanel.lua` from
  `git show 07dfb7c:LibKa0s/WidgetsStepPanel.lua`, and must guard `core.MakeResizable`.

## The first M1 attempt stopped at LK-11 (2026-10-22)

The first executor run (`wf_d04aa10e-280`) landed 18 items. The spike ran and found outcome B, but the
auto-mode permission classifier refused the implementer's `git revert --no-commit 07dfb7c` as a deletion,
so LK-11 returned `blocked` and its 19 dependants were skipped. The lead staged that revert on the run
branch and relaunched the 20 remaining items (`wf_92e45e7b-e9b`), with an item ruling telling LK-11 not
to re-run the spike. All 20 landed.

## The local tag v1.75.0

| When | Event | Commit |
|---|---|---|
| 2026-10-22 (LK-22) | created, local annotated tag, not pushed | `265a89e` |
| 2026-10-22 21:31 (LK-26) | moved `265a89e` -> `6bf5f3e` (Sim minor 2, SimTimeline minor 2; key 2.2.1). Re-gated with `run-automated-tests.sh --no-bundle`: lint 0/0 in 180 files, 2538 passed/0 failed/2 skipped, complexity pass with max CCN 15, verdict green. As with v1.56.0's re-cut, no new release bundle: the frozen 20261022-155222 record describes `2df9193`. Not pushed. | `6bf5f3e` |
| 2026-10-22 23:32 (LK-27) | moved `6bf5f3e` -> `9e5c4e2` (SimPanel minor 2; Sim key 2.2.2). Re-gated with `run-automated-tests.sh --no-bundle`: lint 0/0 in 180 files, 2545 passed/0 failed/2 skipped, complexity pass with max CCN 15, verdict green. No new release bundle. Not pushed. | `9e5c4e2` |

## dev-copilot merged early (owner go-ahead, 2026-10-22)

The installed plugin updates from GitHub `master`, so 2.4.0 had to reach master before M2. On the owner's
explicit go-ahead, dev-copilot's run branch alone was merged `--no-ff` into master as `43dd69b` and pushed,
with no tag. The run branch stays until CT-02 cleans up. CT-02 finds dev-copilot already merged.

## M3 first pass: a Sim-1.0 gap from DW-02 (addendum 01)

The first M3 run (`wf_63c70dcf-91d`) landed 37 items. DW-02, DropWatcher's move onto Sim-1.0, returned
`library_gap`, and its 21 dependants were skipped. Sim minor 1 had two gaps:
- it froze the scenario names at `New`, while DropWatcher fills them after `New` at load;
- `Start` handed `prepare` a fresh `{ scenario, size, seed }`, dropping the host's `band` and `classFilter`.

Following RESUME §5, `plan-data/addendum-01.json` (and `.tsv`) adds:
- **LK-26**, Sim minor 2, the additive fix;
- **DW-RV2, LH-RV2 and BL-RV2**, which refresh the three simulator hosts from the moved tag.

The other eleven addons refresh once at the end of M3, after the tag stops moving. `resume-state.sh`,
`next_args.py` and `execute_milestone.js` now read `plan-data/addendum-*`.

## M3 second pass: a SimPanel gap from DW-04 (addendum 02)

The second M3 run (`wf_f6fb71d2-bd9`) landed DW-RV2, LH-RV2, BL-RV2, DW-02 (`58b84d3`, `a6d88f3`) and DW-03
(`fb2ddbe`). DW-04 returned `library_gap`: SimPanel minor 1 reads the picker's first scenario once, at
`Sim:New`, so a host that fills its scenarios after `New` gets "Start: nil". DW-04's finished work waits in
DropWatcher's `stash@{0}` ("DW-04 partial ..."). Its 12 dependants were skipped.

`plan-data/addendum-02.json` (and `.tsv`) adds:
- **LK-27**, SimPanel minor 2, together with a required audit of every Sim-1.0 value captured at `New`;
- **DW-RV3, LH-RV3 and BL-RV3**, which refresh the three simulator hosts again.

The other eleven addons now refresh in addendum 03.

## Owner go-ahead to merge (2026-10-22)

The owner wrote: "go ahead with whatever commits, merges and pushes you need to do - dont wait for my
approval for this conversation. Treat this message as approval to merge for this plan". CT-02 therefore
proceeds without a further stop. Addon version bumps stay out, since the plan has none.

## LH-11 deviation: hook order in the drivers (review, 2026-10-23)

The LH-11 item text (req-lh-sim §2.3, "Hooks") says a hook is played "after applying the hooked function's
effect to the world". LootHistory's drivers (`modules/SimDrivers.lua`, commit `c98eb56`) do not follow
that uniformly, and the item commit did not list it as a deviation:
- **Hook first, then the effect** (the post-hook sees the pre-call world, as the client's own post-hook
  does): `D.UseItem`, `D.Destroy`, `D.TakeMailItem`, `D.AutoLootMail`, `D.TakeMailMoney`, `D.Send`,
  `D.Post`, `D.Craft` and `D.QuestReward`. This order is required: OnPost's `ItemLocationID` and
  OnContainerItemUse's `ContainerItemHasLoot` read the slot as it was before the call. Pinned by
  `tests/test_sim_drivers.lua` ("a hook driver shows the client's pre-call world to the post-hook").
- **Effect first, then the hook**: `D.Buy`, `D.Buyback`, `D.Repair` and `D.AuctionBuy`, the order the
  binding text names. Pinned by the `MUTATES` table in the same file.

The binding text is wrong for the first group: applying the effect first would break the capture the
simulator exists to drive. Recorded here rather than changed; the LH-11 review commit cites it.

## The executor runs

| Run | What it carried | Outcome |
|---|---|---|
| `wf_d04aa10e-280` | M1, first attempt | 18 landed; stopped at LK-11 (see above) |
| `wf_92e45e7b-e9b` | M1, the 20 remaining items | 20 landed; M1 checkpoint 38/38 |
| `wf_8ebcc8dc-0a6` | M2, the fourteen `<PFX>-RV` re-vendors from `265a89e` | 14 landed; M2 checkpoint 14/14 |
| `wf_63c70dcf-91d` | M3, first pass | 37 landed; DW-02 returned `library_gap` (Sim minor 1), 21 dependants skipped |
| `wf_5cc3bea9-cf4` | LK-26 (addendum 01) | landed as `6bf5f3e`; tag moved `265a89e` -> `6bf5f3e` |
| `wf_f6fb71d2-bd9` | M3, second pass (addendum 01) | DW-RV2, LH-RV2, BL-RV2, DW-02, DW-03 landed; DW-04 returned `library_gap` (SimPanel minor 1), 12 dependants skipped |
| `wf_efa9de70-723` | LK-27 (addendum 02) | landed as `85e4f74` + review fix `9e5c4e2`; tag moved `6bf5f3e` -> `9e5c4e2` |
| `wf_c8ff2435-fbb` | M3, third pass (addendum 02) | 23 landed, 0 failed: DW-RV3, LH-RV3, BL-RV3, DW-04..09, DW-12, LH-10..15, BL-08..14 |
| addendum-03 run | AT/AM/CM/KC/MM/PM/PF/PG/PC/QC/WG-RV2 from the final tag `9e5c4e2`, then LK-23 and CT-01 | the eleven RV2 refreshes and LK-23 landed; M3 78/78 |

The addendum-03 run is the one this record is written in, so its run id is not known from inside it.
DW-04's stashed partial work (DropWatcher `stash@{0}`, "DW-04 partial ...") was continued by the third
pass; CT-02 checks `git stash list` in every repo and drops what this run created.

## What landed, per milestone

- **M1 (38/38), upstream.** WowAddonStandards v2.86.0 (WS-01..11, head `bb4e378`); LibKa0s LK-01..22
  (LK-10's payload withdrawn by LK-11 outcome B, see `exceptions.tsv`), local tag v1.75.0 at `265a89e`;
  dev-copilot 2.4.0 (DC-01..04, head `8c562da`, merged early as `43dd69b`). Checkpoint pushed.
- **M2 (14/14), re-vendor.** Every roster addon re-vendored v1.75.0 (kit 41), declared its LibKa0s icons
  and pruned `media/icons/` to them. Checkpoint pushed.
- **M3 (78/78), adoption.** The planned adoption items (Glow in DW/KC/QC; Sim-1.0 in DW, LH, BL; SearchBox
  in LH/BL/DW; TestStrip in DW/LH/BL/MM; BonusIDsFromLink in BL/LH; key bindings and the preview-mode
  marker; the standards-reference refresh per addon), plus the 19 addendum items: LK-26, LK-27, DW/LH/BL-RV2,
  DW/LH/BL-RV3 and the eleven RV2 refreshes of addendum 03. PC-01, PG-01, PM-01, AT-01, CM-01 and QC-04
  landed with no commit (`exceptions.tsv`). The M3 checkpoint row is the lead's, not this record's.
- **M4 (so far).** LK-23 (`a0d7be5`): CONSUMERS.md stamped v1.75.0 across the fourteen roster addons
  (492 exports across seventeen majors: 287 consumed, 82 thin, 123 zero), and releasing.md's step-9 sweep
  and step-8 paragraph advanced to v1.75.0. The census tool's raw output, hand verdicts and patched
  tool/renderer copies are in `plan-data/census-v1.75.0/`, committed here with CT-01 (LK-23 is a LibKa0s
  item and could not commit in this repo). CT-01 is this record.

## Vendored payload refreshes after the tag moved

| Tag position | Refreshed by | Changed files |
|---|---|---|
| `265a89e` -> `6bf5f3e` (LK-26) | DW-RV2, LH-RV2, BL-RV2 | `Sim.lua` (minor 1 -> 2), `SimTimeline.lua` (1 -> 2) |
| `6bf5f3e` -> `9e5c4e2` (LK-27) | DW-RV3, LH-RV3, BL-RV3 | `SimPanel.lua` (1 -> 2) |
| `265a89e` -> `9e5c4e2` (final) | AT, AM, CM, KC, MM, PM, PF, PG, PC, QC, WG-RV2 | `Sim.lua`, `SimTimeline.lua`, `SimPanel.lua` (each 1 -> 2) |

Each refresh copied both payloads whole from `git archive v1.75.0`, re-ran the tag's `prune-icons.lua`
against the unchanged `LibKa0s icons:` line, kept the provenance line at v1.75.0 (kit revision 41
unchanged) and recorded itself in a new `docs/revendor/2026-10-22-v1.75.0/0N_REFRESH.md`, leaving the
frozen files before it alone. No addon version was bumped.

## Test totals at the end of M3 (re-run for CT-01, 2026-10-23)

Re-run on each run-branch head with `ka0s-bounded` (`lua5.1` for ConsumableMaster, `lua` elsewhere).
Every repo: 0 failed, luacheck 0 warnings / 0 errors. Not yet pushed: every head below except
WowAddonStandards and dev-copilot is ahead of its pushed M2 branch.

| Repo | Head | Tests (passed / failed / skipped) | luacheck files |
|---|---|---|---|
| LibKa0s | `a0d7be5` (tag v1.75.0 = `9e5c4e2`, local) | 2545 / 0 / 2 | 180 |
| AbsorbTracker | `90b4b9b` | 885 / 0 / 1 | 70 |
| AuraMaster | `4b4393c` | 2127 / 0 / 1 | 178 |
| BankLedger | `fff558a` | 1411 / 0 / 1 | 103 |
| ConsumableMaster | `ddda153` | 1217 / 0 / 1 | 130 |
| DropWatcher | `595b325` | 1678 / 0 / 1 | 193 |
| KickCD | `920640f` | 1335 / 0 / 1 | 129 |
| LootHistory | `e0716cf` | 1685 / 0 / 1 | 138 |
| MultiMeters | `7e84ab3` | 2210 / 0 / 1 | 146 |
| PanelMaster | `45add34` | 1064 / 0 / 1 | 71 |
| PartyFrameEnhanced | `fc4105b` | 469 / 0 / 1 | 79 |
| PremadeGroupsFilterExtension | `3975ef6` | 422 / 0 / 1 | 60 |
| PrettyChat | `7b6d914` | 574 / 0 / 1 | 56 |
| QuickComms | `ef38fd2` | 1102 / 0 / 1 | 135 |
| WhatGroup | `e6b5d13` | 942 / 0 / 1 | 59 |

WowAddonStandards (`bb4e378`, v2.86.0) and dev-copilot (`8c562da`, 2.4.0) have not moved since the M1
checkpoint, whose evidence row in `checkpoints.tsv` holds their gate results.

## Deviations, collected

- **LK-10 / LK-11:** outcome B; LK-10's payload withdrawn (above; `exceptions.tsv`).
- **First M1 attempt:** the permission classifier refused LK-11's `git revert`; the lead staged it (above).
- **dev-copilot merged early** on the owner's go-ahead, so `bases.tsv` pins its pre-merge base (above).
- **Two library gaps in M3:** DW-02 (Sim minor 1) and DW-04 (SimPanel minor 1) each needed an addendum and
  a tag move, and the eleven non-Sim hosts refreshed once from the final tag in addendum 03 (above).
- **No-commit items:** PC-01, PG-01, PM-01, AT-01, CM-01, QC-04 (`exceptions.tsv`, each with its proof).
- **LH-11:** driver hook order differs from the item text for nine drivers (above).
- **LK-23:** W.StepPanel has no census row (outcome B: its descriptor fields appear under Sim), and
  O.__releaseChrome never had a CONSUMERS.md row to remove (LK-23 commit body).
- **Smoke file:** SM-LK-1..3 are "outcome A only" and do not apply; SM-LK-4's expected minors are now
  Sim 2, SimTimeline 2, SimPanel 2; the AuraMaster section reuses the id SM-AM-1 for AM-01's check. All stay
  `owed`; see the note at the end of `06_SMOKE_TESTS.md`.

## Smoke tests

Every SM-* check in `06_SMOKE_TESTS.md` is `owed`. The owner runs them in game; no agent marks one passed.

## CT-02: finalize (2026-10-23)

The merges ran on the owner's go-ahead. Order:
1. WowAddonStandards (`db00f05`).
2. LibKa0s (`3b22193`). The `v1.75.0` tag was then pushed: tag object `d0ad7d8`, peeling to `9e5c4e2`.
3. dev-copilot, which was already merged as `43dd69b`; only its branch was deleted.
4. The fourteen addons:

| Addon | Default branch | Merge |
|---|---|---|
| AbsorbTracker | master | `b8d2763` |
| AuraMaster | master | `397cd77` |
| BankLedger | master | `6ba6c64` |
| ConsumableMaster | master | `d416cce` |
| DropWatcher | master | `53f6670` |
| KickCD | master | `e6000ec` |
| LootHistory | master | `09567b2` |
| MultiMeters | master | `eeb9d05` |
| PanelMaster | master | `78251cf` |
| PartyFrameEnhanced | master | `2a76b7d` |
| PremadeGroupsFilterExtension | main | `9a47ba7` |
| PrettyChat | master | `de96776` |
| QuickComms | master (as detected) | `f44d9a1` |
| WhatGroup | master | `fc24af3` |

5. This repo, last.

Every merge was `--no-ff` and was gated again on the merge result: tests 0 failed and luacheck 0/0 in every repo. WowAddonStandards was gated with `check-standard.sh`, all checks passing.

Before merging, a content-only `/dev-copilot:sync-docs` ran in each repo. It committed in five of them: LibKa0s `ba14d7e`, AbsorbTracker `19f6b65`, MultiMeters `570ab08`, BankLedger `d77a0c6` and LootHistory `02cbdae`. Proposals it left for the owner:
- `testkit/README.md` still says "eleven consumers". Changing it needs a kit revision and a re-vendor.
- Historical comment citations in AbsorbTracker were left for confirmation.

The workflow agents' permission classifier refused merges and pushes, so the lead ran every git write. Every run branch is deleted locally and on origin. No run stash or extra worktree remains; DropWatcher's DW-04 stash was dropped by DW-04 after its commit.

The GitHub closure items (WS-12, LK-24, BL-15, DW-11, KC-02, MM-03, WG-02, LH-16, PG-02) are recorded in `exceptions.tsv`. Addon versions were not bumped. Every in-game smoke check in `06_SMOKE_TESTS.md` is still owed by the owner.
