# Execution record: LootHistory + BankLedger WoW Forever port (2026-11-22)

Branch `feat/2026-11-22-forever-port-lh-bl` in LootHistory, BankLedger, WowAddonStandards and this repo. The plan is
`00_DESIGN.md` and `plan-data/items.tsv`, which stay frozen; this file records what happened. Progress comes from git
(`plan-data/resume-state.sh`): 33 of 34 items were done before this record, and CT-REC is this record's own commit.

- **Build workflow:** `forever-port-lh-bl-build` (run `wf_82fca5b9-b52`), script
  `~/.claude/projects/-mnt-d-Profile-Users-Tushar-Documents-GIT-Ka0sAddonsCommonTasks/cc9586a8-8986-4d94-9659-95fca377c5ee/workflows/scripts/forever-port-lh-bl-build-wf_82fca5b9-b52.js`.
  Research ran earlier as `forever-port-lh-bl-research` (its output is `inputs/research/`).
- **Blocked items:** none. **Exceptions** (`plan-data/exceptions.tsv`): none.
- **Not yet done (lead):** checkpoint CP-1 (a `checkpoints.tsv` row, push with the `refs/notes/ka0s-review` notes) and
  `/dev-copilot:finalize` in the order WowAddonStandards, LootHistory, BankLedger, Ka0sAddonsCommonTasks. No version
  bump, no tag (R3).

## Item id collisions with older history

Every LH-NN and BL-NN id used here also appears in older commits on `master`, left by earlier bundles that used the
same ids. Each item agent found them with its idempotency grep, saw that none were in `master..feat/2026-11-22-forever-port-lh-bl`,
and did the item. `resume-state.sh` reported the right state for this run. Any later tool that checks these ids must
look only at `master..<branch>`, and after the merge only at the merge's second parent range.

## What was built

### LootHistory (M1)

| Id | Commit | What |
|---|---|---|
| LH-01 | `8b10010` | New `core/CompatClient.lua` routes IsForever / IsRetail / ClientKey / ForClient / RegionalNames / UnitCharacterName / CharacterKey / RealmKey from LibKa0s-Compat, with stubs for when the library is missing. A static gate bans `WOW_PROJECT_*`, `RegionalUniqueNamesEnabled` and `GetBuildInfo` in every other file. |
| LH-02 | `007bf9a` | Test mock shaped per kit profile: Forever BagIndex (tabs 6..14, account 15..23, Keyring -1), `CharacterBanker` 67, a two-word UnitName, RegionalUniqueNamesEnabled, `C_Bank.CanViewBank`. Helpers `T.forever` and `T.bagIndex`. |
| LH-03 | `57ec654` | On regional names, `Util.PlayerKey`, `QualifyName`, `TradeTargetKey` and `LatestCurrencyTransfer` key characters by "First Surname" with no realm. Helpers `T.ME` and `T.nameKey`. |
| LH-04 | `73cf2b4` | `NS.DEFAULT_SKIN = Skin:DefaultSkin()` is the profile's skin default (WoW Forever on Forever). Helper `T.ka0sDefault` for cases that pin pixels. |
| LH-05 | `e4cea7a` | Sample identity, test data and sim seeds per client: Forever classes, Stormwind-area zones, 1.x items, currencies, Defias Thug kill, `Sampleblade Mockvale`. |
| LH-06 | `8184cbb` | Warband bank Retail-only (`C.FEATURE.warbandBank`, R1); `C.ACCOUNT` words ("Account" / "Account Bound" on Forever); WARBAND_DEPOSIT/WITHDRAW gated through `C.SOURCE_CLIENTS`. Helpers `T.RETAIL_ONLY` and `T.retailWords`. |
| LH-07 | `7995bc8` | MPLUS (with the keystone context, Insights byKeystone, diagnostics line and the sim `key` scenario), BONUS_ROLL, MILLING, PROSPECTING and DECONSTRUCT are absent on Forever (R2). Deconstruct seeds per client (D15: Forever keeps only Disenchant 13262). |
| LH-08 | `3751268` | `C.CONTAINER_GROUPS_BY_CLIENT`: the Keyring (-1) is in BAGS on Forever only (R5). |
| LH-09 | `3bb1838` | R8, both clients: the bank part arms on `CharacterBanker`; `AccountBanker` arms it on Retail only. |
| LH-10 | `76022d9` | R8, both clients: per-container bank readiness guard (`R:BankState`, `meta.bankSlots`, `R.READY_WAIT` = 5 s), `Compat.CanViewCharacterBank`, and `BAG_CONTAINER_UPDATE` / `BANK_TABS_CHANGED` re-read cues. |
| LH-11 | `49f984e` | R8, both clients: money text goes `C_CurrencyInfo.GetCoinTextureString`, then `GetMoneyString`, then text. `ParseRollWon` takes the `%s` link capture (Forever's `|HlootHistory:%d|h` prefix). |
| LH-12 | `7b93b8c` | Per-client Wowhead base (R7) and key-form wording. Tests pin that two-word names are drawn whole on every surface. |
| LH-13 | `f234ae7` | `/lh debug probe start|stop|status|clear` (R4) records into a capped `db.global.probe` (500 entries). New `modules/Probe.lua`, `Compat.ClientBuild()` and `docs/forever-probes.md`. |
| LH-14 | `60ddc12` | Shape: TOC `## Interface: 120105, 16001`, README badge and sentence, both runs named in the gate, `docs/forever-quirks.md` (catalog v2.117.0 plus its own section), the ARCHITECTURE per-client table (22 rows), `tests/test_client_shape.lua`. |
| LH-15 | `1357b4a` | `docs/smoke-tests.md`: a Client column per theme, a `## WoW Forever` theme FOREVER-1..13 and R8 Retail checks FOREVER-14..16, with a doc-shape test. |
| LH-REV | `e204308` | Review fixes, 7 of 9 confirmed (see Reviews). |

### BankLedger (M2)

| Id | Commit | What |
|---|---|---|
| BL-01 | `985b391` | New `core/CompatClient.lua` with the same eight members. They are PURE to the sim seam. |
| BL-02 | `17636d2` | Forever-shaped mock (27-member BagIndex, surname "Mockvault", CanViewBank), sample identity per client. Fixes the 5 forever-profile failures that were already there. |
| BL-03 | `b97f18d` | One record-key builder: `Compat.PlayerName` answers "First Surname" on regional names, `Util.RecordKey` does the join, and SimWorld keys through it. |
| BL-04 | `78b1f3b` | `NS.DEFAULT_SKIN` per client. Helper `T.onKa0sDefault`. |
| BL-05 | `72b473f` | Warband Bank Retail-only (R1): store order, settings grid, container groups, bank-frame reach, coin stores, copy (`C.COIN_BANKS_TEXT`), test mode, session preview, sim scenario. Helper `T.WARBAND_ONLY`. |
| BL-06 | `de9de43` | `C.BAG_PATTERNS_BY_CLIENT`: the Keyring is in BAGS on Forever only (R5). |
| BL-07 | `11906f4` | R8, both clients: per-container readiness guard (`L:CheckReady`, `L.UnreadyContainers`, 6 s deadline), `Compat.CanViewCharacterBank`, and the `BAG_CONTAINER_UPDATE` / `BANK_TABS_CHANGED` cues. |
| BL-08 | `a2f5b84` | R8, both clients: money text goes `C_CurrencyInfo.GetCoinTextureString`, then `GetMoneyString`, then text. |
| BL-09 | `f05699d` | Test-mode and sim seeds per client: Warlock in the Evoker's place, classic capitals 1453-1458, bank tabs of 24 + 16 slots, no warband coin. |
| BL-10 | `4bda00e` | Character dropdown 140 / 180 px per client, UTF-8-safe `W.Truncate`, per-client Character column copy. |
| BL-11 | `fc43581` | Per-client Wowhead base (R7). |
| BL-12 | `2290ee2` | `/bl debug probe start|stop|status|clear` (R4) into a capped `db.global.probe` (200 entries). New `modules/Probe.lua`, `docs/forever-probes.md`. It adds guild-vault reads (P6). |
| BL-13 | `095c00a` | Shape: TOC `120105, 16001`, README, both runs in the gate, `docs/forever-quirks.md` (12 own rows), ARCHITECTURE per-client table, `tests/test_clients_shape.lua`. |
| BL-14 | `09ceb5c` | `docs/smoke-tests.md` `## WoW Forever`: FOREVER-1..15 and R8 Retail checks FOREVER-16..19, with a structural test. |
| BL-REV | `dec3063` | Review fixes, all 5 confirmed (see Reviews). |

### WowAddonStandards (M3)

| Id | Commit | What |
|---|---|---|
| STD-01 | `2d7a05f` | `standards/ADDONS.md`: the Ka0s Bank Ledger (line 21) and Ka0s Loot History (line 27) rows go from `Retail (port pending)` to `Retail · Forever`. No version bump. `scripts/check-standard.sh` passed. KickCD and MultiMeters are now the only rows still marked port pending. |

## Test totals

Every run used `ka0s-bounded`. `luacheck` was 0 warnings / 0 errors at every item, and no shipped file was above 1500 lines.

| Repo | Point | Retail (`lua tests/run.lua`) | Forever (`KA0S_KIT_CLIENT=forever`) | luacheck files |
|---|---|---|---|---|
| LootHistory | first item (LH-01, `8b10010`) | 2063 passed, 0 failed, 1 skipped (2064) | 2063 passed, 0 failed, 1 skipped (2064); before LH-02 this run used the Retail mock, so it was not yet testing Forever | 168 |
| LootHistory | end of build chain (LH-15, `1357b4a`) | 2145 passed, 0 failed, 1 skipped (2146) | 2125 passed, 0 failed, 21 skipped (2146) | 171 |
| LootHistory | after review fixes (LH-REV, `e204308`) | 2149 passed, 0 failed, 1 skipped (2150) | 2129 passed, 0 failed, 21 skipped (2150) | 171 |
| BankLedger | baseline before BL-01 | 1724 (README badge) | 1719 passed, 5 failed | 127 |
| BankLedger | end of build chain (BL-14, `09ceb5c`) | 1833 passed, 0 failed, 3 skipped (1836) | 1812 passed, 0 failed, 24 skipped (1836) | 136 |
| BankLedger | after review fixes (BL-REV, `dec3063`) | 1841 passed, 0 failed, 3 skipped (1844) | 1820 passed, 0 failed, 24 skipped (1844) | 136 |

The Forever skips are declared Retail-only cases (`T.RETAIL_ONLY` in LH, `T.WARBAND_ONLY` in BL), plus the existing
diagnostics opt-out case. After the reviews the complexity suite reports 0 warnings and a maximum CCN of 15 in both
addons. The suite was run in scratch copies or reverted, so no automated-tests bundle was committed.

## Reviews

Each review is a `refs/notes/ka0s-review` note on its fix commit: LootHistory `e204308`, BankLedger `dec3063`.

### LH-REV: 9 findings, 7 confirmed and fixed, 2 rejected

| # | Where | Finding | Verdict |
|---|---|---|---|
| 1 | `modules/Reconciler.lua:754` (medium) | A bag/bank move made while the bank loads was booked as an UNTRACKED OUT plus a one-sided IN. | Confirmed. The whole Flush now waits while the drift read waits (login passes are exempt), and the waited drift pass also reads the bags, so the move pairs as one MOVE. Side effect: a bag change during the wait that is not a bank move (for example a potion drunk at the banker) lands as UNTRACKED. |
| 2 | `modules/Reconciler.lua:47` (medium) | A first-ever visit (no `meta.bankSlots`) took a partial genesis. | Confirmed. The bank is "loading" while fewer containers answer slots than `Compat.NumPurchasedCharacterBankTabs()` (a new member). Where that API is absent the first visit stays unguarded. |
| 3 | `modules/Reconciler.lua:30` (low) | A 0 that is still there after READY_WAIT is believed, so a slow tab shows up as an OUT/IN pair. | Rejected: the documented R8 deadline trade-off. Probe P1 measures it. |
| 4 | `core/Compat.lua:1084` (low) | The currency-transfer destination may lack the surname, which would credit a phantom holder. | Rejected: unverified (probe P5, and whether Forever has the transfer API at all). |
| 5 | `modules/BrowserTable.lua:221` (medium) | The Bound column tooltip still said "Warbound" on Forever. | Confirmed. It now uses `C.ACCOUNT.bound`. |
| 6 | `modules/Reconciler.lua:250` (medium) | `R:Scan` was at CCN 18, above the release limit of 15. | Confirmed. The container read moved into a local `readContainer`. |
| 7 | `tests/wow_mock.lua:13` (low) | The mock's top-level function was at CCN 16. | Confirmed. The BagIndex build moved to `bagIndexFor`. |
| 8 | `modules/Probe.lua:123` (low) | The probe cap could drop the `start` entry. | Confirmed. The cap now drops the oldest entry that is not a start entry. |
| 9 | `core/Util.lua:14` (low) | A degraded install (no library) keyed the character by first name only. | Confirmed. The CompatClient stub joins the surname under regional names. |

### BL-REV: 5 findings, all confirmed and fixed

| # | Where | Finding | Fix |
|---|---|---|---|
| 1 | `modules/Ledger.lua:667` (medium) | The shape memory lived only for the session, so the first bank open after a login or `/reload` was never guarded, and that is the Forever late-load case. | The live shape is stored in `db.global.bankShape[<record key>]`, a new SavedVariables key with no default and no migration. A simulated world's memory stays runtime-only. A character's first-ever visit is still unguarded. |
| 2 | `core/Compat.lua:46` (low) | Without the library, two Forever characters who share a first name got the same record key. | The CompatClient stub joins "First Surname". |
| 3 | `tests/test_docs.lua:84` (medium) | A test function at CCN 19. | Split into three local helpers. |
| 4 | `tests/test_ledger_settling.lua:228` (low) | The settle/hold mechanism was not tested on the forever profile. | Four new both-profile cases: three on the character bank, one guild-bank coin deposit. |
| 5 | `modules/Probe.lua:315` (low) | The 200-entry cap could push out the `start` entry. | The newest `start` is never dropped, and `P:Resume` records start facts again at each login. |

## Deviations from the design

- **No member is literally named `PlayerRecordKey`.** LH-03 routes `Util.PlayerKey` through the Compat readers.
  BL-03 puts the regional branch in `Compat.PlayerName` (the identity member the sim seam wraps) and the join in
  `Util.RecordKey`.
- **Seam classification differs.** LH wraps its CompatClient members, as DropWatcher does. BL marks them PURE,
  because its seam needs a SimWorld provider for every wrapped member (BL-01).
- **Readiness deadlines** were added, which the design does not name: LH `R.READY_WAIT` = 5 s, BL
  `L.READY_TIMEOUT_SECONDS` = 6 s. Without them, a bag taken out of a bank socket would block the bank for good.
- **Stored readiness memory:** LH keeps `holdings meta.bankSlots` per character (LH-10). BL started runtime-only and
  moved to `db.global.bankShape` in BL-REV. Both are new SavedVariables fields, documented in each `schema.md`, with no
  migration needed.
- **CanViewCharacterBank answers differently when the API is absent:** LH answers `true`, BL answers `nil` (read as
  readable). The behaviour is the same, but the shapes differ (see the LibKa0s issue draft).
- **LH arms nothing on `AccountBanker` on Forever** (LH-09). The design said "(Retail) AccountBanker", and probe P1's
  safe default had listed all three types.
- **D15:** Forever's deconstruct id list holds Disenchant 13262 (not empty), so Disenchant does not depend on the
  spell's name being cached. With R2 dropping DECONSTRUCT, a Forever disenchanted item's loss falls through to OTHER.
- **LH sources are gated by a declaration table** (`C.SOURCE_CLIENTS` read through ForClient), not by a filtered seed
  list.
- **BL keeps `C.StoreRGB.WARBAND_BANK` on both clients.** Gating it tripped the kit's skin-values gate.
- **Probe lifetime:** LH's probe is session-only (a reload stops it). BL's resumes across logins until it is stopped.
  LH's cap is 500 entries and BL's is 200.
- **Smoke docs tag clients by theme**, not check by check: LH adds an Index Client column, and BL's FOREVER-15 lists
  the Retail-only checks.
- **Small extra fixes:** British spellings caught by the prose gate ("cancelled" from LH-13, "behaviour" from BL-07),
  and BL's README badge, which was already wrong at HEAD before BL-09.

## Followups

### Owner rulings wanted

1. **The loss reason for a disenchanted item on Forever.** It reads OTHER now that DECONSTRUCT is absent (LH-07, LH smoke FOREVER-3).
2. **A hover for truncated History Character cells and the dropdown**, which would change both clients (LH-12).
3. **Whether BL's in-combat probe entry appends count as a combat path under performance-§12** (BL-13). They are
   written up as a debug aid.
4. **Whether an empty Forever "Account" holder should be hidden** from the Holdings and Timeline lists (LH-06).

### Probe-driven (after the owner's session; open a new bundle for any contradiction, R3)

- **P1:** which interaction type a Forever banker sends (a 68 is a finding), bank load timings against 5 s / 6 s,
  which cue events fire, and LH-REV's rejected finding 3.
- **P2:** whether `C_Bank.FetchNumPurchasedBankTabs` exists on Forever (LH-REV fix 2 depends on it),
  `CanViewBank(Character)` at a normal banker on both clients, Retail 6+5 vs 9+9 tabs, and the base tab slot count
  (BL sim 24).
- **P3:** whether a key can go into the bank, `ContainerIDToInventoryID(-1)`, the keyring at login, and Retail -1.
- **P5:** account-wide Forever currencies and the surname in `destinationCharacterName` (LH-REV's rejected finding 4).
- **P7 / P4 / P8 / P9 / P10 / P11:** forms of names, the roll-won line, money text, sockets, map ids (Stormwind 1453 vs 84).
- **Smaller questions:** spell 13262's name, `LOOT_ITEM_BONUS_ROLL_SELF`, whether a surname can contain a hyphen,
  whether Waylaid Crate 248683 opens, the longest surname (BL dropdown 180 px), and whether Wowhead honours `?bonus=`.
- **Once the probes run:** fill in the Measured stamps in both `forever-quirks.md` files. BankLedger is the second
  repo that meets the bank rows, so the next harvest can promote them.

### Code and docs

- **LibKa0s:** file `inputs/LIBKA0S_ISSUE_container-groups.md` (the shared container-group and bank-readiness reader, D11).
- **LH symlink:** the collection has no `symlinks.txt` line for LootHistory's Forever link (LH smoke FOREVER-1 assumes one).
- **LH `--jobs auto`** gives 30 spurious failures on Forever because the suites are not shard-safe. The gate uses the
  serial run.
- **LH:** the `STEPS.key` table and the keystone shim are still built on Forever, though nothing reads them there.
- **LH sim:** the bank scenario opens only `Banker`. Add a `CharacterBanker` variant if P1 shows Forever sends 67.
- **BL test mode:** item names and ids are still Retail's on both clients. The sim backpack is 20 slots and never uses
  the keyring.
- **BL:** the SimWorld Move and sim-panel running cases are declared skips on Forever, so their non-warband checks do
  not run there.
- **BL `W.Truncate`** budgets by bytes, not glyphs.
- **BL smoke FOREVER-17** assumes Retail has a warband-only access point. If it has none, retire or reword the check.
- **Roster:** KickCD and MultiMeters are the only addons still marked `Retail (port pending)`.
- **Smoke:** see `06_SMOKE_TESTS.md`. Everything there is owed.

## Finalize (2026-11-22, lead)

- CP-1 passed and is logged in `checkpoints.tsv`. The feature branches and `refs/notes/ka0s-review` were pushed.
- The finalize doc sync was content-only:
  - LootHistory `97c33e7`: ARCHITECTURE slash row and doc map, testing.md rows and lint count.
  - BankLedger `ae863f4`: a testing.md line.
  - BankLedger `5ee8ce2`: three comment citations repointed from the bundle's `forever-bank.md` to `docs/forever-quirks.md`.
  - WowAddonStandards: nothing to change.
- Merged `--no-ff`, pushed, and the branch deleted on both sides:
  - WowAddonStandards `6e062cf`. check-standard passed; no version bump.
  - LootHistory `6259578`. Retail 2149/0/1, forever 2129/0/21, luacheck 0/0.
  - BankLedger `90f6548`. Retail 1841/0/3, forever 1820/0/24, luacheck 0/0.
  - Ka0sAddonsCommonTasks: this merge.
- No version bump, tag or release.
- Filed LibKa0s#101 (shared container-group and bank-readiness reader) from `inputs/LIBKA0S_ISSUE_container-groups.md`.
- Dead export reported and not removed: LootHistory `modules/Probe.lua` `NS.Probe.IsRunning`, which only tests call.
- Prose drift reported and not fixed: BankLedger `.luacheckrc:100-103` file counts.
- Still owed by the owner:
  - Create the `_forever_` AddOns symlinks for LootHistory and BankLedger. They are listed in `GIT/symlinks.txt` but are not present.
  - Run the probe session and the checks in `06_SMOKE_TESTS.md`.
