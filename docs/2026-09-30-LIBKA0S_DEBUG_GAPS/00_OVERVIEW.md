# LibKa0s debug gaps (2026-09-30)

The 060 audit (`../2026-09-30-DEBUG_LOGS_AND_RESIZABLE_WINDOWS/99_REPORT.md`, Residuals) found five places where a
LibKa0s module decides something a support read of the log needs, and the addon cannot log it. The owner: "Go
ahead and fix the 5 gaps right away. Create a resumable and check pointed plan, use ultracode, commit
incrementally." Owner also reports the previous run's in-game checks (A2) pass.

| Gap | Module | What is missing today |
|---|---|---|
| G1 | Slash | Its own refusals (disabled gate, unknown verb, parse/validation refusal, profile switch in combat) reach chat only. Hosts cannot see them (AbsorbTracker even matches the gate's chat line to find them). |
| G2 | DebugLog | No Clear hook, so hosts' change-gates ("log once", "log on change": MultiMeters `NS.DebugSteadyReset`, PanelMaster `NS.DebugOnce`, KickCD's list signatures, PartyFrameEnhanced's memos, ConsumableMaster `KCM.DebugQuiet`) are not re-armed by a Clear; and every host hand-rolls the helper. |
| G3 | Options (combat lock) | An open panel's combat lock refuses writes, Defaults and tab switches without a line; "register parked (in combat)" has no flush line. |
| G4 | Launcher | Its dependency lines (LibDataBroker / LibDBIcon found or missing, registered) run at OnEnable while the session-only flag is off, so they never land. |
| G5 | Lifecycle | Stand-down / stand-up edges and holds are not logged by the library; several hosts added their own lines. |

## Decisions (orchestrator, under the owner's standing "use your best judgement")

| # | Decision | Why |
|---|---|---|
| J1 | One shape for every module: the host's gated sink arrives as the descriptor's `debug(tag, message)` field, exactly as Launcher already takes it; absent = the module stays silent (today's behaviour). | One convention the addons already know; additive, no floor raise. |
| J2 | G2 ships a library change-gate (`Once(key, ...)` and `Changed(key, summary, ...)` style helpers on the console instance) whose memory is re-armed on Clear and on enable, plus an `onClear` descriptor hook for hosts that keep their own. Placed in a secondary file (DebugLog.lua is at 999 lines). | Removes five hand-rolled copies; a hook alone leaves the copies. |
| J3 | G4: lines a module writes while logging is off and that describe state (not events) are held and emitted when logging turns on (a small, bounded "at enable" queue on the console), so "dependencies once at enable" (debug-logging-§8) is actually visible. | The flag is off at login by design; the queue is the only way the line lands. |
| J4 | G5: Lifecycle logs each stand-down / stand-up edge with its holds; hosts drop their now-duplicate lines in adoption. | One line per edge, not two. |
| J5 | The standard (v2.73.0) says library modules log their own refusals and edges through the host's sink, hosts MUST pass it and MUST NOT duplicate those lines, and SHOULD use the library change-gate over a hand-rolled one. Written after LibKa0s lands, from its api docs. | The standard describes what the library does. |
| J6 | Release as LibKa0s v1.65.0 (local tag until finalize). No merge, no pushed tag without the owner's go-ahead; branches pushed at milestone ends. | Same rules as the last run. |

## Files

`02_SPEC.md`, `03_EXECUTION_PLAN.md`, `items.tsv`, `checkpoints.tsv`, `RESUME.md` + `resume-state.sh`, `99_REPORT.md` (at the end).
