# Smoke tests: the skin library follow-ups (LibKa0s v1.81.0)

The owner runs these checks in the client. Each repo keeps its own checks in `docs/smoke-tests.md`, listed under
Pending sign-off, and the owner records the results there. This file gives the index and the order to run them in.
The run marks nothing here as passed.

## Before you start

- The game loads every addon from its `GIT/<Addon>` checkout. All 15 addons, LibKa0sSkinTester and LibKa0s are on
  `feat/2026-10-30-skin-library-followups`, so every addon carries LibKa0s v1.81.0.
- `/reload` once. The invalid font height error in MultiMeters should be gone (MM-H1, and the library guard LK-A1).
- The best place to start is the Skin Tester. It shows every skin's HUD face, the new tokens and every newly
  skinned library widget on one screen.

## Cross-cutting checks (run once)

| Id | Check | Ruling | Result |
|---|---|---|---|
| FU-1 | `/reload` with every addon on: no Lua error (the MultiMeters invalid font height in particular) | MM-H1, LK-A1 | |
| FU-2 | Any addon's skin picker: the window title is **Choose a skin**, the addon's full name is on its own line above the dropdown, and nothing is cut off. Try the longest name (Ka0s Premade Groups Filter Extension) | R-11 | |
| FU-3 | Each addon's settings tab is labelled **Skin**, not Appearance | R-10 | |
| FU-4 | Under Ka0s Default, no window wears the stock look any more. QuickComms' popup and icon browser, the PGFE panel (no metal frame) and DpsRace's custom length box are all Ka0s | R-2, D-05, D-06 | |
| FU-5 | Choose **WoW Default**: this is now the stock look. Its HUD face is Friz Quadrata | R-2, D-11 | |
| FU-6 | Switch through the skins with a HUD addon visible (AbsorbTracker, KickCD, DpsRace, AuraMaster). Each skin has its own HUD face: Obsidian Inter SemiBold, Azeroth Vollkorn Bold, Glass Nunito SemiBold, High Contrast Atkinson Bold, Ember Bitter Bold, WoW Midnight Philosopher Bold, WoW Forever Fira Sans SemiBold. **Judge whether you like each one** | R-4, D-11 | |
| FU-7 | Tick **Ignore fonts**: the HUD text returns to each element's own font setting, along with every library window string (debug console title bar, perf and sim panels, drag-strip labels, dropdown menus). Texture and colors keep following the skin. The skin picker's rows keep each skin's own face on purpose | R-1, D-15 | |
| FU-8 | **Ignore settings panel** on (the default): the settings pages are stock, including the reorder lists (ConsumableMaster, LootHistory, MultiMeters) and the id lists. The windows (console, copy, perf, sim, drag strips, picker, editors) still follow the skin | R-5, D-01 | |
| FU-9 | Close buttons: switch skins and then choose WoW Default. A close button's art gets its own color back with no leftover tint | R-3 | |
| FU-10 | Drag-strip tooltips (for example AbsorbTracker's and AuraMaster's) use the skin's tooltip colors. Under Ka0s Default they look as before | R-7, D-14 | |
| FU-11 | Item-quality colors (LootHistory, DropWatcher) match the game's own exactly | R-8 | |
| FU-12 | **New look under Ka0s Default, judge it:** the settings drawer's arrow is now gold-tinted where it was the game's yellow art. The library's tool-window strings and dropdown rows are now in Oxanium. Suggestion rows are 0.9 white | D-13, M1 review nit | |

## Skin Tester (start here)

| Checks | What | Result |
|---|---|---|
| SHOW-8, SHOW-17, SHOW-19..25 | The eleven sections. HUD faces, one line per skin (SHOW-19). The library widgets section. The gtip.* and art-tint values. The SettingsFrameTemplate sample now in Ka0s Default (SHOW-17) | |
| PANEL-11 | The settings chrome's face, hover art and tooltips | |
| PICKER-1, 10, 16 | Picker title and addon-name line | |

## Per addon

| Addon | Checks changed or added | What to look at | Result |
|---|---|---|---|
| AbsorbTracker | SKIN-3, 5, 9, 10, 17, 25, 26 | HUD face per skin (SKIN-5); Ignore fonts on the HUD (SKIN-26) | |
| AuraMaster | SKIN-2, 4, 5, 6, 8, 10, 18, 25 (new) | Ignore fonts on the HUD (SKIN-10); the "not an aura" tag follows Ignore settings panel | |
| BankLedger | SKIN-1, 8, 10, 19, 26 | Oxanium on the library's strings; the resize grip | |
| ConsumableMaster | SKIN-4, 9, 10, 17, 22, and SKIN-7 (clause) | A **one-frame flash of the template color** on the state rows after a skin switch counts as a pass (known limit, report §Lead decisions) | |
| DpsRace | SM-DR-SK1, 4, 9, 10, 12, 25 (new) | The custom length box now Ka0s (SK4); HUD face per skin (SK25); Results tooltip lines follow the skin; resize grips tint | |
| DropWatcher | SKIN-1, 11, 12, 16, 19 | Quality colors exact; the main window's resize grip tints | |
| KickCD | SKIN-6, 9, 11, 12, 14, 22 | Ignore fonts on the HUD (SKIN-14) | |
| LootHistory | PANEL-23, 24; SKIN-1, 8, 17, 24, 27 | Under Ignore settings panel, the AH price table keeps Ka0s Default's gold, white and status colors in the template face (PANEL-24, D-21). **Judge it** | |
| MultiMeters | INSTALL-15; SKIN-2, 4, 5, 8, 9, 12, 15 | The title error is gone; reorder ghost colors follow the Scope | |
| PanelMaster | SKIN-1, 3, 7, 8, 15 | The picker shows the full name (SKIN-15) | |
| PartyFrameEnhanced | INSTALL-4; SKIN-4, 7, 8, 17, 23, 24 | The Ignore fonts tooltip wording; HUD font sections | |
| PremadeGroupsFilterExtension | SKIN-11, 13, 15, 16, 19, 20, 25, 26, 29, 31, 33; APPLY-14, 22; LAYER-1 | **The metal panel is gone** (D-05): one frame painted by the skin, with a 30 px title band | |
| PrettyChat | SKIN-1, 3, 8, 10, 12, 18 | Windows keep the skin under Ignore settings panel (SKIN-3) | |
| QuickComms | SKIN-3, 5, 8, 9, 10, 11, 12, 14, 17; EDIT-9, 13, 14; LOC-1 | **Popup and icon browser are Ka0s under Ka0s Default** (D-06); browser texts now in the skin's face | |
| WhatGroup | SKIN-9, 18, 22 | Picker; Ignore fonts | |
