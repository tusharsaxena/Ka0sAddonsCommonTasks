# SYNTHESIS: the WoW Forever port of LootHistory and BankLedger

Synthesized 2026-11-21 from `lh-code.md`, `bl-code.md`, `forever-bank.md`, `forever-loot.md`, `patterns.md` and
`sv-data.md` (all in this folder), with source re-checks where the reports disagreed or were thin. Read-only; no repo
was touched. The only write outside this file was widening the Forever sparse checkout (`Blizzard_MoneyFrame/`,
`Blizzard_Deprecated/`).

Abbreviations: `LH/` = `GIT/LootHistory`, `BL/` = `GIT/BankLedger`, `STD/` = `GIT/WowAddonStandards/standards`,
`LK/` = `GIT/LibKa0s`, `FV/` = the Forever UI checkout `.../scratchpad/ui/forever/Interface/AddOns`, `FAPI/` =
`FV/Blizzard_APIDocumentationGenerated`, `K/` = `research/ketho/` (Ketho BlizzardInterfaceResources dumps), `FA/` =
`_forever_/Interface/AddOns` (third-party addons), `FSV/` = `_forever_/WTF/Account/ADD1KTED2KA0S/SavedVariables`.
**V** = VERIFIED in source/data at the cite. **V-3P** = a third-party addon's code or comment says so. **I** = INFERRED.

---

## 0. Reconciled disagreements between the reports

| Topic | Report A | Report B | Resolution |
|---|---|---|---|
| Warband (account) bank on Forever | `lh-code.md` §0.2: "NOT meaningless", present | `bl-code.md` §0.2, `forever-bank.md` §3, `sv-data.md` §4: API present, feature locked | **API present, feature locked, and the standard says absent.** The Camelot bank adds the Account page only when `C_Bank.CanViewBank(Account)` is true (`FV/Blizzard_UIPanels_Game/Camelot/BankFrame.lua:114-117,132-133`, V). BagSync: "the whole account bank API but it's locked" (`FA/BagSync/core.lua:185`, V-3P). Owner's data: `warband§ = {money = 0}`, no tabs (`FSV/BagSync.lua:3-4`, V). The standard names "the warband bank" as a Retail-only feature a Forever player never sees (`STD/standards/clients.md:8`) and forbids feature detection deciding whether a whole feature exists (`clients.md` §3, "Feature detection MUST NOT decide whether a whole feature exists"). So: declare it Retail-only. |
| `GetLootSourceInfo` | `lh-code.md` §2d: "?" (not in dumps) | `forever-loot.md` §6: present | **Present.** `K/fn_forever.lua:5575` (V). It is a C global Ketho lists; the generated docs do not carry it. |
| Loot chat strings | `lh-code.md` §2e: "? presence assumed, wording may differ" | `forever-loot.md` §0.3, §4: 36/36 byte-identical | **Identical** for every self-loot/currency/money string LH parses (V, `gsdiff-loot.txt`). The exception is the roll lines, see §1a. |
| `GetCoinTextureString` | `lh-code.md`: no bare global | `bl-code.md` §2b: "exists (DOC CurrencyInfo:161)" | **Only `C_CurrencyInfo.GetCoinTextureString` is documented** (`FAPI/CurrencyInfoDocumentation.lua:5,161`, namespace `C_CurrencyInfo`, V). No bare global in the Forever MoneyFrame or Deprecated trees (grep empty after widening, V); the kit's Ketho sets carry only the namespaced form on both clients (`BL/tests/_kit/client_globals_live.lua`, grep, V). Both addons call the bare global behind a guard with a text fallback (`LH/core/Util.lua:66-75`, `BL/core/Util.lua:40-45`), so I: money may already render as "Ng Ns Nc" text on both clients. Probe P9. |
| Guild bank on Forever | `bl-code.md` §0.6: vault "may not exist" | `forever-bank.md` §6: UI loads, BagSmith hooks it "as FlareUI does on Forever" | **UI loads** (`FV/Blizzard_GuildBankUI/Blizzard_GuildBankUI.toc:7-9`, V); reachable per `FA/BagSmith/Core/Hooks.lua:155-166` (V-3P); owner's guild has `tabs = {}` (`FSV/BagSync.lua:574-577`, V). Treat as supported, unproven. Probe P6. |

---

## 1. Port surface per addon

### 1a. LootHistory (v1.5.0, LibKa0s v1.109.0, 63 non-lib TOC files)

**Baseline gate** (V, `lh-code.md` §4): retail 2054/0/1, forever 2054/0/1, luacheck 0/0. The Forever run proves
little: the shipped code reads no client (`LH/core/Compat.lua:5-7` declares Retail-only), `tests/wow_mock.lua:61-87`
serves Retail BagIndex numbers and a one-word `UnitName`, and the sample identity is pinned to Retail
(`LH/core/SimSeam.lua:82-102`, `Sim.Sample("retail")` at :100, V).

**Works unchanged on Forever** (V unless marked):
- Every `C_*` function, enum and event LH uses is documented on Forever (`lh-code.md` §0.1, §2a-2c, against the
  dumped `api-forever.tsv`). Modern AH, Professions, TokenUI and the currency-transfer UI load
  (`FV/Blizzard_TokenUI/Blizzard_TokenUI.toc:2-7`; `lh-code.md` §0.1).
- Container ids derive by `Enum.BagIndex` member name (`LH/core/Constants.lua:294-320`), so Forever's renumbering
  (`CharacterBankTab_1..9 = 6..14`, `AccountBankTab_1..9 = 15..23`, `FAPI/BagIndexConstantsDocumentation.lua:25-51`)
  is absorbed. Holdings store columns by name (`bags/bank/tabs/...`), never by id (`LH/docs/schema.md:377,393`), so
  stored data cannot be corrupted by ids.
- Self-loot, currency and money chat parsing: strings identical (`forever-loot.md` §4). `CHAT_MSG_LOOT` payload identical
  (`FAPI/ChatInfoDocumentation.lua:1816`). Item links use the same `|cnIQn:|Hitem:` shape (`sv-data.md` §3, V in
  DropWatcher/ConsumableMaster Forever SVs).
- Loot window reads (`GetNumLootItems`, `GetLootSlotLink`, `GetLootSourceInfo`), `LOOT_OPENED`, `ENCOUNTER_START/END`,
  trade, mail, merchant, quest, `CURRENCY_DISPLAY_UPDATE` (payload identical, `FAPI/CurrencyInfoDocumentation.lua:595-604`)
  (`forever-loot.md` §6-7).
- Mail (`FV/Blizzard_MailFrame/Blizzard_MailFrame.toc:5-6` mainline), the modern AH
  (`Blizzard_AuctionHouseUI.toc:9,15`), the guild-bank hook path.
- `C_LootHistory`, `C_LFGList`, `C_TransmogCollection`: **not used by LH** (grep of core/ modules/ empty, V). So
  `lootListKey` vs `lootListID` (`FAPI/LootHistoryDocumentation.lua:66`) and the group finder do not touch LH.

**Must change (behavior bugs on Forever):**
1. **Character key.** `Util.PlayerKey` = one-value `UnitName("player")` .. "-" .. normalized realm
   (`LH/core/Util.lua:6-12`): on Forever `"Traxex-CAMWOWAU1Realm2PvP"`, which drops the surname and collides for two
   characters sharing a first name (`STD/standards/forever-quirks.md` §4; Auctionator's Forever SV shows exactly this
   form, `sv-data.md` §1, V). Feeds `char`, `holdings`, `daily` (`Collector.lua:184,246`, `Reconciler.lua:459`).
2. **Trade partner key.** `local name, realm = UnitName("NPC")` (`LH/core/Compat.lua:1048-1057`) reads the surname as a
   realm → `"Traxex-Silentshot"`.
3. **`Util.QualifyName`** strips all whitespace and appends the realm (`LH/core/Util.lua:366-372`): a typed
   `"Traxex Silentshot"` recipient becomes `"TraxexSilentshot-CAMWOWAU1Realm2PvP"`, so own-alt MOVE detection
   (`LH/modules/AttributionOut.lua:70,112`) misses.
4. **`Compat.LatestCurrencyTransfer`** appends the realm to `destinationCharacterName` (`LH/core/Compat.lua:1060-1072`);
   the field's Forever form is unknown (probe P5).
5. **Lazy bank on open (I, high impact).** On Forever "the bank isn't always loaded yet when it first opens" and tabs may
   report 0 slots (`FA/BagSync/wireframe/events.lua:300`, `scanner.lua:463-481`, V-3P). LH's first read of a banker visit
   is a **drift pass** that records every difference as UNTRACKED (`LH/modules/Reconciler.lua:630-655`), and LH documents
   that "outside the bank the client answers a bank slot as EMPTY, so reading it would record the whole bank as lost"
   (`Reconciler.lua:49-52`). A 0-slot read at open would write the whole bank as an UNTRACKED loss, then an UNTRACKED gain.
   Needs a not-ready guard.
6. **Banker interaction types.** `READABLE_ON` arms the bank on `Banker` and `AccountBanker` only
   (`LH/modules/Reconciler.lua:54-59`); the bank frame also opens for `CharacterBanker` = 67
   (`FV/Blizzard_UIPanels_Game/Mainline/BankFrameTemplates.lua:126-138`, V). BagSync had this exact bug
   (`FA/BagSync/CHANGELOG.md:6-10`, V-3P). Which type a Forever banker NPC sends is probe P1.
7. **Roll-won line.** Forever's `LOOT_ROLL_YOU_WON` = `"|HlootHistory:%d|h[Loot]|h: You won: %s"` (`K/gs_forever.lua:13940`)
   vs Retail `"You won: %s"` (`K/gs_live.lua:13445`), V. `toLootPattern` maps `%d` to a capture
   (`LH/core/Util.lua:109-114`), so `ParseRollWon` returns the loot-history id, not the link. The Collector only tests it
   for truth (`LH/modules/Collector.lua:160`), so the ROLL stamp still works (V code, I runtime); the sim reader at
   `LH/modules/Sim.lua:170` gets the wrong capture. Harden to take the `%s` capture.
8. **Keyring is invisible.** Keyring = -1 is live on Forever (`FV/Blizzard_FrameXMLBase/Constants.lua:166`,
   `Camelot/MainMenuBarBagButtons.lua:47-92`; BagSync stored 2 keys under `[-1]`, `FSV/BagSync.lua`, `sv-data.md` §4), and
   is in no group (`LH/core/Constants.lua:298-300`), so a key moved between keyring and bags reads as a loss/gain (I).

**Must be gated off (Retail-only; absent, never hidden, `clients.md` §4):**
- **Warband bank:** the `tabs` part and `warbandMoney` part (`Reconciler.lua:29,55-56,98,104,173-200,636`), the
  `WARBAND_DEPOSIT/WITHDRAW` reasons (`Reconciler.lua:264-270`; `Constants.lua:24,37`), the `ACCOUNT_MONEY` and
  `PLAYER_ACCOUNT_BANK_TAB_SLOTS_CHANGED` registrations (`lh-code.md` §2c), the Holdings "Warband" tabs column
  (`LH/modules/HoldingsTab.lua:15`), copy that names the warband (`LH/settings/Schema.lua:345,443,1214`,
  `LH/settings/Slash.lua:14`). 197 warband references across 26 files (grep count, V); most are inert once the parts are
  not registered.
- **Mythic+:** the Challenges UI does not load on camelot (`Blizzard_ChallengesUI.toc` `AllowLoadGameType: standard,
  mists`, `lh-code.md` §0.5, V). MPLUS source and keystone context (`LH/modules/Attribution.lua:182,249-287`), the
  CHALLENGE_MODE_* registrations (`Attribution.lua:420-428`), the Insights keystone breakdown
  (`LH/core/Database.lua:856,1004-1005,1161`), the sim `key` scenario, MPLUS test rows.
- **Content-era sources** (I: no vanilla content): BONUS_ROLL (`LH/core/Util.lua:161-176`), MILLING, PROSPECTING,
  DECONSTRUCT. They appear in `C.SourceOrder` and `C.SOURCE_IMPLEMENTED` (the mute list, `LH/core/Constants.lua:29-68`),
  so a Forever player sees "Mythic+", "Bonus Roll", "Milling", "Warband Deposit" in filters and the mute list today.
- Bound states WARBAND / WARBAND_UE in any filter surface (I: harmless in capture, visible in filters).

**Must be rebuilt for Forever:**
- Per-client source tables (order, labels offered, mute list) picked once by `ClientKey()` (`clients.md` §5-6 seed rule).
- A Forever-shaped test mock (BagIndex 6..23, Keyring, two-word `UnitName`, `RegionalUniqueNamesEnabled` true,
  `CanViewBank(2)` false) so the forever run tests something (`lh-code.md` §4).
- Sample identity, test data and sim seeds per client (`Sim.Sample(ClientKey())`, Forever classes and zones).
- `NS.DEFAULT_SKIN = Skin:DefaultSkin()`; today the literal `skin = "ka0s"` (`LH/defaults/Profile.lua:68`;
  `STD/standards/skinning.md:36`; DW precedent `DropWatcher/core/SkinSetup.lua:102-105`).
- The port shape (TOC, README, docs, forever-quirks.md, tests), §2 of `patterns.md`.

**Effort (I):** large-medium. ~13 items; the Reconciler guard and the per-client source tables are the hard parts.
Comparable to DW-FP00..FP12 without DW's roll work: roughly 1.5-2 agent-days including docs and review.

### 1b. BankLedger (v1.3.0, LibKa0s v1.109.0)

**Baseline gate** (V, `bl-code.md` §5): retail 1724/0/1, **forever 1719/5/1**, luacheck 0/0. All 5 failures are sample
identity: the library's Forever sample rows are `"First Surname"` (`BL/libs/LibKa0s/Sim.lua:316-344`) while BL's seam,
fallback and tests assume `Name-Realm` (`BL/core/SimSetup.lua:134-144`; `tests/test_sim_world.lua:141,158`;
`tests/test_sample_characters.lua:24-30,69,104`; `tests/test_sim_e2e.lua:188`). The kit's globals scan, armed in a
scratch clone with `120105, 16001`, passes (`patterns.md` §0, V).

**Works unchanged:**
- No global BL calls is in the kit's Forever `removed` list (`bl-code.md` §0.5, V).
- Store containers by name (`BL/core/Constants.lua:118-150`): BANK → {6..14}, WARBAND_BANK → {15..23}. BagSync recorded
  the character bank under container 6 (`FSV/BagSync.lua:210-236`, V).
- `BANKFRAME_OPENED/CLOSED` drive the bank context (`BL/modules/Ledger.lua:829-830`), which is the right signal on Forever
  (`forever-bank.md` §5, BagSync's fix, V-3P). The "both sides must change" rule (`Ledger.lua:23-33`) means a lazy 0-slot
  read at open writes no row by itself (I).
- Guild-bank path: legacy globals present in Forever FrameXML (`bl-code.md` §2c); `MAX_GUILDBANK_SLOTS_PER_TAB` is
  file-local on Forever but BL's literal 98 fallback covers it (`BL/core/Compat.lua:165`).
- Data-driven surfaces drop empty stores (History dropdown `Browser.lua:327-337`, Insights `Insights.lua:612-630`,
  Export `Export.lua:154-161`).

**Must change:**
1. **Identity.** `Compat.PlayerName` keeps `UnitName`'s first return and the normalized realm (`BL/core/Compat.lua:36-42`),
   joined by `Util.PlayerKey` (`BL/core/Util.lua:7-10`): `"Traxex-CAMWOWAU1Realm2PvP"`, collides on shared first names.
   SimWorld's `buildChars` (`BL/modules/SimWorld.lua:147-157`) must use the same builder. Fixes failure 5.
2. **Sample identity per client** (failures 1-4): `NS.SAMPLE_FALLBACK` Forever twin, `Sim.Sample(ClientKey())`,
   `TEST_OWN_CHARS` (`BL/modules/LedgerTable_TestMode.lua:113-117`, includes an EVOKER), tests' `conventional()`.
3. **Lazy bank and Forever re-diff cues (I).** Add `BAG_CONTAINER_UPDATE` and `BANK_TABS_CHANGED` as reconcile cues
   (BagSync debounces on them, `FA/BagSync/wireframe/events.lua:198-202,315-320,371-378`, V-3P) and a guard so the
   context baseline is not taken from a 0-slot bank.
4. **Keyring** not in BAGS (`BL/core/Constants.lua:121,148`), so keyring↔bank moves are one-sided and write nothing (I).
5. **Wowhead URL** `https://www.wowhead.com/item=` (`BL/core/Util.lua:95-108`, `Export.lua:57`); Forever-only item ids
   (273047, 280088 in `FSV/BagSync.lua:192-235`) do not resolve there (I).

**Must be gated off (Retail-only):** WARBAND_BANK in `C.StoreOrder/StoreLabel/StoreRGB/STORE_OPTIONS`
(`BL/core/Constants.lua:17-26,92-97,272-277`), `L.CONTEXT_STORES[BANK_FRAME]` and `L.MONEY_STORES`
(`BL/modules/Ledger.lua:20,30-33`; `StoresFor` keeps it because its id group is non-empty, `:40-47`), the settings
"Banks to record" grid (`BL/settings/Schema.lua:78-87`, `Panel.lua:205`), copy (`Schema.lua:54-55`,
`Insights.lua:71-73`), test-mode rows (`LedgerTable_TestMode.lua:41,172,202`), session preview
(`SessionWindow.lua:207-208,229`), sim warband scenario and onesided step (`SimScenario.lua:43-60,83-91,98`,
`SimDrivers.lua:46-47,139-192`, `Sim.lua:294-337`, `SimWorld.lua:31,194,301-316,380`).

**Must be rebuilt for Forever:** Forever-shaped mocks; per-client store table; per-client sample/test-mode/sim seeds
(Forever classes, bag-sized tabs instead of `TAB_SLOTS = 98`, `SimWorld.lua:33-34`); `NS.DEFAULT_SKIN`
(`BL/defaults/Profile.lua:89`); name surfaces sized for "First Surname" (char dropdown 140 px `Browser.lua:40`,
`W.ShortChar` keeps the whole two-word name in a 118 px bar `InsightsWidgets.lua:144-146`, which is the right key but needs
a truncation + tooltip); the port shape.

**Effort (I):** medium. ~11 items, mostly gating and seeds; roughly 1 agent-day. Note that 90% of the owner's Retail BL
data is WARBAND_BANK (229/253 rows, `sv-data.md` §2), so on Forever BL becomes a character-bank and guild-bank ledger.

---

## 2. Proposed design

### 2a. Client detection and routing (both addons)
A new `core/CompatClient.lua` per addon (DW precedent `DropWatcher/core/CompatClient.lua:55-87`; keeps LH's
`core/Compat.lua`, 1071 lines, clear of the 1500-line cap) routing `IsForever/IsRetail/ClientKey/ForClient/RegionalNames/
UnitCharacterName/CharacterKey/RealmKey` from the vendored `LibKa0s-Compat-1.0` (`LK/LibKa0s/Compat.lua:107-160,390-460`,
present in v1.109.0, V) with degradation stubs. No `WOW_PROJECT_*` read anywhere in the addon (`clients.md` §3).

### 2b. Name/realm keys
- `Compat.PlayerRecordKey()`: with `RegionalNames()` → `CharacterKey() or UnitCharacterName("player")` = `"Traxex
  Silentshot"`; otherwise the existing `Name-Realm` over the normalized realm, so every stored Retail row stays the same
  character (DW-FP04, `DropWatcher/core/CompatClient.lua:60-75`, V). `Util.PlayerKey` calls it.
- `Compat.TradePartnerName()` through `UnitCharacterName("NPC")` (DW `CompatClient.lua:82-87`).
- `Util.QualifyName`: on regional names return the trimmed name as typed (no whitespace strip, no realm); Retail unchanged.
- `LatestCurrencyTransfer`: no realm append on regional names.
- No SavedVariables migration on either client: Retail keys do not change, and Forever starts from an empty DB (§2f).

### 2c. Forever bank model (shared by both addons' reasoning)
- **Character bank** = `CharacterBankTab_1..9` (6..14); tab 1 is the free base bank; tabs 2..9 are real bags socketed in
  pseudo-container `Characterbanktab` (-2) slots 2..9 (`FV/.../Camelot/BankFrame.lua:26-31,153-154,186,323`, V;
  `FA/BagSync/wireframe/scanner.lua:362`, V-3P). The store stays one "Bank"; no per-tab breakdown.
- **Readiness guard:** at an open bank, if every BANK id reports 0 slots, the bank is "not ready": no baseline (BL) and
  not readable (LH, which keeps the part dirty, `Reconciler.lua:640-660`), re-tried on `BAG_UPDATE_DELAYED`,
  `BAG_CONTAINER_UPDATE`, `BANK_TABS_CHANGED`, `PLAYERBANKSLOTS_CHANGED` (all documented, `FAPI/BankDocumentation.lua:355-421`,
  `ContainerDocumentation.lua:623,677`). Client-agnostic (a 0-slot bank at an open banker is wrong on Retail too), so no
  client branch.
- **Open/close:** LH adds `CharacterBanker` to `READABLE_ON` (exists in both enums, `forever-bank.md` §7), or keys the bank
  visit on `BANKFRAME_OPENED/CLOSED` like BL. Recommendation: add CharacterBanker (smallest change, keeps LH's
  interaction-manager model).
- **Keyring** (-1) joins the BAGS group in both addons by member name `^Keyring$` (D5). On Retail it reads 0 slots, so
  nothing changes there (I).
- **Warband bank:** declared Retail-only (D1): the store/part/reasons/events are registered only when
  `ForClient({"retail"})`; nothing on Forever scans 15..23.
- **Socketed bank bags** (-2): not scanned by default until probe P10 shows `C_Container.GetContainerItemInfo(-2, n)` or an
  ItemLocation read works and what slot 1 holds ("(DNT)" placeholder, `FA/BagSmith/Core/Init.lua:100-102`, V-3P) (D9).

### 2d. Loot capture on Forever (LH)
Unchanged model: chat lines for receipts, `LOOT_OPENED` + `GetLootSourceInfo` for KILL/CONTAINER, encounter/quest/trade/
mail/merchant stamps. Changes: the roll-won capture fix (§1a.7), per-client source tables (D4), MPLUS/keystone context
registered on Retail only. Currency: keep the full path (the system is present, `forever-loot.md` §7; few currencies exist,
owner has 1792 Honor and 3402 Merchant's Favor, `sv-data.md` §4). Account-wide currencies keep going to the account holder
(`Reconciler.lua:372`), labelled per D2.

### 2e. Group finder
**Neither addon uses it** (`C_LFGList`/LFG grep empty in both repos' core/ and modules/, V; the one hit is an atlas name
`UI-LFG-Lock`, `LH/modules/BrowserTable.lua:67`). Nothing to gate. Forever loads the vanilla-style premade finder
(`FV/Blizzard_GroupFinder/Blizzard_GroupFinder.toc:10`, `Blizzard_GroupFinder_VanillaStyle.toc:5`, V) which is irrelevant.

### 2f. Data separation per client
WTF is per install: `_forever_/WTF/...` and `_retail_/WTF/...` are separate trees, and neither addon has a Forever SV yet
(`sv-data.md` §1, V). So: no client field in rows, no migration, no merge of Retail and Forever data, no Export change for
the client. A Forever DB is born at the top of each migration ladder (LH schema 15, `LH/core/Database.lua:423`; BL v7).
AceDB profile keys are already `"Traxex Silentshot"` (AceDB 40, `BL/libs/AceDB-3.0/AceDB-3.0.lua:263-266`).

---

## 3. LibKa0s and standard changes

**LibKa0s: none required.** Everything the port needs ships in the vendored v1.109.0: Compat client and identity readers
(`LK/LibKa0s/Compat.lua:107-160,390-460`), `Sim.Sample(client)` (`LK/LibKa0s/Sim.lua:343-348`), `Skin:DefaultSkin()`,
the forever kit profile and the TOC-armed globals scan (`patterns.md` §1). No re-vendor.

**Shared bank-model module in LibKa0s: not in this run; file an issue.** Three repos derive container groups by
`Enum.BagIndex` name: BL (`core/Constants.lua:118-150`), LH (copied, its comment says so, `core/Constants.lua:293`) and
OutfitterReborn (`core/Compat.lua:851-863`). A `LibKa0s-Compat` reader such as `ContainerGroups()` plus `BankReady()`
would remove the duplication, but it costs a LibKa0s tag and a collection-wide re-vendor mid-port, and the Forever model
(readiness, sockets, keyring) is not yet probed. Recommendation: build it in the addons now, file a LibKa0s issue that
cites the three copies, promote after the probes (D11).

**Standard:**
- **Required:** the two roster rows in `STD/ADDONS.md` (`:21` BankLedger, `:27` LootHistory) from `Retail (port pending)`
  to `Retail · Forever`, in the change that lands each port (`clients.md` §2), one-line roster-data commits, no version bump
  (precedent `88185bb`, `4a16a2d`, `28f927a`, `patterns.md` §2.17).
- **Not now (harvest candidates):** the Forever bank model (tabs are bags, lazy slot counts, keyring = -1 not the bank,
  `CharacterBanker`) will be recorded in both addons' own `docs/forever-quirks.md` sections, which meets the two-repo bar
  for the next `/dev-copilot:wow-harvest-standards`. The `|HlootHistory:%d|h` roll prefix already sits in DW's quirks
  (`DropWatcher/docs/forever-quirks.md:205`); LH's would be the second repo.

---

## 4. Open questions

### 4a. Decisions only the owner can make

**D1. Warband bank on Forever (both addons).**
Options: (a) Retail-only by declaration (`ForClient({"retail"})`): the store, the settings checkbox, the Holdings tabs
column, the WARBAND reasons, the sim scenario and all copy are absent on Forever; (b) feature-detect
`C_Bank.CanViewBank(Enum.BankType.Account)` so it appears if Blizzard unlocks it; (c) leave it registered.
**Recommend (a).** Evidence: `clients.md:8` lists the warband bank as absent on Forever; `clients.md` §3 forbids (b); (c)
shows a dead "Warband Bank" checkbox and scans 9 empty containers per pass (`bl-code.md` §0.2). If Blizzard unlocks it, a
later change flips the declaration.

**D2. LH's account holder (`§warband`) on Forever.** Account-wide and transferable currencies exist on Forever
(`FV/Blizzard_TokenUI/Camelot/Blizzard_TokenUI.lua:75-80,204,555`, V), and LH files account-wide currency under
`§warband` (`LH/modules/Reconciler.lua:372`). Options: (a) keep the holder for account currencies, labelled "Account" on
Forever (Forever's own copy says "Account", `K/gs_forever.lua:153-155`) and "Warband" on Retail; (b) keep the "Warband" label;
(c) drop account-holder tracking on Forever and file account currencies under the character. **Recommend (a).** The stored
key stays `§warband` on both (stored-key contract).

**D3. CURRENCY_TRANSFER reason on Forever (LH).** The transfer UI loads (`Blizzard_TokenUI.toc:2-3`, V). Options: keep on
both, or Retail-only. **Recommend keep on both**; the field shape is probe P5.

**D4. LH Retail-only sources and surfaces on Forever.** Proposed Forever-absent set: MPLUS + keystone context + Insights
keystone breakdown + sim `key` scenario; BONUS_ROLL; MILLING; PROSPECTING; DECONSTRUCT; WARBAND_DEPOSIT/WITHDRAW; WARBAND
and WARBAND_UE bound-state filter options. Options: (a) drop all of them on Forever via per-client tables; (b) drop only
MPLUS and WARBAND (the two the standard names) and keep the rest offered; (c) keep BONUS_ROLL because its string exists
on Forever. **Recommend (a).** Evidence: Challenges UI excluded on camelot (`lh-code.md` §0.5); no vanilla-era bonus-roll
coins, milling or prospecting (I); "a Forever player never sees a Retail-only feature" (`clients.md:8`). A line that
somehow arrives falls back to a generic source, never lost.

**D5. Keyring.** Options: (a) fold Keyring (-1) into the bags group in both addons; (b) a separate "Keyring" column/store;
(c) ignore it. **Recommend (a)**: keys are owned items, the move bags↔keyring is internal, and no Retail surface changes
(Retail's -1 reads 0 slots, I). Probe P3 confirms keys can't go into the bank (if they can, BL sees keyring↔bank moves).

**D6. Forever character key form.** Options: (a) `"Traxex Silentshot"` (CharacterKey, the standard, AceDB's form);
(b) `"Traxex Silentshot-PvP"` (ruleset suffix). **Recommend (a)** per `forever-quirks.md` §4 ("its identity is its whole
name"; realm key = ruleset, two PvP realms share it). Retail stays `Name-Realm`.

**D7. Guild bank on Forever (BL "Guild Bank" store, LH GUILD_DEPOSIT/WITHDRAW).** Options: keep on both (dormant if the
vault never opens) or Retail-only. **Recommend keep on both**: the UI loads on Forever (`Blizzard_GuildBankUI.toc:7-9`, V)
and a Forever addon hooks it (`FA/BagSmith/Core/Hooks.lua:155-166`, V-3P). Probe P6 confirms.

**D8. BL Export `wowhead` column (and LH's `wowheadLink`, `LH/modules/Export.lua:39`) on Forever.** Options: (a) keep the
column, empty on Forever (CSV shape stable); (b) the Retail URL (wrong for Forever-only ids such as 273047, I);
(c) a URL the owner names (for example a classic Wowhead path) in a per-client table. **Recommend (a)** until the owner
names a URL that resolves Forever ids; switching to (c) later is one constant.

**D9. Socketed bank bags.** Moving a bag into a bank socket (-2) moves an item out of the bags. Options: (a) ignore
sockets (LH would record the bag as an OUT; BL writes nothing); (b) scan -2 slots 2..9 as part of the bank so it reads as
a bank TRANSFER (LH) / DEPOSIT (BL). **Recommend (b) after probe P10, (a) as the build default.** Rare event; correctness
depends on a read we have not proven.

**D10. Cross-client fixes found on the way.** CharacterBanker in LH's `READABLE_ON`, the bank readiness guard, and money
text through `C_CurrencyInfo.GetCoinTextureString` change Retail behavior too. Options: apply on both clients (one
codebase) or Forever-only. **Recommend both**: none is client-specific, and the standard bans client branches in feature
code (`clients.md` §3).

**D11. Shared bank module.** Options: LibKa0s module in this run (tag + re-vendor ~20 repos) vs addon-local now + a
LibKa0s issue. **Recommend addon-local + issue** (§3).

**D12. Two-word names in narrow surfaces.** Options: widen (BL char dropdown 140 px → ~180 px; Insights bar label) or keep
widths and truncate with the whole name in a tooltip. **Recommend truncate + tooltip, widen the dropdown** (the standard
allows either, `forever-quirks.md` §4).

**Assumed, not asked (precedent):** no version bump, no tag, no release in the port (`patterns.md` §2.2, §2.18); one
feature branch `feat/2026-11-21-forever-port-lh-bl` in LootHistory, BankLedger, WowAddonStandards and CommonTasks;
plan bundle in CommonTasks (cross-repo).

### 4b. Facts that need an in-game probe (owner, WoW Forever, ~24 h)

Each probe is pasteable chat. Safe default = what the build ships until the probe lands.

| # | Fact | Procedure | Safe default |
|---|---|---|---|
| P1 | Which interaction type a banker sends, and whether bank tabs report 0 slots at open | Away from a bank: `/run local f=CreateFrame("Frame") f:RegisterEvent("BANKFRAME_OPENED") f:RegisterEvent("PLAYER_INTERACTION_MANAGER_FRAME_SHOW") f:SetScript("OnEvent",function(_,e,a) local function s() local n=0 for i=6,14 do n=n+C_Container.GetContainerNumSlots(i) end return n end print(e,a,s()) C_Timer.After(1,function() print("+1s",s()) end) end)` then talk to the banker. Expect `PLAYER_INTERACTION_MANAGER_FRAME_SHOW 8` (Banker) or `67` (CharacterBanker). | LH arms on Banker, CharacterBanker and AccountBanker; both addons apply the 0-slot readiness guard. |
| P2 | Bank model answers | At the banker: `/run print(C_Bank.ShouldUsePlayerBagsInBank(), C_Bank.CanViewBank(0), C_Bank.CanViewBank(2), C_Bank.FetchNumPurchasedBankTabs(0), C_Bank.FetchNumPurchasedBankTabs(2), C_Bank.FetchMaxNumBankTabs(0), C_Bank.FetchDepositedMoney(2))` and `/run for i=-3,23 do local n=C_Container.GetContainerNumSlots(i) if n>0 then print(i,n) end end` | Warband Retail-only by declaration; bank = ids 6..14 by name. |
| P3 | Keyring readable anywhere; keys bankable | `/run print(C_ActionBar.ShouldShowKeyring(), HasKey and HasKey(), C_Container.GetContainerNumSlots(-1)) for i=1,C_Container.GetContainerNumSlots(-1) do local x=C_Container.GetContainerItemInfo(-1,i) if x then print(i,x.hyperlink,x.stackCount) end end`; then try to drag a key into the bank. | Keyring in the bags group; no keyring↔bank pairing. |
| P4 | Self loot line, sender form, loot source | `/run local f=CreateFrame("Frame") f:RegisterEvent("CHAT_MSG_LOOT") f:RegisterEvent("LOOT_OPENED") f:SetScript("OnEvent",function(_,e,...) if e=="LOOT_OPENED" then for i=1,GetNumLootItems() do print(i,GetLootSlotLink(i),GetLootSourceInfo(i)) end else local t,p=... print((t:gsub("\124","\124\124")),p,(select(5,...)),(select(12,...))) end end)` then loot a mob (solo and in a dungeon). | Current parsers (strings identical); GUID decode as on Retail. |
| P5 | Currency list and transfer record shape | `/run for i=1,C_CurrencyInfo.GetCurrencyListSize() do local c=C_CurrencyInfo.GetCurrencyListInfo(i) print(i,c.name,c.isHeader,c.isAccountWide,c.isAccountTransferable,c.quantity) end`; after a transfer to an alt: `/run local l=C_CurrencyInfo.FetchCurrencyTransferTransactions() local t=l and l[#l] if t then for k,v in pairs(t) do print(k,v) end end` | Account currencies → account holder; transfer destination used as-is (no realm) on regional names; a missing field degrades to no pairing. |
| P6 | Guild vault exists and reads | At a guild vault: `/run print(GuildBankFrame and GuildBankFrame:IsShown(), GetNumGuildBankTabs(), GetGuildBankMoney(), GetCurrentGuildBankTab())` | Guild bank on both clients, dormant if never opened. |
| P7 | Trade partner and mail recipient forms | In an open trade: `/run print(UnitName("NPC")) print(GetUnitName("NPC",true))`. Before sending mail to an alt: `/run hooksecurefunc("SendMail",function(r) print("["..tostring(r).."]") end)` | Partner via UnitCharacterName; recipient kept whole, matched against "First Surname" holders. |
| P8 | Group roll line | In a group roll you win: watch the P4 frame print the `\|HlootHistory:` line. | Roll-won pattern takes the `%s` capture; the stamp works either way. |
| P9 | Money text global | On **both** clients: `/run print(GetCoinTextureString, C_CurrencyInfo.GetCoinTextureString and C_CurrencyInfo.GetCoinTextureString(123456))` | Prefer `C_CurrencyInfo.GetCoinTextureString`, then the global, then the text fallback. |
| P10 | Socketed bank-bag reads | At the banker: `/run for i=1,9 do local l=ItemLocation:CreateFromBagAndSlot(-2,i) if C_Item.DoesItemExist(l) then print(i,C_Item.GetItemLink(l)) end end` and `/run for i=1,9 do local x=C_Container.GetContainerItemInfo(-2,i) print(i,x and x.hyperlink) end` | Sockets not scanned (D9 a). |
| P11 | Instance difficulty ids | In a 5-man and a raid: `/run print(GetInstanceInfo())` | Difficulty stored raw as today; no label change. |
| P12 | Ported addons load clean | After the branch is on the Forever install: `/lh diagnostics`, `/bl diagnostics`, `/bl debug scan` at a banker (BL's probe tool, `BL/modules/Ledger_Diagnose.lua:20-137`) | n/a: owner smoke. |

---

## 5. Draft item list (resumable plan)

Branch `feat/2026-11-21-forever-port-lh-bl` in every repo touched. Bundle
`Ka0sAddonsCommonTasks/docs/2026-11-21-LOOTHISTORY_BANKLEDGER_FOREVER_PORT/` (00_DESIGN, 01_EXECUTION_PLAN,
06_SMOKE_TESTS, 07_EXECUTION_RECORD, RESUME.md, checkpoints.tsv, inputs/{research/, owner-rulings.md},
plan-data/{items.tsv, exceptions.tsv, resume-state.sh}), QUICKCOMMS_FOREVER_EMOTES shape (`patterns.md` §3).
Done = a commit whose subject starts `<ID>: `. The roster rows sit in M3 but are merged in the same finalize as the
ports they describe, which is how a separate-repo flip meets `clients.md` §2's "same change" (precedent: WS-FP12 beside DW-FP12).

| id | milestone | repo | title | deps |
|---|---|---|---|---|
| CT-00 | M0 | Ka0sAddonsCommonTasks | Plan bundle: research inputs, owner rulings, design, items, resume-state, smoke sheet | — |
| LH-01 | M1 | LootHistory | CompatClient: client routing and identity readers from LibKa0s-Compat; Compat header no longer Retail-only | CT-00 |
| LH-02 | M1 | LootHistory | Forever-shaped mock profile (BagIndex 6..23, Keyring, two-word UnitName, RegionalNames, CanViewBank(2) false); fixtures read per-profile helpers | LH-01 |
| LH-03 | M1 | LootHistory | Names: PlayerRecordKey (Retail Name-Realm unchanged), TradePartnerName, QualifyName and currency-transfer destination on regional names | LH-02 |
| LH-04 | M1 | LootHistory | Default skin per client (NS.DEFAULT_SKIN) | LH-01 |
| LH-05 | M1 | LootHistory | Sample identity, test data and sim seeds per client (Sim.Sample(ClientKey()), Forever classes/zones/items) | LH-03 |
| LH-06 | M1 | LootHistory | Warband bank Retail-only: tabs and warbandMoney parts, WARBAND reasons, ACCOUNT_MONEY/tab-slot events, Holdings column, copy; account holder label per client (D2) | LH-02 |
| LH-07 | M1 | LootHistory | Retail-only sources per client: MPLUS + keystone context + Insights breakdown + sim key scenario, BONUS_ROLL, MILLING, PROSPECTING, DECONSTRUCT, warband bound filters (D4) | LH-02 |
| LH-08 | M1 | LootHistory | Forever bank model: bank readiness guard, CharacterBanker, Forever re-read cues, Keyring in bags (D5) | LH-06 |
| LH-09 | M1 | LootHistory | Capture hardening: roll-won takes the link capture; money text via C_CurrencyInfo (D10) | LH-02 |
| LH-10 | M1 | LootHistory | Two-word name surfaces: holder labels, filters, Holdings, Timeline sized or truncated with tooltip; wowheadLink per client (D8) | LH-03 |
| LH-11 | M1 | LootHistory | Retail and WoW Forever (120105, 16001): TOC, README badge/sentence, CLAUDE gate, DEPENDENCIES, testing.md, ARCHITECTURE per-client table + doc map, forever-quirks.md, compat-layer/module-map/schema docs, TOC/README tests, test-cases.md | LH-04, LH-05, LH-07, LH-08, LH-09, LH-10 |
| LH-12 | M1 | LootHistory | smoke-tests.md WoW Forever section and probe sheet P1-P12 | LH-11 |
| STD-01 | M3 | WowAddonStandards | LootHistory roster row Retail · Forever | LH-11 |
| BL-01 | M2 | BankLedger | CompatClient: client routing and identity readers; Compat header | CT-00 |
| BL-02 | M2 | BankLedger | Forever-shaped mocks; sample identity per client (SAMPLE_FALLBACK twin, Sim.Sample(ClientKey()), tests' conventional()): the 5 forever failures | BL-01 |
| BL-03 | M2 | BankLedger | Identity: PlayerRecordKey through Compat.PlayerName/Util.PlayerKey and SimWorld buildChars | BL-02 |
| BL-04 | M2 | BankLedger | Default skin per client | BL-01 |
| BL-05 | M2 | BankLedger | Warband Bank Retail-only: StoreOrder/STORE_OPTIONS/CONTEXT_STORES/MONEY_STORES per client, settings grid, copy, test mode, session preview, sim scenarios | BL-02 |
| BL-06 | M2 | BankLedger | Forever bank model: readiness guard, BAG_CONTAINER_UPDATE/BANK_TABS_CHANGED cues, Keyring in BAGS, `/bl debug scan` covers -2 sockets, CanViewBank, ShouldUsePlayerBagsInBank, interaction types | BL-05 |
| BL-07 | M2 | BankLedger | Test-mode and sim seeds per client: Forever classes (no Evoker), bag-sized tabs, zones | BL-03 |
| BL-08 | M2 | BankLedger | Two-word name surfaces: char dropdown, ShortChar bars, char column, tooltips | BL-03 |
| BL-09 | M2 | BankLedger | Wowhead column per client (D8); money text via C_CurrencyInfo (D10) | BL-01 |
| BL-10 | M2 | BankLedger | Retail and WoW Forever (120105, 16001): TOC, README, CLAUDE gate, DEPENDENCIES, testing.md, ARCHITECTURE per-client table + doc map, forever-quirks.md, compat-layer docs, TOC/README tests, test-cases.md | BL-04, BL-06, BL-07, BL-08, BL-09 |
| BL-11 | M2 | BankLedger | smoke-tests.md WoW Forever section and probe sheet | BL-10 |
| STD-02 | M3 | WowAddonStandards | BankLedger roster row Retail · Forever | BL-10 |
| CT-03 | M3 | Ka0sAddonsCommonTasks | Execution record, smoke sheet roll-up, LibKa0s issue text for a shared container-group reader (filed by the lead) | STD-01, STD-02 |
| LH-13 | M4 | LootHistory | Independent review (refs/notes/ka0s-review) and review fixes; automated-test bundle | LH-12 |
| BL-12 | M4 | BankLedger | Independent review and review fixes; automated-test bundle | BL-11 |
| CP-1 | M4 | all | Checkpoint: both profiles green in both addons, luacheck 0/0, 1500-line cap, TOC `120105, 16001`, heads recorded in checkpoints.tsv; push feature branches if authorized | LH-13, BL-12, CT-03 |

Post-run, owner-gated: probes P1-P12 and the WoW Forever smoke; any probe that contradicts a safe default becomes a
follow-up item; `/dev-copilot:finalize` merges `--no-ff` in dependency order (WowAddonStandards, LootHistory, BankLedger,
CommonTasks) on the owner's go-ahead.

---

## Critic

Completeness pass, 2026-11-21. I spot-checked 16 claims against source. **V** = read at the cite, **I** = inferred.

### Spot checks that held (V)
1. `Util.PlayerKey` = `UnitName("player")` .. "-" .. realm with whitespace stripped (`LH/core/Util.lua:6-12`).
2. The trade key reads `local name, realm = UnitName("NPC")` (`LH/core/Compat.lua:1048-1056`). The function is named **`Compat.TradeTargetKey`**, so the plan should not call it `TradePartnerName` (§2b names a function that does not exist).
3. `LatestCurrencyTransfer` appends the realm (`LH/core/Compat.lua:1063-1072`).
4. `READABLE_ON` lists only Banker, AccountBanker, MailInfo and Auctioneer (`LH/modules/Reconciler.lua:54-59`).
5. `LOOT_ROLL_YOU_WON` takes the `|HlootHistory:%d|h` prefix on Forever (`K/gs_forever.lua:13940`) and not on Retail (`K/gs_live.lua:13445`).
6. Forever `Enum.BagIndex` runs Keyring=-1, ReagentBag=5, CharacterBankTab_1..9=6..14 and AccountBankTab_1..9=15..23 (`FAPI/BagIndexConstantsDocumentation.lua`).
7. The Camelot bank adds pages only behind `CanViewBank` (`FV/Blizzard_UIPanels_Game/Camelot/BankFrame.lua:114-133`).
8. Banker, CharacterBanker and AccountBanker are all registered (`Mainline/BankFrameTemplates.lua:126-134`). That file is `[Family] [AllowLoadGameType mainline]` (`Blizzard_UIPanels_Game.toc:137`), and `mainline` includes camelot, because line 140 needs `[ExcludeLoadGameType camelot]` to drop it (I from the TOC convention).
9. ChallengesUI is `AllowLoadGameType: standard, mists`. `standard` excludes camelot, because 11 TOCs spell out `standard, camelot` (git grep count, I from the convention). The claim holds, but `C_ChallengeMode.*` and `CHALLENGE_MODE_*` **are** in `api-forever.tsv`. Gating MPLUS is a feature decision, not an error-safety need.
10. BagSync's "bank isn't always loaded yet" (`FA/BagSync/wireframe/events.lua:300`), its all-tabs-zero guard (`scanner.lua:463-478`) and "account bank API but it's locked" (`core.lua:185`) all read as reported.
11. BL `Compat.PlayerName` (`BL/core/Compat.lua:36-42`), the group patterns (`BL/core/Constants.lua:118-125`), `MONEY_STORES` and `CONTEXT_STORES`/`StoresFor` (`BL/modules/Ledger.lua:20,30-47`) all match the report.
12. AceDB 40 gives charKey `name.." "..surname` and realmKey = ruleset under `RegionalUniqueNamesEnabled` (`BL/libs/AceDB-3.0/AceDB-3.0.lua:263-277`). Both addons use `db.global` and `db.profile` only, no `db.realm` (grep), so the shared ruleset realmKey cannot collide.
13. The roster rows read `Retail (port pending)` (`STD/ADDONS.md:21,27`).
14. Every `C_*` call in both addons' core/ and modules/ is present in `api-forever.tsv` (24 LH + 10 BL names, grep, V). So are all registered events. `GUILDBANK_FRAME_SHOWN/HIDDEN` are BL's own pseudo-events (`BL/modules/Ledger.lua:811-815`), not client events.

### Wrong or overstated
- **§1a.7, the Sim.lua:170 claim is wrong.** `SELF_LINE.CHAT_MSG_LOOT` uses `ParseRollWon` only as a truth predicate (`LH/modules/Sim.lua:169-170`), like the Collector. The roll-won capture fix is defensive only. No reader consumes the wrong capture today.
- **D4, the WARBAND/WARBAND_UE bound filter should not be dropped on Forever.** Forever ships account binding under its own wording: `ITEM_BIND_TO_ACCOUNT = "Binds to Account"` and `ITEM_ACCOUNTBOUND = "Account bound"` (`K/gs_forever.lua:12666-12679`, `gsdiff-loot.txt`). `Compat.ScanBound` matches the globals first (`LH/core/Compat.lua:263-297`), so Forever heirloom-style items **are** captured as WARBAND. The right fix is to keep the states and relabel them "Account" on Forever, the same as D2. Dropping them would hide real data.
- **§2c, the "every BANK id 0 slots" guard is too weak.** BagSync only guards "none have slots". A partly loaded bank (tab 1 ready, socketed tabs 2..9 still 0) slips through. LH's drift pass would then write those tabs' contents as an UNTRACKED loss, and the gain on the next read. A guard per container (a container that had slots last visit and now reads 0 is "not ready") is safer (I).
- **AccountBanker arms the character bank.** BagSync v20.41: "Opening the bank at a Warband-only banker will no longer save your character bank, since your character bank can't be viewed there" (`FA/BagSync/CHANGELOG.md:9`, V-3P). LH arms the `bank` part on AccountBanker (`Reconciler.lua:56`), on Retail too. The readiness check should ask `C_Bank.CanViewBank(Enum.BankType.Character)`, not count slots alone. This is a latent Retail bug, and it belongs under D10.
- **D5's "Retail -1 reads 0 slots" is unverified, and it matters.** Retail's enum also has `Keyring = -1` (`ui/retail/.../BagIndexConstantsDocumentation.lua`), so `^Keyring$` adds -1 to BAGS **on Retail** too. Before 11.2, -1 was the legacy bank container. If Retail still answers -1 at a banker, every Retail bank visit moves items between "bags" and "bank". P3 must also run on Retail. Until then, the safe default is "Keyring in bags only when `ClientKey()=="forever"`", or better, as a per-client container table picked once.
- **The money-text claim is unverified, and the fallback is wrong.** Forever has no bare `GetCoinTextureString`, but it does ship `GetMoneyString` (`FV/Blizzard_SharedXML/FormattingUtil.lua:72`), which is a better fallback than the "Ng Ns Nc" text. The Ketho fn dumps list C functions only, so a missing Lua-defined global there proves nothing about Retail. P9 stands.

### Missing from the code maps
- **Seeded lists with no per-client twin (clients-§5, §10).** LH's `DECONSTRUCT_ID` (about 30 spell ids) and `NAME_SEEDS` (13262, 51005, 434926, 31252, 225904; `LH/modules/Attribution.lua:33-60`) are seeds. They need two lists picked once by `ClientKey()`, and the Forever list must be derived from `wowf` DB2, not filtered from Retail's. No plan item covers this.
- **Perf risk.** If 51005, 434926, 31252 or 225904 do not resolve on Forever, `GetSpellName` returns nil. `allSeedsResolved` is then always false (`Attribution.lua:86-100`), so no negative result is ever memoized, and **every player cast** re-resolves five seeds (`Attribution.lua:342-355`). An empty Forever list by decision avoids this.
- **AH price providers** (`LH/core/Constants.lua:213`): Auctionator is on Forever (`FA/Auctionator`). TSM and Oribos Exchange are unknown there (I). The default priority order and the capture menu may need per-client defaults.
- **Live Retail enum vs the mock.** LH's mock BagIndex is "as 12.0.7 ships it" (`LH/tests/wow_mock.lua:61`). The live 12.1.5 Retail enum is 9+9 tabs. The Retail mock should be re-checked as well as the new Forever one.

### Missing plan items
- `docs/forever-probes.md` in each addon (DW precedent `DropWatcher/docs/forever-probes.md`) to hold P1-P12 and their results. A probe sheet inside smoke-tests.md mixes owner smoke with research.
- An explicit present/absent test per declared feature on each profile (clients-§6: "present where declared, absent where not"). LH-11 and BL-10 bury this.
- The CLAUDE.md gate line must name both runs, `lua tests/run.lua` and `KA0S_KIT_CLIENT=forever lua tests/run.lua` (DW `CLAUDE.md:39`). The automated-tests bundle should run both profiles too.
- Smoke checks that a Retail-only feature is **absent** on Forever: no Warband checkbox, no Mythic+ filter, no keystone Insights (clients-§6).
- `midnight-quirks.md` stays. Adding `forever-quirks.md` must land in the same change as the roster flip (`clients.md:91`). Each addon's ARCHITECTURE doc map should drop the "Not applicable" row for forever-quirks.
- `.pkgmeta` and packaging: confirm nothing in the release metadata pins Retail only (`packaging.md`). There is no CHANGELOG.md in either repo, so the README Version History is untouched (no bump).
- A seed-research item: derive or rule the Forever deconstruct seeds, or record "empty by decision" with the reason.
- An `idempotent first-visit` test: a fresh Forever DB's first bank read is genesis with no rows (`Reconciler.lua:633-634`). The 0-slot risk bites on the **second and later** visits. Tests should cover visit 2 with a partly ready bank.

### Questions the open-questions list lacks
- **D13. Merge gate.** Should the roster flip and merge wait for P1, P2 and P3 (the bank-model probes), given the build cannot prove the bank guard? Recommend building and pushing the branch, but holding the finalize until the bank probes and the Forever smoke pass.
- **D14.** The Retail behavior changes under D10 (CanViewBank gating, CharacterBanker, Keyring) touch the owner's live Retail data. Should they be split into their own commits so they can be bisected?
- **D15.** Should the Forever deconstruct seeds be empty by decision, or derived from wowf DB2 now (Disenchant 13262 exists in vanilla; Milling and Prospecting do not, I)?

### Risks of building without probes
The highest risk is wrong bank readiness. It writes bogus UNTRACKED loss and gain rows into a ledger the owner trusts, and rows are append-only history. Mitigation: a per-container not-ready guard plus a CanViewBank check, both with tests. Next is the Retail keyring change (-1). Lowest are the cosmetic ones (labels, money text, roll capture).
