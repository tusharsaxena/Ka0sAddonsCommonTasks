# 04 — Execution plan: item tables

Generated from `plan-data/items.json` by the session lead; the full spec of each item is in that file
(`python3 -c "import json;print([i for i in json.load(open('plan-data/items.json'))['items'] if i['id']=='LK-13'][0]['spec'])"`).
How the run executes, checkpoints and resumes: `00_OVERVIEW.md` §4 and `RESUME.md`.

## M1 — Upstream: WowAddonStandards v2.86.0, LibKa0s v1.75.0 (local tag), dev-copilot 2.4.0

| id | repo | effort | depends on | title |
|---|---|---|---|---|
| WS-01 | WowAddonStandards | M | — | Open v2.86.0 and land library-stack-§7's narrowed `__` clause (precondition for OptionsTabs minor 9) |
| WS-02 | WowAddonStandards | L | WS-01 | launcher-§6 (MUST): the Show window key binding on the toggle handler; layout-§1 Bindings.xml generalized; slash-commands-§7 key press; anti-pattern #96; playbook and pack ripple |
| WS-03 | WowAddonStandards | M | LK-07, WS-01, WS-02 | preview-mode: the explicit test mode says so on the display (MUST); standalone-windows: Widgets.TestStrip SHOULD for a filter-bar window; anti-pattern #97 |
| WS-04 | WowAddonStandards | S | WS-01 | documentation-§1 item 12: Game-icons credit MUST and MIT-set credit SHOULD for the LibKa0s icon sets an addon ships |
| WS-05 | WowAddonStandards | M | LK-05, WS-01 | automated-tests-§3: a crashed or bounded lizard run is not a complexity pass (clarification); the hazard row split by line shape; anti-pattern #92; AUTOMATED_TESTS.md and playbook ripple |
| WS-06 | WowAddonStandards | M | LK-07, LK-08, LK-09, WS-01 | library-stack: §2 LibCustomGlow-1.0 row; §7 module table gains LibKa0s-Glow-1.0, Item.BonusIDsFromLink, Widgets SearchBox and TestStrip; Glow and Sim adoption is required of none |
| WS-07 | WowAddonStandards | M | LK-16, WS-01, WS-03, WS-06 | preview-mode: the in-game simulator (MAY to ship, MUST build on LibKa0s-Sim-1.0 if shipped) and its host contract; compat sentence; #97 gains the unmarked session |
| WS-08 | WowAddonStandards | M | LK-11, LK-16, WS-01, WS-06, WS-07 | library-stack-§7: the LibKa0s-Sim-1.0 row, StepPanel (public or Sim-private per the PerfPanel spike), the recounted majors/files and inter-module edges, and the count ripple |
| WS-09 | WowAddonStandards | S | WS-08 | library-stack-§7: the library-drawn icon set is closed at close, copy, clear, info (MUST); anti-pattern #95 and playbook ripple |
| WS-10 | WowAddonStandards | S | WS-08 | open-evolutions: index the recorded rejections of LibKa0s#46-#58 with bar and re-check trigger; library-stack-§7 promotion pointer |
| WS-11 | WowAddonStandards | S | WS-02, WS-03, WS-04, WS-05, WS-06, WS-07, WS-08, WS-09, WS-10 | v2.86.0 landing pass: final changelog entry shape, date re-stamp, read-for-meaning cross-checks, M1 checkpoint gate |
| LK-01 | LibKa0s | S | WS-01 | #45 payload half: OptionsTabs minor 9 stops exporting the dead test seam O.__releaseChrome |
| LK-02 | LibKa0s | S | LK-01 | #57 C2: correct the stale 'install missing the art' comments, Core minor 11, DebugLog minor 20, OptionsIdList minor 5 (comment-only) |
| LK-03 | LibKa0s | S | — | Kit revision 41 (1/3): #45 kit half, Kit.__deviationRows and Kit.__declineFor are no longer exported |
| LK-04 | LibKa0s | M | LK-03 | Kit revision 41 (2/3): #46, a lizard crash or bound is a complexity fail with zeroed figures, never a pass |
| LK-05 | LibKa0s | M | LK-04 | Kit revision 41 (3/3): #47, a separate crashed bucket from a per-file retry that names the file; detector and shadow rewrite rejected |
| LK-06 | LibKa0s | M | — | Widgets minor 13 (1/2): W.SearchBox, the flat filter-bar search box in the dropdown's skin, with the gold focus line |
| LK-07 | LibKa0s | S | LK-06 | Widgets minor 13 (2/2): W.TestStrip, the test-mode strip, sharing the minor with SearchBox |
| LK-08 | LibKa0s | S | — | Item minor 3: Item.BonusIDsFromLink, with the rest of #51 recorded as rejected |
| LK-09 | LibKa0s | M | — | New major LibKa0s-Glow-1.0 (Glow minor 1): the stateless LibCustomGlow-1.0 driver |
| LK-10 | LibKa0s | M | LK-07 | W.StepPanel in new WidgetsStepPanel.lua (minor 1): the render-only clickable step panel |
| LK-11 | LibKa0s | M | LK-10 | Spike: rebuild PerfPanel on W.StepPanel; test_perf_panel.lua passes unedited -> StepPanel public (outcome A), else Sim-private (outcome B); record which |
| LK-12 | LibKa0s | M | LK-11 | New major LibKa0s-Sim-1.0 (1/5): Sim.lua and the Compat answer seam, Sim:NewSeam |
| LK-13 | LibKa0s | L | LK-12 | Sim-1.0 (2/5): the session, Sim:New, Start/Stop with guarded and cleanup phases, Fire, After, listeners |
| LK-14 | LibKa0s | L | LK-13 | Sim-1.0 (3/5): SimTimeline.lua, the step machine with the host gate, per-step delay and the internal RunTo |
| LK-15 | LibKa0s | M | LK-14 | Sim-1.0 (4/5): the verbs, sim:RunVerb with the generic grammar, host verbs, WHY lines, status and usage |
| LK-16 | LibKa0s | L | LK-15 | Sim-1.0 (5/5): SimPanel.lua, the docked step panel, picker and controls, session-only position |
| LK-17 | LibKa0s | M | LK-16 | Sim-1.0 contract tests: two-copy pairing isolation, the reference degradation stub with parity, and a DW-shaped mini host end to end |
| LK-18 | LibKa0s | M | LK-17 | Sim-1.0 API document completed: host contract H1-H10 with the C.4 rule, enforce/obligate table, stub shape, STRINGS, adopters |
| LK-19 | LibKa0s | S | LK-02, LK-09, LK-16 | DebugLogDiagnostics minor 3: the diagnostics header lists Glow and Sim, with a gate tying MAJORS to tests/majors.lua |
| LK-20 | LibKa0s | M | LK-05, LK-08, LK-18, LK-19, LK-25 | v1.75.0 repo-wide ripple: README, CLAUDE.md, DEPENDENCIES.md, adoption prompt, and the CHANGELOG block consolidated |
| LK-21 | LibKa0s | M | LK-20 | docs/releasing.md for v1.75.0: constants and counts, the icon-subset re-vendor steps with host-passed art, the attribution note, Consumers rows, 'Where v1.75.0 stands' |
| LK-22 | LibKa0s | M | LK-01, LK-02, LK-03, LK-04, LK-05, LK-06, LK-07, LK-08, LK-09, LK-10, LK-11, LK-12, LK-13, LK-14, LK-15, LK-16, LK-17, LK-18, LK-19, LK-20, LK-21, WS-11 | Release v1.75.0: dated block, pointers, release run with ANALYSIS.md, LOCAL annotated tag (never pushed; movable until finalize) |
| DC-01 | dev-copilot | M | LK-01, LK-21, WS-01, WS-04, WS-09 | wow-revendor-libka0s: LibKa0s icons: declaration, the tag's tools/prune-icons.lua prune, whole-catalog test blocker, icon-set README credits, dead __ stub mirrors, moved-local-tag refresh |
| DC-02 | dev-copilot | S | LK-05, WS-05 | Kit-41 crashed complexity bucket (crashedFiles) in bump-version, wow-automated-tests, the WoW review, the standards audit and finalize |
| DC-03 | dev-copilot | S | DC-01, WS-02, WS-04, WS-09 | Audit, sync-docs and new-addon learn the icon declaration, the pruned media/icons, icon-set credits and the launcher-§6 binding pointer |
| DC-04 | dev-copilot | S | DC-01, DC-02, DC-03, WS-11 | Release dev-copilot 2.4.0: plugin.json, CLAUDE.md version history, README standard v2.86.0, full gate; hand-off for the owner's plugin update before M2 |
| LK-25 | LibKa0s | S | LK-09 | Record the #49/#50/#51/#52/#56/#58 rejections in the API documents of the majors they would have joined |

## M2 — Re-vendor LibKa0s v1.75.0 into the 14 roster addons

| id | repo | effort | depends on | title |
|---|---|---|---|---|
| AT-RV | AbsorbTracker | M | DC-01, DC-04, LK-22, WS-04, WS-11 | Re-vendor LibKa0s v1.75.0 from the local tag: declare 'LibKa0s icons: clear, close, copy, help.', prune media/icons, exempt O.Drawer from Options parity, rewrite the whole-catalog and info.tga tests to the declaration, Open Iconic credit |
| AM-RV | AuraMaster | M | DC-01, DC-04, LK-22, WS-04, WS-09, WS-11 | Re-vendor LibKa0s v1.75.0 (kit 41) from the local tag: the LibKa0s icons: declaration (close, copy, clear, help, info) and prune, the Options-stub Drawer, the info-art test rewritten to the declaration, the Open Iconic credit |
| BL-RV | BankLedger | M | DC-01, DC-04, LK-22, WS-04, WS-11 | Re-vendor LibKa0s v1.75.0 (local tag): both payloads, provenance + 'LibKa0s icons:' line, prune, adoption blockers, Open Iconic credit |
| CM-RV | ConsumableMaster | M | DC-01, DC-04, LK-22, WS-04, WS-11 | Re-vendor LibKa0s v1.75.0 from the local tag: declare and prune icons (clear, close, copy, help, info, segment), kit 41, OptionsDrawer in the major inventory, Open Iconic credit |
| DW-RV | DropWatcher | M | DC-01, DC-04, LK-22, WS-04, WS-11 | Re-vendor LibKa0s v1.75.0 (kit 41) from the local tag; declare and prune the icons; Options stub Drawer parity and dead __releaseChrome mirror; Open Iconic credit; stale kit/payload mentions |
| KC-RV | KickCD | M | DC-01, DC-04, LK-22, WS-04, WS-11 | Re-vendor LibKa0s v1.75.0 (kit 41) from the local tag: icon declaration and prune, Options-stub Drawer, whole-catalog and info.tga tests rewritten to the declaration, Open Iconic credit, revendor bundle |
| LH-RV | LootHistory | L | DC-01, DC-04, LK-22, WS-04, WS-11 | Re-vendor LibKa0s v1.75.0 (local tag): both payloads, provenance paragraph split plus the LibKa0s icons: line, icon prune, every adoption blocker, README credits, docs/revendor bundle |
| MM-RV | MultiMeters | M | DC-01, DC-04, LK-22, WS-04, WS-09, WS-11 | Re-vendor LibKa0s v1.75.0 from the local tag: both payloads, provenance plus 'LibKa0s icons:' line, icon prune, Options-stub Drawer parity, icon tests rewritten to the declaration, Credits, revendor bundle |
| PM-RV | PanelMaster | M | DC-01, DC-04, LK-22, WS-11 | Re-vendor LibKa0s v1.75.0 (kit 41): declare `LibKa0s icons: clear, close, copy.`, prune, split the run-on provenance paragraph, Drawer stub parity, declaration-based icon tests, Open Iconic credit |
| PF-RV | PartyFrameEnhanced | M | DC-01, DC-04, LK-22, WS-04, WS-09, WS-11 | Re-vendor LibKa0s v1.75.0 (kit 41) from the local tag; declare `LibKa0s icons: clear, close, copy.`, prune, fix the Drawer parity and info.tga blockers, credit Open Iconic |
| PG-RV | PremadeGroupsFilterExtension | M | DC-01, DC-04, LK-22, WS-11 | Re-vendor LibKa0s v1.75.0 (kit 41) from the local tag: declare and prune icons to clear, close, copy; Options stub Drawer parity, drop the dead __releaseChrome mirror, credit Open Iconic by set; closes #25 |
| PC-RV | PrettyChat | M | DC-01, DC-04, LK-22, WS-04, WS-09, WS-11 | Re-vendor LibKa0s v1.75.0 from the local tag: both payloads whole, 'LibKa0s icons: clear, close, copy.' plus the prune, Options stub Drawer parity, dead __releaseChrome mirror removed, icon tests rewritten to the declaration, Open Iconic credit, bundle docs/revendor/<date>-v1.75.0 |
| QC-RV | QuickComms | M | DC-01, DC-04, LK-22, WS-04, WS-11 | Re-vendor LibKa0s v1.75.0 (kit 39 -> 41) from the local tag; declare `LibKa0s icons: all (icon browser).`; delete the dead H.__releaseChrome stub mirror; first docs/revendor bundle |
| WG-RV | WhatGroup | M | DC-01, DC-04, LK-22, WS-04, WS-09, WS-11 | Re-vendor LibKa0s v1.75.0 (kit 41) from the local tag: both payloads, provenance + 'LibKa0s icons: close, copy, clear.' line, prune, Options-stub Drawer parity, dead __releaseChrome stub, icon tests rewritten to the declaration, loader XML list, Open Iconic credit, docs/revendor bundle |

## M3 — Adoption and features in the addons (Sim on DropWatcher first, then new simulators in LootHistory and BankLedger)

| id | repo | effort | depends on | title |
|---|---|---|---|---|
| BL-01 | BankLedger | S | BL-RV | Util.WowheadURL reads its bonus ids through Item.BonusIDsFromLink; itemStringFields deleted; ItemSetup stub gains the member |
| BL-02 | BankLedger | S | BL-RV | Ledger filter bar: the item-name search box is W.SearchBox (gold focus line), through B:MakeSearchBox; MakeSearchMark retired or reduced |
| BL-03 | BankLedger | M | BL-RV, WS-03 | Test mode marked by W.TestStrip under the filter bar; panes reserve its height; the red badge kept and routed through L |
| BL-04 | BankLedger | M | BL-RV, WS-02 | launcher-§6: Show window key binding — root Bindings.xml CLICK BankLedgerToggleWindow, plain hidden button on the toggle verb, refusing while stood down |
| BL-05 | BankLedger | M | BL-RV | Sim prerequisite R1: one capture dispatch table L.HANDLERS + L:Dispatch; guild-bank hooks dispatch pseudo-events; behaviour unchanged |
| BL-06 | BankLedger | S | BL-RV | Sim prerequisite R2: player identity through NS.Compat (PlayerName, PlayerClass); three callers moved; compat-layer.md justifies them |
| BL-07 | BankLedger | M | BL-03 | Sim prerequisites R3-R5: Database:Sink write seam, SessionWindow prunes against the sink, one dataset predicate Database:DatasetKind (live/test/sim) |
| BL-08 | BankLedger | M | BL-05, BL-06, BL-07, LK-17, LK-18 | Sim seam: core/SimSetup.lua wraps NS.Compat via Sim:NewSeam straight after core/Compat.lua (LOAD-BEARING), guarded QueryGuildBankTab, degradation stub, Unwrapped() empty |
| BL-09 | BankLedger | L | BL-08 | Sim world: modules/SimWorld.lua — the session-only world model, real-item pool, identities, and a provider for every wrapped Compat key |
| BL-10 | BankLedger | L | BL-09 | Sim session host + drivers: modules/Sim.lua (Sim:New descriptor, refusals, two-phase stop, auto-stops, purge/test-mode exclusivity) and modules/SimDrivers.lua, with the 'bank' scenario |
| BL-11 | BankLedger | L | BL-10 | Sim scenarios: warband (held baseline), guild (issue #12 away-data), onesided; the host gate; the e2e acceptance suite |
| BL-12 | BankLedger | L | BL-11, BL-03, LK-16 | Sim surface: /bl sim feature verb via RunVerb, docked step panel (session-only position), simulation marker on the ledger and session windows, diagnostics sim section, debug-scan header |
| BL-13 | BankLedger | M | BL-12 | Simulator docs and smoke: README section, ARCHITECTURE sim paragraph, compat/schema/data-flow/performance pages, SIM theme in smoke-tests.md |
| BL-14 | BankLedger | S | WS-11, BL-13, BL-04, BL-02, BL-01 | Standards reference refresh to v2.86.0 (/dev-copilot:wow-revendor-standards) and a final read-for-meaning pass over the run's doc ripple |
| DW-01 | DropWatcher | M | DW-RV | Sim host-contract refactor (no library yet): deliver beside the live dispatcher honouring rejectedEvents, NS.SimHost split off NS.Sim, the direct Sim.active/Sim.delivering reads become calls |
| DW-02 | DropWatcher | L | DW-01, LK-12, LK-13, LK-14, LK-17 | Sim-1.0 contract proof (1/3): seam and session on LibKa0s-Sim-1.0 (core/SimSetup.lua, Sim:New descriptor, OnStopGuarded/OnStop, stub, Unwrapped) and the timeline driven by the library (prepare/play/scenarios); DW's step machine deleted |
| DW-03 | DropWatcher | M | DW-02, LK-15 | Sim-1.0 contract proof (2/3): /dw sim through sim:RunVerb; SimVerbs keeps only pull, kill, loot, lockdown and trade with their WHY codes, usage and status line |
| DW-04 | DropWatcher | M | DW-03, LK-11, LK-16 | Sim-1.0 contract proof (3/3): the step panel is the library's SimPanel; DW keeps only the d.panel fields; position session-only (migration 9 retires profile.simPanel); deviation row 301 deleted |
| DW-05 | DropWatcher | S | DW-04, WS-07, LK-18 | Simulator on Sim-1.0: doc and smoke ripple (ARCHITECTURE, design-readings, testing.md suite map, smoke SIM theme owed again) |
| DW-06 | DropWatcher | S | DW-05, LK-07, WS-03 | W.TestStrip: the test-mode banner is the library's strip (NS.MakeTestStrip seam); DW's own copy and its anchoring removed; compact two-line variant kept host-side |
| DW-07 | DropWatcher | S | DW-05, LK-06 | W.SearchBox: the filter bar's search box is the library's (NS.MakeSearchBox seam); flatSkin and lineColor deleted, FB.FLAT kept for CompactChrome |
| DW-08 | DropWatcher | S | DW-05, LK-09, WS-06 | LibKa0s-Glow-1.0: modules/Glow.lua drives LibCustomGlow through NS.GlowLib (core/GlowSetup.lua seam and stub); START/STOP/lib/num deleted |
| DW-09 | DropWatcher | M | DW-05, WS-02 | launcher-§6: the Show window key binding (root Bindings.xml, DropWatcherToggleWindow CLICK button on NS.ToggleWindow, refusal by hold), test_disabled step 8 extended |
| DW-10 | DropWatcher | S | DW-RV, LK-08, LK-25, WS-10 | Documented deviations re-checked at v1.75.0: rows for #49 (chat sender, tooltip reader, loot parser, restriction tracker) and #51 (item read) cite the recorded rejections and new triggers; #50 doc follow-up |
| KC-01 | KickCD | M | KC-RV, LK-09, WS-06 | Adopt LibKa0s-Glow-1.0: core/GlowSetup.lua seam (NS.GlowLib), IconGrid_Render's StopGlow/StartGlow drive the library, the local LCG START/STOP mapping deleted |
| LH-01 | LootHistory | S | LH-RV | options-ui-§19: the Price-sources host parks itself in the placeholder SimpleGroup's own OnRelease |
| LH-02 | LootHistory | S | LH-RV, LK-08 | Adopt Item.BonusIDsFromLink for the Wowhead export link; delete splitColons |
| LH-03 | LootHistory | M | LH-RV, LK-06 | Adopt W.SearchBox for the filter-bar item search (gold focus line), through an NS.MakeSearchBox seam |
| LH-04 | LootHistory | M | LH-RV, LK-07, WS-03 | Adopt W.TestStrip under the filter bar in test mode; the TEST MODE badge stays and goes through L |
| LH-05 | LootHistory | M | LH-RV, WS-02 | launcher-§6: the Show window key binding (CLICK LootHistoryToggleWindow), refusing by hold like the toggle |
| LH-06 | LootHistory | M | LH-RV | Sim host contract 1/4 (H1): route the simulator-relevant client reads and the read-side hooks through NS.Compat |
| LH-07 | LootHistory | L | LH-06 | Sim host contract 2/4 (H3): core/Dispatch.lua, one EVENT_ROWS and one HOOK_ROWS table with NS.Deliver/NS.DeliverHook, registration parity proven |
| LH-08 | LootHistory | M | LH-07 | Sim host contract 3/4: R:ResetState, Attribution:ResetContexts, NS.CancelDeferral(h) and NS.State.loginSettled |
| LH-09 | LootHistory | M | LH-08 | Sim host contract 4/4 (H4): one store accessor per capture store (history, holdings, daily) and the Reconciler coalescing read through Database:History |
| LH-10 | LootHistory | L | LH-09, LK-12, LK-13, LK-17, LK-18, LK-22 | Simulator 1/5: core/SimSeam.lua (Sim:NewSeam over NS.Compat, degradation stub) and modules/Sim.lua session host (refusals, start/stop phases, auto-stop, world-watch, test-mode exclusion) |
| LH-11 | LootHistory | L | LH-10 | Simulator 2/5: modules/SimWorld.lua (deterministic fixture world and its Compat providers) and modules/SimDrivers.lua (event and hook drivers with real payload shapes) |
| LH-12 | LootHistory | L | LH-11, LK-14 | Simulator 3/5: modules/SimScenario.lua, six scenarios as timelines with the ledger-settled gate, plus the end-to-end and saved-data invariant suites |
| LH-13 | LootHistory | L | LH-12, LH-04, LK-15, LK-16 | Simulator 4/5: modules/SimPanel.lua panel descriptor, the simulation marker on the History window, /lh sim verbs, diagnostics sim section and Sim debug tag |
| LH-14 | LootHistory | M | LH-13, WS-07 | Simulator 5/5: docs and the owed SIM smoke theme (spec, ARCHITECTURE, data-flow Simulator section, slash-dispatch, compat-layer, README) |
| MM-01 | MultiMeters | M | MM-RV, LK-07, WS-03 | Adopt W.TestStrip in every meter window: under the title, above the column headers, shown in test mode even with the header hidden; a narrow ApplyTestStrip on toggle |
| MM-02 | MultiMeters | S | MM-RV, MM-01, WS-02 | launcher-§6: the Show window key binding (CLICK MultiMetersToggleWindows) in a root Bindings.xml, on the launcher's toggleWindow handler, refusing exactly as /mm toggle does |
| QC-01 | QuickComms | M | QC-RV, LK-09, WS-06 | Adopt LibKa0s-Glow-1.0: core/GlowSetup.lua seam (NS.GlowLib), modules/Glow.lua drops its START/STOP copy for the driver on both keys |
| QC-02 | QuickComms | S | QC-RV, WS-02 | Perf-hold refusal: Toggle Comms Pads (slash, launcher, key binding), test mode and Preview as... answer the capture line, not the disabled line, under the perf hold alone |
| QC-03 | QuickComms | S | QC-RV, WS-10 | Record the LibKa0s#49 and #56 rejections where the next author looks: Documented deviations rows for the restriction tracker/readers copy and the IconStyle copy |
| WG-01 | WhatGroup | M | WG-RV, WS-02 | launcher-§6: the Show window key binding (Bindings.xml CLICK WhatGroupTogglePopup:LeftButton) on WhatGroup:ToggleFrame, refusing by hold while stood down; test_disabled step 8 extended; docs |
| MM-04 | MultiMeters | S | LK-25, MM-RV, WS-10 | Compat.ChatSender comment points at the LibKa0s#49 rejection record (comment-only) |
| AT-01 | AbsorbTracker | S | AT-RV, DC-04, WS-11 | Standards reference refresh to v2.86.0 (wow-revendor-standards) and read-for-meaning of this run's citations |
| AM-01 | AuraMaster | S | AM-RV, DC-04, WS-11 | Standards reference refresh to v2.86.0 (wow-revendor-standards) and read-for-meaning of this run's citations |
| CM-01 | ConsumableMaster | S | CM-RV, DC-04, WS-11 | Standards reference refresh to v2.86.0 (wow-revendor-standards) and read-for-meaning of this run's citations |
| DW-12 | DropWatcher | S | DC-04, DW-05, DW-06, DW-07, DW-08, DW-09, DW-10, WS-11 | Standards reference refresh to v2.86.0 (wow-revendor-standards) and read-for-meaning of this run's citations |
| KC-03 | KickCD | S | DC-04, KC-01, WS-11 | Standards reference refresh to v2.86.0 (wow-revendor-standards) and read-for-meaning of this run's citations |
| LH-15 | LootHistory | S | DC-04, LH-01, LH-02, LH-03, LH-04, LH-05, LH-14, WS-11 | Standards reference refresh to v2.86.0 (wow-revendor-standards) and read-for-meaning of this run's citations |
| MM-05 | MultiMeters | S | DC-04, MM-01, MM-02, MM-04, WS-11 | Standards reference refresh to v2.86.0 (wow-revendor-standards) and read-for-meaning of this run's citations |
| PM-01 | PanelMaster | S | DC-04, PM-RV, WS-11 | Standards reference refresh to v2.86.0 (wow-revendor-standards) and read-for-meaning of this run's citations |
| PF-01 | PartyFrameEnhanced | S | DC-04, PF-RV, WS-11 | Standards reference refresh to v2.86.0 (wow-revendor-standards) and read-for-meaning of this run's citations |
| PG-01 | PremadeGroupsFilterExtension | S | DC-04, PG-RV, WS-11 | Standards reference refresh to v2.86.0 (wow-revendor-standards) and read-for-meaning of this run's citations |
| PC-01 | PrettyChat | S | DC-04, PC-RV, WS-11 | Standards reference refresh to v2.86.0 (wow-revendor-standards) and read-for-meaning of this run's citations |
| QC-04 | QuickComms | S | DC-04, QC-01, QC-02, QC-03, WS-11 | Standards reference refresh to v2.86.0 (wow-revendor-standards) and read-for-meaning of this run's citations |
| WG-03 | WhatGroup | S | DC-04, WG-01, WS-11 | Standards reference refresh to v2.86.0 (wow-revendor-standards) and read-for-meaning of this run's citations |

## M4 — Records, finalize on the owner's go-ahead, GitHub closures

| id | repo | effort | depends on | title |
|---|---|---|---|---|
| WS-12 | WowAddonStandards | S | CT-02, WS-11 | Close WowAddonStandards#8 (state:done) with the corrected hazard facts, after the owner's merge go-ahead |
| LK-23 | LibKa0s | M | AM-RV, AT-RV, BL-01, BL-02, BL-03, BL-08, BL-09, BL-10, BL-11, BL-12, BL-RV, CM-RV, DW-02, DW-03, DW-04, DW-06, DW-07, DW-08, DW-RV, KC-01, KC-RV, LH-02, LH-03, LH-04, LH-10, LH-11, LH-12, LH-13, LH-RV, LK-22, MM-01, MM-RV, PC-RV, PF-RV, PG-RV, PM-RV, QC-01, QC-RV, WG-RV | Consumer census restamped at v1.75.0 and releasing.md's step-8 record, after every roster addon re-vendored and the adopters landed |
| LK-24 | LibKa0s | S | CT-02, LK-23 | GitHub: close LibKa0s #45-#58 with their verdicts, after the owner's merge go-ahead (no commit; exceptions.tsv) |
| BL-15 | BankLedger | S | BL-03, BL-13, BL-14, CT-02 | GitHub closure: BankLedger#23 and #24 confirmed closed by the merge and labelled state:done, after the owner's merge go-ahead (no commit) |
| DW-11 | DropWatcher | S | CT-02, DW-RV | GitHub: file the two DropWatcher issues the run found but does not fix (ItemRead bonus hole, restriction edge without the combat flag) |
| KC-02 | KickCD | S | CT-02, KC-RV, LK-22 | Repoint KickCD#38 (in-game simulator) at LibKa0s-Sim-1.0 with a comment; it stays open, state:triaged |
| MM-03 | MultiMeters | S | CT-02, LK-22, MM-01, WS-07 | GitHub: MultiMeters#59 labelled state:done once MM-01's merge closes it; #60 repointed at Sim-1.0 and kept open, state:triaged (no commit; exceptions.tsv) |
| WG-02 | WhatGroup | S | CT-02, LK-18, LK-22, WG-RV | GitHub: repoint WhatGroup#24 (in-game simulator) at LibKa0s-Sim-1.0, keep it open state:triaged (no commit; exceptions.tsv) |
| LH-16 | LootHistory | S | CT-02, LH-04, LH-14 | GitHub: LootHistory#36 and #37 confirmed closed by the merge and labelled state:done (no commit; exceptions.tsv) |
| PG-02 | PremadeGroupsFilterExtension | S | CT-02, PG-RV | GitHub: PGFE#25 confirmed closed by PG-RV's merge into main and labelled state:done (no commit) |
| CT-01 | Ka0sAddonsCommonTasks | S | DC-04, LK-23 | Run records before finalize: 06_SMOKE_TESTS.md results column, 99_EXECUTION_RECORD.md, checkpoints.tsv, exceptions.tsv, RESUME.md state |
| CT-02 | Ka0sAddonsCommonTasks | M | CT-01 | Finalize on the owner's go-ahead: --no-ff merges in dependency order, push the LibKa0s v1.75.0 tag, then delete every run branch, stash and worktree |
