# MultiMeters simulator (`/mm sim`): design

- **Scope:** OWNER_SCOPE A ("Add a /mm sim … workflow for multimeters") and B4 (MultiMeters#60's scenario
  list is the scope, each scenario with a headless end-to-end suite; #60 closes when the work merges).
- **Item range:** MM-10..MM-20. MM-01..09 belong to the strips agent (the TEST MODE header word).
- **Read-only analysis.** Sources: MultiMeters master `a14acce` (vendors LibKa0s v1.75.2, Sim key 2.2.4),
  `gh issue view 60`, LibKa0s `docs/api/Sim/version-2.2.4-docs.md` (H1-H10 and the four rulings), the
  standard's `preview-mode.md` *The in-game simulator*, the previous bundle's `design-sim.md` and
  `req-lh-sim.md`, and the three shipped hosts: BankLedger (`core/SimSetup.lua`, `modules/Sim.lua`),
  LootHistory (`modules/Sim.lua`, `tests/sim_support.lua`, `tests/test_sim_e2e.lua`) and DropWatcher.
- **Builds on:** LibKa0s v1.76.0 (MM-RV, lead-owned). From this run's LibKa0s items it uses two things:
  the auto-run on start (a Start plays the run at once; there is no Run all button) and the sim flavor of
  the generalized strip (LK-10..19, the strips agent's design).

---

## 1. Current state, with evidence

### 1.1 Compat: the meter is already routed, the world is not

`core/Compat.lua` (772 lines) holds the eight guarded meter shims (`IsDamageMeterAvailable` :113,
`GetCombatSessionFromType` :127, `GetCombatSessionFromID` :138, `GetCombatSessionSourceFromType` :157,
`GetCombatSessionSourceFromID` :165, `GetAvailableCombatSessions` :179, `GetSessionDurationSeconds` :190,
`ResetAllCombatSessions` :201), the death-recap shims (:248-:476), the formatter and texture helpers, the
three context probes (`IsInDelve` :685, `IsSkyriding` :717, `IsInHousing` :726), `BarInterpolation` :743 and
`ChatSender` :768. `modules/Provider.lua` is the only caller of the meter shims, and
`tests/test_provider.lua:60-98` proves it by scanning the source for `Compat%.GetCombatSession` and the
other shim names.

The world the simulator must answer is **not** routed. These reads go straight to `_G` today:

| Read | Sites |
|---|---|
| `UnitGUID`, `UnitName`, `UnitExists`, `UnitClass` | `modules/Roster.lua:222-230`; `core/MultiMeters.lua:407` (feign) |
| `UnitGroupRolesAssigned`, `GetSpecializationRole` | `modules/Roster.lua:247`, `:258` |
| `GetNumGroupMembers`, `IsInRaid` | `modules/Roster.lua:281`, `:298`, `:522` (debug line) |
| `IsInGroup` | `modules/Visibility.lua:134-135` |
| `IsInInstance` | `modules/Visibility.lua:111-115` (`GetContext`) |
| `UnitAffectingCombat("player")` | `core/MultiMeters.lua:531-534` (`fighting`), `modules/WindowManager.lua:636-638`, `modules/Visibility.lua:157-158`, `modules/Tooltip.lua:560` |
| `OpenDeathRecapUI` (an outward action) | `modules/DrillDown.lua:268` (the call site already prefers a `Compat.OpenDeathRecap` that does not exist yet, :264) |

Left live on purpose (the simulated player is the real player, or the read is not one the simulation
answers): the player-state probes in `modules/Visibility.lua:127-204` (vehicle, mount, form, taxi, pet
battle, dead), `core/CoreSetup.lua:213,265` (the player's class color), `modules/Feign.lua:93,131` (the
simulator fires no `UNIT_SPELLCAST_SUCCEEDED`), `modules/Export.lua:616-629,741` (the real target and the
hardware-event rule; the send itself is guarded), `modules/Window.lua:1083` and `core/Secrets.lua`
(`InCombatLockdown`, the restriction and the secret guards), the clock reads, and every diagnostics read
(the report describes the client).

### 1.2 Events: one table, no single entry

`core/MultiMeters.lua:125-195` is one `EVENTS` array of `{ event, methodName }`, registered through
`NS.SafeRegisterEvent` with refused names collected in `NS.State.rejectedEvents` (:211-218). AceEvent calls
`NS[method](NS, event, ...)` per row. There is no single entry function, so there is no place for a
simulated `deliver` to reuse and none for a real-event classifier. Each handler republishes on the bus
(`MSG.*`) and decides nothing (Feign and the system-message filter aside).

### 1.3 Test mode substitutes the source at the provider

`modules/Provider.lua:328-331` and `:955` return `NS.Aggregator.TestColumn/TestSourceDetail` while
`NS.State.testMode` is on, and `modules/Roster.lua:337-347` caches `Aggregator.TestGroup()`. The data lives in
`modules/Aggregator_Preview.lua`. Test mode is turned on and off only through `WindowManager:SetTestMode`
(:681), which refuses a start in combat, and it ends at `PLAYER_REGEN_DISABLED` through
`M:EndTestModeForCombat` (`core/MultiMeters.lua:334-341`).

### 1.4 SavedVariables a simulation could reach

There is no "saved segment" store of the addon's own: the client holds the segments. What MultiMeters
writes on its own is:

- **`db.global.roster`**, the remembered roster (`modules/Roster.lua:164-186` `remembered()`, written by
  `rememberMember` :390 and `linkPetOf` :365, cleared by `Roster.Forget` :706-716 on `MSG.METER_RESET`).
  Every simulated build and every simulated reset would write it. **This is the H4 store.**
- **`window.data.sessionID` / `sessionType`**, the segment pin, written by `WindowProto:SetSegment`
  (`modules/Window_Header.lua:1032`), `SetSessionType` (:1055) and the stale-pin repair
  `DropStaleSegment` (:1005-1022), which drops a pin `Provider.HasSession` cannot find. During a session
  the simulated session list would make every real pin look stale and drop it.

### 1.5 Outward actions

`Compat.ChatSender` (the export's send), `Compat.ResetAllCombatSessions` (wipes Blizzard's meter too) and
`OpenDeathRecapUI`. `Provider.Reset` (`modules/Provider.lua:895-901`) also publishes `MSG.METER_RESET`
itself.

### 1.6 The strip

`modules/Window.lua:61-77` (`stripReserve`, test mode only) and `:668-671` (`self.testStrip =
W.TestStrip(frame, {...})`), `modules/Window_Header.lua:757-794` (`stripShown`, `PlaceTestStrip`,
`ApplyTestStrip`), and `modules/Window_Lifecycle.lua:95-103` (re-apply on `MSG.TEST_MODE_CHANGED`).
`modules/Window.lua` is 1405 lines.

---

## 2. Design

### 2.1 Files (all under 1500; every function at CCN 15 or less)

| File | Job | Lines |
|---|---|---|
| `core/Compat.lua` | + the world members (§2.2) | ~880 |
| `core/MultiMeters.lua` | + `NS:OnGameEvent`, `NS.DeliverEvent`, `NS.RealEventFilter` (§2.3) | ~690 |
| `core/SimSetup.lua` (new) | the seam: PURE, GUARDED, the two reference stubs | ~170 |
| `modules/Sim.lua` (new) | the host: descriptor, refusals, gate, prepare, stop, the real-event classifier, stop lines, panel fields | ~450 |
| `modules/SimWorld.lua` (new) | the invented world and every provider | ~480 |
| `modules/SimDrivers.lua` (new) | world edits plus the events each one fires | ~320 |
| `modules/SimScenario.lua` (new) | the four scenarios and the step player | ~300 |

TOC: `core\SimSetup.lua` straight after `core\Compat.lua` (before `core\EnvSetup.lua`, whose own position
rule is "before core\Namespace.lua", so the insert keeps it), with the LOAD-BEARING comment the Sim API
document gives. `modules\Sim.lua`, `modules\SimWorld.lua`, `modules\SimDrivers.lua`,
`modules\SimScenario.lua` after `modules\Visibility.lua`, in that order: `Sim.lua` builds `NS.Sim` with the
host's tables, which the three later files fill in place (the library reads every descriptor table at use).

### 2.2 Compat additions (H1)

New members, each a guarded `_G` read at call time, matching the file's style:

`UnitGUID(unit)`, `UnitName(unit)`, `UnitExists(unit)` (boolean), `UnitClass(unit)` (the client's three
returns), `UnitGroupRolesAssigned(unit)`, `GetSpecializationRole(spec)`, `GetNumGroupMembers()` (0 when
absent), `IsInRaid()`, `IsInGroup()`, `IsInInstance()` (`inInstance, instanceType`; `false, "none"` when
absent), `UnitAffectingCombat(unit)` (boolean), `OpenDeathRecap(recapID)` (boolean: whether it opened).
The callers in §1.1's table switch to `NS.Compat.X(...)` read at call time. `docs/compat-layer.md` lists
them.

### 2.3 One dispatch entry (prerequisite named in #60)

- `EVENTS` keeps its rows. Each row is registered with the one handler name `"OnGameEvent"`.
- `NS.HANDLER_BY_EVENT` is built from `EVENTS` at load (`[event] = methodName`).
- `function NS:OnGameEvent(event, ...)`: if `NS.RealEventFilter` is set and answers true for
  `(event, ...)`, the event is consumed; otherwise it calls `NS.DeliverEvent(event, ...)`.
- `NS.DeliverEvent(event, ...) -> n`: answers 0 for an event with no row or one in
  `NS.State.rejectedEvents`; otherwise it calls `NS[method](NS, event, ...)` and answers 1. This is the
  simulator's `deliver`, and the real path runs exactly the same function, so H3 holds by construction.
- The filter is a host hook. Only `modules/Sim.lua` sets it, while a session runs, and nothing else reads
  it. It is consulted on the real path only, never inside `deliver`.

Cost: one table read and one call per event, on top of AceEvent's own. The perf brackets stay inside the
handlers, so `meterEvent`, `spellEvent` and `systemEvent` measure what they measure today.

### 2.4 The seam (`core/SimSetup.lua`)

- **PURE** (never wrapped): `GetSpellInfo`, `GetSpellTexture`, `GetSpecialization`,
  `GetSpecializationInfo`, `GetSpecializationRole` (the real player's spec and real spells),
  `RecapMembers`, `RecapAPIs`, `CallRecap` (diagnostic probes of the real API),
  `CreateAbbreviatedNumberFormatter`, `GetDefaultAbbreviationBreakpoints`, `CreateNumericRuleFormatter`,
  `OpenContextMenu`, `FirstTexture`, `FirstAtlas`, `BarInterpolation`, `IsSkyriding`, `IsInHousing` (the
  real player's travel state).
- **GUARDED:**
  - `ResetAllCombatSessions`: clears the simulated world's segments and fires `DAMAGE_METER_RESET`
    through `NS.Sim:After(0, …)`, as the client's reply would arrive. It answers true and never calls the
    client.
  - `ChatSender`: answers a sender `function(text, chatType, _, target)` that prints
    `[sim] <chatType>[ → target]: <text>` through `NS.Print` and counts `session.mmSends`. The export's
    staggered timer may call it after a stop; it still only prints.
  - `OpenDeathRecap`: prints one line ("Blizzard's death recap cannot open a simulated death.") and
    answers false, so `modules/DrillDown.lua` falls back to its own breakdown.
- **Everything else is wrapped and has a provider** from `modules/SimWorld.lua` (§2.5). A wrapped member
  with no provider would answer live during a session. The e2e suite catches that: its mock world is the
  real solo answer, so a leak shows up as a wrong row.
- `NS.SimHost = {}` (host fields, C.4) and `NS.SimSeam`. When the major is absent, the two reference stubs
  from the API document are used, with the line localized.

### 2.5 The world (`modules/SimWorld.lua`)

Everything lives on the session bag (`sim:Session().mm`), built by `World.New(seed, scenario)` in
`prepare`:

- **`members`**: the ordered group, each `{ unit, guid, name, classFilename, role, specIconID, pet? }`.
  - **The local player is the real player.** In `prepare`, inside `NS.SimSeam:Live`, the real
    `UnitGUID("player")`, `UnitName("player")` and `UnitClass("player")` are read, and the player gets
    `isLocalPlayer`.
  - The others are invented, with GUIDs `Player-9998-SIM%04d` (a range no client issues) and names from a
    fixed list, seeded.
  - Hunters and warlocks carry a pet `Pet-0-9998-SIM%04d` so that pet attribution and `mergePets` run.
- **`group`**: `{ inGroup, inRaid, size }`. Unit tokens are `player` plus `party1-4`, or `raid1-N` with the
  player at a seeded raid index, plus the pet tokens. `World.Unit(token)` resolves a token.
- **`zone`**: `{ inInstance, instanceType, name }`, for example `{ false, "none", "Isle of Dorn" }` or
  `{ true, "party", "The Rookery" }`.
- **`combat`**: a boolean.
- **`segments`**: newest first. Each is `{ sessionID = SIM_ID_BASE + n, name, duration,
  totals[statEnum][guidOrCreature] = { total, deathTime?, recapID? }, spells[statEnum][guid] = { [spellID]
  = amount }, enemies = { {creatureID, name} } }`. `SIM_ID_BASE = 1000000`.
- **`current`**: the segment in progress, or the last one ended, as the client's Current reads.
- **`recaps`**: `[recapID] = { events (newest first), maxHealth }`, in the shape
  `Aggregator.TestRecap` builds (`modules/Aggregator_Preview.lua:210-245`).
- **Numbers are plain and invented.**
  - A per-member rate is drawn from a seeded LCG: the role's shape (the same proportions as
    `Aggregator_Preview.ROLE_SHAPE`) times a class jitter of plus or minus 20%.
  - A tick adds `rate × secondsPerTick` to every stat a role produces, and adds `secondsPerTick` to the
    segment's duration.
  - `amountPerSecond = total / duration`. Overall sums every segment since the last reset.

**Providers** (registered once at file load with `NS.SimSeam:SetProvider(key, fn)`). Each builds a **fresh**
table per call, so nothing the engine does can edit the world.

| Key | Answer while a session runs |
|---|---|
| `IsDamageMeterAvailable` | `true, nil` |
| `GetCombatSessionFromType(type, stat)` | Current → `current`; Overall → the sum of all segments; Expired → nil. `{ combatSources, maxAmount, totalAmount, durationSeconds }`, with `combatSources` sorted by `totalAmount` descending (Provider's documented order assumption, honored), the source fields Provider copies (`modules/Provider.lua:278-293`), enemies as `sourceCreatureID` with no GUID for `EnemyDamageTaken`, and `deathTimeSeconds`/`deathRecapID` for `Deaths` |
| `GetCombatSessionFromID(id, stat)` | the simulated segment with that id; **nil for any other id** (the world is closed: no real data mixes in) |
| `GetCombatSessionSourceFromType/FromID(…, guid, creatureID)` | `{ combatSpells = { { spellID, totalAmount, amountPerSecond }… } descending, maxAmount, totalAmount }` for that source, or nil |
| `GetAvailableCombatSessions` | `{ { sessionID, name, durationSeconds } … }`, newest first |
| `GetSessionDurationSeconds(type)` | the Current or Overall duration, or nil with no segment |
| `HasDeathRecap` | true |
| `HasRecapEvents`, `GetRecapEvents`, `GetRecapMaxHealth` | from `recaps`; false or nil for an id the world does not hold |
| `UnitGUID`, `UnitName`, `UnitExists`, `UnitClass`, `UnitGroupRolesAssigned` | from `World.Unit(token)`. An unknown token answers nil, false or `"NONE"`, as the client does |
| `GetNumGroupMembers`, `IsInRaid`, `IsInGroup` | from `group` |
| `IsInInstance`, `IsInDelve` | from `zone` (`IsInDelve` is always false: no scenario visits a delve) |
| `UnitAffectingCombat(unit)` | `combat` for the player and any group token, else false |

Spell IDs are real (a small `SPELLS` table per class and role), so the pure `GetSpellInfo` names them.

### 2.6 Drivers (`modules/SimDrivers.lua`)

Each driver edits the world, then fires the events the client would fire, in the client's order, through
`NS.Sim:Fire`:

| Driver | World edit | Events |
|---|---|---|
| `FormGroup(n, raid)` | members, group | `GROUP_ROSTER_UPDATE` |
| `Disband()` | members → just the player | `GROUP_ROSTER_UPDATE` |
| `Zone(zoneKey)` | zone | `PLAYER_ENTERING_WORLD(false, false)`, then `ZONE_CHANGED_NEW_AREA` |
| `Pull(fight)` | open a segment, `combat = true` | `PLAYER_REGEN_DISABLED`, `DAMAGE_METER_CURRENT_SESSION_UPDATED` |
| `Tick(fight)` | grow every number | `DAMAGE_METER_CURRENT_SESSION_UPDATED` |
| `Die(guid, fight)` | a death row plus its recap | `DAMAGE_METER_CURRENT_SESSION_UPDATED` |
| `EndFight(fight)` | `combat = false`, close the segment | `PLAYER_REGEN_ENABLED`, then `DAMAGE_METER_COMBAT_SESSION_UPDATED(stat, id)` once per stat in `Constants.STATS`, then `DAMAGE_METER_CURRENT_SESSION_UPDATED` |
| `Reset()` | through `NS.Provider.Reset()`, the player's own reset path (the guarded shim answers it) | `DAMAGE_METER_RESET` (from the guarded shim's `After(0)`) |

A fight is played over time. The step's `play` runs `Pull` plus the first `Tick`, then books the remaining
`fight.ticks - 1` ticks (and any scheduled `Die`) with `NS.Sim:After(TICK = 0.5, …)`, and the last tick
calls `EndFight` when `fight.ends` is set. `session.mm.pending` counts the booked ticks. **The gate is
closed while it is above 0** ("The fight is still running."), so the auto-run, a typed `step` and a
click-ahead all wait for the fight to finish.

### 2.7 Scenarios (`modules/SimScenario.lua`), from #60

| Name | Label | Steps |
|---|---|---|
| `dungeon` | Dungeon: pull and boss (5) | Form a 5-player group · Enter The Rookery · Pull trash (6 ticks × 4 s) · Boss pull (10 ticks × 18 s, the healer's pet-less ally dies at tick 7) · Boss dies, combat ends |
| `raid` | Raid boss (20) | Form a 20-player raid · Enter Liberation of Undermine · Boss pull (12 ticks × 25 s, two deaths) · Boss dies |
| `wipe` | Wipe and reset (5) | Form group · Enter The Rookery · Boss pull (8 ticks, everyone dies by tick 8) · Wipe ends combat · Reset meter data (`Reset`) · Re-pull trash (4 ticks) · Trash dies |
| `zone` | Zone change between segments (5) | Form group · Enter The Rookery · Fight segment 1 · Leave to Isle of Dorn (world) · Enter Priory of the Sacred Flame · Fight segment 2 |

- **No `sizes`** (the issue fixes 5 and 20).
- **No host verbs.**
- **Steps** are `{ kind, label, … }`, and each step's tip names what it fired and what the world now
  holds.
- **Segment names** follow the client's style: the boss name or "Trash", with the wipe's segment named
  "<Boss> (wipe)".

### 2.8 The host (`modules/Sim.lua`)

- **`prepare(session, def, opts, ready)`:**
  1. Build the world.
  2. Snapshot every window's `data.sessionID` and `data.sessionType` by window id into `session.mmPins`.
  3. Install `NS.RealEventFilter = Host.OnRealEvent`.
  4. Publish `MSG.SIM_CHANGED { active = true }`.
  5. `Fire("DAMAGE_METER_RESET")`, so that every cache (Aggregator, Targets, DrillDown, Provider memo, the
     session roster) starts from the empty simulated meter through the real handlers.
  6. `ready()`.

  **No window is force-shown.** Each window's visibility rules answer the simulated world, which is part
  of what is being simulated. The strip and the step panel mark the session.
- **`refusal(opts)`** runs inside `Live`, checked in this order:
  1. stood down (`NS.Slash:DisabledLine()`);
  2. test mode on;
  3. combat (`Compat.UnitAffectingCombat("player")` or `InCombatLockdown()`);
  4. an instance (`Compat.IsInInstance()`);
  5. a group (`Compat.IsInGroup()`);
  6. General visibility `never` ("hides every window").
- **`gate(session)`**: closed while `session.mm.pending > 0`.
- **`stepDelay`**: `Host.StepDelay()`, reading `sim.stepDelay` (MM-18; 1 s default, 0.5 to 10 in steps of
  0.5, as LootHistory and BankLedger have since the owner's 2026-10-23 round).
- **Real-event classifier** (`Host.OnRealEvent(event, ...)`, the filter). It runs only on the real path,
  while a session is active. It answers true to consume the event:

  | Real event | Action |
  |---|---|
  | `PLAYER_REGEN_DISABLED`; `ADDON_RESTRICTION_STATE_CHANGED` with a state other than Inactive | `Stop("combat")`, then deliver (answer false) |
  | `PLAYER_ENTERING_WORLD` | `Stop("world")`, then deliver |
  | `GROUP_ROSTER_UPDATE` | if a live `IsInGroup()`: `Stop("group")` and deliver; else consume |
  | `ZONE_CHANGED_NEW_AREA` | if a live `IsInInstance()`: `Stop("instance")` and deliver; else consume |
  | `DAMAGE_METER_*` | consume (the world owns the meter) |
  | anything else | deliver |

  "Live" means `NS.SimSeam:Live(fn)`.
- **Other stops:**
  - `Stop("standDown")` is the first step of `standDown()` (`core/LifecycleSetup.lua:135`, H6).
  - `Stop("profile")` is called from `fireProfileChanged` (`core/Database.lua:68`) before the message goes
    out. It covers a profile swap, a copy, a reset and `/mm resetall`.
- **`OnStopGuarded`**: cancel nothing extra. Fight ticks are `sim:After` timers, which the library cancels.
- **`OnStop(session, reason)`** (seam off), each step isolated:
  1. Clear `NS.RealEventFilter`.
  2. Restore the pins. For each snapshotted window id that still exists and whose `sessionID` or
     `sessionType` differs, `NS.SetByPaths` writes it back. This is skipped when `reason == "profile"`,
     because the snapshot belongs to the previous profile; a simulated id left there heals itself through
     `DropStaleSegment` the next time that profile is shown.
  3. `NS.State.WipeCache()`.
  4. Resync from the live client **without** `MSG.METER_RESET`. That message would make `Roster.Forget`
     wipe the real `db.global.roster`. Instead: `NS:SendMessage(MSG.ENTERING_WORLD, { isLogin = false,
     isReload = false })` (rebuilds the live roster, invalidates the Provider memo, forgets feign state,
     re-asks visibility), then `MSG.METER_SESSION` (re-reads the meter), then `MSG.COMBAT_CHANGED`. Close
     an open drill-down with `NS.DrillDown:OnMeterReset()`.
  5. `MSG.SIM_CHANGED { active = false }`.
  6. Record `Host.lastStop = { reason, events, sends, segments }` for the diagnostics.
- **Session-only seams in the engine (H4, H5):**
  - `modules/Roster.lua` `remembered()` answers `session.mmRoster` (created on first use) while
    `NS.Sim:IsActive()`, and `Roster.Forget` replaces only that table while active. `db.global.roster` is
    never read or written during a session.
  - `WindowProto:DropStaleSegment` returns early while `NS.Sim:IsActive()`. The simulated session list is
    not the client's holdings.
  - `WindowManager:SetTestMode(true)` refuses while a session runs ("Test mode is not available while a
    simulation runs.") and repaints the panel.
  - The meter reset is **not** refused: it is answered by the guarded shim, and it is the wipe scenario's
    own step.
- **Descriptor:** `name = "MultiMeters"`, `slash = "/mm sim"`, `deliver = NS.DeliverEvent`,
  `isStoodDown = NS.IsStoodDown`, `scenarios = Host.SCENARIOS`, `prepare`, `play = Host.Play`, `refusal`,
  `gate`, `stepDelay`, `stopText`, `L = LINES` (with `STARTED` overridden: "Simulation started (%s): a
  scripted fight through the real meter. Nothing is saved or sent; /mm sim stop ends it."), `print =
  NS.Print`, `debug` (tag `Sim`), and `statusLine` (segments held, ticks pending, sends). Panel fields:
  - `title`: "Multi Meters - Simulation";
  - `stepLabel`, `stepTip`, `startTip`, `stopTip`;
  - `anchorTo`: the first shown window's frame, else nil;
  - `check = NS.Icon("confirm")`.
- **Slash:** one row in `NS.COMMANDS`, `{ "sim", "Simulator: a scripted fight through the real meter; try
  /mm sim", function(a) NS.Sim:RunVerb(a) end }`, a feature verb, refused while disabled.

### 2.9 Secrets (Midnight)

**The simulator never produces a secret and never simulates the Combat restriction.**

- Its values are plain Lua numbers it invented, so `Secrets.CanCompare` answers true and the engine takes
  the GUID join and value sort, exactly as it does out of combat on the client.
- `Secrets.IsRestricted()` stays live. A session cannot coexist with real combat (refused at start,
  stopped at `PLAYER_REGEN_DISABLED` and at the restriction edge), so it always answers false.

The secret paths keep their proof where it is today: the headless `mock_secrets` suites
(`tests/test_provider.lua`, `test_aggregator_identity.lua`, `test_secrets.lua`). Simulating the
restriction with plain values would run the identity build on values that do not raise, which proves
nothing and reads as though it does.

Two invariants still hold:

- `core/Secrets.lua` remains the only inspector of a **client** value.
- `modules/SimWorld.lua` does arithmetic only on its own invented numbers before handing them to the
  seam. It never reads a value back from the client.

`CLAUDE.md`'s rule section says this in two sentences. The `test_provider.lua` scan stays unchanged: the sim
files must never spell `Compat.<meter shim>`, because providers are registered by key string.

### 2.10 The marker (H8) and the strip

- **Every MultiMeters window shows the sim strip while a session runs.** It goes in the test strip's slot
  under the title, because the two modes are exclusive. The text is localized: "SIMULATION: a scripted
  fight, not your data. /mm sim stop ends it."
- It is built with the LibKa0s strip's sim flavor (LK-10..19) and placed by the same
  `PlaceTestStrip`/`ApplyTestStrip` path.
- `stripReserve()` answers the reserve when test mode **or** a session is on.
- Window_Lifecycle re-applies on `MSG.SIM_CHANGED` as it does on `MSG.TEST_MODE_CHANGED`.
- **No SIMULATION word goes in any header.**
- The diagnostics dump gains a `sim` section, and the debug console a `Sim` tag.

---

## 3. Decisions and why

| # | Decision | Why |
|---|---|---|
| D1 | The real player is the simulated local player; group mates are invented. | `isLocalPlayer`, `Roster.LocalGUID` and the player's own row must line up the way they do in game. It is what LootHistory does. |
| D2 | The world is closed: `FromID` answers nil for any id that is not simulated, and real meter events are consumed. | Mixing real and invented segments gives grids no client can produce. |
| D3 | The pins are snapshotted and restored, the stale-pin repair is skipped while active, and `db.global.roster` is swapped for a session store. | These are the only SavedVariables writes a session reaches (H4). The byte-identical test proves it, including a mid-run pin of a simulated segment. |
| D4 | The stop resyncs through `ENTERING_WORLD`, `METER_SESSION` and `COMBAT_CHANGED`, never through `METER_RESET`. | `METER_RESET` makes `Roster.Forget` wipe the real remembered roster once the seam is off. That would be data loss. |
| D5 | Fights tick over time with `sim:After` and a gate. | "Providers that grow over the fight" (#60): bars grow and the throttle and the sort move, while auto-run and click-ahead still wait correctly. |
| D6 | No restriction or secret simulation. | §2.9. |
| D7 | No forced show of windows at start. | The visibility rules answering the simulated world is part of the engine under test. The strip and the panel mark the session. |
| D8 | A step-delay setting, `sim.stepDelay`, appended to the Master controls tail. | The owner gave the three shipped hosts this slider on 2026-10-23, which supersedes C.11's constant for them. With Start now auto-playing, the pace matters more. It is its own item (MM-18), so it can be dropped alone. |
| D9 | Dispatch through one `OnGameEvent` entry. | #60's prerequisite, and H3 by construction: the simulated and real paths share `DeliverEvent`. |
| D10 | No host verbs, no `sizes`. | #60 fixes the group sizes, and every scenario is reachable from the picker. The library bar is unchanged. |

## 4. Risks

- **`modules/Window.lua` is at 1405 lines.** MM-17 adds about 15. If it would cross 1450, the strip code
  peels into `modules/Window_Strip.lua` in the same commit.
- **The strip API is the strips agent's.** MM-17 names the expected call
  (`W.TestStrip(frame, { …, flavor = "sim" })`) and defers to LK's final option name.
- **Registration churn:** suites that assert per-event method names (search `tests/` for
  `"OnRosterUpdate"`, `"OnCombatChanged"` and the like) need updating in MM-11.
- **`/reload` mid-session** leaves a pinned simulated id in the profile. `DropStaleSegment` clears it on the
  next refresh. Nothing else persists.
- **Export staggered sends after a stop** still use the guarded sender and print `[sim]` lines. This is
  intended and harmless.
- **The `confirm` icon** is pruned from the payload today. MM-15 adds it to the `LibKa0s icons:` line and
  restores the file from the v1.76.0 payload, or `test_vendor_sync` and the prune disagree.
- **`docs/test-cases.md` and the README test badge** are generated counts. Every item that adds cases
  regenerates them.
