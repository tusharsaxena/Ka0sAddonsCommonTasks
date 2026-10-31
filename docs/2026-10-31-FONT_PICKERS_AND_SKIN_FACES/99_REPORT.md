# Report: font pickers and skin faces

All 43 planned items and the 18 addendum items landed on `feat/2026-10-31-font-pickers-skin-faces` in 19 repos, pushed with review notes. Nothing merged. LibKa0s tag v1.83.0 is LOCAL at ec41b22 (re-cut twice: LK-A1, LK-A2). Standard v2.94.0.

## Gates on final heads

LibKa0s 3469/0/2, luacheck 0/0, CCN max 15. Skin Tester 605/0/1; AbsorbTracker 972/0/1; AuraMaster 2249/0/1; BankLedger 1534/0/1; ConsumableMaster 1316/0/1; DpsRace 1202/0/1; DropWatcher 1844/0/1; KickCD 1577/0/1; LootHistory 1860/0/1; MultiMeters 2449/0/1; PanelMaster 1161/0/1; PartyFrameEnhanced 565/0/1; PGFE 452/0/1; PrettyChat 656/0/1; QuickComms 1297/0/1; WhatGroup 1045/0/1. Each vendored copy equals the tag apart from the icon prune.

## Lead calls and departures

- Pickers: addons with SharedMediaWidgets keep its stock `LSM30_*` pull-out; only the Skin tab and the fallback use Ka0sMedia (D-08). No addon had a plain media dropdown to convert. The first-run picker has no font or texture chooser, so nothing changed there but LK-A2.
- A window has no public route to a Ka0sMedia type yet; options-ui-§23 records "use LSM30_* until the library publishes a seam". No addon needs it. Not an owner ruling.
- Older fonts removed before this run came back too (Oxanium, Inter, Fira Sans Regular). Payload grows about 6 MB per addon, fonts 3.6 MB to about 10 MB. 13 faces shipped; the manifest's "15" is a typo.
- Obsidian's headings keep their color; only the title moved.
- Unmeasured LSM faces used as overrides draw at Ka0s Default's sizes.
- KickCD's stand-down suite exempts the shared font preload host, as it does the drag handle's measurer.

## Known limits

- The new widgets are proven headless only; the kit's AceGUI has no stock Dropdown, so addon suites do not exercise them.
- D-10: AceDB strips a value equal to its default, so a player who chose All text under the old default moves to HUD text only. An `all` stored by the local v1.82.0 build through a font pick stays, as it cannot be told from a real choice.
- Emblem, Friz and Doris PP have no Cyrillic. Locale-refused faces fall back in size as well as face.
- DpsRace title-bar lock, settings and Results keep their one-line tooltips.
- "over the skin's own" stays in a few skip-render tooltip prose strings and comments (DropWatcher, LootHistory, PGFE); the renamed label is the Skin tab entry.

## Licensing

Open Sans is Apache 2.0; the older open faces are SIL OFL. Prototype and Expressway ship on earlier rulings. Friz (ITC), Doris PP (Ares), Emblem (Weatherly; its name table says "Redistribution strictly prohibited"), Avant Garde (ParaType) and Segoe UI (Microsoft; "Any other use is prohibited") have no grant and ship on the owner's ruling alone. `LibKa0s/media/fonts/FONTS.md` is the record.

## Owner report during the run

The blank Azeroth picker row was a client not restarted after the fonts arrived; confirmed by the owner. LK-A2 hardens the row anyway.
