# AbsorbTracker — frame strata analysis

Scope: item 030. Read from `../AbsorbTracker` at `master` on 2026-10-24: `modules/{Bar,Display}.lua`,
`core/{AbsorbTracker,LauncherSetup,DebugLogSetup,PerfSetup,WidgetsSetup}.lua`, `settings/*.lua`, and the vendored
code that creates frames on the addon's behalf (`libs/LibKa0s/{WidgetsDragHandle,DebugLog,PerfPanel,Widgets,
Options,OptionsTabs,OptionsCombat}.lua`, `libs/LibDBIcon-1.0`, `libs/AceGUI-3.0*`).

**Headline: the addon itself sets no strata and no frame level anywhere** (`grep -rn 'Strata\|FrameLevel\|Toplevel'
core modules settings` returns nothing; the addon's only `CreateFrame` calls are modules/Bar.lua:187, :214 and the
event frame at core/AbsorbTracker.lua:195). Everything the addon owns rides UIParent's MEDIUM and the implicit
parent+1 level. Every explicit strata in the inventory is a library's choice.

## Inventory

| element | file:line | parent | strata | frame level | toplevel / clamped | notes |
|---|---|---|---|---|---|---|
| Absorb bar ×3 (`AbsorbTrackerFrame`, `…TargetFrame`, `…FocusFrame`) | modules/Bar.lua:187, 246-250 | UIParent | MEDIUM, **inherited** | inherited (UIParent+1); **all three equal** | no / clamped (Bar.lua:212) | BackdropTemplate; mouse and movable only while unlocked (Display.lua:237-239); scaled by Master scale (Display.lua:234), alpha = barAlpha × Master alpha (Display.lua:229); created hidden (Bar.lua:243) |
| Bar backdrop: background centre + border edge | modules/Bar.lua:190-203; modules/Display.lua:188-203 | regions on the bar itself (BackdropTemplate pieces) | bar's | **bar's own level** (centre in BACKGROUND, edge pieces in BORDER layer) | — | `edgeSize = borderSize` (0-16 px), background inset `max(1, floor(borderSize/4))` |
| Fill StatusBar | modules/Bar.lua:214-221 | bar | inherited | **inherited, bar+1** | — | anchored at a **fixed 3 px inset** (Bar.lua:215-216) regardless of `borderSize`; its texture covers only the filled fraction |
| Value text FontString | modules/Bar.lua:224-227 | statusBar | inherited | statusBar's (bar+1), OVERLAY layer | — | anchored to the bar's centre |
| Drag handle (unlocked strip) ×3 | modules/Bar.lua:128-181 → libs/LibKa0s/WidgetsDragHandle.lua:653 | bar | inherited | **inherited, bar+1** (same as the fill; the widget sets no level) | no / not clamped (rides the bar's clamp) | anchored BOTTOM to bar TOP + `DRAG_HANDLE.GAP` (Bar.lua:179); shown only unlocked (Display.lua:249-256); inherits bar alpha and scale |
| Drag handle help mark `?` | libs/LibKa0s/WidgetsDragHandle.lua:394 | handle | inherited | handle+1 | — | |
| Drag handle close mark `X` | libs/LibKa0s/WidgetsDragHandle.lua:447 | handle | inherited | handle+1 | — | turns off one bar (Bar.lua:33-37) |
| Label measurer (hidden) | libs/LibKa0s/WidgetsDragHandle.lua:194 | UIParent | inherited | inherited | — | never shown; not visual |
| Drag strip / mark tooltips | modules/Bar.lua:78-94 (placement), WidgetsDragHandle | GameTooltip | TOOLTIP (Blizzard) | Blizzard | — | placed beside the strip by `NS.Util.PlaceTooltipBeside` |
| Minimap button | core/LauncherSetup.lua:107 → libs/LibDBIcon-1.0/LibDBIcon-1.0.lua:246-249 | Minimap | MEDIUM, **explicit + fixed** (`SetFixedFrameStrata`) | 8, **explicit + fixed** (`SetFixedFrameLevel`) | — | not the addon's choice |
| Debug console `AbsorbTrackerDebugWindow` | core/DebugLogSetup.lua:123 → libs/LibKa0s/DebugLog.lua:533-539 | UIParent | DIALOG, **explicit** (library) | inherited; title-bar buttons +1 (DebugLog.lua:336-337) | **not toplevel** / clamped | opened from General > Master controls > Debug console |
| Console copy window | libs/LibKa0s/Widgets.lua:648-656 (opened by the console's Copy button, DebugLog minor 12) | UIParent | FULLSCREEN, **explicit** (library) | inherited | not toplevel / clamped | deliberately one tier above the DIALOG console (Widgets.lua:651-652) |
| Perf panel `AbsorbTrackerPerfPanel` | core/PerfSetup.lua:35 → libs/LibKa0s/PerfPanel.lua:183-189 | UIParent | DIALOG, **explicit** (library) | inherited | **not toplevel** / clamped | `/at perf` |
| Reset-all confirmation `ABSORBTRACKER_RESET_ALL` | settings/General.lua:127, 331-356 | StaticPopup | DIALOG (Blizzard) | Blizzard | toplevel (Blizzard) | |
| Settings canvases (landing, General, Appearance, Profiles) | libs/LibKa0s/Options.lua; settings/General.lua:363, Appearance.lua:286, Profiles.lua:41 | Blizzard SettingsPanel | SettingsPanel's (Blizzard-owned; not set by the addon) | Blizzard; tab panel = body level (OptionsTabs.lua:374-377), tab buttons +1 (OptionsTabs.lua:712-714) | — | |
| Combat cover over a settings page | libs/LibKa0s/Options.lua:589-590; OptionsCombat.lua:160 | panel | inherited | **raised explicitly** above panel content (`__coverLevel`) | — | library-owned |
| Appearance chrome band widgets (Unit DD, mirror CB, Copy BTN) | settings/UnitPanel.lua:172-216 | chrome frame from PageHeader | inherited | inherited | — | AceGUI widgets reparented into the band |
| AceGUI dropdown pullouts (Font flags, Unit, General visibility) | libs/AceGUI-3.0/widgets/AceGUIWidget-DropDown.lua:287, 309, 320 | UIParent | FULLSCREEN_DIALOG, explicit (AceGUI) | — | scroll frame toplevel | third-party |
| LSM dropdown pullouts (bar/background texture, border, font) | libs/AceGUI-3.0-SharedMediaWidgets/prototypes.lua:212 | UIParent | TOOLTIP, explicit (AGSMW) | — | — | third-party; shares a tier with GameTooltip |
| Colour picker | libs/AceGUI-3.0/widgets/AceGUIWidget-ColorPicker.lua:60 | Blizzard ColorPickerFrame | FULLSCREEN_DIALOG, explicit (AceGUI) | — | — | third-party |
| Event frames ×3 (+ library event frames) | core/AbsorbTracker.lua:195 | none | — | — | — | not visual |

Not used by this addon (checked, so not inventoried): LibKa0s-Widgets' own dropdown menu (Widgets.lua:224,
FULLSCREEN_DIALOG); no `Widgets.Dropdown` call exists in core/, modules/ or settings/.

## Problems

| id | file:line | problem |
|---|---|---|
| ABS-S01 | modules/Bar.lua:187 | **No explicit strata on the addon's only HUD frames.** The bars inherit MEDIUM from UIParent, so the tier is a side effect of the parent, not a decision. Nothing records where the bars are meant to sit relative to Blizzard's unit frames, nameplates or other HUD addons. |
| ABS-S02 | modules/Bar.lua:214-216 vs modules/Display.lua:188-203 | **The fill draws over the border.** The border edge is a backdrop region on the bar's own level and is `borderSize` px wide (up to 16), but the fill StatusBar is a child at bar+1 inset a fixed 3 px. With any border thicker than 3 px, the fill (higher level) paints over the inner part of the border **only along the filled fraction** (the unfilled part of a StatusBar is transparent), so the border's inner edge visibly changes width where the fill ends. The element that frames the bar sits *under* the thing it frames. |
| ABS-S03 | modules/Bar.lua:187, 246-250 | **Three sibling bars at the same strata and level, so overlapping bars interleave.** With every bar at level L and every fill/handle at L+1, an overlap does not merely tie: bar A's fill (L+1) draws over bar B's backdrop (L) and B's fill over A's backdrop, whichever bar is "in front". The drag handle of one bar (bar+1) ties with the other bar's fill (also bar+1), so a strip can disappear under a neighbouring bar's fill and its clicks go to the wrong frame. Display.lua:21-26 already had to space the default stack to keep a strip off the bar above; that is a positional workaround for a z-order tie. |
| ABS-S04 | libs/LibKa0s/WidgetsDragHandle.lua:653; modules/Bar.lua:128 | **The drag handle shares its level with the fill and the value text's host.** It is the interactive overlay of the unlocked state but has no level margin above the content it overlays (bar+1 = statusBar). Fine in isolation (it sits outside the bar), wrong under S03. |
| ABS-S05 | modules/Display.lua:229, 234 | **The drag handle inherits the bar's alpha.** With `barAlpha` or Master alpha low (to 0%), the unlocked strip, its `?` and its `X` fade with the bar and can become invisible but still clickable. An affordance for moving the frame should not be dimmed by the frame's own content opacity. (Alpha, not strata, but it is the same overlay-inherits-from-content mistake.) |
| ABS-S06 | libs/LibKa0s/DebugLog.lua:536; libs/LibKa0s/PerfPanel.lua:186 | **Two DIALOG windows, neither toplevel.** The debug console and the perf panel are both explicit DIALOG with no `SetToplevel(true)` (grep confirms none in either file). Opened together (the perf flow opens the console, core/PerfSetup.lua:108), clicking the one underneath does not raise it. Library-owned; same in every consumer. |
| ABS-S07 | libs/LibKa0s/DebugLog.lua:536; settings/General.lua:331 | **Console and Reset-all popup share DIALOG.** The StaticPopup is toplevel and raises on show, so today it wins, but only through Blizzard's toplevel behaviour; the order afterwards depends on clicks. Minor. |
| ABS-S08 | libs/AceGUI-3.0-SharedMediaWidgets/prototypes.lua:212 | LSM pullouts are TOOLTIP strata, the same tier as GameTooltip; a row tooltip can draw under or over an open texture list depending on level. Third-party, not fixable here; noted for the guidance only. |
| ABS-S09 | (whole addon) | **No written layering intent.** There is no comment or doc stating the addon's tiers (HUD, overlays, windows, modals), so each new element (the drag strip, the close mark) inherited whatever its parent had. |

## Proposed strata map

Levels are relative to the bar's own base level `L` (whatever the engine assigns at creation), never absolute
numbers, so the band survives a parent change.

| tier | strata | level band | elements |
|---|---|---|---|
| T1 HUD content | **MEDIUM (explicit)** | L+0 bar frame and backdrop background; L+1 fill StatusBar; **L+2 border frame**; **L+3 value text** | the three bars |
| T2 HUD overlays (unlocked only) | MEDIUM (same as its bar) | **L+5** drag handle; L+6 its `?` and `X` | drag strips |
| T3 Launcher | MEDIUM, level 8 fixed (LibDBIcon) | — | minimap button (not the addon's choice; a bar dragged over the minimap draws under the button, L being low) |
| T4 Settings | Blizzard SettingsPanel | library bands (tab strip +1, combat cover on top) | canvases, band widgets |
| T5 Tool windows | DIALOG, **toplevel** (upstream Z07) | inherited | debug console, perf panel |
| T6 Modals over tools | DIALOG toplevel (Blizzard) / FULLSCREEN | — | Reset-all StaticPopup; console copy window (FULLSCREEN, above the console that opens it) |
| T7 Pickers / pullouts | FULLSCREEN_DIALOG / TOOLTIP (AceGUI, AGSMW) | — | dropdown pullouts, colour picker |
| T8 Tooltips | TOOLTIP (Blizzard) | — | GameTooltip for strips and rows |

Rule of thumb for the addon: content < its border < its text < its interactive overlay, all inside the bar's own
strata; a window the player opens sits in DIALOG and is toplevel; anything opened *from* a window sits one tier
above it.

## Proposed changes

| id | change (file:line, from → to) | reason | confidence |
|---|---|---|---|
| ABS-Z01 | modules/Bar.lua:187-188: after `CreateFrame`, add `bar:SetFrameStrata("MEDIUM")` (from: inherited MEDIUM → explicit MEDIUM). Same visual result today. | Makes the HUD tier a decision with a name, so a reparent or a UIParent change cannot move it silently (S01, S09). The bars are plain, non-secure frames, so the call is safe at file load and in combat. | 85% |
| ABS-Z02 | modules/Bar.lua:190-203 + Display.lua:188-203: move the **border edge** off the bar's backdrop onto a new child frame `bar.border` (BackdropTemplate, edge only, `SetAllPoints(bar)`, mouse left disabled so drags still reach the bar) at `bar:GetFrameLevel() + 2`; the bar keeps the background (from: edge at L+0 under fill at L+1 → edge at L+2 above fill). The fill keeps its 3 px anchor, so its size does not change. The appearance pass's clear-then-set `SetBackdrop` dance (Display.lua:199-201) applies to both frames. | The border frames the bar, so it must sit above the fill (S02), and the edge stops changing width where the fill ends. Pure z-order: no inset or size change. Visible change at `borderSize` > 3 (the border now covers the outer edge of the fill instead of the reverse); needs an owner smoke look at borderSize 1, 3, 8, 16. | 60% |
| ABS-Z03 | modules/Bar.lua:224: re-host the value text on `bar.border` (or its own child frame) at `L+3` (from: statusBar's OVERLAY at L+1 → L+3). Anchor unchanged (bar centre). | With Z02 the border would otherwise draw over text on a short, thick-bordered bar; text is always top of the content stack. | 60% (depends on Z02) |
| ABS-Z04 | modules/Bar.lua:178-180: after the handle is built, `handle:SetFrameLevel(bar:GetFrameLevel() + 5)` (from: inherited L+1 → L+5). The `?` and `X` are the handle's children; confirm in client that they still sit above the strip after the parent's level moves, and re-level them to handle+1 if not. Better long-term: a `levelOffset` option on `Widgets.DragHandle` upstream, so every consumer gets the margin. | Gives the interactive overlay a margin over every content level of *any* bar at the same base, so an overlapping neighbour's fill or text can no longer cover a strip (S03, S04). Tooltips (TOOLTIP strata) are unaffected. | 75% |
| ABS-Z05 | modules/Bar.lua:187-212: `bar:SetToplevel(true)` (from: not toplevel → toplevel) so the bar being dragged comes to the front while unlocked. Locked bars take no mouse (Display.lua:239), so locked behaviour is unchanged. **Interaction to verify in client:** a raise changes the bar's level, and Z02-Z04's explicit child offsets must still hold afterwards (re-apply them in the appearance pass or `OnMouseDown` if the client does not re-base children). Alternative if that is fragile: fixed per-unit base levels (player L, target L+10, focus L+20) for a deterministic order, at the cost that a lower bar's strip sits under a higher bar's content when they overlap. | Resolves S03's interleaving in the one state where it matters (positioning). | 50% |
| ABS-Z06 | modules/Bar.lua:178-180: `handle:SetIgnoreParentAlpha(true)` (from: inherits `bar:SetAlpha` → full opacity), keeping the handle a child of the bar so scale, show/hide and clamp still ride the bar. `tests/wow_mock.lua` needs the method stubbed. | The move affordance must stay visible at 0% bar opacity (S05). Much smaller than the earlier reparent-to-UIParent idea (rejected below). Alpha rather than strata, so it is adjacent to item 030's scope; listed because it is the same overlay-inherits-from-content rule. | 60% |
| ABS-Z07 | Upstream, libs/LibKa0s/DebugLog.lua:536 and PerfPanel.lua:186: add `frame:SetToplevel(true)` (from: not toplevel → toplevel). Not an AbsorbTracker edit; lands through a re-vendor. | Two DIALOG tool windows need click-to-raise (S06, S07). The copy window stays FULLSCREEN above both; AceGUI pullouts (FULLSCREEN_DIALOG) and the StaticPopup are unaffected. Library-owned, so it fixes every consumer at once. | 80% |
| ABS-Z08 | Add a short "Layering" paragraph to `docs/ARCHITECTURE.md` (and a pointer in the Bar.lua header) recording the tier table above. | S09: the next overlay should read the intent instead of inheriting a level. | 85% |

## Considered and rejected

| id | change | why rejected | confidence |
|---|---|---|---|
| ABS-ZR01 | Reparent the drag handle to UIParent (sibling of the bar, explicit MEDIUM, level L+5, scale copied each pass) so it escapes the bar's alpha. | Touches the show/hide ladder (the handle would no longer hide with the bar), the clamp and the scale pass, and the level would have to track Z05's raises. `SetIgnoreParentAlpha` (Z06) gets the same result in one call. | 25% |
| ABS-ZR02 | Inset the fill by the full `borderSize` instead of moving the border (Z02's alternative). | Changes the fill's size, which is a layout/visual change beyond z-order and would alter every existing bar with a border thicker than 3 px. Kept only as the guidance's alternative wording. | 30% |
| ABS-ZR03 | Raise the bars to HIGH so they draw over Blizzard unit frames. | No reported problem, and HIGH would put HUD bars over the Settings panel and other addons' windows; MEDIUM is the right HUD tier. | 10% |

## Notes for the upstream guidance

- **State the HUD tier explicitly.** A display frame parented to UIParent should still call `SetFrameStrata`, so
  the tier is a decision, not inheritance. AbsorbTracker is a clean example of "no strata anywhere, works by
  accident".
- **Content stack inside one display element**: background < fill < border < text < interactive overlay. A
  backdrop border drawn on the parent while the fill is a child is the classic way to get the border *under* the
  fill; codify "the border is a frame above the fill, or the fill is inset by the full border width".
- **Relative level bands, never absolute numbers.** Express levels as `parent:GetFrameLevel() + n` with a fixed
  per-class offset (content +0..+3, overlays +5..+6), and leave a gap so a new layer can slot in.
- **Overlays must outrank sibling content, not just their own parent.** When several same-strata siblings can
  overlap (movable bars, icons, windows), their children interleave by level, so an overlay at parent+1 ties with
  the neighbour's child at parent+1. Put overlays well above the content band, and make movable siblings toplevel
  (or give them a deterministic base order).
- **Affordances should not inherit content alpha.** A drag strip, close mark or resize grip parented to a frame
  whose opacity is a user setting can vanish while still clickable. Use `SetIgnoreParentAlpha(true)` on the
  affordance. LibKa0s `Widgets.DragHandle` could take `levelOffset` and `ignoreParentAlpha` options so every
  consumer gets both.
- **Tool windows**: DIALOG + `SetToplevel(true)` + clamped; a window opened from a tool window goes one tier up
  (the LibKa0s copy window's FULLSCREEN-over-DIALOG choice is the model and is already commented in
  Widgets.lua:651-652). This belongs in LibKa0s so every consumer gets it.
- **Third-party tiers to document, not fight**: LibDBIcon (MEDIUM/8, fixed), AceGUI pullouts and colour picker
  (FULLSCREEN_DIALOG), AGSMW pullouts (TOOLTIP), StaticPopup (DIALOG toplevel). The guidance should list them so
  an addon's own windows are placed relative to known neighbours.

## Review

Independent review, 2026-10-24, against `../AbsorbTracker` `master` (every `CreateFrame` / strata / level / toplevel
call in core/, modules/, settings/ and the vendored libraries the addon drives was re-read).

- **Inventory verified.** Confirmed the addon sets no strata, level or toplevel anywhere, and that
  WidgetsDragHandle sets no level (the handle really is bar+1). Fixed line refs for the backdrop pass
  (Display.lua:188-203). Added: backdrop pieces live on the bar's own level in BACKGROUND/BORDER layers; the fill
  texture covers only the filled fraction; LibDBIcon's fixed strata/level flags; the copy window's opener; that
  LibKa0s-Widgets' own dropdown menu is not used here (checked, so not inventoried).
- **Problems sharpened.** S02 now says the border's inner edge changes width where the fill ends (the visible
  symptom); S03 now says overlapping bars *interleave* (each fill over the other's backdrop), not just tie.
- **Interaction checks.** Z01-Z04 do not touch tooltips (TOOLTIP), pullouts (FULLSCREEN_DIALOG), the Settings
  panel or any protected frame (the bars are not secure). Z02's border frame keeps mouse disabled so drags still
  reach the bar. Z04 gains a check that the marks still sit above the strip after its level moves, and an upstream
  `levelOffset` option. Z05 gains a warning that a raise moves the bar's level and the explicit child offsets
  must survive it; confidence lowered 55% → 50%. Z07 checked against the copy window, popup and pullouts.
- **Z06 rewritten**: the reparent-to-UIParent version (40%) moved to Considered and rejected as ZR01 (25%),
  replaced by `SetIgnoreParentAlpha(true)` on the handle (60%), which keeps show/hide, scale and clamp intact.
- **Added "Considered and rejected"** with ZR01-ZR03 (reparent, inset-the-fill alternative, HIGH strata).
- Guidance notes: added the interleaving wording, `SetIgnoreParentAlpha`, and a suggested DragHandle API.
