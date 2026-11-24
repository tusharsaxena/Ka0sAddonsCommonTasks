# Seeds and ForeverDB (2026-11-25)

The owner, 2026-11-25: "lets build LibKa0s #93 and #102 and #105 now. Especially #105 can be used to validate a
lot of assumptions - so it may warrant a way in which seed data works. You can also mark LibKa0s #44 as closed
now." Later the same day: "ive installed forever-db in my wow forever install folder" (ForeverDB, ForeverDB_Full and
ForeverDB_Locales 2026.11.24.46 under `G:\Games\Blizzard\World of Warcraft\_forever_\Interface\AddOns`).

LibKa0s#44 was closed at the start of the run (the Forever port is complete).

| Issue | What this run builds |
|---|---|
| LibKa0s#105 | `LibKa0s-ForeverDB-1.0`, a read-only runtime adapter over the ForeverDB data addon, plus a kit fake. Separately, ForeverDB becomes a **second evidence source** for Forever seed validation: it covers the server-side facts the client's DB2 lacks (NPCs, their positions, trainers, vendors, quest givers, objects). |
| LibKa0s#93 | LibKa0s's own `docs/validate-seeds.md` contract and `tools/seeds/` tool. They check that the Compat layer's and the kit's per-client assumptions (enum members, API names) hold on each client's interface data. |
| LibKa0s#102 | The adopters that were still missing: CombatTrail (DpsRace's seeds came with the merge), RangeMaster and LootHistory. Also the open follow-ups: QuickComms' per-client `CLASSES`, the two unpinned wago fetches, and the seed tests added to every adopter's CLAUDE.md gate. |

Read in order: `03_SPEC.md` (the decisions), `04_EXECUTION_PLAN.md` (items and milestones),
`plan-data/items.tsv` (the manifest), `RESUME.md` (how to pick up).
