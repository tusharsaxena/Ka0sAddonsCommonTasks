# Item Search round 3: spec

- **Feedback being answered:** `inputs/OWNER_FEEDBACK.md`: the owner's 14 items, numbered 1 to 14 here as
  there, and their answers to the recon's questions.
- **Evidence:** `inputs/RECON.md`, which has the measured counts and the file:line references this spec
  leans on. Line numbers there are at DropWatcher `b1113a6` and LibKa0s `0be9a569`.
- **What it builds on:** the feedback run, `docs/2026-11-25-ITEM_SEARCH_FEEDBACK/03_SPEC.md` (frozen).
  Anything this spec does not change stays as that spec and the merged code have it.
- **Clients:** WoW Forever. Item Search stays absent on Retail (DropWatcher#18).
- **Repos:** LibKa0s and DropWatcher. Branch `feat/2026-11-25-item-search-round3` in each, built in the
  scratch clones `~/ka0s-scratch/isr3/LibKa0s` and `~/ka0s-scratch/isr3/DropWatcher`, never in the live
  repos (the game loads them).
- **Licences.** ForeverDB's data is GPL-3.0: no row of it is copied into either repo, its tests or its
  docs. Counts, table names, row shapes and ids named as examples are fine. ItemTree is All Rights
  Reserved: none of its code or art is ported. Where this spec borrows an idea from it (a first-line badge
  opposite the addon's name, a hairline divider), the design and the code are Drop Watcher's own.

**Owner decisions taken into this spec:**

| Item | Decision |
|---|---|
| 3 | Dropped. The Skill column stays as it is. |
| 6 | Color source names and the Type column by rank. Objects stay plain. |
| 8, 10 | Convert `spw` world coordinates to map positions, and also read ForeverDB_Full's `spz` when it is installed. |
| 14 | A badge with the verdict (Keep / Hold / Sell / Toss), a 0 to 100 score, a confidence (High / Medium / Low; Low never says Toss) and reason lines. |
| 5 | The headers are already clickable but didn't look it. Add a hover highlight and LootHistory's arrow (item 11). |

## 1. LibKa0s: `LibKa0s-ForeverDB-1.0` minor 4 (ISR3-LK-01)

`libs/LibKa0s/ForeverDB.lua` (`LibKa0s/ForeverDB.lua` in the library repo) goes from minor 3 to **4**.
Every minor-3 member keeps its signature and its answers for any input minor 3 answered, except where
this section says otherwise. The six rules in the file header still hold, with rule 1 extended as in §1.4.

### 1.1 Where a creature or an object stands: `Spots(kind, sourceID)`

The answer's shape is unchanged: a new table `{ [uiMapID] = { { x = 0..1, y = 0..1 }, ... } }`, or nil.
There is a **second return**, `origin`, which is the table the answer came from: `"spz"`, `"spm"` or
`"spw"`. Callers that take one value are unaffected.

The order is:

1. **`ForeverDBFull.spz["c<id>" | "o<id>"]`**, when ForeverDB_Full is loaded (§1.4). It has the same
   shape as `spm` (`{ [uiMap] = { x, y, x, y, ... } }` on 0..1000) and holds 16536 keys, a superset of the
   base slice for every source the recon checked.
2. **`ForeverDB.spm[...]`**, the base slice, read as minor 3 reads it. It is capped at 5000 keys.
3. **`ForeverDB.spw[...]`**, world coordinates, converted by `WorldToMap` (§1.2). Each entry is a list of
   runs, `{ { continent, worldX, worldY, worldX, worldY, ... }, ... }`. Each point is converted on its
   own, and the points are grouped under the uiMap each one lands on. A point that converts to no map is
   skipped. If no point converts, the answer is nil.

Values off the scale are skipped, as in minor 3. The answer is always a fresh table (rule 5). The
converted `spw` answer is memoized per key for the session, in the same way as the minor-2 indexes: the
memo is keyed by the `spw` table it was built from, and each answer is a copy of it.

### 1.2 World to map: `WorldToMap(continent, worldX, worldY)`

This is a new, pure member. It answers `uiMapID, x, y` (with x and y on 0..1), or nil. It reads only
ForeverDB's `umaa` and `zbord` tables:

- **`umaa`** (61 rows) holds one row per map assignment:
  `{ uiMap, continent, areaID, uiMinX, uiMinY, uiMaxX, uiMaxY, minX, minY, minZ, maxX, maxY, maxZ }`.
  That layout was measured on the 2026-11-25 build.
- **`zbord[areaID]`** holds `{ c = continent, m = { polygon, ... } }`, where each polygon is a flat
  `{ x, y, x, y, ... }` on that zone's own 0..1000 map scale. 48 of the 61 `umaa` rows have one.

**The conversion.** Take a `umaa` row `r` whose continent is `continent` and whose region contains the
point (`minX ≤ worldX ≤ maxX` and `minY ≤ worldY ≤ maxY`). Then:

```
u = (maxY − worldY) / (maxY − minY)        -- world Y runs east to west; map x runs west to east
v = (maxX − worldX) / (maxX − minX)        -- world X runs south to north; map y runs north to south
x = uiMinX + u · (uiMaxX − uiMinX)
y = uiMinY + v · (uiMaxY − uiMinY)
```

**Which map, when several regions contain the point.** Zone rectangles overlap, so:

1. Among the containing rows that have a `zbord` polygon for their `areaID`, take the smallest-area row
   whose polygon contains `(x·1000, y·1000)`. The test is even-odd point in polygon.
2. Otherwise, take the smallest-area containing row that has no `zbord` entry. This is normally the
   continent map, so the pin is still at the right place in the world.
3. Otherwise, the answer is nil.

**Measured offline, on the installed 2026-11-25 build, over the 1517 keys in both `spm` and `spw`.** The
scripts are read-only on the client folder, run from the builder's scratchpad, and are not in any repo.

- The axis order is the one above. Swapping the axes puts the median point 25% of a map width away.
- Converted points land a median 0.31% of the map width from the nearest `spm` point (p90 1.24%).
- The map pick agrees with `spm` on 1417 keys (93.4%), differs on 97 and finds no map on 3. A
  rectangle-only pick agrees on 69%.
- Coverage gained: 14360 `spw` keys have no `spm` row, and 11615 of them convert.

ISR3-LK-01 re-runs this measurement and writes the numbers into the version-4 docs and the execution
record. The numbers only, never a row.

**`C_Map.GetMapPosFromWorldPos`** is not used by the adapter. The adapter stays pure, so it works
headless and needs no client map API, which is unprobed on Forever. A smoke row (ITEM-SEARCH-39)
compares the two answers in game for three named sources.

### 1.3 Vendor prices: `vendx`

- **`VendorPriceAt(npcID, itemID)`** is new. It answers `price, origin`: from `vendx[npc][item].p` (origin
  `"vendx"`), else from `vp[npc][item][1]` (origin `"vp"`), else nil. The price is in copper.
- **`VendorPrice(itemID)`** now takes the lowest across both tables for every vendor in `vend[item]`. The
  first vendor in `vend`'s order still wins a tie. Its two returns are unchanged.
- `vendx` holds 6 vendors and 60 entries, and `vp` holds 32 vendors and 443 entries. Both are sparse,
  which is why Drop Watcher records prices itself (§4.4).

### 1.4 ForeverDB_Full, on demand only

ForeverDB_Full is a LoadOnDemand addon that sets the global `ForeverDBFull`. It is 7 files and about 20 MB
of Lua.

- **`FullStatus()`** never loads anything. It answers `"loaded"`, `"available"` (installed and loadable),
  `"missing"`, `"disabled"`, `"client"` (not Forever) or `"base"` (the base ForeverDB is not available).
- **`LoadFull()`** is the only caller of `C_AddOns.LoadAddOn("ForeverDB_Full")`. It answers `ok, reason`.
  - It refuses with `"combat"` while `InCombatLockdown()` answers true. That refusal is not cached, so a
    later call can try again.
  - It refuses with `"base"` unless `Available()` answers true.
  - It refuses with `"missing"` or `"disabled"` as `FullStatus` reports.
  - Otherwise it loads once per session. A success or a failure is then cached, as `Available`'s is.
  - It measures the load: `collectgarbage("count")` before and after (in KB), and `debugprofilestop()`
    before and after (in ms) when that function exists. The result is kept for `FullCost()`.
  - If `ForeverDBFull` is still not a table after a successful load, it answers `false, "reshaped"`.
- **`FullCost()`** answers a new `{ kb = n, ms = n|nil }`, or nil before a load.
- Rule 1 of the file header becomes: *the first lookup loads the base addon (`Available()` is its only
  loader); ForeverDB_Full loads only when a host calls `LoadFull()`, never in combat, and nothing loads at
  file load or at login*. Rule 3 now also covers `ForeverDBFull`, read bare and at call time.
- `Status()`, and the diagnostics line it feeds, add the Full state. Examples: `ForeverDB 4 · Full
  loaded (19.6 MB, 840 ms)` and `ForeverDB 4 · Full available`.
- The library never decides **when** to call `LoadFull`. That is the host's policy (§4.6).

### 1.5 Docs, kit and tests

- `docs/api/ForeverDB/version-4-docs.md` (every member, with `Spots`' order, the conversion formula, the
  map pick, the measured numbers and the Full rules), and `members-4.json` written by
  `lua tools/gen-api-members.lua`.
- The header comment's history paragraph gains minor 4. The "ForeverDB_Full is a later minor" sentence is
  removed.
- `docs/api/CONSUMERS.md`: Drop Watcher is still the only consumer, and it now uses `LoadFull`,
  `VendorPriceAt` and `Spots`' origin.
- **Kit revision 65** (`testkit/mock_foreverdb.lua`, invented data in ForeverDB's shape). It adds:
  - `umaa` rows for an invented continent: a continent map and two overlapping zone maps;
  - `zbord` polygons for the two zones;
  - an `spw` entry for a fixture creature with no `spm` row, with points in each zone, in the overlap and
    on the continent map;
  - a `vendx` row for a fixture vendor;
  - a fake `ForeverDB_Full` that `C_AddOns.LoadAddOn` can load, which installs `ForeverDBFull` with an
    `spz` row that differs from that source's `spm` row.

  Every earlier fixture row is unchanged. `tests/_kit/` is re-synced, and
  `docs/api/testkit/version-65-docs.md` is written.
- `tests/test_foreverdb.lua` (or a new `tests/test_foreverdb_spots.lua`, to stay under the 1500-line cap)
  covers:
  - each origin, and the precedence `spz` > `spm` > `spw`;
  - the formula, on hand-computed invented points;
  - the overlap pick, the no-polygon fallback and nil off every region;
  - malformed `umaa`, `zbord` and `spw` rows;
  - the memo returning fresh tables;
  - `VendorPriceAt`'s two origins and `VendorPrice`'s lowest-of-both;
  - `LoadFull` refusing in combat (not cached), then loading, its single-load rule, its cost and
    `"reshaped"`;
  - `FullStatus` never loading;
  - the "ForeverDB 4" diagnostics line;
  - minor 4 and its member list.
- `tests/test_kit_inventory.lua` pins revision 65.
- Gate: both kit profiles, `luacheck` 0/0, `pytest tools/seeds`, the 1500-line cap, and CCN ≤ 15 on every
  new or changed function.

## 2. LibKa0s v1.117.0 (ISR3-LK-REL)

This is done as v1.116.0 was done (LibKa0s `a23266df`, then `cbd82ed3`, following `docs/releasing.md`
steps 4 to 7):

1. **The first commit**, `ISR3-LK-REL: v1.117.0 (2026-11-25): ForeverDB minor 4 (spots from world
   coordinates and Full, vendx prices), kit revision 65`:
   - the CHANGELOG's `## v1.117.0 — 2026-11-25` block, with its versions line: ForeverDB key 4, kit 65,
     every other file at its v1.116.0 minor, and no `NEEDS_*` floor rising;
   - the semver table and the provenance template in `releasing.md`, and the v1.117.0 re-vendor note under
     step 8;
   - the README's kit line;
   - the standards pointer, checked against `head -1 ../WowAddonStandards/standards/STANDARDS.md`.
2. **The second commit**, `ISR3-LK-REL: v1.117.0's release record (...)`:
   - the release-stamped `docs/automated-tests/<stamp>/` bundle measured on the first commit, clean;
   - its hand-written ANALYSIS.md;
   - the RESULTS.md row;
   - the CHANGELOG's release-gate and preview re-look lines.
3. **An annotated local tag**, `v1.117.0`, on the second commit, after the tag's hard preconditions in
   `releasing.md` are read off the manifest. It is **never pushed** until the owner says so.

## 3. Drop Watcher: re-vendor v1.117.0 (ISR3-DW-00)

- Copy `libs/LibKa0s/` and `tests/_kit/` whole from the v1.117.0 tag. Roll the CLAUDE.md provenance line
  to v1.117.0.
- **The `LibKa0s icons:` declaration** (CLAUDE.md:49):
  - **add** `ph:arrow-fat-up`, `ph:arrows-horizontal`, `ph:check-fat`, `ph:coins`, `ph:trash`, `sort-up`
    and `sort-down`;
  - **keep** `ph:arrow-up` and `ph:minus` for now. ISR3-DW-01 stops using them, then removes them from
    the declaration and re-prunes, after a grep finds no other user;
  - **keep** `arrow-up`, `arrow-down` and `confirm`, which TipMarks and WindowCells use, and `help`.

  Then prune `media/icons/` with the tag's `tools/prune-icons.lua`, and keep the README's icon-set credits
  in step. Every icon above was checked to exist in LibKa0s's `LibKa0s/media/icons/` at the current head.
- Write the `docs/revendor/2026-11-25-v1.117.0/01_DELTA.md` bundle, as v1.116.0's was. It records the
  per-file minors, the kit revision pairing and the contract notes: `Spots` gains a second return, and
  `VendorPrice` can answer a lower price than before.
- `core/ForeverDBSetup.lua`'s pinned minor moves to 4. Its tests re-pin.

## 4. Drop Watcher: the items

### 4.1 Glyphs, column inset, header hover and sort triangles (ISR3-DW-01; items 1, 2, 5, 11, 12)

**The recipe glyphs (items 1 and 2).** These are `GLYPH` in `modules/ItemSearchTip.lua`, one renderer
(`IST.CraftMark`) for both the tooltip and the window.

| Recipe | Glyph | Tone |
|---|---|---|
| known, can skill up | `ph:arrow-fat-up` | its skill-up color (`skillOrange`, `skillYellow`, `skillGreen`) |
| known, no skill-up | `ph:arrows-horizontal` | `glyphKnown` (#b0b0b0, the same gray as today's dash) |
| not known | `ph:lock` | `glyphLocked` (unchanged) |

- **The same size everywhere.** A new constant, `C.ITEM_SEARCH.GLYPH_SIZE = 14`, sets the pixel size.
  The escape carries an explicit `14:14`, where `TipMarks.Escape` writes `0:0`. `TipMarks.Escape` gains an
  optional 5th argument, `size` (nil keeps `0:0`, so no existing caller changes). The window's glyph
  column and the tooltip both pass `GLYPH_SIZE`.
- The fallback characters stay `^`, `=` (was `-`) and `x`.
- The header comments (ItemSearchTip.lua:49-51 and :132-134) are updated.

**The column inset (item 12).** `TABS.INSET = 6`, the window's own body margin (`C.WINDOW.INSET`).
`TABS.Layout` starts at `x = INSET` and lays the columns across `width − 2·INSET`. Cells and labels move
together. Row stripes, the hover wash and the selection edge still span the full row. The glyph column
(Crafting) and the mark column (Quests) get `justify = "CENTER"`.

**The header hover (item 5).** Each sortable column label (a Button, ItemSearchGrid.lua:452-466) gets:

- on hover: its text in `text.link` (the same hot tone as the header marks, `ISG.MARK_HOT`), plus the
  column's existing `tip` as a tooltip whose last line is the hint "Click: sort by <title>; click again to
  reverse";
- while hovered and not the active sort: the triangle the click would give, at 50% alpha.

A label for a column that cannot be sorted gets no hover.

**The sort triangles (item 11).** `b.arrow`'s texture becomes `NS.Icon(sort.desc and "sort-down" or
"sort-up")`, the open-iconic solid triangles LootHistory uses. Ascending shows `sort-up`. It is sized to
the label font's line height (`GetStringHeight` of the label, rounded) where it is 10 × 10 today. It is
still tinted `list.header.arrow` through `NS.SkinPaint`, so a skin switch repaints it with no rebuild.
`arrow-up` and `arrow-down` stay declared, because TipMarks uses them.

**Tests** (in `test_item_search_tip.lua`, `test_item_search_tabs.lua` and `test_item_search_window.lua`):
the glyph icon and tone per state, the escape carrying `14:14` from both the tooltip and the window, the
layout's first x at 6 and its total width, the centered justify, a hover changing the label's tone and
showing the next triangle, and `sort-up`/`sort-down` per direction.

### 4.2 The tooltip: skill parts, header and separator, quest marks (ISR3-DW-02; items 4, 13, 14a, 14b)

**Skill breakpoints on recipe rows (item 4).** `ISC.SkillParts` (ItemSearchCells.lua:466-479) moves to the
model as `IS.SkillParts`. ItemSearchCells keeps `ISC.SkillParts` as an alias, so the window is unchanged
and item 3 stays dropped. The tooltip's crafting row (`craftingLines`, ItemSearchTip.lua:243-255)
becomes:

- **left:** `<glyph> <recipe name>`, as today;
- **right:** the colored parts, for example `40 70 90 110`, each part in its `skill*` tone, the same text
  the window's Skill column draws. Then ` · <Profession>` in muted when the rows shown come from more
  than one profession (the profession filter is off, or the player has two crafting professions). A
  recipe with no breakpoints shows the profession alone, as today.

A new setting, `itemSearch.tooltip.craftSkill` (default **true**), "Show recipe skill levels", turns the
parts off and brings back today's right side.

**Perf.** The colored parts string is memoized per recipe id. The breakpoints are static. The memo is
cleared on the skin's `OnLooksChanged`, because the tones change with the skin. That keeps the warm hover
free of new strings.

**The header and the separator (items 14a and 14b).** The block opens like this:

1. **The hairline.** When `itemSearch.tooltip.header` is on (it keeps its key and its default, true), the
   block adds one blank spacer line (`" "`). A per-tooltip Texture lies across the spacer's vertical
   middle:
   - parented to the tooltip and created once per tooltip frame (weak-keyed);
   - anchored LEFT to the tooltip's left + 8 and RIGHT to its right − 8 (`C.ITEM_SEARCH.RULE_INSET = 8`);
   - exactly one physical pixel tall, through LibKa0s's CorePixel (`__PixelSize`), with pixel snapping
     off and its offset rounded to whole pixels;
   - filled with `WHITE8X8` and tinted by a new owner token, **`dw.tipRule`**: default
     `{ 0.55, 0.46, 0.25, 0.9 }`, a dim gold, following `divider`.

   It never sets the tooltip's width, which the old 160-wide escape did. It is hidden on `OnHide` and
   `OnTooltipCleared` (the existing `watch()` hooks), and redrawn on `OnSizeChanged` and once on the next
   frame (`C_Timer.After(0)`), because the post call can run before the tooltip is laid out.
   `IST.Rule`'s escape, `IST.RULE_TEXTURE` as an escape and `C.ITEM_SEARCH.RULE_WIDTH` are removed.
2. **The label line**, always shown when the block is. It is one `AddDoubleLine`:
   - left: `Drop Watcher` in the muted label tone (`mutedGold`, `dw.tipLabel`);
   - right: the badge (§4.5), or nothing when the badge is off.
3. The badge's reason lines (§4.5), and then the sections, as today.

The old title line, `L["Drop Watcher · Item Search"]`, is removed from the tooltip. Its locale key goes
too unless something else still uses it (the window's title keeps its own string). The setting's label
becomes "Separator line", and its tooltip text says it draws the thin line above Drop Watcher's block.

**Quest marks in the game's style (item 13).** There is one mark function, `IST.QuestMark(state, size)`,
for the tooltip and the window alike. Both pass `C.ITEM_SEARCH.MARK_SIZE = 14`, which equals
`GLYPH_SIZE`.

| State | When | Mark | Tint |
|---|---|---|---|
| `can` | not picked up, your level allows it | `Interface\GossipFrame\AvailableQuestIcon` (the yellow `!`) | none |
| `high` | not picked up, your level is too low | the same `!` | dimmed: multiplied by 0.5, 0.5, 0.5, through the escape's color |
| `log` | in your log, not complete | `Interface\GossipFrame\IncompleteQuestIcon` (the gray `?`) | none |
| `ready` | in your log and complete, not turned in | `Interface\GossipFrame\ActiveQuestIcon` (the `?`) | tinted `good` (`dw.upgrade`), so it reads green |
| `done` | turned in | `ph:check-fat` (a plain fat check, no box) | `good` |

- With the media library absent, the fallbacks are `!`, `?` and `+` as colored text.
- `confirm` is no longer used for quests.
- The tooltip's state comes from the same states. It now tells `can` from `high` through the quest's
  min level, as the window does.

**The new `ready` state.**
- `Compat.QuestReady(questID)` is new in `core/CompatSearch.lua`. It tries, in order:
  `C_QuestLog.ReadyForTurnIn`, `C_QuestLog.IsComplete`, then the log entry's `isComplete` through
  `GetQuestLogIndexByID`/`GetQuestLogTitle` where those exist. Each call is pcall-wrapped and
  secret-guarded under the compat rules. It answers true, false or nil (unknown).
- `questState` (ItemSearch.lua:189-193) answers `done` > `ready` > `log` > `todo`.
- `ready` flows through `questTier` (it shares tier 1 with `log` and ranks first within it),
  `ISC.QuestStatus`, `statusText` (the Status column reads "Ready to turn in") and `STATUS_ORDER` (ready
  before log).
- Smoke row ITEM-SEARCH-35 probes which API answers on Forever, and `docs/forever-probes.md` gets an
  entry for it. So do the three GossipFrame textures: whether they exist on Forever, and how they look
  at 14 px.

**Tests:** the row's right side with and without `craftSkill`, one profession and mixed; the memo
cleared by a skin change; the spacer line and the hairline's anchors, inset, height and token; no
hairline when `header` is off; redraw on size change; hidden on clear; the label line with and without
the badge; no title line; each quest state's mark and size, in the tooltip and the window; `QuestReady`'s
three routes and its guards; and `ready` through ranking and status.

### 4.3 Rank colors, test rows, Gathered from (ISR3-DW-03, part 1; items 6, 7)

**Rank colors (item 6).** The color says what kind of creature it is, as the game's unit frames do. It no
longer says "this is a creature", which the Type column already says. The tones are fixed, not skinned:
like the skill-up hues, they carry a game meaning every player reads the same way. They are added to
`FIXED_TONE` in `core/Constants.lua`:

| Rank (`npc` row's `rank`) | Tone key | Value | Type text |
|---|---|---|---|
| 0, normal | `plain` (skinned, as today) | `dw.plain` | Creature |
| 1, elite | `rankElite` | `{ 1.00, 0.82, 0.00 }` (#FFD100, the game's gold) | Elite |
| 4, rare | `rankRare` | `{ 0.78, 0.80, 0.86 }` (#C7CCDB, silver) | Rare |
| 2, rare elite | `rankRareElite` | `{ 0.62, 0.80, 1.00 }` (#9ECCFF, a pale silver-blue, apart from both rare and elite) | Rare Elite |
| 3, boss | `rankBoss` | `{ 0.75, 0.44, 1.00 }` (#BF70FF, a lightened epic purple) | Boss |
| object | `plain` | | Object / Object ×N |
| container | its item quality (unchanged) | | Container |

- **Where:** the Drops from Source cell and Type cell; the Skinned from Creature cell; and the tooltip's
  Drops from and Skinned from rows (the name on the left).
- Vendors and quest givers stay plain.
- The red `tone = "red"` on every creature row (ItemSearchCells.lua:218-225) is removed.
- The previous spec's line ("creatures in the hostile color", feedback §5.4 table) is superseded by this
  section.

**Test and dev sources (RECON test-rows, option A).** A new pure function, `IS.IsTestSource(name)`,
answers true when the name matches any of:

- the whole word `test`, any case (`%f[%a][Tt][Ee][Ss][Tt]%f[%A]`, applied to the name);
- `(DND)`;
- `UNUSED`, in capitals;
- `[PH]`.

Such a source is dropped from every list: drops (creatures and objects), gathered, skinned, vendors and
quest givers. The count goes to the debug log once per item, as unnamed objects' does. ISR3-DW-03 measures
the pattern offline over every `obj` and `npc` name in the installed build. It records the match count and
any real name it would hide (the recon expects 7 objects and 13 creatures, with no false positive). The
filter is always on and has no setting. Option B (pfQuest-only objects with no spot) is not built.

**Gathered from (item 7).** This is a new tab and a new tooltip section. It is a sibling of Skinned from,
which stays its own tab.

The **classification**, `IS.GatherKind(name, item)`, is pure. It answers `"fishing"`, `"mining"`,
`"herbalism"` or nil, and is tried in this order:

1. **Fishing:** the name contains `School`; or is one of `Floating Wreckage`, `Floating Debris`,
   `Oil Spill` or `Patch of Elemental Water`; or contains `Pool` and the searched item's class is not 12
   (quest).
2. **Mining:** the name contains `Vein`, `Deposit` or `Obsidian Chunk`.
3. **Herbalism:** the name is in the curated node table as a herb; or the name equals the searched item's
   own name and the item is class 7, subclass 9.

The recon measured the rule at 155/155 precision on the 2026-11-25 build. An object that classifies
leaves Drops from and joins Gathered from. A fishing node yielding a class 7/9 item (180184 "School of
Fish" yields Peacebloom) is shown as fishing, with one debug-log line per item.

**The curated node table** is `core/GatherNodes.lua`:
`NS.GatherNodes = { [name] = { prof = "herbalism"|"mining", skill = n } }`. It holds game facts (the
client's own "Requires Herbalism N"), not ForeverDB rows, so GPL is not involved. It covers about 28 herbs
and about 25 veins and deposits, including the Ooze Covered variants. Starting values:

- **Herbs:** Peacebloom 1, Silverleaf 1, Earthroot 15, Mageroyal 50, Briarthorn 70, Stranglekelp 85,
  Bruiseweed 100, Wild Steelbloom 115, Grave Moss 120, Kingsblood 125, Liferoot 150, Fadeleaf 160,
  Goldthorn 170, Khadgar's Whisker 185, Wintersbite 195, Firebloom 205, Purple Lotus 210, Arthas' Tears
  220, Sungrass 230, Blindweed 235, Ghost Mushroom 245, Gromsblood 250, Golden Sansam 260, Dreamfoil 270,
  Mountain Silversage 280, Plaguebloom 285, Icecap 290, Black Lotus 300.
- **Mining:** Copper Vein 1, Tin Vein 65, Incendicite Mineral Vein 65, Silver Vein 75, Lesser Bloodstone
  Deposit 75, Iron Deposit 125, Indurium Mineral Vein 150, Gold Vein 155, Mithril Deposit 175, Truesilver
  Deposit 230, Dark Iron Deposit 230, Small Thorium Vein 245, Rich Thorium Vein 275, Small and Large
  Obsidian Chunk 305, each "Ooze Covered" variant at its base vein's value.

The builder checks every name against the objects the build actually has, by counts only. A table name
with no object is dropped, and an object name the patterns catch but the table lacks gets skill nil
("?"). The table's provenance and the "values from the client's node tooltips; verify in game" note go in
its header and in `docs/validate-seeds.md` as a hand-curated list. Fishing has no per-node skill on this
client, so its Skill cell is a dim "–".

**The tab.** `TABS.ORDER = { "drops", "gathered", "vendors", "quests", "crafting", "skinned" }`. Its title
is "Gathered from", and its noun is one node, many nodes.

| Column | Content | Width |
|---|---|---|
| Node | the merged name (`IS.MergeNamedObjects`, per name, inside this tab); its row tooltip says "N kinds of <name>" | *flex* |
| Profession | Herbalism, Mining or Fishing | 90 |
| Skill | the node's minimum skill: red (`red`) when above your rank in that profession, plain otherwise; "?" when not in the table; dim "–" for fishing | 64 |
| Zone | as for Drops (from the union of the ids' spots) | *flex* |
| Chance | bar and percent, the node's highest chance for this item | 150 |
| (pin) | waypoint | 28 |

- **Filters** (view-only): Herbalism, Mining, Fishing, Only my professions, Only my zone.
- **The ranking**, `IS.Rank.gathered`:
  1. a profession you have, at a skill you can gather;
  2. a profession you have, skill too high;
  3. a profession you don't have (before your skills are read, every row is tier 1).

  Within a tier: in your zone first, then higher chance, unknown chance last.
- **The tooltip section** is `gathered`, "Gathered from". Its rows are `<node>` on the left and
  `<Profession> <skill> · <chance>` on the right, with the skill colored as in the tab. It is capped by
  Rows per section. `IST.ORDER` and `IST.SECTIONS` gain `gathered = true` after `drops`.
- A schema step (§5) inserts `gathered` after `drops` in a stored `tooltip.order`.

**Tests:** each rank's tone and Type text in the cells and the tooltip; no red on creatures;
`IsTestSource` on invented names (positives, and near misses like "Contest", "Testament" and "Attest");
the filter across every list and its log line; `GatherKind`'s every branch including the Pool rule and
the class 7/9 rule; the table lookup; the tab's columns, sorts, filters and ranking; the tooltip section
and its cap; and the schema step.

### 4.4 Sold by: recorded prices, "<Side> only", spots (ISR3-DW-03, part 2; items 8, 10)

**Prices seen at vendors.** This is a new module, `modules/ItemSearchPrices.lua`.

- **When it records.** On `MERCHANT_SHOW`, and on `MERCHANT_UPDATE` debounced to 0.5 s while the merchant
  is open. Forever only, only while Item Search is enabled, and only while
  `itemSearch.recordPrices` (default **true**, "Record vendor prices") is on.
- **What it records.** The vendor is `Compat.MerchantNpcID()`, the npc id parsed from `UnitGUID("npc")`,
  pcall-wrapped and secret-guarded (nil skips the visit). For each slot it takes `GetMerchantItemID(i)`
  and `GetMerchantItemInfo(i)`'s price and quantity, through a new `Compat.MerchantItems()`. Slots with
  an extended cost and a zero price (token vendors) are skipped.
- **Where it is stored.** In `db.global.itemSearch.prices[npcID][itemID] = { p = copper, q = quantity,
  t = time() }`. It is global because a vendor's price is the same for every character, except for
  reputation discounts, which are a known limitation. A later visit overwrites the entry.
- **The cap.** `C.ITEM_SEARCH.PRICE_CAP = 5000` entries. Over the cap, the oldest 10% by `t` are pruned.
- **What the window and tooltip show,** per vendor row:
  1. the recorded price (the row tooltip says "Seen here <date>", plus "for N" when `q > 1`);
  2. else `VendorPriceAt` (§1.3), with the row tooltip saying "Recorded by ForeverDB";
  3. else a dim "–", with the row tooltip saying "No price recorded yet: open this vendor and Drop
     Watcher remembers it".

  The price shown is the stack's price. The cheapest-vendor ranking compares `p / q`.
- `facts.vendorPrice` (ItemSearchModel.lua:331-332) becomes per row (`v.price`, `v.priceOrigin`). The
  "only on the vendor it was seen at" rule (ItemSearchCells.lua:315-318, ItemSearchTip.lua:218-223) is
  replaced by the per-row value.

**"<Side> only" (item 8).** Where `IS.OtherSide` answers true, the Faction cell and the tooltip's vendor
row say **"Horde only"** or **"Alliance only"** (`L["%s only"]` with the vendor's side) in `red`, in place
of "can't buy". The cell's row tooltip says: "Only Horde characters can buy here: ForeverDB marks this
vendor Horde. Only my faction hides these rows." The column's tip becomes "Alliance, Horde or Both
(either faction); red: only the other faction can buy here". `L["can't buy"]` is removed.

**Zones and pins (items 8 and 10).** Nothing new is drawn. The Zone cells and pins already read
`lib.Spots` through the spot memo, and minor 4 fills them from `spz` and `spw`. Two changes:

- The spot memo and every cached static fact are **cleared when ForeverDB_Full finishes loading** (§4.6),
  and the open window repaints.
- A source with no spot anywhere says "No known spawn" in its row tooltip and in the tooltip's zone
  slot, where it showed a bare "–". It keeps ranking below rows that have spots.

**Tests:** recording through faked merchant APIs (the price, the quantity, the token skip, a nil or
secret GUID skipped, debounce, the setting off, Retail inert); the cap and its prune; the
seen > vendx > vp > dash precedence and each row tooltip; per-unit ranking; "Horde only" and "Alliance
only" text and tone; the memo cleared on a Full load; and "No known spawn".

### 4.5 The verdict badge (ISR3-DW-05; item 14c)

This is a new pure module, `modules/ItemSearchVerdict.lua`: `IS.Verdict(facts, me, item)` answers
`{ verdict, score, confidence, tier, reasons, hint }`. `item` carries the client facts:

- `quality`, `classID`, `subclassID`, `equippable`;
- `sellPrice` and `bindType`, which `Compat.ItemInfoByID` now reads (GetItemInfo returns 11 and 14);
- `gear`, the Evaluate kernel's verdict for the item, or nil when there is none or it is pending;
- `newCollect`, the Collectibles verdict.

No ItemTree code or logic is ported. The formula is Drop Watcher's own, from RECON's "Proposal"
sections.

**The score**, `clamp(sum, 0, 100)`. Each part is listed below, and each records a reason.

| Part | Points | Cap |
|---|---|---|
| **New collectible** (`newCollect`) | the score is 100, verdict Keep, reason "New to your collection"; nothing else is computed | – |
| **Quest in your log needs it** (`log` or `ready`, role Needs) | +60 each; reason "In your quest log: <title>" or "Ready to turn in: <title>" | quests total 80 |
| **Available quest needs it** (`can`, quest min level ≤ your level + 3) | +35 each; reason "Quest you can pick up: <title>" | (in the 80) |
| **Starts a quest** not done and not in the log | +50; reason "Starts a quest: <title>" | (in the 80) |
| Rewards from, and done quests | 0 | – |
| **Recipes you know**, in a profession you have | orange +30, yellow +20, green +8, gray 0, each; reason "<Profession> skill-up (<color>)" for the best | crafting total 50 |
| **A recipe you don't know** in a profession you have, your rank below its gray breakpoint | +10 each; reason "<Profession> recipe you could learn" | (in the 50) |
| **Recipes in professions you lack** | +3 each; reason "Other professions use it (<n> recipes)" | 9 |
| **Gear** (`equippable`) | upgrade +70, sidegrade +20, else 0; reason "Upgrade for you" or "Sidegrade" | – |
| **Re-buyable** damper | −20 when 3 or more vendors sell it, or any vendor's price (§4.4) is ≤ 500 copper; reason "Easy to buy again" | – |
| **Trivial uses** damper | −15 when the item has uses and every one is gray or done; reason "Every use is gray or done" | – |
| **Poor quality** (quality 0) | the score is capped at 15 unless a quest part is above 0 | – |
| **Quest item** (`classID == 12` or `bindType == 4`) with no quest part | the score is floored at 20 (Hold): it can't be sold and is risky to delete; reason "Quest item" | – |

**The verdict.**

| Verdict | Rule | Icon | Tone |
|---|---|---|---|
| **Keep** | score ≥ 50 (`C.ITEM_SEARCH.VERDICT.KEEP`) | `ph:lock` | `good` (`dw.upgrade`) |
| **Hold** | 20 ≤ score < 50 (`VERDICT.HOLD`), or Toss under Low confidence, or sell price unknown | `ph:hourglass` | `yellow` (`dw.sidegrade`) |
| **Sell** | score < 20 and `sellPrice > 0`; reason "Sells for <money>" | `ph:coins` | `warn` (`dw.urgent`, amber) |
| **Toss** | score < 20 and `sellPrice == 0`, and the confidence is not Low; reason "No use found, and no vendor buys it" | `ph:trash` | `bad` (`dw.notWanted`) |

**The confidence** answers how many of the inputs the score needs were actually answered. It is not the
score.

| Input | Weight | Needed when | Answered when |
|---|---|---|---|
| ForeverDB loaded | 3 | always (Forever) | `Status()` is loaded |
| Client item info | 2 | always | `quality` and `sellPrice` both non-nil |
| Quest states | 3 | the facts have a quest row, or ForeverDB is not loaded | every quest row's state came back non-nil (with ForeverDB not loaded: never) |
| Profession ranks | 3 | the facts have a crafting row | `IS.SkillsRead(me.ranks)` |
| Gear verdict | 2 | `equippable` | `gear` is non-nil |
| Source facts | 1 | always | ForeverDB is loaded and knows the item (`Item(id)` non-nil) |

- `confidence = floor(100 · answered / needed + 0.5)`.
- `tier`: **High** ≥ 80, **Medium** 50 to 79, **Low** < 50.
- `hint`, shown below High: the heaviest unanswered input's fix:
  - "ForeverDB is not loaded";
  - "Item info is still loading";
  - "Open your profession window to rank recipes";
  - "Pawn is still scoring".
- **A Low confidence never says Toss.** It falls back to Hold, so the addon never tells a player to delete
  something it could not judge.

**The badge line** is the label line's right side (§4.2):
`<icon 14px> <Verdict> <score> · <Tier>`. The icon, verdict and score are in the verdict's tone, and
` · <Tier>` is in `muted`. Example: `[lock] Keep 72 · High`.

**The reason lines** follow the label line when `itemSearch.tooltip.reasons` (default **true**,
"Explain the badge") is on:
- up to **2** reasons, the top contributions by absolute points, each `  · <reason>` with the bullet in
  `mutedGold` and the text in `plain`;
- Sell and Toss always carry their price reason;
- then the `hint`, muted, when the tier is below High: "Confidence Medium: open your profession window to
  rank recipes".

**Settings.** `itemSearch.tooltip.badge` (default **true**, "Show the Keep / Hold / Sell / Toss badge")
and `itemSearch.tooltip.reasons` (above). The thresholds and weights are constants
(`C.ITEM_SEARCH.VERDICT`), not settings.

**Perf.** The verdict is memoized per item id, under a generation counter. The counter is bumped on
`QUEST_LOG_UPDATE`, `QUEST_TURNED_IN`, `SKILL_LINES_CHANGED`, `TRADE_SKILL_SHOW` (recipes read), a gear
re-evaluation, a ForeverDB or Full load, and a skin change (tones). A warm hover reads the memo and
builds no tables. The block's perf ceilings (§6) must hold.

**Tests** (`tests/test_item_search_verdict.lua`): every part's points and caps; each damper; the
poor-quality cap and the quest-item floor; each verdict boundary (19, 20, 49, 50); Sell versus Toss versus
an unknown price; the new-collectible short cut; gear upgrade and sidegrade; each confidence input's
needed and answered cases; the tiers at 49, 50, 79 and 80; Low turning Toss into Hold; reason ordering
and the cap at 2; each hint; the badge string's parts and tones; both settings; and the memo's
generation bumps.

### 4.6 ForeverDB_Full, Drop Watcher's policy (ISR3-DW-03)

The setting is **`itemSearch.fullDB`**, "Load ForeverDB (Full)":

- **`"window"`** (the default): "When the Item Search window opens";
- **`"never"`**.

The row is disabled, with the note "ForeverDB_Full is not installed", when `FullStatus()` says missing.

- **When it loads.** On the window's first open in a session, if the setting is `"window"` and
  `FullStatus()` is `"available"`, Drop Watcher calls `LoadFull()`. In combat it waits for one
  `PLAYER_REGEN_ENABLED`, then tries once. The tooltip never triggers the load (its perf ceilings).
- **After the load:**
  - the static-fact cache and the spot memo are cleared (§4.4), and the open window repaints;
  - the debug log gets one line: "ForeverDB_Full loaded: 19.6 MB, 840 ms";
  - Drop Watcher's diagnostics show the library's Full state and cost;
  - the window's footer reads "ForeverDB 2026.11.25.48 · loaded · Full".
- **Measured and documented.** ISR3-DW-03 measures the load offline: Lua 5.1, the seven files read from
  the client folder read-only, the KB from `collectgarbage("count")` and the time from `os.clock`. It
  writes the numbers, not rows, into `docs/performance.md` and the execution record. Smoke row
  ITEM-SEARCH-40 records the in-game numbers.

### 4.7 The key (ISR3-DW-04; item 9)

`IK.Decide(open, shown, hovered)` becomes:

```lua
if hovered then return "show" end
return open and "close" or "open"
```

- Hovering an item always shows it. When it is the item already shown, the window stays open, keeps its
  tab and repaints nothing new. It never closes because the item is the same.
- With no hover, the key toggles the window.
- **A pinned chat-link tooltip doesn't count as hovering.** `IK.TOOLTIPS` becomes `GameTooltip`,
  `ShoppingTooltip1` and `ShoppingTooltip2`. `ItemRefTooltip`, `ItemRefShoppingTooltip1` and
  `ItemRefShoppingTooltip2` are removed.
- The header comment (ItemSearchKey.lua:13-19) and `tests/test_item_search_key.lua` are updated. The
  tests cover every row of the old table that changed, plus a pinned ItemRefTooltip with no hover
  toggling the window.

## 5. Settings and schema (ISR3-DW-06, with each item adding its own rows)

| Key | Default | Row label | Section |
|---|---|---|---|
| `itemSearch.tooltip.header` | true (kept) | **Separator line** (renamed) | Item tooltip |
| `itemSearch.tooltip.badge` | true | Show the Keep / Hold / Sell / Toss badge | Item tooltip |
| `itemSearch.tooltip.reasons` | true | Explain the badge | Item tooltip (indented under badge) |
| `itemSearch.tooltip.craftSkill` | true | Show recipe skill levels | Item tooltip |
| `itemSearch.tooltip.sections.gathered` | true | Gathered from (in the sections list) | Item tooltip |
| `itemSearch.recordPrices` | true | Record vendor prices | Window |
| `itemSearch.fullDB` | `"window"` | Load ForeverDB (Full) | Window |

- Each key gets its `settings/Schema.lua` row (Forever-only `clients`, as the page's other rows have),
  its default in `defaults/Profile.lua`, its locale strings, its `docs/settings-panel.md` line and its
  `docs/schema.md` row, under the options-ui rules.
- **Schema step 18** (per profile, `NS.MigrateGatheredSection`): a stored `itemSearch.tooltip.order` that
  lacks `"gathered"` gets it inserted right after `"drops"`, or appended when `"drops"` is absent.
  Nothing else changes. `db.global.itemSearch.prices` has no default and needs no step.
- The step is tested through the runner, as steps 16 and 17 are.

## 6. Perf

- The tooltip block's ceilings in `tests/perf.lua`, `ITEM_SEARCH_TIP_COLD = 17500` and
  `ITEM_SEARCH_TIP_WARM = 6500`, must hold on both clients after the skill parts, the label line, the
  badge, the reasons and the Gathered from section. The means are the memos named above.
- If a ceiling cannot hold, the builder stops, measures, and either finds the allocation or raises the
  ceiling. A raise must be **named in the calls**, with both numbers, and in the execution record.
- The inert Retail path stays pinned at 0.
- The kit's new `spw` rows can change the cold case's work. If they do, that is measured and said.

## 7. Docs (ISR3-DW-06)

- **README:** the feature list (Gathered from, the badge, recorded prices, Full on demand), the icon
  credits, and the tests badge.
- **`docs/ARCHITECTURE.md` and `docs/module-map.md`:** `ItemSearchVerdict.lua`, `ItemSearchPrices.lua`,
  `core/GatherNodes.lua`, and the tooltip block's new head.
- **`docs/settings-panel.md` and `docs/schema.md`:** §5.
- **`docs/known-limitations.md`:**
  - a spawn converted from world coordinates near a zone border can land on the neighbor's map or the
    continent's (about 6% of the measured keys), and its pin is still at the right place in the world;
  - recorded prices include your reputation discount;
  - the test-name filter can only catch names;
  - ForeverDB_Full costs about 20 MB while loaded;
  - the gathering skills are hand-curated;
  - a pinned chat link doesn't count as hovering;
  - the badge is advice, never an action.
- **`docs/forever-probes.md`:** `QuestReady`'s API, the GossipFrame textures, the Full load's cost, and
  `C_Map.GetMapPosFromWorldPos` against the adapter.
- **`docs/performance.md`:** the Full cost and the tooltip ceilings.
- **`docs/validate-seeds.md`:** the curated node table.
- **`docs/test-cases.md`:** regenerated, with the README's tests badge equal to its Total.
- **`docs/smoke-tests.md`:** ITEM-SEARCH-31 to ITEM-SEARCH-43 (§8), unrun, and an "Owed by" line naming
  this run. Older rows that a new one contradicts are cross-referenced, as the feedback run did.

## 8. Smoke rows (written unrun; never marked passed by an agent)

| Row | What the owner checks | Item |
|---|---|---|
| ITEM-SEARCH-31 | Linen Cloth: the tooltip's and the Crafting tab's skill-up arrows are the same thick arrow at the same size. No-skill-up rows show a gray ↔. The glyph column sits off the table's edge and centered, and every tab's first column is inset. | 1, 2, 12 |
| ITEM-SEARCH-32 | Hovering a column title highlights it and shows a faint triangle. A click sorts, with LootHistory's solid triangle, and a second click flips it. Untitled columns don't react. | 5, 11 |
| ITEM-SEARCH-33 | Peacebloom's tooltip: recipe rows show colored breakpoints such as "25 40 55" on the right. Turning off Show recipe skill levels brings back the profession. | 4 |
| ITEM-SEARCH-34 | The tooltip block: no "Drop Watcher · Item Search" title. A thin dim-gold line runs across the tooltip, 8 px in from each edge, and stays right when the tooltip resizes (shift for comparison). "Drop Watcher" is at the left and the badge at the right. Separator line off removes the line. | 14a, 14b |
| ITEM-SEARCH-35 | Quest marks, tooltip and window: yellow ! (available), dim ! (too high), gray ? (in log), green ? (complete, not turned in), green check with no box (done). **Probe:** `/dump C_QuestLog.ReadyForTurnIn, C_QuestLog.IsComplete, GetQuestLogTitle` on Forever; record which exist. | 13 |
| ITEM-SEARCH-36 | Drops from on Linen Cloth: normal creatures white, elites gold, rares silver, rare elites pale blue, bosses purple, in both Source and Type. Objects white, containers in their quality. TWO-SOLUTION TEST and other test rows are gone. | 6, test rows |
| ITEM-SEARCH-37 | Peacebloom: a Gathered from tab with one "Peacebloom" node (Herbalism 1) and School of Fish (Fishing). Drops from no longer lists them. Copper Ore: veins under Mining with skills; red when above your rank. The tooltip has a Gathered from section. | 7 |
| ITEM-SEARCH-38 | Visit a vendor, then search one of its items: Sold by shows that price ("Seen here <date>"). A Horde vendor reads "Horde only" in red with the explaining tooltip. A never-visited vendor's price says how to fill it. | 8 |
| ITEM-SEARCH-39 | Sold by on Linen Cloth's vendors (Maria Lumere, Hula'mahi, Selina Weston) shows Stormwind City, The Barrens and Tirisfal Glades with pins, and a pin's arrow leads to the vendor. **Probe:** for one source, compare the adapter's map position with `C_Map.GetMapPosFromWorldPos` (snippet in the row). | 8, 10 |
| ITEM-SEARCH-40 | With ForeverDB_Full installed: the first window open loads it (footer "· Full"; the debug log names MB and ms, recorded here). Opening in combat defers it until combat ends. Setting Never: no load. Without Full: the row is disabled with its note. | 8, 10 |
| ITEM-SEARCH-41 | Ctrl-Alt-D: over an item, the window opens on it. Again over the same item, it stays open. Over nothing, it toggles. A pinned chat-link tooltip with the mouse elsewhere: it toggles, ignoring the link. | 9 |
| ITEM-SEARCH-42 | The badge on: a quest item in your log (Keep, reason names the quest); gray junk (Sell, "Sells for …"); a reagent of a profession you have (Keep or Hold by color); a fresh login before the profession window opens (Medium or Low, with the hint, and never Toss). Show the badge and Explain the badge toggles. | 14c |
| ITEM-SEARCH-43 | Hovering many items quickly with every section on shows no hitch. The settings page shows the new rows in §5's order, disabled where their prerequisite is off. | 6 (perf), all settings |

## 9. Not in scope

- Item 3, orange on the Skill column (dropped by the owner).
- The Stock and Requires columns (`vendx.s`, `vendx.r`), which the feedback run left out. Minor 4 reads
  `vendx` for prices only.
- RECON test-rows option B (pfQuest-only objects with no spot), and asking ForeverDB upstream to lift the
  `spm` cap.
- A badge in the window (the badge is a tooltip feature).
- An auction-price source.
- The Retail source (DropWatcher#18).
- Re-vendoring v1.117.0 into any addon but Drop Watcher.

## 10. Calls made without asking the owner

| Item | The call | Why |
|---|---|---|
| 8, 10 | `Spots` order: `spz` (when Full is loaded) > `spm` > converted `spw`, with the origin as a second return | ForeverDB's own projections beat ours; the origin lets the host and the tests tell which answered |
| 8, 10 | The map pick uses ForeverDB's `zbord` zone polygons, then the smallest containing rectangle | Measured 93.4% agreement with `spm` against 69% for rectangles alone; a fallback still puts the pin at the right world spot |
| 8, 10 | `C_Map.GetMapPosFromWorldPos` is not used by the adapter, only compared in a smoke row | Keeps the adapter pure and headless-testable; that API is unprobed on Forever |
| 8, 10 | Full loads on the first window open (default), never from the tooltip, deferred past combat; a setting can turn it off | The 20 MB cost belongs to a player who opened the window; the tooltip has a perf ceiling |
| 8, 10 | `LoadFull` lives in the library and the *when* in Drop Watcher | Mirrors `Available()`: the library owns the load, the host owns the policy |
| 8 | Recorded prices are global, overwritten per visit, capped at 5000 entries, with the oldest 10% pruned | A vendor's price is the same for every character; the cap bounds the saved variables |
| 8 | Prices show per stack, and the ranking compares per unit | Matches what the vendor shows, while still ranking fairly |
| 8 | Token-cost slots (extended cost with zero price) are not recorded | Their price isn't copper |
| 6 | Rank colors: elite #FFD100, rare #C7CCDB, rare elite #9ECCFF, boss #BF70FF; fixed, not skinned | Owner said "define it"; purple keeps the boss apart from the skill-up orange on the same window; fixed because rank is a game meaning, like the skill hues |
| 6 | Rank colors also apply to Skinned from and the tooltip's creature rows | One meaning everywhere a creature name is drawn |
| test rows | The test-name filter is always on, with no setting, in Drop Watcher (not the adapter) | It is presentation policy; the adapter answers what the database holds |
| 7 | Herbs are recognized by the curated table first, then by "name equals the searched item's name, class 7/9" | The recon's rule needs a name-to-item lookup per object, which the tooltip cannot afford; the table holds every classic herb node |
| 7 | Gathered from goes right after Drops from; Skinned from stays its own tab, last | The owner asked for gathering apart from drops; the recon recommends separate tabs |
| 7 | Classic node skill values are in the spec, flagged "verify in game" | They are game facts, not ForeverDB rows; the owner's smoke checks them |
| 13 | Ready uses `ActiveQuestIcon` tinted green; level-locked `!` is dimmed by the escape's color | The game has no green `?` texture; a multiply tint keeps it a game texture |
| 13 | `ph:check-fat` for done | A plain fat check with no box, which the owner asked for |
| 1, 2, 13 | One size, 14 px, for glyphs and marks | The owner asked for consistency; 14 matches the window's row font |
| 14a | The label line is always drawn when the block is; the badge is its right side | The owner asked for the addon name at the left of the section |
| 14b | The hairline token is a new `dw.tipRule` (dim gold, following `divider`), not ItemTree's value | Its own color, skinned like every other chrome line |
| 14c | Weights and bars as in §4.5, from RECON's proposal; quest-item floor at Hold; poor-quality cap at 15 | Original logic, no ItemTree port; the floor stops a Toss on something a quest may need |
| 14c | Sell tone is amber (`warn`), not gold | Gold is the label's tone on the same line |
| 14c | The thresholds and weights are constants, not settings | One fewer page of numbers to explain; they can be exposed later |
| 14c | The badge is tooltip-only | It was asked for on the tooltip |
| 4 | Profession name kept after the parts only when rows mix professions | AddDoubleLine has one right column; with one profession the name is noise |
| 5 | A faint next-sort triangle on hover | Makes the headers look clickable, which was the owner's point |
| 9 | Hovering the shown item re-shows it (no close) | The owner's rule: hover means show |
| all | The previous spec's §5.4 Source color line and §5.7 glyph table are superseded here | Recorded so the frozen spec is not edited |
