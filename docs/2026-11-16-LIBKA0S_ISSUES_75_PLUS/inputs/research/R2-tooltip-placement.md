# R2-tooltip-placement — LibKa0s#92, the tooltip placement surface

Read-only research. Sources: LibKa0s `master` @ `9bc9cc51` (tag v1.104.0); WowAddonStandards `master` @ `3dfb951`
(v2.112.2); addon default branches (`master`, except **SkillMaster and CombatTrail, whose default branch is `main`**,
which contradicts CommonTasks/CLAUDE.md's "every collection repo's default branch is master"; detect per repo).

## 1. What the standard requires (normative text)

`WowAddonStandards/standards/standards/standalone-windows.md:107-171` (*Tooltip placement*, MUST, v2.112.0):

- **Binds** (`:113-121`): addon windows plus docked frames and modals; HUD displays; **library-drawn windows** (debug
  console and copy window, perf, sim and step panels, icon browser, CopyWindow); "an open dropdown menu the addon or
  `LibKa0s-Widgets-1.0` draws itself"; the minimap button. It applies to GameTooltip, custom tooltips and chart hovers.
- **Does not bind** (`:123-130`): Settings-canvas pages, **including the library's own Options widgets**; anything the
  client places (`MenuUtil.SetTooltip`, the launcher's options menu, lines added to client-anchored tooltips; v2.112.1);
  an LDB display's bar; Blizzard frames.
- **Body rule** (`:143-150`): beside the **whole window group**, right if `tipW + gap` fits else left. Right side is
  `TOPLEFT` at `groupRight + 2, elementTop`; left side is `TOPRIGHT` at `groupLeft - 2, elementTop`. A companion panel
  prefers the side away from the main window. Compare in screen space with effective scale. Clamp vertically. Never
  cover the group. If neither side fits, fall back to chrome-below on the element (flip above at the bottom).
  Comparison tooltips go outward via `SetAnchorType("ANCHOR_RIGHT"/"ANCHOR_LEFT",0,0)` (SHOULD). Menu entries use the
  **menu frame** as the group.
- **Chrome rule** (`:152-158`): attached and centered on the element. Top chrome is `TOP` on `BOTTOM`, `0,-2`. Bottom
  chrome (footer, grip) is `BOTTOM` on `TOP`, `0,+2`. Modal controls go below. Flip only when the screen has no room.
  Clamp horizontally. The tooltip may cover the body.
- **Launcher** (`:160`): the vertical side comes from the screen half of the button's center (upper half opens below,
  lower half above). The horizontal side comes from the third (right third `…RIGHT` on `…RIGHT`, left third `…LEFT`,
  middle centered). Gap ±2. LibDBIcon's 0 px `getAnchors` is accepted **until the placer ships**.
- **Library surface** (`:162-167`): beside-the-window placer, attached-centered placer, launcher placer, `TIP_GAP = 2`.
  "The major, file and minor are the library's to choose" (`library-stack.md:127`). **"A window the library draws is
  the library's to move, in that same release"** (`:169`).
- **Verification** (`:173`): a headless SHOULD covers each placer with a right-fits and a right-does-not-fit fake
  screen, asserting side, top alignment and gap from the recorded points. A smoke MUST covers each window near each
  screen edge.
- launcher-§7 (`launcher.md:163-167`): "No host re-anchors the button's tooltip itself", so the gap is the library's
  to add. frame-layering-§4 (`frame-layering.md:88`): a tooltip is never moved below T9. anti-pattern #119
  (`anti-patterns.md:148`).
- Chrome classification readings flagged for the owner in v2.112.0 (`CHANGELOG.md:6`): **a HUD drag strip or mover
  handle is top chrome.** That matters below (§4.3).

## 2. Inventory: every tooltip anchor in `LibKa0s/LibKa0s/*.lua` (master)

Classification: **B** body, **C-top** top chrome, **C-bot** bottom chrome, **L** launcher, **OOS** out of scope
(Settings canvas).

| # | file:line | Code today | Element | Class | Move |
|---|---|---|---|---|---|
| 1 | `IconBrowser.lua:300` | `GameTooltip:SetOwner(cell, "ANCHOR_RIGHT")` | grid cell (window body) | **B** (group = browser window) | beside |
| 2 | `IconBrowser.lua:526-527` | `b.helpers.AttachTooltip(widget, …)` resolves to `OptionsWidgets.lua:499` `ANCHOR_RIGHT` | browser **toolbar** controls (search, buttons) | **C-top** | attached below; needs an AttachTooltip placement option (§4.5) |
| 3 | `IconBrowser.lua:61` (helpers.TabStrip) resolves to `OptionsTabs.lua:731` `ANCHOR_RIGHT` | tab tooltips, if the browser's tabs carry tips | **C-top** | attached below (only if a tab tip exists) |
| 4 | `WidgetsDropdown.lua:292` | `GameTooltip:SetOwner(row, "ANCHOR_RIGHT")` in `lib.__rowTip` | entry of a **library-drawn menu** | **B** (group = menu frame, rule 6) | beside the menu frame |
| 5 | `WidgetsDropdown.lua:291` | `opt.tooltip(row, opt)`, a host renderer that places it itself | same | **B** | library places **after** the renderer returns (§4.4) |
| 6 | `WidgetsReorder.lua:688` | `GameTooltip:SetOwner(self, "ANCHOR_RIGHT")` on the drag handle inside a row | control in a row | **B** (group = host window; OOS when the list sits on a Settings page) | beside |
| 7 | `SimPanel.lua:357` | `tip:SetOwner(owner, "ANCHOR_RIGHT")` in `showTip`; called by `makeButton` `:396` and by `SimPanelRender.lua:219-221` (`d.tooltip = showTip`, `SimPanel.lua:611`) for step rows | step-panel **rows and controls** | **B** ("the controls of a library window whose content is controls … are body", terms table `:137`) | beside the panel (plus the docked/companion frame if the panel docks) |
| 8 | `WidgetsDragHandle.lua:473` | `tip:SetOwner(UIParent, "ANCHOR_CURSOR")` (`tooltipOwner="cursor"`) | HUD drag strip and marks | **C-top** (strip = HUD's title bar) | attached below the strip, restricted-tree safe |
| 9 | `WidgetsDragHandle.lua:475` | `tip:SetOwner(frame, t.anchor or spec.tooltipAnchor or "ANCHOR_TOP")` | same | **C-top** | same |
| 10 | `WidgetsDragHandle.lua:526` | fallback `SetOwner(UIParent,"ANCHOR_CURSOR")` when the host's `place` fails | same | **C-top** | fallback becomes the library's attached placer, never the cursor |
| 11 | `WidgetsDragHandle.lua:522-524` | `tooltipPlace(tip, frame)` host hook (minor 4) | same | — | keep the hook (additive, frozen -1.0); the default changes |
| 12 | `Charts.lua:459` | `self.tip(owner, tip, anchor or "ANCHOR_CURSOR_RIGHT")`, the default for every hoverable | chart marks (bars, segments, rows, scale) | **B** | beside the host's window group |
| 13 | `Charts.lua:306` | `plainTip` → `tip:SetOwner(owner, anchor)` | (the seam) | — | plainTip places via the beside placer; the `anchor` arg becomes a placement hint |
| 14 | `ChartsRender.lua:121` | `hoverable(ctx, f, "ANCHOR_TOP")`, strip bar | chart mark | **B** | beside (drop the per-mark anchor) |
| 15 | `ChartsRender.lua:30-32,61,80,133,153,240` | `hoverable(ctx, f)` with the default from #12 | chart marks | **B** | beside |
| 16 | `Launcher.lua:582` + LibDBIcon `libs/LibDBIcon-1.0/LibDBIcon-1.0.lua:51-57,71-74` (MINOR 52, vendored copy e.g. `../MultiMeters/libs/`) | LibDBIcon `SetOwner(btn,"ANCHOR_NONE")`, `SetPoint(getAnchors(btn))` at 0 px, then calls our `OnTooltipShow = drawTooltip` (`Launcher.lua:403-420`) | minimap button | **L** | re-place inside `drawTooltip` (§4.6) |
| 17 | `DebugLogWindow.lua:179,213,298,493` | `OnEnter` recolors only; **no GameTooltip anywhere in DebugLog*.lua** | — | — | **nothing to move at v1.104.0**; the issue's "debug console moves too" is vacuous unless the plan also adds tips |
| 18 | `Widgets.lua:797-800` (Footer marks) | `spec.onEnter`, host-drawn | footer marks | **C-bot** | optional: `spec.tooltip` placed above by the library (additive) |
| 19 | `PerfPanel.lua:204` | recolor only, no tooltip | — | — | N/A |
| 20 | `WidgetsLineChart.lua:22,694` | the widget reports an index and the host draws the tip | — | — | host's (adoption) |
| 21 | `OptionsWidgets.lua:499` (AttachTooltip), `OptionsTabs.lua:731`, `OptionsNav.lua:165`, `OptionsDrawer.lua:309`, `OptionsIdList.lua:420,633`, `OptionsKeybinds.lua:736`, `OptionsSkinPicker.lua:487` (`ANCHOR_TOP`) | `ANCHOR_RIGHT` / `ANCHOR_TOP` | Settings-canvas widgets | **OOS** | leave, **except** when reused in a standalone window (#2, #3) |

GetCursorPosition reads at `WidgetsDropdown.lua:569`, `WidgetsReorder.lua:210,458,527` and `WidgetsLineChart.lua:615`
are drag and hover math, not tooltip following, so #119 is not reached.

Net library moves: **IconBrowser (2-3 sites), WidgetsDropdown (2), WidgetsReorder (1), SimPanel (1 function, 2
callers), WidgetsDragHandle (3 + default), Charts/ChartsRender (2 seams + 1 literal), Launcher (1)**. The debug console
and PerfPanel have none.

## 3. Prior art in the collection

- DropWatcher `modules/RowTooltip.lua:120-137` (`RT.Place`): ancestor walk to `tipHost`, else the outermost frame under
  UIParent. It joins a `tipDocked` companion into one span (`spanOf` `:85-94`), uses effective-scale screen px and
  picks the side via `MineCells.DockSide`. **But it anchors `BOTTOMLEFT` at the row top**, which is the pre-v2.112
  shape. The rule now wants `TOPLEFT` at the row top.
- DropWatcher `modules/RollsPanel.lua:317-330` (`RP.PlaceTip`): `TOPLEFT` on panel `TOPRIGHT` + gap, with dy from the
  row top. This is the owner's "good example". It does no clamp or fit check.
- AuraMaster `modules/Anchors_Tooltip.lua` (`docs/module-map.md:114`): reads the strip rect through `NS.Secrets.NumberOr`
  and pins **to UIParent only** (the strip sits in a `DisableUntrustedLayoutScriptsTemplate` tree, so SetOwner and
  SetPoint against it are refused: `WidgetsDragHandle.lua:464-469`). If the rect is secret, it falls back beside the
  entry cursor position.
- AbsorbTracker `modules/Bar.lua:151`, KickCD `core/Util.lua:76`, ConsumableMaster `modules/MacroBar.lua:306` all set
  `tooltipPlace = …PlaceTooltipBeside` on their HUD strips, **beside the strip**. Under v2.112.0's reading the strip is
  **top chrome**, so these three plus AuraMaster become attached-below at adoption (see Q3).
- Charts hosts: DpsRace and CombatTrail `core/ChartsSetup.lua` pass `tip = cursorTip` (cursor-anchored, which is #119).
  LootHistory `modules/AnalyticsCharts.lua:41` passes `tip = showTip`. DropWatcher uses plainTip.

## 4. Proposed design

### 4.1 Where it lives: a new major `LibKa0s-Tooltip-1.0`, minor 1, file `LibKa0s/Tooltip.lua`

| Option | For | Against |
|---|---|---|
| **New major `LibKa0s-Tooltip-1.0`** (recommended) | Consumers span five majors (Widgets, Charts, IconBrowser, Launcher, the SimPanel host) and every addon. A leaf major with **no dependency** (pure geometry plus UIParent) creates no new edges: Charts and Launcher today do not need Widgets. It has its own minor stream, its own `docs/api/Tooltip/` and a clean CONSUMERS row. The standard's name "LibKa0s tooltip placement" maps 1:1. | One more major (twenty). Each consumer does a guarded `LibStub("LibKa0s-Tooltip-1.0", true)`. |
| Module of Widgets (`WidgetsTooltip.lua`, Widgets key gains a field) | No new major | Forces Charts, Launcher and IconBrowser to read Widgets at call time. It widens the compound key that other #75+ items also touch, so collision risk is high. |
| Core (`CoreTooltip.lua`) | Everyone already loads Core | Core is the skin/backdrop/pixel base. It bumps Core's key, which every module's `NEEDS_CORE` reads, and the ripple is large. |

Load order: put `<Script file="Tooltip.lua"/>` right after `CorePixel.lua` in `LibKa0s.xml` (`:3`), before Charts
(`:17`) and Widgets (`:32`).

### 4.2 API (all placers act on a tooltip that is **already filled and shown**, so the real width and height are known)

```lua
local Tip = LibStub("LibKa0s-Tooltip-1.0")
Tip.TIP_GAP            -- 2 (also Tip.GAP); a file-local is read by the placers, so writing it moves nothing (as W.FOOTER)

-- Own for a placement: SetOwner(owner, "ANCHOR_NONE"). opts.owner = UIParent for a restricted tree (AuraMaster).
Tip.Own(tip, element, opts) -> tip

-- Body rule. group: frame | {frame,...} | {main=frame, panels={...}} | function()->frames | nil
--   nil -> Tip.GroupOf(element): nearest ancestor with a registered group, else the outermost ancestor under UIParent.
-- opts: { prefer="right"|"left", host=<group member the element is in>, comparisons=true, rect=fn(frame)->l,b,w,h }
-- returns "right" | "left" | "below" | "above" | nil (geometry unreadable: nothing placed, caller keeps its anchor)
Tip.PlaceBeside(tip, element, group, opts)

-- Chrome rule. zone: "top" (default; also modal) | "bottom". Returns "below" | "above" | nil.
Tip.PlaceAttached(tip, element, zone, opts)

-- Launcher rule (halves/thirds). Returns the point string, or nil.
Tip.PlaceLauncher(tip, button, opts)

-- Registration, so library widgets find the right group with no host plumbing:
Tip.SetGroup(window, { companions... })   -- or a function, re-read on each hover so a hidden panel drops out
Tip.GroupOf(element) -> frames

-- Pure solvers (exported with a leading __ for the suite and for host tests; the standard asks for headless cases):
Tip.__solveBeside(groupRectsPx, elemTopPx, tipWpx, tipHpx, screenWpx, screenHpx, gapPx, prefer) -> side, x, y
Tip.__solveAttached(elemRectPx, tipWpx, tipHpx, screenWpx, screenHpx, gapPx, zone) -> side, x, y
Tip.__solveLauncher(btnRectPx, screenWpx, screenHpx, gapPx) -> point, relPoint, dx, dy
```

Mechanics, which are the decisions to make:

- **Apply in absolute UIParent coordinates**: `tip:ClearAllPoints(); tip:SetPoint(pt, UIParent, "BOTTOMLEFT",
  x/ts, y/ts)`, where `ts` is the tooltip's effective scale.
  - This is restricted-tree safe: AuraMaster's strips refuse any anchor to them.
  - It makes the clamp exact, since we compute it.
  - It gives one code path for HUD and window.
  - The cost: the tooltip does not follow a window dragged while the tooltip shows. The pointer leaves on drag anyway,
    so this is acceptable.
  - The launcher placer is the exception and uses a **relative** anchor (point on the button, `0,±2`), because
    LibDBIcon's buttons are not restricted and a relative anchor needs no size.
- **Side choice** compares `groupRight + gap + tipW <= screenW` (px). The left side needs `groupLeft - gap - tipW >= 0`.
  If neither fits, use the body fallback, `__solveAttached(element, …, "top")`, below with a flip above.
- **Companion preference**: when the element's host member is not the group's `main`, prefer the side the member lies
  on relative to main's center (DW RollsPanel's "away from the window"). The default prefer is right.
- **Vertical clamp**: `y = clamp(elemTop, tipH, screenH)`, sliding only as far as needed.
  **Horizontal clamp** for attached: center on the element, then clamp into `[0, screenW - tipW]`.
- **Comparisons**: after the side is picked, call `tip:SetAnchorType("ANCHOR_RIGHT"|"ANCHOR_LEFT", 0, 0)` when
  `tip.SetAnchorType` exists and `opts.comparisons ~= false`. **Risk:** confirm against wow-ui-source that
  SetAnchorType after SetPoint does not re-anchor to the owner. The standard cites `ContainerFrame.lua:1448-1458` for
  this order. Make it a smoke line with an item tooltip plus shift-compare.
- **Geometry reads** are guarded: `type(v)=="number"`, never secret arithmetic (the AuraMaster `NS.Secrets` case).
  `opts.rect` lets a host supply guarded reads. Unreadable geometry answers `nil`, and the caller's fallback is the
  **attached placer, then a plain `SetOwner(element,"ANCHOR_TOP")`-shaped attach. Never the cursor.**
- **Late resize** (item data arriving after Show grows the tooltip): GameTooltipTemplate is clamped to screen
  client-side, which is the backstop. Optionally offer `Tip.Replace(tip)` to re-run the last placement (store the args
  on `tip.__ka0sTip`) so a host can call it from `OnTooltipSetItem`/`TooltipDataProcessor`. This is a Q below; I
  recommend shipping it, since it is tiny.
- **Effective scale**: every rect is `GetLeft()*GetEffectiveScale()` etc., and the screen is
  `UIParent:GetWidth()*UIParent:GetEffectiveScale()`. LibDBIcon's `getAnchors` mixes the button's own-scale
  `GetCenter` with UIParent units (`LibDBIcon-1.0.lua:52-54`). Ours fixes that.

### 4.3 Library moves (same release, required by `standalone-windows.md:169`)

| File | Change | Minor |
|---|---|---|
| `Tooltip.lua` (new) | the surface | `LibKa0s-Tooltip-1.0` **1** |
| `IconBrowser.lua` | cell is `Own`, fill, Show, then `PlaceBeside(tip, cell, browserWindow)`. Toolbar tips go through `AttachTooltip(..., {zone="top"})` (needs #4.5) or a local attached helper. Register `Tip.SetGroup(window)` in IconBrowserWindow. | IconBrowser 1→**2** (and IconBrowserWindow if touched) |
| `WidgetsDropdown.lua` | `__rowTip`: string tips are `Own`, then Show, then `PlaceBeside(GameTooltip, row, menuFrame)`. A function renderer is called and then, **if `GameTooltip:IsShown()` and owned by `row`**, placed (additive: the host renderer keeps drawing lines and the library re-places). | WidgetsDropdown 1→**2** |
| `WidgetsReorder.lua` | handle tip goes beside `Tip.GroupOf(handle)` (the host window; on a Settings page this resolves to the Settings frame, which is out of scope but harmless). Option: skip placement when the list is under `SettingsPanel`, keeping `ANCHOR_RIGHT` there. | WidgetsReorder 6→**7** |
| `SimPanel.lua` | `showTip(owner,row,pal)` is `Own`, fill, Show, then `PlaceBeside(tip, owner, panelGroup)`. The panel frame registers itself. If it docks to a host window (DockTestStrip-style), the group includes it. | SimPanel 10→**11** |
| `WidgetsDragHandle.lua` | the default becomes `PlaceAttached(tip, strip, "top", {owner=UIParent})`, owned by UIParent at ANCHOR_NONE (restricted-safe, which is the shape minor 4 already uses). `tooltipOwner="cursor"` and `ANCHOR_*` values are **accepted but ignored** (frozen -1.0 is additive-only, so the fields stay readable and documented as retired). A host `tooltipPlace` still wins, and its failure falls back to the attached placer, **not** `ANCHOR_CURSOR` (`:526`). A mark (help/close) places by its strip (AuraMaster `StripOf` precedent). | WidgetsDragHandle 13→**14** |
| `Charts.lua` / `ChartsRender.lua` | `Ctx:showTip(owner, tip, placement)`: the default placement is beside `host.group` (new optional host field: frame/frames/function), else `Tip.GroupOf(ctx.content)`. `plainTip` does `Own`, fill, Show, then place. A host `tip` seam is still called with `(owner, lines, anchor)`, where `anchor` is now a **placement table** `{kind="beside", group=…}`. **Contract change for the 3 hosts that override `tip`** (DpsRace/CombatTrail `cursorTip`, LootHistory `showTip`): a host that calls `SetOwner(owner, anchor)` with a table would error. Safer additive path: keep passing the legacy string (`"ANCHOR_NONE"`) as arg 3 and add `ctx:PlaceTip(owner)` as arg 4 or a ctx method the host calls after Show. **Recommend the ctx method**: `host.tip(owner, lines, "ANCHOR_NONE", ctx)` and `ctx:PlaceTip(tip, owner)`. Drop `"ANCHOR_TOP"` at `ChartsRender.lua:121`. | Charts 1→**2**, ChartsRender 1→**2** |
| `Launcher.lua` | §4.6 | Launcher 10→**11** |
| `Widgets.lua` (optional) | Footer marks `spec.tooltip` placed `PlaceAttached(…, "bottom")`, TestStrip none. | Widgets 27→28 (only if taken; it collides with other #75+ items, so coordinate) |
| `OptionsWidgets.lua` (optional, see 4.5) | `O.AttachTooltip(widget, label, tip, opts)` with `opts.zone`/`opts.group`; default unchanged (Settings). | OptionsWidgets minor +1 → Options key moves |

`NEEDS_*`: each consumer guards `LibStub("LibKa0s-Tooltip-1.0", true)`. If the major is absent (it cannot be in one
payload, but an older winner copy could be), keep today's anchor so nothing breaks. `tests/test_versioning.lua` and the
CHANGELOG version block gain the new major.

### 4.4 Ordering inside a hover (why "after Show")

`GameTooltip:GetWidth()` is only valid after lines are added and `:Show()` runs. Every placer therefore requires a
shown tooltip. The DragHandle already does exactly this (`dhShowPlaced`, `:521-528`). Re-placing after Show is one
extra `SetPoint` on the same frame in the same frame tick, so there is no visible jump.

### 4.5 O.AttachTooltip in standalone windows

It is out of scope on Settings pages, but `IconBrowser` (via `spec.helpers`) and DropWatcher (17 window files;
`git grep AttachTooltip`) call Options helpers inside standalone windows, where `ANCHOR_RIGHT` on a toolbar control is
#119. Options: (a) an additive `opts` 4th arg (`zone`/`group`), default unchanged. (b) IconBrowser wraps its own
attached helper and leaves Options alone. Recommend **(a)** because addons need it at adoption too. It moves the
Options key, though, so if another #75+ item is already moving Options, piggyback on it. Otherwise take (b) now and (a)
later.

### 4.6 LibDBIcon (vendored, not ours)

Do **not** patch LibDBIcon (third-party, MINOR 52, vendored per addon; a fork would lose to any other addon's newer
copy via LibStub anyway). Flow (`LibDBIcon-1.0.lua:59-75`): LibDBIcon does `SetOwner(btn,"ANCHOR_NONE")`, then
`SetPoint(getAnchors)`, then **calls our `OnTooltipShow(lib.tooltip)`**, then `Show()`. So `Launcher.lua`'s
`drawTooltip(tt)` (`:403`) re-places at its end:

```lua
local icons = LibStub("LibDBIcon-1.0", true)
local btn = tt.GetOwner and tt:GetOwner()
if icons and tt == icons.tooltip and btn and btn == icons:GetMinimapButton(name) then
  Tip.PlaceLauncher(tt, btn)          -- ClearAllPoints + relative point, 0,±TIP_GAP; needs no size
end
```

The guards matter for three reasons:

- **Broker displays** (Titan, ChocolateBar) call the same `OnTooltipShow` with their own tooltip and must keep their
  anchor (`standalone-windows.md:128`).
- The **addon compartment** path (`onEnterCompartment`, `:97-105`) uses `lib.tooltip` with the compartment button as
  owner. It is a client menu, so it is out of scope, and the `GetMinimapButton` identity check excludes it.
- `GetMinimapButton` exists in LibDBIcon (public API). Verify it is in MINOR 52 at implementation, and fall back to
  `btn.dataObject == object`.

The rule is "no host re-anchors", and the library is not a host, so this is exactly what launcher-§7 anticipates. Test
it by faking `LibStub("LibDBIcon-1.0")` with a `tooltip` and a button, driving `drawTooltip`, and asserting the
recorded point per screen ninth.

## 5. Test plan (headless, LibKa0s suite)

New `tests/test_tooltip_place.lua` (+ `tests/fixture_screen.lua`):

- **Fake screen**: a UIParent stub with `GetWidth/GetHeight/GetEffectiveScale`. Frames use the `fixture_geom.lua`
  `geomFrame` extended with `GetLeft/GetRight/GetTop/GetBottom/GetCenter/GetEffectiveScale/GetParent`. The tooltip
  stub records `ClearAllPoints`/`SetPoint(pt, rel, relPt, x, y)`/`SetAnchorType`/`SetOwner`, with width and height set
  by the case.
- **Pure solver tables**:
  - Beside: right fits; right does not fit and left fits; neither fits (the fallback below; at the screen bottom it
    flips above); bottom clamp (tooltip taller than the space under the element top); top clamp.
  - Companion: docked right of main, so its tips go right; right does not fit, so they go left beyond main; main's
    own tips with a right companion are measured from the companion's right edge.
  - Scale: a window at 0.8 and a tooltip at 1.0.
  - Gap = exactly 2 px in screen px divided by the tooltip scale.
- **Attached solver**: top zone below; flip above at the screen bottom; bottom zone above; flip below at the top; x
  clamp at both screen edges; centering.
- **Launcher solver**: the 3×2 grid (TOPRIGHT/BOTTOMRIGHT, TOP/BOTTOM, TOPLEFT/BOTTOMLEFT) with ±2; the button scale
  differs from UIParent's (Minimap scale).
- **Apply**: points recorded against UIParent BOTTOMLEFT; `SetAnchorType` side; unreadable geometry answers nil with
  nothing recorded; secret-like values (a non-number) answer nil.
- **Per-widget characterization**, red before, green after:
  - `test_icon_browser` (cell beside, toolbar below)
  - `test_widgets` dropdown (`__rowTip` string and function renderer, beside the menu)
  - `test_widgets_reorderlist` handle
  - SimPanel `showTip` button and row
  - `fixture_draghandle` (default attached below; `tooltipOwner="cursor"` no longer yields ANCHOR_CURSOR; a failing
    `tooltipPlace` falls back to attached)
  - `fixture_charts` (plainTip beside; the host seam gets a ctx with `PlaceTip`)
  - launcher (drawTooltip re-places only for the LibDBIcon button)
- **Grep guard test** (prose/inventory style): no `ANCHOR_CURSOR`, `ANCHOR_CURSOR_RIGHT`, `ANCHOR_RIGHT` or
  `ANCHOR_TOP` in `LibKa0s/*.lua` outside `Options*.lua` (Settings, OOS) and outside comment lines. This pins #119 in
  the library.
- **Kit**: add `tests/_kit/mock_screen.lua` (fake screen and tooltip recorder) so addons can write the standard's
  SHOULD cases at adoption. It is a **kit revision bump (56→57)**, so check the pairing rule with other #75+ items that
  also move the kit.
- Gates: `lua tests/run.lua`, `ka0s-bounded luacheck .`, 1500-line cap (the new file stays well under 400),
  CCN ≤ 15 (split the solvers per side).

## 6. Ripple

- LibKa0s: `docs/api/Tooltip/version-1-docs.md` + `members-1.json`; new docs for each moved module minor
  (`docs/api/Widgets/version-<key>-docs.md`, Charts, IconBrowser, Launcher); `docs/api/CONSUMERS.md` row (zero
  consumers until adoption; it is additive and cites #92); CHANGELOG version block; `CLAUDE.md` band census (new file);
  `docs/test-cases.md` regenerated; `docs/releasing.md` re-vendor note ("contract change: DragHandle default placement,
  Charts host seam arg 3/4, Dropdown function renderer now re-placed; adoption blockers per the revendor skill").
- WowAddonStandards (next release after the tag, patch or minor): replace "future surface / no tag ships it" with the
  major, file and minor in `standalone-windows.md:160-169`, `launcher.md:165`, `library-stack.md:127`,
  `anti-patterns.md:148` (the LibDBIcon 0 px exception now ends at the re-vendor), `NEW_ADDON_CONTEXT.md` 24c and the
  DoD line, `EXECUTIVE_SUMMARY.md`, and `AUDIT.md`'s check. "Adoption is blocked" flips to required-at-re-vendor
  (parallel host placer = #47).
- Re-vendor (all roster addons + CombatTrail): this is a no-op for addon code. The library's own windows, menus, charts
  and launcher move automatically. **Visible behavior changes at re-vendor, which are smoke lines:**
  - HUD strip tooltips in AT/AM/CM/KC: unchanged while their host `tooltipPlace` hook is set (it still wins), so they
    remain beside the strip until adoption.
  - Charts in DR/CT/LH: unchanged, because they override `tip`.
  - Charts in DW: moves beside its window.
  - Library dropdown entries everywhere: move beside the menu.
  - The minimap tooltip gains 2 px.
  - The icon browser and sim panel in every host.
- Adoption (deferred per owner): remove host placers (DW RowTooltip/RollsPanel.PlaceTip, AM Anchors_Tooltip,
  AT/KC/CM PlaceTooltipBeside), replace `cursorTip` (DR/CT), and move 160-odd `ANCHOR_*` addon sites. Counts of
  non-lib, non-test `ANCHOR_*` lines: AT 2, AM 11 (3 cursor), BL 12, CM 6, DR 12, DW 9, KC 13, ST 0, LH 22 (3 cursor),
  MM 30, OR 12, PM 0, PFE 2, PGFE 2, PC 1, QC 8, SkillMaster 8 (`main`), WG 1, CombatTrail 21 (`main`).

## 7. Risks

1. **SetAnchorType semantics**: it might re-anchor relative to the owner and undo the absolute point. Verify in
   wow-ui-source, plus a smoke line (shift-compare an item in the DW window near the right edge).
2. **Restricted trees**: `GetLeft` on frames under `DisableUntrustedLayoutScriptsTemplate` or secret rects (AuraMaster
   attached containers) may read secret. Mitigations: guarded number reads, the `opts.rect` hook, and the host's
   `tooltipPlace` still wins.
3. **Late tooltip growth** (item data): side picked on the old width; the client's clamp may slide it over the group.
   Mitigation: `Tip.Replace` (Q4) and the smoke check.
4. **Frozen -1.0 contracts**: DragHandle `tooltipOwner/tooltipAnchor` and Charts `anchor` lose their effect. That is
   documented as retired, not removed. The revendor skill reports these as "contract changes under unchanged
   signatures", so they are adoption blockers to be listed.
5. **Key collisions** with other #75+ items moving Widgets, Options or the kit in the same run. One release
   (v1.105.0?) has to carry one coherent version block.
6. **Group default** (outermost ancestor under UIParent) is wrong for frames parented to UIParent but docked beside
   another window (companions). `Tip.SetGroup` registration on those windows is needed, and the library's own sim
   panel and icon browser have no docked companions today.
7. **CommonTasks CLAUDE.md drift**: SkillMaster and CombatTrail default to `main`. Plans must detect the branch per
   repo.

## 8. Open questions for the owner (recommended answers in **bold**)

1. Host the surface as a new major `LibKa0s-Tooltip-1.0` (minor 1, `Tooltip.lua`, no dependencies)? **Yes, new
   major.** The alternatives are a Widgets module or Core.
2. Apply placements as absolute UIParent points (restricted-safe, exact clamp; the tooltip does not follow a moving
   window), with only the launcher relative? **Yes.**
3. HUD drag strips (AT/AM/CM/KC) are top chrome under v2.112.0's flagged reading, so their tooltips go attached and
   centered below the strip, over the HUD. Today all four place beside the strip. Confirm the reading, or rule strips
   as body (beside the whole display)? **Confirm chrome**: it is the standard's text. Note that beside-the-strip is
   then #119 at adoption.
4. Ship `Tip.Replace(tip)` for re-placing after late growth (item data)? **Yes, it is small.**
5. DragHandle `tooltipOwner="cursor"`, `tooltipAnchor` and a failing `tooltipPlace` all become the attached placer
   (never the cursor), with the fields kept but retired? **Yes.**
6. Charts host seam: keep `host.tip(owner, lines, anchorString)` and add a 4th arg `ctx` with `ctx:PlaceTip(tip,
   owner)`, plus an optional `host.group`, rather than changing arg 3's type? **Yes, additive.**
7. `O.AttachTooltip`/`TabStrip`: add an additive `opts` (`zone`, `group`) now so IconBrowser's toolbar and addon
   windows can use it, or keep Options untouched this run? **Add it now if Options already moves in this run;
   otherwise give IconBrowser a local wrapper.**
8. Debug console has no tooltips at v1.104.0. Treat "debug console moves" as N/A (no new tips added)? **N/A, recorded
   with the grep as evidence.**
9. Add `spec.tooltip` to Footer marks (library-placed above)? **Defer to adoption**, unless Widgets' minor already
   moves in this run.
10. Add a kit `mock_screen.lua` (kit rev +1) for addons' SHOULD cases? **Yes, in the same tag.**
