# Plan C — `LibKa0s-Env-1.0` adoption across nine addons

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Retire eleven hand-rolled copies of `GetAddOnMetadata` and two each of `GetPlayerMapID`
and `GetZone` across nine addons, replacing them with one seam per addon over
`LibKa0s-Env-1.0`.

**Architecture:** Each addon grows `core/EnvSetup.lua` — a seam on the exact model of the
`core/MediaSetup.lua` every one of them already has. It resolves the library once, binds the
addon's own folder name, and degrades to the addon's current behaviour when the library is absent.
The per-addon `Compat.GetAddOnMetadata` / `GetPlayerMapID` / `GetZone` are deleted, and the
call-site copies — the ones no `Compat` audit would ever have found — are deleted with them.

**Tech Stack:** Lua 5.1, LibStub, each addon's vendored test kit, `luacheck`.

**Spec:** [`02_SPEC.md`](02_SPEC.md) §B

**Prerequisite:** [`04_PLAN_B_LIBKA0S_MODULES.md`](04_PLAN_B_LIBKA0S_MODULES.md) Task 8 — the
payload carrying `Env.lua` must already be vendored into the addon being worked on.

## Global Constraints

- Lua 5.1. `luacheck .` **0/0** and `lua tests/run.lua` green before every commit, in the addon
  being worked on.
- **`LibStub("LibKa0s-Env-1.0", true)` — always with the silent flag.** The headless mock's LibStub
  is strict: a lookup written without it resolves to nil and raises.
- **No user-visible behaviour change.** Every one of these functions already answers the same thing
  in all eleven copies; if adoption changes an answer, adoption is wrong.
- **`GetZone` returns two strings and never nil.** LootHistory and BankLedger bucket `""` with nil
  deliberately in storage and in their filters. Preserve that exactly.
- **Each addon's `core/Compat.lua` stays.** It thins to the addon-specific shims it was always for.
- **A consumer must not duplicate the library's unit coverage** (`testing-§8`). The addon's test
  asserts *its seam* — that the helper answers what the deleted shim answered, and that it answers
  the addon's own fallback with the library absent.
- One commit per addon. An addon that has not adopted is still correct.

---

## Reference seam

Every addon's `core/EnvSetup.lua` is this file with the addon's own name in the header and only the
members that addon actually uses. It is written out here in full so that no task has to say "like
the last one".

```lua
local addonName, NS = ...

-- core/EnvSetup.lua — wires the addon into LibKa0s-Env-1.0 (library-stack-§7).
--
-- ── WHAT THIS REPLACED ───────────────────────────────────────────────────────────────────────
--
-- The TOC-metadata reader. It was written ELEVEN times across nine addons before the library had
-- it: six copies in a core/Compat.lua, in four different spellings, and five more inlined straight
-- at the call site where no audit of the shim files would ever have found them. Not one of the
-- eleven behaved differently from any other, which is what made it a library candidate rather than
-- an addon's business.
--
-- ── WHY THE LIBRARY HAS TO BE TOLD OUR NAME ──────────────────────────────────────────────────
--
-- Same reason core/MediaSetup.lua passes it: LibKa0s is VENDORED, so a copy cannot know which
-- addon folder it sits in. `addonName` is the FIRST VARARG every TOC-loaded file gets — not the
-- frame prefix, not the `## Title`, and not a hand-typed literal, all of which have been a
-- different string from the folder name at least once in this collection.
--
-- ── WHAT A DEGRADED INSTALL GETS ─────────────────────────────────────────────────────────────
--
-- Exactly what this addon got before the library existed. Every helper below falls back to the
-- same ladder the deleted shim ran, so an install missing LibKa0s reads its own TOC and stamps its
-- own zone as it always did. That is why the fallbacks are written out rather than left to answer
-- nil: this is a seam, not a feature.

local Env = LibStub and LibStub("LibKa0s-Env-1.0", true)

--- One field of this addon's TOC manifest, or nil.
---
--- @param field string  "Version", "Title", "Notes", "Author", …
--- @return string|nil
function NS.Meta(field)
  if Env then return Env.GetAddOnMetadata(addonName, field) end
  if C_AddOns and C_AddOns.GetAddOnMetadata then
    return C_AddOns.GetAddOnMetadata(addonName, field)
  end
  if GetAddOnMetadata then return GetAddOnMetadata(addonName, field) end
  return nil
end

--- This addon's version string, preferring the TOC over the fallback constant.
---
--- The fallback stays visible here rather than inside the library because which constant this
--- addon falls back to is genuinely its own business — and because a packaged addon whose TOC can
--- be read should never report the constant somebody forgot to edit.
---
--- @return string
function NS.Version()
  if Env then return Env.Version(addonName, NS.version) or "?" end
  return NS.Meta("Version") or NS.version or "?"
end

--- The player's current UI map id, or nil.  -- only where the addon stamps one
function NS.PlayerMapID()
  if Env then return Env.GetPlayerMapID() end
  if C_Map and C_Map.GetBestMapForUnit then return C_Map.GetBestMapForUnit("player") end
  return nil
end

--- Zone and subzone. ALWAYS two strings; "" when the client has no text yet.
---
--- The empty string is load-bearing rather than tidy: this addon buckets "" with nil in storage
--- and in its zone filter, and a nil here would move stored rows between buckets.
---
--- @return string zone, string subzone
function NS.Zone()
  if Env then return Env.GetZone() end
  local zone = (GetZoneText and GetZoneText()) or ""
  local subzone = (GetSubZoneText and GetSubZoneText()) or ""
  return zone, subzone
end
```

**TOC placement.** `core\EnvSetup.lua` goes immediately after `core\Compat.lua` — except where an
addon reads its version at FILE LOAD, in which case it must precede that file. Two addons do:
MultiMeters (`core/Namespace.lua:64`) and PrettyChat (`core/Namespace.lua:7`,
`settings/Panel.lua:25`, `settings/Slash.lua:24`). Their tasks say so explicitly.

**`NS.version` is not universal.** Check what the addon's own constant is called before writing
`NS.Version` — it is `NS.version` in most, `NS.VERSION` in KickCD, and absent in some. Use what is
there; do not invent one.

---

## Reference test

Every addon's `tests/test_envsetup.lua` is this file, with that repo's test global, its mock's
fixture values, and only the members that addon's seam actually publishes. It is written out here in
full so that no task has to send you to another task to find it.

```lua
-- tests/test_envsetup.lua — the LibKa0s-Env-1.0 seam.
--
-- What is asserted here is THE SEAM, not the library. The library's own suite covers the ladder
-- inside GetAddOnMetadata; a second copy of those cases here is exactly the consumer-side
-- duplication testing-§8 forbids. What only this repo can check is that this addon's helpers answer
-- what its deleted shims answered, and that the shims are actually gone.

local T = _G.<XX>_TEST          -- BL_TEST, LH_TEST, … — read tests/run.lua for this repo's name
local NS = T.NS                 -- KCM in ConsumableMaster
local test, assertEqual, assertTrue = T.test, T.assertEqual, T.assertTrue

test("EnvSetup: NS.Meta reads this addon's TOC", function()
  assertEqual(NS.Meta("Version"), "1.2.3")     -- the mock's fixture value; read tests/wow_mock.lua
end)

test("EnvSetup: NS.Version answers the TOC version", function()
  assertEqual(NS.Version(), "1.2.3")
end)

test("EnvSetup: NS.Version falls back to this addon's own constant", function()
  -- The fallback lives at the call site rather than in the library, so it is the seam's job to
  -- prove it still works. Reached by removing both readers, which is what a client that cannot
  -- answer looks like.
  local savedC, savedG = mocks.C_AddOns, mocks.GetAddOnMetadata
  mocks.C_AddOns, mocks.GetAddOnMetadata = nil, nil
  local v = NS.Version()
  mocks.C_AddOns, mocks.GetAddOnMetadata = savedC, savedG
  assertTrue(v ~= nil and v ~= "", "a version string, never nil — it goes straight into a banner")
end)

test("EnvSetup: the deleted shims are gone from Compat", function()
  -- A seam that leaves the old copy in place is a second answer nobody removed, and the next caller
  -- reaches for whichever one autocomplete offers first.
  assertEqual(NS.Compat.GetAddOnMetadata, nil)
end)
```

Two members are added **only where the addon uses them** — BankLedger and LootHistory are the only
two that stamp a zone or a map id:

```lua
test("EnvSetup: NS.Zone answers two strings", function()
  local zone, sub = NS.Zone()
  assertTrue(type(zone) == "string" and type(sub) == "string",
    "both are ALWAYS strings — storage and the zone filter bucket \"\" with nil deliberately")
end)

test("EnvSetup: NS.PlayerMapID answers the map id", function()
  assertEqual(NS.PlayerMapID(), 2112)          -- the mock's fixture value
end)
```

Before writing any of it, read this repo's fixture values rather than trusting the ones above:

```sh
cd <addon> && grep -n "Version\|GetBestMapForUnit\|__context.zone\|_TEST" tests/wow_mock.lua tests/run.lua | head
```

---

### Task 1: BankLedger — the reference adoption

**Files:**
- Create: `BankLedger/core/EnvSetup.lua`
- Modify: `BankLedger/BankLedger.toc` (after `core\Compat.lua`)
- Modify: `BankLedger/core/Compat.lua` — delete `GetAddOnMetadata` (`:13`), `GetPlayerMapID`
  (`:25`), `GetZone` (`:32`)
- Modify: `BankLedger/settings/Slash.lua:105-106`
- Modify: `BankLedger/modules/Ledger.lua:445, :457`
- Test: `BankLedger/tests/test_envsetup.lua` (new), and any existing case referencing the deleted
  shims

**Interfaces:**
- Consumes: `Env.GetAddOnMetadata`, `Env.Version`, `Env.GetPlayerMapID`, `Env.GetZone` from
  `04_PLAN_B` Task 1.
- Produces: `NS.Meta(field)`, `NS.Version()`, `NS.PlayerMapID()`, `NS.Zone()` — the names every
  later task in this plan uses.

- [ ] **Step 1: Write the failing test**

Create `BankLedger/tests/test_envsetup.lua` — this is the **Reference test** above, with all six
cases, `_G.BL_TEST`, and this repo's fixture values:

```lua
-- tests/test_envsetup.lua — the LibKa0s-Env-1.0 seam.
--
-- What is asserted here is THE SEAM, not the library. The library's own suite covers the ladder
-- inside GetAddOnMetadata; duplicating it here would be the consumer-side copy testing-§8 forbids.
-- What only this repo can check is that the addon's helpers answer what the deleted shims answered,
-- and that the addon still works with the library absent.

local T = _G.BL_TEST
local NS = T.NS
local test, assertEqual, assertTrue = T.test, T.assertEqual, T.assertTrue

test("EnvSetup: NS.Meta reads this addon's TOC", function()
  assertEqual(NS.Meta("Version"), "1.2.3")
end)

test("EnvSetup: NS.Version answers the TOC version", function()
  assertEqual(NS.Version(), "1.2.3")
end)

test("EnvSetup: NS.Zone answers two strings", function()
  local zone, sub = NS.Zone()
  assertTrue(type(zone) == "string" and type(sub) == "string",
    "both are ALWAYS strings — storage and the zone filter bucket \"\" with nil deliberately")
end)

test("EnvSetup: NS.PlayerMapID answers the map id", function()
  assertEqual(NS.PlayerMapID(), 2112)
end)

test("EnvSetup: the deleted shims are gone from Compat", function()
  -- A seam that leaves the old copy in place is a second answer nobody removed, and the next
  -- caller reaches for whichever one autocomplete offers.
  assertEqual(NS.Compat.GetAddOnMetadata, nil)
  assertEqual(NS.Compat.GetPlayerMapID, nil)
  assertEqual(NS.Compat.GetZone, nil)
end)
```

Check the mock's TOC fixture and map id first, and use its values rather than these:

```sh
cd BankLedger && grep -n "Version\|GetBestMapForUnit\|__context.zone" tests/wow_mock.lua | head
```

- [ ] **Step 2: Run it to verify it fails**

Add `"test_envsetup"` to the `SUITES` list in `BankLedger/tests/run.lua`, then:

```sh
cd BankLedger && lua tests/run.lua
```

Expected: FAIL — `attempt to call field 'Meta' (a nil value)`.

- [ ] **Step 3: Create the seam**

Create `BankLedger/core/EnvSetup.lua` from the Reference seam above, with all four members
(BankLedger uses metadata, version, map id and zone).

- [ ] **Step 4: Put it in the TOC**

In `BankLedger/BankLedger.toc`, immediately after the `core\Compat.lua` line:

```
# The LibKa0s-Env seam. After Compat, and before every file that reads a version, a zone or a map
# id. Nothing here is resolved at load, so the position is conventional rather than load-bearing.
core\EnvSetup.lua
```

- [ ] **Step 5: Run it again**

```sh
cd BankLedger && lua tests/run.lua
```

Expected: the four positive cases PASS; "the deleted shims are gone from Compat" still FAILS —
`Compat.GetAddOnMetadata` is still there. That is Step 6.

- [ ] **Step 6: Delete the shims and move the call sites**

In `BankLedger/core/Compat.lua`, delete `Compat.GetAddOnMetadata` (`:13`), `Compat.GetPlayerMapID`
(`:25`) and `Compat.GetZone` (`:32`), together with their comment blocks and the now-orphaned
`-- ── World / player ──` heading if nothing else sits under it.

In `BankLedger/settings/Slash.lua`, replace `:105-106`:

```lua
  return NS.Version()
```

In `BankLedger/modules/Ledger.lua:445`:

```lua
  local zone, subzone = NS.Zone()
```

and `:457`:

```lua
    mapID = NS.PlayerMapID(),
```

- [ ] **Step 7: Sweep for anything the grep above missed**

```sh
cd BankLedger && grep -rn "Compat.GetAddOnMetadata\|Compat.GetPlayerMapID\|Compat.GetZone" \
  --include='*.lua' . | grep -v '/libs/'
```

Expected: no hits outside `tests/` (a test asserting the shims are gone is fine and expected).
Any hit inside `tests/` is a case that must be rewritten against the seam or deleted.

- [ ] **Step 8: Run the gate**

```sh
cd BankLedger && lua tests/run.lua && luacheck .
```

Expected: PASS, 0/0.

- [ ] **Step 9: Regenerate the case list and commit**

```sh
cd BankLedger
lua tests/run.lua --list > docs/test-cases.md   # check the file's banner for this repo's exact command
git add core/EnvSetup.lua core/Compat.lua BankLedger.toc settings/Slash.lua modules/Ledger.lua \
        tests/test_envsetup.lua tests/run.lua tests/test_compat.lua docs/test-cases.md
git commit -m "refactor(env): read the TOC, the map and the zone through LibKa0s-Env-1.0

Three shims leave core/Compat.lua for the library. GetAddOnMetadata was written
eleven times across nine addons in four spellings and none of them behaved
differently; GetPlayerMapID and GetZone were byte-identical to LootHistory's.

Compat keeps what is genuinely this addon's: the container and guild-bank
readers. No behaviour change — NS.Zone still answers \"\" and never nil, which
storage and the zone filter both depend on."
```

---

### Task 2: LootHistory

**Files:**
- Create: `LootHistory/core/EnvSetup.lua`
- Modify: `LootHistory/LootHistory.toc` (after `core\Compat.lua`, TOC line 33)
- Modify: `LootHistory/core/Compat.lua` — delete `GetPlayerMapID` (`:10`), `GetZone` (`:112`),
  `GetAddOnMetadata` (`:473`)
- Modify: `LootHistory/settings/Slash.lua:220`
- Modify: `LootHistory/modules/Collector.lua:125, :133, :189, :198`
- Test: `LootHistory/tests/test_envsetup.lua` (new)

**Interfaces:**
- Consumes: `LibKa0s-Env-1.0`.
- Produces: `NS.Meta`, `NS.Version`, `NS.PlayerMapID`, `NS.Zone`.

- [ ] **Step 1: Write the failing test**

Create `LootHistory/tests/test_envsetup.lua` from the **Reference test** above — all six cases,
including `NS.Zone` and `NS.PlayerMapID` — plus one this addon needs and BankLedger does not:

```lua
test("EnvSetup: an absent zone reads as \"\", which storage buckets with nil", function()
  -- core/Database.lua and modules/BrowserTable.lua both say so in comments and both depend on it.
  -- If the seam ever answers nil here, stored rows move between buckets on the next re-render.
  local saved = mocks.GetZoneText
  mocks.GetZoneText = function() return nil end
  local zone = NS.Zone()
  mocks.GetZoneText = saved
  assertEqual(zone, "")
end)
```

- [ ] **Step 2: Run it to verify it fails**

Add `"test_envsetup"` to `SUITES` in `LootHistory/tests/run.lua` — placing it beside
`"test_mediasetup"`, since it is the same kind of seam — then:

```sh
cd LootHistory && lua tests/run.lua
```

Expected: FAIL on `NS.Meta` being nil.

- [ ] **Step 3: Create the seam and wire the TOC**

Create `LootHistory/core/EnvSetup.lua` from the Reference seam (all four members). In
`LootHistory.toc`, after `core\Compat.lua`:

```
# The LibKa0s-Env seam. After Compat; nothing here resolves at load.
core\EnvSetup.lua
```

- [ ] **Step 4: Delete the shims and move the call sites**

Delete `Compat.GetPlayerMapID`, `Compat.GetZone` and `Compat.GetAddOnMetadata` from
`core/Compat.lua`.

`settings/Slash.lua:220` becomes:

```lua
    return NS.Version()
```

`modules/Collector.lua:125` and `:189`:

```lua
  local zone, subzone = NS.Zone()
```

`:133`:

```lua
      zone = zone, mapID = NS.PlayerMapID(), subzone = subzone })
```

`:198`:

```lua
    zone = zone, mapID = NS.PlayerMapID(), subzone = subzone,
```

Leave the comments at `core/Database.lua:548` and `modules/BrowserTable.lua:245` in place, but
update the reference they name from `Compat.GetZone` to `NS.Zone` — a comment pointing at a
function that no longer exists is exactly the citation drift the collection's sync-docs pass hunts.

- [ ] **Step 5: Sweep, gate, commit**

```sh
cd LootHistory
grep -rn "Compat.GetAddOnMetadata\|Compat.GetPlayerMapID\|Compat.GetZone" --include='*.lua' . \
  | grep -v '/libs/'
lua tests/run.lua && luacheck .
lua tests/run.lua --list > docs/test-cases.md
git add -A
git commit -m "refactor(env): read the TOC, the map and the zone through LibKa0s-Env-1.0

GetPlayerMapID and GetZone were byte-identical to BankLedger's; GetAddOnMetadata
was one of six identical copies. Compat keeps what is this addon's — the event
hooks, the mail and GUID decoders, the bind and currency cluster.

NS.Zone still answers \"\" and never nil: core/Database.lua and
modules/BrowserTable.lua both bucket \"\" with nil on purpose."
```

---

### Task 3: MultiMeters — the version is read at FILE LOAD

**Files:**
- Create: `MultiMeters/core/EnvSetup.lua`
- Modify: `MultiMeters/MultiMeters.toc` — **before** `core\Namespace.lua`, not merely after
  `core\Compat.lua`
- Modify: `MultiMeters/core/Compat.lua` — delete `GetAddOnMetadata` (`:44`)
- Modify: `MultiMeters/core/Namespace.lua:64`, `core/PerfSetup.lua:100-101`,
  `settings/OptionsSetup.lua:139`, `settings/Slash.lua:56`
- Test: `MultiMeters/tests/test_envsetup.lua` (new)

**Interfaces:**
- Consumes: `LibKa0s-Env-1.0`.
- Produces: `NS.Meta`, `NS.Version`.

MultiMeters reads its version **at file load** in `core/Namespace.lua:64`, so the seam must already
be published when that file runs. `core\Compat.lua` is TOC line 37 and `core\Namespace.lua` is line
42, so "immediately after Compat" satisfies this — but say so on the line, because it is
load-bearing here and conventional everywhere else.

- [ ] **Step 1: Write the failing test**

Create `MultiMeters/tests/test_envsetup.lua` from the **Reference test** above — the four base cases
only. This addon stamps no zone and no map id, so `NS.PlayerMapID` and `NS.Zone` are **not** written
into its seam at all: a member nobody calls is a member nobody tests. Add:

```lua
test("EnvSetup: the version was resolved at load, not deferred", function()
  -- core/Namespace.lua reads it at file scope. If the seam loaded after it, this would be the
  -- addon's hardcoded constant forever and nothing else would say so.
  assertEqual(NS.version, "1.2.3")
end)
```

- [ ] **Step 2: Run it to verify it fails**

```sh
cd MultiMeters && lua tests/run.lua
```

Expected: FAIL on `NS.Meta` nil.

- [ ] **Step 3: Create the seam and wire the TOC**

Create `MultiMeters/core/EnvSetup.lua` from the Reference seam, with **only** `NS.Meta` and
`NS.Version`. In `MultiMeters.toc`, after `core\Compat.lua`:

```
# The LibKa0s-Env seam. LOAD-BEARING POSITION: core\Namespace.lua reads the version at FILE SCOPE,
# so the seam has to be published before it — a seam that loaded later would leave NS.version as
# the hardcoded constant for the life of the session, silently.
core\EnvSetup.lua
```

- [ ] **Step 4: Delete the shim and move the call sites**

Delete `Compat.GetAddOnMetadata` from `core/Compat.lua:44`.

`core/Namespace.lua:64` becomes:

```lua
    local v = NS.Meta("Version")
```

`core/PerfSetup.lua:100-101`:

```lua
    version = NS.Version(),
```

`settings/OptionsSetup.lua:139` and `settings/Slash.lua:56`: replace the
`local get = NS.Compat and NS.Compat.GetAddOnMetadata` ladders with `NS.Meta(...)` / `NS.Version()`
as each site requires. Read each site before editing — `OptionsSetup.lua` wants `Notes` or `Title`,
not `Version`.

Update the three comments that name `core/Compat.lua` as the owner of the fallback
(`core/PerfSetup.lua:97`, `settings/OptionsSetup.lua:137`, `settings/Slash.lua:52`,
`core/Namespace.lua:18`) to name `core/EnvSetup.lua` and the library. A comment naming a function
that no longer exists is citation drift.

- [ ] **Step 5: Sweep, gate, commit**

```sh
cd MultiMeters
grep -rn "Compat.GetAddOnMetadata" --include='*.lua' . | grep -v '/libs/'
lua tests/run.lua && luacheck .
lua tests/run.lua --list > docs/test-cases.md
git add -A
git commit -m "refactor(env): read the TOC through LibKa0s-Env-1.0

One of six identical GetAddOnMetadata copies leaves core/Compat.lua, and the
three call sites that had their own inline ladder stop having one. The seam sits
before core/Namespace.lua because that file resolves the version at file scope."
```

---

### Task 4: KickCD — three inline copies, no shim to delete

**Files:**
- Create: `KickCD/core/EnvSetup.lua`
- Modify: `KickCD/KickCD.toc` (after `core\Compat.lua`, TOC line 35)
- Modify: `KickCD/core/KickCD.lua:116-119`, `core/PerfSetup.lua:84-85`, `settings/Slash.lua:66`
- Test: `KickCD/tests/test_envsetup.lua` (new)

**Interfaces:**
- Consumes: `LibKa0s-Env-1.0`.
- Produces: `NS.Meta`, `NS.Version`.

KickCD's `core/Compat.lua` has **no** `GetAddOnMetadata` — all three of its copies are inlined at
call sites. This is the case the register never saw, and the reason the count is eleven rather than
six.

- [ ] **Step 1: Write the failing test**

Create `KickCD/tests/test_envsetup.lua` from the **Reference test** above — the four base cases,
minus the "deleted shims are gone from Compat" one, since this addon's `Compat` never had the shim.
Add:

```lua
test("EnvSetup: no file inlines its own C_AddOns ladder any more", function()
  -- The three copies this seam replaced were INLINE, which is why no audit of core/Compat.lua ever
  -- found them. This case is the only thing that stops a fourth appearing.
  local hits = 0
  for _, path in ipairs({ "core/KickCD.lua", "core/PerfSetup.lua", "settings/Slash.lua" }) do
    local f = io.open(path)
    local body = f:read("*a"); f:close()
    local _, n = body:gsub("C_AddOns%s*and%s*C_AddOns%.GetAddOnMetadata", "")
    hits = hits + n
  end
  assertEqual(hits, 0, "the ladder belongs in core/EnvSetup.lua and nowhere else")
end)
```

- [ ] **Step 2: Run it to verify it fails**

```sh
cd KickCD && lua tests/run.lua
```

Expected: FAIL on `NS.Meta` nil, and the inline-ladder case reporting 3.

- [ ] **Step 3: Create the seam and wire the TOC**

Create `KickCD/core/EnvSetup.lua` from the Reference seam with `NS.Meta` and `NS.Version` only.
**KickCD's version constant is `NS.VERSION`, not `NS.version`** — write the fallback accordingly.

In `KickCD.toc`, after `core\Compat.lua`:

```
# The LibKa0s-Env seam. After Compat; nothing here resolves at load.
core\EnvSetup.lua
```

- [ ] **Step 4: Replace the three inline ladders**

`core/KickCD.lua:116-119` — replace the comment about the deprecated global and the `local get =`
ladder with a call to `NS.Meta`. `core/PerfSetup.lua:84-85` becomes `version = NS.Version(),`.
`settings/Slash.lua:66` likewise.

- [ ] **Step 5: Sweep, gate, commit**

```sh
cd KickCD
grep -rn "GetAddOnMetadata" --include='*.lua' . | grep -v '/libs/' | grep -v '/tests/'
lua tests/run.lua && luacheck .
lua tests/run.lua --list > docs/test-cases.md
git add -A
git commit -m "refactor(env): read the TOC through LibKa0s-Env-1.0

Three inline C_AddOns ladders, none of them in core/Compat.lua — which is why an
audit of the shim files counted six copies across the collection when there were
eleven. A test now fails if a fourth appears."
```

---

### Task 5: ConsumableMaster — two inline copies

**Files:**
- Create: `ConsumableMaster/core/EnvSetup.lua`
- Modify: `ConsumableMaster/ConsumableMaster.toc` (after `core\Compat.lua`, TOC line 72)
- Modify: `ConsumableMaster/settings/Slash.lua:38`, `settings/Panel.lua:662-666`
- Test: `ConsumableMaster/tests/test_envsetup.lua` (new)

**Interfaces:**
- Consumes: `LibKa0s-Env-1.0`.
- Produces: `KCM.Meta`, `KCM.Version` — **this addon's namespace local is `KCM`**, not `NS`
  (`core/Bus.lua` shows the convention). Match the file you are editing.

`settings/Panel.lua:663` hardcodes the string `"ConsumableMaster"` rather than using `addonName`.
The seam fixes that for free — it passes the first vararg — and that is worth a line in the commit
message, because a hardcoded folder name is one rename away from silently answering nil.

- [ ] **Step 1: Write the failing test**

Create `ConsumableMaster/tests/test_envsetup.lua` from the **Reference test** above — the four base
cases, hung on `KCM` rather than `NS`, and minus the "deleted shims are gone" one, since this
addon's `Compat` never had the shim. Add:

```lua
test("EnvSetup: Notes comes through the seam, not a hardcoded folder name", function()
  assertEqual(KCM.Meta("Notes"), "A fixture.")
end)
```

- [ ] **Step 2: Run it to verify it fails**

```sh
cd ConsumableMaster && lua tests/run.lua
```

- [ ] **Step 3: Create the seam and wire the TOC**

Create `ConsumableMaster/core/EnvSetup.lua` from the Reference seam with `Meta` and `Version` only,
hung on `KCM`. In the TOC, after `core\Compat.lua`.

- [ ] **Step 4: Replace the two inline ladders**

`settings/Slash.lua:38` → `KCM.Version()`. `settings/Panel.lua:662-666` → `KCM.Meta("Notes") or ""`.

- [ ] **Step 5: Sweep, gate, commit**

```sh
cd ConsumableMaster
grep -rn "GetAddOnMetadata" --include='*.lua' . | grep -v '/libs/' | grep -v '/tests/'
lua tests/run.lua && luacheck .
lua tests/run.lua --list > docs/test-cases.md
git add -A
git commit -m "refactor(env): read the TOC through LibKa0s-Env-1.0

Two inline C_AddOns ladders, one of them naming the addon folder as a hardcoded
string — a rename away from answering nil with nothing to say so. The seam passes
the first vararg instead."
```

---

### Task 6: WhatGroup — two inline copies

**Files:**
- Create: `WhatGroup/core/EnvSetup.lua`
- Modify: `WhatGroup/WhatGroup.toc` (after `core\Compat.lua`, TOC line 37)
- Modify: `WhatGroup/settings/Slash.lua:28-29`, `settings/Panel.lua:127`
- Test: `WhatGroup/tests/test_envsetup.lua` (new)

**Interfaces:**
- Consumes: `LibKa0s-Env-1.0`.
- Produces: `NS.Meta`, `NS.Version`.

- [ ] **Step 1: Write the failing test**

Create `WhatGroup/tests/test_envsetup.lua` from the **Reference test** above (the four base cases;
no `NS.Zone` or `NS.PlayerMapID` — this addon stamps neither), plus the inline-ladder scan, which is
what this addon actually needs since both its copies were inline:

```lua
test("EnvSetup: no file inlines its own C_AddOns ladder any more", function()
  local hits = 0
  for _, path in ipairs({ "settings/Slash.lua", "settings/Panel.lua" }) do
    local f = io.open(path)
    local body = f:read("*a"); f:close()
    local _, n = body:gsub("C_AddOns%s*and%s*C_AddOns%.GetAddOnMetadata", "")
    hits = hits + n
  end
  assertEqual(hits, 0, "the ladder belongs in core/EnvSetup.lua and nowhere else")
end)
```

- [ ] **Step 2: Run it to verify it fails**

```sh
cd WhatGroup && lua tests/run.lua
```

- [ ] **Step 3: Create the seam and wire the TOC** — Reference seam, `Meta` and `Version` only.

- [ ] **Step 4: Replace both ladders** — `settings/Slash.lua:28-29` → `NS.Version()`;
  `settings/Panel.lua:127` → `NS.Meta(...)` for whichever field that site reads.

- [ ] **Step 5: Sweep, gate, commit**

```sh
cd WhatGroup
grep -rn "GetAddOnMetadata" --include='*.lua' . | grep -v '/libs/' | grep -v '/tests/'
lua tests/run.lua && luacheck .
lua tests/run.lua --list > docs/test-cases.md
git add -A
git commit -m "refactor(env): read the TOC through LibKa0s-Env-1.0"
```

---

### Task 7: PrettyChat — three FILE-LOAD reads

**Files:**
- Create: `PrettyChat/core/EnvSetup.lua`
- Modify: `PrettyChat/PrettyChat.toc` — after `core\Compat.lua` (line 28) and therefore before
  `core\Namespace.lua` (line 33); this ordering is **load-bearing**
- Modify: `PrettyChat/core/Compat.lua` — delete `GetAddOnMetadata` (`:11`)
- Modify: `PrettyChat/core/Namespace.lua:7`, `settings/Panel.lua:25`, `settings/Slash.lua:24`
- Test: `PrettyChat/tests/test_envsetup.lua` (new)

**Interfaces:**
- Consumes: `LibKa0s-Env-1.0`.
- Produces: `NS.Meta`, `NS.Version`.

All three of this addon's call sites read at **file scope**, not inside a function:
`NS.version = (…) or "1.4.0"` at `core/Namespace.lua:7`, `local TOC_NOTES = …` at
`settings/Panel.lua:25`, `local VERSION = …` at `settings/Slash.lua:24`. The seam must be published
before every one of them.

- [ ] **Step 1: Write the failing test**

Create `PrettyChat/tests/test_envsetup.lua` from the **Reference test** above — all four base cases
(this addon's `Compat` did carry the shim). Add:

```lua
test("EnvSetup: every file-scope read resolved through the seam", function()
  -- Three call sites read at FILE SCOPE. A seam published after any of them would leave that one
  -- on its hardcoded fallback for the whole session, and nothing would raise.
  assertEqual(NS.version, "1.2.3")
end)
```

- [ ] **Step 2: Run it to verify it fails**

```sh
cd PrettyChat && lua tests/run.lua
```

- [ ] **Step 3: Create the seam and wire the TOC**

Reference seam, `Meta` and `Version` only. In `PrettyChat.toc`, after `core\Compat.lua`:

```
# The LibKa0s-Env seam. LOAD-BEARING POSITION: core\Namespace.lua, settings\Panel.lua and
# settings\Slash.lua all read the TOC at FILE SCOPE, so the seam has to exist before them. A seam
# published later leaves each of those on its hardcoded fallback, silently.
core\EnvSetup.lua
```

- [ ] **Step 4: Delete the shim and move the three reads**

Delete `Compat.GetAddOnMetadata` from `core/Compat.lua:11` — after which that file is ~11 lines and
worth a look: if nothing is left in it, delete the file and its TOC line rather than shipping an
empty shim. Check first:

```sh
cd PrettyChat && grep -c "^function Compat" core/Compat.lua
```

`core/Namespace.lua:7` → `NS.version = NS.Meta("Version") or "1.4.0"`.
`settings/Panel.lua:25` → `local TOC_NOTES = NS.Meta("Notes") or ""`.
`settings/Slash.lua:24` → `local VERSION = NS.Version()`.

- [ ] **Step 5: Sweep, gate, commit**

```sh
cd PrettyChat
grep -rn "Compat.GetAddOnMetadata" --include='*.lua' . | grep -v '/libs/'
lua tests/run.lua && luacheck .
lua tests/run.lua --list > docs/test-cases.md
git add -A
git commit -m "refactor(env): read the TOC through LibKa0s-Env-1.0

All three call sites read at file scope, so the seam sits ahead of them in the
TOC and the line says why."
```

---

### Task 8: AbsorbTracker

**Files:**
- Create: `AbsorbTracker/core/EnvSetup.lua`
- Modify: `AbsorbTracker/AbsorbTracker.toc` (after `core\Compat.lua`, TOC line 36)
- Modify: `AbsorbTracker/core/Compat.lua` — delete `GetAddOnMetadata` (`:12`)
- Modify: `AbsorbTracker/settings/About.lua:23`, `settings/Slash.lua:109`
- Test: `AbsorbTracker/tests/test_envsetup.lua` (new)

**Interfaces:**
- Consumes: `LibKa0s-Env-1.0`.
- Produces: `NS.Meta`, `NS.Version`.

`settings/About.lua:23` wraps the shim in a local helper that takes `field`; that helper becomes
`NS.Meta` and the wrapper goes away.

- [ ] **Step 1: Write the failing test** — metadata and version cases, plus the
  "deleted shim is gone from Compat" case from Task 1.

- [ ] **Step 2: Run it to verify it fails**

```sh
cd AbsorbTracker && lua tests/run.lua
```

- [ ] **Step 3: Create the seam and wire the TOC** — Reference seam, `Meta` and `Version` only.

- [ ] **Step 4: Delete the shim and move both call sites**

`settings/About.lua:23` → the local wrapper is deleted and its callers read `NS.Meta(field)`.
`settings/Slash.lua:109` → `NS.Version()`.

**AbsorbTracker's `core/Compat.lua` is 20 lines and `GetAddOnMetadata` is most of it.** After the
deletion, check whether anything is left; if not, delete the file and its TOC line. An empty shim
file is a place for the next shim to land without anyone asking whether it should.

- [ ] **Step 5: Sweep, gate, commit**

```sh
cd AbsorbTracker
grep -rn "Compat.GetAddOnMetadata" --include='*.lua' . | grep -v '/libs/'
lua tests/run.lua && luacheck .
lua tests/run.lua --list > docs/test-cases.md
git add -A
git commit -m "refactor(env): read the TOC through LibKa0s-Env-1.0"
```

---

### Task 9: PanelMaster

**Files:**
- Create: `PanelMaster/core/EnvSetup.lua`
- Modify: `PanelMaster/PanelMaster.toc` (after `core\Compat.lua`, TOC line 37)
- Modify: `PanelMaster/core/Compat.lua` — delete `GetAddOnMetadata` (`:13`)
- Modify: `PanelMaster/settings/Slash.lua:32-33`
- Test: `PanelMaster/tests/test_envsetup.lua` (new)

**Interfaces:**
- Consumes: `LibKa0s-Env-1.0`.
- Produces: `NS.Meta`, `NS.Version`.

- [ ] **Step 1: Write the failing test**

Create `PanelMaster/tests/test_envsetup.lua` from the **Reference test** above — the four base
cases, no `NS.Zone` and no `NS.PlayerMapID`.

- [ ] **Step 2: Run it to verify it fails**

```sh
cd PanelMaster && lua tests/run.lua
```

- [ ] **Step 3: Create the seam and wire the TOC** — Reference seam, `Meta` and `Version` only.

- [ ] **Step 4: Delete the shim and move the call site** — `settings/Slash.lua:32-33` →
  `NS.Version()`.

- [ ] **Step 5: Sweep, gate, commit**

```sh
cd PanelMaster
grep -rn "Compat.GetAddOnMetadata" --include='*.lua' . | grep -v '/libs/'
lua tests/run.lua && luacheck .
lua tests/run.lua --list > docs/test-cases.md
git add -A
git commit -m "refactor(env): read the TOC through LibKa0s-Env-1.0"
```

---

### Task 10: Collection-wide verification

- [ ] **Step 1: No copy survives anywhere**

```sh
cd /path/to/GIT
for a in AbsorbTracker BankLedger ConsumableMaster KickCD LootHistory MultiMeters PanelMaster PrettyChat WhatGroup; do
  echo "### $a"
  grep -rn "GetAddOnMetadata\|GetBestMapForUnit\|GetZoneText" --include='*.lua' $a \
    | grep -v '/libs/' | grep -v '/tests/' | grep -v 'core/EnvSetup.lua'
done
```

Expected: **no output**. Every hit is either a copy that was missed or a legitimate use that must be
named in this plan and is not.

- [ ] **Step 2: Every addon still green**

```sh
for a in AbsorbTracker BankLedger ConsumableMaster KickCD LootHistory MultiMeters PanelMaster PrettyChat WhatGroup; do
  ( cd $a && echo "### $a" && lua tests/run.lua >/dev/null && luacheck . >/dev/null && echo green ) || echo "FAILED: $a"
done
```

- [ ] **Step 3: Update each addon's documentation**

`docs/compat-layer.md` exists in an addon whose `core/Compat.lua` still carries addon-specific
shims (`documentation-§3`, Tier 2). Where a `Compat.lua` was deleted outright (possibly
AbsorbTracker, possibly PrettyChat), the doc and its `## Documentation map` row go with it. Where it
survived, the doc must stop listing the three functions that left. Run each addon's
`/wow-addon:sync-docs` rather than editing by hand.
