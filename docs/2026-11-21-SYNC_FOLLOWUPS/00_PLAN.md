# Sync-docs follow-ups (2026-11-21)

## Why

The collection-wide sync-docs pass of 2026-11-21 (`SD-FIN-05` in 21 repos) left items it could not fix as a doc sync.
The owner said "fix all of these except the standards audit" and ruled:

- **Land the other session's per-client quirks work.** `feat/2026-11-10-per-client-quirks` in WowAddonStandards
  (the `forever-quirks` catalog) and in dev-copilot (one quirks file per client) are merged, renumbered onto
  today's `master`.
- **Release and push.** When everything is green, merge, push `master` and push the new tags. No addon version bumps.

## Scope

| Item | Where |
|---|---|
| Roster note: CombatTrail and SkillMaster default to `master` | WowAddonStandards `standards/ADDONS.md` |
| The `forever-quirks` catalog lands, standard **v2.117.0** | WowAddonStandards |
| Per-client quirks files land, `roster_clients.py` finds the roster from the repo it runs in, **dev-copilot 2.11.0** | dev-copilot |
| Callout, OptionsCompose and SkinPaintControls peeled on their recorded seams; the kit README counts; CONSUMERS.md regenerated; **LibKa0s v1.109.0** | LibKa0s |
| Re-vendor v1.109.0 and v2.117.0 into all 19 addons (a Forever addon gains `docs/forever-quirks.md`) | 19 addons |
| Loot History `modules/Browser.lua` peeled on its recorded seam | LootHistory |
| Skin Tester's `skinRepaint` ceiling bisected and re-pinned | LibKa0sSkinTester |
| Dead exports removed (test seams and contract stubs kept) | MultiMeters, KickCD, CombatTrail, DropWatcher, RangeMaster, SkillMaster |

The standards audit is out of scope (the owner runs it later).

## Milestones

- **M1, upstreams:** the standard, dev-copilot and LibKa0s, each reviewed independently. Local tags.
- **M2, the addons:** the re-vendors, then the addon-specific items, each reviewed.
- **M3:** CP-1 (every repo green on each client it ships), then finalize: merge `--no-ff` in dependency order
  (standard, dev-copilot, LibKa0s, addons, this repo), push `master` and the tags, delete the branches (and the
  landed per-client-quirks branches and their worktrees).

Branch `feat/2026-11-21-sync-followups` in every repo touched. State is git only: `plan-data/resume-state.sh`,
`items.tsv`, `exceptions.tsv`, `checkpoints.tsv`. To resume, run `resume-state.sh` and continue from the first
TODO row in milestone order.
