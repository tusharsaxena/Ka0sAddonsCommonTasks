# forever-meter-api: what MultiMeters can rely on in WoW Forever

Study date 2026-11-23. Read-only: no repository or game file was written, no suite was run, nothing was run in a client.

## Sources and how to read the citations

| Tag | Source |
|---|---|
| `F:` | Forever UI source 734f065, 1.60.1.71037, paths under `Interface/AddOns/` |
| `L:` | Retail UI source ab5cb85, 12.1.5.70961, same root |
| `F:API/X`, `L:API/X` | `Blizzard_APIDocumentationGenerated/XDocumentation.lua` |
| `MM:` | MultiMeters snapshot, master bf67258 |
| `CT:` | CombatTrail master 30df90e |
| `SV` | CombatTrail Forever SavedVariables, copied 2026-11-23 (500 stored fights, builds 70888 to 71037). Shapes and counts only |
| `BIR` | https://github.com/Ketho/BlizzardInterfaceResources, branch `forever` e230342 = **1.60.1.70938** (99 builds behind the UI source, committed 2026-11-14), and branch `live` |
| `WIKI` | https://warcraft.wiki.gg/wiki/Secret_Values and .../API_C_ChatInfo.SendChatMessage, read 2026-11-23. A secondary source |

VERIFIED = the cited source or measurement says it. For documentation that means "documented", not "seen in game". INFERRED = reasoning given. UNKNOWN = probe given (section 12).

## 0. Verdict

The port is feasible on the same reader. The API is the same on both clients apart from one annotation (`specIconID`). Nothing found blocks the port. Five things need work:

1. `specIconID` is secret. The mid-combat identity key loses its spec part, the class-icon fallback is never reached, and the CSV spec field goes empty.
2. The number formatter MultiMeters is built on refuses secrets from addon code (measured on Forever 70888). In combat every cell uses the `AbbreviateNumbers` fallback and ignores the chosen number mode.
3. Names: `UnitName` gives the first name only and the surname second. MultiMeters drops the surname, and joins and shows names on that half.
4. `GetSpecialization*` describes one class-wide spec, so the role fallback is wrong for hybrids.
5. Four things cannot be settled from source: whether data is collected with the meter CVar off (default 0), the format of meter names, death recap content, and chat lockdown in Forever dungeons.

The 2026-11-07 classification is out of date on one point. "About 50 `specIconID` reads, each need a guard" counts comments, fixtures and probes. The code has six live sites (section 4) and none of them raises as written. Three change behaviour.

## 1. C_DamageMeter: full comparison

Method: a block-by-block comparison of every entry in `API/DamageMeter` and `API/DamageMeterConstants`, plus a whole-file diff. VERIFIED.

### Functions (8 of 8, identical, at the same lines)

| Function | Line | Secrecy | Returns |
|---|---|---|---|
| `GetAvailableCombatSessions()` | 10 | none documented | array of sessionID, name, durationSeconds? |
| `GetCombatSessionFromID(id, type)` | 20 | `SecretWhenInCombat` | session |
| `GetCombatSessionFromType(sessionType, type)` | 38 | `SecretWhenInCombat` | session |
| `GetCombatSessionSourceFromID(id, type, guid?, creatureID?)` | 56 | `SecretWhenInCombat` | source |
| `GetCombatSessionSourceFromType(sessionType, type, guid?, creatureID?)` | 76 | `SecretWhenInCombat` | source |
| `GetSessionDurationSeconds(sessionType)` | 96 | **none documented** | number? |
| `IsDamageMeterAvailable()` | 112 | none | bool, failureReason |
| `ResetAllCombatSessions()` | 123 | none, not protected | nothing |

All that take arguments are `SecretArguments = AllowedWhenUntainted`: addon code cannot pass a secret GUID or creature ID back for a drill-down. MultiMeters already knows this (MM:modules/Aggregator_Identity.lua, "LET THE CLIENT DO THE JOIN").

The functions also exist in the running client: CT:docs/forever-quirks.md (probe, build 70862), and SV shows session, source and EnemyDamageTaken reads producing plain records on 71037.

### Events (3 of 3, identical): `F:API/DamageMeter:130-152`

`DAMAGE_METER_COMBAT_SESSION_UPDATED(type, sessionID)`, `DAMAGE_METER_CURRENT_SESSION_UPDATED`, `DAMAGE_METER_RESET`, all `UniqueEvent`. Payload fields carry no secrecy annotation. All three are in BIR Events at 70938. Firing cadence on Forever is UNKNOWN (P9).

### Enums (7 of 7, identical files)

| Enum | Values |
|---|---|
| DamageMeterType | DamageDone 0, Dps 1, HealingDone 2, Hps 3, Absorbs 4, Interrupts 5, Dispels 6, DamageTaken 7, AvoidableDamageTaken 8, Deaths 9, EnemyDamageTaken 10 |
| DamageMeterSessionType | Overall 0, Current 1, Expired 2 |
| DamageMeterSourceDisplayType | None 0, Ally 1, Enemy 2 |
| DamageMeterSpellDetailsDisplayType | SpellCasted 0, UnitSpecificSpellCasted 1, SpellAffected 2, Deaths 3, EnemyDamageTaken 4 |
| DamageMeterStorageType | Damage 0, HealingAndAbsorbs 1, Absorbs 2, Interrupts 3, Dispels 4, DamageTaken 5, AvoidableDamageTaken 6, Deaths 7, EnemyDamageTaken 8 |
| DamageMeterCombineSessionType | None 0, ChallengeMode 1, Arena 2, ArenaMultiRound 3 |
| DamageMeterOverrideType | Ignore 0, AllowFriendlyFire 1, RedirectSourceToOwner 2, RedirectSourceToAuraCaster 3, IgnoreForAbsorbSpell 4 |

The literal fallbacks in MM:core/Constants.lua:124-158 are correct for Forever.

### Structures and secrecy

"Combat" below means secret while the Combat restriction is active, through the function's predicate.

| Structure | Field | Retail | Forever |
|---|---|---|---|
| AvailableCombatSession | sessionID, name, durationSeconds? | no annotation | same |
| CombatSession | combatSources, maxAmount, totalAmount, durationSeconds? | combat | same |
| CombatSessionSource | combatSpells, maxAmount, totalAmount | combat | same. **There is no `amountPerSecond` field here on either client** |
| CombatSource | sourceGUID?, name | ConditionalSecret | same |
| | sourceCreatureID? | combat | same |
| | classFilename, isLocalPlayer, deathRecapID, classification | NeverSecret | same |
| | **specIconID** | **NeverSecret** | **SecretValue** (`F:API/DamageMeter:203`) |
| | totalAmount, amountPerSecond, deathTimeSeconds | combat | same |
| | sourceDisplayType, factionGroup? | combat | same |
| CombatSpell | spellID, totalAmount, amountPerSecond, creatureName, overkillAmount, isAvoidable, isDeadly, combatSpellDetails | combat | same |
| CombatSpellUnitDetails | unitName, isPet, isMob, amount | combat | same |
| | unitClassFilename, classification | NeverSecret | same |
| | **specIconID** | **NeverSecret** | **SecretValue** (`F:API/DamageMeter:242`) |

These two lines are the whole difference between the files.

Correction to a collection record: forever-quirks §5 and CT's quirk list "the player source's `amountPerSecond` is nil" as a Forever finding. The *source* structure has no such field on either client, so nil is expected on both. The per-second figure is on the session's `combatSources` row and on each spell row. CT measured that: EnemyDamageTaken rows carry `amountPerSecond`, and the live figure comes from the local row (70888). MultiMeters reads the row (MM:modules/Provider.lua:277), so it is unaffected.

## 2. What was measured on Forever

| Fact | Status | Evidence |
|---|---|---|
| In combat the player's `totalAmount` is secret, and plain about 2 s after | VERIFIED 70888, solo | CT quirk "In combat on WoW Forever, the meter is secret" |
| The row rate is secret in combat and a plain float after (69.5625) | VERIFIED 70888 | CT quirk "client number formatters refuse a secret" |
| Spell-row `creatureName` is secret in combat, plain after. The owner's rows read `""`, not nil | VERIFIED 70888 | CT quirk "folds the pet" |
| The pet is folded into the owner's source. Its spells are rows with `creatureName` set, and its melee is a second Auto Attack row. A pet GUID query answers an empty source | VERIFIED 70888, Hunter only | CT quirks. SV: 473 of 500 fights stored a split pet part, 6 of 7 on 71037 |
| EnemyDamageTaken has one row per enemy with `sourceCreatureID` and no `sourceGUID`. The drill-down works by creature ID | VERIFIED 70888, solo | CT quirk |
| That drill returned one row, spellID 0, creatureName "", holding the whole total | VERIFIED 70888, solo | CT quirk. CT did not print `combatSpellDetails`, so a per-caster breakdown is not ruled out |
| EnemyDamageTaken's session `totalAmount` is not always the sum of its rows | VERIFIED 70888, one case of 579 against 1183 | CT quirk |
| Totals, names of targets, creature names and durations read plain after combat in dungeons | VERIFIED 70888, 70938, 70959 | SV: 103 `party`, difficulty 1 fights, all `status = final`, all with named targets. CT's reader stores only plain values (`Meter.ReadFinal`) and retries a sealed read for up to 5 s |
| The same in the open world on the current build | VERIFIED 71037 | SV: 7 fights, all final with named targets |
| EnemyDamageTaken counts more than the player's own damage | INFERRED | SV: the target sum exceeds the player's total by more than 5% in 103 of 103 dungeon fights and 126 of 338 world fights, and is never below 95%. Other attackers' damage is the natural reading |
| The stored evidence covers one class only | VERIFIED | SV: 500 of 500 HUNTER |

SV limits: it holds no raw rows and no in-combat sample. Its `meterDps` is no evidence for the API rate, because CT falls back to total/duration when the pet is split and the two values are equal in all 500 records. Nothing here measures a raid, battleground or PvP. SV cannot show how many fights were lost as sealed.

### Consequences of pet folding

- INFERRED: the Retail row rules for separate pet sources will mostly idle on Forever, and totals already include pets. A guardian or a non-Hunter pet is UNKNOWN (P4).
- MultiMeters never reads `creatureName` (no hit in `modules/`), so a drill-down shows two indistinguishable "Auto Attack" rows for a player with a pet. A cosmetic fix: show the creature name when it is plain.

## 3. Restriction states and secrecy

VERIFIED by diff:

- `API/RestrictedActions` and `API/RestrictedActionsConstants` are identical: `IsAddOnRestrictionActive`, `GetAddOnRestrictionState`, `ADDON_RESTRICTION_STATE_CHANGED(type, state)`; states Inactive 0, Activating 1, Active 2; types Combat 0, Encounter 1, ChallengeMode 2, PvPMatch 3, Map 4, Chat 5.
- `C_Secrets` (`API/SecretPredicateAPI`) is identical.
- `API/SecretPredicates` differs only in the two LossOfControl predicates, which MultiMeters does not use.
- `SecretWhenInCombat` reads "when combat addon restrictions are in effect" on both (`F:API/SecretPredicates:93-97`).
- `issecretvalue`, `canaccessvalue`, `issecrettable`, `canaccesstable` are in BIR GlobalAPI at 70938.
- WIKI: addon code may truth-test a non-boolean secret, concatenate it, `string.format` it, store it as a value and pass it to C APIs marked `AllowedWhenTainted`. It may not compare, calculate, key, index, or take a length.

INFERRED: MM:core/Secrets.lua needs no change. Every primitive it uses exists with the same contract. The meter-secret edge is measured only as "secret at combat+5 s, plain at afterCombat+2 s". That it is exactly the Combat restriction edge, and that a dungeon between pulls is plain immediately, is UNKNOWN (P2).

`GetSessionDurationSeconds` has no predicate on either client, so INFERRED plain in combat, while `session.durationSeconds` is secret through its function. MM:core/Compat.lua's comment says both are secret. Both work through `Format.Duration`.

| Value | Out of combat | In combat | Status |
|---|---|---|---|
| totalAmount, row rate | plain | secret | VERIFIED 70888 |
| creatureName | plain | secret | VERIFIED 70888 |
| Source `name` | plain for enemies (SV) | secret | out: VERIFIED for enemies. In: INFERRED from predicate and ConditionalSecret. Player-name format UNKNOWN (P3) |
| sourceGUID | plain | secret | INFERRED: same annotation as Retail, where MM measured secret and inaccessible. Absent on enemy rows (VERIFIED) |
| classFilename, isLocalPlayer, deathRecapID, classification | plain | plain | documented NeverSecret. In-game value on Forever UNKNOWN (P1) |
| specIconID | secret | secret | INFERRED from `SecretValue = true`, an unconditional field annotation, in contrast to ConditionalSecret. Blizzard added `issecretvalue(texture)` guards for it (section 5). UNKNOWN in game, and what it holds (P1) |
| `UnitGUID`, `UnitName`, `UnitClass` of group members | plain | plain | INFERRED: `SecretWhenUnitIdentityRestricted` (same text on both) exempts player-controlled and party or raid units. Pets and compound tokens may be secret |
| `UnitName` of a non-group target | - | may be secret | documented `SecretWhenUnitNameIdentityRestricted` |

Unit API annotations for `UnitName`, `UnitGUID`, `UnitFullName`, `UnitClass`, `UnitExists`, `UnitIsPlayer`, `UnitAffectingCombat` are identical on both clients.

## 4. specIconID: the six live sites

| Site | With a secret on Forever | Needed |
|---|---|---|
| MM:modules/Provider.lua:274 | copied as an opaque value | none |
| MM:modules/Aggregator.lua:180 | copied | none |
| MM:modules/Aggregator_Identity.lua:118-123 | `IsSecret` turns it to 0, key = class + local flag | Already safe. **Behaviour change:** every same-class pair is ambiguous in combat, so their secondary cells are left empty (`fillCorrelated`, comment at :63). The sort column is unaffected. Common with classic class stacking and worse in raids |
| MM:modules/Row_NameCell.lua:416-417 | the truth test is legal and always true, `SetTexture` accepts secrets (`F:API/SimpleTextureBase`, AllowedWhenTainted) | **Behaviour change:** the class-icon fallback is unreachable. If the secret is 0 the icon is blank, and addon code cannot test for 0. Draw the class icon whenever the field is secret |
| MM:modules/Export.lua:403 | `CsvField` gives "" | No raise. The spec column is always empty |
| MM:core/Diagnostics_Identity.lua, Provider probe | counted as secret | Update the "NeverSecret" wording |

Comments claiming NeverSecret: MM:defaults/Profile.lua:469, MM:settings/Schema.lua:873, MM:modules/Aggregator.lua:168, MM:modules/Row_NameCell.lua:402. Fixtures in `SimWorld` and `Aggregator_Preview` use Retail spec icons and classes.

No plain replacement key exists. The plain fields are classFilename, isLocalPlayer, deathRecapID and classification. `GetInspectSpecialization` is class-wide on Forever, so it would not discriminate either (INFERRED).

## 5. Built-in meter UI, CVars, enablement

VERIFIED:

- `Blizzard_DamageMeter.toc:2` is `AllowLoadGameType: standard, camelot`. The whole addon differs from Retail by:
  - a Camelot override that hides classification icons (`Camelot/DamageMeterEntryOverrides.lua`);
  - `issecretvalue` guards around the icon comparison (`DamageMeterEntry.lua:54`);
  - an unrelated scroll-box refactor (`DamageMeterSessionWindow.lua:747`).
- The stat list, categories and constants are the same, AvoidableDamageTaken included.
- CVars `damageMeterEnabled` and `damageMeterResetOnNewInstance`: **default "0" on both clients**, with the same scope and flags (BIR CVars.lua:602-603 at 70938; live :589-590).
- The checkbox is under Options > **Advanced Options** > Damage Meter on Forever (`F:Blizzard_SettingsDefinitions_Frame/AdvancedOptions.lua:403,415`; BIR string `HUD_EDIT_MODE_DAMAGE_METER_DISABLED_TOOLTIP`). Retail's string says Gameplay Enhancements. Any hint MultiMeters prints must not hard-code the Retail path.
- Shown = CVar is true **and** `IsDamageMeterAvailable()` **and** the Edit Mode visibility (`F:Blizzard_DamageMeter/DamageMeter.lua:166-195`). The CVar and availability are separate checks: availability is "whether the player *can* enable and use" it.
- CT's probe got `IsDamageMeterAvailable() = true` on 70862. CT never writes the CVar.

INFERRED: `IsDamageMeterAvailable` does not report a switched-off CVar, so MultiMeters' "unavailable, switch the built-in meter on" notice (MM:modules/Window_Header.lua:1453, comment at MM:core/Compat.lua:118-121) will not appear for a player who simply has it off. Blizzard's mixin also re-evaluates on `PLAYER_LEVEL_CHANGED`, which suggests a level-dependent answer. MultiMeters' memo is cleared on meter events and world entry only.

UNKNOWN: whether collection runs with the CVar at 0 (P5), and what `failureReason` can say on Forever (no matching global string; P5).

## 6. Death recap

VERIFIED:

- `C_DeathRecap` is identical: `GetRecapEvents`, `GetRecapLink`, `GetRecapMaxHealth`, `HasRecapEvents`, each taking an optional recapID and with no secret predicate. `DeathRecapEventInfo` documents no fields on either client. All four functions are in the client (`GetRecapEvents` checked in BIR GlobalAPI).
- The UI moved to `Blizzard_DeathRecap/Mainline/` and is the same code, except 88163 became `Constants.DeathRecapConsts.SWING_DAMAGE_SPELL_ID` (a Forever-only constants file, same value).
- `OpenDeathRecapUI(id)` is defined in `Mainline/Blizzard_DeathRecap_Bootstrap.lua:7`. The meter opens it for any row with a non-zero recap ID (`DamageMeterSessionWindow.lua:969`), and the death popup asks `HasRecapEvents()` (`Blizzard_StaticPopup_Game/Mainline/GameDialogDefs.lua:203`).

INFERRED: those files load on Forever, because camelot is inside the mainline family (lines such as `[AllowLoadGameType mainline] [ExcludeLoadGameType camelot]` only make sense that way).

UNKNOWN: whether Forever fills recaps, for other players and earlier deaths, how many events, and whether `amount`, `currentHP` or max health are secret in combat (P6). MultiMeters already wraps every reader in `pcall` and degrades.

## 7. Spec and role APIs

VERIFIED:

- `C_SpecializationInfo` keeps every Retail function unchanged and adds `GetAllClassIDs`, `GetCombatConfigIDForSpecGroup`, `HasPlayerEarnedATalentPoint`, `IsSpecSelectionEnabled`, `SetActiveSpecGroup`.
- On 70862 `GetSpecialization` answered 1 and `GetSpecializationInfo` a pseudo spec (Hunter: 1485, name "Hunter", no icon) whatever the talents. Trees come from C_Traits (CT quirk).
- `Blizzard_DeprecatedSpecialization.toc` loads for `classic, standard` only, so the bare `GetSpecialization` and `GetSpecializationInfo` aliases are **absent** on Forever. LibKa0s-Compat reads `C_SpecializationInfo` first (LibKa0s master `LibKa0s/Compat.lua:352,372`), which MultiMeters uses.
- `GetSpecializationRole` and `UnitGroupRolesAssigned` are still C globals on both (BIR).

Consequence: MM:modules/Roster.lua:255-266 falls back from the assigned role to `GetSpecializationRole`, which is class-wide here. clients.md:34 names the fix: `LibKa0s-Role-1.0` `Resolve`. How often `UnitGroupRolesAssigned` answers NONE on Forever, which has no role-queue norm, is UNKNOWN (P7), and it decides how useful the `roster` sort is.

`specIconID` cannot be expected to show a talent tree: INFERRED from the class-wide, icon-less spec. Likely 0 or a class icon (P1).

## 8. Number formatting (the largest hidden dependency)

VERIFIED:

- `NumericFormatter:FormatNumber` is `SecretArguments = AllowedWhenUntainted` **on both clients** (`API/NumericFormatterAPI:11-14`, identical files).
- Measured on Forever 70888: both the abbreviated and the rule formatter raise "Secret values are only allowed during untainted execution for this argument" on a secret from addon code. `AbbreviateNumbers`, `C_StringUtil.FloorToNearestString`, `RoundToNearestString`, `TruncateWhenZero` and `string.format` return secret strings (CT quirk).
- `AbbreviateNumbers` is `AllowedWhenTainted` and takes `options = { breakpointData, locale, config }` (`API/Localization`). `StatusBar:SetValue`, `FontString:SetText` and `Texture:SetTexture` are `AllowedWhenTainted`.

MM:core/Secrets.lua's header and MM:modules/Format.lua:16-18 state that `FormatNumber` accepts secrets. On Forever it does not. The formatter is built successfully from plain probes and cached, then raises on every secret cell, so:

- every cell costs a failing `pcall` on every refresh in combat;
- `abbreviated`, `abbreviatedWhole` and `abbreviatedTwo` all render through bare `AbbreviateNumbers`, so the chosen decimals are lost, and a rate under 1000 shows its tail ("69.5625"), which matters at classic's small numbers;
- `full` falls to `string.format("%s")`, the raw float.

INFERRED fix: use `AbbreviateNumbers(v, options)` with the addon's own breakpoints for secrets and `FloorToNearestString` for whole numbers. A `config` from `CreateAbbreviateConfig` is gated by `RequiresRestrictedAbbreviationBreakpoints` (FailureMode Error), so custom breakpoints under secrets need P8. The same annotation on Retail suggests this is a latent Retail bug too. Retail is not measured.

`C_StringUtil` is otherwise identical on both clients.

## 9. Names

VERIFIED:

- `UnitName` returns first name, surname; only the pair is unique (forever-quirks §4, probe 70790).
- `GetUnitName(unit, true)` is overridden: `F:Blizzard_UnitFrame/Mainline/UnitFrame.lua` passes to `NameUtil.FormatUnitNameForDisplay`, and the Camelot file (`Blizzard_FrameXMLUtil/Camelot/NameUtil.lua:4-12`, loaded by toc:59) returns first + surname separator + surname, whatever the second argument. So the whisper-my-target route gets the full name.
- MM:core/Compat.lua:770 `UnitName` keeps the first return only. MM:modules/Roster.lua:445 stores it as the row name.
- MM:modules/Aggregator.lua:178 prefers the roster name over the meter's.
- MM:modules/Tooltip_Builders.lua:659 looks targets up by `row.name`. MM:modules/Targets.lua keys them by `bareName(combatSpellDetails.unitName)`.

Consequences:

- Two members with one first name show identically in the grid, export and chat.
- INFERRED: if the meter's `name` and `unitName` are full names, a row reads "First" out of combat and "First Last" in identity mode, and **the Targets section never matches for any player**. If they are first-only, Targets merges the two people. Either way use `Compat.UnitCharacterName` (already wired at MM:core/Compat.lua:92, unused). The meter's format decides the join (P3).
- The realm strip (first hyphen) is harmless on names without hyphens. Column widths and the name-length cap need sizing for the two-word form.

## 10. Chat reports and linking

VERIFIED:

- `C_ChatInfo.SendChatMessage` is identical: `HasRestrictions`, `RestrictedForMacroChatMessages`, `SecretArguments = AllowedWhenUntainted` (`F:API/ChatInfo:563`). A secret message, target or a line built from one cannot be sent from addon code.
- `RestrictedForMacroChatMessages` applies only to macro-initiated messages during instance encounters (WIKI).
- SAY and YELL need a hardware event outside instances, CHANNEL everywhere (WIKI). That rule is the one MM:modules/Export.lua:724-741 implements. That Forever enforces the same is INFERRED.
- The bare `SendChatMessage` global exists only through a deprecation addon gated on the `loadDeprecationFallbacks` CVar. `C_ChatInfo.SendChatMessage` is in BIR at 70938 and `Compat.ChatSender` prefers it.
- `InChatMessagingLockdown()` exists and is unchanged. The `SecretInChatMessagingLockdown` predicate names encounters, PvP and "communication-restricted map such as a dungeon or raid". It can answer a secret on Retail (client-quirks §2).
- `ERR_CHAT_PLAYER_NOT_FOUND_S` exists with the same text, so the failed-whisper watcher works.
- Discord chat types are added to `Enum.ChatChannelType` on Forever. They are not export channels.

MultiMeters refuses export only under the Combat restriction and never asks about chat lockdown. Whether an ordinary addon send fails in a Forever dungeon or battleground out of combat is UNKNOWN (P10). `INSTANCE_CHAT` is only meaningful in instance groups, and its use on Forever is UNKNOWN.

Linking: MultiMeters sends plain text and builds no hyperlink (`GetRecapLink` is deliberately not shimmed, MM:core/Compat.lua:228). `C_DeathRecap.GetRecapLink` exists if wanted. Nothing else to port.

## 11. Absent, different, secret: summary

**Absent:** bare `GetSpecialization` and `GetSpecializationInfo` aliases (handled by LibKa0s); a per-player spec; a pet source of its own; `sourceGUID` on enemy rows. No `C_DamageMeter` function, event, enum or field is absent.

**Different:** `specIconID` annotation; class-wide spec; two-part names and `GetUnitName` semantics; settings path; classification icons hidden in Blizzard's meter; death recap files moved; pets folded with `creatureName`.

**Secret:** in combat, all amounts, rates, GUIDs, names, spell rows. Always (INFERRED): `specIconID`. Never (documented): classFilename, isLocalPlayer, deathRecapID, classification.

**Present at 70938 though the content is not:** the events MultiMeters registers for pet battles, gliding and vehicles, and `C_DelvesUI`, `C_PartyInfo.IsDelveInProgress`, `C_Housing`, `C_PlayerInfo.GetGlidingInfo` (BIR GlobalAPI and Events). Feature presence cannot be used to gate Delves, Housing or Skyriding. They need a client declaration (clients §4).

**No data expected (INFERRED):** AvoidableDamageTaken depends on spells flagged avoidable, which classic-era content may lack. The default column set includes Avoidable Damage (MM:core/Constants.lua, `STATS`, `defaultEnabled = true`), so check P11 before keeping it as a Forever default. Challenge-mode session combining has no content.

## 12. In-game probes

Run on 1.60.1.71037+. Each prints shapes only. `D` is `Enum.DamageMeterType`, `S` is `Enum.DamageMeterSessionType`.

P1. Field secrecy, out of combat and then in combat:
```
/run local r=C_DamageMeter.GetCombatSessionFromType(1,0).combatSources[1] if r then for k,v in pairs(r) do print(k,issecretvalue(v) and "SECRET" or type(v)) end end
/run local r=C_DamageMeter.GetCombatSessionFromType(1,0).combatSources[1] local t=UIParent:CreateTexture() t:SetPoint("CENTER") t:SetSize(64,64) t:SetTexture(r.specIconID)
```
The second shows what the secret icon draws. `/reload` clears it.

P2. The secrecy edge, pulled in and out of a dungeon fight:
```
/run local f=CreateFrame("Frame") f:RegisterEvent("ADDON_RESTRICTION_STATE_CHANGED") f:SetScript("OnEvent",function(_,_,t,s) print(t,s,issecretvalue(C_DamageMeter.GetCombatSessionFromType(1,0).totalAmount)) end)
```

P3. Meter name format, grouped, after a fight. Report only whether a space, hyphen or other separator is present:
```
/run for _,r in ipairs(C_DamageMeter.GetCombatSessionFromType(0,0).combatSources) do print(r.name:find(" ") and "space" or "-",r.name:find("-",1,true) and "hyphen" or "-",#r.name) end
```
Repeat on `combatSpellDetails.unitName` from an EnemyDamageTaken drill in the same group. It also settles whether that drill has one row per caster.

P4. Pets: `/ct probe start`, a fight with a Warlock demon, then with a totem or guardian, then `/ct probe`.

P5. Enablement:
```
/run print(GetCVar("damageMeterEnabled"),C_DamageMeter.IsDamageMeterAvailable())
```
Then `/run SetCVar("damageMeterEnabled",0) C_DamageMeter.ResetAllCombatSessions()`, fight, and check `#C_DamageMeter.GetAvailableCombatSessions()` and the session total. Repeat the first line on a level 1 character.

P6. Recap, after another player's death and after your own, in and out of combat:
```
/run for _,r in ipairs(C_DamageMeter.GetCombatSessionFromType(0,9).combatSources) do local i=r.deathRecapID local e=C_DeathRecap.GetRecapEvents(i) print(i>0,C_DeathRecap.HasRecapEvents(i),#e,e[1] and issecretvalue(e[1].amount)) end
```

P7. Roles, in a hand-made and in a queued group: `/run print(UnitGroupRolesAssigned("player"),UnitGroupRolesAssigned("party1"),GetSpecializationRole(1))`

P8. Formatter, in combat:
```
/run local v=C_DamageMeter.GetCombatSessionFromType(1,0).totalAmount print(pcall(AbbreviateNumbers,v,{breakpointData=C_StringUtil.GetDefaultAbbreviationBreakpoints()}))
```
Then with a custom two-decimal breakpoint array, and through a `CreateAbbreviateConfig` config. Run the first on Retail too, with `CreateAbbreviatedNumberFormatter():FormatNumber(v)`.

P9. `/etrace` filtered to `DAMAGE_METER` through one fight, for cadence and payload.

P10. Chat, in a dungeon and a battleground, out of combat and between boss pulls:
```
/run local v=C_ChatInfo.InChatMessagingLockdown() print(issecretvalue(v) and "SECRET" or v, C_RestrictedActions.GetAddOnRestrictionState(4), C_RestrictedActions.GetAddOnRestrictionState(5))
/run C_Timer.After(1,function() C_ChatInfo.SendChatMessage("meter test","PARTY") end)
```

P11. Every stat, after a dungeon run:
```
/run for k,v in pairs(Enum.DamageMeterType) do local s=C_DamageMeter.GetCombatSessionFromType(0,v) print(k,#s.combatSources,s.totalAmount) end
```

## 13. Not checked

- No client was run and no suite was run. Forever behaviour not in section 2 is read from source.
- BIR is build 70938, one step behind 71037. The UI source is 71037.
- Raid, battleground and non-Hunter data: none exists in the evidence.
- The `FormatNumber` refusal on Retail is documented, not measured.
