# Report: the owner's seventh smoke round

The branch is `feat/2026-11-04-smoke-round7` in 19 repos: the WowAddonStandards worktree, LibKa0s, the 16 addons and
this one. WhatGroup's branch carries no commit. Outfitter was not touched. Nothing is merged, no tag is pushed and no
version is bumped. The smoke list is `06_SMOKE_TESTS.md`, and nothing on it is marked passed.

## What shipped (34 R7 commits in 17 repos)

- **R7-STD, standard v2.100.0 (2 commits):** options-ui-§15 now says the Sim mode box is ticked while the sim window
  is shown or a sim runs. In skinning-§10, PGFE previews in test mode, which empties the no-preview list but keeps the
  clause. documentation-§1 item 5 says every README's Usage names `/<slash> skin`. The change also updates
  launcher-§2, ADDONS.md and adds anti-pattern #112. `check-standard.sh` passes.
- **R7-L1, LibKa0s (1 commit):** this commit changes only docs and tests. It adds contract wording to the Options and
  Launcher docs, a round 7 hosts-owe note in `releasing.md`, and window-host tests. Nothing under `LibKa0s/` or
  `tests/_kit/` changed, so R7-REL and R7-RV did not run. v1.85.0 stays at 550ef68.
- **R7-SIM, the 7 sim addons (9 commits):** in AT, BL, DR, DW, KC, LH and MM, `isSimMode` now returns "window shown or
  sim running". Unticking the box stops the sim and hides the window. The box and the launcher entry re-read on window
  show and hide.
- **R7-PG, PGFE (2 commits):** `/pgfe test` is a session-only test mode. It shows the panel alone and centred, with
  Apply and Clear disabled. It comes with a Test mode box, a launcher entry and `spec.preview { mode = "test" }`.
- **R7-RD, the READMEs (20 commits in 15 addons):** each README's Usage section now names `/<slash> skin` and what it
  does: hovering or selecting a skin previews it, Apply keeps it, and the eye switches the addon's preview mode. The
  addons are ST, AT, AM, BL, CM, DR, DW, KC, LH, MM, PM, PF, PG, PC and QC. Review follow-ups made extra commits in
  ST, DR, PF and QC. WhatGroup's Usage already said all of this, so it has no commit (`exceptions.tsv`).

## The lead's calls (00_PLAN.md)

1. PGFE gets `/pgfe test`, which goes through the write seam. Its skin picker previews in test mode. If PGF's dialog
   is open, the picker changes nothing.
2. The Sim mode box is ticked when the sim window is shown or a sim runs. Ticking it opens the window, and unticking it
   stops the sim and hides the window. LibKa0s code did not change, so there is no v1.86.0 and no re-vendor.
3. Every README names the skin verb, without a command table. The standard has gained that rule.
4. The standard moves to the next minor after master's v2.99.0, which is **v2.100.0** (2026-11-04).

## Totals (fresh at this gate, one repo at a time, through ka0s-bounded)

- **LibKa0s:** 4073 passed, 0 failed, 3 skipped. luacheck reports 0/0 in 298 files.
- **The 16 addons:** 22913 passed, 0 failed, 16 skipped. luacheck reports 0/0 in every repo. No Lua file is over 1500
  lines except PrettyChat's exempt generated `GlobalStrings/GlobalStrings.lua`. The per-repo counts are in
  checkpoints.tsv.
- **All 17 code repos:** 26986 passed, 0 failed.
- **Reviews:** 33 of the 34 R7 commits carry a `refs/notes/ka0s-review` note. The exception is bd55542, the reviewer's
  own R7-STD case fix.

## Open items

- **The standard's branch is in the worktree** `../.worktrees/WowAddonStandards-r7`, not in the main checkout. The
  Outfitter agent's branch `feat/2026-11-03-outfitter-roster` holds v2.99.1. Whichever of the two merges second must
  rebase its version stamps and CHANGELOG entry, either onto v2.100.0 or above v2.99.1. After the merge, run
  `git worktree remove` on the worktree.
- **Smoke:** the 11 PGFE checks and the 7 Sim mode blocks in `06_SMOKE_TESTS.md`. The client needs a full restart
  because PGFE has a new `eye.tga`.
- **Pushed:** the branch and `refs/notes/ka0s-review` in all 19 repos; none refused.
- **Your part:** smoke, then the go-ahead to merge. After the merge, delete this run's branches.
