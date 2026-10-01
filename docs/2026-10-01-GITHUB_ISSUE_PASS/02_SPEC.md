# Spec

This page holds the cross-cutting design: what each upstream release carries, the order things land in,
and the conventions every item follows. Per-issue evidence and the detailed design for each item are in
`02a_ISSUE_DESIGNS.md`. Where the two differ, this page wins.

## S1. LibKa0s v1.66.0 (M1)

One release. Every item is its own commit (`GI-LK-NN: ...`) on `feat/2026-10-01-github-issue-pass`, with a
failing test first. The touched files' LibStub minors are bumped once per release, not once per commit.

| Item | Surface | Change | Minor |
|---|---|---|---|
| GI-LK-01 | tests | `test_options.lua` render/refresh block → `test_options_render.lua` | — |
| GI-LK-02 | tests | `test_schema.lua` write stage onward → `test_schema_write.lua`, shared fixtures helper | — |
| GI-LK-03 | Slash | Optional key→string resolver as third argument to `ParseValue`/`FormatValue`, threaded through the file-level parsers. `lib:New` passes `Sl:Text`. A host `d.parse` also receives it | Slash 18→19 |
| GI-LK-04 | Widgets | `ReorderList` → `WidgetsReorder.lua`, `lib.__reorderMinor` / `__reorderShellMinor` pairing, `LibKa0s.xml` row, `tests/majors.lua` row | Widgets shell + Reorder 1 |
| GI-LK-05 | OptionsWidgets | `O.RenderGrid(ctx, items, parent, opts)`: `parent or O.EnsureScroll(ctx)`, `opts.gap` (default `L.ROW_VSPACER`, `false`/`0` = none), the wide branch releases a failed item with no gap. DoLayout is **not** automatic; the docstring and README say so | Widgets 33→34 |
| GI-LK-06 | OptionsTabs | `opts.untabbedSkipRender`, `opts.disabledReplaces` (+ `disabledNoticeFont`), `opts.rerender(ctx)`. All off by default | Tabs 7→8 |
| GI-LK-07 | Perf | Command surface (`P.Usage`, `SUBS`, `P.StatusLines`, `P.OnCommand`) → `PerfCommands.lua` via `lib.__installCommands(P, ctx)`, a stub when absent; `resolveHooks(d)` hoisted to file level | Perf 13→14, Commands 1 |
| GI-LK-08 | Perf | `P.BuildRecord` emits every parent a recorded child names, with zero counts if it was never noted | (Perf 14) |
| GI-LK-09 | Perf | Optional per-bucket `budget = { msPerSec, maxMs }`: validated, copied into the record, reported by `addBudgetLines`, with a one-line finish-ack summary. No gating | (Perf 14) |
| GI-LK-10 | testkit | Kit 35: `testkit/lizard_sighted.lua` (sanitize, countFunctions, shadow/parity CLI, `function a:b(` → `function a.b(self,` in the shadow), the runner's complexity block measures the shadow and fails the suite on any parity mismatch (`blindFiles` in the manifest), `testkit/test_lizard_sighted.lua` gate, `mock_base.lua` GetHeight comment rewritten (net zero lines), `docs/api/testkit/version-35-docs.md` | Kit 34→35 |
| GI-LK-11 | several | Bring the sighted-revealed functions below CCN 15: `lib:New` in Perf, DebugLog and Slash, `P.Context`, `Kit.assertSurfaceParity`, `renderInventory`, the `test_eol` anonymous case | — |
| GI-LK-12 | release | `CHANGELOG.md` v1.66.0, version stamps per `docs/releasing.md`, the release automated-test run (all four suites pass, sighted), regenerated manifests and docs, **local** tag `v1.66.0` | — |

The payload goes from 28 to 30 files (`PerfCommands.lua`, `WidgetsReorder.lua`). The standard's file counts
(library-stack-§7, EXECUTIVE_SUMMARY, NEW_ADDON_CONTEXT `LIB_FILES`) are recounted in GI-STD-01.

## S2. Standard v2.74.0 (GI-STD-01)

- automated-tests-§3 gains a MUST: **the complexity gate is sighted**. The suite measures the kit's
  sanitized shadow, and a function-count parity mismatch means complexity did not pass. That blocks the release
  gate the way a skip does, and never blocks a commit.
- Document lizard 1.24.0's Lua blind spots: `#` read as a preprocessor line, and the Ruby-like reader's
  bare `it` / `class` / `module` / `begin` / `unless`. Add an anti-pattern entry.
- Ripple: STANDARDS.md blurb, changelog, the context pack, AUDIT.md (check: kit ≥ 35), and every page that
  quotes the raw `lizard -l lua -x ...` command points to `bash tests/_kit/run-automated-tests.sh --suite
  complexity` instead. Payload count 28 → 30.

## S3. wow-addon (GI-PLUG-01)

`agents/review.md` and any command that quotes raw lizard switch to the runner's complexity suite.
bump-version's release gate already reads `suites.complexity.status`; it also prints `blindFiles`. If a
file needs no change, record an exception with proof.

## S4. Addon wave (M2)

Each addon first takes **GI-<XX>-RV**:

1. `/wow-addon:revendor-libka0s` mechanics: copy `libs/LibKa0s/` and `tests/_kit/` whole from tag v1.66.0,
   roll the `CLAUDE.md` provenance line, add the frozen `docs/revendor/` bundle. Adoption candidates the
   skill surfaces are **not** interviewed this cycle. Note them in the bundle; GI-LK-13 picks them up.
2. Wire `{name='test_lizard_sighted', dir='tests/_kit/'}` in `tests/run.lua`.
3. Update any `CLAUDE.md` green-gate line that quotes raw lizard.
4. Run the sighted complexity suite and record the figure in the commit body.

Then the addon's own items run in the order `items.tsv` gives (dependencies are serial within a repo). The
sighted CCN refactors (GI-BL-02, GI-CM-02, GI-KC-12, GI-LH-02, GI-MM-02) take characterization tests first and
list each function's before/after CCN in the commit body. If the re-vendored kit reveals a function the
validation pass did not list, it goes into that repo's CCN item. In PanelMaster, PartyFrameEnhanced,
PrettyChat, WhatGroup, AbsorbTracker and AuraMaster, which validation found clean, it goes into the RV commit.

### KickCD order (12 items, one file family)

Pure-move peels first, each with identical suite totals: IconGrid (closest to the cap) → IconGrid_Render's
ticker → wow_mock → Castbar_Frame → Database_Migrations → Spells_Header → three test splits. Then #9 (ticker
owns time, in the new `IconGrid_Ticker.lua`; swipe re-armed **only** on state work), then #10 (RenderGrid
with `{gap=false}`; `reorder:AddRow` on the wrapper group after RenderGrid returns; the wrapper's height
asserted equal to `ROW_HEIGHT`), then the CCN refactor (Cooldowns 46, IconGrid 29, test_perfsetup
anonymous 19).

### PartyFrameEnhanced#3 safety rules

`modules/SecureFollow.lua`: one `SecureHandlerBaseTemplate` header, created out of combat. Frame refs and
attributes are synced out of combat only. Wraps are installed lazily for re-sorting providers only, and the
existing fade stays as the fallback. Every restricted snippet is a string constant that the tests load and
execute against the mock's restricted environment. Stand-down unwraps when ours is the outermost wrap;
otherwise the wrap stays gated on `<f>-live`, recorded as a Documented-deviations row. The issue
stays open until COMBAT-6/9/10 in `04_SMOKE_TESTS.md` pass.

## S5. M3

- **GI-LK-13** runs after M2, so the census measures v1.66.0 as adopted. It produces
  `docs/api/CONSUMERS.md` (per export, per host: call / duplicate / stub with file:line), rewrites
  `docs/adoption-prompt.md`'s "Thinly-consumed surfaces", adds a "no consumer as of v1.66.0, kept because
  ..." line per zero-consumer export, and files one issue per host duplicate found (throttled,
  `state:triaged`, `severity:low`). Nothing is deleted.
- **GI-FIN-01**: `99_REPORT.md`, a comment on every actioned issue naming its commit(s), and branches plus
  `refs/notes/ka0s-review` pushed.

## S6. Conventions

- Commit subject `GI-<..>: <what>`; a review fix is `GI-<..>R: <what>`. End with the session trailers.
- Independent review per item (or per small group of items in the same repo). It writes a
  `refs/notes/ka0s-review` note on the item's last commit starting `OK <ID>`, or lists defects that the
  implementer fixes as `<ID>R:` commits (at most two rounds, then stop and report).
- A red gate that cannot be made green, a merge conflict, or a decision only the owner can make stops that
  repo and is reported. Other repos continue.
