# Report: the LibKa0s v1.89.0 then v1.90.0 re-vendor run (2026-11-06)

Owner's ask: re-vendor the newest LibKa0s into every Ka0s repo and adopt what it offers. The owner then
smoke-tested, and the feedback (`SF1_SMOKE_FEEDBACK.md`, `SF2_REMAINING_EDGES.md`) grew the run into a
LibKa0s release, v1.90.0. Owner smoke SM-01..SM-11 passed in game on 2026-11-06. The owner chose to
merge without a separate SM-12 check.

## What landed

| Milestone | What | Evidence |
|---|---|---|
| M1 | 16 addons re-vendored v1.85.0/v1.86.0/v1.88.0 -> v1.89.0; OutfitterReborn already current (`exceptions.tsv`) | `checkpoints.tsv` M1 |
| M2 | Widgets 23 adoptions: DpsRace submenu rows (V89A-DR), MultiMeters segment tick (V89A-MM), DropWatcher compact Filters cascade (V89A-DW) and History menu (V89A-DWH), Skin Tester cascade sample (V89A-ST) | M2 |
| M4 | LibKa0s v1.90.0: every Widgets edge one physical pixel (SF1-L1); `RegisterOwner` `keepScope`, honoured by `__copySkinTo` (SF1-L2); release (SF1-L3) | M4 |
| M5 | 17 addons re-vendored v1.90.0, plus ConsumableMaster's dark Ka0s Default button edge (SF1-CM), the Skin Tester's `keepScope` (SF1-ST) and DpsRace's column headers without rules (SF1-DR) | M5 |
| M6 | The menu divider, ReorderList row boxes and DragHandle strips one physical pixel (SF2-L1); v1.90.0 refreshed before its push (SF2-L2); 17 refreshes (`06_REFRESH_1.md` in each addon's v1.90.0 bundle) | M6 |
| FIN | Content-only sync-docs in 19 repos, `--no-ff` merges, master pushed in 19 repos, LibKa0s tag **v1.90.0** pushed (`1ba5fa2`), run branches deleted locally and on origin | FIN row |

## What caused the reported problems

None of them was introduced by this run. Each one was older and was exposed by the owner's testing:

- **ConsumableMaster's white edge.** `cm.buttonBorder` had a white Ka0s Default value. The white
  default dates from `ca02dfe` (2026-08-05) and moved onto the skin token in `3827acf` (2026-11-01).
  It showed on a second account's untouched profile.
- **The Skin Tester's stock AceGUI cells.** Apply to all copies a Scope over the tester's
  deviation. The copy dates from `9bc1826` (2026-10-28), and smoke round 4 flagged the risk.
- **Dropdown and search-box edges.** They were 1 UI unit wide, which renders as 1 or 2 px depending
  on where the box sits. This has been true since `8792331` (2026-10-22).
- **DpsRace's header rules.** These are host dividers, present since `39bb2b6` (2026-10-23) and
  skinned in `8f02cb4` (2026-10-29).

## Left open

- `WidgetsLineChart.lua` still draws its axis, grid, markers and crosshair at 1 UI unit (the SF2
  review's finding). The owner was told and did not ask for the fix.
- The dev-copilot `wow-revendor-libka0s` Step 0 roster regex no longer matches ADDONS.md's backticked
  paths. This run used a corrected pattern (`00_PLAN.md`). It is a plugin defect and is not fixed.
- LibKa0s file-size band items the release recorded as unruled: `Core.lua` 1080, `Widgets.lua` 1312,
  `tests/test_toast.lua` 1302, and the `SkinPaintExtras.lua` peel trigger.
- No addon version was bumped.
