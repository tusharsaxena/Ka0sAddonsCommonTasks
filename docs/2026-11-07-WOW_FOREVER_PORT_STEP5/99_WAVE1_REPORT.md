# Wave 1 execution record (2026-11-07)

Every wave-1 item has its commit on `feat/2026-11-07-forever-port-wave1`. Nothing is merged, tagged or version-bumped.

| Item | Repo | Commit | Gate |
|---|---|---|---|
| W1-AT-01 | AbsorbTracker | `b70c476` | 1065 passed / 0 failed under `retail` and `forever`; luacheck 0/0 |
| W1-ST-01 | LibKa0sSkinTester | `eb3ac62` | 897 passed / 0 failed under `retail` and `forever`; luacheck 0/0 |
| W1-STD-01 | WowAddonStandards | `a552390` | `roster_clients.py` reads both rows as `retail+forever` |
| W1-REC | Ka0sAddonsCommonTasks | the bundle commit | — |

With the TOC change, both addons' kit suite `test_client_globals.lua` now checks the Forever API set as well, and passes.

## Found on the way

- **Stale test inventories.** Both addons' `docs/test-cases.md` and README test badges were 3 cases behind. The kit's
  `test_client_globals.lua` arrived in the steps 1–4 re-vendor without a regenerated inventory. Fixed here for these two.
  The same drift is likely in every addon that took that re-vendor. Check with
  `diff <(lua tests/run.lua --list) docs/test-cases.md` in each, and fix in the next sweep.
- **`scripts/check-standard.sh` fails on WowAddonStandards `master`**, before this wave's edit:
  `libka0s-counts` finds "seventy-one files" in `library-stack.md`, `STANDARDS.md` and `EXECUTIVE_SUMMARY.md`, against
  72 in LibKa0s v1.93.0 (the `OptionsHeader` peel, WFP-LK-08, added a file). It needs a standard patch release. Left for
  the owner's call.
- **The runner and the profiles.** `tests/_kit/run-automated-tests.sh` runs one profile per call. It inherits
  `KA0S_KIT_CLIENT`, so a Forever run is `KA0S_KIT_CLIENT=forever tests/_kit/run-automated-tests.sh --suite tests`, and
  both addons' `docs/testing.md` now say so.

## Owed

- Owner smoke: `02_WAVE1_SMOKE.md`.
- The owner's go-ahead to merge the four branches (`/dev-copilot:finalize`).
- The CurseForge packaging test, one alpha tag of AbsorbTracker, which waits for the owner. The Skin Tester is never
  published.
