# Item Search feedback: spec

- **Feedback being answered:** `inputs/OWNER_FEEDBACK.md` (2026-11-25).
- **What it builds on:** the Item Search run, `docs/2026-11-25-ITEM_SEARCH/` (frozen; its spec is
  `03_SPEC.md` there). Anything this spec does not change stays as that spec and the merged code have
  it.
- **Mockups:** the Drop Watcher Item Search canvas, page **v2**
  (https://claude.ai/artifact/SdeXqCBDRn7kUgSyhELR5v). A local copy of every artboard is
  `inputs/mockup/` in this bundle. Where this text and a mockup disagree, this text wins.
- **Clients:** WoW Forever. Item Search stays absent on Retail (DropWatcher#18 tracks a Retail source).
- **Repos:** LibKa0s, DropWatcher, OutfitterReborn, SkillMaster. Branch
  `feat/2026-11-25-item-search-feedback` in each, built in scratch clones under
  `~/ka0s-scratch/isfb/`, never in the live repos (the game loads them).

Ids in brackets (T1, W8, G1) are the owner's items: T = tooltip, W = window, G = general.

## 1. The key that does nothing (T1)

**Cause.** `C.ITEM_SEARCH.DEFAULT_KEY` is `"CTRL-ALT-D"`. The client writes a chord with its
modifiers in the fixed order ALT, CTRL, SHIFT (the owner's `bindings-cache.wtf` has `ALT-CTRL-NUMPAD1`,
never `CTRL-ALT-…`), so a key press arrives as `ALT-CTRL-D`. `SetBinding("CTRL-ALT-D", …)` stores a
chord no key press ever matches, and `GetBindingAction("CTRL-ALT-D")` never sees what is really on
`ALT-CTRL-D`. The binding button itself is sound: the Show window key, built the same way, works on
the owner's `ALT-F8`.

**Fix.**
- `DEFAULT_KEY = "ALT-CTRL-D"`. A test asserts that every key constant the addon binds is in
  canonical order (the kit's chord builder orders `ALT-CTRL-SHIFT-META`).
- **Re-try once.** Every character already has `db.char.itemSearch.keyDefaulted = true` from the broken
  try. A new marker, `keyDefaultedV = 2`, makes the one-time default run again where it is missing,
  under the same rules (only on a free key, only if the binding has no key, out of combat). Before it,
  a binding that holds the dead chord `CTRL-ALT-D` is cleared (`SetBinding("CTRL-ALT-D")`), so the
  binding counts as keyless.
- **The tooltip hint names the real key.** `GetBindingKey` on the binding, written through
  `GetBindingText`, for example "Alt-Ctrl-D: open in Item Search". With no key bound the hint line is
  left out. The hint has its own setting (§7), on by default.

## 2. Objects with names (W15)

ForeverDB has object names: `D.obj[id] = { name, ... }` (for example `obj[153462] = {"Large Solid
Chest"}`). The library never read it, so Drop Watcher drew "Object 153462".

- **LibKa0s.** `LibKa0s-ForeverDB-1.0` minor 3 adds `Object(id)`, answering a new `{ id, name }` or nil
  (from `obj[id][1]`; a row that is not a table or has no string name is nil). Version-3 docs in
  `docs/api/ForeverDB/`, kit fake rows, tests. Nothing else in the surface changes. This is LibKa0s
  **v1.116.0**: version, CHANGELOG, a local tag only. `v1.115.0` is still unpushed, and both tags are
  pushed together on the owner's go-ahead. `docs/api/CONSUMERS.md` names Drop Watcher as ForeverDB's
  only consumer after this run.
- **Drop Watcher** re-vendors v1.116.0. Sources are built as follows:
  - each object source takes its name from `Object(id)`;
  - **objects with the same name become one row:** "Large Solid Chest" appears once, not six times.
    The merged row takes the highest chance of its parts, the union of their map spots, and records how
    many object ids it stands for (its row tooltip says "6 kinds of Large Solid Chest");
  - **an object with no name is dropped**, from both the tooltip and the window. Its count goes to the
    debug log, and is never shown as a row.

## 3. What is shown first: ranking (T3)

Each section has one pure ranking, `IS.Rank.<section>(rows, me)`. The tooltip and the window's
default sort ("Best for you") both use it. `me` is the context:
- `level`;
- `mapID` (the player's best map) and its zone and continent;
- `faction`;
- `ranks` (`{ [skillLine] = rank }`);
- `known(spell)`;
- `questState(id)`.

Each tier below is listed best first. Ties fall to the next rule, and then to the name.

| Section | Tier 1 | Tier 2 | Tier 3 | Last | Within a tier |
|---|---|---|---|---|---|
| **Drops from** (creatures, named objects, containers) | has a spot in your current zone | a creature in your level band, or an object or container (no level); see the band rule after this table | a creature outside the band | – | higher chance first, unknown chance last |
| **Sold by** | in your current zone | on your continent | elsewhere | a vendor your faction can't use (`nfac` says the other side) | unlimited stock before limited, then name |
| **Quests** (needs, rewards, starts) | in your log | can pick up now (your level ≥ its min level, not done) | too high for you now | completed | lower quest level first |
| **Crafting** (recipes using the item) | known, can skill up | known, no skill-up (gray) | not known, in a profession you have | a profession you don't have (filtered by §4, or last when the filter is off) | Known recipes: orange, then yellow, then green. Not-known recipes: the one whose yellow breakpoint is nearest your rank first. The shipped table's `min` is 1 for nearly every recipe, so it cannot order them. |
| **Skinned from** | has a spot in your zone | in your level band | others | – | higher chance first |

**The level band.** A creature is in your band if its level range overlaps
`[level − 5, level + 3]`. Mobs a little below you are easy to farm. Mobs well above you are not.

The window's sortable headers (§5.4) can override this order. The default and "Reset" restore it.

## 4. Only the professions you know (T3)

- One setting, `itemSearch.myProfessionsOnly`, **on** by default, covers both the tooltip and the
  window.
- **"Professions you know"** means the skill lines the player has a rank in (`ranks`). Before the
  player's skills are read, the filter lets everything through.
- **Tooltip.** Recipes in other professions are left out. One dim line under the Crafting rows says
  how many: "+48 in professions you don't know". If every recipe is filtered out, the Crafting heading
  shows that line alone, so the player still learns the item is a reagent. With the setting off,
  nothing is filtered, and the ranking puts the other professions last.
- **Window.** The Crafting tab starts filtered by the setting. Its section header has a toggle chip,
  "My professions" / "All professions", which changes this view only and is not saved. The tab's count
  shows the filtered number with the full number dim beside it: "Crafting 12 / 74".

## 5. The Item Search window

### 5.1 The frame (W1, W2, W3, W13, W14)

- **Title.** "Drop Watcher · Item Search", in the title font and size of Drop Watcher's main window.
- **The lock is gone.** So is the code behind it. The window is always movable by its title bar. The
  stored `locked` value is deleted by a schema step.
- **It is resizable.** A grip in the bottom-right corner resizes it.
  - Minimum 760 × 440, maximum the screen. The default is 980 × 600.
  - The size is saved with the position.
  - The right pane's tables reflow to the new size: some columns are fixed width and the rest flex
    (§5.4).
- **Footer.** ForeverDB's state alone ("ForeverDB 2026.11.25.48 · loaded"). The key hint is gone.
- **Fonts match Drop Watcher.** Every text in the window uses the font objects and sizes of Drop
  Watcher's main window, including the skin's font and its scale. That covers the item header (W3),
  the matches, the tabs and the tables. The header's name is the size of Drop Watcher's list-row
  titles, not `GameFontNormalLarge`. The builder reads `modules/` for the main window's sizes and
  reuses its helpers, never new numbers.

### 5.2 The left pane: search and matches (W4, W5, W6, W10)

- The search box and **Clear**. Clear is a LibKa0s Widgets button, so its label is centered (W6).
- A section header, **Matches**, styled as Skill Master's (§5.5), with the count ("Matches · 6") and
  one action: **Sort** (Best match, Name, Item id).
- **The matches list.** Each row has the icon, the name in its quality color, and the id dim on the
  right.
  - Rows alternate in color.
  - The hovered row is highlighted.
  - The **selected** row (the item shown on the right) has the LibKa0s selected-row look: gold in
    every skin, the 2026-11-24 ruling (W5).
  - Hovering a row shows the item's game tooltip.
  - Shift-click links the item in chat.
- **Recent searches are gone (W4).** That means the section, the list, the code that pushes to it, its
  saved store (deleted by a schema step), its setting and its locale strings.

### 5.3 The right pane: the item and its tabs (W7, W8)

- **The item header.** It shows the icon, the name in its quality color, and a dim line with the
  quality, class, subclass and id.
  - Hovering the icon or the name shows the item's game tooltip.
  - **Shift-clicking either links the item in chat (W7).**
  - The "Link in chat" button and its code are gone.
- **The tab strip** sits under the header. It is a LibKa0s tab widget, the same one Drop Watcher's
  main window uses.
  - There is one tab per section that has rows, in this order: Drops from, Sold by, Quests, Crafting,
    Skinned from. Each label carries its count, for example "Drops from 54".
  - "Rewards from" and "Starts a quest" join the **Quests** tab, as rows with a Role column (§5.4).
    They are not tabs of their own.
  - A section with no rows has no tab.
  - The tab shown is the one last picked, when the new item has it. Otherwise it is the first tab.
- An item that ForeverDB knows nothing about shows the existing empty notice under the header, and no
  tab strip.

### 5.4 The tables, one design per tab (W8)

Every tab is a table with its own columns, drawn in the shared table look:
- a header row with sortable column titles: clicking sorts, and clicking again flips the order;
- rows that alternate in color;
- a hover highlight;
- a tooltip on every row (§5.6);
- **no truncation while there is room:** fixed columns keep their width, and the flex columns (marked
  *flex*) share the rest, so a wider window shows whole names (W8, "use the space").

The default sort is "Best for you" (§3). The section header says which sort is in force.

**Drops from**

| Column | Content | Width |
|---|---|---|
| Source | the name; creatures in the hostile color, objects and containers in white; a container's name is its item link | *flex* |
| Type | Creature, Elite, Rare, Rare Elite, Boss (from `rank`), Object, Container | 80 |
| Level | "35" or "33–35"; dim "–" for objects and containers; colored by difficulty against your level (the game's quest-difficulty colors) | 64 |
| Zone | where it stands: the zone of its first spot in your zone, else the zone with the most spots; "+2 zones" when it stands in more than one; dim "–" when unknown | *flex* |
| Chance | a bar and the percent, "<0.1%" and "unknown" as today | 150 |
| (pin) | the waypoint button (§6), on rows with a spot | 28 |

**Sold by**

| Column | Content | Width |
|---|---|---|
| Vendor | the name, plus its subname on hover | *flex* |
| Level | the vendor's level | 56 |
| Zone | as for Drops | *flex* |
| Faction | Alliance, Horde, or both (`nfac`), with the faction icon; "can't buy" in red for the other side | 90 |
| Price | gold, silver and copper with coin icons (`vendx` price, else `vp`) | 110 |
| Stock | "∞", or "5 (restocks)" for limited stock (`vendx.s`) | 90 |
| Requires | `vendx.r`, for example "Requires Level 35"; dim "–" when none | *flex* |
| (pin) | waypoint | 28 |

**Quests**

| Column | Content | Width |
|---|---|---|
| (state) | the quest mark: ! in your log, ? can pick up, ✓ done; dim ? too high | 24 |
| Quest | the title, in the difficulty color for your level | *flex* |
| Role | Needs it (an objective, "Needs it ×10" when ForeverDB gives a count), Rewards it, Starts it (the item starts the quest) | 110 |
| Level | the quest level | 56 |
| Min | the level needed to pick it up | 56 |
| Status | In your log, Can pick up, Requires level 42, Completed | 130 |
| Giver | the first giver's name and zone | *flex* |
| (pin) | waypoint to the giver, when it has a spot | 28 |

**Crafting**

| Column | Content | Width |
|---|---|---|
| (glyph) | the recipe glyph (§5.7) | 24 |
| Recipe | the recipe name; white if known, gray if not | *flex* |
| Profession | the profession, with its icon | 140 |
| Uses | how many of this item one craft takes, "×4" | 56 |
| Makes | the product's icon and name, as an item link | *flex* |
| Skill | the breakpoints in their colors, "145 155 165 175" (orange, yellow, green, gray), "–" when unknown | 150 |
| Status | Known; Not known; "Learn at 165" only when the recipe's `min` is above 1 and above your rank; "No Blacksmithing" for a profession you don't have | 130 |

**Skinned from**

| Column | Content | Width |
|---|---|---|
| Creature | the name | *flex* |
| Level | as for Drops | 64 |
| Skill | the Skinning skill the creature needs: level × 5 above level 20; `(level − 10) × 10` from 11 to 20 (minimum 1); colored against your Skinning rank | 64 |
| Zone | as for Drops | *flex* |
| Chance | bar and percent | 150 |
| (pin) | waypoint | 28 |

The builder may move a column's width a little. It may not drop a column, unless the client gives no
data for it. In that case the column goes, and the execution record says why.

### 5.5 Section headers and actions, Skill Master style (W10)

Every block in the window has a section header the way Skill Master's rows do:
- a dark bar;
- the gold title;
- the count in dim text;
- action icons on the right, each with a tooltip.

Skill Master's shared header code is the model, through LibKa0s if it lives there. The blocks are:

| Block | Title | Actions |
|---|---|---|
| Left pane | **Matches** · n | Sort (menu: Best match, Name, Item id) |
| Right pane, above each table | the tab's full name · n, for example "Drops from · 54 sources" | **Filter** (a menu of toggles per tab, below), **Sort** (a menu of the table's sorts, with "Best for you" first), **Reset** (back to Best for you with no filters; shown only when something differs from the default) |

Each tab's filter toggles change the view only, and are not saved:
- **Drops:** Creatures, Objects, Containers, Only my zone, Only my level band.
- **Sold by:** Only my faction.
- **Quests:** Hide completed.
- **Crafting:** My professions / All professions (§4), Only known.
- **Skinned from:** Only my zone.

A filter that is on fills its icon with the accent, as Skill Master's does.

### 5.6 Tooltips everywhere (W9)

Every row, header action, tab, chip and button has a tooltip, under the Ka0s tooltip rules
(the standard's tooltip section, through LibKa0s Tooltip):
- a title line;
- label and value rows;
- dim hint lines last ("Shift-click: link in chat", "Click: set a waypoint").

Row tooltips:
- **Drops:** the name; the type and level; every zone with its spot count; the chance; for a merged
  object, "6 kinds of Large Solid Chest"; the hint lines.
- **Sold by:** the name and subname; the zone; the price; the stock; the requirements; the faction.
- **Quests:** the title; the role; the levels; the status; the giver and their zone.
- **Crafting:** the recipe; the profession; your rank against the breakpoints, in words ("Yellow: likely
  to skill up"); the reagents count; what it makes. Hovering the Makes cell shows that item's game
  tooltip instead.
- **Containers and products:** the item's game tooltip.

### 5.7 The recipe glyphs (T4)

These replace the dots, in the tooltip and the window alike, and come from LibKa0s's icon sets
(declared in Drop Watcher's `LibKa0s icons:` line):

| Recipe | Glyph | Color |
|---|---|---|
| known, can skill up | an up arrow (`arrow-up`) | its difficulty color: orange, yellow or green |
| known, no skill-up | a flat dash (a minus glyph) | light gray (`#b0b0b0`) |
| not known | a padlock (`lock`) | dark gray (`#5a5a5a`) |

The glyphs differ in shape as well as color, so they stay readable for color-blind players.

## 6. Waypoints (W11, W12)

- **The pin.** The white → is replaced by a map-pin icon (Phosphor `map-pin`), drawn dim and brightened
  on row hover. Its tooltip: "Set a waypoint", the place ("Hillsbrad Foothills 45.2, 61.8") and which
  arrow it uses.
- **Who draws the arrow.** A new setting, `itemSearch.waypoints`:
  - **Automatic** (the default): TomTom when it is loaded, else Drop Watcher's arrow;
  - **TomTom**: its row is disabled with a note when TomTom isn't loaded;
  - **Drop Watcher's arrow**.
- **Drop Watcher's arrow** is `LibKa0s-WaypointArrow-1.0`, already vendored in Drop Watcher and used
  by Skill Master the same way. Its settings rows (`WaypointArrowSettings`) go on the Item Search
  settings page under a "Waypoint arrow" heading.
- **The client's own user waypoint (`C_Map.SetUserWaypoint`) is no longer used.** It draws no arrow on
  Forever.
- A chat line confirms each waypoint set, as today.

## 7. The tooltip block (T2, T3, T4)

- **No magnifier** before "Drop Watcher · Item Search" (T2). The skin-colored rule and title stay.
- **The per-section cap.** A new setting, `itemSearch.tipRows`, default **5**, range 1 to 20,
  replaces the drops-only `dropsShown` (default 3). A schema step carries a stored `dropsShown` value
  across. The cap applies to every section: Drops from, Sold by, Quests, Crafting and Skinned from.
  Rows past it become "and N more" (§4's profession line is separate, and comes after it).
  The window is never capped.
- Rows come in §3's order, and recipes carry §5.7's glyphs.
- The key hint line follows §1: the real key, or no line. It has its own setting,
  `itemSearch.tipKeyHint`, on by default.

## 8. ForeverDB leaves Outfitter Reborn and Skill Master (G1)

The owner's answer: only Drop Watcher reads ForeverDB.

**Outfitter Reborn** (SF-OR-02 is retired):
- `ForeverDB` comes out of `## OptionalDeps`, and `core/ForeverDBSetup.lua` is deleted;
- the "Describe missing items from ForeverDB" row and its default, locale strings and tests are
  removed;
- `modules/OutfitTooltip.lua` keeps describing a missing item, but from the client's answer alone. When
  the client has not loaded the item, the name is drawn as it always was;
- a schema step deletes the stored key;
- the docs (README, ARCHITECTURE, settings docs, smoke rows) and the vendored-LibKa0s note are updated.

**Skill Master** (SF-SM-02 is retired; LibKa0s#105 stays closed, its library half lives on in Drop
Watcher):
- `ForeverDB` comes out of `## OptionalDeps`, and `modules/ForeverDBSources.lua` is deleted;
- a book rank's sources and a trainer's location come only from Skill Master's own seed data again,
  as before SF-SM-02;
- the setting, its default and its strings are removed;
- a schema step deletes the stored key;
- the tests and docs are updated.

Neither addon re-vendors LibKa0s for this. A vendored ForeverDB component nobody calls is harmless,
and the next collection re-vendor takes them to the current tag.

## 9. Settings: the Item Search page

These are added to or changed on the existing page. The full row list is the mockup's Settings
artboard.

**Tooltip block:**
- Show in item tooltips (kept);
- Comparison tooltips (kept, off);
- **Rows per section** (1–20, 5);
- **Show the key hint** (on);
- **Only professions you know** (on; also the window's default, §4).

**Window:**
- Show Item Search window (kept);
- the remember-the-tab behaviour has no setting, because it always remembers.

**Waypoints:**
- **Waypoints** (Automatic / TomTom / Drop Watcher's arrow);
- the **Waypoint arrow** block (LibKa0s rows), shown when Drop Watcher's arrow can be the one used.

**Removed:**
- Recent searches (and its count);
- Drop sources shown (replaced by Rows per section);
- anything that served the lock.

Every new key gets its `settings/Schema.lua` row, its default in `defaults/Profile.lua`, its
`docs/settings-panel.md` line and its locale strings, under the options-ui rules.

## 10. Tests and smoke

- **Every behavior above has a headless case** in Drop Watcher's suite (both kit profiles):
  - the chord constant and the re-try;
  - object naming and merging;
  - each section's ranking with invented contexts;
  - the profession filter and its count line;
  - the cap;
  - the glyph choice;
  - the tab set and order;
  - each table's columns and sorts;
  - the filters;
  - the waypoint method choice;
  - the schema steps;
  - shift-click linking (the chat-insert call stubbed).
- **Outfitter Reborn and Skill Master:** cases proving no ForeverDB read remains, and the schema steps.
- **LibKa0s:** `Object` cases and the docs-parity checks.
- **New smoke rows in each repo's `docs/smoke-tests.md`:**
  - Drop Watcher: ITEM-SEARCH-19 onward;
  - Outfitter Reborn and Skill Master: their ForeverDB-gone checks.

  These rows are written for the owner. Claude never marks them passed.

## 11. Not in scope

- The Retail source (DropWatcher#18).
- A "Made by" tab (recipes that produce the item). The recipe table could answer it, but it was not
  asked for. It is noted in the execution record as an idea.
- Changing how and when ForeverDB loads (the delayed load stays as it is).

## 12. Calls made without asking the owner

| Item | The call | Why |
|---|---|---|
| G1 | Outfitter Reborn and Skill Master keep their vendored LibKa0s, unchanged | Only Drop Watcher needs v1.116.0; re-vendoring two more addons widens the run for no behavior |
| T3 | Level band `[level − 5, level + 3]` | Easy-to-farm mobs a little under you are the useful ones; far above you is not farmable |
| T3 | One setting covers the tooltip's and the window's profession filter, plus a per-view chip in the window | The owner asked for both; one switch is less to learn |
| W8 | Rewards from and Starts a quest live in the Quests tab, with a Role column | Each has one or two rows at most; tabs of their own would be mostly empty |
| W12 | Automatic means TomTom first | A player who installed TomTom chose it |
| W14 | Minimum size 760 × 440 | The smallest size at which every table's fixed columns still fit beside one flex column |
| W15 | Same-named objects merge, and the highest chance wins | Same chest, different spawn ids; summing chances would mislead |
