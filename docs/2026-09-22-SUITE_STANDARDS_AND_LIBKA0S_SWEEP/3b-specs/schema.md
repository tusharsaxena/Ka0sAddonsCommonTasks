# Design spec — `LibKa0s-Schema-1.0` (minor 1, targeting LibKa0s v1.55.0)

Status: DESIGN (CP-3 delegated; calls recorded under *Judgement calls*). Read-only survey; nothing
outside this file was written.

Sources read in full: the nine consumer homes named in the task (`AbsorbTracker/settings/Schema.lua`
428 lines, `PartyFrameEnhanced/settings/Schema.lua` 372, `AuraMaster/settings/Schema.lua` 835,
`MultiMeters/settings/Schema_Paths.lua` 972, `BankLedger/settings/Schema.lua` 695,
`LootHistory/settings/Schema.lua` 727, `PanelMaster/settings/Schema.lua` 554,
`PrettyChat/settings/Schema.lua` 810, `WhatGroup/settings/Schema.lua` 795 — 6188 lines, measured with
`wc -l`), plus each repo's `settings/OptionsSetup.lua` / `settings/Slash.lua` descriptor wiring,
AbsorbTracker `core/Data.lua`, the `NS.Util.SplitPath` / `DeepEqual` copies, AuraMaster
`FC.Signature`, `LibKa0s/Lifecycle.lua` + its docs and suite (house template), `OptionsCompose.lua`
`MasterControls`, `OptionsWidgets.lua:995-1025` (row read/write), `Slash.lua:620-727` (descriptor
use), and the standard at v2.63.0 (`library-stack.md` §7, `architecture.md` §5,
`options-ui.md` §1, `debug-logging.md` §10, `slash-commands.md` §3, `open-evolutions.md`) and the
harvest (`02_FINDINGS.md` C1-F11, C2-F03; `06_OUTCOME.md`).

---

## 1. Verdict

**Viable, as a narrower major than the harvest sketched.** Every member below has two or more
consumers with the same semantics, measured at file:line. Two consumers — AuraMaster and
MultiMeters, the two whose path is rooted at a runtime instance and the reason `resolveRoot` was
proposed — **do not adopt the write seam itself** in minor 1: AuraMaster's `row.normalize`, whole-
section writes and carve-outs, and MultiMeters' all-or-nothing `SetByPaths` batch that announces
once, are single-consumer write semantics that `library-stack-§7` bar 2 forbids encoding as flags.
They adopt the path primitives, the registry, the bulk bracket and (AuraMaster) validation. The seam
(`Get` / `Set` / `ApplyDefault`) is adopted by the other seven.

The instance-rooted model is still served: `resolveRoot(parts, instanceId)` and the instance
argument on `Get` / `Set` are required by `architecture-§5` itself ("the helper addresses the
instance, by an argument or by resolved context"), so they are standard-driven surface, not
single-consumer surface, and the suite exercises them on an instance-rooted fixture.

---

## 2. The calling convention, and the write-seam name (C1-F11)

**What v2.63.0 says — measured, not settled.** `architecture.md:133` still reads "MUST route every
write to a schema-row path through one helper: `NS.Schema:Set(path, value)`" (colon-called, on
`NS.Schema`). `slash-commands.md:83` still reads `set = function(path, v) NS.SetByPath(path, v) end,
-- the single write seam`. The harvest refuted C1-F11 *as filed* and recorded a stronger
standard-internal contradiction to be re-filed (`02_FINDINGS.md:154-162`); `06_OUTCOME.md` shows no
promotion touching either line, and `git log` in WowAddonStandards shows v2.63.0 (`957b3c5`) as the
latest. **The contradiction is live in v2.63.0.** Reported under *OPEN* (O-1).

**What the library does regardless, and why it is neutral between the two readings.**

- Instance members are **dot-called closures bound to the instance at `:New`** — `inst.Set(path,
  value, id)`, never `inst:Set(...)`. This is the one technical argument the harvest named
  (`02_FINDINGS.md:201`): the Options and Slash descriptors take their seams **as values**
  (`OptionsWidgets.lua:1024` calls `d.set(row.path, value)`; `Slash.lua:688` calls
  `d.set(row.path, v)`), so a member that needs `self` cannot be handed over as `set = inst.Set`.
  House precedent exists: the Options instance is dot-called (`H.RenderSchema`, `O.MasterControls`,
  `O.RefreshPanel`). `lib:New` itself stays colon-called like every other major's constructor.
- **The library does not choose the host's public name.** A host binds whichever name the standard
  settles on: `NS.SetByPath = inst.Set` (reading B), or a one-line colon wrapper
  `function NS.Schema:Set(p, v, id) return inst.Set(p, v, id) end` (reading A). Both are shown in
  the adoption deltas, and each host keeps the name it has today so no call site moves in the
  adoption commit. The library's own member is `Set`.

---

## 3. Library surface (lib-level)

All four functions are **pure** and hold no per-host state; they are lib-level because a host that
does not adopt the instance (AuraMaster, MultiMeters) still calls them, and because a lib-level
function is what `Kit.publicMembers` / `members-1.json` can gate.

| Member | Signature | Returns | Absent inputs / dependency absent | Consumers today (file:line) |
|---|---|---|---|---|
| `lib.SplitPath` | `(path)` | `parts` — **one** array, memoized per path string, **shared: callers MUST NOT mutate it** | non-string → `tostring(path)` first; empty / all-dots → `{}` (empty segments dropped, pattern `[^%.]+`) | AM `:90-99`, MM `:97-106` (memoized); AT `:129`, PFE `:80`, WG `:291`, BL `core/Util.lua:15`, LH `core/Util.lua:25`, PM `core/Util.lua:7` (fresh each call) |
| `lib.Read` | `(root, pathOrParts, first)` | `value` or `nil` (1 value) | `root` not a table → `nil`; any intermediate not a table → `nil`; `first` defaults to `1`; empty path → `root` is **not** returned, `nil` is | AT `ResolvePath :107-124`, PFE `:63-75`, AM `readFrom :101-109`, MM `:109-116`, BL `S:ReadPath :403-410`, LH `:399-406`, PM `:356-363`, WG `Resolve :288-305` (8) |
| `lib.Write` | `(root, pathOrParts, value, first)` | nothing | `root` not a table → no-op; empty path → no-op; a non-table intermediate is **replaced** by `{}` (all eight copies do this) | AT `SetPath :126-138`, PFE `:77-89`, AM `writeInto :111-120`, MM `:119-127`, BL `:412-421`, LH `:408-417`, PM `:365-374`, WG `Resolve(path,true)+assign :416-418` (8) |
| `lib.SameValue` | `(a, b)` | boolean (1 value) | `a == b` first (so `-0 == 0`, `nil == nil`); either side not a table → `false`; tables compared by content, both directions, recursively; no cycle detection, no metatable (none of the copies has either — C2-F07) | AT `:171-181`, PFE `:183-193`, MM `:585-595`, BL `S.SameValue :464-473`, LH `:449-455`, WG `:439-449`, PM `Util.DeepEqual core/Util.lua:256` (7, byte-equivalent bodies) |
| `lib.STRINGS` | table | — | — | the three refusal texts (§5) |
| `lib:New` | `(descriptor)` | instance | raises `"LibKa0s-Schema-1.0: descriptor.rows must be a table"` when `rows` is not a table; every other field optional (§4) | — |
| `lib.MAJOR`, `lib.MINOR`, `lib.MODULES` | — | — | `MODULES = { Schema = 1 }` | house bookkeeping, not surface |

`pathOrParts`: a string is split through `lib.SplitPath` (memoized); a table is taken as already
split. That lets AuraMaster/MultiMeters keep passing `parts` + `first` (their `resolveRoot` hands
back a first index of 2) and lets the flat hosts pass a path string.

**Allocation.** Two consumers carry a *measured* allocation constraint on the read path:
AbsorbTracker (`:109-116`, `tests/perf.lua` dormant repaint 312 → 840 bytes/iter against a 320
ceiling when the walker used `gmatch`) and PartyFrameEnhanced (`:58-62`, `resolveUnchanged` 88 → 0
bytes/iter). A memoized split allocates once per distinct path and **never again** for that path,
and the read loop is an integer `for` over the cached array — 0 bytes/iter after the first call.
The cache is keyed by the path string, so it is bounded by the distinct paths ever asked for (the
schema's own plus whatever a player types into `/x get`), which is the bound AM and MM already
accept (`AM :86-87`, `MM :84-87`). **Both hosts' perf gates must be re-run at adoption** (§9).

**Deliberately not exported:** a deep copy. `C2-F07` (harvest) refuted promoting deep copy on
frequency alone, and `library-stack-§7` says high frequency plus low semantic content stays inline.
The instance copies internally where copying is part of a semantic (the write seam's aliasing guard,
`Default`), and exports nothing named copy.

---

## 4. The descriptor

| Field | Type | Required | What it is |
|---|---|---|---|
| `rows` | array | **yes** | The host's live schema array, **held by reference, never copied**. `AllRows()` returns this exact table (AuraMaster `:245-247` and both descriptors depend on identity). Rows already in it are indexed at `:New`. |
| `resolveRoot` | `function(parts, instanceId) -> root, first, resolvedId` \| `nil, reason` | no | Where a **stored** row's path lives. `first` is the index of the first segment inside `root` (1 for a flat host, 2 for `container.` / `window.`). `resolvedId` is handed on to `validate`, `onChange` and `announce`. A nil `root` means "nowhere to store this now" and its second value, a string, is the refusal text. Absent: only rows carrying `get`/`set` are readable/writable (PrettyChat's shape). |
| `announce` | `function(row, path, value, resolvedId)` | no | The post-write tail: the bus message, the panel refresh. Called once per successful `Set`, **after** `onChange`, including for `row.set` rows — the host filters on `row.sessionOnly` itself (PFE `:218`, AM `:459`). |
| `debug` | `function(tag, fmt, ...)` | no | The host's debug sink. Absent: the seam logs nothing. |
| `debugEnabled` | `function() -> boolean` | no | Consulted **before** a `[Set]` line is formatted. Absent: always log. Exists because two hosts format through `format` on a seam a colour-picker drag reaches every 50 ms (AT `:193-195`, PFE `:212`), and BL/LH gate the same way (`BL :546`, `LH :541`). |
| `format` | `function(row, value) -> string` | no | Renders a value for the `[Set]` line. The **same function** a host hands the Slash descriptor's `format` (AT `NS.FormatSchemaValue :324`, PFE `:299`, PC `Schema.FormatValue :548`). Absent: the raw value is passed to `debug`'s `%s`. |
| `print` | `function(line)` | no | Used by `Validate` only. Absent: `Validate` still counts, silently. |
| `resetExempt` | set `{ [path] = true }` | no | Rows a **sweep** must not reset (launcher-§3's minimap row). Honored by `ApplyDefault` **only while a bulk bracket is open**, so a named single-row reset still works (BL `:580-589`, LH `:501-512`). |
| `L` | plain table | no | Overrides `lib.STRINGS` by key (Slash's shape and its *L trap* rule). |

Not in the descriptor, on purpose: a `name` (nothing here prints diagnostics about the host), a page
filter (§8), a migration hook (§8).

### Row fields this major reads

It reads **only**: `path`, `default`, `validate`, `onChange`, `get`, `set`, `sessionOnly`, `type`,
`page`, `group`. Every other field is Options' or Slash's (`docs/api/Options/version-23.30.3.7.3-
docs.md` *Row fields the flow engine reads*) and is passed through untouched.

**How it composes with `LibKa0s-Options-1.0` rather than overlapping it.** Options reads and writes a
row that has a `path` **only through the descriptor** and consults `row.get`/`row.set` only on a
**path-less** row (`OptionsWidgets.lua:997-1025`: "a row WITH a path goes through the descriptor
exactly as it always has, whatever other fields a host's schema happens to give it"). This major
gives `row.get`/`row.set` their meaning on a **path** row — "this row's storage is its own closure,
not `resolveRoot`" — which is exactly the behind-the-descriptor half Options leaves to the host. The
two never disagree about a row: Options calls `d.get(path)` → `inst.Get(path)` → `row.get()`.
Path-less rows (Options' `spec.bind` records, W15) are ignored by this major's index and exempt from
its resolution check.

| Row field | Meaning here | Consumers with this meaning |
|---|---|---|
| `path` | the key; rows without one are not indexed | all 9 |
| `default` | what `Default`/`ApplyDefault` restore; **`nil` means no restore** (§7 JC-5) | all 9 |
| `validate(value, resolvedId) -> ok, why` | refuse before storing; a bare boolean return is the `why = nil` case | AM `:680-683` (with id + why), PFE `:203`, MM `:494`, BL `:533`, LH `:518`, PM `:455` |
| `onChange(value, resolvedId)` | the row's reaction, after the store | all 9; `resolvedId` used by AM `:723`, MM `:678` |
| `get()` / `set(value)` on a path row | the row's own storage (session state, another store, an inverted key) | BL `:537-540`/`:564`, LH `:524-538`/`:550`, PM `:461-463`/`:507`, PC every row, AM/MM session rows (`AM :306-308`, `MM :310-316`); AT/PFE/WG hold the same pairs in side registries today (AT `core/Data.lua:54`, PFE `:95-131`, WG `:328-386`) |
| `sessionOnly` | not in any store a profile reset reaches; skipped by resolution and by `CountOffDefault` | all 9 |
| `type`, `page`, `group` | shape checks in `Validate` | AT, PFE, AM, WG check them today |

---

## 5. Instance surface

All members are dot-called closures (§2). "Root absent" = `resolveRoot` returned nil or is absent;
"row absent" = no indexed row at the path.

| Member | Signature | Returns | Root / row / callback absent |
|---|---|---|---|
| `AllRows` | `()` | the descriptor's `rows` table (identity) | — |
| `FindRow` | `(path)` | row or `nil` | non-string → `nil`. **First-registered wins** on a duplicate path (§7 JC-7). |
| `AddRows` | `(rows, at)` | number added | `rows` not a table → `0`. `at` nil or `> #rows + 1` → append; `at` ≥ 1 → insert in order starting at `at`. Re-indexes. |
| `Reindex` | `()` | nothing | For a host that mutated `AllRows()` in place (AuraMaster's `UnregisterSchemaRows :250-270`, a head splice done by hand). |
| `Get` | `(path, instanceId)` | value (1) | row has `get` → `row.get()`; row is `sessionOnly` without `get` → `nil`; otherwise `resolveRoot` → `lib.Read`. **Root absent → `nil`**. A path with no row is still read (AM `:299-301`, MM `:289-291`: `get` is a debugging tool). |
| `Set` | `(path, value, instanceId)` | `true` \| `false, err, why` | row absent → `false, STRINGS.NOT_FOUND:format(path)`, nothing stored, nothing called. `validate` refuses → `false, STRINGS.INVALID:format(path), why`. Root absent (stored row) → `false, reason or STRINGS.NO_ROOT:format(path)` — **after** `validate`, so a bad value is named before a missing root (AM `:664-668`). `announce`/`debug`/`format` absent → that step skipped. |
| `Default` | `(path)` | deep copy of the row's `default`, or `nil` | row absent → `nil` |
| `ApplyDefault` | `(row)` | `Set`'s returns, or `false` | not a table / no `path` / `default == nil` → `false` (nothing written). `resetExempt[path]` while `InBulk()` → `false`. |
| `BulkBegin` | `(act, scope)` | nothing | — (the Options/Slash descriptors' `bulkBegin`) |
| `BulkEnd` | `(act, scope, count, err, info)` | nothing | depth already 0 → no-op (never negative). `count` ignored (§6). |
| `BulkRun` | `(act, scope, fn)` | nothing; re-raises `fn`'s error **unchanged** (`error(err, 0)`) | `fn(info)` sets `info.profileReset = true` to silence the line |
| `BulkAdd` | `(n)` | nothing | outside a bracket → no-op |
| `InBulk` | `()` | boolean | — |
| `CountOffDefault` | `(pred)` | number | counts indexed rows with a `path`, not `sessionOnly`, `pred(row) ~= false` (pred absent = all), whose `Get(path)` is not `SameValue` to `default`. Root absent → `Get` is `nil` → counted iff `default ~= nil`. |
| `ResetCounted` | `(resetFn, pred)` | nothing; re-raises `resetFn`'s error unchanged | sets the pending count to `CountOffDefault(pred)`, runs `resetFn` under `pcall`, clears the pending count on **both** exits |
| `ConsumeResetCount` | `()` | number or `nil` | returns and clears the pending count; **also marks an open bracket profile-reset**, so the bracket emits no second line (WG `:520-525`, `:671-676`) |
| `Validate` | `(spec)` | `errors, resolved, missing` | `print` absent → silent counts; `spec.defaultsRoot` absent → no resolution check (`resolved = missing = 0`) |

`lib.STRINGS`: `NOT_FOUND = "Setting not found: %s"`, `INVALID = "Invalid value for %s"`,
`NO_ROOT = "Setting has nowhere to be stored yet: %s"` (the first two are AM/MM's existing texts,
`AM :712/:682`, `MM :476/:495`; hosts on BL/LH/PM's `"unknown path: "` / `"invalid value"` change
wording — presentation only; `L` restores theirs if wanted).

### The `Set` pipeline (order is the contract)

1. `path` not a string, or no indexed row → refuse `NOT_FOUND`.
2. If the row is stored (no `row.set`, not `sessionOnly`): `root, first, rid = resolveRoot(parts,
   instanceId)`.
3. `validate(value, rid)` → on falsy, refuse `INVALID` with the row's `why`.
4. Stored row with no root → refuse with `resolveRoot`'s reason or `NO_ROOT`.
5. If `InBulk()`: `before = Get(path, instanceId)`.
6. **Store:** `row.set` → `row.set(value)` (the value as given); `sessionOnly` without `set` → nothing;
   else `lib.Write(root, parts, deepcopy(value), first)`.
7. If `InBulk()`: `after = Get(path, instanceId)`; tally `+1` iff `not SameValue(before, after)`.
   Taken **here**, before any host code runs, so a raising `onChange` cannot drop a stored write from
   N (AM `:383-384`).
8. **Log** — unless `InBulk()`: if `debug` and (`debugEnabled` absent or true):
   `debug("Set", "%s = %s", path, format and format(row, value) or value)`.
9. `row.onChange(value, rid)` if present. **Errors propagate** (§7 JC-3).
10. `announce(row, path, value, rid)` if present.
11. `return true`.

### The bulk bracket (debug-logging-§10)

One tally shared across nesting levels; a depth counter; the outermost `BulkEnd` emits
`debug("Set", "%s %s: %d rows%s", act, scope, N, failed and " (stopped by an error)" or "")` unless
any level reported `info.profileReset` (or `ConsumeResetCount` ran while open). `N` is the lib's own
tally of writes whose **read-back** value moved, plus `BulkAdd` contributions — never the libraries'
`count`, which includes rows already at their default (Options O16 / Slash 8 contract; every
consumer ignores it: AT `:217`, PFE `:231`, AM `:402`, MM `:623`, BL `:483`, LH `:470`, PM `:401`,
WG `:510`). The line honours `debugEnabled`. A begun bracket always closes: `BulkRun` pcalls `fn`,
calls `BulkEnd` with the raised value as `err`, then re-raises.

### `Validate(spec)`

`spec = { types = set?, pages = set?, defaultsRoot = function(parts, row) -> root, first ? }`.
`types` defaults to `{ bool, number, string, color }` (the four Options widget types).

Per row, each failure printed once as `|cffff0000schema error|r: row #<i> (<path>): <msg>` and
counted in `errors`: row is not a table; `path` missing/empty **unless** the row carries both `get`
and `set` (an Options bound row); `type` not in `types`; `page` not in `pages` (when given); `group`
not a non-empty string (options-ui-§13); `path` already used by an earlier row (duplicate).
Resolution, for a row with a `path` that is not `sessionOnly`: `root, first = defaultsRoot(parts,
row)`; a nil `root` skips the row; `lib.Read(root, parts, first) ~= nil` → `resolved`, else print
"`path` does not resolve against the defaults" and count `missing`. Return
`errors, resolved, missing` (AT `:376`, PFE `:354` already return exactly this triple; AM/BL/LH/PM
return one count and sum the triple).

---

## 6. What the library deliberately does not own (excluded, with the reason)

| Candidate | Where | Why excluded |
|---|---|---|
| **Migration stamps / runner** | 5 variants (open-evolutions) | Task-scoped out; `library-stack-§7`'s worked rejection. |
| `row.normalize(value, id)` | AM `:685`, `:556-565` | Single consumer (bar 1). Re-check trigger: a second host grows a post-validate rewrite. |
| Whole-section writes, carve-outs (`SECTIONS`, `CARVE_OUTS`) | AM `:364-368`, `:510-518`; MM columns `:393-456` | Host-specific data shapes; each host keeps them in front of its own seam. |
| All-or-nothing batch that announces once (`SetByPaths`) | MM `:773-798` | Single consumer; accommodating it would be a flag on `Set`'s announce step (bar 2). |
| Dry-run write (`CheckWrite` / `prepareWrite`) | AM `:761`, MM `:475` | Its only consumers do not adopt `Set`, so a lib `Check` would mirror a seam neither uses. |
| `noReset` / `noResetReason` | AM `:782-784` | Single consumer; a host wrapper around `ApplyDefault`. |
| `__restoring` flag around a reset | MM `:817-823` | Single consumer. |
| Per-write `old` value to `onChange` | AM `:723` | Single consumer; reading it on every write costs a read per colour-drag frame for everyone. |
| `opts { skipLog, skipRefresh, skipOnChange }` | WG `:451-479` | Single consumer, and each is an escape hatch by definition (bar 2). WG's one caller (`:722-727`) is re-expressed in §9. |
| Row-set dedup in the tally ("once however often written") | MM `:612-618` | Single consumer; MM keeps its seen-set and feeds `BulkAdd(1)`. |
| Page filtering / ordering (`SchemaForPage`, `rowsForPage`) | AT `:76-97`, PFE `:39-54` (group-first-index + `order` sort); AM `:284-293` (`hidden` + `auraTypes`); MM `:842-853` (`hidden`); PC `:782-788` (by category) | Two incompatible orderings (sorted vs declaration order) — a render concern that is the Options descriptor's `rowsForPage`, not the schema runtime's. |
| Value formatting (`FormatSchemaValue`, `Schema.FormatValue`) | AT `:324-328`, PFE `:299-303`, PC `:548-564` | Already `LibKa0s-Slash-1.0`'s `lib.FormatValue` + descriptor `format`. This major takes the host's `format` for its `[Set]` line and exports no formatter, so the two majors compose instead of overlapping. PC's pipe-doubling stays in PC's `format`. |
| Default/agreement check (row `default` equals the defaults tree) | MM `:858-921` | Single consumer, and an inverted row makes the comparison host-specific (MM `checkMinimapRow`). |
| `section` / announce payloads / bus message names | PFE `:165-174`, WG `section` | Host half (what `announce` sends). |
| AceDB defaults builder from the schema | WG `BuildDefaults :596-629` | Single consumer; `options-ui-§1` says profile defaults MUST NOT be read off the schema. |
| Pre-db read fallback to shipped defaults | AT `core/Data.lua:93-96`, PFE `:139-144` | Two consumers, but the other seven answer `nil` pre-db and AM/MM *document* nil; adopting it would make `Get` read a second tree. Kept as a two-line host wrapper around `inst.Get`. |
| Snapshot-and-diff reset count | PM `:426-448` | Counts the same thing `ResetCounted` counts; PM MAY keep it (it is exact where a reset does not land on the default), no member needed. |
| A deep-copy export | C2-F07 | Refuted in the harvest (frequency alone). |

---

## 7. Judgement calls (the disagreements measured, and the reading taken)

Each is a place the consumers disagree. None is resolved by a flag; each is resolved by one reading,
and the consumer on the other side changes in its adoption commit (§9) with a pinned test.

- **JC-1 Seam name / call style.** Dot-called closures; host keeps its public name (§2). O-1.
- **JC-2 Unknown path.** AT (`:190-191` writes via `SetSetting` with no row), PFE (`:209`), WG
  (`RawSet :404-419`) store a write to a path with no row; AM, MM, BL, LH, PM, PC refuse. **Refuse.**
  `architecture-§5` scopes the helper to schema-row paths. The write call sites were grepped (non-
  comment lines): AT 14, PFE 6, WG 7. Each is a literal row path, a descriptor pass-through the
  Slash/Options majors only reach with a row they found, or a path built from a row key
  (`AT core/Units.lua:120` over `Units.APPEARANCE_KEYS`, `AT settings/Slash.lua:277/:287`
  `units.<unit>.enabled`) — the last kind is the one each adoption's suite must exercise, because a
  key missing from the schema would now be refused rather than silently stored.
- **JC-3 A raising `onChange`.** WG alone `pcall`s it and prints (`:469-474`); the other eight let it
  raise. **Propagate** — the Lifecycle precedent ("the error reaches the host's own error handler").
  The value is already stored and the `[Set]` line already written (log-before-react, JC-4), so
  the log never claims less than happened.
- **JC-4 Log before or after `onChange`.** Before: AT, PFE, BL, LH, PM, WG. After: AM, MM, PC.
  **Before**, by majority and because it is the reading under which a raising reaction cannot erase
  the trace of a write that did land. Presentation only (line order in the console).
- **JC-5 `default == nil`.** AT (`:290`), PFE (`:287`), AM (`:785`) skip; PM (`OptionsSetup:182`), PC
  (`:692`), MM (`:822`) write `nil`; BL/LH/WG declare the one row that would have none. **Skip.** The
  standard reads this way: test mode's `false` default is "what lets a reset end it"
  (options-ui-§15, cited at BL `:186-187`, LH `:102-103`), i.e. with no default a reset does not.
  PM and PC declare `debugConsole = false` in their `MasterControls` defaults (they currently rely on
  writing `nil` to close the console on a reset).
- **JC-6 Copy on write.** AM, MM, BL, LH, PM deep-copy a table value on the way into the store; AT,
  PFE, WG store the caller's table. **Copy** (5 of 8 path writers), on the aliasing argument MM
  `:660-663` makes. `row.set` rows get the value as given — every consumer does that.
- **JC-7 Duplicate paths.** Linear `FindRow` returns the first match (AT, BL, LH, PM, WG); the four
  indexed hosts' `reindex` returns the last (PFE, AM, MM, PC). **First wins**, and `Validate` now
  reports a duplicate, which no consumer checks today — so the disagreement becomes unreachable.
- **JC-8 Tally test.** Before-vs-`value` (AT, PFE, WG, BL, LH) vs read-back before-vs-after (PM
  `:459-490`, MM `:600-618`). **Read-back**, because it is right for a closure row that stores a
  transformed value (PC clears to absence; BL/LH/PM's inverted minimap row) and identical for a plain
  row. Paid only inside a bracket.
- **JC-9 `BulkRun` callback.** AT/PFE hand `walk(info)`; AM/MM take `fn()` returning `true`.
  **`fn(info)`**, matching the Options/Slash `bulkEnd(..., info)` contract, so a host reads one shape
  of "was this a profile reset". AM (`ContainerManager.lua:471`, `:502`, degraded reset) and MM
  rewrite `return true` as `info.profileReset = true`.
- **JC-10 Reset-exempt mechanism.** AT/PFE/AM/MM veto at the Options descriptor's `applyDefault`
  wrapper; BL/LH veto inside `ApplyDefault` while a bracket is open. Same property (launcher-§3: a
  sweep never touches the row, a named reset does). **Bracket-scoped `resetExempt`** — every sweep in
  the collection opens a bracket (Options `RestoreDefaults`/`RestoreAllDefaults` since O16, Slash
  `CliResetAll` since 8), and a single `CliReset` does not.
- **JC-11 Core floor.** Schema calls no Core member. **Floor on Core minor 1 anyway**, like
  Lifecycle, so a partial payload is uniformly absent (house convention, library-stack-§7). O-2
  records the alternative.
- **JC-12 `ConsumeResetCount` silences an open bracket.** WG only today, but it is the same rule
  (§10: a profile reset inside a bulk act emits no bulk line) enforced at a second point, and it is
  unobservable in AT/PFE whose brackets already carry `info.profileReset`. Adopted as behavior, not
  surface.
- **JC-13 Validation strictness.** `group` required on every row and duplicate paths reported, for all
  adopters. New for MM/BL/LH/PM/PC. Each adoption re-measures `Validate` to zero before committing.
  BL `:600` still carries the `and row.default == nil` conjunct LH (`:563-568`) and PM (`:520-531`)
  documented as making the check structurally dead; adopting `Validate` removes it, which may
  surface rows BL has never been told about.

---

## 8. Degradation stub

**The problem this major introduces.** Every other LibKa0s major is reached by the panel, the CLI or
a diagnostic. This one is reached by the addon's **feature runtime**: AT's repaint pass reads flat
settings through the seam (`AT :109-116`), PFE's show decision reads `general.includePlayer` per
element per pass (`PFE :58-62`). A member-answering stub that prints "not installed" from `Get`
would leave the addon unable to read its own settings, and a load-completing stub (options-ui-§1)
does not cover per-frame reads.

**Amended in verify round 1: the stub is WRITE-COMPLETING and LOG-SILENT.** The first draft of this
section made `Set`/`ApplyDefault` refuse, argued "by the fall-together property no panel or CLI can
reach `Set`", and turned the bracket into no-ops. That argument was false. `options-ui-§1` asks the
Options stub to keep Reset All real, and `slash-commands-§1` says the host verbs keep working. In
AbsorbTracker the host verbs (`settings/Slash.lua:487`), the Options stub's Reset All
(`settings/OptionsSetup.lua:383`) and the combat re-lock (`core/AbsorbTracker.lua:259`) all write
through `NS.SetByPath`. Measured in the verifier's adopted AbsorbTracker copy, a refusing stub reddened
three library-less tests. In PrettyChat the library-less `Schema.Set('Loot.enabled', false)` was
refused, so `tests/test_libka0s.lua:504-507` passed without testing anything. The stub now completes
everything a player can observe, and nothing that only feeds the debug console. Every adopter's
library-less DebugLog stub discards the line (its `Add` and its debug sink, `Debug` or `NS.Debug`,
are empty functions in all nine adopters' `core/DebugLogSetup.lua`, grep-measured), so the degraded
build has nowhere to show one:

| Member | Stub answer |
|---|---|
| `AllRows`, `AddRows`, `FindRow`, `Reindex` | **Real**: `rows` held by reference, append/insert, linear first-match `FindRow`, `Reindex` no-op. Page files call `AddRows` at file load (options-ui-§1's load-completing half). |
| `Get` | **Real**: `row.get` if present; `nil` for `sessionOnly` without `get`; else the host's `resolveRoot` + a plain walk. |
| `Set` | **Real, without log and tally**: unknown path refused; `validate`; missing root refused; store (`row.set` as given / nothing for bare `sessionOnly` / a copy written at the path); `onChange`; `announce`; `true`. |
| `ApplyDefault` | **Real**: `default == nil` → `false`; `resetExempt` while the depth is > 0 → `false`; else `Set(path, copy(default))`. |
| `Default` | A copy of the row's default. |
| `BulkBegin`/`BulkEnd`/`InBulk` | A depth counter only (the sweep veto reads it). No tally, no line. `BulkAdd` no-op. |
| `BulkRun(act, scope, fn)` | Begin, `pcall(fn, { profileReset = false })`, end, re-raise unchanged. |
| `CountOffDefault` | `0`. `ResetCounted(fn)` runs `fn()`. `ConsumeResetCount` → `nil`. (The count exists only for a debug line.) |
| `Validate` | `0, 0, 0` and one honest line. |

**Lib level.** The stub also stands in for the library table: `SplitPath`, `Read`, `Write`,
`SameValue`, and `New(d)` returning the instance stub, so a host writes
`local SchemaLib = LibStub(...) or HostSchemaStub` and keeps one seam. This answers the verifier's
finding that a full adopter's own callers of `lib.Read`/`lib.Write` (AbsorbTracker
`core/Data.lua:93,96`) had no library-less answer. No `STRINGS`: refusals are in the host's words.

**Reference and cost.** `tests/test_schema.lua`'s `referenceStub` is this stub. It closes over
nothing and runs in a plain-Lua environment, and it is pinned on surface (both levels), on store and
reaction order against a live instance, on the sweep veto and on the primitives. It measures 132
non-blank, non-comment lines, 59 of them the write half. Transplanted into the verifier's adopted
AbsorbTracker copy, it turned `Reset All resets a sessionOnly row ... on both builds` green (640/5,
was 639/6). Its two remaining degraded reds are the two debug-line pins, which re-pin (§11).

Each host pins the stub's **member set** against a live instance (two-table form, instance) and by
name (lib level, ignoring `STRINGS`), and pins one degraded write per writer kind it has.

The stub's read and write walks are host code, which is the shape options-ui-§1 forbids for widget
makers and layout constants. Whether a runtime degradation path is inside that prohibition is not
answered by the standard: O-3 and O-5.

---

## 9. Files to create / edit in LibKa0s

| Path | Action |
|---|---|
| `LibKa0s/Schema.lua` | **Create.** Header comment (why, what it is not); Core floor (`NEEDS_CORE = 1`, return before `NewLibrary`); `MAJOR = "LibKa0s-Schema-1.0"`, `MINOR = 1`; `lib.MODULES.Schema = MINOR`; `STRINGS`; `SplitPath`/`Read`/`Write`/`SameValue`; `New` with the instance of §5. Estimate 450-600 lines — well under the 1500 cap (layout-§1). ASCII-only literals; the em dash only in comments. CRLF on disk (`* text=auto eol=crlf`; confirm with `git ls-files --eol LibKa0s/Schema.lua` → `i/lf w/crlf`). |
| `LibKa0s/LibKa0s.xml` | Add `<Script file="Schema.lua"/>` **after `Lifecycle.lua`** (floors on Core only; nothing floors on it). |
| `tests/majors.lua` | Add `{ major = "LibKa0s-Schema-1.0", files = { "Schema" }, primary = "Schema" }` after the Lifecycle row (XML order). |
| `tests/test_schema.lua` | **Create** (§10). |
| `tests/run.lua` | `schema = mocks.LibStub("LibKa0s-Schema-1.0")` in `LK_TEST`; `"test_schema"` in `suites` after `"test_lifecycle"`. |
| `docs/api/Schema/version-1-docs.md` | **Create**, Lifecycle's shape: header table (Major, `Schema.lua` minor 1, shipped in v1.55.0, Current, confirm-in-game `MODULES → { Schema = 1 }`), what it is / is not, lib surface, descriptor, row fields, instance surface, the `Set` pipeline, the bracket, hard invariants (one per test), worked example, the stub contract (§8), composition with Options/Slash. |
| `docs/api/Schema/members-1.json` | **Generate** with `lua tools/gen-api-members.lua` (never hand-edit): `New`, `Read`, `SameValue`, `SplitPath`, `STRINGS`, `Write`. |
| `docs/api/README.md` | Add the `LibKa0s-Schema-1.0` row to the version-key table. |
| `CHANGELOG.md` | Under `## v1.55.0`: new major, `Schema` minor 1 (the versioning suite asserts every live minor is accounted for). No floor raised on any existing major — not a re-vendor trigger beyond the normal one. |
| `CLAUDE.md` | `:229` documentation-map row gains `Schema`; any inventory count. |
| `README.md` | `:13` and `:69` ("Twelve LibStub majors" → recount against `tests/majors.lua`: thirteen), module list near `:20`, the table near `:78`, `MODULES` list `:207`, re-vendor list `:228`, file tree `:243`. |

**Upstream ripple (WowAddonStandards, not this repo — for the orchestrator):** `library-stack.md` §7
module table and counts ("twelve LibStub majors across eighteen files" → recount: thirteen across
nineteen), `open-evolutions.md:13` (the Schema runtime moves from *candidates* to *shipped, portable
half*), and O-1/O-2/O-3 below.

**Additive only.** No existing file's minor moves; no existing major gains a floor or a member.

---

## 10. Test plan — `tests/test_schema.lua`

Every case builds its state from a **fixture constructor**, never from shared mutable state:

- **F-flat** — `db = { profile = { enabled = true, scale = 1, color = {r=1,g=1,b=1,a=1}, units = { player = { width = 200 } } }, global = { minimap = { hide = false } } }`; rows: bool, number with `validate` + `why`, color table, a nested `units.player.width`, a `sessionOnly` row with `get`/`set` over a local, the inverted minimap row (`get = not hide`, `set = hide = not v`) with `default = true`; `resolveRoot = function() return db.profile, 1 end`; defaults tree mirroring `db`.
- **F-instance** — `members = { [1] = {...}, [2] = {...} }`, `active = 1`; rows `member.width` etc.; `resolveRoot(parts, id)` → `members[id or active], 2, id or active`, or `nil, "no member"` when the id names nothing.
- **F-closure** — PrettyChat-shaped: every row has `get`/`set`, `set` clears to absence when handed the default; no `resolveRoot`.
- **Recorder** — `debug`, `announce`, `print`, `onChange` and `format` spies appending to one ordered log, so order is asserted, not just counts.

**Primitives**
P-1 `SplitPath` returns the same table for the same path (identity), drops empty segments, `tostring`s a number.
P-2 `Read` over a nested path; missing leaf → nil; non-table intermediate → nil; nil root → nil; `first = 2`; parts-array input.
P-3 `Write` creates intermediates; replaces a non-table intermediate; nil root no-op; empty path no-op; `first = 2`.
P-4 `SameValue`: scalars, `-0`/`0`, extra key on either side, `false` vs absent key, nested.
P-5 Allocation: after one warm-up `Read`, 1000 `Read`s of the same path grow `collectgarbage("count")` by < 1 KB (the AT/PFE perf guarantee, pinned upstream).

**Registry**
R-1 `New` raises naming `descriptor.rows`; indexes pre-filled rows; `AllRows()` is the host's table.
R-2 `FindRow` first-wins on a duplicate; non-string → nil; path-less row not indexed.
R-3 `AddRows(rows)` appends; `AddRows(rows, 1)` inserts at head **in order**; `at` beyond the end appends; returns the count.
R-4 Host removes a row from `AllRows()` in place, `Reindex()`, `FindRow` no longer finds it.

**Seam (F-flat unless noted)**
S-1 Unknown path → `false, "Setting not found: x"`; recorder empty; store untouched.
S-2 Happy path: returns `true`; log order is `debug` → `onChange` → `announce`, each once; the stored table is a copy (mutating the argument afterwards leaves the store unchanged).
S-3 `validate` refusal → `false, "Invalid value for p", why`; nothing stored; recorder empty.
S-4 (F-instance) `Set(p, v, 2)` writes member 2 while `active = 1`; `onChange`/`announce` receive `2`; `Get(p, 2)` reads it; `Set(p, v, 9)` → `false, "no member"`, and a bad value to member 9 is refused as INVALID first.
S-5 `row.set` row: called with the argument itself (identity), `resolveRoot` never called; `sessionOnly` row without `set` stores nothing and still fires `onChange`/`announce`.
S-6 Minimap inverted row: `Set(true)` stores `hide = false`; `Get` answers `true`.
S-7 `debugEnabled` false → neither `debug` nor `format` called (the colour-drag guarantee).
S-8 `format` present → the line carries `format(row, v)`; absent → the raw value.
S-9 A raising `onChange` propagates; the value is stored; the `[Set]` line was emitted; `announce` not called.
S-10 `Get` of a non-row node answers the node; root absent → nil.
S-11 Every instance member works when taken as a value and called without `self` (`local set = inst.Set; set(p, v)`) — the reason for the convention.

**Defaults**
D-1 `Default(p)` is a deep copy; mutating it leaves `row.default` intact; unknown → nil.
D-2 `ApplyDefault(row)` writes through `Set` (one `[Set]` line, one `onChange`); `default == nil` → `false`, nothing written; non-table / no path → `false`.
D-3 `resetExempt`: inside a bracket → `false`, nothing written; outside → applies.

**Bracket**
B-1 One `[Set] reset all: N rows` line at close; per-row lines muted; a row already at default not counted.
B-2 Nested brackets → one line, summed tally, outermost act/scope.
B-3 `info.profileReset` at any level → no line.
B-4 `err` at any level → ` (stopped by an error)`.
B-5 Unpaired `BulkEnd` → no line, `InBulk()` false afterwards.
B-6 `BulkRun` re-raises the same error value (table identity for a table error), closes the bracket, line marked stopped; `fn(info)` setting `profileReset` silences it.
B-7 `BulkAdd(3)` inside a bracket adds to N; outside → nothing, no line.
B-8 (F-closure) a closure row whose `set` normalizes to the stored value counts 0 (read-back).
B-9 A raising `onChange` inside a bracket: the write still counts toward N.
B-10 The bulk line honours `debugEnabled`.

**Counting**
C-1 `CountOffDefault()` counts rows differing from default; skips `sessionOnly` and path-less rows; `pred` excludes the minimap row.
C-2 `ResetCounted(fn)`: inside `fn`, `ConsumeResetCount()` answers N; a second consume answers nil; after `ResetCounted` returns, nil.
C-3 `ResetCounted` with a raising `fn`: re-raised unchanged, pending cleared.
C-4 `ConsumeResetCount()` while a bracket is open → the bracket closes with no line.

**Validate**
V-1 F-flat healthy → `0, <stored row count>, 0`.
V-2 One fixture per shape error (non-table, missing path, bad type, bad page, missing group, duplicate path) → `errors` counts each once, `print` called once each.
V-3 An unresolvable path → `missing = 1`, printed; `sessionOnly` skipped; `defaultsRoot` returning nil skips; a path-less `get`/`set` row is not an error.
V-4 No `print` → same counts, silent.

**Major**
M-1 Registered; `MODULES.Schema == MINOR`; floors on Core (the `test_slash.lua:878` pattern: reload the file with Core absent → `LibStub(MAJOR, true)` is nil).
M-2 Public lib members are exactly `New, Read, SameValue, SplitPath, STRINGS, Write`; instance members are exactly the §5 list (pins the stub surface hosts mirror).
M-3 `L` overrides a `STRINGS` key.

Gates the addition must stay green on: `test_versioning` (majors.lua row, CHANGELOG, members manifest), `test_surface_parity`, `test_kitsync`, `test_prose` (US English), kit `test_eol`, kit `test_layout_cap`, `luacheck .` 0/0 — all through `/home/tushar/.claude/wow-addon/bin/ka0s-bounded`.

---

## 11. Per-consumer adoption delta (Phase 6 checklist)

Common to every adopter: re-vendor LibKa0s at the tag carrying Schema minor 1 (own commit, CLAUDE.md
provenance line in the same commit); `settings/Schema.lua` becomes the module's setup file
(`LibStub("LibKa0s-Schema-1.0", true)`, `lib:New{...}` or the §8 stub), stash the instance as
`NS.SchemaRuntime`; bind the host's existing public names to instance members so no call site moves;
point the Options and Slash descriptors' `get`/`set`/`applyDefault`/`findRow`/`allRows`/`bulkBegin`/
`bulkEnd` at the instance members directly (values, no wrappers) **only when the host has no
pre-seam gate**. `S.ApplyDefault` calls the instance's own `S.Set`, so a host wrapper in front of
`Set` is bypassed by every reset whatever the descriptors are bound to. A gate belongs in the row's
`validate` (verify round 1; PrettyChat below is the one host with such a gate). Re-pin
`tests/test_schema.lua` and the library-absent case; `luacheck` 0/0, suite green,
`docs/ARCHITECTURE.md` Settings Schema section re-names the seam. Every "delete" below means
"replace with the instance member/alias". A full adopter's `settings/Schema.lua` resolves
`LibStub("LibKa0s-Schema-1.0", true) or HostSchemaStub` (§8, write-completing). The library-absent
suite keeps pinning degraded **writes** (host verbs, Reset All, runtime writers). A pin on a degraded
**debug line** (a `[Set]` line, a bracket line, a reset count) re-pins to "the write landed, and
the line is absent", because the degraded DebugLog stub discards it.

### AbsorbTracker — full adopter
- `settings/Schema.lua:57-61` `RegisterSchemaRows` → `NS.RegisterSchemaRows = S.AddRows`; `:67-71` `FindSchemaRow` → `S.FindRow`.
- `:107-124` `ResolvePath`, `:126-138` `SetPath` → `lib.Read`/`lib.Write` (external caller `core/Data.lua:93,96`). **Re-run `tests/perf.lua`** (dormant repaint ≤ 320 bytes/iter).
- `:144-151` `defaultOnChange` → `announce = function(row) if not row.onChange and NS.bus then NS.bus:SendMessage(NS.MSG.APPEARANCE) end end`.
- `:167-238` bracket + `sameValue` + `NS.Bulk` → `NS.Bulk = { Begin = S.BulkBegin, End = S.BulkEnd, Run = S.BulkRun }` (callers `core/Units.lua:118`, `settings/OptionsSetup.lua:381` already pass `walk(info)`).
- `:187-202` `SetByPath` → `NS.SetByPath = S.Set`; descriptor `debugEnabled = function() return NS.State and NS.State.debug end`, `format = NS.FormatSchemaValue` (keep `:324-328`).
- `:248-282` reset count → `NS.ProfileRowsOffDefault = function() return S.CountOffDefault(notMinimap) end`, `NS.ResetProfileCounted = function(db) S.ResetCounted(function() db:ResetProfile() end, notMinimap) end`, `NS.ConsumeResetCount = S.ConsumeResetCount`.
- `:289-302` `ApplyDefault` → `S.ApplyDefault` (one-level copy becomes deep — safe, every table default is flat).
- `:376-422` `ValidateSchema` → `S.Validate{ pages = {general,appearance,profiles}, defaultsRoot = function(parts) if parts[1] == "global" then return NS.defaults.global, 2 end return NS.defaults.profile, 1 end }` (keeps the 3-count return).
- `core/Data.lua:54-57` `RegisterSessionSetting` and the session/minimap branches in `:81-120` → stamp `get`/`set` onto the composed console row and minimap row (composed at `settings/General.lua:94`); `NS.GetSetting` becomes a wrapper: `S.Get(path)` then `lib.Read(NS.flatDefaults, path)` when nil (JC pre-db fallback, §6); `NS.SetSetting` deleted.
- `settings/OptionsSetup.lua:59` `survivesEveryReset` + `:88-91` wrapper → descriptor `resetExempt = { [NS.Constants.MINIMAP_PATH] = true }`, `applyDefault = S.ApplyDefault`; `:84-92`, `:138-139` → members.
- `settings/Slash.lua:599-609` → members.
- Keep: `SchemaForPage :76-97`, `FormatSchemaValue :324-328`, pages list.
- Behavior deltas to pin: unknown-path `Set` refused (JC-2); table values copied (JC-6).
- Degraded build (§8 stub): the host verbs, the Options stub's Reset All
  (`settings/OptionsSetup.lua:381`) and the combat re-lock (`core/AbsorbTracker.lua:259`) keep
  writing; `NS.ResolvePath`/`NS.SetPath` call `SchemaLib.Read`/`SchemaLib.Write` unconditionally (the
  stub supplies both). `tests/test_optionssetup.lua` "the degraded Reset All logs one line in total"
  re-pins to the handler's line **without** `(N rows)`; "the degraded Reset All with no AceDB logs its
  own one line" re-pins to zero lines plus the rows written. "Reset All resets a sessionOnly row ...
  on both builds" stays as is, and green. The `settings/OptionsSetup.lua:383` rationale ("losing the
  reset would not be") stays true and stays.

### PartyFrameEnhanced — full adopter
- `settings/Schema.lua:22-35` `byPath`/`RegisterSchemaRows`/`FindSchemaRow` → `S.AddRows`/`S.FindRow`.
- `:63-75` `ResolvePath`, `:77-89` `SetPath` → `lib.Read`/`lib.Write`. **Re-run `tests/perf.lua`** (`resolveUnchanged` 0 bytes/iter).
- `:95-131` session/global registries + `IsGlobalSetting` → `get`/`set` stamped on the console and minimap rows (`settings/General.lua:65`); `IsGlobalSetting` survives only as the `pred`/`resetExempt` source or is deleted.
- `:134-161` `GetSetting`/`SetSetting` → wrapper over `S.Get` with `defaults.profile` fallback; `SetSetting` deleted.
- `:165-174` `sectionOf`/`publishConfig` → `announce = function(row) if not row.sessionOnly then publishConfig(sectionOf(row)) end end`.
- `:181-250` bracket → `S.Bulk*` (caller `settings/OptionsSetup.lua:127` passes `walk(info)`).
- `:198-220` `SetByPath` → `S.Set` (the `"%s refused"` debug line at `:204` is dropped — a refused write is not a mutation, §10; returns `false, err` instead of `false`).
- `:259-283` → `CountOffDefault`/`ResetCounted`/`ConsumeResetCount`; `:286-289` → `S.ApplyDefault`.
- `:322-372` validation → `S.Validate{ pages = VALID_PAGES, defaultsRoot = ... }` (global row → `NS.defaults`, 1).
- `settings/OptionsSetup.lua:24-33` `exemptFromReset`, `:59-62` wrapper → `resetExempt`; `:47-64`, `:80-81` → members. `settings/Slash.lua:412-422` → members.
- Keep: `SchemaForPage :39-54`, `FormatSchemaValue :299-303`.

### AuraMaster — partial adopter (primitives, registry, bracket, validation; keeps its seam)
- **Amended in verify round 1.** AM keeps its own `SetByPath`, which must still work library-less
  (`tests/degraded_env.lua` loads no LibKa0s). Its own primitives, index and bracket **are** its
  library-absent answer, so every "→" below reads "call the library when present, else the host's
  existing function" (`local Read = SchemaLib and SchemaLib.Read or readFrom`), never "delete".
  Measured by the verifier: with the host copies deleted, 20 AM tests fail (among them "degraded:
  without LibKa0s the addon still loads and every seam answers" and "slash verbs: without the library
  the host verbs keep working"). With the fallbacks kept, the degraded bracket's one line
  (`bulklog: the degraded build's Reset all is one line in total, too`) stays green because it is
  AM's own bracket. **Cost:** minor 1 removes none of AM's walker or bracket code; the live path runs
  the shared copy, the degraded path AM's. AM MAY defer this adoption until it adopts `Set` (the
  re-check trigger below); the revendor interview decides.
- `settings/Schema.lua:88-99` `splitPath` → `lib.SplitPath`; `:101-109` `readFrom` → `lib.Read`; `:111-120` `writeInto` → `lib.Write` (both take `parts` + `first`).
- `:181-191` index/`FindSchemaRow` → `S.FindRow`. `:209-233` `RegisterSchemaRows(rows, beforePath)` keeps its default stamping (`NS.DefaultFor`, single consumer) then calls `S.AddRows(rows, indexOf(beforePath))`; `:250-270` `UnregisterSchemaRows` keeps its in-place rebuild and ends with `S.Reindex()`.
- New `rows = NS.Schema`; `resolveRoot`/`announce` **not** passed (AM's seam is its own).
- `:389-443` bracket → `NS.Bulk = { Begin = S.BulkBegin, End = S.BulkEnd, Run = S.BulkRun }`; internal `tally(n)` → `S.BulkAdd(n)`; `bulk.depth > 0` tests (`:456`, `:485`, `:501`, `:617`, `:648`, `:686`) → `S.InBulk()`. `Bulk.Run` callers `modules/ContainerManager.lua:471`, `:502` and the degraded Reset all: `return true` → `info.profileReset = true` (JC-9).
- `:427-431` `changes()` → `not lib.SameValue(old, new)` (drops the `FilterCompiler.Signature` dependency; spell-id sets are integer-keyed after `normalizeIdSet :322-330`, so the key-type difference is unreachable).
- `:819-835` `ValidateSchema` → `local e, _, m = S.Validate{ pages = VALID_PAGES, defaultsRoot = function(parts) if parts[1] == "container" then return NS.CONTAINER_TEMPLATE, 2 elseif parts[1] == "global" then return NS.defaults, 1 end return NS.defaults.profile, 1 end }; return e + m`.
- Keep: `SetByPath :711-726`, `GetSetting :302-314`, `CheckWrite :761-775`, `ApplyDefault :782-787`, carve-outs, sections, minimap, `Choices`. Re-check trigger for full adoption: `row.normalize` gains a second consumer.

### MultiMeters — partial adopter (primitives, registry, bracket)
- **Amended in verify round 1**, same shape as AuraMaster: MM keeps its own `SetByPath`, so its
  primitives, index and bracket stay as the library-absent fallback, and every "→" below reads "call
  the library when present, else the host's function". Minor 1 removes none of MM's walker or bracket
  code; MM MAY defer.
- `settings/Schema_Paths.lua:97-106` `splitPath`, `:109-116` `readFrom`, `:119-127` `writeInto` → `lib.*`.
- `:245-280` index/`FindSchemaRow`/`RegisterSchemaRows` → `S.FindRow`/`S.AddRows` (New at file scope where `reindex()` runs today, `:254`).
- `:549-634` bracket: `bulkOpen`/`bulkClose`/`runBulk` → `S.BulkBegin`/`S.BulkEnd`/`S.BulkRun`; `tally :613-618` keeps its seen-set dedup and calls `S.BulkAdd(1)`; `bulk.depth` tests → `S.InBulk()`; `NS.Bulk = { begin = S.BulkBegin, finish = S.BulkEnd, run = S.BulkRun }` (`runBulk` callers: `fn` return `true` → `info.profileReset = true`, JC-9).
- `:585-595` `sameValue` → `lib.SameValue`.
- Keep: `SetByPath :730-739`, `SetByPaths :773-798`, `prepareWrite`, columns carve-out, minimap, `ApplyDefault :809-824`, `ValidateSchema :943-960` (agreement check is single-consumer; MM does not adopt `Validate` in minor 1).

### BankLedger — full adopter
- `settings/Schema.lua:396-421` `FindRow`/`ReadPath`/`WritePath` → `S.FindRow`/`lib.Read`/`lib.Write`; `:427-432` `deepcopy` deleted (lib copies).
- `:460-497` bracket + `S.SameValue` → `S.BulkBegin`/`S.BulkEnd`, `S.SameValue = lib.SameValue`.
- `:502-526` `storedValue`/`writeStored` (minimap inversion) → add `set = function(v) local t = NS.db.global.minimap; if t then t.hide = not v end end` to `MASTER_DECOR[S.MINIMAP_PATH]` (`:260-268`, which already has `get` and the `SetShown` `onChange`).
- `:530-560` `S:Set` → `function S:Set(p, v) return inst.Set(p, v) end`; `resolveRoot = function() return NS.db and NS.db.global, 1 end`; `announce = function() if NS.Panel and NS.Panel.Refresh then NS.Panel:Refresh() end end`; `debugEnabled` from `NS.State.debug`.
- `:562-571` `S:Get`/`S:Default` → members; `:585-589` `S:ApplyDefault` → `inst.ApplyDefault` with `resetExempt = S.RESET_EXEMPT` (`:172`).
- `:594-606` `S:Register` → `S.Validate{ types = {bool,number,string,color,table}, defaultsRoot = function() return NS.defaults.global, 1 end }` — **removes the dead `row.default == nil` conjunct** (JC-13); measure to zero.
- `:334` head splice in `S:ComposeMaster` → `inst.AddRows(rows, 1)` (and drop the `S.__pageRows` reset only if `PageRows` is rebuilt).
- `settings/OptionsSetup.lua:46-49` — note `applyDefault` today calls `S:Set(row.path, S:Default(row.path))`, **bypassing** the `RESET_EXEMPT` veto; pointing it at `inst.ApplyDefault` closes that. `settings/Slash.lua:436-453` → members.

### LootHistory — full adopter
- `settings/Schema.lua:392-417` `FindRow`/`ReadPath`/`WritePath` → members/`lib.*`; `:423-428` `deepcopy` deleted.
- `:445-480` bracket → members; `S.SameValue` (`:449-455`, read by `Sl:ResetEverything`) → `lib.SameValue`.
- `:509-512` `S:ApplyDefault` → `inst.ApplyDefault`, `resetExempt = S.RESET_EXEMPT` (`:499`).
- `:515-546` `S:Set` → wrapper over `inst.Set` (the `row.set`-for-a-stored-row branch `:527-535` is exactly the lib rule); `resolveRoot` → `NS.db.global, 1`; no `announce`.
- `:548-557` `Get`/`Default` → members. `:569-583` `S:Register` → `S.Validate{ types incl. table, defaultsRoot → NS.defaults.global }`.
- New after `:381-383` builds `S.Schema`. `settings/OptionsSetup.lua:179-200`, `settings/Slash.lua:371-395` → members.

### PanelMaster — full adopter
- `settings/Schema.lua:349-374` `FindRow`/`ReadPath`/`WritePath` → members/`lib.*`.
- `:389-419` `S.bulk`/`BulkBegin`/`BulkEnd`/`BulkLine` → members; `BulkLine(act, scope, n)` → `inst.BulkRun(act, scope, function() inst.BulkAdd(n) end)` (callers in `modules/Registry.lua`).
- `:452-493` `S:Set` → wrapper; the minimap branch `:464-479` and the `S:Get` branch `:503-505` move onto the composed minimap row as `get`/`set` in `S:InstallMaster` (`:216`, a `wire(rows, S.MINIMAP_PATH, {...})` beside the others); `resolveRoot = function() return NS.db and NS.db.profile, 1 end`.
- `:511-514` `S:Default` → member. `:426-448` snapshot count MAY stay (§6).
- `:532-554` `S:Register` → `S.Validate{ defaultsRoot = function(parts) if parts[1] == "global" then return NS.defaults, 1 end return NS.defaults.profile, 1 end }`.
- `:337-339` head splice → `inst.AddRows(rows, 1)` (after the `wire` calls, so the index sees `state.locked`, `:304-305`).
- `:242` `defaults` gains `debugConsole = false` (JC-5; PM relies on writing `nil` today).
- `settings/OptionsSetup.lua:180-191` (the `applyDefault` at `:182` becomes `inst.ApplyDefault`), `settings/Slash.lua:552-556` → members.

### PrettyChat — seam adopter (no `resolveRoot`: every row is closure-backed)
- `settings/Schema.lua:43-49` `rows`/`byPath`/`addRow` → `rows` is the descriptor array; `addRow` → `S.AddRows({row})` (or append then one `S.Reindex()` after the build loop `:361-376`).
- `:479-481` `FindByPath` → `S.FindRow`; `:523-527` `Get` → `S.Get` (unknown → nil, same).
- `:636-670` `Schema.Set` → `S.Set`, with **no** wrapper gate (amended in verify round 1). `refusedBySignature` (`:620-629`) moves into `validate` on every `string_format` row where the row is built: `validate = function(v) if refusedBySignature(row, v) then Schema.NotifyPanelChange(row.category); return false, "conversion signature" end return true end` (the chat line and the snap-back refresh stay on the refusal). Then `S.Set`, `S.ApplyDefault` and the value-bound Options/Slash descriptors are all gated. A wrapper would not be: the verifier bound `set = NS.Schema.Runtime.Set` in a copy (`PC_direct`) and `/pc set Loot.LOOT_ITEM_SELF.format Loot | %s %s` stored the surplus-conversion format, reopening PC-R-01 (a raise inside Blizzard's chat handler on every matching message), with the suite still 397/2 and no new red. `ApplyDefault` bypasses any wrapper; shipped defaults pass the gate, so that half is latent, not live. **New PC test:** drive `/pc set <string_format path> <format with a surplus conversion>` through the Slash dispatcher; assert the stored format is unchanged, the refusal line printed once, and the `[Set]` line absent. Wrap each row's `set` in `PrettyChat.Batch` where it is built (`:291`, `:316`, `:342`, `MASTER_WIRING :152-237`) instead of at `:656`. `announce = function(row) if not row.sessionOnly then PrettyChat:ApplyStrings() end Schema.NotifyPanelChange(row.category) end`; `format = Schema.FormatValue`. The `[Set]` line moves before the re-apply (JC-4).
- `:676-678` `AllRows` → `S.AllRows`; `:690-693` `ApplyDefault` → `S.ApplyDefault`; `MASTER_SPEC.defaults :104-107` gains `debugConsole = false` (JC-5).
- `:715-721` `CountChangedRows` → `S.CountOffDefault()`.
- `:744-780` `ResetRows` keeps its body (its one-`ApplyStrings`-per-batch shape is the sanctioned batched entry), MAY replace `NS.Util.RunAct` + local tally with `S.BulkRun`/`S.BulkAdd`.
- `:495-521` `InstallMasterControls` splice (`table.insert(rows, at, row)`) → collect wired rows, `S.AddRows(wired, 1)`.
- Keep: `runValidation :454-471` (per-kind resolver; rows are not path-mapped), category helpers.

### WhatGroup — seam adopter
- `settings/Schema.lua:288-305` `Resolve` → `resolveRoot = function() return WhatGroup.db and WhatGroup.db.profile, 1 end` + `lib.Read`/`lib.Write`.
- `:328-336` `SESSION`, `:368-386` `GLOBAL` → stamp `get`/`set` on the composed rows where they are decorated (`settings/Panel.lua:283-289`). Note the session `get` returns `spec.get() or false` today (`:392`); keep that in the stamped closure.
- `:388-419` `Helpers.Get`/`RawSet` → `S.Get`; `RawSet` deleted (no caller outside the seam).
- `:451-479` `Helpers.Set` → `S.Set` (`announce = function() Helpers.RefreshAll() end`); the `pcall` around `onChange` goes (JC-3).
- `:435-527` bracket → members (`Settings.Bulk = { begin = S.BulkBegin, finish = S.BulkEnd }`); `silenceOpenBracket :523-525` → the lib's `ConsumeResetCount` (JC-12).
- `:481-485` `FindSchema` → `S.FindRow`.
- `:544-577` `ValidateSchema` → `S.Validate{ types = {bool,number,string} }` plus a host loop for `section`/`label` (single-consumer checks).
- `:665-732` → `pendingResetCount`/`ConsumeResetCount`/`countChangedProfileRows` → `S.ResetCounted`/`S.ConsumeResetCount`/`S.CountOffDefault(notGlobal)`; the `STOPPED` line on a raising reset stays host. The session sweep `:722-727` (the one `opts` caller) → `S.BulkRun("reset", "profile", function(info) info.profileReset = true; for each sessionOnly row: S.ApplyDefault(row) end)` — the bracket mutes the per-row line, `profileReset` suppresses the bulk line; the per-row `RefreshAll` it used to skip is two extra refreshes of rows whose `onChange` is a window toggle.
- `:751-754` `ApplyDefault` → `S.ApplyDefault`.
- `settings/Panel.lua:295-296` head splice → `S.AddRows(MASTER_ROWS, 1)`. `settings/OptionsSetup.lua:194-219`, `settings/Slash.lua:232-236` → members.
- Keep: `BuildDefaults :596-629`, popup registration.

---

## 12. OPEN (standard vs design — both readings, not silently picked)

- **O-1 The write seam's name and call style.** Reading A (`architecture.md:133`): the helper is
  `NS.Schema:Set(path, value)`, a colon method on `NS.Schema`. Reading B (`slash-commands.md:83`):
  `NS.SetByPath(path, v)`, a free function. v2.63.0 carries both (C1-F11's surviving finding was not
  promoted). Neither reading can be what a *library* instance member is called, because a colon
  member cannot be handed to a descriptor as a value, and `NS.Schema` is the rows array in four
  hosts. The design takes neither as the library's name (members are `inst.Set`, dot-called) and
  lets a host alias under either. **Proposed upstream ruling:** architecture-§5 names the helper as
  "the schema instance's `Set(path, value, instanceId)`, dot-called so it can be handed to the
  Options and Slash descriptors as a value", and slash-commands-§3's example becomes
  `set = S.Set`. Until then, hosts keep today's names.
- **O-2 Core floor for a runtime-critical major.** Reading A (house convention, library-stack-§7:
  "seven of those eleven gate on it without calling a single member … so that a host holding a
  partial payload gets every module absent"): floor on Core. Reading B: this major calls nothing in
  Core and is the only one the feature runtime reads per frame, so a Core-less file would degrade
  *less* (a partial payload loses the panel and CLI but keeps settings). The standard states A as
  the majority behavior, not as a MUST for a module that needs nothing. **Design takes A**
  (conservative: the fall-together property the options-ui-§1 ruling relies on holds).
- **O-3 A "read-completing" degradation class.** options-ui-§1 defines load-completing (Options) and
  the member-answering default; neither covers a member the runtime reads every frame. The stub in
  §8 carries a few-line read walk, which is the kind of host copy options-ui-§1 forbids for widget
  makers and layout constants. Reading A: the prohibition is scoped to Options' rendering code and a
  read walk is fine. Reading B: any host copy of library behavior is anti-pattern #47. **Design takes
  A** and asks for a ruling naming the class.
- **O-5 A write-completing degradation stub (verify round 1).** Reading A (taken): the stub completes
  writes because `slash-commands-§1` (host verbs keep working), `options-ui-§1` (SHOULD keep Reset
  All real) and anti-pattern #56 shape 2 (a stub blacking out verbs) all describe the degraded path
  as working. The no-copy MUST in options-ui-§1 lists widget makers, the flow engine, the header and
  layout constants, not a runtime write path. `LibKa0s-Compat-1.0`'s guard stubs are the in-release
  precedent for a documented duplication. Cost: 59 lines of write half per full adopter, 132 lines
  for the whole reference stub. Reading B: any host copy of library behavior is anti-pattern #47, so
  the stub refuses writes. Each adopter then records a deviation from slash-commands-§1 for its
  writing host verbs, retires its library-less write pins (AbsorbTracker's host verbs, Reset All and
  combat re-lock; PrettyChat's reset) and deletes AbsorbTracker's "losing the reset would not be"
  rationale. **Proposed upstream ruling:** options-ui-§1 names a *runtime-completing* stub class for
  a major the feature runtime and host writers reach. Reads and writes complete; logging and
  counting do not; the host copy carries a comment naming the section. Until then, each host's stub
  comment cites `docs/api/Schema/version-1-docs.md` "The degradation stub".
- **O-4 `library-stack-§7`'s correctness bar vs the seam.** JC-2 (unknown paths), JC-3 (a raising
  `onChange`) and JC-6 (copy on write) are disagreements about behavior, not presentation. The design
  argues each is settled by the standard's own text or is latent (no exercised call site differs), so
  the seam passes the bar without escape hatches; the two hosts whose disagreements are real and
  exercised (AM, MM) are left out of `Set` rather than accommodated. A reviewer taking the strict
  reading ("any correctness disagreement disqualifies the shape") would ship minor 1 **without**
  `Get`/`Set`/`ApplyDefault`/`Default`/`CountOffDefault`/`ResetCounted`/`ConsumeResetCount` — the
  primitives, registry, bracket and `Validate` still clear all three bars on their own.

---

## 13. Build amendments (2026-09-23, recorded by the builder)

Building minor 1 showed nine places where the spec above was silent or unsafe. Each is now what
`LibKa0s/Schema.lua` does, what `docs/api/Schema/version-1-docs.md` documents, and what a case in
`tests/test_schema.lua` pins. None changes a member, a signature or a judgement call.

- **A-1 `SplitPath(nil)` is the empty path.** §3 said "non-string → `tostring(path)` first", which
  makes `nil` the one-segment path `"nil"` and lets `Write(root, nil, v)` store `root["nil"]`. `nil`
  now answers the shared empty array; every other non-string is still `tostring`ed.
- **A-2 `format` absent → `tostring(value)`, not the raw value.** §4/§5 step 8 passed the raw value
  to `debug`'s `%s`. Under Lua 5.1 `string.format("%s", true)` raises, so a host sink that formats
  (every AT/PFE-shaped `NS.Debug`) would raise on the first boolean write with no `format` given. A
  `format` answering `nil` falls back the same way.
- **A-3 A non-table root is "nowhere", and only a string second value is a reason.** §4 treated a
  nil root as absent and its second value as the reason. `function() return NS.db and NS.db.global,
  1 end` answers `nil, 1` pre-db (and `false, 1` when the db field is `false`), and `1` is not a
  refusal text; the seam now refuses `NO_ROOT` there.
- **A-4 `resolvedId` falls back to `instanceId`.** §4 did not say what `validate`/`onChange`/`announce`
  receive when the resolver returns no third value, or when it is not called (closure and
  `sessionOnly` rows, and a missing root). They receive `instanceId`.
- **A-5 `AddRows` bounds.** `at` non-number → append (as nil); `at < 1` → head; non-integer `at` is
  floored.
- **A-6 `BulkAdd` with a non-number adds nothing.**
- **A-7 Descriptor fields other than `rows` are read at call time** (the Lifecycle precedent: `d.print`
  is read in `PrintHolds`), so a host may fill `announce`/`debug` after `:New`. A field of the wrong
  type counts as absent.
- **A-8 The tally's before-image is deep-copied.** A closure `set` that mutates a stored table in
  place would otherwise hand back the same reference as before and after, and count 0. Paid only
  inside a bracket. (Found while building: the obvious `before = bulk and Get(...) or nil` reads a
  stored `false` as `nil` and counts every false-valued row in a sweep as changed. The bracket case
  B-1 is red under that idiom.)
- **A-9 `CountOffDefault` counts only the indexed row for a path.** §5 said "indexed rows"; iterating
  `AllRows()` would count a later duplicate twice. A row counts iff `FindRow(row.path) == row`.

Additions to the test plan: a reference degradation stub pinned against a live instance with the
kit's two-table `assertSurfaceParity` (§8's "each host pins the stub's member set", made executable
upstream); a bare-false `validate`; a resolver answering `nil, 1`; `Validate`'s `types` replacement.

## 14. Verify round 1 amendments (2026-09-23)

- **V-1 Stub reading.** §8 now specifies a write-completing, log-silent stub (was: read-completing,
  refusing `Set`). Removes the false fall-together claim. O-5 records both readings.
- **V-2 Lib-level stub.** The stub stands in for the library table too (`SplitPath`/`Read`/`Write`/
  `SameValue`/`New`), so a full adopter's own primitive callers work library-less.
- **V-3 Partial adopters.** AM and MM: "call the library when present, else the host's function";
  the host copies stay as the library-absent fallback; minor 1 removes none of their walker/bracket
  code; either MAY defer.
- **V-4 Pre-seam gates.** The common rule binds members directly only with no pre-seam gate; a gate
  goes in `validate` because `ApplyDefault` calls the instance's own `Set`. PrettyChat's
  conversion-signature check moves into `validate`, with a `/pc set` refusal test.
- Upstream proof: `tests/test_schema.lua` replaces the refusing reference stub (1 case) with the
  write-completing one (5 cases). LibKa0s suite 1456 passed, 0 failed, 1 skipped, 1457 total.
