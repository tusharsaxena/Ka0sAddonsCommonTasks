# WoW Forever port, step 5, wave 1: AbsorbTracker and the Skin Tester

The owner's instruction of 2026-11-07: record the classification (`00_CLASSIFICATION.md`) and port "SkinTester and
LibKa0sSkinTester". Those are two names for one addon, so Claude read it as **both group-2 addons**, AbsorbTracker
and LibKa0sSkinTester, which the classification's order puts first. The reading is recorded here so the owner can
correct it; dropping AbsorbTracker is one branch deletion.

## Branch

`feat/2026-11-07-forever-port-wave1` in AbsorbTracker, LibKa0sSkinTester, WowAddonStandards (the roster rows) and
Ka0sAddonsCommonTasks (this bundle). Git is the state: an item is done when a commit whose subject starts
`<ID>: ` exists in its repo.

## Baseline (2026-11-07, before any change)

| Repo | `lua tests/run.lua` retail | `KA0S_KIT_CLIENT=forever` | luacheck |
|---|---|---|---|
| AbsorbTracker | 1065 passed, 0 failed, 1 skipped | 1065 passed, 0 failed, 1 skipped | 0 / 0 |
| LibKa0sSkinTester | 897 passed, 0 failed, 1 skipped | 897 passed, 0 failed, 1 skipped | 0 / 0 |

Found on the way: both `docs/test-cases.md` inventories and README test badges are 3 cases stale (1062 and 894).
The kit's `test_client_globals.lua` suite arrived in the steps 1–4 re-vendor without a regenerated inventory. The
port regenerates them. Other addons probably carry the same drift. That is out of scope here and recorded in the
report.

## What a port changes (clients, toc-file-§3, documentation-§1, testing, clients-§4/§6)

Per addon, in one commit:

1. **TOC:** `## Interface: 120105, 16001`. No load-gating line.
2. **README:** the `[wow]` badge becomes `WoW-Midnight_12.1.5_and_Forever_1.60.1`; the opening sentence becomes
   "Supports Retail and WoW Forever."; the test badge matches the regenerated inventory.
3. **DEPENDENCIES.md:** the runtime row names both clients and the two-number line.
4. **docs/ARCHITECTURE.md:** the per-client feature table (clients-§4), here "all features serve both clients".
5. **CLAUDE.md and docs/testing.md:** the green gate runs both kit profiles.
6. **docs/smoke-tests.md:** a Clients note in *Before you start* (the existing checks are Retail's) and a new
   **FOREVER** theme with the checks to re-run on WoW Forever, the `_forever_` symlink among the setup.
7. **docs/test-cases.md** regenerated.

Turning on the second number also arms the kit's Forever missing-globals check (`test_client_globals.lua` reads a
16xxx number off the TOC). Both addons scanned clean against the forever set before the change.

## Items

See `plan-data/items.tsv`.

| ID | Repo | What |
|---|---|---|
| W1-AT-01 | AbsorbTracker | The port, items 1–7 above |
| W1-ST-01 | LibKa0sSkinTester | The port, items 1–7 above |
| W1-STD-01 | WowAddonStandards | Flip both roster rows to `Retail · Forever`. A roster data edit, as earlier roster rows were (`c21052b`, `35e093e`), so no standard version bump |
| W1-REC | Ka0sAddonsCommonTasks | This bundle and its smoke and report files |

## Gates and what is not done

- Before each commit, both kit profiles and luacheck are green, through the bounded runner.
- Smoke on both clients is the owner's (`02_WAVE1_SMOKE.md`). No check is marked passed by Claude.
- Feature branches are pushed at the end of the wave. No merge, no tag, no version bump without the owner's
  go-ahead. The CurseForge packaging alpha tag of AbsorbTracker is the owner's call.
