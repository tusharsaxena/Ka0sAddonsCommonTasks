# Report: smoke feedback batch

Branch `feat/2026-11-01-full-skinning` in 17 repos. Nothing merged, tagged or version-bumped. Smoke list: `06_SMOKE_TESTS.md` (nothing marked passed).

## What shipped

- M1 library (SF-L1 to SF-L5), M2 bugs and skin fixes, M3 features (SF-L6 to SF-L8, SF-F1, SF-F2, SF-PG-1, SF-ST-2, SF-DR-3 to SF-DR-8, SF-AT-2, SF-KC-1), then the review's SF-FIX commits.
- SF-FIX: the launcher's "Open skin selector" now reaches every addon (`openSkinPicker` in 16 LauncherSetup files, grayed while disabled); mode strips pass `sim` or `onEnd` in BankLedger, DpsRace, DropWatcher, LootHistory, MultiMeters; DpsRace's stepper Stop ends the preview; AbsorbTracker's sim ends with its hold and restores the placeholder; KickCD's e2e test pins Thrall's kick; DpsRace smoke ids renumbered (SM-DR-SF11 to 15 had clashed with SF1 to SF5).
- Review findings: 8 verified issues were right and fixed except SF-DR-9 (below). The ninth (wowLabel not hooking OnButtonStateChanged) is unverified and is smoke check SFX-5.

## Totals

- Final loop, 17 repos: tests 0 failed in all, luacheck 0 warnings / 0 errors in all, no eol reds (one ANALYSIS.md in DpsRace repaired).
- LibKa0s 3919 passed; AuraMaster 2344; MultiMeters 2540; DropWatcher 1929; QuickComms 1699; KickCD 1639; BankLedger 1632; the rest between 517 and 1956.

## Open items

- SF-DR-9 is not done and #70 must not close. The live damage chart draws secret values straight into StatusBars and never computes on them; the library's line chart needs plain numbers to place points, so it cannot draw the live HUD. Only the after-race card and Results chart are plain. Moving them would leave two renderers and change the look (columns, not a line), so I did not guess. Needs your word: land it for the plain views only, or move it out of M3.
- Skin Tester's sample strip takes no right-click menu: it is a specimen with no mode to end.
- Unreleased: LibKa0s HEAD is 2ce2c67 with the grayed skin entry. The local v1.85.0 tag was moved to it (not pushed) and Launcher.lua was re-vendored into all 16 addons. The recorded release battery (docs/automated-tests/20261102-020922) predates that one change; gates were re-run green.
- Not done: no per-addon smoke file got the SFX checks; they live only in `06_SMOKE_TESTS.md`.
- LibKa0s #70, #71, #72 stay open until you merge.

## The lead's calls

- AuraMaster v17 forces Show border on for every bar.
- QuickComms WoW Default border follows the Skin Tester's dialog art, with its gray tint.
- Skin Tester's Source dropdown is an interpretation of "option to see the EllesmereUI skin".
- Carry-over list excludes PartyFrameEnhanced, PremadeGroupsFilterExtension, PrettyChat and DpsRace's existing checks, which you reported passed.

## M4 (the owner's second smoke round, 2026-11-02)

- SG-L1 to SG-L3, SG-AT-1, SG-DR-1 to SG-DR-3, SG-SIM and SG-MM-1 are in. The review's seven findings are fixed with SF-FIX commits: MultiMeters header strip anchored to both corners; DpsRace launcher ticks only Sim mode in a sim; DpsRace Armed step counts one step delay; AbsorbTracker gets the sim.stepDelay slider; the skin notice's combat retry repeats in all 15 hosts; a stood-down host calls SkinNotice record-only; a seen record claims the notice.
- LibKa0s changed (OptionsSkinPicker minor 9, in place): the v1.85.0 tag is re-cut locally at 13e455d, release battery docs/automated-tests/20261102-130954/ (green, 3931 tests), and re-vendored into 16 addons.
- Not done as asked: the reviewer's delay of the first show until login settles. I built it, and it left a library timer armed across a stand-down and deferred every host's first-run picker (about 100 host tests went red), so it was dropped. Residual: an addon with no record that loads before every addon that has one still shows the notice once.
- Not done: no per-host test of the notice retry except ConsumableMaster's; the other 14 share the same code and rely on the library tests. KickCD and MultiMeters sim pace stays fixed (open owner call). SG-DR-2 needs your profile's fontFromSkin to be false; only the smoke proves it. SG-L2 (two buttons) is not reproduced in code; likely the collector.
- LootHistory's two luacheck warnings in tests/test_launcher.lua were cleaned.
- Nothing is marked passed.
