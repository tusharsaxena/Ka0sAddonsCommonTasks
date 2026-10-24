# KickCD — frame strata analysis

Scope: item 030. I read `../KickCD` on `master` on 2026-10-24: every `CreateFrame`, `SetFrameStrata`,
`SetFrameLevel`, `SetClampedToScreen` and region-layer call in `core/`, `modules/` and `settings/`, plus the vendored
`libs/LibKa0s/` constructors KickCD reaches (DragHandle, TestStrip, DebugLog, PerfPanel, SimPanel, the Copy window,
the autocomplete and suggest lists, ReorderList, Glow) and `libs/LibCustomGlow-1.0` (glow frame levels) and
`libs/LibDBIcon-1.0`.

Notation: **G** is an icon grid's frame level and **C** is a cast bar's. Both are `UIParent` children with no
explicit level, so the client assigns `UIParent:GetFrameLevel()+1` to both. G and C are therefore **equal** by
default. Levels written as `X+n` are relative to the named frame.

## Inventory

| element | file:line | parent | strata | frame level | toplevel / clamped | notes |
|---|---|---|---|---|---|---|
| Icon grid (`KickCDIconGrid`, `KickCDIconGridFocus`), one per unit | modules/IconGrid.lua:568-572 | UIParent | **MEDIUM, explicit** | inherited (G) | no / clamped | movable; drag host |
| Icon button (pooled, one per tracked spell) | modules/IconGrid_Render.lua:203 | grid | inherited MEDIUM | inherited G+1 | no / no | `EnableMouse(false)` unless locked with the tooltip on |
| - spell texture | IconGrid_Render.lua:210 | button | — | button, `ARTWORK` | — | |
| - icon border (BackdropTemplate) | IconGrid_Render.lua:219-221 | button | inherited | **explicit** button+1 = G+2 | — | |
| - cooldown swipe (CooldownFrameTemplate) | IconGrid_Render.lua:228 | button | inherited | **inherited** button+1 = G+2 | — | **ties with the border** |
| - cooldown countdown FontString | IconGrid_Render.lua:254 | button | — | button (G+1), `OVERLAY` | — | **below the swipe and the border child frames** |
| - charges badge FontString | IconGrid_Render.lua:263 | button | — | button (G+1), `OVERLAY` | — | **below the swipe and the border**; sits 2px inside the bottom-right corner, where the border edge is |
| - ready-glow host frame | IconGrid_Render.lua:272-274 | button | inherited | **explicit** button+5 = G+6 | — | |
| - LibCustomGlow effect frames | via core/GlowSetup.lua -> libs/LibKa0s/Glow.lua:112; LCG `addFrameAndTex` :126-133, ButtonGlow :661-671, ProcGlow :906/933 | glow host | inherited | LCG default host+8 = G+14 (KickCD passes no `frameLevel`, docs/module-map.md:419) | — | the highest thing in the grid |
| Grid drag handle (LibKa0s DragHandle) | modules/IconGrid_Handle.lua:132; libs/LibKa0s/WidgetsDragHandle.lua:649-669 | grid | inherited MEDIUM | inherited G+1 (help/close children G+2) | no / inherits clamp of nothing (child) | shown only while unlocked; anchored BOTTOM to the label or grid TOP (:117-124) |
| Grid drag-handle label measurer | WidgetsDragHandle.lua:193-194 | UIParent | default (MEDIUM) | default | — | hidden helper, never shown |
| Cast bar (`KickCDCastbar`, `KickCDCastbarFocus`), one per unit | modules/Castbar_Frame.lua:220-225 | UIParent | **MEDIUM, explicit** | inherited (C) | no / clamped | movable in FREE anchor mode |
| - two background textures | Castbar_Frame.lua:239-240 | cast bar | — | C, `BACKGROUND` | — | alpha-switched per state |
| - spell icon texture | Castbar_Frame.lua:279 | cast bar | — | C, `ARTWORK` | — | the bar is inset beside it (Castbar_Skin.lua:249-252) |
| - bar container | Castbar_Frame.lua:248 | cast bar | inherited | inherited C+1 | — | |
| - two StatusBars | Castbar_Frame.lua:250-251 | bar container | inherited | inherited C+2 | — | stacked, alpha-switched |
| - overlay frame (spark, name, time) | Castbar_Frame.lua:265-267 | bar container | inherited | **explicit** StatusBar+1 = C+3 | — | spark `OVERLAY` (:273), name/time FontStrings `OVERLAY` (:285, :289) |
| - two border frames (BackdropTemplate) | Castbar_Frame.lua:305-311 | cast bar | inherited | **explicit** StatusBar+2 = C+4 | — | **above the overlay text and spark** |
| Cast bar drag handle (DragHandle) | modules/Castbar_Handle.lua:91, :120 | cast bar | inherited MEDIUM | inherited C+1 | — | FREE mode, unlocked only; BOTTOM to label or cast bar TOP |
| Unit label holder (`KickCDUnitLabel<Unit>`) | modules/UnitLabel.lua:157-160 | created on UIParent, **reparented to the unit's grid** on every Apply (UnitLabel.lua:144) | inherited MEDIUM | G+1 (the client re-derives it on each SetParent) | no / no | 1x1 holder; FontString `OVERLAY`; **anchored to the cast bar when Attach to = Cast bar, but still in the grid's level tree** |
| Simulation strip (LibKa0s TestStrip, kind "sim"), one per unit | modules/SimStrip.lua:63-75; libs/LibKa0s/Widgets.lua:817-850 | UIParent | **MEDIUM, explicit** (SimStrip.lua:71) | default, about UIParent+1 = G | no / no | mouse off; uses the same anchor slot as the grid drag handle, which is safe because a sim refuses to start unlocked and stops on unlock (modules/Sim.lua:117-119, :333) |
| Debug console (`KickCDDebugWindow`) | core/DebugLogSetup.lua:168 -> libs/LibKa0s/DebugLog.lua:528-539 | UIParent | **DIALOG, explicit (library)** | default | no / clamped | resize grip at window+GRIP_LEVEL (Core.lua:611) |
| Debug copy window (`KickCDDebugCopyWindow`) | libs/LibKa0s/Widgets.lua:647-656 | UIParent | **FULLSCREEN, explicit (library)** | default | no / clamped | above the DIALOG console that opens it, by design |
| Perf step panel | core/PerfSetup.lua:62 -> libs/LibKa0s/PerfPanel.lua:186-189 | UIParent | **DIALOG, explicit (library)** | default | no / clamped | |
| Sim control panel | modules/Sim.lua:345-362 (`panel = PANEL`) -> libs/LibKa0s/SimPanel.lua:211-214 | UIParent | **DIALOG, explicit (library)** | default | no / clamped | |
| Minimap button (LibDBIcon) | core/LauncherSetup.lua:101 -> libs/LibDBIcon-1.0:246-249 | Minimap | MEDIUM, **fixed** | 8, **fixed** | — | the library pins both |
| Spell-row hover tooltip, status-glyph tooltip, icon hover tooltip | settings/Spells_Rows.lua:205-209; IconGrid_Render.lua (OnEnter) | GameTooltip | TOOLTIP (Blizzard) | Blizzard | — | owns no frame |
| Spells reorder ghost | libs/LibKa0s/WidgetsReorder.lua:107 | UIParent | **TOOLTIP, explicit (library)** | default | — | follows the cursor while dragging |
| Spells reorder insertion line / row boxes | WidgetsReorder.lua:255, :600-601 | list rows | inherited (Settings canvas) | row+20 / row-1 | — | |
| Add-a-spell autocomplete list | settings/Spells_Header.lua:239 (H.IdInput) -> WidgetsAutocomplete.lua:66, :161 / OptionsIds.lua:996-998 | UIParent | **FULLSCREEN_DIALOG, explicit (library)** | default | — / clamped | above the Settings panel |
| Library dropdown menu | libs/LibKa0s/Widgets.lua:225 | UIParent | FULLSCREEN_DIALOG (library) | default | — | |
| AceGUI dropdown pullouts and colour picker (Unit picker, Specialization picker, every schema DD / LSM DD, the per-row Category DD, every CP) | libs/AceGUI-3.0/widgets/AceGUIWidget-DropDown.lua:287-326; AceGUIWidget-ColorPicker.lua:60 | UIParent / Blizzard ColorPickerFrame | **FULLSCREEN_DIALOG (AceGUI)** | default | — | (review) missing from the original inventory; opens above the Settings panel and above the DIALOG library windows |
| Settings canvas pages, Defaults buttons, tab strips, nav rail | settings/*.lua via LibKa0s Options | Blizzard SettingsPanel | Blizzard's (inherited) | library-relative (OptionsTabs.lua:375-377, :712-714) | — | Blizzard owns the panel's strata |
| StaticPopups `KICKCD_RESET_ALL`, `KICKCD_RESET_SPELLS` | settings/General.lua:256; settings/Spells.lua:427 | Blizzard StaticPopup | DIALOG (Blizzard) | Blizzard | — | |
| Cast-event filter frames | core/Util.lua:520 | none | — | — | — | event-only, never shown |

## Problems

| id | file:line | problem |
|---|---|---|
| KIC-S01 | IconGrid_Render.lua:254, :263 vs :219-228 | **The countdown text and the charges badge are drawn under the cooldown swipe and the icon border.** Both FontStrings are regions of the button (G+1), and the Cooldown and border are child frames (G+2), so they draw on top whatever the layer name. The swipe darkens the countdown exactly while it is counting, and the border edge (default thickness 2) overlaps the badge's 2px corner inset. The cast bar solved the same problem with an overlay frame (Castbar_Frame.lua:258-267); the icon does not. The effect has not been checked in game, so it needs an owner look. |
| KIC-S02 | IconGrid_Render.lua:221 vs :228 | The border (explicit button+1) and the cooldown swipe (inherited button+1) **tie at G+2**. Their relative order is left to creation order, so whether the swipe paints over the border is undefined by the code. The comment at :215-218 assumes the swipe "isn't affected". |
| KIC-S03 | Castbar_Frame.lua:265-267 vs :305-311 | The cast bar's borders (C+4) sit **above** the spark and the name/time text (C+3). The spark is 30px tall on a 24px bar (:276), so the border edge cuts across it. Inside-left/right text at offset 0 runs under the edge. The comment at :297-304 chose this so the border is not tinted by the fill, which only needs border > StatusBar (C+2), not border > text. |
| KIC-S04 | IconGrid.lua:568-571; Castbar_Frame.lua:220-223 | Grid and cast bar are sibling MEDIUM frames on UIParent with **equal default levels** (G == C). Where they overlap (FREE cast bar dragged over the grid, or a negative PRIMARY offset), which one wins is undefined. The grid's glow (G+14) beats the whole cast bar (max C+4), but its icons (G+1) lose to the bar (C+2). The draw order is mixed, not layered. |
| KIC-S05 | UnitLabel.lua:140-148, :157 | The **label lives in the grid's level tree (G+1)** even when it is attached to the cast bar. Positioned over the cast bar (for example `CENTER` on `CENTER`), it draws **under** the bar's StatusBars (C+2) and borders (C+4). The element meant to sit *on* its host is below it. |
| KIC-S06 | Castbar_Handle.lua:91; IconGrid_Handle.lua:132 | Each drag handle inherits its host's level+1 (G+1 / C+1). A FREE cast bar's handle placed over the grid (G+1..G+14) can draw under icons or glow. Whenever the frames are unlocked, the grab target should be the topmost element of the addon's HUD. |
| KIC-S07 | SimStrip.lua:71 | The sim strip's strata is set ad hoc (MEDIUM, "same as the HUD") at a default level equal to G. With no unit enabled it floats at `UIParent CENTER 0,180` (docs/module-map.md:463), where a grid or cast bar may be. A marker that the display is fake should never sit under the display it marks. |
| KIC-S08 | IconGrid_Render.lua:274; docs/module-map.md:419 | The glow's z is the sum of two magic numbers (+5 by KickCD, +8 by LibCustomGlow's default = +13 over the button). Neither number is named or tied to the elements it must clear (swipe, border, text). |
| KIC-S09 | DebugLog.lua:536; PerfPanel.lua:186; SimPanel.lua:211 | Three library windows share DIALOG strata at default level and are not `SetToplevel`. The console, perf panel and sim panel can be open together (a perf run under a sim is a documented flow). The last-shown or last-created window wins, and clicking one does not raise it. This is library-owned; KickCD picks none of it. |
| KIC-S10 | IconGrid.lua:571; Castbar_Frame.lua:223; SimStrip.lua:71 | Strata is written as a bare literal `"MEDIUM"` in three files. There is no addon constant, so a future change has to find all three, and a fourth element (the label) gets it only by inheritance. |
| KIC-S11 | IconGrid.lua:568-571 | (review) The Target and Focus grids are also equal-level MEDIUM siblings, so where a player stacks them their order is creation order, the same undefined case as S04 but between units. Low impact: the two are positioned apart by default. A fixed per-unit offset is not worth a band; recorded so the guidance covers it. |
| KIC-S12 | IconGrid_Handle.lua:132 vs the proposed Z05 | (review) Under the original Z07 the grid's handle sits at G+19, which is **below** the same unit's cast bar at C = G+20. In PRIMARY mode with a TOP_* anchor point (a cast bar above the grid), the handle that is anchored to the grid TOP would draw under the bar it touches. The original band table's claim "the drag handle is always the top of what it belongs to" did not hold for the grid handle. Z07 is rewritten below. |

There is no collision between the sim strip and the grid drag handle, even though they use the same anchor slot:
`modules/Sim.lua:117-119` refuses a sim while unlocked, and `:333` stops one on unlock. This mutual exclusion is
deliberate and should be kept.

## Proposed strata map

One HUD strata, **MEDIUM**, for everything that is part of the display. Order within it comes from **level
bands**, not from parentage luck. The library's windows sit above, and Blizzard owns its own frames.

| tier | strata | level band | elements |
|---|---|---|---|
| T0 HUD base | MEDIUM | host H (grid G, cast bar C), with **C = G + 20** set explicitly | grid frame, cast bar frame (its BACKGROUND bg and ARTWORK icon textures) |
| T1 content | MEDIUM | H+1 .. H+2 | icon buttons + spell texture (G+1); cooldown swipe (G+2); cast bar container (C+1) and StatusBars (C+2) |
| T2 frame chrome | MEDIUM | H+3 | icon border (G+3); cast bar borders (C+3) |
| T3 text | MEDIUM | H+4 | new icon text overlay holding the countdown and charges (G+4); cast bar overlay holding spark, name and time (C+4) |
| T4 effects | MEDIUM | H+5 (+ LCG's 8) | ready glow host (G+5, so LCG frames at G+13) |
| T5 attached label | MEDIUM | **attach host's top content level + 1** | unit label: G+14 when attached to the grid, C+5 when attached to the cast bar |
| T6 edit affordances | MEDIUM | **G+39** for both handles (top of the unit's whole HUD, above the cast bar band) | drag handles (grid and cast bar). Review: was H+19, which left the grid handle under its own cast bar (S12) |
| T7 markers | MEDIUM | **G+40** (above both units' bands) | sim strip, while a sim runs |
| T8 addon windows | DIALOG (library) | default; toplevel | debug console, perf panel, sim panel |
| T9 modal over window | FULLSCREEN / FULLSCREEN_DIALOG (library) | default | copy window; autocomplete and dropdown lists |
| T10 cursor | TOOLTIP | — | reorder ghost, GameTooltip |
| Blizzard-owned | as Blizzard sets | — | SettingsPanel and its canvases, StaticPopups, minimap button (LibDBIcon pins MEDIUM/8) |

The bands make three statements true by construction. A unit's cast bar draws over that unit's grid wherever they
overlap (the bar is the live, transient thing). Text is never under chrome. The drag handle and the sim marker are
always the top of what they belong to.

## Proposed changes

| id | change (file:line, from → to) | reason | confidence |
|---|---|---|---|
| KIC-Z01 | IconGrid_Render.lua:254, :263: parent the countdown and charges FontStrings on a new child `btn.textLayer = CreateFrame("Frame", nil, btn)` with `SetAllPoints(btn)` and `SetFrameLevel(btn:GetFrameLevel() + 3)`. The text then sits on that frame's `OVERLAY`, not the button's. Alpha still inherits through the child, so "the text dims with cooldownAlpha" (:253) keeps working. | Text above the swipe and border (S01), the same pattern the cast bar already uses. | 80% |
| KIC-Z02 | IconGrid_Render.lua:221: border `btn+1` → `btn+2`. Leave the Cooldown at its inherited `btn+1`, or set it explicitly at :228. | Breaks the tie, so the swipe sits under the border (S02). | 75% |
| KIC-Z03 | IconGrid_Render.lua:274: glow `btn+5` → `btn+4`, named as a constant (`Const.ICON_LEVEL = { swipe = 1, border = 2, text = 3, glow = 4 }`). | Named levels instead of magic numbers (S08). The glow stays above text (LCG +8 on top). Review: the 5→4 change itself has no visible effect, because both values clear the border and the text; the value is in the naming, and keeping 5 would also be fine. | 60% |
| KIC-Z04 | Castbar_Frame.lua:267, :310-311: overlay `StatusBar+1` → `StatusBar+2`, and borders `StatusBar+2` → `StatusBar+1`. The borders stay above both StatusBars, so the fill tint problem the :297-304 comment guards against stays solved. | Spark and text draw over the border edge (S03). | 55% (visual call; owner check) |
| KIC-Z05 | Castbar_Frame.lua:223: after the strata, `frame:SetFrameLevel(Const.HUD_LEVEL + 20)`, with IconGrid.lua:571 setting the grid to `Const.HUD_LEVEL` explicitly. Prefer the constant to reading the live grid, because the cast bar can be built before its unit's grid. The call must stay **before** the children are created (:248 onwards), so the explicit `barLevel + n` arithmetic below stays relative to the new base. | A defined cast-bar-over-grid order instead of equal levels (S04). Review: this also puts the cast bar over the secondary icons when a secondary block grows into it. That is the intended "live thing on top" ordering, but it is new and needs an owner look. | 65% |
| KIC-Z06 | UnitLabel.lua:144 (`applyLabelPlacement`, immediately **after** the SetParent, because SetParent re-derives the level): `f:SetFrameLevel(topLevelOf(anchorFrame) + 1)`, recomputed on every Apply. Use the named band (C+5 for the cast bar, G+14 for the grid after Z03) rather than walking the children. Keep the parent as the grid for visibility and alpha, and decouple only the level. Apply can run in combat (CONFIG_CHANGED, PLAYER_ENTERING_WORLD); that is safe because the holder is a plain, non-secure Frame. | A label attached to the cast bar draws on the cast bar, not under it (S05). | 65% |
| KIC-Z07 | Castbar_Handle.lua (after :91) and IconGrid_Handle.lua (after :132): `handle:SetFrameLevel(Const.HUD_LEVEL + 39)` for **both** handles. Review: was `host + 19`, which put the grid handle (G+19) under its own cast bar (C = G+20), S12. The DragHandle's help and close children are created inside `lib.DragHandle` before the host can set the level; check in game that they follow the handle (the client normally keeps children above a re-leveled parent), or set the level through a future `levelOffset` spec field (upstream note). | The grab target is the top of its unit's display while unlocked (S06, S12). | 65% |
| KIC-Z08 | SimStrip.lua:71: keep MEDIUM, and add `frame:SetFrameLevel(Const.HUD_LEVEL + 40)`. | The fake-data marker is above every HUD element, including the floating case (S07). It shares level space with the handles at +39 but never coexists with them (Sim.lua:117-119, :333). | 60% |
| KIC-Z09 | core/Constants.lua: add `Const.HUD_STRATA = "MEDIUM"` and `Const.HUD_LEVEL`, and read them at IconGrid.lua:571, Castbar_Frame.lua:223 and SimStrip.lua:71. | One declaration of the addon's HUD tier (S10). This is pure refactor, with the same strata. | 70% |
| KIC-Z10 | (library, not KickCD) LibKa0s DebugLog / PerfPanel / SimPanel: `SetToplevel(true)` on each window. | Clicking a window raises it among its DIALOG siblings (S09). File it against LibKa0s. Review: Blizzard's StaticPopups are DIALOG too, so a clicked console can now rise over an open `KICKCD_RESET_*` popup. That is acceptable, because the player clicked it, and it is no worse than today's creation-order luck. The resize grip (Core.lua:611, `level + GRIP_LEVEL`) keeps its offset on a raise. | 70% |

### Interaction check (review)

- **Settings panel, dropdowns, colour picker:** nothing moves out of MEDIUM, and every proposed level stays well
  under the client cap, so Blizzard's SettingsPanel, the AceGUI pullouts and ColorPickerFrame (FULLSCREEN_DIALOG)
  and the library menus still open above the HUD. A HUD element can never cover an open dropdown.
- **Tooltips:** GameTooltip is TOOLTIP strata and is unaffected. The icon hover tooltip needs `EnableMouse` on the
  button, and Z01's new `textLayer` frame takes no mouse (a plain Frame without `EnableMouse`), so it does not steal
  the hover. Z07's handle raise does not change which frame takes the drag.
- **Combat-protected frames:** KickCD has none. The icon is a plain Button, with SecureActionButton deliberately
  avoided (IconGrid_Render.lua:200-202), so every SetFrameLevel here, including Z06's per-Apply call, is legal in
  combat.
- **Blizzard frames:** the HUD stays in MEDIUM, below Blizzard's HIGH and DIALOG UI, as today. LibDBIcon's
  MEDIUM/8 on the Minimap is untouched.
- **OmniCC-style addons** attach their text to the Cooldown child, which Z01/Z02 leave as it is (at btn+1), so
  their text keeps its place under KickCD's border.
- **Tests:** Z01 changes what `btn.cooldownText` and `btn.chargesText` are parented to. `tests/test_icongrid_render.lua`
  and the frame mock (`tests/wow_mock_frames.lua`) will need to follow.

## Notes for the upstream guidance

- **Text belongs on its own frame above every child frame of the element it labels.** A FontString on a button is
  under that button's Cooldown and Backdrop children, whatever its layer name. KickCD's cast bar does this right
  (an overlay frame) and its icon gets it wrong. Codify it: *a region never shares a frame with a child frame it
  must draw over.*
- **Name the level offsets.** Write each frame's level as `host + <named band>`, never a bare `+1`, `+2` or `+5`,
  and state the order once: content < chrome < text < effects. Let ties be impossible by construction (S02 is a
  tie that the comments assumed away).
- **Siblings on UIParent need explicit relative levels.** Two MEDIUM frames created on UIParent get equal levels,
  and their overlap order is creation order. If an addon's elements can overlap (free-drag plus anchors), the
  standard should require an explicit level band per element class.
- **The edit affordance is the top of its host.** Drag handles, resize grips and selection outlines sit at the top
  of the band of the display they edit (LibKa0s's resize grip already does this with `GRIP_LEVEL`). DragHandle
  could take a `levelOffset` and default to it.
- **Markers of fake data sit above the display.** TestStrip/sim strips should get their level from the library
  (host top + margin) rather than each host choosing a strata. KickCD set MEDIUM by hand.
- **Attachment versus parentage.** When an element is *parented* for visibility (label → grid) but *anchored* to
  something else (label → cast bar), its level must follow the anchor host. Parent-inherited levels are only right
  when parent and anchor are the same frame.
- **Library windows:** DIALOG for addon windows, FULLSCREEN or FULLSCREEN_DIALOG for anything opened *from* one
  (copy, autocomplete, menus), TOOLTIP for cursor-followers. The library already follows this. Add `SetToplevel`
  so same-strata windows raise on click.
- **One strata constant per addon tier**, declared in Constants, so an audit can grep one name instead of string
  literals.
- **Reparenting resets the level.** `SetParent` re-derives a frame's level from the new parent, so an explicit level
  has to be set again after every SetParent, never once at build (Z06).
- **AceGUI pullouts are FULLSCREEN_DIALOG.** A host window that wants a dropdown to open over it must stay at or
  below DIALOG. Put this in the strata table so no addon raises a window into FULLSCREEN_DIALOG and buries its own
  menus.
- **Mutually exclusive overlays may share a slot.** KickCD's sim strip and drag handle share an anchor because the
  sim refuses to run unlocked. The guidance should allow that sharing only when the exclusion is enforced in code,
  not assumed.

## Review

Independent review against `../KickCD` on `master`, 2026-10-24. I grepped every `CreateFrame` / `SetFrameStrata` /
`SetFrameLevel` / `SetToplevel` / `SetClampedToScreen` / `SetParent` in `core/`, `modules/` and `settings/`, and
re-read IconGrid_Render.lua:199-290, Castbar_Frame.lua:215-320, UnitLabel.lua:125-175, SimStrip.lua:55-90 and both
handle builders. On the library side I read the strata calls in `libs/LibKa0s`, LibCustomGlow's `frameLevel`
defaults and the AceGUI DropDown and ColorPicker strata.

- **Inventory: accurate on every row I checked.** One correction: the label's reparent is at UnitLabel.lua:144, and
  the client re-derives the level on each SetParent. One missing row: AceGUI dropdown pullouts and the colour picker
  (FULLSCREEN_DIALOG), which are the frames most likely to collide with a raised window. KickCD passes no
  `frameLevel` to the glow (IconGrid_Render.lua:487), so LCG's +8 is confirmed.
- **Problems added:** S11 (Target and Focus grids tie, low impact) and S12. Under the original Z07 the grid handle
  (G+19) sat under its own cast bar (C = G+20), which contradicted the map's own "handle is the top" claim.
- **Changes rewritten:**
  - Z07 now puts both handles at HUD_LEVEL+39 (70→65%, because the DragHandle's help and close children need an
    in-game check).
  - Z05 now uses the constant, not the live grid, and records the creation-order requirement and the new
    bar-over-secondary-icons effect.
  - Z06 is pinned to after the SetParent at :144, and its combat safety is stated.
  - Z08 now uses the constant.
  - Z03 now says the 5→4 number change is cosmetic.
  - Z10 now notes the StaticPopup interaction (75→70%).
- **Added:** an interaction check covering the Settings panel, dropdowns, tooltips, combat-protected frames (none),
  Blizzard frames, OmniCC and the test impact, plus two upstream guidance notes (reparent resets the level; AceGUI
  pullouts are FULLSCREEN_DIALOG).
- **No change fell under 40%**, so nothing moved to rejected. Z01/Z02/Z04 are unchanged; Z04 stays an owner visual
  call.
