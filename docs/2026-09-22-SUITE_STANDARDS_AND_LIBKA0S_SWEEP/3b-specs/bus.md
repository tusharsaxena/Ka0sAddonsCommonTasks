# Design spec: `LibKa0s-Bus-1.0` (Bus minor 1)

Status: **design, CP-3 delegated and decided here.** Read-only everywhere; nothing in any repo was
modified. Measured on 2026-09-23 against every repo on `suite/2026-09-22-standards-sweep`, all nine
consumers vendoring LibKa0s v1.54.2, LibKa0s at `2a5e06f` (test-kit revision 25 committed, library
version string still v1.54.2). Standard: v2.63.0.

**Verdict: viable, on a deliberately narrow surface.** Two things clear `library-stack-§7`'s three
bars and nothing else does:

1. **The stand-down record** (PartyFrameEnhanced's union design): a per-receiver AceEvent target
   whose six register/unregister members are wrapped so the library holds a live record of events
   AND messages, taken down by `StandDown` and replayed from the record as it is NOW by `StandUp`.
   Four repos implement this semantic today (AbsorbTracker, ConsumableMaster, PartyFrameEnhanced,
   MultiMeters); the other three variants are strict subsets of PFE's, so there is no correctness
   disagreement to promote, only weaker copies to retire.
2. **The message catalog** (`Catalog`): the declare-once table the two bus-naming rules promoted in
   v2.63.0 (`architecture-§4` declare-once MUST; `naming-cheatsheet` PascalCase `<Event>` MUST)
   already require of every publisher, validated at load and made strict so a mistyped key raises
   instead of going quiet. Four repos carry a conforming table today (AbsorbTracker, AuraMaster,
   ConsumableMaster, PartyFrameEnhanced); four more owe one under rollout-debt row 9+13 (BankLedger,
   LootHistory, KickCD, MultiMeters).

The bare `NS.NewBusTarget` factory, the most-duplicated shape of all (nine copies), is **not**
promoted: high frequency, low semantic content, and `architecture-§4` prints it as host code.

> **Build corrections (2026-09-23, after `LibKa0s/Bus.lua` minor 1 was built and tested).** Three
> claims below were disproved by the build and are corrected in place, marked *[corrected]*:
> (a) §1 defect 2 is **not a live defect** — AceEvent-3.0 holds every embedded table strongly in
> `AceEvent.embeds` (`AceEvent-3.0.lua:24`, `:103`), so MultiMeters' weak-keyed set can never lose a
> target in the client; and under Lua 5.1 (no ephemerons) a weak-keyed set whose value refers back to
> its key never releases anyway. (b) §1 defect 3's "PFE records `fn or false`" loses nothing:
> CallbackHandler reads a false method as the event name exactly as it reads nil
> (`CallbackHandler-1.0.lua:85`, `method = method or eventname`); only the dropped `arg` is real.
> (c) The fixtures live inside `tests/test_bus.lua` rather than a `tests/fixture_bus.lua`, because the
> build brief allowed three files. The suite carries 27 cases, not 25: a Core-floor case and a
> degradation-stub parity case were added.

---

## 1. The nine homes, measured

Every copy named in the brief was read in full. Line counts from `wc -l`; line refs are to the file
as it stands on the sweep branch.

| Repo | Where | Lines | Target factory | Record? | What the stand-down reaches | Absent AceEvent |
|---|---|---|---|---|---|---|
| PartyFrameEnhanced | `core/Bus.lua` | 140 | `NS.NewBusTarget()` :45 wraps 6 members | **events + messages**, per target, ordered (`order`/`want`) :60-104 | `NS.BusStandDown` :111 raw `UnregisterAll*`; `NS.BusStandUp` :120 replays record | load error (`LibStub("AceEvent-3.0")` :19) |
| MultiMeters | `core/Namespace.lua` :168-253 | 253 (file) | `NS.NewBusTarget()` :210 wraps 3 message members | messages only, `subs[message] = {handler}` :216-232 | `NS.BusStandDown` :246 / `NS.BusStandUp` :251 over a **weak-keyed** set :178 | `nil` :211-212 |
| AbsorbTracker | `core/Bus.lua` | 94 | bare `NS.NewBusTarget()` :43 | messages only, append-only triples via `NS.BusSubscribe` :68 | `NS.BusUnsubscribeAll` :76 / `NS.BusResubscribeAll` :82, each answers `#subscriptions` | load error (:33) |
| ConsumableMaster | `core/Bus.lua` | 102 | `KCM.NewBusTarget(subscribe)` :52 | the **closure**, re-run on stand-up :50-60 | `KCM.Bus.StandDown` :67 (`UnregisterAllMessages`) / `KCM.Bus.StandUp` :74 re-runs closures | load error (:32) |
| AuraMaster | `core/Bus.lua` | 47 | bare `NS.NewBusTarget()` :21 | none | per module by hand (`ContainerManager.StopListening` :557, `TimedSpells.StandDown` :165) | load error (:13) |
| BankLedger | `core/BankLedger.lua` :20-26 | 229 (file) | bare | none | `NS.StandDown` :146 loops `BUS_MODULES` :121, unregisters and **nils** `__ev` (rebuild on Enable) | `nil` |
| LootHistory | `core/LootHistory.lua` :20-26 | 88 (file) | bare | none | per module Disable nils `__ev` (`Analytics.lua:675-678`, `Collector.lua:246-249`) | `nil` |
| PanelMaster | `core/PanelMaster.lua` :20-26 | 127 (file) | bare | none | `Canvas` Disable nils `__ev` (`modules/Canvas.lua:894-897`) | `nil` |
| KickCD | `core/KickCD.lua` :46-52 | 827 (file) | bare | none | AceAddon modules own their receivers; the one factory call is a settings page (`settings/Spells.lua:1334`) | `nil` |

MultiMeters' `core/Constants.lua` carries the catalog (`Constants.MSG` :515-560); it is the one
publisher whose wire names are SCREAMING_SNAKE (`Ka0s_MultiMeters_METER_UPDATED` :519).

### What the comparison settles

- **PFE is the union and nobody disagrees with it on correctness.** MM, AT and CM each record a
  subset of what PFE records (messages only), and none of them takes the other direction: none
  records something PFE drops. That is "strictly weaker", not "incompatible" — so bar 2 of
  `library-stack-§7` (no correctness disagreement) is met.
- **Three real defects in the existing copies, which the library must not inherit:**
  1. PFE `order` grows without bound: `forget` clears `want[key]` but leaves the `order` entry, and a
     re-register appends a second one (`core/Bus.lua:62-68`). Replay then registers the same
     `(kind, name)` twice — harmless to CallbackHandler (overwrite), but a leak under churn
     (Preview's conditional roster watch, `modules/Preview.lua:81`).
  2. *[corrected — not a live defect]* MM's target set is weak-keyed (`core/Namespace.lua:178`).
     The original reading: a stand-down drops CallbackHandler's reference, so a target nothing else
     holds could be collected before stand-up. **It cannot**: `AceEvent:Embed` stores every target
     in `AceEvent.embeds`, a strong table, for the session (`AceEvent-3.0.lua:24`, `:103`), in the
     client and in the kit. The weak key is harmless today; it would only bite under an AceEvent that
     stopped holding its embeds. The library still holds tracked targets strongly itself, so it does
     not lean on that internal.
  3. PFE and MM drop CallbackHandler's optional `arg`. PFE records `fn or false` (:65) — the
     `false` itself is harmless, CallbackHandler reads it as the event name *[corrected]*; MM records
     `{ handler }` (:222) while passing `...` to the raw call, so the live registration and the
     replayed one differ in arity. No consumer uses the `arg` form today (grep), so this is latent.
- **Hosts already hand-write "do not register while down".** AuraMaster guards
  `CM.StartListening` behind `not NS.IsStoodDown()` (`modules/ContainerManager.lua:574`) and
  `TS.Sync` behind the same (`modules/TimedSpells.lua:139`). A tracked target that defers
  registration while stood down makes that guard structural rather than remembered.
- **The standard's "fails at once" claim is only half true.** `architecture-§4` says a typo routed
  through a constant "is a nil index at the call site and fails at once". It fails for a subscriber
  (CallbackHandler raises on a non-string event name), but a publisher's `SendMessage(nil)` is
  silent: CallbackHandler-1.0's `Fire` opens with `if not rawget(events, eventname) ... then return end`
  (verified in `AuraMaster/libs/CallbackHandler-1.0/CallbackHandler-1.0.lua:50`). A strict catalog
  closes the publisher half. See OPEN-2.

---

## 2. The surface

Two library members, three instance members, one field. Everything else is internal.

### Library surface

| Member | Signature | Returns (arity) | Raises |
|---|---|---|---|
| `lib:New(descriptor)` | `descriptor = { name = string, isDown = function? }` | **1**: the bus instance | `name` missing or not a non-empty string; `isDown` present and not a function |
| `lib.Catalog(addonName, messages)` | dot-call; `addonName` string, `messages` = `{ KEY = "Ka0s_<addonName>_<Event>", ... }` | **1**: a fresh strict table with exactly the declared keys | see §6 |
| `lib.MAJOR`, `lib.MINOR`, `lib.MODULES` | bookkeeping | — | — |

### Instance surface

| Member | Signature | Returns (arity) | Notes |
|---|---|---|---|
| `bus:NewTarget()` | none | **1**: a fresh AceEvent-embedded table, or `nil` | The six members are wrapped (§3). One per receiver, never shared. |
| `bus:StandDown()` | none | **1**: number of `(kind, name)` entries in the record at the moment of stand-down; `0` when already down | Raw-unregisters every tracked registration; keeps the record; idempotent. |
| `bus:StandUp()` | none | **2**: `replayed` (number), `rejected` (a fresh sorted array of `"event:NAME"` / `"message:NAME"` strings, empty when none) | Replays the record as it is NOW; idempotent; refused (answers `0, {}`) while `descriptor.isDown()` answers true. |
| `bus.name` | field | — | The descriptor's `name`. Diagnostic only. |

### All-rungs-absent / dependency-absent answers

| Member | LibStub, Core, or this file absent / Core below floor | `AceEvent-3.0` absent from LibStub |
|---|---|---|
| `lib:New` | the major is **absent**: `LibStub("LibKa0s-Bus-1.0", true)` answers `nil`, the host's stub answers (§7) | works: the instance is bookkeeping only |
| `lib.Catalog` | absent; the host's stub hands back its own plain table | works: pure function, no Ace dependency |
| `bus:NewTarget` | — | **`nil`**, which is what five of the nine factories answer today (BL, LH, PM, MM, KickCD); callers already treat nil as "no bus" |
| `bus:StandDown` | — | `0` (nothing was ever tracked) |
| `bus:StandUp` | — | `0, {}` |

The headless kit is a client with every Ace fake present, so the absent-AceEvent column is reached
by a fixture that hides it (§10, case B-22).

---

## 3. Semantics of a tracked target

`bus:NewTarget()`:

1. Resolves `LibStub("AceEvent-3.0", true)` **at call time** (library-stack precedent:
   `Options.lua:603` AceGUI, `Media.lua:265` LibSharedMedia, `Launcher.lua` LDB/LDBIcon). `nil`
   when absent.
2. `AceEvent:Embed(t)` on a fresh table, so the kit's event half (which rides on the embed) and the
   client behave identically.
3. Captures the six raw members, then stamps six wrappers over them: `RegisterEvent`,
   `UnregisterEvent`, `UnregisterAllEvents`, `RegisterMessage`, `UnregisterMessage`,
   `UnregisterAllMessages`. `SendMessage` is left raw (sending is not a registration).

### The record

Per target: an ordered list of keys (`kind .. "\0" .. name`) and, per key,
`{ kind, name, handler, n, extra }` where `n = select("#", ...)` after the handler and `extra`
holds those values. **The key list has no duplicates**: forget removes the key from the list (fixes
PFE defect 1). Re-registering an existing key replaces the entry in place — CallbackHandler's own
overwrite rule, so the record and the live registration never disagree about which handler wins.

Handler forms preserved exactly: a function, a method-name string, `nil` (AceEvent's "method named
for the event"), and the `arg` form **including an explicit nil arg**, replayed with the same
arity (fixes defect 3). CallbackHandler distinguishes "no arg" from "arg is nil" by counting; so
does the replay.

### Retention

A target is held **strongly** by its bus while its record is non-empty, and released the moment it
empties (every `Unregister*` path, including `UnregisterAll*`). So:

- A target only CallbackHandler holds survives a stand-down and is replayed. *[corrected]* In the
  client AceEvent's `embeds` also holds it, so this is the library not leaning on an Ace internal
  rather than a fix of a live loss.
- A target its owner genuinely retires by emptying it (MM `WindowProto:UnregisterBus`,
  `modules/Window.lua:1354-1358`; AM `CM.StopListening`, `modules/ContainerManager.lua:557-563`)
  leaves the registry, with **no `Retire` member needed**. Outside that window the bus holds no
  reference to it at all. *[corrected]* "Becomes collectable" overclaimed: AceEvent's `embeds` keeps
  every embedded table for the session, so the promise is "leaves the bus", not "is collected".

Order: targets replay in creation order, keys within a target in first-registration order. Dispatch
order is not observable through CallbackHandler (it walks a hash), so the order exists for
deterministic tests and a deterministic `rejected` list, nothing else.

### While up (the default at `New`)

- `Register*`: the **raw call first**, then the record. A raw call that raises (retail's
  `Attempt to register unknown event`) propagates to the caller unchanged and **is not recorded**.
  The host's own `events-frames-taint-§1` pcall helper composes with this: it sees the same raise it
  sees today. (The client leaves the CallbackHandler entry behind on that raise; it never fires,
  and `StandDown`'s raw `UnregisterAllEvents` removes it anyway.)
- `Unregister*` / `UnregisterAll*`: forget, then raw.

### While down

- `Register*`: **record only; no raw call.** The registration goes live at `StandUp`. This is what
  makes "a stood-down addon registers nothing" structural for every tracked receiver (the guard
  AuraMaster writes by hand at two sites).
- `Unregister*` / `UnregisterAll*`: forget, then raw (a no-op on the registry, kept unconditional so
  the two paths cannot drift).

### Added by the build

- A non-string name is handed straight to the raw member in both states, so CallbackHandler raises
  its own usage error and nothing is recorded (a nil name would otherwise raise inside the key
  concatenation, with the library's text instead of CallbackHandler's).
- Only a call whose `self` is the target itself is recorded; any other `self` passes straight to
  the raw member. `UnregisterAll*` forgets only when its first argument is the target.
- A rejected replay entry is also raw-unregistered (pcall'd), because the client stores the callback
  before its frame refuses an unknown event; without that the dead entry sat in CallbackHandler
  until the next stand-down.
- `lib.Catalog` refuses a colon call (`Bus:Catalog(...)`) by name.

### `StandDown()`

State first, then work (Lifecycle's invariant 6, for the same reason): `down = true`, then for each
held target `raw.UnregisterAllEvents(t)` and `raw.UnregisterAllMessages(t)`. The record is kept.
Answers the entry count. A second call answers `0` and touches nothing.

### `StandUp()`

1. If already up: `0, {}`.
2. If `descriptor.isDown` is present and answers truthy: `0, {}`, and the bus **stays down**. This is
   the seam guard (§4): a bare stand-up of the registrations while the latch still holds the addon
   down is refused.
3. `down = false` (state first), then replay every entry of every held target, each through `pcall`
   so one entry that raises cannot leave the rest unregistered — `events-frames-taint-§1`'s "a block
   MUST survive one bad name", applied to the replay loop. A raising entry is **dropped from the
   record** and its `"<kind>:<name>"` goes into `rejected`. Nothing is raised out of `StandUp`: it
   runs inside the host's `standUp` callback, and a raise there would abort the rest of the host's
   rebuild (AbsorbTracker calls the bus FIRST, `core/Lifecycle.lua:112`). The host logs `rejected`
   through its debug seam, which is how `events-frames-taint-§1`'s "reachable by the player" is met.
4. Answers `replayed, rejected`.

A replay can only raise for an entry recorded **while down** (never validated by a raw call), so in
practice `rejected` is empty; the pcall is the guard for the day a host registers a retired event
during a disabled session.

---

## 4. The seam with `LibKa0s-Lifecycle-1.0`

**The latch decides WHEN; the bus does WHAT for tracked registrations.** Bus owns no hold set, no
edge, no callbacks, and takes no floor on Lifecycle.

- The host calls `bus:StandDown()` from inside its latch `standDown` callback and `bus:StandUp()`
  from inside `standUp`, **at the position in its own sequence the host chooses**. The position is
  host-specific and load-bearing, so the library cannot pick it:
  - PFE brings the bus down LAST (`core/PartyFrameEnhanced.lua:147-160`): modules suspend and a
    VISIBILITY publish must reach receivers first.
  - AbsorbTracker brings it up FIRST (`core/Lifecycle.lua:112`) so the publishes at the end of its
    stand-up reach receivers.
  - ConsumableMaster does both first (`core/LifecycleSetup.lua:73`, `:111`).
  - MultiMeters brings it up mid-sequence, after `NS:OnEnable` (`core/LifecycleSetup.lua:151` then
    `:159`).
- Bus keeps one boolean, `down`, for its own idempotence and its deferral rule. That is the state of
  **its registrations**, not a second latch: no reason to be down is ever recorded in it.
- `descriptor.isDown` is the one place the bus **asks** the latch, late-bound through a closure
  because a host builds its bus in `core/Bus.lua` long before its latch exists in
  `core/LifecycleSetup.lua`. Every record-half consumer already publishes the predicate:
  `PartyFrameEnhanced/core/LifecycleSetup.lua:83`, `MultiMeters/core/LifecycleSetup.lua:265`,
  `AbsorbTracker/core/Lifecycle.lua:196`, `ConsumableMaster/core/LifecycleSetup.lua:135`.
  Inside the latch's own `standUp` callback the latch has already recorded the edge
  (`Lifecycle.lua` `edge()` sets `down` before calling), so `isDown()` answers false there and the
  replay proceeds; anywhere else while a hold is taken, it answers true and the replay is refused.
  This is Lifecycle's "no bare stand-up" rule carried into the one member here that could otherwise
  be one.
- `StandDown` is **not** guarded: taking registrations down is always safe, and BankLedger reaches
  its teardown from AceAddon's `OnDisable` as well as the latch (`core/BankLedger.lua:195-197`).

---

## 5. Depending on AceEvent-3.0

`library-stack-§7` governs floors between LibKa0s majors and says nothing that forbids resolving a
consumer-vendored Ace lib; `§6` forbids the payload **containing** one. The existing precedent is
optional resolution at call time with a nil/zero answer when absent (Options, Media, Launcher), and
that is what Bus does. No floor on AceEvent is possible (the payload cannot contain it), and none is
declared. Injection (`descriptor.aceEvent`) was considered and rejected: no other major takes a
third-party lib by injection, and it would add a descriptor field every host fills identically.

Core floor: `NEEDS_CORE = 1`, returned before `NewLibrary`, exactly as `Lifecycle.lua:48-50` — a
load-payload check, no Core member called. Bus becomes the eighth of the thirteen majors that gate
on Core without calling it.

---

## 6. `Catalog` and the two bus-naming rules

`lib.Catalog(addonName, messages)` takes the host's **full wire names** (not suffixes), so the same
table is the declaration in both the live arm and the degraded arm and each `Ka0s_` literal still
appears exactly once in the repo (`architecture-§4`'s declare-once MUST):

```lua
local MSG = {
    -- Sender: modules/ContainerManager.lua. Payload: none.
    CONTAINERS_CHANGED = "Ka0s_AuraMaster_ContainersChanged",
}
NS.MSG = Bus and Bus.Catalog(addonName, MSG) or MSG
```

Validation, each a raise at load naming the offending key (level 2):

| Check | Rule it enforces | Evidence it passes today |
|---|---|---|
| `addonName` non-empty string | — | — |
| `messages` a non-empty table | — | — |
| key matches `^%u[%u%d_]*$` | cheatsheet: the key is SCREAMING_SNAKE | all 32 keys in AT (5), AM (4), CM (5), PFE (4), MM (14) |
| value is a string starting `Ka0s_<addonName>_` | `architecture-§4` prefix MUST | all five tables |
| suffix matches `^%u[%a%d]*$` **and** contains a lowercase letter | cheatsheet: `<Event>` is PascalCase (MUST) | AT, AM, CM, PFE pass; MM fails on every name (owed rename, debt row 9+13) |
| no two keys share a value | declare-once (two constants for one wire name is two declarations) | all pass |

The past-participle SHOULD is not checked (not mechanically decidable).

What it returns: a **fresh** table (the host's input is not mutated) holding exactly the declared
keys, so `pairs` enumerates them (a doc-parity test can still walk it), with a metatable whose
`__index` raises `"<addonName>: no bus message named <KEY>"` and whose `__newindex` raises on a new
key. So `NS.MSG.TYPO` raises at the call site, for a publisher as well as a subscriber (OPEN-2).
Existing keys can still be reassigned (a raw field write does not reach `__newindex`); the gate for
that is review, not runtime.

A host that probes a key for presence (`KCM.MSG and KCM.MSG.MACROBAR_REFRESH`,
`ConsumableMaster/modules/MacroBar.lua:586`) keeps working when the key is declared, and raises when
it is not — which is the point: the probe exists only because the host could not be sure of its own
catalog.

Module-scoped constants (the `architecture-§4` MAY; PanelMaster's `modules/Registry.lua:19-20`,
`settings/Schema.lua:31`) can use `Catalog` too, one call per owning module. Not required.

---

## 7. The degradation stub story

A host resolves the major once in its bus file and degrades when it is absent (library-stack-§7
"degrading to a stub"; `testing` `Kit.assertSurfaceParity(stub, "LibKa0s-Bus-1.0")` holds the stub
to the live surface `{ New, Catalog }`):

```lua
local Bus = LibStub and LibStub("LibKa0s-Bus-1.0", true)
if not Bus then
    -- Degraded: the payload is missing. Receivers still get a private target (the receiver rule
    -- holds), but nothing is recorded, so a disable leaves message and event registrations live on
    -- bus targets. Stated, not hidden: this install is already without Options, Slash and Lifecycle.
    Bus = {
        New = function(_, d)
            return {
                name = d and d.name,
                NewTarget = function()
                    local AceEvent = LibStub and LibStub("AceEvent-3.0", true)
                    if not AceEvent then return nil end
                    local t = {}; AceEvent:Embed(t); return t
                end,
                StandDown = function() return 0 end,
                StandUp   = function() return 0, {} end,
            }
        end,
        Catalog = function(_, messages) return messages end,
    }
end
```

The stub is five members of host code; the live path is the library. What the degraded install
loses is exactly one property (registrations on bus targets survive a disable), and the host's
`## Known Limitations` names it.

---

## 8. Deliberately excluded

| Candidate | Why it stays out | Kind |
|---|---|---|
| The bare untracked factory (`NS.NewBusTarget` without a record; 9 copies, 4 to 7 lines each) | `library-stack-§7` "MUST NOT promote on frequency alone": four lines of `Embed` with no decision in them. `architecture-§4` prints this exact function as **host** code, so promoting it would contradict the standard's own example. Hosts keep it for untracked receivers: settings-panel live refresh (setup that survives a stand-down: `AuraMaster/settings/OptionsSetup.lua:395`, `BankLedger/settings/Panel.lua:165`, `:484`, `LootHistory/settings/Panel.lua:154`, `:487`, `KickCD/settings/Spells.lua:1334`) and rebuild-style modules (BL, LH, PM). | frequency, low semantic content |
| The publisher (`NS.bus`) | Sending is not a registration and carries no stand-down semantics. Three shapes, all correct: a fresh embed (AT, AM, CM, PFE), the AceAddon object (BL, LH, PM), `NS` itself (KickCD, MultiMeters `core/Database.lua:61`). The one real hazard (a nil message sent silently) is closed at the key read by `Catalog`. | no semantic content to share |
| ConsumableMaster's closure replay (`NewBusTarget(subscribe)`) | Strictly weaker than the record (messages only; a receiver registering inline escaped it, which `core/Bus.lua:45-46` itself names). CM keeps its signature as a host shim over `bus:NewTarget()`. | subsumed |
| AbsorbTracker's append-only triples (`NS.BusSubscribe`) | Strictly weaker: no events, no forget, so a subscription its owner dropped would be resurrected on stand-up. | subsumed |
| MultiMeters' weak-keyed target set | Not preserved; *[corrected]* not a live defect either (AceEvent's `embeds` holds the target), but the library holds its own strong reference rather than lean on that internal. | Ace internals |
| A `Retire(target)` member | Not needed: emptying a target's record releases it (§3 Retention). Both retiring consumers (MM, AM) already empty the target before dropping it. | unnecessary surface |
| Automatic stand-down on the latch's edges (Bus binding `standDown`/`standUp` itself) | The position in the host's sequence is load-bearing and differs per host (§4). | host-specific |
| The pcall'd event-registration helper and rejected-name record (`events-frames-taint-§1`) | One runtime implementation in the collection (`BankLedger/modules/Ledger.lua:849`), a different concern, and the wrappers propagate a raise unchanged so a host helper composes. A separate candidate if a second consumer appears. | single consumer |
| AceBucket registrations | No consumer registers a bucket on a bus target (grep over all nine: 0). | no consumer |
| Raw `frame:RegisterEvent` / `RegisterUnitEvent` | Not AceEvent. The `events-frames-taint-§1` carve-out frames are the host's to unregister. | host-specific |
| One-sender-per-message enforcement | Not observable at runtime (no caller identity). Stays a documentation and review rule (`architecture-§4`, anti-patterns #17). | not enforceable |
| Detecting two receivers on one target | A second `RegisterMessage` of one message on one target is indistinguishable from a legitimate re-register (AuraMaster's `TS.StartListening` runs at load and again at stand-up). `NewTarget` per receiver is the enforcement, by construction. | not decidable |
| Removing tracked targets from `AceEvent.embeds` to survive an AceEvent upgrade | Reaches into Ace internals (`library-stack-§5`'s spirit). Recorded as a known limitation instead (§9). | Ace internals |

---

## 9. Known limitations (go in the API document)

1. **An AceEvent-3.0 upgrade later in the session re-embeds every target in `AceEvent.embeds`**
   (`AceEvent-3.0.lua:123-126`), which overwrites the six wrappers with raw mixins. From then on the
   record stops following that target: `StandDown` still takes everything down (raw `UnregisterAll*`),
   but `StandUp` replays the record as it was at the upgrade. The collection vendors AceEvent-3.0
   minor 4 everywhere, unchanged for years. Re-check trigger: any AceEvent-3.0 minor above 4 in any
   consumer's `libs/`. PFE and MM carry the same exposure today.
2. **A registration made on a tracked target while the bus is down is not validated until
   `StandUp`.** A bad event name surfaces in `rejected`, not at the call site.
3. **A test probe made through a tracked factory is part of the record.** A consumer suite that
   builds throwaway receivers through `NS.NewBusTarget()` should empty them
   (`t:UnregisterAllMessages()`) or build them as untracked embeds, or a later stand-down/stand-up
   case replays them.

---

## 10. Files in LibKa0s

All CRLF on disk (`.gitattributes`: `* text=auto eol=crlf`; confirm with `git ls-files --eol`),
ASCII-only string literals, US English.

### Create

| File | Purpose | Size estimate |
|---|---|---|
| `LibKa0s/Bus.lua` | the major, minor 1: Core floor, `New`, `Catalog`, the wrappers, the record, `StandDown`, `StandUp` | 300-380 lines with the house comment density (Lifecycle is 208 for a smaller surface) |
| `tests/test_bus.lua` | the suite (§11) | 450-550 |
| ~~`tests/fixture_bus.lua`~~ | *[corrected]* not created: the fixtures are the `F` table at the top of `tests/test_bus.lua` (the build brief allowed three files) | — |
| `docs/api/Bus/version-1-docs.md` | the source-of-truth contract, shaped like `docs/api/Lifecycle/version-1-docs.md`: what it is, library surface, descriptor, instance surface, the record rules (§3), the seam (§4), the absent answers (§2), hard invariants each naming its case, worked example, known limitations (§9) | 250-320 |
| `docs/api/Bus/members-1.json` | **generated** by `lua tools/gen-api-members.lua`, never hand-written; expect members `Catalog` (function) and `New` (function) | generated |

### Modify

| File | Change |
|---|---|
| `LibKa0s/LibKa0s.xml` | `<Script file="Bus.lua"/>` after `Lifecycle.lua` (floors only on Core, so any position after Core loads; beside Lifecycle keeps the stand-down pair together) |
| `tests/majors.lua` | `{ major = "LibKa0s-Bus-1.0", files = { "Bus" }, primary = "Bus" }` after the Lifecycle row (XML order) |
| `tests/run.lua` | `bus = mocks.LibStub("LibKa0s-Bus-1.0"),` in `Kit.expose`; `"test_bus"` in the suite list after `"test_lifecycle"` |
| `docs/api/README.md` | a key-shape row (`<Bus>`) and a per-major version table block |
| `README.md` | the module bullet, the module table row, the `MODULES` example line, the layout listing |
| `CHANGELOG.md` | the release entry: **Bus minor 1 (a new major)**. The current v1.55.0 heading says "No library file changes at all" — see OPEN-4 |
| `docs/releasing.md` | "twelve today" count at :46 recounted from `tests/majors.lua`; a consumer row in the adoption table (~:343) |
| `CLAUDE.md` | the `docs/api/` row's major list gains `Bus` |
| `docs/adoption-report.md` | a Bus row (who adopted what) once Phase 6 runs |

`tests/test_versioning.lua`, `tests/test_surface_parity.lua` and `tools/gen-api-members.lua` iterate
`tests/majors.lua` and need no edit.

### Implementation sketch (non-normative)

```lua
local core = LibStub and LibStub("LibKa0s-Core-1.0", true)
local NEEDS_CORE = 1
if not core or (core.MINOR or 0) < NEEDS_CORE then return end
local MAJOR, MINOR = "LibKa0s-Bus-1.0", 1
local lib = LibStub:NewLibrary(MAJOR, MINOR); if not lib then return end
lib.MAJOR, lib.MINOR = MAJOR, MINOR
lib.MODULES = lib.MODULES or {}; lib.MODULES.Bus = MINOR

local KINDS = { event = { "RegisterEvent", "UnregisterEvent", "UnregisterAllEvents" },
                message = { "RegisterMessage", "UnregisterMessage", "UnregisterAllMessages" } }

function lib:New(d)
  -- validate d.name, d.isDown
  local B, down, seq = { name = d.name }, false, 0
  local held = {}              -- target -> rec, STRONG, only while rec has entries
  local function remember(rec, kind, name, handler, ...) --[[ key list without duplicates ]] end
  local function forget(rec, kind, name) --[[ remove key; if empty then held[rec.t] = nil ]] end
  local function forgetKind(rec, kind) --[[ same, per kind ]] end
  function B:NewTarget()
    local AceEvent = LibStub and LibStub("AceEvent-3.0", true); if not AceEvent then return nil end
    local t = {}; AceEvent:Embed(t); seq = seq + 1
    local rec = { t = t, seq = seq, raw = {}, keys = {}, want = {} }
    -- capture raw, stamp wrappers:
    --   Register: if down then remember() else raw(...) ; remember() end   (raw FIRST when up)
    --   Unregister / UnregisterAll: forget / forgetKind, then raw
    return t
  end
  function B:StandDown() --[[ if down return 0; down = true; raw UnregisterAll* per held ]] end
  function B:StandUp()   --[[ if not down or (d.isDown and d.isDown()) return 0, {};
                              down = false; replay in seq order, pcall each, drop + collect rejected ]] end
  return B
end

function lib.Catalog(addonName, messages) --[[ validate, copy, strict metatable ]] end
```

Note Lua 5.1's hidden `arg` local inside vararg functions (the kit calls this out in
`testkit/mock_base.lua` around `callbackFor`): name the stored optional argument anything but `arg`.

---

## 11. Test plan — `tests/test_bus.lua`

### Fixtures (`tests/fixture_bus.lua`)

- `F.newBus(overrides)` → `bus, rec`: a fresh `Bus:New{ name = "TestHost" }` (overrides merged) and a
  recorder of handler calls in order.
- `F.live(targets...)` → a sorted array of `"<i>:<kind>:<name>"` strings filtered from
  `T.mocks.__registrations()` to the given targets (`i` = the target's position in the argument
  list), so each case asserts only on its own targets even though the mock is shared by the run.
- `F.send(message, ...)` → fires through a raw AceEvent embed's `SendMessage`, so delivery is proven
  through the kit's CallbackHandler, not by calling handlers directly (`architecture-§4`'s
  real-dispatch MUST).
- `F.fire(event, ...)` → `T.mocks.__fire(event, ...)`, answering how many handlers ran.
- `F.withoutAceEvent(fn)` → runs `fn` with a `LibStub` that answers nil for `AceEvent-3.0` and
  delegates everything else, restoring it afterwards even when `fn` raises.
- `F.withBadEvents(set, fn)` → swaps `T.mocks.__badEvents` for the duration, restoring it.
- `F.CATALOG_CASES` → a data table of `{ label, addonName, messages, needle }` rows for the catalog
  refusals; the suite iterates it, one assertion per row naming the row.
- `F.latchedHost()` → a `LibKa0s-Lifecycle-1.0` latch whose `standDown`/`standUp` call
  `bus:StandDown()`/`bus:StandUp()`, with `isDown = function() return lc:IsDown() end`.

Every case below builds its state from these; none reaches into the bus's internals. Negative
assertions carry `testing-§12`'s falsification comment (`-- red under: ...`).

### Cases

| # | Case | Asserts | red under |
|---|---|---|---|
| B-01 | the major is registered, floors on Core, reports its file minor | `MODULES.Bus == MINOR` | — |
| B-02 | `New` refuses a descriptor without `name`, and a non-function `isDown` | raised text names the field | drop either guard |
| B-03 | `NewTarget` answers a fresh table per call | `a ~= b`; two receivers of one message on two targets BOTH fire through `F.send` | return a cached target |
| B-04 | the record follows every wrapper | register event + message, unregister one, `UnregisterAllEvents` leaves the message; `F.live` after a `StandDown`/`StandUp` round shows exactly the survivors | make `UnregisterAllEvents` forget both kinds |
| B-05 | `StandDown` actually unregisters, events AND messages | `F.live` empty for the targets; `F.fire` runs 0 handlers; `F.send` reaches nobody; answers the entry count | skip `UnregisterAllEvents` in StandDown (PFE's union vs AT/CM/MM's messages-only) |
| B-06 | `StandDown` keeps the record and `StandUp` replays it | handlers fire again after `StandUp`; `replayed` equals the count | clear the record in StandDown |
| B-07 | replay is from the record as it is NOW, not a snapshot | while down: unregister A, register B; after `StandUp` only B is live | snapshot the record at StandDown |
| B-08 | a registration made while down is recorded and NOT live | `F.live` empty while down; live after `StandUp` | call raw in the down branch |
| B-09 | `StandDown` and `StandUp` are idempotent | second `StandDown` answers 0 and changes nothing; `StandUp` while up answers `0, {}` | drop the `down` checks |
| B-10 | re-registering a key replaces the entry and does not duplicate it | register M with f1 then f2; after a round trip only f2 fires, once, and `replayed` counts one entry | append instead of replace (PFE defect 1) |
| B-11 | handler forms survive replay: function, method-name string, nil (method named for the event), `arg` form, explicit-nil `arg` | each fires after a round trip with the arguments CallbackHandler would pass (`arg` in front of the event name) | drop the arg or its count (`{ handler }`, MM). *[corrected]* `fn or false` (PFE) is NOT a red: CallbackHandler reads false as the event name |
| B-12 | a raw register that raises while up propagates and is not recorded | `F.withBadEvents`: the raise reaches the caller; after a round trip the bad event is not replayed and `rejected` is empty | record before the raw call |
| B-13 | one entry that raises on replay does not stop the others | record a bad event while down; `StandUp` answers the good entries replayed, `rejected == { "event:BAD" }`, does not raise, and the bus is up | drop the per-entry pcall |
| B-14 | a rejected entry is dropped from the record | a second round trip has an empty `rejected` | keep failing entries |
| B-15 | `StandUp` is refused while the host's latch is down | `isDown` answering true → `0, {}`, nothing live, a later permitted `StandUp` replays | drop the `isDown` check |
| B-16 | composed with Lifecycle: `Hold(disabled); Hold(perf); Release(perf)` leaves the bus down; `Release(disabled)` brings it up | `F.latchedHost`; `F.live` at each step | — (the seam, end to end) |
| B-17 | a target only CallbackHandler holds survives stand-down and GC | create in a closure, take it out of `AceEvent.embeds` (`F.releaseFromAce`, else the case passes whatever the bus does), drop every reference, `StandDown`, `collectgarbage("collect")` twice, `StandUp`, `F.send` fires it | weak-VALUE the held set. *[corrected]* A weak-KEYED set stays green: Lua 5.1 has no ephemerons and the record names its target |
| B-18 | an emptied target leaves the registry | `UnregisterAllEvents` + `UnregisterAllMessages`, `F.releaseFromAce`, drop the reference, collect; a weak probe table no longer holds it; `StandDown` answers 0 | never release |
| B-19 | two buses share nothing | `a:StandDown()` leaves `b`'s targets live | module-level state |
| B-20 | `SendMessage` on a tracked target is untouched | a tracked target can publish while its own receivers are down (reaches untracked receivers) | wrap SendMessage |
| B-21 | the bus prints nothing | `T.mocks.__printed()` unchanged across a full cycle | — |
| B-22 | AceEvent absent | `F.withoutAceEvent`: `NewTarget` answers nil, `StandDown` 0, `StandUp` `0, {}`, `Catalog` still works | resolve at file load, or raise |
| B-23 | `Catalog` accepts a conforming table and returns a fresh copy | same keys and values, `pairs` enumerates exactly them, not the input table, input unmutated | return the input |
| B-24 | `Catalog` refusals, data-driven over `F.CATALOG_CASES` | one row each: bad addonName; empty table; lowercase key; wrong prefix; another addon's prefix; SCREAMING_SNAKE suffix (`Ka0s_X_METER_UPDATED`); camelCase suffix; all-caps suffix without lowercase; duplicate value. Raised text names the key | drop the matching check |
| B-25 | the catalog is strict | reading an undeclared key raises naming it; adding a key raises; reading a declared key does not | drop the metatable |

Twenty-five cases. The count is a design target, not a measurement. *[corrected]* As built:
27 — B-01..B-25 plus "the major is absent without Core, and with a Core below its floor" and "the
documented degradation stub matches the live surface" (`T.assertSurfaceParity` over the §7 stub).
Every red-under above was run as a mutation against the built file (27 mutations); all went red
except the two this table now marks as not-a-red.

Gates the implementer runs, bounded: `/home/tushar/.claude/wow-addon/bin/ka0s-bounded lua tests/run.lua`
and `/home/tushar/.claude/wow-addon/bin/ka0s-bounded luacheck .`, both from the LibKa0s root; then
`lua tools/gen-api-members.lua` and `git ls-files --eol` on every new file.

---

## 12. Per-consumer adoption delta (Phase 6 checklist)

Common to every adopter: re-vendor the tag carrying Bus minor 1 (whole folder, CLAUDE.md provenance
line in the same commit); add the `LibStub("LibKa0s-Bus-1.0", true)` resolution and the §7 stub to
the bus file; add a `Kit.assertSurfaceParity(stub, "LibKa0s-Bus-1.0")` case; name the major in
`docs/ARCHITECTURE.md` → `## Message Bus`. Keep the host's seam **names** (`NS.NewBusTarget`,
`NS.BusStandDown`, `NS.BusStandUp`, `NS.MSG`) so modules and most tests do not move; their bodies
delegate. Log `StandUp`'s second return through the debug seam.

### Record half + Catalog (four repos)

**PartyFrameEnhanced** — the reference design moves upstream almost verbatim.
- `core/Bus.lua:19-23`: keep (the `NS.bus` publisher).
- `core/Bus.lua:25-133`: replace the hand-written record with
  `NS.busRecord = Bus:New{ name = addonName, isDown = function() return NS.IsStoodDown() end }`
  and three one-line delegates (`NS.NewBusTarget`, `NS.BusStandDown`, `NS.BusStandUp`). The rewrite
  also removes the four lines of double-encoded mojibake at :25, :34, :36, :110.
- `core/Bus.lua:135-140`: `NS.MSG = Bus.Catalog(addonName, {...})` (all four names already conform).
- `core/PartyFrameEnhanced.lua:155`, `:166`: unchanged (names kept). Order already puts the bus up
  before any module registers (`:166` before `each("Resume")` at `:172`), so the new while-down
  deferral changes nothing here.
- `NS.IsStoodDown` is defined in `core/LifecycleSetup.lua:83`, after `core/Bus.lua` loads; the
  closure resolves it at call time.
- Tests: the twelve suites that call `NS.NewBusTarget()` keep working; audit `tests/test_bus.lua` for
  probes that should be emptied (§9.3).

**MultiMeters**
- `core/Namespace.lua:168-253`: replace with the delegates. *[corrected]* There is no weak-key loss
  to fix (§1 defect 2): AceEvent's `embeds` already holds `settings/Profiles.lua:121`'s target.
- `core/LifecycleSetup.lua:159`: **move `NS.BusStandUp()` to the first line of `standUp`**, ahead of
  `NS:OnEnable()` at `:151`. Under the library, a registration a module's `OnEnable` makes while the
  bus is still down is deferred until `StandUp`; anything published before that point would reach
  no receiver. Verify with `tests/test_lifecycle.lua` and `tests/test_disabled.lua`.
- `modules/Window.lua:1354-1358` (`UnregisterBus`): unchanged; emptying the record releases the
  target.
- `Catalog`: **blocked on the owed wire rename** (debt row 9+13): rename the fourteen wire strings in
  `core/Constants.lua:519-559` to PascalCase first (subscribers read constants, so the rename is
  behavior-preserving), then `Constants.MSG = Bus.Catalog("MultiMeters", {...})` at `:515`.

**AbsorbTracker**
- `core/Bus.lua:43-47`, `:65-85`: replace with the delegates. Delete `NS.BusSubscribe`,
  `NS.BusUnsubscribeAll`, `NS.BusResubscribeAll`; the five subscription sites become plain
  `target:RegisterMessage(...)`: `core/AbsorbTracker.lua:362`, `modules/Timer.lua:81`,
  `modules/Display.lua:439`, `:442`, `:445`. Update the comments above each that name `BusSubscribe`.
- `core/Lifecycle.lua:104` → `NS.BusStandDown()`, `:112` → `NS.BusStandUp()`. Order is already
  bus-first on the way up.
- `isDown` → `NS.IsStoodDown` (`core/Lifecycle.lua:196`).
- `core/Bus.lua:88-94`: `NS.MSG = Bus.Catalog(addonName, {...})` (all five conform).
- Tests: `tests/test_disabled.lua:113`'s comment names `NS.BusUnsubscribeAll`; the return-value
  meaning is kept (a count), so any assertion on it survives the rename.

**ConsumableMaster**
- `core/Bus.lua:50-76`: keep the `KCM.NewBusTarget(subscribe)` signature as a shim:
  `local t = KCM.busRecord:NewTarget(); if type(subscribe) == "function" and t then subscribe(t) end; return t`.
  `KCM.Bus.StandDown` / `KCM.Bus.StandUp` delegate. Behavior change: stand-up replays the recorded
  handlers instead of re-running the closures; the four closures (`core/Bus.lua:95`,
  `modules/MacroBar.lua:587`, `settings/OptionsShim.lua:263`, `settings/Profiles.lua:119`) register
  unconditionally, so the registration set is identical. A target made **without** a closure is now
  tracked too — the survivor `core/Bus.lua:45-46` warns about stops being possible.
- `isDown` → `KCM.IsStoodDown` (`core/LifecycleSetup.lua:135`).
- `core/Bus.lua:78-84`: `KCM.MSG = Bus.Catalog(addonName, {...})` (all five conform).
- `core/LifecycleSetup.lua:73`, `:111`: unchanged.
- Tests: `tests/test_bus.lua:23`, `:65`, `:76`, `:87` build closure-less targets that were
  deliberately untracked (`core/Bus.lua:48-49`); they are now tracked. Empty them or accept that a
  later stand-down case sees them (§9.3).

### Catalog only (five repos)

**AuraMaster** — `core/Bus.lua:30-47`: `NS.MSG = Bus.Catalog(addonName, {...})` (all four conform).
The factory `:21-25` stays untracked: its receivers already stand down by hand, per module
(`modules/ContainerManager.lua:557-563`, `modules/TimedSpells.lua:165-168`), and the settings target
(`settings/OptionsSetup.lua:395`) is setup that survives. Adopting tracked targets here would be a
second mechanism beside a working first one; not recommended.

**BankLedger** — owes the declare-once table (debt row 9+13). Declare `NS.MSG` for the four messages
(`EntryAdded`, `LedgerChanged`, `SessionChanged`, `SettingsChanged`, all already PascalCase) in
`core/Constants.lua` through `Catalog`, then replace the 25 literal lines across 9 files:
`core/Database.lua:106`, `:569`; `core/Util.lua:208`; `modules/Browser.lua:1212-1214`;
`modules/SessionWindow.lua:662`, `:665`, `:668`, `:669`; `modules/Insights.lua:1000-1001`;
`modules/Ledger.lua:510`, `:888`; `settings/Schema.lua:40`, `:48`, `:55`, `:72`, `:85`, `:225`, `:239`;
`settings/Slash.lua:195`; `settings/Panel.lua:170`, `:171`, `:493`. Factory `core/BankLedger.lua:20-26`
and the rebuild teardown `:121-182` stay.

**LootHistory** — owes the table (debt row 9+13). `NS.MSG` for `RecordAdded`, `HistoryChanged`,
`SettingsChanged` in `core/Constants.lua` through `Catalog`; replace the 20 literal lines across 6
files: `core/Database.lua:265`, `:292`, `:706`; `modules/Analytics.lua:666`, `:668`;
`modules/Browser.lua:1229`, `:1230`, `:1240`; `modules/Collector.lua:228`; `settings/Panel.lua:159`,
`:169`, `:492`; `settings/Schema.lua:159`, `:171`, `:177`, `:183`, `:267`, `:275`, `:282`, `:293`.
Factory `core/LootHistory.lua:20-26` stays.

**KickCD** — owes both halves (debt row 9+13), sequenced: constants first, rename second. Declare
`NS.MSG` for the five messages (`COMBAT_STATE`, `CONFIG_CHANGED`, `GRID_LAYOUT`, `PROFILE_CHANGED`,
`SPELL_STATE`) **with their current wire strings** as a plain table and sweep the 23 literal lines
across 8 files (`core/Database.lua:44`, `core/State.lua:171`, `modules/Cooldowns.lua`,
`modules/IconGrid.lua`, `modules/UnitLabel.lua`, `modules/Castbar.lua`, `settings/Panel.lua:154`,
`settings/Spells.lua:1337`, `:1345`); then rename the wire strings to PascalCase in the one table and
wrap it in `Catalog` (which refuses the SCREAMING_SNAKE forms, so the wrap cannot land before the
rename). Factory `core/KickCD.lua:46-52` stays; KickCD's receivers are AceAddon modules and need no
record.

**PanelMaster** — compliant today by the module-scoped shape; not debt. Optional: wrap each owning
module's constants (`modules/Registry.lua:19-20`, `settings/Schema.lua:31`) in `Catalog` for the
strict read. Factory `core/PanelMaster.lua:20-26` stays.

---

## 13. OPEN — where the standard's text and this design pull apart

- **OPEN-1. `architecture-§4` says "no new lib needed".** Its closing line reads "Implementation:
  AceEvent-3.0's :SendMessage/:RegisterMessage (already in the addon); no new lib needed." Reading A:
  that line is about the ecosystem (no lib beyond AceEvent), and Bus still is AceEvent, so nothing
  conflicts. Reading B: the line says the bus needs no library, and a LibKa0s major for it
  contradicts it. This design takes reading A. The upstream ripple (not done here) should name
  `LibKa0s-Bus-1.0` as the stand-down record for tracked receivers and keep `NS.NewBusTarget` as the
  untracked host factory, so the two stop reading as rivals.
- **OPEN-2. "Fails at once" is only true for subscribers.** `architecture-§4`'s declare-once
  rationale claims a mistyped constant fails at the call site. For `SendMessage` it does not
  (CallbackHandler `Fire` returns quietly on a nil event). Reading A: the rule is right and the
  rationale overclaims; `Catalog`'s strict read makes the claim true. Reading B: the rule should
  also require the strict read. This design ships the strict read and leaves the rule's wording to
  the upstream decision.
- **OPEN-3. The panel's live-refresh subscription: setup or feature?** `slash-commands-§7` lists
  "the settings-category registration and the panel body" as survivors and "every event, message
  and bucket registration" as what goes. BankLedger (`core/BankLedger.lua:136-139`), LootHistory and
  AuraMaster keep the panel's receiver live; ConsumableMaster (`settings/OptionsShim.lua:255-262`,
  arguing its publishers are all stood-down paths) and MultiMeters (`settings/Profiles.lua:121`) take
  it down. The design does not decide: a host picks by choosing the tracked factory or its own
  untracked one. Upstream could settle it in `slash-commands-§7`'s survivor list.
- **OPEN-4. Release placement.** The unreleased v1.55.0 `CHANGELOG.md` entry says "No library file
  changes at all — every major's version key and every file's LibStub minor are exactly v1.54.2's".
  Landing Bus in v1.55.0 makes that sentence false and turns a kit-only release into a payload
  release for eleven consumers. Reading A: fold Bus into v1.55.0 and rewrite the entry. Reading B:
  ship v1.55.0 as the kit-only release the five v2.63.0 commencement clauses name, and Bus in the
  next minor. The orchestrator's call; reading B is the smaller blast radius.
- **OPEN-5. Upstream counts.** `library-stack-§7`'s module table and its "twelve LibStub majors
  across eighteen files", the "eleven of the twelve majors need Core" / "seven of those eleven"
  figures, and `open-evolutions.md:13`'s candidate list all move when Bus ships (Bus floors on Core
  without calling it). Per that section's own instruction they are recounted from
  `tests/majors.lua`, not incremented, and the edit is upstream in WowAddonStandards.
