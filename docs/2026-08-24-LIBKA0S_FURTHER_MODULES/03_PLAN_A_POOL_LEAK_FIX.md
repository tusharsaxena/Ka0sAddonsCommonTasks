# Plan A — LootHistory chart-pool leak Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `LootHistory`'s Analytics widget pools actually recycle, so re-rendering the Insights
tab stops allocating a fresh frame per chart element for the life of the session.

**Architecture:** One function body is wrong — `releaseAll` hides active objects without returning
them to `pool.free`, so `acquire` always falls through to `factory()`. The fix is BankLedger's
already-correct body. The two file-local helpers are published as `Analytics._acquire` /
`Analytics._releaseAll` (the file's existing convention for "published for the headless suite") so
the recycling can be asserted rather than read.

**Tech Stack:** Lua 5.1, the vendored LibKa0s test kit (`tests/_kit/`), `luacheck`.

**Spec:** [`02_SPEC.md`](02_SPEC.md) §A

## Global Constraints

- Lua 5.1 (`std = "lua51"`).
- `luacheck .` must report **0 warnings / 0 errors**; `lua tests/run.lua` must be green.
- Retail only; no game-flavor branching.
- No user-visible behaviour change other than the fix itself.
- Repo: `LootHistory`. This plan touches **no** library and **no** other addon.

---

### Task 1: Publish the pool helpers and pin the recycling contract

**Files:**
- Modify: `LootHistory/modules/Analytics.lua:222-232` (the two helpers), plus one publication line
  beside the existing `Analytics._dayKeyList` block at `:881-884`
- Test: `LootHistory/tests/test_analytics.lua`

**Interfaces:**
- Consumes: nothing.
- Produces: `Analytics._acquire(pool, factory) -> object` and `Analytics._releaseAll(pool)`, both
  reading and writing a pool of the shape `{ free = {}, active = {} }`. Task 2 asserts against these
  names.

- [ ] **Step 1: Write the failing test**

Append to `LootHistory/tests/test_analytics.lua`, after the `_tipText` block:

```lua
-- ── the widget pools (recycling) ────────────────────────────────────────────────────
--
-- The bug this pins: releaseAll used to hide the active objects and drop them, never returning
-- them to pool.free. acquire then fell through to factory() on every single call, and since
-- LayoutCharts releases all 35 pools at the top of every pass, every re-render allocated a fresh
-- frame per chart element — and frames are never destroyed in WoW. Counting factory calls is the
-- only way to see that from a test; reading pool.free would pass against a pool nobody reuses.

local function countingPool()
  local made = 0
  local pool = { free = {}, active = {} }
  local factory = function()
    made = made + 1
    local o = { __shown = false }
    function o:Show() self.__shown = true end
    function o:Hide() self.__shown = false end
    return o
  end
  return pool, factory, function() return made end
end

test("Analytics pool: a released object is reused rather than rebuilt", function()
  local pool, factory, made = countingPool()
  for _ = 1, 3 do NS.Analytics._acquire(pool, factory) end
  assertEqual(made(), 3, "first pass builds three")

  NS.Analytics._releaseAll(pool)
  for _ = 1, 3 do NS.Analytics._acquire(pool, factory) end
  assertEqual(made(), 3, "second pass must build NOTHING — every object comes back off pool.free")
end)

test("Analytics pool: releaseAll returns every active object to the free list", function()
  local pool, factory = countingPool()
  local a = NS.Analytics._acquire(pool, factory)
  NS.Analytics._acquire(pool, factory)
  assertEqual(#pool.active, 2)
  assertEqual(#pool.free, 0)

  NS.Analytics._releaseAll(pool)
  assertEqual(#pool.active, 0, "active is emptied")
  assertEqual(#pool.free, 2, "and the objects land on free — this is the assertion the leak failed")
  assertFalse(a.__shown, "a released object is hidden")
end)

test("Analytics pool: acquire shows what it hands back", function()
  local pool, factory = countingPool()
  local o = NS.Analytics._acquire(pool, factory)
  assertTrue(o.__shown, "a freshly built object is shown")
  NS.Analytics._releaseAll(pool)
  local again = NS.Analytics._acquire(pool, factory)
  assertTrue(again.__shown, "and a recycled one is shown again")
end)
```

- [ ] **Step 2: Run the tests to verify they fail**

```sh
cd LootHistory && lua tests/run.lua
```

Expected: FAIL. The first failure is `attempt to call field '_acquire' (a nil value)` — the helpers
are file-local and not published yet.

- [ ] **Step 3: Publish the helpers**

In `LootHistory/modules/Analytics.lua`, beside the existing publication block at `:881-884`
(`Analytics._dayKeyList = dayKeyList` …), add:

```lua
-- The widget pools, published for the headless suite. NOT pure — they mutate the pool — and that is
-- exactly why they are here: whether a released object comes back off pool.free is invisible from
-- the outside, and the one time it was wrong (every LayoutCharts pass rebuilt every frame) nothing
-- in the suite could have noticed.
Analytics._acquire      = acquire
Analytics._releaseAll   = releaseAll
```

- [ ] **Step 4: Run the tests again**

```sh
cd LootHistory && lua tests/run.lua
```

Expected: the "returns every active object to the free list" and "is reused rather than rebuilt"
cases now FAIL on the assertion rather than on a nil call — `assertEqual(#pool.free, 2)` reports
`0`, and `made()` reports `6` instead of `3`. That is the leak, reproduced.

- [ ] **Step 5: Fix `releaseAll`**

Replace `LootHistory/modules/Analytics.lua:229-232` with:

```lua
-- Hide every active object AND put it back on the free list, which is the whole point of a pool.
-- Dropping them instead (which this did until 2026-08-24) turns `acquire` into an allocator: the
-- free list is empty on every call, `factory()` runs every time, and because frames are never
-- destroyed in WoW the abandoned ones stay for the session. LayoutCharts releases all 35 pools at
-- the top of every pass, so the cost was one fresh frame per chart element per re-render.
local function releaseAll(pool)
  for _, o in ipairs(pool.active) do
    o:Hide()
    pool.free[#pool.free + 1] = o
  end
  wipe(pool.active)
end
```

- [ ] **Step 6: Run the tests to verify they pass**

```sh
cd LootHistory && lua tests/run.lua && luacheck .
```

Expected: all suites PASS; luacheck 0/0.

- [ ] **Step 7: Regenerate the case inventory**

```sh
cd LootHistory && lua tests/run.lua --list > docs/test-cases.md
```

Keep the file's existing line endings — read the banner at the top of `docs/test-cases.md` for the
exact command this repo uses, and use that if it differs.

- [ ] **Step 8: Commit**

```sh
cd LootHistory
git add modules/Analytics.lua tests/test_analytics.lua docs/test-cases.md
git commit -m "fix(analytics): the chart pools recycle instead of allocating every pass

releaseAll hid every active widget and dropped it, so pool.free was empty on
every acquire and factory() ran each time. LayoutCharts releases all 35 pools
at the top of every layout pass, and frames are never destroyed in WoW, so each
re-render of the Insights tab abandoned a full set of bars, swatches and rows
for the rest of the session.

Return released objects to the free list, the way BankLedger's copy of the same
helper always did. The two helpers are published as Analytics._acquire /
._releaseAll so the recycling is asserted by counting factory calls rather than
by reading the source."
```

---

### Task 2: Prove the fix reaches the real render path

**Files:**
- Test: `LootHistory/tests/test_analytics.lua`

**Interfaces:**
- Consumes: `Analytics._acquire`, `Analytics._releaseAll` from Task 1.
- Produces: nothing new.

Task 1 pins the helper. This task pins that the helper is the one `LayoutCharts` actually uses — a
fix to a published copy that the render path bypasses is a green suite over a live leak.

- [ ] **Step 1: Write the failing test**

Append to `LootHistory/tests/test_analytics.lua`:

```lua
test("Analytics pool: LayoutCharts releases through the published helper", function()
  -- Guards against the published helper drifting from the one the render path calls. If someone
  -- later inlines a second release loop into LayoutCharts, the fix above stops covering the code
  -- that leaks, and nothing else in this suite would say so.
  local source = io.open("modules/Analytics.lua"):read("*a")
  local _, releases = source:gsub("releaseAll%(P%[name%]%)", "")
  assertEqual(releases, 1,
    "LayoutCharts must release through the single shared helper; a second release path is a "
    .. "second chance to leak")
  local _, defs = source:gsub("local function releaseAll", "")
  assertEqual(defs, 1, "exactly one releaseAll definition in this file")
end)
```

- [ ] **Step 2: Run it**

```sh
cd LootHistory && lua tests/run.lua
```

Expected: PASS immediately — this case documents and locks the current shape rather than driving a
change. If it fails, the file has a second release path and **that** path must be fixed the same way
before continuing.

- [ ] **Step 3: Commit**

```sh
cd LootHistory
git add tests/test_analytics.lua docs/test-cases.md
git commit -m "test(analytics): pin that LayoutCharts releases through the one shared helper"
```

---

### Task 3: Record the fix

**Files:**
- Modify: `LootHistory/CHANGELOG.md` (if the repo keeps one) or the README's "What's new" — check
  which this repo uses before editing; the collection allows a `CHANGELOG.md` only in Ka0s-owned
  library repos, so in an addon this is the README.
- Modify: `LootHistory/docs/` — whichever topic doc describes the Insights/Analytics pane

- [ ] **Step 1: Find where this repo records changes**

```sh
cd LootHistory && ls CHANGELOG.md 2>/dev/null; grep -n "What's new" README.md | head -3
```

- [ ] **Step 2: Add the entry**

Under the current unreleased/next-version heading, in the repo's own voice:

```markdown
**The Insights charts stopped rebuilding themselves.** The widget pools behind every bar, swatch and
list row hid their contents on each re-render but never returned them for reuse, so a filter change
or a tab switch allocated a fresh frame per element — and frames are never destroyed in WoW. Long
sessions with a lot of chart interaction accumulated hidden frames for the rest of the session.
```

- [ ] **Step 3: Commit**

```sh
cd LootHistory
git add -A
git commit -m "docs: record the Analytics pool-recycling fix"
```

---

## Follow-up (not part of this plan)

Open a GitHub issue on LootHistory recording the defect and this fix, labelled `state:done` with a
severity that reflects a shipped unbounded-allocation defect, so the issue store carries it. Use
`/wow-addon:issue-add`. Do this **after** the fix is committed, so the issue can name the commit.
