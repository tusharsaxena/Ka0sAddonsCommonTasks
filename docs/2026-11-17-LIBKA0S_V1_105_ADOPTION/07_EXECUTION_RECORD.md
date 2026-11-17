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
