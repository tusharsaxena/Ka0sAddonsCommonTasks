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
