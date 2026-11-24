# The owner's feedback batch of 2026-11-24

Created 2026-11-24 from the owner's feedback batch (title bars, KickCD, Party Frame Enhanced, Outfitter
Reborn, Aura Master, Quick Comms, Skill Master), with the owner's screenshots 33 to 50.

Branch `feat/2026-11-24-feedback-batch` in every repo it touches, cut from `master`. The game client loads
the live checkouts under `GIT/`, so builders work in scratch clones and never write, switch, stash or
commit a live repo. Nothing is pushed, no GitHub write is made, no tag leaves the machine, and no addon
version is bumped.

## The owner's words (2026-11-24, verbatim where quoted)

- **T. Title bars:** "it should not cover window title bars. But window title bars should all have a gear
  icon (on non companion windows). Validate this as a task". The right-click rule (standalone-windows,
  v2.118.0) stays strip-only. New rule: every addon window's title bar carries a settings gear, except on
  companion windows (popups or dialogs that belong to another window, such as a New Outfit dialog or a
  confirm). Define "companion" precisely.
- **K. KickCD** (images 33, 34): "Unit > Text label > font when use class is enabled, it doesnt actually use
  the class color, instead it uses the label color (on my hunter I expect it to be green)".
- **P. Party Frame Enhanced** (images 42-44): Cast Bars > Bar > Fill: "Use class color for fill doesnt seem
  to work, always uses the normal cast color. use the skin color does work". The Text tab has the same
  problem as KickCD's text color. "Seems similar to the KickCD issues… Do the same validation for any
  element (text, bar, etc) where class color/skin color can be applied. This may be systematically
  broken." The precedence the collection already documents: a class color comes first (it has no
  companion), then "Use the skin's color", then the swatch.
- **O1. Outfitter Reborn** (images 35, 36): "With Chonky or whenever there are tabs to the right, the frame
  is shifted contents are shifted a bit to the right. However, the horizontal separator line does not
  extend to the entire frame width as expected, and it looks odd. Do not shift the New outfit button,
  leave it where it is".
- **O2. New Outfit dialog** (images 37, 39-41): "Done button has weird looking fontcolor - fix this. Also
  audit all other buttons across all ka0s addons and fix this across all skins. It should look like this
  (from skin tester)" (image 38: Normal / Primary / Disabled). "This seems to be a problem across all
  skins, as if this button text color is hard coded."
- **A. Aura Master** (images 45-48): "High contrast skin makes the bar container text look really weird
  with an exaggerated shadow. Only happens for AuraMaster". The skin picker, Skin Tester and the other
  addons look fine.
- **Q. Quick Comms:** "Toast does not show in /qc test".
- **S1. Skill Master:** "Add options and top of detached window controls to resize the detached window".
- **S2. Skill Master** (image 49): "Arrow does not show in test mode - in fact it does show, but it seems
  to be disabled by default (probably because i have tomtom installed). Either ways, some arrow should
  show in test mode (either this addons arrow, or tomtom's arrow)".
- **S3. Skill Master** (image 50): "Split Trainers and Waypoint into 2 separate tabs" (the page "Trainers
  and Waypoints" has one tab today).
- **S4. Skill Master** still vendors LibKa0s v1.109.0 and missed the v1.111.0 strip run. Re-vendor the
  newest LibKa0s. Its detached windows are title bands, not strips, so the right-click rule does not
  apply. Check T (the gear) for it.

## Diagnoses

Every claim cites the code the diagnosis read. A builder re-reads the cited lines before changing them,
because the line numbers are from the live trees on 2026-11-24.

### K and P: class color (one shared root, several private ladders)

- **The shared root (LibKa0s).** `Core.lua` `lib.ClassColor` / `lib.ResolveColor` knew only the real
  unit. A preview, unlock or sim frame describing a unit that does not exist (target, focus, party1)
  always resolved nil and fell through. The library shipped no class -> skin -> swatch ladder, so about
  twelve private copies existed and disagreed on the unresolved case.
- **KickCD.** The label resolves the class of the unit it names (`modules/UnitLabel.lua:119-124`, unit
  "target"/"focus"). In unlock or preview with no target, the class is nil. `core/SkinSetup.lua:228-238`
  `NS.SkinHudColor` checks the skin only when `useClass ~= true`, so with the class toggle on and the class
  unresolved it skips the skin and draws the stored gold *Label color*, which is what the owner saw.
  Nothing repaints on a target or focus swap: `UnitLabel.lua:277` registers only PLAYER_ENTERING_WORLD,
  and the cast bar's `ReskinColors` (`modules/Castbar_Skin.lua:421-460`) runs only from `Castbar:Reskin`;
  `OnTargetChanged`/`OnFocusChanged` (`modules/Castbar_Events.lua:43-54`) only re-evaluate.
- **Party Frame Enhanced.** `modules/Element.lua:315-324` `Element.Drawn` has the right precedence. Out of
  a party the cast bar preview (`modules/CastBars.lua:297-310` -> `applyFill` :117-137) draws on "party1",
  which does not exist, so the class is nil and Drawn falls to the skin (works) or the swatch (the orange
  *Normal cast color*, image 42; the white *Font color*, image 44). `TargetFrames.lua:95-104` passes
  `Element.ClassResolver(nil)`, and PetFrames' preview resolves an absent unit. Live, `Element.ApplyColors`
  runs only in `reskinAll` (CONFIG/PROFILE/skin), so a roster change keeps the previous occupant's color.
- **Skill Master.** The skin comes before the class at every site, and every `FromSkin` defaults true
  (`defaults/Profile.lua:46,52,105,146,149,162,169,249`): `modules/BarStyle.lua:48-49` and `:61-62`,
  `modules/Detached.lua:264-265` and `:270-272`, `modules/Rows.lua:125-126`, `modules/TrainerPopup.lua:221-228`.
- **Combat Trail.** `modules/Hud_Appearance.lua:306-313` `paintBackdrop` paints the class/swatch color only
  when `<key>FromSkin ~= true`, so the skin's Card paint wins over the class (box bg and border, window bg
  and border). Every other Combat Trail surface is already class-first.
- **Absorb Tracker.** `core/Data.lua:325-330` `skinColor` returns nil whenever the class toggle is on, so a
  target or focus bar with no target draws the swatch instead of the skin.
- **Range Master.** `modules/Style.lua:59` Class mode resolves the tracked unit (default "target"); in test
  mode with no target it draws the swatch. Lower severity: a mode dropdown.
- **Aura Master** (`Style.Followed`, `modules/Style.lua:89-92`) already falls to the skin and needs no
  change beyond the preview stand-in where it previews a unit.

### O2: a disabled primary button

No color is hard-coded. Outfitter Reborn's New Outfit *Done* is `D.Button(..., { primary = true })`
(`modules/Dialog_Outfit.lua:229`, through `modules/UIDialogs.lua:52-61`) and is disabled while the name is
empty (`Dialog_Outfit.lua:43`), the state in every screenshot. LibKa0s `SkinPaintControls.lua` painted
`text.disabled` while disabled (`buttonLabel`) but `primaryFill` only ever chose `btnPrimary.bg` or its
hover, so every skin drew its dim disabled text on its bright primary fill. Skin Tester never showed it:
its *Disabled* sample is a normal button. The only disabled primaries today are Outfitter Reborn's *Done*
and Combat Trail's remapped style buttons (`ct.primary.off*`, `modules/Style.lua:933-936`), which already
worked around it. No addon leaves a stock template button unrepainted.

### T: the gear and the companion window

`standalone-windows` already said the gear belongs on every window but never defined a companion, so each
addon made its own call. Companions that build the gear (with `hideOnSettings`): Combat Trail's compare,
timeline and gear windows (`modules/Results_Compare.lua:380`, `Results_Timeline.lua:148`,
`Results_Gear.lua:341`), the export modals of Bank Ledger (`modules/Export.lua:406`), Loot History
(`modules/Export.lua:494`) and Multi Meters (`modules/Export_Modal.lua:215-219`), Drop Watcher's rolls and
offer panels (`modules/RollsPanel.lua:473-474`, `modules/OfferPanel.lua:169-170`), Skill Master's trainer
popup (`modules/TrainerPopup.lua:365-370`) and the library's copy window (`WidgetsCopyWindow.lua:227-231`).
Companions already without it through the waiver path (`settings = false` + `settingsOptOut`): Outfitter
Reborn's dialogs (`modules/UIDialogs.lua:45`, `:163-167`), Drop Watcher's note editor
(`modules/DetailCard.lua:728`, `:745-746`), Quick Comms' call-out modal (`settings/ModalWindow.lua:99-112`)
and the library's icon browser. `W.HeaderButtons` (`WidgetsHeader.lua:234-244`) had no way to say
"companion" apart from the waiver. Not companions, and they keep the gear: every primary window, Bank
Ledger's session window, Skill Master's detached and group windows (saved positions, outlive the main
window), the debug console, perf panel, sim panel and skin picker.

### A: High Contrast's HUD shadow

High Contrast was the only skin that set `hud.shadowX = 2, hud.shadowY = -2`
(`LibKa0s/SkinDefsOthers.lua:672`). Aura Master's bar text goes through `Style.ApplyFont` -> `S.HudFont` ->
`prim.HudShadow` and is also drawn OUTLINE (profile default `fontFlags "@skin"`), so a 2 px shadow under an
outlined glyph draws a second solid black copy of every letter (images 45/46). The code path is shared;
Aura Master shows it most because its bars are dense small text over its own bright fills. The 2, -2 reason
(white text over a yellow fill) predates v1.82.0, which turned the HUD outline on by default.

### Q: no toast in /qc test

`P.SetTestMode` (`modules/Preview.lua:48-66`) sends TEST_MODE_CHANGED to Surfaces, Editors and CalloutPopup,
but the auto-thank toast host (`modules/AutoThank_Toast.lua`) never subscribes: its `listen()` (line 298)
registers only RESTRICTION_CHANGED, and its only way in is a real buff from a stranger.

### S1, S2, S3: Skill Master

- **S1.** A detached window's width is fixed (`modules/Detached.lua:295`, `D.WIDTH = 280` at line 23) and its
  height follows content (~line 341). Scale is the only size control. The main window already has
  `NS.Chrome.MakeResizable` plus width/maxHeight rows (`modules/MainWindow.lua:55-130`, `366-389`).
  Merged windows (`modules/Groups.lua:339, 395, 410, 728-733`) do their column math in `NS.Detached.WIDTH`.
- **S2.** `WA.ShowTest` (`modules/WaypointArrow.lua:295-297`) returns at once unless `WA.Wanted()`, which is
  false while *Show Skill Master's arrow* is off. With TomTom installed the owner had reason to turn it
  off. `WA.ApplySettings` (line 326) also clears the sample whenever `Wanted()` is false.
- **S3.** `settings/Trainers.lua:10` registers every row under one `GROUP`, and `RegisterSchemaPage`
  renders one tab per group.
- **S4.** Skill Master vendors LibKa0s v1.109.0. The re-vendor takes v1.112.0. Its detached and group
  windows are title bands, not strips, and already carry the gear; only the trainer popup changes (T).

### O1: Outfitter Reborn's separator

Not diagnosed upstream. With tabs to the right (Chonky, image 35) the outfit window's content is shifted
right, and the horizontal separator above *New outfit* starts at the shifted content edge instead of the
frame's. The builder diagnoses first (the separator's anchors against the frame and the tab gutter), then
fixes the separator alone, and leaves the *New outfit* button where it is.

## Decisions (the lead's calls)

1. **T, the companion window**, is defined by the standard (v2.119.0, standalone-windows, *A companion
   window carries no settings mark*) by three tests: **owned** (it opens only from a control on, or
   attached to, one other frame; no launcher entry, keybind, login or event opens it), **bound** (it shows
   only its owner's content, closes with it and keeps no saved position) and **not a display** (not the
   primary or only window, not a display kept on screen). A `StaticPopup` confirm is always one. A
   companion keeps its close and carries no gear, built with `W.HeaderButtons(bar, { companion = true })`
   (WidgetsHeader minor 2). `settings = false` with a reason stays the waiver for a non-companion. The
   v2.118.0 right-click rule stays strip-only. Outfitter Reborn and Quick Comms move their waiver-path
   companions to `companion = true` in the same run, for one greppable shape.
2. **K and P, one library ladder.** `LibKa0s-Core-1.0` minor 20 adds `standIn` to `ClassColor` and
   `ResolveColor` and the new `FollowColor(stored, classOn, unit, fromSkin, skinReader[, token][, standIn])`:
   a class color that resolved first (stored alpha kept), else the skin's color while its companion is
   on, else the swatch. An unresolved class falls to the skin. A host passes `standIn = "player"` while it
   previews, unlocks or simulates. Each host adopts `FollowColor` or holds its private ladder to the same
   order. The standard writes it down (options-ui-§17, v2.119.0, anti-pattern #125).
3. **O2 is a library fix.** A disabled primary paints the plain `btn.*` box under `text.disabled`
   (SkinPaintControls minor 21), so it looks exactly like Skin Tester's *Disabled*; a host's own `bg`
   remap (Combat Trail) still wins. Skin Tester gains a *Button (primary, disabled)* sample.
4. **A takes the preferred fix:** High Contrast's 2, -2 override goes (SkinDefsOthers minor 11) and every
   skin's HUD shadow is 1, -1. No Aura Master code change; it re-vendors.
5. **Q:** the sample toast shows in `/qc test` whether Auto-thank is on or off, because test mode is a
   preview. Its Thank button is disarmed and sends nothing.
6. **S1:** each detached block gets a stored width (`layout.blocks.<id>.width`, default 280, range 200-600,
   step 10) on Layout > Blocks next to *Block scale*, and a corner resize grip on the window that writes it
   and keeps the drop point. *Locked* refuses the grip. Height keeps following content (no body scroll in
   this run). A merged window's columns use its widest member's width.
7. **S2:** test mode always shows Skill Master's sample arrow, labeled when TomTom is loaded or the arrow is
   off; test mode never writes a TomTom waypoint.
8. **S3:** two tabs, *Trainers* and *Waypoints*, on the same page key `"trainers"`, so Defaults and the
   existing tests hold.
9. **S4:** Skill Master re-vendors v1.112.0, the newest tag.
10. **Release:** LibKa0s **v1.112.0** is tagged **locally** (done, `1f1904ee`); the standard is
    **v2.119.0**, untagged. Every roster addon re-vendors v1.112.0 in this run, so the new rules bind and
    the disabled-primary and High Contrast fixes reach each addon's own copy. Pushing, merging and tagging
    remotely wait for the owner's go-ahead. No addon version bumps.

## Upstream status (2026-11-24)

- **LibKa0s** `feat/2026-11-24-feedback-batch`: `3d348e54` (FB-LK-01..04), `f559e050` and `1f1904ee`
  (FB-LK-REL), `eb83fe29` (FB-LK-03: `HeaderButtons` split under CCN 15 after the first release run measured
  16). Local tag `v1.112.0`. Release run `docs/automated-tests/20261124-012313/`: lint 0/0 in 386 files,
  5155 passed, 0 failed, 3 skipped (5158), complexity 0 over CCN 15, perf skipped; also 5155/0/3 under
  `KA0S_KIT_CLIENT=forever`.
- **WowAddonStandards** `feat/2026-11-24-feedback-batch`: `97632e0` (FB-STD-01), v2.119.0, anti-patterns
  #124 and #125, `scripts/check-standard.sh` all checks passed.

## Items

`plan-data/items.tsv` (columns: id, milestone, repo, title, deps, findings, smoke). Every id carries the
prefix `FB-`; this repo's items are `FB-CT-*`, and Combat Trail's are `FB-CTR-*`. Done = a commit whose
subject starts `<ID>: ` (or carries `<ID> + `) on the branch, or a row in `plan-data/exceptions.tsv` with a
proof command. `plan-data/resume-state.sh` computes progress from git; it reads the repos four levels up
from itself, so run it from the run's scratch clone of this repo (whose siblings are the clones and
symlinks) or from the live checkout after the merge.

| Id | M | Repo | What | Finding |
|---|---|---|---|---|
| FB-CT-00 | M0 | Ka0sAddonsCommonTasks | This bundle | all |
| FB-LK-01 | M1 | LibKa0s | Core 20: `standIn`, `FollowColor` | K, P |
| FB-LK-02 | M1 | LibKa0s | SkinPaintControls 21: disabled primary | O2 |
| FB-LK-03 | M1 | LibKa0s | WidgetsHeader 2, CopyWindow 7, IconBrowserWindow 3: companion | T |
| FB-LK-04 | M1 | LibKa0s | SkinDefsOthers 11: High Contrast HUD shadow 1, -1 | A |
| FB-STD-01 | M1 | WowAddonStandards | v2.119.0: gear but on a companion (#124); class -> skin -> swatch, preview stand-in (#125) | T, P |
| FB-LK-REL | M1 | LibKa0s | v1.112.0, local tag | - |
| FB-ST-01 | M2 | LibKa0sSkinTester | Re-vendor; *Button (primary, disabled)* sample | O2 |
| FB-KC-01 | M2 | KickCD | Re-vendor; ladder, preview stand-in, target/focus repaint | K, P |
| FB-PFE-01 | M2 | PartyFrameEnhanced | Re-vendor; preview stand-in, roster repaint | P |
| FB-AT-01 | M2 | AbsorbTracker | Re-vendor; ladder, stand-in | P |
| FB-RM-01 | M2 | RangeMaster | Re-vendor; Class mode stand-in in test mode | P |
| FB-CTR-01 | M2 | CombatTrail | Re-vendor; paintBackdrop class-first | P |
| FB-CTR-02 | M2 | CombatTrail | Compare, timeline, gear: companions | T |
| FB-SM-01 | M2 | SkillMaster | S4 re-vendor v1.112.0 | S4 |
| FB-SM-02 | M2 | SkillMaster | Color sites class -> skin -> swatch | P |
| FB-SM-03 | M2 | SkillMaster | Trainer popup: companion | T |
| FB-SM-04 | M2 | SkillMaster | S1 detached width row and grip | S1 |
| FB-SM-05 | M2 | SkillMaster | S2 test-mode arrow | S2 |
| FB-SM-06 | M2 | SkillMaster | S3 two tabs | S3 |
| FB-DW-01 | M2 | DropWatcher | Re-vendor; rolls, offer, note editor: companions | T |
| FB-BL-01 | M2 | BankLedger | Re-vendor; export: companion | T |
| FB-LH-01 | M2 | LootHistory | Re-vendor; export: companion | T |
| FB-MM-01 | M2 | MultiMeters | Re-vendor; export: companion | T |
| FB-OR-01 | M2 | OutfitterReborn | Re-vendor; dialogs `companion = true` | O2, T |
| FB-OR-02 | M2 | OutfitterReborn | O1 separator full width | O1 |
| FB-QC-01 | M2 | QuickComms | Re-vendor; call-out modal `companion = true` | T |
| FB-QC-02 | M2 | QuickComms | Q test-mode toast | Q |
| FB-AM-01 | M2 | AuraMaster | Re-vendor (High Contrast fix arrives) | A |
| FB-CM-01 | M2 | ConsumableMaster | Re-vendor; companion and precedence audit | T, P |
| FB-PM-01 | M2 | PanelMaster | Re-vendor; companion and precedence audit | T, P |
| FB-PGFE-01 | M2 | PremadeGroupsFilterExtension | Re-vendor; companion audit | T |
| FB-PC-01 | M2 | PrettyChat | Re-vendor; companion audit | T |
| FB-WG-01 | M2 | WhatGroup | Re-vendor; companion and precedence audit | T, P |
| FB-CT-SMOKE | M3 | Ka0sAddonsCommonTasks | Smoke checks file | - |
| FB-CT-REC | M3 | Ka0sAddonsCommonTasks | Execution record | - |

Gates per addon item: `ka0s-bounded lua tests/run.lua`, plus `KA0S_KIT_CLIENT=forever` where the TOC carries
16001, `ka0s-bounded luacheck .` at 0/0, the 1500-line cap, CCN 15 or less, US spelling, line endings
kept, test first. A re-vendor is a whole copy of `libs/LibKa0s/` and `tests/_kit/` from the tag, with the
CLAUDE.md provenance line rolled in the same commit; `libs/` and `tests/_kit/` are never edited otherwise.

## Smoke checks (the owner's to run, in game)

Each Result line stays empty until the owner runs it.

- **S-O2a** Outfitter Reborn, New Outfit with the name empty, under several skins: *Done* looks like Skin
  Tester's *Disabled* (plain box, dim label); typing a name turns it into the primary look.
  Result:
- **S-O2b** Skin Tester's showroom shows a *Button (primary, disabled)* sample matching *Disabled*, in every
  skin.
  Result:
- **S-T1** The library's copy window (any addon's export or the debug console's Copy) carries the close
  alone; the icon browser too.
  Result:
- **S-T2** Combat Trail's compare, timeline and gear windows carry the close alone; Hud, race and Results
  windows keep the gear.
  Result:
- **S-T3** Skill Master's trainer popup carries the close alone; the main window, journal, detached and
  group windows keep the gear.
  Result:
- **S-T4** Drop Watcher's rolls and offer panels and the note editor carry the close alone; the feed
  window keeps the gear.
  Result:
- **S-T5** The export modals of Bank Ledger, Loot History and Multi Meters carry the close alone; their
  browsers, session window and meter windows keep the gear.
  Result:
- **S-T6** Outfitter Reborn's dialogs and Quick Comms' call-out modal still carry the close alone.
  Result:
- **S-K1** KickCD unlocked with no target, on a hunter: the *Target* and *Focus* labels with *Use class
  color* on draw hunter green, with *Use the skin's color* on or off.
  Result:
- **S-K2** KickCD live: target a player of another class, then retarget: the label and cast bar colors
  follow the new target without a /reload.
  Result:
- **S-P1** Party Frame Enhanced preview out of a party: *Use class color for fill* draws the player's class
  color on the cast bar, and the Text tab's class color too, with the skin companion on or off.
  Result:
- **S-P2** Party Frame Enhanced in a party: a member joining or swapping repaints the cast-bar text color.
  Result:
- **S-P3** Absorb Tracker's target bar with class and skin companions on and no target (unlocked): draws
  the player's class color.
  Result:
- **S-P4** Range Master's Class color mode in test mode with no target draws the player's class color.
  Result:
- **S-P5** Combat Trail's HUD box and window backgrounds and borders with *Use class color* on draw the
  class color while *Use the skin's color* is on.
  Result:
- **S-P6** Skill Master's bars, detached background and border, icon border and trainer name with *Use
  class color* on draw the class color while *Use the skin's color* is on.
  Result:
- **S-A1** Aura Master's bars under High Contrast with the Font outline on *HUD text only*: a 1 px shadow,
  no doubled letters; KickCD, PFE and Absorb Tracker HUD text under High Contrast look the same as before
  apart from the thinner shadow.
  Result:
- **S-Q1** `/qc test` shows the auto-thank toast; its Thank button sends nothing; the toast goes when test
  mode ends.
  Result:
- **S-S1** Skill Master: drag a detached window's grip wider and narrower; /reload keeps the width; Locked
  blocks it; the Blocks tab's width slider matches.
  Result:
- **S-S2** Skill Master with TomTom installed and *Show Skill Master's arrow* off: `/sm test` shows a
  labeled sample arrow, which goes when test mode ends.
  Result:
- **S-S3** Skill Master's *Trainers and Waypoints* page shows two tabs, Trainers and Waypoints, with the
  rows split as decided; Defaults resets both.
  Result:
- **S-S4** Skill Master loads clean on Forever after the re-vendor; its detached windows still carry the
  gear and no strip right-click rule applies to them.
  Result:
- **S-O1** Outfitter Reborn with Chonky tabs to the right: the separator above *New outfit* spans the whole
  frame width; the *New outfit* button has not moved.
  Result:
