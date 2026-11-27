# Execution record: owner feedback round 7 (2026-11-27)

Small items sent one by one after the round 6 hand-off, each built, gated on both clients where the
addon ships both, merged `--no-ff` and pushed on the owner's standing go-ahead ("merge as soon as all
change is ready"). Branches and scratch clones deleted. No tags, no version bumps.

| Repo | Merge | Items |
|---|---|---|
| DropWatcher | 7c36f40 | R7-DW-01 a smooth corner drag (a drag moves the columns and the verdict panel only; mouse-up paints in full), R7-DW-02 a tooltip on every verdict panel line (`modules/ItemSearchVerdictTips.lua`), R7-DW-03 "Why this word" renamed "Why this verdict", R7-REV (a doubled % in one tooltip; a hidden window clears its drag flag) |
| SkillMaster | e7575a0 | R7-SM-01 `docs/message-bus.md` split out of ARCHITECTURE (13 messages) |
| SkillMaster | 5939447 | R7-SM-02 the Professions broker is "Skill Master Professions" (a display's old "Skill Master" cell must be re-added) |
| CombatTrail | d784083 | R7-CT-01 the idle HUD hides the empty Damage profile chart, its slot kept; R7-CT-02 the footer reads "live" without the rate |
| OutfitterReborn | 6d98b43 | FLY-TAINT-01 the owner's Retail `ADDON_ACTION_BLOCKED` on `PickupInventoryItem()`: the flyout's getItemsFunc/postGetItemsFunc post-hooks wrote Blizzard's lists, so every flyout button's `location` was addon-written; now the `EquipmentFlyout_UpdateItems` post-hook arranges the buttons instead (order per page, worn items hidden) |
| LootHistory | b6c3bf8 | LH-FISH-01 a Fishing source from `IsFishingLoot()`; LH-SWAP-01 a bags-to-equipped swap writes no Transfer row; the Forever run's leak budget 320 MB until LootHistory#40 |

## Owner answers recorded

- Drop Watcher's "(needs over 10%)" wording: **approved**.
- The two stale October branches (DW `feature/upgrade-glow`, KC `feature/glow-options`): deleted on the
  owner's approval.

## Issues filed

DropWatcher#19 (split Item Search into its own addon), LootHistory#38 (loot toasts like RPGLootFeed),
LootHistory#39 (farm mode), LootHistory#40 (the shared test instance's heap at the leak gate).

## Combat Trail aura diagnostic, second paste (Forever, build 71139)

`aura events player=2 sealedFull=2`, `walks complete=3 incomplete=4 raised=6`, `gains seen=0`: UNIT_AURA
barely fires in combat and both events had `isFullUpdate` sealed; every in-combat walk raised once (the
round 5 one-raise-per-walk tally). Confirms the round 5 reading: no readable in-combat aura source on
Forever. Nothing further to build.

## Smoke

New rows, none marked passed: DW ITEM-SEARCH-76..78, SM SM-R7-1, CT R7-CT-SM1 and R7-CT-SM2, OR
FLY-TAINT-1, LH CAP-39 and LEDGER-SWAP-1.
