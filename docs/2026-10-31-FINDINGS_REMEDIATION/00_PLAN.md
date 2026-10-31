# Plan: remediate the pre-merge findings

Owner request, 2026-10-31: "Fix all the findings from the sync docs and perf results now."
Inputs: `inputs/findings/<repo>.json`, the pre-merge run's returned results, plus each repo's newest `docs/automated-tests/<run>/ANALYSIS.md`.

Branch `feat/2026-10-31-findings-remediation` in every touched repo. Nothing merges, tags or bumps without the owner's go-ahead.

Rulings by the lead:

- **Perf:** fix the cause. A ceiling moves only when the excess is shown to be a measurement artifact or the cost is justified, and the reason goes beside the ceiling.
- **Comment citations:** the owner's "fix all" is the confirmation. Comment-only. A target is written only with evidence; historical mentions of retired files stay.
- **Dead exports:** remove a member with no shipped caller after verifying string dispatch. Keep `__` test seams, degraded-stub parity members and library lifecycle hooks, and record why.
- **Watch list:** split what has a fired re-check, a Peel next state or a spent shelf life, by pure moves. If a split is unsafe, add a tracked deviation row instead.
- **LibKa0s payload is not edited** (`LibKa0s/`, `testkit/`), so no release or re-vendor follows. Payload rows get tracked deviations; a real library gap is reported.
- **Smoke:** per-repo Result lines for the two merged runs' checks record the owner's pass of 2026-10-31. New splits and perf fixes get smoke notes, unpassed.

DpsRace starts after `feat/2026-10-31-dpsrace-bar-styling` lands, stacked on it.

Order per repo: fix, independent review, fix round, recorded run.
