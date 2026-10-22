# Design: `LibKa0s-Glow-1.0`, the stateless LibCustomGlow-1.0 driver (LibKa0s v1.75.0, Glow minor 1)

Status: design for the v1.75.0 run. Read-only survey done 2026-10-22 against working trees at LibKa0s `d9f9454` (master, unreleased v1.75.0, kit 40), WowAddonStandards v2.85.0, and DropWatcher, QuickComms and KickCD as they are checked out today. The three hosts vendor a byte-identical `libs/LibCustomGlow-1.0/LibCustomGlow-1.0.lua` (md5 `78fd0531…`, `MINOR_VERSION = 24`, 955 lines). Every LCG line cited below is from that file.

## 1. Decisions in one place

| # | Decision | Why |
|---|---|---|
| D1 | New major `LibKa0s-Glow-1.0`, one file `LibKa0s/Glow.lua`, minor 1. Floor is `NEEDS_CORE = 1` only, and no Core member is called. | The owner has accepted it. This is the Env/Pool/Item pattern: it floors so that a partial payload leaves every module absent. |
| D2 | The surface is exactly two members, `Start(frame, style, knobs, key, frameLevel)` and `Stop(frame, style, key)`, besides `MAJOR`, `MINOR` and `MODULES`. | It is the smallest contract that serves all three hosts with the same semantics. The challenger's scope cut drops `G.Available()`. |
| D3 | `frameLevel` is a **fifth, optional positional argument**, not a knob. | It says where the host stacks the effect. It is not a player setting. DW and QC pass a constant 2, and KickCD passes nothing (LCG's 8 over its own +5 child). Putting it in `knobs` would make DW write a constant into the profile-derived `cfg` (Glow.lua `read`) and QC write one into the signature-bearing `g` (IconStyle.lua `glowConfig`). Bar 2 allows exactly one optional presentation argument. **Owner check:** the brief sketched 4 arguments (see open questions). |
| D4 | `color` lives **in `knobs`** (`knobs.color`, an `{r,g,b,a}` array). | The owner's 4-argument shape has no colour slot. DW `cfg.color` and QC `g.color` are already arrays in exactly that place, and KickCD sets one field on its reused table. |
| D5 | Style vocabulary is closed: `"button"`, `"proc"`, `"pixel"`, `"autocast"`. These are lowercase strings, exactly what all three hosts store. There are no aliases, and an unknown style is a quiet no-op (`false`). | LCG's own names are "Action Button Glow", "Proc Glow", "Pixel Glow" and "Autocast Shine". The owner's "Button/Action" is LCG's "Action Button Glow" and maps to `"button"`. Aliases would be an escape hatch. |
| D6 | **No `STYLES` member.** The four names are documented vocabulary, pinned by the library's tests. | No host could use a list. DW's `GLOW_STYLES` (SchemaRows.lua:152) is a localized `choices{}` table, QC's `D.GLOW_STYLES` drives its own dropdown in its own order, and KickCD's styles live in its settings rows. A member nobody reads is a member nobody tests, and it stays additive-only forever. |
| D7 | **Knob RANGES are not published (rejected).** See §5. | Ranges are slider policy, not LCG facts. Every host keeps its own table regardless (defaults, keys, kind vocabulary, labels, order). |
| D8 | **No defaults.** A `nil` knob reaches LCG as `nil`, so LCG's own value applies. Two traps are coerced, with nothing else: `pixelLength` (a number > 0, otherwise `nil`) and the two booleans (`false` only when `false`). A numeric knob that is not a number becomes `nil`. | This is the owner's "NO defaults". It is also the challenger's scope cut: the DW/QC `num(v, 0)` and `num(v, 1)` fallbacks are not baked in, because LCG's nil value is the same number. |
| D9 | LCG is resolved **at every call** with `LibStub("LibCustomGlow-1.0", true)`, with no memo. If LCG is absent, `Start` answers `false` and `Stop` does nothing. | Bus/AceEvent is the precedent (Bus.lua:31-32). The call is one LibStub index, negligible next to LCG's own work, and it is never per-frame. KickCD's worst path is a `Stop` per not-ready `SPELL_STATE`, which is event-driven. Call-time resolution is also what lets every host suite inject its fake LCG after load. A memo was rejected: it adds state to a stateless driver and a staleness argument (LibStub upgrades in place, so it would be safe, but it still has to be argued) to save nothing measurable. |
| D10 | Each LCG member is presence-checked (`type(fn) == "function"`) before it is called. | The library cannot floor on a consumer-vendored third-party lib (library-stack-§6/§7). A host whose LCG copy is older than ProcGlow (or is someone else's winning copy) gets `false`, not an error inside the library. |
| D11 | No lifecycle, signature, unchanged-repaint gate, proc-burst spend, trigger, class-colour resolution, stop-before-start, `GlowGroup` composer or catalog. | All rejected (#56). §7 below records them under "What is not here". |

## 2. The contract (what `docs/api/Glow/version-1-docs.md` publishes)

### `Glow.Start(frame, style, knobs, key, frameLevel) -> boolean`

- `frame`: the frame the effect is drawn around. If it is `nil`, the call returns `false` and nothing is called. LCG's `_Start` functions return on a nil frame, but its `_Stop` functions do not all do so (`ButtonGlow_Stop` and `ProcGlow_Stop` index `r` unguarded, LCG:750, :945), so the driver guards both members the same way.
- `style`: one of the four names. Anything else returns `false`.
- `knobs`: a table, or `nil`, which is read as an empty table (a shared constant, no allocation). Any other type is also read as empty. Fields the driver does not name are ignored, so a host can pass its whole config table (DW `cfg`, QC `g`).
- `key`: the caller's identity string, passed through unchanged. `nil` is LCG's shared empty key `""`, so the doc says *pass your addon's own key*. The `button` style takes no key.
- `frameLevel`: a number or `nil` (LCG uses 8). It is relative to `frame` (LCG `r:GetFrameLevel() + frameLevel`, LCG:133, :671, :717, :933).
- It returns `true` when it called LCG's `_Start` for that style. It returns `false` when the frame is nil, the style is unknown, LCG is absent, or the style's `_Start` is missing.
- It does **not** stop anything first. Switching styles is the host's job: stop the old one, then start the new one. All three hosts already do this.

### `Glow.Stop(frame, style, key)`

- `style` given: only that style's `_Stop`. `button` gives `ButtonGlow_Stop(frame)` with no key. The others give `X_Stop(frame, key)`.
- `style == nil`: **all four**, in KickCD's order (Button, Pixel, AutoCast, Proc). This is KickCD's shape (IconGrid_Render.lua:388-396). Per the brief the `style?` stays optional, overriding the challenger's suggestion to drop stop-all.
- An unknown style **string** is a no-op. Only `nil` means all four.
- A nil frame or an absent LCG is a no-op. A missing `_Stop` member is skipped. It returns nothing.

### Knob → LCG argument mapping (the contract table)

`num(v)` is `v` when `type(v) == "number"`, otherwise `nil`.

| Style | LCG call (LCG line) | Arguments, in order |
|---|---|---|
| `pixel` | `PixelGlow_Start(r,color,N,frequency,length,th,xOffset,yOffset,border,key,frameLevel)` (:260) | `frame, knobs.color, num(pixelLines), num(pixelFrequency), length(pixelLength), num(pixelThickness), num(xOffset), num(yOffset), pixelBorder ~= false, key, frameLevel` |
| `autocast` | `AutoCastGlow_Start(r,color,N,frequency,scale,xOffset,yOffset,key,frameLevel)` (:399) | `frame, knobs.color, num(autocastParticles), num(autocastFrequency), num(autocastScale), num(xOffset), num(yOffset), key, frameLevel` |
| `button` | `ButtonGlow_Start(r,color,frequency,frameLevel)` (:657) | `frame, knobs.color, num(buttonFrequency), frameLevel` (no key) |
| `proc` | `ProcGlow_Start(r, options)` (:915) | `frame, { color = knobs.color, startAnim = procStartAnim ~= false, duration = num(procDuration), xOffset = num(xOffset), yOffset = num(yOffset), key = key, frameLevel = frameLevel }`, a **fresh table per call** |

The knob names are the DW/QC camelCase spellings, and the published vocabulary is these fourteen fields: `color, pixelLines, pixelFrequency, pixelLength, pixelThickness, pixelBorder, autocastParticles, autocastFrequency, autocastScale, buttonFrequency, procDuration, procStartAnim, xOffset, yOffset`. KickCD's PascalCase leaves map to them by lower-casing the first letter (`XOffset` → `xOffset`, `ButtonFrequency` → `buttonFrequency`, and so on, all 13 exact).

### The traps, written into the doc

1. **`pixelLength` 0 means automatic.** LCG computes the length only for `nil` (`length = length or floor(...)`, LCG:283). A 0 would draw zero-length lines. The driver passes a number > 0 through and sends 0, negatives and non-numbers as `nil`.
2. **`pixelBorder` draws for anything but `false`.** LCG tests `if not(border==false)` (:303), so `nil` draws the dark border. The driver passes `pixelBorder ~= false`, a real boolean with LCG's own nil meaning: a host that wants no border passes `false`. The same rule applies to `procStartAnim`, where LCG's default is `true` (ProcGlowDefaults, :903-911).
3. **The proc options table must be fresh.** `ProcGlow_Start` calls `setmetatable(options, …)` on whatever it is handed (:920). The driver never hands over the caller's `knobs`, and it does not reuse a scratch table. DW's test reads `lib.calls[n][3].color` / `.duration` after later calls (test_glow.lua:166, :183-200), so a reused scratch would corrupt those recordings. LCG allocates a metatable per proc start anyway, so a fresh options table costs nothing extra. It is also what all three hosts do today.
4. **`color` is retained by reference** by the button style (`f.color = color`, LCG:704, :728). On a restart that reuses the frame, LCG divides the old alpha by `f.color[4]` (:700). A host **must not mutate** a colour array after handing it over. Hand over a fresh array, or one that never changes. DW builds `cfg.color` once per settings generation, QC builds `g.color` per config build, and KickCD allocates `{ r, gr, b, a }` per restart (IconGrid_Render.lua:503). All three comply, and the doc makes it a rule.
5. **The `button` style has no key.** Each frame has one Blizzard-style glow (`r._ButtonGlow`). Two keyed callers on one frame cannot both use `button`, and `Stop(frame, nil, key)` stops any button glow on the frame, whoever started it. **Use stop-all only on a frame you own.** KickCD's own glow child qualifies. QC already keeps its two glows on two frames (`qcIconFrame` under `QuickCommsIcon`, `qcEdge` under `QuickCommsButton`). This is the challenger's missed item, so the doc states it.
6. **`ButtonGlow_Stop` on a visible frame animates out** and releases later (:750-761). A restart inside that window reuses `r._ButtonGlow`. This is LCG behaviour, transparent to the driver, and recorded so nobody "fixes" it.
7. **Combat.** LCG's frames are plain children, so the driver makes no protected call. QC already relies on this for hover and send glows in combat (QC Glow.lua header).

## 3. `LibKa0s/Glow.lua` (implementation spec)

The file is about 110 lines including the header. The header explains why it exists (three hosts mapped the same knobs to the same positional arguments, with the same two traps) and what it deliberately is not (the §7 list). Shape:

```lua
local core = LibStub and LibStub("LibKa0s-Core-1.0", true)
local NEEDS_CORE = 1
if not core or (core.MINOR or 0) < NEEDS_CORE then return end   -- no NewLibrary; module absent

local MAJOR, MINOR = "LibKa0s-Glow-1.0", 1
local lib = LibStub:NewLibrary(MAJOR, MINOR)
if not lib then return end
lib.MAJOR, lib.MINOR = MAJOR, MINOR
lib.MODULES = lib.MODULES or {}
lib.MODULES.Glow = MINOR

local LCG = "LibCustomGlow-1.0"
local NONE = {}                                   -- nil knobs: read nothing, allocate nothing
local function lcg() return LibStub and LibStub(LCG, true) end   -- CALL time, every call
local function num(v) if type(v) == "number" then return v end end
local function len(v) if type(v) == "number" and v > 0 then return v end end
-- START[style](L, frame, k, key, level) -> boolean; each checks type(L.X_Start) == "function"
-- STOP[style](L, frame, key); ORDER = { "button", "pixel", "autocast", "proc" } for stop-all
function lib.Start(frame, style, knobs, key, frameLevel) ... end
function lib.Stop(frame, style, key) ... end
```

- Members are dot-called (`G.Start(...)`), like Pool and Item.
- The non-proc styles allocate nothing in the driver. KickCD's `startEffect` closure `k` (IconGrid_Render.lua:449) goes away, so KickCD's hot path ends slightly lighter, not heavier. This resolves the analyst's allocation risk.
- The file is not secret-sensitive. It reads no unit data.

### Registration ripple inside LibKa0s

| Place | Change |
|---|---|
| `LibKa0s/LibKa0s.xml` | `<Script file="Glow.lua"/>` **after `Item.lua`, before `Media.lua`**, with the other single-file leaf majors. Appending at the end also works. `tests/majors.lua` must use the same position. |
| `tests/majors.lua` | `{ major = "LibKa0s-Glow-1.0", files = { "Glow" }, primary = "Glow" }`, in the same slot. |
| `MODULES` | `lib.MODULES.Glow = MINOR` (above). In-game check: `LibStub("LibKa0s-Glow-1.0").MODULES` → `{ Glow = 1 }`. Version key `<Glow>`. |
| `LibKa0s/DebugLogDiagnostics.lua:80-83` | The hard-coded `MAJORS` name list feeds the diagnostics identity header (`runningMinors`). **Add `"Glow"`** (in the majors.lua slot), or the report silently omits a running major. That is a released change to the file, so `DIAG_MINOR` 2 → 3. Coordinate with the v1.75.0 stale-icon-comment edit to `DebugLog.lua`, so the DebugLog major gets one new version key (e.g. `20.3.1`) and one new `docs/api/DebugLog/version-…-docs.md`, not two. **Add a test** that this list equals the names in `T.majors`: no gate covers it today (no test references `runningMinors`), and it will drift again when Sim-1.0 lands in the same release. |
| `CHANGELOG.md` v1.75.0 | Version block gains `Glow` 1 (and the new DebugLog key). Add a `### LibKa0s-Glow-1.0 (new major, Glow minor 1)` section with the contract, the traps, the adopters, and "What a consumer owes": nothing until it adopts. Re-vendoring makes the file arrive, and a host that never wires it carries a few KB of never-executed code (library-stack-§7). There is no `Kit.VERSION` change. The kit is not touched by this item (kit 41 comes from #46/#47). |
| `tools/gen-api-members.lua` | Run it to produce `docs/api/Glow/members-1.json` (`Start`, `Stop`, both functions). Never hand-edit. |
| `docs/api/Glow/version-1-docs.md` | New. Header table (Major, File, Requires `LibKa0s-Core-1.0` ≥ 1, *Optional at call time:* `LibCustomGlow-1.0`, no floor), Members, the mapping table, the seven traps, "Adopting it" (the setup seam and stub, §4), and "What is not here" (§7). |
| `docs/api/README.md` | Version-key row `| LibKa0s-Glow-1.0 | <Glow> | LibStub("LibKa0s-Glow-1.0").MODULES |`, and a `### LibKa0s-Glow-1.0` section `| [1](./Glow/version-1-docs.md) | Glow.lua 1 | v1.75.0 | **Current** |`. |
| `README.md` | Module bullet list (~:36), the majors table (~:111), the `MODULES` paragraph (~:243), the "every major except Core … resolves Core" list (~:266), and the layout tree (~:285, `Glow.lua -- LibKa0s-Glow-1.0, MINOR at the top of the file; needs Core`). |
| `docs/releasing.md` consumer table (~:455-470) | Row `LibKa0s-Glow-1.0 | DropWatcher, KickCD, QuickComms | core/GlowSetup.lua (all three), as NS.GlowLib`. |
| `docs/api/CONSUMERS.md` | Restamp at the v1.75.0 census re-run: two exports, both with three callers. |
| `tests/run.lua` (:49 area) | Optional: publish `glow = mocks.LibStub("LibKa0s-Glow-1.0")` only if the new suite wants it through `T`. |

### `tests/test_glow.lua` (headless, with a fake LCG)

The fake is registered on the instance's LibStub (as DW and QC's tests do: `m.LibStub:NewLibrary("LibCustomGlow-1.0", 24)`). Each `_Start` and `_Stop` records `{ name, n = select("#", ...), ... }`. Every case says what turns it red.

1. **Absent LCG:** `Start` → `false` for all four styles, `Stop` with and without a style does not raise, and nothing is recorded. *Red under:* a load-time capture or an unguarded `L.X`.
2. **Call-time resolution:** the Glow module loads with no LCG, the fake is registered afterwards, and `Start("pixel")` reaches it. *Red under:* `local L = LibStub(LCG, true)` at file load (KickCD's current shape).
3. **Pixel vector:** with every knob set, all 11 positions are asserted, including `key` at 10 and `frameLevel` at 11.
4. **`pixelLength`:** 0, -3, `"6"` and `nil` each give `nil`. 6 gives 6.
5. **Booleans:** `pixelBorder` false gives `false`. `true`, `nil` and `"x"` give `true`. The same holds for `procStartAnim` via the options table.
6. **Numeric type guard:** `pixelLines = "8"` gives `nil`, and so do `xOffset = "3"` and `procDuration = {}`.
7. **AutoCast vector** (9 positions) and **Button vector** (4 positions, with no key in position 4: `frameLevel` is there).
8. **Proc:** the options table is not `knobs` (`rawequal` false), `getmetatable(knobs) == nil` after the call, the table is new per call (two calls give two tables), and its fields are as in the mapping table. `nil` knobs give absent fields except `startAnim = true`.
9. **`knobs == nil`** and **`knobs = "x"`**: every positional slot is `nil` and the call still happens.
10. **Unknown style** (`"Pixel"`, `"action"`) and **nil frame**: `false`, and no call.
11. **Missing member:** a fake without `ProcGlow_Start` / `ProcGlow_Stop` gives `Start("proc")` → `false`, `Stop(f, "proc", k)` is a no-op, and `"pixel"` still works.
12. **Stop:** `Stop(f, "pixel", "K")` records exactly `PixelGlow_Stop(f, "K")`. `Stop(f, "button", "K")` records `ButtonGlow_Stop(f)` with `n == 1`. `Stop(f, nil, "K")` records all four in order. `Stop(f, "bogus", "K")` records nothing.
13. **Stateless:** `Start` never records a `_Stop`, and repeated `Start` calls record repeated `_Start` calls (no gate).
14. **Surface:** `test_versioning` already compares `members-1.json` against the live module. Add a lint-style assertion that `Glow.lua` names no `LibStub(...)` outside `lcg()` and the Core probe.

The generic suites (`test_versioning`, `test_loader`) cover the floor: Core absent or too low means the major is not registered, because they iterate `T.majors`.

## 4. Host seam and degradation stub

Each adopter gets **`core/GlowSetup.lua`**, published as **`NS.GlowLib`**. `NS.Glow` is already DW and QC's host lifecycle module, and the same name is used in all three hosts:

```lua
local _, NS = ...
-- core/GlowSetup.lua — the LibKa0s-Glow-1.0 seam (library-stack-§7). Absent major: no glow, the
-- same thing an absent LibCustomGlow-1.0 already means here. Never a local copy of the mapping.
local G = LibStub and LibStub("LibKa0s-Glow-1.0", true)
NS.GlowLib = G or {
    Start = function() return false end,
    Stop  = function() end,
}
```

- **Stub expectation:** a member-answering default with the live surface (`Start`, `Stop`). It must **not** carry a START/STOP table: that would be the fork, anti-patterns #47. Each host's `tests/test_surface_parity.lua` gains `T.assertSurfaceParity(degraded.GlowLib, "LibKa0s-Glow-1.0")` with an empty ignore set.
- It stays silent, as every existing `*Setup.lua` stub in these hosts is (DW/QC/KickCD `PoolSetup.lua`). KickCD keeps its `OPTIONAL_LIBS` at-enable line for LibCustomGlow-1.0 (DebugLogSetup.lua:247-249) unchanged, because the player-facing degradation is still "no icon glows".
- **TOC:** the file goes after the libs block and the LibKa0s line, and before its only caller (`modules\Glow.lua` in DW and QC, `modules\IconGrid_Render.lua` in KickCD), with a one-line position comment in each TOC's style (e.g. KickCD's `# The LibKa0s-Pool-1.0 seam. Anywhere after the libs block and before …`).
- **Every host keeps vendoring `libs/LibCustomGlow-1.0/`** and keeps it in `## OptionalDeps`. The LibKa0s payload cannot carry a consumer-vendored third-party lib (library-stack-§6/§7), and the driver only resolves it. QC.toc:32's comment changes from "modules\Glow.lua resolves it at call time" to "LibKa0s-Glow-1.0 resolves it at call time". DW.toc:349 and the three `DEPENDENCIES.md` LCG paragraphs get the same pointer.

## 5. Knob ranges: decision is **do not publish** (agrees with the challenger)

Reasons, strongest first:

1. **The ranges are UI policy, not LCG facts.** LCG accepts any `N > 0`, any frequency (a negative one runs backwards, :272-279), any thickness and any length (clamped to the frame by LCG itself, :284). `1..20` lines and `0.05..2` frequency are the owner's slider choices from KickCD's feedback-21 table. A published range is additive-only forever: widening one slider in one addon would either need a library release or fork the range.
2. **No host table is saved.** Every host still needs its own table for defaults (KickCD `PixelFrequency` 0.25 against DW/QC 0.1, an owner decision at DW defaults/Profile.lua:24-26), key spelling (PascalCase `leaf` against camelCase `key`), kind vocabulary (`number`/`bool` against `slider`/`bool`), labels, tips and order (DW offsets first per feedback-24, QC on DW's older order, KickCD button first). With all of that stripped, 13 rows of min/max/step are low-content data, and "MUST NOT promote on frequency alone" (library-stack §7 bars) keeps it inline.
3. **Clamping is host safety policy.** KickCD clamps every read (`knobValue`, IconGrid_Render.lua:417-430) because a hand-edited 900-line pixel glow freezes the client. That is a default and a policy, which the owner excluded. It stays in KickCD. DW and QC rely on their schema's write validation. A shared clamp would be a behaviour change for DW and QC.
4. **The drift risk is already covered.** Each host's own suite pins its ranges (KickCD test_icongrid_glow_knobs.lua; DW test_schema_rows.lua:222-224; QC's schema tests). A library range table adds a cross-repo join and protects nothing extra at runtime.

**Re-check trigger** (recorded in the API doc's "What is not here" and in the #56 closing comment): a fourth consumer copies the knob table, or one host edits a range and the others do not.

## 6. Line-by-line verification of the three hosts, and every divergence

Sources: DW `modules/Glow.lua` (185 lines): `lib()` :45, `num` :91, START :93-114, STOP :116-121, `Stop` :137-142, `Apply` :149-172. QC `modules/Glow.lua` (236 lines): `lib()` :50, `num` :52, START :55-76, STOP :78-83, `Stop` :95-100, `start` :103-116, `stopButton` :191-197, `Button` :200-208. KickCD `modules/IconGrid_Render.lua` (934 lines): `local LCG` :347, `LCG_KEY` :374, `StopGlow` :388-396, `readKnobs` :432-442, `startEffect` :448-470, `StartGlow` :474-507. DW and QC START/STOP are identical except that QC threads `key`. QC is a declared copy of DW (QC Glow.lua:3).

| # | Aspect | DW | QC | KickCD | Driver | In-game change? |
|---|---|---|---|---|---|---|
| 1 | LCG resolution | call time (:45) | call time (:50) | **file load** (:347) | call time | None. LCG loads before every addon file (KickCD.toc:31 libs block). It is a headless gain: no load-time capture. |
| 2 | `pixelLength` | `num(v,0)`, `>0 and v or nil` | same | `== 0 → nil`, raw otherwise (clamped 0..20) | `>0` number else nil | None. KickCD's clamp makes negatives impossible, and the two expressions agree on 0..20. |
| 3 | `pixelBorder` | `== true` | `== true` | raw (clamped boolean, default true) | `~= false` | **None reachable.** It differs only for `nil` or a non-boolean truthy value: DW/QC today give no border, the driver gives a border (LCG's own nil meaning). DW reads through `NS.Setting`, which falls back to the schema default `true` (settings/Schema.lua:165-169). QC's `glowConfig` backfills `knob.default` (`true`) for nil (IconStyle.lua:65-68). Only a hand-edited SavedVariables value such as `"yes"` reads differently. Recorded and accepted. |
| 4 | `procStartAnim` | `~= false` | `~= false` | raw (clamped boolean) | `~= false` | None. |
| 5 | `xOffset`/`yOffset` | `num(v,0)` | same | raw (clamped number) | `num(v)` → nil → LCG 0 (:287-288, :422-423; proc `__index` 0) | None. Same number. |
| 6 | `procDuration` | `num(v,1)` | same | raw | `num(v)` → nil → LCG `__index` 1 | None. DW's test asserts `.duration == 1` from its profile value 1, which still passes. |
| 7 | Other numerics | `num(v)` | `num(v)` | raw (clamped) | `num(v)` | None. |
| 8 | `frameLevel` | 2 on all four styles | 2 on all four | **none** (LCG 8, over its own `+5` child, :272-274) | 5th argument, host-supplied | None. Each host passes what it passes today. |
| 9 | Button arg count | 4 | 4 | **3** | 4 (`nil` frameLevel for KickCD) | None. LCG reads `frameLevel or 8`. KickCD's test records `n` and never asserts it. |
| 10 | Pixel/AutoCast arg count | 11 / 9 | 11 / 9 | **10 / 8** | 11 / 9 | None, for the same reason. |
| 11 | Proc options | fresh table, `frameLevel = 2` | same | fresh table, no `frameLevel` | fresh table, `frameLevel` field only when given | None. |
| 12 | Stop shape | the recorded style (`STOP[b.glowStyle]`) | the recorded style | **all four, unconditionally** | `style` given → one; `nil` → all four | None, **if DW keeps its guard** (see DW migration). DW's `Stop` gates on `glowKind`, not `glowStyle`. If `glowStyle` were nil, the driver's `nil` would mean stop-all where DW stops nothing today. That is unreachable (`cfg.type` falls back to a schema default), but the migration must pass the style only when non-nil. QC already guards on `qcGlowStyle` / `qcButtonGlowStyle`. |
| 13 | Unknown style | no start; state recorded | no start; state recorded | no start; **state recorded** (`_glowKind = kind`) | `false` | None reachable (schema-validated dropdowns). KickCD gating on the return would not record state for an unknown kind, which only means a re-attempt per update. |
| 14 | Colour | `cfg.color` array, per generation | `g.color` array, per build | fresh `{r,gr,b,a}` per restart | by reference (trap 4) | None. |
| 15 | Per-start allocation | proc table | proc table (+ Perf brackets) | proc table **and a closure `k` every start** | proc table only | KickCD allocates slightly less. |

**Verdict: no behaviour change visible in game** for any state reachable through the UI or defaults, in any of the three hosts. The only semantic delta is row 3, which is limited to corrupt SavedVariables. The existing glow suites in all three hosts assert the exact LCG argument vectors and serve as the characterization. They must pass **unchanged** across the migration commit.

## 7. "What is not here" (API doc section, with where each thing lives)

| Not in Glow-1.0 | Stays in | Re-check trigger |
|---|---|---|
| Defaults for any knob | each host's profile (savedvariables-§2) | never: owner decision |
| Knob ranges / catalog (`KNOBS`) | each host's schema rows | a fourth copy, or one range edited alone (§5) |
| A `STYLES` list | each host's localized dropdown | a host that needs the list without labels |
| Lifecycle: the unchanged-repaint gate (DW kind+gen+width, QC `sig`, KickCD knobs+colour), Apply/Release/StopFree | hosts' `modules/Glow.lua` and `IconGrid_Render.lua` | bar 1 fails today (three different gates) |
| Proc burst spend (`f["_ProcGlow"..KEY].startAnim = false`, DW :129-133, QC :87-92) | DW and QC | never in the library: it writes LCG `__` internal state (LCG :858/:921), bar 3 |
| Triggers (DW trade/upgrade, QC always/hover/send, KickCD ready/casting/interruptible + alpha mask) | hosts | — |
| Class-colour resolution | hosts (`NS.ResolveColor`, options-ui-§17) | — |
| Stop-before-start | hosts | — |
| `O.GlowGroup` composer | hosts' settings | rejected #56 |
| `Available()` | `LibStub("LibCustomGlow-1.0", true)` in the host if it needs to know | — |
| Clamping | KickCD `knobValue` | — |

## 8. Per-host migration (one commit each after the v1.75.0 re-vendor; luacheck 0/0 and `lua tests/run.lua` green before and after; existing glow assertions untouched)

### DropWatcher (`modules/Glow.lua`, 185 lines → about 150)

- **Delete:** `lib()` (:45), `num` (:91), `START` (:93-114) and `STOP` (:116-121).
- **Change:**
  - `Glow.Stop` (:137-142) becomes `if b.glowStyle then NS.GlowLib.Stop(b, b.glowStyle, Glow.KEY) end`. Pass the style only when non-nil (divergence 12).
  - `Glow.Apply`'s start becomes `NS.GlowLib.Start(b, cfg.type, cfg, Glow.KEY, Glow.FRAME_LEVEL)`. `cfg` is passed whole: it already holds `color` and the 13 knobs under the contract names, and its extra `enabled`, `type` and `useClassColor` fields are ignored.
  - The header's HEADLESS paragraph points at the seam, and the "modeled START/STOP" wording goes.
- **Stays:** `KEY`, `FRAME_LEVEL`, `KINDS`, `KindOf`, `read`/`config`/`gen`, the kind+gen+width gate, `spendBurst`, `StopFree` and `Refresh`. The recorded `glowKind`/`glowStyle` keep being written regardless of LCG presence, so test :94 still passes.
- **New:** `core/GlowSetup.lua`, a TOC line, and a parity case in `tests/test_surface_parity.lua`.
- **Tests:** `tests/test_glow.lua` stays unchanged. Its fake LCG on `m.LibStub` is reached by the driver's call-time lookup. This includes the :221 test that swaps `ProcGlow_Start` on the same table, because the driver re-reads the member every call.

### QuickComms (`modules/Glow.lua`, 236 lines → about 200)

- **Delete:** `lib()` (:50), `num` (:52), `START` (:55-76) and `STOP` (:78-83).
- **Change:**
  - `Glow.Stop` (:95-100) becomes `NS.GlowLib.Stop(btn.qcIconFrame, btn.qcGlowStyle, Glow.KEY)`. It is already guarded on `qcGlowStyle`, and the nil frame is guarded by the driver.
  - `start` (:103-116) becomes `NS.GlowLib.Start(btn.qcIconFrame, g.type, g, Glow.KEY, Glow.FRAME_LEVEL)` inside the existing `Perf.Note("glowStart")` bracket.
  - `stopButton` (:191-197) and `Glow.Button` (:200-208) change the same way on `btn.qcEdge` with `Glow.BUTTON_KEY`.
- **Stays:** both keys on two frames, `FRAME_LEVEL`, `SEND_SECONDS`, `spendBurst`, `Wants`, `Update`, `Bind`, `SetHover`, `Sent`, `Shown`, `Release`, `ReleaseFree`, the stand-down hook and the `sig` gate.
- **New:** `core/GlowSetup.lua`, a TOC line, the TOC :32 comment update, and a parity case.
- **Tests:** `tests/test_glow.lua` stays unchanged.

### KickCD (`modules/IconGrid_Render.lua`, 934 lines → about 905)

- **Delete:** `local LCG = LibStub(...)` (:347), `KNOB_INDEX` (:406, :410), `startEffect` (:448-470) and the four direct LCG stops (:393-396).
- **Change:**
  - Build `FIELD[i] = leaf:sub(1,1):lower() .. leaf:sub(2)` once, beside `KNOB_KEYS` (:405-411). `readKnobs` (:432-442) then writes `vals[FIELD[i]]` instead of `vals[i]`. The table is still the icon's own `self._glowKnobs`, made once, so there is no new allocation.
  - `StopGlow` (:388-396) becomes `local g = self.glow; if not g then return end; NS.GlowLib.Stop(g, nil, LCG_KEY); self._glowKind, self._glowColor = nil, nil`. Stop-all is safe because `g` is KickCD's own child frame (trap 5).
  - In `StartGlow` (:474-507), the `if not (g and LCG)` gate becomes `if not g then return end`. Then come the colour resolve, the knob read and the unchanged idempotency gate, then `self:StopGlow()`, `vals.color = c` (fresh `c` as today), and `if not NS.GlowLib.Start(g, kind, vals, LCG_KEY) then return end`, and finally `_glowKind` and `_glowColor` as today. There is no fifth argument: LCG keeps its 8. When the return is `false` (LCG absent), no state is recorded, which is today's outcome. The early-exit position moves, with no visible effect (divergence 13).
- **Stays:** the `LCG_KEY` and its long comment (re-pointed: "the driver's Stop/Start take the key"), `unpackGlowColor`, `knobValue` clamp, `Const.GLOW_KNOBS`, triggers, `applyInterruptibleMask`, the `+5` glow child, `IconGrid.lua:237`'s pool-release `StopGlow`, and the DebugLogSetup `OPTIONAL_LIBS` line.
- **New:** `core/GlowSetup.lua`, a TOC line after `core\PoolSetup.lua` (the same "before modules\IconGrid*" constraint), and a parity case.
- **Tests:**
  - `tests/test_icongrid_glow_knobs.lua` stays unchanged. Its positional assertions (:164-235) and proc-options assertions (:190-192) are exactly the driver's output. Its `T.load` hook injects the recording LCG into `mocks.__libs`, which the kit LibStub reads at call time.
  - `test_flow_traces.lua:322-330` (LCG absent) stays unchanged.
  - **Add one case:** "StopGlow stops all four styles under the KickCD key, the button style keyless". The current suite records `_Stop` calls as no-ops, so stop-all is not pinned today.

### Review check for all three

Run `grep -rn "Glow_Start\|Glow_Stop" --include='*.lua' . | grep -v '/libs/\|tests/'` in each host. It must return nothing after migration. That proves there is no residual host mapping (no fork).

### Owner smoke checks (owed; never marked passed by the executor)

- **DW:** each of the four styles on the Drops row, the compact card and the detail header, for main and off-spec. The proc burst plays once.
- **QC:** the icon glow in each style × always/hover/send on pad and dial, the button glow on pad buttons, and hover in combat.
- **KickCD:** the ready glow in each style for the primary and secondary slots, a knob slider change restarting the glow, and the interruptible-only trigger hiding uninterruptible casts.

## 9. Standard ripple (v2.86.0)

**library-stack-§2, a new row** (after LibDeflate). It is kept short, per the challenger's note on §2's `Lib | When` cells:

`| LibCustomGlow-1.0 | any addon that draws a button, proc, pixel or autocast glow; driven through LibKa0s-Glow-1.0 (library-stack-§7), which resolves it with LibStub(…, true) at call time — absent, no glow |`

The headless-suite claim stays out of the row.

**library-stack-§7, module table:** a new row in `tests/majors.lua` order (after `Item`):

`| LibKa0s-Glow-1.0 | Glow.lua | the stateless LibCustomGlow-1.0 driver: Start(frame, style, knobs, key, frameLevel) and Stop(frame, style, key) map one of the four styles (button, proc, pixel, autocast) and its knob values to LCG's positional arguments, with LCG's two traps handled (pixelLength 0 → nil; a boolean is false only when false). It resolves LibCustomGlow-1.0 at call time and does nothing without it. No defaults, no ranges, no lifecycle: the unchanged-repaint gate, the proc burst and the triggers stay the host's. Ships from LibKa0s v1.75.0 (Glow minor 1); adopters DropWatcher, QuickComms, KickCD |`

**§7 counts paragraph:** "fifteen LibStub majors across thirty-four files" is already stale (the XML has 36 `<Script>` lines at `d9f9454`). Restate the figures by **recount at the v1.75.0 release commit**: `grep -c 'major = "LibKa0s-' tests/majors.lua` and `grep -c '<Script file=' LibKa0s/LibKa0s.xml`, never by increment. Glow contributes +1 major and +1 file. Sim-1.0, and any new Widgets secondary files for SearchBox and TestStrip, land in the same release and must be counted by the same commands. Add a v1.75.0 clause to the running history in the paragraph's style.

**§7 inter-module dependencies:**
- "Fourteen of the fifteen majors floor on Core" and "ten of those fourteen gate on it without calling a single member" become recounted figures. Glow joins the **member-free** list beside `Env`, `Compat`, `Lifecycle`, `Bus`, `Schema`, `Pool`, `Item`, `Media`, `Launcher` and `Options`.
- Add one sentence beside the Bus/AceEvent precedent: "`LibKa0s-Glow-1.0` resolves `LibCustomGlow-1.0` at call time and answers `false` without it, declaring no floor: the payload cannot contain a consumer-vendored lib (library-stack-§6), so there is nothing to floor on, and the §2 row is what lists it."

**§7 fork sentence:** after "Hand-rolling any of these … is forking the toolkit (anti-patterns #47)", add "from v2.86.0 that includes a host START/STOP table over LibCustomGlow-1.0".

The standard changelog line goes in v2.86.0 together with the owner's other v2.86.0 items. No playbook or anti-pattern range changes are needed beyond the #47 mention.

## 10. Order inside the run

1. LibKa0s: `Glow.lua`, XML, majors.lua, `tests/test_glow.lua`, the DebugLogDiagnostics list, its minor bump and new test, the generated manifest, the API docs, README, releasing.md and CHANGELOG. Green gate.
2. The v1.75.0 release, together with the other v1.75.0 items. The census restamp follows.
3. Re-vendor DW, QC and KickCD, then one migration commit each (seam, TOC, host edit and parity case). Their existing glow suites stay unchanged and green.
4. The standard v2.86.0 rows (in parallel with step 1, cited by the CHANGELOG).
5. Close #56's driver half as done. Its other candidates are already closed as rejected (the owner's decision 4).
