# 06 — Smoke tests (owner-run, in client)

The owner runs these. Nobody marks one passed but the owner. Each row: id, the item it checks, the check, result.

| Id | Item | Check | Result |
|---|---|---|---|
| SM-LK-10 | LK-10 | after any addon re-vendors v1.76.0, `/dw test` still shows the amber strip exactly as before (same tint, mark, gold text) | pending |
| SM-DC-21 | DC-01 | After dev-copilot 2.5.0 is installed (/plugin update + /reload-plugins), in ../DropWatcher run /dev-copilot:bump-version with the next patch version. Before any battery runs, the command lists modules/TestMode.lua, the modules/Sim*.lua files, core/SimSetup.lua, settings/SimVerbs.lua and the sim suites, then asks the re-look question. Answer 'Stale, stop now': it stops, names the files, and git status is clean. | pending |
| SM-DC-22 | DC-01 | In ../PrettyChat (no preview file names), run /dev-copilot:bump-version with the next patch version. The command still asks (the empty list is never silently Not applicable) and offers Not applicable only behind a confirmation. Answer 'Stale, stop now': git status is clean. | pending |
| SM-BL-11 | BL-01 | /bl sim start bank: the ledger window and the step panel open, the footer shows Pause, Restart and Stop (no Run all), and the five steps play about 1 s apart with nothing pressed. History gains the simulated rows as before. | pending |
| SM-BL-12 | BL-01 | Mid-run, click the next row: the run pauses (Resume shows) and one step plays. Resume continues. Settings > General > Simulator > Simulation step delay's tooltip no longer mentions Run all. | pending |
| SM-BL-10 | BL-10 | `/bl test` with the ledger open: amber strip under the filter bar, NO red TEST MODE beside the title, panes start under the strip, tooltip on the strip | pending |
| SM-BL-11 | BL-10 | `/bl sim start <scenario>`: the ledger window shows a CYAN strip saying 'Simulation: <scenario> - nothing here is saved.', no header word; hover shows the Simulation tooltip; `/bl sim stop` removes it and the panes move back up | pending |
| SM-BL-12 | BL-10 | during a simulation the session window shows the cyan strip under its title bar and the rows sit under it | pending |
| SM-DW-11 | DW-01 | /dw sim start key: the panel's footer shows Pause, Restart and Stop (no Run all), and with nothing pressed the steps play about 1 s apart, each printing 'Simulation step n of 11: ...', ending with the finished line. | pending |
| SM-DW-12 | DW-01 | While a run plays, click the next (ready) row: the run pauses (the button reads Resume) and exactly that one step plays. Click a row three ahead: the steps up to it play back to back and the run stays paused. Press Resume: it continues at the step delay. | pending |
| SM-DW-13 | DW-01 | Press Restart mid-run: the scenario starts again with a fresh seed and plays on its own from step 1. | pending |
| SM-DW-14 | DW-01 | /dw sim start raid 10, then /dw sim pause at once while the pool is still loading: when the pool is ready nothing plays. /dw sim resume plays it, and /dw sim run, typed while it plays, prints 'The timeline is already playing.' | pending |
| SM-DW-10 | DW-10 | `/dw test`, full layout: amber strip under the filter bar, NO red TEST MODE beside the title; strip tooltip unchanged | pending |
| SM-DW-11 | DW-10 | minimize the window in test mode: the title bar shows TEST MODE (TEST in compact) again; expand: the word goes, the strip returns | pending |
| SM-DW-12 | DW-10 | `/dw sim start raid 10`: a CYAN strip under the filter bar with the simulation line, no SIMULATION word in the title; hovering the strip shows the scenario tooltip; `/dw sim stop` removes it | pending |
| SM-DW-13 | DW-10 | compact layout at about 380 px during a simulation: the short sim line wraps to two lines and the panes move down; the title is centered alone | pending |
| SM-LH-11 | LH-01 | /lh sim start loot: the History window and the step panel open, the footer shows Pause, Restart and Stop (no Run all), and the steps play about 1 s apart on their own (each waiting for the ledger to settle) to the finished line. | pending |
| SM-LH-12 | LH-01 | Mid-run, click the next row: the run pauses and one step plays. Press Restart: it starts again with a fresh seed and plays on its own. | pending |
| SM-LH-10 | LH-10 | `/lh test`: amber strip under the filter bar, NO red TEST MODE beside the title, every tab's pane starts under the strip, strip tooltip says Test mode | pending |
| SM-LH-11 | LH-10 | `/lh sim start <scenario>`: a CYAN strip with the simulation line, NO SIMULATION word beside the title, strip tooltip says Simulation; `/lh sim stop` removes it and the panes move back up | pending |
| SM-LH-12 | LH-10 | entering combat during test mode removes the strip and the panes move back up (no header word appears) | pending |
| SM-MM-01 | MM-01 | `/mm test` with the header shown: the amber strip under the title and NO red TEST MODE in the title text | pending |
| SM-MM-02 | MM-01 | minimize a window in test mode: the title shows the red TEST MODE; expand: it goes and the strip returns | pending |
| SM-KC-1 | KC-01 | In game, out of combat: /run local d=C_DurationUtil and C_DurationUtil.CreateDuration and C_DurationUtil.CreateDuration(); print(d ~= nil, d and pcall(d.SetTimeFromStart, d, GetTime(), 10), d and d.GetRemainingDuration and d:GetRemainingDuration()) prints true true and about 10 (proves Compat.NewDuration's constructor and setter names) | pending |
| SM-KC-2 | KC-01 | Target a hostile caster that casts an interruptible spell with visibility = target_casting_interruptible: the grid shows, the cast bar fills with interruptible colors, and an uninterruptible cast masks the grid as before (no behavior change from the Compat move) | pending |
| SM-KC-3 | KC-03 | /kcd help lists sim; /kcd disable then /kcd sim prints the library's disabled line; /kcd enable restores it | pending |
| SM-KC-4 | KC-05 | Solo, out of combat, grids locked: /kcd sim opens the step panel docked beside the target grid with the first scenario previewed; /kcd sim start pull prints the host's STARTED line and the run plays on its own | pending |
| SM-KC-5 | KC-05 | Each refusal prints its one line and starts nothing: while unlocked (/kcd unlock), in combat on a dummy, in a group, in an instance, with Target and Focus both disabled | pending |
| SM-KC-6 | KC-06 | Start /kcd sim start pull, then attack a training dummy: the simulation stops with the combat line, the strip and panel clear, and the real grid shows your real cooldowns | pending |
| SM-KC-7 | KC-06 | During a simulation /kcd unlock and the launcher's Locked entry refuse with the end-the-simulation line; /kcd resetall refuses; unticking Lock frame in settings stops the simulation with the unlocked line | pending |
| SM-KC-8 | KC-06 | During a simulation /kcd disable stops it first (the stood-down line), then the addon stands down; /kcd enable brings the grid back with real cooldowns | pending |
| SM-KC-9 | KC-06 | During a simulation, target a real mob and cast at it: the simulation keeps running and the grid and cast bar keep showing the simulated world; /kcd diagnostics has a sim section naming the scenario and step | pending |
| SM-KC-10 | KC-08 | /kcd sim start pull with visibility = target_casting: the grid appears as Caster A casts, your kick's swipe starts when you kick, Thrall's and Jaina's [sim] lines print, the CC step dims the other spells for a GCD, combat-ended returns the grid to its idle state | pending |
| SM-KC-11 | KC-08 | /kcd sim start boss shows a 2-charge badge on your kick, counting 2 -> 1 -> 0 with the recharge swipe, and back to 2 on the expire step; /kcd sim start miss shows the uninterruptible cast colors, then the interruptible ones after the shield breaks | pending |
| SM-KC-12 | KC-08 | /kcd sim start leave: after Valeera leaves, the focus bar clears and the target bar picks up Bonecaller's cast mid-way, and your kick interrupts it | pending |
| SM-KC-13 | KC-09 | During /kcd sim start pull the sim strip sits above the Target label (or above the grid with the label off), reads 'Simulation: <scenario> - /kcd sim stop ends it.', stays visible while visibility hides the grid between casts, and disappears on /kcd sim stop | pending |
| SM-KC-14 | KC-09 | Disable Target in settings during a simulation: the strip moves above the Focus grid; disable both: it floats near screen center; no Lua error | pending |
| SM-KC-15 | KC-10 | Read README's Simulator paragraph and /kcd sim's usage lines in game: they agree on the scenarios, the safety claims and how to stop | pending |
| SM-MM-21 | MM-10 | In a real 5-player dungeon, the grid shows every member with role icons and the roster sort orders them as before (Compat routing changed nothing live). | pending |
| SM-MM-22 | MM-10 | Hide-when-solo and only-in-combat visibility rules still hide and show the window at the right edges. | pending |
| SM-MM-23 | MM-11 | /reload in game: windows populate, combat start/end and a zone change still re-evaluate visibility, and /mm diagnostics shows no rejected events beyond the usual ones (dispatch rewire). | pending |
| SM-MM-24 | MM-12 | /reload with the addon loaded: no Lua error, and /mm diagnostics loads (seam installed at load). | pending |
| SM-MM-25 | MM-15 | Solo outside an instance, /mm sim opens the step panel docked to a window. Start plays the run at once and every MultiMeters window shows the SIMULATION strip. | pending |
| SM-MM-26 | MM-15 | /mm sim start dungeon refused in a real group, in an instance, in combat and with test mode on, each with its own line. | pending |
| SM-MM-27 | MM-15 | Pull a training dummy mid-simulation: the simulation stops with the combat line, and the windows show live data again. | pending |
| SM-MM-28 | MM-15 | After /mm sim stop, the windows show the same segments and pins as before the start, and /mm test works again. | pending |
| SM-MM-29 | MM-16 | /mm sim start dungeon: the bars grow during each fight, the segment dropdown lists Trash then Speaker Shadowcrown, and the boss death shows in the Deaths column with a recap tooltip. | pending |
| SM-MM-30 | MM-16 | /mm sim start raid: a 20-row grid, the pet's damage follows the Merge pets setting, and no duplicate player row. | pending |
| SM-MM-31 | MM-16 | /mm sim start wipe: everyone dies, Reset meter data clears the segments (Blizzard's own meter untouched afterwards), and the re-pull starts a fresh segment. | pending |
| SM-MM-32 | MM-16 | /mm sim start zone: a window set to hide outside instances hides during the Isle of Dorn step and returns in the second dungeon. | pending |
| SM-MM-33 | MM-16 | Mid-simulation, Export to Raid prints [sim] lines in chat and nothing is sent to the group. | pending |
| SM-MM-34 | MM-17 | During /mm sim every window shows the SIMULATION strip under its title (its own tint, distinct from the test strip), including a window with its header hidden; no SIMULATION word in any title; the strip goes away at stop. | pending |
| SM-MM-36 | MM-19 | /mm diagnostics during a simulation shows a sim section with the scenario and step; after /mm sim stop it shows the last stop reason. | pending |
| SM-QC-1 | QC-02 | out of combat, Settings -> General -> Master controls -> Preview as -> Solo: a small 'Ka0s Quick Comms - Preview' window appears above the settings with the dropdown on Solo and an End preview button; the pads show PREVIEW | pending |
| SM-QC-2 | QC-02 | pick Arena in the window's dropdown: the pads switch to the arena set and the settings row reads Arena; `/qc preview raid:heroic` moves the dropdown to the Raid Heroic entry | pending |
| SM-QC-3 | QC-02 | close the settings window with a preview on: the preview and the window stay; End preview in the window -> window gone, live pads, the settings row reads Off when reopened | pending |
| SM-QC-4 | QC-02 | with the preview on, the close mark ends it; with the preview on and the settings open, Escape first ends the preview and hides the window, a second Escape closes the settings | pending |
| SM-QC-5 | QC-02 | preview on, pull a mob: the window goes with one 'Preview ended: you entered combat.' line and the live buttons come back; Alt+Z with a preview on hides and restores the window without ending the preview | pending |
| SM-QC-6 | QC-02 | preview on, `/qc test`: window gone (test mode has no window); `/qc disable` with a preview on: window gone; open the dropdown menu then press Escape: menu and window both gone, nothing left floating | pending |
| SM-QC-7 | QC-02 | drag the window, end the preview, start it again: same place; /reload and start again: still the dragged place | pending |
| SM-QC-8 | QC-03 | `/qc preview` in the open world: chat 'Previewing: Current', the window opens on Current and the pads show PREVIEW; `/qc preview list` prints the menu and changes nothing; `/qc preview nope` points at `/qc preview list`; `/qc help` shows the new preview line | pending |
| SM-QC-8 | QC-05 | open Settings -> Groups (edit preview), then Preview as -> Dungeon: dial and pad icons look exactly as in live mode (no fading, no dark circle on the dial icons), only the PREVIEW labels added; buttons do not send | pending |
| SM-QC-9 | QC-06 | with the preview dial open, open New callout over it, then Choose icon...: the dial hub dot and pointer stay behind the dialog, the icon browser sits above the dialog, and the settings window sits below both | pending |
| SM-LK-1 | LK-91 | /bl sim start bank: every step label fits its row; a long one ends in an ellipsis before the /bl sim step column, never under it; hovering the row shows the full label; widening the panel shows more of the label | pending |
| SM-BL-14 | BL-11 | in a freshly started client, /bl sim start bank: every step, including step 4 (the flask deposit), follows the previous one about 1 s later with no multi-second stall | pending |
