# Smoke tests: the owner's seventh smoke round (2026-11-04)

**Fully exit and restart the client before you start. A `/reload` is not enough.** PremadeGroupsFilterExtension gains
a new texture file (the picker's eye, `libs/LibKa0s/media/icons/eye.tga`), and the client only finds a new file on a
full restart. LibKa0s code did not change this round (R7-L1 is docs and tests only), so every addon still carries
v1.85.0 at 550ef68 and nothing was re-vendored. Turn Lua errors on with `/console scriptErrors 1`. Any Lua error or
taint warning fails the check.

Nothing here has passed. Every Result is blank for you to fill in. An ID in brackets is the check in that addon's
`docs/smoke-tests.md`, where the full steps are. The README changes in all 16 addons have no in-game step, so they are
listed in `99_REPORT.md` instead of here.

## 1. PremadeGroupsFilterExtension: `/pgfe test` and the picker's preview

Out of combat. Start with the Group Finder closed and test mode off.

| # | Do | Pass when | Result |
|---|---|---|---|
| PG-1 | `/pgfe test` (PG TEST-1) | One chat line says test mode is on. The filter panel shows on its own in the middle of the screen with its plain title and your current filters (R7-PG2 dropped the *(test mode)* suffix). | |
| PG-2 | Hover **Apply** and **Clear** (PG TEST-1) | Both are grayed out, and the tooltip says PGF's window is not showing its Dungeons filters. | |
| PG-3 | `/pgfe test` again, then `/pgfe test on`, `on`, `off` (PG TEST-1) | The first turns it off and the panel goes. Then: on, still on, off. A `/reload` with it on comes back off. | |
| PG-4 | `/pgfe test`, then open the Group Finder on Dungeons; close it (PG TEST-2) | The panel docks under PGF's dialog and Apply works. When you close the Group Finder, the panel is back alone in the middle with Apply grayed. | |
| PG-5 | Settings, General, *Master controls*: tick and untick **Test mode**; right-click the minimap button (PG TEST-3) | The box shows and hides the panel. The launcher has a **Test mode** entry that agrees with the box and toggles it. The tooltip reads `Test mode: On/Off`. | |
| PG-6 | With test mode on, pull a target dummy (PG TEST-4) | "Test mode ended: combat started." The panel goes and the box reads off. `/pgfe test` in combat is refused. | |
| PG-7 | Test mode off, the Group Finder closed: `/pgfe skin` (PG SKIN-53) | The picker shows in front with a lit eye. The panel shows alone, in test mode, behind it. Hovering or selecting a skin previews it on the panel. | |
| PG-8 | Click the eye twice (PG SKIN-54) | The first click turns test mode off, the panel goes and the eye dims. The second brings them back. | |
| PG-9 | Close the picker with **Apply**, then reopen and close with the **X**, then reopen and close with **Escape** (PG SKIN-52) | After every close the panel is gone and test mode is off. Apply keeps the pick. The X and Escape put the stored skin back. | |
| PG-10 | Open the Group Finder on Dungeons, then `/pgfe skin`, then close the picker (PG SKIN-53) | Nothing opens or moves: the panel is already docked, the eye is dimmed and test mode stays off. After the close, PGF's dialog and the panel are still open. | |
| PG-11 | `/pgfe test` first, then `/pgfe skin`, then close the picker (PG SKIN-54) | The eye is lit and nothing else moves. After the close the panel stays up in test mode until you turn it off. | |
| PG-12 | Group Finder closed: `/pgfe test`; collapse and expand it with the arrow; then open the Group Finder on Dungeons (PG TEST-5, R7-PG2) | Alone, the panel looks like the docked one (your screenshot 74): the same width and scale, the skin's header band, a centred title clear of the arrow, and no row overlapping another. Collapsed, it is the same title strip as docked. Docked again, nothing moves. | |

## 2. The Sim mode box (seven addons)

Your rule is that the box is ticked while the sim window is open or a sim is running, or both, and unticked when
neither is true. Each block runs the same five steps with the addon's slash command and scenario. Before each block,
open Settings, General, *Master controls*, and leave it open. Be out of combat with no sim running and the sim window
closed. The box starts unticked.

1. **Tick.** Tick *Sim mode*. The sim window opens idle, the way a bare `/xx sim` opens it, and the box stays ticked.
2. **X.** Close the sim window with its close button. The box unticks at once.
3. **Run, then close.** Open the window, start the scenario, then close the window while it plays. The box stays ticked
   while the run goes on and unticks when the run ends (or at `/xx sim stop`).
4. **Untick while running.** Open the window, start the scenario again, then untick the box. The sim stops, the window
   hides and the box is unticked.
5. **Launcher.** Repeat steps 1 to 4 and check the minimap button's right-click *Sim mode* entry each time. It must
   agree with the box. With the window open and idle, clicking the entry closes the window. With a run playing,
   clicking it stops the run and closes the window.

| Addon | Slash, scenario, window | Full steps | 1 Tick | 2 X | 3 Run, close | 4 Untick running | 5 Launcher |
|---|---|---|---|---|---|---|---|
| AbsorbTracker | `/at sim`, `fight`, the *Absorb Tracker - Simulation* step window | AT SIM-2, SIM-3 | Pass (owner) | Pass (owner) | Pass (owner) | Pass (owner) | Pass (owner) |
| BankLedger | `/bl sim`, `bank`, the step panel | BL SIM-15, SIM-16 | Pass (owner) | Pass (owner) | Pass (owner) | Pass (owner) | Pass (owner) |
| DpsRace | `/dr sim`, `newbest`, the *DPS Race - Simulation* window | DR SM-DR-R5DR2, SM-DR-R6SIM, SM-DR-R7SIM | Pass (owner) | Pass (owner) | Pass (owner) | Pass (owner) | Pass (owner) |
| DropWatcher | `/dw sim`, `key`, the Simulation panel | DW SIM-19, SIM-20 | Pass (owner) | Pass (owner) | Pass (owner) | Pass (owner) | Pass (owner) |
| KickCD | `/kcd sim`, `pull`, the step panel (`/kcd sim panel` also hides it) | KC SIM-17, SIM-18 | Pass (owner) | Pass (owner) | Pass (owner) | Pass (owner) | Pass (owner) |
| LootHistory | `/lh sim`, `loot`, the sim panel | LH SIM-13, SIM-14 | Pass (owner) | Pass (owner) | Pass (owner) | Pass (owner) | Pass (owner) |
| MultiMeters | `/mm sim`, `dungeon`, the step panel | MM SIM-16 | Pass (owner) | Pass (owner) | Pass (owner) | Pass (owner) | Pass (owner) |

Also check in every block that **Escape** on the open, idle window unticks the box, the same as the X does.
In combat the box stays unticked and no sim starts. After a `/reload` the box is unticked.
