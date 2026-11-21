# How the bank works on WoW Forever (Camelot, 1.60.1 build 71037)

Sources:
- `FV` = `/tmp/claude-1000/-mnt-d-Profile-Users-Tushar-Documents-GIT-Ka0sAddonsCommonTasks/cc9586a8-8986-4d94-9659-95fca377c5ee/scratchpad/ui/forever/Interface/AddOns`. This is the Blizzard UI source, branch forever, commit 734f065 "1.60.1 (71037)".
- `RT` = `.../scratchpad/ui/retail/Interface/AddOns`. This is the Retail 12.1.5 source.
- `DOC` = `Blizzard_APIDocumentationGenerated`.
- `FA` = `/mnt/g/Games/Blizzard/World of Warcraft/_forever_/Interface/AddOns`. These are third-party addons installed on Forever.

Labels:
- **VERIFIED** means I read it in the source at the cited line.
- **VERIFIED-3P** means a third-party addon's code or comment says so. These comments record in-game observations by their authors, not by us.
- **INFERRED** means I deduced it and have not read it directly.

## 0. Load model: Camelot is a member of the "mainline" family

- **VERIFIED.** `FV/Blizzard_UIPanels_Game/Blizzard_UIPanels_Game.toc:140` reads `[Family]\BankFrame.xml [AllowLoadGameType mainline] [ExcludeLoadGameType camelot]`. An exclusion from "mainline" only means something if camelot is part of mainline. Line 141 loads `[Game]\BankFrame.xml [AllowLoadGameType camelot]`, which is the `Camelot/` folder.
- So on Forever, the Mainline bank code `Mainline/BankFrameTemplates.lua` (toc:137, mainline) **loads**, and `Camelot/BankFrame.lua` (toc:138) loads on top of it as an override. The classic `Vanilla/BankFrame.lua` (toc:190, vanilla only) does **not** load.
- BagSync's comment agrees: "WoW Forever runs the retail client, but has its own project ID (WOW_PROJECT_CAMELOT = 18)" (`FA/BagSync/core.lua:28-33`).
- BagSmith disagrees: "Forever reports WOW_PROJECT_MAINLINE" (`FA/BagSmith/Core/Init.lua:13-21`). It detects Forever by the TOC `X-Game` value "Camelot" or by an interface number in the 16000-19999 range.
- BagSync explains the disagreement: "Early beta builds reported MAINLINE with a 1.x interface" (`core.lua:29`). Its detection is belt-and-braces: `WOW_PROJECT_ID == WOW_PROJECT_CAMELOT`, or `== 18`, or an interface below 100000 plus `C_GameRules.GetForeverExperiencePreset` / `C_PlayerInfo.ShouldDisplaySurname` (core.lua:31-45).

## 1. Character bank: the modern bank-tab system, with tabs that are real bags

**Answer: Forever uses the modern `C_Bank` tab API, not the classic `BANK_CONTAINER = -1`, `GetNumBankSlots` and `PurchaseSlot` model.** Each bank tab is a container, and its size comes from a real bag the player puts into the tab's socket. This is a hybrid of tabs and classic bank bags.

### API and constants

- **VERIFIED.** `FV/.../Camelot/BankFrame.lua` uses only `C_Bank.*`:
  - `PurchaseBankTab` and `FetchNextPurchasableBankTabData` (:14, :17)
  - `FetchNumPurchasedBankTabs` and `FetchMaxNumBankTabs` (:43-44)
  - `ShouldUsePlayerBagsInBank` (:87)
  - `FetchPurchasedBankTabData` (:91, :144)
  - `CanViewBank` (:115)
  - `BankBagTypeAndIDToInvSlot` (:304)
- **VERIFIED.** Nothing in the Forever UI tree defines or calls `GetNumBankSlots`, `PurchaseSlot`, `BankButtonIDToInvSlotID`, `NUM_BANKBAGSLOTS` or `BANK_CONTAINER`. The grep hits were in the `Vanilla/` files only, plus unrelated `PurchaseSlot` matches.
- **VERIFIED.** No `DOC` file contains `GetNumBankSlots`, `NUM_BANKBAGSLOTS`, `BankButtonIDToInvSlotID`, `REAGENTBANK*` or `IsReagentBankUnlocked`.
- **VERIFIED.** `Enum.BagIndex` has **no** `Bank` (-1) and no `BankBag_N` members on Forever (`FV/DOC/BagIndexConstantsDocumentation.lua:25-51`).
- **INFERRED.** The global `BANK_CONTAINER` is nil on Forever. BagSmith handles it as possibly nil (`Init.lua:30`), and BagSync's `BagIndex.Bank` guard handles nil (`scanner.lua:454, :484`).

### Tab-per-bag layout

- **VERIFIED.** `Camelot/BankFrame.lua:26-31` defines `GetBagIDFromBankTypeAndSlot`. Character returns `bagSlot + ITEM_INVENTORY_BANK_BAG_OFFSET`, and Account returns `+ NUM_CHARACTER_BANK_SLOTS`. Both constants are set in `FV/Blizzard_FrameXMLBase/Constants.lua:172, :174`. `ITEM_INVENTORY_BANK_BAG_OFFSET` is `NUM_TOTAL_EQUIPPED_BAG_SLOTS` (:170), which is `NUM_BAG_SLOTS + NUM_REAGENTBAG_SLOTS`.
- **VERIFIED.** The bag that fills tab N sits in a pseudo-container:
  - Character: `ItemLocation:CreateFromBagAndSlot(Enum.BagIndex.Characterbanktab /* -2 */, N)` (`BankFrame.lua:186, :323, :367`)
  - Account: `Accountbanktab /* -3 */` (:188, :325, :371)
  - Pickup works through `C_Container.PickupContainerItem(-2, N)` (:378-382).
- **VERIFIED.** `BankBagTypeAndIDToInvSlot(bankType, slotIndex)` exists to map a socket to its inventory slot (`BankFrame.lua:303-305`, `FV/DOC/BankDocumentation.lua:30-44`).
- **VERIFIED.** The bag-socket buttons run `for bagNum = 2, maxBankBags`, with the comment "We skip the first bag as we start with the first bag purchased" (`BankFrame.lua:153-154`). `PurchaseFirstSlot()` auto-buys the Character tab when `tabCost == 0` (:197-206). So **tab 1 is the free base bank and has no player socket**.
- **VERIFIED-3P.** BagSmith's in-game probe: "container -1 has 32 slots and holds the keys; the bank's own slots are container 6, a placeholder tab bag, and its bags follow" (`FA/BagSmith/Core/Init.lua:40-41`). The placeholder item is named with "(DNT)" or "Bank Tab Bag" (`Init.lua:100-102`).
- **VERIFIED-3P.** BagSync: "WoW Forever uses actual bags for the bank tabs. The first tab is the bank itself, so the bags start at slot 2" (`FA/BagSync/wireframe/scanner.lua:362`). Its scan of the socketed bags is at `scanner.lua:363-390`.

### How Blizzard's bank panel reads the tabs

- **VERIFIED.** The item display walks `FetchPurchasedBankTabData(bankType)` and sums `C_Container.GetContainerNumSlots(tabData.ID)` (`Mainline/BankFrameTemplates.lua:1064-1068`, `Camelot/BankFrame.lua:91-101`). **Each tab's `ID` is a container ID (a BagIndex) that `C_Container` reads normally.**
- **VERIFIED.** With `ShouldUsePlayerBagsInBank()` true:
  - All tabs are drawn as one paged grid of 96 slots per page by default (`BankFrameTemplates.lua:3`). Camelot overrides this to 88 (`Camelot/BankFrame.xml:89`).
  - The tab-strip pool is not created (:687-689).
  - The purchase prompt is skipped for Character (:941-943).
  - Any `BAG_UPDATE` marks the panel dirty (:791-795).
- **INFERRED, needs an in-game probe.** `C_Bank.ShouldUsePlayerBagsInBank()` returns true on Forever. The whole Camelot bag-socket UI (`BankFrame.lua:136-191`) only makes sense if it does, and both third-party addons treat it as the Forever path (BagSync `scanner.lua:296`).

## 2. `Enum.BagIndex` on Forever compared with Retail (container IDs)

Forever is `FV/DOC/BagIndexConstantsDocumentation.lua:18-51`, with NumValues 27 and a range of -3 to 23. Retail is `RT/DOC/BagIndexConstantsDocumentation.lua:18-46`, with NumValues 20 and a range of -3 to 16.

| Member | Forever | Retail 12.1.5 |
|---|---|---|
| Accountbanktab (socket pseudo-container) | -3 | -3 |
| Characterbanktab (socket pseudo-container) | -2 | -2 |
| Keyring | -1 | -1 |
| Backpack, Bag_1..Bag_4 | 0..4 | 0..4 |
| ReagentBag | 5 | 5 |
| CharacterBankTab_1..N | **6..14 (N=9)** | 6..11 (N=6) |
| AccountBankTab_1..N | **15..23 (N=9)** | 12..16 (N=5) |

- **VERIFIED.** `Mainline/ContainerFrame.lua:92-98` (Forever tree) checks `CharacterBankTab_1..CharacterBankTab_9` and `AccountBankTab_1..AccountBankTab_9`.
- **Consequence: never hard-code tab IDs.** Derive them from the Enum by name. BagSync collects `CharacterBankTab_1..N` with a `while` loop (`FA/BagSync/core.lua:159-178`). BankLedger already matches by name pattern (`../BankLedger/core/Constants.lua:104-124`, where `^CharacterBankTab_%d+$` and `^AccountBankTab_%d+$` pick up 6..14 and 15..23).
- **INFERRED.** `NUM_CHARACTER_BANK_SLOTS` is 9 at runtime on Forever. `Constants.InventoryConstants.NumCharacterBankSlots` is only `Value = NUM_CHARACTERBANK_SLOTS` in the docs (`FV/DOC/ItemConstants_MainlineDocumentation.lua`, the InventoryConstants table). The value 9 follows from the arithmetic: AccountBankTab_1 = 1 + 5 + 9 = 15, which matches `GetBagIDFromBankTypeAndSlot`.

## 3. Account (Warband) bank: the API exists, the feature is gated

- **VERIFIED.** `Enum.BankType` = `{Character=0, Guild=1, Account=2}` on both clients (`FV/DOC/ItemConstantsDocumentation.lua:17-26`, `RT/DOC/ItemConstantsDocumentation.lua:6-15`).
- **VERIFIED.** The Camelot bank adds an Account page tab only when `C_Bank.CanViewBank(Account)` is true (`BankFrame.lua:114-117, :132-133`). It hides purchasing for Account when 0 tabs are owned (:44). `Enum.PlayerInteractionType.AccountBanker` = 68 and `CharacterBanker` = 67 exist (`FV/DOC/PlayerInteractionManagerConstantsDocumentation.lua:80-81`).
- **VERIFIED-3P.** "WoW Forever has the whole account bank API but it's locked, Blizzard only shows it when CanViewBank(Account) is true" (`FA/BagSync/core.lua:185`). BagSync re-checks this with `CanViewBank(Account)` or `FetchNumPurchasedBankTabs(Account) > 0` at login and when the bank opens (core.lua:189-215).
- **INFERRED, needs an in-game probe.** Whether any Forever player can unlock the Account bank today.

## 4. Reagent bank, reagent bag, keyring, ammo and quivers, bag count

- **Reagent BANK: absent.** VERIFIED: no `REAGENTBANK_CONTAINER`, `IsReagentBankUnlocked` or `PLAYERREAGENTBANKSLOTS_CHANGED` appears anywhere in `FV/DOC` or in the UI grep. The Enum has no reagent-bank index.
- **Reagent BAG slot: present in the UI.**
  - VERIFIED: the Camelot bag bar has `ReagentBag0SlotButton` with slotName `REAGENTBAG0SLOT` (`FV/Blizzard_MainMenuBarBagButtons/Camelot/MainMenuBarBagButtons.xml:127-129`). The keyring is anchored to `CharacterReagentBag0Slot` (:89).
  - VERIFIED: `ITEM_INVENTORY_BANK_BAG_OFFSET = NUM_BAG_SLOTS + NUM_REAGENTBAG_SLOTS` (`FrameXMLBase/Constants.lua:168-172`), and the first bank tab is ID 6.
  - INFERRED: `NUM_REAGENTBAG_SLOTS` is 1, so the offset is 5.
  - INFERRED, probe: whether reagent-bag items exist in Forever content. BagSync gates its reagent-bag handling on `NumReagentBagSlots > 0` (core.lua:182).
- **Keyring: present, as container -1.**
  - VERIFIED: `KEYRING_CONTAINER = Enum.BagIndex.Keyring` (`FrameXMLBase/Constants.lua:166`). The Camelot override defines `PutKeyInKeyRing` and `GetKeyRingSize` over `C_Container.*(KEYRING_CONTAINER, i)` (`Camelot/MainMenuBarBagButtons.lua:47-92`). It is gated by `C_ActionBar.ShouldShowKeyring()` (:117-120, `Mainline/ContainerFrame.lua:10-12`).
  - VERIFIED: `ShouldShowKeyring` is Forever-only (`FV/DOC/ActionBarFrameDocumentation.lua:987`, and has 0 hits in RT). `HasKey` exists in both.
  - VERIFIED-3P: BagSmith says -1 has 32 slots (Init.lua:40). On Forever, -1 is the **keyring, not the bank**; BagSmith had a bug that read keys as bank items (Init.lua:41-45).
  - **Hazard: any code that treats -1 as "the bank" is wrong on Forever.**
- **Ammo and quivers.**
  - VERIFIED: an ammo slot exists, shown by `UnitUsesAmmo("player")` (`Camelot/PaperDollFrame.lua:1517`, `Camelot/CharacterFrame.lua:579-580`). The comment "The backpack shares ID 0 with the ammo slot" is at `Camelot/PaperDollFrame.lua:2183`.
  - VERIFIED: `Enum.BagFlag.RecurseQuivers` and `PreferQuivers` exist (`FV/DOC/BagConstantsDocumentation.lua:21, :24`). This file is identical in RT.
  - INFERRED: quivers and ammo pouches are ordinary equipped bags 1-4, or bank-tab bags, with no separate container ID.
- **Bag count.**
  - VERIFIED: Backpack plus `Bag_1..Bag_4` (`Camelot/MainMenuBarBagButtons.xml:107-124`), plus the reagent bag and the keyring.
  - INFERRED: `NUM_BAG_SLOTS` is 4, from four BagNSlot buttons (BAG0SLOT to BAG3SLOT).

## 5. Events

All of these are VERIFIED in `FV/DOC/BankDocumentation.lua:355-421` and are identical to Retail's:
- `BANKFRAME_OPENED` and `BANKFRAME_CLOSED`, with no payload (:390-400)
- `BANK_TABS_CHANGED(bankType)` (:380-388)
- `BANK_TAB_SETTINGS_UPDATED(bankType)` (:370-378)
- `BANK_BAG_SLOT_FLAGS_UPDATED(slot)` (:360-368)
- `PLAYERBANKSLOTS_CHANGED(slot)` (:412-420)
- `PLAYER_ACCOUNT_BANK_TAB_SLOTS_CHANGED(slot)` (:402-410)

Container events, VERIFIED in `FV/DOC/ContainerDocumentation.lua`, which is byte-identical to RT's: `BAG_CONTAINER_UPDATE` (:623), `BAG_UPDATE(bagID)` (:661), `BAG_UPDATE_DELAYED` (:677), `ITEM_LOCK_CHANGED` (:721).

How Blizzard's own UI uses them, VERIFIED:
- `Camelot/BankFrame.lua:193-195, :238-245` uses `BANK_TABS_CHANGED`.
- The tab-bag socket buttons (:350-376) listen for `PLAYERBANKSLOTS_CHANGED`, which refreshes Character sockets, `PLAYER_ACCOUNT_BANK_TAB_SLOTS_CHANGED`, and `BAG_CONTAINER_UPDATE`, which triggers a full refresh.
- The bank panel listens for `ACCOUNT_MONEY`, `BANK_TABS_CHANGED`, `BAG_UPDATE`, `BANK_TAB_SETTINGS_UPDATED`, `INVENTORY_SEARCH_UPDATE`, `ITEM_LOCK_CHANGED` and `PLAYER_MONEY` (`Mainline/BankFrameTemplates.lua:622-630`).

Bankers and the interaction manager:
- VERIFIED: the bank frame registers with the interaction manager for **three** types: `Banker` (8), `CharacterBanker` (67) and `AccountBanker` (68) (`Mainline/BankFrameTemplates.lua:126-138`). All three open BankFrame, and BankFrame:OnShow calls `OpenAllBags` (:97-102).
- VERIFIED-3P: BagSync used to watch only `PLAYER_INTERACTION_MANAGER_FRAME_SHOW == Banker`, which missed opens at Character and Account bankers. It now uses `BANKFRAME_OPENED` and `BANKFRAME_CLOSED` (`FA/BagSync/CHANGELOG.md:6-10`, `wireframe/unit.lua:231-242`).
- **Use BANKFRAME_OPENED and BANKFRAME_CLOSED, not the interaction type.**

Events that do not exist:
- VERIFIED: `PLAYERBANKBAGSLOTS_CHANGED` and `KEYRING_UPDATE` appear in neither the FV nor the RT DOC. BagSmith still registers them (`Core/Scanner.lua:858-859`).
- INFERRED: registering an unknown event on the modern client raises "Attempt to register unknown event". **Don't register them.**

Timing quirks, VERIFIED-3P:
- "scan on open and again on close, the bank isn't always loaded yet when it first opens (WoW Forever)" (`FA/BagSync/wireframe/events.lua:300-313`).
- If the tabs report 0 slots on open, BagSync keeps its old data (`scanner.lua:463-478`).
- "bank tab sockets (WoW Forever) and purchased tabs can change without a BAG_UPDATE for the container", so BagSync debounces a rescan by 0.5 s on `BAG_CONTAINER_UPDATE`, `BANK_TABS_CHANGED` and `PLAYERBANKSLOTS_CHANGED` (`events.lua:198-202, :315-320, :371-378`).
- BagSmith rescans on `BANK_TABS_CHANGED` and `BANK_TAB_SETTINGS_UPDATED` (`Frames/Bank.lua:296-299`), plus `BAG_UPDATE_DELAYED` and `BAG_CONTAINER_UPDATE` (`Core/Scanner.lua:829-830`).

## 6. Guild bank and mailbox

- **Guild bank: the UI loads on Forever.**
  - VERIFIED: `FV/Blizzard_GuildBankUI/Blizzard_GuildBankUI.toc:7-9` loads the `[Family]` files under `[AllowLoadGameType mainline]`. The bootstrap registers with the interaction manager (`Blizzard_GuildBankUI_Bootstrap.lua:22-30`).
  - VERIFIED: `GuildBankDocumentation.lua` is identical between FV and RT, as the diff showed.
  - VERIFIED-3P: BagSmith follows `GuildBankFrame` OnShow/OnHide "and this is how FlareUI does it on Forever" (`FA/BagSmith/Core/Hooks.lua:155-166`). That implies guild banks are reachable in game.
- **Mailbox: present.**
  - VERIFIED: `FV/Blizzard_MailFrame/Blizzard_MailFrame.toc:5-6` is `AllowLoadGameType: mainline`, which means it loads on Forever.
  - VERIFIED: the only API difference is the Forever-only `C_Mail.IsCODEnabled()` (`FV/DOC/MailInfoDocumentation.lua:51`). MailFrame uses it at `MailFrame.lua:1323` and `:1718`. Cash on delivery (COD) can therefore be server-disabled.
  - VERIFIED: `PlayerInteractionType.MailInfo` = 17 exists (`PlayerInteractionManagerConstantsDocumentation.lua:30`).

## 7. API diff, Forever compared with Retail 12.1.5

- `ContainerDocumentation.lua` (C_Container plus the container events): **identical**. `diff` printed nothing.
- `BagConstantsDocumentation.lua` (BagFlag, BagSlotFlags): **identical**.
- `GuildBankDocumentation.lua`: **identical**.
- `BankDocumentation.lua` (C_Bank): Forever is a **superset**. Nothing was removed or changed. Forever adds three functions:
  - `C_Bank.BankBagTypeAndIDToInvSlot(bankType, slotIndex) -> slot?` (FV :30-44)
  - `C_Bank.FetchMaxNumBankTabs(bankType) -> number` (FV :196-209)
  - `C_Bank.ShouldUsePlayerBagsInBank() -> bool` (FV :322-327)
  - The rest is shared: AreAnyBankTypesViewable, AutoDepositItemsIntoBank, CanDepositMoney, CanPurchaseBankTab, CanUseBank, CanViewBank, CanWithdrawMoney, CloseBankFrame, DepositMoney, DoesBankTypeSupportAutoDeposit, DoesBankTypeSupportMoneyTransfer, FetchBankLockedReason, FetchDepositedMoney, FetchNextPurchasableBankTabData, FetchNumPurchasedBankTabs, FetchPurchasedBankTabData, FetchPurchasedBankTabIDs, FetchViewableBankTypes, HasMaxBankTabs, IsItemAllowedInBankType, PurchaseBankTab, UpdateBankTabSettings, WithdrawMoney.
  - The structs `BankTabData {ID, bankType, name, icon, depositFlags, tabCleanupConfirmation, tabNameEditBoxHeader}`, `PurchasableBankTabData` and `BankLockedReason` are the same on both (FV :424-466).
- `BagIndexConstantsDocumentation.lua`: Forever has **9+9 tabs**; Retail has 6+5. See §2.
- `ItemConstantsDocumentation.lua`:
  - Forever-only `Enum.BankTabFlags {AllowMissingBag = 1}` (FV :6-16). INFERRED: a tab may exist with no bag in its socket.
  - `Enum.BankType` is the same on both.
  - Unrelated BonusStatIndex renames.
- `ActionBarFrameDocumentation.lua`: Forever-only `C_ActionBar.ShouldShowKeyring` (FV :987).
- `MailInfoDocumentation.lua`: Forever-only `C_Mail.IsCODEnabled` (FV :51).
- `PlayerInteractionManagerConstantsDocumentation.lua`: Banker, GuildBanker, MailInfo, CharacterBanker and AccountBanker have the same values on both.

## 8. How third-party Forever addons scan the bank

**BagSync 20.41**, with Interface values including 16001:
- Detection is described in §0.
- `IsBankTabsActive = Enum.BagIndex.CharacterBankTab_1 ~= nil` (core.lua:157).
- `IsBankBagSlotsActive = Enum.BagIndex.Characterbanktab and C_Bank.ShouldUsePlayerBagsInBank` (core.lua:179-180).
- Bank range = the first through last `CharacterBankTab_*` (scanner.lua:141-145).
- `SaveBank`:
  - It skips the scan if `CanViewBank(Character) == false`, the Warband-only-banker case (scanner.lua:440-447).
  - It saves the tab bags through ItemLocation(-2, slot 2..#tabs) (:296-297, :363-390).
  - It aborts if no tab has slots yet (:463-478).
  - It then reads each tab with `C_Container.GetContainerNumSlots` and `GetContainerItemInfo` (:488-492, SaveBag :246-287).
- The keyring is saved as a bag when `HasKey()` is true (:216-225).
- The Warband scan is gated on `isWarbandActive` (:747-749).

**BagSmith 1.9.5**, with Interface 16001:
- The backend is "modern" when `C_Bank.FetchNumPurchasedBankTabs` and `PurchaseBankTab` exist (`Frames/Bank.lua:8-26`).
- `Bank:Info` uses `FetchNumPurchasedBankTabs`, `FetchMaxNumBankTabs`, `FetchNextPurchasableBankTabData.tabCost` and `CanPurchaseBankTab` (:36-49).
- `InvSlot(i)` tries `C_Container.ContainerIDToInventoryID(NUM_BAGS+i)` first, then `C_Bank.BankBagTypeAndIDToInvSlot` (:86-94).
- Bank bags = `NUM_TOTAL_EQUIPPED_BAG_SLOTS + 1 .. + NUM_BANK_BAGS`, where NUM_BANK_BAGS falls back to `InventoryConstants.NumCharacterBankSlots` (`Core/Init.lua:27-37, :72-74`). That gives 6..14.
- The bank is scanned only while `atBank` is set, which BANKFRAME_OPENED sets (`Core/Scanner.lua:298, :845-856`).

## 9. Implications for BankLedger and LootHistory (INFERRED)

1. BankLedger's name-pattern bank IDs (`core/Constants.lua:121-124`) already yield 6..14 and 15..23 on Forever, and hard-code nothing. Keyring -1 and the socket pseudo-containers -2 and -3 match no pattern. Decide whether the keyring counts as "bags" and whether the socketed bank bags themselves are tracked items.
2. Tab 1 is a placeholder "(DNT)" bag. Its container (6) holds the base bank slots. The socket pseudo-container -2 slot 1 may report that placeholder item, so filter it out if -2 is ever scanned.
3. BankLedger's Warband (AccountBankTab) path must be gated on `C_Bank.CanViewBank(Enum.BankType.Account)` on Forever.
4. Money: `C_Bank.FetchDepositedMoney(Account)` exists, but it is meaningless while the Account bank is locked.
5. Open and close: BANKFRAME_OPENED/CLOSED already drive BankLedger (`modules/Ledger.lua:829-834`). Add a deferred rescan, because tab slot counts may read 0 at the moment of open (BagSync quirk), and add BANK_TABS_CHANGED and BAG_CONTAINER_UPDATE.

## Open probes for the owner (once in-game probes are possible)

1. `/dump C_Bank.ShouldUsePlayerBagsInBank()`, which is expected to be true.
2. `/dump C_Bank.FetchPurchasedBankTabData(0)` and `/dump C_Bank.FetchMaxNumBankTabs(0)`.
3. `/dump C_Container.GetContainerNumSlots(6)` at the bank and away from it.
4. `/dump C_Bank.CanViewBank(2), C_Bank.FetchNumPurchasedBankTabs(2)`.
5. `/dump NUM_BAG_SLOTS, NUM_REAGENTBAG_SLOTS, NUM_CHARACTER_BANK_SLOTS, BANK_CONTAINER, C_ActionBar.ShouldShowKeyring(), C_Container.GetContainerNumSlots(-1)`.
6. `/dump C_Item.GetItemLink(ItemLocation:CreateFromBagAndSlot(-2,1))`, which checks for the DNT placeholder.
7. Does BANKFRAME_OPENED fire at every banker type?
8. Does GetContainerNumSlots(6..14) return 0 at the moment of open?
