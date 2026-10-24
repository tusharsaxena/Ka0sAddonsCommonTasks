# 2026-10-25: Ka0s skins, leg 1 (LibKa0s skin engine + LootHistory prototype)

Every visual element of a Ka0s addon drawn from a per-addon **skin**: nine shipped Ka0s skins (Ka0s Default is
today's look) or EllesmereUI's look when it is installed with third-party skinning on. Leg 1 builds the engine in
LibKa0s and converts LootHistory, then stops for the owner's in-game smoke test. Leg 2 (a later bundle) rolls out to
the other 14 addons, moves PGFE onto the library provider and applies the HUD reset.

## Reading order

1. [`inputs/OWNER_SCOPE.md`](inputs/OWNER_SCOPE.md): the brief and the owner's rulings R1-R8.
2. [`03_SPEC.md`](03_SPEC.md): the end state (skin format, engine, Appearance tab, EllesmereUI provider, LootHistory).
3. Evidence: [`inputs/LIBKA0S_INTERNALS.md`](inputs/LIBKA0S_INTERNALS.md),
   [`inputs/LOOTHISTORY_SURFACES.md`](inputs/LOOTHISTORY_SURFACES.md),
   [`inputs/ACEGUI_AND_ENGINE_RESEARCH.md`](inputs/ACEGUI_AND_ENGINE_RESEARCH.md).
4. Mockups: [`plan-data/mockups/skins-mockup.html`](plan-data/mockups/skins-mockup.html) (standalone) and
   `plan-data/mockups/canvas/` (canvas sources; https://claude.ai/artifact/Dt32859dvnj1cCWoUkadzj).
5. [`04_EXECUTION_PLAN.md`](04_EXECUTION_PLAN.md), `items.tsv` / `plan-data/items.json`: milestones and items.
6. [`RESUME.md`](RESUME.md): pick the run up from any point. [`06_SMOKE_TESTS.md`](06_SMOKE_TESTS.md): the owner's checks.

## Versions

WowAddonStandards v2.88.0 → **v2.89.0**; LibKa0s v1.77.0 → **v1.78.0** (local tag until finalize). LootHistory: no
version bump.

## Branch

`feat/2026-10-25-skinning` in WowAddonStandards, LibKa0s, LootHistory and Ka0sAddonsCommonTasks.
