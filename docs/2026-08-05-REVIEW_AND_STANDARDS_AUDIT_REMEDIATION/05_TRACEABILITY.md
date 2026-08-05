# 05 — Traceability

**Every one of the 254 surviving findings mapped to a cluster, a milestone and a work item.**

Nothing here has been executed. See `00_OVERVIEW.md`.

---

## The rule

Every finding gets exactly one row and exactly one work item. A finding deliberately not acted on still
gets a row, marked **DEFERRED** with a reason. **Silence is not allowed.**

Every row also carries a **Disposition**, because "mapped" and "remediated" are not the same claim:

| Disposition | What closing the item actually does |
|---|---|
| `fix` | Code or documentation changes. |
| `rule-change` | The standard changes; the cited code is untouched and becomes compliant by definition. |
| `register-row` | A ratified deviation is recorded in `docs/ARCHITECTURE.md` § Documented deviations. The cited code is untouched. |
| `deferred` | No action; a written reason and, where applicable, a re-check trigger. |

Where two bundles found the same defect independently, both ids appear (so each bundle's ledger stays
complete) and both map to the **same** work item — closing that item closes both.

`OO` in the Cluster column means a true one-off with no counterpart in any other repo.

---

# Part 1 — The map

Ordered by repo, then by finding id, so a per-repo reader can check completeness at a glance.

## AbsorbTracker — 25

| Finding | Sev | Cluster | Milestone | Work item | Disposition |
|---|---|---|---|---|---|
| AT-R-01 | Medium | C9 | M3 | M3-12 | fix |
| AT-R-02 | Low | C26 | M4 | M4-15 | fix |
| AT-R-03 | Low | OO | M4 | M4-18 | fix |
| AT-R-04 | Low | OO | M4 | M4-18 | fix |
| AT-R-05 | Low | C12 | M3 | M3-03 | fix |
| AT-R-06 | Low | C16 | M4 | M4-06 | fix |
| AT-R-07 | Low | OO | M4 | M4-18 | fix |
| AT-R-08 | Low | OO | M4 | M4-18 | fix |
| AT-R-09 | Info | C7 | M4 | M4-07 | fix |
| AT-R-10 | Low | C7 | M4 | M4-07 | fix |
| AT-R-11 | Low | C3 | M4 | M4-10 | fix |
| AT-R-13 | Low | C6 | M3 | M3-02 | fix |
| AT-A-01 | Low | C5 | M4 | M4-08 | fix |
| AT-A-02 | Low | C10 | M4 | M4-01 | fix |
| AT-A-03 | Low | C11 | M4 | M4-27 | rule-change *or* fix |
| AT-A-04 | Low | C5 | M4 | M4-08 | fix |
| AT-A-05 | Low | C18 | M3 | M3-05 | fix |
| AT-A-06 | Low | C23 | M4 | M4-11 | fix |
| AT-A-07 | Low | C8 | M3 | M3-06 | fix |
| AT-A-09 | Low | C20 | M4 | M4-17 | register-row |
| AT-A-10 | Info | OO | M3 | M3-08 | register-row |
| AT-A-11 | Low | C15 | M3 | M3-07 | fix |
| AT-A-12 | Low | C4 | M3 | M3-08 | register-row |
| AT-A-13 | Low | C26 | M4 | M4-15 | fix |
| AT-A-16 | Info | C22 | M4 | M4-12 | fix |

## BankLedger — 24

| Finding | Sev | Cluster | Milestone | Work item | Disposition |
|---|---|---|---|---|---|
| BL-R-01 | Medium | OO | M4 | M4-19 | fix |
| BL-R-02 | Low | C6 | M3 | M3-02 | fix |
| BL-R-03 | Low | C7 | M4 | M4-07 | fix |
| BL-R-04 | Low | OO | M4 | M4-19 | fix |
| BL-R-05 | Low | C3 | M4 | M4-10 | fix |
| BL-R-06 | Info | OO | M4 | M4-19 | fix |
| BL-R-07 | Low | C3 | M4 | M4-10 | fix |
| BL-R-08 | Low | OO | M4 | M4-19 | fix |
| BL-R-09 | Low | C24 | M4 | M4-03 | fix |
| BL-A-01 | Info | C19 | **M5** | **M5-02 — DEFERRED** | deferred |
| BL-A-02 | Medium | C1 | M3 | M3-09 | rule-change |
| BL-A-03 | Low | C1 | M3 | M3-09 | rule-change |
| BL-A-04 | Low | C1 | M3 | M3-09 | rule-change |
| BL-A-05 | Info | C1 | M3 | M3-09 | rule-change |
| BL-A-06 | Low | C1 | M3 | M3-09 | rule-change |
| BL-A-07 | Low | C1 | M3 | M3-09 | rule-change |
| BL-A-08 | Info | C1 | M3 | M3-09 | rule-change |
| BL-A-09 | Medium | C11 | **M2** | M2-08 | fix |
| BL-A-10 | Low | C30 | M4 | M4-14 | fix |
| BL-A-11 | Low | C15 | M3 | M3-07 | fix |
| BL-A-12 | Low | C8 | M3 | M3-06 | fix |
| BL-A-13 | Low | C18 | M3 | M3-05 | fix |
| BL-A-14 | Low | C6 | M3 | M3-02 | fix |
| BL-A-16 | Info | C29 | **M5** | **M5-01 — DEFERRED** | deferred |

## ConsumableMaster — 43

| Finding | Sev | Cluster | Milestone | Work item | Disposition |
|---|---|---|---|---|---|
| CM-R-01 | **High** | C2 | **M2** | M2-03 | fix |
| CM-R-02 | **High** | C2 | **M2** | M2-03 | fix |
| CM-R-03 | Medium | C2 | **M2** | M2-04 | fix |
| CM-R-04 | Medium | C16 | M4 | M4-06 | fix |
| CM-R-05 | Low | OO | M4 | M4-20 | fix |
| CM-R-06 | Medium | C14 | M3 | M3-10 | fix |
| CM-R-07 | Low | C6 | M3 | M3-02 | fix |
| CM-R-08 | Low | C22 | M4 | M4-12 | fix |
| CM-R-09 | Low | C7 | M4 | M4-07 | fix |
| CM-R-10 | Low | C32 | M4 | M4-16 | fix |
| CM-R-11 | Low | C3 | M4 | M4-10 | fix |
| CM-R-12 | Info | C7 | M4 | M4-07 | fix |
| CM-R-13 | Info | C3 | M4 | M4-10 | fix |
| CM-A-01 | Info | C4 | M3 | M3-08 | register-row |
| CM-A-02 | Medium | C14 | M3 | M3-10 | fix |
| CM-A-03 | Medium | C12 | M3 | M3-03b | fix |
| CM-A-04 | Low | C21 | **M2** | M2-03 | fix |
| CM-A-05 | Low | C21 | M3 | M3-13 | fix |
| CM-A-06 | Medium | C1 | M4 | M4-25 | fix |
| CM-A-07 | Low | C9 | M3 | M3-12 | fix |
| CM-A-08 | Low | C9 | M3 | M3-12 | fix |
| CM-A-09 | Low | C1 | M4 | M4-25 | fix |
| CM-A-10 | Low | C1 | M4 | M4-25 | fix |
| CM-A-11 | Low | C1 | M4 | M4-25 | fix |
| CM-A-12 | Low | OO | M4 | M4-20 | fix |
| CM-A-13 | Low | C9 | M3 | M3-12 | fix |
| CM-A-14 | Low | C10 | M4 | M4-01 | fix |
| CM-A-15 | Low | C19 | M4 | M4-02 | fix |
| CM-A-16 | Info | C4 | M3 | M3-08 | register-row |
| CM-A-17 | Low | C5 | M4 | M4-08 | fix |
| CM-A-18 | Medium | C10 | M4 | M4-01 | fix |
| CM-A-20 | Info | C15 | M3 | M3-07 | fix |
| CM-A-21 | Info | C29 | **M5** | **M5-01 — DEFERRED** | deferred |
| CM-A-23 | Info | C31 | M4 | M4-13 | fix |
| CM-A-25 | **High** | C2 | **M2** | M2-03 | fix |
| CM-A-26 | Low | C5 | M3 | M3-11 | fix |
| CM-A-27 | Low | C25 | M4 | M4-09 | fix |
| CM-A-28 | Low | C8 | M3 | M3-06 | fix |
| CM-A-29 | Low | C18 | M3 | M3-05 | fix |
| CM-A-30 | Low | C32 | M4 | M4-16 | fix |
| CM-A-31 | Low | C6 | M3 | M3-02 | fix |
| CM-A-32 | **High** | C2 | **M2** | M2-04 | fix |
| CM-A-34 | Low | C26 | M4 | M4-15 | fix |

## KickCD — 30

| Finding | Sev | Cluster | Milestone | Work item | Disposition |
|---|---|---|---|---|---|
| KCD-R-01 | Medium | OO | **M2** | M2-07 | fix |
| KCD-R-02 | Low | C6 | M3 | M3-02 | fix |
| KCD-R-03 | Medium | C10 | M4 | M4-01 | fix |
| KCD-R-04 | Low | C10 | M4 | M4-01 | fix |
| KCD-R-05 | Low | C9 | M3 | M3-12 | fix |
| KCD-R-06 | Low | C24 | M4 | M4-03 | fix |
| KCD-R-07 | Low | C1 | M4 | M4-25 | fix |
| KCD-R-08 | Medium | C14 | M3 | M3-10 | fix |
| KCD-R-09 | Low | C3 | M4 | M4-10 | fix |
| KCD-R-10 | Low | C3 | M4 | M4-10 | fix |
| KCD-R-11 | Info | C7 | M4 | M4-07 | fix |
| KCD-R-12 | Info | C7 | M4 | M4-07 | fix |
| KCD-A-01 | Medium | C14 | M3 | M3-10 | fix |
| KCD-A-02 | Low | C21 | M3 | M3-13 | fix |
| KCD-A-03 | Low | C21 | M3 | M3-13 | fix |
| KCD-A-04 | Low | C11 | M4 | M4-27 | rule-change *or* fix |
| KCD-A-05 | Medium | C1 | M4 | M4-25 | fix |
| KCD-A-06 | Low | C1 | M4 | M4-25 | fix |
| KCD-A-07 | Low | C5 | M4 | M4-08 | fix |
| KCD-A-08 | Medium | C17 | M4 | M4-04 | fix |
| KCD-A-09 | Medium | C10 | M4 | M4-01 | fix |
| KCD-A-10 | Low | C19 | M4 | M4-02 | fix |
| KCD-A-11 | Medium | OO | **M2** | M2-07 | fix |
| KCD-A-12 | Low | C6 | M3 | M3-02 | fix |
| KCD-A-13 | Low | C8 | M3 | M3-06 | fix |
| KCD-A-14 | Low | C2 | M4 | M4-26 | fix |
| KCD-A-15 | Low | C11 | M4 | M4-27 | rule-change *or* fix |
| KCD-A-16 | Low | C27 | M4 | M4-28 | fix |
| KCD-A-17 | Low | C24 | M4 | M4-03 | fix |
| KCD-A-18 | Low | C9 | M3 | M3-12 | fix |

## LootHistory — 34

| Finding | Sev | Cluster | Milestone | Work item | Disposition |
|---|---|---|---|---|---|
| LH-R-01 | Medium | OO | **M2** | M2-09 | fix |
| LH-R-02 | Low | C28 | M4 | M4-05 | fix |
| LH-R-03 | Low | C17 | M4 | M4-04 | fix |
| LH-R-04 | Low | OO | M4 | M4-21 | fix |
| LH-R-05 | Low | C6 | M3 | M3-02 | fix |
| LH-R-06 | Low | C2 | M3 | M3-04 | fix |
| LH-R-07 | Low | C3 | M4 | M4-10 | fix |
| LH-R-08 | Info | C22 | M4 | M4-12 | fix |
| LH-R-09 | Info | OO | M4 | M4-21 | fix |
| LH-R-10 | Low | C2 | M3 | M3-04 | fix |
| LH-A-19 | Low | C15 | M3 | M3-07 | fix |
| LH-A-20 | Medium | C1 | M3 | M3-09 | rule-change |
| LH-A-21 | Low | C1 | M3 | M3-09 | rule-change |
| LH-A-22 | Low | C1 | M3 | M3-09 | rule-change |
| LH-A-23 | Low | C1 | M3 | M3-09 | rule-change |
| LH-A-24 | Medium | C1 | M3 | M3-09 | rule-change |
| LH-A-25 | Low | C1 | M3 | M3-09 | rule-change |
| LH-A-26 | Low | C1 | M3 | M3-09 | rule-change |
| LH-A-27 | Medium | C10 | **M2** | M2-06 | fix |
| LH-A-28 | Low | C19 | M4 | M4-02 | fix |
| LH-A-29 | Medium | C12 | M3 | M3-03 | fix |
| LH-A-30 | Low | C30 | M4 | M4-14 | fix |
| LH-A-33 | Low | C7 | M4 | M4-07 | fix |
| LH-A-34 | Medium | OO | **M2** | M2-09 | fix |
| LH-A-35 | Low | C17 | M4 | M4-04 | fix |
| LH-A-36 | Low | C8 | M3 | M3-06 | fix |
| LH-A-37 | Low | C23 | M4 | M4-11 | fix |
| LH-A-38 | Low | C5 | M4 | M4-08 | fix |
| LH-A-39 | Low | C2 | M3 | M3-04 | fix |
| LH-A-40 | Low | C6 | M3 | M3-02 | fix |
| LH-A-41 | Low | C23 | M4 | M4-11 | fix |
| LH-A-42 | Low | OO | M4 | M4-21 | fix |
| LH-A-43 | Low | C28 | M4 | M4-05 | fix |
| LH-A-44 | Info | C22 | M4 | M4-12 | fix |

## PanelMaster — 28

| Finding | Sev | Cluster | Milestone | Work item | Disposition |
|---|---|---|---|---|---|
| PM-R-01 | **High** | C2 | **M2** | M2-05 | fix |
| PM-R-02 | Low | C28 | M4 | M4-05 | fix |
| PM-R-03 | Low | C2 | M4 | M4-26 | fix |
| PM-R-04 | Low | OO | M4 | M4-22 | fix |
| PM-R-05 | Low | C6 | M3 | M3-02 | fix |
| PM-R-06 | Low | OO | M4 | M4-22 | fix |
| PM-R-07 | Low | C2 | M3 | M3-04 | fix |
| PM-R-08 | Low | C7 | M4 | M4-07 | fix |
| PM-R-09 | Low | C3 | M4 | M4-10 | fix |
| PM-R-10 | Low | C3 | M4 | M4-10 | fix |
| PM-R-11 | Low | C17 | M4 | M4-04 | fix |
| PM-R-12 | Low | OO | M4 | M4-22 | fix |
| PM-A-01 | Medium | C1 | M3 | M3-09 | rule-change |
| PM-A-02 | Low | C1 | M3 | M3-09 | rule-change |
| PM-A-03 | Low | C1 | M3 | M3-09 | rule-change |
| PM-A-04 | Low | C1 | M3 | M3-09 | rule-change |
| PM-A-05 | Low | C1 | M3 | M3-09 | rule-change |
| PM-A-06 | Info | C1 | M3 | M3-09 | rule-change |
| PM-A-08 | Low | C11 | M4 | M4-27 | rule-change *or* fix |
| PM-A-09 | Low | C1 | M3 | M3-09 | rule-change |
| PM-A-10 | Low | C12 | M3 | M3-03 | fix |
| PM-A-11 | Low | C18 | M3 | M3-05 | fix |
| PM-A-12 | Low | C5 | M4 | M4-08 | fix |
| PM-A-13 | Low | C8 | M3 | M3-06 | fix |
| PM-A-17 | Info | C20 | M4 | M4-17 | register-row |
| PM-A-18 | Info | C4 | M3 | M3-08 | register-row |
| PM-A-19 | Info | C4 | M3 | M3-08 | register-row |
| PM-A-20 | Info | C4 | M3 | M3-08 | register-row |

## prettychat — 29

| Finding | Sev | Cluster | Milestone | Work item | Disposition |
|---|---|---|---|---|---|
| PC-R-01 | **High** | OO | **M2** | M2-01 | fix |
| PC-R-02 | **High** | OO | **M2** | M2-01 | fix |
| PC-R-03 | Medium | C16 | M4 | M4-06 | fix |
| PC-R-04 | Low | OO | M4 | M4-23 | fix |
| PC-R-05 | Medium | OO | M4 | M4-23 | fix |
| PC-R-06 | Low | C20 | M4 | M4-17 | register-row |
| PC-R-07 | Low | C33 | **M1** | M1-LK-06 | fix |
| PC-R-08 | Low | OO | M4 | M4-23 | fix |
| PC-R-09 | Info | C2 | M3 | M3-04 | fix |
| PC-R-10 | Info | C3 | M4 | M4-10 | fix |
| PC-A-01 | Low | C4 | M3 | M3-08 | register-row |
| PC-A-02 | Low | C1 | M3 | M3-09 | rule-change |
| PC-A-03 | Low | C1 | M3 | M3-09 | rule-change |
| PC-A-04 | Info | C1 | M3 | M3-09 | rule-change |
| PC-A-05 | Info | C1 | M3 | M3-09 | rule-change |
| PC-A-06 | Low | C1 | M3 | M3-09 | rule-change |
| PC-A-08 | Low | C5 | M4 | M4-08 | fix |
| PC-A-09 | Low | C5 | M4 | M4-08 | fix |
| PC-A-10 | Low | C5 | M4 | M4-08 | fix |
| PC-A-11 | Info | C29 | **M5** | **M5-01 — DEFERRED** | deferred |
| PC-A-12 | Low | C17 | **M1** | M1-STD-12 | rule-change |
| PC-A-13 | Low | C8 | M3 | M3-06 | fix |
| PC-A-14 | Info | C4 | M3 | M3-08 | register-row |
| PC-A-15 | Info | C4 | M3 | M3-08 | register-row |
| PC-A-16 | Info | C14 | M3 | M3-10 | fix |
| PC-A-17 | Low | C25 | M4 | M4-09 | fix |
| PC-A-18 | Info | C4 | M3 | M3-08 | register-row |
| PC-A-21 | Info | C4 | M3 | M3-08 | register-row |
| PC-A-22 | Info | C4 | **M1** | M1-STD-15 | rule-change |

## WhatGroup — 21

| Finding | Sev | Cluster | Milestone | Work item | Disposition |
|---|---|---|---|---|---|
| WG-R-01 | **High** | OO | **M2** | M2-02 | fix |
| WG-R-03 | Low | C24 | M4 | M4-03 | fix |
| WG-R-04 | Low | OO | M4 | M4-24 | fix |
| WG-R-05 | Low | OO | M4 | M4-24 | fix |
| WG-R-06 | Low | C20 | M4 | M4-17 | register-row |
| WG-R-08 | Info | C7 | M4 | M4-07 | fix |
| WG-R-09 | Low | C27 | M3 | M3-14a | fix |
| WG-A-01 | Low | C1 | M3 | M3-09 | rule-change |
| WG-A-02 | Low | C1 | M3 | M3-09 | rule-change |
| WG-A-03 | Low | C1 | M3 | M3-09 | rule-change |
| WG-A-04 | Low | C1 | M3 | M3-09 | rule-change |
| WG-A-05 | Low | C1 | M3 | M3-09 | rule-change |
| WG-A-06 | Info | C1 | M3 | M3-09 | rule-change |
| WG-A-07 | Low | C31 | M4 | M4-13 | fix |
| WG-A-08 | Low | C11 | M4 | M4-27 | rule-change *or* fix |
| WG-A-10 | Low | C5 | M4 | M4-08 | fix |
| WG-A-11 | Low | C25 | M4 | M4-09 | fix |
| WG-A-12 | Low | C10 | M4 | M4-01 | fix |
| WG-A-13 | Info | OO | M4 | M4-24 | fix |
| WG-A-14 | Low | C8 | M3 | M3-06 | fix |
| WG-A-15 | Info | C15 | M3 | M3-07 | fix |

## LibKa0s — 20

Every LibKa0s finding lands in **Milestone 1**, because LibKa0s is upstream. One is deferred.

| Finding | Sev | Cluster | Milestone | Work item | Disposition |
|---|---|---|---|---|---|
| LK-R-01 | Medium | C12 | M1 | M1-LK-11 | fix |
| LK-R-02 | Low | C3 | M1 | M1-LK-12 | fix |
| LK-R-03 | Low | C16 | M1 | M1-LK-12 | fix |
| LK-R-04 | Low | C9 | M1 | M1-LK-08 | fix |
| LK-R-05 | Info | C9 | M1 | M1-LK-08 | fix |
| LK-R-06 | Low | C9 | M1 | M1-LK-08 | fix |
| LK-A-01 | Low | C13 | M1 | M1-LK-13 | fix |
| LK-A-02 | Low | C13 | M1 | M1-LK-13 | fix |
| LK-A-03 | Low | C13 | M1 | M1-LK-13 | fix |
| LK-A-04 | Low | C13 | M1 | M1-LK-13 | fix |
| LK-A-05 | Low | C13 | M1 | M1-LK-13 | fix |
| LK-A-06 | Low | C27 | M1 | M1-LK-10 | fix |
| LK-A-07 | Low | C23 | M1 | M1-LK-12 | fix |
| LK-A-08 | Low | C8 | M1 | M1-LK-12 | fix |
| LK-A-09 | Medium | C12 | M1 | M1-LK-11 | fix |
| LK-A-10 | Low | C16 | M1 | M1-LK-12 | fix |
| LK-A-11 | Low | C5 | M1 | M1-LK-12 | fix |
| LK-A-12 | Info | C13 | M1 | M1-LK-13 | fix |
| LK-A-13 | Info | C1 | **M5** | **M5-03 — DEFERRED** | deferred |
| LK-A-15 | Low | C3 | M1 | M1-LK-12 | fix |

---

# Part 2 — Coverage proof

## Total surviving findings

| Repo | Review | Audit | Total |
|---|---|---|---|
| AbsorbTracker | 12 | 13 | 25 |
| BankLedger | 9 | 15 | 24 |
| ConsumableMaster | 13 | 30 | 43 |
| KickCD | 12 | 18 | 30 |
| LootHistory | 10 | 24 | 34 |
| PanelMaster | 12 | 16 | 28 |
| prettychat | 10 | 19 | 29 |
| WhatGroup | 7 | 14 | 21 |
| LibKa0s | 6 | 14 | 20 |
| **Total** | **91** | **163** | **254** |

`25 + 24 + 43 + 30 + 34 + 28 + 29 + 21 + 20 = 254` ✓
`91 + 163 = 254` ✓

## Total mapped

**254 of 254.** Every id in Part 1 appears exactly once and carries a work item.

Per repo, rows in Part 1: AbsorbTracker 25, BankLedger 24, ConsumableMaster 43, KickCD 30,
LootHistory 34, PanelMaster 28, prettychat 29, WhatGroup 21, LibKa0s 20.
`25+24+43+30+34+28+29+21+20 = 254` ✓ — identical to the totals above, repo by repo.

**Unmapped: 0.**

## Count per severity — every one mapped

| Severity | Count | Mapped | Unmapped |
|---|---|---|---|
| Critical | 0 | 0 | 0 |
| **High** | **8** | **8** | **0** |
| **Medium** | **30** | **30** | **0** |
| **Low** | **173** | **173** | **0** |
| **Info** | **43** | **43** | **0** |
| **Total** | **254** | **254** | **0** |

`8 + 30 + 173 + 43 = 254` ✓

**Seven findings moved Medium → Low in review.** C6's ten rows are one byte-identical defect
(`if not tag then return end`) that the source bundles graded Low in three repos and Medium in seven. The
reachability is identical in all six repos — *a clone with no `../LibKa0s` sibling; the sibling is present
on this machine and no repo has CI or a git hook* — so under this plan's impact rubric all ten are **Low**.
The seven that moved: `BL-R-02`, `BL-A-14`, `CM-R-07`, `CM-A-31`, `LH-R-05`, `LH-A-40`, `PM-R-05`.

### Severity by repo — the cross-check

| Repo | High | Medium | Low | Info | Total |
|---|---|---|---|---|---|
| AbsorbTracker | 0 | 1 | 21 | 3 | 25 |
| BankLedger | 0 | 3 | 16 | 5 | 24 |
| ConsumableMaster | 4 | 7 | 25 | 7 | 43 |
| KickCD | 0 | 8 | 20 | 2 | 30 |
| LootHistory | 0 | 6 | 25 | 3 | 34 |
| PanelMaster | 1 | 1 | 21 | 5 | 28 |
| prettychat | 2 | 2 | 14 | 11 | 29 |
| WhatGroup | 1 | 0 | 16 | 4 | 21 |
| LibKa0s | 0 | 2 | 15 | 3 | 20 |
| **Total** | **8** | **30** | **173** | **43** | **254** |

Column sums: High `0+0+4+0+0+1+2+1+0 = 8` ✓ · Medium `1+3+7+8+6+1+2+0+2 = 30` ✓ ·
Low `21+16+25+20+25+21+14+16+15 = 173` ✓ · Info `3+5+7+2+3+5+11+4+3 = 43` ✓

### The 8 Highs, individually accounted for

| Finding | Repo | Milestone | Work item | Status |
|---|---|---|---|---|
| CM-R-01 | ConsumableMaster | M2 | M2-03 | mapped |
| CM-R-02 | ConsumableMaster | M2 | M2-03 | mapped |
| CM-A-25 | ConsumableMaster | M2 | M2-03 | mapped |
| CM-A-32 | ConsumableMaster | M2 | M2-04 | mapped |
| PM-R-01 | PanelMaster | M2 | M2-05 | mapped |
| PC-R-01 | prettychat | M2 | M2-01 | mapped |
| PC-R-02 | prettychat | M2 | M2-01 | mapped |
| WG-R-01 | WhatGroup | M2 | M2-02 | mapped |

**All eight are in Milestone 2, and Milestone 2 has no dependency on Milestone 1.**
**Zero Highs are deferred.**

### The 30 Mediums, by work item

| Work item | Mediums |
|---|---|
| M2-03 | CM-R-01†, CM-R-02† — *(Highs; listed for completeness of the item, not counted here)* |
| M2-04 | CM-R-03 |
| M2-06 | LH-A-27 |
| M2-07 | KCD-R-01, KCD-A-11 |
| M2-08 | BL-A-09 |
| M2-09 | LH-R-01, LH-A-34 |
| M3-03 | LH-A-29 |
| M3-03b | CM-A-03 |
| M3-09 | BL-A-02, LH-A-20, LH-A-24, PM-A-01 |
| M3-10 | CM-R-06, CM-A-02, KCD-R-08, KCD-A-01 |
| M3-12 | AT-R-01 |
| M4-01 | CM-A-18, KCD-R-03, KCD-A-09 |
| M4-04 | KCD-A-08 |
| M4-06 | CM-R-04, PC-R-03 |
| M4-19 | BL-R-01 |
| M4-23 | PC-R-05 |
| M4-25 | CM-A-06, KCD-A-05 |
| M1-LK-11 | LK-R-01, LK-A-09 |

Count: `1+1+2+1+2+1+1+4+4+1+3+1+2+1+1+2+2 = ` **30** ✓ († rows are Highs, excluded from this count).

**Two corrections here, both from review.** `M4-19`'s `BL-R-01` (the `/bl debug` panel reading
`LibStub.minors["O.AceGUI-3.0"]`) was **missing from this table entirely** while being mapped correctly in
Part 1 and Part 4 — the one accounting table in this document a reader could have used to conclude a Medium
was unaccounted for. And `M3-02`'s seven rows are gone because C6 re-graded to Low throughout; the earlier
stated sum evaluated to 36, not the claimed 37.

**Zero Mediums are deferred.**

## Mapped per milestone

| Milestone | Work items | Findings mapped |
|---|---|---|
| M1 — Upstream | 41 (+1 conditional) | 22 |
| M2 — The eight Highs | 9 | 16 |
| M3 — Adoption of M1 | 15 | 96 |
| M4 — Repo-local | 28 | 115 |
| M5 — Recorded decisions | 3 | 5 |
| **Total** | **96** | **254** |

`22 + 16 + 96 + 115 + 5 = 254` ✓
`41 + 9 + 15 + 28 + 3 = 96` work items ✓ — **97 under `M1-STD-11` option (b)**, which schedules the
conditional `M1-LK-15`.

Only 22 findings close *inside* Milestone 1 because M1 is upstream: LibKa0s's own 19 (all but the
deferred `LK-A-13`), plus 2 rule-text problems whose resolution **is** the rule change (`PC-A-12` via
`M1-STD-12`; `PC-A-22` via `M1-STD-15`), plus `PC-R-07`, which is a defect in the vendored runner and
therefore fixed at the source (`M1-LK-06`). The other 232 are **unblocked** by M1, not closed by it.
`AT-A-10` was counted here in an earlier draft; it is now an `M3-08` register row, because
`M1-STD-12` no longer carves a permanent `events-frames-taint-§1` exception on one Info row's evidence.

## Mapped per cluster

| Cluster | N | Work items it maps to |
|---|---|---|
| C1 | 40 | M3-09 (32), M4-25 (7), M5-03 (1) |
| C2 | 13 | M2-03 (3), M2-04 (2), M2-05 (1), M3-04 (5), M4-26 (2) |
| C3 | 13 | M4-10 (11), M1-LK-12 (2) |
| C4 | 12 | M3-08 (11), M1-STD-15 (1) |
| C5 | 12 | M4-08 (10), M3-11 (1), M1-LK-12 (1) |
| C6 | 10 | M3-02 (10) |
| C7 | 10 | M4-07 (10) |
| C8 | 9 | M3-06 (8), M1-LK-12 (1) |
| C9 | 9 | M3-12 (6), M1-LK-08 (3) |
| C10 | 8 | M4-01 (7), M2-06 (1) |
| C11 | 6 | M4-27 (5), M2-08 (1) |
| C12 | 6 | M3-03 (3), M3-03b (1), M1-LK-11 (2) |
| C13 | 6 | M1-LK-13 (6) |
| C14 | 5 | M3-10 (5) |
| C15 | 5 | M3-07 (5) |
| C16 | 5 | M4-06 (3), M1-LK-12 (2) |
| C17 | 5 | M4-04 (4), M1-STD-12 (1) |
| C18 | 4 | M3-05 (4) |
| C19 | 4 | M4-02 (3), M5-02 (1) |
| C20 | 4 | M4-17 (4) |
| C21 | 4 | M3-13 (3), M2-03 (1) |
| C22 | 4 | M4-12 (4) |
| C23 | 4 | M4-11 (3), M1-LK-12 (1) |
| C24 | 4 | M4-03 (4) |
| C25 | 3 | M4-09 (3) |
| C26 | 3 | M4-15 (3) |
| C27 | 3 | M3-14a (1), M4-28 (1), M1-LK-10 (1) |
| C28 | 3 | M4-05 (3) |
| C29 | 3 | M5-01 (3) |
| C30 | 2 | M4-14 (2) |
| C31 | 2 | M4-13 (2) |
| C32 | 2 | M4-16 (2) |
| C33 | 1 | M1-LK-06 (1) |
| **Clustered subtotal** | **224** | |
| One-offs (OO) | 30 | M2-01 (2), M2-02 (1), M2-07 (2), M2-09 (2), M3-08 (1), M4-18 (4), M4-19 (4), M4-20 (2), M4-21 (3), M4-22 (3), M4-23 (3), M4-24 (3) |
| **Total** | **254** | |

Cluster running sum: 40, 53, 66, 78, 90, 100, 110, 119, 128, 136, 142, 148, 154, 159, 164, 169, 174,
178, 182, 186, 190, 194, 198, 202, 205, 208, 211, 214, 217, 219, 221, 223, **224** ✓
One-offs: `2+1+2+2+1+4+4+2+3+3+3+3 = 30` ✓
`224 + 30 = 254` ✓

**Two moves out of C4, both from review.** `WG-A-13` left C4 for the one-off list (nothing ratifies it — no
register row, no ledger entry, no in-code rationale; it is a genuinely unmet `debug-logging-§2` SHOULD, now
code work at `M4-24`), and `AT-A-10` joined `M3-08` from `M1-STD-12` as a register row. C4 is 12, not 13;
the one-offs are 30, not 29.

---

# Part 3 — Deferrals

Three work items are dispositions rather than changes. **Five findings** are deferred, and every one
carries a reason. No High and no Medium is among them.

| Work item | Findings | Sev | Reason for deferral |
|---|---|---|---|
| **M5-01** | BL-A-16, CM-A-21, PC-A-11 | Info ×3 | **Closed as not a deviation.** `layout-§1` caps any single `.lua` file at 1500 LOC and puts 1000–1500 "on notice"; a file inside the band is the **compliant** state. BankLedger's four files (1368, 1361, 1052, 1023), ConsumableMaster's `tests/test_macrobar.lua` (1497) and prettychat's `GlobalStrings/GlobalStrings.lua` (23,842) are all either inside the band or — in prettychat's case — a build-time input excluded at `.pkgmeta:21`, named by no TOC line and never loaded, so the cap's purpose (peelable runtime source) does not engage. Each audit's own text says no action is required. `M1-WA-03`'s grading rule is what stops these being re-filed. |
| **M5-02** | BL-A-01 | Info | **Ratified deviation; register row only.** `savedvariables-§2`'s file-placement MUST is unmet, but the argument against creating an empty `defaults/Profile.lua` in an addon with no per-profile settings is written down at `docs/ARCHITECTURE.md:568-581` — exactly where the process asks. Creating an empty file to satisfy the letter is worse than the absence. The row moves into `## Documented deviations` under `M3-08`, with a Decided date and a re-check trigger: the first per-profile setting. |
| **M5-03** | LK-A-13 | Info | **Out of scope by the rule's own text.** `performance-§9`'s own bullet keeps scenarios per-addon — "they stay in the addon rather than moving into the shared lib" — so the library not shipping a `tests/perf.lua` is contemplated by the section rather than a deviation from it. The genuine residue (nobody in the collection holds the `P.Open`/`P.Close` off-path number) is closed by `M1-LK-08`'s zero-overhead isolation case, not by a scenario runner. The manifest continues to record `perf: skip` with its reason. |

**Deferred total: 5 of 254 (2.0%) — 0 High, 0 Medium, 0 Low, 5 Info.**

**"Deferred: 5" is not the same as "remediated: 249", and the Disposition column in Part 1 says so.** The
honest split, recomputed from Part 1:

| Disposition | N | What it means |
|---|---|---|
| `fix` | **194** | Code or documentation actually changes. |
| `rule-change` | **34** | The standard changes; the cited code is untouched. `M3-09` (32) claims the newly written `performance-§12` exemption and adds a register row; `M1-STD-12` (1) and `M1-STD-15` (1) are rule-text corrections. |
| `register-row` | **16** | A ratified deviation is recorded. `M3-08` (12) and `M4-17` (4). The cited code is untouched. |
| `rule-change` *or* `fix` | **5** | `M4-27`, and which one is decided **upstream**: under `M1-STD-11` option (a) these five re-grade and record with no code change; under (b) they are ~50 mechanical call-site rewrites. |
| `deferred` | **5** | `M5-01` (3), `M5-02` (1), `M5-03` (1). |
| **Total** | **254** | |

`194 + 34 + 16 + 5 + 5 = 254` ✓

Each individual disposition is defensible and disclosed in the item text. The point of the column is that
the headline "5 deferred" invites reading the other 249 as remediation, and roughly **50 of them close by
rule change or register row without touching the code they cite**.

---

# Part 4 — Reverse index: work item → findings

For anyone working an item and wanting to know what closing it closes.

## Milestone 1 (22 findings across 41 items, 42 under option (b))

| Item | Findings |
|---|---|
| M1-LK-01 … M1-LK-05, M1-LK-07, M1-LK-09, M1-LK-14, M1-LK-15 (conditional) | *(enabling only — the findings they unblock close in M3)* |
| M1-LK-06 | PC-R-07 |
| M1-LK-08 | LK-R-04, LK-R-05, LK-R-06 |
| M1-LK-10 | LK-A-06 |
| M1-LK-11 | LK-R-01, LK-A-09 |
| M1-LK-12 | LK-R-02, LK-R-03, LK-A-07, LK-A-08, LK-A-10, LK-A-11, LK-A-15 |
| M1-LK-13 | LK-A-01, LK-A-02, LK-A-03, LK-A-04, LK-A-05, LK-A-12 |
| M1-STD-01 … M1-STD-11, M1-STD-13, M1-STD-14, M1-STD-16, M1-STD-17 | *(enabling only)* |
| M1-STD-12 | PC-A-12 |
| M1-STD-15 | PC-A-22 |
| M1-WA-01 … M1-WA-10 | *(enabling only)* |

## Milestone 2 (16 findings across 9 items)

| Item | Findings |
|---|---|
| M2-01 | PC-R-01, PC-R-02 |
| M2-02 | WG-R-01 |
| M2-03 | CM-R-01, CM-R-02, CM-A-25, CM-A-04 |
| M2-04 | CM-R-03, CM-A-32 |
| M2-05 | PM-R-01 |
| M2-06 | LH-A-27 |
| M2-07 | KCD-R-01, KCD-A-11 |
| M2-08 | BL-A-09 |
| M2-09 | LH-R-01, LH-A-34 |

## Milestone 3 (96 findings across 15 items)

| Item | N | Findings |
|---|---|---|
| M3-01 | 0 | *(re-vendor; enabling)* |
| M3-02 | 10 | AT-R-13, BL-R-02, BL-A-14, CM-R-07, CM-A-31, KCD-R-02, KCD-A-12, LH-R-05, LH-A-40, PM-R-05 |
| M3-03 | 3 | AT-R-05, LH-A-29, PM-A-10 |
| M3-03b | 1 | CM-A-03 |
| M3-04 | 5 | LH-R-06, LH-R-10, LH-A-39, PM-R-07, PC-R-09 |
| M3-05 | 4 | AT-A-05, BL-A-13, CM-A-29, PM-A-11 |
| M3-06 | 8 | AT-A-07, BL-A-12, CM-A-28, KCD-A-13, LH-A-36, PM-A-13, PC-A-13, WG-A-14 |
| M3-07 | 5 | AT-A-11, BL-A-11, CM-A-20, LH-A-19, WG-A-15 |
| M3-08 | 12 | AT-A-10, AT-A-12, CM-A-01, CM-A-16, PC-A-01, PC-A-14, PC-A-15, PC-A-18, PC-A-21, PM-A-18, PM-A-19, PM-A-20 |
| M3-09 | 32 | BL-A-02…BL-A-08 (7), LH-A-20…LH-A-26 (7), PM-A-01…PM-A-06 + PM-A-09 (7), WG-A-01…WG-A-06 (6), PC-A-02…PC-A-06 (5) |
| M3-10 | 5 | CM-R-06, CM-A-02, KCD-R-08, KCD-A-01, PC-A-16 |
| M3-11 | 1 | CM-A-26 |
| M3-12 | 6 | AT-R-01, CM-A-07, CM-A-08, CM-A-13, KCD-R-05, KCD-A-18 |
| M3-13 | 3 | CM-A-05, KCD-A-02, KCD-A-03 |
| M3-14a | 1 | WG-R-09 |

`0+10+3+1+5+4+8+5+12+32+5+1+6+3+1 = 96` ✓

## Milestone 4 (115 findings across 28 items)

| Item | N | Findings |
|---|---|---|
| M4-01 | 7 | AT-A-02, CM-A-14, CM-A-18, KCD-R-03, KCD-R-04, KCD-A-09, WG-A-12 |
| M4-02 | 3 | CM-A-15, KCD-A-10, LH-A-28 |
| M4-03 | 4 | BL-R-09, KCD-R-06, KCD-A-17, WG-R-03 |
| M4-04 | 4 | KCD-A-08, LH-R-03, LH-A-35, PM-R-11 |
| M4-05 | 3 | LH-R-02, LH-A-43, PM-R-02 |
| M4-06 | 3 | AT-R-06, CM-R-04, PC-R-03 |
| M4-07 | 10 | AT-R-09, AT-R-10, BL-R-03, CM-R-09, CM-R-12, KCD-R-11, KCD-R-12, PM-R-08, WG-R-08, LH-A-33 |
| M4-08 | 10 | AT-A-01, AT-A-04, CM-A-17, KCD-A-07, LH-A-38, PM-A-12, PC-A-08, PC-A-09, PC-A-10, WG-A-10 |
| M4-09 | 3 | CM-A-27, PC-A-17, WG-A-11 |
| M4-10 | 11 | AT-R-11, BL-R-05, BL-R-07, CM-R-11, CM-R-13, KCD-R-09, KCD-R-10, LH-R-07, PM-R-09, PM-R-10, PC-R-10 |
| M4-11 | 3 | AT-A-06, LH-A-37, LH-A-41 |
| M4-12 | 4 | AT-A-16, CM-R-08, LH-R-08, LH-A-44 |
| M4-13 | 2 | CM-A-23, WG-A-07 |
| M4-14 | 2 | BL-A-10, LH-A-30 |
| M4-15 | 3 | AT-R-02, AT-A-13, CM-A-34 |
| M4-16 | 2 | CM-R-10, CM-A-30 |
| M4-17 | 4 | AT-A-09, PC-R-06, PM-A-17, WG-R-06 |
| M4-18 | 4 | AT-R-03, AT-R-04, AT-R-07, AT-R-08 |
| M4-19 | 4 | BL-R-01, BL-R-04, BL-R-06, BL-R-08 |
| M4-20 | 2 | CM-R-05, CM-A-12 |
| M4-21 | 3 | LH-R-04, LH-R-09, LH-A-42 |
| M4-22 | 3 | PM-R-04, PM-R-06, PM-R-12 |
| M4-23 | 3 | PC-R-04, PC-R-05, PC-R-08 |
| M4-24 | 3 | WG-R-04, WG-R-05, WG-A-13 |
| M4-25 | 7 | CM-A-06, CM-A-09, CM-A-10, CM-A-11, KCD-R-07, KCD-A-05, KCD-A-06 |
| M4-26 | 2 | PM-R-03, KCD-A-14 |
| M4-27 | 5 | AT-A-03, KCD-A-04, KCD-A-15, PM-A-08, WG-A-08 |
| M4-28 | 1 | KCD-A-16 |

`7+3+4+4+3+3+10+10+3+11+3+4+2+2+3+2+4+4+4+2+3+3+3+3+7+2+5+1 = 115` ✓

## Milestone 5 (5 findings across 3 items)

| Item | N | Findings |
|---|---|---|
| M5-01 | 3 | BL-A-16, CM-A-21, PC-A-11 |
| M5-02 | 1 | BL-A-01 |
| M5-03 | 1 | LK-A-13 |

---

# Part 5 — The Milestone-1 dependency proof

**Hard requirement:** nothing in Milestone 2 or later may depend on an upstream change that is not in
Milestone 1.

## Every upstream change is in M1

There are exactly three upstream repositories, and every change to each is enumerated in
`02_UPSTREAM_CHANGES.md` and listed in `04_EXECUTION_PLAN.md` under Milestone 1:

| Repo | M1 items |
|---|---|
| LibKa0s | M1-LK-01 … M1-LK-14 (14), plus the conditional M1-LK-15 |
| WowAddonStandards | M1-STD-01 … M1-STD-17 (17) |
| wow-addon plugin | M1-WA-01 … M1-WA-10 (10) |

**No work item in M2, M3, M4 or M5 touches WowAddonStandards or the `wow-addon` plugin.** LibKa0s appears
in `M3-01` (as the *source* of the re-vendor copy), in `M3-07` (whose scope is LibKa0s's **non-shipped**
paths — `docs/`, `tests/`, `testkit/` — and which is explicitly barred from `LibKa0s/*.lua`) and in
`M5-03` (as the subject of a recorded deferral, which changes nothing). It is never the source of an
upstream change outside Milestone 1.

An earlier draft stated this as "no M2–M5 item touches a file in any of those three repositories" and
"every M2–M5 item's Repo column names one of the eight roster addons", which four items falsified —
`M3-01`, `M3-07`, `M4-08` and `M5-03`. `M4-08`'s LibKa0s clause has since been **deleted**: it duplicated
`M1-LK-12`'s `README.md:196-231` edit across a milestone boundary with no finding behind it, since
`LK-A-11` maps to `M1-LK-12` only.

## Every M2+ upstream dependency resolves inside M1

| Item | Upstream dependency | Satisfied by |
|---|---|---|
| M2-01 … M2-09 | **none** | — (M2 is startable today) |
| M3-01 | the **v1.8.0 tag** carrying kit revision 8 **and** the new library bytes | **M1-LK-14** (which itself depends on M1-LK-01 … M1-LK-13) |
| M3-02 | `Kit.skip`, `vendor_sync.lua`, `testing-§11` scope | M1-LK-01, M1-LK-02, M1-STD-03 |
| M3-03, M3-03b | `Loader.xmlFiles`, `assertSuiteInventory`, `testing-§9` third list | M1-LK-03, M1-LK-04, M1-STD-10 (M3-03b additionally after M3-10) |
| M3-04 | `assertSurfaceParity`, `testing-§8` MUST, anti-pattern #56 | M1-LK-05, M1-STD-04 |
| M3-05 | index-mode rule and command edit | M1-STD-06, M1-WA-01 |
| M3-06 | checkpoint-qualified runner text, sweep 3f, `automated-tests-§4` MUST | M1-LK-07, M1-WA-02, M1-STD-05 |
| M3-07 | citation rule strength, widened sweep, bare-filename list | M1-STD-08, M1-STD-15, M1-WA-07 |
| M3-08 | register section and row shape, audit reads it | M1-STD-02, M1-WA-04 |
| M3-09 | `performance-§12` exemption, register (M3-08) | M1-STD-01 |
| M3-10 | kit adoptable as the harness | M1-LK-01 … M1-LK-05 (via M3-01) |
| M3-11 | CHANGELOG rule resolved, `bump-version` stops recreating it | M1-STD-09, M1-WA-09 |
| M3-12 | observed containment, reconciled bracket idiom | M1-LK-08, M1-STD-14 |
| M3-13 | published LAYOUT scalars | M1-LK-09 |
| M3-14a | swept library source, delivered by M3-01's **library-half** re-vendor | M1-LK-10 |
| M4-06 | *(prettychat half sequenced after M2-01; no upstream dependency)* | — |
| M4-09 | register section exists | M1-STD-02 (via M3-08) |
| M4-17 | terminal English-only state, register | M1-STD-13, M1-STD-02 |
| M4-25 | reconciled bracket idiom (via M3-12) | M1-STD-14, M1-LK-08 |
| M4-26 | parity cases exist (via M3-04) | M1-LK-05, M1-STD-04 |
| M4-27 | `events-frames-taint-§8` resolution chosen; under (b) also the varargs printer and its re-vendor | M1-STD-11; under (b) also **M1-LK-15** and M3-01 |
| M4-01…05, M4-07, M4-08, **M4-10**, M4-11…16, M4-18…24, **M4-28** | **none** | — |
| M5-01 | audit grading rule, which is itself inert without the playbook edit | M1-WA-03 → **M1-STD-17** |
| M5-02 | register section, plus the row landing in M3-08 | M1-STD-02, M3-08 |
| M5-03 | **none** (the rule already says it) | — |

Every **upstream** dependency in the right-hand column is an `M1-*` id. **No M2+ item depends on an
upstream change outside Milestone 1.** ✓ The three non-`M1-*` entries (`M3-03b` after `M3-10`, `M4-09`
and `M5-02` after `M3-08`) are intra-plan sequencing, not upstream changes; they are listed so the
ordering is not lost.

## One flagged conditional

`M1-STD-11` offers two resolutions for `events-frames-taint-§8`. Under option **(b)** — a varargs printer
in LibKa0s so the compliant form is no longer than the bypass — a **new LibKa0s item is required, and it
must be in Milestone 1**, not in M3. That item now exists: **`M1-LK-15`**, written into Group A and marked
CONDITIONAL, folding into `M1-LK-14`'s release. Without it, `M4-27` would schedule AbsorbTracker's 18
sites, PanelMaster's ~25, KickCD's `modules/Castbar_Debug.lua` and WhatGroup's two `pout` arms against a
library API with no item, no release and no vendoring step — breaking this plan's own hard rule by
construction.

**Every headline number in this bundle is an option-(a) number**, and they are labeled as such: 41 M1
items and 96 work items under (a); 42 and 97 under (b). `M4-27`'s effort is **S** under (a) (a re-grade and
a register row, code untouched) and **M–L** under (b) (~50 mechanical rewrites across four repos, after a
re-vendor). The fork should be resolved before Milestone 1 begins — `03_SPEC.md` § C11 records it as a
prerequisite.

---

# Summary

- **254 surviving findings. 254 mapped. 0 unmapped.**
- **0 Critical · 8 High · 30 Medium · 173 Low · 43 Info** — all mapped. (C6's ten rows were re-graded to a
  single severity in review; seven moved Medium → Low.)
- **96 work items across 5 milestones** — 97 under `M1-STD-11` option (b).
- **Dispositions, not just mappings:** 194 `fix`, 34 `rule-change`, 16 `register-row`, 5 decided upstream
  (`M4-27`), 5 `deferred`. Roughly **50 findings close without the cited code changing** — that is
  disclosed in Part 1's Disposition column and in Part 3, not buried under "5 deferred".
- **5 deferrals**, all Info, each with a written reason: `M5-01` (3), `M5-02` (1), `M5-03` (1).
- **All 8 Highs are in Milestone 2, which has no Milestone-1 dependency** and can start immediately.
- **Every upstream change is in Milestone 1**, and every M2+ upstream dependency resolves to an `M1-*` id.
- **Part 4 and `04_EXECUTION_PLAN.md`'s `Closes` column must agree.** A disagreement is the signal that a
  work item was split, merged or reordered without re-mapping — the failure mode a coverage proof cannot
  detect on its own, because it keeps reading 254/254 while pointing at an item that no longer does that
  work.
