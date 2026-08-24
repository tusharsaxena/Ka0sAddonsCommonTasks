# Plan B — LibKa0s v1.14.0: Env, Pool, Item, the copy window and the console cap

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add three new LibStub majors (`Env`, `Pool`, `Item`) and one `Widgets` member
(`CopyWindow`) to LibKa0s, raise the debug console's line cap from 500 to 1500, release the lot as
v1.14.0, and re-vendor the payload into all nine consumers.

**Architecture:** Each module is one file registering one major, gated on `LibKa0s-Core-1.0` with
the collection's standard preamble, with no state and no addon-framework dependency. All five land
in **one** release so the nine-repo re-vendor sweep happens once. Adoption is deliberately **not**
in this plan — after the sweep every addon still behaves exactly as it does today.

**Tech Stack:** Lua 5.1, LibStub, the LibKa0s test kit (`tests/_kit/`), `luacheck`, `lizard`.

**Spec:** [`02_SPEC.md`](02_SPEC.md) §B, §C, §D, §E, §F

## Global Constraints

- Lua 5.1 (`std = "lua51"`). No `goto`, no integer division.
- `luacheck .` **0 warnings / 0 errors** and `lua tests/run.lua` green before every commit. In this
  repo `exclude_files = { "tests/", "docs/" }`, so a new `LibKa0s/*.lua` **is** checked.
- Every module opens with the exact Core gate:
  ```lua
  local core = LibStub and LibStub("LibKa0s-Core-1.0", true)
  local NEEDS_CORE = 1
  if not core or (core.MINOR or 0) < NEEDS_CORE then return end   -- no NewLibrary; module absent
  ```
- Every module registers `lib.MAJOR`, `lib.MINOR` and `lib.MODULES.<File> = MINOR`.
- A new major is a new row in `tests/run.lua`'s `MAJORS` **and** a new `Loader.xmlFiles` entry comes
  free (the load list is derived from `LibKa0s.xml`).
- A minor bump is not released until `docs/api/<Major>/version-<minors>-docs.md` exists —
  `tests/test_versioning.lua` fails naming any major whose document is missing.
- New globals a new file reads must be added to `.luacheckrc`'s `read_globals`.
- No `testkit/` change: `C_Map` and `C_Item` mocks go in **`tests/wow_mock.lua`**, which is
  repo-local. A `testkit/` edit would force a `Kit.VERSION` bump and a `tests/_kit/` re-vendor into
  every consumer.
- Retail only; guard on the API's own presence, never on a game-flavor id.
- Repo for Tasks 1–7: `LibKa0s`. Task 8 touches all nine consumers.

---

### Task 1: `LibKa0s-Env-1.0`

**Files:**
- Create: `LibKa0s/LibKa0s/Env.lua`
- Modify: `LibKa0s/LibKa0s/LibKa0s.xml` (add `<Script file="Env.lua"/>` after `Core.lua`)
- Modify: `LibKa0s/tests/run.lua` (a `MAJORS` row, an `LK_TEST` key, a `suites` entry)
- Modify: `LibKa0s/tests/wow_mock.lua` (add `C_Map`)
- Modify: `LibKa0s/.luacheckrc` (`C_Map` in `read_globals`)
- Test: `LibKa0s/tests/test_env.lua`

**Interfaces:**
- Consumes: `LibKa0s-Core-1.0` (the gate only; no member is called).
- Produces: `Env.GetAddOnMetadata(addonName, field) -> string|nil`,
  `Env.Version(addonName, fallback) -> string|nil`, `Env.GetPlayerMapID() -> number|nil`,
  `Env.GetZone() -> string, string`. Plan C's nine seams call exactly these.

- [ ] **Step 1: Write the failing test**

Create `LibKa0s/tests/test_env.lua`:

```lua
-- tests/test_env.lua — the client facts every addon in the collection reads the same way.
--
-- THE CASES THAT MATTER ARE THE DEGRADED ONES. Every function here is a two-rung ladder over an
-- API Blizzard has already moved once, and the rung that gets exercised in a live client is the
-- top one — so the bottom rung is the half that ships untested unless a test removes the API. All
-- four therefore have a C_*-absent case, reached by nil-ing the mock rather than by stubbing the
-- function under test (testing-§8).

local T = _G.LK_TEST
local env, mocks = T.env, T.mocks
local test, assertEqual, assertTrue = T.test, T.assertEqual, T.assertTrue

--- Run `fn` with global `name` removed, then restore it. The mock table IS the environment the
--- library chunks were loaded into, so removing a key here is genuinely "this client does not have
--- that API" rather than a stub that pretends.
local function without(name, fn)
  local saved = mocks[name]
  mocks[name] = nil
  local ok, err = pcall(fn)
  mocks[name] = saved
  if not ok then error(err, 0) end
end

-- ── metadata ─────────────────────────────────────────────────────────────────────────────

test("env: GetAddOnMetadata reads the TOC through C_AddOns", function()
  assertEqual(env.GetAddOnMetadata("TestHost", "Version"), "1.2.3")
  assertEqual(env.GetAddOnMetadata("TestHost", "Title"), "Test Host")
end)

test("env: GetAddOnMetadata falls back to the deprecated bare global", function()
  without("C_AddOns", function()
    mocks.GetAddOnMetadata = function(_, field) return field == "Version" and "9.9.9" or nil end
    assertEqual(env.GetAddOnMetadata("TestHost", "Version"), "9.9.9")
    mocks.GetAddOnMetadata = nil
  end)
end)

test("env: GetAddOnMetadata answers nil when neither reader exists", function()
  without("C_AddOns", function()
    without("GetAddOnMetadata", function()
      assertEqual(env.GetAddOnMetadata("TestHost", "Version"), nil)
    end)
  end)
end)

-- ── version ──────────────────────────────────────────────────────────────────────────────

test("env: Version answers the TOC version", function()
  assertEqual(env.Version("TestHost"), "1.2.3")
end)

test("env: Version prefers the TOC over the fallback", function()
  -- The fallback is a hardcoded constant in the host. When the TOC can be read it is the truth,
  -- because it is what the packager stamped and the constant is what someone remembered to edit.
  assertEqual(env.Version("TestHost", "0.0.1"), "1.2.3")
end)

test("env: Version returns the fallback when the TOC cannot be read", function()
  without("C_AddOns", function()
    without("GetAddOnMetadata", function()
      assertEqual(env.Version("TestHost", "0.0.1"), "0.0.1")
      assertEqual(env.Version("TestHost"), nil)
    end)
  end)
end)

-- ── map / zone ───────────────────────────────────────────────────────────────────────────

test("env: GetPlayerMapID asks C_Map for the player's map", function()
  assertEqual(env.GetPlayerMapID(), 2112)
end)

test("env: GetPlayerMapID answers nil without C_Map", function()
  without("C_Map", function()
    assertEqual(env.GetPlayerMapID(), nil)
  end)
end)

test("env: GetZone answers zone and subzone", function()
  local zone, sub = env.GetZone()
  assertEqual(zone, "Valdrakken")
  assertEqual(sub, "The Seat of the Aspects")
end)

test("env: GetZone answers empty strings, never nil, when the readers are absent", function()
  -- LOAD-BEARING, not cosmetic. LootHistory buckets "" with nil deliberately in storage and in the
  -- Zone filter (core/Database.lua, modules/BrowserTable.lua). A nil here would move stored rows
  -- between buckets on the first re-render.
  without("GetZoneText", function()
    without("GetSubZoneText", function()
      local zone, sub = env.GetZone()
      assertEqual(zone, "")
      assertEqual(sub, "")
      assertTrue(type(zone) == "string" and type(sub) == "string", "both are always strings")
    end)
  end)
end)
```

- [ ] **Step 2: Run it to verify it fails**

```sh
cd LibKa0s && lua tests/run.lua
```

Expected: FAIL — `tests/test_env.lua` is not in the `suites` list yet, so the run is green but the
cases never execute. Confirm with `lua tests/run.lua --list | grep env` returning nothing. **That
silence is the failure**: wire the suite in (Step 3) before reading any green as meaningful.

- [ ] **Step 3: Wire the module and the suite into the runner**

In `LibKa0s/LibKa0s/LibKa0s.xml`, after the `Core.lua` line:

```xml
	<Script file="Env.lua"/>
```

In `LibKa0s/tests/run.lua`, add to `MAJORS` immediately after the `LibKa0s-Core-1.0` row:

```lua
  {
    major = "LibKa0s-Env-1.0",
    files = { "Env" },
    primary = "Env",
  },
```

add to the `Kit.expose` table:

```lua
  env = mocks.LibStub("LibKa0s-Env-1.0"),
```

and add `"test_env"` to `suites`, after `"test_core"`.

In `LibKa0s/tests/wow_mock.lua`, beside the existing `M.C_AddOns` line:

```lua
  -- The map reader LibKa0s-Env-1.0 sits on. Repo-local rather than in testkit/mock_base.lua: the
  -- kit carries APIs every addon touches, and two addons read a map id.
  M.C_Map = { GetBestMapForUnit = function(unit) return unit == "player" and 2112 or nil end }
```

and set the zone context the base mock already exposes, if it is not already what the test expects:

```lua
  M.__context.zone    = "Valdrakken"
  M.__context.subZone = "The Seat of the Aspects"
```

In `LibKa0s/.luacheckrc`, add to `read_globals`:

```lua
  "C_Map",   -- the player's map id, read by LibKa0s-Env-1.0
```

- [ ] **Step 4: Run it again to verify the cases now fail for the right reason**

```sh
cd LibKa0s && lua tests/run.lua
```

Expected: FAIL with `versioning: every declared major is actually registered` naming
`LibKa0s-Env-1.0`, and every `env:` case failing on a nil `env`.

- [ ] **Step 5: Write `LibKa0s/LibKa0s/Env.lua`**

```lua
-- LibKa0s-Env-1.0 — the handful of client facts every Ka0s addon reads, read one way.
--
-- ── WHY THIS EXISTS ──────────────────────────────────────────────────────────────────────────
--
-- `GetAddOnMetadata` was written ELEVEN times across nine addons before this module. Six copies
-- sat in a `core/Compat.lua`, in four different spellings — two-space and four-space indent, the
-- parameter called `field` and `key`, globals reached bare and through `_G.` — and the other five
-- were the same six-line ladder inlined at the call site, invisible to anyone auditing the shim
-- files. Not one of the eleven behaved differently from any other.
--
-- That is the whole case. There is no addon-specific behaviour here to descriptor-ise and no
-- plausible future in which one host needs a different answer, which is what separates this from
-- the `Compat` extraction that was tested against the evidence and rejected: a container reader is
-- BankLedger's, a mail decoder is LootHistory's, and this is nobody's.
--
-- ── WHY Version IS A MEMBER AND NOT A CALL SITE'S PROBLEM ────────────────────────────────────
--
-- Because the eleven call sites overwhelmingly want one thing — the addon's own version, for an
-- About page, a slash banner or a perf descriptor — and they spelled the fallback nine different
-- ways getting it (`or NS.version or "?"`, `or NS.VERSION`, `or ""`). A bare metadata passthrough
-- would have preserved every one of those spellings. The fallback stays VISIBLE at the call site,
-- as an argument, because which constant an addon falls back to is genuinely its own business.
--
-- ── WHY IT TAKES AN ADDON NAME ───────────────────────────────────────────────────────────────
--
-- Same reason `LibKa0s-Media-1.0` does: this library is VENDORED, so there is no one path to it
-- and a copy cannot know which addon folder it was copied into. `...` carries the addon name only
-- for a file the TOC loads directly, and `LibKa0s.xml` is loaded from inside `libs/`. The host has
-- its name verbatim as the first vararg of every file it loads, so it passes it.
--
-- Depends on LibStub and LibKa0s-Core-1.0, and on no addon framework. No Core member is called —
-- the gate is there so that a host holding a partial payload gets every module absent rather than
-- a working half, and "is LibKa0s here?" stays one question.

local core = LibStub and LibStub("LibKa0s-Core-1.0", true)
local NEEDS_CORE = 1
if not core or (core.MINOR or 0) < NEEDS_CORE then return end   -- no NewLibrary; module absent

local MAJOR, MINOR = "LibKa0s-Env-1.0", 1
local lib = LibStub:NewLibrary(MAJOR, MINOR)
if not lib then return end

lib.MAJOR, lib.MINOR = MAJOR, MINOR

lib.MODULES = lib.MODULES or {}
lib.MODULES.Env = MINOR

-- ── the TOC manifest ─────────────────────────────────────────────────────────────────────

--- One field of an addon's TOC manifest, or nil.
---
--- The reader moved under `C_AddOns` in 10.x and the bare global is deprecated but still present,
--- so both rungs are live: the namespaced one wherever it exists, the global where it does not,
--- and nil where neither does. Nil is a real answer — a field the TOC does not carry answers nil
--- on a perfectly healthy client — so a caller that needs a value supplies its own.
---
--- @param addonName string  the addon FOLDER name, from the host's first vararg
--- @param field string      a TOC key: "Version", "Title", "Notes", "Author", …
--- @return string|nil
function lib.GetAddOnMetadata(addonName, field)
  if C_AddOns and C_AddOns.GetAddOnMetadata then
    return C_AddOns.GetAddOnMetadata(addonName, field)
  end
  if GetAddOnMetadata then
    return GetAddOnMetadata(addonName, field)
  end
  return nil
end

--- An addon's own version string.
---
--- Prefers the TOC, because that is what the packager stamped; `fallback` is what the host had
--- before this module and is usually a constant somebody has to remember to edit. Returning the
--- constant in preference would make a correctly packaged addon report a stale number.
---
--- @param addonName string
--- @param fallback string|nil  the host's own constant, used only when the TOC cannot be read
--- @return string|nil
function lib.Version(addonName, fallback)
  local v = lib.GetAddOnMetadata(addonName, "Version")
  if v ~= nil and v ~= "" then return v end
  return fallback
end

-- ── where the player is ──────────────────────────────────────────────────────────────────

--- The player's current UI map id, or nil.
---
--- Best-effort by design: a map id is a stamp on a stored record, and a record with no map id is
--- worth more than a raise during a zone transition.
---
--- @return number|nil
function lib.GetPlayerMapID()
  if C_Map and C_Map.GetBestMapForUnit then
    return C_Map.GetBestMapForUnit("player")
  end
  return nil
end

--- The player's zone and subzone labels.
---
--- ALWAYS TWO STRINGS, and `""` rather than nil is the contract rather than an accident. Consumers
--- bucket `""` with nil deliberately in storage and in their zone filters, and they wrote that
--- decision down; a library that "improved" this to nil would silently move stored rows between
--- buckets on the first re-render after an upgrade.
---
--- @return string zone, string subzone
function lib.GetZone()
  local zone = (GetZoneText and GetZoneText()) or ""
  local subzone = (GetSubZoneText and GetSubZoneText()) or ""
  return zone, subzone
end
```

- [ ] **Step 6: Run the tests and luacheck**

```sh
cd LibKa0s && lua tests/run.lua && luacheck .
```

Expected: PASS, 0/0. `versioning:` cases now see `LibKa0s-Env-1.0` registered at minor 1. The
`docs/api` gate will fail — that is Task 5; if it fails **now**, note it and continue, or write the
document early.

- [ ] **Step 7: Commit**

```sh
cd LibKa0s
git add LibKa0s/Env.lua LibKa0s/LibKa0s.xml tests/test_env.lua tests/run.lua tests/wow_mock.lua .luacheckrc
git commit -m "feat(env): LibKa0s-Env-1.0 — the TOC manifest, version, map id and zone

GetAddOnMetadata existed eleven times across nine addons in four spellings, six
of them in a core/Compat.lua and five inlined at call sites where no Compat
audit would have found them. None behaved differently from any other.

Version() is a member rather than a passthrough because the eleven call sites
want one thing and spelled the fallback nine ways getting it; the fallback stays
an argument, because which constant a host falls back to is its own business.

GetZone answers \"\" and never nil: consumers bucket \"\" with nil on purpose."
```

---

### Task 2: `LibKa0s-Pool-1.0`

**Files:**
- Create: `LibKa0s/LibKa0s/Pool.lua`
- Modify: `LibKa0s/LibKa0s/LibKa0s.xml` (after `Env.lua`)
- Modify: `LibKa0s/tests/run.lua` (`MAJORS` row, `LK_TEST` key, `suites` entry)
- Test: `LibKa0s/tests/test_pool.lua`

**Interfaces:**
- Consumes: `LibKa0s-Core-1.0` (gate only).
- Produces: `Pool.New() -> pool`, `Pool.Acquire(pool, factory) -> object`,
  `Pool.ReleaseAll(pool, before)`, `Pool.Counts(pool) -> free, active`. A pool is
  `{ free = {}, active = {} }` — a plain table, no metatable.

- [ ] **Step 1: Write the failing test**

Create `LibKa0s/tests/test_pool.lua`:

```lua
-- tests/test_pool.lua — the free/active widget pool.
--
-- THE CASE THAT MATTERS IS THE RECYCLING ONE, and it is why this module exists at all. Four
-- hand-rolled copies of this pool shipped across two addons; three were correct and the fourth
-- hid its active objects without returning them to the free list, so `Acquire` fell through to
-- `factory()` every single time. Nothing about a leaking pool is visible from the outside: the
-- charts render correctly, the suite stays green, and hidden frames accumulate for the session
-- because frames are never destroyed in WoW. Counting factory calls is the only way to see it.

local T = _G.LK_TEST
local pool = T.pool
local test, assertEqual, assertTrue, assertFalse =
  T.test, T.assertEqual, T.assertTrue, T.assertFalse

--- A factory that counts how many objects it was actually asked to build, and objects that record
--- their own shown state. Deliberately not frames: this module never touches a frame API beyond
--- Show/Hide, and a plain table proves that.
local function counting()
  local made = 0
  return function()
    made = made + 1
    local o = { __shown = false, __id = made }
    function o:Show() self.__shown = true end
    function o:Hide() self.__shown = false end
    return o
  end, function() return made end
end

test("pool: New hands back an empty pool", function()
  local p = pool.New()
  local free, active = pool.Counts(p)
  assertEqual(free, 0)
  assertEqual(active, 0)
end)

test("pool: New hands back a DISTINCT pool each call", function()
  -- A shared table returned twice would make two charts fight over one free list, which is the
  -- kind of bug that only shows up under the second consumer.
  local a, b = pool.New(), pool.New()
  pool.Acquire(a, counting())
  assertEqual(select(2, pool.Counts(b)), 0, "acquiring from one pool must not touch the other")
end)

test("pool: Acquire builds when the free list is empty, and shows what it hands back", function()
  local p, factory, made = pool.New(), counting()
  factory, made = counting()
  local o = pool.Acquire(p, factory)
  assertEqual(made(), 1)
  assertTrue(o.__shown, "an acquired object is shown")
  assertEqual(select(2, pool.Counts(p)), 1, "and is on the active list")
end)

test("pool: a released object is REUSED rather than rebuilt", function()
  local p = pool.New()
  local factory, made = counting()
  for _ = 1, 3 do pool.Acquire(p, factory) end
  assertEqual(made(), 3)

  pool.ReleaseAll(p)
  for _ = 1, 3 do pool.Acquire(p, factory) end
  assertEqual(made(), 3, "the second pass must build NOTHING")
end)

test("pool: ReleaseAll hides every active object and returns it to free", function()
  local p = pool.New()
  local factory = counting()
  local a = pool.Acquire(p, factory)
  pool.Acquire(p, factory)

  pool.ReleaseAll(p)
  local free, active = pool.Counts(p)
  assertEqual(active, 0)
  assertEqual(free, 2)
  assertFalse(a.__shown, "released objects are hidden")
end)

test("pool: ReleaseAll on an empty pool is a no-op", function()
  local p = pool.New()
  pool.ReleaseAll(p)
  local free, active = pool.Counts(p)
  assertEqual(free, 0); assertEqual(active, 0)
end)

test("pool: the `before` hook runs on each object, before it is hidden", function()
  -- This hook is what lets one function cover a NESTED pool: a host releasing a pool of panels
  -- releases each panel's own row pool first. Without it that host needs a second library member
  -- and the two drift.
  local p = pool.New()
  local factory = counting()
  pool.Acquire(p, factory); pool.Acquire(p, factory)

  local seen = 0
  local shownAtHookTime = 0
  pool.ReleaseAll(p, function(o)
    seen = seen + 1
    if o.__shown then shownAtHookTime = shownAtHookTime + 1 end
  end)
  assertEqual(seen, 2, "the hook saw every active object")
  assertEqual(shownAtHookTime, 2, "and saw each one BEFORE it was hidden")
end)

test("pool: a nested release through the hook empties both levels", function()
  local panels = pool.New()
  local factory = counting()
  local panel = pool.Acquire(panels, factory)
  panel._rows = pool.New()
  pool.Acquire(panel._rows, factory)
  pool.Acquire(panel._rows, factory)

  pool.ReleaseAll(panels, function(p) pool.ReleaseAll(p._rows) end)
  assertEqual(select(2, pool.Counts(panels)), 0, "the outer pool released")
  assertEqual(select(2, pool.Counts(panel._rows)), 0, "and so did the inner one")
  assertEqual(select(1, pool.Counts(panel._rows)), 2, "the rows are back on their own free list")
end)

test("pool: acquire-release-acquire preserves object identity", function()
  -- Not decoration: a host stashes per-object state (a full label for a tooltip) on the widget,
  -- and a pool that quietly swapped identities would make that state follow the wrong row.
  local p = pool.New()
  local factory = counting()
  local first = pool.Acquire(p, factory)
  pool.ReleaseAll(p)
  local again = pool.Acquire(p, factory)
  assertEqual(again.__id, first.__id, "the same object came back")
end)
```

- [ ] **Step 2: Run it to verify it fails**

Wire the suite in first (same shape as Task 1 Step 3), then:

```sh
cd LibKa0s && lua tests/run.lua
```

Expected: FAIL — `versioning: every declared major is actually registered` names
`LibKa0s-Pool-1.0`, and every `pool:` case fails on a nil `pool`.

Wiring, precisely — in `tests/run.lua` add to `MAJORS` after the Env row:

```lua
  {
    major = "LibKa0s-Pool-1.0",
    files = { "Pool" },
    primary = "Pool",
  },
```

to `Kit.expose`:

```lua
  pool = mocks.LibStub("LibKa0s-Pool-1.0"),
```

to `suites`, after `"test_env"`: `"test_pool"`. And in `LibKa0s.xml`, after `Env.lua`:

```xml
	<Script file="Pool.lua"/>
```

- [ ] **Step 3: Write `LibKa0s/LibKa0s/Pool.lua`**

```lua
-- LibKa0s-Pool-1.0 — the free/active widget pool this collection kept rewriting.
--
-- ── WHY THIS EXISTS, AND IT IS NOT LINE COUNT ────────────────────────────────────────────────
--
-- Four copies of this pool shipped across two addons. Three were correct. The fourth —
-- LootHistory's chart pool — hid its active objects and dropped them: nothing was ever returned to
-- the free list, so `acquire` fell through to `factory()` on every call, and since that addon's
-- layout pass releases thirty-five pools at the top of every re-render, each filter change
-- allocated a fresh frame per chart element. Frames are never destroyed in WoW, so they stayed for
-- the session.
--
-- None of that is visible from outside. The charts draw correctly, the suite stays green, and the
-- only symptom is a client that gets heavier the longer a window is used. Two addons wrote the
-- same eleven lines and one of them got the second half wrong — which is the argument for a
-- library in its purest form.
--
-- ── WHAT A POOL IS HERE ──────────────────────────────────────────────────────────────────────
--
-- A plain table with two arrays and NO METATABLE:
--
--     { free = { … }, active = { … } }
--
-- Plain on purpose. A host holding a pool built before a minor upgrade keeps working, a host
-- without this library writes a nine-line local copy rather than a redesign, and a pool is
-- inspectable in a debugger without knowing anything about this file.
--
-- ── WHAT IT DELIBERATELY IS NOT ──────────────────────────────────────────────────────────────
--
-- Not Blizzard's `CreateFramePool`: that one owns frame creation, resetter functions and a
-- template, and every caller here already has its own factory closure building a fully-wired
-- widget. Not a per-object `Release`: no consumer releases one object at a time, and a member
-- nobody calls is a member nobody tests.
--
-- Depends on LibStub and LibKa0s-Core-1.0, and on no addon framework. No Core member is called;
-- the gate keeps the payload's presence a single question.

local core = LibStub and LibStub("LibKa0s-Core-1.0", true)
local NEEDS_CORE = 1
if not core or (core.MINOR or 0) < NEEDS_CORE then return end   -- no NewLibrary; module absent

local MAJOR, MINOR = "LibKa0s-Pool-1.0", 1
local lib = LibStub:NewLibrary(MAJOR, MINOR)
if not lib then return end

lib.MAJOR, lib.MINOR = MAJOR, MINOR

lib.MODULES = lib.MODULES or {}
lib.MODULES.Pool = MINOR

--- A fresh, empty pool.
---
--- @return table  { free = {}, active = {} }
function lib.New()
  return { free = {}, active = {} }
end

--- Take an object from the pool, building one only if the free list is empty.
---
--- The returned object is SHOWN. Every consumer wants that — a pooled widget is acquired in order
--- to be drawn — and a caller that wants it hidden hides it, which is one line at one call site
--- rather than a flag on every call.
---
--- @param pool table
--- @param factory function  called with no arguments; must return an object with :Show()/:Hide()
--- @return table  the acquired object
function lib.Acquire(pool, factory)
  local o = table.remove(pool.free)
  if not o then o = factory() end
  pool.active[#pool.active + 1] = o
  o:Show()
  return o
end

--- Hide every active object and RETURN IT TO THE FREE LIST.
---
--- The second half is the whole module. A release that only hides is an allocator wearing a pool's
--- name, and that is not hypothetical — it shipped.
---
--- `before` is optional and runs on each object while it is still shown, which is what makes one
--- function cover a NESTED pool: a host releasing a pool of list panels releases each panel's own
--- row pool first, as
---
---     Pool.ReleaseAll(panelPool, function(p) Pool.ReleaseAll(p._rows) end)
---
--- Without the hook that host needs a second library member, and the two drift the way the four
--- hand-rolled copies did.
---
--- @param pool table
--- @param before function|nil  called as before(object) before the object is hidden
function lib.ReleaseAll(pool, before)
  local active = pool.active
  for i = 1, #active do
    local o = active[i]
    if before then before(o) end
    o:Hide()
    pool.free[#pool.free + 1] = o
  end
  for i = #active, 1, -1 do active[i] = nil end
end

--- How many objects are parked and how many are out.
---
--- Published because a leak is otherwise unobservable: a pool that fails to recycle answers `0, 0`
--- after a release where a correct one answers `n, 0`. That is the assertion a consumer's suite
--- makes, and the one nobody could make against the four hand-rolled copies.
---
--- @param pool table
--- @return number free, number active
function lib.Counts(pool)
  return #pool.free, #pool.active
end
```

- [ ] **Step 4: Run the tests and luacheck**

```sh
cd LibKa0s && lua tests/run.lua && luacheck .
```

Expected: PASS, 0/0 (bar the `docs/api` gate, which Task 5 closes).

- [ ] **Step 5: Commit**

```sh
cd LibKa0s
git add LibKa0s/Pool.lua LibKa0s/LibKa0s.xml tests/test_pool.lua tests/run.lua
git commit -m "feat(pool): LibKa0s-Pool-1.0 — the widget pool, with the release half right

Four copies shipped across two addons. Three recycled; the fourth hid its active
objects and dropped them, turning Acquire into an allocator — invisible from
outside, because the charts still drew and frames are never destroyed in WoW.

ReleaseAll takes an optional `before` hook so one function covers a nested pool
(a panel pool releasing each panel's row pool) rather than growing a second
member that drifts from the first."
```

---

### Task 3: `LibKa0s-Item-1.0`

**Files:**
- Create: `LibKa0s/LibKa0s/Item.lua`
- Modify: `LibKa0s/LibKa0s/LibKa0s.xml` (after `Pool.lua`)
- Modify: `LibKa0s/tests/run.lua` (`MAJORS` row, `LK_TEST` key, `suites` entry)
- Modify: `LibKa0s/tests/wow_mock.lua` (`C_Item`, `ITEM_QUALITY_COLORS`, `ITEM_QUALITY*_DESC`)
- Modify: `LibKa0s/.luacheckrc` (`C_Item`, `ITEM_QUALITY_COLORS`, `C_Timer` in `read_globals`)
- Test: `LibKa0s/tests/test_item.lua`

**Interfaces:**
- Consumes: `LibKa0s-Core-1.0` (gate only).
- Produces: `Item.ItemIDFromLink(link) -> number|nil`, `Item.QualityFromLink(link) -> number|nil`,
  `Item.QualityLabel(q) -> string`, `Item.LoadItem(id, cb)`.

- [ ] **Step 1: Write the failing test**

Create `LibKa0s/tests/test_item.lua`:

```lua
-- tests/test_item.lua — the item-identity primitives, and nothing that decides policy.
--
-- WHAT IS DELIBERATELY ABSENT HERE IS THE POINT. There is no merged "resolve an item" function,
-- because the two consumers disagree — on purpose, in writing — about what an UNCACHED item means:
-- LootHistory guesses from the link's colour and brackets, BankLedger refuses and records the skip
-- so a quality gate never admits a row it cannot classify. Both are right for their addon, and a
-- shared resolver would have quietly overturned one of them. So this module carries the four
-- primitives they compose and no opinion about how.

local T = _G.LK_TEST
local item, mocks = T.item, T.mocks
local test, assertEqual, assertTrue = T.test, T.assertEqual, T.assertTrue

local EPIC_LINK =
  "|cffa335ee|Hitem:258586::::::::80:250::5:3:10356:10355:1540:1:28:2462:::|h[Bloodfeather Chestguard]|h|r"
local RARE_LINK = "|cff0070dd|Hitem:19019::::::::80:250:::::|h[Thunderfury]|h|r"

-- ── ItemIDFromLink ───────────────────────────────────────────────────────────────────────

test("item: ItemIDFromLink pulls the id out of a full link", function()
  assertEqual(item.ItemIDFromLink(EPIC_LINK), 258586)
end)

test("item: ItemIDFromLink accepts a bare itemString", function()
  assertEqual(item.ItemIDFromLink("item:19019::::::::::"), 19019)
end)

test("item: ItemIDFromLink answers nil for anything that is not a link", function()
  assertEqual(item.ItemIDFromLink("Linen Cloth"), nil)
  assertEqual(item.ItemIDFromLink(nil), nil)
  assertEqual(item.ItemIDFromLink(2589), nil)
end)

-- ── QualityFromLink ──────────────────────────────────────────────────────────────────────

test("item: QualityFromLink reads the quality out of the colour prefix", function()
  -- THE CASE THE COLLECTION LEARNED THE HARD WAY. C_Item.GetItemInfo(itemID) can only ever answer
  -- with the BASE item, so an upgrade-track drop reads back at the quality it started as. The link
  -- carries the real one in its colour, and that is the only thing available before the client has
  -- cached the item.
  assertEqual(item.QualityFromLink(EPIC_LINK), 4)
  assertEqual(item.QualityFromLink(RARE_LINK), 3)
end)

test("item: QualityFromLink answers nil for an uncoloured or absent link", function()
  assertEqual(item.QualityFromLink("|Hitem:19019::::::::::|h[Thunderfury]|h"), nil)
  assertEqual(item.QualityFromLink(nil), nil)
  assertEqual(item.QualityFromLink("Linen Cloth"), nil)
end)

test("item: QualityFromLink answers nil for a colour no quality uses", function()
  assertEqual(item.QualityFromLink("|cff123456|Hitem:1::|h[x]|h|r"), nil)
end)

-- ── QualityLabel ─────────────────────────────────────────────────────────────────────────

test("item: QualityLabel prefers the client's localized label", function()
  assertEqual(item.QualityLabel(4), "Epic")
end)

test("item: QualityLabel falls back to the static English map", function()
  -- Reached headlessly and on a client that has not populated the global. Matching on the ID and
  -- never on a localized string is localization-§4.
  local saved = mocks.ITEM_QUALITY4_DESC
  mocks.ITEM_QUALITY4_DESC = nil
  assertEqual(item.QualityLabel(4), "Epic")
  mocks.ITEM_QUALITY4_DESC = saved
end)

test("item: QualityLabel defaults to Poor when given nothing", function()
  assertEqual(item.QualityLabel(nil), "Poor")
end)

test("item: QualityLabel stringifies a quality it does not know", function()
  assertEqual(item.QualityLabel(99), "99")
end)

-- ── LoadItem ─────────────────────────────────────────────────────────────────────────────

test("item: LoadItem asks the client to cache the id", function()
  assertEqual(mocks.__loadRequests[2589], nil)
  item.LoadItem(2589)
  assertTrue(mocks.__loadRequests[2589] == true, "the request reached C_Item")
end)

test("item: LoadItem fires the callback once the item is loaded", function()
  local fired = false
  item.LoadItem(2589, function() fired = true end)
  mocks.__runTimers()
  assertTrue(fired, "the callback ran")
end)

test("item: LoadItem is inert without an id or without the API", function()
  item.LoadItem(nil, function() error("must not fire") end)
  local saved = mocks.C_Item
  mocks.C_Item = nil
  item.LoadItem(2589, function() error("must not fire") end)
  mocks.C_Item = saved
end)
```

- [ ] **Step 2: Add the mock surface this needs**

In `LibKa0s/tests/wow_mock.lua`:

```lua
  -- Item APIs, repo-local for the same reason C_Map is: two addons read them, not every addon.
  M.__loadRequests = {}
  M.C_Item = {
    RequestLoadItemDataByID = function(id) M.__loadRequests[id] = true end,
  }

  -- The colour table QualityFromLink builds its reverse map out of. Real hex values — the parse is
  -- the thing under test and a made-up palette would test the parser against itself.
  M.ITEM_QUALITY_COLORS = {
    [0] = { hex = "|cff9d9d9d" }, [1] = { hex = "|cffffffff" }, [2] = { hex = "|cff1eff00" },
    [3] = { hex = "|cff0070dd" }, [4] = { hex = "|cffa335ee" }, [5] = { hex = "|cffff8000" },
    [6] = { hex = "|cffe6cc80" }, [7] = { hex = "|cff00ccff" }, [8] = { hex = "|cff00ccff" },
  }
  M.ITEM_QUALITY0_DESC = "Poor"
  M.ITEM_QUALITY1_DESC = "Common"
  M.ITEM_QUALITY2_DESC = "Uncommon"
  M.ITEM_QUALITY3_DESC = "Rare"
  M.ITEM_QUALITY4_DESC = "Epic"
  M.ITEM_QUALITY5_DESC = "Legendary"
  M.ITEM_QUALITY6_DESC = "Artifact"
  M.ITEM_QUALITY7_DESC = "Heirloom"
  M.ITEM_QUALITY8_DESC = "WoW Token"
```

If the kit's `mock_base.lua` does not already supply a drainable `C_Timer`, add one here **and**
`M.__runTimers`:

```sh
cd LibKa0s && grep -n "C_Timer\|__runTimers" testkit/mock_base.lua tests/wow_mock.lua
```

If it is absent, add to `tests/wow_mock.lua`:

```lua
  -- A drainable timer queue: LoadItem defers its callback, and a test that cannot run the queue
  -- can only assert that nothing happened yet.
  M.__timers = {}
  M.C_Timer = { After = function(_, fn) M.__timers[#M.__timers + 1] = fn end }
  M.__runTimers = function()
    local queue = M.__timers
    M.__timers = {}
    for _, fn in ipairs(queue) do fn() end
  end
```

In `LibKa0s/.luacheckrc`, add to `read_globals`:

```lua
  "C_Item", "C_Timer", "ITEM_QUALITY_COLORS",   -- read by LibKa0s-Item-1.0
```

`ITEM_QUALITY<n>_DESC` needs no entry — it is reached through `_G[...]`, and `_G` is already
declared.

- [ ] **Step 3: Wire the module and the suite in**

`LibKa0s.xml`, after `Pool.lua`:

```xml
	<Script file="Item.lua"/>
```

`tests/run.lua` — `MAJORS` after the Pool row:

```lua
  {
    major = "LibKa0s-Item-1.0",
    files = { "Item" },
    primary = "Item",
  },
```

`Kit.expose`: `item = mocks.LibStub("LibKa0s-Item-1.0"),`
`suites`: `"test_item"`, after `"test_pool"`.

- [ ] **Step 4: Run it to verify it fails**

```sh
cd LibKa0s && lua tests/run.lua
```

Expected: FAIL — `LibKa0s-Item-1.0` declared but never registered, and every `item:` case nil.

- [ ] **Step 5: Write `LibKa0s/LibKa0s/Item.lua`**

```lua
-- LibKa0s-Item-1.0 — item identity, as primitives. No policy.
--
-- ── WHAT THIS IS NOT, FIRST ──────────────────────────────────────────────────────────────────
--
-- There is NO merged "resolve an item" function here, and its absence is the design.
--
-- Two addons in this collection resolve items, and they disagree — deliberately, in writing —
-- about what an UNCACHED item means. LootHistory guesses: it falls back to the name in the link's
-- brackets and the quality in its colour, because a browsable capture log would rather show an
-- approximate row than lose the drop. BankLedger refuses: its quality gate records the skip as
-- "uncached" and asks the client to cache the id, because "cannot be judged" is not "passes" and a
-- row it can never classify is not one a threshold ever asked for.
--
-- Both are correct for their addon. A shared resolver would have to pick one, and picking would
-- have silently overturned a decision the other addon wrote down and tested. That is exactly the
-- "shared bug surface" a module is supposed to avoid being — so this module carries the four
-- primitives both compose, and holds no opinion about how.
--
-- ── WHY THESE FOUR ───────────────────────────────────────────────────────────────────────────
--
-- `QualityLabel` and `LoadItem` were byte-identical in both addons. The other two were each
-- written by only ONE of them — BankLedger had `ItemIDFromLink`, LootHistory had
-- `QualityFromLink` — which is the better argument: each addon was missing a primitive the other
-- had already written, and the colour fallback is the one whose absence had already cost a
-- misclassified item.
--
-- Depends on LibStub and LibKa0s-Core-1.0, and on no addon framework.

local core = LibStub and LibStub("LibKa0s-Core-1.0", true)
local NEEDS_CORE = 1
if not core or (core.MINOR or 0) < NEEDS_CORE then return end   -- no NewLibrary; module absent

local MAJOR, MINOR = "LibKa0s-Item-1.0", 1
local lib = LibStub:NewLibrary(MAJOR, MINOR)
if not lib then return end

lib.MAJOR, lib.MINOR = MAJOR, MINOR

lib.MODULES = lib.MODULES or {}
lib.MODULES.Item = MINOR

-- ── identity ─────────────────────────────────────────────────────────────────────────────

--- The itemID carried by an item link or a bare itemString.
---
--- Locale-independent: it reads the link's own structure, never a displayed name.
---
--- @param link string
--- @return number|nil
function lib.ItemIDFromLink(link)
  if type(link) ~= "string" then return nil end
  return tonumber(link:match("|?H?item:(%d+)"))
end

-- Reverse map of quality-colour hex (rrggbb) → quality id, built on first use.
--
-- LAZILY, and that is a requirement rather than a style preference: this file runs from inside
-- `libs/` before the client has populated ITEM_QUALITY_COLORS, so a map built at load would be
-- empty for the life of the session and every lookup would answer nil — silently, since nil is
-- also the legitimate answer for an uncoloured link.
local qualityByHex

local function buildQualityByHex()
  qualityByHex = {}
  if type(ITEM_QUALITY_COLORS) == "table" then
    for q = 0, 8 do
      local c = ITEM_QUALITY_COLORS[q]
      if c and c.hex then qualityByHex[c.hex:sub(-6)] = q end
    end
  end
end

--- The quality id encoded in an item link's colour prefix, or nil.
---
--- THIS IS THE UNCACHED FALLBACK, and it is the reason the module is worth having. `GetItemInfo`
--- answers nothing until the client has cached the item, and when handed a bare itemID it can only
--- ever answer with the BASE item — so an upgrade-track drop reads back at the quality it started
--- as. The link's colour is the real one, available immediately, from the string the game already
--- handed the addon.
---
--- @param link string
--- @return number|nil
function lib.QualityFromLink(link)
  if not link then return nil end
  local hex = link:match("|c%x%x(%x%x%x%x%x%x)")
  if not hex then return nil end
  if not qualityByHex then buildQualityByHex() end
  return qualityByHex[hex]
end

-- ── display ──────────────────────────────────────────────────────────────────────────────

-- The English names, behind the client's own localized globals. Present so that a headless suite
-- and a client that has not populated the globals both answer something a human recognises.
local QUALITY_LABEL_EN = {
  [0] = "Poor", [1] = "Common", [2] = "Uncommon", [3] = "Rare",
  [4] = "Epic", [5] = "Legendary", [6] = "Artifact", [7] = "Heirloom", [8] = "WoW Token",
}

--- A quality id's display label.
---
--- Matched on the ID and never on a localized string (localization-§4): the client's own
--- `ITEM_QUALITY<n>_DESC` first, the static English map second, and the number itself for a
--- quality neither knows — which is a visible answer rather than a nil that renders as a blank
--- cell nobody can explain.
---
--- @param q number|nil
--- @return string
function lib.QualityLabel(q)
  q = q or 0
  return _G["ITEM_QUALITY" .. q .. "_DESC"] or QUALITY_LABEL_EN[q] or tostring(q)
end

--- Ask the server to cache an item id, and fire `cb` once it should have arrived.
---
--- Inert without an id and without the API, because both mean the same thing to a caller: no name
--- yet, show the placeholder, try again later.
---
--- @param id number
--- @param cb function|nil
function lib.LoadItem(id, cb)
  if not (id and C_Item and C_Item.RequestLoadItemDataByID) then return end
  C_Item.RequestLoadItemDataByID(id)
  if cb and C_Timer and C_Timer.After then C_Timer.After(0.4, cb) end
end
```

- [ ] **Step 6: Run the tests and luacheck**

```sh
cd LibKa0s && lua tests/run.lua && luacheck .
```

Expected: PASS, 0/0 (bar the `docs/api` gate).

- [ ] **Step 7: Commit**

```sh
cd LibKa0s
git add LibKa0s/Item.lua LibKa0s/LibKa0s.xml tests/test_item.lua tests/run.lua tests/wow_mock.lua .luacheckrc
git commit -m "feat(item): LibKa0s-Item-1.0 — item identity primitives, and no resolver

QualityLabel and LoadItem were byte-identical in two addons; ItemIDFromLink and
QualityFromLink were each written by only one of them, so each addon was missing
a primitive the other already had — and the missing colour fallback is the one
that had already cost a misclassified upgrade-track item.

No merged resolver, deliberately: the two addons disagree in writing about what
an uncached item means (guess vs. refuse-and-record), both are right for their
addon, and a shared resolver would have overturned one of them."
```

---

### Task 4: `Widgets.CopyWindow`

**Files:**
- Modify: `LibKa0s/LibKa0s/Widgets.lua` (bump `MINOR` 5 → 6; add the copy window)
- Test: `LibKa0s/tests/test_widgets.lua`

**Interfaces:**
- Consumes: `Core.ApplySkin(frame, skin)`, `Core.MakeCloseButton(parent, onClick, addonName)`.
- Produces: `Widgets.CopyWindow(descriptor) -> handle|nil` with `handle:Show(text)`,
  `handle:Hide()`, `handle:GetText() -> string`, `handle:GetFrame() -> frame`.

- [ ] **Step 1: Write the failing test**

Append to `LibKa0s/tests/test_widgets.lua`:

```lua
-- ── the copy window ──────────────────────────────────────────────────────────────────────
--
-- There is no file I/O in WoW, so every "copy this out" surface in the collection ends in a frame
-- holding a selectable multi-line EditBox. There were FOUR before this member: BankLedger's,
-- LootHistory's, MultiMeters' and the debug log's — and BankLedger's and LootHistory's were the
-- same 52 lines with the addon name substituted.
--
-- The cases below pin the two things a fifth author would have had to rediscover: the descriptor's
-- defaults, and the ORDER inside Show, which is load-bearing (highlighting before the frame is
-- shown selects nothing).

local widgetsTest = test   -- the suite's own `test`, kept legible in this block

widgetsTest("widgets: CopyWindow answers nil with no client", function()
  -- Headless, CreateFrame is a mock, so this asserts the guard exists rather than the absence.
  -- The real degraded path is a host loaded with no UI at all.
  local saved = mocks.CreateFrame
  mocks.CreateFrame = nil
  assertEqual(widgets.CopyWindow({ addonName = "TestHost" }), nil)
  mocks.CreateFrame = saved
end)

widgetsTest("widgets: CopyWindow requires an addon name", function()
  assertEqual(widgets.CopyWindow({}), nil)
  assertEqual(widgets.CopyWindow(nil), nil)
end)

widgetsTest("widgets: CopyWindow fills in the collection's defaults", function()
  local win = widgets.CopyWindow({ addonName = "TestHost" })
  assertTrue(win ~= nil, "a handle came back")
  local d = win.__descriptor
  assertEqual(d.name, "TestHostCopyWindow")
  assertEqual(d.width, 640)
  assertEqual(d.height, 420)
  assertEqual(d.fontSize, 10)
  assertEqual(d.title, "Export")
end)

widgetsTest("widgets: CopyWindow honours an overridden descriptor", function()
  local win = widgets.CopyWindow({
    addonName = "TestHost", name = "MyCopyBox", width = 500, height = 300,
    title = "Export \226\128\148 Ctrl+C, then Esc", fontSize = 12,
  })
  local d = win.__descriptor
  assertEqual(d.name, "MyCopyBox")
  assertEqual(d.width, 500)
  assertEqual(d.fontSize, 12)
end)

widgetsTest("widgets: the frame is built once and reused", function()
  local win = widgets.CopyWindow({ addonName = "TestHost" })
  win:Show("first")
  local f = win:GetFrame()
  win:Hide()
  win:Show("second")
  assertTrue(win:GetFrame() == f, "a second Show must not build a second frame — frames are never "
    .. "destroyed in WoW, so a rebuild per open leaks one per open")
end)

widgetsTest("widgets: Show puts the text in the box and leaves it shown", function()
  local win = widgets.CopyWindow({ addonName = "TestHost" })
  win:Show("a,b,c\r\n1,2,3\r\n")
  assertEqual(win:GetText(), "a,b,c\r\n1,2,3\r\n")
  assertTrue(win:GetFrame().__shown, "the frame is up")
end)

widgetsTest("widgets: Show sets the text BEFORE it highlights", function()
  -- The order is the reason this is worth sharing. Highlighting before the frame is shown selects
  -- nothing, and focusing before the text is set leaves the cursor wherever the last export left
  -- it. Recorded by spying on the EditBox rather than by reading the source.
  local win = widgets.CopyWindow({ addonName = "TestHost" })
  win:Show("seed")
  local edit, order = win:GetFrame().edit, {}
  local realSetText, realHighlight = edit.SetText, edit.HighlightText
  edit.SetText = function(s, t) order[#order + 1] = "SetText"; return realSetText(s, t) end
  edit.HighlightText = function(s) order[#order + 1] = "HighlightText"; return realHighlight(s) end
  win:Show("payload")
  edit.SetText, edit.HighlightText = realSetText, realHighlight
  assertEqual(table.concat(order, ","), "SetText,HighlightText")
end)

widgetsTest("widgets: the frame registers for Esc under its global name", function()
  local before = #mocks.UISpecialFrames
  local win = widgets.CopyWindow({ addonName = "TestHost", name = "EscapeMe" })
  win:Show("x")
  local found = false
  for i = before + 1, #mocks.UISpecialFrames do
    if mocks.UISpecialFrames[i] == "EscapeMe" then found = true end
  end
  assertTrue(found, "the global name is in UISpecialFrames, or Esc does not close it")
end)

widgetsTest("widgets: anchorTo is consulted on EVERY show", function()
  -- Not once at build: the popup has to follow a window the user moved between exports.
  local asked = 0
  local win = widgets.CopyWindow({
    addonName = "TestHost",
    anchorTo = function() asked = asked + 1; return nil end,
  })
  win:Show("one"); win:Hide(); win:Show("two")
  assertEqual(asked, 2)
end)
```

Check the top of `tests/test_widgets.lua` for the locals it already binds (`widgets`, `mocks`,
`test`, `assertEqual`, `assertTrue`) and drop the `local widgetsTest = test` alias if `test` is
already in scope — it is there only so this block can be pasted without colliding.

- [ ] **Step 2: Run it to verify it fails**

```sh
cd LibKa0s && lua tests/run.lua
```

Expected: FAIL — `attempt to call field 'CopyWindow' (a nil value)`.

- [ ] **Step 3: Implement `CopyWindow`**

In `LibKa0s/LibKa0s/Widgets.lua`, bump the minor:

```lua
local MAJOR, MINOR = "LibKa0s-Widgets-1.0", 6
```

and append, after `lib.CloseMenu`:

```lua
-- ── the copy window ──────────────────────────────────────────────────────────────────────────
--
-- WHY THIS IS HERE. There is no file I/O in WoW. Every "export this" surface in the collection
-- therefore ends in the same thing: a frame holding a multi-line EditBox with the text selected,
-- and an instruction to press Ctrl+C. There were four copies before this member — BankLedger's,
-- LootHistory's, MultiMeters' and the debug log's — and two of them were the same fifty-two lines
-- with the addon name substituted out.
--
-- It lives in Widgets rather than in a major of its own for the same reason the dropdown does:
-- Widgets already owns "a frame this collection kept re-drawing", and the three addons that need
-- this already vendor it. A new major would have bought a fourth vendor sweep for nothing.
--
-- WHAT THE HOST STILL OWNS. The art and the face arrive as DESCRIPTOR FIELDS, not as lookups: a
-- vendored copy cannot know which addon folder it sits in, so it cannot resolve a texture path or
-- ask Media for one without being told the host's name. That is the same bargain
-- LibKa0s-Media-1.0 and Core.MakeCloseButton already strike.

local COPY_DEFAULTS = {
  width = 640, height = 420, fontSize = 10, title = "Export",
  backdrop = { 0.06, 0.06, 0.08, 0.95 },
}

--- Fill a caller's descriptor out with the collection's defaults, without mutating theirs.
local function copyDescriptor(d)
  local out = {
    addonName = d.addonName,
    name      = d.name or (d.addonName .. "CopyWindow"),
    width     = d.width or COPY_DEFAULTS.width,
    height    = d.height or COPY_DEFAULTS.height,
    title     = d.title or COPY_DEFAULTS.title,
    font      = d.font,
    fontSize  = d.fontSize or COPY_DEFAULTS.fontSize,
    applySkin = d.applySkin,
    backdrop  = d.backdrop or COPY_DEFAULTS.backdrop,
    anchorTo  = d.anchorTo,
  }
  out.editWidth = d.editWidth or (out.width - 50)
  return out
end

--- Build the frame. Called once, lazily, on the first Show — a modal rebuilt per open leaks a
--- frame per open for the life of the session, because frames are never destroyed in WoW.
local function buildCopyFrame(d)
  local f = CreateFrame("Frame", d.name, UIParent, "BackdropTemplate")
  f:SetSize(d.width, d.height)
  f:SetPoint("CENTER")
  -- FULLSCREEN so it sits above the DIALOG-strata modal that opened it. The modal stays visible
  -- underneath, which is what makes "copy this, then pick a different set" one trip rather than two.
  f:SetFrameStrata("FULLSCREEN")
  f:EnableMouse(true)
  f:SetMovable(true)
  f:SetClampedToScreen(true)

  local bar = CreateFrame("Frame", nil, f)
  bar:SetPoint("TOPLEFT", 1, -1)
  bar:SetPoint("TOPRIGHT", -1, -1)
  bar:SetHeight(26)
  bar:EnableMouse(true)
  bar:RegisterForDrag("LeftButton")
  bar:SetScript("OnDragStart", function() f:StartMoving() end)
  bar:SetScript("OnDragStop", function() f:StopMovingOrSizing() end)

  local title = bar:CreateFontString(nil, "OVERLAY", "GameFontNormal")
  title:SetPoint("CENTER")
  title:SetText(d.title)
  f.title = title

  -- Resolved at CALL time rather than at load: Core is the first file in LibKa0s.xml and this is
  -- the third, so a load-time lookup would be fine here — but MakeCloseButton itself resolves Media
  -- at call time for exactly this reason, and one rule about when the payload is resolvable is
  -- easier to keep than two.
  local coreLib = LibStub and LibStub("LibKa0s-Core-1.0", true)
  if coreLib and coreLib.MakeCloseButton then
    local close = coreLib.MakeCloseButton(bar, function() f:Hide() end, d.addonName)
    if close then close:SetPoint("RIGHT", bar, "RIGHT", -6, 0) end
  end

  local scroll = CreateFrame("ScrollFrame", nil, f, "UIPanelScrollFrameTemplate")
  scroll:SetPoint("TOPLEFT", 8, -30)
  scroll:SetPoint("BOTTOMRIGHT", -28, 10)

  local edit = CreateFrame("EditBox", nil, scroll)
  edit:SetMultiLine(true)
  -- The face arrives as a PATH. SetFont does not accept a LibSharedMedia name, and a CSV is
  -- columns of digits that only line up in a fixed-width face.
  if d.font then edit:SetFont(d.font, d.fontSize, "") end
  edit:SetAutoFocus(false)
  edit:SetWidth(d.editWidth)
  edit:SetScript("OnEscapePressed", function(self) self:ClearFocus(); f:Hide() end)
  scroll:SetScrollChild(edit)

  f.scroll, f.edit = scroll, edit

  if d.applySkin then
    d.applySkin(f)
  elseif coreLib and coreLib.ApplySkin then
    coreLib.ApplySkin(f)
  end
  -- Denser than the shared skin. This frame is a wall of small monospace text, and the world
  -- behind it bleeding through costs legibility in a way it does not on a frame showing four
  -- controls.
  if f.SetBackdropColor then
    f:SetBackdropColor(d.backdrop[1], d.backdrop[2], d.backdrop[3], d.backdrop[4])
  end

  f:Hide()
  -- By NAME, type-guarded: UISpecialFrames is a list of GLOBAL frame names and the table itself is
  -- not guaranteed to exist outside a real client.
  if type(UISpecialFrames) == "table" then
    table.insert(UISpecialFrames, d.name)
  end
  return f
end

--- A read-only copy window: text in, Ctrl+C out, Esc closes.
---
--- Returns a HANDLE, not a frame, so the frame stays lazy — nothing is created until the first
--- Show, which matters because a host builds this at file load and most sessions never open it.
--- Answers nil with no client and without an `addonName` (which the close control needs to find
--- the collection's own art).
---
--- @param d table  see docs/api/Widgets — addonName is the only required field
--- @return table|nil
function lib.CopyWindow(d)
  if type(d) ~= "table" or type(d.addonName) ~= "string" then return nil end
  if type(CreateFrame) ~= "function" then return nil end

  local desc = copyDescriptor(d)
  local frame
  local win = { __descriptor = desc }

  function win:GetFrame()
    if not frame then frame = buildCopyFrame(desc) end
    return frame
  end

  function win:GetText()
    return frame and frame.edit:GetText() or nil
  end

  function win:Hide()
    if frame then frame:Hide() end
  end

  --- THE ORDER IS LOAD-BEARING: width, then text, then cursor to the top, then show, then focus,
  --- then highlight. Highlighting before the frame is shown selects nothing, and focusing before
  --- the text is set leaves the cursor wherever the last export left it. All four hand-rolled
  --- copies got this right and the fifth author would have had to rediscover it.
  function win:Show(text)
    local f = self:GetFrame()

    -- Re-anchored on EVERY show, not once at build: the popup has to land over the window that
    -- spawned it, wherever the user has since dragged that window.
    f:ClearAllPoints()
    local anchor = desc.anchorTo and desc.anchorTo()
    if anchor and anchor.IsShown and anchor:IsShown() then
      f:SetPoint("CENTER", anchor, "CENTER", 0, 0)
    else
      f:SetPoint("CENTER", UIParent, "CENTER", 0, 0)
    end

    local w = f.scroll:GetWidth()
    f.edit:SetWidth((type(w) == "number" and w > 0) and w or desc.editWidth)
    f.edit:SetText(text or "")
    f.edit:SetCursorPosition(0)
    f:Show()
    f.edit:SetFocus()
    f.edit:HighlightText()
    return f
  end

  return win
end
```

- [ ] **Step 4: Run the tests and luacheck**

```sh
cd LibKa0s && lua tests/run.lua && luacheck .
```

Expected: PASS, 0/0. If the mock's `EditBox` has no `GetText`, add one to
`LibKa0s/tests/wow_mock.lua` that records what `SetText` was handed — fidelity rule 3: anything a
test needs to observe must be recorded, not no-opped.

- [ ] **Step 5: Commit**

```sh
cd LibKa0s
git add LibKa0s/Widgets.lua tests/test_widgets.lua tests/wow_mock.lua
git commit -m "feat(widgets): CopyWindow — the export frame the collection had four copies of

BankLedger's and LootHistory's were the same fifty-two lines with the addon name
substituted; MultiMeters' called itself the third copy and was the fourth. The
art and the face arrive as descriptor fields for the same reason Media.Icon
takes an addon name: a vendored copy cannot know which folder it sits in.

Widgets rather than a new major — it already owns 'a frame this collection kept
re-drawing', and all three consumers already vendor it.

Widgets minor 5 -> 6."
```

---

### Task 4b: `MAX_BUFFER` 500 → 1500

**Files:**
- Modify: `LibKa0s/LibKa0s/DebugLog.lua:27` (MINOR), `:38-41` (the comment and the constant)
- Modify: `LibKa0s/tests/test_debuglog.lua:92-110` (the pinned literal)

**Interfaces:**
- Consumes: nothing.
- Produces: `lib.MAX_BUFFER = 1500` and `lib.MODULES.DebugLog = 11`, which Task 5's changelog block
  and API document must both name, and which two consumer suites assert against.

**Spec:** [`02_SPEC.md`](02_SPEC.md) §F

This is the smallest change in the release and the only one that turns two **consumer** suites red
the moment it lands. That is why it ships here, inside the sweep that fixes them, rather than as its
own DebugLog release beforehand.

- [ ] **Step 1: Move the pinned test first**

`tests/test_debuglog.lua:92` pins the literal deliberately — every other case reads the constant
back out of the library and would pass at any value. Change the case name and the literal, and
nothing else in it:

```lua
test("dbg: the cap is 1500 and the message frame is held to the same number", function()
  -- Pinned as a literal because every other case reads the constant back out of the library and
  -- would pass at any value. The two must move together or the visible log and the copied buffer
  -- disagree about how much history there is.
  assertEqual(debuglog.MAX_BUFFER, 1500)
```

- [ ] **Step 2: Run it to verify it fails**

```sh
cd LibKa0s && lua tests/run.lua
```

Expected: FAIL — one case, `1500 expected, got 500`. The eviction case at `:112` reads the constant
and stays green at either value; that is by design and it is not evidence.

- [ ] **Step 3: Raise the cap and bump the minor**

`LibKa0s/DebugLog.lua:41`:

```lua
lib.MAX_BUFFER = 1500
```

and extend the comment above it (`:38-40`) rather than replacing it — the "must move together"
sentence is still the reason there is one number, and the new sentence says why the number is what
it is:

```lua
-- The console keeps the last N lines and no more. Fixed by the standard rather than by the host:
-- a console is a diagnostic window read by hand, and the cap and the message frame's own SetMaxLines
-- must move together or the visible log and the copied buffer diverge.
--
-- 1500 rather than the original 500 because the perf capture workflow pastes out of THIS buffer:
-- `perf report` prints its summary here and `perf dump` writes the whole JSON record as one line
-- (Perf.lua), so a long run overflowed 500 and lost its head with nothing saying so. The copy
-- window is a view of this array and caps nothing of its own, which is why raising this raises
-- both and why there is no second number.
```

`:27` — `local MAJOR, MINOR = "LibKa0s-DebugLog-1.0", 11`.

- [ ] **Step 4: Gate**

```sh
cd LibKa0s && lua tests/run.lua && luacheck .
```

Expected: the DebugLog cases PASS. `test_versioning.lua` now **fails** naming
`docs/api/DebugLog/version-11-docs.md` — that document is Task 5, and this is the expected
intermediate state rather than a defect. Do not write the document here; Task 5 writes all of them
together so the changelog block and `lib.MODULES` are checked against each other once.

- [ ] **Step 5: Commit**

```sh
cd LibKa0s
git add LibKa0s/DebugLog.lua tests/test_debuglog.lua
git commit -m "feat(debuglog): the console holds 1500 lines, not 500

One number, not two: the copy window shows table.concat(buffer) and caps nothing
of its own, so the buffer cap IS the copy cap. The perf capture workflow pastes
out of this buffer -- perf dump writes the whole JSON record as a single line --
and 500 silently lost the head of a long run.

DebugLog minor 10 -> 11. Two consumer suites (ConsumableMaster, PrettyChat) pin
the old literal and go red until their re-vendor commit in Task 8."
```


### Task 5: API documents and the changelog

**Files:**
- Create: `LibKa0s/docs/api/Env/version-1-docs.md`
- Create: `LibKa0s/docs/api/Pool/version-1-docs.md`
- Create: `LibKa0s/docs/api/Item/version-1-docs.md`
- Create: `LibKa0s/docs/api/Widgets/version-6-docs.md`
- Create: `LibKa0s/docs/api/DebugLog/version-11-docs.md`
- Modify: `LibKa0s/docs/api/Widgets/version-5-docs.md` (Status → Superseded)
- Modify: `LibKa0s/docs/api/DebugLog/version-10-docs.md` (Status → Superseded)
- Modify: `LibKa0s/docs/api/README.md` (five new rows)
- Modify: `LibKa0s/CHANGELOG.md`

**Interfaces:**
- Consumes: the four contracts from Tasks 1–4.
- Produces: the documents `tests/test_versioning.lua` derives from live `lib.MODULES`.

- [ ] **Step 1: Confirm exactly which paths the suite demands**

```sh
cd LibKa0s && lua tests/run.lua 2>&1 | grep -i "docs/api"
```

The failure names every missing path. Write those paths, not guessed ones.

- [ ] **Step 2: Copy the nearest existing document as the template**

```sh
cd LibKa0s
cp docs/api/Media/version-1-docs.md docs/api/Env/version-1-docs.md      # a first version, no Supersedes
cp docs/api/Media/version-1-docs.md docs/api/Pool/version-1-docs.md
cp docs/api/Media/version-1-docs.md docs/api/Item/version-1-docs.md
cp docs/api/Widgets/version-5-docs.md docs/api/Widgets/version-6-docs.md
cp docs/api/DebugLog/version-10-docs.md docs/api/DebugLog/version-11-docs.md
```

Then rewrite each to its own contract. For the three new majors: `Status` → **Current**,
`Supersedes` → *(first version)*, every member's `Since` → **1**. For Widgets 6: `Status` →
**Current**, `Supersedes` → version 5, a *What changed at this version* section describing
`CopyWindow`, and `Since: 6` on `CopyWindow` and every descriptor field.

For DebugLog 11: `Status` → **Current**, `Supersedes` → version 10, a *What changed at this version*
section saying the line cap moved 500 → 1500 and nothing else did, and the `lib.MAX_BUFFER` row
(version 10's `:125`) restated as **1500** with `Since: 1` kept — the member is not new, its value
moved. The row's own sentence about the cap and `SetMaxLines` moving together stays; add why 1500
(the perf capture pastes out of this buffer) and that the copy window is a view of it, so there is
no second cap.

- [ ] **Step 3: Mark Widgets 5 and DebugLog 10 superseded**

In `docs/api/Widgets/version-5-docs.md` and `docs/api/DebugLog/version-10-docs.md`: `Status` →
Superseded, fill `Superseded by`, and add the closing *Moving to version 6* / *Moving to version 11*
section. **Never** edit a superseded document to describe new
behaviour — an adopter still on that copy has to be able to read what their copy actually does.

- [ ] **Step 4: Add the rows to `docs/api/README.md`**

Four rows, in the table's existing shape.

- [ ] **Step 5: Write the changelog block**

At the top of `LibKa0s/CHANGELOG.md`:

```markdown
## v1.14.0 — <date>

Versions in this release: **Core minor 6**, **Env minor 1**, **Pool minor 1**, **Item minor 1**,
**Media minor 3**, **Widgets minor 6**, **DebugLog minor 11**, **Slash minor 7**, **Options minor 8**,
**OptionsWidgets minor 7**, **OptionsScroll minor 3**, **Perf minor 7**, **PerfPanel minor 4**,
**kit revision 11**.
```

followed by the entries — what each module is and why it exists. `test_versioning.lua` fails if this
block and any major's `lib.MODULES` disagree, so the file minors above must be the live ones. Read
them out of the source rather than from this plan if there is any doubt:

```sh
cd LibKa0s && grep -n "MINOR = " LibKa0s/*.lua
```

- [ ] **Step 6: Run the full gate**

```sh
cd LibKa0s && lua tests/run.lua && luacheck .
```

Expected: PASS, 0/0 — including the versioning cases, which now find every document.

- [ ] **Step 7: Regenerate the case list**

```sh
cd LibKa0s && lua tests/run.lua --list
```

into `docs/test-cases.md`, keeping CRLF — the exact command is in that file's own banner.

- [ ] **Step 8: Commit**

```sh
cd LibKa0s
git add docs/api CHANGELOG.md docs/test-cases.md
git commit -m "docs(api): contracts for Env 1, Pool 1, Item 1, Widgets 6 and DebugLog 11"
```

---

### Task 6: The release gate

**Files:**
- Modify: `LibKa0s/docs/releasing.md` (the provenance template and the semver in the header table)
- Create: `LibKa0s/docs/automated-tests/<stamp>/` (the frozen bundle)
- Modify: `LibKa0s/docs/automated-tests/RESULTS.md`

- [ ] **Step 1: Move the provenance template to v1.14.0**

In `docs/releasing.md`, update the templated line under "Re-vendoring consumers" and the repo semver
in the table at the top. This is a numbered step in that playbook precisely because the alternative
is remembering, and at v1.5.0 the remembering did not happen.

- [ ] **Step 2: Update the module inventory sentences in `docs/releasing.md`**

Step 2 of that playbook lists the nine file-minor constants by name and step 3 says the `MAJORS`
table "carries one row per shipped major — seven today". Both are now wrong: twelve files, ten
majors. Fix both counts and add `MINOR` in `Env.lua`, `Pool.lua` and `Item.lua` to the list.

- [ ] **Step 3: Run the full battery and freeze the bundle**

```sh
cd LibKa0s && tests/_kit/run-automated-tests.sh --release 1.14.0
```

Read all four suites before going further. **The release gate is all four at `pass` plus zero
functions above CCN 15** (`automated-tests-§3`). A `skip` is NOT EVALUATED rather than passed —
`perf` is a standing skip in this repo because it ships no `tests/perf.lua`, and that is a recorded
hole in the gate, not a pass.

- [ ] **Step 4: Commit and tag**

The bundle and the `RESULTS.md` row belong in the release commit, so the tagged tree contains the
evidence for itself.

```sh
cd LibKa0s
git add docs/releasing.md docs/automated-tests
git commit -m "release: LibKa0s v1.14.0 — Env, Pool and Item majors, Widgets CopyWindow, a 1500-line console"
git tag v1.14.0
```

---

### Task 7: Sweep the consumers table

**Files:**
- Modify: `LibKa0s/docs/releasing.md` (the Consumers table)

- [ ] **Step 1: Re-sweep against the source**

```sh
cd LibKa0s
for a in AbsorbTracker BankLedger ConsumableMaster KickCD LootHistory MultiMeters PanelMaster PrettyChat WhatGroup; do
    grep -rnoE 'LibStub\("LibKa0s-[A-Za-z]+-1\.0", true\)' ../$a --include='*.lua' \
      | grep -v '/libs/' | grep -v '/tests/'
done
```

Every file that prints must appear in the table's third column. This is maintained by hand and the
wiring is not; a second lookup site nobody recorded is a file the checklist never points a reviewer
at.

- [ ] **Step 2: Commit**

```sh
cd LibKa0s && git add docs/releasing.md && git commit -m "docs(releasing): re-sweep the consumers table"
```

---

### Task 8: Re-vendor the payload into all nine consumers

**Files, per consumer:**
- Modify: `<consumer>/libs/LibKa0s/` (the whole payload)
- Modify: `<consumer>/tests/run.lua` (the hand-listed LibKa0s load list)
- Modify: `<consumer>/CLAUDE.md` (the provenance line)
- Modify, in the four consumers that name the old cap: `ConsumableMaster/tests/test_debuglog.lua`,
  `PrettyChat/tests/test_debuglog.lua`, `AbsorbTracker/docs/{ARCHITECTURE,module-map}.md`,
  `WhatGroup/docs/debug.md`

The consumers are **AbsorbTracker, BankLedger, ConsumableMaster, KickCD, LootHistory, MultiMeters,
PanelMaster, PrettyChat, WhatGroup**. BuffTextNotifications and WhoGotLoots do not vendor LibKa0s.

**This task adds three files to a payload every consumer's test runner lists by hand.** Missing that
edit is silent: the addon still loads (the client reads `LibKa0s.xml`), but the headless suite never
sees the new modules and every "the library is absent" branch tests as if it were true.

**It also carries Task 4b's cap into four consumers that state the old number.** Two of them assert
it and go red on the copy alone; the other two only say it in prose, which is worse, because nothing
goes red. Their edits land in the same commit as their payload — a suite that pins 500 beside a
library holding 1500 is a broken build, and a doc that says 500 beside it is a lie nobody is
watching. Step 3b below names all four; the other five consumers have no such edit.

Repeat Steps 1–5 **once per consumer**, committing each separately.

- [ ] **Step 1: Copy the payload**

```sh
cd /path/to/GIT
rm -rf <consumer>/libs/LibKa0s
cp -r LibKa0s/LibKa0s <consumer>/libs/LibKa0s
diff -r LibKa0s/LibKa0s <consumer>/libs/LibKa0s && echo "byte-identical"
```

Expected: no output from `diff`, then `byte-identical`. An empty `diff -r` is `library-stack-§7`'s
vendor-sync MUST and each consumer's `tests/test_vendor_sync.lua` asserts it.

- [ ] **Step 2: Add the three new files to the consumer's test load list**

In `<consumer>/tests/run.lua`, the `Loader.loadAll({ … })` block that spells out
`libs/LibKa0s/*.lua` in XML order. Insert so the order matches `LibKa0s.xml` exactly:

```lua
  "libs/LibKa0s/Core.lua",
  "libs/LibKa0s/Env.lua",
  "libs/LibKa0s/Pool.lua",
  "libs/LibKa0s/Item.lua",
  "libs/LibKa0s/Media.lua",
  "libs/LibKa0s/Widgets.lua",
  ...
```

Verify the order against the XML rather than against this plan:

```sh
cd <consumer> && grep -o 'file="[^"]*"' libs/LibKa0s/LibKa0s.xml
```

- [ ] **Step 3: Roll the provenance line**

In `<consumer>/CLAUDE.md`, find the line naming the vendored LibKa0s version and set it to
**v1.14.0**. It moves in the same commit as the copy — a payload whose provenance line still names
the previous version is a copy nobody can date.

- [ ] **Step 3b: Carry the new cap into the four consumers that name the old one**

Only these four. Run the sweep first rather than trusting the list:

```sh
cd /path/to/GIT
grep -rn "500" <consumer> --include='*.lua' --include='*.md' \
  | grep -iv '/libs/' | grep -i "buffer\|max_lines\|lines"
```

- **ConsumableMaster** — `tests/test_debuglog.lua:256`:
  ```lua
      t.eq(lib.MAX_BUFFER, 1500, "the buffer cap still matches the library's one number")
  ```
  The old message said "still matches the old MAX_LINES" — a constant that predates the library and
  no longer exists anywhere. It goes with the number.

- **PrettyChat** — `tests/test_debuglog.lua:187` (`t.eq(#D.buffer, 1500, ...)`) and `:203`
  (`"1 / 1500 lines"`). Read the loop above `:187` before editing: it writes more lines than the cap
  and the literal is the assertion, not the loop bound. If the loop is written with a literal bound
  such as `for i = 1, 600`, it must move too or it stops overflowing the buffer and the case
  silently stops testing eviction.

- **AbsorbTracker** — prose only, five places: `docs/ARCHITECTURE.md:64` (`lib.MAX_BUFFER = 500`),
  `docs/module-map.md:296` ("the 500-line buffer"), `:352` (`N / 500 lines` in the call-sketch),
  `:770` and `:862` ("the 500-line buffer (`MAX_BUFFER`)").

- **WhatGroup** — prose only, `docs/debug.md:94` ("capped at `lib.MAX_BUFFER`, 500 lines"), `:133`
  (`SetMaxLines(500)`), `:148` ("a right-aligned `N / 500 lines` counter").

The five remaining consumers — BankLedger, KickCD, LootHistory, MultiMeters, PanelMaster — state the
cap nowhere and need no edit beyond the payload. Confirm that with the sweep rather than assuming
it.

- [ ] **Step 4: Run the consumer's gate**

```sh
cd <consumer> && lua tests/run.lua && luacheck .
```

Expected: PASS, 0/0. Nothing in the consumer has adopted anything yet, so behaviour is unchanged;
the new modules simply register and the console holds more history. For ConsumableMaster and
PrettyChat specifically, run the suite **before** Step 3b as well and confirm it is red on the cap
— that is the evidence those two assertions were doing their job.

- [ ] **Step 5: Commit**

```sh
cd <consumer>
git add libs/LibKa0s tests/run.lua CLAUDE.md
git commit -m "chore(libs): re-vendor LibKa0s v1.14.0

Adds LibKa0s-Env-1.0, LibKa0s-Pool-1.0 and LibKa0s-Item-1.0 to the payload and
takes Widgets to minor 6 (CopyWindow) and DebugLog to minor 11 (the console
holds 1500 lines, not 500). Nothing in this addon adopts the new majors yet —
this commit is the copy and the provenance line.

The one behaviour change is the console history depth, which is the library’s
and arrives with the copy.

diff -r against the source repo is empty."
```

- [ ] **Step 6: Repeat for the remaining consumers**

Nine in total. Tick them off here: AbsorbTracker ☐ BankLedger ☐ ConsumableMaster ☐ KickCD ☐
LootHistory ☐ MultiMeters ☐ PanelMaster ☐ PrettyChat ☐ WhatGroup ☐

---

## What happens next

Adoption is **not** in this plan and must not be smuggled into it. After Task 8 every addon behaves
exactly as it did before, and the three adoption plans run independently:

- [`05_PLAN_C_ENV_ADOPTION.md`](05_PLAN_C_ENV_ADOPTION.md) — nine addons
- [`06_PLAN_D_POOL_AND_ITEM_ADOPTION.md`](06_PLAN_D_POOL_AND_ITEM_ADOPTION.md) — BankLedger, LootHistory
- [`07_PLAN_E_COPYWINDOW_ADOPTION.md`](07_PLAN_E_COPYWINDOW_ADOPTION.md) — BankLedger, LootHistory, MultiMeters
