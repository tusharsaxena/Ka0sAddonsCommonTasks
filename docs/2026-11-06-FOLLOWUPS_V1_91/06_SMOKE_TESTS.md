# Owner smoke tests, v1.91.0 follow-ups

The owner runs these in the client and records the results. Nothing here is marked passed by Claude.

| ID | Addon | Check | Result |
|---|---|---|---|
| SM-1 | LootHistory, Skin Tester | Line charts (LootHistory Insights or Timeline, the showroom's chart): axis, grid, markers and the hover crosshair are crisp 1 px lines at your UI scale, in a couple of skins and after a UI-scale change | **passed** (owner, in game, 2026-11-06) |
| SM-2 | all 17 | `/reload` with every addon on: no Lua error. Each addon's window, settings panel, dropdowns, menus (including cascades), toasts (DropWatcher stack, DpsRace new-best) and skin picker work as before. The peels moved code between files and must change nothing | **passed** (owner, in game, 2026-11-06) |
