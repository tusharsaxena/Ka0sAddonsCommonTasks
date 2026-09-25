# Plan-review resolutions

Three independent critics reviewed the draft plan (ordering, owner scope, executability) and raised 24
issues. Every one is resolved in `plan-data/items.json` by `apply_amendments` (see `amendment_log` in that
file). This page records the decisions, because several of them change the plan's shape.

## Decisions that change the shape of the plan

1. **Minimap rename: no SavedVariables migration.** WS-06 renames the minimap row's schema/CLI path from
   `…minimap.hide` to `…minimap.shown`. The stored value stays LibDBIcon's `db.global.minimap.hide`, so an
   existing player's choice cannot be lost. The reconcile pass had added defensive "fold a stray `shown` key"
   migration steps to four addons only (PF-26, PC-27, and amendments to LH-13 and WG-11) and described them
   as an owner requirement. **The owner made no such ruling.** It came from an imprecise line in the planner's
   own prompt. Three of those four steps were also wrong under AceDB's copyDefaults (`hide == nil` is never
   true once `hide = false` is materialized). **Resolution:** PF-26 and PC-27 are dropped, the migration halves
   of LH-13 and WG-11 are not merged, and all eleven addons' rename items carry one identical test-first
   carry-over check instead: a legacy `hide = true` reads `shown = false`, the button stays hidden,
   `minimapPos` survives, and no `shown` key is ever stored. No schema-version bumps.
2. **Fixes owed before a re-vendor now land before it.** Several items said "lands BEFORE RV-x" but
   depended on RV-x. These items move into M2 ahead of their addon's re-vendor, depend on LK-33, and the RV
   item depends on them: AT-01, AM-01, AM-02, BL-01, BL-02, CM-01, KC-01, WG-01. Each must pass on both the
   v1.55.0 payload and the v1.56.0 dry run. The RV commit itself is still copy-only.
3. **Each re-vendor writes its bundle by hand.** The installed plugin is fetched from GitHub, so WA-01's
   amended `/wow-addon:revendor-libka0s` is not runnable until the owner merges wow-addon. Every RV item
   therefore writes `docs/revendor/2026-09-23-v1.56.0/` by hand, following the **local**
   `../wow-addon/commands/revendor-libka0s.md` at the WA-01 commit. Line 1 is exactly
   `Delta: LibKa0s v1.55.0 -> v1.56.0`, and the verify command checks it. RV depends on WA-01.
4. **`/wow-addon:revendor-standards` items are owner-gated (new milestone M4).** The plugin reads the
   standard from GitHub, so AT-26, AM-35, BL-25, CM-31, KC-27, LH-36, MM-32, PF-25, PM-16, PC-26 and WG-30 run
   only after the owner merges and pushes WowAddonStandards v2.65.0. Each carries the same gate check. The
   per-addon `<AB>-DOCS` items no longer wait on them: each gated item runs after its DOCS item and carries its
   own three-place ripple.
5. **v1.56.0 must carry LK-03.** LK-33 (the tag) now depends on LK-03, the AceDB fake fidelity change, which
   was outside the tag's dependency closure. WA-02 and WA-03 are plugin-only and are not ancestors of any RV.
   They are still in M1, and M2 starts only once M1 is complete.

## Corrections folded into item text (marked "PLAN-REVIEW CORRECTION")

- WA-01, WS-01, CM-28: every addon had a kit-only v1.54.2 re-vendor, so the frozen v1.55.0 bundles
  correctly read `v1.54.2 -> v1.55.0`. Bases are cross-checked with `git log -- libs/LibKa0s tests/_kit`.
- The span bundles in BL-23, CM-28, PC-25, WG-29, LH-34, PM-18, AM-02, MM-30, KC-24 and PF-24 are
  normalized to WS-01's exact line-1 grammar and depend on WA-01.
- LK-28: `disabledFor` draws the notice above rows rendered disabled rather than replacing them, and host
  tabs can take a schema group's place, so AM-17 adopts without behaviour change. AM-17 depends on LK-28.
- MM-14: the Schema instance shims are written with dot syntax (`S.FindRow`, not `S:FindRow`).
- MM-16: cites are corrected (CURRENT_DB_VERSION at :53; the minimap move is `migrations[14]`).
- MM-20: the peel target is named (`modules/Row_Cells.lua` plus a TOC entry), and the per-call `local live = {}`
  is removed.
- MultiMeters verify fields spell out the line-cap command instead of saying "line-cap awk".
- Explicit dependency edges were added where an item was only transitively ordered: LK-19→WS-07,
  MM-16→MM-12, BL-06/LH-17→LK-11, BL-11/MM-12/LH-12/WG-08→WS-03, BL-12/KC-17→WS-06, LH-26/PC-15→WS-05,
  WG-02→LK-03, AM-17→LK-28.

## Second pass

A consistency pass over the plan documents, with two owner decisions and two corrections applied to
`items.json` and every document that restated them:

- **Push policy (owner's instruction).** At the end of each milestone, every touched repository's
  `feat/2026-09-23-review-audit-remediation` is pushed to origin. Nothing is merged to `master`/`main`
  without the owner's go-ahead. The LibKa0s `v1.56.0` tag stays local and is pushed only when the owner
  approves the LibKa0s merge. An addon branch whose `CLAUDE.md` provenance line names v1.56.0 may be on
  origin before the tag is; that is acceptable, because the branch is unmerged and the tag is one push away.
- **Re-vendor greenness, all eleven addons.** Every `RV-<AB>` commit is copy-only (`libs/LibKa0s`,
  `tests/_kit`, the provenance line, `docs/revendor/2026-09-23-v1.56.0/`). It is green or lists its reds in
  its commit body. The M2 pre-fixes aim to make it green, the addon's M3 items clear any remaining red, and
  the addon is green again at the latest by `<AB>-DOCS`. The RV commit does not regenerate
  `docs/test-cases.md` or the badge; the addon's next item does, at the latest `<AB>-DOCS`.
- **MM-16 stops and asks.** If a path string is found persisted in SavedVariables, the implementer stops
  and raises it with the owner. This plan adds no migration for it.
- **WG-02 is not folded into RV-WG.** Any red at RV-WG is listed in that commit's body, and WG-02 clears
  it in M3.
- Smaller corrections: LK-19 depends on WS-07 as well as LK-02 (seven LK→WS edges), LH-36 and WG-30 name
  `master`, every M4 item including MM-32 carries the `gh api` gate, and the smoke checklist's MM.14 no
  longer names MM-DOCS, which has no smoke field.
