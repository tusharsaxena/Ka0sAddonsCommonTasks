# Ka0s Bank Ledger: in-game simulator (`/bl sim`), requirements

- **Repo:** `/mnt/d/Profile/Users/Tushar/Documents/GIT/BankLedger` (master `b0f9493`, v1.3.0, vendors LibKa0s v1.71.0 / kit 38). Read-only analysis, 2026-10-22.
- **Closes:** BankLedger#24 ("In-game simulator (like Drop Watcher's /dw sim)", open, `state:triaged`, `severity:low`).
- **Reference host:** Drop Watcher. `core/SimSeam.lua`, `modules/Sim.lua`, `modules/SimScenario.lua`, `modules/SimPanel.lua`, and the specs `docs/superpowers/specs/2026-10-11-drop-watcher-simulator-design.md` and `-sim-feedback-design.md`.
- **Builds on:** LibKa0s v1.75.0, which carries `LibKa0s-Sim-1.0` and the shared step panel (#53/#54, owner decision 1). That release also carries `W.TestStrip`, which Bank Ledger adopts in the same run.
- **Assumed Sim-1.0 surface:** the c54 sketch, i.e. `NewSeam(compat, {pure, guarded})` with `SetProvider`, `Live` and `active`; `NewSession({seam, refusal, deliver})` with `Start`, `Stop`, `AddCleanup`, `After`, `Fire` and `IsDelivering`; a timeline; and a step panel fed `{label, command, state, actionable, tip}` rows. Where the shipped names differ, the **semantics** below are the requirement and the names are not.

---

## 1. What exists today (findings, with file:line)

### 1.1 Client reads: what goes through `NS.Compat`, and what does not

`core/Compat.lua` has 13 function members. Every one is a plain `function Compat.X`, and **no file caches a member at load**: a grep for `= NS.Compat.X` or `local … = NS.Compat` outside Compat finds nothing. Every call site writes `NS.Compat.X(...)` at call time. A Drop-Watcher-style load-time wrap therefore covers all of them, provided it runs straight after `core/Compat.lua` (TOC line 38).

| Member | Compat line | Sim role |
|---|---|---|
| `GetGuildName` | 24-29 | provider (an invented guild when the player has none) |
| `GetMoney` | 33-36 | provider (the sim purse) |
| `GetStoreMoney(store)` | 52-67 | provider (sim warband and guild balances, with the same nil semantics: guild is nil while the sim guild frame is hidden) |
| `GetContainerNumSlots(bagID)` | 72-76 | provider |
| `GetContainerSlot(bagID, slot)` | 80-86 | provider (the same `{itemID, link, count}` triple) |
| `GetGuildBankSlot(tab, slot)` | 91-103 | provider |
| `GetNumGuildBankTabs` | 105-108 | provider |
| `QueryGuildBankTab(tab)` | 116-118 | **guarded** (the only client *request* Bank Ledger makes) |
| `GetCurrentGuildBankTab` | 122-125 | provider |
| `IsGuildBankVisible` | 137-141 | provider (answers `true` or `false` from sim state, never nil) |
| `GuildBankTabSize` | 143-146 | unwrapped (a constant) |
| `GetItemDetails`, `ItemNameQuality` | 153-175 | unwrapped. Item facts stay real, so the real cache, the `uncached` gate path and link-first enrichment all run for real |

**Reads outside Compat** (grep over `core/ modules/ settings/`, excluding Compat):

| Site | Read | Sim must answer? | Action |
|---|---|---|---|
| `core/Util.lua:6-12` `Util.PlayerKey` | `UnitName("player")`, `GetNormalizedRealmName`/`GetRealmName` | **Yes**: every row's `char` (Ledger.lua:345), and the character-switch scenario | Route through Compat (R2) |
| `modules/Ledger.lua:342` `BuildEntry` | `UnitClass("player")` | **Yes**: every row's `classFile` | Route through Compat (R2) |
| `modules/SessionWindow.lua:211` (preview rows) | `UnitClass("player")` | No (preview only) but identity should be uniform | Route through Compat (R2) |
| `modules/Ledger.lua:662-691` `HookGuildBankFrame` | `GuildBankFrame:HookScript` (OnShow/OnHide) | These are the guild bank's **only** open and close (Ledger.lua:641-661). `Fire(event)` cannot drive a hook | Hook bodies move into the dispatch table (R1) |
| `modules/Ledger.lua:344`, `:595`; `core/Database.lua:949,974` | `time()`, `GetTime()` | No. Real time drives the real debounce and settle, which is the point | Keep |
| `core/Constants.lua:118` | `Enum.BagIndex` at load (container id groups) | No. The sim keys its containers by the real `C.BAG_IDS`/`C.BANK_IDS`/`C.WARBAND_BANK_IDS` | Keep |
| `core/EnvSetup.lua` (`NS.Zone`, `NS.PlayerMapID`) via LibKa0s-Env | zone and map id | No. Sim rows carry the real zone (an Env read bypasses any host seam; see c54 risks) | Keep, document |
| `core/ItemSetup.lua:65-67` `LoadItem` | `C_Item.RequestLoadItemDataByID` | No. A harmless cache warm on a real item id | Keep |
| `core/Util.lua:271`, `modules/LedgerTable_TestMode.lua:244` | `InCombatLockdown()` | No. The sim never invents combat; refusals read the real state | Keep |
| `modules/Browser.lua:106` | `UnitClass` (close-button tint, at build) | No (cosmetic) | Keep |
| `modules/Ledger_Diagnose.lua:39-126` | raw `Enum.BagIndex`, `C_Bank`, `GuildBankFrame` | No. `/bl debug scan` is a client probe | Add a "simulation running: Compat answers are simulated" header line (R9) |

### 1.2 Event dispatch: there is no table to fire through

`modules/Ledger.lua:806-819` splits the capture events into `OPEN_EVENTS` (`BANKFRAME_OPENED → BANK_FRAME`), `CLOSE_EVENTS` (`BANKFRAME_CLOSED`), `CHANGE_EVENTS` (`BAG_UPDATE_DELAYED`, `PLAYERBANKSLOTS_CHANGED`, `PLAYER_MONEY`) and `GUILD_DATA_EVENTS` (`GUILDBANKBAGSLOTS_CHANGED`). `L:Enable` (833-867) registers each one with an **anonymous closure** through `NS.RegisterEventSafely` on `NS.addon`, plus `ADDON_LOADED`. The guild bank's open and close are `HookScript` closures (671-688). The addon's own `PLAYER_ENTERING_WORLD` and `PLAYER_REGEN_*` are registered by method name in `NS.StandUp` (`core/BankLedger.lua:132-137`). A simulator has nothing to deliver *through*. That is the #24 prerequisite "its events go through one dispatch table", and the c54 analysis named it as the reason Bank Ledger was a false consumer (it cited Ledger.lua:806-822 and 802-804).

AceEvent holds one handler per event per target, so Bank Ledger has **one handler per event**. That is not Drop Watcher's fan-out (`NS.FEATURE_EVENTS`). The deliver callback is therefore a single lookup, which is a correct use of Sim-1.0's host-supplied `deliver`.

### 1.3 Bank, warband and guild flows (the real engine the sim must drive)

- **Bank frame:** `BANKFRAME_OPENED` → `L:OpenContext(BANK_FRAME)` (705-729), which snapshots bags plus **both** BANK and WARBAND_BANK (`CONTEXT_STORES` 30-33; tab switching fires nothing). Change events → `ScheduleReconcile` (616-626: AceTimer debounce, `DEBOUNCE_SECONDS = 0.35` at 614) → `Reconcile` (580-599) → per store `Diff` (156-179, the both-sides rule), then `GateReason` (298-330), `BuildEntry` (340-383) and `Database:Add`. `settleBaseline` (535-566) **holds** the baseline on a one-sided change for up to `SETTLE_TIMEOUT_SECONDS = 6` (449). `BANKFRAME_CLOSED` → `CloseContext` (760-777) runs a final pass and drops any held change.
- **Money:** a row needs the purse and a store's own balance to move in opposite directions (`moneyMove` 143-154). Only `MONEY_STORES` (20) count, and a nil `storeMoney` on either side means no row (the F-001 rule).
- **Guild bank:** opened by the `GuildBankFrame` OnShow hook (671-681); closed by OnHide (682-688) or `disarmGuildBankIfGone` (571-578). `GUILDBANKBAGSLOTS_CHANGED` → `OnGuildBankData` (751-758), which arms **only** when `IsGuildBankVisible() == true`. That is the issue #12 fix: data arriving while away must not arm. `OpenContext(GUILD_BANK)` queries every tab (`QueryGuildBankTabs` 232-239), and the replies arrive asynchronously as `GUILDBANKBAGSLOTS_CHANGED`. Rows are stamped `guild = Compat.GetGuildName()` (356-358).
- **Session window:** `Ledger` alone sends `SESSION_CHANGED` (`fireSessionChanged` 406-410). `SessionWindow` (`modules/SessionWindow.lua:686-692`) starts and ends a session on it, and appends on `ENTRY_ADDED`.
- **Stand-down:** `NS.StandDown` (`core/BankLedger.lua:255-268`) cancels timers, drops events, then calls `L:DropContext()` (Ledger.lua:789-801, which does **not** reconcile), then drops the bus targets and hides the windows.

### 1.4 SavedVariables writers

| Writer | Writes | Reached by the engine during a sim? |
|---|---|---|
| `Database:Add` (`core/Database.lua:401-409`) | `db.global.ledger` | **Yes**, via `L:Record` (388-392). It must be redirected (R3) |
| `Database:DeleteAt/Delete/Purge/PruneOld` (883-985) | `db.global.ledger` | Only from user acts or the once-per-session PEW prune; they operate on the real ledger |
| `Backfill.Apply` (`modules/Backfill.lua:61-85`, reads `db.global.ledger` at :169) | real rows in place | Never sees sim rows |
| Filters lists, schema writes, view saves, window geometry, LibDBIcon | profile / global | Only from user acts |

### 1.5 Test mode, slash, launcher

- **Test mode:** `State.testRecords` (`core/State.lua:29`) swaps the read dataset through `Database:ActiveLedger()` (`core/Database.lua:392-394`). It is refused in combat and under the visibility rule (`LedgerTable_TestMode.lua:243-252`) and ended by combat (`core/BankLedger.lua:306-317`). The window marker is a red "TEST MODE" title badge (`modules/Browser.lua:992-997`, `UpdateTestBadge` 740-743), which `W.TestStrip` replaces in this run. Test-only predicates are scattered: `Browser_Views.lua:28,246`, `LedgerTable.lua:859` (row menu `live`), and `Browser.lua:742`.
- **Slash:** `NS.COMMANDS` (`settings/Schema.lua:795-896`). Feature verbs are refused while disabled; the live set is the reserved verbs plus `profile` (`settings/Slash.lua`, HOST_LIVE_VERBS). There is no `perf` verb (performance-§12 no-combat-path exemption, `docs/performance.md`).
- **Launcher:** `core/LauncherSetup.lua:189-191` exposes `isTestMode`. A sim gets no launcher entry (Drop Watcher precedent).

---

## 2. The simulated world (providers)

One session table, `NS.State.sim` (runtime-only; never in SavedVariables):

```
State.sim = {
  sim = true, scenario, startedAt, events = 0, queries = 0,
  chars = { main = { key, name, realm, classFile }, alt = { … invented } }, current = "main",
  world = {
    bags   = { [charKey] = { [bagID] = { [slot] = { itemID, link, count } } } },  -- per character
    bank   = { [charKey] = { [bagID] = { … } } },                                  -- per character (BANK ids)
    warband= { [bagID] = { … } },                                                 -- account-wide (WARBAND ids)
    guild  = { name, visible = false, tabs = { [tab] = { [slot] = {…} } }, money },
    purse  = { [charKey] = copper }, warbandMoney = copper,
  },
  pool = { {itemID, link}… }, timeline = {…},
}
NS.State.simLog = {}   -- the session-only ledger the engine writes into (R3)
```

**Real items, invented placement.** At start, the pool comes from the player's **real** bags, read with the seam bypassed (`Live(L.ScanStore, L, C.Store.BAGS, links)`). These are real cached ids and links, including bonus-ID links, so `GetItemDetails`, the link-first enrichment and the quality gate run for real. When fewer than 4 distinct ids are found, the fallback is the fixed ids `modules/SessionWindow.lua:203-209` already uses (2589, 194863, 171276, 6948), warmed with `NS.Item.LoadItem`. The fallback is reported once. Containers use the real ids from `C.STORE_CONTAINERS`:

- The backpack has 20 slots. `CharacterBankTab_1` and `AccountBankTab_1` have 98 each. Every other id answers 0 slots (unpurchased), which is realistic.
- There are 2 guild tabs of `GuildBankTabSize()` slots, and `GetCurrentGuildBankTab` answers 1.
- Starting money: purse 5,000g per character, warband 20,000g, guild 100,000g.

**Identity.** `main` is the real player, read live at start: name, realm and class. `alt` is invented (`L["Simbanker"]`, the real realm, a class different from main's). `Compat.PlayerName`/`PlayerClass` answer the current character's values. When the real player has no guild, `GetGuildName` answers `L["Simulated Guild"]`.

**Provider rules (each one answers fully; none falls back to live while a sim runs):**

- `GetContainerNumSlots(id)`/`GetContainerSlot(id, s)` answer from `bags[current]`, `bank[current]` or `warband` by which `C.*_IDS` group holds `id`. Any other id answers 0 or nil.
- `GetGuildBankSlot`/`GetNumGuildBankTabs`/`GetCurrentGuildBankTab` answer from `guild.tabs`. The client only holds data for queried tabs (Compat.lua:110-115), so the provider answers nil for a tab not yet "queried" this visit. That keeps `OpenContext`'s `QueryGuildBankTabs` load-bearing in the sim exactly as in the client, matching the mock's own rule (`tests/wow_mock.lua:456-457`).
- `IsGuildBankVisible` answers `guild.visible` (strictly true or false).
- `GetStoreMoney(store)`: WARBAND answers `warbandMoney`; GUILD answers `guild.money` only while `guild.visible`, else nil (the real frame-gated semantics, Compat.lua:42-59); anything else answers nil. `GetMoney` answers `purse[current]`.
- **Guarded `QueryGuildBankTab(tab)`:** no client call. It marks the tab queried, counts `queries`, and schedules `Fire("GUILDBANKBAGSLOTS_CHANGED")` 0.2 s later on the session timer, the client's asynchronous reply. This is the one member whose live body must never run during a sim, whatever a provider or caller does.

Bank Ledger makes **no other client writes**. It never picks up, moves, sends or trades an item. "No item is ever moved" therefore holds by construction, and the e2e suite asserts it (§9).

---

## 3. Events: what the drivers fire, with real payload shapes

Every driver mutates the world first and then fires, in client order, the events the real client would fire. Each event is delivered through the dispatch table (R1). An event Bank Ledger does not register runs 0 handlers, which is realistic and harmless.

| Driver | World change | Events fired (payload) |
|---|---|---|
| `OpenBank` | — | `BANKFRAME_OPENED` () |
| `CloseBank` | — | `BANKFRAME_CLOSED` () |
| `Deposit{store=BANK, item, n}` | bags −n, bank +n | `BAG_UPDATE`(bagID) per touched bag, `PLAYERBANKSLOTS_CHANGED`(slot), `BAG_UPDATE_DELAYED` () |
| `Deposit{store=WARBAND, item, n, lag}` | bags −n now; warband +n after `lag` s (nil = together; `"never"` = withheld) | now: `BAG_UPDATE`(bagID), `BAG_UPDATE_DELAYED`; after lag: `BAG_UPDATE`(warbandID), `BAG_UPDATE_DELAYED` (a warband tab is a container, Ledger.lua:444-446) |
| `Withdraw{…}` | symmetric | symmetric |
| `Deposit/Withdraw{store=GUILD}` | bags ∓, tab ± | `BAG_UPDATE`(bagID), `BAG_UPDATE_DELAYED`, `GUILDBANKBAGSLOTS_CHANGED` () |
| `Money{store, dir, copper}` | purse ∓, store balance ± | `PLAYER_MONEY` () |
| `Spend{copper}` (a repair or vendor buy) | purse − only | `PLAYER_MONEY` () |
| `Loot{item, n}` | bags + only | `BAG_UPDATE`(0), `BAG_UPDATE_DELAYED` |
| `OpenGuild` | `guild.visible = true` | host pseudo-event `GUILDBANK_FRAME_SHOWN` (the OnShow hook body); then the guarded tab queries produce `GUILDBANKBAGSLOTS_CHANGED` |
| `CloseGuild` | `guild.visible = false` | `GUILDBANK_FRAME_HIDDEN` (the OnHide hook body) |
| `GuildDataAway{item, n}` (another member's deposit while you are away) | tab +n; `visible` stays false | `GUILDBANKBAGSLOTS_CHANGED` () → must **not** arm (issue #12) |
| `Switch{to}` | closes an open frame first (fires `CloseBank`/`CloseGuild`), then `current = to` | none. A real relog reloads the UI and resets `NS.State`, so with the frame closed the engine is in the same state. `PLAYER_ENTERING_WORLD` is **not** fired: its only handler is the once-per-session prune (`core/BankLedger.lua:320-340`), which touches only the real ledger |

**To verify before freezing (smoke, not code):** the exact 12.1.5 event sequence for a warband deposit, i.e. whether `PLAYER_ACCOUNT_BANK_TAB_SLOTS_CHANGED` or `BANK_TABS_CHANGED` also fire. The driver's event list is data in `modules/SimDrivers.lua`, so a correction is a one-line edit. Bank Ledger's registered set (Ledger.lua:806-819) is the contract that matters.

---

## 4. Seam membership (the `NewSeam` call)

```
seam = Sim.NewSeam(NS.Compat, {
  pure    = { GuildBankTabSize = true, GetItemDetails = true, ItemNameQuality = true },
  guarded = { QueryGuildBankTab = guardedQuery },
})
```

Every other function member is wrapped, including the two new identity members (R2). `seam:Live(fn, …)` is used for refusals, the item pool, the real identity at start, and the stop's real-world re-read.

---

## 5. How saved data stays untouched

1. **One sink.** While `State.simLog` is set, `Database:Add` appends there and stamps `entry.sim = true`, and `ActiveLedger()` answers it (precedence: sim, then test, then live; sim and test are exclusive). Bank Ledger does **not** use `IsDelivering` for attribution. The reconcile that records a move runs on an AceTimer **after** `Fire` returns (Ledger.lua:616-626), so a delivering flag would already be false. Attribution has to be session-wide. That is safe for a reason the refusals guarantee: no real frame can be open while a sim runs (§6), so every movement recorded during a sim is a simulated one.
2. **Reads that compare against the sink.** `SessionWindow:PruneMissing` (`modules/SessionWindow.lua:171-187`) walks `Database:Ledger()`, the real ledger. During a sim it would prune every session row on the first `LEDGER_CHANGED`. It must walk the write sink instead (R4). It must not walk `ActiveLedger()`: under test mode that is the sample, while a real session still writes to the real ledger.
3. **Row menu.** Blacklist, Whitelist and Delete are disabled for synthetic datasets (R5 widens `LedgerTable.lua:859`'s `live`).
4. **Purge** stays a real act on the real ledger and is not blocked. Its line says "ledger purged", and the sim log is untouched.
5. **Stop.** `simLog` is released and the dataset swaps back. The e2e suite asserts `NS.db.global.ledger` is deep-equal before and after every scenario, and that `Database:Count()` is unchanged.

---

## 6. Refusals and automatic stop

**`Start` refuses, printing one line, in this order:**

1. Stood down: the standard disabled line (`NS.IsStoodDown`). `sim` is a feature verb.
2. A simulation is already running.
3. Test mode is on: "Turn test mode off before starting a simulation."
4. In combat (real `InCombatLockdown`).
5. A **real storage frame is open**: `State.openContext ~= nil`, or a live read of `Compat.IsGuildBankVisible() == true`. Line: "Close the bank first: a simulation cannot run beside a real bank visit."
6. General visibility keeps the ledger window closed (`Util.VisibilityRefusal`, the same guard test mode uses).

A real group or instance is **not** refused, because nothing Bank Ledger computes reads either. Being unguilded is not refused; the guild scenario invents a guild.

**Test mode refuses while a sim runs.** Add the guard `simulation` to `LedgerTable_TestMode.lua:243-252`.

**It stops by itself** (reason → line):

- A **real** `BANKFRAME_OPENED`/`BANKFRAME_CLOSED` or a real guild frame show/hide, meaning one that was not delivered by `Fire`. Reason `bank`. The stop runs **before** the real handler, inside `L:Dispatch`, so the real open snapshots the real world.
- `PLAYER_REGEN_DISABLED`. Reason `combat`, in `addon:OnCombatChanged` next to the test-mode end (`core/BankLedger.lua:306-317`).
- Stand-down. Reason `standDown`, as the first step of `NS.StandDown` (`core/BankLedger.lua:255`).
- `/reload` and logout, because nothing is saved.

Real `BAG_UPDATE_DELAYED`, `PLAYER_MONEY` and `GUILDBANKBAGSLOTS_CHANGED` (looting, a guild-mate's deposit) do **not** stop it. With a sim frame open they only cue a re-diff of the simulated world, which the seam answers. With no sim frame open, `ScheduleReconcile` is a no-op (Ledger.lua:617).

**Stop order. Each step runs under pcall, and it is load-bearing:**

1. Cancel the session's timers.
2. `L:DropContext()` **while the seam is still on**. This cancels the pending debounce (`L._pendingTimer`), clears the context, baseline and settle window, and sends `SESSION_CHANGED(false)` (the session window ends). There is **no Reconcile**: a final pass with the seam off would diff a simulated baseline against the real world and invent movements.
3. Seam off.
4. Release `simLog`; identity providers fall away with the seam.
5. `Browser:OnDatasetChanged()` (the window, Insights and the default character filter re-resolve); repaint the panel; hide the strip.
6. Print the stop line.

---

## 7. Scenarios (timeline steps through the real engine)

Each step is one driver call plus a `settle` (the minimum seconds an automatic run waits before the next step). Each step records `rowsBefore = #simLog`, so its row and tooltip report what the engine actually recorded. **Expected counts assume default gate settings**; a user's quality threshold, excluded stores or Track toggles legitimately change them, and that difference is itself a valid observation.

| Scenario (`/bl sim start …`) | Steps | Expected (defaults) |
|---|---|---|
| `bank`: personal bank | Open bank → deposit 20 × A to BANK → deposit 1 × B (a bonus-ID link when the pool has one) → withdraw 5 × C from BANK → close bank | 3 BANK rows (2 deposits, 1 withdrawal); B's row keeps the observed link |
| `warband`: warband transfer between characters | Open bank → deposit 20 × A to WARBAND, lag 1.5 s (settle 3) → deposit 1,000g to WARBAND → close bank → switch to alt → open bank → withdraw 10 × A from WARBAND → withdraw 500g → close bank | 4 WARBAND rows: main's 2 deposits, alt's 2 withdrawals stamped `char = Simbanker-<realm>`, with the alt's class. The held-baseline path runs (`[Diff] one-sided change: baseline held` … `settled`) |
| `guild`: guild bank | Guild data while away (must not arm) → open guild bank (tabs queried, replies 0.2 s later) → withdraw 5 × D → deposit 3 × A → withdraw 200g → close guild bank | 0 rows and no context after step 1; then 3 GUILD_BANK rows stamped `guild` |
| `onesided`: a session closed mid-change | Open bank → loot 2 × E into the bags (settle 6.5: re-anchored, no row) → repair for 25g (purse only, no money row, F-001) → deposit 5 × A to WARBAND with the store half withheld → close bank (`CloseContext` final pass; "held change dropped") | 0 rows |

A typed `/bl sim step` and a panel click run the same `Step`. Clicking a later row runs every step up to it in order (`RunTo`); clicking a completed row does nothing, and its tooltip says when it ran and what was recorded.

---

## 8. Panel, marker, slash, diagnostics

- **Panel:** Sim-1.0's shared step panel, frame `BankLedgerSimPanel`, title `Ka0s Bank Ledger - Simulation`. The rows are `Start: <scenario>`, one per step (label, `/bl sim step`, state, per-row tip: "Moves 20 × Linen Cloth from the backpack to warband tab 1; the warband half lands 1.5 s later"), then `Stop simulation`. Controls are Run all / Pause / Resume / Restart / Stop. While idle, the picker offers Bank, Warband, Guild and One-sided. It opens beside the ledger window (`B:GetWindow()`), never over it. Its position is **window state** in the profile (`settings.simPanel.point`, absent until dragged, written only by the panel host), added to the window-state list in `docs/ARCHITECTURE.md:78-85` and `docs/schema.md`. Run-all step delay: a fixed `SIM_STEP_DELAY = 1.5` s, raised to each step's `settle`. There is no settings row in v1.
- **Marker (preview-mode rule, v2.86.0):** the ledger window's `W.TestStrip` (adopted in this run, replacing `Browser.lua:992-997`) shows `Simulation: <scenario> - nothing here is saved` in its own tone. The **session window** gets the same strip while `simLog` is set, because it draws sim rows. Both read one predicate (R5).
- **Slash** (`NS.COMMANDS` row; a feature verb, refused while disabled; help: "Simulate bank visits through the real capture engine; `/bl sim` for its verbs"):
  - `/bl sim`: status line, and opens the panel.
  - `/bl sim start <bank|warband|guild|onesided>`: refusals per §6. Opens the ledger window and the panel.
  - `/bl sim step|run|pause|resume|restart|stop|panel`.
  - Each prints one line, for example `Simulation step 3 of 9: deposit 20 × Linen Cloth to Warband Bank (1 recorded).`
  - No manual per-driver verbs in v1. Click-ahead covers ad-hoc use.
  - `docs/slash-dispatch.md` gets the rows.
- **Debug:** a `Sim` tag. One line per fired event (`event BANKFRAME_OPENED`), per guarded query, and per start, stop and refusal (with its guard). Engine lines (`[Store]`, `[Diff]`, `[Move]`, `[Skip]`) are unchanged; they are the evidence.
- **Diagnostics:** a `sim` section in `modules/Diagnostics.lua:286-289` covering active, scenario, step pos/total, current character, simLog rows, events fired, guarded queries and seam key count. Add a `simulation=` line to `X.State` (69-79). `/bl debug scan` prints a sim header (R9).

---

## 9. Refactors Bank Ledger needs first (host contract), in order

| # | Change | Where | Size |
|---|---|---|---|
| R0 | Re-vendor LibKa0s v1.75.0 (Sim-1.0, step panel, `W.TestStrip`, `W.SearchBox`, kit 41) through `/dev-copilot:wow-revendor-libka0s`. Roll the provenance line `CLAUDE.md:42-44` (also fixing the stale "kit revision 38"), add the `LibKa0s icons:` line, and regenerate `docs/test-cases.md` | libs/, tests/_kit/ | per the sweep |
| R1 | **One dispatch table.** `L.HANDLERS = { BANKFRAME_OPENED=…, BANKFRAME_CLOSED=…, BAG_UPDATE_DELAYED=…, PLAYERBANKSLOTS_CHANGED=…, PLAYER_MONEY=…, GUILDBANKBAGSLOTS_CHANGED=…, ADDON_LOADED=…, GUILDBANK_FRAME_SHOWN=…, GUILDBANK_FRAME_HIDDEN=… }` and `L:Dispatch(event, …)`, which returns 0 when not `_enabled` and runs the real-frame auto-stop of §6. `Enable` registers each **client** event as `function(e, …) L:Dispatch(e, …) end`. The two hook closures call `L:Dispatch("GUILDBANK_FRAME_SHOWN"/"…HIDDEN")` after their stand-down check, which stays in the hook (the sanctioned one-way-hook gate, 667-670). The two pseudo-event names are documented as host-internal. Behaviour must not change: the existing ledger, guild-bank, settling, disabled and debug-coverage suites stay green unedited | `modules/Ledger.lua:803-867`, 671-688 | ~+25 / −15 |
| R2 | **Identity through Compat:** `Compat.PlayerName()` → name, realm (the ladder from `Util.lua:7-9`) and `Compat.PlayerClass()` → classFile. Callers: `Util.PlayerKey`, `Ledger.lua:342`, `SessionWindow.lua:211`. Update `docs/compat-layer.md` (export count 13 → 15, a "Player" row, and the reason: the simulator's seam answers them) | `core/Compat.lua`, three callers | ~+20 |
| R3 | **Write sink:** `Database:Sink()` = `State.simLog or db.global.ledger`. `Add` appends to it (stamping `sim = true` when simLog is set). `ActiveLedger` puts `simLog` first. `core/Database.lua` is at 990 lines, so with these 4-6 lines it stays under the 1000 band. If anything else lands there, peel the Stats accumulators (510-866) into `core/DatabaseStats.lua` first | `core/Database.lua:385-409` | ~+6 |
| R4 | `SessionWindow:PruneMissing` walks `Database:Sink()` | `modules/SessionWindow.lua:176` | 1 |
| R5 | **One dataset predicate:** `Database:DatasetKind()` → `"live"\|"test"\|"sim"`. Callers that today ask `IsTestMode()` for "synthetic": `Browser_Views.lua:28` (all characters), `:246` (stock baseline), `LedgerTable.lua:859` (row menu), and the strip text (`Browser.lua:740-743` after TestStrip) | 4 sites | ~+8 |
| R6 | Test-mode start refused while a sim runs | `LedgerTable_TestMode.lua:243-252` | ~+3 |
| R7 | Stop hooks: `NS.Sim.Stop("standDown")` as the first line of `NS.StandDown`; `Stop("combat")` in `OnCombatChanged` | `core/BankLedger.lua:255,306-317` | ~+6 |
| R8 | TOC: `core\SimSetup.lua` straight after `core\Compat.lua` (TOC:38), commented **LOAD-BEARING**: it wraps every Compat member at load, before any file could take one. Modules `Sim`, `SimWorld`, `SimDrivers`, `SimScenario` after `modules\Ledger_Diagnose.lua` (TOC:86), conventional | `BankLedger.toc` | ~+10 |
| R9 | `/bl debug scan` sim header line | `modules/Ledger_Diagnose.lua` | ~+3 |

**Degradation:** if `LibStub("LibKa0s-Sim-1.0", true)` is nil, `SimSetup` wraps nothing and `/bl sim` prints "The simulator needs LibKa0s-Sim-1.0." This needs a Sim stub row in `tests/test_surface_parity.lua`, following the per-major convention there (57-286).

---

## 10. New files and size

| File | Holds | Est. lines |
|---|---|---|
| `core/SimSetup.lua` | the seam (pure/guarded lists, guarded query), degradation | 80 |
| `modules/Sim.lua` | the session host: refusal, deliver = `L:Dispatch`, start (Live reads, pool, simLog, dataset swap, window and panel open), the ordered stop, auto-stop entry points, status | 230 |
| `modules/SimWorld.lua` | the world model and every provider | 280 |
| `modules/SimDrivers.lua` | the §3 drivers (world mutation plus event sequences) | 230 |
| `modules/SimScenario.lua` | the 4 scenarios, the timeline adapter, step lines and tips, the panel row and picker adapter, the `/bl sim` sub-verbs | 300 |
| Refactors R1-R9, COMMANDS row, Diagnostics section, strip text | — | ~130 |
| **Runtime total** | | **~1,250** (Drop Watcher: 3,412; no roster, journal or inspect) |

**Tests**, about 1,500 lines:

- `test_sim_seam.lua`: every function member wrapped except the pure three; guarded query never reaches the mock's `QueryGuildBankTab` during a sim; `Live` bypass; an inactive seam is live.
- `test_sim_world.lua`: provider shapes match Compat's triple; queried-tab rule; visibility strictly boolean; nil guild money while hidden; identity switch.
- `test_sim_session.lua`: each refusal and its line; each auto-stop (a real open not delivered by `Fire`, combat, stand-down); stop order (no Reconcile after the seam goes off; pending debounce canceled); test mode refused while a sim runs; panel position write only on drag.
- `test_sim_scenario.lua`: timelines are pure; step/run/pause/resume/restart/RunTo; a typed step repaints the panel; verbs.
- `test_sim_e2e.lua`, the acceptance suite:
  - Each scenario runs against a mock whose **real** containers, money and guild hold *different* contents, with the real frames closed. That proves the sim's answers win.
  - Driven by `__fireTimers` and `__now`.
  - Asserts the exact sim rows (store, direction, kind, quantity, char, classFile, guild, link).
  - Asserts `db.global.ledger` is deep-equal and `Count()` is unchanged.
  - Asserts `SessionWindow` received the rows; issue #12 does not arm; the `[Diff]` hold and settle lines for `warband`; 0 rows for `onesided`; and the dataset back on live after stop.
- Extend `test_disabled`, `test_surface_parity`, `test_slash`, `test_compat`, `test_ledger` (each registered event's handler is `L.HANDLERS`'), `test_debug_coverage` (the `Sim` tag), `test_diagnostics` and `test_docs` (counts).

Run the green gate: `lua tests/run.lua`, `luacheck .` at 0/0, and every authored file under the cap.

**Docs:**

- README simulator section.
- `docs/ARCHITECTURE.md`: module map, load order, window states, a sim paragraph under the data model.
- `docs/module-map.md`, `docs/compat-layer.md`, `docs/slash-dispatch.md`, `docs/schema.md`, `docs/data-flow.md`.
- `docs/performance.md`: the seam costs one boolean test per Compat call, about 3,200 per full reconcile pass. That is negligible, and the sim adds no combat path because it is refused in combat and stops on combat. The performance-§12 exemption stands.
- A new **SIM** theme in `docs/smoke-tests.md`, owed and never marked passed by an agent: start/stop and each refusal; each scenario filling History, Insights and the Session window under the marker; the warband hold settling; guild data while away not arming; a real bank open auto-stopping; `/reload` ending it; the real ledger count unchanged after stop; panel click-ahead; an unguilded character running `guild`.

---

## 11. What this does not do

It does not simulate real item moves, mail, currencies (not captured, `core/Constants.lua:51-55`), the login backfill, or the retention prune. It adds no launcher entry and no settings row. It never writes `db.global.ledger`, and never makes a real guild-bank query while a sim runs.
