# Automated-tests sweep: execution record (2026-09-26)

Every item in the fix queue (`00_FIX_QUEUE.md`, ATS-01..24) landed on
`feat/2026-09-26-automated-tests-sweep`, and the collection-wide battery was then re-run. Status
comes from git (`./resume-state.sh`). The milestone evidence is in `checkpoints.tsv`, and the raw
workflow results are in `plan-data/runs/`.

## Outcome by queue item

| Queue | Outcome | Commit(s) |
|---|---|---|
| ATS-01 CM perf `recompute` | **Not a regression.** A bisect put the step at b19e9bb (DR-CM-03). With GC stopped, a recompute allocates the same amount across the whole range. The figure is garbage from more loaded code that is still uncollected when the loop ends. Recorded in `docs/performance.md`. | CM dffb7fe |
| ATS-02 AM perf `compile`/`applyPass` | **Fixed.** The cause was d0c01f1 (SID-16): `categorizedUnion` was built on every compile. It is now built only when the Hide gate needs it. compile went 42424 → 3576 B/iter and applyPass 164883 → 104403. Plan signatures are byte-identical across 1280 plans. | AM 9134abd |
| ATS-03 LibKa0s shelf-life ×6 | **Fixed.** Every file that had been Accepted since v1.56 was peeled or split. `Options.lua` went 1462 → 1261 (+`OptionsRegistry.lua`), `OptionsTabs.lua` 1493 → 1293 (+`OptionsCombat.lua`) and `testkit/framework.lua` 1386 → 920 (+`inventory.lua`). The four test suites are each below 1000. | LK 2061be6, fad47e9, fa2fa13, db458f8 |
| ATS-04 LibKa0s over cap (#32, #33) | **Fixed; the census is empty.** `OptionsWidgets.lua` went 3852 → 1422, with the id surface moved to `OptionsIds.lua` (1358) and `OptionsIdList.lua` (1193); the title said one file, but the surface could not fit under the cap as one. `test_options_widgets.lua` went 4086 → 717 and is now spread over 7 suites. The case count is unchanged. | LK 3d39ae7, 304c2d8 |
| ATS-05 PM `test_panel.lua` 1491 | Split, 721 + 780 | PM 9bfd6a8 |
| ATS-06 LK `OptionsTabs.lua`, `test_widgets.lua` 1493 | Peeled or split (see ATS-03) | LK fad47e9, db458f8 |
| ATS-07 LK `testkit/test_prose.lua` 1486 | Split below 1000 | LK b515211 |
| ATS-08 AM `test_anchors.lua` 1481 | Split, 815 + 645 | AM 42502cf |
| ATS-09 AM `GeneralSpells.lua` 1480 | Peeled, 984 + `GeneralUserCategories.lua` 550 | AM d4bdf77 (+R) |
| ATS-10 PM `PanelEditor.lua` 1464 (#47) | Peeled, 746 + `PanelEditorTabs.lua` 798 | PM 5119ae1 |
| ATS-11 AT `test_helpers.lua` 1447 (R-14) | Split, 573 + 894 | AT fb55f44 |
| ATS-12 MM `test_slash`, `Row`, `Aggregator` | 1411 → 834, 1446 → 1226, 1432 → 1230 | MM a2ee920, 1399354, 8cfd57a |
| ATS-13 KC `Castbar.lua` 1440 (#24) | Peeled, 1217 + `Castbar_Events.lua` 270 | KC 99211f0 |
| ATS-14 CM three suites | 1426 → 940, 1425 → 713, 1419 → 972 | CM 1717d98 |
| ATS-15 AM `Anchors.lua` 1243 | Peeled, 890 + `Anchors_Attach.lua` 392 | AM e0b0e9c (+R ×3) |
| ATS-16 WG `NS.FrameSnapshot` CCN 15 | 15 → 9 using shape 2 (named helper), with a characterization test first | WG a6e144b |
| ATS-17 MM `doDebug` CCN 15 | 15 → 11 using shape 2 (`doDebugTooltip`) | MM f53ca7a |
| ATS-18 AM three at CCN 15 | `steadyRelative` 15 → 7 using shape 3 (data tables), with a test first. **`standUp` and `ContainerClass:ApplyHang` are left at 15:** no permitted shape applies honestly (anti-pattern #52). The reason is recorded in the commit. | AM 8f7fcfb |
| ATS-19 lizard length/param thresholds | **Kept as designed** (owner's ruling). See `exceptions.tsv`. | none |
| ATS-20 empty table without `None.` | Fixed in the kit (revision 30) and re-vendored everywhere | LK a2a53aa |
| ATS-21 generated files in the band table | Fixed in the kit (revision 31) and re-vendored everywhere. PrettyChat's over-cap count went 1 → 0. | LK 17d72bc |
| ATS-22 hook and subagent write path | The hook now reads command position only (heredoc bodies and quoted prose pass). The skill now names a scratchpad + `cp` route and a unique log path. | WA 7c8f467, 8cf07ce |
| ATS-23 stale Disposition cells | Refreshed in every M3 run | all `*-ATS-99` |
| ATS-24 BL `test_libka0s.lua` 1020 | Split, 676 + 391. The provisional Accepted is gone. | BL d67564c |

LibKa0s **v1.62.0** is the release that carries these changes (5dc9f5d). Its tag is **local only**, and all
eleven addons re-vendored from it (`<P>-ATS-RV`).

## Final runs (M3)

| Repo | Bundle | Tests | Lint files | Perf | Max CCN | Band (was) | Over cap |
|---|---|---|---|---|---|---|---|
| AbsorbTracker | 20260926-193105 | 810 | 67 | 6 pass | 14 | 2 (3) | 0 |
| AuraMaster | 20260926-193601 | 1661 | 144 | 11 pass | 15 | 9 (12) | 0 |
| BankLedger | 20260926-193102 | 1104 | 76 | skip (§12) | 15 | 4 (5) | 0 |
| ConsumableMaster | 20260926-193121 | 1112 | 126 | 5 pass | 14 | 5 (8) | 0 |
| KickCD | 20260926-193108 | 1201 | 112 | 6 pass | 15 | 9 (9) | 0 |
| LibKa0s | 20260926-193105 | 1747 + 1 skip | 122 | skip | 15 | 10 (13) | **0 (2)** |
| LootHistory | 20260926-193103 | 961 | 70 | skip (§12) | 15 | 6 (6) | 0 |
| MultiMeters | 20260926-193124 | 2092 | 144 | 17 pass | 15 | 22 (23) | 0 |
| PanelMaster | 20260926-193106 | 964 | 66 | skip | 15 | 3 (5) | 0 |
| PartyFrameEnhanced | 20260926-193107 | 383 | 75 | 9 pass | 14 | 0 (0) | 0 |
| PrettyChat | 20260926-193107 | 518 | 51 | skip (§12) | 14 | 2 (2) | **0 (1)** |
| WhatGroup | 20260926-193120 | 824 | 54 | 8 pass | 13 | 3 (3) | 0 |

All twelve verdicts are **green**, and every figure was verified against its own artifacts by an independent agent.
No function is above CCN 15 and no authored file is over the cap anywhere in the collection.

## Process notes

- **Reviews:** every M1/M2 item has a `refs/notes/ka0s-review` note. The one exception to "independent": after
  AM-ATS-04 failed a third review round on four stale comment citations, the orchestrator fixed them itself
  (4bfdd89, comment-only) and wrote the note.
- **The installed plugin still has the old hook.** WA-ATS-01's fix reaches sessions only after the merge and
  `/reload-plugins`, so M3 agents still hit the heredoc block and used the scratchpad + `cp` route.
- **`resume-state.sh` is a zsh script.** Several agents ran it with `bash` and hit a syntax error, then checked
  git directly. Run it as `./resume-state.sh`.
- **Left for later, not queued:** stale line-number comment citations into the vendored `OptionsWidgets.lua` in
  about 15 AuraMaster host comments (listed in its `docs/revendor/2026-09-26-v1.62.0/05_SUMMARY.md`), and a
  handful of pre-existing comment nits raised by reviewers. M4's sync-docs pass is where they belong.

## Still the owner's

- M4: sync-docs, then `/wow-addon:finalize` (the merge), which the owner asked for as the final step.
- Pushing the LibKa0s `v1.62.0` tag, and any addon version bump or release.
- In-client smoke checks. The peels are moves with no intended behavior change, but none has been exercised
  in the client.
