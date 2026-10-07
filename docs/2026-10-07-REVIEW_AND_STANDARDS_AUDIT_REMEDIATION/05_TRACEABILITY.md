# 05 — Traceability

Every finding from the 2026-10-07 review and audit, mapped to the work item that resolves it or to the
reason it is out of scope. Derived from `plan-data/items.json` (each item's `finding_ids`) and
`inputs/verified_findings.json` (grade, severity and cluster). When this page and `items.json` disagree,
`items.json` wins.

**Coverage.** Every one of the 251 in-scope findings maps to exactly one item. None is unmapped, none maps
to two items, and no out-of-scope finding is traced to an item. The 39 out-of-scope findings are listed
at the end with their reasons.

| | must | should | optional | no | refuted | total |
|---|---|---|---|---|---|---|
| Findings | 10 | 161 | 80 | 27 | 12 | **290** |

Grades are the final ones, after the owner's rulings in `inputs/OWNER_SCOPE.md`: MM-A-03 and DC-A-05
are downgraded from `must` to `should` (marked "owner: was must" below). LH-R-03 stays `must`, but its
LED-P2-01..24 checks are the owner's to run in the client. LH-STD lists them in `06_SMOKE_TESTS.md`, and
no agent records a result.

Severity is the verified severity (`severity_after`). The item's repository is the fix home. A finding
raised in a different repository says so in its title, for example a standard defect that an addon's
audit found.

---

## In scope: finding → item, by fix-home repository

### WowAddonStandards (38 findings)

| Finding | Grade | Sev | Cluster | Item | Milestone | Title |
|---|---|---|---|---|---|---|
| AT-A-14 | optional | info | C11 | WS-04 | M1 | toc-file-§5 worked example cites stale AbsorbTracker.toc line range (raised in AbsorbTracker) |
| AT-A-15 | should | low | C05 | WS-04 | M1 | AUDIT.md TOC check scoped to # Core block while toc-file-§5 covers the whole listing (raised in AbsorbTracker) |
| DC-A-14 | optional | low | C06 | WS-03 | M1 | line-endings-§7 EOL-gate MUST unscoped for kinds where testing does not apply (ungraded upstream observation) (raised in dev-copilot) |
| DC-A-15 | optional | info | C08 | WS-05 | M1 | documentation-§8 executable-content trigger names three triggers then only the first .lua file (ungraded upstream observation) (raised in dev-copilot) |
| DC-A-16 | should | low | C32 | WS-08 | M1 | versioning-git trunk-based MUST matches neither collection practice nor WAS CLAUDE.md (ungraded upstream observation) (raised in dev-copilot) |
| LK-A-08 | should | low | C11 | WS-07 | M1 | Standard's library-stack-§7 cites Options->Pool floor by stale line and omits OptionsNav.lua (raised in LibKa0s) |
| LK-A-10 | optional | info | C08 | WS-05 | M1 | library-stack-§7 claims its three applicability lists classify every section, but several subsections appear in none (raised in LibKa0s) |
| PC-R-08 | optional | low | C15 | WS-09 | M1 | 758 lines of library-missing degradation stubs serve an install packaging cannot produce (raised in PrettyChat) |
| WAS-A-01 | should | medium | C04 | WS-02 | M1 | Seven docs say no audit/review bundle is ever written into this repo |
| WAS-A-02 | should | low | C04 | WS-02 | M1 | Documentation map registers neither docs/audits/ nor docs/reviews/ |
| WAS-A-03 | should | low | C04 | WS-02 | M1 | DEPENDENCIES.md hard-codes a file count that the bundles will break |
| WAS-A-04 | should | low | C06 | WS-03 | M1 | Repo's own .gitattributes lacks *.py text eol=lf and is not the canonical §5 body |
| WAS-A-05 | should | low | C06 | WS-03 | M1 | documentation-§8 applies-unchanged row names only the *.sh carve-out |
| WAS-A-06 | should | low | C06 | WS-03 | M1 | Docs call this repo's .gitattributes the canonical non-client body (false while WAS-02 stands) |
| WAS-A-07 | should | low | C06 | WS-03 | M1 | EXECUTIVE_SUMMARY names only *.sh as mandatory carve-out |
| WAS-A-08 | should | medium | C08 | WS-06 | M1 | Playbook and sections still tell auditors every addon will fail launcher/disabled-state checks |
| WAS-A-09 | should | low | C11 | WS-07 | M1 | Cross-repo file:line citations have rotted (43 moved, 6 gone of 61) |
| WAS-A-10 | should | low | C11 | WS-07 | M1 | AUDIT.md's BankLedger worked example cites a moved line |
| WAS-A-11 | optional | low | C11 | WS-07 | M1 | Present-tense counts/inventories no longer match the tree |
| WAS-A-12 | optional | low | C08 | WS-05 | M1 | documentation-§3 numbers its last two hub sections in contradictory order |
| WAS-A-13 | should | low | C12 | WS-01 | M1 | Malformed references in changelog and a wrong item pointer |
| WAS-A-14 | should | medium | C08 | WS-05 | M1 | documentation-§6 frozen-store exemption list disagrees with documentation-§3 |
| WAS-A-15 | optional | low | C08 | WS-05 | M1 | documentation-§8 claims to classify every section but omits localization-§1-§4 and documentation-§9; arithmetic double-counts Module Map |
| WAS-A-16 | optional | low | C08 | WS-05 | M1 | Two Tier 2 summaries omit perf-analysis/README.md |
| WAS-A-17 | optional | info | C49 | WS-02 | M1 | Addon roster hard-coded outside ADDONS.md |
| WAS-A-18 | optional | low | C12 | WS-01 | M1 | Changelog out of order; standards/README contradicts itself on changelog position |
| WAS-R-01 | should | low | C06 | WS-03 | M1 | Standard's own .gitattributes breaks line-endings-§3 and §5 |
| WAS-R-02 | should | low | C06 | WS-03 | M1 | Seven restatements of the shebang carve-out still name only *.sh |
| WAS-R-03 | should | medium | C12 | WS-01 | M1 | STANDARDS.md index is 92% changelog and grows every release |
| WAS-R-04 | should | medium | C49 | WS-10 | M1 | Repo has no mechanical gate, so cheap checkable drift keeps slipping through |
| WAS-R-05 | should | medium | C08 | WS-06 | M1 | Scaffold runner comment says missing suites are skipped, opposite of testing-§9 and the kit |
| WAS-R-06 | should | low | C12 | WS-05 | M1 | documentation-§5 cited as the citation scheme, which is §6 |
| WAS-R-07 | optional | low | C12 | WS-01 | M1 | Index footer authority date stale by three releases |
| WAS-R-08 | optional | low | C06 | WS-03 | M1 | Line-ending check (e) splices file names into sh -c script text |
| WAS-R-09 | optional | low | C11 | WS-07 | M1 | Temporal 'today' claims and partial kit-file lists read as complete |
| WAS-R-11 | optional | low | C49 | WS-02 | M1 | Roster Folder links resolve outside the repository on GitHub |
| WAS-R-12 | optional | low | C12 | WS-01 | M1 | Malformed cross-reference 'preview-mode-§' in changelog |
| WG-R-08 | should | low | C20 | WS-09 | M1 | Standard's events-frames-taint §8 named-API trigger set omits C_Spell.GetSpellCooldown fields (raised in WhatGroup) |

### LibKa0s (19 findings)

| Finding | Grade | Sev | Cluster | Item | Milestone | Title |
|---|---|---|---|---|---|---|
| AM-R-03 | should | low | C07 | LK-01 | M1 | [upstream] The test kit's --list Total counts skipped cases, so the inventory cannot match the badge (raised in AuraMaster) |
| AT-R-08 | optional | info | C19 | LK-07 | M1 | LibKa0s Perf stub template still prints suspended = false (raised in AbsorbTracker) |
| LK-A-01 | should | low | C48 | LK-09 | M1 | Five watch-list band entries 'Accepted' for 7-10 consecutive release runs, past the three-run shelf life |
| LK-A-02 | should | low | C33 | LK-08 | M1 | 22 British-spelling lines in two live docs (adoption-prompt.md, adoption-report.md); register row 3 misclassifies the prompt as a frozen record |
| LK-A-03 | optional | low | C01 | LK-07 | M1 | Hand-maintained headroom figure for testkit/mock_base.lua says 44 lines; tree says 42 |
| LK-A-04 | should | low | C27 | LK-06 | M1 | Two inline addon-API ladders end on deprecated globals (GetAddOnMetadata, IsAddOnLoaded); payload comment contradicts the standard's compat worked case |
| LK-A-05 | should | low | C25 | LK-07 | M1 | Register evidence ids (LibKa0s-A-07/-A-10/-A-03) do not resolve in this repo; cross-repo plan ids LK-29/LK-30 collide with this repo's own audit ids |
| LK-A-06 | optional | low | C18 | LK-05 | M1 | Shipped Slash.lua comment cites the standard by file:line (slash-commands.md:34); issue #43 fix skipped by two payload releases |
| LK-A-07 | should | low | C13 | LK-11 | M1 | Four closed issues (#32, #33, #37, #39) still carry open-only state:triaged label |
| LK-R-01 | optional | low | C46 | LK-03 | M1 | LineChart draws unclipped and ChartMath.Dashes is unbounded: one far off-plot point in a dashed range creates unbounded permanent Line regions |
| LK-R-02 | should | low | C47 | LK-04 | M1 | Autocomplete hooks installed once per box die silently on a later SetScript; re-calling lib.Autocomplete cannot reinstall them |
| LK-R-03 | should | low | C46 | LK-03 | M1 | Chart hover does not resync on SetData/Render; every host must call ClearHover before repainting |
| LK-R-06 | should | low | C30 | LK-05 | M1 | ParseValue accepts nan/inf and the write seam stores them on an unbounded number row; clamp absorbs NaN only by argument order |
| LK-R-07 | optional | info | C47 | LK-04 | M1 | owners/hooked weak-table comment claims entries are collected, which Lua 5.1 (no ephemerons) cannot do |
| LK-R-08 | optional | low | C47 | LK-04 | M1 | opts.maxRows accepts a non-integer, desynchronizing row count from list height |
| LK-R-09 | optional | info | C47 | LK-04 | M1 | Autocomplete skin() rebuilds the backdrop on every render (unverified cost) |
| LK-R-10 | optional | info | C26 | LK-03 | M1 | Chart default x labels use C-runtime English month abbreviation (%b) (in-client unverified) |
| LK-R-11 | optional | low | C48 | LK-10 | M1 | v1.69.0/v1.70.0 widget suites carry no '-- red under:' notes on negative assertions |
| WG-R-09 | should | low | C20 | LK-02 | M1 | LibKa0s test kit has no secret-value mock, forcing per-addon simulators (raised in WhatGroup) |

### dev-copilot (27 findings)

| Finding | Grade | Sev | Cluster | Item | Milestone | Title |
|---|---|---|---|---|---|---|
| DC-A-01 | should | low | C04 | DC-06 | M1 | docs/ARCHITECTURE.md hub is absent (documentation-§8 Substitutes #3) |
| DC-A-02 | should | low | C04 | DC-06 | M1 | No ## Documented deviations register (derived from DC-01) |
| DC-A-03 | should | low | C04 | DC-06 | M1 | No ## Documentation map (derived from DC-01) |
| DC-A-05 | should (owner: was must) | medium | C04 | DC-15 | M1 | Audit agent wrongly says neither documentation repo has docs/ARCHITECTURE.md, skipping WAS's real register |
| DC-A-06 | must | medium | C50 | DC-01 | M1 | Bounded-runs hook denies the tool-presence probe 'command -v lizard' |
| DC-A-07 | should | low | C51 | DC-07 | M1 | Stale wow-addon / kind text left after the phase-2 rename |
| DC-A-08 | should | low | C51 | DC-13 | M1 | DEPENDENCIES.md inventory, three citations and version floors have drifted |
| DC-A-09 | should | low | C11 | DC-09 | M1 | Worked examples in specs no longer match the trees they cite |
| DC-A-10 | should | low | C06 | DC-15 | M1 | Audit agent's line-ending check (c) omits the mandatory *.py carve-out |
| DC-A-11 | optional | low | C33 | DC-12 | M1 | 37 British spellings in live specs and root docs |
| DC-A-13 | optional | info | C53 | DC-14 | M1 | Stale origin/main branch from the initial commit |
| DC-R-01 | should | medium | C50 | DC-03 | M1 | ka0s-bounded timeout kills only the top process, then reports the run as stopped |
| DC-R-02 | must | medium | C50 | DC-01 | M1 | Bounded-runs hook denies 'command -v luacheck', a plain tool-presence probe |
| DC-R-03 | should | low | C52 | DC-05 | M1 | Line-ending hook replaces a symlinked file with a regular file and leaves the target unconverted |
| DC-R-04 | should | medium | C53 | DC-08 | M1 | Issue commands disagree on what 'all' means in a WoW repo |
| DC-R-05 | should | medium | C53 | DC-10 | M1 | Cross-addon pass writes a fixed shared /tmp/roots.txt, violating the plugin's own shared-path rule |
| DC-R-06 | should | medium | C52 | DC-04 | M1 | Line-ending hook rewrites user files on every Write/Edit and has no automated test |
| DC-R-07 | should | medium | C53 | DC-11 | M1 | wow-new-addon must edit WowAddonStandards roster without the Edit tool, and its wording implies it may push |
| DC-R-08 | optional | low | C50 | DC-03 | M1 | ka0s-bounded computes the slot count once, before the wait loop |
| DC-R-09 | should | low | C51 | DC-13 | M1 | DEPENDENCIES.md inventory and three citations are stale |
| DC-R-10 | should | low | C51 | DC-07 | M1 | Stale wow-addon mentions survive after phase 2 closed |
| DC-R-11 | optional | info | C51 | DC-10 | M1 | Cross-addon baseline table is fourteen LibKa0s releases behind |
| DC-R-12 | optional | low | C53 | DC-11 | M1 | finalize's push-rejection recovery path (git pull --ff-only) can never succeed |
| DC-R-13 | optional | low | C50 | DC-02 | M1 | Bounded-runs matcher false negatives on 'sh -c' and 'ulimit -v unlimited' |
| DC-R-14 | optional | low | C50 | DC-01 | M1 | Bounded-runs tests leak temporary directories on every run |
| DC-R-15 | optional | low | C51 | DC-07 | M1 | User-facing profile list omits the tooling kind |
| WAS-A-20 | should | low | C04 | DC-15 | M1 | dev-copilot documentation-lane audit prompt repeats stale content (raised in WowAddonStandards) |

### AbsorbTracker (16 findings)

| Finding | Grade | Sev | Cluster | Item | Milestone | Title |
|---|---|---|---|---|---|---|
| AT-A-01 | should | low | C03 | RV-AT | M2 | LibKa0s v1.69.0 and v1.70.0 re-vendors have no docs/revendor/ bundle and no register row |
| AT-A-02 | should | low | C01 | AT-09 | M3 | Doc and comment drift against the tree (seven items, recurs) |
| AT-A-03 | should | low | C22 | AT-09 | M3 | docs/automated-tests/README.md quotes raw lizard as the complexity suite command |
| AT-A-04 | should | low | C05 | AT-03 | M3 | TOC line settings\Schema.lua is load-bearing and unannotated |
| AT-A-05 | should | low | C05 | AT-03 | M3 | TOC line settings\OptionsSetup.lua is load-bearing and unannotated |
| AT-A-06 | should | low | C25 | AT-04 | M3 | savedvariables-§1 register row records a shape the standard now sanctions (retire it) |
| AT-A-07 | should | low | C15 | AT-02 | M3 | LibKa0s-Widgets-1.0 adopted with no setup seam, stub or parity case |
| AT-A-08 | optional | info | C29 | AT-08 | M3 | Pre-formatted chat line in core/Database.lua (recurs with new site) |
| AT-A-09 | optional | low | C24 | AT-08 | M3 | Two hand-rolled log-on-change memos instead of console gates; no onClear |
| AT-R-01 | should | low | C35 | AT-01 | M3 | Offline 'coalesced repaint' and 'zero-overhead' perf scenarios measure a test-written fan-out, not shipped doRepaint |
| AT-R-02 | optional | low | C21 | AT-05 | M3 | doRepaint allocates a fresh closure on every coalesced pass |
| AT-R-03 | optional | low | C19 | AT-06 | M3 | /at debug hold arms its expiry timer while stood down for a perf capture |
| AT-R-04 | optional | low | C34 | AT-07 | M3 | Standing up during combat leaves unlocked bars in preview for the whole fight |
| AT-R-05 | optional | low | C35 | AT-09 | M3 | Changing Master scale may move dragged bars (unverified in-client) |
| AT-R-06 | optional | low | C19 | AT-06 | M3 | Degraded-load test asserts Perf.suspended, which the show ladder no longer reads |
| AT-R-07 | should | low | C07 | RV-AT | M2 | Testkit --list Totals count declared skips while its preamble says the badge must agree |

### AuraMaster (15 findings)

| Finding | Grade | Sev | Cluster | Item | Milestone | Title |
|---|---|---|---|---|---|---|
| AM-A-01 | should | low | C03 | RV-AM | M2 | LibKa0s v1.69.0 and v1.70.0 re-vendors have no docs/revendor/ bundle |
| AM-A-02 | should | low | C10 | AM-09 | M3 | docs/ARCHITECTURE.md is 426 lines and its Module Map runs 94 lines past the ~60-line spill rule |
| AM-A-03 | should | low | C02 | AM-05 | M3 | Complexity record is 173 commits stale and unsighted; logCandidates now CCN 18 would block the release gate |
| AM-A-04 | should | low | C36 | AM-10 | M3 | Tracked .claude/ directory is not ignored in .pkgmeta (line commented out), so the agent command file ships |
| AM-A-05 | should | low | C13 | AM-STD | M3 | Closed issue #22 still carries the open-status label state:untriaged |
| AM-A-06 | should | low | C01 | AM-08 | M3 | Docs and comments still say the launcher's left-click toggles test mode; stale map row and test comment |
| AM-A-07 | should | low | C15 | AM-03 | M3 | Library-absent Slash stub copies FormatRow's em-dash row shape |
| AM-A-08 | should | low | C24 | AM-02 | M3 | Schema-migration debug lines are written while logging is off at load and never reach the log |
| AM-A-09 | should | low | C36 | AM-10 | M3 | 26 MB of media/screenshots ships in the package (observation, owner's call) |
| AM-R-01 | should | medium | C16 | AM-05 | M3 | logCandidates is at CCN 18, above the release gate's limit of 15 |
| AM-R-02 | should | low | C17 | AM-06 | M3 | core/Database.lua is 1406 lines and every schema step adds to it |
| AM-R-04 | optional | low | C17 | AM-04 | M3 | tests/test_anchors_drag.lua is 10 lines below the 1500-line cap |
| AM-R-05 | should | low | C14 | AM-01 | M3 | /am delete 3 deletes container #3 even when a different container is named "3" |
| AM-R-06 | optional | info | C26 | AM-07 | M3 | Translated labels are lowercased with byte-wise :lower() |
| AM-R-07 | optional | info | C14 | AM-03 | M3 | debug help row and documented container listing use punctuation that differs from the standard and the actual output |

### BankLedger (10 findings)

| Finding | Grade | Sev | Cluster | Item | Milestone | Title |
|---|---|---|---|---|---|---|
| BL-A-01 | should | low | C03 | RV-BL | M2 | LibKa0s v1.69.0 and v1.70.0 re-vendors have no docs/revendor/ bundle (recurs, narrowed from 25 tags) |
| BL-A-02 | should | low | C16 | BL-01 | M3 | LT.GroupEntries measures CCN 16; next release tag blocked |
| BL-A-03 | should | low | C07 | RV-BL | M2 | Generated test inventory Total (1259) folds the kit's declared skip; README badge 1258/1258 disagrees |
| BL-A-04 | should | low | C01 | BL-04 | M3 | Stale prose and dangling pointers (recurs, new sites) |
| BL-A-05 | optional | info | C29 | BL-02 | M3 | Six printer calls pre-format with :format / .. (SHOULD NOT observation; reopens with new sites) |
| BL-R-01 | should | low | C16 | BL-01 | M3 | LT.GroupEntries crossed CCN 15 when Type & SubType grouping landed |
| BL-R-02 | should | low | C17 | BL-03 | M3 | modules/Browser.lua at 1427/1500 lines; named peel seam never cut |
| BL-R-03 | optional | low | C37 | BL-02 | M3 | Every ApplyView / tab switch recomputes the window two or three times |
| BL-R-04 | should | low | C37 | BL-02 | M3 | Search filter matches untrimmed text while suggestions trim |
| BL-R-05 | should | low | C01 | BL-04 | M3 | Seven doc lines describe a single saved view; debug.md says session-only tab is written; PANEL-28 checks one tab |

### ConsumableMaster (14 findings)

| Finding | Grade | Sev | Cluster | Item | Milestone | Title |
|---|---|---|---|---|---|---|
| CM-A-01 | should | low | C03 | RV-CM | M2 | LibKa0s v1.69.0 and v1.70.0 re-vendors have no docs/revendor/ bundle or register row |
| CM-A-02 | should | low | C01 | CM-07 | M3 | 19 stale file:line citations in docs/ARCHITECTURE.md and a retired /wow-addon:perf-analysis command name |
| CM-A-03 | should | low | C05 | CM-08 | M3 | core\SlashDump.lua TOC line is load-bearing (captures KCM.Say at file scope) but not annotated |
| CM-A-04 | should | low | C25 | CM-07 | M3 | Two deviations-register rows cite evidence ids that do not resolve (or resolve to unrelated findings) in this repo |
| CM-A-05 | should | low | C22 | CM-07 | M3 | docs/testing.md complexity row quotes the blind raw lizard command instead of the sighted runner |
| CM-A-07 | optional | info | C05 | CM-08 | M3 | TOC # Defaults group's conventional positions are unmarked |
| CM-R-01 | must | high | C38 | CM-01 | M3 | Per-profile macro fingerprint skips writes to account-wide macros holding another profile's body or deleted entirely |
| CM-R-02 | must | high | C38 | CM-02 | M3 | Devourer Demon Hunter spec (12_1480) has no stat-priority seed; ranks as Agility with no secondaries |
| CM-R-03 | optional | low | C38 | CM-06 | M3 | Every out-of-combat recompute re-ranks every category for flyouts with no score cache (63% of pass allocation) |
| CM-R-04 | should | medium | C38 | CM-03 | M3 | Spec change runs no discovery pass, so unseeded bag consumables are missed for the new spec until bags change |
| CM-R-05 | optional | low | C38 | CM-05 | M3 | Composite config resolution written twice; flyout copy compositeRefs is the max-CCN function (15) |
| CM-R-06 | should | low | C30 | CM-04 | M3 | /cm priority accepts any tonumber token: zero, negative, fractional, hex, exponent |
| CM-R-07 | should | low | C21 | CM-03 | M3 | PLAYER_SPECIALIZATION_CHANGED unit argument ignored; groupmates' respecs trigger recompute |
| CM-R-08 | should | low | C38 | CM-02 | M3 | Stat-priority seed test checks per class, not per spec, so it cannot catch F-002 |

### KickCD (13 findings)

| Finding | Grade | Sev | Cluster | Item | Milestone | Title |
|---|---|---|---|---|---|---|
| KC-A-01 | should | low | C03 | RV-KC | M2 | LibKa0s v1.69.0 and v1.70.0 vendored with no re-vendor bundle |
| KC-A-02 | should | low | C01 | KC-08 | M3 | Four doc/comment inventories and descriptions no longer match the tree |
| KC-A-03 | optional | low | C18 | KC-09 | M3 | 17 bare §N citations that name no rule file |
| KC-A-04 | optional | low | C31 | KC-05 | M3 | Migration target is Database.CURRENT_DB_VERSION, not NS.SCHEMA_VERSION |
| KC-A-06 | optional | info | C13 | KC-10 | M3 | Closed decline #11 (no RenderGrid) contradicted by the tree |
| KC-A-07 | should | low | C07 | RV-KC | M2 | docs/test-cases.md Totals folds the skipped case into the total |
| KC-R-01 | must | medium | C39 | KC-01 | M3 | Cast bar keeps a stale primary-icon anchor after the icon grid empties |
| KC-R-02 | should | low | C26 | KC-02 | M3 | Cast-bar name truncation counts bytes, not characters |
| KC-R-03 | optional | info | C14 | KC-04 | M3 | Unknown /kcd debug word toggles the debug console |
| KC-R-04 | optional | info | C14 | KC-04 | M3 | /kcd debug castbar and /kcd debug interrupt can only show the target |
| KC-R-05 | optional | low | C39 | KC-03 | M3 | Glow gate ignores casts by a non-attackable target while the target_casting trigger counts them |
| KC-R-08 | should | low | C39 | KC-07 | M3 | .luacheckrc whitelists 22 read-globals no shipped file reads |
| KC-R-09 | optional | low | C21 | KC-06 | M3 | Util.Throttle allocates an args table on every call, including every SPELL_UPDATE_COOLDOWN |

### LootHistory (27 findings)

| Finding | Grade | Sev | Cluster | Item | Milestone | Title |
|---|---|---|---|---|---|---|
| LH-A-01 | should | low | C05 | LH-05 | M3 | Escrow.lua load-bearing TOC position (below Reconciler) carries no annotation |
| LH-A-02 | should | low | C40 | LH-05 | M3 | Module files reach into other modules' tables at file load; AnalyticsCharts extends NS.Analytics without idempotent publish |
| LH-A-03 | should | low | C10 | LH-15 | M3 | ARCHITECTURE.md hub is 478 lines and ## Module map (77 lines) is past the spill threshold |
| LH-A-04 | should | low | C15 | LH-04 | M3 | Perf library-absent stub has no stub-surface parity case |
| LH-A-05 | should | low | C09 | LH-17 | M3 | README Usage closes on two sentences, not one |
| LH-A-06 | should | low | C01 | LH-16 | M3 | Counts and citations in the doc set drifted from the tree (7 items) |
| LH-A-07 | should | low | C09 | LH-17 | M3 | 1.4.0 Version History row carries a contributor-facing, unprefixed, now-false line |
| LH-A-08 | should | low | C22 | LH-16 | M3 | DEPENDENCIES.md quotes raw lizard as the complexity check |
| LH-A-09 | should | low | C09 | LH-15 | M3 | Documentation map's out-of-scope list misses docs/perf-analysis/<run>/ and over-freezes docs/automated-tests/ |
| LH-A-10 | should | low | C31 | LH-16 | M3 | schema.md holdings writer list omits two writers |
| LH-A-11 | should | low | C02 | LH-14 | M3 | Complexity record unsighted and 171 commits stale; HEAD has 26 functions above CCN 15; band files past re-check triggers |
| LH-A-12 | optional | info | C29 | LH-07 | M3 | Five chat lines pre-format arguments before the shared printer |
| LH-A-13 | should | low | C07 | RV-LH | M2 | Generated inventory Totals counts the skipped case; badge does not |
| LH-A-15 | should | low | C05 | LH-05 | M3 | AnalyticsCharts.lua load-bearing TOC position unannotated (derived from LH-78) |
| LH-A-16 | should | low | C05 | LH-05 | M3 | Timeline.lua load-bearing TOC position unannotated (derived from LH-78) |
| LH-A-17 | should | low | C05 | LH-05 | M3 | settings/Panel.lua load-bearing TOC position unannotated (derived from LH-78) |
| LH-A-18 | should | low | C05 | LH-05 | M3 | # Modules TOC group marks no position conventional; header '(Attribution before Collector)' unexplained (derived from LH-78) |
| LH-R-01 | should | medium | C16 | LH-14 | M3 | 26 functions above CCN 15 since 2026-10-01 block the next release tag |
| LH-R-02 | should | medium | C17 | LH-08 | M3 | BrowserTable.lua is 24 lines under the 1500 cap; both browser files past their own re-check triggers |
| LH-R-03 | must | medium | C40 | LH-STD | M3 | Ledger Phase 2 in-client checks LED-P2-01..24 have no recorded result though the doc's sign-off requires them |
| LH-R-04 | should | low | C19 | LH-02 | M3 | Coalesced repaint canceled by stand-down never fires again on the settings panel's storage readout |
| LH-R-05 | should | low | C40 | LH-03 | M3 | ledgerEvent perf bucket includes the full combat-exit flush though declared as dirty bits only |
| LH-R-06 | optional | low | C40 | LH-15 | M3 | Auction exits: TTL clock restarts on every new exit and one sale mail books every pending exit of the item as sold |
| LH-R-08 | optional | info | C40 | LH-06 | M3 | Two parsers for one <holder>/<container> location string |
| LH-R-09 | optional | low | C01 | LH-16 | M3 | docs/testing.md states a stale suite count (44 vs 60) |
| LK-R-04 | optional | info | C46 | LH-06 | M3 | Chart owns OnSizeChanged->Render, so a host rendering from its own layout pass may draw twice (unverified) (raised in LibKa0s) |
| PC-R-01 | must | high | C44 | LH-01 | M3 | LootHistory's cached loot/currency patterns go stale whenever PrettyChat rewrites the chat globals mid-session (raised in PrettyChat) |

### MultiMeters (17 findings)

| Finding | Grade | Sev | Cluster | Item | Milestone | Title |
|---|---|---|---|---|---|---|
| MM-A-01 | should | low | C03 | RV-MM | M2 | LibKa0s v1.69.0 and v1.70.0 re-vendored with no docs/revendor/ bundle and no register row (recurs, narrowed) |
| MM-A-02 | should | low | C03 | RV-MM | M2 | Same two re-vendors left three docs naming the previous LibKa0s tag or kit revision (derived from MM-A-19) |
| MM-A-03 | should (owner: was must) | low | C18 | MM-10 | M3 | One standard citation still malformed: (architecture-4) (recurs, narrowed) |
| MM-A-04 | should | low | C01 | MM-10 | M3 | ARCHITECTURE.md hub contradicts itself and the tree in four places; two code comments are false (recurs) |
| MM-A-05 | should | low | C27 | MM-07 | M3 | Library-absent GetAddOnMetadata fallback keeps a dead rung no admitted client can reach (new) |
| MM-A-06 | should | low | C09 | MM-08 | M3 | 1.1.0 release notes never told players /mm set global.minimap.hide became global.minimap.shown (new) |
| MM-A-07 | should | low | C22 | MM-09 | M3 | Two docs quote raw (blind) lizard as the complexity check, and DEPENDENCIES.md pins lizard 1.24.0 (new) |
| MM-A-08 | should | low | C41 | MM-05 | M3 | Conformance suite's launcher step 8 drives only the left click; right-click menu 'wrote nothing, showed no frame' clause pinned nowhere (new) |
| MM-A-09 | optional | low | C10 | MM-10 | M3 | docs/ARCHITECTURE.md is 578 lines, past the hub's ~400-line SHOULD ceiling (recurs, narrowed) |
| MM-R-01 | must | high | C41 | MM-01 | M3 | With Merge pets on, a pet ahead of its owner in a column loses its numbers to the owner's own cell |
| MM-R-02 | should | medium | C41 | MM-01 | M3 | Test covers pet-before-owner order but never checks the total, so F-001 passes green |
| MM-R-03 | should | low | C41 | MM-03 | M3 | Under-populated roster is rebuilt on every lookup, not once per refresh; comments say the opposite |
| MM-R-04 | should | low | C41 | MM-04 | M3 | Renaming a window to a different case of its own name appends ' 2' |
| MM-R-05 | optional | info | C14 | MM-10 | M3 | /mm window copy cannot name a source window containing a space, including every default window name |
| MM-R-06 | optional | info | C41 | MM-02 | M3 | plainTruth is defined twice, both copies outside core/Secrets.lua |
| MM-R-07 | optional | low | C20 | MM-02 | M3 | Source-row diagnostics compare isLocalPlayer without the secret guard; field census treats booleans as plain |
| MM-R-08 | should | low | C41 | MM-06 | M3 | Retired drill-down back button's code still runs on every render, with three tests covering it |

### PanelMaster (20 findings)

| Finding | Grade | Sev | Cluster | Item | Milestone | Title |
|---|---|---|---|---|---|---|
| PM-A-01 | should | medium | C23 | PM-02 | M3 | Reset all settings leaves session-only rows (Lock frame, Debug console) untouched |
| PM-A-02 | should | low | C23 | PM-02 | M3 | Global-reset tests do not prove blast radius (dependent of PM-049) |
| PM-A-03 | should | low | C15 | PM-08 | M3 | Library-absent Slash stub copies LibKa0s coloured key = value formatter |
| PM-A-04 | should | low | C27 | PM-09 | M3 | Dead fallback rungs call removed AddOns globals |
| PM-A-06 | should | low | C09 | PM-12 | M3 | CLAUDE.md stub items out of order (provenance before green gate) |
| PM-A-07 | should | low | C22 | PM-11 | M3 | Automated-tests README quotes raw lizard instead of the sighted runner |
| PM-A-08 | should | low | C09 | PM-12 | M3 | README placeholders and un-prefixed highlight reintroduced |
| PM-A-09 | should | low | C01 | PM-11 | M3 | Docs, register row and comments out of sync with tree |
| PM-A-10 | optional | info | C10 | PM-11 | M3 | ARCHITECTURE.md over ~400-line hub guideline (422) |
| PM-A-11 | should | low | C03 | RV-PM | M2 | LibKa0s v1.69.0 and v1.70.0 vendored with no re-vendor bundle |
| PM-A-12 | should | low | C13 | PM-10 | M3 | Closed issue #47 still labelled state:triaged |
| PM-R-01 | should | medium | C26 | PM-05 | M3 | Non-Latin panel names collapse to one frame name; only one can exist |
| PM-R-02 | must | high | C23 | PM-01 | M3 | Delete all panels popup says 'on this character' but profile is shared |
| PM-R-03 | should | medium | C30 | PM-06 | M3 | Panel number fields accept NaN/±inf; /pm recover cannot repair NaN |
| PM-R-04 | should | low | C42 | PM-07 | M3 | R.Sanitize skips accentColor, accentBorderColor, artBlend, artDesaturate |
| PM-R-05 | should | medium | C23 | PM-03 | M3 | Editor per-panel Delete and Reset act on one click; comment falsely claims Reset is confirmed |
| PM-R-06 | should | low | C19 | PM-04 | M3 | Combat-held unlock survives stand-down and fires at a later combat exit |
| PM-R-07 | optional | low | C42 | PM-07 | M3 | Panel list/picker show enabled==nil as disabled while renderer draws it |
| PM-R-08 | optional | low | C01 | PM-11 | M3 | Comment cites moved line in Registry.lua |
| PM-R-09 | should | low | C07 | RV-PM | M2 | Kit inventory header says badge must match Totals, contradicting testing-§5 on skips |

### PartyFrameEnhanced (13 findings)

| Finding | Grade | Sev | Cluster | Item | Milestone | Title |
|---|---|---|---|---|---|---|
| PFE-A-01 | should | low | C28 | PF-03 | M3 | Post-combat secure-write listener is a private CreateFrame event frame in an AceEvent addon |
| PFE-A-02 | should | low | C03 | RV-PF | M2 | LibKa0s v1.69.0 and v1.70.0 re-vendors have no docs/revendor/ bundle |
| PFE-A-03 | should | low | C01 | PF-05 | M3 | Documentation drift: kit 35, retired /wow-addon:perf-analysis, compat shim count 15 vs 14 |
| PFE-A-04 | should | low | C09 | PF-05 | M3 | Documentation map lost its fourth table (### Addon-specific) |
| PFE-A-05 | optional | low | C10 | RV-PF | M2 | docs/ARCHITECTURE.md hub is 435 lines, past the ~400 spill guideline |
| PFE-A-06 | optional | info | C25 | PF-05 | M3 | Register row text nits: row 1 'pending the owner's ratification', row 2 Why cites no issue/bundle |
| PFE-A-07 | optional | low | C09 | PF-05 | M3 | settings-panel.md uses a Page\|Tab\|Covers table and page→tab headings instead of Page\|Covers |
| PFE-A-11 | should | low | C03 | RV-PF | M2 | Four live docs still name LibKa0s v1.68.1 / kit 36 (derived from PFE-26) |
| PFE-R-01 | should | low | C34 | PF-02 | M3 | A profile switch during combat turns preview on mid-fight, bypassing the combat refusal |
| PFE-R-02 | should | low | C43 | PF-01 | M3 | One raising deferred secure write aborts the flush and orphans every later key for the session |
| PFE-R-03 | optional | low | C43 | PF-01 | M3 | unwrapFrame re-wraps another addon's handler without a guard, inside the secure queue |
| PFE-R-04 | optional | info | C14 | PF-04 | M3 | /pfe status prints 'unlocked' twice whenever the elements are unlocked |
| PFE-R-05 | optional | low | C43 | PF-01 | M3 | /pfe profile new rebuilds everything twice and logs a no-op reset |

### PrettyChat (12 findings)

| Finding | Grade | Sev | Cluster | Item | Milestone | Title |
|---|---|---|---|---|---|---|
| PC-A-01 | should | low | C03 | RV-PC | M2 | LibKa0s v1.69.0 and v1.70.0 re-vendors have no docs/revendor/ bundle |
| PC-A-02 | should | low | C01 | PC-06 | M3 | Docs and comments drifted from the tree in four places (majors sentence, perf sweep, .luacheckrc counts, PRETTYCHAT-A-NN ids) |
| PC-A-03 | optional | info | C10 | PC-07 | M3 | docs/ARCHITECTURE.md hub is 434 lines, over the ~400 target |
| PC-A-05 | optional | info | C13 | PC-08 | M3 | Closed issue #8 asserts per-character profiles will never be offered; the Profiles page now offers them |
| PC-R-02 | should | medium | C44 | PC-01 | M3 | Settings panel stores an empty format string that the CLI refuses |
| PC-R-03 | optional | low | C23 | PC-03 | M3 | Categories page Defaults button wipes all eight tabs' custom formats without confirmation |
| PC-R-04 | should | low | C44 | PC-02 | M3 | Downgrading the addon deletes overrides a newer build stored and lowers the schema stamp |
| PC-R-05 | should | low | C44 | PC-05 | M3 | docs/data-flow.md wrongly says _G writes don't taint |
| PC-R-06 | optional | low | C44 | PC-05 | M3 | Comment volume rivals code and some comment figures contradict each other |
| PC-R-07 | should | low | C07 | RV-PC | M2 | Testkit --list Total counts skipped cases, so test-cases.md (573) contradicts the badge (572/572) |
| PC-R-10 | optional | low | C01 | PC-06 | M3 | ARCHITECTURE.md:202 cites stale LootHistory line numbers |
| PC-R-11 | optional | info | C14 | PC-04 | M3 | /pc test category General resolves, then prints '(no matching strings)' |

### WhatGroup (10 findings)

| Finding | Grade | Sev | Cluster | Item | Milestone | Title |
|---|---|---|---|---|---|---|
| WG-A-01 | should | low | C28 | WG-03 | M3 | Stand-down's owed-Hide PLAYER_REGEN_ENABLED registration is a bare self:RegisterEvent, outside the pcalled NS.SafeRegisterEvent helper |
| WG-A-02 | should | low | C03 | RV-WG | M2 | LibKa0s v1.69.0 and v1.70.0 re-vendored with no docs/revendor bundle and no register row (reopened) |
| WG-A-03 | should | low | C01 | WG-06 | M3 | Docs and comments drifted from the tree (settings row counts, Compat shim count, stale file:line citations, .pkgmeta screenshot note, Compat load-order header) (reopened) |
| WG-R-01 | must | medium | C20 | WG-01 | M3 | Teleport-cooldown reader compares cooldown values that can be secret in combat, killing the popup ticker and aborting the join notice |
| WG-R-02 | should | medium | C20 | WG-01 | M3 | Test mock cannot produce a secret cooldown, so the suite never exercises F-001's combat path |
| WG-R-03 | should | low | C45 | WG-02 | M3 | /wg test notify and the panel Test button overwrite the player's real captured group in pendingInfo |
| WG-R-04 | should | medium | C45 | WG-02 | M3 | Panel Test button pressed while disabled builds a hidden popup that appears unasked when the addon is re-enabled; its test only checks stored data |
| WG-R-05 | should | low | C45 | WG-04 | M3 | Popup Height tooltip states default 260 but the shipped default is 280 |
| WG-R-06 | should | low | C01 | WG-05 | M3 | docs/performance.md figures are stale against today's offline perf run |
| WG-R-07 | optional | info | C45 | WG-02 | M3 | reloadProfile comment promises per-profile migration that the account-wide schema stamp cannot deliver |

---

## Items with no finding id

21 items carry no finding id of their own. Each one exists for a reason the plan or the owner's rulings
give:

| Item(s) | Why it exists |
|---|---|
| WS-11 | Closes standard v2.77.0: ripples WS-01…WS-10 through the executive summary, context pack, playbooks, README and index blurbs, and gates on `check-standard.sh`. |
| LK-12 | Cuts LibKa0s v1.71.0 (release record, ANALYSIS.md, local tag), which every M2 item needs. |
| LH-09, LH-10, LH-11, LH-12, LH-13 | Slices of LH-R-01 (26 functions above CCN 15). LH-14 carries the finding id and finishes the work. |
| LH-18 | The second half of LH-R-02, which is traced on LH-08. The critic split the original LH-08 into two pure moves, and this one moves Browser's widget kit into `modules/BrowserWidgets.lua` (`modules/Browser.lua` is at 1416 lines, past its own re-check trigger). |
| BL-05, CM-09, PF-06, WG-07 | Cluster C27 parity: the same dead bare-global `GetAddOnMetadata` fallback that LK-06, MM-07 and PM-09 remove. This is a scope addition the critic made, and the owner can drop these four without affecting any traced finding. |
| AT-STD, BL-STD, CM-STD, KC-STD, MM-STD, PM-STD, PF-STD, PC-STD, WG-STD | Roll each addon's standards reference to v2.77.0 (OWNER_SCOPE ruling 5) and sync the docs. AM-STD and LH-STD also do this, but they carry AM-A-05 and LH-R-03. |

---

## Out of scope: the 39 `no` findings, by repository raised in

These are recorded in `01_CONSOLIDATED_FINDINGS.md` and nothing is done for them (OWNER_SCOPE ruling 1).
The verdict `no` means real but not worth changing (27). `refuted` means it did not survive the reality
check (12). The owner can overrule any of them, and it then moves into a new item as `should`.

### WowAddonStandards (2)

| Finding | Verdict | Cluster | Title | Reason |
|---|---|---|---|---|
| WAS-A-19 | no | C04 | Deviation register empty, correctly | An informational row. A register entry of 'None.' is correct, and the will-not-do issues decline proposals rather than depart from rules. |
| WAS-R-10 | no | C12 | 'One-page TL;DR' is about ten pages | The summary really is 4,733 words under a 'One-page TL;DR' label, but the label appears in six places (EXECUTIVE_SUMMARY.md:3, standards/README.md:12, STANDARDS.md:89, CLAUDE.md:50, README.md:61/:143). Renaming it changes no reader's behaviour and no audit's accuracy, and the real problem, a duplicated second copy, is explicitly deferred. |

### LibKa0s (2)

| Finding | Verdict | Cluster | Title | Reason |
|---|---|---|---|---|
| LK-A-09 | no | C27 | Standard's compat worked case (GetAddOnMetadata is a dead rung) contradicts LibKa0s Env.lua comment | The contradiction is real, but the standard is the side that is right, so there is no standard defect and no upstream route. This finding duplicates LK-A-04, and rewriting the Env.lua comment there resolves it. |
| LK-R-05 | refuted | C47 | Autocomplete calls host provider and onPick unprotected, unlike the library's other host callbacks | The library's convention is not to pcall host callbacks. Core.lua:675 says so, and dd.onSelect at Widgets.lua:171 is called unprotected. Only tooltipPlace is pcall'd, because it has a defined fallback. A raising provider reaches geterrorhandler() with a stack trace that names the host's function, so wrapping it would only hide host bugs. |

### dev-copilot (2)

| Finding | Verdict | Cluster | Title | Reason |
|---|---|---|---|---|
| DC-A-04 | refuted | C04 | Executable-content re-read recorded only in DEPENDENCIES.md (derived from DC-01) | documentation-§8 asks for the re-read outcome to be recorded but names no location, and the Lua trigger has not fired because dev-copilot tracks no .lua files. DEPENDENCIES.md:84-95 already records the outcome explicitly: Lua, luacheck and lizard are not used here, and the Python and shell scripts are on no complexity gate. The rule is met. |
| DC-A-12 | no | C32 | Feature-branch workflow departs from versioning-git trunk-based MUST with no register row | The facts are accurate: dev-copilot/CLAUDE.md:111 makes feature branches the default, and the repo has no Documented deviations register. But the finding is derived from DC-A-16 rather than an independent defect, and owner-directed cross-repo branches already fall under the rule's 'human explicitly asks' clause. Once the upstream revision lands, CLAUDE.md:111 complies with no local change. Only if the owner rejects DC-A-16 would a deviation row, which depends on DC-02, be needed. |

### AbsorbTracker (6)

| Finding | Verdict | Cluster | Title | Reason |
|---|---|---|---|---|
| AT-A-10 | no | C02 | Newest automated-test bundle is unsighted and 57 commits behind | The bundle is 57 commits behind and unsighted, but automated-tests-§4 (line 295) and §6 expect staleness between releases. Max CCN is 14 and no threshold is crossed. |
| AT-A-11 | no | C01 | RESULTS.md names retired /wow-addon:bump-version | RESULTS.md is regenerated whole by the vendored runner, and kit 37 no longer emits the retired name, so the next automated-tests run clears it. Hand-editing a generated file is wrong. |
| AT-A-12 | refuted | C13 | Issue #26 (Widgets declined) is stale | I checked this myself. #26 already has a 2026-09-24 AT-DOCS comment that limits the decline to the Widgets Dropdown and records that the DragHandle is adopted (modules/Bar.lua:15, :126-129). The staleness the finding describes is already annotated. |
| AT-A-13 | no | C07 | test-cases.md Totals 877 vs README badge 876/876 | Audit-side duplicate of AT-R-07 in the same repo. Cleared by the same re-vendor, so it needs no separate item. |
| AT-A-16 | no | C15 | Unreachable 'Debug console unavailable' fallback arms | DebugLogSetup always publishes NS.DebugLog (stub or live) with Toggle and RunDiagnostics, so the 'Debug console unavailable' arms in settings/Slash.lua are dead. They are harmless defensive code, and the auditor already marked them not filed. |
| AT-A-17 | refuted | C13 | Open feature backlog: eight triaged enhancement issues | The eight open enhancements are correctly labelled state:triaged. That is a normal backlog, no rule is violated, and the finding's own remediation is 'None'. |

### AuraMaster (1)

| Finding | Verdict | Cluster | Title | Reason |
|---|---|---|---|---|
| AM-A-10 | no | C36 | Recorded deviation: unit-scoped container keeps previous unit's class until re-apply after a deferred swap | This is a ratified deviation (2026-09-12). The cited options-ui-§17 clause still exists, AM-03 resolves, CM.MustDefer() still holds applies, and neither re-open trigger has fired. It is correctly excluded from the tally. |

### BankLedger (5)

| Finding | Verdict | Cluster | Title | Reason |
|---|---|---|---|---|
| BL-A-06 | no | C17 | modules/Browser.lua at 1427 lines, 73 under cap (advisory, tracked) | This is the same file and fact as BL-R-02, and the numbers are correct (1427 lines, +206 since 1221). Its named seam (skin/close factory plus geometry) is outdated, because B:ApplySkin already delegates to Core.ApplySkin, so that seam would move only about 100 lines. The growth is the per-tab view machinery. It is merged into BL-R-02. |
| BL-A-07 | no | C02 | Newest automated-tests bundle 67 commits stale and predates kit 35 (no sighted measurement) | 67 commits stale, which is expected between releases (§4/§6). The CCN-16 function is tracked separately as F-001, and the header text is fixed in the current runner. |
| BL-A-08 | no | C10 | docs/ARCHITECTURE.md hub is 464 lines vs ~400 SHOULD | 464 lines, but no mandated section breaches the spill. The weight is in the non-mandated sections 'The stand-down' (74) and Launcher (61). Profiles (the suggested move) is already a summary plus one link to profiles.md. Moving text for the number alone would be churn. |
| BL-R-06 | no | C37 | Login backfill always spends its 40-id budget on oldest ids; unresolvable ids could starve it | Confirmed. Backfill.Collect walks oldest-first and caps at BACKFILL_MAX_IDS = 40, and unresolvable ids are never marked, so they are retried first on every login. Starvation needs 40 or more distinct unresolvable ids. Retention, which is account-wide in db.global (retentionDays = 30, not a profile setting), ages them out, except when retention is set to Always. The case is theoretical and has never been observed. |
| BL-R-07 | no | C02 | Committed complexity record describes a tree 67 commits old | Duplicate of BL-A-07. The live problems it mentions (F-001, Browser.lua size) are tracked under their own findings, and the record is regenerated at release. |

### ConsumableMaster (3)

| Finding | Verdict | Cluster | Title | Reason |
|---|---|---|---|---|
| CM-A-06 | refuted | C18 | Three bare §N section references remain in authored files | I checked all three sites. Each continues a qualified citation in the same parenthetical, for example '(debug-logging-§8's deferred work, §9's quiet steady state)' and '(debug-logging-§8/§9, DL-CM-02)'. They resolve at once, and the standard uses the same form itself. |
| CM-A-08 | no | C02 | Automated-test record is 59 commits behind HEAD and its newest run is unsighted | Today's sighted run is clean (0 warnings, max CCN 15). The band dispositions and the header refresh happen at the next release run by rule. |
| CM-A-09 | refuted | C24 | Host keeps its own debug change gate KCM.DebugQuiet (reasoned, cleared on Clear) | This is not a deviation. debug-logging-§9 allows a host gate as long as it re-arms from onClear. KCM.DebugQuiet is reset in onClear (core/DebugLogSetup.lua:258-259) and on enable, and its reason (counting held passes) is documented. The finding itself says no local change is owed. A counting DebugChanged in LibKa0s would serve one consumer, so it is speculative. |

### KickCD (3)

| Finding | Verdict | Cluster | Title | Reason |
|---|---|---|---|---|
| KC-A-05 | no | C02 | Automated-test record 81 commits behind HEAD and not sighted | 81 commits stale, but today's sighted run passes with 0 warnings and max CCN 15. The release is the checkpoint. |
| KC-R-06 | no | C39 | CONFIG_CHANGED{general} rebuilds Cooldowns on scale/alpha slider ticks and grid drags | Accurate: section 'general' (master rows, grid drag-stop, and the panel move at Panel_Render.lua:484) triggers a Cooldowns rebuild. But it is config-time only, throttled and unmeasured, and narrowing it risks the 'enabled' rebuild path. That is not worth it without a perf-analysis capture showing hitches. |
| KC-R-07 | no | C39 | New default spell lists never reach existing profiles | Real latent design gap, but no profile is affected: no spec has been added to defaults/Spells.lua since launch. The finding itself recommends deferring until a trigger fires. |

### LootHistory (2)

| Finding | Verdict | Cluster | Title | Reason |
|---|---|---|---|---|
| LH-A-14 | refuted | C40 | Landing-page logo path hand-types the addon folder name | library-stack-§8 binds arguments passed to the LibKa0s-Media seam, not the addon's own landing-page art path, so no rule is breached. Renaming the folder would break SavedVariables anyway. |
| LH-R-07 | no | C40 | Reconciler coalescing map (self.recent) never pruned during a session | R.recent grows with the number of distinct coalescing keys per session, not with event count, and is cleared on DisableCapture or reload. The memory involved is negligible. |

### MultiMeters (2)

| Finding | Verdict | Cluster | Title | Reason |
|---|---|---|---|---|
| MM-A-10 | no | C02 | Newest automated-test record is unsighted and 53 commits behind HEAD (Info, recurs) | The sighted run is clean and the band set is unchanged. The record lags by design until the next release. |
| MM-R-09 | refuted | C21 | Vehicle event pair registered for every unit and filtered to the player in Lua | The facts are accurate, but nothing is wrong. events-frames-taint makes the private RegisterUnitEvent frame a MAY, docs/midnight-quirks.md and the code comments at core/MultiMeters.lua:155-159 document the choice as deliberate, the events are rare, and the reviewer recommends deferring too. Switching would add a frame that needs slash-commands-§7 teardown and mock coverage, with no measured benefit. |

### PanelMaster (2)

| Finding | Verdict | Cluster | Title | Reason |
|---|---|---|---|---|
| PM-A-05 | refuted | C31 | LibDBIcon minimapPos not named under Settings Schema | ARCHITECTURE.md ## Settings Schema summarizes and spills into docs/schema.md, which documentation-§3 sanctions. Settings Schema already mentions LibDBIcon's minimap table, and schema.md:22 and :38-42 name global.minimap.minimapPos, its owner core/LauncherSetup.lua and its writer LibDBIcon on button drag. The claim that it appears 'only in the launcher table' is false. |
| PM-A-13 | no | C02 | Automated-test record 52 commits stale; tests/test_slash.lua entered 1000-1500 band | Info observation with nothing over a threshold. The test_slash.lua disposition goes in the next release run's ANALYSIS.md. |

### PartyFrameEnhanced (4)

| Finding | Verdict | Cluster | Title | Reason |
|---|---|---|---|---|
| PFE-A-08 | refuted | C24 | runDebug hand-routes debug verbs instead of NS.DebugLog:DebugVerb | settings/Slash.lua:243-254 implements the required behavior in the correct order (diagnostics first, then on/off through SetEnabled, then Toggle). The standard and the library both say DebugVerb is optional and that the behavior is what is required, not the call. The stub carries DebugVerb (core/DebugLogSetup.lua:71), so a swap would be safe, but it is cosmetic dedup only. |
| PFE-A-09 | no | C18 | Retired-notation sweep: 18 hits, all citing the addon's own design spec | This is an observation with no defect. Every hit cites the addon's own design and test-mode specs, which documentation-§6 does not govern, and none is malformed or out of range. |
| PFE-A-10 | no | C02 | Newest automated-test record is 47 commits behind HEAD and predates the sighted complexity suite | No threshold crossed (max CCN 14, 0 band files). The record is refreshed at the next release. |
| PFE-R-06 | no | C21 | Per-pass string and closure building on the driver and in-combat anchor paths (unverified) | The driver-string half is refuted. Lua interns the short strings Driver builds, and ApplyDriver (UnitButtons.lua:58) returns early when __driverWant == driver, so an unchanged driver allocates no closure or key. What remains is one closure per in-combat secure Anchor.Apply (Anchor.lua:228). That path is rare and runs only on combat transitions, so caching it is not worth a perf scenario or extra state on secure code. |

### PrettyChat (4)

| Finding | Verdict | Cluster | Title | Reason |
|---|---|---|---|---|
| PC-A-04 | no | C02 | Automated-test record is 49 commits behind HEAD and predates the sighted complexity gate (carried) | Clean sighted run. listSettings at CCN 15 is within the limit. Refresh at the next release run, and the listSettings peel stays optional. |
| PC-R-09 | refuted | C16 | listSettings is at the CCN 15 cap | listSettings measures exactly CCN 15. The gate fires only above 15, and nothing else in PrettyChat breaches it. Refactoring now would just move a number (#52). The reviewer's own verdict was no action. |
| PC-R-12 | refuted | C28 | Combat watcher is a named global frame | No standard rule forbids named frames. PrettyChat embeds no AceEvent, so its lazy combat watcher is within the §1 boundary-watcher carve-out. The prefixed global name is deliberate and helps with /etrace, and the reviewer's own verdict was no change. |
| PC-R-13 | no | C44 | Version literal duplicated outside the TOC | The "1.6.0" fallback in Namespace.lua:8 is used only when NS.Meta returns nil, which never happens in the client. It agrees with the TOC today, and bump-version already updates code constants. A pinning test would only add churn to every version bump. |

### WhatGroup (1)

| Finding | Verdict | Cluster | Title | Reason |
|---|---|---|---|---|
| WG-A-04 | no | C02 | Automated-test record is 50 commits behind HEAD and has never recorded a sighted complexity run (carried) | Info only, with no release since 1.5.0 and a clean sighted run. The test_libka0s.lua band disposition is a release-run duty. |
