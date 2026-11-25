# Item Search (2026-11-25)

Tracked as DropWatcher#17. On 2026-11-25 the owner asked to move Loot History's ForeverDB "Drops from" tooltip block into
Drop Watcher. There it grows into **Item Search**: facts about any item on every item tooltip, plus a searchable
window. The owner's messages, in order:

- "Lets move this functionality to DropWatcher instead of LootHistory". They want it on every item tooltip, with a skin-coloured
  separator and a Drop Watcher title line, and a drop-sources window with a search box (name or id) and bars. It opens from a
  header icon and from a hover keybind (Ctrl-Alt-D) that prefills the item, and has settings for the window and the
  tooltip. "Remove this functionality from LootHistory".
- "Remove the vendor price bit from Bank Ledger - theres tons of other addons that provide this".
- On the existing feature: rename it ("Sources", then "Item Search"), and deprecate Drop Watcher's existing Sources chip for the
  new feature. Load ForeverDB "a few seconds after login, out of combat".
- Is an item needed for a quest (in your log, or not picked up yet)? Is it used in a crafting recipe, known or not? For a
  known recipe, what skill-up colour? Also add a dedicated Item Search keybind: the same key over a tooltip prefills the
  item, and with no tooltip it opens the window empty.
- On crafting data: "A with a B fallback". That means a recipe-reagent table generated from the Forever client's game data,
  falling back to reagents learned from profession windows the player opens.
- On the mockups (`inputs/MOCKUP.md`): "Mockups look good, go ahead and build this".

| Repo | What this run does |
|---|---|
| LibKa0s | `LibKa0s-ForeverDB-1.0` minor 2: item-name search and the item facts Item Search needs (quests that need an item, quest rewards, quest starters, skinning) |
| DropWatcher | Item Search: the tooltip block, the window, the keybind and the settings page; a generated recipe-reagent table; the old Sources chip removed |
| LootHistory | its ForeverDB "Drops from" tooltip block and setting removed, and with them its runtime use of ForeverDB |
| BankLedger | its ForeverDB vendor buy price removed, and with it its runtime use of ForeverDB |

Read in order: `03_SPEC.md`, then `04_EXECUTION_PLAN.md`, then `plan-data/items.tsv`, then `RESUME.md`.
