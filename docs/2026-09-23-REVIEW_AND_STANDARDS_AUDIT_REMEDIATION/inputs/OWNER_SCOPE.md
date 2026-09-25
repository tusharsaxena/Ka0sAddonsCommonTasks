# Owner scope and rulings — input to the plan

Recorded 2026-09-23, before collation. The plan must honour every line here.

## Scope

1. Every finding from `/wow-addon:review` and `/wow-addon:standards-audit` (2026-09-23 bundles) across
   LibKa0s and the eleven addons in `WowAddonStandards/standards/ADDONS.md` — **all severities**.
2. Upstream first: every LibKa0s (and WowAddonStandards / wow-addon, if needed) change lands and is
   tagged before any addon implementation item.
3. Re-vendor the **entire** LibKa0s payload (`libs/LibKa0s/` and `tests/_kit/`) from the new tag into
   all eleven addons.
4. Build the open enhancement issues filed 2026-09-23:

| Repo | # | Item |
|---|---|---|
| AuraMaster | 21 | Adopt LibKa0s-Schema-1.0 primitives, registry, bulk bracket, validation in settings/Schema.lua |
| AuraMaster | 16 | Peel Dispel Colors out of settings/GeneralSpells.lua (layout-§1 cap) |
| AuraMaster | 17 | Split user-category suites out of tests/test_database.lua |
| AuraMaster | 18 | Split user-category suites out of tests/test_filtercompiler.lua |
| AuraMaster | 19 | Split category-editing suites out of tests/test_pages_general.lua |
| ConsumableMaster | 39 | Adopt LibKa0s-Schema-1.0 for the settings write seam |
| KickCD | 22 | Adopt LibKa0s-Schema-1.0 for the settings schema runtime |
| MultiMeters | 52 | Adopt LibKa0s-Schema-1.0 path primitives, registry, bulk bracket |
| PanelMaster | 52 | Wrap module-scoped bus message constants in LibKa0s-Bus-1.0's Catalog |
| PartyFrameEnhanced | 14 | Adopt LibKa0s-Schema-1.0 once a library-less build can still write composed rows |
| PrettyChat | 18 | Move Schema.ResetRows onto the schema runtime's BulkRun and BulkAdd |
| WhatGroup | 22 | Adopt LibKa0s-Schema-1.0 |

   The seven closed `state:will-not-do` issues (AbsorbTracker #31, AuraMaster #20, BankLedger #20,
   PanelMaster #53, PrettyChat #16/#17, WhatGroup #21) stay declined — not built.

## Rulings

- **WhatGroup #22** — adopting the Schema seam breaks the degraded (library-less) `enable` and `test`
  verbs. **Accepted as a known gap.** Handle it smoothly: in the degraded build those verbs must raise
  **no Lua error** and instead print a chat message saying the verb is unavailable without LibKa0s.
- **PartyFrameEnhanced #14** — acknowledged; adopt once a library-less build can still write its
  composed rows (the library/stub work that makes that true belongs in the plan).
