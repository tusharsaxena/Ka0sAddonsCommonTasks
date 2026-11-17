# Smoke tests (the owner runs these, in the game)

The owner ruled (Q5) that smoke happens at the end, after the full sweep. Record a result against each check as
**PASS**, **FAIL** (with a note) or **N/A**. The run never marks a check passed by itself.

Run these on **Retail and WoW Forever** wherever the addon ships on both.

| Id | Where | Check | Retail | Forever |
|---|---|---|---|---|
| SM-82 | Skin Tester, every skin | A mark's hover is clearly visible against its resting `icon.tint` and against `text.heading`. On Forever, hot is white. | | |
| SM-84 | Skin Tester ListRow, plus CombatTrail Fights tab under Ka0s Default | The alternating stripe, hover row and selected row can be told apart at a glance on every skin. | | |
| SM-79 | Any addon's debug console | Copy pastes plain text with no `|cff` codes, while the console keeps its colors on screen, and still after a skin switch. | | |
| SM-90 | Debug console | The footer is 24 px with a hairline, and the counter is muted and mono. Resizing works from the corner grip, and the console cannot shrink below four lines. | | |
| SM-92 | Library windows: icon browser, dropdown menus, reorder lists, sim panel, HUD drag strip, charts, skin picker, minimap button | No tooltip follows the cursor or sits on a corner. A body tooltip opens beside the window, right then left. A chrome tooltip is centered below its control, or above it in a footer. The minimap tooltip opens toward the screen centre. | | |
| SM-86 | Debug console, copy window, perf panel, sim panel, skin picker | The header reads extras · settings · close. Settings opens the owning addon's settings. The icon browser has no settings mark. | | |
| SM-81 | (no consumer yet) | N/A until Skill Master adopts it in phase [3]. | | |
| SM-RV | Every addon | It loads with no Lua error, its window or HUD opens, and test or sim mode works. Nothing changed apart from the library-driven changes above. | | |
