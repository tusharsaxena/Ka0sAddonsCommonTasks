# PrettyChat — 060 debug coverage map (DL-PC-02)

Audited against debug-logging v2.70.0 §8 (flows + Diagnosis checklist) and §9 (coalescing + quiet
steady state). Repo commit: `1d7cdb5` on `feat/2026-09-30-debug-logs-and-resize`. Gate: 552/552 tests,
luacheck 0/0, lizard 0 Lua functions over CCN 15.

PrettyChat is `frameless`: its display is the chat text. It rewrites `_G[GLOBALNAME]` and registers no
event on a default install. Its only event subscription is the lazy combat watcher
(`PLAYER_REGEN_DISABLED` / `PLAYER_REGEN_ENABLED`), which exists only while a combat-scoped visibility is
stored. There is no OnUpdate, ticker or repeating timer (`docs/performance-sweep.md`).

## Inventory -> existing line -> gap -> what was done

| Inventory item | Where | Existing line | Gap vs §8/§9 | Done |
|---|---|---|---|---|
| `[Init]` session summary | `core/DebugLogSetup.lua` sessionSummary | version, schema, profile, rejected events | Stand-down edge and dependencies both settle at load, while the flag is off, so no line could record them | Added `, stood down: <holds>` and `, chat addons: <names>` tails, each only when it applies (default shape unchanged) |
| Combat boundary (PLAYER_REGEN_*) | `modules/Override.lua` onCombatEdge | `[Visibility] <mode> → applied N restored M` | State edge did not name which edge | Now `[Visibility] combat entered/left (<mode>) → applied N restored M` |
| Combat watcher arm/disarm | `modules/Override.lua` SyncCombatWatch | none (only `[Events] rejected …`, repeated on every re-arm) | No record of whether the watcher was armed; the rejected line repeated on every Reapply (§9 steady state) | `[Events] combat watch armed: N/2 events` / `disarmed`, change-gated; rejected line rides the arm line only |
| Latch stand-down / stand-up | `modules/Override.lua` StandDown/StandUp | `[Lifecycle] stood down → holds: …` / `stood up` | none | kept |
| Profile switch / copy / reset | `core/PrettyChat.lua` | `[Profile] switched …`, `[Set] copied …`, `[Set] reset profile …` | none | kept |
| Settings write seam | LibKa0s-Schema via `settings/Schema.lua` | `[Set] <path> = <value>`, bulk `reset <scope>: N rows` | none | kept |
| Format-signature refusal | `settings/Schema.lua` formatAccepted | `[Set] <path> refused: …` | none (names the guard) | kept |
| Migration / prune | `core/Database.lua` | `[Migrate] vA→vB`, `pruned N keys` | none | kept |
| Slash commands (all verbs) | `settings/Slash.lua` OnSlashCommand | none | Log never showed what the player typed; chat replies are not in the log | `[Cmd] /pc <input>` (pipes doubled, built only with the flag on), `(stood down: <holds>)` tail while down |
| Host-owned slash refusals | `settings/Slash.lua` schemaReady, listSettings, runReset, runTest, runDebug | chat only | Refusal with no log line naming the guard | `[Cmd] <verb> refused: <guard>` at each (schema not ready, unknown category, category given to reset, unknown/absent format string, unknown test/debug form) |
| Panel refresher pcalls | `settings/Schema.lua` NotifyPanelChange, `settings/Panel.lua` category refresher | swallowed silently | Errors caught with no trace | `NS.Util.TraceCaught` -> `[UI] <site> failed: <err>`, once per distinct site+error, gated before any key is built |
| Categories tab switch / string select | `settings/Panel.lua` onSelect / OnGroupSelected | none | §8 view flow: tab switches | `[UI] categories tab <name>`, `[UI] <cat> string <NAME>` |
| Settings panel open / combat refusal / parked register | LibKa0s-Options | `[Cfg] opened`, `open refused (in combat)`, `register parked (in combat)` | none (library-owned) | kept |
| Launcher | LibKa0s-Launcher via `core/LauncherSetup.lua` | `[Launcher] …` | Its registration/missing-lib lines run at OnEnable while the flag is off | left (see below) |
| `/pc test` samples | `settings/Panel.lua` TestToConsole | `[Test]` ungated | none | kept |
| Diagnostics report | library + `modules/Diagnostics.lua` | `[Diag]` + sections | none | `Diagnostics.LoadedChatAddons()` extracted so the report and `[Init]` share one walk |

## Repeating paths (§9 quiet steady state)

| Path | Repeats when | Before | After | Test |
|---|---|---|---|---|
| `SyncCombatWatch` re-registration | every Reapply (each latch arm, profile event, visibility write) | `[Events] rejected …` every call when a name was refused | change-gated `armed`/`disarmed`; rejected once per arming | "re-arming an armed watcher logs nothing, however often it runs" (25 passes armed, 25 disarmed -> 0 lines); "a refused event name is logged once per arming, not once per pass" |
| Combat boundary handler | at most twice per fight | one line per edge | unchanged in cadence (a real recompute, not steady state) | "each combat boundary is one line naming the edge…" |
| Panel `OnSizeChanged` fitTree, `C_Timer.After(0)` fit, Profiles redraw | layout | no lines | no lines | n/a |

## Tests added

`tests/test_debug_coverage.lua` (14 cases, each with a red-under comment), registered in `tests/run.lua`
after `test_panel_categories`. Two existing `/pc resetall` line-count cases (test_debuglog,
test_launcher) now expect the `[Cmd]` line first. `tests/test_locale.lua` records the two new `[Init]`
tail literals as residue. A mutation check (removing the arm/disarm change gate) turned both
quiet-steady-state cases red (25 and 11 lines).

## Docs

`docs/debug.md`: `### Tags in use` replaced by `## Coverage` (every tag, emitter, when, including the
library's `Debug`, `Cfg`, `Launcher`, `Diag`), plus `### Quiet steady state` and
`### Deliberately not traced`. Re-pointed moved citations in `docs/performance-sweep.md` (result block
regenerated against the sweep command), `docs/smoke-tests.md`, `docs/slash-dispatch.md`. Wording updated
in `docs/ARCHITECTURE.md` (Event Subscriptions row, rejected-name sentence), `docs/data-flow.md`,
`docs/testing.md`, `docs/module-map.md`. `docs/test-cases.md` regenerated; README badge 552/552.

## Deliberately left, and why

- **Per-string lines in `ApplyStrings`**: 79 lines a pass; callers log the counts (§9).
- **Load-time work** (snapshot, latch armed from the stored path, panel registration, a failing
  migration step): the session-only flag is off at every load, so a line there cannot land. The
  `[Init]` tails carry the stand-down; a failed migration prints to chat and the report's `state`
  section shows stored vs code schema.
- **`NS.RenderSample` pcall**: per-string, and the error is shown in the Preview and `/pc test`.
- **`CountChangedRows` pcalls** in the reset-count paths: a fallback count only; the one reset line
  still lands.
- **Library-owned slash refusals** (unknown verb, unparsable value, feature verb while stood down,
  profile switch in combat): LibKa0s-Slash-1.0 has no debug hook. The `[Cmd]` line and its
  stood-down tail are the log's side. Candidate for a next-LibKa0s residual.
- **Launcher dependency lines** (LibDataBroker/LibDBIcon missing): emitted by the library at
  `OnEnable` while the flag is off, so they do not land; both libs are bundled, and the report's `ui`
  section shows whether the launcher registered.
- **Smoke tests**: no new in-game check added for the coverage lines (not required by S4); they are
  natural candidates for M4's IN_GAME_CHECKS (a combat edge line names the edge; `/pc list Nope`
  gives a `[Cmd] … refused` line).
