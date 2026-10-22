# Drop Watcher simulator: what is generic, what the host supplies, and what LibKa0s-Sim-1.0 must parameterise

Read-only extraction. Sources: `DropWatcher` master `5611fe4`, `LibKa0s` master `d9f9454` (unreleased v1.75.0, kit 40). File line numbers below are each file's own (`modules/Sim.lua:127` means line 127 of that file).

Files read:
- `core/SimSeam.lua` (142 lines), `modules/Sim.lua` (403), `modules/SimScenario.lua` (340), `modules/SimPanel.lua` (685) and `settings/SimVerbs.lua` (224).
- The plug-ins `SimEvents` (515), `SimWorld` (505), `SimPool` (385), `SimRoster` (280) and `SimReport` (157).
- The host touch points: `core/DropWatcher.lua`, `core/LifecycleSetup.lua`, `modules/History.lua`, `modules/LootFeed.lua`, `modules/Situations.lua`, `modules/WindowTitleBar.lua`, `modules/WindowFooter.lua`, `modules/Diagnostics.lua` and `DropWatcher.toc`.
- Both specs (`2026-10-11-drop-watcher-simulator-design.md`, `-sim-feedback-design.md`).
- `tests/test_sim_*.lua` (7 suites, 2,989 lines).
- `LibKa0s/PerfPanel.lua` (275), `Perf.lua` (997) and `Lifecycle.lua`.
- `analysis.json` clusters c53/c54.

---

## 1. The whole simulator at a glance

| File | Role | Generic share |
|---|---|---|
| `core/SimSeam.lua` | Wraps every non-pure `NS.Compat` function at load. Holds the provider table, the guarded members and `Live`. | Mechanism ~45 lines (`:36-39, 50, 86-142`). The PURE and GUARDED data and the sender/hand-over printers are DW's. |
| `modules/Sim.lua` | The session: start, stop, refusals, `Fire`, timers, cleanup list, restrictions, auto-stop, stand-down. | Mechanism ~150 lines. The refusal inputs, dispatcher, restriction model and stop steps are DW's. |
| `modules/SimScenario.lua` | Scenarios, the pure timeline builder, the step machine (Step, Run, Pause, Resume, Restart), listeners. | The step machine `:117-283` and `:329-340` is generic. SCENARIOS, Timeline shape, PLAY, `ready()` and Start are DW's. |
| `modules/SimPanel.lua` | The step panel (PerfPanel's look), the picker, the controls, docking and the saved point. | Composition rules, Controls, RunTo, ClickRow and the frame are generic. Labels, tips, boss names, loot report, docking and storage are DW's. |
| `settings/SimVerbs.lua` | `/dw sim` parse and run. | Parse/Run for start, run, step, pause, resume, restart, stop, status and panel is generic. pull, kill, loot, lockdown, trade and StatusLine are DW's. |
| `SimEvents`, `SimWorld`, `SimPool`, `SimRoster`, `SimReport` | DW's world: event drivers, providers, Encounter Journal item pool, invented roster, loot-burst report. | None. These are host plug-ins and the reference for how a host plugs in (§4). |

The issue's "≈3,400 lines" is the whole sim (3,412). The four "generic" files total 1,570 lines. Of that, about 350 lines are host-neutral mechanism; the panel adds roughly another 250 once its DW wording is lifted out.

---

## 2. Every generic function and its contract

### 2.1 The answer seam (`core/SimSeam.lua`)

| Member | Lines | Contract (as built) |
|---|---|---|
| `Sim.active` | 36 | `true` only while a session runs. `modules/Sim.lua` writes it. Every wrapped Compat call reads it, so the idle cost is one boolean test plus one closure hop. |
| `Sim.bypass` | 39 | `true` only inside `Live`. Ordinary members then answer live; guarded members do not. |
| `Sim.IsGuarded(key)` | 86-88 | True when `GUARDED[key]` exists. |
| `Sim.Answer(key, live, ...)` | 95-100 | `fallback = GUARDED[key] or live`. If a provider is registered, returns `provider(fallback, ...)`; otherwise `fallback(...)`. **A provider's first argument is the fallback**, never the raw live member when guarded. A provider therefore cannot reach the client for a guarded member, even by mistake. |
| `Sim.SetProvider(key, fn)` | 105-107 | Register or remove (`nil`) one provider per member name. Last write wins, so there is no chaining: DW's Sim.lua owns `IsRestrictionActive` and `InChatMessagingLockdown`, SimEvents owns `InCombatLockdown` and `PlayerInCombat`, and SimWorld owns ~33 others. **Two registrations for one key silently replace each other.** |
| `Sim.Live(fn, ...)` | 112-119 | Runs `fn` with `bypass = true` (nesting-safe: it restores the previous value). It is `pcall`ed so `bypass` is always restored, then rethrows with `error(msg, 0)`, which **drops the traceback**. The return is `unpack(out, 2, table.maxn(out))`, so nil holes survive. |
| `wrap(key, live)` | 122-127 | `if Sim.active and (GUARDED[key] or not Sim.bypass) then return Sim.Answer(key, live, ...) end; return live(...)`. |
| load-time wrap loop | 129-133 | One pass over `pairs(Compat)`. Every `type == "function"` member not in PURE is replaced by `wrap(key, member)`. **A member added to `NS.Compat` after this loop, or captured in a local before it, is never simulated** (bar-3 risk; the TOC comments at `DropWatcher.toc:54-67` are the only guard). |
| `Sim.SeamKeys()` | 137-142 | The sorted wrapped keys. Diagnostics and `test_sim_e2e.lua:123` assert coverage through it. |

### 2.2 The session (`modules/Sim.lua`)

| Member | Lines | Contract |
|---|---|---|
| `Sim.IsActive()` | 64-66 | `Sim.active == true`. |
| `Sim.Session()` | 71-73 | `State.sim` or nil. Callers read it; only sim modules write their own fields. |
| `Sim.Status()` | 106-114 | Snapshot: `{active, sends, handOvers}` when idle, plus scenario, situation, startedAt, members, events, restrictions, lockdown and groups while running. **Mixes generic fields with DW ones** (see §3). |
| `Sim.Refusal()` | 127-137 | First reason as a printable line, or nil. Order: stood down, already running, test mode, then the real world read through `Live` (combat, instance, group). |
| `deliver(event, ...)` (local) | 145-157 | Walks `NS.FEATURE_EVENTS` rows in order. For each row whose event matches, it runs `pcall(NS.addon[method], NS.addon, event, ...)`. A failure becomes a `SIM` debug line and the remaining rows still run. It answers the number of handlers called. It **swallows** errors, unlike the live dispatcher, which rethrows the first error after the loop (`core/DropWatcher.lua:60-70`). It also **ignores `NS.rejectedEvents`**, so an event the client refused to register would still be delivered. |
| `Sim.IsDelivering()` / `Sim.delivering` | 164-166 | True only inside `Fire`. This is how a handler tells a simulated input from a real one that arrives mid-session (`LootFeed.lua:576-581`, `History.lua:636`). |
| `Sim.Fire(event, ...)` | 173-183 | Answers 0 (does nothing) unless a session is active and the addon is not stood down. Otherwise it increments `s.events`, writes a debug line, saves and restores `delivering` (so nested Fires work) and calls `deliver`. Answers the handler count. |
| `Sim.After(delay, fn)` | 190-200 | `C_Timer.NewTimer`, tracked in `s.timers[handle]`. Fires only while `State.sim == s`, and removes itself from the set when it fires. Answers the handle, or nil when idle. |
| `Sim.DeliverForCleanup(event, ...)` | 207-211 | Same delivery, but only when **inactive** and not stood down. It exists so a stop step can undo an edge (combat, bag items) with the seam off. |
| `Sim.AddCleanup(fn)` | 216-218 | Appends `fn(session)` to a module-level list. The list runs at stop, after timers are cancelled and the seam is off, each step under `pcall`. It is never cleared, so registration happens at load. |
| `Sim.Start(opts)` | 278-296 | Refusal (printed) answers `false, line`. Otherwise it creates the session table, resets the counts, sets `active` and prints the start line. `opts = {scenario, situation, seed}`. |
| `Sim.Stop(reason)` | 363-376 | Order: (1) cancel timers; (2) `NS.Asks.CancelQueued` **while the seam still guards the sender**; (3) `active = false`, `State.sim = nil`, `delivering = nil`; (4) the engine steps under `pcall` (the AddCleanup list first, then DW's fixed steps); (5) debug and print the reason's line. An unknown reason becomes `stop`. Answers whether a session was running. |
| `Sim.OnWorldEvent()` | 381-389 | Auto-stop: reads the real world through `Live`. In an instance it stops with `instance`; in a group it stops with `group`. |
| `Sim.SetRestriction` / `SetLockdown` | 229-251 | The simulated `ADDON_RESTRICTION_STATE_CHANGED` and chat lockdown, with providers at `:255-269`. DW's model (§3). |
| `Sim.MarkGUID` / `IsSimGUID` | 84-95 | A registry of invented GUIDs, forgotten at stop. Small and only shaped generically. |
| `Sim.HistoryLog()` | 77-80 | `s.log`. DW's session-only history (§4.4). |

### 2.3 The step machine (`modules/SimScenario.lua`)

| Member | Lines | Contract |
|---|---|---|
| `SC.StepDelay()`, `ValidStepDelay`, `DelayText` | 37-66 | The delay between steps, read from the `sim.stepDelay` setting each time the next timer is set. The valid range is 0.5–10 in steps of 0.5, with a fallback of `NS.C.PROFILE.sim.stepDelay`. |
| `SC.StepLine(pos, total, kind, detail)` | 156-160 | `"Simulation step %d of %d: %s."`. A loot step's detail reads `kind: detail`; any other reads `kind (detail)`. |
| `SC.Step()` | 165-179 | Answers `nil, "notRunning" \| "building" \| "done"` or the step. Advances `pos`, calls `PLAY[kind](step)`, then stamps `step.ranAt` and `step.detail`, prints the line and notifies. |
| `tick(t)` (local) | 186-198 | Sets the **next** timer before running the current step, so listeners already see "playing". When none is left it prints the finished line and notifies. |
| `SC.Run()` | 203-214 | Answers `false, notRunning \| building \| playing \| done`. Clears `paused` and ticks. |
| `SC.Pause()` | 219-230 | Cancels `t.playing` and **removes it from `s.timers` by reaching into the session's internals (`:225`)**, then sets `paused`. |
| `SC.Resume()` | 235-240 | Requires `paused`, then runs `Run`. |
| `SC.Status()` / `SC.Steps()` | 244-259 | `{scenario, ready, pos, steps, playing, paused, next, size}` and the live step list. |
| `SC.AddListener` / `SC.Notify` | 263-280 | Listeners are never removed. Each runs under `pcall`. The stop notifies through an AddCleanup (`:283`). |
| `SC.Restart()` | 332-340 | `Stop("stop")`, then `Start(sameName, sameSize)` with a fresh seed. |
| `t.ready` | 168, 206, 292 | The async gate. The timeline refuses to step (`building`) until the host's preparation finishes. For DW that is the Encounter Journal pool. |

### 2.4 The verbs (`settings/SimVerbs.lua`)

- **`V.Parse` (`:62-69`, pure).** An empty argument answers `{verb="status", open=true}`. The bare verbs are run, step, stop, status, pause, resume, restart and panel. The parsed verbs are start (`name [size]`), loot, lockdown and trade. Anything else answers `{verb="usage", form=...}`.
- **`V.Run` (`:220-224`).** Everything outside `FREE = {status, usage, start, panel}` (`:138`) needs an active session, else it prints `notRunning`. Each `DO[verb]` prints the WHY line for a failure code (`:74-96`), and `refused` stays silent because the refusal line already printed.
- **The click path is the typed path.** The panel calls `V.Run(line)` for every action (`SimPanel.lua:281-283`), so a click prints exactly what typing prints.

### 2.5 The panel (`modules/SimPanel.lua`)

Generic logic:
- **`stepState(i, pos, live)` (`:161-167`).** A row before `pos` is done, the row at `pos` is busy, the row after it is ready, and the rest are locked. Every row is locked when the timeline is not live.
- **`startState` (`:169-173`).** Ready when idle. Busy until the timeline is ready, or while `pos == 0`. Done after that.
- **`SP.Compose(m)` (`:230-237`, pure).** The rows are `Start`, then one per step, then `Stop`. Each row is `{key, index, label, command, state, actionable, ahead, ranAt, tip}`.
  - Keys repeat: every timeline row's key is `step`, so rows are addressed **by index**.
  - A timeline row is actionable when the timeline is live and `i > pos`. A row with `i > pos+1` is "ahead": it is locked yet clickable, and runs every step up to it in order.
  - The start row is actionable when idle. The stop row is actionable while running.
- **`SP.Controls(st, running)` (`:244-251`, pure).** Answers `{running, run, pause={verb,label,enabled}, restart, stop}`. Pause swaps to Resume while paused.
- **`SP.RunTo(index)` (`:303-312`).** Repeats `verb("step")` until `pos >= index`. It stops early when a step does nothing.
- **`SP.ClickRow(index)` (`:318-324`).** Re-composes from the live model first, so a stale or locked row never acts.
- **The model (`:259-277`).** A running model is read from the session plus the timeline. A preview model is `Timeline(SCENARIOS[choice])` at pos 0.
- **The frame (`:343-676`).** Built on the first Show. It refreshes on every listener notification (`:679`), saves its point on drag, and is hidden on stand-down (`:683-685`). The test record (`__label`, `__state`, `__command`) is set in `paintRow` at `:456`.

---

## 3. DW-specific couplings inside the "generic" files

### `core/SimSeam.lua`
- **`:45-48` PURE**, DW's member names. Includes `ParseTradeTimeRemaining`, `ReadTooltipLine`, `IsRestrictionStateActive` and `DecodeDuration`, plus the LibKa0s-Compat secret guards (`IsSecret`, `CanAccess`, `IsSafeKey`).
- **`:42` and `:55-69` `Sim.counts.sends/handOvers`, `printSend`, `handOver`.** These use `NS.Print` and `NS.L` with DW wording.
- **`:75-79` GUARDED** (`ChatSender`, `NotifyInspect`, `ClearInspectPlayer`, `InitiateTrade`), DW's outward actions.
- **`:32` `local Compat = NS.Compat`.** Wraps one fixed host table at load.

### `modules/Sim.lua`
- **`:13-19` session shape.** `situation`, `guids`, `restrictions`, `lockdown`, `log`, `pool`, `members`, `world` and `drive` are DW's fields.
- **`:53-58` STOP_TEXT.** `group` and `instance` are DW's auto-stop reasons; only `stop` and `standDown` are generic.
- **`:77-80` `HistoryLog`, `:289` `log = {v=1, groups={}}`.** DW's History shape.
- **`:84-95` MarkGUID / IsSimGUID**, used by SimRoster `:268` and by `forgetMembers`.
- **`:106-114` Status** reads restrictions, lockdown and `#s.log.groups`.
- **`:117-123` `realWorld()`** reads `NS.Situations.ReadInputs` and `NS.Restrictions.InCombat`.
- **`:127-137` Refusal** reads `NS.StoodDownRefusal`, `State.testMode` and DW's L lines (combat, instance, group).
- **`:145-157` deliver** is bound to `NS.FEATURE_EVENTS` rows and `NS.addon[method]`, which is DW's fan-out dispatcher shape (`core/DropWatcher.lua:42-84`).
- **`:175, :208` `NS.IsStoodDown()`** is DW's Lifecycle wrapper (`core/LifecycleSetup.lua:14-16`).
- **`:229-269`, the restriction model.** Reads `NS.Compat.RestrictionTypes`, fires `ADDON_RESTRICTION_STATE_CHANGED`, calls `NS.Restrictions.Refresh`, and provides `IsRestrictionActive` and `InChatMessagingLockdown`.
- **`:286-294` Start.** `GetTime()` is a raw client read in a sim file (permitted only because the seam does not need to answer it). The start line claims "nothing is sent, and your saved history is not touched", which is a host-guaranteed claim.
- **`:311-350`, the engine steps.** `liftRestrictions`, then `NS.AutoAsk.OnWorldChanged`, `cleanFeed` (`NS.LootFeed.Drops/RemoveWhere`, `NS.AutoAsk.Cancel`), `forgetMembers` (`NS.Inspect.Forget`), `NS.Roster.Refresh`, `NS.History.ReleaseLog`, `NS.TradeTimer.Scan`, `NS.Situations.Refresh` and `NS.Window.Refresh`.
- **`:369` `NS.Asks.CancelQueued`**, the one step that must run **before** the seam goes off.
- **`:381-399` auto-stop policy** (instance or group). The FEATURE_EVENTS rows are appended at `:393-395` and the handler on `NS.addon` at `:397-399`.
- **`:401-403`** appends to `NS.STAND_DOWN`.

### `modules/SimScenario.lua`
- **`:39, :55`** read `NS.C.PROFILE.sim.stepDelay` and `NS.Setting("sim.stepDelay")`.
- **`:71-81`** SCENARIOS and NAMES (situation, kind party or raid, bosses, keystone, burst, band).
- **`:85-115`** Timeline's step vocabulary (pull, lockdownOn, kill, loot, lockdownOff, runStart, runEnd).
- **`:125-146`** PLAY drivers bound to `NS.SimEvents`, `Sim.SetLockdown`, `NS.SimReport` and `NS.LootFeed.Get`. The loot step stores `step.report`.
- **`:195`** the finished line hard-codes "/dw sim stop".
- **`:225`** Pause mutates `s.timers` (an encapsulation leak, not a coupling, but a library must close it).
- **`:288-301`** `ready()`: `NS.SimRoster.Create`, `NS.SimEvents.Join`, `NS.SimPool.Status`, `NS.ShowWindow` and `NS.Window.Refresh`.
- **`:312-327`** Start: `def.situation`, seed, `size`, `band`, `NS.SimPool.Build(..., ready)`.

### `settings/SimVerbs.lua`
- **`:26-55`** the DW verbs pull, kill, loot, lockdown and trade, with their parsers.
- **`:79-87`** DW WHY codes (noPool, noLooter, engaged, notEngaged, noDrop, notSim, notInBags, expired, noPartner).
- **`:100-121`** UsageLines and StatusLine (members, situation label through `NS.WindowFooter`, `NS.SimRoster`).
- **`:180-215`** the DW `DO` verbs.

### `modules/SimPanel.lua`
- **`:33`** `NS.Constants.WINDOW` (`DOCK_GAP`).
- **`:35`** frame name `DropWatcherSimPanel`.
- **`:58-64`** SCENARIO_LABEL and SIZES (raid sizes 9, 12, 15 and 19).
- **`:67-85`** KIND_LABEL, KIND_TIP, START_TIP and STOP_TIP, in DW wording.
- **`:89, 177, 185-191, 221`** `NS.TipMarks.Row/Hint` (DW's tooltip grammar).
- **`:95`** `NS.SLASH .. " sim "`.
- **`:107-159`** `lineCount`, `lootLabel`, `StepLabel` and `bossNames`. These read `NS.SimReport`, `NS.LootFeed.Get` and `NS.SimEvents.BOSSES`, and the pull and kill boss-name preview.
- **`:175-178`** `NS.WindowFooter.Ago`.
- **`:209-213`** loot report tip lines.
- **`:285-297`** `isRaid`: a size is sent only for raid scenarios.
- **`:345-356`** storage at `NS.addon.db.profile.simPanel.point`, absent from defaults and written only by this file.
- **`:370-398, 620-624`** docking beside `NS.Window` through `NS.MineCells.DockSide`, with a redock once the window opens.
- **`:427`** `NS.Icon("confirm")` for the check.
- **`:437, 468, 495, 504`** `NS.Window.AttachTooltip`.
- **`:463`** `NS.Window.TextButton`, DW's own button.
- **`:490, 499`** `NS.MakeDropdown` (a LibKa0s `Dropdown` wrapper).
- **`:579-580`** `NS.BRAND` title and `NS.MakeCloseButton`.
- **`:602`** `NS.ApplySkin`.
- **`:641`** `NS.IsStoodDown`.
- **`:683`** `NS.STAND_DOWN`.

---

## 4. The host contract Drop Watcher satisfies today

1. **The NS.Compat seam, wrapped at load.**
   - **Load order.** `core/Compat.lua`, then `CompatWorld.lua`, then `CompatItem.lua`, then `SimSeam.lua` (`DropWatcher.toc:54-67`). Every file below reads Compat members inside functions only.
   - **Routing.** Every client read the sim must answer is a Compat member: group, units, instance, difficulty, keystone, combat flags, GlobalStrings, inspect, bags, trade window, restriction readers. DW-90 made this true after the first in-game run showed bare globals escaping the seam (`sim-feedback spec §0`).
   - **Enforcement.** `test_sim_e2e.lua:107-121` scans every core, modules and settings file for 16 world-read patterns and for `_G` outside Compat. `:123-131` asserts the key members are in `SeamKeys()`.
   - **Out of reach.** LibKa0s majors that read the client on the host's behalf (Env, Item) bypass the seam.
2. **Event dispatch through one declared table.**
   - The table is `NS.FEATURE_EVENTS = {{event, method}}`. Several rows per event fan out through `DW:OnSharedFeatureEvent` (`core/DropWatcher.lua:42-84`). `Sim.Fire` replays that table.
   - Events the sim must drive: GROUP_ROSTER_UPDATE, PLAYER_ENTERING_WORLD, ENCOUNTER_START and ENCOUNTER_END, CHALLENGE_MODE_START and CHALLENGE_MODE_COMPLETED, PLAYER_REGEN_DISABLED and PLAYER_REGEN_ENABLED, ADDON_RESTRICTION_STATE_CHANGED, CHAT_MSG_LOOT, BAG_UPDATE_DELAYED, INSPECT_READY, the TRADE_* events and UI_INFO_MESSAGE (`SimEvents.lua:286-482`, `SimWorld.lua:266-269`). Payloads follow the client's shapes.
3. **Guarded members.** ChatSender, NotifyInspect, ClearInspectPlayer and InitiateTrade never reach the client while a session runs, including inside `Live`. A provider (SimWorld `:396-408`) gets the guarded answer as its fallback.
4. **Session-only log instead of SavedVariables.**
   - `History.Log()` and `LogFor(sim)` (`History.lua:411-426`) route to `Sim.HistoryLog()` while active. Records carry `sim = IsDelivering()` (`:636`). The stop calls `ReleaseLog` (`Sim.lua:346`).
   - A real drop or trade that arrives mid-session goes to `global.history`. `LootFeed.lua:576-581` classifies it from the **real** situation via `Live`.
   - The library cannot enforce any of this. It is host code.
5. **Refusals (start).**
   - Stood down: `NS.StoodDownRefusal`, which answers the disabled line or "Not available during a performance capture" (`LifecycleSetup.lua:22-27`).
   - Already running.
   - Test mode on. Test mode in turn refuses while a sim runs (`core/DropWatcher.lua:130`): the two are exclusive.
   - Combat, instance or group, read live.
6. **Auto-stop.**
   - Sim.lua's rows for GROUP_ROSTER_UPDATE, PLAYER_ENTERING_WORLD and ZONE_CHANGED_NEW_AREA are **first** in each fan-out (`modules\Sim.lua` is the first module in the TOC at `:124`; `ARCHITECTURE.md:165-169`). The sim therefore stops before any other handler reads the client.
   - Also stops on stand-down, `/reload` or logout: `State.sim` is never saved.
7. **Stand-down and Lifecycle interplay.**
   - Both holds (`disabled`, `perf`) run `NS.StandDown`, which unregisters events and runs `NS.STAND_DOWN` in order. Sim's step is first (`Sim.lua:401`), so the stop cleans up while every module still has its state. SimPanel's hide comes later (`:683`).
   - `Fire` and `DeliverForCleanup` answer 0 while stood down.
   - A Perf capture's suspended arm is a `perf` hold, so starting a capture stops a running sim. Starting a sim during a capture is refused with the perf line.
   - `NS.Lifecycle` is created **after** SimSeam in the TOC (`LifecycleSetup.lua` follows `SimSeam.lua`), so every stood-down read has to happen at call time.
8. **Stop ordering.** Timers first. Then the queued asks are cancelled **with the seam still guarding the sender**. Then the seam goes off. Then cleanups, each under `pcall`, using `DeliverForCleanup` for edges that need the real client (SimEvents `:511-515`). Then the stop line.
9. **Slash verbs.** `sim` is a feature verb in `NS.COMMANDS` (`settings/Slash.lua:86-87`), so the Slash-1.0 dispatcher refuses it while disabled. The verbs are listed in §2.4, and the panel drives them.
10. **Launcher.** None, by design (`simulator spec §4`: "The launcher menu gains no entry; the slash verbs are the interface"). There is no key binding either.
11. **Marking.**
    - Everything invented carries `sim = true` (session, drops, history entries, pool, members).
    - The title bar shows a SIMULATION mode text with a tooltip (`WindowTitleBar.lua:132-141, 315, 341-347`). Test mode wins over it because the two modes are exclusive.
    - The footer shows `Simulating: <situation> · n members` (`WindowFooter.lua:97, 175`).
    - Diagnostics has a `sim` section (`Diagnostics.lua:369-386`).
    - Every injected event and step writes a `SIM` debug line.
12. **Panel state.** `profile.simPanel.point` is window state, not a schema row. It is absent until the player drags the panel, and Reset position clears it.
13. **Asynchronous preparation.** The pool build (`SimPool.Build` with `host = {alive, after = Sim.After}`, `:351`) waits for `EJ_LOOT_DATA_RECIEVED`. That is a **real** event row (`:381`), not delivered through Fire. The timeline answers `building` until it is ready.

---

## 5. Panel geometry and states, PerfPanel against SimPanel

| Aspect | PerfPanel (minor 6) | SimPanel (DW) |
|---|---|---|
| Row geometry | ROW_W 360, ROW_H 22, GAP 4, DOT 8 at x 8, LABEL_X 26, CMD_PAD 10, TITLE_H 24, PAD 8 (`:32-37`) | identical (`:38-41`) |
| Extra geometry | none | CHECK 12, BAR_H 22, BUTTON_W 84, BUTTON_GAP 6 (`:39, 42-43`) |
| Height | `TITLE_H + PAD*2 + n*(ROW_H+GAP)`, fixed rows (`:173`) | `TITLE_H + PAD*3 + n*(ROW_H+GAP) + BAR_H`, recomputed per paint (`:614`). This equals Perf's formula plus a footer of `BAR_H + PAD`. |
| Width | `ROW_W + PAD*2`, **width-only resizable** through `core.MakeResizable` (Core ≥ 9), rows stretch (`:152-166`) | fixed |
| States | done, used, ready, busy, locked, cancel | done, ready, busy, locked, cancel (no `used`) |
| Colors | same palette, CMD_COLOR 0.45/0.45/0.48 (`:42-56`) | same values (`:47-54`) |
| Dot | `SetColorTexture`, alpha 0.35 when locked | same |
| Done mark | none (dot only) | a `confirm` icon texture over the dot, tinted with the state color; the dot is hidden (`:424-427, 449-453`) |
| Actionable | derived from state: ready, cancel or used (`:100-103`) | host-computed per row; locked "ahead" rows are clickable (`:206-207`) |
| Hover | by state: ready or used gold, cancel light red (`:135-140`) | actionable rows only, using HOVER[state]: ready or locked gold, cancel light red (`:55, 402-409`). Both reduce to "actionable row: gold, except cancel at 1/0.45/0.45". |
| Click | key-unique; re-checks actionable, `runCommand(cmd)`, `RefreshPanel` (`:141-145`) | by index; `ClickRow` re-composes and runs the verb or verbs (`:318-324, 436`) |
| Command column | set once at build (`:129`) | repainted on every paint (`:446`) |
| Tooltips | none | per row and per control, through DW's styled `AttachTooltip` and `TipMarks` |
| Footer | none | the picker (scenario dropdown, size dropdown for raids, Start) **or** the controls (Run all, Pause/Resume, Restart, Stop), whichever applies |
| Title | `P.title .. tr("PANEL_TITLE_SUFFIX")`, centered at y −6 | `"%s - Simulation":format(NS.BRAND)`, same anchor |
| Close | `core.MakeCloseButton(frame, Hide, addonName)` at TOPRIGHT −6, −3, **or** the host's `decorate(frame, api)` (exclusive, `:204-215`) | `NS.MakeCloseButton`, same anchor |
| Frame | `d.name.."PerfPanel"`, BackdropTemplate, DIALOG strata, movable, clamped, drag, Core skin, UISpecialFrames | `DropWatcherSimPanel`, same flags |
| Position | CENTER −320, 0; not saved | saved point if dragged; else docked right or left of the main window (`DockSide` with `DOCK_GAP`); else CENTER +420; redocks once the window opens |
| Test record | `b.__label/__state/__command`, `frame.buttons[key]`, `P.__panel()` | `b.__label/__state/__command`, `frame.rows[i]`, `frame.__rows`, `SP.Frame()`, `SP.Stats()` |
| Lifecycle | none | Show refused while stood down; hidden on stand-down |

---

## 6. What the library version must parameterise

The design keeps to the owner's bar: the smallest contract that serves DW, LootHistory and BankLedger with the same semantics, additive-only. Everything is per instance (Perf's rule: each host gets its own seam, session, frames and listeners).

### 6.1 Shape

- **`LibKa0s-Sim-1.0` is a new major** with four files, each paired on the shell's minor as Perf's secondary files are:
  - `Sim.lua`: shell, seam and session.
  - `SimTimeline.lua`: the step machine.
  - `SimVerbs.lua`: the generic verbs.
  - `SimPanel.lua`: the panel, built on `W.StepPanel`.
- **Floors:** Core (skin, close mark, SafeToString) and Widgets (StepPanel, Dropdown). No Lifecycle floor: the host passes a stood-down function, because `NS.Lifecycle` does not exist yet when the seam must wrap (§4.7).
- **`W.StepPanel` goes in `LibKa0s-Widgets-1.0`** as a new file, `WidgetsStepPanel.lua`. It is public because two majors consume it (Perf and Sim). A Sim-private file would force Perf to reach a `__` internal, which the new §7 rule "`__` internals are not contract" forbids.

### 6.2 `Sim:New(d)`: the descriptor

| Field | Required | Contract | DW value |
|---|---|---|---|
| `name` | yes | Addon folder: frame names, close-mark folder, debug and print prefix. | `"DropWatcher"` |
| `compat` | yes | The table to wrap. **Wrapped once, inside New.** | `NS.Compat` |
| `pure` | no | `{[key]=true}`: never wrapped. | `SimSeam.lua:45-48` |
| `guarded` | no | `{[key]=fn}`: the safe answer. The live member is never reached while active, inside `Live` included. | `SimSeam.lua:75-79`, with the host keeping its own counts |
| `deliver` | yes | `fn(event, ...) -> n`. Calls the handlers this event's registration would call, in order. The library wraps each **call to deliver** in `pcall`; per-handler isolation is the host's (DW keeps its pcall-per-row). | DW's FEATURE_EVENTS walk (`Sim.lua:145-157`), moved to `core/DropWatcher.lua` beside the live dispatcher. It should also honor `NS.rejectedEvents`. |
| `isStoodDown` | yes | `fn() -> bool`, read at call time. | `NS.IsStoodDown` |
| `refusal` | no | `fn() -> line\|nil`. **Run inside `Live`** after the library's own "already running" check. The host owns every world rule, and the library never relaxes or adds one: this keeps a bar-2 flag out of the contract. | Stood down, test mode, combat, instance, group |
| `beforeOff` | no | `fn(session)`. Runs at stop after the timers are cancelled and **while the seam still guards**. | `NS.Asks.CancelQueued("simStop")` |
| `stopSteps` | no | `{{name, fn(session)}, ...}`. Run after the AddCleanup list, each under `pcall`, with the seam off. | ENGINE_STEPS (`Sim.lua:340-350`) plus `liftRestrictions` |
| `autoStop` | no | `fn() -> reason\|nil`, run inside `Live` by `sim:CheckAutoStop()`. The host wires its own world-event rows to call it, **first** in each fan-out. | instance, then group |
| `stopText`, `L` | no | Reason → line. Library STRINGS are overridable through `rawget(L, key)` (Perf's `tr`, `Perf.lua:589-594`). Library reasons are `stop` and `standDown`; host reasons are added. | `group`, `instance` |
| `print`, `debug` | no | Call-time sinks, `debug(tag, fmt, ...)` with tag `SIM`. | `NS.Print`, `NS.Debug` |
| `scenarios` | yes for the timeline and panel | `{names = {...}, defs = {[name] = {label, sizes?, timeline = fn(def) -> steps}}}` | `SC.SCENARIOS`, `NAMES`, `SP.SCENARIO_LABEL`, `SIZES` |
| `prepare` | yes | `fn(session, def, opts, ready)`. The host builds its world and calls `ready()` once (sync or async). | pool build, then roster, Join and window open (`SimScenario.lua:288-327`) |
| `play` | yes | `fn(step, session) -> did, detail`. One step's event driver. | PLAY (`:125-146`) |
| `stepDelay` | no | number or `fn() -> number`, read as each next timer is set. Default 2. | `SC.StepDelay` |
| `slash` | yes | The typed prefix, e.g. `"/dw sim"`, for command columns, usage and lines. | `NS.SLASH .. " sim"` |
| `verbs` | no | `{[verb] = {parse = fn(words) -> cmd\|nil, run = fn(cmd) -> ok, code}}` extra verbs, plus `why = {[code] = line}` and `usage = {lines}`. | pull, kill, loot, lockdown, trade and their WHY codes |
| `statusLine` | no | `fn(status) -> line` | `V.StatusLine` |
| `panel` | no | §6.5 | |

### 6.3 The instance: what replaces today's members

- **Seam.**
  - `sim:SetProvider(key, fn)`: the provider is called as `fn(fallback, ...)`.
  - `sim:Live(fn, ...)`: rethrows the original message. Recommended: `xpcall` with a traceback, so a host error is not stripped.
  - `sim:IsGuarded(key)`, `sim:SeamKeys()`.
  - **New in the library:** a `__newindex` on `compat`, only if the table has no metatable, so a member *added* after New is wrapped too. This closes half of the load-order risk. Replacing an existing key still escapes, so New also records the wrapped closures, and `sim:SeamKeys()` plus a `sim:Unwrapped()` check let a suite assert nothing escaped.
  - **Decision for the owner:** whether provider registration should refuse a second provider for the same key instead of silently replacing it.
- **Session.**
  - `sim:Start(opts) -> ok, refusal`. `opts = {scenario, seed, ...}`, and host fields are copied onto the session.
  - `sim:Stop(reason) -> bool`.
  - `sim:IsActive()`. The hot path keeps it in an upvalue, and **there is no public `active` field**. DW must change its eight direct reads: `core/DropWatcher.lua:130`, `History.lua:413, 424, 535, 636`, `LootFeed.lua:578-580` (which reads `Sim.delivering` and `Sim.active` directly), `Situations.lua:180` and `WindowTitleBar.lua:343`.
  - `sim:Session()`: library fields `{sim = true, scenario, seed, startedAt, events}` plus a host bag. The host bag is the table itself, but `timers` stays library-private.
- **Delivery.**
  - `sim:Fire(event, ...)` answers 0 unless active and not stood down.
  - `sim:IsDelivering()`.
  - `sim:DeliverForCleanup(event, ...)` works only while inactive.
- **Timers.** `sim:After(delay, fn) -> handle`. The handle's `Cancel()` also forgets it, which **fixes the `SimScenario.lua:225` reach-in**.
- **Cleanup.** `sim:AddCleanup(fn)`, ordered and pcalled, runs before `stopSteps`. Note that today DW's SimEvents and SimScenario cleanups run **before** its engine steps (`Sim.lua:341`), and this split preserves that order exactly.
- **Status.** `sim:Status()` answers `{active, scenario, startedAt, events, timeline = {...}}`. The host merges its own fields for diagnostics.

**Kept in the host, not the library:**
- `SetRestriction` and `SetLockdown` (DW's restriction model). LootHistory or BankLedger may copy them if needed; promotion waits for a second identical use.
- MarkGUID and IsSimGUID: a session-bag field.
- HistoryLog and the session-log routing.
- `counts` (sends, hand-overs).
- The SIM title-bar text, footer and diagnostics text. Under the new **preview-mode marker rule** these are host markers, and the library supplies only `IsActive`.

### 6.4 Timeline and verbs (`SimTimeline.lua`, `SimVerbs.lua`)

- **The step machine.** Generic Step, Run, Pause, Resume, Restart, Status, Steps and RunTo (moved here from the panel), plus `AddListener` and `Notify`.
  - Answer codes: notRunning, building, done, playing, notPlaying, notPaused, unknown, refused.
  - The step line and finished line come from library STRINGS, formatted with `slash`.
  - `ready` is set by the `prepare` callback's `ready()`.
- **Verbs.** `sim:RunVerb(line)` parses the generic verbs (start `<name> [size]`, run, step, pause, resume, restart, stop, status, panel, and the bare form, which shows status and opens the panel), then the host `verbs`.
  - `FREE` = status, usage, start, panel.
  - WHY lines: library codes plus host codes.
  - The host wires one Slash-1.0 row: `{"sim", desc, function(rest) NS.Sim:RunVerb(rest) end}`, which keeps it a feature verb that the dispatcher refuses while disabled.
- **Size.** It reaches `prepare` only when the scenario declares `sizes`, which generalises DW's `isRaid` (`SimPanel.lua:285-297`).

### 6.5 The panel (`SimPanel.lua` on `W.StepPanel`)

**Library-owned:**
- Compose (start, steps, stop), stepState and startState, Controls, ClickRow (re-compose by index, then RunVerb), the RunTo flow, the preview model and the picker.
  - The picker shows a scenario `Dropdown` from `scenarios.names` and labels, and a size `Dropdown` only when the chosen def has `sizes` (with "random" = 0).
- The controls strip, the listener repaint, stand-down hide (on `Stop("standDown")`) and Show refused while stood down.
- Saving the dragged point and Reset position.

**Host-supplied panel fields (`d.panel`):**
- `title`: a string, or `fn()`.
- `stepLabel(step, i, steps) -> string` and `stepTip(step) -> {{label, value}}`. DW's boss-name preview and loot report live here.
- `startTip` and `stopTip`.
- `store() -> table`: the host table the `point` is saved in. DW passes `profile.simPanel`.
- `anchorTo() -> frame|nil`: dock beside this frame. It uses DockSide's rule: right, else left, else float, with the gap as a library constant (`DOCK_GAP`). The panel redocks once the frame shows, and a saved point always wins. Both LootHistory and BankLedger have a main window to dock beside, so this is shared semantics, not a DW flag.
- `check`: a texture path for the done mark. The host passes `NS.Icon("confirm")`, so no `LibKa0s icons:` declaration is needed.
- `tooltip(owner, title, rows, hint)`: renders a tip in the host's style. The default is GameTooltip with double lines. DW passes its `AttachTooltip`/`TipMarks` renderer.
- `button(parent, width, text, onClick)`. The library has no text-button factory today (Core and Widgets have none; DW uses its own `NS.Window.TextButton`). The default is a minimal Core-skinned button. **Owner question:** accept a host factory, or let the panel's buttons change look.

### 6.6 `W.StepPanel(d)`: the render-only widget

**Descriptor:**
- `name`: the frame global.
- `addonName`: the close-mark folder.
- `title`: a string, or `fn()`.
- `rows = fn() -> {{key, label, command, state, actionable?, tip?}}`. `actionable` defaults to state ∈ {ready, used, cancel}, which is exactly Perf's rule.
- `onClick(row, index)`. Called after `rows()` is re-read and `actionable` re-checked.
- `check`: a texture path, or nil.
- `footer = {height, build(frame), paint(frame)}`, or nil.
- `tooltip(owner, rowTip)`, or nil.
- `place(frame)`: called on each Show. Nil means CENTER −320 at build.
- `decorate(frame, api)`: Perf's exclusive chrome hand-off, carried over unchanged. It has zero live hosts but is kept because it is existing Perf surface.

**Answers:** `{Frame, Show, Hide, Toggle, IsShown, Refresh}`.

**It owns:**
- The geometry and palette (§5).
- Hover: an actionable row turns gold, except `cancel`, which turns 1/0.45/0.45.
- The 0.35 locked dot alpha.
- Height = rows plus the footer.
- Rows hidden when the list shrinks.
- Command text repainted on every Refresh.
- Width-only resize whenever `core.MakeResizable` exists. DW's panel gains a width grip, which costs nothing because its footer is left-anchored.
- Skin, DIALOG strata, drag, clamp and UISpecialFrames.
- The `__label`, `__state` and `__command` record.

**PerfPanel rebuilt on it (owner-preferred if cheap and safe): yes, as a separate last commit.**
- It costs about −100 lines in `PerfPanel.lua`, with PANEL_MINOR 6 → 7.
- It must keep:
  - `P.STEPS`, `PanelStateOf`, `PanelIsActionable`, `Show/Hide/Toggle/IsPanelShown/RefreshPanel` and `__panel()`.
  - `frame.buttons[key]`, which PerfPanel fills from StepPanel's row buttons, and `b.step`. The 634-line `tests/test_perf_panel.lua` reaches both (`:237-293, 388-391, 585-602`).
  - The `decorate` exclusivity (`:445-527`).
  - The pairing guard (`__panelMinor` plus `__panelProbeMinor`, `:20-23`).
  - CENTER −320, no check, no tooltip, no footer.
- It gates on `W.StepPanel` in the panel file only. When that is missing, Perf.lua's no-panel fallbacks (`Perf.lua:970-978`) stay in place, and the probe and commands stay live.
- That suite, unchanged, is the "look unchanged" proof.
- If any assertion needs editing, drop the commit and keep the documented in-library duplicate. Nothing else depends on it.

---

## 7. Drop Watcher's migration, and what LootHistory and BankLedger need

**Drop Watcher:**
- **Replace** `core/SimSeam.lua` with `core/SimSetup.lua` at the same TOC slot. It calls `Sim:New` with `compat`, `pure`, `guarded` (its printSend and handOver closures and counts) and call-time closures for everything else.
- **Delete** from `modules/Sim.lua` the generic half: `:64-73, 145-218, 278-376`. Keep the refusal, autoStop, restriction model, stopSteps, MarkGUID and HistoryLog as host code, at roughly 150 lines.
- **SimScenario** keeps SCENARIOS, Timeline, PLAY, prepare and the step-delay setting.
- **SimVerbs** keeps its five DW verbs.
- **SimPanel** shrinks to the label, tip, store and anchor callbacks.
- **The `docs/ARCHITECTURE.md:301` deviation row is deleted**, because the copy is gone.
- **Tests that move to the library:** seam wrap, guard and Live (`test_sim_core.lua:64-160`), fire isolation (`:180-192, 289-304`), timers (`:209-226`), stop-step isolation (`:305-328`), the step machine and verbs parse (`test_sim_scenario.lua:88-110, 193-299`), panel rows and controls (`test_sim_panel.lua:77-160, 236-388`), and a new `test_widgets_step_panel.lua`.
- **Tests that stay in DW**, as integration: everything that names the engine (e2e, history, auto-stop, restrictions, the seam-only scan at `test_sim_e2e.lua:107`).

**LootHistory and BankLedger (new simulators, prerequisites found):**
- **Routing.** Every read the sim answers must go through `NS.Compat`.
  - LootHistory has 59 Compat members and about 23 direct reads outside it.
  - BankLedger has only 13 Compat members, so its bank, bag, money and guild-bank reads must be added first.
- **`deliver`.**
  - LootHistory dispatches capture events on a private bus target (`Reconciler.lua:712-716`, `self:OnEvent(ev, ...)`). Its deliver is `Reconciler:OnEvent(event, ...)` plus the other targets.
  - BankLedger splits OPEN, CLOSE, CHANGE and GUILD_DATA tables (`Ledger.lua:806-822`), and the guild bank opens and closes through `GuildBankFrame` OnShow and OnHide hooks (`:665-690`). Its deliver must map pseudo-events (e.g. `SIM_GUILDBANK_SHOW` and `SIM_GUILDBANK_HIDE`) onto those hook bodies.
- **Saved writes.** Both addons write ledgers to SavedVariables and need a session-only write path, the analogue of `History.LogFor` (§4.4).
- **Guarded set.** LootHistory needs its chat and attribution sends guarded. BankLedger may have an empty guarded set.

---

## 8. Defects and risks to fix on extraction

1. `SimScenario.lua:225` Pause mutates `s.timers`. Handles must self-forget on Cancel.
2. `SimSeam.lua:117` `Live` drops the traceback.
3. `SimSeam.lua:129-133`: members added after the wrap escape it. Fix with `__newindex` plus the `Unwrapped()` check.
4. `Sim.lua:145-157` deliver ignores `NS.rejectedEvents`, and it differs from the live dispatcher's rethrow-first-error. That difference is intended for simulation, but it must be documented in the library.
5. `Sim.lua:293` and the spec's "nothing is sent / history untouched" are **host guarantees**. The library's default start line must not claim them, and the host overrides the string. A library cannot intercept a send outside the guarded set, nor a SavedVariables write.
6. Providers replace each other silently (`SimSeam.lua:105-107`).
7. Reads made by LibKa0s majors on the host's behalf (Env, Item) are not seen by the seam.
8. Payload weight: whole-folder vendoring ships Sim-1.0 into all 14 addons, and 11 will not call it. It is loaded but idle, with no frames or timers until `New`.
9. The Sim major freezes `play`, `prepare` and the step-state vocabulary forever. Keep the step states to Perf's set (done, used, ready, busy, locked, cancel) and add no new state.
