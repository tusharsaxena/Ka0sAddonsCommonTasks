# Report: skin overrides and the first-run skin picker (LibKa0s#63, #64)

The execution record for `00_PLAN.md`. The plan is frozen and is not edited. Its addenda are
`SO06_KA0S_DEFAULT_MEDIA.md` and `PK02_PICKER_REWORK.md`, and `RESUME.md` records the pause for the
owner's PC restart on 2026-10-28. The run resumed on 2026-10-29 and finished everything short of the
merge.

Branch `feat/2026-10-28-skin-overrides-picker` in LibKa0s, LootHistory, LibKa0sSkinTester and this repo.

## Items

| Id | Repo | Commits | State |
|---|---|---|---|
| SO-01..03 | LibKa0s | 5 | Done |
| PK-01 | LibKa0s | 3 | Done |
| SO-06 (addendum) | LibKa0s | 1 (9bdb6df) | Done: Ka0s Default is Oxanium with a generated Ka0s Default bar |
| PK-02, PK-03 (addendum) | LibKa0s | 4 + 2 | Done: the reworked picker |
| SO-04 | LibKa0s | 1 (71f5df8) | Done after the owner approved the textures, with two swaps (Azeroth on Ka0s Parchment, WoW Forever on Ka0s Classic) |
| SO-05 | LibKa0s | 3 (d66fc1f, 3c9225f, 730c1d8) | Done. The local annotated tag `v1.79.0` is at 730c1d8 and is **not pushed** |
| LH-01 | LootHistory | 12 | Done |
| ST-01 | LibKa0sSkinTester | 12 | Done |
| LH-02 | LootHistory | 5487bf2 | Done: re-vendored from the tag with `git archive`, provenance line back to `v1.79.0 (MIT)`, prune kept 19 files, smoke SKIN-39 added, a doubled "Vendored icons" heading fixed |
| ST-02 | LibKa0sSkinTester | 6e2a0af | Done: the same; prune kept 6 files, smoke SHOW-14 added |
| ST-03 (owner's request after the plan) | LibKa0sSkinTester | 3afa3be | Done: the showroom's skinned scrollbar, shown only on overflow, with four headless cases and smoke SHOW-15 (SHOW-1 amended) |
| CT-01 | this repo | this bundle | Done |

GitHub: LibKa0s #63 and #64 are closed and labeled `state:done`, on the owner's word.

## Checkpoints

| # | What | Evidence | Pushed heads |
|---|---|---|---|
| 1 | Library items SO-01..03, PK-01 | Passed 2026-10-28 | LibKa0s 3914002 |
| 2 | Both consumers on the branch's library | Passed 2026-10-28 | LH 14c108f, ST 751b90a |
| 3 | SO-04, SO-05, LH-02, ST-02 (and ST-03) | Passed 2026-10-29. LibKa0s 3156 passed / 0 failed / 2 skipped; LootHistory 1830 / 0 / 1; LibKa0sSkinTester 538 / 0 / 1; `ka0s-bounded luacheck .` 0 warnings / 0 errors in all three; no file over 1500 lines | LibKa0s 730c1d8, LH 5487bf2, ST 3afa3be |
| 4 | Merge, push the tag, delete the branches | Done 2026-10-29 on the owner's go-ahead, after a doc sync (FIN-01: LibKa0s cc5fd6e, LootHistory 66d820a; the tester needed none). Gates re-run on every merge: 3156 / 1830 / 538 passed, 0 failed, lint 0/0. Tag `v1.79.0` pushed. Branches deleted locally and on origin | LibKa0s master 4e1ae41, LH b287253, ST 18280a6 |

## Smoke checks pending the owner

None of these is marked passed here.

- **LootHistory** (`docs/smoke-tests.md`): the skin checks listed under Pending sign-off for this run, now
  including SKIN-39 (every skin's bars wear its own texture).
- **LibKa0sSkinTester** (`docs/smoke-tests.md`): PANEL-3, PANEL-7..10, SHOW-1 (amended), SHOW-12..15,
  PICKER-1..16.

The new textures and Oxanium are new files, so the client needs a full restart before these checks,
not just `/reload`.

## Left for the owner

1. Run the smoke checks above.
2. Merge, tag push and branch deletion: done 2026-10-29 with `/dev-copilot:finalize` (checkpoint 4).
3. Not started: the backlog item LibKa0s#65 and the other addons' adoption of overrides and the
   picker. The collection-wide skinning adoption pass covers the adoption.
