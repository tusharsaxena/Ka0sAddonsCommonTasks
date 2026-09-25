# Owner rulings

Answers to `04_OPEN_QUESTIONS.md`, recorded 2026-09-26. Where a ruling differs from the recommendation,
the spec and the manifest are amended to match (commit `DR-OW-01`).

## DR-OW-01

| Q | Ruling |
|---|---|
| Q1 (DR-OW-03) | **ConsumableMaster:** X turns the macro bar off (`macroBar.enabled = false`). **AbsorbTracker:** X turns off that unit's bar (`units.<unit>.enabled = false`) on **every** bar, the player bar included, so there is no player-bar exception. **KickCD: no X at all**, so KickCD does not adopt the close option. |
| Q3 | AuraMaster moves onto the shared helper in this pass, as recommended (a). |
| Q11 | **No privacy rules.** The report never goes to GitHub: users send it to the owner privately when they report a problem. Nothing is redacted and there is no BankLedger README note. Print whatever a maintainer needs. |
| README wording | **No destination is named.** Step 3 reads: "If the debug window isn't open, open it with `/<slash> debug`. Press **Copy**, copy the entire output, and include it with your bug report." There is no GitHub link in the section. The closing note is unchanged: "The report is added after the debug trace in the same window, so one copy carries both." AuraMaster's README, which today says "paste it into a GitHub issue" with a link, is corrected to match in DR-AM. |
| Q18 / Q21 | Push the feature branches at checkpoints. **Ask the owner before** merging WowAddonStandards or wow-addon to master (DR-OW-07). Nothing else is merged or tagged without the owner. |
| Q2, Q4-Q10, Q12-Q17, Q19, Q20 | **Accept every recommendation as written.** The buffer is 5000 if the DR-OW-02 measurement passes and 3000 otherwise. The measurement remains an owner gate. |

## DR-OW-02 (the buffer measurement)

Pending: the owner runs the bench (`03_EXECUTION_PLAN.md` §5, option A, as the throwaway `Ka0sCopyBench`
addon) and the figures are recorded here.

## DR-OW-05 (AuraMaster sequencing)

Pending. AuraMaster's items wait for its batch 8, 9 and 10 branch to merge (Q16 (a)).
