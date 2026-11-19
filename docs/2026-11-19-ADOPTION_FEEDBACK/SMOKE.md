# In-game smoke for the adoption feedback run (CP-1)

Run these in the client, Retail and then WoW Forever where the addon ships both. Each check's full
steps and its `Result:` field are in that addon's `docs/smoke-tests.md` on the run branch
`feat/2026-11-19-adoption-feedback`. Fill the Result there, or tell the lead and the lead records
it. Nothing here is marked passed until the owner says so.

Every addon now vendors LibKa0s v1.107.0, re-cut on 2026-11-19 with the fix for LibKa0s#95.

## Everywhere: the drag strip (LibKa0s v1.107.0, `AF-LK-01`, `AF-LK-02`)

Unlock any HUD display with a drag strip. That means Absorb Tracker's bar, Aura Master's
containers, Consumable Master's Macro Bar, Kick CD's cast bar and grids, Quick Comms' pads and Range
Master's anchors.

- The marks read **[?] [gear] [X]**, left to right, closer together than before.
- At rest the marks are the header grey. On hover, the ? and the gear turn the header's link color
  and the X turns red, matching the Drop Watcher window's title marks.
- The gear opens that display's settings. The X hides or disables that display, and its own enable
  toggle brings it back as it was.
- Every strip tooltip opens centered above the strip, and below it only at the top of the screen.

## The secret-geometry fix (LibKa0s#95)

- **AM repro.** In Aura Master, create a new profile. The preset picker opens. Close it without
  picking a preset. Expect no Lua error. Before the fix it raised "attempt to perform arithmetic on
  a secret number value" in `Widgets.lua:647`.

## Per addon

| Addon | Checks | What they cover |
|---|---|---|
| Absorb Tracker | BAR-23 (superseded), BAR-24, BAR-25, BAR-26 | The bar's strip marks, its gear and X, and the tooltip above |
| Aura Master | DRAG-20, CONT-30, CONT-31 (CONT-9, CONT-13, CONT-29, DRAG-11 and DRAG-19 are superseded) | Container strip marks and tooltip above. Aura tooltips stay where the client puts them. A strip whose position reads secret may show no tooltip (LibKa0s#99) |
| Bank Ledger | STATE-10, STATE-11 | The ledger window's header lock mark, `/bl lock` and `/bl unlock` |
| Combat Trail | SM-CT-H19, SM-CT-T16, SM-CT-R30, SM-CT-RM97, SM-CT-RM98 | Every bar takes the skin's statusbar texture (look for a gloss seam under Obsidian on the pace bar). The race call-out strip has no X yet (LibKa0s#100, a recorded deviation) |
| Consumable Master | BAR-10, BAR-40, BAR-43, BAR-44 | The Macro Bar strip's marks, gear and X |
| Drop Watcher | ROLLS-20, ROLLS-21 | Tooltips sit flush to the main window, and beside the Rolls companion only when flush would cover it. The roll companion has a small "Drop Watcher" header with no controls |
| Kick CD | CAST-20, CAST-21, GRID-23, GRID-25 | The cast bar's and grids' strips. The Target bar's X also hides a linked Focus bar |
| Loot History | HIST-50, HIST-51, ICON-7, SLASH-11 | The history browser's header lock mark, `/lh lock` and `/lh unlock` |
| Quick Comms | PAD-18 to PAD-24 | Each pad's strip and header row carry lock, settings and close. Close hides that pad, per profile (a pad closed in one profile stays shown in another), and `/qc show` brings it back. In test mode the X says the pad hides when test mode ends |
| Range Master | ANCHOR-9 | The anchor strip's marks, gear and X |
| Skill Master (Forever) | SM-WIN-6 to SM-WIN-10, SM-DISP-64, SM-DISP-65 | The main window resize grip appears only while unlocked, snaps to the step grid and is capped by Master scale. The LDB tooltip never resizes. Set waypoint places a TomTom waypoint when TomTom is loaded, and leaves an earlier native pin alone |
| Skin Tester | SHOW-56 | The showroom strip specimen shows the three marks |
| WhatGroup | POPUP-14, SKIN-38, SLASH-13 | The popup's header lock mark and `/wg lock`. The bottom Close stays (a recorded deviation) |
| PrettyChat | RV-107 | The re-vendor loads clean |

Multi Meters, Outfitter Reborn, Panel Master, Party Frame Enhanced and PGF Extension only
re-vendored (and recorded a waiver row where ruled). They have no new checks: a clean load with no
Lua error is the check.
