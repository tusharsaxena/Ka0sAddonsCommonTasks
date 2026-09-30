# ConsumableMaster — debug coverage map (DL-CM-02)

Audit against debug-logging v2.70.0 §8 (flows and the Diagnosis checklist) and §9 (coalescing and the quiet steady state).
Repo: `ConsumableMaster`, branch `feat/2026-09-30-debug-logs-and-resize`.

**The sink.** A naive `NS.Debug(` grep finds nothing because the namespace is `KCM` (`local KCM = NS`). The sink is
`KCM.Debug(tag, fmt, ...)`, a callable table built in `core/Debug.lua` that delegates to the `LibKa0s-DebugLog-1.0`
instance's gated sink. The library also reaches it through descriptor seams: Schema `debug`, Launcher `debug`, and the
Widgets ReorderList `debug`. Before this item there were 33 direct call sites under 12 tags: DB, Bus, Macro, Calc, Scan, Set,
Profile, Event, Bar, Prio, GC and Launcher (via the seam).

## 1. Inventory → existing line → gap → what was done

### Events (`KCM.EVENTS`, `core/ConsumableMaster.lua`)

| Event / path | Existing line | Gap | Done |
|---|---|---|---|
| `PLAYER_ENTERING_WORLD` | `[Event] … login= reload=` | none | — |
| `BAG_UPDATE_DELAYED` | `[Scan]` + `[Calc]` on **every** pass | §9 quiet steady state: an unchanged bag update printed a full `Scanned=[…]` line and a `rewrote 0/15` line each time | `traceScan` and `traceCalc` are change-gated on repeating reasons (`bag_update_delayed`, `item_info_received`). The next line that logs carries `(after N unchanged pass(es))` |
| `GET_ITEM_INFO_RECEIVED` (bag item) | per-item `[Scan] discovered …` + `[Calc]` | the `[Calc]` repeat, as above | same gate |
| `GET_ITEM_INFO_RECEIVED` (non-bag) | none (panel refresh only) | none: this changes no macro | — |
| `PLAYER_SPECIALIZATION_CHANGED` | `[Event]` | none | — |
| `PLAYER_REGEN_ENABLED` | `[Event] … flushed=N` | deferred work: a held write the flush could not apply was invisible, and the stood-down branch (which finishes a mid-fight stand-down) logged nothing | now `flushed=N held=M`. `FlushPending` returns the still-held count. The stood-down branch logs `… stood down: held bar teardown finished` |
| `ADDON_RESTRICTION_STATE_CHANGED` | `[Event] … type active rewrite` | none | — |
| `PLAYER_EQUIPMENT_CHANGED` | `[Event]` for slots 16 and 17 | none | — |
| `LEARNED_SPELL_IN_SKILL_LINE` | `[Calc] reason=learned_spell` | none | — |
| `SPELL_UPDATE_COOLDOWN` / `BAG_UPDATE_COOLDOWN` | none | none: this is a repaint, and silent is correct under §9 | — |

### State edges (§8 Diagnosis)

| Edge | Existing | Gap | Done |
|---|---|---|---|
| Combat in | none | CM does not react to it (writes defer lazily), so no line is owed | the first held write says so: `[Macro] held …` / `[Bar] … held` |
| Combat out | `[Event] PLAYER_REGEN_ENABLED` | see above | see above |
| Restriction state | `[Event]` | none | — |
| Zone or instance change | `[Event] PLAYER_ENTERING_WORLD` | none | — |
| Group roster | n/a | not reacted to | — |
| Spec | `[Event]` | none | — |
| Own stand-down and stand-up (Lifecycle latch) | **none** | MUST | `[State] stood down (holds: disabled[, perf])[; bar teardown held for combat]` and `[State] stood up (holds: none)`, from `core/LifecycleSetup.lua` `traceEdge` |
| Stand-down before logging was on (login with the addon disabled) | none | not reconstructable from the log | `[Init]` gains `, stood down (holds: …)` |

### Deferred work

| Hold | Existing | Gap | Done |
|---|---|---|---|
| Macro writes held for combat (`queueForCombat`) | `[Macro] deferred <name> (combat)` **per macro per pass** | §9: per-item, and repeated on every pass in a fight. The known case is a forced rewrite (MarkAllStale), which marks 15 macros stale and printed 15 lines per pass | per-macro line removed. `M.TraceHeld()` after each pass writes one `[Macro] held N write(s) for combat: …`, change-gated on the queue and forgotten at flush. `[Calc]` counts them as `held H`, not as rewrites |
| Macro flush | `[Event] flushed=N`, and `dropped …` on give-up | an intermediate failed replay was silent | `[Macro] flush of X failed (attempt n of 3): err`, once per distinct error, plus `held=` on the regen line |
| Macro bar `pendingUpdate` (Update, flyout rebuild, position reset in combat) | **none** | hold and flush both invisible | `[Bar] <what> held for combat` on the not-held → held edge only, and `[Bar] flushed the held update` |
| Mid-fight stand-down | none | hold and finish invisible | `; bar teardown held for combat` on `[State]`, and the regen line |
| Options refresh debounce / Add-by-ID hold (`OptionsShim`) | none | not deliberately logged: see §3 | — |

### Refusals (the line names the guard)

| Guard | Existing | Done |
|---|---|---|
| `ResetAllToDefaults` in combat or with no db | chat only (popup) | `[Cmd] reset profile refused: in combat` / `db not ready` |
| Page Defaults in combat (`Panel.lua`) | chat only | `[Cmd] <panel> Defaults refused: in combat` |
| General page maintenance buttons in combat | chat only | `[Cmd] <label> refused: in combat` (via `inCombatNotice`) |
| Macro-bar slot move or hide in combat (`settings/MacroBar.lua` `commitSlots`) | chat only | `[Cmd] macroBar.order/shown refused: in combat` |
| Bar drag reorder in combat (`MB.SwapSlots`) | chat only | `[Cmd] macro bar reorder refused: in combat` |
| Macro drag to the action bar in combat (`MD.Pickup`) | chat only | `[Cmd] pickup <name> refused: in combat` |
| Settings panel open in combat (`O.Open`) | chat only (library) | `[Cmd] settings panel refused: in combat` |
| Schema write rejected (panel `SetAndRefresh` / `SetManyAndRefresh`, `/cm set`) | chat only | `[Cmd] <path> refused: <rule>`. Deliberately not `[Set]`, which stays write-only, as test_bulklog pins |
| Feature verb while stood down, unknown verb (library dispatcher) | chat only | not interceptable without wrapping the library. Covered by the new `[Cmd] /cm <line>` trace plus the `[State]` edge |

### Dependencies

`[Init]` gains `, missing libraries: …` listing whichever of these are absent: 9 LibKa0s majors plus AceGUI, AceDBOptions,
AceConfigDialog, LSM, LDB and LibDBIcon. It is written once per enable, and only when something is missing.

### Errors caught by pcalls the addon owns

| Site | Existing | Done |
|---|---|---|
| `runMacroPass` per-category pcall | `[Macro] X recompute failed` on **every** pass | once per distinct (category, error) |
| `FlushPending` pcalls | only the give-up line | once per distinct (macro, error) |
| `fireApply` (row apply), page Defaults, `makeButton`, Category icon button | chat only | `[Cmd] <site> failed: err`, once per distinct error (`Helpers.TraceCaught`) |
| `SafeRegisterEvent` | rejected list in `[Init]` | none needed |
| Diagnostics per-section pcall | library-owned, in the report | — |

### Flows (§8 main list)

Lifecycle (`[Init]`, `[DB]` migration, `[GC]` prune), core compute (`[Scan]`/`[Calc]`/`[Macro]`), data mutations (`[Prio]`
registry, `[Macro] forced rewrite`, `[Set]` bulk and profile), and settings (`[Set]` at the seam) were already covered.
**Slash verbs** had no trace. Every command now leaves one `[Cmd] /cm <line>`.

### Repeating paths (§9)

| Path | Before | After |
|---|---|---|
| `[Scan]` on bag update | every pass | change-gated (key `scan`) |
| no-write `[Calc]` on bag or item-info | every pass | change-gated (key `calc`). Writing and edge passes always log |
| `[Macro] deferred` in combat | per macro per pass | one change-gated held line |
| `[Bar] <cat> flyout capped` | every `MB.Refresh` (every recompute) per capped slot | change-gated per slot (`flyout:<cat>`) |
| `[Prio] paint` | every repaint of an open Macros page (every pass) | change-gated on cat, rows and spec (`prio.paint`) |
| `[Macro] recompute failed` | every pass | once per distinct error |
| `[Macro] <name> failed — <err>` (a refused write, e.g. a full account quota) | every pass (no fingerprint is stored, so every pass retries), and the `error` answer counted as a rewrite, which bypassed the `[Calc]` gate | once per distinct (macro, error) (`write:<name>:<err>`); `runMacroPass` counts it as `failed F`, apart from `rewrote`, so the no-write `[Calc]` stays change-gated (added in DL-CM-02R) |
| `[Macro] <CAT> body exceeds 255 bytes: <body>` | every pass while the oversized pick stays picked (the check runs before the unchanged early-out) | change-gated per category on the body (`oversize:<CAT>`), forgotten once the body fits (added in DL-CM-02R) |
| Cooldown repaint, bar fade tick, flyout idle poll, options debounce timer | silent | silent |

The gate memory is `KCM.DebugQuiet` (`core/ConsumableMaster.lua`: `Changed`, `First`, `Forget`, `Reset`, `Suffix`). It is
reset on every debug-enable, both live and on the degraded stub, so a new logging window shows the current state first. It is
only consulted behind the debug gate.

## 2. Tests (`tests/test_debugcoverage.lua`, 16 cases, 1130 → 1146)

The Changed/First/Forget unit case. The quiet steady state gets seven repeat-N cases, one per fixed path: Scan and Calc, the
held line, the recompute failure, the refused write (with its `failed F` [Calc] tally), the oversize line, the flyout
cap, and the bar hold. There is also an edge-reasons-always-log case. The
reset-on-enable case is red under a missing Reset. The other cases pin the stand-down and stand-up `[State]` lines, the
combat stand-down hold and its finish, the reset refusal, the refused write under `[Cmd]` with no `[Set]`, the `[Cmd]`
slash trace, and the `[Init]` stand-down and missing-library clauses. Each case has a red-under comment. The quiet-gate cases
were verified red by forcing `Changed` to always answer "changed": five went red.

## 3. Deliberately left

- **`[Prio] paint` is gated with no per-page reset.** Leaving a category page and reopening the same one with nothing changed
  logs no second paint line. A different category, spec or row count still logs. Accepted to keep the gate stateless about
  page visibility.
- **Settings panel open and page switches** (a §8 "view open" flow) are not traced. The Blizzard Settings frame and the
  library's page OnShow own them, and CM has no main window of its own. A Macros page paint and the `[Cmd] /cm config` line
  are the proxies. Flagged for the library (an OnShow `debug` hook on LibKa0s-Options), not done here.
- **Options refresh debounce and the Add-by-ID hold** (`OptionsShim`) are not logged. They are UI repaint scheduling with no
  effect on stored state or macros, and a line per burst would be noise.
- **Library-side lines** (Launcher `ask()` raising on hover goes to the debug seam on every hover; the Perf lines are
  ungated by design) are left to LibKa0s.
- **Wording in chat:** `settings/General.lua`'s `inCombatNotice` says "`<x>` deferred until regen", but nothing is queued
  and the action is refused. The new log line says "refused". The chat text is unchanged because it is a locale residue
  string. Worth an owner look.
- **New tags `State` and `Cmd`.** `State` already appears in the diagnostics report's section tag, and `Cmd` is the tag the
  standard's own §8 example uses. Both are listed in docs/debug.md Coverage.
