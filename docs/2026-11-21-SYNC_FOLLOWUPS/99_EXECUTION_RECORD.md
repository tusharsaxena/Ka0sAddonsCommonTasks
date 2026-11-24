# Execution record: sync-docs follow-ups (2026-11-21)

Branch `feat/2026-11-21-sync-followups` in 22 repos plus this one. Progress comes from git (`plan-data/resume-state.sh`).
Every independent review is a `refs/notes/ka0s-review` note on the repo's head.

## What was built

- **WowAddonStandards v2.117.0** (`88c73b3`):
  - The other session's `feat/2026-11-10-per-client-quirks` landed, renumbered from v2.108.0. `forever-quirks` is now the
    WoW Forever catalog and `client-quirks` the Retail one.
  - The roster note now says every repo defaults to `master`.
  - Review fix: events-frames-taint names each client's quirks file.
  - The LibKa0s size statements say 86 files; the CP-1 check-standard run caught it.
- **dev-copilot 2.11.0** (`59009aa`):
  - Its `feat/2026-11-10-per-client-quirks` landed: revendor, harvest, audit, scaffold and sync-docs handle one quirks
    file per client.
  - `roster_clients.py` finds the roster from the repo it runs in, so it works from the plugin cache (17 tests).
- **LibKa0s v1.109.0** (`d5b62f35`):
  - The band files were peeled on their recorded seams:
    - `OptionsCompose.lua` 1217 → 883 (+ `OptionsComposeMaster.lua`);
    - `SkinPaintControls.lua` 1114 → 920 (+ `SkinPaintNav.lua`);
    - `Callout.lua` 1416 → 1113 (+ `CalloutRoute.lua`, `CalloutSound.lua`). Callout stays in the band, **accepted**: its
      seam is the animations, and the re-check trigger is 1250 lines or the next minor that adds a function.
  - Kit revision 59: the kit README counts eight suites and names the roster instead of counting copies.
  - `docs/api/CONSUMERS.md` was re-measured across the 19 addons, with all 152 instance rows the tool could not see read by
    hand. Seven exports have no production reader anywhere (kept for the published surface).
  - Compat minor 5 and Sim minor 4 cite forever-quirks-§4.
  - Release record `docs/automated-tests/20261121-214308/`.
- **The 19 addons:**
  - Each re-vendored LibKa0s v1.109.0 and standard v2.117.0. Every Retail · Forever addon gained `docs/forever-quirks.md`.
  - Forever-only own entries moved there verbatim:
    - Combat Trail 10;
    - Consumable Master: the consumable subclasses;
    - Drop Watcher: the WoW Forever table;
    - Range Master 5.
  - Retail-only addons record forever-quirks as *Not applicable*. Skill Master's catalog moved from the branch's v2.108.0
    to v2.117.0.
  - Forever name citations were repointed to forever-quirks-§4: Combat Trail, Drop Watcher, Outfitter Reborn and Party
    Frame Enhanced.
- **Addon-specific items:**
  - **FU-LH-BROWSER:** Loot History `modules/Browser.lua` 1477 → 988, its view layer peeled into
    `modules/BrowserViews.lua`. The layout-§1 deviation row is retired.
  - **FU-ST-PERF:** Skin Tester `skinRepaint` was bisected over 17 commits. The rise from 1415 to 1459 calls is expected
    cost: V89A-ST's cascade sample, the footer and header buttons, and SD-SK-ST's skin text colors (+27 calls). It is
    re-pinned at 1459 calls and 252260 bytes.
  - **Dead exports removed:**
    - Drop Watcher: `P.Ticking`, `W.IsMasterLootKey`, `WF.SegmentTip`;
    - Range Master: `Container.PreviewKind`, `Container.ShowsAll`, `Frame.__waiting`, `Preview.__drawn`;
    - Skill Master: `R.Opens`, `J.SelectedFilter`;
    - Combat Trail: `NS.ShowCopy`, and its SkinSetup comments no longer cite a missing suite.
  - **Kept:**
    - Multi Meters `NS.__WindowSection` is a live test seam (`exceptions.tsv`).
    - Range Master `NS.SkinPaintAce` is the shared skin seam.
  - **A real bug found:** Kick CD `NS.RefreshOptionsPanel` had no caller, so the open panel kept the old profile's values
    after a profile switch, copy or reset. It is now called from `Database:OnProfileChanged`, test first.

## CP-1 (2026-11-21)

Every repo was tested on each client it ships, and every run passed:

- luacheck 0 / 0 in every repo;
- WowAddonStandards `check-standard.sh`: all checks passed after the count fix;
- dev-copilot: all eight `scripts/test_*.py` suites OK.

| Repo | Retail | WoW Forever |
|---|---|---|
| LibKa0s | 5076 passed / 0 failed | 5076 / 0 |
| AbsorbTracker | 1093 / 0 | 1093 / 0 |
| AuraMaster | 2570 / 0 | 2569 / 0 |
| BankLedger | 1724 / 0 | (Retail only) |
| CombatTrail | 1625 / 0 | 1615 / 0 |
| ConsumableMaster | 1523 / 0 | 1523 / 0 |
| DropWatcher | 2720 / 0 | 2608 / 0 |
| KickCD | 1738 / 0 | (Retail only) |
| LibKa0sSkinTester | 937 / 0 | 937 / 0 |
| LootHistory | 2054 / 0 | (Retail only) |
| MultiMeters | 2659 / 0 | (Retail only) |
| OutfitterReborn | 1613 / 0 | 1592 / 0 |
| PanelMaster | 1211 / 0 | 1211 / 0 |
| PartyFrameEnhanced | 673 / 0 | 673 / 0 |
| PremadeGroupsFilterExtension | 583 / 0 | (Retail only) |
| PrettyChat | 704 / 0 | 704 / 0 |
| QuickComms | 2105 / 0 | 2105 / 0 |
| RangeMaster | 794 / 0 | 794 / 0 |
| SkillMaster | (Forever only) | 817 / 0 |
| WhatGroup | 1139 / 0 | (Retail only) |

## Smoke checks owed (the owner's, in game; never marked passed here)

- **KC-PROFILE-1:** with `/kcd` settings open, switch profile (and Reset profile). The open page shows the new profile's
  values at once. **Passed** (owner, 2026-11-24).
- **LH-BROWSER-1:** `/lh` opens on History. Switching Insights, Holdings and Timeline keeps each tab's filters, group and
  sort. **Passed** (owner, 2026-11-24).
- **LH-BROWSER-2:** Save, Reset and Clear act only on the active tab. Export opens that tab's modal. "Show in Timeline"
  fills Search. **Passed** (owner, 2026-11-24).
- **LH-BROWSER-3:** changing the minimum-quality setting re-filters the open window. A profile switch re-reads the
  geometry and the saved view. **Passed** (owner, 2026-11-24).
- **ALL-1:** every addon loads with no Lua error on each client it ships. The library peels change no behavior.
  **Passed** (owner, 2026-11-24).

## Finalize (2026-11-21)

- **Pre-merge check:** every repo was fetched first. No `master` had moved and no remote held v1.109.0 or v2.117.0.
- **Merged `--no-ff` and pushed in dependency order.** Each merge tree is identical to its CP-1-gated branch.
  - WowAddonStandards `4828484` and tag v2.117.0.
  - dev-copilot `608c076`. This repo has no release tags. The owner updates the installed plugin to 2.11.0.
  - LibKa0s `69113559` and tag v1.109.0.
  - The 19 addons, then this repo. `refs/notes/ka0s-review` was pushed everywhere.
- **Deleted:** the run branch (local only, never pushed) in all 23 repos, and the landed
  `feat/2026-11-10-per-client-quirks` branches (local and remote) with their two worktrees under `#Worktrees/`.
- No addon version was bumped. The smoke checks above are still the owner's.

## Smoke result (2026-11-24)

The owner reported on 2026-11-24 that all five smoke checks above passed (run "SYNC 11-21" of a Google Sheet copy of
`Documents/Ka0sPendingSmoke-2026-11-23.csv`): KC-PROFILE-1 on Retail, LH-BROWSER-1 to LH-BROWSER-3 on both clients,
and ALL-1 on each client every addon ships. Recorded on the owner's word.
