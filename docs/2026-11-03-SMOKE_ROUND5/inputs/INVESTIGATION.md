# Round 5 investigation (read-only workflow wf_d3235619-e06)
Each topic: the investigator's findings and fix, then a skeptic's corrections and misses. Skeptic order follows completion, matched by content.

## dr-sim (item 6b): /dr sim opens mid-session with Resume instead of an idle Start + scenario picker, and the Racing step and final countdown run about 3x fast

### Findings

I changed nothing. All paths are relative to /mnt/d/Profile/Users/Tushar/Documents/GIT. The library is LibKa0s v1.85.0, and DpsRace/libs/LibKa0s/SimPanel.lua and SimTimeline.lua are byte-identical to it.

A. WHY /dr sim OPENS "ON STEP 2" WITH RESUME (image 49)
1. `/dr sim` never goes through the library's verb grammar. The call chain is:
   - DpsRace/settings/Slash.lua:293-295: doSim -> NS.StartSim(word).
   - DpsRace/core/DpsRace.lua:186-195: an empty word becomes Sim.DEFAULT ("newbest"), then startQueued.
   - core/DpsRace.lua:161-166: startQueued sets state.testMode true -> Preview.Start (modules/Preview.lua:147-175) -> NS.Sim.Begin (Preview.lua:165-167).
2. Sim.Begin (DpsRace/modules/Sim.lua:262-270) calls `session:Start({ scenario, fromHost = true })` straight away, then ShowPanel. The session is live the moment the window appears.
3. The library draws a live session as "running", not "idle" (LibKa0s/LibKa0s/SimPanel.lua:260-275, model()):
   - startState says "done" once the session is ready (SimPanel.lua:292-299), so the Start row is green.
   - Armed is pos+1, so its state is "ready" (white) (SimPanel.lua:284-290).
   - The footer swaps the picker for the controls whenever a session exists (SimPanel.lua:523-540).
   - A session started through the member is waiting, not paused, so the first button reads RESUME and sends `run` (SimPanel.lua:504-520).
   Nothing has auto-advanced: Armed is only "next", and the arm is parked (Sim.lua:139, SampleRace.lua:249-266). The panel just looks mid-run because the host started the session itself.
4. How MultiMeters does it (image 50): its slash row hands the text to the library (MultiMeters/settings/Slash.lua:138-139, `NS.Sim:RunVerb(a)`). A bare line runs runVerb's empty-verb branch (LibKa0s/LibKa0s/SimTimeline.lua:587-596): status, usage, then ShowPanel with no session. That is the idle model: Start row ready, steps locked as a preview, and the picker footer (scenario dropdown + Start, SimPanel.lua:440-468). Start sends `start <name>` (SimTimeline.lua:539-546). That starts the session and arms the run, which then plays on its own at sim.stepDelay. MultiMeters' prepare also shows the panel (MultiMeters/modules/Sim.lua:216-229).
5. Related latent bug, same root cause. The DpsRace panel prints the library commands in its right column (`/dr sim start newbest`, `/dr sim step`, `/dr sim stop`; image 49, SimPanel.lua:217, 307, 315, 322). Typing any of them fails: NS.StartSim treats "start", "step" and "stop" as scenario names and prints the usage (core/DpsRace.lua:189-192).
6. If the host is changed so the panel's Start works, two traps:
   - The idle Start is refused today. The descriptor's refusal is `not (opts.fromHost or history)` -> "Start the simulation with /dr sim [scenario]." (Sim.lua:228-230). history is only set by Sim.Begin.
   - A prepare that simply called Preview.Start would kill its own session. Preview.Start calls stopSim -> Sim.Cancel -> stopSession -> session:Stop (Preview.lua:136-140, 153; Sim.lua:251-258, 278-282), and the session is already S.session inside prepare (LibKa0s/LibKa0s/Sim.lua:554-561).

B. WHY THE RUN "ZOOMS"
1. The Racing step paces the race on purpose (R4-DR6, from the owner's round-4 request to make the core damage step "about 10s"; SMOKE_ROUND4/inputs/OWNER_FEEDBACK.md:19-20):
   - Sim.RACE_STEP_SECONDS = 10 (Sim.lua:40-42).
   - paceTheRace sets the pace to `left / 10` (Sim.lua:155-163). The race is MockRuns.LENGTH = 30 s (MockRuns.lua:26; stopAt at MockRuns.lua:590), so 30 race seconds play in 10 wall seconds, 3x.
   - SampleRace's clock multiplies by rate (SampleRace.lua:73-81; Pace at :306-310).
2. The final countdown follows that pace. Countdown.schedule divides every mark's delay by Race.Rate() (Countdown.lua:292-311), and paceTheRace calls Countdown.Refresh (Sim.lua:162). The 10-to-1 numbers therefore play in about 3.3 s.
3. The race stays real-time after the buzzer, but the stepper skips it:
   - buzz/endEarly put the rate back to 1 (SampleRace.lua:164-178).
   - With Run at the default sim.stepDelay = 1 (defaults/Profile.lua:218), Buzzer comes one poll after the race's own buzzer.
   - One second later the Result card step calls SkipToResult (Sim.lua:171), which jumps the clock in 0.5 s strides (SampleRace.lua:290-301). Stop!, the tail (3.1 s), combat end (4.2 s) and the 2.5 s quiet before the read (Scoring.lua:19) pass in about 1 s instead of about 6.7 s.
   - The Results window opens one step delay (1 s) after the card. The no-stepper path holds the card for RESULT_HOLD = 4 s (Sim.lua:35, 126-127).
4. The gate only holds while the race is RUNNING after the Racing step (Sim.lua:193-198), so nothing waits for the read.
5. Armed counts down one step delay (1 s) (Sim.lua:167). SG-SIM pins this so that "Race starts" lights at zero. It is not part of the zoom complaint.

C. OTHER HOSTS
DpsRace is the only sim host that starts its session from the host with fromHost. MultiMeters, DropWatcher, LootHistory, KickCD, BankLedger and AbsorbTracker go through RunVerb or the picker. No library change is needed for parity.

D. TESTS THAT PIN TODAY'S BEHAVIOUR (each must be rewritten with the fix)
DpsRace/tests/test_sim.lua:
- :26-29 sim(): starts through Preview.Start, then Unpark(ARM_HOLD).
- :325-337: a session is active right after Preview.Start.
- :357-382: the step sequence; the Racing step "plays fast"; the buzzer settles until RACE_STEP_SECONDS + 0.5.
- :384-393: labels "Racing (12 s of damage in 10 s)" and "Racing (30 s of damage in 10 s)".
- :441-451: toRacing.
- :453-466: Rate() > 1; buzzer between 9.5 s and 10.1 s.
- :468-492: the countdown 5 and 1 shown inside 10.5 s.
- :494-513: rate back to 1 after the buzzer, gate line.
- :515-534: racing span 9.9 to 10.5 s.
- :398-436: SG-DR-1 and SG-SIM pacing. These stay valid.
DpsRace/tests/test_slash.lua:
- :329-347: `/dr sim` makes Preview.Mode() "sim" immediately; `sim died` switches; `sim sideways` prints the usage plus the scenario lines.
- :349-357: the help line.
DpsRace/tests/test_launcher.lua:61-69: NS.StartSim() makes the Sim mode row tick.
DpsRace/tests/test_countdown.lua:254, 272, 292: Unpark(ARM_HOLD). Unaffected.
SMOKE_ROUND4/06_SMOKE_TESTS.md:42: SM-DR-R4DR6 expects "about 10 s, the clock runs about 3x fast". It is superseded.

### Fix

The fix is host-only, in DpsRace. LibKa0s needs no change.

1. LAYOUT: open idle, like MultiMeters
a. Slash. doSim (settings/Slash.lua:293-295) passes the rest to `NS.Sim.session:RunVerb(rest)`, after one back-compat rewrite: a bare scenario word such as `/dr sim died` becomes `start died`. Results:
   - `/dr sim` prints status and usage, and opens the panel with no session: Start ready, steps previewed and locked, scenario dropdown + Start.
   - `/dr sim start x`, `step`, `stop`, `pause`, `restart`, `status` and `panel` now work as the panel advertises.
   - A word that is neither a scenario nor a verb prints the library usage. It is followed by the "  key: desc" lines, kept as the descriptor's `usage` list.
   - With no library session (headless), keep today's NS.StartSim path.
b. Launcher. LauncherSetup.lua:106-107 toggleSim uses `RunVerb(active and "stop" or "")`, MultiMeters' rule (MultiMeters/core/LauncherSetup.lua:353-357).
c. Session drives Preview. Today Preview starts the session; invert that:
   - Add `Preview.EnterSim(scenario)`, the body of Preview.Start's sim branch: the refusals, the HUD AutoShow, the dataset, ResultsSource.Use and BestToast.EndPreview. It sets state.testMode through the write seam so the Master row and launcher follow. It must NOT call stopSim/Sim.Cancel for the session being prepared.
   - The descriptor's prepare = EnterSim(opts.scenario) + launch(opts.scenario) (parked) + ShowPanel + ready().
   - The refusal returns Preview's lines (combat, a real race on, stood down) in place of "Start the simulation with /dr sim" (Sim.lua:228-230).
   - Sim.Begin remains only for the headless path.
   - OnStop "stop" -> Preview.Stop stays (Sim.lua:244-248). The panel's own Stop leaves the panel open and idle, as MultiMeters does: no HidePanel for the session's own stop. Every other Preview end still hides it.
d. Scenario labels for the dropdown (defs[key].label, Sim.lua:212). Use short readable labels instead of the bare key, e.g. "New best", "Behind the best", "First race", "Incomplete", "You die", "Late cast", "Shared session", "Combat holds on". The Start row then reads "Start: New best". This is a lead decision; no owner input is needed.
e. After Start: the library arms the run (SimTimeline.lua:539-546). Armed plays at once (Unpark(stepDelay)), and the rest follows at sim.stepDelay, exactly as /mm sim does. Nothing runs before Start.

2. REAL-TIME RACE (recommended timings, newbest at the default 1 s step delay)
a. Racing. paceTheRace becomes `Race.Skip(0); racing = true` with no Pace and no Countdown.Refresh. Drop RACE_STEP_SECONDS. The rate stays 1.
   - Racing lasts the race's remaining real time: 30 s for newbest, behind, first, flagged, shared and sticky; 18 s for incomplete; 12 s for died.
   - The final 10-to-1 countdown runs at one number a second.
   - SampleRace.Pace/Rate and Countdown's rate division can stay as dead-safe code or be removed. I recommend removing them, along with the R4-DR6 comments.
b. Label: "Racing (%d s)", with the race length. Update locales/enUS.lua:592.
c. Gate (Sim.lua:193-198):
   - Hold while the race is RUNNING (as today), and also while it is STOPPING, with "Waiting for the result." The Result card step then lands when the race reads its own result at real speed: Stop!, tail, combat end, then 2.5 s of quiet. That is about 6.7 s after the buzzer for newbest, and about 20.5 s for sticky (hintDelay 15 + 3 + 2.5), which is that scenario's point.
   - The Result card step's SkipToResult remains only for a manual click-ahead, where it is a no-op once the result is in.
   - Also hold the Results window step until the card has shown for Sim.RESULT_HOLD (4 s), the no-stepper path's own hold.
d. Resulting newbest run at delay 1:
   - Start = Armed at 0 s.
   - Race starts at 1 s.
   - Racing from about 2 s, buzzer at 31 s.
   - Buzzer step at about 31.25 s (gate poll).
   - Result card at about 37.7 s.
   - Results window at about 41.7 s.
   About 42 s end to end, against about 15 s today.

3. TESTS (write them red first)
- test_slash: bare `/dr sim` leaves Preview off, shows the panel and creates no session (PanelRows()[1].state == "ready"). `/dr sim died` and `/dr sim start died` start the session with Preview.Mode() "sim" and the Master row on. `/dr sim step` and `/dr sim stop` act.
- test_sim: change the sim() helper to start through RunVerb("start x"). The picker's Start works when idle.
- Racing: Rate() == 1, the buzzer at stopAt ± one tick in real seconds, and the countdown numbers one per second.
- Gate: closed through STOPPING until RESULT. Run's full span lies in [40, 44] s for newbest.
- test_launcher:61-69 ticks Sim mode after Start, not on panel open.
- Replace SM-DR-R4DR6 with a new smoke row in the round 5 bundle.

### Sites

- DpsRace/settings/Slash.lua:293-295
- DpsRace/core/DpsRace.lua:161-166
- DpsRace/core/DpsRace.lua:186-195
- DpsRace/core/LauncherSetup.lua:105-107
- DpsRace/modules/Preview.lua:136-175
- DpsRace/modules/Sim.lua:35
- DpsRace/modules/Sim.lua:40-42
- DpsRace/modules/Sim.lua:133-141
- DpsRace/modules/Sim.lua:155-173
- DpsRace/modules/Sim.lua:175-187
- DpsRace/modules/Sim.lua:193-198
- DpsRace/modules/Sim.lua:206-238
- DpsRace/modules/Sim.lua:244-258
- DpsRace/modules/Sim.lua:262-270
- DpsRace/modules/SampleRace.lua:73-81
- DpsRace/modules/SampleRace.lua:164-178
- DpsRace/modules/SampleRace.lua:290-310
- DpsRace/modules/Countdown.lua:292-311
- DpsRace/modules/MockRuns.lua:26
- DpsRace/modules/MockRuns.lua:590-591
- DpsRace/modules/Scoring.lua:19
- DpsRace/defaults/Profile.lua:104-106
- DpsRace/defaults/Profile.lua:218
- DpsRace/locales/enUS.lua:592
- LibKa0s/LibKa0s/SimPanel.lua:260-299
- LibKa0s/LibKa0s/SimPanel.lua:440-468
- LibKa0s/LibKa0s/SimPanel.lua:504-540
- LibKa0s/LibKa0s/SimTimeline.lua:539-546
- LibKa0s/LibKa0s/SimTimeline.lua:587-596
- LibKa0s/LibKa0s/Sim.lua:548-565
- MultiMeters/settings/Slash.lua:138-139
- MultiMeters/modules/Sim.lua:216-229
- MultiMeters/core/LauncherSetup.lua:353-357
- DpsRace/tests/test_sim.lua:26-29
- DpsRace/tests/test_sim.lua:325-393
- DpsRace/tests/test_sim.lua:441-534
- DpsRace/tests/test_slash.lua:329-357
- DpsRace/tests/test_launcher.lua:61-69
- Ka0sAddonsCommonTasks/docs/2026-11-03-SMOKE_ROUND4/06_SMOKE_TESTS.md:42

### Owner questions

- Racing speed: should the Racing step play the 30 s sample race at real speed (about 30 s, with the last-10 s countdown at one number a second), even though in round 4 you asked for about 10 s? The alternative is a shorter sample race, but the 10 s countdown would then be most of it, and the sample history's bests sit on 0:30 boards. Recommended: real speed, 30 s, keeping MultiMeters' fight steps at 10 s.
- After the buzzer: should the sim also play Stop!, the tail and the result read at real speed (the Result card about 6.7 s after the buzzer, and about 20 s for the 'sticky' scenario so the drop-combat hint can show), then hold the card 4 s before the Results window? Today the card arrives 1 s after the buzzer and the window 1 s later. Recommended: yes, real speed throughout, with the step delay only between instant steps.
- `/dr sim died` (scenario typed): should it start that scenario at once, like `/mm sim start dungeon`, or only open the idle panel with 'died' picked? Picking without starting needs a small LibKa0s addition, because the panel has no member to set the picker's choice. Recommended: start at once; bare `/dr sim` opens the idle panel.

## header-darker (item 1: LootHistory, BankLedger, DropWatcher and WhatGroup headers "a bit darker")

### Findings

The screenshots are Ka0s Default. In images 31, 32 and 44 the band has a gold title and an olive-gold vertical gradient. Sampled pixels run from about #312400 at the top to #150E00 at the bottom (31.png at x=300; 32.png and 44.png read the same). That is round 4's option E as the client renders it, with some gamma loss and the blue channel crushed. The library paints the band; no host does. LootHistory (modules/Browser.lua:71 NS.Skin.Shell), BankLedger (modules/Browser.lua:980 and modules/Export.lua:401 NS.Skin.TitleBar), DropWatcher (core/CoreSetup.lua:101 lib.ApplySkin to Shell) and WhatGroup (modules/FrameLayout.lua:62-63 NS.ApplySkin plus Look.TitleBar) all read these tokens:
- LibKa0s/LibKa0s/SkinDefs.lua:486 `title.bg` = #2C2408 opaque. This is the flat blend that flat readers use.
- SkinDefs.lua:487 `title.bgTop` = #3A2F0A.
- SkinDefs.lua:488 `title.bgBottom` = #1F1905.
- The title text is GOLD #FFD100 (SkinDefs.lua:296 and :327).

So the root cause is a value choice, not a bug. Option E was chosen against a black band (R4_SIGNOFF.md:5 and :19). Next to the near-black body (win.bg 0.06,0.06,0.08 at 0.92 over black, which is #0E0E12) it now reads a little too bright.

Every place the values are pinned:
1. LibKa0s/LibKa0s/SkinDefs.lua:483-488, the values and their comment.
2. SkinDefs.lua:526, the picker's second swatch `"#2c2408"`.
3. LibKa0s/tests/test_skin_defs.lua:800-802, exact hex pins for top, bottom and blend, plus :810 for swatch[2]. The comment at :791-795 cites them.
4. test_skin_defs.lua:774-789: `title.bg` must sit within 1/255 of the stops' midpoint on every channel. This applies to every skin.
5. test_skin_defs.lua:803-809: both stops opaque, and each stop's WCAG luminance above the body's.
6. test_skin_defs.lua:745-772: each Ka0s Default stop (via bandStops) must sit 5% or more off the body on its largest channel (the apart() helper at :692), and the divider rule must sit 10% or more off each stop.
7. LibKa0s/tests/test_skin_paint.lua:28-29 reads the stops live through F.tok, so it needs no edit.
8. MultiMeters/core/SkinSetup.lua:167, `NS.SKIN_FALLBACK["title.bg"]` = 0x2c,0x24,0x08. MultiMeters/tests/test_skinsetup.lua:336-350 holds it equal to the vendored live value, so it turns red until both move in the same commit. MultiMeters/modules/Window_Header.lua:223 and :448 draw `title.bg` flat as the meter header strip, so that strip darkens too.
9. Docs:
   - LibKa0s/docs/api/Skin/version-15.1.26.8.17.16.17.4.9-docs.md:714-716, the current Ka0s Default token table.
   - LibKa0s/CHANGELOG.md:24, the unshipped SkinDefs minor 26 entry.
   - LibKa0s/docs/releasing.md:1150, the R4 "hosts owe" record. That is history, so add a new paragraph rather than editing it.
   - LibKa0s/docs/automated-tests/20261103-140451/ANALYSIS.md:35, a frozen bundle. Leave it.
10. Host smoke docs that quote the hexes:
   - LibKa0sSkinTester/docs/smoke-tests.md:244 (SHOW-45)
   - AuraMaster/docs/smoke-tests.md:2680
   - BankLedger/docs/smoke-tests.md:1371-1372
   - PanelMaster/docs/smoke-tests.md:1329-1330
   - WhatGroup/docs/smoke-tests.md:1060 and :1064
   - MultiMeters/docs/smoke-tests.md:2002 (SKIN-44, #2C2408 twice)
   - DpsRace/docs/smoke-tests.md:846

No other host keeps a copy of the band. A grep of all 16 addons plus WowAddonStandards, excluding libs/ and tests/_kit, found MultiMeters' fallback as the only code copy. tools/skin_gallery.py pins nothing.

The test constraints bound how dark the band can go. With the body at #0E0E12 (L 0.0046) and the rule at about 0.212,0.212,0.24:
- The binding test is "lighter than the body" (test_skin_defs.lua:807-808). The bottom stop needs WCAG L above 0.0046, so about #131002 is the floor.
- The 5% apart() test passes easily, because a dark gold band differs from the bluish body by about 0.06 in the blue channel. That means apart() no longer guards the bottom stop perceptually.
- The rule gap passes (0.21 or more) for every candidate below.

Current option E, for reference. Gold contrast: top 9.0:1, blend 10.5:1, bottom 12.0:1. Red-channel gap from the body: top 0.172, bottom 0.066.

Three candidate sets, each blend checked to within 1/255 of the midpoint, with gold #FFD100 contrast:
- **Set 1, subtle (about 20% less luminance):** top #322808, bottom #1B1604, blend #271F06. Gold contrast 10.0 / 11.2 / 12.4. Red gap from the body: top 0.141, bottom 0.051.
- **Set 2, medium (about 35-40% less luminance), recommended:** top #2C2307, bottom #181304, blend #221B06. Gold contrast 10.6 / 11.7 / 12.7. Top 0.117 off the body; bottom L 0.0067 against the body's 0.0046.
- **Set 3, strong (about 50% less):** top #262006, bottom #141103, blend #1D1805. Gold contrast 11.1 / 12.1 / 12.9. Bottom L 0.0056, almost on the floor, so its lower edge nearly melts into the body.

All three pass every current test once the hex pins move. All keep the gold title at 10:1 or better, which is AAA.

Other skins: the token table (docs/api 17.4.9-docs.md:1553-1555) shows every other skin states its own `title.bg`, with `title.bgTop` and `title.bgBottom` set to none. So the change does not leak into them. One thing for the lead to check: SkinEUI.lua:115 FLAT_TOKENS clears `title.bgTop` and `title.bgBottom` when it derives from the Ka0s Default base (SkinEUI.lua:337-340). An eui-derived look that keeps the base `title.bg` would draw the new flat blend.

### Fix

This is a library change: data in SkinDefs, Ka0s Default only, inside the still-unshipped SkinDefs minor 26, so no minor bump. Steps:
1. In LibKa0s/LibKa0s/SkinDefs.lua:486-488, set the three tokens to the chosen set. The recommendation is Set 2: `title.bgTop` {0x2c,0x23,0x07}, `title.bgBottom` {0x18,0x13,0x04}, `title.bg` {0x22,0x1b,0x06}, all /255 and opaque. Update the comment at :483-485 to cite round 5 item 1.
2. Set the swatch at SkinDefs.lua:526 to `"#221b06"`.
3. Update the pins in LibKa0s/tests/test_skin_defs.lua:800-802 and :810, and its comment. Optionally add a regression line that the new stops sit darker than option E's.
4. Update docs/api/Skin/version-15.1.26.8.17.16.17.4.9-docs.md:714-716 and CHANGELOG.md:24. Add a "hosts owe" note to docs/releasing.md: MultiMeters' fallback, and every window under Ka0s Default darkens.
5. Re-vendor into all 16 addons. In MultiMeters, change core/SkinSetup.lua:167 to {0x22/255, 0x1b/255, 0x06/255, 1} in the same commit as the re-vendor, so test_skinsetup.lua:336-350 stays green.
6. Refresh the hexes quoted in the host smoke docs listed under findings, or add new round-5 smoke steps that supersede them, following each repo's convention.
7. Leave the frozen bundles alone.

Run each repo's green gate: lua tests/run.lua, plus ka0s-bounded luacheck . for LibKa0s and MultiMeters at minimum. Other skins stay unchanged.

### Sites

- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/SkinDefs.lua:483-488
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/SkinDefs.lua:526
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/tests/test_skin_defs.lua:745-772
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/tests/test_skin_defs.lua:774-789
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/tests/test_skin_defs.lua:791-811
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/tests/test_skin_paint.lua:28-29
- /mnt/d/Profile/Users/Tushar/Documents/GIT/MultiMeters/core/SkinSetup.lua:167
- /mnt/d/Profile/Users/Tushar/Documents/GIT/MultiMeters/tests/test_skinsetup.lua:336-350
- /mnt/d/Profile/Users/Tushar/Documents/GIT/MultiMeters/modules/Window_Header.lua:223
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/docs/api/Skin/version-15.1.26.8.17.16.17.4.9-docs.md:714-716
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/CHANGELOG.md:24
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/docs/releasing.md:1150
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/SkinEUI.lua:115
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0sSkinTester/docs/smoke-tests.md:244
- /mnt/d/Profile/Users/Tushar/Documents/GIT/AuraMaster/docs/smoke-tests.md:2680
- /mnt/d/Profile/Users/Tushar/Documents/GIT/BankLedger/docs/smoke-tests.md:1371-1372
- /mnt/d/Profile/Users/Tushar/Documents/GIT/PanelMaster/docs/smoke-tests.md:1329-1330
- /mnt/d/Profile/Users/Tushar/Documents/GIT/WhatGroup/docs/smoke-tests.md:1060-1064
- /mnt/d/Profile/Users/Tushar/Documents/GIT/MultiMeters/docs/smoke-tests.md:2002
- /mnt/d/Profile/Users/Tushar/Documents/GIT/DpsRace/docs/smoke-tests.md:846
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LootHistory/modules/Browser.lua:71
- /mnt/d/Profile/Users/Tushar/Documents/GIT/BankLedger/modules/Browser.lua:980
- /mnt/d/Profile/Users/Tushar/Documents/GIT/DropWatcher/core/CoreSetup.lua:101
- /mnt/d/Profile/Users/Tushar/Documents/GIT/WhatGroup/modules/FrameLayout.lua:62-63

### Owner questions

- How much darker? Recommended: Set 2 (#2C2307 to #181304, flat blend #221B06). It drops band luminance by about 35-40%, still reads olive-gold and clearly separate from the body, and gives gold title contrast of 10.6 to 12.7:1. Set 1 (#322808 to #1B1604) may hardly be noticed. Set 3 (#262006 to #141103) lets the bottom edge nearly merge with the body. The lead can decide this, or show the owner a three-swatch mockup like R4_MOCKUP.html if they want to pick.
- Should the other skins' headers darken too? Recommended: no. The praise and the ask are about Ka0s Default windows (all four screenshots are Ka0s Default), and the other skins' bands were signed off in round 4's mockup. Change only Ka0s Default.

## dropdown-close

### Findings

WHAT THE CONTROL IS. The first dropdown in the /st skin picker (images 46, 47) is not an AceGUI Dropdown, not MenuUtil, and not the library's Widgets dropdown or Selector. It is a hand-built toggle list inside the library's skin picker, LibKa0s/LibKa0s/OptionsSkinPicker.lua (PICKER_MINOR 9, Options major minor 37):
- The button is `buildDropdown`, OptionsSkinPicker.lua:979-997. It is a plain `CreateFrame("Button", nil, f, "BackdropTemplate")` painted with `P.Sk.Dropdown(dd)`. Its OnClick at :994 is `setOpen(not P.open)`.
- The list is `buildList`, :966-977. It is a plain `CreateFrame("Frame", nil, f, "BackdropTemplate")` at FULLSCREEN_DIALOG, painted `P.Sk.MenuFrame`, with rows from `makeRow` (:939-956).
- `setOpen(open, p)` is at :605-611. It runs `layout(p)`, and `layout` shows or hides the list at :555 (`if p.open then f.list:Show() else f.list:Hide() end`).

WHY R4-L1 DOES NOT COVER IT. R4-L1's watcher (OptionsCombat.lua:158-325, COMBAT_MINOR 4) is armed only by a post-hook on `AceGUI.SetFocus` (`lib.__armPulloutClose`, :306-320). `lib.__OnPulloutFocus` (:275-285) returns at once unless `openPullout(w)` (:200-205) finds an AceGUI widget with `w.open` and `w.pullout.frame`. The skin list never calls AceGUI:SetFocus and has no `.pullout`, so no GLOBAL_MOUSE_DOWN is ever registered for it.

The picker's own close paths are all explicit calls to `setOpen(false)`:
- a row pick (`pick`, :718)
- the window closing (`closed`, :812)
- a fresh show (:1177)
- a media or scope row change (`onRow`, OptionsSkinPickerRows.lua:86-92)
- a reset icon (`resetMedia`, OptionsSkinPickerRows.lua:101-102)
- the toggle itself (:994)

Even a press on the picker window's own body does not close the list. The window's OnMouseDown at :1107 calls only `dropFocus(mine)` (:519-529), and that clears an AceGUI focus held by one of the media rows. It never touches `p.open`. That matches the report exactly: an outside click does nothing, and a second click on the button toggles the list closed.

"CHECK THIS FOR ALL ADDONS". The bug is the same in all 16 addons. OptionsSkinPicker.lua (md5 73daaa31) and OptionsCombat.lua (md5 fdba0875) are byte-identical in LibKa0s and in every addon's libs/LibKa0s. Every addon's Skin picker has the same unclosable list, whether it is opened from settings, /st or the SkinNotice.

WHY IMAGE 48'S DROPDOWNS DO CLOSE. Each of the Skin Tester Showroom controls goes through a path that already closes itself:
- "Dropdown (click: MenuFrame)" is `W.Dropdown` (LibKa0sSkinTester/modules/ShowroomControls.lua:52). That is the shared Widgets menu, which registers GLOBAL_MOUSE_DOWN when it opens and runs `__OutsideClick` (LibKa0s/Widgets.lua:474-503, :544).
- "WowStyle1DropdownTemplate" (ShowroomControls.lua:123-129) is Blizzard's Menu, which closes itself.
- The AceGUI Dropdown and the Ka0sMedia_Font and Ka0sMedia_Statusbar pickers (ShowroomControls.lua:85, :112) are covered by R4-L1, because they sit on a Shell-painted surface (`lib.__onKa0sSurface`, OptionsCombat.lua:232-243).

SWEEP OF EVERY OTHER DROPDOWN-LIKE CONTROL (library and 16 addons, excluding libs/, tests/ and docs/). Only the skin list is uncovered:
1. Shared Widgets menu, covered. It is `lib.Dropdown` (Widgets.lua:746) and `lib.ContextMenu` (:757), both through `openMenu` (:536-546), which registers GLOBAL_MOUSE_DOWN and exempts the menu and its opener. Users:
   - LibKa0s SimPanel.lua:445, :454 (the scenario and size dropdowns)
   - LibKa0sSkinTester modules/Selector.lua:110 and ShowroomControls.lua:52
   - BankLedger modules/Browser.lua:179
   - DpsRace core/WidgetsSetup.lua:31, :82 (the Results sort and filter menus and the row context menu)
   - DropWatcher core/WidgetsSetup.lua:41
   - LootHistory core/WidgetsSetup.lua:127 (the filter bar)
   - PGFE core/WidgetsSetup.lua:29
   - MultiMeters modules/Export_Modal.lua:679 and modules/Window_Header.lua:1172 (the segment menu)
   - QuickComms modules/PreviewWindow.lua:160
2. Blizzard Menu and MenuUtil, which close themselves:
   - LibKa0s Launcher.lua:482-488
   - DpsRace core/WidgetsSetup.lua:88-96
   - DropWatcher core/Compat.lua:896
   - MultiMeters core/Compat.lua:577-582 and Window_Header.lua:1199
   - PGFE modules/Panel.lua:382, :447, :628 (WowStyle1DropdownTemplate)
   - LibKa0sSkinTester ShowroomControls.lua:123
3. AceGUI dropdowns on settings pages or Shell windows, covered by R4-L1:
   - LibKa0s OptionsAppearance.lua:648, OptionsTabs.lua:1137 (PageBanner), OptionsSkinPickerRows.lua:154 (the picker's Font and Texture rows, which are on the Shell-painted picker window via Core.ApplySkin at OptionsSkinPicker.lua:1055), OptionsMedia.lua:450
   - AbsorbTracker settings/UnitPanel.lua:223
   - AuraMaster settings/OptionsSetup.lua:104 (AuraMasterDropdown)
   - ConsumableMaster settings/CategoryAddByID.lua:73 and StatPriority.lua:363
   - DropWatcher settings/PageEditors.lua:195
   - KickCD settings/Spells_Rows.lua:249 and Spells_Header.lua:160
   - MultiMeters settings/Windows.lua:81
   - PanelMaster settings/PanelEditor.lua:540 and PanelEditorTabs.lua:172, :199, :356
   - QuickComms settings/IconBrowser.lua:441, :448 (parented to ctx.body at :624), Editors.lua:235 and Groups.lua:140, :440, :649
   - every addon's schema `widget = "Dropdown"` rows
4. Host row menus with their own GLOBAL_MOUSE_DOWN listener, which work:
   - LootHistory modules/BrowserTable.lua:972-984, :1087
   - BankLedger modules/LedgerTable.lua:907-919, :1016
   These duplicate the Widgets menu pattern but have no open defect.
5. Autocomplete and suggestion lists, which close on edit focus loss and so close on an outside click:
   - LibKa0s OptionsIdSuggest.lua:632-646
   - WidgetsAutocomplete.lua:301-305, :414-419

ROOT CAUSE. The skin picker's list is the one Ka0s pullout that is neither an AceGUI pullout nor the shared Widgets menu. Both R4-L1 and the Widgets menu reach a pullout only through their own open seams (AceGUI.SetFocus and `openMenu`), and the picker opens its list through neither.

TESTS THAT PIN CURRENT BEHAVIOUR (LibKa0s/tests):
- test_options_skin_picker.lua:148-181, "the list holds every skin...": the list starts closed (:153), a click opens it (:155-156) and a second click closes it (:179-180).
- test_options_skin_picker.lua:278-290, "a pick previews": the list closes on a pick (:286).
- test_options_pullout_close.lua:151-395, the 25 `pulloutCase` tests for R4-L1. Their behaviour must not change.
- test_widgets.lua:508-519 and :693-772, the Widgets menu outside-press contract.
No test asserts anything about an outside press on the skin list, so none goes red until one is written.

### Fix

Library only (LibKa0s Options major), then re-vendor into the 16 addons. No host code changes.

SMALLEST CORRECT FIX. Turn R4-L1's single-purpose watcher in OptionsCombat.lua into the one outside-press watcher for every Ka0s pullout that is not the Widgets menu:
1. In OptionsCombat.lua (COMBAT_MINOR 4 -> 5), add a small transient registry on `lib`: `lib.__OpenTransient(key, frames, close)` and `lib.__CloseTransient(key)`. `frames` lists the frames a press on is not outside, here the list and its opener button. Both functions share the existing hidden `lib.__pulloutWatch` frame and the same Core.SafeRegisterEvent registration.
2. Extend `lib.__OnPulloutPress` (:289-300) to do two things. It keeps its current AceGUI branch unchanged. It also walks the registered transients and, for each entry where the press is over none of its `frames` (the existing `mouseOver` helper, :262-265), calls `pcall(close)` and drops the entry. The watcher stops only when no AceGUI pullout is open and no transient is left, so the lazy let-go stays: a list closed by any other route is found hidden on the next press (`frames[1]:IsShown()` false) and is dropped without calling `close`.
3. In OptionsSkinPicker.lua (PICKER_MINOR 9 -> 10), have `setOpen` (:605-611) call `lib.__OpenTransient(p, { p.frame.list, p.frame.dd }, function() setOpen(false, p) end)` when it opens and `lib.__CloseTransient(p)` when it closes. Guard both with `if lib.__OpenTransient` for a mixed-copy load. The list opens on the dd's OnClick, which is the release, so the opening press has already gone by, as R4-L1's comment notes (OptionsCombat.lua:167-170).

This keeps "listened, never caught". A press on a media row's AceGUI dropdown closes the skin list, and that dropdown's release then opens its own pullout. A press on the window body (OnMouseDown :1107) now closes the list as well. It works in combat, because both frames are plain. The Ka0s-surface gate is unnecessary here: the picker is always a Ka0s window.

DO NOT MIGRATE the Widgets menu (a different major, working and pinned by test_widgets.lua) or the LootHistory and BankLedger row menus in this item. They already close. Folding them into the registry is optional cleanup and can be filed as a follow-up.

TESTS TO ADD (red before the fix):
- In test_options_skin_picker.lua: with the list open, a GLOBAL_MOUSE_DOWN with the mouse over neither the list nor the dd closes it.
- A press over the list (a row) or over the dd does not close it, so the dd's OnClick still toggles.
- A press on the window body closes it.
- A list closed by a pick lets go on the next press and calls nothing.
- With a media row's AceGUI pullout open as well, one outside press closes both.
- In test_options_pullout_close.lua: an AceGUI pullout and a transient open together, then one closed by a pick, and the watcher stays registered until both are gone.
- A version-skew case: OptionsSkinPicker minor 10 over OptionsCombat minor 4 (no `__OpenTransient`) keeps the old toggle-only behaviour without error.

Smoke step for the round 5 list: open the /st skin picker, open the skin list, then click (a) the window body, (b) the game world and (c) the Font dropdown. Each click closes the list, and (c) also opens the Font pullout. Repeat from one other addon's Skin picker.

### Sites

- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/OptionsSkinPicker.lua:605
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/OptionsSkinPicker.lua:555
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/OptionsSkinPicker.lua:966
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/OptionsSkinPicker.lua:994
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/OptionsSkinPicker.lua:1107
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/OptionsSkinPicker.lua:519
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/OptionsCombat.lua:275
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/OptionsCombat.lua:289
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/OptionsCombat.lua:306
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/Widgets.lua:536
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/OptionsSkinPickerRows.lua:86
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/tests/test_options_skin_picker.lua:148
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/tests/test_options_pullout_close.lua:151

### Owner questions

- With the skin list open, should Escape close only the list first and leave the picker window open? Today Escape closes the whole picker (UISpecialFrames, OptionsSkinPicker.lua:1129), and R4-L1 deliberately added no Escape handling. Recommended answer: no, leave Escape as it is (it closes the window), so it behaves the same as every other Ka0s dropdown.

## quickcomms-header

### Findings

WHICH SURFACE. Images 40 and 41 show the Comms Pad, which is a bar window. They do not show the radial dial. The evidence is the "Quick Comms: World" situation chip, the "-" collapse button, the "Solo" section title and the button grid. The header row and its collapse button are built in modules/Pad_Render.lua:752-780 (R.DressHeader), and the title text comes from modules/Pad.lua:359-377 (headerState: L["Quick Comms: %s"]). The radial dial's "header" is its secure hub button (modules/Dial*.lua; tests/test_layers.lua:182). The open/close animations spec (#13) covers the dial only, so it does not apply here.

HOW THE PAD HEADER IS BUILT. The pad root is a BackdropTemplate frame. It is first skinned with NS.SKIN (Pad.lua:288-289, whose comment reads "a pad has no title band"), and on every Apply it is dressed with its own skin table (Pad_Render.lua:595-603, R.ApplyWindowLook -> NS.ApplySkin(root, wl.skin)). Because a skin table is passed in, lib.ApplySkin never calls the owner's S.Shell (LibKa0s Core.lua:236-246: `S = skin == nil and lib.__SkinFacade(owner)`). As a result the library's top band (SkinPaint.lua:968-972, title.bg / title.bgTop / title.bgBottom) is never drawn on a pad. The header is a separate child BackdropTemplate frame (Pad.lua:292-307). It is anchored flush to the root's TOPLEFT/TOPRIGHT at 0,0 (Pad.lua:337-349, anchorEdge), so it sits on top of the window's 1px edge and its inner rule. It is painted flat through R.ApplyHeaderLook -> NS.ApplySkin(header, bandSkin(header)) (Pad_Render.lua:580-588, 609-628).

ROOT CAUSE, KA0S DEFAULT (image 40). bandSkin uses R.BAND_TOKENS = { bg = "qc.bandBg", edge = "qc.bandEdge", size = "qc.bandEdgeSize" } (Pad_Render.lua:471). The owner token qc.bandBg defaults to { 0, 0, 0, 0 } under Ka0s Default and follows title.bg only in other skins (core/SkinSetup.lua:149-155). qc.bandEdgeSize defaults to 0 under Ka0s Default. So under Ka0s Default the header has a transparent fill and no edge, by design, and it never picked up round 4's option E (title.bg #2C2408, gradient #3A2F0A to #1F1905, LibKa0s SkinDefs.lua:484-489). Pixel check on image 40 confirms it: the header rows (y=2..27) read (3,0,6), the same as the body.

ROOT CAUSE, OTHER SKINS (image 41, an Azeroth-like palette, so title.bg is darker than win.bg). The header does paint here, but only as a flat title.bg blend with a hairline edge. That is exactly how each section-title band paints, because both use bandSkin and BAND_TOKENS (Pad_Render.lua:580-588, 630-641). Pixel trace at x=300: the edge at y=0 is the window edge and the header's top edge on the same pixel; the header fill is (12,0,0) for y=1-27; a header bottom edge at y=28; win.bg shows through at y=29-33 as (33,16,1); the "Solo" band's edge is at y=34; its fill is (12,0,0), the same as the header, for y=35-49; its edge is at y=50. So the header and the section band look identical and stack as two boxed rows. There is no gradient (a backdrop color cannot draw one), and the header's top edge sits over the window edge instead of inside it. That is why the owner sees "no header element". LootHistory's band has no edge and sits inside the border.

HOW LOOTHISTORY PAINTS ITS HEADER. LootHistory modules/Browser.lua:982-999 builds a hand-made titleBar, then calls NS.Skin.TitleBar(titleBar). The library's prim.TitleBar (LibKa0s SkinPaintExtras.lua:110-127, TITLE = { fill = "title.bg", extra = true } at :67) fills through P.box (SkinPaint.lua:775-790). On a frame without a backdrop that is a region fill plus boxGradient (SkinPaint.lua:735-742), which draws title.bgTop over title.bgBottom. There is no border in the spec. The body is the owner Shell with noTopBar (Browser.lua:1123). Pixels in image 31 at the left edge (y=25): x=6 is the black edge (0,0,0), x=7 is the gray inner rule (50,49,52), and the band starts at x=8 (34,25,0). Down the column at x=600 the gradient runs from (49,36,0) at y=8 to (21,14,0) at y=42, with no rule under it.

EDGE AND GAP VERSUS LOOTHISTORY (item 2). The pad window's frame already matches LootHistory under Ka0s Default. On image 40's right edge, x=499 is black (0,0,0) and x=498 is the gray inner rule (47,45,54). This comes from R.SkinFor (Pad_Render.lua:511-525): flat 1px, qc.winEdge black (SkinSetup.lua:162), and innerLine win.inner when size==1. So the pad does NOT have the MultiMeters-style black strip from image 33. The only edge and gap problem is the header band: it is anchored at 0,0 over the edge (Pad.lua:346-347), and in every non-default skin it draws its own hairline box (Pad_Render.lua:482-484: a band with no stored thickness takes qc.bandEdgeSize = bar.borderSize). LootHistory's band sits 1px inside the edge, under the inner rule, with no edge of its own. Button padding is PL.PAD = 4 (Pad_Layout.lua:20), which is fine.

VERTICAL CENTRING (item 5, for the record). The situation text is anchored LEFT,0 on the header (Pad_Render.lua:759), so it is vertically centred. The "-" is a GameFontNormal glyph, 2 points larger (Pad_Render.lua:627), filling a 16px button anchored RIGHT,0 (Pad_Render.lua:763-767), so the button is centred. A "-" glyph naturally rides at mid-x-height, which is within a pixel or so of centre.

TESTS THAT PIN CURRENT BEHAVIOUR:
- tests/test_pad.lua:510-541: with T.ownLooks (FromSkin off), the header has no edge, bg alpha 0, and innerBorder alpha 0. This should stay green if the stored-value path is untouched.
- tests/test_skin_flip.lua:241-258: under another skin, drawn[inst.header].bg == title.bg (flat), and the header edgeSize == bar.borderSize ("the band takes the hairline a button wears"). This turns red with the fix.
- tests/test_pad_looks.lua:53-64 and :113-131: under WoW Default the header edge is not white, edgeSize <= 2 or == 2 (the art "Blizzard Tooltip" at 2), the fill is not white, and R.SkinFor(p.header, true, R.BAND_TOKENS) art and tint are checked. The edge assertions change if the header stops drawing an edge.
- tests/test_layers.lua:109-118: header level == root + 1.
- No test pins the qc.bandBg value directly (grep "qc.band" in tests/ only finds comments).

### Fix

HOST FIX, in QuickComms only. No library change is needed, because prim.TitleBar already draws option E and every skin's gradient, and records the frame for live repaint.

1. Give the header its own tokens instead of sharing the section bands' tokens (core/SkinSetup.lua NS.SKIN_TOKENS and Pad_Render.lua:470-471).
   - Add R.HEADER_TOKENS = { bg = "title.bg", edge = "qc.headEdge" }, with no `size` entry so that a skin's None draws no edge (edgeOf, Pad_Render.lua:482-484).
   - Ka0s Default then reads title.bg directly (#2C2408), not the transparent qc.bandBg.
   - Leave qc.bandBg, qc.bandEdge and qc.bandEdgeSize for the section bands only, so their Ka0s Default look stays "no band".

2. Paint the header fill through the library, the way LootHistory does.
   - In Pad.lua build(), add a plain Frame (NOT BackdropTemplate), inst.headBand, as a child of the ROOT (not of the header). If it were a child of the header it would draw over the header's FontStrings.
   - Set its level to the root's level, below the inner rule and the header (both at L+1), so the gray inner rule draws over the band as it does in LootHistory.
   - Anchor it inside the window edge. For down growth: TOPLEFT(root, inset, -inset) and BOTTOMRIGHT(header, -inset, 0). Mirror this for up growth in anchorEdge (Pad.lua:339-356). inset is wl.skin.insets.left (1 for the flat edge; the art inset for a nine-slice).
   - While pad.header.backgroundFromSkin is true and no class colour is set, call NS.Skin.TitleBar(inst.headBand) and draw the header's own backdrop CLEAR (in bandSkin for the header: background = CLEAR when following). Otherwise hide headBand and keep today's stored-colour backdrop.
   - The band has no .title/.text field, so TitleBar's justify (SkinPaintExtras.lua:121-126) does not touch the header text.
   - Under every skin the header then shows the gradient (Ka0s Default #3A2F0A to #1F1905; Ember, WoW Default and Midnight their own bgTop/bgBottom) and stays distinct from the section bands.

3. Draw no header edge while following the skin. This matches LootHistory and round 4's "no separator below header", and removes the double rule in image 41. A stored border style or thickness still draws.

4. Text alignment: keep the header text LEFT (Pad_Render.lua:759). Recommended because:
   - The pad is compact and its width is floored by R.HeaderMinWidth = PAD + text + gap + 16px collapse button + inset (Pad_Render.lua:787-793). Centring would need a symmetric reserve for the "-" on both sides, which widens every pad by about 20px and risks colliding with the LOCKDOWN chip and the "updates after combat" hint.
   - The owner asked for DpsRace's header to be left aligned (item 3a), so left matches the other compact HUD window.
   - Ka0s Default's title.align is CENTER, but that is for windows with a close button and spare width.

Tests:
- Update tests/test_skin_flip.lua:254-257 so that header fill == title.bg on the band, and the header backdrop is clear with no edge while following.
- Add a Ka0s Default case: headBand painted by TitleBar with title.bgTop/bgBottom, and the band inset 1px inside the root.
- Revisit the header edge asserts in tests/test_pad_looks.lua:59-64 and 113-131.
- Keep tests/test_pad.lua:510-541 green (the stored path).
- Add a test_layers case: headBand level == root level.

### Sites

- /mnt/d/Profile/Users/Tushar/Documents/GIT/QuickComms/modules/Pad.lua:288-307 (root skinned with a table, so no Shell top bar; header child frame)
- /mnt/d/Profile/Users/Tushar/Documents/GIT/QuickComms/modules/Pad.lua:337-356 (anchorEdge: header flush at 0,0 over the window edge)
- /mnt/d/Profile/Users/Tushar/Documents/GIT/QuickComms/modules/Pad_Render.lua:470-471 (BAND_TOKENS shared by the header and section bands)
- /mnt/d/Profile/Users/Tushar/Documents/GIT/QuickComms/modules/Pad_Render.lua:477-492 (edgeOf: a band takes the qc.bandEdgeSize hairline)
- /mnt/d/Profile/Users/Tushar/Documents/GIT/QuickComms/modules/Pad_Render.lua:580-628 (bandSkin, HeaderLook, ApplyHeaderLook: flat backdrop)
- /mnt/d/Profile/Users/Tushar/Documents/GIT/QuickComms/modules/Pad_Render.lua:748-793 (DressHeader: LEFT text, RIGHT 16px collapse; HeaderMinWidth)
- /mnt/d/Profile/Users/Tushar/Documents/GIT/QuickComms/core/SkinSetup.lua:149-155 (qc.bandBg transparent under Ka0s Default)
- /mnt/d/Profile/Users/Tushar/Documents/GIT/QuickComms/defaults/PadStyle.lua:46-56 (header defaults: bg alpha 0, FromSkin true, borderSize 0)
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LootHistory/modules/Browser.lua:982-999,1123 (NS.Skin.TitleBar(titleBar); Shell noTopBar)
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/SkinPaintExtras.lua:67,110-127 (prim.TitleBar)
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/SkinPaint.lua:735-790 (boxGradient, P.box), 950-972 (Shell top band)
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/Core.lua:157-172,236-246 (inner rule at 1px; Shell only when no skin table)
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/SkinDefs.lua:484-489 (option E title tokens)
- /mnt/d/Profile/Users/Tushar/Documents/GIT/QuickComms/tests/test_skin_flip.lua:241-258
- /mnt/d/Profile/Users/Tushar/Documents/GIT/QuickComms/tests/test_pad.lua:510-541
- /mnt/d/Profile/Users/Tushar/Documents/GIT/QuickComms/tests/test_pad_looks.lua:53-64,113-131
- /mnt/d/Profile/Users/Tushar/Documents/GIT/QuickComms/tests/test_layers.lua:109-118

### Owner questions

- Pad header text: keep it left aligned (recommended: the pad is compact, the '-' collapse button and the LOCKDOWN and 'updates after combat' chips share the row, and centring widens every pad by about 20px), or centre it like LootHistory's title?
- Section-title bands (the 'Solo' row): in non-default skins they currently draw the same title.bg fill and hairline box as the header, which is why image 41 reads as two stacked headers. Once the header gets the gradient, should section bands keep that flat title.bg box, or draw no band in every skin as under Ka0s Default? Recommended: no band in every skin, so the header is the only band.
- Header edge under skins that state a real bar border style (WoW Default's Blizzard Tooltip art at 2px): drop it so the header matches LootHistory's borderless band (recommended), or keep the art on the header there?

## header-centering (item 5): vertical centring of title text, glyphs and buttons on the window header band, PGFE first, then every window in all 16 addons and all skins

### Findings

I only read files. Nothing was changed, committed, stashed or checked out. I did not open Outfitter.

## 1. PGFE: the root cause is anchoring, not the font

**Measured in the screenshots.** I scanned the bright pixel rows of the title and the arrow.
- Image 42 (Ka0s Default): the title glyphs span rows 11-21, centre about 16. The chevron spans rows 17-25, centre about 21. The title sits about 5 screen px high.
- Image 43: the title spans rows 10-23, where the bottom rows are the descenders of "p" and "G". The arrow spans rows 16-24, centre about 20. The title again sits about 4-5 px high.

**The band.** S.Shell paints the title band at `inset` from the top, `title.height` tall:
- LibKa0s/LibKa0s/SkinPaint.lua:932-950 (`band`) and 967-972 (`h = T["title.height"] or 30`).
- `inset` is `win.borderSize` for a flat edge and 1 otherwise (SkinPaint.lua:1019 and 1027).
- So the band's centre is at `-(inset + h/2)`. That is -16 under Ka0s Default (inset 1, h 30). Under the skin registered at SkinDefsOthers.lua:710, whose edge is `edge(2, "flat", …)`, it is -17.

**The arrow is right.** PremadeGroupsFilterExtension/modules/Panel.lua:856 places it with `TOPRIGHT, -(inset+ARROW_PAD), -(inset + (h - ARROW_BTN)/2)`, which puts its centre exactly on the band's centre. `titleBand()` at Panel.lua:812-818 re-derives the band from the tokens, and the EllesmereUI case is 0 and 25.
- Pinned by PGFE tests/test_skin.lua:207-240, "min/max button … centered on the title band in every skin". It loops all 9 skins.

**The title is wrong.** `centerTitle` (Panel.lua:964-970) re-anchors only the template's TitleContainer, `TOPLEFT/TOPRIGHT` at y = -1. It never touches TitleContainer's height or TitleText's own anchor. `alignTitle` (Panel.lua:869-878) only calls SetJustifyH. So the text keeps Blizzard's PortraitFrameBaseTemplate anchor:
- TitleContainer is 20 px tall.
- TitleText is anchored `TOP y=-5` inside it, with LEFT and RIGHT spanning it. This is from my memory of Blizzard's SharedUIPanelTemplates.xml, which is not in any repo. Confirm it in game with `/dump PremadeGroupsFilterExtensionPanel.TitleContainer.TitleText:GetPoint(1)` or /fstack.
- The text box's top is therefore about 6 px down, and for a 14 px title its centre is about -13. The band's centre is -16, so the text is about 3 UI px high. That matches the screenshots once you allow for the UI scale.
- Pinned only by PGFE tests/test_panel_layout.lua:558-569, "the title is centered on the whole header". It checks the symmetric x inset and `y1 == y2`. Nothing pins the title's vertical position.

**The font is not the cause.** I measured the shipped TTFs in LibKa0s/LibKa0s/media/fonts offline with fontTools, comparing each face's cap-height centre with its line-box centre at 14 px:

| Face | hhea | Win metrics |
|---|---|---|
| Prototype-Regular (Ka0s Default title) | -0.02 px | |
| Expressway-Bold | -0.49 px | |
| OpenSans-Bold | -0.43 px | |
| SegoeUI-Bold | -0.90 px | |
| FiraSans-SemiBold | +0.15 px | |
| AvantGarde-Regular | +1.29 px | -0.08 px |
| DorisPP-Bold | +1.27 px | -0.18 px |
| Emblem-Regular | +1.37 px | +0.31 px |

Image 42 is Ka0s Default (Prototype, 0 px), so the whole visible offset there comes from the anchor. Font metrics add at most about ±1 px, depending on which metric set the client's FreeType uses.

## 2. Sweep of every header in the collection

**On the band centre (correct):**
- LibKa0s DebugLogWindow.lua:447 (title CENTER of a drag bar at 1,-1 with height TITLE_H; bar at DebugLogWindow.lua:328-330), with close, clear and copy anchored RIGHT at y 0 (DebugLogWindow.lua:232 and 259-260).
- LibKa0s WidgetsCopyWindow.lua:190-215 (bar at 1,-1; title CENTER; close RIGHT -6,0).
- LootHistory modules/Browser.lua:964-1015 (title CENTER of titleBar at 1,-1; close RIGHT -6,0). This is the owner's reference.
- BankLedger modules/Browser.lua:954-993, SessionWindow.lua:545-573 and Export.lua:390-404 (S.TitleBar with `place`, close RIGHT -6,0).
- DropWatcher modules/WindowTitleBar.lua:335 and 357-371, plus CompactChrome.lua:444.
- WhatGroup modules/FrameLayout.lua:37-63, through S.TitleBar `place`.
- MultiMeters modules/Export_Modal.lua:194-214.
- LibKa0sSkinTester modules/Showroom.lua:239-253.
- QuickComms modules/PreviewWindow.lua:204 and 216 (CENTER at -band/2; close at -(band-18)/2).
- The S.TitleBar `place` path itself (LibKa0s SkinPaintExtras.lua:97-108) anchors the text by `title.align` at y 0 of the bar, so it is centred by construction.

**Centred, but on y = -1 or y = 0 rather than the band's real top (1-2 px high when `win.borderSize` is 2):**
- Every bar hard-coded at `SetPoint("TOPLEFT", 1, -1)` (or 0,0 in WhatGroup and SkinTester) while the band sits at `inset`.
- LibKa0s PerfPanel.lua:258 and 283, and SimPanelRender.lua:168 and 175, hard-code `-(1 + TITLE_H/2)`. TITLE_H is a file-load constant of 30 (PerfPanel.lua:54, SimPanelRender.lua:70).
- DpsRace modules/Hud.lua:400, 409, 518 and 522, Results.lua:191 and 197, Results_Gear.lua:271 and 276, and Results_Timeline.lua:206 and 211 all use `-HEADER_H/2 = -15` with no inset. That is 1 px above the band centre under Ka0s Default and 2 px under the 2 px border skin, though title and controls agree with each other. HEADER_H is `Style.TITLE_BAR_H = NS.Skin.Token("title.height") or 30`, read once at load (modules/Style.lua:216).

**Off-centre by construction (template or TOP anchors):**
- PGFE (above): about 3 px high.
- QuickComms settings/ModalWindow.lua:58, 99-104: SettingsFrameTemplate under S.Shell's 30 px band. `NineSlice.Text` and `ClosePanelButton` keep Blizzard's template anchors. S.TitleBar is called without `place`, so it only justifies. This is the same class of bug as PGFE. I did not verify Blizzard's exact offsets.
- QuickComms ModalWindow.lua:132 (fallback close at -12,-12) has no band.
- MultiMeters modules/Window_Header.lua:315-320 (`TitleRowMid`) and 383-384, with HeaderControls.lua:496 and 519, centre the title and buttons on `TitleBandHeight()`, which is 0..30 from the frame top (pad 6 + 26 - BAR_INSET 2, Window_Header.lua:329-333). But the tinted strip a player sees, `headerBG`, spans pad..pad+titleHeight, that is 6..32 (Window_Header.lua:452-454). So the text and buttons sit about 4 px above the visible strip's centre. S.Shell is `noTopBar` there (Window_Frame.lua:83-91). This is the same 6 px `pad` gap the owner calls the black "inner border" in item #2, so one fix covers both.
- LibKa0s OptionsSkinPicker.lua:1039-1040 puts the title TOPLEFT/TOPRIGHT at -8 and 1059 puts the close TOPRIGHT at -6,-6. Both are TOP-anchored and not tied to any band: close centre -15, text centre about -15, band -16. Roughly 1 px off and font-dependent.
- DropWatcher modules/OfferPanel.lua:134-143 and DetailCard.lua:688-691 put the title TOPLEFT at -9 and the close TOPRIGHT at -6,-6. These popovers use ApplySkin and have no S.Shell band, so they are TOP-anchored, roughly aligned, and font-dependent.
- LibKa0s SkinAce.lua:526 only recolours the AceGUI Frame `titletext` and never re-anchors it. No Ka0s window was found using an AceGUI Frame header.
- LibKa0s Options.lua:580-581 and 733 is the settings-page heading (TOP -20), not a window band. It is out of scope.

**No window header of their own** (only the library tool windows: console, perf, sim, copy, skin picker): AbsorbTracker, AuraMaster, ConsumableMaster, KickCD, PanelMaster, PartyFrameEnhanced and PrettyChat. Every addon's `MakeCloseButton` goes through Core (e.g. AuraMaster core/CoreSetup.lua:173). It is an 18 px button with centred art (Core.lua around 286-306).

## 3. What the headless kit can measure

- The paint mock records anchors: tests/_kit/mock_paint.lua:136 (`COMMON:GetPoint`) and 141 (`GetHeight`).
- `FONTSTRING:GetStringHeight()` always returns 0 (mock_paint.lua:241). Text metrics cannot be measured headless, only anchor shape.
- CENTER, LEFT and RIGHT anchors are vertically centred by definition, so asserting anchor shape is enough.

**Tests that pin today's behaviour:**
- LibKa0s tests/test_title_shape.lua:105-127 (`assertCenteredOnBand` pins `y = -(1 + h/2)` for the perf and sim panels, and the close at `-(1 + (h-18)/2)`), plus its console and copy-window height cases.
- PGFE tests/test_skin.lua:207-240 (the arrow on the band, all skins), test_panel_layout.lua:558-569 (title container x symmetry) and :621-635 (header click band y 0).
- MultiMeters tests/test_headercontrols.lua:180 and test_window_header.lua:160 (TitleRowMid against BAR_INSET).
- DpsRace tests/test_header_rule.lua:82-115 covers separators only, not centring.
- Host chrome suites that read title anchors: DropWatcher tests/test_compact_chrome.lua, test_window_shell.lua and test_skin_host.lua; WhatGroup tests/test_frame_skin.lua; QuickComms tests/test_skin_windows.lua; BankLedger tests/test_skin_chrome.lua.

### Fix

## Library-level rule (LibKa0s, next minor)

**The rule:** every header child (title FontString, close, header buttons, chevrons, badges) is anchored by a LEFT, CENTER or RIGHT point to the title band's own frame at y = 0. A TOP anchor with a hard-coded offset is not allowed. The band is the single source of the band's geometry.

**1. Band frame in SkinPaint.** S.Shell creates and maintains an invisible holder frame, `frame.__ka0sBand` (exposed as `S.Band(frame)`, recorded like the other regions).
- Anchored TOPLEFT (inset, -inset) and TOPRIGHT (-inset, -inset), with height `title.height`. This is the same arithmetic as `shellBands` (SkinPaint.lua:1027 and 967).
- Under the EllesmereUI source it is 0 and 25, the case PGFE's `titleBand()` handles today.
- It is re-laid on every skin switch, because S.Shell is replayed. Anything anchored to it moves with no host code.
- It is kept even when `noTopBar` is set (MultiMeters, DropWatcher, WhatGroup), because geometry is not fill. Optionally accept `opts.bandHeight` for a host with its own band height.

**2. Header placement opts.** S.Shell `opts.header = { title = fs, left = {…}, right = {…}, align? }`, or a companion `S.HeaderPlace(frame, spec)`.
- The library anchors the title by `title.align` (LEFT, CENTER or RIGHT), in from the edge by the reserve, exactly as SkinPaintExtras.lua `place` does today but on the band.
- It chains the right-hand controls `RIGHT, band, "RIGHT", -6 - pitch*i, 0` and the left ones the mirror way.
- S.TitleBar `place` keeps working and becomes the same code path.
- This also gives DpsRace item 3a (a left-aligned title) for free through `align = "LEFT"`.

**3. Library tool windows.** In PerfPanel.lua:258 and 283, SimPanelRender.lua:168 and 175, DebugLogWindow.lua:328-330, WidgetsCopyWindow.lua:190-195 and OptionsSkinPicker.lua:1039-1059, anchor to `S.Band` instead of a hard-coded 1 or -8. This is only a 1-2 px change, visible only under the 2 px border skin. The skin picker moves from TOP anchors to band-centred.

**4. Baseline compensation.** Do not add a per-face nudge now. The measured cap-centre offsets of the shipped faces are at most about ±1.4 px at 14 px (Prototype 0). If smoke shows a face off by 1 px or more, add an optional per-face `yNudge` to the Media font registry, which P.font applies to the `title` role only (SkinPaint.lua:489). It cannot be tested headless beyond "the nudge is applied".

## Host fixes (once the library ships)

**PGFE** modules/Panel.lua:964-970 and 869-878. Re-anchor TitleContainer to the band: `SetPoint("TOPLEFT", band, "TOPLEFT", 24-inset, 0)`, `SetPoint("BOTTOMRIGHT", band, "BOTTOMRIGHT", -(24-inset), 0)`. Then `TitleText:ClearAllPoints()`; `SetPoint("LEFT", tc, "LEFT")`; `SetPoint("RIGHT", tc, "RIGHT")`, which centres it vertically. Keep the justify from `title.align`. Optionally move the min/max button to `RIGHT, band, RIGHT, -4, 0` and retire the local `titleBand()` copy (Panel.lua:812-818).

**Smallest host-only fix for PGFE, if the library change is deferred:** in `centerTitle`/`placeMinMax`, give TitleContainer `TOPLEFT (24, -inset)` / `TOPRIGHT (-24, -inset)` plus `SetHeight(h)` from `titleBand()`, and re-anchor TitleText LEFT and RIGHT on the container.

**QuickComms** settings/ModalWindow.lua:99-104. Re-anchor `NineSlice.Text` and `ClosePanelButton` to the band, either through S.TitleBar `place` on a band or through S.HeaderPlace.

**MultiMeters.** Fold `TitleBandHeight`/`TitleRowMid` (Window_Header.lua:315-333) and `headerBG` (Window_Header.lua:452-454) onto one band starting at the shell inset. This is shared with the item #2 "inner border" fix. Then anchor the title and HeaderControls (HeaderControls.lua:519) to that band's LEFT and RIGHT at y 0.

**DpsRace.** Anchor the title and controls (Hud.lua:400 and 409, and the Results, Gear and Timeline files) to `S.Band(f)`. This also unblocks 3a, with `align = "LEFT"` at Hud.lua:518.

**DropWatcher, WhatGroup, BankLedger, LootHistory, SkinTester.** Already centred on their bar. Moving them to the band changes at most 1 px under the 2 px border skin. Low priority, but include them for "all windows, all skins".

**DropWatcher popovers** (OfferPanel.lua:134-143, DetailCard.lua:688-691). They have no band. Either give them one (S.Shell plus band, if the owner wants a header strip) or centre the title and close on a 30 px virtual band, LEFT/RIGHT at y = -15.

## Tests (headless, anchor-shape)

**Kit assertion.** Add `K.assertOnBand(frame, region, what)` to tests/_kit/asserts.lua. It asserts the region has exactly one vertical anchor, its point is LEFT, CENTER or RIGHT, its relativeTo is `S.Band(frame)`, and y == 0. Alternatively it accepts the equivalent frame-relative form `relPoint TOP*`, `y == -(inset + h/2)`.

**Band test.** Add LibKa0s tests/test_header_band.lua. For every registered skin (loop `Skin:Skins()`, as PGFE test_skin.lua:213 does), including the 2 px flat border skin, a nine-slice skin and the EllesmereUI source, assert that the band holder sits at (inset, -inset) with height `title.height`, and that it re-lays on a switch.

**Update test_title_shape.lua:105-127** so the perf, sim, console, copy and skin-picker windows assert `assertOnBand` for their title and close.

**Per-host test,** looping all skins through the kit's skin_switch.lua:
- PGFE: TitleText LEFT/RIGHT on a band-height container; the arrow on the band.
- QuickComms: ModalWindow text and close on the band.
- MultiMeters: title, session line and every header control on the band. `headerBG` equals the band.
- DpsRace: HUD, Results, Gear and Timeline titles and controls on the band; title `align` LEFT honoured.
- DropWatcher, WhatGroup, BankLedger, LootHistory, SkinTester: title and close on the band.

Each test should be red first: against today's PGFE the TitleText anchor is the template's TOP and the test fails.

**Cannot be tested headless:** glyph baselines (GetStringHeight is 0 at mock_paint.lua:241). Add an owner smoke step to the round 5 smoke list: every window, every skin, title cap-centre against the chevron or close centre within 1 px.

### Sites

- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/SkinPaint.lua:932-972,1019-1031
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/SkinPaintExtras.lua:93-127
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/PerfPanel.lua:54,258,283
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/SimPanelRender.lua:70,168,175
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/DebugLogWindow.lua:76,232,259-260,328-330,447,485
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/WidgetsCopyWindow.lua:178,190-215
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/OptionsSkinPicker.lua:1038-1061
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/SkinDefsOthers.lua:710
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/tests/_kit/mock_paint.lua:136,141,241
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/tests/test_title_shape.lua:105-127
- /mnt/d/Profile/Users/Tushar/Documents/GIT/PremadeGroupsFilterExtension/modules/Panel.lua:787-818,849-878,958-970,1005-1009
- /mnt/d/Profile/Users/Tushar/Documents/GIT/PremadeGroupsFilterExtension/tests/test_skin.lua:207-240
- /mnt/d/Profile/Users/Tushar/Documents/GIT/PremadeGroupsFilterExtension/tests/test_panel_layout.lua:558-569,621-635
- /mnt/d/Profile/Users/Tushar/Documents/GIT/QuickComms/settings/ModalWindow.lua:58,99-104,132
- /mnt/d/Profile/Users/Tushar/Documents/GIT/QuickComms/modules/PreviewWindow.lua:204,216
- /mnt/d/Profile/Users/Tushar/Documents/GIT/MultiMeters/modules/Window_Header.lua:69,315-333,383-384,452-454
- /mnt/d/Profile/Users/Tushar/Documents/GIT/MultiMeters/modules/HeaderControls.lua:496,519
- /mnt/d/Profile/Users/Tushar/Documents/GIT/MultiMeters/modules/Window_Frame.lua:83-91
- /mnt/d/Profile/Users/Tushar/Documents/GIT/DpsRace/modules/Style.lua:216
- /mnt/d/Profile/Users/Tushar/Documents/GIT/DpsRace/modules/Hud.lua:41,399-409,518-522
- /mnt/d/Profile/Users/Tushar/Documents/GIT/DpsRace/modules/Results.lua:191,197
- /mnt/d/Profile/Users/Tushar/Documents/GIT/DpsRace/modules/Results_Gear.lua:271,276
- /mnt/d/Profile/Users/Tushar/Documents/GIT/DpsRace/modules/Results_Timeline.lua:206,211
- /mnt/d/Profile/Users/Tushar/Documents/GIT/DropWatcher/modules/WindowTitleBar.lua:335,357-371
- /mnt/d/Profile/Users/Tushar/Documents/GIT/DropWatcher/modules/OfferPanel.lua:134-143
- /mnt/d/Profile/Users/Tushar/Documents/GIT/DropWatcher/modules/DetailCard.lua:688-691
- /mnt/d/Profile/Users/Tushar/Documents/GIT/WhatGroup/modules/FrameLayout.lua:37-63
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LootHistory/modules/Browser.lua:964-1015
- /mnt/d/Profile/Users/Tushar/Documents/GIT/BankLedger/modules/Browser.lua:954-993
- /mnt/d/Profile/Users/Tushar/Documents/GIT/BankLedger/modules/SessionWindow.lua:545-573
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0sSkinTester/modules/Showroom.lua:239-253

### Owner questions

- Centring reference: should the title be centred on the band's geometric middle (recommended: anchor-exact, the same in every skin, testable headless), or should we also add per-font baseline nudges for the faces measured up to about 1.3 px off (Emblem, Doris PP, Avant Garde, Segoe UI)? Recommendation: geometric centre now. Add a per-face nudge only if your smoke shows a face visibly off after the anchor fix.
- Some popovers have no header band today: the DropWatcher 'Who could use this?' offer panel, its note editor, and the QuickComms fallback modal. Should they get the full title band like the main windows (recommended, for consistency with 'all addon windows'), or stay band-less with the title and close just vertically aligned with each other?
- When EllesmereUI paints an addon, its shell bar is 25 px and flush with the top, not the Ka0s 30 px band. Should header children centre on EllesmereUI's 25 px bar under that source (recommended, since it is the strip you can see), or on the Ka0s band?

## dpsrace-header

### Findings

I checked the code. Rendering is inferred from the owner's screenshots. I changed nothing.

ROOT CAUSE (item 3, images 34-37): DpsRace never builds a title-bar frame. Every DpsRace window relies on S.Shell's own "top" band, and Shell paints that band as a BACKGROUND-layer texture on the window frame itself. All four DpsRace windows are BackdropTemplate frames, and the backdrop's own pieces (its Center fill is win.bg, alpha 0.92 under Ka0s Default) evidently draw over that band. So title.bg/bgTop/bgBottom are painted (the headless test confirms the colour) but cannot be seen, in every skin.
- The band: LibKa0s/LibKa0s/SkinPaint.lua:936-952 (band(), P.tex(rec,key,frame,"BACKGROUND",sublevel)) and :966-971 (top band, sublevel -5, height title.height 30).
- Backdrop frames take the shellBackdrop arm, so Core.ApplySkin sets backdrop bg = win.bg: SkinPaint.lua:987-991 and :1046-1050 (P.hasBackdrop at :278-280). Frames without a backdrop take shellRegions instead (fill at BACKGROUND -8, :981-984), and that fill sits under the band.
- DpsRace HUD: CreateFrame(...,"BackdropTemplate") at modules/Hud.lua:463. f.title is a FontString on the frame itself (:406-410), with no bar. NS.ApplySkin(f) at :474 goes to core/CoreSetup.lua:92-94, then lib.ApplySkin(f,nil,"DpsRace") (LibKa0s Core.lua:231-240), then S.Shell(f) with no opts, so the top band is on the backdrop frame.
- Results: BackdropTemplate at modules/Results.lua:274, title on the frame at :190-192, NS.ApplySkin(f) at :299.
- Ability timeline: BackdropTemplate at modules/Results_Timeline.lua:448, title at :205-207, NS.Skin.Shell(f, Timeline.SHELL) at :459. Timeline.SHELL (:177) remaps only bg/inner/divider, so it is the same band.
- Gear view: same pattern, modules/Results_Gear.lua:270-272, :349 and :363 (Gear.SHELL = Timeline.SHELL, :267).

WHAT THE SCREENSHOTS SHOW. Every window whose header the owner sees uses a CHILD title-bar frame painted by S.TitleBar, with Shell called under noTopBar. A child frame draws above all of its parent's regions, so its fill shows:
- LootHistory: modules/Browser.lua:963-966 (titleBar child, inset 1), :982-984 (title on the bar), :999 (NS.Skin.TitleBar(titleBar)), :1123 (Shell noTopBar).
- DropWatcher: modules/Window.lua:560 and modules/WindowTitleBar.lua:372.
- WhatGroup: modules/FrameSkin.lua:81-83.
- BankLedger: modules/Browser.lua:980.
- MultiMeters: modules/Window_Frame.lua:83-84.
- Skin Tester showroom: modules/Showroom.lua:289-291.

The one band that does show without a child bar is PGFE's (image 42). Its frame is PortraitFrameTemplateMinimizable, which has no backdrop (modules/Panel.lua:1030, :1007), so the -5 band sits above the -8 fill. Every window that relies on Shell's band on a BackdropTemplate frame shows none:
- the DpsRace windows (34-37)
- the DpsRace sim panel (49) and the MultiMeters sim panel (50), both via SimPanelRender.lua:311
- the /st skin picker (46), via OptionsSkinPicker.lua:1055

I could not read Blizzard's Backdrop.lua offline to give the exact sublevel of the backdrop pieces. The screenshots are consistent on every window, though.

DEBUG WINDOW (37): library-built. It is a BackdropTemplate frame (DebugLogWindow.lua:554). Its title bar is a child drag frame (:444-447) that nobody hands to S.TitleBar. It is painted only through ctx.applySkin (:584), which is DebugLog.lua:305-312 calling core.ApplySkin(f,nil,owner), so it gets the same covered Shell band. DpsRace's descriptor (core/DebugLogSetup.lua:60) and LootHistory's (core/DebugLogSetup.lua:110) are the same: addonName only, with no skin and no applySkin. So the code gives LootHistory's console no band either. The premise that LootHistory's debug window has one is not backed by any screenshot in this bundle. In round 4, SR4-2 expected a band on `/bl debug`, but its Result cell is blank (docs/2026-11-03-SMOKE_ROUND4/06_SMOKE_TESTS.md:55). The same applies to the copy window (WidgetsCopyWindow.lua:165), the perf panel (PerfPanel.lua:297) and toasts (Toast.lua:220).

EDGE/GAP (item 2): DpsRace's edge already goes through the same shellEdges as LootHistory: win.border on the edge holder, plus win.inner inset 1 (SkinPaint.lua:912-928). The band inset is win.borderSize (1), which matches LootHistory's titleBar inset of 1 (Browser.lua:964-965). DpsRace draws no extra inner frame. The Results body is inset 1 (Results.lua:283-284) and the HUD content uses PAD 12 (Hud.lua:41). There is no MultiMeters-style black strip in images 34-36. The missing band is the whole difference from LootHistory, so no separate edge change is needed in DpsRace.

ITEM 3a (image 45): the plain HUD title is anchored CENTER on the frame's TOP at modules/Hud.lua:409. placeTitle re-centres it whenever test mode is off (:512-525: the unmarked branch at :521-523 uses CENTER/TOP and JustifyH CENTER). The four controls take about 94px on the right (:399-400, CONTROL_PITCH 22 at modules/Style.lua:220), which makes the title read as off-centre to the right. Test mode already has a LEFT-aligned arm at :517-520 (LEFT at TOPLEFT +10, RIGHT to ui.drag -4, JustifyH LEFT).

Corollary (not asked, unverified in client): the window gradient (win.bgTop/bgBottom, "grad" at BACKGROUND -7) and the tiled art (-6) on BackdropTemplate frames are probably covered the same way (SkinPaint.lua:955-965).

TESTS THAT PIN CURRENT BEHAVIOUR:
- LibKa0s tests/test_skin_paint.lua:98-111 pins the top band's colour (title.bg) on a backdrop window, but not its layer. The kit records layers: tests/_kit/mock_paint.lua:128-129, :262.
- tests/test_skin_paint.lua:113-126 (R4-SEP, no divider) is unaffected.
- DpsRace tests/test_preview.lua:139-143 asserts the plain HUD title is back to one CENTER point. This must change for 3a.
- tests/test_preview.lua:121-136 pins the marked LEFT/RIGHT/drag/JustifyH LEFT arm, which becomes the always arm.
- DpsRace tests/test_results_timeline_modal.lua:217-220 reads the Shell remap for the timeline.

### Fix

RECOMMENDED: fix it in the library, at the root cause, plus a one-file host change for 3a.

1. LibKa0s SkinPaint.lua band()/shellBands (:936-971). When P.hasBackdrop(frame), create the "top" and "bottom" bars in the BORDER layer (for example sublevel -8 and -7) instead of BACKGROUND -5. BORDER draws above every backdrop piece and below the host's ARTWORK and OVERLAY title text. Keep BACKGROUND for frames without a backdrop, so PGFE is unchanged. Bump the SkinPaint minor. Optionally handle "grad" and "art" the same way, but that also covers any BORDER regions the host draws in the body, so leave them out of this fix and file them separately.
   - What it fixes: all four DpsRace windows (HUD, Results, ability timeline, gear view), and in every addon the debug console, the copy window, the perf panel, the sim panels and the skin picker. DpsRace itself needs no change for item 3.
   - Ripple to settle in the same change: every caller of Core.ApplySkin(f,nil,owner) or S.Shell without noTopBar gains a 30px band. Those are Toast.lua:220 (DpsRace and DropWatcher toasts), DropWatcher modules/DetailCard.lua:686 and modules/OfferPanel.lua:214, and QuickComms modules/PreviewWindow.lua:231. Toasts should opt out: Toast.decorate should call the facade's Shell with { noTopBar = true }, because Core.ApplySkin cannot pass opts. The DropWatcher card and offer panel need a look: the card's title sits at -9 (DetailCard.lua:687-688), not centred in a 30px band.
   - Tests: in test_skin_paint.lua next to :98-111, assert that on F.window (a backdrop frame) the top band's __layer is "BORDER" and that a frame without a backdrop keeps "BACKGROUND". Add a Toast test that it draws no top band.

ALTERNATIVE (host only, smaller ripple, leaves library windows bandless). In each DpsRace window, copy LootHistory Browser.lua:963-999:
   - a child titleBar frame (TOPLEFT 1,-1 / TOPRIGHT -1,-1, height HEADER_H)
   - the title FontString created on the bar but kept as f.title (not bar.title, so S.TitleBar does not justify it)
   - controls and the drag strip parented to the bar
   - NS.Skin.TitleBar(bar), with Shell called under { noTopBar = true }. That means NS.Skin.Shell(f,{noTopBar=true}) instead of NS.ApplySkin(f) at Hud.lua:474 and Results.lua:299, and Timeline.SHELL / Gear.SHELL gaining noTopBar = true.
   For the debug console, DebugLogWindow.lua would still need the facade's TitleBar on its titleBar (:444) plus noTopBar, which is a library change anyway.

3a (host, DpsRace modules/Hud.lua): anchor the title LEFT always. In buildHeader (:409), use SetPoint("LEFT", f, "TOPLEFT", 10, -HEADER_H/2) plus a RIGHT anchor to ui.drag at -4 once the drag strip exists, and SetJustifyH("LEFT"). In placeTitle (:512-525), drop the CENTER arm so both states use the LEFT/RIGHT arm (only the text changes). Do not pass the title to S.TitleBar if the alternative is taken, because TitleBar justifies by the skin's title.align (SkinPaintExtras.lua:118-128), which is CENTER under Ka0s Default. Update tests/test_preview.lua:139-143 to expect two points (LEFT, then RIGHT to u.drag) and JustifyH LEFT in both states.

Vertical centre (item 5 overlap): the band spans y -1 to -31 (inset 1, height 30), so its centre is -16, while the DpsRace title and controls sit at -HEADER_H/2 = -15. That is 1px high. The item-5 sweep should anchor header contents at -(inset + h/2).

### Sites

- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/SkinPaint.lua:936-971
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/SkinPaint.lua:987-991
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/SkinPaint.lua:1037-1051
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/Core.lua:231-240
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/DebugLogWindow.lua:442-447
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/DebugLogWindow.lua:554
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/DebugLogWindow.lua:584
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/DebugLog.lua:305-312
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/Toast.lua:220
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/SimPanelRender.lua:311
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/OptionsSkinPicker.lua:1055
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/SkinPaintExtras.lua:110-129
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/tests/test_skin_paint.lua:98-111
- /mnt/d/Profile/Users/Tushar/Documents/GIT/DpsRace/modules/Hud.lua:406-410
- /mnt/d/Profile/Users/Tushar/Documents/GIT/DpsRace/modules/Hud.lua:463-474
- /mnt/d/Profile/Users/Tushar/Documents/GIT/DpsRace/modules/Hud.lua:512-525
- /mnt/d/Profile/Users/Tushar/Documents/GIT/DpsRace/modules/Results.lua:186-192
- /mnt/d/Profile/Users/Tushar/Documents/GIT/DpsRace/modules/Results.lua:274-299
- /mnt/d/Profile/Users/Tushar/Documents/GIT/DpsRace/modules/Results_Timeline.lua:177
- /mnt/d/Profile/Users/Tushar/Documents/GIT/DpsRace/modules/Results_Timeline.lua:204-207
- /mnt/d/Profile/Users/Tushar/Documents/GIT/DpsRace/modules/Results_Timeline.lua:448-459
- /mnt/d/Profile/Users/Tushar/Documents/GIT/DpsRace/modules/Results_Gear.lua:267-272
- /mnt/d/Profile/Users/Tushar/Documents/GIT/DpsRace/modules/Results_Gear.lua:349-363
- /mnt/d/Profile/Users/Tushar/Documents/GIT/DpsRace/core/CoreSetup.lua:92-94
- /mnt/d/Profile/Users/Tushar/Documents/GIT/DpsRace/core/DebugLogSetup.lua:60
- /mnt/d/Profile/Users/Tushar/Documents/GIT/DpsRace/tests/test_preview.lua:121-143
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LootHistory/modules/Browser.lua:963-999
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LootHistory/modules/Browser.lua:1121-1123
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LootHistory/core/DebugLogSetup.lua:110
- /mnt/d/Profile/Users/Tushar/Documents/GIT/PremadeGroupsFilterExtension/modules/Panel.lua:1007
- /mnt/d/Profile/Users/Tushar/Documents/GIT/PremadeGroupsFilterExtension/modules/Panel.lua:1030
- /mnt/d/Profile/Users/Tushar/Documents/GIT/DropWatcher/modules/DetailCard.lua:686
- /mnt/d/Profile/Users/Tushar/Documents/GIT/DropWatcher/modules/OfferPanel.lua:214

### Owner questions

- Should every window drawn by the library also get the header band: debug consoles, copy windows, the perf panel, the sim panels (images 49 and 50 show none today) and the skin picker (46)? Recommended: yes. Round 4 SR4-2 already expected a band on a debug console and a copy window, and the library fix gives it everywhere in one change.
- Should toasts (the DpsRace personal-best toast, DropWatcher toasts) get a header band? Recommended: no. A toast has no title bar, so it opts out with noTopBar.
- Should the DpsRace HUD title stay left-aligned in every skin, including skins whose title.align is CENTER, while the Results, timeline and gear titles keep following the skin? Recommended: yes. Only the HUD is cramped by its four title-bar controls.

## Item 7: icons with rough native edges and no border (DpsRace images 51 and 52, DropWatcher images 53 to 56), plus a sweep of every icon the 16 addons and LibKa0s draw

### Findings

I changed nothing. All repos were on feat/2026-11-01-full-skinning. I zoomed the images and sampled pixels with scratch PNGs under /tmp/claude-1000/-mnt-d-Profile-Users-Tushar-Documents-GIT-Ka0sAddonsCommonTasks/f08c55e9-325c-49c4-a8cd-b1f74147c24e/scratchpad/icons/.

THE ROOT CAUSE, common to both addons
R4 split icon edges into two cases. Window icons get S.IconBorder, which draws the icon.outline colour 1 physical px wide and zooms the art by 0.07 (LibKa0s/LibKa0s/SkinPaintControls.lua:897-904 for the edge, :912-924 for the zoom, :937-947 for IconBorder). HUD icons get icon.border via opts.hud. But R4-ZOOM only checked HUD icons that "draw their own edge" (Ka0sAddonsCommonTasks/docs/2026-11-03-SMOKE_ROUND4/R4_SIGNOFF.md:40-43). R4-HUD and R4-L3 only re-coloured callers of S.IconBorder. Two groups were never touched:
(a) window icons that never call any edge helper. These are DpsRace's Usage list and Used column.
(b) window icons that a host edges itself from the HUD token icon.border. This is DropWatcher.

DPSRACE, image 51 (Runs list, Used column)
- Where it is drawn: DpsRace/modules/Results_Table.lua:318-328 (Cells.items). Each icon is a bare `row:CreateTexture(nil,"ARTWORK")` at Tbl.ICON = 16 (Results_Table.lua:31). It is bound at Results_Table.lua:481-489 (Bind.items, `icon:SetTexture(list[i])`). The column is defined at Results_Runs.lua:781-783, and its icon textures come from ResultsUsage.Icons (Results_Usage.lua:265-271).
- What is wrong: it has no SetTexCoord crop (so the full 0..1 art shows), no S.IconBorder, no IconEdge and no CropIcon. Zoomed, image 51 shows Blizzard's grey bevelled corner art on every icon, and no Ka0s edge.

DPSRACE, image 52 (Usage list, flask icon)
- Where it is drawn: DpsRace/modules/Results_Usage.lua:340-341 (newRow: `row.icon = row:CreateTexture(nil,"ARTWORK")`, then SetSize). The texture is set at Results_Usage.lua:402 (fillRow). It has no crop and no edge, the same defect as the Used column.

The DpsRace tools exist but these sites never call them:
- Style.IconEdge (DpsRace/modules/Style.lua:505-510) wraps S.IconBorder with `fromSkin` and `hud`.
- Style.CropIcon (Style.lua:520-524) crops 0.08 per side.
- R4-ZOOM's test, DpsRace/tests/test_icon_crop.lua, covers only the loadout cells (:75), the gear view (:89) and the HUD best-card markup (:115). It covers neither the Used column nor the Usage list, so nothing caught this.

Other DpsRace sites with no crop and no edge:
- The spec icon in the Runs list Class column: Results_Table.lua:308-312 and :502, which uses GetSpecializationInfoByID art.
- The class icon beside it, Tbl.SetClassIcon (Results_Table.lua:114-123). It uses CLASS_ICON_TCOORDS from the class atlas at full cell size, with no trim.
- BestToast's class and spec icons: modules/BestToast.lua:194-199 and :224.
- Tooltip markup ResultsUsage.InlineIcon, `|T<icon>:14:14|t` (Results_Usage.lua:260-262). It is used by Results_Tips.lua:165 and Hud_Best.lua:114 and has no crop.
- Already correct: Hud_Best.lua:77 markup, cropped 5:59 of 64 (0.078). Results_Compare.lua:678, Results_Timeline.lua:499 and :621-622, and Hud_Chart.lua:701-702 all crop and edge. Hud_Breakdown.lua:83 edges with hud=true.

DROPWATCHER, images 53 to 56 (compact cards' big item icons)
- Where they are drawn: DropWatcher/modules/CompactGroup.lua:259 (`card.icon = WG.ItemButton(card, K.ROW_ICON)`), which calls modules/WindowGroup.lua:471-486 (b.art covers the whole button). That calls NS.IconStyle.Apply (modules/IconStyle.lua:180-192). The edge is DropWatcher's own BackdropTemplate frame (paintBorder, IconStyle.lua:153-176), not S.IconBorder.
- The crop is fine: zoom 0.1 (defaults/Profile.lua:204, applied at IconStyle.lua:190). The images show no native corner art.
- Size and rounding are fine: all four images are identical in size and square.
- The border colour is wrong. IconStyle.lua:121-124 reads `NS.Skin.Color("icon.border")`, which is the HUD token, not icon.outline. Pixels sampled at the left edge of the first icon:
  - Image 53 (Ka0s Default) is #000000. Loot History and the other windows draw #4D4D57 here.
  - Image 54 (Obsidian) is #2B2B33. Obsidian's icon.border and icon.outline are both #34343b, so this one is correct.
  - Image 55 (Azeroth) is #86652D, matching its #8a6a36, also correct.
  - Image 56 (WoW Forever) is #322C27, against a card background of #312A23. That is FV_EDGE #3a3530 (SkinDefsOthers.lua:285, :306), so the border is practically invisible. icon.outline would be #5a5048.
  So images 53 and 56 look borderless or "not 100%" because of the wrong token. 54 and 55 match only because those skins give both tokens the same value.
- The width is probably also wrong (PLAUSIBLE, not proven). The edge is 2 screenshot px in all four images. DropWatcher's edgeSize is `max(1, icon.borderSize)` = 1 UI unit (IconStyle.lua:116-117), which is not snapped to physical pixels. S.IconBorder draws P.px(h,1), exactly one physical pixel (SkinPaintExtras.lua:437-445), so the cards draw heavier than the library's window outline at the owner's UI scale.
- Tests that pin today's black icon.border: DropWatcher/tests/test_skin_flip.lua:263 ("Ka0s Default's black") and :265 (`Skin:Token(OWNER,"icon.border")`), plus :239-247 (tintedSkin sets only icon.border). Also tests/test_icon_style.lua:65 (black default) and tests/skin_switch_facts.lua:146-153. The same IconStyle path also draws the Toast (Toast.lua:346), CompactHistory.lua:68, WindowHistory.lua:370, DetailCard.lua:181 and :219, OfferPanel.lua:147 and the WindowGroup.lua:541 and :594 rows.

SWEEP: icons without a crop of at least 0.07 and a 1 px edge
I grepped SetTexCoord, IconBorder, SquareIcon, IconEdge, CropIcon, :SetTexture(, SetImage( and |T markup in all 16 addons (excluding libs, tests and docs) and in LibKa0s/LibKa0s. Atlas glyphs, marks from the Ka0s media catalog, ReadyCheck/raid-marker art and the round class circles are not icon art and are left out. The list below assumes settings pages count as windows; I asked the owner to confirm this (question 1).

Window icons, no crop and no edge:
1. DpsRace Results_Table.lua:322 (Used column, image 51).
2. DpsRace Results_Usage.lua:340 (Usage list, image 52).
3. DpsRace Results_Table.lua:309 and :502 (spec icon), and :114-123 (class atlas icon, untrimmed).
4. DpsRace BestToast.lua:197 and :224 (toast spec icon; the toast is HUD-like).
5. LibKa0s OptionsIdList.lua:929-931 (`lbl:SetImage(icon)`, 16 px, on an AceGUI label). Every host's spell/item id list uses it: AuraMaster settings/GeneralSpells.lua and Filters.lua, DpsRace settings/Race.lua and History.lua, BankLedger, LootHistory and others.
6. LibKa0s OptionsIdSuggest.lua:372-374 and :464 (suggestion rows).
7. LibKa0s WidgetsAutocomplete.lua:192-194 and :248.
8. ConsumableMaster modules/KCMItemRow.lua:334-336 and :204-206 (item and spell icon in the options item rows).
9. ConsumableMaster KCMIconButton.lua:74-86 and KCMScoreButton.lua:57-69. These reset coords to 0,1 unless a caller passes them, and are fed by settings/Category.lua:379 and :400.
10. KickCD settings/Spells_Rows.lua:122-124 (spell icon in an AceGUI Icon, no coords).
11. QuickComms settings/IconBrowser.lua:191 (grid cells) and :199 (preview).
12. QuickComms settings/Editors.lua:411, :564-565 and :686-687 (SetImage of a game icon).

Edged, but in the HUD token or with a host-drawn edge:
13. DropWatcher IconStyle.lua:121-124. All window item buttons use icon.border (images 53 and 56).
14. MultiMeters Row_NameCell.lua:136-141. The crop is 0.07 (:267), but the edge has hud=true. This was ruled HUD in R4 (R4_ADDENDUM_HUD_ICON_EDGE.md:20), and that now conflicts with the owner's item 2 ask that MultiMeters look like LootHistory.

Inline |T markup, no crop; it cannot take a border:
15. DpsRace Results_Usage.lua:261.
16. MultiMeters Tooltip_Builders.lua:234, :551 and :675, and Tooltip_Lines.lua:710.
17. KickCD settings/Spells_Header.lua:72 (ClassIcon_* art) and :107 (spec icon).
18. ConsumableMaster settings/StatPriority.lua:178 (spec icon).

HUD sites already compliant (crop of at least 0.07 and an icon.border edge):
- AuraMaster Style.lua:266 and Style_Icons.lua:92, with its own border.
- KickCD IconGrid_Render.lua:806 and Castbar_Frame.lua:293 (0.08), with LSM border frames.
- ConsumableMaster MacroBarButton.lua:556, with BB border.
- QuickComms IconStyle.lua:143-148 (NATIVE_CROP 0.07 at :56) and its edge in icon.border at :121-125.
- PartyFrameEnhanced Element.lua:79-80 (0.07 plus IconBorder with hud=true).
- WhatGroup FrameLayout.lua:138 and FrameSkin.lua:86 (IconBorder on the Texture, 0.07 plus outline, in a window).
- MultiMeters Row_NameCell.lua:408, :418 and :430-431 (trimmed).
- Skin Tester ShowroomControls.lua:201-205 and ShowroomOverlays.lua:155-157.
- Nothing to sweep in AbsorbTracker, PanelMaster, PrettyChat (chat markup only), PGFE (Panel.lua:916 is a catalog chevron), LootHistory (no item art in its window), or BankLedger (class circles and marks only).

### Fix

THE RULE, to record in the standard's skinning section and in LibKa0s docs/api:
- Every Blizzard icon art (an item, spell, spec, class or currency fileID or path) is cropped by at least 0.07 per side.
- In a window it is edged 1 physical px in icon.outline: S.IconBorder(tex) with no hud flag.
- On the HUD it is edged in icon.border: S.IconBorder(..., {hud=true}), or the host's own BB edge from icon.border.
- Inline |T markup cannot be bordered. It is cropped through its texcoord arguments (`:s:s:0:0:64:64:5:59:5:59`, which is 0.078).
- Atlas glyphs, Ka0s catalog marks and round art are exempt.

SMALLEST FIXES (host first; the library only for its own widgets):

1. DpsRace (host)
   - Results_Usage.lua:340: after the CreateTexture, add `Style.CropIcon(row.icon); NS.Skin.IconBorder(row.icon, { fromSkin = true })`. The Texture form keeps its holder on the texture's bounds and follows its shown state.
   - Results_Table.lua:323-325 (Cells.items): the same two calls for each slot icon. Bind.items's SetShown is followed automatically (SkinPaintControls.lua:860-868).
   - Results_Table.lua:309-311: CropIcon plus IconBorder on cell.spec. For cell.class, trim the CLASS_ICON_TCOORDS sub-rect by 0.07 of its width, as MultiMeters does at Row_NameCell.lua:430-431, and add the same edge.
   - BestToast.lua:197: crop, plus IconBorder with hud=true. This depends on the owner's answer to question 3.
   - Results_Usage.lua:261: change the markup to `:14:14:0:0:64:64:5:59:5:59|t`. Update test_results_usage.lua:152, which pins `:14:14|t`.
   - Extend tests/test_icon_crop.lua with the Used column, the Usage list and the spec icon (red today), plus a check that each one has an IconBorder record in icon.outline. That check follows the edgeColor helper in tests/test_hud_icon_edge.lua.

2. DropWatcher (host, modules/IconStyle.lua)
   - In read() (:121-124), have window buttons read icon.outline first, then icon.border. A button marked HUD (the Toast, if the owner rules it HUD) keeps icon.border. The smallest way is a flag on the button: WG.ItemButton(parent, size, { hud = true }) at Toast.lua:346, cached in its own cfg.
   - Snap edgeSize to physical pixels: multiply by PixelUtil.GetPixelToUIUnitFactor()/b:GetEffectiveScale(), as P.px does. Re-run it on UI scale changes, which Refresh already covers through OnLooksChanged/scale.
   - Keep the 0.1 zoom.
   - Update test_skin_flip.lua:239-265 (the token is now icon.outline, and Ka0s Default is #4D4D57 rather than black), test_icon_style.lua:65 and skin_switch_facts.lua:146. Add a toast case that stays icon.border.

3. LibKa0s (library, a minor bump plus re-vendor to all 16 addons; never Outfitter)
   - OptionsIdList.lua:929-931: after SetImage, `lbl.image:SetTexCoord(0.07,0.93,0.07,0.93)` plus S.IconBorder(lbl.image, { fromSkin = true }). It must be undone on release, because AceGUI labels are pooled: SetImage(nil) or a coords reset in entryRelease.
   - OptionsIdSuggest.lua:372 and WidgetsAutocomplete.lua:192: the same crop and edge on the row texture.

4. Settings pages in other hosts, if the owner rules them windows (question 1): ConsumableMaster KCMItemRow.lua:334 and KCMIconButton/KCMScoreButton, KickCD Spells_Rows.lua:122, and QuickComms IconBrowser.lua:191 and :199 and Editors.lua:411, :564 and :686. Each needs CropIcon at 0.07-0.08 plus S.IconBorder(tex, {fromSkin=true}). AceGUI Icon and Label widgets are pooled, so the crop must be restored on release.

5. Tooltip markup (question 2): crop to 5:59 at MultiMeters Tooltip_Builders.lua:234, :551 and :675 and Tooltip_Lines.lua:710, KickCD Spells_Header.lua:72 and :107, and ConsumableMaster StatPriority.lua:178.

6. MultiMeters Row_NameCell.lua:141: drop hud=true only if the owner says meter rows are window icons (question 4).

### Sites

- /mnt/d/Profile/Users/Tushar/Documents/GIT/DpsRace/modules/Results_Table.lua:318-328 (Used column icons, no crop, no edge; image 51)
- /mnt/d/Profile/Users/Tushar/Documents/GIT/DpsRace/modules/Results_Table.lua:481-489 (Bind.items SetTexture)
- /mnt/d/Profile/Users/Tushar/Documents/GIT/DpsRace/modules/Results_Usage.lua:340-341 and :402 (Usage list icon, no crop, no edge; image 52)
- /mnt/d/Profile/Users/Tushar/Documents/GIT/DpsRace/modules/Results_Usage.lua:260-262 (InlineIcon markup without a crop; pinned by tests/test_results_usage.lua:152)
- /mnt/d/Profile/Users/Tushar/Documents/GIT/DpsRace/modules/Results_Table.lua:114-123, :308-312, :502 (class and spec icons, untrimmed)
- /mnt/d/Profile/Users/Tushar/Documents/GIT/DpsRace/modules/BestToast.lua:194-199, :224 (toast class and spec icons)
- /mnt/d/Profile/Users/Tushar/Documents/GIT/DpsRace/modules/Style.lua:505-524 (IconEdge, CropIcon: the existing tools)
- /mnt/d/Profile/Users/Tushar/Documents/GIT/DpsRace/tests/test_icon_crop.lua (R4-ZOOM coverage; misses both sites)
- /mnt/d/Profile/Users/Tushar/Documents/GIT/DropWatcher/modules/IconStyle.lua:116-124 (edgeSize in UI units; colour from icon.border, not icon.outline; images 53 and 56)
- /mnt/d/Profile/Users/Tushar/Documents/GIT/DropWatcher/modules/IconStyle.lua:153-192 (paintBorder and Apply; 0.1 zoom is fine)
- /mnt/d/Profile/Users/Tushar/Documents/GIT/DropWatcher/modules/CompactGroup.lua:259 and modules/WindowGroup.lua:471-486 (compact card item button)
- /mnt/d/Profile/Users/Tushar/Documents/GIT/DropWatcher/modules/Toast.lua:346 (same item button on the toast)
- /mnt/d/Profile/Users/Tushar/Documents/GIT/DropWatcher/tests/test_skin_flip.lua:239-265, tests/test_icon_style.lua:65, tests/skin_switch_facts.lua:146-153 (pin the black icon.border)
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/SkinPaintControls.lua:897-947 (drawIconEdge, zoomIcon 0.07, IconBorder)
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/SkinPaintExtras.lua:437-445 (P.px)
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/SkinDefsOthers.lua:285, :293-310 (per-skin icon.border vs icon.outline)
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/OptionsIdList.lua:929-931 (id-list icon, no crop, no edge)
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/OptionsIdSuggest.lua:372-374, :464
- /mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/WidgetsAutocomplete.lua:192-194, :248
- /mnt/d/Profile/Users/Tushar/Documents/GIT/ConsumableMaster/modules/KCMItemRow.lua:334-336, :204-206
- /mnt/d/Profile/Users/Tushar/Documents/GIT/ConsumableMaster/modules/KCMIconButton.lua:74-86, KCMScoreButton.lua:57-69; settings/Category.lua:379, :400
- /mnt/d/Profile/Users/Tushar/Documents/GIT/ConsumableMaster/settings/StatPriority.lua:178 (markup)
- /mnt/d/Profile/Users/Tushar/Documents/GIT/KickCD/settings/Spells_Rows.lua:122-124
- /mnt/d/Profile/Users/Tushar/Documents/GIT/KickCD/settings/Spells_Header.lua:72, :107 (markup)
- /mnt/d/Profile/Users/Tushar/Documents/GIT/QuickComms/settings/IconBrowser.lua:191, :199
- /mnt/d/Profile/Users/Tushar/Documents/GIT/QuickComms/settings/Editors.lua:411, :564-565, :686-687
- /mnt/d/Profile/Users/Tushar/Documents/GIT/MultiMeters/modules/Tooltip_Builders.lua:234, :551, :675; Tooltip_Lines.lua:710 (markup)
- /mnt/d/Profile/Users/Tushar/Documents/GIT/MultiMeters/modules/Row_NameCell.lua:136-141 (hud=true on meter rows; crop 0.07 at :267)

### Owner questions

- Do settings pages count as windows for the icon rule? This covers the spell/item id lists in every addon, the id suggestion and autocomplete rows, ConsumableMaster's item rows, KickCD's spell rows and QuickComms' icon browser and editors. Recommended: yes, crop them by at least 0.07 and give them the 1 px grey outline (icon.outline), the same as Loot History.
- Tooltip and chat icons are inline text markup and cannot take a border. Is cropping them enough? Recommended: yes, crop them (about 0.078, the 5:59 of 64 the DpsRace HUD best card already uses) so the rough native corners disappear, with no border.
- Are the DropWatcher toast and the DpsRace 'New best' toast window icons or HUD icons? Recommended: HUD. They float over the game world, so they keep the black icon.border edge, while the Drop Watcher window's cards and rows move to the grey outline (#4D4D57 under Ka0s Default) like Loot History.
- In round 4 the MultiMeters meter rows' unit icons were ruled HUD (black edge). Item 2 asks for MultiMeters to look like Loot History. Should those icons switch to the window outline? Recommended: keep them black (HUD), since the meter is read in combat over the game world. Change them only if you want the meter to match the windows exactly.

## inner-border (item 2): MultiMeters' black strip between the window edge and the header, plus a sweep of every Ka0s window against the LootHistory structure

### Findings

I read the code and sampled pixels from the screenshots. I changed no files. Repos: LibKa0s/LibKa0s plus 16 addons, all on feat/2026-11-01-full-skinning.

## 1. How LootHistory builds its window (the target look, image 31)
- Shell: LootHistory/modules/Browser.lua:1123 calls `B:ApplySkin(frame, nil, { noTopBar = true, bottomBar = FOOTER_H })`, which goes through Browser.lua:66-71 to `NS.Skin.Shell`. Inside the library (LibKa0s/LibKa0s/SkinPaint.lua:1012-1034) Shell paints:
  - the fill;
  - the edge on the edge holder, above every child (SkinPaint.lua:913-928): a 1px `win.border` in black plus a 1px `win.inner` rule just inside it, grey `EDGE` (SkinDefs.lua:325-326);
  - the bands, inset by `win.borderSize` = 1 (SkinPaint.lua:1027-1028, 932-976).
- Header band: Browser.lua:963-966 anchors the title bar at TOPLEFT (1,-1) / TOPRIGHT (-1,-1) with height `SKIN.titleBarH` = 30 (Browser.lua:14). Browser.lua:999 calls `NS.Skin.TitleBar(titleBar)`, and the TITLE box (SkinPaintExtras.lua:67, 117-128) fills it with P.fill (SkinPaint.lua:398-417). That fill is the vertical gradient from `title.bgTop` #3A2F0A to `title.bgBottom` #1F1905 (SkinDefs.lua:486-488).
- The band sits flush against the 1px edge on the top, left and right, with no gutter. Pixels from image 31 at x=300: y6 black, y7 grey rule, y8-42 gradient from (49,36,0) to (20,11,0), then the body. Across a row at y=25: x6 black, x7 grey, x8 band, and on the right x1667 band, x1668 grey, x1669 black.
- There is no separator (R4-SEP, the 1px empty `dividerBar` at Browser.lua:1005-1009). The title is centred (Browser.lua:983).
- Content is inset 6px: panes at Browser.lua:150-151, the filter bar at BAR_INSET 6 (Browser.lua:32, 1027-1028), the footer band from Shell's bottomBar. In the image the column-header row starts at x13, 6px inside the edge.

## 2. How the MultiMeters meter window differs (image 33)
- Shell: MultiMeters/modules/Window_Frame.lua:83-92 calls `paintShell`, which runs NS.ApplySkin and then `NS.Skin.Shell(frame, { noTopBar = true })`. The edge and inner rule are the same as LootHistory's.
- The header band is the texture `self.headerBG` (Window_Frame.lua:307, BORDER layer). It is placed by `WindowProto:ApplyHeaderStrip` (MultiMeters/modules/Window_Header.lua:452-455):
```lua
self.headerBG:SetPoint("TOPLEFT", frame, "TOPLEFT", pad, -pad)
self.headerBG:SetPoint("TOPRIGHT", frame, "TOPRIGHT", -pad, -pad)
self.headerBG:SetHeight(layout.titleHeight)
self.headerBG:SetColorTexture(ar, ag, ab, aa)
```
  - `pad` is `frame.padding` = 6 (defaults/Profile.lua:135, Window.lua:322/332), the player's "inset from the frame edge to the rows". `titleHeight` is 26 (Profile.lua:254-257).
  - So the band is inset 6px from the top, left and right. The 4-5px between the 1px edge plus inner rule and the band shows `win.bg`. That is the "black strip". Pixels from image 33: x15 black, x16 grey, x17-21 dark (16,11,12), band from x22. On the right: band to x839, dark x840-844, grey x845, black x846. On the top: y11 black, y12-13 grey, y14-17 dark, band from y18.
- Root cause 1 (geometry): the title band reuses the row padding as its own inset. It should sit at the edge inset (`win.inset` = 1, SkinDefs.lua:326, the same in every skin) as LootHistory's does.
- Root cause 2 (fill): the band is a flat `title.bg`. `titleBarColor` (Window_Header.lua:225-229) reads `looks.titleBg`, which caches only `title.bg` (MultiMeters/core/SkinSetup.lua:235). In image 33 the band is a flat (34,25,0), while LootHistory shows the bgTop to bgBottom gradient. MultiMeters therefore also will not pick up the item-1 "darker header" change through the gradient pair.
- The geometry contract still works after the fix. `TitleBandHeight()` = padding 6 + titleHeight 26 - BAR_INSET 2 = 30 (Window_Header.lua:69, 330-333), and that already defines the title bar the player sees from the frame top. The title, session line and controls are centred in it (`TitleRowMid`, 315-320) and the drag strip covers it (464-466). A band at (1,-1) with height TitleBandHeight() is exactly LootHistory's 30px band.
- The column-header strip and body stay at `pad`: `headerFrame` at Window_Header.lua:710-711 / 835-836, body at 838-839 and Window_Frame.lua:488-492, with headerTop = pad + titleHeight (Window.lua:366-371) = 32. That is the same 6px content inset LootHistory uses, so the inset column strip in image 33 is consistent with LootHistory and needs no change. After the fix the band ends at y31 and the column strip starts at y32.
- Minimized windows: the frame height is `padding*2 + titleHeight` = 38 (Window_Header.lua:882). With a flush 30px band, 7px of win.bg is left under it. Making it `TitleBandHeight() + win.inset` (31) would make a collapsed window exactly the band.
- Edge size: under `borderColorMode` class or custom, ApplyBorder draws the player's own edge (default "Blizzard Tooltip", size 2, Profile.lua:131-133). The band inset then needs to be that edge's drawn size rather than 1, or the art overlaps the band. That still looks fine, because the edge is a child frame above the BORDER texture.

## 3. Sweep: every top-level window against LootHistory's structure (band flush at the 1px edge inset, 30px, gradient, no separator, content about 6px in)
- These windows wear Shell's own top band. Calling `Core.ApplySkin(f, nil, owner)` (Core.lua:231-241) runs `S.Shell(frame)` with no opts, and Shell paints the "top" band at inset 1, height `title.height` 30, with P.fill's gradient (SkinPaint.lua:967-971).
- **Library windows: all match**
  - Debug console: dragBar at (1,-1) h30 (DebugLogWindow.lua:324-335, 76), skinned through ctx.applySkin (DebugLog.lua:305-321).
  - Copy window: bar at (1,-1) (WidgetsCopyWindow.lua:194-195, TITLE_H 30 at 178), ApplySkin with owner (159-166).
  - Sim panel: SimPanelRender.lua:311 / 336, title centred at -(1+15) (168).
  - Perf panel: PerfPanel.lua:297, title at 258.
  - Skin picker: OptionsSkinPicker.lua:1055. The band matches, but the title is TOP-anchored at -8 (1039-1040), not centred in the band (item-5 topic).
  - Toast: Toast.lua:220. It also gets a 30px top band.
- **LootHistory**
  - Browser: the reference.
  - Export: Export.lua:469 tbar at (1,-1) h30, plus TitleBar at 486 and Shell noTopBar at 524. Matches.
- **BankLedger: all match**
  - Browser: Browser.lua:954-956, TitleBar at 980, Shell noTopBar at 1093.
  - Export: Export.lua:390 / 401 / 454.
  - SessionWindow: SessionWindow.lua:545-547 / 564 / 632.
- **DropWatcher**
  - Main window: WindowTitleBar.lua:357-358 bar at (1,-1), TitleBar at 372, Window.lua:558-560 ApplySkin then Shell noTopBar. Matches.
  - DetailCard editor: DetailCard.lua:686 ApplySkin gives Shell's top band, so the band matches. The title is top-anchored at -9 (688), the item-5 topic.
  - OfferPanel: OfferPanel.lua:214. The band matches.
- **WhatGroup**: FrameLayout.lua:37-39 bar at (0,0) h30. The edge holder draws over it, so it looks identical. FrameSkin.lua:81-83 Shell noTopBar plus TitleBar. Matches.
- **PremadeGroupsFilterExtension**: Panel.lua:1007 `S.Shell(f, { stock = ... })` on PortraitFrameTemplateMinimizable, giving Shell's top band at inset 1. Matches; the owner confirmed it looks great.
- **LibKa0sSkinTester**: showroom bar at (0,0) h TITLE_H (Showroom.lua:238-241), `Paint("Shell", f, {noTopBar=true})` plus `Paint("TitleBar", bar)` (291-292). Matches.
- **MultiMeters**
  - Meter window: DIFFERS, see section 2.
  - Export modal: Export_Modal.lua:196-197 bar at (1,-1), with Shell noTopBar plus TitleBar place at 793-794. Matches.
- **QuickComms**
  - Pad, the "dial" in images 40 and 41: DIFFERS.
    - The root gets Core's backdrop from NS.SKIN only (Pad.lua:289, "a pad has no title band"). Pad_Render.lua:599-603 does the same.
    - The header is a plain child at (0,0) (Pad.lua:341-347), height `PL.HEADER_H` 24 (defaults/PadStyle.lua:40).
    - It is dressed by `bandSkin` with `R.BAND_TOKENS` `qc.bandBg` / `qc.bandEdge` (Pad_Render.lua:471, 581-587, 619-623). That token is shared with the section bands and is clear under Ka0s Default, so there is no `title.bg` gradient band at all. This is item 4.
  - Preview window: PreviewWindow.lua:231 `NS.Skin.Shell(f)`, Shell's top band. Matches.
  - Settings modal: settings/ModalWindow.lua:99-103 Shell(stock) plus nineSlice TitleBar noBg. Matches. Its no-template fallback (128-131) is Shell noTopBar, where "the page draws its own header". It differs, but only on a client without the template.
- **DpsRace**
  - HUD: Hud.lua:474. The code path should draw Shell's top band: `NS.ApplySkin(f)` (core/CoreSetup.lua:92-93) runs Core.ApplySkin and then S.Shell(f) with no noTopBar, and the owner is registered (core/SkinSetup.lua:630). The title is CENTER at -HEADER_H/2 (Hud.lua:409), with HEADER_H = Style.TITLE_BAR_H, PAD 12, CONTENT_TOP = HEADER_H+10 (Hud.lua:41-42).
    - Images 34-37 and 45 show no band: y=10..38 is near-opaque (1,0,3) straight under the 1px edge. Something hides or covers Shell's "top" region. I did not find it in Hud*.lua, Style.lua or Hud_Appearance.lua, so this is for the item-3 investigator.
    - Content is inset 12px, not about 6.
  - Results: Results.lua:299, the same path and the same symptom.
  - Timeline: Results_Timeline.lua:459 Shell with SHELL token remaps (177), so it should get the top band.
  - Gear: Results_Gear.lua:363, likewise.
- **AbsorbTracker, AuraMaster, ConsumableMaster, KickCD, PanelMaster, PartyFrameEnhanced, PrettyChat**: no top-level window of their own (HUD bars, icons and anchors only). Their consoles, copy, sim and perf windows are the library's, which match.

## 4. Tests that pin current behaviour
- MultiMeters/tests/test_skin_window.lua:91 asserts `headerBG.__colorTexture == title.bg` (flat). It goes red under a gradient fix.
  - Lines 197, 209, 252 and 280 assert the custom swatch, and the clear colour for a skin with no band.
- MultiMeters/tests/skin_facts.lua:82-84: the "title bar's band" surface is headerBG.
- MultiMeters/tests/test_headercontrols.lua:166 asserts TitleBandHeight 30; lines 205 and 224 use it for centring. These stay green.
- MultiMeters/tests/test_window_header.lua:160 (TitleRowMid against BAR_INSET) and 1238-1263: headerFrame, body and testStrip at padding+titleHeight. These stay green, because the band move does not touch them.
- No MultiMeters test pins headerBG's anchor at `pad`, so add one for (win.inset, -win.inset) and height TitleBandHeight.
- LootHistory/tests/test_skin_chrome.lua:191 and 270-271 (TitleBar recorded, height = title.height) is the reference contract.
- LibKa0s/tests/test_skin_paint.lua:21-28 pins the bgTop/bgBottom gradient.

Note for the lead: the question of whether DpsRace's band is hidden by something else is item 3's. The vertical centring on the skin picker and DropWatcher editor titles is item 5's.

### Fix

The fix belongs in the hosts. The library already draws LootHistory's band correctly through Shell's top band or S.TitleBar. MultiMeters is the only window that draws the band itself at the wrong inset.

1. MultiMeters/modules/Window_Header.lua:452-455 (ApplyHeaderStrip):
   - Anchor headerBG at the edge inset, not at `pad`:
```lua
local e = (NS.Skin and NS.Skin.Token and NS.Skin.Token("win.inset")) or 1
self.headerBG:SetPoint("TOPLEFT", frame, "TOPLEFT", e, -e)
self.headerBG:SetPoint("TOPRIGHT", frame, "TOPRIGHT", -e, -e)
self.headerBG:SetHeight(self:TitleBandHeight())  -- 30, LootHistory's bar
```
   - Under borderColorMode class or custom, use the player's drawn edge size (frameCfg.borderSize) for `e`.
   - Leave `padding`, the rows, the column strip and the body alone. They already match LootHistory's 6px content inset.
2. Gradient while `header.bgColorFromSkin`:
   - Add `titleBgTop = "title.bgTop"` and `titleBgBottom = "title.bgBottom"` to WINDOW_LOOKS, CHROME_LOOKS and CLEAR_WHEN_UNSET in MultiMeters/core/SkinSetup.lua:235/257/263.
   - In ApplyHeaderStrip, when both are present, call `SetColorTexture(1,1,1,1)` and then `SetGradient("VERTICAL", CreateColor(bottom), CreateColor(top))`, mirroring P.fill (SkinPaint.lua:398-417). Otherwise use the flat colour, and reset the gradient to white the way P.fill does.
   - Do not make headerBG a recorded S.TitleBar frame. Its replay on a skin switch would paint over a player's custom swatch.
3. Minimized height, Window_Header.lua:882: use `self:TitleBandHeight() + e` instead of `padding*2 + titleHeight`, so a collapsed meter is exactly the band.
4. Tests:
   - Update test_skin_window.lua:91 to expect the gradient pair: `__gradient`, or whatever the harness stub records for SetGradient.
   - Add a pin that headerBG's first point is (win.inset, -win.inset) and its height is TitleBandHeight().
   - Keep 197/209/252/280, the flat custom swatch.
5. The other windows the sweep flagged belong to other items:
   - QuickComms pad (Pad.lua:289/341-347, Pad_Render.lua:581-623): item 4. Give the header its own `title.bg` gradient band at the edge inset, separate from the section bands' `qc.bandBg`.
   - DpsRace HUD and Results (Hud.lua:474, Results.lua:299): item 3. Shell's band is expected but not visible.
   - Every other window already matches LootHistory, so no change is needed there for item 2.

### Sites

- MultiMeters/modules/Window_Header.lua:452-455 (headerBG anchored at pad, flat colour): root cause
- MultiMeters/modules/Window_Header.lua:225-229 (titleBarColor reads only title.bg)
- MultiMeters/core/SkinSetup.lua:235,257,263 (WINDOW_LOOKS titleBg = title.bg only)
- MultiMeters/modules/Window_Header.lua:69,330-333 (BAR_INSET, TitleBandHeight = 30)
- MultiMeters/modules/Window_Header.lua:882 (minimized height padding*2+titleHeight)
- MultiMeters/modules/Window_Frame.lua:83-92,307 (paintShell noTopBar, headerBG texture)
- MultiMeters/defaults/Profile.lua:135,254-257 (padding 6, header.height 26)
- LootHistory/modules/Browser.lua:14,963-966,999,1123 (reference: bar at 1,-1 h30, TitleBar, Shell noTopBar)
- LibKa0s/LibKa0s/SkinPaint.lua:398-417,913-976,1012-1034 (P.fill gradient, edges, bands, Shell)
- LibKa0s/LibKa0s/SkinPaintExtras.lua:67,117-128 (S.TitleBar)
- LibKa0s/LibKa0s/SkinDefs.lua:325-326,486-488 (win.border, win.inner, win.inset 1, title gradient)
- LibKa0s/LibKa0s/Core.lua:231-241 (ApplySkin with owner -> S.Shell top band)
- QuickComms/modules/Pad.lua:289,341-347 and Pad_Render.lua:471,581-623 (pad: no title band, qc.bandBg)
- DpsRace/modules/Hud.lua:41-42,409,474 and Results.lua:299 (band expected, not visible in images 34-37)
- MultiMeters/tests/test_skin_window.lua:91 (pins flat title.bg)

### Owner questions

- MultiMeters lets a player turn off 'Use the skin's background' for the title bar and pick a custom colour. Should a custom colour also use the new flush, edge-to-edge band geometry, drawn flat? Recommended: yes. Every mode uses one geometry, and only the colour changes.
- The MultiMeters column-label strip and rows stay 6px in from the edge, which is the 'Padding' setting and the same inset LootHistory uses for its table. Is that what you want, or should the column-label strip also run edge to edge? Recommended: keep it 6px in, like LootHistory's column header.
- A minimized MultiMeters window today is 38px tall, which would leave a 7px dark strip under the new 30px band. Should a collapsed meter be exactly the header band (31px)? Recommended: yes.

# Skeptics

## Skeptic

**Verdict:** The diagnosis is confirmed. I re-read every cited site and found no material line errors. DpsRace's /dr sim bypasses the library's RunVerb grammar. NS.StartSim (core/DpsRace.lua:186-195) goes through startQueued (:161-166), then Preview.Start (modules/Preview.lua:147-175), then Sim.Begin (modules/Sim.lua:262-270), which calls session:Start({fromHost=true}) and ShowPanel. The panel therefore opens with a live session, and the library models that as running (LibKa0s/LibKa0s/SimPanel.lua:260-275, 292-299, 504-540). That gives image 49: a green Start row, Armed next, and Resume/Restart/Stop in the footer, where the button sends `run`. Nothing has actually auto-advanced, because the arm is parked (Sim.lua:139, SampleRace.lua:249-266). MultiMeters (settings/Slash.lua:138-139) sends the line to RunVerb, and an empty verb opens the idle picker panel (SimTimeline.lua:587-596; SimPanel.lua:440-468), which is image 50. The zoom is also confirmed. paceTheRace sets the pace to left/RACE_STEP_SECONDS=10 (Sim.lua:40-42, 155-163) on the 30 s MockRuns.LENGTH (MockRuns.lua:26, 590), so the race runs 3x fast. Countdown.schedule divides each mark's delay by Rate (Countdown.lua:292-311), so the last-10 s numbers take about 3.3 s. After the buzzer, the Result card step's SkipToResult (SampleRace.lua:290-301) compresses Stop!, the tail and the read. The proposed host-only fix, RunVerb plus an idle panel, a session-driven Preview and a real-time race, would produce image 50's layout. Three parts need correcting: the gate design as written is self-contradictory, the Rate removal misses a consumer, and the list of affected tests and docs is incomplete. The verified LibKa0s SimPanel.lua and SimTimeline.lua are byte-identical to DpsRace/libs/LibKa0s.

**Corrections:**

- Gate design contradiction (fix 2c vs 2d): the library calls the gate as gate(session) only (LibKa0s/LibKa0s/SimTimeline.lua:199-205). It is not told which step comes next. If the gate also holds 'while the race is STOPPING', it is closed before every step, the Buzzer step included. The Buzzer step would then wait for RESULT and land together with the Result card, not at about 31.25 s as 2d says. The fix needs a host flag set by playStep: after the Buzzer step has played (for example `afterBuzzer = true` in STEP_MOMENTS.buzzer, Sim.lua:170), hold while STOPPING with 'Waiting for the result.'. After the Result card step, hold until resultAt + RESULT_HOLD. Racing's hold stays on `racing` plus RUNNING (Sim.lua:193-198).
- Removing SampleRace.Pace/Rate (fix 2a) misses one consumer. modules/Hud.lua:642 (scheduleSlice, with its R4-DR6 comment at :632-633) also divides by race.Rate(). It must be updated with Countdown.lua:299, or Rate kept as a constant 1. The full set of Rate/Pace sites is Countdown.lua:299, Hud.lua:642, SampleRace.lua:306-313 and Sim.lua:161.
- The LauncherSetup citation is :105-108 (isSimMode :105, toggleSim :106-108), not :105-107. Today toggleSim calls NS.ToggleTestMode() when the sim is on and NS.StartSim() otherwise. With the fix, isSimMode should probably follow session:IsActive() (MultiMeters core/LauncherSetup.lua:351) or Preview.Mode()=='sim' after Start. An idle panel has no session, so the launcher tick stays off until Start. That matches test_launcher:61-69 needing a rewrite.
- Fix 2d's arithmetic is right with the real-time clock. Armed calls Unpark(stepDelay=1) and Race starts plays at 1 s wall. Racing plays at 2 s wall, when race time is about 1 s, so the buzzer comes at 31 s wall. 'Racing from about 2 s' is accurate. Racing's Skip(0) is then a no-op, and only `racing = true` matters.
- Owner question 3 is confirmed: the panel's picker choice is the private P.choice (SimPanel.lua:229, 451, 669), and no member sets it. 'Open idle with died picked' would need a LibKa0s change. The recommended answer, start at once, needs none.

**Missed:**

- The investigator's test list covers only test_sim, test_slash, test_launcher and test_countdown. Other suites also start the sim through Preview.Start({mode='sim'}), and so depend on Preview.Start's sim branch starting the session: tests/test_chart.lua:567 and :587, test_chart_icons.lua:581, test_pace.lua:294, test_sample_parity.lua:27, and test_sim.lua:187 and :199 (the refusal tests). Fix 1c moves the start into the descriptor's prepare and keeps Sim.Begin 'only for headless'. Either Preview.Start({mode='sim'}) keeps working as a programmatic start (for example by routing to session:Start({scenario}) plus arm), or all of these must move to RunVerb('start x'). The plan must choose one before writing the tests red.
- In docs, the R4-DR6 and auto-start text must be rewritten in docs/module-map.md:90 and :92 (Pace/Rate, RACE_STEP_SECONDS), docs/testing.md:143 ('about 10 s and not before 9.5'), docs/test-cases.md:1427-1430, docs/data-flow.md:553 (/dr sim queues Preview), docs/settings-panel.md:61 (Test mode 'ticked while /dr sim plays') and :81, docs/schema.md:57, docs/scope.md:52 and :101 (usage 'sim [scenario]'). Also docs/smoke-tests.md P5 (:192), R8e (:128), P11 (:198), SM-DR-CH8 (:318), SM-DR-CH9 (:319) and SM-DR-BL8 (:363), which all assume a bare `/dr sim` plays the race. They now need a Start press, or `/dr sim start newbest`.
- The usage text changes. Sim.Usage (Sim.lua:291-294, 'Usage: %s sim [%s]') and locales/enUS.lua:588 are printed by NS.StartSim (core/DpsRace.lua:190-191). With RunVerb, the library prints its own usage, so the scenario-key lines (L['  %s: %s']) and the slash help line (test_slash:349-357) need a decision. The investigator mentions keeping them as the descriptor's `usage` list, but the Usage function and its locale key also need retiring or keeping.
- A test-mode-to-sim switch is not covered. Today, /dr sim while /dr test is on switches in place (startQueued, core/DpsRace.lua:164). With RunVerb(''), a bare /dr sim leaves test mode running behind an idle panel. Preview.EnterSim (prepare) must then perform the switch on Start, ending the test body without calling stopSim on the session being prepared. That is the same trap as finding A6, reached by this path, and it needs a test.
- Racing label: the new 'Racing (%d s)' needs a new locale key next to enUS.lua:592, and the old key 'Racing (%d s of damage in %d s)' must be removed. For image-50 parity, MultiMeters' rows read 'Pull Trash (10 s)', so 'Racing (30 s)' matches that style.
- Sticky scenario: with real-time STOPPING, sticky's Result card waits for hintDelay (Profile.lua:106, 15 s) + STICKY_EXTRA (Sim.lua:37, 3 s) + QUIET_BEFORE_READ (Scoring.lua:19, 2.5 s), about 20.5 s with no step moving. The gate line should say something visible, such as 'Waiting for the result (combat holds on).', so the owner does not read it as a hang. This belongs with owner question 2.
- Armed timing: ARM_HOLD = 3 (Sim.lua:31-32) still governs the no-stepper path only. With the idle panel, Start arms the run, so Armed plays on the next frame and the race starts one stepDelay later. Confirm that no test still assumes the headless ARM_HOLD when a session exists (test_sim.lua:29, 401).

## Skeptic

**Verdict:** The finding stands. I re-read the code and confirmed it. The first /st dropdown in images 46 and 47 is the library's own hand-built skin list. Its button is LibKa0s/LibKa0s/OptionsSkinPicker.lua:979-997 (a BackdropTemplate Button painted with P.Sk.Dropdown, OnClick at :994 = setOpen(not P.open)). The list is buildList :966-977 (a FULLSCREEN_DIALOG Frame painted with P.Sk.MenuFrame). setOpen is at :605-611 and layout's Show/Hide at :555. Nothing registers GLOBAL_MOUSE_DOWN for it. R4-L1 (OptionsCombat.lua:158-325) is armed only by the AceGUI.SetFocus post-hook (:306-320), and __OnPulloutFocus (:275-285) returns early because openPullout (:200-205) needs an AceGUI widget with .open and .pullout.frame. The window's OnMouseDown (:1107) calls only dropFocus (:518-528), which clears an AceGUI focus held by a media row and never touches p.open. So an outside press does nothing, and a press on the button toggles the list closed. That matches images 46 and 47 exactly. Image 48's controls do close, because each goes through W.Dropdown (Widgets openMenu :536-546, registers GLOBAL_MOUSE_DOWN at :544), Blizzard's Menu, or an AceGUI type on a Shell-painted surface that R4-L1 covers. I spot-checked the cited close paths: pick :718, closed :812, fresh show :1177, onRow OptionsSkinPickerRows.lua:86-92, resetMedia :101-102. I also checked SimPanel :445/:454, Selector.lua:110 and ShowroomControls.lua:52. All are accurate. I ran my own sweep over the library and all 16 addons, excluding libs/ and tests/, for MenuFrame, GLOBAL_MOUSE_DOWN, UIDropDownMenu/EasyMenu, FULLSCREEN_DIALOG popups and show/hide toggles. It found no other uncovered pullout. The only other self-made menus are the LootHistory and BankLedger row menus, and they already listen for GLOBAL_MOUSE_DOWN. The LootHistory Browser.lua:310-312 'click-catcher' text is a historical comment, not live code. The diagnosis is right: this is a library fix that reaches every addon's Skin picker. The proposed registry would produce what the owner asked for, but a smaller fix exists (see corrections).

**Corrections:**

- Escape: UISpecialFrames is registered at OptionsSkinPicker.lua:1125, not :1129. The Escape comment is at :1097.
- dropFocus is at OptionsSkinPicker.lua:518-528, not :519-529. Also note that setOpen itself calls dropFocus(p) first (:607). So opening or closing the skin list already clears a media row's AceGUI pullout, and any fix must keep that order.
- test_options_pullout_close.lua has 24 pulloutCase tests, not 25. The 25 grep matches include the helper's own definition at :124. The range is :151 to the last case starting at :395, and the file is 405 lines.
- A smaller fix exists, and I'd recommend it over the cross-file registry. Give the skin list its own listener, the pattern Widgets.lua:474-503/:544 and LootHistory BrowserTable.lua:972-984 already use. In setOpen(:605-611), register GLOBAL_MOUSE_DOWN on f.list when p.open (through Core.SafeRegisterEvent, like OptionsCombat :281-284) and unregister it on close and in an OnHide hook. The list's OnEvent should call setOpen(false, p) when neither f.list:IsMouseOver() nor f.dd:IsMouseOver() is true. That is one file (PICKER_MINOR 9->10), with no OptionsCombat change (COMBAT_MINOR stays 4) and no version-skew case. The 24 R4-L1 tests stay untouched. Only the picker is uncovered, so a 'one watcher for every pullout' registry adds nothing today. Keep it as optional follow-up cleanup, together with folding the LH/BL row menus into Widgets.
- If the registry route is kept anyway, __OnPulloutPress (:289-300) needs more than an extra branch. Today it calls stopWatch() on its first line whenever no AceGUI pullout is focused, and stopWatch nils lib.__pulloutAce. The AceGUI 'let go' and the transient 'let go' must be split, or an open skin list loses its listener the moment any AceGUI pullout closes. The proposal also skips __OnPulloutFocus's surface gate for transients, which is correct, but the fix text should say so explicitly. The version-skew test it proposes (picker 10 over combat 4) is mostly moot. Both files belong to the same Options major and load from the same copy, and they guard on lib.MINOR (:157-160, :39-41).

**Missed:**

- The window-body press is a second symptom the owner will hit. A press on the picker's own body or title (OnMouseDown :1107), or on its eye or gear icons, also leaves the list open. Pressing the eye or gear should close the list and still run that button's click. Add both cases to the smoke step, not only body, world and Font.
- Pin a test that a press over a row in the open list does not close it before the row's OnClick runs pick(). The list keeps EnableMouse(true) (:973), so a press in the 2px gutter between rows also counts as 'over the list' and must not close it.
- Pin a test with two pickers open: setOpen(not P.open) at :994 uses the last-shown P, not that window's own p. The close callback must capture the specific p (as closed(p) does at :812), or an outside press could close the wrong picker's list. The listener-per-list approach avoids this naturally.
- The question for the owner about Escape is fine as written, and I agree with the recommendation to leave it unchanged. One additional point, not a question: the SkinNotice and settings-page Skin pickers are the same OptionsSkinPicker code. One re-vendor to the 16 addons fixes them all, so smoke only needs the /st picker plus one addon's picker, as proposed.

## Skeptic

**Verdict:** Mostly confirmed. The root cause is a value choice, not a bug: Ka0s Default's band is option E (LibKa0s/LibKa0s/SkinDefs.lua:486-488: title.bg #2C2408, bgTop #3A2F0A, bgBottom #1F1905, all opaque), and all four hosts paint it through the library's S.Shell/S.TitleBar. I checked each host call site and they match: LootHistory/modules/Browser.lua:71, BankLedger/modules/Browser.lua:980 and Export.lua:401, DropWatcher/core/CoreSetup.lua:101, WhatGroup/modules/FrameLayout.lua:62-63. Every test pin the investigator cited sits where they said: test_skin_defs.lua:800-802 and :810 (hex and swatch), :807-808 (lighter than the body), :774-789 (blend within 1/255), :745-772 (apart floor of 5% and rule of 10%). So does SkinDefs.lua:526 (the swatch), and the MultiMeters fallback at core/SkinSetup.lua:167 with its pin at tests/test_skinsetup.lua:336-350. I recomputed the numbers and they hold. Body composite #0E0E12 has L 0.00456. Gold contrast for option E is 9.0/10.5/12.0, Set 1 10.0/11.2/12.4, Set 2 10.6/11.7/12.7, Set 3 11.1/12.1/12.9. Every set's blend is within 0.5/255 of the stops' midpoint. The bottom-stop apart() values are 0.066, 0.058, 0.058 and 0.062, all of them carried by the blue channel. The images are Ka0s Default: the bands in 31, 32, 38 and 44 sample the same, #2F2300 at the top to #150E00 at the bottom, and 39 differs by one or two levels (#302400 to #140B00). The body renders at about #040108 against the token's #0E0E12, so the whole capture is uniformly darker (screenshot or gamma), not just the band. Set 2 is a sound fix for "a bit darker" that keeps the look the owner praised. The misses below are mostly doc and release-mechanics sites, plus one wrong statement about the other skins.

**Corrections:**

- Wrong statement about the other skins: they do not all set title.bgTop/bgBottom to none. Ember (#3A1A0F to #24100A), WoW Default (#4B4B4B to #252525) and WoW Midnight (#2A2347 to #17142B) have gradient bands. See SkinDefsOthers.lua:598, :653 and :711 (grad() writes <stem>.bgTop/.bgBottom, :182) and the docs table at LibKa0s/docs/api/Skin/version-15.1.26.8.17.16.17.4.9-docs.md:1559-1561. The investigator cited :1553-1555, but those rows are win.bg, win.bgTop and win.bgBottom. The conclusion still holds, because each skin states its own values, so a Ka0s Default edit does not leak into them.
- Wrong line numbers for the current docs table: the Ka0s Default title rows in version-15.1.26.8.17.16.17.4.9-docs.md are at :720-722, not :714-716. Lines :714-716 hold the same rows in the older file version-15.1.26.8.17.16.16.4.9-docs.md (also at :23 there), which is a superseded version and should stay as it is.
- The floor estimate is slightly off: #131002 has L 0.00513, so the real 'lighter than the body' floor (L > 0.00456) is nearer #110F02 to #121002. This does not change the recommendation, and Set 3's bottom stop (#141103, L 0.0056) is still above the floor.
- A 'Red gap' figure is mislabeled. apart() takes the largest channel, so for the dark-end stops (option E 0.066, Set 1 0.058, Set 2 0.058, Set 3 0.062) the binding channel is blue: the band is less blue than the bluish body. The 'red' figures quoted for the top stops are correct as the max channel.

**Missed:**

- A release step is missing from the fix. SkinDefs DEFS_MINOR is 26 at SkinDefs.lua:198. LibKa0s has a v1.85.0 tag on HEAD (2a78817, R4-REL3) that is local only: `git ls-remote --tags origin v1.85.0` returns nothing. Changing the values therefore needs another local re-cut of v1.85.0 and a new re-cut paragraph in docs/releasing.md, as R4-REL2 and R4-REL3 did. Every host's re-vendor must also come from the re-cut.
- A stale quantitative claim in the current API doc: version-15.1.26.8.17.16.17.4.9-docs.md:29 repeats the option E hexes and says 'Every stop stands off the body (6.6% at the dark end)'. That becomes 5.8% for Set 2, so the line needs rewriting or a new round-5 bullet that supersedes it.
- A missing host doc that quotes the hexes: WhatGroup/docs/frame.md:21 names #3A2F0A, #1F1905 and #2C2408 explicitly. LibKa0sSkinTester/docs/smoke-tests.md:244 (SHOW-45) also quotes the swatch #2C2408, which was cited. Prose-only mentions with no hex (BankLedger/docs/windows.md:14, MultiMeters/docs/ARCHITECTURE.md:337-346) need no edit.
- QuickComms reads title.bg for skins other than Ka0s Default. QuickComms/core/SkinSetup.lua:153 has `qc.bandBg` = { default = {0,0,0,0}, follow = "title.bg" }, so under Ka0s Default it draws nothing today and owes nothing for item 1. QuickComms/tests/test_skin_flip.lua:254 reads it live. Cross-topic note for the lead: if item 4 (the dial header) moves the QuickComms band onto title.bg or S.TitleBar under Ka0s Default, it inherits the new values. Sequence item 1's value change before item 4's smoke steps are written.
- Cross-topic note on MultiMeters: its meter header strip draws title.bg flat (modules/Window_Header.lua:223-228 titleBarColor, :448), so it shows the blend and not the gradient. Item 2 asks MultiMeters to look just like LootHistory. Whether MultiMeters should switch to the gradient belongs to topic 2, but it decides whether the SKIN_FALLBACK copy should also carry bgTop/bgBottom. Today test_skinsetup.lua:336-350 would pin those too, since it iterates every SKIN_FALLBACK entry.
- The EllesmereUI-derived look darkens too. SkinEUI.lua:115 FLAT_TOKENS clears title.bgTop/bgBottom, and title.bg is not in PANEL_TOKENS (:114), so the EUI look draws Ka0s Default's flat title.bg blend (SkinEUI.lua:333-341 derive from lib.DEFAULT). The darker blend therefore reaches EUI-themed owners. That is probably desired, but it should go in the CHANGELOG's 'moves a look' line.
- Consider a regression line. test_skin_defs.lua's R4-L2 case (:791-811) pins exact hexes only. Changing them should add a 'red under: option E's #3A2F0A/#1F1905 band' note to the case comment, following the file's convention, so the rationale for the darker values is recorded.
- The darkening in the images is not band-only, so no pixel-match target should be set from them. The client capture renders the band about 11 levels darker than its tokens (top #2F2300 against token #3A2F0A) and the body about 10 levels darker (#040108 against #0E0E12). Pixel targets taken from screenshots must allow for that, and the smoke text should describe 'darker than round 4' relatively rather than quote exact rendered hexes.
- An owner ambiguity worth one line: 'header' could mean the title band alone, or the band plus the tab strip under it (tab idle and tab.onBg 0.18 in image 31). The recommended answer is the band only, since the tab strip was not mentioned and the round 4 work was band-only.

## Skeptic

**Verdict:** Mostly CONFIRMED. I re-read every cited site and the claims hold. The surface is the Comms Pad bar window, not the radial dial. Images 40 and 41 show the situation chip, the '-' collapse button, the 'Solo' band and the button grid. The root cause is correct on both points. (1) The pad root is skinned with a table: NS.ApplySkin (core/CoreSetup.lua:99) passes into lib.ApplySkin (LibKa0s Core.lua:236-246), whose `S = skin == nil and ...` means the owner's Shell, and with it its top band (SkinPaint.lua:968-972), never runs. (2) The header shares R.BAND_TOKENS with the section bands (Pad_Render.lua:471), and qc.bandBg is {0,0,0,0} under Ka0s Default (SkinSetup.lua:153), so option E never reaches it. In other skins it draws a flat title.bg box with an edge, the same as the 'Solo' band. The host-only fix direction is sound. Header text should stay LEFT. Some details of the proposed fix are wrong or risky (frame level, WoW Default art inset, the test_layers pin), and the investigator stated one alternative too strongly.

**Corrections:**

- 'a backdrop color cannot draw one' is true of the current bandSkin path, but the investigator implies that is why a separate frame is needed. That part is wrong. P.box (LibKa0s SkinPaint.lua:775-790) handles a BackdropTemplate frame: with spec.extra and a gradient it clears the backdrop fill and draws the gradient as a BACKGROUND -7 region of the frame itself (boxGradient :738-744, P.subTex :360-364, P.SUB.grad = -7 at :356). So NS.Skin.TitleBar(inst.header) would paint option E directly under the header's OVERLAY text. The real reason for a separate frame is that two painters would then share one backdrop. R.ApplyHeaderLook (Pad_Render.lua:619-622) re-SetBackdrops the header, gated only by qcLookSig, while the library's live repaint calls P.backdrop on the same frame, so each would clobber the other's stored and following state. State the reason that way.
- Fix step 2's 'set headBand level to the root's level' is risky. P.box regions are textures of the target frame itself (P.tex / P.subTex). A child frame at the same level as the root ties with the root's own backdrop textures, which draw win.bg, and the winner is not deterministic. LootHistory does something else: titleBar is a plain child at the default level (root+1), anchored TOPLEFT 1,-1 / TOPRIGHT -1,-1 (Browser.lua:963-965). It ties with the library's inner-rule child, which is also root+1 and inset 1 (Core.lua:157-166). The pixels show the rule winning (image 31: x=7 is the rule, the band starts at x=8). The deterministic version is headBand at root+1 and inst.header raised to root+2, which is safe because the header's backdrop is CLEAR and edgeless while it follows. Alternatively, the gradient region can be drawn on the root at a sublevel above win.bg. Either way it is a layering change.
- Test pin missed: tests/test_layers.lua:117 `assertEqual(lv(inst.header), lv(inst.root) + 1)` turns red if the header is raised to keep the band below it. The investigator's proposed new layers test ('headBand level == root level') would pin the risky tie described above.
- tests/test_pad.lua:510-541 does not merely 'stay green if the stored path is untouched'. Under T.ownLooks it asserts skins[header].bg[4] == 0 and no edgeFile, so it pins FromSkin-off behaviour only, and the fix must leave headBand hidden there. Fine, but say so explicitly.
- Image 41's palette: the investigator calls it 'Azeroth-like'. The browns look like Ember or a similar warm skin. The skin is not proven from code, and the conclusion (title.bg flat box equal to the section band) does not depend on which skin it is.

**Missed:**

- WoW Default geometry is not addressed. There the pad window wears qc.winBorderStyle 'Blizzard Dialog' at qc.winBorderSize 16 (SkinSetup.lua:159-160, edgeOf at Pad_Render.lua:486-489), with an inset of floor(16/4+0.5) = 4 (Pad_Render.lua:518). The header is anchored at 0,0 (Pad.lua:346-347), so today its text at PL.PAD=4 and the '-' at -2 (Pad_Render.lua:759, 765) sit over the roughly 11px-wide dialog art. Under the proposed fix, headBand inset by insets.left (4) would paint the gradient under the art's visible frame as well. The owner asked for an edge and gap 'like LootHistory' in every skin, so the header row (text and collapse) also needs to move inside the art, not only the band. That likely means anchoring header and headBand at the art inset, and PL.Compute or HeaderMinWidth must then account for it.
- Up-growth: anchorEdge puts the header at the BOTTOM (Pad.lua:341-343). A title gradient there runs bgTop to bgBottom on a bottom row, so the owner needs to decide whether it flips. The drag handle also moves (Pad.lua:350-353). The investigator mentions mirroring the anchor but not the gradient direction or the owner call.
- TitleBar (SkinPaintExtras.lua:118-127) does not paint the header text, because headBand has no .title/.text. The header's text therefore keeps hud.label (test_skin_flip.lua:252), not title.text and the title font. That matches today's behaviour, but the gold-on-gold readability over option E (#3A2F0A to #1F1905) should be checked. LootHistory's title takes title.text through the Shell.
- Live repaint and teardown: when backgroundFromSkin is turned off, or a class colour is set, after TitleBar has painted headBand, the fix must call the library's unpaint, or hide headBand and rely on P.hide of its 'fill'/'grad' regions. Otherwise a stale gradient survives under the stored-colour backdrop. No test was proposed for the follow-to-stored flip.
- Other QuickComms windows that are in scope for the item 2/5 sweep were not checked by the investigator. The QC preview window (modules/PreviewWindow.lua:231 NS.Skin.Shell(f), which does draw the Shell top band; close button at :215-216 centred on band()) already follows the library. It is unaffected, but should be listed as checked.
- The section bands' R.SectionLook (Pad_Render.lua:630-641) shares bandSkin, so any change to bandSkin for the header must be header-only (a separate HEADER_TOKENS or flag), or the 'Solo' band changes too. The investigator raises this only as an owner question. It is also a correctness constraint on the fix.
- Owner question to add: under WoW Default, should the pad header sit inside the dialog art like the Skin Tester and LootHistory windows (recommended: yes, inset the row by the art's visible width), or keep today's flush row over the art?

## Skeptic

**Verdict:** The core diagnosis holds. In PGFE the min/max arrow sits on the band centre (PremadeGroupsFilterExtension/modules/Panel.lua:856), and the title keeps the template's TOP anchor inside a 20 px TitleContainer, because centerTitle (Panel.lua:964-970) re-anchors only the container, at y=-1, and alignTitle (Panel.lua:869-878) only justifies it. I confirmed this by tracing columns in images 42 and 43. The arrow's 20 px button box shows as rows 10-33 and 9-32, centres about 21.5 and 20.5. The title glyphs span rows 11-21 and 11-22, centres about 16, so the title sits about 5 screen px (about 4 UI px) high. The fix direction is sound: anchor every header child LEFT, CENTER or RIGHT to a band frame owned by the library. Most file:line claims check out: SkinPaint.lua:932-950, :967 and :1027; PerfPanel.lua:54/258/283; SimPanelRender.lua:70/168/175; DpsRace Style.lua:216 and Hud.lua:400/409/518-522; MultiMeters Window_Header.lua:315-333/383-384/452-454 and HeaderControls.lua:519; QuickComms ModalWindow.lua:58/99-104/132 and PreviewWindow.lua:204/216; LootHistory Browser.lua:964-1015; WhatGroup FrameLayout.lua:37-63; OptionsSkinPicker.lua:1038-1059; the mock_paint.lua lines; test_title_shape.lua:103-120; PGFE test_skin.lua:207 and test_panel_layout.lua:558-569. Four parts are wrong or need changing: (a) which skin image 42 shows, and so the "the font is not the cause" conclusion; (b) the claim that the DropWatcher popovers and the skin picker have no S.Shell band; (c) the claim that the PGFE test would go red first; (d) the plan for windows built from Blizzard templates, which should be handled once in the library rather than host by host. The sweep also missed the QuickComms dial (item 4), the Skin Tester's SettingsFrameTemplate sample, and DpsRace Results.lua:203.

**Corrections:**

- Image 42 is not Ka0s Default. It shows Ember: orange accent, a #FFB45A title in Emblem at 12.5 (LibKa0s/LibKa0s/SkinDefsOthers.lua:592-598). Ka0s Default's title is GOLD in Prototype (SkinDefs.lua:320 and 327). So 'the whole visible offset there comes from the anchor' is wrong. Emblem is the face the investigator measured as most off (+1.37 px hhea). The roughly 3.5 UI px from the anchor plus about 1.4 px from the font matches the roughly 4-5 px offset measured on screen. Image 43 has a white title and a yellow accent, so it is not Ka0s Default either. The anchor is still the main cause, but the screenshots do not prove the font adds nothing. Prefer the owner question that offers a per-face nudge as a follow-up for Emblem, Doris PP and Avant Garde.
- DropWatcher's OfferPanel and DetailCard popovers are said to 'have no S.Shell band'. That is wrong. NS.ApplySkin is lib.ApplySkin(frame, skin, addonName) (DropWatcher/core/CoreSetup.lua:100-102), and LibKa0s Core.lua:231-241 calls S.Shell(frame) for a registered owner. So OfferPanel (via ApplySkin) and DetailCard.lua:686 get the 30 px title.bg band at the inset, and the title at TOPLEFT 10,-9 and the close at -6,-6 (OfferPanel.lua:134-143, DetailCard.lua:688-691) are measured against a real band. The same applies to OptionsSkinPicker.lua:1054, which calls core.ApplySkin(f, nil, P.owner) and so S.Shell. Owner question 2's premise ('popovers have no header band today') should be rewritten. The real choice is whether those popovers keep the band S.Shell already draws, or pass noTopBar.
- The claim that the PGFE test would 'be red first: against today's PGFE the TitleText anchor is the template's TOP' is wrong. The PGFE mock builds TitleContainer.TitleText as a bare stub with no points (PremadeGroupsFilterExtension/tests/wow_mock.lua:343-348). An assertion of a LEFT/RIGHT, band-relative anchor is red only because there are no points at all. A 'no TOP anchor' assertion would pass vacuously. The mock must seed the template's anchors: TitleContainer at 58,-1 / -24,-1 with height 20, and TitleText at TOP y=-5, after confirming them in game with /dump. Only then does the characterization test reproduce the bug. The same applies to QuickComms and the Skin Tester's SettingsFrameTemplate NineSlice.Text and ClosePanelButton under mock_paint.
- The PGFE template is PortraitFrameTemplateMinimizable (tests/test_panel.lua:31), not PortraitFrameBaseTemplate as Panel.lua:958 says. The TitleText offsets are still from memory, so they need the in-game /dump before the mock is seeded.
- Line cite: SkinPaint.lua:1019 is `local style = ...`. The inset is computed only at :1027. The band function is at :932 and shellBands at :952.
- Fix altitude for windows built from Blizzard templates: the plan fixes PGFE (TitleContainer.TitleText) and QuickComms (NineSlice.Text and ClosePanelButton) separately in each host. S.Shell already knows these windows through opts.stock and markStock, and S.TitleBar is already called on NineSlice (QuickComms ModalWindow.lua:99-104, and the SkinTester ShowroomOwner.lua:117-127 sample). The smallest correct general fix is one library step in S.Shell or S.HeaderPlace. When a frame carries TitleContainer.TitleText, NineSlice.Text or ClosePanelButton, that step re-anchors them to the band centre and replays the change on every skin switch. Then all template windows are covered, and the Skin Tester sample pins it.
- QuickComms ModalWindow: MW.INSET_TEMPLATE.top is 24 (ModalWindow.lua:60), but S.Shell paints a 30 px band from the inset, so the page overlaps the band's bottom 6-7 px. Before choosing the anchors, decide whether the band is 30 px or the template's header (about 24 px): centring on a band the page covers would read as off-centre.
- DpsRace: the owner reports item 3, 'no header at all, in any skin', even though Hud.lua:474 and Results.lua:299 go through NS.ApplySkin → S.Shell. The band frame the fix relies on is therefore not visibly painted on these windows today, for a cause the investigator did not find. The centring fix for DpsRace depends on the item-3 root cause and should be sequenced after it. Separately, Results' tabs start at -HEADER_H (Results.lua:173) while the band runs from the inset to inset+30. With a 2 px border (midnight) the band would overlap the tab strip by 1-2 px once it is painted.
- DpsRace item 3a: a left-aligned path already exists. Hud.lua:518-520 anchors LEFT at TOPLEFT 10 when the title is 'marked'. Item 3a can reuse it or the proposed align=LEFT; it does not need the new primitive.
- In the headless kit, only the anchor shape can be checked. FontString GetStringHeight is 0 (mock_paint.lua:241), and CENTER/LEFT/RIGHT anchors centre the box, not the glyphs. In WoW a LEFT+RIGHT-anchored FontString centres its line box, descender included, so descender-heavy titles such as 'Premade Groups' still look a little high. The owner smoke step needs a 1 px tolerance, and the per-face nudge question stays open.

**Missed:**

- QuickComms dial (owner item 4): it has no header today, so the sweep never lists it. Any header added for item 4 must be built on the new band rule, title and close on band centre, and get its own all-skins anchor test.
- LibKa0sSkinTester modules/ShowroomOwner.lua:24 and :107-130 is a SettingsFrameTemplate sample window (Shell + FadeNineSlice + TitleBar on NineSlice with noBg + ClosePanelButton). It has the same template-anchor defect as the QuickComms ModalWindow. It is the natural library-level pin for template windows, and the sweep did not list it.
- DpsRace Results.lua:203 (viewToggle, RIGHT at -6-CONTROL_PITCH, -HEADER_H/2) and Results.lua:206 (the drag strip bottom at -HEADER_H) are missing from the DpsRace site list. Hud.lua:400 placeControl covers four controls, not two.
- The PGFE chevron's own centring inside its 20 px button was not checked. In image 42 the visible chevron rows (about 17-21) sit about 2 px above the button box's centre (about 21.5). If the ArrowUp/ArrowDown icon art is not centred in its 12 px box (ARROW_ICON at Panel.lua:796), centring the text on the band still leaves text and glyph visibly apart. Check buildMinMax's chevron anchor and the icon art's padding.
- MultiMeters' title row centre comes from TitleRowMid, floor((30-h)/2) (Window_Header.lua:318-322). With an odd difference the floor puts the row 0.5 px high on top of the 4 px band mismatch. Note it for the test tolerance or switch to an exact centre.
- OptionsSkinPicker: under the 2 px flat border skin (midnight), its TOP -8 title and -6,-6 close sit against a band at inset 2. Its title is also a GameFontNormal string repainted by Shell (P.font for rawget(frame,'title'), SkinPaint.lua:1031), so the font is skin-dependent. It belongs in test_title_shape like perf and sim, not as a low-priority note.
- Owner question to add (recommended answer: yes): should the per-face nudge ship now for Ember (Emblem), the face actually in image 42, instead of waiting for another smoke? Recommendation: the anchor fix first, then re-smoke Ember and High Contrast specifically, because Emblem and Doris PP are the largest measured offsets (about 1.3 px).

## Skeptic

**Verdict:** The investigator is mostly right. I re-read every DpsRace and DropWatcher site it cited and the root cause holds. In DpsRace, Results_Table.lua:318-328 (Cells.items, bound at :481-489) and Results_Usage.lua:340-341 (texture set at :402) create bare ARTWORK textures and never call SetTexCoord, Style.CropIcon, Style.IconEdge or S.IconBorder. Images 51 and 52 show exactly that: native bevel and no edge. In DropWatcher, the crop (zoom 0.1, Profile.lua:204) and the size are fine. The fault is the colour: IconStyle.lua:125 reads NS.Skin.Color("icon.border"), the HUD's black, not icon.outline. Ka0s Default's black is on the same near-black as the card (image 53), and WoW Forever's FV_EDGE #3a3530 (SkinDefsOthers.lua:285, :306) almost matches the card background (image 56). Obsidian and Azeroth look right only because their icon.border and icon.outline values are equal (:298, :300). Two parts of the proposed fix would misbehave as written: the class-atlas edge and the pooled AceGUI image edge (see corrections). The sweep also missed a few judgement calls and evidence points, listed below. Images 51 to 56 were checked by eye; I did not re-sample pixels.

**Corrections:**

- DropWatcher: the colour read is at modules/IconStyle.lua:125, inside the borderColorFromSkin branch at :123-126, not :121-124. The width read (edgeSize = max(1, icon.borderSize), in UI units) is at :116-117. Defaults/Profile.lua:206 still has borderSize = 2 and its comment says '2 pixels'. borderStyleFromSkin = true (:218) overrides it with icon.borderSize = 1 (LibKa0s SkinDefs.lua:442), so the 2 screenshot px are 1 UI unit at the owner's UI scale. That fits the PLAUSIBLE width claim, but the stale default and comment should be fixed together with it.
- DropWatcher: WG.ItemButton is defined at modules/WindowGroup.lua:508. It wraps the local itemButton at :471-487, and setItem at :491-499 calls IS.Apply again with the link. The investigator gave only :471-486.
- DropWatcher tests: tests/skin_switch_facts.lua:146-153 does not pin black. It only checks that the border frame follows the two companions across a skin switch, so it should survive the token change as long as the fact reads the token rather than a literal. The tests that really pin black are test_skin_flip.lua:263 and :265 and test_icon_style.lua:65. Also, test_skin_flip.lua:239-247's tintedSkin sets only icon.border. After the fix the reader must fall back from icon.outline to icon.border, as SquareIcon does at SkinPaintControls.lua:853, or that test skin loses its colour.
- DpsRace class icon: the proposed fix of CLASS_ICON_TCOORDS trimmed plus 'the same edge' is wrong if the edge is S.IconBorder on the class Texture itself. zoomIcon (SkinPaintControls.lua:917-924) clamps coords in whole-texture space: max(0.07, c1), min(0.93, c7). On a sub-rect of UI-CHARACTERCREATE-CLASSES (Results_Table.lua:40) that crops 28% of a top-row or left-column cell, and it replays on every repaint. Tbl.SetClassIcon (:114-123) also re-sets the coords on every bind. Either pass zoom = false, or edge a separate bare Texture over it, as MultiMeters does (Row_NameCell.lua:136-141 makes its own 'edge' Texture so the zoom lands on nothing). The sub-rect trim belongs inside SetClassIcon, copying Row_NameCell.lua:428-431. The same applies to BestToast.lua:194-196 and :222, which call the same SetClassIcon.
- LibKa0s OptionsIdList.lua:929-931: the crop needs no extra undo. AceGUI Label:SetImage(path, l, r, t, b) takes texcoords and resets them to 0,1,0,1 when none are passed (AceGUIWidget-Label.lua:109-124), and OnAcquire calls SetImage(nil) (:78). So `lbl:SetImage(icon, 0.07, 0.93, 0.07, 0.93)` is pool-safe on its own. The AceGUI Icon widget's SetImage behaves the same way, so the same applies to KickCD Spells_Rows.lua:122 and QuickComms Editors.lua:411, :564 and :686. The real pooling hazard is the S.IconBorder record, which the investigator did not name. AceGUI widgets are shared across every addon through LibStub. Label:SetImage(nil) never Hides the image Texture (only imageshown = nil plus ClearAllPoints, :121-123 and UpdateImageAnchor), so followShown (SkinPaintControls.lua:856-865) never hides the holder. The edge record and its zoom replay then stay on a pooled label that another addon later acquires for text only or for an atlas glyph. Draw the library edge on a holder the id-list row owns and release it in entryRelease, or unpaint the record on release, never on the pooled AceGUI image.
- KickCD settings/Spells_Header.lua:72: the ClassIcon_ |T markup is only the fallback when CreateAtlasMarkup('classicon-<class>') fails (:69-71). Normally an atlas glyph is drawn, which the rule exempts, so this is a low-value site. :107 (spec icon markup, `:16:16:0:0`) is a real miss.
- MultiMeters tooltip markup: :551 (DEATH_ICON 237275) and :675 (TARGET_ICON, Interface\ICONS\Ability_Hunter_FocusedAim, Tooltip.lua:107) are both real Interface\ICONS art, so the crop applies to them as well as to the spell icons at Tooltip_Builders.lua:234 and Tooltip_Lines.lua:710. The format must grow from `:%d:%d:0:0|t` to `:%d:%d:0:0:64:64:5:59:5:59|t`.
- Minor: the claim that S.IconBorder's Texture form follows Bind.items's SetShown is right, but the hook is at SkinPaintControls.lua:856-865, not :860-868. SetTexture in Bind.items does not reset texcoords in the client, so a CropIcon applied once at Cells.items survives every bind, and IconBorder's tighten-only zoom (:921-923) keeps the 0.08.

**Missed:**

- The owner's reference, Loot History, draws no Blizzard item art in its window. Its only icon-like marks are the bound-lock glyph (BrowserTable.lua:714-722) and class markup (:182). So 'like LootHistory' for icons can only mean the library's icon.outline 1 px edge (#4D4D57 under Ka0s Default, SkinDefs.lua:195-197) as drawn by WhatGroup and DpsRace Results_Compare.lua:678. The plan should name those as the visual reference for smoke, not Loot History.
- DropWatcher already classifies its toast as a window surface for text: defaults/Profile.lua:235 says 'the window, the cards and the toast are window text'. That is direct evidence against the recommended answer to question 3 (toast = HUD) for DropWatcher. Put it to the owner, and if the toast stays HUD, say so explicitly, because it diverges from the addon's own font scope.
- DropWatcher has a built-in per-item quality border (icons.borderQuality, default false, Profile.lua:209, painted at IconStyle.lua:166-169). It is an alternative to a grey outline on the epic-purple cards in images 53 to 56 and is worth one line in the owner question. The fix must keep the class and quality companions ahead of the new icon.outline read.
- DropWatcher settings text: the Window > Icons composed block documents the skin colour as `icon.border` (Profile.lua:216-217 comment, and the row descriptions that FS-DW-FLIP added). Those strings and the docs need the same token change, or the settings will describe the wrong token.
- QuickComms settings/Editors.lua:486 (`g:SetImage(spec.texture())`) was not examined. Settle whether it draws game icon art or a glyph before closing the sweep.
- AuraMaster window-side sites: Style_Bars.lua:380 and Style_Text.lua:696 (`am.icon:SetTexture(aura.icon)` for placeholders/preview) go through Style.LayoutIcon (Style.lua:255-266) with iconZoom 0.08 by default (defaults/Profile.lua:263, :312) and a user-set border. They pass the crop, but the edge is the user's AuraMaster border, not icon.outline, so they are compliant only under the HUD reading.
- ConsumableMaster MacroBarButton's crop is the user's iconZoom = 8% (defaults/Profile.lua:234, applied at MacroBarButton.lua:553-555), and KickCD's is zoom 0.10 (defaults/Profile.lua:47). Both are user-adjustable down to 0. The rule should say the default must be at least 0.07 and that the player may override it, or these will be flagged as non-compliant later.
- DpsRace Hud_Best.lua:114 (HUD best-card tooltip) uses ResultsUsage.InlineIcon, so changing InlineIcon to the 5:59 crop fixes both the Results tooltip (Results_Tips.lua:165) and the HUD tooltip. Hud_Best.ConsumableIcon (:77) already uses that form, so InlineIcon should probably share it as one helper.
- Test gap to add: none of DpsRace's tests/test_icon_crop.lua cases (:69, :77, :92, :115) covers the Used column, the Usage list, the Class/spec column or BestToast. tests/test_hud_icon_edge.lua has the edgeColor helper (:54) to assert icon.outline on the window sites and icon.border on BestToast if it is ruled HUD. DropWatcher needs a case asserting icon.outline under Ka0s Default (#4D4D57) and under WoW Forever (#5a5048 vs FV_EDGE).

## Skeptic

**Verdict:** The root cause holds up. I re-checked every file:line claim I relied on and all of them hold. Shell paints its "top" band as a BACKGROUND -5 texture on the window frame itself (LibKa0s/LibKa0s/SkinPaint.lua:931 band(), :966-971). Every DpsRace window is a BackdropTemplate frame: Hud.lua:463, Results.lua:274, Results_Timeline.lua:448, Results_Gear.lua:349. Each takes the shellBackdrop arm (:987-991, :1046-1050), so the backdrop's own Center fill (win.bg 0.06/0.06/0.08/0.92, SkinDefs.lua:324) covers the band. Every window the owner calls good draws its header on a child title-bar frame, with Shell under noTopBar: LootHistory Browser.lua:963-999 and :1123, DropWatcher Window.lua:560, WhatGroup FrameSkin.lua:82, BankLedger Browser.lua:1093. PGFE's band shows only because Panel.lua:1007 is not a backdrop frame. The library already relies on this layering: P.box draws a backdrop control's gradient at BACKGROUND sublevel 1, documented as "over its fill" (SkinPaint.lua:734-740). I could not refute any of it. The debug console path is confirmed too: DebugLogWindow.lua:324-336 is the drag bar that nothing paints, :554 is the BackdropTemplate frame, :584 is ctx.applySkin, and DebugLog.lua:305-312 goes through Core.ApplySkin(f, nil, owner), which reaches S.Shell at Core.lua:240. The fix direction (move the band above the backdrop fill in the library) does what the owner asked for items 3 and 4, and the plan for 3a is right. The proposal has one real ripple it does not cover: it also moves the "bottom" bar, which would change LootHistory, the owner's reference window. Several of its details need tightening (see corrections).

**Corrections:**

- Do not move the 'bottom' bar together with 'top'. LootHistory, the window the owner says looks fantastic, is a BackdropTemplate frame (Browser.lua:940) and calls Shell with { noTopBar = true, bottomBar = FOOTER_H } (Browser.lua:1123). Ka0s Default sets foot.bg = {0.04,0.04,0.05,0.9} (LibKa0s/LibKa0s/SkinDefs.lua:489), even though the host comment at Browser.lua:1122 says 'none on Ka0s Default'. That footer band is covered by the backdrop today, so lifting 'bottom' out of BACKGROUND would make a new near-black strip appear across LootHistory's footer, the 'black strip' look item 2 asks to get rid of. Move only the 'top' band, or settle foot.bg first: set it to false in Ka0s Default, or have the owner rule on it. Then add a test that LootHistory's footer band stays unchanged.
- Suggested layer refinement: rather than BORDER -8, keep the band in BACKGROUND with a positive sublevel above the backdrop Center (Center is BACKGROUND in the kit, tests/_kit/mock_paint.lua:397). The library already puts a backdrop box's gradient at BACKGROUND 1 'over its fill' (SkinPaint.lua:740). On backdrop frames that means grad 1, art 2, top 3. The 'grad' and 'art' corollary is then fixed in the same change, and the bands stay under any host BORDER regions instead of over them. BORDER also works, but it lifts the band over host BORDER textures, so 'grad' had to be deferred.
- The claim that LootHistory's debug console has a band 'is not backed by any screenshot' needs a qualifier. OWNER_ANSWERS.md item 2 tells us to treat round 4's 06_SMOKE_TESTS.md as passed apart from the items this feedback raises, and SR4-2 (06_SMOKE_TESTS.md:55) includes '/dr General > Skin' and a debug console (/bl debug). The owner's blanket pass therefore covers SR4-2 even though the code gives no console a band, and DpsRace SM-DR-R4RV2 contradicts images 34-37. Treat that blanket pass as unreliable for the band, not as evidence either way. The library's own comments expect the band on the console, the copy window, the sim panel and the perf panel (DebugLogWindow.lua:52, WidgetsCopyWindow.lua:24, SimPanelRender.lua:27, PerfPanel.lua:16), which strengthens the case for the library fix.
- Location fix: band() starts at SkinPaint.lua:931 (the comment is at :929-930), not :936. The top-band lines :966-971 and shellRegions at :981-984 are correct.
- 3a detail: the drag strip does not exist yet when buildHeader sets the title's point (Hud.lua:409; the drag strip is created at :427-437). The RIGHT anchor to ui.drag must therefore be added after line 437, or placeTitle must be called once at the end of ensureWindow. placeTitle's early return (`if ui.titleMarked == marked then return end`, Hud.lua:513) would otherwise leave a one-point title if buildHeader alone set LEFT. Simplest: delete the CENTER arm (:521-523) and the early-return guard's role for the plain state, so placeTitle always sets LEFT at TOPLEFT +10 and RIGHT to ui.drag -4.

**Missed:**

- Ripple through double-paint hosts: DropWatcher Window.lua:558-560, WhatGroup FrameLayout.lua:62 followed by FrameSkin.lua:82, and MultiMeters Window_Frame.lua:89-91 (paintShell, called again at :309 and :481) each call NS.ApplySkin(frame) first, which is Shell without noTopBar, and then Shell(frame, { noTopBar = true }). This works only because P.track keeps one record per frame, so the last opts win (SkinPaint.lua:853-866). Once the band is visible, any path that calls NS.ApplySkin(frame) alone later, or the facade replaying the first call, would show a band behind those child title bars. Pin it with a test that, after both calls and a skin switch, the 'top' region stays hidden on those hosts.
- Other facade Shell windows without noTopBar that the investigator did not list: QuickComms settings/ModalWindow.lua:99, S.Shell(f, { stock = ... }) on a template-built window (created at :113, with a BackdropTemplate fallback at :121 and :127). If the template has no backdrop, it already shows a band today and the fix leaves it alone. Check it so it does not end up with a band twice or not at all. The investigator did list QuickComms PreviewWindow.lua:231. AuraMaster CoreSetup.lua:161 passes a keys table, so S stays nil and Shell is never reached, and nothing consumes it (per its comment). Not affected.
- Toast ripple scale: Toast.lua:220 already reaches S.Shell through Core.ApplySkin(f, nil, owner). After the fix, a 30px band at the top of a small toast would be very visible. Toast.decorate must change in the same commit (call the facade's Shell with noTopBar after ApplySkin, as SimPanel.lua:384-385 does for its buttons), not as a follow-up.
- Vertical centring (item 5), verified: Style.TITLE_BAR_H = title.height or 30 (DpsRace modules/Style.lua:216), and the controls sit at -HEADER_H/2 (Hud.lua:399-400). The band runs from inset 1 to 31, so its centre is -16 while the content sits at -15. That is a 1px offset in the HUD, Results (:191), Timeline (:206) and Gear (:271), and should go into the item-5 sweep. The library console's drag bar is inset 1 (DebugLogWindow.lua:328-330), so its title is centred on the bar and lines up with the band.
- Results-side 3a scope: Results, Timeline and Gear titles are anchored CENTER/TOP (Results.lua:190-191, Results_Timeline.lua:205-206, Results_Gear.lua:270-271). The owner only named the HUD (image 45). The investigator's third owner question covers whether those stay centred, and I agree with its recommended answer.
- Test to add for the band layer: the kit records layer and sublevel (mock_paint.lua:128-129, :262). In test_skin_paint.lua next to :98-111, assert that on F.window the top band's __layer/__sublevel draws above the backdrop Center, and that LootHistory-style { noTopBar, bottomBar } leaves 'bottom' where it is today (or hidden), so the reference window cannot regress without a failing test.

## Skeptic

**Verdict:** The investigator is right on the main points. I re-read MultiMeters/modules/Window_Header.lua:451-456 and confirmed that headerBG is anchored at (pad, -pad) with height layout.titleHeight and painted flat with SetColorTexture. pad is 6 (defaults/Profile.lua:135) and titleHeight is 26 (Profile.lua:254-257). paintShell passes noTopBar (Window_Frame.lua:83-92), so Shell draws no band of its own. Sampling image 33 at x=400 gives: y11 black edge, y12-13 grey inner rule, y14-17 dark win.bg (the "black strip"), then a flat (34,25,0) band from y18 to y49. The row at y=30 shows the same thing on the left: x15 black, x16 grey, x17-21 dark, band from x22. The MultiMeters root cause is correct: the band reuses the row padding as its edge inset, and it is flat title.bg only (titleBarColor at Window_Header.lua:225-229 reads looks.titleBg, cached from title.bg only at core/SkinSetup.lua:235). LootHistory's reference is correct as stated: titleBar at (1,-1) with SKIN.titleBarH 30 (Browser.lua:14, 963-966), S.TitleBar at 999, and Shell with noTopBar plus bottomBar at 1123. The library's Shell draws its bands at `style == "flat" and win.borderSize or 1` (SkinPaint.lua:1027-1028) and P.fill draws the bgTop/bgBottom gradient (SkinPaint.lua:398-417). The spot-checked sweep sites are at the lines claimed: OptionsSkinPicker.lua:1039-1040, DetailCard.lua:686-688, WidgetsCopyWindow.lua:194-196, DebugLogWindow.lua:324-330, OfferPanel.lua:214, Showroom.lua:238-241 and 291-292, WhatGroup FrameLayout.lua:37-39, and Pad.lua:289 and 341-347. The tests pin current behaviour where claimed (test_skin_window.lua:91 asserts headerBG.__colorTexture == title.bg). The proposed host-only fix would produce the LootHistory look for the MultiMeters meter. It needs the corrections below: the inset token, the minimized height, and the way the gradient is reset.

**Corrections:**

- Wrong token for the band inset. The fix anchors headerBG at `win.inset`, saying it is "1 in every skin", but Shell does not use win.inset. It insets its bands by `style == "flat" and T["win.borderSize"] or 1` (LibKa0s/LibKa0s/SkinPaint.lua:1027-1028), and borderSize varies between skins. SkinDefsOthers.lua:710 is a flat 2px window edge (edge(2, "flat", MN_GOLD)). The nine-slice skins (Glass edge(8, ...) at :493, Blizzard Dialog edge(32, ...) at :651) fall back to inset 1. The fix should copy Shell's rule: `local st = Token("win.borderStyle") or "flat"; local e = st == "flat" and (Token("win.borderSize") or 1) or 1`. Under borderColorMode class or custom, use the player's own edge size instead.
- Minimized height is off by one. With the band at y=e..e+30 and a bottom edge of e, a collapsed frame needs TitleBandHeight() + 2*e (32 under Ka0s Default), not TitleBandHeight() + e (31). At 31 the bottom 1px edge and inner rule sit on the band's last row. The line is Window_Header.lua:882 (`padding*2 + titleHeight`); the investigator cited it correctly.
- Band height. TitleBandHeight() is padding + titleHeight - BAR_INSET (Window_Header.lua:330-333), so the proposed band grows and shrinks with the player's Padding and Header height settings. It only equals LootHistory's 30 (title.height, SkinDefs.lua:327) at the defaults. That is acceptable, and it keeps the title row centred (TitleRowMid at 315-320), but the report should say it is 30 only at the default settings.
- Gradient reset detail. P.fill (SkinPaint.lua:405-417) resets with `SetGradient("VERTICAL", WHITE, WHITE)` only when the texture was previously gradiented. A host copy has to track that state per texture, or a custom swatch drawn after a gradient will be tinted. The kit colour-literal rule allows SetColorTexture(1,1,1,1) followed by a SetGradient on the same name (tests/_kit/skin_values.lua:341-356, isWhiteBase). A literal CreateColor(1,1,1,1) in the reset may still be flagged, so reuse a named white constant. Other skins set title.bgTop/bgBottom to `false` rather than nil when the band is flat (SkinDefsOthers.lua:185-195, put()), so the gradient branch must test for truthiness, not for non-nil.
- QuickComms pad (item 4): the problem is more than a missing header band. Pad.lua:289 calls `NS.ApplySkin(root, NS.SKIN)`, and Pad_Render.lua:602 calls it with `wl.skin`. Both pass a skin table, so Core.ApplySkin never hands the frame to the owner's S.Shell (LibKa0s/LibKa0s/Core.lua:232-240, where `S` is nil when `skin ~= nil`). The pad therefore has none of the skin's win.border plus win.inner edge that LootHistory has. Being consistent with LootHistory needs the root painted through Shell (or the pad's look mapped onto it) as well as a title.bg band. The header can also be anchored at the BOTTOM of the root for up-growth pads (Pad.lua:342-344, anchorEdge), so a fixed top band at (e,-e) would be wrong for those pads.
- DpsRace (item 3): Style.TITLE_BAR_H comes from the skin token `title.height` (modules/Style.lua:216), not a constant. It matches Shell's band height, so the HUD title is centred on the band Shell should draw. The investigator's call that something hides the band remains unexplained; I found no SetAlpha or region hide in Hud_Appearance.lua either. That stays with item 3.

**Missed:**

- Blizzard Settings and AceConfig pages are out of scope for the sweep. Every addon's Profiles page opens AceConfigDialog into an embedded container (for example LootHistory/settings/Profiles.lua:68 and MultiMeters/settings/Profiles.lua:105), and LibKa0s has no AceGUI `Frame` window painter (SkinAce.lua lists only widget painters at 364-730). No addon opens a standalone AceGUI Frame window, so there is no further window to fix here. The sweep should say this explicitly.
- QuickComms PreviewWindow.lua:139 (`NS.Skin.Shell(b, { noTopBar = true })`) and SimPanel.lua:384-385 paint button boxes, not windows. Excluding them is correct, but the sweep did not name them.
- PartyFrameEnhanced StandIn.lua:154 (a named UIParent frame on BackdropTemplate) and AuraMaster FramePicker.lua:113 (an overlay) are top-level frames, not titled windows, and neither calls Shell or ApplySkin. They fall outside the LootHistory window structure and should be listed as checked and excluded.
- Toast (Toast.lua:220) gets Shell's 30px top band. If a toast is only about 30px tall, it is all band. That is worth a smoke check, but it is not a window in the owner's sense.
- Missing test: no test pins Shell's flat-versus-nine inset rule for a host-drawn band. Add a MultiMeters test under a 2px flat skin (the SkinDefsOthers.lua:710 skin) asserting that headerBG's first point is (2,-2), alongside the proposed Ka0s Default pin at (1,-1).
- After the move there is a 1px win.bg seam between the band (bottom at e + TitleBandHeight = 31) and the column strip at pad + titleHeight = 32 (Window_Header.lua:710-711 and 835-836). This is cosmetic. Either accept it, or note that LootHistory also leaves its 1px dividerBar (Browser.lua:1005-1009) under the band.
