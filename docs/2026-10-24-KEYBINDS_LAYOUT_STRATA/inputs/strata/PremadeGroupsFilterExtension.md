# PremadeGroupsFilterExtension — frame strata analysis

Scope: item 030. Read from `../PremadeGroupsFilterExtension` at `master` (e5b741a) on 2026-10-24: `modules/{Panel,EUISkin,RegionTags}.lua`,
`settings/{Panel,Schema,Slash,Profiles}.lua`, `core/{LauncherSetup,DebugLogSetup,PGFBridge}.lua`, the vendored
`libs/LibKa0s/{DebugLog,Widgets,Launcher,Options,OptionsTabs}.lua`, and the installed host addon
`G:\...\AddOns\PremadeGroupsFilter\UI\Dialog.xml` + `Dialog.lua` (to check what the panel inherits). Every
`CreateFrame`, `SetFrameStrata`, `SetFrameLevel`, `SetToplevel`, `StaticPopup_Show` and `GameTooltip:SetOwner` under `core/`,
`modules/` and `settings/` was enumerated (PGFE calls `SetToplevel` nowhere).

PGFE has no free-standing HUD. Its one display surface is a panel **parented to and anchored under** PGF's dialog,
`PremadeGroupsFilterDialog`. PGF creates that dialog as a child of `PVEFrame` (`Dialog.lua:33`), its template
declares `frameStrata="FULLSCREEN"`, movable, **not** toplevel (`Dialog.xml:4-6`), and it is anchored at `PVEFrame`
TOPRIGHT (`Dialog.lua:256-262`) unless PGF's own `dialogMovable` setting lets the player drag it
(`Dialog.lua:88-110`; right-click resets it). Everything below follows from that: the panel must layer with PGF's
dialog, not with the rest of the UI.

## Inventory

Strata column: **E** explicit (set by code or XML), **I** inherited from the parent, **B** Blizzard/library-owned.
Level column: **abs** absolute number, **rel** parent ± n, **inh** default (parent + 1).

| element | file:line | parent | strata | frame level | toplevel / clamped | notes |
|---|---|---|---|---|---|---|
| Attached filter panel `PremadeGroupsFilterExtensionPanel` (PortraitFrameTemplateMinimizable) | modules/Panel.lua:769-772 | PGF dialog | **E** FULLSCREEN (hard-coded, matches PGF's XML) | **rel** dialog level + 5 (`ABOVE_DIALOG`, :46), snapshot at build only | no / no | Raised over PGF's NineSlice bottom border, which it overlaps by `ATTACH_RAISE` = 3px (:37-46). Under the EllesmereUI skin it is re-anchored flush (`SHELL_GAP` = 0, `modules/EUISkin.lua:28, :286-290`), so the overlap, and with it the tie the raise exists for, only arises in the Blizzard look. Never moved by the player: it follows the dialog. |
| Header art clips ×2 (top/bottom) | modules/Panel.lua:638-640 | panel | I | **rel** = panel level (`sinkToParentLevel`, :632-635) | — | Sunk to the panel's own level so they do not tie with MaximizeMinimize or the close button (:630-631). `SetClipsChildren`. |
| Header art NineSlice copies ×2 | modules/Panel.lua:641-642 | clip | I | **rel** = panel level | — | Two copies of PGF's border layout, cut at `HEADER_SEAM`. EllesmereUI skin sets alpha 0 (`EUISkin.lua:275`). |
| Template NineSlice, TitleContainer, TopTileStreaks, CloseButton (hidden) | template (:769, :722) | panel | I | inh (template) | — | Blizzard template children. CloseButton hidden; MaximizeMinimize replaces it. |
| Body frame | modules/Panel.lua:782-785 | panel | I | inh (panel + 1) | — | Starts at `BODY_TOP` −28, below the 24px title band, so it does not overlap the header click button. |
| Body widgets: check buttons ×8 (Active, keyTargeting, smartKeyLevel, regionsEnabled, playstyleEnabled, compositionEnabled, experiencedLeader, maxAgeEnabled) | :206, :270 | body | I | inh (body + 1) | — | UICheckButtonTemplate. Hit rect stretched over the label. |
| Edit boxes ×3 (level, age, copy-range) | :232, :561 | body | I | inh | — | InputBoxTemplate. |
| Dropdown buttons ×4 (regions, playstyle, composition, preset) | :335, :528 | body | I | inh | — | WowStyle1DropdownTemplate. |
| Dropdown menus (Blizzard_Menu) | :351, :532 (SetupMenu) | Menu manager | **B** (Blizzard menu strata, above FULLSCREEN) | B | B | Owned by Blizzard_Menu. Opens over the panel. Menu-entry tooltips are Blizzard_Menu's (:104-). |
| Buttons ×5 (Save, Save as, Delete, Apply, Clear) | :126 | body | I | inh | — | UIPanelButtonTemplate. |
| Copy-label hover frame | :583-587 | body | I | inh (body + 1) | — | Mouse-only frame over a font string, to carry its tooltip. |
| Font strings (labels, readout, unsupported, minutes, Smart) | :117, :257, :294, :384, :447, :579, :789 | body / panel | — (region) | ARTWORK layer | — | No frame level. `f.unsupported` sits on the panel, not the body. |
| MaximizeMinimize button frame | :723-724 | panel | I | inh (panel + 1) | — | Template. Horizontally disjoint from the header click button (`HEADER_CLICK_RT` = 30). |
| Header click button | :738-748 | panel | I | inh (panel + 1) | — | Spans the title band minus 30px at the right. |
| EllesmereUI shell / faded regions / skinned widgets | modules/EUISkin.lua:268-299 (`S.Shell`, `S.Checkbox`, …) | panel and its widgets | I (EllesmereUI decides) | EllesmereUI-owned, unknown | — | Third-party facade. PGFE chooses no strata or level for what `S` creates. |
| EllesmereUI accent ring (per checked box) | modules/EUISkin.lua:103-110 | check button | I | **rel** check button + 3 (`ACCENT_BORDER_LEVEL`, :30) | — | +3 so it clears EllesmereUI's own checkbox border, whose level is EllesmereUI's choice (not verified). |
| EllesmereUI min/max glyph textures | modules/EUISkin.lua:236 | min/max button | — (region) | OVERLAY layer | — | |
| StaticPopup `PGFE_PRESET_SAVE_AS` (with edit box) | modules/Panel.lua:487-500, shown :520 | UIParent (StaticPopupN) | **B** DIALOG | B | B | Launched from the FULLSCREEN panel. |
| StaticPopup `PGFE_PRESET_DELETE` | modules/Panel.lua:501-507, shown :523 | UIParent | **B** DIALOG | B | B | Launched from the FULLSCREEN panel. |
| StaticPopup `PREMADEGROUPSFILTEREXTENSION_RESET_ALL` | settings/Schema.lua:171-186, shown settings/Panel.lua:46 (Reset all settings and the header Defaults button), settings/Slash.lua:181 | UIParent | **B** DIALOG | B | B | From Settings (HIGH) or from `/pgfe resetall` in chat. |
| StaticPopup `PGFE_EUI_SKIN_RELOAD` | modules/EUISkin.lua:410-415, shown :365 | UIParent | **B** DIALOG | B | B | From the euiSkin switch (Settings) or from a profile switch, copy or reset. |
| GameTooltip (panel widgets) | modules/Panel.lua:91-102 | owner = panel widget | **B** TOOLTIP | B | B | `ANCHOR_RIGHT`. Hidden by the stand-down when owned by the panel (:890-901). |
| GameTooltip (settings: euiSkin box, status lines) | settings/Panel.lua:236, :295 | AceGUI widget | **B** TOOLTIP | B | B | |
| Settings canvas pages (landing, General, Profiles) and AceGUI widgets, incl. the 5 InteractiveLabel status lines and 2 TextRow previews | settings/Panel.lua:349, :284-305, :148; settings/Profiles.lua:22 (LibKa0s Options) | Blizzard SettingsPanel | **B** (SettingsPanel, HIGH) | library: OptionsTabs.lua:375-377 (tab panel = body level), :712-714 (tab + 1); Options.lua:589-590 (combat cover, computed) | B | The library picks levels inside the canvas. PGFE sets none. |
| AceGUI colour picker (Region colors tab) → Blizzard ColorPickerFrame | settings/Panel.lua:157 (RenderField) | Blizzard | **B** (Blizzard's choice; not re-verified for this client) | B | B | Opens over Settings (HIGH) in practice. |
| AceGUI read-only EditBox (PGF skin link) | settings/Panel.lua:256-276 | Settings canvas | I | inh | — | |
| Debug console `<name>DebugWindow` | libs/LibKa0s/DebugLog.lua:533-539 (via core/DebugLogSetup.lua) | UIParent | **E** DIALOG (library) | inh; title-bar button + 1 (DebugLog.lua:337) | movable, **clamped**; no toplevel | Library choice. debug-logging says DIALOG "so it sits above the addon's main window". |
| Debug copy window | libs/LibKa0s/Widgets.lua:647-656 | UIParent | **E** FULLSCREEN (library) | inh (UIParent child: low) | movable, **clamped**; no toplevel, no Raise | FULLSCREEN so it sits above the DIALOG console that opens it. |
| Minimap button (LibDBIcon via LibKa0s-Launcher) | core/LauncherSetup.lua:44-58 | Minimap | **B** (LibDBIcon: MEDIUM) | B (LibDBIcon) | B | PGFE picks nothing. |
| Region tags | modules/RegionTags.lua:69-72 | Blizzard Group Finder rows | — | — | — | Text prepended into Blizzard's own font strings. **No frame created.** |

Totals: 1 addon-owned top-level surface (the attached panel) with about 27 child frames, 4 StaticPopup specs, 2
library windows, 1 library minimap button, and 0 frames in the Group Finder.

## Problems

- **PRE-S01: the panel's strata is a hard-coded copy of the host's.** `f:SetFrameStrata("FULLSCREEN")`
  (`modules/Panel.lua:770`) restates `frameStrata="FULLSCREEN"` from PGF's `Dialog.xml:6`. A child created on a
  parent already takes the parent's strata, so the explicit call adds nothing today. If PGF moves its dialog to
  another strata in a later release, the call turns into a fault: the panel stays FULLSCREEN and floats above (or
  below) a dialog it is meant to be part of, and the frame-level raise (`ABOVE_DIALOG`) is meaningless across
  strata. The intent is "same strata as the dialog", and the code says "FULLSCREEN".
- **PRE-S02: the frame level is a one-time snapshot (theoretical).** `f:SetFrameLevel(dialogLevel + ABOVE_DIALOG)`
  (`modules/Panel.lua:771-772`) runs once, at the lazy build, and is never re-asserted on show
  (`Panel.UpdateVisibility`, :841-853). PGF's dialog is not toplevel, so the client does not re-raise it, and nothing
  in PGF calls `SetFrameLevel` on it. Whether a later `SetFrameLevel` on the dialog (by a skin or another addon) would
  carry the panel along is client behaviour this review did not verify; the panel is the dialog's child, so it may
  well follow. **No observed defect.** Recorded so the band is documented (S07), not as a fix candidate.
- **PRE-S03: the preset popups sit a strata below the panel that opens them.** *Save as* (with an edit box) and
  *Delete* are StaticPopups, at DIALOG strata, launched from a FULLSCREEN panel (`modules/Panel.lua:487-507,
  520, 523`). FULLSCREEN is above DIALOG, so wherever the popup and PGF's dialog or the panel overlap, **the popup
  draws under them**. StaticPopup1 anchors at screen TOP, about −135, centred, about 320-420px wide; PGF's 300px
  dialog hangs off `PVEFrame`'s top-right (or wherever the player dragged it, with `dialogMovable`). Whether they
  overlap depends on resolution, UI scale and PGF's position, so **this needs an in-client confirmation** (owner
  smoke) before any fix. Where it happens, the *Save as* edit box can be partly covered while it holds keyboard focus.
- **PRE-S04: the same inversion is possible for the chat- and profile-launched popups.** `/pgfe resetall`
  (`settings/Slash.lua:181`) and the EllesmereUI reload prompt from a profile switch (`modules/EUISkin.lua:365`)
  open DIALOG popups. When the Group Finder and PGF's dialog are open at that moment, the same overlap applies.
  From the Settings panel itself (HIGH) both are correct. Lower impact than S03, because these are not launched
  *from* the FULLSCREEN surface.
- **PRE-S05: the debug console sits below the addon's own surface.** The console is DIALOG
  (`libs/LibKa0s/DebugLog.lua:536`). The standard's reason for DIALOG, "so it sits above the addon's main window"
  (debug-logging), does not hold for PGFE, whose only surface is FULLSCREEN. With the Group Finder open, the console
  (default `CENTER +220,−80`) can be overlapped by PGF's dialog and the attached panel, which is exactly the surface
  you are debugging. Developer-facing only.
- **PRE-S06: the copy window ties with the panel's strata and loses on level.** The copy window is FULLSCREEN
  (`libs/LibKa0s/Widgets.lua:653`), the same strata as the panel, and as a UIParent child with no toplevel and no
  `Raise()` it gets a low default level. The panel is at dialog level + 5. Where they overlap (the copy window opens
  at screen CENTER), the copy window draws **under** the attached panel and PGF's dialog. Developer-facing only.
- **PRE-S07: there is no single statement of the panel's level band.** The z-order inside the panel rests on three
  magic numbers in two files: `ABOVE_DIALOG = 5` (`modules/Panel.lua:46`), `sinkToParentLevel` = +0
  (`:632-635`) and `ACCENT_BORDER_LEVEL = 3` (`modules/EUISkin.lua:30`), plus template defaults (+1). Each is
  justified locally. Together they are an undocumented band (panel L; header art L; body, min/max and header click
  L+1; widgets L+2; EllesmereUI ring widget+3), and a future child can tie with one of them without anyone noticing,
  which is the failure mode the :42-45 comment records.
- **PRE-S08: the EllesmereUI accent ring's +3 is calibrated against a level PGFE does not control.** `S.Checkbox`
  creates EllesmereUI's own border frames at a level EllesmereUI chooses. +3 works today (owner-verified look) but is
  not derived from anything (`modules/EUISkin.lua:103-110`). Low risk, and a ring under the skin's border would be
  visible at once.
- **PRE-S09 (accepted, inherited): the panel covers the Settings panel when both are open.** The panel is FULLSCREEN
  and the SettingsPanel is HIGH, so when the Group Finder stays open under `/pgfe config`, Settings shows with PGF's
  dialog and the attached panel drawn over it. (Whether opening Settings closes `PVEFrame` first was not verified;
  if it does, this never occurs.) This is by design: the panel must match PGF's dialog
  (`docs/ARCHITECTURE.md:445`, Documented deviations, the standalone-windows / library-stack-§8 / options-ui-§15 row:
  "an extension surface must read as part of the host window it attaches to"; that row covers chrome and visibility
  but does not mention strata), and PGF itself does the same. **No change proposed.** Recorded so that the upstream
  rule allows "inherit the host's strata" as a legitimate class.

No problem found with: tooltips (TOOLTIP, owned and hidden correctly, stand-down handled at :890-901), dropdown menus
(Blizzard_Menu above the panel), the header art and body split (the body starts below the clip seam, and the clips
are deliberately at the panel's level), the min/max and header-click pair (disjoint rects at equal level), region
tags (no frames), and the minimap button (LibDBIcon's own layer).

## Proposed strata map

The addon's intended layering, lowest to highest. "Host" means PGF's dialog, `PremadeGroupsFilterDialog`.

| tier | strata | level band | elements |
|---|---|---|---|
| T0 Minimap | MEDIUM (LibDBIcon) | LibDBIcon's | minimap button. Not PGFE's to choose. |
| T1 Settings | HIGH (Blizzard SettingsPanel) | library-managed (OptionsTabs, combat cover) | landing, General, Profiles canvases and their AceGUI widgets. Not PGFE's to choose. |
| T2 Settings-launched modals | DIALOG | Blizzard | reset-all popup and EllesmereUI reload popup **when launched from Settings with no Group Finder open**, ColorPickerFrame. Correct above T1. |
| T3 Host-attached surface | **= host's strata** (FULLSCREEN today), read from the host, never restated | host level + 5 = **L** | the attached panel |
|  | | L + 0 | header art clips and NineSlice copies (deliberately at the panel's level) |
|  | | L + 1 | body, MaximizeMinimize, header click button, template children |
|  | | L + 2 | body widgets (checks, edit boxes, dropdown buttons, buttons, hover frame) |
|  | | widget + 3 | EllesmereUI accent ring (above EllesmereUI's own checkbox art) |
| T4 Modals launched from T3 | **FULLSCREEN_DIALOG**: one strata above the surface that opens them | Blizzard | preset *Save as* / *Delete* popups, and any PGFE popup shown while T3 is visible |
| T5 Menus | FULLSCREEN_DIALOG (Blizzard_Menu) | Blizzard | dropdown menus. A T4 popup and a menu never coexist in practice: the popup is opened by a button click, which closes any open menu. |
| T6 Developer windows | at least T3 + 1 strata when the addon's surface is FULLSCREEN | library | debug console, copy window (above the console). Upstream decision (Z05). |
| T7 Tooltips | TOOLTIP | Blizzard | GameTooltip |

The rule this map encodes: **a modal or developer window is at least one strata above the surface that opens it,
and an attached surface takes its host's strata by reading it, not by repeating it.**

## Proposed changes

| id | change (file:line, from → to) | reason | confidence |
|---|---|---|---|
| PRE-Z01 | `modules/Panel.lua:770`: `f:SetFrameStrata("FULLSCREEN")` → `f:SetFrameStrata(dialog:GetFrameStrata() or "FULLSCREEN")` (guarded like `dialogLevel` at :771). An equally valid form is to delete the call and let the child take its parent's strata at creation; pick whichever the in-client check confirms keeps PGF's bottom border under the panel. Update the header comment (:8-12) to say "the dialog's strata". | Same result today, and it still holds if PGF changes its strata. States the real intent, "layer with the host". No interaction changes: tooltips, menus and popups keep their own strata. Fixes S01. | 70% |
| PRE-Z03 | One host helper, `NS.ShowPopup(name, ...)` in `core/`, used by every PGFE `StaticPopup_Show` site (`modules/Panel.lua:520, :523`, `settings/Panel.lua:46`, `settings/Slash.lua:181`, `modules/EUISkin.lua:365`): it shows the popup, and while `NS.Panel.frame` is shown it records the returned frame's current strata and raises it to `FULLSCREEN_DIALOG`; each PGFE dialog spec gets an `OnHide` that puts back **the recorded strata** (not a hard-coded "DIALOG"). Better, if the library adds it: a LibKa0s confirm/prompt dialog with a `strata` option, so PGFE need not touch a shared Blizzard frame. **Gate: only after the owner confirms S03 in client.** | Puts the popups above the FULLSCREEN surface that opened them, so the edit box is never under PGF's dialog. The restore matters because `StaticPopupN` frames are shared with every other caller, and leaving one raised would change other addons' and Blizzard's popups. Restoring the recorded value rather than "DIALOG" survives a client or skin that uses another default. Merges the original Z03 and Z04 into one helper. Fixes S03, S04. | 50% |
| PRE-Z05 | Upstream (LibKa0s DebugLog / Widgets): let the DebugLog descriptor take `strata` (default DIALOG) and keep the copy window above the console. PGFE's `core/DebugLogSetup.lua` then passes `strata = "FULLSCREEN_DIALOG"`. "One above" FULLSCREEN_DIALOG would be TOOLTIP, which is wrong for a window, so the library has to decide that case: the copy window stays in the console's strata and opens at a higher frame level (or toplevel). Not a PGFE-local change. | The debug console and its copy window should never sit under the surface they are debugging. Developer-facing only, so low priority. Fixes S05, S06. | 40% |
| PRE-Z06 | `modules/Panel.lua:37-50`: gather the level offsets into one documented block, `LEVEL = { ABOVE_HOST = 5, HEADER_ART = 0 }`, with a comment giving the band (L / L+1 / L+2 / widget+3). `modules/EUISkin.lua:30` refers to it for `ACCENT_BORDER_LEVEL` with a "relative to the check button" note (EUISkin loads after Panel in the TOC, so the table exists at its load). No numeric change. | Makes the band one readable statement, so a new child cannot silently tie. Fixes S07 (and documents S08). | 55% |
| PRE-Z08 | No change for S09. Record it in `docs/ARCHITECTURE.md` → Documented deviations (owner-ratified register) as "strata inherited from the host dialog (FULLSCREEN), which therefore covers the Settings panel when both are open". | The deviation is real and intended, so it should be written down; the row needs the owner's ratification like the others. | 65% |

### Considered and rejected

- **PRE-Z02 (was 60%, now 35%): re-assert strata and level on every show through a `layerWithDialog` helper.** S02 is
  theoretical (no observed defect, and the panel is the dialog's child, so it may follow a re-level anyway). The fix
  also carries a real risk: the header art clips and NineSlice copies were sunk to the panel's level once, at build
  (`sinkToParentLevel`, :632-642), and the EllesmereUI accent rings were set to check button + 3 once
  (`EUISkin.lua:108-109`). Re-levelling the panel on show without re-sinking those children could leave the header
  art under the panel's own background, breaking the collapsed look that the sink exists to protect. Revisit only
  if a re-level is ever observed.
- **PRE-Z04 as a separate change:** folded into Z03's single helper; a second gated copy of the same raise/restore
  is a second place for the rule to drift.
- **PRE-Z07 (30%): derive the accent ring as `max(ellesmereBorderLevel, cb) + 1`.** +3 works and is owner-verified;
  deriving it is only worth doing if EllesmereUI's `S.Checkbox` changes.
- **Lowering the attached panel below DIALOG** so the stock popups win: it would break the panel's match with PGF's
  dialog (S09's ratified premise) and let PGF's FULLSCREEN dialog draw over the panel's title strip.

## Notes for the upstream guidance

- **Attached surfaces inherit, never restate.** A frame grafted onto another addon's or Blizzard's frame takes the
  host's strata by reading it (`host:GetFrameStrata()`) or by not setting one. It raises its level by a named offset
  over the host, the smallest offset that clears the host's own border and children. PGFE is the collection's case
  (`modules/Panel.lua:769-772`).
- **Modals go at least one strata above their launcher.** StaticPopups are DIALOG, so a DIALOG popup launched from a
  FULLSCREEN surface draws under it. The guidance should name the pairing (surface strata → minimum modal strata).
  It should also warn that `StaticPopupN` frames are **shared**: a host that raises one must restore the value it
  found on hide, or every later caller inherits the raise. This is a strong candidate for a LibKa0s prompt/confirm
  helper with a `strata` option, so no addon touches a Blizzard popup frame.
- **The debug console's strata premise needs a qualifier.** debug-logging says DIALOG "so it sits above the addon's
  main window". That holds for MEDIUM/HIGH windows and fails for an addon whose surface is FULLSCREEN (PGFE) or
  FULLSCREEN_DIALOG. Suggest: the console's strata defaults to DIALOG, the descriptor may raise it, the copy window
  is always above the console, and an addon whose surface is at or above DIALOG **SHOULD** raise it (developer-facing,
  so SHOULD rather than MUST).
- **Write the level band down where the frames are built.** Tie-breaking by frame level is fragile when it is a set
  of local magic numbers. PGFE's own comment (:42-45) records a real tie that produced a random draw order. A rule
  that every explicit `SetFrameLevel` names its offset in one per-addon constant block, with the band in a comment,
  would have caught it.
- **Deliberately sunk children are legitimate, and couple to any re-level.** `sinkToParentLevel` (+0) exists to stop
  art children tying with the template's interactive children at +1. The guidance should allow "level = parent" for
  non-interactive art and say why, so an audit does not flag it as a missing raise, and should say that any code
  that later re-levels the parent must re-sink those children in the same place.
- **Region-tag style decoration creates no frames.** Text written into Blizzard's own font strings has no strata
  question at all. Worth noting as the lowest-risk way to annotate Blizzard UI.

## Review

Independent review against the code at `master` e5b741a and the installed PGF `UI/Dialog.xml` / `Dialog.lua`
(2026-10-24). Changes made to this file:

- **Inventory corrected.** PGF's dialog is a child of `PVEFrame` (`Dialog.lua:33`) and can be dragged when PGF's
  `dialogMovable` is on (`:88-110`); the original said only "anchored at PVEFrame TOPRIGHT". Added that the
  EllesmereUI skin re-anchors the panel flush (`SHELL_GAP` 0), so the border overlap and the tie `ABOVE_DIALOG`
  guards against exist only in the Blizzard look. Added the header Defaults button as a reset-popup launcher, the
  settings status lines and previews to the canvas row, "no toplevel / no Raise" on the two library windows, and
  marked the ColorPickerFrame strata as unverified rather than asserting DIALOG. Fixed the accent-ring range
  (:105-109 → :103-110) and the deviation-row citation (`docs/ARCHITECTURE.md:445`, which also cites
  library-stack-§8). Confirmed there is no `SetToplevel` anywhere in PGFE.
- **S02 rewritten as theoretical** (its claim that a dialog re-level "leaves the panel where it was" was not
  verifiable and contradicts the panel being the dialog's child) and **Z02 moved to *Considered and rejected* (60% →
  35%)**: re-levelling the panel on show without re-sinking the header art and accent rings could break the collapsed
  header look.
- **S03 now requires an in-client confirmation** before a fix: the overlap depends on resolution, UI scale and PGF's
  movable dialog.
- **Z03 and Z04 merged** into one helper covering all five `StaticPopup_Show` sites (the original Z04 missed
  `settings/Panel.lua:46`), restoring the **recorded** strata on hide rather than a hard-coded "DIALOG"; confidence
  50%. Checked the interaction: a FULLSCREEN_DIALOG popup ties with Blizzard_Menu menus, but a popup is opened by a
  button click that closes any open menu, and tooltips stay above at TOOLTIP.
- **Z01** now offers "delete the call" as the equivalent form (75% → 70%). **Z05** marked upstream-only and
  developer-facing (40%). **Z07 (30%)** moved to *Considered and rejected*, plus a rejected "lower the panel below
  DIALOG" option. **Z08** notes the deviation register is owner-ratified (70% → 65%).
- Upstream notes: debug-console raise softened to SHOULD (developer-facing), and the sunk-children note now says a
  parent re-level must re-sink them.
