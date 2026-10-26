# Smoke tests: owner, in game (Ka0s Skin Tester)

Mark each row **pass** / **fail** with a note. Only the owner marks rows.

**Setup:** symlink `GIT/LibKa0sSkinTester` into `World of Warcraft\_retail_\Interface\AddOns\LibKa0sSkinTester`,
check out `feat/2026-10-26-skin-tester`, and **fully exit and restart the client**: new font and texture files
are only seen at client start. Later rows may `/reload`. The tester vendors LibKa0s v1.78.0 (`7bc3e9b`), the
same tag LootHistory carries.

The tester's own `docs/smoke-tests.md` holds the per-surface checks (SHOW-1..10, SLASH-4, PANEL-5 and the
scaffold's INSTALL / SLASH / PANEL / PROFILE / STATE / COMBAT / DIAG / DEGRADED / LOC rows). The rows below are
the run-level pass.

| Id | Verifies | Check | Expect | Result |
|---|---|---|---|---|
| ST-S1 | ST-01, ST-04 | Restart the client with the addon installed, then `/st` and `/st show` | No Lua error at login; `/st` opens Settings -> AddOns -> Ka0s Skin Tester; `/st show` opens a 960x640 window titled "Ka0s Skin Tester — Skin showroom", footer "Wearing Ka0s Default", sections scrolling under the wheel | |
| ST-S2 | ST-03 | Click each of the nine swatch cards in turn | The whole window repaints at each click; the clicked card's name reads in the skin's accent and no other card's does; no EllesmereUI card | |
| ST-S3 | ST-03 | Pick Obsidian on a card, `/reload`, `/st show` | Still Obsidian, and the Obsidian card is the selected one | |
| ST-S4 | ST-05, ST-06 | In each skin, scroll the whole window: Chrome, Controls, Lists, Text, Panels, Overlays, Values | Every sample legible. Record an illegible sample as a **skin defect** (skin, section, caption), not a tester failure. Hover "Hover me" (tooltip), open the dropdown (menu), click tabs 2 and 3 | |
| ST-S5 | ST-07 | Pick Obsidian, open Settings -> Ka0s Skin Tester -> Sample controls; then pick Glass and reopen | A heading over a checkbox, a slider, a dropdown, a color swatch and Use class color, in the skin worn; no Appearance tab, no copy button; the page follows the change | |
| ST-S6 | ST-03, ST-04 | Enter combat (a target dummy), open the showroom and click a card | No Lua error, no taint warning; the window opens and repaints in combat | |
| ST-S7 | ST-07 | `/skintester show`. Then, with any other addon that registers `/st` enabled, log in | `/skintester` opens the showroom. With the other addon: one tagged line at login saying the tester answers only to `/skintester`, and `/st` reaches the other addon. Without one: no line | |
| ST-S8 | ST-01 | Minimap button: left-click, right-click -> Show window; bind a key on General -> Keybindings and press it | Settings open; the menu's Show window toggles the showroom; the key toggles it | |
| ST-S9 | ST-04 | With Loot History installed and both on the same skin, open its History window beside the showroom | The two look the same: same shell, title bar, buttons, tabs, list rows | |
