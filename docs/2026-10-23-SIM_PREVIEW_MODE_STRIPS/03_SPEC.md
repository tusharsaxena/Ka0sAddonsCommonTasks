# 03 — End state and lead decisions

## End state

1. **Sim auto-run (LibKa0s v1.76.0, SimTimeline 3 / SimPanel 5).** A simulation started from the verb layer
   (the picker's Start, typed `/<slash> sim start …`, typed or button Restart) plays by itself at the host's step
   delay once the session is ready. The "Run all" button and `RUN_ALL` string are gone. The controls are
   Pause/Resume, Restart and Stop. A manual step, typed or a click on a row, holds a playing run and then acts, so
   the run is left paused with Resume offered. `run` stays as a synonym of resume. The members `sim:Start` and
   `sim:Restart` stay literal, so scripted suites are unchanged. Hosts BankLedger, DropWatcher and LootHistory take
   the fallout (BL-01, DW-01, LH-01). Standard: WS-01.
2. **Mode strips (LibKa0s Widgets minor 14).** `W.TestStrip(parent, { kind = "sim", text, icon })` gives a cyan
   simulation flavor; `strip.kind` reads back the flavor; `TestStrip` without a kind is unchanged. No new member.
   - A window that shows a strip drops the matching header word: TEST MODE goes from the BankLedger, DropWatcher,
     LootHistory and MultiMeters windows, and SIMULATION from DropWatcher and LootHistory, which get a sim strip.
     BankLedger's SessionWindow moves to the sim flavor.
   - A layout where the strip cannot show, such as a minimized or compact window or Widgets being absent, keeps
     the word.
   - QuickComms, AuraMaster, WhatGroup and KickCD keep their words.
   - Items: LK-10, BL-10, DW-10, LH-10, MM-01, WS-05.
3. **QuickComms preview selector (QC-01..04).** A small skinned, draggable window with a situation dropdown,
   an End preview button and a close mark. It is shown exactly while "Preview as…" is on, whatever started it, and
   it follows `/qc preview <name>`.
   - A bare `/qc preview` opens the window on a live preview of the current situation, and `/qc preview list`
     prints the menu.
   - Plain Test mode has no window.
   - The window's position persists in the profile.
4. **`/mm sim` (MM-10..20, MultiMeters#60)** and **`/kcd sim` (KC-01..10, KickCD#38)** are Sim-1.0 hosts with
   their issue's scenario lists and a headless end-to-end suite per scenario. MultiMeters puts the sim strip on
   every window; KickCD puts one on top of each icon grid. Both close their issue on merge.
5. **Release re-look (WS-25/26, LK-25, DC-01).**
   - Standard v2.87.0, preview-mode: a new MUST, *Kept current at every release*. Each release's ANALYSIS.md
     records `## Preview and simulation data`: Current, Refreshed, Deferred or Not applicable.
   - LibKa0s releasing.md gets the matching step.
   - dev-copilot 2.5.0 WoW bump-version asks the question in Step 1b, before the gate, and lists the files it
     found.
6. Every roster addon re-vendors LibKa0s v1.76.0 and refreshes its standard reference to v2.87.0 (`<PFX>-RV`).

## Lead decisions (taken, not asked)

- **D-KC (party narration).** KickCD tracks only the player's own interrupts and CC against target and focus
  casts; it has no party tracking (README, verified). KickCD#38's "made-up party" and "party interrupts" therefore
  become narration: the party's kicks end enemy casts and print `[sim]` lines. Each #38 scenario maps to the engine
  path it stresses. No party tracking is added. OWNER B2's "party icon grid" is read as KickCD's icon grid(s).
- **D-MM-DELAY.** No `sim.stepDelay` settings row for MultiMeters (the design's MM-18 is dropped as outside
  OWNER_SCOPE). Both new hosts use a 1 s constant.
- **D-QC-POS.** The QC preview window's position persists in the profile (standalone-windows' persist MUST), rather
  than the session-only position the design proposed.
- **D-WORD.** "Remove the header word wherever the strip exists" keeps the word only where the strip cannot show:
  minimized, compact, or Widgets absent.
- **D-RUN.** Clicking a row while a run plays holds the run and then acts (design-autorun A5).
