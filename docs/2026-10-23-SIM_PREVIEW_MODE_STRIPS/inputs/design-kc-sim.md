# KickCD simulator, `/kcd sim`: design (KC-01 to KC-10)

- **Scope:** OWNER_SCOPE A ("Add a /kcd sim workflow"), B2 (the sim strip on top of the icon grid, shown only
  while a simulation runs), B4 (KickCD#38's scenario list, a headless end-to-end suite, #38 closes on merge).
- **Status:** design input for the bundle's spec. Read-only analysis: nothing in any repo was edited.
- **Sources read:**
  - KickCD `master` at `4dcbf8d`, carrying LibKa0s v1.75.2: `CLAUDE.md`, `KickCD.toc`, `docs/ARCHITECTURE.md`,
    `docs/testing.md`, `docs/slash-dispatch.md`, `docs/smoke-tests.md` (index and format), `core/Compat.lua`
    (whole), `core/State.lua`, `core/CoreSetup.lua`, `core/Util.lua` (`NewUnitCastFilter`), `core/KickCD.lua`
    (`COMMANDS`, `FEATURE_VERBS`, `setLocked`), `core/LifecycleSetup.lua`, `core/MediaSetup.lua`,
    `modules/Cooldowns.lua`, `modules/IconGrid.lua`, `modules/IconGrid_Handle.lua`,
    `modules/IconGrid_Visibility.lua`, `modules/Castbar.lua`, `modules/Castbar_Events.lua`,
    `modules/UnitLabel.lua` (`FrameAbove`), `modules/Diagnostics.lua`, `defaults/Profile.lua` and
    `defaults/Spells.lua`.
  - The test harness: `tests/run.lua`, `tests/wow_mock.lua`, and the kit's `tests/_kit/mock_base.lua`
    (CallbackHandler and AceEvent mocks, `GetTime` and timers).
  - LibKa0s `docs/api/Sim/version-2.2.4-docs.md` (the whole host contract, H1 to H10) and the Widgets
    13.1.4.3.2 `TestStrip` contract.
  - The Sim-1.0 hosts: BankLedger `core/SimSetup.lua` and `modules/Sim.lua` (whole), LootHistory
    `modules/Sim.lua` (`deliver`, `STOP_TEXT`, the `stepDelay` row), and DropWatcher `NS.DeliverEvent`.
  - WowAddonStandards `preview-mode.md`, *The in-game simulator (MAY)*.
  - The previous bundle's `99_EXECUTION_RECORD.md` (the 2026-10-23 step-delay feedback round).
  - KickCD#38.

---

## 0. Decisions in one page

| # | Decision | Why |
|---|---|---|
| D1 | **The simulated "party" is narrative. The engine paths are the player's own.** KickCD tracks only the *player's* interrupt and CC cooldowns, against the *target's* and *focus's* casts (ARCHITECTURE.md *Overview*). It has no party tracking. So the four made-up party members appear only in `[sim]` lines and step labels, and their kicks end enemy casts through `UNIT_SPELLCAST_INTERRUPTED`. What the engine actually runs on is the player's cooldowns, the target and focus units, their casts, combat and the GCD. No party tracking is added. | B4 makes #38's scenario list the scope. #38 is the collection's template wording ("party UNIT_SPELLCAST_SUCCEEDED"), and KickCD has no code path that reads a party member. A simulator drives the *real* engine (preview-mode). It cannot exercise a feature that does not exist, and adding one is out of scope. Each #38 scenario maps onto the engine path it stresses (§4). |
| D2 | **Prerequisite: close the compat gaps first (KC-01).** Nine direct client reads outside `core/Compat.lua` move behind new Compat members, read at call time. | Host contract H1, and compat-§1, which standard v2.79.0 named as the simulator prerequisite in #38. A read the seam cannot see answers live data during a session, silently. |
| D3 | **Prerequisite: one dispatch table (KC-02).** It is a route registry that `NS.RegisterEventList` and `Util.NewUnitCastFilter` both feed, plus `NS.DeliverEvent(event, ...)`. That call reproduces exactly the handlers the client would run: the AceEvent routes still registered, and the armed cast filters for the event's unit. | H3. KickCD has no single dispatch table. Game events reach six AceEvent targets and four private cast-filter frames. Both registration paths are already single choke points, so recording at them is the minimal change. |
| D4 | **The sim answers through providers on Compat members only. It uses the player's real class, spec and spell list, but simulated cooldowns.** `GetSpellInfo`, `GetSpellTexture`, `IsSpellAvailable`, `GetSpecialization*` and `UnitClass` stay live. | The player sees their own grid working, with their own spells. No spell DB has to be faked. The spell list is read, never written. |
| D5 | **Duration objects are real client objects**, from a new pure Compat member `Compat.NewDuration(start, duration)` over `C_DurationUtil.CreateDuration()`. On a client without it, the simulation refuses to start. | The grid and the cast bar hand the handle to C methods (`SetCooldownFromDurationObject`, `SetValue`), which take no Lua table. A Lua fake would raise in game. The headless suite installs a fake `C_DurationUtil`. |
| D6 | **No guarded members.** `opts.guarded = {}`. | KickCD sends nothing and acts on nothing: it has no chat, comm or cast call in Compat (checked). "Nothing is cast, nothing announced" holds by construction. The `[sim]` lines are narration printed through the host's own printer. |
| D7 | **The step delay is a fixed host function, `step.wait or 1` seconds, with no settings row.** | The scenarios tell a timed story: a 3 s cast is kicked 1 s in, and the kick comes back. A 10 s slider (the LH/BL rows) would let a run break its own story. Sim-1.0 C.11 allows a host constant, and the default matches the owner's 1 s ask from 2026-10-23. The drivers are also *state-driven* (§5), so a pause or a click-ahead never produces a wrong line, only a different outcome, narrated truthfully. |
| D8 | **The marker is the LibKa0s sim-flavor strip, parented to `UIParent`.** It is placed exactly where `anchorHandle` puts the unlock strip: BOTTOM to TOP of the unit label when one sits above the grid, else of the grid, 2 px clear. It shows only while a session is active. | B2. It is parented to UIParent rather than to the grid because the visibility mode hides the grid between casts, and a marker that vanishes with the grid fails "mark the session while it runs". `UnitLabel:FrameAbove` already answers "is the label in the way" for the drag strip. |
| D9 | **Refusals, in order:** stood down; performance capture running; unlocked (KickCD's preview); in combat; in an instance; in a group; neither the Target nor the Focus grid enabled; no tracked spell the player can use; client cannot build durations. | Preview-mode MUSTs (stood down, "test mode", combat, instance, group). The rest are what the engine needs to show anything. Unlocking *is* KickCD's preview (ARCHITECTURE.md *launcher*: "No Test mode entry (unlocking *is* the preview)"). |
| D10 | **Auto-stops:** a real `PLAYER_REGEN_DISABLED` (`combat`), a real `PLAYER_ENTERING_WORLD` (`world`), a real `GROUP_ROSTER_UPDATE` that leaves the player in a group (`group`), a profile change (`profile`), a `locked = false` write by any path (`unlocked`), and the stand-down (`standDown`, the first stand-down step, H6). A real target or focus change, a real `UNIT_SPELLCAST_*` on them and a real `SPELL_UPDATE_*` are **absorbed**: their handlers re-read the simulated world. | "Stops by itself when the real world interferes" (#38). The absorbed events cannot change what the player sees during a session, because every read they trigger is answered by the sim. |
| D11 | **Slash-only `sim` feature verb**, refused while disabled (`FEATURE_VERBS`). No launcher entry and no key binding. The library's step panel docks beside the grid. | H7, preview-mode. |
| D12 | **Ten items, KC-01 to KC-10, in M3.** KC-01 and KC-02 depend on nothing. Everything from KC-03 on depends on `KC-RV` (LibKa0s v1.76.0, for the sim strip flavor and the auto-run start). | Reviewable slices. Each one stays green on its own. |

---

## 1. Current state, with evidence

### 1.1 What the engine reads

| Path | Client reads | Through Compat today? |
|---|---|---|
| Cooldown poll, `modules/Cooldowns.lua:162-198` (`buildSpellState`) | `GetSpellCooldown` (5 returns, plain `isActive`), `GetSpellCooldownDuration` (handle), `GetSpellCharges`, `IsSpellUsable` | **yes**: all four are `NS.Compat.*` read at call time |
| Pollability, `Cooldowns.lua:103-119` | `GetSpellInfo`, `IsSpellAvailable` | yes, and they stay live (D4) |
| Recharge handle per tick, `Cooldowns.lua:156-159` (`RechargeHandle`, called by `IconGrid_Ticker.lua` every 0.1 s) | `GetSpellCooldown`, `GetSpellCharges`, `GetSpellCooldownDuration` | yes |
| Class and spec, `Cooldowns.lua:89-94` | `UnitClass("player")` (bare), `Util.PlayerSpecID` → `Compat.GetSpecialization*` | stays live (D4) |
| Cast bar, `modules/Castbar.lua:757-766` (`Reevaluate`) | `_G.UnitExists`, `_G.UnitIsDead`, then `Compat.GetCastingInfo` | **no** for the first two |
| `Compat.GetCastingInfo` / `GetChannelInfo`, `core/Compat.lua:322-344, 481-493` | `_G.UnitCastingInfo`, `_G.UnitChannelInfo`, `_G.UnitCastingDuration`, `_G.UnitChannelDuration`, `_G.UnitCanAttack` | inside Compat, but they call `_G` directly, so one provider per raw read would not reach them |
| Hostile-cast test, `core/State.lua:89-96` (`IsHostileUnitCasting`) | `_G.UnitExists`, `_G.UnitCanAttack`, `_G.UnitCastingInfo`, `_G.UnitChannelInfo` | **no** |
| Interruptible mask, `core/State.lua:116-137` (`ApplyInterruptibleAlpha`) | the same four, positions 1 and 8 (cast) and 1 and 7 (channel) | **no** |
| Grid "is casting", `modules/IconGrid.lua:176-181` (`instanceCasting`) | `_G.UnitExists`, `_G.UnitCastingInfo`, `_G.UnitChannelInfo` | **no** |
| Glow gate, `modules/IconGrid_Visibility.lua:197-207` (`resolveInterruptible`) | `_G.UnitCastingInfo` position 8, `_G.UnitChannelInfo` position 7 | **no** |
| Combat seed, `core/State.lua:172, 239` | `_G.InCombatLockdown` | not needed: the sim drives combat through the regen events (§5.4) |
| Debug dumps, `modules/Castbar_Debug.lua:64-69`, `Compat.DebugInterrupt` | raw unit reads | **left raw on purpose**: they dump the *real* client, which is what a bug report wants. Recorded in compat-layer.md. |

**Nothing outward.** Compat has no send, comm, cast or world-changing member. KickCD prints only to its own
chat frame through `NS.Util.print`.

### 1.2 How events arrive (no single table)

- **AceEvent targets.** Each registers through `NS.RegisterEventList(target, list)` (`core/CoreSetup.lua:85-92`),
  the one host caller of `SafeRegisterEvent`:
  - `Cooldowns`: `SPELL_UPDATE_COOLDOWN`, `_USABLE` and `_CHARGES` → `OnCooldownEvent`, with a next-frame
    coalescing throttle; `PLAYER_ENTERING_WORLD`, `PLAYER_SPECIALIZATION_CHANGED`, `SPELLS_CHANGED` and
    `TRAIT_CONFIG_UPDATED` (`Cooldowns.lua:596-617`).
  - `IconGrid`: spec, PEW and spells events, plus `PLAYER_TARGET_CHANGED` / `PLAYER_FOCUS_CHANGED`
    (`IconGrid.lua:742-769`).
  - `Castbar`: PEW, target changed and focus changed (`Castbar.lua:848-862`).
  - `UnitLabel`: its lifecycle list.
  - `core/State.lua`'s `boot` target: `PLAYER_REGEN_*` and `PLAYER_LOGIN` (`State.lua:188-203`).
  - `core/SpellInput.lua` and the Spells page: their own lists.
- **Per-unit cast filters.** `Util.NewUnitCastFilter(module, unit, routes)` (`core/Util.lua:513-540`) builds one
  private frame per (module, unit) and registers `UNIT_SPELLCAST_*` with `RegisterUnitEvent` for that unit.
  IconGrid's `ICON_CAST_ROUTES` (`IconGrid.lua:89`) and Castbar's `CASTBAR_CAST_ROUTES` (`Castbar.lua:119-133`)
  each have one filter per enabled unit. `Arm` and `Disarm` keep an `armed` flag.
- AceEvent stores each registration's callable in its CallbackHandler registry,
  `LibStub("AceEvent-3.0").events.events[event][target]`. The kit's mock reproduces that registry field for field
  (`tests/_kit/mock_base.lua:245-330`, 716-768), so a deliver that reads it behaves the same headless and in game.

### 1.3 Surfaces the simulator touches

- **Slash.** `COMMANDS` (`core/KickCD.lua:231-306`). `FEATURE_VERBS = { "lock", "unlock", "toggle",
  "resetposition" }` (`:374`), which the library refuses while disabled. `core/KickCD.lua` is 940 lines.
- **Preview.** Unlocking (`setLocked`, `core/KickCD.lua:172-185`, and `NS.ToggleLock` `:198-201`, which the
  launcher's *Locked* entry also calls) bypasses the visibility mode and draws the cast-bar placeholder
  (`Castbar.lua:707-711`, `IconGrid_Visibility.lua:67, 94`). The settings checkbox is a composed Master-controls
  row (`settings/SchemaSetup.lua:38-46`).
- **The top-of-grid placement already exists.** `IconGrid_Handle.lua:117-127` (`anchorHandle`) hangs the unlock
  strip `BOTTOM` → `TOP` of `UnitLabel:FrameAbove(unit, "icons")` or of the grid, `DRAG.GAP` clear.
  `IconGrid:GetGridFrame(unit)` (`IconGrid.lua:967-970`) answers the grid frame. By default the label sits
  above the grid (`defaults/Profile.lua:302-307`) and the cast bar sits below it (`:213-217`).
- **Stand-down.** `core/LifecycleSetup.lua:118-133` (`standDown`). H6 needs `NS.Sim:Stop("standDown")` as its
  first line.
- **Diagnostics.** `modules/Diagnostics.lua:259-274` (`X.Sections`). H8 needs a `sim` section.
- **Icons.** The `LibKa0s icons:` line declares `clear, close, copy, help, segment` (CLAUDE.md). The step panel's
  done mark (`confirm`) and the strip's mark (`info`) are host-declared, so both join the line and
  `libs/LibKa0s/media/icons/`, which is pruned to the line.
- **No CHANGELOG.md.** KickCD records history in README `## Version History`, and that section is only rolled
  at a version bump, which this run does not do. So the change is recorded in the docs set (§8), and the
  Version History line waits for the owner's next bump.

---

## 2. Files

| File | New / edit | Lines (est.) | Role |
|---|---|---|---|
| `core/Compat.lua` | edit | 493 → ~590 | KC-01 members |
| `core/State.lua`, `modules/IconGrid.lua`, `modules/IconGrid_Visibility.lua`, `modules/Castbar.lua` | edit | ±10 each | KC-01 call sites |
| `core/Events.lua` | **new**, after `core\CoreSetup.lua` | ~150 | KC-02 route registry and `NS.DeliverEvent` |
| `core/CoreSetup.lua`, `core/Util.lua` | edit | +6 | KC-02 record calls |
| `core/SimSetup.lua` | **new**, directly after `core\Compat.lua` (LOAD-BEARING) | ~120 | KC-03 seam and both stubs |
| `modules/SimWorld.lua` | **new** | ~380 | KC-04 world model and providers |
| `modules/Sim.lua` | **new** | ~420 | KC-05/06 descriptor, refusals, stop, interference, presentation |
| `modules/SimDrivers.lua` | **new** | ~360 | KC-07 one driver per step kind |
| `modules/SimScenario.lua` | **new** | ~330 | KC-08 party and the four scenarios |
| `modules/SimStrip.lua` | **new** | ~170 | KC-09 the marker |
| `core/KickCD.lua` | edit | +25 | `sim` row, `FEATURE_VERBS`, lock refusal, `resetall` refusal |
| `core/LifecycleSetup.lua`, `modules/Diagnostics.lua` | edit | +3 / +25 | H6, H8 |
| `locales/enUS.lua` | edit | +~90 | every new line |
| tests | **new**: `test_compat_units.lua`, `test_event_routes.lua`, `sim_support.lua`, `test_sim_seam.lua`, `test_sim_world.lua`, `test_sim_session.lua`, `test_sim_drivers.lua`, `test_sim_e2e.lua`, `test_sim_strip.lua` | each < 600 | registered in `tests/run.lua`'s suite list (the kit's inventory gate) |

The TOC places the module files after `modules\UnitLabel.lua` and before `modules\Diagnostics.lua`, in this order:

1. `SimWorld`: registers its providers at load, on `NS.SimSeam`.
2. `SimDrivers`
3. `Sim`: creates `Host.SCENARIOS` and calls `Sim:New`.
4. `SimScenario`: fills `Host.SCENARIOS` in place, which Sim-1.0 reads at call time.
5. `SimStrip`

Each line carries a LOAD-BEARING comment where its order matters. No file nears the 1500 cap. Every
function stays under CCN 15: refusals and drivers are tables of small functions, the BankLedger `CHECKS`
idiom.

---

## 3. The seam (KC-03)

- `core/SimSetup.lua` is BankLedger's file with these changes:
  - `pure = { IsSecret = true, _firstReturn = true, NewDuration = true, DebugInterrupt = true }`.
  - `guarded = {}` (D6).
  - `debug = function(tag, fmt, ...) if NS.State and NS.State.debug and NS.Debug then NS.Debug("Sim", fmt, ...) end end`.
  - `NS.SimHost = NS.SimHost or {}`.
  - The library-absent branch publishes `newSeamStub()` and `newSimStub(say)`, copied from the Sim document's
    reference stub. `say` resolves `NS.Util.print` at call time, because CoreSetup loads later.
- Every other Compat member is wrapped. That includes the CompatLib-routed ones (`GetSpellCooldown`, ...),
  because each is a function member of `NS.Compat`.
- `tests/test_sim_seam.lua` asserts:
  - `#NS.SimSeam:Unwrapped() == 0` after the whole addon loads (H2);
  - `Keys()` includes every KC-01 member and excludes the four pure ones;
  - the stub-parity triple (Sim document, *Adopting it*, step 4).

---

## 4. Scenarios (KC-08): #38 mapped onto the engine

The party is made up: **Thrall** (Enhancement Shaman, Wind Shear), **Jaina** (Frost Mage, Counterspell),
**Uther** (Protection Paladin, Rebuke) and **Valeera** (Subtlety Rogue, Kick). They are data in `SimScenario.lua`,
named only in `[sim]` lines and labels. "Your kick" is the first enabled, watched entry of category
`interrupt` in the active spec's list (`Database:GetSpellList`, `defaults/Spells.lua` categories), else the first
watched entry. "Your CC" is the first watched entry of any other category, else none: a CC step then narrates
"no crowd control tracked" and fires nothing.

| Scenario (`name`, label) | Steps (the engine path each exercises) |
|---|---|
| `pull`, *Mythic+ pull, several kickers* | 1. Pull starts: simulated combat, `PLAYER_REGEN_DISABLED` → `COMBAT_STATE` (in_combat visibility). 2. You target Caster A (`PLAYER_TARGET_CHANGED`). 3. You focus Caster B (`PLAYER_FOCUS_CHANGED`). 4. A starts an interruptible 3 s cast (`UNIT_SPELLCAST_START` target). 5. You kick A: kick cooldown starts, then `UNIT_SPELLCAST_SUCCEEDED` player, `SPELL_UPDATE_COOLDOWN`, `UNIT_SPELLCAST_INTERRUPTED` target. 6. B starts a channel (`UNIT_SPELLCAST_CHANNEL_START` focus). 7. Thrall kicks B (`UNIT_SPELLCAST_INTERRUPTED` focus, `[sim]` line). 8. A casts again while your kick is still cooling; Jaina kicks it. 9. You CC A (CC cooldown plus a 1.5 s GCD on every other on-GCD spell, so the GCD-suppress curve runs). 10. A dies (`UnitIsDead`, then target cleared, `PLAYER_TARGET_CHANGED`). 11. Pull ends (`PLAYER_REGEN_ENABLED`). |
| `boss`, *Boss kick rotation* | Target the boss. Your kick has **two simulated charges** (`SPELL_UPDATE_CHARGES`: the charge badge and the recharge swipe). Rotation: Uther kicks cast 1; you kick cast 2 (charge 2 → 1, recharge starts); Valeera kicks cast 3; you kick cast 4 (1 → 0, `isActive` true); the recharge completes on a compressed step (`SPELL_UPDATE_CHARGES`, `SPELL_UPDATE_COOLDOWN`); you kick cast 5. One of the casts is a channel. |
| `miss`, *Kick on cooldown, uninterruptible cast* | The target casts an **uninterruptible** spell (`notInterruptible = true`: the cast bar's uninterruptible visuals and the `target_casting_interruptible` alpha mask). Your kick attempt is refused (`[sim]` only; nothing fires). The shield breaks (`UNIT_SPELLCAST_INTERRUPTIBLE`, `OnInterruptibilityChanged`). You kick. The next cast arrives with your kick on cooldown: the attempt is refused and the cast completes (`UNIT_SPELLCAST_SUCCEEDED` / `_STOP` target). The kick comes back (a compressed expiry, `SPELL_UPDATE_COOLDOWN`). |
| `leave`, *Party member leaves mid-pull* | Simulated combat. Target A, focus B. B starts a 4 s cast that Valeera is assigned to. Valeera leaves the party (`GROUP_ROSTER_UPDATE`: no KickCD handler, delivered for fidelity, `[sim]` line). You clear focus and target B **mid-cast** (`PLAYER_FOCUS_CHANGED`, then `PLAYER_TARGET_CHANGED`: the cast bar snaps to an in-progress cast through `Reevaluate`, `Castbar.lua:757`). You kick B. Combat ends. |

There are no sizes. Every timeline is pure (Sim-1.0 previews it while idle), so a step names its role ("your
kick") and resolves the real spell when it plays.

---

## 5. The world, the drivers and timing (KC-04, KC-07)

### 5.1 The world

`Host.world` is built in `prepare` and dropped at stop.

- `units`: `{ target = enemy|nil, focus = enemy|nil }`. An enemy is `{ key, name, hostile = true, dead = false,
  cast = nil|{ spellID, name, texture, notInterruptible, isChannel, start, duration, castID } }`. Enemies are
  shared by key, so focus and target can be the same mob.
- `spells[id]`: `{ start, duration, offGcd, maxCharges, charges, chargeStart, chargeDuration }`.
- `gcd`: `{ start, duration }`.
- `combat`: a boolean, true while the sim has simulated combat.

### 5.2 Providers

Registered once at file load with `NS.SimSeam:SetProvider`. Each reads `NS.SimHost.world` at call time and
falls back when there is none.

| Member | Answer while active |
|---|---|
| `GetSpellCooldown(id)` | Its own cooldown if running. Else the GCD for a spell not marked `offGcd` while the GCD runs. Else `0, 0, false, 1, false`. Plain numbers. |
| `GetSpellCooldownDuration(id)` | `Compat.NewDuration(start, dur)`, or a zeroed duration when idle (the client's own shape, `Compat.lua:133-138`) |
| `GetSpellCharges(id)` | `charges, maxCharges, chargeStart, chargeDuration` for a charge spell; else nil |
| `IsSpellUsable(id)` | `true, false` |
| `UnitExists(u)` | `"player"`: true. `target` / `focus`: whether the world has that enemy. Anything else: false. |
| `UnitCanAttack(u)` | `enemy.hostile` (false when absent) |
| `UnitIsDead(u)` | `enemy.dead` |
| `UnitCastingInfo(u)` / `UnitChannelInfo(u)` | The client's positional returns for a cast or channel in progress. `notInterruptible` is at 8 (cast) and 7 (channel); `spellID` is at 9 and 8. |
| `UnitCastingDuration(u)` / `UnitChannelDuration(u)` | `NewDuration(cast.start, cast.duration)` |

`GetCastingInfo` and `GetChannelInfo` need no provider: after KC-01 they compose from the wrapped raw readers.

### 5.3 Drivers

The drivers are a table keyed by `step.kind`. Each edits the world, then fires the client's events in client
order through `NS.Sim:Fire`, and answers a one-line detail:

| Kinds | Groups |
|---|---|
| `Combat`, `Target`, `Focus` | combat and unit changes |
| `CastStart`, `ChannelStart`, `Interruptible` | an enemy cast begins or changes |
| `Kick`, `PartyKick`, `Complete`, `Cc` | a cast is kicked, or completes |
| `Die`, `Leave`, `Expire` | other world changes |

The drivers are **state-driven**. `Kick` reads the world: no cast, an uninterruptible cast, the kick on cooldown,
and no charge left each take their own truthful branch, with its own `[sim]` line. So a paused run, a click-ahead
or a long step delay never prints a false line.

### 5.4 Combat and timing

- **Combat.** The sim fires `PLAYER_REGEN_DISABLED` / `_ENABLED` into the State `boot` route, so `NS.State.inCombat`
  and `COMBAT_STATE` are the engine's own.
- **Cooldown expiry.** Every cooldown the world starts schedules `sim:After(remaining, ...)`, which clears it and
  fires `SPELL_UPDATE_COOLDOWN` (or `_CHARGES`), as the client does. The `Expire` kind compresses time by ending
  it at once.
- **Casts.** A cast ends only by a step: `Kick`, `PartyKick`, `Complete` or `Die`. KickCD's bar waits for the stop
  event and never ends a cast from `OnUpdate` (`Castbar.lua:501`), so a paused run shows an empty bar until the
  next step, which is honest.
- **Step delay.** `function(step) return step.wait or 1 end` (D7).
- **No `gate`.** Nothing settles asynchronously. The Cooldowns throttle coalesces to the next frame, and the next
  step is at least 1 s later. A click-ahead that runs steps back to back coalesces into the final state, which is
  correct.

---

## 6. The session host (KC-05, KC-06)

### Descriptor

- `name = "KickCD"`, `seam = NS.SimSeam`, `slash = "/kcd sim"`.
- `deliver = NS.DeliverEvent`.
- `isStoodDown = function() return NS.IsDown ~= nil and NS.IsDown() end`. Check the name: `core/LifecycleSetup.lua`
  publishes the latch read used by `IconGrid:ReconcileUnits` (`NS.IsDown`).
- `scenarios = Host.SCENARIOS`, `prepare`, `play`, `refusal`, `stepDelay`, `stopText`.
- `L = { STARTED = L["Simulation started (%s): nothing is cast, nothing is saved, and your settings are not touched."] }`.
- `print = function(line) NS.Util.print(line) end`.
- `debug` writes `NS.Debug("Sim", ...)` when debug logging is on.
- `panel = { title, stepLabel, stepTip, startTip, stopTip, anchorTo, check = NS.Icon("confirm") }`. `title` keeps
  the library default, `KickCD - Simulation`. It is the panel's name, not a mode word on a host window, and
  KickCD has no window header to strip (OWNER C).

### `prepare`

1. Build the world. This calls `NS.Cooldowns:Rebuild()`, so the watched set re-polls through the seam and every
   icon shows ready.
2. Resolve "your kick" and "your CC".
3. Register the interference watch.
4. Show the strip.
5. Show the panel.
6. Call `ready()`.

With LibKa0s v1.76.0, the run then plays by itself (OWNER C, LK auto-run).

### Interference watch

A `Host.watch` AceEvent target, registered with `NS.SafeRegisterEvent` while a session runs. It deliberately does
**not** use `RegisterEventList`, so it is never a deliver route. It listens to:

- `PLAYER_REGEN_DISABLED` → `Stop("combat")`;
- `PLAYER_ENTERING_WORLD` → `Stop("world")`;
- `GROUP_ROSTER_UPDATE` → `Stop("group")` when `IsInGroup()` (read through `Live`).

It ignores anything that arrives while `IsDelivering()`. The `profile` stop rides `Database:OnProfileChanged`. The
`unlocked` stop rides `IconGrid:OnConfigChanged`'s `general` section when `profile.locked == false`, which covers
the settings checkbox. `setLocked` refuses outright for `/kcd unlock`, `/kcd toggle` and the launcher's *Locked*
entry.

### The stop

- **`OnStopGuarded`** has nothing to do.
- **`OnStop`**, with the seam off, each step isolated:
  1. Drop the world and unregister the watch.
  2. Hide the strip.
  3. Re-sync the engine to the real client:
     - `DeliverForCleanup("PLAYER_TARGET_CHANGED")` and `DeliverForCleanup("PLAYER_FOCUS_CHANGED")`, so the cast
       bars and grids re-read the real target and focus;
     - `DeliverForCleanup("SPELL_UPDATE_COOLDOWN")` and `DeliverForCleanup("SPELL_UPDATE_CHARGES")`;
     - `NS.Cooldowns:Rebuild()`, so the real cooldowns repaint;
     - `DeliverForCleanup("PLAYER_REGEN_ENABLED")` **only** when the world had simulated combat and the reason is
       not `combat`. Real combat already set the flag.

### Destructive surfaces (H5)

- `/kcd resetall` refuses while a session runs.
- `unlock`, `toggle`-to-unlocked and the launcher *Locked* entry refuse while a session runs, through one guard in
  `setLocked`.
- Spell-list edits are not refused: they rebuild through the seam, and the world answers new spells ready.

---

## 7. The marker (KC-09)

- **Module.** `NS.SimStrip`, in `modules/SimStrip.lua`.
- **Built lazily** on the first `Show`: `W.TestStrip`'s sim flavor, as LK-10..19 ships it. The implementer reads the
  vendored Widgets document for the exact call. `{ text = ..., icon = NS.Icon("info") }`, parented to `UIParent`,
  strata `MEDIUM`.
- **Text.** `L["Simulation: %s - /kcd sim stop ends it."]`, with the scenario's label.
- **Placement**, re-run on each sim listener transition, on `Ka0s_KickCD_GridLayout`, and on `CONFIG_CHANGED` for
  the `general` and `units` sections:
  - **Unit.** `target` when `NS.Units.IsEnabled("target")`, else `focus`, else none.
  - **Anchor.** `UnitLabel:FrameAbove(unit, "icons") or IconGrid:GetGridFrame(unit)`.
  - **Point.** `BOTTOM` → anchor `TOP`, 0, 2.
  - **Scale.** `strip:SetScale(grid:GetEffectiveScale() / UIParent:GetEffectiveScale())`, so it reads at the grid's
    size.
  - **Width.** `max(STRIP_MIN_W = 220, grid:GetWidth())`.
  - **No unit, or no grid.** It floats at `UIParent CENTER 0, 180`, so the marker never disappears while a session
    runs.
  - **Test record.** `strip.__anchorTo`, the `anchorHandle` idiom.
- **Visibility.** Shown while `NS.Sim:IsActive()`, hidden otherwise. It is not parented to the grid, so a grid the
  visibility mode hides leaves the strip up.
- **Bus.** The strip subscribes to `GRID_LAYOUT` and `CONFIG_CHANGED` through its own `NS.NewBusTarget()` only while
  shown, and releases them on hide. message-bus.md gains the consumer row.
- **No tooltip.** It is mouse-transparent: the step panel explains the session.

---

## 8. Documentation ripple (KC-10)

- **README.** A short `### Simulator` paragraph under *Usage*: what `/kcd sim` does, that it is safe, and how to stop
  it. README carries no command table.
- **docs/ARCHITECTURE.md:**
  - module-map rows for the simulator and the dispatch table;
  - the five new module files and the two core files in *Load order*;
  - an invariant: "every client read the simulator answers is a Compat member read at call time" (H1);
  - `## Documentation map`;
  - the slash list;
  - no deviation row: there is none.
- **Topic docs:**
  - `docs/compat-layer.md`: the new members, the pure set, and why the debug dumps stay raw.
  - `docs/slash-dispatch.md`: the `sim` row, plus the `resetall` and `unlock` refusals.
  - `docs/message-bus.md`: the strip's consumer rows.
  - `docs/module-map.md`.
  - `docs/data-flow.md`: the deliver path.
  - `docs/testing.md`: the new suites and the coverage matrix rows.
  - `docs/test-cases.md`, regenerated with `lua tests/run.lua --list`.
- **docs/smoke-tests.md.** A new `## SIM` section, SIM-1 to SIM-12, with an index row and every check listed under
  *Pending sign-off*. The owner signs them off; nobody else marks a pass.
- **CLAUDE.md.** Only the `LibKa0s icons:` line changes: `clear, close, confirm, copy, help, info, segment`.
- **No CHANGELOG.md exists.** README's *Version History* moves only with a version bump, and this run does not
  bump.

---

## 9. Risks

| Risk | Mitigation |
|---|---|
| `C_DurationUtil.CreateDuration` and its setter name (`SetTimeFromStart`) are recalled, not verified in a 12.1 client | `Compat.NewDuration` pcall-guards the constructor and the setter, and answers nil on any failure. The refusal "this client cannot build simulated cooldowns" then stops the session before anything draws. SM-KC-1 is an in-game `/run` probe and the first smoke check. If the setter name differs, the KC-01 implementer adjusts the single body. |
| A `LuaDurationObject` may lack `EvaluateTotalDuration` | `IconGrid_Render.lua:586-589` already falls back to `EvaluateRemainingDuration`. GCD classification then degrades to remaining-time, which is cosmetic. |
| `NS.DeliverEvent` reads CallbackHandler's `registry.events`, a field CallbackHandler publishes but documents loosely | It has been stable since 2008, and the kit mock reproduces it. When the field is not a table, `DeliverEvent` answers 0 and writes one debug line. The e2e suite would go red, and so would SIM-2 in game. |
| Real AceEvent dispatch order is `pairs`, the route registry's is registration order | No KickCD event has two handlers whose relative order matters: target and focus changes re-evaluate per-module state, and the bus orders cross-module effects. Documented in data-flow.md. |
| A user drags or reads the real target mid-session | Absorbed by design (D10), and the strip and panel say a simulation is running. SIM-9 checks it. |
| The strip's sim-flavor API is designed in parallel (LK-10..19) | KC-09 depends on `KC-RV`, reads the vendored Widgets document, and tests through `strip.text` and the doc's public surface only. |
| #38's party wording versus a player-only tracker | D1. Recorded as the one open question, with the decision already taken. |
