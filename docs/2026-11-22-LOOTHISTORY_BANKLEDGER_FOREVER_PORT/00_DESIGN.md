# LootHistory + BankLedger: the WoW Forever port, design

Created 2026-11-22. Classification groups 5 (high) in `../2026-11-07-WOW_FOREVER_PORT_STEP5/00_CLASSIFICATION.md`.
Research: `inputs/research/SYNTHESIS.md` (synthesis + critic, read it first) and the six reports beside it. The Forever UI
source used was Gethe/wow-ui-source `forever` 734f065 (1.60.1 71037); Retail `live` ab5cb85 (12.1.5 70961).

Branch `feat/2026-11-22-forever-port-lh-bl` in LootHistory, BankLedger, WowAddonStandards and Ka0sAddonsCommonTasks.

## Owner rulings (2026-11-21/22)

| # | Question | Ruling |
|---|---|---|
| R1 | Warband bank on Forever | **Retail-only by declaration** (`ForClient({"retail"})`). On Forever: no Warband store, settings row, Holdings tabs column, WARBAND reasons, warband-money part, events or sim scenario. |
| R2 | LH vanilla-less sources | **Drop on Forever:** MPLUS (+ keystone context, Insights keystone breakdown, sim `key` scenario), BONUS_ROLL, MILLING, PROSPECTING, DECONSTRUCT, WARBAND_DEPOSIT/WITHDRAW. **Keep and relabel "Account" on Forever:** the account holder (stored key stays `§warband`) and the WARBAND / WARBAND_UE bound states (Forever ships "Binds to Account"). |
| R3 | Merge gate | **Build, push and merge** once the gates are green, without waiting for probes. Probe results that contradict a default become follow-up items. No version bump, no tag, no release. |
| R4 | Probes | **Ship permanent probe verbs** under each addon's debug/diagnostics family (`/lh debug probe …`, `/bl debug probe …`) that record the facts below to SavedVariables; a `/run` sheet stays in each addon's `docs/forever-probes.md` as a fallback. |
| R5 | Keyring (-1) | **In the bags group, Forever only**, through a per-client container table picked once by `ClientKey()`. Retail untouched. |
| R6 | Socketed bank bags (-2) | **Ignored for now.** A bag socketed into the bank reads as a bag OUT (LH) / nothing (BL). The probe verb records what -2 reads, for a later decision. |
| R7 | Wowhead links | **Forever uses `https://www.wowhead.com/forever/item=<id>`**; Retail unchanged. A per-client constant. |
| R8 | Retail-affecting fixes | **Both clients, one commit each with its own test**, so each can be bisected: LH `CharacterBanker` arming; the per-container bank-readiness guard + `C_Bank.CanViewBank(Enum.BankType.Character)`; money text through `C_CurrencyInfo.GetCoinTextureString` → `GetMoneyString` → text. |

Lead's calls (recommendations accepted by default, not asked): D3 currency transfer kept on both clients; D6 the Forever
character key is `"First Last"` (`Compat:CharacterKey()`), Retail keeps `Name-Realm` so no stored Retail row moves; D7
guild bank kept on both clients; D11 container groups stay addon-local and a LibKa0s issue proposes a shared reader;
D12 two-word names: widen BL's character dropdown, truncate narrow bar labels with the full name in a tooltip; D15
LH's Forever seed list = Disenchant 13262 only, deconstruct ids empty by decision (R2 drops the source).

## Design

### Client routing
Each addon gets `core/CompatClient.lua` (DropWatcher precedent `DropWatcher/core/CompatClient.lua`) exposing
`IsForever / IsRetail / ClientKey / ForClient / RegionalNames / UnitCharacterName / CharacterKey / RealmKey` from the
vendored `LibKa0s-Compat-1.0` (v1.109.0, no re-vendor). No `WOW_PROJECT_*` read anywhere else (clients-§3). Feature
presence is a declaration (clients-§4), never feature detection.

### Identity
- `PlayerRecordKey()`: under `RegionalNames()` → `CharacterKey()` (`"Traxex Silentshot"`); else today's `Name-Realm`.
- LH `Compat.TradeTargetKey` through `UnitCharacterName("NPC")`; `Util.QualifyName` keeps a typed two-word name whole and
  adds no realm on regional names; `LatestCurrencyTransfer` adds no realm on regional names.
- BL `Compat.PlayerName` / `Util.PlayerKey` / SimWorld `buildChars` all route through the one builder.
- No SavedVariables migration: WTF is per client install, Retail keys are unchanged and a Forever DB is born fresh.

### Per-client tables (seeded once by `ClientKey()`, clients-§5)
Containers (keyring on Forever, R5), stores/parts/reasons/sources (R1, R2), labels ("Account" vs "Warband"), seed
lists (D15), Wowhead base (R7), sample identity / test-mode / sim seeds (`Sim.Sample(ClientKey())`, Forever classes,
no Evoker, bag-sized tabs), default skin (`NS.DEFAULT_SKIN = Skin:DefaultSkin()`).

### Bank model (both addons)
- Character bank = `CharacterBankTab_*` by member name (6..14 on Forever, 6..11 on Retail).
- **Readiness guard (R8):** a bank container that reported slots on the last ready read and now reports 0 is not ready;
  if `C_Bank.CanViewBank(Enum.BankType.Character)` is false (warband-only banker) the character bank is not readable.
  Not-ready → no baseline (BL) / part stays dirty (LH); re-read on `BAG_UPDATE_DELAYED`, `BAG_CONTAINER_UPDATE`,
  `BANK_TABS_CHANGED`, `PLAYERBANKSLOTS_CHANGED`. Covered by a "visit 2, partly loaded bank" test.
- LH arms the bank part on `Banker`, `CharacterBanker` and (Retail) `AccountBanker` (R8).

### Capture hardening (LH)
Roll-won parsing takes the `%s` link capture (Forever prefixes `|HlootHistory:%d|h[Loot]|h: `). Money text per R8.

### Probe verbs (R4)
Record into the addon's existing SavedVariables (a capped `probe` table under `db.global`, never a new SV global) with a
client stamp and build: banker interaction type; per-container slot counts at open, +1 s and +3 s; `CanViewBank(0/2)`,
`FetchNumPurchasedBankTabs`, `ShouldUsePlayerBagsInBank`, `FetchDepositedMoney(2)`; keyring slots and contents; -2
socket reads (`ItemLocation` and `GetContainerItemInfo`); raw `CHAT_MSG_LOOT` / money / currency lines and
`GetLootSourceInfo` per slot (LH); currency list flags and the last currency-transfer record (LH); trade partner and mail
recipient forms (LH); guild-vault reads (BL); `GetCoinTextureString` / `GetMoneyString` presence; `GetInstanceInfo`.
`/x debug probe start|stop|status|clear`; the lead reads
`_forever_/WTF/Account/<acct>/SavedVariables/<Addon>.lua` after logout.

### Docs and shape (each addon)
TOC `## Interface: 120105, 16001`, no load gating; README badge + "Retail · WoW Forever" sentence; CLAUDE.md gate names
both runs (`lua tests/run.lua` and `KA0S_KIT_CLIENT=forever lua tests/run.lua`); `docs/forever-quirks.md` (bank model,
keyring, sockets, roll prefix, names); `docs/forever-probes.md`; ARCHITECTURE per-client table and doc map; testing.md;
smoke-tests.md WoW Forever section including absence checks (no Warband checkbox, no Mythic+ filter, no keystone
Insights); `docs/test-cases.md` regenerated; present/absent tests per declared feature on each profile (clients-§6).
Roster rows in `WowAddonStandards/standards/ADDONS.md` flip to `Retail · Forever`, no standard version bump.
