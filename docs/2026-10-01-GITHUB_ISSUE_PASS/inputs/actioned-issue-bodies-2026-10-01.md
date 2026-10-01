

######## AbsorbTracker-10 — Border is acting funny, fix it


--- comment (tusharsaxena 2026-08-06):
### Context
A GitHub-sourced pending item on the border rendering path, carried as deferred by the pending audit.

### Evidence
Source: `GitHub #10`
Evidence hash: `f0c7ab96`

### Deferral rationale
Cannot be worked without a repro: the issue is a title with an empty body, and the border path has been rewritten twice since it was filed.

### Provenance
Migrated from `docs/pending/LEDGER.md` row `ISS-10` (evidence hash `f0c7ab96`), originally decided 2026-07-31.

--- comment (tusharsaxena 2026-09-07):
### 2026-09-07 remediation cycle — issue reconciliation (`M2-23`)

**Disposition: unaffected.**

No pass in this cycle filed a border defect against AbsorbTracker, and this issue carries no reproduction, no version and no screenshot to match a finding against — so the plan neither covers it nor decides against it.

The one piece of border work in the plan, in case it turns out to be this: `C02` (`PANELMASTER-R-01`, five repos) has `core/LSMPatch.lua` re-registering AceGUI's process-global `LSM30_Border` widget type at `PLAYER_LOGIN`, so **whichever addon loaded last owns everyone's Border dropdown**. AbsorbTracker is the one divergent case in the five — it calls `NS.ApplyLSMBorderPatch()` from `core/AbsorbTracker.lua:52` rather than from a frame, so its patch runs at a different moment than the other four. `M1-STD-10` (landed) rules that a widget-type re-registration is the library's concern; `M1-LK-05` (landed, in v1.27.0) publishes `lib.__PatchLSM30Border()`; `M4-02` calls it, `M4-03` is the session-5 in-client sweep that loads all five addons together in several load orders, and `M4-04`…`M4-08` delete the five local patches.

**Ask:** attach a reproduction — which control, what it does, and whether other Ka0s addons are loaded. If it reproduces only alongside a sibling, session 5 will settle it and this becomes `C02`. If it reproduces with AbsorbTracker alone, it is a defect this cycle did not find.

---
*Filed by work item `M2-23` of the **2026-09-07 review-and-standards-audit remediation** cycle — 207 triaged findings in 39 clusters across ten repositories, 106 work items in five milestones. The bundle lives in the `Ka0sAddonsCommonTasks` repo at `docs/2026-09-07-REVIEW_AND_STANDARDS_AUDIT_REMEDIATION/`: `01_CONSOLIDATED_FINDINGS.md` for the findings and clusters, `04_EXECUTION_PLAN.md` for the work items, `05_TRACEABILITY.md` for the finding-to-item map, `06_SMOKE_TESTS.md` for the six in-client sessions, `PROGRESS.md` for what has actually landed. `M2-23` gives every open issue in the eleven stores one of three dispositions — covered, unaffected, contradicted — and closes nothing.*

*State at the time of writing: **M1 complete** (38/38, LibKa0s v1.26.0 and v1.27.0 cut on the branch, the standard rolled to v2.39.0), **M2 in flight**, M3/M4/M5 not started, and no in-client smoke session performed.*

--- comment (tusharsaxena 2026-09-24):
### 2026-09-23 remediation (`AT-DOCS`): referred, still out of scope

The 2026-09-23 standards audit listed this open high-severity bug as finding AbsorbTracker-A-27 (audit `AT-Info-10`). It is a backlog item, not a standards deviation. The audit did not investigate it and referred it to review, and the review did not raise it.

It is **outside this remediation's scope** and stays as it is: open, `state:triaged`, `severity:high`. It still needs its own investigation, either an `issue-triage` pass or a targeted debug session on the border rendering path.



######## AbsorbTracker-20 — Gate the unit-panel mirror refresher on IsShown; flag off-screen panels dirty
Deferred from the 2026-07-31 review (finding F-008), re-deferred by
/wow-addon:pending-audit as item PLAN-03.

## Evidence

> ### F-008 — the mirror refresher rebuilds off-screen panels `[perf][ux]`
> **Where:** `settings/UnitPanel.lua:463-471`.
> **Problem:** The registered refresher calls `Helpers.RenderUnitPanel(ctx, pageKey)` — a full
> `ClearScroll` + rebuild — whenever the unit's mirror state changed since the last render, with no
> `ctx.panel:IsShown()` check. options-ui-§11 requires structural rebuilds to be scoped to the
> on-screen subcategory, with off-screen panels flagged dirty for a lazy rebuild on next `OnShow`
> (anti-patterns #39).
> **Impact:** One `/at set units.focus.mirror true`, one Defaults click, or one profile switch tears
> down and rebuilds every rendered Bar/Border/Font panel, including the two the user cannot see.
> Three pages is not the ~15 that produced the half-second stall the rule was written from, so this
> is a latency and widget-churn concern rather than a visible freeze.
> **Direction:** Gate the re-render on `ctx.panel and ctx.panel:IsShown()`; otherwise set
> `ctx.__dirty = true` and extend each page's first-show guard to re-render when dirty. The in-place
> checkbox re-sync above it stays unconditional — that half is already compliant.

## Location

`settings/UnitPanel.lua:463-471`, plus the first-show guards in `settings/Bar.lua`,
`settings/Border.lua` and `settings/Font.lua`.

## Severity

Medium — a deviation from the Ka0s WoW Addon Standard (options-ui-§11, anti-patterns #39) carried
over from a review bundle. Not a correctness bug: the behaviour predates the LibKa0s extraction and
was carried verbatim from the deleted `settings/Helpers.lua`.

## Why it is still open

Deferred in commit `ef71076` to protect the M9 in-game pass, whose purpose was confirming the
extraction changed nothing visible. It is now the addon's only remaining structural rebuild —
everything else refreshes in place inside LibKa0s.

## Design already specified

`docs/reviews/2026-07-31/02_PROPOSED_CHANGES.md` (C-7) and `04_EXECUTION_PLAN.md` (M3.2).


--- comment (tusharsaxena 2026-08-06):
### Context
A review-plan item from the 2026-07-31 review bundle (finding F-008), deferred a second time by the pending audit and now tracked publicly.

### Evidence
Source: `` `docs/reviews/2026-07-31/01_FINDINGS.md` (F-008) ``
Evidence hash: `77a8ee64`

### Deferral rationale
Second deferral, now tracked publicly. Previously deferred in commit `ef71076` to protect the M9 in-game pass. Design already specified (C-7 / M3.2).

### Provenance
Migrated from `docs/pending/LEDGER.md` row `PLAN-03` (evidence hash `77a8ee64`), originally decided 2026-07-31.

--- comment (tusharsaxena 2026-09-07):
### 2026-09-07 remediation cycle — issue reconciliation (`M2-23`)

**Disposition: unaffected.**

The plan opens `settings/UnitPanel.lua`, but for a different defect and at a different place. `ABSORBTRACKER-R-02` (cluster `C28`, work item `M4-18`) is `core/Units.lua:111-119` reached from `UnitPanel.lua:224-228` — `CopyFromPlayer` writing 19 keys plus `dst.mirror = false` directly instead of through `NS.SetByPath`, so the write seam never logs them. This issue is `:463-471`, the registered mirror refresher rebuilding off-screen panels with no `ctx.panel:IsShown()` check (`options-ui-§11`, anti-pattern #39).

No finding in the bundle names that refresher, so `F-008` / `PLAN-03` is untouched and its deferral stands. Worth knowing that `M4-18` will be editing the write path this issue's fix would render through — do them in that order if both land.

---
*Filed by work item `M2-23` of the **2026-09-07 review-and-standards-audit remediation** cycle — 207 triaged findings in 39 clusters across ten repositories, 106 work items in five milestones. The bundle lives in the `Ka0sAddonsCommonTasks` repo at `docs/2026-09-07-REVIEW_AND_STANDARDS_AUDIT_REMEDIATION/`: `01_CONSOLIDATED_FINDINGS.md` for the findings and clusters, `04_EXECUTION_PLAN.md` for the work items, `05_TRACEABILITY.md` for the finding-to-item map, `06_SMOKE_TESTS.md` for the six in-client sessions, `PROGRESS.md` for what has actually landed. `M2-23` gives every open issue in the eleven stores one of three dispositions — covered, unaffected, contradicted — and closes nothing.*

*State at the time of writing: **M1 complete** (38/38, LibKa0s v1.26.0 and v1.27.0 cut on the branch, the standard rolled to v2.39.0), **M2 in flight**, M3/M4/M5 not started, and no in-client smoke session performed.*


######## AbsorbTracker-32 — Adopt O.RenderTabbedSchema opts for the Appearance page strip
Evaluated under remediation item AT-15 (finding AbsorbTracker-A-04), against LibKa0s v1.56.0, Options `24.31.4.7.4` (OptionsTabs minor 4, which adds `RenderTabbedSchema`'s fifth `opts` argument: `tabs`, `cfg`, `disabledFor`, `disabledNotice`, `chrome`).

`settings/UnitPanel.lua` `renderUnitPanelBody` step 2 hand-builds the Appearance page's strip: `partitionTabs`, then `Helpers.TabStrip`, then `RenderRows` or `renderMirroredHint`. The item adopts `O.RenderTabbedSchema(ctx, pageKey, nil, nil, { disabledFor = ..., disabledNotice = ... })` only if all four conditions hold.

| # | Condition | Holds at v1.56.0? |
|---|---|---|
| i | A `PageHeader` drawn before the call survives, and `ctx.__bannerHeight` still feeds the strip's reservation | Yes: `TabStrip` reads `ctx.__bannerHeight`, and `ClearScroll` leaves the chrome ledger alone |
| ii | Rows come from the descriptor's `rowsForPage(pageKey, ctx.unit)` | Yes: `OptionsTabs.lua` `O.RenderTabbedSchema` line 1457 |
| iii | `disabledFor(cfg)` is re-evaluated on every render and tab click | Yes: `pageDisabled(opts)` runs in `renderBody` on each render, and a tab click re-renders with the same `opts` |
| iv | `skipRender` rows stay out of the strip | **No.** `partition(rows)` (OptionsTabs.lua ~1332) keys on `row.group ~= nil` only, so the mirror flag row (`skipRender = true`, `group = "Link"`, settings/Appearance.lua) would become a sixth "Link" tab on target and focus |

**Failing condition: (iv).** Two more mismatches came up in the evaluation. Neither is one of the four conditions, but either would also block a like-for-like adoption:

- `disabledFor` draws `disabledNotice` **above** rows that are still drawn, disabled. This page draws the hint **in place of** the rows (the smoke test says "Focus with 'Linked to Player' shows the hint only"). The host cases in `tests/test_widgets.lua` pin this and would go red.
- The library's tab click is `ClearScroll` plus a re-render of `RenderTabbedSchema` alone. `ClearScroll` resets `ctx.refreshers`, so the page's two-tier mirror refresher would be gone after the first tab click.

The workaround would be a host tab keyed by each group whose `render` draws the hint, plus a `skipRender` filter on the host side. That means a local fork of the partition, which the spec lists as a non-goal. The host composition stays.

**Re-check trigger:** the next Options minor (OptionsTabs minor 5 or later). Adopt once `RenderTabbedSchema`'s partition skips `skipRender` rows. Then weigh the other two mismatches: a notice that replaces the rows rather than sitting above them, and a tab click that keeps host refreshers. The characterization cases added by AT-15 in `tests/test_widgets.lua` ("every unit's Appearance strip is its schema's groups…", "a mirrored unit's every tab draws the hint…") must stay green through an adoption.



######## BankLedger-2 — Backfill item names onto rows stored before the client cached the item
A ledger row written while the client had not yet cached the item keeps only its item id, permanently. Such a row shows as `Item <id>` in History and drops out of the Type, Sub-type and Quality breakdowns in Insights for good. Documented under *Known limitations* in `docs/ARCHITECTURE.md`.

**The pieces already exist.** `Compat.ItemNameQuality` returns `(name, quality)` and is nil-safe for an uncached id, and `Compat` already has a request-and-callback path that fires once an id loads (`core/Compat.lua:215-225`). The settings Filters list uses exactly this — `settings/Panel.lua:467` notes that a background load is kicked off so a later rebuild fills the name in. Stored ledger rows never get the same treatment.

**What it would take.** Walk stored history for rows missing `itemName`, request those ids, and rewrite the rows as they resolve.

**The care needed.** This is a write path over the saved variables, so it wants:

- a bound on how much it walks and requests at login, so it cannot stall the client;
- idempotency, so a repeated run cannot corrupt or duplicate a row;
- a decision on whether it also backfills `quality`, `itemType` and `itemSubType` — which is what actually returns the row to the Insights breakdowns.

Deferred via `/wow-addon:pending-audit` on 2026-07-31 (item `DOC-04`).

--- comment (tusharsaxena 2026-08-06):
### Context

A Known limitation in `docs/ARCHITECTURE.md`: rows recorded before the client had the item cached keep a missing or placeholder name, and nothing backfills them afterwards. Already tracked as issue #2.

### Evidence

Source: `` `docs/ARCHITECTURE.md` ▸ Known limitations ``

Evidence hash: `c079f94b`

### Deferral rationale

Deferred with a tracking issue, [#2](https://github.com/tusharsaxena/BankLedger/issues/2). Backfilling names means rewriting stored rows on the saved-variable write path, which wants a design pass of its own.

### Provenance

Migrated from `docs/pending/LEDGER.md` row `DOC-04` (evidence hash `c079f94b`), originally decided 2026-07-31.

--- comment (tusharsaxena 2026-09-07):
### 2026-09-07 remediation cycle — issue reconciliation (`M2-23`)

**Disposition: unaffected.**

The bundle is 207 triaged findings from the 2026-09-07 review and standards-audit passes: defects, standards deviations and record drift. It carries no feature work, and decision 5 of the cycle is that nothing ships (no addon version bump anywhere). Nothing in the plan advances this request or decides against it, so it stands exactly as filed.

No finding names item-name backfill. Relevant neighbour: `M2-05` (landed, `d4534d0`) made the migration ladder functional — `g.schemaVersion or 1` had been reading the current version, so the `< NS.SCHEMA_VERSION` arm never ran. A backfill is most naturally a migration step, and until this cycle there was no working ladder to hang one on.

---
*Filed by work item `M2-23` of the **2026-09-07 review-and-standards-audit remediation** cycle — 207 triaged findings in 39 clusters across ten repositories, 106 work items in five milestones. The bundle lives in the `Ka0sAddonsCommonTasks` repo at `docs/2026-09-07-REVIEW_AND_STANDARDS_AUDIT_REMEDIATION/`: `01_CONSOLIDATED_FINDINGS.md` for the findings and clusters, `04_EXECUTION_PLAN.md` for the work items, `05_TRACEABILITY.md` for the finding-to-item map, `06_SMOKE_TESTS.md` for the six in-client sessions, `PROGRESS.md` for what has actually landed. `M2-23` gives every open issue in the eleven stores one of three dispositions — covered, unaffected, contradicted — and closes nothing.*

*State at the time of writing: **M1 complete** (38/38, LibKa0s v1.26.0 and v1.27.0 cut on the branch, the standard rolled to v2.39.0), **M2 in flight**, M3/M4/M5 not started, and no in-client smoke session performed.*


######## KickCD-10 — Adopt RenderGrid for the spell-list editor — blocked on two LibKa0s gaps
### Description

`LibKa0s-Options-1.0` shipped `RenderGrid` in `OptionsWidgets` minor 4 as the caller-driven sibling of `RenderRows` — for lists whose **length is not in the schema**. Its stated rationale was that "every host had a hand-rolled copy of this loop".

KickCD has exactly one such list — the spell-list editor — and `RenderGrid` currently **cannot reach it**. A read-only recon during the 2026-08-01 adoption report returned `not-expressible`, and the reason is two gaps in the library rather than anything bespoke about this addon.

The list in question is `settings/Spells.lua:913`:

```lua
for i = 1, #list do container:AddChild(buildRow(AceGUI, list, i)) end
```

One row per tracked spell for the selected class/spec, length coming from the profile's spell table. `buildRow` (`settings/Spells.lua:506`) builds a 28px full-width `SimpleGroup(Flow)` of eight fixed-pixel-width widgets. Rows are reorderable and removable at runtime.

### Motivation

`RenderGrid` currently has exactly **one** consumer (ConsumableMaster). A surface with one consumer has had its contract tested against one shape, and every adopter so far has surfaced a descriptor assumption that only held for the ones before it. Making KickCD's spell list a real second consumer is worth more than the lines it would retire.

It also corrects a standing claim: `LibKa0s/docs/adoption-prompt.md` records ~450 lines across `settings/Panel.lua`, `Panel_Widgets.lua` and `Panel_Render.lua` as having "no library equivalent". That assessment **predates `RenderGrid`**, and it still stands — but for a reason it never recorded, which is finding 1 below.

### Proposed behavior

Both fixes are upstream in `../LibKa0s`, additive within `-1.0`, and neither can be worked around here. **Never edit `libs/` — the next re-vendor reverts it silently.**

**1. `RenderGrid` needs a `parent` parameter (blocking).**

`libs/LibKa0s/OptionsWidgets.lua:534-535`:

```lua
function O.RenderGrid(ctx, items)
  local scroll = O.EnsureScroll(ctx)   -- hard-bound
```

`EnsureScroll` caches on `ctx.scroll` and anchors its ScrollFrame flush to the whole of `ctx.body` (`libs/LibKa0s/Options.lua:289-290`, `TOPLEFT PADDING_X-4,-8` / `BOTTOMRIGHT -(PADDING_X+12),8`).

`settings/Spells.lua:888` creates **its own** ScrollFrame, anchored `TOPLEFT body 16,-56` to leave room for a hand-anchored header, and applies `PatchAlwaysShowScrollbar` to that container itself. Calling `RenderGrid` there would silently instantiate a second, full-body scroll frame overlapping the header.

`RenderGrid` is the only maker in the module that does not take a parent. Seven siblings already do it the right way — `RenderField(ctx, row, parent, relativeWidth)` at `:464`, `SessionCheckbox` at `:481`, and five makers using `parent = parent or O.EnsureScroll(ctx)` (`:255`, `:276`, `:333`, `:375`, `:395`, `:482`).

Proposed: `RenderGrid(ctx, items, parent)` with the same `parent or O.EnsureScroll(ctx)` default. Additive, preserves today's behavior for the existing consumer, and is the single change that makes this adoptable.

**2. `RenderGrid` never calls `DoLayout()`.**

`RenderRows` ends with `if scroll.DoLayout then scroll:DoLayout() end` (`OptionsWidgets.lua:657`). `RenderGrid` ends at `flushRow()` and returns. A host that renders a page with `RenderGrid` **alone** — the whole point of a caller-driven sibling — gets an unlaid-out scroll frame and has to know to call `DoLayout` itself. The README entry does not say so. Either match `RenderRows` or document the asymmetry.

### Acceptance criteria

- [ ] `RenderGrid` accepts an optional `parent`, defaulting to `O.EnsureScroll(ctx)`; ConsumableMaster's existing call is unchanged in behavior.
- [ ] The `DoLayout` asymmetry is resolved — matched to `RenderRows` or documented in `LibKa0s/README.md`.
- [ ] Both land upstream in `../LibKa0s` with a failing test first, the touched files' minors bumped, `CHANGELOG.md` updated, and a re-vendor into **every** consumer (`LibKa0s/docs/releasing.md`). Each existing consumer's suite must be unchanged — that is what proves the change was additive.
- [ ] `settings/Spells.lua:913` renders through `RenderGrid`, with the row strip visually unchanged.
- [ ] Smoke test §25 and §10 (spell-list editor) pass.

### Out of scope / notes

Two further `RenderGrid` limits were found and are **not** blockers for this issue — the spell row would still be one opaque `wide` item whose `make` builds the strip, so adoption retires little of `buildRow`:

- Only two cell widths exist: `HALF` (0.5) or full-width via `wide`. A dense multi-column list needs a per-item `width`, or an items-per-row parameter.
- `O.AddSpacer(scroll, L.ROW_VSPACER)` fires unconditionally after every flushed row (`:548`, `:575`) with no opt-out. The spell list is a compact 28px List layout with no inter-row gap, so it would change visually.

Separately, the `wide` branch adds its SimpleGroup **and** its spacer even when the item's render returned false, leaving a blank gap where a failing item was. The paired branch is correct. Guard-per-item is the stated contract; the wide path only half-honours it.

Source: `LibKa0s/docs/adoption/2026-08-01/` (§7 of `03_DEVIATIONS.md` / `04_RECOMMENDATIONS.md`), and the recon recorded in `docs/pending/LEDGER.md`.

--- comment (tusharsaxena 2026-08-06):
### Triage decision

- **Decision:** triaged
- **Decided:** 2026-08-07
- **Approach:** Blocked upstream. This cannot start until `LibKa0s` gives `RenderGrid` a `parent` parameter — an additive change within `-1.0`. The adoption itself is then straightforward.

### Rationale

Real work, but not now, and **not blocked on anything in this repo**.

`RenderGrid` hard-binds `O.EnsureScroll(ctx)` (`libs/LibKa0s/OptionsWidgets.lua:534-535`), which caches on `ctx.scroll` and anchors its ScrollFrame flush to the whole of `ctx.body`. The spell-list editor creates **its own** ScrollFrame at `settings/Spells.lua:888`, anchored `TOPLEFT body 16,-56` to leave room for a hand-anchored header, and applies `PatchAlwaysShowScrollbar` to that container. Calling `RenderGrid` there would silently instantiate a second, full-body scroll frame overlapping the header.

That is a library gap rather than anything bespoke about this addon: **`RenderGrid` is the only maker in the module that does not take a parent.** Seven siblings already do it the right way — `RenderField(ctx, row, parent, relativeWidth)` at `:464`, `SessionCheckbox` at `:481`, and five makers using `parent = parent or O.EnsureScroll(ctx)`.

**The fixes are upstream and must be made there.** Never edit `libs/` — the next re-vendor reverts it silently.

### Why this is worth doing at all

The value is in the library, not in the lines KickCD would retire. `RenderGrid` currently has exactly **one** consumer (ConsumableMaster), so its contract has been tested against exactly one shape — and every adopter so far has surfaced a descriptor assumption that only held for the ones before it. Making the spell list a real second consumer tests the contract in a way nothing else currently does.

It also corrects a standing claim: `LibKa0s/docs/adoption-prompt.md` records ~450 lines across `settings/Panel.lua`, `Panel_Widgets.lua` and `Panel_Render.lua` as having "no library equivalent". That assessment predates `RenderGrid` and still stands — but for a reason it never recorded, which is the `parent` gap above.

### Not done here

No code changed, and no upstream issue was filed as part of this triage. Whoever picks this up should raise the `parent` parameter in `LibKa0s` first; this issue stays open tracking the KickCD-side adoption that follows.


--- comment (tusharsaxena 2026-09-07):
### 2026-09-07 remediation cycle — issue reconciliation (`M2-23`)

**Disposition: unaffected.**

Not scheduled, and the two LibKa0s gaps this is blocked on were not closed. M1 cut both of the cycle's tags — v1.26.0 (`M1-LK-04`) and v1.27.0 (`M1-LK-15`), both landed — and the fifteen LibKa0s items in between are the composer fix (`M1-LK-02`), the `TabStrip` pooling (`M1-LK-03`), `__PatchLSM30Border` (`M1-LK-05`), the dead-button report (`M1-LK-06`) and the test-kit work (`M1-LK-07`…`M1-LK-10`). `RenderGrid` appears in none of them, and the plan then declines *"cut any release beyond v1.26.0 and v1.27.0"*.

So the blocker is unchanged and this waits on the next Options/Widgets major. The related decision to read alongside it: `M5-09` declines an upstream composer arm for PanelMaster's record-backed binds with the reasoning *"adding a third surface to carry one addon's hand-written groups is the tail wagging the dog"* — the same argument would be made against a `RenderGrid` change with one consumer, so make the two-consumer case explicitly when this is re-proposed.

---
*Filed by work item `M2-23` of the **2026-09-07 review-and-standards-audit remediation** cycle — 207 triaged findings in 39 clusters across ten repositories, 106 work items in five milestones. The bundle lives in the `Ka0sAddonsCommonTasks` repo at `docs/2026-09-07-REVIEW_AND_STANDARDS_AUDIT_REMEDIATION/`: `01_CONSOLIDATED_FINDINGS.md` for the findings and clusters, `04_EXECUTION_PLAN.md` for the work items, `05_TRACEABILITY.md` for the finding-to-item map, `06_SMOKE_TESTS.md` for the six in-client sessions, `PROGRESS.md` for what has actually landed. `M2-23` gives every open issue in the eleven stores one of three dispositions — covered, unaffected, contradicted — and closes nothing.*

*State at the time of writing: **M1 complete** (38/38, LibKa0s v1.26.0 and v1.27.0 cut on the branch, the standard rolled to v2.39.0), **M2 in flight**, M3/M4/M5 not started, and no in-client smoke session performed.*


######## KickCD-24 — Peel modules/Castbar.lua below the 1000-line band (1435 lines)
`modules/Castbar.lua` is 1435 lines, inside the 1000–1500 band of layout-§1 (authored files over 1000 lines carry a tracked peel; 1500 is the hard cap).

**Peel seam:** the cast-event handlers into `modules/Castbar_Events.lua`.

Filed by the 2026-09-23 review/audit remediation (KC-28, finding KICKCD-A-12). Measured with `wc -l` on branch feat/2026-09-23-review-audit-remediation.


######## KickCD-25 — Peel modules/IconGrid.lua below the 1000-line band (1368 lines)
`modules/IconGrid.lua` is 1368 lines, inside the 1000–1500 band of layout-§1 (authored files over 1000 lines carry a tracked peel; 1500 is the hard cap).

**Peel seam:** the visibility and glow gate into `modules/IconGrid_Visibility.lua`.

Filed by the 2026-09-23 review/audit remediation (KC-28, finding KICKCD-A-12). Measured with `wc -l` on branch feat/2026-09-23-review-audit-remediation.


######## KickCD-26 — Peel modules/IconGrid_Render.lua below the 1000-line band (1014 lines)
`modules/IconGrid_Render.lua` is 1014 lines, inside the 1000–1500 band of layout-§1 (authored files over 1000 lines carry a tracked peel; 1500 is the hard cap).

**Peel seam:** the cooldown-text ticker into `modules/IconGrid_Text.lua`.

Filed by the 2026-09-23 review/audit remediation (KC-28, finding KICKCD-A-12). Measured with `wc -l` on branch feat/2026-09-23-review-audit-remediation.


######## KickCD-27 — Peel tests/wow_mock.lua below the 1000-line band (1233 lines)
`tests/wow_mock.lua` is 1233 lines, inside the 1000–1500 band of layout-§1 (authored files over 1000 lines carry a tracked peel; 1500 is the hard cap).

**Peel seam:** the mock's frame model into `tests/wow_mock_frames.lua`.

Filed by the 2026-09-23 review/audit remediation (KC-28, finding KICKCD-A-12). Measured with `wc -l` on branch feat/2026-09-23-review-audit-remediation.


######## KickCD-28 — Peel settings/Spells.lua below the 1000-line band (1115 lines)
`settings/Spells.lua` is 1115 lines, inside the 1000–1500 band of layout-§1 (authored files over 1000 lines carry a tracked peel; 1500 is the hard cap).

**Peel seam:** the class/spec header builders (titleCaseToken … buildSpellsHeader, about :524-735) into `settings/Spells_Header.lua`.

Filed by the 2026-09-23 review/audit remediation (KC-28, finding KICKCD-A-12). Measured with `wc -l` on branch feat/2026-09-23-review-audit-remediation.


######## KickCD-29 — Peel core/Database.lua below the 1000-line band (1002 lines)
`core/Database.lua` is 1002 lines, inside the 1000–1500 band of layout-§1 (authored files over 1000 lines carry a tracked peel; 1500 is the hard cap).

**Peel seam:** the profile migrations (FoldLegacyUnits … MigrateProfile, about :505-862) into `core/Database_Migrations.lua`.

Filed by the 2026-09-23 review/audit remediation (KC-28, finding KICKCD-A-12). Measured with `wc -l` on branch feat/2026-09-23-review-audit-remediation.


######## KickCD-30 — Peel tests/test_slash.lua below the 1000-line band (1035 lines)
`tests/test_slash.lua` is 1035 lines, inside the 1000–1500 band of layout-§1 (authored files over 1000 lines carry a tracked peel; 1500 is the hard cap).

**Peel seam:** the disabled-state and degraded-stub cases into `tests/test_slash_degraded.lua`.

Filed by the 2026-09-23 review/audit remediation (KC-28, finding KICKCD-A-12). Measured with `wc -l` on branch feat/2026-09-23-review-audit-remediation.


######## KickCD-31 — Peel tests/test_options_panel.lua below the 1000-line band (1099 lines)
`tests/test_options_panel.lua` is 1099 lines, inside the 1000–1500 band of layout-§1 (authored files over 1000 lines carry a tracked peel; 1500 is the hard cap).

**Peel seam:** the degraded-stub and linked-Focus cases into `tests/test_options_panel_degraded.lua`.

Filed by the 2026-09-23 review/audit remediation (KC-28, finding KICKCD-A-12). Measured with `wc -l` on branch feat/2026-09-23-review-audit-remediation.


######## KickCD-32 — Peel tests/test_perfsetup.lua below the 1000-line band (1018 lines)
`tests/test_perfsetup.lua` is 1018 lines, inside the 1000–1500 band of layout-§1 (authored files over 1000 lines carry a tracked peel; 1500 is the hard cap).

**Peel seam:** the latch, suspended-flag and library-absent cases into `tests/test_perfsetup_latch.lua`.

Filed by the 2026-09-23 review/audit remediation (KC-28, finding KICKCD-A-12). Measured with `wc -l` on branch feat/2026-09-23-review-audit-remediation.


######## KickCD-7 — Non-interruptible casts intermittently show in "target casting interruptible" visibility mode
### Description
In General visibility mode = "When target is casting an interruptible spell", the icon grid and cast bar intermittently light up for **non-interruptible** casts that should stay hidden. Root cause (from a code trace): the interruptibility alpha-mask is purely event-driven with no polling. WoW frequently reports `UnitCastingInfo.notInterruptible` as **falsy at `UNIT_SPELLCAST_START`** and only corrects it via `UNIT_SPELLCAST_NOT_INTERRUPTIBLE`, which fires **only on a transition** — so a spell that is non-interruptible for its *entire* duration may never emit that event, leaving the grid + cast bar at alpha 1 for the whole cast.

Two gaps prevent self-correction:
- `modules/IconGrid.lua` `EnableUnit` (~L608-616) does **not** register `UNIT_SPELLCAST_DELAYED` / `UNIT_SPELLCAST_CHANNEL_UPDATE`, so a pushback never re-runs `RefreshVisibility` → `ApplyInterruptibilityMask`.
- `modules/Castbar.lua` `OnCastDelayed` (~L1324-1349) re-reads the corrected `notInterruptible` and re-colors child widgets but **never re-applies the frame-level `ApplyVisibilityMask`**, so the bar frame stays fully visible even though the corrected flag is already in hand.

### Steps to reproduce
1. General visibility = "When target is casting an interruptible spell"; frame **locked**.
2. In Murder Row, target the **Bribed Guard** NPC.
3. Watch it cast **Shield Bash** / **Crimson Glaive** (both non-interruptible).
4. Intermittently the grid + cast bar light up for these non-interruptible casts.

### Expected
Non-interruptible casts never show the grid/cast bar in this mode (alpha 0 for the whole cast).

### Actual
Intermittently they show at full alpha for the entire cast.

### Proposed fix (narrowest → most robust)
- Register `UNIT_SPELLCAST_DELAYED` + `UNIT_SPELLCAST_CHANNEL_UPDATE` on the grid (`OnUnitCastEvent` already re-masks via `RefreshVisibility`).
- Add `ApplyVisibilityMask(inst.frame, inst.unit)` to `Castbar:OnCastDelayed`.
- And/or a one-shot deferred re-apply (`C_Timer.After` after START/CHANNEL_START) to pick up the settled `notInterruptible` even when Blizzard never emits a change event.

All interruptibility handling must stay secret-value-safe (`notInterruptible` passed straight into `SetAlphaFromBoolean`, never compared in Lua) per `docs/midnight-quirks.md`.

### Not part of this bug (by design)
While the frame is **unlocked**, the interruptibility filter is intentionally bypassed (everything shows so you can drag). The default is now `locked=false`, so a fresh profile shows all casts until `/kcd lock`. Expected behavior, not this bug.

### Environment
KickCD 1.2.0 · Interface 120007 (WoW 12.0.7 Midnight)

--- comment (tusharsaxena 2026-08-06):
### Context

GitHub issue #7 reports non-interruptible casts appearing in the "target casting interruptible" visibility mode. Reviewed in the 2026-07-31 pending audit and deferred.

### Evidence

Source: `GitHub issue #7 — non-interruptible casts showing in "target casting interruptible" mode`

Evidence hash: `4242f403`

### Deferral rationale

Not now. Cost stated at decision time: the bug stays live for users.

### Provenance

Migrated from `docs/pending/LEDGER.md` row `ISS-07` (evidence hash `4242f403`), originally decided 2026-07-31.

--- comment (tusharsaxena 2026-09-07):
### 2026-09-07 remediation cycle — issue reconciliation (`M2-23`)

**Disposition: unaffected.**

This is one of the seven live `severity:high` rows `M2-23` exists to account for: the plan opens KickCD in seven work items and **never touches the interruptibility mask**. Nothing in the 207 findings names `UNIT_SPELLCAST_NOT_INTERRUPTIBLE`, `modules/IconGrid`'s alpha mask, or the event-driven-with-no-polling shape this issue traces.

That silence is a property of how the cycle was run, not a judgment on the bug: every pass audited one repository against the standard, and none of them read the issue store — which is the defect `M2-23` was written to correct. This remains the most severe *live* KickCD defect on record and the plan does not schedule it.

One interaction to know about: `M3-01` re-vendors LibKa0s v1.26.0 into this repo and `M4-01` re-vendors v1.27.0. Neither goes near `modules/Cooldowns.lua` or `modules/IconGrid.lua`, so a fix for this can be written against today's code without waiting for either.

---
*Filed by work item `M2-23` of the **2026-09-07 review-and-standards-audit remediation** cycle — 207 triaged findings in 39 clusters across ten repositories, 106 work items in five milestones. The bundle lives in the `Ka0sAddonsCommonTasks` repo at `docs/2026-09-07-REVIEW_AND_STANDARDS_AUDIT_REMEDIATION/`: `01_CONSOLIDATED_FINDINGS.md` for the findings and clusters, `04_EXECUTION_PLAN.md` for the work items, `05_TRACEABILITY.md` for the finding-to-item map, `06_SMOKE_TESTS.md` for the six in-client sessions, `PROGRESS.md` for what has actually landed. `M2-23` gives every open issue in the eleven stores one of three dispositions — covered, unaffected, contradicted — and closes nothing.*

*State at the time of writing: **M1 complete** (38/38, LibKa0s v1.26.0 and v1.27.0 cut on the branch, the standard rolled to v2.39.0), **M2 in flight**, M3/M4/M5 not started, and no in-client smoke session performed.*


######## KickCD-9 — Move time-varying icon render onto the cooldown ticker
### Description

`Icon:Apply` currently does all cooldown rendering — the alpha/tint/GCD-suppression curve evaluations, the swipe re-arm, and the countdown text — and it only runs when `Cooldowns` emits `Ka0s_KickCD_SPELL_STATE`. Because that emit is forced to fire ~10x/sec for any spell on cooldown (see Background), the emit is effectively acting as the animation driver for those visuals.

This proposes inverting that: let the existing 0.1s ticker in `modules/IconGrid_Render.lua` own everything time-varying, so `Cooldowns` can emit only on genuine state transitions.

### Background — why the emit rate is currently fixed

`C_Spell.GetSpellCooldownDuration` mints a **fresh object on every call**, so `Cooldowns.StateChanged`'s `prev.cdObject ~= next_.cdObject` compare is true on every poll for any spell on cooldown.

That compare cannot simply be replaced. Measured on a live 12.0.7 client via `/kcd debug duration` (results recorded in `docs/midnight-quirks.md`): **in combat every `DurationObject` getter is secret-tainted, including the booleans** — `HasExpired`, `HasStarted`, `IsActive`, `IsZero`. A secret boolean can't be branched on. Only `HasSecretValues()` stays plain.

So there is no Lua-side way to detect "this spell's cooldown changed" in combat. The identity compare over-fires but never under-fires, and nothing on the object can replace it.

**The ticker approach sidesteps this entirely** — re-fetching the handle each tick is unconditionally correct, so there is nothing to detect.

### Motivation

Already addressed in 9fc0d8b by splitting `Icon:Apply` into state-work vs time-work and gating the state half — a **measured 35%** reduction in widget calls per repeat apply. This issue is the remaining, larger half.

Baseline in combat (4 spells on cooldown, target+focus enabled, ~10 events/sec):

| | Now | After |
|---|---|---|
| `Icon:Apply` calls/sec | 80 | ~0 |
| C calls/sec | ~1600 | ~880 |
| Table allocations/sec | 80 | 40 |

The stronger argument is structural rather than performance. ~1600 C calls/sec is not a framerate problem. But today there's no rule about what may be added to `Icon:Apply`, which is why `Icon:StartGlow` needed a bespoke idempotency gate to stop a visible ButtonGlow pop at 10Hz. Removing the 10Hz emit makes that trap stop existing rather than needing to be remembered.

### Proposed behavior

- **Ticker (0.1s)** — for each icon with an active cooldown: fetch a fresh handle, evaluate the three curves, apply alpha/tint/suppression, re-arm the swipe, update the countdown text. Stop when `C_Spell.GetSpellCooldown(...).isActive` goes false — that stays **plain** in combat and is what `Cooldowns:PollSpell` already relies on.
- **Emit** — only on material change (`ready` / `isActive` / handle presence / plain charges) -> glow, charges badge, branch selection, ticker register/unregister.
- **`StateChanged`** — drop the `cdObject` / `chargeCdObject` identity compares. `MaterialChange` (added in the parent commit as a log gate) then folds back into it.

Rule to preserve: **emit = state changed, ticker = time passed.**

### Known constraints

- Ticker registration is currently gated on `cfg.showCooldownText`; it must become "any icon with an active cooldown" or curve updates stop when the user disables cooldown text.
- Branch 2 (charge recharge, `chargeCdObject`) needs the same treatment as branch 1.
- `GetSpellCooldownDuration` returns a **zeroed object, not nil**, for an idle spell — a non-nil handle is not an "is on cooldown" signal.
- `Assign()`/`Copy()` exist and work, but offer little here: you still fetch a fresh object to assign *from*, so the allocation remains.

### Acceptance criteria

- [ ] `SPELL_STATE` emits for a spell on an unchanged cooldown drop to ~0 (verify with `/kcd debug on`)
- [ ] Curve-driven visuals still update — in particular the icon brightening from cooldown alpha/tint to ready visuals in a cooldown's final ~1.6s (the `GCD_UPPER` step)
- [ ] Swipe animates smoothly with no stutter or restart
- [ ] Countdown text ticks continuously; charges badge stays live in combat where the count is secret
- [ ] Config changes (glow type/colour, cooldown text toggle) still take effect mid-cooldown
- [ ] No errors in combat — the whole point is that everything stays C-side
- [ ] `docs/smoke-tests.md` §9c passes
- [ ] `lua tests/run.lua` and `luacheck .` clean

### Environment

KickCD 1.2.0, Interface 120007. Related: 9fc0d8b (the 35% half + probe), `/kcd debug duration`, `docs/midnight-quirks.md`.

--- comment (tusharsaxena 2026-08-06):
### Context

GitHub issue #9 proposes moving the time-varying icon render onto the cooldown ticker. Reviewed in the 2026-07-31 pending audit and deferred.

### Evidence

Source: `GitHub issue #9 — move time-varying icon render onto the cooldown ticker`

Evidence hash: `a1507973`

### Deferral rationale

Not now — the issue is itself titled `[Optional]` and argues the case is structural rather than framerate, and this run already had the Castbar peel plus three `IconGrid_Render` changes touching the same ticker code.

### Provenance

Migrated from `docs/pending/LEDGER.md` row `ISS-09` (evidence hash `a1507973`), originally decided 2026-07-31.

--- comment (tusharsaxena 2026-09-07):
### 2026-09-07 remediation cycle — issue reconciliation (`M2-23`)

**Disposition: unaffected.**

Not scheduled, and the plan's stance is the same *optional* this issue already carries. `M4-22` names KickCD's per-cast closure at `modules/Castbar.lua:833` among three allocation candidates and rules: *"take them only with a scenario that measures them, added first — otherwise skip them."* Moving the time-varying render onto the 0.1s ticker is a larger version of the same trade and has no measurement behind it either.

Nothing in the cycle contradicts the analysis in this issue — `docs/midnight-quirks.md`'s secret-taint findings are untouched by every item that opens this repo. It stands as filed.

---
*Filed by work item `M2-23` of the **2026-09-07 review-and-standards-audit remediation** cycle — 207 triaged findings in 39 clusters across ten repositories, 106 work items in five milestones. The bundle lives in the `Ka0sAddonsCommonTasks` repo at `docs/2026-09-07-REVIEW_AND_STANDARDS_AUDIT_REMEDIATION/`: `01_CONSOLIDATED_FINDINGS.md` for the findings and clusters, `04_EXECUTION_PLAN.md` for the work items, `05_TRACEABILITY.md` for the finding-to-item map, `06_SMOKE_TESTS.md` for the six in-client sessions, `PROGRESS.md` for what has actually landed. `M2-23` gives every open issue in the eleven stores one of three dispositions — covered, unaffected, contradicted — and closes nothing.*

*State at the time of writing: **M1 complete** (38/38, LibKa0s v1.26.0 and v1.27.0 cut on the branch, the standard rolled to v2.39.0), **M2 in flight**, M3/M4/M5 not started, and no in-client smoke session performed.*


######## LibKa0s-1 — Perf: set regression thresholds and gates once baselines exist
Carried forward from the AbsorbTracker perf-instrumentation spec, where it was deferred as issue #17's last acceptance criterion.

Thresholds cannot be chosen before baseline numbers exist, and now they should not be chosen from a single addon either — the point of `LibKa0s-Perf` is that six addons emit comparable records.

**Blocked on:** rollout step 5 (all six consumers wired and producing captures).

**Decide then:**
- Whether any threshold gates CI, or whether this stays report-only like `docs/complexity.md`.
- Per-bucket ms/s ceilings, or a single delta-ms-per-frame ceiling, or both.
- Whether thresholds live in the lib (shared defaults) or per-addon in the descriptor.

Design context: `docs/superpowers/specs/2026-07-29-libka0s-perf-extraction-design.md` § Open questions.

--- comment (tusharsaxena 2026-08-06):
### Triage decision

- **Decision:** triaged
- **Decided:** 2026-08-07
- **Approach:** Unchanged — stays blocked on **rollout step 5**, all six consumers wired and producing captures. The thresholds get chosen from the collected baselines, not before.

### Rationale

Real work, but not now, and genuinely blocked rather than merely unstarted. Thresholds cannot be chosen before baseline numbers exist, and they should not be chosen from a single addon either — the point of `LibKa0s-Perf` is that six addons emit **comparable** records, so a threshold derived from one of them would be the wrong number wearing a shared name.

### The three decisions waiting on it

1. **Does any threshold gate CI**, or does this stay report-only like `docs/complexity.md`?
2. **What shape is the ceiling** — per-bucket ms/s, a single delta-ms-per-frame, or both?
3. **Where do thresholds live** — in the lib as shared defaults, or per-addon in the descriptor?

### A prerequisite worth naming

Rollout step 5 may not be reachable until **#5** (in-combat and out-of-combat capture variants) lands. Today's protocol is combat-gated, and out-of-combat addons — BankLedger and LootHistory — have nothing to measure under it, which is part of why neither has a Perf module built. "All six consumers producing captures" plausibly depends on that variant existing first.

This was not obvious from either issue read alone, and is recorded here so the dependency is not rediscovered when someone picks up step 5.

### Not done here

No code changed and no threshold was chosen. Triage records decisions; this one stays blocked by design.


--- comment (tusharsaxena 2026-09-07):
### 2026-09-07 remediation cycle — issue reconciliation (`M2-23`)

**Disposition: unaffected.**

Not scheduled. M1 spent fifteen items in this repository and none of them sets a perf regression threshold or a gate. The two that touch `Perf.lua` are `M1-LK-13` (reusing bracket slots from a high-water free list at `:478`, and taking `C_SpecializationInfo.GetSpecialization` before the bare global at `:615-618`) and `M1-LK-11` (five player-facing British spellings), neither of which produces a baseline.

What did change under this issue: `M1-LK-07` rewrote `testkit/run-automated-tests.sh` so the runner now emits the complexity watch list and one standing section per suite — the two things `automated-tests.md:221-224` MUSTs and the runner had never written. `M5-01` then regenerates the record in all ten repositories. That is the first time the collection will have comparable per-run figures in a generated file, which is the precondition this issue's *"once baselines exist"* is waiting on. Re-read it after `M5-01`.

---
*Filed by work item `M2-23` of the **2026-09-07 review-and-standards-audit remediation** cycle — 207 triaged findings in 39 clusters across ten repositories, 106 work items in five milestones. The bundle lives in the `Ka0sAddonsCommonTasks` repo at `docs/2026-09-07-REVIEW_AND_STANDARDS_AUDIT_REMEDIATION/`: `01_CONSOLIDATED_FINDINGS.md` for the findings and clusters, `04_EXECUTION_PLAN.md` for the work items, `05_TRACEABILITY.md` for the finding-to-item map, `06_SMOKE_TESTS.md` for the six in-client sessions, `PROGRESS.md` for what has actually landed. `M2-23` gives every open issue in the eleven stores one of three dispositions — covered, unaffected, contradicted — and closes nothing.*

*State at the time of writing: **M1 complete** (38/38, LibKa0s v1.26.0 and v1.27.0 cut on the branch, the standard rolled to v2.39.0), **M2 in flight**, M3/M4/M5 not started, and no in-client smoke session performed.*


######## LibKa0s-12 — A bucket's within can name a parent absent from the record
### Description

`docs/record-schema.md` introduces the per-bucket `within` field as the thing that makes a record
self-describing — carried on each bucket "so a reader can reconstruct the nesting without the
addon's source in hand". **That promise does not hold when the named parent recorded no calls.**

`Perf.Note` creates a bucket **lazily, on first observation** (`LibKa0s/Perf.lua:411-415`):

```lua
local b = buckets[key]
if not b then
  b = { calls = 0, totalMs = 0, maxMs = 0 }
  buckets[key] = b
end
```

A bucket that is declared in the descriptor but never noted during a capture therefore never enters
`buckets`, and never reaches the record — while any *child* that did fire still carries
`within = "<that parent>"`. The result is a dangling parent reference in the JSON.

**The library's own reader cannot notice.** `addBucketLines` and `addNestingNote` both fall back to
the live descriptor (`record.buckets[key].within or P.BUCKET_WITHIN[key]`, `LibKa0s/Perf.lua:214`
and `:265`), so in-process formatting stays correct. Only an **out-of-process reader of the JSON
alone** is affected — which is precisely `/wow-addon:perf-analysis` reading a frozen `dump.json`,
and precisely the case `within` was added for.

### Steps to reproduce

1. Declare two buckets where one nests in the other and the parent is not reached on every path —
   e.g. AbsorbTracker's `{ key = "appearance" }` and `{ key = "visibility", within = "appearance" }`
   (`AbsorbTracker/core/PerfSetup.lua:68` and `:72`).
2. Take an in-game capture in which the child fires and the parent does not.
3. Read the resulting `dump.json` without the addon's source in hand.

### Expected

Nesting is reconstructable from the record alone. Either the declared-but-unused parent appears with
zero counts, or the orphaned `within` is dropped from the child on the way into the record.

### Actual

In `AbsorbTracker/docs/perf-analysis/20260807-125002/dump.json`:

```jsonc
"visibility": { "calls": 21, "maxMs": 0.0915, "totalMs": 0.2388, "within": "appearance" }
```

…and `appearance` is not a key of `buckets` at all. A reader following `within` is pointed at a
parent that is not there.

### Environment

- LibKa0s **v1.13.0**, `LibKa0s-Perf-1.0` minor **7**, record `schema` **2**.
- Observed capture: AbsorbTracker 1.9.0, interface 120007, taken 2026-08-07.

**No runtime impact.** Nothing errors, nothing is lost, and no total is wrong: a parent with no calls
contributes nothing, so treating the orphaned child as top-level neither drops nor double-counts it.

### Provenance

Found while analysing [#1](https://github.com/tusharsaxena/LibKa0s/issues/1) (perf regression
thresholds), recorded in that analysis at
`Ka0sAddonsCommonTasks/docs/2026-08-24-LIBKA0S_PERF_THRESHOLDS/01_ANALYSIS.md` § 5. It did not
affect any figure in that analysis.

--- comment (tusharsaxena 2026-09-07):
### 2026-09-07 remediation cycle — issue reconciliation (`M2-23`)

**Disposition: unaffected.**

Not covered. `C24` (*LibKa0s options and perf seam defects*) is the cluster this would have belonged to, and its four findings are `LIBKA0S-R-08` (a composed reset button rendering live with a nil handler), `LIBKA0S-R-06` (`OptionsWidgets.lua:696`'s `local print = d.print or function() end` swallowing `NO_GROUPS`/`EMPTY_DROPDOWN`/`BUTTON_FAILED`), `LIBKA0S-R-07` (`Perf.lua:478` allocating a bracket table per open) and `LIBKA0S-A-10` (the un-namespaced `GetSpecialization`). All four landed in `M1-LK-13` and `M1-LK-06`. None of them is the record's `within` field.

So the lazy-bucket behaviour at `Perf.lua:411-415` is unchanged and `docs/record-schema.md`'s promise still does not hold for a declared-but-never-noted parent. Note that `M1-LK-13` **did** edit `Perf.lua:478`'s open path (bracket slots now come from a high-water free list), so re-read the line numbers in this issue against v1.27.0 before working on it.

---
*Filed by work item `M2-23` of the **2026-09-07 review-and-standards-audit remediation** cycle — 207 triaged findings in 39 clusters across ten repositories, 106 work items in five milestones. The bundle lives in the `Ka0sAddonsCommonTasks` repo at `docs/2026-09-07-REVIEW_AND_STANDARDS_AUDIT_REMEDIATION/`: `01_CONSOLIDATED_FINDINGS.md` for the findings and clusters, `04_EXECUTION_PLAN.md` for the work items, `05_TRACEABILITY.md` for the finding-to-item map, `06_SMOKE_TESTS.md` for the six in-client sessions, `PROGRESS.md` for what has actually landed. `M2-23` gives every open issue in the eleven stores one of three dispositions — covered, unaffected, contradicted — and closes nothing.*

*State at the time of writing: **M1 complete** (38/38, LibKa0s v1.26.0 and v1.27.0 cut on the branch, the standard rolled to v2.39.0), **M2 in flight**, M3/M4/M5 not started, and no in-client smoke session performed.*


######## LibKa0s-17 — C12/ABSORBTRACKER-A-10: tab-strip geometry has no invariance case in AbsorbTracker — deferred to kit 16
**Finding `ABSORBTRACKER-A-10`** (AbsorbTracker) — from the 2026-09-07 review and standards audit remediation bundle,
`docs/2026-09-07-REVIEW_AND_STANDARDS_AUDIT_REMEDIATION/` in the Ka0sAddonsCommonTasks repo — cluster
`C12`, rule `options-ui-§13`, severity **low**. Filed by `M5-07` on LibKa0s as the kit's owner, one issue
per consumer row. Its three siblings are the other consumers: the four are `ABSORBTRACKER-A-10`,
`MULTIMETERS-A-08`, `PANELMASTER-A-07` and `PRETTYCHAT-A-10`.

### What AbsorbTracker filed

`tests/test_widgets.lua:770` — the only assertion is `assertTrue(ctx.chromeHeight > 0, ...)`; nothing asserts that the band height and the row y offsets are equal across every selection. **Remedy when the kit allows it:** a wrapping-page case asserting `chromeHeight` and each row's y offset are identical per selection, with mock heights varied so the case can fail.

### Why it is filed on LibKa0s and not on the consumer

The obstacle is the shared kit's fidelity contract, which this repository owns. `testkit/mock_base.lua`
returned 0 from `GetHeight` for every frame and defined no `SetAtlas` at all, so `OptionsWidgets.lua:433-442`'s
atlas-derived tab pitch always took its `L.TAB_H` fallback and **any `options-ui-§13` invariance assertion
passed vacuously**. Four repositories independently filed the same missing case; not one of them could write
it, and none of them could fix it either.

### What kit 15 shipped, and where it stopped

`M1-LK-08` — `24946a5` *"the shared mock can be asked how tall something is, and still answers zero by
default"* — is **purely additive**:

- `SetAtlas(name, useAtlasSize)` records what it was told and writes a height from a kit-published atlas
  table (`testkit/mock_base.lua:143-153`).
- `f:__setGeom(w, h)` is the opt-in (`:141`).
- `GetHeight` still answers zero unless geometry was armed (`:132` —
  `return (self.__geomLive and self.__geomH) or 0`).

That default is deliberate. Roughly **308 test files across ten repositories** lean on geometry answering
zero, and every assertion that passes today *because* of that flips with it. `03_SPEC.md` § `C12` puts the
flip in **kit 16** — a tag this plan does not cut — together with the cases themselves, and names flipping
`GetHeight` in kit 15 as an explicit non-goal. Kit is at `Kit.VERSION = 15` today
(`testkit/framework.lua:20`).

### So this row is deferred, not fixed

`05_TRACEABILITY.md` Part 4 says it plainly: after this plan the four findings are still open, with the
obstacle removed, and **no work item in this plan writes a tab-strip geometry case in any of the four
repositories**. The rows are marked `deferred` rather than `fix` for exactly that reason. What covers the
interval is an operator: `06_SMOKE_TESTS.md` § 3.5 cycles every multi-tab panel in all nine addons after the
`M4-01` wave — a weaker check than the four findings ask for, named rather than left unstated.

### What closes it

Kit 16: `GetHeight` returns recorded geometry by default, once each consumer has adopted the opt-in where it
needs it. Then the consumer above carries a case asserting the chrome band height and every row's y offset
are identical across each tab selection, **verified red** under a mutation to the tab atlas heights. A green
case written before the flip proves nothing, which is the whole reason this is parked instead of closed.



######## LibKa0s-18 — C12/MULTIMETERS-A-08: tab-strip geometry has no invariance case in MultiMeters — deferred to kit 16
**Finding `MULTIMETERS-A-08`** (MultiMeters) — from the 2026-09-07 review and standards audit remediation bundle,
`docs/2026-09-07-REVIEW_AND_STANDARDS_AUDIT_REMEDIATION/` in the Ka0sAddonsCommonTasks repo — cluster
`C12`, rule `options-ui-§13`, severity **low**. Filed by `M5-07` on LibKa0s as the kit's owner, one issue
per consumer row. Its three siblings are the other consumers: the four are `ABSORBTRACKER-A-10`,
`MULTIMETERS-A-08`, `PANELMASTER-A-07` and `PRETTYCHAT-A-10`.

### What MultiMeters filed

`tests/test_options_panel.lua:630-640` — confirmed: the nearest case asserts `activeTab` and `#__tabKids >= 2` only, and a grep for `wrap` in that file returns zero hits. **Remedy when the kit allows it:** make `wow_mock` answer different selected/unselected atlas heights, then assert the chrome band and every row y offset are selection-invariant.

### Why it is filed on LibKa0s and not on the consumer

The obstacle is the shared kit's fidelity contract, which this repository owns. `testkit/mock_base.lua`
returned 0 from `GetHeight` for every frame and defined no `SetAtlas` at all, so `OptionsWidgets.lua:433-442`'s
atlas-derived tab pitch always took its `L.TAB_H` fallback and **any `options-ui-§13` invariance assertion
passed vacuously**. Four repositories independently filed the same missing case; not one of them could write
it, and none of them could fix it either.

### What kit 15 shipped, and where it stopped

`M1-LK-08` — `24946a5` *"the shared mock can be asked how tall something is, and still answers zero by
default"* — is **purely additive**:

- `SetAtlas(name, useAtlasSize)` records what it was told and writes a height from a kit-published atlas
  table (`testkit/mock_base.lua:143-153`).
- `f:__setGeom(w, h)` is the opt-in (`:141`).
- `GetHeight` still answers zero unless geometry was armed (`:132` —
  `return (self.__geomLive and self.__geomH) or 0`).

That default is deliberate. Roughly **308 test files across ten repositories** lean on geometry answering
zero, and every assertion that passes today *because* of that flips with it. `03_SPEC.md` § `C12` puts the
flip in **kit 16** — a tag this plan does not cut — together with the cases themselves, and names flipping
`GetHeight` in kit 15 as an explicit non-goal. Kit is at `Kit.VERSION = 15` today
(`testkit/framework.lua:20`).

### So this row is deferred, not fixed

`05_TRACEABILITY.md` Part 4 says it plainly: after this plan the four findings are still open, with the
obstacle removed, and **no work item in this plan writes a tab-strip geometry case in any of the four
repositories**. The rows are marked `deferred` rather than `fix` for exactly that reason. What covers the
interval is an operator: `06_SMOKE_TESTS.md` § 3.5 cycles every multi-tab panel in all nine addons after the
`M4-01` wave — a weaker check than the four findings ask for, named rather than left unstated.

### What closes it

Kit 16: `GetHeight` returns recorded geometry by default, once each consumer has adopted the opt-in where it
needs it. Then the consumer above carries a case asserting the chrome band height and every row's y offset
are identical across each tab selection, **verified red** under a mutation to the tab atlas heights. A green
case written before the flip proves nothing, which is the whole reason this is parked instead of closed.



######## LibKa0s-19 — C12/PANELMASTER-A-07: tab-strip geometry has no invariance case in PanelMaster — deferred to kit 16
**Finding `PANELMASTER-A-07`** (PanelMaster) — from the 2026-09-07 review and standards audit remediation bundle,
`docs/2026-09-07-REVIEW_AND_STANDARDS_AUDIT_REMEDIATION/` in the Ka0sAddonsCommonTasks repo — cluster
`C12`, rule `options-ui-§13`, severity **low**. Filed by `M5-07` on LibKa0s as the kit's owner, one issue
per consumer row. Its three siblings are the other consumers: the four are `ABSORBTRACKER-A-10`,
`MULTIMETERS-A-08`, `PANELMASTER-A-07` and `PRETTYCHAT-A-10`.

### What PanelMaster filed

`tests/wow_mock.lua:165` and `tests/_kit/mock_base.lua:97` — `OptionsWidgets.lua:434-435` measures pitch from unselected atlas art, but the mock's `GetHeight` answers 0 for any atlas, so `tabArtHeight` always falls back. The cited locus was corrected in triage: `wow_mock`'s `reader("__h")` is the effective definition, and `SetAtlas` never wrote `__h`. **Remedy when the kit allows it:** give `wow_mock` a per-atlas height, then assert band height and every row y-offset stay equal across active tabs, verified red under the `TAB_ATLAS` mutation.

### Why it is filed on LibKa0s and not on the consumer

The obstacle is the shared kit's fidelity contract, which this repository owns. `testkit/mock_base.lua`
returned 0 from `GetHeight` for every frame and defined no `SetAtlas` at all, so `OptionsWidgets.lua:433-442`'s
atlas-derived tab pitch always took its `L.TAB_H` fallback and **any `options-ui-§13` invariance assertion
passed vacuously**. Four repositories independently filed the same missing case; not one of them could write
it, and none of them could fix it either.

### What kit 15 shipped, and where it stopped

`M1-LK-08` — `24946a5` *"the shared mock can be asked how tall something is, and still answers zero by
default"* — is **purely additive**:

- `SetAtlas(name, useAtlasSize)` records what it was told and writes a height from a kit-published atlas
  table (`testkit/mock_base.lua:143-153`).
- `f:__setGeom(w, h)` is the opt-in (`:141`).
- `GetHeight` still answers zero unless geometry was armed (`:132` —
  `return (self.__geomLive and self.__geomH) or 0`).

That default is deliberate. Roughly **308 test files across ten repositories** lean on geometry answering
zero, and every assertion that passes today *because* of that flips with it. `03_SPEC.md` § `C12` puts the
flip in **kit 16** — a tag this plan does not cut — together with the cases themselves, and names flipping
`GetHeight` in kit 15 as an explicit non-goal. Kit is at `Kit.VERSION = 15` today
(`testkit/framework.lua:20`).

### So this row is deferred, not fixed

`05_TRACEABILITY.md` Part 4 says it plainly: after this plan the four findings are still open, with the
obstacle removed, and **no work item in this plan writes a tab-strip geometry case in any of the four
repositories**. The rows are marked `deferred` rather than `fix` for exactly that reason. What covers the
interval is an operator: `06_SMOKE_TESTS.md` § 3.5 cycles every multi-tab panel in all nine addons after the
`M4-01` wave — a weaker check than the four findings ask for, named rather than left unstated.

### What closes it

Kit 16: `GetHeight` returns recorded geometry by default, once each consumer has adopted the opt-in where it
needs it. Then the consumer above carries a case asserting the chrome band height and every row's y offset
are identical across each tab selection, **verified red** under a mutation to the tab atlas heights. A green
case written before the flip proves nothing, which is the whole reason this is parked instead of closed.



######## LibKa0s-20 — C12/PRETTYCHAT-A-10: tab-strip geometry has no invariance case in PrettyChat — deferred to kit 16
**Finding `PRETTYCHAT-A-10`** (PrettyChat) — from the 2026-09-07 review and standards audit remediation bundle,
`docs/2026-09-07-REVIEW_AND_STANDARDS_AUDIT_REMEDIATION/` in the Ka0sAddonsCommonTasks repo — cluster
`C12`, rule `options-ui-§13`, severity **low**. Filed by `M5-07` on LibKa0s as the kit's owner, one issue
per consumer row. Its three siblings are the other consumers: the four are `ABSORBTRACKER-A-10`,
`MULTIMETERS-A-08`, `PANELMASTER-A-07` and `PRETTYCHAT-A-10`.

### What PrettyChat filed

`tests/_kit/mock_base.lua:97` plus an absent case in `tests/test_panel.lua` — `mock_base.lua:97` was `function f:GetHeight() return 0 end` for every frame, so any geometry-invariance assertion would pass vacuously. Kept low in triage as a real gap, topical after the tab revamp, whose fix touches the shared kit's fidelity contract rather than this repository. **Remedy when the kit allows it:** give atlas-bearing textures per-atlas heights in `tests/wow_mock.lua`, then assert band and row offsets are identical across selections.

### Why it is filed on LibKa0s and not on the consumer

The obstacle is the shared kit's fidelity contract, which this repository owns. `testkit/mock_base.lua`
returned 0 from `GetHeight` for every frame and defined no `SetAtlas` at all, so `OptionsWidgets.lua:433-442`'s
atlas-derived tab pitch always took its `L.TAB_H` fallback and **any `options-ui-§13` invariance assertion
passed vacuously**. Four repositories independently filed the same missing case; not one of them could write
it, and none of them could fix it either.

### What kit 15 shipped, and where it stopped

`M1-LK-08` — `24946a5` *"the shared mock can be asked how tall something is, and still answers zero by
default"* — is **purely additive**:

- `SetAtlas(name, useAtlasSize)` records what it was told and writes a height from a kit-published atlas
  table (`testkit/mock_base.lua:143-153`).
- `f:__setGeom(w, h)` is the opt-in (`:141`).
- `GetHeight` still answers zero unless geometry was armed (`:132` —
  `return (self.__geomLive and self.__geomH) or 0`).

That default is deliberate. Roughly **308 test files across ten repositories** lean on geometry answering
zero, and every assertion that passes today *because* of that flips with it. `03_SPEC.md` § `C12` puts the
flip in **kit 16** — a tag this plan does not cut — together with the cases themselves, and names flipping
`GetHeight` in kit 15 as an explicit non-goal. Kit is at `Kit.VERSION = 15` today
(`testkit/framework.lua:20`).

### So this row is deferred, not fixed

`05_TRACEABILITY.md` Part 4 says it plainly: after this plan the four findings are still open, with the
obstacle removed, and **no work item in this plan writes a tab-strip geometry case in any of the four
repositories**. The rows are marked `deferred` rather than `fix` for exactly that reason. What covers the
interval is an operator: `06_SMOKE_TESTS.md` § 3.5 cycles every multi-tab panel in all nine addons after the
`M4-01` wave — a weaker check than the four findings ask for, named rather than left unstated.

### What closes it

Kit 16: `GetHeight` returns recorded geometry by default, once each consumer has adopted the opt-in where it
needs it. Then the consumer above carries a case asserting the chrome band height and every row's y offset
are identical across each tab selection, **verified red** under a mutation to the tab atlas heights. A green
case written before the flip proves nothing, which is the whole reason this is parked instead of closed.



######## LibKa0s-35 — tests/test_options.lua: peel the render/refresh block into test_options_render.lua (1339, on notice)
`tests/test_options.lua` is **1339 lines**, inside `layout-§1`'s 1000–1500 on-notice band, measured 2026-09-24 with `wc -l` (v1.56.0 unreleased). It has carried "owed a tracked ID" in `docs/automated-tests/RESULTS.md`'s watch list for many releases without one; this is that ID (audit finding `LibKa0s-A-03`).

### The seam

The render/refresh block: `-- ── the page registry and the two refresh tiers` (line 439 as measured today) running to just before `-- ── LSMValues` (line 718), about 280 lines. It peels whole to a new suite, `tests/test_options_render.lua`, registered in `tests/run.lua` beside `tests/test_options_bulk.lua` and `tests/test_options_fontpreload.lua`, which are the precedent: a coherent block of cases with a seam of its own, taken to its own suite. The case count must be identical before and after.

### Trigger

The next case appended to `tests/test_options.lua`, or the file reaching 1450 lines — whichever comes first. Until then the file is on notice, not in breach.

### Terminal state

`CLAUDE.md` § *Files over the 1500-line cap* names this issue in its band paragraph; `RESULTS.md`'s Disposition cell reads "already tracked as #NN".



######## LibKa0s-36 — LibKa0s/Widgets.lua: split into per-widget files (1266, on notice)
`LibKa0s/Widgets.lua` is **1266 lines**, inside `layout-§1`'s 1000–1500 on-notice band, measured 2026-09-24 with `wc -l` after `LK-21`'s minor 10. Its RESULTS.md watch-list entry recorded its own shelf life as crossed with the promised issue never opened; this is that issue (audit finding `LibKa0s-A-03`).

### The seam

Per-widget files. The file already holds three unrelated widgets under their own banners:

- the dropdown and its menu (`MakeDropdown`, `lib.Dropdown`, `lib.CloseMenu`, lines 58–431 as measured today);
- `-- ── the copy window` (`lib.CopyWindow`, lines 432–620);
- `-- ── ReorderList` with its handle pool, row box and drag (lines 621–end).

`LibKa0s/WidgetsDragHandle.lua` (v1.48.0) is the precedent. The likeliest first cut is `ReorderList` out to `LibKa0s/WidgetsReorder.lua`, the largest and most self-contained block. A peel here is a release: a payload file, a `LibKa0s.xml` row, its own LibStub minor, a `tests/majors.lua` row, the multi-file pairing guard, a component on the major's version key, an API document and a regenerated manifest.

### Trigger

The next member added to `LibKa0s/Widgets.lua`, or the file reaching 1450 lines.

### Terminal state

`CLAUDE.md` § *Files over the 1500-line cap* names this issue in its band paragraph; `RESULTS.md`'s Disposition cell reads "already tracked as #NN".



######## LibKa0s-38 — tests/test_schema.lua: split by pipeline stage (1335, on notice)
`tests/test_schema.lua` is **1335 lines**, inside `layout-§1`'s 1000–1500 on-notice band, measured 2026-09-24 with `wc -l` (1101 when new at v1.55.0, 1233 before `LK-22` / `LK-23`). Its RESULTS.md Disposition cell was blank (audit finding `LibKa0s-A-03`); this issue is its disposition.

### The seam

Split by pipeline stage. The suite is already banner-separated along the Schema major's pipeline (line numbers as measured today):

- fixtures and the reference degradation stub (19–376) — shared setup;
- the major, path primitives, the registry (377–694);
- `-- ── the write seam` (695–936);
- defaults, the bulk bracket, the profile reset's count (937–1181);
- `-- ── the shape check` (1182–end).

The first cut is the write stage onward (write seam + bulk bracket + reset count), to `tests/test_schema_write.lua`; the fixtures move to a local helper both suites load. The case count must be identical before and after.

### Trigger

The next case appended to `tests/test_schema.lua`, or the file reaching 1450 lines.

### Terminal state

`CLAUDE.md` § *Files over the 1500-line cap* names this issue in its band paragraph; `RESULTS.md`'s Disposition cell reads "already tracked as #NN".



######## LibKa0s-40 — Slash: parseBool, allowedText and parseColor read lib.STRINGS directly, so a host's L overrides cannot reach them
**Bug.** In `LibKa0s/Slash.lua` (v1.61.0), the file-level parsers `parseBool`, `allowedText` and `parseColor` read `lib.STRINGS` directly (around :281, :356, :381, :387), above `lib:New` (:484). A host's localized `L` overrides passed to its Slash instance therefore never reach them, and those strings always come out in the library's defaults.

**Consumer impact.** ConsumableMaster#16 ("Three Slash `L` overrides cannot be reached") is blocked on this: its `settings/Slash.lua:431-439` marks the three overrides dead. Any other host that localizes those strings has the same gap. Broader i18n is LibKa0s#6; this is the concrete defect.

**Fix direction.** Move the three parsers onto the instance (or pass the instance's string resolver into them) so they read the host's `L` like the rest of the Slash surface, bump Slash's LibStub minor, add a test that a host override is used, then re-vendor and close ConsumableMaster#16.

Found by the 2026-09-26 issue audit.



######## LibKa0s-7 — Perf.lua sits in the layout-§1 on-notice band (1163 LOC)
### Description

`LibKa0s/Perf.lua` is **1163 LOC**, inside `layout-§1`'s 1000–1500 *on notice* band. It is the
only shipped file in the band and the widest surface consumers bind against.

This issue exists to **discharge a shelf-life obligation, not to schedule a split.** The file is
under the 1500 cap, so nothing is in violation. `automated-tests-§4` (anti-pattern #53) says a
watch-list disposition carried as *Accepted* across three consecutive **release** runs is owed
either a fix or a tracked deviation ID with an owner. This one has been carried through v1.8.0
(`20260805-123655`), v1.8.1 (`20260806-180959`) and v1.8.2 (`20260807-105553`), so the clock
expired at v1.8.2. This is the ID.

### Why it is not being split now

The diagnosis is **breadth, not knots** — worst function in the file is `groupContext` at CCN 11,
and the file's average CCN is 3.4. There is no tangle to unpick.

Splitting a *library* file also costs more than splitting an addon file: it touches `LibKa0s.xml`
load order, the LibStub major boundaries, and every consumer that vendors `libs/LibKa0s/` **whole**
(anti-pattern #48). Spending that churn to move a file from 1163 to two files around 580 each, with
337 lines of headroom under the cap, buys nothing a reader or a consumer can feel.

### The plan if it does cross 1500

The peel seam is already identified: **the sampler** and **the group/scenario bookkeeping** are the
two coherent halves. `layout-§1` MAYs a peel into 2–3 sibling files in the same folder, so the
shape would be `LibKa0s/Perf.lua` + `LibKa0s/Perf_Sampler.lua` (or similar), both listed in
`LibKa0s.xml` in dependency order, with the LibStub major unchanged so no consumer re-binds.

### Trigger

- **Hard:** the file crosses **1500 LOC** — at that point `layout-§1` is a MUST failure and the peel
  above is executed, not re-argued.
- **Soft:** re-read at each release run. The figure has been static at 1163 since
  `20260805-002859`; it last grew for the observed-containment record and the keyed `Open`/`Close`
  bracket.

### Disposition recorded in the record

`docs/automated-tests/RESULTS.md` → `## Complexity watch list` → *Files by `layout-§1` band* now
reads **Already tracked as this issue** rather than *Accepted, expired*.

--- comment (tusharsaxena 2026-08-07):
### Triage decision

- **Decision:** triaged
- **Decided:** 2026-08-07
- **Approach:** Hold this issue open as the tracked deviation ID with an owner, discharging the `automated-tests-§4` / anti-pattern #53 shelf-life obligation. No peel now. Re-evaluate only on the triggers already recorded in the body — hard at 1500 LOC, where `layout-§1` becomes a MUST failure and the sampler / group-and-scenario-bookkeeping seam is taken.

### Rationale

Kept open as real work, not now — which is precisely what this issue was created to be. The
disposition had been carried as *Accepted* across three consecutive release runs (v1.8.0
`20260805-123655`, v1.8.1 `20260806-180959`, v1.8.2 `20260807-105553`), and #53 owes either a fix or
a tracked ID at that point. This is the ID, so closing it would put the disposition straight back to
*Accepted with no owner* and the obligation would fall due again at the next release.

Not splitting is the substantive half of the decision: the diagnosis is breadth rather than knots
(worst function `groupContext` at CCN 11, file average CCN 3.4), there are 337 lines of headroom, and
a library split costs `LibKa0s.xml` load order, the LibStub major boundary and a whole-folder
re-vendor into every consumer — churn that buys nothing a reader or a consumer can feel.

*(Rationale inferred from the option chosen; no free-text reason was given.)*

--- comment (tusharsaxena 2026-09-07):
### 2026-09-07 remediation cycle — issue reconciliation (`M2-23`)

**Disposition: covered.**

**Cluster `C22` (`layout-§1`'s 1500-LOC cap breached in four repos, and unclassified for a library) · work item `M1-STD-08`, landed as `a171735`, with `M4-14` the sweep.**

This issue was filed against a section that did not say whether it applied here. `M1-STD-08` settles it. `layout-§1` now carries an explicit *What the cap binds (MUST)* block: **every authored `.lua` file the repository tracks, wherever in the tree it sits — `tests/` included, and a Ka0s-owned library repo's own module folder included (`library-stack-§7`)**, with exactly two carve-outs (vendored code, and generated non-shipping data meeting all three conditions). `LibKa0s/Perf.lua` is authored, tracked and in this repo's module folder, so the 1000–1500 on-notice band binds it and the 1163 figure is a real classification rather than an open question.

The amendment names this repository as one of the four divergent readings that motivated it: *"LibKa0s graded its two breaches Low and left them there because nothing said the cap reached a library repo at all."*

It also names what discharges the obligation. A file has **three** terminal states — peeled, or **an open issue in the addon's issue store naming the seam a peel would follow**, or a ratified deviation row with a re-check trigger — and *"an audit MUST NOT re-file `layout-§1` against a file covered by the second or the third"*. This issue is that second state. `M4-14` then dispositions every file still over the cap in this repo among five; keep this issue open as the band's record, and make sure it names the seam explicitly when `M4-14` runs.

---
*Filed by work item `M2-23` of the **2026-09-07 review-and-standards-audit remediation** cycle — 207 triaged findings in 39 clusters across ten repositories, 106 work items in five milestones. The bundle lives in the `Ka0sAddonsCommonTasks` repo at `docs/2026-09-07-REVIEW_AND_STANDARDS_AUDIT_REMEDIATION/`: `01_CONSOLIDATED_FINDINGS.md` for the findings and clusters, `04_EXECUTION_PLAN.md` for the work items, `05_TRACEABILITY.md` for the finding-to-item map, `06_SMOKE_TESTS.md` for the six in-client sessions, `PROGRESS.md` for what has actually landed. `M2-23` gives every open issue in the eleven stores one of three dispositions — covered, unaffected, contradicted — and closes nothing.*

*State at the time of writing: **M1 complete** (38/38, LibKa0s v1.26.0 and v1.27.0 cut on the branch, the standard rolled to v2.39.0), **M2 in flight**, M3/M4/M5 not started, and no in-client smoke session performed.*


######## LibKa0s-9 — Establish today's zero-consumer export set, and retire the host duplicates behind it
LibKa0s carries public exports that no host calls, while the addons still ship their own duplicates of
the same behaviour. Under `-1.0`'s frozen additive-only rule there is no deprecation available, so
every one of those exports is permanent — which makes "who actually calls this" a question worth
answering once, deliberately, rather than re-deriving per adoption cycle.

Filed as discovery. The first task is measurement, because the three records the repo already has
**disagree with each other**, and none of them is today's number.

## What the existing records say

**1. `docs/adoption-prompt.md:776` — "Thinly-consumed surfaces", stamped as of v1.5.0.** Names
**two** zero-consumer surfaces:

- `makeCloseButton` (DebugLog minor 4) — both hosts that once passed it dropped it deliberately once
  Core minor 3 made the Ka0s edge the library's own default.
- `skin` (DebugLog) — same state, reached the same way.

That section is explicit that it carries consumer counts "deliberately, so that the next drift shows
up as a wrong number rather than as a heading nobody re-reads." This issue is that drift showing up.

**2. `docs/adoption/2026-08-01-v2/03_DEVIATIONS.md:634` (frozen).** Names **eight**:
`lib.FormatKV`, `lib.MAX_BUFFER`, `Sl:HelpHeader`, `Sl:HelpRows` called by name, `D:LastLine`,
`O.__pages`, the `skin` descriptor field and the `ring` descriptor field.

It also flags the interesting one: *"`HelpRows` is the notable one — every host reaches it through
`PrintHelp`, so the indented half of the row-formatter pair has no caller anywhere outside the
library, and the only textual hits in the collection are inside KickCD's own degradation stub."*
That is the whole difficulty in one sentence.

**3. A textual census run today** across the eight addons (excluding `libs/` and `tests/_kit/`) found
exactly three module-level exports with **no mention anywhere**: `DEFAULT_RING`, `FindCommand`,
`SplitVerb`.

## Why the census cannot be taken at face value, and why that is the finding

A name appearing in an addon does not mean the library's export is called. Every high-count name in
that census resolves to one of three things:

| Shape | What it means |
|---|---|
| A real call into the library | the export has a consumer |
| A **host-owned duplicate** of the same function | the convergence has not happened here |
| A **degradation stub** naming the member so a missing library cannot crash the addon | neither a call nor a duplicate |

`HelpRows` is the worked example: 15 files mention it and its consumer count is zero. Separating
these three shapes per export is the actual work this issue is asking for — a `grep` count is what
produced the disagreement above, not what resolves it.

## Why it matters

- **`-1.0` is frozen additive-only.** There is no deprecation path inside the major, so an export
  with no caller cannot be renamed or removed — it can only be worked around later. An assumption
  baked into a zero-consumer surface is permanent, and its shape is currently pinned by nothing but
  the library's own guess about what a host would want.
- **A host duplicate is the thing the convergence exists to eliminate.** The 2026-08-01 bundle already
  records the sharp case: AbsorbTracker's degraded stub reimplements `FormatRow`'s format string, "a
  second copy of the one formatter the convergence exists to eliminate."
- **No single suite covers a thinly-consumed surface.** The bundle's own reading: the Options page
  registry and the Slash schema-CLI tail "are each carried by two hosts at most, and the two hosts
  differ per surface — so no single consumer's suite covers either half, and a change to either has
  to be reasoned about rather than tested." A zero-consumer surface is that failure at its limit —
  only the library's own suite stands behind it.

## Direction

1. **Measure.** Per public export, per host, classify each textual hit as call / host duplicate /
   degradation stub. Produce today's zero-consumer set with file:line evidence, and correct
   `docs/adoption-prompt.md`'s "Thinly-consumed surfaces" counts, which are stamped v1.5.0 and are
   the file that is supposed to make drift visible.
2. **Split the result three ways.** A zero-consumer export with a host duplicate behind it is an
   **adoption** task in that host. One with no duplicate and no plausible host is a **documentation**
   task — say in the API docs that it is uncalled and why it still exists. One whose shape is
   suspect is worth settling *before* a first host adopts it, since first contact is the last moment
   the contract can be argued about.
3. **Do not delete anything.** Additive-only means the exports stay whatever the census says.

## Related

- #2 — *Decide which further modules move into LibKa0s.* Adjacent but the opposite direction: that
  issue is about moving host code **into** the library; this one is about hosts adopting what the
  library **already exports**.
- The per-addon adoption ledgers (`LIBKA0S-*`) already record several deliberate declines with
  reasons — those are answers, not gaps, and the census should not re-open them.

--- comment (tusharsaxena 2026-08-07):
### Triage decision

- **Decision:** triaged
- **Decided:** 2026-08-07
- **Approach:** Census first — per public export, per host, classify every textual hit as a real call, a host-owned duplicate, or a degradation stub, with file:line. Produce today's zero-consumer set and correct `docs/adoption-prompt.md`'s v1.5.0 counts. Then split the result three ways: a zero-consumer export with a host duplicate behind it is an **adoption** task in that host; one with no duplicate and no plausible host is a **documentation** task; one whose shape is suspect is a **contract to settle before** a first host adopts it. Delete nothing — `-1.0` is additive-only.

### Rationale

Kept open as real work, not now. The census is a substantial sitting in its own right and was not
going to happen mid-triage. Recording the approach means whoever picks it up starts from a decision
rather than a blank page — which matters more here than usual, because the three existing records
disagree and the obvious method (a `grep` count) is the one that produced the disagreement.

*(Rationale inferred from the option chosen; no free-text reason was given.)*

--- comment (tusharsaxena 2026-09-07):
### 2026-09-07 remediation cycle — issue reconciliation (`M2-23`)

**Disposition: contradicted.**

**The plan decided against the retirement half of this, for the one export where it was concretely proposed.**

`CX06` (*`lib.MakeCloseButton`'s third argument forces the same wrapper into eight repos and two declines*, 10 repos) is this issue's shape made specific: a library export, eight host duplicates of the same three-line wrapper, and a proposal to retire them behind a rebind. `04_EXECUTION_PLAN.md` § *What this plan deliberately does not do* declines it:

> Payoff is roughly 24 lines across eight three-line wrappers. Cost is a signature change to a surface all nine consumers vendor, forcing a re-vendor wave for cosmetics — and it is contradicted by the library's own reasoning at `LibKa0s/Media.lua:14-20`, which records that `...` carries the addon folder name only for a file the TOC loads directly, so the library cannot infer it. The cheap close is `M1-STD-04` plus one BankLedger register row in `M5-02`.

`M1-STD-04` landed (`07ec867`) and `M5-02` will carry the row. The decline also corrects a stale premise this issue inherits: the old *"BankLedger and LootHistory declined"* is one release out of date — `LootHistory/core/CoreSetup.lua:167` wraps it correctly and `:19-25` records that its decline *"expired with LibKa0s v1.10"*.

**What survives.** The measurement half — establishing today's zero-consumer export set — was not done and is not contradicted; the three records this issue cites still disagree with each other and none is today's number. What is now decided is that *finding* a zero-consumer export does not by itself justify a signature change under `-1.0`'s frozen additive-only rule. Any future retirement has to clear the `CX06` bar: more than cosmetic payoff, or no re-vendor wave.

**Re-triage:** `severity:medium` → `severity:low`. The half with a concrete proposal behind it is decided against; what remains is a measurement task with no consumer waiting on it.

---
*Filed by work item `M2-23` of the **2026-09-07 review-and-standards-audit remediation** cycle — 207 triaged findings in 39 clusters across ten repositories, 106 work items in five milestones. The bundle lives in the `Ka0sAddonsCommonTasks` repo at `docs/2026-09-07-REVIEW_AND_STANDARDS_AUDIT_REMEDIATION/`: `01_CONSOLIDATED_FINDINGS.md` for the findings and clusters, `04_EXECUTION_PLAN.md` for the work items, `05_TRACEABILITY.md` for the finding-to-item map, `06_SMOKE_TESTS.md` for the six in-client sessions, `PROGRESS.md` for what has actually landed. `M2-23` gives every open issue in the eleven stores one of three dispositions — covered, unaffected, contradicted — and closes nothing.*

*State at the time of writing: **M1 complete** (38/38, LibKa0s v1.26.0 and v1.27.0 cut on the branch, the standard rolled to v2.39.0), **M2 in flight**, M3/M4/M5 not started, and no in-client smoke session performed.*


######## LootHistory-32 — Peel modules/Analytics.lua: renderers vs formatting/segmenting helpers
modules/Analytics.lua is 1200 lines, in the 1000-1500 watch band (layout-§1 / automated-tests-§4). docs/automated-tests/RESULTS.md has carried its Disposition as "Peel next" for seven runs with nothing tracking it.

Split the chart renderers (pooled bar/strip/list renderers) from the formatting and segmenting helpers, so the Insights view file stays well clear of the 1500-line cap.

Source: docs/audits/2026-09-23 LH-52 (finding LootHistory-A-20; remediation item LH-35).


######## MultiMeters-56 — Tighten the None-source admission: an enemy can carry a player class
**Finding (owner's in-client diagnostics, 2026-09-26).** After fighting a PvP Training Dummy, `/mm diagnostics` reported `enemies carrying a player class: 1 of 1` — `[1] name=PvP Training Dummy guid=plain creatureID=243211 display=0 class=WARRIOR`. So an NPC can carry a `RAID_CLASS_COLORS` class filename, and the client files the enemy column's sources under display type None (0), not Enemy (2).

**Why it matters.** The aggregator's companion rule (`modules/Aggregator.lua`, around :751-766: a None source with a player class is admitted as a companion) is now the only thing that would stop a mob from reaching a grid column, and it would admit a classed mob. `isEnemySource` (around :721-724) keys on Enemy (2), which never arrives, and identity mode (`modules/Aggregator_Identity.lua` around :255 and :631) relies on it alone.

**Nothing is wrong in practice today.** In the same session the grid showed only the player (DamageDone had one source); mobs have never been seen in the ally meter types. This is hardening.

**Fix direction.** Tighten the None admission, for example require a Player-style GUID or a known companion creature ID (careful: Valeera's GUID is `Creature-…`, see `tests/test_aggregator.lua` around :786), and decide whether to keep or retire the Enemy gate. Tests first: a classed NPC source in DamageDone is refused; a companion is still admitted.

Background: MultiMeters c374876 (diagnostics now report the class count), docs/midnight-quirks.md "Enemies are filed under None, not Enemy".



######## PanelMaster-15 — Panel level has no options UI and stays CLI-only
### Context
A `Known limitations` entry in `docs/ARCHITECTURE.md`: there is no UI for a panel's `level`, so it can only be set from the command line.

### Evidence
`docs/ARCHITECTURE.md` ▸ Known limitations

Evidence hash: `10a1babb`

### Deferral rationale
Deferral re-affirmed. Hash moved from `904842e7` because the entry's text was corrected once panel levels became strided — the *limitation* is unchanged (still no level UI, `level` still CLI-only), only its description of cross-panel ordering.

### Provenance
Migrated from `docs/pending/LEDGER.md` row `DOC-04` (evidence hash `10a1babb`), originally decided 2026-07-31.

--- comment (tusharsaxena 2026-09-07):
### 2026-09-07 remediation cycle — issue reconciliation (`M2-23`)

**Disposition: unaffected.**

No finding names panel `level` or its absence from the options UI. The plan does open PanelMaster's settings panel — `M4-15` moves the five Panels-page acts (Copy, Enabled, Unlock, Reset, Delete) into the `H.PageHeader` chrome band and drops the emptied General tab, and `M5-09` writes an `options-ui-§16` register row per remaining hand-written group — but neither adds a row for `level`.

Note for whoever does add it: after `M4-15` the Panels page's control layout changes, so build the row against the post-`M4-15` shape rather than today's. The Known-limitations entry and its deferral are untouched.

---
*Filed by work item `M2-23` of the **2026-09-07 review-and-standards-audit remediation** cycle — 207 triaged findings in 39 clusters across ten repositories, 106 work items in five milestones. The bundle lives in the `Ka0sAddonsCommonTasks` repo at `docs/2026-09-07-REVIEW_AND_STANDARDS_AUDIT_REMEDIATION/`: `01_CONSOLIDATED_FINDINGS.md` for the findings and clusters, `04_EXECUTION_PLAN.md` for the work items, `05_TRACEABILITY.md` for the finding-to-item map, `06_SMOKE_TESTS.md` for the six in-client sessions, `PROGRESS.md` for what has actually landed. `M2-23` gives every open issue in the eleven stores one of three dispositions — covered, unaffected, contradicted — and closes nothing.*

*State at the time of writing: **M1 complete** (38/38, LibKa0s v1.26.0 and v1.27.0 cut on the branch, the standard rolled to v2.39.0), **M2 in flight**, M3/M4/M5 not started, and no in-client smoke session performed.*


######## PanelMaster-42 — S.Installed() has no caller — dead export, or an unwired guard
Found by a dead-export sweep during the `O.RefreshPanel` adoption (`630d1ea`), alongside `P:RefreshPanels`, which was removed in `c596092`. This one was left in place because it is not the same kind of dead.

## What

`S.Installed()` — `modules/SunnArt.lua:246` — has **zero callers** anywhere in `core/`, `modules/`, `settings/`, `defaults/` or `locales/`.

```lua
function S.Installed()
  return #S.Themes() > 0
end
```

## Why it was not simply deleted

Three things make it heavier than an orphan:

1. **Its own comment claims a job nothing does.** It reads *"Used to keep the whole feature silent on a machine without it — no category, no rows, no settings copy about an addon the player does not have."* No code performs that gate through this function. The feature does stay silent, but by a different route: `modules/SunnArt.lua:466` calls `S.Themes()` directly and appends nothing when the list is empty. So the guard the comment describes is either redundant or was never wired.
2. **Six test assertions across four cases depend on it**, including one written specifically for it — *"SunnArt: Installed() agrees with the dropdown rather than with the globals"* (`tests/test_sunnart.lua:812`). Deleting the function means rewriting those as `#S.Themes() > 0`.
3. **It is documented as a deliberate design decision.** `docs/rendering.md:255` explains why it is defined as `#S.Themes() > 0` rather than as its own inspection of the Sunn globals: the earlier version returned true whenever any Sunn global existed, including for a SunnArt whose every theme named an uninstalled pack — so it could answer yes to a question the dropdown then answered no to. That reasoning is worth keeping whether or not the function is.

## The decision

Three ways to close this, and they are genuinely different:

- **Delete it.** Rewrite the six assertions as `#S.Themes() > 0`, and trim the last sentence of the `docs/rendering.md` paragraph (the folder-gate reasoning above it stays — it is about `S.Themes()` and is still live). Cheapest, and honest about what the code does.
- **Wire it.** If the comment describes a gate that *should* exist and does not, the fix is a caller, not a deletion. Worth checking whether the settings copy about Sunn is currently shown on a machine with no Sunn installed — if it is, this is a small bug rather than dead code.
- **Keep it as public surface.** If other addons are meant to be able to ask, say so in the comment and it stops looking accidental. Nothing currently documents it as public API and there is no `public-api` doc in this repo, so this is the weakest of the three.

## Not urgent

Zero runtime cost, zero user-visible effect, and the suite covers it either way. This is tidiness plus a comment that currently misdescribes the code.

## Where to look

- `modules/SunnArt.lua:238-248` — the function and its comment
- `modules/SunnArt.lua:466` — how the feature actually guards itself
- `tests/test_sunnart.lua:104, 115, 129, 687, 704, 812-821`
- `docs/rendering.md:248-257`

--- comment (tusharsaxena 2026-08-07):
### Triage decision

- **Decision:** triaged
- **Decided:** 2026-08-07
- **Approach:** **Delete it.** Remove `S.Installed()` (`modules/SunnArt.lua:238-248`); rewrite the six assertions across four cases in `tests/test_sunnart.lua` (`104`, `115`, `129`, `687`, `704`, `812-821`) as `#S.Themes() > 0`; trim **only** the last sentence of `docs/rendering.md:248-257` — the folder-gate reasoning above it is about `S.Themes()` and stays live. The code change is a separate session; triage wrote no code.

### Rationale

Chosen after the issue's own second branch — *"wire it"* — was **checked and ruled out** during
triage. The three things verified:

1. **Zero callers confirmed.** Across `core/`, `modules/`, `settings/`, `defaults/` and `locales/`
   the only other matches are `folderInstalled`, an unrelated local at `modules/SunnArt.lua:230`.
2. **The feature already guards itself by the other route**, exactly as the issue said:
   `modules/SunnArt.lua:466-468` builds `S.Rows(S.Themes())` and appends nothing when the list is
   empty, so a Sunn-less machine gets no category and no rows without `Installed()` being involved.
3. **The "settings copy about an addon the player does not have" does not exist.** The only Sunn
   reference under `settings/` is `settings/PanelEditor.lua:793`, a *Fit to artwork* tooltip that
   uses a three-section Sunn bar as a **pixel-size example** ("1536x256"). It is not conditional on
   Sunn being installed, and it is not something `Installed()` would gate.

So the guard the comment describes is **redundant, not missing** — there is no small bug hiding here,
which is what made deletion the honest close rather than a coin-flip against wiring it up.

Deleting is preferred over keeping-and-fixing-the-comment because the comment is the actual trap: it
claims a job nothing performs, and the next reader would re-run this exact investigation. The design
reasoning worth keeping — why the predicate was defined as *"does this yield anything to offer"*
rather than as its own inspection of the Sunn globals — is about `S.Themes()` and survives in
`docs/rendering.md` above the trimmed sentence.

*(Rationale inferred from the option chosen; the verification above was performed during triage.)*

--- comment (tusharsaxena 2026-09-07):
### 2026-09-07 remediation cycle — issue reconciliation (`M2-23`)

**Disposition: unaffected.**

Not covered, and again the near miss is the useful part. `C20` (*dead exports, dead arms and hand-copied helpers*, 7 findings across 5 repos) is exactly this class of problem, but its work item `M4-20` covers **AbsorbTracker, ConsumableMaster, KickCD and PrettyChat** — deleting `NS.PartitionUnitRows` and its only caller, KickCD's pre-`KCD-09` test branch and an unreachable `or _G.print` arm, a duplicated paragraph, and recording PrettyChat's three argued-in-place seams in `docs/module-map.md` rather than deleting them. PanelMaster is not in it; no pass filed a dead export here.

`M4-20`'s shape is the precedent to follow when this is decided: a seam that is deliberate gets **recorded**, not deleted, and a genuinely dead export goes with its caller in the same commit, with `docs/test-cases.md` and the README badge moved alongside. The comment on `S.Installed()` claiming a job nothing does is the part that has to be resolved either way.

---
*Filed by work item `M2-23` of the **2026-09-07 review-and-standards-audit remediation** cycle — 207 triaged findings in 39 clusters across ten repositories, 106 work items in five milestones. The bundle lives in the `Ka0sAddonsCommonTasks` repo at `docs/2026-09-07-REVIEW_AND_STANDARDS_AUDIT_REMEDIATION/`: `01_CONSOLIDATED_FINDINGS.md` for the findings and clusters, `04_EXECUTION_PLAN.md` for the work items, `05_TRACEABILITY.md` for the finding-to-item map, `06_SMOKE_TESTS.md` for the six in-client sessions, `PROGRESS.md` for what has actually landed. `M2-23` gives every open issue in the eleven stores one of three dispositions — covered, unaffected, contradicted — and closes nothing.*

*State at the time of writing: **M1 complete** (38/38, LibKa0s v1.26.0 and v1.27.0 cut on the branch, the standard rolled to v2.39.0), **M2 in flight**, M3/M4/M5 not started, and no in-client smoke session performed.*


######## PanelMaster-54 — Instance-addressed schema rows for per-panel fields (architecture-§5 option a)
Owner's option (a) for the `architecture-§5` register row in `docs/ARCHITECTURE.md` ▸ Documented deviations (the fields on a panel), recorded from audit finding PanelMaster-A-07 (audit PM-039). The row was re-decided as **keep** (option b) on 2026-09-24; this issue holds the adopt path so the decision can be revisited.

## Background

LibKa0s-Schema-1.0 has forwarded an instance id since Schema minor 2: `S.Set(path, value, instanceId)` hands it to `resolveRoot(parts, id)`. The host does not use it. `settings/Schema.lua`'s `resolveRoot` ignores the id (it always answers `NS.db.profile`), and the colon wrappers `NS.Schema:Set(path, value)` / `NS.Schema:Get(path)` do not forward one.

## Option (a): adopt instance addressing

1. **Resolver.** `resolveRoot(parts, id)` maps an instance id to its panel registry record (and keeps the profile root when no id is given).
2. **Rows.** Register instance-relative schema rows for every `C.PANEL_FIELD_TYPE` field (colors, border / bar / bar-border blocks, textures, size, `strata`, `level`, `scale`, `alpha`, mouseover, `enabled`, the `art*` fields, the anchor `point` / `relPoint` / `x` / `y`). `name` keeps routing to `R:Rename`.
3. **Writes.** `Registry:Set` routes through `NS.SchemaRuntime.Set(path, v, id)`, and the whole-record and bulk verbs (`R:Reset`, `R:CopyFrom`, `R:FitToArtwork`, `R:Recover`, `R:ResetPositions`, the unlock drag-stop through `:SetPosition`) become callers of the helper. The colon wrappers forward the id.
4. **Retire the row.** The `architecture-§5` row in Documented deviations retires in the same change.

This is a large change (the largest per-record migration in the collection) for fields the Registry already validates, logs and announces, which is why the row is kept for now.



######## PartyFrameEnhanced-12 — Attribute the 16.6 bytes per cast cycle the offline perf runner still measures
### Description
`tests/perf.lua`'s `castStartStop` scenario (five start/stop cycles per iteration) measures 16.6 bytes/iter after the 2026-09-15 perf pass. Every other hot path measures 0, and the mock's own recorders have been ruled out. The ceiling is 41 (measured + 24).

### Motivation
Noted in `docs/performance.md` and the ceiling comment in `tests/perf.lua`. Small, constant, and unexplained.

### Proposed behavior
Find the source; fix it if it is the addon's, or document it if it is the harness's.

### Acceptance criteria
The figure is attributed in `docs/performance.md`, and the ceiling is re-derived from the new measurement.


######## PartyFrameEnhanced-3 — Re-anchor the clickable target and pet frames during combat through a secure handler
### Description
When Blizzard's raid-style party frames or EllesmereUI re-sort mid-combat (someone joins or leaves), the secure target and pet frames cannot be moved from Lua. Today they fade out and re-anchor on `PLAYER_REGEN_ENABLED` (`modules/Anchor.lua`, spec §6.4).

### Motivation
Deferred from v0.1.0 (spec §10 item 3). A frame that vanishes for the rest of a pull is a user-visible gap.

### Proposed behavior
Wrap the frame system's member frames' `OnAttributeChanged` with `SecureHandlerWrapScript`, set up out of combat, so restricted code re-anchors (or re-points) the matching button in combat. Must be proven taint-free against EllesmereUI's SecureGroupHeader before shipping.

### Acceptance criteria
_TBD_ — at minimum: a mid-combat roster change leaves every target/pet frame beside the right member with no `ADDON_ACTION_BLOCKED`.


######## PrettyChat-1 — Update default format strings
Migrated from TODO.md backlog during the 2026-07-12 standards-audit remediation.

Review and refresh the per-string default format strings in `Defaults.lua` (labels + default templates) so they reflect current preferred styling across all categories (Loot, Currency, Money, Reputation, Experience, Honor, Tradeskill, Misc).

--- comment (tusharsaxena 2026-08-06):
### Context

The addon ships roughly 81 default chat format templates. Refreshing their wording and styling was raised as a pending item during the pending-audit sweep and deferred; it is tracked on GitHub as issue #1, which stays open.

### Evidence

Source: `GitHub issue #1`

Evidence hash: `25bd6725`

### Deferral rationale

Refreshing the ~81 default format templates is a taste call about wording and styling that needs a design pass on the actual strings, not a mechanical fix folded into a sweep. GitHub issue #1 stays open.

### Provenance

Migrated from `docs/pending/LEDGER.md` row `ISS-01` (evidence hash `25bd6725`), originally decided 2026-07-31.

--- comment (tusharsaxena 2026-09-07):
### 2026-09-07 remediation cycle — issue reconciliation (`M2-23`)

**Disposition: unaffected.**

Not scheduled — no finding asks for the default format strings to be refreshed. But `M2-01` **landed** (`5a7e63f`) and changes the rules this work has to play by, so read it before starting.

`M2-01` (cluster `C06`, `PRETTYCHAT-R-01`) moves `conversionSequence` into `modules/Override.lua` as `NS.ConversionSequence` and makes `Schema.Set` (`settings/Schema.lua:464`) refuse any write whose conversion sequence is not a **positional prefix of the shipped default's**. Previously `row.set` stored any string and the Preview could never see a surplus conversion, because `buildSampleArgs` synthesises its arguments from the format itself — the raise happened later, inside Blizzard's chat handler.

**Consequence for this issue:** a default's conversion sequence is now load-bearing. Changing the order or count of conversions in a default silently changes what every player's stored custom format validates against. Restyling (wording, colour escapes, spacing) is free; moving a `%s` is not. `tests/test_defaults.lua` asserts the prefix rule, so the suite will tell you.

---
*Filed by work item `M2-23` of the **2026-09-07 review-and-standards-audit remediation** cycle — 207 triaged findings in 39 clusters across ten repositories, 106 work items in five milestones. The bundle lives in the `Ka0sAddonsCommonTasks` repo at `docs/2026-09-07-REVIEW_AND_STANDARDS_AUDIT_REMEDIATION/`: `01_CONSOLIDATED_FINDINGS.md` for the findings and clusters, `04_EXECUTION_PLAN.md` for the work items, `05_TRACEABILITY.md` for the finding-to-item map, `06_SMOKE_TESTS.md` for the six in-client sessions, `PROGRESS.md` for what has actually landed. `M2-23` gives every open issue in the eleven stores one of three dispositions — covered, unaffected, contradicted — and closes nothing.*

*State at the time of writing: **M1 complete** (38/38, LibKa0s v1.26.0 and v1.27.0 cut on the branch, the standard rolled to v2.39.0), **M2 in flight**, M3/M4/M5 not started, and no in-client smoke session performed.*


######## PrettyChat-5 — Known limitation: Retail only, Classic untested
### Context

A Known Limitation recorded in `docs/ARCHITECTURE.md`: the addon targets Retail (`## Interface: 120007`); Classic and Classic Era are untested. Surfaced by the pending-audit sweep as a doc-level open item and deferred.

### Evidence

Source: `` `docs/ARCHITECTURE.md:79` ``

Evidence hash: `586d7473`

### Deferral rationale

Known Limitation (Retail only, Classic untested). Documentation of a real scope boundary, not debt. Kept visible rather than closed.

### Provenance

Migrated from `docs/pending/LEDGER.md` row `DOC-06` (evidence hash `586d7473`), originally decided 2026-07-31.

--- comment (tusharsaxena 2026-09-07):
### 2026-09-07 remediation cycle — issue reconciliation (`M2-23`)

**Disposition: unaffected.**

Untouched, and the cycle is Retail-only throughout — every finding, every measurement and all six in-client sessions assume a Retail (Live) client, and no item adds a Classic path or a Classic check anywhere in the collection.

The one adjacent piece of work: `M5-08` writes a non-English-client section into this repo's `docs/smoke-tests.md` and owns session 6, whose step 6.2 is *PrettyChat's whole function* — triggering one line from each override family on a deDE/frFR client. That is a **locale** axis, not a **flavour** axis; it says nothing about Classic. The limitation stands as filed.

---
*Filed by work item `M2-23` of the **2026-09-07 review-and-standards-audit remediation** cycle — 207 triaged findings in 39 clusters across ten repositories, 106 work items in five milestones. The bundle lives in the `Ka0sAddonsCommonTasks` repo at `docs/2026-09-07-REVIEW_AND_STANDARDS_AUDIT_REMEDIATION/`: `01_CONSOLIDATED_FINDINGS.md` for the findings and clusters, `04_EXECUTION_PLAN.md` for the work items, `05_TRACEABILITY.md` for the finding-to-item map, `06_SMOKE_TESTS.md` for the six in-client sessions, `PROGRESS.md` for what has actually landed. `M2-23` gives every open issue in the eleven stores one of three dispositions — covered, unaffected, contradicted — and closes nothing.*

*State at the time of writing: **M1 complete** (38/38, LibKa0s v1.26.0 and v1.27.0 cut on the branch, the standard rolled to v2.39.0), **M2 in flight**, M3/M4/M5 not started, and no in-client smoke session performed.*


######## WhatGroup-1 — Add role to the pop


--- comment (tusharsaxena 2026-08-06):
### Context

Open GitHub issue #1 requests that the joined-group popup show the role. The pending audit on 2026-07-31 deferred it: the request is a one-line spec covering real feature work that has not been scoped.

### Evidence

`GitHub issue #1`

Evidence hash: `b16fc5b1`

### Deferral rationale

"Add role to the pop" is a one-line spec for real feature work (capture the role, add a popup row, add a schema toggle); needs scoping before it can be built. Stays open on GitHub.

### Provenance

Migrated from `docs/pending/LEDGER.md` row `ISS-03` (evidence hash `b16fc5b1`), originally decided 2026-07-31.

--- comment (tusharsaxena 2026-09-07):
### 2026-09-07 remediation cycle — issue reconciliation (`M2-23`)

**Disposition: unaffected.**

The bundle is 207 triaged findings from the 2026-09-07 review and standards-audit passes: defects, standards deviations and record drift. It carries no feature work, and decision 5 of the cycle is that nothing ships (no addon version bump anywhere). Nothing in the plan advances this request or decides against it, so it stands exactly as filed.

No finding names role display. This repo's plan work is `M2-20`/`M2-21`/`M2-22`/`M2-25` (all landed), `M4-12`, `M4-13`, `M4-19`, `M4-24`, `M5-04`, `M5-08` and `M5-10`. `M2-22` (landed, `cc3f20e`) is the closest — it keys captures by `searchResultID` through the existing `GetApplicationInfo` bridge instead of binding the FIFO head to whatever application id arrives, so a notification now reliably names its own group. Role would come off that same `GetApplicationInfo` bridge, which is now trustworthy.

---
*Filed by work item `M2-23` of the **2026-09-07 review-and-standards-audit remediation** cycle — 207 triaged findings in 39 clusters across ten repositories, 106 work items in five milestones. The bundle lives in the `Ka0sAddonsCommonTasks` repo at `docs/2026-09-07-REVIEW_AND_STANDARDS_AUDIT_REMEDIATION/`: `01_CONSOLIDATED_FINDINGS.md` for the findings and clusters, `04_EXECUTION_PLAN.md` for the work items, `05_TRACEABILITY.md` for the finding-to-item map, `06_SMOKE_TESTS.md` for the six in-client sessions, `PROGRESS.md` for what has actually landed. `M2-23` gives every open issue in the eleven stores one of three dispositions — covered, unaffected, contradicted — and closes nothing.*

*State at the time of writing: **M1 complete** (38/38, LibKa0s v1.26.0 and v1.27.0 cut on the branch, the standard rolled to v2.39.0), **M2 in flight**, M3/M4/M5 not started, and no in-client smoke session performed.*


######## WowAddonStandards-6 — Complexity gate: lizard reads Lua's # length operator as a C preprocessor line and silently drops functions
The automated-tests complexity gate runs `lizard -l lua … -C 15`. Lizard's shared tokenizer treats `#` as the start of a C preprocessor directive and throws away the rest of the line. In Lua, `#` is the length operator. So when a keyword (`end`, `then`, `do`, `function`, `and`, `or`, …) or an unbalanced brace follows `#` on the same line, lizard never sees it, mis-nests the blocks, and drops whole functions from its report.

Dropped functions are not measured at all. The gate stays silent and the bundle records a clean "max CCN" that isn't true.

## Minimal repro (lizard 1.24.0)

```lua
-- hidden.lua
local function a(t)
  for _, x in ipairs(t) do t[#t + 1] = x end
  return t
end

local function b(x)
  if x then return 1 end
  return 2
end
```

`lizard -l lua hidden.lua` lists only `b@6-9`; function `a` is gone. Put the loop body on its own line and both `a@1-6` and `b@8-11` are listed.

## Impact seen in AuraMaster

- 111 lines in 33 files hid **67 functions**: lizard listed 845 against 912 once `#` was stripped.
- Three hidden functions were over the limit: `FC.Compile` at CCN **42**, `Database.PrepareProfile` at about **21**, and `Helpers.RenderContainerPage` at **20**.
- The committed automated-test bundle still recorded "max CCN 15, 0 warnings".
- The usual idiom `t[#t + 1] = v end` on one line is enough to trigger it, so every Ka0s addon is likely affected.

Fixed on the AuraMaster branch `fix/review-audit-2026-09-11` (commit ba7d18a):
- Every hazardous line was rewritten equivalently: the length hoisted into a local, one-liners expanded, `find(prefix, 1, true) == 1`, and `t[1]` instead of `#t > 0`.
- The three functions were split below 15.
- A regression guard was added.

## Proposal

1. **Document it** in the complexity-gate section (automated-tests / testing): a `#` followed by a keyword or an unbalanced brace on the same line hides code from lizard, and the rule is to keep what follows a length operator on its own line or in a local.
2. **Ship a guard in the kit** (LibKa0s `testkit/`) so every consumer gets it. AuraMaster's local version is `tests/test_lintconfig.lua`, case "lintconfig: no length operator shares its line with a keyword or brace lizard must see". It strips comments and string contents from each line of every tracked non-vendored `.lua` file, then flags a line where a keyword lizard counts, or an unbalanced `{`/`}`, follows the first `#`. A balanced `{ … }` is allowed. The scanner self-tests on known-positive and known-negative lines.
3. **Optionally add a parity check to the runner:** compare the number of functions lizard lists per file with a `#`-stripped copy, and fail on any mismatch. That catches this and any future tokenizer blind spot.
4. **Re-run the complexity gate across the collection.** Existing "max CCN" figures from before the fix may be understated.

Found during the AuraMaster remediation (T29), after the review in `docs/reviews/2026-09-11` noted that lizard skipped `PrepareProfile`.

