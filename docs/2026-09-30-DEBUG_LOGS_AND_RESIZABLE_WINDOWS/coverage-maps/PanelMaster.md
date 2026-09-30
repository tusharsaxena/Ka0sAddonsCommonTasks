# PanelMaster: 060 debug-coverage map (DL-PM-02)

Audited against debug-logging v2.70.0 §8 (the flows and the Diagnosis checklist) and §9 (coalescing
and the quiet steady state). Branch `feat/2026-09-30-debug-logs-and-resize`. The tag-by-tag list
lives in the repo at `docs/debug.md` ▸ *Coverage*.

## S4.1 Inventory, S4.2 gaps and S4.3 fixes

| Inventory item | Existing line | Gap | What was done |
|---|---|---|---|
| Lifecycle: `[Init]` on enable (`NS.InitSummary`) | name, version, schema, profile, panels | §8 dependencies: none logged; the flag is off at OnEnable, so the Init line is the only place | `NS.DependencySummary()` appended: `LSM yes/no, LibDBIcon yes/no, Sunn themes N` (`core/Database.lua`); Sunn count recorded by `SunnArt.Inject` |
| Lifecycle: stand-down / stand-up latch (`core/LifecycleSetup.lua`) | `[Lifecycle] stood down (<holds>)`, `stood up` | none | kept |
| Events: PLAYER_LOGIN, PLAYER_ENTERING_WORLD, PLAYER_REGEN_ENABLED/DISABLED; refused names | `[Events] rejected <name>` | none for refusals | kept |
| Loading-screen edge (PLAYER_ENTERING_WORLD → RenderAll) | only the `rendered` line, with no cause | §8 state edge | `[Canvas] entered world: repainting` in `addon:OnEnterWorld` |
| Combat edges (REGEN → `Canvas:RenderForCombat`) | none | §8 state edge, when the renderer acts | `[Canvas] combat entered/left: repainting for visibility '<mode>'`, only for inCombat/outOfCombat; Always/Never stay silent (the renderer ignores the edge) |
| Combat edge → unlock queue flush (`U:ResumePending`) | none (chat only) | §8 deferred work: flush and count | `[Unlock] combat over: flushed held unlocks (all=…, N panel(s), M gone)`, only when something was held |
| Deferred work: combat-held unlocks (`U:SetUnlocked`, `U:SetPanelUnlocked`) | none (chat only) | §8 hold line with its reason | `[Unlock] unlock all held: in combat`, `'<panel>' unlock held: in combat` |
| Held-then-never-flushed: a lock drops the queue; a profile change drops the panel queue (`U:ForgetPending`) | `panels locked` only; ForgetPending silent | §8 "a hold with no flush must be visible" | lock line gains `, N held unlock(s) dropped`; `dropped N held panel unlock(s): profile changed` (lock path peeled into `dropAllUnlocks`) |
| Registry mutations (create, delete, delete all, rename, reset, copy, fit, set, move) | one `[Panel]`/`[Set]` line each | none | kept |
| Registry refusals (the editor and the slash both reach them) | none (chat only, or the editor's status) | §8 refusals with the reason | `refuse(verb, fail, reason)` helper: `[Panel] <verb> refused: <reason>`; the coercer's refusal as `set '<panel>'.<field> refused: <reason>` |
| Slash-local refusals: `/pm panel <name>` naming no panel, `/pm panel <name> <field>` with an unknown field (`Sl:CliPanel`) | none (chat only; refused before any Registry verb) | §8 refusals with the reason (review round 1) | the same helper, published as `R.Refuse`: `[Panel] panel refused: no panel called '<name>'` / `unknown field '<field>'` |
| `R:Recover` screen guard (`GetScreenSize` answers nil) | none; the slash then claimed "every panel is already on screen" | §8 a guard with no named reason (review round 1) | `[Panel] recover refused: cannot measure the screen` through `refuse`; `/pm recover` prints the reason |
| Settings seam (library `R.Set`, bulk bracket, profile handler) | `[Set] …` (library + host) | refusals of a bad value are not logged | deliberately left (below) |
| Profile events (`core/Database.lua`) | `[Profile] switched…`, `[Set] copied/reset profile…` | none | kept |
| Migration, preview sweep | `[Migrate]`, `[Preview]` | render only if logging is on at load (it never is) | kept; their result reaches the Init line (schema) and diagnostics |
| View open / recompute | library `[Cfg] opened`; `[Canvas] rendered N panels` | the recompute line could not tell hidden from missing | now `rendered N panels, M shown`, built behind the gate (`NS.DebugBuild` + `renderCounts`) |
| Errors caught: settings-page closures (`settings/Panel.lua` `safeRun`) | `[Panel] <tag> failed: <err>` on every failure | §8 once per distinct error (a broken refresher raises on every refresh) | routed through the new `NS.DebugOnce`, keyed on the closure's tag as the site (review round 1), so two closures raising one message are two lines |
| Errors caught: `Compat.MouseIsOver` pcall, on the 10Hz tick | none (silently false) | §8 errors caught, and §9: must not repeat per tick | `[Canvas] MouseIsOver failed: <err>` once per distinct error via `NS.DebugOnce` |
| Media fallback (`Compat.FetchMedia`, every repaint) | none | §8 no-op with the reason ("why is my panel plain") | `[Canvas] <type> texture '<name>' not found: drawn as Solid`, once per type and name |
| Repeating path: shared 10Hz mouseover OnUpdate (`modules/Canvas.lua`) | silent | none (already quiet) | pinned by a quiet-steady-state test (100 ticks, 0 lines) and a one-line-per-error test |
| Repeating path: slider drag throttle (`scheduleTimer`, 50 ms) | `[Set]` per applied step + `[Canvas] rendered` | none: user-driven, each `[Set]` carries a new value (a real recompute, §9) | kept |
| Slash verbs | chat acks; mutations logged at the Registry/schema seams | disabled-state refusal not logged | deliberately left (below) |
| Launcher, Options | library `[Launcher]`, `[Cfg]` lines | none | kept |

New seam: `NS.DebugOnce(site, key, tag, fmt, ...)` in `core/DebugLogSetup.lua` (gate first, seen-set
written only past the gate, two-level key so an erroring site builds no string), with a no-op on the
library-absent arm and a parity assertion in `tests/test_surface_parity.lua`.

## S4.4 Tests

`tests/test_debuglog.lua` ▸ *Coverage* (12 new cases, 975 → 987; review round 1 added 4 more, 987 → 991: the re-arm on enable, the per-closure `safeRun` key, the two `/pm panel` slash refusals, and the recover screen guard), each with a red-under comment:
the hold and flush lines; the lock and profile drops; an empty combat exit writes nothing (20 exits);
the combat edge logged only under a combat-dependent visibility; the world edge ahead of its
rebuild; the shown count; three refusals; the Init dependency clause; `NS.DebugOnce` gating and
dedupe; and the quiet steady state for the one repeating path fixed or pinned: 100 mouseover ticks
write nothing, a swallowed tick error is exactly one line in 100 ticks, and a missing texture is
one line across 10 rebuilds. Mutation-checked: a plain `NS.Debug` in `MouseIsOver` and an
unconditional flush line each turn cases red.

## Deliberately left, and why

- **Schema-write refusals** (`/pm set <path> <bad value>`): the refusal comes from
  `LibKa0s-Schema-1.0`'s `R.Set`, which the slash descriptor takes as a value with no host wrapper,
  by design (`settings/Slash.lua`). A debug line for it belongs in the library (residual for the next
  LibKa0s).
- **Feature verb refused while disabled**: answered by `LibKa0s-Slash-1.0`'s dispatcher gate. The
  disabled state itself is in the log (`[Lifecycle] stood down (disabled)`) and the report. Library
  residual as above.
- **Load-time lines** (`[Migrate]`, `[Preview]`, `[Artwork] Sunn adapter`): kept as written. The
  flag is off at load, so they rarely render. Their results reach the log through the Init summary
  and `/pm diagnostics`.
- **Unreacted edges** (group roster, spec, `ADDON_RESTRICTION_STATE_CHANGED`): the addon registers
  none of them. §8: an edge the addon does not react to needs no line.
- **`NS.DebugOnce` and a console Clear**: the seen-set is re-armed on every logging enable edge (the
  descriptor's `setEnabled`, review round 1), so each logging session shows each recurring error or
  fallback once. A Clear does not re-arm it, because `LibKa0s-DebugLog-1.0` exposes no clear hook to
  the host. Library residual for the next LibKa0s: a descriptor `onClear` callback.
