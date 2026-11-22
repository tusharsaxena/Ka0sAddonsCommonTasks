# Adversarial fact check of the Forever port research

2026-11-23. Read-only: no repository, game file or remote was written. No client was run.
Raw downloads and scripts are in `/tmp/claude-1000/-mnt-d-Profile-Users-Tushar-Documents-GIT-Ka0sAddonsCommonTasks/ea63b620-1400-4f8d-a094-c4acd4276c35/scratchpad/port/work/factcheck`.

## Sources

| Tag | Source |
|---|---|
| F: | Forever UI 734f065, 1.60.1.71037, under `Interface/AddOns/` |
| L: | Retail UI ab5cb85, 12.1.5.70961 |
| D: | `F:Blizzard_APIDocumentationGenerated/`, file name without `Documentation.lua` |
| DB2 | `https://wago.tools/db2/<Table>/csv?build=1.60.1.71037`, downloaded again for this check (71037 is the newest wowf build listed) |
| BIR | https://github.com/Ketho/BlizzardInterfaceResources branch forever e230342, **build 1.60.1.70938** |
| CT | CombatTrail master 30df90e, `docs/forever-quirks.md` and code |
| SV | The owner's Forever install, read only on 2026-11-23: CombatTrail records (counts only), file presence, four named CVars |

VERIFIED means the cited source says it. For API docs that is a contract and not a runtime observation.

Outcome words: **HELD** (status stands), **REFUTED** (the claim or a load-bearing part is false), **DOWN** (weaker status or narrower scope), **UP** (evidence settles more than claimed).

## Findings that change the plan

### A. Druid Feral Charge is not a cat-and-bear interrupt as claimed (claim 51)

- VERIFIED, DB2 71037: 1238122 has cast mask 145 (cat, bear, dire bear) and triggers 19675 (effect 68, 4 s). 19675's own mask is 144 (bear, dire bear).
- VERIFIED, DB2: two passive form auras replace 1238122 through aura type 332 (SpellEffect misc value = 1238122, base points = the replacement):
  - 1238124, mask 144: replacement **16979 Feral Charge (Bear)**, 15 s, interrupts through 19675.
  - 414925, mask 1: replacement **414924 Feral Charge (Cat)**, "Leap behind an enemy", 30 s in category 2182, GCD 1.5 s, effects 175 and 3 only, **no interrupt**.
- VERIFIED, DB2 Spell 1238122: the description says "Requires Bear Form, Dire Bear Form" and appends `$@spelltooltip414924` for the cat spell.
- INFERRED: it interrupts in bear forms only. The reading of aura 332 follows the same shape in Rebuke's rune aura 425616 ("Gain the Rebuke ability", base points 425609).
- INFERRED: 16979 is reachable as the bear override, although its AcquireMethod is 3. No client row shows what grants the two auras.
- UNKNOWN: what the cooldown readers answer for the base id in each form. Probe, in cat and then bear with the talent:
  `/dump GetShapeshiftFormID(), C_Spell.GetOverrideSpell(1238122), C_Spell.GetSpellName(C_Spell.GetOverrideSpell(1238122)), C_Spell.GetSpellCooldown(1238122)`
  Then charge a caster in each form.
- Effect on the port: keep 1238122 as the stored id, treat it as an interrupt in bear only, and resolve the override before drawing cooldown, usability or texture. Never call 16979 unreachable.

### B. The Cooldown Manager does hold the higher-rank interrupt ids (claim 19)

- VERIFIED, DB2 CooldownSetLinkedSpell 71037: 6554, 1671, 1672, 1767-1769, 8044, 8045, 8046, 10412, 10413 and 10414 are linked rows of their rank-1 entries. Only Spell Lock 19244/19647 is in neither table.
- VERIFIED, KickCD 333cd49 `core/SpellInput.lua:204-205`: the walk reads `info.spellID` only, so refusing 6554 is an addon bug, not a data gap.
- UNKNOWN: whether runtime `linkedSpellIDs` returns them. Probe on a rogue:
  `/run for _,i in ipairs(C_CooldownViewer.GetCooldownViewerCategorySet(1,true)) do local c=C_CooldownViewer.GetCooldownViewerCooldownInfo(i) if c then print(c.spellID,table.concat(c.linkedSpellIDs,",")) end end`
- Effect: "no higher ranks in the table" is not a reason to make the gate absent on Forever. Spell Lock and the uncurated-list argument still are.

### C. The meter probably collects with `damageMeterEnabled` 0 (claim 32)

- VERIFIED, SV: none of the three Forever characters' `config-cache.wtf`, nor the account cache, stores `damageMeterEnabled`. The same files do store `cooldownViewerEnabled "1"` and, for one, `damageMeterResetOnNewInstance "1"`, which have the same scope and flags.
- VERIFIED, BIR CVars:602: the default is "0" (70938).
- VERIFIED, SV and CT: 500 final fights on 70888-71037 came from `C_DamageMeter`, and CT never writes the CVar.
- INFERRED: collection runs with the CVar at 0, so "switch the built-in meter on" must not be shown as a requirement.
- Settle with: `/dump GetCVar("damageMeterEnabled"), C_DamageMeter.IsDamageMeterAvailable()`, then fight and `/dump #C_DamageMeter.GetAvailableCombatSessions()`.

### D. The local row's rate is measured (bears on 7, 27, 29, 30)

- VERIFIED, CT code `modules/Meter.lua:496-547`: the probe's "live DPS figure" has three rungs, and rungs a and c read `amountPerSecond` from the per-source struct, which has no such field (D:DamageMeter:182-191; measured "dps nil").
- INFERRED from that and the 70888 trial (secret in combat, 69.5625 after): it came from the local `combatSources` row. So that row's rate is present in and out of combat, and `isLocalPlayer` is plain in combat, for a solo player.
- The standard's "player source's amountPerSecond is nil out of combat" is about the other struct. An ally's row is still UNKNOWN.

### E. The recommended library replacement repeats the class-loop bug (bears on 24, 48)

- VERIFIED, LibKa0s `LibKa0s/Role.lua:168-175`, same in the vendored copy: `SpecsForClass` loops `1..GetNumClasses()` into `C_CreatureInfo.GetClassInfo`, whose argument is a **classID** (D:CreatureInfo:10-19).
- patterns.md G4 recommends that function. If the count is 9 it loses Druid too. ConsumableMaster `core/SpecHelper.lua:55` has the same loop and is already on Forever.
- `C_SpecializationInfo.GetAllClassIDs` is Forever-only (D:SpecializationInfo:57; absent in L:), so a shared fix needs a Retail rung.

### F. Two small traps found on the way

- VERIFIED: the options for `AbbreviateNumbers` are `{ config = cfg }` (D:Localization:26-36,182-190). CT `modules/Format.lua` `abbreviateWith` passes the config object as the options argument. Do not copy it, and do not take CT's "config" trial as evidence.
- VERIFIED: Blizzard's own meter formats secrets with `AbbreviateLargeNumbers` (F:Blizzard_DamageMeter/DamageMeterEntry.lua:125-131; AllowedWhenTainted at D:Localization:10-13). No report tried it. Its rendering of 69.5625 is UNKNOWN: `/dump AbbreviateLargeNumbers(69.5625), AbbreviateLargeNumbers(30190.47)`.

## Verdicts

### mm-code.md

| # | Claim | Was | Now | Evidence |
|---|---|---|---|---|
| 1 | C_DamageMeter identical apart from specIconID | VERIFIED | HELD VERIFIED | Own diff: only D:DamageMeter:203,242. Constants identical. Eight functions and three events in BIR 70938 |
| 2 | specIconID secret out of combat too | INFERRED | **DOWN UNKNOWN** | `SecretValue = true` has no predicate, but no source defines the flag and nobody read the field in game. Blizzard's added `issecretvalue` (DamageMeterEntry.lua:54) does not say when. Probe: after combat `/run print(issecretvalue(C_DamageMeter.GetCombatSessionFromType(0,0).combatSources[1].specIconID))` |
| 3 | Nine classes, one spec, all damage, one icon per class | VERIFIED | **REFUTED in part** | DB2: nine, one each, Role 2, SpellIconFileID 625999-626008. But the runtime answer measured on 70862 has **no icon** (CT quirks:215-219), so "one icon per class" does not hold for `GetSpecializationInfo`. What the meter's icon holds is UNKNOWN (draw it). "Spec role says nothing beyond class" stands |
| 4 | FormatNumber refuses a secret, the two helpers accept | VERIFIED | HELD VERIFIED | D:NumericFormatterAPI:11-14, D:Localization:26-29, D:StringUtil:106-108. CT quirks:287-298, 70888 |
| 5 | AbbreviateConfig keeps the decimal formats | UNKNOWN | HELD UNKNOWN | `RequiresRestrictedAbbreviationBreakpoints`, FailureMode Error (D:LocalizationShared:49), conditions undocumented. The error enum includes InvalidBreakpoint and NotMultipleOfTen, so 0.001 may fail. See F. Probe: the report's P3, on a plain value, then a secret |
| 6 | Surname second, 12+12 letters, GetUnitName and Ambiguate keep it whole | VERIFIED | HELD VERIFIED | W1_FOREVER_NAME_PROBE.md (70790). F:Blizzard_CharacterCreate/Camelot/Blizzard_CharacterCreate.xml:590,608. GlobalStrings 34055. Separator " " (BIR LuaEnum:9558) |
| 7 | An ally row's amountPerSecond present | UNKNOWN | HELD UNKNOWN | Local row: see D. Ally probe: grouped, `/run for _,r in ipairs(C_DamageMeter.GetCombatSessionFromType(1,0).combatSources) do local v=r.amountPerSecond print(issecretvalue(v) and "secret" or v) end`, mid-fight and after |
| 8 | EnemyDamageTaken gives a row per attacker | UNKNOWN | HELD UNKNOWN | The only measurement is one row with the whole total, solo (CT quirks:280-284). Two-player probe stands |
| 9 | Forever folds a pet into its owner's source | VERIFIED | **DOWN**: VERIFIED for Hunter pets, UNKNOWN otherwise | CT quirks:241-262 (70888). SV holds Hunters only. Probe: fight with a demon, totem and guardian, print each row's name and class |
| 10 | No arena or scenario maps, no housing UI, Delve APIs present | VERIFIED | HELD VERIFIED | DB2 Map InstanceType counts 0:18 1:42 2:13 3:5. Scenario not served at 71037, served for Retail. All 17 housing TOCs `standard`. `C_DelvesUI.HasActiveDelve` in BIR |
| 11 | C_DeathRecap and OpenDeathRecapUI work as loaded code | VERIFIED | **DOWN**: existence VERIFIED, "work" INFERRED | Doc identical. `OpenDeathRecapUI` in BIR FrameXML 70938. Never opened. Probe: die, then `/run OpenDeathRecapUI()` |
| 12 | Avoidable may never populate | UNKNOWN | HELD UNKNOWN | GlobalStrings 57100, DamageMeterSessionWindow.lua:712-714 |

### kc-code.md

| # | Claim | Was | Now | Evidence |
|---|---|---|---|---|
| 13 | Spec ids 1482, 1484-1491, pet 1493 | VERIFIED | HELD VERIFIED | Whole ChrSpecialization read: those ten rows, no 1483 |
| 14 | KickCD's APIs and events documented identically | VERIFIED | HELD VERIFIED (documentation) | Own name-driven diff of every KickCD identifier: 58 matched blocks. The only difference is `SetFrameStrata` secrecy, which is outside the claim |
| 15 | IsPlayerSpell and IsSpellKnown are CVar shims | VERIFIED | HELD VERIFIED | Deprecated_SpellBook.lua:4-19, neither is in BIR GlobalAPI. The shim maps IsSpellKnown to IsSpellInSpellBook, not to C_SpellBook.IsSpellKnown |
| 16 | Global GetNumSpecializationsForClassID absent | VERIFIED | **DOWN INFERRED** | TOC `classic, standard`, only definition. The sibling GetSpecialization measured nil 2026-11-07. This global itself was never dumped: `/dump GetNumSpecializationsForClassID`. The member is VERIFIED (D:SpecializationInfo:136, BIR) |
| 17 | Each rank its own id | VERIFIED | HELD VERIFIED | SpellName, Spell, SkillLineAbility. Same-name unreachable rows exist (Kick 1775, 3467; Earth Shock 408681.., 1220744..), so a name-only derivation is wrong |
| 18 | Superseded rank known, lookups walk ranks | UNKNOWN | HELD UNKNOWN | D:SpellBook:719-756 says nothing of ranks. Probe P4 stands |
| 19 | CDM table holds no higher-rank interrupt and no Spell Lock | VERIFIED | **REFUTED in part** | See B. "No Spell Lock" holds |
| 20 | Cast reads secret, the sinks accept secrets | VERIFIED | HELD VERIFIED (documentation) | D:SecretPredicates:115-117. SimpleFrameAPI:1144, SimpleStatusBarAPI:228,354, SimpleFontStringAPI:538,663,674, CurveUtil:48. Not secret when the unit is the player or pet. The bool sinks are non-nilable while the flag is nilable |
| 21 | Enemy casts exposed, notInterruptible meaningful | UNKNOWN | HELD UNKNOWN | GameRule TargetCastBarDisabled 106 exists. Probe: `/dump C_GameRules.IsGameRuleActive(Enum.GameRule.TargetCastBarDisabled)`, then a live cast |
| 22 | Focus: frame, bar, slash, binding, event | VERIFIED | **DOWN** for the slash: INFERRED. Rest VERIFIED | `FocusFrame` in BIR Frames. `/focus` registers only if the active game mode allows the category (SlashCommands.lua:234-300), and Camelot's mode value is not measured. Probe: `/dump C_GameRules.GetActiveGameMode()`, `/focus` |
| 23 | Kicks on the GCD, glow drops each GCD | INFERRED | HELD INFERRED | DB2 133 with 1.0-1.5 s. Retail 12.1.5.70961 has 0 for the same kicks. `ready = not isActive` at Cooldowns.lua:186. Probe: press any instant and read `C_Spell.GetSpellCooldown(id).isActive` |
| 24 | GetNumClasses iteration may miss Druid | INFERRED | **DOWN UNKNOWN** | Ids are 1-5,7,8,9,11. The count and GetClassInfo's argument semantics are unshown, and https://warcraft.wiki.gg/wiki/API_GetNumClasses says Classic changed them over time. See E. `/dump GetNumClasses(), GetClassInfo(9), GetClassInfo(11), C_SpecializationInfo.GetAllClassIDs()` |

### forever-meter-api.md

| # | Claim | Was | Now | Evidence |
|---|---|---|---|---|
| 25 | Full match: 8, 3, 7, every field | VERIFIED | HELD VERIFIED | As 1. Seven enums counted |
| 26 | specIconID always secret, key collapses, class fallback unreachable | INFERRED | **DOWN**: "always" UNKNOWN, in-combat consequence INFERRED | As 2. The code consequence follows only where the field is secret (Aggregator_Identity.lua:118-123, Row_NameCell.lua:416) |
| 27 | Amounts, rates, creature names secret in combat, plain after | VERIFIED | **DOWN**: VERIFIED for a solo Hunter's own rows on 70888, INFERRED generally | CT quirks:264-271,246-249,288-294. D: SecretWhenInCombat. SV recount 500 final, 103 party, all Hunter. SV cannot count sealed reads, so it does not prove "always plain after". Probe P2 for group and edge |
| 28 | Formatter raises, MultiMeters falls back on every combat cell | VERIFIED | **DOWN** for the second half: INFERRED | Refusal as 4. The ladder consequence is from Format.lua:525-546 and only for secret cells, MultiMeters never ran there. Probe: `/mm` in combat on 16001, read the cells |
| 29 | Rate is on the rows, not on the source struct | VERIFIED | HELD VERIFIED | D:DamageMeter:182-205. See D |
| 30 | Four NeverSecret fields plain in combat | INFERRED | HELD INFERRED | D:202,206,207,209. `isLocalPlayer` has indirect support, see D. Probe P1 |
| 31 | Meter loads, both CVars default 0, checked apart | VERIFIED | HELD VERIFIED | TOC:2, DamageMeter.lua:166-177, `DamageMeter` in BIR Frames. Defaults are 70938, not 71037 |
| 32 | Collection with the CVar at 0, failureReason | UNKNOWN | **UP INFERRED** for collection. failureReason UNKNOWN | See C |
| 33 | Roster loses the surname, GetUnitName gives the full name | VERIFIED | HELD VERIFIED | As 6. Compat.lua:770-775 keeps one return, Roster.lua:446 stores it |
| 34 | Format of meter player names | UNKNOWN | HELD UNKNOWN | CT stores no player row name. Probe P3 stands |
| 35 | Death recap with Retail shape, content unmeasured | INFERRED | HELD INFERRED | As 11 |
| 36 | SendChatMessage identical, lockdown in content unknown | UNKNOWN | HELD UNKNOWN (doc half VERIFIED) | Block diff identical, D:ChatInfo:563. Probe P10 |

### forever-cooldown-api.md

| # | Claim | Was | Now | Evidence |
|---|---|---|---|---|
| 37 | One spec each, GetSpecialization 1 and the class-wide id | VERIFIED | **DOWN**: data VERIFIED, runtime VERIFIED for Hunter only, INFERRED for the other eight | CT quirks:215-219, OutfitterReborn probes:11. `/dump C_SpecializationInfo.GetSpecializationInfo(C_SpecializationInfo.GetSpecialization())` per class |
| 38 | CDM ships, nine sets, rank 1 with linked ranks, no Spell Lock | VERIFIED | HELD VERIFIED (data) | Own counts 72,70,54,48,57,69,56,47,70. `EssentialCooldownViewer` in BIR Frames |
| 39 | Getters answer with the CVar off | INFERRED | **DOWN UNKNOWN** | The unconditional call is UI code, not an answer. All three of the owner's characters run with the CVar at 1, so no evidence exists. `/run SetCVar("cooldownViewerEnabled",0) print(#C_CooldownViewer.GetCooldownViewerCategorySet(1,true))` |
| 40 | Retail cooldown contract | VERIFIED | HELD VERIFIED (documentation) | D:Spell:290,308,326, D:SpellShared:19-30, SecretPredicates:89-92. Per-spell flags outrank the restriction |
| 41 | Per-kick secrecy flags | UNKNOWN | HELD UNKNOWN | Probe P4 stands |
| 42 | Cast info secret regardless of combat, two events carry only the unit | VERIFIED | HELD VERIFIED (documentation) | D:Unit:827,869,4744-4773. Plain when the target is the player or pet |
| 43 | notInterruptible populated and never nil | UNKNOWN | HELD UNKNOWN | D:Unit:827 Nilable. Probe P5 |
| 44 | Focus fully supported | VERIFIED | **DOWN INFERRED** for "fully" | Pieces VERIFIED, never used in game, slash as 22 |
| 45 | Every rank an id, category cooldowns, GCD rule | VERIFIED | **REFUTED in part** | Silence 15487 has RecoveryTime 45000 and category 0, so "interrupts use category cooldowns" is false for it. Feral Charge carries both. Category 88 and the GCD list hold. The cat spell 414924 has a 1.5 s GCD |
| 46 | IsSpellKnown(rank1) after rank 2 | UNKNOWN | HELD UNKNOWN | As 18 |
| 47 | Three spec globals absent, two spellbook shims | INFERRED | HELD INFERRED | As 16. GetSpecialization itself VERIFIED nil in game 2026-11-07 |
| 48 | The loop misses Druid | INFERRED | **DOWN UNKNOWN** | As 24 |

### forever-interrupt-data.md

| # | Claim | Was | Now | Evidence |
|---|---|---|---|---|
| 49 | Spec ids, trees are groups | VERIFIED | HELD VERIFIED | ChrSpecialization, TraitNodeGroupDisplayInfo (27 rows) |
| 50 | Class interrupts, cooldowns, lockouts | VERIFIED | HELD VERIFIED (data) | Every id re-read: effect 68, SpellMisc to SpellDuration, CategoryRecoveryTime, class skill line with AcquireMethod 0. See the id table |
| 51 | Druid: 1238122 in cat and bear, 16979 unreachable | VERIFIED | **REFUTED in part, rest DOWN to INFERRED** | See A. Talent gate of 10 points (TraitCond 42785) and Skull Bash's method 3 hold |
| 52 | Silence interrupts with a 3 s lockout through a server link | INFERRED | **DOWN UNKNOWN** for the lockout | Silence, 45 s, 5 s, 20 points (TraitCond 43492) are VERIFIED. 1241057 is linked only by description text, no effect triggers it. Probe: Silence a casting mob and try the same school after 5 s, and an immune-to-silence caster |
| 53 | Only pet interrupt is Spell Lock | VERIFIED | HELD VERIFIED (data) | Effect-68 closure over all skill lines. Items 16388/16389 teach 19244/19647 |
| 54 | Paladin and Hunter none, Rebuke unreachable | INFERRED | HELD INFERRED | 425609 method 3, reached only by 425616 and enchant 7042. No `C_Engraving` in BIR 70938. A server grant cannot be excluded. `/dump C_SpellBook.IsSpellKnown(425609)` on a Paladin |
| 55 | Retail seed cannot be filtered by presence | VERIFIED | HELD VERIFIED | 99 Demoralizing Roar, 23920 no skill line, trait, item or trigger, seed lists 19647 only (Spells.lua:92,295,335) |
| 56 | Supersede chains, known answer unknown | UNKNOWN | HELD UNKNOWN (chains VERIFIED) | SupercedesSpell re-read |
| 57 | Shared categories, GCD | VERIFIED | HELD VERIFIED (data), runtime UNKNOWN | 88, and 19 (Flame and Frost Shock 6000 ms). Cat Feral Charge excepted, it is not an interrupt |
| 58 | Bare GetNumSpecializationsForClassID undefined | INFERRED | HELD INFERRED | As 16 |
| 59 | Shims behind the CVar | VERIFIED | HELD VERIFIED | As 15 |
| 60 | 61304 absent from client data | VERIFIED | HELD VERIFIED (data) | No row in any table named. Runtime answer UNKNOWN: `/dump C_Spell.GetSpellCooldown(61304)` after an instant |

### patterns.md

| # | Claim | Was | Now | Evidence |
|---|---|---|---|---|
| 61 | specIconID the only doc differences | VERIFIED | HELD VERIFIED | As 1 |
| 62 | Meter and CDM load | VERIFIED | HELD VERIFIED | TOCs and both frames in BIR Frames 70938 |
| 63 | Both formatters raise | VERIFIED | HELD VERIFIED on 70888 | As 4. Unmeasured on 71037 |
| 64 | Secret specIconID can go to SetTexture | VERIFIED | HELD VERIFIED (documentation) | D:SimpleTextureBaseAPI:603-606. KickCD IconGrid.lua:300-303 comments the opposite for spell textures, so pcall or smoke it. What it draws is UNKNOWN |
| 65 | Global nil, member exists | INFERRED | HELD INFERRED | As 16 |
| 66 | Kit scan passes, cannot see guarded calls | VERIFIED | HELD VERIFIED | Rerun on own armed copies under the forever profile: scan PASS for both (1716/20/3, 2611/46/3). Header's GUARDED rule |
| 67 | IsPlayerSpell and IsSpellKnown available | UNKNOWN | **UP INFERRED** on this install | Default "1" (BIR CVars:1016), no override in the Forever Config.wtf. Still dump them |
| 68 | Class-wide spec, trees through Role.Groups | VERIFIED | HELD VERIFIED (Hunter runtime, all classes data) | Role.lua marks its group order "MATCHED, NOT CONFIRMED" |
| 69 | Surname, identity and ruleset key | VERIFIED | HELD VERIFIED | Name probe 70790, D:Unit:536 |
| 70 | Every rank an id, linked by name, two tables absent | VERIFIED | **DOWN** | Ids hold. "Linked by name" is not universal: 9634 Dire Bear Form supersedes 5487 Bear Form, and same-name unreachable clones exist (17). The tables are not served for 71037 and are served for Retail, so absent is INFERRED |
| 71 | v1.110.0 not needed, one parity failure each | VERIFIED | HELD VERIFIED | Four-file diff and both trial logs, one FAIL each (parity). It also does not fix E |
| 72 | No Retail-seeded profiles on Forever | UNKNOWN | **UP VERIFIED** for this install | No KickCD.lua, MultiMeters.lua or .bak in any account or character SavedVariables under `_forever_` on 2026-11-23, though both addon folders are present. A running session writes only at logout, so look again at flip time |

## Spell ids, checked against DB2 71037

| Class | Ability | Ids | Cooldown | Lockout | GCD | Forms | Verdict |
|---|---|---|---|---|---|---|---|
| Warrior | Pummel | 6552, 6554 | 10 s, cat 88 | 4 s | 1.5 | Berserker | correct |
| Warrior | Shield Bash | 72, 1671, 1672 | 12 s, cat 88 | 6 s | 1.5 | Battle, Defensive | correct |
| Rogue | Kick | 1766, 1767, 1768, 1769 | 10 s, cat 88 | 5 s | 1.0 | - | correct, exclude 1775 and 3467 |
| Mage | Counterspell | 2139 | 30 s, cat 88 | 10 s | 0 | - | correct |
| Shaman | Earth Shock | 8042, 8044, 8045, 8046, 10412, 10413, 10414 | 6 s, cat 19 | 2 s | 1.5 | - | correct, exclude the clone families |
| Priest | Silence | 15487 | 45 s, own | 3 s UNKNOWN, silence 5 s | 1.5 | mask lists Shadowform (same as Mind Blast) | id correct |
| Druid | Feral Charge | 1238122 to 16979 in bear | 15 s, cat 2182 | 4 s through 19675 | 0 | bear, dire bear | corrected |
| Druid | Feral Charge (Cat) | 414924 | 30 s, cat 2182 | none | 1.5 | cat | not an interrupt |
| Warlock pet | Spell Lock | 19244, 19647 | 30 s, cat 88 | 6 s, 8 s | 1.5 | - | correct |
