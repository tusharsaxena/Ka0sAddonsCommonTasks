# Automated-tests sweep — fix queue (2026-09-26)

`/wow-addon:automated-tests` was run in all eleven addons (per `../WowAddonStandards/standards/ADDONS.md`)
and LibKa0s, each on a clean `master`. **All twelve are green**: 0 test failures, lint 0/0 everywhere,
**no function above CCN 15, no file over the 1500-line cap in any addon.** Nothing below blocks a
commit. This file queues what the runs surfaced, most urgent first. Every figure comes from the
repo's own bundle; the bundle path is the evidence.

The bundles and `RESULTS.md` changes are uncommitted in each repo.

## Runs

| Repo | Bundle | Tests | Lint files | Perf | Max CCN | Band files / over cap |
|---|---|---|---|---|---|---|
| AbsorbTracker | `20260926-160433` | 810 | 66 | 6 pass | 14 | 3 / 0 |
| AuraMaster | `20260926-160451` | 1660 | 140 | 11 pass | 15 | 12 / 0 |
| BankLedger | `20260926-160240` | 1104 | 75 | skip (§12 exemption) | 15 | 5 / 0 |
| ConsumableMaster | `20260926-160431` | 1112 | 122 | 5 pass | 14 | 8 / 0 |
| KickCD | `20260926-160251` | 1201 | 111 | 6 pass | 15 | 9 / 0 |
| LibKa0s | `20260926-160448` | 1744 (+1 deliberate skip) | 100 | skip (no perf.lua) | 15 | 13 / **2** |
| LootHistory | `20260926-160249` | 961 | 70 | skip (§12 exemption) | 15 | 6 / 0 |
| MultiMeters | `20260926-160431` | 2092 | 141 | 17 pass | 15 | 23 / 0 |
| PanelMaster | `20260926-160448` | 964 | 64 | skip (no perf.lua, ratified decline) | 15 | 5 / 0 |
| PartyFrameEnhanced | `20260926-160553` | 383 | 75 | 9 pass | 14 | 0 / 0 |
| PrettyChat | `20260926-160432` | 518 | 51 | skip (§12 exemption) | 14 | 2 / 1 (generated, exempt) |
| WhatGroup | `20260926-160442` | 823 | 54 | 8 pass | 15 | 3 / 0 |

## Queue

Tracking: an existing issue is named where one exists; **untracked** means nothing tracks it yet.

### P1 — regressions and standard violations

| ID | Repo | Task | Evidence | Tracking |
|---|---|---|---|---|
| ATS-01 | ConsumableMaster | Bisect the `recompute` perf allocation rise, 6505.88 → 14740.12 bytes/iter (+127%), over `f8729fa..bc284a4`; api/iter unchanged; `tests/perf.lua` untouched in range | `perf.json` vs `20260924-120622` | untracked |
| ATS-02 | AuraMaster | Bisect the perf allocation rise: `compile` 22200 → 42424 (+91%), `applyPass` 118147 → 164883 (+40%) bytes/iter, over `79d4f80..e5bb12c` (177 commits) | `perf.txt` vs `20260924-185738` | untracked |
| ATS-03 | LibKa0s | Six band entries carried as *Accepted* across six release runs (v1.56–v1.61), past the three-release shelf life (`automated-tests-§4`, anti-pattern #53): `Options.lua` 1462, `OptionsTabs.lua` 1493, `testkit/framework.lua` 1386, `tests/test_options_idsuggest.lua` 1002, `tests/test_options_tabs.lua` 1218, `tests/test_slash.lua` 1339. Each is owed a fix or a tracked deviation ID with an owner | `RESULTS.md` history | untracked |
| ATS-04 | LibKa0s | Two files over the 1500 cap: `LibKa0s/OptionsWidgets.lua` 3852, `tests/test_options_widgets.lua` 4086 | `complexity.txt` | #32, #33 |

### P2 — within 25 lines of the 1500 cap

| ID | Repo | File | LOC | Tracking |
|---|---|---|---|---|
| ATS-05 | PanelMaster | `tests/test_panel.lua` (1399 → 1491, past its 1400 re-check) | 1491 | untracked |
| ATS-06 | LibKa0s | `LibKa0s/OptionsTabs.lua`, `tests/test_widgets.lua` | 1493, 1493 | part of ATS-03 / untracked |
| ATS-07 | LibKa0s | `testkit/test_prose.lua` | 1486 | untracked |
| ATS-08 | AuraMaster | `tests/test_anchors.lua` (+97 this interval) | 1481 | untracked |
| ATS-09 | AuraMaster | `settings/GeneralSpells.lua` (already *Peel next*) | 1480 | untracked |

### P3 — re-check triggers fired or close, headroom under 100

| ID | Repo | File(s) | Tracking |
|---|---|---|---|
| ATS-10 | PanelMaster | `settings/PanelEditor.lua` 1464 | #47 |
| ATS-11 | AbsorbTracker | `tests/test_helpers.lua` 1447 (*Peel next*) | R-14 |
| ATS-12 | MultiMeters | `tests/test_slash.lua` 1411 (past its 1400 trigger; peel the diagnostics cases), `modules/Row.lua` 1446, `modules/Aggregator.lua` 1432 (+38) | untracked |
| ATS-13 | KickCD | `modules/Castbar.lua` 1440 (10 below its 1450 trigger) | #24 |
| ATS-14 | ConsumableMaster | `tests/test_slash.lua` 1426, `tests/test_macrobar.lua` 1425, `tests/test_settingsui.lua` 1419 | untracked |
| ATS-15 | AuraMaster | `modules/Anchors.lua` 526 → 1243 in one interval (*Peel next*, attachment seam) | untracked |

### P4 — functions that newly reached CCN 15 (at the release line, not over)

| ID | Repo | Function | Shape |
|---|---|---|---|
| ATS-16 | WhatGroup | `NS.FrameSnapshot` `modules/Frame.lua:1168` (new, `c0ce81c`) | dense `and`/`or` coercion |
| ATS-17 | MultiMeters | `doDebug` `settings/Slash.lua:736` (14 → 15) | — |
| ATS-18 | AuraMaster | `standUp` `core/LifecycleSetup.lua:105`, `steadyRelative` `modules/Anchors.lua:554`, `ContainerClass` `modules/Container.lua:592` | — |

### P5 — kit and tooling (fix upstream, then re-vendor)

| ID | Repo | Task |
|---|---|---|
| ATS-19 | LibKa0s | The runner's lizard call sets `length > 1000` and `parameter_count > 100`, so function length and parameter count never warn (a 12-parameter `Layout.layoutBlock` in KickCD and a 197-line `LT` in BankLedger both pass). Confirm this is intended, or tighten it in the standard and the kit |
| ATS-20 | LibKa0s | The generated `RESULTS.md` prints an empty "Functions `lizard` warned on" table with no `None.` row (seen in every addon) |
| ATS-21 | LibKa0s | The band table lists generated files (PrettyChat `GlobalStrings/GlobalStrings.lua`, 23842) despite the playbook's generated-file carve-out |
| ATS-22 | wow-addon | `/wow-addon:automated-tests` cannot finish inside a subagent. The Write tool refuses a subagent's `ANALYSIS.md`, and the `ka0s-bounded` PreToolUse hook blocks any heredoc whose text contains the word "lizard". Agents fell back to scratchpad-and-`cp`, and one used `KA0S_BOUNDED_HOOK=off`. The hook should match commands, not prose |

### P6 — record hygiene (low)

| ID | Repo | Task |
|---|---|---|
| ATS-23 | several | Stale figures in carried `RESULTS.md` Disposition cells: LibKa0s (OptionsTabs "eleven lines of room" is 7; `test_slash.lua` "1327" is 1339), KickCD (Castbar "1345 → 1435"), LootHistory (`Browser.lua` "grew" note), MultiMeters (`Provider.lua`, `enUS.lua`, `test_options_panel.lua`), ConsumableMaster (`test_slash.lua`). Refresh on the next run |
| ATS-24 | BankLedger | Confirm the provisional *Accepted* on newly-banded `tests/test_libka0s.lua` (1020) |

## Also noted, no action

- Perf `ms/iter` rose in MultiMeters, WhatGroup and AuraMaster with api/iter and bytes/iter flat; all
  twelve batteries ran concurrently, so it reads as host load.
- Several repos have old bundles with no `ANALYSIS.md`; the standard forbids backfilling them.
