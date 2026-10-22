# Ka0s Loot History: in-game simulator (`/lh sim`), requirements

- **Repo:** `../LootHistory` (master @ 8c79b23, v1.5.0, vendors LibKa0s **v1.71.0**). Issue: LootHistory#37 (open, `state:triaged`, `severity:low`).
- **Builds on:** LibKa0s v1.75.0, specifically `LibKa0s-Sim-1.0` (#54) and its shared step panel (#53), as decided by the owner.
- **Reference:** DropWatcher `core/SimSeam.lua`, `modules/Sim*.lua` (3,412 lines) and its two specs, `docs/superpowers/specs/2026-10-11-drop-watcher-simulator-design.md` and `-sim-feedback-design.md`.
- **Read-only analysis.** This document is the requirements. The dated spec and the checkpointed plan belong in LootHistory under `docs/superpowers/specs/` and `docs/superpowers/plans/`.

---

## 0. Corrections to issue #37 and to the prior analysis

1. **#37 "Build on Sim-1.0 once it ships".** It now ships in v1.75.0. LootHistory still vendors **v1.71.0** (CLAUDE.md "Vendored LibKa0s"), so re-vendoring to v1.75.0 through `/dev-copilot:wow-revendor-libka0s` comes first. That re-vendor also brings W.SearchBox, W.TestStrip and Item.BonusIDsFromLink, which LootHistory adopts in the same run.
2. **The analysis's "about 23 direct client reads sit outside core/Compat.lua".** That count is true of the whole addon. Most of those reads are UI (`CreateFrame`, `C_Texture` atlases) or the clock (`time`, `GetTime`, `date`), and a simulator does not need them. Only a short list blocks the simulator; §3.1 gives it. The analysis was right that there is **no single dispatch table**. Capture events are registered in four places on four different targets (§3.2).
3. **#37 lists "items whose links carry bonus data" and "Mythic+ runs".** Both are covered below. The "vendor and disenchant session" and "trade" scenarios need the **hook** path as well as events. Five read-side hooks and thirteen loss-side hooks run through `hooksecurefunc`, and the issue does not mention them. A simulator that only fires events cannot exercise VENDOR, MAIL/AH, CONTAINER, QUEST, SELL/BUY/REPAIR, AH_POST_FEE/AH_BUY/AH_SOLD, MAIL_SEND/ALT_MAIL or DESTROY (§2.3).
4. **The "session-only store" is three stores in LootHistory, where Drop Watcher has one.** LootHistory writes `db.global.history` (core/Database.lua:585-604), `db.global.holdings` (modules/Holdings.lua:36-41) and `db.global.daily` (modules/Rollup.lua:20-25). The Reconciler also reads the live history directly (modules/Reconciler.lua:489). All four must be redirected (§4).

---

## 1. Goal and the one principle

`/lh sim` runs the **real capture engine** against an invented world, solo and outside an instance, so capture and ledger changes can be tested between live sessions.

- **Inputs invented at the edges:** a bag, bank, warband, mail and auction inventory, loot windows, chat lines, encounters, keys, interaction frames, hook calls and the player's own actions.
- **Everything between the edges runs as it does live:** `Util.ParseSelf*`, `Attribution` (stamp and consume), `Collector` (gate, record, claim), `Reconciler` (dirty, debounce, scan, plan, hold, commit), `Escrow`, `Ledger.PickReason`, `Holdings`, `Rollup`, `AuctionPrice:GatherAll`, the Browser, Insights, Holdings and Timeline tabs.

**The principle (copied from Drop Watcher spec §1):**
- The simulator never calls `Database:Add`, `Holdings:Apply*`, `Attribution:Stamp` or `R:Write` itself.
- It never writes a source, reason or row.
- If a simulated row reads `AH_SOLD`, then `Ledger.PickReason` decided it.

Test mode (`BrowserTable:SetTestMode`, modules/BrowserTable.lua:682-699) is the opposite: it shows fixed preview data. The two modes are mutually exclusive.

---

## 2. The world it simulates

### 2.1 World state (session-only, `State.sim.world`)

| Part | Shape | Answers |
|---|---|---|
| `bags[bagID][slot]` | `{ itemID, link, count, hasLoot }` | carried bags (`C.BAG_IDS`) |
| `bank[bagID][slot]`, `tabs[bagID][slot]` | same | character bank (`C.BANK_IDS`), warband tabs (`C.WARBAND_TAB_IDS`) |
| `equipped[slot]` | `{ itemID, link }` | `C.EQUIP_SLOTS` plus bag slots |
| `money`, `warbandMoney` | copper | purse, warband bank gold |
| `currencies` | `{ {id, quantity, accountWide} }` | the token list |
| `inbox[i]` | `{ sender, subject, money, items = { {itemID, link, count} } }` | mailbox |
| `sendMail` | `{ items = {id=n}, money }` | staged Send Mail frame |
| `owned[i]` | `{ itemID, link, quantity, status }` | owned auctions |
| `loot` | `{ guid, n }` | the open loot window's first source GUID and slot count |
| `instance` | `{ party = bool, keystone = level\|nil, zone, subzone, mapID }` | situation reads |
| `combat` | bool | the Reconciler's lockdown gate |
| `trade` | `{ target = "Name-Realm" }` | trade partner |
| `quest` | `{ id }` | quest frame |
| `targeting` | bool | `SpellIsTargeting` |

- **Seeded deterministically** from the scenario fixture (`seed` optional). It does not mirror the player's real bags: mirroring would make the end-to-end suite non-deterministic, and it would show the player's real items inside a simulated history.
- **Items are real.** The fixture uses current-expansion item and currency IDs, so `GetItemInfo`, `GetItemExtras`, `ScanBound` and the AH price providers answer for real. Uncached links fall back to the link's own name and color (core/Compat.lua:170-171), and that fallback is exercised too.
- Links are built as `|cffXXXXXX|Hitem:<id>::::::::<lvl>:::<nBonus>:<bonus…>|h[Name]|h|r`. At least one fixture link carries bonus IDs (#37's "items whose links carry bonus data"). That link is also where Item.BonusIDsFromLink, newly adopted by LootHistory, gets exercised.
- **A simulated own alt.** `Simalt-<realm>` is seeded into the **session** holdings store, so `Attribution:IsOwnAlt` (modules/AttributionOut.lua:111-113) answers true for the ALT_MAIL and ALT_TRADE steps.

### 2.2 Client reads that need providers (all `NS.Compat` members, through the Sim-1.0 seam)

| Compat member (core/Compat.lua) | Reader | Provider answers |
|---|---|---|
| `GetContainerNumSlots` :632, `GetContainerSlot` :637 | Scanner :15-16 | world bags, bank and tabs |
| `GetInventoryItem` :661 | Scanner :37/:41 | world equipped |
| `GetMoney` :647, `GetWarbandMoney` :654 | Scanner :58-59, `R:IsReadable` :28 | world money |
| `ListCurrencies` :722 (**guarded**, see §2.4) | Scanner :50 | world currencies |
| `ScanInbox` :785, `GetMailHeader` :106, `ReadSendMail` :801 | Escrow scan, `StampMail` :385, `OnSendMail`/`OnTakeInboxMoney` | world inbox and sendMail |
| `ScanOwnedAuctions` :814, `ItemLocationID` :828 | Escrow scan, `OnPost` | world owned auctions; the ItemLocation token the driver passes |
| `ContainerItemHasLoot` :57, `IsSpellTargeting` :84 | `OnContainerItemUse` :321-324 | world slot `hasLoot`, world `targeting` |
| `CurrentQuestID` :76 | `StampQuestReward` :405 | world quest |
| `GetActiveKeystoneLevel` :29, `InPartyInstance` :38 | `OnChallengeModeStart/Completed/OnZoneChanged` :247-290 | world instance |
| `InCombatLockdown` :681 | `R:Flush` :654, `R:LoginScan` :678 | world combat |
| `TradeTargetKey` :859 | `OnTradeAcceptUpdate` :375, `OnTradeAccept` | world trade |
| `LatestCurrencyTransfer` :871 | Reconciler plan step | world transfer (social scenario) |
| **new** `NumLootItems`, `LootSourceGUID(slot)` | `OnLootOpened` (today bare, Attribution.lua:206-208) | world loot |
| **new** `Zone`, `PlayerMapID` | `NS.Zone`/`NS.PlayerMapID` (today LibKa0s-Env, EnvSetup.lua:86-110) | world instance zone, subzone and map |

**Answered live** (wrapped, no provider). These read the real player or real items, and live is the correct answer because the simulated player is the real player:

- Item reads: `GetItemInfo`, `GetItemExtras`, `ScanBound`, `ItemBindState`, `GetItemTypeInfo`, `GetItemSellPrice`, `GearItemLevel`, `IsConsumable`.
- Spell and currency reads: `GetSpellName`, `GetCurrencyInfoFromLink`, `CurrencyCategory`, `CurrencyQuality`, `CurrencyName`, `CurrencyBound`, `CurrencyIsAccountWide`, `ListedCurrencyID`, `CurrencyListChanged`.
- `PlayerClassFile`.

`ListedCurrencyID` also consults `NS.Holdings:Get`, which resolves to the session store during a simulation (§4), so the world's currencies count as "held".

**Never wrapped (PURE):**
- Text and parse helpers: `FoldNBSP`, `IsAuctionHouseMail`, `DecodeGUID`, `BindState`, `BestBound`, `CurrencyLinkID`, `AuctionMailKind`, `CurrencySourceName`, `InteractionType`.
- The tooltip `Show*`/`HideTooltip` family. These are display only.
- The four hook installers: `HookUseContainerItem`, `HookGetQuestReward`, `HookSecure`, `HookSecureMember`. They run once at Enable, never during a simulation.
- **New members:** `InInstance`, `InGroup` and `PlayerInCombat` are *read only through `seam:Live`* by the refusal and the auto-stop. They are wrapped but given no provider, so they always answer live.

### 2.3 Events, with their real payload shapes

The world is mutated **before** the event fires, the same order the client uses. Each driver fires a burst.

| Event | Payload the driver fires | Handler(s) today |
|---|---|---|
| `CHAT_MSG_LOOT` | full 17-arg chat shape. `text` = `LOOT_ITEM_SELF[_MULTIPLE]`, `LOOT_ITEM_PUSHED_SELF*`, `LOOT_ITEM_BONUS_ROLL_SELF*`, `LOOT_ROLL_YOU_WON` formatted from the **same** global accessors the parser uses (`lootGlobals()`, core/Util.lua:160). `playerName` = own name, `guid` = player GUID | Collector:OnChatMsgLoot :198 |
| `CHAT_MSG_CURRENCY` | `CURRENCY_GAINED[_MULTIPLE]` (`currencyGlobals()`, Util.lua:237) | Collector :300 |
| `CHAT_MSG_MONEY` | `YOU_LOOT_MONEY` / `LOOT_MONEY_SPLIT` with `GOLD/SILVER/COPPER_AMOUNT` text (Util.lua:331-342) | Collector :332 |
| `LOOT_OPENED` | `(autoLoot, isFromItem)`. The GUID comes from the provider: `Creature-0-…-<npcID>-…`, `GameObject-…`, `Item-…` | Attribution:OnLootOpened :197 |
| `ENCOUNTER_START` / `ENCOUNTER_END` | `(encounterID, encounterName, difficultyID, groupSize[, success])` | Attribution :222/:233 |
| `CHALLENGE_MODE_START` / `_COMPLETED` / `_RESET` | `(mapID)` / none / `(mapID)` | Attribution :247/:254/:292 |
| `ZONE_CHANGED_NEW_AREA` | none | Attribution :271 |
| `UNIT_SPELLCAST_SUCCEEDED` | `("player", castGUID, spellID)`. Disenchant 13262; Milling and Prospecting by ID | Attribution:OnSpellSucceeded :365 (unit frame) |
| `QUEST_TURNED_IN` | `(questID, xp, money)` | Attribution :395 |
| `TRADE_ACCEPT_UPDATE` | `(1, 1)` | Attribution :373 **and** AttributionOut:OnTradeAccept :117 |
| `PLAYER_INTERACTION_MANAGER_FRAME_SHOW/HIDE` | `(Enum.PlayerInteractionType.X)` for Merchant, MailInfo, Auctioneer, Banker, AccountBanker | AttributionOut:OnInteraction :44 **and** R:OnInteraction :58 |
| `MAIL_SEND_SUCCESS`, `MAIL_FAILED` | none / `(itemID)` | AttributionOut :75/:82 |
| `BAG_UPDATE(bagID)`, `BAG_UPDATE_DELAYED`, `PLAYER_EQUIPMENT_CHANGED(slot, hasCurrent)`, `PLAYER_MONEY`, `ACCOUNT_MONEY`, `CURRENCY_DISPLAY_UPDATE(id, quantity, change, gainSource, lostSource)`, `PLAYERBANKSLOTS_CHANGED(slot)`, `PLAYER_ACCOUNT_BANK_TAB_SLOTS_CHANGED(tab)`, `MAIL_INBOX_UPDATE`, `OWNED_AUCTIONS_UPDATED`, `CURRENCY_TRANSFER_LOG_UPDATE`, `PLAYER_REGEN_ENABLED` | as listed | R:OnEvent :143 (`EVENT_HANDLERS` :94-125) |

**Hooks (post-hooks):**
- The simulator never calls the hooked function itself (§2.4). It applies that function's effect to the world, then calls the hook rows (§3.3) with the real argument shapes.
- Read side (Attribution.lua:463-475): `BuyMerchantItem(index, qty)`, `TakeInboxItem(mailIndex, attachIndex)`, `AutoLootMailItem(mailIndex)`, `UseContainerItem(bag, slot)`, `GetQuestReward(choice)`.
- Loss side (AttributionOut.lua:143-162): `RepairAllItems`, `BuyMerchantItem`, `BuybackItem`, `DeleteCursorItem`, `SendMail(recipient, subject, body)`, `TakeInboxMoney(index)`, `C_AuctionHouse.PostItem(itemLocation, duration, qty, …)`, `PostCommodity`, `PlaceBid`, `ConfirmCommoditiesPurchase`, `C_TradeSkillUI.CraftRecipe/CraftSalvage/CraftEnchant`.
- `BuyMerchantItem` has **two** rows (StampVendor and StampOut BUY), and both run, in that order.

### 2.4 Guarded members (anything that acts on the world)

LootHistory almost never acts on the world. This is a real difference from Drop Watcher, which sends chat, inspects players and opens trades.

- **`ListCurrencies` is the only Compat member that changes client state.** It expands and collapses the player's Currency-tab headers (core/Compat.lua:697-728). It is **guarded**: while a simulation runs it answers only the world's list (or `{}`) and never reaches `C_CurrencyInfo.ExpandCurrencyList`.
- **Hooked client functions are never called by the simulator.** These are `BuyMerchantItem`, `TakeInboxItem`, `SendMail`, `PostItem` and the rest. They are not Compat members, so the rule lives in `modules/SimDrivers.lua` and a static test checks it (§8): the Sim files contain no call to any hooked name.
- **Nothing leaves the client.** LootHistory sends no chat or addon messages, and the Export window only shows text.

### 2.5 Safety summary

- Saved data is never written (§4).
- No client state changes (§2.4).
- Only rows produced while the simulator is delivering carry `sim = true`. A *real* capture event during a simulation stops it first, then runs live (§5.3), so real data is never lost into the session log.

---

## 3. Refactors LootHistory needs first (the host contract)

These land as their own commits, before any Sim file, each with characterization tests and the green gate.

### 3.1 Route the simulator-relevant reads through `NS.Compat` (lesson DW-90)

DW-90 shows what goes wrong when a bare global is left unseamed: the simulator runs and silently records nothing. These are the reads that must move:

| # | Where | Today | Change |
|---|---|---|---|
| C1 | modules/Attribution.lua:206-208 | `GetNumLootItems()`, `GetLootSourceInfo(slot)` bare | new `Compat.NumLootItems()`, `Compat.LootSourceGUID(slot)` (presence-guarded, same answers) |
| C2 | core/EnvSetup.lua:86-110 (`NS.PlayerMapID`, `NS.Zone`) | LibKa0s-Env, not a Compat member, so the seam cannot reach it | new `Compat.Zone()` and `Compat.PlayerMapID()` delegating to Env (keeping the `""` contract, :95-104). `NS.Zone`/`NS.PlayerMapID` become call-time forwarders to the Compat members. Callers are unchanged: Collector :180/:188/:244/:253/:318/:325, `R.MakeRow` (Reconciler ~:455) |
| C3 | refusal and auto-stop reads | none exist (`IsInInstance`/`IsInGroup` are not in Compat; `Compat.InPartyInstance` only answers party) | new `Compat.InInstance()`, `Compat.InGroup()`, `Compat.PlayerInCombat()`, read through `seam:Live` |
| C4 | modules/Attribution.lua:463-472 | raw `hooksecurefunc("BuyMerchantItem"…)` etc. | install through `Compat.HookSecure` (already exists, :736) from the HOOK_ROWS table (§3.3) |
| C5 (hygiene, recommended) | modules/Collector.lua:181, :246; modules/BrowserTable.lua:639; modules/Browser.lua:1067 | `UnitClass("player")`, `UnitAffectingCombat` bare | `Compat.PlayerClassFile()` (exists :686) and `Compat.PlayerInCombat()`. Live answers are correct today, so this is not a blocker |

**Deliberately left bare:**
- `Util.PlayerKey`/`QualifyName` (UnitName, realm): the simulated player is the real player.
- `time()`, `GetTime()`, `date()`: the simulation uses the real clock. TTLs and holds then behave as they do live, and the kit's clock (`M.__now`) drives them headless.
- `CreateFrame`, atlases, `GetCoinTextureString`, `ItemSetup` cache warm-up, `EnvSetup` TOC metadata.

**Load-time capture check (already clean):** no file binds `local x = Compat.Member`. Grep shows only table captures (`local Compat = NS.Compat`), which read members at call time. The seam (Sim-1.0 `NewSeam`) wraps at file load, right after `core/Compat.lua`. A new test (§8) keeps it that way.

`core/Compat.lua` is 882 lines; it grows by about 45 and stays under the 1500-line cap.

### 3.2 One event dispatch table

Capture registrations live in four places today, on four targets:

- Collector:Enable: 3 chat events on the shared `NS.addon` bus (Collector.lua:344-349).
- Attribution:Enable: 9 events on the bus (Attribution.lua:432-440), plus a `RegisterUnitEvent` frame (:449-455).
- AttributionOut:EnableOut: 6 events on `__outEv` (AttributionOut.lua:170-178).
- Reconciler:Enable: 14 events on `__ev` (Reconciler.lua:688-719).

Two events fan out to two handlers each: `TRADE_ACCEPT_UPDATE` and `PLAYER_INTERACTION_MANAGER_FRAME_SHOW/HIDE`. Payloads are adapted ad hoc, for example `R:OnEvent(event, a1, _, a3, a4, a5)`.

**Requirement:** a new `core/Dispatch.lua` (~120 lines, after CoreSetup, above Modules).

- **The table.** `NS.EVENT_ROWS` is an ordered list of `{ event, owner, target, fn }`. `target` is `"bus"`, `"out"`, `"ledger"` or `"spell"`, and `fn(event, ...)` receives the client's full payload. Each module **appends its rows at file load** (the `R.SCAN_STEPS` precedent, Escrow.lua:20). Row order is TOC order, which matches today's stand-up order (core/LifecycleSetup.lua:177-184): Attribution, AttributionOut, Collector, Reconciler.
- **Registration.** `NS.RegisterRows(owner, targetObj, targetKey)` registers every matching row through `NS.SafeRegisterEvent`/`SafeRegisterUnitEvent`. It marks `row.registered = true` only on success, and `NS.UnregisterRows(owner)` clears the flag. Each module's Enable and Disable call these helpers in place of their hand-written lists. The (target, event) set must stay **identical**: tests/test_disabled.lua names the registrations and tests/test_attribution.lua:467-597 pins `Attribution.__events`.
- **The real-event wrapper.** Each registration calls `NS.Deliver(row, event, ...)`:
  ```lua
  if Sim.active and not Sim.delivering then return NS.SimOnRealEvent(row, event, ...) end
  return row.fn(event, ...)
  ```
  With no simulation running, that costs one boolean test per real event, the same cost as Drop Watcher's seam. The Shape-A perf brackets stay inside the handlers, so tests/perf.lua's `Collector._lootLine` baseline is unchanged.
- **Simulated delivery.** `Sim.Fire(event, ...)` uses the host `deliver` callback to walk `NS.EVENT_ROWS` in order and `pcall` every row whose `registered` is true. Fire therefore delivers to exactly the handlers the client would call. When `trackLedger` is off, the Reconciler rows are unregistered and are not called.

### 3.3 One hook table

`NS.HOOK_ROWS` is an ordered list of `{ name, member?, fn }`, appended at file load by Attribution (5 rows) and AttributionOut (13 rows). It is installed **once per session** through `Compat.HookSecure`/`HookSecureMember`, keeping the `_hooked`/`_outHooked` latches and the stood-down gate in the bodies, as slash-commands-§7 requires.

- Each installed hook calls `NS.DeliverHook(row, ...)`, which applies the same real/simulated split as §3.2.
- The simulator plays a hook as `Sim.Fire("hook:<name>", ...)`. Its `deliver` callback recognises the `hook:` prefix and walks `NS.HOOK_ROWS`. Sim-1.0 needs no hook concept for this.

### 3.4 Smaller host fixes

- **Per-handle cancel for `NS.After`.** core/LifecycleSetup.lua:61-88 only offers `NS.CancelDeferrals()`, which cancels everything. Add `NS.CancelDeferral(h)` so the simulator's stop can cancel `R._pending` (Reconciler.lua:43-46) and `R._recheck` without killing the login deferrals.
- **Split `R:ResetState()`** out of `R:DisableCapture` (Reconciler.lua:723-733): dirty, readable, claims, recent, memo, pendingCur/curGain/curLoss, holds and timers, without unregistering. Do the same for Attribution: a `ResetContexts()` taken from Attribution:Disable :494 plus AttributionOut:DisableOut :188-191 (lootContext, encounter, keystone, outContext, pendingMail, soldMail, mailTaken, tradeTarget, craftUntil, scopes, pendingPost).

### 3.5 Prerequisite re-vendor

LibKa0s v1.71.0 → v1.75.0, the whole folder, with the CLAUDE.md provenance line rolled in the same commit (tests/test_vendor_sync.lua).

---

## 4. Saved data stays untouched (session-only stores)

`State.sim.stores = { history = {}, holdings = {}, daily = {} }`. Every capture-path write resolves through one accessor per store.

| Store | Write accessor (new or changed) | Read accessor | Live-only paths (unchanged, explicit) |
|---|---|---|---|
| history | new local `historyStore()` in core/Database.lua returning `Sim.Stores().history or NS.db.global.history`, used by `Add` :585, `Amend` :598, `History` :549, `Count` :561 and `Delete` :1146 | `ActiveHistory` :557 = `State.testRecords or historyStore()` | `Purge` :1165, `PruneOld` :1236, `StorageStats` :1201, `CountOlderThan` :1219, `RepairBoundStates` :537, migrations |
| holdings | `Holdings:Store()` :36 returns the session table first | `ActiveStore` :47 unchanged (test, then Store) | — |
| daily | `Rollup:Store()` :20 returns the session table first | `ActiveStore` :30 unchanged | `SeedOnce` :139, `Prune` :153 (login deferral) read `NS.db.global` directly; keep them live and refuse a simulation until they have run (§5.1) |
| Reconciler coalescing | modules/Reconciler.lua:489 `NS.db.global.history[recent.index]` must use `NS.Database:History()` | — | — |

- **Write hooks need no change.** `Rollup:OnWrite` (Database:OnWrite, core/Database.lua:571) writes `Rollup:Store()`, which is the session store during a simulation.
- **Destructive surfaces are refused while a simulation runs**, with one line `"<what> is not available while a simulation runs."`:
  - `/lh purge` (settings/Schema.lua:1127),
  - the ledger reset offer and confirm (settings/Slash.lua:120-160),
  - "Forget this character" (`R.ForgetHolder`, Reconciler.lua:749),
  - a retention change that would prune.

  Row-menu Delete (BrowserTable.lua:1247) is allowed, because it acts on the session log the window is showing.
- **The invariant test (§8):** across every scenario, `NS.db.global.history`, `.holdings` and `.daily` serialize byte-identically before start and after stop.
- **Session genesis.** At start, after the stores are swapped, run `R:LoginScan()` with the seam on. Session holdings are empty, so the first pass is a silent **genesis** (Reconciler.lua:676-687) and writes no rows. The bank and warband tabs stay `partial` until the scenario's first banker visit, exactly as they would live.

---

## 5. Session: refusals, auto-stop, stop

### 5.1 Refusals (`Sim.Refusal`, one printed line each, checked in this order)

1. Stood down (disabled, or a perf capture holds `HOLD_PERF`): `NS.IsStoodDown()`.
2. Already running.
3. Test mode on (`NS.BrowserTable.testMode`). Test mode in turn refuses while a simulation runs: add this case to `testModeRefusal`, BrowserTable.lua:638-645.
4. Real combat (`Compat.PlayerInCombat` via `seam:Live`).
5. Inside any instance (`Compat.InInstance` via Live).
6. In a real group (`Compat.InGroup` via Live).
7. A real interaction frame is open (`next(State.scopes)` or `next(R.readable)`). Otherwise the real readable and scope state would interleave with the simulated state.
8. The ledger is settling (`R._pending`, `R._holdSince`, `R.deferred` or `R.loginPending` set). Starting would discard a real classification that is still in flight.
9. The login deferrals have not run (`NS.State.cleanupDone` and a new `NS.State.loginSettled`, set by the 20-second deferral at core/LootHistory.lua:150-152). `PruneOld`, `RepairBoundStates` and `Rollup:SeedOnce` must not race the store swap.
10. Scenario-specific: the `vendor`, `ah`, `bank` and `social` scenarios refuse when `settings.trackLedger` is off ("these steps record through the ledger, so turn on gains and losses first"). The `loot` and `key` scenarios run either way.

### 5.2 Start

Refusal, then:
1. Create `State.sim` (world, stores, timeline, counters).
2. `R:ResetState()` and `Attribution:ResetContexts()`.
3. `seam.active = true`.
4. Register the simulation's own world-watch target (§5.3).
5. Session genesis (§4).
6. Browser `OnDatasetChanged` and the preview marker on (§6).
7. Open the panel.
8. Print one line: `Simulation started (<scenario>): nothing is saved; your history and holdings are not touched.`

### 5.3 Auto-stop, then live delivery

`NS.SimOnRealEvent(row, event, …)` and its hook counterpart classify what the real client delivers while a simulation runs:

- **Interference: stop with reason `world`, then deliver the real event live.** The live delivery reaches the real stores, so no real loot is lost.
  - `CHAT_MSG_LOOT`, `CHAT_MSG_CURRENCY`, `CHAT_MSG_MONEY`, but only when the self-parse matches. Another player's line is ignored.
  - `LOOT_OPENED`, `ENCOUNTER_START`, `CHALLENGE_MODE_START`, `QUEST_TURNED_IN`, `TRADE_ACCEPT_UPDATE`, `MAIL_SEND_SUCCESS`, `PLAYER_INTERACTION_MANAGER_FRAME_SHOW`.
  - Any real hook call.
- **Absorbed (ignored): bag, money, currency, equipment, bank, auction and spell-cast events.** What they changed is caught when the stop runs a drift pass.
- **World-watch.** The simulation registers its own private bus target only while it runs. `GROUP_ROSTER_UPDATE` stops with reason `group` when it is a live group. `PLAYER_ENTERING_WORLD` and `ZONE_CHANGED_NEW_AREA` stop with reason `instance` when the player is live in an instance. `PLAYER_REGEN_DISABLED` stops with reason `combat`.
  - `PLAYER_ENTERING_WORLD` needs its own target because the bus already binds it to `OnEnterWorld` (Attribution.lua:422-425).
- **Lifecycle.**
  - The stand-down stops with reason `standDown`. Add `call("SimStop")` as the **first** of `STAND_DOWN_STEPS` (core/LifecycleSetup.lua:157).
  - A profile switch, copy or reset stops with reason `profile`, first thing in `NS.OnProfileEvent` (core/LootHistory.lua:94).
  - `/reload` and logout end the simulation, because it is session-only.

### 5.4 Stop (each step under `pcall`; one failing step never skips the rest)

1. Cancel the simulation timers (the timeline, the Sim-1.0 session `After`).
2. `seam.active = false`. Clear `State.sim` and `delivering`.
3. Cancel `R._pending`/`R._recheck` (§3.4). Then `R:ResetState()` and `Attribution:ResetContexts()`. Without this, a simulated stamp or claim would attribute the next real loot.
4. Release the stores. Every read accessor falls back to live.
5. Unregister the world-watch target.
6. **Real reconcile:** `NS.After(1, R:LoginScan)`, unless the simulation is stopping because of a stand-down. Whatever really changed during the simulation becomes UNTRACKED drift. That is the same answer the addon already gives after a disable/enable (Reconciler.lua:712-716).
7. Browser `OnDatasetChanged`, `HISTORY_CHANGED`, `HOLDINGS_CHANGED` for the session's holders, and the preview marker off.
8. Repaint the panel to the scenario picker.
9. Print `Simulation stopped[: <reason>].`
10. One `[Sim]` debug line with the event count, rows written and the reason.

---

## 6. UI: panel, marker, diagnostics, debug

- **Panel.** The panel is the Sim-1.0 shared step panel (#53/#54).
  - Title: `Ka0s Loot History - Simulation`.
  - Rows: status dot, step label (`Kill: Rookery Bat`, `Loot: 3 items + gold`, `Merchant: sell 4`, `Mailbox: take sale money`), and the right-aligned command `/lh sim step`.
  - Clicks: clicking ahead runs every step up to and including the clicked one, in order. A completed row's tooltip says when it ran. Each row's tooltip says what the step injects, for example "LOOT_OPENED (Creature GUID), two CHAT_MSG_LOOT lines, BAG_UPDATE burst".
  - Footer: Run all / Pause / Resume / Restart / Stop.
  - Picker: when no simulation runs, a scenario picker (§7) with a Start button.
  - Placement: it opens beside the History window. Its position is remembered in the same profile window-state table as the History window's geometry. That is window state, not a schema setting.
  - Size: LootHistory's own panel code is only the descriptor, the picker and the tooltips, in `modules/SimPanel.lua`, about 150 lines.
- **Preview-mode marker.** Per the v2.86.0 preview-mode marker rule, the History window shows `SIMULATION` in the title bar, in its own color, next to the slot used by the `TEST MODE` badge (modules/Browser.lua:887-889, :582-583). LootHistory adopts **W.TestStrip** for test mode in this run, so the simulation uses the same strip with a simulation label and color, if TestStrip takes a label option (open question 1). The footer reads `Simulating: <scenario> · step k/n`.
- **Diagnostics.** A new `sim` section in modules/Diagnostics.lua's `SECTIONS` (:348):
  - active, scenario, step k/n, events fired, hooks fired;
  - rows in the session log, holders in the session store;
  - last stop reason;
  - the seam's wrapped-key count and the guarded keys.

  It reads module fields only, per the rule at Diagnostics.lua:17.
- **Debug.** A `Sim` tag logs every fired event or hook, every refusal and every stop step. It is gated at the call site like the other tags.
- **Launcher.** No entry, as in Drop Watcher. The Show-window key binding owed under the new launcher-§6 rule is separate work.

---

## 7. Scenarios (timelines that drive the real engine end to end)

Each step is one or more driver calls. "Expect" lists what the end-to-end suite asserts. Every expectation is produced by engine rules already in the code, and the suite pins the exact rows.

**`loot` (open world).**
- Steps: start, then kill (`LOOT_OPENED` with a Creature GUID). Then two `CHAT_MSG_LOOT` lines (a single item and an `xN` stack), the first **chat before bags** and the second **bags before chat**. Then a poor-quality item below the threshold, and a `CHAT_MSG_MONEY`. Then lockbox open (`hook:UseContainerItem` on a `hasLoot` slot). Then quest reward (`hook:GetQuestReward` plus `QUEST_TURNED_IN`). Then end.
- Expect:
  - KILL rows carrying the npcID detail;
  - GOLD IN KILL;
  - CONTAINER and QUEST rows;
  - the gated poor item recorded **only** as a Reconciler diff row (spec D2, Collector.lua:146-149);
  - **no duplicates**: each claim is consumed (Reconciler.lua:318-335), whichever arrives first.

**`key` (Mythic+).**
- Steps: `CHALLENGE_MODE_START` (keystone +10, party instance, zone and subzone from the provider). Then two times: pull (simulated combat on, ENCOUNTER_START) and kill (ENCOUNTER_END success, combat off with `PLAYER_REGEN_ENABLED`), followed by loot. Bags change **during** simulated combat, so the flush defers (`R:Flush` :654) and runs on the regen edge. Then `CHALLENGE_MODE_COMPLETED`, the end chest (`LOOT_OPENED` with a GameObject GUID), currency (`CHAT_MSG_CURRENCY` plus `CURRENCY_DISPLAY_UPDATE`), a bonus-roll line, and a roll-won pair. Then zone out (`InPartyInstance` false plus `ZONE_CHANGED_NEW_AREA`).
- Expect:
  - KILL rows with encounter and keystone detail;
  - MPLUS from the chest;
  - BONUS_ROLL and ROLL as CERTAIN;
  - a currency row under the listed id;
  - the keystone context cleared afterwards.

**`vendor` (merchant and disenchant).**
- Steps: Merchant SHOW. Sell 3 items (bags −, money +). `hook:BuyMerchantItem`, then a `LOOT_ITEM_PUSHED_SELF` line. `hook:RepairAllItems` with money −. `hook:DeleteCursorItem` on one item. Merchant HIDE. Disenchant: `UNIT_SPELLCAST_SUCCEEDED("player", _, 13262)`, then `LOOT_OPENED` with an Item GUID (the disenchant stamp is kept, :202-204), then the materials lines, with the disenchanted item leaving the bags.
- Expect (reasons from `MERCHANT_REASON`, core/Ledger.lua:234-237):
  - item OUT SELL, gold IN SELL;
  - item IN VENDOR, gold OUT BUY;
  - gold OUT REPAIR;
  - item OUT DESTROY;
  - materials DISENCHANT, item OUT DECONSTRUCT.

**`ah` (Auction House day).**
- Steps: Auctioneer SHOW. `hook:PostItem` on 2 items with a posting fee, then `OWNED_AUCTIONS_UPDATED`. `hook:PlaceBid` with money −. HIDE. Later: Auctioneer SHOW, then `OWNED_AUCTIONS_UPDATED` with one auction gone (sold) and one still listed. HIDE. Then MailInfo SHOW plus `MAIL_INBOX_UPDATE`, with a sale mail (subject from `AUCTION_SOLD_MAIL_SUBJECT`, money), a won mail (attachment) and an expired mail (the posted item). `hook:TakeInboxMoney(1)` with money +. `hook:TakeInboxItem` ×2 with bags +. HIDE.
- Expect, per the escrow rules (Escrow.lua:7-13):
  - MOVE bags→auctions;
  - gold OUT AH_POST_FEE and AH_BUY;
  - exit held, then item OUT AH_SOLD with gold IN AH_SOLD;
  - the won item IN AH;
  - the expired item back as an own-origin MOVE, not a gain.
- Timing: the one-sided-hold timeout of 6 s (core/Ledger.lua:49) applies, so the timeline waits on the ledger (§9).

**`bank`.**
- Steps: Banker SHOW (the first visit is the bank's genesis, with no rows). Deposit 2 stacks (`BAG_UPDATE` plus `PLAYERBANKSLOTS_CHANGED`). AccountBanker SHOW. Deposit to a warband tab, and deposit gold (`ACCOUNT_MONEY`). Withdraw 1. HIDE.
- Expect: intra-holder MOVE rows; WARBAND_DEPOSIT and WARBAND_WITHDRAW pairs (Reconciler.lua:249-257); the warband's genesis on first read.

**`social` (mail and trade).**
- Steps: MailInfo SHOW. `hook:SendMail("Simalt")` with `ReadSendMail` from the world, then `MAIL_SEND_SUCCESS`. A trade with `Simalt` (`TRADE_ACCEPT_UPDATE(1,1)`), then a trade with a stranger. A warband currency transfer (`CURRENCY_TRANSFER_LOG_UPDATE` plus `LatestCurrencyTransfer`).
- Expect: OUT ALT_MAIL with the alt's mail credited in the session store; ALT_TRADE both ways; TRADE_GIVE and an IN TRADE; CURRENCY_TRANSFER pair rows.

Every scenario ends on a **settled** ledger (no `_pending`, no `_holdSince`).

---

## 8. Slash verbs (`/lh sim …`)

One `NS.COMMANDS` row, `"sim"`. It is a feature verb, so `gateFeatureVerbs` refuses it while the addon is disabled (settings/Schema.lua:1023-1040). It is **not** in `LIVE_WHILE_DISABLED`.

| Verb | Does |
|---|---|
| `/lh sim` | Opens the panel; prints status and usage |
| `/lh sim start <loot\|key\|vendor\|ah\|bank\|social>` | Refusals (§5.1), start, open the panel |
| `/lh sim run` / `step` / `pause` / `resume` / `restart` | Timeline control, the same functions the panel calls |
| `/lh sim loot [n]` | n ad hoc self-loot lines now (kill context) |
| `/lh sim stop` | Stop (§5.4) |
| `/lh sim panel` | Toggle the panel |

Update docs/slash-dispatch.md, the help counts tests/test_slash.lua pins, and the README feature list. Do not add a command table, per the sync-docs rule.

With no LibKa0s (a degraded install), `sim` answers the collection's library-absent line, as the `perf` stub does.

---

## 9. What LootHistory needs from LibKa0s-Sim-1.0 (input to the library design)

LootHistory is the second consumer. These are the needs it brings that Drop Watcher alone would not surface:

1. **Seam over a host table** with `pure` and `guarded` sets, `SetProvider(key, fn(fallback, …))`, `Live(fn, …)` and an `active` flag costing one boolean test. The wrap happens at load. LootHistory has no runtime-added Compat members (verified).
2. **Session:** `Start` (host refusal), `Stop(reason)` running host steps in order under `pcall`, `After` timers cancelled at stop, `Fire(event, …)` via the host `deliver` callback with `IsDelivering()`. LootHistory relies on `deliver` accepting **any string** (it uses `hook:<name>`).
3. **Timeline:** `Step`, `Run`, `Pause`, `Resume`, `Restart`, `RunTo` and listeners, **plus an optional host `gate()` predicate** checked before the next step while running. LootHistory gates on "ledger settled". Without it, `Run` races the Reconciler's 0.35 s debounce, 1.5 s claim wait and 6 s settle hold. `Step` while the gate is closed prints "settling…" and does not advance.
4. **Step panel:** rows by **index** (Drop Watcher's keys repeat), and a footer slot for the scenario picker and run controls.

No library code touches a SavedVariables store. Store redirection stays host code (§4), as the challenger's "five safety rules cannot be enforced by the library" finding requires.

---

## 10. Files and size

| File | Kind | ~Lines |
|---|---|---|
| core/Compat.lua | +C1-C3 members | +45 (882 → ~927) |
| core/Dispatch.lua | new: EVENT_ROWS, HOOK_ROWS, Register/Unregister/Deliver | 120 |
| modules/Attribution.lua, AttributionOut.lua, Collector.lua, Reconciler.lua | rows replace hand lists; ResetState and ResetContexts | net +30 |
| core/Database.lua, modules/Holdings.lua, modules/Rollup.lua, Reconciler.lua:489 | store accessors | +25 |
| core/LifecycleSetup.lua, core/LootHistory.lua | `CancelDeferral(h)`, SimStop step, profile stop, `loginSettled` | +20 |
| core/SimSeam.lua | new: `Sim.NewSeam(NS.Compat, {pure, guarded})`, the PURE list and GUARDED.ListCurrencies; TOC right after core/Compat.lua (load-bearing comment) | 60 |
| modules/Sim.lua | new: session host, refusal, start/stop steps, stores, auto-stop, world-watch | 300 |
| modules/SimWorld.lua | new: world tables, fixtures, mutation helpers, providers | 380 |
| modules/SimDrivers.lua | new: event and hook drivers with payload shapes, line writers from the parser's global accessors | 380 |
| modules/SimScenario.lua | new: six scenarios, timelines, step lines, ledger gate | 320 |
| modules/SimPanel.lua | new: panel descriptor, picker, tooltips | 150 |
| settings/Schema.lua, Diagnostics.lua, BrowserTable.lua, Browser.lua | verb row, sim section, exclusivity, marker | +80 |

Totals:
- **New runtime code:** about 1,600 lines across 6 files.
- **Refactors:** about 250 lines.
- **Tests:** about 1,300 lines.
- No file nears the 1500-line cap. Every new function stays at or below CCN 15 (release battery).

---

## 11. Tests (headless, `lua tests/run.lua` plus `luacheck .` at 0/0)

1. **test_dispatch.lua.**
   - Every capture registration comes from `NS.EVENT_ROWS`, and the (target, event) set is identical to today's.
   - Row order is checked.
   - `registered` follows Enable and Disable, including trackLedger off.
   - A real interference event during a simulation stops it, then is handled live into the real store.
   - An absorbed event is ignored.
   - Hook rows are installed once, and both `BuyMerchantItem` rows run.
2. **test_sim_seam.lua.**
   - Every non-PURE Compat member is wrapped. A snapshot of members means a new member must be classified as pure, guarded, provided or live.
   - `ListCurrencies` never reaches `C_CurrencyInfo.ExpandCurrencyList` while a simulation runs.
   - Static scan:
     - no `GetNumLootItems`, `GetLootSourceInfo`, `IsInInstance`, `IsInGroup` or raw `hooksecurefunc` in modules/;
     - no `local x = Compat.Member` outside core/Compat.lua;
     - no call to any hooked client function in the `modules/Sim*.lua` files.
3. **test_sim_store.lua.** For every scenario, the live `history`, `holdings` and `daily` serialize identically before and after. The maintenance paths stay live. Purge, ledger reset, Forget and retention prune are each refused with their line.
4. **test_sim_e2e.lua (the DW-90 regression).**
   - The world is the mock's **real solo answers**: not in a group, not in an instance, no keystone, no loot window. Only providers may answer.
   - Each scenario runs with `step` and with `run` (the kit clock advances), and the suite asserts the §7 rows: source or reason, direction, quantity, holder.
   - No duplicate rows. The session holdings are correct.
   - `ActiveHistory` and `Holdings:ActiveStore` serve the session data. The Browser shows rows under the **default** filters.
5. **test_sim_session.lua.**
   - Each refusal (§5.1) prints its line.
   - Each auto-stop: group, instance, combat, real loot line, real hook, stand-down, profile event.
   - Stop clears contexts and Reconciler state, cancels `R._pending`, releases the stores and schedules the drift `LoginScan`.
   - Test mode and the simulation exclude each other.
6. **test_sim_panel.lua.** Rows track the timeline. Clicking ahead runs the steps in between. A typed `/lh sim step` repaints the panel. The ledger gate shows "settling". Run, pause, resume, restart and stop all work. The picker starts the chosen scenario.
7. **test_sim_slash.lua.** Every verb works. `sim` is refused while disabled. The library-absent stub answers.
8. **Unchanged and green:** test_disabled (the stand-down stops the simulation first), test_attribution, test_reconciler*, test_collector, test_perf, test_vendor_sync, test_surface_parity (help counts updated).
9. **Smoke, owed (`docs/smoke-tests.md`, new SIM theme; never marked passed by an agent):**
   - start and stop, and the refusals;
   - a full run of each scenario showing rows in History, Holdings and Timeline;
   - a real loot during a simulation stops it and records live;
   - saved data unchanged after `/reload`;
   - the panel follows the run and clicking ahead works;
   - the marker is shown.

---

## 12. Order of work (commits on LootHistory's feature branch)

1. Re-vendor to v1.75.0.
2. C1-C5 Compat routing.
3. The dispatch and hook tables (§3.2-3.3), with registration parity proven by tests.
4. ResetState/ResetContexts and `CancelDeferral`.
5. Store accessors, plus the Reconciler.lua:489 fix.
6. SimSeam.
7. The session (Sim.lua).
8. World and drivers.
9. Scenarios and the end-to-end suite.
10. Panel and marker.
11. Slash verbs, diagnostics and docs: ARCHITECTURE module map and message-bus, data-flow "Simulator" section, slash-dispatch, smoke-tests SIM theme, compat-layer member list.

**Effort:** M/L, about 2-3 sessions. This is the LootHistory half of the owner's "new simulators in LootHistory and BankLedger". BankLedger can reuse this design's store, dispatch and ledger-gate shape where its Reconciler-style code matches. That check belongs to BankLedger's own requirements.
