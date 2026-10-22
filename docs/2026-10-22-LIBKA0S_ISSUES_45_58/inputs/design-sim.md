# LibKa0s-Sim-1.0 and W.StepPanel: design (LibKa0s v1.75.0)

- **Status:** design for the owner's decision (1), "Sim-1.0 plus a shared step panel, #53/#54". This document is read-only analysis. The dated spec and plan it feeds go in the cross-repo bundle.
- **Sources read:**
  - LibKa0s master `d9f9454`: `CLAUDE.md`, `LibKa0s.xml`, `Perf.lua` (`New`, `tr`, no-panel fallbacks), `PerfPanel.lua` (whole file), the `Widgets.lua` and `WidgetsLineChart.lua` headers, the `Lifecycle.lua` header, `tests/majors.lua`, `docs/api/README.md`, and the `tests/test_perf_panel.lua` reaches.
  - WowAddonStandards `library-stack.md` §7: the floors, "MUST NOT feature-detect", the attach-file floors, and promotion bars 1-3.
  - `analysis.json` c53/c54 challenges.
  - The DW reference, the LH requirements and the BL requirements given in the task.
  - A grep of DW's provider tables: no key is registered twice across `Sim.lua`, `SimEvents.lua` and `SimWorld.lua`.

---

## 0. Decisions in one page

| # | Decision | Why |
|---|---|---|
| D1 | **One new major, `LibKa0s-Sim-1.0`, in three files.** `Sim.lua` is the shell: seam, session, Fire, timers, stop. `SimTimeline.lua` holds the step machine and verbs. `SimPanel.lua` holds the panel adapter. Both secondary files are paired on the shell's minor, the way Perf's files are. Version key `<Sim>.<SimTimeline>.<SimPanel>` = `1.1.1`. | All three hosts use all three layers with the same semantics. The verbs ride with the timeline because every verb drives it. A fourth file would only add one more pairing guard. |
| D2 | **Two constructors, matching the two real lifetimes.** `Sim:NewSeam(compat, opts)` runs at file load, right after the host's Compat file. `Sim:New(d)` runs when the host's Sim module loads and binds that seam. | The seam has to wrap before any file can read Compat. Everything else (scenarios, play, refusal) is defined later. One `New` at load would force every descriptor field to be a call-time closure. Both LH and BL already assume `NewSeam` plus a session. |
| D3 | **`W.StepPanel` is public, in a new `LibKa0s/WidgetsStepPanel.lua`** paired on the Widgets shell's minor. | Two majors consume it (Sim, and Perf after the rebuild). The new v2.86.0 §7 rule "`__` internals are not contract" forbids one major reaching another's private file. The challenger's "Sim-private" cut assumed PerfPanel would not be rebuilt; the owner prefers the rebuild. |
| D4 | **PerfPanel is rebuilt on `W.StepPanel` (PANEL_MINOR 6 → 7), as the last library commit.** The unchanged `tests/test_perf_panel.lua` (634 lines) is the proof that the look did not change. If any assertion needs editing, drop the commit and keep the in-library duplicate. | Cheap (about −100 lines) and safe, because the suite already pins every pixel-adjacent fact a host can see. |
| D5 | **The descriptor carries no behaviour flags (bar 2).** Every host difference is data (scenarios, steps, rows), a host callback with one meaning (`deliver`, `play`, `prepare`, `refusal`, `gate`), or a presentation argument (`check`, `tooltip`, `button`, `title`). Perf's `decorate` and resize do not enter StepPanel: resize is always on, and `decorate` stays Perf's own and is implemented in PerfPanel. | Owner's bar. |
| D6 | **Floors.** `Sim.lua` floors on Core 1. `SimPanel.lua` floors on Widgets with StepPanel (an attach-file floor, like Options' `NEEDS_POOL`), so a headless Sim (seam, session, timeline) is never lost to a missing panel. `WidgetsStepPanel.lua` floors on Core 9 (`MakeResizable`) instead of feature-detecting it. `PerfPanel.lua` gains an attach-file floor on Widgets plus StepPanel, so Perf's no-panel fallbacks answer when it is unmet. **No Lifecycle floor:** the host passes `isStoodDown`. | §7 "MUST NOT feature-detect a too-old dependency", and floors live in attach files where only the attach needs them. |
| D7 | **The library never touches SavedVariables.** The one exception is `point`, written into a host-supplied table (`panel.store()`) on drag. | Session-only stores are host code in all three (DW `History.LogFor`, LH's three stores, BL `Database:Sink`). The library cannot intercept a write, so it must not claim to. |
| D8 | **Step states stay at Perf's set: done, used, ready, busy, locked, cancel. No new state, ever.** The "ahead" rows are `locked` with `actionable = true`. | The step-state vocabulary is frozen with the major. |

---

## 1. Placement in the payload

- **`LibKa0s.xml`.**
  - Append `Sim.lua`, `SimTimeline.lua` and `SimPanel.lua` after `PerfPanel.lua`.
  - Add `WidgetsStepPanel.lua` to the Widgets block after the attach files the release already adds (W.SearchBox, W.TestStrip). The xml order of the new Widgets files fixes the composite key, so the release plan fixes it once, for all three new files.
- **`tests/majors.lua`.** Add the row:
  `{ major = "LibKa0s-Sim-1.0", files = {"Sim","SimTimeline","SimPanel"}, primary = "Sim", paired = { {file="SimTimeline", minorField="__timelineMinor", probeField="__timelineShellMinor"}, {file="SimPanel", minorField="__panelMinor", probeField="__panelShellMinor"} } }`.
  Add `WidgetsStepPanel` to the Widgets row with `__stepPanelMinor`/`__stepPanelShellMinor`.
- **Payload weight.** Whole-folder vendoring ships Sim into all 14 addons. Load cost is three file bodies that define functions and create no frame, timer or event registration until `NewSeam`/`New` is called. The 11 non-callers pay parse time only. Record this in the CHANGELOG, as the challenger asked.
- **Size budget** (all far under the 1500 cap; every function ≤ CCN 15):

  | File | Contents | Lines |
  |---|---|---|
  | `Sim.lua` | header, floors, STRINGS, NewSeam, New, session | ~480 |
  | `SimTimeline.lua` | step machine, verbs, status line | ~420 |
  | `SimPanel.lua` | compose, picker, controls, placement | ~330 |
  | `WidgetsStepPanel.lua` | the render-only widget | ~330 |

---

## 2. `LibKa0s-Sim-1.0`: the public API

### 2.1 Library table

| Member | Contract |
|---|---|
| `Sim.MAJOR`, `Sim.MINOR`, `Sim.MODULES` | As every major. `MODULES.Sim`, `.SimTimeline`, `.SimPanel`. |
| `Sim.STRINGS` | Built-in English. A host overrides any key through `d.L` read with `rawget` (Perf's `tr`, `Perf.lua:590-594`). Keys are listed in §2.6. |
| `Sim:NewSeam(compat, opts) -> seam` | §2.2 |
| `Sim:New(d) -> sim` | §2.3 |

### 2.2 The seam: `Sim:NewSeam(compat, opts)`

**Arguments:**
- `compat` (table, required). The host's own Compat table. It is wrapped in place, once, inside `NewSeam`.
- `opts.pure` (`{[key]=true}`). Never wrapped.
- `opts.guarded` (`{[key]=fn}`). The safe answer while a session is active (§2.2.2).
- `opts.name` (string, required). Used for errors and debug lines.

**Wrap rule.** Every member with `type == "function"` that is not in `pure` is replaced by a closure:

```lua
-- state is seam-private; the hot path reads one upvalue field
return function(...)
  if state.active and (g or not state.bypass) then return answer(key, live, g, ...) end
  return live(...)
end
```

`answer` calls the provider as `provider(fallback, ...)`, where `fallback = guarded[key] or live`. With no provider, it calls `fallback(...)`.

**Members:**

| Member | Contract |
|---|---|
| `seam:SetProvider(key, fn)` | Registers the provider for one wrapped key. `nil` removes it. **Raises** on a key that is not wrapped (pure or unknown, which is a typo caught at load). **Raises** when a second non-nil provider is set for a key that already has one: two owners of one answer is a bug. DW has no duplicate today; the grep found none. |
| `seam:Live(fn, ...) -> ...` | Runs `fn` with `bypass = true` and is nesting-safe. Ordinary members answer live, and guarded members still answer guarded. `bypass` is restored on every exit. An error is re-raised **with its original value** (`error(v, 0)`, so tables survive), and the traceback is written to the session's debug sink first. This fixes DW's dropped traceback. Nil holes in the returns survive (`select('#')`). |
| `seam:IsGuarded(key)` | `guarded[key] ~= nil` |
| `seam:IsActive()` | True while the bound session is active, including its guarded stop phase (§2.3.3). |
| `seam:Keys()` | Sorted wrapped keys. Used by diagnostics and by host coverage tests. |
| `seam:Unwrapped()` | Sorted keys of function members of `compat` that are neither pure nor still the recorded wrapper. Two cases show up here: a member added after `NewSeam`, and a member replaced by `rawset`/assignment. **A host suite MUST assert it is empty** (host contract H2). This replaces DW's comment-only guard. It is chosen over a `__newindex` metatable, which would add magic to the host's table and still miss replacements. |

#### 2.2.1 What the seam enforces

- **Idle cost.** One upvalue field test per wrapped call. BL measures this at about 3,200 per reconcile pass, which is negligible.
- **Bypass is always restored**, even when `fn` raises.
- **A guarded member never reaches the client while the session is active** (§2.2.2).

#### 2.2.2 Guarded members

- While the session is active, the guarded `fn` answers in place of the live member, inside `Live` included. A provider's first argument is the guarded `fn`, never the live member, so no provider can reach the client by mistake.
- While idle, guarded members call live.
- Guarded keys per host:

  | Host | Guarded keys |
  |---|---|
  | DW | `ChatSender`, `NotifyInspect`, `ClearInspectPlayer`, `InitiateTrade` |
  | LH | `ListCurrencies` |
  | BL | `QueryGuildBankTab` (its guarded fn schedules `sim:Fire("GUILDBANKBAGSLOTS_CHANGED")` through `sim:After(0.2, …)`) |

**One seam binds one session.** `Sim:New` raises if `d.seam` is already bound.

### 2.3 The session: `Sim:New(d)`

#### 2.3.1 Descriptor

| Field | Req. | Contract |
|---|---|---|
| `name` | yes | The addon folder. Used for frame names (`<name>SimPanel`), the close-mark folder and error text. |
| `seam` | yes | From `Sim:NewSeam`. |
| `slash` | yes | The typed prefix, for example `"/dw sim"`. Used in command columns, usage and lines. |
| `deliver` | yes | `fn(event, ...) -> n`. Calls exactly the handlers the client's registration would call for this event, in order, and answers how many ran. **Any string is legal** (LH `hook:<name>`, BL `GUILDBANK_FRAME_SHOWN`). The library `pcall`s each call to `deliver`; per-handler isolation is the host's. |
| `isStoodDown` | yes | `fn() -> bool`, read at call time. |
| `scenarios` | yes | `{ names = {ordered}, defs = { [name] = { label, sizes = {n,...}?, timeline = fn(def, opts) -> steps } } }`. `timeline` MUST be pure. A step is a host table with at least `kind`. The library adds `ranAt`, `detail` and `index`, and writes nothing else into a step. |
| `prepare` | yes | `fn(session, def, opts, ready)`. Builds the host's world and calls `ready()` exactly once, sync or async. Until then the timeline answers `building`. A second `ready()` call is ignored. |
| `play` | yes | `fn(step, session) -> detail?`. Drives one step's events through `sim:Fire`. It runs under `pcall`; an error pauses the run (§2.4). |
| `refusal` | no | `fn(opts) -> line|nil`. Run **inside `Live`**, after the library's "already running" check. It owns every host rule: stood-down wording, test mode, combat, instance, group, open frames, ledger settling, and per-scenario prerequisites (LH `trackLedger`). The library adds no world rule and relaxes none. |
| `gate` | no | `fn(session) -> open, line?`. Checked before every step: by `Step`, by `Run` ticks and by `RunTo`. Closed means "the host's world has not settled" (LH: Reconciler debounce, claim wait and hold; BL: pending lag timers and the settle window). With no gate, the gate is always open (DW). |
| `stepDelay` | no | A number, or `fn(step) -> seconds`: the pause after `step` before `Run` plays the next one. Default 2. It is read when each timer is set. DW passes its setting reader. BL passes `max(1.5, step.settle or 0)`. |
| `verbs` | no | `{ [verb] = { parse = fn(words) -> cmd|nil, run = fn(cmd, sim) -> ok, code } }`, the host's extra verbs. They need an active session unless `free = true`. |
| `why` | no | `{ [code] = line }`, lines for the host's verb failure codes. |
| `usage` | no | `{ lines }`, appended to the library usage. |
| `statusLine` | no | `fn(status, session) -> line|{lines}`, appended to the library status line. |
| `stopText` | no | `{ [reason] = line }`, stop lines for host reasons (`group`, `instance`, `world`, `combat`, `bank`, `profile`, `standDown`). |
| `L` | no | Locale table. Library STRINGS are overridable through `rawget`. |
| `print`, `debug` | no | `print(line)` and `debug(tag, fmt, ...)` with tag `SIM`. Read at call time. The defaults are `DEFAULT_CHAT_FRAME` and a no-op. |
| `panel` | no | §2.5. With no `panel`, `ShowPanel` and friends are no-ops. |

**Validation.** Missing required fields raise in `New` with the field name, following Perf's `required()`.

#### 2.3.2 Session members

| Member | Contract |
|---|---|
| `sim:Start(opts) -> ok, line` | `opts = {scenario, size?, seed?}`. Checks run in this order, and each refusal is printed and returned as `false, line`: (1) unknown scenario gives the `UNKNOWN_SCENARIO` line plus the names; (2) already running; (3) `refusal(opts)` inside `Live`; (4) backstop: `isStoodDown()` gives `STOOD_DOWN`. Then it creates the session `{sim=true, scenario, size, seed, startedAt=time(), events=0}`, sets the seam active, prints `STARTED`, calls `prepare` under `pcall` (an error becomes `Stop("error")`) and notifies listeners. `size` reaches `prepare` only when `def.sizes` exists; `0` means random. `seed` defaults to a time-derived integer. |
| `sim:Stop(reason) -> bool` | §2.3.3. Answers whether a session was running. `reason` defaults to `"stop"`. |
| `sim:IsActive()` | True from Start to the end of the guarded stop phase. **There is no public `active` field.** DW's eight direct reads of `Sim.active`/`Sim.delivering` become calls. |
| `sim:IsDelivering()` | True only inside `Fire` and nesting-safe. Hosts use it to tell a simulated input from a real one (DW `LootFeed`, LH `NS.Deliver`). |
| `sim:Session()` | The live session table or nil. Library fields are read-only by convention. **Host fields go on the same table**, which is the host bag (DW `world`/`members`/`log`, LH `stores`, BL `chars`/`world`). Timers and timeline internals are not on it. |
| `sim:Fire(event, ...) -> n` | Answers 0 unless the session is active, not stopping and not stood down. If `isStoodDown()` is true while a session is active, Fire first calls `Stop("standDown")`, which is the library's self-stop backstop. Otherwise it increments `events`, writes a debug line, sets `delivering`, `pcall`s `deliver(event, ...)` and restores `delivering`. On an error it writes a debug line and answers 0. |
| `sim:After(delay, fn) -> handle|nil` | A session timer that answers nil while idle. It fires only while the same session is live, under `pcall`. `handle:Cancel()` cancels the timer **and forgets it**, fixing DW's `SimScenario.lua:225` reach-in. Every live handle is cancelled at stop. |
| `sim:Live(fn, ...)` | Shorthand for `seam:Live`. |
| `sim:OnStopGuarded(fn)` | Registers `fn(session)` to run at stop **while the seam still answers** (DW `Asks.CancelQueued`, BL `L:DropContext`). Registration is permanent and ordered, normally at file load. |
| `sim:OnStop(fn)` | Registers `fn(session, reason)` to run at stop **after the seam is off** (DW engine steps, LH store release and drift `LoginScan`, BL `simLog` release). Permanent and ordered. |
| `sim:DeliverForCleanup(event, ...) -> n` | Delivers through `deliver` **only during the OnStop phase** with the seam off, and answers 0 at any other time. DW uses it to undo the combat edge and bag items. |
| `sim:Status() -> t` | `{active, scenario, size, seed, startedAt, events, ready, pos, total, playing, paused, settling}`. Hosts merge their own fields for diagnostics. |

#### 2.3.3 Stop order

This order is what the library enforces. Each numbered step after (1) is `pcall`ed, so one failing step never skips the rest.

1. Cancel the run (`playing`, the gate poll) and every session timer.
2. Mark the session `stopping`. `IsActive()` stays true and the seam still answers, but `Fire` and `After` refuse.
3. Run the `OnStopGuarded` list.
4. Turn the seam off, clear the session and `delivering`, and enter the cleanup phase.
5. Run the `OnStop` list (`DeliverForCleanup` is legal here).
6. Leave the cleanup phase. Hide the panel if `isStoodDown()`; otherwise repaint it to the picker. Notify listeners.
7. Print `stopText[reason]` or the library line for `stop`, `restart` or `error`, or else `STOPPED_REASON` formatted with the reason. Write one debug line with the event count and the reason.

Reasons the library emits itself: `stop`, `restart`, `error` and `standDown` (the self-stop backstop only). All others come from the host.

### 2.4 Timeline and verbs (`SimTimeline.lua`)

#### Step machine members

| Member | Answers | Contract |
|---|---|---|
| `sim:Steps()` | the live list | Empty while idle. |
| `sim:Step()` | `step` or `nil, code` | Codes: `notRunning`, `building`, `done` or `settling`. `settling` comes when the gate is closed, and it prints the gate's line or `SETTLING`; the step does not advance. On success it advances `pos`, `pcall`s `play`, stamps `ranAt` and `detail`, prints `STEP_LINE`, and notifies listeners. If `play` errors, the step counts as run, its detail is `ERROR`, the run pauses, and `STEP_FAILED` is printed. |
| `sim:Run()` | `true` or `false, code` | Codes: `notRunning`, `building`, `playing` or `done`. Clears `paused` and plays to the end. Each tick checks the gate. When the gate is closed it re-polls after `GATE_POLL = 0.25` s without advancing; when it is open it runs `Step` and schedules the next tick after `stepDelay(step)`. At the end it prints `FINISHED` (formatted with `slash`) and notifies. `playing` is true from `Run` until finished, paused or stopped. |
| `sim:Pause()` | `true` or `false, code` | Code: `notPlaying`. |
| `sim:Resume()` | `true` or `false, code` | Code: `notPaused`. On success it calls `Run`. |
| `sim:Restart()` | `true` or `false, code` | Code: `notRunning`. `Stop("restart")`, then `Start{scenario, size}` with a fresh seed. A refusal is printed and the answer is `false, "refused"`. |
| `sim:RunTo(index)` | `true` or `false, code` | Plays every step up to and including `index` in order, **back to back** (no `stepDelay`), honouring the gate the same way `Run` does (polling while it is closed). It is synchronous when the gate is open throughout, which is DW's behaviour today. A step failure, or a `done`/`notRunning` answer, ends it. |
| `sim:AddListener(fn)` | — | `fn(sim)` runs under `pcall` on every transition: start, ready, step, run, pause, stop. Listeners are permanent. |

#### Verbs: `sim:RunVerb(line) -> ok, code`

`RunVerb` prints every result through `d.print`.

**The generic grammar:**

| Typed | Effect |
|---|---|
| (empty) | Status plus usage, and opens the panel |
| `start <name> [size]` | `Start` |
| `run` / `step` / `pause` / `resume` / `restart` / `stop` | the timeline control of the same name |
| `status` | status line |
| `panel` | toggles the panel |
| `help` | usage |

- After the generic verbs, the host's `verbs` are tried. Anything else prints usage.
- **Free verbs** (no session needed) are `status`, `help`, `start`, `panel` and the empty line. Every other verb, the host's included unless they are marked `free`, prints `NOT_RUNNING` when idle.
- A failure code prints its WHY line: the library's codes plus `d.why`. `refused` stays silent, because the refusal line has already printed.
- **The click path is the typed path.** Every panel action calls `RunVerb` (or `RunTo`, which prints the same per-step lines), so a click prints exactly what typing prints.
- **Host wiring is one Slash-1.0 row:** `{"sim", desc, function(rest) NS.Sim:RunVerb(rest) end}`. That keeps `sim` a feature verb, which the dispatcher refuses while the addon is disabled.

### 2.5 The panel (`SimPanel.lua`, on `W.StepPanel`)

#### Library-owned behaviour

- **Rows.** `Start`, then one row per step, then `Stop`. Rows are addressed **by index**, because keys repeat.
- **States and actionability:**

  | Row | State | Actionable |
  |---|---|---|
  | Timeline row before `pos` | done | no |
  | Timeline row at `pos` while playing or settling | busy | no |
  | Timeline row at `pos+1` | ready | yes |
  | Rows further ahead | locked | yes (click-ahead through `RunTo`) |
  | Any timeline row while not live, or before `ready` | locked | no |
  | Start row | ready when idle, busy until `ready`, then done | only when idle |
  | Stop row | cancel while running | only while running |

- **Command column.** `slash.." start "..name[ .." "..size]`, `slash.." step"` and `slash.." stop"`.
- **Tips.** A done row's tip adds `RAN_AGO`.
- **Footer.**
  - Idle: the **picker**. A scenario `W.Dropdown` built from `names`/`label`; a size `W.Dropdown` only when the chosen def has `sizes`, with `RANDOM` = 0; and Start.
  - Running: the **controls**. Run all, Pause or Resume (swapping), Restart and Stop.
- **Click.** Re-composes from the live model and re-checks the clicked index, so a stale row never acts.
- **Preview model while idle.** `timeline(def, opts)` of the picked scenario at `pos` 0, all rows locked.
- **Refresh and visibility.** Repaints on every listener notification. `ShowPanel` answers false and does nothing while stood down. The panel is hidden on a stand-down stop.
- **Placement.** A saved point in `panel.store().point` (written on drag stop only) always wins. Otherwise the panel docks to the right of `panel.anchorTo()`, or to its left if there is no room, or floats at CENTER +420 when neither fits, with `DOCK_GAP = 8`. It redocks the next time it is shown with no saved point. `ResetPanelPosition()` clears `point`.

#### Instance members

`ShowPanel()`, `HidePanel()`, `TogglePanel()`, `IsPanelShown()`, `RefreshPanel()`, `ResetPanelPosition()` and `PanelRows()`. `PanelRows()` is the pure composed list `{key, index, label, command, state, actionable, tip}`, published so that host suites assert rows without reaching `__` fields.

**Fallbacks.** `Sim.lua` installs no-op fallbacks for all of these and for `RunVerb`/timeline members (printing `NO_TIMELINE`), following Perf's no-panel pattern (`Perf.lua:970-978`). An attach file overwrites them.

#### `d.panel` fields (presentation only)

| Field | Default | DW / LH / BL |
|---|---|---|
| `title` (string or fn) | `name.." - Simulation"` | `"<Brand> - Simulation"` |
| `stepLabel(step, i, steps)` | `step.label or step.kind` | DW boss and loot labels; LH `Kill: Rookery Bat`; BL `Deposit 20 × Linen Cloth to Warband Bank` |
| `stepTip(step, i) -> {{left, right?}}` | none | what the step injects, plus what was recorded |
| `startTip`, `stopTip` (line lists) | none | host wording |
| `store() -> table` | none (no position saving) | DW `profile.simPanel`, LH the History window-state table, BL `settings.simPanel` |
| `anchorTo() -> frame|nil` | none | DW main window, LH History window, BL `B:GetWindow()` |
| `check` (texture path) | none (dot only) | `NS.Icon("confirm")`. The host resolves it, so no `LibKa0s icons:` declaration is needed. |
| `tooltip(owner, title, lines)` | GameTooltip with double lines | DW `AttachTooltip`/`TipMarks`; LH and BL may take the default |
| `button(parent, width, text, onClick) -> button` | a minimal Core-skinned button | DW `NS.Window.TextButton` (open question 1) |

### 2.6 STRINGS (all overridable)

`STARTED` ("Simulation started (%s)." — neutral; **it makes no "nothing is saved" claim**, because that guarantee is the host's, and each host overrides it with its own guarantee line), `STOPPED`, `STOPPED_RESTART`, `STOPPED_ERROR`, `STOPPED_REASON`, `ALREADY_RUNNING`, `STOOD_DOWN`, `UNKNOWN_SCENARIO`, `NOT_RUNNING`, `BUILDING`, `PLAYING`, `NOT_PLAYING`, `NOT_PAUSED`, `DONE`, `SETTLING`, `STEP_LINE` ("Simulation step %d of %d: %s."), `STEP_FAILED`, `FINISHED` ("Simulation finished: %s stop ends it."), `STATUS_IDLE`, `STATUS_RUNNING`, `USAGE_*`, `PANEL_START`, `PANEL_STOP`, `RUN_ALL`, `PAUSE`, `RESUME`, `RESTART`, `STOP`, `RANDOM`, `RAN_AGO`, `NO_TIMELINE`.

---

## 3. `W.StepPanel(d)`: the render-only widget (`WidgetsStepPanel.lua`)

**Floor.** An attach-file floor `NEEDS_CORE = 9` for `MakeResizable`; Core is 10 today. If it is unmet the file returns and `W.StepPanel` is absent. It is paired on the Widgets shell's minor.

**Descriptor:**

| Field | Req. | Contract |
|---|---|---|
| `name` | yes | Frame global name. |
| `addonName` | yes | Close-mark folder (the third `MakeCloseButton` argument, whose absence was Perf minor 3's bug). |
| `title` | yes | String or `fn()`, re-read on every Refresh. |
| `rows` | yes | `fn() -> {{key?, label, command, state, actionable, tip?}}`. `actionable` is explicit row data (nil means false). |
| `onClick` | yes | `fn(row, index)`, called only after `rows()` is re-read and `actionable` re-checked at that index. |
| `check` | no | Texture path for the done mark, drawn over a hidden dot and tinted with the state color. |
| `tooltip` | no | `fn(owner, row)` is called on enter when a row has `tip`. |
| `footer` | no | `{height, build(frame, api), paint(frame)}`. `paint` runs on every Refresh. |
| `close` | no | Default true. False leaves the corner to the caller (PerfPanel's `decorate` path). |
| `place` | no | `fn(frame)`, called on every Show. With none the panel sits at CENTER −320, set at build (Perf's spot). |
| `onDragStop` | no | `fn(frame)`, the hook for SimPanel's point save. |

**Answers** `{Frame(), Show(), Hide(), Toggle(), IsShown(), Refresh(), Buttons()}`.
- `Frame()` builds lazily and answers nil headless with no `CreateFrame`.
- `Buttons()` answers the row buttons by index.

**What the widget owns:**
- **Geometry.** ROW_W 360, ROW_H 22, GAP 4, DOT 8 at x 8, LABEL_X 26, CMD_PAD 10, TITLE_H 24, PAD 8.
- **Palette and colors.** Perf's palette and CMD_COLOR. The locked dot sits at alpha 0.35.
- **Hover.** An actionable row turns gold (1, 0.82, 0), except `cancel`, which turns (1, 0.45, 0.45). For Perf this is identical to today, because Perf's actionable states are exactly ready, used and cancel.
- **Height and rows.** Height = `TITLE_H + PAD*2 + n*(ROW_H+GAP)`, plus `footer.height + PAD` when there is a footer. It is recomputed on each Refresh. Rows are created on demand and hidden when the list shrinks.
- **Command text.** Repainted on every Refresh.
- **Frame chrome.** Title at TOP 0, −6. Close at TOPRIGHT −6, −3. BackdropTemplate, DIALOG strata, movable, clamped, left-drag, `core.ApplySkin`, and UISpecialFrames.
- **Resize.** Always width-only, through `core.MakeResizable`; rows stretch. On each Refresh the min/max height bounds are re-pinned to the computed height, so a growing row count never leaves empty space. *Verify against Core's `widthOnly` bound handling in the first commit's test.*
- **Test record.** `b.__label`, `b.__state`, `b.__command` and `b.__index`.

**What it does not do.** No state logic, no slash knowledge, no saved position. It is render-only, so both consumers own their semantics: the "same shape, not same semantics" concern from c53 is answered by putting the semantics in Perf and Sim, not in the widget.

---

## 4. PerfPanel rebuilt on StepPanel (yes, last library commit)

- **Version and floor.** `PANEL_MINOR = 7`. A new attach-file floor on Widgets plus `MODULES.WidgetsStepPanel >= 1`. If it is unmet, PerfPanel returns before `lib.__AttachPanel` exists, and Perf's no-panel fallbacks answer. The probe and the commands stay live.
- **Floor implication.** This is a fourth inter-module edge (Perf → Widgets, attach-borne like Options → Pool). It is a vendoring trigger, called out in the CHANGELOG. In practice it costs nothing, because the payload is whole-folder and this release re-vendors every consumer. The §7 sentence "exactly three second edges" is rewritten in v2.86.0 to list Perf → Widgets (attach), Sim → Widgets (attach) and Widgets-StepPanel → Core 9 (attach).
- **Kept byte for byte (public):**
  - `P.STEPS`, `P.PanelStateOf` and `P.PanelIsActionable`;
  - `P.ShowPanel`/`HidePanel`/`TogglePanel`/`IsPanelShown`/`RefreshPanel` and `P.__panel()`;
  - the `tr`-resolved labels;
  - CENTER −320, no check, no tooltip, no footer;
  - the pairing guard `__panelMinor`/`__panelProbeMinor`.
- **Kept for the suite.** `frame.buttons[key]` and `b.step`: PerfPanel fills both from `panel:Buttons()` after `Frame()`. `frame.title`. `frame.closeButton` (StepPanel exposes it).
- **`decorate`.** PerfPanel passes `close = not decorate`, calls `decorate(frame, {Show, Hide, Toggle, TITLE_H, PAD, ROW_W})` once after the first `Frame()`, and keeps the exclusivity the suite pins at `:445-527`.
- **Proof and fallback.** `tests/test_perf_panel.lua` and `test_perf_*` pass **unedited**. Any needed edit means the commit is dropped and the documented in-library duplicate stays. Nothing else depends on this commit.

---

## 5. Safety: what the library enforces, and what it only documents

| Property | Enforced by the library | Host obligation |
|---|---|---|
| A guarded member never reaches the client while active, including inside `Live` and providers | **yes** | classify the members correctly |
| The idle seam costs one field test | **yes** | — |
| No simulated event outside a live, not-stood-down session | **yes** (`Fire` answers 0, and self-stops on an observed stand-down) | call `Stop("standDown")` **first** in its stand-down steps (H6) |
| Timers die with the session; a cancel forgets its handle | **yes** | use `sim:After`, never a raw `C_Timer`, inside the sim |
| Stop runs guarded steps, then turns the seam off, then runs the rest, each step isolated | **yes** | put a step that must still see simulated answers in `OnStopGuarded` |
| `Live` restores bypass and keeps the error | **yes** | read the real world only through `Live` |
| Refusals are read against the real world | **yes** (`refusal` runs inside `Live`) | own every rule |
| Nothing escapes the wrap | **detected** (`Unwrapped()`) | assert it empty in a suite; create the seam straight after the Compat file (a TOC line commented LOAD-BEARING); never `local x = Compat.Member` |
| Saved data is untouched | **no** | session-only stores (DW `LogFor`, LH three stores plus `Reconciler.lua:489`, BL `Database:Sink`), and an invariant test |
| Nothing is sent or acted on | only for guarded keys | never call hooked client functions from sim files (LH static scan) |
| Reads made by LibKa0s majors (Env, Item) on the host's behalf | **no**, outside the seam | route through Compat what the sim must answer (LH C2 `Zone`/`PlayerMapID`) |
| Dispatch fidelity | **no** | `deliver` calls only registered handlers, in client order, skipping rejected events (DW: honour `NS.rejectedEvents`) |
| Real input mid-session | **no** | classify it: stop and deliver live (LH interference), stop first (BL real bank open, DW world rows first in the fan-out), or absorb |
| Test mode and simulation are exclusive | **no** | refuse each from the other |
| Marker | **no** (supplies `IsActive`) | preview-mode marker rule v2.86.0: title or TestStrip label, plus footer |

**Documented in the API doc.** Simulated delivery deliberately differs from a live dispatcher that rethrows the first error: an error in `deliver` is swallowed to a debug line so that a session survives a bad handler.

---

## 6. Host contract (MUSTs, in the API doc and in each host's spec)

- **H1.** Every client read the simulator answers, and every outward action, is a `NS.Compat` member read at call time.
- **H2.** `Sim:NewSeam` runs in a setup file loaded straight after the Compat files (a LOAD-BEARING TOC comment). A suite asserts `seam:Unwrapped()` is empty after the whole addon loads.
- **H3.** One `deliver` that reproduces the client's handler set and order for any event name the host fires, pseudo-events included.
- **H4.** Session-only storage for every SavedVariables write the capture path reaches, plus a byte-identical before/after test.
- **H5.** `refusal` covers stood-down, test mode and the world rules that apply to the host, and test mode refuses while a simulation runs.
- **H6.** `sim:Stop("standDown")` is the first stand-down step. A profile event (LH), combat (BL, LH) or a real frame (BL), where it applies, calls `Stop` with a host reason.
- **H7.** One Slash-1.0 feature-verb row, `sim`, calling `RunVerb`, which is refused while disabled. No launcher entry.
- **H8.** Preview-mode marker, diagnostics `sim` section and a `Sim` debug tag.
- **H9.** Degradation stub (§7) and a surface-parity case.
- **H10.** Panel position is window state (absent until dragged), listed in the host's window-state docs, and never a schema row.

---

## 7. Degradation stub (host side, when `LibStub("LibKa0s-Sim-1.0", true)` is nil)

The setup file wraps nothing and builds an **inert stub**:

- `IsActive`, `IsDelivering` and `IsPanelShown` answer false. `Fire` and `DeliverForCleanup` answer 0. `After` answers nil.
- `Start` answers `false, line`. `RunVerb` prints `"The simulator needs LibKa0s-Sim-1.0."` and answers `false, "absent"`. `Stop` answers false.
- `Live(fn, ...)` calls `fn(...)`, and `SetProvider` is a no-op.
- `OnStop`, `OnStopGuarded` and `AddListener` are no-ops. Panel members are no-ops. `Status` answers `{active=false}`. `Session` answers nil. `PanelRows` and `Steps` answer `{}`.

**Parity.** `Kit.assertSurfaceParity(stub, "LibKa0s-Sim-1.0")` against the **instance** surface, registered with `Kit.setSurfaceSource`, plus a seam-stub parity case. Hosts that read `IsActive`/`IsDelivering` on hot real-event paths (LH `NS.Deliver`, DW History) need those members unconditionally, so the stub is mandatory, not optional.

---

## 8. Headless tests (LibKa0s)

- **`test_sim_seam.lua`**
  - Every non-pure function is wrapped, and `Keys` are sorted.
  - An idle call goes straight to live.
  - Providers get the fallback.
  - A guarded member never reaches live while active, inside `Live` included, and calls live when idle.
  - `SetProvider` raises on an unwrapped key and on a second owner; `nil` releases.
  - `Live` restores bypass when it raises, re-raises the original value (a table survives) and keeps nil holes.
  - `Unwrapped` lists a late-added member and a replaced member.
  - A second `New` on one seam raises.
- **`test_sim_session.lua`**
  - Refusal order; refusal runs inside `Live`; the stood-down backstop.
  - `Start` prints and creates the session; `size` is passed only with `sizes`.
  - `Fire` answers 0 when idle, stood down or stopping; a stand-down self-stops; `deliver` errors are isolated; nested Fire restores `delivering`.
  - `After` fires only within its session; `Cancel` forgets.
  - Stop order is guarded → off → cleanup, each step pcalled, with `DeliverForCleanup` legal only in the cleanup phase.
  - Reason lines, host `stopText` and STRINGS overrides through `rawget` (the locale fallback trap).
- **`test_sim_timeline.lua`**
  - Step codes: `building` until `ready()`, a second `ready` ignored, `done`.
  - The gate's `settling` line, without advancing.
  - `Run` with the kit clock: delay per step through `fn(step)`, and the gate poll.
  - `Pause` with no orphan timer, `Resume`, and `Restart` with a fresh seed.
  - `RunTo` is synchronous with an open gate and waits on a closed gate.
  - A `play` error pauses the run and prints `STEP_FAILED`.
  - Listeners fire on every transition.
- **`test_sim_verbs.lua`**
  - The full grammar, free verbs, host verbs and WHY lines; `refused` is silent; usage on unknown input.
  - Click path equals typed path (the same printed lines).
- **`test_sim_panel.lua`**
  - `PanelRows` states for idle, building, mid-run, done and stopping; ahead rows are locked and actionable.
  - Click-ahead runs `RunTo`; a stale click re-composes and refuses.
  - The picker shows the size dropdown only with `sizes`; the controls swap Pause and Resume.
  - Placement: saved point beats dock beats float; the point is written only on drag; `ResetPanelPosition`.
  - `Show` refused while stood down; hidden on a stand-down stop.
  - No-panel and no-timeline fallbacks.
- **`test_widgets_step_panel.lua`**
  - Geometry and palette constants, and the test record.
  - Hover for an actionable row (including cancel) and no hover for a non-actionable row.
  - Height with and without a footer, and shrink hiding rows.
  - `onClick` re-check; `close=false` draws no close mark; the close mark gets `addonName`; width-only resize re-pins height; headless `Frame()` answers nil.
- **Unchanged and green:** `test_perf_panel.lua` and the other `test_perf_*` suites (the PerfPanel proof).
- **Updated:**
  - `test_versioning.lua` through the majors row and members manifests;
  - `test_loader.lua` for xml order;
  - the kit-sync and inventory suites, if they count files.

No kit change is needed for Sim. Kit 41 is the runner-crash revision only.

---

## 9. Docs (LibKa0s and the standard)

**LibKa0s:**
- `docs/api/Sim/version-1.1.1-docs.md` plus `members-1.1.1.json`. The document covers:
  - the full contract above and the host contract H1-H10;
  - the enforce/obligate table (§5);
  - the stub shape and the error-swallowing delivery note;
  - "STARTED makes no saved-data claim".
- New Widgets key document and manifest (StepPanel plus the release's SearchBox and TestStrip), and Perf `version-15.1.1.7-docs.md`.
- `docs/api/README.md` key table row for Sim.
- `CONSUMERS.md` re-run after the hosts adopt.
- `CHANGELOG` v1.75.0: the new major, the StepPanel member, PerfPanel 7, the Perf → Widgets attach floor as a re-vendor trigger, and the payload-weight note.
- `CLAUDE.md` file-size list and doc map. `README.md` major list. `DEPENDENCIES.md` if it lists majors.

**Standard v2.86.0 (§7):**
- Module table rows for Sim-1.0 (with the host half spelled out: stores, refusals, deliver and marker stay per addon) and for `W.StepPanel` in the Widgets row.
- The edge sentence rewritten.
- The majors count, coordinated with Glow-1.0: seventeen majors.
- "`__` internals are not contract", already in the decision list.
- The preview-mode marker rule names a simulation as a preview mode.
- c53/c54 re-check triggers retired.

---

## 10. Drop Watcher migration (proves the contract)

**Replace and delete:**
- `core/SimSeam.lua` becomes **`core/SimSetup.lua`** in the same TOC slot. It calls `Sim:NewSeam(NS.Compat, {pure=PURE, guarded=GUARDED, name="DropWatcher"})` and keeps DW's PURE list, its GUARDED closures and their `counts` (sends, hand-overs) as host code. It carries the stub when Sim is absent.
- **Deleted from `modules/Sim.lua`:**
  - `IsActive`/`Session`, `deliver`, `IsDelivering`, `Fire`, `After`, `DeliverForCleanup`, `AddCleanup` and the generic `Start`/`Stop` (`:64-73`, `:145-218`, `:278-376`).
- **Kept in `modules/Sim.lua`** as `Sim:New` descriptor wiring:
  - the refusal, the restriction and lockdown model with its providers, MarkGUID and HistoryLog;
  - the engine steps, as `OnStop` registrations in today's order;
  - `Asks.CancelQueued` as `OnStopGuarded`;
  - the auto-stop rows, which stay **first** in the fan-out and call `sim:Live(readWorld)` then `sim:Stop(reason)`.
- **Moved:** `deliver` moves beside the live dispatcher in `core/DropWatcher.lua` and gains the `NS.rejectedEvents` skip.
- **Rewired:** the stand-down step calls `sim:Stop("standDown")` (still first in `NS.STAND_DOWN`).
- **`SimScenario.lua`.** Delete the step machine (`:117-283`, `:329-340`). Keep SCENARIOS, Timeline (as `defs[name].timeline`), PLAY (as `play`), `ready` (as `prepare`) and the `stepDelay` setting reader. The finished line comes from the library, with `slash`.
- **`SimVerbs.lua`.** Keep only pull, kill, loot, lockdown and trade as `verbs`, plus their WHY codes, usage lines and `StatusLine`. Delete Parse, Run and FREE.
- **`SimPanel.lua`.** Shrinks to the `panel` fields: stepLabel (boss names, loot report), stepTip, start and stop tips, `store = profile.simPanel`, `anchorTo = NS.Window` frame, `check`, `tooltip`, `button`. Delete the frame, Compose, Controls, RunTo and ClickRow.
- **Call sites.** Change the eight direct `Sim.active`/`Sim.delivering` reads to `NS.Sim:IsActive()`/`:IsDelivering()` (`core/DropWatcher.lua:130`, `History.lua:413,424,535,636`, `LootFeed.lua:578-580`, `Situations.lua:180`, `WindowTitleBar.lua:343`).
- **Docs.** Delete the `docs/ARCHITECTURE.md:301` SimPanel deviation row. Update the module map and the compat-layer note (`Unwrapped` test).
- **Tests.**
  - Generic cases move to the library (seam, fire isolation, timers, stop isolation, step machine, parse, panel rows).
  - DW keeps the integration suites: e2e, history, auto-stop, restrictions, the seam-only scan.
  - DW adds `assert #seam:Unwrapped() == 0` and a stub parity case.
- **Acceptance.** Every remaining DW suite passes, with assertion edits confined to the moved and deleted tests. Smoke SIM theme: owed again, owner-run.

---

## 11. How LootHistory and BankLedger build on it

Both re-vendor v1.75.0 first. Their prerequisite refactors are host work and land before any Sim file.

**LootHistory:**

| Need | Maps to |
|---|---|
| prerequisite refactors | C1-C5 Compat routing; `core/Dispatch.lua` with EVENT_ROWS and HOOK_ROWS; ResetState/ResetContexts; `CancelDeferral(h)`; store accessors |
| `core/SimSeam.lua` | `Sim:NewSeam(NS.Compat, {pure, guarded={ListCurrencies=…}})` straight after `core/Compat.lua` |
| `deliver` | walks `NS.EVENT_ROWS` (registered rows only), and `NS.HOOK_ROWS` for `hook:<name>` |
| `gate` | ledger settled: no `R._pending`, no `_holdSince`, no `deferred` |
| `refusal` | §5.1 items 1, 3-10 (the library does "already running") |
| `OnStop` | context and Reconciler reset, store release, world-watch unregister, drift `LoginScan` unless standDown, dataset events, marker off |
| `NS.Deliver` real-event split | reads `NS.Sim:IsActive()` and `:IsDelivering()` |
| extra verb | `loot [n]` |
| panel | `anchorTo` = History window; `store` = its window-state table |

The six scenarios are `defs`.

**BankLedger:**

| Need | Maps to |
|---|---|
| prerequisite refactors | R1-R9: `L.HANDLERS` plus `L:Dispatch`; `Compat.PlayerName`/`PlayerClass`; `Database:Sink`; `DatasetKind`; the stop hooks |
| `core/SimSetup.lua` | `Sim:NewSeam(NS.Compat, {pure={GuildBankTabSize,GetItemDetails,ItemNameQuality}, guarded={QueryGuildBankTab=…}})` straight after `core/Compat.lua` |
| `deliver` | one lookup into `L.HANDLERS` (one handler per event), pseudo-events `GUILDBANK_FRAME_SHOWN`/`HIDDEN` included |
| `OnStopGuarded` | `L:DropContext()`, with **no Reconcile** |
| `OnStop` | release `simLog`, `Browser:OnDatasetChanged`, strip off |
| `stepDelay` | `fn(step) return math.max(1.5, step.settle or 0) end` |
| `gate` | no pending lag timer and no held baseline. This lets click-ahead (`RunTo`) wait correctly; `settle` alone only paces `Run`. |
| `refusal` | §6 items 1, 3-6 |
| auto-stop | `L:Dispatch` calls `sim:Stop("bank")` for a real open or close not delivered by `Fire` (`not sim:IsDelivering()`); `OnCombatChanged` calls `Stop("combat")` |
| panel | `anchorTo` = ledger window; `store` = `settings.simPanel` |

No extra verbs. Four scenario `defs`.

**Same semantics across the three hosts:**
- seam (pure, guarded, provider, Live);
- one deliver callback for any event name;
- session with refusal-in-Live and a two-phase stop;
- the timeline with an optional gate and per-step delay;
- verbs through `RunVerb` and one slash row;
- a panel docked beside the main window.

No host needs a flag that changes what a library function does.

---

## 12. Order of work

1. **LibKa0s, on the release branch**, one commit per item, gate green after each:
   1. `WidgetsStepPanel.lua` and its suite.
   2. `Sim.lua` (seam and session) and its suites.
   3. `SimTimeline.lua` and its suites.
   4. `SimPanel.lua` and its suite.
   5. docs/api, manifests, CHANGELOG, majors and xml rows.
   6. **Last:** the PerfPanel 7 rebuild. It is dropped if `test_perf_panel.lua` needs any edit.
2. **Standard v2.86.0 §7 edits**, alongside the release.
3. **Tag v1.75.0** (owner go-ahead).
4. **DropWatcher migration** (§10) on the cross-repo feature branch. It must pass unchanged integration suites; this is the contract proof. A gap found here is fixed **upstream before the tag** if the tag has not shipped, or else in an additive minor. Never patch `libs/`.
5. **LootHistory**: re-vendor, refactors, then the simulator, per its requirements §12.
6. **BankLedger**: R0-R9, then the simulator.
7. **Close-out.** Smoke SIM themes are recorded as owed in each repo (never marked passed by an agent), and `CONSUMERS.md` is re-run.

**Sequencing caveat.** DW proves the contract only after the library is written. To keep "tag once" honest, hold the v1.75.0 tag until the DW migration branch is green against the release-branch payload (vendored from the branch head for the check only, then re-vendored from the tag).
