# Execution record

The workflow was `wf_9a4a5110-967` (12 agents, 0 errors). Builders worked in `~/ka0s-scratch/itemsearch/<Repo>`, and the lead
brought the branches into the live repos.

## What was built
- **LibKa0s v1.115.0** (tag local only, `f8c2ea68`). `LibKa0s-ForeverDB-1.0` minor 2 adds SearchItems, QuestsForItem,
  RewardFrom, StartsQuest and SkinnedFrom, with kit revision 63. The API doc is now version 2.
- **Drop Watcher (DropWatcher#17).** Item Search, on WoW Forever only:
  - the block on every item tooltip (a TooltipDataProcessor post call, no block until ForeverDB has loaded);
  - the Item Search window, opened from the header magnifier, `/dw search` or Ctrl-Alt-D (never steals a bound key);
  - the delayed out-of-combat ForeverDB load;
  - quests, crafting (a recipe-reagent table generated from wowf DB2, plus a profession-window learner) and the other
    facts;
  - the settings page;
  - the old detail-card Sources chip retired, with schema step 15.
- **Loot History.** Item sources (SF-LH-02) and its runtime use of ForeverDB are removed, with schema v16.
- **Bank Ledger.** The ForeverDB vendor buy price (SF-BL-01) and its saved setting are removed.

## Lead gate (2026-11-25, branch heads)

| Repo | Retail | Forever | luacheck | seeds |
|---|---|---|---|---|
| LibKa0s | 5236/0 | 5236/0 | 0/0 | 18 |
| LootHistory | 2179/0 | 2158/0 | 0/0 | 17 |
| BankLedger | 1870/0 | 1849/0 | 0/0 | – |
| DropWatcher | 2773/0 | 2724/0 | 0/0 | 32 |

The addons' merge results were re-gated after the doc conflict resolution, with the same totals.

## Merged (2026-11-25, owner: "merge item search to master so i can test it")

| Repo | Merge |
|---|---|
| LibKa0s | d0d31457 |
| LootHistory | 7c98851 |
| BankLedger | 866c7f6 |
| DropWatcher | ca53d2e |

**Conflicts.** There was one in each addon's `docs/smoke-tests.md`, against that day's smoke-record commits:
- **Loot History:** SEEDS-LH-1 to SEEDS-LH-3 keep their PASS and gain the superseded note.
- **Bank Ledger:** FOREVER-20 to FOREVER-23 were retired with the feature, and the sign-off records that they passed.
- **Drop Watcher:** both "owed" paragraphs are kept.

**Branches** are deleted, local and origin.

## Still owed
- **The owner's smoke:** Drop Watcher ITEM-SEARCH-1 to ITEM-SEARCH-18; Loot History SEEDS-LH-4; a Bank Ledger check that
  the price is gone. Each repo's `docs/smoke-tests.md` lists them.
- **The LibKa0s v1.115.0 tag push**, on the owner's go-ahead. Closing DropWatcher#17 after smoke.
- **Loot History's Forever leak gate** passes with under 1 MB of headroom (the deviation was retired).
- **Probes, assumed until done:** the tooltip hook, `C_Map.SetUserWaypoint` and `tip:GetItem()` on WoW Forever.
