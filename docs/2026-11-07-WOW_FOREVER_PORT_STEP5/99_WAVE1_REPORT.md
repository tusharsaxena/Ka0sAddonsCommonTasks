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

## Finish (2026-11-08)

On the owner's go-ahead ("Go ahead"), `/dev-copilot:finalize` merged `feat/2026-11-07-forever-port-wave1` with
`--no-ff` into `master` in five repos, pushed each, and deleted the branch locally and on origin. LibKa0s's tag
**`v1.94.0`** is pushed. Every merge result was gated before its push: LibKa0s 4270 / 0 failed under both kit
profiles, AbsorbTracker 1065 / 0, the Skin Tester 899 / 0, luacheck 0/0 in each, vendor drift empty, and
`check-standard.sh` all passed (standard v2.104.0). All wave-1 smoke has passed, including the follow-ups in
`W1_DEFAULT_SKIN_AND_FOREVER_NAMES.md` and `W1_FOREVER_NAME_PROBE.md`.

| Repo | Pushed `master` |
|---|---|
| LibKa0s | `40e0010` |
| WowAddonStandards | `3e72e46` |
| AbsorbTracker | `5533711` |
| LibKa0sSkinTester | `ef53889` |
| Ka0sAddonsCommonTasks | this record's merge |

Not done here: no addon version bump and no release. The CurseForge packaging test (one AbsorbTracker alpha tag)
still waits for the owner. Next: group 3 (PanelMaster, PrettyChat, PartyFrameEnhanced).
