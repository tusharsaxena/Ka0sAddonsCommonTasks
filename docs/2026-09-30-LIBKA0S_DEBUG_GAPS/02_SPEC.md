# Spec

Branch everywhere: `feat/2026-09-30-libka0s-debug-gaps`. Every repo's `CLAUDE.md` governs work in it.

## S1 — LibKa0s v1.65.0 (DG-LIB-01)

Commit per gap (`DG-LIB-01: G<n> ...`), tests first for each, bump each touched module's LibStub minor, docs/api
for each touched major, one CHANGELOG v1.65.0 block, the release record docs/releasing.md requires, local
annotated tag v1.65.0 on the last commit (not pushed). Keep every file under the 1000-line band (DebugLog.lua is at
999: new DebugLog surface goes in a secondary file loaded by LibKa0s.xml, as DebugLogDiagnostics.lua does).

- **G1 Slash.** The descriptor takes `debug(tag, message)`. Every refusal Slash decides itself writes one line
  naming the verb and the guard: the disabled gate, an unknown verb, a parse/validation refusal of get/set/reset,
  a profile switch refused in combat (and any other refusal the module owns). Tag `Cmd` unless the module already
  has a vocabulary. Nothing is printed to chat that was not printed before.
- **G2 DebugLog.** (a) `onClear()` descriptor hook, called by `D:Clear()`. (b) A change-gate on the instance:
  `D:DebugOnce(key, tag, fmt, ...)` (first time per key per arming) and `D:DebugChanged(key, tag, fmt, ...)`
  (only when the formatted line differs from the last one for that key); both gated like `D.Debug` with the
  string built only when logging is on; memory cleared by `Clear()` and by turning logging on. Name them in the
  module's existing style if a better name fits; document them.
- **G3 Options combat lock.** A refused write, Defaults, Restore-all or tab switch under the combat lock writes one
  line naming what was refused; a registration parked in combat writes a line when parked and a flush line when it
  runs. Through the descriptor's `debug` (Options already has a descriptor).
- **G4 Launcher (+ DebugLog).** A bounded "at enable" queue on the console: `D:AtEnable(tag, fmt, ...)` (or the
  module's own name) records a line while logging is off and emits it when logging turns on (and immediately when
  it is already on). Launcher's dependency / registration lines use it through its host wiring, so they land the
  first time the player turns logging on. Bound it (e.g. 32 lines) and say what is dropped.
- **G5 Lifecycle.** The descriptor takes `debug`. Each stand-down and stand-up edge writes one line with the holds
  (added / released, and the resulting set). No line when a call changes nothing.
- **Tests** for each gap, including the silent default when no `debug` is passed; the kit (testkit/) only where a
  mock is missing (bump the kit revision if it changes).

## S2 — Standard v2.73.0 (DG-STD-01), after S1

From LibKa0s v1.65.0's api docs: debug-logging (§4 sink wiring, §8, §9) states that LibKa0s modules log their own
refusals and edges through the host's `debug` sink; a host **MUST** pass `debug` to every LibKa0s descriptor that
takes it, **MUST NOT** log a duplicate of a line the library writes, and **SHOULD** use the console's change-gate and
at-enable queue rather than hand-rolled ones. Update library-stack-§7's rows, AUDIT.md's debug checks, the context
pack, NEW_ADDON templates. Full ripple, version bump.

## S3 — wow-addon (DG-PLUG-01), after S2

Match v2.73.0 wherever the plugin prescribes debug wiring or checks it. No commit if nothing needs changing.

## S4 — Adoption in each addon (DG-<XX>-01), after S1 and S2

Re-vendor v1.65.0 (whole `libs/LibKa0s/` and `tests/_kit/` from the local tag); standards reference v2.73.0.
Pass the host's gated sink as `debug` to every LibKa0s descriptor that takes it (Slash, Options, Lifecycle,
Launcher). Replace hand-rolled change-gates with the console's (keep behaviour; delete the copy), route
dependency/state-at-enable lines through the at-enable queue, and remove host lines the library now writes
(Lifecycle edges, Slash refusals such as AbsorbTracker's DisabledLine matching). Tests pin the library-owned lines
landing in this addon's log and the absence of duplicates; `docs/debug.md` Coverage updated (which tags are the
library's); smoke rows for a Slash refusal and a Lifecycle edge showing in the console. Gate green.

## S5 — Record (DG-FIN-01)

`99_REPORT.md`, checkpoints, branches pushed. Merge only on the owner's go-ahead.
