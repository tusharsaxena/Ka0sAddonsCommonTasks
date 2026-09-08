# MultiMeters CCN / LOC remediation — 2026-09-09

**Repo under change:** `../MultiMeters` — branch `feat/2026-09-09-ccn-loc-remediation`
**Plan repo:** `Ka0sAddonsCommonTasks` — branch `feat/2026-09-09-ccn-loc-remediation`

## The target, stated once

Two numbers, both from the standard rather than from any one issue:

- **CCN.** `automated-tests-§3` *The release gate*: `complexity` passes with **no function above CCN 15**,
  measured by `lizard -l lua -x "./libs/*" -x "./tests/_kit/*" .`. Baseline: **23 warnings**.
- **LOC.** `layout-§1`: every **authored** `.lua` the repo tracks is capped at **1500 lines**
  (`tests/` included; `libs/` and `tests/_kit/` are the only carve-outs). Baseline: **15 files over**.

The GitHub issues (#27–#45) cover 11 of the 23 CCN warnings and 8 of the 15 LOC breaches. The
standard binds all of them, so the work list is the measurement, not the issue list. The extra
twelve get fixed under the same rules and their issues get filed as they land.

## The constraint that shapes every item

`performance-§11` — *Acting on a complexity finding*:

1. Permitted shapes only: module-level table dispatch; a **named** file-local helper; a data table
   plus one loop; splitting a builder into N builders.
2. **MUST NOT** move a body wholesale into `doTheRest`-style helper to make the wrapper score well.
3. **MUST NOT** allocate per call — every dispatch/defaults table is built once at file scope.
4. **MUST NOT** change behaviour, including fixing a bug noticed on the way.
5. **MUST NOT** drop a comment that records *why* — especially one recording a past bug.
6. **MUST** pin behaviour with a characterization test first where the function has no coverage,
   and run it against the **unrefactored** code.

`layout-§1` peels: 2–3 sibling files in the same folder, seam as named in the issue.

## Baseline (2026-09-09, at `c08c0dc`)

- `lua tests/run.lua` — **1534 passed, 0 failed, 0 skipped**
- `luacheck .` — **0 warnings / 0 errors in 94 files**
- `lizard` — **23 warnings**
- files over 1500 — **15**

## Ordering, and why

**CCN before LOC.** A peel moves functions between files and invalidates every `path:first-last` in
the complexity register; doing CCN first empties that register before the peels churn it. It is also
what issue #30 asks for in as many words — the peel and the complexity disposition "are two
decisions and should not arrive in one commit".

**Source peels before test peels**, because a test peel follows the module peel it mirrors.

**The TOC and `tests/run.lua` suite list are serialized.** Parallel agents never edit them; each
peel agent reports the line it needs and the orchestrator applies it between waves.

---

## Phase 1 — CCN (23 items → 0 warnings)

One agent per **file**, so no two agents write the same file. Files are independent.

| ID | Function (real name) | File | CCN | Issue |
|---|---|---|---|---|
| C-01 | `migrations[1]` (lizard: `]@270-296`) | `core/Database.lua` | 16 | — |
| C-02 | `migrations[4]` (lizard: `]@372-401`) | `core/Database.lua` | 17 | — |
| C-03 | `migrations[12]` (lizard: `]@659-684`) | `core/Database.lua` | 16 | — |
| C-04 | `reportDeathDating@648-689` | `core/Diagnostics.lua` | 25 | — |
| C-05 | `reportFeignRoster@1738-1761` | `core/Diagnostics.lua` | 17 | — |
| C-06 | `scanColumn@1462-1565` | `modules/Aggregator.lua` | 34 | #35 |
| C-07 | `DrillDown:OnCellClick@395-428` | `modules/DrillDown.lua` | 18 | — |
| C-08 | `Export.ChatLines@535-600` | `modules/Export.lua` | 27 | #36 |
| C-09 | `onPrintToChat@1432-1497` | `modules/Export.lua` | 16 | — |
| C-10 | `Feign.Prune@247-337` | `modules/Feign.lua` | 25 | #37 |
| C-11 | `Format.DeathTime@646-665` | `modules/Format.lua` | 19 | — |
| C-12 | `onClick@322-372` | `modules/HeaderControls.lua` | 24 | #38 |
| C-13 | `build@249-366` | `modules/Roster.lua` | 20 | — |
| C-14 | `Cell:ApplyBorder@659-739` | `modules/Row.lua` | 30 | #39 |
| C-15 | `Cell:ApplyIcons@1168-1244` | `modules/Row.lua` | 19 | — |
| C-16 | `eventColumns@1866-1919` | `modules/Tooltip.lua` | 19 | — |
| C-17 | `drawDeathEvents@1957-2039` (lizard: `(anonymous)@1968-2039`) | `modules/Tooltip.lua` | 26 | #40 |
| C-18 | `Tooltip:CellTooltip@2342-2404` | `modules/Tooltip.lua` | 20 | — |
| C-19 | `Visibility.ShouldShow@239-276` | `modules/Visibility.lua` | 23 | #41 |
| C-20 | `WindowProto:BuildLayout@312-413` | `modules/Window.lua` | 24 | #42 |
| C-21 | `place@1283-1415` (133 lines) | `modules/Window.lua` | 18 | #43 |
| C-22 | `NS.ReorderableBlocks@227-322` | `settings/ColumnBlocks.lua` | 28 | #44 |
| C-23 | `doDebug@434-505` | `settings/Slash.lua` | 25 | #45 |

Wave shape: 15 file-agents in parallel → verify (`luacheck`, `lua tests/run.lua`, `lizard`) →
adversarial behaviour-preservation review per changed file → repair loop until lizard reports
**0 warnings** and the suite is green → one commit per file.

## Phase 2 — LOC (15 files → 0 over cap)

| ID | File | Lines | Issue | Seam (from the issue, or named here) |
|---|---|---|---|---|
| L-01 | `settings/Schema.lua` | 3080 | #27 | path machinery + read/write seams → `settings/Schema_Paths.lua` |
| L-02 | `tests/test_window.lua` | 2737 | — | mirrors L-05 |
| L-03 | `tests/test_tooltip.lua` | 2708 | — | mirrors L-04 |
| L-04 | `modules/Tooltip.lua` | 2659 | #28 | the four builders → `modules/Tooltip_Builders.lua` |
| L-05 | `modules/Window.lua` | 2650 | #29 | header art, sort hand-off, segment selector → `modules/Window_Header.lua` |
| L-06 | `tests/wow_mock.lua` | 2270 | #34 | `tests/mock_secrets.lua` + `tests/mock_frame.lua`, `dofile`d |
| L-07 | `modules/Aggregator.lua` | 2083 | #30 | identity mode + correlation rectangle → `modules/Aggregator_Identity.lua` |
| L-08 | `core/Diagnostics.lua` | 1824 | #31 | one file per long-lived probe |
| L-09 | `modules/Export.lua` | 1748 | #32 | the modal → `modules/Export_Modal.lua` |
| L-10 | `modules/Row.lua` | 1715 | #33 | the name cell → `modules/Row_NameCell.lua` |
| L-11 | `tests/test_row.lua` | 1606 | — | mirrors L-10 |
| L-12 | `tests/test_aggregator.lua` | 1605 | — | mirrors L-07 |
| L-13 | `tests/test_diagnostics.lua` | 1583 | — | mirrors L-08 |
| L-14 | `tests/test_schema.lua` | 1573 | — | mirrors L-01 |
| L-15 | `tests/test_export.lua` | 1509 | — | mirrors L-09 |

Serialized surfaces the orchestrator owns, never an agent:

- `MultiMeters.toc` — one new line per source peel, in the right load position.
- `tests/run.lua` — the suite list, one new entry per test peel.
- `docs/ARCHITECTURE.md` — the cap census and the complexity register.

## Phase 3 — the bookkeeping the two gates force

- **`tests/test_layout_cap.lua` and `tests/test_complexity_register.lua` have an empty-state bug.**
  Each fails if its ARCHITECTURE.md section is missing, *and* fails if the section's table has no
  rows while telling you to "delete the section rather than leaving an empty table". Both states are
  red once the last breach is gone. The suites must be amended to accept the terminal state they
  were written to drive the repo toward: no section **and** no breach is green; a section with no
  rows, or a breach with no section, stays red.
- `docs/ARCHITECTURE.md` — remove both registers, retire their prose.
- `docs/complexity.md` — regenerate (`performance-§10` invocation, generated-file header).
- `docs/automated-tests/` — a fresh bundle via `/wow-addon:automated-tests`, plus `RESULTS.md`.
- `docs/module-map.md`, `docs/testing.md`, `docs/test-cases.md` — the new files.
- Close issues #27–#45 as `state:done`; file issues for the twelve CCN warnings and seven LOC
  breaches that had none, then close those too (the collection's record is the issue store).

## Phase 4 — finalize

`/wow-addon:finalize` once every gate is green: lint 0, suite green, lizard 0 warnings, 0 files
over 1500.

---

## Checkpoint log

Each checkpoint is a commit on `feat/2026-09-09-ccn-loc-remediation` in `../MultiMeters`. To resume:
read this log, `git log --oneline` on that branch, then re-measure — the measurement, not this file,
is the authority on what is left.

| # | Checkpoint | State | Commit |
|---|---|---|---|
| CP-0 | Branch cut, plan written, baseline measured | done | `b7b7f0c` (plan repo) |
| CP-1a | 194 characterization tests, run against unrefactored code — 1728 green | done | `77d0723` |
| CP-1b | 23 lizard warnings to **0**; suite 1728 green, lint 0/0 | done | `7d86d8e` |
| CP-1c | Repair of the 6 files the adversarial review flagged | pending | — |
| CP-2 | Phase 2 source peels landed (L-01, L-04, L-05, L-07, L-08, L-09, L-10) | pending | — |
| CP-3 | Phase 2 test peels landed (L-02, L-03, L-06, L-11…L-15) | pending | — |
| CP-4 | Phase 3 registers, gates and docs | pending | — |
| CP-5 | Phase 4 finalize | pending | — |

## Resume procedure

```bash
cd ../MultiMeters
git checkout feat/2026-09-09-ccn-loc-remediation
lizard -l lua -x "./libs/*" -x "./tests/_kit/*" . | tail -40      # what CCN is left
git ls-files '*.lua' | grep -v '^libs/' | grep -v '^tests/_kit/' \
  | xargs wc -l | sort -rn | awk '$1>1500'                        # what LOC is left
lua tests/run.lua | tail -3 && luacheck . | tail -2               # is the tree green
```

Anything the two measurements still report is unfinished, regardless of what the checkpoint table
says.

## Workflow run log (for `resumeFromRunId`)

| Wave | Run ID | Script |
|---|---|---|
| Phase 1a — characterization | `wf_68cf9ad3-cd4` | `multimeters-characterization-wf_68cf9ad3-cd4.js` |
| Phase 1b — CCN refactor + adversarial verify | `wf_5ea3abae-aa4` | `multimeters-ccn-refactor-wf_5ea3abae-aa4.js` |
| Phase 1c — regression repair + re-verify | `wf_3d2f3a00-aca` | `multimeters-ccn-repair-wf_3d2f3a00-aca.js` |

Scripts live under the session's `workflows/scripts/` directory; resume with
`Workflow({scriptPath, resumeFromRunId})`.
