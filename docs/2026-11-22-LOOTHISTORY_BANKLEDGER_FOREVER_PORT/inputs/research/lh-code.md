# LootHistory — Forever port code map

Repo: /mnt/d/Profile/Users/Tushar/Documents/GIT/LootHistory (branch master, clean, v1.5.0, LibKa0s v1.109.0).
Forever source: scratchpad/ui/forever (1.60.1 71037). Retail docs: scratchpad/ui/retail (12.1.5).
VERIFIED = read in source (file:line given). INFERRED = reasoning or third-party evidence, not proven.

Method: the Forever and Retail `Blizzard_APIDocumentationGenerated` trees were loaded into Lua and dumped to
`research/api-forever.tsv` / `research/api-retail.tsv` (functions, events, enums, structs; dumper
`scratchpad/lhscripts/dumpdocs.lua`). Every LH reference (`research/lh-refs.tsv`, extractor
`scratchpad/lhscripts/extract.py`, over the 63 non-lib TOC files in `research/lh-files.txt`) was checked
against those dumps and, for undocumented globals, grep over the checked-out Forever FrameXML.

## 0. Headline findings

1. **Every C_* function, Enum and event LH uses is documented on Forever.** No API is missing outright (§2).
   The engine is the modern one, and Forever loads modern AH (`Blizzard_AuctionHouseUI` with `[Game]` Camelot
   override, toc:9,15), modern Professions (`Blizzard_Professions.toc` Camelot lines), a Camelot TokenUI
   with account-wide/transferable currencies (`Blizzard_TokenUI/Camelot/Blizzard_TokenUI.lua:75-80`) and the
   currency-transfer UI (`Blizzard_TokenUI.toc:2-3`, loaded unconditionally). VERIFIED.
2. **Forever HAS a warband (account) bank with tabs and warband gold.** `Blizzard_UIPanels_Game/Camelot/BankFrame.lua:26-31,133,288-298,316-327`,
   `Camelot/BankFrame.xml:49-52` (4 account-tab icons), `Blizzard_MoneyFrame/Shared/MoneyFrame.lua:60`
   (`C_Bank.FetchDepositedMoney(Enum.BankType.Account)`). VERIFIED. So LH's `§warband` holder is NOT
   meaningless on Forever. Whether a given account has the tab purchased is runtime (Camelot BankFrame.lua:44
   hides purchase when Account has 0 tabs; INFERRED: account tabs may be unobtainable/unpurchased on Forever).
3. **Enum.BagIndex is renumbered on Forever.** Forever: CharacterBankTab_1..9 = 6..14, AccountBankTab_1..9 = 15..23;
   Retail: CharacterBankTab_1..6 = 6..11, AccountBankTab_1..5 = 12..16 (both from the API dumps, VERIFIED).
   Keyring = -1 exists in both enums and is LIVE on Forever (`Blizzard_FrameXMLBase/Constants.lua:166`,
   `Blizzard_MainMenuBarBagButtons/Camelot/MainMenuBarBagButtons.lua:51,58`). LH derives ids by member name
   (`core/Constants.lua:294-320`) so the renumbering is absorbed (VERIFIED), but **Keyring is not in any group**
   (`core/Constants.lua:298-300`), so keys on the keyring are invisible to Holdings and a key moved bag<->keyring
   reads as a loss/gain (INFERRED). The test mock pins the Retail numbers (`tests/wow_mock.lua:61-72`).
4. **Character names on Forever carry a surname, and `UnitName`'s 2nd return is the SURNAME, not the realm.**
   `Blizzard_FrameXMLUtil/Camelot/NameUtil.lua:4-12,14-21,35-46` (`local name, surname = UnitName(unit)`, joined
   with `Constants.CharacterNameSeparatorConsts.CHARACTERNAME_SURNAME_SEPARATOR`, a space per
   `Blizzard_ChatFrameBase/Shared/SlashCommands.lua:1163-1165`). API docs still label it `unitServer`
   (`UnitDocumentation.lua` UnitName returns) — the docs are shared and misleading. `C_PlayerInfo.ShouldDisplaySurname`
   and `C_NameUtil.ReplaceSurnameSeparatorWithLinkSeparator` are Forever-only (absent from the Retail dump). VERIFIED.
   BagSync, running on Forever, keys characters by full name via `GetUnitName("player", false)` and migrates its
   old first-name keys (`_forever_/Interface/AddOns/BagSync/wireframe/unit.lua:116-134`, `wireframe/data.lua:257-259,328-340,1424-1425`). INFERRED corroboration.
   Impact on LH (VERIFIED code, INFERRED effect):
   - `Util.PlayerKey` (`core/Util.lua:6-12`) uses only the first name: two Forever characters sharing a first
     name on one realm collide in `char`, `holdings`, `daily`.
   - `Compat.TradeTargetKey` (`core/Compat.lua:1048-1057`) reads `name, realm = UnitName("NPC")` — on Forever
     `realm` is the partner's surname, producing `"First-Surname"` keys.
   - `Util.QualifyName` (`core/Util.lua:367-372`) strips all whitespace (`gsub("%s+","")`), which glues a
     typed `"First Surname"` mail recipient into `"FirstSurname-Realm"` (own-alt MOVE detection at
     `modules/AttributionOut.lua:70,112` then misses).
   - `Compat.LatestCurrencyTransfer` (`core/Compat.lua:1060-1072`) appends realm to `destinationCharacterName`;
     whether that field carries the surname is unknown (INFERRED: probe).
   - `SimDrivers` parses the name with `^([^%-]+)` (`modules/SimDrivers.lua:49`) — fine, but a full-name key with
     a space breaks nothing there.
5. **Mythic+ is dead on Forever.** `Blizzard_ChallengesUI.toc` `## AllowLoadGameType: standard, mists` excludes
   camelot (VERIFIED). `C_ChallengeMode` and the CHALLENGE_MODE_* events are still documented, so the code is
   harmless (presence-gated, `core/Compat.lua:29-34`), just inert (INFERRED).
6. **Gate: green on both profiles, but the Forever profile proves little.** 2054/0/1 retail, 2054/0/1 forever,
   luacheck 0/0 (§4). LH has zero `WOW_PROJECT_*` / `GetBuildInfo` reads in shipped code (grep of core/ modules/
   settings/ defaults/ returned nothing; `core/Compat.lua:5-7` declares it Retail-only), and the kit's forever
   profile only changes the project constants, build info and five absent globals (`tests/_kit/mock_client.lua:18-29`).
7. **TOC carries `## Interface: 120105` only** (`LootHistory.toc:1`); `docs/ARCHITECTURE.md:576` says
   `forever-quirks.md` is not applicable while Clients is `Retail (port pending)` — both must change in the port.

## 1. Module list (TOC order; roles from docs/module-map.md role table, VERIFIED)

core/
- Compat.lua — the compat firewall; every client read the simulator answers; presence-gated, no flavor branch (`core/Compat.lua:5-7`).
- SimSeam.lua — LibKa0s-Sim answer seam; wraps every NS.Compat member at load (TOC LOAD-BEARING).
- EnvSetup.lua — LibKa0s-Env seam: NS.Meta/Version/Zone/PlayerMapID (C_AddOns.GetAddOnMetadata at `core/EnvSetup.lua:64-65`).
- ItemSetup.lua — LibKa0s-Item seam: link parsing, QualityLabel/QualityFromLink, ITEM_QUALITY_COLORS read lazily (`core/ItemSetup.lua:70-72`).
- MediaSetup.lua — LibKa0s-Media seam (icons, mono font, LSM).
- Constants.lua — SourceType/Confidence enums, bag-id groups from Enum.BagIndex (`:294-320`), equip slots (`:323`), CURRENCY_SOURCE_REASON (`:344-353`), layers.
- Namespace.lua / State.lua — bootstrap; runtime contexts (lootContext, encounter, keystone, scopes).
- Util.lua — PlayerKey (`:6-12`), money formatting via GetCoinTextureString (`:66-75`), loot-line patterns from LOOT_ITEM_* globals (`:155-230`), QualifyName (`:367-372`).
- Ledger.lua — pure ledger primitives (ThingKey, Diff, PickReason).
- CoreSetup.lua — LibKa0s-Core: printer, SafeRegisterEvent, class colors (`:71`).
- SkinSetup.lua — LibKa0s-Skin owner seam.
- Dispatch.lua — NS.EVENT_ROWS / NS.HOOK_ROWS, NS.DeliverAll (`:40,47`).
- LifecycleSetup.lua — the disable latch. PerfSetup.lua — LibKa0s-Perf. WidgetsSetup / DebugLogSetup / PoolSetup — library seams.
- LootHistory.lua — AceAddon, OnInitialize/OnEnable, PLAYER_ENTERING_WORLD prune.
- Database.lua — AceDB init, 15-step migration ladder (`:16-423`), Add/Delete/Purge/Stats/Export.
- LauncherSetup.lua — minimap + LDB launcher, key-binding button.
defaults/Global.lua (account-wide), defaults/Profile.lua (every setting).
modules/
- Attribution.lua — source engine: LOOT_OPENED GUID decode, encounter/keystone/trade/quest/spell stamps; 9 bus rows + 1 spell row + 5 hooks (`:419-444`).
- AttributionOut.lua — loss-side reasons: 13 hooks + 6 rows (`:146-177`), guild bank HookScript.
- Collector.lua — CHAT_MSG_LOOT/CURRENCY/MONEY capture (`:340-342`), writes records (`:184,246`).
- Filters.lua — black/whitelist. Scanner.lua — stateless container/equipped/currency/money reads.
- Holdings.lua — db.global.holdings store (`:30,123` container gates). Rollup.lua — daily rollup.
- Reconciler.lua — ledger scan/plan/commit; READABLE_ON (`:54-59`); 14 ledger rows (`:695-703`); BAG_UPDATE routing by group (`:95-100`).
- Escrow.lua — mail + owned-auction escrow steps. AuctionPrice.lua — third-party price readers (Auctionator/TSM/Oribos…).
- LedgerFormat / BrowserWidgets / Browser / BrowserViews / BrowserFilterBar / BrowserTable / BrowserTableGroup / BrowserTableTestData — the History window (shift-click ChatEdit_InsertLink `BrowserTable.lua:591-592,1016`; class icons CLASS_ICON_TCOORDS `:154`; atlases `:76-78,151`).
- Export.lua — export modal. Analytics / AnalyticsFormat / AnalyticsCharts / AnalyticsLedger — Insights tab (byKeystone breakdown `core/Database.lua:856,1005`).
- HoldingsTab.lua (Forget popup `:291-296`), TimelineModel.lua, Timeline.lua — ledger tabs.
- TestData.lua; SimWorld / SimDrivers / SimScenario / Sim / SimPanel — the in-game simulator (6 scenarios incl. `key`, `bank`, `ah`).
- Diagnostics.lua — diagnostics sections (lists the LOOT_ITEM_* globals `:55-57`).
settings/ OptionsSetup, Schema (32 rows), Slash, Panel, PanelAuction, Profiles.

## 2. WoW API / global / Enum / event inventory, classified

Legend: E = exists-on-Forever (documented in Forever API dump or used by Forever FrameXML), D = differs-on-Forever,
M = missing-on-Forever, ? = undocumented on both; presence assumed (INFERRED).

### 2a. C_* namespaces (all documented in BOTH dumps — VERIFIED)
| API | Where (file:line) | Class | Note |
|---|---|---|---|
| C_Timer.After / NewTimer | core/LootHistory, Reconciler deferrals (15 + 4 sites) | E | |
| C_Item.GetItemInfo | core/Compat.lua:235,398-400,371,570-585,599 (13 sites) | E | 14th return Enum.ItemBind; same enum both clients |
| C_Item.GetItemInfoInstant | core/Compat.lua:230,393,593,942 | E | classID 2/4/0 identical in Forever Enum.ItemClass |
| C_Item.GetDetailedItemLevelInfo | core/Compat.lua:406,597 | E | vanilla ilvls small, works |
| C_Item.RequestLoadItemDataByID | settings/Panel filters | E | |
| C_Item.GetItemID | core/Compat.lua:1017-1020 | E | |
| C_CurrencyInfo.GetCurrencyInfo / FromLink / ListSize / ListInfo / ListLink / ExpandCurrencyList | core/Compat.lua:428-565,886-923 | E | Camelot TokenUI shows isAccountWide/isAccountTransferable (TokenUI/Camelot:75-80) |
| C_CurrencyInfo.FetchCurrencyTransferTransactions | core/Compat.lua:1061 | E | CurrencyTransfer UI loads on Forever (TokenUI.toc:2-3); payload field names unverified on both |
| C_Container.GetContainerItemInfo / GetContainerNumSlots / ContainerIDToInventoryID / UseContainerItem | core/Compat.lua:117-133,821-834,857-860 | E | Forever's own UI uses them (Camelot/BankFrame.lua:102, MainMenuBarBagButtons Camelot:51) |
| C_Bank.FetchDepositedMoney | core/Compat.lua:843-849 | E | used by Forever MoneyFrame.lua:60 |
| C_TooltipInfo.GetHyperlink | core/Compat.lua:308-310 | E | |
| C_Map.GetBestMapForUnit | core/Compat.lua:85-91 | E | vanilla map ids |
| C_Spell.GetSpellName / GetSpellInfo | via LibKa0s-Compat (core/Compat.lua:169-170) | E | |
| C_ChallengeMode.GetActiveKeystoneInfo | core/Compat.lua:29-34 | E (inert) | Challenges UI not loaded on camelot (Blizzard_ChallengesUI.toc AllowLoadGameType standard, mists) |
| C_AuctionHouse.GetNumOwnedAuctions / GetOwnedAuctionInfo | core/Compat.lua:1003-1015 | E | Enum.AuctionStatus Active=0 same |
| C_AuctionHouse.PostItem / PostCommodity / PlaceBid / ConfirmCommoditiesPurchase (hooks) | modules/AttributionOut.lua:158-162 | E | modern AH loads for camelot (AuctionHouseUI.toc:15) |
| C_TradeSkillUI.CraftRecipe / CraftSalvage / CraftEnchant (hooks) | modules/AttributionOut.lua:163-166 | E | Salvage/Enchant likely never fire (no salvage/enchant-recipe content; INFERRED) |
| C_Texture.GetAtlasInfo | modules/BrowserTable.lua:76-78,151; modules/AnalyticsFormat.lua:86-88 | E | atlas names themselves unverified on Forever (guarded) |
| C_AddOns.GetAddOnMetadata | core/EnvSetup.lua:64-65 | E | |
| C_EventUtils.IsEventValid | via LibKa0s Core SafeRegisterEvent | E | |
| C_LootHistory, C_LFGList, C_TransmogCollection | — | n/a | **not used by LH** (grep of core/ modules/ empty) |

### 2b. Enums
| Enum | Where | Class | Note |
|---|---|---|---|
| Enum.BagIndex | core/Constants.lua:304 | **D** | renumbered (Forever 9+9 tabs, ids 6..23; Retail 6+5, ids 6..16); Keyring -1 live on Forever and not grouped |
| Enum.BankType.Account | core/Compat.lua:846 | E | Character=0 Guild=1 Account=2 both |
| Enum.PlayerInteractionType (Banker, AccountBanker, MailInfo, Auctioneer, …) | core/Compat.lua:862-866; modules/Reconciler.lua:54-59 | E | same values; Forever adds PetUntrainer=80 |
| Enum.AuctionStatus.Active | core/Compat.lua:1008 | E | |
| Enum.ItemBind (via BIND_STATE 1-9) | core/Compat.lua:337-347 | E | identical values |
| Enum.ItemQuality (quality column, labels) | core/ItemSetup.lua, Constants.lua:162-170 | E | identical 0-8 |
| Enum.ItemClass 0/2/4 (literals) | core/Compat.lua:387,945 | E | identical |
| Enum.CurrencyDestroyReason | core/Compat.lua:960-966; Constants.lua:344-353 | E | identical members |
| Enum.CurrencySource | core/Compat.lua:963 | ? | absent from BOTH dumps (runtime-only); same risk both clients (smoke LED-P2-14) |

### 2c. Events (all 34 documented in BOTH dumps — VERIFIED)
LOOT_OPENED, ENCOUNTER_START/END, CHALLENGE_MODE_START/COMPLETED/RESET (inert on Forever), TRADE_ACCEPT_UPDATE,
QUEST_TURNED_IN, ZONE_CHANGED_NEW_AREA (modules/Attribution.lua:420-428); UNIT_SPELLCAST_SUCCEEDED (:431);
CHAT_MSG_LOOT/CURRENCY/MONEY (modules/Collector.lua:340-342); PLAYER_INTERACTION_MANAGER_FRAME_SHOW/HIDE, MAIL_SEND_SUCCESS,
MAIL_FAILED, ADDON_LOADED (modules/AttributionOut.lua:172-177); BAG_UPDATE, BAG_UPDATE_DELAYED, PLAYER_EQUIPMENT_CHANGED,
PLAYER_MONEY, ACCOUNT_MONEY, CURRENCY_DISPLAY_UPDATE, PLAYERBANKSLOTS_CHANGED, PLAYER_ACCOUNT_BANK_TAB_SLOTS_CHANGED,
PLAYER_REGEN_ENABLED, CURRENCY_TRANSFER_LOG_UPDATE, MAIL_INBOX_UPDATE, OWNED_AUCTIONS_UPDATED (modules/Reconciler.lua:696-700);
PLAYER_ENTERING_WORLD, PLAYER_REGEN_DISABLED, GLOBAL_MOUSE_DOWN, GROUP_ROSTER_UPDATE (lifecycle/browser/sim).
PLAYERBANKSLOTS_CHANGED and PLAYER_ACCOUNT_BANK_TAB_SLOTS_CHANGED are registered by Forever's own bank
(Camelot/BankFrame.lua:340-344). CURRENCY_DISPLAY_UPDATE payload (id, qty, change, gainSource, destroyReason)
identical (Forever CurrencyInfoDocumentation.lua:595-604). Events not registrable cost one edge via SafeRegisterEvent.

### 2d. Global functions
| Global | Where | Class | Evidence |
|---|---|---|---|
| GetNumLootItems | core/Compat.lua:53-56 | E | Forever Mainline/LootFrame.lua |
| GetLootSourceInfo | core/Compat.lua:60-63 | ? | not in either dump nor Forever FrameXML checkout; KILL/CONTAINER attribution depends on it (probe) |
| GetZoneText / GetSubZoneText | core/Compat.lua:76-82 (fallback) | E | doc |
| IsInInstance / IsInGroup / UnitAffectingCombat / InCombatLockdown | core/Compat.lua:38-110,870-873 | E | doc / FrameXML |
| GetQuestID / GetQuestReward (hook) | core/Compat.lua:138-147 | E | Mainline QuestFrame.lua |
| SpellIsTargeting | core/Compat.lua:151-153 | E | SecureTemplates.lua |
| GetInboxHeaderInfo / GetInboxNumItems / GetInboxItem / TakeInboxItem / AutoLootMailItem / TakeInboxMoney / SendMail / GetSendMailItem / GetSendMailMoney | core/Compat.lua:173-180,974-1001; hook rows Attribution.lua:439-440, AttributionOut.lua:155-156 | E | Blizzard_MailFrame/MailFrame.lua (MailFrame.toc AllowLoadGameType mainline incl. camelot, INFERRED) |
| GetInboxItemLink | core/Compat.lua:982 | ? | no Forever FrameXML hit; guarded `type(...)=="function"` |
| GetMoney / GetCursorMoney / GetPlayerTradeMoney | core/Compat.lua:836-841 | E | doc / TradeFrame.lua |
| GetInventoryItemID / GetInventoryItemLink | core/Compat.lua:850-855 | E | FrameXML |
| UnitClass / UnitGUID | core/Compat.lua:875-879; SimDrivers.lua:52 | E | doc |
| UnitName | core/Util.lua:7; core/Compat.lua:1050 | **D** | 2nd return = surname on Forever (Camelot/NameUtil.lua:5) |
| GetNormalizedRealmName / GetRealmName | core/Util.lua:8-9,370; Compat.lua:1054,1066 | E | doc |
| BuyMerchantItem / BuybackItem / RepairAllItems / DeleteCursorItem (hooks) | Attribution.lua:438; AttributionOut.lua:150-154 | E | MerchantFrame.lua, GameDialogDefs.lua |
| UseContainerItem (global fallback hook) | core/Compat.lua:117-122 | M (both) | unused: C_Container path wins |
| GetCoinTextureString | core/Util.lua:71-73 | ? | no bare global in Forever FrameXML; C_CurrencyInfo.GetCoinTextureString exists in both dumps; guarded with text fallback |
| ChatEdit_InsertLink | modules/BrowserTable.lua:591-592,1016 | E (deprecated) | Blizzard_DeprecatedChatInfo/Deprecated_ChatFrame.lua:43 alias to ChatFrameUtil.InsertLink; same on Retail ("removed at next expansion" toc note) |
| CreateAtlasMarkup / CreateTextureMarkup / FauxScrollFrame_* / StaticPopup_Show / BreakUpLargeNumbers / CreateFrame / hooksecurefunc / GetTime / IsShiftKeyDown | various (StaticPopup_Show settings/Schema.lua:150-151,1003-1008,1270-1271; Slash.lua:142,210; Panel.lua:128,300; HoldingsTab.lua:295-296) | E | SharedXML / doc |

### 2e. Global tables and strings
| Global | Where | Class |
|---|---|---|
| ITEM_QUALITY_COLORS | core/ItemSetup.lua:70-72; Constants.lua:169; SkinSetup.lua:271 | E (INFERRED, guarded) |
| RAID_CLASS_COLORS / CLASS_ICON_TCOORDS | CoreSetup.lua:71; BrowserWidgets.lua:75; BrowserTable.lua:154,908; AnalyticsFormat.lua:96; AnalyticsLedger.lua:232; TimelineModel.lua:239 | E (INFERRED); Forever classes are the vanilla nine, extra keys harmless |
| INVSLOT_FIRST/LAST_EQUIPPED | core/Constants.lua:323 | E (fallback 1..19) |
| LOOT_ITEM_SELF(_MULTIPLE), _PUSHED_, _CREATED_, _BONUS_ROLL_, LOOT_ITEM_REFUND(_MULTIPLE), LOOT_ROLL_YOU_WON | core/Util.lua:155-230; Diagnostics.lua:55-57 | ? GlobalStrings not in the checkout; presence assumed, wording may differ (probe) |
| CURRENCY_GAINED(_MULTIPLE/_BONUS/_OVERFLOW), YOU_LOOT_MONEY, LOOT_MONEY_SPLIT, YOU_LOOT_MONEY_GUILD | Collector.lua | ? same |
| ITEM_BIND_TO_ACCOUNT(_UNTIL_EQUIP), ITEM_ACCOUNTBOUND(_UNTIL_EQUIP), ITEM_BIND_TO_BNETACCOUNT, ITEM_BNETACCOUNTBOUND, RETRIEVING_ITEM_INFO | core/Compat.lua:268-275,311 | ? literal fallbacks cover English |
| AUCTION_HOUSE, AUCTION_*_MAIL_SUBJECT, ATTACHMENTS_MAX_RECEIVE/SEND | core/Compat.lua:184-205,977,994,1028-1036 | ? guarded, fallbacks 16/12 |

### 2f. Areas the brief flagged
- **Bank / Warband / tabs / reagent:** account bank, tabs, warband gold all exist (§0.2). Reagent bag exists
  (`Blizzard_MainMenuBarBagButtons/Camelot/MainMenuBarBagButtons.lua:5`, CharacterReagentBagMixin). There is no
  separate reagent BANK member in either enum. Interaction types Banker/AccountBanker/CharacterBanker exist;
  LH's READABLE_ON lists Banker + AccountBanker only (`modules/Reconciler.lua:54-59`) — same as Retail.
  Forever bank is tab-based with `C_Bank.ShouldUsePlayerBagsInBank()` paging (Camelot/BankFrame.lua:93-106).
- **C_LootHistory / group loot / encounter loot:** LH does not use C_LootHistory. ROLL comes from the
  LOOT_ROLL_YOU_WON line (`core/Util.lua:218-227`); ENCOUNTER_* stamps the encounter context. Both events exist.
  RPGLootFeed carries a Forever LootHistory override (`RPGLootFeed/BlizzOverrides/LootHistory.lua:16`), INFERRED
  that Forever's group-loot frame behaves differently; LH is unaffected.
- **C_LFGList:** not used.
- **Name/realm keys:** §0.4.
- **Currency:** full modern currency system present; `Constants.CURRENCY_SOURCE_REASON` members
  FulfillCraftingOrder/ConcentrationCast/AccountTransfer exist in the Forever enum but will mostly never fire.
- **Item levels / quality:** same APIs and enums.
- **Transmog:** not used.
- **Hyperlinks:** item/currency links parsed by pattern (`core/Compat.lua:420-423`, ItemSetup); `C_NameUtil`
  hints player links embed the surname separator (Forever-only API), irrelevant to item links.

## 3. SavedVariables schema and character keying (VERIFIED)
- TOC: `## SavedVariables: LootHistoryDB, LootHistoryPerfDB` (`LootHistory.toc:7`).
- `db.global` (`defaults/Global.lua`): schemaVersion (0 default; ladder top 15, `core/Database.lua:423`), history
  (dense array of records), holdings, daily, retentionDays 30, rollupRetentionDays 0, minimap; plus undeclared
  ledgerSince, resetPrompt(Pending), rollupSeeded (docs/schema.md:368-391).
- `db.profile` (`defaults/Profile.lua`): every setting (32 schema rows, docs/schema.md:253+), blacklist/whitelist,
  window geometry, savedViews. AceDB profiles; Default profile.
- Migrations: 15 steps, v8->v9 moved settings to profile, v10->v11 ledger stores, v12->v13 holder moves, v13->v14
  savedViews, v14->v15 font retirement (`core/Database.lua:16-423`). Runner `NS:RunMigrations` `:432-445`.
- Character key: record `char = Util.PlayerKey()` = `UnitName("player") .. "-" .. normalized realm with spaces
  stripped` (`core/Util.lua:6-12`; Collector.lua:184,246; Reconciler.lua:459). Holdings keyed by the same string,
  Warband = literal `"§warband"` (docs/schema.md:373-384). Daily rollup `[date][holder][thingKey]`.
- Container groups stored by NAME (`bags`/`bank`/`tabs`/`equipped`/`mail`/`auctions`), not bag id
  (docs/schema.md:377,393) — so Forever's renumbering cannot corrupt stored data.
- Retail SV: `_retail_/.../SavedVariables/LootHistory.lua` is 2.37 MB, schemaVersion 15, chars like
  `"Helyâ-Frostmourne"`. Forever WTF (`_forever_/WTF/Account/ADD1KTED2KA0S/SavedVariables/`) has no LootHistory
  file: separate install, separate SavedVariables, no cross-client data sharing (VERIFIED by ls).
- Forever risk: first-name-only keys collide for same-first-name characters; a later fix to full-name keys
  would need a migration of `char`/holdings/daily keys on Forever-originated data (fresh DB, so cheap if done before release).

## 4. Test gate (run from the repo, read-only)
| Run | Result |
|---|---|
| `lua tests/run.lua` | 2054 passed, 0 failed, 1 skipped, 2055 total (rc 0) |
| `KA0S_KIT_CLIENT=forever lua tests/run.lua` | 2054 passed, 0 failed, 1 skipped, 2055 total (rc 0); PASS/SKIP sets identical to retail (diff empty) |
| `~/.claude/dev-copilot/bin/ka0s-bounded luacheck .` | 0 warnings / 0 errors in 166 files (rc 0) |
Only skip (both): "diagnostics contract: an addon that opts out lands the report and leaves logging off — this
addon keeps the default (Kit.diagnostics.enablesLogging is not false)". No Forever-specific failure or skip.
Why it is uninformative: the profile flips WOW_PROJECT_ID/CAMELOT, GetBuildInfo and removes
GetSpecialization*/GetTalentInfo/SetDesaturation only (`tests/_kit/mock_client.lua:18-29`); LH reads none of them,
and `tests/wow_mock.lua:61-87` still serves Retail BagIndex numbers, `UnitName` without a surname and no Keyring.
Logs: research/lh-retail.txt, lh-forever.txt, lh-luacheck.txt.

## 5. Features meaningless (or near) on Forever
- **Mythic+ source (MPLUS) and keystone context**: Attribution.lua:182,249-287; Insights byKeystone (Database.lua:856,1005);
  sim scenario `key`; test data MPLUS rows (BrowserTableTestData.lua:38,253). Challenges UI not loaded (VERIFIED). Hide/gate (INFERRED).
- **Bonus roll (BONUS_ROLL)**: LOOT_ITEM_BONUS_ROLL_SELF lines (Util.lua:161-176) — no bonus-roll content in vanilla era (INFERRED).
- **Deconstruct name-family fallback for Milling/Prospecting/Mass variants** (ARCHITECTURE.md documented deviation
  `localization-§4`): milling/prospecting do not exist in vanilla (INFERRED); Disenchant does.
- **Crafting orders / Concentration / CraftSalvage / CraftEnchant** reasons (Constants.lua:350-351; AttributionOut.lua:163-166): inert (INFERRED).
- **AH commodities hooks** (PostCommodity/ConfirmCommoditiesPurchase): modern AH loads, commodity behaviour on Forever unverified (INFERRED).
- **Warband-bound item states (WARBAND / WARBAND_UE)**: enum supports them; vanilla-content items are unlikely to carry them (INFERRED), the code is harmless.
- **Warband bank / warband gold / currency transfer**: NOT meaningless — present on Forever (§0.2), though account tabs may be unpurchased.
- **Third-party AH price providers** (AuctionPrice.lua): Auctionator runs on Forever (installed), TSM/Oribos unknown.

## 6. Port punch list (inputs to the plan)
1. TOC `## Interface: 120105, 16001` (or the standard's dual-slot form) and the client list in ADDONS.md; docs/forever-quirks.md, ARCHITECTURE.md:576.
2. Character key: full name incl. surname on Forever (UnitName 1st+2nd, or a `GetUnitName("player", false)`-style read), behind a Compat member, no flavor branch if possible (e.g. presence of `C_PlayerInfo.ShouldDisplaySurname`).
3. Trade partner key: Compat.TradeTargetKey must not treat the surname as a realm.
4. QualifyName: do not strip the surname separator space.
5. Keyring: decide whether `^Keyring$` joins BAGS (Forever only has content; Retail enum has it but unused).
6. Gate MPLUS/BONUS_ROLL surfaces (labels, filters, Insights card, sim `key` scenario) when the client has no Challenges UI.
7. Mock: a Forever BagIndex/UnitName-surname profile in tests/wow_mock.lua so the forever run means something.
8. Probes owed (owner, ~24 h): GetLootSourceInfo on a corpse; CHAT_MSG_LOOT/MONEY/CURRENCY wordings; UnitName("player") and ("NPC") returns; GetNormalizedRealmName; FetchDepositedMoney away from bank; account bank tab count; keyring scan; FetchCurrencyTransferTransactions fields; Enum.CurrencySource members; ITEM_BIND_* globals; GetCoinTextureString global.
