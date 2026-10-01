# Execution record

The 2026-10-01 GitHub issue pass, run in one session on 2026-10-01. Every item in `items.tsv` is done, and
each was reviewed independently: `./resume-state.sh` reports M0 1/1, M1 14/14, M2 40/40 and M3 (GI-LK-13) 1/1,
with GI-FIN-01 being this commit. Nothing is merged, no tag is pushed, and no addon version moved.

## Outcome per owner decision (39 rows)

| Group | Issues | Where it stands |
|---|---|---|
| Closed on the owner's word | AbsorbTracker#10, KickCD#7, PrettyChat#1, PrettyChat#5 | Closed 2026-10-01. KickCD#7 carries a correction comment: the proposed code fix was never applied, and the issue was closed on the owner's report that the symptom is gone |
| Found already addressed | LibKa0s#17, #18, #19, #20 | Closed 2026-10-01 with evidence (`test_options_tabs.lua` invariance cases). Kit 35 rewrote the stale mock comment |
| Fixed on the feature branches | 30 issues (table below) | Commented with their commits. **They close at finalize**, after the owner's merge go-ahead (D11) |
| Fixed, waits on in-client proof | PartyFrameEnhanced#3 | Built and tested offline. It stays open until COMBAT-6/9/10 pass in the client (D9) |

Carried in: ConsumableMaster#16 was fixed by GI-CM-01 and also closes at finalize.

### Fixed issues → commits

| Issue | Item | Repo | Commits |
|---|---|---|---|
| LibKa0s#35 | GI-LK-01 | LibKa0s | cc7190d |
| LibKa0s#38 | GI-LK-02 | LibKa0s | b06f0bb |
| LibKa0s#40 | GI-LK-03 | LibKa0s | bf4e00d, d37d16b |
| LibKa0s#36 | GI-LK-04 | LibKa0s | 8bf5c1f |
| LibKa0s#7 | GI-LK-07 | LibKa0s | a904e6a, 39f9204, c83ecd7 |
| LibKa0s#12 | GI-LK-08 | LibKa0s | e907508 |
| LibKa0s#1 | GI-LK-09 | LibKa0s | 975ca50 |
| LibKa0s#9 | GI-LK-13 | LibKa0s, Ka0sAddonsCommonTasks | 389a65b; 2f6b731 |
| WowAddonStandards#6 | GI-LK-10, -11, GI-STD-01, GI-PLUG-01, every GI-*-RV, GI-AM-01, the five CCN items | all 14 | LibKa0s a1e797a, 4a9969b, c2836b1, c9bfcc0, 738f892, bc9d2d4; standard cb11720, 8d8c36a, 544db10; wow-addon 78200c9, 28672a7, d3b05f5 |
| AbsorbTracker#20 | GI-AT-01 | AbsorbTracker | 45cf8cc |
| AbsorbTracker#32 | GI-LK-06, GI-AT-02 | LibKa0s, AbsorbTracker | 63c19c3; c1d8492, ac2ff82, ef895a4, cc72830, eccf766 |
| BankLedger#2 | GI-BL-01 | BankLedger | dd3080a |
| ConsumableMaster#16 | GI-CM-01 | ConsumableMaster | aacc43b |
| KickCD#25 | GI-KC-01 | KickCD | 04056df, 442dab8 |
| KickCD#26 | GI-KC-02 | KickCD | ef89983, 442dab8 |
| KickCD#27 | GI-KC-03 | KickCD | ec383aa |
| KickCD#24 | GI-KC-04 | KickCD | 5b51f60, 442dab8 |
| KickCD#29 | GI-KC-05 | KickCD | 2dcf730, 442dab8 |
| KickCD#28 | GI-KC-06 | KickCD | 252fdc0 |
| KickCD#30 | GI-KC-07 | KickCD | 411eab8, 071f93a |
| KickCD#31 | GI-KC-08 | KickCD | 410a61e |
| KickCD#32 | GI-KC-09 | KickCD | 7bc51bc |
| KickCD#9 | GI-KC-10 | KickCD | ee541b1, 5fa1ec8 |
| KickCD#10 | GI-LK-05, GI-KC-11 | LibKa0s, KickCD | 0cc0d6e; e0da04c |
| LootHistory#32 | GI-LH-01 | LootHistory | dbe3a89, 6faecb1, d9ebc61, f75a26c, 1194ad6 |
| MultiMeters#56 | GI-MM-01 | MultiMeters | cdb7578 |
| PanelMaster#42 | GI-PM-01 | PanelMaster | c75d5e3 |
| PanelMaster#15 | GI-PM-02 | PanelMaster | 3d2cc40 |
| PanelMaster#54 | GI-PM-03 | PanelMaster | 962ce15, b58cba5 |
| PartyFrameEnhanced#12 | GI-PF-01 | PartyFrameEnhanced | c3d4298 |
| PartyFrameEnhanced#3 | GI-PF-02 | PartyFrameEnhanced | abfd7e9 |
| WhatGroup#1 | GI-WG-01 | WhatGroup | 2ed2aa5, 1f7bfca |

## Releases (local, unpublished)

- **LibKa0s v1.66.0**: local annotated tag on `e4c5ef7`. The release bundle `docs/automated-tests/20261001-133255/`
  is green: 1997/0/2, luacheck 0/0, sighted complexity 0 warnings, max CCN 15, 0 blind files. The payload is
  **32 files** (PerfCommands, PerfSampler, WidgetsReorder, SlashParse added). Kit revision **35**.
  GI-LK-13 (`389a65b`) sits one commit after the tag and is docs only.
- **Standard v2.74.0** (`544db10`): the complexity gate is sighted (automated-tests-§3), lizard's five Lua
  blind spots are documented, a complexity warning means CCN > 15 only (`-L 1500`), and the payload is recounted.
- **wow-addon** (`d3b05f5`): review agent and bump-version use the runner's sighted suite, and blindFiles is a
  release-gate condition.

## Changes to the plan during execution

- **Addendum A1/A2** (`M1_ADDENDUM_RELEASE_GATE.md`). The first release run was refused on two length-only
  lizard warnings, so lizard's length threshold now equals the file cap. Perf and Slash got a second peel so the
  cycle adds no file to the 1000–1500 band.
- **The validation pass found WowAddonStandards#6 broader than filed.** The cause is the Ruby-like reader's
  `it/class/module/begin/unless`, as well as `#`. A fifth blind spot (a function literal in a `for … in`
  header) turned up during kit 35. About 1,600 functions collection-wide had never been measured. The
  sighted gate surfaced the over-15 functions in LibKa0s, BankLedger, ConsumableMaster, KickCD, LootHistory and
  MultiMeters, and every one is now at CCN 15 or under.
- **Notable implementer judgement calls** (each accepted by the independent reviewer):
  - KickCD#9 re-arms the swipe once after `OnCooldownDone` if the spell is still active, which covers the GCD →
    real-cooldown handoff. An icon whose cooldown ended stays registered until the ready emit arrives.
  - KickCD#10 builds each spell row directly into RenderGrid's wrapper (`BuildRow(..., into)`).
  - PanelMaster#54 adds a record-write mode so CopyFrom is not refused over media that has not loaded yet.
  - WhatGroup's default popup height goes from 260 to 280 to fit the Role row.
  - BankLedger peeled `L:Diagnose` to `Ledger_Diagnose.lua` so Ledger.lua stays out of the band.
  - LibKa0s#7 peeled the command surface **and** the sampler (Perf.lua 1307 → 975).
- Most addons also wrote a span re-vendor bundle for v1.64.0–v1.65.0, because the revendor skill requires one
  for tags vendored without a record.
- Files still in the 1000–1500 band and newly entered: AbsorbTracker `tests/test_panelpages.lua` 1019, and
  LootHistory `settings/Panel.lua` 1133 (it was already in the band and grew by 20). Each is dispositioned at its
  next automated-test battery.

## LibKa0s#9 census (GI-LK-13)

106 of 409 public exports have no consumer. Every one is documented in place ("no consumer as of v1.66.0,
kept because …"), and nothing was deleted. The census filed nine issues: LibKa0s#41 (MakeResizable has no lock
gate) and #42 (addonName descriptor field unconsumed), plus host-adoption issues BankLedger#21, LootHistory#33,
MultiMeters#58, AbsorbTracker#33, KickCD#36, ConsumableMaster#44 and PanelMaster#56. The tool and data are in
`plan-data/census*`.

## Verification (orchestrator re-run, 2026-10-01 after M2)

| Repo | Tests | luacheck | Sighted complexity | Vendor diff |
|---|---|---|---|---|
| AbsorbTracker | 855/0/1 | 0/0 | 0 warnings, max 14 | 0 |
| AuraMaster | 1788/0/1 | 0/0 | 0, max 15 | 0 |
| BankLedger | 1214/0/1 | 0/0 | 0, max 15 | 0 |
| ConsumableMaster | 1186/0/1 | 0/0 | 0, max 15 | 0 |
| KickCD | 1282/0/1 | 0/0 | 0, max 15 | 0 |
| LootHistory | 1040/0/1 | 0/0 | 0, max 15 | 0 |
| MultiMeters | 2168/0/1 | 0/0 | 0, max 15 | 0 |
| PanelMaster | 1033/0/1 | 0/0 | 0, max 15 | 0 |
| PartyFrameEnhanced | 453/0/1 | 0/0 | 0, max 14 | 0 |
| PrettyChat | 571/0/1 | 0/0 | 0, max 15 | 0 |
| WhatGroup | 913/0/1 | 0/0 | 0, max 15 | 0 |
| LibKa0s | 1997/0/2 | 0/0 | 0, max 15, 0 blind | — |

## In-client smoke checks

`04_SMOKE_TESTS.md` is the cross-cutting list. Each addon's `docs/smoke-tests.md` now also carries the
checks its implementer added (all **never run**):

| Addon | New or re-owed checks |
|---|---|
| AbsorbTracker | LOOK-15, LOOK-17 (Appearance strip via RenderTabbedSchema), DIAG-26–39 (perf run on v1.66.0) |
| BankLedger | CAPT-18, CAPT-19 (login backfill) |
| ConsumableMaster | SLASH-4 (corrected), SLASH-15 (parse refusals in the host's wording) |
| KickCD | GRID-15, GRID-16 (ticker owns time; no repeating emit) plus GRID-5/8/9 re-owed |
| LootHistory | PANEL-20 (ReorderList from WidgetsReorder), INS-22 (Insights split) |
| MultiMeters | GRID-15, GRID-16 (corrected for the companion identity) |
| PanelMaster | PANEL-27 (Frame level), PANEL-28–31 (instance-addressed writes), FRAME-12 (corrected) |
| PartyFrameEnhanced | COMBAT-6, 9, 10 (in-combat follow; #3 closes on these), COMBAT-11, 12 |
| WhatGroup | POPUP-9, TEST-12, LFG-5–8 (Role row) |

## What the owner does next

1. Run the smoke checks above. Record results in `04_SMOKE_TESTS.md` and in each addon's `docs/smoke-tests.md`.
2. Give the merge go-ahead. `/wow-addon:finalize` then merges in dependency order (LibKa0s → standard → wow-addon →
   addons → this repo), pushes tag `v1.66.0`, deletes the branches and closes the 30 fixed issues plus
   ConsumableMaster#16. PartyFrameEnhanced#3 closes only on COMBAT-6/9/10.
