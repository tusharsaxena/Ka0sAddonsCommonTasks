# WoW Forever port (steps 1-4 + M5 follow-ups): final whole-branch review

Reviewer: final whole-branch reviewer, 2026-11-07. Read-only, with no edits and no git writes outside this file.
Scope: the 20 diff packages in `final/`, plus direct reads of LibKa0s (`feat/2026-11-07-wow-forever-port`, head 60c2f41),
OutfitterReborn, DpsRace, the standard (master 6f47f6d) and the live `wow-ui-source` deprecation shim.
Re-run here: `ka0s-bounded luacheck .` on LibKa0s gives 0 warnings and 0 errors in 324 files. All 17 addon trees are clean and on the run branch.
External check: `Gethe/wow-ui-source@live:Interface/AddOns/Blizzard_DeprecatedActionBar/Deprecated_ActionBar.lua`
returns early `if not GetCVarBool("loadDeprecationFallbacks")`. When it loads, it defines `ChangeActionBarPage` and
`GetActionBarPage` as forwards to `C_ActionBar.SetActionBarPage` and `C_ActionBar.GetActionBarPage`. Ketho's `live`
set (kit `client_globals_live.lua`) lists only the two `C_ActionBar` members.

## Critical

None.

## Important

### I-1. OutfitterReborn: the action-bar-page effect switches the page but cannot restore it on Retail without the deprecation fallbacks
- **Where:** `OutfitterReborn:modules/Triggers_Effects.lua:73-76` (`currentPage`), with `:59-62` (`pageSetter`) and the test
  `OutfitterReborn:tests/test_triggers.lua:516-545` (it mocks `M.GetActionBarPage`, a global, at `:523`).
- **Failure:** WFP-RV2-OR changed only the setter, which now goes `C_ActionBar.SetActionBarPage`, then `ChangeActionBarPage`.
  The getter still reads only `_G.GetActionBarPage`, and on live Retail that is a deprecation shim, present only while
  `loadDeprecationFallbacks` is on. When the CVar is off, or once Blizzard drops the 12.0.0 shims, `apply` records
  `saved = nil` but still switches the page through `C_ActionBar`. `restore` then calls `setPage(nil)`, which returns on
  `type(page) ~= "number"`. The player is left on the outfit's bar page after the outfit comes off, and nothing logs it.
  Before this run the same client raised on the bare `ChangeActionBarPage`, so the run turns a loud failure into a silent
  half-effect. The test cannot see this, because it supplies the global getter in all three rungs.
- **Fix:** mirror the setter ladder in the getter: `local api = _G.C_ActionBar; local get = (api and api.GetActionBarPage) or _G.GetActionBarPage`.
  In the test's "live client" rung, set `M.GetActionBarPage = nil` and provide `C_ActionBar.GetActionBarPage`. Also
  assert that `Restore` puts the page back. This ships to Retail on merge, so fix it before the merge. It is one commit
  (`WFP-RV2-OR:` or a new `WFP-FIX-03:`). Add an owner smoke check: with `/console loadDeprecationFallbacks 0`, wear and
  remove an outfit that changes the bar page.

### I-2. LibKa0s: the bulk resets still write rows that the `clients` gate removed (gate-copy drift)
- **Where:** `LibKa0s:LibKa0s/Options.lua:932` (page Defaults walks `d.rowsForPage(pageKey)`) and `:980`
  (`O.RestoreAllDefaults` walks `d.allRows()`), both ungated. Compare the CLI, where `Slash.lua:596-601` (`liveRows`)
  gates `resetall`.
- **Failure:** the design says a gated entry "is never created" and is not reachable (§3 anti-goals; clients-§4). A row
  declared `clients = { "retail" }` is not drawn on Forever. Clicking Defaults on its page, or "Reset all" in the
  settings, still calls `applyDefault`, and so the row's `set`/`onChange`, on Forever. A Retail-only row's `onChange`
  usually calls the Retail-only API it configures (a `C_*` member that Forever lacks), so the reset raises in the middle of
  the bulk walk. The bracket then reports a partial reset. The two reset paths also disagree: `/x resetall` skips the row
  and the button writes it. No consumer declares a gated row today, so Retail is not affected. It is latent until the
  first step-5 port.
- **Fix:** wrap both walks in `lib.__GateClients(...)`, the same choke point `RenderRows` uses. Add cases to
  `tests/test_options_clients.lua` under the forever profile: Defaults and RestoreAllDefaults do not call a
  retail-gated row's `set`. It is cheap enough to land in v1.93.0 now. If it is deferred, it must land before the first
  addon flips to `Retail · Forever`, and should be filed as a LibKa0s issue so the deferral is not lost.

## Minor

- **M-1** `WowAddonStandards:standards/standards/clients.md:40` vs `LibKa0s:LibKa0s/Compat.lua:154-160`. The standard
  says the `clients` tokens are `retail`, `forever` and `both`, but `ForClient({ "both" })` raises "unknown client"
  on every client. Only the bare string `"both"` is accepted. A host that follows the standard's wording breaks its own
  registration. **Fix:** accept `"both"` inside the array (preferred), or reword clients-§4 to "nil, the string `"both"`, or
  an array of `retail`/`forever`". Give the bare-string-other-than-"both" error its own message (the deferred M2a minor).
- **M-2** `clients.md:30` says "The library reads `WOW_PROJECT_ID` once". Compat rule 1 and the code read it bare at
  every call. **Fix:** the wording, at the next standard patch.
- **M-3** `LibKa0s:LibKa0s/OptionsNav.lua:257-262` (`O.NavRail` `spec.entries`) and `O.Drawer` ignore `clients`. A
  nav-rail category is a "settings page" in clients-§4's sense, so a host has to filter it by hand, even though the
  standard says the library honors the descriptor on options surfaces. **Fix:** gate `spec.entries` through
  `__GateClients`, or document the host-side `ForClient` for these two.
- **M-4** Key bindings. clients-§4 promises that a Forever player's "key bindings list" shows no trace of a Retail-only
  binding. The library gates only its own editor rows (`OptionsKeybinds.lua:857`). `Bindings.xml` entries still appear in
  Blizzard's Key Bindings panel on both clients. **Fix:** a standard note, or a design for step 5 (for example, binding
  headers that are inert, or no binding for a gated feature). This does not block anything today.
- **M-5** `WhatGroup:WhatGroup.toc:3`, `PremadeGroupsFilterExtension.toc:3` read `ExcludeLoadGameType: camelot`
  only. The research recommends naming `forever, camelot` to survive the type's rename
  (`reports/WoW Forever porting research.md:62`), and SM-F2 (the not-listed check) was waived, so the gate is
  unverified on Forever. **Fix:** `## ExcludeLoadGameType: camelot, forever` in both TOCs and in clients-§7.
- **M-6** `DpsRace:modules/Hud.lua:496-499`. In `modeStrip()`, `simOn() and ui.simStrip or ui.strip` falls through to
  the test strip while a sim runs and the sim strip is not built yet. It is harmless today, because
  `applyTestMarker` builds the sim strip before the title is set (`:550`), but the idiom is a trap. **Fix:**
  `if simOn() then return ui.simStrip end; return ui.strip`.
- **M-7** SIM wording leftovers. Tooltip titles still read "Simulation" (`BankLedger:modules/Browser.lua:710`,
  `LootHistory:modules/Browser.lua:915`), and so do the sim panel titles ("DPS Race - Simulation", "Absorb Tracker -
  Simulation", LH's `%s - Simulation`). The strips and badges are consistent. Whether the owner's "SIM everywhere" covers
  titles and tooltips is the owner's call. Report it and do not change it silently.
- **M-8** `WhatGroup:DEPENDENCIES.md:24`. The Ace3 provenance was appended inside the table cell with no separator
  ("…Profiles page alone Ace3: WoWUIDev/…"). **Fix:** add a `.` or `; `, or move it to its own line under the table.
- **M-9** `OutfitterReborn:modules/Triggers_Effects.lua:60,74` read `_G.C_ActionBar` and `_G.GetActionBarPage`. That is
  one of the missing-globals gate's documented false negatives (`testkit/client_globals.lua` header), and it departs from
  the bare call-time read convention. It is acceptable here because both rungs are guarded, but note it in the OR quirks
  file so the port knows the gate does not see these.
- **M-10** `LibKa0s:LibKa0s/Compat.lua` `ForClient`, and the call-time gates in Slash, Launcher and Options. A typo'd token
  raises on every client, but only when the surface is drawn (help, landing page, menu open, page render), not at
  registration. A typo in one verb's `clients` therefore takes down the whole help index. This matches the documented
  contract and is the deferred M2b minor. Validate once in `Slash:New` and `Launcher:New` when the first consumer
  appears.

Test edits checked for weakening. The new-library-file edits add `OptionsHeader` to loader lists, `majors.lua`, CM's
`test_libka0s` and KCD's major count (20 to 21). The Compat parity edits add the four helpers to the NOT_WIRED lists in
AM, CM, KCD, PFE, WG, PGFE and DW. LH's exact pins became `>=` ratchets, with an exact v1.93.0 pin added
(`LootHistory:tests/test_libka0s.lua:1279-1284`), which is the established pattern. The SIM string assertions were
updated in step with the strings. The LibKa0s `test_perf_core` spec expectation is conditional on the profile, but it is
still exact under retail. `GetBuildInfo` assertions now read the active profile. None of these edits weakens a test.
The one gap I found is the test-side half of I-1: OR's new case mocks a getter that live Retail does not have.

Consistency between the standard, dev-copilot and LibKa0s is clean, apart from M-1 and M-2. Roster values
(`Retail · Forever`, `Retail`, `Retail (port pending)`) map to `retail+forever`, `retail` and `retail-pending` in
`roster_clients.py`. `KA0S_KIT_CLIENT=retail|forever`, with retail the default, is the same in clients-§6, both
dev-copilot specs and `testkit/mock_client.lua`. 120105 and 16001 agree across the kit, TOCs, bump specs and the 16xxx
detector in `client_globals.lua:clientsFromToc`. The README supported-clients sentence is present in all 17 addons, with
the right variant for WG and PGFE.

Retail exposure on merge: there is no addon `clients` declaration anywhere, so every gate takes its `nil -> true` path.
The Ace3 ac3d1225 profile keys were proven headless (ACE-00) and smoked (R1-R3). The WG/PGFE gating lines were smoked
on Retail (R4). The OptionsTabs to OptionsHeader peel attaches at instance time, every addon loads `LibKa0s.xml`, and
mixed old and new copies resolve per file, highest minor wins. I-1 is the only Retail-visible defect I found.

## Triage of the ledger's deferred minors

| Deferred minor | Status | Before merge? |
|---|---|---|
| M1: `open-evolutions.md:13` "sixty-seven" | open; standard is already on master | No. Next standard patch. |
| M3: `bump_interface.py` has no Clients awareness | open; the command doc tells the operator to run `roster_clients` and ask | No. Before the first `/wow-bump-interface` on a ported addon. |
| M3: `bump-version.md` hardcodes the Live numbers | open; the text says to ask when unsure | No. |
| M3: releases report has no versions column | open; the summary carries `gameVersions` | No. Before the first step-5 release. |
| M2a: `Compat.lua:18` wrap | folded in M2b (now wrapped at `:18-19`) | Done. |
| M2a: loader first-`makeEnv`-wins doc line | folded in M2b | Done. |
| M2a: `ForClient` bare-string message | open; see M-1 (the `{ "both" }` drift makes it worth doing with M-1) | No, but pair it with M-1 before the first port. |
| M2a: perf test pin | resolved by the Perf `C_SpecializationInfo` rung plus the conditional expectation | Done. |
| M2b: `FindCommand` ungated / `entryClients` doc | fixed in 88e6c25 / d690237 | Done. |
| M2b: tokens validated at call time, not at registration | open; see M-10 | No. |
| M5lib: false-negatives doc / forever best-effort | fixed in 60c2f41 (header "KNOWN FALSE NEGATIVES") | Done. |
| M5lib: `look()` rescans per test | open, cost only | No. |
| Ruling (LK-08): OptionsTabs header/sub-strip peel owed | done in WFP-LK-08 | Done. |

None of the deferred minors has to be fixed before the merge.

## Verdict

**Ready after fixes.** Fix I-1 (OutfitterReborn page getter, plus its test) before the merge, because it reaches Retail
players. I-2 should land in LibKa0s now, while v1.93.0 is still a local tag. If it is deferred, file it as a
blocking-for-first-port LibKa0s issue. The minors can follow in the next standard or library patch. M-1 and M-5 are the
ones worth doing before the first step-5 port.
