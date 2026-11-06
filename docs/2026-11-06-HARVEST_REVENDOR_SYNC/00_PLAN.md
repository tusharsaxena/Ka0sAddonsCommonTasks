# 2026-11-06 — Harvest, re-vendor the standard, sync docs, finalize

**The owner's request (2026-11-06):** run `/dev-copilot:wow-harvest-standards` over all Ka0s addons
*including Outfitter Reborn*, which joins the Ka0s suite from today (recorded in WowAddonStandards and in
memory); then commit; then `/dev-copilot:wow-revendor-standards` into every Ka0s addon; then
`/dev-copilot:sync-docs` on every repo; then `/dev-copilot:finalize` on every repo.

**Branch:** `feat/2026-11-06-harvest-standards`, the same name in every repo it touches.

## Steps, in order

1. **Harvest** (WowAddonStandards). Read-only sweep of the seventeen rostered addons and LibKa0s, plus every
   repo's issue store; frozen bundle `WowAddonStandards/harvests/2026-11-06/` (01–06); interview the owner per
   proposal; apply the accepted ones with the full ripple; commit.
2. **Land the standard before the re-vendor.** `/dev-copilot:wow-revendor-standards` fetches the standard from
   GitHub `master`, so the harvest release is merged `--no-ff` and pushed first — the owner's finalize request
   for all repos covers this, done early because the re-vendor depends on it.
3. **Re-vendor the standard** into all seventeen addons: dry-run plans per repo, one owner approval for the
   whole multi-repo plan (the command's rule), then apply, gate (bounded tests + `ka0s-bounded luacheck .`)
   and commit per repo.
4. **Sync docs** on the seventeen addons and the four non-addon repos (WowAddonStandards, LibKa0s,
   dev-copilot, this workspace). Items the spec reserves for confirmation are collected per repo and put to
   the owner in one batch.
5. **Finalize** every repo in dependency order (WowAddonStandards, LibKa0s, dev-copilot, the addons, this
   workspace): merge `--no-ff`, push `master`, delete the feature branch. No tags, no version bumps.

The run's record is `99_REPORT.md` beside this file.
