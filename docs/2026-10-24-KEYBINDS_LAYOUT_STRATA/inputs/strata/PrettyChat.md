# PrettyChat — frame strata analysis

Item 030. Read-only analysis of `../PrettyChat` at `master` (`b08c579`, v1.7.0). Sources: every `CreateFrame` /
`SetFrameStrata` / `SetFrameLevel` / `SetToplevel` / `SetClampedToScreen` in `core/`, `modules/`, `settings/`
(the addon's own code), plus the vendored code that draws on its behalf: `libs/LibKa0s/DebugLog.lua`,
`Widgets.lua`, `Options.lua`, `OptionsCombat.lua`, `OptionsTabs.lua`, `OptionsWidgets.lua`, `Launcher.lua`,
`libs/LibDBIcon-1.0/LibDBIcon-1.0.lua`, `libs/AceGUI-3.0/AceGUI-3.0.lua`,
`libs/AceGUI-3.0/widgets/AceGUIWidget-DropDown*.lua`, `AceGUIContainer-TreeGroup.lua` and
`libs/AceConfig-3.0/AceConfigDialog-3.0/AceConfigDialog-3.0.lua`.

**Headline: PrettyChat's own code makes no strata or level decision.** A grep of `core/ modules/ settings/
defaults/ locales/` finds one `CreateFrame` (a non-visual event frame) and no `SetFrameStrata`,
`SetFrameLevel`, `SetToplevel` or `Raise` call. The addon's output is text in Blizzard's chat frames, and it
changes the strings, never the frames. Every visual element below is one of three kinds: an AceGUI widget
inside a Settings canvas, which inherits the canvas's strata; a library- or Blizzard-owned window; or a
third-party (Ace3, LibDBIcon) frame. Wherever the library picks the strata, the addon has no hook to change
it. The work for this addon is therefore to **record** its layering, plus library-level items that belong
upstream.

## Inventory

| element | file:line | parent | strata | frame level | toplevel / clamped | notes |
|---|---|---|---|---|---|---|
| `PrettyChatCombatWatcher` | modules/Override.lua:199 | none | n/a (never shown) | n/a | no / no | Event-only (combat edges for General visibility). No size, anchor or texture. Not a visual element. |
| Landing canvas `PrettyChatOptionsPanel` | libs/LibKa0s/Options.lua:657 (`mainPanelName`, settings/OptionsSetup.lua:265) | created parentless; Blizzard reparents into `SettingsPanel.Container` | **inherited** from SettingsPanel (Blizzard-owned; HIGH in retail `Blizzard_SettingsPanel.xml`, which cannot be checked from this repo) | inherited | SettingsPanel is toplevel / no | Logo texture plus labels via `BuildLandingPage` (Panel.lua:794). |
| Sub-page canvases ×3 (General, Categories, Profiles) | Options.lua:657 via `H.CreatePanel` (Panel.lua:737, 755; Profiles.lua:95) | as above | inherited | inherited | — | Anonymous frames. |
| Canvas `body` / `chrome` | Options.lua:694, 704 | canvas / body | inherited | inherited (child +1 by the client) | — | Header title, atlas divider, Defaults button (AceGUI, reparented). |
| Tab strip panel | libs/LibKa0s/OptionsTabs.lua:374-377 | `ctx.body` | inherited | **explicit, relative**: `= body:GetFrameLevel()` | — | General's 1-tab strip; Categories' 8-tab strip (Panel.lua:639). |
| Tab buttons | OptionsTabs.lua:708-714 | strip panel | inherited | **explicit, relative**: strip +1 | — | Tooltips via GameTooltip. |
| AceGUI ScrollFrame and content | AceGUIContainer-ScrollFrame.lua:167-193, via `H.EnsureScroll` (Panel.lua:152, 619) | created under UIParent, reparented into `ctx.body` | inherited after reparent | inherited | — | Holds every body widget. |
| General: Enable / Debug console / Minimap checkboxes, Test + Reset all buttons | composed (Schema.lua:123-196; OptionsCompose.lua:466-566) | scroll content | inherited | inherited | — | AceGUI pooled widgets. |
| General visibility **dropdown pullout** (+ its scroll, slider, items) | libs/AceGUI-3.0/widgets/AceGUIWidget-DropDown.lua:287-326, items DropDown-Items.lua:74-75, 162 | UIParent | **explicit FULLSCREEN_DIALOG** (AceGUI) | pullout = dropdown frame +1 (DropDown.lua:451) | scroll/items toplevel / clamped | Outside the canvas, so the combat cover cannot reach it. The library closes it on combat start (OptionsCombat.lua `__releaseOwnedFocus`). |
| Categories: TreeGroup (frame, tree pane, scrollbar, border, content pane) | settings/Panel.lua:482-499; AceGUIContainer-TreeGroup.lua:638-692 | scroll content | inherited | inherited | — | Per-string editor widgets inside: Panel.lua:247-324. |
| TreeGroup list buttons | AceGUIContainer-TreeGroup.lua:320, 477 | tree pane | inherited | **explicit, relative**: tree pane +1 | — | *(review: was missing)* One per visible string entry. |
| Category Enable checkbox, footnote label, per-string EditBoxes (+ AceGUI EditBox "OK" button) | Panel.lua:463, 655, 271-305; AceGUIWidget-EditBox.lua:217-243 | scroll content / TreeGroup content | inherited | inherited | — | |
| Widget tooltips (`H.AttachTooltip`, tab tips) | OptionsWidgets.lua:512-519; Panel.lua:258, 284, 295, 303, 321 | GameTooltip | Blizzard **TOOLTIP** | Blizzard | — | Shared GameTooltip, not owned by the addon. |
| **`AceGUITooltip`** | libs/AceGUI-3.0/AceGUI-3.0.lua:48; used by AceGUIContainer-TreeGroup.lua:204-209 | UIParent | **TOOLTIP** (GameTooltipTemplate) | template default | — | *(review: was missing)* A second tooltip frame. The TreeGroup list's hover tooltip uses this one, not GameTooltip. |
| **Combat cover** (one per page) | libs/LibKa0s/OptionsCombat.lua:210-231; raised at Options.lua:589-590 | the canvas | inherited | **explicit, computed**: `max(panel+100, deepest descendant+1)`, capped at 10000 (OptionsCombat.lua:150-175) | — | Dim plus "Settings are locked during combat." over the header, strip and body. |
| Profiles container + AceConfigDialog widgets | settings/Profiles.lua:72-80, 104-108 | `ctx.body` (SimpleGroup reparented, not in a scroll) | inherited | inherited | — | AceDBOptions dropdown pullouts follow the AceGUI row above (FULLSCREEN_DIALOG). |
| **AceConfigDialog confirmation** (Profiles: delete / copy / reset profile) | AceConfigDialog-3.0.lua:547-557 | UIParent | **explicit TOOLTIP** (AceConfigDialog) | **explicit 100** | no / — | *(review: corrected)* Not a StaticPopup at DIALOG, as the first draft said. Since minor 81 AceConfigDialog draws its own 320×72 frame at TOOLTIP/100 "with lots of room to draw under it", so it sits above every other element in this table, GameTooltip included. |
| StaticPopup `PRETTYCHAT_RESET_ALL` | settings/Panel.lua:43-55, shown :61 | Blizzard `StaticPopupN` | Blizzard **DIALOG** | Blizzard (raised on show) | toplevel (Blizzard) / — | Raised by the General Defaults, Reset all settings, and `/pc resetall` via ResetAll. |
| StaticPopup `PRETTYCHAT_RESET_CATEGORIES` | Panel.lua:67-79, shown :78 | Blizzard `StaticPopupN` | Blizzard **DIALOG** | Blizzard | toplevel (Blizzard) / — | Raised by the Categories header Defaults. |
| **Debug console** `PrettyChatDebugWindow` | libs/LibKa0s/DebugLog.lua:527-539 (descriptor core/DebugLogSetup.lua) | UIParent | **explicit DIALOG** (library) | default (client-assigned at creation; never raised) | **not toplevel** / clamped | 700×344 at CENTER(+220,−80). Opened by the Test button and `/pc test` **over the open Settings window**, by `/pc debug`, by the Debug console checkbox, and by `/pc diagnostics`. Movable. In `UISpecialFrames` (`escClose`, DebugLog.lua:364-365, called at :677), so Escape closes it. |
| Console drag bar, toggle button, log, slider | DebugLog.lua:513, 590, 611, 629 | console | inherited | inherited | — | |
| Console Diagnostics link | DebugLog.lua:330-337 | title bar | inherited | **explicit, relative**: toggle +1 | — | Overlaps the toggle's 80px button on purpose. |
| **Copy window** `PrettyChatDebugCopyWindow` | libs/LibKa0s/Widgets.lua:648-656 (via DebugLog `EnsureCopyWindow`, :717) | UIParent | **explicit FULLSCREEN** (library) | default | not toplevel / clamped | Sits above the DIALOG console that opens it, by design (comment at Widgets.lua:651). In `UISpecialFrames` (Widgets.lua:714-715). |
| **Minimap button** `LibDBIcon10_PrettyChat` | libs/LibDBIcon-1.0/LibDBIcon-1.0.lua:243-248 (registered from core/LauncherSetup.lua) | Minimap | **explicit MEDIUM, fixed** (LibDBIcon) | **explicit 8, fixed** | — | Third-party; the same for every LibDBIcon addon. |
| Launcher hover tooltip | Launcher.lua (LDB `OnTooltipShow`) | GameTooltip | TOOLTIP | Blizzard | — | |
| Launcher right-click menu | libs/LibKa0s/Launcher.lua:384-395 (`MenuUtil.CreateContextMenu`) | client Menu manager | client-owned | client-owned | — | |
| Hidden probe / registry frames | OptionsTabs.lua:114, OptionsNav.lua:88, OptionsScroll.lua:249, OptionsRegistry.lua:81, OptionsCombat.lua:62 | UIParent / none | n/a | n/a | — | Measurement and event frames, never shown. |

Not present in PrettyChat: no HUD or display frame, bars, icons, glows, drag handles, preview/sim strips or
sim panel, perf panel (the addon takes no `perf` hold; core/LifecycleSetup.lua:26-29), nav rail (stubbed only
for the degraded path, settings/OptionsSetup.lua:138), ID pickers, or `Bindings.xml`.

## Problems

| id | Where | Problem |
|---|---|---|
| PRC-S01 | addon-wide | **The layering is nowhere recorded.** The addon's correctness depends on library and third-party choices it does not state: console DIALOG above SettingsPanel, copy window FULLSCREEN above the console, pullouts FULLSCREEN_DIALOG above both, Blizzard confirmations in DIALOG, and AceConfigDialog's confirmation at TOOLTIP above everything. A library minor that moved the console to HIGH or MEDIUM would put the Test report **under** the Settings window that opened it, and nothing in PrettyChat would fail a test. Severity: low today, but no test guards it. |
| PRC-S02 | DebugLog.lua:536 vs Blizzard StaticPopup | *(review: corrected)* **The console and the addon's own destructive confirmations share DIALOG.** The first draft said a console opened *after* a popup could cover it. Today that is unlikely. The console is not toplevel and is never raised, so it keeps the low level it was created with (UIParent +1), while the StaticPopup is toplevel and is raised to the top of DIALOG on show. The popup therefore ends above the console whichever opened first (Blizzard's StaticPopup levels cannot be checked from this repo, so confirm it in-client). The real risk is **conditional**: any change that raises the console (PRC-Z01's `SetToplevel`, or a `Raise()` on click) would let a console shown or clicked after the popup land on top of it. The 700×344 console at CENTER(+220,−80) overlaps the StaticPopup's top-center slot at common resolutions. |
| PRC-S03 | DebugLog.lua:527-539 | **The console is not toplevel**, so it does not come forward when clicked. With two Ka0s consoles open (every addon's console is DIALOG, same library), or the console and a Blizzard DIALOG window, the one you click stays behind. This is a library-wide inconsistency, not PrettyChat's alone. Fixing it is what creates S02's risk, so the two must be solved together. |
| PRC-S04 | Widgets.lua:653 | The copy window is FULLSCREEN, **above** StaticPopups (DIALOG). A copy window left open can cover a reset confirmation raised later. This is lower risk than S02: the copy window is opened deliberately from the console and is usually closed straight away, and Escape closes it (UISpecialFrames). |
| PRC-S05 | OptionsCombat.lua:150-175 | The cover's level floor is a hard-coded `+100` over the canvas. It is correct, and it is computed against the deepest descendant, so there is no collision. But it is the one literal level in PrettyChat's settings tree. Recorded for the guidance (library-owned). |
| PRC-S06 | OptionsTabs.lua:375-377 | The tab strip panel is set to the **same** level as `body`, its parent, so strip and scroll content are siblings at the same level and are ordered by creation. They do not overlap today, because the scroll is inset below the chrome band (`__scrollTopInset`), so there is no visible defect. But the separation rests on geometry alone; nothing orders the two. Library-owned. |
| PRC-S07 | LibDBIcon-1.0.lua:246-248 | Minimap button fixed at MEDIUM / 8. This is third-party and correct, and the addon must not touch it. Listed only so the inventory is complete. No action. |
| PRC-S08 | AceGUI-3.0.lua:48 vs OptionsWidgets.lua:512-519 | *(review)* **Two tooltip frames.** Settings widgets use GameTooltip, while the TreeGroup list uses `AceGUITooltip`. Both are TOOLTIP strata, so neither hides under anything. But a host that adds its own `OnButtonEnter` tooltip on GameTooltip (layout PRC-L04) without turning off the TreeGroup's built-in one shows two tooltips at once. Third-party; recorded for the layout change and the guidance. |

## Proposed strata map

PrettyChat's intended layering. The addon sets none of it in its own code, and should keep it that way.

| tier | strata | level band | elements |
|---|---|---|---|
| 0 | — | — | Non-visual: `PrettyChatCombatWatcher`, probe and event frames. Never shown. |
| 1 | MEDIUM (fixed, LibDBIcon) | 8 (fixed) | Minimap button. |
| 2 | HIGH (inherited from Blizzard SettingsPanel) | canvas base L | Settings canvases → body → scroll → all AceGUI widgets, TreeGroup (buttons at tree pane +1), footnote, Profiles container. |
| 2 | HIGH (inherited) | L … L+1 | Chrome: header, Defaults button, tab strip (L), tab buttons (L+1). |
| 2 | HIGH (inherited) | ≥ L+100, above the deepest descendant | Combat cover (top of the page, below anything in a higher strata). |
| 3 | DIALOG | Blizzard toplevel, raised on show | StaticPopups: `PRETTYCHAT_RESET_ALL`, `PRETTYCHAT_RESET_CATEGORIES`. These must stay above the console (S02). |
| 3 | DIALOG | client-assigned, below the raised popups | Debug console (library window band). If it is made toplevel (Z01), it must yield to a visible popup (Z02). |
| 4 | FULLSCREEN | client-assigned | Copy window (opened from the console). |
| 5 | FULLSCREEN_DIALOG | AceGUI-managed | Dropdown pullouts (General visibility, Profiles). |
| 6 | TOOLTIP | Blizzard / template | GameTooltip (widget, tab and launcher tooltips), `AceGUITooltip` (TreeGroup list). Client menus are client-owned. |
| 6 | TOOLTIP | 100 (fixed, AceConfigDialog) | AceConfigDialog confirmation (Profiles page). |

Rule this addon follows and should keep: **the addon never calls `SetFrameStrata` / `SetFrameLevel` /
`SetToplevel` / `Raise` itself. Every window is the library's or a third party's, and every settings widget
inherits the canvas.**

## Proposed changes

| id | change (file:line, from → to) | reason | confidence |
|---|---|---|---|
| PRC-Z01 + Z02 | *(review: merged; they must ship together)* **Upstream, LibKa0s** `DebugLog.lua:536-539`: make the console come forward on click (`SetToplevel(true)` after `SetFrameStrata("DIALOG")`, no strata change), **and** in the same change keep confirmations on top: after the console shows or is raised, re-raise any visible StaticPopup (`StaticPopupN:IsShown()` → `:Raise()`). `Raise` on a non-secure Blizzard frame is a plain C method that writes no Lua state, so it raises no taint concern. The copy window gets the same click-to-front for symmetry. PrettyChat picks it up by re-vendoring, with no host edit. Interaction check: pullouts (FULLSCREEN_DIALOG), tooltips (TOOLTIP), the AceConfigDialog confirmation (TOOLTIP/100) and the Settings window (HIGH) are all unaffected; none of these frames is combat-protected. | Click-to-front among DIALOG peers, including other Ka0s consoles (S03), without creating the covered-confirmation risk that toplevel alone would introduce (S02). | 55% |
| PRC-Z03 | **Addon** `docs/ARCHITECTURE.md`: add a short *Layering* section that states the rule (the addon sets no strata; settings widgets inherit the canvas; windows are LibKa0s's and confirmations are Blizzard's/Ace3's) and **cites** the upstream strata guidance section once it exists, rather than copying the tier table's library-owned values. A copied table goes stale the first time the library changes. | Puts the intent in writing so that a library change that breaks it reads as a regression, not a refactor (S01). | 75% |
| PRC-Z04 | **Addon** `tests/`: add a static check that `core/`, `modules/`, `settings/` contain no `SetFrameStrata`, `SetFrameLevel`, `SetToplevel` or `:Raise(` call (comment lines excluded). The "console strata is above HIGH" assertion the first draft proposed here moves to **LibKa0s's** suite instead: it pins library behaviour, and a consumer must not duplicate a library pin (testing-§8, as options-ui-§13 cites it). | Pins S01 in the addon. The library pin catches a minor that drops the console below the Settings window the Test button opened it from. | 60% |
| PRC-Z05 | **No change** to the combat cover (`+100` floor), the tab strip's same-level panel, LibDBIcon's fixed MEDIUM/8, AceGUI's pullouts or AceConfigDialog's TOOLTIP/100 confirmation. Record S05, S06 and S08 for the upstream guidance only. | Library- or third-party-owned, no visible defect, and the addon has no hook to change them. | 90% |

## Notes for the upstream guidance

- **"A frameless addon owns no strata" is a valid, testable shape.** The guidance should name it: the
  addon's only visual surfaces are the Settings canvas (inherit), library windows (the library's call) and
  Blizzard/Ace3 popups and tooltips (their call). Its obligation is to make no strata call of its own,
  pinned by a static test (Z04).
- **The library window band needs one rule for every Ka0s addon.** Debug console DIALOG, copy window
  FULLSCREEN, perf panel DIALOG (PerfPanel.lua:186), sim panel DIALOG (SimPanel.lua:211), and menus/ID pickers
  FULLSCREEN_DIALOG (Widgets.lua:225, OptionsIds.lua:997). Codify it: a **library diagnostic window must sit
  above SettingsPanel (HIGH)**, because it is routinely opened *from* the settings (Test, Diagnostics).
- **Confirmations outrank diagnostics.** A destructive confirmation must never be covered by a window the same
  addon opened. Two of the three confirmation kinds already satisfy this by construction: AceConfigDialog's sits
  at TOOLTIP/100, and Blizzard's StaticPopups sit above a never-raised console. The rule therefore has to
  constrain the *window* side: any library window that is toplevel or raises itself must re-raise a visible
  StaticPopup (Z01 + Z02), or stay out of DIALOG. Pick one rule collection-wide.
- **Use relative levels, never literals, inside a page.** PrettyChat's settings tree uses only relative levels
  (`+1` strip buttons, `+1` tree buttons, `+1` diagnostics link, cover computed over the deepest descendant).
  The one literal, the cover's `+100` floor, is a library constant and should be documented as such. The
  guidance can cite OptionsCombat.lua:150-175 as the reference pattern: compute over the deepest descendant and
  cap at the client maximum.
- **Pullouts escape covers.** Anything parented to UIParent at FULLSCREEN_DIALOG (AceGUI dropdowns) escapes
  any canvas-level overlay. The guidance should say that an overlay meant to block input must also close the
  owned pullouts, as `__releaseOwnedFocus` does.
- **One tooltip frame per surface.** AceGUI's TreeGroup has its own `AceGUITooltip`. A host that adds its own
  hover tooltip to an AceGUI container should turn the built-in one off (S08).
- No current standard section (events-frames-taint.md, standalone-windows.md, options-ui.md) says anything
  about strata. A `grep -i strata` over `standards/standards/` finds nothing, so this will be a new section,
  not an amendment.

## Review

Independent review against `PrettyChat@b08c579` and its vendored libraries. What changed and why:

- **Inventory corrected.** The Profiles page's confirmation is not a DIALOG StaticPopup. Since minor 81 it is
  AceConfigDialog's own frame at **TOOLTIP / level 100** (AceConfigDialog-3.0.lua:547-557). The inventory row,
  the tier map and the upstream note are fixed.
- **Inventory completed.** Added the TreeGroup list buttons (explicit tree pane +1), `AceGUITooltip` (a second
  TOOLTIP frame, the one the TreeGroup uses), the AceGUI EditBox "OK" button, the pullout's relative level, the
  ScrollFrame's UIParent-then-reparent creation, and the console and copy window's `UISpecialFrames`
  membership (Escape-close). Fixed the line ranges for the console and the cover. Re-ran the addon-side grep,
  which found no strata, level, toplevel or `Raise` call, and listed the absent surfaces with citations.
- **S02 reasoning inverted.** A never-raised, non-toplevel console sits below a raised StaticPopup whichever
  opened first. So the risk the first draft described does not exist today, and Z01's `SetToplevel` is what
  would create it. Z01 and Z02 are merged into one change that must ship together (70%/50% → 55%), with the
  interaction check against pullouts, tooltips, AceConfigDialog, the Settings window and protected frames
  written out.
- **Z03 reworked (85% → 75%).** It now states the rule and cites the upstream guidance instead of copying
  library-owned strata values into the addon, where they would go stale.
- **Z04 reworked (55% → 60%).** The addon's static check now covers `SetToplevel` and `:Raise(`. The console-strata
  assertion moves to LibKa0s's suite, because a consumer must not duplicate a library pin.
- **Added** S08 (two tooltip frames, which matters for layout PRC-L04) and the sim-panel strata in the library
  band note. No change in this file asks PrettyChat to set a strata itself.
