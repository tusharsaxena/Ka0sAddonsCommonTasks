# Suite sweep 2026-09-22 — harvest, re-vendor standards, re-vendor LibKa0s + adoption

**Plan of record.** This file is the resume point. Read it first; keep it current. Every phase ends at
a committed checkpoint, so the run can stop anywhere and pick up from the ledger below.

## Current position

> **Phase 0 complete — branches cut, plan committed. Phase 1 (harvest sweep) not yet started.**

## How to resume

1. `cd /mnt/d/Profile/Users/Tushar/Documents/GIT/Ka0sAddonsCommonTasks && git log --oneline -5` — the
   last `CP-n` commit names the last checkpoint that landed.
2. Read **Current position** above and the **Status ledger** below.
3. Every repo in the sweep sits on branch `suite/2026-09-22-standards-sweep`. Nothing is merged and
   nothing is pushed — that is deliberate (see *Owner decisions*).
4. Resume at the first ledger row that is not `done`. Each phase's own artifacts (the harvest bundle,
   the per-addon revendor bundles) are the detailed state; this file is the index to them.

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
| 1 | Harvest sweep | WowAddonStandards (write); all others read-only | pending | — |
| CP-1 | Harvest interview | — | pending | — |
| 2 | Promote into the standard | WowAddonStandards | pending | — |
| 3 | New LibKa0s majors + tag | LibKa0s | pending | — |
| CP-3 | Major-set interview | — | pending | — |
| 4 | Re-vendor the standard | 11 addons + LibKa0s + wow-addon | pending | — |
| 5 | Re-vendor LibKa0s | 11 addons | pending | — |
| 6 | Adoption | 11 addons | pending | — |
| CP-6 | Adoption interview | — | pending | — |
| 7 | Verify and report | all | pending | — |

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
