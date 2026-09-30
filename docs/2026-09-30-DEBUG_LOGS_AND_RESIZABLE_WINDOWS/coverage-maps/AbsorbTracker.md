# AbsorbTracker: debug coverage map (DL-AT-02)

Audited against debug-logging v2.70.0 §8 (flows + Diagnosis) and §9 (coalescing + quiet steady
state). Repo commit `7f4ed1e` on `feat/2026-09-30-debug-logs-and-resize`. Gate: 833/833 tests,
luacheck 0/0, lizard 0 functions over CCN 15.

## Inventory -> existing line -> gap -> action

| Inventory item | Where | Existing line | Gap | Action |
|---|---|---|---|---|
| `[Init]` session summary | `core/DebugLogSetup.lua` initSummary | version, schema, profile, rejected count | no dependency line, no enable state at the moment logging starts | `initSuffix()` adds `stood down (holds: ...)` and `missing libraries: ...` only when present (shares `NS.Diagnostics.MissingLibraries()` with the `ui` section) |
| Schema migration | `core/Database.lua` | `[Migrate]` per step / failure | none (runs at load, debug off; report's `state` covers it) | none |
| Settings writes | Schema library `[Set]`, profile handlers | `[Set]`, `[Profile]` | none | none |
| Addon stand-down / stand-up (disabled, perf holds) | `core/Lifecycle.lua` StandDown/StandUp | none (Lifecycle library logs nothing) | §8 state edge missing | `[Life] stood down (holds: X): pending repaint dropped=yes/no`, `[Life] stood up: N bus subscription(s) replayed` |
| PLAYER_ENTERING_WORLD | `core/AbsorbTracker.lua` OnEnterWorld | `[World] entering world` | kind of loading screen unknown | `(login)` / `(reload)` / `(zone change)` from the event's flags |
| PLAYER_REGEN_DISABLED | OnEnterCombat | `[Combat] entered` | the re-lock the addon took from it not stated | `entered: bars re-locked` when it re-locked |
| PLAYER_REGEN_ENABLED | OnLeaveCombat | `[Combat] left: N events, M repaints[, final]` rollup | none | none |
| UNIT_ABSORB_AMOUNT_CHANGED (hot path) | OnAbsorbChanged | `[Absorb] shield up/gone`, change-gated | secret reads silent: a restricted-content log had no line saying why nothing traced | extracted `traceAbsorb()`; one `[Absorb] reads secret ...` / `reads readable again` per edge |
| UNIT_MAXHEALTH (hot path) | OnMaxHealthChanged | none | none (quiet by design) | quiet test |
| PLAYER_TARGET/FOCUS_CHANGED | OnUnitSwap | none; `[Bar]` covers a show/hide it causes | none | left (see below) |
| Coalesced repaint timer (repeating) | `modules/Timer.lua` doRepaint | none; counted into the `[Combat]` rollup | none | quiet test |
| Visibility ladder pass (repeating) | `modules/Display.lua` ApplyVisibility | `[Bar] unit: shown/hidden (rung)`, change-gated | none | quiet test |
| `/at debug hold` (deferred: live repaints held) | Display HoldPreview / ClearPreview | none | hold and flush invisible | `[Bar] hold: live repaints held for N s`, `hold expired: repaint published`, `hold cleared early` |
| Pending repaint dropped at stand-down | StandDown | none | deferral dropped silently | in the `[Life] stood down` line |
| Library disabled gate refusal | LibKa0s-Slash, chat only | none | §8 refusal not in log | Slash descriptor's printer notes the gate's own `DisabledLine()` when it is the first line of a dispatch: `[Cmd] <verb> refused: addon disabled` (help's notice is not a refusal) |
| `/at debug hold` refusals | `settings/Slash.lua` runHold | chat only | guard not in log | `[Cmd] debug hold refused: addon disabled / bad arguments '<rest>' / every bar disabled` |
| `/at toggle <unit>` unknown unit | runToggle | chat only | refusal not in log | `[Cmd] toggle refused: unknown unit '<x>'` |
| In-combat unlock refusal | `settings/General.lua` locked reaction | chat only; log showed `[Set] locked = false` then `= true` | guard not named | `[Set] locked: unlock refused (in combat)` |
| Options open/register in combat | LibKa0s-Options | `[Cfg] open refused (in combat)`, `register parked` | none here | none |
| Event registration refused (pcall) | noteRejected | `[Events] rejected X` every refusal | repeated on every UNITS sync / stand-up | once per name per session (gated set) |
| Unit panel render pcall | `settings/UnitPanel.lua` | chat only | caught error not in log | `[Cfg] unit panel render failed (page): err`, once per distinct error |
| Bus stand-up rejections | `core/Bus.lua` | `[Bus] rejected on stand-up` | list joined before the debug gate (§4) | join moved behind the gate |
| Launcher click with no handler | `core/LauncherSetup.lua` | `[Launcher]` | none | none |
| Diagnostics report | `modules/Diagnostics.lua` | raw append, user-initiated | none | `MissingLibraries()` exported for `[Init]` |

## Tests (`tests/test_debugcoverage.lua`, 14 cases)

One case per added line with a red-under comment; two quiet-steady-state cases: the absorb path
(1 readable read, 20 secret, 20 readable unchanged -> exactly 2 lines) and the other repeating paths
(10 passes of repaint + max-health + visibility with no change -> 0 lines). Each new case was
confirmed red with the source changes stashed (the second quiet case passes before and after,
because those paths were already quiet; it pins that).

## Deliberately left, and why

- **Target/focus swaps**: no per-swap line. Tab-targeting fires this many times a minute; the
  `[Bar]` transition line already records the only state change it causes.
- **Per-unit event-frame registration changes** after a toggle: the `[Set] units.<u>.enabled` line
  implies it and the report's `events` section shows the result.
- **LSM media fallback**: per appearance pass, per row; the report's `media` section names the rung.
- **ADDON_RESTRICTION_STATE_CHANGED, roster, spec**: the addon does not react to them. The secret
  state it does react to (per read) is now the `[Absorb]` edge.
- **A command echo (`[Cmd] /at ...` for every command)**: rejected; it would add a line to every
  dispatch, and the §10 suites pin exact line counts for profile/reset commands.
- **Degraded (LibKa0s-absent) refusals** ("settings helpers failed to load"): the stub has no
  console, so a debug line would land nowhere.
- **Library-side gaps (not this repo)**: LibKa0s-Options' combat lock on an open page (writes,
  Defaults, tab switches refused until PLAYER_REGEN_ENABLED) logs nothing, and `register parked`
  has no matching flush line. LibKa0s-Slash's disabled gate has no debug seam (the addon reads the
  gate's line instead). Candidates for the next LibKa0s.

## Judgment calls

- New tag `[Cmd]` (the standard's own example tag) for command refusals; everything else reuses
  existing tags (`Life` was already the report's lifecycle section tag).
- Refusal detection for the library gate compares the dispatch's first printed line with
  `cli:DisabledLine()` instead of re-deriving the gate's live-verb rule.
- Change-gating, never a time throttle (J5), on the one path touched (the absorb secret edge).

## Noted, not fixed (pre-existing)

- `tests/test_debuglog.lua:260` and `tests/test_surface_parity.lua:73` cite
  `core/DebugLogSetup.lua:72` for the descriptor; `lib:New` was already at line 96 before this item
  (now 117). Comment-only citations in test files, not touched.
