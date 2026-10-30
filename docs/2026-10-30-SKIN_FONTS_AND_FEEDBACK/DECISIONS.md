# Decisions: skin fonts and feedback (LibKa0s v1.82.0)

Owner rulings are marked **(owner)**. The rest are the lead's, taken from the M0 inventory (`inputs/inventory/`,
reports A to K and the critic Z). The plan follows these. A later change goes in `99_REPORT.md`, never here.

## Fonts

- **D-01 Ship all three faces (owner, 2026-10-30).** The owner answered the license finding: Expressway Regular is
  "free for commercial use under the Typodermic Desktop License" (dafont.com/expressway.font), and Prototype ships
  with its `Prototype.txt`. LK-01 takes both from their public distributions (dafont), not from the owner's pack:
  Expressway **Regular** with the Typodermic license text, Prototype with `Prototype.txt` verbatim. If the
  distributed Expressway differs from the pack's Bold cut, the distributed one ships and the sizes in LK-05 are
  measured on it. Fira Sans Medium comes from google/fonts at the commit `tools/artwork/fonts.py` already pins
  (same build as the shipped SemiBold). Each license file ships beside its font; `test_media`'s OFL check learns
  the two non-OFL terms by name.
- **D-02 Faces per skin.** Ka0s Default: Prototype for body, titles and HUD. Obsidian: Expressway for all three.
  WoW Forever: Fira Sans Medium for body, Fira Sans SemiBold for titles and HUD (the heavier-HUD rule R-4; critic
  C3). The other skins keep their faces.
- **D-03 Delete what no skin uses (item 7).** Ka0s Inter, Ka0s Inter SemiBold, Ka0s Oxanium SemiBold, Ka0s Oxanium
  Bold, Ka0s Fira Sans (Regular), after a grep over all 17 trees proves nothing names them. JetBrains Mono stays
  (the mono role). No migration: no released addon shipped them, and an unknown saved font already falls back to
  the skin's face. `tools/skin_gallery.py` and QuickComms' copy of the HUD face move with it.
- **D-04 Language masks from the shipped bytes' cmap.** Prototype and Expressway are Latin only, so `western`.
- **D-05 Real Friz Quadrata is unmeasured.** On the owner's client `Fonts/FRIZQT__.TTF` is byte-identical to
  Prototype (critic C1). WoW Default's sizes stay; an issue asks for a real-Friz measurement (IS-07).

## Outline and font settings

- **D-06 The outline setting (owner).** A Skin-tab choice, `skin.outline` in each addon's profile: **All text**
  (default), **HUD text only**, **Off**. The flag is OUTLINE. It never outlines the mono role (critic C4). Ignore
  fonts greys it out and wins. Copy to every Ka0s addon carries it.
- **D-07 Every addon stores font flags, and every font setting is the minimum set (owner).** Each font setting in
  every addon comes with size, color (with a class-color option), flags and shadow; more is allowed. The flags
  setting gains a **From skin** value, the default for every element, which resolves through `skin.outline`
  (All or HUD: OUTLINE; Off: none). A flag the player picked wins. MultiMeters and DpsRace gain stored flags.
  LibKa0s supplies the resolver and, if no composite exists yet, a font-group helper that builds the set. The
  standard makes the set a MUST (WS-01).

## Sizes (item 5)

- **D-08 Width parity, Ka0s Default the baseline.** Body and title sizes per skin are re-measured on the shipped
  bytes **with outline on** (D-06 is the default) so each skin's text is as wide as Ka0s Default's (Prototype
  12 / 14). Report C's method (per-glyph pixel snapping, six scale models). A LibKa0s test pins the ratios.
  High Contrast loses "larger text" from its description.
- **D-09 HUD sizes scale too (owner).** A per-skin HUD size factor (`HUD_SIZE`), applied through a new
  `S.HudFontSize` wherever an element uses the skin's font. It scales the stored size; the stored value is never
  rewritten.

## Skin tab (items 1, 6)

- **D-10 A skin change resets both overrides (item 1).** `lib.__chooseSkin` clears font and texture when the drawn
  look changes (`DrawsKey` before and after), from the tab, the picker (preview clears, close restores, Apply saves)
  and Apply to all. Never inside `Skin:SetChoice` (it runs at login). `/xx set skin.skin` stays a raw write.
- **D-11 Layout (item 6).** Reset font and Reset texture as a row of two half-width buttons under the dropdowns,
  each disabled while its half is the skin's own. The Scope check boxes go half width (0.492) to line up with the
  dropdowns above; Copy to every Ka0s addon gets its own heading, "Other Ka0s addons"; the description line moves
  to the Look section. The two icons at image-30's right are the page's stock scroll bar: no change.

## Anchors and markers (items 9a, 11)

- **D-12 Drag-strip titles fit (owner: fix now).** The drag handle re-measures its title on every skin repaint,
  with 2 px slack, and measures on a host carrying the strip's own font. Addons that size their strips themselves
  (AuraMaster's shortened name cache) get a re-fit hook. One LibKa0s tracker issue checks every addon's anchors
  once the sizes are frozen (IS-03).
- **D-13 The simulation placeholder anchor goes (item 11).** It is KickCD's floating `SimStrip`, the only strip that
  floats over a HUD. KickCD drops it and builds its step panel with `close = false`, so the panel stays the
  on-screen sign. The window addons' cyan bands stay (they are window chrome, not anchors; owner ruling
  2026-10-23). Standard: no simulation marker floats over a HUD display.
- **D-14 AuraMaster's TEST marker goes (item 9a).** The standard's test-mode marker MUST becomes a MAY for HUD
  displays (AuraMaster containers, KickCD grids); windows keep the MUST (DpsRace's race HUD strip and DropWatcher's
  compact chrome are windows and keep theirs). The unlocked drag strip's TEST tag stays.

## Per-addon fixes

- **D-15 AuraMaster/KickCD glow (owner).** A one-time migration turns "Use the skin's font" off on every element
  that stored a font other than the skin's own HUD face (the owner's Ka0s Kait picks), so the stored face and the
  earlier glow come back. The glow code does not change.
- **D-16 `/xx skin` (item 12).** `O.SkinVerb(spec)` in the library (OptionsSkinPicker minor 3) opens the new-profile
  picker whatever `pickerSeen` says; refused while the addon is disabled; in combat a gray refusal on every call;
  no arguments. Each addon adds a `skin` row after `config`, `NS.RunSkinVerb`, and `SkinVerb` on its Options stub.
  Reserved verb, a MUST for every skinned addon.
- **D-17 Conditional sections (item 10).** OptionsWidgets gains `shownWhen = { any = {...} }` (OR across dropdowns).
  OptionsWidgets is 1447 lines, so it is split first if the change would cross the cap. DropWatcher hides the
  Pixel border / Auto cast / Button / Proc sections unless either style dropdown selects them; a glow turned off
  still opens its section (greyed). The standard gains the MUST (options-ui), naming `shownWhen`.
- **D-18 DropWatcher defaults.** Proc for both glows; main spec #19FF19, off-spec #3FC7EB. AceDB defaults carry
  existing profiles that never chose; no migration. Situations columns `{8, 128, 188, 262, 424}`, dropdowns 150.
- **D-19 Characters (item 5b).** Fix only what a shipped face cannot draw: the 7 sites in LootHistory and BankLedger
  (`≈` to `~`, `→` to "to", the BankLedger tooltip's `▼▲` dropped, LootHistory's Transfer `⇄` to `↔`, drawn by
  mono). A test-kit helper fails a display string carrying a character outside the safe set; the standard gains
  the allowed set, derived from the shipped faces (critic C11).
- **D-20 PGFE expand/collapse (item 8).** A chevron texture from the shipped icon set, tinted from tokens, with an
  explicit size and anchor in the title band, the same in every skin.
- **D-21 QuickComms (item 15).** The four test groups get numbered glyphs (`ph:number-circle-one`..`four`, tinted).
  A group or callout with no icon draws `ph:folder-simple` / `ph:chat-circle-dots`, the "?" only without the
  library. The animation request is a comment on the existing #13 (each surface on its own), not a new issue.

- **D-25 Arm Race contrast (owner item 16).** The label is dim in three skins, so the cause is most likely the
  library's accent-button label color, not DpsRace. LK-14 finds it and fixes the label for every skin and every
  accent button (a guard test on label-to-fill contrast in all skins). If the cause is DpsRace's own (it disables
  or recolors the button while idle), LK-14 lands as an exception with proof and DR-02 fixes it there.

## Issues (M3, spaced out)

- **D-22** IS-01 LibKa0s: conditional sections across every addon + the standard MUST. IS-02 DropWatcher: stacked
  toasts (needs Toast minor 2). IS-03 LibKa0s: anchor width check in every addon. IS-04 MultiMeters: Insights view.
  IS-05 MultiMeters: bar animations (rank slide, enter/leave, change pulse; #23's fill slide is done). IS-06
  QuickComms #13 comment. IS-07 LibKa0s: measure real Friz Quadrata for WoW Default's sizes.

## Mechanics

- **D-23 One minor per library file per release**, and one re-vendor commit per addon carries every stub and
  facade the tag needs (SkinVerb, HudFontSize, outline), so no addon suite is red between commits.
- **D-24** Branch `feat/2026-10-30-skin-fonts-feedback` in every touched repo, from master.
