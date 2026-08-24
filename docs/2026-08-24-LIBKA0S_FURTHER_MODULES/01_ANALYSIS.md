# 01 — Analysis: which further modules move into LibKa0s

**For [LibKa0s #2](https://github.com/tusharsaxena/LibKa0s/issues/2) — "Decide which further modules
move into LibKa0s".**

Produced 2026-08-24. **Analysis only — nothing here has been executed.** No module was extracted, no
addon was edited, no issue was opened or relabelled, and the register on #2 is unchanged. Every
count, hash and line reference below was recomputed from the working trees of the eleven addon repos
and `LibKa0s` as they stand today, not copied from the issue body or from any earlier write-up.

---

## The short version

The register asks one question — *is the duplicated code actually identical in shape, or only
similar?* — and it has been answered per candidate. Sweeping every `core/Compat.lua` and every
export surface in the collection produces a different ranking than the issue currently carries:

> **The two candidates the register names as live are the two weakest. The strongest candidate is
> not in the register at all, and it carries a live defect that a shared module would have
> prevented.**

Specifically:

1. **The `Env` cluster** (`GetAddOnMetadata` / `GetPlayerMapID` / `GetZone`) is the cheapest, safest
   extraction in the collection and the register lists it as a footnote to `Compat`. Eleven call
   sites, six copies of one eight-line function, four spellings, zero behavioural difference.
2. **The copy-paste window is on its fourth copy, not its third.** BankLedger has one, nobody
   recorded it, and MultiMeters' source comment — the comment the register was written to
   substantiate — says "the third in the collection" and is wrong.
3. **The widget pool is a candidate the register does not mention, and it has already cost
   something.** LootHistory's chart pool never returns released widgets to the free list. It is a
   pool that only ever allocates. BankLedger's copy of the same eleven lines is correct.
4. **The `Item` cluster's case has weakened, not strengthened.** The bug that justified it is fixed,
   and the two addons have since adopted *deliberately opposite* policies for the uncached item.
   The merged resolver the register proposes would silently overturn one of them.
5. **The message bus should be declined and struck from the register.** Its entire shared surface is
   six lines wrapping `AceEvent:Embed`. Everything else in those files is a per-addon message
   catalog, which by definition cannot be shared.

---

## 0. The register's own facts are stale

Before the candidates, the state the issue describes is out of date in ways that change the
arithmetic:

| The issue body says | On disk today |
|---|---|
| "five LibStub majors across eight files as of v1.8.0" | **seven majors across ten files, v1.13.0** — `Media-1.0` (minor 3) and `Widgets-1.0` (minor 5) shipped since |
| `Core` 5, `DebugLog` 8, `Slash` 7, `Options` 7, `OptionsWidgets` 7, `OptionsScroll` 3, `Perf` 7, `PerfPanel` 3 | `Core` **6**, `DebugLog` **10**, `Slash` 7, `Options` **8**, `OptionsWidgets` 7, `OptionsScroll` 3, `Perf` 7, `PerfPanel` **4** |
| "Seven addons vendor it: AbsorbTracker, BankLedger, ConsumableMaster, KickCD, LootHistory, PanelMaster, WhatGroup" | **Nine** — MultiMeters and PrettyChat vendor it too. Only BuffTextNotifications and WhoGotLoots do not |
| copy window: "there are three" | **four** — the register misses `BankLedger/modules/Export.lua:231` |
| six functions byte-identical across BankLedger ∩ LootHistory | **five.** `ItemNameQuality` diverged (see §4) |

`WowAddonStandards`' own `open-evolutions.md:13` is stale in the same direction — "six majors across
nine files" — and it names two candidates #2 does not: **the Schema runtime and the object pool**.
The pool turns out to matter (§3).

---

## 1. The `Env` cluster — extract first

The register files this under `Compat` as "separately an `Env`/`Zone` cluster". On the evidence it is
the single best-value item on the list.

**`Compat.GetAddOnMetadata` exists six times**, in AbsorbTracker, BankLedger, LootHistory,
MultiMeters, PanelMaster and PrettyChat. Three of the six are byte-identical (BankLedger:13,
LootHistory:473, PanelMaster:13, hash `db2001bb`). The other three differ **only** in cosmetics:

| Copy | Difference from the identical three |
|---|---|
| AbsorbTracker:12 | 2-space indent instead of… 2-space indent; parameter `field`. Identical logic |
| PrettyChat:11 | 4-space indent, parameter renamed `key` |
| MultiMeters:44 | 4-space indent, every global reached through `_G.` |

Every one of them is the same six-line ladder: try `C_AddOns.GetAddOnMetadata`, fall back to the
deprecated bare global, return nil. There is no addon-specific behaviour to descriptor-ise, and no
plausible future in which one addon needs a different answer.

**And the duplication is worse than the six copies suggest**, because four addons skip `Compat`
entirely and inline the same ladder at the call site:

- `ConsumableMaster/settings/Panel.lua:662-666`
- `ConsumableMaster/settings/Slash.lua:38`
- `KickCD/core/KickCD.lua:119`, `KickCD/core/PerfSetup.lua:84-85`, `KickCD/settings/Slash.lua:66`

That is **eleven implementations of one function**, and the overwhelming majority of callers want
exactly one thing from it — the addon's own `Version` string, for the About page, the slash banner
and the perf descriptor.

`GetPlayerMapID` (BankLedger:25, LootHistory:10) and `GetZone` (BankLedger:32, LootHistory:112) are
**byte-identical pairs**, called from `BankLedger/modules/Ledger.lua:445,457` and
`LootHistory/modules/Collector.lua:125,133,189,198` to stamp a capture with where it happened.

**Recommendation: extract as `LibKa0s-Env-1.0`.** Roughly 40 lines of library covering
`GetAddOnMetadata`, `Version(addonName)` as the named convenience the eleven call sites actually
want, `GetPlayerMapID` and `GetZone`. No descriptor, no state, no frames, no art — which also makes
it the easiest module in the library to test headlessly. Nine consumers on day one.

The one judgement to make deliberately: **`Version` should be a named function, not just a
`GetAddOnMetadata` passthrough.** Nine addons currently spell "my version, or a fallback" nine
different ways (`or NS.version or "?"`, `or NS.VERSION`, `or ""`), and the passthrough would preserve
that spread.

---

## 2. The copy-paste window — four copies, and the record is wrong about it

There is no file I/O in WoW, so every "copy this out" surface ends in a frame holding a selectable
multi-line `EditBox`. The register says there are three. There are four:

| # | Where | Code lines in the builder | Named frame |
|---|---|---|---|
| 1 | `LibKa0s/LibKa0s/DebugLog.lua:545` | 35 | `<Addon>DebugCopyWindow` |
| 2 | `LootHistory/modules/Export.lua:319` | 46 | `LootHistoryExportCopyWindow` |
| 3 | **`BankLedger/modules/Export.lua:231`** | 47 | `BankLedgerExportCopyWindow` |
| 4 | `MultiMeters/modules/Export.lua:1010` | 45 | `MultiMetersExportCopyWindow` |

**Copies 2 and 3 are the same file.** Stripping comments and substituting the addon name away, the
two builders are 52 and 51 lines and differ by exactly three things: one `copyFrame.title = t`
assignment BankLedger keeps and LootHistory drops, one line wrapped at 100 columns in LootHistory
and not in BankLedger, and a trailing `end`. Every geometry constant, every strata, every backdrop
alpha, the `UISpecialFrames` registration, the `OnEscapePressed` handler and the load-bearing
`ShowCopy` ordering (width → text → cursor → show → focus → highlight) are character-for-character
the same. Their `ShowCopy` functions are byte-identical.

**The record itself is the finding here.** `MultiMeters/modules/Export.lua:788-792` describes its
frame as "a deliberate local copy of the one in LootHistory and the one in LibKa0s' debug log — the
third in the collection, recorded as a harvest candidate for the library rather than fixed here."
That comment is what the 2026-08-24 register entry was written to substantiate. It is wrong about
the count, because BankLedger's copy predates it and nobody was looking. A register entry that
undercounts by one is exactly how the dropdown got to three before anyone extracted it.

### The two objections the register raises are already answered

The register says two things must be settled first. Both have since been settled *by the library
itself*:

1. **"The art and fonts would have to arrive as parameters, because a vendored copy cannot know
   which addon folder it sits in."** `LibKa0s-Media-1.0` already solved this and the signature is on
   disk: `lib.Icon(addonName, name, vendorPath)`, `lib.Font(addonName, name, vendorPath)`
   (`Media.lua:202,233`). `LibKa0s-Core-1.0` likewise takes the host by name —
   `lib.MakeCloseButton(parent, onClick, addonName)` (`Core.lua:234`) — and `lib.ApplySkin(frame,
   skin)` (`Core.lua:190`) is the skin seam these four frames each re-apply by hand.
2. **"MultiMeters deliberately keeps its own frame so the two can evolve apart (`b2a1440`)."** That
   argument has to be met, not ignored — and MultiMeters' own file has since *reversed* the identical
   argument for the dropdown: `modules/Export.lua:1099-1101` records that the case for a local menu
   "REVERSES what this file used to argue." The evolve-apart claim is also not borne out: the three
   export copies still agree on all four of the values a divergence would show up in (640×420,
   `FULLSCREEN`, `0.06/0.06/0.08/0.95`, 10pt mono).

**Recommendation: extract as a `LibKa0s-Widgets-1.0` addition — `lib.CopyWindow(descriptor)` —
rather than a new major.** Widgets already exists, already owns "a frame the collection kept
re-drawing", and is already vendored by exactly the three addons that need this (BankLedger,
LootHistory, MultiMeters). A new major would need a fourth vendor sweep for nothing. The descriptor
is small and every field is already a per-copy constant: `{ addonName, name, width, height, font,
fontSize, title, skin, anchorTo }`. Minor bump on `Widgets.lua`, no lockstep.

Do **not** fold `DebugLog`'s copy window into it in the same change. It is the smallest of the four,
it lives inside the library already, and it is wired to `escClose`/`applySkin`/`dragBar` internals
that are file-local to `DebugLog.lua`. Converting it is a second, independent step — and one worth
taking only once the shared surface has three consumers proving its shape.

---

## 3. The widget pool — not in the register, and it is already leaking

Neither #2 nor `open-evolutions.md`'s "the object pool" bullet carries evidence. Here it is, and it
is the strongest single argument on this page for extraction.

Four pool implementations across two addons:

| Where | Shape | Correct? |
|---|---|---|
| `BankLedger/modules/LedgerTable.lua:658,798` | inline row pool | yes |
| `LootHistory/modules/BrowserTable.lua:660,799` | inline row pool — **byte-identical to BankLedger's** apart from `wipe()` vs. the reverse-index clear | yes |
| `BankLedger/modules/InsightsWidgets.lua:362-379` | generic `NewPool` / `Acquire` / `ReleaseAll` | yes |
| `LootHistory/modules/Analytics.lua:222-232` | generic `acquire` / `releaseAll` | **no** |

The two generic copies are eleven and eight lines and their `acquire` halves are identical. Their
`releaseAll` halves are not:

```lua
-- BankLedger/modules/InsightsWidgets.lua:372          -- LootHistory/modules/Analytics.lua:229
function W.ReleaseAll(pool)                            local function releaseAll(pool)
  for _, o in ipairs(pool.active) do                     for _, o in ipairs(pool.active) do o:Hide() end
    o:Hide()                                             wipe(pool.active)
    pool.free[#pool.free + 1] = o                      end
  end
  for i = #pool.active, 1, -1 do pool.active[i] = nil end
end
```

**LootHistory's version never puts anything back on `pool.free`.** `acquire` does
`table.remove(pool.free)` against a list that is empty and stays empty, so `factory()` runs on every
single acquisition. The Analytics pane declares **sixteen** pools (`Analytics.lua:629-638`) and
releases them all through this one function (`Analytics.lua:895`); the five factories build real
frames and textures (`makeBar`, `makeStackedBar`, `makeSwatch`, `makeStripBar`, `makeListRow`, at
`:690,719,740,792,827`). Frames are never destroyed in WoW. Every re-render of the Insights charts —
each filter change, each tab switch — allocates a fresh frame per chart element and abandons the
previous set hidden and unreachable for the life of the session.

This is the register's own criterion, satisfied harder than by any other candidate: *the same code,
in two addons, where one learned the lesson and the other didn't* — and here the one that didn't is
paying for it continuously rather than in a single mislabelled row.

**Recommendation: extract as `LibKa0s-Pool-1.0`, and fix LootHistory's leak *first* and
separately.** The fix is a two-line bug fix that should not wait behind a library extraction, and it
should be its own issue on LootHistory with its own severity — this is a performance defect in
shipped code, which outranks every refactor on this page. The extraction that follows is genuinely
tiny (≈25 lines: `New()`, `Acquire(factory)`, `ReleaseAll()`, `Count()`), pure Lua, trivially
testable headlessly, with no frames or art of its own, and it retires four hand-rolled copies.

---

## 4. The `Item` cluster — the case has weakened; extract primitives, not policy

The register's item-module comment (2026-08-06) rests on a measured bug: BankLedger passing a bare
`itemID` where LootHistory passed a link, flattening upgrade-track items to base quality.

**That bug is fixed.** Both surviving call sites now pass the link first:

- `BankLedger/modules/Ledger.lua:423` — `NS.Compat.ItemNameQuality(move.link or id)`
- `BankLedger/modules/Ledger.lua:477` — `NS.Compat.GetItemDetails(move.link or move.itemID)`

and the reasoning is written into the source at `Ledger.lua:420-422` and `:470-473`, naming the
Epic-read-as-Rare failure exactly as the issue comment described it. So the *cost* half of the
argument has been paid off, and what remains is the ordinary duplication argument.

**And the two addons have since diverged on purpose, in the one place the proposed merged resolver
would touch.** For an item the client has not cached:

- **LootHistory guesses**, and says so: `Compat.GetItemInfo` (`core/Compat.lua:169-185`) falls back
  to the name in brackets and to `QualityFromLink`'s `|cff` colour parse.
- **BankLedger refuses**, and says so: `GetItemDetails` returns `nil` outright when the name is
  uncached, and `Ledger.lua:414-419` documents the decision — *"cannot be judged" is not "passes"
  (F-006)* — recording the skip as `"uncached"` and calling `LoadItem` so the next move judges
  properly, rather than admitting a row it can never classify.

Both are defensible; they answer different questions (a browsable capture log vs. a gated ledger).
The register's proposal — *"`GetItemInfo(linkOrID)` — the merged resolver: prefer the link … colour-
parse fallback when uncached"* — would replace BankLedger's documented refusal with a guess. That is
a behaviour change smuggled inside a refactor, and it is the "shared bug surface" the issue's own
decision criterion exists to catch.

**Byte-identical today** (recomputed): `GetAddOnMetadata`, `GetPlayerMapID`, `GetZone`, `QualityLabel`
(`BankLedger:178` / `LootHistory:161`), `LoadItem` (`:211` / `:199`). Five, not six — **`ItemNameQuality`
has drifted**, and the drift is instructive rather than accidental: the bodies are functionally
identical, but BankLedger renamed the parameter `id` → `idOrLink` and wrote six lines of comment
above it explaining that a link must be passed. That rename *is* the scar tissue from the bug.

**Recommendation: extract the primitives, decline the resolver.** A `LibKa0s-Item-1.0` carrying
`QualityLabel(q)`, `LoadItem(id, cb)`, `ItemIDFromLink(link)` and `QualityFromLink(link)` is four
policy-free functions, two of them already byte-identical across both addons and two of them
currently single-addon primitives the *other* addon should have had. Each caller keeps its own
resolver and composes those primitives under its own uncached policy. `GetItemDetails` /
`GetItemInfo` stay in the addons.

This is a smaller module than the register proposes and it should stay smaller until a third addon
grows item handling. `LootHistory`'s bind/currency cluster (`ScanBound`, `BindState`, `BestBound`,
`ItemBindState`, `GetItemExtras`, `Currency*` — eleven functions, `Compat.lua:271-471`) has no
counterpart anywhere in the collection and is not a candidate.

---

## 5. The message bus — decline, and strike it from the register

The register calls this "still open, still duplicated" and notes the placement drift as evidence the
pattern was never pinned down. The placement drift is real — `core/Bus.lua` in AbsorbTracker and
ConsumableMaster, the root file in BankLedger / KickCD / LootHistory / PanelMaster,
`core/Namespace.lua` in MultiMeters, nothing in WhatGroup. But **seven** addons declare a
bus factory, not eight, and reading all seven, **the drift is in where the file sits, not in what it
does, and what it does is almost nothing.**

The entire duplicated surface is:

```lua
NS.bus = NS.bus or {}
AceEvent:Embed(NS.bus)

function NS.NewBusTarget()
  local AceEvent = LibStub and LibStub("AceEvent-3.0", true)
  if not AceEvent then return nil end
  local t = {}
  AceEvent:Embed(t)
  return t
end
```

Three of the seven `NewBusTarget` bodies are byte-identical (`BankLedger/core/BankLedger.lua:20`,
`LootHistory/core/LootHistory.lua:20`, `PanelMaster/core/PanelMaster.lua:20`); the other four differ
only in indentation, the local's name, and whether the `LibStub` lookup is itself nil-guarded
(`MultiMeters/core/Namespace.lua:90`, `KickCD/core/KickCD.lua:46`, and AbsorbTracker's and
ConsumableMaster's, which take `AceEvent` from a file upvalue). Everything else in those files — the
whole of `AbsorbTracker/core/Bus.lua`'s 56 lines and `ConsumableMaster`'s 53 — is the
**message catalog** (`NS.MSG`), which is per-addon by construction and cannot move anywhere, plus
the doc comment explaining anti-pattern #32, which is the standard's job and not the library's.

Extracting this buys seven addons about eight lines each and introduces a LibKa0s major whose whole
content is a two-line wrapper around a function Ace3 already provides. It also costs something real:
`NewBusTarget` currently degrades to `nil` when AceEvent is missing, and routing it through LibKa0s
adds a *second* library that can be absent on the same path.

**Recommendation: decline, and record the decline in the register.** The valuable half of what the
register noticed is the *placement* drift, and that is a documentation-and-layout finding for
`WowAddonStandards` (`architecture-§4` / `layout`), not a library extraction — if the bus belongs in
`core/Bus.lua`, say so upstream and let the audits move four files.

---

## 6. Ranking

| Rank | Candidate | Shape | Consumers | New major? | Verdict |
|---|---|---|---|---|---|
| 1 | **Pool leak fix** (LootHistory) | 2-line bug fix | 1 | no | **Do now, independently.** Shipped perf defect, not a refactor |
| 2 | **`Env`** | ~40 lines, no state | 9 | `LibKa0s-Env-1.0` | **Extract.** Cheapest, widest, zero policy |
| 3 | **`Pool`** | ~25 lines, pure Lua | 2 (+every future table) | `LibKa0s-Pool-1.0` | **Extract**, after the fix lands |
| 4 | **Copy window** | ~50 lines + frames | 3 | no — add to `Widgets-1.0` | **Extract.** Fourth copy; both blockers already answered |
| 5 | **`Item` primitives** | 4 functions | 2 | `LibKa0s-Item-1.0` | **Extract the primitives only.** Leave the resolver and its policy in the addons |
| — | **`Item` merged resolver** | — | — | — | **Decline.** Would overturn BankLedger's documented F-006 refusal |
| — | **Message bus** | 6 lines | 7 | — | **Decline.** The catalog is the file; the shared part is an Ace3 wrapper |
| — | **`Compat` wholesale** | — | — | — | **Already declined** (2026-08-07). Unchanged by this analysis |

The ordering is deliberately *cheapest and least contentious first*. `Env` and `Pool` are pure
functions with no frames, no art and no host descriptor — they are the two that can ship with full
headless coverage and no smoke test, which is what makes them the right way to re-prove the
extraction pipeline before spending it on the copy window.

---

## 7. What this suggests writing back to #2

Analysis only — none of this has been done:

1. **Correct the stale facts in the body** — seven majors / ten files / v1.13.0, nine vendoring
   addons, and the copy-window count of **four**.
2. **Add the two missing candidates** — the widget pool (with the LootHistory leak as its evidence)
   and the `Env` cluster promoted out of the `Compat` bullet into a candidate of its own.
3. **Open a LootHistory issue for the pool leak**, at a severity that reflects a shipped
   unbounded-allocation defect, and do not let it wait behind any extraction.
4. **Correct `MultiMeters/modules/Export.lua:788-792`**, which names itself the third copy and is the
   fourth. The comment asserts a count nobody was checking — the same failure mode the 2026-08-24
   entry was added to fix.
5. **Record the message-bus decline** in the register rather than leaving it listed as live, and
   raise the file-placement drift with `WowAddonStandards` instead.
6. **Refresh `open-evolutions.md:13`** — "six majors across nine files" is two releases behind, and
   its candidate list and #2's have drifted apart.

---

## Appendix — method

- Function-level comparison: every top-level `function` block in all nine `core/Compat.lua` files was
  extracted, whitespace-collapsed, and hashed (124 functions). Identity claims above mean *equal
  hashes*; near-identity claims are backed by a `diff` with the addon name substituted out and
  comment lines stripped, and the surviving differences are quoted in full.
- Copy-window comparison: builders extracted by line range, comments and blank lines stripped before
  counting, then diffed with the addon name removed.
- Call-site counts come from a `grep` across all eleven addon repos excluding `libs/`, `tests/` and
  each addon's own `core/Compat.lua`, so a shim is never counted as its own caller.
- Repos read: AbsorbTracker, BankLedger, BuffTextNotifications, ConsumableMaster, KickCD,
  LootHistory, MultiMeters, PanelMaster, PrettyChat, WhatGroup, WhoGotLoots, LibKa0s,
  WowAddonStandards — all at their working-tree state on 2026-08-24.
- Nothing was written to any repo other than this bundle.
