# KickCD: 060 debug-coverage map (DL-KC-02)

Audited against debug-logging v2.70.0 §8 (flows + Diagnosis checklist) and §9 (coalescing + quiet
steady state). Repo commit: `ad887ed` on `feat/2026-09-30-debug-logs-and-resize` (the review
round-1 fixes, three `DL-KC-02R` commits on top of `252c38c`, then the round-2 fix `ad887ed`). Line numbers
are at `ad887ed`.

Gate at the commit: `lua tests/run.lua` 1228 passed / 0 failed / 0 skipped; `luacheck .` 0 / 0;
lizard: no function over CCN 15. The touched ones peak at CCN 15, at the threshold: `setLocked`
(`core/KickCD.lua:170-183`, 13 before `5c19b74` added the `verb` line and its two `refuse()` calls).
`runDebug` (`:449-473`) stays at 8.

## S4.1 Inventory, and S4.2/S4.3 gap -> action

### Events and state edges

| Inventory item | Where | Existing line (before) | Gap | Action |
|---|---|---|---|---|
| `PLAYER_REGEN_DISABLED/ENABLED` (combat edge) | `core/State.lua:164-186` | `[Combat] entered` / `left` (`:167`, `:170`) | none; nothing is held for combat, so there is no state to add | kept |
| `PLAYER_LOGIN` (combat seed) | `core/State.lua:171` | none | one-shot seed, no decision | left |
| `PLAYER_ENTERING_WORLD` (zone / loading screen) | Cooldowns, IconGrid, Castbar, UnitLabel | effect only: `[Cooldowns] rebuild ...` (change-gated) | the IconGrid rebuild had no line | covered by the new `[IconGrid] [unit] list ...` summary (change-gated) |
| `PLAYER_SPECIALIZATION_CHANGED` (spec edge) | Cooldowns, IconGrid, SpellInput | `[Cooldowns] rebuild <class>(<id>) <spec>(<id>) ...` names the spec | IconGrid's rebuild silent | covered by the IconGrid list summary, which names class/spec |
| `SPELLS_CHANGED` / `TRAIT_CONFIG_UPDATED` | Cooldowns, IconGrid, SpellInput | Cooldowns rebuild line (change-gated) | IconGrid silent; cooldown-manager cache invalidation silent | IconGrid list summary; the next CM build logs (below) |
| `PLAYER_TARGET_CHANGED` / `PLAYER_FOCUS_CHANGED` | IconGrid, Castbar | effect only: visibility line, cast gate line | no line per swap | **deliberately left**: the effect lines (`[IconGrid] visibility`, `[Cast] cast gate`, new `[Castbar] cast ...`) are change-gated; a line per swap is one per tab-target in combat |
| `UNIT_SPELLCAST_*` (per-unit filter frames) | IconGrid, Castbar | `[Cast] [unit] cast gate: interruptible ...` (change-gated, `modules/IconGrid.lua:1298`) | the cast bar's outcome was never logged: a suppressed or skipped bar left no trace | **added** `[Castbar] [unit] cast shown / suppressed: visibility <mode> / skipped: the client returned no duration object`, change-gated per unit (`modules/Castbar.lua:935-948`) |
| `SPELL_UPDATE_COOLDOWN/USABLE/CHARGES` (many/s in combat) | `modules/Cooldowns.lua` | `[Cooldowns] N/M changed: ...` only on a material change (`:566`) | none (already quiet in steady state) | pinned with a quiet-steady-state test |
| `ADDON_RESTRICTION_STATE_CHANGED` | not registered | - | the addon does not react to it | none needed (§8: "an edge the addon does not react to needs no line") |
| Group roster | not registered | - | - | none needed |
| Addon stand-down / stand-up (Lifecycle latch) | `core/LifecycleSetup.lua` | none (the latch prints nothing by design) | **gap**: "it stopped working" with the addon disabled or perf-suspended was invisible | **added** `[State] stood down (holds: <keys>) ...` and `[State] standing up ...` (`core/LifecycleSetup.lua:94-101`, called from `standDown`/`standUp`) |
| Per-unit enable / disable (ReconcileUnits) | `modules/IconGrid.lua`, `modules/Castbar.lua` | none | **gap** | **added** `[IconGrid] [unit] unit enabled/disabled` (`:886`, `:898`) and `[Castbar] [unit] unit enabled/disabled` (`:1078`, `:1095`); only on a real edge |

### Deferred work

| Inventory item | Existing | Action |
|---|---|---|
| Combat-held work | none exists: KickCD owns no secure frame and defers nothing to combat's end (`core/LifecycleSetup.lua` header) | none needed |
| Settings-panel registration parked in combat | library `[Cfg]` line via `settings/OptionsSetup.lua:157` | kept (library-owned) |
| `SPELL_UPDATE_*` zero-delay coalescer (`NS.Util.Throttle`) | none | **deliberately left**: a one-frame coalesce, not held work; logging it would be a per-burst line |
| `[Set]` debounce (0.3 s per path) | `settings/SchemaSetup.lua:91`, `:110` | kept; flushes pending lines before any bracket line |

### Refusals and no-ops

| Inventory item | Existing | Gap | Action |
|---|---|---|---|
| `/kcd config` / `NS:OpenSettings` refused in combat | chat notice only | **gap** | **added** `[Open] settings panel refused: in combat` (`core/KickCD.lua:909`) |
| `NS:OpenSettings` with no options layer | chat only | gap | **added** `[Open] settings panel refused: the options layer did not load` (`:917`) |
| Cooldowns `Rebuild` early returns (no class/spec, no stored list) | none | **gap**: empty grid unexplained | **added** `[Cooldowns] rebuild skipped: <reason> (class=, spec=); watching nothing`, sharing the rebuild signature so a slider drag (~20 rebuilds/s) is one line (`modules/Cooldowns.lua:420-428`) |
| IconGrid `BuildActiveList` no spec / no list / not castable / duplicate | per-duplicate line only (`logDuplicateSpell`, pre-formatted) | **gap** for the rest; per-item line | **replaced** by one change-gated summary per unit: `[IconGrid] [unit] list <CLASS>/<spec>: N icon(s) (ids); N not castable (ids); N duplicate spellID(s) skipped (ids)`, or the skip reason (`modules/IconGrid.lua:358-370`) |
| Cast bar start with no duration object / suppressed by visibility | none | gap | the `[Castbar]` outcome line above |
| Spell add refused by the cooldown-manager gate | chat reason only | gap | **added** `[Spells] add <id> to <class>/<spec> refused: not in the cooldown-manager set` (`core/SpellInput.lua:298`) |
| Cooldown-manager gate skipped (off the live pair / no viewer API) | `[Spells]` lines (`settings/Spells.lua:342`, `core/SpellInput.lua:290`) | both pre-formatted inside the gate (§4 letter) | **fixed**: arguments passed to the sink |
| Spell-list writer refused (`Database:AddSpell` no spellID / unknown class / no list; `RemoveSpell`, `SetSpellEnabled`, `SetSpellCategory` not in the list / no list; `MoveSpell` no list / non-number / out of range / same position; `ResetSpellList` no list) | none (the trace comment said "a verb that writes nothing logs nothing") | **gap** (review round 1) | **added** one `[Spells] <act> <id> in <class>/<spec> refused: <guard>` line, at the writer so the Spells page and `/kcd spells` share it (`core/Database.lua:418-422`, called from each writer); `tests/test_spell_registry.lua`'s "writes nothing" case now pins one refusal line per refused verb |
| `/kcd spells` verb refused before the writer | chat only | **gap** (review round 1) | **added** `[Spells] /kcd spells <verb> refused: <guard>` via `refuse()` (`core/KickCD.lua:141-147`) through `spellsRefuse()` (`:678-680`); see the slash-verb inventory below |
| Host top-level verb refused (`lock`/`unlock`/`toggle` with no db or settings layer; `reset`, `resetall`, `resetposition` with no settings layer) | chat only | **gap** (review round 1) | **added** `[Set] /kcd <verb> refused: <guard>` via the same `refuse()` |
| `list`, `get`, `set`, `profile` with no settings layer (`listSettings`, `getSetting`, `setSetting`, `runProfile`) | chat only (`Settings layer not ready yet`) | **gap** (review round 2) | **added** `[Set] /kcd <verb> refused: settings layer not ready` via `refuse()` (`core/KickCD.lua:515`, `:520`, `:525`, `:533`). Practically unreachable through dispatch, since `NS.Slash:OnSlash` is `NS.Slash.cli:OnSlash`, but logged for parity with the reset guards |
| `/kcd debug` refused (`runDebug` unknown subcommand; the `spells`, `castbar`, `interrupt` topics with their module missing) | chat only | **gap** (review round 2) | **added** `[Debug] /kcd debug refused: unknown subcommand '<sub>'` (`:471`) and `[Debug] /kcd debug <topic> refused: <module> ...` (`:386`, `:392`, `:399`) via `refuse()`; new `Debug` tag row in `docs/debug.md`. `on`/`off`/`toggle`/`window` with the DebugLog module missing stay chat-only: that module is the sink, so there is nowhere to log; listed in `docs/debug.md` 'Deliberately not logged' |
| `/kcd set` refused (unknown path, bad value), feature verb while disabled, profile switch in combat | chat, printed by LibKa0s-Slash | no host hook | **deliberately left**: Slash-1.0 "logs nothing" and gives the host no seam; the only host-side refusal path (`Store.Set` answering false through the descriptor's `set`) is unreachable in practice because no KickCD row has a `validate`. Next-LibKa0s residual (see open questions) |

### Dependencies

| Inventory item | Existing | Gap | Action |
|---|---|---|---|
| LibCustomGlow-1.0, LibSharedMedia-3.0, LibDataBroker-1.1, LibDBIcon-1.0 (optional) | the launcher's `[Launcher]` missing-library line, which lands at PLAYER_LOGIN while the flag is off and so never renders | **gap** | **added** a `, missing <names>` clause to the `[Init]` summary (`core/DebugLogSetup.lua:173-183`), empty when all load so the common line is byte-identical; the line lands on enable, which is the once-at-enable the checklist asks for |
| LibKa0s majors | the stubs' own once-only chat notices | none | kept |

### Errors caught by an owned `pcall`

| Site | Existing | Action |
|---|---|---|
| Migration step (`core/Database.lua:960`) | chat + `[Migrate]` line | kept |
| Cooldown-manager walk (`core/SpellInput.lua:191-210`, two pcalls per category) | silent | **added** one build line: `[Spells] cooldown-manager set built: N spell(s) / empty: ...; K viewer call(s) raised[: <site>: <message> \| ...]` (`:217-225`), once per build (memoized), not per call. Review round 1: each distinct `site: message` is kept (`noteError`, `:179-185`; up to three, then `(+N more)`), only while the flag is on |
| Panel link click (`settings/Panel_Widgets.lua:95`) | chat `link failed: <err>` | **added** (review round 1) a gated `[Open] settings link click raised: <err>` line (`:97-99`) beside the chat line; DIAGNOSTIC residue row in `tests/test_locale.lua` |
| Bulk brackets, `RefreshRows`, Reset buttons | re-raise | none needed (the error propagates) |
| Diagnostics frame reads, `valuesFor` hint probe, `CreateAtlasMarkup` | read-only probes, degrade to a missing clause | **deliberately left** |

### Data mutations, settings seam, slash verbs, view open

| Inventory item | Existing line | Action |
|---|---|---|
| Spell-list edits / resets / resetall | `[Spells]` (`core/Database.lua:310`, `:407` trace) | kept; refusals added (above) |
| Schema writes | `[Set] path = value` debounced; bulk `[Set] <act> <scope>: N rows` | kept |
| Profile reset / copy / switch | `[Set]` / `[Profile]` (`core/Database.lua:997-1003`) | kept |
| Migrations | `[Init]` / `[Migrate]` | kept |
| Settings panel open | `[Open] settings panel` (`core/KickCD.lua:921`) + library `[Cfg]` | kept; refusals added |
| Launcher | library `[Launcher]` | kept |
| Rejected events | `[Events] rejected <name>`, once per name | kept |
| Geometry (drag stop, reset position) | none | left: named non-setting state, §10 SHOULD NOT / MAY |
| Perf | `[Perf]` via raw `Add` (ungated by design) | kept |

### Slash verbs (S4.1 inventory, review round 1)

The verb set is `NS.COMMANDS` plus the `SPELLS_COMMANDS` sub-table (`core/KickCD.lua`). A verb's
effect is logged by the flow it drives (the tables above); this table is about what a pasted log
shows when a verb is refused.

| Verb | Refusal owner | What the log shows when refused |
|---|---|---|
| unknown verb | LibKa0s-Slash | nothing (no host seam; chat is the record) |
| `set` / `get` / `reset <path>` (bad path or value) | LibKa0s-Slash | nothing (no host seam) |
| any feature verb while disabled | LibKa0s-Slash | nothing (no host seam) |
| `profile` (switch in combat, unknown name) | LibKa0s-Slash | nothing (no host seam) |
| `config` | host | `[Open] settings panel refused: in combat` / `the options layer did not load` |
| `debug` | host (`runDebug`) | `[Debug] /kcd debug refused: unknown subcommand '<sub>'`; a topic with its module missing logs `[Debug] /kcd debug <topic> refused: <module> ...`. `on`/`off`/`toggle`/`window` with no DebugLog module: chat only (no sink; `docs/debug.md` 'Deliberately not logged') |
| `diagnostics`, `perf` | library verbs | not refusal paths |
| `list`, `get`, `set`, `profile` (no settings layer) | host | `[Set] /kcd <verb> refused: settings layer not ready` (a bad path, value or profile name is the library's, above) |
| `help`, `version`, `events`, `enable`/`disable` | host or library | no host refusal path (`enable`/`disable` go through `set`) |
| `lock` / `unlock` / `toggle` | host | `[Set] /kcd lock\|unlock refused: db not ready` / `settings layer not ready` |
| `reset <path>`, `resetall`, `resetposition` | host | `[Set] /kcd <verb> refused: settings layer not ready`; `reset` given a retired page word (`spells`, or one of the four old page names `general`, `icons`, `castbar`, `label` in `RETIRED_RESET_PAGES`, `settings/Slash.lua:230-235`) logs `[Set] /kcd reset <word> refused: a retired page word, redirected` (`settings/Slash.lua:245`). A bad path is the library's, above |
| `spells` (unknown subcommand) | host | `[Spells] /kcd spells <sub> refused: unknown subcommand` |
| `spells list` | host | `refused: class/spec unresolved` (an empty list is a read, not a refusal) |
| `spells add` | host + writer | `refused: <parse reason>` (usage / unknown spell / bad class or spec), `refused: db not ready`, the cooldown-manager `[Spells] add ... refused`, and the writer's `add ... refused: <guard>` |
| `spells remove` / `enable` / `disable` | host + writer | `refused: no spell id`, `refused: no spell list`, then the writer's `... refused: not in the list` |
| `spells category` | host + writer | `refused: no spell id or category`, `refused: unknown category '<cat>'`, `refused: no spell list`, then the writer's |
| `spells reset` | host + writer | `refused: class/spec unresolved`, `refused: db not ready`, the writer's `reset ... refused` |
| `spells resetall` | host | `refused: db not ready` |

Pinned by `tests/test_flow_traces.lua`'s "a refused spell-list write names its guard" case (the
writer lines, three `/kcd spells` verbs, `/kcd lock` with no db, `/kcd reset spells`, and, round 2,
`/kcd debug frobnicate` and `/kcd debug interrupt` with no `Compat.DebugInterrupt`).

### Repeating paths (§9)

| Path | Rate | Before | After | Test |
|---|---|---|---|---|
| `Cooldowns:Refresh` | per frame in combat (coalesced) | logs only material changes | unchanged | quiet test: 10 unchanged polls add no lines |
| `Cooldowns:Rebuild` | ~20/s on a slider drag | change-gated signature | skip reasons share the signature | quiet test: 5 rebuilds with no list, one line |
| `IconGrid:BuildActiveList` | several per login, every `spells` write | a per-duplicate line on every rebuild | one change-gated summary per unit | quiet test: 6 identical rebuilds, one line; a change logs again |
| `Castbar:Start` | every cast | nothing | change-gated outcome per unit | quiet test: 5 shown casts one line, 5 suppressed casts one line |
| `IconGrid:RefreshVisibility` | cast events, combat, swaps | change-gated | unchanged | existing |
| `IconGrid:RefreshAllGlows` (cast gate) | cast events | change-gated label | unchanged | existing (`test_icongrid_glowgate.lua`) |
| 0.1 s text ticker, cast bar `OnUpdate` | 10 Hz / 60 Hz | nothing | nothing | - |
| `UnitLabel:ApplyAll` | every grid layout | nothing | nothing | - |

## S4.4 Tests added (`tests/test_flow_traces.lua`)

Each carries a `red under:` comment; the three change-gate cases were mutation-checked (removing
the compare reddens the case).

- BuildActiveList writes ONE list summary for an unchanged list, however often it rebuilds
- the list summary names the spells it could not draw and the duplicates it skipped
- a cast bar logs its outcome once per change, not once per cast
- a per-unit enable and disable edge is one line from each module
- the stand-down and stand-up edges are logged, naming the hold
- a rebuild that watches nothing says why, once for a repeated reason
- Cooldowns:Refresh stays silent across passes that change nothing
- a settings open refused in combat names the guard in the log
- the Cooldown Manager walk logs one build line, with the calls that raised (round 1: and the
  site and message of the caught error)
- a settings link whose click raises names the site and the error in the log (round 1)
- a refused spell-list write names its guard, once, from the writer or the verb (round 1)
- the [Init] line names an optional library that did not load

`tests/test_icongrid_buildlist.lua`'s duplicate case now finds the summary's wording.

## S4.5 Docs

`docs/debug.md`: tag table rows updated (`Init`, `Spells`, `Cooldowns`, `IconGrid`, `Open`; new
`Castbar` and `State` rows for `NS.Debug`), the `[Init]` paragraph names the missing clause, and a new
`### Coverage` section (flow, tag, when, repeating-path treatment, and what is deliberately not
logged). `docs/ARCHITECTURE.md`'s documentation-map row for `debug.md` mentions it.
`docs/test-cases.md` regenerated; README badge 1216 -> 1226, then 1228 in round 1 (which also
rewrote the "writes nothing traces nothing" case in `tests/test_spell_registry.lua` to pin one
refusal line per refused verb, and added the spell-list refusal and link-click error rows to
`docs/debug.md`).

## Deliberately left, with why

- **The `(gcd)` churn lines in `Cooldowns:Refresh`** (`modules/Cooldowns.lua:566`). Every GCD writes
  two `N/M changed ... (gcd)` lines (down, then ready): about 80 lines a minute of steady casting,
  enough to turn over the 3000-line buffer in well under an hour. Each line reports a real state
  change, so §9's text allows it ("a per-pass line whose content changes"), but it is the shape the
  quiet-steady-state rule was written against. The marker-not-suppress design is an explicit prior
  decision (issue #15, pinned by five tests in `tests/test_cooldowns.lua`), so it goes to the owner.
- Target/focus swaps, per-cast start/stop, the text ticker and `OnUpdate`, the throttle coalescer,
  and the read-only probe pcalls: reasons in the tables above.
- Slash-library refusals: no host seam (LibKa0s residual).
