# Report: font pickers and skin faces

All 43 planned items and the 36 addendum items landed on `feat/2026-10-31-font-pickers-skin-faces` in 19 repos, pushed with review notes. Nothing merged. LibKa0s tag v1.83.0 is LOCAL at 6c816fd (re-cut for LK-A1, LK-A2, LK-A3). Standard v2.94.0.

## Gates on final heads

LibKa0s 3522/0/2, luacheck 0/0, CCN max 15. Skin Tester 605/0/1; AbsorbTracker 972/0/1; AuraMaster 2249/0/1; BankLedger 1534/0/1; ConsumableMaster 1316/0/1; DpsRace 1206/0/1; DropWatcher 1844/0/1; KickCD 1577/0/1; LootHistory 1860/0/1; MultiMeters 2449/0/1; PanelMaster 1161/0/1; PartyFrameEnhanced 565/0/1; PGFE 452/0/1; PrettyChat 656/0/1; QuickComms 1297/0/1; WhatGroup 1045/0/1. Each vendored copy equals the tag apart from the icon prune.

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

## After the first report (owner requests)

- **LK-A3.** Every addon's skin picker gains the Skin tab's Font, Texture, resets, Font outline and Scope rows: 308 wide (+10%), about 320 tall, full-width rows with reset icons beside them. Live preview; Apply saves; close restores. Apply to all now carries scope, font, texture and outline. A tab edit while the picker is up drops unapplied previews there.
- The review fix's PLAYER_REGEN_ENABLED registration broke the stand-down rule in seven addons, caught at re-vendor. The picker now registers no event; a throttled OnUpdate runs only while rows are locked.
- Lazy-build pins in PrettyChat and the Skin Tester count past the picker's five rows; a fresh profile shows them at login. LootHistory's SkinAce pin moved.
- **DR-F05.** One bar scale across Damage, DPS and spells. Blue is the board's best in *Compare vs best* and *vs runner-up*; a picked run goes by total damage, this run on a tie. The final colors (#203652, #403500, opaque) were committed by the lead after the independent review, tests and lint only.
- The event removal and the final pins had no independent review. Reset icons use the client's art, unverified in game.
