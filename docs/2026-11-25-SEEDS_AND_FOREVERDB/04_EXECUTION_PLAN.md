# Execution plan

The branch is `feat/2026-11-25-seeds-foreverdb`, with the same name in every repo touched. `plan-data/items.tsv` is
the manifest. An item is done when a commit whose subject starts `<ID>: ` is on that branch in its repo.
SF-GATE-01 has one commit per repo.

## Where builders work

**Builders never write the live repos**: the owner plays from them, since the game loads `GIT/<Repo>` through
symlinks. Each builder works in a clone, then the lead brings the branches into the live repos.

- **Cloning.** Each builder clones its live repo to `~/ka0s-scratch/seeds/<Repo>`, branching from the live
  `master`:

  ```sh
  git clone -q /mnt/d/Profile/Users/Tushar/Documents/GIT/<Repo> ~/ka0s-scratch/seeds/<Repo>
  cd ~/ka0s-scratch/seeds/<Repo> && git checkout -b feat/2026-11-25-seeds-foreverdb
  ```

- **Sibling paths.** A repo whose tools or tests resolve siblings through `../` (for example
  `../WowAddonStandards`) finds them in `~/ka0s-scratch/seeds/` when they are cloned there. Otherwise a builder
  passes the live path explicitly, or sets `KA0S_GIT=/mnt/d/Profile/Users/Tushar/Documents/GIT` for
  `roster_clients.py`.
- **The ForeverDB helper.** Builders that need it use `~/ka0s-scratch/seeds/dev-copilot/scripts/foreverdb.py`
  from SF-DC-01's branch.
- **Moving branches live.** After review, the lead runs this for each repo:

  ```sh
  git -C <live> fetch ~/ka0s-scratch/seeds/<Repo> feat/2026-11-25-seeds-foreverdb:feat/2026-11-25-seeds-foreverdb
  ```

  That creates the branch ref without checking it out, so the owner's working tree and `master` are untouched.
  The lead then pushes the feature branches.

## Milestones

| Milestone | Items | Checkpoint |
|---|---|---|
| M1 upstream | SF-STD-01, SF-DC-01, SF-LK-01 → SF-LK-02 → SF-LK-REL | each repo's own gate green; LibKa0s on both kit profiles; dev-copilot `python3 -m pytest scripts` (or its documented gate) |
| M2 addons | SF-RM-01, SF-LH-01, SF-QC-01, SF-OR-01, SF-GATE-01 (start at once); SF-CT-01 and SF-SM-01 (after SF-DC-01) | each addon's CLAUDE.md gate, both kit profiles where the roster says `Retail · Forever`; each contract's `## Gate` |
| M3 review and record | an independent review of the large items, with a fix pass, then lead: branches live, feature branches pushed, issues filed, SF-CT-REC | `plan-data/resume-state.sh` reports every item DONE; the record lists the test totals and heads |

Merging, pushing tags and closing #93, #102 and #105 wait for the owner's go-ahead after smoke.
