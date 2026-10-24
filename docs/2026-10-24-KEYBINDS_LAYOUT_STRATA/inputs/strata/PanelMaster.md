# PanelMaster — frame strata analysis

Item 030. Analysed read-only at `../PanelMaster` (branch `master` at `e0a9ee3`, v1.3.0). PanelMaster
differs from the rest of the collection: its main visuals are **user-layered backdrops**. Both the strata
and the level of every panel are player settings (`strata`, `level` on the record; `settings.defaultStrata`
for new panels), so this addon's job is not to pick one strata. Its job is to keep (a) each panel's
**internal** stack coherent, (b) panels **separable** from each other, and (c) its own chrome (unlock
overlay, popups, console) usable whatever strata the player picks.

## Inventory

| element | file:line | parent | strata | frame level | toplevel / clamped | notes |
|---|---|---|---|---|---|---|
| Panel frame `PanelMaster_Panel_<slug>` | `modules/Canvas.lua:240` (create), `:566` (strata), `:571` (level) | UIParent | **explicit**, per record (`spec.strata`, default `LOW`, `C.PANEL_TEMPLATE`, `core/Constants.lua:289`). Inherits UIParent's strata between creation and the first `applySpec` | **explicit** `level * C.PANEL_LEVEL_STRIDE` (stride 8, `core/Constants.lua:259`); level 0–100 → 0–800 | not toplevel / `SetClampedToScreen(false)` (`:241`, intentional) | Pooled by global name. Mouse off while locked (`:242`), so a locked panel never takes clicks at any strata; the mouseover fade uses `MouseIsOver`, not mouse input. |
| Background fill frame `f.bgFrame` | `Canvas.lua:249` | panel | inherited | **explicit** base+2 (`C.BG_FRAME_LEVEL`, `Canvas.lua:594`) | — | Texture `f.bg` in `BACKGROUND` (`:253`). |
| Border frame `f.borderFrame` (BackdropTemplate) | `Canvas.lua:262` | panel | inherited | **explicit** base+4 (`C.BORDER_FRAME_LEVEL`, `:595`) | — | Backdrop edgeFile. |
| Accent container `f.accentFrame` | `Canvas.lua:277` | panel | inherited | **explicit** base+5 (`C.ACCENT_FRAME_LEVEL`, `:596`) | — | Holds no regions of its own. |
| Accent bar ×4 `f.accents[edge]` | `Canvas.lua:285` | accentFrame | inherited | **implicit**: the client default for a child, so ≥ accentFrame+1 = **base+6**. Never set | — | Fill texture `ARTWORK` (`:287`). Anchored **outside** the panel's bounds at `accentOffset ≥ 0` (`:390-410`, default 0 = flush outside); a negative offset pulls it over the panel. |
| Accent bar border `bar.borderFrame` (lazy, BackdropTemplate) | `Canvas.lua:342` | accent bar | inherited | **implicit**: ≥ bar+1 = **base+7**. Never set | — | Built when `accentBorderSize > 0` (`:350`). The shipped default **is** 1 (`Constants.lua:364`), so it is built on every panel with an accent bar. The comments at `Constants.lua:357` and `Canvas.lua:337` still say "size 0 by default" (stale). |
| Artwork frame `f.artFrame` | `Canvas.lua:296` | panel | inherited | **explicit**, per render: base + `C.ART_FRAME_LEVEL[layer]` = +1 / +3 / **+6** (`Canvas.lua:496-497`, `Constants.lua:232`) | — | `SetClipsChildren(true)` (`:307`), so art never leaves the panel's bounds. Textures `ARTWORK` (`:318`, `:330`), N per composed bar. |
| Unlock overlay `f.overlay.frame` (lazy) | `modules/Unlock.lua:77` | panel | inherited | **explicit** base+7 (`C.UNLOCK_FRAME_LEVEL`, `Unlock.lua:174`), re-asserted on every `Decorate`, which Canvas calls after every render | — | Four `OVERLAY` edge textures and a name FontString in `OVERLAY`. Mouse off; the **panel** takes the drag (`Unlock.lua:216-223`). |
| Drag (StartMoving) | `Unlock.lua:223` | — | — | — | panel not toplevel, so no raise on click | The panel keeps its strata and level while dragged. An unlock asked for in combat is queued until combat ends (`Unlock.lua:146-151`). |
| Mouseover driver | `Canvas.lua:656` | none | — | — | — | Non-visual OnUpdate ticker. Listed for completeness. |
| Debug console `PanelMasterDebugWindow` (LibKa0s-DebugLog) | lib `libs/LibKa0s/DebugLog.lua:536-539` | UIParent | **explicit `DIALOG`** (library) | default, plus the library's internal +1s (`DebugLog.lua:337`) | movable, **clamped** | Opened from Master controls ▸ Debug console. The addon does not pick its strata. |
| Confirm popups ×4 `KA0S_PANELMASTER_RESETALL / DELETEALL / DELETE / RESET` | `settings/Slash.lua:83,91,108,116`; shown from `Slash.lua:70,223`, `Panel.lua:436`, `PanelEditor.lua:161` | Blizzard StaticPopup | Blizzard `DIALOG` | Blizzard | Blizzard | `preferredIndex = 3`. Shared Blizzard frames: the addon must not restyle their strata. |
| Settings canvases (General / Panels / Profiles / landing) | `settings/Panel.lua:352,421,472`; lib `O.CreatePanel` | Blizzard SettingsPanel | inherited from SettingsPanel (Blizzard; believed `HIGH`, confirm with `/fstack`) | inherited | — | Host-drawn content on AceGUI. Library chrome inside it (tab strip `OptionsTabs.lua:375,712`, combat cover `Options.lua:589-590`) sets relative levels only. |
| Landing logo texture | lib `O.BuildLandingPage` via `Panel.lua:276` | AceGUI SimpleGroup | inherited | inherited | — | — |
| Panels band block (picker and create box) | `settings/PanelEditor.lua:512-524` | the chrome header frame (lib) | inherited | inherited | — | Parented by hand. |
| AceGUI dropdown pullouts, LSM30 media dropdowns | AceGUI / AGSMW (`Panel.lua:100-135` tracks them) | UIParent (AceGUI) | library (`FULLSCREEN_DIALOG` / `TOOLTIP` per widget lib) | library | clamped by lib | Closed on scroll by this addon (`Panel.lua:118-135`). |
| Colour picker | Blizzard `ColorPickerFrame` via AceGUI ColorPicker | Blizzard | Blizzard (`DIALOG` or higher; confirm with `/fstack`) | Blizzard | — | — |
| Tooltips | `O.AttachTooltip` → GameTooltip | UIParent | `TOOLTIP` | Blizzard | — | Owned by the library. |
| Minimap launcher button | LibDBIcon via `core/LauncherSetup.lua` | Minimap | library (`MEDIUM`) | library | — | The addon picks nothing. |

Explicit strata calls in addon code: **one** (`Canvas.lua:566`, user-driven). Explicit level calls:
**six** (`Canvas.lua:497,571,594,595,596`, `Unlock.lua:174`). Hardcoded strata literals: none (the
debug console's `DIALOG` is the library's). No `SetToplevel`, no `SetFixedFrameStrata/Level`. Verified
with a grep of `CreateFrame|SetFrameStrata|SetFrameLevel|SetToplevel` over `core/ modules/ settings/`.

## Problems

| id | where | problem |
|---|---|---|
| PAN-S01 | `Canvas.lua:285-289`; ladder comment `Canvas.lua:573-580`, `Constants.lua:232-241` | **The accent bars are not on the ladder.** The ladder says "+5 accent bars", but +5 is the *container*. The bars are its children and get no explicit level, so they sit at ≥ **base+6**. That is the same rung as **ABOVE_ALL artwork** (+6). The "Above border and accent" draw-layer choice therefore has **no guaranteed order** against the bars. The art frame is clipped to the panel and the bars hang outside it at `accentOffset ≥ 0`, so the tie only shows where a **negative** `accentOffset` pulls a bar over the panel. There the logo can draw under the bar it is supposed to cover, and the order depends on creation sequence, which the name-keyed pool scrambles. |
| PAN-S02 | `Canvas.lua:342` vs `Unlock.lua:174`, `Constants.lua:241` | **The accent bar's border is level with the unlock overlay** (≥ base+7 against base+7). The overlay is documented as "the top of the stack by definition" (`Constants.lua:237-241`), but a bar border overlapping the panel edge (negative offsets) can cover the gold outline or the name label. It is also the **ceiling of the stride**: an implicit level that drifted to +8 would collide with the **next panel level's** base+0. The shipped `accentBorderSize = 1` means this border exists on every accent bar, not only on customised ones. |
| PAN-S03 | `Canvas.lua:571`; tooltip `PanelEditorTabs.lua:425-427`; docs `settings-panel.md` | **Two panels on the same strata and level interleave rung by rung.** They do not merely draw "in no guaranteed order". Both get the same base, so panel A's border (+4) can sit over panel B's fill (+2) while B's ABOVE_ALL art (+6) sits over A's border. The result is a mix of the two stacks, not one panel in front of the other. The tooltip understates this. The stride fixes *different* levels and does nothing for equal ones, and equal is the default: every panel starts at level 0 (`Constants.lua:290`). |
| PAN-S04 | `Unlock.lua:77`, `:216-223`; `Canvas.lua:566` | **The unlock overlay and drag target inherit the panel's strata.** A panel at `BACKGROUND`/`LOW` (the default `LOW`) under a mouse-enabled `MEDIUM` frame (action bars, unit frames, other addons' windows) shows its gold outline *under* that frame and **cannot be grabbed** where they overlap. Unlock mode is meant to make every panel findable (`Constants.lua:237`), and for low-strata panels under busy UI it does not. |
| PAN-S05 | `C.STRATA` `Constants.lua:15-18`; `Canvas.lua:566`; `Slash.lua:83-122`; lib `DebugLog.lua:536` | **A panel can sit above the addon's own popups, console and settings.** The player may choose `DIALOG`, `FULLSCREEN`, `FULLSCREEN_DIALOG` or `TOOLTIP`. At `FULLSCREEN` and above, a panel draws **over** the four confirm popups and the debug console (`DIALOG`), and over the Settings window where the player is editing it. At `TOOLTIP` it can also cover dropdown pullouts and tooltips. At `DIALOG` it ties with the popups and their order is undefined. While **locked** this is visual only: the panel is mouse-transparent. While **unlocked** the panel is mouse-enabled, so it also **swallows the clicks** meant for the *Delete* / *Reset* popup, the console, or the Settings window's own *Lock frame* checkbox under it. `/pm lock` is the only escape. |
| PAN-S06 | `Canvas.lua:240` vs `:566` | A new (non-pooled) frame exists at UIParent's inherited strata and default level until its first `applySpec`. `Canvas:Render` runs `applySpec` in the same Lua call, and the client renders only between frames, so nothing can be **seen** in that window. This is hygiene (strata stated at creation), not a visible defect. |
| PAN-S07 | `Canvas.lua:249`, `:262`, `:277`, `:296` | Every child's level is set **after** creation, in `applySpec`, from `GetFrameLevel()`. So the ladder only holds while every repaint goes through `applySpec`. `Unlock.lua:174` re-asserts its own rung for the same reason. That is consistent, but the accent bars and bar borders (S01/S02) are the parts no code re-asserts. |
| PAN-S08 | `Constants.lua:259`, `MAX_PANEL_LEVEL 100` | The stride is derived from `UNLOCK_FRAME_LEVEL + 1` and ignores the implicit +6/+7 rungs (S01/S02). Any fix that adds explicit rungs has to grow the stride with them. The ceiling, 100 × stride, stays far below the client's per-strata level limit (10 000) even at stride 10–12; `tests/test_constants.lua:112-121` already pins the ceiling against the constants. |
| PAN-S09 | `PanelEditorTabs.lua:416-418`, `Schema.lua:122-126` | Strata is chosen ad hoc per panel with no guidance on the collection's tiers. The tooltip does not say that `MEDIUM` is where most HUD lives, or that `DIALOG`+ covers popups. This is a guidance gap, not a code defect. |
| PAN-S10 | `Constants.lua:357`, `Canvas.lua:337` vs `Constants.lua:364` | Comment drift: two comments say the accent bar border "ships at size 0"; it ships at 1. It matters here because S02's reach depends on it. |

## Proposed strata map

The intended layering, tier by tier.

| tier | strata | level band | elements |
|---|---|---|---|
| T0 — backdrop panels (player-chosen) | `BACKGROUND` / `LOW` recommended; `MEDIUM`/`HIGH` allowed; `DIALOG`+ allowed with a warning | `level × STRIDE` + an internal ladder. Proposed **stride 10**: +1 art BELOW_BG · +2 bg fill · +3 art ABOVE_BG · +4 border · +5 accent container · **+6 accent bars (explicit)** · **+7 accent bar borders (explicit)** · **+8 art ABOVE_ALL** · **+9 unlock overlay** | panel and all its children; children never set a strata of their own (except the T1 overlay, below) |
| T0′ — same-level tie-break (optional, Z03) | same as panel | two panels sharing strata and level get distinct bases, base = `(level × TIE_K + rank) × STRIDE`, rank by panel id among same strata+level, TIE_K = 8 → ceiling (100 × 8 + 7) × 10 = 8 070 < 10 000 | makes "same level" mean "stacked in id order, never interleaved" |
| T1 — editing affordance (unlocked only) | **max(panel strata, `HIGH`)** for the overlay frame (Z04); the panel itself keeps its own strata | panel base +9 within the panel's strata; own strata when lifted | unlock outline and name label; the drag target is the panel itself |
| T2 — addon chrome (library/Blizzard) | `DIALOG` | library / Blizzard | debug console, four StaticPopups, colour picker |
| T3 — transient UI | `FULLSCREEN_DIALOG` / `TOOLTIP` | library | AceGUI pullouts, LSM dropdowns, GameTooltip |
| outside | Blizzard SettingsPanel (believed `HIGH`) | inherited | settings canvases and their AceGUI content |

The rule to state: **a T0 panel may be raised by the player into T2/T3, and the addon warns about it
but does not forbid it**, because a high-strata backdrop is a legitimate choice. While unlocked, such a
panel must never stop the player from answering the addon's own popups.

## Proposed changes

| id | change (file:line, from → to) | reason | confidence |
|---|---|---|---|
| PAN-Z01 | `Constants.lua:232-241,259`: ladder `ART ABOVE_ALL 6 → 8`, `UNLOCK_FRAME_LEVEL 7 → 9`, add `C.ACCENT_BAR_LEVEL = 6`, `C.ACCENT_BAR_BORDER_LEVEL = 7`; stride `8 → 10` (still derived as `UNLOCK + 1`). Update the ladder comments at `Canvas.lua:573-580` and `Constants.lua:225-259` (incl. "highest frame level ... 800" → 1 000), and the stale size-0 comments (S10). Tests that already read the constants (`test_artwork.lua:382-385`, `test_unlock.lua:200-221`, `test_canvas.lua:328-343`, `test_constants.lua:121`) follow; add `ABOVE_ALL > ACCENT_BAR_BORDER_LEVEL`. | Gives the bars and their borders rungs of their own, so ABOVE_ALL art is really above the accent and the overlay is really on top (S01, S02, S08). The stored `artLayer` is a token, not a number (`C.ART_FRAME_LEVEL[layer]`), so no saved value moves. Max level becomes 1 000, which is safe. | 80% (that the bars sit at ≥ +6 is how the client defaults child levels; confirm with `/fstack` on a panel with ABOVE_ALL art and a negative accent offset) |
| PAN-Z02 | `Canvas.lua:596` (applySpec): after the accent container, set each bar explicitly, `bar:SetFrameLevel(base + C.ACCENT_BAR_LEVEL)`, and, when present, `bar.borderFrame:SetFrameLevel(base + C.ACCENT_BAR_BORDER_LEVEL)`. `applyAccents` runs after these lines and `ensureAccentBorder` (`Canvas.lua:340-345`) can build a border mid-render, so set the border's level inside `applyAccentBorder` after `ensureAccentBorder` (or move the level block after `applyAccents`). | Turns the implicit rungs into explicit ones. Every element of the stack is then stated once and re-asserted on every repaint, the same pattern the overlay already follows (S01, S02, S07). | 85% |
| PAN-Z03 | `Canvas.lua:571`: base = `level × STRIDE` → `(level × TIE_K + tieRank) × STRIDE`, where `tieRank` is the panel's stable rank among panels with the same strata **and** level (by id, which is allocated monotonically per profile, `Registry.lua:463-464`), clamped to 0..TIE_K-1 with TIE_K = 8. Update the tooltip at `PanelEditorTabs.lua:425-427` to "panels on the same strata and level stack in the order they were created". | Equal levels then stack panels whole instead of interleaving their layers (S03). The stored setting does not change, only the base derived from it. Costs: the renderer must see every panel to rank one (cross-panel coupling in a per-panel path), a delete or a level change re-ranks the others, and the ninth same-level panel shares rank 7 and interleaves again. | 45% (the owner may prefer to keep the documented "no guarantee" and take Z03b) |
| PAN-Z03b | (alternative to Z03, wording only) `PanelEditorTabs.lua:425-427` and `docs/settings-panel.md`: "Panels on the same strata and level can **interleave**: parts of one may show through the other. Give overlapping panels different levels." | Tells the truth about S03 at no code cost. | 90% |
| PAN-Z04 | `Unlock.lua:174` (Decorate): while a panel is unlocked, lift the **overlay frame only** to its own strata, **`max(panel strata, "HIGH")`** by `C.STRATA` order, and restore it to the panel's strata in `StripOverlay` (`Unlock.lua:198-207`). `Decorate` already runs after every render, so the lift is re-applied after `applySpec`'s `SetFrameStrata` on the parent, which resets children. The panel's own strata is **unchanged**. | The gold outline and name of a `LOW` panel stay visible over action bars while editing (S04, the visibility half). A flat `"HIGH"` (as first drafted) would have **lowered** the overlay below its own panel for any panel at `DIALOG` or above, hiding the outline exactly where S05 needs it, hence the max. This does **not** fix grabbing, because the drag target is the panel. Non-secure frames, so no combat restriction applies (an in-combat unlock is queued to combat end anyway). | 60% (visibility only) |
| PAN-Z05 | `Slash.lua:83-122`: in the four `KA0S_PANELMASTER_*` dialog tables, `OnShow` sets `EnableMouse(false)` on every **unlocked** panel whose strata is ≥ `DIALOG`, and `OnHide` re-arms them through `Unlock:Decorate` (a render), not a bare `EnableMouse(true)`. | A popup must never be click-blocked by its own addon's panels (S05). The visual overlap remains, but the clicks get through. Does **not** cover the debug console or the Settings window, which S05 names too. Those keep `/pm lock` as the escape, and the Z06 tooltip warns. Changing the StaticPopup frames' own strata is rejected: they are shared Blizzard frames. | 50% |
| PAN-Z06 | Strata tooltips: **implemented as layout PAN-L20** (one `C.STRATA_TIP` string at `Schema.lua:124-125` and `PanelEditorTabs.lua:417-418`, plus `docs/settings-panel.md`): "BACKGROUND / LOW: under the HUD (recommended for backdrops). MEDIUM: level with most of the HUD. HIGH: over the HUD. DIALOG and above: over windows, **including this addon's own confirmation popups and the Settings window**." | Turns strata from an ad hoc choice into a tiered one (S05, S09). One change with layout L20, not two. Confirm the Settings window's strata in game before the wording ships. | 85% |
| PAN-Z07 | `Canvas.lua:240-242` (newFrame): `f:SetFrameStrata(C.PANEL_TEMPLATE.strata)` immediately after `CreateFrame`. | Hygiene only (S06): the frame never exists at UIParent's inherited strata, which matches the upstream "state the strata at creation" guidance. No visible effect. The draft's extra `f:Hide()` is dropped: it buys nothing, because no render happens before `applySpec`'s `SetShown`, and it adds a show/hide edge to a pooled frame. | 50% |
| PAN-Z08 | `tests/` (new case): pin that the ladder is **strictly increasing** and ends below the stride: bg < border < accent container < bars < bar border < ABOVE_ALL < overlay < STRIDE. Also pin that `applySpec` sets an explicit level on every child frame, including each accent bar and a built bar border; `tests/wow_mock.lua:178` records `SetFrameLevel`. | Keeps the explicit ladder from drifting back to implicit rungs. The mutation it dies under is deleting the bar `SetFrameLevel` in Z02. | 80% |

## Considered and rejected

| id | idea | why rejected | confidence |
|---|---|---|---|
| PAN-Z04b | Make the overlay frame the mouse target (`EnableMouse(true)` plus a drag that forwards `StartMoving` to the panel), so a low panel under busy UI can be grabbed. | Moves the drag handling out of `ArmDrag` and needs the lifted overlay (Z04) to capture clicks meant for frames above the panel, such as action buttons, while unlocked. That is a larger behaviour change than item 030 needs, and the panel can still be moved from the Position tab. | 35% |
| PAN-Z09 | Clamp the per-panel strata choice to ≤ `HIGH`. | Removes a legitimate player choice (`Constants.lua:9-14` argues for the full set), and changes a setting's value range, which is forbidden. | 10% |
| PAN-Z10 | Raise the four StaticPopups' strata above `TOOLTIP` while shown. | They are shared Blizzard frames, so a strata write leaks into every other addon's popups. | 10% |

## Notes for the upstream guidance

- **"Every child frame in a composite stack gets an explicit level, re-asserted on every repaint."**
  PanelMaster does this for five of its seven child frames, and the two it skips (accent bars and bar
  borders, nested one level deeper) are exactly where the collisions are. *Nested* children are the
  trap: a container at +N does not reserve +N+1 for its children unless the ladder says so.
- **"A parent's `SetFrameStrata` resets its children's strata."** Any child lifted into its own strata
  (an editing overlay) must be re-lifted after every parent strata write, and the lift must be
  `max(parent, target)`. It must never drop a child below its parent.
- **"Derive the per-instance stride from the ladder's top rung, and state the ladder once in
  Constants."** PanelMaster's `C.PANEL_LEVEL_STRIDE = C.UNLOCK_FRAME_LEVEL + 1` is a good pattern, but
  only if every rung, implicit ones included, is in the ladder.
- **"Equal user levels must not interleave."** An addon that lets players layer several composite frames
  has to either tie-break (stable rank) or document interleaving. "No guaranteed order" is not an
  accurate description of what happens.
- **"Editing affordances (unlock outlines, drag handles, preview strips) must be visible and reachable
  regardless of the strata of the thing being edited."** Either lift the affordance into its own strata
  or explain why it cannot be lifted. This applies to every addon with an unlock mode.
- **"An addon's own popups and console (DIALOG) must never be click-blocked by that addon's own frames."**
  Where an addon lets the player choose a strata of DIALOG or higher, it owns making its confirm dialogs
  still answerable, and it never does so by restyling shared Blizzard frames.
- **"Name the tiers."** A collection-wide table: HUD displays `LOW`/`MEDIUM`, primary windows
  `MEDIUM`/`HIGH`, editing overlays `HIGH`, addon dialogs/console `DIALOG`, pullouts and tooltips
  `FULLSCREEN_DIALOG`/`TOOLTIP`. Plus a library-owned strata tooltip string for any addon that exposes
  a strata picker.
- **"State the strata at creation."** Set a frame's strata in the same block as its `CreateFrame`, even
  if a later paint overrides it, so the frame never exists at an inherited, accidental strata.

## Review

Independent review against `../PanelMaster` at `e0a9ee3` (v1.3.0), 2026-10-24.

- **Inventory:** re-grepped every `CreateFrame` / `SetFrameStrata` / `SetFrameLevel` / `SetToplevel` in
  `core/`, `modules/`, `settings/`. The draft was complete and accurate on the addon's frames. I added:
  - that locked panels are mouse-transparent and so never block clicks;
  - that accent bars sit outside the panel at offset ≥ 0, so S01/S02 bite only with negative offsets;
  - the StaticPopup call sites;
  - the library chrome inside the Settings canvas;
  - unverified Blizzard strata (SettingsPanel, ColorPickerFrame), flagged for `/fstack`;
  - the `:307` line fix for `SetClipsChildren`.
- **New problem S10:** two comments say the accent-bar border ships at size 0. It ships at 1
  (`Constants.lua:364`), which is why S02 affects every accent bar. Folded into Z01.
- **Interaction fixes:**
  - **Z04** now lifts the overlay to `max(panel strata, HIGH)`. A flat `HIGH` would have put the outline
    under its own panel for any panel at `DIALOG` or above.
  - Z04 also notes that the parent's `SetFrameStrata` resets children, and that `Decorate` re-applies
    after each render.
  - **Z02** now sets the bar-border level after `ensureAccentBorder`, which runs later in the same
    `applySpec`.
  - **Z05** now re-arms through `Decorate` and says it does not cover the console or the Settings
    window.
  - **S05** now covers `TOOLTIP`-strata panels hiding pullouts and tooltips, and an unlocked panel
    blocking the Settings window's own *Lock frame* checkbox.
- **Recalibrated:**
  - Z03 went from 55% to 45% (cross-panel coupling, re-ranking, overflow).
  - Z05 went from 55% to 50%.
  - Z07 went from 70% to 50%, and its `f:Hide()` was dropped. The client never renders between
    `CreateFrame` and `applySpec`, so S06 is hygiene, not a visible bug.
  - The overlay-as-drag-handle variant (45%) moved to *Considered and rejected* with two more options.
- **De-duplicated:** Z06 is now marked as implemented by layout PAN-L20, so the tooltip change lands
  once.
- **Upstream note added:** a parent's strata write resets its children. Lift a child only with
  `max(parent, target)`.
