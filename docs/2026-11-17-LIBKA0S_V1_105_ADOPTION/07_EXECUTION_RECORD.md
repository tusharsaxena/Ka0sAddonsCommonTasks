# Execution record

## Wave A (2026-11-17)

- **Build:** one agent per addon (13), each with an independent review. Two reviews asked for changes, both fixed:
  - **Aura Master:** the first pass stopped AD-88-AM as a library blocker and drafted a root-only design. The fix
    round built it: only the top container of each chain carries a strip, and a block whose edges read secret shows
    none. Its preset-picker footer was shortened to fit W.Footer's single line.
  - **Multi Meters:** the session line kept its "Test" word while the strip showed.
- **Follow-ups:** the 11 approved reviews still had minor findings. One round fixed them in 9 addons.
  - **Kick CD:** a label above an anchored cast bar could sit under the strip.
  - **Combat Trail:** the Race window showed its sample race with no strip. This gap predates the run.
  - **Skill Master:** the Journal's Alts hint line is now a footer, and the title-band bottom is no longer a copied
    number.
  - **Bank Ledger, Combat Trail, Dps Race and Outfitter Reborn:** tests for the footer used when the library is
    missing.
  - **Stale docs:** wording about where the strip sits.
- **Deviations from the brief, accepted:** Combat Trail's and Dps Race's HUDs dock with `dock = "title"`, not
  `"hud"`. Preview-mode counts a HUD with a title bar as a window.
- **Exceptions:**
  - AD-88-ST: ruling 3.
  - AD-89-MM: the meter window draws no footer.
- **Library finding:** LibKa0s#95. The dock code does arithmetic on geometry that can read secret. Aura Master guards
  its own side. The fix belongs in a later LibKa0s release.
- **Checkpoint CP-A:** the lead re-gated all 13 addons under each client they ship. All had 0 failed, luacheck 0/0,
  no vendored file changed, and no .lua file over 1500 lines (largest DpsRace `modules/Hud_States.lua` 1486).
  The run branches are pushed. The smoke sheet is `A_SMOKE.md`.

## Owner rulings for wave C (2026-11-17)

- **Aura Master `tooltipAnchor`, option B.** The aura buttons' tooltips are placed by the client
  (`SetTooltipAnchorPoint`), so standalone-windows *What it does not bind* (v2.112.1) puts them out of scope. The
  owner still wants "At the cursor" gone. The setting keeps its six edge and corner choices and drops
  `ANCHOR_CURSOR`. A saved `ANCHOR_CURSOR` migrates to the default, `ANCHOR_BOTTOMLEFT`.
- **Multi Meters `window.tooltip.anchor`, option A.** A meter row is a body element, so its tooltip opens beside
  the window group.
  - The choices become **"Beside the window"** (the default: right, flipping left when there is no room) and
    **"Beside, prefer left"**.
  - Every saved value migrates to the default.
  - The offset X/Y settings stay as a nudge.

## Wave B (2026-11-17)

- **Build:** one agent per addon (19), each with an independent review. Every review finding was fixed in the same
  run: 16 addons have commits, and two reviews asked for changes (Absorb Tracker docs, Multi Meters).
- **Not applicable:** Panel Master, Party Frame Enhanced and Pretty Chat own no titled window and no drag strip.
- **Library finding:** LibKa0s#96. `DragHandle:ApplyLevel` does not re-level the new settings mark. The smoke check
  BAR-23 (Absorb Tracker) watches for it.
- **Checkpoint CP-B:** the lead re-gated all 16 addons under each client they ship. All had 0 failed, luacheck 0/0,
  no vendored file changed, and no .lua file over 1500 lines (largest DpsRace 1486). The branches are pushed. The
  smoke sheet is `B_SMOKE.md`.

## Wave C (2026-11-17 to 2026-11-18)

- **Outage:** at about 23:00 on 2026-11-17 the WSL D: mount went to "Input/output error" mid-run, and every agent
  stopped. Absorb Tracker and PGF Extension were committed; nine addons held half-done, uncommitted edits. When D:
  came back, every touched repo passed `git fsck`. The first run's agent results were lost with its temp folder.
- **Resume:** `plan-data/wave-c-resume-workflow.js` is a copy of `wave-c-workflow.js` (left unchanged) that tells
  each agent to read and continue the half-done tree, never discard it. Run `wf_5328a36b-96e`: 46 agents, no
  errors. 16 addons built, 13 reviews with findings, every finding fixed (four reviews asked for changes: Aura
  Master, Combat Trail, Multi Meters, Outfitter Reborn).
- **Not applicable:** Pretty Chat. Its only own tooltip is on the Settings canvas (`exceptions.tsv`).
- **Owner rulings built:** Aura Master option B (cursor choice dropped, migrated to Bottom left); Multi Meters
  option A ("Beside the window" default, "Beside, prefer left"; every saved value migrated).
- **Owner calls raised** (current behavior kept until ruled; listed in `C_SMOKE.md`): Outfitter Reborn TP4 (does
  the character sheet count as part of the window group), Skill Master SM-TIP-7 (block-header marks keep the
  above-the-mark tooltip by smoke round 1 ruling 3), Dps Race HUD (beside rather than the attach fallback, DR-03).
- **Notes from agents:** Loot History's leak gate has almost no headroom (about 255.8 of 256 MB), with library-side
  retention through Skin owner listeners; Multi Meters places beside without a size inside the addon, and a size
  override in LibKa0s-Tooltip-1.0 could be a later follow-up. Neither is filed yet.
- **Checkpoint CP-C:** the lead re-gated all 17 addons under each client they ship: 0 failed everywhere, luacheck
  0/0, no vendored file changed, no .lua file over 1500 lines in a touched addon (largest Dps Race 1489; Pretty
  Chat's generated GlobalStrings.lua predates the run and was not touched). The 16 branches are pushed. The smoke
  sheet is `C_SMOKE.md`.

## Wave D (2026-11-18)

- **Manifest:** 65 items (`0b8ec65`): #79, #87 and #82 in all 19 addons, AD-80-SM, AD-81-SM, AD-81-STD, AD-85-DR/DW/QC/SM
  and the checkpoint. Run `wf_d6ff4ee7-f70` (`plan-data/wave-d-workflow.js`): 56 agents, no errors, no library
  blocker. 18 addons had commits and were reviewed; six reviews asked for changes (Combat Trail, Dps Race, Drop
  Watcher, Multi Meters, Outfitter Reborn, Party Frame Enhanced), and every finding was fixed or answered.
- **Built:** report verbs onto `D:Report` in 17 addons (none in PGF Extension or What Group); shared sample
  characters in 12 (BL, CT, DR, DW, KC, LH, MM, OR, PFE, QC, SM, WG); row floors in Drop Watcher (expanded-row wash) and
  Multi Meters (stripe .08, hover .15); Skill Master on `W.Bar` with a Journal launcher entry; Dps Race's countdown on
  LibKa0s-Callout-1.0 (`modules/Countdown.lua` deleted).
- **Standard:** v2.113.1 on the run branch (`b537b06`): Skill Master's launcher column lists Journal. Renumber before
  finalize if origin/master has moved.
- **Not applicable:** 29 rows in `exceptions.tsv`, each with the agent's proof command. The #85 decisions (Dps Race
  adopted; Drop Watcher and Quick Comms not now; Skill Master never) are recorded on LibKa0s#85.
- **Owner calls:** 14, listed in `D_SMOKE.md` (report routing edges, sample-character choices, real names in docs,
  the Multi Meters and Drop Watcher row tints, the Dps Race countdown's look).
- **Checkpoint CP-D:** the lead re-gated all 19 addons under each client they ship: 30 runs with 0 failed, luacheck
  0/0, no vendored file changed, no authored .lua over 1500 lines (largest Dps Race 1489). The 19 run branches and the
  standard's are pushed (three new on GitHub: Panel Master, Party Frame Enhanced, Pretty Chat). The smoke sheet is
  `D_SMOKE.md`.
