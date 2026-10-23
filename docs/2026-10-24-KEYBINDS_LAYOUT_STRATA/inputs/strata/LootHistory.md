# LootHistory — frame strata analysis

Item 030. Read-only analysis of `../LootHistory` on `master` plus the vendored
`libs/LibKa0s/` modules that create frames on its behalf. Paths are relative to `../LootHistory`;
`LK/` means `libs/LibKa0s/`.

The addon sets strata in exactly **four** places of its own: Browser.lua:936, Export.lua:468,
BrowserTable.lua:1198 and BrowserTable.lua:1207 (re-verified: `grep -rn SetFrameStrata` outside
`libs/` and `tests/` returns exactly these four). Everything else is either inherited from those
parents or chosen by LibKa0s or Blizzard. No addon frame calls `SetFrameLevel`, `SetToplevel` or
`Raise`.

## Inventory

| element | file:line | parent | strata | frame level | toplevel / clamped | notes |
|---|---|---|---|---|---|---|
| **History window** `LootHistoryWindow` | modules/Browser.lua:924, :936 | UIParent | **HIGH** (explicit) | default | not toplevel / clamped (:939) | Primary window. UISpecialFrames (:1089). Same strata as Blizzard's SettingsPanel (HIGH, per Blizzard_Settings XML; not verified in-session). |
| title bar (drag handle) | Browser.lua:943 | window | inherited HIGH | relative (+1) | — | Holds title, TEST/SIM badge FontString (:968), close button. |
| close button | Browser.lua:983 → core/CoreSetup.lua wrapper → LK/Core.lua MakeCloseButton | title bar | inherited | relative | — | Fallback build at CoreSetup.lua:60. |
| divider texture | Browser.lua:974 | window | ARTWORK layer | — | — | Region, not a frame. |
| tab strip + tab buttons | Browser.lua:254, :263 | window | inherited | relative | — | Underline texture ARTWORK. |
| filter bar host | Browser.lua:998 | window | inherited | relative | — | Dropdown buttons BrowserFilterBar.lua:331, Search EditBox :366. |
| test-mode strip / sim strip | Browser.lua:907 → LK Widgets TestStrip (core/WidgetsSetup.lua:295) | window | inherited | relative | — | Anchored under the filter bar; panes are pushed down by `TestStripReserve` (Browser.lua:142), so there is no overlap. |
| content panes (History, Insights, Holdings, Timeline) | Browser.lua:150 | window | inherited | relative | — | Shown one at a time. |
| History pane host | Browser.lua:863 (B:BuildTable) | pane | inherited | relative | — | Fills the pane; the table attaches to it. |
| History table: header, header buttons, faux scroll, row host, rows | BrowserTable.lua:917, :956, :925, :935, :746 | pane | inherited | relative | — | Row stripe BACKGROUND, highlight HIGHLIGHT, bound icon OVERLAY layers (:751, :756, :781). |
| Holdings table: header, header cells, scroll, content, rows | HoldingsTab.lua:477, :437, :486, :490, :325 | pane | inherited | relative | — | Same layer scheme as the History rows. |
| Insights: scroll, content, cards, day/value/hour/currency strips, bars, list panels | Analytics.lua:49, :53, :62, :216-222; AnalyticsCharts.lua:35, :69, :84, :125, :149, :165, :189, :213; AnalyticsLedger.lua:87 | pane | inherited | relative | — | Track BACKGROUND, axis OVERLAY. |
| Timeline: bar, strip, legend, buttons, line chart | Timeline.lua:200, :231, :236, :144, :154, :168; chart LK/WidgetsLineChart.lua:504 (Timeline.lua:249) | pane | inherited | relative | — | Hover is GameTooltip (Timeline.lua:539). |
| resize grip | LK/Core.lua:605-611 (via NS.MakeResizable) | window | inherited | **parent + 10** (`GRIP_LEVEL`, LK/Core.lua:546) | — | The library bumps the level so the grip clears the footer/pane children. |
| resize grip (degraded fallback) | core/CoreSetup.lua:96 | window | inherited | **relative +1 (no bump)** | — | Only without LibKa0s. |
| window inner-border highlight | LK Core ApplySkin; fallback core/CoreSetup.lua:233 | window | inherited | relative | — | A 1px BackdropTemplate child. |
| **Row context menu** (History + Holdings) | modules/BrowserTable.lua:1197-1198 | **UIParent** | **FULLSCREEN_DIALOG** (explicit) | default | not toplevel / **not clamped** | Host-built. Muted-gold edge (:1201), unlike the library menu's black edge. Menu rows :1265. |
| **Row-menu click catcher** | BrowserTable.lua:1205-1207 | UIParent | **FULLSCREEN** (explicit) | default | full-screen | Eats the dismissing click (both buttons registered, :1210). Hidden only by the menu's OnHide. |
| **Export modal** `LootHistoryExportWindow` | modules/Export.lua:463, :468 | UIParent | **DIALOG** (explicit) | default | not toplevel / clamped (:469) | UISpecialFrames (:544). Its OnHide closes the library dropdown menu (:534). |
| export title bar, buttons, Data set dropdown | Export.lua:481, :419, NS.MakeDropdown | modal | inherited | relative | — | — |
| **Export copy window** `LootHistoryExportCopyWindow` | Export.lua:368 → LK/Widgets.lua:653 | UIParent | **FULLSCREEN** (library) | default | clamped | Above the DIALOG modal by design (LK comment :651). |
| library dropdown menu (filter bar ×9, Export Data set) | LK/Widgets.lua:224-225 | UIParent | **FULLSCREEN_DIALOG** (library) | default | **not clamped** | Process-wide singleton. Dismissed by `GLOBAL_MOUSE_DOWN` and catches no clicks (LK :246-273). Closed on window/modal hide (Browser.lua:1079, Export.lua:534) and on disable (LifecycleSetup.lua:187). |
| Search autocomplete list | BrowserFilterBar.lua:445 → LK/WidgetsAutocomplete.lua:161 | UIParent | **FULLSCREEN_DIALOG** (library default `AC.STRATA`, :66; host passes none) | default | **not clamped** | — |
| debug console (+ its copy window) | LK/DebugLog.lua:536 | UIParent | **DIALOG** (library) | default | clamped | Above the main window by standard (debug-logging). |
| perf panel | LK/PerfPanel.lua:186 | UIParent | **DIALOG** (library) | default | clamped | — |
| simulation panel | LK/SimPanel.lua:211 (host strings modules/SimPanel.lua) | UIParent | **DIALOG** (library) | default | clamped | — |
| StaticPopups ×10 (purge, prune, forget holder, reset all, 3× clear list, clear filters, ledger reset ×2) | settings/Slash.lua:8-148 | Blizzard | **DIALOG** (Blizzard) | Blizzard | toplevel (Blizzard) | Raised from the settings panel (HIGH), the History window (HIGH) and the Export flow (DIALOG). |
| GameTooltip uses (rows, headers, charts, strips, ⓘ, filter buttons) | e.g. BrowserTable.lua:809, AnalyticsCharts.lua:23, Browser.lua:913, Panel.lua:636 | Blizzard | **TOOLTIP** | Blizzard | — | AnalyticsCharts anchors to UIParent at the cursor (ANCHOR_NONE). |
| Settings canvas (General page, landing, Profiles) | Panel.lua:1096 → LK Options | Blizzard SettingsPanel | inherited (HIGH) | library-managed (tab strip LK/OptionsTabs.lua:375, :712 +1) | — | Combat cover level from `lib.__coverLevel` (LK/Options.lua:589). |
| AH price-table host + 11 row frames + ⓘ buttons + reparented AceGUI checkboxes | Panel.lua:801, :834, :847, :861-865 | panel → placeholder | inherited | relative | — | The host is re-parented per render (:804). |
| reorder handles / row boxes / drop line / drag ghost | LK/WidgetsReorder.lua:599-601 (box **parent − 1**), :254 (line **+20**), :107 (ghost **TOOLTIP**) | row / container / UIParent | inherited / TOOLTIP | relative | — | The ghost shares TOOLTIP with the GameTooltip ("Drag to re-rank"). |
| IdList suggestion list (Filters tab) | LK/OptionsIds.lua:997 | UIParent | **FULLSCREEN_DIALOG** (library) | default | clamped | — |
| minimap button | LibDBIcon via LK/Launcher.lua | Minimap | LibDBIcon's (MEDIUM) | LibDBIcon | — | The addon picks nothing. |
| keybinding toggle button `LootHistoryToggleWindow` | core/LauncherSetup.lua:85 | UIParent | default | default | — | Never shown; it is a click target for the binding. |
| Attribution event frame | modules/Attribution.lua:461 | none | — | — | — | Invisible. |

## Problems

| id | file:line | problem |
|---|---|---|
| LOO-S01 | BrowserTable.lua:1194-1213; Browser.lua:1076-1080; LifecycleSetup.lua:187 | **The row menu can outlive its window.** Every close path (window OnHide, the Escape route through UISpecialFrames, the disable ladder) calls `NS.CloseMenu()`, which closes only the *library* dropdown. The host row menu, at FULLSCREEN_DIALOG, and its full-screen catcher, at FULLSCREEN, stay up over the game after the History window is gone. The next click anywhere is then eaten by the catcher. |
| LOO-S02 | BrowserTable.lua:1205-1210 | **Two dismissal models in one addon.** The row menu uses a full-screen FULLSCREEN catcher, the mechanism LibKa0s retired because it swallows the click that dismisses (LK/Widgets.lua:234-249). The addon's dropdowns use `GLOBAL_MOUSE_DOWN`. Right-click a row, then left-click a filter dropdown, and the dropdown does not open: the catcher eats the press. |
| LOO-S03 | BrowserTable.lua:1207 vs LK/Widgets.lua:653 | **Strata tie.** The catcher (FULLSCREEN) shares a strata with the Export copy window (FULLSCREEN). The copy window is centred and the History rows stay reachable around it, so a row menu can be opened while it is up; a click on the copy window then lands on whichever of the two has the higher level, which depends on creation order rather than intent. Either the copy window eats the click (and the row menu stays open) or the catcher does (and the copy window ignores the click). Low severity, but a transient helper should not share a tier with a real window. |
| LOO-S04 | Browser.lua:936 | **The History window shares HIGH with Blizzard's SettingsPanel and is not toplevel.** Ticking **Test mode** (and the "Ticking it opens the window" path) or pressing the keybind with Settings open puts two HIGH frames on screen. SettingsPanel raises itself on click (toplevel); the History window cannot, so once under, it stays under until Settings closes. |
| LOO-S05 | Export.lua:468 | **The Export modal shares DIALOG with three library windows** (debug console, perf panel, sim panel) **and Blizzard's StaticPopups**, and none of the addon's DIALOG frames is toplevel. With the debug console open, opening Export leaves stacking to creation order, and clicking the one underneath does not raise it. |
| LOO-S06 | Export.lua:465-466 | **Stale rationale.** The comment says DIALOG was chosen to sit "below the dropdown menu's FULLSCREEN catcher so an outside click closes the Data Set menu". The library menu has had no catcher since Widgets minor 5 (LK/Widgets.lua:232-249). DIALOG is still the right tier, for a different reason: above the HIGH window, below the FULLSCREEN copy window. |
| LOO-S07 | Browser.lua:936, Export.lua:468, BrowserTable.lua:1198, :1207 | **Strata chosen ad hoc as literals at four sites.** There is no named tier table, and BankLedger repeats the same literals at five sites (BankLedger Browser.lua:1029, SessionWindow.lua:536, Export.lua:376, LedgerTable.lua:824/833), so a tier change is nine edits across two repos. |
| LOO-S08 | core/CoreSetup.lua:96 vs LK/Core.lua:610-611 | **Degraded-path level drift.** The fallback grip takes the default +1 level, while the library grip takes +10 to clear the window's other children. On a library-less install the grip can draw under a later-created footer child in the bottom-right corner. |
| LOO-S09 | BrowserTable.lua:1197 | **The row menu is not clamped** (`SetClampedToScreen` absent). A right-click on a row near the bottom edge of a window dragged low opens a menu partly off-screen; the Holdings tab shares the menu (HoldingsTab.lua:346). The library's own dropdown menu (LK/Widgets.lua:224) and autocomplete list (LK/WidgetsAutocomplete.lua:161) are not clamped either; only the IdList suggestion list (LK/OptionsIds.lua:998) and the windows are. So clamping is not yet a collection convention, and T4 "clamped" below needs a library change too. |
| LOO-S10 | LK/WidgetsReorder.lua:107 | The drag ghost and the handle's GameTooltip ("Drag to re-rank") share TOOLTIP, so either can draw over the other mid-drag. This is library-owned and cosmetic. Noted for the upstream guidance only. |
| LOO-S11 | BrowserTable.lua:1201 vs LK/Widgets.lua:228 | Not strata, but z-adjacent chrome: the two popup menus in the addon wear different edges (muted gold vs black). One visual tier should have one look. |

Checked and found fine: test/sim strip placement (no overlap, by reserve); grip above pane
content (library path); copy window above modal; every transient popup in FULLSCREEN_DIALOG;
StaticPopups above the HIGH window; settings-panel children all inherited; the ReorderList box
deliberately one level under its row (parent − 1) so the row draws over its own box.

## Proposed strata map

| tier | strata | level band | elements |
|---|---|---|---|
| T0 HUD | MEDIUM (LibDBIcon) | library | minimap button. The addon has no HUD of its own. |
| T1 Primary window | **HIGH**, `SetToplevel(true)` | window base; chrome children +1..+5 (inherited); strips/badges inherited; **resize grip +10** (both paths) | History window and everything in it |
| T2 Modals and tool windows | **DIALOG**, `SetToplevel(true)` | default | Export modal, debug console, perf panel, sim panel; Blizzard StaticPopups share this tier by Blizzard's choice |
| T3 Output windows | **FULLSCREEN** | default | Export copy window (output of a T2 modal), and nothing transient |
| T4 Transient popups | **FULLSCREEN_DIALOG**, clamped (row menu here; library menu and autocomplete upstream) | default | library dropdown menu, autocomplete list, IdList suggestions, **row context menu**. No click catchers in any tier. |
| T5 Pointer | **TOOLTIP** | Blizzard | GameTooltip, reorder drag ghost |

Rule of the map: a frame opened *from* another frame sits in the same tier as its opener or one
above it, never below. A transient popup always sits above every window tier. No tier holds a
full-screen input catcher.

## Proposed changes

| id | change (file:line, from → to) | reason | confidence |
|---|---|---|---|
| LOO-Z01 | Add `BrowserTable:HideMenu()` (hides `rowMenu`, which hides its catcher) and call it beside `NS.CloseMenu()` in the window OnHide (Browser.lua:1079) and the disable ladder (LifecycleSetup.lua:187). | The row menu is closed on every path its window closes (S01). | 85% |
| LOO-Z02 | BrowserTable.lua:1205-1212: delete the FULLSCREEN catcher and dismiss the row menu like the library menu does, registering `GLOBAL_MOUSE_DOWN` while shown (unregister in OnHide), with outside = `not m:IsMouseOver()`. Interaction check: a press on a menu item is not outside, so the item's OnClick (on release) still fires; a right-click on another row closes the menu on the press and the row's `RightButtonUp` (BrowserTable.lua:831) reopens it there, which is the intended move; a press on a filter dropdown closes the row menu and opens the dropdown in one click, which fixes S02. Without the catcher nothing else hides the menu, so Z01 becomes mandatory with it. Better: add a `W.ContextMenu` to LibKa0s-Widgets (BankLedger LedgerTable.lua:824-833 has the identical catcher) and have both addons consume it. | It removes the T3-tier transient and the swallowed click, and gives one dismissal model per addon (S02, S03). | 75% (local fix) / 65% (library widget) |
| LOO-Z03 | Browser.lua:936: add `frame:SetToplevel(true)` after `SetFrameStrata("HIGH")`. | A toplevel frame is raised when it is shown and when it is clicked, so the window comes up over a co-tier SettingsPanel when Test mode or the keybind opens it, and comes back on click (S04). Interaction check: Raise() shifts only levels inside HIGH and all children are relative (grip +10 stays +10); every popup it opens is at DIALOG or above, so nothing it opens can fall under it; the window is not a secure frame, so raising it is legal in combat. SettingsPanel itself raises on click (Blizzard), so the two simply alternate. | 70% |
| LOO-Z04 | Export.lua:468: add `frame:SetToplevel(true)`. | A click raises the modal within the shared DIALOG tier (S05). | 65% |
| LOO-Z05 | Export.lua:465-466: rewrite the comment to "DIALOG: above the HIGH History window that opens it, below the FULLSCREEN copy window it opens." | The current rationale names a frame that no longer exists (S06). | 95% |
| LOO-Z06 | Name the tiers once, as `NS.Constants.STRATA = { window = "HIGH", modal = "DIALOG", output = "FULLSCREEN", popup = "FULLSCREEN_DIALOG" }`, and use them at Browser.lua:936, Export.lua:468 and BrowserTable.lua:1198. Ideally the table is LibKa0s's (`Core.STRATA`), so the library windows read the same names. | One declaration per tier; consistent across the addon and the collection (S07). | 60% (local) / 70% (library-owned) |
| LOO-Z07 | core/CoreSetup.lua:96: after creating the fallback grip, `grip:SetFrameLevel(frame:GetFrameLevel() + 10)`. | The degraded grip matches the library's band (S08). The path only runs without LibKa0s, which the addon vendors, so the benefit is small. | 45% |
| LOO-Z08 | BrowserTable.lua:1198: add `rowMenu:SetClampedToScreen(true)`. | T4 popups are clamped (S09). | 80% |
| LOO-Z09 | BrowserTable.lua:1201: border color `(0.62, 0.5, 0.18, 1)` → `(0, 0, 0, 1)` (library menu edge), or the reverse in the library. Owner's call; falls away if Z02 takes the library widget. | One look per tier (S11). | 45% |

## Notes for the upstream guidance

- **A five-tier ladder fits a windowed Ka0s addon exactly**: HIGH primary window → DIALOG
  modals/tool windows → FULLSCREEN output windows → FULLSCREEN_DIALOG transient popups →
  TOOLTIP pointer. LootHistory already follows it in all but the row-menu catcher, and BankLedger
  uses the same four literals, so this is codifying practice, not inventing it.
- **No full-screen click catchers.** LibKa0s already learned this (Widgets minor 5,
  `GLOBAL_MOUSE_DOWN`). The standard should forbid catchers and name the replacement, because both
  table addons still carry one.
- **Every popup a window opens must close on every path that window closes** (OnHide covers
  Escape/UISpecialFrames; the disable ladder covers slash-commands-§7). LootHistory gets this
  right for the library menu and wrong for its own, so it is a check worth an anti-pattern number.
- **Windows sharing a tier should be `SetToplevel(true)`**, so a click raises them. No Ka0s or
  LibKa0s window does this today; the collection relies on creation order.
- **The primary window shares HIGH with Blizzard's SettingsPanel.** Because `Test mode` and a
  keybind can open the window while Settings is up, the guidance should say what is intended:
  co-tier plus toplevel (recommended), or MEDIUM for the primary window, which then always sits
  under Settings.
- **Relative levels only**, as LibKa0s does (grip +10, drop line +20, box −1). LootHistory sets
  no absolute level anywhere, and the guidance should keep it that way and name the library bands
  so a host never picks its own.
- **Strata names belong in one table** (preferably `LibKa0s-Core`'s), read by host and library
  windows alike, so a tier change is one edit for the collection.
- **Clamp every transient popup**, the library's dropdown menu and autocomplete list included. Today
  only the IdList suggestion list is clamped, so a host that clamps its own menu (Z08) is ahead of
  the library it borrows from.
- **Degraded fallbacks must match the library's level choices** (the grip), or a library-less
  install stacks differently from a normal one.

## Review

Independent review, 2026-10-24, against `../LootHistory` on `master` at 82e1921 (read-only).

- **Inventory verified** by grepping every `CreateFrame`, `SetFrameStrata`, `SetFrameLevel`,
  `SetToplevel`, `Raise` and `SetClampedToScreen` outside `libs/` and `tests/` (every CreateFrame
  site, across 13 files), and the library sites the addon calls into (Core.lua:546/:611,
  Widgets.lua:225/:653, WidgetsAutocomplete.lua:66/:161, OptionsIds.lua:997, DebugLog.lua:536,
  PerfPanel.lua:186, SimPanel.lua:211, WidgetsReorder.lua:107/:255/:601). The four strata literals
  and the "no SetFrameLevel / SetToplevel / Raise" claim hold. Added two missing rows (the History
  pane host Browser.lua:863, the Holdings header cells HoldingsTab.lua:437) and marked the library
  dropdown menu and autocomplete list **not clamped**.
- **Problems confirmed** in code: S01 (window OnHide Browser.lua:1076-1080 and the disable ladder
  LifecycleSetup.lua:187 call only `NS.CloseMenu`; nothing hides `rowMenu`), S02 (the catcher eats
  the press; the library comment LK/Widgets.lua:232-249 records the same defect), S06 (the stale
  Export.lua:465-466 comment). Corrected S07 (BankLedger has five literal sites, including
  SessionWindow.lua:536, so nine edits, not eight), S09 (the library menu is *not* a clamped peer,
  so the clamp convention needs upstream work) and sharpened S03 (both failure shapes spelled out,
  low severity).
- **Interaction checks** added to Z02 (menu item clicks, re-open on another row, one-click dropdown
  after dismissal, Z01 becomes mandatory) and Z03 (toplevel raises on show as well as on click,
  relative levels survive, no protected frame involved). Nothing proposed moves a frame below a
  popup it opens, and the settings panel, StaticPopups and GameTooltip keep their Blizzard tiers.
- **Confidence**: Z07 50% → 45% (library-less path only). The rest stand; nothing fell under 40%.
- **Upstream note** added: clamp every transient popup, the library's included.
