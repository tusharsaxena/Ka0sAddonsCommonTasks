# Smoke tests — owner, in game (leg 1, LootHistory)

Mark each row **pass** / **fail** with a note. Only the owner marks rows.

**Setup:** LootHistory and LibKa0s on `feat/2026-10-25-skinning` (the game loads `GIT/LootHistory` through its
symlink; LootHistory vendors the local tag `v1.78.0` at LibKa0s `65a23cb`). **Fully exit and restart the WoW client**
after checking out the branch: new font and texture files are only seen at client start, and `/reload` is not
enough. Later rows may `/reload`.

LootHistory's own `docs/smoke-tests.md` carries the per-surface checks the items added (HIST-44, INS-23, TL-18,
LED-13, PANEL-22..24, SKIN-1..18); the rows below are the run-level pass.

| Id | Verifies | Check | Expect | Result |
|---|---|---|---|---|
| SK-01 | LH-02..LH-05, LK-03 (SK-ENGINE) | Open the History window with the skin left at **Ka0s Default** | Looks exactly as before this run: window, tabs, filter bar, table, Export, Insights, Timeline, Holdings, settings pages | |
| SK-02 | LH-01, LK-10 (SK-TAB) | Settings → LootHistory → General → **Appearance** tab | Sits **immediately before Keybindings**; shows Skin source, the nine skins with swatches, Copy to every Ka0s addon, the HUD note | |
| SK-03 | LH-02..LH-04, LK-04, LK-11, LK-A2, LK-A3 (SK-LH-*) | Pick each skin in turn with the History window open (Obsidian, Azeroth, Glass, High Contrast, Ember, WoW Default, WoW Midnight, WoW Forever, back to Ka0s Default) | Window, table rows (scroll to see pooled rows), bind padlocks, tabs, buttons, search, dropdown and its menu, footer, Export, Insights cards/charts, Timeline, Holdings, AH price table all repaint **without a reload**; text stays readable | |
| SK-04 | LK-07, LK-08, LH-06 (SK-SETTINGS) | With a non-default skin, open the settings pages of LootHistory **and** another Ka0s addon (e.g. BankLedger) and another AceGUI addon | LootHistory's pages (nav rail, tabs, headings, checkboxes, sliders, dropdowns, edit boxes, drawers) are skinned; the other addons' pages are **stock**, including after flipping back and forth between them (AceGUI pool leak check) | |
| SK-05 | LK-11, LK-02 | WoW Forever skin | Warm charcoal panels, black title bars with centered white titles, tan accent, gold headings, thin borders. Barlow shows in title bars, buttons, edit boxes, dropdowns and settings controls; **table, Insights, Timeline and Holdings body text keep the client font by design** (their layout is measured against it; leg-2 item) | |
| SK-06 | LK-11 | High Contrast skin | Black/white/yellow, larger Atkinson text; hovered row highlighted | |
| SK-07 | LK-02, LK-A1 | Fonts | Barlow / Cinzel / Atkinson render (no fallback squares) on an English client; `/dump LibStub("LibSharedMedia-3.0"):IsValid("font","Ka0s Barlow")` is true; **no** "LibSharedMedia-3.0: Attempt to register an invalid file/font" error from any addon at login (the error reported earlier today) | |
| SK-08 | LK-09, LH-05 (SK-TOOLS) | Debug console (`/lh debug`), the sim/test strip, the perf panel (`/lh perf`), a copy window, the Export copy window | Follow LootHistory's skin | |
| SK-09 | LK-05 (SK-EUI) | EllesmereUI loaded, third-party skinning on, LootHistory on in its Third-Party list | Appearance → Skin source **EllesmereUI** enabled; choosing it repaints in the EllesmereUI look live | |
| SK-10 | LK-05 | Turn LootHistory off in EllesmereUI's Third-Party list (or disable EllesmereUI) and reload | The EllesmereUI choice is disabled with the failing condition and its fix listed; LootHistory falls back to its Ka0s skin | |
| SK-11 | LK-05 | Switch from EllesmereUI back to a Ka0s skin | A reload is offered; after reload the Ka0s skin shows | |
| SK-12 | LK-10 | Copy to every Ka0s addon | Disabled with the hint (only LootHistory adopts skins in leg 1); nothing else changes | |
| SK-13 | LH-01 | Profile switch / reset in LootHistory's Profiles | The skin follows the profile | |
| SK-14 | LK-03, LK-10 | Combat: change skin in combat | No Lua error, no taint warning; settings page behaves as other settings in combat | |
| SK-15 | LH-05 | Minimap button and its tooltip under every skin | Unchanged, no Lua error | |
| SK-16 | LH-03, LH-04, LK-A3 | Under Azeroth and High Contrast: tooltips on a History row, an Insights bar and a Timeline point; the reset/purge popups | Legible; the tooltip frame is Blizzard's; popups are stock. Known leg-2 item: under Azeroth, Timeline's Gained/Lost tooltip lines take the dark parchment green/red and may read poorly on the dark tooltip | |
| SK-17 | LH-04, LH-06 | Settings → General → AH price table, the Filters tab, Profiles | Follow the skin | |
| SK-18 | LK-06..LK-09 | With LootHistory on a non-default skin, open two other Ka0s addons' windows, debug console, sim panel/test strip and settings pages; then disable LootHistory, `/reload` and compare | The other addons are unchanged in both cases | |
