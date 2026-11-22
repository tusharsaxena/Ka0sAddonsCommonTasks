# Compat: a shared container-group reader (per client, by Enum.BagIndex member name) and bank-readiness helpers


## Problem

Three addons each carry their own copy of the same two things:

1. **Container groups.** Each turns `Enum.BagIndex` member names into the ids for bags, the character bank and the
   account (warband) bank, and each has a per-client twist: on WoW Forever the keyring (`Keyring`, -1) belongs in
   the bags.
2. **Bank readiness.** The bank frame can open before every bank container has loaded. That is the documented case
   on WoW Forever, and it can also happen after a `/reload` on Retail. A container that read slots last time and
   reads 0 now is "not ready", and a warband-only banker does not show the character bank at all.

The copies:

| Addon | Container groups | Bank readiness |
|---|---|---|
| BankLedger | `core/Constants.lua:124-201`: `C.BAG_PATTERNS_BY_CLIENT` (149-153, `^Keyring$` on Forever only), `GROUP_PATTERNS` (155-160), `idsMatching` (163-180), `C.BAG_IDS` / `BANK_IDS` / `WARBAND_BANK_IDS` (183-187), a numeric `{0..5}` fallback (191), `C.STORE_CONTAINERS` (197-201) | `core/Compat.lua:108` `Compat.CanViewCharacterBank` (answers nil when it cannot tell); `modules/Ledger.lua:638` `READY_TIMEOUT_SECONDS = 6`, `:672` `ShapeMemory` (stored in `db.global.bankShape[<record key>]`), `:697` `L.UnreadyContainers(snap, memory)`, `:737` `L:CheckReady` |
| LootHistory | `core/Constants.lua:368-415`: its header says it was "copied from BankLedger core/Constants.lua". `C.CONTAINER_GROUPS_BY_CLIENT` (379-390, the same patterns, Keyring on Forever only), its own `idsMatching`, and no numeric fallback (the groups degrade to empty) | `core/Compat.lua:857` `Compat.CanViewCharacterBank` (answers true when it cannot tell), `:867` `Compat.NumPurchasedCharacterBankTabs`; `modules/Reconciler.lua:30` `READY_WAIT = 5`, `:43` `firstVisitLoading`, `:53` `R:BankState` (memory in `holdings meta.bankSlots`), `:112-119` `R.READABLE_ON` (Banker, CharacterBanker, and AccountBanker on Retail only) |
| OutfitterReborn | `core/Compat.lua:838-864`: `appendSeries` and `Compat.BankBagIDs` (the `CharacterBankTab_` series when the build has it, otherwise the legacy `Bank` + `BankBag_` series; no warband tabs, no keyring) | `core/Compat.lua:866-872` `Compat.IsBankerInteraction` (Banker or CharacterBanker) |

The copies have already drifted apart:

- **CanViewCharacterBank when the API is absent:** BankLedger answers nil (three-valued) and LootHistory answers true.
- **Fallback when `Enum.BagIndex` is absent:** BankLedger guarantees `{0..5}`, LootHistory degrades to empty, and
  OutfitterReborn returns `{}`.
- **How ids are found:** OutfitterReborn walks numbered series, while the other two match anchored patterns. The
  patterns have to stay anchored and case-sensitive, because `Enum.BagIndex` also carries the type constants
  `Characterbanktab = -2` and `Accountbanktab = -3`.
- **Deadlines and memory:** 5 s vs 6 s, and memory kept per holder vs per record key.

The lesson behind the by-name rule was learnt once already. BankLedger once assumed `AccountBankTab_1 = 13`, which
put warband tab 1 inside the character bank group on 12.0.7 and double-counted every stack. Every new consumer that
writes its own copy risks learning it again.

## Proposal

Add these to `LibKa0s-Compat-1.0`. They are read-only and answer plain values, and each client's table is picked
once by `ClientKey()` (clients-§5) through a declaration, never by detecting a feature.

- `Compat:ContainerGroups()` returns `{ bags = {...}, bank = {...}, accountBank = {...} }`: sorted, de-duplicated
  ids matched by anchored member-name patterns.
  - `bags`: `Backpack`, `Bag_N`, `ReagentBag`, plus `Keyring` on Forever only.
  - `bank`: `Bank`, `BankBag_N`, `CharacterBankTab_N`.
  - `accountBank`: `AccountBankTab_N` on clients that declare the warband bank (Retail), and empty elsewhere. Forever
    numbers 15..23 in the enum, but the bank is not there.
  - Also publish the pattern table, `Compat.CONTAINER_PATTERNS_BY_CLIENT`, so a consumer's tests can pin it.
  - Settle one documented fallback for an absent enum. A guaranteed backpack `{0}`, or `{0..5}`, is the likely choice.
- `Compat:CanViewCharacterBank()`: three-valued, `C_Bank.CanViewBank(Enum.BankType.Character)` read by name, and nil
  when the build cannot tell (callers read nil as readable).
- `Compat:NumPurchasedBankTabs(bankTypeName)`: `C_Bank.FetchNumPurchasedBankTabs`, or nil.
- `Compat:BankerKind(interactionType)` returns `"character"`, `"account"` or nil, from `Enum.PlayerInteractionType`
  read by name (Banker, CharacterBanker, AccountBanker). Consumers then decide what each kind arms.
- A pure helper, `Compat.UnreadyBankContainers(shape, memory, purchased)`: `shape` maps id to slots now, and
  `memory` maps id to slots at the last ready read. It returns the sorted ids that read 0 after reporting slots, or,
  with no memory, a marker when fewer containers answer than `purchased`. The caller keeps the memory and the
  deadline, because BankLedger diffs within one visit while LootHistory diffs against stored history.

Out of scope: socketed bank bags (-2), which stay ignored (R6) until the probes settle them; the guild bank; and any
store or ledger logic.

## Tests to carry over

- BankLedger `tests/test_keyring_client.lua`, `tests/test_bank_readiness.lua`, and the bag-group cases in
  `tests/test_constants.lua`.
- LootHistory's bag-group and Keyring cases in `tests/test_compat.lua`, and the readiness cases in
  `tests/test_reconciler_rows.lua` (visit 2 with a partly loaded bank, the deadline, an unviewable bank, the first
  visit).
- Run each on both kit profiles. The kit's Forever profile would need the 27-member BagIndex (character tabs 6..14,
  account 15..23, `Keyring = -1`) and `C_Bank.CanViewBank`. Both addons currently build these in their own
  `tests/wow_mock.lua`.

## Facts still owed (probes, not blocking the API)

- **P1:** load timings against 5 s / 6 s, and which cue events fire while the bank loads.
- **P2:** whether Forever has `FetchNumPurchasedBankTabs`.
- **P3:** whether a key can go into the bank, and what Retail -1 answers.

The results go in the addons' `docs/forever-probes.md`. Shape the API so a later probe answer changes a table row,
not the signatures.

## Adoption

After a release: BankLedger, LootHistory and OutfitterReborn drop their copies through
`/dev-copilot:wow-revendor-libka0s`, each with a characterization test first. Any other addon that reads bank
containers should use the shared reader from the start.

