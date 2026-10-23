# Design: simulator auto-run (OWNER_SCOPE A.1, C.1)

- **Status:** design note for the run's spec. Read-only analysis; nothing was edited in any repo.
- **Items:** LK-01, WS-01, DW-01, BL-01, LH-01.
- **Sources read** (all on the default branch, 2026-10-23):
  - LibKa0s `99fb662`: `LibKa0s/SimTimeline.lua` (whole file), `LibKa0s/SimPanel.lua` (header, STRINGS, the
    adapter, `act`, `buildControls`, `paintControls`, `footer`), `LibKa0s/Sim.lua` (`readyFor`, `Start`, `Stop`,
    `newCtx`, `New`), `tests/test_sim_timeline.lua`, `tests/test_sim_panel.lua` (the controls cases),
    `tests/run.lua`, `docs/releasing.md` steps 2 to 6, `docs/api/Sim/version-2.2.4-docs.md`, `members-2.2.4.json`.
  - DropWatcher `e017d26`, BankLedger `8b93492`, LootHistory `ceb76a0`: their `modules/Sim*.lua`, settings rows,
    locales, sim suites and sim support files, and every live doc that names `Run all` or `/xx sim run`.
  - WowAddonStandards `db00f05`: `standards/standards/preview-mode.md` (*The in-game simulator*),
    `library-stack.md` (the Sim row), `AUDIT.md` (the simulator sub-check), `STANDARDS.md`.
  - The previous run's `inputs/design-sim.md` (Sim-1.0's design) for the idioms.

---

## 1. Current state, with evidence

### 1.1 The library

- **A session never plays on its own.** `Sim.lua:548-565` (`sim.Start`) creates the session, runs `prepare`, and
  notifies. Nothing in `SimTimeline.lua` reacts to `ready()`: `readyFor` (`Sim.lua:527-534`) sets `S.ready` and
  calls `notify`. Play starts only from `Run()` (`SimTimeline.lua:335-344`), `Step()` (`:328-330`) or the panel's
  click-ahead `runTo` (`:305-317`).
- **The panel's controls** (`SimPanel.lua:712-727`, `buildControls`) are four `BUTTON_W = 84` buttons at
  `(i-1) * (84 + 6)`: `run` (`RUN_ALL`), `pause`, `restart`, `stop`. `paintControls` (`:746-762`) enables `run`
  while steps are left and nothing plays, and swaps `pause` to `RESUME` (verb `resume`) while `st.paused`.
  `RUN_ALL = "Run all"` is a `Sim.STRINGS` key (`:90`).
- **Clicking a row** (`act`, `SimPanel.lua:592-605`): the row at `pos + 1` runs the typed `step`; a row further
  ahead calls `ctx.runTo(index)`, which answers `false, "playing"` while a run plays (`SimTimeline.lua:309`) and
  prints `PLAYING`. So today a click ahead does nothing while Run all plays, and a click on the next row plays a
  step **beside** the run: `stepOnce` never looks at `R.playing`, so the run's pending tick then plays the step
  after it as well.
- **The "waiting" state.** After a RunTo finishes (`runToPass`, `:298-301`) and after a manual `Step` the run is
  neither playing nor paused. Today only Run all continues from there; `Pause/Resume` is disabled (it is enabled
  only while `playing`, or as Resume while `paused`).
- **`Resume` while building** clears `paused` before `Run` answers `building` (`:355-360`), so a refused Resume
  loses the paused flag. Small, and fixed in passing.
- **Verbs** (`runVerb`, `:526-551`): `start` (`verbStart`, `:484-489`) and the six controls; `run` is `Run`.
  `RunVerb` is a closure over `ctx` only; the step machine `T` is not reachable from the verb functions.
- **The testkit** mocks no part of Sim (grep of `testkit/` for the panel and the verbs: none). The kit's clock is
  manual: `m.__fireTimers()` runs what is pending.

### 1.2 The hosts

Three hosts use the major: DropWatcher, LootHistory, BankLedger. WhatGroup only lists the three vendored Sim files
in its test loader (`WhatGroup/tests/loader.lua:87-91`), and PGFE and the other addons have no simulator.
**No host overrides `RUN_ALL`** (grep of every host's `locales/` and `modules/` for `RUN_ALL`: none).

What the hosts' code and docs say about Run all:

| Host | Player-visible strings | Comments | Docs |
|---|---|---|---|
| DW | `locales/enUS.lua:225` ready line (`... /dw sim run plays it, /dw sim step one event at a time.`, printed by `modules/SimScenario.lua:191`); `:228` the step-delay tooltip (`automatic run (Run all, \`/dw sim run\`)`), used at `settings/SchemaRows.lua:567` | `modules/SimScenario.lua:3`, `settings/SchemaRows.lua:561` | `docs/data-flow.md:331`, `docs/settings-panel.md:67`, `docs/schema.md:67`, `docs/smoke-tests.md` (lines 658, 674, 694, 743, 2344, 2356, 2403, 2415-2419, 2455-2458, 2492, 2505, 2551), `docs/test-cases.md` (generated) |
| BL | `settings/Schema.lua:124` the step-delay tooltip (`the simulator's Run all (and /bl sim run)`) | `core/Constants.lua:171`, `defaults/Profile.lua:68`, `settings/Schema.lua:114-115` | `README.md:91`, `docs/settings-panel.md:20, 270-271`, `docs/smoke-tests.md:850, 912-914` |
| LH | `settings/Schema.lua:417` the step-delay tooltip | `settings/Schema.lua:407`, `defaults/Profile.lua:52`, `modules/Sim.lua:58, 75` | `README.md:61`, `docs/ARCHITECTURE.md:507`, `docs/settings-panel.md:65`, `docs/schema.md:266`, `docs/smoke-tests.md:1661, 1698-1699` |

LootHistory's `docs/testing.md:146` ("Run all four") and `docs/smoke-tests.md:1274` ("Run all four ways") are
not about the simulator and stay.

How the hosts' suites drive a session:

- **Through the member `sim:Start{}`** (unaffected by this design): BankLedger's `tests/sim_support.lua:144-160`
  (`withSession`) and `:111` (`runToEnd` calls `sim:Run()`); LootHistory's `tests/sim_support.lua:147-175`
  (`H.run`, `playByRun`, `playByStep`) and `tests/test_sim_panel.lua:83-86` (`start`); DropWatcher's
  `tests/test_sim_e2e.lua` and the `NS.SimScenario.Start` cases.
- **Through the typed verb or the panel** (affected): DropWatcher `tests/test_sim_scenario.lua` (the `/dw sim`
  cases at 236-262, 265-282, 336-360, 377-387, 409-422, 424-447, 488-497) and `tests/test_sim_panel.lua:171-196`;
  LootHistory `tests/test_sim_slash.lua:69-95` and `tests/test_sim_panel.lua:220-240` (the controls case reads
  `c.run`); BankLedger `tests/test_slash.lua:833` (the usage line) only.

### 1.3 The standard

No section names Run all or the panel's controls. `preview-mode.md:32` (*The in-game simulator*, the reference
implementation) says the panel "shows the scenario's steps while it runs"; `library-stack.md:99` (the Sim row)
lists the timeline's verbs "(step, run, pause, resume, restart; `RunTo` is Sim-internal)". `AUDIT.md:948-959`
(the simulator sub-check) does not touch play. Both prose sites stay true after this change, but neither says a
session plays on its own, which is now the behavior every host has; WS-01 adds that one fact.

---

## 2. The design

### 2.1 Decisions

| # | Decision | Why |
|---|---|---|
| A1 | **Auto-play is a library default with no new public member, no descriptor field and no Start option.** | The owner wants it for every host. Library-stack-§7 bar 2 (no behavior flags) rules out an opt-out field. |
| A2 | **The verb layer plays, the member layer does not.** `RunVerb("start …")` and `RunVerb("restart")` arm the run. The picker's Start and the controls' Restart reach it because they call `RunVerb`. The members `sim:Start(opts)` and `sim:Restart()` are unchanged: they start a session and play nothing. | Every player entry point (the typed verb, the picker, the Restart button) goes through `RunVerb`, which is what *the click path is the typed path* already guarantees, so the owner gets auto-play everywhere. The members are the scripting layer that host suites and host code drive (`withSession`, `H.run`, `SimScenario.Start`), and keeping them literal leaves dozens of deterministic host cases untouched. No host's runtime code starts a session through the member (grep: `NS.SimScenario.Start` has no caller outside DW's tests). |
| A3 | **"Armed" means `playing`.** Arming sets `R.playing = true` at once, even while the world is still building. The first tick is scheduled through `sim:After(0, …)` once `ready()` has fired: immediately if it already has, else from the timeline's own listener when `ready()` notifies. Every later tick waits `stepDelay(step)`, as Run does today. | A deferred first tick never plays a step inside the host's `prepare` (a synchronous `ready()` fires inside `Start`) or inside a listener loop. In the client, `After(0)` is the next frame, which reads as "straight away". With `playing` true during building, `Pause` works before the first step and the panel's Pause is enabled at once. No new `Status()` field is needed. |
| A4 | **The ready hook is a listener the timeline registers on itself at attach**, `sim:AddListener(kick)`, not a change to `Sim.lua`. | It needs no new handshake field and no shell minor (Sim.lua stays 2). The key moves only in its second and third numbers. `readyFor` already notifies exactly once per session. |
| A5 | **A manual act takes over a playing run.** `Step()` (typed `step`, or a click on the next row) and the click-ahead `runTo` first **hold** a playing run: they cancel its pending tick or poll, and set `playing = false` and `paused = true`. Then they act. A hold happens only when the act can proceed past `blocked()` (not `notRunning`, `building` or `done`); a `step` refused as `building` leaves an armed run armed. | The owner: "can still manually pause and click on every step individually". Today a click on the next row double-plays (it plays one step and the run's tick plays the next), and a click ahead is refused with `PLAYING`. Pause-then-act is the only reading under which a click does exactly what its row says. Resuming after the act would replay the old race, so the run stays held until Resume. |
| A6 | **A manual act leaves the run paused while steps remain.** After `Step()` plays or settles, and after a click-ahead ends short of the last step, `paused = true`. | The panel then always offers **Resume** after a manual act. That replaces the only job Run all had left, continuing from the "waiting" state. |
| A7 | **Run all goes. The controls are Pause/Resume, Restart and Stop: three equal buttons spanning the bar.** `CONTROL_W = floor((ROW_W - 2 * BUTTON_GAP) / 3)`, which is 116, at x = 0, 122 and 244. The picker's Start keeps `BUTTON_W`. | Three buttons in a row of 360 at 84 each would leave a 96-pixel hole on the right; spanning the bar keeps the footer as wide as the rows. |
| A8 | **The Pause/Resume button.** While `playing`: label `PAUSE`, verb `pause`, enabled. Otherwise: label `RESUME`, enabled while the world is ready and steps remain. Its verb is `resume` when `paused`, else `run`, and the tooltip's typed command follows the verb. | A session started through the member (a host script, or a future host button) is neither playing nor paused, and without Run all only this button can start it. Sending `run` there keeps one button for both cases. |
| A9 | **`run` stays as a verb and as `sim:Run()`**: the synonym of resume, and still the way to play a member-started session. Its usage line becomes `"%s run: play the remaining steps (the same as resume)."`. `USAGE_START` becomes `"%s start <scenario> [size]: start a simulation. It plays at once; pause it to step by hand."`. | The second sentence keeps the substring `start a simulation.` that four host assertions match with `find` (`BankLedger/tests/test_slash.lua:833`, `LootHistory/tests/test_sim_slash.lua:63, 141`, `DropWatcher/tests/test_sim_scenario.lua:141, 160`), so the usage change costs them nothing. |
| A10 | **`RUN_ALL` leaves `Sim.STRINGS`.** | It would be a dead key. No host overrides it (grep), and `STRINGS` keys are presentation, not a member (`members-2.2.4.json` lists only `New`, `NewSeam`, `STRINGS`). |
| A11 | **`Resume()` checks `blocked()` before it clears `paused`.** | This fixes 1.1's lost paused flag, which otherwise becomes visible on a panel whose only continue control is Resume. |
| A12 | **Host verbs (`/dw sim pull`, `/lh sim loot`, …) do not hold the run.** | They inject beside the timeline; they are not steps. The usage tells a player who wants a quiet timeline to pause first. Recorded as a risk. |

### 2.2 The step machine (`SimTimeline.lua`, minor 2 → 3)

The R record gains `awaiting` (armed before ready). The new file-local helpers are:

```lua
--- Hold a playing run (a Run, an armed run or a RunTo): no tick, not playing, paused.
local function hold(T, R)
  cancelTimer(R)
  R.playing, R.paused, R.settling, R.awaiting, R.target = false, true, false, false, nil
  T.ctx.notify()
end

--- Schedule an armed run's first tick once the world is ready (After(0): never inside prepare).
local function kick(T, R)
  if not (R and R.awaiting and R.playing and live(T, R) and T.ctx.ready()) then return end
  R.awaiting = false
  schedule(T, R, 0, tick)
end

--- Arm the live session's run: playing from now, its first step on the frame after ready().
local function arm(T)
  local R = current(T)
  if not R then return end
  R.paused, R.playing, R.target, R.awaiting = false, true, nil, true
  T.ctx.notify()
  kick(T, R)
end
```

- `__AttachTimeline` registers `sim:AddListener(function() kick(T, T.R) end)` before it returns. That listener
  is the first one registered, so it runs before the panel's and the host's.
- `verbStart` arms after `sim:Start` answers true. `verbControl` arms after `sim:Restart()` answers true. `runVerb`
  and its helpers take `T` (it carries `sim` and `ctx`), and `sim.RunVerb` becomes
  `function(_, line) return runVerb(T, line) end`.
- `sim.Step`: `local R = current(T); if R and R.playing and not blocked(T, R) then hold(T, R) end`, then
  `stepOnce(T, R, true)`, then `if R and live(T, R) and not R.playing and R.pos < #R.steps and T.ctx.ready() then
  R.paused = true end`.
- `runTo`: drop `if R.playing then return false, "playing" end` and hold instead. When `runToPass` ends live,
  short of `#R.steps` and not failed, set `paused = true`.
- `Run` is unchanged, so `Run` during a pending RunTo poll still answers `playing` (C.2). A second click-ahead
  holds the first and retargets.
- `Pause`: also clears `awaiting`. While armed and building it answers true, and no first tick is ever scheduled.
- `Resume`: `blocked()` first (A11), then `paused = false`, then `Run`.
- `finish`: also clears `paused` and `awaiting`.
- `Status()`: `playing` is true from a verb start until the run finishes, pauses or stops, **including the
  building phase**. `stateWord` already reports `building` first, so the status line is unchanged while building.

### 2.3 The panel (`SimPanel.lua`, minor 4 → 5)

- `buildControls`: the list is `{ "pause", "PAUSE" }, { "restart", "RESTART" }, { "stop", "STOP" }` at `CONTROL_W`.
  `verbOf("pause")` returns `c.pause.__verb`.
- `paintControls`: `left = st.ready and pos < total`. While `st.playing`: verb `pause`, label `PAUSE`, enabled.
  Otherwise: label `RESUME`, verb `st.paused and "resume" or "run"`, enabled iff `left`. Restart and Stop stay
  enabled.
- `act` is unchanged. Its click on the next row is the typed `step` (which now holds), and its click ahead is
  `ctx.runTo` (which now holds). The `WHY.playing` entry stays for a stale double click inside the same frame.
- STRINGS: drop `RUN_ALL`.
- The header comment's *WHAT THE ADAPTER OWNS* gains one sentence: a click while the run plays holds it first.

### 2.4 Versions and documents

- **Sim key 2.2.4 → 2.3.5** (Sim.lua 2, SimTimeline 3, SimPanel 5). If another item of this release has already
  moved `SimPanel.lua` or `SimTimeline.lua` on the run branch (the sim strip may), LK-01 does not bump that file
  again. Each file bumps once per release (`docs/releasing.md` step 2), and LK-01 extends the version document
  and CHANGELOG section that item wrote.
- `docs/api/Sim/version-2.3.5-docs.md` (Current, Supersedes 2.2.4, *What changed at this version*, `Since`
  SimTimeline 3 / SimPanel 5 on the changed members and rows), the old document marked Superseded with
  *Moving to 2.3.5*, the `docs/api/README.md` row, `lua tools/gen-api-members.lua` (members-2.3.5.json; no
  member change), the CHANGELOG `v1.76.0` section with *What a consumer owes*, and `docs/test-cases.md` from
  `lua tests/run.lua --list`.

### 2.5 Host fallout (one item per host, after its re-vendor)

Each host owes three things, and no code beyond its strings:

1. **Strings and comments** that name Run all or present `/xx sim run` as the way to play.
2. **Suites** whose typed or clicked start now arms a run. The rule for the implementer: a case whose subject is
   not auto-play keeps its subject. It starts through the member (`NS.SimScenario.Start`, `Sim:Start{}`) or
   follows the typed start with `sim pause`. A case whose subject **is** the typed path asserts the new
   behavior. New failing cases come first.
3. **Docs**: README, settings and schema docs, data flow, and the smoke procedures. A smoke check whose
   procedure presses Run all or types `/xx sim run` after a start gets its procedure amended, with
   `(procedure amended for auto-play, <ID>, 2026-10-23)` after it. Its recorded result is left as written,
   because a passed check is never edited into a new pass. New SIM checks are added for auto-play, with no
   result.

No host bumps its version, and no host has a root CHANGELOG (addons keep the README's Version History, which a
version bump writes, so nothing is written there now).

---

## 3. Risks

- **Fallout in the library's own suites.** About fifteen existing cases start through the typed verb or the
  picker and then call `run` or click `Run all` (`tests/test_sim_panel.lua:445-469`, `tests/test_sim_verbs.lua:364-381`,
  `tests/test_sim_host.lua:227, 275, 295`, `tests/test_sim_session.lua:178`, and every case that asserts
  `RUN_ALL`). Each is rewritten to its new truth in LK-01. None is deleted without a replacement asserting the
  same subject.
- **DropWatcher's async pool.** A typed start that waits on the Encounter Journal now plays as soon as the pool
  is ready, and `m.advance` in DW's suites fires that first tick. Cases that advance the clock after a typed
  start (`test_sim_scenario.lua` 265-282, `test_sim_panel.lua` 205-222) must pause first or start through the
  member.
- **Host verbs beside a playing run** (A12). `/dw sim pull` during an auto-run can meet the timeline's own pull
  and print DW's "already engaged" refusal. This is acceptable and documented in the usage line ("pause it to
  step by hand").
- **The gate.** The armed run's ticks go through `tick`, so LH's ledger gate and BL's settle window hold an
  auto-run exactly as they hold Run all today.
- **A host start that bypasses `RunVerb`** would not auto-play. None exists today (grep), and A8's Resume-as-run
  makes such a session playable from the panel anyway.
- **Smoke results.** The checks DW SIM-10/SIM-11, BL SIM-11 and LH SIM-9 passed on 2026-10-23 against Run all.
  Their procedures are amended, not re-passed, and the new auto-play checks carry the in-client proof.
