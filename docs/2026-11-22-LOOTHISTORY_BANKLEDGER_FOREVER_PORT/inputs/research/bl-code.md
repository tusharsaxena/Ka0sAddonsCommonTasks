# BankLedger: code map for the WoW Forever port

Researched 2026-11-21. Read-only. Repo: `/mnt/d/Profile/Users/Tushar/Documents/GIT/BankLedger` (branch `master`, clean),
v1.3.0, LibKa0s v1.109.0 (kit rev 59). Abbreviations:
- `BL/` = the BankLedger repo
- `FV/` = the Forever UI checkout `.../scratchpad/ui/forever/Interface/AddOns/` (1.60.1 71037)
- `FAPI/` = `FV/Blizzard_APIDocumentationGenerated/`
- `RT/` = the Retail checkout `.../scratchpad/ui/retail/Interface/AddOns/`
- `FSV/` = `/mnt/g/Games/Blizzard/World of Warcraft/_forever_/WTF/Account/ADD1KTED2KA0S/SavedVariables/`
- `FADD/` = `/mnt/g/Games/Blizzard/World of Warcraft/_forever_/Interface/AddOns/`

**VERIFIED** means I read it in source or data. **INFERRED** means I reasoned it and nobody has measured it in game.

---

## 0. Headline findings

1. **Container ids resolve by name on Forever, but the id groups change.** VERIFIED: in `FAPI/BagIndexConstantsDocumentation.lua:25-51`,
   Forever's `Enum.BagIndex` has `CharacterBankTab_1..9` = 6..14 and `AccountBankTab_1..9` = 15..23. Retail has
   `CharacterBankTab_1..6` = 6..11 and `AccountBankTab_1..5` = 12..16 (`RT/.../BagIndexConstantsDocumentation.lua`).
   `BL/core/Constants.lua:118-150` matches members by name pattern, so `C.BANK_IDS` becomes {6..14} and
   `C.WARBAND_BANK_IDS` becomes {15..23} with no code change. VERIFIED measurement: Forever's BagSync recorded the
   character bank under container **6** (`FSV/BagSync.lua:210-236`, 24 items in `[6]`).
2. **The Warband/Account bank API is present on Forever, but the feature is locked.** VERIFIED: the Forever bank frame,
   `FV/Blizzard_UIPanels_Game/Camelot/BankFrame.lua`, handles `Enum.BankType.Account` (lines 30, 44, 133, 187-188,
   288-297). The shared base adds the Account tab (`FV/Blizzard_UIPanels_Game/Mainline/BankFrameTemplates.lua:42-49`)
   and shows each tab only when `C_Bank.CanViewBank(bankType)` is true (`:67-72`). INFERRED, from third-party code:
   BagSync's comment at `FADD/BagSync/core.lua:185` says "WoW Forever has the whole account bank API but it's
   locked", and BagSync gates the feature on `CanViewBank(Account)` or a purchased-tab count above 0 (`:189-201`).
   The owner's Forever data shows `warband§.money = 0` and no warband tabs (`FSV/BagSync.lua:3-5`). The standard says
   "the warband bank" is absent on Forever and must be **absent, never just hidden** (`WowAddonStandards/standards/standards/clients.md:8`;
   `forever-quirks.md:85`).
   **Consequence:** BankLedger would keep `WARBAND_BANK` reachable (its 9 ids are non-empty, `BL/modules/Ledger.lua:40-47`).
   It would scan 9 empty containers on every pass, and every surface that lists stores would show "Warband Bank".
   Fixing this needs a feature-detected gate.
3. **Identity is the one real behavior bug.** `BL/core/Compat.lua:36-42` builds `name, realm` from `UnitName("player")`
   (first return only) and `GetNormalizedRealmName()`, and `BL/core/Util.lua:7-10` joins them as `Name-Realm`.
   On Forever that gives `"Traxex-CAMWOWAU1Realm2PvP"`. The surname is dropped, so two characters that share a first
   name collide. The standard requires `"Traxex Silentshot"` through LibKa0s-Compat `CharacterKey()`
   (`forever-quirks.md:119-150`; `BL/libs/LibKa0s/Compat.lua:441-454`, already vendored in `LibKa0s.xml`).
   The vendored AceDB is minor 40 (`BL/libs/AceDB-3.0/AceDB-3.0.lua:44`), which already keys profiles regionally (`:263-266`).
4. **The Forever gate is red, 5 failures, all from sample identity.** Section 5 has the detail.
5. **No function BankLedger calls is missing from Forever's global set.** VERIFIED against the kit's Ketho-derived
   `BL/tests/_kit/client_globals_forever.lua` (its `removed` list at line 50 contains none of BankLedger's names).
   The kit's Forever scan is dormant until the TOC carries 16xxx (`BL/tests/_kit/client_globals.lua:55-56`).
6. **Guild bank: the code loads on Forever, but whether the world has a guild vault is unknown.** VERIFIED:
   `FV/Blizzard_GuildBankUI/Blizzard_GuildBankUI.toc:7-9` loads the `[Family]` mainline files, and the camelot
   family is part of mainline. The evidence is `FV/Blizzard_UIPanels_Game/Blizzard_UIPanels_Game.toc:44`, which uses
   `[AllowLoadGameType mainline] [ExcludeLoadGameType camelot]`, a combination that only makes sense if camelot is
   inside mainline. The Forever guild-bank API doc is byte-identical to Retail's (diff empty). The owner's guild
   "Warcraft Forever©" has empty BagSync `tabs = {}` (`FSV/BagSync.lua:574-577`). INFERRED: the vault may not exist in
   the vanilla-era world. This needs a probe.
7. **Separate WTF trees, so no data migration is needed.** VERIFIED: `_forever_/WTF/...` and `_retail_/WTF/...` are
   separate directories. BankLedger is not installed on Forever yet (no `BankLedger` under `FADD/`, no
   `BankLedger.lua` under `FSV/`). A Forever ledger starts empty. A change of key shape on Forever touches no stored rows.

---

## 1. Module list (TOC order, `BL/BankLedger.toc`)

TOC: `## Interface: 120105` (line 1). The port needs `120105, 16001`. `## SavedVariables: BankLedgerDB` (line 7).

| File | Lines | Purpose | Forever impact |
|---|---|---|---|
| core/Compat.lua | 195 | The only caller of varying APIs: guild name, `PlayerName`/`PlayerClass`, purse, store coin, container readers, guild-bank readers, item resolver | **Edits:** identity (`:36-42`); warband money/visibility gate (`:80-85`); header "Retail-only addon" (`:5`) |
| core/SimSetup.lua | 173 | LibKa0s-Sim seam; wraps Compat; `NS.SAMPLE_FALLBACK` Retail rows (`:136-142`); `NS.SampleCharacters` (`:144`) | Fallback rows are Retail-only and Name-Realm; the comment at `:134-135` says "ships Retail alone" |
| core/EnvSetup.lua | 103 | LibKa0s-Env seam: metadata, version, map id, zone | `C_AddOns.GetAddOnMetadata` (`:47-56`), `C_Map.GetBestMapForUnit` (`:84-85`), `GetZoneText`/`GetSubZoneText` (`:100-101`), all present |
| core/ItemSetup.lua | 89 | LibKa0s-Item seam; `ITEM_QUALITY_COLORS` (`:51-53`); `C_Item.RequestLoadItemDataByID` + `C_Timer.After` (`:85-87`) | Present |
| core/MediaSetup.lua | 116 | LibKa0s-Media seam (the mono font) | None |
| core/Constants.lua | 366 | Store/Context/Direction/Kind enums; `StoreOrder` (`:17-19`); labels (`:21-26`); colors (`:92-97`); **BagIndex name-pattern groups** (`:118-162`); `STORE_OPTIONS` (`:272-277`) | Groups re-resolve by name. WARBAND_BANK is always present in `StoreOrder` and `STORE_OPTIONS` |
| core/Namespace.lua | 20 | `NS.name`, `SCHEMA_VERSION`, prefix | None |
| core/CoreSetup.lua | 254 | LibKa0s-Core seam; `RegisterEventSafely` (`CreateFrame` `:180`, `C_EventUtils.IsEventValid` `:208`) | Present. An unknown event lands in `NS.EventRecord` |
| core/DebugLogSetup.lua | 202 | DebugLog seam | None |
| core/LifecycleSetup.lua | 115 | Stand-down latch | None |
| core/State.lua | 49 | Runtime state (openContext, lastSnapshot, debug) | None |
| core/Util.lua | 427 | **`PlayerKey` (`:7-10`)**; money (`GetCoinTextureString` `:43-44`); `ClassIconMarkup` (`CLASS_ICON_TCOORDS` `:121`); `WowheadURL` (`:95-108`); `InCombatLockdown` (`:314`) | PlayerKey shape. The wowhead base URL may be wrong for Forever item ids (open question Q6) |
| core/BankLedger.lua | 365 | AceAddon, bus, OnInitialize/OnEnable, combat edges | None found |
| core/Database.lua | 753 | AceDB `New("BankLedgerDB", defaults, true)` (`:9`); migrations v3-v7; Query/QueryList; search fields include `e.char` (`:693`) | None structural |
| core/DatabaseStats.lua | 367 | Insights aggregation (byChar `:156`) | None |
| core/PoolSetup.lua | 51 | Pool seam | None |
| core/LauncherSetup.lua | 309 | LDB/LibDBIcon launcher | None |
| core/SkinSetup.lua | 912 | LibKa0s-Skin seam (`InCombatLockdown` `:535`, `C_Timer.After` `:576-578`, `ITEM_QUALITY_COLORS` `:300`, `EllesmereUI` `:314`) | None (EllesmereUI is installed on Forever) |
| defaults/Global.lua | 40 | Account-wide: `schemaVersion`, `ledger`, `settings.retentionDays`, `minimap` | Schema in section 3 |
| defaults/Profile.lua | 92 | Per-profile settings, filter lists, `excludedStores` (`:36`), windows, sim, appearance | `excludedStores` may hold `WARBAND_BANK` |
| modules/Filters.lua | 131 | Blacklist/whitelist id sets | None |
| modules/Ledger.lua | 928 | **The capture engine**: `MONEY_STORES` (`:20`), `CONTEXT_STORES` (`:30-33`), `StoresFor` (`:40-47`), diff, scan, snapshot, gate, BuildEntry (`char` `:345`), settle, guild-bank frame hooks (`:670-703`), the CAPTURE event table (`:825-858`), Enable (`:904-928`) | WARBAND gating; event semantics need a probe |
| modules/Ledger_Diagnose.lua | 162 | `/bl debug scan`: BagIndex dump (`:37-49`), id groups (`:52-59`), container probe over -8..40 (`:20,61-70`), money/BankType probes (`:72-112`), guild bank (`:114-130`), events (`:132-137`) | **This is the probe tool for the owner's in-game session.** It already covers ids 15..23 |
| modules/SimWorld.lua | 408 | Sim world: `BACKPACK_SLOTS=20`, `TAB_SLOTS=98` (`:33-34`), `WARBAND_MONEY` (`:31`), `buildChars` main key `name.."-"..realm` (`:147-157`), groups from `C.BANK_IDS`/`C.WARBAND_BANK_IDS` (`:194,201`), `Enum.BagIndex` (`:48`) | Identity shape; the warband world |
| modules/SimDrivers.lua | 290 | Sim event drivers, including the warband lag (`:46-47,139-192`) | Warband scenario |
| modules/Sim.lua | 490 | Sim session host (`InCombatLockdown` `:115`; warband labels `:294-337`) | Warband scenario |
| modules/SimScenario.lua | 108 | Scenarios bank / **warband** (`:43-60,98`) / guild / onesided (warband, `:83-91`) | A warband scenario on Forever shows an absent feature |
| modules/Backfill.lua | 190 | Login backfill of uncached item fields | None |
| modules/Browser.lua | 1235 | Ledger window, filter bar; char dropdown (`:382-397`, width `DD_W.char=140` `:40`); store dropdown is **data-driven** (`:327-337`); `RAID_CLASS_COLORS` (`:388`); `ResolveCharFilter` (`:418-430`) | Long Forever names in a 140 px dropdown |
| modules/Browser_Views.lua | 305 | Per-tab saved views | None |
| modules/Browser_Chrome.lua | 240 | Window chrome/geometry | None |
| modules/LedgerTable.lua | 1041 | History table (char column `:111-112`, `RAID_CLASS_COLORS` `:493`, `ChatEdit_InsertLink` `:634-635,957`, FauxScrollFrame `:719,846-847`) | Char column width |
| modules/LedgerTable_TestMode.lua | 317 | Test-mode dataset: stores include WARBAND_BANK (`:41,172,202`); own chars include **EVOKER** (`:113-117`), Name-Realm | Shows the warband and an Evoker on Forever |
| modules/SessionWindow.lua | 787 | Live session window; preview rows WARBAND_BANK (`:207-208,229`); `PlayerKey` (`:219,228`) | Warband preview |
| modules/InsightsWidgets.lua | 936 | Charts; `W.ShortChar` = `^[^-]+` (`:144-146`) | Forever keys have no `-`, so the whole "First Surname" is kept in a 118 px bar |
| modules/Insights.lua | 757 | Insights tab; store lists iterate StoreOrder but skip empty stores (`:612-630`); tooltips name the warband (`:71-73`) | Tooltip copy |
| modules/Insights_Render.lua | 299 | Renderers | None |
| modules/Export.lua | 485 | CSV; `char` column (`:40`); `wowhead` column (`:57`); store rows only where data exists (`:154-161`) | Wowhead URL |
| modules/Diagnostics.lua | 323 | `/bl diagnostics` (`C_AddOns.IsAddOnLoaded` `:289`) | None |
| settings/Schema.lua | 1097 | Schema; trackMoney tooltip names the warband (`:54-55`); `excludedStores` grid over `C.STORE_OPTIONS` (`:78-87`) | The grid always shows Warband Bank |
| settings/Slash.lua | 519 | Slash seam, StaticPopupDialogs (`:7-49`) | None |
| settings/OptionsSetup.lua | 320 | Options seam | None |
| settings/Panel.lua | 817 | Store grid render (`:205`), `BreakUpLargeNumbers` (`:152`), `StaticPopup_Show` | Grid |
| settings/Profiles.lua | 73 | AceDBOptions page | Forever profile keys are "First Surname" (AceDB 40) |
| locales/enUS.lua, PostLoad.lua | 29/7 | Locale seam | None |

---

## 2. Every WoW API, global, enum and event, classified for Forever

How each call was checked: **DOC** means it is in `FAPI` (the Forever-generated docs, which differ from Retail's, so
they are Forever's own: `BankDocumentation.lua` adds `BankBagTypeAndIDToInvSlot`, `FetchMaxNumBankTabs` and
`ShouldUsePlayerBagsInBank` against Retail). **FXML** means it is defined or used in Forever FrameXML. **CG** means it
is present in the kit's Forever globals set (not in its `removed` list). Every entry is VERIFIED present unless it says otherwise.

### 2a. Bank model (the focus)

| Call / name | BankLedger site | Forever | Notes |
|---|---|---|---|
| `Enum.BagIndex` (iterated by name) | Constants.lua:130-146; Ledger_Diagnose.lua:39-49; SimWorld.lua:48 | **DIFFERS** | FAPI BagIndexConstants:25-51: 27 members, `CharacterBankTab_1..9` = 6..14, `AccountBankTab_1..9` = 15..23, `Keyring` = -1, `ReagentBag` = 5. No `Bank`/`BankBag_N`. The name patterns at Constants.lua:121-124 still match. The `Characterbanktab` = -2 and `Accountbanktab` = -3 type constants are excluded by the anchored patterns (Constants.lua:114-117) |
| BAGS group `Backpack, Bag_N, ReagentBag` | Constants.lua:121,148 | exists | ReagentBag (5) is a live 5th bag slot on Forever. VERIFIED by BagSync's `bagslot=5` item 254035 (FSV/BagSync.lua:289-294). **`Keyring` (-1) is not in BAGS**, and Forever has a real keyring (BagSync `bag[-1]` holds 2 items, FSV/BagSync.lua:~280; the kit's Forever "added" list carries `GetKeyRingSize` and `C_ActionBar.ShouldShowKeyring`). INFERRED: a key moved between the keyring and the bank is a one-sided change, so no row is written |
| BANK group `Bank, BankBag_N, CharacterBankTab_N` | Constants.lua:123,149 | exists (differs) | Resolves to 6..14 (9 tabs vs Retail 6). On Forever the "tabs" are bank bags (`C_Bank.ShouldUsePlayerBagsInBank`, FAPI Bank:322; Camelot BankFrame.lua:86-102,154-189). The first tab is the base bank. Slot counts vary by bag |
| WARBAND_BANK group `AccountBankTab_N` | Constants.lua:124,150 | ids exist; **feature locked** | Resolves to 15..23. INFERRED: `GetContainerNumSlots` answers 0 while the account bank is locked |
| `C_Container.GetContainerNumSlots` | Compat.lua:93-94 | exists | DOC Container:313 |
| `C_Container.GetContainerItemInfo` (`.itemID/.hyperlink/.stackCount`) | Compat.lua:101-105 | exists | DOC Container:192. Field names not re-diffed (INFERRED same) |
| `C_Bank.FetchDepositedMoney(Enum.BankType.Account)` | Compat.lua:81-84; Ledger_Diagnose.lua:93-97 | exists | DOC Bank:181 (returns WOWMONEY, non-nil). INFERRED: answers 0 while locked, so no money row (the diff needs both sides to move, Ledger.lua:143-154) |
| `Enum.BankType.{Character=0,Guild=1,Account=2}` | Compat.lua:82; Ledger_Diagnose.lua:85-110 | exists | DOC ItemConstants:24-26 |
| `C_Bank.CanViewBank` | **not used** | exists | DOC Bank:91. **The candidate feature-detect for the warband gate** (Blizzard's own gate, BankFrameTemplates.lua:70) |
| `C_Bank.FetchNumPurchasedBankTabs / FetchPurchasedBankTabData / PurchaseBankTab / FetchNextPurchasableBankTabData / UpdateBankTabSettings` | not used | exist | DOC Bank:226,241,311,211,331. BankLedger does not track tab purchases or settings |
| `BANKFRAME_OPENED` / `BANKFRAME_CLOSED` | Ledger.lua:829-830 | exists | DOC Bank:398/392. Forever opens the bank through PlayerInteractionManager (`Banker`/`CharacterBanker`/`AccountBanker`, BankFrameTemplates.lua:126-137), same as Retail. INFERRED: fires (probe) |
| `PLAYERBANKSLOTS_CHANGED` | Ledger.lua:834 | exists | DOC Bank:414. Forever's bank-bag buttons listen to it (Camelot BankFrame.lua:350-368) |
| `BAG_UPDATE_DELAYED` | Ledger.lua:833 | exists | DOC Container:677 |
| `PLAYER_MONEY` | Ledger.lua:835 | exists | DOC CurrencyInfo:637. Note: buying a bank bag while the bank is open moves the purse only, so by design (BANK is not in MONEY_STORES) no row is written |
| `PLAYER_ACCOUNT_BANK_TAB_SLOTS_CHANGED`, `BANK_TABS_CHANGED`, `BAG_CONTAINER_UPDATE`, `ACCOUNT_MONEY` | not registered | exist | DOC Bank:404,382; CurrencyInfo:589. Not needed |

### 2b. Money

| Call | Site | Forever |
|---|---|---|
| `GetMoney` | Compat.lua:53-54; Ledger.lua:275 (via Compat); Ledger_Diagnose.lua:106; SimWorld.lua:385 | exists (DOC PlayerScript:642) |
| `GetCoinTextureString` | Util.lua:43-44 | exists (DOC CurrencyInfo:161) |
| `BreakUpLargeNumbers` | Panel.lua:152 | exists (DOC Localization:42) |

### 2c. Guild bank (legacy globals: none are in the API docs on either client)

| Call | Site | Forever |
|---|---|---|
| `GetGuildInfo("player")` | Compat.lua:26-27 | exists (FXML: FV/Blizzard_FrameXML/InstanceDifficulty.lua:219; CG) |
| `GetGuildBankMoney` | Compat.lua:76-78; Ledger_Diagnose.lua:108,111 | exists (FXML: FV/Blizzard_GuildBankUI/Mainline/Blizzard_GuildBankUI.lua:204) |
| `GetGuildBankItemLink` | Compat.lua:112-113 | exists (FXML GuildBankUI.lua:202,690) |
| `GetGuildBankItemInfo` | Compat.lua:116-117 | exists (FXML GuildBankUI.lua:195,246) |
| `GetNumGuildBankTabs` | Compat.lua:125-126 | exists (FXML GuildBankUI.lua:160) |
| `QueryGuildBankTab` | Compat.lua:136-137; SimSetup.lua:53,167 | exists (FXML GuildBankUI.lua:62,597) |
| `GetCurrentGuildBankTab` | Compat.lua:142-143 | exists (FXML GuildBankUI.xml:724) |
| `GuildBankFrame` + `:HookScript` | Compat.lua:158-160; Ledger.lua:672-688 | exists if the LoD addon loads (Blizzard_GuildBankUI.toc:2,7-8) |
| `MAX_GUILDBANK_SLOTS_PER_TAB` | Compat.lua:165 | **differs**: on Forever it is a FILE-LOCAL (`local MAX_GUILDBANK_SLOTS_PER_TAB = 98`, GuildBankUI.lua:1), so it is not a global. BankLedger's literal fallback of 98 covers it (Compat.lua:165). Harmless |
| `ADDON_LOADED` "Blizzard_GuildBankUI" | Ledger.lua:698-703,840 | exists (DOC AddOns:391) |
| `GUILDBANKBAGSLOTS_CHANGED` | Ledger.lua:838 | exists (DOC GuildBank:70) |
| Guild vault in the Forever world | n/a | **UNKNOWN** (INFERRED probably absent in vanilla content; BagSync `tabs={}`) |

### 2d. Items

| Call | Site | Forever |
|---|---|---|
| `C_Item.GetItemInfo` (returns 1,2,3,6,7) | Compat.lua:175-178,190-192 | exists (DOC Item:626) |
| `C_Item.RequestLoadItemDataByID` | ItemSetup.lua:85-86 | exists (DOC Item:1710) |
| `ITEM_QUALITY_COLORS` | Constants.lua:256; ItemSetup.lua:51-53; SkinSetup.lua:300 | INFERRED exists (not in the local sparse tree; guarded at every site) |
| Wowhead URL `https://www.wowhead.com/item=` | Util.lua:95-108; Export.lua:57 | **probably differs**: Forever item ids such as 273047 and 280088 (FSV/BagSync.lua:192-235) are Forever-only. INFERRED: Retail wowhead does not resolve them |

### 2e. Identity, world and UI globals

| Call | Site | Forever |
|---|---|---|
| `UnitName("player")` | Compat.lua:37 | **DIFFERS**: the 2nd return is the surname (forever-quirks.md:128). BankLedger keeps only the 1st |
| `GetNormalizedRealmName` / `GetRealmName` | Compat.lua:38-39 | **DIFFERS**: the long label "CAMWOWAU1Realm2PvP" (forever-quirks.md:131) |
| `UnitClass` | Compat.lua:47 | exists (DOC Unit:911). Forever has the 9 vanilla classes |
| `UnitNameUnmodified`, `RegionalUniqueNamesEnabled` | not used (used by vendored LibKa0s Compat :425-454) | exist (DOC Unit:2523, :536) |
| `GetZoneText` / `GetSubZoneText` | EnvSetup.lua:100-101 | exists |
| `C_Map.GetBestMapForUnit` | EnvSetup.lua:84-85 | exists (DOC Map:49) |
| `C_AddOns.GetAddOnMetadata` / `IsAddOnLoaded` | EnvSetup.lua:47-56; Diagnostics.lua:289 | exists (DOC AddOns:165,322) |
| `C_EventUtils.IsEventValid` | CoreSetup.lua:208 | exists (DOC EventUtils:26) |
| `C_Timer.After` | ItemSetup.lua:87; SkinSetup.lua:576-578 | exists |
| `GetTime`, `time`, `date` | Ledger.lua:603,344 | exists |
| `InCombatLockdown` | SkinSetup.lua:535; Util.lua:314; LedgerTable_TestMode.lua:264; Sim.lua:115 | exists |
| `IsShiftKeyDown` | LedgerTable.lua:634; SessionWindow.lua:385 | exists |
| `ChatEdit_InsertLink` | LedgerTable.lua:634-635,957; SessionWindow.lua:385-386 | exists as a deprecated alias (FV/Blizzard_DeprecatedChatInfo/Deprecated_ChatFrame.lua:43); absent from the kit's live set too |
| `FauxScrollFrame_Update/GetOffset/OnVerticalScroll` | LedgerTable.lua:719,846-847; SessionWindow.lua:609,680-681 | exists (FV/Blizzard_SharedXML/SecureScrollTemplates.lua:158,227,236) |
| `RAID_CLASS_COLORS` | Browser.lua:388; InsightsWidgets.lua:137; LedgerTable.lua:493 | exists (FV/Blizzard_SharedXML/ClassColors.lua:1, includes EVOKER etc.) |
| `CLASS_ICON_TCOORDS` | Util.lua:121 | exists (FV/Blizzard_SharedXML/SharedConstants.lua:27-42) |
| `CreateFrame`, `UIParent`, `GameTooltip`, `UISpecialFrames`, `StaticPopup_Show`, `StaticPopupDialogs`, `Settings.*` | many (see grep in section 1) | CG present; StaticPopupDialogs is used by Forever FrameXML |

---

## 3. SavedVariables schema and keying

- One AceDB `BankLedgerDB` (`BL/core/Database.lua:9`, `defaultProfile=true`).
- **`db.global`** (`BL/defaults/Global.lua:17-40`): `schemaVersion` (default 0; real stamp = `NS.SCHEMA_VERSION`, migrations
  v3-v7 in Database.lua:100-330), `ledger` (an array, oldest first, **one ledger per account across all characters**),
  `settings.retentionDays` (30), `minimap`.
- **`db.profile`** (`BL/defaults/Profile.lua:13-92`): `blacklist`, `whitelist`, `savedViews`, `settings.{enabled,
  trackItems, trackMoney, qualityThreshold, excludedStores, visibility, windowScale, alpha, locked, window,
  rowStripe/Hover*, showSessionWindow, sessionWindow, sim.stepDelay, appearance}`.
- **Ledger entry** (`BL/modules/Ledger.lua:340-382`): `ts, char, classFile, kind (ITEM|MONEY), direction
  (DEPOSIT|WITHDRAW), store (BANK|WARBAND_BANK|GUILD_BANK), quantity, zone, subzone, mapID, guild (guild-bank only),
  itemName ("Gold" for money), itemID, quality, itemType, itemSubType, itemLink`. Store and direction values are the
  CSV contract and must never be renamed (Constants.lua:6-7).
- **Character key**: `char = NS.Util.PlayerKey()`, which is `UnitName .. "-" .. GetNormalizedRealmName (whitespace stripped)`
  (Util.lua:7-10, Compat.lua:36-42). Realms and accounts are not keyed separately: the realm is part of the `char`
  string, and the account is implied by the WTF Account folder. Retail data VERIFIED: `["char"] = "Trâxex-Frostmourne"`
  and others (10 characters, 253 rows; stores BANK 21, GUILD_BANK 3, WARBAND_BANK 229), with profileKeys
  `"Trâxex - Frostmourne"` (`_retail_/.../SavedVariables/BankLedger.lua:4036-4042`).
- **Forever key today** (INFERRED from forever-quirks.md:128-131): `"Traxex-CAMWOWAU1Realm2PvP"`. That key drops
  the surname and so can collide. The standard's key is `"Traxex Silentshot"` (CharacterKey). The AceDB profile key is
  already `"Traxex Silentshot"`.
- **Readers of `char` that assume the "Name-Realm" shape:** `W.ShortChar` `^[^-]+` (InsightsWidgets.lua:144-146) keeps
  the whole Forever name, which is good but long. `charOptions` sorts on the raw value (Browser.lua:392). Test mode,
  SimWorld and the tests hardcode Name-Realm. Search and Export treat `char` as opaque text (Database.lua:693; Export.lua:40,182).

---

## 4. UI: what assumes the Warband bank or tabs

Data-driven, so it adapts once no warband rows exist:
- The History store dropdown lists only stores present in the data (Browser.lua:327-337).
- The Insights "By store" lists skip empty stores (Insights.lua:612-630).
- The Export by-store rows appear only where data exists (Export.lua:154-161).

Always shows the Warband bank (each of these needs a gate on Forever):
- `C.StoreOrder`/`C.StoreLabel`/`C.StoreRGB` (Constants.lua:17-26,92-97) feed `C.STORE_OPTIONS` (Constants.lua:272-277).
  That feeds the settings "Banks to record" grid (`settings.excludedStores`, Schema.lua:78-87; Panel.lua:205), so the
  grid always shows a **Warband Bank** checkbox.
- `L.CONTEXT_STORES[BANK_FRAME] = {BANK, WARBAND_BANK}` (Ledger.lua:30-33) and `L.MONEY_STORES` (Ledger.lua:20).
  `StoresFor` drops a store only when its id group is empty (Ledger.lua:40-47), and on Forever the group is not
  empty. The result: 9 extra empty-container reads per pass, and a `WARBAND_BANK 0` entry in each [Store] and [Diff]
  debug line (Ledger.lua:720-726, 497-503).
- Copy: the trackMoney tooltip "guild and warband banks" (Schema.lua:54-55); the Insights goldIn/goldOut tooltips
  (Insights.lua:71-73); Ledger.lua comments.
- Test mode: sample rows for WARBAND_BANK (LedgerTable_TestMode.lua:41,172,202) and an EVOKER sample character
  (`:117`, a class absent on Forever).
- Session window preview: WARBAND rows and warband money (SessionWindow.lua:207-208,229).
- Simulator: the "Warband transfer" scenario (SimScenario.lua:43-60,98), the onesided scenario's warband step
  (`:83-91`), drivers (SimDrivers.lua:46-47,139-192), labels (Sim.lua:294-337), and world state (SimWorld.lua:31,194,301-316,380).
- Sizes: `SW.TAB_SLOTS = 98` (SimWorld.lua:34) is Retail's tab size. Forever bank "tabs" are bags whose size varies,
  so the sim world shape is only cosmetic. `BACKPACK_SLOTS = 20` (`:33`).
- The guild bank: no Forever-specific UI. The pseudo-event and hook path (Ledger.lua:670-703,842-857) is
  client-agnostic and stays dormant if the frame never shows.

---

## 5. Gate results (run 2026-11-21, master, clean)

Raw outputs: `.../scratchpad/research/bl-gate-{retail,forever,luacheck}.txt`.

| Command | Result |
|---|---|
| `lua tests/run.lua` | **1724 passed, 0 failed, 1 skipped, 1725 total**, exit 0 |
| `KA0S_KIT_CLIENT=forever lua tests/run.lua` | **1719 passed, 5 failed, 1 skipped, 1725 total**, exit 1 |
| `~/.claude/dev-copilot/bin/ka0s-bounded luacheck .` | **0 warnings / 0 errors in 125 files**, exit 0 |

The skip, identical on both clients: "diagnostics contract: an addon that opts out lands the report and leaves logging off".
BankLedger keeps the default (`Kit.diagnostics.enablesLogging`), so the skip is by design.

The 5 Forever failures. Every one comes from `Sim.Sample()`, which answers Forever rows (`fullName = "First Surname"`,
`BL/libs/LibKa0s/Sim.lua:316-344`) when `ClientKey()=="forever"`, while the host and the tests assume Name-Realm:
1. `tests/test_sim_world.lua:141` "SimWorld: main is the real player; after Switch the identity members answer the alt".
   It expected `Sampleblade-Samplerealm` and got `Sampleblade Mockvale`.
2. `tests/test_sim_world.lua:158` "SimWorld: a paladin's alt is the shared sample warrior". It expected
   `Mockshield-Mockrealm` and got `Mockshield Sampleforge`.
3. `tests/test_sample_characters.lua:69` "every test-mode character follows the convention, none on a real realm".
   `conventional()` (`:24-30`) requires `^(%a+)%-(%a+)$` and rejects `Samplemender Mockbrook`.
4. `tests/test_sample_characters.lua:104` "without the library test mode draws the same characters". The degraded
   ledger lost `Samplemender Mockbrook`, because the degraded path uses the Retail `NS.SAMPLE_FALLBACK`
   (SimSetup.lua:136-142) while the library path uses the Forever rows.
5. `tests/test_sim_e2e.lua:188` "Sim e2e: warband records main's 2 deposits and the alt's 2 withdrawals...". Row 3's
   `char` was expected as `Sampleblade Mockvale` and came back `Sampleblade-Samplerealm`. The mismatch is between the
   sim's alt key (`alt.fullName`, SimWorld.lua:155) and what `PlayerKey` builds from the switched `PlayerName`
   (`name.."-"..realm`). In other words, the host's identity seam is Name-Realm and the library's Forever rows are not.

The Forever mock profile changes only the `WOW_PROJECT_*` constants, `GetBuildInfo` and a few absent globals
(`BL/tests/_kit/mock_client.lua:18-30`). It does **not** model Forever's `Enum.BagIndex`, the locked account bank,
`RegionalUniqueNamesEnabled` or the two-word `UnitName`. So a green Forever suite proves little about capture on
Forever, and the port must add its own Forever-shaped mocks. Also, `client_globals` stays live-only until the TOC
carries 16001 (`BL/tests/_kit/client_globals.lua:55-56`). My manual check against the Forever set found no missing names.

---

## 6. Port work list (INFERRED plan inputs)

1. TOC `## Interface: 120105, 16001`. Add `docs/forever-quirks.md` (forever-quirks-§1). Update ADDONS.md Clients to
   `Retail · Forever`. Update the README line 9 and the Compat header (Compat.lua:5), compat-layer.md:7,73 and
   ARCHITECTURE.md:778-779.
2. Identity: `Compat.PlayerName` and `Util.PlayerKey` go through LibKa0s-Compat `CharacterKey()` / `UnitCharacterName`
   when `RegionalNames()`. Keep `Name-Realm` on Retail so existing Retail data still matches. SimWorld `buildChars`
   (`:147-157`) must use the same key builder. `NS.SAMPLE_FALLBACK` needs Forever rows, or the call
   `Sim.Sample(client)` must pick the right set. The Name-Realm assumptions in `TEST_OWN_CHARS` (LedgerTable_TestMode.lua:113-117)
   and in tests/test_sample_characters.lua:24-30 must change too.
3. Warband gate: a Compat member, for example `Compat.HasAccountBank()`, feature-detected through
   `C_Bank.CanViewBank(Enum.BankType.Account)` or the purchased-tab count. Drop `WARBAND_BANK` from `StoresFor`,
   `STORE_OPTIONS`, test mode, the session preview, the sim scenarios and the tooltips when it answers false.
   Whether to evaluate it at load or at bank open is an open question.
4. Guild bank: keep the path dormant (it degrades). Decide whether to hide "Guild Bank" from the settings grid on Forever.
5. Test-mode classes: EVOKER on Forever (LedgerTable_TestMode.lua:117).
6. Wowhead URL per client.
7. Forever-shaped mocks in tests (BagIndex 6..14/15..23, CanViewBank=false, two-word names).

## 7. Open questions for the owner (the probe can answer most)

- Q1: Warband: with the account bank locked on Forever, should BankLedger drop the Warband Bank store entirely from
  every surface (the standard says absent, never hidden), and gate it dynamically so it appears if Blizzard unlocks it?
- Q2: Does `C_Bank.CanViewBank(Enum.BankType.Account)` answer false on Forever, at login and at a banker? Do
  `GetContainerNumSlots(15..23)` answer 0? Probe with `/bl debug scan` at a banker, which already dumps BagIndex, the
  groups, containers -8..40, FetchDepositedMoney and the events (Ledger_Diagnose.lua).
- Q3: Guild bank: is there a guild vault in the Forever world? If not, should "Guild Bank" leave the settings grid and
  the sim scenarios on Forever?
- Q4: Character key on Forever: "First Surname" alone (the standard; realm = ruleset), or "First Surname-Ruleset"?
  The standard (forever-quirks-§4) says the whole name, with no realm in the key.
- Q5: Keyring (-1): should BAGS include `Keyring` so that key moves between the keyring and the bank are seen? Can keys
  go in the Forever bank at all?
- Q6: The Export wowhead column on Forever: which URL (if any) resolves Forever item ids? Or should the column be blank?
- Q7: Does `BANKFRAME_OPENED` fire on Forever, and do the bank-bag (tab) contents update through `BAG_UPDATE_DELAYED` or
  `PLAYERBANKSLOTS_CHANGED`? (Either reconciles, Ledger.lua:833-835.)
