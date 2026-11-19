# HUD header audit (2026-11-19, read-only, at the merged adoption heads)

`W.HeaderButtons` (LibKa0s/LibKa0s/WidgetsHeader.lua:261-284) builds `close` (on by default), `settings` (on by
default; turning it off needs `settingsOptOut`) and `extras`. Lock is not built in, so every lock today is an
`extras` entry.

## Primary windows

| Addon | Window | Header call | Close / Settings / Lock | Ruling |
|---|---|---|---|---|
| BankLedger | Ledger browser | modules/Browser.lua:1034 (strip Browser_Chrome.lua:105) | Y / Y / missing | add a lock that toggles `settings.locked` (launcher verb core/LauncherSetup.lua:248), plus `/bl lock` |
| LootHistory | History browser | modules/Browser.lua:1074 (strip :97, core/WidgetsSetup.lua:406) | Y / Y / missing | add a lock that toggles `settings.locked` (core/LauncherSetup.lua:233), plus `/lh lock` |
| LibKa0sSkinTester | Skin showroom | modules/Showroom.lua:261 | Y / Y / missing (no lock concept) | waived (dev tool) |
| OutfitterReborn | Outfit window | modules/Window.lua:239 | Y / Y / missing | waived (docked; drag only undocked in test mode, Dock.lua:225-228) |
| QuickComms | Comms Pads | modules/Pad_Render.lua:887 (`close=false, settings=false`) | missing / missing / missing | add all three. Settings uses `NS.addon:OpenSettings`, lock uses `NS.SlashVerbs.ToggleLock`, and close hides that pad (restorable). Settings today sits only on the strip (Pad.lua:336, :349-350) |
| WhatGroup | Group info popup | modules/FrameLayout.lua:43 | Y / Y / missing | add a lock that calls `NS.addon:SlashToggleLock()`, plus `/wg lock`. The bottom Close (FrameLayout.lua:194-197) stays as a deviation row |

Already compliant: CombatTrail HUD (Hud.lua:508) and Race window, DropWatcher feed window, MultiMeters meter
windows, OutfitterReborn outfit bar, SkillMaster main window.

## Secondary windows without close

| Addon | Window | Call | Ruling |
|---|---|---|---|
| SkillMaster | Detached block windows | modules/Detached.lua:162-163 | waived (the dock mark is the way back) |
| SkillMaster | Group windows | modules/Groups.lua:645 | waived (same) |
| PremadeGroupsFilterExtension | Filter panel | modules/Panel.lua:954-956 | waived (a docked child of PGF's dialog) |

## Footers

Footer marks are actions, which the rule allows: DropWatcher's scan, post, reset and Expand/Collapse all, its Offer
panel's Announce, OutfitterReborn's New, None and All, and CombatTrail's Race footer row. The only window control
outside a header is WhatGroup's bottom Close, ruled as a deviation.

## Drag strips (DragHandle), for AF-LK-01, AF-LK-02 and AF-STRIP-*

AbsorbTracker modules/Bar.lua:86 · AuraMaster modules/Anchors.lua:710 · ConsumableMaster modules/MacroBar.lua:251 ·
KickCD modules/Castbar_Handle.lua:94 and modules/IconGrid_Handle.lua:135 · QuickComms modules/Pad.lua:336 ·
RangeMaster (one) · LibKa0sSkinTester (showroom specimen).

Hosts passing `tooltipPlace`: AbsorbTracker, AuraMaster (2), ConsumableMaster and KickCD (2). Hosts with a settings
mark today: AbsorbTracker and ConsumableMaster. PanelMaster (modules/Unlock.lua:355) and PartyFrameEnhanced
(modules/Anchor.lua:324) draw their own unlock overlays, not a DragHandle.
