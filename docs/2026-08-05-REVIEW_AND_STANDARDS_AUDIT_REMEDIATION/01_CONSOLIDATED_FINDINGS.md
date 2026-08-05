# 01 — Consolidated Findings

**254 surviving triaged findings across 9 repositories, grouped by cluster then by repo.**

Nothing here has been executed. See `00_OVERVIEW.md`.

---

## How to read this

| Column | Meaning |
|---|---|
| **Repo** | Which repository the finding is against. |
| **ID** | Stable consolidated id. `<repo>-R-nn` = review bundle, `<repo>-A-nn` = audit bundle. |
| **Src** | `R` = `docs/reviews/2026-08-05/`, `A` = `docs/audits/2026-08-05/`. |
| **Sev** | **Triaged** severity — reachable impact, not the strength of the rule broken. |
| **Evidence** | The leading `file:line` citation, re-opened during triage. Paths are relative to the repo. |
| **Rule** | The `filename-§N` section, where one applies. Blank means no rule was violated — the finding is a defect or a hygiene item that no section governs. |

**Severity rubric used by triage.** Critical = data loss, taint propagation, SavedVariables corruption,
or a failure to load a normal install reaches. High = a user, their saved variables or their session
can hit it today. Medium = real but narrow, self-correcting, or an integrity gap in the record rather
than in shipped behavior. Low = doc-only, config-only, or unreachable in any shipping configuration.
Info = no defect behind it.

**Section references** use `filename-§N` only. The global `§N.M` numbering is retired; where a finding's
original bundle used it, the reference below is normalized. Where a bundle cited a section number that
does not exist (`standalone-windows-§2`, `packaging-§1` — neither file carries numbered subsections),
the bare filename is used and the discrepancy is itself carried by cluster **C15**.

**Severity totals:** Critical 0 · High 8 · Medium 30 · Low 173 · Info 43 · **Total 254**.
Seven C6 rows moved Medium → Low in adversarial review — one byte-identical defect had carried two
severities across ten findings, and the reachability is identical in all six repos. See C6 and
`00_OVERVIEW.md` § Adversarial review.

---

# Part 1 — Clustered findings (224)

A cluster is one problem seen from several repositories. Clusters spanning three or more repos are
marked **[COLLECTION]** — treating those as N independent findings is the single largest source of
inflated counts in the bundles.

---

## C1 · Perf harness unadopted, re-filed as 5–7 MUSTs per repo — 40 findings, 8 repos [COLLECTION]

`performance-§1` makes wiring `LibKa0s-Perf-1.0` an unconditional MUST. Six further sections then each
derive a separate MUST from it (`toc-file-§2`, `slash-commands-§2`, `performance-§5`, `performance-§6`,
`performance-§9`, `documentation-§3`). Five addons declined the harness with recorded, evidence-backed
reasons. One decision becomes 40 findings, because the standard has no *declined with recorded cause*
state.

### BankLedger — 7

| Repo | ID | Src | Sev | Evidence | Rule |
|---|---|---|---|---|---|
| BankLedger | BL-A-02 | A | Medium | no `core/PerfSetup.lua`; decline at `docs/pending/LEDGER.md:65` | `performance-§1` |
| BankLedger | BL-A-03 | A | Low | `BankLedger.toc:7` — one SavedVariables global | `toc-file-§2` |
| BankLedger | BL-A-04 | A | Low | `settings/Schema.lua:226-286` — no `perf` verb | `slash-commands-§2` |
| BankLedger | BL-A-05 | A | Info | `.luacheckrc` — no `debugprofilestop`, no `BankLedgerPerfDB` | `lint` |
| BankLedger | BL-A-06 | A | Low | `ls docs` — no `performance.md`, no `perf-runs/` | `documentation-§3` |
| BankLedger | BL-A-07 | A | Low | `ls tests/perf.lua` → absent | `performance-§9` |
| BankLedger | BL-A-08 | A | Info | no suspend flag in `core/State.lua`; no `NS.Perf` consumer | `performance-§6` |

### LootHistory — 7

| Repo | ID | Src | Sev | Evidence | Rule |
|---|---|---|---|---|---|
| LootHistory | LH-A-20 | A | Medium | no `core/PerfSetup.lua` in `LootHistory.toc:16-58` | `performance-§1` |
| LootHistory | LH-A-21 | A | Low | `LootHistory.toc:7` — one SavedVariables global | `toc-file-§2` |
| LootHistory | LH-A-22 | A | Low | `settings/Schema.lua:213-245` — 14 verbs, no `perf` | `slash-commands-§2` |
| LootHistory | LH-A-23 | A | Low | no `suspend`/`resume` symbol in `core/`, `modules/`, `settings/` | `performance-§6` |
| LootHistory | LH-A-24 | A | Medium | `ls tests/perf.lua` → absent; `docs/automated-tests/RESULTS.md` perf column all `skip` | `automated-tests-§3` |
| LootHistory | LH-A-25 | A | Low | `ls docs/` — no `performance.md` | `documentation-§3` |
| LootHistory | LH-A-26 | A | Low | `.luacheckrc:10-40` no `debugprofilestop`; `:42-45` no `LootHistoryPerfDB` | `performance-§5` |

### PanelMaster — 7

| Repo | ID | Src | Sev | Evidence | Rule |
|---|---|---|---|---|---|
| PanelMaster | PM-A-01 | A | Medium | no `core/PerfSetup.lua`; `CLAUDE.md:36` "`Perf` is declined." | `performance-§1` |
| PanelMaster | PM-A-02 | A | Low | `settings/Slash.lua:214-267` — 18 verbs, no `perf` | `performance-§4` |
| PanelMaster | PM-A-03 | A | Low | `PanelMaster.toc:7` — one SavedVariables global | `toc-file-§2` |
| PanelMaster | PM-A-04 | A | Low | `ls tests/perf.lua` → absent; manifest of `20260804-233329` records `perf: skip` | `performance-§9` |
| PanelMaster | PM-A-05 | A | Low | no `docs/performance.md`, no `docs/perf-runs/`; `docs/automated-tests/README.md:44` links `../perf-runs/` | `documentation-§3` |
| PanelMaster | PM-A-06 | A | Info | `.luacheckrc:9-21` no `debugprofilestop`; `:22-27` no `PanelMasterPerfDB` | `performance-§2` |
| PanelMaster | PM-A-09 | A | Low | grep `suspend` over `core modules settings` → no hit | `performance-§6` |

### WhatGroup — 6

| Repo | ID | Src | Sev | Evidence | Rule |
|---|---|---|---|---|---|
| WhatGroup | WG-A-01 | A | Low | no `core/PerfSetup.lua`; `WhatGroup.toc:26-33`; decline at `docs/pending/LEDGER.md:63` (LIBKA0S-15, 2026-08-02) | `performance-§1` |
| WhatGroup | WG-A-02 | A | Low | `WhatGroup.toc:7` — one SavedVariables global | `toc-file-§2` |
| WhatGroup | WG-A-03 | A | Low | `settings/Slash.lua:44-67` — 11 verbs, no `perf` | `slash-commands-§2` |
| WhatGroup | WG-A-04 | A | Low | `ls docs/` — no `performance.md`, no `perf-runs/` | `documentation-§3` |
| WhatGroup | WG-A-05 | A | Low | `ls tests/perf.lua` → absent; manifest `20260804-233335` records skip | `performance-§9` |
| WhatGroup | WG-A-06 | A | Info | `.luacheckrc:18-21` no `WhatGroupPerfDB`; `:25-39` no `debugprofilestop` | `performance-§2` |

### prettychat — 5

| Repo | ID | Src | Sev | Evidence | Rule |
|---|---|---|---|---|---|
| prettychat | PC-A-02 | A | Low | `libs/LibKa0s/Perf.lua` vendored; `ls core/` no `PerfSetup.lua`; decline at `CLAUDE.md:6` and `docs/pending/LEDGER.md:66` | `performance-§1` |
| prettychat | PC-A-03 | A | Low | `PrettyChat.toc:7` — one SavedVariables global | `toc-file-§2` |
| prettychat | PC-A-04 | A | Info | `settings/Slash.lua:45-70` — 10 verbs, no `perf` | `slash-commands-§2` |
| prettychat | PC-A-05 | A | Info | `ls tests/perf.lua` → absent; manifest `20260804-233338:15` records skip | `performance-§9` |
| prettychat | PC-A-06 | A | Low | `ls docs/` — no `performance.md`, no `perf-runs/` | `documentation-§3` |

### ConsumableMaster — 4 (harness **is** wired; these are genuine residual gaps)

| Repo | ID | Src | Sev | Evidence | Rule |
|---|---|---|---|---|---|
| ConsumableMaster | CM-A-06 | A | Medium | `ls tests/perf.lua` → absent; brackets at `core/ConsumableMaster.lua:332-333,349` and `modules/MacroBar.lua:322-323,330` | `performance-§9` |
| ConsumableMaster | CM-A-09 | A | Low | `ConsumableMaster.toc:11` declares `ConsumableMasterPerfDB`; `.luacheckrc:30-34` does not | `performance-§5` |
| ConsumableMaster | CM-A-10 | A | Low | `ls docs/` — no `performance.md` | `documentation-§3` |
| ConsumableMaster | CM-A-11 | A | Low | `ls docs/` — no `perf-runs/` directory | `documentation-§3` |

### KickCD — 3 (harness **is** wired)

| Repo | ID | Src | Sev | Evidence | Rule |
|---|---|---|---|---|---|
| KickCD | KCD-R-07 | R | Low | `core/PerfSetup.lua:104-118` cites "125.02 ms … 51.14 … 73.9 ms" with no capture in the repo | `performance-§8` |
| KickCD | KCD-A-05 | A | Medium | `ls tests/perf.lua` → absent; manifest `20260804-233245` records `perf: skip` | `performance-§9` |
| KickCD | KCD-A-06 | A | Low | `ls docs/` — no `performance.md`, no `perf-runs/` | `documentation-§3` |

### LibKa0s — 1

| Repo | ID | Src | Sev | Evidence | Rule |
|---|---|---|---|---|---|
| LibKa0s | LK-A-13 | A | Info | `ls tests/perf.lua` → absent; `performance.md:112-125` keeps scenarios per-addon | `performance-§9` |

---

## C2 · Degraded-install (library-absent) paths raise or lie — 13 findings, 5 repos [COLLECTION]

Degradation stubs are hand-written per addon with no shared contract test. A stub that omits one member
converts a graceful fallback into a crash on a rarer path. **Contains 5 of the 8 collection Highs.**

| Repo | ID | Src | Sev | Evidence | Rule |
|---|---|---|---|---|---|
| ConsumableMaster | CM-R-01 | R | **High** | `settings/Panel.lua:571` binds `Helpers.RefreshAllPanels = UI and UI.RefreshAllPanels`; bare call at `:833`; reproduced: `attempt to call field 'RefreshAllPanels' (a nil value)` | `options-ui-§1` |
| ConsumableMaster | CM-R-02 | R | **High** | `settings/Panel.lua:572` / `:643` — raises *after* `Helpers.Set` at `:640` and `fireOnChange` at `:641`; reproduced with `ok=false` | `options-ui-§1` |
| ConsumableMaster | CM-A-25 | A | **High** | `settings/Panel.lua:571-572`, `:643`, `:833`, bus receiver `:940-943` fed by `core/ConsumableMaster.lua:313` | `options-ui-§1` |
| ConsumableMaster | CM-A-32 | A | **High** | `settings/Slash.lua:341` `if not Sl then return printHelp() end`; 17 verbs at `:66-170`, 11 of which never used the library | `slash-commands-§1` |
| PanelMaster | PM-R-01 | R | **High** | `settings/Slash.lua:285` opens the stub, returns at `:316` without `FormatKV`; assigned live at `:381`; call sites `:101, :124, :125, :181, :188`; reproduced | `slash-commands-§1` |
| ConsumableMaster | CM-R-03 | R | Medium | `settings/Panel.lua:265-271` vs `settings/Slash.lua:300-303` and `:341` | `slash-commands-§1` |
| PanelMaster | PM-R-03 | R | Low | `core/DebugLogSetup.lua:137` hand-copies the ack; library ACK/STATE at `libs/LibKa0s/DebugLog.lua:68-70`, hexes at `:635-636` | `debug-logging-§7` |
| PanelMaster | PM-R-07 | R | Low | `settings/OptionsSetup.lua:35-40` latches `said`, `:49` binds `OpenOptionsPanel = explain`; reproduced — call #1 emits 2 lines, #2 and #3 emit 0 | `slash-commands-§1` |
| KickCD | KCD-A-14 | A | Low | `core/DebugLogSetup.lua:94-96` returns `<ts> \| [<tag>] <msg>`, byte-identical to `libs/LibKa0s/DebugLog.lua:93-94` | `debug-logging-§7` |
| LootHistory | LH-R-06 | R | Low | `tests/test_libka0s.lua:90-102` is the only stub-surface walk; `settings/Slash.lua:210` exports `HelpHeader`, degraded block `:129-163` does not | `testing-§8` |
| LootHistory | LH-A-39 | A | Low | same asymmetry, correctly cited: `settings/Slash.lua:210` vs `:129-163` | `testing-§8` |
| LootHistory | LH-R-10 | R | Low | `settings/Slash.lua:150-157` — bare `/lh` falls to `unavailable()` at `:135-137` although 7 verbs still dispatch | `slash-commands-§3` |
| prettychat | PC-R-09 | R | Info | `settings/OptionsSetup.lua:90-95` comment; consumers `settings/Panel.lua:275`, `:138`, `:347`, all guarded by `if not scroll then return end` | `options-ui-§8` |

---

## C3 · Stale comments naming deleted files or wrong callers — 13 findings, 8 repos [COLLECTION]

No gate ties a comment's named file or caller to reality. `sync-docs` checks docs, never code comments.

| Repo | ID | Src | Sev | Evidence | Rule |
|---|---|---|---|---|---|
| AbsorbTracker | AT-R-11 | R | Low | `modules/Bar.lua:5-6` and `:86-87` name `core/DebugLog.lua`; `ls core/` shows `DebugLogSetup.lua` only | `documentation-§5` |
| BankLedger | BL-R-05 | R | Low | `settings/Panel.lua:11` is self-referential ("`O.AceGUI` is reached through `O.AceGUI`"); `:13, :21, :23, :302, :402` carry it | |
| BankLedger | BL-R-07 | R | Low | blank runs `settings/Panel.lua:39-42, 61-67, 77-80, 119-120, 171-173`; paragraph written twice at `:471-473` and `:474-476` | |
| ConsumableMaster | CM-R-11 | R | Low | `modules/DebugLog.lua:97-99` names `KCM.DebugLog.AddLine`; `core/Debug.lua:39-40` reads `DL and DL.instance` | `debug-logging-§1` |
| ConsumableMaster | CM-R-13 | R | Info | `core/ConsumableMaster.lua:328` "the 13-category walk"; `defaults/Categories.lua:42` has 15 `key =` entries | |
| KickCD | KCD-R-09 | R | Low | `core/PerfSetup.lua:108` "All four of PollSpell's exits"; `modules/Cooldowns.lua:179` says TWO, returns at `:196` and `:202` | |
| KickCD | KCD-R-10 | R | Low | `settings/Slash.lua:211` cites `(settings/Slash.lua:383)` in a 347-line file; repeated at `tests/test_coresetup.lua:360` | |
| LootHistory | LH-R-07 | R | Low | `settings/Slash.lua:111-112` and `:165-167` name `settings/Panel.lua` as a reader of `FormatSchemaValue`/`FormatKV`; it reads neither | |
| PanelMaster | PM-R-09 | R | Low | `core/CoreSetup.lua:21` lists `modules/DebugLog.lua`; `ls modules/` shows Artwork, Canvas, Registry, SunnArt, SunnArtPacks, Unlock | |
| PanelMaster | PM-R-10 | R | Low | `tests/test_vendor_sync.lua:29-31` asserts a `.gitattributes` pin of `* text=auto eol=crlf`; the file carries only `*.sh text eol=lf` | |
| prettychat | PC-R-10 | R | Info | `settings/Panel.lua:182` and `:248` leak `gsub`'s count into `SetText`; the cited comparator `core/Util.lua:18` is itself unparenthesized | |
| LibKa0s | LK-R-02 | R | Low | `docs/releasing.md:146` claims a gate `tests/test_versioning.lua:107-128` does not implement (CHANGELOG only) | |
| LibKa0s | LK-A-15 | A | Low | same: `docs/releasing.md:146`; `tests/test_kitsync.lua:81-94` is the only API-document gate | `documentation-§5` |

---

## C4 · Ratified deviations re-filed as open findings — 12 findings, 5 repos [COLLECTION]

The audit playbook has no way to read `docs/pending/LEDGER.md`, an ARCHITECTURE "Documented deviations"
block, `docs/scope.md` or a `CLAUDE.md` deviation paragraph as *closing* a rule.

| Repo | ID | Src | Sev | Evidence | Rule |
|---|---|---|---|---|---|
| AbsorbTracker | AT-A-12 | A | Low | `docs/ARCHITECTURE.md:277-282, :283-296, :297-306, :307-315` list four behaviors the standard now sanctions; three marked "Pending promotion" for a shipped rollout | `documentation-§5` |
| ConsumableMaster | CM-A-01 | A | Info | `docs/scope.md:20` records the enUS tooltip-parsing deviation; classification already on classID/subClassID at `core/Classifier.lua:167-170` | `localization-§4` |
| ConsumableMaster | CM-A-16 | A | Info | The within-`core/` load sequence does not begin `Compat → Constants → Namespace`: `ConsumableMaster.toc:48-58` orders `Namespace → ConsumableMaster → Bus → Constants → CoreSetup → Compat → State → Database`. The rationale is written at `ConsumableMaster.toc:44-47` and `:53-55` (Namespace bootstraps `KCM`; CoreSetup needs `KCM.PREFIX` from Constants). `toc-file-§5`'s only MUST is the **section-header** order — Libraries → Locales → Core → Defaults → Modules → Settings — which this TOC satisfies; the within-section file sequence is illustrative in the section's code block, not an ordered MUST. Filed by the audit as **CM-49** against `layout-§1` | `toc-file-§5` |
| prettychat | PC-A-01 | A | Low | `PrettyChat.toc:42-68` `# GlobalStrings` section; recorded at `CLAUDE.md:8` | `layout-§2` |
| prettychat | PC-A-14 | A | Info | `settings/Panel.lua:127-128` `LEFT_W = 0.4` / `RIGHT_W = 0.6`; justified in-code, at `CLAUDE.md:11` and `docs/pending/LEDGER.md:60` | `options-ui-§6` |
| prettychat | PC-A-15 | A | Info | `PrettyChat.toc:2` rainbow Title, `:4` stylized Author; recorded at `CLAUDE.md:10` | `toc-file-§1` |
| prettychat | PC-A-18 | A | Info | `core/Constants.lua:54-60` hands the vendored font path straight to the descriptor; rationale at `CLAUDE.md:9` | `debug-logging-§2` |
| prettychat | PC-A-21 | A | Info | `library-stack.md:13-14` lists AceEvent/AceTimer as vendored; `:39` MUSTs vendoring only what is LibStub'd. Noted at `DEPENDENCIES.md:118-119` | `library-stack-§1` |
| prettychat | PC-A-22 | A | Info | `PrettyChat.toc:10` `Category-enUS: Chat & Communication`; `toc-file.md:19` enumerates six values | `toc-file-§1` |
| PanelMaster | PM-A-18 | A | Info | `README.md:58-60` `## Screenshots` placeholder; unreleased at 0.1.0 | `documentation-§1` |
| PanelMaster | PM-A-19 | A | Info | `PanelMaster.toc:1-12` no `X-Curse-Project-ID`; `README.md:3-6` four badges, no published-version badge | `toc-file-§1` |
| PanelMaster | PM-A-20 | A | Info | `docs/pending/LEDGER.md` exists; no root `TODO.md` | `documentation-§4` |

**`WG-A-13` was in this cluster and does not belong here.** Nothing ratifies it — there is no register
row, no ledger entry and no in-code rationale. It is a genuinely unmet `debug-logging-§2` SHOULD and is
re-filed as a WhatGroup one-off (Part 2), closing at `M4-24`.

**`CM-A-16`'s row carried `CM-A-23`'s evidence verbatim** in an earlier draft of this document — the
`.pkgmeta` ignore-list text — which erased the finding while leaving the id in the coverage proof. The
row above is the real finding, restored from `ConsumableMaster/docs/audits/2026-08-05/02_DEVIATIONS.md:36`
(**CM-49**). Its disposition is a register row at `M3-08` plus the `toc-file-§5` clarification in
`M1-STD-15`; the ratification here lives in the TOC's own comments rather than in a register, which is the
same reading failure the rest of C4 describes.

---

## C5 · README / CLAUDE.md canonical shape — 12 findings, 8 repos [COLLECTION]

`documentation-§1` fixes **twelve** README sections in this order — H1 title, badge row, logo, description,
`## What's new`, `## Screenshots`, `## Usage`, `## How <it> works`, `## FAQ`, `## Troubleshooting`,
`## Issues and feature requests`, `## Version History`. `documentation-§2` fixes a **five-item** CLAUDE.md
stub — H1 title, adherence line, `## Standards compliance (read first)`, the "read the docs" pointer list,
the green-gate line. Nothing enforces either. **`CM-A-26` is not repo drift** — it is a genuine standard-versus-tooling
contradiction.

| Repo | ID | Src | Sev | Evidence | Rule |
|---|---|---|---|---|---|
| ConsumableMaster | CM-A-26 | A | Low | root ships CHANGELOG.md, CLAUDE.md, DEPENDENCIES.md, LICENSE, README.md; `documentation.md:5` — "exactly three docs plus LICENSE … never a fourth"; `bump-version` is specified to write the CHANGELOG entry | `documentation-§1` |
| AbsorbTracker | AT-A-01 | A | Low | `README.md:15-24` eight `## What's new in 1.9.0` bullets vs `README.md:159` four Version History highlights, none of them the first four | `documentation-§1` |
| AbsorbTracker | AT-A-04 | A | Low | `CLAUDE.md:40-41` — "Four of those topic-detail docs are required" then lists five | `documentation-§3` |
| ConsumableMaster | CM-A-17 | A | Low | `CLAUDE.md:1` is `# CLAUDE.md`; `documentation-§2` item 1 pins `# CLAUDE.md — Ka0s <Name>` | `documentation-§2` |
| KickCD | KCD-A-07 | A | Low | `README.md:191` renders `/kcd reset <setting>`; `:75` already uses the bare form | `documentation-§1` |
| LootHistory | LH-A-38 | A | Low | `CLAUDE.md` is 102 lines with sections at `:24`, `:55`, `:89` beyond `documentation-§2`'s five items | `documentation-§2` |
| PanelMaster | PM-A-12 | A | Low | `README.md:138-152` renders `\| Setting \| What it does \|`; item 7 requires `Tab \| Covers` | `documentation-§1` |
| prettychat | PC-A-08 | A | Low | `README.md:116` contains `` `/pc reset <setting>` ``; `:63` is correct | `documentation-§1` |
| prettychat | PC-A-09 | A | Low | `README.md:15` `## Unreleased` and `:120` `## Credits` are outside the twelve permitted sections | `documentation-§1` |
| prettychat | PC-A-10 | A | Low | `CLAUDE.md` is 63 lines; `:5-13` six deviation paragraphs precede `## Standards compliance (read first)` at `:14`, which is item 3 | `documentation-§2` |
| WhatGroup | WG-A-10 | A | Low | `README.md:81` `## Bundled libraries` sits between `## How it works` (`:75`) and `## FAQ` (`:85`) | `documentation-§1` |
| LibKa0s | LK-A-11 | A | Low | `README.md:196-231` omits `docs/automated-tests/` and `docs/audits/`, both present on disk | `documentation-§5` |

---

## C6 · Vendor-sync gate PASSes without looking — 10 findings, 6 repos [COLLECTION]

Identical `if not tag then return end` in all six. A bare `return` registers as PASS. **Verified: `Kit.skip`
does not exist in `LibKa0s/testkit/framework.lua` (`Kit.VERSION = 7`)** — there is no honest local fix.

**One severity for all ten, re-graded here.** The source bundles graded the same byte-identical defect
Low in three repos and Medium in seven, and the split was inherited rather than reasoned. The reachability
line is identical in every one of the six: *the skip branch fires only in a clone that has no `../LibKa0s`
sibling; `../LibKa0s` is present on this machine, and no repo in the collection has CI or a git hook that
would run the suite anywhere else.* Under this plan's rubric — impact, not rule strength — that is **Low**
in all ten. (This is the re-grading pass `M1-WA-08` exists to make routine.)

| Repo | ID | Src | Sev | Evidence | Rule |
|---|---|---|---|---|---|
| AbsorbTracker | AT-R-13 | R | Low | `tests/test_vendor_sync.lua:111-116`, `:138-141`, `:144-147`; header at `:106-109` claims the skip is in the case name | `testing` |
| BankLedger | BL-R-02 | R | Low | `tests/test_vendor_sync.lua:110-118`, `:138-140`, `:144-146`; `testing.md:234-235` | `testing-§11` |
| BankLedger | BL-A-14 | A | Low | `tests/test_vendor_sync.lua:110-111`, `:138-140`, `:144-146`; header `:105-108` | `testing-§12` |
| ConsumableMaster | CM-R-07 | R | Low | `tests/test_vendor_sync.lua:140-141`, `:146-147`; `siblingTag` nil at `:112`; header `:108-110` | `testing-§12` |
| ConsumableMaster | CM-A-31 | A | Low | `tests/test_vendor_sync.lua:140-141`, `:146-147` | `testing-§11` |
| KickCD | KCD-R-02 | R | Low | `tests/test_vendor_sync.lua:110-116`, `:138-142`, `:144-149`; comment `:107-109` | `testing-§12` |
| KickCD | KCD-A-12 | A | Low | same lines; `../LibKa0s` exists on this machine, so the skip branch has no live trigger here | `testing-§12` |
| LootHistory | LH-R-05 | R | Low | `tests/test_vendor_sync.lua:110-116`, `:138-142`, `:144-150`; case names `:137`, `:143` | `testing-§11` |
| LootHistory | LH-A-40 | A | Low | same lines; header claim at `:105-109` | `testing-§11` |
| PanelMaster | PM-R-05 | R | Low | `tests/test_vendor_sync.lua:110-116`; guards at `:140` and `:146` (both bundles cite `:138`/`:144`, the `test(` lines) | `testing-§12` |

**The CRLF `gsub` in these files is correct and MUST survive the rewrite.** An earlier draft filed
ConsumableMaster's `tests/test_vendor_sync.lua:133` as a second defect under `CM-A-31`. It is not one.
The gate compares a **working-tree** file against a **`git show` blob**: the blob is LF
(`git -C LibKa0s show HEAD:LibKa0s/Core.lua | tr -cd '\r' | wc -c` → **0**) while the working tree is
CRLF (`tr -cd '\r' < AbsorbTracker/libs/LibKa0s/Core.lua | wc -c` → **322**), because eight of the nine
repos pin `text=auto eol=crlf` (or `*.lua text eol=crlf`) in `.gitattributes`. Stripping CR from the
working-tree side compares the file to the blob it round-trips to; AbsorbTracker's own header says so at
`tests/test_vendor_sync.lua:28-32`. Removing it reddens the gate in every repo on the commit that adopts
it. `testing-§11`'s no-normalization MUST is written for the **library-side** pair, where `testkit/` and
`tests/_kit/` are two working-tree directories in one checkout; `M1-STD-03` scopes it accordingly.

---

## C7 · Dead exported surface — 10 findings, 8 repos

No dead-export gate in the shared kit, so per-repo cleanup is endless.

| Repo | ID | Src | Sev | Evidence | Rule |
|---|---|---|---|---|---|
| AbsorbTracker | AT-R-09 | R | Info | `core/Units.lua:36-42` and `core/Database.lua:26-31` identical copies; `settings/Schema.lua:158-164` comment names an operation the loop does not perform | |
| AbsorbTracker | AT-R-10 | R | Low | `core/Units.lua:78-85` names the slash CLI as sole caller; `Units.Set` has zero callers repo-wide; `docs/file-index.md:100` compounds it | `documentation-§5` |
| BankLedger | BL-R-03 | R | Low | `core/Compat.lua:184`, `core/Database.lua:551`, `modules/Filters.lua:40,45`, `modules/Insights.lua:30,52`; false comment at `core/Database.lua:550` vs real delete at `modules/LedgerTable.lua:1005` | |
| ConsumableMaster | CM-R-09 | R | Low | `core/TooltipCache.lua:147` declared, `:448, :463, :480` written, no read anywhere | |
| ConsumableMaster | CM-R-12 | R | Info | `modules/MacroBar.lua:288-290`; grep returns only the definition | |
| KickCD | KCD-R-11 | R | Info | `modules/Castbar.lua:1312` `NS.Castbar = Castbar`; grep returns only that assignment | |
| KickCD | KCD-R-12 | R | Info | `.luacheckrc:29` allowlists `InterfaceOptionsFrame_OpenToCategory`; addon uses `Settings.OpenToCategory` at `core/KickCD.lua:757` | `lint` |
| PanelMaster | PM-R-08 | R | Low | `core/CoreSetup.lua:86` `NS.Format = printer.Format` is the only occurrence; stub at `:34-69` omits it | |
| WhatGroup | WG-R-08 | R | Info | `core/CoreSetup.lua:76-82` fallback and `:135` assignment; zero callers | |
| LootHistory | LH-A-33 | A | Low | `media/logos/wowhead-logo.png` referenced only in two retired plan docs | `layout-§3` |

---

## C8 · Release gate undocumented — 9 findings, 9/9 repos [COLLECTION]

**Machine-generated.** `LibKa0s/testkit/run-automated-tests.sh:372` emits `**lint and tests gate. perf and
complexity are recorded and never fail a run**` into every `RESULTS.md`; `:322-323` hardcode `"gating": false`.
Every cited sentence is true about a run and none names the tag checkpoint.

| Repo | ID | Src | Sev | Evidence | Rule |
|---|---|---|---|---|---|
| AbsorbTracker | AT-A-07 | A | Low | `docs/testing.md:22, :47, :49, :57-58`; `docs/automated-tests/RESULTS.md:9-11` generated by the runner | `automated-tests-§3` |
| BankLedger | BL-A-12 | A | Low | `docs/testing.md:44-56` Release checklist has no manifest/CCN item; `docs/automated-tests/README.md:20-31` | `automated-tests-§3` |
| ConsumableMaster | CM-A-28 | A | Low | `docs/testing.md:145-146, :148, :156-157`; `CLAUDE.md:71` "It is a **report, not a gate**" | `automated-tests-§3` |
| KickCD | KCD-A-13 | A | Low | `docs/testing.md:86-99`; `CLAUDE.md:74` "Complexity — recorded, never a gate" | `automated-tests-§3` |
| LootHistory | LH-A-36 | A | Low | `docs/testing.md:164-176`, `docs/automated-tests/README.md:19-31`, `RESULTS.md:9-11` | `automated-tests-§3` |
| PanelMaster | PM-A-13 | A | Low | `docs/testing.md:116-121, :123, :131`; `docs/automated-tests/README.md:19-32`; `CLAUDE.md:46-50` | `automated-tests-§3` |
| prettychat | PC-A-13 | A | Low | `docs/testing.md:111-112`; `docs/automated-tests/README.md:19-29`; `RESULTS.md:11-13` | `automated-tests-§3` |
| WhatGroup | WG-A-14 | A | Low | `docs/testing.md:220, :228-229`; `docs/automated-tests/README.md:28`; `RESULTS.md:9`; `DEPENDENCIES.md:92` | `automated-tests-§3` |
| LibKa0s | LK-A-08 | A | Low | `docs/automated-tests/README.md:27-36`; `RESULTS.md:9-11` (the second is runner-emitted) | `automated-tests-§3` |

---

## C9 · Perf bracket shape and API — 9 findings, 4 repos

`performance-§2` and `performance-§3` specify an idiom; nothing verifies descriptor truthfulness or
bracket closure on an early return. The library's own docstring and `performance-§2` currently specify
**different shapes**.

| Repo | ID | Src | Sev | Evidence | Rule |
|---|---|---|---|---|---|
| AbsorbTracker | AT-R-01 | R | Medium | `core/PerfSetup.lua:46-47` `within = "repaintPass"` on both; `modules/Timer.lua:33-35`; `modules/Display.lua:59, :158, :216-221`; `docs/perf-runs/2026-07-30-ingame-post-extraction.json` | `performance-§3` |
| ConsumableMaster | CM-A-07 | A | Low | `core/ConsumableMaster.lua:332` `local perf = KCM.Perf` inside `P.Recompute`; same at `modules/MacroBar.lua:322` | `performance-§2` |
| ConsumableMaster | CM-A-08 | A | Low | `modules/PerfSetup.lua:97-100` declares `cooldown`/`recompute`; `tests/test_perfsetup.lua:134-145` asserts only idle non-accrual | `performance-§3` |
| ConsumableMaster | CM-A-13 | A | Low | `ConsumableMaster.toc:108` `modules\PerfSetup.lua`; `performance-§1` names `core/PerfSetup.lua` | `performance-§1` |
| KickCD | KCD-R-05 | R | Low | `modules/IconGrid_Render.lua:827` opens `cdText`, return `:831-837` skips the note at `:843`; `modules/Castbar.lua:690`/`:694-697`/`:716` | `performance-§3` |
| KickCD | KCD-A-18 | A | Low | same two brackets, verified line by line (audit cites `IconGrid_Render.lua:826`, the function header) | `performance-§3` |
| LibKa0s | LK-R-04 | R | Low | `LibKa0s/Perf.lua:378-379` claims "one boolean test and nothing else"; `:400-403` and `:407-410` are two real calls on the off path | |
| LibKa0s | LK-R-05 | R | Info | `LibKa0s/Perf.lua:367-376` raises "table index is nil" for a nil key; `:408` returns early with capture off | |
| LibKa0s | LK-R-06 | R | Low | `LibKa0s/Perf.lua:822-840` `P.Cancel` never clears `P.context` set at `:756`; read at `:574` and emitted at `:919` | |

---

## C10 · Options page lifecycle and registration — 8 findings, 5 repos

`options-ui-§5` MUSTs lazy creation and the library page registry; three addons kept a private path
alongside the adopted one.

| Repo | ID | Src | Sev | Evidence | Rule |
|---|---|---|---|---|---|
| LootHistory | LH-A-27 | A | Medium | `settings/Panel.lua:329` sets `ctx.dirty`, `:146` clears it; library gate is `ctx._dirty` at `libs/LibKa0s/Options.lua:472`, set only at `:481`; `RefreshAllPanels` has no caller | `options-ui-§11` |
| AbsorbTracker | AT-A-02 | A | Low | `settings/Profiles.lua:51-56` creates the SimpleGroup inside `build`; `:60-62` OnShow only opens; `:68-69` registered at file load | `options-ui-§5` |
| ConsumableMaster | CM-A-14 | A | Low | `settings/Panel.lua:186-252` holds the Options seam inline; no `settings/OptionsSetup.lua` | `options-ui-§1` |
| ConsumableMaster | CM-A-18 | A | Medium | `settings/Panel.lua:19`, `settings/StatPriority.lua:23`, `settings/Category.lua:29` call `LibStub("AceGUI-3.0")` with no `true` | `library-stack-§4` |
| KickCD | KCD-R-03 | R | Medium | `settings/Panel.lua:546`, `:557-604` (`Settings.RegisterCanvasLayoutCategory` at `:589`), `:607-616`; library forwarders dead at `settings/OptionsSetup.lua:228-234` | `options-ui-§5` |
| KickCD | KCD-R-04 | R | Low | `settings/Panel_Render.lua:259-266` re-runs what `libs/LibKa0s/Options.lua:403`'s `afterRestoreAll` already did (`settings/OptionsSetup.lua:93-97`) | `options-ui-§11` |
| KickCD | KCD-A-09 | A | Medium | same private registry; six page tails at General:183, Icons:417, Castbar:560, Label:193, Spells:1158, Profiles:66; second open path `core/KickCD.lua:775-790` | `options-ui-§5` |
| WhatGroup | WG-A-12 | A | Low | `settings/Panel.lua:268-272` returns under `InCombatLockdown()` before `CreateOptionsPanel()` at `:276`; `options-ui.md:170` says registration never taints | `options-ui-§9` |

---

## C11 · Chat output bypasses the secret-safe printer — 6 findings, 5 repos [COLLECTION]

`events-frames-taint-§8` bans pre-`..`/`tostring`/`table.concat` at roughly 50 sites collection-wide and
says a site is non-compliant "even if never handed a secret today". `.luacheckrc` cannot see it.

| Repo | ID | Src | Sev | Evidence | Rule |
|---|---|---|---|---|---|
| BankLedger | BL-A-09 | A | Medium | `modules/Browser.lua:917` and `:926` call the global `print()`; `:1-5` declares no `local print = NS.Print`; peers do at `settings/Panel.lua:4`, `settings/Schema.lua:5`, `settings/Slash.lua:4` | `events-frames-taint-§8` |
| AbsorbTracker | AT-A-03 | A | Low | 18 sites: `settings/Slash.lua:33,97,242,246,282,321,334,339,344,352,357,365,389,414,427,428,439` and `settings/Schema.lua:214` | `events-frames-taint-§8` |
| KickCD | KCD-A-04 | A | Low | `core/Compat.lua:373-381` second secret-safe stringifier (`_G.issecretvalue` at `:374`), used at `:387-390`; sanctioned copy at `core/CoreSetup.lua:83-92` | `events-frames-taint-§8` |
| KickCD | KCD-A-15 | A | Low | `modules/Castbar_Debug.lua:125` binds `NS.Util.print or _G.print`; pre-concatenation at `:35, :82, :85-86, :102` | `events-frames-taint-§8` |
| PanelMaster | PM-A-08 | A | Low | ~25 sites: `settings/Slash.lua:15, :49-50, :58, :71, :114, :160, :177, :186, :196`; `settings/PanelEditor.lua:91, :104, :118, :125, :126, :774`; `settings/Schema.lua:144, :171` | `events-frames-taint-§8` |
| WhatGroup | WG-A-08 | A | Low | `settings/Panel.lua:22-25` and `settings/Schema.lua:48-51` both end `pout(...)` in `print(...)`; unreachable because `core/WhatGroup.lua:83` sets `_print` first | `events-frames-taint-§8` |

---

## C12 · Runner load and suite lists ungated — 6 findings, 5 repos [COLLECTION]

`testing-§9` MUSTs TOC derivation. `loadSuites` in the shared kit skips a missing file **by design**
(`testkit/framework.lua:99` comment), which is the enabling mechanism for both silent failure modes.

| Repo | ID | Src | Sev | Evidence | Rule |
|---|---|---|---|---|---|
| AbsorbTracker | AT-R-05 | R | Low | `tests/run.lua:58-81` — 21 hand-written entries; `ls tests/test_*.lua \| wc -l` = 21; `tests/_kit/framework.lua:101-108` | `testing` |
| ConsumableMaster | CM-A-03 | A | Medium | `tests/loader.lua:79-113` — hand-copied 33-entry `PURE_LAYER`; consumed at `:178, :184, :196, :237`; only `:208` uses `L.tocFiles()` | `testing-§9` |
| LootHistory | LH-A-29 | A | Medium | `tests/run.lua:30` derives via `Loader.tocFiles`; `:39` publishes no loaded list; no case asserts the fed list, path existence, or that no `libs/` path leaked | `testing-§9` |
| PanelMaster | PM-A-10 | A | Low | `tests/run.lua:24-31` lists 6 files; `libs/LibKa0s/LibKa0s.xml` lists 8 (Perf.lua, PerfPanel.lua absent) | `testing-§9` |
| LibKa0s | LK-R-01 | R | Medium | `tests/run.lua:17-19` (library files) and `:76-80` (suites), both hand-written; `LibKa0s/LibKa0s.xml:2-9` never parsed; `testkit/framework.lua:101-110` | `testing-§9` |
| LibKa0s | LK-A-09 | A | Medium | same lines; partial mitigation at `tests/test_versioning.lua:43-57` catches only a file already in MAJORS | `testing-§9` |

---

## C13 · Addon-scoped documentation rules applied to the library repo — 6 findings, LibKa0s only

Every rule in `documentation` opens "Every Ka0s addon". LibKa0s is a library repo and does not appear in
`standards/ADDONS.md:19-26`. This is an audit **scope error**, not repo drift.

| Repo | ID | Src | Sev | Evidence | Rule |
|---|---|---|---|---|---|
| LibKa0s | LK-A-01 | A | Low | root listing has no `CLAUDE.md`; rule at `documentation.md:67-78` | `documentation-§2` |
| LibKa0s | LK-A-02 | A | Low | grep for "WowAddonStandards" in `README.md` returns nothing; two hits only in `CHANGELOG.md:418`, `:475` | `documentation-§6` |
| LibKa0s | LK-A-03 | A | Low | root listing has no `DEPENDENCIES.md`; toolchain readable only from `docs/automated-tests/20260805-002859/manifest.json` | `documentation-§7` |
| LibKa0s | LK-A-04 | A | Low | `ls docs/` has no `testing.md`; content is at `README.md:121-159` | `documentation-§3` |
| LibKa0s | LK-A-05 | A | Low | `ls docs/` has no `ARCHITECTURE.md`; `README.md:196-231` is a file tree only | `documentation-§3` |
| LibKa0s | LK-A-12 | A | Info | `ls docs/` — no `smoke-tests.md`, no `performance.md`; reason recorded at `docs/automated-tests/README.md:47-51` | `documentation-§3` |

---

## C14 · Shared kit vendored but not consumed — 5 findings, 3 repos

The kit has no isolated-environment mode, which is why prettychat forked; ConsumableMaster and KickCD
forked before adoption. The byte-identity gate protects a payload nothing loads.

| Repo | ID | Src | Sev | Evidence | Rule |
|---|---|---|---|---|---|
| ConsumableMaster | CM-R-06 | R | Medium | `tests/run.lua:21` `require("harness")`; grep for `_kit` across `tests/*.lua` returns comments plus `tests/test_vendor_sync.lua:145,150` | `testing-§1` |
| ConsumableMaster | CM-A-02 | A | Medium | same evidence, independently confirmed | `testing-§1` |
| KickCD | KCD-R-08 | R | Medium | `tests/run.lua:15-88` private loader + registry + assertion set; `:40-53` runs each case body at registration; comments only at `tests/run.lua:75`, `tests/wow_mock.lua:573` | `testing-§1` |
| KickCD | KCD-A-01 | A | Medium | `tests/loader.lua` 108 LOC private loader; `tests/wow_mock.lua` 1066 LOC | `testing-§1` |
| prettychat | PC-A-16 | A | Info | `tests/loader.lua` alongside `tests/_kit/loader.lua`; justified at `CLAUDE.md:12`, tracked as LIBKA0S-01 in `docs/pending/LEDGER.md` | `testing-§1` |

---

## C15 · Retired `§N.M` notation — 5 filed, 9 repos affected [COLLECTION]

v2.21.0 retired the global numbering with no sweep. Measured across the collection: AbsorbTracker 83,
LibKa0s 183, KickCD 39, ConsumableMaster 38, WhatGroup 13, LootHistory 7, BankLedger 3, PanelMaster 1,
prettychat 1 — **368 live sites**. KickCD, PanelMaster, prettychat and LibKa0s carry it unflagged.

**What the 368 excludes, stated because an earlier draft's sweep scope did not match it.** `libs/`,
`tests/_kit/`, `docs/audits/`, `docs/reviews/` **and `docs/automated-tests/`** — all three `docs/` paths
are frozen evidence. The last one matters: KickCD's figure is 39 with all five excluded and **69** with
only the first four, because 30 `§N.M` lines live inside its frozen automated-test bundles
(`20260804-182144/`, `-214315/`, `-233245/`). Those 30 are evidence and stay. Of LibKa0s's 183, **two are
in shipped source** (`LibKa0s/LibKa0s/Options.lua:129`, `:173`), which is vendored byte-for-byte into all
eight addons — they are swept in `M1-LK-10`, never in `M3-07`.

| Repo | ID | Src | Sev | Evidence | Rule |
|---|---|---|---|---|---|
| AbsorbTracker | AT-A-11 | A | Low | `settings/Slash.lua:199` reads `slash-commands-§:` (malformed); `core/Constants.lua:11`, `:15`; `core/AbsorbTracker.lua:9, :38, :63, :163`; `defaults/Profile.lua:5, :8` | `documentation-§5` |
| BankLedger | BL-A-11 | A | Low | `settings/OptionsSetup.lua:43`, `settings/Schema.lua:184`, `docs/ARCHITECTURE.md:106` (`options-ui-§41`); `settings/Panel.lua:58` (`§190`); `tests/test_panel.lua:175` (`§189`) — `options-ui` has §1–§11 | `documentation-§5` |
| ConsumableMaster | CM-A-20 | A | Info | 34 lines, e.g. `core/Bus.lua:1`, `core/Constants.lua:15`, `core/Database.lua:6`, `core/Debug.lua:4`, `core/LSMPatch.lua:26` | |
| LootHistory | LH-A-19 | A | Low | `settings/OptionsSetup.lua:101`, `tests/test_database.lua:390` | `documentation-§5` |
| WhatGroup | WG-A-15 | A | Info | `.luacheckrc:1` (`§14`), `.pkgmeta:4` (`§3.3, §13`) | |

---

## C16 · Tests that cannot go red — 5 findings, 4 repos

Assertions pin a relation, or pin "it raised", rather than a value.

| Repo | ID | Src | Sev | Evidence | Rule |
|---|---|---|---|---|---|
| AbsorbTracker | AT-R-06 | R | Low | `tests/perf.lua:228-229` asserts `probeOff.bytesPerIter <= probeOn.bytesPerIter + 1` — a relation, not a ceiling | `performance-§2` |
| ConsumableMaster | CM-R-04 | R | Medium | `tests/test_settingsui.lua:243-246` — comment claims "readable and writable"; assertions are `#KCM.Settings.Schema > 0` and `FindSchema("enabled")` | `testing-§12` |
| prettychat | PC-R-03 | R | Medium | `tests/test_defaults.lua:107-114` validates each format string against arguments `modules/Override.lua:171-197` derived from that same string | `testing-§12` |
| LibKa0s | LK-R-03 | R | Low | `tests/test_perf_core.lua:15-24` four bare `assertFalse`; `LibKa0s/Perf.lua:328` raises independently of the `:290` guard | |
| LibKa0s | LK-A-10 | A | Low | same lines; `testkit/framework.lua:67-71` already returns the message; `tests/test_perf_core.lua:26-41` does it correctly | `testing-§12` |

---

## C17 · Message-bus discipline — 5 findings, 5 repos

`architecture-§4` bans two senders for one message. No gate counts senders. **`PC-A-12` is a rule-scope
problem**, not repo drift.

| Repo | ID | Src | Sev | Evidence | Rule |
|---|---|---|---|---|---|
| prettychat | PC-A-12 | A | Low | `docs/ARCHITECTURE.md:119` "There is no message bus."; `modules/Override.lua:108-109, 120-121, 138-139` call `NS.Schema.NotifyPanelChange` directly | `architecture-§4` |
| KickCD | KCD-A-08 | A | Medium | six senders of `Ka0s_KickCD_CONFIG_CHANGED`: `core/KickCD.lua:128`, `:457`, `modules/IconGrid.lua:553`, `modules/Castbar.lua:333`, `settings/Spells.lua:345`, `settings/Panel.lua:77`; `docs/ARCHITECTURE.md:118` records five. `Ka0s_KickCD_PROFILE_CHANGED` also has two (`:120`) and went unflagged | `architecture-§4` |
| LootHistory | LH-R-03 | R | Low | `modules/Browser.lua:1366`, `modules/Collector.lua:217`, `modules/Analytics.lua:657` all `NS.NewBusTarget() or bus`; unreachable — `core/LootHistory.lua:4` errors via `libs/AceAddon-3.0/AceAddon-3.0.lua:182-186` | `architecture-§4` |
| LootHistory | LH-A-35 | A | Low | same three sites, correctly enumerated | `architecture-§4` |
| PanelMaster | PM-R-11 | R | Low | `modules/Canvas.lua:743` registers the raw string while `:741`/`:742` use constants; `settings/Schema.lua:21` publishes `S.MSG_SETTINGS` | `architecture-§4` |

---

## C18 · Vendored runner committed at git mode 100644 — 4 filed, 9 repos affected [COLLECTION]

Re-vendoring drops the executable bit. **Verified `100644` in all nine**, including LibKa0s's own
`testkit/run-automated-tests.sh` and `tests/_kit/run-automated-tests.sh` — so the source every consumer
copies from is wrong too. WSL DrvFs masks it locally by reporting `rwxrwxrwx` for every file.

| Repo | ID | Src | Sev | Evidence | Rule |
|---|---|---|---|---|---|
| AbsorbTracker | AT-A-05 | A | Low | `git ls-files -s tests/_kit/` → `100644`; `docs/testing.md:37-39` invokes it bare | `automated-tests-§2` |
| BankLedger | BL-A-13 | A | Low | `git ls-files -s tests/_kit/run-automated-tests.sh` → `100644 30da7c07…`; CRLF half handled at `.gitattributes:34` | `automated-tests-§2` |
| ConsumableMaster | CM-A-29 | A | Low | `git ls-files -s tests/_kit/run-automated-tests.sh` → `100644 30da7c07…` | `automated-tests-§2` |
| PanelMaster | PM-A-11 | A | Low | mode `100644`; `docs/testing.md:110-112` and `docs/automated-tests/README.md:8-10` document invoking it directly | `automated-tests-§2` |

---

## C19 · Defaults declared outside `defaults/Profile.lua` — 4 findings, 4 repos

| Repo | ID | Src | Sev | Evidence | Rule |
|---|---|---|---|---|---|
| BankLedger | BL-A-01 | A | Info | `defaults/` contains `Global.lua` only; accepted deviation at `docs/ARCHITECTURE.md:568-581` | `savedvariables-§2` |
| ConsumableMaster | CM-A-15 | A | Low | `core/ConsumableMaster.lua:25` `KCM.dbDefaults = {`; `ls defaults/` shows Categories.lua and fifteen `Defaults_*.lua`, no `Profile.lua` | `savedvariables-§2` |
| KickCD | KCD-A-10 | A | Low | `ls defaults/` shows `Spells.lua` only; `DEFAULT_PROFILE` at `core/Database.lua:239-303`; second copy at `modules/Castbar.lua:569-588` | `savedvariables-§2` |
| LootHistory | LH-A-28 | A | Low | `defaults/Global.lua:21-27` vs `settings/Schema.lua:25, :52, :61, :70, :77, :85`; `:109` already does it right | `savedvariables-§2` |

---

## C20 · Localization seam exported, unused — 4 findings, 4 repos

All MUSTs met (seam present, `enUS.lua` ships); only the SHOULD is open. **Four repos independently
reached "English-only, deliberate"**, which is evidence about the SHOULD, not about the repos.

| Repo | ID | Src | Sev | Evidence | Rule |
|---|---|---|---|---|---|
| AbsorbTracker | AT-A-09 | A | Low | `locales/enUS.lua` is 12 lines, one `L["` occurrence, no populated keys; grep for `NS.L[` returns zero. Deferred as PLAN-02 in `docs/pending/LEDGER.md` | `localization-§1` |
| prettychat | PC-R-06 | R | Low | `settings/Schema.lua:72-73`; `settings/Panel.lua:168`, `:393` — four concatenated user-facing strings | `localization-§1` |
| PanelMaster | PM-A-17 | A | Info | `locales/enUS.lua:6` sets the metatable fallback; `:8-14` documents the 0.1.0 English-only decision | `localization-§1` |
| WhatGroup | WG-R-06 | R | Low | `locales/enUS.lua:67-70` and `:104` — five dead keys; strings passed as literals at `settings/OptionsSetup.lua:99`, `settings/Panel.lua:176`, `:220` | `localization-§3` |

---

## C21 · Options library constants and members copied to the host — 4 findings, 2 repos

`KCD-A-03` is **unfixable downstream** — `libs/LibKa0s/Options.lua` never publishes `PADDING_X` on the
instance.

| Repo | ID | Src | Sev | Evidence | Rule |
|---|---|---|---|---|---|
| ConsumableMaster | CM-A-04 | A | Low | `settings/Panel.lua:41-42` `local Helpers = KCM.Settings.Helpers or {}`; instance is a separate `UI` at `:187-243`, copied at `:244-252`, `:571-572` | `options-ui-§1` |
| ConsumableMaster | CM-A-05 | A | Low | `settings/Panel.lua:74` `SECTION_HEADING_H = 26`, `:75` `BUTTON_PAIR_REL = 0.492`; used at `:502-503` and `:734` | `options-ui-§8` |
| KickCD | KCD-A-02 | A | Low | `settings/Panel.lua:281, :341, :394, :443` shadow `libs/LibKa0s/Options.lua:322, :502` and `OptionsWidgets.lua:333, :362` | `options-ui-§1` |
| KickCD | KCD-A-03 | A | Low | `core/Constants.lua:66` `PANEL_PADDING_X = 16` vs `libs/LibKa0s/Options.lua:46`; `settings/Panel.lua:426` `ROW_VSPACER = 8` overwrites the published `O.ROW_VSPACER` at `:430` | `options-ui-§8` |

---

## C22 · Lint config drift — 4 findings, 3 repos

Lint is 0/0 in every repo either way.

| Repo | ID | Src | Sev | Evidence | Rule |
|---|---|---|---|---|---|
| AbsorbTracker | AT-A-16 | A | Info | `.luacheckrc:6` excludes all of `docs/`; `lint.md:11` names `docs/audits/`, `docs/reviews/` | `lint` |
| ConsumableMaster | CM-R-08 | R | Low | `.luacheckrc:23` `ignore = { "212", "542", "241" }` — 241 silenced tree-wide across 54 files, documented at `:22` | `lint` |
| LootHistory | LH-R-08 | R | Info | `modules/AuctionPrice.lua:1` `-- luacheck: ignore addonName`; `.luacheckrc:8` already carries `211/addonName` | `lint` |
| LootHistory | LH-A-44 | A | Info | same line; audit's `.luacheckrc` citation is wrong (`:14` for `:8`) | `lint` |

---

## C23 · Bundle and record shape — 4 findings, 4 repos

| Repo | ID | Src | Sev | Evidence | Rule |
|---|---|---|---|---|---|
| AbsorbTracker | AT-A-06 | A | Low | `docs/automated-tests/RESULTS.md:64-91` is prose; `:95-97` is a real table. Runner's row prepend at `tests/_kit/run-automated-tests.sh:331-352` does not touch it | `automated-tests-§4` |
| LootHistory | LH-A-37 | A | Low | `docs/automated-tests/RESULTS.md:49` dispositions `modules/Browser.lua` as "Already tracked as LH-31"; `docs/audits/2026-08-04/02_DEVIATIONS.md:74` defines LH-31 as the retired `docs/complexity.md` | `automated-tests-§4` |
| LootHistory | LH-A-41 | A | Low | `docs/perf-runs/README.md` documents `<YYYYMMDD-HHMMSS>/` folders; `performance-§8` MUSTs flat `<YYYY-MM-DD>-ingame-<label>.json`, a schema summary and a library pointer | `performance-§8` |
| LibKa0s | LK-A-07 | A | Low | `docs/automated-tests/20260805-002859/manifest.json` — `"label": null, "release": null, "dirty": true`; `docs/releasing.md:28-59` has no runner step | `automated-tests-§6` |

---

## C24 · SavedVariables writes outside the write seam — 4 findings, 4 repos

| Repo | ID | Src | Sev | Evidence | Rule |
|---|---|---|---|---|---|
| BankLedger | BL-R-09 | R | Low | `settings/Schema.lua:124-125` names two of four carve-outs; also `modules/SessionWindow.lua:256`, `:287`, `modules/Browser.lua:916` cleared at `:923` | |
| KickCD | KCD-R-06 | R | Low | `settings/Slash.lua:121` `parent[key] = candidate`, `:122` `allowedKeys(row)`, `:123` restore — no pcall | `options-ui-§1` |
| KickCD | KCD-A-17 | A | Low | same lines (audit cites `:120`/`:122`); documented as deliberate at `:98-102` | `options-ui-§1` |
| WhatGroup | WG-R-03 | R | Low | `settings/Schema.lua:206`, `:216` materialize missing parent tables; `Helpers.Get` at `:222`; reproduced | |

---

## C25 · `docs/ARCHITECTURE.md` missing mandated sections — 3 findings, 3 repos

`documentation-§3` names eight headings: Overview, Module Map, Settings Schema, Message Bus, Slash
Commands, Event Subscriptions, Taint Notes, Known Limitations.

| Repo | ID | Src | Sev | Evidence | Rule |
|---|---|---|---|---|---|
| ConsumableMaster | CM-A-27 | A | Low | `grep '^## ' docs/ARCHITECTURE.md` — no Settings Schema, Slash Commands, Event Subscriptions, Taint Notes, Known Limitations | `documentation-§3` |
| prettychat | PC-A-17 | A | Low | `grep -n '^## ' docs/ARCHITECTURE.md` — no `## Message Bus`; content is the last sentence of `:119` | `documentation-§3` |
| WhatGroup | WG-A-11 | A | Low | headings at `:5, :11, :57, :85, :91, :108` — no Settings Schema, Message Bus, Slash Commands, Known Limitations | `documentation-§3` |

---

## C26 · Preview mode absent or incomplete — 3 findings, 2 repos

| Repo | ID | Src | Sev | Evidence | Rule |
|---|---|---|---|---|---|
| AbsorbTracker | AT-R-02 | R | Low | `settings/Slash.lua:282` prints "…for %d s", `:291` sets `NS.testHoldUntil`; `modules/Display.lua:185-188`; only two `ScheduleTimer` sites exist and neither is armed by `runTest` | `preview-mode` |
| AbsorbTracker | AT-A-13 | A | Low | `modules/Display.lua:92-98` (no placeholder fill while unlocked); `:185-188` plus `settings/Slash.lua:291` (no off verb, no lock-triggered clear) | `preview-mode` |
| ConsumableMaster | CM-A-34 | A | Low | grep for `preview\|placeholder` across `modules/MacroBar.lua`, `settings/MacroBar.lua`, `core/MacroBarModel.lua` returns nothing; `preview-mode.md:5` is SHOULD for positionable displays | `preview-mode` |

---

## C27 · British spellings in authored text — 3 findings, 3 repos

LibKa0s is the source. Local patches in a consumer revert on the next whole-folder re-vendor
(anti-pattern #48).

| Repo | ID | Src | Sev | Evidence | Rule |
|---|---|---|---|---|---|
| KickCD | KCD-A-16 | A | Low | `docs/superpowers/plans/2026-08-04-ccn-elimination.md:51, :53, :57, :117, :121, :123, :147, :149, :213` (audit lists only five) | `localization-§5` |
| WhatGroup | WG-R-09 | R | Low | 29 hits under `libs/LibKa0s/`; e.g. `libs/LibKa0s/Core.lua:76, :77, :78, :79, :100` | `localization-§5` |
| LibKa0s | LK-A-06 | A | Low | 33 hits in `LibKa0s/*.lua`; `Core.lua:76-79, :100, :156, :257`; `DebugLog.lua:180, :216, :230, :304`; `Options.lua:525`; `OptionsWidgets.lua:32, :56` | `localization-§5` |

---

## C28 · Boot validation unreachable — 3 findings, 2 repos

Identical `and row.default == nil` conjunct; every shipped row carries a default. A copied idiom.

| Repo | ID | Src | Sev | Evidence | Rule |
|---|---|---|---|---|---|
| LootHistory | LH-R-02 | R | Low | `settings/Schema.lua:194`; all 11 rows declare a non-nil default (two are `false`), so the print at `:195` is unreachable | `architecture-§5` |
| LootHistory | LH-A-43 | A | Low | `settings/Schema.lua:188-198`, condition at `:194` | `architecture-§5` |
| PanelMaster | PM-R-02 | R | Low | `settings/Schema.lua:171`; all 9 rows at `:27-98` declare a default; `tests/test_schema.lua:8-11` asserts `S:Register() == 0` | `architecture-§5` |

---

## C29 · On-notice LOC band filed as a deviation — 3 findings, 3 repos

`layout-§1` caps at 1500 and puts 1000–1500 "on notice". A file inside the band is **the compliant
state**. Filing it in a deviations table is an observation, not a deviation.

| Repo | ID | Src | Sev | Evidence | Rule |
|---|---|---|---|---|---|
| BankLedger | BL-A-16 | A | Info | `modules/Browser.lua` 1368, `tests/test_ledger.lua` 1361, `modules/LedgerTable.lua` 1052, `modules/Insights.lua` 1023 | `layout-§1` |
| ConsumableMaster | CM-A-21 | A | Info | `wc -l tests/test_macrobar.lua` → 1497; `settings/Panel.lua` 950, `core/SlashCommands.lua` 836 | `layout-§1` |
| prettychat | PC-A-11 | A | Info | `wc -l GlobalStrings/GlobalStrings.lua` → 23842; excluded at `.pkgmeta:21`, referenced by no TOC line | `layout-§1` |

---

## C30 · Window skin restated rather than delegated — 2 findings, 2 repos

Values agree with the normative edge exactly in both repos, so nothing renders wrong. `standalone-windows`
carries no numbered subsections — both bundles cited `standalone-windows-§2`, which cannot resolve.

| Repo | ID | Src | Sev | Evidence | Rule |
|---|---|---|---|---|---|
| BankLedger | BL-A-10 | A | Low | `modules/Browser.lua:21-34` private SKIN table; `:67-89` builds the backdrop by hand; rule at `standalone-windows.md:27` | `standalone-windows` |
| LootHistory | LH-A-30 | A | Low | `modules/Browser.lua:20-33` and `:65-86`; every value matches the normative table | `standalone-windows` |

---

## C31 · Packaging ignore-list gaps — 2 findings, 2 repos

| Repo | ID | Src | Sev | Evidence | Rule |
|---|---|---|---|---|---|
| ConsumableMaster | CM-A-23 | A | Info | `.pkgmeta` ignore omits `.claude/`, `.superpowers/`, `CHANGELOG.md`; all three exist at root | `packaging` |
| WhatGroup | WG-A-07 | A | Low | `.pkgmeta:6-11` omits `_dev` and lockfiles; canonical block at `packaging.md:19`, MUST at `:24` | `packaging` |

---

## C32 · Compat routing and API currency — 2 findings, ConsumableMaster

`GetItemInfo` / `GetItemCount` are **live retail globals**, not deprecated ones, so `compat`'s MUST does
not squarely apply. What is verifiably wrong is a false comment.

| Repo | ID | Src | Sev | Evidence | Rule |
|---|---|---|---|---|---|
| ConsumableMaster | CM-R-10 | R | Low | `core/TooltipCache.lua:459` bare `GetItemInfo`; guarded neighbors at `core/Classifier.lua:167-170`, `core/WeaponSlots.lua:33-36` | `compat` |
| ConsumableMaster | CM-A-30 | A | Low | `core/TooltipCache.lua:459` and `modules/Ranker.lua:88` bare; `core/Compat.lua` wraps only `:17, :26, :36, :45, :60, :68`. The false claim is at `.luacheckrc:66` (audit cites `:74`) | `compat` |

---

## C33 · Runner emits impossible durations — 1 filed, 5 repos affected [COLLECTION]

`$(date +%s)` integer seconds × 1000, never clamped. Confirmed `-2000` in AbsorbTracker and BankLedger
manifests, `-1000` in KickCD, LootHistory and prettychat.

| Repo | ID | Src | Sev | Evidence | Rule |
|---|---|---|---|---|---|
| prettychat | PC-R-07 | R | Low | `tests/_kit/run-automated-tests.sh` brackets with `t0=$(date +%s)` and emits `$(( DUR * 1000 ))`; `docs/automated-tests/20260804-233338/manifest.json:16` records `"durationMs": -1000` | `automated-tests-§5` |

---

# Part 2 — True one-offs (30)

A one-off is a finding with no counterpart in any other repo. **LibKa0s has zero** — every LibKa0s
finding is either a shared-code root cause or an audit scope error.

## AbsorbTracker — 5

| Repo | ID | Src | Sev | Evidence | Rule |
|---|---|---|---|---|---|
| AbsorbTracker | AT-R-03 | R | Low | `settings/General.lua:50-53` REPAINT guarded, VISIBILITY unconditional; `modules/Display.lua:130-131` defaults unit to `"player"`, `:133` returns false when the player bar is disabled | |
| AbsorbTracker | AT-R-04 | R | Low | `settings/General.lua:133-138` prints outside the guard; `settings/Slash.lua:169-175` prints inside, with an `else` and a comment saying why | |
| AbsorbTracker | AT-R-07 | R | Low | `docs/performance.md:242` "**`delta` is the headline.**", `:247`, caveat at `:258`; `performance-§7` says the opposite | `performance-§7` |
| AbsorbTracker | AT-R-08 | R | Low | `defaults/Profile.lua:78` `schemaVersion = 4` under `global` vs `:56` `= 1` per profile with rationale at `:50-55`; `core/Database.lua:189-190`, `:187-211` | `savedvariables-§1` |
| AbsorbTracker | AT-A-10 | A | Info | `docs/ARCHITECTURE.md:316-331` written justification; `events-frames-taint.md` §1's own parenthetical anticipates this case | `events-frames-taint-§1` |

## BankLedger — 4

| Repo | ID | Src | Sev | Evidence | Rule |
|---|---|---|---|---|---|
| BankLedger | BL-R-01 | R | Medium | `settings/Panel.lua:405` reads `LibStub.minors["O.AceGUI-3.0"]`, consumed at `:406`; the registered major is `AceGUI-3.0`; test asserts by shape only at `tests/test_panel.lua:460` | |
| BankLedger | BL-R-04 | R | Low | `modules/SessionWindow.lua:158-169` builds the presence set before consulting `self:Entries()`; `core/Database.lua:620-636` fires `LedgerChanged` at `:631` unconditionally | |
| BankLedger | BL-R-06 | R | Info | `modules/Ledger.lua:713` and `:743` use `C.Store.GUILD_BANK` for frame context; `core/Constants.lua:35-36` sanctions the shared value | |
| BankLedger | BL-R-08 | R | Low | `settings/Panel.lua:547-548` tooltip; `P:RestoreDefaults` calls both `ResetWindow()`s, the latter wiping `settings.sessionWindow` at `modules/SessionWindow.lua:287` | |

## ConsumableMaster — 2

| Repo | ID | Src | Sev | Evidence | Rule |
|---|---|---|---|---|---|
| ConsumableMaster | CM-R-05 | R | Low | `modules/MacroBar.lua:392`, `:404` written directly from `core/SlashCommands.lua:781-787` and `:811`; `macroBar.locked` (`settings/MacroBar.lua:71`) has no onChange | `options-ui-§1` |
| ConsumableMaster | CM-A-12 | A | Low | `ConsumableMaster.toc:103` lists `modules\DebugLog.lua` inside the `# Modules` block; `debug-logging-§1` requires `core/DebugLogSetup.lua` | `debug-logging-§1` |

## KickCD — 2

| Repo | ID | Src | Sev | Evidence | Rule |
|---|---|---|---|---|---|
| KickCD | KCD-R-01 | R | Medium | `modules/Castbar.lua:726-729` `rgba` reads positionally, consumed at `:740`, `:747-748`; stored keyed at `core/Database.lua:203`, `:213`; shape-agnostic reader exists at `core/Util.lua:22-28` | `options-ui-§1` |
| KickCD | KCD-A-11 | A | Medium | same lines; migration to keyed at `core/Database.lua:677-704`; grep of `tests/` finds no `nameTextColor` or `rgba` | `options-ui-§1` |

## LootHistory — 5

| Repo | ID | Src | Sev | Evidence | Rule |
|---|---|---|---|---|---|
| LootHistory | LH-R-01 | R | Medium | `defaults/Global.lua:36-39` (7 tags) vs `core/Constants.lua:146-153` (11); `modules/AuctionPrice.lua:87-98`; `settings/Panel.lua:431` sole `ReconcilePriority` caller; `tests/test_schema.lua:140-148` guards `row.type ~= "table"` | `savedvariables-§2` |
| LootHistory | LH-A-34 | A | Medium | same evidence, more precisely cited | `savedvariables-§2` |
| LootHistory | LH-R-04 | R | Low | `settings/Panel.lua:635` → StaticPopup; `settings/Slash.lua:19-26`, `:84-92` (Purge + CliResetAll); `settings/Schema.lua:223` `resetall` → settings only | `slash-commands-§2` |
| LootHistory | LH-A-42 | A | Low | same sites; the dialog text at `settings/Slash.lua:20` discloses both effects first | `slash-commands-§2` |
| LootHistory | LH-R-09 | R | Info | `modules/Analytics.lua:175-197` — `_charStackSegments` called at `:180` and again at `:185`; sorts twice at `:152-167` | |

## PanelMaster — 3

| Repo | ID | Src | Sev | Evidence | Rule |
|---|---|---|---|---|---|
| PanelMaster | PM-R-04 | R | Low | `core/Database.lua:71` calls `RunMigrations` from the profile callback; gate at `:88`, stamp at `:113`, already run at `:17-19`. **Larger half:** `defaults/Global.lua:13` seeds `schemaVersion = NS.SCHEMA_VERSION` as the AceDB default, making `:99-111` unreachable for any account | `savedvariables-§1` |
| PanelMaster | PM-R-06 | R | Low | `modules/Canvas.lua:551` reaches `NS.Unlock` unguarded — but so do `:125, 274, 332, 356, 384, 546, 555, 677, 713, 723, 741, 742` | |
| PanelMaster | PM-R-12 | R | Low | `settings/Panel.lua:12`, `settings/PanelEditor.lua:7`, `core/LSMPatch.lua:35` resolve AceGUI; `settings/OptionsSetup.lua:98` stashes `NS.AceGUI`, which has no reader | `library-stack-§4` |

## prettychat — 5

| Repo | ID | Src | Sev | Evidence | Rule |
|---|---|---|---|---|---|
| prettychat | PC-R-01 | R | **High** | `defaults/Defaults.lua:162-165` default carries `%d`; `GlobalStrings/GlobalStrings_011.lua:203` is `"Reputation with %s decreased."`; written into `_G` at `modules/Override.lua:84`; `enabled = true` at `defaults/Defaults.lua:144` | |
| prettychat | PC-R-02 | R | **High** | `defaults/Defaults.lua:190-193` first and only conversion is `%d`; `GlobalStrings/GlobalStrings_011.lua:214` is `"%s has gained %d guardian experience points."`; contrast `:186-189` | |
| prettychat | PC-R-04 | R | Low | `settings/Panel.lua:180-182` reads the shipped dump; `modules/Override.lua:246` reads the live snapshot; snapshot taken at `core/PrettyChat.lua:38-43`; pinned at `tests/test_panel.lua:309-317` | |
| prettychat | PC-R-05 | R | Medium | `PrettyChat.toc:38-63` lists 26 chunks; `du -ch` = 2.0M; 22,879 entries for 79 unique lookups; only consumer is `settings/Panel.lua:180` | `performance-§9` |
| prettychat | PC-R-08 | R | Low | `settings/Panel.lua:368` calls `NS.SlashCommands.LandingRows()` through a dot; `libs/LibKa0s/Slash.lua:460` declares `function Sl:LandingRows()` | |

## WhatGroup — 4

| Repo | ID | Src | Sev | Evidence | Rule |
|---|---|---|---|---|---|
| WhatGroup | WG-A-13 | A | Info | `core/WhatGroup.lua:96` hands the vendored TTF path to the descriptor built at `core/DebugLogSetup.lua:95` with **no Blizzard fetch-failure fallback**. Moved out of C4: nothing ratifies it — no register row, no `docs/pending/LEDGER.md` entry, no in-code rationale — so it is a genuinely unmet SHOULD, not a re-filed ratified deviation | `debug-logging-§2` |
| WhatGroup | WG-R-01 | R | **High** | `core/WhatGroup.lua:488` is the only `db.profile.enabled` read (in `OnApplyToGroup`); the `inviteaccepted` branch at `:639`, `:650`, `:671` has none; `_TryFireJoinNotify` (`:533-573`) gates only on pendingInfo/notifiedFor/IsInGroup. Reproduced headlessly; contradicts the tooltip at `settings/Schema.lua:92` | |
| WhatGroup | WG-R-04 | R | Low | `core/WhatGroup.lua:391-395` defines `Labels.GetPlaystyleLabel`; `modules/Frame.lua:292-294` open-codes it; `:283` does use the sibling helper | |
| WhatGroup | WG-R-05 | R | Low | `modules/Frame.lua:145` `RegisterForClicks('AnyUp', 'AnyDown')`; macro at `:229-230`; PreClick at `:243-249` gates on `down` because of it | |

---

# Part 3 — Rejected in triage

The skepticism was applied. These items appeared in a bundle and are **not** carried forward.

## Rejected outright — the claim did not survive re-checking

| Repo | Bundle id | Why rejected |
|---|---|---|
| AbsorbTracker | AT-46 (audit) | Rests on "≈60 committed" dev files. `git ls-files .superpowers .claude` returns zero and both paths are in `.gitignore`. |
| AbsorbTracker | AT-41 (audit) | Filed as a deviation while its own text concludes no change is required. |
| AbsorbTracker | F-012 (review) | Reads "do NOT cache the resolved color on a frame" as a claim that nothing is memoized. It is a directive about frames, and the half the comment does assert is true. |
| BankLedger | BL-23 (audit) | Concedes `documentation-§4` is satisfied and then applies it "by extension". |
| ConsumableMaster | CM-52, CM-66 (audit) | Verbatim duplicates of review F-008/F-009 and F-011. |
| ConsumableMaster | CM-55 (audit) | Flags an extra README section `documentation-§1` does not forbid; its own remedy is "keep it". |
| ConsumableMaster | CM-57 (audit) | Cites `documentation-§4`'s `TODO.md` ban against `docs/pending/LEDGER.md`, a file `wow-addon:pending-audit` is specified to write. |
| LootHistory | LH-32 (audit) | The audit itself states this is not a deviation from a rule that names a different file. |
| PanelMaster | PM-007, PM-020, PM-021, PM-022 (audit) | Audit twins of review F-001, F-005, F-012, F-003. Canonicalized on the review ids. PM-022 additionally cites a `debug-logging-§3` MUST NOT that governs the console line formatters and their `6f8faf`/`c9a66b` colors, not the chat ack's state hexes — while `debug-logging-§7` positively requires the stub to print that ack. |
| prettychat | PC-45 (audit) | The `.luacheckrc` is correct as written; both entries only become MUSTs once perf brackets and the `PerfDB` global exist, as the deviation itself concedes. |
| prettychat | PC-58, PC-59 (audit) | Verbatim duplicates of review F-003 and F-006. |
| WhatGroup | F-007 (review) | The anchor chain provably terminates at `UIParent` in both branches of `NS.Windows.Restore` (`core/Util.lua:50-58`), so `GetLeft`/`GetTop` cannot be nil there. |
| WhatGroup | F-U02 (review) | Asserts no defect at all — an unrun-check disclosure dressed up as a numbered finding. |
| WhatGroup | F-002 / WG-44 (both bundles) | **Both bundles assert the same false claim**: that the master-switch capture case at `tests/test_capture.lua:63-76` cannot fail. Deleting the gate at `core/WhatGroup.lua:488` in a scratchpad copy took the suite to 421/1 with exactly that case failing. Two agents agreeing is not two verifications. |
| LibKa0s | LK-A-14 (audit) | Cites `automated-tests-§1` for a dirty-tree rule that does not exist in that section, and is in any case the same fact as LK-A-07. |

## Rejected as duplicates within a repo — merged, not dropped

Where both bundles found the same defect independently, both ids survive so each bundle's ledger stays
complete, but they map to **one** work item and are counted once toward the underlying problem:

`CM-R-01`/`CM-A-25`, `CM-R-06`/`CM-A-02`, `CM-R-07`/`CM-A-31`, `KCD-R-01`/`KCD-A-11`,
`KCD-R-02`/`KCD-A-12`, `KCD-R-05`/`KCD-A-18`, `KCD-R-08`/`KCD-A-01`, `LH-R-01`/`LH-A-34`,
`LH-R-02`/`LH-A-43`, `LH-R-03`/`LH-A-35`, `LH-R-04`/`LH-A-42`, `LH-R-05`/`LH-A-40`,
`LH-R-06`/`LH-A-39`, `LH-R-08`/`LH-A-44`, `BL-R-02`/`BL-A-14`, `KCD-R-06`/`KCD-A-17`,
`LK-R-01`/`LK-A-09`, `LK-R-02`/`LK-A-15`, `LK-R-03`/`LK-A-10`, `AT-R-01` (bundle-internal).

## Fix directions rejected — do not execute as written

**`AT-R-01` — AbsorbTracker perf descriptor.** Both bundles direct you to drop `within` from the
`visibility` bucket. `modules/Display.lua:100` calls `ApplyVisibility` from inside the open `appearance`
bracket, so `visibility` **is** nested — in `appearance`, not in `repaintPass`. The prescribed fix
substitutes one false containment claim for another. The correct value is `within = "appearance"`, and
the durable answer is `M1-LK-08` (the library observes containment rather than trusting the descriptor).

## Claims corrected but the finding retained

| Finding | Correction |
|---|---|
| `AT-A-03` | Audit's `02_DEVIATIONS` table says 17 sites; its own execution plan step 3.6 says 18. The count is **18**. |
| `AT-A-11` | Audit reports 31 hits. The sweep missed the live `docs/` pages: 25 in code plus 25 in docs = **50** in this repo. |
| `AT-R-05` | Misdescribes the fourth pinned list — `tests/test_loadorder.lua:3-5` names `test_perf.lua`'s `loadDegraded()`, not the LibKa0s XML order. |
| `AT-R-09`, `AT-R-10` | Both claim `tests/test_units.lua` exercises `Units.DeepCopy` / `Units.Set`. Nothing anywhere calls either. `docs/file-index.md:100` carries the same wrong claim. |
| `BL-A-11` | Audit's count of nine is wrong in both directions — `docs/pending/LEDGER.md:63` is a frozen row that should not count, and `:64` carries the same notation and was missed. |
| `BL-R-04` | Misreads `core/Database.lua:619` — "Fires LedgerChanged when it actually runs" correctly describes the `days == 0` early return. |
| `BL-R-05` | Calls five comments nonsense; only `settings/Panel.lua:11` is genuinely incoherent. |
| `CM-A-05` | Audit cites use sites `:507` and `:711`; the actual uses are `:502-503` and `:734`. |
| `CM-A-13` | Audit's headline "loads after both bracket sites" is wrong — `modules\PerfSetup.lua` is TOC `:108`, `modules\MacroBar.lua` is `:111`. |
| `CM-A-30` | The false `.luacheckrc` comment is at `:66`, not `:74`. |
| `CM-R-13` | Cites `core/ConsumableMaster.lua:189-194`, the `dbDefaults` `order` array, not `KCM.Categories.LIST` at `defaults/Categories.lua:42`. |
| `KCD-A-12` | Audit escalates with "today's run printed PASS for both, and the sibling repo was never read". `../LibKa0s` exists on this machine, and the repo has no `.github` CI and no git hooks — the skip branch has essentially no live trigger here. |
| `KCD-A-13` | Audit's "the addon cannot currently pass the release gate" is wrong: `perf: skip` for an addon shipping no `tests/perf.lua` is the section's one named exception. |
| `KCD-A-02` | The sharpest sub-claim — that the table-versus-closure difference breaks `options-ui-§6`'s deferral — is wrong. All eight call sites already wrap it in a closure. |
| `KCD-A-16` | Audit's line list misses `:117, :123, :147, :213`. |
| `KCD-A-08` | Both bundles miss that `Ka0s_KickCD_PROFILE_CHANGED` also has two senders (`docs/ARCHITECTURE.md:120`) under the same rule. |
| `KCD-A-18` | Audit cites `modules/IconGrid_Render.lua:826`, the function header rather than the bracket. |
| `LH-R-03` | Cites `modules/Collector.lua:494` in a 221-line file, and misses the third fallback site. The fallback is not merely latent but **unreachable**. |
| `LH-R-06` | Cites `core/DebugLogSetup.lua:84-91` for a stub that lives at `:63`. The `ConsoleCheckbox` half is wrong — `libs/LibKa0s/DebugLog.lua:660` exports it and `tests/test_debuglog.lua:180` calls it. |
| `LH-A-26` | Cites `.luacheckrc:60` for the `LootHistoryDB` line, which is `:43`. |
| `LH-A-28` | Understates the safety net: `tests/test_schema.lua:140-148` already covers all six defaults. |
| `LH-A-38` | The audit's own row says "the three required items" where `documentation-§2` lists five. |
| `PM-R-05` | Both bundles cite `:138`/`:144`, which are the `test(` declaration lines; the guards are at `:140` and `:146`. |
| `PM-R-06` | The premise "every other cross-module reach in the same file guards first" is false — twelve of them do not. |
| `PM-R-11` | The sub-claim "nothing reads it" is false — `tests/test_canvas.lua:297` reads `NS.Schema.MSG_SETTINGS`. |
| `PM-A-12` | Audit files it as SHOULD; `documentation-§1` item 7 is a MUST. |
| `PC-R-01`, `PC-R-02` | The review cites `GlobalStrings_009.lua` for both; they live at `GlobalStrings_011.lua:203` and `:214`. |
| `PC-R-10` | Of three cited "correct" comparators, `core/Util.lua:18` is **not** parenthesized and leaks a count itself. |
| `PC-A-10` | Calls `CLAUDE.md` 64 lines; it is 63. |
| `PM-R-03` | Both bundles mis-cite the library ACK/STATE hexes as `632-634`/`633-637`; they are at `libs/LibKa0s/DebugLog.lua:68-70` and `:635-636`. |
| `LK-A-15` | The review's citation of `tests/test_kitsync.lua:79-92` is two lines off from the actual `:81-94`. |
| `CM-A-16` | An earlier draft of **this** document gave `CM-A-16` `CM-A-23`'s evidence verbatim (the `.pkgmeta` ignore list), erasing the finding while keeping the id in the coverage proof. Restored to the real finding — the within-`core/` load sequence, filed by the audit as **CM-49**. |
| `CM-A-31` | An earlier draft added a second half to this finding: that `tests/test_vendor_sync.lua:132`–`:133` CR-normalizes before comparing, "which `testing-§11` makes an explicit MUST NOT". **That correction is itself withdrawn.** The CR strip is required — one side is a `git show` blob (LF), the other a working tree pinned to CRLF — and removing it reddens every consumer's gate. Only the vacuous-pass half of `CM-A-31` survives. |
| `PC-R-01`, `PC-R-02` (second correction) | The re-derivation the plan asks for was **executed** here, loading `defaults/Defaults.lua` and all 26 `GlobalStrings/` chunks under `lua5.1`: **81 overrides checked, 6 conversion-sequence mismatches**, not 2. Four are deliberate, harmless truncations — `LOOT_DISENCHANT_CREDIT` (`[s]` vs `[s,s]`), `COMBATLOG_DISHONORGAIN` (`[]` vs `[s]`), `OPEN_LOCK_OTHER` (`[s,s]` vs `[s,s,s]`), `OPEN_LOCK_SELF` (`[s]` vs `[s,s]`) — because `string.format` ignores surplus arguments. Only the two filed Highs raise: `FACTION_STANDING_DECREASED_GENERIC` is `[s,d]` against Blizzard's `[s]` (a missing argument), and `FACTION_STANDING_INCREASED_GUARDIAN` is `[d]` against `[s,d]` (a name into `%d`). The acceptance criterion is therefore a **positional-prefix** rule, not equality — see `M2-01` and `M4-06`. |

## Process flags — not findings, but do not lift these into a PR

- **KickCD `docs/reviews/2026-08-05/05_FINAL_SUMMARY.md`** is written in the past tense ("two performance
  brackets … now close on every exit"; "the perf figures … now have a committed record") while the
  working tree is clean apart from the two bundles. Nothing was implemented.
- **prettychat `docs/reviews/2026-08-05/05_FINAL_SUMMARY.md`** carries counts ("Critical fixed: 2 · High
  fixed: 2 …") for work that was never applied.
- **LibKa0s `docs/reviews/2026-08-05/05_FINAL_SUMMARY.md`** claims 480 → 485 cases while its own
  `04_EXECUTION_PLAN` says 483.

All three carry a disclaimer banner. A document that reads as a changelog for changes that do not exist
is the exact shape that gets pasted into a PR description.

- **BankLedger review false negative.** `01_FINDINGS.md`'s "Not findings (checked and clear)" block
  states that every call site uses the shadowed `local print = NS.Print` upvalue and there is no bare
  global `print` anywhere in the addon's own source. **That is false.** `modules/Browser.lua:917` and
  `:926` call the global and the file declares no such upvalue — which is `BL-A-09`, on its third
  consecutive cycle. A reviewer who affirmatively clears a defect another agent has raised twice is
  worse than one who misses it.

- **PanelMaster review provenance header** reports `standards/standards/tiered-layout.md` as a 404 from a
  26-file Sections list. `STANDARDS.md` v2.21.0 links 25 section files and none is `tiered-layout`; the
  name survives only inside frozen changelog prose. The review "lost" a rule that does not exist.
