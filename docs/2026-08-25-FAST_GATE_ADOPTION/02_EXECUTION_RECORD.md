# Fast-gate adoption — execution record

Executed 2026-08-25 across the nine addons in
[`ADDONS.md`](../../../WowAddonStandards/standards/ADDONS.md). The measurements this record acts on
are in [`01_MEASUREMENTS.md`](01_MEASUREMENTS.md).

Nothing was pushed and no addon version was bumped, per the prompt's closing instruction.

## What changed, per repo

| Repo | Change |
|---|---|
| ConsumableMaster | `tests/run.lua` — memoised `resolve()`; README test badge 693 → 698 |
| BankLedger | README test badge 781 → 791; `docs/smoke-tests.md` menu-dismissal step corrected |
| KickCD | README test badge 774 → 780 |
| LootHistory | `docs/smoke-tests.md` — two menu-dismissal steps corrected |
| MultiMeters | `docs/smoke-tests.md` — menu-dismissal step corrected |
| AbsorbTracker, PanelMaster, PrettyChat, WhatGroup | automated-test bundle only |

All nine also gained a fresh `docs/automated-tests/<stamp>/` bundle and a `RESULTS.md` row.

Nothing under `tests/_kit/` or `libs/` was touched in any repo. The one source-tree change in the
collection is Consumable Master's `resolve()`, which is per-addon test scaffolding, not kit code.

### The badges were stale; the inventories were not

Three repos' README badges disagreed with their suites — BankLedger at 781 against 791, Consumable
Master at 693 against 698, KickCD at 774 against 780. `docs/test-cases.md` was regenerated in all
three with `lua tests/run.lua --list`; in all three it came back **byte-identical**, so the
inventory had been kept current and only the badge had drifted. Badges corrected, inventories
unchanged.

## Step 6 — the smoke test for the library jump

Three repos consume `LibKa0s-Widgets-1.0` outside `libs/` and `tests/`: **BankLedger**,
**LootHistory** and **MultiMeters**. The other six do not, so step 6 does not apply to them and
nothing was added to their smoke tests.

In those three the step turned out not to be "add a check". Each already had a check on this exact
behaviour, and each **documented the pre-v1.13.0 defect as the expected result**:

- `BankLedger/docs/smoke-tests.md` item 4 — "the menu closes and the click does **not** land on the
  modal … which is what makes the outside click reach the catcher first."
- `LootHistory/docs/smoke-tests.md` item 3 — "the click does not land on the History window … below
  the menu's catcher."
- `MultiMeters/docs/smoke-tests.md`, the Export selectors — "It closes and the click does **not**
  land on the modal behind it."

LibKa0s v1.13.0 (Widgets minor 5) removed that full-screen click catcher, and all three repos
vendor v1.15.0, so all three steps now instruct a tester to confirm behaviour the library no longer
has — a smoke test that fails when the addon is correct. Each was rewritten to the current
contract: one press both dismisses the menu and reaches what is under the cursor, and a right-click
does the same.

LootHistory carried a fourth, longer instance. Its item 10 explained the asymmetry at length —
that the library's catcher "takes only `LeftButtonUp`", that a right-click over an open filter menu
"is swallowed with no handler", that the tester should "expect one *left*-click to dismiss the
filter menu before the right-click lands" — and closed with "Reported upstream as a `Widgets` gap;
do not patch `libs/` here." That report is what became the v1.13.0 fix. The step now checks the
fix instead of the gap: with a filter dropdown open, a right-click on a table row closes the menu
and raises the row actions on the same press, and needing two presses is a regression.

The corrected wording was checked against `libs/LibKa0s/Widgets.lua` in each repo, not against the
changelog alone — the source comment at the dismissal site states it directly: *"One press now both
dismisses the menu and does the thing the player pressed on."*

**Still owed: the in-client run.** These are smoke tests, and headless suites cannot see click
routing. The three corrected steps have not been executed in the client; only the instructions have
been brought back in line with the shipped library.

## Step 5 — the recorded runs

`tests/_kit/run-automated-tests.sh` was run in all nine repos, serially.

| Repo | Version | Lint | Tests | Perf | Complexity | Verdict |
|---|---|---|---|---|---|---|
| AbsorbTracker | 1.9.0 | 0/0 | 508/508 | pass | 0 warn, max CCN 14 | green |
| BankLedger | 1.0.0 | 0/0 | 791/791 | skip | 0 warn, max CCN 15 | green |
| ConsumableMaster | 1.5.0 | 0/0 | 698/698 | pass | 0 warn, max CCN 15 | green |
| KickCD | 1.2.1 | 0/0 | 780/780 | pass | 0 warn, max CCN 15 | green |
| LootHistory | 1.2.0 | 0/0 | 644/644 | skip | 0 warn, max CCN 15 | green |
| MultiMeters | 0.1.0 | 0/0 | 1257/1257 | **fail** | **19 warn, max CCN 31** | **amber** |
| PanelMaster | 1.0.0 | 0/0 | 731/731 | skip | 0 warn, max CCN 15 | green |
| PrettyChat | 1.4.0 | 0/0 | 271/271 | skip | 0 warn, max CCN 12 | green |
| WhatGroup | 1.3.0 | 0/0 | 485/485 | skip | 0 warn, max CCN 15 | green |

The five `skip`s are repos that ship no `tests/perf.lua`. A skip is not a pass, and at the release
gate it is not evaluated — that is a standing gap in those five, unchanged by this work and not
introduced by it.

### Multi Meters' amber is inherited, and here is the evidence

Both reasons are present, unchanged, in that repo's **previous** run — `20260825-021705`, its own
fast-gate adoption run, taken before any of today's work:

| | Perf | CCN warnings | Max CCN | Verdict |
|---|---|---|---|---|
| `20260825-021705` (previous) | fail | 19 | 31 | amber |
| `20260825-103437` (this run) | fail | 19 | 31 | amber |

The two failing perf assertions are byte-identical across the two runs, down to the measured
allocation:

```
- a restricted pass allocated 447916 bytes/iter, over the 436000-byte ceiling — identity correlation grew
- a dormant pass allocated 351313 bytes/iter, over the 336000-byte ceiling — one refresh of this window grew
```

The only change made to that repo today is one paragraph of `docs/smoke-tests.md`, which cannot
move an allocation count or a cyclomatic complexity figure. The amber is pre-existing and is
reported as inherited, not as caused here. It remains a real thing that repo owes work on: at the
tag, `automated-tests-§3` gates on all four suites at `pass` plus zero functions above CCN 15, so
Multi Meters cannot currently be released without addressing both.

## What was deliberately not done

- **`--jobs` was not switched on anywhere**, because every gate is now under 10 seconds. See
  [`01_MEASUREMENTS.md`](01_MEASUREMENTS.md).
- **No sharded-run verification was performed**, because nothing opted in. The prompt's
  serial-versus-sharded diff is a precondition for adopting `--jobs`, not an exercise to run for
  its own sake, and a suite that never shards cannot reveal an inter-suite dependency. Whether
  these nine suites are shard-clean is therefore still unknown.
- **No re-vendor**, because every repo already carried v1.15.0 and both payloads matched the tag.
- **No push and no version bump**, per the prompt.
- **No in-client smoke run** for the three corrected menu checks.
