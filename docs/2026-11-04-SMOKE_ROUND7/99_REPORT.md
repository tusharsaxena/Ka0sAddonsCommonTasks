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

## Addendum: R7-RD2, the Usage rewrite

The owner asked for it after the gate ("Do the usage section rewrite as well please, as a part of this run").
LibKa0sSkinTester (8516f52, 1b2fa87, aa07bff) and AuraMaster (4c5ad5a, f411e42) now have five-paragraph README Usage
sections, with the detail moved to their existing docs/settings-panel.md and docs/scope.md. The independent review
restored one dropped fact in each repo and corrected two claims that had been carried over from the old text. AuraMaster's
said a skin "never changes your colors or borders", but by default it sets font colors, shadows and border styles. The
Skin Tester's said Ignore fonts covers every string, but the per-skin face lines keep their fonts. Gates: Skin Tester 886
passed, AuraMaster 2355 passed, luacheck 0/0. Both are pushed. There is no in-game step.

## Addendum: R7-PG2, the test-mode panel looks like the docked panel

Owner: "This is PGFE test mode looks like in-game - not at all like the actual window" (inputs/images/71-74.png).

The cause: alone, the panel took its width from PGF's hidden dialog. That dialog is 300 wide by its template, and PGF
only widens it to 420 on the dungeon panel. As a result, the rows built for 420 overlapped, and the "(test mode)" title
ran over the arrow. The fix is in PremadeGroupsFilterExtension fe487b9 and e32885f (review). Alone, the panel now uses
the last docked width, then PGF's desired width, then 420. It also matches the dialog's scale, and drops back to scale 1
when docked. The title is the plain one, so the greyed Apply and Clear are what mark the mode. Gate: 544 passed, 0
failed; luacheck 0/0. The new smoke check is PG-12. The owner reported that the Sim mode checks pass (2026-11-04).

## Finish

On 2026-11-04 the owner reported "works as expected, smoke tests all pass" and asked for sync-docs, then the finalize.
Every check in 06_SMOKE_TESTS.md is marked as passed, and so is each addon's R7 rows (R7-SMOKE). R7-SD ran in all 18
repos and every gate was green. First, the standard was rebased onto master. The Outfitter merge had already brought in
v2.99.1, so v2.100.0 now sits above it and the v2.99.1 entry moved to CHANGELOG.md. Next, R7-FIN merged everything
--no-ff with each merge tree equal to its branch tree: WowAddonStandards e8b6e94, LibKa0s 06eae81, LibKa0sSkinTester
9e7da7b, AbsorbTracker b79b6ac, AuraMaster 6f21878, BankLedger bfc2aee, ConsumableMaster 2dbbbcd, DpsRace 2e27c30,
DropWatcher e0e3567, KickCD 4ca8ffa, LootHistory 0c05279, MultiMeters 2353197, PanelMaster 90e983f, PartyFrameEnhanced
9e6ea5c, PremadeGroupsFilterExtension 2147456, PrettyChat bec670f, QuickComms b5e9a8b. WhatGroup had no commits, so its
branch was simply deleted. GitHub answered 500 on five master pushes, and they went through on the retry. Master and
the notes are pushed. The branches are deleted locally and on origin, and the standards worktree is removed. No tag was
pushed, because LibKa0s is unchanged at v1.85.0. No addon version was bumped, and Outfitter was not touched. Two items
are left for later. LibKa0s's tests/test_launcher.lua is past its 1200-line trigger (1218). The library comments at
OptionsCompose.lua:457/975 and SIM_TIP still describe isSimMode as "whether the sim runs".
