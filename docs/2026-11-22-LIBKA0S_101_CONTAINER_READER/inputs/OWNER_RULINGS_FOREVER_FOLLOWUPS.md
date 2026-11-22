# Owner rulings on the Forever port's open questions (2026-11-22)

These are the four "Owner rulings wanted" items of `../../2026-11-22-LOOTHISTORY_BANKLEDGER_FOREVER_PORT/07_EXECUTION_RECORD.md`.
They are built on this run's branch after the LibKa0s#101 items, as `K101-FU-*`.

| # | Question | Ruling | Item |
|---|---|---|---|
| F1 | The loss reason for a disenchanted item on Forever (it reads OTHER today) | **Keep a "Disenchant" reason on Forever, for Disenchant 13262 only.** Milling, Prospecting and the Retail deconstruct spells stay absent (R2). | K101-FU-01 (LootHistory) |
| F2 | A hover for truncated History Character cells and the character dropdown | **A full-name tooltip whenever a name is cut off, on both clients.** Cells that are not cut off show nothing. | K101-FU-02 (LootHistory) |
| F3 | BankLedger's in-combat probe writes and performance-§12 | **Exempt as debug-only.** They run only while `/bl debug probe` is on, capped at 200 entries. Record it as an accepted exemption in BankLedger's performance docs. | K101-FU-03 (BankLedger) |
| F4 | Hide an empty Forever "Account" holder in Holdings and the Timeline | **Always show it** (no change). | none |
