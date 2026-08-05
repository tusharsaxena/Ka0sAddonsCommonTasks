# 06 — Execution Record

**The plan in this directory has been executed.** Written 2026-08-05, after the fact, against measured
state rather than against the plan's intent.

This document exists because `00_OVERVIEW.md` opens with "NOTHING HERE HAS BEEN RUN". That is no longer
true, and the correction belongs beside the claim rather than inside it — the other five documents are the
record of what was intended and are not rewritten.

---

## What was executed

All **96** work items, on branch `feat/2026-08-05-audit-review-remediation` in eleven repositories.
**201 commits.** No item was blocked or abandoned.

`M1-STD-11` was resolved by the owner as **option (a)** before Milestone 1 began, as `03_SPEC.md` § C11
requires. The MUST in `events-frames-taint-§8` is scoped to the APIs that can receive a combat-protected
value; the rest is a SHOULD. **`M1-LK-15` was therefore never created**, and `M4-27` was executed as a
disposition — the five findings closed by re-grading and a register row, with the cited call sites
untouched. The plan has 96 items, not 97.

| Milestone | Items | Repos |
|---|---|---|
| M1 — upstream | 41 | LibKa0s, WowAddonStandards, wow-addon |
| M2 — the eight Highs | 9 | 7 addons |
| M3 — adoption | 15 | 8 addons + LibKa0s |
| M4 — repo-local | 28 | 8 addons |
| M5 — recorded decisions | 3 | — |

| Repo | Commits |
|---|---|
| AbsorbTracker | 20 |
| BankLedger | 14 |
| ConsumableMaster | 26 |
| KickCD | 23 |
| LootHistory | 21 |
| PanelMaster | 19 |
| prettychat | 16 |
| WhatGroup | 18 |
| LibKa0s | 17 |
| WowAddonStandards | 17 |
| wow-addon | 10 |

---

## Measured end state

Every figure below was produced by re-running the suite after the last commit, not read from a report.

| Repo | tests, before → after | lint | lizard | working tree |
|---|---|---|---|---|
| AbsorbTracker | 470 → **487** | 0/0 | 0 warnings | clean |
| BankLedger | 726 → **724** | 0/0 | 0 warnings | clean |
| ConsumableMaster | 656 → **671** | 0/0 | 0 warnings | clean |
| KickCD | 737 → **752** | 0/0 | 0 warnings | clean |
| LootHistory | 579 → **594** | 0/0 | 0 warnings | clean |
| PanelMaster | 706 → **712** | 0/0 | 0 warnings | clean |
| prettychat | 255 → **260** | 0/0 | 0 warnings | clean |
| WhatGroup | 422 → **433** | 0/0 | 0 warnings | clean |
| LibKa0s | 480 → **498** | 0/0 | 0 warnings | clean |

**BankLedger is the one repo whose count fell**, and the plan sanctions exactly this movement: case counts
move only where a test referenced a removed symbol, and each move is explained. `M4-07` removed
`Compat.QualityFromLink` and `Insights.RankRows`/`BarFraction` as dead exported surface; the seven cases in
`tests/test_stats.lua` that referenced the two `Insights` helpers went with them. `M4-19` added one. Net −6.

### The plan's own "done" checklist

| Criterion | Result |
|---|---|
| All four suites green in all nine repos | **met** |
| `git ls-files -s tests/_kit/run-automated-tests.sh` → `100755` in all nine | **met** — index mode, never `ls -l` |
| `grep -rn "never fail a run"` returns only checkpoint-qualified sentences | **met** in all nine |
| Every finding id CLOSED or DEFERRED with a reason | **met** |
| No frozen bundle edited | **met** — `--diff-filter=M` over `docs/audits/` and `docs/reviews/` returns 0 in all nine; the only movement is the initial commit *adding* the previously-untracked 2026-08-05 bundles |
| `grep -rEn '§[0-9]+\.[0-9]'` outside the five paths → 0 in all nine | **not met as written — see below** |

Additionally verified, beyond the checklist:

- LibKa0s is tagged **v1.8.0** with `Kit.VERSION = 8`.
- All eight addons' `libs/LibKa0s/` **and** `tests/_kit/` are byte-identical to that tag (`diff -r` empty
  both ways, all sixteen pairs). No vendor-sync gate stands on a payload its repo does not hold.
- WowAddonStandards is at **v2.22.0**; `performance.md` carries §12 **appended**, so no `filename-§N`
  renumbered; anti-patterns run to **#56**; `AUDIT.md:91` grades by impact.
- **No addon repository was touched by a Milestone 1 item** (M1 exit criterion 8).

---

## Corrections to the plan, found by executing it

Recorded here rather than edited into the plan documents, which are the record of intent.

### 1. C15's acceptance is unachievable as written, for the same reason objection #11 identified

`M3-07` and `03_SPEC.md` § C15 require `grep -rEn '§[0-9]+\.[0-9]'` under the five exclusions to return
**0 in all nine repos**. It returns **0 in seven**. LootHistory returns **5** and LibKa0s returns **176**.

Every one of the 181 was opened. **None is a standards citation:**

- LootHistory's five are `§6.2`, `§6.3` and `§8.2` inside
  `docs/superpowers/specs/2026-07-25-insights-dashboard-ux-design.md`, cross-referencing **that document's
  own sections**.
- LibKa0s's are `docs/adoption/2026-08-01-v2/` (a dated frozen bundle whose rows reference its own §1, §3,
  §10.1), two `docs/superpowers/` plan and spec documents, one `(spec §5.2)` comment in
  `tests/fixture_options.lua`, and one **released `CHANGELOG.md` entry that quotes** the two
  `Ka0s standard §3.4` strings it records retiring — which `M1-LK-10` explicitly forbids sweeping.

This is structurally identical to blocking objection #11 in `00_OVERVIEW.md`: an acceptance criterion whose
only route to zero runs through frozen or historical evidence. The 368-site census counted raw `§N.M`
matches without separating standards citations from document-internal self-references.

**Disposition.** The substance of C15 is met — zero retired standards citations survive anywhere in the
collection, and the malformed and out-of-range references (`AbsorbTracker`'s `slash-commands-§:`,
BankLedger's `options-ui-§41`, `§190`, `§189`) were fixed by hand as MUSTs. The acceptance command should
read *"zero retired standards citations"*, and a future sweep needs a sixth exclusion for dated bundles
under `docs/adoption/` and `docs/superpowers/`, or a pattern that requires a `filename-` prefix.

### 2. `M1-LK-01`'s verification bullet contradicts `M1-LK-04`

`M1-LK-01`'s "Verified by" cell asks that `lua5.1 tests/run.lua` **still exit 0 after `rm` of a suite**.
That is the pre-`M1-LK-04` silent-skip behavior, which `M1-LK-04` deliberately reverses. After both items,
removing a declared suite exits **1**, naming the position — which is what `03_SPEC.md` § C12 and
`testing-§9` require. The bullet was treated as stale and the `M1-LK-04` behavior implemented.

### 3. `M3-02`'s skip-path check is unsafe under parallel execution

The acceptance step is `mv ../LibKa0s ../LibKa0s.bak`. With several repos adopting concurrently against the
same sibling checkout, that is a race that can redden an unrelated repo. The skip path was proven instead
by pointing the gate at a non-existent sibling in a scratch harness. Same assertion, no shared-state
mutation. A future plan should specify it that way.

### 4. `M1-LK-04`'s first implementation made `pending` unreachable

Not a plan defect — a defect the plan's own discipline caught. `Kit.assertSuiteInventory` initially demanded
every declared name exist on disk, which reddened the very entry whose purpose is to declare deliberate
absence. Found by a planted-violation probe, fixed by exempting `pending` entries from that direction only.
Recorded because it is the clearest evidence that the mandatory red-then-green step earns its cost.

---

## What is not done, and is not claimed

- **Every in-game smoke test remains an operator action.** Nothing here rests on a client session. The
  smoke steps in `04_EXECUTION_PLAN.md` — the reputation and guardian lines, KickCD's spell-name color,
  LootHistory's blacklist round-trip, WhatGroup's in-combat `/reload`, "no panel moves a pixel" for
  `M3-13` — are written as instructions and have not been performed.
- **The branch is not merged and not pushed** in any repository.
- **No release was cut for any addon.** LibKa0s v1.8.0 is the only tag, and it exists because Milestone 3
  could not begin without it.
- **The last "done" criterion is unverified by design**: *"a fresh `/wow-addon:standards-audit` in each of
  the eight addons produces a `02_DEVIATIONS.md` whose MUST tally is under five rows."* Running it is the
  honest test of this work, and it should be run after the branch is merged, not against it.
