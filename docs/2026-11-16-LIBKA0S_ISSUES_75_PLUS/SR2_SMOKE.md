# Smoke round 2: re-smoke sheet

This sheet covers what changed for `SR2_SMOKE_ROUND2.md`'s rulings. The owner runs the checks in game and
records **PASS**, **FAIL** (with a note) or **N/A**. The run never marks a check passed by itself.

Run each check on Retail and WoW Forever wherever the addon ships on both. Checks that passed in
`SR1_SMOKE.md` are not repeated.

| Id | Where | Check | Retail | Forever |
|---|---|---|---|---|
| SR2-HOV | Combat Trail's title bar (or any window's), in all nine skins | Hover a title-bar mark: it turns a clearly different color from its gray rest, with the glow kept. The four skins re-tuned: **Azeroth** bright yellow, **Glass** cyan, **WoW Midnight** gold, **WoW Forever** amber. The X still turns red. | | |
| SR2-EDGE | The skin picker or any window, in **WoW Midnight, Azeroth and Ember** | The window border is one thin 1px line, as in WoW Forever: Midnight gold, Azeroth gold, Ember amber. There is no second inner line. | | |
| SR2-POP | A dropdown menu and a popup (for example the skin picker's skin list), in **Azeroth and WoW Midnight** | The menu and popup borders are 1px, the same as the window's. Glass and WoW Default still draw their art frames. | | |
| SR2-FOOT | The skin picker's **Apply to all Ka0s addons**, and the icon browser's Choose / Cancel, in all nine skins | On hover, the glow stays and the label changes to a clearly different color. | | |
| SR2-PRI | The skin picker's **Apply** (the highlighted button), in all nine skins | On hover, the button's **background** turns a clearly different shade, the glow stays and the label keeps its color. Look hardest at Ember, Obsidian, Glass and WoW Forever, which showed almost no change before. | | |
| SR2-SIM | Any addon's sim panel (`/<addon> sim`), in Ka0s Default | Start and the step controls hover **orange** (the link color), where they hovered gold before. | | |
| SR2-STP | Skin Tester `/st show`, the "(Scope: panel)" samples | With your profile not having set it, General → Skin → Scope → **Ignore settings panel** is now **off**. Ka0sMedia_Font, Ka0sMedia_StatusBar and the AceGUI dropdown show **skinned**, like Dropdown and WowStyle1DropdownTemplate. Turning the option on makes them stock again. | | |
| SR2-RV | Every addon | Loads with no Lua error, its windows open, and test or sim mode works. | | |

## Not changed, by the owner's answers

- The HUD drag strips of Aura Master, Absorb Tracker, Consumable Master and Kick CD keep their tooltip
  **beside** the strip.
- Skill Master's block-header marks rest **gray**.
