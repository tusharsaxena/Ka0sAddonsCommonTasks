# Addendum A2: running diagnostics turns debug logging on; the A1 rollout (owner, 2026-09-30)

The owner looked at the AuraMaster preview (DL-AM-03): **"Looks good."** That approves the A1 Diagnostics link
for the rollout. Same message, a behavior change:

> By default clicking on Diagnostics (or doing /xx diagnostics) should also turn on debug (/xx debug on)
> for that session.

This changes the standard: debug-logging-§14 says the report "MUST NOT read or change the debug flag … the
flag reads the same afterwards", and the kit's diagnostics contract pins it. It is an owner decision to change
the standard (CLAUDE.md, choice 2), recorded here.

## Spec (S6)

1. **Standard v2.71.0 (DL-STD-02).**
   - debug-logging-§14: running the report (the `diagnostics` word, either form, and the console's
     Diagnostics link) **turns debug logging on for the session** through the flag's one seam (§5,
     `SetEnabled(true)`), **before** it writes, when logging is off. It never turns logging off. A host
     **MAY** opt out through the descriptor (`diagnosticsEnablesLogging = false`). The report's
     **sections** still read state only and **MUST NOT** touch the flag; only the run does. The report
     still lands in full through the ungated sink. Reword §12's user-initiated-run rule to match.
   - debug-logging-§1 "What the library guarantees": the orange **Diagnostics** link in the console's title
     bar, beside the Debug On/Off label, which runs the report.
   - Full ripple (index blurb, changelog, version stamps, context pack, playbooks; AUDIT.md's check of §14).
2. **LibKa0s (DL-LIB-03), still v1.64.0.** `D:RunDiagnostics()` calls `D:SetEnabled(true)` before writing
   when the flag is off and the descriptor does not set `diagnosticsEnablesLogging = false`; the
   `[Debug] logging enabled` line and the `[Init]` summary therefore precede the report. The link runs the
   same function. Bump DebugLogDiagnostics' minor (and DebugLog's if it changes). Kit revision 34: the
   contract case "the report lands with logging off and leaves it off" becomes "lands with logging off and
   turns it on for the session", plus an opt-out case (the flag stays off) and an already-on case (no second
   enable line). CHANGELOG v1.64.0, api docs, release record, local tag moved. Not pushed.
3. **wow-addon (DL-PLUG-01).** Wherever the plugin states the diagnostics contract or the console's
   furniture (review/standards-audit agents, new-addon, sync-docs), match v2.71.0. Nothing else.
4. **Every addon (DL-AM-04, DL-<XX>-03 for the other ten).** Re-vendor the final v1.64.0 (kit rev 34); refresh
   the standards reference to v2.71.0; fix addon tests or docs that assert diagnostics leaves logging off;
   `docs/debug.md` says the report turns logging on; smoke rows: the orange Diagnostics link (the other ten)
   and "diagnostics turns logging on for the session, /reload turns it off" (all eleven, AuraMaster's A1 row
   reworded). Gate green, reviewed.
