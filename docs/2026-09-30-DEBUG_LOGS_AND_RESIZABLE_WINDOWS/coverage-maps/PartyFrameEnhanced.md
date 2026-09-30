# PartyFrameEnhanced: debug coverage map (DL-PF-02)

Audited against debug-logging v2.70.0 §8 (flows + Diagnosis) and §9 (coalescing + quiet steady
state). Repo commit `082ed15` on `feat/2026-09-30-debug-logs-and-resize`. Gate: 406/406 tests,
luacheck 0/0, lizard 0 functions over CCN 15 (initSummary is the highest one touched, at 14).

Format: inventory item -> existing line -> gap -> what was done.

## Lifecycle and state edges

| Inventory | Existing line | Gap | Done |
|---|---|---|---|
| OnInitialize / OnEnable (PLAYER_LOGIN) | `[Init]` from the library when logging goes on | Optional dependency not named anywhere | `[Init]` summary gains `EllesmereUI raid frames loaded\|not loaded` (core/DebugLogSetup.lua). The flag is off at login, so the summary is the only at-enable line that can land |
| Migration runner (core/Database.lua) | `[Migrate]` per step; failure ungated | none | kept |
| Stand-down (NS.StandDown, both holds) | none | §8 own enable/stand-down edge | `[State] stood down (holds: <keys>), N secure write(s) held`, logged at the END so it counts the driver releases the Suspend hooks queue |
| Stand-up (NS.StandUp) | none | same | `[State] stood up, N secure write(s) held` |
| PLAYER_ENTERING_WORLD (OnEnterWorld) | none | §8 loading screen edge | `[State] entered world: in a party\|not in a party` |
| GROUP_ROSTER_UPDATE (OnRosterUpdate) | `[Party]` only when the party answer flips | none (already change-gated) | kept |
| PLAYER_REGEN_DISABLED (OnEnterCombat) | none | §8 combat-in edge | `[Combat] entered: secure writes queue until it ends` |
| PLAYER_REGEN_ENABLED (OnLeaveCombat) | `[Combat] left: <rollup>` | none | kept; rollup gains `targetEvents` |
| ADDON_ACTION_BLOCKED / FORBIDDEN | `[Secure]` ungated, ours only | none | kept |
| ADDON_RESTRICTION_STATE_CHANGED, spec change | not registered | none (no edge the addon reacts to) | nothing |

## Deferred work

| Inventory | Existing line | Gap | Done |
|---|---|---|---|
| NS.RunSecure queue (combat lockdown) | `[Secure] queued %s` on EVERY write | §9 quiet: a re-sort in combat re-queues the same `anchor:<key>` pass many times a fight; also no reason named | Logged once per key, when it is first held: `queued <key> (combat lockdown, N held)`. A replacing write is silent |
| flushSecure (regen, stand-up, stood-down regen watcher) | `[Secure] flushed N deferred write(s)` | none | kept (a hold line with no flush line after it is the evidence) |
| Providers next-frame / burst resolve (C_Timer) | `[Provider]` only on a changed map | none | kept |
| Options register parked in combat | library `[Cfg]` | none | kept |

## Refusals and no-ops

| Inventory | Existing line | Gap | Done |
|---|---|---|---|
| Unlock refused (NS.AcceptLock): combat, disabled, perf suspend | chat only | §8 refusal names the guard | `[Preview] unlock refused: in combat\|addon disabled\|perf run suspended` |
| NS.ToggleLock while disabled | chat only | same | `[Preview] lock toggle refused: addon disabled` |
| Cast bar hidden while casting | `[Cast] ... casting but hidden: <rung>`, once per reason | none | kept |
| Anchor pass that moved nothing | silent | none (correct no-op) | kept |
| Schema write refused (validate/normalize) | none: library seam | a refused write logs nothing | left: the library's Schema seam owns it, and the addon's schema test pins "logs nothing" as the adopted contract (debug-logging-§10: a refusal is not a mutation). Candidate for a next-LibKa0s residual |
| Slash disabled gate | chat only, from the library dispatcher | the host never sees the refused verb | left: library-owned (next-LibKa0s residual) |
| profile verbs' refusals (missing name, self-copy) | chat only | minor | left: the reply is the whole reaction and no state moved |

## Data mutations

| Inventory | Existing line | Gap | Done |
|---|---|---|---|
| Every setting write | `[Set]` from the library seam | none | kept |
| Profile switch / reset / copy | `[Profile]` / `[Set]` | none | kept |
| Profile delete (Profiles page, `/pfe profile delete`) | none | §8 data mutation | `OnProfileDeleted` registered in InitDB, `[Profile] deleted '<name>'` |
| Free-placement drag (Anchor.SavePosition) | none (the pass line may follow) | geometry: MAY | `[Anchor] <key> dragged to <point> x, y` |
| `/pfe resetposition` (Anchor.ResetPositions) | none | geometry reset: MAY | `[Anchor] positions reset to default (N feature(s))` |

## Dependencies and caught errors

| Inventory | Existing line | Gap | Done |
|---|---|---|---|
| EllesmereUI / EllesmereUIRaidFrames present | none | §8 dependency, once at enable | in `[Init]` (above) |
| ADDON_LOADED for EllesmereUI after us | none | late dependency | `[Provider] <name> loaded after us: re-resolving` (fires once per addon) |
| EditMode.Exit RegisterCallback pcall (Providers) | swallowed | §8 error caught, once per distinct error | `[Provider] EditMode.Exit register\|unregister failed: <err>`, deduped by message |
| Migration step pcall | `[Migrate] vN failed` ungated | none | kept |
| StandIn getter pcalls | none | the result shows as `from fallback` in the stand-in line | left |
| core/Compat.lua secret guards, Util LSM fetch pcall | none | none: they fail by design on a secret / a missing key | left (logging would log the secret) |
| SafeRegister* refusals | `/pfe status`, diagnostics `events` | no console line at refusal | left: registrations run mostly at login with the flag off, and the list is deduped; status and the report name them. `[Bus]` covers the stand-up replay |

## Repeating paths (§9)

| Path | Before | After | Test |
|---|---|---|---|
| CastBars OnUpdate | silent | silent | (existing) |
| TargetFrames health ticker | silent per tick; start/stop edges | unchanged | (existing) |
| UNIT_TARGET / PLAYER_TARGET_CHANGED | `%s targets %s` every event | change-gated per button on the stringified name | `coverage quiet: repeated UNIT_TARGET ...` |
| UNIT_PET | `%s pet: %s` every event | change-gated per button | `coverage quiet: repeated UNIT_PET ...` |
| Pet UNIT_HEALTH / NAME_UPDATE, RAID_TARGET_UPDATE, UNIT_IN_RANGE_UPDATE, SetAlpha hooks | silent | silent | n/a |
| Providers resolve (hooks, bursts) | change-gated | unchanged | (existing) |
| Anchor pass | only when moved/faded | unchanged | (existing) |
| Secure queue in combat | every write | once per key | `coverage: a secure write queued in combat ...` |
| Preview stand-in on every GROUP_ROSTER_UPDATE out of a party | every roster update | change-gated, reset on lower (once per raise) | `coverage quiet: previewing out of a party ...` |
| RangeFade update (LAYOUT/VISIBILITY/PROFILE/CONFIG) | no line | new `[Fade]` mode line, change-gated | `coverage quiet: the range fade ...` |
| UnitButtons driver set/released | per button, memo-gated on the driver string | unchanged | n/a |

## Deliberately left

- **Per-button `[Secure] driver` lines** (UnitButtons). They are change-gated by the driver memo, and
  a stand-down writes up to ten. Each carries the driver string a support read needs, so they were
  kept rather than folded into a count.
- **`[Cast] <unit> interrupted|failed`**, one per interrupt. Each line is a distinct event whose
  content changes, and the `[Combat]` rollup counts them too.
- **The first `[Fade]` line after logging goes on.** The change gate is behind the flag (§9: with
  logging off nothing is built or compared), so the first update after `/pfe debug on` states the
  current mode once. tests/test_schema.lua's exact-trace helper now records only `[Set]` lines,
  because a General write reaches RangeFade.
- **Secret-to-secret target changes.** Two secret target names in a row both read `<secret>`, so the
  second is not logged. `targetEvents` in the `[Combat]` rollup counts every event.
- **Library-owned refusals** (the slash disabled gate, a refused schema write): they need a
  LibKa0s change, not a host line.
