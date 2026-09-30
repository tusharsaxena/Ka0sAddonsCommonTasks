# MultiMeters: 060 debug-coverage map (DL-MM-02)

Audited against debug-logging v2.70.0 §8 (the flows plus the Diagnosis checklist) and §9 (coalescing
plus quiet steady state). Commit `0363623` on `feat/2026-09-30-debug-logs-and-resize`. Gate after
the commit: 2121 passed / 0 failed / 0 skipped, luacheck 0/0, lizard 0 functions over CCN 15.

## S4.1 Inventory -> existing line -> gap -> what was done

### Repeating paths (§9)

| Path | Rate | Existing line | Gap | Done |
|---|---|---|---|---|
| Refresh pass summary, `modules/Aggregator.lua` `logPass` | 4/s per window | `[Aggregator] window=… rows=…` via `NS.DebugSteady` | The sink's 10 s heartbeat re-emitted the unchanged run as `(x41)`: **the 060 case** | Heartbeat removed from `NS.DebugSteady` (`core/DebugLogSetup.lua`). An unchanged run says nothing; its `(xN)` comes out once, when the run ends |
| Identity rectangle, `modules/Aggregator_Identity.lua` | 4/s mid-pull | `[Aggregator] identity rows=…` via DebugSteady | Same heartbeat | Fixed by the same change |
| Render, `modules/Window.lua` | 4/s per window | `[Render] window N drew D/E rows` via DebugSteady | Same heartbeat | Fixed by the same change |
| Visibility pass, `modules/Visibility.lua` `Evaluate` | every roster, combat, zone and player-state edge (mount, form, glide bursts) | `[Visibility] #1=show(...)` via plain `NS.Debug` on every pass | Repeated identical `#1=show(...)` lines: **the 060 case** | Through `NS.DebugSteady("visibility", …)` |
| Drop reason, `modules/Aggregator.lua` `logDrop` | first drop of every pass, 4/s | `[Aggregator] dropped guid=…` via `NS.Debug` | The same refusal was written every pass for the rest of a pull | Through DebugSteady keyed on the window |
| Partial roster build, `modules/Roster.lua` | retried on every read (4/s) while the unit API is short | `[Roster] partial build (a of b) — will retry` via `NS.Debug` | Written on every retry for as long as the group stayed short | One `logBuild` site for `built`/`partial` via DebugSteady, so a held build writes once and its `(xN)` lands when the completing `built` line arrives |
| Drill view, `modules/DrillDown.lua` `BuildRows` | every refresh while drilled in | `[DrillDown] rows window=… n=…` via `NS.Debug` | Written every pass | Both shapes (spells, deaths) via DebugSteady keyed on the window |
| Meter availability memo, `modules/Provider.lua` `IsAvailable` | refilled after every session update and world entry | none | No line at all for a state edge every window reacts to | New `[Provider] meter available` / `meter unavailable: <reason>`, change-gated |
| Row hover, `modules/Row.lua` `rowOnEnter` | mouse motion | `[Tooltip] row spell=…` via `NS.Debug` | Opt-in behind `/mm debug tooltip`, but opt-in does not exempt a path from §9: resting on a row wrote a line per motion event (review round 1) | Through DebugSteady keyed on the row frame (DL-MM-02R) |
| Cell and name tooltips, `modules/Tooltip_Builders.lua` `CellTooltip` / `NameTooltip` | every rebuild while the cursor rests (4/s) | `[Tooltip] cell … spells=` / `name stats=` via `NS.Debug` | Same: an unchanged rebuild wrote a line every refresh (review round 1) | Through DebugSteady keyed on the hovered frame. Leaving the cell or row calls the new `NS.DebugSteadyForget(frame)`, which writes the held run's `(xN)` and forgets it, so each new hover speaks once (DL-MM-02R) |

`NS.DebugSteady` also gained a nil-key guard, so an emitter with no window id cannot raise as a
table index.

### Diagnosis checklist (§8)

| Item | Inventory | Existing line | Gap | Done |
|---|---|---|---|---|
| Combat in/out | `PLAYER_REGEN_DISABLED/ENABLED` | `[Event] … lockdown= restricted=` | none | — |
| Restriction / secret state | `ADDON_RESTRICTION_STATE_CHANGED` | `[Event] … type= state=` with `restricted=` after refresh | none | — |
| Loading screen, zone | `PLAYER_ENTERING_WORLD`, `ZONE_CHANGED_NEW_AREA` | `[Event]` | none | — |
| Group roster | `GROUP_ROSTER_UPDATE` | `[Event]` + `[Roster] built` | none | — |
| Spec change | not registered, nothing reacts | — | n/a | — |
| Player-state block (mount, vehicle, form, glide, pet battle, death) | registered | none (owner ruling, 2026-09-29) | Left out by owner decision; its effect shows in the now change-gated `[Visibility]` line | Deliberately left |
| Own enable / stand-down | `core/LifecycleSetup.lua` `standDown`/`standUp` | only indirect `[Provider] suspended/resumed` | No edge line; could not tell a `disabled` hold from a perf hold | New `[Init] stood down (holds: …)` / `[Init] stood up` |
| Meter availability | `Provider.IsAvailable` | none | see above | New change-gated `[Provider]` line |
| Deferred: partial roster build | held until the unit API fills | `[Roster] partial …` | Spammed (fixed above); hold and flush now pair up | done above |
| Deferred: staggered chat dump | `modules/Export.lua` `Send` / `cancelQueue` | none | No record of a held tail or of it being dropped | New `[Export] sent …` (at once / staggered / printed locally) and `[Export] canceled the queued rest of a dump: <why>` (superseded, stood down, no player named X); a cancel with nothing queued stays silent. Review round 1 (DL-MM-02R): the hold now pairs with a flush, `[Export] sent the queued rest of a dump (N-1 lines) to X`, written when the last queued line goes out, so a hold with neither flush nor cancel stands out as a tail whose timers never ran; a one-line dump writes `sent 1 line to X` and no longer claims a queued tail |
| Deferred: player-state settle timer | `core/MultiMeters.lua` | none | Its only effect is re-running the visibility pass, which is logged | Deliberately left |
| Refusal: settings write | `NS.SetByPath` | none (the library logs landed writes only) | A rejected write left no trace | New `[Set] <path> refused: <reason>` (the same sentence the caller shows) |
| Refusal: test mode in combat | `WindowManager:SetTestMode` | chat only | no log line | New `[Test] start refused: in combat` |
| Refusal: Player-header sort while restricted | `WindowProto:SortByColumn` | chat only | no log line | New `[Window] window N sort by name refused: restricted` |
| Refusal: export (csv, chat, open) | `modules/Export_Modal.lua`, seven sites | chat only | no log line | One `refuse(act, line)` helper prints and logs `[Export] <act> refused: <sentence>` |
| Refusal: slash verb while disabled | `LibKa0s-Slash-1.0` gate | chat only | Library-owned; `/mm diagnostics` `state` shows the hold | Deliberately left (library surface) |
| Dependencies | LibSharedMedia is the one optional library that can be missing while the console loads | none | not logged | `[Init]` summary now carries `windows N, LibSharedMedia yes/missing` |
| Errors caught by an owned `pcall` | `core/Database.lua` rebuild (logs `(stopped by an error)`), Diagnostics sections (library logs the section) | present | none | — |
| Probe `pcall`s | `core/Compat.lua`, `core/CoreSetup.lua`, `core/Secrets.lua`, `modules/Format.lua`, `modules/Provider.lua` lookups | none | A failure there is an answer (a secret refused, an API missing), and a line per failure would be a line per cell or pass | Deliberately left, recorded in `docs/debug.md` |

### Flows (§8), already covered

Lifecycle (`[Init]` summary, `[Migrate]`, `[Roster]` prune/forget), capture/compute
(`[Aggregator]`, `[Render]`, drop reason), data mutations (`[Windows]`, `[Provider] reset all combat
sessions`, `[Roster] forgot`), views (`[DrillDown]`, `[Columns] paint`), settings (`[Set]`,
`[Profile]`). No gap beyond the ones above.

## S4.4 Tests (red-under confirmed for the three module fixes by reverting them)

- `tests/test_debuglogsetup.lua`: the heartbeat case is replaced by "an unchanged run stays silent
  however long it lasts"; `[Init]` summary window count and LibSharedMedia.
- `tests/test_window.lua`: 80 unchanged refreshes write no `[Aggregator]` or `[Render]` line (the 060 case end to end).
- `tests/test_visibility.lua`, `tests/test_roster.lua`, `tests/test_aggregator.lua`,
  `tests/test_drilldown.lua`, `tests/test_provider.lua`: one quiet-steady-state case per path.
- `tests/test_disabled.lua` (stand-down/up), `tests/test_export.lua` (send and cancel, and a silent
  no-op cancel), `tests/test_export_modal.lua`, `tests/test_schema_paths.lua`,
  `tests/test_windowmanager.lua`, `tests/test_window_header_sort.lua`: the refusal lines.

## S4.5 Docs

- `docs/debug.md`: "The channels" became `## Coverage`: one row per tag with what writes it, when,
  and whether it is steady-gated, plus the deliberately-not-logged list. The `[Event]` paragraph is
  now a subsection.
- `docs/ARCHITECTURE.md`: the `debug-logging-§8` deviation row (the steady-state sink with its
  heartbeat) is **retired**. Its re-check trigger ("debug-logging gains a rule for repeating
  timer-driven passes") fired with v2.70.0 §9, and the heartbeat it ratified is the behavior §9 now
  forbids.
- `docs/common-tasks.md`, `docs/scope.md`: the heartbeat prose is corrected. `docs/test-cases.md` is
  regenerated and the README test badge is now 2121. Moved citations are re-pointed in
  `docs/performance.md` (Provider.lua:375, Aggregator.lua:1158, DrillDown.lua:734) and
  `docs/settings-panel.md` (DebugLogSetup.lua:292). The Provider and DebugLogSetup citations were
  already one line stale before this change.

## Review round 1 (DL-MM-02R)

- The staggered `[Export]` hold now pairs with a flush line, and a one-line dump no longer claims a
  queued tail (rows above). Tests: `tests/test_export.lua` (flush once, one-line dump).
- The three `[Tooltip]` lines are change-gated per hovered frame (rows above), with
  `NS.DebugSteadyForget` on leave. Tests: `tests/test_row_mouse.lua` (cell, name and row rest).
  The source scan in `tests/test_slash_diagnostics.lua` now matches either sink and expects exactly
  three sites. `docs/debug.md` Coverage marks `Tooltip` steady-gated. No deviation row is needed.
- `traceRefused` (`settings/Schema_Paths.lua`) and `traceEdge` (`core/LifecycleSetup.lua`) moved
  above the doc blocks they had split, so `NS.SetByPath` and `standDown` have their own docs again.
- Gate: 2125 passed / 0 failed / 0 skipped, luacheck 0/0, lizard 0 functions over CCN 15.
  `docs/test-cases.md` regenerated, README badge 2125. Citations re-pointed in `docs/performance.md`
  (Row.lua:1167, Tooltip_Builders.lua :930/:948/:1010/:1024/:1038) and `docs/settings-panel.md`
  (DebugLogSetup.lua:316).

## Deliberately left, and why

- **`[Window] N moved to …` once per drag** (`modules/Window_Placement.lua`). debug-logging-§10 says
  a per-drag geometry write SHOULD NOT be logged. That is outside this item's §8/§9 scope and it is a
  SHOULD, so it is flagged here and not changed.
- **`[Roster] built …` after a roster event that rebuilt the same group** is now change-gated along
  with the partial line, so an identical rebuild writes nothing. The `[Event] GROUP_ROSTER_UPDATE`
  line still records the edge itself.
- **The `[Event]` line is not change-gated.** It is one line per real game edge, by owner ruling, and
  none of its events fires many times a second.
- **The console's Clear button** does not reset the DebugSteady comparison, because the library
  offers no hook. A cleared console stays silent until the next change. This is documented; the fix
  would be a library seam.
