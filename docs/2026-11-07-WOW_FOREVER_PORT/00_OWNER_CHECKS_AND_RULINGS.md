# WoW Forever port: owner checks and rulings

The owner made these in-game checks and rulings on 2026-11-07, after reading
`reports/WoW Forever porting research.md`. The research notes behind that report are in `research_notes/`.

## In-game checks (owner, 2026-11-07)

| Check | Client | Result | What it settles |
|---|---|---|---|
| `/dump WOW_PROJECT_ID, WOW_PROJECT_CAMELOT, GetBuildInfo()` | Forever | `18, 18, "1.60.1", "70790", "Nov  3 2026", 16001, "", " "` | Live Forever reports project ID 18, and `WOW_PROJECT_CAMELOT` is defined as 18. Build 1.60.1.70790, interface 16001. The beta reading of 1 is stale. |
| `/dump GetSpecialization` | Forever | `nil` | The deprecated spec globals are absent on Forever, as the research expected (the shim is gated `classic, standard`). Spec reads need a Compat path. |
| `/dump SetDesaturation` | Retail | `nil` | The global is gone on Retail too, since 12.1.0. |

Corroborating read-only check, made by Claude the same day: the owner's
`_retail_/Interface/AddOns` holds 16 third-party copies of AceGUI CheckBox v27 and 5 copies of v26.
AceGUI registers only the highest widget version, so on this install a third-party v27 masks the Ka0s v26
bug. v26 calls `SetDesaturation` from both `SetValue` and `SetDisabled` (`AceGUIWidget-CheckBox.lua:100-130`).
A Retail player who has no addon carrying v27 would hit the error on every Ka0s checkbox.

## Owner rulings (2026-11-07)

1. **Scope:** every Ka0s addon repo supports Retail and Forever from one codebase. No separate Forever addons,
   and no Classic flavours.
2. **Standard:** the Retail-only rules (`toc-file.md:57-65`, `compat.md`, `anti-patterns.md`, and the other
   rules the report lists) must change so that dual-client support is allowed.
3. **Checkbox / Ace3:** open. Re-vendoring Ace3 or adding a Compat shim is to be decided during planning.
4. **Feature-level addons:** decided one addon at a time. Candidates include PremadeGroupsFilterExtension,
   BankLedger, LootHistory, DropWatcher, MultiMeters, DpsRace, KickCD and OutfitterReborn.
5. **dev-copilot:** must change. From now on, all work builds for both Retail and Forever. That covers
   `wow-bump-interface`, `wow-new-addon`, `bump-version`, the review agent and the audit.
