# Plan review resolutions

The planning workflow (`plan-data/plan-workflow.json`, 19 agents) ran two critics over the planners' 104 items: one for
completeness and traceability, one for feasibility and ordering. Every finding was disposed of by the session lead in
`plan-data/tools/assemble.py`, which writes `plan-data/items.json` and `items.tsv` and checks that every dependency resolves
and that the graph is acyclic.

## Accepted, as written by the critics

- **Placeholder dependencies.** These came from the parallel WS/LK/DC planning and were mapped to real ids (WS-03/05/06/07/08, DC-01..04).
- **Missing ordering edges:**
  - LK-01 → WS-01 (the `__` clause before the removal)
  - LK-22 → WS-11 (the release reads the finished standard)
  - LK-23 → every adoption item
  - KC-01 → LK-09 and WS-06
  - every `<PFX>-RV` → LK-22, WS-11 and DC-04
  - DW-04 → LK-11, not LK-10 (LK-10 may be reverted)
  - DW-10 → LK-25 and WS-10
- **Contract contradictions removed:**
  - `d.panel.store` from BL-12 and LH-13
  - `IsGuarded` from DW-02's stub
- **LK-12 and LK-13.** No temporary `seam.__setActive` hook; the active-path cases are written against a real session.
- **LK-11 outcome B.** The revert is folded into the `LK-11:` commit and recorded in `exceptions.tsv`.
- **LK-03.** Cites the kit's own revision contract, not the `__` clause.
- **LK-02.** The false Quick Comms clause is dropped.
- **LK-04 and LK-05.** A ≤ 1450-line budget for run-automated-tests.sh, else a sourced helper.
- **PC-RV.** VERIFY commands added.
- **BL-02.** The opts.icon branch only.
- **WG-01.** A combat-path test.
- **Oversized items** land as two green commits under one id: DW-02 (seam and session, then timeline) and LH-10 (seam, then session).
- **Missing items added:**
  - LK-25: rejections in the API documents
  - MM-04: the ChatSender comment
  - a standards-reference refresh per addon: AT-01, AM-01 (with the test-mode marker audit), CM-01, DW-12, KC-03, LH-15, MM-05,
    PM-01, PF-01, PG-01, PC-01, QC-04, WG-03
  - LH-16 and PG-02: GitHub closures
  - CT-01: run records
  - CT-02: finalize

## Lead rulings

- **DropWatcher keeps its `sim.stepDelay` schema row.** OWNER_SCOPE C.11's fixed constant binds only the new simulators, because DW's row
  is an owner choice from its sim feedback batch.
- **The cycle the completeness critic's CT-01 proposal would have created** (CT-01 → WS-12 → CT-02 → CT-01) is broken. CT-01 records
  the run before finalize. Every GitHub closure item (LK-24, WS-12, BL-15, MM-03, KC-02, WG-02, DW-11, LH-16, PG-02) depends on
  CT-02 and runs after the merge.
