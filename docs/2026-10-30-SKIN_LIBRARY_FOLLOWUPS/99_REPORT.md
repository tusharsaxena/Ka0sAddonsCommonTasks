# Report: the skin library follow-ups (LibKa0s v1.81.0)

This is the execution record. The plan (`00_PLAN.md`) and `DECISIONS.md` stay as written; everything decided after
them is recorded here.

## Where it stands (2026-10-30, end of M3)

- Every item in M0, M1 and M2 has landed. `resume-state.sh` shows each item as a commit or as an `exceptions.tsv` row
  with a proof command.
- Every run branch is pushed with its `refs/notes/ka0s-review` note: LibKa0s, WowAddonStandards, LibKa0sSkinTester,
  the 15 addons and this repo. **Nothing is merged.** The LibKa0s tag `v1.81.0` is **local only** (aefeba9).
- The run is stopped for the owner's in-game smoke test (`06_SMOKE_TESTS.md`) and their go-ahead (M4).

## What shipped, per ruling

| Ruling | Delivered by | What the player sees |
|---|---|---|
| R-1 Ignore fonts covers the HUD | LK-01, every addon's XX-01 | With Ignore fonts ticked, the HUD text uses each element's own font setting |
| R-2 No stock look under Ka0s Default | LK-02, D-04..D-06, PG-01, QC-01, DR-RV/01 | Ka0s Default is Ka0s everywhere; WoW Default is the stock look |
| R-3 Close-button tint | LK-03 | Close art gets its own color back on unpaint |
| R-4 A HUD face per skin | LK-04 (D-11) | Each skin draws its own HUD face |
| R-5 Custom widgets skinned and scoped | LK-05, LK-06a..d | Every library widget is skinned. Settings-page widgets obey Ignore settings panel; windows always follow the skin |
| R-6 ResetToSkin sentinel | LK-07 | An absent companion becomes `true`, not the sentinel. Opt-in for picker keys (see below) |
| R-7 DragHandle tooltip colors | LK-08, LK-06d | Tooltips use the skin's `gtip.*` colors |
| R-8 Item-quality colors | LK-09 | `q.*` are the client's colors exactly |
| R-9 Public DrawsKey | LK-10 | `Skin:DrawsKey(owner)`; `__DrawsKey` is an alias for one release |
| R-10 "Skin" tab | WS-01 | The standard names the tab Skin |
| R-11 Picker title | LK-11 | "Choose a skin", with the addon's full name above the dropdown |
| Owner's Lua error | MM-H1, LK-A1 | The MultiMeters title gets a font first, and the library never sends SetFont a size of 0 or below |

## Milestones

| Milestone | Evidence |
|---|---|
| M0 | 19 inventory reports in `inputs/inventory/`; `DECISIONS.md` D-01..D-20 |
| M1 | LibKa0s v1.81.0: 3297 passed, 0 failed, 2 skipped; luacheck 0/0 in 237 files; release run `docs/automated-tests/20261030-055012/` green (lint, tests, complexity max CCN 15). The standard is v2.92.0 and `check-standard.sh` is green. Skin Tester: 571/0/1, luacheck 0/0. Independent reviews and fixes are in place (`checkpoints.tsv`) |
| M2 | 15 addons re-vendored. Every vendored copy diffs clean against `git archive v1.81.0` (icon prune aside). The gates were re-run by the lead after the reviews (table below). Every addon has a review note |
| M3 | This report and `06_SMOKE_TESTS.md` |

### M2 gates (re-run by the lead after the fix rounds)

| Addon | Tests (passed/failed/skipped) | luacheck | Head |
|---|---|---|---|
| AbsorbTracker | 954/0/1 | 0/0, 77 files | 2c83cba |
| AuraMaster | 2216/0/1 | 0/0, 188 | b734425 |
| BankLedger | 1510/0/1 | 0/0, 111 | ec45a07 |
| ConsumableMaster | 1293/0/1 | 0/0, 138 | c0c8c9e |
| DpsRace | 1146/0/1 | 0/0, 148 | fc245db |
| DropWatcher | 1792/0/1 | 0/0, 202 | baf004f |
| KickCD | 1557/0/1 | 0/0, 153 | 4e46415 |
| LootHistory | 1834/0/1 | 0/0, 151 | e397d91 |
| MultiMeters | 2418/0/1 | 0/0, 171 | 78e13cf |
| PanelMaster | 1140/0/1 | 0/0, 80 | 5c963ac |
| PartyFrameEnhanced | 538/0/1 | 0/0, 87 | 3c1c8a7 |
| PremadeGroupsFilterExtension | 429/0/1 | 0/0, 64 | 17a6b05 |
| PrettyChat | 631/0/1 | 0/0, 62 | 5a359d7 |
| QuickComms | 1260/0/1 | 0/0, 143 | 20ab5a7 |
| WhatGroup | 1025/0/1 | 0/0, 69 | 5fb0b23 |

No authored file is over 1500 lines. PrettyChat's `GlobalStrings/GlobalStrings.lua` is generated data that the run
did not touch, and it was over the cap before the run.

## Exceptions (no commit, with proof)

LK-06 was split into LK-06a..d. PC-01, PM-01 and WG-01 had no workaround to delete: PrettyChat, PanelMaster and
WhatGroup have no HUD and no stock-look, scope, ResetToSkin, DrawsKey or tint code. The lead re-ran each proof
command in `exceptions.tsv` and got the expected output.

## Lead decisions taken during the run (after DECISIONS.md)

- **D-21: LootHistory's AH price table under Ignore settings panel.** The table draws Ka0s Default's token values
  (gold, white and the green/yellow/red status colors) in the template face, so the status colors keep their
  meaning on a stock page. PANEL-24 checks this. The alternative is the template's own white and gold, which drops
  the status colors. The owner judges this in game.
- **D-22: D-19's "a schema step that already shipped" means a step in a release tag.** MultiMeters' v20 step is on
  origin/master but in no tag (1.2.0-release ends at migrations[15]), so MM-01 dropped its companion seeding. The
  step names its companions, and Skin minor 8 sets them, so no profile's result changes.
- **D-23: ConsumableMaster keeps one stock-color line.** `KCM.SkinPanelText` keeps its plain `SetTextColor` for
  state colors the templates do not carry (disabled gray, "Macro not created yet", gold on a white template). This
  departs from the v1.81.0 "What a consumer owes" LK-05 point on purpose. A later sweep must not delete it. The cost
  is a template-color flash of about one frame on those rows after a skin switch. SKIN-7 counts that as a pass.
- **The picker-key half of D-19 is opt-in.** A picker key's absent companion is fixed only when the caller names
  the companions or passes `{ companions = true }`. The library cannot tell an absent pick from a plain setting
  (M1 review nit). Every addon was told this, and those that seed companions in a shipped step kept the guard.
- **The drawer arrow under Ka0s Default** is gold-tinted (`icon.arrow`) where it used to be the client's yellow art.
  No ruling covers it, so FU-12 asks the owner to judge it.

## Things the run noticed

- The M1 review caught that LK-A1 had not been done before the release. It was fixed and the tag was cut after the
  fix, so no re-cut was needed.
- The first release run failed complexity: `ReorderList` reached CCN 17 and `TestStrip` CCN 16. The functions were
  split before the tag. The failed bundle is kept as the record.
- Two M2 implementers shared a scratch folder for the tag extraction. Every addon's vendored copy was re-diffed
  against the tag afterwards and all 15 are clean.

## Proposed follow-ups (not filed)

- **LibKa0s: a recorded state color under Ignore settings panel.** For example `S.Text(fs, role, { panel = true,
  stockRole = ... })`, so ConsumableMaster can drop its last plain `SetTextColor` (D-23) and lose the flash.
- **Remove the `__DrawsKey` alias** in the release after next.

## M4 (on the owner's go-ahead)

1. Finalize in dependency order: WowAddonStandards, then LibKa0s (push tag `v1.81.0`), then LibKa0sSkinTester, then
   the 15 addons, then this repo. Merge each with `--no-ff`, push it with its notes, and delete its branch locally
   and on origin. No version bumps.
2. Clean up any stashes and worktrees this run created (none exist at the end of M3).
