# 03 — Specification: the end state

This is what is true when the run is merged. The per-item end states, with file:line, live in `plan-data/items.json`. The full
designs are in `inputs/design-*.md` and `inputs/req-*-sim.md`. **`inputs/OWNER_SCOPE.md` binds over all of them**, and every
"PLAN-REVIEW RESOLUTION" paragraph in an item binds over the rest of that item.

## 1. The library bar

LibKa0s gains exactly this public surface and nothing more:

- `W.SearchBox`
- `W.TestStrip` + `TEST_STRIP.HEIGHT`
- `W.StepPanel`, only if LK-11 succeeds
- `LibKa0s-Glow-1.0`: `Start` and `Stop`
- `LibKa0s-Sim-1.0`: `NewSeam`, `New` and the instance members
- `Item.BonusIDsFromLink`

Every member is additive-only from its first minor, for the life of its major. Everything censused and rejected is
recorded in the API document of the major it would have joined, with its re-check trigger (LK-25), and is indexed in the
standard's open-evolutions (WS-10).

## 2. LibKa0s v1.75.0

- **Payload:**
  - OptionsTabs 9 (no `__releaseChrome`)
  - Core 11, DebugLog 20 and OptionsIdList +1 (corrected comments; an undeclared icon draws blank)
  - Widgets 13 (SearchBox, TestStrip; one file-local `SKIN` that MakeDropdown reads, with no visible change)
  - WidgetsStepPanel 1 (outcome A) or no such file (outcome B)
  - Item 3
  - Glow 1 (new major)
  - Sim 1 + SimTimeline 1 + SimPanel 1 (new major)
  - DebugLogDiagnostics 3
- **Kit 41:**
  - The runner treats a lizard crash or bound as complexity `fail` with every `CCN_*` at 0, parity skipped, and `crashedFiles` naming
    each crashing file through a per-file retry, with the static hint "hoist the table to a local".
  - `fld` always yields a number, and `manifest.json` is always valid JSON.
  - Stderr stays out of the parse.
  - `Kit.__deviationRows` and `Kit.__declineFor` are gone.
- **Registration:** `LibKa0s.xml` and `tests/majors.lua` list Glow (after Item) and Sim with its files. `tests/run.lua` lists the new
  suites. `docs/api/<Major>/` holds current documents and members manifests, and test_versioning is green.
- **Sim-1.0 host contract (H1–H10, `docs/api/Sim/`):**
  - Every simulated client read goes through the host's Compat table, wrapped once at load. `seam:Unwrapped()` is empty, and every host
    suite asserts it.
  - Events arrive through one host `deliver`, which honours rejected events.
  - Members that act on the world are `guarded`.
  - Host fields live on the host's own table, never on the library instance.
  - A second `SetProvider` for a key raises.
  - `Live` re-raises the original error and logs the traceback.
  - `ready()` is bound to its session.
  - Stop is re-entrancy-safe.
  - RunTo shares Run's `playing` slot.
  - `DeliverForCleanup` answers 0 while stood down.
  - The panel position is session-only.
  - The library enforces the refusal order and the guarded-member rule. Saving nothing, sending nothing and never acting on a real
    player are host obligations, stated as such.
- **Release:** green gate, release run with ANALYSIS.md, CHANGELOG `## v1.75.0 — <date>`, and a **local** annotated tag. The tag is
  pushed only by CT-02, after the owner's go-ahead. Until then it may move (OWNER_SCOPE B).

## 3. WowAddonStandards v2.86.0

See `02_UPSTREAM_CHANGES.md` for the table. `scripts/check-standard.sh` passes, LF only, with version stamps in agreement.

## 4. dev-copilot 2.4.0

The re-vendor command handles the icon declaration and the prune. The kit-41 crashed bucket is understood wherever complexity
output is read. The installed plugin is updated by the owner before M2.

## 5. Every roster addon (all fourteen)

- **The re-vendor (`<PFX>-RV`):**
  - `libs/LibKa0s/` and `tests/_kit/` match tag v1.75.0, except that `media/icons/` holds exactly the icons the
    `LibKa0s icons:` line declares, plus each shipped set's license and attribution files.
  - The CLAUDE.md `Bundles … v1.75.0 (MIT).` line is directly followed by that declaration. Quick Comms declares
    `all (icon browser).`
  - The Options degradation stub carries `Drawer` and no `__releaseChrome` mirror.
  - Kit 39 `__fireUnconditional` stand-down cases are green for real reasons.
  - Icon tests check the declaration.
  - README `## Credits` follows documentation-§1 item 12.
  - The gate is green, with a `docs/revendor/` bundle.
- **Standards reference:** v2.86.0 in the TOC `X-Standard`, the README badge and CLAUDE.md, with this run's citations resolving
  (`<PFX>-SR`-type items).
- **No addon version is bumped.**

## 6. Per-addon adoption

| Addon | End state beyond the re-vendor |
|---|---|
| DropWatcher | Simulator runs on Sim-1.0: SimSetup through `NewSeam`, `Sim:New`, `RunVerb`, the library SimPanel. The generic copy is deleted and its own world, events, pool, roster and scenarios stay. Keeps its `sim.stepDelay` setting. `W.TestStrip` (compact variant host-side), `W.SearchBox`, `LibKa0s-Glow-1.0`. The launcher-§6 binding `DropWatcherToggleWindow`. Documented deviations re-checked. Two new issues filed (bonus-hole offset, restriction combat edge). |
| LootHistory | **New simulator** on Sim-1.0 (`/lh sim`). Prerequisites: client reads through NS.Compat, one event and hook dispatch table, resettable state, store accessors. Then a fixture world, drivers, six scenarios with a Reconciler-settled gate, the panel and verbs, docs and a SIM smoke theme. Destructive surfaces are refused during a sim. `W.SearchBox`, `W.TestStrip` (badge kept, routed through L), `Item.BonusIDsFromLink`, the launcher-§6 binding `LootHistoryToggleWindow`, and the options-ui-§19 Price-sources fix. |
| BankLedger | **New simulator** on Sim-1.0 (`/bl sim`). Prerequisites: one capture dispatch, identity through NS.Compat, a write sink. Then the world, a session host with a two-phase stop, scenarios (warband, guild, one-sided) with a gate, the panel and verbs, docs and smoke. `/bl purge` is refused during a sim. `W.SearchBox` (with its magnifier), `W.TestStrip` (badge kept, through L), `Item.BonusIDsFromLink`, and the launcher-§6 binding `BankLedgerToggleWindow`. |
| MultiMeters | `W.TestStrip` in every meter window, visible with the header hidden, using a narrow `ApplyTestStrip` and no tooltip. The launcher-§6 binding `MultiMetersToggleWindows`. The ChatSender comment corrected. |
| QuickComms | `LibKa0s-Glow-1.0`. The perf-hold refusal fixed. The #49 and #56 rejections recorded in its Documented deviations. |
| KickCD | `LibKa0s-Glow-1.0`. |
| WhatGroup | The launcher-§6 binding `WhatGroupTogglePopup`, with a combat-path test. |
| AuraMaster | Test-mode marker audited against preview-mode, and fixed if a layout hides it. |
| AbsorbTracker, ConsumableMaster, PanelMaster, PartyFrameEnhanced, PremadeGroupsFilterExtension, PrettyChat | Re-vendor and standards reference only. |

## 7. GitHub

These run after merge (M4), spaced out:

- LibKa0s #45–#58 closed with their verdicts and census comments.
- MultiMeters#60, WhatGroup#24 and KickCD#38 repointed at Sim-1.0 and left open, `state:triaged`.
- Resolved addon issues confirmed closed and labelled `state:done`: LootHistory#36 and #37, BankLedger#23 and #24, MultiMeters#59, PGFE#25.
- WowAddonStandards#8 closed.
- Two new DropWatcher issues filed.
