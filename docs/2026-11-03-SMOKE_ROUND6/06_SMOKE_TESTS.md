# Smoke tests: the owner's sixth smoke round (2026-11-04)

**Fully exit and restart the client before you start. A `/reload` is not enough.** This round ships no new font or
texture file, but all 16 addons carry a re-vendored LibKa0s, and only a full restart makes every addon load that copy
fresh. The skin picker is now `OptionsSkinPicker` minor 11. Every check below assumes the local re-cut LibKa0s v1.85.0 at
**79d043d** (R6-REL, the seventeenth re-cut), re-vendored into all 16 addons. Turn Lua errors on with
`/console scriptErrors 1`. Any Lua error or taint warning fails the check.

Nothing here has passed. Every Result is blank for you to fill in. An ID is the check's ID in that addon's
`docs/smoke-tests.md`, where the full steps are; the short form is here. Addon prefixes: ST Skin Tester, AT
AbsorbTracker, AM AuraMaster, BL BankLedger, CM ConsumableMaster, DR DpsRace, DW DropWatcher, KC KickCD, LH LootHistory,
MM MultiMeters, PM PanelMaster, PF PartyFrameEnhanced, PG PremadeGroupsFilterExtension, PC PrettyChat, QC QuickComms,
WG WhatGroup.

## The rule you asked for (images 62, 63, 66)

When the skin picker shows and the addon's main surface is hidden, the addon enters its preview mode. That is test mode
if it has one, otherwise unlock mode (the Skin Tester's showroom window and PrettyChat's debug console are the two
exceptions). The eye toggles the mode: lit means on, dimmed means off, and its tooltip says which. Every way of closing
the picker puts the mode back to the state it had when the picker opened: Apply, Apply to all, the gear, the close mark
and Escape.

**The common steps.** Each addon block below runs these four, with the addon's own slash prefix and mode:

1. **Open hidden.** Hide the surface (test mode off and the window closed, or the frames locked), then `/xx skin`. The
   mode turns on and the picker stays in front of it. The eye is lit.
2. **Eye.** Hover the eye and read the tooltip. Click it: the mode turns off, the eye dims and the tooltip rewords. Click
   it again: the mode is back on and the eye is lit.
3. **Close by every route.** Reopen with `/xx skin` between closes. Close once with **Apply**, once with the **close
   mark** (the X) and once with **Escape**. After each close the addon is back as it was before the picker opened (mode
   off, the window closed or the frames locked). Where the addon has them, also close with the **gear** and with **Apply
   to all Ka0s addons**.
4. **Open shown.** Show the surface first (the window open, or `/xx unlock`), then `/xx skin`. Nothing changes at open.
   Click the eye (the mode goes off), then close: the mode is back on, as it was.

**Unlock is a stored setting** (the lead's call 3). For AT, CM, KC and PF, a `/reload` while the picker is up leaves the
frames unlocked until `/xx lock`. PM is the exception: its unlock is session state, so a `/reload` comes back locked.

## 0. Load and the first-run queue (once)

| ID | Do | Pass | Result |
|---|---|---|---|
| R6-LOAD | After the full restart, log in with all 16 addons and `/console scriptErrors 1` | No Lua error, and no LibKa0s minor-mismatch line. `/st diagnostics` lists `OptionsSkinPicker 11` (ST PICKER-26) | |
| R6-QUEUE | Create a new profile shared by several addons (or reset AT, CM and DW, for example), then `/reload`. The first-run pickers queue and show one at a time | Each picker that shows enters its own addon's mode (AT and CM unlock their bars, DW opens in test mode). Closing one puts that addon back *before* the next picker shows and enters its mode, so two modes are never on together. Apply to all on one picker dismisses the queued ones and leaves their addons untouched. The one-time SkinNotice picker behaves the same (PF SKIN-43). The first-run picker now carries the eye: AT SKIN-17, CM SKIN-17, KC SKIN-22, PM SKIN-15, PC SKIN-10 | |

## 1. LibKa0sSkinTester: window (the showroom)

| ID | Do | Pass | Result |
|---|---|---|---|
| ST PICKER-26 | `/st diagnostics` | `OptionsSkinPicker 11` | |
| ST PICKER-27 | Showroom closed, `/st skin`; the common steps 1 to 4 (step 4: `/st show` and the "Show the picker" button) | The showroom opens with the picker in front of it. Tooltip: "Preview: the skin showroom is open/closed". Every close (the X, Escape, Apply, the gear, the launcher entry then Apply) closes it again. Opened already: it stays open. Closing the showroom yourself while the picker is up keeps it closed | |
| ST PICKER-3 (re-opened) | Fresh profile, pick Ember, then the eye | The eye closes and reopens the showroom in Ember, with the pick still pending | |

## 2. AbsorbTracker: unlock (`/at unlock`)

| ID | Do | Pass | Result |
|---|---|---|---|
| AT SKIN-45 | `/at skin`; Apply, the X and Escape | Loads and closes clean, and a pick previews on the bars | |
| AT SKIN-46 | `/at lock`, then the common steps (closes also by the gear) | The bars unlock at open; tooltip "Preview: the frames are unlocked/locked"; every close locks them again. Opened unlocked: nothing moves. In combat the eye's unlock is refused ("Cannot unlock the bars during combat"). Lock frame and the minimap Lock entry agree throughout | |

## 3. AuraMaster: test (`/am test`)

| ID | Do | Pass | Result |
|---|---|---|---|
| AM SKIN-52 | Pick a skin, close by the X, Escape, Apply, Apply to all and the gear | The X and Escape put the skin back; Apply and Apply to all keep it; no Lua error | |
| AM SKIN-53 | `/am test off`, then the common steps (closes also by Apply to all, the gear and a profile switch); step 4 with `/am test on` | Test mode turns on with the placeholders; the Test mode box and the launcher agree; every close turns it off again. In combat the eye gives one gray "Test mode can't start in combat." line. SKIN-19's eye now toggles | |

## 4. BankLedger: test (`/bl test`)

| ID | Do | Pass | Result |
|---|---|---|---|
| BL SKIN-47 | `/bl skin`; pick Obsidian, the X, then Apply | Loads clean; the eye sits beside the gear | |
| BL SKIN-48 | Ledger closed, test mode off, then the common steps (closes also by the gear); step 4 with `/bl show` | Test mode opens the ledger on sample rows behind the picker; every close takes test mode and the window down. With `/bl show` first, the eye leaves your real window open. Test mode on and the window closed at open: back like that after the close | |

## 5. ConsumableMaster: unlock (`/cm unlock`)

| ID | Do | Pass | Result |
|---|---|---|---|
| CM SKIN-45 | `/cm diagnostics`, `/cm skin` | `OptionsSkinPicker 11`; the picker behaves as before | |
| CM SKIN-46 | `/cm bar on`, `/cm lock`, then the common steps (closes also by the gear and Apply to all) | The macro bar unlocks at open (move tint and handle); every close locks it again. The lock is not refused in combat. A profile switch with the picker up leaves the new profile's lock as it was, in combat too | |

## 6. DpsRace: test (`/dr test`)

| ID | Do | Pass | Result |
|---|---|---|---|
| DR SM-DR-R6RV | `/reload`, General > Skin, hover the eye, close | Loads clean | |
| DR SM-DR-R6PV | Out of combat, the HUD and Results closed, test mode off, then the common steps (closes also by the gear); step 4 with `/dr hud show` and then `/dr test`; last, `/dr sim newbest` with the picker | Test mode shows the HUD and Results on sample data; tooltip "test mode is on/off"; every close ends it and closes both windows. HUD already up: test mode stays off. The sim plays on through the eye and the close | |

## 7. DropWatcher: test (`/dw test`)

| ID | Do | Pass | Result |
|---|---|---|---|
| DW SKIN-50 | `/dw skin`; pick, Apply, reopen, the X and Escape | The selector is in front; an unapplied pick goes back | |
| DW SKIN-51 | `/dw hide`, test mode off, then the common steps (closes also by the gear); step 4 with `/dw test` and with `/dw show` | The window opens in test mode with the TEST MODE strip; every close turns it off and closes the window. In combat: "Test mode is not available in combat." `/dw disable` and `/dw enable` with the picker up: the window stays closed | |

## 8. KickCD: unlock (`/kcd unlock`)

| ID | Do | Pass | Result |
|---|---|---|---|
| KC SKIN-46 | `/kcd skin`; the X, then Escape | Opens and closes clean | |
| KC SKIN-47 | `/kcd lock`, then the common steps (closes also by the gear); also `/kcd sim start` then `/kcd skin` | The grids and cast bars unlock at open; every close locks them. With a sim running the unlock is refused ("End the simulation first") and the close leaves them locked | |
| KC SKIN-48 | `/kcd skin` on a locked profile, then switch profile; also the reset case in its file | The profile you left comes back locked; the other keeps its own lock; a reset profile is not relocked | |

## 9. LootHistory: test (`/lh test`)

| ID | Do | Pass | Result |
|---|---|---|---|
| LH SKIN-53 | `/lh skin`, Glass and Apply; again, Ka0s Default and Escape | Applies and reverts as before | |
| LH SKIN-54 | Test mode off, History closed, then the common steps (closes also by the gear and `/lh disable`); step 4 with `/lh show` and with `/lh test` | History opens in test mode on sample rows; every close turns it off and closes it. The Test mode box and the minimap tooltip follow the eye. A window you had open stays open | |

## 10. MultiMeters: test (`/mm test`)

| ID | Do | Pass | Result |
|---|---|---|---|
| MM SKIN-49 | `/mm skin` | The eye and gear in the header; the list closes on an outside press | |
| MM SKIN-50 | No meter on screen (`/mm toggle`, then a second run on *Only in combat*), test mode off, then the common steps (closes also by Apply to all and the gear) | Every meter shows TEST MODE behind the picker; every close turns it off and no meter is left on screen; on *Only in combat* a zone change after the close keeps them hidden. In combat the eye says "Cannot start test mode during combat" | |

## 11. PanelMaster: unlock (`/pm unlock`)

| ID | Do | Pass | Result |
|---|---|---|---|
| PM SKIN-42 | `/reload`; `/pm debug`, Copy and `/pm skin` | No load error; the windows look as before | |
| PM SKIN-43 | At least one panel, `/pm lock`, then the common steps (closes also by Apply to all and the gear); also the one-panel-unlocked case in its file | Every panel shows its gold outline at open; the eye's tooltip reads "Preview: the frames are unlocked/locked"; every close locks them again. A panel you unlocked yourself stays unlocked. In combat a gray "no skin preview in combat" line. A `/reload` comes back locked | |

## 12. PartyFrameEnhanced: unlock (`/pfe unlock`)

| ID | Do | Pass | Result |
|---|---|---|---|
| PF INSTALL-4 (re-opened) | `/reload` | A clean load on the vendored copy | |
| PF SKIN-43 | Out of combat, the elements locked, then the common steps (closes also by the gear); also a profile switch with the picker up | Placeholders (or the stand-in out of a party) at open; Lock frame and the launcher read unlocked; every close locks again. In combat an unlock from the eye prints the unlock's own refusal. The profile you left comes back locked | |

## 13. PremadeGroupsFilterExtension: no preview (the no-eye check)

| ID | Do | Pass | Result |
|---|---|---|---|
| PG SKIN-52 | PGF closed, `/pgfe skin`; pick, then the X, Escape, the gear and Apply; again with PGF open on Dungeons | No eye; nothing else opens; only Apply stores the pick | |
| PG SKIN-53 | PGF closed, `/pgfe skin`; then PGF open on Dungeons, `/pgfe skin` | No eye, and no window, test mode or unlock turns on. Closing changes nothing; PGF and its panel stay as they were | |

## 14. PrettyChat: console (the debug console with the `/pc test` sample)

| ID | Do | Pass | Result |
|---|---|---|---|
| PC RV-88 | `/reload`, `/pc skin`; Apply, the X, Escape | Loads and closes clean | |
| PC SKIN-34 | Console closed, `/pc skin`; the common steps (closes also by the gear); step 4 with `/pc debug` | The debug console opens filled with `/pc test`'s sample, from its header to *end of test output*. Tooltip: "Preview: the debug console is open/closed". A second eye click writes no second sample. Every close hides it. A console you opened yourself gets no sample and stays open. After a `/reload` it is closed | |
| PC SKIN-10 (re-opened) | The first-run picker on a fresh profile | It now has the eye and opens the console | |

## 15. QuickComms: test (`/qc test`)

| ID | Do | Pass | Result |
|---|---|---|---|
| QC SKIN-34 | `/qc skin`; the X, Escape, Apply | An unapplied pick goes back | |
| QC SKIN-35 | Test mode off, `/qc toggle` to hide the pads, then the common steps (closes also by the gear); step 4 with `/qc test` and with the pads shown | Every pad shows placeholders and dial 1 opens, behind the picker; every close turns test mode off and hides the pads. Pulling a dummy ends test mode with its own line, and the close adds no second line | |

## 16. WhatGroup: test (`/wg test`)

| ID | Do | Pass | Result |
|---|---|---|---|
| WG SKIN-41 | `/wg skin`; Apply, the gear, the X, Escape | Every route closes clean | |
| WG SKIN-42 | Popup closed, test mode off, then the common steps (closes also by the gear and `/wg disable`); step 4 with `/wg test` and over a real group's popup | The popup opens on the sample group; every close turns test mode off and closes it. Over a real popup the eye shows the sample and the close brings the real group back. In combat a gray "cannot start test mode during combat" line. SKIN-19's eye now toggles | |

## Follow-up (2026-11-04): the Sim checkbox, the export glyph, the PFE profile switch, the README names

**Fully exit and restart the client first.** LibKa0s v1.85.0 is re-cut again, the eighteenth time, at **550ef68**
(R6-REL2), and re-vendored into all 16 addons (R6-RV2). Only `OptionsCompose.lua` moved, to minor 19. Every Result
below is blank. Nothing has passed. The full steps for each ID are in that addon's `docs/smoke-tests.md`.

**The Sim checkbox steps (S1 to S6).** Each sim addon block below runs these with its own slash prefix:

1. **Where.** Open General > Master controls. The **Sim mode** box sits where the row says. It is unticked.
2. **Tick.** With no sim running, tick it. It does exactly what a bare `/xx sim` does: the status line prints and the
   step panel opens. Nothing plays yet, so the box goes back to unticked. Start a scenario from the panel. The box ticks
   at once, with the page still open.
3. **Untick.** Untick it. The sim stops with its own stop line, as `/xx sim stop` does.
4. **Follows the slash command.** With the page open, `/xx sim start <scenario>` ticks the box at once, and `/xx sim
   stop` unticks it. Close the settings, start a sim from the slash command or the launcher's *Sim mode* entry, then
   reopen the page. The box is ticked, and the launcher's entry agrees with it.
5. **Refusals.** In combat, tick it. It stays unticked and nothing starts. A sim that stops itself (its end, combat, a
   real event) unticks the box.
6. **Session only.** Start a sim, then `/reload`. The box is unticked and nothing was stored.

| ID | Do | Pass | Result |
|---|---|---|---|
| AT SIM-2 | S1 to S6 with `/at sim` (scenario `fight`) | **Sim mode** beside **Lock frame** (no Test mode row), and Debug console and Minimap button on the next line. A tick opens the step window. With a sim running, Reset all settings stops it | |
| BL SIM-15 | S1 to S6 with `/bl sim` (scenario `bank`; test mode off, no bank open) | **Sim mode** alone on the line under Minimap button and Test mode. A real bank visit also ends it. With a sim running, Reset all settings leaves it running and the box ticked (OWNER_SCOPE C.13) | |
| BL PANEL-5 (re-opened) | General > Master controls | The rows as before, plus the Sim mode line, then Reset position and Reset all settings side by side | |
| DR SM-DR-R6SIM | S1 to S6 with `/dr sim` (scenario `newbest`, no race armed) | **Sim mode** beside **Test mode**. The tick opens the *DPS Race - Simulation* window idle. With a sim running, Reset all settings stops it | |
| DR SM-DR-R6RV2 | `/reload`; Master controls; then the Skin picker, close it | A clean load, and the picker draws as before | |
| DW SIM-19 | S1 to S6 with `/dw sim` (scenario `key`) | **Sim mode** on the line under Minimap button and Test mode. With test mode on, a tick opens the panel and a start refuses ("Turn test mode off before starting a simulation."). Reset all settings stops a running sim and starts none | |
| DW PANEL-11 | `/dw config`, every page; tick and untick Test mode | A clean load, and every row in its place | |
| KC SIM-17 | S1 to S6 with `/kcd sim` (scenario `pull`) | **Sim mode** beside **Lock frame**, and Debug console and Minimap button on the next line. With a sim running, Reset all settings stops it | |
| LH SIM-13 | S1 to S6 with `/lh sim` (scenario `loot`) | **Sim mode** opens the line under Minimap button and Test mode. Its tooltip names `/lh sim`. Untick takes the cyan strip away. Reset all settings stops a running sim and starts none | |
| MM SIM-15 | S1 to S6 with `/mm sim` (scenario `dungeon`) | **Sim mode** on its own line under Minimap button and Test mode. Untick puts the windows back on live data. With a sim running, Reset all settings stops it | |

**The nine addons with no sim (R6-RV2).** Each loads clean on the re-cut and its Master controls shows exactly the rows
it showed before, with **no** Sim mode box. A Sim mode box, a moved or missing row, or a Lua error fails the check.

| ID | Do | Pass | Result |
|---|---|---|---|
| ST PANEL-19 | `/st diagnostics`, then General | The running line lists `OptionsCompose 19`. No Sim mode box | |
| AM PANEL-28 | General > Master controls; tick and untick Test mode | Test mode beside Minimap button. No Sim mode box | |
| CM PANEL-35 | `/cm diagnostics`; General; tick and untick Lock frame | `OptionsCompose 19`; the nine controls PANEL-6 lists. No Sim mode box | |
| PM SKIN-44 | `/reload`; `/pm config`; `/pm skin`, `/pm debug` | Minimap button alone on its line. No Sim mode box | |
| PG PANEL-6 | Master controls under Ka0s Default and one other skin | No Sim mode box and no Test mode box | |
| PC RV-89 | `/reload`; `/pc config` > General > Master controls | The rows PANEL-7 lists. No Sim mode row | |
| QC PANEL-4 | General > Master controls | PANEL-2's rows, in its pairs. No Sim mode row | |
| WG PANEL-23 | `/wg config` > General > Master controls; tick and untick Test mode | Lock frame and Debug console, then Minimap button and Test mode, then the reset pair. No Sim mode box | |
| PF INSTALL-4 (still owed) | `/reload` | A clean load on the re-cut. Nothing new is drawn in this addon | |

**The MultiMeters export glyph (R6-MM2, image 67).**

| ID | Do | Pass | Result |
|---|---|---|---|
| MM WIN-58 | `/mm test`; look at the header; pick each skin; Header > Controls > Control size at its smallest and largest; hover the bubble | The export chat bubble is the same visual size as reset, the segment menu, the gear, the padlock, minimize and close in every skin and at every control size. Its edges are not clipped, it stays on the bar's middle and it takes the hover color | |

**The PartyFrameEnhanced profile switch (R6-PF1).**

| ID | Do | Pass | Result |
|---|---|---|---|
| PF CAST-8 | Profiles `A` (Ka0s Default) and `B` (Glass). On A, `/pfe unlock`, then `/pfe profile B`; then the lock and unlock sequence in its file, switching between two unlocked profiles; once solo and once in a party | Zero Lua errors (none naming `CastBars.lua:120`, "attempt to index local 'u'"). The bars repaint in B's skin and lock state, and the preview casts keep their fill color | |

**The README names (R6-NAME, README only).** All 16 READMEs drop Ka0s from the title (for example `# Ka0s Loot
History` is now `# Loot History`). The TOC, the compartment, settings, the launcher, windows and chat all keep Ka0s.

| ID | Do | Pass | Result |
|---|---|---|---|
| R6-NAME spot-check | Open one addon's README on GitHub after the push (for example LootHistory), then that addon in game: the AddOns list, the compartment and the settings category | The README's title and opening line read `Loot History`. In game it is still `Ka0s Loot History` everywhere | |
