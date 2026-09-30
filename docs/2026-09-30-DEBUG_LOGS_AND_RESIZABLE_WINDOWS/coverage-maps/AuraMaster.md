# AuraMaster: 060 debug-coverage map (DL-AM-02)

Audited against debug-logging v2.70.0 §8 (flows and the Diagnosis checklist) and §9 (coalescing and
the quiet steady state). Repo commit: `f2ef059` on `feat/2026-09-30-debug-logs-and-resize`. Line
numbers are at that commit.

Gate at the commit: `lua tests/run.lua` 1765 passed / 0 failed / 0 skipped (was 1756; 9 new cases);
`luacheck .` 0 / 0; lizard: no function over CCN 15. The touched ones peak at CCN 15:
`initSummary` (`core/DebugLogSetup.lua`) and `standUp` (`core/LifecycleSetup.lua`), both at the limit.

## S4.1 Inventory, and S4.2/S4.3 gap -> action

### Events and state edges

| Inventory item | Where | Existing line (before) | Gap | Action |
|---|---|---|---|---|
| `PLAYER_ENTERING_WORLD` | `core/AuraMaster.lua` `OnEnterWorld` | `[Event] PLAYER_ENTERING_WORLD secret= lockdown= queued= login= reload=` | none | kept |
| `LOADING_SCREEN_DISABLED` | `OnLoadingScreenEnd`, `modules/FontPrimer.lua` | `[Event] ...` plus `[Fonts] PLAYER_ENTERING_WORLD at X, loading screen ended at Y` or `loading screen ended at Y, no PLAYER_ENTERING_WORLD before it` | none. The known 060 observation (LSD with no PEW before it) is one line per loading screen, a real edge carrying timing | **kept on purpose**: one line per edge, not steady state |
| `PLAYER_REGEN_DISABLED` / `_ENABLED` | `OnCombatChanged` | `[Event] PLAYER_REGEN_...` | the state taken is in the `[Apply]` line after it, which repeated per edge (below) | `[Event]` kept; the `[Apply]` line fixed |
| `ADDON_RESTRICTION_STATE_CHANGED` | `OnRestrictionChanged` | `[Event] ... type= active=` | as above | kept |
| Target / focus / pet swaps, `ADDON_LOADED`, `ITEM_DATA_LOAD_RESULT`, `GET_ITEM_INFO_RECEIVED` | `core/AuraMaster.lua` | none (owner decision 2026-09-29) | none, by decision | **kept out**; their effects log (enchant reset, anchor resolve) |
| Group roster, spec change | not registered | - | the addon does not react | none needed |
| Addon stand-down / stand-up (Lifecycle latch: `disabled`, `perf`) | `core/LifecycleSetup.lua` `standDown` / `standUp` | none | **gap**: a report of "nothing shows" with the addon disabled or perf-suspended left no trace | **added** `[State] stood down: events and timers off, containers hidden (holds: …)` / `stood up: … (holds: none)` (`:124`, `:151`, via `traceEdge` `:63`) |
| Test mode (session state) | `modules/Preview.lua` `SetTestMode` | checkbox path only: the session row's `[Set] state.testMode = …` | **gap**: `/am test`, the launcher and combat ending it wrote nothing | **added** `[Preview] test mode on|off (<who>)` for callers outside the seam (`:43`); the checkbox passes no `why`, so no second line beside its `[Set]` (§10) |
| Profile switch / reset / copy | `core/AuraMaster.lua` | `[Profile] changed -> X`, `[Set] reset profile …`, `[Set] copied profile …` | none | kept |

### Deferred work

| Inventory item | Existing | Gap | Action |
|---|---|---|---|
| Apply queue held (combat lockdown, aura secrecy) | `[Apply] deferred: secret= lockdown= edge=` on **every** flush that held (`noteDeferred`) | **§9 violation**: in a key the same hold wrote one line per combat end and per restriction flip (the real-key-log observation) | **fixed**: `traceHold` (`modules/ContainerManager.lua:233`) writes once per hold and again only when secrecy, lockdown or the queue changes; the line gains `queued=`. The gate state resets when a flush may run (`:354`) and at stand-down (`:809`). The flush is the existing `[Apply] applied N container(s)` |
| Stand-down's secure half held by combat | none | **gap**: a held-then-never-finished stand-down was invisible | **added** `[State] stood down: …; hiding held until combat ends` (`:127`) and `stand-down finished after combat: …` (`:99`) |
| Frame-attach resolve under lockdown | `[Anchor] pending resolve skipped under lockdown; retried when combat ends` on every call | written on every `ADDON_LOADED` in combat, even with nothing pending; no flush line | **fixed**: once per fight and only while something waits (`modules/Anchors.lua:358`); **added** `resolved N pending frame target(s), M still pending` when a resolve attaches one (`:381`) |
| Blizzard-frame toggle under lockdown (`hideBlizzardBuffs` / `hideBlizzardDebuffs`) | `[Apply] deferred: secret=false lockdown=true …` through `CM.NoteDeferred` (`settings/General.lua:86`) | **gap**: the regen `BlizzardFrames.Apply()` (`core/AuraMaster.lua:150`) wrote nothing and `FlushPending('regen')` is idle, so the hold had no flush line (review round 1) | **added** `[Apply] Blizzard frames applied after combat` (`modules/BlizzardFrames.lua:63`), written only after `BF.NoteHeld` (`settings/General.lua:85`) marked a hold |
| Class-stale re-apply, enchant reset, font refresh | covered by `[Apply] applied`, `[Apply] enchants reset …`, `[Fonts] …` | none | kept |
| Coalescing timer (0 s) | none | a one-frame coalesce, not held work | **left**: its pass is the `applied` line |

### Refusals and no-ops

| Inventory item | Existing | Gap | Action |
|---|---|---|---|
| `CM.Create` in combat (panel New/Duplicate, `/am new`) | gray chat line only | **gap** | **added** `[Containers] create refused (in combat)` (`modules/ContainerManager.lua:589`) |
| Delete in combat (`/am delete`, the delete popup) | chat only | **gap** | **added** `[Containers] delete refused (in combat)` (`settings/Slash.lua:307`), `delete <id> refused (in combat)` (`settings/Containers.lua:142`) |
| Attach popup in combat | chat only | **gap** | **added** `[Anchor] attach refused (in combat)` (`settings/Layout.lua:143`) |
| Frame pick in combat | chat only | **gap** | **added** `[Anchor] frame pick refused (in combat)` (`modules/FramePicker.lua:144`) |
| Test mode start in combat | chat only | **gap** | **added** `[Preview] test mode refused (in combat)` (`modules/Preview.lua:37`) |
| Test mode checkbox start while disabled (host guard) | the dispatcher's `DisabledLine` in chat; the seam's `[Set] state.testMode = true` recorded a value never stored | **gap** (review round 1: this guard is host code, not LibKa0s-Slash's) | **added** `[Preview] test mode refused (addon disabled)` (`settings/General.lua:125`); the `[Set]` line after it is the request |
| `NS.OpenOptionsPage` in combat | chat only (the library's own open logs `[Cfg] open refused (in combat)`) | **gap** on the host's page-open path | **added** `[Cfg] open <page> refused (in combat)` (`settings/OptionsSetup.lua:363`), the library's shape |
| A write the seam refuses | nothing (a test pinned "logs nothing") | **gap**: "the setting did not change" had no answer in the log | **added** `[Set] <path> refused: <reason>` at `NS.SetByPath` (`settings/Schema.lua:895`; the body moved to a local `write`). `NS.CheckWrite` stays silent: it is a probe |
| A refused `CopyFrom` | nothing (pinned "logs nothing") | **gap** | **added** `[Set] copy <scope> refused at <key>: <reason>` (`modules/ContainerManager.lua:682`) |
| The disabled-state verb refusal (`/am test`, `/am profile`), `/am profile` in combat | LibKa0s-Slash's own chat lines | library-owned | **left**: library surface (no host seam); a library-side debug hook is a LibKa0s follow-up |
| Text template refused | `[Style] text template refused, drawing the default` once per template | none | kept |
| Anchor position read secret on drag | `[Anchor] container N: position reads secret, not saved` | a user action, one per drag | kept |

### Dependencies (once at enable)

| Item | Existing | Action |
|---|---|---|
| LibKa0s missing | no console at all; chat says so once | kept |
| LibSharedMedia-3.0 (optional; the #24 font bug lives here) | none | **added** to `[Init]`: `, LibSharedMedia-3.0 missing (media-pack fonts and textures fall back)` (`core/DebugLogSetup.lua:107` `initNotes`) |
| Aura container API | chat line at login only (flag off then) | **added** `, no aura container API (containers are not drawn)` |
| Stood down at enable | none | **added** `, stood down (holds: …)` |
| Rejected events | `, rejected events: …` | kept |

A healthy session's `[Init]` line is unchanged, so the existing pin still holds (with an LSM stand-in).

### Errors caught by our pcalls

| Site | Existing | Gap | Action |
|---|---|---|---|
| `callEngine` (`modules/Container.lua:34`) | `[Engine] M failed: …` on every failure | **§8/§9**: a refresh runs on every target swap | **fixed**: `NS.DebugOnce` (`core/DebugLogSetup.lua:23`), once per tag + site + first line, gated first |
| `Style.Bind` (`modules/Style.lua:524`) | a line per failed binding | per button per restyle | **fixed**: `NS.DebugOnce` |
| `Style.ReportError` (`modules/Style.lua:540`) | a line per failure, by design (a test pinned 15 lines for 3 restyles of 5 frames) | per-item wall | **fixed**: once per distinct error; the error-handler dedupe is unchanged |
| `applyDirty`'s xpcall (container apply) | error handler only, no log line | **gap**: BugSack had it, a pasted log did not | **added** `[Apply] container #<id> failed: <first line>` via `NS.DebugOnce` (`modules/ContainerManager.lua:304`) |
| Secret-probe pcalls (`UnitExists`, `UnitIsFriend`, the aura reads in EmptyWatch/TimedSpells/Diagnostics) | none | expected refusals, not faults | **left**: logging a secret read's refusal is noise; Diagnostics sections have their own `section … failed` |

### Data mutations and the settings seam

| Item | Existing | Action |
|---|---|---|
| `[Set] <path> = <value>` at the seam, section writes, bulk acts | present | kept |
| Container create / delete | `[Containers] created` / `deleted` | kept |
| User categories create / rename / delete / canonicalize / forget | `[Set] user category …` | kept |
| Timed spells learned / forgotten | `[Timed] learned N`, `forgot N` | kept |
| Migrations, seeding | `[Migrate] …` | kept |

### Slash verbs

Every verb reaches a logged seam: `set/reset/resetall/enabled/lock` (the Set seam), `new/delete`
(`[Containers]`), `profile` (`[Profile]`), `test` (`[Preview]`, new), `resetposition` (bulk
`[Set]`), `forgettimed` (`[Timed]`), `redraw` (`[Apply]`), `debug`/`diagnostics` (the library).
`select`, `containers`, `get`, `list`, `version`, `help` are read-only or one integer of view state:
no line (§10 named non-setting state).

### Repeating paths (§9 quiet steady state)

| Path | Before | After | Test |
|---|---|---|---|
| Apply-queue flushes during a hold (every combat end in a key, each restriction flip) | one `deferred:` line per edge | once per hold, again on change | `coverage: a held apply is traced once while the hold lasts, …` (8 regen flushes + 1 timer flush -> 1 line) |
| `Anchors.Place` screen fallback (every apply pass, every follower re-place, every `ADDON_LOADED` at login) | a line per placement | once until the container lands | `anchors: a fallback and a lockdown skip are traced once while they last, …` (10 places + 10 ADDON_LOADED -> 1 line) |
| `Anchors.ResolvePending` under lockdown | a line per call, pending or not | once per fight while something waits | same test (5 skips -> 1 line; 0 lines with nothing pending) |
| `FontPrimer` priming (every settings write, every Announce) | `N font(s) refused` on every pass with a refusal | only when the count moves | `fontprimer: one Fonts debug line when the refused count moves, …` (10 passes -> no new line) |
| Guarded style/engine calls (restyle of every button, refresh per swap) | a line per failure | once per distinct error | `container: a re-dress that raises is reported, a debug line and the client's error handler once per message` (15 -> 2); `text style: … the debug log once` (3 -> 1) |
| EmptyWatch pass (UNIT_AURA, 0.2 s), TimedSpells scan (UNIT_AURA, 0.5 s), FramePicker `OnUpdate` | silent (TimedSpells logs only when it learns) | unchanged | already quiet; not re-pinned |
| `[Apply] applied N container(s)` per coalesced pass | per real apply | unchanged | a real recompute on each pass (§9: stays compliant) |

## S4.4 Tests

`tests/test_debug_coverage.lua` (new, 8 cases, each with a red-under comment): the hold's quiet
steady state and its re-arm; the gate's memory never written with logging off; a container apply
error once per distinct error; every combat refusal naming its guard; test mode's switch naming who
switched it and the checkbox path writing no second line; the `[State]` stand-down / stand-up with
holds; the combat-held secure half and its finish; the `[Init]` notes. Plus the new anchor
quiet-steady-state case. Updated to the rule (the old pins asserted the behavior §8/§9 now forbid):
`schema paths: a refused write … logs one refusal line naming the guard`, `bulklog: a refused
CopyFrom writes no row and logs one line naming the refused key`, the `container:`/`text style:`
per-failure pins, and the font-primer refused-line pin (now with its 10-pass quiet check). Tests that
record the sink turn `NS.State.debug` on, since the new gates sit in front of the sink.

## S4.5 Docs

`docs/debug.md` gains `## Coverage` (tag -> what writes it -> when, plus what is left out on purpose),
and its event-trace and font-primer paragraphs describe the change-gated lines. `docs/data-flow.md`
and `docs/midnight-quirks.md` follow. `docs/module-map.md` lists the new suite. Moved `file:line`
citations re-pointed in the live docs (ARCHITECTURE, common-tasks, data-flow, midnight-quirks,
module-map, performance, schema, scope, slash-dispatch, DEPENDENCIES); `docs/test-cases.md`
regenerated, README badge 1765/1765.

## Deliberately left, and why

- **Target/focus/pet swaps, `ADDON_LOADED`, item-data events**: owner decision (2026-09-29), fires
  too often in a key; their effects log.
- **The `[Event]` line on every combat edge**: one line per edge is what §8's state-edge bullet asks
  for; it is not a steady-state repeat. What repeated was the `[Apply]` line after it, now fixed.
- **TimedSpells and EmptyWatch gate open/close**: the `[Event]` combat/restriction lines already mark
  the edge, and neither changes what a player sees except through the apply/visibility lines.
- **Library-owned refusals** (the disabled-state verb refusal of `/am test` and `/am profile`, `/am profile`
  in combat): LibKa0s-Slash owns them and exposes no host hook; a library change, out of scope here.
  The Master controls checkbox's own disabled guard (`settings/General.lua:122`) is host code and
  logs `[Preview] test mode refused (addon disabled)` (review round 1).
- **Tag vocabulary**: two tags are new to this addon, `State` (the stand-down edges; the tag the
  standard's §8 example and most siblings use) and `Preview` (test mode). No existing tag named
  either subject.
