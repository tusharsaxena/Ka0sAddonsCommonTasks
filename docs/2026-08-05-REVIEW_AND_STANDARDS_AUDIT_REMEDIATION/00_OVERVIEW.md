# 00 — Overview

**Consolidated spec and plan for the Ka0s World of Warcraft addon collection.**

Produced 2026-08-05. Nothing in this directory has been executed.

---

## NOTHING HERE HAS BEEN RUN

Read this first, because the rest of these documents are written in the imperative and will read like
a changelog if you skim them.

- **No addon, library, standard or plugin repository has been modified.** Every repo listed below was
  read-only for the whole of this exercise.
- **No commit, branch, tag, push or file edit exists anywhere outside this directory.** The only files
  created are the six documents you are reading.
- **Every work item in `04_EXECUTION_PLAN.md` is unstarted.** The verification commands are written so
  the owner can run them; none of them has been run as part of applying a change.
- **This awaits the owner's go-ahead.** Milestone 1 in particular changes three upstream repositories
  that every addon depends on, and it should not begin until the owner has read `02_UPSTREAM_CHANGES.md`
  and `03_SPEC.md` and said so.

Where a suite figure appears (test counts, lizard numbers, lint results), it was *observed* by
re-running the suite during the per-repo verification passes that fed this consolidation. Observing a
suite is not changing a repo.

---

## What this is

Nine repositories were each independently reviewed and audited on 2026-08-04/05, producing eighteen
frozen bundles. Each bundle pair was then triaged by a separate verification pass that re-ran all four
suites, re-opened every cited `file:line`, and re-graded severity by reachable impact rather than by
the strength of the rule that was broken.

This directory is what came out the other end: one finding ledger, one spec, one plan, and one
traceability proof, across the whole collection.

The four documents that carry the substance:

| File | What it is |
|---|---|
| `01_CONSOLIDATED_FINDINGS.md` | Every surviving finding, grouped by cluster then repo, with evidence and rule reference. Plus what triage rejected, and why. |
| `02_UPSTREAM_CHANGES.md` | Milestone 1 — every change to LibKa0s, WowAddonStandards and the `wow-addon` plugin, with the findings each unblocks and the adoption cost it creates. |
| `03_SPEC.md` | The normative end state per cluster: target shape, acceptance criteria, explicit non-goals. Not a schedule. |
| `04_EXECUTION_PLAN.md` | Milestones with ordered, individually-verifiable work items — id, repo, change, verification command, dependencies. |
| `05_TRACEABILITY.md` | Every finding id → cluster → milestone → work item, with the coverage proof. |

---

## Scope

### Repositories

Nine, all under `/mnt/d/Profile/Users/Tushar/Documents/GIT/`:

**The eight roster addons** (`WowAddonStandards/standards/ADDONS.md:19-26`) — AbsorbTracker,
BankLedger, ConsumableMaster, KickCD, LootHistory, PanelMaster, prettychat, WhatGroup.

**One shared library repo** — LibKa0s. It is *not* on the roster, and that omission is itself a finding
cluster (C13): six of its twenty findings are addon-scoped documentation rules applied to a repo that
ships nothing a player installs.

Three further repositories are **changed by this plan but were not audited**: WowAddonStandards (the
standard itself), the `wow-addon` plugin, and — for the vendored payload — LibKa0s in its role as
upstream rather than as an audited repo.

### Runs consumed

Per repo, two frozen bundles under the repo's own `docs/`:

| Repo | Review bundle | Audit bundle |
|---|---|---|
| AbsorbTracker | `docs/reviews/2026-08-05/` | `docs/audits/2026-08-05/` |
| BankLedger | `docs/reviews/2026-08-05/` | `docs/audits/2026-08-05/` |
| ConsumableMaster | `docs/reviews/2026-08-05/` | `docs/audits/2026-08-05/` |
| KickCD | `docs/reviews/2026-08-05/` | `docs/audits/2026-08-05/` |
| LootHistory | `docs/reviews/2026-08-05/` | `docs/audits/2026-08-05/` |
| PanelMaster | `docs/reviews/2026-08-05/` | `docs/audits/2026-08-05/` |
| prettychat | `docs/reviews/2026-08-05/` | `docs/audits/2026-08-05/` |
| WhatGroup | `docs/reviews/2026-08-05/` | `docs/audits/2026-08-05/` |
| LibKa0s | `docs/reviews/2026-08-05/` | `docs/audits/2026-08-05/` |

Plus the most recent automated-test bundles referenced as evidence — `docs/automated-tests/20260804-233138/`
(AbsorbTracker), `…-233144/` (BankLedger), `…-233147/` (ConsumableMaster), `…-233245/` (KickCD),
`…-233322/` (LootHistory), `…-233329/` (PanelMaster), `…-233338/` (prettychat), `…-233335/` (WhatGroup),
`20260805-002859/` (LibKa0s).

### Out of scope

- The two non-roster WoW folders in the same parent directory (`BuffTextNotifications`, `WhoGotLoots`).
- Frozen bundle contents under `docs/audits/`, `docs/reviews/` and `docs/automated-tests/` — they are
  evidence and are never rewritten, including their British spellings and their impossible durations.
- Anything requiring an in-game client. Every smoke-test step in `04_EXECUTION_PLAN.md` is written as an
  instruction to the operator, never as a claim that it passed.

---

## Headline numbers

| | |
|---|---|
| Repositories | **9** |
| Bundles consumed | **18** (9 review + 9 audit) |
| Surviving triaged findings | **254** |
| Clusters | **33**, absorbing **224** findings |
| True one-offs | **30** |
| Distinct underlying problems | roughly **35** |
| Milestones | **5** |
| Work items | **96** (**97** under `M1-STD-11` option (b), which schedules the conditional `M1-LK-15`) |

### Severity, after triage

| Severity | Count | Note |
|---|---|---|
| Critical | **0** | Nothing taints a protected frame, corrupts SavedVariables, or loses user data. |
| High | **8** | 5 of them are degraded-install paths in ConsumableMaster and PanelMaster; 3 are user-visible output defects in prettychat and WhatGroup. |
| Medium | **30** | Led by the harness forks (4), the perf harness's live members, and the options-lifecycle group. |
| Low | **173** | Includes all ten vendor-sync-gate rows, re-graded to one severity in adversarial review. |
| Info | **43** | |
| **Total** | **254** | |

**Seven rows moved Medium → Low after the plan was written.** C6 is one byte-identical defect
(`if not tag then return end`) in six repos, graded Low in three of the source bundles and Medium in
seven. The reachability is identical everywhere — a clone with no `../LibKa0s` sibling, which no repo's CI
or git hook produces because no repo has either — so under this plan's own impact rubric all ten are Low.
See `05_TRACEABILITY.md` Part 2.

### Suite state — all four suites, all nine repos

Every figure below was reproduced by re-running the suite; none disagreed with the committed bundle.

| Repo | lint | tests | perf | complexity (CCN > 15) |
|---|---|---|---|---|
| AbsorbTracker | 0/0, 28 files | 470/470 | 6 scenarios, clean | 0 warnings, max 15 |
| BankLedger | 0/0, 24 files | 726/726 | no `tests/perf.lua` — skip | 0 warnings |
| ConsumableMaster | 0/0, 54 files | 656/656 | no `tests/perf.lua` — skip | 0 warnings |
| KickCD | 0/0, 32 files | 737/737 | no `tests/perf.lua` — skip | 0 warnings |
| LootHistory | 0/0, 23 files | 579/579 | no `tests/perf.lua` — skip | 0 warnings, max 15 |
| PanelMaster | 0/0, 25 files | 706/706 | no `tests/perf.lua` — skip | 0 warnings, max 15 |
| prettychat | 0/0, 17 files | 255/255 | no `tests/perf.lua` — skip | 0 warnings, max 12 |
| WhatGroup | 0/0, 14 files | 422/422 | no `tests/perf.lua` — skip | 0 warnings, max 13 |
| LibKa0s | 0/0, 11 files | 480/480 | no `tests/perf.lua` — skip | 0 warnings, max 12 |

**All four suites are green in all nine repos, and the commit gate passes everywhere.** Nothing in this
plan is unblocking a red build.

**The release gate is a weaker claim, and it is worth stating precisely.** It has never been exercised:
every one of the nine most recent manifests records `"release": null` and `"dirty": true`, so no repo holds
a release-labelled bundle at all — a state filed as a finding for LibKa0s (`LK-A-07`) and for nobody else.
And the gate's one sanctioned exception carries an obligation that is unmet: `perf` skipped for an addon
shipping no `tests/perf.lua` passes, but **MUST** be stated in the Step 6 report and the release notes
(`bump-version.md:62-64`). No addon's release notes say it (that is C8 and `LH-A-24`), and the command
never writes it (that is `M1-WA-06`). So eight of nine repos would pass the mechanical gate while failing
its attached MUST.

---

## The two gates — stated precisely, because the collection is confused about them

This distinction is load-bearing for four of the five milestones and nine of the findings, so it is
written out once here and referenced everywhere else.

**A commit is gated on `lint` + the harness, and nothing else** (`testing-§4`). `perf` and `complexity`
are recorded at a run and never fail one. A threshold on every commit gets routed around with
`--no-verify`, after which it protects nothing.

**A tag is gated on all four suites at `pass`, plus `suites.complexity.warnings == 0`** — zero functions
above CCN 15 (`automated-tests-§3`, *The release gate*). The runner's exit code is unchanged, because
the same vendored script is the commit gate. The release gate is evaluated by `/wow-addon:bump-version`
from the run's `manifest.json` (`wow-addon/commands/bump-version.md:45-54`), and a `skip` there blocks as
**NOT EVALUATED** rather than reading as a pass (`bump-version.md:56-58`). One narrow exception:
`perf` skipped because the addon ships no `tests/perf.lua` passes the gate and **MUST** be stated in the
release notes (`bump-version.md:62-64`).

Nine of the nine repos state only the first half. That is cluster **C8**, and it is machine-generated —
`LibKa0s/testkit/run-automated-tests.sh:372` emits the sentence into every `RESULTS.md`.

### One correction to the input analysis

The cross-repo analysis handed to this exercise states that the runner's hardcoded `"gating": false`
(`LibKa0s/testkit/run-automated-tests.sh:322-323`) "currently makes `bump-version`'s release gate
structurally unable to fire." **That is not true, and it was checked.** `bump-version.md:45-54` evaluates
the gate from `suites.<name>.status` and `suites.complexity.warnings`; it never reads the `gating` field.
The `gating` field is decorative in the manifest. The C8 problem is real — the *emitted prose* is a
half-truth in nine repos — but it is a documentation defect, not a broken gate. `02_UPSTREAM_CHANGES.md`
and `04_EXECUTION_PLAN.md` are written against the corrected reading.

---

## How this was produced

1. **Nine review bundles and nine audit bundles** were produced independently, per repo, by the
   `wow-addon:review` and `wow-addon:standards-audit` skills.
2. **A per-repo verification pass** re-ran `luacheck .`, `lua5.1 tests/run.lua`, `tests/perf.lua` where
   it exists, and `lizard -l lua -x "./libs/*" -x "./tests/_kit/*" .`; re-opened every cited `file:line`;
   reproduced the reproducible defects by execution where possible; and re-graded severity by reachable
   impact. That pass rejected findings outright where the evidence did not survive — see
   `01_CONSOLIDATED_FINDINGS.md` § *Rejected in triage*.
3. **A cross-repo pass** clustered the survivors, attributed each cluster's root cause to the repository
   that can actually fix it, and measured four things the individual bundles had each under-counted:
   the vendored runner's git index mode (9/9 at `100644`), the retired `§N.M` notation (368 live sites
   across 9 repos, 5 filed), the negative `durationMs` values (5 committed manifests), and the absence of
   `Kit.skip` from `testkit/framework.lua`.
4. **A spot-verification pass for this document** re-confirmed the load-bearing mechanical claims
   directly: the nine index modes, `run-automated-tests.sh:372` and `:322-323`, the absence of any
   `Kit.skip` in `testkit/framework.lua` (`Kit.VERSION = 7`), the standard at v2.21.0 with `performance`
   carrying §1–§11 and anti-patterns running to #55, and `bump-version.md`'s actual gate conditions.

### The evidence rule

Every claim in these six documents resolves to a `file:line` in a named repository, or to a named
bundle artifact. Where a bundle's own claim did not survive re-checking, the finding is recorded with
the correction attached rather than dropped silently, and where a bundle's prescribed *fix* is wrong it
is called out as a do-not-execute (there is exactly one: `AT-R-01` — see `03_SPEC.md` § C9).

Counts in these documents are always written with their members named, per the house rule.

---

## The shape of the answer, in one paragraph

254 findings describe roughly 35 distinct problems. Four clusters — C1 (perf harness declined, re-filed
as 5–7 MUSTs per repo), C4 (ratified deviations re-audited as open), C8 (release gate undocumented) and
C15 (retired section notation) — account for **66 findings** and are counting artifacts of three things:
one declined library adoption the standard has no vocabulary for, one notation change that was never
swept, and one vendored script's hardcoded output. Eight findings are worth fixing this week, and five
of those live in two repos' degraded-install paths. Milestone 1 changes three upstream repositories so
that the remaining four milestones have something honest to adopt; Milestone 2 fixes the eight Highs and
does not depend on Milestone 1 at all.

And one caveat the coverage proof is supposed to earn rather than assume: **"254 mapped" is not "254
remediated."** Roughly fifty findings close by a rule change or a register row without the cited code
changing, and five more are decided upstream by a fork (`M1-STD-11`) whose two branches differ by two
orders of magnitude in cost. `05_TRACEABILITY.md` Part 1 now carries a **Disposition** column so that
distinction is visible per row rather than inferred.

---

## Adversarial review

After the six documents were written, three independent critics re-derived the load-bearing claims
against the live repositories rather than against the documents. **32 objections were raised — 11
blocking, 12 major, 9 minor.** Every one was re-checked here by execution before it was applied or
rejected. **29 were applied in full, 1 in part, and 2 were rejected** — all three of the last on measured
evidence.

Nothing in this section changes what the plan is trying to do. It changes eleven places where the plan
would not have worked.

### The eleven blocking objections

| # | What the critic found | Verified how | Applied as |
|---|---|---|---|
| 1 | **The vendor-sync gate's CRLF `gsub` is required, not a defect.** The plan ordered `no CRLF normalization` and "remove any `gsub("\r\n","\n")`". The gate compares a working-tree file against a `git show` blob. | `git -C LibKa0s show HEAD:LibKa0s/Core.lua \| tr -cd '\r' \| wc -c` → **0**; `tr -cd '\r' < AbsorbTracker/libs/LibKa0s/Core.lua \| wc -c` → **322**; 8/9 repos pin `eol=crlf`. | `M1-LK-02`, `M1-STD-03`, `M3-02`, `03_SPEC` C6, `01` C6 and the corrections table: one CR strip on the working-tree side, `testing-§11`'s MUST scoped to the library-side pair. |
| 2 | **`CM-A-16`'s substance was lost** — its row carried `CM-A-23`'s evidence byte-for-byte, so the id survived the coverage proof while the finding did not exist. | `grep` for `toc-file-§5` / "load order" across all six docs → 0 hits; the real finding is `CM-49` at `ConsumableMaster/docs/audits/2026-08-05/02_DEVIATIONS.md:36`. | Real row restored in `01` C4; register row named in `M3-08`; rule half added as `M1-STD-15` part 3. |
| 3 | **Part 5's "no M2–M5 item touches an upstream repo" was false in four places**, and `M4-08` duplicated `M1-LK-12`'s LibKa0s README edit with no finding behind it. | Read `M3-01`, `M3-07`, `M4-08`, `M5-03` repo columns; `LK-A-11` maps to `M1-LK-12` only. | LibKa0s clause deleted from `M4-08`; Part 5's proof restated precisely. |
| 4 | **No item re-vendors `libs/LibKa0s/`.** `M3-01` was kit-only while bumping the README provenance line the gate reads for **both** pairs. | `AbsorbTracker/tests/test_vendor_sync.lua:100-102`, `:138-141`, `:144-149`. | `M3-01` now copies both payloads in one commit; `M3-12`/`M3-13`/`M3-14a` depend on the library half. |
| 5 | **No item cuts the LibKa0s release** every M3 item depends on. | `LibKa0s/docs/releasing.md:20-59` is a nine-step gated procedure; latest tag is **v1.7.0**. | New **`M1-LK-14`** — cut v1.8.0, steps 1–7 verbatim. `M3-01` depends on it; it is M1 exit criterion 4. |
| 6 | **`M3-10`'s dependency column and the contention note contradicted each other**, and KickCD's hand-typed loader list was migrated by nothing. | `KickCD/tests/loader.lua:29-36`; KickCD absent from `M3-03`'s repo list. | `M3-03` rescoped; new **`M3-03b`** (CM + KCD, after `M3-10`); contention note corrected. |
| 7 | **`M1-STD-11` option (b) scheduled ~50 call-site rewrites against a LibKa0s API with no item.** | `M4-27`'s dependency column named only `M1-STD-11`. | New **`M1-LK-15`** (CONDITIONAL); `M4-27` re-gated; the fork recorded as a prerequisite in `03_SPEC` C11. |
| 8 | **`M1-WA-03`'s grading rule is overridden at runtime** because `AUDIT.md:91` still says "MUST/SHOULD severity". | `AUDIT.md:91`; `wow-addon/agents/standards-audit.md:44` — "the fetched playbook wins". | New **`M1-STD-17`** edits `AUDIT.md:91`; `M1-WA-03` depends on it; M1 exit criterion 6. |
| 9 | **Observed containment cannot observe anything** — it was specified as a `P.Open`/`P.Close` stack, and **zero** such call sites exist. | `grep` across AbsorbTracker, KickCD, ConsumableMaster: every bracket is `local t0 = Perf.on and debugprofilestop()` … `Perf.Note(…)`. `P.Open()` (`Perf.lua:400-403`) takes no key. | `M1-LK-08` respecified as `P.Note(key, ms, parentKey)`; `M3-12` passes the parent; the unbalanced-bracket claim withdrawn. |
| 10 | **`M2-01`'s "zero mismatches" is unachievable** and mandates four behavior changes with no finding behind them. | Re-derivation executed under `lua5.1`: **81 overrides, 6 mismatches**; four are safe truncations. | Restated as a **positional-prefix** rule in `M2-01`, `M4-06` and `03_SPEC` § The eight Highs, with the four sanctioned keys named. |
| 11 | **The `§N.M` sweep omitted `docs/automated-tests/`**, making C15's acceptance reachable only by corrupting frozen evidence; and it swept LibKa0s's **shipped** source, which is vendored into all eight addons. | KickCD: 69 hits under the old exclusions, **39** with `docs/automated-tests/` added — 30 inside frozen bundles. `diff -q LibKa0s/LibKa0s/Options.lua AbsorbTracker/libs/LibKa0s/Options.lua` → identical. | Fifth exclusion added in `M1-WA-07`, `M3-07` and `03_SPEC` C15; the two shipped-source sites moved into `M1-LK-10`. |

### The twelve major and nine minor objections, applied

- **Accounting.** The "37 Mediums by work item" table omitted `M4-19`/`BL-R-01` and summed to 36. Rebuilt
  and re-derived from Part 1.
- **C6 severity.** One byte-identical defect carried three severities across ten findings. Re-graded to a
  single **Low** with one stated reachability line; totals moved 37 → 30 Medium, 166 → 173 Low, and the
  per-repo table, the Mediums table and this document's headline all move with it.
- **`M3-08`'s uncovered rows.** `PC-A-21` (record at `DEPENDENCIES.md:118-119`, a `library-stack`
  contradiction), `CM-A-16` and `AT-A-10` are now named in the item. `WG-A-13` is **out** of C4 — nothing
  ratifies it — and is code work at `M4-24`.
- **`M4-10` unblocked.** Eleven one-line comment fixes no longer wait on a plugin feature; `M1-WA-10` is
  re-sequenced after them as the recurrence guard.
- **`M1-LK-09` reduced to one scalar.** Five of six proposed publishes had **no** consumer anywhere in the
  collection — anti-pattern **#55** verbatim, added to the standard one day before this plan.
- **`M1-STD-12` narrowed.** The `events-frames-taint-§1` carve-out rested on one Info row with a written
  justification already in place; it is a register row, not a permanent exception in a shared document.
  The `architecture-§4` scope sentence stays, because that MUST is unsatisfiable in principle for a
  single-module addon.
- **`M1-LK-04`'s premise corrected.** BankLedger (20/20) and PanelMaster (20/20) **already ship** the
  suite-inventory gate and are the reference implementations; ConsumableMaster auto-discovers. `M3-01`
  gains a per-repo pre-flight so a later drift is caught rather than assumed.
- **`C12`'s acceptance narrowed** to "derived or pinned", which is what `testing-§9` wants and what five
  repos already satisfy; `M3-03` scoped to the three that do not.
- **`M1-LK-06` gains `:86`.** Converting `:272` without `RUN_START` yields epoch-ms minus epoch-s
  (≈1.7 × 10¹²) — and the "no negative `durationMs`" check passes on it. A magnitude check was added.
- **Parallelism claims fixed.** "Group A, B, C and M2 in parallel" was false in seven places; M2 alone is
  unconditionally parallel, and Group B leads.
- **Exec bit de-duplicated** (`M3-05` only), **`M3-14` split** (`M3-14a` + `M4-28`), **`M4-01`'s KickCD
  half** recorded as running before `M3-13`, **`M2-05`'s verification** reworded off the `M3-04` primitive,
  **M1 exit criterion 6** reworded so M2's parallel work does not read as a violation.
- **Verification commands that cannot fail.** `M4-27`'s `grep -cE '…' settings/` lacked `-r` and reports
  "Is a directory", which reads as a clean result — fixed. A standing rule was added: every "Verified by"
  command is shown red against a planted violation before it is accepted. (The related claim about
  `grep -rniE "colour\|grey\|behaviour"` is **half right and is recorded as such**: in a GFM table cell
  `\|` is table escaping and renders as a literal pipe, so the rendered command is a correct ERE — but
  copied out of the raw markdown it becomes a pattern that can never fire, which is now said explicitly at
  every such site.)
- **Traceability hardened.** A `Closes` column on all 97 work-item rows and a `Disposition` column on all
  254 Part-1 rows, with the rule that a disagreement between them is the signal an item was edited without
  re-mapping.
- **Citations and spelling.** `run-automated-tests.sh:118` → `:117`; the `PADDING_X` site list completed
  (`:203`, `:331`); "neighbours" → "neighbors" at `01_CONSOLIDATED_FINDINGS.md`; doc-set counts enumerated
  at every site (`03_SPEC` invariant 4 now carries all five lists once, and everything else points at it).

### Rejected — two, both on measured evidence

1. **"`M3-02` leaves WhatGroup red because its README provenance line does not match the canonical
   `Bundles [LibKa0s](...) vX.Y.Z (MIT).` sentence."** *Rejected.* The critic read the assertion **message**
   at `AbsorbTracker/tests/test_vendor_sync.lua:114` as the pattern. The actual pattern is
   `[Bb]undles %[LibKa0s%]%b() (v[%d%.]+)`, deliberately lenient about casing and mid-sentence position
   because LootHistory writes it that way — the file says so at `:95-99`. Executed against WhatGroup's
   `README.md:83` it returns `v1.7.0`; prettychat's `README.md:122` is the canonical form. Neither repo
   needs a `readmePattern` override, and neither is expected to redden on the provenance line. The check
   and its result are now recorded in `M1-LK-02` and `M3-02` so the question does not come back.
2. **"PanelMaster's slash stub returns at `:317`, not `:316`."** *Rejected.* `grep -n "" PanelMaster/settings/Slash.lua`
   puts `return` on **`:316`** and the closing `end` on `:317`. The plan was right; `M2-05`'s citation is
   unchanged (the surrounding text now also names `:285` and `:381` explicitly).

### What the review did not change

The finding set (254), the cluster count (33), the eight Highs, the five deferrals, and Milestone 2's
independence from Milestone 1. Every number that moved, moved because a measurement disagreed with the
document — and the measurement is quoted beside it.
