# Plan D — `LibKa0s-Pool-1.0` and `LibKa0s-Item-1.0` adoption

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Retire four hand-rolled widget pools and the duplicated item primitives across BankLedger
and LootHistory, replacing them with `LibKa0s-Pool-1.0` and `LibKa0s-Item-1.0`.

**Architecture:** Two seams per addon on the model of `core/MediaSetup.lua` — `core/PoolSetup.lua`
and `core/ItemSetup.lua` — each resolving its library once and degrading to a local copy of the
same code when it is absent. The pool adoption replaces both generic pools and both inline row
pools; the item adoption replaces four primitives and **deliberately leaves each addon's resolver
and its uncached policy alone**.

**Tech Stack:** Lua 5.1, LibStub, each addon's vendored test kit, `luacheck`.

**Spec:** [`02_SPEC.md`](02_SPEC.md) §C, §E

**Prerequisites:**
- [`04_PLAN_B_LIBKA0S_MODULES.md`](04_PLAN_B_LIBKA0S_MODULES.md) Task 8 — the payload carrying
  `Pool.lua` and `Item.lua` is vendored into both addons.
- [`03_PLAN_A_POOL_LEAK_FIX.md`](03_PLAN_A_POOL_LEAK_FIX.md) — **LootHistory's leak is fixed
  first.** Adopting the library on top of an unfixed leak would make the fix look like a side effect
  of the refactor, and the test that proves it would be written against the wrong code.

## Global Constraints

- Lua 5.1. `luacheck .` **0/0** and `lua tests/run.lua` green before every commit.
- **`LibStub("LibKa0s-Pool-1.0", true)` / `LibStub("LibKa0s-Item-1.0", true)`** — always the silent
  flag.
- **No user-visible behaviour change.** Both addons render and classify exactly as before.
- **`Compat.GetItemDetails` (BankLedger) and `Compat.GetItemInfo` (LootHistory) do NOT move**, and
  neither does `ItemNameQuality`. Their uncached policies are opposite on purpose and both are
  documented in their own source. Touching either is out of scope and would be a behaviour change
  smuggled inside a refactor.
- A pool is `{ free = {}, active = {} }` — the library's shape is the shape both addons already use,
  so no stored state changes.
- One commit per module per addon: four commits total.

---

### Task 1: BankLedger adopts `LibKa0s-Pool-1.0`

**Files:**
- Create: `BankLedger/core/PoolSetup.lua`
- Modify: `BankLedger/BankLedger.toc` — before `modules\InsightsWidgets.lua`
- Modify: `BankLedger/modules/InsightsWidgets.lua:362-379` (`W.NewPool`, `W.Acquire`,
  `W.ReleaseAll`) and `:789-792` (`W.ReleasePanels`)
- Modify: `BankLedger/modules/LedgerTable.lua:658-675, :798-805` (`LT:AcquireRow`,
  `LT:ReleaseAllRows`)
- Modify: `BankLedger/modules/SessionWindow.lua:301, :391` (`SW:AcquireRow`, `SW:ReleaseAllRows`)
- Test: `BankLedger/tests/test_poolsetup.lua` (new); `tests/test_insights.lua:375` already builds a
  pool and must keep passing

**Interfaces:**
- Consumes: `Pool.New()`, `Pool.Acquire(pool, factory)`, `Pool.ReleaseAll(pool, before)`,
  `Pool.Counts(pool)` from `04_PLAN_B` Task 2.
- Produces: `NS.Pool` — a table with `New`, `Acquire`, `ReleaseAll`, `Counts`, either the library's
  or the local fallback's.

- [ ] **Step 1: Write the failing test**

Create `BankLedger/tests/test_poolsetup.lua`:

```lua
-- tests/test_poolsetup.lua — the LibKa0s-Pool-1.0 seam.
--
-- The library's own suite covers the pool's semantics; duplicating them here is the consumer-side
-- copy testing-§8 forbids. What only this repo can assert is that the seam is wired, that the
-- fallback behaves the same when the library is absent, and — the case worth having — that the
-- addon's real render path recycles.

local T = _G.BL_TEST
local NS = T.NS
local test, assertEqual, assertTrue = T.test, T.assertEqual, T.assertTrue

local function counting()
  local made = 0
  return function()
    made = made + 1
    local o = { __shown = false }
    function o:Show() self.__shown = true end
    function o:Hide() self.__shown = false end
    return o
  end, function() return made end
end

test("PoolSetup: the seam is published", function()
  assertTrue(type(NS.Pool) == "table", "NS.Pool exists")
  assertTrue(type(NS.Pool.New) == "function")
  assertTrue(type(NS.Pool.Acquire) == "function")
  assertTrue(type(NS.Pool.ReleaseAll) == "function")
end)

test("PoolSetup: a released object is reused rather than rebuilt", function()
  local p = NS.Pool.New()
  local factory, made = counting()
  for _ = 1, 3 do NS.Pool.Acquire(p, factory) end
  NS.Pool.ReleaseAll(p)
  for _ = 1, 3 do NS.Pool.Acquire(p, factory) end
  assertEqual(made(), 3, "the second pass builds nothing")
end)

test("PoolSetup: a nested release empties both levels", function()
  -- This is the shape W.ReleasePanels had, expressed through the library's `before` hook. If the
  -- hook is not wired, the inner rows silently stop being recycled and only a heap profile says so.
  local panels = NS.Pool.New()
  local factory = counting()
  local panel = NS.Pool.Acquire(panels, factory)
  panel._rows = NS.Pool.New()
  NS.Pool.Acquire(panel._rows, factory)
  NS.Pool.ReleaseAll(panels, function(p) NS.Pool.ReleaseAll(p._rows) end)
  assertEqual(select(2, NS.Pool.Counts(panel._rows)), 0)
  assertEqual(select(1, NS.Pool.Counts(panel._rows)), 1, "the row went back on its own free list")
end)
```

- [ ] **Step 2: Run it to verify it fails**

Add `"test_poolsetup"` to `SUITES` in `BankLedger/tests/run.lua`, then:

```sh
cd BankLedger && lua tests/run.lua
```

Expected: FAIL — `NS.Pool` is nil.

- [ ] **Step 3: Create the seam**

Create `BankLedger/core/PoolSetup.lua`:

```lua
local _, NS = ...

-- core/PoolSetup.lua — wires the addon into LibKa0s-Pool-1.0 (library-stack-§7).
--
-- ── WHAT THIS REPLACED ───────────────────────────────────────────────────────────────────────
--
-- Four hand-rolled pools: the generic one in modules/InsightsWidgets.lua and the inline row pools
-- in modules/LedgerTable.lua and modules/SessionWindow.lua. All three of this addon's were
-- correct. LootHistory's fourth copy was not — it hid its active widgets and never returned them
-- to the free list, so every re-render allocated a fresh frame per chart element, and frames are
-- never destroyed in WoW. Two addons wrote the same eleven lines and one of them got the second
-- half wrong; that is the whole case for the library.
--
-- ── WHAT A DEGRADED INSTALL GETS ─────────────────────────────────────────────────────────────
--
-- The same pool, locally. It is nine lines, it is the code that was here before, and writing it
-- out is cheaper than making every caller branch — a chart that cannot pool is a chart that
-- allocates, which is precisely the failure this module exists to end.

local Pool = LibStub and LibStub("LibKa0s-Pool-1.0", true)

NS.Pool = Pool or {
  New = function() return { free = {}, active = {} } end,

  Acquire = function(pool, factory)
    local o = table.remove(pool.free)
    if not o then o = factory() end
    pool.active[#pool.active + 1] = o
    o:Show()
    return o
  end,

  -- The `before` hook is not optional garnish in the fallback either: modules/Insights.lua
  -- releases a pool of list panels and each panel owns its own row pool.
  ReleaseAll = function(pool, before)
    local active = pool.active
    for i = 1, #active do
      local o = active[i]
      if before then before(o) end
      o:Hide()
      pool.free[#pool.free + 1] = o
    end
    for i = #active, 1, -1 do active[i] = nil end
  end,

  Counts = function(pool) return #pool.free, #pool.active end,
}
```

- [ ] **Step 4: Put it in the TOC**

In `BankLedger/BankLedger.toc`, before the `modules\` block (the pools are consumed there):

```
# The LibKa0s-Pool seam. Before every module that pools a widget — InsightsWidgets, LedgerTable and
# SessionWindow all take NS.Pool at call time, so this is conventional rather than load-bearing.
core\PoolSetup.lua
```

- [ ] **Step 5: Run it again**

```sh
cd BankLedger && lua tests/run.lua
```

Expected: the three new cases PASS. Nothing else has changed yet.

- [ ] **Step 6: Move `InsightsWidgets` onto the seam**

Replace `BankLedger/modules/InsightsWidgets.lua:362-379` with:

```lua
-- The pool lives in LibKa0s-Pool-1.0 now (core/PoolSetup.lua). These three stay as names because
-- every call site in modules/Insights.lua reads W.Acquire / W.ReleaseAll, and renaming forty call
-- sites to prove a point is not a refactor.
W.NewPool    = function() return NS.Pool.New() end
W.Acquire    = function(pool, factory) return NS.Pool.Acquire(pool, factory) end
W.ReleaseAll = function(pool) return NS.Pool.ReleaseAll(pool) end
```

and `:789-792`:

```lua
-- A panel owns a row pool, so releasing the panels releases their rows first. That ordering used
-- to be two nested loops here; it is the library's `before` hook now.
function W.ReleasePanels(pool)
  NS.Pool.ReleaseAll(pool, function(p) NS.Pool.ReleaseAll(p._rows) end)
end
```

- [ ] **Step 7: Move the two row pools onto the seam**

`modules/LedgerTable.lua` — `LT:AcquireRow` keeps its frame-building body but takes the object from
the seam:

```lua
function LT:AcquireRow()
  return NS.Pool.Acquire(self.rowPool, function() return self:BuildRow() end)
end
```

Extract the existing frame construction (currently the tail of `AcquireRow`, `:665-...`) into
`function LT:BuildRow()` unchanged, returning the row. Then:

```lua
function LT:ReleaseAllRows()
  NS.Pool.ReleaseAll(self.rowPool)
end
```

Do the same in `modules/SessionWindow.lua:301` / `:391` with `SW:BuildRow`.

**Check where `self.rowPool` is created** and route it through the seam too:

```sh
cd BankLedger && grep -n "rowPool = " modules/LedgerTable.lua modules/SessionWindow.lua
```

- [ ] **Step 8: Run the gate**

```sh
cd BankLedger && lua tests/run.lua && luacheck .
```

Expected: PASS, 0/0. `tests/test_insights.lua:375` builds a pool through `W.NewPool` and must still
pass unchanged — if it does not, the seam's shape has drifted from the hand-rolled one.

- [ ] **Step 9: Commit**

```sh
cd BankLedger
lua tests/run.lua --list > docs/test-cases.md
git add core/PoolSetup.lua BankLedger.toc modules/InsightsWidgets.lua modules/LedgerTable.lua \
        modules/SessionWindow.lua tests/test_poolsetup.lua tests/run.lua docs/test-cases.md
git commit -m "refactor(pool): pool widgets through LibKa0s-Pool-1.0

Three hand-rolled pools in this addon, all correct — and a fourth in LootHistory
that was not, which is why the code moved rather than being left alone. The
nested panel/row release becomes the library's \`before\` hook instead of two
loops that only one of the two addons ever had."
```

---

### Task 2: LootHistory adopts `LibKa0s-Pool-1.0`

**Files:**
- Create: `LootHistory/core/PoolSetup.lua`
- Modify: `LootHistory/LootHistory.toc` — before `modules\Analytics.lua`
- Modify: `LootHistory/modules/Analytics.lua:222-232` (delete both local helpers), `:881-884`
  (the publication lines Plan A added), `:690, :719, :740, :792, :827, :895`
- Modify: `LootHistory/modules/BrowserTable.lua:660-676, :799-806`
- Modify: `LootHistory/tests/test_analytics.lua` — the pool cases from Plan A move onto the seam
- Test: `LootHistory/tests/test_poolsetup.lua` (new)

**Interfaces:**
- Consumes: `LibKa0s-Pool-1.0`.
- Produces: `NS.Pool`.

**The Plan A cases do not get deleted.** They move: the counting-factory recycling assertions now
run against `NS.Pool`, and the `Analytics._acquire` / `_releaseAll` publication lines go away with
the helpers they published. Deleting the cases instead would retire the only test that has ever
caught this bug.

- [ ] **Step 1: Write the failing test**

Create `LootHistory/tests/test_poolsetup.lua`:

```lua
-- tests/test_poolsetup.lua — the LibKa0s-Pool-1.0 seam.
--
-- The library's own suite covers the pool's semantics. What only this repo can assert is that the
-- seam is wired and that THIS addon — the one whose pool leaked — recycles.

local T = _G.LH_TEST
local NS = T.NS
local test, assertEqual, assertTrue = T.test, T.assertEqual, T.assertTrue

local function counting()
  local made = 0
  return function()
    made = made + 1
    local o = { __shown = false }
    function o:Show() self.__shown = true end
    function o:Hide() self.__shown = false end
    return o
  end, function() return made end
end

test("PoolSetup: the seam is published", function()
  assertTrue(type(NS.Pool) == "table", "NS.Pool exists")
  assertTrue(type(NS.Pool.New) == "function")
  assertTrue(type(NS.Pool.Acquire) == "function")
  assertTrue(type(NS.Pool.ReleaseAll) == "function")
end)

test("PoolSetup: a released object is reused rather than rebuilt", function()
  local p = NS.Pool.New()
  local factory, made = counting()
  for _ = 1, 3 do NS.Pool.Acquire(p, factory) end
  NS.Pool.ReleaseAll(p)
  for _ = 1, 3 do NS.Pool.Acquire(p, factory) end
  assertEqual(made(), 3, "the second pass builds nothing — this is the assertion the leak failed")
end)

test("PoolSetup: ReleaseAll returns every active object to the free list", function()
  local p = NS.Pool.New()
  local factory = counting()
  NS.Pool.Acquire(p, factory); NS.Pool.Acquire(p, factory)
  NS.Pool.ReleaseAll(p)
  local free, active = NS.Pool.Counts(p)
  assertEqual(active, 0)
  assertEqual(free, 2)
end)
```

- [ ] **Step 2: Run it to verify it fails**

Add `"test_poolsetup"` to `SUITES` in `LootHistory/tests/run.lua`, then:

```sh
cd LootHistory && lua tests/run.lua
```

Expected: FAIL — `NS.Pool` is nil.

- [ ] **Step 3: Create the seam and wire the TOC**

Create `LootHistory/core/PoolSetup.lua` — the same file as Task 1 Step 3, with a header naming this
addon's own history:

```lua
-- ── WHAT THIS REPLACED, AND WHAT IT COST ─────────────────────────────────────────────────────
--
-- This addon's chart pool was the one that got it wrong. `releaseAll` hid every active widget and
-- dropped it: the free list stayed empty, `acquire` called `factory()` every time, and since
-- LayoutCharts releases thirty-five pools at the top of every pass, each filter change allocated a
-- fresh frame per chart element. Frames are never destroyed in WoW, so they stayed for the session.
-- BankLedger's copy of the same eleven lines had always been right.
--
-- The bug was fixed on its own first, deliberately, so that the fix is a fix in the history rather
-- than a side effect of a refactor.
```

TOC line, before the `modules\` block:

```
# The LibKa0s-Pool seam. Before every module that pools a widget (Analytics, BrowserTable).
core\PoolSetup.lua
```

- [ ] **Step 4: Move `Analytics` onto the seam**

Delete the two local helpers at `:222-232` and the two publication lines Plan A added at `:881-884`.
Replace each `acquire(pool, factory)` call — `:690, :719, :740, :792, :827` — with
`NS.Pool.Acquire(pool, factory)`, and `releaseAll(P[name])` at `:895` with
`NS.Pool.ReleaseAll(P[name])`.

Route the pool construction at `:628-654` through the seam as well: each
`{ free = {}, active = {} }` literal becomes `NS.Pool.New()`. Thirty-five of them — do it with an
editor's replace-all on the exact literal, then re-read the block, because a literal that survives
is a pool the library never sees and nobody would notice.

- [ ] **Step 5: Move `BrowserTable` onto the seam**

`modules/BrowserTable.lua:660-676` and `:799-806`, as in Task 1 Step 7: extract the frame
construction into `BrowserTable:BuildRow()` and let `AcquireRow` / `ReleaseAllRows` go through
`NS.Pool`.

- [ ] **Step 6: Move the Plan A cases onto the seam**

In `tests/test_analytics.lua`, the three pool cases now read `NS.Pool.Acquire` /
`NS.Pool.ReleaseAll` instead of `NS.Analytics._acquire` / `._releaseAll`. Keep the counting factory
and keep every assertion — including `made() == 3` on the second pass, which is the one that failed
before the fix.

Delete the `LayoutCharts releases through the published helper` case from Plan A Task 2 and replace
it with the same guard against the new shape:

```lua
test("Analytics: every pool goes through the LibKa0s seam", function()
  local source = io.open("modules/Analytics.lua"):read("*a")
  local _, literals = source:gsub("{%s*free%s*=%s*{}%s*,%s*active%s*=%s*{}%s*}", "")
  assertEqual(literals, 0, "a hand-built pool literal is a pool the seam never sees")
  local _, locals = source:gsub("local function releaseAll", "")
  assertEqual(locals, 0, "the local helpers are gone")
end)
```

- [ ] **Step 7: Run the gate**

```sh
cd LootHistory && lua tests/run.lua && luacheck .
```

Expected: PASS, 0/0.

- [ ] **Step 8: Commit**

```sh
cd LootHistory
lua tests/run.lua --list > docs/test-cases.md
git add -A
git commit -m "refactor(pool): pool widgets through LibKa0s-Pool-1.0

Thirty-five chart pools and the browser's row pool move to the library. The leak
itself was fixed in its own commit first, so this one changes no behaviour — the
recycling cases move onto the seam and keep every assertion, including the one
that counts factory calls on the second pass."
```

---

### Task 3: BankLedger adopts `LibKa0s-Item-1.0`

**Files:**
- Create: `BankLedger/core/ItemSetup.lua`
- Modify: `BankLedger/BankLedger.toc` — after `core\Compat.lua` (beside the Env seam)
- Modify: `BankLedger/core/Compat.lua` — delete `ItemIDFromLink` (`:167`), `QualityLabel` (`:178`,
  with its `QUALITY_LABEL_EN` table), `LoadItem` (`:211`); **keep** `GetItemDetails` and
  `ItemNameQuality`
- Modify: `BankLedger/core/Compat.lua:116` (the internal `ItemIDFromLink` caller),
  `core/Constants.lua:181`, `modules/Export.lua:47, :157`, `modules/Browser.lua:434`,
  `modules/Insights.lua:726, :732`, `modules/LedgerTable.lua:79, :209`, `modules/Ledger.lua:426`,
  `settings/Panel.lua:166`
- Modify: `BankLedger/tests/test_compat.lua:6-27` — the primitive cases move to the seam
- Test: `BankLedger/tests/test_itemsetup.lua` (new)

**Interfaces:**
- Consumes: `Item.ItemIDFromLink`, `Item.QualityFromLink`, `Item.QualityLabel`, `Item.LoadItem`
  from `04_PLAN_B` Task 3.
- Produces: `NS.Item` — a table with the same four names.

**`modules/Insights.lua:732` passes `NS.Compat.QualityLabel` as a *function value*, not a call.**
It becomes `NS.Item.QualityLabel`; a seam that only forwards at call sites would break it.

- [ ] **Step 1: Write the failing test**

Create `BankLedger/tests/test_itemsetup.lua`:

```lua
-- tests/test_itemsetup.lua — the LibKa0s-Item-1.0 seam.
--
-- What is NOT here is the point: no case about resolving an item, because this addon's resolver
-- did not move. Compat.GetItemDetails still refuses an uncached item and records the skip, and
-- that refusal is this addon's policy (F-006), not the library's business.

local T = _G.BL_TEST
local NS = T.NS
local test, assertEqual, assertTrue = T.test, T.assertEqual, T.assertTrue

local EPIC_LINK =
  "|cffa335ee|Hitem:258586::::::::80:250::5:3:10356:10355:1540:1:28:2462:::|h[Bloodfeather Chestguard]|h|r"

test("ItemSetup: the seam is published", function()
  assertTrue(type(NS.Item) == "table")
  assertTrue(type(NS.Item.ItemIDFromLink) == "function")
  assertTrue(type(NS.Item.QualityFromLink) == "function")
  assertTrue(type(NS.Item.QualityLabel) == "function")
  assertTrue(type(NS.Item.LoadItem) == "function")
end)

test("ItemSetup: the primitives answer what the deleted shims answered", function()
  assertEqual(NS.Item.ItemIDFromLink(EPIC_LINK), 258586)
  assertEqual(NS.Item.QualityLabel(4), "Epic")
  assertEqual(NS.Item.QualityLabel(nil), "Poor")
end)

test("ItemSetup: this addon now HAS the colour fallback it lacked", function()
  -- QualityFromLink was LootHistory-only before the library. It is the primitive whose absence let
  -- an upgrade-track drop read back at its base quality; having it here does not change the gate's
  -- policy, it just means the addon can see the quality when it chooses to.
  assertEqual(NS.Item.QualityFromLink(EPIC_LINK), 4)
end)

test("ItemSetup: the resolver did NOT move", function()
  -- Deliberate. Compat.GetItemDetails refuses an uncached item and records "uncached" rather than
  -- guessing, and LootHistory's resolver guesses. Both are right for their addon, and a shared
  -- resolver would have overturned one of them.
  assertTrue(type(NS.Compat.GetItemDetails) == "function", "the resolver stays in Compat")
  assertTrue(type(NS.Compat.ItemNameQuality) == "function", "and so does ItemNameQuality")
end)

test("ItemSetup: the moved shims are gone from Compat", function()
  assertEqual(NS.Compat.ItemIDFromLink, nil)
  assertEqual(NS.Compat.QualityLabel, nil)
  assertEqual(NS.Compat.LoadItem, nil)
end)
```

- [ ] **Step 2: Run it to verify it fails**

Add `"test_itemsetup"` to `SUITES`, then:

```sh
cd BankLedger && lua tests/run.lua
```

Expected: FAIL — `NS.Item` is nil.

- [ ] **Step 3: Create the seam**

Create `BankLedger/core/ItemSetup.lua`:

```lua
local _, NS = ...

-- core/ItemSetup.lua — wires the addon into LibKa0s-Item-1.0 (library-stack-§7).
--
-- ── WHAT MOVED, AND WHAT POINTEDLY DID NOT ───────────────────────────────────────────────────
--
-- Four primitives moved: ItemIDFromLink, QualityFromLink, QualityLabel, LoadItem. Two of them were
-- byte-identical to LootHistory's and two were written by only one of the two addons — this one had
-- ItemIDFromLink, that one had QualityFromLink, and the missing colour fallback is the primitive
-- whose absence once let an upgrade-track drop record at its base quality.
--
-- THE RESOLVER DID NOT MOVE, and that is a decision rather than an oversight. Compat.GetItemDetails
-- refuses an item the client has not cached: the capture gate records the skip as "uncached" and
-- asks the client to cache the id, because "cannot be judged" is not "passes" (F-006) and a row
-- that can never be classified is not one a quality threshold ever asked for. LootHistory's
-- resolver does the opposite on purpose — it guesses from the link, because a browsable capture log
-- would rather show an approximate row than lose the drop. A shared resolver would have had to pick
-- one, and picking would have silently overturned the other.
--
-- ── WHAT A DEGRADED INSTALL GETS ─────────────────────────────────────────────────────────────
--
-- The same four primitives, locally. They are short, pure and were here before; a caller that had
-- to branch on the library's presence would be a caller that renders differently on a broken
-- install.

local Item = LibStub and LibStub("LibKa0s-Item-1.0", true)

local QUALITY_LABEL_EN = {
  [0] = "Poor", [1] = "Common", [2] = "Uncommon", [3] = "Rare",
  [4] = "Epic", [5] = "Legendary", [6] = "Artifact", [7] = "Heirloom", [8] = "WoW Token",
}

local qualityByHex

NS.Item = Item or {
  ItemIDFromLink = function(link)
    if type(link) ~= "string" then return nil end
    return tonumber(link:match("|?H?item:(%d+)"))
  end,

  QualityFromLink = function(link)
    if not link then return nil end
    local hex = link:match("|c%x%x(%x%x%x%x%x%x)")
    if not hex then return nil end
    if not qualityByHex then
      qualityByHex = {}
      if type(ITEM_QUALITY_COLORS) == "table" then
        for q = 0, 8 do
          local c = ITEM_QUALITY_COLORS[q]
          if c and c.hex then qualityByHex[c.hex:sub(-6)] = q end
        end
      end
    end
    return qualityByHex[hex]
  end,

  QualityLabel = function(q)
    q = q or 0
    return _G["ITEM_QUALITY" .. q .. "_DESC"] or QUALITY_LABEL_EN[q] or tostring(q)
  end,

  LoadItem = function(id, cb)
    if not (id and C_Item and C_Item.RequestLoadItemDataByID) then return end
    C_Item.RequestLoadItemDataByID(id)
    if cb and C_Timer and C_Timer.After then C_Timer.After(0.4, cb) end
  end,
}
```

Add `ITEM_QUALITY_COLORS` to `BankLedger/.luacheckrc`'s `read_globals` if it is not already there.

- [ ] **Step 4: Put it in the TOC**

Immediately after `core\EnvSetup.lua` (or after `core\Compat.lua` if Plan C has not run yet):

```
# The LibKa0s-Item seam. After Compat, and before core\Constants.lua, which builds the quality
# threshold labels at load through NS.Item.QualityLabel.
core\ItemSetup.lua
```

**`core/Constants.lua:181` builds its label at file load**, so this position is load-bearing. Verify
before committing:

```sh
cd BankLedger && grep -n "QualityLabel" core/Constants.lua
```

- [ ] **Step 5: Delete the moved shims and move the call sites**

Delete `Compat.ItemIDFromLink`, `Compat.QualityLabel` (with its `QUALITY_LABEL_EN`) and
`Compat.LoadItem` from `core/Compat.lua`. Point `core/Compat.lua:116`'s internal call at
`NS.Item.ItemIDFromLink`.

Replace `NS.Compat.QualityLabel` with `NS.Item.QualityLabel` at `core/Constants.lua:181`,
`modules/Export.lua:47, :157`, `modules/Browser.lua:434`, `modules/Insights.lua:726`,
`modules/LedgerTable.lua:79, :209` — and at `modules/Insights.lua:732`, where it is passed as a
**function value** (`{ labelOf = NS.Item.QualityLabel, … }`).

Replace `NS.Compat.LoadItem` with `NS.Item.LoadItem` at `modules/Ledger.lua:426` and
`settings/Panel.lua:166`.

- [ ] **Step 6: Move the primitive cases out of `test_compat.lua`**

`BankLedger/tests/test_compat.lua:6-27` tests `ItemIDFromLink` and `QualityLabel`. Those cases move
into `tests/test_itemsetup.lua` against `NS.Item` — moved, not deleted, and not duplicated.

- [ ] **Step 7: Sweep, gate, commit**

```sh
cd BankLedger
grep -rn "Compat.ItemIDFromLink\|Compat.QualityLabel\|Compat.LoadItem" --include='*.lua' . | grep -v '/libs/'
lua tests/run.lua && luacheck .
lua tests/run.lua --list > docs/test-cases.md
git add -A
git commit -m "refactor(item): item primitives through LibKa0s-Item-1.0

ItemIDFromLink, QualityLabel and LoadItem leave core/Compat.lua, and this addon
gains QualityFromLink, which only LootHistory had.

The resolver stays: Compat.GetItemDetails refuses an uncached item and records
the skip, LootHistory's guesses, and both are right for their addon. A shared
resolver would have picked one."
```

---

### Task 4: LootHistory adopts `LibKa0s-Item-1.0`

**Files:**
- Create: `LootHistory/core/ItemSetup.lua`
- Modify: `LootHistory/LootHistory.toc` — after `core\Compat.lua`, before `core\Constants.lua`
- Modify: `LootHistory/core/Compat.lua` — delete `buildQualityByHex` (`:136`), `QualityFromLink`
  (`:147`), `QualityLabel` (`:161`, with `QUALITY_LABEL_EN`), `LoadItem` (`:199`); **keep**
  `GetItemInfo` and `ItemNameQuality`
- Modify: `LootHistory/core/Compat.lua:169-185` (`GetItemInfo`'s internal `QualityFromLink` call),
  `core/Constants.lua:98`, `core/Database.lua:214`, `modules/Analytics.lua:978, :987`,
  `modules/Browser.lua:429`, `modules/Export.lua:90, :220`,
  `modules/BrowserTable.lua:170, :260`, `settings/Panel.lua:166`
- Modify: `LootHistory/tests/test_compat.lua:299-303`, `tests/test_browsertable.lua:292`,
  `tests/test_export.lua:110`
- Test: `LootHistory/tests/test_itemsetup.lua` (new)

**Interfaces:**
- Consumes: `LibKa0s-Item-1.0`.
- Produces: `NS.Item`.

**`Compat.GetItemInfo` stays and keeps calling `QualityFromLink` — through the seam.** That call is
the addon's guess-when-uncached policy, and it stays exactly where it is; only the primitive
underneath it moves.

- [ ] **Step 1: Write the failing test**

Create `LootHistory/tests/test_itemsetup.lua`:

```lua
-- tests/test_itemsetup.lua — the LibKa0s-Item-1.0 seam.

local T = _G.LH_TEST
local NS = T.NS
local test, assertEqual, assertTrue = T.test, T.assertEqual, T.assertTrue

local EPIC_LINK =
  "|cffa335ee|Hitem:258586::::::::80:250::5:3:10356:10355:1540:1:28:2462:::|h[Bloodfeather Chestguard]|h|r"

test("ItemSetup: the seam is published", function()
  assertTrue(type(NS.Item) == "table")
  assertTrue(type(NS.Item.ItemIDFromLink) == "function")
  assertTrue(type(NS.Item.QualityFromLink) == "function")
  assertTrue(type(NS.Item.QualityLabel) == "function")
  assertTrue(type(NS.Item.LoadItem) == "function")
end)

test("ItemSetup: the primitives answer what the deleted shims answered", function()
  assertEqual(NS.Item.QualityLabel(4), "Epic")
  assertEqual(NS.Item.QualityLabel(nil), "Poor")
  assertEqual(NS.Item.QualityFromLink(EPIC_LINK), 4)
end)

test("ItemSetup: this addon now HAS the id parser it lacked", function()
  -- ItemIDFromLink was BankLedger-only before the library.
  assertEqual(NS.Item.ItemIDFromLink(EPIC_LINK), 258586)
end)

test("ItemSetup: the moved shims are gone from Compat", function()
  assertEqual(NS.Compat.QualityLabel, nil)
  assertEqual(NS.Compat.QualityFromLink, nil)
  assertEqual(NS.Compat.LoadItem, nil)
end)
```

plus this addon's own version of the "the resolver did not move" case:

```lua
test("ItemSetup: the resolver did NOT move, and still guesses when uncached", function()
  -- This addon's policy, opposite to BankLedger's and deliberately so: a browsable capture log
  -- would rather show an approximate row than lose the drop.
  assertTrue(type(NS.Compat.GetItemInfo) == "function")
  local _, name, quality = NS.Compat.GetItemInfo(EPIC_LINK)
  assertEqual(quality, 4, "the colour fallback still answers for an uncached item")
  assertTrue(name ~= nil, "and the bracketed name still stands in")
end)
```

- [ ] **Step 2: Run it to verify it fails**

```sh
cd LootHistory && lua tests/run.lua
```

- [ ] **Step 3: Create the seam and wire the TOC**

Create `LootHistory/core/ItemSetup.lua` — the same file as Task 3 Step 3, with a header stating this
addon's opposite policy. TOC, after `core\Compat.lua` and before `core\Constants.lua` (which builds
threshold labels at load, `core/Constants.lua:98`).

- [ ] **Step 4: Delete the moved shims and move the call sites**

Delete `buildQualityByHex`, `Compat.QualityFromLink`, `Compat.QualityLabel` (and its
`QUALITY_LABEL_EN`) and `Compat.LoadItem`. Inside `Compat.GetItemInfo`, the fallback line becomes:

```lua
  quality = quality or NS.Item.QualityFromLink(link)
```

Replace `NS.Compat.QualityLabel` with `NS.Item.QualityLabel` at `core/Constants.lua:98`,
`modules/Analytics.lua:978, :987`, `modules/Browser.lua:429`, `modules/Export.lua:90, :220`,
`modules/BrowserTable.lua:170, :260`. Replace `NS.Compat.LoadItem` with `NS.Item.LoadItem` at
`core/Database.lua:214` and `settings/Panel.lua:166`.

- [ ] **Step 5: Move the primitive cases**

`tests/test_compat.lua:299-303` moves to `tests/test_itemsetup.lua`. Update the two references in
`tests/test_browsertable.lua:292` and `tests/test_export.lua:110` to `NS.Item.QualityLabel` — those
are assertions *using* the label, not tests *of* it, so they stay where they are.

- [ ] **Step 6: Sweep, gate, commit**

```sh
cd LootHistory
grep -rn "Compat.QualityLabel\|Compat.QualityFromLink\|Compat.LoadItem" --include='*.lua' . | grep -v '/libs/'
lua tests/run.lua && luacheck .
lua tests/run.lua --list > docs/test-cases.md
git add -A
git commit -m "refactor(item): item primitives through LibKa0s-Item-1.0

QualityFromLink, QualityLabel and LoadItem leave core/Compat.lua, and this addon
gains ItemIDFromLink, which only BankLedger had.

Compat.GetItemInfo stays exactly where it is and still guesses when the client
has not cached an item — that is this addon's policy, and the primitive under it
is the only thing that moved."
```

---

### Task 5: Verification

- [ ] **Step 1: No hand-rolled pool or moved primitive survives**

```sh
cd /path/to/GIT
for a in BankLedger LootHistory; do
  echo "### $a"
  grep -rn "free = {}, active = {}" --include='*.lua' $a | grep -v '/libs/' | grep -v 'PoolSetup'
  grep -rn "Compat.QualityLabel\|Compat.LoadItem\|Compat.ItemIDFromLink\|Compat.QualityFromLink" \
    --include='*.lua' $a | grep -v '/libs/'
done
```

Expected: **no output.**

- [ ] **Step 2: Both resolvers are still where they belong**

```sh
grep -n "function Compat.GetItemDetails" BankLedger/core/Compat.lua
grep -n "function Compat.GetItemInfo"    LootHistory/core/Compat.lua
```

Expected: both present. If either has moved, revert — that is the one thing this plan forbids.

- [ ] **Step 3: Both addons green**

```sh
for a in BankLedger LootHistory; do
  ( cd $a && lua tests/run.lua >/dev/null && luacheck . >/dev/null && echo "green: $a" ) || echo "FAILED: $a"
done
```

- [ ] **Step 4: Documentation**

Run `/wow-addon:sync-docs` in each addon. `docs/compat-layer.md` must stop listing the moved
functions, and each addon's architecture hub should name the two new seam files in its module map.
