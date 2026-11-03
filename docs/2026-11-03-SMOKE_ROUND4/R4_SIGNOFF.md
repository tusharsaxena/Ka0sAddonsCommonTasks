# R4 mockup sign-off (owner, 2026-11-03)

Owner's reply to `R4_MOCKUP.html`, verbatim:

1. Header - E
2. Picker swatch: "Swatch: header" (second swatch becomes the new header colour)
3. Icon borders, which skins: "Icon borders: proposed, all skins"

> For headers - lot of addons with an actual window have a "separator line" under the header - which the skin
> tester does not have. Make them all like SkinTester (i.e. no separator line below header). Make sure to do this
> for all windows of every addon - including the main addon window, debug window, debug copy windows, skin
> selectors, etc etc

Images: `inputs/images/23.png` (MultiMeters), 24 (DpsRace), 25 (Loot History), 26 (Bank Ledger), 27 (Skin Tester,
the reference: no line), 28 (Skin Tester debug), 29 (WhatGroup).

## What it means

- **R4-L2 header:** Ka0s Default `title.bgTop` #3A2F0A, `title.bgBottom` #1F1905, `title.bg` the blend #2C2408 for
  flat readers (MultiMeters' meter header strip, its fallback copy). Swatch 2 becomes #2C2408.
- **R4-L3 icon borders:** proposed values in every listed skin: Ka0s Default #4D4D57, Glass white 0.35, WoW Forever
  #5A5048, Ember #8A3C1C, WoW Midnight #7A6532; Obsidian, Azeroth, High Contrast, WoW Default unchanged.
- **Scope (not answered; lead's call): one token, `icon.border`** (mockup option 1, its recommendation). HUD icon
  edges in AuraMaster, KickCD, DropWatcher, QuickComms, DpsRace and ConsumableMaster's button border follow it, as
  Obsidian's already do; DpsRace and QuickComms fallback copies move with it. Reversible at smoke.
- **R4-SEP no header separator:** no line under the title band in any window of any addon (main windows, debug
  and debug copy windows, skin selectors, export/copy windows, every other window). The Skin Tester showroom is the
  reference. Settings pages' `title.rule` is not a window header and stays unless it draws under a window title.
