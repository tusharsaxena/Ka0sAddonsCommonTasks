# Smoke tests: LootHistory + BankLedger WoW Forever port

The owner's in-game checks for this run, rolled up from LootHistory `docs/smoke-tests.md` (`## WoW Forever`, the
FOREVER checks), BankLedger `docs/smoke-tests.md` (`## WoW Forever`), and both addons' `docs/forever-probes.md`. Each
addon's own file holds the full steps and an empty `Result:` line, and the owner records results there. This sheet is
the index and the status board. Every status is **owed**. Only the owner runs these and only the owner marks them;
an agent never does.

Ids: `LH-F<n>` = LootHistory FOREVER-n, `BL-F<n>` = BankLedger FOREVER-n, `LH-P<n>` / `BL-P<n>` = a probe in that
addon's `forever-probes.md`, `PW-<n>` = a step of the probe walk-through below, `REV-<n>` = checks the reviews added.

**Setup.** On the Forever client, link each repo folder as `<WoW>\_forever_\Interface\AddOns\LootHistory` and
`...\BankLedger`. You need a character with a surname ("First Surname") and a second character on the same account,
a character bank with at least one bag tab bought, a guild bank you can deposit to, some gold, and a key on the
keyring. A check fails on any Lua error.

## 1. Probe walk-through (run first, WoW Forever)

One play session with both probes running answers most of the probe sheets. After logout the lead reads
`_forever_/WTF/Account/<account>/SavedVariables/LootHistory.lua` and `BankLedger.lua` (`global.probe`), and fills in
nothing on the owner's behalf.

| Id | Client | Steps | Expected | Status |
|---|---|---|---|---|
| PW-1 | Forever | `/lh debug probe start` and `/bl debug probe start`. | Each answers one line naming `forever` and the build. | owed |
| PW-2 | Forever | **Banker visit**: open the bank, wait 5 s, move one item in and out, close it. Then open it a second time. | LH: `interaction`, three `bank` entries (phase 0/+1 s/+3 s) and `cue` entries. BL: an `interaction` and three `bank` entries (phase 0, 1, 3), plus `event` entries. | owed |
| PW-3 | Forever | **Loot a mob solo**, then in a dungeon. | LH `chat` and `loot` entries (P4); the zone-in writes an `instance` entry (P11). | owed |
| PW-4 | Forever | **Group roll**: on group loot, win a Need or Greed roll. | LH `chat` holds the raw roll-won line, led by the `HlootHistory:N` link and then `[Loot]: You won: <link>` (P8). | owed |
| PW-5 | Forever | **Currency transfer** to the alt, if any currency is transferable. | LH `transfer` entry, field by field (P5). Note it if nothing can be transferred. | owed |
| PW-6 | Forever | **Trade**: open a trade with another player. | LH `trade` entry with `UnitName("NPC")`'s two answers (P7). | owed |
| PW-7 | Forever | **Mail**: send a mail to the alt, typing its "First Surname". | LH `mail` entry, the recipient as typed and as keyed (P7). | owed |
| PW-8 | Forever | **Guild vault**: open it, wait 5 s, deposit and take back an item, click through the tabs. | BL `interaction` (GuildBanker), three `guild` entries, and whether a `GUILDBANKFRAME_OPENED` `event` appears (P6). | owed |
| PW-9 | Forever | `/reload`, then open the bank once more. | BL: a fresh `start` entry (its probe resumes). LH: its probe is session-only, so `/lh debug probe start` again first. Then `bank` entries for the visit right after the reload (P1 late load). | owed |
| PW-10 | Forever | `/lh debug probe status` and `/bl debug probe status`, then `stop` on both, then **log out**. | Each status answers one line under its cap (LH 500, BL 200). After logout both SV files hold the client stamp and the entry kinds above, with a `start` entry still present. | owed |
| PW-11 | Retail | Repeat PW-1, PW-2 and PW-10 on Retail (the "both clients" probes P1, P2, P3's -1, P9, P-SKIN, P6). | Records stamped `retail`. | owed |

## 2. LootHistory on WoW Forever

| Id | Client | Steps | Expected | Status |
|---|---|---|---|---|
| LH-F1 | Forever | Install: check the AddOns list, log in, `/reload`, `/lh version`, `/lh diagnostics`, `/lh debug events`, then make a new profile. | Listed and not out of date (`120105, 16001`); no Lua error; events `none` (P12); a fresh profile wears **WoW Forever**. | owed |
| LH-F2 | Forever | No Warband: settings tooltips, `/lh help`, Holdings after a banker visit, the Source filter, Insights reasons, Bound column, exports. | No Warband or Warbound word anywhere (the Bound header tooltip included, after LH-REV); Account / Account Bound instead; no Warband column or split. | owed |
| LH-F3 | Forever | Record data from, the Source filter, a dungeon boss, then disenchant an item. | No Mythic+, Bonus Roll, Milling, Prospecting, Deconstructed or Warband Deposit/Withdraw. Materials read **Disenchant**. Record which reason the disenchanted item's loss reads (an owner ruling is open). | owed |
| LH-F4 | Forever | `/lh test`, then Insights and its CSV; `/lh diagnostics`; `/lh sim start key`. | No Mythic+ slice or By Keystone section; no `attribution: keystone` line; `key` is refused, and the picker lists loot, vendor, ah, bank, social. | owed |
| LH-F5 | Forever | Two-word names: loot on two characters, mail the alt, trade, then check the Insights bars. | The whole "First Surname" with no realm everywhere; **Alt Mail** for the alt; a truncated bar shows the whole name on hover. | owed |
| LH-F6 | Forever | Bank and keyring: open the bank, deposit a stack, reopen it in the same session and again after a relog, then move keys. | The Bank column fills; a deposit is one Transfer; no Untracked row when nothing changed (even on the first open after login); keys count in Bags; record whether a key can go into the bank (P3); note what a socketed bag shows (R6). | owed |
| LH-F7 | Forever | Win a group roll. | The row reads **Roll**, named for the item and never `[Loot]`. | owed |
| LH-F8 | Forever | Sell to a vendor and loot coin. | Coin glyphs in History, Holdings, the Timeline and Insights; the CSV still writes `Ng Ns Nc`. | owed |
| LH-F9 | Forever | Export the History CSV and open a `wowheadLink`. | `https://www.wowhead.com/forever/item=<id>`, and it opens the same item. | owed |
| LH-F10 | Forever | `/lh test`. | Nine classic classes, "First Surname" samples, Stormwind-area zones, Forever item names, no warband holder, the Timeline opens on Arcane Crystal. | owed |
| LH-F11 | Forever | `/lh sim start` loot, bank, social and vendor, then `/reload`. | A Defias Thug in Stormwind City; the bank is the character bank only; alt `Sampleblade Mockvale` with Alt Mail and Alt Trade; Disenchant; no simulated row left after the reload. | owed |
| LH-F12 | both | The probe session (PW-1..PW-11), plus `/lh sim start loot` while the probe runs. | The record is stamped and holds the start/interaction/bank/cue/chat/stop kinds; nothing is recorded during a sim; a start during a sim is refused. | owed |
| LH-F13 | Forever | Run every `both` theme check that is not tagged `Client: Retail.` on Forever. | Each Forever result goes on that check's own Result line; steps that need something absent are skipped. | owed |

## 3. BankLedger on WoW Forever

| Id | Client | Steps | Expected | Status |
|---|---|---|---|---|
| BL-F1 | Forever | Install: AddOns list, `/reload`, `/bl version`, `/bl show`, `/bl diagnostics`, `/bl debug scan` at a banker. | Not out of date; no Lua error; copy any UNAVAILABLE event onto the Result line (P12). | owed |
| BL-F2 | Forever | Banks to record grid, the Record gold tooltip, the Insights gold cards, the Store dropdown, `/bl debug scan` groups. | Character Bank and Guild Bank only; the tooltip names the guild bank; no `group WARBAND_BANK`. | owed |
| BL-F3 | Forever | `/bl sim start warband`, the idle step panel, then the `onesided` run. | `Unknown scenario 'warband'. Scenarios: bank, guild, onesided.`; no warband step. | owed |
| BL-F4 | Forever | `/bl test`, then `/bl session` away from a bank. | No Warband Bank rows; "First Surname"; a Warlock and no Evoker; the classic capitals; the gold row is on Guild Bank. | owed |
| BL-F5 | Forever | Deposit and withdraw at a banker in tab 1 and in a bought bag tab, then sell to a vendor. | Correct Deposit and Withdraw rows to Character Bank; no gold row at the character bank. | owed |
| BL-F6 | Forever | `/bl debug scan`, then move keys between the keyring and the bank, and between the keyring and the backpack. | `group BAGS = [-1, 0, 1, 2, 3, 4, 5]`; keyring to bank is a Deposit (if the client allows it); keyring to backpack writes no row. | owed |
| BL-F7 | Forever | `/reload`, open the bank and move an item at once; repeat on a second open. | Exactly one Deposit and one Withdraw; the console shows `bank not ready` then `bank ready after Ns` (or the re-anchor line); no phantom rows. | owed |
| BL-F8 | Forever | Socket a bag into a bank tab, take it out, then deposit into the bag-backed tab. | No row for the socket; one Deposit for the item. | owed |
| BL-F9 | Forever | Names: the Character column, header tooltip, dropdown and Insights bars. | The whole "First Surname"; "full name and surname"; `…` on a cut label with the full name on hover. | owed |
| BL-F10 | Forever | Make a fresh profile and `/reload`. | The picker preselects WoW Forever; an older stored skin is kept. | owed |
| BL-F11 | Forever | CSV export, the `wowhead` cell. | `https://www.wowhead.com/forever/item=<id>`, the right item; a gold row's cell is empty. | owed |
| BL-F12 | Forever | `/bl sim start bank`, pause, `/bl debug scan`, step through, stop. | Two bank tabs, `6: 24` and `7: 16`; SIM-1's three rows; the real history comes back. | owed |
| BL-F13 | Forever | CAPT-9, -10 and -12 at a guild vault; click through its tabs. | Guild Bank rows with the guild name; no row for a tab that is only loading; the session window opens and closes with the vault. | owed |
| BL-F14 | both | The probe verbs: status, start, a bank visit, stop, clear, start while disabled, bare `probe`. | One chat line each; three `bank` entries (phase 0, 1, 3) per visit; refused while disabled. Record Forever and Retail separately. | owed |
| BL-F15 | Forever | Run the rest of the file on Forever, except CAPT-4, CAPT-5, CAPT-8, SIM-3, SIM-10 and SESS-5, and the warband steps of CAPT-20, LEDG-22, SESS-8 and SIM-14. | Each result goes on that check's own Result line. | owed |

## 4. Retail regression checks (R8 changes)

R8 changed Retail on purpose, with one commit per fix: LH `CharacterBanker` arming (LH-09), the readiness guard and
`CanViewBank(Character)` (LH-10, BL-07), and the money text (LH-11, BL-08). LH-11's roll-won parse runs on both clients.

| Id | Client | Steps | Expected | Status |
|---|---|---|---|---|
| LH-F14 | Retail | LED-2 and TR-2 at a banker; reopen in the same session and after a relog; deposit in the first seconds; a warband-only (`AccountBanker`) visit with the probe running. | The Bank and Warband columns fill; a deposit is one Transfer; no Untracked rows; at the warband-only banker the tabs read and the character Bank column keeps its count and age. | owed |
| LH-F15 | Retail | Check money in every window; win a group roll. | Coin glyphs as before, the same size; the roll reads **Roll** (CAP-9). | owed |
| LH-F16 | Retail | The presence side of LH-F2..F5 and LH-F9..F11. | Warband wording, column and holder; Mythic+, Bonus Roll, Milling, Prospecting and Warband Deposit/Withdraw offered; Warbound; the keystone diagnostics line; `key` runs; the Retail Wowhead URL; `Name-Realm`; Ka0s Default; TM-3's sample and Everlight Crystal; a Rookery Bat. | owed |
| BL-F16 | Retail | CAPT-1, -2, -4 and -5 at an ordinary banker with `/bl debug on`. | The same rows as before; a `bank not ready` line after a `/reload` is followed by `bank ready after Ns`. | owed |
| BL-F17 | Retail | Move items at a warband-only access point, then at an ordinary banker. | Only Warband Bank rows; `BANK not viewable at this banker (CanViewBank(Character) false): not read`; no whole-bank rows afterwards. If Retail has no such access point, record that (the check would be retired). | owed |
| BL-F18 | Retail | `/reload`, open, close, reopen and move one item at once. | Exactly one Deposit and one Withdraw. | owed |
| BL-F19 | both | Move gold at a coin bank (warband or guild on Retail, guild on Forever). | Coin icons in the Qty, the tooltip, the session window and the Insights cards. Record Forever and Retail separately. | owed |

## 5. Checks the reviews added

| Id | Client | Steps | Expected | Status |
|---|---|---|---|---|
| REV-1 | both | LH-REV fix 1: at a banker, withdraw an item in the first second after opening (while tabs still load). | One MOVE, with no UNTRACKED OUT and no one-sided IN. | owed |
| REV-2 | Forever | LH-REV fix 2: a character's first-ever bank visit with several bought tabs. | No gain rows for tabs that finish loading late. Depends on `FetchNumPurchasedBankTabs` existing (P2). | owed |
| REV-3 | Forever | BL-REV fix 1: `/bl debug on`, `/reload`, then open the bank while the socketed tabs read 0. | `baseline deferred until the bank is ready`; no phantom rows. | owed |
| REV-4 | both | BL-REV fix 5: `/reload` with a probe started. | A fresh `start` entry per login; the newest `start` survives the cap. | owed |

## 6. Probe sheets (what the lead reads from the SV files)

Both addons record a `Result:` line for each probe in their own `forever-probes.md`. Status is owed until the owner's session is read.

| Id | Client | Fact | Safe default shipped | Status |
|---|---|---|---|---|
| LH-P1 / BL-P1 | both | The banker's interaction type; bank slots at open, +1 s and +3 s; cue events. | Arms on Banker / CharacterBanker (AccountBanker Retail-only, LH); readiness waits 5 s (LH) / 6 s (BL). | owed |
| LH-P2 / BL-P2 | both | `CanViewBank(0/2)`, purchased and max tabs, `ShouldUsePlayerBagsInBank`, deposited money, slots -3..23. | Warband Retail-only; character bank = `CharacterBankTab_*` by name; BL sim base tab 24. | owed |
| LH-P3 / BL-P3 | Forever (Retail -1) | Keyring slots and contents, `ContainerIDToInventoryID(-1)`, key into the bank. | Keyring in BAGS on Forever only; no keyring-to-bank pairing in LH. | owed |
| LH-P4 | Forever | Loot line shapes, self-chat sender form, loot-source GUIDs. | Retail parsers; the sim sends the first name. | owed |
| LH-P5 | Forever | Currency account flags (1792, 3402), `destinationCharacterName` form. | Per character; the destination is used as given. | owed |
| BL-P6 | both | The guild vault reads, whether `GUILDBANKFRAME_OPENED` fires. | Guild bank on both clients (D7). | owed |
| LH-P7 | Forever | Trade partner and mail recipient forms. | `UnitCharacterName("NPC")`; typed name kept whole. | owed |
| LH-P8 | Forever | Roll-won raw line. | The `%s` capture. | owed |
| LH-P9 / BL-P9 | both | Which money functions exist. | `C_CurrencyInfo` → `GetMoneyString` → text. | owed |
| LH-P10 / BL-P10 | Forever | Socket (-2) reads. | Not scanned (R6). | owed |
| LH-P11 / BL-P11 | Forever | Instance difficulty ids; capitals' uiMapIDs. | Stored raw; Forever capitals 1453-1458. | owed |
| LH-P12 / BL-P12 | Forever | A clean load. | n/a. | owed |
| BL-P-NAME | Forever | `regionalNames`, `characterKey` timing, the longest surname. | "First Surname", not nil, by first record; dropdown 180 px. | owed |
| BL-P-SKIN | both | `defaultSkin`. | `forever` / `ka0s`. | owed |
| BL-P-WOWHEAD | Forever | Whether `?bonus=` is accepted. | Appended when there are bonus ids. | owed |
| LH-Q1..Q5 | Forever | The name of spell 13262; `LOOT_ITEM_BONUS_ROLL_SELF`; the sender form; whether a surname can contain a hyphen; whether Waylaid Crate 248683 opens. | 13262 = Disenchant; parser safe either way; first name; no hyphen; openable. | owed |
