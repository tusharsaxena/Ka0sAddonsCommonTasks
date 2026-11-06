# WoW Forever port, steps 1–4: smoke tests

The owner runs these in game. Claude records the results and never marks a check passed. Do this after CP-4,
with the run branch checked out in every `GIT/<Addon>` folder the game loads.

| ID | Client | Check | Result |
|---|---|---|---|
| SM-R1 | Retail | **Ka0s only:** disable every non-Ka0s addon, `/reload`. In each addon's settings, tick and untick a checkbox, then disable and re-enable a row that has one. No Lua error, and the check mark greys and ungreys. This proves that the Ka0s-shipped CheckBox v27 works without third-party masking. | pending |
| SM-R2 | Retail | With everything enabled again, in an addon with a colour control (AuraMaster, MultiMeters, PrettyChat): open the colour picker, change alpha, confirm, `/reload`. The alpha is not inverted and survives the reload. | pending |
| SM-R3 | Retail | Profiles: on two characters, check that each addon still shows the same active profile as before the run, and that no settings were reset. `/dump` the addon's `db:GetCurrentProfile()` where it has a diagnostics verb. | pending |
| SM-R4 | Retail | WhatGroup and PremadeGroupsFilterExtension load and work as before. The load-gating TOC lines do not hide them on Retail. | pending |
| SM-R5 | Retail | Spot-check two addons from each tier (AT, PM, AM, QC, BL, MM): open settings, use the main feature, `/reload`, no errors. | pending |
| SM-F1 | Forever | `/dump C_SpecializationInfo and C_SpecializationInfo.GetSpecialization and C_SpecializationInfo.GetSpecialization()`. Record the value. It fixes what LibKa0s Compat's spec readers answer on Forever (WFP-LK-05). | pending |
| SM-F2 | Forever | WhatGroup and PremadeGroupsFilterExtension are **not listed** in the Forever AddOns list. This needs a `_forever_` symlink to each to test. | pending |
