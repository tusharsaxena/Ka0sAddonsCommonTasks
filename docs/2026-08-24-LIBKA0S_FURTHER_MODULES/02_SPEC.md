# 02 — Spec: three new LibKa0s majors, one Widgets addition, one console cap, one bug fix

**Implements items #1–#5 of [`01_ANALYSIS.md`](01_ANALYSIS.md)'s ranking, for
[LibKa0s #2](https://github.com/tusharsaxena/LibKa0s/issues/2).**

Written 2026-08-24. **Nothing here has been executed.** This is the design the plans in
`03_`–`07_` implement; where the two disagree, this file is wrong and should be corrected rather
than worked around.

---

## Scope

| # | Deliverable | Where it lands | Consumers |
|---|---|---|---|
| A | Fix the chart-pool leak | `LootHistory/modules/Analytics.lua` | LootHistory only |
| B | **`LibKa0s-Env-1.0`** — TOC metadata, version, map id, zone | new `LibKa0s/Env.lua`, minor 1 | 9 addons |
| C | **`LibKa0s-Pool-1.0`** — the free/active widget pool | new `LibKa0s/Pool.lua`, minor 1 | BankLedger, LootHistory |
| D | **`lib.CopyWindow`** — the selectable-EditBox export frame | `LibKa0s/Widgets.lua`, minor 5 → 6 | BankLedger, LootHistory, MultiMeters |
| E | **`LibKa0s-Item-1.0`** — item-identity primitives | new `LibKa0s/Item.lua`, minor 1 | BankLedger, LootHistory |
| F | **`MAX_BUFFER` 500 → 1500** — the console's line cap | `LibKa0s/DebugLog.lua`, minor 10 → 11 | all 9 vendoring addons |

**Out of scope, deliberately** (see `01_ANALYSIS.md` §4 and §5): the merged item resolver
(`GetItemInfo` / `GetItemDetails` stay in the addons with their own uncached policies), the message
bus, and a wholesale `Compat` extraction.

---

## Global constraints

These bind every task in every plan. Values are copied verbatim from the repos as they stand on
2026-08-24.

- **Lua 5.1.** `.luacheckrc` is `std = "lua51"`. No `goto`, no integer division, no `#!`-isms.
- **`luacheck .` must report 0 warnings / 0 errors** in every repo touched, and `lua tests/run.lua`
  must be green. In LibKa0s, `exclude_files = { "tests/", "docs/" }`, so a new library file **is**
  inside the checked set. Any new global an added file reads must be added to `read_globals` in
  `LibKa0s/.luacheckrc` (`C_Map`, `C_Item`, `ITEM_QUALITY0_DESC`… are **not** there today).
- **One LibStub minor per file, bumped on every released change** (`docs/releasing.md` step 2).
  Never a lockstep bump: a file that did not change does not move.
- **A new major is also a new row in `tests/run.lua`'s `MAJORS`** (`docs/releasing.md` step 3), or
  `tests/test_versioning.lua` never checks it.
- **A minor bump is not released until `docs/api/<Major>/version-<minors>-docs.md` exists** —
  `test_versioning.lua` derives the path from live `lib.MODULES` and fails naming any major whose
  document is missing. The suite is red until the document is written.
- **`CHANGELOG.md`'s release block names every file's live minor**, and `test_versioning.lua` fails
  if the block and `lib.MODULES` disagree.
- **The vendored copy is byte-identical to the source** (`library-stack-§7`): `diff -r
  LibKa0s/LibKa0s <consumer>/libs/LibKa0s` must be empty, and the re-vendor lands in the consumer's
  commit together with the `CLAUDE.md` provenance line.
- **Every module gates on Core** with the collection's exact preamble, even where it uses no Core
  member:

  ```lua
  local core = LibStub and LibStub("LibKa0s-Core-1.0", true)
  local NEEDS_CORE = 1
  if not core or (core.MINOR or 0) < NEEDS_CORE then return end   -- no NewLibrary; module absent
  ```

  This is uniformity with a purpose: a host holding a partial or mis-copied payload gets *every*
  module absent rather than a working half, and "is LibKa0s here?" stays one question.
- **A host never assumes the library is present.** Every consumer resolves with the silent flag —
  `LibStub("LibKa0s-X-1.0", true)` — and the seam file degrades to the addon's own behaviour. The
  headless mock's LibStub is strict about the flag: a lookup written without `, true` resolves to
  nil and raises.
- **Retail only.** No game-flavor branching; guard on the presence of the API itself
  (`if C_Map and C_Map.GetBestMapForUnit then`), which is what every existing shim does.
- **No new library dependency.** These modules depend on LibStub and LibKa0s-Core-1.0 and on no
  addon framework — not Ace3, not AceGUI, not LibSharedMedia.

### One release, not four

B, C, D, E and F all land in **one LibKa0s release, v1.14.0**, and therefore in **one re-vendor sweep**
across nine consumers rather than five sweeps. The releasing playbook already supports a
multi-file release — the version block names each file's minor — and the property that matters
(independent adoption) is unaffected: after the sweep, each addon adopts each module on its own
schedule, and an addon that adopts nothing is still correct.

A is not part of that release. It is a bug fix in one addon, it touches no library, and it ships
first.

---

## A — The LootHistory chart-pool leak

**File:** `LootHistory/modules/Analytics.lua:229-232`.

```lua
local function releaseAll(pool)
  for _, o in ipairs(pool.active) do o:Hide() end
  wipe(pool.active)
end
```

`acquire` (`:222`) takes from `pool.free` with `table.remove` and falls back to `factory()`.
`releaseAll` hides the active objects and drops them on the floor: nothing is ever put back on
`pool.free`, so `pool.free` is empty on every call and `factory()` runs every time.

**Blast radius.** `self.pool` is built once in the constructor and holds **35 pools**
(`:628-654`). `Analytics:LayoutCharts` (`:888-896`) releases all 35 at the top of every layout
pass, and the five factories build real frames — `makeBar`, `makeStackedBar`, `makeSwatch`,
`makeStripBar`, `makeListRow` (`:690, :719, :740, :792, :827`). Frames are never destroyed in WoW,
so every re-render of the Insights tab — each filter change, each date-range change, each tab
switch — allocates a fresh frame per chart element and abandons the previous set hidden and
unreachable for the session.

**The fix** is BankLedger's already-correct body (`modules/InsightsWidgets.lua:372-379`):

```lua
local function releaseAll(pool)
  for _, o in ipairs(pool.active) do
    o:Hide()
    pool.free[#pool.free + 1] = o
  end
  wipe(pool.active)
end
```

**Acceptance:** a headless test drives two layout passes over the same stats and asserts the second
pass creates **no** new frames — proven by a counting factory, not by reading the source. This ships
before, and independently of, everything else in this spec.

---

## B — `LibKa0s-Env-1.0`

### Why

Eleven implementations of one six-line function across nine addons, in four spellings, with no
behavioural difference between any of them (`01_ANALYSIS.md` §1). Three copies are byte-identical;
the rest differ in indentation, in the parameter's name, and in whether globals are reached through
`_G.`. Four addons skip `Compat` entirely and inline the ladder at the call site. `GetPlayerMapID`
and `GetZone` are byte-identical pairs across BankLedger and LootHistory.

### Contract

```lua
local Env = LibStub("LibKa0s-Env-1.0", true)
```

| Member | Signature | Returns |
|---|---|---|
| `Env.GetAddOnMetadata` | `(addonName, field)` | the TOC field as a string, or `nil` |
| `Env.Version` | `(addonName, fallback)` | the TOC `Version`, else `fallback`, else `nil` |
| `Env.GetPlayerMapID` | `()` | the player's current UI map id, or `nil` |
| `Env.GetZone` | `()` | `zone, subzone` — **always two strings**, `""` when the API is absent |

**`GetAddOnMetadata`** is the existing ladder, unchanged in behaviour: `C_AddOns.GetAddOnMetadata`
first, the deprecated bare global second, `nil` third.

**`Version` is the point of the module**, not a convenience wrapper. Nine addons currently spell
"my version, or a fallback" nine different ways; `Version(addonName, NS.version)` is one call whose
fallback is still visible at the call site. It exists because the overwhelming majority of the
eleven call sites want exactly this, and a bare metadata passthrough would have preserved the spread.

**`GetZone` returns `""`, never `nil`**, for both values. This is load-bearing rather than
cosmetic: LootHistory's storage and filters bucket `""` with `nil` deliberately and say so at
`core/Database.lua:548` and `modules/BrowserTable.lua:245`. A library that "improved" this to `nil`
would move stored rows between buckets.

**No state, no frames, no descriptor, no host name held anywhere.** Every function is pure with
respect to the library; the addon name is a parameter for the same reason `Media.Icon` takes one —
a vendored copy cannot know which folder it sits in.

### Host seam

Each consumer grows `core/EnvSetup.lua`, on the model of the existing `core/MediaSetup.lua`, placed
in the TOC after `core/Compat.lua` and before any file whose load-time code reads a version. It
publishes `NS.Env`-shaped helpers bound to `addonName` and degrades to the addon's current
behaviour when the library is absent.

Each addon's own `Compat.GetAddOnMetadata` / `GetPlayerMapID` / `GetZone` are **deleted**, and their
call sites move to the seam. Where an addon inlines the ladder at the call site (ConsumableMaster,
KickCD, WhatGroup) the inline copy is deleted too — those are the copies that were invisible to a
`Compat` audit.

---

## C — `LibKa0s-Pool-1.0`

### Why

Four hand-rolled pools across two addons; three correct and near-identical, one leaking (§A).
The two generic copies have identical `acquire` halves and divergent `release` halves, which is the
register's own criterion for extraction met exactly.

### Contract

```lua
local Pool = LibStub("LibKa0s-Pool-1.0", true)
```

| Member | Signature | Behaviour |
|---|---|---|
| `Pool.New` | `()` | a fresh pool: `{ free = {}, active = {} }` |
| `Pool.Acquire` | `(pool, factory)` | pop `free`, else `factory()`; push to `active`; `:Show()`; return it |
| `Pool.ReleaseAll` | `(pool, before)` | for each active object: call `before(o)` if given, `:Hide()`, push back to `free`; then empty `active` |
| `Pool.Counts` | `(pool)` | `free, active` — the two lengths |

**`ReleaseAll`'s `before` hook is what makes one function cover both addons.** BankLedger's
`W.ReleasePanels` (`modules/InsightsWidgets.lua:789-792`) releases each panel's nested `_rows` pool
before releasing the panel itself; with the hook that is
`Pool.ReleaseAll(panelPool, function(p) Pool.ReleaseAll(p._rows) end)` and needs no second library
member.

**`Counts` exists for tests and for a future diagnostic**, and it is the assertion that makes a
recycling failure visible: after one acquire-release cycle, `free` is non-zero. A pool that leaks
answers `0, 0` where a correct one answers `n, 0`.

**The pool is a plain table with two arrays and no metatable**, so a host holding a pool built
before an upgrade keeps working, and the degraded path (no library) is a nine-line local copy rather
than a redesign.

`Acquire` calls `:Show()` on the object; `ReleaseAll` calls `:Hide()`. Both addons rely on that
today and neither has a pooled object that should stay hidden on acquire.

---

## D — `Widgets.CopyWindow`

### Why

There is no file I/O in WoW, so every "copy this out" surface ends in a frame holding a selectable
multi-line `EditBox`. There are four (`01_ANALYSIS.md` §2), and two of them — BankLedger's and
LootHistory's — are the same 52-line file with the addon name substituted. The register's two
stated blockers are already answered on disk: `Media.Icon(addonName, …)` and
`Core.MakeCloseButton(parent, onClick, addonName)` are the parameterization precedent, and
MultiMeters' own file has since reversed the identical "let them evolve apart" argument for the
dropdown (`modules/Export.lua:1099`).

### Why an addition to `Widgets`, not a new major

`LibKa0s-Widgets-1.0` already exists, already owns "a frame this collection kept re-drawing", and is
already vendored by exactly the three consumers this needs — BankLedger, LootHistory, MultiMeters.
A new major would buy a fourth vendor sweep for nothing.

### Contract

```lua
local W = LibStub("LibKa0s-Widgets-1.0", true)
local win = W.CopyWindow(descriptor)   -- nil headlessly (no CreateFrame)
win:Show(text)
```

**Descriptor** — every field is a per-copy constant today, so nothing here is invention:

| Field | Type | Default | Notes |
|---|---|---|---|
| `addonName` | string | **required** | passed to `Core.MakeCloseButton`; the frame's global name is derived from it |
| `name` | string | `addonName .. "CopyWindow"` | the **global** frame name — needed for `UISpecialFrames` |
| `width`, `height` | number | `640`, `420` | BankLedger, LootHistory and MultiMeters all use 640×420 |
| `title` | string | `"Export"` | already localized by the host; the library never localizes |
| `font` | string | — | a **path**, not an LSM name; `SetFont` does not accept a name |
| `fontSize` | number | `10` | |
| `editWidth` | number | `width - 50` | the first-open fallback, before the scroll frame has been laid out |
| `applySkin` | function(frame) | `Core.ApplySkin` | the host's own skin seam |
| `backdrop` | `{r,g,b,a}` | `{0.06, 0.06, 0.08, 0.95}` | denser than the shared skin's 0.92, for the same reason all three copies are |
| `anchorTo` | function() → frame\|nil | `nil` | called on **every** `Show`, so the popup follows a window the user moved |

**Handle:**

| Member | Behaviour |
|---|---|
| `win:Show(text)` | build once on first call, then: width → text → cursor to top → show → focus → highlight, **in that order** |
| `win:Hide()` | hide |
| `win:GetText()` | the `EditBox` contents |
| `win:GetFrame()` | the frame, for a host that needs to reach past the handle |

**The `Show` ordering is load-bearing and is the reason this is worth sharing.** Highlighting before
the frame is shown selects nothing; focusing before the text is set leaves the cursor where the last
export left it. All four existing copies get it right, and the fifth author would have had to
rediscover it.

**Strata is `FULLSCREEN`**, not configurable: the window exists to sit above the `DIALOG`-strata
modal that spawned it, in all three copies, and a host that wants otherwise has a different widget.

**`Esc` closes and clears focus**, and the frame's global name is appended to `UISpecialFrames`
under a `type(UISpecialFrames) == "table"` guard — the table is not guaranteed outside a real
client.

**Returns `nil` when `CreateFrame` is absent**, so the headless suite exercises the descriptor
handling and the host's fallback rather than a frame nobody can drive.

**`DebugLog`'s own copy window is not converted in this change.** It is the smallest of the four, it
lives inside the library already, and it is wired to `escClose` / `applySkin` / `dragBar` locals
that are file-scoped to `DebugLog.lua`. Converting it is an independent step, worth taking only once
the shared surface has three consumers proving its shape.

---

## E — `LibKa0s-Item-1.0`

### Why, and why it is smaller than the register proposes

The bug that justified an item module is **fixed**: both BankLedger call sites pass the link first
(`modules/Ledger.lua:423, :477`) and the reasoning is written into the source. What remains is
ordinary duplication — plus a divergence that must **not** be flattened.

For an item the client has not cached, the two addons now do deliberately opposite things:
LootHistory guesses (name from brackets, quality from the `|cff` colour, `core/Compat.lua:169-185`)
and BankLedger refuses, records the skip as `"uncached"`, and calls `LoadItem` so the next move
judges properly (`modules/Ledger.lua:414-419`, F-006). Both are correct for their addon. The merged
resolver the register proposes would replace BankLedger's documented refusal with a guess — a
behaviour change smuggled inside a refactor.

**So the module carries primitives and no policy.** Each addon keeps its own resolver and composes
these under its own uncached rule.

### Contract

```lua
local Item = LibStub("LibKa0s-Item-1.0", true)
```

| Member | Signature | Returns |
|---|---|---|
| `Item.ItemIDFromLink` | `(link)` | the itemID from a link or itemString, or `nil` |
| `Item.QualityFromLink` | `(link)` | the quality id parsed from the `\|cffRRGGBB` prefix, or `nil` |
| `Item.QualityLabel` | `(q)` | the localized label, falling back to a static English map |
| `Item.LoadItem` | `(id, cb)` | asks the server to cache `id`; fires `cb` once loaded |

Names are **the addons' current names**, unchanged, so each seam is a straight passthrough and the
adoption diff is reviewable line by line.

**`QualityFromLink` and `ItemIDFromLink` are each single-addon today** — LootHistory has the first,
BankLedger the second — and that is an argument *for* the module rather than against it: each addon
is missing a primitive the other already wrote.

**`QualityLabel` matches on the quality *id*, never on a localized string** (`localization-§4`). It
reads `_G["ITEM_QUALITY" .. q .. "_DESC"]` first and falls back to the static English map, which is
also what makes it answer correctly headlessly.

**`QualityFromLink` builds its hex→quality map lazily from `ITEM_QUALITY_COLORS`** on first use, as
LootHistory's does. The map is cached in a file-local; it must be built lazily rather than at load,
because `ITEM_QUALITY_COLORS` is not populated when a library file in `libs/` runs.

### What stays in the addons

- `BankLedger.Compat.GetItemDetails` and `LootHistory.Compat.GetItemInfo` — the resolvers, with
  their opposite uncached policies.
- `ItemNameQuality` in both — it is `C_Item.GetItemInfo` with a two-value return, and its BankLedger
  copy carries six lines of comment that are BankLedger's policy rather than shared knowledge.
- LootHistory's bind and currency cluster (`ScanBound`, `BindState`, `BestBound`, `ItemBindState`,
  `GetItemExtras`, `Currency*` — `core/Compat.lua:271-471`). No counterpart anywhere; not shared,
  not a candidate.

---

---

## F — `MAX_BUFFER`: 500 → 1500

### The decision, and why it is one number

The console keeps the last N lines; the copy window shows `table.concat(D.buffer, "\n")`
(`DebugLog.lua:684`) and caps nothing of its own. **The copy window is a view of the buffer**, so
there is one number to raise and raising it raises both. A second cap — a visible console held at
500 while the buffer holds 1500 — was considered and rejected: the two would then disagree about
how much history exists, and `DebugLog.lua:38-41`'s own comment says the array cap and the message
frame's `SetMaxLines` must move together. They still do.

**1500, not 5000.** Three times the history at a fraction of the ceiling that was floated. The
number that matters is the perf capture: `perf report` prints its summary lines into the console and
`perf dump` writes the entire JSON record as **one** line (`Perf.lua:1097`), so what a player pastes
out of `/<slash> perf finish` is bounded by this cap and silently loses its head when it overflows,
with nothing saying so. 500 was tight for that; 1500 is not, and it is small enough that a
1500-entry Lua array and a 1500-line `ScrollingMessageFrame` remain an unremarkable cost. **No
measurement is claimed** — the cost was not measured at 500 either, and this is a three-fold change
rather than a ten-fold one.

### It stays fixed by the standard, not by the host

`lib.MAX_BUFFER` is **not** a descriptor field today and does not become one. No host can override
it and no host does. A per-addon cap would mean nine numbers to reason about when a player pastes a
log, and the comment at `:38-41` — which is about the cap and the frame moving together — would
have to become an argument about which addon's console is authoritative.

### Ripple

This is a one-line change with a five-place ripple, and every place is a place that asserts or
prints the literal 500:

| Where | What |
|---|---|
| `LibKa0s/LibKa0s/DebugLog.lua:41` | `lib.MAX_BUFFER = 1500`, and `MINOR` 10 → 11 at `:27` |
| `LibKa0s/tests/test_debuglog.lua:92` | the pinned literal — deliberately pinned so a case reading the constant back cannot pass at any value. It moves to 1500 and stays pinned |
| `LibKa0s/docs/api/DebugLog/version-11-docs.md` | new; version 10 → Superseded |
| `ConsumableMaster/tests/test_debuglog.lua:256` | `t.eq(lib.MAX_BUFFER, 500, …)` — and its message names a `MAX_LINES` that predates the library |
| `PrettyChat/tests/test_debuglog.lua:187, :203` | writes 500+ lines and asserts `"1 / 500 lines"` on the status bar |

Plus prose in `AbsorbTracker/docs/ARCHITECTURE.md:64`, `AbsorbTracker/docs/module-map.md:296, :352,
:770, :862` and `WhatGroup/docs/debug.md:94, :133, :148`, each of which states 500 as a fact about
the library.

**The two consumer suites are the reason F ships inside v1.14.0 rather than before it.** They go red
the moment the library file changes and stay red until that consumer is re-vendored — so the cap
change and the sweep must be the same release, which is exactly the sweep B–E already pay for.

### Acceptance

The pinned case reads 1500, the message frame is held to the same number by the same case, the
eviction case still drops the oldest line first, and both consumer suites are green **after** their
re-vendor commit and not before.


## Test strategy

**In LibKa0s**, each new major gets `tests/test_env.lua`, `tests/test_pool.lua`,
`tests/test_item.lua`, and the copy window extends `tests/test_widgets.lua`. All four are registered
in `tests/run.lua`'s `suites` list and exposed through `LK_TEST`.

**The mock stays repo-local.** `C_Map` and `C_Item` go into **`LibKa0s/tests/wow_mock.lua`**, not
into `testkit/mock_base.lua`. The kit's own rule is that it carries an API *every* addon touches;
these are not, and a kit change would force `Kit.VERSION` and a re-vendor of `tests/_kit/` into
every consumer for nothing.

**Every degraded path is tested by absence, not by stubbing** (`testing-§8`): the C_* branch is
reached by setting the mock's `C_Map` / `C_AddOns` / `C_Item` to nil and asserting the fallback,
which is how the existing `GetAddOnMetadata` shim is already tested.

**In each consumer**, the adoption test asserts the seam, not the library: the addon's helper
answers the same thing the deleted shim did, and answers the addon's own fallback when
`LibStub("LibKa0s-Env-1.0", true)` is nil. A consumer **must not** duplicate the library's unit
coverage (`testing-§8`).

---

## Sequencing

```
A  LootHistory pool leak fix ──────────────────────────────► ships alone, first
                                                              (no library involved)

B/C/D/E/F library work on one branch ─► LibKa0s v1.14.0 ──► re-vendor sweep (9 addons)
                                                                  │
                                                                  ├─► Env adoption   × 9
                                                                  ├─► Pool adoption  × 2
                                                                  ├─► Copy window    × 3
                                                                  └─► Item adoption  × 2
```

Adoption order after the sweep is **cheapest and least contentious first** — Env, then Pool, then
Item, then the copy window. Env and Pool are pure functions with no frames and no art, so they carry
full headless coverage and need no smoke test; the copy window needs one in-client check per addon
and is therefore last.

Each addon's adoption is an independent commit, and an addon that has not adopted is still correct.

---

## Explicit non-goals

- No addon's user-visible behaviour changes anywhere in B–E. These are extractions; the two
  behaviour changes in this spec are A, which is a fix, and F, which is a cap the user asked to raise.
- `MAX_BUFFER` does not become a descriptor field. One number, library-wide (§F).
- No `Compat.lua` is deleted. Each thins to the addon-specific shims it was always for.
- No message-bus module (`01_ANALYSIS.md` §5).
- No merged item resolver.
- No conversion of `DebugLog`'s copy window.
- No `testkit/` change, and therefore no `Kit.VERSION` bump and no `tests/_kit/` re-vendor.
