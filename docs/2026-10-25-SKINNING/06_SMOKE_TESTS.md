# Smoke tests — owner, in game (leg 1, LootHistory)

Mark each row **pass** / **fail** with a note. Only the owner marks rows. Setup: LootHistory and LibKa0s on
`feat/2026-10-25-skinning` (the game loads `GIT/LootHistory` through its symlink), `/reload`.

| Id | Check | Expect | Result |
|---|---|---|---|
| SK-01 | Open the History window with the skin left at **Ka0s Default** | Looks exactly as before this run: window, tabs, filter bar, table, Export, Insights, Timeline, Holdings, settings pages | |
| SK-02 | Settings → LootHistory → General → **Appearance** tab | Sits after Interface, before Keybindings; shows Skin source, the nine skins with swatches, Copy to every Ka0s addon, the HUD note | |
| SK-03 | Pick each skin in turn with the History window open (Obsidian, Azeroth, Glass, High Contrast, Ember, WoW Default, WoW Midnight, WoW Forever, back to Ka0s Default) | Window, table rows (scroll to see pooled rows), tabs, buttons, search, dropdown and its menu, footer, Export, Insights cards/charts, Timeline, Holdings all repaint **without a reload**; text stays readable | |
| SK-04 | With a non-default skin, open the settings pages of LootHistory **and** another Ka0s addon (e.g. BankLedger) and another AceGUI addon | LootHistory's pages (nav rail, tabs, headings, checkboxes, sliders, dropdowns, edit boxes, drawers) are skinned; the other addons' pages are **stock**, including after flipping back and forth between them (AceGUI pool leak check) | |
| SK-05 | WoW Forever skin | Warm charcoal panels, black title bars with centered white titles, tan accent, gold headings, thin borders, Barlow font | |
| SK-06 | High Contrast skin | Black/white/yellow, larger Atkinson text, selected row outlined in yellow | |
| SK-07 | Fonts | Barlow / Cinzel / Atkinson render (no fallback squares) on an English client | |
| SK-08 | Debug console (`/lh debug`), the sim/test strip, a copy window | Follow LootHistory's skin | |
| SK-09 | EllesmereUI loaded, third-party skinning on, LootHistory on in its Third-Party list | Appearance → Skin source **EllesmereUI** enabled; choosing it repaints in the EllesmereUI look live | |
| SK-10 | Turn LootHistory off in EllesmereUI's Third-Party list (or disable EllesmereUI) and reload | The EllesmereUI choice is disabled with the failing condition and its fix listed; LootHistory falls back to its Ka0s skin | |
| SK-11 | Switch from EllesmereUI back to a Ka0s skin | A reload is offered; after reload the Ka0s skin shows | |
| SK-12 | Copy to every Ka0s addon | Confirmation names the registered addons (only LootHistory adopts skins in leg 1, so it says so); nothing else changes | |
| SK-13 | Profile switch / reset in LootHistory's Profiles | The skin follows the profile | |
| SK-14 | Combat: change skin in combat | No Lua error, no taint warning; settings page behaves as other settings in combat | |
