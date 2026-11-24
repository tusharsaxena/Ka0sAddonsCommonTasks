# Smoke tests: feedback batch 2026-11-24

The plan's smoke list (`00_PLAN.md`, *Smoke checks*: S-O2a, S-O2b, S-T1..T6, S-K1..K2, S-P1..P6, S-A1, S-Q1,
S-S1..S4, S-O1) became 42 in-game checks in the addons' own `docs/smoke-tests.md`. The owner ran them from
the sheet `Documents/Ka0sPendingSmoke-2026-11-24-ADDED-FB.csv` (run "FB 11-24", both clients).

| Addon | Checks |
|---|---|
| Aura Master | PRESETS-51, SKIN-59 |
| Absorb Tracker | LOOK-25, SKIN-48 |
| Bank Ledger | LEDG-67 |
| Loot History | HIST-53 |
| Combat Trail | SM-CT-H24, SM-CT-H25, SM-CT-T12, SM-CT-T13, SM-CT-T14 |
| Consumable Master | DIAG-45, SKIN-50 |
| Drop Watcher | FEED-113 |
| KickCD | CAST-23, LABEL-16, LABEL-17 |
| Multi Meters | EXPORT-58 |
| Outfitter Reborn | FB1, FB2, FB3 |
| Panel Master | DIAG-31 |
| Party Frame Enhanced | CAST-9, CAST-10 |
| Pretty Chat | RV-112 |
| Quick Comms | EDIT-36, SKIN-36, THANK-14 |
| Range Master | DIAG-4, DRAW-11, DRAW-12 |
| Skill Master | SM-FB-1 .. SM-FB-6 |
| Skin Tester | DIAG-6, SHOW-62, SHOW-63 |
| PGF Extension | DIAG-4 |
| WhatGroup | POPUP-15 |

## Result

**All 42 passed: the owner's report, 2026-11-24** ("Ka0sPendingSmoke-2026-11-24-ADDED-FB.csv all pass").
The sheet's Result column was left blank; the result is the owner's word in the session, not a filled sheet.

The same message brought one more finding on THANK-14: the sample toast's note, "Test mode: a placeholder
that sends nothing.", wraps onto a second line. Fixed before the merge as FB-QC-03 (the note now reads
"Test mode: sends nothing."). THANK-14 in Quick Comms' `docs/smoke-tests.md` now fails on a wrapped note.
That re-check is owed: **THANK-14 (re-check of the one-line note).** Result:
