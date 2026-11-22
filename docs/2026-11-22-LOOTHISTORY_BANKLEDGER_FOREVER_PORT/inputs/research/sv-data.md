# SavedVariables evidence for the LootHistory + BankLedger Forever port

Read-only sampling, 2026-11-21. Paths abbreviated:
- `RSV` = `/mnt/g/Games/Blizzard/World of Warcraft/_retail_/WTF/Account/ADD1KTED2KA0S/SavedVariables`
- `FACC` = `/mnt/g/Games/Blizzard/World of Warcraft/_forever_/WTF/Account/ADD1KTED2KA0S`
- `FBS` = `FACC/SavedVariables/BagSync.lua` (646 lines, 12 KB, written 2026-11-20 22:32)
- `BSA` = `/mnt/g/Games/Blizzard/World of Warcraft/_forever_/Interface/AddOns/BagSync` (v20.41)
- `FUI` = the Forever UI sparse checkout (`.../scratchpad/ui/forever/Interface/AddOns`)
- `GIT` = `/mnt/d/Profile/Users/Tushar/Documents/GIT`

Helper scripts (scratch only): `.../scratchpad/research/sv/shape.lua`, `dig.lua`, `dig2.lua`; outputs `lh-dig.txt`, `lh-dig2.txt`.

---

## 1. Forever WTF layout (VERIFIED)

- `_forever_/WTF/Account/` holds `ADD1KTED2KA0S/` and an account-less `SavedVariables/` (Blizzard files only).
- Realm folder is the number **`91`**, not a realm name: `FACC/91/`. Character folders are
  **`Bursar-Dinwiddie`, `Sacrilege-Nightbane`, `Traxex-Silentshot`**, i.e. "First-Surname" with a hyphen.
  The client's GetRealmName answers **"CAMWOW AU1 Realm 2 PvP"** (FBS:185, `realmKey` FBS:293) and the normalized form is
  **"CAMWOWAU1Realm2PvP"** (`rwsKey` FBS:298).
- `FACC/character-list-order.txt` lists GUID-ish rows `6801-000C920A`, `6801-000C9309`, `6801-002B61BE` (realm id 6801),
  plus `6797-0008E5B1` (a fourth character on realm 6797 with no WTF folder).
- **Neither LootHistory nor BankLedger has ever run on Forever**: no `LootHistory.lua`/`BankLedger.lua` in
  `FACC/SavedVariables` or in any `FACC/91/*/SavedVariables`, and `grep -i 'loothistory|bankledger' FACC/91/*/AddOns.txt` is empty.
- Ka0s addons WITH Forever account SVs: AbsorbTracker, AuraMaster, CastTrail, CombatTrail, ConsumableMaster, DropWatcher,
  LibKa0sSkinTester, OutfitterReborn, PanelMaster, PartyFrameEnhanced, PrettyChat, QuestTrail, QuickComms, RangeMaster,
  SkillMaster (directory listing of `FACC/SavedVariables`).

### Character / realm key forms seen on Forever (VERIFIED, by grep)
| Source | Key form |
|---|---|
| AceDB profileKeys (AuraMaster, DropWatcher, SkillMaster, CombatTrail, ... all Ka0s) | `"Traxex Silentshot"` — no realm suffix |
| BagSync | realm `"CAMWOW AU1 Realm 2 PvP"` → char `"Traxex Silentshot"` (FBS:185-186) |
| DropWatcher data | `"Traxex Silentshot"` (440 hits) and other players `"First Last"` |
| CombatTrail / EllesmereUI `realm` field | `"PvP"` (the ruleset) |
| Auctionator (UnitName + normalized realm) | `"Traxex-CAMWOWAU1Realm2PvP"` — **first name only** |
| AddonProfiler / AtlasLoot | `"Traxex-CAMWOW AU1 Realm 2 PvP"`, `"Bursar - CAMWOW AU1 Realm 2 PvP"` |

Source of the AceDB form: `GIT/AuraMaster/libs/AceDB-3.0/AceDB-3.0.lua:277-281` (regional names → `name .. " " .. surname`,
realmKey = ruleset). LibKa0s mirrors it: `GIT/LibKa0s/LibKa0s/Compat.lua:384-447` (`lib.RegionalNames`,
`lib.UnitCharacterName`, `lib.CharacterKey`, ruling cited as forever-quirks §4).

**Port impact (VERIFIED in code):** both addons build the char key from `UnitName("player") .. "-" .. normalizedRealm`:
`GIT/LootHistory/core/Util.lua:6-12` (`Util.PlayerKey`), `GIT/BankLedger/core/Compat.lua:36-42` (`Compat.PlayerName`).
On Forever UnitName's second return is the surname, so these would yield `"Traxex-CAMWOWAU1Realm2PvP"` (INFERRED from the
Auctionator row and LibKa0s Compat.lua:417-418) — Bursar Dinwiddie and a hypothetical "Bursar Other" would collide.
LootHistory also qualifies other names with the realm: `Util.QualifyName` (Util.lua:366-372),
`Compat.TradeTargetKey` (LootHistory/core/Compat.lua:1047-1055), `Compat.LatestCurrencyTransfer` (Compat.lua:1062-1070).

---

## 2. BankLedger — Retail SV (`RSV/BankLedger.lua`, 4,118 lines, 109 KB) (VERIFIED)

Shape (AceDB):
```
BankLedgerDB = {
  global = { ledger = { <row>, ... 253 rows }, skinNotice = 1, schemaVersion = 6 },   -- :3-4, :4034
  profileKeys = { ["Helyâ - Frostmourne"] = "Default", ... 17 chars },                -- :4036
  profiles = { Default = { savedViews = {Insights, History}, settings = {appearance, sessionWindow, window},
                           blacklist = { [6948]=true, [241325]=true } } } }            -- :4055-4112
```
Row (BankLedger.lua:5-17 MONEY, :45-61 ITEM, :260-276 GUILD_BANK):
`ts, zone, subzone, mapID, char="Name-Realm", classFile, direction=DEPOSIT|WITHDRAW, kind=MONEY|ITEM,
store=BANK|WARBAND_BANK|GUILD_BANK, quantity` (copper for MONEY), `itemName` ("Gold" for money); ITEM rows add
`itemID, itemLink, quality, itemType, itemSubType`; GUILD_BANK rows add `guild="Misguided"`.
- Counts: store WARBAND_BANK 229, BANK 21, GUILD_BANK 3; kind ITEM 147 / MONEY 106; DEPOSIT 142 / WITHDRAW 111.
- `char` values all `-Frostmourne` (10 chars). No reagent-bank store, no client field, no realm-per-row field
  beyond the char key.
- **Warband is 90% of the data.** On Forever the account bank is locked (see §4), so WARBAND_BANK rows would never be written.
- Store containers are derived by Enum.BagIndex member name: `GIT/BankLedger/core/Constants.lua:104-124`
  (`BANK = ^Bank$, ^BankBag_%d+$, ^CharacterBankTab_%d+$`; `WARBAND_BANK = ^AccountBankTab_%d+$`).

## 3. LootHistory — Retail SV (`RSV/LootHistory.lua`, 95,167 lines, 2.3 MB) (VERIFIED)

TOC: `## SavedVariables: LootHistoryDB, LootHistoryPerfDB` (`GIT/LootHistory/LootHistory.toc:7`).
```
LootHistoryDB.global = {
  schemaVersion = 15 (:8), ledgerSince, rollupSeeded, boundRepairRevision = 4, skinNotice, debug, __lhNoScrollFix, __lhSkipCapture,
  holdings = { [<PlayerKey>|"§warband"] = {...} }   -- :9, §warband at :1516 (13 holders)
  history  = { <row> x 3265 }                         -- :5486, ts 1792604259 .. 1795188423
  daily    = { ["YYYY-MM-DD"] = { [<holder>] = { ["i:<itemID>"|"c:<currencyID>"|"g"...] = {c=,i=,o=} } } }  -- :80324, 37 days
}
LootHistoryPerfDB = { schema = 2, runs = { {addon, buckets, context{character="Sacrìlege", realm="Frostmourne", ...},
                      fps, interface = 120100, version = "1.4.0", ...} } }    -- :95117
```
- **holdings[<holder>]** = `items[itemID] = {bags=,bank=,equipped=,mail=,auctions=,tabs=}`, `links[itemID] = itemLink`,
  `currency[currencyID] = n`, `money` (copper), `meta = {genesis, completeAt, lastSeen, partial, classFile}`,
  `scanned = {bags, bank, equipped, mail, auctions, currency, money, tabs}` (timestamps), `escrow = {exits, mailMoney, mailOwn}`
  (Aellâ, :5235). Slot keys used across all holders: bank 434, bags 233, equipped 223, tabs 121, mail 15, auctions 3.
  `tabs` appears only under `§warband` (warband bank); there is **no reagent or keyring slot key**.
- **§warband holder** (`C.WARBAND_HOLDER = "§warband"`, `GIT/LootHistory/core/Constants.lua:107`): items/links/currency
  (currency 2032 = 3860), money 12,599,924,285, scanned = {money, currency, tabs}.
- **history row** fields: `ts, char, holder, classFile, kind=ITEM|GOLD|CURRENCY` (159 legacy rows have no kind),
  `dir=IN|OUT|MOVE, source, confidence=CERTAIN|INFERRED, zone, subzone, mapID, quantity, itemName, itemType, itemSubType,
  itemID, itemLink, quality, itemLevel, vendorPrice, bound=BOP|BOE|WARBAND|WARBAND_UE, claimed, currencyID,
  from/to="<holder>/<container>"` (containers: bags, bank, equipped, money, tabs, auctions), `pairId, auctionPrice.auctionator.minbuyout,
  sourceDetail = {npcID, encounterID, difficulty, keystoneLevel, questID}`.
- **source** counts: OTHER 831, CONSUME 498, WARBAND_DEPOSIT 242, WARBAND_WITHDRAW 200, TRANSFER 178, KILL 172,
  DISENCHANT 169, CONTAINER 156, MPLUS 145, SELL 104, REPAIR 104, DECONSTRUCT 101, AH 81, UNTRACKED 75, QUEST 67, BUY 34,
  AH_BUY 30, CRAFT 25, BONUS_ROLL 23, VENDOR 15, MAIL 4, GUILD_DEPOSIT 3, DESTROY 3, AH_SOLD 3, AH_POST_FEE 2.
  Retail-only on Forever (INFERRED, content-era): WARBAND_*, MPLUS/keystoneLevel, BONUS_ROLL, DECONSTRUCT, bound WARBAND*,
  difficulty 16/208/250 (Mythic/Delves).
- Holder keys: all `Name-Frostmourne` with accented names (`Aellâ-Frostmourne`, 1132 rows) plus `§warband` 273 rows.

### Item link format (VERIFIED, both clients)
- Retail: `|cnIQ4:|Hitem:243605::::::::90:66::::1:38:13:::::|h[Dawn Crystal |A:Professions-ChatIcon-Quality-12-Tier1:17:15::1|a]|h|r`
  (BankLedger.lua:52). Crafted-quality atlases are embedded in the name; some links carry `Player-3725-...` crafter GUIDs.
- **Forever uses the same `|cnIQn:` colour tag** (DropWatcher.lua 154/154, ConsumableMaster.lua 498 links, OutfitterReborn 37).
  Sample: `|cnIQ1:|Hitem:16072::::::::30:1485::14:::::::|h[Expert Cookbook]|h|r` — level 30, specID field **1485/1486**
  (Forever spec ids, vs Retail 66/253/267). No bonus-id-heavy links seen in the sample. INFERRED: a parser that reads
  itemID from `Hitem:(%d+)` and quality from `cnIQ(%d)` works unchanged.

---

## 4. BagSync on Forever — the closest thing to probe data

Top level (FBS): `warband§ = {money = 0}` (:3-4), `options§` (:6, addonversion 20.41 :57), `blacklist§`, `whitelist§`,
`savedsearch§`, `forceDBReset§ = 3` (:645), and one realm table `["CAMWOW AU1 Realm 2 PvP"]` (:185) holding three chars and
one guild: **Traxex Silentshot** (:186, Hunter, guid Player-6801-000C920A :189, guild "Warcraft Forever©", money 254084 :324),
**Sacrilege Nightbane** (:536, Paladin, Player-6801-000C9309, money 0), **Bursar Dinwiddie** (:578, Paladin,
Player-6801-002B61BE, money 6724 :626), guild **"Warcraft Forever©" = { tabs = {} }** (:574-575, never scanned / empty).

### Bag and bank ids (VERIFIED in data + code)
- Forever Enum.BagIndex (`FUI/Blizzard_APIDocumentationGenerated/BagIndexConstantsDocumentation.lua:25-50`):
  Accountbanktab -3, Characterbanktab -2, Keyring -1, Backpack 0, Bag_1..4 = 1..4, ReagentBag 5,
  **CharacterBankTab_1..9 = 6..14**, **AccountBankTab_1..9 = 15..23**. Retail (`.../ui/retail/.../BagIndexConstantsDocumentation.lua:25-44`):
  CharacterBankTab_1..6 = 6..11, AccountBankTab_1..5 = 12..16. **No `Bank` (-1) or `BankBag_N` member on either.**
- Traxex `bag`: keys -1, 0, 1..5 (FBS:261, :281). `[-1]` = Keyring with 2 items (6893, 277507). `[1]` = 10 stacks of
  3033 (arrows: a quiver/ammo bag). `[5]` = ReagentBag container present but empty; equipbags.bag has `"254035;1;bagslot=5"`
  (:294) — BagSync only scans slot 5 when `IsReagentBagActive` (`BSA/wireframe/scanner.lua:316-317`;
  `BSA/core.lua:182` = `NumReagentBagSlots > 0`), so **the reagent bag slot is live on Forever** (INFERRED from data + code).
- Character bank: Traxex `bank = { [6] = {24 entries} }` (:210-235); Bursar `bank = { [6] = {} }` (:589-591); Sacrilege no bank key.
  BagSync writes `bagDB[bagid]` only when `GetContainerNumSlots(bagid) > 0` (`BSA/wireframe/scanner.lua:259-270`) and stores
  occupied slots only (:273-276). So: **CharacterBankTab_1 (id 6) is the base bank and has slots; tabs 7..14 reported 0 slots**
  (no bank bags owned). 24 occupied stacks fits the vanilla 24-slot base bank (INFERRED; exact slot count not stored).
- Bank bags: Forever puts real bags into bank-tab slots 2..N of the `Characterbanktab` (-2) inventory
  (`BSA/core.lua:179-180`, `BSA/wireframe/scanner.lua:362-385`, `FUI/Blizzard_UIPanels_Game/Camelot/BankFrame.lua:87,186,315,323`:
  container id = `CharacterBankTab_1 + bagSlotID - 1`; gated by `C_Bank.ShouldUsePlayerBagsInBank()`).
  Traxex `equipbags.bank = {}` (:296-297): no bank bags slotted yet.
- Reagent bank: BagSync's `tracking.reagents = false`, `void = false` (:175-176) — user setting, so no evidence either way.
  Forever enum has no Reagentbank member (enum listing above).
- **Warband/account bank: locked on Forever.** `warband§` holds only `money = 0` and no `tabs` (:3-4). BagSync: "WoW Forever has
  the whole account bank API but it's locked, Blizzard only shows it when CanViewBank(Account) is true" (`BSA/core.lua:185-213`);
  `SaveWarbandBank` returns early unless `isWarbandActive` (`BSA/wireframe/scanner.lua:747-751`). So the API surface exists but
  no tabs were ever scanned (INFERRED: CanViewBank(Account) false and FetchNumPurchasedBankTabs(Account) 0 on this account).
- Bank open timing: "scan on open and again on close, the bank isn't always loaded yet when it first opens (WoW Forever)"
  (`BSA/wireframe/events.lua:300`); "bank tab sockets (WoW Forever) ... can change without a BAG_UPDATE" (:315);
  "on Forever this fires when a bag is put in or taken out of a bank tab" (:372). Scanner keeps old data when tabs report 0 slots
  ("TabsNotReady", `BSA/wireframe/scanner.lua:466-481`) and bails when `C_Bank.CanViewBank(Character)` is false (:443-449).
- Detection: `WOW_PROJECT_ID == WOW_PROJECT_CAMELOT` or `== 18` (`BSA/core.lua:31-46`); Forever is treated as the retail API
  (`BSA/core.lua:48-49`); "WoW Forever (16001) runs the 12.x API without the deprecation fallbacks, so the old globals are nil"
  (`BSA/core.lua:134`).
- Naming: BagSync migrated from first-name-only keys because alts with the same first name overwrote each other
  (`BSA/wireframe/data.lua:326-341`, `BSA/wireframe/unit.lua:114-130`) — direct precedent for §1's port impact.
  "GetPlayerInfoByGUID() doesn't include the surname" on Forever (`BSA/wireframe/data.lua:1424`).
- Currency on Forever (Traxex): 1792 Honor Points 71, 3402 Merchant's Favor 80. Auctions exist (4 posted). Mailbox keys exist.

## 5. Port-relevant conclusions

1. Both addons already derive container ids by Enum.BagIndex member name (BankLedger Constants.lua:104-124,
   LootHistory Constants.lua:294-320), so Forever's 9 character tabs (6..14) and shifted AccountBankTab ids (15..23) resolve
   without numeric edits. The `^Bank$`/`^BankBag_` patterns match nothing on either client.
2. The character key is the real break: switch to LibKa0s `CharacterKey()`/`UnitCharacterName()` semantics on Forever
   ("Traxex Silentshot", realm = ruleset or omitted), and decide the holder-key form (e.g. `"Traxex Silentshot"` vs
   `"Traxex Silentshot-PvP"`). Existing Retail data needs no migration (no Forever data exists for either addon).
3. Warband bank / WARBAND_* sources / bound WARBAND are dead on Forever for this account; the API exists but is locked.
4. The guild bank is real on Forever (BagSync models it; guild "Warcraft Forever©") but has no scanned tabs, so it is untested.
5. Forever bank opening is lazy (tabs may report 0 slots on BANKFRAME_OPENED) and bank bags live in -2 slots 2..9 —
   relevant to any snapshot-diff ledger.
6. Keyring (-1) holds items on Forever; neither addon's BAGS pattern (`^Backpack$, ^Bag_%d+$, ^ReagentBag$`) includes Keyring.
