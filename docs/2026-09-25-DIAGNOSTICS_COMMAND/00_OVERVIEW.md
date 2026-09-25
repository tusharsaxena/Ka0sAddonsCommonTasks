# Diagnostics command rollout: overview

**Status: DRAFT, not executed.** Nothing in this bundle has run. No repo has a
`feat/2026-09-25-diagnostics-rollout` branch yet, and nothing has been committed or pushed. The bundle
itself is not committed either. It is frozen once execution starts (see `../../CLAUDE.md`, "Bundle
conventions"). The owner's rulings of 2026-09-26 (`OWNER_RULINGS.md`) are applied throughout.

Built on 2026-09-25 from twelve read-only surveys: the eleven addons that
`../WowAddonStandards/standards/ADDONS.md` names, plus one of WowAddonStandards and LibKa0s together.
AuraMaster was read only through `git show feat/2026-09-25-feedback-batch8:<path>`, because another
workflow owns that working tree.

## What this is

One pass across the collection that does four things:

1. **Makes a diagnostics dump a MUST.** Today `debug-logging.md:59` says an addon "MAY support
   structured dump verbs". After this pass every Ka0s addon ships `/<slash> diagnostics` and
   `/<slash> debug diagnostics`, and nothing else that runs the report.
2. **Adds a "Reporting a bug" README section** to every addon, in the owner's exact wording.
3. **Raises `LibKa0s-DebugLog` `lib.MAX_BUFFER`** from 1500 to 5000 (3000 as the fallback). The change is
   gated on an in-game measurement of the Copy window. `BUFFER_SLACK` scales with it.
4. **Adopts the v1.59.0 DragHandle close (X) button** in ConsumableMaster and AbsorbTracker. KickCD, the
   third DragHandle host, does not adopt it (Q1 ruling). AuraMaster already uses it on its batch-8 branch.

Every addon gets **one** LibKa0s re-vendor, from a new **v1.60.0** stacked on the unmerged v1.59.0
branch. That single re-vendor carries the X button (WidgetsDragHandle 3), the diagnostics helper, the
`diagnostics` live verb and the new buffer size.

## Owner decisions this plan is built on (2026-09-25)

| # | Decision | Where it lands |
|---|---|---|
| D1 | A diagnostics dump is a MUST for every Ka0s addon. Exactly two forms, `/<slash> debug diagnostics` and `/<slash> diagnostics`, with no short alias such as `diag`. It works while the addon is disabled, writes to the debug console through the ungated sink, appends and never clears, is secret-value safe (Midnight 12.x), is capped below the console buffer, and has begin and end markers. | `02_SPEC.md` STD-01..STD-16 |
| D2 | Every README gets a "Reporting a bug" section with the owner's three steps and the closing note, verbatim apart from the slash. Step 3 names no destination and there is no GitHub link (ruled 2026-09-26). | `02_SPEC.md` STD-17, per-addon `-04` items |
| D3 | `lib.MAX_BUFFER` goes 1500 → 5000, gated on an in-game measurement of Copy open and highlight time at 5000, with 3000 as the fallback. `BUFFER_SLACK` (64) scales. The standard, LibKa0s tests, consumer pins and addon docs follow. | `02_SPEC.md` BUF-01..BUF-07, gate DR-OW-02 |
| D4 | The same pass adopts the v1.59.0 DragHandle X. Ruled 2026-09-26 (Q1): ConsumableMaster X sets `macroBar.enabled = false`; AbsorbTracker X sets `units.<unit>.enabled = false` on every bar, the player bar included; KickCD gets no X. | `02_SPEC.md` X-01..X-05, recorded as DR-OW-03 |
| D5 | AuraMaster is the reference implementation (`modules/Diagnostics.lua`, `docs/debug.md`, `settings/Slash.lua`, README "Reporting a bug", on `feat/2026-09-25-feedback-batch8`). | `01_FINDINGS.md` §4 |
| D6 | v1.59.0 exists only as a local tag on the unmerged `feat/2026-09-25-draghandle-close`. Merges and tag pushes wait for the owner. One re-vendor per addon carries everything. | Dependency order below |

## Scope

| Repo | What it gets | Milestone |
|---|---|---|
| WowAddonStandards | v2.68.0: debug-logging-§14 (the diagnostics MUST), slash-commands-§2/§7 (`diagnostics` becomes the thirteenth reserved live verb), documentation-§1 (the README section), anti-pattern #90, an AUDIT.md check, the `NEW_ADDON.md` playbook and context pack (so new addons are born with the command), the root README Status line, and the buffer number | M1 |
| wow-addon | README item citations, the live-verb enumerations in the audit and review agents, the new-addon and sync-docs README rules, and a plugin version bump (STD-25) | M1 |
| LibKa0s | v1.60.0: DebugLog 14 (buffer, slack, copy-timing flag), a new DebugLogDiagnostics secondary file (the shared report helper), Slash 16 (`diagnostics` in `LIVE_VERBS`) | M2 |
| AbsorbTracker, BankLedger, ConsumableMaster, KickCD, LootHistory, MultiMeters, PanelMaster, PartyFrameEnhanced, PrettyChat, WhatGroup | Re-vendor, diagnostics sections on the helper, both verb forms, README section, docs, tests; X on ConsumableMaster and AbsorbTracker (KickCD: none, Q1) | M3 |
| AuraMaster | Re-vendor, buffer doc ripple, and (per OW ruling Q3) migration onto the helper. It already has the command, the README section and the X. | M3, after its batch branch |
| All of the above | Standards pointer to v2.68.0, sync-docs, and the new AUDIT check run once, after the owner publishes the standard (DR-OW-07) | M4 |

Out of scope: version bumps, releases, CurseForge uploads, and any change to the layout-§1 1500-line
**file** cap. That constant shares the literal 1500 with the buffer, and the two must not be confused
(see `01_FINDINGS.md` C3).

## Milestones

| Milestone | Repos | Content | Checkpoint |
|---|---|---|---|
| **M0** | Ka0sAddonsCommonTasks | Owner rulings on `04_OPEN_QUESTIONS.md` (DR-OW-01), recorded as a commit | Rulings file committed |
| **M1** | WowAddonStandards, wow-addon | The standard v2.68.0 and its ripple. The buffer number lands last (DR-WS-05, after DR-OW-02). | Standard's own checks green; branch pushed (Q18) |
| **M2** | LibKa0s | v1.60.0 stacked on v1.59.0. The measurement (DR-OW-02) happens between DR-LK-01 and DR-LK-02. Local tag only. | Release battery green (`--release 1.60.0`), local tag `v1.60.0` |
| **M3** | 11 addons | Per addon: re-vendor, seams, diagnostics, README, docs, X where applicable | Each addon's full green gate after its last M3 item |
| **M4** | 11 addons + this repo | DR-OW-07 (owner publishes the standard and the plugin), then `revendor-standards` to v2.68.0, `sync-docs`, the AUDIT §14 check, the smoke session | Audit check passes in every addon; smoke results recorded |

## Dependency order

```
DR-OW-01 rulings ──► M1  WowAddonStandards v2.68.0 (DR-WS-01..DR-WS-04, DR-WS-06) + wow-addon (DR-WA-01)
                        │
                        │                 DR-OW-02 buffer measurement (needs DR-LK-01's timing flag, or the zero-code bench)
                        │                    │
                        ▼                    ▼
                  M2  LibKa0s  branch feat/2026-09-25-diagnostics-rollout cut from 53c141a (= local v1.59.0)
                      DR-LK-01 timing flag ─► DR-LK-02 MAX_BUFFER/SLACK ─┐
                      DR-LK-03 diagnostics helper ────────────────────┼─► DR-LK-05 docs ─► DR-LK-06 release run + local tag v1.60.0
                      DR-LK-04 Slash 16 LIVE_VERBS ───────────────────┘       (DR-WS-05 lands the same number in the standard)
                        │
                        ▼
                  M3  one re-vendor per addon from local v1.60.0, then that addon's items
                      AT BL CM KC LH MM PM PF PC WG  in any order, one repo at a time each
                      CM/AT X items also wait on DR-OW-03 (X semantics, ruled Q1; KickCD has no X)
                      AM waits on DR-OW-05 (its batch-8/9/10 branch merged), or stacks on that branch tip
                        │
                        ▼
                  DR-OW-07 owner is asked, then merges and pushes WowAddonStandards v2.68.0 + wow-addon
                        │   (revendor-standards and standards-audit read the standard from GitHub master)
                        ▼
                  M4  revendor-standards + sync-docs + AUDIT §14 check per addon; smoke session (owner)
                        │
                        ▼
                  DR-OW-06 owner merges and pushes: LibKa0s (master + v1.59.0 + v1.60.0 tags together),
                           then AuraMaster's batch branch if still open, then the addons
```

Why this order:

- **The standard comes first** so that LibKa0s's release check reads a standards pointer that already
  says v2.68.0 (LibKa0s `docs/releasing.md` step 7 reads `../WowAddonStandards/standards/STANDARDS.md`
  from the working tree; that repo must be on this plan's branch when DR-LK-06 runs).
- **LibKa0s v1.60.0 stacks on the v1.59.0 branch** rather than re-cutting v1.59.0. v1.59.0 is already
  vendored by AuraMaster's batch-8 branch, so moving that tag would break a consumer. Stacking keeps both
  tags valid, and the owner's merge (fast-forward or `--no-ff`, **never** squash or rebase) keeps both
  tag commits reachable.
- **One re-vendor per addon.** v1.59.0 has neither the buffer change nor the helper, so re-vendoring any
  addon to v1.59.0 now would mean a second re-vendor later. Every addon except AuraMaster is on v1.58.0 and
  goes straight to v1.60.0.
- **AuraMaster last.** Its diagnostics work lives on `feat/2026-09-25-feedback-batch8`, with batches 9 and
  10 committed on top (tip `d3e0118` on 2026-09-26). Its items either wait for that branch to merge into master
  (recommended) or branch from its tip at a recorded commit. See `04_OPEN_QUESTIONS.md` Q3 and Q16.

## What only the owner can do

| Gate | What | Blocks |
|---|---|---|
| **DR-OW-01** | Rule on the open questions in `04_OPEN_QUESTIONS.md` (standard version, live-while-disabled meaning, existing dump verbs, markers, cap, `docs/debug.md` trigger, and the rest) | M1 |
| **DR-OW-02** | **The buffer measurement.** Run the Copy bench at 1500, 3000 and 5000 in the live client and pick 5000 or 3000 against the thresholds in `02_SPEC.md` BUF-02 | DR-LK-02, DR-WS-05, every re-vendor |
| **DR-OW-03** | **What X does**, ruled (Q1): ConsumableMaster macro bar off; AbsorbTracker that unit's bar off on every bar, player included; KickCD no X. Recorded as a commit | DR-CM-06, DR-AT-06 |
| **DR-OW-04** | Pushing `feat/2026-09-25-diagnostics-rollout` to origin at checkpoints: **authorized** (Q18) | Nothing now |
| **DR-OW-05** | Merge AuraMaster's batch-8/9/10 branch, or approve stacking on its tip | AM items |
| **DR-OW-07** | Merge and push WowAddonStandards v2.68.0 and wow-addon to `master`. The executor **asks the owner first** (Q21) | Every `-07` |
| **DR-OW-06** | Merge every remaining branch and push the `v1.59.0` and `v1.60.0` tags | Nothing in this plan; it is the end state |
| — | Run the in-client smoke session; bump versions and cut releases | Not in this plan |

## File map

| File | What it is |
|---|---|
| `00_OVERVIEW.md` | This page |
| `01_FINDINGS.md` | Per-addon survey table, cross-cutting findings, and the standard and library findings |
| `02_SPEC.md` | Requirement IDs: the standard rule text, anti-pattern and audit check, the LibKa0s helper API, the buffer change and its gate, per-addon content contracts, and the X behavior per host (ruled, Q1) |
| `03_EXECUTION_PLAN.md` | Tasks with IDs, dependencies, gates, branch and push policy, checkpoints and the resume procedure |
| `04_OPEN_QUESTIONS.md` | Every owner decision, with options and a recommendation |
| `items.tsv` | The manifest: id, milestone, repo, title, depends_on, effort, smoke |
| `resume-state.sh` | Computes progress from git (an item is done when a commit subject starts `<ID>: `) |

## Review pass (2026-09-26, before execution)

An adversarial review checked the draft against the surveys and the owner decisions. The bundle was
unexecuted, so it was corrected in place. Changes: Q7 now recommends retiring `diag` with no hint (the
owner named `diag`); the owner gate DR-OW-07 was added because the M4 skills read the standard from GitHub;
the ripple now also covers the `NEW_ADDON.md` playbook, the root README Status line, the library-stack
recount and applicability row, the file-count sites (standard, LibKa0s `releasing.md`, AbsorbTracker docs)
and the wow-addon agents and commands (STD-25); DR-LK-03 and DR-LK-04 now wait for the rulings; there is a
LibKa0s tree pre-check; the tag-never-re-cut and v2.68.x versioning rules; smoke checks S5, S9, S10 and
S11; `resume-state.sh` lists owner gates separately; and some line citations were corrected (CM README,
Slash comments, WhatGroup Frame.lua size, the report cannot print a LibKa0s release string).

`checkpoints.tsv`, `exceptions.tsv` and `RESUME.md` do not exist yet. Create them when execution starts
(see `03_EXECUTION_PLAN.md` §7).
