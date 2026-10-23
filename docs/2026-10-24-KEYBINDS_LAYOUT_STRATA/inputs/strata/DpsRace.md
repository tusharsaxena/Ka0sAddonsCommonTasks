# DpsRace — frame strata analysis

Read from `../DpsRace` on `master` (clean), 2026-10-24: every `CreateFrame` / `SetFrameStrata` /
`SetFrameLevel` / `SetToplevel` in `core/`, `modules/`, `settings/`, and the vendored LibKa0s v1.76.0
surfaces the addon calls (`Core.lua` MakeResizable/MakeCloseButton, `Widgets.lua` Dropdown/TestStrip,
`DebugLog.lua` console, `PerfPanel.lua`). Levels are written relative to the owning window's level `L`
(a frame created with a parent gets `parent level + 1` unless set). No addon file calls `SetFrameLevel`.

## Inventory

| element | file:line | parent | strata | frame level | toplevel / clamped | notes |
|---|---|---|---|---|---|---|
| **Race HUD window** `DpsRaceHudFrame` | `modules/Hud.lua:435` | UIParent | **MEDIUM** explicit (`Hud.lua:438`) | inherited (UIParent+1) = `L` | **not toplevel** / clamped (`:439`) | Persistent display. Movable, resizable, in UISpecialFrames, Master scale. |
| HUD title / divider | `Hud.lua:386,389` | HUD | inherited | regions of `L` (OVERLAY / ARTWORK) | — | |
| HUD title-bar controls (close, lock, settings, results) | `Hud.lua:394-401`; close via `Core.lua:237`, others `Style.lua:132` | HUD | inherited | L+1 (implicit) | — | Tooltip via GameTooltip ANCHOR_TOP (`Style.lua:143`). |
| HUD drag strip | `Hud.lua:405` | HUD | inherited | L+1 (implicit) | — | Ends left of the 4 controls, so no overlap with them. |
| HUD content (clip) | `Hud.lua:444` | HUD | inherited | L+1 (implicit) | — | `SetClipsChildren(true)`. Pushed down by the test strip's height when it shows (`Hud.lua:523`). |
| HUD bodies (idle / armed / running / result) | `modules/Hud_States.lua:321` | content | inherited | L+2 | — | One shown at a time. |
| HUD panels, KPI boxes, target card, chips | `Hud_States.lua:101,210` | body | inherited | L+3 | — | Chips show GameTooltip (`Hud_States.lua:218`). |
| HUD flat buttons (presets, Custom, Arm, Share…) | `Hud_States.lua:128` | body | inherited | L+3 | — | |
| HUD custom-length edit box | `Hud_States.lua:381` | body | inherited | L+3 (same as the Custom button it covers) | — | `SetAllPoints(custom)` (`:418`), shown **instead of** the button (`:429-430`), so equal levels never stack. |
| HUD live rows host / breakdown rows / status bars | `Hud_States.lua:505,676`; `Hud_Breakdown.lua:55,60` | body | inherited | L+3 / L+4 / L+5 | — | Result rows host clips (`Hud_States.lua:679`). |
| HUD test-mode strip | `Hud.lua:507` → `libs/LibKa0s/Widgets.lua:817` | HUD | inherited | L+1 (implicit, created lazily after content) | — | Overlay *above the content*: the content's top moves down by the strip height, so the two never overlap. |
| HUD resize grip | `Hud.lua:452` → `Core.lua:606-611` | HUD | inherited | **L+10** (library `GRIP_LEVEL`) | — | Hidden while locked (`Hud.lua:466`). |
| **Results window** `DpsRaceResultsFrame` | `modules/Results.lua:205` | UIParent | **HIGH** explicit (`:208`) | inherited = `R` | **toplevel** (`:212`) / clamped (`:209`) | Browser. Movable (ignores Lock), resizable, UISpecialFrames, Master scale. |
| Results close / drag / tab buttons | `Results.lua:152,154,126` | Results | inherited | R+1 | — | Tabs sit under the title bar, drag over it, so they don't overlap. |
| Results body | `Results.lua:215` | Results | inherited | R+1 | — | |
| Results detail pane (Tbl.Panel) | `Results.lua:218` → `Results_Detail.lua:332` → `Results_Table.lua:66` | body | inherited | R+2 | — | A `BackdropTemplate` frame that **draws** (fill + 1px edge). Built in `ensureWindow`, **before** any tab pane. In wide mode it is anchored inside the Runs pane's rectangle, below the filter bar (`Results.lua:249-261`, `-barH`). |
| Runs pane / Bests pane | `Results_Runs.lua:282`; `Results_Bests.lua:100` | body | inherited | R+2 (same as the detail pane) | — | Built **lazily** on first tab show (`buildTab`, `Results.lua:107-121`), so always after the detail pane. `SetAllPoints(body)`, so each covers the whole body, detail area included. Draws nothing itself and isn't mouse-enabled. |
| Filter bars, dropdown buttons, filter checkboxes | `Results_Runs.lua:254,243,265`; `Results_Bests.lua:104,110,118` | pane | inherited | R+3 / R+4 | — | |
| Table header, header buttons, body, rows, scrollbar, tip spots | `Results_Table.lua:430,354,440,380,397,188` | list host | inherited | R+4 … R+6 | — | Tip spots show GameTooltip ANCHOR_RIGHT (`Results_Table.lua:175`). |
| Detail scroll frame / content | `Results_Detail.lua:334-335` | detail | inherited | R+3 / R+4 | — | |
| Detail KPI panels, flags panel, timing strip + segments, breakdown | `Results_Detail.lua:211,284,261-264,344` | detail content | inherited | R+5 … R+7 | — | Deepest nesting in the addon: R+7 (breakdown status bar). Grip is R+10. |
| Detail Back / Add Note / Share / Delete | `Results_Detail.lua:309-319` | detail | inherited | R+3 (same as the scroll frame) | — | Scroll frame is sized to stop short of them (`Results_Detail.lua:627-629`). |
| Detail note edit box | `Results_Detail.lua:291` | detail content | inherited | R+5 | — | Swapped with the note text, never both (`:609-610`). |
| Results resize grip | `Results.lua:229` → `Core.lua:611` | Results | inherited | **R+10** | — | |
| **Dropdown popup menu** (process-wide singleton) | `libs/LibKa0s/Widgets.lua:224-225` via `core/WidgetsSetup.lua:27` | UIParent | **FULLSCREEN_DIALOG** (library) | inherited | not toplevel | Opened from the Results filter bars. `NS.CloseMenu()` on Results hide / tab switch. |
| **Center-screen countdown** | `modules/Countdown.lua:166` | UIParent | **FULLSCREEN_DIALOG** explicit (`:167`) | inherited | not toplevel, not clamped | Mouse-disabled (`:168`). Digits OVERLAY, glow OVERLAY sublevel 2 (`:133,135`), fallback font OVERLAY (`:156`). |
| Buzzer raid warning "STOP" | `Hud.lua:159-161` | Blizzard `RaidWarningFrame` | Blizzard's | Blizzard's | — | Not the addon's frame. Listed because it is a visual the addon triggers. |
| Debug console `DpsRaceDebugWindow` | `libs/LibKa0s/DebugLog.lua:535-536` | UIParent | **DIALOG** (library) | inherited | not toplevel / clamped | Session row on Master controls. |
| Perf panel `DpsRacePerfPanel` | `libs/LibKa0s/PerfPanel.lua:184-186` | UIParent | **DIALOG** (library) | inherited | not toplevel / clamped | `/dr perf`. |
| StaticPopups: reset all, delete all runs, delete run, whisper share | `settings/General.lua:24`; `settings/History.lua:58`; `modules/Results.lua:430`; `modules/Share.lua:152` | Blizzard StaticPopup | DIALOG (Blizzard) | Blizzard's | — | All above both windows. |
| GameTooltip (HUD controls, chips, Results cells) | `Style.lua:143`; `Hud_States.lua:217`; `Results_Table.lua:174` | Blizzard | TOOLTIP | — | — | |
| Settings panel pages | `settings/OptionsSetup.lua:69`, `General.lua:144`, `Profiles.lua:23` | Blizzard SettingsPanel canvas | Blizzard's (HIGH per FrameXML, to confirm in client) | library-managed (combat cover `Options.lua:589`) | Blizzard's | The HUD's *Settings* control opens it over the MEDIUM HUD. It ties with the HIGH Results window, and click order decides which is in front (both toplevel). |
| Key-binding buttons `DpsRaceToggleHud`, `DpsRaceToggleResults`, `DpsRaceArmToggle` | `core/LauncherSetup.lua:24,29,34` | UIParent | default | default | — | Hidden, never drawn. No z-order. |
| Minimap button | LibDBIcon via `core/LauncherSetup.lua` | Minimap | LibDBIcon's (MEDIUM) | LibDBIcon's | — | Not chosen by the addon. |
| Event frame | `modules/Watchers.lua:109` | none | — | — | — | `CreateFrame("Frame")`, never shown, never drawn. Exempt, like the binding buttons. (Missing from the first draft.) |

## Problems

| id | where | problem |
|---|---|---|
| DPS-S01 | `modules/Hud.lua:435-440` vs `modules/Results.lua:212` | **The two windows disagree on toplevel.** Results is `SetToplevel(true)` and the HUD is not. Among MEDIUM-strata frames (other addons' HUDs, Blizzard MEDIUM panels), a click on the HUD doesn't raise it, so a HUD dragged partly under another MEDIUM frame stays under it. The addon has no rule that says which. |
| DPS-S02 | `modules/Countdown.lua:167` vs `libs/LibKa0s/Widgets.lua:225` | **Countdown shares FULLSCREEN_DIALOG with the dropdown menu.** Both have default levels, so their relative order is undefined. A Results filter menu opened during the last ten seconds can be drawn under the countdown numbers wherever they overlap. The countdown is mouse-disabled, so no click is lost, but the menu text can be covered. The strata was picked ad hoc ("its own frame, FULLSCREEN_DIALOG", `Countdown.lua:18`) and no reason is recorded. |
| DPS-S03 | `modules/Countdown.lua:18,167` | **The alert sits in the menu tier with no recorded reason.** The header says only "FULLSCREEN_DIALOG strata". The number draws over StaticPopups, the debug console and the perf panel (all DIALOG). That is fine and intended: it is mouse-disabled, shows only in the last ≤10 s, and should read like a pull timer. Note that FULLSCREEN is **also** above DIALOG, so moving it one tier down does not change this; the only thing the tier choice decides is its order against menus (S02). (Corrected: the first draft called the over-dialog draw a problem and then proposed a fix that keeps it.) |
| DPS-S04 | `modules/Results.lua:218` + `Results_Runs.lua:282-283` | **Equal-level overlap in the Results body.** In wide mode the detail pane (R+2) sits inside the Runs pane's rectangle (R+2, `SetAllPoints(body)`). The order is creation order (detail built first) and is undefined by API. It is harmless today only because the pane frame draws nothing and takes no mouse, and its children stop at `listWidth` (`Results_Runs.lua:331`). Any later backdrop or `EnableMouse` on the pane frame would sit over or under the detail at random. |
| DPS-S05 | `Results_Detail.lua:309-319` vs `:334` | Detail buttons and the scroll frame are both R+3 siblings, kept apart only by geometry (`Results_Detail.lua:627-629`). Fine, but undocumented. |
| DPS-S06 | `Hud.lua:507` | The test strip is L+1, the same level as the content and the drag strip. It is kept clear by moving the content down (`Hud.lua:523`), not by level. That is correct for a strip that *displaces* the content. It would be wrong if the strip were ever made to overlay instead. Worth stating as the rule. |
| DPS-S07 | `libs/LibKa0s/Core.lua:546,611` | **The resize grip's band is a fixed +10 over the window, and the Results window already nests to R+7** (detail breakdown status bar). Three more nesting levels anywhere in the Results body would put content above the grip. HUD max depth is L+5. Not a bug today, but there is no headroom check. |
| DPS-S08 | (whole addon) | **No written layering.** HUD MEDIUM, Results HIGH, countdown FULLSCREEN_DIALOG are each hard-coded at their call site with no shared constant and no comment that relates them. The choice matches the collection's de-facto pattern (display MEDIUM, browser HIGH, modal DIALOG, menu FULLSCREEN_DIALOG, seen in BankLedger, LootHistory, DropWatcher), but only by convention. |
| DPS-S09 | `Hud.lua:405` / `Hud.lua:394-401` | Title-bar controls and the drag strip are equal-level (L+1) siblings. They don't overlap now because the drag rect stops at `-(8 + 4 * CONTROL_PITCH)`. Adding a fifth control without widening that inset would put the drag strip over it in undefined order. |

## Proposed strata map

| tier | strata | level band | elements |
|---|---|---|---|
| 1. Persistent display | **MEDIUM**, toplevel | window `L`; chrome (title bar controls, drag strip, test strip, content host) L+1; body content L+2…L+6; resize grip L+10 | Race HUD |
| 2. Browser window | **HIGH**, toplevel | window `R`; chrome (close, drag, tabs, body) R+1; list panes R+2; **detail pane explicitly R+3** (Z03); content up to R+8; resize grip R+10 | Results window |
| 3. Modal / tool windows | **DIALOG** | library-owned | StaticPopups (Blizzard), debug console, perf panel (LibKa0s) |
| 4. Screen alert (non-interactive) | **FULLSCREEN**, mouse-disabled | default | Center-screen countdown |
| 5. Transient menus | **FULLSCREEN_DIALOG** | library-owned | LibKa0s dropdown popup |
| 6. Tooltips | **TOOLTIP** | Blizzard | GameTooltip |

Rule inside each window: a sibling that must be on top of an equal-parent sibling gets an **explicit**
`SetFrameLevel(parent level + n)`. Creation order is never relied on. Overlays that displace content (the test
strip) stay at the chrome level.

## Proposed changes

| id | change (file:line, from → to) | reason | confidence |
|---|---|---|---|
| DPS-Z01 | `modules/Hud.lua:438-440`: add `f:SetToplevel(true)` after `SetFrameStrata("MEDIUM")` | Both windows behave alike: a click raises within their strata (S01). Interaction check: a raise only re-levels the HUD within MEDIUM, so it never rises over the HIGH Results window, the Settings panel, StaticPopups or menus. Children keep their offsets, including the library grip's +10 (the Results window already works this way). The HUD has no secure children and nothing parented to it from Blizzard. | 70% |
| DPS-Z02 | `modules/Countdown.lua:167`: `"FULLSCREEN_DIALOG"` → `"FULLSCREEN"`, and update the `Countdown.lua:18` header comment to say why (above every DIALOG window as today, below every menu) | Takes the countdown out of the menus' strata, so a Results filter menu (or any Ka0s addon's dropdown: the LibKa0s popup is a process-wide singleton) is always drawn over it (S02). Its draw over dialogs is unchanged (S03). Interaction check: mouse-disabled, so no click target changes. Residual risk: a Blizzard frame that uses FULLSCREEN would now tie with the numbers instead of being under them. Confirm in client with a fullscreen panel open during the last 10 s. | 60% |
| DPS-Z03 | `modules/Results_Detail.lua:332` (`Detail.Build`): right after `Tbl.Panel(parent, …)`, add `frame:SetFrameLevel(parent:GetFrameLevel() + 2)` (R+3) before any child is created. The Runs/Bests panes built lazily at `Results.lua:110-121` keep their implicit body+1 (R+2) | Puts the drawing detail pane in its own band above the empty list pane instead of relying on creation order (S04). Setting it before the children are built means every child inherits the raised band with no re-levelling. The deepest detail child (today R+7) then sits at R+8, still under the grip at R+10 (S07). (Corrected from the first draft's `+ 3`, which gives R+4 and a deepest child of R+9, contradicting its own "R+3 band" and "R+8".) Interaction check: the Runs filter bar (R+3) and its dropdown buttons are above the detail's top edge (`-barH`, `Results.lua:258`), so they never overlap the raised pane. Narrow mode shows one of the two only (`Results.lua:264-265`). The popup menu is FULLSCREEN_DIALOG, unaffected. Defensive only: nothing is visibly wrong today. | 50% |
| DPS-Z04 | Add `NS.Constants.STRATA = { HUD = "MEDIUM", RESULTS = "HIGH", ALERT = "FULLSCREEN" }` (`core/Constants.lua`) and read it at `Hud.lua:438`, `Results.lua:208`, `Countdown.lua:167`, with one comment block stating the tier map above. `ALERT` assumes Z02. Otherwise it is `"FULLSCREEN_DIALOG"`. | One place that states the addon's layering (S08). Keeps future frames from picking a strata ad hoc. Better still if the upstream guidance names the tiers, so every addon uses the same keys. | 55% |
| DPS-Z05 | `modules/Hud.lua:405-407`: a comment stating that the drag strip's right inset must cover every title-bar control (`4` = close + lock + settings + results, `Hud.lua:394-401`). Comment only: the first draft's alternative (`#ui.controls.controls`) names a field nobody has verified, and the close button is placed outside that loop. | Guards S09's equal-level overlap against a future fifth control. | 45% |
| DPS-Z06 | `docs/ARCHITECTURE.md` (or `docs/module-map.md`): add a *Layering* paragraph that copies the strata map | The record that the upstream guidance will ask every addon to keep. | 75% |

No change proposed for S05, S06 or S07 (geometry-separated equal levels, and a library grip band with
headroom today). They are recorded for the upstream guidance.

## Notes for the upstream guidance

- **A tier table by element class works for this addon unchanged:** persistent display MEDIUM, opened-on-purpose
  browser HIGH, modal/tool windows DIALOG, non-interactive screen alerts FULLSCREEN, transient menus
  FULLSCREEN_DIALOG, tooltips TOOLTIP. DpsRace already fits it except the alert (one tier too high).
- **Toplevel should be a per-tier rule, not a per-window accident.** Every movable window in tiers 1–2 gets
  `SetToplevel(true)`.
- **Non-interactive alerts must not share a strata with interactive menus.** Same-strata, same-level ordering
  is undefined.
- **"Explicit level for intended overlap"**: when one sibling is laid inside another's rectangle (a detail
  pane in a list pane, an edit box over a button), either show only one at a time (as `Hud_States.lua:429-430`
  and `Results_Detail.lua:609-610` do) or set the top one's level explicitly. Never rely on creation order.
- **Displacing overlays vs covering overlays**: a test/sim strip that pushes the content down may share the
  chrome level. One that covers content must be level-raised above the content band.
- **Library bands need a stated headroom.** `Core.lua`'s grip at +10 assumes window content nests less than 10
  deep. The guidance should state the band (content ≤ +8, grip +10) so a host can check itself, or the
  library could raise the grip relative to the deepest child on first show.
- **Hidden binding buttons** (`CLICK <Name>:LeftButton` targets) are exempt from the strata rules and should be
  listed as such, so audits don't flag them.

## Review

Independent review, 2026-10-24. I re-grepped every `CreateFrame` / `SetFrameStrata` / `SetFrameLevel` /
`SetToplevel` under `core/`, `modules/` and `settings/` in `../DpsRace`, and read `Results.lua:200-265`,
`Results_Detail.lua:328-340`, `Results_Table.lua:60-72`, `Countdown.lua:15-20,160-172`, `Hud.lua:400-412`,
`libs/LibKa0s/Core.lua:600-615` and `libs/LibKa0s/Widgets.lua:220-228`.

- **Inventory:** added the missing `Watchers.lua:109` event frame (exempt). Recorded that the detail pane
  draws a backdrop (`Tbl.Panel`) and that the Runs/Bests panes are built lazily (`buildTab`), which is why the
  detail pane always comes first in creation order. The rest of the inventory checked out: the levels, the
  four title-bar controls against the `4 * CONTROL_PITCH` inset, no addon `SetFrameLevel`, Results toplevel,
  HUD not toplevel, menu FULLSCREEN_DIALOG and grip `+GRIP_LEVEL`.
- **S03 rewritten.** The strata order is DIALOG < FULLSCREEN < FULLSCREEN_DIALOG, so the first draft's fix
  (Z02) left the "outranks every dialog" complaint in place. That draw is intended. The real issue is the
  tie with menus, which is S02.
- **Z02:** the reason was narrowed to S02. A residual-risk note for Blizzard FULLSCREEN frames was added.
  Confidence 65% → 60%.
- **Z03:** fixed an arithmetic contradiction. `+ 3` gives R+4 (deepest R+9), not the "R+3 band / R+8" it
  claimed, so the change is now `+ 2`. Added the interaction check: the filter bar sits above the detail's
  top, and narrow mode shows one pane at a time. Confidence 55% → 50% (defensive only).
- **Z04:** made its dependency on Z02 explicit. 60% → 55%.
- **Z05:** limited to a comment. The proposed `#ui.controls.controls` was unverified, and the close button
  is outside that loop. 50% → 45%.
- **Z01:** added an interaction check. Confidence unchanged.
- **Interaction sweep (item 5):** no change moves a frame above the Settings panel, a StaticPopup, the
  dropdown menu or GameTooltip. No change touches the binding buttons, the minimap button or Blizzard's
  RaidWarningFrame. The addon has no combat-protected frames, so none of this needs combat deferral.
  Nothing fell under 40%, so there is no rejected section.
