# AuraMaster — frame strata analysis

Read from `../AuraMaster` on `master` (clean), 2026-10-24: every `CreateFrame`, `SetFrameStrata`,
`SetFrameLevel`, `SetClampedToScreen`, `CreateTexture`/`CreateFontString` layer and `SetDrawLayer` in `core/`,
`modules/` and `settings/`, plus the vendored LibKa0s frames the addon opens (`libs/LibKa0s/DebugLog.lua`,
`PerfPanel.lua`, `Widgets.lua`, `WidgetsDragHandle.lua`, `OptionsIds.lua`, `WidgetsAutocomplete.lua`).
History checked: `git log -S'strata = "MEDIUM"' -- defaults/Profile.lua` (3197c05 L-3 raised the default to
HIGH, 0f31609 X-3 put it back to MEDIUM). The standard has no strata or frame-level rule today
(`grep -i strata standards/standards/*.md` finds none).

`L` below is the container anchor's frame level (the user's `layout.level`, 1-100, default 5) and `S` its
strata (the user's `layout.strata`, default MEDIUM). Every per-container frame is a descendant of the
anchor, so it **inherits S** unless it sets its own.

## Inventory

| element | file:line | parent | strata | frame level | toplevel / clamped | notes |
|---|---|---|---|---|---|---|
| Container anchor `AuraMasterAnchor<id>` (DisableUntrustedLayoutScriptsTemplate) | modules/Container.lua:49 | UIParent | **explicit, user**: `SetFrameStrata(L.strata or D.layout.strata)` :608, on **every** `Apply`, which also re-strata's every child that is not fixed; choices BACKGROUND/LOW/MEDIUM/HIGH/DIALOG (core/Constants.lua:184) | **explicit, user**: `SetFrameLevel(L.level)` :609, default 5 (defaults/Profile.lua:195) | clamped :55; not toplevel; movable | Set in `Apply` only (out of combat) |
| Aura engine (`AuraContainer`, CustomAuraContainerTemplate) | Container.lua:449 | anchor | inherited S | inherited L+1; with text glow `Twins.LevelMain` writes max(L+1, GAP+1 = 4) through `CallEngine` (Container_Twins.lua:74-80), which the engine may refuse | — | Blizzard frame; buttons are its children |
| Engine aura buttons | (engine) | engine | inherited S | engine+1 | — | Dressed by Style_* (rows below) |
| Mouse blocker | Container.lua:251 | anchor | inherited S | **explicit relative**: engine − 1 (:257) | — | Mouse only, no visual |
| Glow twin holders ×4/8 (Text style, glow on; `C.TEXT_GLOW_TWINS`) | Container_Twins.lua:89 | anchor | inherited S | **explicit relative**: main − GAP − 1 (:111, re-set on every apply :148; GAP = 3, Constants.lua:290) | — | Can sit **below** L (L=5 → main 6 → holder 2) |
| Glow twin engines | Container_Twins.lua:113 | holder | inherited S | **explicit relative**: main − GAP (:115) | — | Copies of the text, under the main |
| Unlocked outline | Container.lua:796 | anchor | inherited S | **inherited, unset**: L+1 (ties with engine and placeholders) | — | 1px white edges, alpha OUTLINE_ALPHA |
| Name label host | Container.lua:823 | anchor | inherited S | **explicit relative**: L+1 (modules/Anchors.lua:815) | — | X/Y nudge ±200 can move it over the block |
| Drag handle (LibKa0s-Widgets DragHandle) | Anchors.lua:663 | anchor | inherited S | **explicit relative**: L+50 (`HANDLE_LEVEL`, :473, :681, :907); attached: max(own, parent L+51) (:708-715) | — | Only while unlocked; widget sets no strata |
| Handle help / close marks | libs/LibKa0s/WidgetsDragHandle.lua:394, :447 | handle | inherited S | inherited handle+1 | — | |
| Handle tooltip (GameTooltip) | modules/Anchors_Tooltip.lua (owner UIParent) | UIParent | Blizzard TOOLTIP | Blizzard | — | Never anchored into the anchor tree |
| Preview placeholders (Button pool) | modules/Preview.lua:121, factory(container.anchor) :189 | anchor | inherited S | inherited L+1 | — | Test mode; same dressing as live buttons |
| Preview extent | Preview.lua:221 | anchor | inherited S | inherited L+1 | — | Invisible; followers hang from it |
| Test marker ("TEST") | Preview.lua:273 | anchor | inherited S | **explicit relative**: L+40 (`MARKER_LEVEL`, :252, :282) | — | Comment: "below the strip (HANDLE_LEVEL 50)" |
| Bars: border frame | modules/Style_Bars.lua:37 (Style.NewBorder, modules/Style.lua:387) | button | inherited S | **unset**: button+1 | — | Solid strips (BORDER layer) laid **inside** the frame edge (Style.lua:400-408) |
| Bars: icon texture / bg texture | Style_Bars.lua:40, :43 | button | — | button | — | ARTWORK / BACKGROUND regions of the button |
| Bars: icon border frame | Style_Bars.lua:42 | button | inherited S | **unset**: button+1 | — | |
| Bars: StatusBar (invisible) + fill | Style_Bars.lua:46, :51 | button | inherited S | **unset**: button+1 | — | fill = ARTWORK, covers the whole bar area |
| Bars: spark clip + spark | Style_Bars.lua:54-55 | bar | inherited S | **explicit relative**: bar+1 (:69) | — | spark OVERLAY, ADD blend |
| Bars: text frame (name/time/stacks) | Style_Bars.lua:63, :71-73 | button | inherited S | **explicit relative**: bar+2 (:70) | — | OVERLAY font strings |
| Bars: pandemic wash | Style_Bars.lua:77 | text frame | — | bar+2 | — | BACKGROUND layer, ADD |
| Icons: icon texture | modules/Style_Icons.lua:28 | button | — | button | — | ARTWORK |
| Icons: cooldown swipe | Style_Icons.lua:31 | button | inherited S | unset: button+1 (the base the others count from) | — | CooldownFrameTemplate; also draws *Blizzard countdown numbers* (`SetHideCountdownNumbers`, :128), hidden with the swipe (:123) |
| Icons: border / dispel edge / text frame | Style_Icons.lua:44, :47, :52 | button | inherited S | **explicit relative**: cd+1, cd+2, cd+3 (:66-69) | — | Pinned, with the comment that equal-level siblings "stack in no promised order" (:63-65) |
| Icons: pandemic wash | Style_Icons.lua:57 | text frame | — | cd+3 | — | BACKGROUND, ADD: drawn over border and dispel edge |
| Text: clip → anim → area → chain | modules/Style_Text.lua:137, :140, :145, :168 | button | inherited S | unset: each parent+1 | — | Clip frames; glyphs OVERLAY |
| Text: icon texture / icon border frame | Style_Text.lua:143-144 | anim | inherited S | icon = anim region; iconBorder **unset** anim+1 (ties with `area`) | — | |
| Text: dispel backdrop / edge strips | Style_Text.lua:119-123 | area | — | area | — | BACKGROUND / BORDER layers |
| Text: glow letter copies | modules/Style_TextGlow.lua:135-136 | anim | — | anim | — | `SetDrawLayer("BACKGROUND", COPY_SUBLEVEL)`: under the icon |
| Backdrop host (non-Solid border styles) | Style.lua:464 | border frame | inherited S | **explicit**: the border's level when readable (:469) | — | |
| Snap highlight (dots, line, box) | modules/Anchors_Snap.lua:444 (dots :407, box :419) | UIParent | **explicit TOOLTIP** (`HIGHLIGHT_STRATA`, :382, :445) | inherited default | — | Only during a drag |
| Frame picker overlay `AuraMasterFramePicker` + outline + label | modules/FramePicker.lua:88, :112, :116 | UIParent | **explicit TOOLTIP** (:90, literal) | inherited | — | Settings window is closed while it runs |
| Debug console `AuraMasterDebugWindow` | libs/LibKa0s/DebugLog.lua:533-539 | UIParent | explicit DIALOG (library) | library | clamped | |
| Debug console copy window (`<name>DebugCopyWindow`, LibKa0s-Widgets `CopyWindow`) | libs/LibKa0s/DebugLog.lua:717-725 → Widgets.lua:653 | UIParent | explicit **FULLSCREEN** (library: "above the DIALOG-strata modal that opened it") | library | clamped | Missing from the first inventory |
| Perf step panel | libs/LibKa0s/PerfPanel.lua:186-189 (via core/PerfSetup.lua) | UIParent | explicit DIALOG (library) | library | clamped | |
| Settings: ID suggestions, autocomplete, LibKa0s menus | libs/LibKa0s/OptionsIds.lua:997, WidgetsAutocomplete.lua:66 (`AC.STRATA`) / :161, Widgets.lua:225 | UIParent / box | explicit FULLSCREEN_DIALOG (library) | library | clamped | Used by Spell categories / Overrides add boxes |
| Settings: AceGUI dropdown pullouts, LSM30 media pickers, color picker | libs/AceGUI-3.0, AceGUI-3.0-SharedMediaWidgets (via `NS.CreateDropdown`, OptionsSetup.lua:90, and every `values` row) / Blizzard `ColorPickerFrame` | UIParent | AceGUI / LSM: FULLSCREEN_DIALOG; color picker: Blizzard | library | — | Missing from the first inventory; every Layout → Strata and anchor-point pick opens one |
| Blizzard Settings panel (host of every page) | Blizzard_Settings | UIParent | Blizzard **HIGH**, toplevel (verify with `/fstack` in client) | Blizzard | — | Reference row: the tier any HUD frame that rises to HIGH competes with while the player edits |
| Combat cover on a settings page | libs/LibKa0s/Options.lua:589 | panel | inherited | explicit `__coverLevel` | — | Library |
| StaticPopups (5: reset all, delete container, attach flow, delete / forget categories) | General.lua:163, Containers.lua:132, Layout.lua:140, GeneralUserCategories.lua:247, :329 | Blizzard | Blizzard DIALOG | Blizzard | toplevel | |
| Minimap button / broker / options menu | core/LauncherSetup.lua (LibDBIcon, MenuUtil) | Minimap / Blizzard | library / Blizzard | — | — | Addon picks nothing |
| Hidden parent for Blizzard BuffFrame/DebuffFrame | modules/BlizzardFrames.lua:25 | UIParent | — | — | hidden | No visual |
| Font primer, time-text measurer, event drivers | FontPrimer.lua:98, Style.lua:224, ContainerManager.lua:812, EmptyWatch.lua:328, TimedSpells.lua:135, Anchors_Snap.lua:826 | UIParent / none | — | — | hidden or off-screen | No visual |

## Problems

| id | file:line | problem |
|---|---|---|
| AUR-S01 | core/Constants.lua:184, modules/Container.lua:608 | **A user can put a HUD container in DIALOG**, the tier the addon's own debug console, perf panel and its five StaticPopups use. A Dialog container can then sit over the attach-flow popup it triggered on drop, or over the console. Nothing says so on the Strata row (settings/Layout.lua:366: "Which layer of the interface the container draws in."). |
| AUR-S02 | Anchors.lua:681, :707-715, Preview.lua:282, Container.lua:796, :823 | **Edit-mode chrome is not separated from content.** The drag handle, its marks, the outline and the test marker all inherit the container's user strata. A BACKGROUND or LOW container's handle can sit under Blizzard's MEDIUM UI (action bars) and under any container in a higher strata, so it cannot be grabbed; across an attached chain in mixed strata the +50/+51 levels order nothing (the code comment at :706 admits it, docs/known-limitations.md:308 too). |
| AUR-S03 | modules/Style_Bars.lua:37-46, :68-70 | **Bars leave the border frames' level unpinned.** `am.border` and `am.iconBorder` are created at button+1, the same level as `am.bar` (whose ARTWORK fill covers the bar area). Their Solid strips are laid inside the frame edge, so the stacking of border vs. fill is "no promised order" — the exact case Style_Icons.lua:63-69 pins for icons. Bars pins only spark (+1) and text (+2). |
| AUR-S04 | modules/Container.lua:796-800 | **The unlocked outline has no level of its own**: L+1, tied with the engine and with the preview placeholders (also L+1), so whether it shows over a placeholder is undefined and it is always under live buttons (engine+1). |
| AUR-S05 | modules/Anchors.lua:815 | **The name label host sits at L+1**, tied with the engine and the placeholders. A label nudged over the block (X/Y ±200, Layout.lua:541-546) has undefined stacking against the auras. |
| AUR-S06 | Anchors.lua:473, :713, :815; Preview.lua:252; Container_Twins.lua:78, :111, :115; Constants.lua:290; Style_Bars.lua:69-70; Style_Icons.lua:67-69; Container.lua:257 | **Level offsets are magic numbers in seven files.** HANDLE 50, MARKER 40, chain +1, label +1, glow gap 3 and floor 4, blocker −1, per-style +1/+2/+3. The invariant "marker under handle" lives only in a comment (Preview.lua:252). There is no one table that says what sits above what. |
| AUR-S07 | Anchors_Snap.lua:382, FramePicker.lua:90 | **The two edit overlays pick TOOLTIP independently** (one named local, one literal). TOOLTIP is GameTooltip's own tier, so the snap highlight can cover a tooltip; LibKa0s puts its transient overlays (menus, suggestions) in FULLSCREEN_DIALOG, which is still above every user-selectable strata. **The two are not alike, though:** the picker draws a cursor-following label and an outline over whatever frame the cursor is on (FramePicker.lua:64-76), and that frame's own GameTooltip (TOOLTIP) shows while it is hovered; below TOOLTIP the picker's label and outline would sit under it. |
| AUR-S08 | modules/Style_Text.lua:144-146 | Text style: `iconBorder` and `area` are equal-level siblings under `anim`, unpinned. They do not overlap today (the icon sits beside the text area), so low risk, but it is the same pattern as S03. |
| AUR-S09 | modules/Style_Bars.lua:77, Style_Icons.lua:57 | The pandemic wash is a BACKGROUND texture of the **text** frame, so it draws over the bar's spark and over the icon's border and dispel edge (text frame cd+3 > dispel cd+2). It may be intended (the wash is additive and meant to read over the element), but it is not stated anywhere. |
| AUR-S10 | core/Database_Migrations.lua:180-183 vs defaults/Profile.lua:195 | Profiles upgraded from schema v1 had MEDIUM raised to **HIGH** by the v2 step, but the template went back to **MEDIUM** (X-3). On such a profile every new container draws one strata below the old ones, and its unlocked handle sits under theirs (S02). Stored data, not code: no change proposed, recorded so the owner knows why two containers stack "wrong". |
| AUR-S12 | Anchors.lua:681, :907; Container.lua:608 | **Any strata of its own given to a child of the anchor is undone on the next apply**: `anchor:SetFrameStrata` (Container.lua:608) runs in every `Apply` and carries every child that is not `SetFixedFrameStrata(true)` with it. Z06 as first written (a plain `handle:SetFrameStrata`) would hold only until the next config change. |
| AUR-S13 | Style_Bars.lua:46, :63, :68-70; Style_Icons.lua:64-69 | **The two styles count their element levels from different bases**: Bars from the StatusBar (spark +1, text +2), Icons from the Cooldown (border +1, dispel +2, text +3). The first draft's map claimed "Bars and Icons on one scheme" with offsets (+1 swipe/fill/spark, +2 border, +3 dispel, +4 text) that matched neither file. |
| AUR-S11 | Container_Twins.lua:111 | Glow holders sit **below the anchor's own level** (L=5 → main 6 → holder 2). Legal and harmless (they hold glow copies only), but it is the one place a per-container frame leaves the anchor's band, and only a comment says why. |

## Proposed strata map

One addon, one ladder. Strata picks the tier; within the HUD tier everything is a fixed offset from the
anchor's level `L`, published once.

| tier | strata | element class | level band |
|---|---|---|---|
| T0 | — | hidden helpers (BlizzardFrames hidden parent, font primer, measurer, event drivers) | n/a |
| T1 HUD content | **S** = user's `layout.strata` (BACKGROUND / LOW / MEDIUM / HIGH; DIALOG kept but flagged, Z07) | glow twin holders / engines | L+1−GAP−1 … L+1−GAP (below the main) |
| | | anchor, mouse blocker | L+0 (blocker = engine−1) |
| | | engine, live buttons, preview placeholders, preview extent | L+1 (buttons L+2) |
| | | per-element internals, counted from the style's base child (Bars: the StatusBar; Icons: the Cooldown) | base +0 (bar fill / swipe) · +1 spark (Bars) · +2 border and icon border · +3 dispel edge (Icons) · +4 text frame (and the pandemic wash on it). One `C.ELEMENT_LEVEL` table for both styles (Z02) |
| | | name label | L+20 |
| | | unlocked outline | L+30 |
| | | test marker | L+40 |
| T2 edit chrome | **max(S, MEDIUM)**, fixed (`SetFixedFrameStrata`) | drag handle + marks | L+50 (+1 per chain hop) in that strata |
| T3 edit overlays | snap highlight: FULLSCREEN_DIALOG; frame picker: **TOOLTIP** (two named constants) | snap highlight, frame picker | library default level |
| T4 addon windows | DIALOG (library / Blizzard); copy window FULLSCREEN | debug console, perf panel, StaticPopups; the console's copy window | library / Blizzard |
| T5 popovers | FULLSCREEN_DIALOG (library / AceGUI) | ID suggestions, autocomplete, LibKa0s menus, AceGUI and LSM pullouts | library |
| T6 tooltips | TOOLTIP (Blizzard) | GameTooltip, AuraButtonTooltip | Blizzard |

## Proposed changes

| id | change (file:line, from → to) | reason | confidence |
|---|---|---|---|
| AUR-Z01 | core/Constants.lua: add one band table, e.g. `C.LEVEL = { BLOCKER = -1, CONTENT = 1, LABEL = 20, OUTLINE = 30, MARKER = 40, HANDLE = 50 }` and `C.ELEMENT_LEVEL = { SPARK = 1, BORDER = 2, DISPEL = 3, TEXT = 4 }` (offsets from the style's base child, Z02); Anchors.lua:473 `HANDLE_LEVEL = 50` → `C.LEVEL.HANDLE`; Preview.lua:252 `MARKER_LEVEL = 40` → `C.LEVEL.MARKER`; Anchors.lua:815 `+ 1` → `+ C.LEVEL.LABEL`; Container.lua:257 `- 1` → `+ C.LEVEL.BLOCKER`. A suite case pins the order MARKER < HANDLE, LABEL < OUTLINE < MARKER. | One ladder in one place, testable, instead of seven files and a comment. | 85% |
| AUR-Z02 | modules/Style_Bars.lua:68-70: pin every sibling from `C.ELEMENT_LEVEL`: bar +0, sparkClip bar+1 (as now), **border bar+2, iconBorder bar+2** (new), text bar+4 (from +2). Style_Icons.lua:67-69 reads the same table: border cd+2 (from +1), dispelHost cd+3 (from +2), text cd+4 (from +3): the same order, new numbers. The non-Solid backdrop host takes the border's level (Style.lua:469) and follows it. | The bar's fill covers the whole button (am.bar is pinned TOPLEFT→BOTTOMRIGHT of the frame, Style_Bars.lua:108-113) and the Solid strips lie inside the frame edge, so border vs. fill is a real overlap at equal levels; same rule Icons already follows, and one table for both styles. In-client check: a 2px Solid border stays visible over a full bar with every texture, and Icons look unchanged. | 70% (Bars) · 55% (Icons renumber, churn only) |
| AUR-Z03 | modules/Container.lua:796-806 `ApplyOutline`: set `o:SetFrameLevel(levelOf(anchor) + C.LEVEL.OUTLINE)` on every show (from inherited L+1). | The outline is an unlock aid; it should read over the placeholders and live auras it outlines, deterministically. | 60% |
| AUR-Z04 | modules/Anchors.lua:815 label host: `levelOf(anchor) + 1` → `+ C.LEVEL.LABEL` (20). | A nudged label stacks above the block it may overlap, below the outline, marker and handle. | 55% |
| AUR-Z05 | Name both overlay strata in core/Constants.lua: `C.STRATA_SNAP_HIGHLIGHT = "FULLSCREEN_DIALOG"` (Anchors_Snap.lua:382, from TOOLTIP) and `C.STRATA_FRAME_PICKER = "TOOLTIP"` (FramePicker.lua:90, value unchanged). | The drop highlight only has to clear every user strata (DIALOG included), so it can leave TOOLTIP to tooltips, matching LibKa0s' popovers. The picker must stay at TOOLTIP: its cursor label and outline are drawn over the hovered frame, whose own GameTooltip would otherwise cover them (S07). In-client check: during a drag onto a container in Dialog, the dots and line still show. | 60% |
| AUR-Z06 | modules/Anchors.lua:681 and :907: give the handle a fixed strata of its own, `handle:SetFixedFrameStrata(false)`, `handle:SetFrameStrata(higherOf(S, "MEDIUM"))`, `handle:SetFixedFrameStrata(true)`, re-run on every `placeHandle` (S follows the user's pick), before setting its level. **Floor MEDIUM, not HIGH** (as first proposed): HIGH is the Blizzard Settings panel's tier, so a handle at L+50 there could draw over the panel while the player edits with containers unlocked. In-client checks: the strip follows a strata change; the help and close marks follow the strip; with containers unlocked and `/am config` open, no strip draws over the Settings panel; a BACKGROUND container's strip can be grabbed over the action bars. | Fixes the BACKGROUND and LOW strips buried under the MEDIUM UI. Chain ordering is fixed only among containers at MEDIUM or below. A plain `SetFrameStrata` would be undone by Container.lua:608 on the next apply (S12). | 45% |
| AUR-Z07 | settings/Layout.lua:366 Strata tooltip → "Which layer of the interface the container draws in. Dialog shares its layer with popups and the debug console, so it can cover them; High can draw over the settings window; Medium or lower is usual." (text only; the value list stays, removing DIALOG would be a stored-value change). | Says the collisions S01 describes without touching a setting, including the HIGH case that migrated v1 profiles already have (S10). Overlaps layout item 020 (the Layout → Scale & strata tab). | 70% |
| AUR-Z08 | modules/Style_Text.lua:144-146: `area` anim+1, `iconBorder` anim+2. | Determinism, same rule as Z02; the two do not overlap today. | 40% |
| AUR-Z10 | Container_Twins.lua:78, :111, :115, :148: no value change; express the glow floor and gap through the Z01 table, with the "holders below L" note beside it. | Same ladder, documented exception (S11). | 70% |

### Considered and rejected

| id | change | why not | confidence |
|---|---|---|---|
| AUR-Z09 | Style_Bars.lua:77 / Style_Icons.lua:57: comment and docs/ARCHITECTURE.md line that the pandemic wash is drawn over border and dispel edge on purpose (or move it to the button's ARTWORK). | An owner call with no evidence of a visible fault: the wash is additive and meant to read over the element. Raise it with the owner; do not plan it. | 35% |
| AUR-Z11 | For S10, `/am diag` lists containers whose strata differ from the others. | Stored data the player chose or inherited; a diag line is a feature, not strata hygiene. Z07's tooltip covers the explanation. | 30% |
| — | Drop DIALOG from `C.STRATA`. | A stored-value change (a migration for every container holding DIALOG); Z07 warns instead. | 20% |
| — | Frame picker overlay to FULLSCREEN_DIALOG (the first Z05). | Puts the picker's label and outline under the hovered frame's GameTooltip (S07). | 25% |

## Notes for the upstream guidance

- **Two axes, one rule each.** Strata separates *tiers* (HUD content, edit chrome, edit overlays, windows,
  popovers, tooltips); frame level orders *within* a frame's own tier. An addon publishes its ladder once (a
  `C.LEVEL` table) and every `SetFrameLevel` reads it.
- **Never leave overlapping siblings at the same level.** Children created on one parent get parent+1 and
  stack "in no promised order"; any two that overlap get explicit, distinct levels (Icons does it, Bars does
  not).
- **Edit-mode chrome is its own tier.** Handles, outlines and test markers shown while unlocked should not
  inherit a strata the player picked for the content; floor them so they are always reachable (Z06), but
  below HIGH, the Blizzard Settings panel's tier, so they never cover the panel the player is editing in. A
  child given its own strata must be `SetFixedFrameStrata(true)`, or the parent's next `SetFrameStrata` takes
  it back (S12).
- **A user-selectable strata list should stop at HIGH**, or warn: DIALOG is where the addon's own popups and
  windows live. New addons should not offer DIALOG; existing ones keep it (stored values) and say what it
  costs.
- **Transient full-screen overlays use named strata constants**, above every user-selectable strata.
  FULLSCREEN_DIALOG (what LibKa0s already uses for menus and suggestions) is right for a drop highlight. An
  overlay that labels the frame under the cursor (a frame picker) stays at TOOLTIP, because the hovered
  frame's own tooltip would otherwise cover it.
- **Levels under a restricted anchor are read guarded** (`NS.Secrets.NumberOr`), because a frame anchored
  into an aura engine can answer its level secret; AuraMaster's `levelOf` helpers (Anchors.lua:689,
  Container_Twins.lua:54) are the pattern. A LibKa0s helper (`LevelOf(frame, fallback)`) would save each addon
  its own copy.
- **Document every deliberate exception** (a frame below its parent's level, a wash drawn over a border) next
  to the ladder, so a later reader does not "fix" it.

## Review

Independent review, 2026-10-24, against `../AuraMaster` at `c77c7fc` (master, clean). I grepped every
`CreateFrame`, `SetFrameStrata`, `SetFrameLevel`, `SetToplevel` and `SetClampedToScreen` in `core/`,
`modules/` and `settings/` (`settings/` creates no frames), and read the library frames the addon opens.

**Inventory.** All 40 first-draft rows check out against the code. Corrections:
- Added three missing rows: the debug console's copy window (FULLSCREEN, Widgets.lua:653), the AceGUI / LSM
  dropdown pullouts and the color picker, and the Blizzard Settings panel (HIGH) as the reference tier for
  any HUD frame raised to HIGH.
- Noted that `anchor:SetFrameStrata` runs on every apply and re-stratas unfixed children.
- Noted that the engine's glow level is a `CallEngine` write the engine may refuse.
- Noted that the Icons swipe frame also draws the Blizzard countdown numbers.

**New problems.**
- S12: a strata of its own on an anchor child is undone by Container.lua:608 on the next apply, so the
  first Z06 would not have held.
- S13: Bars and Icons count element levels from different bases. The first map's "one scheme" row matched
  neither file.
- S07 now separates the frame picker, which labels a hovered frame whose own tooltip sits at TOOLTIP, from
  the snap highlight.

**Interaction checks that changed proposals.**
- Z05: the frame picker stays at TOOLTIP. Moving it to FULLSCREEN_DIALOG would put its label and outline
  under the hovered frame's GameTooltip. Only the snap highlight moves. The change is now two named
  constants, and confidence goes up from 55% to 60%.
- Z06: the floor drops from HIGH to MEDIUM so an unlocked strip never draws over the Settings panel (HIGH)
  while the player edits. The handle uses `SetFixedFrameStrata` and is re-applied on every `placeHandle`.
  Four in-client checks are listed. Confidence goes down from 50% to 45%.
- Z02: rewritten to one real `C.ELEMENT_LEVEL` ladder from each style's base child. Bars' border overlap is
  confirmed: the bar is pinned to the full button, Style_Bars.lua:108-113. The Icons renumbering keeps
  the same order and is scored separately as churn, at 55%.
- Z07: the tooltip also names the HIGH case, because migrated v1 profiles sit at HIGH (S10).

No proposed change alters a stored strata or level value, the user's strata list, or any combat-protected
path. Every write is to the addon's own frames, the same ones it already writes in `Apply` or placement.
Z09 (35%) and Z11 (30%) moved to a new "Considered and rejected" table, with two more rejected
alternatives: dropping DIALOG from the list, and the first Z05's picker move. The two upstream notes on
edit chrome and overlays are amended to match.
