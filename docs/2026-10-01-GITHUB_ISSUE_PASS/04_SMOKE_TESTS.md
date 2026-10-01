# In-client smoke tests

These are the owner's to run, on a Retail client with every Ka0s addon on its feature branch. Record each
result in the **Result** column (pass / fail plus a note). Nobody else marks a check passed. `99_REPORT.md`
may add checks for things execution changed beyond this plan.

Before you start: `/console scriptErrors 1`, and BugSack (or the default error frame) visible.

## S0. Load

| # | Check | Expected | Result |
|---|---|---|---|
| S0-1 | Log in with all eleven addons enabled | No Lua error; every addon prints its normal login line (or nothing) | pass (owner-reported, 2026-10-02) |
| S0-2 | `/reload` twice | Same; no "LibKa0s minor mismatch" or partial-vendor stub line | pass (owner-reported, 2026-10-02) |

## S1. Library surfaces every addon touches (LibKa0s v1.66.0)

| # | Check | Expected | Result |
|---|---|---|---|
| S1-1 | Any addon: `/<slash> set <bool path> maybe`, then a bad colour, then a value outside an allowed set | The usual refusal lines (ConsumableMaster: its own wording, see S5) | pass (owner-reported, 2026-10-02) |
| S1-2 | Drag-reorder a row in any ReorderList (KickCD spell list, ConsumableMaster pins, PanelMaster panel list) | Ghost, drop and save as before (ReorderList now lives in `WidgetsReorder.lua`) | pass (owner-reported, 2026-10-02) |
| S1-3 | Open every settings page that renders a grid (AbsorbTracker, AuraMaster, ConsumableMaster, KickCD Grid/General/Icons/Castbar, MultiMeters, PanelMaster, PrettyChat) | Layout unchanged; no blank gaps | pass (owner-reported, 2026-10-02) |
| S1-4 | In a perf-wired addon: `/<slash> perf` (usage), `perf start`, fight briefly, `perf finish` | Commands behave as before. A host with no declared budgets shows no budget line | pass (owner-reported, 2026-10-02) |

## S2. AbsorbTracker

| # | Check | Expected | Result |
|---|---|---|---|
| AT-1 | Appearance page for player, target and focus. Cycle every tab | Same tabs as before; no extra "Link" tab on target or focus | pass (owner-reported, 2026-10-02) |
| AT-2 | Focus with "Linked to Player" on | The hint **replaces** the rows on every tab | pass (owner-reported, 2026-10-02) |
| AT-3 | Click a tab, then toggle `/at set units.focus.mirror true/false` with the page open | The page re-renders the mirror state after the tab click (the refresher survives) | pass (owner-reported, 2026-10-02) |

## S3. BankLedger

| # | Check | Expected | Result |
|---|---|---|---|
| BL-1 | With a history containing `Item <id>` rows, log in and wait ~10 s, then open History | Those rows now show item names | pass (owner-reported, 2026-10-02) |
| BL-2 | Open Insights | The previously-unnamed items appear in the Type / Sub-type / Quality breakdowns | pass (owner-reported, 2026-10-02) |
| BL-3 | `/reload` again | No duplicate rows; nothing changes a second time | pass (owner-reported, 2026-10-02) |

## S4. KickCD

| # | Check | Expected | Result |
|---|---|---|---|
| KC-1 | Cast-bar unlock, drag, lock; `/reload` | Position saved; drag works (Castbar_Frame peel) | pass (owner-reported, 2026-10-02) |
| KC-2 | In combat, put 3–4 tracked spells on cooldown | Swipe animates smoothly with no restart. Countdown text ticks. Icon brightens in the final ~1.6 s | pass (owner-reported, 2026-10-02) |
| KC-3 | Turn **cooldown text off**, repeat KC-2 | Icon still brightens at the end of the cooldown (curves no longer depend on the text ticker) | pass (owner-reported, 2026-10-02) |
| KC-4 | `/kcd debug on` during a steady cooldown | No repeating `SPELL_STATE` line for an unchanged cooldown | pass (owner-reported, 2026-10-02) |
| KC-5 | Change glow type/colour mid-cooldown | Takes effect immediately | pass (owner-reported, 2026-10-02) |
| KC-6 | Spell-list editor: add, remove, reorder spells; switch class/spec | Rows look identical to before (28 px, no gaps); drag-reorder lands where dropped | pass (owner-reported, 2026-10-02) |
| KC-7 | Charges spell in combat | Charges badge stays live | pass (owner-reported, 2026-10-02) |

## S5. ConsumableMaster

| # | Check | Expected | Result |
|---|---|---|---|
| CM-1 | `/cm set <bool path> maybe`, a bad colour, a value outside an allowed set | ConsumableMaster's own (localized) refusal wording, not the library default | pass (owner-reported, 2026-10-02) |

## S6. LootHistory

| # | Check | Expected | Result |
|---|---|---|---|
| LH-1 | Open Insights; cycle every section and segment | Charts, bars, strips and lists render as before; tooltips work | pass (owner-reported, 2026-10-02) |

## S7. MultiMeters

| # | Check | Expected | Result |
|---|---|---|---|
| MM-1 | Hit a PvP Training Dummy, then `/mm diagnostics` | The classed dummy never appears as a grid column | pass (owner-reported, 2026-10-02) |
| MM-2 | Group with Valeera (companion) | Valeera is still admitted to the ally meters | pass (owner-reported, 2026-10-02) |

## S8. PanelMaster

| # | Check | Expected | Result |
|---|---|---|---|
| PM-1 | Panel editor → Position and size: **Frame level** slider under Frame strata. Move it with two overlapping panels | The panel's stacking changes; value clamps 0–100; `/pm` CLI agrees | pass (owner-reported, 2026-10-02) |
| PM-2 | Edit colour, size, border, art and anchor for a panel; drag it unlocked; Reset; Copy from; Fit to artwork | All behave as before. `/pm debug` shows `[Set] panel.<field> = ... on '<name>'` lines | pass (owner-reported, 2026-10-02) |
| PM-3 | Profile switch with panels present | Panels update; no error | pass (owner-reported, 2026-10-02) |
| PM-4 | Without SunnArt installed | No Sunn category or rows (S.Installed deleted) | pass (owner-reported, 2026-10-02) |

## S9. PartyFrameEnhanced (secure follow; #3 closes only on these)

| # | Check | Expected | Result |
|---|---|---|---|
| COMBAT-6 | Blizzard raid-style party frames: enter combat, have someone join | Their target and pet frames appear beside the right member **in combat**; no `ADDON_ACTION_BLOCKED` | pass (owner-reported, 2026-10-02) |
| COMBAT-9 | Same with someone leaving (re-sort) | Remaining frames follow their members in combat | pass (owner-reported, 2026-10-02) |
| COMBAT-10 | EllesmereUI party frames: join/leave mid-combat | Same as COMBAT-6/9, no taint (check `/console taintLog 1` output) | pass (owner-reported, 2026-10-02) |
| PF-4 | Stand the addon down (`/pfe` disable) and re-enable, out of combat | No error; frames behave; fade fallback still works for unwrapped providers | pass (owner-reported, 2026-10-02) |

## S10. WhatGroup

| # | Check | Expected | Result |
|---|---|---|---|
| WG-1 | Apply to a premade as Tank+Healer, get invited, accept | The popup shows the role (assigned role, with icon) | pass (owner-reported, 2026-10-02) |
| WG-2 | Chat notification with `notify.showRole` on and then off | Role line shown, then hidden | pass (owner-reported, 2026-10-02) |
