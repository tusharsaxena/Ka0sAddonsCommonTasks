# forever-cooldown-api: what KickCD can rely on in WoW Forever

Read-only study, 2026-11-23. KickCD master 333cd49.

| Source | Pin |
|---|---|
| Forever UI (`F:` below, root `Interface/AddOns/`) | 734f065, 1.60.1.71037 |
| Retail UI (`L:`) | ab5cb85, 12.1.5.70961 |
| API docs (`DOC:`) | `Blizzard_APIDocumentationGenerated/` in both trees |
| DB2 (`DB2:`) | `https://wago.tools/db2/<Table>/csv?build=1.60.1.71037` |
| Global and CVar dumps (`BIR:`) | github.com/Ketho/BlizzardInterfaceResources, branch forever e230342 (build 1.60.1.70938), live f3b334b |

`VERIFIED` = read in source or data at the pin. That proves what ships and what the contract is, not runtime behavior.
`INFERRED` = reasoning is given. `UNKNOWN` = the probe that settles it is given (section 12). `MEASURED` = an in-game
measurement another Ka0s repo recorded. **Nothing here was run in the client.**

## 0. Verdict

The engine half of KickCD ports as it is: cooldown, duration-object, curve, cast and interruptibility contracts are
the same on both clients, secrecy included. The identity half does not work at all: spec, spell list and rank.

| # | Finding | Effect on master if only the TOC is changed | Weight |
|---|---|---|---|
| B1 | One spec per class, ids 1482 and 1484-1491. The seed is keyed by Retail's ids | `GetSpellList(class, 1491)` is nil, "no stored spell list", empty grid for every character | blocker |
| B2 | One id per rank. Seeds and polls use one literal id, with no rank resolution | An icon may vanish or go stale when a rank is trained. A list written with max-rank ids is empty while leveling | blocker |
| B3 | 52 of the 73 distinct (class, id) seed pairs do not exist on Forever. Several survivors are other spells | A re-key alone gives wrong and incomplete lists | blocker |
| B4 | The global `GetNumSpecializationsForClassID` is absent on Forever | `buildSpecNameMaps` and the spec-icon cache return empty without an error: no client spec names, order or icons | must fix |
| B5 | The Cooldown Manager gate matches `info.spellID` only, which is rank 1, and has no pet spells | `/kcd spells add` and the page refuse Kick rank 2+, Pummel rank 2 and Spell Lock | must fix |
| B6 | `for classID = 1, GetNumClasses()` over non-contiguous class ids (1,2,3,4,5,7,8,9,11) | Druid can be dropped from class lists (INFERRED) | must fix |
| R1 | Spell-known checks run only through deprecation shims | Empty grid if `loadDeprecationFallbacks` is 0 | should fix |
| R2 | GCD spell 61304 does not exist on Forever | The debug log's "(gcd)" mark never fires. Render is unaffected | minor |
| R3 | Forever kicks are on the GCD (except Counterspell) | Every GCD flips `isActive`, so more emits, and the ready glow drops on each GCD | behavior to smoke |

## 1. Cooldown Manager (C_CooldownViewer)

### 1.1 Ships
- VERIFIED: `F:Blizzard_CooldownViewer/Blizzard_CooldownViewer.toc:2` is `AllowLoadGameType: standard, camelot`
  (Retail: `standard`). `F:Blizzard_SettingsDefinitions_Frame/Camelot/InterfaceOverrides.lua:52-53` returns true from
  `HasCooldownViewer()`, so the settings section shows.
- VERIFIED: `DOC:CooldownViewerDocumentation.lua` has the same functions, events and `CooldownViewerCooldown` fields.
  The only doc difference is `GroupBuffItem`, which on Forever adds `displaySpellID` ("highest known rank") and says
  `spellID` is "shared by every rank of the spell".
- VERIFIED: `CooldownViewerConstantsDocumentation.lua` is identical: categories 0-8; set-spell flags HideAura 1,
  HideByDefault 2, SelectHighestLevelLinkedSpell 4.
- VERIFIED: the Lua differs in item/category cooldown sources (`C_Spell.GetItemCooldown`), Edit Mode hooks and layout.

### 1.2 Populated, per class
VERIFIED, DB2 CooldownSet (32 rows), CooldownSetSpell (609), CooldownSetLinkedSpell (1906):

| Class | classID | specID | Set | Rows | Interrupt entries (category 0 Essential, 1 Utility) |
|---|---|---|---|---|---|
| Warrior | 1 | 1491 | 5236 | 72 | Pummel 6552 (1, HideByDefault), Shield Bash 72 (1) |
| Paladin | 2 | 1486 | 5261 | 70 | none; Hammer of Justice 853 (1) |
| Hunter | 3 | 1485 | 5265 | 54 | none; Scatter Shot 19503, Intimidation 19577 (1) |
| Rogue | 4 | 1488 | 5240 | 48 | Kick 1766 (1) |
| Priest | 5 | 1487 | 5238 | 57 | Silence 15487 (1) |
| Shaman | 7 | 1489 | 5263 | 69 | Earth Shock 8042 (0) |
| Mage | 8 | 1482 | 5234 | 56 | Counterspell 2139 (1) |
| Warlock | 9 | 1490 | 5237 | 47 | **none: Spell Lock 19244/19647 is in no set** |
| Druid | 11 | 1484 | 5235 | 70 | Feral Charge 1238122 (1); Bash 5211 (1) |

- The other sets are racial (gated by PlayerCondition), priest racials, and two global item/equip sets with spell id 0
  (categories 5 and 7). Category totals: 0=107, 1=137, 2=313, 4=47, 5=3, 7=2; categories 3, 6 and 8 are empty.
- A ranked entry stores **rank 1 as SpellID**, lists all ranks in CooldownSetLinkedSpell and carries flag 4. Example:
  row 200224 = 1766, linked 1766, 1767, 1768, 1769. Pummel, Shield Bash, Earth Shock, Bash and Hammer of Justice are alike.
- A TrackedBuff row of the same spell can link aura ids instead (853 in category 2 links 1324513...), so linked ids
  from category 2 and 3 are not all casts.

### 1.3 Enablement
- VERIFIED: CVar `cooldownViewerEnabled` defaults to "0" on both (BIR CVars). It controls the display only
  (`F:CooldownViewer.lua:1900-1912`), along with `IsCooldownViewerAvailable()`. The data provider reads the category
  sets without testing either (`CooldownViewerSettingsDataProvider.lua:108-112`).
- INFERRED: the two getters answer with the CVar off, because Blizzard's provider calls them unconditionally.
  UNKNOWN for a low-level character or when unavailable: probe P3.
- UNKNOWN: whether `info.spellID` stays rank 1 or becomes the highest known rank, what `overrideSpellID` holds, and
  whether `allowUnlearned=false` (KickCD's call) hides untrained rows. Probe P3. The data says rank 1.

### 1.4 What KickCD may use it for
- Not as the seed: it has no pet spells and no "this interrupts" field, and it lists only the live class.
- As an admission hint, with a widened match: `spellID`, `overrideSpellID`, and the `linkedSpellIDs` of the Essential
  and Utility rows, plus pet spells by another route. Also call it with `allowUnlearned = true`, or admit any known spell.
- `core/SpellInput.lua:204` records `info.spellID` only, and `Admissible` refuses a miss whenever the set is non-empty.
  On Forever the set is non-empty for every class, so the lenient path never rescues it (B5).
- The invalidator hears `TRAIT_CONFIG_UPDATED` and `PLAYER_SPECIALIZATION_CHANGED` only. It needs `SPELLS_CHANGED`
  (training) and `COOLDOWN_VIEWER_DATA_LOADED` as well, or a set cached at login stays stale after training.

## 2. C_Spell cooldowns, charges, usability

VERIFIED: the doc blocks for all of these are byte-identical on the two clients.

| API (DOC:SpellDocumentation.lua) | Secrecy | KickCD use |
|---|---|---|
| `GetSpellCooldown` :309 | `SecretWhenCooldownsRestricted`; `isActive`, `isEnabled`, `isOnGCD` are NeverSecret (SpellShared :19) | branches on `isActive` only: safe |
| `GetSpellCooldownDuration(id, ignoreGCD=false)` :327 | no secret return; the object's getters may be secret | object to C sinks: safe. `ignoreGCD` is unused today |
| `GetSpellCharges` :291 | `SecretWhenCooldownsRestricted`; `maxCharges`, `isActive` NeverSecret | nil test only: safe |
| `GetSpellChargeDuration` :274 | none | unused |
| `IsSpellUsable` :980 | none | boolean test: safe |
| `GetSpellInfo` :416, `GetSpellTexture` :595, `GetSpellSubtext` :578 | none on return | as Retail |
| `GetBaseSpell` :90, `GetOverrideSpell` :206 | none | see section 8 |

- VERIFIED: the predicate (`DOC:SecretPredicatesDocumentation.lua:89-93`) is secret in combat, encounter, challenge
  mode or PvP, with per-spell never/always flags taking priority. `C_Secrets.ShouldSpellCooldownBeSecret` and
  `GetSpellCooldownSecrecy` ship on both (SecretPredicateAPI doc identical).
- UNKNOWN: the per-spell flags for Forever's kicks, probe P4. The code needs no answer: it treats all as secret.
- VERIFIED, DB2 SpellCategory and SpellCategories: no kick has charges (ChargeCategory 0, MaxCharges 0). The charge
  branch idles.
- VERIFIED: the `C_Spell` additions on Forever are `GetItemCooldown`, `GetTargetSpellID`, `IsActiveSpell`,
  `CancelAutoRepeatSpell`, `CancelItemTempEnchantment`, `PlaceTargetingSpellAtCursor`. The one secrecy change is
  `IsSpellCrowdControl`, whose SecretArguments tightened from AllowedWhenTainted to AllowedWhenUntainted. KickCD calls none.

### Cooldown shapes (DB2 SpellCooldowns, SpellCategories: VERIFIED)

| Spell | Ranks | Cooldown | Category | GCD | Notes |
|---|---|---|---|---|---|
| Kick | 1766, 1767, 1768, 1769 (levels 12/26/42/58) | 10 s | 88 | 1.0 s | supersede chain |
| Pummel | 6552, 6554 (38/58) | 10 s | 88 | 1.5 s | supersede chain |
| Shield Bash | 72, 1671, 1672 (12/32/52) | 12 s | 88 | 1.5 s | supersede chain; same category as Pummel |
| Counterspell | 2139 (24) | 30 s | 88 | **0** | no ranks |
| Spell Lock (pet) | 19244, 19647 (36/52) | 30 s | 88 | 1.5 s | skill line 189; class mask 0 |
| Earth Shock | 8042, 8044, 8045, 8046, 10412, 10413, 10414 (4 to 60) | 6 s | 19 | 1.5 s | **no supersede**: all ranks stay for downranking; category shared with other shocks |
| Silence | 15487 | 45 s | none | 1.5 s | talent; silence aura, not effect 68 |
| Feral Charge | 1238122 (20) | 15 s | 2182 | 0 | trait; triggers 19675 (effect 68); 16979 is a second trait-referenced id |
| Bash | 5211, 6798, 8983 | 60 s | 32 | 1.5 s | stun |
| Hammer of Justice | 853, 5588, 5589, 10308 | 60 s | 32 | 1.5 s | stun; no supersede |

- Cooldowns are **category** cooldowns (RecoveryTime 0, CategoryRecoveryTime set). INFERRED: Pummel and Shield Bash
  lock each other out, and any rank reports the same cooldown. Probe P2 confirms the second half.
- Rebuke 425609 and Skull Bash 410176 carry effect 68 and skill-line rows (AcquireMethod 3), but no trait and no
  CooldownSet row references them. UNKNOWN whether obtainable: do not seed (probe P9).
- `Const.GCD_UPPER = 1.6` still separates every GCD (1.0, 1.5) from the shortest interrupt cooldown (6 s): VERIFIED against the table.
- VERIFIED: spell 61304 is absent from Forever's SpellName (32,504 rows), and Forever's UI never names it.
  `Cooldowns.lua:447` therefore reads false (R2). `isOnGCD` is the replacement, but the doc says to trust it only
  inside a SPELL_UPDATE_COOLDOWN response.
- INFERRED (R3): on Retail most kicks are off the GCD. Here `isActive` is true during each GCD, so `ready` is false
  and the glow drops, while the curves keep alpha and tint "ready". Stance, shield and rage also feed `usable`
  (Pummel needs Berserker Stance, Shield Bash a shield in classic rules: confirm with P2).

## 3. Duration objects and curves
- VERIFIED: LuaDurationObjectAPI, DurationUtil and CurveUtil docs are identical on both clients.
  `CreateDuration` :11, `SetTimeFromStart` :445, `EvaluateTotalDuration` :109 (SecretWhenCurveSecret) and
  `EvaluateColorValueFromBoolean` :49 (AllowedWhenTainted) all exist.
- VERIFIED: `Cooldown:SetCooldownFromDurationObject` (FrameAPICooldown :308) and `SetAlphaFromBoolean`
  (SimpleFrameAPI :1145, takes a secret when tainted) are unchanged. The Cooldown doc's only change is a nilable texture.
- VERIFIED: `UnitCastingDuration` is `SecretReturns = true` and `UnitChannelDuration` is not, on both. The "plain
  numbers" comments on the CastingDuration methods (`core/Compat.lua:306,347,376`) are contradicted by KickCD's own
  Castbar comments. The code only passes getters to C sinks, so nothing breaks. Fix the comments.
- INFERRED: KickCD's measured Retail table (every getter secret in combat except `HasSecretValues`) holds here. P4.

## 4. Casts on target and focus
- VERIFIED: `UnitCastingInfo` (DOC:Unit :828), `UnitChannelInfo` :870, both duration readers (:811, :854) and the
  `UNIT_SPELLCAST_*` events (:4615-4850) are identical, with the same positions (`notInterruptible` 8 for a cast, 7
  for a channel).
- VERIFIED: `SecretWhenUnitSpellCastRestricted` (:115-117) means secret whenever the unit "is not the player or their
  pet", per-spell flags first. **This is not combat-gated**, so name, texture, times, id and `notInterruptible` of a
  target or focus are secret by default everywhere. NeverSecret: `isTradeskill`, `castBarID`, `delayTimeMs`,
  `isEmpowered`, `numEmpowerStages`.
- VERIFIED: the unit argument is `UnitTokenPvPRestrictedForAddOns` on both clients.
- VERIFIED as code evidence: PartyFrameEnhanced (`master:core/Compat.lua:97-135`, `modules/CastBars.lua:120-135,283`)
  ships the same technique on Forever: truthiness of the name, `BoolValue`, `AlphaFromBool`, a duration object to C.
  Its `docs/forever-quirks.md` records no Forever-specific finding. That is absence of a report, not a measurement.

## 5. notInterruptible and interruption
- VERIFIED: `notInterruptible` is `bool, Nilable = true` and secret under the cast predicate.
  `UNIT_SPELLCAST_INTERRUPTIBLE` :4759 and `NOT_INTERRUPTIBLE` :4769 carry the unit only, with no secrecy, so
  KickCD's plain-after-flip rule holds by contract.
- VERIFIED: Forever's own cast bar honors the flag and wraps the result with `WrapValueInSpellCastSecrecy`
  (`F:Blizzard_UIPanels_Game/Shared/CastingBarFrame.lua:334-354,608`).
- UNKNOWN: whether classic-era creature data populates it meaningfully (interrupt-immune mobs, player spells that
  cannot be silenced, physical "casts"), and whether nil occurs where the C sinks want a non-nil bool. Probe P5.
- VERIFIED: `UNIT_SPELLCAST_INTERRUPTED` :4744 carries `unitTarget, castGUID, spellID, interruptedBy, castBarID`,
  secret under the cast predicate except castBarID. `CHANNEL_STOP` :4629 carries `interruptedBy` too. KickCD routes
  both to stop handlers that ignore the payload: safe. An "interrupted by X" feature could only display the secret.
- MEASURED (CombatTrail, forever-quirks §5, build 70862): registering `COMBAT_LOG_EVENT_UNFILTERED` raises
  `ADDON_ACTION_FORBIDDEN`, which pcall does not catch. KickCD does not register it and must not start.
- UNKNOWN: whether `UNIT_SPELLCAST_SUCCEEDED` fires for the player's kicks here. KickCD does not depend on it.
- `UNIT_SPELLCAST_EMPOWER_*` exist on Forever (doc :4672). No class uses them, so the routes are harmless.

## 6. Focus
- VERIFIED: focus ships whole. `Blizzard_UnitFrame.toc:57` loads `[Family]\TargetFrame.xml` with no camelot
  exclusion, and that is `Mainline/TargetFrame.xml:572` FocusFrame with a spell bar on `PLAYER_FOCUS_CHANGED`.
- VERIFIED: `F:Blizzard_FrameXML/Bindings_Camelot.xml:1155,1158,1535` has FOCUSTARGET, TARGETFOCUS and FOCUSCAST.
  `/focus` is in the standard slash set (`SlashCommands.lua:38,235-239`). `FocusUnit` is a C global (BIR), restricted
  (`TargetScriptDocumentation.lua:39-43`). `PLAYER_FOCUS_CHANGED` is at Unit :3792.
- INFERRED: that Camelot runs as GameMode Standard for slash commands, since no Camelot entry exists in that table. P6.
- KickCD needs no client branch for the focus unit.

## 7. Spec, talents, classes
- VERIFIED, DB2 ChrSpecialization: one row per class (Mage 1482, Druid 1484, Hunter 1485, Paladin 1486, Priest 1487,
  Rogue 1488, Shaman 1489, Warlock 1490, Warrior 1491), plus Default 1493. All are role 2 and OrderIndex 0.
- MEASURED (CombatTrail `docs/forever-quirks.md:215-229`, build 70862, Hunter): `GetSpecialization` answers 1 and
  `GetSpecializationInfo` answers 1485 "Hunter" with no icon, whatever the points. The trees are C_Traits groups.
- `C_SpecializationInfo.GetSpecialization` and `GetSpecializationInfo` ship. LibKa0s-Compat tries them first, so
  `Util.PlayerSpecID` resolves 1491 and its siblings.
- VERIFIED: the bare `GetSpecialization`, `GetSpecializationInfo` and `GetNumSpecializationsForClassID` are defined
  only by `Blizzard_DeprecatedSpecialization`, whose TOC line 3 is `classic, standard`, with no camelot, and BIR lists
  none as a C global. INFERRED absent on Forever: `standard` and `camelot` are disjoint (the Cooldown Manager TOC had
  to add camelot; PlayerSpells loads `standard` and `camelot` variants as alternatives). The kit's forever profile agrees.
- KickCD callers of the absent global: `core/Util.lua:273,283`, `settings/Spells_Header.lua:88,95`. Both are guarded,
  so they fail silently and the kit's client-globals check passes them (B4). Use
  `C_SpecializationInfo.GetNumSpecializationsForClassID`. `GetSpecializationInfoForClassID` stays a C global (BIR).
- VERIFIED, DB2 ChrClasses: ids 1,2,3,4,5,7,8,9,11. Blizzard replaced `for i = 1, GetNumClasses()` with
  `C_SpecializationInfo.GetAllClassIDs()` and `GetClassInfo(classID)` in Forever's ClubFinder.lua :80,549,605,621,
  WhoList and Wardrobe. INFERRED: the old loop misses class 11 if `GetNumClasses()` is 9 (B6; callers `core/Util.lua:277`,
  `core/Database.lua:459`, `settings/Spells_Header.lua:91`). Value: P1.
- Dual spec: `GetCombatConfigIDForSpecGroup`, `SetActiveSpecGroup`, `IsSpecSelectionEnabled`, `GetAllClassIDs` and
  `HasPlayerEarnedATalentPoint` are Forever additions (VERIFIED, SpecializationInfo doc diff and
  `F:Blizzard_PlayerSpells/Camelot/ClassTalents/Blizzard_ClassTalentsFrame.lua:120,183,370`). The specID does not
  change with the group.
- Events: `TRAIT_CONFIG_UPDATED`, `ACTIVE_TALENT_GROUP_CHANGED`, `PLAYER_TALENT_UPDATE`, `CHARACTER_POINTS_CHANGED`
  and `LEARNED_SPELL_IN_SKILL_LINE` are all documented. Which fire on a spent point is UNKNOWN (RangeMaster RANGE-9,
  still a smoke check). Follow RangeMaster: register each if valid, plus `SPELLS_CHANGED` and `PLAYER_LEVEL_UP`
  (`RangeMaster master:core/RangeMaster.lua:100-110`). P7.
- Spell Lock needs the pet bank, and `UNIT_PET` if `SPELLS_CHANGED` does not cover a summon (P9).

## 8. Spellbook and ranks

### Known checks
- VERIFIED: `IsPlayerSpell` and `IsSpellKnown` are not C globals on either client (BIR). Both come from
  `Blizzard_DeprecatedSpellBook/Deprecated_SpellBook.lua:4-19`, which has no game-type gate, is identical on both
  clients and returns early unless `loadDeprecationFallbacks` is on (default "1" on both).
  `Compat.IsSpellAvailable` has no other rung, so with the CVar off every seed is rejected (R1).
- Replacement, VERIFIED present: `C_SpellBook.IsSpellKnown(id, bank)` :738 and
  `IsSpellInSpellBook(id, bank, includeOverrides)` :720, with `Enum.SpellBookSpellBank.Player` and `.Pet`.

### Do ids change per rank?
- VERIFIED: **yes**, one id per rank (table in section 2; subtext "Rank N").
- VERIFIED: two families. Superseded chains (Kick, Pummel, Shield Bash, Bash, Kidney Shot, via SkillLineAbility
  SupercedesSpell) and downrankable ones with no supersede (Earth Shock, Hammer of Justice).
- VERIFIED: Forever adds `C_SpellBook.IsSpellBookItemLowRank` ("lower rank of a known higher rank") and CVar
  `ShowAllSpellRanks` (default "0"), which filters the spellbook display
  (`F:Blizzard_PlayerSpells/SpellBook/Blizzard_SpellBookFrame.lua:567-593`).
  INFERRED: low ranks can remain spellbook items, at least in the downrankable family.

### Does a base or override id resolve a rank?
- VERIFIED: no documented API maps a rank to another. `GetBaseSpell`, `GetOverrideSpell` and `Find*` speak of
  overrides only. Rank links exist in SkillLineAbility and CooldownSetLinkedSpell.
- UNKNOWN: whether they resolve ranks in practice, and whether `IsSpellKnown(rank1)` stays true after rank 2. P2.
  RangeMaster records the same question as unmeasured (`docs/forever-quirks.md`, smoke RANGE-8).
- Resolution by name is the collection's precedent: `RangeMaster master:core/Compat.lua:169-192` `CurrentSpellID`
  does id, then name, then `C_Spell.GetSpellInfo(name).spellID`, then a known override. It rebuilds on
  `CVAR_UPDATE` because `ShowAllSpellRanks` changes what a name looks up. It is also unmeasured.
- **Recommended, safe whatever P2 says:** store a rank-1 key, ship the rank-id array per entry (from DB2), and at
  rebuild take the highest id that `C_SpellBook.IsSpellKnown` confirms. That is deterministic, independent of locale
  and CVar, and needs no probe. Use name resolution only for user-added spells outside the table.
  Poll, texture, usable and known all use the resolved id. The stored key and the icon key stay the family's.

### What of today's seed survives
VERIFIED, DB2 SpellName against `defaults/Spells.lua`: 21 of 73 distinct (class, id) pairs exist.
- None: Death Knight, Demon Hunter, Evoker, Monk (no such class), Shaman (Wind Shear and the others are absent).
- Same id, different spell or rank: 5211 Bash (was Mighty Bash), 99 Demoralizing Roar (was Incapacitating Roar),
  6789 Death Coil (was Mortal Coil), 19647 is rank 2 of Spell Lock, 6552 and 1766 are rank 1.
- Racial War Stomp 20549 survives. The other four RaceCastStoppers races do not exist here.
- So Forever needs its own list from `wowf` data (clients-§5; `docs/validate-seeds.md` already says so).

## 9. Chat, macros, secure rules
- VERIFIED: KickCD sends no chat, sets no secure attribute, creates no secure button (no match for SendChat,
  C_ChatInfo, SetAttribute in core/modules/settings; `IconGrid_Render.lua:300` avoids SecureActionButton on purpose).
  **No announce restriction applies to the port.**
- For any later announce, VERIFIED: `C_ChatInfo.SendChatMessage` :564 is `HasRestrictions`,
  `RestrictedForMacroChatMessages`, AllowedWhenUntainted, identical on both. The bare `SendChatMessage` is a
  deprecation shim. `InChatMessagingLockdown` :293 exists, and the predicate covers encounter, challenge mode, PvP and
  "communication-restricted map such as a dungeon or raid" (SecretPredicates :65-67).
- QuickComms reads that lockdown on both clients and treats a secret as locked (`master:core/Compat.lua:597-601`,
  `modules/Restrictions.lua:12,87`). It has no Forever measurement: the catalog row is "assumed".
- RestrictedActions and SecretPredicateAPI docs are identical, so combat lockdown for protected frames is as Retail (INFERRED).

## 10. What differs in secrecy
- VERIFIED: in SecretPredicates, Forever adds `SecretWhenLossOfControlRestricted` and widens
  `SecretWhenLossOfControlInfoRestricted` to always secret, the player included. `SecretAspect` adds FrameStrata.
  KickCD reads no loss-of-control API and no frame strata from a tainted frame.
- MEASURED (standard forever-quirks §3, build 70862): the secret system is live (a secret `UnitStat`, a raising aura
  read). Cooldown and `notInterruptible` secrecy are "assumed, not probed" in §2 of that catalog.

## 11. Evidence from the four Forever addons, and the old classification

| Addon | What it proves for KickCD | What it does not |
|---|---|---|
| PartyFrameEnhanced | The cast/channel, duration-object and secret-bool code path ships dual-client | No recorded Forever measurement; party units, not target/focus |
| RangeMaster | Rank resolution pattern, talent/rank event list, nameplate strata | Both rank and talent-event behavior are "Measured: not measured" |
| AuraMaster | Forever seeds are derived from `wowf` DB2 with every rank shipped (`docs/validate-seeds.md:162,177`) | Aura ids, not cast ids |
| QuickComms | Lockdown guard, class-wide spec handled through LibKa0s-Role | No Forever-only quirk recorded |

Re-check of `2026-11-07-WOW_FOREVER_PORT_STEP5/00_CLASSIFICATION.md:56`: "C_CooldownViewer and C_Spell cooldowns
exist" holds. "defaults keyed by Retail spec IDs (Warrior 1491)" holds. "A per-class check of the Cooldown Manager"
is now done from data (1.2). Missed by it: ranks, the pet-spell gap, the two absent/shimmed global families,
class-id holes and the GCD spell.

## 12. In-game probes (owner runs, Forever, record the build)

| # | Where | Command | Settles |
|---|---|---|---|
| P1 | any character | `/dump GetNumClasses(), C_SpecializationInfo.GetAllClassIDs(), GetClassInfo(11), GetNumSpecializationsForClassID, C_SpecializationInfo.GetSpecialization(), C_SpecializationInfo.GetSpecializationInfo(1)` | B4, B6, spec id, behavior below level 10 |
| P2 | rogue with Kick rank 2+ | `/dump C_SpellBook.IsSpellKnown(1766), C_SpellBook.IsSpellKnown(1767), IsPlayerSpell(1766), C_Spell.GetBaseSpell(1767), C_Spell.GetOverrideSpell(1766), C_Spell.GetSpellInfo("Kick").spellID` then, just after a Kick, `/dump C_Spell.GetSpellCooldown(1766).isActive, C_Spell.GetSpellCooldown(1767).isActive` | rank model. Repeat on a shaman (8042/8044) and with ShowAllSpellRanks 1 |
| P3 | each class available | `/dump C_CooldownViewer.IsCooldownViewerAvailable(), #C_CooldownViewer.GetCooldownViewerCategorySet(1,false), #C_CooldownViewer.GetCooldownViewerCategorySet(1,true)` and, on a rogue, `/run for _,i in ipairs(C_CooldownViewer.GetCooldownViewerCategorySet(1,true)) do local c=C_CooldownViewer.GetCooldownViewerCooldownInfo(i) print(c.spellID,c.overrideSpellID,c.isKnown,table.concat(c.linkedSpellIDs,",")) end` | gate shape, works with the CVar off |
| P4 | in combat | `/dump C_Secrets.ShouldSpellCooldownBeSecret(1766), issecretvalue(C_Spell.GetSpellCooldown(1766).duration), C_Spell.GetSpellCooldownDuration(1766):HasSecretValues()` | cooldown secrecy |
| P5 | enemy caster targeted, mid-cast, in and out of combat | `/dump issecretvalue((select(8,UnitCastingInfo("target")))), issecretvalue((UnitCastingInfo("target")))` plus `/kcd debug interrupt`, once on an interrupt-immune mob | cast secrecy, meaningful notInterruptible, nil |
| P6 | any target | `/focus`, then `/dump UnitExists("focus")` | focus |
| P7 | before and after a talent point, a trainer visit, a pet summon | `/etrace` filtered to TALENT, TRAIT, SPELLS_CHANGED, LEARNED, UNIT_PET | rebuild events |
| P8 | a kick that lands | `/etrace`: UNIT_SPELLCAST_INTERRUPTED on target, UNIT_SPELLCAST_SUCCEEDED on player | interrupt events |
| P9 | warlock with felhunter | `/dump C_SpellBook.IsSpellKnown(19244, Enum.SpellBookSpellBank.Pet), C_SpellBook.IsSpellKnown(19647, Enum.SpellBookSpellBank.Pet), C_Spell.GetSpellCooldown(19244)` | pet interrupt. Also ask a paladin and druid whether 425609/410176 is ever trainable |

None of these blocks the build if section 8's rank-array design and the widened gate are used. They are smoke checks.

## 13. Offline experiment
A copy of the snapshot (`work/forever-cooldown-api/kcd`, only the TOC changed to `120105, 16001`) under
`KA0S_KIT_CLIENT=forever`: **1717 passed, 19 failed, 3 skipped**. The failures are skin, font and layout-guard cases
(the Forever default skin is the likely cause, not investigated here) and one SimScenario case. The client-globals
check passed, and **no test failed for B1 to B6**: the mock does not model Forever's specs, ranks or Cooldown Manager.
The port needs Forever fixtures for those three, or a green suite will hide an empty grid.

## 14. Limits
- No client run. Every runtime claim is marked INFERRED or UNKNOWN.
- BIR's forever dump is build 70938, 99 builds behind 71037. The UI source and DB2 are exactly 71037.
- DB2 does not prove a spell is obtainable.
- PlayerCondition gates on racial sets were not decoded.
