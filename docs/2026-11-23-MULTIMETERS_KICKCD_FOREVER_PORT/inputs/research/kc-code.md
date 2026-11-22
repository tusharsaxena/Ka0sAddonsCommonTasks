# KickCD: WoW Forever port code audit (kc-code)

Snapshot: KickCD master 333cd49 (v1.5.0, TOC `120105`, LibKa0s v1.109.0, roster `Retail (port pending)`, standard ADDONS.md:25).

Sources and labels:
- **F:** = `port/ui/forever/Interface/AddOns/` (734f065, 1.60.1.71037). **L:** = `port/ui/live/Interface/AddOns/` (ab5cb85, 12.1.5.70961). **D:** = `Blizzard_APIDocumentationGenerated/`.
- **DB2** = `https://wago.tools/db2/<Table>/csv?build=1.60.1.71037`, the newest `wowf` build on 2026-11-23 and the same build as the UI snapshot. Cached in `port/work/kc-code/dl/`.
- VERIFIED = read or run, with the citation. INFERRED = reasoning given. UNKNOWN = probe named (section 12).
- "Simulated" = run in the headless scratch copy with Forever-shaped mocks. It proves KickCD's logic, not client behavior.
- All paths without a prefix are in the KickCD snapshot.

## 0. Verdict

Port. The engine carries over: every cooldown, curve, duration, cast and focus API and every event KickCD uses is documented
on Forever with a definition identical to Retail's. What breaks is identity and data.
Flipping the TOC alone would ship an addon that loads without an error and shows nothing.

| # | Finding | Status | Effect if only the TOC is flipped | Fix |
|---|---|---|---|---|
| B1 | Spell lists are keyed by 39 Retail spec ids; Forever has one spec per class (1482, 1484-1491) | VERIFIED (DB2 ChrSpecialization; simulated) | `GetSpellList("WARRIOR",1491)` is nil: empty grid, sim refuses, Spells Defaults gives 0 entries | Forever seed table keyed by the nine spec ids, picked once by `ClientKey()` |
| B2 | Forever keeps every rank as its own spell id | VERIFIED (DB2 SkillLineAbility, Spell) | A rank-1 entry may stop resolving once rank 2 is trained, or vice versa | Rank-family table and one resolver shared by every consumer |
| B3 | The Cooldown Manager gate has Forever data, rank-1 ids only, no pet spells | VERIFIED (DB2 CooldownSetSpell; simulated) | Adding Pummel rank 2, Kick 2-4, Hammer of Justice 2-4 or Spell Lock is refused as "not tracked" | Gate is Retail-only by declaration |
| B4 | `BuildSpells` seeds only an empty `profile.spells` (core/Database.lua:277) | VERIFIED (simulated: 13 Retail classes seeded, no list for 1491) | Anyone who ran KickCD out of date on Forever keeps an empty grid after the port | Forever-only per-profile backfill of absent class/spec keys |
| B5 | Availability rests on `IsPlayerSpell` / `IsSpellKnown`, which exist only under CVar `loadDeprecationFallbacks` | VERIFIED (F:Blizzard_DeprecatedSpellBook/Deprecated_SpellBook.lua:4-19, same file on L; simulated false without them) | Works while the CVar is 1; when Blizzard drops the fallback every spell is unavailable on both clients | `C_SpellBook.IsSpellKnown` / `IsSpellInSpellBook` in Compat, both clients |
| B6 | `GetNumSpecializationsForClassID` global does not exist on Forever | VERIFIED (F:Blizzard_DeprecatedSpecialization.toc `classic, standard`; absent from kit's forever globals) | Spec names render as "1491", no spec icons or order, name input does not resolve | `C_SpecializationInfo` member, or a static Forever class table |
| B7 | Sim party, enemy casts and story are Retail | VERIFIED (DB2 SpellName) | Counter Shot 147362, Rebuke 96231, Chaos Bolt 116858, Drain Life 234153 print as numbers with a default icon | Per-client sim seeds and label |
| B8 | Whether enemy casts are exposed and what `notInterruptible` reads on Forever | UNKNOWN (P1, P2) | The default visibility mode and every cast bar depend on it | Probe first in smoke; nothing in source says it is missing |

No finding makes the core absent on Forever, so the single-client exit (clients-2) does not apply.

## 1. What changed since the 2026-11-07 classification

`00_CLASSIFICATION.md:56` said: CooldownViewer and cooldowns exist, seeds keyed by Retail spec, "a Forever interrupt list
per class and spec, and a per-class check of the Cooldown Manager".
- Still true: the APIs and the spec keys. Warrior 1491 is confirmed on 71037.
- "per class and spec" is per class: one spec per class. VERIFIED DB2 ChrSpecialization; OutfitterReborn probe P1/P2 measured `GetNumSpecializations()=1`, Hunter 1485 (`docs/superpowers/specs/2026-11-08-forever-port-probes.md:11`).
- The Cooldown Manager check is answered, and the answer is to drop the gate (B3).
- Missing from it: ranks (B2), the deprecation-gated availability ladder (B5), the absent spec global (B6), the existing-profile trap (B4), the sim.

## 2. Keyed by spec, talent, spell id or Cooldown Manager category

### 2.1 Spec keys
Forever `ChrSpecialization` (VERIFIED, whole table): MAGE 1482, DRUID 1484, HUNTER 1485, PALADIN 1486, PRIEST 1487, ROGUE 1488,
SHAMAN 1489, WARLOCK 1490, WARRIOR 1491, plus pet 1493. Name = class name. No 1483, no DK/DH/Monk/Evoker
(DB2 ChrClasses; F:Blizzard_FrameXMLBase/Camelot/Constants.lua:1-12).

| Site | Reads | Forever behavior | Action |
|---|---|---|---|
| core/Constants.lua:198-225 `SPEC`, :236-239 `SPEC_TOKEN` | 39 Retail ids | 1491 displays as "1491" | Per-client table; token = class file token |
| defaults/Spells.lua:33-339 `DefaultSpells` | [class][Retail spec] | no row | `defaults/Spells_Forever.lua`, picked once |
| core/Util.lua `PlayerSpecID` | `GetSpecializationInfo(GetSpecialization())` | 1491 expected; documented default is **0**, which passes `type == "number"` (D:SpecializationInfoDocumentation.lua:254, `Default = 0`) | Treat <= 0 as nil; on Forever fall back to the class's seeded id so a nil early answer cannot empty the grid (P5) |
| core/Util.lua:273-290 `buildSpecNameMaps` | `GetNumSpecializationsForClassID` global | false, all maps empty | B6 |
| core/Util.lua:277, settings/Spells_Header.lua:91, core/Database.lua:459 | `for 1..GetNumClasses()` as class id | Class ids are 1,2,3,4,5,7,8,9,11. If the count is 9, Druid is never reached (INFERRED; P6) | `C_SpecializationInfo.GetAllClassIDs()` (Forever-only, D:SpecializationInfoDocumentation.lua:57; used F:Blizzard_Communities/ClubFinder.lua:80) or the static table |
| core/Util.lua `resolveByConstToken` | Retail token fallback | `ARMS` resolves to 71 (simulated). `add` refuses it through `specBelongs`; `reset`, `list`, `remove` do not validate (core/KickCD.lua:731-745), so `/kcd spells reset WARRIOR ARMS` creates an orphan list | Per-client `SPEC`; validate in `resolveClassSpec` |
| core/Database.lua:455-463 `IsKnownClass` | defaults, then client class list | accepts Retail classes through the defaults | follows the per-client seed; do not fall through to the client list on Forever |
| settings/Spells_Header.lua:101-125,166 | picker over DefaultSpells | 39 Retail rows; with Forever seeds "Warrior Warrior" | Forever label "Class", one name, class icon only |
| settings/Spells.lua:133-178 | order, player pair | 1491 not in defaults, so falls to first Retail spec | follows the seed |
| core/SpellInput.lua:68-101, :284 | live pair, membership | works with Forever seeds | none beyond the seed |
| modules/SimScenario.lua:57-63, SimDrivers.lua:335 | `specID` | Forever sample rows carry `tree`, no `specID` (LibKa0s Sim.lua:325-331); the driver already falls back to the English `spec` | per-client fallback copy |
| core/Database_Migrations.lua:138-186 `MigrateSpecKeys` | string keys from v2 | none on Forever | unchanged |
| `LibKa0s-Role-1.0` | not used | `Groups()` gives talent trees | not needed for a per-class list |

Talents: no talent id is stored. "Talent awareness" is only the known-spell filter plus `TRAIT_CONFIG_UPDATED`, which Forever's
talent frame also uses (Blizzard_PlayerSpells loads `Camelot/ClassTalents` over the shared traits frame). VERIFIED in source.

### 2.2 Retail seed ids on Forever
78 distinct ids (73 seeds + 5 racials) checked against SpellName 71037. Full output: `port/work/kc-code/seeds.txt`.
56 of the 78 are absent. Survivors, several with a different meaning:

| Id | Retail | Forever | Trap |
|---|---|---|---|
| 5211 | Mighty Bash | Bash Rank 1 | renamed, ranked |
| 99 | Incapacitating Roar | Demoralizing Roar Rank 1 | **not a cast-stopper** |
| 6789 | Mortal Coil | Death Coil Rank 1 | renamed, ranked |
| 19647 | Spell Lock | Spell Lock **Rank 2** (rank 1 is 19244) | pet bank |
| 23920 | Spell Reflection | named, on no skill line | not learnable |
| 2139, 15487, 20066, 19577, 1833, 2094, 5246 | same | same, single id | fine |
| 6552, 1766, 408, 853, 118, 605, 8122, 5782, 5484 | same | Rank 1 of a family | ranks |
| 20549 | War Stomp | War Stomp | the only surviving racial |

So filtering the Retail list would ship Demoralizing Roar as an incapacitate and drop Earth Shock and Shield Bash. clients-5 forbids it anyway.

### 2.3 Forever interrupts (candidates for the seed run, not rulings)
VERIFIED = in DB2. "Learnable" is INFERRED from SkillLineAbility; DB2 does not prove a trainer sells it.

| Class | Spell | Ids by rank | Cooldown / GCD | Notes |
|---|---|---|---|---|
| WARRIOR | Pummel | 6552, 6554 | 10 s / 1.5 | category 88 |
| WARRIOR | Shield Bash | 72, 1671, 1672 | 12 s / 1.5 | category 88, so shares its cooldown with Pummel |
| ROGUE | Kick | 1766, 1767, 1768, 1769 | 10 s / 1.0 | |
| MAGE | Counterspell | 2139 | 30 s / off GCD | |
| SHAMAN | Earth Shock | 8042, 8044, 8045, 8046, 10412, 10413, 10414 | 6 s / 1.5 | category 19, the shared shock cooldown |
| WARLOCK | Spell Lock | 19244, 19647 | 30 s | pet bank (Felhunter) |
| PRIEST | Silence | 15487 | 45 s / 1.5 | talent; no effect 68, so an effect-68 sweep misses it |
| PALADIN | Rebuke | 425609 | 15 s / 1.0 | AcquireMethod 3, in no trait and no Cooldown Manager set: obtainability UNKNOWN (P9) |
| DRUID | Skull Bash | 410176 | 10 s | same doubt (P9) |
| DRUID | Feral Charge | 1238122 | 15 s / off GCD | in TraitDefinition and the Druid set |
| HUNTER | none by effect 68 | | | CC leads the list, as for Retail Holy Paladin today |

Skill lines cannot supply rank families alone: `SupercedesSpell` chains Pummel, Kick, Shield Bash and Bash but is 0 for every
Earth Shock and Hammer of Justice rank. Build families from class skill line + name + `NameSubtext_lang`, then rule them.

### 2.4 Ranks: the design
VERIFIED: `IsPlayerSpell` maps to `C_SpellBook.IsSpellKnown` (D:SpellBookDocumentation.lua:738), and the spellbook knows low ranks
(`IsSpellBookItemLowRank`, D:SpellBookDocumentation.lua:651; CVar `ShowAllSpellRanks`, F:Blizzard_PlayerSpells/SpellBook/Blizzard_SpellBookFrame.lua:207,568,590).
UNKNOWN (P4): whether a superseded rank still reads known, and whether override / base lookups walk ranks.
`displaySpellID` ("highest known rank") exists only on `GroupBuffItem` (D:CooldownViewerDocumentation.lua), not on the cooldown info KickCD reads; it is no help here.

Design that holds whichever way P4 answers:
1. Seed one row per family, stored id = rank 1. A Forever `SpellRanks` table lists the ordered ranks.
2. `NS.ResolveSpell(storedID)` answers the highest rank the player knows, else nil; Retail's is identity + known.
3. Route every consumer through it: modules/Cooldowns.lua:103-117 (`isPollable`) and :344 (`Rebuild`), modules/IconGrid.lua:273-277,339-355 (render and dedupe on the resolved id),
   modules/Sim.lua:88-110 (`usable`, `ResolveSpells`), settings/Spells_Rows.lua:175,191,253-255 (tooltip, name, known mark), modules/Diagnostics.lua `entryText`.
4. `AddSpell` canonicalizes any rank to the family key, so a typed rank 2 does not create a second row.
5. Re-resolve on `SPELLS_CHANGED` (already registered). P10 covers trainer learn and pet summon.

### 2.5 Cooldown Manager (core/SpellInput.lua:148-300; settings/Spells.lua:337-427)
- VERIFIED: loads on Forever (`AllowLoadGameType: standard, camelot`, F:Blizzard_CooldownViewer.toc); same two functions and the same nine categories 0-8 (D:CooldownViewerConstantsDocumentation.lua:72).
- VERIFIED: DB2 CooldownSet has a populated set for each of the nine specs (47-72 rows). Of the interrupts above: Shield Bash 72, Pummel 6552, Kick 1766, Counterspell, Earth Shock 8042, Feral Charge and Silence are in; **every higher rank, both Spell Locks, Rebuke and Skull Bash are in no set** (`port/work/kc-code/cdm.txt`).
- The walk reads `info.spellID` only, not `overrideSpellID` or `linkedSpellIDs`. Whether those carry ranks at runtime is UNKNOWN (P11) and does not rescue pet spells.
- VERIFIED (simulated with a set holding 6552): `Admissible(6554)` is refused.
- The set answers "what Blizzard chose to display", not "what the player can track".

Recommendation: **absent on Forever** by `Compat.ForClient({"retail"})`: no gate, no "not tracked" tag (settings/Spells.lua:407-414),
no invalidator, no `cmcache` diagnostics section, and Forever strings that do not mention it. Validity is the name resolve plus the known mark.

## 3. Features

| Feature | Files | Recommendation | Evidence and work |
|---|---|---|---|
| Interrupt / CC cooldown tracking | modules/Cooldowns.lua | **Adapt** | APIs identical; `isActive` is NeverSecret on both (D:SpellSharedDocumentation.lua:19). Seeds, resolver, availability |
| Icon grid, layout, drag, handles | modules/IconGrid*.lua | **Port** | curves, duration objects and cooldown methods identical |
| Countdown, swipe, GCD suppression | IconGrid_Render/Ticker, `GCD_UPPER = 1.6` | **Port** | Forever GCD 1.0/1.5 and the shortest seeded cooldown 6 s, so the threshold holds (DB2 SpellCooldowns) |
| GCD attribution in the debug log | modules/Cooldowns.lua:76,445-450 | **Adapt** | 61304 has no Forever SpellName or SpellCooldowns row. The line would lose its "(gcd)" mark (P7). Log only |
| Charges badge, offsets | icons.showCharges, chargesOffsetX/Y | **Port** | no seeded interrupt has a ChargeCategory; API present, draws only for a spell that has charges (P8) |
| Ready glow | IconGrid_Render `UpdateGlow` | **Port; owner question Q2** | `ready = not isActive`. Every Forever kick except Counterspell and Feral Charge has StartRecoveryCategory 133, so a glow drops during each GCD. On Retail kicks are off the GCD, so it never did |
| Usability | `IsSpellUsable` | **Port** | stance, shield, energy and mana now matter: glow off, icon not dimmed. Existing semantics |
| Cast bar | modules/Castbar*.lua | **Port, probe** | same positions, duration getters and events. Pushback is routed (`DELAYED`, `CHANNEL_UPDATE`, Castbar.lua:124,127) |
| Interruptibility colors and masks | Castbar.lua:591-625, core/State.lua:119-139 | **Port, guard** | see section 3.1 |
| Focus unit, grid, bar, link | core/Units.lua | **Port** | `FocusFrame` (F:Blizzard_UnitFrame/Mainline/TargetFrame.xml:572, the family camelot loads), its spell bar (:601), `/focus` (F:Blizzard_ChatFrameBase/Shared/SlashCommands.lua:581-591), the binding (F:Blizzard_FrameXML/Bindings_Camelot.xml:1155), `PLAYER_FOCUS_CHANGED` (D:UnitDocumentation.lua:3790) |
| Empower routes | Castbar.lua:130-132, IconGrid.lua:98-100 | **Port as is** | events documented and identical; no emitter expected (no Evoker, INFERRED). Dead but harmless inside a shared feature |
| Visibility modes | always, in_combat, target_casting, interruptible (default) | **Port** | default depends on P1/P2 |
| Unit label | modules/UnitLabel.lua | **Port** | static "Target"/"Focus" text; no unit names, so two-word names do not reach it |
| Spell-list editor, `/kcd spells` | settings/Spells*.lua, core/KickCD.lua | **Adapt** | class picker, ranks, no gate, strings |
| Racial append | core/Database.lua:227-235 | **Adapt** | Forever table = Tauren 20549 only. Playable races add Skyborne (DB2 CharBaseInfo); its five racials name no obvious stopper (INFERRED from names; rule it in the seed run) |
| Sim | modules/Sim*.lua | **Adapt** | section 5 |
| Sound | none | **n/a** | VERIFIED: grep of core, modules, settings, defaults finds no PlaySound, sound row or media |
| Announce / chat | none | **n/a** | VERIFIED: no SendChatMessage or addon message |
| CVars | none read or written | **n/a** | VERIFIED grep. Indirect: `loadDeprecationFallbacks` (B5); the OR probe read 1 on Forever (`...port-probes.md:25`) |
| Launcher, profiles, perf, debug, skin | seams | **Port** | library-owned and client-neutral |
| Key bindings | no Bindings.xml | **n/a** | |

Only one feature is Retail-only (the Cooldown Manager gate) and none is Forever-only.

### 3.1 Cast information and secrets
VERIFIED identical on both clients:
- `UnitCastingInfo` / `UnitChannelInfo` `SecretWhenUnitSpellCastRestricted` (D:UnitDocumentation.lua:828,870): secret for any unit other than the player or pet (D:SecretPredicatesDocumentation.lua:115-117). KickCD's target and focus reads are secret on both; its pass-through design is required and sufficient by documentation.
- `UnitCastingDuration` is `SecretReturns = true` on both (D:UnitDocumentation.lua:811); `UnitChannelDuration` is not.
- `GetSpellCooldown` / `GetSpellCharges` `SecretWhenCooldownsRestricted` (combat, encounter, challenge, PvP; per-spell flags win; SecretPredicatesDocumentation.lua:90-92).
- The sinks accept secrets from tainted code: `SetAlphaFromBoolean` (SimpleFrameAPIDocumentation.lua:1145), `StatusBar:SetValue` (SimpleStatusBarAPIDocumentation.lua:355), `FontString:SetFormattedText` (SimpleFontStringAPIDocumentation.lua:539), `EvaluateColorValueFromBoolean` (CurveUtilDocumentation.lua:49).

Risks:
- `notInterruptible` is `Nilable = true` while both sinks take `bool, Nilable = false`. Retail evidently never hands nil for a live cast (INFERRED from the shipped addon). On Forever UNKNOWN (P2). Cheap guard in `buildCastRecord` and `ApplyInterruptibleAlpha`: a non-secret nil becomes false, the secret test first.
- `Enum.GameRule.TargetCastBarDisabled` is read by F:Blizzard_SharedXML/GameRulesUtil.lua:50-51 and can hide Blizzard's target bar. Whether Camelot activates it, and whether it also limits the API, is UNKNOWN (P1). Retail carries the identical line (L:Blizzard_SharedXML/GameRulesUtil.lua:51), so its presence is not evidence that Forever sets the rule.
- Vanilla NPC casts are mostly interruptible and many bosses immune; the flag's fidelity on Forever is UNKNOWN (P2).
- `modules/Castbar_Debug.lua:70-71` concatenates `UnitName` and branches on `UnitIsUnit`, both conditionally secret; on Forever it also prints only the first name. Use `UnitCharacterName` + `SafeToString` and test `IsSecret` first. Same for core/Compat.lua:531 (name only). These are the only name reads.

## 4. Client surface: what each needs

The full file:line list for every name is Appendix A.

| Group | Names | Forever | Need |
|---|---|---|---|
| Spell | `C_Spell.GetSpellCooldown / CooldownDuration / Charges / Info / Texture / IsSpellUsable` | VERIFIED identical (D:SpellDocumentation.lua:309,327,291,416,595,980) | none. `IsSpellUsable`'s table branch is unneeded |
| Spellbook | `IsPlayerSpell`, `IsSpellKnown(id[,true])` | VERIFIED fallback-only, both clients | B5: Player `IsSpellKnown`, then `IsSpellInSpellBook(id, Player, false)`, then `(id, Pet, false)` (D:SpellBookDocumentation.lua:720,738) |
| Spec | `C_SpecializationInfo.GetSpecialization / Info` | VERIFIED identical (:237,:254) | reject id 0 |
| Spec by class | `GetSpecializationInfoForClassID` | VERIFIED global present (kit forever globals; F:Blizzard_CharacterCreate/Camelot/Blizzard_CharacterCreate.lua:3132). The `C_` form does not exist on either | keep the global, through Compat |
| Spec count | `GetNumSpecializationsForClassID` global | VERIFIED absent | `C_SpecializationInfo` member (:137) |
| Classes | `GetNumClasses`, `GetClassInfo` | VERIFIED present; iteration semantics UNKNOWN | P6 or static table |
| Unit | Exists, CanAttack, IsDead, CastingInfo, ChannelInfo, CastingDuration, ChannelDuration, Class, Race, Name, IsUnit | VERIFIED identical docs | section 3.1; `UnitName`'s second return is the surname (not read) |
| Duration | `C_DurationUtil.CreateDuration`, `SetTimeFromStart`, getters, `Evaluate*` | VERIFIED identical (DurationUtilDocumentation.lua:11; LuaDurationObjectAPIDocumentation.lua) | none |
| Curves | `CreateCurve`, `CreateColorCurve`, `EvaluateColorValueFromBoolean`, `Enum.LuaCurveType` | VERIFIED identical | none |
| Cooldown viewer | two functions, category enum | VERIFIED identical | absent on Forever (2.5) |
| Events | cooldown x3, SPELLS_CHANGED, TRAIT_CONFIG_UPDATED, spec changed, PEW, login, target, focus, regen x2, roster, 13 UNIT_SPELLCAST | VERIFIED all documented and identical | none. `SafeRegisterEvent` records a refusal, see `/kcd debug events` |
| Timers, lockdown, group, instance | `C_Timer.*`, `InCombatLockdown`, `IsInGroup`, `IsInInstance` | documented or in the kit's forever globals | none |
| Frames | CooldownFrameTemplate, BackdropTemplate, number/normal fonts, GameTooltip, StaticPopup, Settings, UISpecialFrames | modern engine; the only Cooldown doc diff is a nilable texture arg | none |
| Markup | `CreateAtlasMarkup`, `classicon-<class>`, `RAID_CLASS_COLORS`, class names | VERIFIED present (F:Blizzard_SharedXML/SharedConstants.lua:44-45) | none |
| LibCustomGlow | `isRetail` is false on Forever (libs/LibCustomGlow-1.0/LibCustomGlow-1.0.lua:15,23,150) | classic shine texture + ADD blend for autocast; proc atlases referenced by F:Blizzard_ActionBar/Shared/ActionButtonSpellAlerts.xml:13 | smoke all four styles; no patch to vendored code |
| Client detection | none in shipped code (VERIFIED grep) | | route `IsForever / IsRetail / ClientKey / ForClient` (and `UnitCharacterName`) from LibKa0s-Compat; `core/CompatClient.lua` as in DropWatcher |

`core/SimSetup.lua` wraps every Compat member at load: a new compat file must load before it, and new pure members go in its `PURE` list (tests/test_sim_seam.lua enforces it).

## 5. Retail-shaped settings, presets, test mode, sim, samples

Test mode is unlock (client-neutral; preview text "KickCD castbar" and a question-mark icon). There are no presets.

| Item | Where | Retail shape | Forever |
|---|---|---|---|
| Spec picker | settings/Spells_Header.lua:166 | "Class and specialization", class + spec | "Class" |
| Strings | locales/enUS.lua:87,509,526,552,841; core/SpellInput.lua:297; slash help `[CLASS SPEC]` (core/KickCD.lua:924-942) | spec wording | class wording; Forever accepts `[CLASS]` |
| Scenario `pull` | SimScenario.lua:149-167, :232; locales:233 | "Mythic+ pull" | "Dungeon pull"; keep the key `pull` |
| Scenario `boss` | SimScenario.lua:170-190 | "your kick gets two charges", plays charge events | drop the Setup/Expire charge steps and use the kick's cooldown, or omit the scenario on Forever. Recommend adapt |
| Party kicks | SimScenario.lua:51-56 | Counter Shot, Rebuke, Counterspell, Pummel | per-client table. Hunters have none, so the timeline naming `samplehunter` (:160) must change with it: `memberName` raises on a member absent from the party. Use Mockflame 2139, Mockshield 72 (a shield tank), Samplemender Silence only with a Shadow story; Sampleblade only if P9 confirms Rebuke |
| Sample names | `buildParty` uses `row.name` | first name | `row.fullName` on Forever ("Mockflame Samplewick"); keep the key as the first name |
| Enemy casts | SimScenario.lua:88-92 | 116858, 234153 absent | 686, 15407, 5782 exist; pick a vanilla boss cast and Drain Life rank from DB2 |
| Kick off GCD | modules/Sim.lua:235 `MarkOffGcd(Host.kick)` | always | only if the spell really is off the GCD (Counterspell, Feral Charge) |
| `D.KICK_CD = 15`, `CC_CD = 30`, `RECHARGE = 15` | SimDrivers.lua | story times | fine; optionally 10 s on Forever |
| Fallback copy | SimScenario.lua:57-63 | Retail rows | per-client copy (the one non-skin suite failure) |
| Visibility, glow, cast bar, icon rows | settings/General, Icons, Castbar | none Retail-only | keep |
| Seed tool | tools/seeds/seeds.py, rulings_retail.json, docs/validate-seeds.md:22-24,167 | product `wow` only, spec reach model | `forever` flavor: product `wowf`, class reach, ranks, pet skill lines, rulings_forever.json, frozen bundle |

## 6. SavedVariables

Globals `KickCDDB` (AceDB, shared "Default" profile) and `KickCDPerfDB`.

| Shape | Client split touches it? | Action |
|---|---|---|
| `profile.spells[CLASS][specID] = { {spellID, category, enabled}, ... }` | yes | same shape: Forever spec ids, family key as spellID. Retail untouched, no schema bump for the shape |
| seeded-once rule (core/Database.lua:267-305) | yes | Forever only: for each seeded class, seed the pair when its **key** is absent. A list the player emptied keeps its key, so intent survives and no marker is needed. Leave stray Retail pairs in place (hidden, harmless); do not delete |
| racial appended at first creation to the creator's class | existing limit | a shared profile's later Tauren alt gets no War Stomp. Both clients; out of scope |
| `CountCustomizedSpellLists` | yes | stray Retail pairs would count as customized on Forever; count only the running client's pairs |
| `profile.skin.skin` default | yes | already per client (section 7). AceDB strips default-equal values, so nothing is stored |
| `skin.*Reset`, `fontPicksKept`, `global.schemaVersion` (10) | no | migrations run clean on a fresh Forever profile (simulated) |
| `units.*`, anchors, `sim.stepDelay`, minimap | no | |
| character/realm keys | no | KickCD stores none; AceDB 40 keys profiles itself |
| `KickCDPerfDB` | no | per install |

INFERRED: WTF is per client install, so the two clients never share a DB unless a player copies the file. The backfill covers that case too.

## 7. Default skin

Already correct (skinning-2):
- core/SkinSetup.lua:127 reads `Skin:DefaultSkin()` once; defaults/Profile.lua:386 names it; core/SkinSetup.lua:274 and core/Database_Migrations.lua:491 fall back to it.
- The only `"ka0s"` literals are the library-absent fallback and the skin *source* (VERIFIED grep).
- VERIFIED by run: the Forever profile gives `NS.DEFAULT_SKIN == "forever"`.
- `MigrateSkinFontPicks` treats "Ka0s Prototype" as a pick under the Forever skin and turns "Use the skin's font" off; `MigrateFullSkin`, which runs last, turns it back on. VERIFIED by simulated Init and ResetProfile: all three follow the skin afterwards. No product bug, but the order is load-bearing on Forever, so add a fresh-profile and reset test.
- The Forever skin scales HUD text (22 -> 21.08, 14 -> 13.42); expected.

## 8. Suite and lint

Commands ran through ka0s-bounded in `port/work/kc-code/` copies.

| Run | Result |
|---|---|
| retail | 1736 passed, 0 failed, 3 skipped |
| `KA0S_KIT_CLIENT=forever` | **1717 passed, 19 failed, 3 skipped** |
| TOC `120105, 16001` (arms the Forever globals scan), retail / forever | 1736/0/3 and 1717/19/3; globals scan passes |
| forever, with the library's default skin pinned to ka0s in the copy | **1735 / 1 / 3** |
| luacheck | 0 warnings, 0 errors, 160 files |

The pin proves 18 failures are the default skin alone. None is a product bug.

| # | Failing case | Message | Cause | Fix |
|---|---|---|---|---|
| 1 | SimScenario: without LibKa0s the party is a copy of the library's rows | `samplehunter.specID (expected nil, got 253)` | `SAMPLE_COPY` is Retail's while `Sim.Sample()` answers Forever's | per-client copy (product fallback) |
| 2 | Apply pushes the configured size and color onto the FontString | 22 vs 21.083 | Forever HUD font scale | pin the skin in the test |
| 3 | Apply falls back to a 14pt outline for a style with no size or flags | 14 vs 13.417 | same | same |
| 4 | a LINKED focus renders target's styling but its own text | 27 vs 25.875 | same | same |
| 5 | both labels share the config font, and NONE flags normalize to empty | 16 vs 15.333 | same | same |
| 6 | Skin seam: the read answers Ka0s Default before the profile store exists | ka0s vs forever | test types Retail's default | assert `Skin:DefaultSkin()` |
| 7 | Skin seam: the eight skin keys default to Ka0s Default, ... | ka0s vs forever | same | same |
| 8 | Skin seam: a profile reset takes the skin back to Ka0s Default | ka0s vs forever | same | same |
| 9 | the profile default and the pre-store fallback name the library's DefaultSkin, never a literal | ka0s vs forever | the test itself compares to the literal | same |
| 10 | HUD skin: the cast bar draws the skin's face, texture and border while following | hud.font on Ka0s Default | baseline assumes ka0s | pin |
| 11 | HUD skin: a companion turned off draws the player's stored pick again | still follows | same | pin |
| 12 | HUD skin: the countdown follows hud.font and the charges badge takes the skin's face | hud.font | same | pin |
| 13 | HUD skin: the unit label follows hud.font, and a false companion is the player's face | assertTrue | same | pin |
| 14 | HUD skin: the reset puts every companion on the skin once, keeps the picks, ... | expected true, got false | worn face differs, so the isolated font-pick step reads the stored default as a pick | pin; add the full-order Forever case (section 7) |
| 15 | skin font kept: a picked face other than the skin's turns Use the skin's font off, once | Ka0s Default's own face | same | pin |
| 16 | skin flip: Ka0s Default keeps this addon's pixels, with no shadow | bg 0,0,0,.5 vs parchment dark | baseline skin | pin |
| 17 | skin flip: each slot's glow reaches the driver in the skin's color | yellow vs bronze | same | pin |
| 18 | skin flip: the charges badge draws the skin's HUD shadow | no shadow vs 1,-1,1 | same | pin |
| 19 | layout guard: every stored path, type, default and range ... | row 12 `skin.skin` ka0s vs forever | snapshot of Retail's default | substitute `DefaultSkin()` for that row |

Why 1717 green proves little. The kit profile changes project constants, build and five globals. `tests/wow_mock.lua` still gives
a Retail Hunter, Retail spec ids, 13 classes, `IsPlayerSpell`/`IsSpellKnown` always true (:708-709) and no CooldownViewer (:734). B1-B6 all pass
unnoticed, and the globals scan cannot see guarded `_G.X` reads of fallback globals. The port needs a Forever world in the host mock:
nine classes at their real ids, spec = class, ranked known sets, `C_SpellBook`, no `GetNumSpecializationsForClassID` global, no 61304.

## 9. File sizes (cap 1500)

None is over, none is within 400 lines of it. Every file at 800 or more:

| Lines | File | Port pressure |
|---|---|---|
| 1092 | modules/IconGrid_Render.lua | on notice; little change |
| 1057 | tests/test_schema.lua | none |
| 1047 | core/KickCD.lua | on notice; keep the per-client arg parsing out of it |
| 1023 | modules/IconGrid.lua | on notice; resolver in its own file |
| 976 | modules/Castbar.lua | crosses 1000 with +25 |
| 969 | settings/Spells.lua | crosses 1000 with +32 |
| 947 | tests/test_settings_spells_editor.lua | put Forever cases in a new suite |
| 905, 882, 872 | tests/test_skin_flip, test_perfsetup, test_slash | none |
| 892 | locales/enUS.lua | about +15 |
| 859, 859 | tests/test_castbar_frame, tests/wow_mock.lua | put the Forever world in `tests/wow_mock_forever.lua` |
| 832 | core/Database.lua | backfill fits |
| 800 | modules/Cooldowns.lua | fine |

New files: `core/CompatClient.lua`, `core/SpellRanks.lua`, `defaults/Spells_Forever.lua`. Kit and libs are vendored, not counted.

## 10. Work items, in order

1. Compat client routing; TOC `120105, 16001`; both-profile gate.
2. Both clients, one commit each with a test (LH/BL ruling R8 shape): `C_SpellBook` availability; spec count through `C_SpecializationInfo`; spec id 0 = none; nil `notInterruptible` guard; secret-safe debug header.
3. Forever mock world, then characterization cases for B1-B6.
4. Seed run (`tools/seeds` forever flavor), rulings, `defaults/Spells_Forever.lua`, per-client `SPEC` and racials.
5. Rank resolver and canonical add.
6. Backfill for existing Forever profiles.
7. Cooldown Manager gate Retail-only; present/absent tests.
8. Spells page and slash wording per client.
9. Sim per client.
10. Test pins for the 18 skin cases.
11. Docs: README badge and sentence, CLAUDE.md gate, DEPENDENCIES.md:16,33, docs/ARCHITECTURE.md:3,149,467,501 + per-client table, testing.md, validate-seeds.md, scope.md, smoke-tests.md Forever section, new forever-quirks.md, test-cases regenerated; roster row in the same change.

## 11. Decisions the lead can take

- One list per class (the client's only spec identity); the known filter hides untalented spells. (See Q1.)
- One row per rank family, showing the highest known rank.
- Cooldown Manager gate absent on Forever.
- Hard CC scope same as Retail; Hunter's first row is a CC.
- Rebuke and Skull Bash stay out of the seed until P9 confirms them.
- No Retail behavior change except the items in step 2.

Owner questions:
- **Q1.** One spell list per class, or one per talent tree (27)? Recommend per class.
- **Q2.** On Forever most kicks are on the GCD, so "glow when ready" blinks off after every ability. Keep it literal, or hold the glow through a GCD-only lockout? Recommend keep literal for the port and revisit after smoke.

## 12. Probes (UNKNOWN), in game on 1.60.1

| P | Settles | Probe |
|---|---|---|
| P1 | enemy casts exposed | `/dump C_GameRules.IsGameRuleActive(Enum.GameRule.TargetCastBarDisabled), GetCVar("showTargetCastbar")`; target a casting NPC: `/kcd debug interrupt target`; same on focus and on an enemy player |
| P2 | flag value | during an interruptible and an immune NPC cast: `/dump issecretvalue(select(8,UnitCastingInfo("target"))), type((select(8,UnitCastingInfo("target"))))`; `/kcd debug castbar` after the TOC flip |
| P3 | cooldown secrecy in combat | in combat: `/dump C_Secrets.ShouldSpellCooldownBeSecret(6552), C_Spell.GetSpellCooldown(6552).isActive, C_Spell.GetSpellCooldownDuration(6552) ~= nil` |
| P4 | ranks | Warrior with Pummel rank 2: `/dump C_SpellBook.IsSpellKnown(6552), C_SpellBook.IsSpellKnown(6554), C_SpellBook.IsSpellInSpellBook(6552,0,false), C_SpellBook.FindBaseSpellByID(6554), C_SpellBook.FindSpellOverrideByID(6552), C_Spell.GetSpellInfo("Pummel").spellID` |
| P5 | spec before talents | level 1 and level 10: `/dump C_SpecializationInfo.GetSpecialization(), C_SpecializationInfo.GetSpecializationInfo(1)` |
| P6 | class iteration | `/dump GetNumClasses(), {GetClassInfo(6)}, {GetClassInfo(9)}, {GetClassInfo(11)}, C_SpecializationInfo.GetAllClassIDs()` |
| P7 | GCD id | cast an instant, then at once `/dump C_Spell.GetSpellCooldown(61304)` |
| P8 | charges absent | `/dump C_Spell.GetSpellCharges(6552)`: expect nil |
| P9 | obtainable | Paladin and Druid at the trainer / in the spellbook: `/dump C_SpellBook.IsSpellKnown(425609)` and `(410176)`; talent tree for Feral Charge 1238122 |
| P10 | refresh events | `/etrace`, learn a rank, summon a Felhunter: `SPELLS_CHANGED`? then `/dump C_SpellBook.IsSpellInSpellBook(19244,1,false)` |
| P11 | viewer runtime | `/run for _,i in ipairs(C_CooldownViewer.GetCooldownViewerCategorySet(1)) do local x=C_CooldownViewer.GetCooldownViewerCooldownInfo(i) if x then print(x.spellID,x.overrideSpellID,table.concat(x.linkedSpellIDs or {},",")) end end` |
| P12 | deprecation CVar | `/dump GetCVar("loadDeprecationFallbacks"), IsPlayerSpell ~= nil, GetNumSpecializationsForClassID` |
| P13 | glow art | all four glow styles on Forever |

## Appendix A. Inventory: every client name with file:line

Extracted from code lines (comments stripped) by luacheck's undefined-global report plus a scan for `_G.`, `C_*`, `Enum`, events, widget methods and templates.
Library internals (libs/) are out of scope. "same" = documented identically on both clients or present in both kit globals lists.

| Name | Forever need | file:line |
|---|---|---|
| `C_CurveUtil` (G) | same | modules/Castbar.lua:599, modules/Castbar.lua:601, modules/Castbar.lua:608, modules/Castbar.lua:610, modules/Castbar.lua:616, modules/Castbar.lua:618, modules/Castbar.lua:621, modules/Castbar.lua:622, modules/Castbar.lua:623, modules/Castbar.lua:624, modules/Castbar_Debug.lua:55, modules/IconGrid_Render.lua:189, modules/IconGrid_Render.lua:229, modules/IconGrid_Render.lua:238, modules/IconGrid_Render.lua:239, modules/IconGrid_Render.lua:260 |
| `C_DurationUtil` (G) | same | core/Compat.lua:323 |
| `C_Spell` (G) | same | core/Compat.lua:150, core/Compat.lua:151, core/Compat.lua:177, core/Compat.lua:178, core/Compat.lua:222, core/Compat.lua:223 |
| `C_Timer` (G) | same | core/SkinSetup.lua:508, core/SkinSetup.lua:510, core/Util.lua:156, modules/IconGrid_Ticker.lua:214, modules/IconGrid_Ticker.lua:215, settings/OptionsSetup.lua:120, settings/SchemaSetup.lua:104 |
| `GameFontNormal` (G) | same | modules/Castbar.lua:372 |
| `GetClassInfo` (G) | P6 | core/Database.lua:458, core/Database.lua:460 |
| `GetNumClasses` (G) | P6 | core/Database.lua:458, core/Database.lua:459 |
| `GetSpellCharges` (G) | legacy arm, unreachable; P8 | core/Compat.lua:185, core/Compat.lua:186 |
| `GetTime` (G) | same | modules/SimDrivers.lua:51, modules/SimWorld.lua:39 |
| `InCombatLockdown` (G) | same | core/KickCD.lua:978, core/SkinSetup.lua:436, core/State.lua:176, core/State.lua:243, modules/Sim.lua:139 |
| `IsInGroup` (G) | same | modules/Sim.lua:149, modules/Sim.lua:205 |
| `IsInInstance` (G) | same | modules/Sim.lua:144 |
| `IsLoggedIn` (G) | same | modules/Cooldowns.lua:655 |
| `IsPlayerSpell` (G) | B5 replace | core/Compat.lua:210 |
| `IsSpellKnown` (G) | B5 replace | core/Compat.lua:211, core/Compat.lua:212, core/Compat.lua:213 |
| `IsUsableSpell` (G) | legacy arm, unreachable | core/Compat.lua:231, core/Compat.lua:232 |
| `NumberFontNormal` (G) | same | modules/IconGrid_Render.lua:974 |
| `STANDARD_TEXT_FONT` (G) | same | core/Constants.lua:177, core/SkinSetup.lua:594, core/SkinSetup.lua:624, modules/UnitLabel.lua:97 |
| `UISpecialFrames` (G) | same | modules/Sim.lua:343, modules/Sim.lua:362 |
| `UnitCanAttack` (G) | same | core/Compat.lua:284, core/Compat.lua:285, core/Compat.lua:532, modules/Castbar_Debug.lua:69 |
| `UnitCastingDuration` (G) | P1 | core/Compat.lua:308, core/Compat.lua:309 |
| `UnitCastingInfo` (G) | P1, P2 | core/Compat.lua:296, core/Compat.lua:297, core/Compat.lua:536, core/Compat.lua:538 |
| `UnitChannelDuration` (G) | P1 | core/Compat.lua:314, core/Compat.lua:315 |
| `UnitChannelInfo` (G) | P1, P2 | core/Compat.lua:302, core/Compat.lua:303, core/Compat.lua:541, core/Compat.lua:543 |
| `UnitClass` (G) | same; 9 classes | core/KickCD.lua:724, core/KickCD.lua:725, core/SpellInput.lua:60, core/SpellInput.lua:61, settings/Spells.lua:166, settings/Spells.lua:167, settings/Spells.lua:323, settings/Spells.lua:324, settings/Spells.lua:554 |
| `UnitExists` (G) | same | core/Compat.lua:276, core/Compat.lua:277, core/Compat.lua:526, core/KickCD.lua:460, modules/Castbar_Debug.lua:65 |
| `UnitIsDead` (G) | same | core/Compat.lua:290, core/Compat.lua:291 |
| `UnitName` (G) | surname / secret-safe | core/Compat.lua:531, modules/Castbar_Debug.lua:70 |
| `issecretvalue` (G) | same | core/Compat.lua:47 |
| `C_AddOns.GetAddOnMetadata` (api) | same | core/EnvSetup.lua:75, core/EnvSetup.lua:76 |
| `C_CooldownViewer.GetCooldownViewerCategorySet` (api) | Retail-only (2.5) | core/SpellInput.lua:166 |
| `C_CooldownViewer.GetCooldownViewerCooldownInfo` (api) | Retail-only (2.5) | core/SpellInput.lua:167 |
| `C_CurveUtil.CreateColorCurve` (api) | same | modules/IconGrid_Render.lua:238, modules/IconGrid_Render.lua:239 |
| `C_CurveUtil.CreateCurve` (api) | same | modules/IconGrid_Render.lua:189, modules/IconGrid_Render.lua:229, modules/IconGrid_Render.lua:260 |
| `C_CurveUtil.EvaluateColorValueFromBoolean` (api) | same; nil guard (3.1) | modules/Castbar.lua:599, modules/Castbar.lua:601, modules/Castbar.lua:608, modules/Castbar.lua:610, modules/Castbar.lua:616, modules/Castbar.lua:618, modules/Castbar.lua:621, modules/Castbar.lua:622, modules/Castbar.lua:623, modules/Castbar.lua:624, modules/Castbar_Debug.lua:55, modules/Castbar_Debug.lua:56, modules/Castbar_Debug.lua:57 |
| `C_Spell.GetSpellCharges` (api) | same | core/Compat.lua:177, core/Compat.lua:178 |
| `C_Spell.GetSpellCooldownDuration` (api) | same | core/Compat.lua:150, core/Compat.lua:151 |
| `C_Spell.IsSpellUsable` (api) | same | core/Compat.lua:222, core/Compat.lua:223 |
| `C_Timer.After` (api) | same | core/SkinSetup.lua:508, core/SkinSetup.lua:510, settings/SchemaSetup.lua:104 |
| `C_Timer.NewTicker` (api) | same | modules/IconGrid_Ticker.lua:214, modules/IconGrid_Ticker.lua:215 |
| `C_Timer.NewTimer` (api) | same | settings/OptionsSetup.lua:120 |
| `Enum.CooldownViewerCategory` (api) | Retail-only (2.5) | core/SpellInput.lua:168, core/SpellInput.lua:242 |
| `Enum.LuaCurveType` (api) | same | modules/IconGrid_Render.lua:190, modules/IconGrid_Render.lua:230, modules/IconGrid_Render.lua:240 |
| `Enum.LuaCurveType.Linear` (api) | same | modules/IconGrid_Render.lua:191, modules/IconGrid_Render.lua:231, modules/IconGrid_Render.lua:241 |
| `GROUP_ROSTER_UPDATE` (event) | same | modules/SimDrivers.lua:403, modules/SimDrivers.lua:409 |
| `PLAYER_ENTERING_WORLD` (event) | same | modules/Castbar.lua:854, modules/Cooldowns.lua:600, modules/IconGrid.lua:752, modules/UnitLabel.lua:278 |
| `PLAYER_FOCUS_CHANGED` (event) | same | modules/Castbar.lua:859, modules/IconGrid.lua:764, modules/Sim.lua:482, modules/SimDrivers.lua:41, modules/SimDrivers.lua:218, modules/SimDrivers.lua:388 |
| `PLAYER_LOGIN` (event) | same | core/State.lua:175, core/State.lua:179, core/State.lua:195 |
| `PLAYER_REGEN_DISABLED` (event) | same | core/State.lua:169, core/State.lua:196, core/State.lua:200, modules/SimDrivers.lua:185, modules/SimDrivers.lua:191 |
| `PLAYER_REGEN_ENABLED` (event) | same | core/SkinSetup.lua:471, core/State.lua:172, core/State.lua:197, core/State.lua:201, modules/Sim.lua:494, modules/SimDrivers.lua:185, modules/SimDrivers.lua:191 |
| `PLAYER_SPECIALIZATION_CHANGED` (event) | same | core/SpellInput.lua:324, modules/Cooldowns.lua:601, modules/IconGrid.lua:751, settings/Spells.lua:835 |
| `PLAYER_TARGET_CHANGED` (event) | same | modules/Castbar.lua:858, modules/IconGrid.lua:763, modules/Sim.lua:482, modules/SimDrivers.lua:41, modules/SimDrivers.lua:215, modules/SimDrivers.lua:387 |
| `SPELLS_CHANGED` (event) | same | modules/Cooldowns.lua:607, modules/IconGrid.lua:757, settings/Spells.lua:833 |
| `SPELL_UPDATE_CHARGES` (event) | same | modules/Cooldowns.lua:599, modules/Sim.lua:483, modules/SimDrivers.lua:204, modules/SimDrivers.lua:211, modules/SimDrivers.lua:294, modules/SimDrivers.lua:319, modules/SimDrivers.lua:413, modules/SimDrivers.lua:421, modules/SimWorld.lua:212 |
| `SPELL_UPDATE_COOLDOWN` (event) | same | modules/Cooldowns.lua:597, modules/Sim.lua:482, modules/SimDrivers.lua:293, modules/SimDrivers.lua:319, modules/SimDrivers.lua:365, modules/SimDrivers.lua:380, modules/SimDrivers.lua:413, modules/SimDrivers.lua:422, modules/SimWorld.lua:158, modules/SimWorld.lua:184, modules/SimWorld.lua:213 |
| `SPELL_UPDATE_USABLE` (event) | same | modules/Cooldowns.lua:598 |
| `TRAIT_CONFIG_UPDATED` (event) | same | core/SpellInput.lua:323, modules/Cooldowns.lua:608, modules/IconGrid.lua:758, settings/Spells.lua:834 |
| `UNIT_SPELLCAST_` (event) | prefix, not an event | core/Events.lua:46, core/Util.lua:450 |
| `UNIT_SPELLCAST_CHANNEL_START` (event) | same | modules/Castbar.lua:125, modules/IconGrid.lua:94, modules/SimDrivers.lua:256, modules/SimDrivers.lua:258 |
| `UNIT_SPELLCAST_CHANNEL_STOP` (event) | same | modules/Castbar.lua:126, modules/IconGrid.lua:95, modules/SimDrivers.lua:142, modules/SimDrivers.lua:296, modules/SimDrivers.lua:320, modules/SimDrivers.lua:339, modules/SimDrivers.lua:350, modules/SimDrivers.lua:354, modules/SimDrivers.lua:387 |
| `UNIT_SPELLCAST_CHANNEL_UPDATE` (event) | same | modules/Castbar.lua:127 |
| `UNIT_SPELLCAST_DELAYED` (event) | same | modules/Castbar.lua:124 |
| `UNIT_SPELLCAST_EMPOWER_START` (event) | same; no emitter expected | modules/Castbar.lua:130, modules/IconGrid.lua:98 |
| `UNIT_SPELLCAST_EMPOWER_STOP` (event) | same; no emitter expected | modules/Castbar.lua:132, modules/IconGrid.lua:100 |
| `UNIT_SPELLCAST_EMPOWER_UPDATE` (event) | same; no emitter expected | modules/Castbar.lua:131, modules/IconGrid.lua:99 |
| `UNIT_SPELLCAST_FAILED` (event) | same | modules/Castbar.lua:122, modules/IconGrid.lua:92 |
| `UNIT_SPELLCAST_INTERRUPTED` (event) | same | modules/Castbar.lua:123, modules/IconGrid.lua:93, modules/SimDrivers.lua:296, modules/SimDrivers.lua:320, modules/SimDrivers.lua:339, modules/SimDrivers.lua:350 |
| `UNIT_SPELLCAST_INTERRUPTIBLE` (event) | same | modules/Castbar.lua:128, modules/IconGrid.lua:96, modules/SimDrivers.lua:261, modules/SimDrivers.lua:268 |
| `UNIT_SPELLCAST_NOT_INTERRUPTIBLE` (event) | same | modules/Castbar.lua:129, modules/Castbar_Events.lua:122, modules/IconGrid.lua:97, modules/SimDrivers.lua:261, modules/SimDrivers.lua:268 |
| `UNIT_SPELLCAST_START` (event) | same | modules/Castbar.lua:120, modules/IconGrid.lua:90, modules/SimDrivers.lua:253, modules/SimDrivers.lua:254 |
| `UNIT_SPELLCAST_STOP` (event) | same | modules/Castbar.lua:121, modules/IconGrid.lua:91, modules/SimDrivers.lua:142, modules/SimDrivers.lua:354, modules/SimDrivers.lua:387 |
| `UNIT_SPELLCAST_SUCCEEDED` (event) | same | modules/SimDrivers.lua:232, modules/SimDrivers.lua:292, modules/SimDrivers.lua:319, modules/SimDrivers.lua:354, modules/SimDrivers.lua:360, modules/SimDrivers.lua:365, modules/SimDrivers.lua:379 |
| `BackdropTemplate` (frame) | same (modern UI) | modules/Castbar_Frame.lua:318, modules/Castbar_Frame.lua:319, modules/IconGrid_Render.lua:319 |
| `CooldownFrameTemplate` (frame) | same (modern UI) | modules/IconGrid_Render.lua:328 |
| `GameFontNormal` (frame) | same (modern UI) | modules/Castbar.lua:372, modules/UnitLabel.lua:167, settings/Spells.lua:538 |
| `NumberFontNormal` (frame) | same (modern UI) | modules/IconGrid_Render.lua:372, modules/IconGrid_Render.lua:381, modules/IconGrid_Render.lua:974 |
| `SettingsPanel` (frame) | same (modern UI) | settings/Spells.lua:797 |
| `StaticPopupDialogs` (frame) | same (modern UI) | settings/General.lua:369, settings/Spells.lua:429 |
| `UISpecialFrames` (frame) | same (modern UI) | modules/Sim.lua:343, modules/Sim.lua:362 |
| `C_AddOns` (global) | same | core/EnvSetup.lua:75, core/EnvSetup.lua:76 |
| `C_CooldownViewer` (global) | Retail-only | core/SpellInput.lua:165, core/SpellInput.lua:166, core/SpellInput.lua:167 |
| `CreateAtlasMarkup` (global) | same | settings/Spells_Header.lua:72, settings/Spells_Header.lua:74 |
| `CreateColor` (global) | same | modules/IconGrid_Render.lua:238, modules/IconGrid_Render.lua:243, modules/IconGrid_Render.lua:244, modules/IconGrid_Render.lua:245, modules/IconGrid_Render.lua:246 |
| `CreateFrame` (global) | same (engine / library) | core/Util.lua:465, modules/Castbar_Frame.lua:224, modules/Castbar_Frame.lua:258, modules/Castbar_Frame.lua:261, modules/Castbar_Frame.lua:262, modules/Castbar_Frame.lua:278, modules/Castbar_Frame.lua:318, modules/Castbar_Frame.lua:319, modules/IconGrid.lua:568, modules/IconGrid_Render.lua:302, modules/IconGrid_Render.lua:319, modules/IconGrid_Render.lua:328, modules/IconGrid_Render.lua:366, modules/IconGrid_Render.lua:392, modules/UnitLabel.lua:165, settings/Spells_Rows.lua:147 |
| `DEFAULT_CHAT_FRAME` (global) | same (engine / library) | core/CoreSetup.lua:180, core/CoreSetup.lua:183, core/CoreSetup.lua:188 |
| `Enum` (global) | same | core/SpellInput.lua:168, core/SpellInput.lua:242, modules/IconGrid_Render.lua:190, modules/IconGrid_Render.lua:191, modules/IconGrid_Render.lua:230, modules/IconGrid_Render.lua:231, modules/IconGrid_Render.lua:240, modules/IconGrid_Render.lua:241 |
| `GameTooltip` (global) | same | modules/IconGrid_Render.lua:416, modules/IconGrid_Render.lua:417, modules/IconGrid_Render.lua:418, modules/IconGrid_Render.lua:419, modules/IconGrid_Render.lua:421, modules/IconGrid_Render.lua:422, modules/IconGrid_Render.lua:430, modules/IconGrid_Render.lua:431, settings/Spells_Rows.lua:85, settings/Spells_Rows.lua:86, settings/Spells_Rows.lua:87, settings/Spells_Rows.lua:109, settings/Spells_Rows.lua:174, settings/Spells_Rows.lua:175, settings/Spells_Rows.lua:176, settings/Spells_Rows.lua:178, settings/Spells_Rows.lua:272 |
| `GetClassInfo` (global) | P6 | core/Util.lua:273, core/Util.lua:278, settings/Spells_Header.lua:87, settings/Spells_Header.lua:92 |
| `GetNumClasses` (global) | P6 | core/Util.lua:273, core/Util.lua:277, settings/Spells_Header.lua:87, settings/Spells_Header.lua:91 |
| `GetNumSpecializationsForClassID` (global) | B6 absent, replace | core/Util.lua:273, core/Util.lua:283, settings/Spells_Header.lua:88, settings/Spells_Header.lua:95 |
| `GetSpecializationInfoForClassID` (global) | present; route via Compat | core/Util.lua:274, core/Util.lua:284, settings/Spells_Header.lua:88, settings/Spells_Header.lua:97 |
| `LOCALIZED_CLASS_NAMES_MALE` (global) | same | settings/Spells_Header.lua:50, settings/Spells_Header.lua:51 |
| `LibStub` (global) | same (engine / library) | core/Compat.lua:35, core/Constants.lua:63, core/CoreSetup.lua:72, core/Database.lua:757, core/Database_Migrations.lua:395, core/Database_Migrations.lua:488, core/Database_Migrations.lua:569, core/DebugLogSetup.lua:43, core/DebugLogSetup.lua:277, core/EnvSetup.lua:61, core/Events.lua:74, core/GlowSetup.lua:15, core/KickCD.lua:30, core/KickCD.lua:46, core/LauncherSetup.lua:65, core/LifecycleSetup.lua:50, core/MediaSetup.lua:57, core/MediaSetup.lua:126, core/PerfSetup.lua:33, core/PoolSetup.lua:38, core/SimSetup.lua:35, core/SkinSetup.lua:115, core/State.lua:166, modules/Castbar.lua:175, modules/Castbar_Handle.lua:41, modules/IconGrid_Handle.lua:42, modules/IconGrid_Render.lua:107, modules/IconGrid_Render.lua:124, modules/IconGrid_Render.lua:153, modules/IconGrid_Render.lua:1014, modules/Sim.lua:194, modules/Sim.lua:435, modules/SimScenario.lua:67, modules/SimStrip.lua:47, modules/UnitLabel.lua:22, settings/OptionsSetup.lua:71, settings/OptionsSetup.lua:243, settings/Panel.lua:195, settings/Profiles.lua:17, settings/Profiles.lua:19, settings/Profiles.lua:20, settings/Profiles.lua:21, settings/Profiles.lua:22, settings/SchemaSetup.lua:438, settings/Slash.lua:55, settings/Spells.lua:614, settings/Spells.lua:668, settings/Spells_Rows.lua:359 |
| `Mixin` (global) | same (engine / library) | modules/IconGrid_Render.lua:436 |
| `RAID_CLASS_COLORS` (global) | same | settings/Spells_Header.lua:57 |
| `Settings` (global) | same | settings/General.lua:383, settings/General.lua:423, settings/Grid.lua:25, settings/Grid.lua:49, settings/Profiles.lua:14, settings/Profiles.lua:96, settings/Spells.lua:873, settings/Spells.lua:883 |
| `SettingsPanel` (global) | same | settings/Spells.lua:797 |
| `StaticPopup_Show` (global) | same | settings/General.lua:110, settings/Spells.lua:755 |
| `UIParent` (global) | same (engine / library) | core/Util.lua:65, modules/Castbar_Frame.lua:225, modules/Castbar_Frame.lua:233, modules/IconGrid.lua:568, modules/IconGrid.lua:574, modules/UnitLabel.lua:165 |
| `UnitClass` (global) | same; 9 classes | core/Database.lua:231, modules/Cooldowns.lua:90, modules/Diagnostics.lua:149, modules/IconGrid.lua:193, modules/Sim.lua:82 |
| `UnitIsUnit` (global) | secret-safe | modules/Castbar_Debug.lua:71 |
| `UnitRace` (global) | per-client racial table | core/Database.lua:230 |
| `debugprofilestop` (global) | same (engine / library) | modules/Castbar.lua:521, modules/Castbar.lua:531, modules/Castbar.lua:552, modules/Cooldowns.lua:222, modules/Cooldowns.lua:225, modules/Cooldowns.lua:233, modules/Cooldowns.lua:357, modules/Cooldowns.lua:367, modules/Cooldowns.lua:458, modules/Cooldowns.lua:463, modules/Cooldowns.lua:566, modules/Cooldowns.lua:586, modules/IconGrid.lua:808, modules/IconGrid.lua:821, modules/IconGrid_Render.lua:876, modules/IconGrid_Render.lua:897, modules/IconGrid_Ticker.lua:181, modules/IconGrid_Ticker.lua:195, modules/IconGrid_Ticker.lua:205, modules/IconGrid_Visibility.lua:118, modules/IconGrid_Visibility.lua:131, modules/IconGrid_Visibility.lua:139, modules/IconGrid_Visibility.lua:145, modules/IconGrid_Visibility.lua:266, modules/IconGrid_Visibility.lua:285, modules/IconGrid_Visibility.lua:298 |
| `AddPoint` (method) | same | modules/IconGrid_Render.lua:193, modules/IconGrid_Render.lua:194, modules/IconGrid_Render.lua:195, modules/IconGrid_Render.lua:196, modules/IconGrid_Render.lua:233, modules/IconGrid_Render.lua:234, modules/IconGrid_Render.lua:235, modules/IconGrid_Render.lua:236, modules/IconGrid_Render.lua:243, modules/IconGrid_Render.lua:244, modules/IconGrid_Render.lua:245, modules/IconGrid_Render.lua:246 |
| `EvaluateRemainingDuration` (method) | same | modules/IconGrid_Render.lua:718 |
| `EvaluateTotalDuration` (method) | same | modules/IconGrid_Render.lua:715, modules/IconGrid_Render.lua:716 |
| `GetElapsedDuration` (method) | same | modules/Castbar.lua:468, modules/Castbar.lua:469, modules/Castbar.lua:542, modules/Castbar.lua:543 |
| `GetRemainingDuration` (method) | same | modules/Castbar.lua:465, modules/Castbar.lua:466, modules/Castbar.lua:539, modules/Castbar.lua:540, modules/Castbar.lua:548, modules/IconGrid_Ticker.lua:91 |
| `GetTotalDuration` (method) | same | modules/Castbar.lua:462, modules/Castbar.lua:463, modules/Castbar.lua:548, modules/Castbar_Events.lua:162, modules/Castbar_Events.lua:163 |
| `RegisterUnitEvent` (method) | same | core/CoreSetup.lua:168 |
| `SetAlphaFromBoolean` (method) | same; nil guard (3.1) | core/State.lua:119, core/State.lua:137, modules/IconGrid_Render.lua:731, modules/IconGrid_Render.lua:734, modules/IconGrid_Render.lua:735, modules/IconGrid_Ticker.lua:76, modules/IconGrid_Ticker.lua:77 |
| `SetAtlas` (method) | same | settings/Spells_Rows.lua:98, settings/Spells_Rows.lua:99 |
| `SetBackdrop` (method) | same | modules/Castbar_Skin.lua:91, modules/IconGrid_Render.lua:923 |
| `SetCooldownFromDurationObject` (method) | same | modules/IconGrid_Render.lua:798, modules/IconGrid_Ticker.lua:157 |
| `SetDrawBling` (method) | same | modules/IconGrid_Render.lua:333 |
| `SetDrawEdge` (method) | same | modules/IconGrid_Render.lua:334 |
| `SetFormattedText` (method) | same | modules/Castbar.lua:547, modules/IconGrid_Render.lua:841, modules/IconGrid_Ticker.lua:91 |
| `SetHideCountdownNumbers` (method) | same | modules/IconGrid_Render.lua:338, modules/IconGrid_Render.lua:339, modules/IconGrid_Render.lua:1004, modules/IconGrid_Render.lua:1005 |
| `SetMinMaxValues` (method) | same | modules/Castbar.lua:462, modules/Castbar.lua:463, modules/Castbar.lua:751, modules/Castbar.lua:753, modules/Castbar_Events.lua:162, modules/Castbar_Events.lua:163, modules/Castbar_Frame.lua:266 |
| `SetSpellByID` (method) | same | modules/IconGrid_Render.lua:418, modules/IconGrid_Render.lua:419, settings/Spells_Rows.lua:175 |
| `SetTimeFromStart` (method) | same | core/Compat.lua:327 |
| `SetType` (method) | same | modules/IconGrid_Render.lua:190, modules/IconGrid_Render.lua:191, modules/IconGrid_Render.lua:230, modules/IconGrid_Render.lua:231, modules/IconGrid_Render.lua:240, modules/IconGrid_Render.lua:241 |
| `SetValue` (method) | same | modules/Castbar.lua:465, modules/Castbar.lua:466, modules/Castbar.lua:468, modules/Castbar.lua:469, modules/Castbar.lua:539, modules/Castbar.lua:540, modules/Castbar.lua:542, modules/Castbar.lua:543, modules/Castbar.lua:708, modules/Castbar.lua:709, modules/Castbar.lua:752, modules/Castbar.lua:754, modules/Castbar_Frame.lua:267, settings/Spells_Header.lua:169, settings/Spells_Rows.lua:210, settings/Spells_Rows.lua:292 |
| `SetVertexColor` (method) | same | modules/IconGrid_Render.lua:816, modules/IconGrid_Render.lua:823, modules/IconGrid_Ticker.lua:85, settings/Spells_Rows.lua:104, settings/Spells_Rows.lua:248 |

Through LibKa0s-Compat (core/Compat.lua:101,160,169,252,258): `GetSpellCooldown`, `GetSpellTexture`, `GetSpellInfo`, `GetSpecialization`, `GetSpecializationInfo`,
each resolving to the `C_Spell` / `C_SpecializationInfo` member, present on Forever.

## Appendix B. Evidence files
Under `port/work/kc-code/`: `api.txt` (two-client doc diff), `seeds.txt`, `cdm.txt`, `inv.txt`, `run-{KickCD,armed}-{retail,forever}.txt`, `run-skinpin.txt`,
`exp/tests/exp.lua` (the simulation), `bin/` (scripts). The snapshot and the live repositories were not written.
