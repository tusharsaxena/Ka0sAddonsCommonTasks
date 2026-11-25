# Execution plan

**Branch.** `feat/2026-11-25-item-search`, with the same name in LibKa0s, DropWatcher, LootHistory, BankLedger and this
repo.

**Manifest.** `plan-data/items.tsv`. An item is done when its repo's branch has a commit whose subject starts `<ID>: `.

## Where builders work

The pattern is the same as `docs/2026-11-25-SEEDS_AND_FOREVERDB`.

- **Builders never write the live repos**, because the game loads them. Each builder clones its repo to
  `~/ka0s-scratch/itemsearch/<Repo>` from the live `master` and branches there.
- **One repo, one agent at a time.** The Drop Watcher items run one after another in the same clone.
- **Siblings.** Clone WowAddonStandards and dev-copilot into the scratch folder too (read-only) wherever a tool resolves
  `../<Repo>`.
- **The ForeverDB helper** (dev-time) is `~/ka0s-scratch/itemsearch/dev-copilot/scripts/foreverdb.py`, or the
  installed plugin's copy, 2.12.0. Its cache is `~/.cache/ka0s-seeds/foreverdb/v2026.11.24.46/`.
- **Moving branches live.** After review, the lead runs
  `git -C <live> fetch ~/ka0s-scratch/itemsearch/<Repo> feat/2026-11-25-item-search:feat/2026-11-25-item-search`.
  This adds the branch without checking it out. The lead then pushes the feature branches.

## Milestones

| Milestone | Items | Checkpoint |
|---|---|---|
| M1 library and removals | IS-LK-01, then IS-LK-REL; IS-LH-01 and IS-BL-01 in parallel | the LibKa0s gate on both kit profiles; the LH and BL CLAUDE.md gates on both profiles |
| M2 Drop Watcher | IS-DW-02 can start at once; IS-DW-01 waits for IS-LK-REL; then IS-DW-03 → 04 → 05 → 06 → 07 in order | the Drop Watcher gate on both profiles, the seed tests and luacheck 0/0 |
| M3 review and record | IS-REV (independent review, then a fix pass); the lead brings the branches live, pushes them and runs IS-CT-REC | `plan-data/resume-state.sh` reports every item done; the gate table is in `EXECUTION_RECORD.md` |

Merging, pushing the v1.115.0 tag and closing DropWatcher#17 wait for the owner's go-ahead.
