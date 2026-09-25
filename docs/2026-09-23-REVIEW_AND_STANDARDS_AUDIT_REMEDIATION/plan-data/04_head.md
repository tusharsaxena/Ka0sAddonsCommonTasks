# 04 — Execution Plan

**384 work items in four milestones, ordered by dependency.**

> **Nothing in this plan has been executed.** No item has been started, no tag cut, no payload copied and
> no test written. Every "add", "move" and "re-vendor" below describes a change that has not been made
> yet. `./resume-state.sh` is the only record of progress, and it reads git.

`03_SPEC.md` says what each item must achieve. `02_UPSTREAM_CHANGES.md` gives the upstream rationale and
blast radius. `01_CONSOLIDATED_FINDINGS.md` has the findings, and `05_TRACEABILITY.md` maps each finding
to its items. This document is assembled from `plan-data/04_head.md` (these rules) followed by
`plan-data/04_tables.md` (the item tables). The tables are generated from `plan-data/items.json`, the
single source of truth. Edit that file, regenerate and reassemble; never hand-edit the tables.

**There are no dates in this document.** Milestones set the order of the work, not a schedule.

---

## Milestone map

| M | Name | Items | Repos touched | Depends on |
|---|---|---|---|---|
| **M1** | Upstream: WowAddonStandards v2.65.0, LibKa0s v1.56.0 (local tag), wow-addon plugin 2.4.0 | **44**: WS-01…08 (8), LK-01…33 (33), WA-01…03 (3) | WowAddonStandards, LibKa0s, wow-addon | nothing |
| **M2** | Pre-re-vendor fixes, then a whole-payload re-vendor of v1.56.0 into all eleven addons | **19**: AT-01, AM-01, AM-02, BL-01, BL-02, CM-01, KC-01, WG-01 (8), then RV-AT … RV-WG (11) | all eleven addons | **M1 complete** |
| **M3** | Addon remediation: every remaining finding, consumer follow-up and owner-scope issue | **310**: AT 25 · AM 33 · BL 23 · CM 30 · KC 27 · LH 36 · MM 32 · PM 24 · PF 25 · PC 26 · WG 29 | all eleven addons | that addon's RV item |
| **M4** | `/wow-addon:revendor-standards` against v2.65.0 (owner-gated) | **11**: AT-26, AM-35, BL-25, CM-31, KC-27, LH-36, MM-32, PF-25, PM-16, PC-26, WG-30 | all eleven addons | **the owner merging and pushing WowAddonStandards**, plus that addon's RV and `<AB>-DOCS` items |

### The rule

1. **All upstream work is in M1, and M1 finishes before any addon is touched.** No item in M2 or later
   edits LibKa0s, WowAddonStandards or wow-addon. Within M1, WS-01…08 go first because WS-02, WS-04 and
   WS-07 carry rulings that LK items implement. Then LK-01…33 in id order, respecting `depends_on`. WA-02
   can land any time; WA-01 any time after WS-01. WA-03 goes last, after the tag. LK-33 cuts `v1.56.0`
   **locally**. Its dependency closure includes LK-03, the AceDB fake fidelity change, so the tag carries
   it.
2. **M2 fixes first, then re-vendors.** In each addon, the pre-re-vendor fixes land first:
   - AbsorbTracker: AT-01
   - AuraMaster: AM-01, AM-02
   - BankLedger: BL-01, BL-02
   - ConsumableMaster: CM-01
   - KickCD: KC-01
   - WhatGroup: WG-01

   Each must pass on the vendored v1.55.0 payload **and** on the v1.56.0 dry run. Then that addon's RV
   item copies the **whole** payload (`libs/LibKa0s/` and `tests/_kit/`) from the local tag and rolls the
   CLAUDE.md provenance line. The RV commit also writes `docs/revendor/2026-09-23-v1.56.0/` **by hand**,
   following the local `../wow-addon/commands/revendor-libka0s.md` at the WA-01 commit. The installed
   plugin comes from GitHub and does not have WA-01 until the owner merges wow-addon. Line 1 of
   `01_DELTA.md` is exactly `Delta: LibKa0s v1.55.0 -> v1.56.0`. The RV commit is copy-only
   (`libs/LibKa0s/`, `tests/_kit/`, the CLAUDE.md provenance line, `docs/revendor/2026-09-23-v1.56.0/`).
   It takes no adoption decision, edits no addon code and does not regenerate `docs/test-cases.md` or the
   badge. It is green or lists its reds in its commit body.
3. **M3 runs per addon, in parallel across repositories and serially within one.** Inside a repository,
   items land in id order, respecting `depends_on`. Each addon ends with its `<AB>-DOCS` item, which
   writes the automated-test bundle and the doc ripple. Cross-repository dependencies in M3 point only
   at M1 or M2 items, which are already done by then.
4. **M4 runs after the owner merges.** `/wow-addon:revendor-standards` fetches the standard from GitHub.
   Every M4 item therefore starts by checking that
   `gh api repos/tusharsaxena/WowAddonStandards/contents/standards/STANDARDS.md --jq .content | base64 -d | grep -m1 v2.65.0`
   returns a match. If it does not, stop and leave the item open. Never hand-edit the three-place standards
   reference from the local sibling.

**Kit revision 26 will redden some consumer suites, and that is intended.** `CreateFrame` starts shown,
the AceDB fake raises and strips defaults, `EventRegistry` callbacks are recorded, frame `RegisterEvent`
honours `__badEvents`, `test_eol` catches lone CRs, the prose gate scans store roots, and kit case names
carry `§`. The owner's standing ruling is that a red exposes a real bug: tighten the setup, and never
weaken an assertion. Every RV commit is green or lists its reds in its commit body. The addon's M2
pre-fixes aim to make it green, its M3 items clear any remaining red, and the addon is green again at the
latest by its `<AB>-DOCS` item.

**The minimap rename carries no SavedVariables migration.** WS-06 renames the row's schema/CLI path from
`…minimap.hide` to `…minimap.shown`. The stored key stays LibDBIcon's `db.global.minimap.hide`. No addon
adds a migration step or bumps a schema version for it. Each addon's rename item carries the same
test-first carry-over check: a legacy `hide = true` reads as `shown = false`, the button stays hidden,
`minimapPos` survives, and no `shown` key is ever stored.

---

## Standing verification, every item

Unless an item says otherwise, "verified" means all of the following pass in the repository touched.
Every suite runs through the bounded runner by absolute path, because it is not on `PATH`:

```
B=/home/tushar/.claude/wow-addon/bin/ka0s-bounded
$B luacheck .                                                   # 0 warnings / 0 errors
$B lua5.1 tests/run.lua                                         # 0 failed
$B lua5.1 tests/run.lua --list | diff --strip-trailing-cr - docs/test-cases.md   # empty
$B lizard -l lua -x './libs/*' -x './tests/_kit/*' -C 15 -w .   # no output: no function above CCN 15
git ls-files '*.lua' ':!libs' ':!tests/_kit' | xargs wc -l | awk '$2!="total" && $1>1500'   # no output
git status --porcelain                                          # only the intended paths
```

If the repository has `tests/perf.lua`, also run `$B lua5.1 tests/perf.lua` wherever an item touches a
hot path, and quote the before and after figures in the commit body.

- **CCN ≤ 15** for every function outside `libs/` and `tests/_kit/`. An item that edits a function at
  CCN 13–15 records the lizard delta.
- **1500-line cap** for every authored Lua file. A generated file that is exempt by rule, such as
  PrettyChat's `GlobalStrings/`, stays exempt.
- **Tests first where behaviour changes.** Write the case, watch it fail against the current code, then
  make the change. The item's `tests` field names the red-first case. An item whose `tests` field says
  "none: docs only" states the behavioural check it uses instead.
- **When the case count moves, `docs/test-cases.md` and the README tests badge move in the same
  commit.** Kit revision 26 renames the kit's own cases, so items give deltas (+N), not absolute totals.
  The copy-only RV commit is the exception: the addon's next item regenerates the inventory and badge, at
  the latest `<AB>-DOCS`, which also regenerates the final totals.
- **Never edit `libs/` or `tests/_kit/` in an addon.** Both are vendored payload that only an RV item
  writes, by whole copy. A defect found there belongs upstream, in a new LibKa0s item, never in a local
  patch.

---

## Commits, branches and pushes

- **One commit per item.** The subject is **`<ID>: <summary>`**, for example
  `LK-11: Core gains SafeRegisterEvent`. `resume-state.sh` detects landed work from that prefix and from
  nothing else. When two items must land together to stay green, the subject carries both ids:
  `LK-01 + LK-02: …`. End every message with the session's attribution lines.
- **Branch `feat/2026-09-23-review-audit-remediation` in every repository.** That covers the eleven
  addons, LibKa0s, WowAddonStandards, wow-addon and Ka0sAddonsCommonTasks. All fifteen already have it
  checked out. Never commit to `master` or `main` directly.
- **Push the branch to origin at the end of each milestone**, for every repository that milestone
  touched. Pushing a branch is not a merge.
- **Never merge to `master`/`main` without the owner's go-ahead.** That applies in every repository.
  Merge upstream before the addons.
- **Tag `v1.56.0` is created locally by LK-33** on the LibKa0s branch. The M2 re-vendors and every
  consumer's `test_vendor_sync` resolve it from the local sibling checkout. It stays local and is pushed
  only when the owner approves the LibKa0s merge, after Session L in `06_SMOKE_TESTS.md`. An addon branch
  whose CLAUDE.md provenance line names v1.56.0 may be on origin before the tag is. That is acceptable:
  the branch is unmerged, and the tag is one push away.
- **No addon version bump and no release.** No TOC version, README version badge, Version History row,
  release tag or `/wow-addon:bump-version` run. The only versions this plan moves are upstream: standard
  v2.65.0, LibKa0s v1.56.0 and plugin 2.4.0.
- **GitHub writes are throttled.** Any `gh issue` create or edit an item calls for is spaced at least 5 s
  from the previous write. Writes marked "after the owner merges" wait for that merge.

---

## Checkpoints

Stop and check at each of these points:

- **After each milestone.**
- **In M3, after each addon's last item.** That is its `<AB>-DOCS` item, or its M4 item once M4 opens.

At each checkpoint:

1. Run `./resume-state.sh`. The milestone, or the addon, must show every item landed. There must be no
   dirty trees and no repository off the branch. `-- LibKa0s tag v1.56.0` must read `present (local)`
   from the end of M1 onward.
2. Run the standing verification in every repository the milestone or addon touched. **All suites must
   be green**: lint 0/0, tests 0 failed, `--list` matching `docs/test-cases.md`, lizard silent, and nothing
   over the line cap. The one exception is the end of M2: an addon whose RV commit body lists reds carries
   them into M3, where its items clear them by `<AB>-DOCS` at the latest.
3. Push the branch to origin in each of those repositories.

If a checkpoint fails, fix it before moving on. Apart from the listed RV reds above, a red suite is never
carried into the next milestone or the next addon.

---

## The `⚠` convention

**`⚠` after an item's title means the item has at least one in-client smoke step in
`06_SMOKE_TESTS.md`.** Its `smoke` field is non-empty. There are **168** such items: M1 17, M2 2, M3 149,
M4 0. The headless suites cannot prove a `⚠` item on their own. It is code-complete when it lands, and
in-client verified only when its session in `06_SMOKE_TESTS.md` has been run and signed off. Nothing in
this plan claims that has happened. An item without `⚠` has nothing that needs a client, though a
session may still re-check it opportunistically while the operator is in game.

---
