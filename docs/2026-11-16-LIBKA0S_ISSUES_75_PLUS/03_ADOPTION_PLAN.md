# Phase [3]: adoption plan (planned, not executed in this run)

**Precondition:** each addon vendors v1.105.0 (phase [2]). Adoption runs as its own bundle. Each addon gets one
branch and one commit per surface (`AD-<ISSUE>-<ABBR>`). Each addon's adoption items are owed under the v2.113.0
"owed when the addon adopts" clauses, and its re-vendor bundle lists them.

The counts below come from the research of 2026-11-16 (R3, R7, R8). The site lists are in those notes. Each count
is approximate until the adoption run re-checks it.

## Per surface

| Issue | Surface | Work per addon | Affected |
|---|---|---|---|
| #92 | `LibKa0s-Tooltip-1.0` placers | Move every `GameTooltip:SetOwner`/`ANCHOR_*` site onto `PlaceBeside`/`PlaceAttached`. Remove the cursor and corner anchors. Charts hosts move from a cursor tip to `ctx:PlaceTip`. | All 19 except PanelMaster and PartyFrameEnhanced (0 sites). Largest: CombatTrail 22, LootHistory 14 (3 cursor), DpsRace 13, BankLedger 12, OutfitterReborn 10, Skill Master and QuickComms 8. |
| #92 | AuraMaster's tooltip-anchor option | This is a player setting that offers `ANCHOR_CURSOR`. Migrate saved values to the placer. **Owner ruling needed** on whether a player choice survives. | AuraMaster |
| #88 | Docked test/sim strip | Use `dock="title"` in windows and `dock="hud"` on HUDs. Remove the header mode words. | AbsorbTracker, AuraMaster, KickCD (HUD; reverses KickCD ruling D-13 and inverts `test_sim_marker`). BankLedger, CombatTrail, DpsRace, LootHistory, Skin Tester, MultiMeters, OutfitterReborn, Skill Master (undocked today). DropWatcher is done. |
| #89 | `W.Footer` 24 px | Replace each hand-built footer. | BankLedger and LootHistory (18 px), CombatTrail (2), DpsRace (20 px), Skin Tester (22 px), AuraMaster's PresetPicker, OutfitterReborn, Skill Master. DropWatcher is done. |
| #79 | `D:Report` / `D:Serialize` | Move each report verb onto `D:Report`. Replace `DevTools_Dump` (no live call is known). | ConsumableMaster (one-line lift; delete its local serializer), AuraMaster `containers`, KickCD `spells`/`debug`, OutfitterReborn `missing`/`iteminfo`, PanelMaster `panels`, PartyFrameEnhanced `status`, QuickComms `why`/`check`/`probe`, DropWatcher `scan`, Skin Tester `widths`, BankLedger `session`, DpsRace `results`, and CombatTrail and DpsRace ignore lists. Confirm each verb against its handler. |
| #86 | `W.HeaderButtons` | Move each addon-owned window's title marks onto the strip, with settings on every window. Turn on the drag-handle settings mark per addon. | CombatTrail (6 windows, 12 marks), DpsRace (4 windows, 7 marks), BankLedger 3, LootHistory 2, AuraMaster 1, Skin Tester 1, Skill Master, DropWatcher, OutfitterReborn and QuickComms windows. |
| #87 | `Sim.Sample(client)` | Replace the addon's own sample names with the shared sets (retail/forever). Keep the seeded crowd lists in DropWatcher and MultiMeters. | Every addon with test or sim data, including BankLedger's localized name. Fixtures that look like real characters (`Kaosmage-Frostmourne`, `Kaos-Silvermoon`) are renamed. |
| #80 | `W.Bar` | Skill Master swaps `NS.Bar` for `W.Bar`, deletes `modules/Bar.lua` and remaps its bonus tokens. | Skill Master |
| #81 | Launcher `extraEntries` | Skill Master adds **Journal**. The ADDONS.md launcher column gains "· Journal". | Skill Master |
| #85 | Callout consumers | Evaluate each candidate. Recommended decisions: DpsRace **adopt** (replace `modules/Countdown.lua`); DropWatcher and QuickComms **not now**; Skill Master **never**. | DpsRace, DropWatcher, QuickComms, Skill Master |
| #82 | Host owner tokens | Check each host's own `*.hot` aliases against the new floors. | Skill Master (block-header detach mark), others as found |
| — | `DefaultSkin` (skinning-§2 MUST since v1.94.0) | Adopt the default skin. | MultiMeters, PGFE, WhatGroup |

## Order (recommended)

1. **Compliance gaps first:** the `DefaultSkin` adoption in MultiMeters, PGFE and WhatGroup.
2. **#88 and #89 together:** both change window geometry, so do them with one smoke per window.
3. **#86:** it builds on #88 and #89's chrome.
4. **#92 last among the chrome items:** tooltips sit on the final chrome.
5. **#79, #87, #80, #81 and #85,** which are independent of each other.

Pilot each surface in one addon before the sweep: DropWatcher is the reference for #88 and #89, and CombatTrail
for #92 and #86. Each addon's smoke checks and docs move in the same commit as the code.
