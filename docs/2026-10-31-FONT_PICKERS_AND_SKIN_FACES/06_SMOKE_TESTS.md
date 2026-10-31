# Smoke tests: font pickers and skin faces (LibKa0s v1.83.0)

The owner runs these in the client. Each repo's checks are in its `docs/smoke-tests.md`. The run marks nothing as passed. These sit on top of the unfinished 2026-10-30 list, `../2026-10-30-SKIN_FONTS_AND_FEEDBACK/06_SMOKE_TESTS.md`.

**Start with a full client restart.** `/reload` cannot see new font files.

1. **Skin Tester.** PANEL-13 shows one Ka0sMedia picker of each kind. Sound holds only None unless a media pack is loaded. PANEL-5 to PANEL-8 reopened for the new wording and faces.
2. **Picker look.** Skin tab Font and Texture in any addon: each row in its own face or with its swatch, "Skin's default (X)" first and previewing X. Swatches are 44x13; large faces may crowd the 16 px rows.
3. **Addons with no SharedMediaWidgets** (BankLedger, DropWatcher, LootHistory, PGFE, PrettyChat, QuickComms, WhatGroup): their pickers fall back to Ka0sMedia. QuickComms' pad rows are checked by SKIN-29.
4. **First-run picker.** Every skin name draws, in its own face where the client has it.
5. **Faces.** Each skin against D-06; WoW Default now differs from Ka0s Default. Judge the sizes: High Contrast's Doris PP is 10.5 and Ember's Emblem 11, and WoW Default is 11/13 because real Friz is wider. Fira Sans Medium caveat from the 2026-10-30 list still applies.
6. **Obsidian.** Title is #2A86D1; section headings stay as they were.
7. **Outline.** A fresh profile is HUD text only. Your existing profiles keep a stored "All text": choose HUD text only once on the Skin tab if a profile still shows All. Check each addon's SKIN-24 to SKIN-28 area.
8. **Overrides.** Pick a Ka0s face as a font override: text keeps Prototype's width.
9. **DpsRace.** Run detail has one header row, starting "Spell". HUD tooltips SM-DR-FP6 to SM-DR-FP11, including an in-combat hover (SM-DR-FP8), which the harness cannot prove.
10. **ruRU**, if you care to check: Ember and WoW Default window text has no Cyrillic face.
