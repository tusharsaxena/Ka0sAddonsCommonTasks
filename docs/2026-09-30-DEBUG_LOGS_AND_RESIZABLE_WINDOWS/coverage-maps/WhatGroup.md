# WhatGroup — 060 debug-coverage audit (DL-WG-02)

Audited against debug-logging v2.70.0 §8 (flows + Diagnosis checklist) and §9 (coalescing + quiet
steady state). Repo: `WhatGroup`, branch `feat/2026-09-30-debug-logs-and-resize`. Line numbers are
the post-change tree unless marked "old".

Gate after the change: 869 passed / 0 failed / 0 skipped (was 846); luacheck 0/0; lizard 0 functions
over CCN 15 (every touched function stays at or under its old CCN; highest touched is the LFG
status handler at 13, unchanged).

## S4.1 Inventory

### Events registered

| Event / hook | Where | Existing line | Gap | Done |
|---|---|---|---|---|
| `GROUP_ROSTER_UPDATE` | `core/WhatGroup.lua` `registerFeatureEvents` | `[Roster]` on transitions only | none (already change-gated) | kept |
| `LFG_LIST_APPLICATION_STATUS_UPDATED` | same | `[LFG] appID status` per event; `[LFG] dropped …` | "applied" with no capture was silent | added `[LFG] appID=… applied: nothing captured under result id=… to pair` |
| `PLAYER_REGEN_DISABLED` / `_ENABLED` → `OnCombatStateChanged` | same | none | combat edge: the gate's effect, the drain, not logged | the popup transition line (below) names the edge; the drain logs its flush |
| `PLAYER_REGEN_ENABLED` → `OnDisabledCombatEnded` (stand-down's one kept registration) | `NS.StandDown` | none | the owed Hide's settling invisible | `FrameFinishStandDown` logs `popup soft-hidden, Hide owed → hidden: combat ended, addon stood down` |
| `hooksecurefunc(C_LFGList, "ApplyToGroup")` | file load | `[Apply] id=… captured …` | stood-down return silent | `[Apply] ignored id=…: addon stood down` |
| EventRegistry `SetItemRef` callback / degraded `SetItemRef` post-hook | file load | `[ChatLink] clicked hasPending=…` | degraded stood-down return silent | `[ChatLink] ignored: addon stood down` (guard moved after the "is it ours" tests so other addons' links stay silent; behavior identical) |

### State edges (§8 Diagnosis)

| Edge | Reacts? | Existing | Gap | Done |
|---|---|---|---|---|
| Combat in/out | yes (test-mode end, combat-end drain, visibility gate) | `[Test] test mode off (combat)` only | gate effect + drain unlogged | `[Frame] popup <before> → <after>: combat started/ended, visibility=…` only when the popup's state moved; `[Frame] combat ended: flushing N held (…)` |
| Addon stand-down / stand-up (Lifecycle latch) | yes | `[Set] enabled = …` (the write, not the edge); `[Capture] wiped (addon stood down)` if in flight | edge itself, and which hold, unlogged (the Lifecycle major logs nothing) | `[State] stood down (holds: …)` first in `NS.StandDown`; `[State] stood up: events and the chat link re-registered` |
| Group roster | yes | `[Roster]` | none | kept |
| Loading screen / zone / instance, spec, `ADDON_RESTRICTION_STATE_CHANGED` | no | — | not applicable | none (documented in `docs/debug.md` "What stays quiet") |

### Deferred work (§8 Diagnosis)

| Deferral | Hold line before | Flush line before | Done |
|---|---|---|---|
| Combat-end queue `firstShow` (ShowFrame in combat, unbuilt popup) | chat only | none | `[Frame] held until combat ends: firstShow (in combat)` on empty→queued; `[Frame] combat ended: flushing N held (…)` in `NS.FrameDrainCombatEnd` |
| Combat-end queue `teleport` (secure configure in combat) | none | none | same two lines (`teleport` key) |
| Queue dropped by stand-down | — | none (silent `wipe`) | `[Frame] dropped held work: … (addon stood down)` |
| Soft hide (alpha 0, `pendingHide`) — Close/Escape/gate/stand-down in combat | none | none | transition line `on screen → soft-hidden, Hide owed: <cause>` and its settling `soft-hidden, Hide owed → hidden/on screen: <cause>` |
| Size/scale refused in combat (applied at next open) | none | the next open | `[Frame] popup size|scale not applied: in combat (the next open applies it)` |
| Notify one-shot timer | `[Notify] scheduling …` | `fired` / `canceled (superseded)` | kept; added `popup not auto-shown: frame.autoShow is off` at fire |

### Refusals and no-ops (§8 Diagnosis)

| Guard | Before | Done |
|---|---|---|
| `ShowNotification` `notify.enabled` off | silent return | `[Notify] skip: notify.enabled is off (no chat notice)` |
| `_TryFireJoinNotify` already notified | silent | `[Notify] skip: already notified for this group (<reason>)` |
| `_TryFireJoinNotify` not in group yet | silent | `[Notify] skip: not in a group yet (<reason>)` |
| `_TryFireJoinNotify` no pendingInfo on ROSTER path | silent by design | kept silent: the `[Roster]` line on that same transition already says `hasPending=false` |
| `inviteaccepted` arm stood down (direct calls only) | silent | `[Invite] ignored appID=…: addon stood down` |
| `/wg show` with no capture | chat only | `[Frame] /wg show refused: no captured group` |
| test mode start in combat | chat only | `[Test] test mode refused: in combat` |
| `ResetFramePosition` in combat | silent | `[Frame] popup saved position dropped; re-anchor refused: in combat` |
| `/wg enable|disable` seam refusal | chat only | `[Set] enabled refused: <err>` |
| visibility `never`, gate declined a show | `[Frame]` lines existed | kept |
| Slash library's disabled-verb gate | library, logs nothing | left (library-owned; upstream if wanted) |

### Dependencies (§8 Diagnosis)

| Dependency | Before | Done |
|---|---|---|
| Blizzard addon link type (EventRegistry route vs SetItemRef post-hook) | diagnostics report only | `[Init]` clause `, link route: SetItemRef post-hook (degraded client)`, absent on the normal route. On `[Init]` because the flag is off at login, so an enable-time line in `OnEnable` could never render |
| Refused event names | `[Init]` `rejected events:` clause | kept |
| LibDataBroker / LibDBIcon | Launcher library's one chat notice | left (library-owned) |
| LibKa0s majors absent | each stub's one chat line | left (stub prints; a stub cannot log through a DebugLog that did not load) |

### Errors caught by owned pcalls (§8 Diagnosis)

| Site | Before | Done |
|---|---|---|
| `ResolveSearchResultID` `pcall(GetApplicationInfo)` | a line per call, without the message | `NS.DebugErrorOnce` (new, `core/WhatGroup.lua`): site + message, once per distinct pair, marked seen only when actually logged |
| `GetApplicationInfo` missing | a line per call | once per session through the same helper |
| `settings/OptionsSetup.lua` page render pcall | chat only | `[Cfg] settings page '<key>' render raised: <err>` once per distinct error, site built behind the gate |
| `settings/Panel.lua` InlineButton onClick pcall | chat only | `[Cfg] button '<text>' onClick raised: <err>` once per distinct error |
| `settings/Schema.lua` profile reset pcall | `[Set] … (stopped by an error)` | kept |
| `core/CoreSetup.lua` SafeRegisterEvent pcall | `[Init]` rejected clause | kept |
| `core/DebugLogSetup.lua` font probe | none | left: runs at load with the flag off, and the result is visible (the console's own font) |
| `modules/Diagnostics.lua` reads | the report prints `unreadable` | left: the report is the output |

### Data mutations, settings seam, slash verbs

- Captures (`capturesByResult`, `pendingApplications`, `pendingInfo`) — `[Apply]`, `[LFG]`, `[Invite]`, `[Capture] wiped` — covered.
- Settings: library `[Set]` at the single write seam, profile reset/copy/switch lines — covered, unchanged.
- Popup geometry (named non-setting state): per-drag save unlogged (correct per §10); reset logged (MAY).
- Slash verbs: dispatch is the library's; each host verb's effect or refusal is logged by the code it reaches.

### Repeating paths (§9)

| Path | Before | Gap | Done |
|---|---|---|---|
| Cooldown ticker (`ScheduleRepeatingTimer`, 1 s) | no per-tick line | none | pinned quiet (30 ticks → no lines) |
| Combat edges (twice per pull, all session once the popup is built) | no lines | the new gate lines had to be change-gated | transition line written only when `popupState()` differs before/after; pinned quiet (25 pulls under `always` → no lines) |
| Teleport configure (twice per open: `PopulateFields` then `OnShow`) | `[Frame] teleport …` pair logged twice per open | duplicate per pass | change-gated on (spellID, known, activity, map, cd/ready), reset per show request in `preparePopup`; pinned once-per-open and still-logs-on-change (cooldown runs out) |
| `GROUP_ROSTER_UPDATE` | transition-gated | none | kept |

## Tests added (tests/test_debuglog.lua, 23 cases)

20 pins (each with a red-under comment; all 20 fail against the pre-change source) and 3 quiet or
change cases (combat edges quiet, ticker quiet, cooldown-runs-out still logs).

## Docs

- `docs/debug.md`: new `## Coverage` (tag → writer → when) and `### What stays quiet, and why`;
  intro bullet pointing at it.
- `docs/debug-content.md`: `State` tag, `[Init]` link-route clause, pointer to the Coverage table.
- `docs/common-tasks.md`: `[State]` bullet pointing at Coverage.
- Citations re-pointed for moved lines: `docs/performance.md`, `docs/ARCHITECTURE.md`, `docs/frame.md`,
  `docs/module-map.md`, `docs/slash-dispatch.md`, `WhatGroup.toc` load-order notes, one comment each
  in `core/DebugLogSetup.lua` and `tests/test_surface_parity.lua` (the latter two were already stale
  by a couple of lines; re-pointed at the line they describe). `docs/performance.md`'s `:113`
  (already stale, meant the `RegisterCallback` line) re-pointed with its siblings.
- `docs/test-cases.md` regenerated; README badge 846 → 869.

## Deliberately left

- New tag `State` (the standard's own example tag) rather than overloading an existing one; every
  other added line reuses the existing vocabulary.
- No separate `[State] combat entered/left` line per edge: the addon's reaction to a combat edge is
  entirely the popup (gate, owed Hide, queue), so the transition and flush lines are the one line
  per edge, and an edge that changes nothing writes nothing (§8: "an edge the addon does not react
  to needs no line"; §9 quiet steady state).
- Frozen bundles (`docs/audits`, `docs/reviews`, `docs/automated-tests`, `docs/revendor`) and the
  historical `docs/superpowers/plans` citations untouched.
- Library-side gaps (Slash disabled-gate refusal, Lifecycle edge logging) are LibKa0s's; not patched
  locally (`libs/` is never edited).
