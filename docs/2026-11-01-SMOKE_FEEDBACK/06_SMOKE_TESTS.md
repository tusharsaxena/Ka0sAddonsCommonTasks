# Smoke tests: smoke feedback batch (2026-11-01 to 2026-11-02)

**Fully exit and restart the client before you start. A `/reload` is not enough**: this batch changed library files (LibKa0s v1.85.0 re-cut: Launcher, Widgets, Sim, line chart, skin paint) and QuickComms, DpsRace and Skin Tester gained or moved files. Turn Lua errors on with `/console scriptErrors 1`; any Lua error or taint warning fails the check.

Nothing here has passed. Every Result is blank for you to fill in. An ID is the check's ID in that addon's `docs/smoke-tests.md`, where the full steps are; the short form is here. IDs starting `SFX-` are new on this list only and have no addon file yet (the batch's library items and its review fixes). Order: A is the quick library and launcher walk, B is addon by addon, C is the carry-over from the full skinning run.

## A. Library and every addon (SFX)

| ID | Do | Pass | Result |
|---|---|---|---|
| SFX-1 | Right-click the minimap button of any addon with skins (try three, one with the addon disabled) | The menu ends with "Open skin selector"; clicking it opens that addon's skin picker. Disabled: the entry is grayed with "(enable the addon first)". Fail: no entry, or it opens nothing | Passed (owner, 2026-11-02) |
| SFX-2 | SF-F1. Turn on a test mode or `/<addon> sim` in BankLedger, DpsRace, DropWatcher, LootHistory, MultiMeters; right-click its amber or cyan strip | A menu offers End test or End sim (a sim also Step and Restart); the entry ends the mode. Left-click does nothing new. The Skin Tester's sample strip takes no menu by design | Passed (owner, 2026-11-02) |
| SFX-3 | SF-L1 to SF-L5. In Obsidian, Glass, Forever and High Contrast open any table window and the skin picker | Picker tooltips wrap to several rows; table headers keep the skin color with the sort arrow in its own color; alternate rows show in every skin; every skin shows a rule between header and content (Obsidian's brighter, not dark); High Contrast edges are thinner everywhere | Passed (owner, 2026-11-02) |
| SFX-4 | SF-L6 (#72). Drag any window's resize grip, then reload and close/reopen it | The window keeps the new size and anchors back to where it was; nothing stranded or jumping | Passed (owner, 2026-11-02) |
| SFX-5 | SF-L7 (#71). In the Skin Tester or PremadeGroupsFilterExtension open a Blizzard dropdown (WowStyle1) in Obsidian; hover and press it; open then close its menu with the pointer elsewhere | Flat box, one chevron, no gold button; the label stays the skin color on hover, press and after the menu closes. Fail: the label turns white after close. That last case is unverified in code (no Blizzard source): if it fails, the fix is a hook on OnButtonStateChanged | Passed (owner, 2026-11-02) |
| SFX-6 | SF-L8 (#70). Skin Tester, Library widgets, line chart; LootHistory's chart | The first series has a soft area under its line; the chart still reads the same without it | Passed (owner, 2026-11-02) |
| SFX-7 | SF-AT-2 follow-ups. AbsorbTracker `/at unlock`, `/at sim`; toggle Lock mid-sim; again, `/at sim stop` during the last second and with bars unlocked; `/at debug hold 5000 3` mid-sim | Toggling the lock stops the sim and leaves no fake value; stop with bars unlocked returns the placeholder; stop in the tail says "Sim stopped"; a hold mid-sim replaces the sim; no fake number stays after any of them | Passed (owner, 2026-11-02) |
| SFX-8 | SF-DR-8. DpsRace `/dr sim`, press Stop on the stepper window | The sample race stops, the preview goes off, no Results window opens afterwards. Restart on the stepper still replays | Passed (owner, 2026-11-02) |
| SFX-9 | SF-KC-1. KickCD `/kcd sim start pull`, step through | See SIM-14 below; Thrall's kick ends the focus channel | Passed (owner, 2026-11-02) |

## B. Added or re-opened by this batch, by addon

### LibKa0sSkinTester

| ID | Do | Pass | Result |
|---|---|---|---|
| SHOW-37 | `/st show`, find the Source dropdown (now on its own row under the cards, inside the right edge); with EllesmereUI installed pick EllesmereUI, then a Ka0s skin. This is the lead's reading of "dropdown option to see the EllesmereUI skin" (SF-ST-1), not the owner's wording | The showroom wears EllesmereUI's look with no card selected; picking Ka0s skins goes back (asks for `/reload` if EllesmereUI painted). Without EllesmereUI it falls back | Passed (owner, 2026-11-02) |
| SHOW-38 | Library widgets in Obsidian (SF-ST-2) | Line chart area fill; Blizzard dropdown flat with one chevron, label keeps the skin color on hover and press | Passed (owner, 2026-11-02) |
| PANEL-6 | Fresh profile, General > Appearance: Ignore settings panel ticked, Ignore fonts not; untick, pick Azeroth, tick Ignore fonts; `/reload` | Pages take the skin at once; Cinzel titles go back to game fonts; ticks persist | Passed (owner, 2026-11-02) |
| PANEL-5 and the card-row check | Re-opened: PANEL-5 needs Ignore settings panel unticked first; the card-row check (in the Skin Tester's file, marked changed by SF-ST-1) now expects the Source dropdown | As their file steps say | Failed (owner, 2026-11-02): re-opened as R3-L1 (PANEL-5; the card-row check, SHOW-5, passed) |

### QuickComms

| ID | Do | Pass | Result |
|---|---|---|---|
| ANIM-3, ANIM-12, ANIM-13, ANIM-14 | Merged styles: Scale and Scale and fade (grow on open, shrink into the centre on close; no start-large); the list has 18 styles; Inward and Outward spiral | Each does what its label says; text stays sharp; the Open and Close lists match | Passed (owner, 2026-11-02) |
| ANIM-21 | A profile that stored Scale in, Scale out or their fade versions | They read Scale or Scale and fade, durations kept; Rotate and scale still the default | Passed (owner, 2026-11-02) |
| ANIM-22 | Wear WoW Default (SF-QC-3). Lead's interpretation: the owner saw the dialog-box border in the Skin Tester and the pad should match it; the gray tint of that art is as the Skin Tester draws it | The pad window is framed in the dialog-box border art, not a thin gray line; header, bands and buttons keep hairlines; other skins unchanged. Say if the gray tint is wrong | Passed (owner, 2026-11-02) |

### AbsorbTracker

| ID | Do | Pass | Result |
|---|---|---|---|
| SKIN-43 | SF-AT-1. `/at unlock`, all three bars, High Contrast then other skins | "Absorb" shows whole, centered, never clipped | Passed (owner, 2026-11-02) |
| SLASH-3, SIM-1 | `/at help` lists 21 verbs with sim; `/at sim` plays the made-up fight | As the file says | Passed (owner, 2026-11-02) |

### AuraMaster

| ID | Do | Pass | Result |
|---|---|---|---|
| SKIN-43 | Glow is black in every skin (SF-AM-1) | New Text container: Use the skin's color unticked, ring black in four skins | Passed (owner, 2026-11-02) |
| SKIN-44 | Bars: dark background and border in every skin (SF-AM-2). Lead's call: migration v17 forces Show border ON for every existing bar, because a deliberate off cannot be told from the old default and you asked for a border on every bar; a bar where you chose off turns on once | Dark background, black border, the skin's texture; Show border on after the update. Say if you want any bar to keep an old off | Passed (owner, 2026-11-02) |
| SKIN-45 | Fill, Text font and icon border colors stay yours (SF-AM-3, accepted deviation). Re-opened: SKIN-36, SKIN-38, SKIN-40 | Stored colors draw unchanged by a skin switch; ticking the box takes the skin's | Passed (owner, 2026-11-02) |

### BankLedger, ConsumableMaster, LootHistory

| ID | Do | Pass | Result |
|---|---|---|---|
| BankLedger SKIN-38 | Insights headings across five skin switches (SF-BL-1) | Headings never grow | Passed (owner, 2026-11-02) |
| BankLedger SKIN-39, LootHistory SKIN-47 | Sort arrow color (SF-L2) | The arrow wears the skin's arrow color; group expanders keep their icon color | Passed (owner, 2026-11-02) |
| ConsumableMaster SKIN-39, SKIN-40 (re-opened SKIN-37) | Bar border in every skin; your own None (SF-CM-1) | One thin solid edge by default, the skin's own under Azeroth, High Contrast, WoW Default, Midnight; your None draws no edge | Passed (owner, 2026-11-02) |

### MultiMeters, DpsRace, KickCD, PremadeGroupsFilterExtension

| ID | Do | Pass | Result |
|---|---|---|---|
| MultiMeters SKIN-41, SKIN-42 | SF-MM-1 to SF-MM-5: title left, cell borders off by default, bar opacity 15%, no overflow while dragging, chat-text export glyph. A stored window left-aligns | All five hold; skin switches leave 15% | Passed (owner, 2026-11-02) |
| DpsRace SM-DR-SF1 | Elapsed and time left clocks follow the skin font (SF-DR-1) | Per the file | Failed (owner, 2026-11-02): re-opened as R3-DR-1 |
| DpsRace SM-DR-SF11 to SM-DR-SF15 (renumbered by a fix; they clashed with SF1 to SF5) | Insights scoped by tab and Overall (SF-DR-3, 4); Race page tabs (SF-DR-5, 6); toast sound Default, no applause shipped because no verified sound id exists (SF-DR-7); the Sim stepper beside the race window (SF-DR-8) | Per the file | Passed (owner, 2026-11-02) |
| KickCD SIM-14 (re-opened SIM-8) | `/kcd sim start pull`, step through (SF-KC-1) | Focus casts beside the target; Uther's kick ends the focus cast, Thrall's ends the channel | Passed (owner, 2026-11-02) |
| PremadeGroupsFilterExtension SKIN-47 | Library paints the panel's dropdowns alone (SF-PG-1) | Flat box, one triangle, on Ka0s Default and Ember | Passed (owner, 2026-11-02) |

## C. Carry-over: checks from `docs/2026-11-01-FULL_SKINNING/06_SMOKE_TESTS.md` with no result yet

That file is frozen and holds the steps; its Result cells are all blank. You reported PartyFrameEnhanced, PremadeGroupsFilterExtension, PrettyChat and DpsRace's existing checks as passed, so they are left out. Still owed (194), by section:

- QuickComms: the dial's animations (3): ANIM-12, ANIM-17, ANIM-18
- QuickComms: the pad in each skin (11): PLOOK-1, PLOOK-2, PLOOK-3, PLOOK-4, PLOOK-5, PLOOK-6, PLOOK-7, PLOOK-8, PLOOK-9, PLOOK-10, PLOOK-11
- QuickComms: layering (two things to judge) (2): LAYER-6, LAYER-7
- LibKa0sSkinTester (15): SHOW-34, SHOW-35, SHOW-36, SHOW-30, SHOW-31, SHOW-32, SHOW-33, SHOW-9, SHOW-28, SHOW-29, PANEL-5, PANEL-13, PANEL-14, PANEL-15, PROFILE-3
- QuickComms (rest) (38): ANIM-1, ANIM-2, ANIM-3, ANIM-4, ANIM-5, ANIM-6, ANIM-7, ANIM-8, ANIM-9, ANIM-10, ANIM-11, ANIM-13, ANIM-14, ANIM-15, ANIM-16, ANIM-19, ANIM-20, LAYER-8, LAYER-9, FSKIN-1, FSKIN-2, FSKIN-3, FSKIN-4, FSKIN-5, FSKIN-6, FSKIN-7, FSKIN-8, FSKIN-9, FSKIN-10, FSKIN-11, FSKIN-12, SKIN-5, SKIN-6, SKIN-11, SKIN-12, SKIN-13, BUTTON-1, SHINE-1
- AbsorbTracker (14): SKIN-1, SKIN-5, SKIN-6, SKIN-24, SKIN-25, SKIN-35, SKIN-36, SKIN-37, SKIN-38, SKIN-39, SKIN-40, SKIN-41, SKIN-42, MIGRATE-2
- AuraMaster (12): SKIN-1, SKIN-4, SKIN-9, SKIN-31, SKIN-35, SKIN-36, SKIN-37, SKIN-38, SKIN-39, SKIN-40, SKIN-41, SKIN-42
- KickCD (15): SKIN-2, SKIN-5, SKIN-7, SKIN-36, SKIN-37, SKIN-38, SKIN-39, SKIN-40, SKIN-41, SKIN-42, GRID-10, LABEL-8, PANEL-33, PANEL-34, DEGRADED-16
- ConsumableMaster (23): SKIN-1, SKIN-2, SKIN-4, SKIN-6, SKIN-23, SKIN-25, SKIN-31, SKIN-32, SKIN-33, SKIN-34, SKIN-35, SKIN-36, SKIN-37, SKIN-38, INSTALL-5, PROFILE-2, PROFILE-5, BAR-2, BAR-4, BAR-12, BAR-13, BAR-29, BAR-30
- MultiMeters (22): SKIN-28, SKIN-29, SKIN-30, SKIN-31, SKIN-32, SKIN-33, SKIN-34, SKIN-35, SKIN-36, SKIN-37, SKIN-38, SKIN-39, SKIN-40, WIN-1, WIN-49, PANEL-54, GRID-25, SKIN-2, SKIN-4, SKIN-5, SKIN-11, DEGRADED-11
- DropWatcher (11): SKIN-37, SKIN-38, SKIN-39, SKIN-40, SKIN-41, SKIN-42, SKIN-43, SKIN-2, SKIN-14, SKIN-30, GLOW-9
- BankLedger (7): SKIN-1, SKIN-35, SKIN-36, SKIN-37, LEDG-36, DIAG-7, DEGRADED-16
- LootHistory (11): SKIN-1, SKIN-43, SKIN-44, SKIN-45, SKIN-46, HIST-43, HIST-44, INS-23, LED-13, TL-18, DEGRADED-15
- WhatGroup (5): SKIN-1, SKIN-10, SKIN-32, SKIN-33, POPUP-11
- PanelMaster (5): SKIN-20, SKIN-32, SKIN-33, SKIN-34, SKIN-35

Also still owed, from the `[No lib]` and per-skin walk sections of that file: run them last.

## SG-RV (not run)

- SG-RV-1: On one account, with all addons on the refreshed LibKa0s v1.85.0, log in once: exactly one skin picker opens (the first addon to ask), reopening any other addon or /reload shows none; the right-click launcher menu of AbsorbTracker, BankLedger, DpsRace, DropWatcher, KickCD, LootHistory and MultiMeters shows a Sim mode checkbox that ticks while the sim runs and starts or stops it, and every addon shows Open settings. Not run.
  Result: Passed (owner, 2026-11-02)

## SG-MM-1 (not run)

- SG-MM-1: In MultiMeters, drag the resize grip of a window wider and narrower: the column headers never draw past the window edge during the drag, as the cells already do. Not run.
  Result: Passed (owner, 2026-11-02)

## SG-AT-1 (not run)

- SG-AT-1: In AbsorbTracker, /at sim opens the library step window (fight, drain, refresh) and plays nothing until you start it; a run follows the scripted step gaps, a click on a step jumps the bar to that shield, and Stop (or /at sim stop) returns the bar to live data. Not run.
  Result: Passed (owner, 2026-11-02)

## SG-DR-1 (not run)

- SG-DR-1: In DpsRace, /dr sim opens the race window armed and the step window beside it, and nothing moves until you press Run or play the Armed step; the Armed step then starts the 3 second countdown. Not run.
  Result: Passed (owner, 2026-11-02)

## SG-DR-2 (not run)

- SG-DR-2: In DpsRace on your existing profile, /reload once, then switch the skin between Ka0s Default, Obsidian and WoW Forever: the Elapsed and Time Left clocks change face with the skin each time. Not run.
  Result: Failed (owner, 2026-11-02): re-opened as R3-DR-1

## SG-DR-3 (not run)

- SG-DR-3: In DpsRace, open Results and click Insights: Overall is lit. Pick another board, switch to Runs and back to Insights, close and reopen Results: the board you picked is lit; after /reload Overall is lit again. Not run.
  Result: Passed (owner, 2026-11-02)

## SG-SIM (not run)

- SG-SIM: In DpsRace, set Race > Simulator > Simulation step delay to 5, run /dr sim and press Run: each step follows the last by about 5 seconds, and changing the slider mid-run takes effect from the next step. BankLedger, DropWatcher and LootHistory already read their slider; KickCD and MultiMeters have no such setting (an owner call is open). Not run.
  Result: Passed (owner, 2026-11-02)

## M4: the owner's second smoke round, with the review's fixes (none run)

The checks above under SG-RV, SG-MM-1, SG-AT-1, SG-DR-1, SG-DR-2, SG-DR-3 and SG-SIM stand. The re-cut after the review changes what they must show; each id below is the full set for M4.

- SG-L1: Right-click the minimap button of every addon: Open settings is always present and live; Sim mode is present only where the addon has a sim; every toggle row is a checkbox with a live tick. In DpsRace, start /dr sim: only Sim mode is ticked, Test mode is not.
  Result: Passed (owner, 2026-11-02)
- SG-L2: Count the minimap buttons per addon in your button collector with each addon enabled once: one button per addon. If two remain, note which collector and which addons; the library makes one broker object and one button and never registers a compartment entry.
  Result: Passed (owner, 2026-11-02)
- SG-L3: With a profile that has never seen the notice, log in: one skin picker opens in total, not one per addon. Relog: it does not open again. With AbsorbTracker disabled and every other addon already past the notice, log in: it does not open. Log in while in combat: it opens after combat ends, however long the combat runs. Known gap: an addon with no record that loads before every addon that has one still opens it once.
  Result: Passed (owner, 2026-11-02)
- SG-REL: The local tag v1.85.0 is at 13e455d (eighth re-cut, bundle docs/automated-tests/20261102-130954/ in LibKa0s). Nothing to run in the client; confirm the tag is not on the remote.
  Result: Passed (owner, 2026-11-02)
- SG-RV: All 16 vendored copies carry the re-cut OptionsSkinPicker; with every addon on, /reload shows no Lua error.
  Result: Passed (owner, 2026-11-02)
- SG-AT-1: In AbsorbTracker, Settings > General > Behavior > Simulation step delay (seconds) exists; at 4 s each step of /at sim follows the last by about 4 s, and a change lands on the next step.
  Result: Passed (owner, 2026-11-02)
- SG-DR-1: /dr sim does not start by itself; the race stays armed until you press Run or play the Armed step.
  Result: Passed (owner, 2026-11-02)
- SG-SIM: In DpsRace with the delay at 5, play the Armed step: the countdown lasts about 5 s and Race starts lights as the race starts. At 1 s the countdown is about 1 s. Repeat the delay setting in AbsorbTracker, BankLedger, DropWatcher, LootHistory. KickCD and MultiMeters keep a fixed 1 s and stay the open owner call.
  Result: Passed (owner, 2026-11-02)
- SG-MM-1: In MultiMeters, drag a window narrower: the Deaths column header is cut at the window edge during the drag, as the cells are.
  Result: Passed (owner, 2026-11-02)
- SG-DR-2: In DpsRace, Elapsed and Time Left use the active skin's font under Ka0s Default, Obsidian and WoW Forever. If not, check your SavedVariables clocks.fontFromSkin: this depends on it being false in your profile.
  Result: Failed (owner, 2026-11-02): re-opened as R3-DR-1
- SG-DR-3: Insights opens on Overall the first time; later opens remember the last board for the session only; /reload resets it.
  Result: Passed (owner, 2026-11-02)
