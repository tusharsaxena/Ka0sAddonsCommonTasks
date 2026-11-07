# The Forever name and realm probe (2026-11-08)

The owner ran this probe in game on WoW Forever (1.60.1, build 70790), as character Traxex Silentshot. It answers
the open probe that `W1_DEFAULT_SKIN_AND_FOREVER_NAMES.md` §2 left. The standard records the result as
client-quirks-§5's Forever entry (v2.104.0).

## Output, verbatim

```
Dump: value=UnitName("player")            [1]="Traxex", [2]="Silentshot"
Dump: value=UnitFullName("player")        [1]="Traxex", [2]="Silentshot"
Dump: value=GetUnitName("player", true)   [1]="Traxex Silentshot"
Dump: value=GetRealmName()                [1]="CAMWOW AU1 Realm 2 PvP"
Dump: value=GetNormalizedRealmName()      [1]="CAMWOWAU1Realm2PvP"
char=[Traxex Silentshot] realm=[PvP] factionrealm=[Alliance - PvP]          (AceDB-3.0 40's db.keys)

Dump: value=UnitName("target")            [1]="Ryz", [2]="Rockheart"
Dump: value=UnitFullName("target")        [1]="Ryz", [2]="Rockheart"
Dump: value=GetUnitName("target", true)   [1]="Ryz Rockheart"
Dump: value=Ambiguate(GetUnitName("target", true), "short")   [1]="Ryz Rockheart"

CHAT_MSG_SAY sender=[Doom Dock] arg5=[Doom Dock]
```

The owner: "Chat with someone from another realm is not possible in Forever i think", and "This [the AceDB keys] is
key i feel - we can use this char and realm combo on forever".

## What it means

- **`UnitName` and `UnitFullName` put the surname where Retail puts the realm.** Code that reads the second return
  as a realm builds `First-Surname`. Code that reads one value keeps only the first name, and two characters who
  share a first name collide.
- **The whole name is `GetUnitName(unit, true)`.** A chat sender carries the whole name and no realm.
- **AceDB 40 already does what the owner asked for**, without asking which client it is on. When
  `RegionalUniqueNamesEnabled()` is true, the character key is `UnitNameUnmodified("player")`'s name and surname
  joined, and the realm key is the ruleset from `C_GameRules` (`Hardcore`, `RP-PvP`, `RP`, `PvP`, `PvE`). The
  standard adopts that identity: `db.keys.char` and `db.keys.realm`, or the same derivation inside the compat family.

## Call sites to fix at each port

This is a grep of the pending addons' own `.lua` (outside `libs/` and `tests/`), for review at port time. It is
not a full audit.

**Second return read as a realm (wrong on Forever):**
- DropWatcher `core/Compat.lua:883` (`UnitName("NPC")`), `modules/Roster.lua:97`
- LootHistory `core/Compat.lua:980` (`UnitName("NPC")`)
- OutfitterReborn `modules/Triggers_Params.lua:321`
- QuickComms `core/Compat.lua:133`, `:148` (`UnitFullName("player")`)

**One value as the identity, so the first name only (collides on Forever):**
- BankLedger `core/Compat.lua:37-39` and LootHistory `core/Util.lua:7-9`, the character key (`Name-Realm`). Both
  should move to the AceDB keys.
- DropWatcher `modules/CharFilter.lua:196`, `LootFeed.lua:194`, `LootParser.lua:188`, `TestMode.lua:110`, through
  `Compat.UnitName`
- MultiMeters `core/Compat.lua:760` (`Compat.UnitName`), `modules/Roster.lua:234`, `Sim.lua:201`
- QuickComms `core/Compat.lua:248`, `:255`; DpsRace `modules/Share.lua:179`; KickCD `core/Compat.lua:531`

**Display only (shows the first name; needs width for the pair):**
- PartyFrameEnhanced `modules/TargetFrames.lua:82`, `:227`, `UnitButtons.lua:133`, `PetFrames.lua:91`, `StandIn.lua:247`
- KickCD `modules/Castbar_Debug.lua:70`; LibKa0s `Perf.lua:439-440` (the perf report's character and realm)

**A library helper, recommended for the first name-keyed port.** Most of these addons already route the call
through their own `core/Compat.lua`, so the natural fix is in LibKa0s Compat: `UnitFullName(unit)` and
`CharacterKey()` / `RealmKey()`, mirroring AceDB 40's derivation and gated on `RegionalUniqueNamesEnabled`. Each
port then adopts it. It is not built yet, because wave 1 has no consumer.
