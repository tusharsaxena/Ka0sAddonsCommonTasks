# BankLedger: 060 debug coverage map (DL-BL-02)

Audited against debug-logging v2.70.0 §8 (flows and the Diagnosis checklist) and §9 (coalescing and
quiet steady state). Repo commit `7ef7940` on `feat/2026-09-30-debug-logs-and-resize`.
Gate: 1167 passed / 0 failed / 0 skipped, luacheck 0/0, lizard 0 functions over CCN 15.

The test for "enough" was whether a support read of a pasted log could reconstruct what happened.

## Inventory, existing line, gap, action

### Events and state edges

| Inventory item | Where | Existing line before | Gap | Action |
|---|---|---|---|---|
| Stand-up (latch release, load) | `NS.StandUp`, core/BankLedger.lua | none | §8 State edges: own enable transition missing. The swallowed registration refusals (a caught error) never reached the log | **Added** `[State] stood up: N events registered, M unavailable[: names]` |
| Stand-down | `NS.StandDown` | none (only `[Store] … dropped (stand-down)` when a bank was open) | §8 State edges: stand-down missing | **Added** `[State] stood down (holds: …)[; login prune postponed]` |
| PLAYER_REGEN_DISABLED / ENABLED | `addon:OnCombatChanged` | none | §8 combat in/out edge, reacted to (visibility pass, test mode end) | **Added** `[Combat] entered/left: visibility <mode>, hid N, re-showed N`, emitted only when the addon reacted (a window moved, a combat-bound rule, or test mode ended). Silent under `always` |
| PLAYER_ENTERING_WORLD | `addon:OnEnterWorld` | none | §8 deferred work: the login prune is held 5 s; no hold line | **Added** `[Prune] login retention pass armed: runs in 5s` |
| BANKFRAME_OPENED / CLOSED | Ledger OpenContext / CloseContext | `[Store] X opened (baseline …)`, `[Store] X closed` | A close that throws a held one-sided change away was silent | **Changed** closed line gains `, held change dropped` |
| GuildBankFrame OnShow / OnHide hooks | `L:HookGuildBankFrame` | `[Store] GUILD_BANK frame hooks installed`; open/close via the lines above | §8 refusal: OnShow ignored while another context is armed was silent | **Added** `[Store] GUILD_BANK shown while BANK_FRAME is open: context kept` |
| GUILDBANKBAGSLOTS_CHANGED | `L:OnGuildBankData` | reconcile lines only when armed | Not arming (window not visible) is silent | **Left**: fires on login sync and every guildmate's deposit; a line per event is §9 spam. The absence of an `opened` line is the evidence (smoke CAPT-14) |
| BAG_UPDATE_DELAYED, PLAYERBANKSLOTS_CHANGED, PLAYER_MONEY | debounced `ScheduleReconcile` | per-pass `[Diff]`, `[Move]`, per-item `[Skip]` | see Repeating paths | see Repeating paths |
| ADDON_LOADED | `L:OnAddonLoaded` | none; hook install logs | none | Left (hook line covers it) |
| PLAYER_LOGOUT (two window targets) | geometry save | none | named non-setting state, §10 SHOULD NOT log | Left |
| Profile switch / copy / reset | `NS.OnProfileEvent` | `[Set]` / `[Profile]` one line | none | Left |
| ADDON_RESTRICTION_STATE_CHANGED, zone, roster, spec | not registered | n/a | addon does not react | No line needed |

### Deferred work and flushes

| Item | Existing | Gap | Action |
|---|---|---|---|
| Settle hold (one-sided change, up to 6 s) | only the timeout `never settled; baseline re-anchored` | Hold start and settle unlogged | **Added** `[Diff] one-sided change: baseline held, settles within 6s` (once per hold) and `[Diff] held change settled after Ns, N recorded`; `, held change dropped` on the close and stand-down lines |
| Reconcile debounce (0.35 s) | its flush is the pass's lines | a hold line per event would be spam | Left; the pass line is the flush |
| Login prune (5 s timer) | `PruneOld` logged only when retention > 0 | no hold line; no flush line under retention Always; stand-down cancel silent | **Added** armed line; **added** `[Prune] retention always: nothing pruned`; stand-down line says `login prune postponed` |
| Browser / Insights refresh debounces | render/recompute summary lines | none | Left |
| Uncached item under a quality floor | `[Skip] … (uncached)` | none | Kept (now inside the coalesced line) |

### Refusals and no-ops

| Item | Existing | Action |
|---|---|---|
| Capture gate (`GateReason`) | per-item `[Skip]` | Coalesced (see §9 below) |
| Ledger window show refused by visibility / stand-down | silent early return | **Added** `[UI] window show refused: stood down` or `visibility <mode>` (new `Util.VisibilityRefusal` names the guard) |
| Session window held at a session start | silent | **Added** `, window not shown: session window off / capture off / visibility <mode>` on the `[Session] started` line (`SW:ShowRefusal`) |
| `/bl session` preview refused (a real session is open) or held shut (`SW:Show` returning on the window's own switch, capture off, or visibility) | chat only / silent | **Added** `[Session] preview refused: a real session is open`, `[Session] preview on` (with `, window not shown: <SW:ShowRefusal()>` when held shut) and `[Session] preview off` in `SW:TogglePreview`; the StartSession path keeps its own guard on the `started` line, so nothing is double-logged |
| Test mode start refused (combat, visibility) | chat only | **Added** `[Table] test mode start refused: in combat` / `: visibility <mode>`; also `[Table] test mode on: N sample rows` and `test mode off` (material effect; `/bl test` has no `[Set]` line) |
| Slash feature verb refused while disabled | chat only, library-owned (LibKa0s-Slash) | **Left**: the library logs nothing and has no host hook; the `[State] stood down` line explains every such refusal. Residual for LibKa0s (open question) |
| Schema write refused (validate/normalize) | chat only, library-owned (LibKa0s-Schema) | **Left**, same reason. Residual for LibKa0s |
| Filters add of an id already listed | returns false, UI line | Left (UI feedback is the answer; no state change) |

### Dependencies

| Item | Existing | Action |
|---|---|---|
| Bank-replacing addons (ArkInventory, Baganator, …) | report `[Env]` section only | **Added** to the `[Init]` line tail: `bank addons: none` or names (new `NS.Diagnostics.LoadedBankAddons`, shared with the report section) |
| Launcher libraries (LibDBIcon / LibDataBroker / LibKa0s-Launcher) | library `[Launcher]` lines at registration (login, usually gated off) | **Added** to the `[Init]` tail: `launcher registered / unregistered / degraded` |
| LibKa0s itself | no console without it | n/a |

"Once, at enable" is read as the moment logging is switched on (the `[Init]` line), because the
flag is off at every login (§5) and any line at addon enable is always gated off.

### Errors caught by addon-owned pcalls

| Site | Swallows? | Action |
|---|---|---|
| `NS.RegisterEventSafely` (core/CoreSetup.lua) | yes (records the name as unavailable) | Surfaced once per stand-up in the `[State] stood up` line |
| `probeMoney` in `L:Diagnose`, `X.Environment` | yes, into diagnostic output (raw append) | Left (explicit dumps, not the trace) |
| `Panel filterWrite`, `P:Batch`, Schema `SetMany` | no, re-raise | n/a |

### Data mutations, settings seam, views

All already traced and left: `[Data]` delete / delete-by-predicate / purge, `[Prune]` result,
`[Filters]` list changes, `[Set]` at the schema seam (library) and one line per profile reset/copy,
`[Profile]` switch, `[Migrate]` (only when a migration runs), `[UI]` window shown/hidden and tab,
`[Table]` render summary, `[Insights]` recompute summary.

## Repeating paths (§9)

| Path | Before | Action | Test |
|---|---|---|---|
| Reconcile pass while a bank is open (BAG_UPDATE_DELAYED, PLAYERBANKSLOTS_CHANGED, PLAYER_MONEY, GUILDBANKBAGSLOTS_CHANGED, the settle deadline) | one `[Diff]` line per store on **every** pass, identical when nothing changed | **Change-gated** (`traceDiff`): writes on the first pass after an open, on any pass with a movement, and when the summary differs from the last one written for that store. Compare is behind the gate; the cache resets on every open | "reconcile passes that change nothing write nothing after the first" (whole-buffer compare, so `(xN)` folding also fails it); "a pass that records a movement still writes"; "the gate starts fresh on every open". Mutation-checked: removing the gate turns the first red |
| Same pass, capture-gate refusals | one `[Skip]` line **per refused movement** | **Coalesced** to one `[Skip] <store>: <id> <dir> (<reason>), …` line per store per pass; `Ledger:Record` now returns `nil, reason` and traces nothing | "a pass that skips several movements writes one [Skip] line naming each" |
| Combat edges | none | New line is edge-driven and silent when the addon did not react | "a combat edge the addon does not react to writes nothing" (10 edges, 0 lines) |
| Table render / Insights recompute | one summary per recompute | Left: user- or data-driven recomputes whose content changes (§9 "a real recompute stays compliant") | existing |

No OnUpdate, ticker or per-frame path exists in the addon.

## Tests pinned (tests/test_debug_coverage.lua, 17 cases)

State stand-down/up lines; postponed login prune; retention-Always prune line; combat edge under a
combat-bound rule (both directions); combat silence under `always`; refused window show; session
window guard; `/bl session` preview on/held/off/refused; test mode on/off/refused; guild frame over an armed bank; `[Init]` dependency tail;
settle hold lines (one hold line across repeated passes, one settle); close dropping a held change;
the three `[Diff]` gate cases; the coalesced `[Skip]` line. Each case carries a red-under comment.

## Docs

`docs/debug.md` gains `## Coverage` (every tag, emitter, when; the quiet-steady-state rule; what is
deliberately not traced). `docs/smoke-tests.md` gains DIAG-25 (idle bank is quiet), DIAG-26 (edges in
the log), DIAG-27 (refusals name their guard), DIAG-2 names the `[Init]` tail, CAPT-15 reworded for
the coalesced `[Skip]` line. `docs/testing.md` suite tree, `docs/ARCHITECTURE.md` doc-map row,
`docs/test-cases.md` and the README badge regenerated (1167). Moved citations re-pointed:
`core/Database.lua:519-550`, `:415`, `:432` in smoke-tests.md; `modules/SessionWindow.lua:162-167`
in core/BankLedger.lua and tests/test_lifecycle.lua; `modules/Browser.lua:1205` in
tests/test_lifecycle.lua (it was already stale, pointing at `B:OnLedgerChanged`; now the
`Insights:Enable` call it describes).

## Deliberately left, and why

- **Library-owned refusals** (Slash disabled-verb gate, Schema write refusals): chat only, no host
  hook. The stand-down line covers the disabled case. Candidate for a LibKa0s change.
- **Guild data arriving away from a bank**: a high-frequency no-op; a line would be §9 spam.
- **Login-time lines** (`[Migrate]`, first stand-up, the login prune): gated off by §5 at login;
  the report's `state` section carries their outcome.
- **The `[Table]` line on a window resize** repeats the same summary per resize: a user action,
  not a steady-state path; left.
- **Export**: produces output, mutates nothing; not a §8 flow. No line added.
