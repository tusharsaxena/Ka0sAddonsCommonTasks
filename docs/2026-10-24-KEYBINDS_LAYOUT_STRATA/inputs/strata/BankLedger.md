# BankLedger — frame strata analysis

Read from `../BankLedger` on `master`, 2026-10-24: every `CreateFrame`, `SetFrameStrata`, `SetFrameLevel`,
`SetToplevel`, `SetClampedToScreen` and `GameTooltip:SetOwner` in `core/`, `modules/`, `settings/`, plus the
vendored LibKa0s modules that build frames on the addon's behalf (`Widgets.lua`, `WidgetsAutocomplete.lua`,
`Core.lua`, `DebugLog.lua`, `SimPanel.lua`, `Options.lua`, `OptionsCombat.lua`, `OptionsIds.lua`,
`OptionsTabs.lua`). BankLedger draws no HUD, bars, icons, glows or drag handles; it is two windows, one dialog
and their popups. The host never calls `SetFrameLevel` and never calls `SetToplevel`; nothing in the vendored
library calls `SetToplevel` either. BankLedger holds no perf harness, so `PerfPanel.lua` (DIALOG) never builds
here.

Blizzard references (from memory, verify with `/fstack` in game): StaticPopup frames are `DIALOG` and
toplevel; `GameTooltip` is `TOOLTIP`; the Settings panel is `HIGH` and toplevel; the bank/warband/guild bank
frames sit at `MEDIUM`/`HIGH`; LibDBIcon's minimap buttons are `MEDIUM`.

## Inventory

| element | file:line | parent | strata | frame level | toplevel / clamped | notes |
|---|---|---|---|---|---|---|
| Ledger window `BankLedgerWindow` | modules/Browser.lua:1022, strata :1029 | UIParent | **HIGH (explicit)** | inherited (UIParent+1) | not toplevel / clamped :1032 | movable, resizable, UISpecialFrames :1159; master scale/alpha/lock via Util.ApplyMasterFrame; OnHide closes the library menu only (:1142-1143) |
| ├ title bar | Browser.lua:1034 | ledger window | inherited HIGH | relative (+1) | — | drag handle for the window; title, TEST MODE badge FontStrings |
| ├ close button | Browser.lua:104 (MakeCloseButton) | title bar | inherited | relative | — | OVERLAY texture art :113 |
| ├ tab strip + 2 tab buttons (History, Insights) | Browser.lua:260, :269 (TABS :203) | ledger window | inherited | relative | — | ARTWORK underline :276 |
| ├ panes (History, Insights) | Browser.lua:1081 | ledger window | inherited | relative (+1) | — | one per tab, shown one at a time |
| ├ filter bar host | Browser.lua:1089 | ledger window | inherited | relative (+1) | — | holds dropdown buttons, search box, bar buttons |
| │ ├ bar buttons | Browser.lua:354 | filter bar | inherited | relative | — | BackdropTemplate |
| │ ├ dropdown buttons (×8) | Browser.lua:857-975 → LibKa0s Widgets.lua:339 | filter bar | inherited | relative | — | |
| │ └ search box | Browser.lua:322 → Widgets.lua:510 | filter bar | inherited | relative | — | EditBox |
| ├ test strip / sim strip | Browser.lua:821-823 → Widgets.lua:820 | ledger window | inherited | relative (+1) | — | anchored under the filter bar; panes re-anchored below it (no overlap) |
| ├ ledger table header, sort buttons | LedgerTable.lua:632, :668 | pane | inherited | relative | — | |
| ├ FauxScrollFrame + row host | LedgerTable.lua:640, :650 | pane | inherited | relative | — | |
| ├ pooled rows | LedgerTable.lua:486 | row host | inherited | relative (+3/+4 from window) | — | BACKGROUND stripe :491, HIGHLIGHT hover :495 (alpha from settings); right-click opens the row menu (:567) |
| ├ Insights scroll, content, 3 chart frames | Insights.lua:122, :127, :150-152 | pane | inherited | relative | — | |
| ├ Insights cards, bars, segments, swatches, legend | InsightsWidgets.lua:398, 457, 507, 515-516, 577, 594, 648, 666-667, 722, 760, 786, 807, 834 | content | inherited | relative | — | textures BACKGROUND/ARTWORK/OVERLAY only |
| ├ inner border | Core.lua:141 (library) / CoreSetup.lua:111 (fallback) | window | inherited | relative (+1) | — | 1px backdrop edge |
| └ resize grip | Core.lua:606, level :611 (library) / CoreSetup.lua:144 (fallback) | window | inherited | **library: parent+10 (`GRIP_LEVEL`, Core.lua:546); fallback: inherited (+1)** | — | bottom-right corner |
| Session window `BankLedgerSessionWindow` | modules/SessionWindow.lua:534, strata :536 | UIParent | **HIGH (explicit)** | inherited | not toplevel / clamped :539 | auto-shown at a bank; UISpecialFrames :642; preview via `/bl session` |
| ├ title bar, pane, header cells | SessionWindow.lua:543, :575, :581, :446 | session window | inherited | relative | — | |
| ├ FauxScrollFrame + row host + rows | SessionWindow.lua:587, :597, :343 | pane | inherited | relative | — | stripe :348, highlight :352 |
| ├ sim strip | SessionWindow.lua:485 → Widgets.lua:820 | session window | inherited | relative (+1) | — | under the title bar; pane moved down by its reserve |
| └ resize grip, inner border | as ledger window | | | | | |
| Export dialog `BankLedgerExportWindow` | modules/Export.lua:371, strata :376 | UIParent | **DIALOG (explicit)** | inherited | not toplevel / clamped :377 | movable; UISpecialFrames :446; comment :374-375 cites a FULLSCREEN "catcher" |
| ├ title bar, bar buttons | Export.lua:383, :335 | export dialog | inherited | relative | — | |
| └ data-set dropdown | Export.lua:403 → Widgets.lua:339 | export dialog | inherited | relative | — | |
| CSV copy window `BankLedgerExportCopyWindow` | Export.lua:282 → Widgets.lua:648, strata :653 | UIParent | **FULLSCREEN (library-chosen)** | inherited | clamped :656 | sits above the DIALOG export dialog by design (Widgets.lua:651-652) |
| Dropdown menu (shared, one per process) | Widgets.lua:224, strata :225 | UIParent | **FULLSCREEN_DIALOG (library)** | inherited | — | outside click via GLOBAL_MOUSE_DOWN, no catcher (Widgets.lua:232-275) |
| Search autocomplete list | Browser.lua:917 → WidgetsAutocomplete.lua:160, :161 | search box | **FULLSCREEN_DIALOG (library default `AC.STRATA`, :66; host passes none)** | inherited | — | |
| Ledger row context menu | modules/LedgerTable.lua:823, strata :824 | UIParent | **FULLSCREEN_DIALOG (explicit)** | inherited | — | host-built, not the library menu; **nothing hides it when the ledger window hides** |
| ├ row-menu buttons | LedgerTable.lua:894 | row menu | inherited | relative | — | HIGHLIGHT :900 |
| Row-menu click catcher | LedgerTable.lua:831, strata :833 | UIParent (SetAllPoints) | **FULLSCREEN (explicit)** | inherited | — | full-screen Button, LeftButtonUp+RightButtonUp; hides the menu and swallows the click; shown at :923, hidden only by the menu's OnHide (:837) |
| Debug console `BankLedgerDebugWindow` | core/DebugLogSetup.lua:174 → DebugLog.lua:533, strata :536 | UIParent | **DIALOG (library)** | inherited; diagnostics link toggle+1 (DebugLog.lua:337) | not toplevel / clamped :539 | `state.debugConsole` row |
| Simulation panel | core/SimSetup.lua:99 → SimPanel.lua:358, strata :211 | UIParent | **DIALOG (library)** | inherited | not toplevel / clamped :214 | `/bl sim` |
| Key-binding click button `BankLedgerToggleWindow` | core/LauncherSetup.lua:142 | UIParent | inherited (MEDIUM) | inherited | — | always hidden; never drawn |
| Minimap button | LibDBIcon via core/LauncherSetup.lua | Minimap | MEDIUM (LibDBIcon's) | LibDBIcon's | — | not chosen by the addon |
| Confirm popups PURGE / RESETALL / CLEAR_BLACKLIST / CLEAR_WHITELIST | settings/Slash.lua:8, :21, :37, :49 | Blizzard StaticPopup | DIALOG (Blizzard) | Blizzard | toplevel (Blizzard) | raised from the Settings panel (HIGH) and from `/bl` |
| Settings canvases (General, Profiles, landing) | Panel.lua:722, Profiles.lua:41 → library CreatePanel | SettingsPanel canvas | inherited (HIGH) | inherited | — | |
| ├ settings tab buttons (primary strip, Filters sub-strip) | OptionsTabs.lua:708-714 (library) | chrome / sub-strip host | inherited | parent+1 | — | so the selected tab overlaps the content edge |
| ├ IdList name-suggestion dropdown (Filters tab add box) | Panel.lua:389 → OptionsIds.lua:996-997 (library) | **UIParent** | **FULLSCREEN_DIALOG (library)** | inherited | clamped :998 | hidden by the edit box's OnHide (OptionsIds.lua:1224) and on pick (:929) |
| └ Combat lock cover | OptionsCombat.lua:209 `O.__buildCover` (library) | settings canvas | inherited | **raised when put up: max(panel+100, deepest descendant+1), capped** (Options.lua:589-590 → OptionsCombat.lua:179-183, `COVER_LEVEL_FLOOR` :156) | — | dims and blocks the canvas in combat |
| Tooltips | Browser.lua:373, :829; LedgerTable.lua:535, :542, :678; SessionWindow.lua:393, :397, :457, :491; InsightsWidgets.lua:377, :430, :736 | GameTooltip | TOOLTIP (Blizzard) | — | — | all owner-anchored; none addon-owned |

## Problems

| id | file:line | problem |
|---|---|---|
| BAN-S01 | Browser.lua:1029, SessionWindow.lua:536 | **The two windows share HIGH and neither is toplevel.** At a bank both are routinely open and overlapping; which one draws on top is decided by creation order and frame level, and clicking the one underneath does not raise it. The player cannot bring the session window forward over the ledger window (or vice versa) except by moving it. |
| BAN-S02 | Browser.lua:1029 | **The ledger window ties the Settings panel (both HIGH).** `/bl config` from an open ledger, or the ledger opened over Settings, overlaps by level alone; Settings is toplevel and the ledger window is not, so the order flips depending on which was clicked last (verify in game). |
| BAN-S03 | LedgerTable.lua:831-838 | **The row-menu catcher is a full-screen FULLSCREEN button that swallows the dismissing click**, the exact defect LibKa0s retired from its own dropdown menu (Widgets.lua:232-245: "That frame INTERCEPTED the click, and intercepting was the defect"). While it is up, every HIGH and DIALOG frame — both windows, the Settings panel, the export dialog, StaticPopups — is unclickable, and a right-click on another row only closes the menu. It also shares FULLSCREEN with the CSV copy window, so with the copy window open the two are ordered by level alone (verify which wins in game). |
| BAN-S04 | Export.lua:374-375 | **Stale strata rationale.** "DIALOG (below the dropdown menu's FULLSCREEN catcher) so an outside click closes the Data Set menu" — the library menu has had no catcher since Widgets minor 5; the strata is still right but the stated reason is false, which invites a wrong "fix" later. |
| BAN-S05 | Export.lua:376, DebugLog.lua:536, SimPanel.lua:211 | **Three DIALOG windows, none toplevel.** The export dialog, debug console and simulation panel all live at DIALOG; open together (common while testing an export under `/bl sim` with the console up) they stack by level only and a click does not raise one. Blizzard's StaticPopups share DIALOG; they are toplevel, so whether a confirm can open underneath the console or sim panel depends on whether the client raises a toplevel frame on Show (verify in game). |
| BAN-S06 | Browser.lua:1029 vs LedgerTable.lua:824 vs Widgets.lua:225 | **Strata are bare string literals at five host sites** (HIGH ×2, DIALOG, FULLSCREEN_DIALOG, FULLSCREEN) with no shared constant, so the addon's tiers are only discoverable by grep; three of the five sites carry no comment at all. |
| BAN-S07 | CoreSetup.lua:144 | **Degraded-path resize grip has no level raise**, unlike the library's `GRIP_LEVEL = 10` (Core.lua:546, :611). Without LibKa0s-Core the grip is at window+1, the same as the panes, and the pooled table rows (window+3/+4) under the bottom-right corner can take the mouse over it. Degraded installs only. |
| BAN-S08 | (withdrawn) | ~~Combat cover gets no level of its own.~~ Wrong: the library raises the cover every time it goes up over a shown page, to `max(panel+100, deepest descendant+1)` (Options.lua:589-590, OptionsCombat.lua:179-183). No defect. |
| BAN-S09 | SessionWindow.lua:536 | **The session window's tier is not stated anywhere.** It is a bank-companion panel that must sit above the bank UI (MEDIUM/HIGH) and under dialogs; HIGH achieves that today but nothing records that this is the reason, unlike the export dialog and copy window, which document theirs. |
| BAN-S10 | Browser.lua:1142-1148, :1184-1188 vs LedgerTable.lua:823-838 | **The row menu outlives its window.** The ledger window's OnHide and `B:Hide` close the library dropdown (`W.CloseMenu()`) and the autocomplete, but never the host row menu. Right-click a row, then Escape (UISpecialFrames), the key binding, `/bl hide` or a visibility change hides the window: the menu stays floating at FULLSCREEN_DIALOG over nothing, its catcher stays up across the whole screen, and the player's next click anywhere in the UI is swallowed. |
| BAN-S11 | OptionsIds.lua:996-997 (library) | **The IdList suggestion list is parented to UIParent at FULLSCREEN_DIALOG**, so it is above the Settings panel's combat cover rather than under it; if combat starts while it is open, it stays clickable over a locked page. Library-wide, not chosen by BL; flagged for the LibKa0s pass (verify in game — the cover may still hide the edit box and so the list). |

No collisions found inside a single window: every child inherits its window's strata, levels are relative,
the test/sim strips are anchored clear of the panes (Browser.lua:1076-1078, SessionWindow.lua:574), and textures
use draw layers (BACKGROUND stripe < ARTWORK < HIGHLIGHT/OVERLAY) consistently.

## Proposed strata map

| tier | strata | level band | elements |
|---|---|---|---|
| T0 world-attached (not ours) | MEDIUM | LibDBIcon's | minimap button; hidden binding button (never drawn) |
| T1 windows | **HIGH**, **toplevel** | base set by the client; children relative (+1…+6); resize grip base+10 | ledger window, session window. Above bags and bank frames, below every dialog. Last-clicked window on top. Shares the tier with Blizzard's Settings panel (also HIGH, toplevel). |
| T2 dialogs | **DIALOG**, **toplevel** | client base; children relative | export dialog, debug console (library), simulation panel (library), Blizzard StaticPopups |
| T3 detached child windows | **FULLSCREEN** | client base | CSV copy window (library) — opened from a T2 dialog, must sit above it |
| T4 transient popups | **FULLSCREEN_DIALOG** | client base | dropdown menu (library), autocomplete list (library), IdList suggestion list (library), ledger row context menu |
| T5 | TOOLTIP | Blizzard | GameTooltip |

Rules: a popup is always at least one tier above the frame that opened it; a popup closes when its opener
hides; no full-screen click catcher at any tier (outside clicks are listened for with `GLOBAL_MOUSE_DOWN`); no
absolute `SetFrameLevel`, only parent-relative offsets; every explicit `SetFrameStrata` reads a named constant.

## Proposed changes

| id | change (file:line, from → to) | reason | confidence |
|---|---|---|---|
| BAN-Z01 | Browser.lua:1029: add `frame:SetToplevel(true)` beside `SetFrameStrata("HIGH")` | Clicking the ledger window raises it over the session window and the Settings panel (S01, S02). Interaction check: every popup the window opens is T3/T4, so raising the window cannot bury its own menus; tooltips are TOOLTIP. | 75% |
| BAN-Z02 | SessionWindow.lua:536: add `frame:SetToplevel(true)`; comment states the T1 reason (above bank UI, below dialogs) | Same as Z01 for the companion window; records the tier's reason (S01, S09). | 75% |
| BAN-Z03 | LedgerTable.lua:823-838: delete the FULLSCREEN catcher; close the row menu on `GLOBAL_MOUSE_DOWN` when `not rowMenu:IsMouseOver()`, registered in OnShow and dropped in OnHide (the Widgets.lua:246-275 pattern). The library exports no general context-menu surface (only `Dropdown`/`CloseMenu`, Widgets.lua:448/:472), so this stays host code. Interaction check: `ShowRowMenu` runs from the row's click (mouse-up, :567), so registering on show cannot catch the opening press; the menu's own buttons are exempt through `IsMouseOver`. Behaviour note: the dismissing click now also reaches what is under it (a right-click on another row re-opens the menu there), as the library menu already does. | Removes a full-screen click-swallowing frame and its FULLSCREEN collision with the copy window (S03). | 70% |
| BAN-Z09 | Browser.lua:1142-1143 (OnHide hook) and :1185 (`B:Hide`): hide the row menu beside `W.CloseMenu()`, through a small `LT:HideRowMenu()` (LedgerTable.lua, next to `EnsureRowMenu`) that is a no-op before the menu exists. | A popup closes when its opener hides; today the stranded menu and its catcher eat the next click anywhere (S10). Independent of Z03 (without Z03 it also takes the catcher down via the menu's OnHide). | 85% |
| BAN-Z04 | Export.lua:374-375: rewrite the comment → "DIALOG: above the ledger window (HIGH) that opens it, below the CSV copy window (FULLSCREEN) and the dropdown menu (FULLSCREEN_DIALOG)." | The stated reason is false today (S04). Comment only. | 90% |
| BAN-Z05 | Export.lua:376: add `frame:SetToplevel(true)` | T2 dialogs raise on click (S05). The copy window it opens is T3, so raising the dialog cannot cover it. | 65% |
| BAN-Z06 | core/Constants.lua: add `C.STRATA = { WINDOW = "HIGH", DIALOG = "DIALOG", POPUP = "FULLSCREEN_DIALOG" }` and use it at Browser.lua:1029, SessionWindow.lua:536, Export.lua:376, LedgerTable.lua:824 (the fifth site, the catcher's FULLSCREEN, goes with Z03). If the upstream guidance adds a LibKa0s tier table, read that instead. | One declaration of the addon's tiers, greppable, commented once (S06). Covers host sites only; half the addon's strata stay library-chosen. | 55% |
| BAN-Z07 | CoreSetup.lua:144: after `CreateFrame`, `grip:SetFrameLevel(f:GetFrameLevel() + 10)` (guarded), matching the library's `GRIP_LEVEL` | Degraded grip stays above the rows like the library one (S07). Degraded installs only, so low player impact. | 50% |
| BAN-Z08 | (LibKa0s, not BL) DebugLog.lua:536 and SimPanel.lua:211: add `SetToplevel(true)`. ~~OptionsCombat cover level raise~~ struck — already done (S08 withdrawn). | Library-owned DIALOG windows join T2's raise-on-click rule (S05). Lands in LibKa0s and arrives by revendor. | 55% |
| BAN-Z10 | (LibKa0s, not BL) OptionsIds.lua: hide the suggestion list when the combat cover goes up over its page (or parent it under the canvas so the cover's raise covers it). | Keeps T4 popups from outliving a combat-locked page (S11). Verify in game first. | 40% |

Totals: 10 changes (8 in BankLedger, 2 upstream in LibKa0s). None changes a strata tier; they make the existing
tiers explicit, raise-on-click, close popups with their opener, and remove the one catcher.

## Notes for the upstream guidance

- **A tier table is the natural rule.** BankLedger already follows an implicit four-tier ladder (windows HIGH <
  dialogs DIALOG < detached child window FULLSCREEN < transient popups FULLSCREEN_DIALOG). The guidance should name
  the tiers and say which kind of element goes in each, so that "what strata?" is a lookup and not a choice.
- **"A popup sits at least one tier above its opener"** is the invariant the export → copy-window and
  window → dropdown pairs already satisfy, and the one the comment at Export.lua:374 tries to state.
- **"A popup closes when its opener hides."** A UIParent-parented popup does not inherit its opener's hide; the
  opener's OnHide must close it (the library's `CloseMenu` seam exists for exactly this, Browser.lua:1135-1143).
  BankLedger's row menu is a live miss (S10).
- **Same-tier windows MUST be toplevel.** Two movable windows at one strata without `SetToplevel(true)` are
  ordered by accident; this is the one real ordering defect in this addon (S01, S05).
- **No full-screen click catchers.** LibKa0s already retired its own (Widgets.lua:232-275); the guidance should
  forbid them collection-wide and point at the `GLOBAL_MOUSE_DOWN` listener pattern. BankLedger's row menu is a
  live instance (S03).
- **Levels are relative, never absolute,** and a frame that must sit above its siblings (a resize grip, a
  diagnostics link, a combat cover) raises by a named offset from its parent (`GRIP_LEVEL`,
  `COVER_LEVEL_FLOOR`). The degraded arm must follow the same offset as the library arm (S07).
- **Every explicit strata call carries its reason in a comment** naming the frames above and below it; a stale
  reason is a defect (S04).
- **Library-chosen strata count.** Over half of this addon's explicit strata are picked by LibKa0s (copy window,
  menus, autocomplete, IdList suggestions, debug console, sim panel). The guidance should cover the library's
  choices too, and LibKa0s could publish the tier table (`lib.STRATA`) so hosts read it rather than restate it.

## Review

Independent review, 2026-10-24, against the code on `master`.

- **Inventory corrected.** The ledger window has 2 tabs and 2 panes (History, Insights; Browser.lua:203), not 3 /
  "Ledger/Insights". Profiles canvas ref is Profiles.lua:41 (not :323). The combat cover row was wrong: the
  library raises it on cover-up (Options.lua:589-590 → OptionsCombat.lua:179-183, floor +100). Added three missing
  rows: the IdList name-suggestion dropdown on the Filters tab (OptionsIds.lua:996-997, FULLSCREEN_DIALOG on
  UIParent), the settings tab buttons' +1 level (OptionsTabs.lua:708-714), and the row-menu catcher's show/hide
  sites. Confirmed by grep that neither the host nor the vendored library calls `SetToplevel`, and that PerfPanel
  never builds in this addon.
- **Problems:** S08 withdrawn (false). New S10 (row menu and its full-screen catcher survive the ledger window
  hiding — the next click anywhere is eaten) and S11 (library IdList suggestions sit above the combat cover).
  S03 widened (the catcher blocks every HIGH/DIALOG frame, including Settings and StaticPopups) and its copy-window
  claim softened to "ordered by level, verify". S05's StaticPopup claim marked verify (StaticPopups are toplevel).
  S06 recounted to five literal sites.
- **Changes:** Z08's cover half struck. New Z09 (close the row menu with its window, 85%) and Z10 (library,
  40%). Z03 gained the interaction check and the note that the library exports no context-menu surface;
  70% (was 75%) because it changes what the dismissing click does. Z06 60→55, Z07 60→50. Interaction checks
  added for Z01 and Z05: every popup either window or dialog opens is at a higher tier, so raise-on-click
  cannot bury a dropdown, menu, copy window or tooltip.
- **Strata map:** T1 now names the Settings panel as a tier-mate; T4 lists the IdList suggestions; a
  "popup closes with its opener" rule added.
