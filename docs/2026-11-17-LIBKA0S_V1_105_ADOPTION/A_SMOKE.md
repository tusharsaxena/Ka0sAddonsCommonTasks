# Wave A smoke sheet

The owner runs these checks in game and records **PASS**, **FAIL** (with a note) or **N/A**. The run never marks
a check passed by itself. Each id is written out in full in that addon's `docs/smoke-tests.md`.

Run each check on Retail, and on WoW Forever too where the addon ships there (marked **R·F**). Skill Master
ships on Forever only.

**What to look for everywhere:**
- **The strip, in a window:** it sits flush **directly under the title bar**, full width, above any tabs or
  filter bar. The content moves down by its height, and nothing is covered. The title shows no "Test" or "Sim"
  word while the strip shows.
- **The strip, on a HUD:** it sits on the display's **top edge, outside it**. It flips below the display near
  the top of the screen, and it takes no clicks.
- **A footer:** 24 px, no dark band, one hairline along its top, muted text, with the grip in the corner.

| Addon | Checks | What changed | Result |
|---|---|---|---|
| Absorb Tracker (R·F) | SIM-4, FOREVER-11 | A cyan sim strip on each bar's top edge, above the drag handle when unlocked; it follows a drop and a scale change, and goes on stop | |
| Aura Master (R·F) | CONT-28, PRESETS-2, PRESETS-44 | An amber test strip above each chain's top container (locked and unlocked); the preset picker's footer reads "Change it later on General > Presets." on one line | |
| Kick CD | SIM-12, SIM-19, SIM-13 | A cyan strip on each icon grid during `/kcd sim` (was none, ruling D-13 reversed); it clears the label and the cast bar and flips at the screen top; the step panel is unchanged | |
| Bank Ledger | LEDG-64, LEDG-65, SESS-16, LEDG-20, LEDG-52/54/57/58, SESS-14, DEGRADED-13 | The ledger strip is now under the title bar (was under the filter bar); the footer is 24 px; the session window strip | |
| Combat Trail (R·F) | SM-CT-H8, SM-CT-H16, SM-CT-R26, SM-CT-RM93, SM-CT-RM94, SM-CT-RM41 | The HUD, Results and Race window strips under the title bar (the Race window had none before); the HUD and Race footers are 24 px | |
| Dps Race | SM-DR-AD88HUD, SM-DR-AD88RES, SM-DR-AD89HUD, SM-DR-AD89RES, SM-DR-UT46, SM-DR-UT49 | The HUD and Results strips under the title bar; the footers are 24 px, and the resize grip sits on the footer | |
| Loot History | HIST-45, HIST-46, STATE-13/15/17, SIM-1, SIM-12 | The History strip is now under the title bar (was under the filter bar); the footer is 24 px | |
| Skin Tester (R·F) | SHOW-53, SHOW-1, SHOW-50 | The showroom footer is 24 px; the showcase strips are unchanged | |
| Multi Meters | WIN-40, WIN-48, WIN-59 | The strip is under the title, the column headers sit flush under it, and the session line drops its "Test" word; the default skin is in the profile defaults (a new profile wears Ka0s Default) | |
| Outfitter Reborn (R·F) | WCF1-WCF5, RT1-RT4, FS1-6, FS2-2 | The outfit window and outfit bar strips are docked; the footer is a hairline (Forever: right of the side tabs) | |
| Skill Master (F) | SM-TEST-6, SM-TEST-7, SM-SIM-1 | The strip under the title bar in the main window, the Journal and the LDB tooltip's Main style; the 24 px footer for the bonus legend and the Journal's Alts hint line | |
| PGF Extension | SKIN-56 | A new profile starts on Ka0s Default | |
| What Group | SKIN-43 | A new profile starts on Ka0s Default | |
