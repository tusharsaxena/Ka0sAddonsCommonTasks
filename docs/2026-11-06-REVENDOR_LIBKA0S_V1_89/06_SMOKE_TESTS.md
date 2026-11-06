# Owner smoke tests, v1.89.0 re-vendor

The owner runs these in the client and records the result. Nothing here is marked passed by Claude.

| ID | Addon | Check | Result |
|---|---|---|---|
| SM-01 | all 17 | `/reload` with every addon enabled: no Lua error. Each addon's settings panel and main window open, and skinned menus and dropdowns look as before | |
| SM-02 | DpsRace | Right-click a run in Results: Share and Ignore for late casts open as **child menus beside the parent**, and the parent stays drawn. Picking a channel or entry runs it and closes every level. Hovering a plain row closes an open child | |
| SM-03 | MultiMeters | Click a window's segment line: the shown segment (a stored one, Current or Overall) carries a **tick**. Pick another, reopen, and the tick follows | |
| SM-04 | DropWatcher | Compact layout, then Filters ▾: a menu with Quality, Content, Character and Sort, each opening a child. Ticks match the full bar's dropdowns, a multi-select pick keeps the menu open and updates the `Filters · N` count and the list, Sort ticks one choice, a press outside closes it, and switching back to the full layout shows the same choices | |
| SM-05 | DpsRace | A new-best toast still shows, one at a time, as before | |
