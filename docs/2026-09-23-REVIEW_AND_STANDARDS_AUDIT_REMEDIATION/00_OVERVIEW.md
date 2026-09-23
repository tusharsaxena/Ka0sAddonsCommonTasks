# 00 — Overview

**The consolidated spec and plan for remediating the 2026-09-23 review and standards audit of the Ka0s
World of Warcraft addon collection.**

Produced 2026-09-23. None of the work in this directory has been executed yet.

---

## NOTHING HERE HAS BEEN RUN

Read this first. The documents that follow are written in the imperative, and a quick skim makes them
look like a changelog.

- **No repository has been changed beyond its branch and its bundle commit.** Every repository this plan
  touches is on `feat/2026-09-23-review-audit-remediation`. LibKa0s and the eleven addons each carry
  exactly one commit above `master`, which records the 2026-09-23 review and audit bundles. That commit
  adds 10 files under `docs/reviews/2026-09-23/` and `docs/audits/2026-09-23/`. WowAddonStandards and
  wow-addon have the branch with no commits on it. See *The state of every repository* below.
- **No work item has landed.** `./resume-state.sh` reports `TOTAL 0/384 items landed`. No commit's subject
  starts with an item id. There is no `v1.56.0` tag, standards v2.65.0, plugin 2.4.0 or re-vendor.
- **Nothing has been pushed.** No branch has an upstream, and origin has none of the remediation branches.
- **No step in `06_SMOKE_TESTS.md` has been performed.** No client has been launched for this plan.

Suite figures below were **observed** when the review and audit passes re-ran each repository's suites.
They were measured, and measuring a suite does not change a repository.

---

## What this is

Twelve repositories were each reviewed (`/wow-addon:review`) and audited (`/wow-addon:standards-audit`)
on 2026-09-23: LibKa0s and the eleven addons that `WowAddonStandards/standards/ADDONS.md` names. That
produced twenty-four frozen bundles. A separate adversarial pass then re-verified every finding against
the code. That pass rejected **3** of the **439** findings and corrected several more. The **436**
survivors were clustered across the collection into 47 clusters. A planner turned them into work items,
a reconcile pass matched upstream items to what each consumer needs, and three independent critics
reviewed the draft plan. All 24 issues the critics raised are resolved in `plan-data/items.json`. The
decisions are in `plan-data/PLAN_REVIEW_RESOLUTIONS.md`.

`plan-data/items.json` is the single source of truth. It holds the final 384 items after the reconcile
results and the plan-review amendments, with the amendments listed in its `amendment_log` field.
`items.tsv`, `05_TRACEABILITY.md` and the item tables in `04_EXECUTION_PLAN.md` are generated from it.

### File map

| File | What it is |
|---|---|
| `00_OVERVIEW.md` | This page: scope, owner rulings, the state of every repository, the milestone map, owner gates and how to resume. |
| `01_CONSOLIDATED_FINDINGS.md` | All 436 verified findings grouped by cluster and repository, with evidence, rule and the item each is planned in. It also lists the 3 rejected findings and why. |
| `02_UPSTREAM_CHANGES.md` | Milestone 1 in depth: every WowAddonStandards, LibKa0s and wow-addon change, its rationale and its blast radius on the consumers. |
| `03_SPEC.md` | The target end state: upstream, after the re-vendor, and per cluster. Acceptance criteria and non-goals. It is not a schedule. |
| `04_EXECUTION_PLAN.md` | The rules (milestone map, standing verification, commit/branch/push policy, checkpoints) followed by all 384 items with change, tests, verify command, dependencies and effort. No dates. It is assembled, never hand-edited: `plan-data/04_head.md` (the rules) followed by `plan-data/04_tables.md` (the item tables `gen_docs.py` generates from `items.json`). |
| `05_TRACEABILITY.md` | Every finding mapped to its cluster, items and milestone, plus every owner-scope issue mapped to its items. Coverage: 436/436. Generated, never hand-edited. |
| `06_SMOKE_TESTS.md` | The in-client checklist: every `⚠` item's check batched into sessions, each step with an observable pass condition. |
| `items.tsv` | The flat manifest `resume-state.sh` reads: id, milestone, repo, title, depends_on, effort, smoke, finding ids, issue refs. |
| `resume-state.sh` | Reports from git which items have landed, per milestone, and prints the `RESUME:` line. |
| `exceptions.tsv` | **Does not exist yet.** Create it when an item legitimately lands with no commit. Each row is `<ID>\t<reason>`, and the reason must include a command a reader can run to check the claim. |
| `inputs/` | What the plan was built from. `verified_findings.json` and `findings/<Repo>.json` (plus `_rejected.json` and `_upstream_routed.json`) hold the verified findings. `OWNER_SCOPE.md` holds the owner's scope and rulings. |
| `plan-data/` | The planner's working data. `items.json` is the final plan. `PLAN_REVIEW_RESOLUTIONS.md` records the critics' decisions. `04_head.md` and `04_tables.md` are the two halves `04_EXECUTION_PLAN.md` is assembled from (head, then tables; see `tools/README.md`); edit the head or regenerate the tables, then reassemble. `raw_plan.json`, `unmatched_followups.json` and `docs_workflow_output.json` are intermediate output. |

---

## Scope

### The roster

LibKa0s plus the eleven addons: **AbsorbTracker · AuraMaster · BankLedger · ConsumableMaster · KickCD ·
LootHistory · MultiMeters · PanelMaster · PartyFrameEnhanced · PrettyChat · WhatGroup**.

**WhoGotLoots and BuffTextNotifications are not Ka0s addons.** They are not in `ADDONS.md` and do not
vendor LibKa0s. They were not read or counted, and nothing here touches them.

This plan also changes **WowAddonStandards** (v2.64.0 → v2.65.0) and the **wow-addon** plugin
(2.3.0 → 2.4.0), and it is tracked in **Ka0sAddonsCommonTasks**. None of those three was reviewed or
audited this cycle. They are changed because upstream-routed findings were filed against them: 50 of
the 436 findings route upstream.

### The owner's scope (`inputs/OWNER_SCOPE.md`)

1. **Every finding, all severities**, from both passes across all twelve repositories.
2. **Upstream first.** Every LibKa0s, WowAddonStandards and wow-addon change lands, and v1.56.0 is tagged,
   before any addon implementation item.
3. **Re-vendor the whole LibKa0s payload** (`libs/LibKa0s/` and `tests/_kit/`) from the new tag into all
   eleven addons.
4. **Build the twelve open enhancement issues filed 2026-09-23.** They map to items as follows:

| Issue | What | Item(s) |
|---|---|---|
| AuraMaster#21 | Adopt LibKa0s-Schema-1.0 in `settings/Schema.lua` | LK-22, AM-15 |
| AuraMaster#16 | Peel Dispel Colors out of `settings/GeneralSpells.lua` | AM-23 |
| AuraMaster#17 | Split user-category suites out of `tests/test_database.lua` | AM-24 |
| AuraMaster#18 | Split user-category suites out of `tests/test_filtercompiler.lua` | AM-25 |
| AuraMaster#19 | Split category-editing suites out of `tests/test_pages_general.lua` | AM-26 |
| ConsumableMaster#39 | Adopt LibKa0s-Schema-1.0 for the settings write seam | LK-22, CM-17 |
| KickCD#22 | Adopt LibKa0s-Schema-1.0 for the settings schema runtime | LK-22, KC-18 |
| MultiMeters#52 | Adopt LibKa0s-Schema-1.0 path primitives, registry, bulk bracket | LK-22, MM-14 |
| PanelMaster#52 | Wrap bus message constants in LibKa0s-Bus-1.0's Catalog | PM-12 |
| PartyFrameEnhanced#14 | Adopt LibKa0s-Schema-1.0 once a library-less build can write composed rows | WS-02, LK-23, PF-11 |
| PrettyChat#18 | Move `Schema.ResetRows` onto `BulkRun` and `BulkAdd` | PC-05 |
| WhatGroup#22 | Adopt LibKa0s-Schema-1.0 | WS-02, LK-18, LK-23, WG-12 |

The seven issues closed as `state:will-not-do` stay declined and are not built: AbsorbTracker #31,
AuraMaster #20, BankLedger #20, PanelMaster #53, PrettyChat #16 and #17, WhatGroup #21.

### The owner's rulings

- **WhatGroup#22.** Adopting the Schema seam breaks the degraded (library-less) `enable` and `test` verbs.
  The owner accepted this as a known gap. WG-12 carries it out: on a library-absent load, `/wg enable`,
  `/wg disable` and `/wg test` raise no Lua error and print the library-absent line instead. WhatGroup
  deliberately declares no `writeThrough` list (route (b) under WS-02).
- **PartyFrameEnhanced#14.** Adopt once a library-less build can still write its composed rows. The
  library work that makes this possible is in the plan: WS-02 rules on it, LK-23 adds the Schema
  `writeThrough` path list, and PF-11 adopts with `writeThrough = {'enabled','locked'}`.

### Decisions from the plan review (`plan-data/PLAN_REVIEW_RESOLUTIONS.md`)

These decisions change the plan's shape, and every document in this directory follows them:

1. **No minimap SavedVariables migration and no schema-version bump for it.** WS-06 renames the minimap
   row's schema/CLI path from `…minimap.hide` to `…minimap.shown`. The stored value stays LibDBIcon's
   `db.global.minimap.hide`, so a player's choice cannot be lost. PF-26 and PC-27 were dropped, and the
   migration halves of LH-13 and WG-11 were not merged. The owner never asked for them. Instead, every
   addon's rename item carries the same test-first carry-over check. A legacy `hide = true` must read as
   `shown = false`, the button must stay hidden, `minimapPos` must survive, and no `shown` key may ever be
   stored.
2. **Fixes owed before a re-vendor land before it, in M2.** AT-01, AM-01, AM-02, BL-01, BL-02, CM-01,
   KC-01 and WG-01 each depend on LK-33, and their addon's RV item depends on them. Each must pass on both
   the v1.55.0 payload and the v1.56.0 dry run. The RV commit itself stays copy-only, and is green or lists
   its reds in its commit body.
3. **Each re-vendor writes its bundle by hand.** The installed plugin is fetched from GitHub, so WA-01's
   amended `/wow-addon:revendor-libka0s` cannot be run until the owner merges wow-addon. Every RV item
   therefore writes `docs/revendor/2026-09-23-v1.56.0/` by hand, following the **local**
   `../wow-addon/commands/revendor-libka0s.md` at the WA-01 commit. Line 1 of `01_DELTA.md` is exactly
   `Delta: LibKa0s v1.55.0 -> v1.56.0`. Every RV item depends on WA-01.
4. **The eleven `/wow-addon:revendor-standards` items form M4 and are owner-gated.** AT-26, AM-35, BL-25,
   CM-31, KC-27, LH-36, MM-32, PF-25, PM-16, PC-26 and WG-30 run only after the owner merges and pushes
   WowAddonStandards v2.65.0. Each checks that gate before it starts and stops if the gate is not met. The
   `<AB>-DOCS` items no longer wait on them.
5. **v1.56.0 carries LK-03.** LK-33, which cuts the tag, depends on LK-03, the AceDB fake fidelity change.
   WA-02 and WA-03 are plugin-only and no RV item depends on them. They stay in M1, and M2 starts only
   once M1 is complete.

The critics' smaller corrections are written into the item text and marked `PLAN-REVIEW CORRECTION`.
Among them: under LK-28, when `disabledFor` answers true the notice is drawn **above** the rows, which
render disabled rather than being replaced, and host `tabs` can take a schema group's place, so AM-17
adopts with no change in behaviour. The span bundles are normalized to WS-01's line-1 grammar. MM-14
uses dot syntax for its shims. Explicit dependency edges were added where an order was only implied.

### Out of scope

- **Addon releases and version bumps.** No addon changes its TOC version, README badge or Version History,
  and no `/wow-addon:bump-version` runs. Every `<AB>-DOCS` item says "no version bump, no tag: the owner
  decides." The only versions this plan moves are upstream: LibKa0s v1.56.0, standard v2.65.0 and plugin
  2.4.0. **Nothing here reaches a player until the owner cuts releases separately.**
- The frozen bundles under each repository's `docs/audits/`, `docs/reviews/`, `docs/automated-tests/`,
  `docs/perf-analysis/` and `docs/revendor/`. Their evidence is dated and never rewritten. A misstatement
  in one is corrected in the next bundle.
- WhoGotLoots and BuffTextNotifications.

---

## The state of every repository, as observed

Read-only `git`, run while this overview was written:

| Repo | Branch | HEAD | Above default branch | Tree | Latest tag |
|---|---|---|---|---|---|
| LibKa0s | `feat/2026-09-23-review-audit-remediation` | `ab6404d` | 1 (bundles, 10 files) | clean | `v1.55.0` |
| AbsorbTracker | same | `f4b61a6` | 1 (bundles, 10 files) | clean | `1.10.0-release` |
| AuraMaster | same | `0ede122` | 1 (bundles, 10 files) | clean | none |
| BankLedger | same | `24ede85` | 1 (bundles, 10 files) | clean | `1.1.0-release` |
| ConsumableMaster | same | `38f3901` | 1 (bundles, 10 files) | clean | `1.6.2-release` |
| KickCD | same | `f28df97` | 1 (bundles, 10 files) | clean | `1.3.0-release` |
| LootHistory | same | `36072e5` | 1 (bundles, 10 files) | clean | `1.3.0-release` |
| MultiMeters | same | `888e26f` | 1 (bundles, 10 files) | clean | `1.0.1-release` |
| PanelMaster | same | `7183100` | 1 (bundles, 10 files) | clean | `1.1.1-release` |
| PartyFrameEnhanced | same | `4c2a7e6` | 1 (bundles, 10 files) | clean | `1.0.1-release` |
| PrettyChat | same | `e561b79` | 1 (bundles, 10 files) | clean | `1.5.0-release` |
| WhatGroup | same | `7177411` | 1 (bundles, 10 files) | clean | `1.4.0-release` |
| WowAddonStandards | same | `e68795f` | 0 (branch only) | clean | none (`STANDARDS.md:1` reads v2.64.0) |
| wow-addon | same | `82095ac` | 0 (branch only) | clean | none (plugin 2.3.0) |
| Ka0sAddonsCommonTasks | same | `525f87c` | 2 above `main` (`inputs/` for this plan, plus an unrelated 2026-09-22 smoke record) | this directory's plan files untracked | none |

Every repository's default branch is `master`, except Ka0sAddonsCommonTasks, which uses `main`. None
of the remediation branches has an upstream.

WS-01 and WA-01 each open with "PRE: create the branch". WowAddonStandards and wow-addon are already on
it, so that step is already done.

### The suites, as the passes measured them

Each pass measured at the commit just before its repository's bundle commit, on standard v2.64.0 with
LibKa0s v1.55.0 vendored (kit revision 25). Every run went through
`~/.claude/wow-addon/bin/ka0s-bounded` by absolute path.

| Repo | lint | tests (passed) | perf | lizard |
|---|---|---|---|---|
| LibKa0s | 0/0, 81 files | 1484 (+1 declared skip) | n/a (library) | 0 warnings, max CCN 15 |
| AbsorbTracker | 0/0, 61 files | 710 | present, all assertions held | 0 warnings, max CCN 14 |
| AuraMaster | 0/0, 110 files | 1296 | present, 10 scenarios | **2 warnings**: `Cat.SyncUserCategories` CCN 25, `renderCategories` CCN 16 |
| BankLedger | 0/0, 71 files | 1017 | none (performance-§12 exemption) | 0 warnings, max CCN 15 |
| ConsumableMaster | 0/0, 116 files | 998 | present, 5 scenarios | 0 warnings, max CCN 15 |
| KickCD | 0/0, 101 files | 1050 | present, 6 scenarios | 0 warnings, max CCN 15 |
| LootHistory | 0/0, 65 files | 858 | none (performance-§12 exemption) | 0 warnings, max CCN 15 |
| MultiMeters | 0/0, 125 files | 1948 | present, 15 scenarios | 0 warnings, max CCN 15 |
| PanelMaster | 0/0, 60 files | 884 | none (ratified deviation) | 0 warnings, max CCN 15 |
| PartyFrameEnhanced | 0/0, 71 files | 289 | present, 9 scenarios | 0 warnings, max CCN 14 |
| PrettyChat | 0/0, 48 files | 438 | none (performance-§12 exemption) | 0 warnings, max CCN 14 |
| WhatGroup | 0/0, 48 files | 727 | present, 8 scenarios | 0 warnings, max CCN 14 |

Every suite is green, and AuraMaster's two lizard warnings are the only complexity-gate failures in
the collection. Kit revision 26 changes kit behaviour: `CreateFrame` starts shown, the AceDB fake raises,
`EventRegistry` callbacks are recorded, lone CRs are caught and the prose gate reaches store roots. Some
addon suites **will** go red on the new payload. The owner's standing ruling is that a red exposes a real
bug. Each copy-only RV commit is green or lists its reds in its commit body. The M2 pre-fixes aim to make
it green, each addon's M3 items clear any remaining red, and the addon is green again at the latest by
its `<AB>-DOCS` item.

---

## Headline numbers

| | |
|---|---|
| Repositories reviewed and audited | **12**: LibKa0s + 11 addons |
| Bundles consumed | **24** (12 review + 12 audit) |
| Findings raised / rejected / in scope | **439 / 3 / 436** |
| Clusters | **47** |
| Findings routed upstream | **50** |
| Work items | **384**: M1 44 · M2 19 · M3 310 · M4 11 |
| Findings mapped to an item | **436 / 436** (`05_TRACEABILITY.md`) |
| Effort | 252 S · 121 M · 11 L |
| Items marked `⚠` (in-client smoke step) | **168**: M1 17 · M2 2 · M3 149 · M4 0 |
| Upstream versions cut | LibKa0s **v1.56.0** (local tag), standard **v2.65.0**, plugin **2.4.0** |
| Addon releases cut | **0** |

### Severity, after verification

| critical | high | medium | low | info | total |
|---|---|---|---|---|---|
| 0 | 16 | 45 | 311 | 64 | **436** |

`0 + 16 + 45 + 311 + 64 = 436` ✓. The per-repository split is in `01_CONSOLIDATED_FINDINGS.md` § Totals.

The 3 rejected findings are AuraMaster-A-19, MultiMeters-A-08 and PanelMaster-A-20. The reasons are at
the end of `01_CONSOLIDATED_FINDINGS.md`.

---

## Milestone map

| M | What | Items | Repos | Starts when |
|---|---|---|---|---|
| **M1** | Upstream: WowAddonStandards v2.65.0 (WS-01…08), LibKa0s v1.56.0 (LK-01…33, LK-33 cuts the **local** tag), wow-addon plugin 2.4.0 (WA-01…03) | 44 (8 + 33 + 3) | WowAddonStandards, LibKa0s, wow-addon | now |
| **M2** | The pre-re-vendor fixes (AT-01, AM-01, AM-02, BL-01, BL-02, CM-01, KC-01, WG-01), then a whole-payload re-vendor of v1.56.0 into all eleven addons (RV-AT … RV-WG), each writing its `docs/revendor/2026-09-23-v1.56.0/` bundle by hand | 19 (8 + 11) | all eleven addons | M1 complete |
| **M3** | Addon remediation: every remaining finding, consumer follow-up and owner-scope issue, per addon, closing with each addon's `<AB>-DOCS` item | 310 | all eleven addons (BL 23 · PF 25 · MM 32 · LH 36 · AT 25 · PM 24 · PC 26 · WG 29 · CM 30 · AM 33 · KC 27) | that addon's RV item |
| **M4** | `/wow-addon:revendor-standards` against v2.65.0, one per addon | 11 | all eleven addons | **owner merges and pushes WowAddonStandards**, and that addon's `<AB>-DOCS` item |

The full rules are in `04_EXECUTION_PLAN.md`: ordering, standing verification, one commit per item,
branch and push policy, and checkpoints.

---

## What is gated on the owner

Nothing in this list happens without the owner's explicit go-ahead. Execution stops at each gate and
does not work around it.

1. **Merging each repository's branch.** No `feat/2026-09-23-review-audit-remediation` is merged to
   `master` (or `main`) without approval, in any of the fifteen repositories. Branches are pushed to
   origin at the end of each milestone, which is not the same as merging them. Merge the upstream repos
   before the addons, because every addon's re-vendor names v1.56.0.
2. **Pushing the `v1.56.0` tag.** LK-33 creates it on the LibKa0s branch **locally**. The M2 re-vendors
   and each consumer's `test_vendor_sync` resolve it from the local sibling checkout. The tag is pushed only
   when the owner approves the LibKa0s merge, after Session L in `06_SMOKE_TESTS.md` (the pre-merge gate).
   An addon branch whose `CLAUDE.md` provenance line names v1.56.0 may be on origin before the tag is.
   That is acceptable: the branch is unmerged, and the tag is one push away.
3. **Merging and pushing WowAddonStandards (v2.65.0) before M4.** `/wow-addon:revendor-standards` and the
   review and audit agents fetch the standard from GitHub. M4 cannot start until
   `gh api repos/tusharsaxena/WowAddonStandards/contents/standards/STANDARDS.md --jq .content | base64 -d | grep -m1 v2.65.0`
   returns a match. The three-place reference is never hand-edited from the local sibling.
4. **Merging wow-addon.** The installed plugin comes from GitHub, so the amended
   `/wow-addon:revendor-libka0s` (WA-01) and plugin 2.4.0 reach the installed commands only after this
   merge. The plan does not depend on it: the RV items follow the local command file.
5. **The in-client smoke sessions.** `06_SMOKE_TESTS.md` requires a person at a client. The `⚠` items
   stay code-complete but unverified in-client until the owner runs their sessions and records the result.
6. **Releases and version bumps are NOT in this plan.** No addon version bump, no Version History row and
   no release tag. The owner decides whether and when to release, separately.

Some GitHub issue writes also wait on a merge. For example, AM-15 and AM-23 label and close their issues
"after the owner merges", with at least 5 s between `gh` writes.

A few items record a choice the plan made where the audit offered options. They are open to the owner
at execution:

- **BL-05** takes Option A, so Defaults and `/bl resetall` discard recorded history after the confirm
  popup. That is a player-visible data-loss change, and the BankLedger plan notes ask for it to be
  confirmed.
- **PF-22** takes option (b).
- **PM-15** takes a default the owner may swap.
- **AM-32**'s register row stands only if the owner re-ratifies it.

---

## How to resume

```
./resume-state.sh          # per-milestone summary, the RESUME line, the v1.56.0 tag, dirty trees, off-branch repos
./resume-state.sh -v       # also lists every remaining id
./resume-state.sh M3       # one milestone
```

The script trusts git and nothing else. An item is **done** when a commit whose subject starts with
**`<ID>: `** exists in the repo that owns it, on the remediation branch or the default branch. A commit
that carries several ids writes them as `LK-01 + LK-02: …`. The `RESUME:` line names the next outstanding
ids in manifest order. Pick up from there, respecting each item's `depends_on` in `04_EXECUTION_PLAN.md`.

When an item legitimately produces no commit, add a row to `exceptions.tsv`. The row is the id, a tab,
and a reason that includes a command a reader can run to check the claim. `resume-state.sh` counts the
row as landed.

Never mark progress by editing this directory. The record is the commits.
