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

Measured 2026-09-26 by the owner with the throwaway `Ka0sCopyBench` v2 (`03_EXECUTION_PLAN.md` §5,
option A). Each figure is the median of 3 runs of Copy-open plus the next frame, with the N=0 baseline subtracted:

| Width | N=1500 | N=3000 | N=5000 | Limit |
|---|---|---|---|---|
| W=120 | 112 ms | 246 ms | **378 ms** | 250 ms |
| W=200 | 171 ms | 346 ms | 419 ms | 1000 ms |

Hands-on at 5000 (`/copybench keep`): Copy captured all 5000 lines intact, but the owner found the box
"a bit slow and sluggish".

**Ruling: MAX_BUFFER = 3000, BUFFER_SLACK = 128.** At 5000 the W=120 case fails its 250 ms limit, and the
hands-on check confirms it, so the Q2 fallback applies. 3000 passes, though only just (246 ms against 250 ms),
which is why the fallback is not 5000. DR-LK-02, DR-WS-05 and DR-LK-05 use 3000.

## DR-OW-03 (the DragHandle X, Q1)

Ruled in DR-OW-01 (the Q1 row above) and recorded here as its own item: **ConsumableMaster**'s X sets
`macroBar.enabled = false`; **AbsorbTracker**'s X sets `units.<unit>.enabled = false` on every bar, the
player bar included; **KickCD** gets no X (X-03). The M3 items for those three addons follow this.

## DR-OW-05 (AuraMaster sequencing)

Done 2026-09-26. With every smoke section (Z to AD) passed, the owner approved the merge, and
`/wow-addon:finalize` merged AuraMaster's `feat/2026-09-25-feedback-batch8` (batches 8 to 11) to master as
`73e2d8f`. It vendors LibKa0s v1.59.0, whose close-button branch was merged (`c01db86`) and tagged and
pushed first. AuraMaster's DR-AM items now start from that master.

## DR-OW-07 (publishing the standard)

Done 2026-09-26, on the owner's go-ahead in the same finalize pass: WowAddonStandards v2.68.0 merged to
master (`2854053`) and wow-addon merged (`837554f`), so revendor-standards and standards-audit fetch the
new standard from raw GitHub master. LibKa0s's rollout branch was merged too (`db0c54a`, v1.60.0
unreleased); its release and local tag remain DR-LK-06, which needs the owner.
