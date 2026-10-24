# MultiMeters — frame strata analysis

Item 030. Read-only analysis of `../MultiMeters` at `master` (2026-10-24), together with the vendored
`libs/LibKa0s/` it ships. A WoW frame's draw order is strata, then frame level, then draw layer (and
sublevel) for regions. A child frame with no explicit level gets its parent's level + 1. A frame with no
explicit strata inherits its parent's. "Base" below means the level a `UIParent` child receives by default.

## Inventory

| element | file:line | parent | strata | frame level | toplevel / clamped | notes |
|---|---|---|---|---|---|---|
| Window anchor `MultiMetersWindow<id>Anchor` | modules/Window.lua:561 | UIParent | inherited (MEDIUM); never set | base, implicit | no / **clamped** per `frame.clampToScreen` (:564, :751) | Invisible, childless, no mouse. Movable; the resize grip sizes it. The only frame `GetPoint` reads (`SavePosition`). |
| Window art frame `MultiMetersWindow<id>` | modules/Window.lua:569 | UIParent | **explicit, user setting** `window.frame.strata` (Window.lua:779). Values LOW/MEDIUM/HIGH/DIALOG (settings/Schema_Compose.lua:172), default MEDIUM | base, implicit; **identical for every window** | **no toplevel** / not clamped (pinned to the anchor) | Backdrop via `NS.ApplySkin`. Regions: `headerBG` BORDER (:625), `divider` ARTWORK (:614), `title` OVERLAY (:611), `notice` OVERLAY (:684). Not in UISpecialFrames (deliberate, :594-603). |
| Drag bar | modules/Window.lua:584 | art frame | inherited | +1 implicit | — | Invisible, mouse-enabled, spans the title band (height set at Window_Header.lua:431). |
| Header control buttons ×8 | modules/HeaderControls.lua:430 | art frame | inherited | **explicit `dragBar + 5`** = frame + 6 (HeaderControls.lua:473, :511) | — | `tex` and `glyph` OVERLAY (:435, :439). Raised so they win clicks over the drag bar. |
| Session line | modules/Window.lua:660 | art frame | inherited | +1 implicit | — | No mouse, on purpose (:646-656: it used to be a Button carrying the segment menu); text OVERLAY (:662). The context menu still anchors to it (Window_Header.lua:1128). |
| Column-header strip `headerFrame` | modules/Window.lua:672 | art frame | inherited | +1 implicit | — | `headerBg` BACKGROUND (:677). |
| Column-header buttons | modules/Window_Header.lua:538 | headerFrame | inherited | +2 implicit | — | `bg` BACKGROUND, label, arrow and arrowTex OVERLAY. Click to sort. |
| Body | modules/Window.lua:495 | art frame | inherited | +1 implicit | — | Wheel scroll; mouse only while a breakdown is open (:530). |
| Row frame (pooled) | modules/Row.lua:1036 | body | inherited | +2 implicit | — | `row.bg` BACKGROUND (alternating stripe, :1060). **`selfHighlight` OVERLAY (:1077)** and **`mouseHighlight` OVERLAY (:1083)**: textures on the row frame, *below* its child cells. |
| Cell StatusBar (name cell + one per stat) | modules/Row.lua:549 | row frame | inherited | +3 implicit | — | `bg` BACKGROUND (:553); fill moved to BACKGROUND sublevel 1 (:634); left/right text OVERLAY (:560, :569); flat border OVERLAY sublevel 7 (Row_Border.lua:112); LSM border = backdrop edge (BORDER); class/spec icon ARTWORK (Row_NameCell.lua:74). |
| Empty-state frame | modules/Window.lua:1350 | body | inherited | +2 implicit | — | Two OVERLAY FontStrings; built on first use. |
| Test-mode strip | modules/Window.lua:545 → libs/LibKa0s/Widgets.lua:820 | art frame | inherited | +1 implicit | — | Library `TestStrip`: fill BACKGROUND, icon ARTWORK. Placed between the title and the column headers (Window_Header.lua:803). |
| Simulation strip | modules/Window.lua:692 → Widgets.lua:820 | art frame | inherited | +1 implicit | — | Same slot as the test strip; one or the other is shown. |
| Resize grip | modules/Window.lua:716 → libs/LibKa0s/Core.lua:606 | art frame (`gripParent`) | inherited | **explicit parent + 10** (`GRIP_LEVEL`, Core.lua:546, :611) | — | Shown only while unlocked (Window_Placement.lua:135). Sizes the anchor. |
| GameTooltip (Blizzard's; addon sets owner, anchor, scale, spacing) | modules/Tooltip.lua:558-595 | — | Blizzard (TOOLTIP) | Blizzard | — | Scale reset on hide (Tooltip.lua:1039). |
| Tooltip spell-line carriers (pooled) | modules/Tooltip_Lines.lua:80 | GameTooltip | inherited (TOOLTIP) | **explicit = GameTooltip's level**, set once at creation (:83) | — | FontStrings OVERLAY (:99-145). Deliberately interleaves with the tooltip's own regions (Tooltip.lua:710-714). |
| Tooltip spell-line StatusBar | modules/Tooltip_Lines.lua:88 | carrier | inherited | **explicit = carrier level** (:90) | — | track BACKGROUND (:91); fill re-stated as BACKGROUND sublevel 1 on every draw (:639); LSM border on the bar. |
| Tooltip text ruler | modules/Tooltip_Lines.lua:173 | none | — | — | — | Hidden; measuring only. Never drawn. |
| Export modal `MultiMetersExportWindow` | modules/Export_Modal.lua:729 | UIParent | **explicit DIALOG** (:738) | base, implicit | **no toplevel** / **clamped** (:741) | In UISpecialFrames (:874). Title bar (:208), buttons (:246), whisper row and box (:766, :789) inherit. |
| Export selector menus (shared LibKa0s dropdown popup) | libs/LibKa0s/Widgets.lua:225 | UIParent | explicit FULLSCREEN_DIALOG | base | — | One instance per process. Closes on `GLOBAL_MOUSE_DOWN`; **no catcher frame since Widgets minor 5** (Widgets.lua:232-249). |
| Export copy window `MultiMetersExportCopyWindow` | modules/Export_Modal.lua:126 → Widgets.lua:650 | UIParent | explicit FULLSCREEN (:653) | base | no / clamped | Sits above the DIALOG modal on purpose. |
| Debug console `…DebugWindow` | libs/LibKa0s/DebugLog.lua:536 | UIParent | explicit DIALOG | base | no / clamped | Toggled from General > Master controls > Debug console. |
| Perf panel `…PerfPanel` | libs/LibKa0s/PerfPanel.lua:186 | UIParent | explicit DIALOG | base | no / clamped | `/mm perf`. |
| Simulation step panel | libs/LibKa0s/SimPanel.lua:211 | UIParent | explicit DIALOG | base | no / clamped | `/mm sim`. |
| StaticPopups: reset all, reset meter data, delete window | settings/General.lua:82, :136; settings/Windows.lua:338 | Blizzard StaticPopup frames | Blizzard (DIALOG) | Blizzard | Blizzard | The reset-meter-data popup is re-centered on UIParent (General.lua:180-184). |
| Header context menus (segment picker, export, etc.) | modules/Window_Header.lua:1129-1144 | Blizzard Menu | Blizzard | Blizzard | — | Built with `root:CreateButton` / `CreateTitle`. |
| Minimap button | via LibKa0s-Launcher → LibDBIcon (core/LauncherSetup.lua) | Minimap | LibDBIcon's | LibDBIcon's | — | Library's status tooltip on hover. |
| Key-binding click target `MultiMetersToggleWindows` | core/LauncherSetup.lua:152 | UIParent | — | — | — | Hidden Button that is never drawn; target of `Bindings.xml`. |
| Settings panel canvas + AceGUI widgets | settings/*.lua via LibKa0s Options | Blizzard SettingsPanel | Blizzard | AceGUI / library | — | Combat cover is level-raised by the library (Options.lua:589). The tab content panel is levelled to the body (OptionsTabs.lua:375). |
| Columns block editor: blocks and glyphs | settings/ColumnBlocks.lua:141, :146 | AceGUI container | inherited | implicit | — | Parked on hidden `blockAttic` (ColumnBlocks.lua:105, UIParent) between renders. |
| Settings-panel dropdown pullouts | libs/AceGUI-3.0/widgets/AceGUIWidget-DropDown.lua:287; libs/AceGUI-3.0-SharedMediaWidgets/prototypes.lua:212 | UIParent | AceGUI Dropdown **FULLSCREEN_DIALOG**; LSM30_* media pullouts **TOOLTIP** | AceGUI | clamped | Not the addon's. Listed because a HIGH or DIALOG meter must not cover them, and it cannot: both are above any value the strata setting allows. |
| Reorder drag ghost / insertion line | libs/LibKa0s/WidgetsReorder.lua:107, :255 | UIParent / list | ghost **TOOLTIP**; line inherited | line **explicit + 20** | — | Library-owned; the ghost takes no mouse. |

**What the addon chooses itself:** the window strata (a user setting), the header-control level
(+5 over the drag bar), the export modal's DIALOG, and the tooltip-line levels (equal to the tooltip's).
Everything else is inherited by accident of parentage or picked by the library.

## Problems

| id | file:line | problem |
|---|---|---|
| MUL-S01 | modules/Row.lua:1077, :1083 vs :549 | **Overlays drawn below the things they overlay.** *Highlight yourself* (a 3px gold left edge) and *Highlight on mouseover* (a 10% white wash) are OVERLAY textures on the **row** frame. The cells are **child frames** of that row (level +1), and every region of a child draws above every region of its parent, whatever the layer. So the self edge sits under the name cell (`x = 0`, `modules/Window.lua:393`), whose bar fill starts at that same left edge with the default `fillDirection = LEFT`, and the hover wash sits under every cell's fill and background. Both show only through the unfilled, 10%-alpha part of a cell and through the seams. The comment at Row.lua:1065-1076 assumes the edge sits "in a part of the row the tint does not use", but the *fill* uses it. Not confirmed in client: **owner to verify** with Highlight yourself on and your own bar non-empty. |
| MUL-S02 | modules/Window.lua:569, :779 | **Peer windows collide.** Every window is a UIParent child at the same strata (MEDIUM by default) and the same implicit base level, with no `SetToplevel` and no per-window level band. Where two windows overlap, window A's cells (+3) draw over window B's backdrop (+0) and rows, so the windows bleed through each other instead of one sitting on top. Dragging a window over another does not raise it. |
| MUL-S03 | settings/Schema_Compose.lua:172; modules/Export_Modal.lua:738 | **A meter can sit on top of its own dialogs.** The window strata setting offers **DIALOG**, which is the strata of the export modal (opened from that window's header), the debug console, the perf and sim panels and the three confirmation popups. Within one strata the winner is decided by level and creation order, and the modal is not toplevel. A Dialog-strata meter can cover the export window it just opened. A HIGH or DIALOG meter can also cover the Blizzard Settings window while it is being edited; verify the Settings window's strata in client. |
| MUL-S04 | modules/Export_Modal.lua:731-737 | **Stale rationale.** The modal's DIALOG choice is justified by "the FULLSCREEN strata the shared dropdown menu puts its click-catcher on". The library removed the catcher in Widgets minor 5 (Widgets.lua:232-249), and the menu now listens to `GLOBAL_MOUSE_DOWN`. DIALOG is still right, because it keeps the modal below the copy window (FULLSCREEN) and below the menu (FULLSCREEN_DIALOG), but the stated reason is not. |
| MUL-S05 | modules/Tooltip.lua:710-714 vs modules/Tooltip_Lines.lua:632-639 | **Stale layering note.** It says the tooltip bar's "fill is BORDER", but the code moved the fill to BACKGROUND sublevel 1 because BORDER collided with the backdrop edge. The note is the only description of the tooltip's z-order, and it is wrong. |
| MUL-S06 | modules/Tooltip_Lines.lua:83, :90 | **Level captured once.** Carrier and bar take `GameTooltip:GetFrameLevel()` at creation and are pooled for the session. If anything re-levels GameTooltip later (a tooltip skin, another addon, Blizzard raising it), pooled carriers keep the old level. The design depends on *equal* levels so regions interleave: a lower level puts the bars under the tooltip backdrop, and a higher one puts them over the tooltip's own ARTWORK text (the spell name). |
| MUL-S07 | modules/HeaderControls.lua:473 | **Ad hoc magic offsets.** Header controls sit at `dragBar + 5` (relative to a sibling, not to the frame), the grip at `frame + 10` (library) and the reorder line at `+ 20` (library). Strips, body, header strip, session line and drag bar all share an *implicit* +1. Nothing names the bands, so a future overlay (or the S01 fix) has no defined slot. It works today only because the +1 siblings do not overlap. |
| MUL-S08 | libs/LibKa0s/DebugLog.lua:536, PerfPanel.lua:186, SimPanel.lua:211; modules/Export_Modal.lua:729 | **Four DIALOG peers, none toplevel.** The export modal, debug console, perf panel and sim panel are all DIALOG with default levels and no `SetToplevel`. With two open (console plus export while debugging, or sim panel plus export during a sim), clicking the lower one does not bring it forward. Low impact; mostly debug surfaces. |
| MUL-S09 | modules/Window.lua:561 vs :779 | **Anchor and art frame strata can differ.** The anchor stays MEDIUM while the art frame follows the setting. That is harmless today: the anchor is invisible, takes no mouse and has no children. It is listed so nobody parents something visible to the anchor and expects it to follow the window's strata. |
| MUL-S10 | settings/Schema.lua:331-334 | The *Frame strata* tooltip does not warn about S03 (layout item MUL-L22 rewords it). |

No glow, flash or animation frames exist. No overlay frame is created anywhere in the addon. The empty
state and the notice draw inside the body area, and only while there are no rows. The test and sim strips
take the slot between title and column headers, which the layout reserves (`ChromeOffsets`), so they never
overlap the drag bar or the rows.

## Proposed strata map

Levels are relative to the window art frame's base level **L**.

| tier | strata | level band | elements |
|---|---|---|---|
| 0 — geometry | MEDIUM (fixed) | base | Window anchor (invisible; never parent anything visible to it) |
| 1 — HUD: meter windows | `window.frame.strata`, **recommended range LOW / MEDIUM / HIGH** | **L** (each window raised as a whole by `SetToplevel`) | art frame backdrop, header background, divider, title, notice |
| | | L+1 | chrome: drag bar, session line, column-header strip, body, test strip, sim strip |
| | | L+2 | row frames, column-header buttons, empty state |
| | | L+3 | cells (StatusBar: bg, fill, text, border, icon) |
| | | **L+4 (new)** | **row overlay**: self edge, mouseover wash (mouse disabled) |
| | | L+6 | header controls (stated relative to L, not to the drag bar) |
| | | L+10 | resize grip (library `GRIP_LEVEL`) |
| 2 — addon dialogs | DIALOG, **toplevel** | base | export modal, debug console, perf panel, sim panel; Blizzard StaticPopups |
| 3 — dialog children | FULLSCREEN | base | export copy window (opens above its modal) |
| 4 — menus | FULLSCREEN_DIALOG | base | shared dropdown popup; settings-panel AceGUI Dropdown pullouts (the LSM30_* media pullouts are TOOLTIP); Blizzard context menus (strata of the Blizzard `Menu` frames to verify in client) |
| 5 — tooltips | TOOLTIP | = GameTooltip level, re-stated per draw | GameTooltip and spell-line carriers/bars; reorder ghost |

The rule for this addon: **HUD below dialogs, dialogs below their own children, menus above all
windows, tooltips on top.** Within a window, level bands go up from back to front, each with a named
offset, and anything that marks a row sits in a band above the cells it marks.

## Proposed changes

| id | change (file:line, from → to) | reason | confidence |
|---|---|---|---|
| MUL-Z01 | modules/Row.lua:1077, :1083: parent `selfHighlight` and `mouseHighlight` to a new mouse-disabled `row.overlay = CreateFrame("Frame", nil, row.frame)`, with `SetAllPoints(row.frame)` and `SetFrameLevel(row.frame:GetFrameLevel() + 2)` (above the cells at +1). Layer stays OVERLAY. Pool-safe: built once in `Row.New`. The overlay must stay mouse-disabled (a Frame is by default; never call `EnableMouse`/`EnableMouseMotion` on it), or it steals every cell hover and the tooltip. | Fixes S01: the marks draw above what they mark. Owner to confirm the symptom in client first; if the edge is meant to sit under the fill, document that and close as intended. Side effect to check: once on top, the 3px edge (`SELF_EDGE_WIDTH`, Row.lua:991) covers the first pixel of a left icon or name, which start at `ICON_EDGE_INSET = 2` (Row_NameCell.lua:83, :181), and the 10% wash now tints the cell text too. Lowered from 70% because the fix changes what the player sees, not only the stacking. | 65% |
| MUL-Z02 | modules/Window.lua:569: add `frame:SetToplevel(true)` on the art frame, then wire an explicit raise into the drag start and the header-control click path. `onDragStart` (Window.lua:465) receives the **drag bar**, so the call is `frame.mmWindow.frame:Raise()`, not `frame:Raise()`. (The art frame takes no mouse, so toplevel alone may never fire; the explicit `Raise` is the part that works for certain.) | Fixes S02: overlapping windows stack whole instead of interleaving, and the one you touch comes to the front. In-client checks before keeping it: after a raise, the header controls (re-levelled on every layout, HeaderControls.lua:511) and the resize grip (levelled **once**, at creation, Core.lua:611) must still sit above the drag bar and the cells. If the client does not carry explicitly-levelled children along with a raised parent, the grip falls under the window and needs re-levelling after each raise. No combat concern: none of these frames is protected. Low player impact: meters rarely overlap. | 50% |
| MUL-Z03 | modules/Export_Modal.lua:738-741: add `modal:SetToplevel(true)` and `modal:Raise()` on every open. | Lessens S03 and S08 within DIALOG: the modal comes up above a DIALOG meter and above the debug, perf and sim panels when opened. | 65% |
| MUL-Z04 | settings/Schema_Compose.lua:172-173: drop `DIALOG` from the window strata values (LOW / MEDIUM / HIGH), with a migration step mapping stored `DIALOG` → `HIGH` and a raised `NS.SCHEMA_VERSION` (savedvariables-§1). | Removes S03 at the root: a HUD window cannot share a strata with the addon's dialogs. **This changes a setting's value set, so it is an owner decision.** It must not ride along with item 020, whose brief forbids changing settings, and `/mm set window.frame.strata DIALOG` would start being refused. If the owner keeps DIALOG, Z03 and the L22 tooltip are the mitigation. | 40% |
| MUL-Z05 | modules/Export_Modal.lua:731-737: rewrite the comment as "DIALOG: above the HUD windows, below the copy window (FULLSCREEN) and the shared dropdown menu (FULLSCREEN_DIALOG), so a menu opened from the modal draws over it and the copy window opens above it." | Fixes the stale rationale (S04). | 95% |
| MUL-Z06 | modules/Tooltip.lua:710-714: correct the note to "track BACKGROUND 0, fill BACKGROUND 1, GameTooltip text ARTWORK, number slots OVERLAY, LSM edge BORDER". | Fixes the stale note (S05). | 95% |
| MUL-Z07 | modules/Tooltip_Lines.lua:83, :90: also re-state `frame:SetFrameLevel(GameTooltip:GetFrameLevel())` and the bar's level in the per-draw path (beside the fill re-stating at :639). | Fixes S06: the equal-level interleave survives a re-levelled tooltip. Costs two calls per line per hover. Not confirmed that GameTooltip's level ever moves in practice: owner check is `/dump` of a carrier's level against `GameTooltip:GetFrameLevel()` after an hour of play with a tooltip addon loaded. If they always match, this is defensive only. | 55% |
| MUL-Z08 | Name the window's level bands in one table, e.g. `Const.LEVEL = { CHROME = 1, ROWS = 2, CELLS = 3, ROW_OVERLAY = 4, CONTROLS = 6, GRIP = 10 }` in core/Constants.lua. Set HeaderControls.lua:473 to `frame:GetFrameLevel() + LEVEL.CONTROLS` (frame-relative), and have Z01 use `ROW_OVERLAY - ROWS`. | Fixes S07: one named stack instead of three unrelated magic numbers. The grip's +10 stays the library's. Mirror the number in the table and cite `GRIP_LEVEL`. | 60% |
| MUL-Z09 | docs/ARCHITECTURE.md (or a "Layering" section in docs/data-flow.md): add the proposed strata map above as the addon's reference, and a smoke test: two overlapping windows; Dialog-strata meter opening its export; Highlight yourself on a non-empty bar. | Makes the layering reviewable; the owner runs the in-client checks. | 80% |
| MUL-Z10 | Upstream (LibKa0s): `SetToplevel(true)` on the debug console, perf panel and sim panel frames (DebugLog.lua:536, PerfPanel.lua:186, SimPanel.lua:211). | S08, for every addon at once. This is a library change and is not edited in MultiMeters. | 50% |

### Considered and rejected

| id | change | why rejected | confidence |
|---|---|---|---|
| — | Per-window level bands (`id × 20` added to each art frame's level). | Fixes the overlap order once and for all, so the window you drag stays under a lower-id window. It also spends level headroom per window on a profile that may hold twenty. Z02 follows the player's last touch instead. | 30% |
| — | Raise the tooltip spell-line carriers one level above GameTooltip, to stop depending on equal levels (S06). | Every carrier region then draws above GameTooltip's own ARTWORK text, which covers the spell name with the bar. The equal-level interleave is the design (Tooltip.lua:710-714), and Z07 keeps it. | 15% |
| — | Put the meter windows in UISpecialFrames, or make them toplevel DIALOG frames. | Window.lua:594-603 explains why a meter is furniture and not a dialog: Escape would close it constantly. HUD stays below the dialog tier. | 10% |
| — | Re-parent the self edge to the name cell, instead of Z01's overlay frame. | Fixes the edge but not the mouseover wash, which spans every cell. One overlay frame fixes both. | 30% |

## Notes for the upstream guidance

- **Overlay frames, not overlay layers.** A highlight or marker drawn as an OVERLAY *texture on a parent*
  sits under the parent's child frames. MultiMeters' row highlights are the live example (S01). Rule to
  codify: **anything that marks or overlays a child frame lives on its own mouse-disabled frame at a level
  above that child.** Draw layers order regions only within one frame level.
- **One HUD strata knob, capped below DIALOG.** If an addon exposes a strata setting for its HUD, the range
  should stop at HIGH. DIALOG belongs to the addon's own dialogs, popups and debug panels. A HUD that can
  share a strata with its own modal will cover it sooner or later.
- **Named level bands per window.** Write the stack down as named offsets from the window's base level
  (chrome +1, rows +2, cells +3, overlay +4, controls +6, grip +10 from Core). Set levels relative to the
  window frame, never relative to a sibling (`dragBar + 5`).
- **Peer windows: toplevel.** An addon with several movable windows of one kind should make each
  `SetToplevel(true)` and raise it on drag, so windows stack whole instead of interleaving by child level.
- **Dialog tier.** Every addon-owned modal and debug panel goes in DIALOG, toplevel, clamped. Any window
  opened *from* a dialog goes one strata up (FULLSCREEN, as the library's copy window already does). Menus
  are FULLSCREEN_DIALOG (library popup, Blizzard Menu). The pattern exists in LibKa0s already; the
  guidance should state it so addons stop justifying it with their own (now stale) reasons (S04).
- **Children of Blizzard's tooltip.** Frames hung on GameTooltip that rely on equal-level interleaving
  must re-state the level on every show, because the tooltip's level is not the addon's to keep.
- **Comments that describe layering go stale.** Two of MultiMeters' three layering comments are wrong
  (S04, S05). The guidance should ask for one layering table per addon (in its architecture doc), so the
  stack is written down in one place and reviewed in one place.

## Review

Independent review, 2026-10-24, against `../MultiMeters` at `master` (`fd3200a`). Every `CreateFrame`,
`SetFrameStrata`, `SetFrameLevel`, `SetToplevel` and `SetClampedToScreen` in `core/`, `modules/` and
`settings/` was matched to an inventory row, and the library frames the addon opens were checked in
`libs/LibKa0s/`. The inventory is accurate: header controls really sit at drag bar + 5 = frame + 6
(HeaderControls.lua:472, :511), the grip at + 10 (Core.lua:546, :611), the tooltip carriers at
GameTooltip's level (Tooltip_Lines.lua:83, :90). Both stale comments, S04 (Export_Modal.lua:732-737) and S05
(Tooltip.lua:710-714 still says "fill is BORDER"), are confirmed. So is S01: the highlights are OVERLAY
textures on the row frame (Row.lua:1077, :1083) and the cells are its child StatusBars (Row.lua:549).

What changed:

- **Inventory.** Gave the export modal its real name (`MultiMetersExportWindow`, Export_Modal.lua:125),
  explained why the session line takes no mouse and noted the menu anchors to it, and added the
  settings-panel pullouts (AceGUI Dropdown FULLSCREEN_DIALOG, LSM30 media TOOLTIP) as a row and to tier 4, so the "menus above all windows" claim names them.
- **Z01** 70→65%. It needs the overlay kept mouse-disabled, or it steals every cell hover. On top, the 3px
  edge covers 1px of a left icon or name (inset 2px) and the wash tints the text. Both are visible changes
  the owner should accept.
- **Z02** 55→50%. Corrected the call site: the drag handler gets the drag bar, so the raise is
  `mmWindow.frame:Raise()`. Toplevel alone may not fire on a mouse-disabled frame. Added the in-client check
  that the once-levelled grip survives a raise. No combat or protected-frame risk.
- **Z04** is marked an owner decision, kept apart from item 020's no-settings rule, with the
  `/mm set` consequence named.
- **Z07** now says how to verify whether GameTooltip's level ever drifts, so it is not kept on faith.
- **Interaction check (brief point 5).** None of the proposed changes puts a HUD frame above a menu,
  tooltip or settings pullout. Those are FULLSCREEN_DIALOG/TOOLTIP, above any value the strata setting
  allows. Z03 raises the export modal within DIALOG only, so the copy window (FULLSCREEN) and the selector
  menu (FULLSCREEN_DIALOG) still open over it. No proposed frame is protected or touched in combat.
- **Added "Considered and rejected"** with four alternatives and the reasons they lost.

