# Design spec: `LibKa0s-Compat-1.0` (minor 1, target LibKa0s v1.55.0)

Status: DESIGN (CP-3 delegated; conservative reading taken wherever the evidence split).
Standard: WowAddonStandards v2.63.0. Governing rules: `library-stack-§7` (the three promotion bars,
one major per module, Core floor, additive-only, API document per version), `compat`, `testing-§8`
(degraded cases reached by removing the API, never by stubbing the member under test).
Evidence: harvest `2026-09-22` findings C2-F01 (Compat), C2-F04 -> C3-F08 (secret seam, narrowed).

Verdict: **viable, as a narrow major of nine members.** The wide extraction (the union of the nine
copies) stays rejected, for the reason `LibKa0s/Env.lua:11-14` already records.

---

## 1. Measurements (all taken from the tree on 2026-09-23)

| Copy | Lines | Members that map onto this major | Lines those members occupy (function + doc block) |
|---|---:|---|---:|
| `AuraMaster/core/Compat.lua` | 328 | GetSpellInfo (`:312-328`) | 17 |
| `KickCD/core/Compat.lua` | 496 | GetSpellCooldown (`:64-92`), GetSpellTexture + GetSpellInfo (`:146-174`), GetSpecialization + GetSpecializationInfo (`:253-270`) | 76 |
| `MultiMeters/core/Compat.lua` | 777 | GetSpellInfo + GetSpellTexture (`:39-70`), spec pair (`:95-112`) | 50 |
| `ConsumableMaster/core/Compat.lua` | 83 | spec pair (`:16-33`), IsSecret + GetSpellName (`:53-83`) | 49 |
| `LootHistory/core/Compat.lua` | 411 | GetSpellName (`:80-87`) | 8 |
| `WhatGroup/core/Compat.lua` | 161 | GetSpellName + GetSpellTexture (`:25-51`), GetSpellCooldownTimes (`:113-127`) | 42 |
| `BankLedger/core/Compat.lua` | 175 | none | 0 |
| `PanelMaster/core/Compat.lua` | 173 | none | 0 |
| `PartyFrameEnhanced/core/Compat.lua` | 216 | IsSecret (`:11-16`) | 6 |
| **Nine Compat copies** | **2820** | | **248** |
| `AuraMaster/core/Secrets.lua` (not a Compat file) | 79 | IsSecret + CanAccess (`:33-50`), IsSafeKey (`:71-79`) | 27 |
| `MultiMeters/core/Secrets.lua` (not a Compat file) | 325 | IsSecret + CanAccess (`:144-171`), IsSafeKey (`:201-227`) | 55 |

- The collection has exactly nine `core/Compat.lua` files (`find -maxdepth 3 -name 'Compat*.lua'`
  outside `libs/`, excluding the non-Ka0s `Outfitter/`). AbsorbTracker and PrettyChat have none.
- **248 of 2820 lines** in the nine copies map onto this major; with the two `Secrets.lua` seams the
  total is **330**. The harvest's "~400 genuinely duplicated" is not reproduced: the other ~70 it
  counted are shapes excluded below (interpolation enum, rule formatter, cast readers).
- KickCD has **12** inline `_G.issecretvalue(` call expressions and no seam: 3 in
  `core/Compat.lua` (`:86`, `:380`, `:393`) and 9 across four feature modules
  (`modules/Castbar_Debug.lua:95`, `modules/Cooldowns.lua:122, 251, 252, 289, 290`,
  `modules/IconGrid.lua:334, 1186`, `modules/Castbar.lua:303`).

### Production consumers per member (library-stack-§7 bar 1)

| Member | Consumers with a production caller | Evidence |
|---|---|---|
| `GetSpellInfo` | AuraMaster, KickCD, MultiMeters (3) | AM `modules/CastAura.lua:72`, `settings/GeneralSpells.lua:256, 1247`; KickCD `core/KickCD.lua:575-609`, `modules/Cooldowns.lua:105, 692`, `modules/IconGrid.lua:315`, `settings/Spells.lua:260, 281`; MM `modules/DrillDown.lua:550`, `modules/Tooltip_Lines.lua:661` |
| `GetSpellName` | ConsumableMaster, LootHistory, WhatGroup (3) | CM `modules/KCMItemRow.lua:85`, `modules/MacroBarFlyout.lua:332`, `modules/MacroManager.lua:55`, `settings/CategoryAddByID.lua:69`; LH `modules/Attribution.lua:64, 293`; WG `modules/Frame.lua:521` |
| `GetSpellTexture` | KickCD, MultiMeters, WhatGroup (3) | KickCD `modules/IconGrid.lua:333`, `settings/Spells.lua:268`; MM `modules/Tooltip_Builders.lua:134`; WG `modules/Frame.lua:522` |
| `GetSpellCooldown` | KickCD, WhatGroup (2) | KickCD `modules/Cooldowns.lua:149, 428`, `modules/IconGrid_Render.lua:381`; WG `modules/Frame.lua:830` (Times), `core/WhatGroup.lua:678`, `modules/Frame.lua:487, 510` (Remaining) |
| `GetSpecialization`, `GetSpecializationInfo` | KickCD, ConsumableMaster (2); MultiMeters defines both with **no production caller** | KickCD `core/Util.lua:202-207`; CM `core/SpecHelper.lua:41-44`; MM reads `_G.GetSpecialization` directly at `modules/Roster.lua:187` instead |
| `IsSecret` | ConsumableMaster, PartyFrameEnhanced, AuraMaster, MultiMeters (4); KickCD inline x12 | CM `core/MacroDisplay.lua:139`; PFE `modules/StandIn.lua:45`, `modules/TargetFrames.lua:82`, `modules/UnitButtons.lua:78`, `modules/RangeFade.lua:73-117`, and nine uses inside its own Compat; AM via `core/Secrets.lua`; MM `modules/Aggregator.lua:723-833`, `modules/Provider.lua:496, 509`, `modules/Aggregator_Identity.lua:118-120` |
| `CanAccess` | AuraMaster, MultiMeters (2) | AM `modules/Anchors.lua:299`; MM `modules/Aggregator.lua:579`, `modules/Export.lua:195, 359, 445`, `modules/Format.lua:587, 645, 735` |
| `IsSafeKey` | AuraMaster, MultiMeters (2) | AM `modules/TimedSpells.lua:71, 112`; MM `modules/Feign.lua:153-341`, `modules/Aggregator.lua:833`, `modules/DrillDown.lua:222`, `core/Diagnostics*.lua` |

Every member clears bar 1. Bar 2 (no per-consumer flags): no member takes a behavior flag. Bar 3
(stable abstraction): every member is a ladder over an API Blizzard has already moved once
(`C_Spell` in 11.0, `C_SpecializationInfo` in 12.0) or a 12.0 global that is the client's own
definition of the question (`issecretvalue`, `canaccessvalue`).

---

## 2. The member list

Nine stateless lib-level functions, plus the bookkeeping every major carries (`MAJOR`, `MINOR`,
`MODULES = { Compat = 1 }`). Everything is read off the LibStub table; nothing is instance-shaped.

### 2.1 Rules every member obeys

1. **Globals are read BARE and at CALL time** (`C_Spell`, never `_G.C_Spell`, and never captured
   into an upvalue at load). The kit loader resolves a bare name through the mock table first and
   `_G` second (`testkit/loader.lua:12-24`); an explicit `_G.` lookup steps around the mock
   (`BankLedger/core/Compat.lua:133-136` records the same trap). Call-time reads are what let a
   suite remove a rung after load and see the ladder move.
2. **Rung order is namespaced first, deprecated global second, absent answer last.** "Absent" means
   the namespace or the function is not there (`type(x) ~= "function"` is not required; a presence
   test `ns and ns.fn` is the house shape, matching `Env.lua:60-68`).
3. **Authority.** For `GetSpellInfo`, `GetSpellTexture`, `GetSpellCooldown`, `GetSpecialization`,
   `GetSpecializationInfo`: the **first rung that EXISTS is authoritative** -- a nil from it is the
   answer and the next rung is not consulted. For `GetSpellName` alone: the **first rung that
   ANSWERS** wins (a nil or plain `""` falls through). See judgement J3 for why the one member differs.
4. **A value that may be secret is returned untouched.** Spell names, cooldown timings and modRate
   are never compared, formatted or used in arithmetic. The operations the library does perform on
   client values are: `type()` (legal on a secret); `x or default` on a timing or modRate (truthiness
   of a secret number is legal -- only a secret BOOLEAN may not be tested,
   `AuraMaster/core/Secrets.lua:13`); `n == ""` only after `IsSecret(n)` is false; `d > 0` only after
   `type(d) == "number" and not IsSecret(d)`; and `info.isEnabled ~= false` / `info.isActive == true`,
   inherited unchanged from KickCD and WhatGroup. KickCD `core/Compat.lua:61-62` records
   `isActive` as the plain boolean it gates on in combat; that `isEnabled` is plain is shipped
   behavior in both copies rather than a recorded measurement, and the API document says so.
5. **Identifier domain.** Spell members accept a `number` or a `string` (the client's
   `spellIdentifier` accepts an id, a name or a link, and KickCD resolves typed names through
   `GetSpellInfo(input)` at `settings/Spells.lua:281` and `core/KickCD.lua:580`). Any other type,
   including `nil`, answers the member's no-answer value **without calling any rung**. `type()` on a
   secret is legal, so the guard is secret-safe.
6. **No pcall** around client calls. None of the nine copies wraps these readers, and adding it
   would turn a client defect into silence; the single exception in the collection (MM's death-recap
   readers) is host-specific and excluded.
7. **Arity is exact.** Where the client returns more than the contract, the library truncates with
   parentheses or explicit locals, so a caller passing the result as the last argument of a C call
   (`SetTexture`, `SetCooldown`) never forwards a stray value.
8. **Internal calls go through file locals, never back through `lib.X`** (added at build). The LibStub
   table is shared by every addon that loaded the copy; one host replacing `lib.IsSecret` must not
   change what another host's `GetSpellName` answers. Pinned by case 49.

### 2.2 Members

| # | Signature | Returns (arity) | Ladder | All rungs absent | Bad input |
|---|---|---|---|---|---|
| 1 | `IsSecret(v)` | `boolean` (exactly 1) | `issecretvalue(v) and true or false` | `false` | none; any value, including nil |
| 2 | `CanAccess(v)` | `boolean` (exactly 1) | `canaccessvalue(v) and true or false`; else `not IsSecret(v)` | `true` | none |
| 3 | `IsSafeKey(v)` | `boolean` (exactly 1) | `IsSecret(v)` -> `false`; else `v ~= nil` (IsSecret, NOT CanAccess). Built order: the secret test runs FIRST so a secret never meets `== nil`; the answer is identical on every input to the copies' `v == nil`-first order | `v ~= nil` | none |
| 4 | `GetSpellInfo(id)` | hit: `name, iconID, castTime, minRange, maxRange, spellID` (exactly 6); miss: `nil` (exactly 1) | `C_Spell.GetSpellInfo(id)` table flattened, authoritative; else global `GetSpellInfo(id)` **remapped** from its real shape `name, rank, icon, castTime, minRange, maxRange, spellID` (rank dropped) | `nil` | not number/string -> `nil`, no rung called |
| 5 | `GetSpellName(id)` | `string` or `nil` (exactly 1; may be a secret string) | `C_Spell.GetSpellName(id)` -> `C_Spell.GetSpellInfo(id).name` -> global `GetSpellInfo(id)` first return. A rung answers when its value is secret (returned untouched) or a plain non-empty string; nil or plain `""` falls to the next rung | `nil` | not number/string -> `nil`, no rung called |
| 6 | `GetSpellTexture(id)` | `fileID` or `nil` (exactly 1; the client's second return, `originalIconID`, is dropped) | `C_Spell.GetSpellTexture(id)` authoritative; else global `GetSpellTexture(id)` | `nil` | not number/string -> `nil`, no rung called |
| 7 | `GetSpellCooldown(id)` | `startTime, duration, isEnabled, modRate, isActive` (always exactly 5) | Modern: `info = C_Spell.GetSpellCooldown(id)`; nil info -> inert tuple; else `info.startTime or 0, info.duration or 0, info.isEnabled ~= false, info.modRate or 1, info.isActive == true`. Legacy: `s, d, e, m = GetSpellCooldown(id)` -> `s or 0, d or 0, (e ~= false and e ~= 0), m or 1, active` where `active = type(d) == "number" and not IsSecret(d) and d > 0` | `0, 0, false, 1, false` | not number/string -> inert tuple, no rung called |
| 8 | `GetSpecialization()` | `number` or `nil` (exactly 1) | `C_SpecializationInfo.GetSpecialization()` authoritative; else global `GetSpecialization()` | `nil` | n/a |
| 9 | `GetSpecializationInfo(index)` | the rung's own returns, **unmodified and variable** (client: `specID, name, description, icon, role, primaryStat, ...`); `nil` (exactly 1) on no answer | `C_SpecializationInfo.GetSpecializationInfo(index)` authoritative; else global `GetSpecializationInfo(index)` | `nil` | `not index` -> `nil`, no rung called |

Notes on specific rows:

- **Row 4, the legacy remap is a correction, not a preference.** The deprecated global's second
  return is the rank. AuraMaster remaps and pins it (`AuraMaster/tests/test_compat.lua:496-501`,
  "red under: reading the legacy global's second return (the rank) as the icon"); KickCD
  (`core/Compat.lua:170-172`) and MultiMeters (`core/Compat.lua:53-55`) pass it through raw, and
  their fixtures encode the wrong shape (`KickCD/tests/test_compat_api.lua:221`,
  `MultiMeters/tests/test_compat.lua:77`). Reachable only in a harness or on a client that still
  carries the global.
- **Row 5, secret handling is new and deliberate.** ConsumableMaster compares every rung's answer
  with `""` (`core/Compat.lua:72, 76, 80`); a secret name there raises in combat. The library asks
  `IsSecret` first and returns a secret untouched.
- **Row 7, the `isEnabled` normalization.** The legacy global historically answered `1`/`0`;
  WhatGroup treats `0` as disabled (`core/Compat.lua:106`), KickCD's `e ~= false` reads `0` as
  enabled (`core/Compat.lua:89`). The library takes WhatGroup's reading (J6). The modern rung is
  unchanged from KickCD's (`isEnabled ~= false`), which both copies share.
- **Row 9 keeps the passthrough.** All three copies pass the multi-return through untouched and two
  consumers read positions 1-2; fixing an arity here would be inventing a contract nobody asked for.

### 2.3 What the headless harness answers (the "client with no rungs")

The consumer kit (`testkit/mock_base.lua`) carries **no** `C_Spell`, no `C_SpecializationInfo`,
no `issecretvalue`/`canaccessvalue`, but **does** carry the legacy globals
`GetSpecialization -> 1` and `GetSpecializationInfo -> 250, <spec name>` (`mock_base.lua:1096-1097`).
`tests/_kit/mock_ids.lua`, where a repo opts in, adds `C_Spell.GetSpellInfo` only.

| Member | Answer on a bare kit harness | With `mock_ids` installed |
|---|---|---|
| IsSecret / CanAccess / IsSafeKey | `false` / `true` / `v ~= nil` | same |
| GetSpellInfo | `nil` | 6-tuple for a seeded id (modern rung) |
| GetSpellName | `nil` | seeded name, via the `C_Spell.GetSpellInfo` middle rung |
| GetSpellTexture | `nil` | `nil` |
| GetSpellCooldown | `0, 0, false, 1, false` | same |
| GetSpecialization | `1` (legacy rung) | same |
| GetSpecializationInfo(1) | `250, <spec name>` (legacy rung) | same |

---

## 3. Relation to `LibKa0s-Core-1.0` (no member duplicated)

Core ships `IsConcatSafe(v)` and `SafeToString(v)` (`LibKa0s/Core.lua:52-67`). They answer a
**different question**: whether `table.concat` will accept `v`, probed version-agnostically.
`IsConcatSafe(true) == false` (concat rejects a boolean) while `IsSecret(true) == false`;
`IsConcatSafe` on a secret is `false` and `IsSecret` is `true`; `IsConcatSafe` never consults
`issecretvalue`. Core's comment (`Core.lua:48-51`) chooses the probe over `issecretvalue` for
rendering on purpose, and that choice stands: rendering keeps going through `SafeToString`, and
guards that decide comparability go through this major. The test plan pins the disagreement on a
boolean so nobody later "deduplicates" the two.

The secret trio goes in **this** major, not in Core: `issecretvalue`/`canaccessvalue` are 12.0
globals (version-variant, which is `compat`'s subject), and a Core promotion would raise the Core
floor question for eleven sibling majors (`library-stack-§7`, "A promotion into Core is not free").

---

## 4. Degradation stub story

`library-stack-§7`: the host resolves the major with `LibStub("LibKa0s-Compat-1.0", true)` and falls
back to a stub when it is absent. The library cannot publish its own stand-in (a stand-in would
live in the payload that is absent by definition; `tests/test_surface_parity.lua:10-14`). Two
classes of member need two different stub rules, and the difference is the design:

1. **Readers (members 4-9): the stub answers the all-rungs-absent value from section 2.2.**
   `nil` / `0, 0, false, 1, false`. A degraded install loses spell names, icons and spec, and never
   raises; every caller already handles these values because they are the documented contract. A
   stub that re-implemented the top rung would re-create the duplication this major removes, so it
   is **not** the recommended shape. (AuraMaster's `core/EnvSetup.lua:25-30` does re-implement
   Env's top rung; that precedent is not extended here -- J9.)
2. **Guards (members 1-3): the stub MUST re-implement the one-rung body**, three to four lines each.
   For a guard, "the library is absent" is not "the client has no secrets system": a stub answering
   `IsSecret -> false` on a 12.x client sends a secret into a comparison and raises in combat, on
   exactly the degraded path the stub exists to survive. This is a deliberate, documented
   duplication in the sense of `library-stack-§7`'s Core-promotion paragraph, and the stub MUST
   carry a comment saying so and naming this document.

How the host wires it (the shape Phase 6 applies; the host keeps `core/Compat.lua` as its single
seam, per `compat`, and keeps `NS.Compat.X` as the call surface so every existing call site and
every test monkeypatch keeps working -- e.g. `LootHistory/tests/test_attribution.lua:156-261`
replaces `NS.Compat.GetSpellName` at runtime):

```lua
local CompatLib = LibStub and LibStub("LibKa0s-Compat-1.0", true)

-- Reader: the library, or its documented no-rung answer.
Compat.GetSpellName = CompatLib and CompatLib.GetSpellName or function() return nil end

-- Guard: the library, or the same one-rung body. Deliberate duplication: see
-- LibKa0s docs/api/Compat/version-1-docs.md, "Degradation".
Compat.IsSecret = CompatLib and CompatLib.IsSecret or function(v)
    return issecretvalue ~= nil and issecretvalue(v) and true or false
end
```

No separate "library missing" message: a Compat-only absence can arise only from a partial copy,
which `library-stack-§7` forbids, and a whole-payload absence is already announced by the host's
`core/CoreSetup.lua`.

**Gate.** Each adopter adds a degraded-load case (library files skipped, never the member stubbed,
`testing-§8`) asserting every wired member's answer equals section 2.2's absent column (readers) or
the library's own answer under the same `issecretvalue` fixture (guards). Where a repo wires members
onto one table, `Kit.assertSurfaceParity(NS.Compat, "LibKa0s-Compat-1.0", ignore)` with `ignore`
listing the members it deliberately does not wire; a member added to the major later then fails
parity until the host decides, which is the intended pressure.

**Gate amendment (verify round 1).** That single call runs as written only when two things hold:

- **The runner's surface source answers this name.** The by-name form resolves the live half through
  `Kit.setSurfaceSource`; `Kit.expose` auto-wires the mock's `LibStub` only when the runner
  registered no source. A runner that registers a **table map** MUST add
  `["LibKa0s-Compat-1.0"] = mocks.LibStub("LibKa0s-Compat-1.0", true)` (its own name for the live
  load's mock) to that map, or the by-name call raises `the surface source answers nil ... the live
  surface never loaded`. Measured (grep of each `tests/run.lua`): AuraMaster `:38`, KickCD `:219`,
  MultiMeters `:337`, LootHistory `:110`, WhatGroup `:66`, PartyFrameEnhanced `:39` register a table
  map; ConsumableMaster registers none and auto-wires. Reproduced upstream with a kit probe: a map
  without the row raises exactly that message, a map with it passes.
- **The members sit on the table the call names.** AuraMaster and MultiMeters wire the trio onto
  `NS.Secrets`. Their gate is two calls: `NS.Compat` with `ignore` = the trio plus every unwired
  reader, and `NS.Secrets` with `ignore` = the six readers. A member added later is ignored by
  neither call, so the pressure survives the split.

---

## 5. Deliberately excluded (the rejection record `library-stack-§7` asks to keep)

Recorded in the Compat.lua header and in `docs/api/Compat/version-1-docs.md` "What is not here".

### 5.1 Correctness disagreement (bar "MUST NOT promote a shape whose consumers disagree about correctness")

| Shape | Copies | Disagreement |
|---|---|---|
| Spell known/available | WG `IsSpellKnown` (`core/Compat.lua:70-78`), KickCD `IsSpellAvailable` (`:212-220`) | WG: `C_SpellBook.IsSpellKnown` is final, "a false does not fall through ... either says yes ... hide a disagreement" (`:66-69`). KickCD: `IsPlayerSpell or IsSpellKnown(id) or IsSpellKnown(id, true)` -- exactly the either-says-yes ladder WG forbids. |
| Cast info | KickCD `GetCastingInfo`/`GetChannelInfo` (`:307-355`, `:484-496`), PFE `CastInfo` (`:75-87`) | KickCD returns a record and overrides `notInterruptible` to true for a unit the player cannot attack (`:333-338`); PFE returns the raw flag and a kind with empower detection. Different answers to "is this interruptible". |
| Secret boolean to C-side | PFE `BoolValue`/`AlphaFromBool` (`:121-142`), KickCD `State.ApplyInterruptibleAlpha` (`core/State.lua:109-127`) | PFE gates on IsSecret first; KickCD calls `SetAlphaFromBoolean` ungated on purpose (`KickCD/docs/castbar.md:133`). C3-F08 already refuted this. |
| Cooldown remaining with a GCD floor | WG `GetSpellCooldownRemaining` (`:94-111`) | Pure WG policy (1.5 s floor, `GetTime()` arithmetic on plain values); stays in WG built on member 7. |
| Item resolver | LH `GetItemInfo` (`:144-157`), BL `GetItemDetails`/`ItemNameQuality` (`:153-175`) | Already recorded by `LibKa0s-Item-1.0` (`Item.lua:3-17`): LH guesses, BL refuses. |

### 5.2 Two consumers, but low semantic content (bar "MUST NOT promote on frequency alone")

| Shape | Copies | Why it stays inline |
|---|---|---|
| `Enum.StatusBarInterpolation` read | AM `Interpolation(smooth)` (`:113-117`), MM `BarInterpolation()` (`:774-777`), PFE inline `.Immediate` (`:112`) | The shared content is one enum-member presence read -- the optional-object-guard shape `library-stack-§7` names as the worked example of what not to promote. A library call would add a stub obligation to each host and remove no logic. |
| `C_StringUtil.CreateNumericRuleFormatter` | AM `CreateRuleFormatter(breakpoints)` (`:232-239`), MM `CreateNumericRuleFormatter()` (`:576-580`) | Shared content is a presence guard around one constructor. The non-guard content (AM's pcall and `SetBreakpoints` refusal handling) has one consumer, and the two copies differ on whether a raising constructor propagates (MM) or reads as nil (AM). |

### 5.3 Single consumer (in the nine copies)

- AuraMaster: `HasAuraContainer`, `EnsureAuraContainer`, `AurasAreSecret`, every aura-container
  enum reader, `CreateSecondsFormatter`, `ExpiringTextColor`, `DurationProperty`,
  `CreateDurationBinding`, `BlinkTextColor`, `TimerDirection`, `DispelStyle`, `GetMouseFocus`.
  `core/Secrets.lua`: `IsReadableNumber`, `NumberOr`.
- KickCD: `_firstReturn`, `GetSpellCooldownDuration`, `GetSpellCharges`, `IsSpellUsable`,
  `DebugInterrupt`.
- MultiMeters: the whole `C_DamageMeter` block (`:132-237`), `C_DeathRecap` readers and discovery
  (`:264-513`), `CreateAbbreviatedNumberFormatter`, `GetDefaultAbbreviationBreakpoints`,
  `OpenContextMenu`, `FirstTexture`, `FirstAtlas`, `IsInDelve`, `IsSkyriding`, `IsInHousing`.
  `core/Secrets.lua`: `CanCompare`, `CanCompare2`, `IsSecretTable`, `CanAccessTable`,
  `SafeIterate`, the restriction-state pair.
- ConsumableMaster: `GetNumSpecializationsForClassID`, `GetSpecializationInfoForClassID`.
- LootHistory: `FoldNBSP`, keystone, container/quest hooks, mail, `DecodeGUID`, the bind-state
  scanner (`:159-334`), currency readers.
- WhatGroup: `GetSpellLink`, `GetActivityInfoTable`, `AddOnLinkType`.
- BankLedger: guild name, money, store money, container and guild-bank readers, item resolver.
- PanelMaster: `AddOnFolders`, screen size, UI scale, `InCombat`, LSM media, `MouseIsOver`.
- PartyFrameEnhanced: `IsAddOnLoaded`, `FrameVisible`, `FrameUnit`, `CastDuration`, `ApplyTimer`,
  unit readers (`HealthPercent`, `ClassToken`, `IsPlayer`, `Reaction`), `RaidMarker`,
  `UseRaidStyleParty`.

### 5.4 Library-internal copy left in place

`LibKa0s/Perf.lua:700-714` reads the spec inline (namespaced index rung, legacy info rung). It stays:
making Perf call this major is a new floor for Perf, which `library-stack-§7` calls a breaking change
to the vendoring, and this release is additive-only. See OPEN-2.

---

## 6. Files to create or touch in LibKa0s (all text files CRLF on disk per `.gitattributes`
`* text=auto eol=crlf`; verify with `git ls-files --eol` after staging -- expect `i/lf w/crlf`)

| Path | Change |
|---|---|
| `LibKa0s/Compat.lua` | **New.** Header in the house style (`Env.lua:1-33`): why this exists, why narrow, the rejection record (section 5), the two stub rules. `local core = LibStub and LibStub("LibKa0s-Core-1.0", true); local NEEDS_CORE = 1; if not core or (core.MINOR or 0) < NEEDS_CORE then return end`; `MAJOR, MINOR = "LibKa0s-Compat-1.0", 1`; `lib.MODULES.Compat = MINOR`. Nine `lib.X` functions per section 2. No Core member called. Expected size 250-350 lines; cap 1500. ASCII-only string literals; US English. |
| `LibKa0s/LibKa0s.xml` | Add `<Script file="Compat.lua"/>` immediately after `Env.lua`. |
| `.luacheckrc` | **Added at build (the design omitted it; the linter reports 10 W113 on `Compat.lua` without it).** Top-level `read_globals` gains `"GetSpellInfo", "GetSpellTexture", "GetSpellCooldown", "issecretvalue", "canaccessvalue"` (the other globals Compat reads are already declared for Options/Perf). |
| `tests/majors.lua` | Add `{ major = "LibKa0s-Compat-1.0", files = { "Compat" }, primary = "Compat" }` after the Env row (XML order). |
| `tests/run.lua` | Expose `compat = mocks.LibStub("LibKa0s-Compat-1.0")` in `Kit.expose{...}`; add `"test_compat"` after `"test_env"` in `suites`. |
| `tests/test_compat.lua` | **New.** Section 7. |
| `docs/api/Compat/version-1-docs.md` | **New**, shaped like `docs/api/Env/version-1-docs.md`: header table (Files and minors `Compat.lua` 1, Shipped in v1.55.0, Status Current), what the major is, the nine-row contract table of section 2.2 with the absent column, the harness table 2.3, "Degradation" (section 4, both rules), "Relation to Core" (section 3), "What is not here" (section 5). |
| `docs/api/Compat/members-1.json` | **Generated** by `lua tools/gen-api-members.lua`; never hand-written. Expected members: CanAccess, GetSpecialization, GetSpecializationInfo, GetSpellCooldown, GetSpellInfo, GetSpellName, GetSpellTexture, IsSafeKey, IsSecret. |
| `docs/api/README.md` | Index row (`LibStub("LibKa0s-Compat-1.0").MODULES`) and a `### LibKa0s-Compat-1.0` version table. |
| `README.md` | Major bullet, module table row, MODULES line, file tree line. |
| `CLAUDE.md` | `docs/api/` row's major list gains `Compat`. |
| `docs/releasing.md` | File/minor list (`:26`), major count (`:46`), `NEEDS_CORE` list (`:281`), consumer table row naming the seven intended adopters as "adoption pending" rather than "none yet" (the table's own warning at `:343-344`). |
| `CHANGELOG.md` | v1.55.0 gains the new major. **The v1.55.0 lead paragraph currently says every file's minor is exactly v1.54.2's (`CHANGELOG.md:16`); that sentence becomes false and must be rewritten** (orchestrator). The entry MUST name the re-vendor step every consumer owes (section 8.0). |
| `docs/test-cases.md` | Regenerate with `lua tests/run.lua --list`. |

No existing major's file is edited (additive only). `Env.lua:11-14`'s "the `Compat` extraction ...
rejected" stays true: it describes the wide extraction, which remains rejected.

---

## 7. Test plan: `tests/test_compat.lua`

House shape: `local T = _G.LK_TEST; local compat, mocks = T.compat, T.mocks`. Every case is
fixture-driven through one helper, `with(fixture, fn)`: for each key in `fixture` it saves
`mocks[key]`, installs the fixture value (the sentinel `ABSENT` installs nil), runs `fn` under
pcall, restores every key, and re-raises. Removing a key from `mocks` is genuinely "this client does
not have that API" (`tests/test_env.lua:12-22`). Because `wow_mock.lua` installs `mock_ids`
(which fills `C_Spell.GetSpellInfo`) and `mock_base` installs the legacy spec globals, every spell
and spec case installs its **whole** `C_Spell` / `C_SpecializationInfo` table and states each
global explicitly -- no case relies on what the base happens to carry.

Fixtures used across cases:
- `SECRET` -- a table whose metatable raises on `__eq`, `__lt`, `__le`, `__concat`, `__len`,
  `__index`, `__newindex`, `__call`, with `issecretvalue = function(v) return rawequal(v, SECRET) end`.
  Lua 5.1 raises on `<`/`>` between a table and a number without consulting metamethods, so any
  ordering on it raises; equality across types is silent in Lua 5.1, so "never compared with `""`"
  is pinned structurally by call-order spies (below), not by the metatable.
- `spy(ret...)` -- a function recording its call count and arguments, returning `ret...`.

### 7.1 Registration and shape (3)
1. Major registers; `MINOR == 1`; `MODULES.Compat == 1`; public members are exactly the nine names
   (via `T.publicMembers`).
2. Floor: a fresh mock with no Core loaded -> `LibStub("LibKa0s-Compat-1.0", true) == nil`
   (loaded with `Loader.loadSource` of `Compat.lua` alone, never by stubbing).
3. Source shape: `LibKa0s/Compat.lua` contains no `_G.` or `_G[` (rule 2.1.1), read with
   `Loader.readFile`.

### 7.2 Secret seam (10)
4. IsSecret, no `issecretvalue`: false for `nil`, `0`, `"x"`, `{}`, `true`; each returns exactly one value.
5. IsSecret with fixture: `SECRET` -> true; `300` -> false.
6. IsSecret normalizes a truthy non-boolean (`issecretvalue` answering `1`) to `true`.
7. CanAccess with `canaccessvalue` answering false for `SECRET` -> false; true for `300`.
8. CanAccess, `canaccessvalue` absent, `issecretvalue` present -> `not IsSecret`.
9. CanAccess, both absent -> true (including for nil).
10. Secret yet accessible (`issecretvalue(SECRET) = true`, `canaccessvalue(SECRET) = true`):
    CanAccess true, IsSecret true, **IsSafeKey false** -- pins "IsSafeKey is IsSecret, not CanAccess"
    (`MultiMeters/core/Secrets.lua:218-220`).
11. IsSafeKey(nil) -> false with and without the system.
12. IsSafeKey on plain values -> true; system absent -> `v ~= nil`.
13. Core is not duplicated: `core.IsConcatSafe(true) == false` while `compat.IsSecret(true) == false`,
    and with the fixture `core.IsConcatSafe` does not consult `issecretvalue` (spy count 0).

### 7.3 GetSpellInfo (7)
14. Modern table flattened in order; `select("#", ...) == 6`.
15. Modern present answering nil -> single nil; legacy spy **not called** (authoritative).
16. Legacy only (`C_Spell = ABSENT`), fixture in the REAL shape `"Legacy", "Rank 1", 999, 1.5, 0, 30, 774, 998`
    -> `"Legacy", 999, 1.5, 0, 30, 774`. Red under reading the rank as the icon.
17. All absent -> `nil`, `select("#") == 1`.
18. Bad type (`nil`, `{}`, `true`) -> nil, modern spy not called; string `"Kick"` is passed to the
    modern rung verbatim (spy args).
19. Secret fields pass through: modern table with `name = SECRET` -> first return `rawequal SECRET`, no raise.
20. Legacy rung answering nil name -> single nil.

### 7.4 GetSpellName (8)
21. `C_Spell.GetSpellName` hit -> name; later-rung spies not called.
22. `GetSpellName` nil -> middle rung `C_Spell.GetSpellInfo(id).name`.
23. `GetSpellName` answers `""` -> falls through; every rung `""` -> nil.
24. `C_Spell.GetSpellName` absent, `C_Spell.GetSpellInfo` present -> name.
25. Legacy only -> first return only (`select("#") == 1` against a multi-return fixture).
26. All absent -> nil.
27. First rung answers `SECRET` -> returned `rawequal`; the middle and legacy spies are not called,
    and `issecretvalue` was called with that value before anything else (ordering spy). **Plus (added
    at build):** a rung answering `""` that the fixture flags secret is returned, not fallen through.
28. `nil` id -> nil, no rung called.

### 7.5 GetSpellTexture (4)
29. Modern answering `(111, 222)` -> exactly one value, `111`.
30. Modern present answering nil -> nil; legacy spy not called.
31. Legacy only -> value; `select("#") == 1`.
32. All absent -> nil; `nil` id -> nil with no rung called.

### 7.6 GetSpellCooldown (9)
33. Modern table -> the five values in order.
34. Missing `isEnabled` -> true; missing `isActive` -> false; `isActive = 1` -> false.
35. Modern answering nil info -> `0, 0, false, 1, false`.
36. Secret `startTime`/`duration` (`SECRET`) -> returned `rawequal`, no raise.
37. Legacy (`C_Spell = {}`), `5, 12, true, 1` -> `5, 12, true, 1, true`.
38. Legacy zero duration -> `isActive false`.
39. Legacy `e = 0` -> `isEnabled false`; `e = false` -> false; `e = 1` -> true (J6).
40. Legacy secret duration (`SECRET`) -> `isActive false`, duration `rawequal`, no raise. **Plus (added at
    build):** a plain number the fixture flags secret (`issecretvalue = v == 12`, legacy `5, 12, true, 1`)
    -> `isActive false`. `SECRET` alone never reaches the IsSecret gate (`type(SECRET) ~= "number"`
    stops first), so without this shape removing the gate stays green.
41. All absent and bad type -> inert tuple with `select("#") == 5`; no rung called on bad type.

### 7.7 Spec (6)
42. Namespaced preferred over the global when both answer different values. **Plus (added at build):**
    namespaced present answering nil -> nil, global spy not called (the design pinned authority for
    GetSpecializationInfo only; a fall-through mutant of GetSpecialization survived without it).
43. Global only (`C_SpecializationInfo = ABSENT`) -> the global's value; `select("#") == 1`.
44. All absent -> nil.
45. GetSpecializationInfo namespaced passthrough preserves a 6-value multi-return exactly.
46. GetSpecializationInfo global fallback; namespaced-present-answering-nil does not fall through.
47. GetSpecializationInfo(nil) -> nil, no rung called; all absent -> nil.

### 7.8 The absent table (1)
48. With every rung removed at once (`C_Spell`, `C_SpecializationInfo`, `GetSpellInfo`,
    `GetSpellTexture`, `GetSpellCooldown`, `GetSpecialization`, `GetSpecializationInfo`,
    `issecretvalue`, `canaccessvalue` all `ABSENT`), a table-driven loop asserts every member's
    answer and arity against one literal table that is copied verbatim into the API document's
    absent column. This is the reference each host's stub is checked against (section 4).

### 7.9 The shared table (1, added at build)
49. With `compat.IsSecret` replaced on the shared table, `GetSpellName` still answers from the file
    local (a rung answering a fixture-secret `""` is returned, not fallen through). Pins rule 2.1.8.

49 cases (as built). Green gate: `/home/tushar/.claude/wow-addon/bin/ka0s-bounded lua tests/run.lua` and
`/home/tushar/.claude/wow-addon/bin/ka0s-bounded luacheck .` (0/0). `test_versioning` covers the
minor/changelog/doc coupling through `majors.lua`; `test_prose` covers US English and ASCII.

---

## 8. Per-consumer adoption delta (Phase 6 checklist)

Adoption happens **with** the v1.55.0 re-vendor, one commit per candidate after the re-vendor
commit (`wow-addon:revendor-libka0s`). Call sites keep calling `NS.Compat.X` (or `NS.Secrets.X`);
only the definitions change. Each adopter adds the degraded-load case of section 4, **and** (the
six table-map runners: AuraMaster, KickCD, MultiMeters, LootHistory, WhatGroup, PartyFrameEnhanced)
adds `["LibKa0s-Compat-1.0"]` to the `Kit.setSurfaceSource{...}` map in `tests/run.lua` in the same
commit, per section 4's gate amendment. ConsumableMaster needs no runner edit.

### 8.0 Every consumer, at the re-vendor (adopting or not)

- The whole-folder copy brings `libs/LibKa0s/Compat.lua` and the XML line. Hosts whose harness
  **derives** the lib list from `LibKa0s.xml` need nothing (AbsorbTracker, AuraMaster, BankLedger,
  ConsumableMaster, KickCD, MultiMeters, PanelMaster, PartyFrameEnhanced, PrettyChat).
- **LootHistory** `tests/test_libka0s.lua:20` (`LIB_FILES`) and **WhatGroup** `tests/loader.lua:24`
  (`LIBKA0S`) hand-type the list: add `"libs/LibKa0s/Compat.lua"` after `"libs/LibKa0s/Env.lua"`,
  or the XML-order check fails. The `NO_LIBKA0S` skip lists (WG `tests/test_envsetup.lua:18`,
  `tests/test_mediasetup.lua:24`, `tests/test_libka0s.lua:489`) need no change: Core absent already
  takes every major down.

### 8.1 AuraMaster

- `core/Compat.lua` top (after `:3`): resolve `CompatLib`.
- `core/Compat.lua:312-328` `GetSpellInfo`: keep AM's number-only policy locally, delegate the rest:
  `if type(id) ~= "number" then return nil end; if CompatLib then return CompatLib.GetSpellInfo(id) end; return nil`.
  Returns 6 values instead of 2; callers read `name` only (`modules/CastAura.lua:72`,
  `settings/GeneralSpells.lua:256, 1247`) -- unaffected. Degraded install: nil (was: a C_Spell read).
- `core/Secrets.lua:36-40, 46-50, 76-79`: wire `IsSecret`, `CanAccess`, `IsSafeKey` from the major,
  the current bodies becoming the guard stubs (section 4 rule 2, with the duplication comment).
  `IsReadableNumber`, `NumberOr` stay.
- Tests: `tests/test_compat.lua:486-502` stays green (legacy shape already correct; `"774"` still nil
  via the local guard). Add the degraded-load case. `tests/run.lua:38` map gains the Compat row. The
  parity gate is two calls: `NS.Compat` ignoring the trio and every unwired reader (all but
  `GetSpellInfo`), `NS.Secrets` ignoring the six readers. `docs/compat-layer.md` rows for these members
  point at the library.

### 8.2 KickCD

- `core/Compat.lua` top: resolve `CompatLib`.
- `:64-92` `GetSpellCooldown` -> library. **Behavior change:** legacy rung `e == 0` now reads
  disabled. `:94-144` `GetSpellCooldownDuration` stays.
- `:146-157` `GetSpellTexture` -> library (drops the client's second return; callers
  `modules/IconGrid.lua:333` assign one local, `settings/Spells.lua:268` flows into
  `SetImage(getSpellIcon(...) or 134400)` at `:632` -- unaffected).
- `:159-174` `GetSpellInfo` -> library. String input still resolves (`settings/Spells.lua:281`,
  `core/KickCD.lua:580` read position 6). **Behavior change:** legacy rung remapped.
- `:253-270` spec pair -> library. **Behavior change:** `GetSpecializationInfo(nil)` answers nil
  instead of calling the client with nil (`core/Util.lua:204` already guards).
- **New seam:** `Compat.IsSecret` wired from the major (guard stub). Replace the 12 inline calls
  (section 1) with `NS.Compat.IsSecret(x)`; `core/Compat.lua:86` disappears with GetSpellCooldown.
  The `a ~= nil and ...` prefixes at `modules/Cooldowns.lua:251-252, 289-290` and
  `modules/IconGrid.lua:334` become redundant (IsSecret(nil) is false) but are harmless to keep.
  This closes C2-F04's "no seam at all" breach. The C-side boolean helpers in `core/State.lua` stay.
- Tests: `tests/test_compat_api.lua:218-224` fixture `return "Legacy", 9, 1.5` encodes the wrong
  legacy shape -- change to `"Legacy", nil, 9, 1.5` and keep the assertions. Add a legacy `e = 0`
  case. `:209-216` (authoritative nil) and `:179-195` stay green. `tests/test_compat.lua:7-35` stays
  green. `docs/compat-layer.md` and `docs/midnight-quirks.md` references updated.

### 8.3 MultiMeters

- `core/Compat.lua:44-57` `GetSpellInfo`, `:62-70` `GetSpellTexture` -> library. **Behavior
  change:** legacy rung remapped.
- `:97-112` spec pair -> library. These have no production caller today; additionally route
  `modules/Roster.lua:187` (`_G.GetSpecialization`, a direct deprecated-global read in a feature
  module -- an existing `compat` breach) through `NS.Compat.GetSpecialization`.
  `GetSpecializationRole` (`:188`) is not in this major (one consumer) and stays inline, flagged.
- `core/Secrets.lua:151-155, 166-171, 224-227`: wire the trio (guard stubs). `CanCompare`,
  `CanCompare2`, table members, `SafeIterate` stay and keep calling `Secrets.CanAccess` at call time.
- Tests: `tests/test_compat.lua:74-82` asserts only the name, stays green; correct its fixture
  (`"Old " .. id, 7, 0, 0, 40, id`) to the real legacy shape anyway. `:84-90`, `:111-115` stay green.
  `tests/test_secrets.lua` unchanged. `tests/run.lua:337` map gains the Compat row. The parity gate
  is two calls: `NS.Compat` ignoring the trio plus the unwired readers (`GetSpellName`,
  `GetSpellCooldown`), `NS.Secrets` ignoring the six readers.

### 8.4 ConsumableMaster

- `core/Compat.lua:17-33` spec pair -> library (identical, including the nil-index guard).
- `:60-63` `IsSecret` -> library (guard stub).
- `:68-83` `GetSpellName` -> library. **Behavior change:** a secret name is returned instead of
  being compared with `""` (removes a latent in-combat raise). Ladder, `""` handling and nil guard
  otherwise identical to CM's.
- `:36-51` the two class-ID spec readers stay.
- Tests: `tests/test_compat.lua:43-66, 92-157` stay green. CM's harness writes `_G.C_Spell`
  (`tests/wow_mock.lua:876`); the library's bare reads fall back to `_G`, so no harness change.

### 8.5 LootHistory

- `core/Compat.lua:82-87` `GetSpellName` -> library. **Behavior change:** a modern nil or `""` falls
  through to `C_Spell.GetSpellInfo` and the legacy global (inert on a live client, where both read
  the same spell data); nil id guard unchanged.
- Keep `NS.Compat.GetSpellName` a field: `tests/test_attribution.lua:156-261` monkeypatches it.
- Tests: `tests/test_compat.lua:48` stays green (LH's mock has no `C_Spell`). Plus 8.0's list edit.

### 8.6 WhatGroup

- `core/Compat.lua:27-38` `GetSpellName` -> library. **Behavior change:** nil id answers nil
  (was: the client called with nil); a plain `""` falls through; secret-safe.
- `:43-51` `GetSpellTexture` -> library (second return dropped; `modules/Frame.lua:522` uses `or 134400`).
- `:116-127` `GetSpellCooldownTimes` -> `local s, d = CompatLib.GetSpellCooldown(id); return s, d`
  (the truncation matters: `modules/Frame.lua:830` spreads it into `SetCooldown`, whose third
  parameter is `modRate`). Degraded: `0, 0`.
- `:94-111` `GetSpellCooldownRemaining` reads `start, duration, enabled` from member 7; the GCD floor
  and `GetTime()` arithmetic stay WG's. Result identical on every branch (the inert tuple's
  `enabled == false` returns 0 exactly as `not info` did).
- `IsSpellKnown`, `GetSpellLink`, `GetActivityInfoTable`, `AddOnLinkType` stay.
- Tests: `tests/test_compat.lua:105-139` stay green (WG loads the library per instance in the same
  env, `tests/loader.lua:47-60`, so `env.C_Spell = nil` reaches it). Plus 8.0's list edit.

### 8.7 PartyFrameEnhanced

- `core/Compat.lua:13-16` `IsSecret` -> library (guard stub). Every other PFE member keeps calling
  `Compat.IsSecret` at call time. `tests/test_compat.lua:27-28` stays green.

### 8.8 BankLedger, PanelMaster, AbsorbTracker, PrettyChat

No member adopted: BankLedger's and PanelMaster's Compat are wholly addon-specific (section 5.3);
AbsorbTracker and PrettyChat have no `core/Compat.lua`. Re-vendor only (8.0).

---

## 9. OPEN (deviation discipline: both readings, no silent pick)

- **OPEN-1 -- `compat.md`'s example contradicts the chosen `GetSpellInfo` contract.**
  `WowAddonStandards/standards/standards/compat.md` (the code block) returns `info.name, nil, info.iconID`
  on the modern rung -- the legacy positional shape with the rank slot nil. The library returns
  `name, iconID, castTime, minRange, maxRange, spellID` (KickCD's and MultiMeters' shape, of which
  AuraMaster's `name, icon` is a prefix). Reading A: the block is illustrative; the library contract
  governs, and the standard's example is updated upstream to route through `LibKa0s-Compat-1.0` (or
  to show this shape). Reading B: the example is the normative shape, and the library must return
  `name, nil, iconID, castTime, minRange, maxRange, spellID`, which changes every live caller in
  three addons (`MM DrillDown.lua:550`, `Tooltip_Lines.lua:661` read icon at 2; KickCD reads spellID
  at 6). Recommended: A, as an upstream change to the standard.
- **OPEN-2 -- `LibKa0s/Perf.lua:700-714` keeps an inline spec read.** With this major shipped, the
  library has a single Compat owner that Perf does not use. LibKa0s's own audit `LK-31`
  (`docs/audits/2026-09-08/02_DEVIATIONS.md:41`) proposed Env as the home and Perf calling it.
  Reading A: record a `## Documented deviations` row in LibKa0s `CLAUDE.md` (Rule `compat`; Perf's
  inline read duplicates `LibKa0s-Compat-1.0`'s spec pair because a Perf floor on Compat is a
  vendoring break; re-check trigger: the next Perf floor raise made for any other reason), and add the
  cross-reference comment to `Perf.lua` at its next minor. Reading B: raise Perf's floor now, a
  re-vendor trigger for all eleven consumers in a release otherwise declared additive. Recommended: A.
  Also: LK-31's "move it to Env" is superseded by this major if A is taken; the audit row should say so.
- **OPEN-3 -- upstream counts and the open-evolution.** `library-stack.md:11` ("twelve LibStub majors
  across eighteen files") and its module table, and `open-evolutions.md:13` ("Candidates the
  collection still duplicates: the `Compat` shim ..."), become stale: thirteen majors across nineteen
  files, and the Compat entry becomes "narrow major shipped; the wide extraction rejected (reasons in
  `docs/api/Compat/version-1-docs.md`)". This is the standard's ripple, not LibKa0s's.
- **OPEN-4 -- the guard stub is a hand-rolled copy of a LibKa0s member.** anti-patterns #47 forbids
  hand-rolling what a LibKa0s module provides; section 4 rule 2 requires each host to carry the
  three-line body as its degradation arm. Reading A: a degradation arm is not a fork (it runs only
  when the module is absent), and `library-stack-§7`'s documented-duplication paragraph covers it
  when commented at both copies. Reading B: the host should fail closed instead (e.g. treat every
  value as inaccessible while the library is absent), which avoids the copy but makes every guarded
  path take its fallback on a degraded install. Recommended: A; the standard could say so in one line.
- **OPEN-5 -- AbsorbTracker and PrettyChat ship no `core/Compat.lua`** while `compat` says every
  addon MUST. Outside this design; noted because the harvest counted "nine copies" and a reader may
  assume eleven.
- **OPEN-6 -- MultiMeters `modules/Roster.lua:187-188`** reads deprecated spec globals directly in a
  feature module (existing `compat` breach, found while measuring). 8.3 routes `GetSpecialization`;
  `GetSpecializationRole` has no shim anywhere in the collection and would be a single-consumer
  member, so it belongs in MultiMeters' own Compat, not here.

---

## 10. Judgement calls (CP-3, delegated)

- **J1 -- Nine members, not the union.** Only shapes with two or more PRODUCTION consumers and the
  same semantics (section 1 table). Interpolation and rule-formatter clear the count but not the
  content bar (5.2); everything else is single-consumer or disagrees (5.1, 5.3).
- **J2 -- `GetSpellInfo` contract = the 6-tuple `name, iconID, castTime, minRange, maxRange, spellID`.**
  The three copies hold three contracts (AM `name, icon`; KickCD/MM the 6-tuple; the standard's
  example `name, nil, iconID`). The 6-tuple changes no live caller: AM's is its prefix, KickCD reads
  position 6 (`settings/Spells.lua:281`), MM reads positions 1-2. The legacy rung is remapped from
  its real shape (AM's pinned test is the evidence); KickCD/MM fixtures that encode rank-as-icon are
  corrected, not honored. Standard example conflict is OPEN-1.
- **J3 -- `GetSpellName` falls through on nil/`""`; every other reader treats the first existing rung
  as authoritative.** The authoritative rule is argued and tested where it is stated
  (`KickCD/tests/test_compat_api.lua:209-216` for GetSpellInfo; `WhatGroup/core/Compat.lua:66-69`
  for IsSpellKnown). For GetSpellName, both copies that test the policy test fall-through
  (`ConsumableMaster/tests/test_compat.lua:117`, `WhatGroup/tests/test_compat.lua:112`); LootHistory's
  finality is untested and unargued. Two rungs reading the same spell data can only disagree about
  presence, so fall-through cannot hide a disagreement the way it would for a boolean.
- **J4 -- `GetSpellName` keeps ConsumableMaster's middle rung (`C_Spell.GetSpellInfo(id).name`).**
  Single-consumer rung inside a three-consumer member; monotone (it can only turn a nil into a name)
  and it is the rung the kit's `mock_ids` answers, so CM's harness keeps resolving names.
- **J5 -- Secret-aware `""` test in `GetSpellName`.** A secret answer is returned untouched and ends
  the ladder; CM's `n ~= ""` on a secret would raise in combat. New behavior for CM, a fix.
- **J6 -- Legacy `isEnabled`: `0` reads disabled** (WhatGroup `core/Compat.lua:106`), over KickCD's
  `e ~= false`, which reads `0` as enabled. KickCD's reading is an unargued defect on a rung only a
  harness reaches; nil stays enabled in both copies and in the library.
- **J7 -- `GetSpellCooldown` counts WhatGroup as a consumer** through `GetSpellCooldownTimes`, whose
  contract is exactly member 7's first two returns on every branch (modern, nil info, legacy, absent).
  WG keeps a two-value wrapper because `SetCooldown`'s third parameter is modRate.
- **J8 -- Spell members accept number OR string; AuraMaster's number-only guard stays in AuraMaster.**
  KickCD resolves typed names through position 6; AuraMaster pins `"774" -> nil`. A domain flag would
  be the per-consumer escape hatch bar 2 forbids, so the library takes the client's own domain and
  the narrower policy stays a one-line guard in the one addon that wants it.
- **J9 -- Reader stubs answer the absent value; guard stubs re-implement.** Section 4. The absent
  answer for a guard is only correct when the CLIENT lacks the system, not when the LIBRARY is missing.
- **J10 -- The secret trio lives in this major, not Core.** Version-variant 12.0 globals are
  `compat`'s subject, Core's probe answers a different question (section 3), and a Core promotion
  raises the floor question for eleven majors.
- **J11 -- `IsSafeKey` clears the bar.** Two consumers (AuraMaster, MultiMeters), byte-equivalent
  bodies, same stated semantics, and MM documents why it is IsSecret-based (`core/Secrets.lua:218-220`).
- **J12 -- `GetSpecializationInfo` stays a passthrough** with CM's nil-index guard added for everyone
  (turns a client raise on nil into nil; KickCD `core/Util.lua:204` already guards, MM has no caller).
- **J13 -- Perf.lua's inline spec read is left alone** (additive-only release; a Perf floor on Compat
  is a vendoring break). OPEN-2.
- **J14 -- Exact arity everywhere but member 9.** `GetSpellTexture` and `GetSpecialization` are
  parenthesized to one value; `GetSpellName`'s legacy rung is truncated to one.
- **J15 -- Load position: immediately after `Env.lua`** in `LibKa0s.xml` and `tests/majors.lua`
  (Core floor only, no dependents), matching the "client facts" group.
