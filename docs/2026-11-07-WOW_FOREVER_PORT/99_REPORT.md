# WoW Forever port, steps 1–4: execution record

Finished on 2026-11-07. Every item in `plan-data/items.tsv` landed. `WFP-LK-06` was first deferred and then built in M5. Git holds the per-item record (`WFP-<ID>: ` subjects), `checkpoints.tsv` the milestone evidence, and `refs/notes/ka0s-review` the reviews.

## What shipped (merged and pushed to `master`)

| Repo | Result |
|---|---|
| WowAddonStandards | **v2.103.1**. The roster gains a Clients column (`Retail · Forever` / `Retail` / `Retail (port pending)`). The new `clients` section covers detection through Compat, gating at registration, per-client seed lists, two kit profiles and both-client smoke. It rewrites the Retail-only TOC, compat, layout, packaging, versioning, badge, testing and quirks rules, and adds anti-patterns #113–#117. v2.103.1 fixes one British spelling in the vendored quirks block. |
| dev-copilot | **2.8.0**. `roster_clients.py`; per-slot `wow-bump-interface`; dual-client `wow-new-addon`; both kit profiles in `bump-version` and `wow-automated-tests`; per-client review checks; and the journal records Forever game versions. |
| LibKa0s | **v1.92.0 and v1.93.0, both tags pushed**. Compat `IsForever` / `IsRetail` / `ClientKey` / `ForClient`, now at Compat minor 3, which accepts `{ "both" }`. `clients` gating in Options (pages, tabs, rows, landing, NavRail, Defaults and Reset all), Slash (verbs, help, schema CLI, `FindCommand`), Launcher and Keybinds, with tokens validated at registration. Kit revision 53 adds the `retail`/`forever` profiles (`KA0S_KIT_CLIENT`) and the static missing-globals suite (#77) with its path-scoped built-in allowlist. Also: `OptionsHeader` peeled out of `OptionsTabs`, and Perf reads the spec name through `C_SpecializationInfo`. |
| 17 roster addons | Ace3 at **`ac3d1225`** (CheckBox v27, ColorPicker v29, AceDB 40; the Retail profile-key proof passed). LibKa0s v1.93.0 and standard v2.103.1, each README gains a supported-clients sentence, and WG and PGFE gain the Forever load-gating lines. Sim strips and titles read **SIM** in AT, BL, DR, DW, KC, LH and MM, and the DpsRace HUD and Results show the sim strip during a sim. OutfitterReborn changes the action-bar page through `C_ActionBar`, and restores it, on both clients. No version bumps. |

## Verification

- Owner smoke: SM-R1 to R5 passed. SM-F1 was recorded (`C_SpecializationInfo.GetSpecialization()` returns 1 on Forever). SM-F2 was waived.
- SM-R6, SM-R7 and SM-R8 (the M5 follow-ups) ran after the merge and **passed** (owner, 2026-11-07); see `03_SMOKE_TESTS.md`.
- Every reviewed task passed its review, after fix rounds where there were any. The whole-branch final review, on the most capable model, returned "Ready after fixes". One fix wave followed, and a scoped re-review found every item addressed.
- Merge gates, run at finalize on the merge result: every addon had 0 failed tests and luacheck 0/0 (totals per repo are in the finalize log in the session). LibKa0s: 4262 passed, 0 failed under both profiles.

## Follow-ups

- **LibKa0s#76:** move from Ace3 `ac3d1225` to Ace3's first tagged release that includes it.
- **LibKa0s#78:** deferred items: the SimPanel default title, three points of standard wording and the Forever TOC exclude, and three dev-copilot nits.
- **Step 5:** per-addon Forever ports, decided one addon at a time (LibKa0s#44). WhatGroup and PGFE stay Retail-only.
- **Process note:** the finalize script's first pass mis-parsed the gate output, so it stopped before pushing, with each addon merged locally. A corrected resume re-gated every merge result before pushing. Nothing unverified was pushed.
