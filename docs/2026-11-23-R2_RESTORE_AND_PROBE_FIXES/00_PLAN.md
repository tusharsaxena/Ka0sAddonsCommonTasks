# R-2 restores and Forever probe fixes (2026-11-23)

Branch `fix/2026-11-23-r2-restore-probe-fixes` in CombatTrail, RangeMaster, MultiMeters, ConsumableMaster,
BankLedger, LootHistory and this repo. Built in scratch clones and switched into the live checkouts only when
green, because the game loads each working tree. Committed, not pushed; merged only on the owner's go-ahead.

## Owner rulings (2026-11-23)

- **AuraMaster** (already merged, 7e713b9): the six colors stay off the skin, over U-8 and U-9.
- **A.** Restore the looks the R-2 defaults changed in Combat Trail, Range Master and Multi Meters, disable those
  migrations, repair migrated profiles and fix the pick-loss, preset and Consumable Master channel bugs.
  **Bank Ledger keeps its new stripe and hover** ("keep the BL stripes"), so its v7 stays.
- **B.** Fix the four findings of the Forever probe.

These supersede `docs/2026-11-20-LIBKA0S_94_97_99_100/SD_RULE.md` for U-1, U-2, U-8, U-9 and U-14, and R-2 for the
options each addon's *Documented deviations* names. A later sweep asks the owner about each by name.

## Items

| Id | Repo | What |
|---|---|---|
| R2P-CT | CombatTrail | Own defaults, step removed, v4 restore |
| R2P-RM | RangeMaster | Own defaults, step removed, step 3 restore, frameless preset fixed |
| R2P-MM | MultiMeters | Own defaults, v28 retired, v29 restore |
| R2P-CM | ConsumableMaster | Border swatch default back to 0.25 gray (U-16's black edge stands) |
| R2P-BL | BankLedger | Forever sim base tab 48 slots |
| R2P-LH | LootHistory | Late loot lines, claims across combat, sim sender |
| R2P-CT-REC | this repo | This bundle |

Out of scope: the R-1 fixes of hard-coded looks (Insights bar textures, lane icon text, the pet paw tint, spell chip
colors, Multi Meters' classless cell neutral) stay as built. Wrong rows already in Loot History are not rewritten.
