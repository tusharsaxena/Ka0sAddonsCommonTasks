# 00 — Overview

**Consolidated spec and plan for the Ka0s World of Warcraft addon collection.**

Produced 2026-09-07. Nothing in this directory has been executed.

---

## NOTHING HERE HAS BEEN RUN

Read this before anything else, because the six documents that follow are written in the imperative and
will read like a changelog if you skim them.

- **No addon, library, standard or plugin repository has been modified.** All thirteen repositories under
  `/mnt/d/Profile/Users/Tushar/Documents/GIT/` were read-only for the whole of this exercise. The only
  files created anywhere are the seven you are reading.
- **No commit, branch, tag, push, merge or file edit exists outside this directory.** No `v1.26.0`, no
  `v1.27.0`, no standards version bump, no re-vendor, no `.pkgmeta` line, no test.
- **Every one of the 106 work items in `04_EXECUTION_PLAN.md` is unstarted.** The verification commands
  are written so the owner can run them; not one has been run as part of applying a change. The five
  decisions below have been **taken**, and taking a decision changed this bundle's text and nothing else.
- **Every step in `06_SMOKE_TESTS.md` is unperformed.** No client was launched.
- **Milestone 1 is approved and unstarted.** Decisions 1 and 2 were taken as recommended on
  2026-09-07, so the two LibKa0s tags and the fifteen standards amendments have the owner's word. That
  is permission to begin, not evidence that anything began: no upstream repository has been touched.

Where a suite figure appears below — test counts, `lizard` numbers, lint results, line-ending counts —
it was **observed** by re-running the suite during the triage passes that fed this consolidation.
Observing a suite is not changing a repository.

---

## What this is

Ten repositories were each independently reviewed and audited on 2026-09-07, producing twenty frozen
bundles. Every bundle was then re-read against the code by a separate pass that re-ran the suites,
re-opened every cited `file:line`, and re-graded severity by reachable impact rather than by the strength
of the rule broken. The survivors were clustered across the whole collection, and four cross-cutting
lenses were run over the set held as one thing.

This directory is what came out: one finding ledger, one upstream change set, one spec, one plan, one
traceability proof and one in-client checklist, across the whole collection.

| File | What it is |
|---|---|
| `00_OVERVIEW.md` | This. The map, the scope, the state of every repository, and the five decisions as taken. |
| `01_CONSOLIDATED_FINDINGS.md` | All 207 surviving findings, grouped by cluster then repo, with evidence and rule reference. Plus the 24 that triage rejected and why, the claims corrected against the code, and the verified-clean negatives. |
| `02_UPSTREAM_CHANGES.md` | Milestone 1 — every change to LibKa0s, WowAddonStandards and the `wow-addon` plugin, with the findings each unblocks and the adoption cost it creates. |
| `03_SPEC.md` | The normative end state per cluster: target shape, acceptance criteria, explicit non-goals. Not a schedule. |
| `04_EXECUTION_PLAN.md` | Five milestones, 106 ordered work items — id, repo, change, verification command, dependencies, effort. Plus the branch name, the merge order, and where the record goes. No dates. |
| `05_TRACEABILITY.md` | Every finding → cluster → milestone → work item, the coverage proof, **the seven findings that had no work item**, and four defects the proof found in the plan itself. |
| `06_SMOKE_TESTS.md` | The in-client checklist: everything no out-of-game suite can reach, grouped by milestone, each with an observable pass condition. |
| *(`07_EXECUTION_RECORD.md`)* | **Does not exist yet, and must not.** It is written after the work, against measured state, the way every prior bundle in this directory did — see `04_EXECUTION_PLAN.md` § *Branches, merge order, and where the record goes*. |

---

## Scope

### The roster — nine addons and one library

`WowAddonStandards/standards/ADDONS.md:19-27` names nine in-scope addons, and `:38` names one Ka0s-owned
library repository. All ten were reviewed and audited:

**AbsorbTracker · BankLedger · ConsumableMaster · KickCD · LootHistory · MultiMeters · PanelMaster ·
PrettyChat · WhatGroup**, plus **LibKa0s**.

**`WhoGotLoots` and `BuffTextNotifications` sit in the same parent directory and are deliberately
excluded.** They are not Ka0s addons: neither appears in `ADDONS.md`, neither vendors LibKa0s, and
neither is governed by the standard. They were not read, not measured and are not counted in any figure
in this bundle.

### Three repositories this plan changes but nobody audited

`WowAddonStandards`, `wow-addon` and `Ka0sAddonsCommonTasks` received **neither a review nor an audit**
on 2026-09-07. A `find` over all three returns no `reviews/`, no `audits/` and no `docs/automated-tests/`
directory of any date.

That matters more than it looks, and it is a finding in its own right. `WowAddonStandards` is the
normative source every audit finding cites, and two clusters (`C16`, `C25`) plus `LIBKA0S-R-15` and
`LIBKA0S-A-14` are filed *against* it with no audited baseline for the repository receiving the work.
`wow-addon/agents/review.md` (321 lines) and `WowAddonStandards/AUDIT.md` (515 lines) drove all twenty of
this cycle's passes, so a defect in either was reproduced twenty times and reviewed zero times. Both are
docs-only, which is presumably why they were skipped. `M1-WA-06` puts **two** of the three in the
rotation. The third, `Ka0sAddonsCommonTasks`, is deliberately left out and the reason is stated in the
item: it holds a README and a tree of frozen planning bundles — no Lua, no TOC, no `libs/`, no suites —
so the audit checklist has nothing to bind to and would manufacture findings, which is the failure
`library-stack-§7` names for auditing a library against the addon rule set.

### Out of scope

- Anything requiring a client. Every step in `06_SMOKE_TESTS.md` is written as an instruction to an
  operator, never as a claim that it passed.
- The frozen bundle contents under `docs/audits/`, `docs/reviews/`, `docs/automated-tests/` and
  `docs/perf-analysis/` in each repository. They are dated evidence and are never rewritten — including
  the 35 bundles that carry no `ANALYSIS.md`, which `M5-01` fixes forward rather than backfilling.
- **Any addon version bump — decided, not merely proposed.** This plan cuts two LibKa0s tags and one
  standards version, and nothing else. Decision 5 settled it: this is a review-and-audit fix pass, so no
  TOC version, README badge, "What's new" roll or `/wow-addon:bump-version` run happens in any of the
  nine. **The consequence is worth stating rather than inferring: no addon release means no player
  receives anything this plan fixes until a release is cut separately**, which is next cycle's call.
- Splitting any file for the 1500-line cap, and flipping the shared mock's `GetHeight`. Both are argued
  and declined in `04_EXECUTION_PLAN.md` § *What this plan deliberately does not do*.

---

## The state of every repository, as observed today

Read-only `git` only. Every addon and LibKa0s shows the same two untracked paths — the 2026-09-07 review
and audit bundles this consolidation consumed — and no other working-tree change.

| Repo | Branch | HEAD | Working tree | Latest tag |
|---|---|---|---|---|
| AbsorbTracker | `master` | `686cae5`, 2026-09-03 | the two 2026-09-07 bundles, untracked | `1.9.0-release` |
| BankLedger | `master` | `0aec078`, 2026-09-03 | as above | `1.0.0-release` |
| ConsumableMaster | `master` | `69a4d56`, 2026-09-03 | as above | `1.5.0-release` |
| KickCD | `master` | `1dca167`, 2026-09-03 | as above | `1.2.1-release` |
| LootHistory | `master` | `6d3c2de`, 2026-09-03 | as above | `1.2.0-release` |
| **MultiMeters** | `master` | **`81642e6`, 2026-09-07** | `docs/audits/` and `docs/reviews/` untracked **in whole** — this repo has never committed a bundle of either kind | **none** |
| PanelMaster | `master` | `c5b4159`, 2026-09-03 | the two 2026-09-07 bundles, untracked | `1.0.0-release` |
| PrettyChat | `master` | `6469f88`, 2026-09-03 | as above | `1.4.0-release` |
| WhatGroup | `master` | `9b35a23`, 2026-09-03 | as above | `1.3.0-release` |
| LibKa0s | `master` | `4eacebe`, 2026-09-03 | as above | **`v1.25.0`** |
| WowAddonStandards | `master` | `03a9aa0`, 2026-09-03 | clean | none (version is `STANDARDS.md:1`, **v2.38.0**, 2026-09-02) |
| wow-addon | `master` | `2258f1b`, 2026-08-25 | clean | none |
| Ka0sAddonsCommonTasks | `main` | `ce572a3`, 2026-09-03 | this directory, untracked | none |

### MultiMeters was reviewed with an uncommitted working tree

Stated plainly because it is the one place in this cycle where the evidence and the tree could have
diverged. MultiMeters' review pass opened on a tree the task brief described as ten modified files.
**Partway through that session those files were committed by someone else** as
`81642e6 "Measure why the feign filter misses party members, before fixing it"`, dated today. The pass
records this itself at `MultiMeters/docs/reviews/2026-09-07/01_FINDINGS.md:13-18`.

Every MultiMeters finding was formed against that content and every line number cites it. The perf
baseline in `MULTIMETERS-R-01` is `0e74319`, the commit immediately before, which is the correct
before-arm. The triage pass re-ran all three suites at `81642e6` and reproduced both bundles' numbers
exactly.

The practical consequence: **`C04`, the feign-trace cluster, sits on top of a commit made the same day
that was itself a measurement of the same bug.** M2 Lane C should be read against `81642e6`, not against
the 2026-09-03 state the other eight addons are in.

### The four suites, all ten repositories, re-run during triage

| Repo | lint | tests | perf | complexity |
|---|---|---|---|---|
| AbsorbTracker | 0/0, 27 files | 547 | 6 scenarios, `probeOverheadOff` 48.0 B/iter | 0 warnings, max CCN 15, 8903 NLOC |
| BankLedger | 0/0, 28 files | 831 | no `tests/perf.lua` | 0 warnings, four functions at CCN 15, 14174 NLOC |
| ConsumableMaster | 0/0, 59 files | 749 | present | 0 warnings, max CCN 15, 17632 NLOC |
| KickCD | 0/0, 36 files | 841 | present | **1 warning — CCN 18 at `tests/test_schema.lua:595`**, 17109 NLOC |
| LootHistory | 0/0, 28 files | 699 | no `tests/perf.lua` | 0 warnings, max CCN 15, 13222 NLOC |
| MultiMeters | 0/0, 45 files | 1496 | 13 scenarios, exit 0 | **23 warnings, max CCN 36** at `scanColumn`, `modules/Aggregator.lua:1439-1540`; 31773 NLOC |
| PanelMaster | 0/0, 27 files | 763 | no `tests/perf.lua` | 0 warnings, 12122 NLOC |
| PrettyChat | 0/0, 18 files | 300 | no `tests/perf.lua` | 0 warnings, 52211 NLOC (`GlobalStrings` dominates) |
| WhatGroup | 0/0, 16 files | 528 | no `tests/perf.lua` | 0 warnings, 7047 NLOC |
| LibKa0s | 0/0, 18 files | 764, 22 suites | not applicable | 0 warnings, max CCN 14, 13678 NLOC |

**7,518 headless cases pass and nothing is red.** Lint is 0/0 in all ten. Nothing in this plan unblocks a
broken build.

**Two of the ten carry complexity warnings, and `automated-tests-§3`'s release gate is
`suites.complexity.warnings == 0`.** MultiMeters has 23, topping out at CCN 36 in `scanColumn`; KickCD
has one, the anonymous function at `tests/test_schema.lua:595-631` — 29 NLOC, CCN 18, whose own comment
at `:613` names the seam to split on. **Neither repository can cut a tag while they stand.** As first
drafted, no work item in this plan cleared either: MultiMeters' was filed only as a stale watch list
(`MULTIMETERS-R-05`, which `M5-01` corrects without reducing the count) and KickCD's was `KICKCD-R-02`,
one of the eight unmapped findings. Both now have one. `M4-25` splits KickCD's on the seam its own
comment names, taking that repository to zero. `M4-26` writes a disposition for every one of MultiMeters'
23 — split, accepted with a register row, or an open issue naming the seam — which is the most that can
be done without splitting shipped source this plan is not splitting, and it is what `M5-01`'s
"every watch-list entry carries a disposition" needs to have something to resolve against. See
`05_TRACEABILITY.md` § 3b.

### MultiMeters is the repository every risk signal points at

Stated as a risk in its own right, because the plan schedules it as a peer of BankLedger and the numbers
do not support that. It is the largest addon at 31,773 NLOC, roughly twice the next. It is the only
repository whose `docs/audits/` and `docs/reviews/` are untracked **in whole**. It is the only addon that
has never been tagged. It was reviewed on a tree committed mid-session. It holds **all 23** of the
collection's shipped-source complexity warnings, topping out at CCN 36. It carries 13 open GitHub issues,
four of them `severity:high` and untriaged. And it does not appear in the eleven-repo commit table of the
2026-08-05 remediation cycle at all. Against that, 22 findings over 31,773 NLOC is the **lowest** finding
density in the collection — 0.69 per kNLOC against WhatGroup's 3.55 over 7,047 — and a low density here
is not evidence of health; it is evidence that this is the repository twenty passes had the least
purchase on. M2 Lane C, `M4-26` and `M5-01` are what this plan does about it, and they may not be enough.

Two figures a reader should not take from the committed record: every repository's `RESULTS.md` newest
row is behind its tree by one to eight runs (that is `C08`, 25 findings), and `git ls-files --eol` in all
ten disagrees with the declared CRLF pin (that is `C10`, 12 findings, including two files inside
LibKa0s's own **shipped** payload).

---

## How this was produced

1. **Twenty independent passes, 2026-09-07.** `/wow-addon:review` and `/wow-addon:standards-audit` were
   run in each of the ten repositories, writing frozen bundles to `docs/reviews/2026-09-07/` and
   `docs/audits/2026-09-07/`. Each re-ran that repository's own four suites first, so every finding rests
   on today's numbers rather than the committed record's.
2. **A per-repo adversarial triage pass.** For each repository, a separate pass re-ran `luacheck .`,
   `lua tests/run.lua`, `tests/perf.lua` where it exists and `lizard`; re-opened every cited `file:line`;
   reproduced what could be reproduced by execution; and re-graded severity by reachable impact. It
   dropped **24 bundle items** whose evidence did not survive, corrected the claims of several more while
   keeping the finding, and recorded fix directions that are wrong as written. All of that is
   `01_CONSOLIDATED_FINDINGS.md` Part 3.
3. **A collection-wide clustering pass** over the 207 survivors, attributing each cluster's root cause to
   the repository that can actually fix it. It produced 39 clusters — 31 from the per-repo findings and
   **8 `CX*` clusters that only exist from the collection view**, two of which (`CX01`, `CX02`) carry no
   per-repo finding at all because no single-repo pass was positioned to state them.
4. **Four cross-cutting lenses**, each holding all ten repositories at once: LibKa0s upstream; standards
   and plugin upstream; sequencing, risk and dependencies; and completeness — what twenty passes did not
   surface. Between them they reversed two cluster dispositions, corrected three census counts — and got
   a fourth wrong in the same way, `CX08`'s, where the ledger's figure was right and the correction
   counted a generated tree and nine vendored copies of one payload. That is recorded under
   *Critique and disposition* below and is `M1-WA-02`'s reason for existing.

### The evidence rule

Every claim in these seven documents resolves to a `file:line` in a named repository or to a named bundle
artifact. Where a bundle's own claim did not survive re-checking, the finding carries the correction
rather than being dropped silently. Where a bundle's prescribed *fix* is wrong, it is recorded as a
do-not-execute — there are several, and `LIBKA0S-A-08`'s `minimise` rename is the sharpest: `lib.Icon`
builds the file path *from* the catalog key, and `minimise.tga` is the file on disk in ten vendored
trees, so adding `"minimize"` to `lib.ICONS` alone yields a path to nothing.

Counts are written with their members named, per the house rule. Where a count moved in triage, both
numbers appear.

---

## Headline numbers

| | |
|---|---|
| Repositories reviewed and audited | **10** |
| Bundles consumed | **20** (10 review + 10 audit) |
| Surviving triaged findings | **207** |
| Rejected in triage | **24** |
| Clusters | **39** — 31 per-repo, 8 collection-only |
| Milestones | **5** |
| Work items | **106** — 100 as first drafted, plus six from decision 4 |
| Findings mapped to a work item | **207** — 200 as first drafted, plus the seven decision 4 scheduled |
| **Findings with no work item** | **0** — see `05_TRACEABILITY.md` § 3 |
| LibKa0s tags this plan cuts | **2** (`v1.26.0`, `v1.27.0`) |
| **Addon releases this plan cuts** | **0** — see decision 5 |
| Standards sections amended | **15**, plus one version rollup |
| Open GitHub issues reconciled against this bundle | **91**, at `M2-23` |
| In-client sessions | **6** — about seventy-five minutes for the plan's five, plus a locale pass |

### Severity, after triage

| Severity | Count | What it is |
|---|---|---|
| **Critical** | **1** | `LIBKA0S-A-01`. Three lines in `OptionsCompose.lua` wrap a closure that is already a closure, so every composed font, border and bar-texture dropdown yields an empty list. |
| **High** | **5** | `BANKLEDGER-R-02` and the migration seam; `KICKCD-R-01`, the process-global widget registry; `MULTIMETERS-R-01`, a disarmed diagnostic that allocates anyway; `PRETTYCHAT-R-01` and `-R-02`, an unchecked chat format and a texture that rides a shared pool. |
| **Medium** | **25** | Led by the feign-trace subsystem (4 of `C04`), the settings-panel shape group, and the record integrity gaps. |
| **Low** | **176** | Developer-facing, config-only, or unreachable in any shipping configuration. |
| **Total** | **207** | |

`1 + 5 + 25 + 176 = 207` ✓

### The shape of the answer, in one paragraph

207 findings describe roughly 39 distinct problems, and three clusters — `C08` (25), `C19` (13) and
`C10` (12) — account for a quarter of the count while changing no shipped behaviour at all. The one
Critical is a three-line library edit whose blast radius is one addon: `C01`'s defect is in the shipped
payload of all nine consumers, but three of the four addons that use the composers each independently
wrote a private workaround, so **KickCD alone ships empty dropdowns today**. Fixing it upstream and
re-vendoring KickCD is the whole of Milestone 3's payload, and because `OptionsCompose.lua:32-35`
resolves the highest compose minor present in the session, that one re-vendor repairs every consumer in
a live client — the wave does not have to be atomic. Milestone 2 holds every reachable defect in the
collection and depends on nothing; it can start the same hour this is approved.

---

## Read these first

**1 · `05_TRACEABILITY.md` § Part 3 and § Part 7 — eight pages in, and the only part of this bundle that
says the plan is wrong.** Seven findings have no work item. Four are specified in `03_SPEC.md` and
scheduled nowhere — and three of those four are acceptance criteria § `C30` states in its own text, which
is a worse failure than forgetting them; three are in neither document. An eighth, `KICKCD-R-02`, left
that list and became `M4-25` once it was measured against the release gate it blocks. The second defect
that part records — `02_UPSTREAM_CHANGES.md` and `04_EXECUTION_PLAN.md` **using different `M1-LK` numbers
for eleven of the sixteen LibKa0s items** — **has since been repaired**, and § 7a now carries the
crosswalk as the record of what moved rather than as work outstanding. An item id is unambiguous across
this bundle without naming the document it came from.

**2 · `02_UPSTREAM_CHANGES.md` § `M1-LK-01` and `04_EXECUTION_PLAN.md` § `M3-02` — the one change in this
plan that can break something silently.** The composed-media fix moves `__AttachCompose` from calling a
host's `LSMValues` at render time to calling it once at row-declaration time. MultiMeters supplies a
table-returner at `settings/Schema.lua:670`. Post-fix its rows take a media list frozen at file load: no
crash, no warning, no red test, and exactly the failure `Options.lua:759-763` says the deferral exists to
prevent, in as many words. The revert is non-optional and must be in the same commit as the re-vendor.

**3 · `04_EXECUTION_PLAN.md` § *What this plan deliberately does not do*.** **Eleven** things were
proposed by a finding or a cluster disposition, examined and declined: the `MakeCloseButton` rebind,
every 1500-line split, the `ANALYSIS.md` backfill, the `minimise` rename, annotating every TOC line,
turning on lint for 308 test files at once, flipping the shared mock's `GetHeight`, publishing a no-op
Options surface from LibKa0s, withdrawing any `performance-§12` exemption, shipping a `RESULTS.md` figure
by hand, and cutting any release beyond the two LibKa0s tags. Each is argued from measurement. If you
disagree with one, that is a decision to make now rather than a discovery to make in week three — and
`M5-07` files all eleven as `state:will-not-do` issues so next cycle does not re-argue them from
scratch.

**4 · The two reversed dispositions, `M1-STD-01` and `M1-STD-02`.** `CX05` as filed asks ten repositories
to violate `lint.md`'s own template, which all ten follow exactly. `CX04` as filed measures
`toc-file-§5:144`'s MUST against every line of nine TOC files when the MUST binds only load-bearing
positions — eight one-line additions across three files, not nine files of work. Between them the two
findings as triaged would have put roughly 320 files of work into ten repositories to satisfy readings
the standard's own text does not carry. Both are answered by amending the standard.

---

## The decisions, as taken

**All five were answered by the owner on 2026-09-07, and this bundle has been rewritten to match.**
Three were taken as recommended; **two were not**, and where the plan argued the other way that argument
is kept in place beside the decision rather than deleted — a plan that quietly erases the case it lost
teaches the next reader nothing.

| # | Decision | Taken as |
|---|---|---|
| 1 | Two LibKa0s tags, not one or seven | **As recommended.** No change to the plan. |
| 2 | Amend fifteen sections of the standard | **As recommended.** No change to the plan. |
| 3 | Start M2 in parallel with M1 | **Reversed — M2 waits for M1.** `04_EXECUTION_PLAN.md`'s milestone map and its M2 preamble now say so. |
| 4 | What to do about the seven unmapped findings | **Do all seven.** Six new work items; the plan now maps 207 of 207. |
| 5 | Does this cycle ship | **No addon release this cycle.** Upstream version bumps are authorised; addon version bumps are not. |

**Decision 3 is the one that costs something, and the plan's objection stands on the record.** M2 holds
every reachable defect in the collection and depends on nothing technically; the sequencing lens called
scheduling it behind M1 "the single most likely way this plan goes wrong". The owner decided it waits
anyway. `04_EXECUTION_PLAN.md` § *Milestone map* states the cost in full — the five High findings now sit
behind 38 upstream items, with `M1-LK-07` as the long pole — and states the upside the decision buys:
a serial order means no addon repository is opened by two lanes that do not know about each other.

**Decision 5 draws a line the rest of the bundle now respects.** This is a review-and-audit fix pass, not
a release. **No addon version bump, anywhere** — no TOC version, no README badge, no "What's new" roll,
no `/wow-addon:bump-version` run in any of the nine. Upstream versioning is explicitly authorised and
unchanged: LibKa0s cuts `v1.26.0` (`M1-LK-04`) and `v1.27.0` (`M1-LK-15`), and `WowAddonStandards` takes
its version rollup at `M1-STD-16`. The consequence the bundle already stated is unchanged and is now the
accepted position rather than an open question: **nothing here reaches a player this cycle.** KickCD's
eight media dropdowns stay empty in the live client until a release is cut, and cutting it is next
cycle's decision. `M4-25` and `M4-26` still run, because they remove the mechanical obstacle — the
`suites.complexity.warnings == 0` gate — so that next cycle's answer can be yes without a prerequisite
block in front of it.

The original framing of the ask is kept below, because the reasoning behind each option is what makes
the decision auditable later.

### The ask, as it was put

**Approve Milestone 1, or send it back.** Everything else follows from it, and it is the only part that
changes repositories every addon depends on.

Concretely, four things need your word before any work starts:

1. **Cut two LibKa0s tags rather than one or seven.** `v1.26.0` carries `C01`'s fix, its regression gate
   and the two LF files, and nothing else, because `C01` is a shipped player-facing break and should not
   wait on the kit. `v1.27.0` carries the rest. All nine consumers sit on `v1.25.0` today, and that flat
   baseline is what makes a multi-item release cheap; it will not survive a partial rollout.
2. **Amend fifteen sections of the standard.** Four of them resolve contradictions the standard has with
   itself — `standalone-windows.md:30` against `:34` (that file carries no numbered subsections, so the
   house rule in `01_CONSOLIDATED_FINDINGS.md` gives line numbers), `library-stack` §1 against §3,
   `line-endings` §4 against §5, and `automated-tests` §4 against `documentation` §3. Two reverse a triaged disposition.
   One is unsatisfiable as written and nine of nine repositories invented the same workaround for it.
3. **Start Milestone 2 immediately and in parallel with Milestone 1.** It has no upstream dependency at
   all, it holds every reachable defect, and scheduling it behind M1 is the single most likely way this
   plan goes wrong.
4. **Decide what to do about the seven unmapped findings** before M2 opens. Three are one-line edits in
   files M2 already opens, one needs a locale client (`M5-08` now schedules that client session), and one
   needs a ruling. All seven are filed as issues by `M5-07` either way, so the decision can be "not this
   cycle" without the rows evaporating.
5. **Decide whether this cycle ships, and to which addons.** This is the decision the first draft of this
   bundle did not ask for, and it is the one that decides whether anything above reaches a player.
   `03_SPEC.md` puts every addon release out of scope, so as written this plan ends at merged commits in
   thirteen repositories. Two things make the question answerable now rather than later: `M4-25` takes
   KickCD to zero complexity warnings and `M4-26` gives MultiMeters' 23 a disposition, so
   `automated-tests.md:143`'s release gate — `suites.complexity.warnings == 0` — stops being the reason
   the two most-affected repositories cannot cut a tag. If the answer is yes, the releases are a sixth
   milestone this plan does not contain and should be scoped as its own thing; if it is no, say so, and
   `00`'s closing paragraph below is the honest version of the urgency.

Nothing here is urgent in the sense of a broken build: all four suites are green in all ten repositories
and the collection is shipping. One thing is urgent in the sense of a player noticing: **KickCD's eight
media dropdowns are empty in the client right now.** `M1-LK-02` plus `M3-01` is the shortest path in this
bundle — three lines upstream, one re-vendor, no addon code — but it is a path to a **commit**, not to a
player. Nobody's dropdowns fill until KickCD cuts a release, and this plan cuts none. That was decision 5,
and it is the difference between this bundle being finished and this bundle being delivered.

---

## Critique and disposition

Two adversarial passes audited this bundle after it was written — one for internal consistency, one for
completeness — and between them raised 29 items: 18 consistency defects and 11 completeness gaps. Every
one was re-measured against the repositories before it was acted on. Twenty-three were right and the
documents changed. Five were wrong, or right about a sentence and wrong about the remedy, and one got a
fact about the issue store wrong; those six are recorded here rather than silently ignored, because a
critic being wrong is a fact about the bundle worth keeping — the next reader will have the same thought
and deserves the measurement that settles it.

**Read this section as a changelog with reasons, not as an apology.** Where a repair widened a claim it
is because the measurement supported a wider one.

### The four that changed the plan, not just its prose

**`M1-LK-00` was two files and the repository has seven.** `git ls-files --eol` in LibKa0s reports seven
tracked files at `w/lf` under `attr text=auto eol=crlf`, and the item repaired the two in the shipped
payload. `M1-LK-10` then widens `tests/test_eol.lua` to the whole tracked set — and that gate reads
working-tree bytes — so the remaining five would have turned the library's own suite red inside M1, with
the only sweep that clears them (`M4-10`) sitting behind the tag M1 has to cut. That is a cycle, and it
would have been discovered by an operator watching `lua tests/run.lua` go red with nothing in the plan to
run. `M1-LK-00` now names all seven. While there: `git add --renormalize` cannot repair any of this —
it rewrites an index that was already correct — so `M4-10`'s stated action was wrong in the same way and
now reads `rm` plus `git checkout --`, which is what the gate's own failure message tells you to run.

**`C08`'s mechanism was a ruling with no producer.** `M1-STD-07` said "make the generated half producible
by the runner" and no item gave the runner that capability. `testkit/run-automated-tests.sh:388-437`
writes one table row plus a fixed lead-in; `automated-tests.md:221-224` MUSTs a complexity watch list as
two tables and a standing section per suite. Twenty-two findings closed at `M5-01` on a mechanism that
did not exist. `M1-LK-07` now builds it, `M5-01` states which single column stays authored, and the item
grew from M to L.

**Ninety-one open GitHub issues were never reconciled.** The collection's tracking moved to GitHub issues;
this bundle referenced six of them. `LibKa0s#15` is this collection's Critical, filed, still
`state:untriaged`, and cited here only as the thing a ConsumableMaster comment points at. `M2-23` is the
reconciliation and `M5-07` files what this plan decided not to do, including all eleven declines, so they
outlive the directory.

**Nothing here reached a player, and the overview closed by implying it did.** Addon releases are out of
scope by an argued decision that stands — but "KickCD's dropdowns are empty right now" as the plan's one
urgency, next to a plan that ends at a merged commit, is a claim the scope does not support. The closing
paragraph now says so, and shipping is decision 5. The completeness pass asked for a sixth milestone;
that is declined below. What it *did* earn is `M4-25` and `M4-26`, which put the two repositories the
gate blocks in a position to pass it.

### The rest of what changed, in one list

Accepted, measured, and applied without further comment: the ⚠ index (`M2-11`, `M2-22`, `M3-02`,
`M4-01`, `M4-15`, `M4-16` were running in-client steps unmarked, and `M5-08` now owns session 6);
session 5's run count, which read two, three and six across three places and is now six everywhere, the
only reading consistent with the five deletion commits' stated purpose; five `layout.md` and
`packaging.md` citations pointing past the end of files of 75 and 32 lines, with the same facts cited
correctly elsewhere in this bundle; `C29`'s repo count, three in `01` against four in `03`, with a KickCD
finding sitting in its own table; `05`'s explanation of the coverage gap, which named `C30` and `C31` and
then evidenced `C31` and `C29`; `05`'s "every acceptance criterion in § `C30` unsatisfied", which is
three of five; `05`'s five-and-three arithmetic on the unmapped rows; `02`'s Group A and Group B closure
counts and its one contradictory `BANKLEDGER-A-02` claim; `02`'s claim that the vendored byte diff fails
in nine repositories, which is eight — PrettyChat's two copies match today and `M1-LK-00` is what starts
them diverging until `M3-05`; `04`'s five `Perf.lua` sites labelled `CANCELLED` when three carry
`unlabelled`, which the one in-client check written for them could not have seen; `OptionsWidgets.lua:694`
against an actual `:696`, in four documents; `PRETTYCHAT-A-07`'s count and its false `.tga`/`.ttf`
reason; `M2-09` and `M2-11` editing inside MultiMeters' three worst warned functions with no lizard
delta recorded; `M1-LK-03` rewriting a widget all nine addons render with no in-client check anywhere
(now § 3.5); the six in-client sessions living only in this frozen directory (every `Smoke, session N`
step now lands in the owning addon's `docs/smoke-tests.md` in the same commit); the missing locale
sections (`M5-08`); and the absent branch name, merge order and execution record, which every prior
bundle in this directory carried and which `04` now states.

### Where the critics were wrong

**`ABSORBTRACKER-A-01` should not be regraded to Low.** The consistency pass was right that the evidence
was false — `.superpowers` and `.claude` are gitignored and wholly untracked in AbsorbTracker, so the
"2.8M of **tracked** review diffs shipped to every player" line fails the exact test that rejected
`BANKLEDGER-A-03`, `MULTIMETERS-A-04` and `WHATGROUP-A-13`, and the directory is 60 files with 30
`review-*.diff`, not 62 mostly-diffs. All of that is corrected. The **grade** is not, because measuring
the repository turned up player bytes the audits missed entirely: `media/screenshots` is tracked in every
repository that has one and ignored in only four, so **KickCD ships 7.5M, LootHistory 5.9M, AbsorbTracker
2.0M and WhatGroup 880K — 16.3M of project-page art in every download.** Only `WHATGROUP-R-09` named it,
and only its own 880K. A Medium held on corrected evidence is not the same as a Medium held, and `C11`,
`M2-19` and § C11 of the spec now separate the shipped half from the present-but-untracked half in every
place they appear. The completeness pass's "only WhatGroup's 880K is real player bytes" under-measured by
a factor of eighteen.

**`CX08`'s "corrected" census was wrong, and the ledger's original 75 was right.** The consistency pass
called the figures unverifiable and proposed PrettyChat 1 / Buttons 11 / Tooltips 3. Measured: over
tracked `*.lua` excluding `libs/`, `tests/` and the generated `PrettyChat/GlobalStrings/` tree this plan
exempts by rule, the collection carries **75 lines holding 76 paths** — precisely the number the ledger
gave and the triage pass "corrected". The 93 counted 92 hits inside `GlobalStrings/`; the 246/138 chrome
pair was measured with `libs/` and `tests/` included, which is nine vendored copies of one Ace3 and
LibKa0s payload. So the fix went further than asked: `CX08` is restored to 75 with its command and scope
written beside it, in all four documents that carry it, and `M1-WA-02` now cites this as its own
strongest case — a second pass with no stated scope is not a check, it is a second guess.

**`PRETTYCHAT-A-07` is four files, but "restore it to 4" is not the whole repair.** The audit's four
reproduce; the triage narrowed the scope to "outside `libs/` and `tests/_kit/`", got two, and filed that
as a correction. Both numbers are true against their own scope. What was false is the stated *reason* —
"vendored `libs/` files and binary `.tga`/`.ttf` assets" — there are no binary hits at all, and the two
the narrowing dropped are `libs/LibKa0s/DebugLog.lua` and `Pool.lua`, Lua source in the **shipped**
payload and the only stragglers in that repository a player receives. The finding now carries four with
the scope split named, which is the fact that matters and which neither number alone conveys.

**A sixth milestone for addon releases is declined.** The completeness pass is right that nothing here
reaches a player and right that the overview implied otherwise, and both are fixed. But this plan's own
rule is that scope traces to a finding, and no finding asks for a release; inventing a milestone of
version bumps, changelog rolls and tag cuts across nine repositories — each of which runs
`/wow-addon:bump-version`'s full four-suite gate — would be the largest block in the bundle and the only
one with no evidence behind it. It is a decision for the owner, so it is asked as one. What the argument
did earn is the two items that remove the mechanical obstacle, and a decision list that no longer has
four items where it needed five.

**Verifying a standards amendment by grepping it for its own keyword is weak, and re-running a full audit
per item is not the fix.** The completeness pass is right that fifteen of sixteen Group B items go green
the instant a token is typed. Its proposed remedy — a fresh `/wow-addon:standards-audit` against a named
repository per item — is sixteen audit runs to verify sixteen documentation edits, and `M5-06` already
runs exactly that across all ten repositories once the standard is rolled. What the group lacked was an
honest statement of what its greps prove, plus a requirement with teeth: every amendment must now state,
in its own text, the repository and `file:line` the old wording got wrong. That is checkable by reading,
which a keyword grep is not, and it makes `M5-06` the real gate rather than a formality.

**One smaller correction to the consistency pass, for the record.** It reported the C29 cluster's repo
count, the ⚠ index, the session-5 cadence, the two `layout.md`/`packaging.md` citation clusters, the
`Options.lua:757-761` range, the "nine declines" undercount, the `standalone-windows` §-for-line notation,
`05`'s five-and-three arithmetic, `02`'s closure counts and the `M1-LK-02`/`M1-LK-01` numbering collision
— **all ten reproduce exactly, and all ten are fixed.** Its `KICKCD-R-02` characterisation of KickCD #7 as
`state:untriaged` is the one factual slip: that issue is `state:triaged`, and KickCD #8 is the other
`severity:high` row. Neither changes anything the pass concluded.

### What is still open, and deliberately

Nothing in Part 7 is now outstanding. The `M1-LK` renumbering — the one item this section previously
held open — was applied on 2026-09-07 as a single mechanical pass over `02_UPSTREAM_CHANGES.md` against
§ 7a's crosswalk, and the two documents now name the same sixteen items by the same ids. What moved is
recorded in § 7a and summarised under *The renumbering pass* below.

Four of the seven unmapped findings are one-line edits the plan could simply have absorbed. They are not
absorbed, because `00_OVERVIEW.md` asks the owner to decide about them and scheduling them here would
quietly answer a question that was put deliberately. `M5-07` files all seven, so the decision can be
deferred without the rows being lost.

### The renumbering pass

Applied 2026-09-07, after the critique above and before anything else. `04_EXECUTION_PLAN.md` is the
canonical numbering because it is the plan and the superset; `02_UPSTREAM_CHANGES.md` was rewritten onto
it. **No document other than `02_UPSTREAM_CHANGES.md` changed an id**, because § 7d had already moved the
one citation in `03_SPEC.md` and every other document was written in `04`'s numbering from the start.

What the pass did, all of it against § 7a's crosswalk table:

- **Renumbered all 83 `M1-LK` references** in `02_UPSTREAM_CHANGES.md` — item headings and every
  cross-reference, including the ASCII dependency tree and the ordering-constraint arrows.
- **Split `02`'s `M1-LK-11`** — the one item the two documents did not merely number differently but
  *divided* differently — into `M1-LK-12` (the `.luacheckrc` narrowing, which exists separately because
  it is the pilot `M1-STD-01` and `M4-11` depend on) and `M1-LK-13` (the printer, the bracket slots, the
  `C_SpecializationInfo` rung and one comment). `C24`'s closure now names both.
- **Gave the two tag cuts their ids.** `M1-LK-04` cuts v1.26.0 and `M1-LK-15` cuts v1.27.0. They were
  prose in `02`'s *Group A tags* section and items in `04`; they are now items in both, which is what
  takes Group A from 15 to **16** and makes the at-a-glance table agree with the milestone map.
- **Reordered Group A's sections into ascending id order**, so the document reads 00 … 14 top to bottom
  with the two tag cuts in the section that explains them.
- **Corrected the range and shorthand expressions the mapping breaks.** A range is not remappable
  member-by-member: `M1-LK-04 … M1-LK-12` for v1.27.0 became `M1-LK-05 … M1-LK-14`, cut by `M1-LK-15`,
  and the `` `M1-LK-01`, `-05`, `-06`, `-07` `` shorthand became `` `-02`, `-05`, `-07`, `-08` ``. These
  are where a mechanical pass would have silently produced a wrong document, and they were done by hand.
- **Renumbered the two adoption milestones.** `02`'s *Milestone 2* and *Milestone 3* are `04`'s **M3**
  and **M4**, because M2 is the block of defects that needs no upstream anything. A reader carrying
  "Milestone 2" between the documents was scheduling the re-vendor wave where the SavedVariables
  migrations belong.

**Verification.** The set of distinct `M1-LK` ids in `02_UPSTREAM_CHANGES.md` and in
`04_EXECUTION_PLAN.md` is now identical — sixteen in each, no id in one and not the other — and each
id's subject matches its counterpart's by title. That is a check on the pass, not on the plan: it proves
the two documents agree about which item is which, which is exactly and only what § 7a said was broken.

