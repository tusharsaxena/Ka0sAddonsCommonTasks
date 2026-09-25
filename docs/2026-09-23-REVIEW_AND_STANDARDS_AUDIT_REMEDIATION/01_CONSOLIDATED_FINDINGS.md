# 01 — Consolidated Findings

**436 verified findings** from the 2026-09-23 `/wow-addon:review` and `/wow-addon:standards-audit` runs over LibKa0s and the eleven addons, after adversarial re-verification against the code. 3 were rejected and are listed at the end.

Severity and remediation are the **post-verification** values; `verdict` says whether the verifier confirmed the finding as written or corrected it. Source bundles: `<Repo>/docs/reviews/2026-09-23/` and `<Repo>/docs/audits/2026-09-23/`. Machine-readable copy: `inputs/findings/<Repo>.json`.

## Totals

| Repo | critical | high | medium | low | info | total | upstream-routed |
|---|---|---|---|---|---|---|---|
| LibKa0s | 0 | 1 | 3 | 21 | 4 | 29 | 0 |
| AbsorbTracker | 0 | 1 | 6 | 23 | 11 | 41 | 9 |
| AuraMaster | 0 | 1 | 2 | 26 | 5 | 34 | 5 |
| BankLedger | 0 | 1 | 4 | 19 | 8 | 32 | 1 |
| ConsumableMaster | 0 | 0 | 4 | 29 | 4 | 37 | 5 |
| KickCD | 0 | 1 | 7 | 31 | 7 | 46 | 4 |
| LootHistory | 0 | 2 | 3 | 33 | 4 | 42 | 4 |
| MultiMeters | 0 | 3 | 2 | 23 | 5 | 33 | 2 |
| PanelMaster | 0 | 2 | 4 | 19 | 3 | 28 | 3 |
| PartyFrameEnhanced | 0 | 2 | 3 | 26 | 6 | 37 | 5 |
| PrettyChat | 0 | 1 | 4 | 30 | 3 | 38 | 6 |
| WhatGroup | 0 | 1 | 3 | 31 | 4 | 39 | 6 |
| **all** | **0** | **16** | **45** | **311** | **64** | **436** | **50** |

## Suite state as measured on 2026-09-23

- **LibKa0s** — Measured at 46ccaa6 (clean) against standard v2.64.0, via ~/.claude/wow-addon/bin/ka0s-bounded by absolute path (not on PATH; no 124/137 exits). luacheck: pass, 0 warnings / 0 errors over 81 files. Headless tests (lua5.1 tests/run.lua): pass, 1484 passed / 0 failed / 1 skipped (1485 total); skip is the declared decline of tests/_kit/test_prose.lua (register row 3). Fresh --list inventory byte-identical to docs/test-cases.md. Perf: skipped, no tests/perf.lua (library repo). lizard: pass, 0 warnings, max CCN 15 (4 functions at exactly 15), 30419 NLOC, 4248 functions, avg CCN 2.0, identical to release bundle 20260923-144526. make test: skipped (no Makefile). Kit sync (testkit vs tests/_kit): empty diff; kit revision 25. Downstream vendor sync: all 11 consumers byte-identical for libs/LibKa0s and tests/_kit. Line endings: canonical .gitattributes, 0 stragglers. Cross-addon: 22 unique slash r
- **AbsorbTracker** — Both runs at 8f64eb6 on feat/2026-09-23-review-audit-remediation. Standard: v2.64.0 (2026-09-23), all 27 sections. Every run used ~/.claude/wow-addon/bin/ka0s-bounded; it is not on PATH, and the timeout 900 fallback was never used. luacheck: 0 warnings / 0 errors in 61 files (28 source + 33 test). Headless suite (lua5.1 tests/run.lua): 710 passed / 0 failed / 0 skipped. A fresh --list matches docs/test-cases.md, and the README badge reads 710/710. Offline perf (tests/perf.lua): ran with exit 0 and every assertion held. api/iter · bytes/iter: absorbEvent 0.0·0.0; paintPass 12.0·48.0; appearancePass 48.0·97.8; settingsRead 0.0·0.0; probeOverheadOff 12.0·48.0; probeOverheadOn 12.0·48.3. lizard 1.24.0 (libs and tests/_kit excluded): NLOC 11389, 1639 functions, avg CCN 1.7, max CCN 14 (S.Set in settings/Schema.lua, OnAbsorbChanged in core/AbsorbTracker.lua, NS.ResolveColor in core/CoreSetup.l
- **AuraMaster** — Measured 2026-09-23 on branch feat/2026-09-23-review-audit-remediation @ 8046dfb (both runs went through ~/.claude/wow-addon/bin/ka0s-bounded by absolute path because it is not on PATH). luacheck: pass, 0 warnings / 0 errors in 110 files. Headless tests: 1296/1296 passed, 0 failed, 0 skipped. It ran serially in 2m54s wall with 36.4s user CPU (about 28% utilization, see AM-27). The --list inventory is byte-identical to docs/test-cases.md. Offline perf (tests/perf.lua): 10 scenarios ran and every assertion held. probeOverheadOff equals probeAbsent (5 api calls, 384 B), so the dormant bracket is confirmed free. unitAuraOther was 0.00013 ms/iter and 0 B. There is no in-client capture: docs/perf-analysis/ holds only its README, so all in-game cost claims are unverified. Lizard: 3348 functions, avg CCN 2.3, 2 warnings over CCN 15: Cat.SyncUserCategories CCN 25 (defaults/Categories.lua:1112) an
- **BankLedger** — Both bundles ran at HEAD 3256d8c on feat/2026-09-23-review-audit-remediation against standard v2.64.0 (2026-09-23), all through ~/.claude/wow-addon/bin/ka0s-bounded invoked by absolute path (it is not on PATH). Results: luacheck passed with 0 warnings and 0 errors in 71 files. Headless tests (lua5.1 tests/run.lua) gave 1017 passed, 0 failed, 0 skipped. The --list inventory is byte-identical to docs/test-cases.md and the README badge reads 1017/1017. Perf was skipped: there is no tests/perf.lua, by the ratified performance-§12 no-combat-path exemption (a skip, not a pass). There is no docs/perf-analysis/. lizard (libs/ and tests/_kit/ excluded) gave 17,397 NLOC, 2,640 functions, average CCN 2.0, max CCN 15, 0 warnings. make test was skipped because there is no Makefile. libs/LibKa0s and tests/_kit are byte-identical to LibKa0s v1.55.0 (kit revision 25). The four cross-addon checks were cl
- **ConsumableMaster** — Both bundles measured the same numbers on 2026-09-23 at HEAD 7adfea1 (branch feat/2026-09-23-review-audit-remediation), every command run through ~/.claude/wow-addon/bin/ka0s-bounded by full path because it is not on PATH. No run exited 124 or 137. luacheck: PASS, 0 warnings / 0 errors in 116 files (libs/, tests/_kit/, docs/audits/ and docs/reviews/ excluded). Headless tests: PASS, 998 passed, 0 failed, 0 skipped. The --list inventory matches docs/test-cases.md (diff empty), and the README badge reads 998/998. Offline perf (tests/perf.lua): ran 5 scenarios, exit 0, no assertion failures. recompute 1.027 ms/iter at 2551.1 B/iter, cooldownRefresh 6000.0 B/iter, probeOverheadOff 6000.0 B/iter (dormant, under the 6144 ceiling), probeOverheadOn 6001.3 B/iter, refreshBurst 0.0 B/iter. The zero-overhead property holds. lizard: PASS, no thresholds exceeded. 23258 NLOC, 2499 functions, average CC
- **KickCD** — Both bundles were measured at HEAD dc11094 on feat/2026-09-23-review-audit-remediation (clean tree), against Ka0s WoW Addon Standard v2.64.0. ka0s-bounded was not on PATH, so both runs called it by absolute path and no bare timeout 900 was needed. - luacheck: pass, 0 warnings / 0 errors in 101 files (review and audit agree). .luacheckrc excludes libs/, docs/audits/, _dev/, tests/_kit/ and docs/reviews/, lints tests/, and has no top-level ignore. - Headless tests: 1050 passed, 0 failed, 0 skipped, 1050 total. `--list` is identical to docs/test-cases.md, and the README badge reads 1050/1050. - Offline perf (tests/perf.lua) ran 6 scenarios, figures as ms/iter, api/iter, bytes/iter:   - spellPoll: 0.02021, 18.0, 1196.3   - spellState: 0.00558, 0, 1697.3   - iconApply: 0.00240, 0, 848.0   - probeOverheadOff: 0.00261, 0, 848.0   - probeOverheadOn: 0.00273, 0, 848.1   - castStart: 0.00518, 0, 2
- **LootHistory** — Measured 2026-09-23 on feat/2026-09-23-review-audit-remediation @ 54b7cc7, standard v2.64.0 (WowAddonStandards e68795f). Every run used ~/.claude/wow-addon/bin/ka0s-bounded by absolute path (it is not on PATH); no timeout 900 fallback, no exit 124/137. luacheck 1.2.0: 0 warnings / 0 errors in 65 files. Headless suite: 858 passed, 0 failed, 0 skipped. The fresh --list inventory diffs empty against docs/test-cases.md, and the README badge is 858/858. Perf: skipped because tests/perf.lua does not exist. This is covered by the ratified performance-§12 exemption (issue #22), but every manifest records the wrong skip reason (LH-69, upstream kit). No in-game perf-analysis capture exists. make test: skipped, no Makefile. lizard 1.24.0: 16326 NLOC, 2200 functions, avg CCN 2.1, 0 warnings, max CCN 15. Seven functions sit at 15: Export E@39-159, three BrowserTable functions, Compat.ScanBound, Attri
- **MultiMeters** — Both the review and the audit measured the same state at 4aefb58 on branch feat/2026-09-23-review-audit-remediation. Every run went through ~/.claude/wow-addon/bin/ka0s-bounded, which is installed but not on PATH.  - luacheck: pass, 0 warnings / 0 errors in 125 files. - Headless tests (lua5.1 tests/run.lua): 1948 passed, 0 failed, 0 skipped. The fresh --list inventory is byte-identical to docs/test-cases.md after CR normalisation, and the README badge reads 1948/1948. - Offline perf (tests/perf.lua): ran, exit 0, 15 scenarios.   - refresh20x7: 303438.1 B/iter, 1.31 ms/iter, 8 API calls/iter.   - refresh20x7Restricted: 412373.3 B/iter.   - probeOverheadOff / On: 303415.8 / 303420.9 B/iter.   - feignTraceAbsent / Off: 71544.1 / 71544.1 B/iter.   - suspended: 0.0 B/iter. - lizard: pass, 0 warnings. 4126 functions, 40425 NLOC, average CCN 2.4, max CCN 15 (10 functions at 15, none above). Ren
- **PanelMaster** — Measured identically by review and audit at afb30d7 (branch feat/2026-09-23-review-audit-remediation, addon 1.1.1, LibKa0s v1.55.0 vendored, kit revision 25), all runs through ~/.claude/wow-addon/bin/ka0s-bounded by full path because it is not on PATH. No run exited 124 or 137. luacheck: 0 warnings / 0 errors over 60 files. Headless tests (lua5.1 tests/run.lua): 884 passed / 0 failed / 0 skipped / 884 total. The fresh --list inventory is byte-identical to docs/test-cases.md after CR normalisation, and the README Tests-884/884 badge agrees. Perf: skipped, because there is no tests/perf.lua (ratified performance-§1 deviation). lizard 1.24.0: 0 warnings, max CCN 15 (Compat.AddOnFolders core/Compat.lua@27-45 and R.ApplyArtSize modules/Registry.lua@607-635), 1687 functions, 14325 NLOC, avg CCN 2.0, no watch-list drift. Layout: 0 files over the 1500 cap; 4 files in the 1000-1500 band (settings
- **PartyFrameEnhanced** — Both bundles measured the same commit, 314c95e (v1.0.1, branch feat/2026-09-23-review-audit-remediation), against Ka0s WoW Addon Standard v2.64.0. Every run used ~/.claude/wow-addon/bin/ka0s-bounded by its full path because it is not on PATH. Nothing ran unbounded, no run timed out, and no timeout-900 fallback was needed. - luacheck: pass, 0 warnings and 0 errors in 71 files. The exclude list matches the lint template, and there is no top-level ignore. - Headless tests: pass, 289 passed, 0 failed, 0 skipped. A fresh `--list` is byte-identical to docs/test-cases.md (289), and the README badge reads 289/289. - Offline perf (tests/perf.lua): 9 scenarios, all assertions held. anchorUnchanged 0.0 B/iter, castStartStop 5.4 B/iter, settingsDrag 895.9 B/iter, probeOverheadOff/On 0.0/0.5 B/iter, 11/11 API calls. - lizard: 8045 NLOC, 1047 functions, average CCN 2.2, max CCN 14 (NS.SetByPath settin
- **PrettyChat** — Both runs used ~/.claude/wow-addon/bin/ka0s-bounded by full path because it is not on PATH. No run exited 124 or 137. Checked against standard v2.64.0, LibKa0s v1.55.0 vendored. Branch feat/2026-09-23-review-audit-remediation at HEAD 2a32870. - luacheck: pass, 0 warnings / 0 errors in 48 files. - Headless tests: pass, 438 passed / 0 failed / 0 skipped. Fresh --list is byte-identical to docs/test-cases.md, and the README badge reads 438/438. The kit rev-25 gates (test_layout_cap, test_prose, test_eol, test_vendor_sync, test_surface_parity, test_disabled) are all green. - Perf: skipped. There is no tests/perf.lua, under the ratified performance-§12 no-combat-path exemption (docs/ARCHITECTURE.md:269). The runner records the wrong skip reason (PC-90). - lizard 1.24.0: pass. 941 functions, NLOC 54,817, avg CCN 1.9, max CCN 14 (Database.PruneOrphans core/Database.lua:52-76; stubSet settings/Sc
- **WhatGroup** — Both runs measured on 2026-09-23 at feat/2026-09-23-review-audit-remediation @ 1124ac4 (v1.4.0, LibKa0s v1.55.0, standard v2.64.0). All runs went through ~/.claude/wow-addon/bin/ka0s-bounded by absolute path (not on PATH); no 124/137 exits. luacheck: 0 warnings / 0 errors over 48 files (exclude_files libs/, docs/audits/, docs/reviews/, _dev/, tests/_kit/). Headless tests: 727 passed / 0 failed / 0 skipped (7.2 s wall, ~21 MB RSS); fresh --list matches docs/test-cases.md exactly and README badge reads 727/727. Perf (review ran it; audit only confirmed presence): tests/perf.lua 8 scenarios all matching docs/performance.md: cooldownTick 2.0 api/iter 240.4 B/iter, formatDurationLong 34.5, formatDurationShort 0.8, combatGateSteady 0/0, combatGateFlipping 7.0/1064.1, showFrameRepeat 18.0/1872.5, applyScale 1.0/0.0, applyAlpha 1.0/0.0; performance.md call-site census re-measures 20 lines/4 file

## Clusters

| Cluster | Title | Findings | Repos |
|---|---|---|---|
| C01 | Unrecorded LibKa0s re-vendor bundles | 11 | AbsorbTracker, AuraMaster, BankLedger, ConsumableMaster, KickCD, LootHistory, MultiMeters, PanelMaster, PrettyChat, WhatGroup |
| C02 | AUDIT.md playbook contradictions (upstream WowAddonStandards) | 8 | AbsorbTracker, AuraMaster, ConsumableMaster, KickCD, LootHistory, PanelMaster, PartyFrameEnhanced, WhatGroup |
| C03 | Event registration without per-event pcall isolation | 12 | AbsorbTracker, AuraMaster, BankLedger, ConsumableMaster, KickCD, LibKa0s, LootHistory, MultiMeters, PanelMaster, PartyFrameEnhanced, PrettyChat, WhatGroup |
| C04 | Event subscription scope: private frames and session-long registrations | 7 | AuraMaster, BankLedger, KickCD, MultiMeters, PartyFrameEnhanced, PrettyChat, WhatGroup |
| C05 | Unannotated load-bearing TOC positions (toc-file-§5) | 28 | AbsorbTracker, BankLedger, ConsumableMaster, KickCD, LootHistory, MultiMeters, PanelMaster, PartyFrameEnhanced, PrettyChat, WhatGroup |
| C06 | Stand-down leaves timers, callbacks, drivers and frames armed | 17 | AuraMaster, BankLedger, ConsumableMaster, KickCD, MultiMeters, PartyFrameEnhanced, WhatGroup |
| C07 | Disabled/suspended latch bypassed by UI paths | 12 | AuraMaster, BankLedger, ConsumableMaster, MultiMeters, PanelMaster |
| C08 | Disabled refusal line and launcher disabled-state seam | 8 | LibKa0s, LootHistory, MultiMeters, PartyFrameEnhanced, WhatGroup |
| C09 | Test-kit and mock fidelity gaps | 7 | AbsorbTracker, BankLedger, ConsumableMaster, MultiMeters, PartyFrameEnhanced |
| C10 | Slash verbs that misreport their outcome (profile sub-verbs, lock, test) | 8 | AbsorbTracker, LibKa0s, PartyFrameEnhanced |
| C11 | Profile switch and SavedVariables migration correctness | 10 | KickCD, LootHistory, PanelMaster, PartyFrameEnhanced, PrettyChat, WhatGroup |
| C12 | British spellings and the kit prose gate | 9 | ConsumableMaster, KickCD, LibKa0s, MultiMeters, PanelMaster |
| C13 | Automated-test runner cannot record the performance-§12 exemption | 5 | BankLedger, LibKa0s, LootHistory, PrettyChat |
| C14 | Stale automated-test records, watch lists and release bundles | 22 | AbsorbTracker, BankLedger, ConsumableMaster, KickCD, LibKa0s, LootHistory, MultiMeters, PanelMaster, PartyFrameEnhanced, PrettyChat, WhatGroup |
| C15 | Complexity gate, file-size band and test runtime | 7 | AbsorbTracker, AuraMaster, ConsumableMaster, KickCD, LibKa0s, MultiMeters |
| C16 | ARCHITECTURE hub size and one-screen doc limits | 11 | AbsorbTracker, AuraMaster, BankLedger, ConsumableMaster, KickCD, LootHistory, MultiMeters, PanelMaster, PrettyChat, WhatGroup |
| C17 | Tier 2 doc set: owed, falsely N/A, or re-documenting LibKa0s | 10 | AbsorbTracker, AuraMaster, BankLedger, KickCD, MultiMeters, PanelMaster, WhatGroup |
| C18 | Documented-deviations register hygiene | 24 | AbsorbTracker, AuraMaster, BankLedger, ConsumableMaster, LibKa0s, LootHistory, MultiMeters, PanelMaster, PartyFrameEnhanced, PrettyChat, WhatGroup |
| C19 | Issue-store label and premise housekeeping | 10 | AbsorbTracker, AuraMaster, BankLedger, KickCD, MultiMeters, PanelMaster |
| C20 | Malformed standards citations (documentation-§6) | 10 | AbsorbTracker, BankLedger, ConsumableMaster, KickCD, LootHistory, MultiMeters, PartyFrameEnhanced, WhatGroup |
| C21 | Doc prose and file:line drift in ARCHITECTURE/docs | 20 | AuraMaster, BankLedger, ConsumableMaster, KickCD, LibKa0s, LootHistory, MultiMeters, PanelMaster, PartyFrameEnhanced, PrettyChat, WhatGroup |
| C22 | Stale or misplaced code comments | 11 | AbsorbTracker, AuraMaster, ConsumableMaster, KickCD, LootHistory, MultiMeters, PanelMaster, PrettyChat, WhatGroup |
| C23 | README and DEPENDENCIES.md content | 13 | AuraMaster, BankLedger, ConsumableMaster, KickCD, LootHistory, PanelMaster, PrettyChat, WhatGroup |
| C24 | Namespace bootstrap and self-naming file headers | 5 | AbsorbTracker, PartyFrameEnhanced, PrettyChat |
| C25 | Unused .luacheckrc read_globals | 8 | AbsorbTracker, AuraMaster, KickCD, MultiMeters, PartyFrameEnhanced, PrettyChat, WhatGroup |
| C26 | Degradation stubs: library copies and surface-parity tests | 13 | AbsorbTracker, AuraMaster, BankLedger, LootHistory, PanelMaster, PrettyChat, WhatGroup |
| C27 | Compat and deprecated API use | 5 | AbsorbTracker, AuraMaster, ConsumableMaster, MultiMeters, PrettyChat |
| C28 | Combat-state detection and secure-frame writes | 6 | ConsumableMaster, LootHistory, PanelMaster, PartyFrameEnhanced |
| C29 | WhatGroup popup combat taint and visibility | 3 | WhatGroup |
| C30 | Options reset semantics (options-ui-§12/§13) | 8 | BankLedger, ConsumableMaster, LootHistory, PrettyChat |
| C31 | Printer pre-formatting and chat fallbacks | 6 | AbsorbTracker, BankLedger, KickCD, LootHistory, WhatGroup |
| C32 | Localization of player-visible strings | 9 | AuraMaster, ConsumableMaster, LibKa0s, MultiMeters, PartyFrameEnhanced, WhatGroup |
| C33 | Hard-coded brand, folder names and non-catalog marks | 7 | AbsorbTracker, BankLedger, ConsumableMaster, KickCD, LootHistory, PartyFrameEnhanced, WhatGroup |
| C34 | Message-bus literals and the no-bus ruling | 5 | BankLedger, ConsumableMaster, LootHistory, PrettyChat, WhatGroup |
| C35 | Hot-path allocation, throttles and redundant work | 15 | AbsorbTracker, BankLedger, KickCD, LibKa0s, LootHistory, MultiMeters, PartyFrameEnhanced, PrettyChat, WhatGroup |
| C36 | Test-only exports and dead code on the production namespace | 7 | AbsorbTracker, AuraMaster, ConsumableMaster, KickCD, PrettyChat, WhatGroup |
| C37 | Vacuous assertions and missing invariant tests | 9 | AbsorbTracker, AuraMaster, ConsumableMaster, KickCD, LibKa0s, LootHistory, PrettyChat |
| C38 | LibKa0s library defects | 8 | LibKa0s |
| C39 | KickCD Spells page and icon grid | 7 | KickCD |
| C40 | LootHistory capture and export correctness | 7 | LootHistory |
| C41 | MultiMeters window rows and drill-down | 2 | MultiMeters |
| C42 | PanelMaster panel geometry and frame naming | 4 | PanelMaster |
| C43 | PrettyChat format overrides and cross-addon interaction | 5 | PrettyChat |
| C44 | PartyFrameEnhanced third-party SavedVariables and packaging | 4 | AuraMaster, PartyFrameEnhanced |
| C45 | AuraMaster container frames and host re-implementations | 2 | AuraMaster |
| C46 | WhatGroup LFG status and minimap row | 2 | WhatGroup |
| C47 | Standard text conflicts and tooling baseline (upstream) | 9 | AbsorbTracker, ConsumableMaster, KickCD, LootHistory, MultiMeters |

### C01 — Unrecorded LibKa0s re-vendor bundles

Every addon's docs/revendor/ store stops recording after mid-September: 19-28 re-vendored tags (v1.18.0/v1.35.0 to v1.54.2) have neither a bundle nor a register row, because sweep commits re-vendored without writing one. Affects AbsorbTracker, AuraMaster, BankLedger, ConsumableMaster, KickCD, LootHistory, MultiMeters, PanelMaster, PrettyChat and WhatGroup. AuraMaster's v1.55.0 base note is correct (kit-only v1.54.2) and must not be 'corrected'. One consolidated span bundle per addon lands before the new collection-wide re-vendor.

**AbsorbTracker**

- **AbsorbTracker-A-01** `medium` (audit AT-72; corrected) — 24 re-vendored LibKa0s tags have no docs/revendor/ bundle and no register row  
  *Where:* docs/revendor/, docs/ARCHITECTURE.md:592, CLAUDE.md:43  
  *Evidence:* The AUDIT.md step 4 script (horizon 2026-08-25) finds 31 vendored tags and 9 recorded, leaving 24 unrecorded: v1.18.0 v1.18.1 v1.19.0 v1.23.0 v1.24.0 v1.26.0-v1.29.0 v1.36.0 v1.36.1 v1.36.2 v1.37.0-v1.39.0 v1.42.0 v1.44.0 v1.45.0 v1.46.1 v1.47.0 v1.50.0-v1.53.0. There are 32 libs/LibKa0s commits. The High grade follows AUDIT.md step 4 explicitly; step 5's impact table would call it Low (see Info-5).  
  *Remediation:* C1/S3.2: write one consolidated bundle, docs/revendor/<date>-v1.18.0-v<new-tag>/, with 01_DELTA.md naming the span and all 24 tags plus the upcoming re-vendor tag, and 05_SUMMARY.md saying per tag either 'carried by sweep, nothing adopted' or naming the adoption commit. Do not write per-tag 02-04 files. Write it in the same commit window as the next re-vendor (B/S3.1). Re-run the step 4 script and expect 0 unrecorded, and make sure the folder or first line matches what the check parses.  
  *Rule:* audit-review-history (A re-vendor commit implies a bundle)  
  *Planned in:* AT-25

**AuraMaster**

- **AuraMaster-A-01** `high` (audit AM-21; corrected) — 19 vendored LibKa0s tags (v1.35.0-v1.53.0) have no docs/revendor/ bundle; the v1.55.0 bundle misstates its base as v1.54.2 when it was really v1.53.0  
  *Where:* docs/revendor/2026-09-23-v1.55.0/01_DELTA.md:1; docs/revendor/ (store); git log -- libs/LibKa0s (f6f61d3 v1.53.0 -> f6f3ffb v1.55.0)  
  *Evidence:* E-7: since the store's first bundle (2026-09-12), 27 commits touch libs/LibKa0s and vendor 22 distinct tags, but only 6 are recorded. Unrecorded: v1.35.0, v1.36.0, v1.36.1, v1.36.2, v1.37.0, v1.38.0, v1.39.0, v1.42.0, v1.44.0, v1.46.1, v1.47.0, v1.48.0, v1.48.1, v1.49.0, v1.49.1, v1.50.0, v1.51.0, v1.52.0, v1.53.0. The v1.55.0 01_DELTA.md says 'v1.54.2 -> v1.55.0', but the repo went straight from v1.53.0. Graded High only because AUDIT.md step 4 names that grade. Step 5's impact table would give Low, since no player can hit it.  
  *Remediation:* Write one consolidated bundle, docs/revendor/<date>-v1.35.0-v1.54.2/, with 01_DELTA.md and 05_SUMMARY.md. 01_DELTA.md holds the span log and diff --stat, and lists every repo commit that carried a tag, from 9ba3d01 (v1.35.0) through f6f61d3 (v1.53.0), plus 329e1a3 (v1.54.2, kit-only: library bytes identical to v1.53.0). 05_SUMMARY.md says the sweeps carried these tags and names DragHandle v1.48.0, the entry suffix v1.49.0 and the Lifecycle/Slash minor-14 floor v1.42.0. Do NOT add a 'Correction' paragraph about the v1.55.0 base: v1.54.2 is correct there. Leave the frozen v1.55.0 bundle unedited. Check: the AUDIT.md re-vendor listing shows nothing unrecorded. Also verify by hand that the kit-only v1.54.2 re-vendor is recorded, because that listing cannot see a commit that does not touch libs/LibKa0s. Land this before the collection-wide re-vendor, which writes its own bundle in the same change.  
  *Rule:* audit-review-history (a re-vendor commit implies a bundle)  
  *Planned in:* AM-02
- **AuraMaster-A-21** `low` (audit AM-21 (base misstatement root cause); confirmed · upstream → wow-addon) — The v1.55.0 revendor bundle took its delta base from the library's previous tag (v1.54.2), not from the addon's actually vendored tag (v1.53.0)  
  *Where:* docs/revendor/2026-09-23-v1.55.0/01_DELTA.md:1-15 (produced by /wow-addon:revendor-libka0s steps 2-4, run non-interactively by the suite standards sweep)  
  *Evidence:* 01_DELTA.md runs 'git -C ../LibKa0s log --oneline v1.54.2..v1.55.0', but the repo's previous re-vendor commit f6f61d3 was v1.53.0. Inferred from the bundle text: the base was not derived from the addon's CLAUDE.md provenance line or its last vendoring commit. Other addons re-vendored by the same sweep may share the error.  
  *Remediation:* In the wow-addon plugin's revendor-libka0s command (and any sweep script that drives it), derive the delta base from the addon's recorded vendored tag (CLAUDE.md provenance or last libs/LibKa0s commit), not the library's previous tag. Before the collection-wide LibKa0s re-vendor in this plan, check the other addons' v1.55.0 bundles for the same misstatement.  
  *Rule:* audit-review-history (a re-vendor commit implies a bundle)  
  *Planned in:* WA-01

**BankLedger**

- **BankLedger-A-01** `high` (audit BL-41; confirmed) — 25 re-vendored LibKa0s tags (v1.18.0 to v1.53.0) have no docs/revendor/ bundle and no register row  
  *Where:* docs/revendor/; CLAUDE.md:46 provenance history; git log -- libs/LibKa0s (36 commits since 2026-08-25)  
  *Evidence:* Store horizon docs/revendor/2026-08-25/ (v1.15.0). 36 vendoring commits carry 31 distinct tags, and the bundles record 8. Unrecorded: v1.18.0, v1.18.1, v1.19.0, v1.23.0, v1.24.0, v1.26.0-v1.29.0, v1.35.0, v1.36.0-v1.36.2, v1.37.0, v1.38.0, v1.39.0, v1.42.0, v1.44.0, v1.45.0, v1.46.1, v1.47.0, v1.50.0-v1.53.0 (03_EVIDENCE E-01). The AUDIT.md playbook fixes the grade at High. On player impact alone it would be Low.  
  *Remediation:* S1-1: write one consolidated bundle, docs/revendor/2026-09-23-v1.18.0-v1.53.0/. Its 01_DELTA.md first line names 'LibKa0s v1.15.0 -> v1.54.2' and lists the 36 commits and their tags, noting sweeps carried them. Its 05_SUMMARY.md records what was adopted (launcher, Lifecycle latch v1.42.0, combat lock v1.46.x, IdList v1.47.0/v1.50.0...). Do not back-fill per-tag folders. Land it before or with the next re-vendor, which writes its own bundle. Verify that the AUDIT.md comparison prints nothing.  
  *Rule:* audit-review-history (A re-vendor commit implies a bundle)  
  *Planned in:* BL-23

**ConsumableMaster**

- **ConsumableMaster-A-02** `low` (audit CM-91; corrected) — 27 of the 33 LibKa0s tags vendored since 2026-08-25 have no docs/revendor/ bundle and no Documented deviations row  
  *Where:* docs/revendor/; CLAUDE.md:61 (provenance history); docs/audits/2026-09-23/03_EVIDENCE.md E8  
  *Evidence:* The only bundle after v1.34.0 is 2026-09-23-v1.55.0 (v1.54.2 -> v1.55.0). The span v1.35.0 -> v1.53.0 (18 tags) and 9 earlier tags (v1.18.0-v1.29.0, excluding v1.25.0) went unrecorded. Graded High because AUDIT.md's re-vendor check says so explicitly. The impact is record-keeping only; step 5's impact table would make it Low.  
  *Remediation:* Write one consolidated bundle, docs/revendor/<date>-v1.53.0/ (01_DELTA.md and 05_SUMMARY.md), whose 01_DELTA.md names the span of 27 tags from v1.18.0 to v1.53.0 and the sweeps that vendored them, and whose 05_SUMMARY.md records the adoptions made along the way. Add a '## Documented deviations' row keyed audit-review-history that points at that bundle for the individual tags; E8 reads one tag per bundle, so the row is what clears the span. The S1-1 whole-folder re-vendor carries its own <date>-v<tag> bundle. Re-run E8 and confirm it comes out at 0.  
  *Rule:* audit-review-history  
  *Planned in:* CM-28

**KickCD**

- **KICKCD-A-01** `low` (audit KICKCD-C-01; corrected) — 25 vendored LibKa0s tags since 2026-08-25 have no re-vendor bundle and no register row  
  *Where:* docs/revendor/, CLAUDE.md:42  
  *Evidence:* The AUDIT.md payload-derived check finds 31 vendored tags against 8 recorded. Unrecorded: v1.18.0, v1.18.1, v1.19.0, v1.23.0, v1.24.0, v1.26.0-v1.29.0, v1.35.0, v1.36.0-v1.36.2, v1.37.0, v1.38.0, v1.39.0, v1.42.0, v1.44.0, v1.45.0, v1.46.1, v1.47.0, v1.50.0-v1.53.0. The playbook grades this High explicitly, but it is a records gap no player can reach (see A-02 for the upstream conflict).  
  *Remediation:* Write one consolidated bundle, docs/revendor/<date>-v1.18.0-to-v1.53.0/, with 01_DELTA.md and 05_SUMMARY.md. List the 25 tags and their carrying commits (git log -- libs/LibKa0s), and state that they arrived via bulk sweeps. Name the span on line 1 in the format A-02 settles upstream. Do not back-fill per-tag folders. It is done when the upstream-amended check prints 0 unrecorded tags. Until A-02 lands, the current check will still list 24 of the 25, because it reads one tag from line 1. Grade Low, and name the audit-review-history MUST.  
  *Rule:* audit-review-history (a re-vendor commit implies a bundle)  
  *Planned in:* KC-24

**LootHistory**

- **LootHistory-A-01** `high` (audit LH-62; confirmed) — 25 vendored LibKa0s tags have no re-vendor bundle or register row  
  *Where:* docs/revendor/, CLAUDE.md:51  
  *Evidence:* Since the 2026-08-25 horizon, commits touching libs/LibKa0s vendored 31 distinct tags (read off CLAUDE.md provenance at each commit). docs/revendor/ records 8. The 25 unrecorded tags are v1.18.0, v1.18.1, v1.19.0, v1.23.0, v1.24.0, v1.26.0-v1.29.0, v1.35.0-v1.39.0 (incl. v1.36.1/.2), v1.42.0, v1.44.0, v1.45.0, v1.46.1, v1.47.0 and v1.50.0-v1.53.0. No bundle names a span and there is no Documented deviations row. The High grade is fixed by AUDIT.md step 4; by impact alone it would be Low, since no user reaches it.  
  *Remediation:* Write one consolidated bundle, docs/revendor/<date>-v1.53.0/. Its 01_DELTA.md line 1 names the span v1.15.0 -> v1.53.0, with a table of the 25 unrecorded tags and the vendoring commit of each (git log --format='%h %ad %s' --date=short -- libs/LibKa0s). Its 05_SUMMARY.md states the intermediate tags were carried by sweeps with nothing adopted beyond the commits. Do not back-fill per-tag folders. Re-run the ledger commands and expect count=0. The later re-vendor (the LH-69 fix) must write its own bundle so this does not recur.  
  *Rule:* audit-review-history (A re-vendor commit implies a bundle); AUDIT.md step 4  
  *Planned in:* LH-34

**MultiMeters**

- **MultiMeters-A-19** `high` (audit MM-A-19; confirmed) — 28 LibKa0s tags (v1.18.0 to v1.53.0) were vendored with no re-vendor bundle and no register row  
  *Where:* docs/revendor/; CLAUDE.md:53; git log -- libs/LibKa0s  
  *Evidence:* The commits name 34 distinct tags since the 2026-08-25 horizon. The bundles name 8 tags (v1.15.0, v1.25.0, v1.30.0, v1.31.0-v1.34.0, v1.55.0). The kit-only v1.54.2 (d2169d4) is not seen by the check. The High comes from AUDIT.md step 4; by player impact this would be Low.  
  *Remediation:* Write one consolidated bundle, docs/revendor/<date>-v1.34.0-to-v1.54.2/ (or widen it to v1.15.0 -> v1.54.2, or add a second bundle for v1.15.0 -> v1.30.0). Its 01_DELTA.md first line names the span, and 05_SUMMARY.md records the carrying commit and any adoption per tag. Do not back-fill a folder per tag. Any later collection re-vendor writes its own bundle.  
  *Rule:* audit-review-history (A re-vendor commit implies a bundle); AUDIT.md step 4  
  *Planned in:* MM-30

**PanelMaster**

- **PanelMaster-A-15** `low` (audit PM-048; corrected) — 25 vendored LibKa0s tags since 2026-08-25 have no re-vendor bundle naming them  
  *Where:* docs/revendor/, docs/revendor/2026-09-23-v1.55.0/01_DELTA.md:1, CLAUDE.md:44  
  *Evidence:* 32 commits touching libs/LibKa0s vendored 31 distinct tags, and bundles record 8. The 25 unrecorded tags run v1.18.0 through v1.53.0. The v1.55.0 bundle names only v1.54.2->v1.55.0.  
  *Remediation:* Write one consolidated bundle, docs/revendor/<date>-v1.16.0-to-v1.54.2/, with 01_DELTA.md and 05_SUMMARY.md. First line: '# 01 — Delta: LibKa0s v1.16.0 → v1.54.2 (consolidated)'. In the body, list every unrecorded vendored tag: v1.16.0, the 25 tags from v1.18.0 to v1.53.0, and v1.54.2. Also list the commits that carried them. Re-run AUDIT.md's two-listing check and confirm it prints nothing. If the check reads only the opening line's end tag, the enumerated list in the body must be the thing it reads. Do not write a folder per tag.  
  *Rule:* audit-review-history (a re-vendor commit implies a bundle)  
  *Planned in:* PM-18

**PrettyChat**

- **PRETTYCHAT-A-01** `high` (audit PC-82 (PRETTYCHAT-C-03); confirmed) — 26 vendored LibKa0s tags (v1.18.0–v1.53.0) have no docs/revendor/ bundle and no register row  
  *Where:* docs/revendor/, CLAUDE.md:42, libs/LibKa0s/  
  *Evidence:* Since 2026-08-25, 32 commits touched libs/LibKa0s and vendored 31 distinct tags. Only 7 bundles exist (v1.15.0, v1.30.0–v1.34.0, v1.55.0). Unrecorded: v1.18.0, v1.18.1, v1.19.0, v1.23.0–v1.29.0, v1.35.0, v1.36.0–v1.36.2, v1.37.0, v1.38.0, v1.39.0, v1.42.0, v1.44.0, v1.45.0, v1.46.1, v1.47.0, v1.50.0–v1.53.0. The playbook fixes the grade at High, although no player can reach it.  
  *Remediation:* Write one consolidated bundle docs/revendor/<date>-v1.18.0-v1.53.0/ with 01_DELTA.md (the tag list plus the commit that carried each, from git log -- libs/LibKa0s) and 05_SUMMARY.md (Launcher adopted at v1.39.0, latch after v1.42.0, the rest carried by sweeps). Its first line names the span. Do not back-fill per tag. Also write the bundle for the new re-vendor tag. Optionally raise upstream the playbook's fixed High grade versus its own impact table (Sprint 0.7).  
  *Rule:* audit-review-history (A re-vendor commit implies a bundle)  
  *Planned in:* PC-25

**WhatGroup**

- **WHATGROUP-A-10** `low` (audit WG-71; confirmed) — 25 vendored LibKa0s tags since 2026-08-25 have no re-vendor bundle and no register row  
  *Where:* docs/revendor/, libs/LibKa0s (git log --since=2026-08-25: 32 commits), CLAUDE.md  
  *Evidence:* 31 distinct tags vendored, 6 recorded (v1.25.0, v1.31.0-v1.34.0, v1.55.0). Unrecorded: v1.18.0, v1.18.1, v1.19.0, v1.23.0, v1.24.0, v1.26.0-v1.29.0, v1.35.0-v1.39.0 (+v1.36.1, v1.36.2), v1.42.0, v1.44.0, v1.45.0, v1.46.1, v1.47.0, v1.50.0-v1.53.0. Three re-vendors folded into feature commits (f98ef41, 127baa1, f74893a). AUDIT.md calls this High but its step 5 grades doc-only Low (contradiction filed as WG-82).  
  *Remediation:* During the whole-folder re-vendor (after upstream tag), write one consolidated docs/revendor/<date>-v<tag>/ bundle (01_DELTA.md + 05_SUMMARY.md) with a Backlog section naming the unrecorded span v1.18.0->v1.24.0 and v1.35.0->v1.53.0 and the three folded commit SHAs. Do not back-fill a folder per tag. Re-run AUDIT.md bundle check to print nothing.  
  *Rule:* audit-review-history (MUST: re-vendor bundle or register row)  
  *Planned in:* WG-29


### C02 — AUDIT.md playbook contradictions (upstream WowAddonStandards)

AUDIT.md step 4 hard-codes High for an unrecorded re-vendor, while step 5's impact table grades docs-only gaps Low. Its git log --since skips same-day commits, cannot read a consolidated span bundle and misses kit-only re-vendors. Reported by AbsorbTracker, AuraMaster, ConsumableMaster, KickCD, LootHistory, PanelMaster, PartyFrameEnhanced and WhatGroup. The fix is one upstream edit to the playbook.

**AbsorbTracker**

- **AbsorbTracker-A-22** `info` (audit AT-Info-5; confirmed · upstream → WowAddonStandards) — Info [upstream]: AUDIT.md step 4 grades an unrecorded re-vendor High while the step 5 impact table would grade it Low  
  *Where:* WowAddonStandards AUDIT.md (step 4, step 5)  
  *Evidence:* This is a playbook inconsistency. AT-72 followed step 4's explicit High.  
  *Remediation:* S0.4: raise with WowAddonStandards and have the playbook settle on one grade.  
  *Rule:* AUDIT.md step 4/5  
  *Planned in:* WS-01

**AuraMaster**

- **AuraMaster-A-20** `info` (audit AM-21 (grading note); confirmed · upstream → WowAddonStandards) — AUDIT.md contradicts itself: step 4 hard-codes High for an unrecorded re-vendor tag, while step 5's impact table grades docs-only gaps Low  
  *Where:* WowAddonStandards AUDIT.md step 4 (re-vendor check) vs step 5 (impact table)  
  *Evidence:* The auditor had to record both grades on AM-21 (High by step 4, Low by step 5) 'so the tension inside the playbook stays visible'.  
  *Remediation:* In WowAddonStandards, reconcile the playbook: either have step 4 defer to step 5's impact grading, or state explicitly that step 4's grade overrides step 5.  
  *Rule:* AUDIT.md steps 4/5; audit-review-history  
  *Planned in:* WS-01

**ConsumableMaster**

- **ConsumableMaster-A-03** `low` (audit CM-91 (A5 / S0-5 process note); confirmed · upstream → WowAddonStandards) — AUDIT.md grades the re-vendor check High, contradicting its own step-5 impact table; the check also cannot read a consolidated span bundle  
  *Where:* WowAddonStandards AUDIT.md (re-vendor check; step 5 impact table)  
  *Evidence:* The re-vendor check says a tag vendored with no bundle and no row 'is a High finding'. Step 5 reserves High for user- or session-reachable defects, so a record-keeping gap becomes this addon's only High. E8 may also not recognise a consolidated span bundle as covering the tags in it.  
  *Remediation:* Upstream in WowAddonStandards: either grade the re-vendor check through step 5 (Low, still a MUST) or state explicitly that it is an exception. Make the check able to read a consolidated span bundle (01_DELTA.md naming the span).  
  *Rule:* AUDIT.md step 5; audit-review-history  
  *Planned in:* WS-01

**KickCD**

- **KICKCD-A-02** `info` (audit KICKCD-C-01 (grade note / D9 U2b); confirmed · upstream → WowAddonStandards) — AUDIT.md's explicit High for missing re-vendor bundles conflicts with its own step-5 reachability grading table, and the consolidated-bundle line-1 format is unspecified  
  *Where:* WowAddonStandards AUDIT.md (re-vendor check; step 5 grading table)  
  *Evidence:* The re-vendor check says 'A tag vendored with no bundle naming it ... is a High finding', but step 5 reserves High for user-reachable defects. The check greps one vX.Y.Z off line 1 of 01_DELTA.md, so it is unclear how a consolidated bundle names a span.  
  *Remediation:* Sprint 0.3: in WowAddonStandards AUDIT.md, reconcile the explicit High with the step-5 table, and state how a consolidated bundle's first line names a span so the check reads it. File a playbook edit or an issue.  
  *Rule:* AUDIT.md re-vendor check vs step 5  
  *Planned in:* WS-01

**LootHistory**

- **LootHistory-A-22** `info` (audit 01_CURRENT_STATE non-finding (playbook tension); confirmed · upstream → WowAddonStandards) — AUDIT.md step 4 fixed-High grade for the re-vendor ledger conflicts with step 5's impact grading  
  *Where:* WowAddonStandards AUDIT.md step 4 / step 5  
  *Evidence:* Step 4 fixes a vendored tag with no bundle or row at High. Step 5's impact table would grade any doc-only gap Low. The audit followed step 4 for LH-62 and recorded the tension.  
  *Remediation:* Raise upstream in WowAddonStandards: reconcile AUDIT.md step 4's fixed High with step 5's impact-not-rule-strength grading. Either make step 4 an explicit named exception to step 5, or regrade the ledger finding by impact.  
  *Rule:* AUDIT.md step 4 vs step 5  
  *Planned in:* WS-01

**PanelMaster**

- **PanelMaster-A-16** `info` (audit PM-048 (playbook note); confirmed · upstream → WowAddonStandards) — AUDIT.md grades an unrecorded re-vendor tag High in its check text but Low in its step-5 table  
  *Where:* WowAddonStandards AUDIT.md (re-vendor check vs step-5 grading table)  
  *Evidence:* This run graded PM-048 Low by step 5, and flagged the conflict for the documentation-lane audit of WowAddonStandards.  
  *Remediation:* File a proposal in the WowAddonStandards documentation lane to reconcile the re-vendor check's 'High' with step 5's Low grading for a missing record. This is a proposal only and does not block the addon.  
  *Rule:* AUDIT.md re-vendor check; AUDIT.md step 5  
  *Planned in:* WS-01

**PartyFrameEnhanced**

- **PartyFrameEnhanced-A-19** `info` (audit AUDIT.md evidence note (03_EVIDENCE §10); confirmed · upstream → WowAddonStandards) — The AUDIT.md re-vendor check's git log --since="$horizon" skips same-day re-vendor commits  
  *Where:* WowAddonStandards AUDIT.md (re-vendor check)  
  *Evidence:* git reads a bare date as the current time of day. A run at 20:00 skipped e331135, committed at 14:53 the same day. The audit read the commit directly instead. This is not a finding against the addon.  
  *Remediation:* Audit Sprint 5.3: in WowAddonStandards AUDIT.md, change the check to `git log --since="$horizon 00:00"`.  
  *Rule:* audit-review-history (re-vendor bundle check)  
  *Planned in:* WS-01

**WhatGroup**

- **WHATGROUP-A-23** `info` (audit WG-82; confirmed · upstream → WowAddonStandards) — Three upstream standard text issues: AUDIT.md re-vendor check grade contradicts step 5; toc-file-§3 says 'currently 120007'; layout-§4 '.png ships' ambiguity  
  *Where:* WowAddonStandards AUDIT.md step 4; standards toc-file-§3; standards layout-§4; .pkgmeta:27-31  
  *Evidence:* (1) AUDIT.md calls a missing re-vendor bundle 'a High finding' while step 5 grades doc-only failures Low (see WG-71). (2) toc-file-§3 literal 120007 vs collection 120100. (3) layout-§4 says editable .png 'ships but is never loaded' while .pkgmeta deliberately excludes it.  
  *Remediation:* WowAddonStandards: (1) change to 'is a finding (grade by impact, step 5)'; (2) update to 120100 or drop the literal and point at ADDONS.md; (3) state whether 'ships' is normative; if so WhatGroup .pkgmeta:30-31 needs a row or change. Re-check after amendment (S6-2).  
  *Rule:* AUDIT.md; toc-file-§3; layout-§4  
  *Planned in:* WS-07, WG-26


### C03 — Event registration without per-event pcall isolation

events-frames-taint-§1 requires each event registration to be isolated (a pcall, optionally gated by C_EventUtils.IsEventValid) with rejected names recorded, so one retired event cannot abort OnEnable. Every addon and the LibKa0s payload register with bare loops or calls. The best fix is one LibKa0s helper, adopted in AbsorbTracker, AuraMaster, BankLedger, ConsumableMaster, KickCD, LootHistory, MultiMeters, PanelMaster, PartyFrameEnhanced, PrettyChat and WhatGroup.

**LibKa0s**

- **LibKa0s-A-10** `info` (audit LK-37; corrected) — Payload registers client events raw on private frames with no pcall'd per-event isolation or rejected-name record  
  *Where:* LibKa0s/OptionsTabs.lua:102-103; LibKa0s/OptionsTabs.lua:139-140; LibKa0s/Widgets.lua:393  
  *Evidence:* f:RegisterEvent("PLAYER_REGEN_DISABLED"/"PLAYER_REGEN_ENABLED") on combat-lock frame and m:RegisterEvent("GLOBAL_MOUSE_DOWN") on popup menu; events-frames-taint-§1 (binds per library-stack-§7) requires a single pcall'd helper, player-reachable rejected-name record, AceEvent over private frames. Not reachable today; no register row records why. Note: the library cannot floor on consumer-vendored AceEvent (library-stack-§6), a tension the audit resolves locally via a register row rather than flagging against the standard.  
  *Remediation:* Record a CLAUDE.md register row for events-frames-taint-§1. It covers the widget-owned private frames in OptionsTabs.lua (combat lock, PLAYER_REGEN_DISABLED/ENABLED) and Widgets.lua (popup-menu dismiss, GLOBAL_MOUSE_DOWN). Reasons: the section is written against addon event traffic; these frames carry UI state for one widget; and the three names are stable core events, so one-bad-name isolation cannot trigger. Do not justify the row with 'the library cannot use AceEvent', because Bus.lua already resolves AceEvent at call time. Re-check trigger: registering any event newer than the current expansion, or a fourth private registration site. Make no code change unless the owner chooses the pcall'd-helper route. If they do, batch it with the OptionsTabs/Widgets minors already planned.  
  *Rule:* events-frames-taint-§1; library-stack-§7  
  *Planned in:* LK-30

**AbsorbTracker**

- **AbsorbTracker-A-12** `low` (audit AT-74; corrected) — Event registrations are bare calls with no per-event pcall and no record of rejected names  
  *Where:* core/AbsorbTracker.lua:120-122, core/AbsorbTracker.lua:164-165, core/AbsorbTracker.lua:176, core/AbsorbTracker.lua:181, core/Lifecycle.lua:68-71  
  *Evidence:* RegisterLifecycleEvents makes 3 bare RegisterEvent calls. SyncUnitEventFrames makes bare RegisterUnitEvent calls and 2 RegisterEvent calls. There is no pcall anywhere around registration. This is latent: one retired event name would leave every later registration unbound with no visible error.  
  *Remediation:* C4/S2.1: add file-local safeRegister(addon, event, method) and safeRegisterUnit(frame, event, unit) helpers in core/AbsorbTracker.lua. Each pcalls the registration, optionally front-gates with C_EventUtils.IsEventValid when it exists (SHOULD), appends failures to NS.State.rejectedEvents and emits NS.Debug('Events', ...). Route all 7 calls through them; StandUp inherits the change through RegisterLifecycleEvents and SyncUnitEventFrames. Make the list reachable through the debug verb or console (for example, /at debug events, or a line in the debug-enable [Init] summary). Write the quirks-doc note that the standard asks for. Tests: RegisterEvent half via M.__badEvents (-- red under: drop the pcall). Upstream (LibKa0s testkit): make the mock frame's RegisterUnitEvent/RegisterEvent honor M.__badEvents, then add the unit-half test after the re-vendor. Until then, a local stub on the frame can stand in. Keep test_disabled green.  
  *Rule:* events-frames-taint-§1 (An unknown event name raises)  
  *Planned in:* AT-07

**AuraMaster**

- **AuraMaster-R-05** `low` (both F-005; AM-23; confirmed · upstream → LibKa0s) — Event registration is bare sequential RegisterEvent calls, with no per-event pcall isolation and no record of rejected names  
  *Where:* core/AuraMaster.lua:57-67; modules/TimedSpells.lua:140-142; modules/TimedSpells.lua:121; core/LifecycleSetup.lua:71  
  *Evidence:* RegisterLifecycleEvents makes eight bare self:RegisterEvent calls, ending with ADDON_RESTRICTION_STATE_CHANGED. TS.Sync registers three more, and syncAuraListen registers UNIT_AURA. An unknown name raises and takes the rest of the block with it. Every name is valid on 12.1, so this is latent.  
  *Remediation:* Upstream first: nominate a SafeRegisterEvent(target, event, handler, record) helper to LibKa0s-Core-1.0 (a C_EventUtils.IsEventValid front-gate plus pcall, appending refused names to a caller-owned list). Optionally, LibKa0s-DebugLog renders the rejected list inside [Init]. It clears library-stack-§7's promotion bars because every addon is bound by events-frames-taint-§1. If it ships, re-vendor the whole folder with a bundle. If declined, add a host NS.RegisterEventSafe in core/CoreSetup.lua. Route RegisterLifecycleEvents (as a loop over a module-level list), TS.Sync, syncAuraListen and the LifecycleSetup PLAYER_REGEN_ENABLED hold through it. Record rejects in NS.RejectedEvents and surface them in the [Init] summary (optionally /am debug events). Test with kit M.__badEvents = {ADDON_RESTRICTION_STATE_CHANGED=true}: the other seven still register and the name is recorded (red under: bare RegisterEvent).  
  *Rule:* events-frames-taint-§1 (an unknown event name raises; IsEventValid front-gate SHOULD)  
  *Planned in:* LK-11, AM-07

**BankLedger**

- **BankLedger-A-13** `low` (audit BL-47; confirmed) — Five event registrations bypass the pcall-isolating helper; no C_EventUtils.IsEventValid front gate anywhere  
  *Where:* core/BankLedger.lua:87,91,92; modules/Browser.lua:1218; modules/SessionWindow.lua:673; modules/Ledger.lua:849-854; docs/ARCHITECTURE.md:373-385  
  *Evidence:* Only the capture engine uses L:RegisterEventSafely. In NS.StandUp, a raise on the first of the three registrations would also abort Ledger:Enable, Browser:Enable and SessionWindow:Enable. ARCHITECTURE's argument that the names cannot retire is prose, not the helper. The problem is latent.  
  *Remediation:* S3-3: promote to a shared NS.RegisterEventSafely(target, event, handler) (core/Util.lua or BankLedger.lua) writing one registered/unavailable record that /bl debug scan reports and NS.StandDown resets. Front-gate it with C_EventUtils.IsEventValid when available, keeping the pcall. Route all five sites through it. Add a test that a bad name in the stand-up block does not stop Ledger:Enable, and update the ARCHITECTURE Event Subscriptions section. Coordinate with R-08, whose PIM registration uses the same helper.  
  *Rule:* events-frames-taint-§1 (MUST isolation; SHOULD IsEventValid)  
  *Planned in:* BL-06

**ConsumableMaster**

- **ConsumableMaster-A-08** `low` (audit CM-87; confirmed) — The event registration block in KCM:OnEnable has no per-event pcall and no rejected-name record  
  *Where:* core/ConsumableMaster.lua:706-717  
  *Evidence:* Nine bare self:RegisterEvent calls. All nine names are live today, so this is latent. A retired name would silently leave the addon deaf to every event registered after it, and standUp calls OnEnable too.  
  *Remediation:* B4 / S3-1 (after B1 and B2): a module-level EVENTS list and a safeRegister helper using pcall, front-gated by C_EventUtils.IsEventValid. Publish KCM.RejectedEvents and surface it in the [Init] debug content and a /cm dump events target. Add a mock.__badEvents case, with a falsification comment, where one retired name leaves the other eight bound. Point test_disabled step 1 at KCM.EVENTS. Note the trade in docs/midnight-quirks.md. Optional A4 / S0-4: a shared SafeRegister on LibKa0s-Core-1.0, then re-vendor; this is the owner's scheduling call, not a blocker.  
  *Rule:* events-frames-taint-§1  
  *Planned in:* CM-15

**KickCD**

- **KICKCD-A-03** `low` (audit KICKCD-C-02; confirmed) — No event-registration block is pcall-isolated and no rejected-name record exists  
  *Where:* modules/Cooldowns.lua:544-555, modules/IconGrid.lua:935-949, modules/Castbar.lua:1081-1087, modules/UnitLabel.lua:253, core/State.lua:144-146, core/State.lua:205-213, settings/Spells.lua:380-381, settings/Spells.lua:1358-1364  
  *Evidence:* All events are registered bare, one after another. A grep for IsEventValid, pcall around Register, or badEvents finds nothing. The defect is latent (every name is valid on 12.1.0), but the first retired name would silently stop the rest of its block.  
  *Remediation:* D2/Sprint 2.3: add Util.SafeRegister(target, event, handler), fronted by C_EventUtils.IsEventValid (the SHOULD) with a pcall fallback, plus a unit-event sibling used by R-03's Arm. Keep rejected names in NS.State.rejectedEvents, log one [Events] console line each, and add a /kcd debug events verb. Route every block through it. Test with the kit mock's __badEvents: mark SPELL_UPDATE_USABLE bad and assert the later events still register and the name shows in /kcd debug events. Must land after R-03.  
  *Rule:* events-frames-taint-§1 (an unknown event name raises)  
  *Planned in:* KC-04

**LootHistory**

- **LootHistory-A-03** `low` (audit LH-64; confirmed) — Event-registration blocks are not isolated per event and nothing records rejected event names  
  *Where:* modules/Attribution.lua:349-355, modules/Attribution.lua:369, modules/Collector.lua:218-219, modules/Browser.lua:1246, modules/Browser.lua:1252, core/LifecycleSetup.lua:112  
  *Evidence:* Every registration is a bare call. A retired event name would raise, and every registration after it in the block would go unbound silently. A grep for IsEventValid, __badEvents or rejected in core, modules and settings finds nothing. This is latent: every name is valid on 12.1. The C_EventUtils.IsEventValid SHOULD is also unmet.  
  *Remediation:* Add NS.SafeRegister(target, event, handler, unit), which front-gates with C_EventUtils.IsEventValid and pcalls the register, plus NS.RejectedEvents, in core/LifecycleSetup.lua or core/Util.lua. Route every block through it. Keep Attribution.__events as the names that actually registered, so Disable stays symmetric. Surface the list via /lh debug events and a clause in the [Init] summary. Add C_EventUtils to .luacheckrc. Test with the kit's M.__badEvents (ENCOUNTER_START): the other six still register and the rejected list names it. tests/test_disabled.lua must still reach an empty set. Smoke S2.  
  *Rule:* events-frames-taint-§1 (MUST)  
  *Planned in:* LH-17

**MultiMeters**

- **MultiMeters-A-20** `low` (audit MM-A-20; confirmed) — Event registration is not isolated per event, and rejected names are not recorded  
  *Where:* core/MultiMeters.lua:149-213; core/MultiMeters.lua:124-132; core/MultiMeters.lua:127-128; core/MultiMeters.lua:195; core/MultiMeters.lua:153-156  
  *Evidence:* There are 21 bare self:RegisterEvent calls, so the first unknown name aborts every later one, including DAMAGE_METER_*. registerIfValid calls RegisterEvent outside the pcall. The :153-156 comment wrongly says an unknown event costs nothing. Nothing reachable by the player records rejections.  
  *Remediation:* Add a single pcall-wrapped registerEvent(target, event, handler) with IsEventValid as a front gate, and route all 22 registrations through a module-level EVENTS list. Keep failures in NS.State.rejectedEvents, reset on each OnEnable, with a debug line. Show them in /mm debug diag. Add a test_lifecycle case using M.__badEvents. Fix the comment and add a note in docs/midnight-quirks.md. Keep target=self so Disabled 3 and Disabled 9 stay green.  
  *Rule:* events-frames-taint-§1  
  *Planned in:* MM-07

**PanelMaster**

- **PanelMaster-A-01** `low` (audit PM-035; confirmed) — Event registration has no per-event pcall and records rejected event names nowhere  
  *Where:* core/LifecycleSetup.lua:126-129, core/PanelMaster.lua:63, core/DebugLogSetup.lua  
  *Evidence:* NS.StandUp registers three events with bare calls, and OnInitialize registers PLAYER_LOGIN bare. On retail an unknown name raises, so a throw would leave the later registrations, Canvas:Enable() and the repaint unbound, with nothing visible. This is two MUSTs. It is latent: no registered event is retired today.  
  *Remediation:* Add a file-local safeRegister(event, handler) in core/LifecycleSetup.lua that pcalls NS.addon:RegisterEvent, appends failures to NS.State.rejectedEvents and logs NS.Debug('Events', ...). Route all four registrations through it; StandDown keeps its bare UnregisterEvent. Surface 'rejected events: <n> (<names>)' in D:Diagnose() so /pm debug reaches it. C_EventUtils.IsEventValid is an optional SHOULD. Write the test first using the kit mock's M.__badEvents, with a red-under comment.  
  *Rule:* events-frames-taint-§1  
  *Planned in:* PM-08

**PartyFrameEnhanced**

- **PartyFrameEnhanced-A-03** `low` (audit PFE-14; corrected) — Event registrations are bare loops with no per-event pcall, no C_EventUtils.IsEventValid gate and no record of rejected names  
  *Where:* core/PartyFrameEnhanced.lua:140; modules/CastBars.lua:336; modules/Providers.lua:330-336; modules/PetFrames.lua:103-107; modules/TargetFrames.lua:214,320,326; modules/RangeFade.lua:168; modules/Preview.lua:81,154  
  *Evidence:* `for event, method in pairs(LIFECYCLE_EVENTS) do self:RegisterEvent(event, method) end` and `for i = 1, #EVENTS do el:RegisterUnitEvent(EVENTS[i], unit) end`. `grep IsEventValid` finds nothing. One retired event name would leave every later event in the block unregistered. This is latent: every name is valid on 12.1.0. Two MUSTs and one SHOULD fail.  
  *Remediation:* Add NS.SafeRegister in core/: one pcall per event, rejected names recorded in NS.RejectedEvents, and IsEventValid as an optional front gate that is never the only guard. Route every RegisterEvent and RegisterUnitEvent site through it. Make NS.RejectedEvents reachable through the reserved debug verb or the debug console, as §1 requires; /pfe status can also show it. Write the test first using the kit's existing M.__badEvents. Record the probing trade-off in the quirks doc. Optionally raise upstream whether LibKa0s should ship this helper, since five repos have each written their own.  
  *Rule:* events-frames-taint-§1 (An unknown event name raises)  
  *Planned in:* PF-10

**PrettyChat**

- **PRETTYCHAT-A-09** `low` (audit PC-85 (PRETTYCHAT-C-06); confirmed) — Event registrations are a bare loop with no pcall helper and no record of rejected names  
  *Where:* modules/Override.lua:138-140  
  *Evidence:* `for _, event in ipairs({...}) do combatWatcher:RegisterEvent(event) end`. A retired event name would raise, or silently deafen the watcher, with no record.  
  *Remediation:* Add a registerEvent(frame, event) helper: C_EventUtils.IsEventValid front gate, pcall(frame.RegisterEvent), and a rejected-name record in NS.RejectedEvents. Surface it in /pc debug and in the [Init] summary. Add a test using the kit's M.__badEvents to prove one bad name leaves the other registered and is recorded. Keep test_disabled green.  
  *Rule:* events-frames-taint-§1 (An unknown event name raises)  
  *Planned in:* PC-12

**WhatGroup**

- **WHATGROUP-A-07** `low` (audit WG-67; confirmed) — Event registrations are bare; one retired event name aborts OnEnable before settings, launcher and latch  
  *Where:* core/WhatGroup.lua:293-304, core/WhatGroup.lua:373, core/WhatGroup.lua:388, core/WhatGroup.lua:397, core/WhatGroup.lua:405, modules/Frame.lua:529, modules/Frame.lua:1028  
  *Evidence:* registerFeatureEvents calls self:RegisterEvent four times unprotected and runs first in OnEnable; retail raises on unknown names, leaving no panel, no minimap button, dead disable switch. Raw frame RegisterEvent calls not isolated. No rejected-names record, no /wg debug surface, no C_EventUtils.IsEventValid front gate. Latent (all four events current).  
  *Remediation:* Add a file-scope safeRegister(target, event, handler) helper: C_EventUtils.IsEventValid front gate, pcall(RegisterEvent), record failures in session-only NS.RejectedEvents; route the four AceEvent registrations (and WG-68 replacement) through it; surface rejectedEvents in the [Init] summary on /wg debug on and log each once via NS.Debug("Events", fmt, ...). Test-first case seeding kit mock __badEvents with GROUP_ROSTER_UPDATE asserting other three register, Settings.Register and NS.Launcher:Register ran, rejection recorded (-- red under bare RegisterEvent). Record the probing trade in docs/midnight-quirks.md.  
  *Rule:* events-frames-taint-§1 (MUST x2, IsEventValid SHOULD)  
  *Planned in:* WG-06


### C04 — Event subscription scope: private frames and session-long registrations

Addons carry ordinary non-unit event traffic on private CreateFrame frames, keep narrow-use events registered all session instead of syncing them per feature, or register events that never fire. The standard's events-frames-taint-§1 and library-stack-§1 wording conflict (upstream). Affects AuraMaster, BankLedger, KickCD, MultiMeters, PartyFrameEnhanced, PrettyChat and WhatGroup.

**AuraMaster**

- **AuraMaster-R-03** `low` (review F-002; corrected) — UNIT_AURA registered via AceEvent for every unit while a 'without a duration' container exists; the standard's carve-out permits a player/pet unit-filtered frame  
  *Where:* modules/TimedSpells.lua:121; modules/TimedSpells.lua:111-113; modules/TimedSpells.lua:13-21  
  *Evidence:* events:RegisterEvent('UNIT_AURA', onUnitAura), where onUnitAura discards everything except player and pet. The header rationale ('vendored AceEvent has no RegisterUnitEvent') is stale: events-frames-taint-§1 now has a named carve-out that cites this addon. Offline, unitAuraOther costs 0.00013 ms/iter and 0 B. The client dispatch cost is unverified with no in-client capture. It is reachable only when a container sets durationMode to 'only without a duration'; no starter does. The audit ('checked and not filed') treats the AceEvent path as compliant and the carve-out as optional.  
  *Remediation:* Optional adoption of the events-frames-taint-§1 MAY carve-out. Hold one private frame on the module, TS.unitFrame = TS.unitFrame or CreateFrame('Frame'). Its single OnEvent dispatches to onUnitAura. syncAuraListen opens it with RegisterUnitEvent('UNIT_AURA','player','pet') and closes it with UnregisterEvent('UNIT_AURA'). TS.Stop must unregister it by hand, because AceEvent's UnregisterAllEvents does not reach it. Reuse the frame across disable/enable. Rewrite the :13-21 header: AceEvent still lacks RegisterUnitEvent, and this is the carve-out. Tests: the test_disabled census includes the frame, and test_timedspells asserts the frame's __unitEvents.UNIT_AURA == {'player','pet'} (the kit mock already records it at tests/_kit/mock_base.lua:226, so no mock work is needed). Replace the perf.lua unitAuraOther scenario, update docs/performance.md, and put pre/post in-client captures in docs/perf-analysis/ if the change is taken.  
  *Rule:* events-frames-taint-§1 (one permitted private frame carve-out)  
  *Planned in:* AM-08

**BankLedger**

- **BankLedger-R-08** `low` (review F-005; confirmed) — GUILDBANKFRAME_OPENED/_CLOSED are registered although the code's own comment says they never fire; the modern PLAYER_INTERACTION_MANAGER_FRAME_SHOW/_HIDE is unused  
  *Where:* modules/Ledger.lua:697,713-736,819-826; docs/ARCHITECTURE.md (registration count of 14); docs/performance.md sweep row  
  *Evidence:* The comment at :697 says GUILDBANKFRAME_CLOSED 'registers without complaint and never fires on 12.0.7'. The real signal is the GuildBankFrame OnShow/OnHide HookScript. The dead registrations inflate /bl debug scan and the ARCHITECTURE count. Whether PIM fires for GuildBanker on 12.1 is unverified in client.  
  *Remediation:* C-08: step 1 in client: run /etrace filtered to GUILDBANK and PLAYER_INTERACTION while opening and closing the vault, and record which events fire and with what argument. Step 2: if PIM fires with Enum.PlayerInteractionType.GuildBanker, register it through RegisterEventSafely with a type filter driving OpenContext(GUILD_BANK) and CloseContext(), keep the hook as backstop and remove the dead names. Otherwise just remove GUILDBANKFRAME_OPENED/_CLOSED from OPEN_EVENTS/CLOSE_EVENTS. Either way, update the ARCHITECTURE count and the performance.md sweep row in the same commit, plus a test_ledger case if PIM is added. Do this after R-01 and the doc sweep.  
  *Rule:* events-frames-taint (register in the enable path); performance-§12 (sweep must stay current)  
  *Planned in:* BL-07

**KickCD**

- **KICKCD-A-04** `low` (audit KICKCD-C-04; corrected) — Two private frames carry ordinary non-unit event traffic (State boot frame, Spells cacheEvents)  
  *Where:* core/State.lua:143-146, settings/Spells.lua:375-381, docs/ARCHITECTURE.md:99  
  *Evidence:* The State boot frame carries PLAYER_LOGIN and PLAYER_REGEN_DISABLED/ENABLED. Spells cacheEvents carries TRAIT_CONFIG_UPDATED and PLAYER_SPECIALIZATION_CHANGED. Neither is a RegisterUnitEvent filter. ARCHITECTURE.md:99 argues for the State frame, but no register row records it.  
  *Remediation:* Move cacheEvents onto an AceEvent target created eagerly at settings/Spells.lua module scope, via NS.NewBusTarget(), which is available by then, or a shared Spells.__ev created at file load rather than in the lazy panel builder, so the cache still invalidates when the panel is never opened. For the State boot listener, NS.NewBusTarget is not defined yet when core/State.lua loads (TOC 55 vs core/KickCD.lua at 68). Either embed AceEvent directly in State.lua (local boot = {}; LibStub('AceEvent-3.0'):Embed(boot)), or move NewBusTarget into a file that loads before State.lua. Then rewrite StandDown/StandUp as UnregisterAllEvents/RegisterEvent on that target. If the owner holds that the raw frame is load-bearing, keep it and add a Documented deviations row with a re-check trigger instead. test_state and test_disabled must stay green.  
  *Rule:* events-frames-taint-§1 (MUST NOT create per-module frames for ordinary event traffic)  
  *Planned in:* KC-06, KC-07

**MultiMeters**

- **MultiMeters-R-17** `low` (review F-017; confirmed) — UNIT_SPELLCAST_SUCCEEDED and CHAT_MSG_SYSTEM stay registered all session for narrow uses, and neither is measured  
  *Where:* core/MultiMeters.lua:201; core/MultiMeters.lua:208; modules/Export.lua:839-856  
  *Evidence:* No perf bucket brackets either handler, so their cost is unverified.  
  *Remediation:* C-15, measurement only: add the handlers to an existing bucket or a debug-only counter. A new bucket needs its descriptor entry in core/PerfSetup.lua and its bracket in the same commit. Decide on registration changes next cycle from the numbers.  
  *Rule:* performance-§3  
  *Planned in:* MM-19

**PartyFrameEnhanced**

- **PartyFrameEnhanced-R-17** `low` (review F-017; confirmed) — Session-long event registrations bypass the per-feature syncEvents discipline, and debug arguments are built even with debug off  
  *Where:* modules/TargetFrames.lua:205, :320, :326; modules/PetFrames.lua:83, :189; modules/Preview.lua:154  
  *Evidence:* PLAYER_TARGET_CHANGED and RAID_TARGET_UPDATE are registered at file load for every enabled session, including solo and feature-off. Preview's PLAYER_REGEN_DISABLED stays registered while not previewing. UnitName(...) is called just to build an NS.Debug argument on every UNIT_TARGET/UNIT_PET, even with debug off.  
  *Remediation:* C-008 / T-12, after T-1 and T-5: guard the NS.Debug argument construction with `if NS.State.debug`. Move PLAYER_TARGET_CHANGED and RAID_TARGET_UPDATE into each module's syncEvents (feature on and in a party). Move Preview's PLAYER_REGEN_DISABLED into listen(on). Re-run test_disabled and confirm R_on is still non-empty.  
  *Rule:* events-frames-taint-§1  
  *Planned in:* PF-09

**PrettyChat**

- **PRETTYCHAT-A-08** `low` (audit PC-84 (PRETTYCHAT-C-05); confirmed · upstream → WowAddonStandards) — Combat watcher is a private CreateFrame carrying non-unit events; the standard contradicts itself (events-frames-taint-§1 vs library-stack-§1)  
  *Where:* modules/Override.lua:120-139  
  *Evidence:* CreateFrame('Frame','PrettyChatCombatWatcher') registers PLAYER_REGEN_DISABLED/_ENABLED. §1 requires AceEvent, and its carve-out excludes a private RegisterEvent for events the client does not filter by unit. library-stack-§1 cites this very frame as the reason AceEvent is 'when used'. Stand-down is correct, so there is no player impact.  
  *Remediation:* Upstream first (Sprint 0.1): file a WowAddonStandards issue to widen the §1 carve-out to a lazily-created, fully stood-down boundary-event frame, or to state that such an addon records a row. If the rule is kept, add a Documented deviations row keyed events-frames-taint-§1 (trigger: the first additional event, or a second event-registering module). Vendoring AceEvent is not recommended.  
  *Rule:* events-frames-taint-§1; library-stack-§1  
  *Planned in:* WS-04, PC-12

**WhatGroup**

- **WHATGROUP-A-08** `low` (audit WG-68; confirmed) — Two private frames carry ordinary PLAYER_REGEN_ENABLED traffic outside AceEvent  
  *Where:* modules/Frame.lua:526-541, modules/Frame.lua:1026-1038, modules/Frame.lua:1115-1123  
  *Evidence:* deferTeleportUntilCombatEnds does f:RegisterEvent("PLAYER_REGEN_ENABLED") and swaps OnEvent; ShowFrame's first-show defer creates buildWaitFrame for the same event. Not unit-filtered, so outside the RegisterUnitEvent carve-out (new v2.63.0 text). Torn down correctly by NS.FrameStandDown.  
  *Remediation:* Replace with a pending-work queue in modules/Frame.lua (NS.FrameQueueForCombatEnd / NS.FrameDrainCombatEnd) drained first by WhatGroup:OnCombatStateChanged("PLAYER_REGEN_ENABLED"); deferTeleportUntilCombatEnds queues once keeping latest-info semantics; delete buildWaitFrame; FrameStandDown clears the queue (replaces raw unregisters); OnDisabledCombatEnded does not drain. Alternative: one private AceEvent-embedded target. Retarget combat-defer tests to fire through AceEvent mock; keep rawRegs survey as regression guard. Note: interacts with review C-001's deferral replay (NO_CAPTURE sentinel) — sequence together.  
  *Rule:* events-frames-taint-§1 (MUST NOT per-module frames)  
  *Planned in:* WG-05


### C05 — Unannotated load-bearing TOC positions (toc-file-§5)

Some files' TOC positions are load-bearing (file-scope reads of NS members, GetModule at load, Setup ordering), yet those lines have no comment, and conventional groups lack the 'conventional' note. The fix is a TOC-comment pass per addon, ideally pinned by a load-order test, in AbsorbTracker, BankLedger, ConsumableMaster, KickCD, LootHistory, MultiMeters, PanelMaster, PartyFrameEnhanced, PrettyChat and WhatGroup.

**AbsorbTracker**

- **AbsorbTracker-A-05** `low` (audit AT-64; confirmed) — TOC line core\PerfSetup.lua is load-bearing but has no annotation  
  *Where:* AbsorbTracker.toc:53, core/AbsorbTracker.lua:7, modules/Display.lua:8, modules/Timer.lua:9  
  *Evidence:* This recurs. NS.Perf is taken as a file-scope upvalue by AbsorbTracker, Display and Timer. The comment at :49-51 annotates Lifecycle, not this line.  
  *Remediation:* C2/S1.1: add '# LOAD-BEARING: publishes NS.Perf, a file-scope upvalue in core/AbsorbTracker.lua, modules/Display.lua and modules/Timer.lua (performance-§1).' above :53.  
  *Rule:* toc-file-§5  
  *Planned in:* AT-20
- **AbsorbTracker-A-06** `low` (audit AT-65; confirmed) — TOC line core\Units.lua is load-bearing but has no annotation  
  *Where:* AbsorbTracker.toc:55, core/Database.lua:32  
  *Evidence:* This recurs. core/Database.lua:32 takes local deepcopy = NS.Units.DeepCopy at file load.  
  *Remediation:* C2/S1.1: add '# LOAD-BEARING: publishes NS.Units, whose DeepCopy core/Database.lua takes at file load.' above :55.  
  *Rule:* toc-file-§5  
  *Planned in:* AT-20
- **AbsorbTracker-A-07** `low` (audit AT-69; confirmed) — TOC line core\Bus.lua is load-bearing but has no annotation (a later position fails silently)  
  *Where:* AbsorbTracker.toc:47, core/AbsorbTracker.lua:357-362  
  *Evidence:* core/AbsorbTracker.lua calls NS.NewBusTarget() and reads NS.MSG.UNITS at file load behind 'if NS.NewBusTarget then'. Moving the Bus line below it would silently lose the UNITS subscription.  
  *Remediation:* C2/S1.1: add '# LOAD-BEARING: publishes NS.NewBusTarget / NS.MSG; core/AbsorbTracker.lua subscribes UNITS with them at file load behind a guard, so a later position fails silently.' above :47.  
  *Rule:* toc-file-§5  
  *Planned in:* AT-20
- **AbsorbTracker-A-08** `low` (audit AT-70; confirmed) — TOC line core\CoreSetup.lua is load-bearing but has no annotation  
  *Where:* AbsorbTracker.toc:48, core/LauncherSetup.lua:60, core/AbsorbTracker.lua:25, core/DebugLogSetup.lua:22, core/PerfSetup.lua:28, core/CoreSetup.lua:12-14  
  *Evidence:* NS.Print, NS.Util.print and NS.LIBKA0S_MISSING are captured at file load by LauncherSetup, AbsorbTracker and the stub branches of DebugLogSetup and PerfSetup. The constraint is written only in the file's own header.  
  *Remediation:* C2/S1.1: add '# LOAD-BEARING: publishes NS.Print / NS.Util.print and NS.LIBKA0S_MISSING, captured at file load by LauncherSetup, AbsorbTracker and the stub branches of DebugLogSetup and PerfSetup.' above :48.  
  *Rule:* toc-file-§5  
  *Planned in:* AT-20
- **AbsorbTracker-A-09** `low` (audit AT-71; confirmed) — TOC line core\Namespace.lua is load-bearing but has no annotation  
  *Where:* AbsorbTracker.toc:45, core/PerfSetup.lua:47  
  *Evidence:* PerfSetup captures version = NS.version into the perf descriptor at file load. Moving Namespace below PerfSetup would stamp captures with a nil version.  
  *Remediation:* C2/S1.1: add '# LOAD-BEARING: publishes NS.version, captured into the perf descriptor by core/PerfSetup.lua at file load.' above :45. Also add a conventional-group note over State.lua, Data.lua and Database.lua (toc-file-§5 SHOULD).  
  *Rule:* toc-file-§5  
  *Planned in:* AT-20

**BankLedger**

- **BankLedger-A-06** `low` (audit BL-36; confirmed) — BankLedger.toc: the load-bearing position of modules\Insights.lua (file-scope NS.InsightsWidgets upvalue) is unannotated (recurs)  
  *Where:* BankLedger.toc:78,84-85; modules/Insights.lua:5; modules/InsightsWidgets.lua:2  
  *Evidence:* local W = NS.InsightsWidgets at file scope. Swapping the TOC lines leaves W nil for the session with no load error. Five other load-bearing positions are annotated.  
  *Remediation:* S4-3: add a comment above modules\Insights.lua: 'LOAD-BEARING: takes NS.InsightsWidgets as a file-scope upvalue; modules\InsightsWidgets.lua above creates it — swapped, W is nil and every chart call raises'. Optionally pin it in test_harness or test_libka0s.  
  *Rule:* toc-file-§5  
  *Planned in:* BL-16
- **BankLedger-A-07** `low` (audit BL-42; confirmed) — BankLedger.toc: the load-bearing position of settings\Slash.lua (reads NS.SchemaRuntime.* at file load) is unannotated (new with the v1.55.0 Schema adoption)  
  *Where:* BankLedger.toc:89-90; settings/Slash.lua:438-454; settings/Schema.lua:580  
  *Evidence:* Slash.lua hands SchemaRuntime.Get, Set, FindRow, AllRows, ApplyDefault, BulkBegin and BulkEnd to lib:New at load. Its comment at :452 relies on the TOC order, but the TOC says nothing. The sibling OptionsSetup is annotated. It arrived in 0d9d1e6.  
  *Remediation:* S4-3: add a comment above settings\Slash.lua: 'LOAD-BEARING: hands NS.SchemaRuntime's members to LibKa0s-Slash at file load; settings\Schema.lua above builds it'.  
  *Rule:* toc-file-§5  
  *Planned in:* BL-16

**ConsumableMaster**

- **ConsumableMaster-A-16** `low` (audit CM-83; confirmed) — Conventional TOC groups (# Locales, # Modules, the four # Settings page files) carry no 'conventional' note  
  *Where:* ConsumableMaster.toc:57-58; ConsumableMaster.toc:166-176; ConsumableMaster.toc:202-205  
  *Evidence:* The load-bearing MUST holds; this is the SHOULD half. Open since 2026-09-08.  
  *Remediation:* B10 / S4-5: add one comment per group above locales\enUS.lua, modules\Ranker.lua and settings\General.lua. Comment only, with no line moves.  
  *Rule:* toc-file-§5  
  *Planned in:* CM-24

**KickCD**

- **KICKCD-A-16** `low` (audit KICKCD-C-16; confirmed) — Load-bearing TOC position with no annotation: modules\IconGrid_Layout.lua calls NS:GetModule('IconGrid') at file scope  
  *Where:* KickCD.toc:96, modules/IconGrid_Layout.lua:15  
  *Evidence:* Non-silent GetModule raises if IconGrid.lua has not loaded, so the position is load-bearing. This is the root of the four C-16a-d dependents.  
  *Remediation:* D5/Sprint 3.1: add '# LOAD-BEARING POSITION: the IconGrid_* / Castbar_* siblings call NS:GetModule(<parent>) at file scope, so each follows its parent' above the IconGrid group (:96-97) and the Castbar group (:99-101). Two comments close the root and all four dependents.  
  *Rule:* toc-file-§5  
  *Planned in:* KC-23
- **KICKCD-A-17** `low` (audit KICKCD-C-16a; confirmed) — Unannotated load-bearing TOC position: modules\IconGrid_Render.lua (derived from C-16)  
  *Where:* KickCD.toc:97, modules/IconGrid_Render.lua:19  
  *Evidence:* NS:GetModule('IconGrid') at file scope.  
  *Remediation:* Same comment as A-16 (IconGrid group).  
  *Rule:* toc-file-§5  
  *Planned in:* KC-23
- **KICKCD-A-18** `low` (audit KICKCD-C-16b; confirmed) — Unannotated load-bearing TOC position: modules\Castbar_Handle.lua (derived from C-16)  
  *Where:* KickCD.toc:99, modules/Castbar_Handle.lua:24  
  *Evidence:* NS:GetModule('Castbar') at file scope.  
  *Remediation:* Same comment as A-16 (Castbar group).  
  *Rule:* toc-file-§5  
  *Planned in:* KC-23
- **KICKCD-A-19** `low` (audit KICKCD-C-16c; confirmed) — Unannotated load-bearing TOC position: modules\Castbar_Skin.lua (derived from C-16)  
  *Where:* KickCD.toc:100, modules/Castbar_Skin.lua:53  
  *Evidence:* NS:GetModule('Castbar') at file scope.  
  *Remediation:* Same comment as A-16 (Castbar group).  
  *Rule:* toc-file-§5  
  *Planned in:* KC-23
- **KICKCD-A-20** `low` (audit KICKCD-C-16d; confirmed) — Unannotated load-bearing TOC position: modules\Castbar_Debug.lua (derived from C-16)  
  *Where:* KickCD.toc:101, modules/Castbar_Debug.lua:10  
  *Evidence:* NS:GetModule('Castbar') at file scope. The file's own comment says it depends on Castbar.lua loading first; the TOC line does not.  
  *Remediation:* Same comment as A-16 (Castbar group).  
  *Rule:* toc-file-§5  
  *Planned in:* KC-23
- **KICKCD-A-21** `low` (audit KICKCD-A-02; confirmed) — TOC groups (Locales, Defaults, Modules, Settings past Panel, unannotated Core lines) carry no conventional-position note  
  *Where:* KickCD.toc:39, KickCD.toc:43, KickCD.toc:54-56, KickCD.toc:65-68, KickCD.toc:89, KickCD.toc:93, KickCD.toc:120-127  
  *Evidence:* Only EnvSetup, PoolSetup and LauncherSetup carry conventional notes. Graded as one SHOULD row for the file. Carried over from the prior audit.  
  *Remediation:* D5/Sprint 3.2: add one comment per group (Locales: read via NS.L, free within group; Defaults: read at call time by Database; Modules: parents are free relative to each other; Settings past Panel: free; Core: 'lines without a LOAD-BEARING POSITION: comment are conventional'). Fold this into the same edit as A-16.  
  *Rule:* toc-file-§5 (SHOULD)  
  *Planned in:* KC-23

**LootHistory**

- **LootHistory-A-04** `low` (audit LH-56; corrected) — core\CoreSetup.lua load-bearing TOC position is unannotated  
  *Where:* LootHistory.toc:48, core/CoreSetup.lua:180, core/Namespace.lua:18  
  *Evidence:* core/CoreSetup.lua:180 builds the printer at file scope with lib:New({ prefix = NS.PREFIX }), where NS.PREFIX is published by core/Namespace.lua:18. TOC line 48 is bare.  
  *Remediation:* Add a comment above LootHistory.toc:48 naming both constraints: 'LOAD-BEARING: lib:New{ prefix = NS.PREFIX } runs at file load (core\Namespace.lua must be above), and NS.Print, published here, is captured as a file-scope local by modules\Browser.lua, settings\Schema.lua and settings\Slash.lua (must be below them).' Put it in one TOC commit with A-05, A-06 and A-07, and keep the tests/test_harness.lua TOC-derivation cases green.  
  *Rule:* toc-file-§5 (MUST)  
  *Planned in:* LH-27
- **LootHistory-A-05** `low` (audit LH-57; confirmed) — core\DebugLogSetup.lua load-bearing TOC position is unannotated  
  *Where:* LootHistory.toc:56, core/DebugLogSetup.lua:90, core/Constants.lua:64  
  *Evidence:* The file-load lib:New{...} descriptor at core/DebugLogSetup.lua:76-90 reads NS.Constants.FONT_MONO, which is resolved at core/Constants.lua:64. TOC line 56 is bare.  
  *Remediation:* Add a comment above LootHistory.toc:56: LOAD-BEARING: the descriptor reads NS.Constants.FONT_MONO at :New; core\Constants.lua must be above. Same commit as LH-56.  
  *Rule:* toc-file-§5 (MUST)  
  *Planned in:* LH-27
- **LootHistory-A-06** `low` (audit LH-63; corrected) — settings\Slash.lua load-bearing TOC position is unannotated  
  *Where:* LootHistory.toc:87, settings/Slash.lua:355, settings/Slash.lua:358, settings/Slash.lua:415, settings/Schema.lua:739  
  *Evidence:* The dispatcher is built at file scope with commands = NS.COMMANDS (assigned at Schema.lua:739) and brandName = NS.BRAND. Moved above Schema, it would get nil and every verb would silently go unknown. TOC line 87 is bare.  
  *Remediation:* Add a comment above LootHistory.toc:87: 'LOAD-BEARING: the dispatcher is built at file load with commands = NS.COMMANDS, assigned by settings\Schema.lua; below Schema, LibKa0s-Slash :New raises and /lh is never registered.' Land it in the same TOC commit as A-04.  
  *Rule:* toc-file-§5 (MUST)  
  *Planned in:* LH-27
- **LootHistory-A-07** `low` (audit LH-58; confirmed) — Conventional TOC groups don't say they are conventional; PoolSetup comment claims a position (dependent of LH-56)  
  *Where:* LootHistory.toc:29, LootHistory.toc:67, LootHistory.toc:57  
  *Evidence:* # Locales (:29), # Defaults (:67) and the plain # Core run (Constants, Namespace, State, Util, LootHistory, Database) carry no 'free to move' statement. The PoolSetup comment at :57 states a position, but nothing resolves at load: every NS.Pool call is inside a function. SHOULD, derived from LH-56.  
  *Remediation:* In the LH-56 commit, add a one-line conventional note per group and reword the PoolSetup comment as conventional.  
  *Rule:* toc-file-§5 (SHOULD)  
  *Planned in:* LH-27

**MultiMeters**

- **MultiMeters-A-22** `low` (audit MM-A-22; confirmed) — Three load-bearing TOC positions carry no at-line comment, and conventional groups have no 'conventional' marker  
  *Where:* MultiMeters.toc:134; MultiMeters.toc:58; MultiMeters.toc:51; MultiMeters.toc:52-56; MultiMeters.toc:128-131  
  *Evidence:* settings/OptionsSetup.lua: page files capture NS.Helpers at file scope. core/PerfSetup.lua: the descriptor reads NS.Version() at file scope. core/CoreSetup.lua: defines NS.LIBKA0S_MISSING, which DebugLogSetup and LauncherSetup read at file scope.  
  *Remediation:* Add three at-line LOAD-BEARING comments naming what resolves at load, plus one 'conventional' note per group. Optionally add pair assertions to tests/test_loadorder.lua.  
  *Rule:* toc-file-§5; anti-pattern #66  
  *Planned in:* MM-24

**PanelMaster**

- **PanelMaster-A-02** `low` (audit PM-036; confirmed) — The load-bearing TOC position of settings\Slash.lua (after Schema) has no comment  
  *Where:* PanelMaster.toc:97, settings/Slash.lua:532, settings/Slash.lua:554-558, settings/Schema.lua:375  
  *Evidence:* Slash.lua builds its dispatcher at file scope from NS.SchemaRuntime members, which Schema.lua publishes, so Schema must load first. Only the OptionsSetup comment states the Schema ordering. The position became load-bearing with the Schema adoption (af8a935).  
  *Remediation:* Add a comment above PanelMaster.toc:97: '# Slash AFTER Schema, load-bearing: its dispatcher descriptor takes NS.SchemaRuntime's members as VALUES at file load (settings/Slash.lua:554-558).' tests/test_harness.lua already pins TOC order.  
  *Rule:* toc-file-§5  
  *Planned in:* PM-14
- **PanelMaster-A-03** `low` (audit PM-037; confirmed) — The load-bearing TOC position of core\Util.lua (after Constants) has no comment, and the conventional groups have no notes  
  *Where:* PanelMaster.toc:56, PanelMaster.toc:53, core/Util.lua:4  
  *Evidence:* core/Util.lua:4 captures local C = NS.Constants at file scope; if Util loaded above Constants the upvalue would be nil forever. The existing comment at :57-58 names Util only as a predecessor of CoreSetup. SHOULD, folded in: the Namespace/State/PanelMaster/Database, Defaults and Modules groups carry no 'conventional' note.  
  *Remediation:* Add a comment above :56 naming the NS.Constants file-scope upvalue dependency, and a single 'conventional from here' note for each unannotated group.  
  *Rule:* toc-file-§5  
  *Planned in:* PM-14

**PartyFrameEnhanced**

- **PartyFrameEnhanced-A-07** `low` (audit PFE-16; confirmed) — The TOC load-order comment names the wrong file: LifecycleSetup's load-bearing position (Perf needs NS.lifecycle) is unannotated and unpinned  
  *Where:* PartyFrameEnhanced.toc:57-59; core/PerfSetup.lua:56; libs/LibKa0s/Perf.lua:342; core/LifecycleSetup.lua:13-14; tests/test_loadorder.lua  
  *Evidence:* The comment at :57 ('publishes NS.Perf…') sits above core\LifecycleSetup.lua. PerfSetup reads NS.lifecycle at file scope, and Perf raises without it. No load-order case names LifecycleSetup.  
  *Remediation:* Audit Sprint 3.1: put a 'LOAD-BEARING: publishes NS.lifecycle, which core\PerfSetup.lua hands LibKa0s-Perf-1.0 at file load' note above LifecycleSetup, and move the NS.Perf note directly above PerfSetup. Add a tests/test_loadorder.lua case, 'LifecycleSetup loads before PerfSetup, and the TOC says why', in the shape of the MediaSetup case at :41.  
  *Rule:* toc-file-§5  
  *Planned in:* PF-20

**PrettyChat**

- **PRETTYCHAT-A-03** `low` (audit PC-77 (PRETTYCHAT-C-01); confirmed) — TOC: load-bearing core\CoreSetup.lua position has no comment  
  *Where:* PrettyChat.toc:53, core/PrettyChat.lua:14, core/CoreSetup.lua:142, docs/ARCHITECTURE.md:35, docs/ARCHITECTURE.md:43  
  *Evidence:* CoreSetup must follow core\PrettyChat.lua, because NewAddon's AceConsole embed overwrites NS.Print and CoreSetup's last line reclaims it. If it is moved earlier, nothing errors, but every chat line turns green with a trailing colon (anti-pattern #36).  
  *Remediation:* Add an at-line comment above core\CoreSetup.lua naming what resolves. Comment only, no reordering. Do it in the same edit as PC-78/79/80/60, and align ARCHITECTURE.md:35 and module-map.md load order with the TOC. Optionally add a test_doc_structure case pinning the hub's load-bearing list against the TOC comments.  
  *Rule:* toc-file-§5  
  *Planned in:* PC-18
- **PRETTYCHAT-A-04** `low` (audit PC-78 (derived from PC-77); confirmed) — TOC: load-bearing core\DebugLogSetup.lua position has no comment  
  *Where:* PrettyChat.toc:54, core/DebugLogSetup.lua:128, docs/ARCHITECTURE.md:44  
  *Evidence:* The descriptor reads NS.Const.FONT_MONO at file scope, so the file must follow core\Constants.lua.  
  *Remediation:* Add an at-line comment naming NS.Const.FONT_MONO (and noting that NS.State/NS.Print are read at call time).  
  *Rule:* toc-file-§5  
  *Planned in:* PC-18
- **PRETTYCHAT-A-05** `low` (audit PC-79 (derived from PC-77); confirmed) — TOC: load-bearing settings\OptionsSetup.lua position has no comment  
  *Where:* PrettyChat.toc:78, settings/OptionsSetup.lua:271-277, settings/OptionsSetup.lua:312, docs/ARCHITECTURE.md:45  
  *Evidence:* It takes NS.SchemaRuntime.Get/Set/ApplyDefault/AllRows as values at load and calls NS.Schema.InstallMasterControls at file scope, so it must follow settings\Schema.lua.  
  *Remediation:* Add an at-line comment naming the runtime members and InstallMasterControls.  
  *Rule:* toc-file-§5  
  *Planned in:* PC-18
- **PRETTYCHAT-A-06** `low` (audit PC-80 (derived from PC-77); confirmed) — TOC: load-bearing settings\Slash.lua position has no comment  
  *Where:* PrettyChat.toc:79, settings/Slash.lua:265-269  
  *Evidence:* On the library path, the descriptor takes NS.SchemaRuntime Get/Set/FindRow/AllRows/ApplyDefault as values at file load.  
  *Remediation:* Add an at-line comment naming the runtime members.  
  *Rule:* toc-file-§5  
  *Planned in:* PC-18
- **PRETTYCHAT-A-24** `low` (audit PC-60 (PRETTYCHAT-A-01, carried); corrected) — TOC groups lack conventional-position notes (# Core, # Modules, # Settings)  
  *Where:* PrettyChat.toc:55-61, PrettyChat.toc:62-67, PrettyChat.toc:73, PrettyChat.toc:76  
  *Evidence:* # Core says nothing about Constants/Namespace/State/Database/PrettyChat. # Modules says only 'the override pipeline'. # Settings still says 'depend on everything else being initialized'. SHOULD.  
  *Remediation:* Add one conventional-position note per group to PrettyChat.toc, in the shape of # Locales (:31). Put one on the # Core header (:34) covering Constants/Namespace/State/Database/PrettyChat/CoreSetup/DebugLogSetup, whose positions are fixed only by the annotated lines above them. Put one on # Modules (:73). On # Settings (:76), say that Schema/OptionsSetup/Slash are conventional and only Panel (:80-83) is load-bearing. Do this in the same edit as PC-77..80.  
  *Rule:* toc-file-§5 (conventional groups)  
  *Planned in:* PC-18

**WhatGroup**

- **WHATGROUP-A-09** `low` (audit WG-70; confirmed) — core\Compat.lua TOC position is load-bearing and unannotated  
  *Where:* WhatGroup.toc:42, WhatGroup.toc:41, core/WhatGroup.lua:87  
  *Evidence:* core/WhatGroup.lua:87 calls NS.Compat.AddOnLinkType() at file load, so Compat must load first; TOC line carries no comment. core\Util.lua (:41) conventional and unannotated (SHOULD, not filed separately).  
  *Remediation:* Add a comment above WhatGroup.toc:42 naming NS.Compat.AddOnLinkType() and core/WhatGroup.lua:87 as load-bearing; add a conventional note above :41 for core\Util.lua. tests/test_harness.lua already pins the load list.  
  *Rule:* toc-file-§5 (MUST)  
  *Planned in:* WG-20


### C06 — Stand-down leaves timers, callbacks, drivers and frames armed

slash-commands-§7 requires a disable to cancel every timer, unregister every callback and driver, and hide every owned frame. Instead, addons gate uncancellable C_Timer.After callbacks, EventRegistry callbacks and secure state drivers on the latch, rebuild per-unit frames on every enable, or leave capture context armed. The conformance tests miss these because their survey cannot see such registrations. Affects AuraMaster, BankLedger, ConsumableMaster, KickCD, MultiMeters, PartyFrameEnhanced and WhatGroup.

**AuraMaster**

- **AuraMaster-A-03** `low` (audit AM-24; confirmed) — Two one-shot C_Timer.After callbacks armed before a stand-down cannot be canceled and wake up to find the latch  
  *Where:* modules/ContainerManager.lua:155 (C_Timer.After(0, CM.FlushPending)); modules/ContainerManager.lua:253; modules/ContainerManager.lua:557-563 (CM.StopListening); modules/TimedSpells.lua:106 (C_Timer.After(0.5, scanTick)); modules/TimedSpells.lua:94-97; modules/TimedSpells.lua:131-134; modules/TimedSpells.lua:162-164  
  *Evidence:* FlushPending returns on NS.IsStoodDown() and scanTick drops on its listening guard. The file's own comment admits C_Timer.After returns no handle to cancel. The standard says timers must not be 'left armed to wake up and find a flag'. Graded Low: each wakes at most once and never re-arms.  
  *Remediation:* Switch both to C_Timer.NewTimer handles: flushTimer = NewTimer(0, fn) and scanTimer = NewTimer(0.5, scanTick). Cancel them in CM.StopListening and TS.Stop, and reset the scheduled and scanScheduled flags on cancel so the stand-up's RequestApply(nil, true) is not swallowed. Keep the listening guard as defence in depth and rewrite the :162-164 comment. Confirm the kit mock's C_Timer.NewTimer handle :Cancel() removes it from __timers(); if it does not, that is an upstream testkit item. Test: test_disabled step 4 arms both before disabling and asserts __timers() is empty (red under: C_Timer.After). Step 9 re-enable still passes.  
  *Rule:* slash-commands-§7 (every timer is canceled)  
  *Planned in:* AM-06
- **AuraMaster-R-08** `low` (review F-006; confirmed) — CM.Init and CM.Announce build container frames while the addon is stood down, contradicting the doc comment  
  *Where:* core/AuraMaster.lua:51; modules/ContainerManager.lua:568-569 (comment); modules/ContainerManager.lua:575 (CM.Sync)  
  *Evidence:* CM.Init runs whatever the latch says. A player who logs in disabled, or switches profile while disabled, gets an anchor and a drag handle per container, left in CreateFrame's default shown state. They are empty and invisible. The comment says Init is called 'only when the addon is actually running'. The disabled suite covers only enabled->disabled.  
  *Remediation:* C-06: when NS.IsStoodDown(), CM.Init returns after EnsureAuraContainer + TimedSpells.Sync, and CM.Announce skips CM.Sync. LifecycleSetup standUp calls NS.ContainerManager.Sync() before ApplyVisibility. Fix the :568-569 doc. Test: log in disabled, spyCreate 'AuraMasterAnchor' counts 0; on enable the instances exist and draw (red under: CM.Init building before the latch check).  
  *Rule:* slash-commands-§7 (nothing built/armed while down); performance-§6  
  *Planned in:* AM-04

**BankLedger**

- **BankLedger-R-01** `medium` (review F-001; corrected) — Stand-down leaves the capture context armed (openContext, lastSnapshot, _settleSince, sessionActive), so re-enabling records movements made while disabled  
  *Where:* core/BankLedger.lua:146-191; modules/Ledger.lua:750-815; core/State.lua:16,21,41; tests/test_disabled.lua:159-546  
  *Evidence:* NS.StandDown never clears these fields. A headless repro shows a deposit made while disabled written as 1 ledger row after re-enable at the same bank visit. Disabling at a bank, closing it and re-enabling elsewhere leaves openContext=BANK_FRAME, so every BAG_UPDATE_DELAYED or PLAYER_MONEY, in combat too, schedules a full rescan. That undercuts the performance-§12 exemption premise. sessionActive stays true, so later rows append to the old visit. None of the 11 test_disabled cases opens a storage context.  
  *Remediation:* C-01: add L:DropContext() in modules/Ledger.lua. It cancels the pending reconcile, nils openContext, lastSnapshot and _settleSince, and fires SessionChanged(false) if a context was open. Call it as step 3b inside NS.StandDown, before the bus targets are dropped. There is no second teardown path and no CloseContext flush. Add 2 test_disabled cases with red-under comments (1017 to 1019), regenerate docs/test-cases.md, move the badge, and update the ARCHITECTURE stand-down section. Smoke test C-01, cases A and B.  
  *Rule:* slash-commands-§7 (What MUST stand down); performance-§6; performance-§12; testing-§12  
  *Planned in:* BL-03
- **BankLedger-R-05** `low` (both F-009, BL-46; confirmed) — The retention prune's C_Timer.After(5) survives the stand-down (gated, not cancelled), and the cleanupDone latch set before the timer skips the prune for the whole session  
  *Where:* core/BankLedger.lua:216-229 (latch :218, C_Timer.After :220, IsStoodDown check :221-225); core/State.lua; docs/performance.md:47  
  *Evidence:* C_Timer.After cannot be cancelled. A disable within 5 s of the first loading screen leaves it armed, and its body finds a flag and returns. That is exactly the shape slash-commands-§7 forbids. Every other timer goes through AceTimer and StandDown's CancelAllTimers (:151-155). Because cleanupDone=true is set before the timer, retention is also skipped until the next session (review F-009).  
  *Remediation:* Audit (BL-46): schedule through NS.addon:ScheduleTimer(fn, 5) (or keep a C_Timer.NewTimer handle) so NS.StandDown cancels it. Keep the IsStoodDown belt, and clear cleanupDone on cancel or document the skip. Review (C-07): move the latch inside the timer with a session-only cleanupPending flag in core/State.lua, so a stand-down postpones rather than cancels. Retry on the next PEW. Combine the two: an AceTimer-armed prune plus the latch set only when the prune runs. Add a falsification case ('stand-down inside the prune window postpones rather than cancels'; red under C_Timer.After), +1 test. Update docs/performance.md:47. Smoke test C-07. Do this after R-06, the mock fix.  
  *Rule:* slash-commands-§7 (every timer is canceled, not left armed to find a flag); testing-§12  
  *Planned in:* BL-01

**ConsumableMaster**

- **ConsumableMaster-A-01** `medium` (audit CM-84; confirmed) — Macro-bar flyout attribute drivers (kcmCombat) stay registered while the addon is disabled; nothing unregisters them  
  *Where:* modules/MacroBarFlyout.lua:289-290; modules/MacroBarButton.lua:463; modules/MacroBar.lua:453-460  
  *Evidence:* RegisterAttributeDriver(flyout, 'kcmCombat', '[combat] 1; 0') runs once per slot, up to 15 slots. There is no UnregisterAttributeDriver anywhere in the tree. The disable path unregisters the bar's visibility state driver and clears OnUpdate, but never reaches the flyouts. The secure state-driver manager keeps evaluating these after the player disables the addon.  
  *Remediation:* B1 / S2-1: add FO.StandDown and FO.StandUp, plus a module-level FLYOUT_COMBAT_DRIVER constant, to modules/MacroBarFlyout.lua. Call FO.StandDown for every built flyout from MB.Update's disable branch, which is already combat-deferred. Re-arm them on the enable path through ensure() and applyVisibility(). Keep the frames rather than rebuilding them. Re-run smoke test §11e.  
  *Rule:* slash-commands-§7 (What MUST stand down)  
  *Planned in:* CM-06
- **ConsumableMaster-A-09** `low` (audit CM-85 (derived from CM-84); confirmed) — tests/test_disabled.lua passes over the flyout attribute-driver survivor; it never reads mock.attributeDrivers  
  *Where:* tests/test_disabled.lua:209-224 (:222-223); tests/wow_mock.lua:823-830  
  *Evidence:* Step 4 checks only the bar's OnUpdate and mock.stateDrivers[bar].visibility.  
  *Remediation:* S2-2: step 4 asserts kcmCombat is set on at least one flyout before disabling (a non-empty baseline) and absent from every flyout after. Step 9 asserts the drivers come back on re-enable. Add the falsification comment 'red under: drop FO.StandDown from MB.Update's disable branch'.  
  *Rule:* slash-commands-§7 (conformance test); testing-§12  
  *Planned in:* CM-06

**KickCD**

- **KICKCD-R-03** `medium` (both F-003; KICKCD-C-03; confirmed) — Per-unit cast-event frames are rebuilt on every enable, leaking 36 frames per disable/enable cycle  
  *Where:* core/Util.lua:437-445, modules/IconGrid.lua:810-822, modules/IconGrid.lua:831-832, modules/IconGrid.lua:860-861, modules/Castbar.lua:1016-1031, modules/Castbar.lua:1044-1045, modules/Castbar.lua:1109-1110, modules/Castbar.lua:1136  
  *Evidence:* Util.RegisterUnitCastEvent calls CreateFrame('Frame') per event: IconGrid makes 8 per unit and Castbar 10. DisableUnit and Suspend drop them with inst.eventFrames = {}. Scratch measurement: 142 -> 178 -> 214 -> 250 frames, +36 per cycle. Reached through /kcd disable+enable, the per-unit Enable toggles, a profile switch that flips enabled, and each /kcd perf suspend/resume. The helper also accepts any eventName, which is the shape of the forbidden 'general-purpose private-frame factory'. test_disabled counts registrations by name only, so it cannot see orphaned frames.  
  *Remediation:* Review C-03 / audit D1: hold one filter frame per (module, unit) on inst (Util.UnitCastFilter or Util.NewUnitFilter with Arm/Disarm), created once. Re-register events on EnableUnit/Resume and UnregisterAllEvents on teardown. Use a file-scope route map so enable allocates nothing (AP #43). Change the Resume guard at Castbar.lua:1136 to an armed flag. Narrow the helper to the cast family, or document its one job. Route the RegisterUnitEvent calls through the pcall-isolated helper (A-03). Test: CreateFrame count across two disable/enable cycles adds 0; it must be red on HEAD. Add a test_util idempotency case for Arm/Disarm. Update the per-unit frames paragraph in docs/ARCHITECTURE.md.  
  *Rule:* events-frames-taint-§1 (unit-filter carve-out reuse MUST); slash-commands-§7  
  *Planned in:* KC-05
- **KICKCD-R-17** `low` (review F-017; confirmed) — A disabled-at-login addon re-registers a PLAYER_LOGIN that will never fire  
  *Where:* core/State.lua:213, core/KickCD.lua:109  
  *Evidence:* `if not State.__seeded then boot:RegisterEvent('PLAYER_LOGIN') end` in State.StandUp. The first hold is taken inside PLAYER_LOGIN itself, so the 'enabled again before login' case cannot occur, and a dead registration is left behind.  
  *Remediation:* C-10: drop the PLAYER_LOGIN re-registration in State.StandUp; the InCombatLockdown() seed on the next line covers it. Coordinate with A-04 (the State boot frame may move to an AceEvent target).  
  *Rule:* slash-commands-§7  
  *Planned in:* KC-07

**MultiMeters**

- **MultiMeters-R-05** `low` (review F-005; corrected) — A window created while the addon is stood down is armed with an OnUpdate  
  *Where:* modules/Window.lua:1382; modules/WindowManager.lua:253; modules/WindowManager.lua:341; modules/Window.lua:1420-1424  
  *Evidence:* Window.New calls inst.frame:SetScript('OnUpdate', onUpdate) unconditionally. Create and Duplicate are reachable from the settings panel while disabled. Reproduced headless: the OnUpdate is left armed.  
  *Remediation:* C-01: arm OnUpdate only when not NS.IsStoodDown(). Stand-up already re-arms it via WindowManager:Resume. Test: Create while disabled leaves no OnUpdate, and after enable every instance has one. Smoke test SM-03.  
  *Rule:* slash-commands-§7 (every OnUpdate cleared)  
  *Planned in:* MM-01
- **MultiMeters-R-08** `low` (review F-008; corrected) — The remembered roster (db.global.roster) is persisted with no bound and is never cleared at login  
  *Where:* modules/Roster.lua:355-361; modules/Roster.lua:572-582; modules/Roster.lua:621; modules/Roster.lua:628-630; modules/Roster.lua:489; modules/Roster.lua:506; modules/Roster.lua:519  
  *Evidence:* Every build() records each member into seenMap.byGuid, which is cleared only by Roster.Forget on METER_RESET. IsGroupMember falls back to the remembered map, so players from earlier sessions may pass the group filter. Unverified: whether DAMAGE_METER_RESET fires at login.  
  *Remediation:* C-14, blocked on smoke test SM-06. If the meter is empty after a fresh login, call Roster.Forget() on ENTERING_WORLD with isLogin. If the data survives logout, cap the map (for example, prune entries not in the live roster above 4 x MAX_ROWS). Add a case in either branch. No SavedVariables write from a game event while disabled.  
  *Rule:* slash-commands-§7  
  *Planned in:* MM-21

**PartyFrameEnhanced**

- **PartyFrameEnhanced-R-03** `low` (both F-005, PFE-12; corrected) — The stand-down leaves the EditMode.Exit EventRegistry callback registered, and burst() keeps arming two C_Timer.After timers while the addon is disabled  
  *Where:* modules/Providers.lua:342-343, :348-353 (Suspend), :355-359 (Resume), :61-67 (burst), :65-66  
  *Evidence:* `pcall(EventRegistry.RegisterCallback, EventRegistry, "EditMode.Exit", burst, Providers)` is registered once in OnEnable. Suspend runs only ev:UnregisterAllEvents(). burst() bumps burstGen and arms two C_Timer.After calls even while suspended. The callback has a real unregister, so the hooksecurefunc carve-out does not apply. The audit graded this Medium (MUST).  
  *Remediation:* C-004 / T-4 / audit Sprint 1.4: add a registerEditMode(on) or registerCallbacks()/unregisterCallbacks() pair behind the presence guard and pcall. Call it from OnEnable/Resume, and call the unregister from Suspend. burst() returns before it touches burstGen or timers while suspended. Add `-- red under: drop unregisterCallbacks() from Providers:Suspend` / `-- red under: drop the suspended guard in burst`. Rejected: an addon-side tracked-callback helper, which would be a second stand-down record (anti-pattern #85). If one is wanted, it belongs as a LibKa0s Bus minor.  
  *Rule:* slash-commands-§7; anti-pattern #85  
  *Planned in:* PF-05
- **PartyFrameEnhanced-R-06** `low` (review F-006; corrected) — The stand-down replaces the target and pet buttons' secure state drivers with 'hide' instead of unregistering them  
  *Where:* modules/UnitButtons.lua:41-60; modules/TargetFrames.lua:269-279; modules/PetFrames.lua:150-160; .luacheckrc:31  
  *Evidence:* Driver returns 'hide' when not allowed, and ApplyDriver re-registers it, so ten state drivers stay registered while the addon is disabled. UnregisterStateDriver is declared in .luacheckrc but never called. slash-commands-§7 requires state drivers to be stood down where they can be, which is out of combat.  
  *Remediation:* C-005 / T-5, after T-3 and T-1: while suspended, refresh calls UnitButtons.Release(btn). Through NS.RunSecure('driver:'..key) it runs UnregisterStateDriver(btn,'visibility'), btn:Hide() and clears __driver, and it sets __driverWant=nil at request time. Stand-up re-registers through refresh. Add tests in tests/test_disabled.lua: no __drivers.visibility after an out-of-combat disable, re-enable restores the driver, and the in-combat variant completes after OnLeaveCombat. Mark them `-- red under: keep the "hide" driver`. Needs a combat smoke test (S-005).  
  *Rule:* slash-commands-§7, events-frames-taint-§2  
  *Planned in:* PF-04
- **PartyFrameEnhanced-A-01** `low` (audit PFE-13; confirmed) — Eight container frames the addon owns (five fade frames, three free-placement holders) stay shown while it is disabled  
  *Where:* modules/RangeFade.lua:11, :55; modules/Anchor.lua:232; tests/test_disabled.lua (step 5)  
  *Evidence:* `f = CreateFrame("Frame", "PartyFrameEnhanced_Fade_" .. unit, UIParent)` carries the comment 'never hidden'. The holders are never hidden on any path either. The frames are empty and take no mouse, so nothing is visible, but the MUST says every owned frame is hidden. The suite cannot see this because the kit mock creates frames hidden.  
  *Remediation:* Audit Sprint 1.5: RangeFade:Suspend/Resume hides and shows the fade frames, and a new Anchor:Suspend/Resume does the same for the holders, both through NS.RunSecure because they parent or anchor secure buttons. An in-combat stand-down defers to the PLAYER_REGEN_ENABLED flush. Stand-up shows the frames before PublishVisibility. Add explicit step-5 assertions that PartyFrameEnhanced_Fade_* and *_Holder are hidden after disable. Verify in game that an in-combat disable hides them once combat ends.  
  *Rule:* slash-commands-§7 (Every frame the addon owns is hidden)  
  *Planned in:* PF-06
- **PartyFrameEnhanced-A-11** `low` (audit PFE-12b; confirmed) — The Event Subscriptions table omits the EditMode.Exit callback while claiming every row comes off during stand-down (derived from PFE-12)  
  *Where:* docs/ARCHITECTURE.md:149-166, :165  
  *Evidence:* ':165 Every registration in this table except the last comes off while the addon is stood down', yet the table has no EditMode.Exit row.  
  *Remediation:* Audit Sprint 4.2: add an EditMode.Exit (EventRegistry callback) row under modules/Providers.lua. Once PFE-12 is fixed, :165 holds as written.  
  *Rule:* documentation-§3 (Event Subscriptions)  
  *Planned in:* PF-05

**WhatGroup**

- **WHATGROUP-A-01** `low` (audit WG-64; corrected) — EventRegistry 'SetItemRef' callback survives the stand-down, gated by IsStoodDown instead of unregistered  
  *Where:* core/WhatGroup.lua:108-111, core/WhatGroup.lua:96-100, core/WhatGroup.lua:329-349  
  *Evidence:* Registered at file load via EventRegistry:RegisterCallback("SetItemRef", ..., WhatGroup); NS.StandDown never calls UnregisterCallback. Comment claims the hooksecurefunc carve-out, but §7 says it MUST NOT be generalized to APIs with a real unregister; EventRegistry has one (modeled in tests/wow_mock.lua:684-687). Anti-pattern #85. Disabled addon still enters Lua on every addon: link click.  
  *Remediation:* Extract registerLinkCallback() (keep file-load call); NS.StandDown calls EventRegistry:UnregisterCallback("SetItemRef", WhatGroup) when ADDON_LINK_TYPE; NS.StandUp calls registerLinkCallback(). Keep IsStoodDown check for the hooksecurefunc fallback; reword :96-99 comment. Add smoke test (disable, enable, GameMenu Logout, click details link) to docs/smoke-tests.md. If in-client taint appears, revert and file a slash-commands-§7 Documented deviations row instead.  
  *Rule:* slash-commands-§7 (MUST); anti-pattern #85  
  *Planned in:* WG-01
- **WHATGROUP-A-02** `low` (audit WG-65; confirmed) — ARCHITECTURE.md claims only the two hooksecurefunc rows survive the stand-down (derived from WG-64)  
  *Where:* docs/ARCHITECTURE.md:158-161, docs/ARCHITECTURE.md:170, docs/ARCHITECTURE.md:238-241  
  *Evidence:* Hub says every row is gone while disabled except the two hooksecurefunc rows, yet lists the EventRegistry callback at :170 which survives.  
  *Remediation:* After WG-64 fix, rewrite :158-161 and :238-241 so only the two hooksecurefunc rows survive (then true) and move the EventRegistry row at :170 into the gone-while-disabled set.  
  *Rule:* documentation-§5 (MUST), documentation-§3  
  *Planned in:* WG-01
- **WHATGROUP-A-03** `low` (audit WG-66; confirmed) — tests/test_disabled.lua registration survey cannot see EventRegistry callbacks (derived from WG-64)  
  *Where:* tests/test_disabled.lua:76-82, tests/wow_mock.lua:694  
  *Evidence:* regNames reads kit __registrations() and the raw frame stub only; EventRegistry fake's __callbacks is never surveyed, so steps 3, 6, 9 pass with WG-64's survivor. Graduates to a root if WG-64 is closed by a register row.  
  *Remediation:* Test-first: add mock.EventRegistry.__callbacks("SetItemRef") (keyed by owner) to regNames with -- red under: dropping the UnregisterCallback in NS.StandDown; verify red against current code. Optional collection-wide half upstream: add an EventRegistry fake + callback survey (kind="callback") to LibKa0s testkit mock_base.lua/mock_record.lua so consumer fakes can shrink.  
  *Rule:* testing-§12 (MUST); slash-commands-§7 conformance test  
  *Planned in:* WG-01, WG-10


### C07 — Disabled/suspended latch bypassed by UI paths

Show, unlock, test-mode, toggle and reset paths read the wrong enabled predicate or skip the stand-down latch. As a result a disabled (or perf-suspended) addon redraws, arms drag, re-shows windows or loses its settings category. The root cause is several enabled readers instead of one latch-aware seam. Affects AuraMaster, BankLedger, ConsumableMaster, MultiMeters and PanelMaster.

**AuraMaster**

- **AuraMaster-R-09** `low` (review F-007; corrected) — Degraded Lifecycle stub is level-triggered (runs full standUp on every SyncEnabled), where the library is edge-triggered  
  *Where:* core/LifecycleSetup.lua:120-131  
  *Evidence:* NS.SyncEnabled calls standDown or standUp on every call, including OnInitialize before PLAYER_LOGIN and every profile switch. standUp re-registers events, arms an apply timer and re-reparents the Blizzard frames, which means redundant apply passes. It affects only installs where libs/LibKa0s failed LibStub's floor.  
  *Remediation:* Keep a local `down = false` in the degraded branch. SyncEnabled computes want = not enabledStored() and calls standDown/standUp only when want ~= down, then sets down = want. Add the case to tests/test_lifecycle.lua (or whichever suite already loads tests/degraded_env.lua): two unchanged SyncEnabled calls arm one apply timer and register the lifecycle events once. Classify it as correctness (degraded-path parity), not a library-stack-§7 deviation.  
  *Rule:* library-stack-§7 (the stub mirrors the member's contract)  
  *Planned in:* AM-05
- **AuraMaster-R-10** `low` (review F-009; confirmed) — The panel's Test mode checkbox is accepted while the addon is disabled, while /am test and the launcher refuse  
  *Where:* settings/General.lua:107-114; settings/Slash.lua:124-133; core/LauncherSetup.lua:118-122  
  *Evidence:* The row is bound straight to NS.Preview.SetTestMode. Ticking it while disabled silently sets NS.State.testMode = true, and the addon comes back up in test mode when enabled. The state is session-only, with no SavedVariables write.  
  *Remediation:* C-09: row.set refuses turning it on while NS.IsDisabled() and prints NS.Slash.DisabledLine() (one refusal line from the dispatcher). Turning it off stays allowed. Test in test_disabled.lua: a panel set while disabled leaves testMode false and prints one refusal line.  
  *Rule:* slash-commands-§2/§7; launcher-§2  
  *Planned in:* AM-09

**BankLedger**

- **BankLedger-R-02** `medium` (review F-002; corrected) — 'Reset all settings' while disabled restores settings.enabled=true in the store but never re-runs the latch  
  *Where:* settings/Slash.lua:161-197; settings/Schema.lua:222-226; core/LifecycleSetup.lua:107-110; tests/test_panel.lua:411-720  
  *Evidence:* ResetEverything wipes db.global in place and merges defaults, bypassing the row onChange and NS.ReevaluateEnabled. Repro: stored enabled = true, IsDisabled = true, IsStoodDown = true. The checkbox says enabled while nothing records until /reload or a toggle. None of the 8 ResetEverything cases runs while disabled.  
  *Remediation:* C-02: after the SETTINGS_CHANGED send and before refreshAfterReset(), call NS.ReevaluateEnabled() (as OnProfileReset does). Add a test_panel case 'ResetEverything while disabled stands the addon back up' (+1). Behavior change: a reset made while disabled re-enables. Note it under API/behavior changes. Smoke test C-02. Coordinate with the BL-34 reset unification.  
  *Rule:* options-ui-§12 (indistinguishable from a fresh install); slash-commands-§7 (re-evaluate when the stored switch can change)  
  *Planned in:* BL-04

**ConsumableMaster**

- **ConsumableMaster-R-03** `medium` (both F-003 + CM-86; confirmed) — A settings category parked in combat is never registered while the addon is disabled; the panel and Enable checkbox are gone for the session  
  *Where:* settings/Panel.lua:1267-1269; core/ConsumableMaster.lua:623-657 (replay at :654-656, stood-down early return at :631-635); core/LifecycleSetup.lua:98-100; settings/OptionsShim.lua:233; tests/test_settingsui_optionsui.lua:769-799  
  *Evidence:* registerPanel parks the registration under lockdown (registerPending = true). The only replay is at the end of OnRegenEnabled. The stood-down branch unregisters PLAYER_REGEN_ENABLED and returns before the replay. When the stand-down finished out of combat, no PLAYER_REGEN_ENABLED is registered at all. A probe showed 'stood down: true / parked: true / replays on regen while disabled: 0'. /cm config, bare /cm and the launcher right-click then print the misleading 'settings panel unavailable on this client'. slash-commands-§7 'What MUST survive' names settings-category registration. Existing tests pin the replay only while the addon is enabled.  
  *Remediation:* C-03 / B2: extract the replay into a named helper (replayParkedSettings / replayParkedRegistration) and call it on both branches, before the stood-down return. Extract, do not branch: OnRegenEnabled is at CCN 15 and should drop to about 12. Add KCM.EnsureRegenForParkedSettings() in core/LifecycleSetup.lua, called from registerPanel's park branch, which registers PLAYER_REGEN_ENABLED when stood down. Add red-first cases for a stand-down out of combat and one in combat, with a falsification comment. Add a row to ARCHITECTURE.md 'What SURVIVES'. After upstream A3 lands, call UI.ReplayPending() instead. Run smoke test §6a with the addon disabled.  
  *Rule:* slash-commands-§7 (What MUST survive); performance-§11; anti-pattern #52; automated-tests-§3  
  *Planned in:* CM-05
- **ConsumableMaster-R-04** `low` (review F-004; corrected) — The settings panel opened while disabled cannot hydrate item rows ([Loading]), and the code comment claims it can  
  *Where:* core/ConsumableMaster.lua:213-218; core/ConsumableMaster.lua:659-678; core/LifecycleSetup.lua:92; settings/OptionsShim.lua:263-264; modules/KCMItemRow.lua:84-99  
  *Evidence:* The stand-down unregisters GET_ITEM_INFO_RECEIVED and drops the options target's PANEL_REFRESH subscription, and those are the only hydration triggers. Rows opened in a fresh session sit on [Loading]. The comment documents the opposite and cites a toggle onChange in settings/Panel.lua that no longer exists. slash-commands-§7 records the panel-refresh question as 'Recorded, not ruled', so this is a behavior regression plus a false comment, not a compliance finding.  
  *Remediation:* C-04: rewrite the comment truthfully and remove the dead pointer. Add a Known Limitations bullet to docs/ARCHITECTURE.md. Deferred for an owner decision at CP2: panel-owned hydration while disabled through LibKa0s-Item LoadItem (core/ItemSetup.lua:14-16 declines it today). Either open a tracked issue or record the behavior as accepted.  
  *Rule:* slash-commands-§7 (Recorded, not ruled)  
  *Planned in:* CM-14
- **ConsumableMaster-R-07** `low` (review F-007; confirmed) — Standing back up skips login's auto-discovery pass and stale-discovered sweep  
  *Where:* core/LifecycleSetup.lua:110-119; core/ConsumableMaster.lua:582-597 (:587-590)  
  *Evidence:* runAutoDiscovery and Selector.SweepStaleDiscovered run only in OnPlayerEnteringWorld, which does not fire again on re-enable. Non-seeded consumables looted while disabled are not candidates until the next BAG_UPDATE_DELAYED.  
  *Remediation:* C-05: extract P.DiscoverAndSweep(reason), call it from OnPlayerEnteringWorld and from standUp before RequestRecompute, and publish it as KCM.Pipeline.DiscoverAndSweep. Add the case 'Disabled 9c: an item looted while disabled is discovered on the way back up'.  
  *Rule:* performance-§6  
  *Planned in:* CM-07
- **ConsumableMaster-R-10** `low` (review F-010; confirmed) — Bare /cm bar toggle reads the latch-inclusive IsEnabled, so it never toggles off during a perf hold  
  *Where:* core/SlashCommands.lua:904; core/MacroBarModel.lua:146-150  
  *Evidence:* During a perf capture's suspended arm, it writes enabled = true and prints ON every time while the bar stays hidden.  
  *Remediation:* C-09: local on = not (KCM.MacroBarModel.Config() or {}).enabled. Add the case 'bare /cm bar toggles the stored flag during a perf hold'.  
  *Rule:* slash-commands-§5  
  *Planned in:* CM-08
- **ConsumableMaster-R-11** `low` (review F-011; confirmed) — The launcher left-click and /cm unlock unlock a switched-off bar and say 'drag it'  
  *Where:* core/LauncherSetup.lua:180-187; core/SlashCommands.lua:869-870  
  *Evidence:* macroBar.locked is toggled without checking macroBar.enabled, and the same wording is duplicated in runLock.  
  *Remediation:* C-10: keep the write. When cfg.enabled == false, say 'macro bar unlocked (the bar is off — /cm bar on to show it)'. The launcher reuses KCM.SlashCommands.Verbs.RunLock instead of its own copy of the wording. Add a test case.  
  *Rule:* launcher-§2; slash-commands-§5  
  *Planned in:* CM-09

**MultiMeters**

- **MultiMeters-R-02** `high` (review F-002; confirmed) — A disabled addon re-shows its windows when Test mode is unticked, because WindowProto:Show() skips the latch  
  *Where:* modules/WindowManager.lua:659; modules/WindowManager.lua:630; modules/Window_Placement.lua:231-242; settings/Schema_Compose.lua:794-801; libs/LibKa0s/Perf.lua:426  
  *Evidence:* The guard at :659 checks only NS.Perf.suspended (the perf hold) and never NS.IsStoodDown(). WindowProto:Show() calls frame:Show() without consulting NS.ShouldShow. Headless repro: 'windows shown while disabled after test-mode on/off: 1 / 1'. The window stays up because every event is unregistered.  
  *Remediation:* C-01: WindowProto:Show() returns false first when NS.IsStoodDown(). Change WindowManager.lua:659 to use `not (NS.IsStoodDown and NS.IsStoodDown())`. Test in tests/test_disabled.lua: disable mid-session, tick and untick Test mode, and assert no window is shown ('red under' reverting the Show() guard). Keep test_lifecycle.lua:288 and Disabled 5 green. Smoke test SM-01.  
  *Rule:* slash-commands-§7; performance-§6; anti-pattern #85  
  *Planned in:* MM-01
- **MultiMeters-R-04** `medium` (review F-004; confirmed) — During a perf capture's suspended arm, /mm toggle and the launcher's left-click still show windows  
  *Where:* modules/WindowManager.lua:690-708 (:697, :706); core/LauncherSetup.lua:229-237; settings/Slash.lua:254  
  *Evidence:* Feature verbs are refused only while disabled. Under the perf hold, Toggle calls inst:Show(), which bypasses the ladder. Headless repro: 'windows shown during perf suspend after /mm toggle: 1 / 1'. This contaminates arm B of the capture.  
  *Remediation:* C-01: the Show() latch guard, plus M:Toggle returning false with L['Windows are suspended while a performance capture runs.'] when NS.IsStoodDown(). The launcher (LauncherSetup.lua:235-236) prints that err. Add the locale key. Test in tests/test_disabled.lua: under a perf suspend, toggle and launcher onClick show nothing and print the line. Smoke test SM-02.  
  *Rule:* performance-§6; slash-commands-§7  
  *Planned in:* MM-01, MM-02

**PanelMaster**

- **PanelMaster-R-01** `high` (both F-001 / PM-034; confirmed) — A disabled addon still draws, outlines and arms drag on every unlocked panel: Unlock:Decorate overrides the stand-down latch  
  *Where:* modules/Canvas.lua:802, modules/Canvas.lua:823, modules/Unlock.lua:171-177, modules/Unlock.lua:123-126, settings/Schema.lua:503-509, settings/Slash.lua:342, settings/PanelEditor.lua:749-750  
  *Evidence:* Canvas:Render sets spec.shown=false when NS.Lifecycle:IsDown() (:802), then calls NS.Unlock:Decorate(f, rec) (:823). Decorate runs f:Show() and ArmDrag (EnableMouse, SetMovable, RegisterForDrag) and never consults the latch. A headless probe on the real TOC with two panels gave: unlocked then disabled, shown=2; disabled plus per-panel unlock, shown=1; disabled plus Lock frame unticked, shown=2; relocked, shown=0. Three routes reach it: (A) unlock then disable; (B) the Lock frame row or /pm set state.locked false while disabled; (C) the per-panel Unlock tick while disabled. Dragging a panel then writes db.profile.panels while the addon is off.  
  *Remediation:* In Canvas:Render, read the latch once (local down = NS.Lifecycle and NS.Lifecycle:IsDown()). If down, call NS.Unlock:StripOverlay(f); otherwise call NS.Unlock:Decorate(f, rec). Keep the session unlock state (NS.State.unlocked, unlockedPanels) untouched so NS.StandUp -> RenderAll restores the outlines from current state (performance-§6). Rejected alternatives: an imperative Hide or force-lock sweep in NS.StandDown (anti-pattern #85), and per-surface disabled gates. Land it test-first with R-02. Add an unlock-then-disable case to docs/smoke-tests.md.  
  *Rule:* slash-commands-§7 (every frame hidden, enforced at the source); performance-§6; anti-pattern #85  
  *Planned in:* PM-02
- **PanelMaster-R-02** `medium` (both F-006 / PM-034a; confirmed) — The stand-down conformance suite never unlocks a panel, so it stays green against R-01  
  *Where:* tests/test_disabled.lua:221-251, tests/test_disabled.lua:424  
  *Evidence:* The seed()/shownPanels() surveys and step 5 assert zero shown panels only with every panel locked. The only unlock reference is the launcher-refusal case (:424). A conformance suite that stays green while a frame is drawn during stand-down is the testing-§12 'second draw gate' shape. The review grades this Medium; the audit grades it Low as a dependent of PM-034.  
  *Remediation:* Extend step 5 with routes A (unlock, then disable), B (disabled, then S:Set('state.locked', false), and via NS.Slash:OnSlash('set state.locked false')) and C (disabled, then NS.Unlock:SetPanelUnlocked(id, true)). Assert shownPanels() is empty and no panel frame has the mouse enabled. After re-enable, assert the unlocked panels come back decorated (the positive half). Add '-- red under: call Unlock:Decorate unconditionally in Canvas:Render' and watch the cases go red before the fix. Regenerate docs/test-cases.md and the README badge in the same commit.  
  *Rule:* slash-commands-§7 (conformance test); testing-§12; testing-§4  
  *Planned in:* PM-02


### C08 — Disabled refusal line and launcher disabled-state seam

Stub, launcher and Lock-row fallbacks re-spell the collection refusal line by hand instead of using lib.DISABLED_LINE_FORMAT. LibKa0s's launcher has no disabled-state seam, so each host hand-writes the refusal differently; launcher notices repeat, and tooltips offer actions the disabled state refuses. LibKa0s owns the seam (upstream); LootHistory, MultiMeters, PartyFrameEnhanced and WhatGroup consume it.

**LibKa0s**

- **LibKa0s-R-06** `low` (review F-006; corrected) — Launcher click has no disabled-state seam; three hosts hand-write the rung (a)/(b) refusal differently  
  *Where:* LibKa0s/Launcher.lua:178-185; LibKa0s/Launcher.lua:98-127; BankLedger/core/LauncherSetup.lua:156; AuraMaster/core/LauncherSetup.lua:120; AbsorbTracker/core/LauncherSetup.lua:161  
  *Evidence:* launcher-§2 requires a disabled left-click on rung (a)/(b) to be refused with the dispatcher's line; the one OnClick owner (anti-patterns #81) has no isEnabled field, so BankLedger, AuraMaster and AbsorbTracker each gate inside onClick in three spellings; a host that forgets writes SavedVariables while disabled (#85).  
  *Remediation:* C-06 (Launcher minor 1->2): add optional descriptor fields isEnabled (function) and disabledLine (function returning the Slash line); in click, when left button, onClick present and not isEnabled(), emit disabledLine() and return. Rung (c) still expressed by omitting onClick. Tests for rung (a) refused, rung (c) unchanged, right-click unchanged. Consumer follow-up M6-T12: each rung (a)/(b) host passes the two fields and deletes its hand-written gate, one commit per host. Serialize after M5-T1 (shared tests/test_launcher.lua). Smoke S-006.  
  *Rule:* launcher-§1/§2; anti-patterns #81, #85; slash-commands-§7  
  *Planned in:* LK-16
- **LibKa0s-R-09** `low` (review F-009; confirmed) — Launcher missing-library notices repeat on every Register and are double-tagged [LibKa0s]  
  *Where:* LibKa0s/Launcher.lua:203; LibKa0s/Launcher.lua:228; LibKa0s/Launcher.lua:235; LibKa0s/Launcher.lua:70-75  
  *Evidence:* Register is callable from OnInitialize and login, so NO_BROKER/NO_ICON/NO_MINIMAP print twice; strings start "[LibKa0s] %s:" and go through the host's tagged printer. Only reachable where broker libs are missing.  
  *Remediation:* Part of C-06: guard each notice with once[key] per instance; drop the "[LibKa0s] " tag from the values (keys unchanged, L overrides still work). Test one NO_ICON across two Register calls.  
  *Planned in:* LK-16

**LootHistory**

- **LootHistory-R-05** `low` (review F-005; corrected) — Degraded Slash stub refusal line drifted from lib.DISABLED_LINE_FORMAT  
  *Where:* settings/Slash.lua:255-257, libs/LibKa0s/Slash.lua:596, settings/Slash.lua:282-286  
  *Evidence:* The stub renders '... enable it with /lh' while claiming to be byte-identical to the library, which renders '<brand> ... /lh enable'. That breaks the canonical refusal-line shape. On that path, enable itself is unavailable, so the line points at nothing that works. Reachable only on a library-less install with settings.enabled=false.  
  *Remediation:* C-005: format the stub line with '/lh enable' (slash .. ' enable'), and correct the comment to note that enable is unavailable on the library-less path. Better still, drop the stub's own format string. Add a +1 parity case in the degraded block of tests/test_slash.lua comparing the stub output to lib.DISABLED_LINE_FORMAT:format(NS.BRAND, '/lh enable') with the library loaded. Smoke S-005. Re-check after any LibKa0s re-vendor in case the library format moved.  
  *Rule:* slash-commands-§7 (refusal line); library-stack-§7 stub rules  
  *Planned in:* LH-16
- **LootHistory-R-13** `low` (review F-013; confirmed) — Launcher tooltip hard-codes the brand and offers a left-click the disabled state refuses  
  *Where:* core/LauncherSetup.lua:113, core/LauncherSetup.lua:117, core/LauncherSetup.lua:104-106  
  *Evidence:* :113 hard-codes 'Ka0s Loot History' instead of NS.BRAND. :117 says 'Left-click: open the history window' even while disabled, when the click prints the refusal; and the click is a toggle, not an open.  
  *Remediation:* C-012: tt:AddLine(NS.BRAND, 1, 0.82, 0). Change the text to 'Left-click: show/hide the history window'. When NS.AddonIsOff(), replace it with a gray disabled line derived from NS.Slash.DisabledLine() minus the tag, not hand-built. Update tests/test_launcher.lua if it pins the tooltip text. Smoke S-008.2-3.  
  *Planned in:* LH-11

**MultiMeters**

- **MultiMeters-R-06** `low` (review F-006; corrected) — The Slash degradation stub has no DisabledLine, and the launcher calls it through an always-present wrapper  
  *Where:* settings/Slash.lua:185-236; settings/Slash.lua:743; core/LauncherSetup.lua:232; tests/test_surface_parity.lua (header)  
  *Evidence:* The wrapper `function Sl:DisabledLine() return cli:DisabledLine() end` always exists, so the launcher's guard passes and the stub raises 'attempt to call method DisabledLine' on a disabled left-click. This is reachable only when Launcher loads and Slash does not.  
  *Remediation:* C-04: publish Sl:DisabledLine only if cli.DisabledLine exists. Do not add a separate stub wording. Test in tests/test_degraded.lua: remove LibKa0s-Slash from libFiles, disable, call the launcher onClick, and assert no error and no write. Optionally note the coverage in test_surface_parity's header. Smoke test SM-11.  
  *Rule:* testing-§8  
  *Planned in:* MM-02

**PartyFrameEnhanced**

- **PartyFrameEnhanced-A-08** `low` (audit PFE-17; confirmed) — A second, non-standard 'addon is disabled' refusal on the Lock-frame row  
  *Where:* modules/Preview.lua:40, :110, :114; settings/General.lua:115-117  
  *Evidence:* Unticking Lock frame, or `/pfe set locked false`, while disabled prints the gray 'cannot unlock — the addon is disabled' (REFUSED_DISABLED) instead of cli:DisabledLine(). The verbs and the launcher already use the collection line.  
  *Remediation:* Audit Sprint 2.1: NS.AcceptLock's disabled branch (after the combat check) prints the collection line through NS.DisabledLine(), published from settings/Slash.lua and read at call time. Delete REFUSED_DISABLED and its locale key. Add a test_disabled case: NS.SetByPath('locked', false) while disabled prints exactly cli:DisabledLine() and writes nothing.  
  *Rule:* slash-commands-§7 (The refusal line)  
  *Planned in:* PF-07
- **PartyFrameEnhanced-R-11** `low` (both F-010, PFE-23; corrected · upstream → LibKa0s, WowAddonStandards) — The library-absent Slash stub hand-copies LibKa0s's refusal-line format and row shape, and re-implements its dispatcher; slash-commands-§1 and §7 pull in opposite directions  
  *Where:* settings/Slash.lua:325-391, :327, :331, :361-388; libs/LibKa0s/Slash.lua:83; tests/test_surface_parity.lua:77-111  
  *Evidence:* `local DISABLED_LINE = "%s is disabled \226\128\148 enable it with \|cFFFFFF00%s\|r"` copies lib.DISABLED_LINE_FORMAT, and FormatRow copies `cmd — desc`. §1 says a stub MUST NOT re-implement the library's rendering, while §7 requires one collection-wide refusal line even in a degraded build. The parity test pins the drift. The review graded this Low; the audit filed it as Info because it is a question of how two rules interact.  
  *Remediation:* Upstream first. WowAddonStandards rules on the §1/§7 interaction: either slash-commands-§1 names the refusal line as the one string a library-absent stub may carry, or the rule requires LibKa0s to export the refusal shape as data that a host can bundle. LibKa0s documents the prescribed stub shape in its Slash docs 'Degradation' section. Addon side: now, drop the copied FormatRow em-dash formatter in favour of a plainly rendered row, and correct the false comment at settings/Slash.lua:322-324. Leave the DisabledLine wording alone until the standard rules, then adopt exactly what it prescribes. Do not invent a new per-addon refusal sentence. Adjust test_surface_parity to match the ruled shape.  
  *Rule:* slash-commands-§1, slash-commands-§7  
  *Planned in:* LK-18, PF-12

**WhatGroup**

- **WHATGROUP-A-19** `low` (audit WG-81; confirmed) — Launcher fallback re-spells the collection refusal line ('Ka0s WhatGroup is disabled.')  
  *Where:* core/LauncherSetup.lua:148-155  
  *Evidence:* `Sl:DisabledLine() or "Ka0s WhatGroup is disabled."` literal has trailing period and no /wg enable; unreachable today (both Slash branches publish DisabledLine) but a latent second spelling.  
  *Remediation:* Drop the `or` literal at :151-152; if a guard is still wanted, return the degraded Slash stub's own DisabledLine shape (settings/Slash.lua:168-170).  
  *Rule:* slash-commands-§7 (refusal line MUST NOT be re-spelled)  
  *Planned in:* WG-13


### C09 — Test-kit and mock fidelity gaps

The vendored kit's fakes diverge from the client: AceDB CopyProfile/DeleteProfile no-op instead of raising, SetProfile skips removeDefaults, CreateFrame starts frames hidden, there is no EventRegistry recorder, C_Timer.After no-ops, and the mock hard-codes Version. Tests therefore stay green over real bugs. The kit fixes are upstream in LibKa0s (reported by AbsorbTracker and PartyFrameEnhanced); BankLedger, ConsumableMaster and MultiMeters fix their local mocks.

**AbsorbTracker**

- **AbsorbTracker-R-06** `medium` (review F-006; confirmed · upstream → LibKa0s) — [upstream] The test kit's AceDB fake silently no-ops where AceDB-3.0 raises (CopyProfile and DeleteProfile)  
  *Where:* tests/_kit/mock_record.lua:257-270 (LibKa0s testkit/mock_record.lua), tests/_kit/mock_base.lua:26  
  *Evidence:* The fake's db.CopyProfile returns when the source is missing or equals the current profile, and db.DeleteProfile returns when the name is current. Real AceDB raises on self-copy, missing copy source, deleting the active profile, and deleting a missing profile when not silent (AceDB-3.0.lua:531-537, :581-587). This breaks the kit's fidelity rule 5 and is what hides F-002 in every consumer.  
  *Remediation:* U-01: in the LibKa0s repo, make the fake raise with AceDB's verbatim messages at level 2 for all four cases, honouring silent. Bump the kit revision and add a changelog line under docs/api/testkit/. Then re-vendor the whole testkit/ into tests/_kit/ in every consumer, one commit each. Do not edit locally. Sibling suites that go red afterwards are exposing real bugs.  
  *Rule:* testing-§1, testing-§8 (kit fidelity rule 5)  
  *Planned in:* LK-03

**BankLedger**

- **BankLedger-A-03** `low` (audit BL-46a; confirmed) — tests/wow_mock.lua no-ops C_Timer.After, so test_disabled's timer step cannot see a surviving C_Timer.After (derived from BL-46)  
  *Where:* tests/wow_mock.lua:614-617; tests/test_disabled.lua:184-203  
  *Evidence:* The mock replaces the kit's recording C_Timer.After with function() end so the prune never runs in suites. test_disabled then asserts #mocks.__timers() == 0, which cannot count that survivor.  
  *Remediation:* S3-1: drop the override so the kit's recording After stands. Keep the prune from running by not firing it: check which suites call __fireTimers, or filter by delay. Extend test_disabled:184-203 to drive OnEnterWorld before disable() and watch it go red against today's code. Then fix BL-46.  
  *Rule:* testing-§1 (mock fidelity: record rather than no-op); testing-§12  
  *Planned in:* BL-01

**ConsumableMaster**

- **ConsumableMaster-R-06** `low` (review F-006; corrected) — The test harness cannot see F-001, F-002 or F-003: the mock SetProfile skips removeDefaults, and no case covers a per-hand flush or a registration parked while stood down  
  *Where:* tests/wow_mock.lua:491-499; tests/test_macromanager.lua:330-340; tests/test_settingsui_optionsui.lua:777-797  
  *Evidence:* The mock's db.SetProfile merges defaults but never runs removeDefaults over the outgoing profile. A probe against the mock showed the defaults intact (4 entries) where the real AceDB leaves 0. No case flushes a per-hand entry, and no case parks a registration while stood down. The mock is the addon's own file, not the kit.  
  *Remediation:* M0-T2: model AceDB removeDefaults on profile switch in tests/wow_mock.lua (scalar and sub-table arms; note that the */** arms are unused). M0-T3: red-first cases for F-001, F-002 and F-003, confirmed failing at CP0 and committed together with their fixes.  
  *Rule:* testing-§12; testing-§13  
  *Planned in:* CM-02

**MultiMeters**

- **MultiMeters-R-13** `low` (review F-013; confirmed) — The test mock hard-codes Version='0.1.0', so perf records carry the wrong version  
  *Where:* tests/wow_mock.lua:1087; tests/perf.lua:753-754; docs/automated-tests/20260916-184449/perf.json  
  *Evidence:* The TOC says 1.0.0, but perf.json records "version":"0.1.0".  
  *Remediation:* C-10: derive __toc.Version in tests/wow_mock.lua from the MultiMeters.toc '## Version:' line through the mock's root. Update the comments in tests/test_envsetup.lua (:12, :27-30, :164) that describe the fixture as '0.1.0'. Do not edit the frozen docs/automated-tests bundle. The next run records the right version.  
  *Planned in:* MM-10

**PartyFrameEnhanced**

- **PartyFrameEnhanced-R-09** `medium` (review F-011; confirmed · upstream → LibKa0s) — The test kit's AceDB fake does not raise on CopyProfile/DeleteProfile the way AceDB-3.0 does, and does not strip defaults from the outgoing profile on SetProfile  
  *Where:* tests/_kit/mock_record.lua:241-268, :259 (upstream LibKa0s testkit/mock_record.lua); tests/_kit/mock_base.lua:26  
  *Evidence:* `if not src or name == current then return end` returns silently where AceDB raises. DeleteProfile is silent on the current profile. SetProfile never runs removeDefaults. This breaks kit fidelity rule 5 ('Model the awkward real behavior') and hides F-004 and stripped-default reads in every consumer.  
  *Remediation:* Upstream U-1: in LibKa0s testkit/mock_record.lua, CopyProfile raises the AceDB messages. DeleteProfile raises on the active profile, and on a missing one unless silent. SetProfile strips defaults from the outgoing profile. Bump the kit revision with a README entry. Then re-vendor the whole tests/_kit and libs/LibKa0s into this addon and every consumer, one commit each. Other consumers may go red, which is expected. Never edit it locally.  
  *Rule:* library-stack-§7, testing-§1, testing-§11, anti-patterns #45/#47  
  *Planned in:* LK-03
- **PartyFrameEnhanced-R-10** `low` (both F-012, PFE-12a; confirmed · upstream → LibKa0s) — The test kit has no EventRegistry fake or recorder, so test_disabled cannot see the EditMode.Exit survivor  
  *Where:* tests/_kit/mock_base.lua, tests/_kit/mock_record.lua (upstream testkit); tests/wow_mock.lua; modules/Providers.lua:342-345; tests/test_disabled.lua:95-97  
  *Evidence:* `grep EventRegistry tests/_kit/mock_base.lua tests/wow_mock.lua` returns nothing. The presence guard is false in the harness, so the callback never enters __registrations(), and step 3 of test_disabled cannot fail on PFE-12/F-005.  
  *Remediation:* Review (preferred): upstream U-2 adds an additive recording EventRegistry (RegisterCallback/UnregisterCallback/TriggerEvent, kind='callback' in __registrations()) to LibKa0s testkit/mock_base.lua and mock_record.lua, sharing the kit revision bump with U-1, then re-vendors tests/_kit whole. Audit (interim): add an EventRegistry recorder to the addon-owned tests/wow_mock.lua, and confirm step 3 goes red at 314c95e and green after the PFE-12 fix. The review says a test-local shim is acceptable until the kit ships one.  
  *Rule:* testing-§12, slash-commands-§7 (conformance step 3)  
  *Planned in:* LK-04, PF-05
- **PartyFrameEnhanced-A-02** `low` (audit PFE-13 (upstream half); confirmed · upstream → LibKa0s) — The test kit's mock CreateFrame starts frames hidden, whereas the client starts them shown, so consumers' F_on baselines never see container frames  
  *Where:* tests/_kit/mock_base.lua:121 (upstream LibKa0s testkit/mock_base.lua)  
  *Evidence:* `local f = { __shown = false, __scripts = {} }`, so a mock frame starts hidden while a client frame starts shown.  
  *Remediation:* Audit Sprint 5.1: in LibKa0s testkit/mock_base.lua, make CreateFrame start frames shown, as the client does. Bump the kit revision, then re-vendor tests/_kit whole into every consumer. Until then, keep the direct step-5 assertions in the addon.  
  *Rule:* testing-§11, slash-commands-§7 (conformance)  
  *Planned in:* LK-05


### C10 — Slash verbs that misreport their outcome (profile sub-verbs, lock, test)

In /at and /pfe, 'profile new <existing>' silently switches to that profile and wipes it, copy raises a raw AceDB error, delete of a missing name reports success, and a mistyped name on use creates a profile. LibKa0s Slash CliSet/CliReset ignore the write seam's refusal, AbsorbTracker's lock/unlock print a fixed success line, and /at test accepts negative durations. The shared root is that verbs do not validate input or echo the real resulting state. Affects AbsorbTracker, PartyFrameEnhanced and LibKa0s.

**LibKa0s**

- **LibKa0s-R-03** `medium` (review F-003; confirmed) — Slash CliSet/CliReset ignore the write seam's false,err refusal and echo the unchanged value  
  *Where:* LibKa0s/Slash.lua:688; LibKa0s/Slash.lua:703; LibKa0s/Schema.lua:451; AuraMaster/settings/Slash.lua:467-471; BankLedger/settings/Slash.lua:439  
  *Evidence:* Schema.Set returns false, invalid, why on validate rejection; CliSet discards it and prints path = <old value>. CliReset likewise ignores ApplyDefault false. BankLedger passes Schema.Set directly; MultiMeters has 14 validated rows; AuraMaster hand-prints the refusal in its own wrapper.  
  *Remediation:* C-03 (Slash minor 14->15): capture ok, err = d.set(row.path, v); if ok == false print INVALID(path) plus indented err and return, else echo. CliReset prints new NO_DEFAULT string when applyDefault returns exactly false. Document that set may answer false, reason (nil/true unchanged). Tests in tests/test_slash.lua or new tests/test_slash_refusal.lua if over 1500 lines. Consumer follow-up M6-T13: AuraMaster wrapper becomes return NS.SetByPath(path, v) and drops its own prints; re-check other hosts' wrappers. Smoke S-003.  
  *Rule:* library-stack-§7 (additive); architecture-§5 (single write seam)  
  *Planned in:* LK-17

**AbsorbTracker**

- **AbsorbTracker-R-01** `high` (review F-001; confirmed) — /at profile new <existing name> silently switches to and resets that profile, then prints 'Created ... new profile'  
  *Where:* settings/Slash.lua:431-435, settings/Slash.lua:427-430, settings/Slash.lua:383, docs/profiles.md:79, tests/test_slashcmds.lua:544  
  *Evidence:* new = needsName(... db:SetProfile(name); NS.ResetProfileCounted(db); print("Created and switched to new profile '"..name.."'")). When the name already exists, SetProfile switches to it and ResetProfile empties it, with no confirmation. The help text and docs promise 'Create new profile with defaults'. Tests cover only a fresh name.  
  *Remediation:* C-01: add a profileExists(db,name) helper that walks db:GetProfiles(). new refuses an existing name with one line pointing to /at profile use <name> and /at profile reset. Update the comment at :427-430, docs/profiles.md:79 and docs/smoke-tests.md. Red-first test: seed units.player.barWidth=333 on Keep, run 'new Keep', assert Keep still holds 333 and the current profile has not changed (-- red under: removing the profileExists guard).  
  *Rule:* slash-commands-§3, slash-commands-§4  
  *Planned in:* AT-03
- **AbsorbTracker-R-02** `medium` (review F-002; confirmed) — /at profile copy raises a real AceDB Lua error on a missing or current name; /at profile delete <missing> reports a deletion that did not happen  
  *Where:* settings/Slash.lua:437-448, libs/AceDB-3.0/AceDB-3.0.lua:535, libs/AceDB-3.0/AceDB-3.0.lua:581-587, tests/test_slashcmds.lua:560, tests/test_slashcmds.lua:589  
  *Evidence:* copy calls db:CopyProfile(name) bare, and AceDB errors on a missing source or on self-copy. delete calls db:DeleteProfile(name,true), which is a no-op for a missing name, and then prints 'Deleted profile'. A scratch probe printed '[AT] Copied settings from profile 'NoSuchProfile'' and '[AT] Deleted profile 'NoSuchProfile''. The suite passes only because the kit's AceDB fake never raises (F-006).  
  *Remediation:* C-02: before calling AceDB, check the name against GetCurrentProfile() and against profileExists(). Print 'Cannot copy a profile onto itself', 'Cannot delete the current profile', or 'Profile '<name>' not found — /at profile list shows them'. Do not use pcall. Add three red-first tests (copy missing, copy current, delete missing) with output assertions. They will also cover the raise once F-006 lands upstream.  
  *Rule:* slash-commands-§3  
  *Planned in:* AT-03
- **AbsorbTracker-R-03** `medium` (review F-003; confirmed) — /at lock and /at unlock print a fixed success line that can contradict the stored value, and they do not refresh an open panel  
  *Where:* settings/Slash.lua:89-98, settings/General.lua:180-188, settings/Slash.lua:310-317, core/AbsorbTracker.lua:260, tests/test_slashcmds.lua:98-106, tests/test_display.lua:609  
  *Evidence:* In combat the onChange refuses the unlock and writes true back, yet the verb still prints 'Bar unlocked'. Probe output: 'locked=true out=[AT] Cannot unlock the bars during combat \| [AT] Bar unlocked'. Neither verb calls NS.RefreshOptionsPanel(), although setEnabled, the descriptor set and the launcher click all do. The text says 'Bar' while the addon has three bars. The lines are not in the slash-commands-§5 set shape that §8 SHOULD use.  
  *Remediation:* C-03: extract an echoStored(path) local that refreshes the options panel, reads the stored value back, formats it through the row, and prints it via SlashLib.FormatKV. Use it for lock, unlock and setEnabled, and change the help text to 'bars'. Change tests/test_slashcmds.lua:98-106 to assert 'locked = false', and add an in-combat case asserting the output ends with 'locked = true' (-- red under: restoring the fixed 'Bar unlocked' line). Update README and docs/slash-dispatch.md if they quote the old lines.  
  *Rule:* slash-commands-§8, slash-commands-§5  
  *Planned in:* AT-04
- **AbsorbTracker-R-12** `low` (review F-011; confirmed) — /at test <value> [secs] does not validate the duration and announces negative or truncated values  
  *Where:* settings/Slash.lua:336, settings/Slash.lua:349  
  *Evidence:* local hold = tonumber(args[2]) or 5 is announced with '%d s'. A value of -3 is announced as 'for -3 s', and 2.5 is announced as '2 s' but held for 2.5 s.  
  *Remediation:* C-10: clamp hold to 0.5..60, or refuse values of 0 or less with the usage line. Announce with %.1f or %s. Add a test that '/at test 1000 -3' prints the usage line or the clamped value. If AT-76 moves the verb under /at debug hold, apply the fix there.  
  *Planned in:* AT-11

**PartyFrameEnhanced**

- **PartyFrameEnhanced-R-02** `high` (review F-002; confirmed) — `/pfe profile new <existing name>` silently wipes that profile and prints 'Created' (data loss)  
  *Where:* settings/Slash.lua:270-274  
  *Evidence:* `new` calls db:SetProfile(name) and then NS.ResetProfileCounted(db) without checking whether the name already exists. Reproduced: profile new Healer, set castbar.width 222, profile use Default, profile new Healer; castbar.width comes back as 140. The case meets the Critical floor; the review graded it High because it needs a name collision, and triage may raise it.  
  *Remediation:* C-002 / T-2: add an exists(db,name) helper based on db:GetProfiles(). `new` refuses an existing name with one tagged, localized line pointing at use/reset. Add a test in tests/test_slash.lua (`-- red under: drop the exists() guard in new`). Regenerate docs/test-cases.md and the README badge in the same commit.  
  *Rule:* slash-commands-§3, slash-commands-§4, localization-§1, localization-§5  
  *Planned in:* PF-01
- **PartyFrameEnhanced-R-05** `medium` (review F-004; confirmed) — Profile sub-verbs mishandle bad names: copy raises a raw AceDB error, delete of a missing profile prints a false 'Deleted', and use of a typo silently creates a profile  
  *Where:* settings/Slash.lua:265-285, :283; libs/AceDB-3.0/AceDB-3.0.lua:581-587  
  *Evidence:* db:CopyProfile raises 'Cannot copy profile %q as it does not exist.' and 'Cannot have the same source and destination profiles'. delete passes silent=true and prints 'Deleted profile X' for a profile that does not exist. SetProfile creates a profile on demand, so a mistyped `use` creates one. The kit's AceDB fake hides the copy error (F-011).  
  *Remediation:* C-002 / T-2: use, copy and delete refuse a missing name, and copy also refuses the current profile. Each refusal is one tagged, localized line through the existing printer; format strings go in locales/enUS.lua. Add tests for each verb to tests/test_slash.lua. The copy test goes red only after the F-011 kit re-vendor; until then, assert on the printed line. Note in the changelog that `use` no longer creates profiles. Rejected: pcall-and-print of the AceDB error.  
  *Rule:* slash-commands-§3, slash-commands-§4, localization-§1  
  *Planned in:* PF-01
- **PartyFrameEnhanced-R-08** `low` (review F-008; corrected) — No test covers a real profile switch or the profile sub-verbs, so the suite stays green over two High bugs  
  *Where:* tests/test_database.lua:38-40; tests/test_slash.lua:98-99  
  *Evidence:* test_database calls NS.OnProfileChanged() directly and never checks placement. test_slash covers only `profile` with no argument. F-001, F-002, F-003 (the profile route) and F-004 go undetected.  
  *Remediation:* Track no separate work. Close this finding when the red-first tests from R-01 (a real SetProfile, CopyProfile and reset placement), R-02 and R-05 (every profile sub-verb) and R-04 (the in-combat A-to-B-to-A toggle, not a profile route) land. Regenerate docs/test-cases.md and the README badge in the same commits.  
  *Rule:* testing-§5  
  *Planned in:* PF-02


### C11 — Profile switch and SavedVariables migration correctness

Migration runners migrate only the active profile yet stamp the account-wide schemaVersion, stamp past a step that raised, or let AceDB strip a schemaVersion that equals its default. Profile switches leave stale cached cfg behind. The standard has no ruling on who owns the migration stamp (upstream). Affects KickCD, LootHistory, PanelMaster, PartyFrameEnhanced, PrettyChat and WhatGroup.

**KickCD**

- **KICKCD-R-01** `high` (review F-001; confirmed) — Color-shape and font-flag migrations run once per account, so any profile not active at the 1.3.0 upgrade keeps its old shape  
  *Where:* core/Database.lua:719-720, core/Database.lua:752, core/Database.lua:821-826, core/Database.lua:666  
  *Evidence:* migrations[3]/[4] (MigrateColorShape, MigrateFontFlags) are gated by the account-level db.global.schemaVersion but walk only db.profile. OnProfileChanged re-runs only FoldLegacyUnits, BackfillLabelStyle, MigrateSpecKeys and BuildSpells. A scratch repro under the kit mock, after a swap to a profile at v5, gave '[1]=0.1 r=1' and fontFlags=NONE: nothing was converted. Result: customised colors read back as defaults, and the outline dropdown opens blank. The mock AceDB has no SetProfile, so no test covers this path.  
  *Remediation:* C-01: call MigrateColorShape and MigrateFontFlags from Database:Init and every OnProfileChanged, after MigrateSpecKeys. Both are idempotent. Keep the version steps so schemaVersion still advances. Add an `if not (db and db.profile) then return end` guard in MigrateColorShape. Mitigation: convert only when the keyed part equals the declared default, otherwise drop the array part; state this in docs/schema.md. Add a real SetProfile to tests/wow_mock.lua and a two-profile test with a 'red under' line (test_color_shape or test_database). Update the savedvariables-§1 register row in docs/ARCHITECTURE.md to name all five shape-driven steps (see KICKCD-A-08 / B-03). No schemaVersion bump.  
  *Rule:* savedvariables-§1  
  *Planned in:* KC-03
- **KICKCD-A-08** `low` (audit KICKCD-B-03; corrected) — The first savedvariables-§1 register row says 'Two profile migrators' (the tree runs three, soon five), and both rows' schema.md line anchors have rotted  
  *Where:* docs/ARCHITECTURE.md:390, docs/ARCHITECTURE.md:468, core/Database.lua:821-824, docs/schema.md:256, docs/schema.md:266, docs/schema.md:269  
  *Evidence:* The row names two migrators, but FoldLegacyUnits, BackfillLabelStyle and MigrateSpecKeys run ungated. Anchors #L256 and #L266 now point at a code-block comment; the reasoning is at :269 under '### units.<unit>.label.style shape'. Carried over from the prior audit. R-01 adds two more shape-driven steps.  
  *Remediation:* D6/Sprint 4.5, after R-01 lands: the owner decides whether BackfillLabelStyle or MigrateSpecKeys counts as the trigger's 'third shape addition'. Either retire row 1 with a retirement note, or rewrite What differs to name every shape-driven migrator actually run at Database:Init/OnProfileChanged and restate the trigger. Replace row 1's schema.md#L256 with the heading anchor for '### units.<unit>.label.style shape' (the reasoning is the paragraph at :271). Replace row 2's schema.md#L266 with the anchor for '## Migration: folding legacy icons/castbar/anchors into units.target' (the reasoning is at :281).  
  *Rule:* documentation-§3; audit-review-history; savedvariables-§1  
  *Planned in:* KC-03

**LootHistory**

- **LootHistory-A-18** `low` (audit LH-75; confirmed · upstream → WowAddonStandards) — schemaVersion held at 1 in defaults while migrations stamp to 8, reasoned only in a comment  
  *Where:* defaults/Global.lua:8-13, core/Database.lua:103, core/Database.lua:133  
  *Evidence:* versioning-git: MUST increment schemaVersion in defaults whenever an SV migration is required. The defaults hold 1, and the runner walks to 8. The comment gives a real reason (a seeded stamp would claim migrations that never ran under the AceDB backfill), and open-evolutions records this as the unruled 'Migration-stamp ownership' case. The rule conflicts with the runner shape savedvariables-§1 prints.  
  *Remediation:* Local: add a versioning-git register row citing the comment and open-evolutions 'Migration-stamp ownership', with trigger 'the standard rules on migration-stamp ownership'. Upstream (WowAddonStandards, not blocking): propose that versioning-git defer to the migration-stamp ruling, or state that the runner's highest 'to' is the version and the defaults value is the pre-migration floor. This resolves the conflict with savedvariables-§1.  
  *Rule:* versioning-git (MUST); savedvariables-§1; open-evolutions  
  *Planned in:* WS-03, LH-12

**PanelMaster**

- **PanelMaster-A-05** `low` (audit PM-038; confirmed) — The deliberate omission of schemaVersion from defaults has no Documented-deviations register row  
  *Where:* defaults/Global.lua:8-20, core/Database.lua:132, core/Database.lua:158, docs/ARCHITECTURE.md (## Documented deviations)  
  *Evidence:* toc-file-§2 and savedvariables-§1 say you MUST declare schemaVersion in defaults. The addon omits it on purpose, because AceDB would serve the default for legacy accounts and mask the v1->v2 migration (M4-22, febf108). The reasoning lives only in a code comment. open-evolutions 'Migration-stamp ownership' is unruled.  
  *Remediation:* Add a register row: toc-file-§2 / savedvariables-§1 \| schemaVersion is written by the migration runner (core/Database.lua:132, :158), not declared in NS.defaults.global \| AceDB backfills a declared default as current, which masks legacy accounts; open-evolutions 'Migration-stamp ownership' (M4-22, febf108) \| 2026-08-05 \| the standard rules on migration-stamp ownership, or a schema bump that no longer needs a shape-driven legacy check. Upstream half: propose a ruling in WowAddonStandards open-evolutions sanctioning 'stamped by the runner, never declared' for AceDB hosts (see A-13). The row is not blocked on it.  
  *Rule:* toc-file-§2; savedvariables-§1; audit-review-history; documentation-§3  
  *Planned in:* PM-10
- **PanelMaster-A-06** `low` (audit PM-038a; corrected) — ARCHITECTURE.md and common-tasks.md say defaults/Global.lua carries schemaVersion, which it does not  
  *Where:* docs/ARCHITECTURE.md:34, docs/common-tasks.md:12-13, defaults/Global.lua:73-76  
  *Evidence:* Both docs say Global.lua holds the schemaVersion stamp ('today only schemaVersion qualifies'). Global.lua declares only minimap. Derived from PM-038.  
  *Remediation:* Reword docs/ARCHITECTURE.md:34, docs/common-tasks.md:12-13, docs/module-map.md:24 and docs/profiles.md:11 in one change, together with the A-05 register row. Each should say that defaults/Global.lua declares only LibDBIcon's minimap table, and that schemaVersion is written into the SavedVariables by the migration runner (core/Database.lua RunMigrations) and deliberately not declared (see the register row). Coordinate with R-09 on defaults/Profile.lua:4-5 and core/Database.lua:16. Leave docs/schema.md:21 as it is.  
  *Rule:* documentation-§5  
  *Planned in:* PM-10
- **PanelMaster-A-17** `info` (audit PM-038 (upstream half); confirmed · upstream → WowAddonStandards) — The standard has no ruling on migration-stamp ownership ('runner-stamped, never declared' for AceDB hosts)  
  *Where:* WowAddonStandards open-evolutions 'Migration-stamp ownership'; toc-file-§2; savedvariables-§1  
  *Evidence:* PanelMaster is a worked instance: a declared AceDB default masks legacy accounts (defaults/Global.lua:8-20, febf108). The MUST to declare schemaVersion in defaults conflicts with a correct migration for AceDB hosts.  
  *Remediation:* Propose a ruling in open-evolutions sanctioning 'stamped by the runner, never declared in defaults' for AceDB hosts, with PanelMaster as the worked case. If accepted, the A-05 register row becomes compliance and can retire.  
  *Rule:* toc-file-§2; savedvariables-§1; open-evolutions  
  *Planned in:* WS-03, PM-10

**PartyFrameEnhanced**

- **PartyFrameEnhanced-R-01** `high` (review F-001; confirmed) — A profile switch, copy or reset leaves elements placed by the OLD profile, because Anchor reads the features' cached cfg upvalues in an undefined bus dispatch order  
  *Where:* modules/Anchor.lua:359; modules/Anchor.lua:123-124 (wrong comment); modules/CastBars.lua:372,408; modules/TargetFrames.lua:258,297; modules/PetFrames.lua:139,178; tests/test_anchor.lua:181-182 (wrong comment); libs/CallbackHandler-1.0/CallbackHandler-1.0.lua:16  
  *Evidence:* CallbackHandler dispatches with next(), so the order of PROFILE handlers is hash order, not TOC order. spec.config returns a captured cfg upvalue that each feature rebinds only in its own PROFILE handler. Nothing re-anchors afterwards. Reproduced in a scratch script: 'back to Default pet anchoredToHolder=true cfgMode=attached' and 'after Reset all settings target anchoredToHolder=true cfgMode=attached'. The comments at Anchor.lua:123-124 and test_anchor.lua:181-182 wrongly assume registration order equals dispatch order.  
  *Remediation:* C-001 / T-1: change spec.config to read live data (`function() return NS.db.profile.castbar\|target\|pet end`) in all three features, and switch the slotSize closures to the same live read. Rewrite the Anchor comment to say CallbackHandler order is undefined. Add real-switch tests to tests/test_anchor.lua (or a new tests/test_profile_switch.lua): SetProfile between profiles that differ in anchorMode, assert __aTarget, repeat after RestoreAllDefaults. Mark the case with `-- red under: revert config() to the captured upvalue`. Rejected: deferring to the next frame, or a second ordered PROFILE message.  
  *Rule:* architecture-§4, architecture-§5  
  *Planned in:* PF-02
- **PartyFrameEnhanced-R-15** `low` (both F-015, PFE-22; confirmed) — The migration runner migrates only the active profile but stamps the account-wide schemaVersion  
  *Where:* core/Database.lua:34, :37-48, :40-45  
  *Evidence:* `step.apply(NS.db.profile)` followed by `g.schemaVersion = step.to`. The first real ladder step would leave every non-active profile unmigrated forever. SCHEMA_STEPS is empty today, so nothing can reach it. Review graded Low; audit filed Info (an observation).  
  *Remediation:* Review C-008 / T-10 (fix now): apply each step to every stored profile (`for name,p in pairs(NS.db.profiles or {[cur]=NS.db.profile})`), with defaults-merge caveats commented, and stamp the global version only after all profiles. Add a unit case with a test-local injected fake step using two profiles. The audit's alternative is to defer until the first step is written, or to migrate lazily on OnProfileChanged with a per-profile stamp.  
  *Rule:* savedvariables-§1  
  *Planned in:* PF-08

**PrettyChat**

- **PRETTYCHAT-R-03** `low` (review F-003 (change C-02); corrected) — Migration runner migrates only the active profile (global stamp) and stamps past a step that raised  
  *Where:* core/Database.lua:100, core/Database.lua:102, core/Database.lua:85-90, core/Database.lua:42, core/PrettyChat.lua:54-56  
  *Evidence:* `local from = db.global.schemaVersion or 0`, and schemaVersion is stamped unconditionally after runSteps. A failed step is printed and counted as ran. Later OnProfileChanged/Copied/Reset see from == SCHEMA_VERSION and run nothing, so inactive profiles keep the old shape. The PrettyChat.lua:54-56 comment claims the opposite. There is no impact today because the migrations table is empty, but F-002's fix writes the first migration.  
  *Remediation:* Keep schemaVersion in global. Split the steps into profileSteps (idempotent, shape-detecting, run on every load-pass entry regardless of the stamp) and globalSteps (gated by the stamp). runSteps returns false if any step raised, and the stamp moves only when all steps succeed. Rewrite the core/PrettyChat.lua:54-56 comment. Add tests in tests/test_database.lua: a profile step runs on OnProfileChanged into a second profile after the stamp moved, and a raising global step leaves the stamp unmoved (with -- red under: notes). Watch that RunMigrations (CCN 12) stays under 15, or split it into helpers.  
  *Rule:* savedvariables  
  *Planned in:* PC-03

**WhatGroup**

- **WHATGROUP-R-03** `medium` (review F-003; confirmed · upstream → WowAddonStandards) — global.schemaVersion default equals current version, so AceDB strips it at logout and the first real migration is skipped for every existing user  
  *Where:* settings/Schema.lua:609, core/Database.lua:27, core/Database.lua:31-36, tests/test_database.lua:27-30  
  *Evidence:* global = { schemaVersion = NS.SCHEMA_VERSION or 1 }; AceDB removeDefaults (AceDB-3.0.lua:134, :425) strips values equal to default, so no SV file carries a stamp; when SCHEMA_VERSION becomes 2 the default reads 2 and 1->2 never runs. `or NS.SCHEMA_VERSION` at Database.lua:27 is dead. Existing test sets schemaVersion=0 explicitly and cannot see this (testing-§12 near-miss). The savedvariables-§1 template prescribes the same shape (collection-wide).  
  *Remediation:* Local C-003: declare global.schemaVersion = 0 (pre-versioning) default, keep NS.SCHEMA_VERSION = 1; RunMigrations steps 0->1 (no-op) and stores 1 which persists; delete dead `or`; document steps must be idempotent against a fresh default profile. Rewrite 'BuildDefaults seeds global.schemaVersion' test to pin 0; add red-under case: boot, run removeDefaults strip, re-boot with SCHEMA_VERSION=2 and a 1->2 step, assert step ran. Upstream U-1: amend WowAddonStandards savedvariables-§1 template to declare 0 and explain the AceDB strip; standard minor bump. Local fix does not wait for U-1. Smoke S-003.  
  *Rule:* savedvariables-§1  
  *Planned in:* WS-03, WG-08


### C12 — British spellings and the kit prose gate

localization-§5 requires US spelling, but the kit's test_prose gate skips docs/automated-tests/ and docs/perf-analysis/ entirely while it scans frozen stores, and its BRITISH list lacks 'synchronis'. The gate is fixed upstream in the LibKa0s testkit, followed by local respellings in ConsumableMaster, KickCD, LibKa0s, MultiMeters and PanelMaster. MultiMeters' 'minimise' reaches stored paths, so it needs a SavedVariables migration.

**LibKa0s**

- **LibKa0s-A-07** `low` (audit LK-28; corrected) — 210 British spellings in 33 live authored files  
  *Where:* tests/ (151 lines, 23 files); live docs/api/ highest-version docs (25 in 5); docs/releasing.md (10); README.md (4); DEPENDENCIES.md (1); tools/artwork/*.py (19 in 2); CLAUDE.md:75 (register row 3)  
  *Evidence:* Published BRITISH (91) / ALLOWED (30) lists with testkit/test_prose.lua's matcher; excludes ratified payload hits (rows 1, 2) and 560 lines in superseded docs/api records. Register row 3 ratifies gate scope, not the spellings; its trigger names the tests/ sweep as owed. Recurs (216 in 33 on 2026-09-08).  
  *Remediation:* As proposed (re-run the counter at HEAD, sweep with the published lists, never touch superseded docs/api versions, leave the quoted 'was -> is' lines), with two explicit exclusions. First, leave `.cancelled` / `IsCancelled` member accesses that model AceTimer/C_Timer handles (e.g. tests/test_mock_ace.lua:237,415,443-444,465); either extend register row 1 and tests/test_prose.lua's RATIFIED to cover that path, or keep them as identifiers and fix only the surrounding prose (e.g. test names such as tests/test_perf_core.lua:383 'a cancelled run'). Second, leave tests/test_prose.lua's own quoted forbidden-word fixtures. Target 0 prose hits and update register row 3's figures.  
  *Rule:* localization-§5  
  *Planned in:* LK-29

**ConsumableMaster**

- **ConsumableMaster-A-05** `low` (audit CM-79; confirmed · upstream → LibKa0s) — The kit's prose gate skips docs/automated-tests/ and docs/perf-analysis/ whole, hiding authored store-root files (README.md, RESULTS.md)  
  *Where:* tests/_kit/test_prose.lua:209-213 (LibKa0s testkit/test_prose.lua); tests/run.lua:507  
  *Evidence:* localization-§5 lets a gate skip frozen dated bundles only. docs/automated-tests/README.md, RESULTS.md and docs/perf-analysis/README.md are authored or regenerated in place. The gate passes over two real British spellings (CM-80). This is vendored code the repo must not patch (library-stack-§5).  
  *Remediation:* A1 / S0-2 upstream in the LibKa0s testkit: replace the whole-directory skips with dated-bundle skips (every subdirectory of the two stores counts as a frozen bundle, and the store-root files are scanned). Add a self-test that plants a British spelling in a store-root README and expects red. Tag, then re-vendor whole (S1-1).  
  *Rule:* localization-§5; library-stack-§5  
  *Planned in:* LK-07
- **ConsumableMaster-A-06** `low` (audit CM-81; confirmed · upstream → WowAddonStandards) — 'synchronisation' in authored prose; 'synchronis' is missing from the published BRITISH list  
  *Where:* docs/settings-panel.md:80; tests/_kit/test_prose.lua:198 (PUBLISHED_BRITISH = 91)  
  *Evidence:* '... is a synchronisation problem the design would have invented'. No gate can catch it, and localization-§5 forbids a private addition to the list. Open since 2026-09-08.  
  *Remediation:* A2 / S0-1 upstream: add 'synchronis' to localization-§5's BRITISH list in WowAddonStandards (91 -> 92, with a changelog entry; admissible because no US word contains it). Then sync the kit's BRITISH list and PUBLISHED_BRITISH = 92 in LibKa0s (S0-2), and re-vendor. S1-2: change the text to 'synchronization' in the same commit the gate turns red.  
  *Rule:* localization-§5  
  *Planned in:* WS-07, CM-01
- **ConsumableMaster-A-07** `low` (audit CM-80 (derived from CM-79); confirmed) — Two British spellings in docs/perf-analysis/README.md: 'analysed' and 'neighbours'  
  *Where:* docs/perf-analysis/README.md:25; docs/perf-analysis/README.md:26  
  *Evidence:* Both 'analys' and 'neighbour' are on the published list. The gate passes only because of CM-79's exclusion. Open since 2026-09-08.  
  *Remediation:* S1-2 / B11: after the re-vendor that carries A1, change to 'analyzed' and 'neighbors' in the same commit the gate turns red.  
  *Rule:* localization-§5; anti-pattern #46  
  *Planned in:* CM-01

**KickCD**

- **KICKCD-A-06** `low` (audit KICKCD-B-02 (upstream cause); corrected · upstream → LibKa0s) — Kit test_prose skips the whole docs/perf-analysis/ and docs/automated-tests/ directories, hiding live rewritten READMEs and RESULTS.md  
  *Where:* tests/_kit/test_prose.lua:211 (LibKa0s testkit/test_prose.lua SKIPPED_DIRS)  
  *Evidence:* SKIPPED_DIRS includes 'docs/automated-tests/' and 'docs/perf-analysis/' whole. localization-§5 excludes only frozen dated bundles, and documentation-§3 says the perf-analysis README is rewritten.  
  *Remediation:* D9 U1/Sprint 0.1: in LibKa0s testkit/test_prose.lua, keep the dated bundles excluded but stop hiding the rewritten store files, without using a pattern (localization-§5 requires each exclusion to be named file by file or directory by directory). Recommended: add an explicitly named scan-back list for docs/perf-analysis/README.md, docs/automated-tests/README.md and docs/automated-tests/RESULTS.md, which the walker scans even though they sit under a skipped directory. Another option is for the gate to enumerate the store's dated bundle directories by name at scan time, but it must not grow a regex. Add a kit test proving the README gets scanned and a bundle file does not. Bump the kit revision, run LibKa0s's suite, and tag. Then re-vendor the whole LibKa0s/ and testkit/ into KickCD (Sprint 1.1, /wow-addon:revendor-libka0s, CLAUDE.md provenance line, docs/revendor bundle) and confirm test_prose goes red on 'analysed' and 'neighbours'.  
  *Rule:* localization-§5; AP #46; library-stack-§5; AP #47  
  *Planned in:* LK-07
- **KICKCD-A-07** `low` (audit KICKCD-B-02 (local words); confirmed) — Two British spellings in the live docs/perf-analysis/README.md  
  *Where:* docs/perf-analysis/README.md:35, docs/perf-analysis/README.md:36  
  *Evidence:* 'analysed' at :35 and 'neighbours' at :36. Also raised by the review summary as upstream item B-02.  
  *Remediation:* Sprint 1.2: after the A-06 re-vendor shows test_prose red, change them to 'analyzed' and 'neighbors'.  
  *Rule:* localization-§5; AP #46  
  *Planned in:* KC-01

**MultiMeters**

- **MultiMeters-A-18** `low` (audit MM-A-18; confirmed) — British 'minimise'/'minimised' survives in player-visible strings, README, identifiers and comments, held by an unsanctioned waiver  
  *Where:* locales/enUS.lua:214; locales/enUS.lua:231; README.md:50; modules/HeaderControls.lua:127; tests/prose_waivers.lua:24; tests/prose_waivers.lua:30-57  
  *Evidence:* 154 lines across 22 authored files. The waiver covers 25 files and calls itself 'a DEBT, not a decision'. None of the three sanctioned waiver shapes applies, and there is no register row.  
  *Remediation:* Correct prose, comments, README (with the de-AI pass) and locale values. Rename the keys (L['Show minimize'], L['Minimized']) and the header control key and art together with all call sites. Remove each minimis waiver entry in the same change, and delete the file if it ends up empty. Stored paths go through MM-A-18a. Afterwards grep minimis returns 0 in authored scope.  
  *Rule:* localization-§5  
  *Planned in:* MM-13
- **MultiMeters-A-18a** `low` (audit MM-A-18a; confirmed) — The minimise spelling reaches two stored SavedVariables paths, so it needs a v15->v16 migration (derived from MM-A-18)  
  *Where:* defaults/Profile.lua:130; defaults/Profile.lua:148; core/Database.lua; settings/Schema.lua; settings/Schema_Paths.lua  
  *Evidence:* showMinimise=true and window.frame.minimised=false are stored keys. A find-and-replace would orphan every player's stored values.  
  *Remediation:* Add a v15->v16 step in the Database runner that walks every profile and window, copies minimised->minimized and showMinimise->showMinimize, then nils the old keys. Rename defaults and schema rows, keep ValidateSchema passing, and add a migration case. Alternatively, ratify the decline as a localization-§5 register row.  
  *Rule:* localization-§5; versioning-git; savedvariables  
  *Planned in:* MM-13

**PanelMaster**

- **PanelMaster-A-09** `low` (audit PM-041; confirmed · upstream → LibKa0s) — The kit prose gate scans frozen docs/superpowers/ and docs/investigations/; two frozen specs were respelled to the non-word 'catalogd'  
  *Where:* tests/_kit/test_prose.lua:209-213, docs/superpowers/specs/2026-07-31-panel-artwork-design.md:5, docs/superpowers/specs/2026-08-02-wiki-artwork-import-design.md:5, tests/prose_waivers.lua  
  *Evidence:* The kit's SKIPPED_DIRS (kit revision 25) omits docs/superpowers/ and docs/investigations/, which documentation-§3 lists as frozen. Commit e30e329 'fixed' line 5 of two frozen specs from 'catalogued' to 'catalogd'. The prior audit (PM-032a) had declined to touch these lines for this reason.  
  *Remediation:* Upstream first, in LibKa0s testkit/test_prose.lua: add 'docs/superpowers/' and 'docs/investigations/' to SKIPPED_DIRS, with a kit self-test pinning both the exclusion and its narrowness. Bump to kit revision 26, add a changelog entry, get the kit-sync gate green, and tag a patch. Then re-vendor the whole of LibKa0s and testkit. Then restore line 5 of both specs from 'git show e30e329^:<path>' and confirm test_prose stays green. Interim, if the re-vendor is delayed: skipDirs = { 'docs/superpowers/' } in tests/prose_waivers.lua, removed after the re-vendor.  
  *Rule:* localization-§5; documentation-§3 (frozen-store list)  
  *Planned in:* LK-07, PM-17


### C13 — Automated-test runner cannot record the performance-§12 exemption

The vendored runner records the perf skip as 'no tests/perf.lua' and never as the ratified performance-§12 exemption. RESULTS.md therefore denies an exemption the addon holds, and the release notes and docs drift with it. The fix is upstream in the LibKa0s kit runner; the BankLedger, LootHistory, PrettyChat and LibKa0s docs follow.

**LibKa0s**

- **LibKa0s-A-06** `low` (audit LK-36; confirmed) — Release notes stopped stating the perf skip  
  *Where:* CHANGELOG.md:13-507 (v1.55.0); CHANGELOG.md:583-605 (v1.53.0); CHANGELOG.md:579-581 (v1.54.0 model); docs/releasing.md step 7  
  *Evidence:* automated-tests-§3 requires the perf SKIP for a repo with no tests/perf.lua to be stated in release notes; present for v1.50.0-v1.52.0 and v1.54.0, absent from v1.55.0, v1.53.0, v1.49.1, v1.49.0, v1.48.1, v1.48.0, v1.47.0.  
  *Remediation:* Add a template line to releasing.md step 7 filled from the manifest: 'Release gate (docs/automated-tests/<stamp>/): lint ... tests ... complexity ... Perf SKIPPED, not measured — no tests/perf.lua — so the gate covered three suites, not four.' Next entry states it; released entries not rewritten.  
  *Rule:* automated-tests-§3  
  *Planned in:* LK-31

**BankLedger**

- **BankLedger-A-04** `low` (audit BL-48; confirmed · upstream → LibKa0s) — Vendored automated-test runner records the perf skip as 'nothing to run' and denies the addon's ratified performance-§12 exemption  
  *Where:* tests/_kit/run-automated-tests.sh:343-344,833-848 (upstream LibKa0s/testkit/run-automated-tests.sh); docs/automated-tests/RESULTS.md:59-63; newest manifest skipReason  
  *Evidence:* The manifest says skipReason 'no tests/perf.lua — this addon ships no offline scenarios'. RESULTS.md says the skip is 'rather than a ratified performance-§12 no-combat-path exemption', which is false because docs/ARCHITECTURE.md:501 holds that exemption. The runner knows only sanctioned reason (1). The addon may not edit the kit.  
  *Remediation:* Upstream first, in LibKa0s: teach testkit/run-automated-tests.sh sanctioned skip reason (2). Detect a `performance-§12` row under ## Documented deviations in docs/ARCHITECTURE.md; an explicit flag or env var like KA0S_PERF_EXEMPT is a fallback only. Emit a skipReason naming performance-§12 and an md_perf_section sentence pointing at docs/performance.md. Add kit self-tests for both branches, a kit revision bump and a changelog entry, then tag a release. Consumer side: whole-folder re-vendor of LibKa0s/ and testkit/ with the CLAUDE.md provenance line in the same commit, its own docs/revendor bundle and the chmod +x on the runner. Run the four suites once so RESULTS.md regenerates. No hand edits.  
  *Rule:* automated-tests-§3 (two sanctioned perf skipReasons; the second MUST be recorded when it applies)  
  *Planned in:* LK-09, BL-DOCS

**LootHistory**

- **LootHistory-A-12** `low` (audit LH-69; confirmed · upstream → LibKa0s) — Vendored runner always records the perf skip as 'no tests/perf.lua', never the ratified performance-§12 exemption  
  *Where:* tests/_kit/run-automated-tests.sh:343-344, tests/_kit/run-automated-tests.sh:838-841, docs/automated-tests/*/manifest.json, docs/automated-tests/RESULTS.md  
  *Evidence:* Every manifest has skipReason 'no tests/perf.lua — this addon ships no offline scenarios', and the RESULTS Perf prose says the skip is not the exemption. But the addon holds the ratified performance-§12 row (issue #22), and automated-tests-§3 says reason (2) MUST be recorded, naming performance-§12. The runner (kit revision 25) has no input that would let it know. testing-§1 forbids a local kit edit.  
  *Remediation:* Upstream first, in LibKa0s/testkit/run-automated-tests.sh. Before falling back to reason (1), detect a performance-§12 row in docs/ARCHITECTURE.md ## Documented deviations, or accept an explicit env/flag override. Emit skipReason 'performance-§12 no-combat-path exemption (ratified; docs/ARCHITECTURE.md -> Documented deviations)' and branch the RESULTS Perf section on it. Add kit cases for with-row, without-row, and unparseable register (fails loudly). Release a tag, re-vendor the whole of LibKa0s (libs/LibKa0s + tests/_kit, provenance line and +x bit in the same commit) with its own docs/revendor bundle, then run the four suites so the new bundle records reason (2). Never hand-edit RESULTS.md or frozen bundles.  
  *Rule:* automated-tests-§3 (MUST); testing-§1  
  *Planned in:* LK-09, LH-DOCS

**PrettyChat**

- **PRETTYCHAT-A-15** `low` (audit PC-90 (PRETTYCHAT-C-12); confirmed · upstream → LibKa0s) — The vendored automated-test runner cannot record the performance-§12 exemption; RESULTS.md denies an exemption the addon holds  
  *Where:* tests/_kit/run-automated-tests.sh:343-344, tests/_kit/run-automated-tests.sh:838-841, docs/automated-tests/RESULTS.md:58-62  
  *Evidence:* The runner (kit rev 25) hard-codes a single skip reason ('ships no tests/perf.lua ... rather than a ratified performance-§12 exemption'). automated-tests-§3 requires reason (2), naming performance-§12, when it applies. testing-§1 forbids editing the kit in place.  
  *Remediation:* Upstream LibKa0s first (Sprint 1.1). testkit/run-automated-tests.sh detects a performance-§12 row under ## Documented deviations in docs/ARCHITECTURE.md (or root CLAUDE.md for a library), or accepts an explicit consumer fact (KA0S_PERF_EXEMPT or an opts file). It emits reason (2) in manifest skipReason and in the standing paragraph. Add a kit self-test with two fixtures and a changelog entry. Tag, re-vendor whole, and re-run at the next release. No hand-edits here.  
  *Rule:* automated-tests-§3  
  *Planned in:* LK-09, PC-DOCS
- **PRETTYCHAT-A-16** `low` (audit PC-91 (derived from PC-90); confirmed) — docs/testing.md tells release notes to cite the bare absence of perf.lua instead of the exemption  
  *Where:* docs/testing.md:238-239  
  *Evidence:* It says 'perf skipped because this addon ships no tests/perf.lua'. §3 says an exempt addon's release notes name the exemption.  
  *Remediation:* Reword to: 'perf is skipped under the ratified performance-§12 no-combat-path exemption (register row in docs/ARCHITECTURE.md), which the release notes name.'  
  *Rule:* automated-tests-§3  
  *Planned in:* PC-23


### C14 — Stale automated-test records, watch lists and release bundles

docs/automated-tests/RESULTS.md trails HEAD by about 30 commits in nearly every repo. Watch-list dispositions have expired or cite retired trackers, and some tags shipped without a release bundle or ANALYSIS.md. The fix is one fresh run per repo after remediation, plus the LibKa0s kit runner and release-doc fixes. Affects AbsorbTracker, BankLedger, ConsumableMaster, KickCD, LibKa0s, LootHistory, MultiMeters, PanelMaster, PartyFrameEnhanced, PrettyChat and WhatGroup.

**LibKa0s**

- **LibKa0s-A-01** `low` (audit LK-35; corrected) — Six tags cut with no release bundle naming them (release gate never evaluated)  
  *Where:* docs/releasing.md:157; docs/automated-tests/*/manifest.json; tags v1.28.0, v1.29.0, v1.36.0, v1.36.1, v1.54.1, v1.54.2  
  *Evidence:* releasing.md:157 says no tag is cut without a bundle whose release field names it; set difference of tags minus manifest release values leaves six tags since 2026-09-08 (v1.54.1/v1.54.2 five minutes apart). Four-suite gate not evaluated for versions vendored into eleven consumers.  
  *Remediation:* Add a mechanical precondition to docs/releasing.md step 7: `grep -l '"release": "<X.Y.Z>"' docs/automated-tests/*/manifest.json` must print at least one path, and the stamp being tagged from must be one of them (the newest, clean, all-pass bundle). Do not require exactly one: re-runs for the same release are normal (1.35.0 has five). Do not fabricate bundles. Name the six tags once in the next release ANALYSIS.md. At close-out, verify that the new tag appears in at least one manifest.  
  *Rule:* automated-tests-§6; automated-tests-§3  
  *Planned in:* LK-31
- **LibKa0s-A-02** `low` (audit LK-33; confirmed) — Watch-list over-cap dispositions contradict the census (closed issues, deleted gate file, blank cell)  
  *Where:* docs/automated-tests/RESULTS.md:167; docs/automated-tests/RESULTS.md:168; docs/automated-tests/RESULTS.md:169; CLAUDE.md:129-131  
  *Evidence:* RESULTS.md:167 points OptionsWidgets.lua at closed #16 and names deleted tests/test_layout_cap.lua as gate (census says #32); :169 points test_options_widgets.lua at closed #8 (census #33); :168 testkit/framework.lua blank. layout-§1/automated-tests-§4 require the two records to agree and over-cap cells to point at the census row.  
  *Remediation:* Replace the three Disposition cells with 'See the census row, CLAUDE.md § Files over the 1500-line cap' (optionally naming #32/#33/register row). One-time edit; runner carries authored cells forward. Confirm with a --no-bundle complexity run or next full run.  
  *Rule:* layout-§1; automated-tests-§4  
  *Planned in:* LK-33
- **LibKa0s-A-03** `low` (audit LK-17d; confirmed) — Five of ten on-notice watch-list dispositions expired or blank  
  *Where:* docs/automated-tests/RESULTS.md:157 (LibKa0s/Options.lua); :158 (LibKa0s/OptionsTabs.lua); :160 (LibKa0s/Widgets.lua); :162 (testkit/test_prose.lua); :163 (tests/test_options.lua); :164 (tests/test_schema.lua); :166 (tests/test_widgets.lua)  
  *Evidence:* test_options.lua 'owed a tracked ID' across 54 releases with no issue; Widgets.lua and test_widgets.lua crossed own shelf life 20 releases ago, promised issue never opened; Options.lua passed 'Re-check at 1350' (now 1476) without re-rule; OptionsTabs.lua blank v1.50.0-v1.55.0. New blank cells test_prose.lua (1499, one line from cap, kit code) and test_schema.lua. Recurs from 2026-09-08, wider.  
  *Remediation:* File issues (state:triaged, severity:low, throttled gh calls) for tests/test_options.lua (render/refresh block -> test_options_render.lua), LibKa0s/Widgets.lua (per-widget files), tests/test_widgets.lua (split by widget family), testkit/test_prose.lua; replace cells with 'already tracked as #NN'. Re-rule Options.lua (issue naming the font-preload peel, or written acceptance with a new trigger <1500). Write dispositions for OptionsTabs.lua and test_schema.lua. No peels in this track.  
  *Rule:* automated-tests-§4; anti-pattern #53  
  *Planned in:* LK-32
- **LibKa0s-A-04** `low` (audit LK-34; confirmed) — Census row claims a 'Ratified deviation row' for testkit/framework.lua that the register does not hold  
  *Where:* CLAUDE.md:131; CLAUDE.md:163-165; CLAUDE.md:71-78; CLAUDE.md:51-53  
  *Evidence:* Census dispositions framework.lua (1583) as a ratified deviation row, but the register has four rows, none citing layout-§1, and :78 says 'Four rows'. Census row has trigger but no Rule/Decided date; the kit gate reads the word only.  
  *Remediation:* Add register row 5 at CLAUDE.md:77: Rule layout-§1; testkit/framework.lua over cap at 1583; Why condensed from :154-165; Decided 2026-09-23; Re-check trigger from :131. Update :78 to 'Five rows'; repoint census cell to 'Register row (layout-§1, 2026-09-23)'. Or, by owner choice, open an issue and repoint :131.  
  *Rule:* layout-§1; audit-review-history  
  *Planned in:* LK-01
- **LibKa0s-A-05** `low` (audit LK-19; confirmed) — Release runs ship without ANALYSIS.md and docs/releasing.md never asks for one  
  *Where:* docs/releasing.md (step 7, :141-160); docs/automated-tests/20260923-144526/; docs/automated-tests/20260916-093057/ANALYSIS.md:60-62  
  *Evidence:* v1.55.0 release bundle has no ANALYSIS.md; 32 of 38 release-stamped bundles since 2026-09-08 lack one; grep -ci analysis docs/releasing.md returns 0. 20260916-093057/ANALYSIS.md:60-62 misreads a release run's missing write-up as 'not a breach'. Recurs from 2026-09-08.  
  *Remediation:* Add numbered sub-step to releasing.md step 7 (write <stamp>/ANALYSIS.md per AUTOMATED_TESTS.md prompt) and test -f <stamp>/ANALYSIS.md to the hard-precondition block; write-up rides in the bundle commit before the tag. No backfill; next ANALYSIS.md notes the gap once and corrects :60-62's reading. After: grep -ci analysis docs/releasing.md >= 1.  
  *Rule:* automated-tests-§5  
  *Planned in:* LK-31
- **LibKa0s-A-09** `low` (audit LK-30; confirmed) — Kit runner emits 'None.' prose instead of a headed table for empty watch-list sets  
  *Where:* testkit/run-automated-tests.sh:713-728 (fn_table); testkit/run-automated-tests.sh:730 (band_table); docs/automated-tests/RESULTS.md:149-151  
  *Evidence:* '### Functions lizard warned on' followed by 'None.'; both emitters printf 'None.' and return on empty set, while automated-tests-§4 requires a table with header row. Kit vendored byte-identically into eleven consumers, so every consumer's record has the defect. Recurs unchanged.  
  *Remediation:* Track C (kit revision 25->26): print header + separator unconditionally, no data rows (or one '\| — \| … \|' row) for empty set; drop 'None.' early return; self-test asserting header on empty set; bump Kit.VERSION, docs/api/testkit/version-26-docs.md, regenerate members JSON (lua tools/gen-api-members.lua), CHANGELOG entry; sync testkit/ -> tests/_kit/ same commit. Batch with the review's kit changes (C-02 survey, C-09 asserts.lua) into one kit revision so consumers re-vendor once; re-vendor all eleven.  
  *Rule:* automated-tests-§4  
  *Planned in:* LK-09
- **LibKa0s-A-11** `info` (audit LK-32; confirmed) — Over-count in 20260908-181447/ANALYSIS.md:92 never corrected forward  
  *Where:* docs/automated-tests/20260908-181447/ANALYSIS.md:92; docs/automated-tests/20260916-093057/ANALYSIS.md:61  
  *Evidence:* The 2026-09-08 audit found :92 over-counts by one; the next write-up mentions the bundle but does not correct it. Recurs.  
  *Remediation:* Next release ANALYSIS.md Record corrections paragraph states once that 20260908-181447:92 was one too high. Nothing frozen edited.  
  *Rule:* automated-tests-§5  
  *Planned in:* LK-33

**AbsorbTracker**

- **AbsorbTracker-A-20** `info` (both AT-Info-3; review measurement note (RESULTS.md stale); confirmed) — Info: docs/automated-tests/RESULTS.md trails the tree (635 tests; lists test_slashcmds.lua over cap at 1745)  
  *Where:* docs/automated-tests/RESULTS.md, docs/automated-tests/20260916-184524/  
  *Evidence:* The newest bundle is at 1080857, 37 commits behind HEAD, and records 635 tests, NLOC 10555 and 1479 functions. Today's run gives 710, 11389 and 1639. test_slashcmds.lua is now 1304 LOC, not over the cap. The report gives test_helpers.lua as 1415; it is 1416. It is regenerated at release, so the audit did not file it as non-compliant.  
  *Remediation:* S3.3: run the full four-suite bundle (tests/_kit/run-automated-tests.sh) at close-out or at the next bump-version so RESULTS.md and the band table re-align.  
  *Rule:* automated-tests  
  *Planned in:* AT-DOCS

**BankLedger**

- **BankLedger-R-07** `low` (both F-008, BL-24, automated-tests-§4/§6 observation; confirmed) — Committed complexity/automated-test record predates watch-list movement: Insights.lua entered the 1000-1500 band (1002) with no disposition; the Browser note is stale; test counts drifted  
  *Where:* docs/automated-tests/RESULTS.md (newest bundle 20260916-184426, sha 076f674); modules/Insights.lua; modules/Browser.lua  
  *Evidence:* The record is 37 commits behind HEAD: tests 943 to 1017, lint files 67 to 71, NLOC 16,380 to 17,397, functions 2,498 to 2,640, band 3 to 4. Browser went 1208 to 1220 under BL-24, so its 'moving the right way' note is false. Max CCN is still 15 with 0 warnings. No row has commit cells, because all rows predate kit revision 25. BL-24 is advisory: the disposition is owed at the next release, not now.  
  *Remediation:* C-09 / R-1: nothing now, and never regenerate outside release or gate commits on it. At the next /wow-addon:bump-version release run, the regenerated RESULTS.md needs an owner disposition for modules/Insights.lua (accept, or name the I:Layout section-renderer peel seam), Browser 1220 under BL-24 with a corrected note, and the new pass count. Release gate: all four suites pass (perf skip naming performance-§12 after BL-48) and zero CCN above 15. The BL-48 re-vendor run also regenerates it.  
  *Rule:* layout-§1; automated-tests-§3/§4/§6; performance-§10  
  *Planned in:* BL-DOCS

**ConsumableMaster**

- **ConsumableMaster-A-17** `info` (both CM-95 + review measurement note (RESULTS.md stale); confirmed) — docs/automated-tests/RESULTS.md is stale (33 commits behind; 928 tests, 8 functions at CCN 15, pre-peel LOC, deleted test_layout_cap.lua)  
  *Where:* docs/automated-tests/RESULTS.md (:117); bundle 20260916-184427  
  *Evidence:* Today's run shows 998 tests, 116 files and one function at CCN 15 (KCM:OnRegenEnabled, not on the watch list). Category.lua has moved 1400 -> 1141 and Panel.lua 1488 -> 1312. The checkpoint is release, not commit, so this is stale rather than non-compliant.  
  *Remediation:* Nothing now. S5-1: at the next release run the full bundle (bump-version), regenerate RESULTS.md and write ANALYSIS.md. Keep OnRegenEnabled at or under CCN 15 (C-03 lowers it). Never run lizard into the repo as part of remediation.  
  *Rule:* automated-tests-§4; anti-pattern #51  
  *Planned in:* CM-DOCS

**KickCD**

- **KICKCD-A-12** `low` (audit KICKCD-C-10; corrected) — The RESULTS.md watch list is a backlog: four runs of 'watch, no action' citing retired trackers A-2 and KCD-30  
  *Where:* docs/automated-tests/RESULTS.md:84-87  
  *Evidence:* All four band entries have read 'Already tracked as A-2' or 'KCD-30' across 20260908, 20260910 (release 1.3.0) and both 20260916 runs. A-2 resolves only to the retired row docs/audits/2026-08-05/02_DEVIATIONS.md:50. Spells (1444) is past its 1400 re-check line, and IconGrid_Render has no disposition. Related to R-10.  
  *Remediation:* D8/Sprint 6.1, at the next release run: re-run the battery so the band table reflects the current tree (Spells 1444, Castbar 1423, IconGrid 1343, IconGrid_Render 1014, wow_mock 1129). Give each band entry a live GitHub issue naming its peel seam (Spells first, since it is past its own 1400 re-check line, and Castbar is near its 1450 line) or a fix. Write IconGrid_Render's first disposition, since it newly enters the band. Replace the A-2/KCD-30 references with those issue numbers.  
  *Rule:* automated-tests-§4; AP #53  
  *Planned in:* KC-28, KC-DOCS
- **KICKCD-A-23** `info` (both KICKCD-B-04; review Step-0 'committed artifacts disagree' observation; confirmed) — The automated-test record trails HEAD by 38 commits (RESULTS.md shows 973 tests and 4 band files; today it is 1050 and 5)  
  *Where:* docs/automated-tests/RESULTS.md:26, docs/automated-tests/20260916-184417/manifest.json  
  *Evidence:* The newest row, 20260916-184417, measured fac2411; git rev-list --count fac2411..HEAD = 38. Since then: tests 973 -> 1050, lint files 97 -> 101, NLOC 19884 -> 20793, functions 2494 -> 2640, and IconGrid_Render entered the band. The checkpoint is release (last release 1.3.0-release at ed88759), so this is recorded, not filed. The review calls it stale, not non-compliant.  
  *Remediation:* D8/Sprint 6.1: at the next release, run tests/_kit/run-automated-tests.sh (kit rev 25+ adds commit and dirty cells) so RESULTS.md's newest row names HEAD.  
  *Rule:* automated-tests-§4; AP #51  
  *Planned in:* KC-DOCS
- **KICKCD-A-25** `info` (audit KICKCD-B-06; confirmed) — ARCHITECTURE.md describes RESULTS.md as 'generated, never hand-edited', missing the watch-list Disposition exception  
  *Where:* docs/ARCHITECTURE.md:367  
  *Evidence:* The documentation-§3 template reads 'generated by the runner, never hand-edited apart from the watch list's Disposition column'. Part (b) of the prior row moved to C-10 (A-12).  
  *Remediation:* Sprint 4.6: change :367 to the documentation-§3 template wording.  
  *Rule:* documentation-§3  
  *Planned in:* KC-26

**LootHistory**

- **LootHistory-A-20** `low` (audit LH-52; confirmed) — Analytics.lua watch-list 'Peel next' disposition has nothing tracking it  
  *Where:* docs/automated-tests/RESULTS.md:84, modules/Analytics.lua  
  *Evidence:* modules/Analytics.lua has read 'Peel next' for seven runs since 20260804-233322, with no issue in gh issue list --state all. The file is now 1200 lines. The three-release clock has not started (only one release run), so this is not counted as a MUST failure. The review's Known follow-ups also names the Analytics peel as an open watch-list item.  
  *Remediation:* gh issue create 'Peel modules/Analytics.lua: renderers vs formatting/segmenting helpers' with labels state:triaged and severity:low (throttled), or do the peel. At the next automated-tests run, set the Disposition to 'already tracked as #N', the only hand edit RESULTS.md permits.  
  *Rule:* automated-tests-§4 / performance-§10 (anti-pattern #53); MUST NOT not yet reached  
  *Planned in:* LH-35
- **LootHistory-R-20** `info` (review measured observation (01 Measurement run); confirmed) — docs/automated-tests/RESULTS.md is stale against today's run  
  *Where:* docs/automated-tests/RESULTS.md, docs/automated-tests/20260916-184506/manifest.json  
  *Evidence:* The newest bundle records 786 cases, 63 lint files, 15349 NLOC and 2045 functions. Today's run gives 858, 65, 16326 and 2200. Band files have grown: Analytics 1178->1200, Browser 1244->1271 (its disposition says it 'shrank'), Panel 1062->1107. New in the band: tests/test_schema.lua (1048) and tests/test_slash.lua (1020). The review calls this stale, not non-compliant.  
  *Remediation:* No hand edit. Regenerate through the four-suite run at release (/wow-addon:bump-version or run-automated-tests.sh after the LH-69 re-vendor), and refresh the Browser disposition wording then.  
  *Rule:* automated-tests-§4  
  *Planned in:* LH-DOCS

**MultiMeters**

- **MultiMeters-A-21** `low` (audit MM-A-21; confirmed) — Tag 1.0.1-release ships a TOC saying 1.0.0, with no Version History row and no release run  
  *Where:* MultiMeters.toc (at tag 1.0.1-release, 71e5742); README.md:101-104; docs/automated-tests/  
  *Evidence:* `git show 1.0.1-release:MultiMeters.toc` shows '## Version: 1.0.0'. No manifest.json has release 1.0.1.  
  *Remediation:* At the next release, run /wow-addon:bump-version past the tag: 1.1.0 if the MM-A-18a schema bump lands, otherwise 1.0.2. Roll Version History, optionally with a '1.0.1 re-published 1.0.0 unchanged' row. Run the release battery with all four suites at pass before tagging. Never cut a tag without the bump.  
  *Rule:* versioning-git; automated-tests-§3  
  *Planned in:* MM-31
- **MultiMeters-A-26** `info` (both MM-A-26; review Step 0 'committed artifacts that disagree' (RESULTS.md, perf.json); confirmed) — The newest automated-test run is 32 commits and one warned function behind HEAD (stale RESULTS.md)  
  *Where:* docs/automated-tests/RESULTS.md; docs/automated-tests/20260916-184449/; docs/automated-tests/20260916-184449/perf.json; settings/Schema_Paths.lua:943-960  
  *Evidence:* The run records 1884 cases and NS.ValidateSchema at CCN 19. Today there are 1948 cases, ValidateSchema is at 15 and there are 0 warnings. perf.json has suspended at 5202.3 B/iter (0.0 today). The table has no commit cell (pre-rule row).  
  *Remediation:* No separate work. The next release run (MM-A-21, /wow-addon:bump-version) regenerates RESULTS.md with commit cells and drops the stale row.  
  *Rule:* automated-tests-§6  
  *Planned in:* MM-DOCS

**PanelMaster**

- **PanelMaster-A-18** `low` (both PM-033 / review note (RESULTS.md stale); corrected) — The automated-test record is 29 commits stale, and the 1.1.1 release has no release bundle  
  *Where:* docs/automated-tests/RESULTS.md, docs/automated-tests/20260916-184500  
  *Evidence:* The newest bundle, 20260916-184500 (sha 3c4005a, addon 1.1.0), recorded 834 tests, 1624 functions and 13887 NLOC; HEAD has 884, 1687 and 14325. No threshold was crossed and there is no watch-list drift. The 1.1.1 tag (1.1.1-release on dd04000) has no release bundle, and automated-tests-§5 forbids backfilling one.  
  *Remediation:* Cite automated-tests-§6 (a release MUST produce a four-suite bundle before the tag) for the 1.1.1 gap. Also cite automated-tests-§4 for the stale RESULTS trend. Close the gap forward: at the next release, run tests/_kit/run-automated-tests.sh through the ka0s-bounded runner as a release run via /wow-addon:bump-version. Carry the four band dispositions forward, and note once in that bundle's ANALYSIS.md that 1.1.1-release (dd04000) was tagged with no release bundle and with a TOC that still read 1.1.0. Do not create a bundle stamped for 1.1.1 after the fact.  
  *Rule:* automated-tests-§4; automated-tests-§6; anti-pattern #51  
  *Planned in:* PM-DOCS

**PartyFrameEnhanced**

- **PartyFrameEnhanced-A-17** `info` (audit PFE-09; confirmed) — The newest automated-test record (20260918-121606, 227 tests) predates HEAD by 32 commits and has no commit cell; RESULTS.md is stale  
  *Where:* docs/automated-tests/20260918-121606/; docs/automated-tests/RESULTS.md  
  *Evidence:* The record measured e4d7f41 (clean, 1.0.1): 227 tests, 70 files, 7378 NLOC, 942 functions, and it still lists tests/test_spelling.lua, since retired. HEAD has 289 tests, 71 files, 8045 NLOC and 1047 functions. There is no complexity drift. The review noted the same staleness in its measurement run.  
  *Remediation:* At the next release (not a sprint): run tests/_kit/run-automated-tests.sh --release <v> (or /wow-addon:bump-version) over the tree being tagged. The revision-25 runner writes the commit cell.  
  *Rule:* automated-tests-§3/§4/§6  
  *Planned in:* PF-DOCS

**PrettyChat**

- **PRETTYCHAT-A-17** `low` (audit PC-92 (PRETTYCHAT-C-13); confirmed) — RESULTS.md over-cap watch-list row rules a second time (with a stale .pkgmeta citation) instead of pointing at the census row  
  *Where:* docs/automated-tests/RESULTS.md:84  
  *Evidence:* The Disposition for GlobalStrings/GlobalStrings.lua reads 'Accepted — not shipped and not loaded ... .pkgmeta:24', but the line is actually .pkgmeta:39. §4 says the cell points at the census row.  
  *Remediation:* At the next runner run, set the authored Disposition cell to 'exempt — see docs/ARCHITECTURE.md → Files over the 1500-line cap'.  
  *Rule:* automated-tests-§4; layout-§1  
  *Planned in:* PC-DOCS
- **PRETTYCHAT-A-27** `info` (both PC-76 (PRETTYCHAT-B-06, carried, re-measured) + review Step-0 note (RESULTS.md stale by date); confirmed) — Newest automated-test bundle is 30 commits behind HEAD (385 tests vs 438); regenerate at the next release  
  *Where:* docs/automated-tests/RESULTS.md, docs/automated-tests/20260916-184747/  
  *Evidence:* The record shows 385 tests / 46 lint files / 854 functions / 54,311 NLOC. The tree measures 438 / 48 / 941 / 54,817. Max CCN is 14 in both, with the same band file. The checkpoint is release, and no release has been cut since 1.5.0. Not a finding.  
  *Remediation:* Run tests/_kit/run-automated-tests.sh (all four suites) on the re-vendored kit at the next release. Write ANALYSIS.md, and regenerate test-cases.md and the badge. Do not hand-edit.  
  *Rule:* automated-tests-§4; anti-pattern #51  
  *Planned in:* PC-DOCS

**WhatGroup**

- **WHATGROUP-R-14** `low` (both F-014 / WG-48; confirmed) — Automated-test record (RESULTS.md) is stale, 29 commits behind; core/WhatGroup.lua entered the layout-§1 1000-1500 band without a disposition  
  *Where:* docs/automated-tests/RESULTS.md:26, docs/automated-tests/RESULTS.md:66-86, core/WhatGroup.lua, modules/Frame.lua, tests/test_frame.lua  
  *Evidence:* Recorded 20260916-184548 (d64656b): 667 tests, NLOC 9903, 1298 fns, max CCN 15, 45 lint files, 2 band files. HEAD 1124ac4: 727 tests, NLOC 10462, 1368 fns, max CCN 14, 48 files, 3 band files (core/WhatGroup.lua 1099 new; modules/Frame.lua 1144 up from 1063; tests/test_frame.lua 1421). Nothing crossed a threshold; no release since 1.4.0. Review Low, audit Info.  
  *Remediation:* At next release (/wow-addon:bump-version), run tests/_kit/run-automated-tests.sh with all four suites from a clean tree (first kit-revision-25 run, emits commit and clean/dirty cells), disposition core/WhatGroup.lua in the band table, write ANALYSIS.md. Do not hand-edit RESULTS.md now.  
  *Rule:* layout-§1; automated-tests-§1, §4; anti-pattern #51  
  *Planned in:* WG-DOCS


### C15 — Complexity gate, file-size band and test runtime

Functions over CCN 15 fail the release gate, and others sit exactly at the ceiling. Authored files have entered, or sit at the edge of, the layout-§1 1000-1500 on-notice band or the 1500-line cap. AuraMaster's serial test suite does not use --jobs. Affects AuraMaster, AbsorbTracker, ConsumableMaster, KickCD, MultiMeters and LibKa0s.

**LibKa0s**

- **LibKa0s-R-15** `info` (review F-015; corrected) — Four functions sit exactly at the CCN 15 release-gate ceiling  
  *Where:* LibKa0s/Bus.lua:295-347 (lib.Catalog); LibKa0s/Compat.lua:243-260 (lib.GetSpellCooldown); LibKa0s/OptionsWidgets.lua:2944-2953 (idHelpIcon); testkit/mock_record.lua:95-113 (liveTimers)  
  *Evidence:* lizard: max CCN 15 on these four; next added branch fails the tag (automated-tests-§3). None tangled.  
  *Remediation:* C-14: no code change. At the next release run, add watch-list Disposition entries in RESULTS.md for all six functions at CCN 15: Bus.lua:295 lib.Catalog, Compat.lua:243 lib.GetSpellCooldown, OptionsWidgets.lua:2944 idHelpIcon, testkit/mock_record.lua:95 liveTimers, testkit/mock_record.lua:539 M.__fire and testkit/test_layout_cap.lua:427 audit. Batch this with the LK-17d/LK-33 disposition edits.  
  *Rule:* automated-tests-§3; performance-§10  
  *Planned in:* LK-33

**AbsorbTracker**

- **AbsorbTracker-R-14** `info` (review 05_FINAL_SUMMARY known follow-up; confirmed) — Info: tests/test_helpers.lua (1416 LOC) is in the 1000-1500 on-notice band and should be peeled by helper group before it reaches 1500  
  *Where:* tests/test_helpers.lua  
  *Evidence:* The LOC census has 2 files in the band: test_helpers.lua at 1416 and test_slashcmds.lua at 1304, the latter growing to about 1345 with the new cases. The follow-up was already dispositioned in RESULTS.md.  
  *Remediation:* No action this cycle. Peel test_helpers.lua by helper group before it crosses 1500, and watch test_slashcmds.lua as cases are added.  
  *Rule:* layout-§1  
  *Planned in:* AT-DOCS

**AuraMaster**

- **AuraMaster-R-01** `medium` (both F-003; AM-31; confirmed) — Two functions over CCN 15 (Cat.SyncUserCategories CCN 25, renderCategories CCN 16) will fail the release gate, and the committed complexity record is stale  
  *Where:* defaults/Categories.lua:1112-1194; settings/Filters.lua:500-543; docs/automated-tests/RESULTS.md  
  *Evidence:* Fresh lizard: SyncUserCategories NLOC 64, CCN 25, four sequential phases (teardown, insert points, materialize, register); renderCategories CCN 16, a three-way branch on grid kind. The newest run, 20260916-184324, is 129 commits behind: recorded 21,163 NLOC / 2,446 functions / 943 tests / 0 over CCN 15 / 0 files over cap / 2 in band; now 30,336 / 3,348 / 1,296 / 2 / 4 / 4. RESULTS.md still shows tests/test_database.lua at 1037 lines; it is 1702. Its watch list names neither warning.  
  *Remediation:* Pin characterization tests first (testing-§13). Coverage exists in test_defaults, test_database and test_pages_filters; confirm each phase is pinned. Split SyncUserCategories into four named file-local phase helpers (teardownUserDefinitions/insertBeforePaths or insertionAnchors/materializeRecords/registerUserRows, each CCN <= 8, orchestrator <= 5; performance-§11 shapes 2/4, not a part2). For renderCategories, the review extracts renderCustomGrid; the audit prefers a module-level GRID_RENDER per-grid table (shape 1). Either works; pick one. Keep the WHY comments with the code and change no behavior. Check: fresh lizard shows 0 warnings. Regenerate the automated-tests bundle and RESULTS.md at release through the four-suite runner (bump-version), with a Disposition for every new watch-list entry.  
  *Rule:* automated-tests-§3 (release gate); performance-§10/§11; automated-tests-§4; anti-pattern #52  
  *Planned in:* AM-13
- **AuraMaster-A-08** `low` (audit AM-27; confirmed) — Serial commit-gate test suite takes 2m54s wall at 28% CPU utilization; --jobs is not enabled  
  *Where:* tests/run.lua:57-115 (Kit.run with no jobs); docs/testing.md:16-19  
  *Evidence:* E-2: 1296 cases take 2m54s wall and 36.4 s user CPU (about 28%). testing-§14 says --jobs SHOULD be on once the serial gate passes about 10 s.  
  *Remediation:* Measure per testing-§14 (wall, CPU, loadfile vs git spawn) and record the figures in RESULTS.md. Run with -j auto and compare totals and exit code against serial. Fix any suite that fails only when sharded. Then set jobs='auto' in Kit.run in its own commit, separate from other test changes, and correct docs/testing.md:16-19.  
  *Rule:* testing-§14  
  *Planned in:* AM-22

**ConsumableMaster**

- **ConsumableMaster-R-18** `info` (review Known follow-up (05_FINAL_SUMMARY); confirmed) — settings/Panel.lua (1312 LOC) and settings/Category.lua (1141) remain in the layout-§1 on-notice band, and their watch-list acceptance shelf life is up  
  *Where:* settings/Panel.lua; settings/Category.lua; docs/automated-tests/RESULTS.md watch list  
  *Evidence:* Band census: 8 files in the 1000-1500 band, 0 over 1500.  
  *Remediation:* Disposition belongs to the next release run (bump-version), not to this remediation.  
  *Rule:* layout-§1  
  *Planned in:* CM-30

**KickCD**

- **KICKCD-R-10** `low` (review F-010; corrected) — layout-§1 band drift: settings/Spells.lua (1444) has passed its own 'Re-check at 1400' line, and IconGrid_Render.lua has entered the band  
  *Where:* settings/Spells.lua, modules/Castbar.lua, modules/IconGrid.lua, tests/wow_mock.lua, modules/IconGrid_Render.lua  
  *Evidence:* Census of authored Lua: Spells 1444 (was 1246), Castbar 1423 (1345), IconGrid 1343 (1163), wow_mock 1129 (1060), IconGrid_Render 1014 (new, with a blank Disposition). Nothing is over 1500. Max CCN 15, 0 over threshold.  
  *Remediation:* Record current dispositions for all five band files, with IconGrid_Render.lua new and Spells.lua past its 1400 re-check, in the next /wow-addon:automated-tests bundle's watch list. That is where layout-§1 says the band is dispositioned. Optionally do the C-09 mechanical split of the Spells.lua row builders into settings/Spells_Rows.lua: add a TOC line, keep behavior and comments unchanged in the same commit, and keep test_settings_spells_editor unchanged. Sequence it after C-05. The Castbar/IconGrid peels remain follow-ups.  
  *Rule:* layout-§1; AP #52  
  *Planned in:* KC-13, KC-DOCS

**MultiMeters**

- **MultiMeters-R-18** `info` (review 05_FINAL_SUMMARY Known follow-ups (tests/test_provider.lua at cap); confirmed) — tests/test_provider.lua sits at exactly the 1500-line cap and cannot take another case  
  *Where:* tests/test_provider.lua  
  *Evidence:* The census puts it at exactly 1500 lines. 02_PROPOSED_CHANGES says not to add cases there.  
  *Remediation:* Peel it (split by concern) before it takes another case. Until then, add no cases to it.  
  *Rule:* layout-§1  
  *Planned in:* MM-23


### C16 — ARCHITECTURE hub size and one-screen doc limits

documentation-§3 wants the hub under about 400 lines, with any section past about 60 lines spilled to a Tier 2 file, and an exempt performance.md kept to one screen. The hubs run 468-841 lines, with oversized Settings Schema and Message Bus sections. Affects AbsorbTracker, AuraMaster, BankLedger, ConsumableMaster, KickCD, LootHistory, MultiMeters, PanelMaster, PrettyChat and WhatGroup.

**AbsorbTracker**

- **AbsorbTracker-A-13** `low` (audit AT-75; corrected) — docs/ARCHITECTURE.md hub is 788 lines; Settings Schema (116) and Message Bus (73) are past the ~60-line spill threshold  
  *Where:* docs/ARCHITECTURE.md:118-233, docs/ARCHITECTURE.md:234-306, docs/ARCHITECTURE.md:346-399, docs/ARCHITECTURE.md:400-486  
  *Evidence:* wc -l gives 788, up from 454. The spill is a MUST, and the ~400-line hub size is a SHOULD. The disabled-state essay (87 lines) and the Launcher section add to the bulk.  
  *Remediation:* C5/S2.6: cut Settings Schema to about 20 lines plus one link to docs/schema.md, and move the runtime, bulk-bracket and named-state detail there. For Message Bus, spill to docs/message-bus.md as documentation-§3 names it, and flip its Conditional row to Present with the reason 'spill target of the hub rule'. If that conflicts with the more-than-ten threshold, raise it upstream in WowAddonStandards rather than spilling into data-flow.md. Move the disabled-state essay (:400-486) to a Tier 3 docs/lifecycle.md, and add a new '### Addon-specific (documentation-§3, Tier 3)' table after '### Verification and record' to register it. Target 400 lines or fewer, with no mandated section over about 60. Do the C10 line fixes first, and update the test_docs heading pins.  
  *Rule:* documentation-§3  
  *Planned in:* AT-24

**AuraMaster**

- **AuraMaster-A-06** `low` (audit AM-25; corrected) — docs/ARCHITECTURE.md hub is 841 lines, and four sections break the spill rule  
  *Where:* docs/ARCHITECTURE.md:6-74 (Overview 69), :107-243 (Settings Schema 137), :245-268 (Locale routing), :270-318 (Filter priority), :391-419 (Launcher), :444-486 (disabled state), :488-585 (Taint Notes 98), :586-775 (Known Limitations 190)  
  *Evidence:* E-23 section sizes. The SHOULD is about 400 lines, and mandated sections should be about 60 lines or fewer. Known Limitations and Taint Notes have no canonical spill target, and the non-mandated sections add about 150 lines.  
  *Remediation:* Spill every mandated section over about 60 lines, leaving a short summary and exactly one link (documentation-§3). Move Settings Schema detail to docs/schema.md. Move the Taint Notes and Known Limitations detail into docs/midnight-quirks.md, or a new Tier 3 docs/known-limitations.md registered in the Documentation map in the same change, instead of trimming it away. Optionally move the non-mandated sections (Locale routing, Filter priority, the disabled state, the Launcher detail) and the Overview library table to their topic docs (common-tasks.md or data-flow.md, module-map.md, or a registered Tier 3 file) to get toward the roughly 400-line SHOULD. Move content only; delete nothing.  
  *Rule:* documentation-§3 (hub spill rule; ~400-line SHOULD)  
  *Planned in:* AM-33

**BankLedger**

- **BankLedger-A-11** `low` (audit BL-43; confirmed) — docs/ARCHITECTURE.md ## Settings Schema runs 167 lines unspilled; the hub is 522 lines (SHOULD <= ~400)  
  *Where:* docs/ARCHITECTURE.md:45-211; docs/schema.md; docs/settings-panel.md  
  *Evidence:* A mandated section over ~60 lines MUST spill into its topic doc and leave a summary and one link. This one holds the runtime narrative, bulk-bracket rules, the tab list, the registry and recorded data, and four named-state entries, and ends on two links.  
  *Remediation:* S5-1: move the registry, recorded data, named state (:140-210) and runtime/stub narrative (:51-73) to docs/schema.md. Move the bulk-bracket and reset routes (:75-100) and the tabs/Filters text (:102-138) to docs/settings-panel.md. Leave a section of 60 lines or fewer: the row count, the one write seam, one sentence per registry and named state (keeping architecture-§5 naming findable), and exactly one link. Target about 400 lines for the file. Move text, don't rewrite it. Keep tests/test_docs.lua green. Do it before the BL-45 citation sweep.  
  *Rule:* documentation-§3 (hub spill rule); architecture-§5  
  *Planned in:* BL-19

**ConsumableMaster**

- **ConsumableMaster-A-14** `low` (audit CM-92; confirmed) — The docs/ARCHITECTURE.md hub is 504 lines (SHOULD is ~400)  
  *Where:* docs/ARCHITECTURE.md:404-504 (peel narrative :455-504); docs/ARCHITECTURE.md:267-316 (LibKa0s adoption table); docs/ARCHITECTURE.md:447  
  *Evidence:* The Documented deviations section runs 101 lines, and :455-504 is history rather than index. The adoption table is a per-major reference.  
  *Remediation:* B8 / S4-6: move the peel narrative into module-map.md rows or issues #32 and #33. Optionally move the adoption table to module-map.md and leave a summary plus a link. Keep the census table and the sentence at :447 exactly as the kit's test_layout_cap reads them. Target at or under ~420 lines.  
  *Rule:* documentation-§3  
  *Planned in:* CM-26

**KickCD**

- **KICKCD-A-22** `low` (audit KICKCD-C-09; corrected) — docs/ARCHITECTURE.md is 468 lines, over the roughly 400-line SHOULD  
  *Where:* docs/ARCHITECTURE.md:226-310, docs/ARCHITECTURE.md:117  
  *Evidence:* '## The stand-down: disabled is total' runs 85 lines, and the LibKa0s bullet at :117 is one 2,900-character line. No mandated section is over roughly 60 lines.  
  *Remediation:* D6/Sprint 4.8, last among the hub edits: move the stand-down narrative into slash-dispatch.md's disabled-state section (or a Tier 3 stand-down.md) with a summary and one link, and split the :117 bullet into a list linking module-map.md. Target under roughly 400 lines, with every map row still resolving.  
  *Rule:* documentation-§3 (SHOULD)  
  *Planned in:* KC-26

**LootHistory**

- **LootHistory-A-08** `low` (audit LH-60; confirmed) — ARCHITECTURE.md hub is 554 lines; Settings schema section past the ~60-line spill threshold  
  *Where:* docs/ARCHITECTURE.md:118-160, docs/ARCHITECTURE.md  
  *Evidence:* The hub is 554 lines against a ~400-line SHOULD (458 at the last run; issue #31 was closed done at 490). ## Settings schema is 68 lines against the ~60-line MUST and carries five links. ## The disabled state is 79 lines but is not a mandated section. Carried and grown.  
  *Remediation:* Spill the named-state and registry paragraphs of Settings schema (:118-160) into schema.md and leave a summary of 15 lines or fewer with one link. Move The disabled state body to a Tier 3 docs/disabled-state.md registered in ### Addon-specific. Re-measure: hub under 400 lines, section at 60 or fewer.  
  *Rule:* documentation-§3 (hub spill MUST; ~400 SHOULD)  
  *Planned in:* LH-30
- **LootHistory-A-13** `low` (audit LH-70; confirmed) — docs/performance.md is 190 lines; the exempt shape must be one screen  
  *Where:* docs/performance.md  
  *Evidence:* Under the exemption the page must shrink to one screen: it brackets nothing, which of (b)/(c) applies, where the sweep lives, and what re-arms it. It currently carries the 77-line sweep, two allocation essays and a complexity section.  
  *Remediation:* Cut the page to one screen. Move the sweep to a Tier 3 docs/combat-path-sweep.md registered in the map, linked from the page and from the performance-§12 register row. Drop or relocate the allocation and complexity material. Keep tests/test_doc_structure.lua green.  
  *Rule:* documentation-§3 (performance.md under exemption, MUST)  
  *Planned in:* LH-31

**MultiMeters**

- **MultiMeters-A-06** `low` (audit MM-A-06; confirmed) — docs/ARCHITECTURE.md is 762 lines, past the hub's ~400-line SHOULD  
  *Where:* docs/ARCHITECTURE.md:427-499; docs/ARCHITECTURE.md:500-681; docs/ARCHITECTURE.md:621-681; docs/ARCHITECTURE.md:682-717  
  *Evidence:* The size is held by the Documentation map (73 lines), Documented deviations (182 lines) and the Complexity register.  
  *Remediation:* After the MM-A-03 spills, move 'Hard-coded texture paths' (:621-681) to a Tier 3 doc (for example docs/texture-paths.md) registered under Addon-specific, and repoint tests/test_texture_paths.lua. Target 560 lines or fewer. Optionally move 'The segment selector' to data-flow.md or scope.md.  
  *Rule:* documentation-§3 (SHOULD)  
  *Planned in:* MM-28

**PanelMaster**

- **PanelMaster-A-10** `low` (audit PM-042; confirmed) — docs/ARCHITECTURE.md has outgrown the hub shape: 471 lines, a 102-line Settings Schema section, retired-row narratives and non-canonical headings  
  *Where:* docs/ARCHITECTURE.md:30-131, docs/ARCHITECTURE.md:47-78, docs/ARCHITECTURE.md:80-103, docs/ARCHITECTURE.md:132, docs/ARCHITECTURE.md:288, docs/ARCHITECTURE.md:380-428  
  *Evidence:* - The file is 471 lines against a SHOULD of about 400. - Settings Schema is 102 lines against the MUST to spill to schema.md at about 60. - 49 lines of prose describe retired register rows. - Two headings are not canonical: '## Message bus (architecture-§4)' should be 'Message Bus', and '## Taint' should be 'Taint Notes'.  
  *Remediation:* Move :47-78 (the schema-runtime adoption narrative, the stub and the Master controls composition) into docs/schema.md under '## The schema runtime'. Keep a summary of five lines or fewer, the registry naming (:80-103) and one link. Collapse the retired-row narratives to one line each, citing PM-029, #48 and the bundle. Rename the two headings and check tests/test_docs.lua for heading pins. Target: under 400 lines.  
  *Rule:* documentation-§3 (hub and spill rule)  
  *Planned in:* PM-21

**PrettyChat**

- **PRETTYCHAT-A-29** `low` (audit PC-101 (PRETTYCHAT-C-22); corrected) — docs/performance.md claims to be a one-screen answer but runs 230 lines  
  *Where:* docs/performance.md  
  *Evidence:* Most of the length is the sweep that performance-§12 requires. The page is correct, just not one screen long.  
  *Remediation:* Cut docs/performance.md down to one screen with the four facts documentation-§3 names. Move the sweep (currently the '## The sweep' section through the Panel next-frame subsection, :26-134) and the PC-R-05 history (:197-224) into a Tier-3 doc, e.g. docs/performance-sweep.md. Register that doc in ARCHITECTURE.md's ## Documentation map and link to it from the page. The register row should keep citing the sweep commit only.  
  *Rule:* performance-§12; documentation-§3  
  *Planned in:* PC-23

**WhatGroup**

- **WHATGROUP-A-15** `low` (audit WG-76; confirmed) — docs/ARCHITECTURE.md hub is 533 lines (SHOULD stay under ~400)  
  *Where:* docs/ARCHITECTURE.md:193-282, docs/ARCHITECTURE.md:313-341, docs/ARCHITECTURE.md:349-365, docs/ARCHITECTURE.md:367-410  
  *Evidence:* wc -l = 533; mass in unmandated sections: The stand-down (~90 lines), Invariants, Load order, External dependencies. No mandated section exceeds ~60 lines.  
  *Remediation:* Spill ## The stand-down to a new Tier 3 docs/stand-down.md (with Addon-specific row) and ## Load order's per-file list to docs/module-map.md, leaving 5-10 line summaries and a link; target <= ~400 lines; re-run test_docmap/test_doc_structure and fix pins.  
  *Rule:* documentation-§3 (SHOULD)  
  *Planned in:* WG-28


### C17 — Tier 2 doc set: owed, falsely N/A, or re-documenting LibKa0s

Documentation-map rows say 'Not applicable' for docs whose trigger has fired (debug.md, compat-layer.md, slash-dispatch.md, message-bus.md, profiles.md). module-map.md omits files, out-of-scope stores are listed, and compat-layer.md and debug.md restate LibKa0s contracts. The Tier 1 settings-panel row wording conflicts with itself (upstream). Affects AbsorbTracker, AuraMaster, BankLedger, KickCD, MultiMeters, PanelMaster and WhatGroup.

**AbsorbTracker**

- **AbsorbTracker-A-26** `info` (audit AT-Info-9; confirmed) — Info: Documentation-map wording is off for automated-tests/, perf-analysis/ and the RESULTS.md row  
  *Where:* docs/ARCHITECTURE.md:592  
  *Evidence:* The out-of-scope sentence names whole directories while registering their READMEs; the standard names the <run> subdirectories. The RESULTS.md row says 'generated, never hand-edited' and leaves out the Disposition exception. Cosmetic.  
  *Remediation:* Optional: reword to name the <run> subdirectories and mention the Disposition exception. It can go in the R-07/AT-75 doc sweep.  
  *Rule:* documentation-§3  
  *Planned in:* AT-22

**AuraMaster**

- **AuraMaster-A-07** `low` (audit AM-26; confirmed) — docs/spell-research/ is listed as an out-of-scope frozen store that documentation-§3 doesn't allow; its .md files appear in no table  
  *Where:* docs/ARCHITECTURE.md:778-781; docs/ARCHITECTURE.md:817-819; docs/spell-research/2026-09-20/{ANALYSIS,DIFF,SOURCES}.md  
  *Evidence:* documentation-§3's frozen-store list doesn't include spell-research, and repos may not extend it. '### Addon-specific' reads 'None.'  
  *Remediation:* Register the store as one Tier 3 row under Addon-specific ('spell-research/ \| Frozen per-build derivation bundles from tools/spell-research/research.py'; dated bundles not enumerated) and remove it from the prose at :781. Optional upstream: propose adding docs/spell-research/ to the canonical frozen-store list (see AuraMaster-A-19).  
  *Rule:* documentation-§3 (## Documentation map)  
  *Planned in:* AM-31

**BankLedger**

- **BankLedger-A-12** `low` (audit BL-44; confirmed) — docs/debug.md is recorded 'Not applicable' although its trigger fired (/bl debug scan and /bl debug panel are debug surfaces beyond the LibKa0s console)  
  *Where:* docs/ARCHITECTURE.md:467; modules/Ledger.lua:279; settings/Panel.lua:638; settings/Schema.lua:708-721  
  *Evidence:* The N/A row names the two surfaces that fire the trigger. /bl debug scan runs NS.Ledger:Diagnose() and /bl debug panel runs NS.Panel:Diagnose(), both ungated. A false N/A row is worse than the bare omission.  
  *Remediation:* S5-2: write docs/debug.md covering the two verbs, what each prints, their [Scan]/[Panel] tags, the raw-append rule (debug-logging-§4), the registeredEvents/unavailableEvents record, and when to paste each into an issue. Flip ARCHITECTURE:467 to Present, and link it from testing.md or smoke-tests.md if they walk the verbs.  
  *Rule:* documentation-§3 (Tier 2 debug.md trigger)  
  *Planned in:* BL-21

**KickCD**

- **KICKCD-A-09** `low` (audit KICKCD-C-06; confirmed) — The debug.md 'Not applicable' row gives a false reason: the /kcd debug dumps print to chat, not the console  
  *Where:* docs/ARCHITECTURE.md:356, core/Compat.lua:441, modules/Castbar_Debug.lua:134, modules/Cooldowns.lua:661, core/KickCD.lua:307-325  
  *Evidence:* The row says the sub-commands 'dump state through [the console]', but the three dumps (spells, castbar, interrupt) print via NS.Util.print to chat.  
  *Remediation:* D6/Sprint 4.2 (recommended option a): write a Tier 2 docs/debug.md covering the spells, castbar, interrupt and new events (A-03) dumps, and flip the map row to Present with the trigger stated. Option b: route the dumps into NS.Debug and correct the row's reason.  
  *Rule:* documentation-§3 (Tier 2 debug.md)  
  *Planned in:* KC-25
- **KICKCD-A-10** `low` (audit KICKCD-C-07; confirmed) — docs/compat-layer.md restates the contracts of six LibKa0s-Compat members  
  *Where:* docs/compat-layer.md:13-14, docs/compat-layer.md:16-17, docs/compat-layer.md:23-24  
  *Evidence:* Rows for IsSecret, GetSpellCooldown, GetSpellInfo, GetSpellTexture, GetSpecialization and GetSpecializationInfo spell out return shapes and ladders that LibKa0s documents in docs/api/Compat/version-1-docs.md.  
  *Remediation:* D6/Sprint 4.3: collapse the six rows into one line linking LibKa0s docs/api/Compat/version-1-docs.md. Keep only KickCD-specific caveats, e.g. 'use isActive'.  
  *Rule:* documentation-§3 (shims LibKa0s supplies MUST NOT be re-documented)  
  *Planned in:* KC-25

**MultiMeters**

- **MultiMeters-A-03** `low` (audit MM-A-03; confirmed) — Three Tier 2 docs are owed (slash-dispatch.md, message-bus.md, profiles.md), and their register rows falsely say 'Not applicable'  
  *Where:* docs/ARCHITECTURE.md:475; docs/ARCHITECTURE.md:476; docs/ARCHITECTURE.md:477; tests/test_docmap.lua  
  *Evidence:* 18 verbs plus the window sub-tree meet the 8+ command trigger. There are 14 messages against a trigger of more than 10. settings/Profiles.lua hosts AceDBOptions. test_docmap does not judge triggers.  
  *Remediation:* Spill the Slash commands, Message bus and Profiles material into the three canonical docs (a move, with a summary and link left in the hub). Flip the rows to Present, and keep test_docmap and test_doc_structure green. Do this after the code sprints.  
  *Rule:* documentation-§3  
  *Planned in:* MM-27

**PanelMaster**

- **PanelMaster-A-04** `low` (audit PM-031; confirmed) — docs/compat-layer.md is missing although core/Compat.lua has 8 shims (threshold 3), and the map row says 'Not applicable'  
  *Where:* docs/ARCHITECTURE.md:327, core/Compat.lua:27,56,65,79,103,124,139,164  
  *Evidence:* Carried from 2026-09-08. The documentation-§3 grep returns 8 shims. The LibKa0s-Compat-1.0 decision (#53) makes all eight addon-specific. The map row still asserts Not applicable.  
  *Remediation:* Write docs/compat-layer.md with one section per shim (AddOnFolders, GetScreenSize, GetUIScale, InCombat, RegisterMedia, FetchMedia, MediaList, MouseIsOver): what varies, what the guard answers when the API is absent, and who calls it. Link #53. Flip the row to '\| compat-layer.md \| Present \| 8 shims in core/Compat.lua (threshold is 3) \|'. Update tests/test_docs.lua if it pins the map. The R-03 fix changes the InCombat shim, so document its final form.  
  *Rule:* documentation-§3 (Tier 2 compat-layer.md)  
  *Planned in:* PM-20
- **PanelMaster-A-11** `low` (audit PM-043; confirmed) — docs/module-map.md misses 28 of 32 authored test files and 3 of 4 tools/ generators  
  *Where:* docs/module-map.md, tests/, tools/artwork/artwork_cleaner.py, tools/artwork/make_poster.py, tools/artwork/update_catalog.py  
  *Evidence:* The basename check finds every test_*.lua except test_envsetup, test_harness, test_libka0s and test_surface_parity unmentioned, and the same for run.lua, wow_mock.lua, degraded_env.lua and prose_waivers.lua. Three artwork generators are also missing (03_EVIDENCE.md §10).  
  *Remediation:* Add a '## tests/' table: rows for run.lua, wow_mock.lua, degraded_env.lua and prose_waivers.lua, plus one row per suite or a suite-family table naming every file. Add a '## tools/' table with four generator rows describing what each writes.  
  *Rule:* documentation-§3 (Tier 1 module-map.md: every non-vendored file)  
  *Planned in:* PM-22

**WhatGroup**

- **WHATGROUP-A-14** `low` (audit WG-75; corrected) — compat-layer.md and debug.md re-document LibKa0s substrate instead of addon-specific content  
  *Where:* docs/compat-layer.md:21-22, docs/ARCHITECTURE.md:464, docs/ARCHITECTURE.md:462, docs/debug.md, core/Compat.lua:50, core/Compat.lua:58  
  *Evidence:* compat-layer.md documents library GetSpellName/GetSpellTexture rung by rung; map row claims 'eight addon-specific shims' but the standard's grep counts 6 (two are library members). debug.md registered Present on a Tier 2 trigger (debug surfaces beyond the LibKa0s console) that has not fired; most of the page restates LibKa0s-DebugLog guarantees.  
  *Remediation:* Trim compat-layer.md to the six addon-owned shims (GetSpellLink, IsSpellKnown, GetSpellCooldownRemaining, GetSpellCooldownTimes, GetActivityInfoTable, AddOnLinkType). Replace the two library rows with a one-line pointer to LibKa0s docs/api/Compat/version-1-docs.md. Change the count to six at compat-layer.md:16, ARCHITECTURE.md:388 and ARCHITECTURE.md:464. Trim debug.md to addon-owned content (descriptor fields, tag vocabulary, adding a debug line, /wg debug semantics) and point at the library for window/format/font/copy-clear. Then set the :462 row honestly: either 'Not applicable' with the tag vocabulary moved to a Tier 3 doc, or Present with a stated reason. Re-run test_docmap/test_doc_structure.  
  *Rule:* documentation-§3 (MUST NOT re-document library shims)  
  *Planned in:* WG-24
- **WHATGROUP-A-22** `info` (audit WG-56; confirmed · upstream → WowAddonStandards) — documentation-§3 Tier 1 settings-panel.md row says 'Tab \| Covers (one row per settings subcategory)', contradicting its own granularity  
  *Where:* docs/settings-panel.md:327-341  
  *Evidence:* Column named Tab but rows are pages; WhatGroup has one subcategory, three tabs; repo carries per-tab tables (8/8/3) and page->tab->row tree. Carried, standards-upstream.  
  *Remediation:* Upstream in WowAddonStandards: pick Page \| Covers or per-tab rows and word the row to match; then re-check docs/settings-panel.md against the amended text (S6-2).  
  *Rule:* documentation-§3  
  *Planned in:* WS-07, WG-26


### C18 — Documented-deviations register hygiene

Register rows are stale (the rule changed or the trigger fired), cite evidence ids that resolve to nothing, key the wrong section, or record compliant behaviour. Rows are missing for real declines, and accepted deviations and closed items are recorded as info. Each register needs an evaluate-and-rewrite docs pass in AbsorbTracker, AuraMaster, BankLedger, ConsumableMaster, LibKa0s, LootHistory, MultiMeters, PanelMaster, PartyFrameEnhanced, PrettyChat and WhatGroup.

**LibKa0s**

- **LibKa0s-A-12** `info` (audit LK-38; confirmed) — Register row 1 evidence cites a review bundle that doesn't exist (resolves only to a commit)  
  *Where:* CLAUDE.md:73  
  *Evidence:* Row 1 says 'Filed by the v1.31.0 review'; docs/reviews/ holds 2026-07-31, 2026-08-05, 2026-09-07 only; the review is commit 1f1790c (2026-09-12) with no frozen bundle.  
  *Remediation:* Change evidence to 'Filed by the v1.31.0 review (commit 1f1790c, recorded in docs/api/testkit/version-17-docs.md)'.  
  *Rule:* audit-review-history  
  *Planned in:* LK-30

**AbsorbTracker**

- **AbsorbTracker-A-11** `low` (audit AT-73; corrected) — The events-frames-taint-§1 register row records as a deviation behaviour v2.64.0 now permits (the unit-filter carve-out)  
  *Where:* docs/ARCHITECTURE.md:652, docs/ARCHITECTURE.md:676-697, docs/ARCHITECTURE.md:507, core/AbsorbTracker.lua:84, core/AbsorbTracker.lua:140-157, core/Lifecycle.lua:95  
  *Evidence:* The private CreateFrame per unit has only SetScript OnEvent plus RegisterUnitEvent, is held at self.__unitEventFrames, is unregistered in StandDown, and is reused. That meets all four carve-out conditions, yet the row, the :507 text and the code comment at :84 still call it a deviation.  
  *Remediation:* C3/S1.2: delete the events-frames-taint-§1 register row, leaving 3 rows. Replace ARCHITECTURE.md:676-697 with a short design note that cites the carve-out and names each condition by symbol: the only job is RegisterUnitEvent plus onEvent; held at addon.__unitEventFrames; unregistered in Lifecycle StandDown; created once and reused. Reword ARCHITECTURE.md:507, core/AbsorbTracker.lua:84 (comment only), docs/data-flow.md:77, docs/module-map.md:425 and :807, and docs/midnight-quirks.md:120 to 'the events-frames-taint-§1 unit-filter carve-out'. In midnight-quirks, also correct the frame description to one frame per unit. Check: the register has 3 rows, and grep -rn 'events-frames-taint-§1 deviation' over the live docs and code, excluding docs/audits, docs/reviews, docs/investigations and docs/superpowers, returns nothing.  
  *Rule:* audit-review-history, documentation-§3, events-frames-taint-§1  
  *Planned in:* AT-23
- **AbsorbTracker-A-18** `info` (audit AT-Info-1; confirmed) — Info: no close-button wrapper exists, and none is needed  
  *Where:* core/CoreSetup.lua, core/PerfSetup.lua:118  
  *Evidence:* NS.MakeCloseButton was removed at f445da8. The addon builds no close control (no host window, and the perf panel uses the library's arm). The standalone-windows 'wrap exactly once' rule is scoped to the addon's own windows.  
  *Remediation:* None; not filed.  
  *Rule:* standalone-windows  
  *Planned in:* AT-22

**AuraMaster**

- **AuraMaster-A-02** `low` (audit AM-20; confirmed) — README ## Screenshots is still a placeholder on a published addon; the register row's trigger has fired, and the docs disagree on whether the addon is published  
  *Where:* README.md:26-29; README.md:156; docs/ARCHITECTURE.md:826 (register row); docs/ARCHITECTURE.md:744-745; AuraMaster.toc:13  
  *Evidence:* The TOC has carried X-Curse-Project-ID 1698345 since a326ed7 (2026-09-16), and the README shows the live CurseForge badge. The row cites 'item 5', but Screenshots is item 4 since v2.45.0, and the row itself says its first-publish half has fired. Known Limitations says 'Unpublished', while the Version History records a 'First release' and the placeholder says screenshots come 'before the first release'.  
  *Remediation:* Capture real in-client screenshots into media/screenshots/ (issue #3). Add a captioned ## Screenshots between the description and Usage, run the README de-AI pass, and decide the .pkgmeta handling (ignore). Retire the register row. Until the images exist, the owner re-ratifies it (item 4, a new Decided date, a trigger such as 'captioned images land') or leaves the finding open. Delete or restate the 'Unpublished' Known Limitations bullet and drop the 'before the first release' wording. Optional guard: the docs gate asserts at least one image in Screenshots when the TOC has X-Curse-Project-ID.  
  *Rule:* documentation-§1 item 4; audit-review-history (register triggers)  
  *Planned in:* AM-32
- **AuraMaster-A-12** `low` (audit AM-32; corrected) — Four unratified layout-§1 rows sit in the Documented deviations register, and their triggers are instructions, not conditions  
  *Where:* docs/ARCHITECTURE.md:827-830; docs/ARCHITECTURE.md:834-841 (census)  
  *Evidence:* Each Why cell says the row 'awaits the owner's ratification', but the register only holds ratified decisions. Open issues #16-#19 already give each over-cap file a compliant terminal state. The trigger 'the next change that grows this file carries the peel..., and so does the next standards audit' names this run.  
  *Remediation:* Delete the four unratified layout-§1 rows at docs/ARCHITECTURE.md:827-830 and let open issues #16-#19 carry each file's terminal state (layout-§1, second state). Rewrite the census preamble and the four Terminal state cells to cite only the issue and seam, dropping every 'The layout-§1 row above...' clause. If the owner prefers to ratify the rows instead, keep them, remove 'awaits ratification', put the ratification date in Decided, and shrink the trigger to its condition alone: 'Retired when the peel along the named seam lands and the file is back under 1500 lines.' Afterwards test_layout_cap must stay green.  
  *Rule:* documentation-§3 (register); audit-review-history (trigger evaluation); layout-§1  
  *Planned in:* AM-23, AM-24, AM-25, AM-26
- **AuraMaster-A-17** `info` (audit AM-03 (recorded, not counted); confirmed) — Recorded deviation: a unit-scoped container shows the previous unit's class until re-apply after a swap made under lockdown or secrecy  
  *Where:* docs/ARCHITECTURE.md:825  
  *Evidence:* The options-ui-§17 register row, ratified 2026-09-12, cites docs/audits/2026-09-11 AM-03. Neither trigger has fired: there is no class-colour engine binding, and MustDefer still holds.  
  *Remediation:* No action. Re-read the trigger at the next audit.  
  *Rule:* options-ui-§17 (one resolver)  
  *Planned in:* AM-32

**BankLedger**

- **BankLedger-A-05** `low` (audit BL-34a; confirmed) — The expired options-ui-§12 register row still reads as live after its re-check trigger fired on 2026-09-11 (derived from BL-34)  
  *Where:* docs/ARCHITECTURE.md:505  
  *Evidence:* The row (decided 2026-09-02) calls itself 'a placeholder for a resolution, not an exemption' with the trigger 'Re-check at the next release'. 1.1.0-release was tagged 2026-09-11.  
  *Remediation:* S2-2: delete the row in the same commit that closes BL-34 (Option A), or replace it with a new row carrying a real trigger (Option B).  
  *Rule:* audit-review-history (deviation register, third MUST)  
  *Planned in:* BL-05
- **BankLedger-A-17** `info` (audit BL-07; confirmed) — Accepted deviation: no per-profile store (global-only SavedVariables)  
  *Where:* docs/ARCHITECTURE.md:502  
  *Evidence:* Register row decided 2026-07-27. The trigger (first per-profile setting) has not fired. The rule is unchanged in substance.  
  *Remediation:* None. Re-evaluate the trigger at the next audit.  
  *Rule:* savedvariables-§2  
  *Planned in:* BL-24
- **BankLedger-A-18** `info` (audit BL-11..BL-17; confirmed) — Accepted deviation: performance-§12 no-combat-path exemption (one row)  
  *Where:* docs/ARCHITECTURE.md:501; docs/performance.md:46,55-60; core/BankLedger.lua:91-92  
  *Evidence:* Decided 2026-08-05 with evidence issue #9 (LIBKA0S-17). The trigger has not fired: no OnUpdate or repeating ticker, and the combat-edge pair is bounded and named in the sweep. Its stale Why sentence is filed under BL-45 (R-06). Note that R-01's rescan-armed state threatens the exemption's premise.  
  *Remediation:* None for the row itself. Keep the sweep current: fix R-01, R-06 and R-09.  
  *Rule:* performance-§12  
  *Planned in:* BL-20
- **BankLedger-A-19** `info` (audit BL-04; confirmed) — Accepted deviation: English-only localization  
  *Where:* docs/ARCHITECTURE.md:503; locales/enUS.lua; locales/PostLoad.lua  
  *Evidence:* Decided 2026-07-31. Issue #3 and BL-04 (2026-09-07) resolve. The trigger (first non-English locale) has not fired.  
  *Remediation:* None (but close issue #3, A-10).  
  *Rule:* localization-§1  
  *Planned in:* BL-24
- **BankLedger-A-20** `info` (audit BL-28; confirmed) — Accepted deviation: host close-button factory instead of lib.MakeCloseButton (terminal compliant decline)  
  *Where:* docs/ARCHITECTURE.md:504; modules/Browser.lua:95,101,1056; modules/SessionWindow.lua:485; modules/Export.lua:362  
  *Evidence:* All four conditions were re-checked and hold: host windows only, the catalog close through NS.Icon, one factory with three callers, and the row present. The trigger has not fired. Its drifted line numbers are filed under BL-45 (R-06).  
  *Remediation:* None. The citation fix is in R-06.  
  *Rule:* standalone-windows  
  *Planned in:* BL-20
- **BankLedger-A-22** `info` (audit BL-35, BL-40 (closed); confirmed) — Closed since 2026-09-08: BL-35 (British spellings, now caught by the kit's test_prose gate) and BL-40 (Panel.lua said six tabs)  
  *Where:* tests/_kit/test_prose.lua; tests/run.lua:36; settings/Panel.lua:736-741  
  *Evidence:* test_prose scans the whole tracked set and is green. Panel.lua now says five tabs (a different stale phrase at :767 is under BL-45).  
  *Remediation:* None. Recorded as closed.  
  *Rule:* localization-§5; documentation-§5  
  *Planned in:* BL-DOCS

**ConsumableMaster**

- **ConsumableMaster-A-11** `low` (audit CM-90; confirmed) — The stale preview-mode register row: its rule changed (v2.47.0 / v2.49.0 exempts this addon) and its re-check trigger fired  
  *Where:* docs/ARCHITECTURE.md:416; docs/ARCHITECTURE.md:418  
  *Evidence:* v2.49.0 exempts an addon whose unlocked view is its preview and names Ka0s Consumable Master. The trigger 'a preview / test verb added to /cm' fired at 87ed204 and was reversed at 9c45eff, with no update to the row.  
  *Remediation:* B6 / S4-2: retire the row. Add a prose retirement line under the table next to the toc-file-§5 note. Alternatively, the owner re-decides the row against the current text with today's date.  
  *Rule:* audit-review-history; documentation-§3  
  *Planned in:* CM-26
- **ConsumableMaster-A-18** `info` (audit CM-96; confirmed) — The compat register row names two of the four direct GetItemInfo call sites  
  *Where:* docs/ARCHITECTURE.md:415; modules/KCMItemRow.lua:96; modules/KCMItemRow.lua:139  
  *Evidence:* The row cites core/TooltipCache.lua:459 and modules/Ranker.lua:88 only. Related to F-005: if C-06 routes those two through Compat, the row's cited sites change.  
  *Remediation:* B8 / S4-9: add KCMItemRow.lua:96 and :139 to the row's What differs cell, and reconcile the row with F-005's Compat change in the same edit.  
  *Rule:* audit-review-history  
  *Planned in:* CM-13

**LootHistory**

- **LootHistory-A-17** `low` (audit LH-74; confirmed) — Deconstruct attribution matches localized spell names with no localization-§4 register row  
  *Where:* modules/Attribution.lua:64, modules/Attribution.lua:94, modules/Attribution.lua:20-50  
  *Evidence:* Seed ids resolve to client-locale names (:64), and cast names are matched against them (:94). This is locale-correct by construction and reasoned in comments and closed issue #2. But the MUST says never by a localized display string, and a departure reasoned only in comments is not ratified.  
  *Remediation:* Add a localization-§4 row to docs/ARCHITECTURE.md ## Documented deviations. Why: per-herb/ore Mass Mill/Prospect ids are not enumerable, and the names are derived from ids on the same client, so there is no English literal (cite :20-50 and #2). Trigger: Blizzard exposes a stable deconstruct token or category, or the id set becomes enumerable. Alternatively, replace the fallback with an id list.  
  *Rule:* localization-§4 (MUST); documentation-§3 register  
  *Planned in:* LH-29

**MultiMeters**

- **MultiMeters-A-25** `low` (audit MM-A-25; confirmed) — Two library-stack-§8 declines (Tooltip TARGET_ICON, Window size-grabber) exist only as census dispositions, with no register row  
  *Where:* modules/Tooltip.lua:107; modules/Window.lua:645-646; docs/ARCHITECTURE.md:667; docs/ARCHITECTURE.md:669-670; libs/LibKa0s/Media.lua:136; libs/LibKa0s/Media.lua:103  
  *Evidence:* The catalog carries 'target' and 'resize'. The census rows have no Decided date and no trigger. The ColumnBlocks decline has the proper row at :519.  
  *Remediation:* The owner chooses. (a) Adopt: NS.Icon('target') with the path as the nil fallback, and a resize grip with a vertex-tint hover. A hover variant, if wanted, is an upstream LibKa0s-Media-1.0 addition made first (generator, minor bump, re-vendor). (b) Ratify: add two register rows citing library-stack-§8 with Decided dates and triggers, and extend the test_texture_paths register assertion.  
  *Rule:* library-stack-§8; documentation-§3; audit-review-history  
  *Planned in:* MM-28

**PanelMaster**

- **PanelMaster-A-07** `low` (audit PM-039; confirmed) — The architecture-§5 register row's re-check trigger is met at the library layer (SchemaRuntime instance addressing) but has not been re-decided  
  *Where:* docs/ARCHITECTURE.md:378, libs/LibKa0s/Schema.lua:236, libs/LibKa0s/Schema.lua:339-342, libs/LibKa0s/Schema.lua:432, settings/Schema.lua:360, docs/revendor/2026-09-23-v1.55.0/05_SUMMARY.md:94-98  
  *Evidence:* The trigger reads 'schema helper gains instance addressing'. S.Set(path, value, instanceId) now passes the id to resolveRoot, but the host resolver ignores it and the colon wrappers do not forward it. No open issue carries the owner's decision, and #49 is closed. The trigger text is ambiguous.  
  *Remediation:* Owner's decision, recorded either way. (a) Adopt: resolveRoot(parts, id) maps an id to the panel record, instance-relative rows are registered for C.PANEL_FIELD_TYPE fields, Registry:Set routes through NS.SchemaRuntime.Set(path, v, id), and the row retires. This is a large change and needs its own state:triaged issue. (b) Keep: re-word the trigger to the host-side condition, re-date the row, and file a state:triaged issue with option (a) as its body.  
  *Rule:* audit-review-history (third MUST: evaluate every re-check trigger); architecture-§5  
  *Planned in:* PM-15

**PartyFrameEnhanced**

- **PartyFrameEnhanced-A-04** `low` (audit PFE-10; confirmed) — The deviation register's only row (events-frames-taint-§1) is stale; v2.63.0 ruled it is not a violation  
  *Where:* docs/ARCHITECTURE.md:352  
  *Evidence:* The v2.63.0 changelog item (5): "PartyFrameEnhanced's row turned out not to be a violation at all". The row's trigger has not fired; the only RegisterUnitEvent in libs/ is a comment at Lifecycle.lua:83.  
  *Remediation:* Audit Sprint 4.1: delete the row and write 'None.' under ## Documented deviations. Keep the ### Files over the 1500-line cap sub-heading where it is, because test_layout_cap parses it. Move the one-sentence rationale, citing the v2.63.0 ruling, into Event Subscriptions.  
  *Rule:* audit-review-history (register MUST 2), documentation-§3  
  *Planned in:* PF-22

**PrettyChat**

- **PRETTYCHAT-A-12** `low` (audit PC-73 (PRETTYCHAT-B-03, carried); confirmed) — toc-file-§1 register row still records the absent X-Wago-ID as a deviation (it is a MAY)  
  *Where:* docs/ARCHITECTURE.md:271  
  *Evidence:* The row's What/Why say X-Wago-ID is absent and that toc-file-§1 asks for both distribution ids. Omitting it is compliant, so the Wago half is a graveyard entry.  
  *Remediation:* Narrow the row to the brand mark: strike the Wago clauses, reduce the trigger to 'a decision to retire the brand mark', and record the narrowing in the retired block. Issue #7 stays will-not-do.  
  *Rule:* documentation-§3; audit-review-history; toc-file-§1  
  *Planned in:* PC-21
- **PRETTYCHAT-A-13** `low` (audit PC-88 (PRETTYCHAT-C-10); confirmed) — The debug-logging-§2 register row records compliant behaviour and should be retired  
  *Where:* docs/ARCHITECTURE.md:272  
  *Evidence:* The row's own Why says core/MediaSetup.lua calls Media.RegisterLSM like every other addon, which is exactly what debug-logging-§2 asks. The no-op without LSM follows from library-stack-§3.  
  *Remediation:* Retire the row into the retired block with the date and this reasoning. Optionally keep the fixed-monospace note as prose.  
  *Rule:* audit-review-history (register MUST 2); documentation-§3  
  *Planned in:* PC-21
- **PRETTYCHAT-A-14** `low` (audit PC-89 (PRETTYCHAT-C-11); confirmed) — The localization-§1 register row cites LIBKA0S-05, which resolves to nothing  
  *Where:* docs/ARCHITECTURE.md:276, locales/enUS.lua:26, tests/test_locale.lua:237  
  *Evidence:* grep over docs/audits and docs/reviews finds no LIBKA0S-05, and there is no issue by that id. LIBKA0S-06 and LIBKA0S-01 do resolve.  
  *Remediation:* Re-point the citation at a resolvable source (LibKa0s README section 'The L trap', or an issue) in the row and in both code comments.  
  *Rule:* audit-review-history (register MUST 3)  
  *Planned in:* PC-21

**WhatGroup**

- **WHATGROUP-A-05** `low` (audit WG-61; confirmed) — Two register rows cite evidence ids that resolve to nothing or to a different finding (carried)  
  *Where:* docs/ARCHITECTURE.md:503, docs/ARCHITECTURE.md:504, docs/ARCHITECTURE.md:494-498  
  *Evidence:* WG-R-06 resolves to WHATGROUP-R-06 (Compat.IsSpellKnown, issue #15), not the localization decision (real evidence F-006 in docs/reviews/2026-08-05/). WG-A-08 is assigned by no bundle (real evidence WG-37 in docs/audits/2026-08-05/).  
  *Remediation:* Change :503 WG-R-06 -> F-006 (2026-08-05 review) and :504 WG-A-08 -> WG-37 (2026-08-05 audit); extend the key at :494-498 to name the F-NNN review shape and dated bundle. Land together with WG-63 test tightening.  
  *Rule:* audit-review-history (register MUST: evidence ids resolve); documentation-§3  
  *Planned in:* WG-22
- **WHATGROUP-A-06** `low` (audit WG-63; confirmed) — Register-evidence gate test is green against WG-61's broken ids (derived from WG-61, carried)  
  *Where:* tests/test_register.lua:94, tests/test_register.lua:59-77  
  *Evidence:* test_register skips any -R- id (:94) and isAssigned accepts any table cell in any bundle (:59), including echo tables; last touched e735453 (2026-09-08).  
  *Remediation:* Resolve WG-R-NN/F-NNN ids against docs/reviews/ instead of skipping; drop bundles' Recorded deviations echo tables from isAssigned's corpus; add -- red under: restore WG-A-08 in :504. Must go red against current :503/:504, then land together with WG-61 fix.  
  *Rule:* testing-§12 (MUST); audit-review-history  
  *Planned in:* WG-22
- **WHATGROUP-A-17** `low` (audit WG-78; confirmed) — English-only register row keyed to localization-§3 instead of localization-§1  
  *Where:* docs/ARCHITECTURE.md:503  
  *Evidence:* localization-§3 state 2 requires a row citing localization-§1 (where the routing SHOULD lives); Rule cell reads localization-§3.  
  *Remediation:* Change :503 Rule cell to `localization-§1`.  
  *Rule:* audit-review-history (MUST); localization-§3  
  *Planned in:* WG-22


### C19 — Issue-store label and premise housekeeping

Closed issues carry open-state labels and open issues carry state:done. Triaged issues rest on premises already resolved, and some declines are contradicted by the tree. The fix is a GitHub-only relabel and close pass, throttled, in AbsorbTracker, AuraMaster, BankLedger, KickCD, MultiMeters and PanelMaster.

**AbsorbTracker**

- **AbsorbTracker-A-19** `info` (audit AT-Info-2; confirmed) — Info: issue-store housekeeping. #25 is open over a condition that no longer exists; #26 declines Widgets, which is now bound  
  *Where:* GitHub issues #25, #26; libs/LibStub/; modules/Bar.lua (DragHandle)  
  *Evidence:* find libs/LibStub -type f returns only LibStub.lua, while #25 still describes five files. #26 says will-not-do for Widgets, yet modules/Bar.lua uses the Widgets DragHandle.  
  *Remediation:* S2.8 (optional): close #25 as resolved and re-triage #26.  
  *Rule:* audit-review-history  
  *Planned in:* AT-DOCS
- **AbsorbTracker-A-27** `info` (audit AT-Info-10; confirmed) — Info: open severity:high bug #10 ('Border is acting funny') is a backlog item, not a standards deviation  
  *Where:* GitHub issue #10  
  *Evidence:* This is an open high-severity issue in the store. The audit did not investigate it and referred it to code review, and the review did not raise it.  
  *Remediation:* Triage or investigate #10 separately (issue-triage, or a targeted debug session).  
  *Planned in:* AT-DOCS

**AuraMaster**

- **AuraMaster-A-16** `info` (audit AM-36; confirmed) — Issue #10 is closed but labelled state:triaged (an open-status label)  
  *Where:* GitHub issue #10 (tusharsaxena/AuraMaster)  
  *Evidence:* 'Let players create their own spell categories' shipped (docs/ARCHITECTURE.md:167-214) but still carries state:triaged.  
  *Remediation:* gh issue edit 10 --remove-label state:triaged --add-label state:done. Space it out from any bulk label work.  
  *Rule:* audit-review-history (status-label vocabulary)  
  *Planned in:* AM-28

**BankLedger**

- **BankLedger-A-10** `low` (audit BL-39; confirmed) — Issue #3 is open state:triaged for a localization-§1 register row that already exists (recurs)  
  *Where:* GitHub issue #3; docs/ARCHITECTURE.md:503  
  *Evidence:* Issue #3 ('Record the BL-04 deviation in ARCHITECTURE's Documented deviations register') is OPEN with state:triaged and severity:low. The row exists at ARCHITECTURE:503 (M5-02). No explicit MUST fails.  
  *Remediation:* S6-1: gh issue close 3 --comment 'Row landed: docs/ARCHITECTURE.md -> Documented deviations, localization-§1 (M5-02).', then gh issue edit 3 --remove-label state:triaged --add-label state:done. Use gh subcommands, not GraphQL, and throttle the API writes.  
  *Rule:* audit-review-history (issue store)  
  *Planned in:* BL-24
- **BankLedger-A-21** `info` (audit audit-review-history issue-store observation; confirmed) — state:will-not-do issues decline library adoptions/scope, not rules; none owes a register row  
  *Where:* GitHub issues #4, #6, #7, #8, #10, #15, #20 (#5 and #9 have rows)  
  *Evidence:* This is an observation only. No action is needed.  
  *Remediation:* None.  
  *Rule:* audit-review-history (issue store)  
  *Planned in:* BL-24

**KickCD**

- **KICKCD-A-13** `low` (audit KICKCD-C-11; confirmed) — Issue #15 is OPEN but labeled state:done  
  *Where:* GitHub issue #15, README.md:125  
  *Evidence:* gh issue list shows '15 OPEN bug,state:done,severity:low'. The 1.3.0 Version History row cites #15 as fixed.  
  *Remediation:* Sprint 5.2: close #15 if the fix shipped in 1.3.0, otherwise relabel it state:triaged. Throttle GitHub writes.  
  *Rule:* audit-review-history (state:done is terminal and closed)  
  *Planned in:* KC-28
- **KICKCD-A-24** `info` (audit KICKCD-B-05; confirmed) — Issue #9 still carries an '[Optional]' title prefix  
  *Where:* GitHub issue #9  
  *Evidence:* '[Optional]' is not a state: value, so this is not AP #62, but it is noise by analogy.  
  *Remediation:* Sprint 5.4: strip '[Optional]' from #9's title.  
  *Rule:* audit-review-history; AP #62 (by analogy)  
  *Planned in:* KC-28
- **KICKCD-A-26** `info` (audit KICKCD-C-12; confirmed) — Closed decline #12 (LibKa0s-Widgets 'no control wants it') is contradicted by the tree  
  *Where:* GitHub issue #12, settings/Spells.lua (ReorderList), modules/Castbar_Handle.lua:41  
  *Evidence:* The addon now consumes LibKa0s-Widgets-1.0 twice (ReorderList and DragHandle). No register row is owed.  
  *Remediation:* Sprint 5.3: comment on #12 recording the Widgets adoption, with commits, so a later re-vendor does not read the decline as current.  
  *Rule:* audit-review-history  
  *Planned in:* KC-28

**MultiMeters**

- **MultiMeters-A-16** `low` (audit MM-A-16; confirmed) — Three closed issues carry an open-state label (#4, #21 state:triaged; #24 state:untriaged)  
  *Where:* GitHub issues #4, #21, #24  
  *Evidence:* `gh issue list --state all`: #4 and #21 are CLOSED with state:triaged, and #24 is CLOSED with state:untriaged.  
  *Remediation:* Relabel with spaced gh issue edit calls: #21 -> state:done; #4 -> terminal after reading it (likely will-not-do); #24 -> terminal after reading it against #22. Then verify that closed+triaged and closed+untriaged both return nothing.  
  *Rule:* audit-review-history (Pending-audit decisions live in GitHub issues)  
  *Planned in:* MM-31

**PanelMaster**

- **PanelMaster-A-19** `info` (audit PM-047; confirmed) — Five open state:triaged issues (#19, #20, #22, #23, #24) have premises that are already resolved  
  *Where:* GitHub issues #19, #20, #22, #23, #24; CLAUDE.md:83; ADDONS.md:26; PanelMaster.toc:13; README.md:4; docs/ARCHITECTURE.md:375  
  *Evidence:* - #19: agent-context.md was deleted. - #20: the addon is registered in ADDONS.md:26. - #22: X-Curse-Project-ID 1642836 is present. - #23: the CurseForge badge is present. - #24: the performance-§1 row is ratified.  
  *Remediation:* Close #19, #20, #22 and #23 as state:done and #24 as state:will-not-do, each with a one-line evidence comment (gh issue close plus a label edit). Space out the API writes.  
  *Rule:* audit-review-history (the issue store is the backlog)  
  *Planned in:* PM-15


### C20 — Malformed standards citations (documentation-§6)

Citations use the retired global §N numbering, dotted or space forms, literal escape bytes, or line numbers such as packaging.md:28. The vendored kit's own case names spell citations without §, and those render into the generated test-cases.md (upstream). Affects AbsorbTracker, BankLedger, ConsumableMaster, KickCD, LootHistory, MultiMeters, PartyFrameEnhanced and WhatGroup.

**AbsorbTracker**

- **AbsorbTracker-A-17** `low` (audit AT-79; corrected · upstream → LibKa0s) — Malformed and non-canonical standard citations (localization-5, packaging.md:28, lint.md), including the kit's own case names  
  *Where:* tests/prose_waivers.lua:3, tests/prose_waivers.lua:7, tests/test_docs.lua:194, docs/module-map.md:852, .pkgmeta:17, .pkgmeta:20, .pkgmeta:21, .luacheckrc:9, .luacheckrc:14, .luacheckrc:78, docs/test-cases.md (kit case names localization-5, line-endings-5, layout-1)  
  *Evidence:* 'localization-5' does not parse as filename-§N, which is a MUST. 'packaging.md:28' and 'lint.md' are not canonical bare-filename citations (SHOULD). The kit's test_prose.lua, test_eol.lua and test_layout_cap.lua emit case names spelled localization-5, line-endings-5 and layout-1, which docs/test-cases.md inherits. The retired §N.M sweep finds 0 and nothing is out of range.  
  *Remediation:* Addon half (C9/S1.4): respell as localization-§5 in prose_waivers.lua, test_docs.lua and module-map.md, and as the bare 'packaging' and 'lint' in .pkgmeta and .luacheckrc (comments only), after confirming the addon's prose/ASCII scan tolerates § in those files. Kit half (A3/S0.2, LibKa0s): do not hand-type § into kit string literals. Either build the section sign from bytes (string.char(194,167)), as test_eol.lua:421-424 already does for its delimiter, in the case names and KIT_GATE_RULE, or amend the library's ASCII gate or documentation-§6 to admit an ASCII citation form in string literals (a WowAddonStandards decision). Then bump the kit revision, re-vendor, and regenerate docs/test-cases.md (S3.1).  
  *Rule:* documentation-§6  
  *Planned in:* LK-08, AT-21

**BankLedger**

- **BankLedger-A-15** `low` (audit BL-50; confirmed) — .pkgmeta cites the standard as 'packaging.md:28', a line number that has already moved  
  *Where:* .pkgmeta:17,22  
  *Evidence:* packaging has no numbered subsections and is cited bare. The strong-form MUST is not on line 28 of the v2.64.0 file. Fails a SHOULD.  
  *Remediation:* S5-5: cite 'packaging' (its strong-form ignore rule) bare. Comment only.  
  *Rule:* documentation-§6 (Citing the standard)  
  *Planned in:* BL-20

**ConsumableMaster**

- **ConsumableMaster-A-15** `low` (audit CM-75; confirmed) — 46 bare §N citations in 22 files (the SHOULD half of documentation-§6)  
  *Where:* settings/General.lua:346, 377; tests/test_settingsui_optionsui.lua:5, 71, 721, 723; settings/Slash.lua:85; others per 03_EVIDENCE E12  
  *Evidence:* Up from 24 in 12 files on 2026-09-08. Most continue a full filename-§N in the same clause. Of the 672 full citations, 0 are out of range and 0 malformed, and there are 0 retired dotted forms.  
  *Remediation:* B8 / S4-7: expand each bare citation to its full filename-§N, using the E12 command to find them. Leave the smoke-tests.md §N numbering and Selector.lua's TECHNICAL_DESIGN §4 alone.  
  *Rule:* documentation-§6  
  *Planned in:* CM-27

**KickCD**

- **KICKCD-A-15** `low` (audit KICKCD-C-15; corrected) — Eight bare §N citations use the retired global numbering  
  *Where:* core/Compat.lua:245, modules/IconGrid.lua:1207, settings/Panel.lua:179, tests/test_compat_api.lua:4, tests/test_debuglog.lua:108, tests/test_debuglog.lua:115, tests/test_debuglog.lua:124, tests/test_settings_log.lua:1, docs/test-cases.md:403-405  
  *Evidence:* Hits include '(§11)', '(§9)', 'standard §10' and '(§10)' naming no file. filename-§N is the only cross-reference form.  
  *Remediation:* Qualify every bare §N. core/Compat.lua:245 and tests/test_compat_api.lua:4 become 'compat'. IconGrid.lua:1207 becomes debug-logging-§9. Panel.lua:179 and test_settings_log.lua:1 become debug-logging-§10. test_debuglog.lua:108/115/124/128 become debug-logging-§11. Panel.lua:187 gets the correct qualified section: check whether it means debug-logging-§4 or the performance zero-alloc rule. Also qualify the same-comment back-references at IconGrid.lua:850/866 and Panel.lua:306. Rename the three test_debuglog titles, regenerate docs/test-cases.md via --list, and check the badge count in the same commit.  
  *Rule:* STANDARDS.md 'Reading this document'; documentation-§5  
  *Planned in:* KC-22

**LootHistory**

- **LootHistory-A-10** `low` (audit LH-67; confirmed) — Unresolvable standard citations: disabled-§7 test names and packaging.md:28 in .pkgmeta  
  *Where:* tests/test_disabled.lua:174-516, docs/test-cases.md, .pkgmeta:14, .pkgmeta:19, .pkgmeta:20  
  *Evidence:* 12 test names cite disabled-§7 or disabled-§7.N, but there is no disabled section file, and 11 of them use the retired dotted form. docs/test-cases.md mirrors them. .pkgmeta cites packaging.md:28, a line number into a file with no numbered subsections whose line 28 no longer carries the rule.  
  *Remediation:* Rename the cases to 'slash-commands-§7 step N: ...' and regenerate docs/test-cases.md (the count stays 858). Cite 'packaging' (bare filename) in .pkgmeta. Re-run the sweep: 0 disabled-§ hits, 0 dotted §N.M hits.  
  *Rule:* documentation-§6 (MUST malformed + SHOULD form)  
  *Planned in:* LH-24

**MultiMeters**

- **MultiMeters-A-23** `low` (audit MM-A-23; confirmed) — 57 citations do not parse as filename-§N (space form, §-less form, literal \194\167 in comments), including a register Rule cell  
  *Where:* docs/ARCHITECTURE.md:519; docs/ARCHITECTURE.md:671; docs/ARCHITECTURE.md:679; tests/test_texture_paths.lua:48; core/LifecycleSetup.lua (x8); modules/Export.lua (x1); tests/prose_waivers.lua (x2); tests/test_disabled.lua (x7); core/MultiMeters.lua:135 and 34 more lines in 18 files  
  *Evidence:* 4 'library-stack §8' forms, with COLUMNBLOCKS_RULE pinning the form. 18 §-less forms (slash-commands-7 etc.). 35 comment lines contain the literal '\194\167'. The 2 retired dotted hits are in a frozen plan and are not filed.  
  *Remediation:* Run one mechanical sweep: library-stack-§8 (move test_texture_paths.lua:48 in the same commit), add § to the 18 §-less forms, and use a raw § in the 35 comment lines. Re-run the three greps and expect 0 each.  
  *Rule:* documentation-§6; documentation-§3  
  *Planned in:* MM-26

**PartyFrameEnhanced**

- **PartyFrameEnhanced-A-18** `info` (audit PFE-08; confirmed) — The retired-notation sweep finds 18 dotted-section hits, all citing the addon's own design spec  
  *Where:* repo-wide (the design spec and its citations, e.g. 'spec §6.4')  
  *Evidence:* `grep -rEn '§[0-9]+\.[0-9]'` → 18 hits, none citing the standard. Range check: 271 citations, 0 out of range, 0 malformed.  
  *Remediation:* None required; 'design spec §6.4' is already the house form.  
  *Rule:* documentation-§6  
  *Planned in:* PF-DOCS

**WhatGroup**

- **WHATGROUP-A-12** `low` (audit WG-73; confirmed) — Five malformed standards citations in authored files  
  *Where:* core/LauncherSetup.lua:143, tests/prose_waivers.lua:2, tests/prose_waivers.lua:4, tests/run.lua:140, tests/run.lua:145  
  *Evidence:* 'slash-commands-@7' (typo), 'localization-5' x3, 'layout-1' — none parses as filename-§N; four copy the kit's ASCII spelling (WG-74). Overlaps review F-009's LauncherSetup.lua:143 item.  
  *Remediation:* Fix to slash-commands-§7, localization-§5 (x3), layout-§1; re-run the §F sweep to 0 authored hits.  
  *Rule:* documentation-§6 (MUST)  
  *Planned in:* WG-21
- **WHATGROUP-A-13** `low` (audit WG-74; confirmed · upstream → LibKa0s) — Vendored test kit spells citations without § (74 lines) and they render into generated docs/test-cases.md  
  *Where:* tests/_kit/test_prose.lua (35), tests/_kit/test_eol.lua (25), tests/_kit/test_layout_cap.lua (9), tests/_kit/framework.lua (5); docs/test-cases.md:784, 788, 789, 808  
  *Evidence:* Kit case names/comments write localization-5, line-endings-5, layout-1, testing-12; --list renders four into this repo's tracked generated inventory, which cannot be hand-edited.  
  *Remediation:* Upstream in LibKa0s/testkit: spell as localization-§5, line-endings-§5, layout-§1, testing-§12 (or build § at runtime from "\194\167" / record an ASCII exception in kit README and documentation-§6); land in one kit revision, bump kit revision, tag. Then whole-folder re-vendor and regenerate docs/test-cases.md (all consumer addons' inventories move).  
  *Rule:* documentation-§6 (MUST); testing-§1  
  *Planned in:* LK-08, WG-21, WG-DOCS
- **WHATGROUP-R-09** `low` (review F-009; confirmed) — Numeric counts in comments disagree with each other and the code (rows, addons) plus a malformed §7 citation  
  *Where:* settings/Schema.lua:5, settings/Schema.lua:104, settings/Schema.lua:125, settings/Schema.lua:589, settings/Panel.lua:192, settings/Panel.lua:284, settings/Panel.lua:313, defaults/Profile.lua:15, defaults/Profile.lua:25, core/LauncherSetup.lua:143  
  *Evidence:* Master-controls block is 8 rows (19 schema rows total) but comments say seven, nine, eight, six; collection is ten addons but comments say nine and eleven; LauncherSetup.lua:143 cites 'slash-commands-@7' (same site as audit WG-73).  
  *Remediation:* C-007: replace numeric 'N addons'/'N rows' with non-numeric phrasing ('every Ka0s addon', 'the composed block'); fix core/LauncherSetup.lua:143 to slash-commands-§7 (coordinate with WG-73).  
  *Rule:* documentation; documentation-§6  
  *Planned in:* WG-21


### C21 — Doc prose and file:line drift in ARCHITECTURE/docs

Stated inventories, counts, load order and file:line citations in ARCHITECTURE.md and other docs no longer match the tree after recent peels and adoptions. The root cause is the same in every repo: counts and line anchors are maintained by hand. Affects AuraMaster, BankLedger, ConsumableMaster, KickCD, LibKa0s, LootHistory, MultiMeters, PanelMaster, PartyFrameEnhanced, PrettyChat and WhatGroup.

**LibKa0s**

- **LibKa0s-A-08** `low` (audit LK-29; confirmed) — Hand-maintained figures in root CLAUDE.md disagree with the tree  
  *Where:* CLAUDE.md:268-269; CLAUDE.md:203; CLAUDE.md:180; CLAUDE.md:185-218  
  *Evidence:* (a) lint scope 'eighty files' vs luacheck 81 (DEPENDENCIES.md:124 and releasing.md:19 already say 81); (b) tests/test_schema.lua recorded 1101, actually 1233 (RESULTS.md:164); (c) cites OptionsTabs.lua:39 (blank) for __tabsMinor/__tabsShellMinor guard at :43-46. Recurs.  
  *Remediation:* One commit: (a) 81, or better point at RESULTS.md's generated lint sentence; (b) 1233 after re-running the band wc -l command and re-checking all band figures in :185-218; (c) cite lib.__tabsMinor / lib.__tabsShellMinor by symbol. Close-out: luacheck file count must agree with every prose copy.  
  *Rule:* documentation-§5; lint  
  *Planned in:* LK-30

**AuraMaster**

- **AuraMaster-A-04** `low` (audit AM-07; confirmed) — Five docs/ARCHITECTURE.md file:line citations point at the wrong line (recurs); docs/testing.md -j claim stale  
  *Where:* docs/ARCHITECTURE.md (citations of settings/Schema.lua:377->:460, modules/ContainerManager.lua:520->:535, :543->:545, settings/OptionsSetup.lua:380->:396, modules/Style.lua:823-825->:826-828); docs/testing.md:16-19  
  *Evidence:* E-15: 5 of 35 distinct citations are wrong. docs/testing.md says -j auto applies 'if the serial suite ever passes about ten seconds', but the serial suite runs 174 s (that fix belongs to AM-27).  
  *Remediation:* Run one citation sweep over docs/ and the root docs (together with F-012 and AM-08). Strengthen the docs gate (issue #6's successor) to check each citation's symbol and text, not only that the line exists; at minimum, report citations landing on a comment or blank line.  
  *Rule:* documentation-§5  
  *Planned in:* AM-34
- **AuraMaster-A-13** `low` (audit AM-33; confirmed) — LibDBIcon's minimapPos isn't named as named non-setting state in the hub  
  *Where:* docs/ARCHITECTURE.md:216; docs/schema.md:39  
  *Evidence:* The hub says 'two pieces of named non-setting state' (timedSpells, AuraMasterPerfDB). global.minimap.minimapPos, written by LibDBIcon, is the same class of state. schema.md names the key but gives no owner module.  
  *Remediation:* Add a third bullet: storage key global.minimap.minimapPos, owner core/LauncherSetup.lua, writer LibDBIcon-1.0 (the player dragging the button), no addon writer. Change 'two pieces' to 'three'.  
  *Rule:* architecture-§5; documentation-§3 (Settings Schema)  
  *Planned in:* AM-30
- **AuraMaster-R-12** `low` (review F-012; confirmed) — Stale citations in docs/performance.md and a README 0.1.0 row that misdescribes the addon  
  *Where:* docs/performance.md:51; docs/performance.md:55; README.md:156  
  *Evidence:* performance.md:51 cites core/AuraMaster.lua:98 for unitSwap; the bracket is at :115. performance.md:55 cites modules/Style.lua:772-780; Style.Element is at :774-784. README.md:156 says 'buff, debuff and weapon enchant containers ... bars or icons ... preview mode'. But the weapon-enchant aura type was retired in schema v5, the text style exists, and the UI calls it Test mode. This is the same citation-drift class as AM-07.  
  *Remediation:* C-12: change :98 to :115 and 772-780 to 774-784. Reword the README 0.1.0 history row only to fix the inaccuracy: bars, icons or text; weapon enchants as a buff category; test mode. Fold into the AM-07 citation sweep.  
  *Rule:* documentation-§5  
  *Planned in:* AM-34

**BankLedger**

- **BankLedger-R-06** `low` (both F-007, BL-45; confirmed) — Stale file:line citations and prose across ARCHITECTURE (register rows, Event Subscriptions), performance.md, Schema.lua, Panel.lua, Database.lua and test_schema.lua  
  *Where:* docs/ARCHITECTURE.md:378,379,384,501,504; docs/performance.md:46; settings/Schema.lua:139,178,396-403; tests/test_schema.lua:278; settings/Panel.lua:767; core/Database.lua:579-581  
  *Evidence:* The ARCHITECTURE:378/379 citations are BankLedger.lua:45 and :49-50, but the lines are now :87 and :91-92. ARCHITECTURE:384 cites Browser:1206, now :1218, and wrongly says 'each window's own event frame' where it means a private bus target. ARCHITECTURE:504 cites the factory at :98 (now :95), NS.Icon at :104 (now :101) and the caller at :1047 (now :1056). The ARCHITECTURE:501 perf row's Why says three combat events only nil-check, but the combat pair also runs ApplyVisibility. docs/performance.md:46 says OnEnable where the code has NS.StandUp. Schema.lua:139 cites Browser :1123/:1165, now :1132/:1179. Schema.lua:178 and test_schema:278 cite SetMovable at :1007, now :1016. Schema.lua:396-401 has shifted Browser lines. Schema.lua:402-403 names the deleted B:SetupMinimap, now core/LauncherSetup.lua. Panel.lua:767 says 'two host-drawn filter tabs' where there is one Filters tab. Database.lua:581 cites test_ledger:572, but DeleteAt is at :564.  
  *Remediation:* C-05 / S5-4: correct each site in one sweep, done after the BL-43 spill so citations are fixed where they end up. Where a line number has rotted, cite the symbol instead (NS.StandUp, B:Enable, B:MakeCloseButton, B:SaveGeometry, the 'undo a recorded row' test). Replace B:SetupMinimap with core/LauncherSetup.lua. Rewrite the performance-§12 row's Why to point at the docs/performance.md table (five events can fire in combat). Fix performance.md:46 (NS.StandUp) and Panel.lua:767 (one Filters tab). Comment and doc only. Smoke desk check C-05.  
  *Rule:* documentation-§5 (keep doc set in sync with code); audit-review-history (register evidence must resolve)  
  *Planned in:* BL-20
- **BankLedger-A-09** `low` (audit BL-38; confirmed) — Seven lines in six files still say the host close factory serves four title bars; it serves three (the copy window is the library's) (recurs, narrowed)  
  *Where:* core/MediaSetup.lua:86; docs/media.md:46; docs/smoke-tests.md:597-599; tests/test_libka0s.lua:63; tests/test_marks.lua:71,98; docs/test-cases.md:941  
  *Evidence:* The register row and core/CoreSetup.lua:117-131 now say three. The smoke step tells testers the copy window's close goes through B:MakeCloseButton, which it does not.  
  *Remediation:* S5-3: change four to three at each site and name the copy window as LibKa0s-Widgets-1.0's CopyWindow. Split the docs/media.md:46 cell: the close mark is on four windows, the factory on three. Rewrite the smoke step to check the copy window separately. Rename the test_marks:98 case and regenerate docs/test-cases.md. Re-run the census grep and expect no output.  
  *Rule:* documentation-§5; standalone-windows  
  *Planned in:* BL-20

**ConsumableMaster**

- **ConsumableMaster-A-12** `low` (both CM-94 + F-015 (TOC 'second' comment); corrected) — Load-order statements in the docs and a TOC comment are wrong since core/LifecycleSetup.lua took the second line of # Core  
  *Where:* docs/ARCHITECTURE.md:324; docs/ARCHITECTURE.md:418; docs/module-map.md:598; docs/module-map.md:642; docs/performance.md:46; ConsumableMaster.toc:76-77  
  *Evidence:* The docs list Namespace -> PerfSetup with no LifecycleSetup, and module-map omits LauncherSetup. The docs and the TOC say PerfSetup 'sits second', but it is third. ARCHITECTURE.md:418 cites TOC line numbers that now hold other comments. The review's F-015 flags the same 'It sits here, second' TOC comment.  
  *Remediation:* Fix all seven statements: the six cited plus docs/module-map.md:38. Replace the ordinals with 'after core/LifecycleSetup.lua'. Add LifecycleSetup and LauncherSetup to the load-order chains. Cite TOC comments by what they annotate, not by line number. In the TOC, edit only the comment text, with no line moves (anti-pattern #66).  
  *Rule:* documentation-§5; anti-pattern #66  
  *Planned in:* CM-24
- **ConsumableMaster-R-14** `low` (review F-014; corrected) — A comment and a doc claim /cm set macroBar.point\|x\|y repositions the bar; no such schema row exists  
  *Where:* modules/MacroBar.lua:175; docs/ARCHITECTURE.md:340; docs/ARCHITECTURE.md:130  
  *Evidence:* settings/MacroBar.lua declares no position row. The doc sends a player on a degraded install to a verb that refuses.  
  *Remediation:* C-13: correct modules/MacroBar.lua:175 and docs/ARCHITECTURE.md:340 so they say the position is set only by dragging or by a reset (/cm bar reset, Reset position), and /cm set cannot reach it. Leave docs/ARCHITECTURE.md:130 as it is; it is already correct.  
  *Rule:* documentation-§5  
  *Planned in:* CM-23

**KickCD**

- **KICKCD-A-11** `low` (audit KICKCD-C-08; confirmed) — Six stated inventories or cross-file line citations no longer match the tree  
  *Where:* docs/ARCHITECTURE.md:77-81, .luacheckrc:24-28, docs/ARCHITECTURE.md:352, docs/ARCHITECTURE.md:353, docs/ARCHITECTURE.md:281, core/LifecycleSetup.lua:113, .luacheckrc:89, .pkgmeta:17, .pkgmeta:20, .pkgmeta:21  
  *Evidence:* 1. 'Five' files read addonName; the tree has 8 (and 30 write _). 2. The compat trigger says '496 lines'; the file is 485, and the trigger should count shims (8). 3. The message-bus row states no trigger (5 messages). 4. 'Five subscriptions' for Spells; there are 7. 5. .luacheckrc cites tests/run.lua:217; the global is at :299. 6. .pkgmeta cites packaging.md:28, now a template comment.  
  *Remediation:* D6/Sprint 4.4: re-derive every figure with a command recorded in the commit message (8/30 files, 8 shims, 5 messages with trigger not fired, 7 registrations). Replace cross-file line citations with symbols or section ids (e.g. 'KICKCD_TEST = Kit.expose', 'packaging'). Do this after the code sprints so the docs describe the final tree.  
  *Rule:* documentation-§5; packaging  
  *Planned in:* KC-26
- **KICKCD-R-09** `low` (review F-009; corrected) — docs/performance.md's bucket table does not match the Perf descriptor, and spellState runs outside its declared stateEmit parent on the Rebuild path  
  *Where:* docs/performance.md:36-55, core/PerfSetup.lua:100-101, core/PerfSetup.lua:105, modules/IconGrid.lua:994, modules/Cooldowns.lua:339  
  *Evidence:* performance.md says spellState sits within spellPoll, omits stateEmit, and says glowGate is 'deliberately not declared'. PerfSetup declares stateEmit within spellPoll, spellState within stateEmit, and glowGate. The Rebuild emit at Cooldowns.lua:339 is not bracketed as stateEmit, and Perf.Note('spellState') at IconGrid.lua:994 passes no parent. The committed captures (20260909-014035) predate the current nesting.  
  *Remediation:* Fix the Rebuild path so the declared nesting is true at every level. Either (a) bracket Rebuild's emit under its own undeclared or root bucket (e.g. 'rebuildEmit', no within) and have IconGrid:OnSpellState pass its observed parent to Perf.Note, so LibKa0s-Perf reports observedMixed honestly, or (b) drop stateEmit's 'within = spellPoll' and state in PerfSetup that stateEmit has two callers. Then regenerate the docs/performance.md bucket table from the PerfSetup descriptor, including stateEmit and glowGate and removing the 'glowGate not declared' paragraph. Add a test_perfsetup case asserting every spellState note happens under an open stateEmit and that stateEmit's observed parent matches its declaration. Re-run tests/perf.lua. The in-game two-arm capture via /wow-addon:perf-analysis stays as the smoke step.  
  *Rule:* performance-§3; performance-§8  
  *Planned in:* KC-14

**LootHistory**

- **LootHistory-R-11** `low` (review F-011; confirmed) — Two stale line citations in docs/midnight-quirks.md  
  *Where:* docs/midnight-quirks.md:9, docs/midnight-quirks.md:64  
  *Evidence:* :9 cites C_TooltipInfo.GetHyperlink (:226), but it is at core/Compat.lua:234-235. :64 cites Compat.GetMailHeader (:90-96), but it is at :98-104.  
  *Remediation:* C-010: re-point :9 to :234 and :64 to :98-104.  
  *Rule:* documentation-§7  
  *Planned in:* LH-28

**MultiMeters**

- **MultiMeters-A-24** `low` (audit MM-A-24; confirmed) — The hub's inventory line says 57 files / 18 core, but the tree and module-map.md say 58 / 19  
  *Where:* docs/ARCHITECTURE.md:14; docs/ARCHITECTURE.md:45; docs/module-map.md:6  
  *Evidence:* git ls-files counts 58 files, 19 under core/. The hub contradicts itself at :45.  
  *Remediation:* Correct :14 to 58 / 19 core/. Optionally add a test_doc_structure case that derives the counts from git ls-files.  
  *Rule:* documentation-§5  
  *Planned in:* MM-29
- **MultiMeters-R-15** `info` (review F-015; corrected) — docs/performance.md quotes a feign figure (71224.1) that the runner no longer produces (71544.1)  
  *Where:* docs/performance.md:289  
  *Evidence:* Today's tests/perf.lua gives feignTraceAbsent and feignTraceOff at 71544.1 each.  
  *Remediation:* C-12: keep the historical sentence and label it as the closing run's figures. If a current figure is wanted, re-run tests/perf.lua in the commit and add today's printed value (71544.1 for both arms as of 2026-09-23) as a separate, dated statement that keeps the arm-equality claim. Do not overwrite one number inside the before/after pair.  
  *Planned in:* MM-29

**PanelMaster**

- **PanelMaster-A-12** `low` (audit PM-044; confirmed) — Stale inventory counts and code comments in the docs and in PanelEditor.lua  
  *Where:* docs/ARCHITECTURE.md:21-24, docs/ARCHITECTURE.md:339, docs/testing.md:106, docs/testing.md:340-351, docs/module-map.md:69-70, settings/PanelEditor.lua:178-190, settings/PanelEditor.lua:1191-1223, .gitignore:6  
  *Evidence:* - ARCHITECTURE says 'six of eight seams'; there are nine. - testing.md says 'nine of ten majors resolve Core'; it is fourteen of fifteen. - testing.md says 'four seams adopted'; nine are adopted, with six parity cases (seven after A-08). - module-map says 'other nine'; it should say fourteen. - ARCHITECTURE:339 calls RESULTS.md 'never hand-edited', but its Disposition column is authored. - PanelEditor comments say 'General is GONE', 'THREE EXPLICIT ROWS' and refreshHeaderActs, all of which are stale. - .gitignore:6 cites a nonexistent tools/artwork/wiki_import.py.  
  *Remediation:* Do a single sweep, recounting with grep -c rather than by hand. Restate seven parity cases after A-08 lands. Rewrite the PanelEditor comment blocks: General is back and first, the band is one row, and refreshHeaderActs is gone. Keep the PanelEditor edit net-neutral given the 1500-line cap. Drop the wiki_import.py reference in .gitignore, or re-point it at the actual script.  
  *Rule:* documentation-§5  
  *Planned in:* PM-22

**PartyFrameEnhanced**

- **PartyFrameEnhanced-A-06** `low` (audit PFE-15a; corrected) — scope.md and ARCHITECTURE.md say the addon only reads other addons' frame position and unit, but it also reads EllesmereUIDB (derived from PFE-15)  
  *Where:* docs/scope.md:24-26; docs/ARCHITECTURE.md:248-249  
  *Evidence:* 'it only reads their position and unit, and only through hooksecurefunc / HookScript.' Providers.lua:293 reads EllesmereUIDB.  
  *Remediation:* Correct docs/scope.md:24-26 to match the PFE-15 decision. If the read stays, name the EllesmereUIDB size read there. ARCHITECTURE.md needs a change only if option (a) removes the read: the Taint Notes sentence at :251-254 then has to go. If option (b) is chosen, add the register row there.  
  *Rule:* documentation-§5  
  *Planned in:* PF-22
- **PartyFrameEnhanced-A-10** `low` (audit PFE-19; confirmed) — The Message Bus table leaves Preview out as a consumer of CONFIG and PROFILE  
  *Where:* docs/ARCHITECTURE.md:107, :109; modules/Preview.lua:161, :170  
  *Evidence:* Preview registers NS.MSG.CONFIG and NS.MSG.PROFILE, but neither row's Consumers cell names it.  
  *Remediation:* Audit Sprint 4.3: add Preview to both cells. Optional: a tests/test_bus.lua case that derives consumers from source so the table cannot drift again.  
  *Rule:* architecture-§4  
  *Planned in:* PF-23
- **PartyFrameEnhanced-A-12** `low` (audit PFE-01; corrected) — The doc set lags the code at seven sites (recurring, with new content)  
  *Where:* CLAUDE.md:33; docs/ARCHITECTURE.md:3-6, :140, :324; docs/module-map.md:17; docs/compat-layer.md:4, :16, :22; defaults/Profile.lua:4  
  *Evidence:* The resume pointer still names the v0.1.0 build ledger. module-map lists a `test` field that State.lua no longer has. Blank lines break the compat-layer table. ARCHITECTURE says '15 shims' where the grep counts 14. compat-layer.md:4 says feature modules 'never' call raw APIs, but CastBars:216, RangeFade:116 and TargetFrames:81 do. The right-click rationale cites v2.56.0's 'narrows the slash surface'. The defaults header mentions 'the phase that builds each feature'.  
  *Remediation:* Audit Sprint 4.5: one sync-docs pass, done last after the code changes. Repoint the resume pointer in CLAUDE.md:33 and ARCHITECTURE.md:3-6. Drop `test` from module-map.md:17. Rejoin the compat-layer.md table by removing the blank lines at :16 and :22. Soften 'never' at compat-layer.md:4 so it matches the raw calls at CastBars:216, RangeFade:116 and TargetFrames:81, or route those through Compat. Restate the right-click rationale at ARCHITECTURE.md:140 per v2.57.0: the panel is setup, reachable in either state. Rewrite the defaults/Profile.lua:4 header. KEEP '15 shims' at ARCHITECTURE.md:324. It is correct: 14 function statements plus the Compat.IsSecret assignment. Optionally add the grep that counts both forms.  
  *Rule:* documentation-§5  
  *Planned in:* PF-23
- **PartyFrameEnhanced-R-12** `low` (review F-009; confirmed) — docs/performance.md figures are stale, and settingsDrag grew by about 50% without anyone noticing  
  *Where:* docs/performance.md (scenario table, 'Figures from' line); tests/perf.lua:243-258 (comments)  
  *Evidence:* The doc says castStartStop 16.6 B/iter; measured today 5.4. The doc says settingsDrag 596 B/iter; measured today 895.9 (bundle 885.9). Probably caused by structureSignature (modules/Element.lua:168-176) gaining three marker fields. settingsDrag has no assertion.  
  *Remediation:* C-006 / T-7, after T-6: re-run tests/perf.lua and copy the figures into docs/performance.md in the same change, explain the settingsDrag growth, and update the perf.lua comment text without changing any ceiling. Never hand-edit a number that was not just measured.  
  *Rule:* performance-§9, testing-§5  
  *Planned in:* PF-19

**PrettyChat**

- **PRETTYCHAT-A-10** `low` (audit PC-86 (PRETTYCHAT-C-07); corrected) — Doc set drifted from code in eight places  
  *Where:* docs/ARCHITECTURE.md:71, docs/module-map.md:240, docs/settings-panel.md:61, docs/smoke-tests.md:898, docs/ARCHITECTURE.md:33, docs/ARCHITECTURE.md:147, settings/Slash.lua:243, core/Constants.lua:24-25, settings/Slash.lua:405-408, docs/scope.md:45, .pkgmeta:21, .pkgmeta:25, docs/ARCHITECTURE.md:193  
  *Evidence:* The eight drift items: 1. A General-page explainer TextRow and an afterGroup Test button are still described, but both were removed in 8be34c6. 2. The load order omits core/LifecycleSetup. 3. Slash is cited as minor 13; the vendored minor is 14. 4. The STRING_VSPACER comment says 'bespoke 40/60 editor'. 5. A stale IsAddonEnabled 'second reader' comment. 6. scope.md lists a deleted doc index. 7. .pkgmeta cites packaging.md:28 by line number. 8. ARCHITECTURE.md:193 puts all of docs/automated-tests/ out of scope, when the standard only excludes docs/automated-tests/<run>/.  
  *Remediation:* Fix items 1-5 and 7 only. Rewrite the General-page description in ARCHITECTURE.md:71, module-map.md:240, settings-panel.md:61 and smoke-tests.md:898 as RenderTabbedSchema over Master controls, with the composer's Test leadButton and Reset pair. Add core/LifecycleSetup to the ARCHITECTURE.md:33 load order, in TOC position. Change ARCHITECTURE.md:147 to Slash minor 14. Drop '40/60' from core/Constants.lua:24-25. Reword settings/Slash.lua:405-408 so it no longer counts readers. Change the two .pkgmeta citations to 'packaging-§1' (no line number). Leave scope.md:45 and ARCHITECTURE.md:193 unchanged. Optionally add the test_doc_structure check that the ARCHITECTURE load order matches the TOC file list.  
  *Rule:* documentation-§5; documentation-§6  
  *Planned in:* PC-20

**WhatGroup**

- **WHATGROUP-A-16** `low` (audit WG-77; confirmed) — Docs and comments have drifted from the tree (eight sites)  
  *Where:* README.md:41, README.md:48, docs/ARCHITECTURE.md:19, docs/module-map.md:68, docs/ARCHITECTURE.md:55, docs/ARCHITECTURE.md:319, docs/ARCHITECTURE.md:383, docs/ARCHITECTURE.md:502, core/MediaSetup.lua:33-34  
  *Evidence:* README says both windows' positions persist (console's does not, issue #11); ARCHITECTURE/module-map say FIFO queue (removed; keyed by searchResultID); 'eight seams' vs nine; :319 degrading seams list incomplete and 'other three' miscounts; :383 LibKa0s.xml lists 16 files vs 21; :502 references retired 'row above'; MediaSetup comment references removed footer mark.  
  *Remediation:* Correct each: README 'the place you dragged the popup to' (de-AI pass per documentation-§1); FIFO -> 'keyed by search-result id'; eight -> nine; list every degrading seam and fix the count; say 'the 21 files LibKa0s.xml lists' rather than enumerating; drop 'row above' references at :502; fix MediaSetup comment (footer mark removed, NS.Icon has no caller).  
  *Rule:* documentation-§5 (MUST); documentation-§1  
  *Planned in:* WG-25


### C22 — Stale or misplaced code comments

Source comments describe removed behaviour (draw gates, printers, load order, taint rules), sit above the wrong function, or narrate review history. The fixes are comment-only, per file, in AbsorbTracker, AuraMaster, ConsumableMaster, KickCD, LootHistory, MultiMeters, PanelMaster, PrettyChat and WhatGroup.

**AbsorbTracker**

- **AbsorbTracker-R-05** `medium` (both F-005; AT-80 item (6); confirmed) — The comment on /at enable and /at disable describes the removed draw gate ('gates ShouldShowBar's second rung... no event registration changes')  
  *Where:* settings/Slash.lua:292-309, settings/Slash.lua:300, settings/General.lua:145, core/Lifecycle.lua:79-106, modules/Display.lua:327  
  *Evidence:* The comment says onChange runs VISIBILITY then REPAINT and that enabled gates only the second rung. In fact onChange is NS.SyncEnabledHold(), which moves the lifecycle 'disabled' hold, StandDown unregisters every event, frame and bus registration, and rung 0 asks the latch. The comment misstates the §7 invariant at its entry point (anti-pattern #85).  
  *Remediation:* C-05 (and C10 row): rewrite the comment. The enabled row's onChange moves the latch's disabled hold; StandDown unregisters everything; the dispatcher, config, help and bare /at stay live (slash-commands-§2/§7).  
  *Rule:* slash-commands-§7, anti-pattern #85, documentation-§5  
  *Planned in:* AT-04
- **AbsorbTracker-R-07** `low` (both F-007; AT-80; confirmed) — Doc and comment drift against code: stale load-order, file-count, test-mode, version, line-count, throttle and misplaced comments  
  *Where:* settings/General.lua:14-27, settings/General.lua:21, settings/General.lua:38-43, settings/General.lua:73-80, settings/General.lua:209-210, settings/General.lua:308-309, core/PerfSetup.lua:11-13, core/CoreSetup.lua:12-14, core/AbsorbTracker.lua:114-117, defaults/Profile.lua:145, core/Constants.lua:56-77, docs/ARCHITECTURE.md:30-34, docs/ARCHITECTURE.md:74, docs/ARCHITECTURE.md:570, docs/ARCHITECTURE.md:655, docs/ARCHITECTURE.md:728, docs/module-map.md:756, .luacheckrc:25-27, docs/settings-panel.md:68, locales/enUS.lua:16  
  *Evidence:* Review F-007 items: - General.lua still draws a [Test mode] row and says 'all nine rows', but the addon ships no Test mode row. - The console-path comment sits above unlockGuard, not above DEBUG_CONSOLE_PATH. - The appearancePass figure is stale: the comment says 384.5 bytes, today's run measures 97.8. - The throttle comment names GetSetting('throttleWindow'), but the code calls NS.GetThrottleWindow(). - PerfSetup and CoreSetup claim adjacency in the TOC, but Lifecycle sits between them. - AbsorbTracker.lua:114-117 says Suspend/Resume, which is now the latch's StandDown/StandUp. - defaults/Profile.lua:145 names settings/{Bar,Border,Font}.lua, now merged into Appearance.lua. - The MINIMAP_PATH comment is split from its constant by the BRAND block. - ARCHITECTURE.md:655 says v1.41.0 where :570 and enUS say v1.42.0.  Audit AT-80 adds: - ARCHITECTURE.md:30-34 says 6 and 20 files; the tree has 9 and 19. - module-map.md:756 omits Lifecycle.lua and LauncherSetup.lua. - .luacheckrc:25-27 lists CoreSetup among the binding files, but it opens local _, NS. - ARCHITECTURE.md:728 says 1415 lines; the file is 1416. - settings-panel.md:68 omits the Minimap button row.  Item (6), the enable comment, is tracked under R-05.  
  *Remediation:* C-06 and C10/S1.6: correct each site to match the code in one comment and doc sweep. - Redraw the General diagram without Test mode, adding [Minimap button]: 'seven rows plus the button pair'. - Move the console-path comment onto its constant. - Drop the byte figure and point at tests/perf.lua appearancePass instead. - Change the throttle reference to NS.GetThrottleWindow(). - Make the TOC order read CoreSetup → Lifecycle → PerfSetup ('loads after core/Lifecycle.lua, whose latch the descriptor carries'). - Say StandUp. - Say settings/Appearance.lua. - Move the MINIMAP_PATH comment next to its constant. - Settle the v1.41/v1.42 conflict via git log -S. - Change 'nine files bind addonName / nineteen' and name them. - Add Lifecycle and LauncherSetup to module-map. - Fix the .luacheckrc file list. - Measure the census count or drop it. - Add the minimap row to settings-panel.md.  Then run /wow-addon:sync-docs. Lint stays 0/0 and the suite does not change.  
  *Rule:* documentation-§5  
  *Planned in:* AT-22

**AuraMaster**

- **AuraMaster-R-11** `low` (review F-011; corrected) — Comment hygiene: fused/misplaced doc blocks, a merged 150-char line, and review-history narration in code  
  *Where:* core/Database.lua:478-538 (block at :508 above filterableCategories :539); core/Database.lua:521; modules/Container.lua:414-416  
  *Evidence:* Three functions' docs are fused above the wrong one (liftCategoryWhitelist, categoriesDecided, filterableCategories). Container.lua:414-415 merges two sentences. 'CORRECTION (review, after this shipped once already wrong)', 'fix round 3' and 'review round 2' narrate history instead of explaining why.  
  *Remediation:* Comment-only. Split core/Database.lua:478-538 into three doc comments, each directly above its function (liftCategoryWhitelist, categoriesDecided, filterableCategories). Rewrite :521's CORRECTION paragraph as a plain WHY. Re-wrap modules/Container.lua:414-416. Also strip the review/fix-round framing, keeping the reasoning, at modules/FilterCompiler.lua:38,45,56,76,81, modules/Container.lua:195,490, core/Database.lua:724 and core/Constants.lua:243.  
  *Rule:* documentation (comment hygiene)  
  *Planned in:* AM-27

**ConsumableMaster**

- **ConsumableMaster-R-15** `low` (review F-015; confirmed) — Stale comments that describe removed behavior (12 sites)  
  *Where:* defaults/Profile.lua:54, 107, 112; core/ConsumableMaster.lua:367-404; settings/Slash.lua:25, 271-305 (288-291); modules/Selector.lua:5, 604; ConsumableMaster.toc:50, 76, 81; settings/OptionsSetup.lua:159-165 (:160 vs :231)  
  *Evidence:* The comments describe: a recompute early-return (now a stand-down); frames being torn down (now hidden); every scalar having a schema row (false for point, relPoint, x, y); an orphaned restoreProfileDefaults block; KCM.Say's location; a gate covering both dispatch arms; nonexistent TECHNICAL_DESIGN and Core.lua references; a TOC list of five modules (fifteen majors ship); 'second' (it is third, overlapping CM-94); the retired suspend/resume pair; and contradictory statements about the row makers.  
  *Remediation:* C-13: correct each comment in place. Delete the orphaned restoreProfileDefaults block. Shrink the gate essay in settings/Slash.lua. TOC edits are prose only, with no line moves (anti-pattern #66).  
  *Rule:* anti-pattern #66; documentation-§5  
  *Planned in:* CM-23, CM-24

**KickCD**

- **KICKCD-R-12** `low` (review F-012; confirmed) — Four stale or wrong code comments  
  *Where:* core/KickCD.lua:13-19, core/KickCD.lua:23-27, modules/Cooldowns.lua:35-38, modules/Cooldowns.lua:648-650, core/Util.lua:101, settings/Spells.lua:1411  
  *Evidence:* - KickCD.lua:13-19 describes an _G.KickCD rebind, which :23-27 denies. - The Cooldowns comments describe master-enable recovery via a general rebuild, which the Lifecycle latch superseded. - Util.Throttle is called 'Leading-edge' but fires trailing. - Spells.lua:1411 ('precisely one thing') understates the disabled cost.  
  *Remediation:* C-10: rewrite the four comment blocks. Comment-only.  
  *Planned in:* KC-22

**LootHistory**

- **LootHistory-R-10** `low` (review F-010; confirmed) — Four stale or misplaced comments  
  *Where:* settings/Schema.lua:759-760, settings/Slash.lua:279, core/Util.lua:14, core/Util.lua:38  
  *Evidence:* Schema.lua:759-760 and Slash.lua:279 say Collector reads the enabled flag, but the reader is now NS.AddonIsOff (core/LifecycleSetup.lua:175-178). Util.lua:14's SplitPath comment sits above DeepCopy, and SplitPath is at :25. Util.lua:38 says 'MM/DD/YY', but the function does DD-MMM-YYYY.  
  *Remediation:* C-010: reword the Schema and Slash comments to name NS.AddonIsOff / the latch as the reader. Move the Util.lua:14 comment above SplitPath and delete the stale :38 line.  
  *Planned in:* LH-28

**MultiMeters**

- **MultiMeters-R-12** `low` (review F-012; confirmed) — Stale and misplaced comments on the show ladder, spell and system handlers, load order and launcher  
  *Where:* core/MultiMeters.lua:459-463; core/MultiMeters.lua:346-361; core/MultiMeters.lua:377; core/MultiMeters.lua:500; core/MultiMeters.lua:522; modules/Window_Placement.lua:202; modules/HeaderControls.lua:302; modules/HeaderControls.lua:372; core/LauncherSetup.lua:213-214  
  *Evidence:* The ShouldShow doc sits above fighting(). The OnSpellSucceeded doc is attached to OnSystemMessage. Ladder steps are numbered 0 then 2, and Window_Placement still points at the removed step 1. HeaderControls says settings/ loads ahead of modules/, but it loads last. The launcher comment claims Toggle writes 'shown'.  
  *Remediation:* C-09: move the doc blocks to their functions, renumber the ladder steps and fix Window_Placement:202, correct 'settings/ loads after modules/', and restate what Toggle does. Comments only.  
  *Planned in:* MM-25

**PanelMaster**

- **PanelMaster-R-09** `low` (review F-009; confirmed) — Comments and two docs are stale or wrong: printer location, AceConsole vs AceGUI, enabled announce, global contents, schema v1 example, and the PEW rationale  
  *Where:* core/PanelMaster.lua:10, core/CoreSetup.lua:17-18, settings/Slash.lua:292-293, defaults/Profile.lua:4-5, core/Database.lua:16, core/Database.lua:170, core/PanelMaster.lua:101-103, core/LifecycleSetup.lua:112-115, docs/ARCHITECTURE.md:228, docs/data-flow.md:200  
  *Evidence:* - NS.Print is built in core/CoreSetup.lua, not core/Util.lua. - The embed overwrites NS.Print with AceConsole's :Print, not AceGUI's. - The enabled row does not announce; its onChange is NS.RefreshEnabled(). - global does not carry only the stamp: Global.lua deliberately does not seed it and declares the minimap table. - The example [Init] line says schema v1, but SCHEMA_VERSION is 2. - Painting at PLAYER_ENTERING_WORLD is justified by 'recovery measures UIParent', yet recovery is on-demand only (modules/Registry.lua:854-858).  
  *Remediation:* Text-only rewrite of each sentence to the current mechanism (see the C-09 table). If tests/test_docs.lua pins any of these strings, update it in the same change. Coordinate with R-11 (PM-038a), which fixes the same global-stamp claim in docs/ARCHITECTURE.md:34 and docs/common-tasks.md.  
  *Rule:* documentation-§5  
  *Planned in:* PM-09, PM-10, PM-19

**PrettyChat**

- **PRETTYCHAT-R-04** `medium` (both F-006 (change C-06) + PC-87 (PRETTYCHAT-C-08); confirmed) — Stale user-facing text: Test tooltip says /pc test prints to chat (it writes to the debug console); resetall help row; three stale comments  
  *Where:* settings/Schema.lua:162, locales/enUS.lua, settings/Slash.lua:60, settings/Slash.lua:62, settings/Panel.lua:86-88, settings/Panel.lua:101-104, settings/Panel.lua:551-552, settings/Schema.lua:450-451  
  *Evidence:* Tooltip: '/pc test prints the same report to chat.' Since 8be34c6 (2026-09-16), /pc test routes through TestToConsole to the debug console. The resetall help row reads 'Reset every category to addon defaults', but it is a full profile reset that also resets General.enabled and visibility. Comments: Panel.lua:86-88 says /pc test still prints to chat; Panel.lua:551-552 says 'one SECONDARY tab per format string' (it is now a TreeGroup); Schema.lua:450-451 says 'pairs() order is non-deterministic' (untrue since PC-16). The audit grades the tooltip Medium (documentation-§5 MUST). The review grades the whole set Low.  
  *Remediation:* Reword the tooltip key and its enUS manifest entry together, e.g. 'Write a sample of every active format string to the debug console ... /pc test writes the same report there.' Change the resetall row to L['Reset every setting to defaults'] with its enUS key. Fix the three comments. Add a test (test_locale or test_panel) that fails if an L[...] key mentioning /pc test says 'chat' while runTest routes to TestToConsole.  
  *Rule:* documentation-§5; localization-§1; localization-§5; slash-commands-§4  
  *Planned in:* PC-10

**WhatGroup**

- **WHATGROUP-R-07** `low` (review F-007; confirmed) — Stale and contradictory comments in modules/Frame.lua (incl. misstated taint rule) and a stray argument  
  *Where:* modules/Frame.lua:194-206, modules/Frame.lua:748-751, modules/Frame.lua:385-402, modules/Frame.lua:1003-1005, modules/Frame.lua:608  
  *Evidence:* :199 says outOfCombat popup stays up; :205 says f:Show() is not a secure write (contradicted by :255-258 and test_frame.lua:1172); :748-751 zero Lua-side repeat contradicted by :366-369 and performance.md; four detached doc comments stacked above applyTeleportAction; :1003-1005 contradicted by :1006-1009; :608 stopCooldownTicker(self) passes arg to a zero-arg function.  
  *Remediation:* C-007: rewrite the outOfCombat bullet and delete :205-206 paragraph; restate :748-751 (swipe has no Lua repeat; point at performance.md ratified ticker deviation); move each doc block onto its function (deferTeleportUntilCombatEnds, resolveTeleportState, applyTeleportNote, applyTeleportAction); delete superseded :999-1005 paragraph; change :608 to stopCooldownTicker().  
  *Rule:* documentation (comments tell the truth)  
  *Planned in:* WG-21
- **WHATGROUP-R-08** `low` (review F-008; confirmed) — File headers name the wrong homes (slash dispatch, printer/SafeToString, Util seams)  
  *Where:* core/WhatGroup.lua:2, core/WhatGroup.lua:20, core/WhatGroup.lua:44, core/WhatGroup.lua:129, core/Util.lua:2, core/Util.lua:21-25, core/Util.lua:40  
  *Evidence:* WhatGroup.lua header still says slash dispatch (moved to settings/Slash.lua); attributes printer/SafeToString to Util.lua but they live in core/CoreSetup.lua; Util.lua calls NS.Windows 'the one low-level seam' while also defining NS.FormatDuration, and its Windows comment block is separated from the code.  
  *Remediation:* C-007: name settings/Slash.lua and core/CoreSetup.lua in the headers; fix Util.lua header to name both seams and move the Windows comment block above NS.Windows.  
  *Rule:* documentation  
  *Planned in:* WG-21


### C23 — README and DEPENDENCIES.md content

READMEs carry removed sections, placeholder screenshots, angle-bracket placeholders, jargon rows, an undisclosed default retention or wrong command claims, and Usage does not end on the configuration signpost. DEPENDENCIES.md has wrong citations, puts tools in the wrong groups or omits Python and Pillow, and a root CLAUDE.md has its sections out of order. Affects AuraMaster, BankLedger, ConsumableMaster, KickCD, LootHistory, PanelMaster, PrettyChat and WhatGroup.

**AuraMaster**

- **AuraMaster-A-05** `low` (audit AM-08 (derived from AM-07); confirmed) — DEPENDENCIES.md has three wrong file:line citations  
  *Where:* DEPENDENCIES.md (core/Constants.lua:25->:26 C.LOGO_PATH; core/Constants.lua:31->:32 C.LOGO_ICON_PATH; modules/ContainerManager.lua:568->:572 no-engine notice)  
  *Evidence:* E-15 resolver loop. Same cause as AM-07.  
  *Remediation:* Fix the three citations in the same sweep as AM-07.  
  *Rule:* documentation-§7  
  *Planned in:* AM-34
- **AuraMaster-A-14** `low` (audit AM-34; confirmed) — DEPENDENCIES.md puts Python 3 and Pillow in the wrong groups, and Pillow has no install command  
  *Where:* DEPENDENCIES.md:13-14; DEPENDENCIES.md:117-133; defaults/CastToAura.lua:3-6  
  *Evidence:* The summary lists Python 3 under Development and says Release/assets is 'None.', yet research.py regenerates committed data and Pillow regenerates the icon. That is the Release/assets definition. Pillow gets a recipe but no install line.  
  *Remediation:* Move python3 and the network note to Release/assets. List Pillow with an install command (sudo apt-get install -y python3-pil) and a check (python3 -c 'import PIL; print(PIL.__version__)'). The table row reads 'Python 3.8+ (spell-research generator); Pillow (the 128 icon). Not needed to build, run or test.'  
  *Rule:* documentation-§7 (the three groups)  
  *Planned in:* AM-29

**BankLedger**

- **BankLedger-R-04** `low` (review F-004; corrected) — Default 30-day retention silently deletes older history at login; the README never discloses it  
  *Where:* defaults/Global.lua:47; settings/Schema.lua:118; core/BankLedger.lua:216-228; core/Database.lua:656-675; README.md  
  *Evidence:* retentionDays = 30 by default. The prune runs once per session at login. The 164-line README and its FAQ never mention retention. The only disclosure is a dropdown tooltip on Settings > History.  
  *Remediation:* C-03: add a README FAQ row saying that movements older than 30 days are removed at login by default and can be kept under Settings > History > Keep history for, optionally with a note beside /bl purge. Changing the default to 0 is an optional owner decision (CP2). If taken, note that AceDB strips default-equal values, so players who deliberately chose 30 will also move to 'Always'. Record this under the Version History behavior changes. Drop the savedvariables-§1 rule citation, because this is a documentation (player-facing README) gap.  
  *Rule:* documentation (README is player-facing); savedvariables-§1  
  *Planned in:* BL-22

**ConsumableMaster**

- **ConsumableMaster-A-10** `low` (audit CM-89; confirmed) — README.md still carries the removed '## What's new in 1.6.2' section  
  *Where:* README.md:35-38; README.md:137  
  *Evidence:* This is not one of the eleven canonical sections, and v2.42.0 removed it. Its bullet duplicates the top Version History row.  
  *Remediation:* B5 / S4-3: delete README.md:35-38 and run the de-AI pass over the edit. No version bump.  
  *Rule:* documentation-§1  
  *Planned in:* CM-25

**KickCD**

- **KICKCD-R-14** `low` (both F-014; KICKCD-C-05; confirmed) — README claims /kcd config opens after combat (the code refuses), and /kcd resetposition only resets the target icon grid  
  *Where:* README.md:97, README.md:113, core/KickCD.lua:815-819, settings/Panel_Render.lua:358-377  
  *Evidence:* README.md:97 says '/kcd config waits until combat ends' and :113 says 'it opens the moment combat ends'. NS:OpenSettings refuses and returns, which options-ui-§2 requires (MUST NOT defer-and-replay). Separately (review only), Helpers.ResetIconPosition resets only the target grid, while its help text says 'the icon grid'; the focus grid and both cast bars are untouched.  
  *Remediation:* Rewrite README :97 and :113: the game blocks the panel in combat, so run /kcd config again after it ends. Run the de-AI pass (documentation-§1). For resetposition, either extend ResetIconPosition to every unit's grid and rename the help text to 'Restore the icon grids to their default positions', or keep target-only and say so in the verb text. No badge moves.  
  *Rule:* documentation-§5; documentation-§1; options-ui-§2  
  *Planned in:* KC-15

**LootHistory**

- **LootHistory-A-14** `low` (audit LH-71; confirmed) — README Usage does not close on a one-sentence configuration signpost  
  *Where:* README.md:58  
  *Evidence:* The closing paragraph runs six sentences: configuration, then the enable/disable explanation, then the disabled slash surface. §1 requires one sentence and nothing more.  
  *Remediation:* Move the disabled-state sentences into the Usage body (or FAQ/Troubleshooting). End Usage on one sentence naming Settings ▸ AddOns and /lh help or /loothistory help. Run a de-AI pass.  
  *Rule:* documentation-§1 item 5 (MUST)  
  *Planned in:* LH-32
- **LootHistory-A-15** `low` (audit LH-72; confirmed) — Root CLAUDE.md sections out of mandated order (provenance before green gate)  
  *Where:* CLAUDE.md:49, CLAUDE.md:62  
  *Evidence:* ## Vendored LibKa0s (with the provenance line at :51) precedes ## Green gate at :62. §2 orders the green-gate line (5) before the provenance line (6).  
  *Remediation:* Swap the two sections. The vendor gate greps rather than reading a position; keep tests/test_vendor_sync.lua green.  
  *Rule:* documentation-§2 (MUST)  
  *Planned in:* LH-33
- **LootHistory-A-16** `low` (audit LH-73; corrected) — Doc citations drifted from the tree (DEPENDENCIES.md, ARCHITECTURE.md)  
  *Where:* DEPENDENCIES.md:49, DEPENDENCIES.md:53, DEPENDENCIES.md:112, docs/ARCHITECTURE.md:42-45, docs/ARCHITECTURE.md:207, docs/ARCHITECTURE.md:447, docs/module-map.md  
  *Evidence:* DEPENDENCIES.md:53 cites run-automated-tests.sh :186/:109, now :242/:122 after the v1.55.0 re-vendor. :49 and :112 cite docs/testing.md:187/:179, now :191/:183. ARCHITECTURE.md:42-45 names four load-bearing seams (Item, Media, Widgets, Pool), but CoreSetup and DebugLogSetup are load-bearing too and Pool resolves nothing at load. :207 cites slash-commands-§4 for bare /lh, but the rule is §3. :447's compat trigger says '419 lines' where the trigger is a shim count (21).  
  *Remediation:* Re-point the citations: DEPENDENCIES.md:53 to run-automated-tests.sh:242 (declare -A) and :122 (EPOCHREALTIME); DEPENDENCIES.md:49 to docs/testing.md:191; DEPENDENCIES.md:112 to docs/testing.md:183. Change ARCHITECTURE.md:207 to cite slash-commands-§3. Write the :447 trigger as '21 shims (grep -cE '^\s*function\s+[A-Za-z_][A-Za-z0-9_]*\.' core/Compat.lua)'. Restate the load-bearing set in ARCHITECTURE.md:42-48 and docs/module-map.md from evidence in the tree: Item and Media above Constants; CoreSetup above every file that captures NS.Print at load (modules/Browser.lua:5, settings/Schema.lua:5, settings/Slash.lua:4); Widgets below Media; OptionsSetup above Schema. Call Pool conventional, since nothing resolves at load. Include DebugLogSetup only if a file-load capture of NS.Debug or NS.DebugLog is found. Keep the TOC comments in the same commit, consistent with that set.  
  *Rule:* documentation-§7, documentation-§5 (MUST)  
  *Planned in:* LH-27, LH-28

**PanelMaster**

- **PanelMaster-A-13** `low` (audit PM-045; confirmed) — DEPENDENCIES.md cites stale tests/_kit/framework.lua line numbers after the kit-25 re-vendor  
  *Where:* DEPENDENCIES.md:63, tests/_kit/framework.lua:643-644, tests/_kit/framework.lua:627-628  
  *Evidence:* DEPENDENCIES.md cites framework.lua:515-516 (ls -A / dir /b listing) and :498-500 (LuaFileSystem note). Those lines are now doc comments; the real lines are :643-644 and :627-628. The loader.lua and vendor_sync.lua citations still resolve.  
  *Remediation:* After the whole-folder re-vendor, re-derive every tests/_kit/*:NN citation against the new payload. Cite by function name (Kit.assertSuiteInventory, listDir) next to the line numbers so the next re-vendor does not break them.  
  *Rule:* documentation-§7  
  *Planned in:* PM-23
- **PanelMaster-A-14** `low` (audit PM-046; confirmed) — README has angle-bracket placeholders that CurseForge strips, and Usage does not end on the configuration line  
  *Where:* README.md:51, README.md:79-80, README.md:67-69, README.md:86-95  
  *Evidence:* /pm delete <name>, /pm get <setting> and /pm reset <setting> lose their argument on CurseForge. The configuration signpost sits mid-section and Usage ends on the disabled-state paragraph. Usage is nine paragraphs against guidance of five, which is not a breach.  
  *Remediation:* Write the arguments as bare examples (/pm delete ChatBG, /pm get settings.gridSize). Move the configuration pointer to Usage's last line. Merge the two disabled-state paragraphs. Run the /humanize de-AI pass.  
  *Rule:* documentation-§1  
  *Planned in:* PM-24

**PrettyChat**

- **PRETTYCHAT-A-22** `low` (audit PC-97 (PRETTYCHAT-C-18); confirmed) — DEPENDENCIES.md omits Pillow for the layout-§4 logo TGA recipe  
  *Where:* DEPENDENCIES.md:157-163, core/LauncherSetup.lua:96-97  
  *Evidence:* It says no image tooling is needed, yet the repo's own comment says the 128 TGA was generated with layout-§4's Pillow recipe. documentation-§7 requires the release/assets group to name it.  
  *Remediation:* Add a Pillow (python3-pil) entry under Release / assets: why, install (sudo apt install -y python3-pil), verify (python3 -c 'import PIL; print(PIL.__version__)'), and a note that it is not needed to build or test.  
  *Rule:* documentation-§7  
  *Planned in:* PC-24
- **PRETTYCHAT-A-23** `low` (audit PC-98 (PRETTYCHAT-C-19); confirmed) — README Version History 1.5.0 row uses codebase jargon  
  *Where:* README.md:74  
  *Evidence:* 'The write seam now refuses a format string...' and 'read a nil result as silence rather than as an answer'.  
  *Remediation:* Reword both highlights for players, e.g. 'A format with a placeholder the game cannot fill is now refused when you save it'. Run it through the de-AI pass.  
  *Rule:* documentation-§1  
  *Planned in:* PC-24

**WhatGroup**

- **WHATGROUP-A-18** `low` (audit WG-79; confirmed) — DEPENDENCIES.md omits Python 3 + Pillow for the logo recipe and labels lizard optional  
  *Where:* DEPENDENCIES.md:190-192, DEPENDENCIES.md:92-99  
  *Evidence:* Says no image tooling needed, but layout-§4 fixes a Pillow recipe to regenerate media/logos/whatgroup.logo.128.tga; lizard labeled optional/skip-is-fine while automated-tests-§3 treats a complexity skip at release as not passed.  
  *Remediation:* Add Python 3 + Pillow under Release/assets citing layout-§4 (apt python3-pil or pipx/venv; verify with python3 -c "import PIL; print(PIL.__version__)"; not needed to build/run/test). Relabel lizard 'optional per commit, required at release (automated-tests-§3)'.  
  *Rule:* documentation-§7 (MUST)  
  *Planned in:* WG-27


### C24 — Namespace bootstrap and self-naming file headers

architecture-§1 mandates 'local addonName, NS = ...' while lint forbids suppressing warning 211 for addonName (an upstream conflict). Some files open on a different line, and others lack or misplace the documentation-§9 self-naming header. Affects AbsorbTracker, PartyFrameEnhanced and PrettyChat.

**AbsorbTracker**

- **AbsorbTracker-A-25** `info` (audit AT-Info-8; confirmed) — Info: bootstrap spelling; 19 files open 'local _, NS = ...' and 7 have self-naming headers  
  *Where:* core/, modules/, settings/ (19 files)  
  *Evidence:* Lint keeps the spelling honest, and documentation-§9 grandfathers the existing headers.  
  *Remediation:* None; not filed.  
  *Rule:* documentation-§9  
  *Planned in:* AT-22

**PartyFrameEnhanced**

- **PartyFrameEnhanced-A-13** `low` (audit PFE-20; confirmed) — 10 of the 38 source files do not open on the namespace bootstrap line  
  *Where:* settings/About.lua:5; settings/ElementRows.lua:5; settings/Profiles.lua:6; core/EnvSetup.lua:8; locales/enUS.lua:9; core/MediaSetup.lua:14; settings/PetFrames.lua:14; settings/General.lua:16; settings/CastBars.lua:17; settings/TargetFrames.lua:18  
  *Evidence:* Bootstrap census: 28 files open with `local …, NS = ...` on line 1, 10 open it later, below a header comment.  
  *Remediation:* Audit Sprint 3.2: move `local _, NS = ...` (or `local addonName, NS = ...`) to line 1 in each file, with the header directly beneath. Lint and the suite are the check.  
  *Rule:* architecture-§1  
  *Planned in:* PF-21
- **PartyFrameEnhanced-A-14** `low` (audit PFE-20a; confirmed) — The self-naming header sits above the bootstrap in 10 files, and 3 core files have no header (derived from PFE-20)  
  *Where:* core/Namespace.lua; core/Constants.lua; core/State.lua; the 10 files of PFE-20  
  *Evidence:* `head -5 \| grep -- "-- $f"`: 35 files have a header, 3 do not. SHOULD.  
  *Remediation:* Audit Sprint 3.2: put the header beneath the bootstrap in the PFE-20 sweep, and add path headers to core/Namespace.lua, core/Constants.lua and core/State.lua.  
  *Rule:* documentation-§9  
  *Planned in:* PF-21

**PrettyChat**

- **PRETTYCHAT-A-25** `low` (audit PC-99 (PRETTYCHAT-C-20); confirmed) — 11 of 20 source files lack a self-naming first comment  
  *Where:* core/Constants.lua:1, core/Database.lua:1, core/Namespace.lua:1, core/PrettyChat.lua:1, core/State.lua:1, core/Util.lua:1, defaults/Defaults.lua:1, defaults/Profile.lua:1, locales/enUS.lua:1, modules/Override.lua:1, settings/Schema.lua:1  
  *Evidence:* documentation-§9 SHOULD. The *Setup.lua, Panel.lua and Slash.lua files already follow the model.  
  *Remediation:* Prepend '-- <path> — <one-line purpose>' to each of the eleven, below the vararg line where there is one.  
  *Rule:* documentation-§9  
  *Planned in:* PC-16
- **PRETTYCHAT-A-28** `info` (audit PC-100 (PRETTYCHAT-C-21); corrected · upstream → WowAddonStandards) — architecture-§1 mandates `local addonName, NS = ...` while lint forbids suppressing 211/addonName (eleven files use `local _, NS = ...`)  
  *Where:* .luacheckrc:29-38  
  *Evidence:* The two MUSTs cannot both be met literally for a file that never reads the name. Recorded, not filed.  
  *Remediation:* Raise upstream as a clarification only. architecture-§1 should read 'destructure both varargs; name the first `_` when the file never reads it', so the collection does not need per-file 211/addonName stanzas that lint.md would allow but that are just noise. Change nothing in the addon.  
  *Rule:* architecture-§1; lint  
  *Planned in:* WS-07


### C25 — Unused .luacheckrc read_globals

Each of these .luacheckrc files allowlists removed or deprecated globals that nothing reads (GetSpellInfo, GetAddOnMetadata, UnitExists, UISpecialFrames), so a regression would lint clean. WhatGroup's also omits the template's docs/revendor/ exclusion. Affects AbsorbTracker, AuraMaster, KickCD, MultiMeters, PartyFrameEnhanced, PrettyChat and WhatGroup.

**AbsorbTracker**

- **AbsorbTracker-R-09** `low` (review F-008; confirmed) — .luacheckrc allowlists eight read_globals that no authored source reads  
  *Where:* .luacheckrc (top-level read_globals), settings/OptionsSetup.lua:144  
  *Evidence:* C_Timer, hooksecurefunc, CreateColor, PlaySound, strsplit, strtrim, tinsert and tremove each grep to 0 hits over authored Lua. C_Timer's only hit is a comment. A stray hooksecurefunc or C_Timer call would lint clean and bypass library-stack-§1's AceTimer rule.  
  *Remediation:* C-07: remove the eight names from read_globals and confirm luacheck stays 0/0. test_lintconfig checks ignore shape only, so it is unaffected.  
  *Rule:* lint, library-stack-§1  
  *Planned in:* AT-17

**AuraMaster**

- **AuraMaster-R-07** `low` (both F-010; AM-28; confirmed) — .luacheckrc declares four read_globals nothing references (GameTooltip, C_Spell, GetAddOnMetadata, GetSpellInfo)  
  *Where:* .luacheckrc:13-23 (entries at :14-15)  
  *Evidence:* The file's own header says a name nothing reads comes off the list. After the v1.55.0 Compat wiring these names appear only in comments or as table fields (NS.Compat.GetSpellInfo, C_AddOns.GetAddOnMetadata). A probe with the four removed still gives 0/0 over 110 files (E-1). Declaring the removed global GetSpellInfo would let a regression of anti-pattern #10 lint clean.  
  *Remediation:* Delete the four entries and re-run luacheck (it must stay 0/0). If tests/test_lintconfig.lua pins the list, update it in the same commit. Optionally add a lint-config case asserting every read_globals name is referenced by some authored file.  
  *Rule:* lint (config hygiene); anti-pattern #10  
  *Planned in:* AM-21

**KickCD**

- **KICKCD-R-16** `low` (review F-016; confirmed) — .luacheckrc whitelists deprecated globals that no shipped code reads, so a regression would lint clean  
  *Where:* .luacheckrc:57, .luacheckrc:63  
  *Evidence:* read_globals lists GetSpellInfo, GetSpecialization, GetSpecializationInfo, IsPlayerSpell, IsSpellKnown and IsSpellKnownOrOverridesKnown. A bare-name count over shipped code gives 0 for each.  
  *Remediation:* C-10: remove them from read_globals and move any that tests/ needs into files['tests/']. Update tests/test_lintconfig.lua in the same change if it pins the list.  
  *Rule:* lint  
  *Planned in:* KC-21

**MultiMeters**

- **MultiMeters-R-14** `low` (review F-014; confirmed) — .luacheckrc whitelists the removed global GetSpellInfo  
  *Where:* .luacheckrc:69  
  *Evidence:* The code calls only Compat.GetSpellInfo (modules/DrillDown.lua:549-550, modules/Tooltip_Lines.lua:660-661). A future bare call would lint clean.  
  *Remediation:* C-11: remove 'GetSpellInfo' from read_globals, then confirm luacheck is still 0/0.  
  *Planned in:* MM-11

**PartyFrameEnhanced**

- **PartyFrameEnhanced-R-13** `low` (review F-013; confirmed) — .luacheckrc whitelists 12 globals that nothing uses, including the deliberately removed UnitExists  
  *Where:* .luacheckrc:14-38; core/Compat.lua:205-208  
  *Evidence:* GetTime, wipe, Mixin, UnitExists, UnitGUID, UnitIsUnit, UnitIsDeadOrGhost, UnitIsConnected, C_Secrets, RegisterUnitWatch, UnregisterUnitWatch and UnregisterStateDriver have 0 bare-global uses. A raw UnitExists(compoundToken) would lint clean, which is the secret-value hazard Compat documents removing.  
  *Remediation:* C-008 / T-9, after T-5: remove the unused names. UnregisterStateDriver stays because C-005 gives it a real use. Keep UnitExists out, with a comment pointing to core/Compat.lua:205-208.  
  *Rule:* lint  
  *Planned in:* PF-14

**PrettyChat**

- **PRETTYCHAT-R-08** `low` (review F-008 (change C-08); confirmed) — .luacheckrc declares 12 unused globals, including a writable UISpecialFrames  
  *Where:* .luacheckrc:55, .luacheckrc:64, .luacheckrc:65, .luacheckrc:67, .luacheckrc:70, .luacheckrc:71, .luacheckrc:78, .luacheckrc:82-86  
  *Evidence:* With the 12 entries removed (UISpecialFrames, date, wipe, SettingsPanel, GameTooltip, InCombatLockdown, UIParent, five GameFont*), luacheck still reports 0/0 in 48 files. They are left over from code that moved into LibKa0s.  
  *Remediation:* Delete the 12 entries. tests/test_lintconfig.lua keeps passing.  
  *Rule:* lint  
  *Planned in:* PC-17

**WhatGroup**

- **WHATGROUP-R-11** `low` (review F-011; confirmed) — .luacheckrc read_globals grants removed/unused globals (GetSpellInfo etc.), so a regression would lint clean  
  *Where:* .luacheckrc:47, .luacheckrc:52, .luacheckrc:54  
  *Evidence:* read_globals lists GetSpellInfo, GetSpellTexture, GetSpellCooldown, CastSpellByID, SettingsPanel, date; no authored runtime file reads them (spell ladder is LibKa0s-Compat's); three are removed on retail.  
  *Remediation:* C-009: remove those six names from top-level read_globals; run luacheck (must stay 0/0); restore any name that surfaces with a comment naming its reader. test_lintconfig checks ignores only.  
  *Rule:* lint; testing-§4  
  *Planned in:* WG-18
- **WHATGROUP-A-20** `info` (audit WG-83; confirmed) — .luacheckrc omits the template's docs/revendor/ exclusion  
  *Where:* .luacheckrc:13-17  
  *Evidence:* Template exclude_files ends "docs/revendor/", "_dev/", "tests/_kit/"; repo lacks docs/revendor/ despite its own comment excluding frozen bundles. No Lua there today.  
  *Remediation:* Add "docs/revendor/" to exclude_files at .luacheckrc:17; update tests/test_lintconfig.lua if it pins the list.  
  *Rule:* lint (template)  
  *Planned in:* WG-18


### C26 — Degradation stubs: library copies and surface-parity tests

Library-absent stubs copy library formatters and composers, overwrite real host functions with no-ops, or are level-triggered where the library is edge-triggered, and several have no testing-§8 surface-parity case. The options-ui-§1 hollow-composer ruling conflicts with the live enable/disable verbs on a degraded load (upstream). Affects AbsorbTracker, AuraMaster, BankLedger, LootHistory, PanelMaster, PrettyChat and WhatGroup.

**AbsorbTracker**

- **AbsorbTracker-A-02** `low` (audit AT-62; confirmed · upstream → LibKa0s) — The Options degradation stub still carries host copies of all five composed blocks; the hollow fix is unavailable because host verbs reach composed rows on a degraded load  
  *Where:* settings/OptionsSetup.lua:237-377 (composeBlock :241, ColorPair :278, FontGroup :289, BorderGroup :300, BarGroup :314, MasterControls :329), settings/Slash.lua:540-541, settings/Slash.lua:311, settings/Slash.lua:91, settings/Slash.lua:96, core/AbsorbTracker.lua:259, settings/Schema.lua:160-161  
  *Evidence:* This recurs. On a library-less load, enable, disable, lock, unlock, the combat re-lock and the launcher stub all write the composed rows 'enabled' and 'locked' through NS.SetByPath. The Schema stub refuses a path with no row. A hollow composer would therefore silently break /at disable on a broken install, while the host copy is anti-pattern #73. options-ui-§1's fall-together bound denies the hollow exemption here.  
  *Remediation:* Upstream first (A1/S0.1): LibKa0s-Options-1.0 ships the composers (ColorPair, FontGroup, BorderGroup, BarGroup, MasterControls, MASTER_GROUP) from a unit that loads without the Options major but keeps the Core floor, with a library test. Then re-vendor (S3.1) and delete composeBlock, ORDER_STEP and the host copies. Interim (C14/S2.7), recommended option (a): file a Documented-deviations row for options-ui-§1 citing the fall-together gap and the upstream issue. Option (b), hollow composers plus degraded host verbs that refuse honestly, is not recommended. Also raise the §1 tension upstream (Info-6).  
  *Rule:* options-ui-§1, anti-pattern #73  
  *Planned in:* LK-23, AT-08
- **AbsorbTracker-A-03** `low` (audit AT-63; confirmed · upstream → LibKa0s) — Suite pins schema equality across the live and degraded arms instead of counts plus the named gap (dependent of AT-62)  
  *Where:* tests/test_perf.lua:501, tests/test_optionssetup.lua:233, tests/test_optionssetup.lua:243  
  *Evidence:* This recurs. The pins are assertEqual(#NS2.Schema, #NS.Schema), '-- red under: a stub composer returning {}', and assertEqual(#rows, 4, 'the canonical border block is four rows'). They are written to fail against the hollow shape. §1 wants both counts and the named gap.  
  *Remediation:* Moves with AT-62. After the S0.1 re-vendor, point tests/test_perf.lua:501 and test_optionssetup.lua:233-243 at the library's degraded arms (equality then holds by construction). If interim path (b) is chosen instead, rewrite the pins as three figures: full count, degraded count, and the named gap attributed to the five composers.  
  *Rule:* options-ui-§1  
  *Planned in:* LK-23, AT-08
- **AbsorbTracker-A-10** `low` (audit AT-67; corrected) — No stub-surface parity cases for LibKa0s-Perf-1.0 and LibKa0s-Lifecycle-1.0  
  *Where:* tests/test_surface_parity.lua:3, core/PerfSetup.lua:23-30, core/Lifecycle.lua:155-177, tests/run.lua  
  *Evidence:* This recurs, and is now wider. Parity covers 7 seams (Core, DebugLog, Options, Slash, Launcher, Bus, Schema). The Perf and Lifecycle stubs are real member tables: the host calls Perf.on, .Note, .OnCommand and .suspended, and lifecycle:Set, :IsDown, :Reevaluate and :Holds. Both stubs are complete today, but nothing gates them.  
  *Remediation:* C13/S2.2: add parity cases for NS2.Perf (LibKa0s-Perf-1.0) and NS2.lifecycle (LibKa0s-Lifecycle-1.0) to tests/test_surface_parity.lua. Take the degraded arm from tests/degraded_env.lua and the live arm from NS.Perf / NS.lifecycle, registered in Kit.setSurfaceSource. Assert the grep-derived member set the host reaches, present and non-nil on BOTH arms: Perf {on, suspended, Note, OnCommand} and lifecycle {Set, IsDown, Reevaluate, Holds}. Name each grep in the case comment: grep -rohE '\bPerf[.:][A-Za-z_]+' core modules settings, and grep -rohE 'lifecycle[.:][A-Za-z_]+' core modules settings. Only use the whole-surface by-name form with an ignore set where the stub mirrors the instance closely (Lifecycle); for Perf that form would need an ignore set covering most of the instance. Update the header count to nine, and verify by mutation (delete a stub member) that each case goes red.  
  *Rule:* testing-§8  
  *Planned in:* AT-14
- **AbsorbTracker-A-23** `info` (audit AT-Info-6; confirmed · upstream → WowAddonStandards) — Info [upstream]: the options-ui-§1 hollow-composer ruling conflicts with slash-commands-§1/§2's live enable and disable verbs on a degraded load  
  *Where:* standard: options-ui-§1, slash-commands-§1, slash-commands-§2  
  *Evidence:* Every addon that composes Master controls meets AT-62's dilemma: its host verbs write the composed 'enabled' row on a degraded load.  
  *Remediation:* S0.4 / A2: ask WowAddonStandards to rule which rule wins, or require the LibKa0s degraded-composer fix (A1) collection-wide.  
  *Rule:* options-ui-§1, slash-commands-§1/§2  
  *Planned in:* WS-02

**AuraMaster**

- **AuraMaster-R-06** `low` (both F-008; AM-22; confirmed) — Degradation stubs copy library behavior; the Options stub composers rebuild composed blocks instead of answering an empty row list  
  *Where:* settings/OptionsSetup.lua:175-280 (composeBlock, ColorPair, FontGroup, BorderGroup, BarGroup, MasterControls); tests/test_optionssetup.lua:369; settings/Slash.lua:388-391 (stub.DisabledLine); core/PoolSetup.lua:17-49; docs/settings-panel.md  
  *Evidence:* Each stub is described as 'spelled as the library spells it', which makes it the copy that drifts (anti-pattern #56). Since v2.64.0, stub composer members MUST answer an empty row list, and a host copy of a composed block inside the stub is anti-pattern #73. The test pins #NS2.Schema == #NS.Schema, when it should pin full, degraded and delta. The Slash stub re-spells the library refusal line. The Pool stub copies New/Acquire/ReleaseAll/Counts, which is defensible because a pool-less preview leaks. Only degraded installs reach any of this.  
  *Remediation:* Options stub (the audit's v2.64.0 ruling overrides the review's 'keep if validation fails' fallback): every composer answers {}, MasterControls answers {}, function() end, and composeBlock is deleted. Update the header comment to cite options-ui-§1. Replace the :369 assertion with three pins: the full-load count, the library-absent count, and the named composer delta (red under: a non-empty stub composer). Add a fall-together case: on the degraded load, /am set <composed path> answers the unavailable line. Make NS.ValidateSchema and the degraded path validation tolerate the smaller schema. Update docs/settings-panel.md 'The degraded panel'. Slash stub: keep DisabledLine but make it falsifiable with a test_surface_parity case comparing the with-library and without-library strings (red under: the library rewording). Pool stub: keep it, and tighten its comment to give the leak reason.  
  *Rule:* options-ui-§1; anti-patterns #56, #73; library-stack-§7  
  *Planned in:* AM-16

**BankLedger**

- **BankLedger-A-08** `low` (audit BL-37; corrected) — No test pins the library-absent row count or the composed delta (16 / 8 / 8) (recurs)  
  *Where:* tests/test_schema.lua:236-297; settings/OptionsSetup.lua:203-207; settings/Schema.lua:31-124,315-350; tests/test_surface_parity.lua; tests/degraded_env.lua  
  *Evidence:* The suite pins fully-loaded tab counts and the member set only. The delta grew from 6 to 8 when minimapPath and testModePath joined the composer, and nothing noticed.  
  *Remediation:* S4-1: add a case beside the tab-count case. It loads the live instance and Env.loadDegraded() and asserts #S.Schema == 16 live and 8 degraded, and #S:PageRows() == 17 live and 9 degraded (PageRows adds one row over the registry). Assert live minus degraded == 8 on both measures and attribute the delta to MasterControls/the composer in the message. Keep the falsification comment ('red under a composer that stops being hollow, or a host row added or removed'). +1 test.  
  *Rule:* options-ui-§1 (When the missing content is COMPOSED)  
  *Planned in:* BL-14

**LootHistory**

- **LootHistory-R-08** `low` (review F-008; corrected) — DebugLog degradation stub copies library formatters and colors with no caller  
  *Where:* core/DebugLogSetup.lua:34-40  
  *Evidence:* The stub's FormatPlain/FormatColored repeat the library's format strings and color codes (\|cff6f8faf, \|cffc9a66b). A grep finds no addon non-test caller; only tests/test_debuglog.lua reaches these members, and it reaches the live library instance. The copy is inert and will go stale.  
  *Remediation:* Keep both members on the stub, but make each one return tostring(msg), or a plain concatenation with no color codes, so no library format string lives in the addon and the surface-parity case stays green without an ignore-list change. The alternative is to remove them and add "FormatPlain" and "FormatColored" to the ignore list at tests/test_surface_parity.lua:129, with the zero-caller grep in the comment. Land this together with R-07.  
  *Rule:* library-stack-§7 (no-copy bound); anti-pattern #47  
  *Planned in:* LH-20
- **LootHistory-R-14** `low` (review F-014; confirmed) — Degraded CliResetAll clears all three id lists then only says 'unavailable'  
  *Where:* settings/Slash.lua:317-320  
  *Evidence:* It runs NS.Filters:ClearAll() and then unavailable(), so the player is not told that the blacklist, whitelist and currency blacklist were emptied. Reachable only on a library-less install via a host caller.  
  *Remediation:* C-013: print 'filters reset (N ids cleared); other settings need the LibKa0s library.' using the counted return of Filters:ClearAll(). Smoke S-008.4.  
  *Rule:* library-stack-§7  
  *Planned in:* LH-16
- **LootHistory-A-11** `low` (audit LH-68; confirmed) — No surface-parity case for the Env, Item, Media, Pool and Lifecycle stubs  
  *Where:* tests/test_surface_parity.lua:66-214, core/EnvSetup.lua, core/ItemSetup.lua:40-67, core/MediaSetup.lua, core/PoolSetup.lua:24-52, core/LifecycleSetup.lua:148-162  
  *Evidence:* Parity cases exist for Core, Widgets, Slash, DebugLog, Options, Bus, Compat and Schema. Five adopted modules with library-absent branches have none. Every member reached today is answered, so this is a gate gap, not a live crash. Launcher has no stub by written decision.  
  *Remediation:* Add five parity cases, by-name or two-table, each with a '-- members from: grep ...' comment and the degraded arm from tests/degraded_env.lua. Verify each goes red when a stub member is deleted and record that mutation (testing-§12). Move the badge and inventory in the same commit.  
  *Rule:* testing-§8 (MUST)  
  *Planned in:* LH-22

**PanelMaster**

- **PanelMaster-A-08** `low` (audit PM-040; confirmed) — The Lifecycle degradation stub has no surface-parity case, although a code comment and module-map.md say it does  
  *Where:* core/LifecycleSetup.lua:147-190, tests/test_surface_parity.lua:3, tests/test_surface_parity.lua:59-226, docs/module-map.md:19, tests/run.lua (Kit.setSurfaceSource), tests/degraded_env.lua  
  *Evidence:* The stub has 9 members (Hold, Release, Set, IsHeld, IsDown, Holds, Reevaluate, PrintHolds, name). The parity suite has six cases (Core, DebugLog, Launcher, Slash, Options, Schema) and none for Lifecycle. Env and Media are not affected because they have no separate stub.  
  *Remediation:* Add 'Parity: the Lifecycle seam's degraded surface matches the live one'. Build the degraded arm with loadPartial or degraded_env omitting Lifecycle.lua, name the grep (grep -rn 'NS\.Lifecycle[:.]' core modules settings) in a comment, add ['LibKa0s-Lifecycle-1.0'] = NS.Lifecycle to Kit.setSurfaceSource, and put name in the ignore set if walked. Update the header count to seven and docs/testing.md:340-351.  
  *Rule:* testing-§8  
  *Planned in:* PM-13

**PrettyChat**

- **PRETTYCHAT-R-06** `low` (review F-005 (change C-05); confirmed) — Degraded install: /pc test and the Test button print nothing after the first run, though the comments and docs claim a chat fallback  
  *Where:* settings/Panel.lua:101-104, core/DebugLogSetup.lua:71, modules/Override.lua:663-668, docs/settings-panel.md:231, docs/module-map.md:236  
  *Evidence:* TestToConsole always passes the NS.DebugLog:Add sink, and the stub's Add is a no-op, so the NS.Print default is unreachable. With LibKa0s absent, the first run prints one 'console unavailable' line and every run after that prints nothing.  
  *Remediation:* In TestToConsole, resolve LibStub('LibKa0s-DebugLog-1.0', true) once at file load. When it is absent, call PrettyChat:Test(filter) with no sink so NS.Print serves it. Leave the stub's member set unchanged (test_surface_parity). Update docs/settings-panel.md:231 and module-map.md:236. Add a case in tests/test_libka0s.lua with the library absent, asserting that '/pc test category Loot' puts a 'Category: Loot' line in the chat mock.  
  *Rule:* testing-§8; options-ui-§1  
  *Planned in:* PC-08

**WhatGroup**

- **WHATGROUP-A-11** `low` (audit WG-72; confirmed) — No stub-surface parity case for the Launcher and Lifecycle seams  
  *Where:* tests/test_surface_parity.lua:1-43, tests/test_launcher.lua:391-403, core/LauncherSetup.lua, core/LifecycleSetup.lua, tests/run.lua  
  *Evidence:* Parity suite covers Core, DebugLog, Slash, Options, Compat; header says 'five seams' but nine majors adopted. Launcher has only a hand-listed member test without grep; Lifecycle has none. Stubs match live today (5 and 8 members).  
  *Remediation:* Add by-name cases T.assertSurfaceParity(degraded.Launcher, "LibKa0s-Launcher-1.0") and Lifecycle (ignore `name` data field if needed), degraded arm from T.newAddon{skip=NO_LIBKA0S}, grep named in comment; register live instances via Kit.setSurfaceSource in tests/run.lua; rewrite header inventory to name all seven stubs plus Env/Media via namespace case.  
  *Rule:* testing-§8 (MUST); anti-pattern #56  
  *Planned in:* WG-14
- **WHATGROUP-R-04** `low` (review F-004; corrected) — Options degradation stub overwrites host's real RestoreAllDefaults with a no-op; /wg resetall falsely reports success  
  *Where:* settings/OptionsSetup.lua:150, settings/Schema.lua:691, settings/Schema.lua:791-792, settings/Slash.lua:396-405, tests/test_libka0s.lua:637-661  
  *Evidence:* On the degraded path H is the host table; `H.RestoreAllDefaults = function() end` replaces the real reset. Repro with NO_LIBKA0S: notify.delay=7, RestoreAllDefaults() -> still 7. options-ui-§1 SHOULD keeps the global reset real in the stub. Degraded block tests cover enable/disable and test on\|off but not resetall.  
  *Remediation:* C-004: `H.RestoreAllDefaults = H.RestoreAllDefaults or function() end` with a comment citing options-ui-§1 (RestoreAllDefaults is the only colliding stub member by inspection). Add degraded case to tests/test_libka0s.lua: load NO_LIBKA0S, change row, call RestoreAllDefaults, assert default (red under the no-op assignment). Move inventory/badge. Smoke S-004.  
  *Rule:* options-ui-§1 (SHOULD); anti-pattern #47  
  *Planned in:* WG-09


### C27 — Compat and deprecated API use

Deprecated globals (GetItemInfo, SendChatMessage, GetAddOnMetadata, GetMouseFocus) are called outside core/Compat.lua or without a C_* ladder. The standard is inconsistent about whether Compat.lua is required (upstream). Affects AbsorbTracker, AuraMaster, ConsumableMaster, MultiMeters and PrettyChat.

**AbsorbTracker**

- **AbsorbTracker-A-15** `low` (audit AT-77; confirmed · upstream → WowAddonStandards) — No core/Compat.lua; the deprecated GetAddOnMetadata rung lives in core/EnvSetup.lua  
  *Where:* core/EnvSetup.lua:67-72 (function NS.Meta, :70-71)  
  *Evidence:* compat says every addon MUST ship core/Compat.lua as the only file calling deprecated APIs. The file was deleted at bebb43f when metadata moved to LibKa0s-Env-1.0. There is no register row. library-stack-§7 notes that AbsorbTracker and PrettyChat carry none but rules nothing.  
  *Remediation:* C7/S2.5 branches on the S0.4 ruling. Either (a) restore a thin core/Compat.lua, loaded first and annotated, that publishes NS.Compat.GetAddOnMetadata, have EnvSetup's fallback call it, and add a module-map row plus a compat-layer row at '1 shim'; or (b) file a 'compat' register row with the re-check trigger 'first deprecated/version-variant API outside the Env seam'; or close it if the standard adds an applicability condition. Raise the applicability question upstream.  
  *Rule:* compat, library-stack-§7  
  *Planned in:* WS-05, AT-16

**AuraMaster**

- **AuraMaster-R-13** `info` (review F-013; corrected) — Duplicated enabled predicate, production exports kept only for tests, and a dead GetMouseFocus fallback  
  *Where:* core/LifecycleSetup.lua:30-32; settings/Slash.lua:109-111; modules/ContainerManager.lua:415-422 (CM.Rename); core/Database.lua:66 (Database.Merge); settings/Schema.lua:523 (NS.IsSection); core/Compat.lua:314  
  *Evidence:* enabledStored() and isEnabled() are the same NS.GetSetting('enabled') ~= false, each with its own copy of the comment. CM.Rename, Database.Merge and NS.IsSection are test-only seams with production names. Compat falls back to _G.GetMouseFocus, which was removed in 11.0 and is dead on a 120100-only TOC.  
  *Remediation:* Hoist one NS.EnabledStored() into core/LifecycleSetup.lua (it loads before settings/Slash.lua) and have Slash.lua's liveness check call it, with one copy of the comment. Leave the documented test seams (CM.Rename, Database.Merge, NS.IsSection) as they are. A `__` rename is optional and, if done, needs all test callers updated in the same commit. Dropping the GetMouseFocus fallback in core/Compat.lua is optional, and if done should also drop the other pre-11.0 fallbacks in the file for consistency. Neither is a standards requirement.  
  *Rule:* architecture; compat (deprecated API)  
  *Planned in:* AM-19

**ConsumableMaster**

- **ConsumableMaster-R-05** `low` (review F-005; corrected) — Two hot-path item reads call the bare deprecated global GetItemInfo with no C_Item ladder; itemFields caches an unread subType  
  *Where:* modules/Ranker.lua:88; modules/Ranker.lua:83-96; modules/Ranker.lua:235-322; core/TooltipCache.lua:459  
  *Evidence:* The siblings core/Classifier.lua:165-169 and core/WeaponSlots.lua:46-49 already prefer C_Item with a guarded fallback. These two sites run on every recompute and every tooltip-cache fill. Whether 12.0.x still ships the global is unverified; if a patch removes it, ranking and tooltip parsing both fail. subType is fetched and cached but none of the 15 callers reads it.  
  *Remediation:* Add KCM.Compat.GetItemInfo in core/Compat.lua (C_Item.GetItemInfo first, the global as a guarded fallback) and route Ranker.itemFields and TooltipCache.Get through it. Drop subType from the fetch, the cache and the return, and update the 14 call sites (Ranker.lua:235-322 and :582) to destructure (quality, ilvl, tt). Add C_Item.GetItemInfo to tests/wow_mock.lua if it is missing, add a compat test, and compare the offline recompute B/iter against the 2551.1 baseline.  
  *Rule:* anti-pattern #10; compat  
  *Planned in:* CM-13

**MultiMeters**

- **MultiMeters-R-03** `medium` (review F-003; corrected) — Chat exports call the deprecated global SendChatMessage from a feature module, and would silently fall back to printing to self  
  *Where:* modules/Export.lua:879; modules/Export.lua:885-889; core/Compat.lua  
  *Evidence:* `local send = chatType and _G.SendChatMessage`. The global has been deprecated since 11.2.0 (Deprecated_ChatInfo.lua) in favour of C_ChatInfo.SendChatMessage. When it is absent, the export prints the lines to the player and returns true, with no notice, so a channel export looks sent when nothing was sent.  
  *Remediation:* C-03: add Compat.ChatSender() in core/Compat.lua, resolved at call time, preferring C_ChatInfo.SendChatMessage and falling back to _G.SendChatMessage. Export.lua uses NS.Compat.ChatSender(). If a real channel was requested and no sender exists, print one localized notice before the self-print. SELF stays silent. Tests (tests/test_export.lua): C_ChatInfo preferred; one notice on RAID with no sender; no notice on SELF. A LibKa0s-Compat member is deferred (one consumer, anti-pattern #55). Smoke test SM-05.  
  *Rule:* compat (deprecated calls only in core/Compat.lua)  
  *Planned in:* MM-04

**PrettyChat**

- **PRETTYCHAT-A-18** `low` (audit PC-93 (PRETTYCHAT-C-14); confirmed · upstream → WowAddonStandards) — No core/Compat.lua, and the legacy GetAddOnMetadata is called directly; the standard is inconsistent about whether Compat is required  
  *Where:* core/EnvSetup.lua:75-76, core/EnvSetup.lua:6-20  
  *Evidence:* compat says every addon MUST ship core/Compat.lua. library-stack-§7 says 'AbsorbTracker and PrettyChat carry none', and the documentation-§3 compat-layer.md trigger counts shims in a possibly-absent file. The legacy call is on the degraded-install path only.  
  *Remediation:* Upstream first (Sprint 0.3): ask WowAddonStandards whether the MUST binds an addon with zero addon-specific shims. If it does, add a minimal core/Compat.lua (TOC before EnvSetup, annotated) with NS.Compat.GetAddOnMetadata owning the legacy rung, have EnvSetup's fallback call it, and update the compat-layer.md N/A row. If it does not, the finding closes by rule change.  
  *Rule:* compat; library-stack-§7; documentation-§3  
  *Planned in:* WS-05, PC-15


### C28 — Combat-state detection and secure-frame writes

Visibility decides from InCombatLockdown(), which stays false until after PLAYER_REGEN_DISABLED, so 'only in/out of combat' misses the pull, and tests deliver the events in the reverse order. Secure-write memos lose a change reverted in combat, and a weapon-enchant macro deferred in combat flushes as a single-item macro. Affects ConsumableMaster, LootHistory, PanelMaster and PartyFrameEnhanced.

**ConsumableMaster**

- **ConsumableMaster-R-01** `medium` (review F-001; corrected) — A weapon-enchant (WPN_ENCH) macro deferred in combat is flushed as a single-item macro, losing /use 16 and /use 17 and the off-hand line  
  *Where:* modules/MacroManager.lua:531; modules/MacroManager.lua:418; modules/MacroManager.lua:598-602; settings/Slash.lua:210-222; tests/test_macromanager.lua:330  
  *Evidence:* A per-hand write queued in combat stores only itemID = mhPick or ohPick, and entry.cat is nil. FlushPending then rebuilds it through M.SetMacro, which only knows the single-item shape. A scratch probe gave '#showtooltip / /use item:944001 / /use 16 / /use item:944002 / /use 17' out of combat, but '#showtooltip / /use item:944003' after a deferral and flush. The fingerprint stores the wrong body, so nothing corrects it until some later recompute. Reachable through /cm rewritemacros in combat (documented as allowed), a weapon swap mid-fight, or an oil looted or used up mid-fight. The FlushPending test covers KCM_FOOD only.  
  *Remediation:* C-01: FlushPending replays the queued body. Composites keep pcall(M.SetCompositeMacro, entry.cat, nil). Every other entry calls pcall(commitMacro, name, entry.body, entry.itemID, entry.catKey) through the one write tail, with no second write path (events-frames-taint-§4). Characterization first (the FOOD case at :330), then two red-first cases: a per-hand flush keeps /use 16 and /use 17, and /cm rewritemacros in combat keeps the WPN_ENCH body. About +2 cases; regenerate test-cases.md and the badge.  
  *Rule:* events-frames-taint-§4; testing-§13  
  *Planned in:* CM-04

**LootHistory**

- **LootHistory-A-02** `medium` (audit LH-65; confirmed) — General visibility decides from InCombatLockdown(), so 'Only out of combat' fails to hide at the pull  
  *Where:* modules/Browser.lua:1135, modules/Browser.lua:1246-1247, modules/Browser.lua:1252, modules/BrowserTable.lua:543  
  *Evidence:* B:VisibilityAllows reads InCombatLockdown() for a purely visual decision, and B:ApplyVisibility runs from the PLAYER_REGEN_DISABLED handler, where lockdown is not yet engaged (options-ui-§15 relies on that timing). BrowserTable's testModeRefusal reads the same flag. tests/test_browser.lua:627-636 set the mock's lockdown flag directly, so the suite cannot see the event timing. Not reproduced in the client.  
  *Remediation:* Make VisibilityAllows(inCombat) and ApplyVisibility(inCombat) take the edge explicitly: true from PLAYER_REGEN_DISABLED, false from PLAYER_REGEN_ENABLED, else UnitAffectingCombat('player'). Use UnitAffectingCombat for testModeRefusal too. Add UnitAffectingCombat to .luacheckrc read_globals. Add tests that fire PLAYER_REGEN_DISABLED with mock lockdown false and assert the window hides under Only out of combat (red under an InCombatLockdown read), plus the mirror for Only in combat. Add a Version History note for the behavior change. Smoke S1: pull a dummy with Only out of combat set.  
  *Rule:* events-frames-taint-§2 (SHOULD)  
  *Planned in:* LH-05

**PanelMaster**

- **PanelMaster-R-03** `high` (review F-002; confirmed) — 'Only in combat' and 'Only out of combat' visibility never flip at combat start because Compat.InCombat uses InCombatLockdown  
  *Where:* core/Compat.lua:79-82, modules/Canvas.lua:787, core/PanelMaster.lua:116-127  
  *Evidence:* Compat.InCombat() returns InCombatLockdown(). Lockdown begins after PLAYER_REGEN_DISABLED and ends before PLAYER_REGEN_ENABLED, so it reads false inside both handlers. OnRegenDisabled -> RenderForCombat() therefore rebuilds every spec with inCombat=false. An inCombat profile stays hidden for the whole fight and an outOfCombat profile stays visible. events-frames-taint-§2 names this exact shape.  
  *Remediation:* Thread the transition's truth from the event: OnRegenDisabled -> NS.Canvas:RenderForCombat(true), and OnRegenEnabled -> RenderForCombat(false) after ResumePending. Add an optional inCombat parameter to Canvas:Render, RenderAll and RenderForCombat (Render defaults it to NS.Compat.InCombat()). Change Compat.InCombat() to prefer UnitAffectingCombat('player'), presence-guarded, with InCombatLockdown as the fallback. Add UnitAffectingCombat to .luacheckrc read_globals. Keep the unlock deferral on InCombatLockdown. Keep BuildSpec pure. Verify in-client (smoke C-03).  
  *Rule:* events-frames-taint-§2; compat  
  *Planned in:* PM-03
- **PanelMaster-R-06** `medium` (review F-005; corrected) — The combat-visibility test raises the combat flag before delivering PLAYER_REGEN_DISABLED, the reverse of the client's order  
  *Where:* tests/test_canvas.lua:422-446, tests/test_canvas.lua:436-437  
  *Evidence:* The case sets T.mocks.__inCombat = true and then calls NS.addon:OnRegenDisabled(). The client fires the event before lockdown begins, so the case passes against the broken implementation in R-03. That is testing-§12's 'coverage that is asleep' shape.  
  *Remediation:* Deliver OnRegenDisabled with __inCombat still false and assert the outOfCombat panel hides. Mirror it for an inCombat profile: shown after OnRegenDisabled, hidden after OnRegenEnabled. For the test_compat case, diverge the two APIs within the test: temporarily override the mock's InCombatLockdown to return false while __inCombat is true, assert Compat.InCombat() is true, and restore it after. Do not edit tests/_kit/ locally. If a separate lockdown flag in the kit mock is wanted, file it upstream in LibKa0s and re-vendor. Run red before the R-03 fix and add '-- red under: drop the explicit inCombat argument from OnRegenDisabled'.  
  *Rule:* testing-§12; testing-§4  
  *Planned in:* PM-03

**PartyFrameEnhanced**

- **PartyFrameEnhanced-R-04** `medium` (review F-003; confirmed) — The secure-write memo compares against the APPLIED value, so a change reverted in combat is lost (Click to target stays off after combat)  
  *Where:* modules/UnitButtons.lua:54,56,65,67  
  *Evidence:* `if btn.__clicks == on then return end` and `if btn.__driver == driver then return end` are set only inside the deferred closure. Toggling A→B→A in combat therefore leaves B queued. Reproduced: 'setting true btn.__clicks false attr *type1 nil' after leaving combat.  
  *Remediation:* C-003 / T-3: keep request-side memos (__clicksWant, __driverWant) that are set at request time and used for the early return. __clicks/__driver stay as the applied state inside the closure. Test in tests/test_targetframes.lua (and petframes): force InCombatLockdown, toggle clickToTarget false then true, call OnLeaveCombat, and assert *type1 == 'target'. Mark it `-- red under: compare against btn.__clicks`.  
  *Rule:* events-frames-taint-§2  
  *Planned in:* PF-03
- **PartyFrameEnhanced-R-16** `info` (review F-016; corrected) — Movable named holder and stand-in frames are not excluded from the client's layout cache  
  *Where:* modules/Anchor.lua:232, :257-262; modules/StandIn.lua:152-160  
  *Evidence:* StartMoving marks a frame as user-placed, so the client persists its position in layout-local.txt beside the addon's own stored position. After Reset position, the two can disagree. Not verified in the client.  
  *Remediation:* Optional hygiene (C-008 / T-11): add a presence-guarded `if frame.SetDontSavePosition then frame:SetDontSavePosition(true) end` after holder:SetMovable (Anchor.lua:257) and f:SetMovable (StandIn.lua:153), so the client stops writing cache entries the addon always overrides. Verify in-game only by checking layout-local.txt, since the visible position is already the addon's. Cite no standards clause, because none requires it.  
  *Rule:* compat  
  *Planned in:* PF-16


### C29 — WhatGroup popup combat taint and visibility

Reopening a soft-hidden popup in combat calls protected Hide() on the secure teleport button, and preparePopup restores the popup's alpha before the visibility gate runs. No test covers ShowFrame against a soft-hidden popup. Single-repo theme in WhatGroup's modules/Frame.lua.

**WhatGroup**

- **WHATGROUP-R-01** `high` (review F-001; confirmed) — Reopening a soft-hidden popup in combat with no capture calls protected Hide() on the secure teleport button (ADDON_ACTION_BLOCKED)  
  *Where:* modules/Frame.lua:852, modules/Frame.lua:888-893, modules/Frame.lua:1014, modules/Frame.lua:947  
  *Evidence:* PopulateFields' no-capture branch calls fields.teleportBtn:Hide() (SecureActionButtonTemplate child) unguarded; ShowFrame's combat defer (:1014) only covers a popup not shown, so an alpha-0 soft-hidden popup passes through. Reachable via minimap ToggleFrame in combat after Close/gate-hide with no pending capture. Scratch repro recorded mock.blocked = {"<anonymous>:Hide()"}. The already-hidden variant is unverified headlessly (smoke S-001). No test coverage (F-006).  
  *Remediation:* C-001: route the not-info branch through ConfigureTeleportButton(fields.teleportBtn, fields.teleportIcon, nil), which already defers under lockdown; add a file-scope NO_CAPTURE sentinel so deferTeleportUntilCombatEnds can stash nil and the replay passes nil back. teleportNote:Hide() stays direct. Add red-first test 'frame: reopening a soft-hidden popup in combat with no capture never Hides the secure button'. Move inventory/badge in same commit. Confirm in client via S-001.  
  *Rule:* events-frames-taint-§2  
  *Planned in:* WG-03
- **WHATGROUP-R-02** `medium` (review F-002; corrected) — preparePopup restores alpha of a soft-hidden popup before the visibility gate; 'Only out of combat' popup reappears mid-fight and cannot be closed by launcher/Escape  
  *Where:* modules/Frame.lua:888, modules/Frame.lua:148-151, modules/Frame.lua:1045, modules/Frame.lua:284-286, modules/Frame.lua:1076, settings/Panel.lua:276  
  *Evidence:* ApplyFrameAlpha does f:SetAlpha(masterAlpha()) with no softHidden knowledge and runs unconditionally in preparePopup; gate asked later. Repro (visibility=outOfCombat): AFTER PULL shown=true alpha=0; AFTER SHOW alpha=1; TOGGLE returned=false alpha=1. /wg show, chat link, minimap, /wg set alpha all reveal it; onScreen() lies so ToggleFrame and ESC fail until combat ends.  
  *Remediation:* As proposed (C-002): ApplyFrameAlpha sets f:SetAlpha(softHidden and 0 or masterAlpha()), with the softHidden/pendingHide declarations hoisted above :148. Also correct the title and the evidence: the footer Close button still dismisses the popup; only the launcher toggle and Escape fail.  
  *Rule:* events-frames-taint-§2; standalone-windows  
  *Planned in:* WG-04
- **WHATGROUP-R-06** `medium` (review F-006; confirmed) — No test exercises ShowFrame against a soft-hidden popup (no-capture and gate-declined branches)  
  *Where:* tests/test_frame.lua:684  
  *Evidence:* 90 cases, 28 name combat; closest (:684) covers only capture-exists and gate-allows. Both High findings (F-001, F-002) sit on untested paths the inventory reads as covered.  
  *Remediation:* Closed by the C-001/C-002 red-first cases: 'frame: reopening a soft-hidden popup in combat with no capture never Hides the secure button', 'frame: a gate-declined reopen in combat leaves a soft-hidden popup at alpha 0, and the launcher still closes it', 'frame: an alpha write while soft-hidden does not reveal the popup', each with a -- red under: comment.  
  *Rule:* testing-§12  
  *Planned in:* WG-03, WG-04


### C30 — Options reset semantics (options-ui-§12/§13)

Reset controls disagree on scope (page, tab or profile), a reset empties data without announcing it, a destructive retention change has no confirm, and a color validator stores the dbDefaults table itself. Affects BankLedger, ConsumableMaster, LootHistory and PrettyChat.

**BankLedger**

- **BankLedger-R-03** `medium` (review F-003; confirmed) — 'Reset all settings' empties the ledger without announcing LedgerChanged; History, Insights, the session window and the storage read-out keep showing deleted rows  
  *Where:* settings/Slash.lua:184-196; core/Database.lua:575-577; modules/Insights.lua:1000; modules/Browser.lua:1185-1193; modules/SessionWindow.lua:668; settings/Panel.lua:170  
  *Evidence:* The wipe replaces g.ledger with {} and sends only SETTINGS_CHANGED 'reset'. The four consumers refresh only on LEDGER_CHANGED or ENTRY_ADDED. Whether refreshAfterReset reaches the storage read-out is unverified.  
  *Remediation:* C-02: call NS.Database:FireLedgerChanged() after the wipe. Database stays the single sender, so there is no direct bus send from Slash. Add a test_panel case 'ResetEverything announces LedgerChanged exactly once' (+1, cumulative 1021). Smoke test C-02.  
  *Rule:* architecture-§4 (one sender per message); debug-logging-§10; options-ui-§12  
  *Planned in:* BL-04
- **BankLedger-A-02** `medium` (audit BL-34; confirmed) — The global reset is two acts behind three controls: Reset all settings wipes everything, while Defaults, the Blizzard footer and /bl resetall keep history; the session-only state.debugConsole is not swept  
  *Where:* settings/Slash.lua:161-197,513-523; settings/Panel.lua:696-705; settings/Schema.lua:326-333; docs/ARCHITECTURE.md:505; README.md:88-96,148; tests/test_panel.lua  
  *Evidence:* Reset all settings runs KA0S_BANKLEDGER_RESETALL, which calls Sl:ResetEverything and wipes db.global, ledger included. P:RestoreDefaults (the page Defaults and footer OnDefault) and /bl resetall run Sl:CliResetAll, a schema walk that keeps the ledger. ResetEverything ends testMode but not state.debugConsole. The register row's trigger 're-check at next release' fired when 1.1.0-release was tagged on 2026-09-11 (243dfab). This is the only player-reachable audit finding.  
  *Remediation:* Owner decision first (S2-0). Option A, unify up (recommended, the only compliant end state): route P:RestoreDefaults, the footer and resetall through a shared Sl:RequestResetAll() that shows the confirm-gated popup and whose OnAccept runs ResetEverything. Restore state.debugConsole and state.testMode by name without per-row [Set] lines, and keep minimap. Drop CliResetAll's partial behavior (/bl purge already covers history-only). Write characterization tests first, then blast-radius tests including the footer route. Reword README Usage and Troubleshooting, add a Version History line, and delete the ARCHITECTURE:505 row. Option B, unify down: needs a new register row with a real trigger. Not recommended. Interacts with R-02 and R-03, which fix the same ResetEverything body.  
  *Rule:* options-ui-§12  
  *Planned in:* BL-05

**ConsumableMaster**

- **ConsumableMaster-R-02** `medium` (review F-002; confirmed) — The color validator returns value without copying, so /cm reset <color> stores the dbDefaults table itself; a later profile switch empties the shipped default  
  *Where:* settings/Panel.lua:920-923; settings/Panel.lua:321-335; settings/Slash.lua:530-533; libs/LibKa0s/OptionsCompose.lua:171; libs/AceDB-3.0/AceDB-3.0.lua:462  
  *Evidence:* This is the only table validator that does not copy (order and map do; see :929). A probe showed 'stored IS dbDefaults table = true'. Against the real vendored AceDB, SetProfile's removeDefaults nils every channel, leaving the defaults color with 0 entries. For the rest of the session the swatch reads opaque black and /cm get reports fallbacks. The Macro Bar Defaults button is unaffected because it uses CopyTable.  
  *Remediation:* C-02: the color validator returns a shallow copy (local out = {}; copy the pairs; return out), with a comment explaining why. Add red-first cases: 'resetting a color row stores a copy', and 'a profile switch after a color reset leaves the shipped default intact' (#defaults == 4). The second depends on the mock fix in F-006.  
  *Rule:* savedvariables-§2; options-ui-§1; architecture-§5; testing-§12  
  *Planned in:* CM-03
- **ConsumableMaster-R-08** `low` (review F-008; confirmed) — The /cm resetall help text understates a whole-profile reset, and its two doors (popups, combat guard, refresh) diverge  
  *Where:* settings/Slash.lua:231; core/ConsumableMaster.lua:558-560, 571-580; core/SlashCommands.lua:41-61; settings/General.lua:107-118, 146-159  
  *Evidence:* The help says 'Reset every priority list and stat override', but the act is db:ResetProfile(). KCM_CONFIRM_RESET and KCM_RESET_ALL are duplicate popups. Only the panel door combat-guards and refreshes, yet a comment claims 'the two doors cannot diverge'.  
  *Remediation:* C-07: reword the help to 'Reset this profile to the addon's defaults — every setting and list (asks first)'. KCM.ResetAllToDefaults refuses in combat (returns false, 'combat'). doResetAll drops its own guard. The OnAccept handler distinguishes combat from DB not ready. Optionally collapse to one popup. Add a combat-refusal case for both doors.  
  *Rule:* options-ui-§12  
  *Planned in:* CM-11
- **ConsumableMaster-R-09** `low` (review F-009; confirmed) — The 'Reset all priorities' tooltip points to a 'Reset all settings above' button that is on another tab  
  *Where:* settings/General.lua:367; settings/General.lua:242, 353-370  
  *Evidence:* The button is on the Maintenance tab, and Reset all settings is on Master controls.  
  *Remediation:* C-08: change the wording to '...use Reset all settings on the Master controls tab.' Update locales/enUS.lua and the test_locale pin if either exists.  
  *Rule:* options-ui-§12  
  *Planned in:* CM-11

**LootHistory**

- **LootHistory-R-04** `medium` (review F-004; corrected) — Shortening 'Keep history for' deletes history immediately with no confirm  
  *Where:* settings/Schema.lua:370-375, settings/Slash.lua:8-18, core/LootHistory.lua:81-84  
  *Evidence:* The settings.retentionDays onChange calls NS.Database:PruneOld() directly. A mis-click in the dropdown, or /lh set settings.retentionDays 7, irreversibly drops older records in the same action. /lh purge, by contrast, goes through the KA0S_LOOTHISTORY_PURGE confirm. No test pins this onChange today.  
  *Remediation:* Keep the Schema:Set write (architecture-§5). Add Database:CountOlderThan(days) and do nothing when it is 0. Otherwise show a KA0S_LOOTHISTORY_PRUNE StaticPopup naming N, following the house pair: Yes/No, timeout=0, whileDead, hideOnEscape. Accept runs PruneOld. Decline should restore the previous retention value through Schema:Set, so that declining actually protects the records, and print one line saying so. Headless, or with no StaticPopup_Show, keep the immediate prune. Add tests in tests/test_schema.lua for popup present (no prune before accept, and decline restores) and popup absent (prunes). Update docs/settings-panel.md. Drop the options-ui-§12 rule_ref; there is no standards rule behind this.  
  *Rule:* options-ui-§12 (confirm style)  
  *Planned in:* LH-04

**PrettyChat**

- **PRETTYCHAT-A-02** `medium` (audit PC-81 (PRETTYCHAT-C-02); confirmed) — Categories page Defaults button (and Blizzard footer forward) resets only the selected tab; the rule requires page-wide  
  *Where:* settings/Panel.lua:738, settings/Panel.lua:752-754, README.md  
  *Evidence:* defaultsOnClick calls PrettyChat:ResetCategory(activeCategory(ctx)). The tooltip reads 'Reset the strings on the selected category tab to their defaults.' options-ui-§13: its blast radius MUST NOT narrow to the visible tab. The README documents the narrow behaviour, but there is no register row.  
  *Remediation:* Owner decision. (a) Make it page-wide per the rule: one Schema.ResetRows batch over all eight categories' rows, one [Set] reset Categories line, a new tooltip key (old key removed), an optional confirmation popup, and README/settings-panel.md/schema.md:158/smoke tests updated in the same commit. Or (b) ratify it with a Documented deviations row keyed options-ui-§13 (trigger: an options-ui revision naming a per-tab reset control, or the category tabs becoming one schema group). Extend the test_panel Defaults case to assert the chosen scope and that the footer OnDefault forwards to it.  
  *Rule:* options-ui-§13  
  *Planned in:* PC-06
- **PRETTYCHAT-A-21** `low` (audit PC-96 (PRETTYCHAT-C-17); corrected) — General subcategory draws no Defaults button; the standard is descriptive rather than explicit  
  *Where:* settings/Panel.lua:722, docs/settings-panel.md:79, modules/Override.lua:332  
  *Evidence:* defaultsButton = false. options-ui-§5's header describes a Defaults button on subcategories, and slash-commands-§2 assumes every schema page has one. The omission is recorded only as a redundancy call, with no register row. Graded as a contract gap, not a MUST.  
  *Remediation:* No upstream ruling is needed, because options-ui-§5 (lines 111/114) already requires the button. On the General sub-page, set defaultsButton = true with a defaultsTooltip. Point defaultsOnClick at the same reset-all implementation, with its confirm popup, that the in-body Reset all settings control and /pc resetall use (options-ui-§12, options-ui.md:260), rather than at a General-only ResetCategory. The minimap-hide allow-list must survive that path (launcher-§3), so keep test_launcher asserting it through the real button. Update docs/settings-panel.md:79. The alternative is to keep the omission and record a documented-deviation register row in ARCHITECTURE.md.  
  *Rule:* options-ui-§5; slash-commands-§2; launcher-§3  
  *Planned in:* PC-06


### C31 — Printer pre-formatting and chat fallbacks

Chat call sites pre-format with '..' or :format before calling the shared printer (events-frames-taint-§8), and register row counts have drifted. Dead DEFAULT_CHAT_FRAME and _G.print fallbacks hand-write the chat tag, and debug calls build their message before NS.Debug. Affects AbsorbTracker, BankLedger, KickCD, LootHistory and WhatGroup.

**AbsorbTracker**

- **AbsorbTracker-A-16** `low` (audit AT-78; confirmed) — Three pre-formatted chat lines fall outside the events-frames-taint-§8 register row's scope, and the row's count has drifted from 18 to 17  
  *Where:* core/DebugLogSetup.lua:47, core/Lifecycle.lua:173, settings/UnitPanel.lua:409, docs/ARCHITECTURE.md (events-frames-taint-§8 register row)  
  *Evidence:* The three sites are NS.Print("debug logging " .. ...), NS.Print(("%s: %s"):format(addonName, ...)) and NS.Print(("Unit panel render failed: %s"):format(...)). None formats a protected value. The row names only Slash.lua and Schema.lua, and the recorded grep now counts 17 there, not 18. This is a SHOULD.  
  *Remediation:* C8/S1.3: pass the parts to the printer instead, as NS.Print('debug logging', state), NS.Print(addonName..':', holds) and NS.Print('Unit panel render failed:', err). Correct the row count to the re-measured figure (17). The alternative is to widen the row to name the three files.  
  *Rule:* events-frames-taint-§8  
  *Planned in:* AT-19
- **AbsorbTracker-R-08** `low` (both F-012; AT-81; confirmed) — Dead DEFAULT_CHAT_FRAME fallback in the schema chatPrint hand-writes the chat tag '\|cFF00FFFF[AT]\|r'  
  *Where:* settings/Schema.lua:233-239 (:237), core/CoreSetup.lua:67, core/CoreSetup.lua:106, core/Namespace.lua:10  
  *Evidence:* The branch is 'elseif DEFAULT_CHAT_FRAME then DEFAULT_CHAT_FRAME:AddMessage("\|cFF00FFFF[AT]\|r " .. line)'. NS.Print is defined on both arms of CoreSetup, which loads first, so the branch can never run. It is a dead second copy of NS.PREFIX that §4 forbids.  
  *Remediation:* C-11 / C11 / S1.5: replace it with local function chatPrint(line) NS.Print(line) end, resolved at call time so suites can still spy on it. Delete the elseif arm.  
  *Rule:* slash-commands-§4  
  *Planned in:* AT-18

**BankLedger**

- **BankLedger-A-16** `info` (audit BL-51; confirmed) — Eight printer call sites pre-format with '..' or :format (outside the secret trigger set)  
  *Where:* modules/LedgerTable.lua:1074,1080; settings/Schema.lua:677,691; settings/Slash.lua:51,62,316,395  
  *Evidence:* All format addon-owned counts, labels and verbs, so no secret can reach them. SHOULD NOT drift, not a defect.  
  *Remediation:* O-1 (optional): when next touching these files, pass argument lists (print("blacklist cleared", n, ...)) instead of pre-formatted strings. No schedule.  
  *Rule:* events-frames-taint-§8  
  *Planned in:* BL-17

**KickCD**

- **KICKCD-A-05** `low` (audit KICKCD-A-08; confirmed) — Three unreachable 'or _G.print' fallback arms remain  
  *Where:* core/KickCD.lua:127, core/Compat.lua:441, modules/Cooldowns.lua:661  
  *Evidence:* `self.Util and self.Util.print or _G.print` and similar. CoreSetup defines Util.print on both paths, but the rule forbids the global print at any site. Carried over from the prior audit.  
  *Remediation:* D4/Sprint 2.5: add a test_source_style case scanning authored files (derived from git ls-files) for 'or _G%.print' and see it red. Then change all three sites to NS.Util.print / self.Util.print.  
  *Rule:* events-frames-taint-§8  
  *Planned in:* KC-21

**LootHistory**

- **LootHistory-A-21** `info` (audit LH-77; confirmed) — Six chat lines pre-format their arguments before the shared printer  
  *Where:* settings/Slash.lua:40, settings/Slash.lua:51, settings/Slash.lua:62, settings/Slash.lua:76, settings/Schema.lua:785  
  *Evidence:* The lines use ('...%d...'):format(n, ...) and 'test mode ' .. (on and 'on' or 'off') before NS.Print. All format addon-owned values, so none can meet a secret. SHOULD NOT.  
  *Remediation:* When these lines are next touched, pass the values as print(...) arguments instead of formatting first (optional).  
  *Rule:* events-frames-taint-§8 (SHOULD NOT)  
  *Planned in:* LH-25

**WhatGroup**

- **WHATGROUP-R-05** `low` (both F-005 / WG-69; corrected) — 16 NS.Debug call sites build the message (concatenation/tostring) before the call  
  *Where:* core/Database.lua:43; core/WhatGroup.lua:506, 786, 818, 832, 885, 916-918, 973, 1026, 1096; modules/Frame.lua:425-427, 504-507, 890-892, 1050-1051; settings/Schema.lua:398, 465  
  *Evidence:* debug-logging-§4 MUST NOT build the message before the call. E.g. NS.Debug("LFG", "appID=" .. tostring(appID) .. " status=" .. tostring(newStatus)) allocates on every LFG_LIST_APPLICATION_STATUS_UPDATED with debug off; values bypass the sink's safeToString. Census: 16 of 39 NS.Debug lines (17th hit settings/OptionsSetup.lua:188 is a vararg false positive). Review graded Medium, audit Low (not per-frame). The ratified events-frames-taint-§8 register row lists these sites for secret safety but does not cover §4.  
  *Remediation:* C-005 / 04 §3: rewrite to NS.Debug(tag, "fmt %s", a, b) passing raw values; split the modules/Frame.lua:890 ternary into two calls (or %s of a constant literal); keep wording byte-identical (pinned [Set] line). Characterization first: confirm each rewritten line is pinned in test_debuglog/test_capture, add pins if missing. Re-run census to 0 (except the vararg false positive). Afterwards amend the events-frames-taint-§8 register row (ARCHITECTURE.md:504) since the pre-formatting half no longer describes the tree. Optional: zero-allocation-when-off test per busiest path. Smoke S-005.  
  *Rule:* debug-logging-§4 (MUST NOT)  
  *Planned in:* WG-16


### C32 — Localization of player-visible strings

Player-visible acknowledgements and errors are raw English or use the wrong key, and confirmations use custom sentences instead of the set-shape echo. Some locale keys are dead or duplicated, and LibKa0s registers a font without a langmask. Affects AuraMaster, ConsumableMaster, LibKa0s, MultiMeters, PartyFrameEnhanced and WhatGroup.

**LibKa0s**

- **LibKa0s-R-04** `medium` (review F-004; confirmed) — Media.RegisterLSM registers JetBrains Mono without a langmask (refused on ruRU/CJK) but still counts it; comment wrong  
  *Where:* LibKa0s/Media.lua:274-275; LibKa0s/Media.lua:251-258  
  *Evidence:* LSM refuses a font with no langmask on non-Western clients (LibSharedMedia-3.0.lua:247-249 returns false); call passes no mask and ignores return, so on ruRU/koKR/zhCN/zhTW the face is never registered while count reports 1. Comment claims identical triples cost nothing, but each consumer registers a different path; first registration wins.  
  *Remediation:* C-04 (Media minor 3->4): pass LSM.LOCALE_BIT_western + LSM.LOCALE_BIT_ruRU as langmask; count a font/statusbar only if LSM:IsValid(type, name) after registering; rewrite the comment (first registration wins; every consumer's path names identical bytes). Test with fake non-western LSM in tests/test_media.lua. Smoke S-004 (ruRU + enUS).  
  *Rule:* library-stack-§8  
  *Planned in:* LK-13

**AuraMaster**

- **AuraMaster-A-09** `low` (audit AM-13; confirmed) — Four library-missing lines join two routed locale fragments instead of one placeholder sentence (recurs, narrower)  
  *Where:* core/CoreSetup.lua:72; core/DebugLogSetup.lua:19; core/LauncherSetup.lua:50; core/PerfSetup.lua:24  
  *Evidence:* NS.LIBKA0S_MISSING .. ', ' .. NS.L['so ... is unavailable.']. The neighbouring sites settings/OptionsSetup.lua:194 and settings/Slash.lua:361 already route the whole sentence with %s.  
  *Remediation:* Use L['%s, so ... is unavailable.'] (and '%s; running on reduced built-in fallbacks.') through Printf or format at all four sites. Add the keys to locales/enUS.lua and remove the old fragment keys; tests/test_locale.lua enforces no dead keys.  
  *Rule:* localization-§1 (routing SHOULD)  
  *Planned in:* AM-18
- **AuraMaster-A-10** `low` (audit AM-29; confirmed) — enable/disable/lock/unlock confirm with custom sentences instead of the set-shape key = value echo  
  *Where:* settings/Slash.lua:191-195 (runEnabled, :194); settings/Slash.lua:282-285 (runLock, :284)  
  *Evidence:* The writes go through NS.SetByPath, which is correct, but the confirmations print 'Aura Master enabled' and similar, where slash-commands-§5's set shape wants 'enabled = true'.  
  *Remediation:* Print the stored value through the dispatcher's key/value formatter (cli:CliGet('enabled') or the library's exported FormatKV, whichever LibKa0s-Slash-1.0 v1.55.0 publishes), so the echo is 'enabled = true' / 'locked = false'. Drop the prose sentence, or keep it as one extra line if the owner wants. Update the test_slash_verbs and test_disabled step-7 expectations. If no formatter is published, request it upstream in LibKa0s.  
  *Rule:* slash-commands-§2 / §5 / §8 (confirmation SHOULD)  
  *Planned in:* AM-12

**ConsumableMaster**

- **ConsumableMaster-R-12** `low` (review F-012; confirmed) — /cm enable and /cm disable print two lines in two vocabularies ('Master enable ON\|OFF' plus 'enabled = true\|false')  
  *Where:* settings/General.lua:249; settings/Slash.lua:116-117; libs/LibKa0s/OptionsCompose.lua:473  
  *Evidence:* A probe of /cm disable printed both lines. Three surfaces name one switch three ways.  
  *Remediation:* C-11: drop the KCM.Say('Master enable ...') from the row onChange and keep the canonical echo. Update the test_locale registry in the same commit.  
  *Rule:* slash-commands-§5  
  *Planned in:* CM-10

**MultiMeters**

- **MultiMeters-R-10** `low` (review F-010; corrected) — Window commands answer with the wrong error string  
  *Where:* modules/WindowManager.lua:704; modules/WindowManager.lua:272; modules/WindowManager.lua:307; modules/WindowManager.lua:309; modules/WindowManager.lua:324; modules/WindowManager.lua:471-472; locales/enUS.lua:901  
  *Evidence:* /mm toggle <unknown> answers 'Setting not found: %s'. /mm window delete\|copy <unknown> answers 'No window is selected.' An empty rename answers the label L['Window name'].  
  *Remediation:* Same as C-07, with rule_ref cleared: this is not a localization-§2 deviation.  
  *Rule:* localization-§2  
  *Planned in:* MM-06
- **MultiMeters-R-11** `low` (review F-011; corrected) — Feature-verb acknowledgements are raw English strings, with a concatenated plural  
  *Where:* settings/Slash.lua:415; settings/Slash.lua:428; settings/Slash.lua:446-447; settings/Slash.lua:580; settings/Slash.lua:632-633; settings/Slash.lua:696-697  
  *Evidence:* These lines are unrouted, while the same file routes NS.L["No window named '%s'."] at :574. The plural is built by concatenation.  
  *Remediation:* C-08: route the cited lines through NS.L with whole-sentence English keys and format placeholders, using two keys for the 1/N windows plural. Do the same for the other unrouted user-facing lines in settings/Slash.lua (:193, :207, :232, :367, :556, WINDOW_USAGE). Add every key to locales/enUS.lua and leave no enUS key unread. Cite localization-§1 (routing SHOULD), not §2/§3. Smoke test SM-09.  
  *Rule:* localization-§2; localization-§3  
  *Planned in:* MM-22

**PartyFrameEnhanced**

- **PartyFrameEnhanced-R-14** `low` (both F-014, PFE-18; corrected) — Dead locale keys ('Position' and the old '/pfe %s does nothing while the addon is off' refusal) plus two near-duplicate key pairs  
  *Where:* locales/enUS.lua:31, :150, :134-136; settings/Slash.lua:107,109; settings/General.lua:200,202; tests/test_optionssetup.lua:88  
  *Evidence:* 209 keys scanned. The :150 refusal key has no reader (both bundles). 'Position' is read only by a negative test (audit). The review's scan also found near-duplicates: 'All settings reset to defaults' vs '...defaults.', and the same split for 'Cannot reset settings…'. A player can see the wording drift.  
  *Remediation:* Delete the dead 'Position' and '/pfe %s does nothing while the addon is off …' keys (localization-§1: no key nothing reads). Collapse each near-duplicate pair to one spelling. No-trailing-period is the recommended choice for consistency with the collection's chat lines, but it is a preference, since slash-commands-§4 only forbids trailing colons. Delete the twin and point settings/General.lua:200/202 at the kept key. Optionally add a dead-key guard in tests. Sequence after PFE-17 as planned.  
  *Rule:* localization-§3, localization-§1, slash-commands-§4  
  *Planned in:* PF-15
- **PartyFrameEnhanced-A-09** `low` (audit PFE-05; confirmed) — Provider labels and the DebugLog degraded-stub strings are not localized (recurring, narrowed)  
  *Where:* modules/Providers.lua:96,119,138; settings/Slash.lua:196; core/DebugLogSetup.lua:40,54  
  *Evidence:* The labels 'EllesmereUI', 'Blizzard (raid-style)' and 'Blizzard (classic)' are printed by /pfe status. The stub has 'debug logging …' and 'Debug console'. There is no English-only register row (#9 is triaged). SHOULD.  
  *Remediation:* Audit Sprint 2.3: wrap the three labels in L[...] at definition, route the stub's two strings through NS.L, and add the keys to locales/enUS.lua (state 1, Routed).  
  *Rule:* localization-§1, localization-§3  
  *Planned in:* PF-15

**WhatGroup**

- **WHATGROUP-R-10** `low` (review F-010; confirmed) — Locale key with no reader, and locale header describing strings that no longer exist  
  *Where:* locales/enUS.lua:119-123, locales/enUS.lua:19-35  
  *Evidence:* L["WhatGroup is disabled — \|cffFFFF00/wg enable\|r turns it back on"] has no reader (refusal is LibKa0s-Slash's since minor 13, settings/Slash.lua:90-98); header calls such keys a defect, lists the disabled refusal as routed, and cites a nonexistent "Settings layer not ready yet" diagnostic.  
  *Remediation:* C-008: delete the dead key and its comment (:119-123); correct the header to say the refusal is LibKa0s-Slash's DISABLED_LINE_FORMAT and drop the 'Settings layer not ready yet' example.  
  *Rule:* localization-§3  
  *Planned in:* WG-19


### C33 — Hard-coded brand, folder names and non-catalog marks

Brand strings and addon folder names are typed as literals beside their single source. Blizzard atlases and textures are used where the LibKa0s catalog ships a mark (library-stack-§8). Affects AbsorbTracker, BankLedger, ConsumableMaster, KickCD, LootHistory, PartyFrameEnhanced and WhatGroup.

**AbsorbTracker**

- **AbsorbTracker-R-10** `low` (review F-009; confirmed) — Second literal of the brand string: PARENT_TITLE duplicates C.BRAND  
  *Where:* settings/OptionsSetup.lua:26, core/Constants.lua:67, core/Constants.lua:75  
  *Evidence:* local PARENT_TITLE = "Ka0s Absorb Tracker" duplicates C.BRAND, whose comment claims 'there is exactly one of it'. The two strings can drift on the next rename.  
  *Remediation:* C-08: set local PARENT_TITLE = NS.Constants.BRAND (Constants loads earlier). Keep the local name. Smoke-check that the category still reads Ka0s Absorb Tracker.  
  *Planned in:* AT-18

**BankLedger**

- **BankLedger-R-10** `info` (review F-010; corrected) — The brand name is spelled out twice beside NS.BRAND_NAME, which claims to be its one spelling  
  *Where:* core/LauncherSetup.lua:80,89,163; settings/OptionsSetup.lua:24  
  *Evidence:* tt:AddLine("Ka0s Bank Ledger", ...) at :163 and PARENT_TITLE = "Ka0s Bank Ledger" at OptionsSetup:24, while the header at :80 says 'THE BRAND NAME, IN THE ONE PLACE IT IS SPELLED'.  
  *Remediation:* C-06: tt:AddLine(NS.BRAND_NAME, 1, 0.82, 0) at core/LauncherSetup.lua:163 and local PARENT_TITLE = NS.BRAND_NAME at settings/OptionsSetup.lua:24. For core/CoreSetup.lua:34, which loads before NS.BRAND_NAME exists, either add a comment explaining the early literal or reword the LauncherSetup.lua:80 header so it no longer claims to be the only spelling. Rule ref: the addon's own single-spelling comment (naming hygiene), not launcher-§1. Smoke test C-06.  
  *Rule:* launcher-§1  
  *Planned in:* BL-18

**ConsumableMaster**

- **ConsumableMaster-R-17** `low` (review F-017; corrected) — The About page logo path hard-codes the ConsumableMaster folder name  
  *Where:* settings/Panel.lua:148  
  *Evidence:* Every other media path derives from addonName (core/LauncherSetup.lua:107-108). A renamed install folder draws no logo.  
  *Remediation:* C-15: in settings/Panel.lua:148 build the path from the namespace: local LOGO_TEXTURE = ('Interface\\AddOns\\%s\\media\\logos\\%s.logo.tga'):format(KCM.name, KCM.name:lower()). Alternatively capture the first vararg (`local addonName, NS = ...`) and use that. Cite it as consistency with core/LauncherSetup.lua:107-108, not as a layout-§4 deviation.  
  *Rule:* layout-§4  
  *Planned in:* CM-21

**KickCD**

- **KICKCD-A-14** `low` (audit KICKCD-C-13; corrected) — The Spells remove button uses the one-off Blizzard atlas transmog-icon-remove instead of a LibKa0s catalog mark  
  *Where:* settings/Spells.lua:798, settings/Spells.lua:590-622, libs/LibKa0s/Media.lua:94, libs/LibKa0s/Media.lua:97  
  *Evidence:* The catalog carries close, clear and cancel, which NS.Icon resolves. This is a cosmetic drift from the other Ka0s list editors.  
  *Remediation:* In rowRemoveButton (settings/Spells.lua:797-798), pass image = NS.Icon and NS.Icon('clear') (or 'close'), and keep atlas = 'transmog-icon-remove' only as the fallback when NS.Icon returns nil. The existing opts.image -> SetImage branch handles the path, so no new branch is needed. Put image ahead of atlas in makeRowIconBtn's if-chain. Optionally tint via SetVertexColor, since catalog marks are white-in-alpha. Rewrite the comment at Spells.lua:563-567 so it no longer says the atlas is required. Upstream work (a new 'remove' mark in LibKa0s tools/artwork, then a release and a re-vendor) only if neither clear nor close reads right.  
  *Rule:* library-stack-§8; AP #63  
  *Planned in:* KC-12

**LootHistory**

- **LootHistory-A-19** `low` (audit LH-76; confirmed) — Resize grip draws Blizzard UI-ChatIM-SizeGrabber where the LibKa0s catalog ships 'resize'  
  *Where:* modules/Browser.lua:1042-1048, libs/LibKa0s/Media.lua:103, libs/LibKa0s/media/icons/resize.tga  
  *Evidence:* The grip uses the Blizzard SizeGrabber textures. The catalog carries 'resize'. The choice is argued only in a comment at :1042-1046 (matching the collection's corner grabbers), with no register row.  
  *Remediation:* Either draw NS.Icon('resize') (tinted like the other title-bar marks, with a hover tint) with the Blizzard grabber as the fallback rung, or add a library-stack-§8 register row. Optional upstream: since the argument is collection-wide, propose in WowAddonStandards (standalone-windows / library-stack-§8) whether the resize grip is a catalog mark or the Blizzard grabber, which would close it for every addon at once. Not blocking; either local path closes it. Smoke S3 if the mark is adopted. This touches the same line as LootHistory-R-09 (Lock frame gating), so coordinate the two.  
  *Rule:* library-stack-§8 (MUST)  
  *Planned in:* LH-10

**PartyFrameEnhanced**

- **PartyFrameEnhanced-A-16** `info` (audit PFE-24; confirmed) — LOGO_PATH hand-types the folder name instead of deriving it from addonName  
  *Where:* core/Constants.lua:17; core/LauncherSetup.lua:47-48  
  *Evidence:* `C.LOGO_PATH = "Interface\\AddOns\\PartyFrameEnhanced\\media\\logos\\partyframeenhanced.logo.tga"`, while the launcher builds the same path from addonName.  
  *Remediation:* Audit Sprint 3.3, after PFE-20: `C.LOGO_PATH = "Interface\\AddOns\\" .. addonName .. "\\media\\logos\\" .. addonName:lower() .. ".logo.tga"`. Constants needs `local addonName, NS = ...` on line 1.  
  *Rule:* library-stack-§8 (observation)  
  *Planned in:* PF-21

**WhatGroup**

- **WHATGROUP-A-21** `info` (audit WG-80; confirmed) — Landing-page logo path hand-types the folder name  
  *Where:* settings/Panel.lua:87, settings/Panel.lua:14  
  *Evidence:* MAIN_LOGO_TEXTURE types "WhatGroup"; LauncherSetup builds its icon path from addonName per library-stack-§8; issue #17 (WHATGROUP-R-12) fixed the same pattern elsewhere in the file.  
  *Remediation:* Build it as ("Interface\\AddOns\\%s\\media\\logos\\%s.logo.tga"):format(addonName, addonName:lower()); addonName is bound at :14.  
  *Rule:* options-ui-§5; library-stack-§8  
  *Planned in:* WG-17


### C34 — Message-bus literals and the no-bus ruling

Tests type 'Ka0s_...' wire-name literals at SendMessage/RegisterMessage call sites instead of using constants. architecture-§4's bus MUST binds addons that have no bus, and its threshold is ambiguous (upstream). Affects BankLedger, ConsumableMaster, LootHistory, PrettyChat and WhatGroup.

**BankLedger**

- **BankLedger-A-14** `low` (audit BL-49; corrected) — Twelve 'Ka0s_...' wire-name literals at SendMessage/RegisterMessage call sites in six test files  
  *Where:* tests/test_database.lua:40,53,54; tests/test_lifecycle.lua:64; tests/test_mock.lua:312,313,315,320; tests/test_panel.lua:614; tests/test_schema.lua:36; tests/test_sessionwindow.lua:143,145; core/Constants.lua:281-289; tests/test_bus.lua:19-22  
  *Evidence:* Shipped code has none. A mistyped literal in a driver sends a message nobody receives, and the test then asserts on silence.  
  *Remediation:* S4-2: use NS.MSG.ENTRY_ADDED, LEDGER_CHANGED, SETTINGS_CHANGED and SESSION_CHANGED at every test site. That covers the 12 Register/Send calls, the paired UnregisterMessage calls (test_database 42,56,57; test_panel 618; test_schema 40), the msg comparison at test_database:276 and the __msgRegistry keys at test_lifecycle:86,92. Give test_mock's 'Ka0s_Scratch_Ping' a local constant so it appears once. Keep tests/test_bus.lua:19-22 as the single wire-name oracle. test_surface_parity:276, which checks the degraded MSG value, may compare against the oracle or NS.MSG from the live load. Re-run grep '"Ka0s_' tests/*.lua and expect only the oracle and the scratch constant.  
  *Rule:* architecture-§4 (constant at every call site)  
  *Planned in:* BL-15

**ConsumableMaster**

- **ConsumableMaster-A-13** `low` (audit CM-93; corrected) — The test-only bus literal Ka0s_ConsumableMaster_HarnessPing is typed at two call sites  
  *Where:* tests/test_harness.lua:73; tests/test_harness.lua:74  
  *Evidence:* These are the mandated grep's only hits outside core/Bus.lua. It is a mock-dispatch probe, not a catalog message.  
  *Remediation:* Declare `local PING = "Ka0s_ConsumableMaster_HarnessPing"` once at the top of the test case and use it at all three sites (:73, :74, :77). Alternatively, rename the probe to a string without the Ka0s_ prefix.  
  *Rule:* architecture-§4  
  *Planned in:* CM-22

**LootHistory**

- **LootHistory-A-09** `low` (audit LH-66; confirmed) — Nine bus-message string literals at Send/RegisterMessage call sites in tests  
  *Where:* tests/test_browser.lua:536, tests/test_browser.lua:552, tests/test_collector.lua:440, tests/test_collector.lua:444, tests/test_collector.lua:473, tests/test_harness.lua:145, tests/test_harness.lua:146, tests/test_panel.lua:232, tests/test_panel.lua:252  
  *Evidence:* The grep (Send\|Register)Message("Ka0s_ outside libs/ and tests/_kit/ finds 9 hits, all in tests. A typo'd literal would send to nobody and the case would pass vacuously. Production code has none.  
  *Remediation:* Use NS.MSG.RECORD_ADDED, HISTORY_CHANGED and SETTINGS_CHANGED. In tests/test_harness.lua, declare local PROBE = 'Ka0s_LootHistory_HarnessProbe' once. The literal assertions in tests/test_constants.lua stay. Re-run the grep and expect 0.  
  *Rule:* architecture-§4 (MUST)  
  *Planned in:* LH-23

**PrettyChat**

- **PRETTYCHAT-A-11** `low` (audit PC-102 (PRETTYCHAT-C-23); confirmed · upstream → WowAddonStandards) — architecture-§4 closed-message-bus MUST binds (a module registers game events), but there is no bus and no register row; the threshold is ambiguous  
  *Where:* modules/Override.lua:139, settings/Schema.lua:730-731, docs/ARCHITECTURE.md:139  
  *Evidence:* The §4 threshold is 'two or more feature modules, or any module that registers game events'. The ## Message Bus section justifies the absence with 'publishes no named message' and a re-check trigger at the first LibStub('AceEvent-3.0'), and neither is the rule's threshold. The clobber hazard cannot arise with one module and one private frame.  
  *Remediation:* Decide upstream together with PC-84 (Sprint 0.2). If WowAddonStandards narrows the event arm (to modules registering through a shared AceEvent target, or to a second receiver), rewrite the ## Message Bus sentence to cite it. Otherwise add a Documented deviations row keyed architecture-§4 (trigger: a second feature module or a second event-registering module). Do not adopt a bus.  
  *Rule:* architecture-§4  
  *Planned in:* WS-04, PC-12

**WhatGroup**

- **WHATGROUP-A-04** `low` (audit WG-57; confirmed · upstream → WowAddonStandards) — architecture-§4 bus MUST applies as written (addon registers game events) and there is no message bus; reopened  
  *Where:* core/WhatGroup.lua:294-302, docs/ARCHITECTURE.md:122-129, modules/Frame.lua  
  *Evidence:* Applicability clause binds 'any module that registers game events'; core registers four game events, Frame registers PLAYER_REGEN_ENABLED on two frames; modules talk by direct calls (ShowFrame, GetTeleportSpell, FrameStandDown). 2026-09-08 bundle treated it as sub-threshold using the rule's rationale. Previously rejected in triage as WHATGROUP-A-12.  
  *Remediation:* Recommended C: take the ambiguity upstream to WowAddonStandards (does an AceAddon shell's own event handling count as 'a module'?; name 'the addon object's own event handlers' explicitly); close against amended text. Fallback B: Documented deviations row citing architecture-§4 with re-check trigger 'a second feature module, or a second consumer of the join data'. Option A (minimal bus NS.MSG.JOIN_READY via LibKa0s-Bus with stand-down wiring and ## Message Bus docs) has cost and is not recommended.  
  *Rule:* architecture-§4 (MUST)  
  *Planned in:* WS-04, WG-23


### C35 — Hot-path allocation, throttles and redundant work

Hot paths allocate per-call table literals and closures and repeat parses and sorts; other waste includes full row rebuilds, no-op republishes and caches nothing reads. KickCD's scheduleTimer returns nil, which defeats the LibKa0s throttle because the library uses that return value as its armed flag (upstream). LibKa0s's own perf internals also need work: the O(n) DebugLog trim, metatable misses on the sampler path, and a Perf bracket left open by an error. Affects AbsorbTracker, BankLedger, KickCD, LibKa0s, LootHistory, MultiMeters, PartyFrameEnhanced, PrettyChat and WhatGroup.

**LibKa0s**

- **LibKa0s-R-10** `low` (review F-010; confirmed) — DebugLog buffer trims with O(n) table.remove(1) on every line at the cap  
  *Where:* LibKa0s/DebugLog.lua:623  
  *Evidence:* At the 1500-line MAX_BUFFER every Add shifts 1500 slots; only under debug logging.  
  *Remediation:* C-11 (DebugLog minor 12->13): ring buffer with head index; BufferSize/LastLine/FindLine/CopyText walk in order. D.buffer is public: grep consumers for .buffer; keep an ordered lazily-rebuilt view or fall back to batched trim (compact every 64). Characterization cases first (testing-§13), plus '1501st line drops the first'. Smoke S-008.  
  *Rule:* testing-§13  
  *Planned in:* LK-19
- **LibKa0s-R-11** `low` (review F-011; corrected) — Perf gate comment says 'no metatable' but instance has one; nil-initialized fields hit __index/__newindex every sampler frame  
  *Where:* LibKa0s/Perf.lua:400-401; LibKa0s/Perf.lua:404-405; LibKa0s/Perf.lua:424; LibKa0s/Perf.lua:940  
  *Evidence:* P.armed/P.recording/P.label are assigned nil so never raw keys; every onUpdate read calls the __index closure. P.on gate is raw so performance-§2 holds; cost small, only during perf runs.  
  *Remediation:* C-12 (Perf minor 12->13): initialize armed/recording/label as false (plain assignment works before setmetatable). Change every later nil write to false (Perf.lua:911, :921, :959, :1011, :1033, :1044) so the keys stay raw, and audit any '== nil' reads of these fields first. Rewrite the :400-401 comment: P.on is a raw field and the metatable exists only for 'suspended'. Keep the tests/test_perf_isolation.lua 0 KB pin green, and add a case asserting rawget(P,'recording') ~= nil after a window closes.  
  *Rule:* performance-§2  
  *Planned in:* LK-20
- **LibKa0s-R-16** `low` (review F-016; confirmed) — A Perf bracket left open by an error misattributes later brackets' observed parent for the rest of the run  
  *Where:* LibKa0s/Perf.lua:569-584; LibKa0s/Perf.lua:592  
  *Evidence:* openDepth only reset in P.Reset (from Start); a host raise between Open and Close leaves the slot open so later Close records the leaked key as observedWithin; window open/close doesn't reset.  
  *Remediation:* Part of C-12: reset openDepth = 0 in openWindow and closeWindow. Test in tests/test_perf_core.lua: leaked Open in window A does not parent a bracket in window B.  
  *Planned in:* LK-20

**AbsorbTracker**

- **AbsorbTracker-R-11** `low` (review F-010; confirmed) — Profile adopt runs a no-op Reevaluate() and double-publishes POSITION, APPEARANCE and REPAINT on an enable edge  
  *Where:* core/AbsorbTracker.lua:317-323, core/Lifecycle.lua:123-131  
  *Evidence:* SyncEnabledHold's lifecycle:Set already re-evaluates, so the next Reevaluate() is a no-op. On an off-to-on switch, StandUp publishes POSITION, VISIBILITY, APPEARANCE and REPAINT, and adoptProfile then publishes UNITS, POSITION, APPEARANCE and REPAINT again. That is two three-bar appearance passes (about 48 API calls each). Cold path.  
  *Remediation:* C-09: drop the Reevaluate(). Capture wasDown before SyncEnabledHold. Always send UNITS, and send POSITION, APPEARANCE and REPAINT only when the latch did not just stand up. First add a characterization test pinning APPEARANCE deliveries for a same-state switch and an off-to-on switch (test_disabled step 9 or test_database), then assert the off-to-on count drops from 2 to 1. Serialize with the R-07 edits to core/AbsorbTracker.lua.  
  *Rule:* testing-§13  
  *Planned in:* AT-05

**BankLedger**

- **BankLedger-R-09** `low` (review F-006; confirmed) — Util.ApplyVisibility (and ApplyMasterChrome) allocate a table literal per call/combat edge while docs/performance.md claims 'No allocation'  
  *Where:* core/Util.lua:240,274-288; docs/performance.md:46  
  *Evidence:* pairs({ Browser = NS.Browser, SessionWindow = NS.SessionWindow }) builds a table on every call, including in the default 'always' mode, twice per fight. The exemption's evidence page says 'No allocation, no scan, no timer.'  
  *Remediation:* C-04: use module-level name lists, local VISIBILITY_OWNERS = {"Browser","SessionWindow"} and {"Browser","SessionWindow","Export"} for ApplyMasterChrome, iterated with ipairs and NS[key] resolved at call time. This is a pure refactor with deterministic order, and performance.md:46 becomes true. Smoke test C-04.  
  *Rule:* performance-§12 (sweep must be true); anti-patterns #52 (not applicable)  
  *Planned in:* BL-13

**KickCD**

- **KICKCD-R-04** `medium` (review F-004; confirmed) — scheduleTimer returns nil (C_Timer.After), so the LibKa0s color-picker and slider throttle never engages  
  *Where:* settings/OptionsSetup.lua:243  
  *Evidence:* `scheduleTimer = function(fn, delay) return _G.C_Timer.After(delay, fn) end`. The library uses the return value as its armed flag (libs/LibKa0s/OptionsWidgets.lua:1471-1482), so every ~60 Hz drag tick schedules its own SetAndRefresh and CONFIG_CHANGED fan-out. No test pins the throttle's call count.  
  *Remediation:* C-04: `return _G.C_Timer.NewTimer(delay, fn)`. Test: drive the color widget's OnValueChanged 10 times inside one mock window and assert one SetAndRefresh. Independent of U-001 and can land early; U-001 makes it belt-and-braces.  
  *Planned in:* KC-10
- **KICKCD-R-19** `medium` (review U-001; confirmed · upstream → LibKa0s) — LibKa0s OptionsWidgets uses the host's scheduleTimer return value as its armed flag; nil-returning hosts defeat the throttle  
  *Where:* libs/LibKa0s/OptionsWidgets.lua:1326-1337, libs/LibKa0s/OptionsWidgets.lua:1471-1482, libs/LibKa0s/Options.lua:537-539  
  *Evidence:* The color throttle does `timer = d.scheduleTimer(...)` then `if timer then return end`, and the slider live-commit uses the same pattern. The Options.lua descriptor doc does not require a truthy handle. KickCD, LootHistory (settings/OptionsSetup.lua:205-207) and MultiMeters (settings/OptionsSetup.lua:270-272) all pass C_Timer.After wrappers that return nil.  
  *Remediation:* Upstream in LibKa0s: track armed in a library-local boolean set before calling d.scheduleTimer and cleared in the callback, and ignore the returned handle. Document in Options.lua that the return value is unused. Add a LibKa0s test with a nil-returning scheduleTimer asserting one commit per window. Bump the OptionsWidgets.lua LibStub minor (and Options.lua's if the file changes), update CHANGELOG, and tag. Then re-vendor the whole libs/LibKa0s and tests/_kit into KickCD and every consumer as its own commit, updating the CLAUDE.md provenance line; test_vendor_sync gates it. Never patch libs/ locally (library-stack-§7, #45/#48).  
  *Rule:* library-stack-§7; AP #45; AP #48  
  *Planned in:* LK-26

**LootHistory**

- **LootHistory-R-06** `low` (review F-006; corrected) — AH priority list re-parsed per record on every Stats/export pass; accumulateTime calls date() twice per record  
  *Where:* modules/AuctionPrice.lua:91-100, core/Util.lua:82-88, core/Database.lua:657, core/Database.lua:536-539, modules/Export.lua  
  *Evidence:* AuctionPrice:Pick calls cfg() and runs tag:match('^(.-):(.+)$') on each priority tag, up to 11 allocating matches per record. It is reached once per record in Database:Stats and 3-4 times per CSV row. accumulateTime calls date() twice per record, and date('*t') allocates a table. Both violate the loop-invariant hoist rule stated at core/Database.lua:307-313. Unverified: there is no perf runner or capture.  
  *Remediation:* Measure first with an uncommitted micro-benchmark over a large synthetic history, and act only if it shows a real cost. If it does, memoize tag parsing in a module-local table keyed by the tag string (tag -> prov, key). Tag strings are immutable, so this needs no invalidation, no bus target and no stand-down change. In Stats/Export, read cfg() once per call and pass the priority list to Pick (for example Pick(map, priority)). For accumulateTime, cache the day string per ts//86400 within one Stats call. Add a test that Pick honours a reorder after MovePriorityWithin. Drop the events-frames-taint-§7 rule_ref.  
  *Rule:* events-frames-taint-§7  
  *Planned in:* LH-19
- **LootHistory-R-16** `low` (review F-016; confirmed) — Loot hot path allocates a gate-config table on every CHAT_MSG_LOOT  
  *Where:* modules/Collector.lua:116-119  
  *Evidence:* A fresh { qualityThreshold = ..., ... } table is built per loot line. This matters in mass-loot bursts. Unverified: there is no perf runner.  
  *Remediation:* C-006 step 3: keep a module-level gateCfg table refreshed in RefreshUpvalues, and set gateCfg.itemID per call.  
  *Rule:* events-frames-taint-§7  
  *Planned in:* LH-18
- **LootHistory-R-18** `low` (review F-018; confirmed) — Login prune fires HistoryChanged even when it removed nothing  
  *Where:* core/Database.lua:796-798, core/Util.lua:230-235  
  *Evidence:* fireHistoryChanged() is unconditional. With the window open, that triggers about nine full-history passes 5 s after login for no change.  
  *Remediation:* C-006 step 4: fire only when removed > 0. Add a test that a zero-removal PruneOld sends no HistoryChanged, using a recorded-message spy that is first shown to record a positive send (red under an unconditional fire).  
  *Planned in:* LH-08

**MultiMeters**

- **MultiMeters-R-07** `low` (review F-007; corrected) — Every refresh releases and rebuilds every visible row, and Row:Update writes hidden cells  
  *Where:* modules/Window.lua:1168; modules/Window.lua:912-914; modules/Window.lua:1206-1220; modules/Row.lua:1446-1455; modules/Row.lua:1199-1204; modules/Row.lua:1376-1378  
  *Evidence:* HideAll releases the pool and Cell:Clear clears each cell. Rows are then re-acquired, re-anchored and refilled 4 times a second in combat. Capture 20260909-014604 (dated, solo): render 0.75 ms/pass, renderRow 0.10 ms/row. Offline refresh20x7 is 1.31 ms/iter. The saving is unmeasured.  
  *Remediation:* C-05 (measure first): keep self.slots bound across passes, acquire only when needed, release only the surplus, and re-anchor only when layoutVersion (bumped in ApplyConfig) changes. For Row:Update, make ApplyLayout keep an ordered array of live cells on the row (self.liveCells, rebuilt only in ApplyLayout, reusing the table rather than allocating a new one each call). Row:Update then iterates that array instead of pairs(self.cells). The alternative is to iterate layout.columns and index self.cells. Row.lua must stay at or under 1500 lines. Gate: before and after in-client /mm perf bundles (SM-07) with render ms/call lower. Offline refresh20x7 must keep API count at 8 and bytes/iter at or under 303438.1. Revert if render does not move.  
  *Rule:* performance-§2; performance-§9; layout-§1  
  *Planned in:* MM-20
- **MultiMeters-R-09** `low` (review F-009; confirmed) — Visibility:Evaluate runs the whole ladder to feed a LastResult cache that no shipped code reads  
  *Where:* modules/Visibility.lua:389-419; modules/Visibility.lua:373; modules/Visibility.lua:461-471; tests/test_visibility.lua  
  *Evidence:* Visibility.LastResult has zero callers in core/, modules/ or settings/. Only a test reads it. Each window's rules are evaluated twice per context edge, with a table allocated per changed result.  
  *Remediation:* C-06: return early from Evaluate when not State.debug, and delete Visibility.LastResult and its test (or wire it into /mm debug diag). Keep the subscriptions.  
  *Planned in:* MM-08

**PartyFrameEnhanced**

- **PartyFrameEnhanced-R-07** `low` (review F-007; corrected) — The zero-overhead perf scenario compares capture-off with capture-on instead of with instrumentation absent  
  *Where:* tests/perf.lua:226-240, :262  
  *Evidence:* `assert_(probeOff.bytesPerIter <= probeOn.bytesPerIter + 1, ...)` would pass a dormant bracket that allocates as much as an armed one. The probeOverheadOff ≤ 24 B ceiling only partly compensates. Today: off 0.0 B/iter, on 0.5 B/iter.  
  *Remediation:* Build a true 'absent' baseline and do not compare against castStartStop. Preferred: load a second environment where NS.Perf is pre-seeded so the bracket compiles to nothing, or where the bracket helpers are stubbed out, then measure castOnce there and assert probeOff.bytesPerIter <= absent.bytesPerIter + 1. Acceptable fallback: wrap debugprofilestop and NS.Perf.Note with call counters, assert 0 calls per iteration while Perf.on == false, and keep the existing ceiling. Add a comment explaining why this stands in for 'absent'. Add no wall-clock assertion. It stays a scenario outside docs/test-cases.md.  
  *Rule:* performance-§9, performance-§2, testing-§7  
  *Planned in:* PF-18

**PrettyChat**

- **PRETTYCHAT-R-09** `low` (review F-009 (change C-09); corrected) — Sorted per-category name list rebuilt at four sites; ApplyStrings allocates and sorts 8 tables per pass  
  *Where:* modules/Override.lua:283-287, modules/Override.lua:566-575, settings/Schema.lua:434-438, settings/Panel.lua:454-458  
  *Evidence:* NS.Defaults is static after load, yet four loops each rebuild and sort the names, which gives four places for the PC-16 ordering rule to drift. The cost is unmeasured (no tests/perf.lua, by exemption).  
  *Remediation:* Keep the remediation, with the rule_ref changed to none (plain maintainability/perf, no standard cited) instead of anti-pattern #55. Publish a memoized NS.SortedStringNames(category) in modules/Override.lua and return the cached array read-only, with a 'do not mutate' comment. collectNames must copy or filter into a new table rather than filter the cached one. Replace the other three loops. Label the perf benefit as unmeasured, and run the SMK-C09 diff to confirm the order is unchanged.  
  *Rule:* anti-pattern #55  
  *Planned in:* PC-11

**WhatGroup**

- **WHATGROUP-R-16** `low` (review F-016; confirmed) — Teleport configure allocates three fresh script closures per call  
  *Where:* modules/Frame.lua:403-456, modules/Frame.lua:411, modules/Frame.lua:416, modules/Frame.lua:423, modules/Frame.lua:444-449, modules/Frame.lua:516-523  
  *Evidence:* applyTeleportAction builds OnEnter/OnLeave/PreClick closures every configure; with resolveTeleportState's per-call table this is most of showFrameRepeat's 1872.5 B/iter. Once per popup show; hygiene.  
  *Remediation:* C-006: define onTeleportEnter/onTeleportLeave/onTeleportPreClick once at file scope reading btn.__wgSpellID/__wgSpellName from self; re-run tests/perf.lua, record new showFrameRepeat in docs/performance.md and lower the scenario ceiling (measured + 24) in the same change. Smoke S-006.  
  *Rule:* performance-§9  
  *Planned in:* WG-15


### C36 — Test-only exports and dead code on the production namespace

Production modules publish aliases and fields that only tests read, keep duplicated predicates or flows, write fields nothing reads, or publish non-idempotently. Some defaults are typed in several places. Affects AbsorbTracker, AuraMaster, ConsumableMaster, KickCD, PrettyChat and WhatGroup.

**AbsorbTracker**

- **AbsorbTracker-R-13** `low` (review F-013; confirmed) — Test-only aliases NS.bar, NS.statusBar, NS.valueText and NS.backdropInfo are published on the production namespace  
  *Where:* modules/Bar.lua:163-172, tests/test_display.lua, tests/test_data.lua, tests/test_slashcmds.lua  
  *Evidence:* The file's own comment says no production caller remains and only the tests read them. A mistaken production caller would lint and test clean.  
  *Remediation:* C-12: delete modules/Bar.lua:163-172. Preferred: replace the test reads with NS.bars.player.*. Alternative: define the aliases in tests/run.lua before the suites load. Run the full suite.  
  *Planned in:* AT-13

**AuraMaster**

- **AuraMaster-R-14** `low` (review F-014; corrected) — Two copies of the frame-pick flow (runPick / pickFrame), and a needlessly named global picker overlay  
  *Where:* settings/Slash.lua:303-317; settings/Layout.lua:217-232; modules/FramePicker.lua:88  
  *Evidence:* Both functions resolve the active container, refuse in combat, start FramePicker and make the same two SetByPath writes. Only the completion message and the panel re-open differ. The overlay is named 'AuraMasterFramePicker' and nothing reads that global.  
  *Remediation:* Add a shared NS.FramePicker.PickFor(id, onDone, onCancel) that owns the active-container resolve, the combat refusal and the two SetByPath writes. runPick and pickFrame pass only their completion and cancel behavior. Unnaming the overlay is optional. If it is done, expose a test seam (for example FP.__overlay()) and move tests/test_anchors.lua:569,588,598 off mocks.__globals.AuraMasterFramePicker in the same commit. Drop the events-frames-taint rule_ref.  
  *Rule:* architecture; events-frames-taint (global names)  
  *Planned in:* AM-20

**ConsumableMaster**

- **ConsumableMaster-R-16** `low` (review F-016; confirmed) — KCM.Settings.GENERAL_TABS is published with no reader; O.SetMacroTab is read only by tests  
  *Where:* settings/General.lua:383; settings/Category.lua:1106  
  *Evidence:* There are zero readers of GENERAL_TABS in core/, modules/, settings/ or tests/.  
  *Remediation:* C-14: delete KCM.Settings.GENERAL_TABS = TABS. Keep O.SetMacroTab as a deliberate test seam (informational).  
  *Planned in:* CM-20

**KickCD**

- **KICKCD-R-13** `low` (review F-013; corrected) — Three readers of the master 'enabled' path, one of which claims to be the only one; dead early returns in Cooldowns  
  *Where:* core/LifecycleSetup.lua:59, modules/Cooldowns.lua:298-302, modules/Cooldowns.lua:311, modules/Cooldowns.lua:408, core/Units.lua:33-37  
  *Evidence:* LifecycleSetup says it is 'THE one reader of the stored path', yet Cooldowns.isEnabled and Units.IsEnabled also read p.enabled. Cooldowns' Rebuild/Refresh early returns are dead under the latch.  
  *Remediation:* C-10: route all three module readers through NS.MasterEnabled(): Cooldowns isEnabled (:298), IconGrid isEnabled (:133), and Units.IsEnabled's first rung (:35). Keep the Cooldowns.MasterEnabled and IconGrid.MasterEnabled exports as aliases so callers don't break. Keep the early returns at Cooldowns.lua:311/:408 but comment them as defense-in-depth behind the latch, or drop them only if no test calls Rebuild/Refresh directly while disabled. After this change, LifecycleSetup's 'THE one reader' claim is true.  
  *Planned in:* KC-09

**PrettyChat**

- **PRETTYCHAT-A-19** `low` (audit PC-94 (PRETTYCHAT-C-15); corrected) — Defaults hard-coded in multiple places (global defaults in Database.lua; Master-controls defaults typed three times)  
  *Where:* core/Database.lua:34-39, settings/Schema.lua:119-120, modules/Override.lua:38, modules/Override.lua:72, settings/Schema.lua:212  
  *Evidence:* savedvariables-§2 says defaults/Profile.lua MUST be the only place a default is hard-coded. enabled=true and visibility='always' each appear in MASTER_SPEC.defaults, in the reader fallbacks and in the clearing arm.  
  *Remediation:* First write characterization tests for IsAddonEnabled and GetVisibility, plus a test that the global minimap default survives a reset. Declare NS.GlobalDefaults = { schemaVersion = 0, minimap = { hide = false } } and NS.GeneralDefaults = { enabled = true, visibility = 'always' } in defaults/Profile.lua, beside NS.ProfileDefaults. Do not add a new defaults/Global.lua, because savedvariables-§2 names defaults/Profile.lua as the declaration site. defaults/ loads after core/, so assemble Database.defaults.global from NS.GlobalDefaults at OnInitialize. Then read NS.GeneralDefaults from MASTER_SPEC.defaults, IsAddonEnabled, GetVisibility and the General.visibility set arm (Schema.lua:212). The enabled fallback should keep its `== nil` form (savedvariables-§5).  
  *Rule:* savedvariables-§2  
  *Planned in:* PC-14
- **PRETTYCHAT-A-20** `low` (audit PC-95 (PRETTYCHAT-C-16); confirmed) — settings/Schema.lua publishes NS.Schema non-idempotently  
  *Where:* settings/Schema.lua:5-6  
  *Evidence:* `local Schema = {}; NS.Schema = Schema`. architecture-§3 requires NS.<Module> = NS.<Module> or {}, and every other module uses that form.  
  *Remediation:* Change to `NS.Schema = NS.Schema or {}; local Schema = NS.Schema`.  
  *Rule:* architecture-§3  
  *Planned in:* PC-16

**WhatGroup**

- **WHATGROUP-R-13** `low` (review F-013; corrected) — Two settings-category fields written and never read, pinned by a test  
  *Where:* settings/Panel.lua:387-390, tests/test_panel.lua:90-91  
  *Evidence:* WhatGroup._settingsCategory and _parentSettingsCategory have no production reader (OpenOptionsPanel holds its own); test asserts non-nil, pinning dead state. grep -rn _settingsCategory libs/ is empty.  
  *Remediation:* C-011: delete the two assignments and their comment at settings/Panel.lua:387-390. Drop the two asserts at tests/test_panel.lua:90-91 and keep the rest of the case (the test count is unchanged), then re-run --list. In the same commit, remove the sentence about the recorded handles in docs/ARCHITECTURE.md:323 and docs/settings-panel.md:260. Rewrite the docs/midnight-quirks.md:38-40 example with a local category variable so it does not reference self._settingsCategory.  
  *Rule:* testing-§12  
  *Planned in:* WG-17


### C37 — Vacuous assertions and missing invariant tests

Tests assert against removed keys (nil==nil), assertError calls only check that something raised, and some cases test library internals. Defect paths go uncovered, tab-strip invariance is unpinned, and a stray CR hides a test file from EOL normalization, a blind spot in the kit's EOL test (upstream). Affects AbsorbTracker, AuraMaster, ConsumableMaster, KickCD, LibKa0s, LootHistory and PrettyChat.

**LibKa0s**

- **LibKa0s-R-07** `low` (review F-007; corrected) — 23 assertError calls only assert that something raised; four pass the expected text as the failure message  
  *Where:* tests/test_launcher.lua:123-128; tests/test_kit_inventory.lua:173,182,190,202,230; tests/test_mock_ace.lua (9 calls); tests/test_loader.lua:116-117; tests/test_options_compose.lua:674-675; tests/test_schema.lua:548; testkit/framework.lua:266-273  
  *Evidence:* Kit.assertError(fn, msg) uses msg only as failure text and returns the raised error, which callers discard; launcher case's red-under comment claims field check that doesn't happen; kit-inventory cases can pass on unrelated raises. grep gives 23 statement-position calls. testing-§12: MUST NOT treat 'it raised' as sufficient.  
  *Remediation:* C-09 (kit revision +1): add Kit.assertErrorMatches(fn, needle, msg) in a new testkit/asserts.lua loaded by framework.lua (framework.lua is over the cap, don't grow it); sync tests/_kit; rewrite all 23 call sites to assert on a substring of the raised error (launcher expected strings become needles). Pass count unchanged. Fold with C-02 kit half into one kit revision.  
  *Rule:* testing-§12; layout-§1  
  *Planned in:* LK-02

**AbsorbTracker**

- **AbsorbTracker-R-04** `medium` (review F-004; confirmed) — Slash and profile tests address the removed flat key barWidth and the removed pages bar and border, giving vacuous nil==nil asserts and no-op cleanups that leak state  
  *Where:* tests/test_slashcmds.lua:224-225, tests/test_slashcmds.lua:371, tests/test_slashcmds.lua:552, tests/test_slashcmds.lua:574, tests/test_slashcmds.lua:545-548, tests/test_slashcmds.lua:604-606, settings/Schema.lua:397, defaults/Profile.lua:32  
  *Evidence:* VALID_PAGES is {general, appearance, profiles}, so RestoreDefaults('bar') and RestoreDefaults('border') reset nothing. barWidth has been per-unit since schema v3, so NS.flatDefaults.barWidth is nil and the 'new/reset starts from defaults' cases assert nil==nil. Writes such as units.target.barWidth=300 (:218) leak into later suites.  
  *Remediation:* C-04: replace the cleanups with RestoreDefaults('appearance'). Rewrite :545-548 and :604-606 to use units.player.barWidth against NS.unitDefaults.barWidth, each with a '-- red under:' note. Afterwards, git grep for RestoreDefaults("bar"), RestoreDefaults("border") and rawSet("barWidth" must return nothing. Fix any ordering dependency this exposes where it lives.  
  *Rule:* testing-§12  
  *Planned in:* AT-02
- **AbsorbTracker-A-04** `low` (audit AT-60; confirmed) — No test asserts that the tab strip's reserved band and row y offsets are identical for every tab selection  
  *Where:* tests/test_widgets.lua:850, tests/_kit/mock_base.lua:102-109  
  *Evidence:* This recurs. The only assertion is chromeHeight > 0. The upstream blocker is gone: the kit now answers Options_Tab_* at 28 and Options_Tab_Active_* at 33. No page wraps today (2 tabs on General, 5 on Appearance).  
  *Remediation:* C12/S2.3: in test_widgets.lua, force a wrap with a narrow width or padded labels, reading heights from M.__atlasSizes. For each tab selection, record chromeHeight and every row's y offset and assert they are all equal (-- red under: pitch measured off Options_Tab_Active_*). A red at the current tag goes to LibKa0s and is not patched locally.  
  *Rule:* options-ui-§13, anti-pattern #70  
  *Planned in:* AT-15

**AuraMaster**

- **AuraMaster-A-11** `low` (audit AM-30; confirmed) — tests/page_helpers.lua has a stray bare CR at :80, so git classifies it binary and it escapes normalization  
  *Where:* tests/page_helpers.lua:80  
  *Evidence:* Line 80 ends \r\r\n. git ls-files --eol shows i/-text, and the blob is stored CRLF (272 CR). The E-8 working-tree one-liner counts 1 file. The kit's test_eol is green over it (the known lone-CR limit).  
  *Remediation:* Delete the stray \r, run git add --renormalize tests/page_helpers.lua, and confirm i/lf w/crlf. The (e) one-liner should print 0. Upstream testkit hardening is tracked separately in AuraMaster-A-18.  
  *Rule:* line-endings-§7 (property e)  
  *Planned in:* AM-01
- **AuraMaster-A-18** `low` (audit AM-30 (upstream note); U-2 in audit 05_EXECUTION_PLAN; corrected · upstream → LibKa0s) — LibKa0s testkit test_eol misses a tracked file git classifies -text under text=auto (the lone-CR blind spot)  
  *Where:* LibKa0s testkit test_eol (vendored as tests/_kit/); AuraMaster tests/page_helpers.lua:80 as the example  
  *Evidence:* test_eol stays green over tests/page_helpers.lua even though git stores it unnormalized as i/-text. line-endings-§7 names the lone-CR case as the one-liner's known limit.  
  *Remediation:* In LibKa0s, extend tests/_kit/test_eol.lua. For every tracked path with text not unset and no NUL byte (the same set the gate already scans), also count lone CRs: a byte 13 that is not followed by byte 10. Fail with the path and the line number whenever that count is above 0. Do not key the check on the index's -text classification alone, because that would redden real auto-detected binaries such as PanelMaster's realesrgan binary. Add a fixture test for a `\r\r\n` line. Update line-endings-§7's lone-CR note in WowAddonStandards: the kit now catches the case, and 'No file in the collection has one' is no longer true. Tag LibKa0s and re-vendor the whole of LibKa0s (libs/LibKa0s/ and tests/_kit/) into every addon. Land the local AM-30 fix first, so that AuraMaster is green when the new case arrives.  
  *Rule:* line-endings-§7  
  *Planned in:* LK-06

**ConsumableMaster**

- **ConsumableMaster-R-13** `low` (review F-013; confirmed) — Two assertions in the disabled suite cannot fail  
  *Where:* tests/test_disabled.lua:292; tests/test_disabled.lua:378  
  *Evidence:* ':292 t.truthy((ran or 0) > 0 or true, ...)' is a tautology. ':378 t.truthy(true, ...)' is padding.  
  *Remediation:* C-12: at :292, assert (ran or 0) > 0, or delete the line if 0 is legitimate (:296 already falsifies). Delete :378.  
  *Rule:* testing-§12  
  *Planned in:* CM-12

**KickCD**

- **KICKCD-R-11** `low` (review F-011; corrected) — The High and Medium defects sit on paths no test covers, and the shared instance swallows an OnInitialize raise  
  *Where:* tests/wow_mock.lua:573-640, tests/wow_mock.lua:769, tests/run.lua:105, tests/test_disabled.lua:436  
  *Evidence:* The gaps: - F-001: no profile swap at v5, and the mock AceDB has no SetProfile. - F-002: no assertion on scripts or mouse state left on released widgets. - F-003: mocks.__frames is never asserted. - F-004: no throttle call count. - F-008: no render count. Also, tests/run.lua:105 runs pcall(NS.OnInitialize, NS), which hides an init raise.  
  *Remediation:* C-11: add one red-under test per fix (testing-§12 '-- red under:' line). Replace the no-op SetProfile stub in tests/wow_mock.lua's DB_STUBS/AceDB mock with one that really switches db.profile to a separate per-profile table. That is the addon's own mock, not the kit. Add a #mocks.__frames delta assertion across disable/enable (F-003), plus a throttle call count (F-004) and a render count (F-008). Surface OnInitialize failures in tests/run.lua, either by capturing pcall's result and failing the instance or by not wrapping it. Regenerate docs/test-cases.md and move the README tests badge in each commit that adds cases.  
  *Rule:* testing-§12  
  *Planned in:* KC-02

**LootHistory**

- **LootHistory-R-07** `low` (review F-007; corrected) — tests/test_debuglog.lua unit-tests the library's own formatter  
  *Where:* tests/test_debuglog.lua:10-28  
  *Evidence:* Four cases (FormatPlain wraps/renders the tag, tolerates a nil tag, FormatColored colors) test LibKa0s-DebugLog rendering, not addon wiring. A legitimate upstream formatter change would turn them red while the library suite is green.  
  *Remediation:* C-007: delete the four cases and keep the FONT_MONO and NS.Debug / NS.SafeToString integration cases. That is -4 cases; move docs/test-cases.md and the README badge in the same commit. The cases belong in LibKa0s's suite, which already owns that behavior.  
  *Rule:* testing-§8  
  *Planned in:* LH-20

**PrettyChat**

- **PRETTYCHAT-A-26** `info` (audit PC-69 (PRETTYCHAT-A-10, carried); corrected · upstream → WowAddonStandards) — No test pins the Categories tab-strip wrap invariance; options-ui-§13 Testing MUST conflicts with testing-§8 for a library-drawn strip  
  *Where:* libs/LibKa0s/OptionsTabs.lua, tests/test_panel.lua, tests/wow_mock.lua  
  *Evidence:* No case asserts that the reserved band and every row's y offset are identical across selections when the selected-state art has a different height. The strip is H.TabStrip (library). Deferred with M1-LK-08.  
  *Remediation:* Drop the LibKa0s Sprint 1.2 item, because test_options_tabs.lua:573 already covers it. Do not add a host case. Upstream only: have WowAddonStandards clarify options-ui-§13 Testing to say that for a library-drawn strip (H.TabStrip) the library's suite pins the invariant, and the consumer relies on it under testing-§8. PrettyChat needs no change.  
  *Rule:* options-ui-§13 (Testing MUST); testing-§12; testing-§8  
  *Planned in:* WS-06


### C38 — LibKa0s library defects

These are correctness and design bugs in the library itself. Item.QualityFromLink cannot parse the 11.1.5+ \|cnIQ link color, PageBanner leaks frames on every render, and a newer AceEvent re-embed overwrites the Bus wrappers. printer.Format raises on secret values, ReorderList hijacks pooled frames, the quality map is cached even when empty, Schema drops instanceId, and Lifecycle's re-entrancy is undocumented. Single-repo theme in LibKa0s, shipped to every addon by the re-vendor.

**LibKa0s**

- **LibKa0s-R-01** `high` (review F-001; confirmed) — Item.QualityFromLink cannot parse the 11.1.5+ \|cnIQ<n> item-link color; tests pin the retired \|cff format  
  *Where:* LibKa0s/Item.lua:85; LibKa0s/Item.lua:75; tests/test_item.lua:14-16; LootHistory/core/Compat.lua:163; LootHistory tests/test_itemsetup.lua:14  
  *Evidence:* Pattern link:match("\|c%x%x(%x%x%x%x%x%x)") only matches \|c+8 hex; since patch 11.1.5 item links use \|cnIQ<n> (warcraft.wiki.gg ItemLink / UI_escape_sequences), so every live link on 120100 returns nil. LootHistory's Compat.GetItemInfo falls back to it for uncached items, so those drops are recorded with nil quality. All three test cases and LootHistory's fixture use the pre-11.1.5 \|cff shape, so they pass anyway.  
  *Remediation:* C-01 (Item minor 1->2): add a rung reading tonumber(link:match("\|cnIQ(%d+)")) ahead of the hex rung (anchor on digits, don't require trailing ':'); keep the hex rung for stored legacy links. Add \|cnIQ fixtures, keep \|cff as legacy-rung case (red under: drop the \|cnIQ rung). Update docs/api/Item version-2 docs + members-2.json, test-cases.md and README badge in same commit. Smoke S-001. Consumer follow-up M6-T14: refresh LootHistory tests/test_itemsetup.lua EPIC_LINK to \|cnIQ shape.  
  *Rule:* localization-§4; library-stack-§7 (additive)  
  *Planned in:* LK-12
- **LibKa0s-R-02** `medium` (review F-002; corrected) — PageBanner/PageHeader/divider leak an AceGUI Dropdown or raw Frame plus a texture on every full page render  
  *Where:* LibKa0s/OptionsTabs.lua:1036; LibKa0s/OptionsTabs.lua:1117; LibKa0s/OptionsTabs.lua:577; LibKa0s/OptionsTabs.lua:734-741; testkit/mock_base.lua:1364  
  *Evidence:* O.PageBanner does AceGUI:Create("Dropdown") each render, O.PageHeader CreateFrame each call, drawChromeDivider creates a new texture each call; releaseLedger only Hide()/SetParent(nil)s them, never AceGUI:Release. Unbounded growth per render in 8 consumers' banner/header pages (AuraMaster, ConsumableMaster, KickCD, MultiMeters, AbsorbTracker, PanelMaster). Kit mock AceGUI never reuses widgets so no test can see it. Side issue: SetParent(nil) on a texture Region unverified.  
  *Remediation:* C-02 (OptionsTabs minor 3->4, new Options version key): pool PageHeader frame per ctx (ctx.__headerPool via LibKa0s-Pool-1.0, released in releaseChrome via Pool.ReleaseAll); build divider texture once per ctx (ctx.__ruleTex), hide on release, never SetParent(nil) a Region; keep ctx.__bannerWidget and AceGUI:Release it at top of next releaseChrome. Kit revision +1: mock AceGUI Create/Release per-type survey in testkit/mock_record.lua with 2-line hook in mock_base.lua. New tests in tests/test_options_tabs.lua (second render releases first dropdown; header frame reused; divider drawn once per ctx). Smoke S-002.  
  *Rule:* events-frames-taint-§6; options-ui-§14  
  *Planned in:* LK-27
- **LibKa0s-R-05** `low` (review F-005; corrected) — A later-loading newer AceEvent-3.0 re-embed silently overwrites the Bus tracking wrappers  
  *Where:* LibKa0s/Bus.lua:196; LibKa0s/Bus.lua:165-184  
  *Evidence:* AceEvent-3.0 upgrade loop re-Embeds every target, overwriting the six members including Bus wrappers; later registrations go straight to CallbackHandler and are never recorded, so StandDown leaves them live (anti-pattern #85 draw gate) or StandUp never replays them. Latent: needs a third-party addon shipping a newer AceEvent minor.  
  *Remediation:* C-05 (Bus minor 1->2): keep rec.wrap[kind]; add restamp(rec) that re-assigns any member not equal to its wrapper and adopts the new raw member as rec.raw[kind]; keep a weak-keyed created list beside held and restamp every created target in StandDown/StandUp, returning a trailing restamped count via isDown's debug seam. Document the residual window in the docstring. Test in tests/test_bus.lua simulating re-embed (red under: drop restamp). Smoke S-005. Do not fork Ace3 or use a metatable proxy.  
  *Rule:* library-stack-§5; anti-patterns #85  
  *Planned in:* LK-14
- **LibKa0s-R-08** `low` (review F-008; corrected) — Core printer.Format raises on a secret value in a numeric specifier (bug DebugLog already fixed)  
  *Where:* LibKa0s/Core.lua:459; LibKa0s/DebugLog.lua:640-658  
  *Evidence:* Args are stringified first; a secret becomes "<secret>" and %d/%.1f raises 'number expected, got string' in combat. DebugLog added a pcall + verbatim fallback for the identical failure. Latent: 0 current consumer call sites pass a numeric specifier through printer.Format.  
  *Remediation:* C-07 (Core minor 7->8): pcall(string.format, SafeToString(fmt), unpack(parts)); on failure join fmt and parts with spaces; emit. No floor raise. Test in tests/test_core.lua (secret into %d lands as format + <secret>; red under: remove pcall). Smoke S-007.  
  *Rule:* debug-logging-§4  
  *Planned in:* LK-10
- **LibKa0s-R-12** `low` (review F-012; corrected) — ReorderList hijacks the host row frame's OnUpdate and caches its drop line on the AceGUI-pooled container  
  *Where:* LibKa0s/Widgets.lua:999; LibKa0s/Widgets.lua:915; LibKa0s/Widgets.lua:1080; LibKa0s/Widgets.lua:753; LibKa0s/Widgets.lua:783-795  
  *Evidence:* Drag poll SetScript("OnUpdate") on row.frame then clears it, overwriting any host OnUpdate; container.__ka0sDropLine rides back into AceGUI's pool keeping the first caller's lineColor, contradicting the file's own pooled-frame rule. No shipped row frame carries an OnUpdate today.  
  *Remediation:* Same remediation as stated (poll on the library-owned ghost frame, drop line from a library pool reclaimed in Cancel, re-coloured per list, tests in a new tests/test_widgets_reorder.lua). Change rule_ref to the Widgets.lua:783-795 pooled-frame invariant (internal) instead of events-frames-taint-§6.  
  *Rule:* events-frames-taint-§6  
  *Planned in:* LK-21
- **LibKa0s-R-13** `low` (review F-013; confirmed) — Item quality-color map cached even when built empty; LoadItem waits a fixed 0.4s timer  
  *Where:* LibKa0s/Item.lua:64; LibKa0s/Item.lua:87; LibKa0s/Item.lua:124; LibKa0s/Item.lua:57-60  
  *Evidence:* If first call precedes ITEM_QUALITY_COLORS population the empty map persists for the session; LoadItem fires after C_Timer.After(0.4) regardless of data arrival. Unlikely in client; less relevant once \|cnIQ rung lands.  
  *Remediation:* Part of C-01: build into a local and assign qualityByHex only if at least one entry landed; add empty-map retry case. Leave LoadItem unchanged (byte-identical in both hosts) and record that decision.  
  *Planned in:* LK-12
- **LibKa0s-R-14** `low` (review F-014; confirmed) — Schema ApplyDefault and a row's own get drop instanceId  
  *Where:* LibKa0s/Schema.lua:358; LibKa0s/Schema.lua:497-502  
  *Evidence:* Set/Get accept instanceId via resolveRoot, but ApplyDefault calls S.Set with no id and a closure row's get() receives no id. No current consumer affected (AuraMaster keeps its own runtime).  
  *Remediation:* C-08 (Schema minor 1->2, optional): S.ApplyDefault(row, instanceId) forwards to S.Set; S.Get calls row get(instanceId). Additive. Review recommends deferring until an instanced host adopts the runtime and recording the deferral in CHANGELOG.md and the Schema API doc; user asked for ALL findings so plan should either implement or explicitly record deferral.  
  *Rule:* library-stack-§7 (additive)  
  *Planned in:* LK-22
- **LibKa0s-R-17** `low` (review F-017; confirmed) — Lifecycle edge is re-entrant and the file doesn't document it  
  *Where:* LibKa0s/Lifecycle.lua:123-129  
  *Evidence:* A standDown callback that takes/releases a hold fires a nested edge (standUp inside unwinding standDown); latch stays consistent but host teardown can interleave. No shipped callback touches the latch.  
  *Remediation:* C-13 (Lifecycle minor 1->2): document in New's docstring that a callback MUST NOT take or release a hold (or queue nested edges), and add a tests/test_lifecycle.lua case pinning the chosen nested-edge behavior.  
  *Planned in:* LK-15


### C39 — KickCD Spells page and icon grid

The Spells page hooks pooled AceGUI frames, so its tooltips leak into every AceGUI consumer, and each edit renders the page twice behind a guard an error can leave stuck. /kcd spells add disagrees with the page and accepts orphan class/spec lists, and GateHint writes into the live profile. Empowered casts are untracked, and an IconGrid rebuild relies on dispatch order. Single-repo theme in KickCD's settings/Spells.lua and modules/IconGrid*.

**KickCD**

- **KICKCD-R-02** `medium` (review F-002; corrected) — The Spells page HookScripts AceGUI's pooled Label and Dropdown frames, so its tooltips and mouse capture leak into every AceGUI consumer  
  *Where:* settings/Spells.lua:662-666, settings/Spells.lua:763-770, settings/Spells.lua:853-865, settings/Spells.lua:1295-1300  
  *Evidence:* label.frame:EnableMouse(true) plus HookScript OnEnter/OnLeave, and dd.frame:HookScript('OnEnter', ...) showing the 'Category for future filtering…' tooltip. AceGUI recycles these frames through one process-global pool, a hook cannot be removed, and the Label and Dropdown OnAcquire reset neither scripts nor EnableMouse. Recycled labels in other addons' panels (AbsorbTracker, AuraMaster, BankLedger, ConsumableMaster, LootHistory, PanelMaster, PrettyChat) then show a KickCD spell tooltip and swallow clicks. One more hook pair is added per row per render, and F-008 doubles the renders. No test covers this.  
  *Remediation:* Replace the Label with AceGUI:Create('InteractiveLabel') and use SetCallback('OnEnter'/'OnLeave'). Call SetHighlight(nil) if the highlight is unwanted. Replace the dd.frame HookScript with H.AttachTooltip(dd, L['Category'], L['Category for future filtering. Currently informational only.']). This also fixes the dropdown tooltip, which never fires today because dd.frame is not mouse-enabled. Test: render twice, release, acquire a plain Label, and assert it has no OnEnter script and IsMouseEnabled() is false. Also assert the dropdown's OnEnter callback shows the tooltip. Drop the options-ui-§1 rule_ref, or cite AP #76 by analogy (AceGUI objects are process-global).  
  *Rule:* options-ui-§1  
  *Planned in:* KC-12
- **KICKCD-R-05** `medium` (review F-005; confirmed) — /kcd spells add disagrees with the Spells page: multi-word names split, Cooldown Manager gate skipped, resolver duplicated  
  *Where:* core/KickCD.lua:501-505, core/KickCD.lua:570-584, core/KickCD.lua:617-624, settings/Spells.lua:272-285, settings/Spells.lua:461-473, README.md:95  
  *Evidence:* tokenize on %S+ splits 'Wind Shear' into the name 'Wind' and a class token 'Shear'. The CLI skips cooldownManagerRejects, which the page applies, although the README says only tracked cooldowns can be added. The ID/name resolver exists twice. The documented <name> form fails for most interrupts.  
  *Remediation:* C-05: add a new core/SpellInput.lua (Resolve, Admissible, ParseTail) after core/Database.lua in the TOC, with a comment naming load-time needs (#66). Move the _cmCache builder and its invalidation frame there from settings/Spells.lua:287-384. Call it from both core/KickCD.lua and settings/Spells.lua. Trailing tokens become [CLASS SPEC] only if they resolve. Tests in test_slash and test_spell_registry: 'Wind Shear' adds 57994 on a Shaman, and the CLI refuses a spell the Cooldown Manager lacks. Add docs/ARCHITECTURE.md module-map row. Serialized ahead of F-008 and F-010 (all touch settings/Spells.lua), after M2.  
  *Rule:* architecture-§5; layout-§1; toc-file; AP #66  
  *Planned in:* KC-06
- **KICKCD-R-06** `medium` (review F-006; confirmed) — Empowered casts (UNIT_SPELLCAST_EMPOWER_*) are not tracked by the cast bar or the icon grid's cast-state logic  
  *Where:* modules/Castbar.lua:1016-1027, modules/IconGrid.lua:810-819  
  *Evidence:* Neither module registers UNIT_SPELLCAST_EMPOWER_START/STOP/UPDATE (a grep for 'empower' finds nothing), while the sibling PartyFrameEnhanced does. The bar misses an empower started after targeting, may persist after one ends, and target_casting visibility and glow lag. Unverified in the client: it mainly affects PvP Evokers, and whether any NPC empowers is unknown.  
  *Remediation:* Part of C-03: add the three EMPOWER events to both route maps, riding the single filter frame. In Castbar they map to OnChannelStart/OnCastStop/OnCastDelayed, and in IconGrid to OnUnitCastEvent. Register them via pcall/C_EventUtils.IsEventValid. Add an EMPOWER note to docs/midnight-quirks.md. Verify with smoke test C-03 step 4; record it as untested if no Evoker is available.  
  *Rule:* events-frames-taint-§1  
  *Planned in:* KC-05
- **KICKCD-R-07** `medium` (review F-007; confirmed) — An IconGrid rebuild repaints every icon 'ready' and relies on unordered CallbackHandler dispatch for correction  
  *Where:* modules/IconGrid.lua:351, modules/IconGrid.lua:340-353, modules/IconGrid.lua:1290-1306, modules/Cooldowns.lua:547-555  
  *Evidence:* BuildActiveList applies { ready = true, start = 0, duration = 0 } to every icon. Cooldowns and IconGrid both handle PEW, SPELLS_CHANGED, TRAIT_CONFIG_UPDATED, PROFILE_CHANGED and CONFIG_CHANGED, and dispatch runs in pairs order. If Cooldowns fires first, its SPELL_STATE lands on the old pool. An interrupt on cooldown can then show ready after a talent swap, pet summon, spec or profile switch, or /reload, until the next SPELL_UPDATE_*. Unverified in the client.  
  *Remediation:* C-06: publish a read-only Cooldowns:StateFor(spellID) returning watched[id]. After BuildActiveList, seed with btn:Apply(st or READY_SEED, true), where READY_SEED is a file-scope constant. Alternative: Cooldowns re-emits on GRID_LAYOUT. Test: register Cooldowns before IconGrid, fire PEW, and assert an on-cooldown icon is not ready. Serialize after R-03 (both touch IconGrid.lua). Smoke test C-06.  
  *Rule:* architecture-§4; AP #19  
  *Planned in:* KC-08
- **KICKCD-R-08** `low` (review F-008; corrected) — Every Spells-page edit renders the page twice, and an error mid-render leaves the render guard stuck for the session  
  *Where:* settings/Spells.lua:404-407, settings/Spells.lua:1179-1244, settings/Spells.lua:1345-1350, settings/Spells.lua:1186-1188  
  *Evidence:* doCommit calls RefreshRows and then FireConfigChanged, whose synchronous subscriber calls RefreshRows again. If fillRows raises, rebuildScheduled stays true and every later RefreshRows returns early. The comment's claim that the flag 'is cleared on EVERY exit' is true of the explicit returns only.  
  *Remediation:* doCommit should call only FireConfigChanged when the addon is up, and call RefreshRows directly only when NS.IsDown(), because StandDown has unregistered the CONFIG_CHANGED subscriber. Make RefreshRows run its body in a pcall/xpcall (or an equivalent) that always resets rebuildScheduled and then re-raises the error. Tests: one RefreshRows per commitSoon flush, and a later refresh still renders after a forced fillRows raise. Drop slash-commands-§7 as the rule_ref: this is a correctness defect, not a standards deviation.  
  *Rule:* slash-commands-§7  
  *Planned in:* KC-11
- **KICKCD-R-18** `low` (review F-018; confirmed) — /kcd spells accepts any CLASS token or numeric spec and lazily creates orphan lists; the bare /kcd spells prints a raw spec ID  
  *Where:* core/KickCD.lua:532-547, core/Util.lua:406-408, core/Util.lua:347-351, core/Database.lua:147-154, core/KickCD.lua:764  
  *Evidence:* NormalizeClassToken output is unvalidated and ResolveSpecID returns any number, so AddSpell -> EnsureSpellList writes spells.WARLORD[99999]. KickCD.lua:764 prints the default spec as a number, where every other line uses SpecDisplay.  
  *Remediation:* Folded into C-05: SpellInput.ParseTail validates the class against GetClassInfo and the spec for that class, and Database:AddSpell rejects an unknown class token. At core/KickCD.lua:764, the raw spec ID becomes sd(spc).  
  *Rule:* architecture-§5  
  *Planned in:* KC-06
- **KICKCD-R-15** `info` (review F-015; corrected) — GateHint probes by temporarily writing candidate values into the live profile  
  *Where:* settings/Slash.lua:127-129  
  *Evidence:* `parent[key] = candidate` ... `parent[key] = gateVal` is a temporary write around the single write seam. It is safe only while every row.values() is pure and nothing runs in between.  
  *Remediation:* Optional: add a row.valuesFor(gateValue) hook to the rows that have a valueGate, and have GateHint call it when present so the live profile is never written. Keep the existing pcall/restore probe as the fallback. No other change is needed, because Resolve, pcall and the documentation already exist.  
  *Rule:* architecture-§5  
  *Planned in:* KC-16


### C40 — LootHistory capture and export correctness

Keystone context is never cleared, encounter detail clears before the boss corpse is looted, and the currency-category cache never rebuilds. Warbound repair cannot warm link-only rows and Export shares nested tables with live history. The resize grip ignores Lock frame, and exports use two vocabularies for bind state. Single-repo theme in LootHistory.

**LootHistory**

- **LootHistory-R-01** `high` (review F-001; confirmed) — Mythic+ keystone context never cleared; every later GameObject loot recorded as MPLUS  
  *Where:* modules/Attribution.lua:228-233, modules/Attribution.lua:235-243, modules/Attribution.lua:173-176, modules/Attribution.lua:411, modules/Attribution.lua:238  
  *Evidence:* State.keystone is set on CHALLENGE_MODE_START and deliberately kept after completion. It is cleared only in Attribution:Disable (:411); grep finds writes only at :229/:238/:411. ResolveLootSource maps any GameObject loot to S.MPLUS while state.keystone is set, so herbs, ore, world chests and other instances' containers are persisted to LootHistoryDB as MPLUS with a keystoneLevel. That pollutes the Source column and filter, the Insights by-source and keystone breakdowns (core/Database.lua:557-558) and both CSVs, with no repair. No test covers the context lifetime; only the pure resolver case at tests/test_attribution.lua:71 exists. Related, unverified: at :238 a completion-time 0 from GetActiveKeystoneLevel is truthy, so 0 would be stored.  
  *Remediation:* C-001: add a presence-guarded NS.Compat.InPartyInstance() shim (IsInInstance, instanceType == 'party'). Add Attribution:OnZoneChanged, which clears State.keystone when not in a party instance, and OnChallengeModeReset. Register ZONE_CHANGED_NEW_AREA and CHALLENGE_MODE_RESET on bus and append them to self.__events so Disable tears them down. Do NOT register PLAYER_ENTERING_WORLD on NS.addon, which would collide with LifecycleSetup:112 OnEnterWorld. Guard :238 with (lvl and lvl > 0). Add 3 tests (clears when out of instance, kept in instance, CHALLENGE_MODE_RESET) and update the Enable 'seven events' case to nine. Update docs/data-flow.md:88 and midnight-quirks.md:22, and move test-cases.md and the badge in the same commit. Smoke S-001. Existing mislabelled rows cannot be repaired (no signal).  
  *Planned in:* LH-01
- **LootHistory-R-03** `medium` (review F-003; corrected) — Currency-category cache is built once per session and never rebuilt  
  *Where:* core/Compat.lua:392-393, modules/Collector.lua:198  
  *Evidence:* The id-to-header map is a snapshot taken at the session's first currency loot. A currency first discovered later, or one under a header that was collapsed at build time (unverified), is missing from it. Its row is persisted with itemSubType = nil and never backfilled. This hits routinely at season start.  
  *Remediation:* In Compat.CurrencyCategory, rebuild the cache at most once per miss (a module-local sentinel keyed by the missed id, so an id that is genuinely absent does not trigger a walk on every loot) and look it up again. Keep the unknown-id -> nil contract (test_compat.lua:338). For collapsed headers, either (a) verify in the client whether GetCurrencyListInfo exposes collapsed children and, if not, document the gap in midnight-quirks.md, or (b) expand collapsed headers for the walk via C_CurrencyInfo.ExpandCurrencyList, guarded for presence, and restore them afterwards. Add a test_compat case where the mock list gains an id after the first call. Smoke S-003.  
  *Rule:* compat  
  *Planned in:* LH-03
- **LootHistory-R-02** `low` (review F-002; corrected) — Encounter detail cleared at ENCOUNTER_END, before the boss corpse is looted  
  *Where:* modules/Attribution.lua:223-226, modules/Attribution.lua:168-171, modules/Attribution.lua:203  
  *Evidence:* OnEncounterEnd sets State.encounter = nil. The corpse's LOOT_OPENED comes after ENCOUNTER_END, so sourceDetail.encounterID and difficulty are effectively never written for boss loot. docs/data-flow.md:74 and docs/midnight-quirks.md:17 claim the field is captured. No UI displays the field, which caps severity. The event order needs in-client confirmation.  
  *Remediation:* C-002: on a successful ENCOUNTER_END (success == 1), keep State.encounter and stamp expires = GetTime() + Constants.ENCOUNTER_GRACE (a new constant, about 60 s). Clear it on a wipe. ResolveLootSource treats the encounter as live while now <= expires, with now passed via state in tests. Add 2 tests (within grace carries encounterID, after grace does not) and move the badge and inventory. Checkpoint CP-1 / smoke S-002 first: if LOOT_OPENED precedes ENCOUNTER_END in-client, close as not reproduced and make no code change (or document the field as not captured).  
  *Planned in:* LH-02
- **LootHistory-R-09** `low` (review F-009; confirmed) — Window resize grip ignores Lock frame  
  *Where:* modules/Browser.lua:1049, modules/Browser.lua:958-961, docs/settings-panel.md:40, docs/settings-panel.md:191  
  *Evidence:* The grip's OnMouseDown calls StartSizing with no B:IsLocked() check, while the title-bar drag checks it. SaveWindow persists the resize. docs/settings-panel.md:40 defines Lock frame as drag-only, so this is an expectation gap, not a contract break.  
  *Remediation:* C-009: add 'if B:IsLocked() then return end' before frame:StartSizing('BOTTOMRIGHT'). Update docs/settings-panel.md:40 and :191 to say 'dragged or resized'. Smoke S-007. Coordinate with LH-76, which touches the same grip.  
  *Planned in:* LH-10
- **LootHistory-R-12** `low` (review F-012; confirmed) — Two vocabularies for bind state across exports and sentinels  
  *Where:* modules/Export.lua:11-14, modules/Export.lua:140-141, core/Database.lua:357, core/Database.lua:524, tests/test_export.lua:217  
  *Evidence:* The row CSV uses 'Bind on Pickup' / 'Not Bound'. The Insights CSV uses 'Soulbound' / 'Unbound'. Database uses both the 'NONE' (:357) and 'UNBOUND' (:524) sentinels for the same state.  
  *Remediation:* C-011: unify both exports on the row-CSV labels (BOUND_LABEL_CSV reads from BOUND_LABEL, with UNBOUND mapped to NONE). Update tests/test_export.lua:217 from 'Unbound' to 'Not Bound' as an intended output change, and note it in the release notes. Leave the sentinels (NONE is a persisted savedView.bound key; UNBOUND keys Analytics/BrowserTable styling), but add comments at Database.lua:357 and :524 naming the other sentinel and why they differ. Smoke S-008.1.  
  *Planned in:* LH-09
- **LootHistory-R-15** `low` (review F-015; confirmed) — Warbound repair cannot warm the item cache for a link-only row  
  *Where:* core/Database.lua:214, libs/LibKa0s/Item.lua:122  
  *Evidence:* NS.Item.LoadItem(r.itemID) with a nil itemID is a no-op, so the row stays pending until the 10-pass cap. Affects only legacy or hand-edited rows.  
  *Remediation:* C-014: NS.Item.LoadItem(r.itemID or NS.Item.ItemIDFromLink(r.itemLink)). Add a +1 test where the spy on C_Item.RequestLoadItemDataByID sees the parsed id.  
  *Planned in:* LH-06
- **LootHistory-R-17** `low` (review F-017; confirmed) — Database:Export claims a plain copy but shares nested tables with live history  
  *Where:* core/Database.lua:439, core/Database.lua:442  
  *Evidence:* auctionPrice and sourceDetail are copied by reference. No shipped path mutates an export result today.  
  *Remediation:* C-015: auctionPrice = r.auctionPrice and NS.Util.DeepCopy(r.auctionPrice), and the same for sourceDetail. This is export-only, so the cost is paid once per export.  
  *Planned in:* LH-07


### C41 — MultiMeters window rows and drill-down

'Always show yourself' does nothing on the default maxRows=0 profile, because the pin works against a 40-row cap while only about 10 rows draw. The drill-down closes when its window is renamed. Single-repo theme in the MultiMeters window code.

**MultiMeters**

- **MultiMeters-R-01** `high` (review F-001; confirmed) — 'Always show yourself' does nothing on the default profile (maxRows=0): the pin works against a 40-row cap, but the window draws only about 10 rows  
  *Where:* modules/Aggregator.lua:1289-1314; modules/Window.lua:1206-1207; modules/Window.lua:324-335; defaults/Profile.lua:281; tests/test_aggregator.lua:411-424  
  *Evidence:* ApplyRowLimit treats cap<=0 as Const.MAX_ROWS (40), while Render stops at layout.maxRows (10 at 220px). The pin also ignores the scroll offset. Headless repro: 'default window: maxRows=0 alwaysShowSelf=true visible=10 kept=20 self-in-view=false' (player at rank 15). The existing test covers only an explicit maxRows=3.  
  *Remediation:* C-02: add a pure, allocation-free Aggregator.SelfPinIndex(entries, first, visible, rowsConfig) beside ApplyRowLimit. Window:Render computes the pin index for 1+offset and layout.maxRows (skipped in drill-down) and draws entries[pin] in the last slot. Keep ApplyRowLimit's pin. Keep Render at CCN 15 or below with a single-expression substitution or a named local, never a part2 split. Pass the entry's real rank if the name cell shows one. Tests: 3 in tests/test_window.lua (default window with player at rank 15; scrolled so the player is in the slice; alwaysShowSelf=false) and 1 in tests/test_aggregator.lua. Smoke test SM-04.  
  *Rule:* CLAUDE.md R3 (layout from config); anti-pattern #52  
  *Planned in:* MM-03
- **MultiMeters-R-16** `low` (review F-016; confirmed) — The drill-down closes when its window is renamed  
  *Where:* modules/DrillDown.lua:850-855; modules/WindowManager.lua:316  
  *Evidence:* The drill-down exits on any WINDOWS_CHANGED addressed to its window, including action 'renamed'.  
  *Remediation:* C-13: exit only when payload.action ~= 'renamed'. Add a case in tests/test_drilldown.lua. Smoke test SM-10.  
  *Planned in:* MM-05


### C42 — PanelMaster panel geometry and frame naming

/pm recover bounds scaled offsets against the unscaled screen size, and a profile switch that swaps id-to-name ownership creates duplicate named frames. The grid slider and C.MAX_GRID disagree, and the per-panel Unlock tick can misreport state. Single-repo theme in PanelMaster.

**PanelMaster**

- **PanelMaster-R-04** `medium` (review F-003; corrected) — /pm recover bounds scaled panel offsets against unscaled UIParent screen size  
  *Where:* modules/Registry.lua:876-904, modules/Registry.lua:892-895, modules/Canvas.lua:566-569, modules/Canvas.lua:112-113, modules/Canvas.lua:85-89, modules/Unlock.lua:211  
  *Evidence:* applySpec calls SetScale(spec.scale) before SetPoint, so stored offsets are in the frame's scaled space (spec.scale = own scale x master Scale). R:Recover clamps rec.x/rec.y against Compat.GetScreenSize(), which is in UIParent units. At s=0.5 a visible TOPLEFT panel at x=3000 is moved; at s>1 a genuinely off-screen panel is left in place. The five existing Registry.Recover cases (tests/test_registry.lua:283-330) all run at scale 1.  
  *Remediation:* Add Util.EffectiveScale(rec, settings) in core/Util.lua (own scale clamped to MIN/MAX_PANEL_SCALE, times the master scale, default 1). Use it in Canvas addGeometry, which removes the now-unused masterScale. In R:Recover, bound with offsetRange(relPoint, w / s) and offsetRangeY(relPoint, h / s). Add two test_registry cases, red first: at scale 0.5, x=3000 is not moved; at scale 2, x=1500 is moved. Keep the five scale-1 cases unchanged.  
  *Rule:* options-ui-§15 (master rows as multipliers; one definition shared by render and recover)  
  *Planned in:* PM-04
- **PanelMaster-R-05** `medium` (review F-004; confirmed) — A profile switch that swaps which id owns which frame name creates a duplicate named frame and orphans one each switch  
  *Where:* modules/Canvas.lua:811-820, modules/Canvas.lua:696-703, modules/Canvas.lua:829-842, modules/Canvas.lua:36-40  
  *Evidence:* RenderAll resolves mismatches one id at a time. When id 1 wants a name still held by active[2], acquire runs CreateFrame with that global name a second time. When id 2 is released, its frame overwrites the pool slot, and the earlier frame becomes unreachable. A probe alternating {1 Alpha, 2 Xray}/{1 Xray, 2 Alpha} six times recorded 6 named CreateFrame calls, with PooledCount stuck at 1. test_profiles.lua never swaps ids.  
  *Remediation:* Make Canvas:RenderAll(inCombat) two-pass. First build want[id]=Registry.FrameName(rec), then release every active frame that is retired or whose __frameName is not want[id], then Render each id. Keep the Render(id) single-id mismatch branch as the fallback. Add a test_profiles case, red first, that swaps names across ids several times through OnProfileChanged and asserts zero named CreateFrame calls after the first render, plus _G-name/active identity.  
  *Rule:* events-frames-taint-§6  
  *Planned in:* PM-05
- **PanelMaster-R-07** `low` (review F-007; confirmed) — The grid-size setting has two maxima: the slider stops at 64 while C.MAX_GRID allows 128  
  *Where:* settings/Schema.lua:71-76, core/Constants.lua:100, modules/Unlock.lua:39  
  *Evidence:* The schema row declares max = 64, while its validate function and Unlock snap clamp use C.MAX_GRID = 128. The only way to reach a value between 65 and 128 is a hand-edited SavedVariables file.  
  *Remediation:* Use one constant. The recommended option is to lower C.MAX_GRID to 64, since no UI or CLI path could ever store more. The alternative is max = C.MAX_GRID. Add a test_schema case asserting S:FindRow('settings.gridSize').max == C.MAX_GRID.  
  *Planned in:* PM-07
- **PanelMaster-R-08** `low` (review F-008; confirmed) — The per-panel Unlock tick on the Panels page can show a state the panel is not in  
  *Where:* settings/PanelEditor.lua:743-758, modules/Unlock.lua:123-126, modules/Unlock.lua:245  
  *Evidence:* The tick has no refresher. It reads IsPanelUnlocked, which is true whenever the global unlock is on, so unticking it while globally unlocked has no effect. A global lock clears per-panel unlocks without refreshing the editor. A combat-deferred unlock replayed on PLAYER_REGEN_ENABLED leaves the box unticked.  
  *Remediation:* Give the tick a scalar refresher that reads NS.Unlock:IsPanelUnlocked(rec.id). Disable it, with a tooltip line, while the global unlock is on. From the end of U:SetUnlocked, U:SetPanelUnlocked and U:ResumePending, call NS.PanelEditor:RefreshUnlock() behind a presence guard (precedent: modules/Registry.lua:516). Do not add a new bus message. PanelEditor.lua is 1476 lines, so keep the change to 12 added lines or fewer, or land it after the issue #47 split; it must never cross 1500.  
  *Rule:* layout-§1 (constraint)  
  *Planned in:* PM-06


### C43 — PrettyChat format overrides and cross-addon interaction

PrettyChat rewrites the CHAT_MSG_LOOT/CURRENCY globals at runtime, so LootHistory's once-compiled patterns stop matching. Loot-tab copies are saved but never applied, OriginalFormat reports PrettyChat's own override as Blizzard's, the New box passes gsub's count as instanceId, and a generator sits outside tools/. Single-repo theme in PrettyChat that touches LootHistory's contract.

**PrettyChat**

- **PRETTYCHAT-R-01** `medium` (review F-001 (handoff H-1; smoke SMK-F001; change C-01); corrected) — PrettyChat rewrites CHAT_MSG_LOOT/CURRENCY text at runtime; LootHistory compiles its loot/currency patterns once and silently stops recording  
  *Where:* modules/Override.lua:292, modules/Override.lua:302, modules/Override.lua:121-127, docs/ARCHITECTURE.md:151, LootHistory/core/Util.lua:118, LootHistory/core/Util.lua:147, LootHistory/core/Util.lua:187, LootHistory/core/Util.lua:210  
  *Evidence:* ApplyStrings sets _G[globalName] on every settings write, latch transition, profile event and, while the combat watcher is armed, every combat boundary (visibility inCombat/outOfCombat). LootHistory caches lootPatterns/currencyPatterns on first parse (`local pats = lootPatterns or Util.BuildLootPatterns()`) and never rebuilds them. After any change, self-loot and self-currency in the other state go unrecorded, with no error. The mechanism is inferred from PrettyChat's own premise and is unverified in-client. No headless suite can see it.  
  *Remediation:* PrettyChat side (C-01): add a Known Limitations bullet in docs/ARCHITECTURE.md saying PrettyChat rewrites the CHAT_MSG_LOOT/CURRENCY/MONEY/COMBAT_* payload for every addon, that parsers must build patterns from the live global or revalidate them, and that inCombat/outOfCombat modes change these globals at every combat boundary. Name handoff H-1. Add one sentence to docs/scope.md and add SMK-F001 to docs/smoke-tests.md. Cross-repo (H-1, LootHistory): Util.ParseSelfLoot (:145) and ParseSelfCurrency (:208) record the source global values the cache was built from and rebuild when any differs (about 10 string-identity compares per line). Add a LootHistory test that flips a global between two parses. File a LootHistory issue citing F-001. Do not add a PrettyChat public API, bus message or chat filter. Verify in-client with SMK-F001 (/etrace arg1 changes with combat state).  
  *Planned in:* PC-22
- **PRETTYCHAT-R-02** `medium` (review F-002 (change C-03); confirmed) — Loot tab copies of LOOT_ITEM_CREATED_SELF/_MULTIPLE are dead settings: saved but never applied; Tradeskill copy always wins  
  *Where:* defaults/Defaults.lua:39, defaults/Defaults.lua:43, defaults/Defaults.lua:329, defaults/Defaults.lua:333, settings/Schema.lua:15-19, modules/Override.lua:280-305, settings/Panel.lua:243, locales/enUS.lua:58, settings/Schema.lua:446-468  
  *Evidence:* Headless probe: Schema.Set('Loot.LOOT_ITEM_CREATED_SELF.format','LOOTEDIT %s') returns true, but live _G stays Tradeskill's format. Disabling Tradeskill's copy restores Blizzard's original even though the Loot copy is enabled and customized. The tooltip says the last category wins 'on /reload', but it wins on every pass. /pc test prints both copies. Four tests pin the current behaviour (test_apply, test_panel, test_schema, test_defaults cross-registration cases).  
  *Remediation:* Keep only the Tradeskill registration. Delete the Loot entries at defaults/Defaults.lua:39-46. Bump SCHEMA_VERSION to 2 with an idempotent profile-scoped step: move categories.Loot.strings[G] to Tradeskill if Tradeskill has none, drop the Loot strings/disabledStrings, prune empty tables, and log one [Migrate] line. Replace the crossRegisteredGlobals block with a load-time assertion that no global is registered twice. Drop the 'Shared with' tooltip branch (Panel.lua:228-247) and its locale key. Update docs (ARCHITECTURE Known Limitations :186, data-flow.md:145, slash-dispatch.md:77, module-map.md:153, smoke-tests T-53). Replace the four tests, and add 'no double registration' and 'migration v2 moves/keeps/idempotent' cases. Regenerate test-cases.md and the README badge in the same commit. Depends on C-02 (F-003).  
  *Rule:* events-frames-taint-§5; savedvariables; testing-§7  
  *Planned in:* PC-04
- **PRETTYCHAT-R-05** `low` (review F-004 (change C-04); confirmed) — NS.OriginalFormat reports PrettyChat's own override as Blizzard's original when the client lacks the global  
  *Where:* modules/Override.lua:589-592, settings/Panel.lua:268-269, docs/common-tasks.md:51  
  *Evidence:* `return (addon and addon.originalStrings and addon.originalStrings[globalName]) or _G[globalName]`. When the snapshot recorded a nil original, the lookup falls through to live _G, which holds the override. The probe returned the PrettyChat-colored Loot string for LOOT_ITEM_SELF with its original set to nil. It shows up in the panel's Original box and in the /pc test Original line. Reachable only after a patch removes or renames a global (PC-R-07 class).  
  *Remediation:* If addon.snapshotKeys[globalName] is set, return addon.originalStrings[globalName] (possibly nil). Otherwise return _G[globalName]. The panel already shows '(original not available)' on nil. Add a test in test_override/test_render: a snapshot key with a nil original answers nil after ApplyStrings (red under the current `or _G[...]`).  
  *Planned in:* PC-07
- **PRETTYCHAT-R-07** `low` (review F-007 (change C-07); confirmed) — Panel New box passes gsub's substitution count into Schema.Set as instanceId  
  *Where:* settings/Panel.lua:281, libs/LibKa0s/Schema.lua:432-478  
  *Evidence:* `NS.Schema.Set(formatPath, (value or ""):gsub("\|\|", "\|"))` is not parenthesized, so the count reaches Set as rid and is threaded into validate/onChange/announce. There is no effect today because nothing reads rid. This is the same defect class as PC-R-10, which Util.lua:17-20 and Panel.lua:270-272 already guard against.  
  *Remediation:* Change it to `NS.Schema.Set(formatPath, ((value or ""):gsub("\|\|", "\|")))`. Add a spy test in tests/test_panel.lua asserting select('#', ...) == 2.  
  *Planned in:* PC-09
- **PRETTYCHAT-A-07** `low` (audit PC-83 (PRETTYCHAT-C-04); corrected) — Authored generator GlobalStrings/split_globalstrings.py is not under tools/  
  *Where:* GlobalStrings/split_globalstrings.py, .pkgmeta:39, DEPENDENCIES.md:146-150, docs/common-tasks.md, docs/global-strings.md, GlobalStrings/README.md, tests/prose_waivers.lua:7, docs/ARCHITECTURE.md:270  
  *Evidence:* layout-§1 (v2.61.0) names this exact file as owing the move. It is not ratified.  
  *Remediation:* git mv GlobalStrings/split_globalstrings.py tools/split_globalstrings.py. In the same commit, change main() so that repo_root = dirname(dirname(abspath(__file__))), input_path = repo_root/GlobalStrings/GlobalStrings.lua, output_dir = repo_root/GlobalStrings, and the TOC path is repo_root/PrettyChat.toc. Run it once and confirm that git diff over GlobalStrings/ is empty. Add '- tools' to .pkgmeta ignore. Update the paths in DEPENDENCIES.md, docs/common-tasks.md, docs/global-strings.md, GlobalStrings/README.md, tests/prose_waivers.lua:7, and the regenerate command inside the ARCHITECTURE.md:270 layout-§2 row. Re-check the three conditions of the layout-§1 generated-data exemption (ARCHITECTURE.md 'Files over the 1500-line cap', which ties the dump's exemption to its generator) against the generator's new location.  
  *Rule:* layout-§1  
  *Planned in:* PC-19


### C44 — PartyFrameEnhanced third-party SavedVariables and packaging

The preview reads EllesmereUIDB, although library-stack-§6 forbids reading other addons' SavedVariables, and the docs deny it. The package ships misspelled PNG screenshots the client cannot load, and .pkgmeta ignores directories that do not exist (AuraMaster too). Affects PartyFrameEnhanced and AuraMaster.

**AuraMaster**

- **AuraMaster-A-15** `info` (audit AM-35; confirmed) — .pkgmeta ignores .claude, but the repo has no .claude directory (false claim)  
  *Where:* .pkgmeta:12  
  *Evidence:* E-9: packaging check (c) prints 'FALSE CLAIM — .claude ignored, no such directory'.  
  *Remediation:* Delete the line, or comment it out with its condition ('#   - .claude  # only in a repo that has one'). Check (c) should then print nothing.  
  *Rule:* packaging (conditional ignore entries)  
  *Planned in:* AM-28

**PartyFrameEnhanced**

- **PartyFrameEnhanced-A-05** `low` (audit PFE-15; confirmed) — The addon reads EllesmereUI's SavedVariables (EllesmereUIDB) to size the preview stand-in, which library-stack-§6 forbids  
  *Where:* modules/Providers.lua:286-302, :293; modules/StandIn.lua:35  
  *Evidence:* ellesmereConfiguredSize() reads EllesmereUIDB.profiles[active].addons.EllesmereUIRaidFrames.partyFrameWidth/Height. The read is nil-guarded and read-only, and it is reached only while unlocked out of a party. There is no register row. This needs the owner's decision.  
  *Remediation:* Owner decision (Sprint 3.4): (a) stop the read, measuring from ERFPartyHeader's child with FALLBACK.ellesmere (125x60) as the fallback; or (b) keep it and add a library-stack-§6 register row with the trigger 'EllesmereUI exposes its configured party size through a frame or API, or its hidden party buttons report party size'. If (b) is chosen, optionally ask WowAddonStandards (Sprint 5.4) whether a presence-guarded, read-only suite SV read under §6's MAY should be permitted by name.  
  *Rule:* library-stack-§6  
  *Planned in:* PF-22
- **PartyFrameEnhanced-R-18** `low` (review F-018; confirmed) — The package ships three PNG screenshots the client cannot load, and their filenames are misspelled  
  *Where:* .pkgmeta; media/screenshots/partframeenhanced.screenshot.0{1,2,3}.png  
  *Evidence:* .pkgmeta ignores media/logos/*.png but not media/screenshots. The files are misspelled 'partframe'. The README links the CurseForge copies instead.  
  *Remediation:* C-008 / T-13: add `- media/screenshots` to the .pkgmeta ignore list. Optionally rename the files to partyframeenhanced.*; nothing in the code or README references them.  
  *Rule:* packaging  
  *Planned in:* PF-17
- **PartyFrameEnhanced-A-15** `info` (audit PFE-21; confirmed) — .pkgmeta ignores two directories that do not exist (.claude, .superpowers)  
  *Where:* .pkgmeta:12-13  
  *Evidence:* Packaging check (c): 'FALSE CLAIM — .claude ignored, no such directory'; the same for .superpowers.  
  *Remediation:* Audit Sprint 3.5: comment both lines out in the template's shape (`#   - .claude   # only when the directory exists`) or delete them.  
  *Rule:* packaging (strong form, branch c)  
  *Planned in:* PF-17


### C45 — AuraMaster container frames and host re-implementations

A reused container id builds a second anchor frame set and leaks the old one. The host also re-implements LibKa0s's tabbed-page and banner chrome (upstream adoption). Single-repo theme in AuraMaster.

**AuraMaster**

- **AuraMaster-R-02** `medium` (review F-001; confirmed) — A reused container id builds a second AuraMasterAnchor<id> frame set and leaks the old one when destroyed out of combat  
  *Where:* modules/Container.lua:43; modules/ContainerManager.lua:85; modules/ContainerManager.lua:107-108; modules/ContainerManager.lua:51-63 (comment)  
  *Evidence:* Only instances parked under CM.MustDefer() are revived. Out of combat, CM.Sync calls inst:Destroy() and drops the instance, and the next build calls NS.Container.New(id), which creates a new anchor/engine/blocker/outline/handle/preview pool and overwrites _G.AuraMasterAnchor<id>. Ids come back on a profile switch between profiles with different container counts, on reset (ResetProfile rewinds nextContainerId) and on copy. tests/test_containermanager.lua:488/:510 cover only the deferred half.  
  *Remediation:* C-01: keep destroyed instances in a dormant[id] table (CM.Sync non-deferred branch: Destroy then dormant[id]=inst; destroyParked moves to dormant). In follow(), add a dormant branch that sets staleData=true and calls revive(id, d, hold); CM.Announce already queues the apply. Add Container:Revive() only if re-Show is needed. Correct the :51-63 comment. New test: A(1-5) -> B(1-2) -> A, where spyCreate 'AuraMasterAnchor3' counts 0 on return and the container draws A's data (red under: dropping the destroyed instance). Regenerate docs/test-cases.md and the README badge. In-client smoke: same table address after the round trip, and no memory climb.  
  *Rule:* events-frames-taint-§2 (no anchor work under lockdown)  
  *Planned in:* AM-03
- **AuraMaster-R-04** `low` (review F-004 (upstream U-1); corrected · upstream → LibKa0s) — The host re-implements LibKa0s's tabbed-page render and page-banner chrome (Helpers.RenderTabbedPage, buildContainerHeader)  
  *Where:* settings/OptionsSetup.lua:659 (RenderTabbedPage), :560 collectTabs, :583 settleActiveTab, :624 renderActiveTab, :480-504 buildContainerHeader (:484 raw Dropdown, :497 raw Button); libs/LibKa0s/OptionsWidgets.lua:3861 O.RenderTabbedSchema; libs/LibKa0s/OptionsTabs.lua:1029 O.PageBanner  
  *Evidence:* The host keeps a second copy of group->tab partitioning, the stale-tab heal, the tab-switch re-render and the banner picker. The library version lacks bespoke (non-row) tabs, a per-container disabled notice, a chrome hook, and a picker+create one-row band (options-ui-§14). Library fixes never reach the seven pages (anti-pattern #47 fork shape). The same hand-built TabStrip shape appears in AbsorbTracker settings/UnitPanel.lua:327, KickCD settings/Panel_Render.lua:208, ConsumableMaster settings/General.lua:402 (+3 files) and MultiMeters settings/Columns.lua:321.  
  *Remediation:* U-1 in LibKa0s: additive fields on O.RenderTabbedSchema (tabs rendered by a host callback and placed before a group; disabledFor(cfg) + disabledNotice; chrome(ctx) hook), and an optional right-half action button on O.PageBanner. Bump the OptionsWidgets and OptionsTabs minors by 1. Existing callers are unchanged. Evaluate it against anti-pattern #55 with the other candidate consumers first. U-2: re-vendor the WHOLE LibKa0s folder into every consumer as its own commit (diff -rq empty), with a revendor bundle. Then C-04b: replace RenderTabbedPage/buildContainerHeader with RenderTabbedSchema(..., {tabs, disabledFor, disabledNotice, chrome}) and PageBanner+action, re-pointing the test_optionssetup and test_pages_* tab cases. Never patch libs/ locally. If U-1 is declined, C-04a: add a documented deviation row in docs/ARCHITECTURE.md with a re-check trigger.  
  *Rule:* library-stack-§5/§7; anti-patterns #47, #55; options-ui-§14  
  *Planned in:* LK-28, AM-17


### C46 — WhatGroup LFG status and minimap row

The terminal LFG application statuses (timedout, invitedeclined, failed) are missing from APPLICATION_ENDED. The minimap row's CLI path global.minimap.hide reads inverted, which traces to the upstream Options row shape. Single-repo theme in WhatGroup.

**WhatGroup**

- **WHATGROUP-R-12** `low` (review F-012; confirmed) — Terminal LFG application statuses (timedout, invitedeclined, failed) missing from APPLICATION_ENDED  
  *Where:* core/WhatGroup.lua:936-941, tests/test_capture.lua  
  *Evidence:* Ends only on declined, declined_full, declined_delisted, cancelled; timed-out/declined-invite captures linger in capturesByResult/pendingApplications until next inviteaccepted or group-leave wipe. Bounded, id-keyed, no cross-invite effect. Status spellings unverified for 12.1.0.  
  *Remediation:* C-010: first record exact status strings in client (/etrace LFG_LIST_APPLICATION_STATUS_UPDATED, smoke S-008), then add them to APPLICATION_ENDED and one tests/test_capture.lua case per status pinning the capture drop; move inventory/badge.  
  *Rule:* testing-§12  
  *Planned in:* WG-07
- **WHATGROUP-R-15** `low` (review F-015; confirmed · upstream → WowAddonStandards) — Minimap row's CLI path global.minimap.hide reads inverted (true while visible)  
  *Where:* settings/Schema.lua:361  
  *Evidence:* /wg get global.minimap.hide answers true while the button is shown; /wg set ... false hides it. Path and inversion mandated by launcher-§3 and options-ui-§15, so WhatGroup is compliant; collection-wide wart.  
  *Remediation:* Upstream U-2: WowAddonStandards rules on a shown-polarity CLI alias for the minimap row while storage stays minimap.hide; if adopted, LibKa0s OptionsCompose/Slash gains an alias field (minor bump) and each addon re-vendors the whole libs/LibKa0s folder in its own commit. No local edit (renaming the path is rejected by launcher-§3).  
  *Rule:* launcher-§3; options-ui-§15  
  *Planned in:* WS-06, WG-11


### C47 — Standard text conflicts and tooling baseline (upstream)

These are upstream-only observations. They cover the options-ui-§15 test-verb rules for the lock-is-preview shape, DebugLog's MAX_BUFFER of 1500 against debug-logging-§1's 500, whether slash-commands-§2 reaches sub-trees, and CreateOptionsPanel adoption. The tooling notes are that ka0s-bounded is not on PATH and the review brief's cross-addon baseline is stale. Reported by AbsorbTracker, ConsumableMaster, KickCD, LootHistory and MultiMeters.

**AbsorbTracker**

- **AbsorbTracker-A-14** `low` (audit AT-76; confirmed · upstream → WowAddonStandards) — /at test verb exists in an addon whose unlocked view is its preview (standard bars a test verb in that shape)  
  *Where:* settings/Slash.lua:109-110, settings/Slash.lua:334-372, settings/General.lua:167-172, README.md:34-36, README.md:120  
  *Evidence:* options-ui-§15 and the preview-mode exception say an addon that uses Lock frame as its preview 'ships no /<slash> test verb either'. /at test is a one-shot value hold, which §15 permits only beside a real test mode (Info-7).  
  *Remediation:* C6/S2.4 branches on the S0.4 standards ruling. If the standard stands, remove 'test' from NS.COMMANDS and move runTestHold to /at debug hold <value> [secs]. In the same change, update README :34-36 and :120 (with a de-AI pass), docs/slash-dispatch.md, docs/smoke-tests.md, test_slashcmds.lua, test_disabled.lua's feature-verb list and docs/test-cases.md. If upstream permits the one-shot value-hold verb, close as compliant. See also R-11 (F-011), whose fix moves with the verb.  
  *Rule:* options-ui-§15, preview-mode, anti-pattern #80  
  *Planned in:* WS-06, AT-11
- **AbsorbTracker-A-21** `info` (audit AT-Info-4; confirmed · upstream → LibKa0s) — Info [upstream]: LibKa0s DebugLog MAX_BUFFER = 1500 versus debug-logging-§1's 500  
  *Where:* libs/LibKa0s/DebugLog.lua:57  
  *Evidence:* lib.MAX_BUFFER = 1500, while the standard says 500.  
  *Remediation:* S0.3: reconcile upstream by changing either the library constant or the standard. Then re-vendor.  
  *Rule:* debug-logging-§1  
  *Planned in:* WS-07
- **AbsorbTracker-A-24** `info` (audit AT-Info-7; corrected) — Info [upstream]: options-ui-§15 permits a one-shot value-hold test beside a test mode but bars any test verb in the lock-is-preview shape  
  *Where:* standard: options-ui-§15, preview-mode  
  *Evidence:* /at test <value> is exactly the permitted one-shot shape, in the one addon shape where it is barred. The outcome decides AT-76.  
  *Remediation:* Resolve AT-76 locally under the existing rule (options-ui-§15 and preview-mode both bar a `test` verb in the lock-is-preview shape). Either remove `/at test <value>`, or add a `## Documented deviations` row in docs/ARCHITECTURE.md. Optionally propose to WowAddonStandards that a one-shot value-hold verb be allowed in that shape, but do not block on it.  
  *Rule:* options-ui-§15, preview-mode  
  *Planned in:* AT-11

**ConsumableMaster**

- **ConsumableMaster-A-04** `low` (audit CM-88; confirmed · upstream → LibKa0s) — The host hand-rolls the settings open, category-ID capture and SetExpanded walk beside LibKa0s-Options-1.0's CreateOptionsPanel and OpenOptionsPanel  
  *Where:* settings/OptionsShim.lua:192-205; settings/OptionsShim.lua:207-236; settings/Panel.lua:1253-1286; settings/OptionsSetup.lua:287; libs/LibKa0s/Options.lua:1322-1347, 1351, 1411  
  *Evidence:* O.Open calls Settings.OpenToCategory(KCM._settingsCategoryID) and privately copies the expand walk. The library's CreateOptionsPanel and OpenOptionsPanel are never called. The host copy is the only one that parks registration in combat, so it cannot be deleted until the library parks. The library's registerMain has no InCombatLockdown check.  
  *Remediation:* Upstream first (A3 / S0-3, LibKa0s-Options-1.0): CreateOptionsPanel refuses and parks under InCombatLockdown. Add O.ReplayPending(). OpenOptionsPanel returns a boolean. Add library tests for park, replay and idempotence. Tag, then re-vendor whole. Then B3 / S3-2: KCM.Options.Open delegates to UI.OpenOptionsPanel. registerPanel delegates to UI.CreateOptionsPanel, with buildMain and RegisterOptionsPage. Delete expandMainCategory and KCM._settingsCategoryID. Use the library's COMBAT_REFUSED wording. Add CreateOptionsPanel, OpenOptionsPanel and ReplayPending as stub no-ops, pinned by test_surface_parity. Rewrite the two registration cases against ReplayPending. If upstream declines, add a Documented deviations row keyed options-ui-§2 with the trigger 'the options library parks registration in combat'.  
  *Rule:* options-ui-§2  
  *Planned in:* LK-25, CM-05
- **ConsumableMaster-R-19** `info` (both Review measurement note + audit tooling note; confirmed · upstream → wow-addon) — ka0s-bounded is not on PATH (it lives at ~/.claude/wow-addon/bin), and the review agent brief's cross-addon baseline table is out of date (it predates AuraMaster, Interface 120100 and the new minors)  
  *Where:* ~/.claude/wow-addon/bin/ka0s-bounded; wow-addon review agent brief (cross-addon baseline)  
  *Evidence:* Every run had to use the full path. The cross-addon result is clean, but differs uniformly from the brief's 2026-09-07 baseline: +2 slash roots, five new majors, Interface 120007 -> 120100.  
  *Remediation:* In the wow-addon plugin: put ka0s-bounded on PATH (or have the agents resolve it by full path), and refresh the cross-addon baseline table in the review agent brief.  
  *Planned in:* WA-02

**KickCD**

- **KICKCD-A-27** `info` (audit KICKCD-C-14; corrected · upstream → WowAddonStandards) — Unclear whether slash-commands-§2's reserved enable/disable verbs reach sub-trees like /kcd spells enable\|disable  
  *Where:* core/KickCD.lua:733-736  
  *Evidence:* §2 says the reserved verbs MUST NOT be reused for anything else, but the standard's own §3 debug example uses enable/disable as sub-arguments. The sub-tree keeps dispatch unambiguous. Not filed as a MUST failure until the standard rules.  
  *Remediation:* Sprint 0.2: ask WowAddonStandards to rule on whether slash-commands-§2's ban ('enabling a module, a feature or a unit is that thing's own verb or row', slash-commands.md:31) reaches sub-tree verbs, citing the text rather than the §3 debug example. Sprint 5.5: if it does, rename /kcd spells enable\|disable to a non-reserved pair such as track/untrack across COMMANDS, help, docs and tests. Otherwise make no change and record the ruling.  
  *Rule:* slash-commands-§2  
  *Planned in:* WS-06, KC-25

**LootHistory**

- **LootHistory-R-19** `info` (review measured non-finding (01 Measurement run; 05 Known follow-ups); confirmed · upstream → wow-addon) — Review agent's cross-addon baseline table (2026-09-07) is out of date  
  *Where:* wow-addon plugin review agent cross-addon baseline  
  *Evidence:* The recorded baseline has 9 addons, the older minors and Interface 120007. Today's measurement: 10 addons (AuraMaster added), 20 slash roots, minors Bus:1 Compat:1 Core:7 DebugLog:12 Env:1 Item:1 Launcher:1 Lifecycle:1 Media:3 Options:23 Perf:12 Pool:3 Schema:1 Slash:14 Widgets:9, and Interface 120100. Every class is still single-valued, so there is no collision.  
  *Remediation:* Refresh the baseline table in the wow-addon plugin's review agent with today's measured values. Nothing changes in LootHistory.  
  *Planned in:* WA-03

**MultiMeters**

- **MultiMeters-R-19** `info` (review Step 0 note / 05_FINAL_SUMMARY Known follow-ups (stale cross-addon baseline); confirmed · upstream → wow-addon) — The review brief's cross-addon baseline is stale (9 addons / 10 majors / 120007, against today's 10 / 15 / 120100)  
  *Where:* wow-addon plugin review brief (cross-addon pass baseline)  
  *Evidence:* The review measured 10 addons, 15 majors and Interface 120100, uniform across the collection. The brief is dated 2026-09-07. This is not an addon defect.  
  *Remediation:* Update the baseline line in the wow-addon review brief wherever it is maintained.  
  *Planned in:* WA-03
- **MultiMeters-R-20** `info` (both review Step 0 note; audit 01_CURRENT_STATE 'Bounded runs' note; confirmed · upstream → wow-addon) — ka0s-bounded is installed at ~/.claude/wow-addon/bin but is not on PATH  
  *Where:* ~/.claude/wow-addon/bin/ka0s-bounded  
  *Evidence:* Both runs found it missing from PATH and invoked it by absolute path. No run needed the timeout 900 fallback.  
  *Remediation:* Have the wow-addon plugin put ka0s-bounded on PATH, or have its briefs resolve the absolute path. No addon change.  
  *Planned in:* WA-02

## Rejected by verification

- **AuraMaster-A-19** (AuraMaster) — Propose docs/spell-research/ for documentation-§3's canonical list of frozen stores. *Why rejected:* The finding's premise is that repos can't extend the list, so an addon-owned store needs an upstream change. The standard says the opposite. WowAddonStandards/standards/standards/documentation.md:350-354 says the list is upstream only 'because these stores are written by a command shared across every repo'. It then says 'it takes nothing from Tier 3: a frozen store that is genuinely one addon's own still ships under any name that addon picks, with no upstream change needed to create it.' docs/spell-research/ is written by AuraMaster's own tools/spell-research/research.py, not by a shared command, so it fails the list's stated admission criterion. AuraMaster already names the store once, in the out-of-scope sentence at AuraMaster/docs/ARCHITECTURE.md:778-781. Any leftover placement question is the local Tier 3 item (AuraMaster-A-07). Nothing needs to be proposed upstream.
- **MultiMeters-A-08** (MultiMeters) — No suite case pins a wrapped tab strip's geometry against the selection. *Why rejected:* The invariant is already pinned where the code lives. LibKa0s/tests/test_options_tabs.lua:573 has 'a wrapped strip's geometry is IDENTICAL for every value of the selection'. The same file also has :802 (the sub-strip variant), :615 (the hit-rect inset matches the pitch), :636 (the pitch is measured off the INACTIVE family) and :144 (__tabBand). Line 575 names this exact bug. The code under test is libs/LibKa0s/OptionsTabs.lua:691/729/789, which is vendored library code. It belongs to, and is already covered by, LibKa0s's own suite. An addon-side copy that drives the vendored __ seams would duplicate upstream coverage. MultiMeters has no wrapping page, so it adds no addon-specific signal. The grep being empty in MultiMeters/tests is accurate, but that is not a defect.
- **PanelMaster-A-20** (PanelMaster) — The ka0s-bounded runner is not on PATH; both runs had to call it by absolute path. *Why rejected:* This is not a defect, because the plugin never puts the runner on PATH by design. wow-addon/CLAUDE.md:23 says the hook refreshes the `~/.claude/wow-addon/bin/ka0s-bounded` symlink as 'the one path specs name, stable across plugin-cache version directories'. wow-addon/README.md:48, agents/standards-audit.md:329 and commands/automated-tests.md:75-76 all call the runner by that absolute path. `which ka0s-bounded` failing is therefore expected. The finding's own evidence says every run used the absolute path and none failed. Its optional remediation (have the skills always call the runner by absolute path) describes what the plugin already does.
