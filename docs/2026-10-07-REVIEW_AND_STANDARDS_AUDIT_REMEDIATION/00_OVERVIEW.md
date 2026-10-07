# 00 — Overview

**The plan for remediating the 2026-10-07 review and standards audit of the Ka0s World of Warcraft addon
collection.**

Produced 2026-10-07. Branch in every repository: **`feat/2026-10-07-review-audit-remediation`**.

---

## Status: nothing in the plan has run yet

The documents in this directory are written in the imperative. They describe work that has not been done.

- **No work item has landed.** No commit in any repository has a subject that starts with a plan item id.
  `./resume-state.sh` is the record of progress, and it reads git.
- **Each repository carries one commit above `master`: the bundle commit.** That commit is
  `RA-00: record 2026-10-07 standards audit and review bundles`, and it adds the 10 files under
  `docs/audits/2026-10-07/` and `docs/reviews/2026-10-07/`. This repository's `RA-00` commit (`09e745b`)
  adds `01_CONSOLIDATED_FINDINGS.md`. Every tree is clean apart from this directory's untracked plan files.
- **Nothing has been pushed.** No remediation branch has an upstream.
- **No version has moved.** The standard is v2.76.1, LibKa0s's newest tag is v1.70.0, and dev-copilot is
  plugin 2.0.1. There is no `v1.71.0` tag.
- **No in-client check has been run.** `06_SMOKE_TESTS.md` is for the owner.

---

## What this is

On 2026-10-07, `/dev-copilot:wow-standards-audit` and `/dev-copilot:review` ran over fourteen repositories:
the eleven addons that `../WowAddonStandards/standards/ADDONS.md` names, LibKa0s, WowAddonStandards and
dev-copilot. The 28 frozen bundles they wrote held **290 findings** (158 from audits, 132 from reviews).

An adversarial pass then took each finding through three steps. It checked whether the finding was real,
argued that it did not need fixing, and reconciled the two. It grouped the findings into **53 clusters**
by root cause and graded each one `must`, `should`, `optional` or `no`. The results are in
`01_CONSOLIDATED_FINDINGS.md`.

The owner read that document and set the scope in `inputs/OWNER_SCOPE.md`. Every `must`, `should` and
`optional` finding is in scope, which is **251 findings**. The **39** `no` findings are out of scope:
27 are real but not worth changing, and 12 were refuted. A planner turned the 251 findings into work
items, and a critic pass fixed 25 problems in the draft. Those fixes are listed in
`plan-data/PLAN_REVIEW_RESOLUTIONS.md`. The result is **164 items in three milestones**.

`plan-data/items.json` is the single source of truth. It holds every item's spec, steps, verify block and
smoke check. `items.tsv` and the tables in `04_EXECUTION_PLAN.md` and `05_TRACEABILITY.md` are derived
from it.

---

## Reading order

| File | What it is |
|---|---|
| `00_OVERVIEW.md` | This page: scope, counts, milestones, owner gates, the state of every repository, and how to resume. |
| `01_CONSOLIDATED_FINDINGS.md` | All 290 findings by cluster, with evidence, verdict and remediation. It ends with the 27 `no` findings and the 12 refuted ones, each with its reason. |
| `02_UPSTREAM_CHANGES.md` | M1 in depth: the WowAddonStandards, LibKa0s and dev-copilot changes and what each one means for the addons. |
| `03_SPEC.md` | The end state each item must reach. It is not a schedule. |
| `04_EXECUTION_PLAN.md` | How the run works (milestones, ordering, the per-item loop, checkpoints, owner gates), then every item in a table per milestone. |
| `05_TRACEABILITY.md` | Every in-scope finding mapped to its item, and every out-of-scope finding with its reason, grouped by repository. |
| `06_SMOKE_TESTS.md` | The owner's in-client checklist for the 57 items marked `⚠`, and the LootHistory LED-P2-01..24 checks. |
| `RESUME.md` | How a fresh session picks the run up from any point. |
| `items.tsv` | The flat manifest `resume-state.sh` reads: id, milestone, repo, title, depends_on, effort, smoke, finding ids. |
| `resume-state.sh` | Reports from git which items have landed, per milestone, and prints the `RESUME` line. |
| `checkpoints.tsv` | One line per milestone that passed its checkpoint and was pushed, with the evidence. Empty so far. |
| `exceptions.tsv` | Items that land with no commit, each with a command that proves the claim. Empty so far. |
| `inputs/` | What planning drew on: `OWNER_SCOPE.md`, `verified_findings.json`, the per-repo raw findings, `clusters.json` and the per-cluster verdicts. |
| `plan-data/` | `items.json` (the plan), `PLAN_REVIEW_RESOLUTIONS.md`, the per-repo planner output in `items/`, the executor scripts in `tools/` (`execute_milestone.js`, `next_args.py`, `assemble.py`) and finished run results in `runs/`. |

---

## Scope

### Repositories

- **Upstream:** WowAddonStandards, LibKa0s and dev-copilot.
- **Addons:** AbsorbTracker, AuraMaster, BankLedger, ConsumableMaster, KickCD, LootHistory, MultiMeters,
  PanelMaster, PartyFrameEnhanced, PrettyChat and WhatGroup.
- **Tracking:** Ka0sAddonsCommonTasks, which holds this directory and nothing else for this run.

### The owner's rulings (`inputs/OWNER_SCOPE.md`)

1. **In scope:** every `must`, `should` and `optional` finding, 251 in all. The 39 `no` findings stay
   recorded in `01_CONSOLIDATED_FINDINGS.md` and nothing is done for them.
2. **Two downgrades.** `MM-A-03` (one malformed `(architecture-4)` citation) and `DC-A-05` (the audit
   agent misses WowAddonStandards' `docs/ARCHITECTURE.md` register) move from `must` to `should`.
   `LH-R-03` (LootHistory's LED-P2-01..24 in-client checks) is the owner's to run. The plan lists them in
   `06_SMOKE_TESTS.md`, and no agent records a result for them or marks them passed.
3. **Order:** upstream first, then the LibKa0s re-vendor, then the addon items.
4. **Standing guidelines:** decide autonomously and ask only when necessary; keep the plan resumable and
   checkpointed; use one feature branch per repository and commit incrementally; push the feature branches
   at milestone checkpoints; never merge, push a tag, bump an addon version or cut a release without the
   owner's go-ahead; after the approved merge, delete every branch, stash and worktree the run created.
5. **Derived rulings:**
   - The new LibKa0s release is **v1.71.0**. LK-12 tags it **locally** on its final commit. The tag is
     pushed only on the owner's go-ahead, and the addons re-vendor from the local tag.
   - Re-vendoring is mechanical. Each RV item copies both payloads whole, rolls the provenance line and
     writes the `docs/revendor/` bundle, plus one span bundle for the v1.69.0 and v1.70.0 re-vendors that
     were never recorded. Adoption candidates the plan does not require are listed as "not adopted in this
     run". There is no adoption interview and no issue filing.
   - Each addon's standards reference (TOC `X-Standard`, README badge, CLAUDE.md) rolls to the standard
     version this run produces, **v2.77.0**, read from WowAddonStandards' feature branch.
   - The only GitHub writes are closing, relabelling or commenting on issues that a finding names. They
     are spaced out.

### Decisions from the plan review

The critic pass (`plan-data/PLAN_REVIEW_RESOLUTIONS.md`) changed the plan in these ways:

- **DC-15 was added**, and DC-06 now covers only the ARCHITECTURE.md hub. DC-15 carries the handoffs from
  the standard into dev-copilot's audit agent and specs: the changelog's new home (H-01), the check (e)
  quoting, `check-standard.sh` in sync-docs, and the standard version in README.
- **Four items were added for consistency: BL-05, CM-09, PF-06 and WG-07.** Each removes the same dead
  bare-global `GetAddOnMetadata` fallback that LK-06, MM-07 and PM-09 remove (cluster C27). No finding
  names those four sites, so this is a small addition beyond the finding list. The owner can drop the
  four items without affecting any traced finding.
- **LH-08 was split into two items.** LH-08 moves BrowserTableGroup and LH-18 moves BrowserWidgets. Each
  is a pure move.
- **LK-12 and LH-14 each make two commits.** The first is subject `<ID> (1/2): …`, which the id regex does
  not match, so the item counts as landed only once its final commit exists.
- **Every re-vendor item must end green.** If a re-vendor produces a behavioural red, the item stops.
- **Cross-repo edges were added:** LK-07 and DC-09 depend on WS-07, LK-12 depends on WS-11, and PC-06
  depends on LH-01.

### Out of scope

- **Addon releases and version bumps.** No TOC version, README version badge, Version History row or
  release tag moves. The only versions this run moves are the standard (v2.77.0) and LibKa0s (v1.71.0,
  local tag).
- The 39 `no` findings, listed with reasons in `05_TRACEABILITY.md`.
- Frozen bundles under any repository's `docs/audits/`, `docs/reviews/`, `docs/automated-tests/`,
  `docs/perf-analysis/` and `docs/revendor/`. Their evidence is dated and never rewritten.

---

## Headline numbers

| | |
|---|---|
| Repositories reviewed and audited | **14**: 11 addons, LibKa0s, WowAddonStandards, dev-copilot |
| Bundles consumed | **28** (14 audit + 14 review) |
| Findings raised | **290** (158 audit, 132 review) |
| Clusters | **53** |
| In scope | **251**: must 10 · should 161 · optional 80 (after the two owner downgrades) |
| Out of scope | **39**: 27 real but not worth changing, 12 refuted |
| Work items | **164**: M1 38 · M2 11 · M3 115 |
| Findings mapped to an item | **251 / 251**, each to exactly one item (`05_TRACEABILITY.md`) |
| Items with no finding id | **21**: the closing and release items, the LootHistory complexity slices and the four C27 parity items |
| Effort | 102 S · 60 M · 2 L |
| Items with an in-client smoke check (`⚠`) | **57**: M1 4 · M2 6 · M3 47 |
| Versions moved | standard **v2.77.0**, LibKa0s **v1.71.0** (local tag) |
| Addon releases | **0** |

### In-scope findings by severity, after verification

| high | medium | low | info | total |
|---|---|---|---|---|
| 5 | 29 | 187 | 30 | **251** |

### Items per repository

| Repo | M1 | M2 | M3 | Total |
|---|---|---|---|---|
| WowAddonStandards | 11 | | | 11 |
| LibKa0s | 12 | | | 12 |
| dev-copilot | 15 | | | 15 |
| AbsorbTracker | | 1 | 10 | 11 |
| AuraMaster | | 1 | 11 | 12 |
| BankLedger | | 1 | 6 | 7 |
| ConsumableMaster | | 1 | 10 | 11 |
| KickCD | | 1 | 11 | 12 |
| LootHistory | | 1 | 19 | 20 |
| MultiMeters | | 1 | 11 | 12 |
| PanelMaster | | 1 | 13 | 14 |
| PartyFrameEnhanced | | 1 | 7 | 8 |
| PrettyChat | | 1 | 9 | 10 |
| WhatGroup | | 1 | 8 | 9 |
| **all** | **38** | **11** | **115** | **164** |

---

## Milestone map

| M | What | Items | Starts when |
|---|---|---|---|
| **M1** | Upstream. WowAddonStandards opens and closes v2.77.0 (WS-01…WS-11). LibKa0s fixes its findings and cuts v1.71.0 with kit revision 38, tagged locally by LK-12 (LK-01…LK-12). dev-copilot fixes its hooks, runner, docs and command specs (DC-01…DC-15). | 38 | now |
| **M2** | Re-vendor LibKa0s v1.71.0 from the local tag into all eleven addons (RV-AT…RV-WG), each with its `docs/revendor/` bundles. | 11 | LK-12 has landed and the local `v1.71.0` tag exists |
| **M3** | Addon items, serial within a repository and parallel across repositories. Each addon closes with its `<AB>-STD` item, which rolls the standards reference to v2.77.0 and syncs the docs. | 115 | that addon's RV item |

`04_EXECUTION_PLAN.md` has the rules and the item tables.

---

## What waits for the owner

Execution stops at each of these points and does not work around them.

1. **Merging.** No `feat/2026-10-07-review-audit-remediation` branch is merged to `master` without the
   owner's go-ahead. Once approved, `/dev-copilot:finalize` merges with `--no-ff` in dependency order:
   WowAddonStandards, LibKa0s, dev-copilot, the addons, then this repository.
2. **Pushing the `v1.71.0` tag.** It stays local until the LibKa0s merge is approved. An addon branch on
   origin may name v1.71.0 before the tag is on origin. That is acceptable because the branch is unmerged.
3. **Deleting dev-copilot's stale `origin/main` (DC-14).** This happens only inside the approved finalize.
   Until then `exceptions.tsv` carries a "deferred" row for it.
4. **In-client smoke checks.** The 57 `⚠` items and LootHistory's LED-P2-01..24 checks need a person at a
   client. Those items are code-complete when they land, but they are verified in the client only once the
   owner records a result in `06_SMOKE_TESTS.md`.
5. **Releases and version bumps.** Neither is part of this plan.
6. **Cleanup after the merge.** Delete every remediation branch, local and on origin, and every stash and
   worktree the run created.

---

## The state of every repository, as observed

Read-only `git`, run while this overview was written.

| Repo | Branch | HEAD | Above `master` | Tree | Version now |
|---|---|---|---|---|---|
| WowAddonStandards | `feat/2026-10-07-review-audit-remediation` | `63ccc5c` | 1 (`RA-00` bundles) | clean | standard v2.76.1 |
| LibKa0s | same | `b263c24` | 1 (`RA-00` bundles) | clean | tag v1.70.0 |
| dev-copilot | same | `d90b974` | 1 (`RA-00` bundles) | clean | plugin 2.0.1 |
| AbsorbTracker | same | `e83325b` | 1 (`RA-00` bundles) | clean | vendors LibKa0s v1.70.0 |
| AuraMaster | same | `20a39d6` | 1 (`RA-00` bundles) | clean | vendors LibKa0s v1.70.0 |
| BankLedger | same | `3094a0a` | 1 (`RA-00` bundles) | clean | vendors LibKa0s v1.70.0 |
| ConsumableMaster | same | `9b056f6` | 1 (`RA-00` bundles) | clean | vendors LibKa0s v1.70.0 |
| KickCD | same | `9913604` | 1 (`RA-00` bundles) | clean | vendors LibKa0s v1.70.0 |
| LootHistory | same | `aaee6e1` | 1 (`RA-00` bundles) | clean | vendors LibKa0s v1.70.0 |
| MultiMeters | same | `349e319` | 1 (`RA-00` bundles) | clean | vendors LibKa0s v1.70.0 |
| PanelMaster | same | `9e41cd9` | 1 (`RA-00` bundles) | clean | vendors LibKa0s v1.70.0 |
| PartyFrameEnhanced | same | `1b9f196` | 1 (`RA-00` bundles) | clean | vendors LibKa0s v1.70.0 |
| PrettyChat | same | `caa366b` | 1 (`RA-00` bundles) | clean | vendors LibKa0s v1.70.0 |
| WhatGroup | same | `0f7afcb` | 1 (`RA-00` bundles) | clean | vendors LibKa0s v1.70.0 |
| Ka0sAddonsCommonTasks | same | `09e745b` | 1 (`RA-00` findings) | this directory's plan files untracked | — |

None of the remediation branches has an upstream.

When the passes measured them, every repository had lint at 0/0 and no failing test. Three addons had
functions above CCN 15: AuraMaster one (`logCandidates`, CCN 18), BankLedger one (`LT.GroupEntries`,
CCN 16) and LootHistory 26. Those block each addon's next release tag. AM-05, BL-01 and LH-09…LH-14 clear
them. The full per-repository figures are in `01_CONSOLIDATED_FINDINGS.md` § Suite state.

---

## How to resume

```
./resume-state.sh          # per-milestone counts, the RESUME line, unreviewed items, dirty trees, branch check
./resume-state.sh -v       # also every remaining id
./resume-state.sh M3       # one milestone
```

**Git is the only state.** An item is done when a commit whose subject starts `<ID>: ` exists in the
repository that owns it. One commit may carry several ids, as in `LK-01 + LK-02: …`. An item is
reviewed when one of its commits carries a `refs/notes/ka0s-review` note. Items that land with no commit
go in `exceptions.tsv` with a command that proves the claim. `RESUME.md` has the full procedure: cleaning
up an interrupted item, building the executor's arguments, relaunching, and running a milestone checkpoint.

Never mark progress by editing the plan. The record is the commits, the review notes, `exceptions.tsv`
and `checkpoints.tsv`.
