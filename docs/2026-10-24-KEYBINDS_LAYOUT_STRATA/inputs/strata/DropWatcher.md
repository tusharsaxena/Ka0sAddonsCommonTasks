# DropWatcher — frame strata analysis

Item 030. Read-only analysis of `../DropWatcher` on `master` (2026-10-24) and of the vendored
`libs/LibKa0s/`. Explicit strata calls in the addon: **6**, in 5 files (`Window.lua:531`,
`Toast.lua:384`, `OfferPanel.lua:202` and `:265`, `DetailCard.lua:663`, `CompactChrome.lua:301`).
Explicit `SetFrameLevel` calls in the addon: **0**. `SetToplevel` calls: **0**. The only level number the
addon chooses is the glow's relative level, `Glow.FRAME_LEVEL = 2` (`modules/Glow.lua:47`). There is no
strata constant: every strata is a string literal at its call site.

Levels below are written relative to the main window's own level, **W**. A child made by `CreateFrame`
with no `SetFrameLevel` is at parent + 1. "Inherited" strata means no `SetFrameStrata` call, so the
frame follows its parent.

## Inventory

| element | file:line | parent | strata | frame level | toplevel / clamped | notes |
|---|---|---|---|---|---|---|
| Main window `DropWatcherWindow` (`NS.Constants.WINDOW.NAME`; full and compact are one frame) | modules/Window.lua:530-533 | UIParent | **MEDIUM**, explicit | inherited (UIParent + 1), **W** | not toplevel / clamped | Movable, resizable, in `UISpecialFrames` (:546) |
| Resize grip (LibKa0s `MakeResizable`) | Window.lua:496 → libs/LibKa0s/Core.lua:605-611 | window | inherited MEDIUM | explicit relative **W+10** (`GRIP_LEVEL`) | — | The library chooses the level |
| Title bar, its icon/text buttons, mode words, "new" chip | modules/WindowTitleBar.lua:300, :167, :183, :231, :250, :265 | window | inherited | W+1, buttons W+2 | — | Drag handle for the window is the title bar (:305-307) |
| Body, tab strip, tabs, panes | Window.lua:459, :415, :398, :426 | window | inherited | W+1 … W+3 | — | |
| Filter-bar host / footer host | Window.lua:465, :472 | body | inherited | W+2 | — | |
| Test-mode strip (amber) and simulation strip (cyan), LibKa0s `W.TestStrip` | Window.lua:447, :451 → core/WidgetsSetup.lua:68 | body | inherited | W+2 | — | Laid in the body between filter bar and panes, so it does not overlap the content |
| Filter-bar dropdowns (View, Quality, Content) and footer Sort, LibKa0s `W.Dropdown` | WindowFilterBar.lua:580, :622; WindowFooter.lua:216 | filter host / footer host | inherited | W+3 | — | |
| **Dropdown popup menu** (process-wide singleton) | libs/LibKa0s/Widgets.lua:224-225 | UIParent | **FULLSCREEN_DIALOG**, explicit (library) | inherited | — | Closed on window hide (Window.lua:518) |
| Search box, LibKa0s `W.SearchBox` | WindowFilterBar.lua:676 | filter host | inherited | W+3 | — | |
| Drops table: header, scroll, content, rows, group headers, cells | WindowGroup.lua:914, :932, :935, :641, :662, :320, :592 | pane | inherited | W+3 (scroll) … W+6 (cells) | — | Rows are pooled (core/PoolSetup.lua) |
| History table: header, info strip, scroll, rows, cells | WindowHistory.lua:501, :519, :540, :383, :351 | pane | inherited | W+3 … W+6 | — | |
| Drops strip / empty state | DropsStrip.lua:95, :132 | pane | inherited | W+3 | — | |
| Compact cards (Drops, History), hit frames, scroll | CompactGroup.lua:617, :326, :187; CompactHistory.lua:56 | pane | inherited | W+3 … W+6 | — | |
| **Compact "Filters" button and panel** (holds the 4 dropdowns in compact) | CompactChrome.lua:280, **:300-301** | button: filter host; panel: **window** | panel **DIALOG**, explicit | panel inherited, **W+1** | — | A popover over the window's own rows. *(review)* The four filter dropdowns are **reparented** into it (`CompactChrome.lua:325`, `dd:SetParent(p)`), so in compact they take the panel's DIALOG strata, and back to the filter host's MEDIUM in full (`WindowFilterBar.lua:720`) |
| Detail card (expanded row) and its boxes, chips, Replaces rows | DetailCard.lua:319, :99, :169, :189 | scroll content | inherited | W+5 … W+8 | — | Inline in the scroll, so it is clipped like a row |
| **Edit message box** (Edit before sending) | DetailCard.lua:658-670 | **window** | **DIALOG**, explicit | inherited, **W+1** | not toplevel / not clamped | Centered over the window; only shown while the window is shown (core/DropWatcher.lua:277). Its `EditBox` child (DetailCard.lua:647, inside the `box` frame) inherits |
| **Offer panel** | OfferPanel.lua:198-212 | **window** | **MEDIUM** (:202), then **re-set per dock**: MEDIUM docked left/right, **DIALOG floating** (:265) | inherited, **W+1** | — | Strata changes at runtime; floating = over the window's right side |
| Offer panel rows, header cells, scroll | OfferPanel.lua:89, :108, :156, :186 | panel | inherited | panel + 1 … + 3 | — | |
| Item buttons (every icon: rows, cards, detail card, toast, History, Offer panel) | WindowGroup.lua:468 (callers: DetailCard.lua:164/:202, CompactGroup.lua:260, CompactHistory.lua:63, OfferPanel.lua:141, Toast.lua:397, WindowHistory.lua:372) | its cell/card | inherited | parent + 1 (in the window that is W+5 … W+9) | — | |
| Icon border frame (Window › Icons) | IconStyle.lua:118-119 | item button | inherited | **implicit** button + 1 | — | Glow.lua:47 says "at 1" but no code sets it. It is the CreateFrame default |
| **Upgrade glow** (LibCustomGlow via LibKa0s-Glow) | Glow.lua:47, :135 → libs/LibKa0s/Glow.lua:112 | item button | inherited | explicit relative **button + 2** | — | Over the border; library default would be +8 |
| Toast `DropWatcherToast` | modules/Toast.lua:382-389 | UIParent | **HIGH**, explicit | inherited | not toplevel / clamped | Movable (drag in test mode, Toast.lua:272); its own icon, Ask and close buttons inherit |
| GameTooltip (item and cell tooltips) + TipGrid holder | Window.lua:227; WindowGroup.lua:445; TipGrid.lua:83 | GameTooltip | TOOLTIP (Blizzard) | holder inherited | — | Placement by RowTooltip.lua:132-148, beside the docked panel when there is one |
| Simulation step panel (LibKa0s-Sim) | modules/SimPanel.lua:124 (`anchorTo` = window) → libs/LibKa0s/SimPanel.lua:211 | UIParent | **DIALOG**, explicit (library) | inherited | clamped | Docks **right** of the window, else left, else floats at CENTER+420 |
| Debug console (LibKa0s-DebugLog) | core/DebugLogSetup.lua:82 → libs/LibKa0s/DebugLog.lua:536 | UIParent | **DIALOG**, explicit (library) | inherited | clamped | |
| *(review)* Debug console's **Copy** window (LibKa0s `W` copy frame) | libs/LibKa0s/DebugLog.lua:898 → Widgets.lua:647-653 | UIParent | **FULLSCREEN**, explicit (library) | inherited | clamped | Above the DIALOG console that opens it, by design (Widgets.lua:651-652) |
| Perf panel (LibKa0s-Perf) | core/PerfSetup.lua:48 → libs/LibKa0s/PerfPanel.lua:186 | UIParent | **DIALOG**, explicit (library) | inherited | clamped | Only during `/dw perf` |
| StaticPopups: Clear history, retention shrink, Reset all | History.lua:607; HistoryRetention.lua:244; settings reset popup | Blizzard | DIALOG (Blizzard) | Blizzard | — | |
| Launcher right-click menu | core/Compat.lua:884 (MenuUtil) | Blizzard | Blizzard menu strata | — | — | |
| Minimap button (LibDBIcon via LibKa0s-Launcher) | core/LauncherSetup.lua:73 | Minimap | Minimap's (LibDBIcon) | LibDBIcon | — | |
| Key-binding click target `DropWatcherToggleWindow` | core/LauncherSetup.lua:33 | UIParent | inherited, hidden | — | — | Never shown; not visual |
| *(review)* Other plain children: header cells, info strips, footer sort host, Offer list content, situations-table rows and hit frames | WindowGroup.lua:920; WindowHistory.lua:507; DropsStrip.lua:104; WindowFooter.lua:193; OfferPanel.lua:189; settings/PageEditors.lua:184, :195 | their builders' parents | inherited | parent + 1 | — | No strata or level of their own; listed for completeness |
| Settings: Situations table host | settings/PageEditors.lua:227 (re-hosted per render) | panel → placeholder | inherited (Blizzard Settings canvas) | parent + 1 | — | Its cells are AceGUI CheckBox/Dropdown (AceGUI pullouts are AceGUI's own strata) |

## Problems

| id | file:line | problem |
|---|---|---|
| DRO-S01 | DetailCard.lua:663, OfferPanel.lua:265, CompactChrome.lua:301 | **Three window popovers tie at DIALOG / W+1.** The Edit message box, the floating Offer panel and the compact Filters panel are all children of the window, all set to DIALOG, all at the CreateFrame default level W+1. When two overlap, creation order decides who draws on top, not intent. A concrete case: with no room beside the window, the Offer panel floats over its right side. Pressing Offer with Edit before sending on opens the Edit box centered over the window, and the box can draw **under** the Offer panel that opened it. |
| DRO-S02 | modules/SimPanel.lua:124-127 vs OfferPanel.lua:248-268 | **The simulation panel and the docked Offer panel dock to the same side.** Both prefer the window's right edge. The sim panel is DIALOG and the Offer panel MEDIUM, so during a simulation the sim panel covers the Offer panel completely. The strata fixes who wins, but the overlap is the defect. |
| DRO-S03 | OfferPanel.lua:202, :265 | **Strata switched at runtime as a stand-in for a level.** The Offer panel goes MEDIUM ↔ DIALOG on every dock. It only needs DIALOG when floating because, at W+1, it would sit *under* the window's own rows (W+5 and up). This is a level problem solved by a strata jump. It also lifts a floating panel above every HIGH frame on screen, the addon's own toast among them, and into the same strata as Blizzard's StaticPopups. |
| DRO-S04 | (all six call sites) | **No strata vocabulary.** Six literal strings across five files, no constant, and no comment that states the addon's layering as a whole. Each site's reason is local. "Popover over the window" is spelled DIALOG in three files, which is consistent today only by accident. |
| DRO-S05 | Window.lua:530-533 | **The main window is not toplevel.** At MEDIUM with `SetToplevel` unset, a click does not raise it over another MEDIUM frame it overlaps (other addons' windows, Blizzard panels at MEDIUM). Clicking into Drop Watcher can leave it half-covered. DpsRace's Results window sets `SetToplevel(true)` (DpsRace/modules/Results.lua:212, on a HIGH frame, :208), so the collection is inconsistent. |
| DRO-S06 | IconStyle.lua:118-119, Glow.lua:47 | **An implicit level that a comment treats as explicit.** The icon border relies on the CreateFrame default (button + 1), and the glow's `FRAME_LEVEL = 2` is "one over the border" only because of that default. If a future change sets a level on the border, or adds another child to the item button before it (a cooldown, a count frame), the glow can end up below the border. |
| DRO-S07 | Window.lua:496 → Core.lua:611 vs WindowGroup/DetailCard nesting | **Nesting depth approaches the grip's band.** Content nests to about W+8 (detail card › side › row › item button) and +10 for that button's glow, while the library grip sits at W+10. No visible collision exists today: the grip lives in the footer corner, and the scroll frame clips content above the footer. But the two bands are not separated by design. Low severity. |
| DRO-S08 | Toast.lua:384 vs DetailCard.lua:663 | The toast (HIGH) can sit over the window (MEDIUM), which is intended because an alert should be seen. But a floating Offer panel or the Filters panel (DIALOG) draws over the toast, so a transient window popover beats the alert. The order is accidental, not chosen. |
| ~~DRO-S09~~ | DetailCard.lua:660-670 | ~~The Edit message box is not clamped to the screen.~~ *(review: not a defect.)* The box is centered on the window, the window is clamped (Window.lua:533), and the box (`EDITOR_W` 380 × `EDITOR_H` 156, `core/Constants.lua:106-107`) is smaller than the window's least size in either layout (`COMPACT_MIN_W` 400, :53). So it can never leave the screen. |
| DRO-S10 | CompactChrome.lua:300-301, :325 | *(review)* The compact Filters panel's four dropdowns are reparented into it, so any strata or level change to the panel moves them as well. Today they draw at DIALOG and their menu at FULLSCREEN_DIALOG. Any re-tiering of the panel (Z03) has to be checked with a dropdown opened from inside it. |

## Proposed strata map

One addon-wide table, `K.STRATA` / `K.LEVEL` in `core/Constants.lua`, read by every call site.

| tier | strata | level band | elements |
|---|---|---|---|
| 0 · window | **MEDIUM** | W (inherited from UIParent) | Main window (full and compact), docked Offer panel |
| 0a · window content | MEDIUM, inherited | W+1 … W+12 (whatever nesting gives) | title bar, body, strips, tables, cards, detail card, item buttons; icon border = button **+1 explicit**; glow = button **+2** |
| 0b · window chrome above content | MEDIUM, inherited | W+15 (`K.LEVEL.GRIP`) | resize grip (library; today +10. See upstream note) |
| 1 · window popovers | **MEDIUM**, same strata as the window | **W+30** floating Offer panel, **W+35** compact Filters panel | Above every content level, so no strata jump is needed. Stays below the toast, Blizzard popups and the library's menus. |
| 2 · window modal | **DIALOG** | W+40 explicit, toplevel | Edit message box: the one thing the player must answer before going on. Above every popover in the addon. |
| 3 · alert | **HIGH** | inherited | Toast. Above the window and its popovers, below any modal. |
| 4 · tool panels (library) | DIALOG (library-owned) | inherited | Simulation panel, debug console, perf panel. Dock beside, never over, the window and its docked panel. |
| 4a · tool sub-windows (library) | FULLSCREEN (library-owned) | inherited | Debug console's Copy window, above the console that opens it |
| 5 · menus (library) | FULLSCREEN_DIALOG (library-owned) | inherited | Dropdown popup menu, which must beat every tier above because the Filters panel's dropdowns open from tier 1. |
| 6 · tooltips (Blizzard) | TOOLTIP | — | GameTooltip + TipGrid holder |

Invariants to keep: a popover is above its own window's content (tier 1 > 0a). The modal is above every
popover (2 > 1). The alert is above the window but below the modal (0 < 3 < 2). Menus are above
everything they open from (5 > 1, 2, 4). No frame changes strata at runtime.

## Proposed changes

| id | change (file:line, from → to) | reason | confidence |
|---|---|---|---|
| DRO-Z01 | core/Constants.lua: add `C.STRATA = { WINDOW = "MEDIUM", MODAL = "DIALOG", ALERT = "HIGH" }` and `C.LEVEL = { POPOVER_OFFER = 30, POPOVER_FILTERS = 35, MODAL = 40, ICON_BORDER = 1, GLOW = 2 }`, then replace the six literals with them (Window.lua:531, Toast.lua:384, OfferPanel.lua:202/:265, DetailCard.lua:663, CompactChrome.lua:301). `C` here is the file's local for `NS.Constants` (`core/Constants.lua:8-9`), so modules read `NS.Constants.STRATA`/`.LEVEL`, not `NS.C` (the profile defaults). | One vocabulary and one place that states the layering. Fixes S04. A pure refactor, no visible change. | 90% |
| DRO-Z02 | OfferPanel.lua:265: `SetFrameStrata(side == "float" and "DIALOG" or "MEDIUM")` → always `C.STRATA.WINDOW`, plus `SetFrameLevel(win:GetFrameLevel() + (side == "float" and C.LEVEL.POPOVER_OFFER or 1))`. Drop the strata line at :202. | A floating panel needs to beat the window's rows, not every HIGH frame. A level does that without a runtime strata jump. Fixes S03 and the panel half of S08. *(review)* Safe for interactions: the floating panel lies inside the window's bounds (`dock`, OfferPanel.lua:261-262), so nothing outside the window can newly cover it. Its rows' GameTooltip stays TOOLTIP, and its children re-level with it (the client moves child levels with the parent unless `SetFixedFrameLevel`). Docked left or right it stays at W+1, as today. | 70% |
| DRO-Z03 | CompactChrome.lua:301: `SetFrameStrata("DIALOG")` → `SetFrameLevel(f:GetFrameLevel() + C.LEVEL.POPOVER_FILTERS)` (strata inherited MEDIUM). | Same reasoning as Z02. It sits above the floating Offer panel because it is the more transient of the two. The library menu (FULLSCREEN_DIALOG) still opens above it. Fixes S01 and S08 for this panel. *(review)* Two checks. (1) Set the level at build (`buildPanel`) **before** `fillPanel` reparents the dropdowns (S10), so they land at panel + 1. (2) Unlike the floating Offer panel, this panel hangs under the filter button and can reach past a short compact window's bottom edge. There, another addon's MEDIUM frame at a higher level could now draw over it, where DIALOG wins today. Smoke-check it with a dropdown opened from the panel. | 60% |
| DRO-Z04 | DetailCard.lua:663: keep `DIALOG` (via `C.STRATA.MODAL`), add `e:SetFrameLevel(win:GetFrameLevel() + C.LEVEL.MODAL)` and `e:SetToplevel(true)`. *(review: dropped the draft's `SetClampedToScreen`, because S09 cannot happen.)* | The modal must always win over the popovers it is opened from. Today it ties with them (S01). If Z02 and Z03 land, the strata alone separates it, and the level is belt-and-braces. If only Z04 lands, the level alone fixes S01. | 75% |
| DRO-Z05 | Window.lua:531: add `f:SetToplevel(true)` after the strata line. | A click raises the window among MEDIUM frames, as DpsRace's Results window does. Fixes S05. *(review)* A raise changes W at runtime. The explicit child levels of Z02, Z03, Z04 and Z06 and the grip's +10 move with it, because the client re-levels children with their parent. Z02 recomputes on every `dock` anyway. UISpecialFrames and the grip are unaffected. It is still a behaviour change (the window now comes to the front on click), so it needs a smoke check against another addon's MEDIUM window. | 65% |
| DRO-Z06 | IconStyle.lua:119: after `SetAllPoints`, `f:SetFrameLevel(b:GetFrameLevel() + C.LEVEL.ICON_BORDER)`. Glow.lua:47: `Glow.FRAME_LEVEL = C.LEVEL.GLOW`, with the comment stating "border + 1". | Makes the border < glow ordering explicit instead of relying on the CreateFrame default. Fixes S06. | 85% |
| DRO-Z07 | *(rewritten in review)* **Let the Offer panel avoid the sim panel's side**, not the other way round. In `OfferPanel.lua` `dock` (:248-268), when the sim panel is shown and sits right of the window (its `GetLeft()` ≥ the window's `GetRight()`), dock left if `MC.DockSide` says left fits, else float. `F.anchorTo` (modules/SimPanel.lua:124-127) keeps answering the window. | Removes the S02 overlap. The draft's version (anchor the sim panel to a right-docked Offer panel) **breaks**. The library's `place` (libs/LibKa0s/SimPanel.lua:834-852) docks *left* of its anchor when the right has no room, and left of a right-docked Offer panel is on top of the window, at DIALOG over MEDIUM. The library also redocks only on Show (:52-53), so an Offer panel opened while the sim panel is up would never move it. The Offer panel redocks on every open, so it is the side that can adapt. Reading `frame.__dock` would couple to a library-private field, so compare edges, or add a public side accessor to LibKa0s-Sim (upstream). | 45% |
| DRO-Z08 | Toast.lua:384: no change (stays HIGH, via `C.STRATA.ALERT`). | Tier 3 is right: above the window, below the modal. Listed so the owner sees it was checked. | 90% |

## Notes for the upstream guidance

- **State the layering once, per addon, as constants.** A short table (window / popover / modal / alert)
  at the top of the constants file, and no strata literal at call sites. DropWatcher's six literals were
  each locally right and still collided (S01).
- **A popover over its own window is a *level* problem, not a strata problem.** Prefer the window's
  strata + a level band clear of the deepest content (window + 30) over jumping to DIALOG. A strata jump
  lifts the popover above every unrelated HIGH frame, the addon's own alert included (S03, S08).
- **Never switch strata at runtime** to change ordering. Set a level instead, or keep two frames.
- **Children that must order among themselves get explicit levels** (border +1, glow +2), not the
  CreateFrame default. The default is an accident of creation order (S06).
- **One modal tier, toplevel and clamped.** An input box the player must answer sits on DIALOG at an
  explicit level above every popover, with `SetToplevel(true)` and `SetClampedToScreen(true)`.
- **Main windows: `SetToplevel(true)`** so a click raises them (DpsRace already does). Pick one strata
  for collection main windows. Today it is MEDIUM here and in DpsRace's HUD and QuickComms' pad, and HIGH
  in LootHistory's and BankLedger's browsers. Suggest MEDIUM for always-on HUD-like windows and HIGH
  for browse-on-demand windows, written down as a rule.
- **Docked companions must negotiate sides.** When an addon docks more than one panel beside its
  window (an Offer panel, the library's sim panel), the later one anchors to the outermost docked
  panel, not to the window (S02). Worth a sentence in standalone-windows and possibly an
  `anchorTo` convention in LibKa0s-Sim.
- **Library-owned strata are part of the map.** Menus at FULLSCREEN_DIALOG, tool panels at DIALOG and
  the grip at frame + 10 should be documented in `docs/api/` with the reason, so an addon can place its
  own tiers around them. The grip's +10 is within reach of ordinary nesting depth (S07). A larger fixed
  offset, or a documented "content stays below +10" rule, would close that.

## Review

Independent review against `../DropWatcher` on `master` and its vendored `libs/LibKa0s/`, 2026-10-24.
Re-grepped every `CreateFrame`, `SetFrameStrata`, `SetFrameLevel`, `SetToplevel` and
`SetClampedToScreen` outside `libs/`. The six strata calls, zero level calls and zero toplevel calls
are confirmed.

- **Inventory fixes.** The main window's global name is `DropWatcherWindow`, not `DropWatcherFrame`
  (`core/Constants.lua:20`). Added rows for: the debug console's Copy window (library, FULLSCREEN), the
  Edit box's `EditBox` child, the remaining plain children (header cells, strips, footer host, Offer
  list content, situations-table rows), and the reparenting of the compact filter dropdowns into the
  Filters panel (`CompactChrome.lua:325`). Added tier 4a to the map for the Copy window.
- **S09 struck.** The Edit box (380×156) is centered on a clamped window whose least size is 400 wide,
  so it can never go off-screen. The `SetClampedToScreen` part of Z04 was dropped, and Z04 went
  80% → 75%.
- **S10 added.** The reparented dropdowns take on the Filters panel's strata, so Z03 must set the
  panel's level before `fillPanel` and be smoke-checked with a dropdown opened from the panel.
- **Z07 rewritten, 60% → 45%.** The draft would have docked the sim panel (DIALOG) over the window
  whenever the right of a right-docked Offer panel had no room (`libs/LibKa0s/SimPanel.lua:834-852`
  falls back to the left of the anchor). It also never re-docks an already-shown sim panel (:52-53).
  The Offer panel now picks the free side instead.
- **Z02 confirmed safe.** The floating Offer panel stays inside the window's bounds, so going from
  DIALOG to MEDIUM+30 loses nothing to outside frames. Tooltips stay TOOLTIP and menus stay
  FULLSCREEN_DIALOG.
- **Z03 lowered, 65% → 60%.** This panel can hang past a short compact window's edge, and there a
  MEDIUM frame from another addon could now cover it.
- **Z05 lowered, 70% → 65%.** Being raised on click is a visible behaviour change. Noted that the
  explicit child levels move with the raised parent.
- **Z01 clarified.** The constants are `NS.Constants.*` (the file's local `C`), not `NS.C`.
- **S05 evidence.** DpsRace's toplevel Results window is HIGH (`Results.lua:208`), not MEDIUM. The
  cross-addon strata list in the upstream notes was re-verified: LootHistory and BankLedger browsers
  HIGH, DpsRace HUD MEDIUM, QuickComms pad MEDIUM.
- **No combat-protected frames are involved.** DropWatcher has no secure templates apart from the
  hidden binding button (`core/LauncherSetup.lua:33`, a plain `Button` that is never shown), so no
  change here touches taint.

