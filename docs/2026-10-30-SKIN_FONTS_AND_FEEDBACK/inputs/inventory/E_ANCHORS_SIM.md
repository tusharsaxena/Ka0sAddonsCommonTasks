# E_ANCHORS_SIM: drag-strip title truncation and the simulation placeholder strip (item 11)

Read-only inventory, 2026-10-30. Trees read on `feat/2026-10-30-skin-library-followups` (LibKa0s at
`aefeba9`, v1.81.0). Screenshots: image-43/44/45 show KickCD's Focus and Target strips truncated
("Ka0s KickCD — Fo...", "— Ta...") under three skins. image-46 shows two floating cyan-flavor strips
reading "Simulation: Mythic+ pull, several ki..." (KickCD's `pull` scenario,
`KickCD/modules/SimScenario.lua:186`, `locales/enUS.lua:243`), one per grid.

## (a) The drag strip's title truncates

### The widget

`LibKa0s/LibKa0s/WidgetsDragHandle.lua` (minor 7) is `lib.DragHandle`, the strip with the "?" help mark.

- The label is bounded on both sides at the reserve and does not wrap, so it truncates with "..." when
  the strip is narrower than the text (`dhBuildLabel`, :619-633: LEFT `+reserve`, RIGHT `-reserve`,
  `SetWordWrap(false)`, `SetMaxLines(1)`).
- Width is the host's call, never the widget's. `Measure()` = `dhLabelWidth + dhReserve*2` (:697-699).
  `ApplyWidth(minWidth)` = `max(Measure(), minWidth)` and `SetWidth` (:710-714). `SetLabel` does not
  re-apply the width (:686-690).
- Measurement is done on a detached FontString per face, `lib.__DragHandleMeasurer` (:231-243). Its
  host frame is **hidden** (`host:Hide()`, :237). `dhLabelWidth` (:258-272) lends the measurer the
  label's skin font object when `lib.__fonted[label]`, then `fs:GetStringWidth()`. The value is not
  ceiled and has no slack.
- On a skin switch, `dhRepaint` (:587-600, hooked through `lib.__onSkin` at :825) re-fonts the label
  (`dhFontLabel` → `lib.__skinFont` → `P.font`, `SkinPaint.lua` ~:545-570, a per-owner font object)
  and recolors it. **It never re-measures or re-applies the width.**

### Root cause (most to least certain)

1. **The width is stale after the face changes (certain).** The face is per skin (body face, scaled
   size, `font.outline` flags), and so is the label's drawn width. The width is fixed at the last
   `ApplyWidth`. KickCD's cast-bar strip measures **once at build** (`KickCD/modules/Castbar_Handle.lua:115`,
   whose comment at :66-74 says "measurement is taken once ... never has to be hooked into Reskin").
   The grid strip measures only on unlock (`IconGrid_Handle.lua:197`). So a skin switch, or an
   "Ignore fonts" toggle, with the strip already sized leaves a width measured in the old face.
   A wider face truncates, as in image-43..45.
2. **The first measure can run before the face is loaded (likely, needs an in-client check).** The
   measurer lives on a hidden frame. The library's own font preload says why that matters: "the client
   may skip work for a hidden or fully transparent region" (`OptionsScroll.lua:572-574`, which parks its
   frame shown, at alpha 1, off-screen). The collection has hit lazy addon fonts before (AuraMaster #24,
   `AuraMaster/core/AuraMaster.lua:126-149` FontPrimer). KickCD calls `ApplyWidth` before `Show()`
   (`IconGrid_Handle.lua:197-198`) and at build (`Castbar_Handle.lua:115`). That is before any visible
   string has drawn the skin face, so the measure can come back in a fallback face. Nothing re-measures
   once the face is loaded.
3. **An exact fit has no slack (minor).** The label's bound equals the measured `GetStringWidth`
   exactly. A fractional width plus pixel snapping, or outline flags, can trip the ellipsis by a glyph
   even when the measure is right.

### Every consumer and how it sizes

| Repo | Call site | Width passed | Effect of a library re-fit |
|---|---|---|---|
| KickCD | `modules/IconGrid_Handle.lua:133`, `:197` `ApplyWidth(0)` on each unlock | natural | fixed |
| KickCD | `modules/Castbar_Handle.lua:92`, `:115` `ApplyWidth(0)` once at build | natural | fixed (today never re-measured) |
| AbsorbTracker | `modules/Bar.lua:135`, `modules/Display.lua:273` `ApplyWidth(barWidth)` per pass | floor = bar width | fixed when the label is wider than the bar |
| ConsumableMaster | `modules/MacroBar.lua:276`, `:444` `ApplyWidth(bar:GetWidth())` | floor = bar width | fixed |
| QuickComms | `core/WidgetsSetup.lua:21-26` wrapper, `modules/Pad.lua:310`, `:514` `ApplyWidth(inst.width or 0)` | floor = pad width | fixed |
| AuraMaster | `modules/Anchors.lua:691`, `placeHandle` :937-958 | **caps** at element width with `SetWidth(w)` when `stripCapped`, else `ApplyWidth(w)` | capped strips shorten on purpose (`stripLabel`/`shortened`, :884-930). Its cache (`container.stripFull/stripAvail`, :927-929) has no face in its key, so a skin switch serves stale shortened text. Needs the hook below. |
| LibKa0sSkinTester | `modules/ShowroomWidgets.lua:71-73` `ApplyWidth(220)` | floor 220 | fixed (the natural width still wins when wider) |

These are not `DragHandle` and are not fixed by a library change. They belong to the per-addon width
issue the owner asked for:

- PartyFrameEnhanced `modules/Anchor.lua:299-312`: a free label above the holder, with a grip sized to it.
- PanelMaster `modules/Unlock.lua:114`, `:231`: a centered label in the overlay, with no bound.

Neither of these truncates by construction. Each can overflow its plate instead.

### Proposed change (LibKa0s, `WidgetsDragHandle.lua` minor 8)

1. **Fit with slack.** In `dhLabelWidth`, prefer `GetUnboundedStringWidth` when the method exists and
   fall back to `GetStringWidth`. Return `math.ceil(w)`. Add `lib.DRAG_HANDLE.FIT_SLACK = 2` to
   `Measure()` (published, like RESERVE).
2. **Measure on a shown string.** Change `__DragHandleMeasurer`'s host frame to `preloadFrame`'s
   shape: shown, alpha 1, 1x1, parked off-screen at `TOPRIGHT` of `UIParent`'s `TOPLEFT`. Then the
   client loads the face it is asked to measure.
3. **Re-fit by itself after the face changes, once the host has sized it.** `ApplyWidth(minWidth)`
   records `self.__fitFloor = minWidth` (and `__fitted = true`). `dhRepaint` then does one of two
   things:
   - when `spec.onRefit` (new, a function) is set, it calls `spec.onRefit(handle)` under pcall;
   - else, when `__fitted` is true, it calls `self:ApplyWidth(self.__fitFloor)`.

   A strip never sized by its host stays unsized, so the born-hidden, no-width contract holds. Also
   re-fit on the strip's `OnShow`, once, one frame later (`C_Timer.After(0)`), to catch a face that
   finished loading after the first measure. `SetWidth` on the strip is not protected, and the measure
   goes through `spec.number`, so this is as combat-safe as the hosts' own calls.
4. **AuraMaster** passes `onRefit = function() placeHandle(container, container:Cfg()) end` (or the
   module's re-place entry point) and adds the skin face (or a skin-switch generation counter) to the
   `stripLabel` cache key.
5. **KickCD** deletes the "taken once ... never hooked into Reskin" rationale
   (`Castbar_Handle.lua:66-74`), because the library now re-fits.

Tests (LibKa0s `tests/test_widgets_draghandle.lua`, `tests/test_widgets_skin.lua`, with
`fixture_draghandle.lua`'s `stubMeasurer` made face-aware):

- A skin switch re-fits a fitted strip to the new face's width.
- A strip that was never fitted is not sized by a switch.
- `onRefit` replaces the default re-fit.
- `OnShow` re-fits once.
- The measurer's host is shown and off-screen.
- Ceil + `FIT_SLACK` is in `Measure()`.
- Update the pinned exact widths: 88 at :267-268, :302-303 and :638, `11*6+58` at :314, and
  `RESERVE*2` at :323.
- AuraMaster: a test that its capped label recomputes after a skin switch.

Docs:

- A `docs/api/Widgets/` version doc for the new minor. The latest is `version-17.3.7.5.5.2-docs.md`,
  which pins DragHandle 7.
- CHANGELOG and the CONSUMERS row for `onRefit` / `FIT_SLACK`.
- Re-vendor all 7 consumers.

### Risks

- A strip that grows wider after a switch can run over a neighbor. AuraMaster's `stripOverhang` and the
  side-room reads depend on the width, which is why AuraMaster gets the hook rather than a silent
  `ApplyWidth`.
- `OnShow` + `C_Timer.After` adds one closure per show. Keep a single reusable closure per handle.
- `GetUnboundedStringWidth` is absent in a headless mock. Guard on the method.

### Open questions

1. **Slack size.** Recommendation: 2 px, published, not per host.
2. **Default re-fit on, or opt-in?** Recommendation: on for every fitted strip. Six of the seven hosts
   want it, and AuraMaster opts into the hook.
3. **Bundle the per-addon width issue** (owner: "check every anchor's width in every addon once the
   fonts are frozen")? Recommendation: one issue per addon with a mover (the 7 above plus
   PartyFrameEnhanced and PanelMaster), filed after the font freeze.

## (b) The simulation placeholder strip

### What it is

`lib.TestStrip(parent, { kind = "sim" })` (`LibKa0s/LibKa0s/Widgets.lua:756-845`, flavor since Widgets
minor 14 / v1.76.0) is the cyan mode strip. The thing in image-46 is **KickCD's HUD use** of it,
`KickCD/modules/SimStrip.lua` (KC-09, KickCD#38):

- one strip per enabled grid, **parented to UIParent** (:65), floating BOTTOM-to-TOP of the grid or
  its unit label (:86-104), or at `CENTER 0,180` when no unit is enabled (:96);
- width `max(220, grid width)` (:31, :102), so the text truncates too;
- text `"Simulation: %s - /kcd sim stop ends it."` (:134, `locales/enUS.lua:105-107`) with the `info`
  icon (:71);
- driven from `modules/Sim.lua:225` (start), `:382` (stop) and `:410`;
- placed in the HUD band by `core/Constants.lua:264`, `:280` (`HUD.MARKER = 41`).

Because the grid hides between casts (`target_casting`) and the strip deliberately does not, a
player sees cyan bars floating with nothing under them. That is the "placeholder anchor".

### Every sim-strip host

| Repo | Where | Kind of surface |
|---|---|---|
| **KickCD** | `modules/SimStrip.lua` (HUD, floating over the grids) | **HUD overlay: the one in image-46** |
| BankLedger | `modules/Browser.lua:871-873`, `:1164`; `modules/SessionWindow.lua:484-512` | in-window band under the filter bar / title |
| LootHistory | `core/WidgetsSetup.lua:314-316`, `modules/Browser.lua:938-1055` | in-window band |
| MultiMeters | `modules/Window.lua:728` (beside the test strip at :571) | in-window band |
| DropWatcher | `core/WidgetsSetup.lua:78-80`, `modules/Window.lua:460-461`, `modules/CompactChrome.lua:380` | in-window band (DW-10) |

KickCD is the only host whose sim strip floats over a HUD display. The other four are window chrome,
under the standard's "one marker per mode on screen" rule.

### What the standard requires

- `standards/standards/preview-mode.md:51`, *The in-game simulator*:
  - the session **MUST** be marked on the display, and the step panel on screen satisfies this;
  - a window that marks test mode with the strip **SHOULD** mark a sim with `kind = "sim"`.
- `standards/standards/standalone-windows.md:46` and the bullet after it: the two flavors, one strip per
  kind at one anchor, and no header word while a strip shows.
- `standards/standards/frame-layering.md:57`: the layering of a displacing or covering test/sim strip.
- `standards/AUDIT.md:1042-1044`: the missing sim strip is a **SHOULD** finding, and #97.
- `NEW_ADDON_CONTEXT.md:1662` (item 18), `EXECUTIVE_SUMMARY.md:22`, `CHANGELOG.md:71` (v2.87.0, origin).

Nothing in the standard requires a sim strip on a HUD display. KickCD's is a choice beyond the
SHOULD, which covers windows with a test strip only.

### Does removal lose anything?

- **Stop.** The strip has no stop button, only the hint text "/kcd sim stop ends it." The library's
  step panel (`SimPanel.lua`) has the scenario title, every step, a Stop row (`stopRow`, :664-667,
  `PANEL_STOP`) and Pause/Resume/Restart/Stop controls (:37-39, :507). KickCD docks the panel beside
  the grid at start (`KickCD/modules/Sim.lua:226-227`). The step panel satisfies the MUST.
- **Gap:** the panel's close mark hides only the panel (`SimPanel.lua:266`, `panel.Hide`). After that
  nothing on screen says a session runs. That was the strip's real job. Options are in Q2.

### Proposed change

**Recommended (A): remove the HUD sim strip; keep the in-window bands.**

- KickCD:
  - delete `modules/SimStrip.lua` and its TOC line (`KickCD.toc:162-164`) and the three calls in
    `modules/Sim.lua` (:225, :382, :410);
  - delete the locale string (`locales/enUS.lua:105-107`) and `HUD.MARKER` (`core/Constants.lua:264`, :280);
  - delete `tests/test_sim_strip.lua` and the SimStrip references in `tests/test_layers.lua` and
    `tests/test_skinsetup.lua`;
  - drop `info` from the `LibKa0s icons:` line (`CLAUDE.md:43`; `SimStrip.lua:71` is its only user) and
    prune `media/icons/info.*` with the tag's `tools/prune-icons.lua`;
  - update the docs: `docs/ARCHITECTURE.md`, `module-map.md`, `icon-grid.md`, `message-bus.md`,
    `testing.md`, `test-cases.md`, `smoke-tests.md`.
- LibKa0s: no code change needed. Document in `TestStrip`'s API doc that the sim flavor is window
  chrome, not a HUD overlay.
- Standard (minor bump): add to preview-mode *The in-game simulator* a **SHOULD NOT**: "a display that
  is not a window (a HUD bar, grid or icon) SHOULD NOT carry a sim strip or any floating marker; the
  step panel is its marker". Ripple it to `frame-layering.md:57` (drop "sim" from the covering case if
  no host is left), `AUDIT.md:1044`, `NEW_ADDON_CONTEXT.md` item 18, anti-patterns #97 (name the
  floating marker), `EXECUTIVE_SUMMARY.md`, CHANGELOG.

**Alternative (B): remove the sim flavor everywhere, library included.**

- Widgets minor bump to drop `kind = "sim"`, plus 4 more addons (BankLedger, LootHistory, MultiMeters,
  DropWatcher).
- Each of those must put a cyan header word back, because the one-marker rule says the header word is
  the marker where no strip shows. That reverses the 2026-10-23 owner request (`CHANGELOG.md:71`).
- Retire the SHOULD at preview-mode:51 and the standalone-windows flavor bullet.

Far larger, and it contradicts an earlier owner ruling. Not recommended unless the owner confirms
"every addon" means the window bands too.

### Risks

- Under (A), a session whose step panel is closed has no on-screen marker (see Q2).
- `tests/test_disabled.lua` registration sets: SimStrip held no idle registrations (`SimStrip.lua:23-24`),
  so no change is expected. Re-run the suite.
- The KickCD#38 / KC-09 history should record that the strip was withdrawn at the owner's request.

### Open questions

1. **Scope of "every addon that has it."** Is it only the HUD placeholder (KickCD, the only one), or
   also the in-window cyan bands in four addons? Recommendation: (A), KickCD only. image-46 is the HUD
   case, and the window bands answer a ruling the owner made on 2026-10-23.
2. **The marker after the step panel is closed.** Options:
   - (i) KickCD passes `close = false` to the step panel (`SimPanel.lua:277` honours `d.close ~= false`);
   - (ii) a closed panel re-opens on the next step;
   - (iii) accept it, since `/kcd sim` status still answers.

   Recommendation: (i). It is one descriptor field, and it keeps the MUST true for the whole session.
3. **Fold the "/kcd sim stop ends it" hint into the panel's title or footer?** Recommendation: no. The
   panel's Stop row already shows the `/kcd sim stop` command (`stopRow` `command = slashOf(P, "stop")`).
