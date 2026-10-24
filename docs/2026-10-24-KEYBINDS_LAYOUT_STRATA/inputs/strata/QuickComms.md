# QuickComms — frame strata analysis

Item 030. A read-only analysis of `../QuickComms` at `master` (2026-10-24). Every `CreateFrame`,
`SetFrameStrata`, `SetFrameLevel` and draw-layer choice in `core/`, `modules/` and `settings/` was
traced, plus the LibKa0s frames the addon opens.

QuickComms already went through one stacking fix, **QC-06**. The rationale is in the comments at
`settings/ModalWindow.lua:17-31` and `modules/PreviewWindow.lua:30-38`. The strata tiers below are
mostly deliberate. The problems are at the **frame-level and draw-layer** scale inside one button or
wedge, in the hard-coded numbers, and in two LibKa0s tool windows that ignore QC-06's tiers.

"Inherited" means the frame never sets the value and takes its parent's strata, at parent level + 1.
"L" is a frame's level.

## Inventory

| element | file:line | parent | strata | frame level | toplevel / clamped | notes |
|---|---|---|---|---|---|---|
| Comms Pad root `QuickCommsPad<id>` | `modules/Pad.lua:270-276` | UIParent | **MEDIUM**, explicit (`:273`) | client default | no / **clamped** (`:271`) | Movable; carries the Ka0s skin backdrop (`NS.ApplySkin`) |
| Pad header row | `Pad.lua:280` | pad root | inherited | inherited (root+1) | no / no | Mouse on: hover, why-tooltip, click to collapse |
| Pad header collapse button | `modules/Pad_Render.lua:501` | header | inherited | inherited (root+2) | no / no | Font string glyph |
| Pad header strings (situation, LOCKDOWN, stale hint) | `Pad_Render.lua:494-513` | header | inherited | — | — | OVERLAY |
| Pad drag strip (LibKa0s DragHandle) | `Pad.lua:296` → `libs/LibKa0s/WidgetsDragHandle.lua:653` | pad root | inherited | inherited (root+1) | no / no | Shown while unlocked. Anchored **outside** the root, `NS.DRAG_GAP` (2 px) above or below it (`Pad.lua:332-338`), so it never overlaps the header or the buttons. Its help button and close button are children (`WidgetsDragHandle.lua:394, 447`) |
| Section title band | `Pad.lua:139` | pad root | inherited | inherited (root+1) | no / no | BackdropTemplate, mouse off; title font string OVERLAY on it (`:141`); pooled |
| Section title hit frame | `Pad.lua:155` | pad root | inherited | inherited (root+1), **same rect as the band** | no / no | Right-click opens Groups; pooled. Draws nothing, and the band under it is mouse-off (`Pad.lua:140`), so their order has no visible or click effect |
| Pad button (secure) `QuickCommsSend<n>` | `modules/SendEngine.lua:84` | pad root | inherited | inherited (root+1) | no / no | SecureActionButtonTemplate; pooled |
| … button background `qcBg` | `Pad_Render.lua:162` | button | — | — | — | BACKGROUND |
| … icon `qcIcon` | `Pad_Render.lua:169` | button | — | — | — | ARTWORK |
| … shine overlay (3 pieces, plus 2 blooms) | `modules/Shine.lua:108` | button | — | — | — | ARTWORK sublevels 5 to 7 |
| … label, padlock | `Pad_Render.lua:172, 174` | button | — | — | — | OVERLAY |
| … veils: dim (refused), cool (cooldown), flash (send) | `Pad_Render.lua:123` (`veil`), `:182-184` | button | — | — | — | OVERLAY |
| … hover tint | `Pad_Render.lua:187` | button | — | — | — | HIGHLIGHT |
| … edge frame `qcEdge` (button border; button-glow host) | `Pad_Render.lua:166` | button | inherited | inherited (**btn+1**) | — | BackdropTemplate, mouse off |
| … icon frame `qcIconFrame` (icon border; icon-glow host) | `modules/IconStyle.lua:127` | button | inherited | inherited (**btn+1**) | — | Made on first use |
| … button glow (LibCustomGlow) | `modules/Glow.lua:170` | `qcEdge` | inherited | **edge + 2** (`Glow.FRAME_LEVEL = 2`, `:50`) | — | Key `QuickCommsButton` |
| … icon glow (LibCustomGlow) | `Glow.lua:77` | `qcIconFrame` | inherited | **icon frame + 2** | — | Key `QuickCommsIcon` |
| Comms Dial header `QuickCommsDial<n>` (secure) | `SendEngine.lua:206-209` | UIParent | **DIALOG**, explicit (`:208`) | client default | no / no | SecureHandlerClickTemplate. Its strata is protected in combat |
| Dial ring container (secure) | `SendEngine.lua:217` | header | inherited | inherited (h+1) | — | SecureFrameTemplate |
| … ring title | `modules/Dial_Render.lua:371` | ring | — | — | — | OVERLAY |
| … slice fills, highlight, shine layers, masks | `modules/Dial_Slices.lua:59, 97, 121, 205, 218` | ring | — | — | — | BACKGROUND sublevels 1 to 6 |
| … page pills and dots | `Dial_Slices.lua:71-80` | ring | — | — | — | OVERLAY caps |
| Dial ring catcher (secure) | `SendEngine.lua:230-234` | ring | inherited | **explicit: header − 1** (`:234`) | — | Takes every disc click. Set below its own parent ring |
| Dial screen catcher (secure) | `SendEngine.lua:247-249` | header | **HIGH**, explicit (`:248`) | inherited | — | `SetAllPoints(UIParent)`; shown only on a key open |
| Dial wedge (secure) | `Dial_Secure.lua:271` → `SendEngine.lua:84` | ring | inherited | inherited (h+2) | — | Mouse off: the tracker drives hover |
| … wedge icon, label, padlock | `Dial_Render.lua:458-462` | wedge | — | — | — | ARTWORK / OVERLAY |
| … wedge veils (dim, cool, flash) | `Dial_Render.lua:467-472` | wedge | — | — | — | OVERLAY |
| … wedge icon frame and its glow | `IconStyle.lua:127`, `Glow.lua:77` | wedge | inherited | h+3; glow **h+5** | — | |
| Dial page arrows (secure) | `Dial_Secure.lua:277` | ring | inherited | inherited (h+2) | — | Plate BACKGROUND, chevron ARTWORK (`Dial_Render.lua:385-386`) |
| Dial hub front frame `qcPointer` | `Dial_Render.lua:169-191` | header | inherited | **explicit: header + 20** (`:211`, `RaiseFront`) | — | Hub disc, rim, ring and dot, the pointer, and the LOCKDOWN, stale and TEST strings; mouse off |
| Preview window `QuickCommsPreviewWindow` | `modules/PreviewWindow.lua:182, 162` | UIParent | **FULLSCREEN**, explicit | client default (never `Raise`d by design, `:35-38`) | no / **clamped** (`:165`) | Movable; position persisted |
| … its buttons, dropdown and close mark | `PreviewWindow.lua:108, 246, 184` | window | inherited | inherited | — | The dropdown's menu is the LibKa0s menu (below) |
| Modal click-catcher (popup band) | `settings/ModalWindow.lua:95-98` | UIParent | **FULLSCREEN**, explicit | **explicit: `LEVEL` = 10** | — | Dims what it covers |
| Callout popup window | `ModalWindow.lua:120-121`, `settings/CalloutPopup.lua:454` | catcher | FULLSCREEN, explicit | **explicit: 12** | special frame (Escape) | `SettingsFrameTemplate`. Bg 11 (`:137`), page 13 (`:133`), close X 15 (`:141`), fallback bg (`:79`) |
| … token glyph | `CalloutPopup.lua:230` | popup body | inherited | inherited | — | |
| Icon browser catcher and window | `settings/IconBrowser.lua:558` via `ModalWindow.lua:115-141` | UIParent / catcher | FULLSCREEN, explicit | **explicit band at `LEVEL_OVER` = 200** (200 / 201 / 202 / 203 / 205) | special frame | 560 × 594 |
| … grid, cells, slider, clear mark, hint box | `IconBrowser.lua:340, 364, 373, 463, 500, 562` | browser body | inherited | inherited | — | |
| Icon browser's Wowhead link window | `IconBrowser.lua:491-494` | UIParent (LibKa0s CopyWindow) | **FULLSCREEN_DIALOG**, overridden after creation (`:494`) | client default | clamped (lib) | Must sit over the browser's band |
| Share export window `QuickCommsShareWindow` | `modules/Share.lua:699` → `libs/LibKa0s/Widgets.lua:653` | UIParent | **FULLSCREEN** (library default) | client default | clamped | |
| Confirm popups (delete, Reset all): Blizzard StaticPopup | `ModalWindow.lua:153-170` (`LiftConfirm`) | Blizzard | **FULLSCREEN_DIALOG** while shown, then restored | Blizzard | Blizzard | Restored to its remembered strata, or DIALOG |
| LibKa0s dropdown menu (preview window, browser filters) | `libs/LibKa0s/Widgets.lua:225` | UIParent | FULLSCREEN_DIALOG (library) | library | — | The addon does not pick it |
| LibKa0s debug console | `libs/LibKa0s/DebugLog.lua:536` | UIParent | **DIALOG** (library) | client default | clamped | Opened by *Debug console*; default position CENTER (+220, −80) |
| LibKa0s debug copy window (the console's Copy) | `DebugLog.lua:578, 717, 898-899` → `Widgets.lua:653` (CopyWindow) | UIParent | **FULLSCREEN** (library) | client default | clamped | Opened from the console. It sits over the console only because it is one strata higher (added in review) |
| LibKa0s perf panel | `libs/LibKa0s/PerfPanel.lua:186` | UIParent | **DIALOG** (library) | client default | clamped | `/qc perf`; default position CENTER (−320, 0) |
| Blizzard ColorPickerFrame (swatches in the popup, the icon browser and the settings) | AceGUI ColorPicker widget; `settings/Editors.lua:282-320` | UIParent | **FULLSCREEN_DIALOG** (AceGUI lifts it, `IconBrowser.lua:37-39`) | Blizzard | toplevel (Blizzard) | Not modal; hidden when the browser closes (added in review) |
| AceGUI Dropdown pull-outs (Channel, filters, every settings dropdown) | AceGUI | UIParent | **FULLSCREEN_DIALOG** (AceGUI) | AceGUI | — | Over both modal bands (added in review) |
| LibKa0s settings parts: combat cover, tab strip, reorder rows, IdList suggestions, autocomplete | `Options.lua:589`, `OptionsTabs.lua:375, 712`, `WidgetsReorder.lua:255, 600`, `OptionsIds.lua:997`, `WidgetsAutocomplete.lua:161` | Blizzard SettingsPanel (HIGH) | inherited / FULLSCREEN_DIALOG | library relative levels | — | The addon does not pick these |
| LibKa0s reorder drag ghost | `libs/LibKa0s/WidgetsReorder.lua:107` | UIParent | TOOLTIP (library) | — | — | |
| Tooltips (pad, title, header, wedge, arrow, hub) | `Pad_Render.lua:141-157`, `Dial_Render.lua:346-356` | GameTooltip | TOOLTIP (Blizzard) | — | — | The dial anchors its tooltips outside the disc |
| Toggle Comms Pads click target | `settings/SlashVerbs.lua:91-95` | UIParent | inherited (MEDIUM) | default | — | Never shown. A binding target only |
| Minimap button | LibDBIcon (`core/LauncherSetup.lua`) | Minimap | LibDBIcon's | LibDBIcon's | — | The addon does not pick it |

## Problems

- **QUI-S01**: Inside a pad button, the button's veils are **below** its own borders and glows. The dim
  veil (a refused slot), the cooldown veil and the send flash are OVERLAY regions on the button
  (`Pad_Render.lua:182-184`). The edge frame (`:166`) and the icon frame (`IconStyle.lua:127`) are child
  frames, so they draw above every region of the button. Their borders, and both LibCustomGlow effects
  started on them (`Glow.lua:77, 170`), draw **over** the veils. A dimmed, refused button keeps a
  full-brightness icon border and glow. The send flash goes under the glow it should light. The padlock
  and the label (OVERLAY on the button) sit under any border thicker than their inset. The same holds on a
  dial wedge (`Dial_Render.lua:458-472`): its icon frame and glow at h+3 and h+5 draw over its own
  OVERLAY veils at h+2.
- **QUI-S02**: Siblings tie, so the order is creation order:
  - The edge frame and the icon frame both take the default btn+1 (`Pad_Render.lua:166`,
    `IconStyle.lua:127`). Where they overlap (an icon-only button, square around its icon, with a border
    on each), whichever was created later draws on top, and the icon frame is created lazily.
  - The button glow (edge + 2) and the icon glow (icon frame + 2) both land on **btn+3**, because one
    `Glow.FRAME_LEVEL` (`Glow.lua:50`) serves both.
- **QUI-S03**: Every child of the pad root takes the default root+1: the header, the drag strip, the
  section title bands, the title hit frames and the buttons (`Pad.lua:139, 155, 280, 296`). The hit frame
  and the title band share a rectangle and a level. *(Review: there is no visible or click defect. The hit
  frame draws no region, and the band is mouse-off (`Pad.lua:140`), so a click reaches the hit frame
  whichever is on top. The drag strip is anchored outside the root, 2 px past its edge (`Pad.lua:332-338`),
  so it never overlaps the header. This is a documentation point only.)*
- **QUI-S04**: The hard-coded levels are scattered across five files with no shared table:
  - `+20` for the hub front (`Dial_Render.lua:211`)
  - `header − 1` for the ring catchers (`SendEngine.lua:234`)
  - `Glow.FRAME_LEVEL = 2` (`Glow.lua:50`)
  - `MW.LEVEL = 10` and `MW.LEVEL_OVER = 200`, with offsets +1, +2, +3 and +5 (`ModalWindow.lua:44-141`)

  The strata names are scattered the same way: `"MEDIUM"`, `"DIALOG"`, `"HIGH"` and `"FULLSCREEN"`
  appear as literals in `Pad.lua:273`, `SendEngine.lua:208, 248` and `PreviewWindow.lua:162`, beside
  `MW.STRATA` and `MW.CONFIRM_STRATA`. The QC-06 reasoning ties these numbers together, but a reader has
  to reassemble it from four comment blocks.
- **QUI-S05**: The LibKa0s **debug console** (`DebugLog.lua:536`) and the **perf panel**
  (`PerfPanel.lua:186`) are DIALOG, the Comms Dial's strata. The hub front at header + 20, the wedges and
  their glows can draw over the console. That is the level race QC-06 fixed for the preview window by
  moving it to FULLSCREEN. The console's default spot (CENTER +220, −80) overlaps a dial at its default
  place. Test mode and *Preview as* open dial 1 in the middle of the screen while a developer is reading
  the console. *(Review: the console's own Copy window is the library's CopyWindow, FULLSCREEN
  (`Widgets.lua:653`). It is over the console today only because the console is DIALOG. Lifting the
  console to FULLSCREEN alone would tie the two at client-default levels, and the copy window could
  open under the console.)*
- **QUI-S06**: The dial's full-screen **screen catcher** is HIGH (`SendEngine.lua:248`). Blizzard's
  `SettingsPanel` is also HIGH and toplevel. With the settings window open and a dial opened by its key,
  a click on the settings window raises it over the catcher and lands on the settings, instead of closing
  the dial as the catcher's snippet intends ("lets nothing through"). This is low severity: a key-opened
  dial over an open settings window is rare.
- **QUI-S07**: Two FULLSCREEN windows rest at client-default levels with no rule between them: the
  preview window (`PreviewWindow.lua:162`) and the Share export window (`Share.lua:699`, library default).
  Neither raises (the preview window is not raised by design), so which is on top is creation order. This
  is low severity, because they rarely meet.
- **QUI-S08**: The strata override is made in two ways. The Wowhead link window is lifted to
  FULLSCREEN_DIALOG by a `SetFrameStrata` call after the library builds it (`IconBrowser.lua:494`). The
  Share window keeps the library's FULLSCREEN, and the confirms are lifted by `LiftConfirm`. Three ways
  to pick a strata for a borrowed window.
- **QUI-S09**: The ring catcher's level is set **below its own parent ring** (`SendEngine.lua:234`, level
  h − 1 under a ring at h + 1). The client allows it and it works today, because the ring draws nothing.
  But nothing pins this inversion, and a future ring backdrop would draw over the catcher's area. Low
  severity.
- **QUI-S10**: The preview window is in FULLSCREEN, a high tier for a small control strip. It covers the
  world map, the bags and the character frame. QC-06 justifies this: the dial's DIALOG header cannot move
  in combat, so the window must sit above it. It is listed here for the upstream rule, not as a defect.

## Proposed strata map

Tier by tier, bottom to top. "Band" is a frame-level range relative to the element's own root.

1. **HUD: Comms Pads.** MEDIUM. Pad root at client level L, with these bands:
   - L+1: the header, the section title bands, the title hit frames, the buttons and the drag strip
     (the strip lies outside the root's rect, so it needs no band of its own)
   - L+2: the header's collapse button

   Inside a button at level B:
   - regions: BACKGROUND (bg), then ARTWORK (icon), then ARTWORK 5-7 (shine)
   - B+1: the edge frame (button border)
   - B+2: the button glow
   - B+3: the icon frame (icon border, over the button's border)
   - B+4: the icon glow
   - **B+6: the overlay frame**, with the label and padlock (OVERLAY 0) and the dim, cool and flash
     veils (OVERLAY 1-3)
   - the hover stays HIGHLIGHT on the button

2. **Pop-up HUD: Comms Dial.** DIALOG, header at level H. The header's strata is protected in combat, so
   this tier is the fixed point everything else is measured against.
   - H+1: the ring containers (the title, and the slice fills and shine at BACKGROUND 1-6)
   - H+2: the wedges and page arrows (mouse off, apart from the arrows)
   - H+3: the wedge icon frame
   - H+4: the wedge icon glow
   - H+6: the wedge overlay frame (label, padlock, veils)
   - **H+20**: the hub front (hub, pointer and status strings), named as a constant
   - the ring catcher stays at H−1, documented as an inversion
   - **the screen catcher: HIGH**, one tier under the dial
3. **Developer tools: the debug console and the perf panel.** These should be in the same tier as the
   QuickComms windows (FULLSCREEN, lowest band), not DIALOG, so the dial can never cover them. That needs a
   LibKa0s `strata` option (QUI-Z05). The console's copy window must then stay a tier above it
   (FULLSCREEN_DIALOG), through the same option on CopyWindow (QUI-Z06).
4. **QuickComms windows.** FULLSCREEN at client levels, never raised: the preview window and the Share
   export window.
5. **Modals.** FULLSCREEN:
   - the popup band at 10 to 15 (catcher 10, Bg 11, window 12, page 13, close 15)
   - the icon browser band at 200 to 205
6. **Over-modal.** FULLSCREEN_DIALOG: the confirms (lifted while shown), the icon link window, the LibKa0s
   menus, the AceGUI pull-outs and the color picker.
7. **Tooltips and the drag ghost.** TOOLTIP (Blizzard and the library).

## Proposed changes

| id | change (file:line, from → to) | reason | confidence |
|---|---|---|---|
| QUI-Z01 | Add `core/Constants.lua` → `NS.Layers`, a single table. Strata: `PAD = "MEDIUM"`, `DIAL = "DIALOG"`, `DIAL_SCREEN = "HIGH"`, `WINDOW = "FULLSCREEN"`, `OVER_MODAL = "FULLSCREEN_DIALOG"`. Levels: `BTN_EDGE = 1`, `BTN_GLOW = 1` (relative to the edge), `BTN_ICON = 3`, `ICON_GLOW = 1` (relative to the icon frame), `BTN_OVER = 6`, `DIAL_FRONT = 20`, `MODAL = 10`, `MODAL_OVER = 200`. Then replace the literals at `Pad.lua:273`, `SendEngine.lua:208, 234, 248`, `PreviewWindow.lua:162`, `Dial_Render.lua:211`, `Glow.lua:50` and `ModalWindow.lua:44-51` with reads of it. Move the QC-06 reasoning into the table's header comment once. `core/Constants.lua` already exists and loads first. `MW.STRATA` and `MW.CONFIRM_STRATA` become aliases of the table, so `CalloutPopup.lua:454` and `IconBrowser.lua:558` keep working. *(Review: dropped `PAD_HIT` and `PAD_STRIP` with Z07.)* | One place states the whole stack (S04), and a later change cannot quietly pull one number out of step. | 75% |
| QUI-Z02 | Pad button: give `qcEdge` an explicit level, B+1 (`Pad_Render.lua:166`). Give `qcIconFrame` an explicit B+3 (`IconStyle.lua:127`, `SetFrameLevel(btn:GetFrameLevel() + BTN_ICON)`). Start the button glow at `BTN_GLOW = 1` (`Glow.lua:170`) and the icon glow at `ICON_GLOW = 1` (`Glow.lua:77`), which gives B+2 and B+4. Set them in `R.Dress` and `IS.IconFrame`. Both run out of combat on a pooled button (`SE.NewButton` refuses in combat), and a child's explicit level moves with its parent's later level changes. | Removes both ties (S02). The icon border is always over the button border, and each glow sits over its own border. Watch for this: on an icon-only button the icon rect is the button rect, so the icon border at B+3 then draws over the inner half of a button glow at B+2. Check it in the client. | 65% |
| QUI-Z03 | Pad button: add a mouse-off overlay frame `btn.qcOver` at B+6 (`Pad_Render.lua`, `R.Dress`). Reparent `qcLabel` and `qcLock` (OVERLAY 0) and `qcDim`, `qcCool` and `qcFlash` (OVERLAY sublevels 1 to 3) onto it. `qcBg`, `qcIcon`, the shine and the HIGHLIGHT hover stay on the button. The overlay **must** be `EnableMouse(false)`, or it would take the clicks of the secure button under it. Hover, the tooltip and the click stay on the button. | The veils then cover the borders and glows they veil: a refused button dims whole, and the flash lights over the glow. The label and padlock can no longer sit under a thick border (S01). | 60% |
| QUI-Z04 | Dial wedge: the same as Z02 and Z03 in `Dial_Render.lua:455-472` (wedge overlay at H+6 holding the label, padlock and veils), with the icon frame and its glow at H+3 and H+4. | The wedge's layer order then matches the button's within one addon (S01). | 60% |
| QUI-Z05 | Upstream to LibKa0s: `DebugLog` console and `PerfPanel` descriptors accept `strata` (default DIALOG, so other addons are unchanged). QuickComms passes `NS.Layers.WINDOW` (FULLSCREEN) in `core/DebugLogSetup.lua` and `core/PerfSetup.lua`. **The same change must lift the console's copy window** to FULLSCREEN_DIALOG, through Z06's `strata` on CopyWindow, inside DebugLog. Without it, the copy window ties with the console it was opened from (S05 review note). The modal catchers at FULLSCREEN level 10 and up still cover the console, as they do today. | The developer tools cannot then sit under the dial's hub and wedges (S05), and the QC-06 fix reaches the library-owned windows too. The dial over the console is a developer-only annoyance, so the upstream cost weighs against it. | 45% |
| QUI-Z06 | Upstream to LibKa0s: `CopyWindow` accepts `strata`. QuickComms then passes `OVER_MODAL` in the icon link window's descriptor (`IconBrowser.lua:491`) and drops the post-hoc `SetFrameStrata` (`:494`). The Share window passes `WINDOW` explicitly (`Share.lua:699`). Inside LibKa0s, DebugLog passes FULLSCREEN_DIALOG for the console's copy window when Z05 lifts the console. | One way to pick a borrowed window's strata (S08), and the Share window's tier is stated rather than borrowed from a library default (S07). | 50% |
| QUI-Z08 | `SendEngine.lua:234`: keep `header − 1`, but name it `NS.Layers.DIAL_CATCHER = -1`, with a comment that it is deliberately under its parent ring, and add a headless pin that the ring frame draws no region. | It documents and guards the inversion (S09). | 45% |
| QUI-Z09 | The screen catcher (`SendEngine.lua:248`): **no strata change**. A HIGH tie with the SettingsPanel is accepted and documented in `NS.Layers`. Moving it to DIALOG would tie with the ring catchers (the comment at `SendEngine.lua:240-244`). | The tie is known and rare (S06). The alternatives are worse. DIALOG ties with the ring catchers, FULLSCREEN would cover the dial and take every slice click, and a level below the ring catchers' `header − 1` can go below 0. *(Review: the draft's 40% read as doubt about a decision whose alternatives are all worse.)* | 75% (that no change is right) |
| QUI-Z10 | The preview window (`PreviewWindow.lua:162`): **no change**. Record FULLSCREEN as the "QuickComms windows" tier in `NS.Layers`. | QC-06 is correct. The dial's DIALOG is fixed in combat (S10). | 85% (that no change is right) |

That is **9 strata changes**: 7 code changes, of which 2 are upstream LibKa0s options, and 2 that are
documented as no change. Z07 moved to "Considered and rejected".

## Considered and rejected

| id | change | why rejected | confidence |
|---|---|---|---|
| QUI-Z07 (draft) | Pad root children: set explicit levels at creation. The title hit frame becomes root + `PAD_HIT` (`Pad.lua:155`), and the drag strip becomes root + `PAD_STRIP` after `NS.MakeDragHandle` (`Pad.lua:296`). The header, title bands and buttons stay at root+1. | No defect to fix. The hit frame draws nothing and its band is mouse-off, so their order changes neither the picture nor the click. The drag strip sits outside the root, so it cannot be under the header (S03 review note). A level constant for a non-problem is one more number to keep in step. | 35% |

## Notes for the upstream guidance

- **A secure frame's strata is a fixed point.** When an addon owns a secure frame that shows in combat
  (the dial header), its strata cannot be moved in combat. Choose it once, high enough. Every insecure
  window that must sit above it then moves up a tier instead. QC-06 is the worked example. The guidance
  should say: "pick the secure tier first, then build the rest of the stack around it."
- **Use strata for separation and levels for stacking within a tier.** QuickComms separates its
  modals from the dial **by strata** (FULLSCREEN over DIALOG) rather than by level, because the dial's hub
  sits at header + 20 and a level race against it is lost. Suggested rule: elements of different owners or
  roles (HUD, pop-up HUD, windows, modals, over-modal, tooltips) are separated by strata. Elements within
  one role use explicit level **bands**.
- **Bands for nested modals.** One strata, two bands far apart (10 and 200), each with fixed offsets for
  catcher, background, window, page and close. That is a clean pattern for "a modal over a modal" without
  spending a strata.
- **Never Raise a window that shares a strata with modals.** `PreviewWindow.lua:35-38` explains why:
  `Raise` lifts a frame over every frame in its strata, including a modal's catcher. The guidance should
  make this a MUST for any window in the modal tier.
- **A child frame draws over every region of its parent.** A border or glow host made as a child frame sits
  above the parent's OVERLAY veils and labels. Put the veils, labels and marks on an **overlay child** at
  the top of the element's band (QUI-Z03). This is the most likely defect across the collection.
- **Never let two siblings tie.** Two child frames at the default parent+1 that overlap are ordered by
  creation, and a pooled or lazy frame makes that order unpredictable. Set the level explicitly whenever
  overlapping siblings **both draw**. A sibling that draws nothing, or a mouse-off one, needs no level of
  its own.
- **An overlay child is mouse-off.** A region-holder frame laid over a clickable button, secure ones above
  all, has to `EnableMouse(false)`, or it takes the button's clicks.
- **Moving a library window's strata moves its children's too.** Before lifting a library window to a
  higher strata, check every window it opens, such as a copy window, so they keep their order.
- **Lift a borrowed Blizzard dialog only while it is shown.** `ModalWindow.LiftConfirm` (`:153-170`) lifts a
  shared StaticPopup to FULLSCREEN_DIALOG while it is shown and puts it back on hide, so other addons'
  popups are unaffected. That is a reusable pattern, and a LibKa0s candidate.
- **One layers table per addon.** Every strata name and level offset is a named constant in one table, and
  its header comment states the stack. That is the "consistency within a single addon" the brief asks for,
  in checkable form: a lint or grep for literal `SetFrameStrata("…")` outside the table.
- **Library-owned windows need a strata option.** The console, the perf panel and the copy window hard-code
  their strata (DIALOG, DIALOG, FULLSCREEN). An addon whose secure tier is DIALOG cannot keep them above
  its HUD. The library should take `strata` in each descriptor.

## Review

Independent review against `../QuickComms` at `master` (`bdce9d4`), 2026-10-24. Every `CreateFrame`,
`SetFrameStrata`, `SetFrameLevel`, `SetToplevel`, `SetClampedToScreen` and `Raise` in `core/`, `modules/` and
`settings/` was re-grepped. There is no `SetToplevel`, no `Raise` and no `SetFixedFrame*` in the addon. The
LibKa0s strata the addon depends on were re-read (`DebugLog.lua:536`, `PerfPanel.lua:186`,
`Widgets.lua:225, 653`, `WidgetsReorder.lua:107`).

- **Inventory corrected.** The drag strip is anchored outside the pad root, 2 px past its edge
  (`Pad.lua:332-338`), so it cannot overlap the header. The title hit frame draws no region, and its band
  is mouse-off. Added rows for the debug console's copy window (CopyWindow, FULLSCREEN), Blizzard's
  ColorPickerFrame (FULLSCREEN_DIALOG through AceGUI) and the AceGUI dropdown pull-outs
  (FULLSCREEN_DIALOG), all of which the stack depends on. The perf panel's default position is noted.
  The other rows checked out: the levels at `SendEngine.lua:208, 234, 248`, `Dial_Render.lua:211`,
  `Glow.lua:50, 77, 170` and `ModalWindow.lua:44-51, 79, 95-141`, the veils as OVERLAY regions at
  `Pad_Render.lua:182-184` and `Dial_Render.lua:467-472`, and the lazy icon frame at `IconStyle.lua:124-131`.
- **S03 downgraded** to a documentation point, because it has no visible or click effect. **Z07 rejected**
  (35%), and `PAD_HIT` and `PAD_STRIP` were dropped from Z01. The proposed map's L+3 strip band was removed.
- **An interaction break caught in Z05.** Lifting the console to FULLSCREEN alone ties it with its own
  copy window (FULLSCREEN, client-default level), so Copy could open under the console. Z05 now requires
  the copy window lifted through Z06, and drops to 45%.
- **Interaction guards added.** Z03 and Z04's overlay frame must be mouse-off, or it would take the secure
  button's clicks. Z02 notes that on an icon-only button the icon border at B+3 draws over the inner half
  of the button glow, and that needs an in-client look (75% → 65%). Z01 keeps `MW.STRATA` and
  `MW.CONFIRM_STRATA` as aliases for their two callers (80% → 75%).
- **Z09 re-scored** from 40% to 75% (that no change is right), with each alternative's failure stated.
- **Checked and unaffected.** The settings panel (HIGH) stays under every modal (FULLSCREEN). The color
  picker and the pull-outs stay over both modal bands. Tooltips and the drag ghost stay in TOOLTIP. No
  proposed change touches a secure frame's strata or level, or makes a protected call in combat. The
  dial header, the rings, the catchers and the wedges keep their values, and the new frames are plain,
  mouse-off children made out of combat.
- **Upstream notes added:** mouse-off overlay children, a level only for siblings that both draw, and
  checking a library window's child windows before lifting it.
