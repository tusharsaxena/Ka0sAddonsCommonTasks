# Execution plan

Git is the only state: an item is done when a commit whose subject starts `<ID>: ` sits on `feat/2026-10-25-skinning`
in its repo, on top of that repo's default branch. Items run through `plan-data/tools/execute_milestone.js`
(implement test-first, an independent review that writes a `refs/notes/ka0s-review` note, one fix round). Items run
serially within a repo and in parallel across repos. Workflow agents commit locally and never push; the lead pushes at
checkpoints.

## M0 — Plan review (lead)

Before M1, an adversarial review of `03_SPEC.md` and `plan-data/items.json` against the evidence: missing ripples,
wrong file/line assumptions, cap and CCN traps, ordering. Accepted corrections are written into the item specs as
`PLAN-REVIEW RESOLUTION` paragraphs (they bind over the text above them) before any item runs.

## M1 — Upstream (15 items)

- **WowAddonStandards v2.89.0** (WS-00, WS-01, WS-90): the new `skinning` section, the library-stack and options-ui
  ripple, the anti-pattern with leg-2 commencement.
- **LibKa0s v1.78.0** (LK-00 … LK-10, LK-90): mockups under `docs/skins/`; kit revision 43 paint recorder; fonts and
  textures; the `LibKa0s-Skin-1.0` major with nine skins; Ka0s primitives; the EllesmereUI provider; owner-aware Core,
  Widgets, settings chrome, AceGUI rows (restore on release) and tool windows; `O.AppearanceTab`; release with the
  LOCAL annotated tag `v1.78.0`. Only LootHistory re-vendors in this run (lead's call, recorded in the CHANGELOG).

Checkpoint: every item reviewed; both repos' gates green on the run branch; push both run branches and notes, never the
tag. Append to `checkpoints.tsv`.

## M2 — LootHistory prototype (6 items)

LH-RV (re-vendor v1.78.0), LH-01 (owner seam, profile keys, Appearance tab, repaint plumbing), LH-02 (window chrome
and Export), LH-03 (History table), LH-04 (Insights, Timeline, Holdings), LH-05 (tool surfaces, the no-hard-coded-chrome
audit, docs and smoke rows). Ka0s Default keeps every golden unchanged.

Checkpoint: as M1 for LootHistory; push.

## M3 — Record and stop

CT-01: the execution record and the smoke file. **The run stops here** for the owner's in-game smoke test
(`06_SMOKE_TESTS.md`). Nothing merges and no tag is pushed.

## After the smoke test

Findings become an addendum (`plan-data/addendum-01.{json,tsv}`) of fix items on the same branches. Leg 2 (rollout to
the other 14 addons, PGFE onto the library provider, the HUD reset per R3) is a new bundle. **Merging and pushing the
`v1.78.0` tag happen only on the owner's explicit go-ahead**, via `/dev-copilot:finalize` in dependency order
(WowAddonStandards → LibKa0s → LootHistory → Ka0sAddonsCommonTasks), followed by deleting every branch, stash and
worktree this run created.
