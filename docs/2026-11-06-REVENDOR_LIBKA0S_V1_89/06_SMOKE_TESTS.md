# Owner smoke tests, v1.89.0 re-vendor

The owner runs these in the client and records the result. Nothing here is marked passed by Claude.

| ID | Addon | Check | Result |
|---|---|---|---|
| SM-01 | all 17 | `/reload` with every addon enabled: no Lua error. Each addon's settings panel and main window open, and skinned menus and dropdowns look as before | **passed** (owner, in game, 2026-11-06) |
| SM-02 | DpsRace | Right-click a run in Results: Share and Ignore for late casts open as **child menus beside the parent**, and the parent stays drawn. Picking a channel or entry runs it and closes every level. Hovering a plain row closes an open child | **passed** (owner, in game, 2026-11-06) |
| SM-03 | MultiMeters | Click a window's segment line: the shown segment (a stored one, Current or Overall) carries a **tick**. Pick another, reopen, and the tick follows | **passed** (owner, in game, 2026-11-06) |
| SM-04 | DropWatcher | Compact layout, then Filters ▾: a menu with Quality, Content, Character and Sort, each opening a child. Ticks match the full bar's dropdowns, a multi-select pick keeps the menu open and updates the `Filters · N` count and the list, Sort ticks one choice, a press outside closes it, and switching back to the full layout shows the same choices | **passed** (owner, in game, 2026-11-06) |
| SM-05 | DpsRace | A new-best toast still shows, one at a time, as before | **passed** (owner, in game, 2026-11-06) |
| SM-06 | LibKa0sSkinTester | Showroom: the cascade sample opens a child level beside its row, with the submenu arrow and a ticked row, and it follows each skin (cycle through a few). The parent stays drawn | **passed** (owner, in game, 2026-11-06) |
| SM-07 | DropWatcher | History tab: right-click a row, and the menu is the skinned Ka0s menu with the same entry, which still works | **passed** (owner, in game, 2026-11-06) |

## SF1 additions (after the owner's first feedback, `SF1_SMOKE_FEEDBACK.md`)

| ID | Addon | Check | Result |
|---|---|---|---|
| SM-08 | ConsumableMaster | Ka0s Default on an untouched profile: each bar button has a **thin dark** edge like Obsidian, not a white one. Show border off still removes it | **passed** (owner, in game, 2026-11-06) |
| SM-09 | all | Every window dropdown, search box and opened menu has a crisp 1 px edge on all four sides, as in LootHistory. Check DropWatcher, DpsRace, LootHistory, BankLedger and the others, in several skins and after a UI-scale change | **passed** (owner, in game, 2026-11-06) |
| SM-10 | LibKa0sSkinTester + any addon | Run Apply to all (or a Skin-tab copy) from another Ka0s addon: the tester's AceGUI "(Scope: panel)" cells stay painted, and its Ignore settings panel stays unticked | **passed** (owner, in game, 2026-11-06) |
| SM-11 | DpsRace (+ any addon fixed in SF1-DR) | Results column headers: no grey line above or below, the same as LootHistory | **passed** (owner, in game, 2026-11-06) |
