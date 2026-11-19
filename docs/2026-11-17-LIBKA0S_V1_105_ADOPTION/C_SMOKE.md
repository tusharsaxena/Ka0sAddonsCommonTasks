# Wave C smoke sheet (#92 tooltip placement)

The owner runs these in game and records **PASS**, **FAIL** (with a note) or **N/A**. The run never marks a check
passed by itself. Each id is written out in full in that addon's `docs/smoke-tests.md`. Run each check on Retail,
and on WoW Forever too where the addon ships there (**R·F**). Skill Master ships on Forever only.

**What to look for everywhere:**
- **Body tooltips** (rows, cards, chart marks, icons, list entries): the tooltip opens **beside the window group**,
  2 px off its right edge, top level with the hovered element. At the screen's right edge it opens on the left. It
  never covers the window or a docked companion panel.
- **Chrome tooltips** (title-bar marks, drag strips, tabs, filter-bar controls, footer buttons): centered 2 px
  **above** the control, flipping below it near the screen's top.
- **Never at the pointer:** no tooltip follows the cursor or sits at a corner offset.
- **Late growth:** a tooltip that grows when item or spell data arrives is placed again and stays on screen.
- **Out of scope (unchanged):** Settings-page tooltips, Blizzard frames, client-placed aura tooltips and LDB
  displays. Each addon's `docs/ARCHITECTURE.md` lists the ones it left alone.

| Addon | Checks | What changed | Result |
|---|---|---|---|
| Absorb Tracker (R·F) | BAR-17, BAR-12, BAR-13, BAR-23, SKIN-10 | Drag-strip and mark tooltips now open **above** the strip (chrome), no longer beside it. BAR-17's earlier pass is withdrawn | |
| Aura Master (R·F) | DRAG-19, DRAG-11, LAYOUT-39 | Drag strip tooltip stays beside the strip (SR2 ruling), now through the library; the cursor fallback is gone; "At the cursor" is dropped from the tooltip-anchor choices and a saved cursor choice becomes Bottom left (option B) | |
| Bank Ledger | LEDG-68, LEDG-69, INS-20, SESS-18 | Ledger, Insights and session tooltips beside the window; buttons and the test strip above | |
| Combat Trail (R·F) | SM-CT-H3, SM-CT-H18, SM-CT-N20, SM-CT-R28, SM-CT-R29, SM-CT-T15, SM-CT-RM96 | HUD lanes, Results, Timeline and Race tooltips beside their windows; chart hovers no longer at the cursor | |
| Consumable Master (R·F) | BAR-41, BAR-42, BAR-9, BAR-10, BAR-40 | Macro bar and flyout entry tooltips beside the bar or flyout | |
| Dps Race | SM-DR-AD92RUN, SM-DR-AD92DET, SM-DR-AD92CMP, SM-DR-AD92TL, SM-DR-AD92GV, SM-DR-AD92INS, SM-DR-AD92HUD, SM-DR-UT75, SM-DR-SF9 | Every window's body tooltips beside it; board tabs above; HUD spell rows beside the HUD (a recorded deviation, see the execution record) | |
| Drop Watcher (R·F) | FEED-109, FEED-110, FEED-111 (FEED-26, FEED-27, FEED-29, COMPACT-7 superseded) | Content beside the window group, chrome above, Insights marks beside the window | PASS (owner, 2026-11-19) |
| Kick CD | GRID-24, GRID-17, GRID-23, CAST-10, CAST-15, CAST-20, LAYER-9 | Icon grid tooltips beside the grid, including late growth | |
| Skin Tester (R·F) | SHOW-55 | The Overlays sample tooltip opens beside the showroom | |
| Loot History | HIST-49, TL-19, LED-14, INS-18, TL-15 | History, Timeline, Ledger and Insights tooltips beside the browser; late growth | |
| Multi Meters | TIP-23, TIP-29, TIP-38, TIP-39, TIP-40, TIP-41, PANEL-41 | Tooltip anchor becomes "Beside the window" (default) or "Beside, prefer left"; old saved anchors migrate to the default; X/Y offsets stay as a nudge (option A) | |
| Outfitter Reborn (R·F) | TP1, TP2, TP3, TP4, TP5, TP6, TP7 | Outfit window and outfit bar tooltips beside their group; Shift-compare further out; TP4 needs an owner call (below) | |
| PGF Extension | APPLY-27, APPLY-19 | The panel's tooltips beside the panel | |
| Quick Comms (R·F) | TIP-1, TIP-2, TIP-3, TIP-4, TIP-5, TIP-6, DIAL-21 | Dial and pad tooltips clear of the ring, title and page arrows; corner anchors removed | |
| Skill Master (F) | SM-TIP-1 … SM-TIP-7, SM-DISP-4, SM-DISP-30, SM-DISP-37, SM-DISP-44 | Main, detached, Journal, trainer popup and waypoint arrow tooltips beside their windows; header marks still above | |
| What Group | TELE-9, TELE-1, TELE-3, POPUP-13 | The teleport spell tooltip opens beside the popup | |

Pretty Chat: not applicable. Its only tooltip is on its Settings page (`plan-data/exceptions.tsv`).

**Owner calls raised in wave C** (the build keeps the current behavior until you rule):
1. **Outfitter Reborn TP4:** the window group is the outfit window alone. Docked right of the character sheet with
   no room on its right, a row's tooltip opens on the left, over Blizzard's sheet. Should the sheet count as part of
   the group?
2. **Skill Master SM-TIP-7:** the main window's block-header marks sit in the body, which the standard would class
   as body elements, but they keep the above-the-mark tooltip by smoke round 1 ruling 3.
3. **Dps Race HUD:** a body tooltip with a window stays beside it (DR-03, 2026-10-30) rather than the standard's
   attach fallback, which would cover the HUD's other rows. Recorded as a deviation in its ARCHITECTURE.md.
