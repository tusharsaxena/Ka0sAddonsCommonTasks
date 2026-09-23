# Suite sweep 2026-09-22 — harvest, re-vendor standards, re-vendor LibKa0s + adoption

**Plan of record.** This file is the resume point. Read it first; keep it current. Every phase ends at
a committed checkpoint, so the run can stop anywhere and pick up from the ledger below.

## Current position

> **Phase 3b in flight.** 3a is done: test-kit revision 25 committed as `LibKa0s@2a5e06f` (1318/0/1,
> luacheck 0/0) after a sixth fix closed the verifier's late-narrowing major. 3b (Compat, Bus, Schema
> portable half) runs as workflow `wf_1b472691-c6f`: design -> build -> integrate -> consumer-driven
> verify -> fix loop. The owner delegated CP-3 and CP-6 (see *Owner decisions*, 2026-09-23 rows).

## How to resume

1. `cd /mnt/d/Profile/Users/Tushar/Documents/GIT/Ka0sAddonsCommonTasks && git log --oneline -5` - the
   last `CP-n` commit names the last checkpoint that landed.
2. Read **Current position** above, then **Uncommitted work in flight**, then the **Status ledger**.
3. Every repo in the sweep sits on branch `suite/2026-09-22-standards-sweep`. Nothing is merged and
   nothing is pushed - that is deliberate (see *Owner decisions*).
4. Resume at the first ledger row that is not `done`. Each phase's own artifacts (the harvest bundle,
   the per-addon revendor bundles) are the detailed state; this file is the index to them.
5. **Before starting any phase, read *Contracts Phase 3 owes* below.** Text already written into the
   standard cites a LibKa0s tag and kit revision that do not exist yet. A phase that ignores that
   leaves eleven repos measured against rules nothing can satisfy.

## Uncommitted work in flight

**Check this before anything else.** Run `git status` in each repo and reconcile against this table. A
working tree that does not match it is a session that died mid-phase.

| Repo | Expected state | What it is |
|---|---|---|
| `LibKa0s` | **modified, uncommitted while 3b runs** | Phase 3b: the three new majors. Commits after its verify loop. |
| every other repo | **clean** | Phases 0-2 are committed. |

If a repo is dirty, a phase died mid-run. Read that phase's row in the ledger, then the phase's own
artifacts, before deciding whether to keep the work or discard it. Nothing in this run is expensive to
redo: each phase's evidence is committed before the phase that consumes it.

## Contracts Phase 3 owes - pinned, not negotiable

Phase 2 wrote commencement clauses into the standard that **name a library release which does not exist
yet**. That was the fix for a whole blocker class: a MUST no repo can satisfy by any act of its own. The
numbers below are therefore a contract - Phase 3 delivers exactly them, or the standard is wrong.

- **LibKa0s `v1.55.0`**, carrying **test-kit revision 25** (`testkit/framework.lua` -> `Kit.VERSION = 25`;
  it is at 24 today).
- The phrase the standard uses, verbatim, is **"from LibKa0s test-kit revision 25 (LibKa0s v1.55.0)"**.
  Grep for it before cutting the tag and make every citation true.

**Phase 3 therefore has seven deliverables, not three** - the three approved extractions, plus the kit
gates Phase 2's new rules now cite by name:

| # | Deliverable | Cited by |
|---|---|---|
| 1 | `LibKa0s-Compat-1.0` - the ~400 genuinely duplicated lines out of 2820 across 9 copies; the addon-specific remainder stays in each `core/Compat.lua` | `open-evolutions`, `compat` |
| 2 | `LibKa0s-Bus-1.0` - the union design, which is the per-receiver register whose `StandDown`/`StandUp` replay from a live record | `architecture-§4` |
| 3 | Schema runtime - **portable half only**, behind `resolveRoot` and `announce` callbacks | `open-evolutions` |
| 4 | `test_layout_cap.lua` - the 1500-line cap gate | `layout-§1` |
| 5 | `test_eol.lua` second case - the `.gitattributes` body gate (owner ruling O3) | `line-endings-§7` |
| 6 | `framework.lua` - declaration keyed by **(basename, directory)**; collision and unreferenced-kit-suite reporting | `testing-§9` |
| 7 | The automated-test runner - emit the commit SHA and clean flag into `RESULTS.md` and `manifest.json` | `automated-tests-§4` |

The doc-shape gate and the lint-config gate were accepted in the batch and are candidates for the same
revision; confirm against `harvests/2026-09-22/06_OUTCOME.md`'s rollout-debt table, which marks every
item that cannot be discharged until v1.55.0 ships.

## Why Phase 3 was split (2026-09-23)

The seven deliverables are two different kinds of work and carry different risk, so they ship as two
passes with the tag after both.

- **3a - the kit (deliverables 4-7).** These are what **five committed rules in standard v2.63.0 cite
  by name**. Until they exist, those rules describe a release that never shipped, so this half is not
  optional and not negotiable in shape: it is built *to the rule text*, and a mismatch is reported
  rather than quietly built differently.
- **3b - the extractions (deliverables 1-3).** Compat, Bus and the Schema runtime's portable half.
  Additive, larger design surface, and their real test is Phase 6 adoption rather than the standard.

A verify lens in 3a produces the **per-repo consumer impact list** - which of the twelve repos goes red
on which new gate when it re-vendors. That list is Phase 5's and Phase 6's work, and nobody recovers it
as cheaply later.

## 3a fix rounds (2026-09-22/23)

| Round | Workflow | Closed | Verify found |
|---|---|---|---|
| 1 | `wf_19b2a06b-9a9` | built rev 25 | path-spelling blocker (`./tests/_kit/` vs `tests/_kit/`) aborts MultiMeters + KickCD |
| 2 | `wf_45b23e7b-72e` | `normDir`; prose generated-data carve-out | self-test reads live `Kit.prose`; carve-out is a silent whole-file waiver |
| 3 | `wf_cfae017e-fb8` | fixture-driven self-test; TOC + `.pkgmeta` refusals; disclosure | `prose_waivers.lua` skipDirs/skipFiles ungated beside the gated `Kit.prose.exempt` |
| 4 | `wf_1fca1599-61d` | waiver file routed through the refusals | refusals disagree: `.pkgmeta` checked on the entry, TOC on coverage - `skipDirs = {"tools"}` hides root `tools-notes.md` |
| 5 | `wf_006f57e4-eb5` | one resolved coverage set feeds both refusals + disclosure; paths listed (bounded); `waived` validated; covers-nothing message | verify died with the session; re-run as a plain agent 2026-09-23 |

Round-5 open judgement calls from the fixer: `test_prose.lua` sits 4 lines under the 1500 cap
(CLAUDE.md's watch-list figure for it is stale); a covers-nothing entry `.pkgmeta` does ignore stays
green (stale-not-failing doctrine); the TOC refusal no longer fires on TOC paths outside the scan
universe; disclosure thresholds 12 / 3.

## Phase 5 checklist, measured by running every tree (2026-09-23)

Not estimated. All twelve repos were copied **with `.git`** (the eol and cap gates shell out to
`git ls-files` and `git check-attr`), baselined green, then had revision 25 vendored in and re-run; then
the whole release was simulated in seven of them - a tagged throwaway LibKa0s, the provenance line
bumped, the census written, `.gitattributes` replaced with the canonical body.

**Every repo aborts on first vendor** with one or two inventory problems, and that is the gate working:
`tests/_kit/test_layout_cap.lua` arrives undeclared, and in six repos a bare `"test_prose"` or
`"test_layout_cap"` now reads as a shadow. Wiring is the first step everywhere.

| Repo | Baseline | On full rollout | What it owes beyond wiring |
|---|---|---|---|
| **AbsorbTracker** | 647 | **668 / 0** | nothing - fully green |
| **MultiMeters** | 1908 | **1926 / 0** | nothing - fully green; census already correct |
| AuraMaster | 1255 | 1270 / 6 | census heading; **its own `tests/test_docs.lua`** - `DEPENDENCIES.md` cites three kit line numbers revision 25 moved. Only repo whose `.gitattributes` was already canonical. |
| KickCD | 1006 | 1022 / 5 | census heading. Calls `assertSuiteInventory` a **second** time from `tests/test_coresetup.lua`; a decline registers exactly once across both - verified. |
| PartyFrameEnhanced | 241 | 257 / 5 | census heading. Nothing else. |
| ConsumableMaster | 958 | 971 / 5 | census exists but sits **outside** the register (line 28 vs the register at 480). A move, not new work. |
| PanelMaster | 848 | 860 / 6 | census headed `Files by the layout-§1 band` - owes a **rename and a move**. Plus the `.py` terminator breakage on four `tools/artwork` + `tools/sunn` generators: add the line, then `rm <path> && git checkout -- <path>` per file, **in the same commit**. |
| PrettyChat | 401 | green with opts | the **only** repo needing both carve-outs: `Kit.prose = { exempt = { "GlobalStrings/" } }` and `Kit.layoutCap = { exempt = { "GlobalStrings/" } }`. With them the three disclosure cases pass and report *"suppressed 28 of 95 tracked authored files"*. Without them: 34 prose failures. |
| LootHistory | 801 | 816 / 6 | census heading + **2 real British spellings** its own 262-line copy never caught (`core/LifecycleSetup.lua:66,:79`). |
| WhatGroup | 686 | 701 / 6 | census heading + **5 real British spellings** (`core/WhatGroup.lua:317,:940`, `docs/data-flow.md:56`, two test files). |
| **BankLedger** | 959 | 973 / 7 | census heading **and a trap**: its own `tests/test_harness.lua` parses the suites list and understands only bare strings, so following the kit's remedy literally crashes it with *"attempt to concatenate local 'suite' (a table value)"*. **Teach that file the pair form first**, before wiring anything else in this repo. |

**`.gitattributes`:** ten of eleven owe the `*.py text eol=lf` line; AuraMaster is the only one already
canonical. In PanelMaster that fix must land with the per-file re-checkout or the repo is red between
steps.

**Census:** nine owe one - seven absent, ConsumableMaster's misparented, PanelMaster's misnamed *and*
misparented.

### Ordering, which is not negotiable

1. **Commit and tag LibKa0s v1.55.0 first.** `vendor_sync` **fails rather than skips** on a missing tag,
   so a consumer that rolls its provenance line before the tag exists is red with no act of its own able
   to clear it.
2. Then per repo: vendor both payloads, roll the provenance line **in the same commit**, wire the suites,
   then discharge that repo's row above.

### The lesson 3a earned, three times over

Every defect in revision 25 was **work enforced in one place and unenforced in the place right beside
it**, and every one was invisible from inside LibKa0s:

- a raw string comparison of two spellings of one path - green here, **aborted the entire suite** in the
  two repos that declare the kit suite exactly as the standard prescribes;
- a self-test reading **live consumer state** instead of a fixture - permanently green here (this repo
  declines that gate), permanently red in the one repo the feature exists for;
- a carve-out gated on `Kit.prose.exempt` while the waiver file beside it stayed ungated, with the
  failure text **advertising the unpoliced door**.

**LibKa0s is an unrepresentative consumer of its own kit** - it declines the prose gate, spells its
paths one way, has no `.toc` and no `libs/`. A green run here proves very little. **Drive a gate against
the trees it will govern, not only the tree that wrote it.**

## Phase 2 defect record - the seven blockers, so the repair is verifiable rather than trusted

Found by a four-lens adversarial audit of the v2.63.0 release **before** it was committed. Thirteen
blocker reports collapsed to seven distinct defects; the duplication was four lenses agreeing.

| # | Site | Defect |
|---|---|---|
| 1 | `layout-§1` | The cap gate's scope said "this section's two carve-outs (`libs/`, `tests/_kit/`)". Those are two *instances* of one carve-out; the real second is **generated non-shipping data**. As written the gate fails a repo on its 23,842-line generated file - the exact case the carve-out exists for, cited in that same section. |
| 2 | `layout-§1`, `automated-tests-§4` | Mandated a kit suite file and `RESULTS.md` commit columns, neither of which ships in any kit revision. Every repo non-compliant on release day with **no act available to become compliant**. Fixed by the v1.55.0 / revision 25 commencement. |
| 3 | `testing-§1` | "Every gate ... MUST read the whole `git ls-files` set" - false for the two payload gates `testing-§11` mandates and the parity gate `testing-§8` mandates. The quantifier had to move to the rule's own denominator. |
| 4 | `testing-§9` vs `localization-§5` | §9 made an unreferenced kit suite a MUST-level failure; §5 explicitly permits declining a kit gate and wiring your own. Both MUSTs could not be satisfied. |
| 5 | `audit-review-history` | Claimed `versioning-git` "requires the re-vendor commit **to stand alone**". Checked against the file: the commit is a **MUST**, standing alone is a **SHOULD** (`versioning-git.md:9`). One audit lens claimed the rule was absent entirely - that lens was wrong; do not act on it. |
| 6 | `AUDIT.md` | The re-vendor check grepped **commit subjects** for a tag and compared **bare folder names**, while the same release grandfathers bare-dated bundles - 28 of 68 on disk. It would have filed false High findings against ten repos for records that exist. |
| 7 | `README.md` | The Status line still advertised **v2.62.1**. The repo's own amendment procedure names that line as a required bump target, and Phase 4 reads this repo to learn the current version - it would have carried v2.62.1 into eleven addons. |

## Pass 2's own defects, corrected by measurement (2026-09-23)

Pass 2 cleared every blocker it was given and then shipped six new wrong numbers - the same failure mode
this release is *about*. Each was re-measured against the tree before correction:

| Site | Was | Measured |
|---|---|---|
| `layout.md` | "Eight addons wrote none at all" | **Seven** - 4 of 11 addons carry the gate; the fifth copy is the library's |
| `documentation.md` | "three nest it exactly there" | **Two** - ConsumableMaster nests under `## Layout`, LibKa0s keeps it a sibling `##` |
| `packaging.md` | "**Five** of them argue", "two states" | **Four**, and **three** states - one repo is simply silent, which the strong form permits |
| `library-stack.md` | "exactly two second edges" | **Three** - `OptionsWidgets.lua:33` and `OptionsTabs.lua:38` both floor on `LibKa0s-Pool-1.0` |
| `AUDIT.md` | "sixty-eight unregistered `.md` files" | **25-36 per repo**; 68 was the collection-wide *bundle* count |
| `line-endings.md` | "never **travelled**" | **traveled** - a British spelling, introduced by the pass promoting the prose gate, in a release whose anti-pattern #46 forbids exactly this |

**The lesson, now a standing rule for this run:** a number in an agent's report is a claim to verify, not
a fact to copy. Three passes have each shipped a count written from prose rather than from the tree.

## The commit gate's seven, fixed before CP-2 (pass 4)

Two were serious enough to have done real damage:

- **`events-frames-taint-§1`'s carve-out blessed only a frame that cannot work.** It permitted a private
  frame "whose only job is `RegisterUnitEvent`" and separately forbade it a script - but a frame that
  registers and never dispatches receives nothing. The permission now names the single `OnEvent` inside
  it, so the exclusions bite on a *second* job rather than on the first.
- **`AUDIT.md`'s EOL check was blind to the very MUST O3 is about.** It grepped `*.sh` only, while
  `line-endings-§3` has MUSTed `*.py` beside it since v2.61.0 and this release measured 12 of 14 repos
  failing exactly that pin. Until kit revision 25 lands, that playbook is the only check any repo has.

The rest: `layout.md:85` contradicted `:69` about the census heading's level; `AUDIT.md:190` kept the old
81/82 body-intact figure after `line-endings` moved to 84/85; the new gate's repo-kind discriminator
(`a .toc or a client-bound libs/`) **misfiles a Ka0s-owned library repo**, which has neither; the
call-site count said two where the tree has ten across four addons; and `documentation-§9` claimed
"nothing already on disk becomes non-compliant" while settling placement the way the collection's
majority does *not* write it - existing headers are now grandfathered where they sit.

## Workflow runs - for resuming a phase rather than redoing it

A completed workflow can be re-entered with `Workflow({scriptPath, resumeFromRunId})`; agents whose
prompt is unchanged replay from cache instead of re-running.

| Phase | Run ID | Result |
|---|---|---|
| 1 - harvest sweep | `wf_8f5827b0-12c` | complete; the bundle was written on a second pass after a payload-handoff defect was patched in the script |
| 2 - promote | `wf_8014b00e-a1f` | complete; produced v2.63.0 **and** the 13 blockers |
| 2r - repair (pass 2) | `wf_9b3c85ff-8c5` | complete; all seven blockers verified dead at their sites, but it introduced six count errors |
| 2f - final (pass 3) | `wf_ecb77e37-5ee` | complete; closed the judgement defects and ran the three-lens commit gate, which found 7 more |
| 2g - gate fixes (pass 4) | *(orchestrator, no workflow)* | the gate's 7 blockers fixed directly against measurements, then `CP-2` |

Scripts live under `~/.claude/projects/-mnt-d-*-AuraMaster/c09a6172-*/workflows/scripts/`.

## Scope

Resolved from `WowAddonStandards/standards/ADDONS.md`, not guessed.

- **11 addons** — AbsorbTracker, AuraMaster, BankLedger, ConsumableMaster, KickCD, LootHistory,
  MultiMeters, PanelMaster, PartyFrameEnhanced, PrettyChat, WhatGroup.
- **1 library** — LibKa0s (audited against `library-stack-§7`'s applicability list).
- **2 documentation-and-tooling repos** — WowAddonStandards, wow-addon (`documentation-§8` lane).
- **This repo**, Ka0sAddonsCommonTasks, holds the plan only. It is outside the audit rotation.
- **Out of scope:** `Outfitter` (a third-party fork, not on the roster).

**Starting state (2026-09-22):** standard at **v2.62.1**; LibKa0s at **v1.54.2** with `HEAD` on the
tag; all 11 addons vendoring v1.54.2; every repo clean on `master` before the branch was cut.

## Owner decisions taken at the top of the run

| Question | Decision |
|---|---|
| Harvest gate | **Auto-apply clear wins; interview judgement calls only.** A proposal that is already unanimous practice across the collection is promoted without asking. Anything the playbook calls an ambiguous signal — a MUST N repos fail, a standard-internal contradiction, a rule retirement — goes to the owner with both readings and counts. |
| Adoption depth | **Also build new LibKa0s majors.** Beyond adopting shipped v1.54.2 surfaces, extract the still-duplicated candidates named in `open-evolutions.md` (Compat shim, message bus, Schema runtime) into new majors, cut a tag, and re-vendor it across all 11 addons. |
| Branch policy | **Branch per repo, left unmerged and unpushed.** Branch `suite/2026-09-22-standards-sweep` in all 15 repos. Incremental commits, green gate before each. Merging and pushing is the owner's, via `/wow-addon:finalize`. |

### Added 2026-09-23

| Question | Decision |
|---|---|
| CP-3 / CP-6 interviews | **Delegated** - "use your best judgement to take whatever decisions you need". Every call is recorded with its evidence in the phase's output. |
| Orchestration | **Ultracode** - each phase runs as a workflow with adversarial, consumer-driven verify; commit incrementally. |
| Tag vs push | Tag `v1.55.0` **locally** after 3b, before Phases 4-5 (`vendor_sync` reads tags from the sibling checkout, never the remote). Push stays with finalize. |

## Phases

Each phase is a workflow run, ends at a checkpoint commit here, and is independently resumable.

- **Phase 0 — Setup.** Branches in all 15 repos; this plan committed.
- **Phase 1 — Harvest sweep (read-only on every addon).** The ten harvest categories swept across the
  collection with `repo:file:line` evidence; three filters applied (date, `open-evolutions` dedup,
  two-repo evidence bar). Writes `WowAddonStandards/harvests/2026-09-22/01..05`.
- **CP-1 — Interview.** Clear wins listed for information; ambiguous signals put to the owner.
- **Phase 2 — Promote into the standard.** Accepted proposals applied with the full ripple (section,
  index blurb, anti-pattern range, changelog, version bump, context pack, executive summary,
  playbooks). Writes `06_OUTCOME.md`.
- **Phase 3 — New LibKa0s majors.** The accepted extractions built in LibKa0s, with tests, `docs/api/`
  entries and the degradation stubs; kit revision paired; new tag cut.
- **CP-3 — Interview** on the major set before the tag is cut.
- **Phase 4 — Re-vendor the standard** into all 11 addons + LibKa0s + wow-addon. Documentation only:
  the three-place reference, retired notation and file names, unresolvable `filename-§N` references,
  the vendored quirks catalogue, `.gitattributes`.
- **Phase 5 — Re-vendor LibKa0s** into all 11 addons from the new tag: both payloads whole, the
  provenance line rolled in the same commit, per-addon `docs/revendor/2026-09-22/` delta bundle.
- **Phase 6 — Adoption.** Per addon: adopt shipped surfaces the addon still hand-rolls
  (characterization test first, green gate per commit); file declines as GitHub issues.
- **CP-6 — Interview** on the per-addon candidate list.
- **Phase 7 — Verify and report.** Full four-suite battery per repo; the run's summary written here.

## Status ledger

Legend: `pending` · `in-flight` · `done` · `blocked` · `skipped`

| # | Phase | Repos touched | State | Evidence |
|---|---|---|---|---|
| 0 | Setup — branches + plan | all 15 | **done** | this commit |
| 1 | Harvest sweep | WowAddonStandards (write); all others read-only | **done** | `WowAddonStandards@8609f86` — `harvests/2026-09-22/` (5 files, 3634 lines). 91 findings → 64 live → 18 verified. |
| CP-1 | Harvest interview | — | **done** | 4 rulings taken; see *Owner rulings* below |
| 2 | Promote into the standard | WowAddonStandards | **done** | `CP-2` = `WowAddonStandards@957b3c5`, v2.63.0, 23 files. Four passes: promote -> 13 blockers cleared -> 6 self-inflicted counts fixed -> commit gate found 7 more, all closed. Record in `harvests/2026-09-22/06_OUTCOME.md`. |
| 3a | Kit revision 25 - the four gates | LibKa0s | **done** | `LibKa0s@2a5e06f`. 1318/0/1, luacheck 0/0. Six fix rounds; the sixth (late narrowing refused by the gate itself) applied and proven in a consumer copy by the orchestrator. |
| 3b | The three extraction majors | LibKa0s | **in-flight** | `wf_1b472691-c6f`. Deliverables 1-3: Compat, Bus, Schema (portable half). |
| 3t | Cut v1.55.0 | LibKa0s | pending | After CP-3 only. |
| CP-3 | Major-set interview | — | **delegated** | Owner (2026-09-23): use best judgement. Design agents record each call; orchestrator reviews them before the tag. |
| 4 | Re-vendor the standard | 11 addons + LibKa0s + wow-addon | pending | — |
| 5 | Re-vendor LibKa0s | 11 addons | pending | — |
| 6 | Adoption | 11 addons | pending | — |
| CP-6 | Adoption interview | — | **delegated** | Owner (2026-09-23): use best judgement. |
| 7 | Verify and report | all | pending | — |

## Owner rulings taken at CP-1 (2026-09-22)

These are decisions, not recommendations. They are not re-litigated by a later phase.

| Ruling | Decision | Consequence |
|---|---|---|
| **O1** — `events-frames-taint-§1` forbids private event frames, but `slash-commands-§7` and `testing-§1` both presuppose they exist | **Reading B** — carve out, by name, a private `CreateFrame` whose only job is `RegisterUnitEvent` for a named unit, with the three conditions three repos independently arrived at. The boss-mod-scale hand-rolling the MUST NOT was aimed at stays forbidden. | Retires 3 `Documented deviations` rows rather than adding 2 more. The wrapper was **not** taken as a LibKa0s extraction. |
| **O2** — `packaging`'s `.pkgmeta` ignore template is unconditional while its own strong form binds only what is present | **Reading A** — the strong form governs. `.claude`/`.superpowers` get the treatment `tools/` already has; the list is a template whose entries bind only when the entry exists. | 2 repos owe a one-line removal. `AUDIT.md:210-212` must gate all three the same way. |
| **O3** — nothing gates the `.gitattributes` body; 12 of 14 repos miss a MUST line | **Reading 1** — the collection is non-compliant. Gate it in the kit, then fix the twelve. | A kit gate (second case in `test_eol.lua`) plus twelve one-line commits. |
| **Batch** — the twelve non-ruling proposals | **All four groups accepted**: the 5 kit gates, the 3 client-behaviour rules, the 2 bus-naming rules, and the self-naming file header as a SHOULD. | Rollout debt lands in Phases 4–6. |

**Deferred, not rejected:** C8-F03's second half — whether an unlock/move anchor earns a SHOULD that it
must be the library's drag handle rather than a hand-built one. Its factual half (naming the shipped file
in `library-stack`) is applied; the SHOULD is recorded in `open-evolutions.md` with its evidence so the
next harvest finds a strengthened case rather than starting over.

## Rules the run holds itself to

- **Phase 1 is read-only on every repo but `WowAddonStandards`.** Not one byte written to an addon
  during the harvest — the evidence has to stay independent of the argument being built from it.
- **Never edit a frozen bundle** — `docs/audits/<date>/`, `docs/reviews/<date>/`,
  `docs/automated-tests/<stamp>/`, `harvests/<date>/` — in any repo, for any reason.
- **Green gate before every commit** in an addon or in LibKa0s: the headless harness and lint, both
  clean, run through the bounded runner at
  `/home/tushar/.claude/wow-addon/bin/ka0s-bounded` (a machine hook refuses an unbounded run).
- **No version bump** in any addon without an explicit instruction. The standard's own version and
  LibKa0s's are bumped by their phases, which is what those phases are for.
- **No merge, no push, in any repo.**
- **Deviation discipline.** A change that would deviate from the standard stops and is flagged, never
  silently made and never silently "fixed" to match.
- **Scratch discipline.** Every workflow task writes scratch under its own `scratchpad/<task-id>/`
  and never runs another task's scripts.
