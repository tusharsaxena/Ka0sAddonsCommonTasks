# 2026-10-01 GitHub issue pass

The owner went through every open issue in the collection, using the 2026-09-30 dump, and wrote a
decision in column S (`ACTION`) of `inputs/owner-decisions-2026-09-30.csv`. This bundle acts on the
**39 rows that carry a decision** and on nothing else. The other 74 open issues are out of scope for this
cycle.

## Reading order

| File | What it holds |
|---|---|
| `00_OVERVIEW.md` | This page: scope, what was closed up front, decisions taken, milestones |
| `01_REQUIREMENTS.md` | The consolidated requirements: one row per actioned issue with verdict, requirement and acceptance |
| `02_SPEC.md` | The cross-cutting spec: the LibKa0s v1.66.0 contents, standard v2.74.0, the sighted complexity gate, sequencing, conventions |
| `02a_ISSUE_DESIGNS.md` | Per-issue evidence and design from the validation pass (generated from `plan-data/validation.json`) |
| `03_EXECUTION_PLAN.md` | Milestones, items, how they run, checkpoints. **Frozen once execution starts** |
| `04_SMOKE_TESTS.md` | The in-client checks the owner runs. Results are recorded there |
| `RESUME.md`, `resume-state.sh`, `items.tsv`, `checkpoints.tsv`, `exceptions.tsv` | Resumable state: git is the only state |
| `99_REPORT.md` | Execution record (written at the end) |

## The 39 decisions, after validation

Validation (`plan-data/validation.json`) was six read-only agents, one per repo group. They checked every
issue against the code at the v1.65.0 merges.

| Outcome | Issues |
|---|---|
| **Closed up front on the owner's word** (4) | AbsorbTracker#10, KickCD#7 (closed as no longer reproducing; a follow-up comment records that the proposed code fix was never applied), PrettyChat#1 and #5 (will not do) |
| **Already addressed, closed** (4) | LibKa0s#17, #18, #19, #20. The selection-invariance cases exist and are red-verified in LibKa0s's own `test_options_tabs.lua`. The kit-wide `GetHeight` flip is retired, and kit 35 rewrites the stale comment |
| **Already addressed, pin then close** (1) | AbsorbTracker#20. SetRenderer's hidden-panel gate (`5c03fb8`) does what the issue asked. GI-AT-01 adds the regression pin and closes it |
| **Partially addressed, finish** (4) | KickCD#24 (Castbar regrew to 1251 after its first peel), KickCD#10 (the host side no longer needs `parent`, but RenderGrid's spacer still blocks it), PartyFrameEnhanced#12 (now 3.6 B/iter, not yet attributed), WowAddonStandards#6 (fixed in AuraMaster only) |
| **Not addressed, build** (26) | Everything else (see `01_REQUIREMENTS.md`) |

## What validation found that changes the size of the work

**WowAddonStandards#6 is broader than `#`.** lizard 1.24.0's Lua reader subclasses its Ruby-like reader.
So bare `it`, `class`, `module`, `begin` and `unless` also derail it, alongside `#` read as a C
preprocessor line. Across the collection about 1,600 functions go unmeasured. Measured sighted, **29 functions
sit above CCN 15** today, in LibKa0s (7), MultiMeters (8), LootHistory (5), BankLedger (4), KickCD (3) and
ConsumableMaster (2). The owner's "fix now" includes the issue's proposal 4 (re-run the gate across the
collection). Fixing the measurement and leaving the gate red would contradict that, so refactoring those
29 functions is in scope (decision D3).

## Decisions taken (owner asked for best judgement; none needed escalation)

| # | Decision | Why |
|---|---|---|
| D1 | One LibKa0s release, **v1.66.0**, carries every library change. One re-vendor wave reaches all eleven addons | A release per issue would mean eleven re-vendors per release |
| D2 | Fix lizard's blindness by measuring a **sanitized shadow** of the tree (kit 35, `testkit/lizard_sighted.lua`) with a function-count parity check, not by rewriting about 2,800 hazard lines | The rewrite would have to be redone forever; the shadow fixes the tool once for every consumer |
| D3 | Refactor every function the sighted gate reveals above CCN 15, characterization tests first | It is what proposal 4 implies, and it keeps every release gate green |
| D4 | LibKa0s#7 peels the **command surface** (`PerfCommands.lua`), not the sampler the issue named | The sampler needs about ten closure locals threaded through; the command surface's dependencies are all passable. The issue allows the seam to be chosen |
| D5 | LibKa0s#1 budgets are **report-only**: per-bucket ms/s plus per-call maxMs, with the mechanism in the lib and the values in each host's descriptor. No CI gate and no delta-ms-per-frame | Matches the 2026-08-24 perf-thresholds analysis. In-game captures are noisy and offline counters already gate releases |
| D6 | KickCD#10 and AbsorbTracker#32 get **opt-in** library options (`RenderGrid` `parent` + `opts.gap`; `RenderTabbedSchema` `untabbedSkipRender`, `disabledReplaces`, `rerender`). RenderGrid does not auto-`DoLayout`; the asymmetry is documented | A global change breaks BankLedger, LootHistory and AuraMaster (skipRender groups), and auto-layout adds passes in seven addons |
| D7 | LibKa0s#9 delivers the **census and documentation** now. Host adoptions it uncovers are filed as issues, not executed | The issue asks for measurement. `-1.0` is additive-only, so nothing is deleted |
| D8 | PanelMaster#54 adopts option (a) host-side. Debug `[Set]` lines for panel writes take the library's shape (`[Set] panel.width = 300 on 'Alpha'`) | One write seam, one line shape. The owner's "fix now" reverses the 2026-09-24 keep |
| D9 | PartyFrameEnhanced#3 wraps lazily, out of combat, only for re-sorting providers, with the fade kept as fallback. Stand-down residue (a gated wrap left in place when ours is not outermost) becomes a Documented-deviations row under slash-commands-§7. **#3 stays open until the owner's in-client combat checks pass** | Secure code cannot be proven offline |
| D10 | ConsumableMaster#16 (not in the CSV) is closed by GI-CM-01, because LibKa0s#40's fix exists to unblock it | It is the consumer half of an actioned issue |
| D11 | Issues fixed on the feature branches get a comment naming the commit and are **closed at finalize**, once merged on the owner's go-ahead. Issues found already addressed were closed immediately | A fix on an unmerged branch is not shipped yet |
| D12 | "Push to master after major milestones, but do not merge" is read as **push the feature branches** at each milestone checkpoint. Nothing reaches `master` without the owner's go-ahead | That is the only reading consistent with "do not merge", and it matches CLAUDE.md |
| D13 | No addon version bump, no pushed tag. The LibKa0s v1.66.0 tag is local until finalize | CLAUDE.md |

## Milestones

| M | What | Items |
|---|---|---|
| M0 | This bundle | GI-PLAN-01 |
| M1 | LibKa0s v1.66.0 (kit 35), standard v2.74.0, wow-addon | GI-LK-01…12, GI-STD-01, GI-PLUG-01 |
| M2 | Re-vendor into all eleven addons, plus every addon-side issue | GI-<XX>-RV ×11, then 29 addon items |
| M3 | LibKa0s#9 census, record, issue comments, push | GI-LK-13, GI-FIN-01 |

Branch everywhere: `feat/2026-10-01-github-issue-pass`.
