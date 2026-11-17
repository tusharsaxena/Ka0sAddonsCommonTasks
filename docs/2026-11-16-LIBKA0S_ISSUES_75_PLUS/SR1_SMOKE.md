# Smoke round 1: re-smoke sheet

What changed for `SR1_SMOKE_ROUND1.md`'s rulings. The owner runs these in game and records **PASS**, **FAIL**
(with a note) or **N/A**. The run never marks a check passed by itself. Run on **Retail and WoW Forever** wherever
the addon ships on both. The checks in `06_SMOKE_TESTS.md` that passed in round 1 are not repeated.

| Id | Where | Check | Retail | Forever |
|---|---|---|---|---|
| SR1-TIP | Any library window (debug console, copy window, perf panel, sim panel, skin picker) and any HUD drag strip | Hover each title-bar control: its tooltip opens **centered above** it, never under the pointer. Drag the window to the top of the screen: the tooltip flips below. | | |
| SR1-TIPS | Debug console (any addon), and every addon window below | **Every** title-bar control has a one-line tooltip: Debug toggle, Diagnostics, Copy, Clear, settings, close. | | |
| SR1-COL | Same windows, under Ka0s Default plus two other skins | At rest every control (the X and Diagnostics included) is the same icon color. On hover the glow stays **and** the control turns the skin's link color (orange in Ka0s Default); the X turns red. Debug ON/OFF keeps its green/red. | | |
| SR1-BAND | Drop Watcher History and Drops (full and compact layouts), Skill Master, Dps Race Results, Skin Tester ListRow | In every skin, a section header sits on a band you can tell apart from a plain row, a striped row and a hovered row. Drop Watcher's group headers now read like Skill Master's. | | |
| SR1-DW | Drop Watcher main window, Rolls panel | Minimize, layout, lock: tooltips above; gray at rest, link color on hover; X red on hover. Unlocked lock still looks dimmed. | | |
| SR1-SM | Skill Master main window, journal, trainer popup, block headers, detached and merged bands | Every mark has a tooltip above (the chevrons now say "Collapse this block" / "Expand this block"). **Block-header marks now rest gray, not gold** (ruling 4 reverses the round-2 gold rest). | | |
| SR1-CT | Combat Trail HUD, Race window (Retail), Results, Compare, Gear view, Ability timeline | Every title-bar control has a tooltip above; gray at rest, link color on hover, X red. | | |
| SR1-OR | Outfitter Reborn outfit window and outfit bar | The gear and the lock now hover in the link color (they hovered red before); the X still hovers red; tooltips above. | | |
| SR1-QC | Quick Comms preview window, callout popup, Comms Pad header | The X shows "Close" above; the Pad's -/+ shows "Collapse"/"Expand" above and hovers in the link color. | | |
| SR1-PGFE | PGF dialog, Dungeons panel | The collapse/expand chevron rests gray, hovers orange, tooltip above. | | |
| SR1-MM | Multi Meters, the seven header controls of a meter window | Tooltips above; lock and minimize tooltips change their words with the state; gray at rest, link color on hover, X red. | | |
| SR1-RV | Every addon | Loads with no Lua error; its windows open; test or sim mode works. Each other addon's own close X (Absorb Tracker, Aura Master preset picker, Bank Ledger, Loot History, Skin Tester showroom, What Group) shows "Close" above and hovers red. | | |

## Owner calls the pass surfaced

1. **HUD strips with a "beside" placement.** Aura Master (your #22 ruling), Absorb Tracker, Consumable Master and
   Kick CD place their drag strip's tooltip **beside** the strip through their own hook, so ruling 2 did not move
   them. Keep them beside, or move them above like every other attached tooltip?
2. **Skill Master's block-header marks** (chevron, detach, sort, filter) rested gold under round 2 / R8-3. Ruling
   4 makes them rest gray like every title-bar control. Confirm, or keep gold for block headers only.
3. **Footer buttons** (Widgets window footers) still light only faintly on hover. Ruling 4 covers title-bar
   controls only. Extend it to footer buttons?
4. **Skin Tester dropdowns** (round 1 item 1): unchanged. They are stock while Scope → Ignore settings panel is
   on, which is the default. Flip that default?

## Owner result (2026-11-17)

**Passed.** The owner reported "Smoke tests passed" for this sheet, apart from the feedback recorded in
`SR2_SMOKE_ROUND2.md`: the hover colors in Azeroth, Glass, WoW Midnight and WoW Forever, and window border
thickness. The four owner calls above were answered there as well. The owner did not report Retail and
Forever separately, so this records one result for the sheet.
