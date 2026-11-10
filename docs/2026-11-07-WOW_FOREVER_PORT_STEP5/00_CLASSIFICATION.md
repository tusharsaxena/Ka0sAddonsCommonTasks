# WoW Forever port, step 5: difficulty classification

Step 5 of the WoW Forever port (`../2026-11-07-WOW_FOREVER_PORT/`) ports the roster addons one at a time.
This file ranks all 17 roster addons by how much a port changes and how much is unknown, so the waves can run
in order. The owner approved it on 2026-11-07 ("this looks fine").

**Scope note.** The roster is `../../../WowAddonStandards/standards/ADDONS.md`. This file names addons only
to classify them; it is not a copy of the roster.

## How it was measured (2026-11-07)

- **The missing-globals scan, forced to Forever.** The kit's `tests/_kit/client_globals.lua` scanner (kit revision
  53) was run against every addon with the `forever` set, read-only, from a scratch script. Every addon is clean in
  shipping code. The only hits are `loadfile`/`dofile` in `tools/` (OutfitterReborn, QuickComms), which never ship.
  No addon is held back by a missing API, so what ranks them is behavior and data.
- **Counts of risky references** in each addon's shipping code (`libs/`, `tests/`, `tools/` left out): specs, the
  group finder and M+, the bank, the Encounter Journal and transmog, loot, `GetFrameStrata`, Edit Mode, chat sends,
  Blizzard frames, `C_DamageMeter`, `C_CooldownViewer`, equipment, talents, and Delves, Garrison and Housing.
- **Seed data**, at the owner's request a difficulty factor of its own: clients-§5 needs a Forever list wherever an
  addon ships a Retail list of spells, items, zones, instances or spec IDs, never a filtered Retail one.
- **Blizzard's Forever UI source** (Gethe/wow-ui-source, branch `forever`), for what loads there:
  `Blizzard_GroupFinder` carries `ExcludeLoadGameType: camelot`; `Blizzard_EncounterJournal` is
  `AllowLoadGameType: standard, classic`; `Blizzard_DamageMeter` and `Blizzard_CooldownViewer` are
  `standard, camelot`; `Blizzard_AuraContainer` and `Blizzard_CompactRaidFrames` carry no game-type gate.
- The research report, `../2026-11-07-WOW_FOREVER_PORT/reports/WoW Forever porting research.md`.

## 1. Will not port to Forever

| Addon | Reason |
|---|---|
| WhatGroup | Retail-only by the owner's ruling of 2026-11-07. It reads `C_LFGList` applications and search results, and Forever does not load Retail's group finder. Already carries the load-gating lines. |
| PremadeGroupsFilterExtension | Same ruling and cause. It extends `LFGListFrame`/`PVEFrame`, which do not exist on Forever. Its `defaults/Realms.lua` seed and M+ filters are Retail-only. Already load-gated. |
| DpsRace | Retail-only by the owner's ruling of 2026-11-10: "there are no training dummies in forever so this makes no sense". It races against a training dummy, and Forever has none. Gets the load-gating lines (`DpsRace` and `WowAddonStandards` commits `QFE-DPS`, Ka0sAddonsCommonTasks `docs/2026-11-10-QUICKCOMMS_FOREVER_EMOTES/`). Before the ruling it was in group 4: The meter engine ports. The seeds do not: the dummy catalog (Retail creature IDs, by rule only measured in game, so the owner captures Forever's), the hearthstone list from Retail DB2 exports, the spec references and the secret spec icon. |

## 2. No changes except the TOC

| Addon | Reason |
|---|---|
| AbsorbTracker | It sums absorb shields into one bar. No spec IDs, no seed data, no Blizzard frame hooks; absorbs and secret values behave the same on both clients. The Ace3 fix it needed shipped in steps 1–4. |
| LibKa0sSkinTester | A showroom for the LibKa0s skins, built on LibKa0s widgets only. No game data and no Blizzard systems. Never on CurseForge, so it owes no packaging test. |

## 3. Minimal changes

| Addon | Reason |
|---|---|
| PanelMaster | Four `GetFrameStrata` calls. On Forever a strata read off a Blizzard frame can be secret (`Enum.SecretAspect.FrameStrata`), so those sites need a guard. No seed data. |
| PrettyChat | It rewrites chat format strings through `_G[GLOBALNAME]`. Its seed list (`defaults/Defaults.lua`) is Retail's, and some strings (Warband, crafting orders, Delves) do not exist on Forever: a Forever list, or tolerance for a missing string, plus an in-game pass over the loot and currency lines. |
| PartyFrameEnhanced | It already supports both the compact party frames and the classic `PartyFrame` (`modules/Providers.lua`), and `Blizzard_CompactRaidFrames` loads on Forever. Open: its Edit Mode hooks against Forever's extra Edit Mode systems, and Forever's redrawn unit frames. Mostly smoke, with small fixes. |

## 4. Medium changes

| Addon | Reason |
|---|---|
| MultiMeters | `C_DamageMeter` loads on Forever, so the core works. About 50 `specIconID` reads, which Forever makes secret, each need a guard; the Delve content type is gated off; the chat reports need a check. |
| QuickComms | The engine is client-neutral. The seeds are all Retail: the M+ builtin, the battleground and arena builtins, and `defaults/GameIds_Instances.lua` (derived from Retail's Encounter Journal). Forever needs its own instance, battleground and arena lists, and the M+ builtin gated off. Also 2 strata reads and 28 spec references. |
| KickCD | `C_CooldownViewer` and `C_Spell` cooldowns exist on Forever, but `defaults/Spells.lua` is keyed by Retail spec IDs (Forever's differ: Warrior 1491), and the spells differ. A Forever interrupt list per class and spec, and a per-class check of the Cooldown Manager. |

## 5. High changes

| Addon | Reason |
|---|---|
| ConsumableMaster | The whole seed set is Midnight consumables (flasks and phials, food, potions, augment runes, Vantus runes, weapon enchants); Forever has none of them. The stat-priority seed is keyed by Retail spec IDs and Retail's stats, and Forever's character sheet shows hit and defense, which suggests an older stat set. Seeds and the ranking model both need rework. |
| AuraMaster | The engine ports (`Blizzard_AuraContainer` loads on Forever). The data does not: `defaults/CastToAura.lua` (generated from Retail build 12.1.0), `defaults/Categories.lua` and `settings/GeneralSpells.lua` are Retail spell IDs per class and spec. Forever's ids differ and its API suggests spell ranks are back. The spell-research tool needs a Forever data source, which is not confirmed to exist. |
| DropWatcher | The most problems at once: a Retail 12.x spec table (246 spec references), the Encounter Journal (36, not loaded on Forever), transmog (off on Forever), the group finder (26), Delves (14), and undocumented Forever loot rules. The largest of these addons, about 43k lines. |
| LootHistory | It records loot and tracks holdings across the bank: 76 bank references, the Warband bank among them, plus the group finder. Forever has no working Warband bank and a different bank layout. `C_LootHistory` under Forever's loot rules, and one two-value `UnitName` call (the second value is a surname on Forever). |
| BankLedger | The whole addon is the bank (51 bank-API references), where Forever differs most: no Warband bank, no `Enum.BagIndex.Bank`, and Forever-only `C_Bank` calls that hint at older bank bags. The model is rebuilt per client, and the layout is only known in game. |
| OutfitterReborn | Built on Forever's redrawn character frame (71 frame references). `EquipmentManager_UnpackLocation` is gone, `C_EquipmentSet` is unverified, transmog is off, talents and specs differ, and `defaults/Zones.lua` is Retail battleground and arena maps. One two-value `UnitName` call and one strata read. |

## Order

**Amended 2026-11-10:** DpsRace left group 4 for section 1 (Retail-only) by the owner's ruling; group 4 is now MultiMeters, QuickComms and KickCD.

Port in group order: group 2 first, then group 3, group 4 and group 5. In group 5, ConsumableMaster and AuraMaster
are mostly a seed-data question, so the first thing to settle there is whether Forever data exports exist.

The CurseForge packaging question (does CurseForge's own packager tag a `120105, 16001` file for both Retail and
Forever?) is settled by one alpha tag of a ported CurseForge addon. Group 2's AbsorbTracker is the candidate; the
Skin Tester is never published. The tag waits for the owner's go-ahead.
