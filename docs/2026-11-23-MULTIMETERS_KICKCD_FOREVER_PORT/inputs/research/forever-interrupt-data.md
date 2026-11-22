# Forever seed data for KickCD: interrupts and stops (forever-interrupt-data)

Client: WoW Forever 1.60.1.71037 (wago product `wowf`, newest build listed on 2026-11-23). KickCD snapshot: master 333cd49.
Read-only study. No suite was run, nothing was tested in game.

Status words: **VERIFIED** = read in a named table, file or URL of that build. It means "the client data says so", not "seen in game".
**INFERRED** = reasoning over such data, stated. **UNKNOWN** = needs the named probe.

## 1. The answer

| class | spec id | true interrupt | best stop otherwise |
|---|---|---|---|
| Warrior | 1491 | Shield Bash (12), Pummel (38) | Concussion Blow (talent) |
| Paladin | 1486 | **none** | Hammer of Justice (8) |
| Hunter | 1485 | **none, pets included** | Scatter Shot or Intimidation (talents), Freezing Trap |
| Rogue | 1488 | Kick (12) | Kidney Shot, Cheap Shot, Gouge, Blind |
| Priest | 1487 | Shadow talent only: Silence (3 s lockout + 5 s silence) | Psychic Scream (14) |
| Shaman | 1489 | Earth Shock (4) | War Stomp for a Tauren |
| Mage | 1482 | Counterspell (24) | Polymorph |
| Warlock | 1490 | Felhunter only: Spell Lock (36) | Death Coil, Howl of Terror, Fear |
| Druid | 1484 | Feral talent only: Feral Charge 1238122 (20), in a form | Bash (14) |

- Every class has ONE spec id. The three trees are talent groups and have no spec id.
- The 186 shipped rows (181 list rows + 5 racials; 78 distinct class and id pairs) map to **57 keep, 13 replace, 116 drop**
  (20, 5 and 53 distinct).
- The proposal is 35 abilities covering 82 rank ids, in `forever-interrupt-data-raw/forever_seed_proposal.json`.
- The Retail list cannot be filtered at runtime: id 99 exists on Forever as Demoralizing Roar, 23920 exists and is unlearnable,
  and 19647 is only rank 2 of Spell Lock.
- An id-for-id swap is not enough. Forever has ranks, and KickCD stores and tests one id per ability (section 8).

## 2. Evidence and method

- **Primary:** `https://wago.tools/db2/<Table>/csv?build=1.60.1.71037`. The tables and their sha256 are in `forever-interrupt-data-raw/MANIFEST.sha256`.
  The rows relied on are in `forever-interrupt-data-raw/rows/<Table>.csv`, script output in `output/`, scripts in `scripts/`.
  The scripts expect the full CSVs in a sibling `dl71037/`.
- **Completeness:** three sweeps over the class, pet and racial skill lines and the live trait trees:
  effects and mechanics (with the trigger closure to depth 3), description text, and a read of every active talent.
  All Effect 68 spells of the build were listed and each player-shaped one was ruled (`output/sweep.txt`, `output/ext.txt`).
  Stops linked only by a server script and not described in their tooltip would be missed. Two linked that way were found by
  their tooltip tokens: Silence to 1241057 and Holy Wrath to 429147.
- **Lockout** = the duration of the Effect 68 spell, which the tooltips print as "prevents any spell in that school ... for $d". VERIFIED.
- **Learned:** `SkillLineAbility.AcquireMethod` is 0 = learned, 1 = automatic by skill, 2 = automatic with the skill line, 3 = never learned.
  The names come from TrinityCore `src/server/game/DataStores/DBCEnums.h` (SkillLineAbilityAcquireMethod), third party, so INFERRED.
  DB2 holds no trainer inventory: "trainer" below means method 0 on a class line with no talent or item route, **INFERRED**.
- **Cross-check 1, earlier build:** against AuraMaster's frozen 1.60.1.70938 tables
  (`docs/spell-research/2026-11-14-forever/raw/`), none of the ids here changed in SpellName, Spell, SpellEffect, SpellCooldowns,
  SpellCategories, SkillLineAbility or TraitDefinition. The one change among the ids compared is an attribute bit on Sap, which is not seeded. `output/rows.txt`.
- **Cross-check 2, Blizzard's own curation:** `CooldownSet` and `CooldownSetSpell` name Pummel 6552, Shield Bash 72, Kick 1766,
  Counterspell 2139, Earth Shock 8042, Feral Charge 1238122, Silence 15487, Bash 5211 and Hammer of Justice 853
  under the same spec ids, and War Stomp 20549 in the spec-less set (ChrSpecialization 0), always by the rank-1 id. `output/ext3.txt`. Spell Lock is not in those sets.
- **Not cross-checked:** Wowhead's Forever pages. www.wowhead.com and nether.wowhead.com answered 403 with a regional block notice
  to this machine on 2026-11-23, so they were left alone. No independent second source has confirmed any number here.
- **Cross-check 3, local frozen seeds:** RangeMaster `defaults/SpellSeeds.lua` (forever block) uses the same Kick 1766, Gouge 1776, Bash 5211,
  Hammer of Justice 853 and Earth Shock 8042. AuraMaster `defaults/Categories_Forever.lua` carries Concussion Blow 12809, Repentance 20066,
  Confounding Flash 1277455 and Feral Charge's triggered 19675 as crowd control. All agree. ConsumableMaster's and SkillMaster's records
  were read for procedure and spec ids only, since their seeds are items and skills. No SavedVariables were read.

## 3. Spec and tree ids (VERIFIED: ChrSpecialization, TalentTab, SkillLineXTraitTree, TraitNodeGroupDisplayInfo)

`GetSpecializationInfo` answering the class-wide id is measured in game for the Hunter (1485, DropWatcher `docs/forever-quirks.md`).
The other eight are INFERRED from the same table. 1493 is the pet "Default" spec. `order` is `OrderIndex` + 1.
This order confirms, from data, the order LibKa0s `Role.lua` TALENT_GROUP_ROLE marks "MATCHED, NOT CONFIRMED".

| class | spec id | order | tree | TalentTab | TraitTree | group | SkillLine | first choice | talents of this tree that change it |
|---|---|---|---|---|---|---|---|---|---|
| DRUID | 1484 | 1 | Balance | 283 | 1089 | 11328 | 574 | Bash 5211 | - |
| DRUID | 1484 | 2 | Feral Combat | 281 | 1089 | 11347 | 134 | Feral Charge 1238122 then Bash 5211 | Feral Charge; Brutal Impact (Bash -15/-30 s, +0.5/1 s) |
| DRUID | 1484 | 3 | Restoration | 282 | 1089 | 11340 | 573 | Bash 5211 | - |
| HUNTER | 1485 | 1 | Beast Mastery | 361 | 1091 | 11372 | 50 | Intimidation 19577 then Freezing Trap 1499 | Intimidation |
| HUNTER | 1485 | 2 | Marksmanship | 363 | 1091 | 11371 | 163 | Scatter Shot 19503 then Freezing Trap 1499 | Scatter Shot |
| HUNTER | 1485 | 3 | Survival | 362 | 1091 | 11370 | 51 | Freezing Trap 1499 then Scatter Shot 19503 | Survivalist's Discipline (traps -20/-40%) |
| MAGE | 1482 | 1 | Arcane | 81 | 1112 | 11582 | 237 | Counterspell 2139 | Improved Counterspell (2/4 s silence) |
| MAGE | 1482 | 2 | Fire | 41 | 1112 | 11594 | 8 | Counterspell 2139 | Impact (proc stun, not tracked) |
| MAGE | 1482 | 3 | Frost | 61 | 1112 | 11601 | 6 | Counterspell 2139 | - |
| PALADIN | 1486 | 1 | Holy | 382 | 1100 | 11486 | 594 | Hammer of Justice 853 | - |
| PALADIN | 1486 | 2 | Protection | 383 | 1100 | 11541 | 267 | Hammer of Justice 853 | Improved Hammer of Justice (-5/-10/-15 s) |
| PALADIN | 1486 | 3 | Retribution | 381 | 1100 | 11559 | 184 | Hammer of Justice 853 then Repentance 20066 | Repentance |
| PRIEST | 1487 | 1 | Discipline | 201 | 1114 | 11608 | 613 | Psychic Scream 8122 | - |
| PRIEST | 1487 | 2 | Holy | 202 | 1114 | 11615 | 56 | Psychic Scream 8122 | - |
| PRIEST | 1487 | 3 | Shadow | 203 | 1114 | 11622 | 78 | Silence 15487 then Psychic Scream 8122 | Silence; Improved Psychic Scream (-2/-4 s) |
| ROGUE | 1488 | 1 | Assassination | 182 | 1111 | 11580 | 253 | Kick 1766 | Improved Gouge (+0.5/1/1.5 s) |
| ROGUE | 1488 | 2 | Combat | 181 | 1111 | 11573 | 38 | Kick 1766 | Improved Kick (50/100% 2 s silence) |
| ROGUE | 1488 | 3 | Subtlety | 183 | 1111 | 11572 | 39 | Kick 1766 | Elusiveness (Blind -45/-90 s) |
| SHAMAN | 1489 | 1 | Elemental | 261 | 1082 | 11326 | 375 | Earth Shock 8042 | Reverberation (shocks -0.2 to -1.0 s) |
| SHAMAN | 1489 | 2 | Enhancement | 263 | 1082 | 11363 | 373 | Earth Shock 8042 | - |
| SHAMAN | 1489 | 3 | Restoration | 262 | 1082 | 11362 | 374 | Earth Shock 8042 | - |
| WARLOCK | 1490 | 1 | Affliction | 302 | 1116 | 11629 | 355 | Spell Lock 19244 | - |
| WARLOCK | 1490 | 2 | Demonology | 303 | 1116 | 11636 | 354 | Spell Lock 19244 | Improved Felhunter (Spell Lock -2/-4/-6 s) |
| WARLOCK | 1490 | 3 | Destruction | 301 | 1116 | 11637 | 593 | Spell Lock 19244 | - |
| WARRIOR | 1491 | 1 | Arms | 161 | 1117 | 11650 | 26 | Pummel 6552 then Shield Bash 72 | - |
| WARRIOR | 1491 | 2 | Fury | 164 | 1117 | 11657 | 256 | Pummel 6552 then Shield Bash 72 | Improved Intercept (-5/-10 s) |
| WARRIOR | 1491 | 3 | Protection | 163 | 1117 | 11670 | 257 | Shield Bash 72 then Pummel 6552 | Concussion Blow; Improved Shield Bash (50/100% 3 s silence) |

"First choice" is what a list per tree would put first. Trainer spells are open to every tree, and a talent only needs its points,
so a hybrid can hold another tree's stop.

## 4. Interrupts, every rank (VERIFIED except "how learned")

Sources: SpellName, Spell (subtext), SpellCooldowns, SpellCategories, SpellEffect, SpellMisc with SpellDuration, SpellLevels,
SpellShapeshift, SpellEquippedItems. `cd cat` is the shared cooldown category.

| class | spell | rank | id | cd s | cd cat | GCD s | lockout s | level | form / gear | cast s | how learned |
|---|---|---|---|---|---|---|---|---|---|---|---|
| WARRIOR | Pummel | Rank 1 | 6552 | 10 | 88 | 1.5 | 4 | 38 | Berserker Stance | 0 | trainer |
| WARRIOR | Pummel | Rank 2 | 6554 | 10 | 88 | 1.5 | 4 | 58 | Berserker Stance | 0 | trainer |
| WARRIOR | Shield Bash | Rank 1 | 72 | 12 | 88 | 1.5 | 6 | 12 | Battle Stance/Defensive Stance; shield | 0 | trainer; needs a shield |
| WARRIOR | Shield Bash | Rank 2 | 1671 | 12 | 88 | 1.5 | 6 | 32 | Battle Stance/Defensive Stance; shield | 0 | trainer; needs a shield |
| WARRIOR | Shield Bash | Rank 3 | 1672 | 12 | 88 | 1.5 | 6 | 52 | Battle Stance/Defensive Stance; shield | 0 | trainer; needs a shield |
| ROGUE | Kick | Rank 1 | 1766 | 10 | 88 | 1 | 5 | 12 | - | 0 | trainer |
| ROGUE | Kick | Rank 2 | 1767 | 10 | 88 | 1 | 5 | 26 | - | 0 | trainer |
| ROGUE | Kick | Rank 3 | 1768 | 10 | 88 | 1 | 5 | 42 | - | 0 | trainer |
| ROGUE | Kick | Rank 4 | 1769 | 10 | 88 | 1 | 5 | 58 | - | 0 | trainer |
| PRIEST | Silence | - | 15487 | 45 | - | 1.5 | 3 | 30 (talent gate, INFERRED) | Shadowform or none | 0 | talent: Shadow, 20 points; 5 s silence plus 3 s lockout (1241057) |
| SHAMAN | Earth Shock | Rank 1 | 8042 | 6 | 19 | 1.5 | 2 | 4 | - | 0 | trainer; shared with Flame and Frost Shock |
| SHAMAN | Earth Shock | Rank 2 | 8044 | 6 | 19 | 1.5 | 2 | 8 | - | 0 | trainer; shared with Flame and Frost Shock |
| SHAMAN | Earth Shock | Rank 3 | 8045 | 6 | 19 | 1.5 | 2 | 14 | - | 0 | trainer; shared with Flame and Frost Shock |
| SHAMAN | Earth Shock | Rank 4 | 8046 | 6 | 19 | 1.5 | 2 | 24 | - | 0 | trainer; shared with Flame and Frost Shock |
| SHAMAN | Earth Shock | Rank 5 | 10412 | 6 | 19 | 1.5 | 2 | 36 | - | 0 | trainer; shared with Flame and Frost Shock |
| SHAMAN | Earth Shock | Rank 6 | 10413 | 6 | 19 | 1.5 | 2 | 48 | - | 0 | trainer; shared with Flame and Frost Shock |
| SHAMAN | Earth Shock | Rank 7 | 10414 | 6 | 19 | 1.5 | 2 | 60 | - | 0 | trainer; shared with Flame and Frost Shock |
| MAGE | Counterspell | - | 2139 | 30 | 88 | 0 | 10 | 24 | - | 0 | trainer; item 4148 also teaches it |
| WARLOCK | Spell Lock | Rank 1 | 19244 | 30 | 88 | 1.5 | 6 | 36 | - | 0 | pet (Felhunter): grimoire items 16388/16389; plus 3 s silence 24259 |
| WARLOCK | Spell Lock | Rank 2 | 19647 | 30 | 88 | 1.5 | 8 | 52 | - | 0 | pet (Felhunter): grimoire items 16388/16389; plus 3 s silence 24259 |
| DRUID | Feral Charge | - | 1238122 | 15 | 2182 | 0 | 4 | 20 | Cat Form/Bear Form/Dire Bear Form | 0 | talent: Feral Combat, 10 points; lockout on triggered 19675 |

Notes:

- Only Counterspell and Feral Charge are off the global cooldown. The others cost 1.0 s (Kick) or 1.5 s, unlike Retail's kicks. VERIFIED.
  `Const.GCD_UPPER` is 1.6 (`core/Constants.lua:79`), so the existing GCD curve still hides those swipes. INFERRED.
- Pummel and Shield Bash share category 88, so pressing one starts the other's cooldown (INFERRED from the category; probe P4).
  Kick, Counterspell and Spell Lock carry 88 too, with no effect across classes.
- Earth Shock shares category 19 with Flame and Frost Shock, so either of those puts the interrupt on cooldown. VERIFIED in data.
- Silence: the tooltip reads "silences ... for $d and interrupting their spellcasts for $1241057d". 1241057 is Effect 68, 3 s.
  The link is server side. VERIFIED tooltip and data, UNKNOWN that it lands on an interruptible mob (probe P6).
- Counterspell's category cooldown is 30 s. Improved Counterspell 11255 adds a 2 or 4 s silence.
- Feral Charge: 1238122 is the cast to track, usable in Cat, Bear and Dire Bear by the shapeshift mask, though the tooltip says bear forms only
  (UNKNOWN, probe P6). 16979 "Feral Charge (Bear)" is method 3 in a tree with no skill line: do not seed it.
  19675 is the triggered interrupt: never seed it.
- Silence's level 30 is INFERRED: a gate of 20 points (TraitCond) and one point a level from 10 (TraitCurrencySource).

### Player-shaped interrupts that must NOT be seeded

| id | spell | why | status |
|---|---|---|---|
| 425609 | Rebuke (paladin) | method 3; granted only by override aura 425616, which comes from enchant 7042 of "Engrave Pants - Rebuke" | unreachable: INFERRED |
| 410176 | Skull Bash (druid) | method 3; rune chain 415759, enchant 7491 | unreachable: INFERRED |
| 440488, 400009 | Shockwave, Between the Eyes (stuns) | method 3; rune chains | unreachable: INFERRED |
| 412787 | Disrupt | no skill line, talent or teacher | VERIFIED absent from every reach table |
| 427745 | Felguard Intercept | method 3; Summon Felguard 427733 has no skill line or talent | unreachable: INFERRED |
| 408681-408689, 1220744-1220750 | Earth Shock copies | no skill line, talent or teacher | VERIFIED absent from every reach table |

Runes are Season of Discovery leftovers here: skill lines 2851 and 2853 still exist, but the 71037 UI source has no "engrav" string
in any file (`grep -rli engrav Interface`). Probe P8 would close it.

## 5. Stuns, silences and other stops (VERIFIED except "how learned")

| class | spell | rank | id | cd s | cd cat | GCD s | lockout s | level | form / gear | cast s | how learned |
|---|---|---|---|---|---|---|---|---|---|---|---|
| WARRIOR | Concussion Blow | - | 12809 | 45 | - | 0 | - | 30 | - | 0 | talent: Protection, 20 points |
| WARRIOR | Intimidating Shout | - | 5246 | 180 | - | 1.5 | - | 22 | - | 0 | trainer |
| WARRIOR | Intercept | Rank 1 | 20252 | 30 | 872 | 0 | - | 30 | Berserker Stance | 0 | trainer; stun is the triggered 20253/20614/20615 |
| WARRIOR | Intercept | Rank 2 | 20616 | 30 | 872 | 0 | - | 42 | Berserker Stance | 0 | trainer; stun is the triggered 20253/20614/20615 |
| WARRIOR | Intercept | Rank 3 | 20617 | 30 | 872 | 0 | - | 52 | Berserker Stance | 0 | trainer; stun is the triggered 20253/20614/20615 |
| PALADIN | Hammer of Justice | Rank 1 | 853 | 60 | 32 | 1.5 | - | 8 | - | 0 | trainer |
| PALADIN | Hammer of Justice | Rank 2 | 5588 | 60 | 32 | 1.5 | - | 24 | - | 0 | trainer |
| PALADIN | Hammer of Justice | Rank 3 | 5589 | 60 | 32 | 1.5 | - | 40 | - | 0 | trainer |
| PALADIN | Hammer of Justice | Rank 4 | 10308 | 60 | 32 | 1.5 | - | 54 | - | 0 | trainer |
| PALADIN | Repentance | - | 20066 | 60 | - | 1.5 | - | 20 | - | 0 | talent: Retribution, 20 points; humanoids |
| PALADIN | Holy Wrath | Rank 1 | 2812 | 60 | 35 | 1.5 | - | 50 | - | 2 | trainer; 2 s stun 429147, undead and demons |
| PALADIN | Holy Wrath | Rank 2 | 10318 | 60 | 35 | 1.5 | - | 60 | - | 2 | trainer; 2 s stun 429147, undead and demons |
| HUNTER | Scatter Shot | - | 19503 | 30 | - | 1.5 | - | 30 | - | 0 | talent: Marksmanship, 20 points; needs a ranged weapon |
| HUNTER | Intimidation | - | 19577 | 60 | - | 1.5 | - | 30 | - | 0 | talent: Beast Mastery, 20 points; pet stuns on next hit (24394, 3 s) |
| HUNTER | Freezing Trap | Rank 1 | 1499 | 30 | 411 | 1.5 | - | 20 | - | 0 | trainer; freeze is 3355/14308/14309, 10/15/20 s |
| HUNTER | Freezing Trap | Rank 2 | 14310 | 30 | 411 | 1.5 | - | 40 | - | 0 | trainer; freeze is 3355/14308/14309, 10/15/20 s |
| HUNTER | Freezing Trap | Rank 3 | 14311 | 30 | 411 | 1.5 | - | 60 | - | 0 | trainer; freeze is 3355/14308/14309, 10/15/20 s |
| HUNTER | Scare Beast | Rank 1 | 1513 | 30 | 33 | 1.5 | - | 14 | - | 1.5 | trainer; beasts |
| HUNTER | Scare Beast | Rank 2 | 14326 | 30 | 33 | 1.5 | - | 30 | - | 1.5 | trainer; beasts |
| HUNTER | Scare Beast | Rank 3 | 14327 | 30 | 33 | 1.5 | - | 46 | - | 1.5 | trainer; beasts |
| ROGUE | Gouge | Rank 1 | 1776 | 10 | 33 | 1 | - | 6 | - | 0 | trainer |
| ROGUE | Gouge | Rank 2 | 1777 | 10 | 33 | 1 | - | 18 | - | 0 | trainer |
| ROGUE | Gouge | Rank 3 | 8629 | 10 | 33 | 1 | - | 32 | - | 0 | trainer |
| ROGUE | Gouge | Rank 4 | 11285 | 10 | 33 | 1 | - | 46 | - | 0 | trainer |
| ROGUE | Gouge | Rank 5 | 11286 | 10 | 33 | 1 | - | 60 | - | 0 | trainer |
| ROGUE | Kidney Shot | Rank 1 | 408 | 20 | 270 | 1 | - | 30 | - | 0 | trainer; finisher, 1-5 s / 2-6 s |
| ROGUE | Kidney Shot | Rank 2 | 8643 | 20 | 270 | 1 | - | 50 | - | 0 | trainer; finisher, 1-5 s / 2-6 s |
| ROGUE | Cheap Shot | - | 1833 | 0 | - | 1 | - | 26 | Stealth | 0 | trainer |
| ROGUE | Blind | - | 2094 | 300 | - | 1 | - | 34 | - | 0 | trainer; reagent item 5530 |
| PRIEST | Psychic Scream | Rank 1 | 8122 | 30 | 43 | 1.5 | - | 14 | Shadowform or none | 0 | trainer |
| PRIEST | Psychic Scream | Rank 2 | 8124 | 30 | 43 | 1.5 | - | 28 | Shadowform or none | 0 | trainer |
| PRIEST | Psychic Scream | Rank 3 | 10888 | 30 | 43 | 1.5 | - | 42 | Shadowform or none | 0 | trainer |
| PRIEST | Psychic Scream | Rank 4 | 10890 | 30 | 43 | 1.5 | - | 56 | Shadowform or none | 0 | trainer |
| PRIEST | Confounding Flash | - | 1277455 | 120 | - | 0 | - | 10 | - | 0.5 | Gnome priest racial spell; taught by 1277662 |
| PRIEST | Mind Control | Rank 1 | 605 | 0 | - | 1.5 | - | 30 | Shadowform or none | 3 | trainer; humanoids |
| PRIEST | Mind Control | Rank 2 | 10911 | 0 | - | 1.5 | - | 44 | Shadowform or none | 3 | trainer; humanoids |
| PRIEST | Mind Control | Rank 3 | 10912 | 0 | - | 1.5 | - | 58 | Shadowform or none | 3 | trainer; humanoids |
| SHAMAN | Grounding Totem | - | 8177 | 15 | 230 | 1 | - | 30 | - | 0 | trainer; redirects one spell |
| MAGE | Polymorph | Rank 1 | 118 | 0 | - | 1.5 | - | 8 | - | 1.5 | trainer; variants 28270/28271/28272 are separate spells |
| MAGE | Polymorph | Rank 2 | 12824 | 0 | - | 1.5 | - | 20 | - | 1.5 | trainer; variants 28270/28271/28272 are separate spells |
| MAGE | Polymorph | Rank 3 | 12825 | 0 | - | 1.5 | - | 40 | - | 1.5 | trainer; variants 28270/28271/28272 are separate spells |
| MAGE | Polymorph | Rank 4 | 12826 | 0 | - | 1.5 | - | 60 | - | 1.5 | trainer; variants 28270/28271/28272 are separate spells |
| WARLOCK | Seduction | - | 6358 | 0 | - | 1.5 | - | 26 | - | 1.5 | pet (Succubus): grimoire item 16379; humanoids |
| WARLOCK | Death Coil | Rank 1 | 6789 | 120 | 633 | 1.5 | - | 42 | - | 0 | trainer |
| WARLOCK | Death Coil | Rank 2 | 17925 | 120 | 633 | 1.5 | - | 50 | - | 0 | trainer |
| WARLOCK | Death Coil | Rank 3 | 17926 | 120 | 633 | 1.5 | - | 58 | - | 0 | trainer |
| WARLOCK | Howl of Terror | Rank 1 | 5484 | 40 | 634 | 1.5 | - | 40 | - | 2 | trainer |
| WARLOCK | Howl of Terror | Rank 2 | 17928 | 40 | 634 | 1.5 | - | 54 | - | 2 | trainer |
| WARLOCK | Fear | Rank 1 | 5782 | 0 | - | 1.5 | - | 8 | - | 1.5 | trainer |
| WARLOCK | Fear | Rank 2 | 6213 | 0 | - | 1.5 | - | 32 | - | 1.5 | trainer |
| WARLOCK | Fear | Rank 3 | 6215 | 0 | - | 1.5 | - | 56 | - | 1.5 | trainer |
| DRUID | Bash | Rank 1 | 5211 | 60 | 32 | 1.5 | - | 14 | Bear Form/Dire Bear Form | 0 | trainer |
| DRUID | Bash | Rank 2 | 6798 | 60 | 32 | 1.5 | - | 30 | Bear Form/Dire Bear Form | 0 | trainer |
| DRUID | Bash | Rank 3 | 8983 | 60 | 32 | 1.5 | - | 46 | Bear Form/Dire Bear Form | 0 | trainer |
| DRUID | Pounce | Rank 1 | 9005 | 0 | - | 1 | - | 36 | Cat Form | 0 | trainer; prowling and behind |
| DRUID | Pounce | Rank 2 | 9823 | 0 | - | 1 | - | 46 | Cat Form | 0 | trainer; prowling and behind |
| DRUID | Pounce | Rank 3 | 9827 | 0 | - | 1 | - | 56 | Cat Form | 0 | trainer; prowling and behind |
| DRUID | Hibernate | Rank 1 | 2637 | 0 | - | 1.5 | - | 18 | Moonkin Form or none | 1.5 | trainer; beasts and dragonkin |
| DRUID | Hibernate | Rank 2 | 18657 | 0 | - | 1.5 | - | 38 | Moonkin Form or none | 1.5 | trainer; beasts and dragonkin |
| DRUID | Hibernate | Rank 3 | 18658 | 0 | - | 1.5 | - | 58 | Moonkin Form or none | 1.5 | trainer; beasts and dragonkin |
| RACE | War Stomp | Racial | 20549 | 90 | - | 0 | - | 1 (racial) | - | 0.5 | racial: Tauren (automatic with the racial skill line) |

- Stances and forms matter for the alternates too. A spell whose mask carries "or none" has attribute ALLOW_WHILE_NOT_SHAPESHIFTED.
- Freezing Trap 1499 has no not-in-combat attribute (SpellMisc Attributes_0 bit 0x10000000 clear), so nothing in the data stops an in-combat trap.
- Intimidation stuns on the pet's next successful hit, so it is not an instant stop.
- Cheap Shot, Pounce, Polymorph, Fear, Mind Control and Seduction have no cooldown: their icons would always read ready when known.
- Considered and excluded: Charge (attribute: not in combat), Sap (out-of-combat targets), Banish, Shackle Undead and Turn Undead
  (one creature type, as hard CC), procs (Blackout, Impact, Pyroclasm, Improved Starfire, Seal of Justice, Improved Concussive Shot),
  Frost Nova and Entangling Roots (roots do not stop casts), Tremor Totem and Will of the Forsaken (defensive), Inferno (1 h summon).
- No learnable Wyvern Sting, Silencing Shot or Dragon's Breath exists in this build: those names have no skill line and no talent. VERIFIED.

### Talents that change these rows (VERIFIED: TraitDefinitionEffectPoints with CurvePoint)

| talent | id | tree | effect, per rank |
|---|---|---|---|
| Improved Shield Bash | 12311 | Protection | 50/100% chance of a 3 s silence |
| Improved Intercept | 20504 | Fury | Intercept -5/-10 s |
| Improved Hammer of Justice | 20487 | Protection | -5/-10/-15 s |
| Improved Kick | 13754 | Combat | 50/100% chance of a 2 s silence |
| Improved Gouge | 13741 | Assassination | +0.5/1/1.5 s |
| Elusiveness | 13981 | Subtlety | Blind -45/-90 s |
| Improved Counterspell | 11255 | Arcane | 2/4 s silence |
| Improved Psychic Scream | 15392 | Shadow | -2/-4 s |
| Reverberation | 16040 | Elemental | shocks -0.2 to -1.0 s over 5 ranks |
| Improved Felhunter | 1225217 | Demonology | Spell Lock -2/-4/-6 s |
| Brutal Impact | 16940 | Feral Combat | Bash -15/-30 s; Bash and Pounce +0.5/1 s |
| Survivalist's Discipline | 1310496 | Survival | trap cooldown -20/-40% |

Guardian Totems 16258 (Grounding Totem) and Purifying Power 429144 (Holy Wrath) also modify optional rows (`output/ext8.txt`).
KickCD reads the live cooldown, so it needs none of these numbers.

## 6. Pets and racials

- **Pet interrupt:** Spell Lock on the Felhunter (skill line 189), ranks 19244 and 19647, taught by items 16388 "Grimoire of Spell Lock
  (Rank 1)", level 36, and 16389 (Rank 2), level 52, through 20433 and 20434 (effect 36). VERIFIED (ItemSparse, ItemEffect, SpellEffect).
- **Other pet stops:** Seduction 6358 (Succubus, grimoire 16379). Intimidation's stun 24394 is on "Pet - Generic", and the id to track is the
  player's 19577. No hunter pet family line carries an Effect 68 or another castable stun or silence. Boar Charge is a root. VERIFIED by the sweep.
- **Racials:** War Stomp 20549 is the only cast-stopping racial: 0.5 s cast, 2 s stun, 90 s, no GCD (Tauren Racial line 124).
  Tauren play Warrior, Hunter, Shaman and Druid here (CharBaseInfo).
  Confounding Flash 1277455 is a priest spell masked to Gnome (SkillLineAbility RaceMasks), not a racial skill, so it belongs in the priest list.
- Skyborne (races 95 and 96, both file string "Skyborne") have no stop. Walk on Air's knockback effect targets the caster. VERIFIED.
- `NS.RaceCastStoppers` on Forever is `{ Tauren = 20549 }`.

## 7. Proposed seed

One list per class spec id. The grid shows only known spells and makes the first shown one the primary (`modules/IconGrid.lua`, `isRenderable`,
`ordered[1]`), so talent and level gaps resolve themselves once availability is rank-aware.

| class | spec id | default list, in order (rank-1 id) | owner-optional additions |
|---|---|---|---|
| WARRIOR | 1491 | Pummel 6552, Shield Bash 72, Concussion Blow 12809, Intimidating Shout 5246 | Intercept 20252 |
| PALADIN | 1486 | Hammer of Justice 853, Repentance 20066 | Holy Wrath 2812 |
| HUNTER | 1485 | Scatter Shot 19503, Intimidation 19577, Freezing Trap 1499 | Scare Beast 1513 |
| ROGUE | 1488 | Kick 1766, Kidney Shot 408, Cheap Shot 1833, Blind 2094 | Gouge 1776 |
| PRIEST | 1487 | Silence 15487, Psychic Scream 8122, Mind Control 605 | Confounding Flash 1277455 |
| SHAMAN | 1489 | Earth Shock 8042 | Grounding Totem 8177 |
| MAGE | 1482 | Counterspell 2139, Polymorph 118 | - |
| WARLOCK | 1490 | Spell Lock 19244, Death Coil 6789, Howl of Terror 5484, Fear 5782 | Seduction 6358 |
| DRUID | 1484 | Feral Charge 1238122, Bash 5211 | Pounce 9005, Hibernate 2637 |

- Core = the kept rows plus the replacements and the interrupts the class can reach (KickCD `docs/validate-seeds.md` admits interrupts on the data).
- Optional = curation calls, which that procedure leaves to the owner. Recommendation: ship core, plus Gouge and Intercept.
- Category follows Retail's closed set: Silence stays "silence" and Feral Charge is "interrupt".
- The JSON carries every rank list. Seed one entry per ability, never one entry per rank.

## 8. What the data forces in KickCD

1. **Ranks (UNKNOWN behavior, VERIFIED shape).** `SkillLineAbility.SupercedesSpell` chains Pummel, Shield Bash, Kick, Gouge, Kidney Shot,
   Intercept, Bash, Pounce and Spell Lock. It is 0 for Earth Shock, Hammer of Justice, Psychic Scream, Fear, Death Coil and Polymorph ranks.
   INFERRED: the first group replaces the lower rank in the spellbook and the second keeps every rank known.
   If so, a seeded rank-1 id disappears at level 58 for Kick, and seeding every rank would draw seven Earth Shock icons.
   Needed: an entry is an ability (a rank list), resolved to the highest known id for availability, cooldown, usability and texture,
   with a cast of any rank matched to the entry. `C_SpellBook.IsSpellBookItemLowRank` exists (SpellBookDocumentation.lua:651).
   `GetBaseSpell` is documented for overrides only (SpellDocumentation.lua:90), so do not rely on it for ranks. Probes P2 and P3.
2. **Spec keys (VERIFIED).** `Const.SPEC` holds no Forever id, so `NS.DefaultSpells[class][1485]` is nil and the addon would track nothing.
   Add the nine ids with Forever-only tokens. `SPEC_TOKEN` strips a trailing `_[A-Z]+`, so avoid underscored tokens.
3. **Spec enumeration (INFERRED broken on Forever).** `core/Util.lua:273` and `settings/Spells_Header.lua:87` need the bare
   `GetNumSpecializationsForClassID`. Its only definition in the 71037 source is
   `Blizzard_DeprecatedSpecialization/Deprecated_Specialization_Standard.lua:10`, in an addon whose TOC loads for `classic, standard`
   and not `camelot`. Both maps would stay empty. Use `C_SpecializationInfo.GetNumSpecializationsForClassID`
   (SpecializationInfoDocumentation.lua:137). Probe P1.
4. **Class enumeration (INFERRED broken).** `core/Util.lua:277`, `settings/Spells_Header.lua:91` and `core/Database.lua:459` loop
   `1..GetNumClasses()` as class ids. Forever's ids are 1-5, 7, 8, 9, 11, so a count of 9 would never reach Druid 11. Blizzard replaced that
   loop with `C_SpecializationInfo.GetAllClassIDs()` at the same call sites (Blizzard_ClassMenu.lua:99 on Forever against :99 on live;
   SpecializationInfoDocumentation.lua:57). Probe P1.
5. **Availability (VERIFIED dependency, UNKNOWN value).** `IsPlayerSpell` and `IsSpellKnown` exist only in
   `Blizzard_DeprecatedSpellBook/Deprecated_SpellBook.lua:11,16`, behind `GetCVarBool("loadDeprecationFallbacks")`. If it is off,
   `Compat.IsSpellAvailable` answers false for everything. Use `C_SpellBook.IsSpellKnown(id, bank)` and `IsSpellInSpellBook` (documented at :738 and :720).
   Their deprecated shims are exactly those calls.
6. **The GCD sentinel (VERIFIED absent).** Spell 61304 has no row in SpellName, Spell, SpellMisc, SpellCooldowns or SpellCategories of 71037.
   `C_Spell.GetSpellCooldown` "Returns nil if spell is not found", so the "(gcd)" mark in the debug log (`modules/Cooldowns.lua:76,447`) never fires.
   Only that log uses it. Probe P5.
7. **Secrets.** `GetSpellCooldown` is SecretWhenCooldownsRestricted, while `isActive` and `isOnGCD` are NeverSecret
   (SpellSharedDocumentation.lua:26,30). VERIFIED docs. The duration-object path KickCD uses exists (SpellDocumentation.lua:327).
8. **Simulator ids (VERIFIED absent).** `modules/SimScenario.lua:52-53,90-91` uses 147362, 96231, 234153 and 116858, none in 71037's SpellName.
   6552, 2139, 686, 5782 and 15407 exist.
9. **Seed tool.** `tools/seeds/seeds.py` derives reach from tables this build does not serve (wago answers "Table not found" for SpecializationSpells,
   SpecSetMember, TraitNodeXTraitCond and TraitTreeLoadout). A `forever` flavor needs its own reach: SkillLineAbility with AcquireMethod other than 3,
   trait trees joined through SkillLineXTraitTree, and TraitNodeGroupDisplayInfo for the tree. Do not use the `Talent` table alone:
   it still lists old talents and misses 1238122.

## 9. Every row of `defaults/Spells.lua`

`rows (spec)` lists each Retail row the line covers. Presence, names and reach are VERIFIED (SpellName, SkillLineAbility, trait tables).
The verdict is a judgment on those.

| class | Retail id | Retail name | rows (spec) | name of that id on Forever | verdict | Forever id | why |
|---|---|---|---|---|---|---|---|
| DEATHKNIGHT | 47528 | Mind Freeze | BLOOD, FROST_DK, UNHOLY | (absent) | **drop** | - | no such class; absent |
| DEATHKNIGHT | 49576 | Death Grip | BLOOD, FROST_DK, UNHOLY | (absent) | **drop** | - | no such class; absent |
| DEATHKNIGHT | 108199 | Gorefiend's Grasp | BLOOD | (absent) | **drop** | - | no such class; absent |
| DEATHKNIGHT | 221562 | Asphyxiate | BLOOD, FROST_DK, UNHOLY | (absent) | **drop** | - | no such class; absent |
| DEATHKNIGHT | 207167 | Blinding Sleet | BLOOD, FROST_DK, UNHOLY | (absent) | **drop** | - | no such class; absent |
| DEATHKNIGHT | 1263569 | Abomination Limb | BLOOD | (absent) | **drop** | - | no such class; absent |
| DEATHKNIGHT | 279302 | Frostwyrm's Fury | FROST_DK | (absent) | **drop** | - | no such class; absent |
| DEMONHUNTER | 183752 | Disrupt | HAVOC, VENGEANCE, DEVOURER | (absent) | **drop** | - | no such class; absent |
| DEMONHUNTER | 179057 | Chaos Nova | HAVOC, VENGEANCE | (absent) | **drop** | - | no such class; absent |
| DEMONHUNTER | 217832 | Imprison | HAVOC, VENGEANCE, DEVOURER | (absent) | **drop** | - | no such class; absent |
| DEMONHUNTER | 207684 | Sigil of Misery | HAVOC, VENGEANCE, DEVOURER | (absent) | **drop** | - | no such class; absent |
| DEMONHUNTER | 202138 | Sigil of Chains | VENGEANCE | (absent) | **drop** | - | no such class; absent |
| DEMONHUNTER | 202137 | Sigil of Silence | VENGEANCE | (absent) | **drop** | - | no such class; absent |
| DEMONHUNTER | 1234195 | Void Nova | DEVOURER | (absent) | **drop** | - | no such class; absent |
| DRUID | 78675 | Solar Beam | BALANCE | (absent) | **drop** | - | absent; no druid silence |
| DRUID | 132469 | Typhoon | BALANCE, FERAL, GUARDIAN, RESTORATION_DRUID | (absent) | **drop** | - | absent |
| DRUID | 5211 | Mighty Bash | BALANCE, FERAL, GUARDIAN, RESTORATION_DRUID | Bash | **keep** | 5211 | same id, now named Bash; add ranks 6798, 8983 |
| DRUID | 33786 | Cyclone | BALANCE, FERAL, GUARDIAN, RESTORATION_DRUID | (absent) | **drop** | - | absent; Hibernate 2637 is an optional analog |
| DRUID | 99 | Incapacitating Roar | BALANCE, FERAL, GUARDIAN, RESTORATION_DRUID | Demoralizing Roar | **drop** | - | ID COLLISION: 99 is Demoralizing Roar here, which stops nothing |
| DRUID | 106839 | Skull Bash | FERAL, GUARDIAN | (absent) | **replace** | 1238122 | Feral Charge, the only reachable druid interrupt (rune Skull Bash 410176 is not learnable) |
| DRUID | 22570 | Maim | FERAL | (absent) | **drop** | - | absent; Pounce 9005 is an optional analog |
| EVOKER | 351338 | Quell | DEVASTATION, PRESERVATION, AUGMENTATION | (absent) | **drop** | - | no such class; absent |
| EVOKER | 357214 | Wing Buffet | DEVASTATION, PRESERVATION, AUGMENTATION | (absent) | **drop** | - | no such class; absent |
| EVOKER | 368970 | Tail Swipe | DEVASTATION, PRESERVATION, AUGMENTATION | (absent) | **drop** | - | no such class; absent |
| EVOKER | 360806 | Sleep Walk | DEVASTATION, PRESERVATION, AUGMENTATION | (absent) | **drop** | - | no such class; absent |
| HUNTER | 147362 | Counter Shot | BEASTMASTERY, MARKSMANSHIP | (absent) | **drop** | - | absent; hunters have no interrupt |
| HUNTER | 19577 | Intimidation | BEASTMASTERY, SURVIVAL | Intimidation | **keep** | 19577 | same id; talent; pet stuns on its next hit |
| HUNTER | 109248 | Binding Shot | BEASTMASTERY, MARKSMANSHIP, SURVIVAL | (absent) | **drop** | - | absent |
| HUNTER | 187650 | Freezing Trap | BEASTMASTERY, MARKSMANSHIP, SURVIVAL | (absent) | **replace** | 1499, 14310, 14311 | Freezing Trap |
| HUNTER | 213691 | Scatter Shot | BEASTMASTERY, MARKSMANSHIP | (absent) | **replace** | 19503 | Scatter Shot |
| HUNTER | 392060 | Wailing Arrow | BEASTMASTERY, MARKSMANSHIP | (absent) | **drop** | - | absent |
| HUNTER | 187707 | Muzzle | SURVIVAL | (absent) | **drop** | - | absent; hunters have no interrupt |
| MAGE | 2139 | Counterspell | ARCANE, FIRE, FROST_MAGE | Counterspell | **keep** | 2139 | same id; interrupt, single rank |
| MAGE | 31661 | Dragon's Breath | ARCANE, FIRE, FROST_MAGE | (absent) | **drop** | - | absent under this id; no reachable Dragon's Breath |
| MAGE | 113724 | Ring of Frost | ARCANE, FIRE, FROST_MAGE | (absent) | **drop** | - | absent |
| MAGE | 118 | Polymorph | ARCANE, FIRE, FROST_MAGE | Polymorph | **keep** | 118 | same id; add ranks 12824, 12825, 12826 |
| MAGE | 157980 | Supernova | ARCANE | (absent) | **drop** | - | absent |
| MAGE | 383121 | Mass Polymorph | ARCANE, FIRE, FROST_MAGE | (absent) | **drop** | - | absent |
| MONK | 116705 | Spear Hand Strike | BREWMASTER, MISTWEAVER, WINDWALKER | (absent) | **drop** | - | no such class; absent |
| MONK | 119381 | Leg Sweep | BREWMASTER, MISTWEAVER, WINDWALKER | (absent) | **drop** | - | no such class; absent |
| MONK | 115078 | Paralysis | BREWMASTER, MISTWEAVER, WINDWALKER | (absent) | **drop** | - | no such class; absent |
| MONK | 198898 | Song of Chi-Ji | BREWMASTER, MISTWEAVER, WINDWALKER | (absent) | **drop** | - | no such class; absent |
| MONK | 116844 | Ring of Peace | BREWMASTER, MISTWEAVER, WINDWALKER | (absent) | **drop** | - | no such class; absent |
| PALADIN | 853 | Hammer of Justice | HOLY_PALADIN, PROTECTION_PALADIN, RETRIBUTION | Hammer of Justice | **keep** | 853 | same id; add ranks 5588, 5589, 10308 |
| PALADIN | 20066 | Repentance | HOLY_PALADIN, PROTECTION_PALADIN, RETRIBUTION | Repentance | **keep** | 20066 | same id; talent |
| PALADIN | 115750 | Blinding Light | HOLY_PALADIN, PROTECTION_PALADIN, RETRIBUTION | (absent) | **drop** | - | absent |
| PALADIN | 96231 | Rebuke | PROTECTION_PALADIN, RETRIBUTION | (absent) | **drop** | - | absent; Rebuke 425609 exists but is NeverLearned, rune-only |
| PALADIN | 31935 | Avenger's Shield | PROTECTION_PALADIN | (absent) | **drop** | - | absent |
| PRIEST | 15487 | Silence | DISCIPLINE, SHADOW | Silence | **keep** | 15487 | same id; talent, also a 3 s lockout on Forever |
| PRIEST | 605 | Mind Control | DISCIPLINE, HOLY_PRIEST, SHADOW | Mind Control | **keep** | 605 | same id; add ranks 10911, 10912 |
| PRIEST | 8122 | Psychic Scream | DISCIPLINE, HOLY_PRIEST, SHADOW | Psychic Scream | **keep** | 8122 | same id; add ranks 8124, 10888, 10890 |
| PRIEST | 64044 | Psychic Horror | DISCIPLINE, SHADOW | (absent) | **drop** | - | absent |
| PRIEST | 88625 | Holy Word: Chastise | HOLY_PRIEST | (absent) | **drop** | - | absent |
| ROGUE | 1766 | Kick | ASSASSINATION, OUTLAW, SUBTLETY | Kick | **keep** | 1766 | same id; add ranks 1767-1769 |
| ROGUE | 408 | Kidney Shot | ASSASSINATION, OUTLAW, SUBTLETY | Kidney Shot | **keep** | 408 | same id; add rank 8643 |
| ROGUE | 1833 | Cheap Shot | ASSASSINATION, OUTLAW, SUBTLETY | Cheap Shot | **keep** | 1833 | same id; no cooldown |
| ROGUE | 2094 | Blind | ASSASSINATION, OUTLAW, SUBTLETY | Blind | **keep** | 2094 | same id; 300 s |
| SHAMAN | 57994 | Wind Shear | ELEMENTAL, ENHANCEMENT, RESTORATION_SHAMAN | (absent) | **replace** | 8042 to 10414 (7 ranks) | Earth Shock |
| SHAMAN | 192058 | Capacitor Totem | ELEMENTAL, ENHANCEMENT, RESTORATION_SHAMAN | (absent) | **drop** | - | absent |
| SHAMAN | 51490 | Thunderstorm | ELEMENTAL, RESTORATION_SHAMAN | (absent) | **drop** | - | absent |
| SHAMAN | 51514 | Hex | ELEMENTAL, ENHANCEMENT, RESTORATION_SHAMAN | (absent) | **drop** | - | absent |
| WARLOCK | 19647 | Spell Lock | AFFLICTION, DEMONOLOGY, DESTRUCTION | Spell Lock | **keep** | 19647 | same id, it is rank 2; add rank 1 19244 |
| WARLOCK | 30283 | Shadowfury | AFFLICTION, DEMONOLOGY, DESTRUCTION | (absent) | **drop** | - | absent |
| WARLOCK | 6789 | Mortal Coil | AFFLICTION, DEMONOLOGY, DESTRUCTION | Death Coil | **keep** | 6789 | same id, now named Death Coil; add ranks 17925, 17926 |
| WARLOCK | 5782 | Fear | AFFLICTION, DEMONOLOGY, DESTRUCTION | Fear | **keep** | 5782 | same id; add ranks 6213, 6215 |
| WARLOCK | 5484 | Howl of Terror | AFFLICTION, DEMONOLOGY, DESTRUCTION | Howl of Terror | **keep** | 5484 | same id; add rank 17928 |
| WARLOCK | 89766 | Axe Toss | DEMONOLOGY | (absent) | **drop** | - | absent; Felguard Intercept 427745 is NeverLearned |
| WARRIOR | 6552 | Pummel | ARMS, FURY, PROTECTION_WARRIOR | Pummel | **keep** | 6552 | same id; add rank 6554; pair with Shield Bash 72/1671/1672 |
| WARRIOR | 107570 | Storm Bolt | ARMS, FURY, PROTECTION_WARRIOR | (absent) | **replace** | 12809 | Concussion Blow, the warrior talent stun; Protection tree, but any warrior can take it |
| WARRIOR | 5246 | Intimidating Shout | ARMS, FURY, PROTECTION_WARRIOR | Intimidating Shout | **keep** | 5246 | same id; single rank |
| WARRIOR | 386071 | Disrupting Shout | PROTECTION_WARRIOR | (absent) | **drop** | - | absent; no AoE interrupt |
| WARRIOR | 46968 | Shockwave | PROTECTION_WARRIOR | (absent) | **drop** | - | absent; Shockwave 440488 is NeverLearned, rune-only |
| WARRIOR | 23920 | Spell Reflection | PROTECTION_WARRIOR | Spell Reflection | **drop** | - | id exists with no skill line, talent or teacher |
| RACE | 20549 | War Stomp | Tauren | War Stomp | **keep** | 20549 | same id; Tauren |
| RACE | 255654 | Bull Rush | HighmountainTauren | (absent) | **drop** | - | absent |
| RACE | 107079 | Quaking Palm | Pandaren | (absent) | **drop** | - | absent |
| RACE | 287712 | Haymaker | KulTiran | (absent) | **drop** | - | absent |
| RACE | 260364 | Arcane Pulse | Nightborne | (absent) | **drop** | - | absent |

## 10. In-game probes

Each is a read-only line to paste on Forever.

- **P1 spec and class:** `/dump C_SpecializationInfo.GetSpecializationInfo(1), C_SpecializationInfo.GetAllClassIDs(), GetNumClasses(), GetNumSpecializationsForClassID`
  Run it below level 10 too, to see whether the spec is nil before talents.
- **P2 replaced ranks:** on a Rogue of 26+ or a Warrior of 32+ (Kick 1766/1767, or 72/1671):
  `/dump C_SpellBook.IsSpellKnown(1766), C_SpellBook.IsSpellInSpellBook(1766,0,false), C_SpellBook.IsSpellKnown(1767), C_Spell.GetBaseSpell(1767), C_Spell.GetOverrideSpell(1766)`
- **P3 kept ranks:** the same five reads with 8042 and 8044 on a Shaman of 8+. Then cast the top rank and
  `/dump C_Spell.GetSpellCooldown(8042).isActive`. Repeat with `ShowAllSpellRanks` on and off.
- **P4 shared cooldown:** Shield Bash, then at once `/dump C_Spell.GetSpellCooldown(6552).isActive` (Warrior 38+).
- **P5 GCD sentinel and fallbacks:** `/dump C_Spell.GetSpellCooldown(61304), GetCVarBool("loadDeprecationFallbacks"), IsPlayerSpell, IsSpellKnown`
- **P6 effect checks:** Silence on a casting mob (does the cast stop, is the school locked 3 s); Feral Charge from Cat Form.
- **P7 pet bank:** with a Felhunter out and dismissed:
  `/dump C_SpellBook.IsSpellInSpellBook(19244,1,false), C_SpellBook.IsSpellKnown(19244,1), C_Spell.GetSpellCooldown(19244)`
- **P8 runes:** `/dump C_Engraving, C_SpellBook.IsSpellKnown(425609)` on a Paladin.

## 11. Owner decisions

1. One list per class (recommended: it matches the one spec id Forever reports and the storage shape) or one per talent tree
   (needs a tree-derived key and a rule for hybrids and ties; it buys only a different order, mainly Protection warrior).
2. How wide the defaults are: core only, or with the optional column (recommended: core, plus Gouge and Intercept).
