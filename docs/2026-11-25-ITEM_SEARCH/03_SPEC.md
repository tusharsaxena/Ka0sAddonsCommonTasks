# Spec: Item Search

The owner decided the items marked **(owner)**. The lead decided the items marked **(lead)**; the owner may overturn any of
them at smoke. Anything not covered here is the builder's call, recorded in the commit message.

## 0. Facts this rests on (checked 2026-11-25)

- **Tooltip hook.** WoW Forever has `TooltipDataProcessor.AddTooltipPostCall`; ItemTree uses it there for item tooltips.
  The kit's Forever globals (Ketho `forever` e230342) keep `C_TooltipInfo`.
- **ForeverDB tables**, from its README's table reference at build v2026.11.24.46:
  - `qx[quest]` field 10 holds the quest's **item objectives**. As a check, quest 204 *Bad Medicine* lists item 2633 Jungle
    Remedy. Fields 1 and 2 are the race and class masks, fields 3 and 4 the prequests.
  - `rew[item]` is the quests that reward the item.
  - `start[item]` is the quest the item starts.
  - `skin[item]` is a flat `{npc, chance per 10000, ...}` list.
  - `item[id]` is `{name, quality, reqLevel, itemLevel, class, subclass, invType, icon, ...}`. It has 32,279 rows.
  - `sla[spell]` holds skill-line spells (recipes). For example `[171, 1, 55, 95, ...]` for Minor Healing Potion reads as
    profession 171, yellow at 55 and grey at 95.
  - **ForeverDB has no reagent lists.**
- **The adapter today.** `LibKa0s-ForeverDB-1.0` minor 1 has Available, IsLoaded, Status, Meta, NPC, Item, Quest,
  ItemSources, VendorPrice, Spots and TrainerSpells. It looks items up only by id.
- **Licensing.** ForeverDB is GPL-3.0 (`03_SPEC.md` §1 of `docs/2026-11-25-SEEDS_AND_FOREVERDB`). No ForeverDB row is ever
  copied into a repo; tests use invented fixture values. The recipe-reagent table comes from **Blizzard client DB2**
  (wago.tools, pinned by `?build=`), the same source as every other seed. It is not ForeverDB data.
- **Not regressing a merged feature.** Drop Watcher's merged SF-DW-01 Sources chip (`modules/ItemSources.lua`, the
  `window.itemSources` setting, painted by `modules/DetailCard.lua`) is deprecated here, not left beside the new feature.

## 1. Where Item Search exists

- **(owner) Name.** The feature is "Item Search". It is Drop Watcher's own; no other addon draws it.
- **(lead) Clients.** WoW Forever only. On Retail the tooltip block, the window, the header icon, the keybind's action
  and the settings page are **absent**, per clients-§4: no row, no default, no read. The keybind does nothing on Retail,
  and its `Bindings.xml` row may exist on both clients because the client reads one file for both. The feature is
  gated on `C.FEATURE` the way SF-DW-01 was.
- **(owner) Without ForeverDB, no tooltip block.** When ForeverDB is not installed or has not loaded yet, the tooltip
  shows **nothing** of Item Search (not even Crafting). The window still opens. It searches by item id and shows Crafting
  (from the shipped table), and says "ForeverDB not installed: drop sources, quests and name search are unavailable", or
  "ForeverDB: loading…" before the load (lead).

## 2. When ForeverDB loads (owner)

ForeverDB loads "a few seconds after login, out of combat".
- **The timer.** `PLAYER_ENTERING_WORLD` (first login or reload only) arms a timer: `C.ITEM_SEARCH.LOAD_DELAY`, 5 s.
- **When it fires.** Out of combat, it calls the adapter's `Available()`, the one place that loads. In combat, it waits for
  `PLAYER_REGEN_ENABLED` and tries again then.
- **Before the load.** Every Item Search read asks "loaded yet?" first and **never loads**. The tooltip block is absent and
  the window footer says "ForeverDB: loading…".
- **Opting out.** When the player has switched Item Search off entirely (both the tooltip block and the window), nothing
  loads.

## 3. LibKa0s: `LibKa0s-ForeverDB-1.0` minor 2

Rules 1–6 of the file header still hold: the first lookup loads, calls are Forever-only, globals are read bare at call
time, there's no pcall but every type is checked defensively, every answer is a fresh table, and ids are numbers.

These members are new:

| Member | Answer |
|---|---|
| `SearchItems(query, limit)` | Up to `limit` items (default 50) whose name contains `query`, case-insensitive, plain find, no patterns. Prefix matches come first, then shorter names, then id. A `query` that is all digits also matches that exact id first. Rows are `{ id, name, quality, icon, requiredLevel }`. With fewer than 2 characters it answers `{}`. The first call builds a lower-cased name index once a session, kept on the library; later calls only scan it. |
| `QuestsForItem(itemID)` | Quests whose item objectives (`qx` field 10) include the item, as `{ id, title, level, minLevel, races, classes, preQuests }`. `races` and `classes` are the masks; nil means any. `preQuests` is a merged array of fields 3 and 4. The first call builds the item→quests index once a session from `qx`. |
| `RewardFrom(itemID)` | Quests that reward the item: an array of `{ id, title, level }` from `rew`. |
| `StartsQuest(itemID)` | `{ id, title, level }` from `start`, or nil. |
| `SkinnedFrom(itemID)` | `{ { id, name, chance } ... }` from `skin`, sorted by chance as ItemSources sorts. `chance` is 0..1, or nil when the rate is unknown. |

- **Tests.** The kit fake `testkit/mock_foreverdb.lua` gains invented `qx`, `rew`, `start` and `skin` rows and a few
  more `item` rows for search. The kit revision goes up.
- **Docs.** `docs/api/ForeverDB/version-1-docs.md` documents each member and its degradation (missing → `{}` or nil). It
  also updates the consumer list: Drop Watcher, Skill Master and Outfitter Reborn are the runtime consumers, and Loot
  History and Bank Ledger no longer are. `docs/releasing.md` gets the same change.
- **Release.** LibKa0s **v1.115.0**, tagged locally only. The tag is pushed on the owner's go-ahead.

## 4. Drop Watcher

### 4.1 Re-vendor

Copy LibKa0s v1.115.0 `LibKa0s/` and `testkit/` whole, in the manner of `/dev-copilot:wow-revendor-libka0s`: provenance
line, icons declaration and prune. Only Drop Watcher re-vendors in this run.

### 4.2 The recipe-reagent table (owner: "A with a B fallback")

- **Generated by** `tools/seeds/` (extending the existing `seeds.py`, or a sibling script it drives) from wago.tools DB2
  for the **wowf** build, pinned with `?build=`, the same build the run's seeds used. It joins these tables:
  - `SkillLineAbility`: recipe spell, skill line, `MinSkillLineRank`, `TrivialSkillLineRankLow` and
    `TrivialSkillLineRankHigh`. Only crafting professions are kept: Alchemy, Blacksmithing, Enchanting, Engineering,
    Leatherworking, Tailoring, Cooking, First Aid and Jewelcrafting if present. The builder lists the skill-line ids
    actually present.
  - `SpellReagents`: up to 8 reagents and counts.
  - `SpellEffect` effect 24 (`CREATE_ITEM`): the item the recipe makes, when there is one.
  - `SpellName`: the recipe's name.
- **Shipped as** a generated Lua data file (`data/RecipeReagents.lua`, or the folder the addon uses for generated data).
  - It is shaped for the lookup Item Search makes, **reagent item → recipes**:
    `[reagent] = { spell, ... }`, plus `recipes[spell] = { skillLine, min, yellow, grey, made, name, reagents = {...} }`.
  - The data sits inside a function body that runs only on WoW Forever, the first time Item Search asks. On Retail it is
    never built.
  - The header records the build, the date and a sha256 of the inputs.
- **Validation.** Drop Watcher's `docs/validate-seeds.md` gains a *recipe reagents* seed with a gate test. The test checks
  that the data file matches the generator's output for the recorded build, so a hand edit is caught.
- **Skill-up colour (lead).** Below `yellow` it is orange, from `yellow` it is yellow, from `green` it is green, and from
  `grey` it is grey. `green = floor((yellow + grey) / 2)`, the classic rule.
  - `yellow` is `TrivialSkillLineRankLow` and `grey` is `TrivialSkillLineRankHigh`. These match ForeverDB `sla` positions
    3 and 4; the builder checks a sample against `sla` with the dev-time helper and records the check.
  - The player's rank in the profession comes from the client's skill lines (Forever: `C_SkillInfo.GetSkillLineInfo` /
    `GetSkillLineInfo`; the builder picks what the Forever globals hold).
  - Whether you know the recipe comes from `IsPlayerSpell(spell)`, falling back to `IsSpellKnown`.
- **Fallback, B.** When a profession window is open (Forever's trade-skill API; the builder picks from the Forever
  globals), Drop Watcher reads each listed recipe's reagents. Any recipe **the shipped table lacks** goes into
  `global.itemSearch.learnedRecipes[spell] = { skillLine, reagents, made, name, build }` (account-wide). Item Search
  consults it after the table. Entries are dropped when the shipped table later covers the spell. This is out of combat
  only, and runs only when Item Search is on.

### 4.3 The model (pure)

`NS.ItemSearch.Facts(itemID, ctx)` returns:

`{ item, drops, dropMore, worldMinLevel, vendors, quests, crafting, rewardFrom, startsQuest, skinnedFrom, fdb = "loaded"|"loading"|"missing"|... }`

- **Drops and vendors** reuse the SF-DW-01 model: the merged, sorted sources from `ItemSources`.
- **Quests** come from `QuestsForItem`, filtered by the player's race and class masks. Each gets `state`:
  - `"log"` from `C_QuestLog.GetLogIndexForQuestID`, or the Forever equivalent;
  - `"done"` from `C_QuestLog.IsQuestFlaggedCompleted`;
  - otherwise `"todo"`.
- **Crafting** rows come from the table plus the learned recipes: `{ spell, name, skillLine, known, colour, rank, min,
  yellow, green, grey }`.

The model is cached per item for the session, except the quest state and crafting colour, which are read live.

### 4.4 The tooltip block (owner: every item tooltip)

- **Hook.** `TooltipDataProcessor.AddTooltipPostCall(Enum.TooltipDataType.Item, fn)`, registered once at login on
  Forever. This covers chat links (`ItemRefTooltip`), bags, the loot window, comparison tooltips and other addons'
  `GameTooltip`. Shopping/comparison tooltips get the block only when the setting allows (owner: off by default for
  comparison tooltips, a setting turns it on).
- **What it adds**, per the mockup board 1 and in the settings' section order:
  - a separator line, a texture line or `AddLine` of rule glyphs, in the **skin accent** read from Drop Watcher's skin at
    call time;
  - the title line, "Drop Watcher · Item Search", with the magnifier icon in the accent;
  - the sections the player switched on;
  - the hint "<key>: open in Item Search", which names the actual bound key and is left out when unbound.

  The Quests marks are `!` / `?` / `✓`. The Crafting marks are `●` (coloured) and `○`.
- **It is never added twice** to one tooltip show. It guards on the tooltip and item id, and resets on the tooltip's
  `OnHide` / `OnTooltipCleared`.
- **Secret-safe.** It reads only `data.id` / the hyperlink, never other lines' text (client-quirks: tooltip text can be
  secret).
- **It never loads ForeverDB** (§2) and never errors on missing data; an empty section is left out.
- **Performance.** It works from the cached model. The first build of the quest and name indexes happens at the §2 load,
  not on a hover. The perf scenario covers a hover on a cold and a warm cache.

### 4.5 The Item Search window (owner)

- A Drop Watcher standalone window, laid out as mockup board 2. It uses Drop Watcher's window chrome, skin, lock and
  position save, and follows the standalone-windows rules. It's a **companion** window, so it has no second settings mark
  if that's how HeaderButtons treats companions; the builder follows the existing companion pattern (FB-DW-01).
- **Ways in:**
  - a new magnifier extra in the main window's header (`modules/WindowTitleBar.lua` `spec.extras`), with the tooltip
    "Item Search";
  - the keybind (§4.6);
  - a slash verb, `/dw search [name|id]` (lead), listed in help and in the slash-dispatch doc.
- **Search.** An edit box for a name or id, with a debounce of `C.ITEM_SEARCH.DEBOUNCE` (0.25 s).
  - All digits: look up that id directly (works without ForeverDB, using the client's item info; it shows a row for an
    item cached on the client).
  - Otherwise: `SearchItems`. The matches list shows icon, name in quality colour and id. Clicking a match shows it.
    Enter shows the first match.
  - Recent searches: the last 10 shown items, stored in `char` or `global` (lead: `global`), each clickable. They follow a
    "remember recent searches" switch.
- **Detail pane sections:**
  - **DROPS FROM** lists every source, not just the top 3. Each row has the name (creature, object or container),
    level range (creatures, from `NPC`), zone (from `Spots`, the first map, named through `C_Map.GetMapInfo`), a bar
    scaled to the highest chance, the %, and a waypoint pin. The pin sets `C_Map.SetUserWaypoint` (if Forever has it)
    or uses TomTom when it is installed, and is hidden when there's no spot. A World drop row shows its minimum level.
  - **SOLD BY** lists vendors with the lowest price seen.
  - **QUESTS**, **CRAFTING** and **ALSO** as in the mockup.
- **Footer.** The ForeverDB version and state, and the keybind hint.
- **Link in chat** inserts the item link into the chat edit box.
- **Settings it obeys:** bar colour (skin, or custom), density, font size, the zone and level columns, waypoint pins and
  recent searches.

### 4.6 The keybind (owner)

- **The binding.** A new `Bindings.xml` row, `DROPWATCHER_ITEMSEARCH`, labelled "Item Search" in the Drop Watcher
  category. It sits beside the existing window toggle, which is unchanged.
- **Default Ctrl-Alt-D**, set once per character, only when `GetBindingAction("CTRL-ALT-D")` is empty. This follows
  ItemTree's rule of never stealing a key, and the existing Drop Watcher keybind code if it has one. The player can rebind
  it in the client's Key Bindings, and the settings page shows the current key with a button that opens that screen or
  captures a key, matching what Drop Watcher already does for its window toggle.
- **On press:**
  - if an item tooltip is showing (`GameTooltip`, `ItemRefTooltip` or the comparison tooltips, whichever is visible and
    has an item), open the window with that item prefilled and shown;
  - otherwise, open the window empty with the search box focused.
  - (owner) While the window is open: pressed over the item already shown, or with no item tooltip showing, it closes
    the window. Pressed over a different item, it switches to that item.

### 4.7 Settings (owner)

- **A new "Item Search" page**, laid out as mockup board 3 (Forever only). The schema rows are listed below; the builder
  names keys in the schema's style. Every row has a default and a docs/settings-panel.md entry.

  | Setting | Default |
  |---|---|
  | Add Item Search to item tooltips | on |
  | Only while holding Shift | off |
  | Separator and title line | on |
  | Keybind hint line | on |
  | Section switches: Drops from, Sold by, Quests, Crafting, Reward from / starts quest | on, on, on, on, off |
  | Section order | the default order |
  | Drop sources shown | 3, range 1–10 |
  | Hide completed quests | on |
  | Comparison tooltips too | off |
  | Item Search window: bar colour follows the skin | on |
  | Item Search window: custom bar colour | – |
  | Item Search window: density | comfortable |
  | Item Search window: font size | 13, range 10–16 |
  | Item Search window: zone and level columns | on |
  | Item Search window: waypoint pins | on |
  | Item Search window: remember recent searches | on |
  | Keybind row | shows and changes the binding |

- **Section order (lead).** If the settings widget set has no reorder control, order is fixed: Drops, Sold by, Quests,
  Crafting, Also. That is recorded as a deviation.

### 4.8 Deprecating the old Sources chip (owner)

- **Removed:**
  - the detail card's Sources chip and its painting in `DetailCard.lua`;
  - the `window.itemSources` row and default;
  - the chip's pure functions that Item Search does not reuse.
- **Kept:** the model the tooltip and window reuse (§4.3), moved under Item Search.
- **Migration.** A schema migration removes `window.itemSources` from saved profiles, as the next migration step.
- **Docs.** The detail card docs and the smoke rows for the chip (FOREVER-18 and FOREVER-19 in the 2026-11-25 sheet) are
  superseded by Item Search rows.

### 4.9 Docs and gate

Update every doc that the standard's documentation section requires to stay true:
- README (feature list, keybinds, slash verbs);
- `docs/settings-panel.md`, `docs/schema.md`, `docs/module-map.md` and `docs/ARCHITECTURE.md`;
- `docs/slash-dispatch.md`, `docs/test-cases.md`, `docs/smoke-tests.md` and `docs/performance.md` (memory and CPU
  budgets for the hook and the reagent table);
- `docs/forever-quirks.md`, which gets one row for the tooltip hook as used on Forever, marked assumed until probed;
- the locales, every new string in enUS.

The gate is the CLAUDE.md gate on both kit profiles, plus the seed tests.

## 5. Loot History: remove its Item sources (owner)

Remove SF-LH-02 completely:
- `modules/ItemSources.lua`;
- its calls from `modules/BrowserTable.lua`;
- `core/ForeverDBSetup.lua`;
- the setting row, the default and the locale strings;
- ForeverDB from `## OptionalDeps` and from `.pkgmeta` `optional-dependencies` (if listed);
- the tests (`test_itemsources.lua` and the ForeverDB parts of the other tests);
- the doc mentions: README, ARCHITECTURE, module-map, browser, performance, testing, test-cases, smoke-tests and
  DEPENDENCIES.

Also:
- **Migration.** A schema migration removes the saved setting key.
- **Still kept:**
  - the dev-time ForeverDB evidence in `docs/validate-seeds.md` and the frozen `docs/seed-research/` bundles;
  - the vendored LibKa0s, whose payload is whole.
- **The result.** The History tooltip is exactly what it was before SF-LH-02. With Drop Watcher installed, Drop Watcher's
  block appears on it like on any other item tooltip.
- **Revendor bundle.** `docs/revendor/2026-11-25-v1.114.0` is frozen and stays. Add a line to the next revendor's notes
  only if one is written.

## 6. Bank Ledger: remove its vendor buy price (owner)

Remove SF-BL-01 completely:
- the tooltip price line;
- the setting row, default and locale strings;
- `core/ForeverDBSetup.lua`;
- ForeverDB from `## OptionalDeps` and `.pkgmeta`;
- `tests/test_vendor_buy_price.lua` and the ForeverDB parts of other tests;
- the doc mentions: README, ARCHITECTURE, module-map, performance, settings-panel, schema, test-cases and smoke-tests.

Also:
- **Migration.** A schema migration removes the saved key.
- **The result.** Bank Ledger on WoW Forever behaves as it did before SF-BL-01.

## 7. Smoke

These checks go in a new sheet, `Documents/Ka0sPendingSmoke-2026-11-25-ITEM-SEARCH.csv`, in the same columns as the
2026-11-25 sheet:
- the tooltip block on every source: bags, chat link, loot window and another addon's tooltip, such as Loot History's;
- the block's sections and their marks;
- Shift-only;
- before and after the 5-second load, and a login while in combat;
- running without ForeverDB (Crafting only);
- Retail, where everything is absent;
- the window: icon, keybind with and without a hover, name and id search, bars, pins, recent searches, Link in chat;
- the keybind default not stealing a bound key;
- the settings;
- the old chip gone from the detail card;
- Loot History's own block gone;
- Bank Ledger's price gone;
- the profession-window fallback.

In the 2026-11-25 seeds sheet, the superseded rows are marked "superseded by ITEM-SEARCH" rather than deleted:
SEEDS-LH-1 and SEEDS-LH-2, Bank Ledger FOREVER-20, FOREVER-21 and FOREVER-22, and Drop Watcher FOREVER-18 and
FOREVER-19.

## 8. Owner answers (2026-11-25, before the build)

- **Retail:** "Forever only, file a github issue to find an equivalent for retail". That issue is DropWatcher#18.
- **Without ForeverDB, or before it loads:** the tooltip shows nothing (§1).
- **Comparison tooltips:** off by default (§4.4).
- **Keybind while the window is open:** it closes when pressed over the same item or with no tooltip, and switches when
  pressed over a different item (§4.6).
