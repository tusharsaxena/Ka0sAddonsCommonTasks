# A right-click on an unlock strip opens what its gear opens

Created 2026-11-23 from the owner's smoke feedback of the same day. Branch `feat/2026-11-23-strip-right-click` in
LibKa0s, WowAddonStandards, Ka0sAddonsCommonTasks and each addon that changes (the items below). AbsorbTracker's
branch stacks on `feat/2026-11-23-absorbtracker-feedback` and AuraMaster's on
`feat/2026-11-23-auramaster-preset-restack`, the branches those live repos sit on; every other repo branches from
`master`.

## The owner's words

> [Image #31] Right clicking on any unlock strip should open the relevant settings page - same way as clicking the
> gear icon
> - This seems to work for AuraMaster but not AbsorbTracker (abosrbTracker gear icon works, right clickign strip
>   doesnt work)
> - Make this an upstream standard and audit all addons that have this kind of strip, and audit and fix their
>   behavior to confiom to the standard.

## Why AbsorbTracker failed and AuraMaster worked

LibKa0s `WidgetsDragHandle` through minor 16 registered a right-click only when the host passed `spec.onRightClick`
(`dhSetClick`: "NO CLICK REGISTRATION AT ALL without a handler"). The gear has been on by default since minor 15, but
nothing tied the right-click to it. AuraMaster passes `onRightClick` with the same function as its gear
(`modules/Anchors.lua:721`, `:726`). AbsorbTracker passes only `onSettings` (`modules/Bar.lua:166`), so its strip
registered no click at all.

## The audit (2026-11-23, every roster addon plus LibKa0sSkinTester)

An **unlock strip** is the strip a HUD display shows while it is unlocked, to be dragged by. Window title bars are
recorded below for completeness but are not unlock strips (decision D3). "Today" is each live repo's checked-out
branch with its vendored LibKa0s v1.109.0 (`WidgetsDragHandle` minor 16).

| Addon | Unlock strip (implementation) | Gear's left click | Right-click today | Fix |
|---|---|---|---|---|
| AbsorbTracker | each unit bar's strip (`DragHandle`, `modules/Bar.lua:110`) | `onSettings`: `NS.OpenUnitSettings(unit)`, the Appearance page on that unit (`:166`) | **nothing** (no `onRightClick`, no click registered) | revendor-only |
| AuraMaster | each container's strip (`DragHandle`, `modules/Anchors.lua:708`) | `settings`: `openSettings(container)`, the Containers page on that container (`:721`) | the same function (`onRightClick`, `:726`); the owner's working reference | revendor-only (drop the redundant `onRightClick`, standard SHOULD) |
| BankLedger | none (browser, session and export windows: title bars) | — | — | none-no-strips |
| CombatTrail | the call-out's strip (`DragHandle` built by LibKa0s `Callout.lua:696`, through `core/CalloutSetup.lua`) | `onSettings`: `NS.CalloutSettings()`, the Race mode page on its Callout tab (`CalloutSetup.lua:95`) | **nothing** | revendor-only |
| CombatTrail (other) | the HUD and Race window title bands (window headers, `modules/Hud.lua:511`, `modules/RaceWindow.lua:289`); the lanes' edit overlays (`modules/LaneAnchor.lua:358`, whole-frame, no marks) | header gear / none | nothing | not unlock strips (D3); the overlays carry no gear, so the rule has nothing to mirror |
| ConsumableMaster | the macro bar's strip (`DragHandle`, `modules/MacroBar.lua:267`) | `settings`: `openBarSettings`, the Macro Bar page (`:309`) | **nothing** | revendor-only |
| DropWatcher | none (drop feed and roll popup: title bars; the feed's title-bar click is left-button only) | — | — | none-no-strips |
| KickCD | cast-bar strip (`DragHandle`, `modules/Castbar_Handle.lua:140`) and icon-grid strip (`modules/IconGrid_Handle.lua:160`) | `settings`: `NS:OpenUnitSettings(unit, "castbar")` / `(unit, "icons")`, the unit's entry on the Units page (`:158`, `:175`) | **another page**: `onRightClick = NS:OpenSettings()`, the root page (`:151`, `:170`) | revendor-and-code |
| LibKa0sSkinTester | the showroom's demo strip (`DragHandle`, `modules/ShowroomWidgets.lua:78`) | default gear: Core `OpenSettings(owner)` | **nothing** | revendor-only |
| LootHistory | none (browser and export windows: title bars) | — | — | none-no-strips |
| MultiMeters | none (meter windows' title bands, `modules/Window_Frame.lua:281`; no right-click on the band) | — | — | none-no-strips |
| OutfitterReborn | none that is an unlock strip; the outfit bar's title band has its own drag strip (`modules/Bar_Chrome.lua:145`) | header gear: `NS.OpenOptionsPanel("bar")` (`:121`) | the same page (`OnMouseUp`, `:154`) | none-no-strips (already matches; D3) |
| PanelMaster | none (an unlocked panel is dragged by its own frame and outline, no strip, no marks) | — | — | none-no-strips |
| PartyFrameEnhanced | none with marks (the unlocked stack's caption grip, `modules/Anchor.lua:311`, has no gear) | — | — | none-no-strips |
| PremadeGroupsFilterExtension | none | — | — | none-no-strips |
| PrettyChat | none | — | — | none-no-strips |
| QuickComms | each Comms Pad's strip (`DragHandle` through `NS.MakeDragHandle`, `modules/Pad.lua:354`) | `settings`: `Pad.OpenSettings(id)`, the pad's own page (`:373`) | **another page**: `onRightClick = NS.addon:OpenSettings()`, the root page (`:368`) | revendor-and-code |
| RangeMaster | each screen display's strip (`DragHandle`, `modules/Anchors_Screen.lua:146`) | `settings`: `openSettings(inst)`, the Containers page on that display (`:150`) | the same function (`onRightClick`, `:155`) | revendor-only (drop the redundant `onRightClick`) |
| SkillMaster | detached group windows' bands (`modules/Groups.lua:633`, own `Button`, settings mark via `NS.Detached.BandMarks`) and sub-headers (`:594`) | the band's settings mark | **another target**: the group menu (`G.Menu`, `:613`, `:551`) | deferred (another agent holds the repo; needs D3's ruling on window bands first) |
| WhatGroup | none (the group popup's title bar) | — | — | none-no-strips |

DpsRace is retired and left out.

## Decisions

- **D1. The library does it by default.** `WidgetsDragHandle` minor 17 (`SRC-LK-01`): a strip that carries the
  settings mark and no `onRightClick` answers a right-click, on the band and on each mark, with the mark's own action
  (`dhOpenSettings`: `settings` when a function, else `onSettings`, else Core `OpenSettings`). A host's explicit
  `onRightClick` still wins. A strip with `settings = false` and no `onRightClick` still registers no click (no
  consumer builds one today: ConsumableMaster's strip gained its gear at AF-STRIP-CM, so it is not that case any
  more). LibKa0s v1.111.0 is tagged **locally** at `ee9b4c97`; pushing and merging wait for the owner.
- **D2. The standard's rule** (`SRC-STD-01`, v2.118.0): standalone-windows, *The drag strip's marks*, *A right-click
  opens what the gear opens* (MUST), anti-pattern #123, the AUDIT.md step 4 line. A `DragHandle` host passes no
  `onRightClick`, and none that opens anything else without a waiver row; an addon-drawn unlock strip wires its
  right-click to its settings mark's function. Binds at the re-vendor of v1.111.0 for a `DragHandle` strip.
- **D3. Scope is the unlock strip, not every title bar.** The owner's words name "unlock strip" and the strip in
  image 31. A window's title bar is a different surface with its own rules (standalone-windows, *Title-bar
  controls*); OutfitterReborn's bar band already answers a right-click with its gear's page, and SkillMaster's group
  bands answer one with a menu. Widening the rule to title bars is an **open question for the owner**, and
  SkillMaster's fix waits on that answer.
- **D4. KickCD and QuickComms drop their `onRightClick`.** Each opened the root page while the gear opened the
  unit's or the pad's own page. Their strip tooltips ("Right-click for settings.") stay true.
- **D5. AuraMaster and RangeMaster drop their redundant `onRightClick`** at the re-vendor, so one function backs
  both the gear and the right-click and the two cannot drift.
- **D6. Addons with no unlock strip are not re-vendored by this run.** Each vendors its own pinned copy, and the
  in-client winner is the newest minor any installed addon ships, so their behavior does not depend on it. They pick
  up v1.111.0 at the next sweep.
- **D7. The re-vendor spans v1.110.0.** Every affected addon vendors v1.109.0 today, so its re-vendor also brings
  Compat minor 6 and kit revision 60 (LibKa0s#101); a suite pinning `Compat 5`, `KIT_VERSION` 59 or
  `WidgetsDragHandle 16` re-pins.
- **D8. CombatTrail's ids are `SRC-CTR-*`**, because `SRC-CT-*` is this repo's.

## Items

`plan-data/items.tsv`. Done = a commit whose subject starts `<ID>: ` in the owning repo; `plan-data/resume-state.sh`
computes progress (`BR=feat/2026-11-23-strip-right-click`). Gates per repo: `ka0s-bounded lua tests/run.lua`, plus
`KA0S_KIT_CLIENT=forever` where the TOC carries 16001, `ka0s-bounded luacheck .` 0/0, the 1500-line cap and CCN 15.
No addon version bumps, no pushes, no merges without the owner's go-ahead.

## Smoke checks (the owner's to run, in game)

- **SRC-S1 AbsorbTracker.** Unlock the bars. Right-click a bar's strip, then its `?` and its X: each opens the
  Appearance page on that bar's unit, as the gear does.
  Result:
- **SRC-S2 AuraMaster.** Unlock. Right-click a container's strip: the Containers page on that container, as before
  and as the gear.
  Result:
- **SRC-S3 ConsumableMaster.** Unlock the macro bar. Right-click its strip: the Macro Bar page, as the gear.
  Result:
- **SRC-S4 CombatTrail.** Unlock the call-out. Right-click its strip: the Race mode page on its Callout tab, as the
  gear.
  Result:
- **SRC-S5 KickCD.** Unlock. Right-click the cast-bar strip, then the icon-grid strip: each opens that unit's Cast
  bar or Icons entry on the Units page, as its gear, no longer the root page.
  Result:
- **SRC-S6 QuickComms.** Unlock a pad. Right-click its strip: the pad's own page, as the gear, no longer the root.
  Result:
- **SRC-S7 RangeMaster.** Unlock. Right-click a screen display's strip: the Containers page on that display.
  Result:
- **SRC-S8 Skin Tester.** In the showroom, right-click the demo drag strip: the Skin Tester's settings, as its gear.
  Result:
- **SRC-S9 Left click and drag unchanged.** On any strip above, a left-drag still moves the display and a left click
  on the strip opens nothing; the X's left click still closes.
  Result:
