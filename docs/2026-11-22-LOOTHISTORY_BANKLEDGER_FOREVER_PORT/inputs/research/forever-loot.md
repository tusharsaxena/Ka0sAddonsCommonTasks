# How loot works on WoW Forever (1.60.1, interface 16001) vs Retail 12.1.5

Research for the LootHistory + BankLedger Forever port. 2026-11-21. Read-only; no repo touched.

Tags: **VERIFIED** = read in source/docs at the cited line. **INFERRED** = my reading, needs an in-game probe.

## Paths

- `F/` = Blizzard UI, branch `forever` 1.60.1 (71037), `.../scratchpad/ui/forever/Interface/AddOns/`
- `R/` = Blizzard UI, live 12.1.5, `.../scratchpad/ui/retail/Interface/AddOns/`
- `D/` = `Blizzard_APIDocumentationGenerated/` under F or R
- `K/` = Ketho/BlizzardInterfaceResources `forever` and `live` branches (fetched 2026-11-21), `.../scratchpad/research/ketho/{gs,fn,ev}_{forever,live}.lua`
  (gs = GlobalStrings enUS, fn = GlobalAPI, ev = Events)
- `RLF/` = `/mnt/g/Games/Blizzard/World of Warcraft/_forever_/Interface/AddOns/RPGLootFeed/` (v1.39.2, Interface 11509,16001,...,120105, `RPGLootFeed.toc:1,4`)
- Derived diffs: `.../scratchpad/research/apidiff-loot.txt` (doc diff), `ketho-diff-loot.txt` (fn/ev diff), `gsdiff-loot.txt` (strings diff)
- Prior art inside the collection: `../DropWatcher/docs/superpowers/research/2026-11-13-forever-port/01_FOREVER_LOOT_RULES.md` (DW research, build 70888) and `../DropWatcher/docs/forever-quirks.md:174-205`. Everything below was re-checked on 71037; it agrees with DW.

## 0. Short version

1. **Forever runs the Mainline (Retail) loot UI and API.** Camelot is a game type inside the `mainline` family. VERIFIED by TOC pattern: `F/Blizzard_UIPanels_Game/Blizzard_UIPanels_Game.toc:140` `[Family]\BankFrame.xml [AllowLoadGameType mainline] [ExcludeLoadGameType camelot]` (an exclude only makes sense if mainline includes camelot); same pattern `F/Blizzard_FrameXML/Blizzard_FrameXML.toc:131-132`. Camelot and `standard` (Retail) are siblings: `F/Blizzard_Collections/Blizzard_Collections.toc:41` `[AllowLoadGameType camelot, standard]`.
2. **The loot API surface is the same set on both clients.** Ketho fn/ev diff over Loot/Roll/Currency/Transmog/LFG/Encounter/Instance/Merchant/Mail/Trade/Quest/Money/Bank: only 22 Forever-only and 2 Live-only names, none of them a loot read (`ketho-diff-loot.txt`). Doc diff: `apidiff-loot.txt`, 46 lines, same conclusion. VERIFIED.
3. **Every personal-acquisition chat string LootHistory parses is byte-identical** (36/36 keys `LOOT_ITEM*`, `CURRENCY_GAINED*`, `YOU_LOOT_MONEY*`, `LOOT_MONEY*`, `LOOT_CURRENCY_REFUND`, `CREATED_ITEM*`, `ERR_QUEST_REWARD_*`, `ERR_AUCTION_SOLD_S/WON_S`). VERIFIED (`gsdiff.py --all`, all SAME).
4. **What does differ:** the `C_LootHistory` drop key name (`lootListKey` vs `lootListID`), the group-roll chat lines (Forever prefixes every one with `|HlootHistory:%d|h[Loot]|h: `), names (two-word "First Last", no realm), and missing Blizzard UIs (Encounter Journal, Retail Group Finder/LFD, Trading Post). Details below.
5. **API presence is not content.** The generated docs and Ketho's dump carry Azerite, Garrison, ChallengeMode, Bonus Roll, warband currency transfer etc. on Forever (`F/D/LootDocumentation.lua:39-89` AZERITE_EMPOWERED_ITEM_LOOTED, BONUS_ROLL_*, GARRISON_MISSION_BONUS_ROLL_LOOT). The engine exports them; whether the server ever fires them is INFERRED-no for most. Feature-detect, then expect silence.

## 1. C_LootHistory (Forever vs Retail)

- Same 5 functions, 5 events, 1 enum, 4 structs on both. Only difference: the drop identifier is named **`lootListKey`** on Forever, **`lootListID`** on Retail. VERIFIED: `F/D/LootHistoryDocumentation.lua:66` (GetSortedInfoForDrop arg 2), `:102` (LOOT_HISTORY_ONE_HUNDRED_ROLL payload), `:113` (LOOT_HISTORY_UPDATE_DROP payload), `:151` (EncounterLootDropInfo field); Retail `R/D/LootHistoryDocumentation.lua` same lines say `lootListID`.
- Functions: `GetAllEncounterInfos` `:11`, `GetInfoForEncounter(encounterID)` `:20`, `GetLootHistoryTime` `:35`, `GetSortedDropsForEncounter(encounterID)` `:44`, `GetSortedInfoForDrop(encounterID, lootListKey)` `:59`. Events `LOOT_HISTORY_CLEAR_HISTORY` `:81`, `_GO_TO_ENCOUNTER` `:87`, `_ONE_HUNDRED_ROLL` `:97`, `_UPDATE_DROP` `:108`, `_UPDATE_ENCOUNTER` `:119`. VERIFIED.
- `EncounterLootDropRollState`: NeedMainSpec 0, NeedOffSpec 1, Transmog 2, Greed 3, NoRoll 4, Pass 5 (`:138-143`). `EncounterLootDropInfo` fields `:151-160` (itemHyperlink, playerRollState, currentLeader, isTied, winner, allPassed, rollInfos, startTime, duration); `EncounterLootDropRollInfo` `:168-174` (playerName, playerGUID, playerClass, isSelf, state, isWinner, roll). VERIFIED.
- Classic-shape events (`LOOT_HISTORY_ROLL_CHANGED`, `LOOT_HISTORY_ROLL_COMPLETE`, `LOOT_HISTORY_AUTO_SHOW`) are **absent** on Forever (`K/ev_forever.lua` no hit). VERIFIED.
- Blizzard's own frame is the Mainline one: `F/Blizzard_FrameXML/Blizzard_FrameXML.toc:125-127` loads `[Family]\LootHistory.lua/.xml` plus `[Game]\LootHistory.lua [AllowLoadGameType camelot]`, whose whole body is `ShouldAutoOpen() return false` (`F/Blizzard_FrameXML/Camelot/LootHistory.lua:2-4`). The Mainline frame reads the drop key positionally from the event and from `elementData.lootListKey` (`F/Blizzard_FrameXML/Mainline/LootHistory.lua:19-21, 382, 546`). VERIFIED.
- **Rule:** never read the field by name alone; take it positionally from the event, or `drop.lootListID or drop.lootListKey`. RLF does exactly this (`RLF/Features/LootRolls/LootRolls.lua:273-274`); DropWatcher records it as an own quirk (`../DropWatcher/docs/forever-quirks.md:205`).

## 2. Group loot rolls

- Events present on Forever: `START_LOOT_ROLL`, `LOOT_ROLLS_COMPLETE`, `CANCEL_LOOT_ROLL`, `CANCEL_ALL_LOOT_ROLLS`, `MAIN_SPEC_NEED_ROLL`, `LOOT_ITEM_ROLL_WON`, `CONFIRM_LOOT_ROLL`, `CONFIRM_DISENCHANT_ROLL` (`K/ev_forever.lua:1271, 1257, 1260, 1254`; `F/D/LootDocumentation.lua:91-128, 204-216`). VERIFIED.
- Legacy globals present (undocumented in the generated docs, listed by Ketho): `GetLootRollItemInfo` (`K/fn_forever.lua:5569`), `GetLootRollItemLink` `:5570`, `RollOnLoot` `:6395`, `GetActiveLootRollIDs` `:5276`, plus `C_Loot.GetLootRollDuration` (`F/D/LootDocumentation.lua:11`). VERIFIED.
- Roll frame: Mainline `GroupLootFrame` loads on Forever (`F/Blizzard_UIPanels_Game/Blizzard_UIPanels_Game.toc:129-130`, `[AllowLoadGameType mainline]`, no camelot exclude). It reads `texture, name, count, quality, bindOnPickUp, canNeed, canGreed, canDisenchant, reasonNeed, reasonGreed, reasonDisenchant, deSkillRequired, canTransmog = GetLootRollItemInfo(rollID)` (`F/Blizzard_UIPanels_Game/Mainline/GroupLootFrame.lua:317`) and rolls 0 pass / 1 need / 2 greed / 4 transmog (`:1274-1291`). Same file as Retail. VERIFIED.
- Disenchant: no DE button in this frame on either client; `LOOT_ROLL_ROLLED_DE` strings still exist. Transmog rolls: Forever has `LOOT_ROLL_ROLLED_TRANSMOG` which Live lacks (`K/gs_forever.lua:13932`), so INFERRED the server can offer Transmog. Owner (per DW) sees Need/Greed in practice.

## 3. Loot method / master loot

- Legacy global `GetLootMethod` is **gone on both** (`K/fn_forever.lua` no hit); use `C_PartyInfo.GetLootMethod()` → `method, masterLootPartyID?, masterLooterRaidID?` (`F/D/PartyInfoDocumentation.lua:287-296`, `K/fn_forever.lua:3084`). `Blizzard_DeprecatedPartyInfo` has no shim for it (its TOC loads only `Deprecated_PartyInfo.lua`). VERIFIED.
- `Enum.LootMethod`: Freeforall 0, Roundrobin 1, Masterlooter 2, Group 3, Needbeforegreed 4, Personal 5 (`F/D/LootConstantsDocumentation.lua:13-18`). VERIFIED.
- Master loot threshold differs: Forever `LootConsts_Camelot.MasterLootQualityThreshold = 4` (`F/D/LootConstants_MainlineDocumentation.lua:39-43`); Retail `LootConsts.MasterLootQualityThreshold = 5` (`R/D/LootConstantsDocumentation.lua:47-54`). `IsMasterLooter`, `GetMasterLootCandidate` present (`K/fn_forever.lua:6109, 5587`). VERIFIED.
- `LOOT_MASTER_LOOTER`: Forever "Loot: Master Loot" (`K/gs_forever.lua:13889`) vs Live "Loot: Guild Master Loot". VERIFIED.
- Personal loot: enum value exists; DW's owner ruling (2026-11-13) is that Forever groups use Group/FFA/Master only. INFERRED from source, OWNER in DW.

## 4. Chat: CHAT_MSG_LOOT / CURRENCY / MONEY

- `CHAT_MSG_LOOT` payload is identical on both (diffed the event block of `D/ChatInfoDocumentation.lua`; Forever `:1816`, Retail `:1789`). `text`, `playerName`, `playerName2`, `guid` are not `NeverSecret`. `CHAT_MSG_CURRENCY` F`:1513`, `CHAT_MSG_MONEY` F`:1843`. VERIFIED.
- Self lines identical (VERIFIED, Forever / Live line): `LOOT_ITEM_SELF` "You receive loot: %s" 13877/13383; `_MULTIPLE` "%sx%d" 13878/13384; `LOOT_ITEM_PUSHED_SELF` "You receive item: %s" 13873/13379; `LOOT_ITEM_CREATED_SELF` 13868/13374; `LOOT_ITEM_BONUS_ROLL_SELF` 13866; `LOOT_ITEM_REFUND` 13875/13381; `LOOT_CURRENCY_REFUND` 13849; `CURRENCY_GAINED` "You receive currency: %s" 5563/5436 (+ `_MULTIPLE`, `_BONUS`, `_OVERFLOW` 5564-5566); `YOU_LOOT_MONEY` "You loot %s" 25923/24710 (+ `_GUILD`, `_MOD`); `LOOT_MONEY_SPLIT` "Your share of the loot is %s." 13893/13399; `LOOT_ITEM` "%s receives loot: %s." 13863/13369; `LOOT_ITEM_WHILE_PLAYER_INELIGIBLE` 13879.
- Group-roll lines differ (all VERIFIED, `gsdiff-loot.txt`): on Forever `LOOT_ROLL_NEED/GREED/PASSED/ROLLED_NEED/ROLLED_GREED/WON/YOU_WON` carry a leading `|HlootHistory:%d|h[Loot]|h: ` (e.g. `K/gs_forever.lua:13920, 13910, 13923, 13930, 13929, 13934, 13940`); on Live the other-player ones have no prefix, and the `_SELF` ones have the prefix **plus** a trailing `[View Loot Rolls]` link that Forever lacks (Live `:13417, 13427, 13432`). Consequence: a pattern built from the client's own GlobalString at runtime still matches, but capture positions shift by one on Forever. Any `msg:match("HlootHistory:")` filter (RLF does this, `RLF/Features/ItemLoot/ItemLoot.lua:659`) drops roll lines; `LOOT_ITEM_SELF` lines carry no such link, so a self-loot parser is unaffected.
- `CHAT_MSG_COLLECTED_APPEARANCE` exists on Forever only (`F/D/ChatInfoDocumentation.lua:1348-1374`, `K/ev_forever.lua:322`), wired into chat config (`F/Blizzard_ChatFrame/Mainline/ChatConfigFrame.lua:312`). VERIFIED.

## 5. Names (biggest risk for a self-loot parser)

- Forever names are "First Last", unique per region; `UnitName(unit)` returns **name, surname** (not realm); chat sender arg 2 is `"First Last"` with no realm. VERIFIED in Blizzard source: `F/Blizzard_FrameXMLUtil/Camelot/NameUtil.lua:4-12` (`local name, surname = UnitName(unit)`), loaded instead of the shared NameUtil (`F/Blizzard_FrameXMLUtil/Blizzard_FrameXMLUtil.toc:58-59`). Measured by owner probe 2026-11-08 (standard `forever-quirks-§4`, vendored in `../DropWatcher/docs/forever-quirks.md:124-150`).
- RLF matches self as `sender == UnitName("player") or playerName2 == GetUnitName("player", false)`, then GUID fallback (`RLF/Features/ItemLoot/ItemLoot.lua:666-673`), and drops `UnitName`'s second return on Forever (`RLF/Features/PartyLoot/PartyLoot.lua:70-74`).
- **LootHistory hits (for the port, VERIFIED):** `../LootHistory/core/Util.lua:7` builds `PlayerKey` from one-value `UnitName("player")` + `GetNormalizedRealmName()` → first name + "CAMWOWAU1Realm2PvP" (collides for two chars sharing a first name; not AceDB's key). `../LootHistory/core/Compat.lua:1050` `local name, realm = UnitName("NPC")` → on Forever builds "First-Surname". Both need `LibKa0s-Compat-1.0` `CharacterKey()` / `UnitCharacterName()` per forever-quirks-§4.

## 6. Loot window, ENCOUNTER_LOOT_RECEIVED, toasts

- Mainline `LootFrame` loads ungated (`F/Blizzard_UIPanels_Game/Blizzard_UIPanels_Game.toc:127-128`). `LOOT_READY`, `LOOT_OPENED(autoLoot)`, `LOOT_CLOSED`, `LOOT_SLOT_CLEARED`, `LOOT_BIND_CONFIRM`, `ITEM_PUSH` present (`F/D/LootDocumentation.lua:156-224`; `K/ev_forever.lua:1252-1259, 1249`). `GetNumLootItems`, `GetLootSlotInfo`, `GetLootSlotLink`, `GetLootSlotType`, `GetLootSourceInfo`, `GetLootInfo`, `LootSlot` present (`K/fn_forever.lua:5672, 5572-5575, 5568, 6220`). `Enum.LootSlotType` None/Item/Money/Currency (`F/D/LootConstantsDocumentation.lua:40-45`). VERIFIED.
- Forever-only: `C_LootFrame.TryAutoLoot`, `C_AutoLoot.SetUseAutoLootToggle`, `UnitHasLootInteraction` (`K/fn_forever.lua:2810, 432, 6707`). VERIFIED.
- `ENCOUNTER_LOOT_RECEIVED(encounterID, itemID, itemLink, quantity, itemName, fileName)` identical (`F/D/LootDocumentation.lua:130-141`, `K/ev_forever.lua:1247`). `ENCOUNTER_START/END` present (`K/ev_forever.lua:665-666`). VERIFIED. Fires on Forever: INFERRED yes (Mainline boss banner loads there, `RLF/BlizzOverrides/BossBanner.lua:12-13`).
- `SHOW_LOOT_TOAST`, `QUEST_LOOT_RECEIVED`, `LFG_COMPLETION_REWARD`, `BONUS_ROLL_RESULT` all registered events on Forever (`K/ev_forever.lua:1266, 1265, 1167, 1241`); whether the server fires bonus rolls: INFERRED no (no vanilla-era bonus-roll coins).

## 7. Other acquisition sources

- **Trade:** `TRADE_ACCEPT_UPDATE`, `TRADE_CLOSED`, `UI_INFO_MESSAGE` present (`K/ev_forever.lua:1869, 1870, 1835`); `GetTradePlayerItemInfo/Link`, `GetTradeTargetItemInfo/Link`, `GetPlayerTradeMoney`, `GetTargetTradeMoney` (`K/fn_forever.lua:5935-5938, 5746, 5916`); TradeFrame loads ungated (`Blizzard_UIPanels_Game.toc:116-117`); `TradeInfoDocumentation.lua` identical. VERIFIED.
- **Mail:** `GetInboxHeaderInfo`, `GetInboxItem`, `GetInboxItemLink`, `TakeInboxItem`, `TakeInboxMoney` (`K/fn_forever.lua:5485-5488, 6608-6609`); `MAIL_INBOX_UPDATE`, `MAIL_SUCCESS` (`K/ev_forever.lua:1300, 1306`). Forever adds `C_Mail.IsCODEnabled` and `MAIL_OPEN_ALL_CANCELED` (`F/D/MailInfoDocumentation.lua:51-59, 125-130`). Blizzard_MailFrame is its own addon on Forever (the FrameXML copy is classic-only, `Blizzard_UIPanels_Game.toc:207-208`). VERIFIED.
- **Vendor:** MerchantFrame Mainline loads (`Blizzard_UIPanels_Game.toc:110,113`); `MerchantFrameDocumentation.lua` identical; `BuyMerchantItem`, `GetMerchantItemLink`, `GetBuybackItemInfo` present (`K/fn_forever.lua:76, 5605, 5330`); legacy `GetMerchantItemInfo` absent on Forever (use `C_MerchantFrame`). VERIFIED.
- **Quest rewards:** `GetQuestItemInfo/Link`, `GetQuestLogRewardInfo`, `GetNumQuestRewards`, `GetRewardMoney`, `C_QuestLog.GetQuestRewardCurrencyInfo` present (`K/fn_forever.lua:5769, 5771, 5786, 5686, 5835, 3575`); `QUEST_TURNED_IN` (`K/ev_forever.lua:1580`); `ERR_QUEST_REWARD_MONEY_S` "Received %s." (`K/gs_forever.lua:8945`). VERIFIED.
- **Currency:** `C_CurrencyInfo` doc file identical to Retail (diff -q), incl. `GetCurrencyInfo`, `GetCurrencyInfoFromLink`, `GetCurrencyListInfo`, `ExpandCurrencyList`, `FetchCurrencyTransferTransactions` (`F/D/CurrencyInfoDocumentation.lua:79, 265`). Forever ships its own Currency tab (`F/Blizzard_TokenUI/Blizzard_TokenUI.toc:4-7`, Mainline excluded, Camelot loaded) that uses `C_CurrencyInfo.GetCurrencyListSize/GetCurrencyListInfo/ExpandCurrencyList` and account-transferable currency (`F/Blizzard_TokenUI/Camelot/Blizzard_TokenUI.lua:23, 204, 353-354, 376-383`); `Blizzard_CurrencyTransfer.lua` loads too (`toc:2-3`). RLF: "Forever reports expansion 0 but ships the Mainline currency system (C_CurrencyInfo + CURRENCY_DISPLAY_UPDATE with quantityChange)" (`RLF/Features/Currency/Currency.lua:275-283`). VERIFIED (source), real currencies existing: INFERRED few/none (`RLF/GameTesting/TestMode.lua:116` "TODO: Add WoW Forever test currencies once any exist").
- **Money:** `GetMoney`, `PLAYER_MONEY`, `CHAT_MSG_MONEY` present (`K/fn_forever.lua:5616`, `K/ev_forever.lua:596, 340`). VERIFIED.
- **Item / ilvl:** `C_Item.GetItemInfo`, `C_Item.GetDetailedItemLevelInfo`, `C_Item.GetItemInfoInstant` present (`K/fn_forever.lua:2528, 2511`; `F/D/ItemDocumentation.lua:354`). Global `GetItemInfo` / `GetDetailedItemLevelInfo` absent on Forever (as on Retail). `ItemDocumentation` differs only by Forever-only `C_Item.DeleteItem`, `ConfirmDeleteItem`, `GetWeaponEnchantInfo`. VERIFIED.
- **Transmog:** Collections + Wardrobe load on Forever (`F/Blizzard_Collections/Blizzard_Collections.toc:40-42`); `C_TransmogCollection.PlayerHasTransmogByItemInfo`, `GetItemInfo`, `PlayerHasTransmog`, `GetSourceInfo` present (`K/fn_forever.lua:4579, 4551, 4578, 4558`; `F/D/TransmogItemsDocumentation.lua:908`); `TRANSMOG_COLLECTION_SOURCE_ADDED` (`K/ev_forever.lua:1926`; RLF registers it, `RLF/Features/Transmog/Transmog.lua:126`). VERIFIED.
- **Bank:** Forever-only `C_Bank.FetchMaxNumBankTabs`, `ShouldUsePlayerBagsInBank`, `BankBagTypeAndIDToInvSlot`, `ReagentsFromBankAllowed` (`ketho-diff-loot.txt`); Forever has its own BankFrame (`Blizzard_UIPanels_Game.toc:138, 141`). Relevant to BankLedger; not loot. VERIFIED.

## 8. Group finder, instance, encounter journal

- **Retail Group Finder / Dungeon Finder UI is not loaded on Forever:** `F/Blizzard_GroupFinder/Blizzard_GroupFinder.toc:10` `## ExcludeLoadGameType: camelot`. Forever loads the Vanilla-style premade finder (`F/Blizzard_GroupFinder_VanillaStyle/Blizzard_GroupFinder_VanillaStyle.toc:5` `AllowLoadGameType: classic, camelot`) when `C_LFGList.GetPremadeGroupFinderStyle() == Enum.PremadeGroupFinderStyle.Vanilla` (`F/Blizzard_LFGUtil/Camelot/LFGUtil.lua:1-14`). `C_LFGList`, `C_LFGInfo`, `GetLFGDungeonInfo` exist (`K/fn_forever.lua:2698, 2731, 2669, 5527`); Forever adds `C_LFGListRoles` and `LFG_LIST_SHOW_SEARCH`/`LFG_LIST_ROLE_UPDATE`. VERIFIED. No LFD random-dungeon queue on Forever: INFERRED (UI absent).
- **Instance:** `GetInstanceInfo` returns the same 11 values (`InstanceDocumentation.lua` identical; `F/D/InstanceDocumentation.lua:103-119`, incl. `difficultyID`, `instanceID`, `lfgDungeonID?`). `DifficultyUtil.ID` is the Mainline table on Forever (`F/Blizzard_FrameXMLUtil/Blizzard_FrameXMLUtil.toc:33-36`; `Mainline/DifficultyUtil_Base.lua:3-25`: DungeonNormal 1, DungeonHeroic 2, Raid40 9, RaidClassic20Normal 242, RaidClassic10Normal 243, RaidWorld 250 ...). Forever's difficulty tooltip maps by maxPlayers 5/10/20/40 and uses DungeonNormal for dungeons (`F/Blizzard_FrameXML/Camelot/InstanceDifficultyOverrides.lua:1-23`). Which IDs the server actually reports (1? 9? 242/243?): INFERRED, **needs a probe**.
- **Encounter Journal UI not loaded on Forever:** `F/Blizzard_EncounterJournal/Blizzard_EncounterJournal.toc:7` `## AllowLoadGameType: standard, classic` (camelot not listed). The API exists (`EJ_GetEncounterInfo`, `EJ_GetInstanceInfo`, `EJ_SelectInstance` `K/fn_forever.lua:5195, 5199, 5219`; `C_EncounterJournal.*` doc identical). A third-party `ForeverDungeonJournal` addon is installed, consistent with no Blizzard EJ. VERIFIED (TOC); EJ data populated for vanilla content: INFERRED doubtful, needs probe.
- `GetExpansionLevel()` reports 0 on Forever (`RLF/BlizzOverrides/BossBanner.lua:12`, `RLF/Features/Currency/Currency.lua:275`). REPORTED by RLF.

## 9. RPGLootFeed's Forever handling (summary)

- Detection: `IsForever = WOW_PROJECT_CAMELOT ~= nil and WOW_PROJECT_ID == WOW_PROJECT_CAMELOT`; `IsRetail` returns true on Forever too (`RLF/utils/AddonMethods.lua:49-51, 82-84`); prefers capability checks (`HasModernLootHistoryAPI`, `:53-62`). Blizzard confirms `WOW_PROJECT_CAMELOT = 18` (`F/Blizzard_ProjectConstants/Camelot/ProjectConstants.lua:1-2`).
- Treats Forever as Mainline except: `lootListKey` fallback (`LootRolls.lua:273-274`); two-word sender names (`ItemLoot.lua:666-673`, `PartyLoot.lua:70-74, 254-257`); currency forced on despite expansion 0 and chat currency events off (`Currency.lua:275-283`); Trading Post off (`:285-288`); Traveler's Log off (`TravelPoints.lua:24-26`); Forever-only test items (`TestMode.lua:84-86`); auto-open suppression respects Camelot `ShouldAutoOpen` (`BlizzOverrides/LootHistory.lua:13-24`).

## 10. Open probes (owner, in game)

1. `C_LootHistory.GetSortedDropsForEncounter` on a real Forever group roll: confirm `lootListKey` field and that `LOOT_HISTORY_UPDATE_DROP` fires.
2. `GetInstanceInfo()` difficultyID in a 5-man dungeon and a 40-man raid.
3. One `CHAT_MSG_LOOT` self line: print `text, playerName, playerName2, guid` (sender form, secrecy in an instance).
4. `C_CurrencyInfo.GetCurrencyListSize()` on a level-cap char: any currencies at all?
5. Does `ENCOUNTER_LOOT_RECEIVED` fire on a dungeon boss kill?
6. `EJ_GetInstanceInfo` / `C_EncounterJournal` answers anything for a vanilla instance?
