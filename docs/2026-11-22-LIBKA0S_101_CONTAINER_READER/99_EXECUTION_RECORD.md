# Execution record: LibKa0s#101, the shared container-group and bank-readiness reader (2026-11-22)

Branch `feat/2026-11-22-libka0s-101` in LibKa0s, BankLedger, LootHistory, OutfitterReborn and this repo.
WowAddonStandards was not touched: no standard fact moved (it stays on `master` at v2.117.0). The plan is `00_PLAN.md`
and `plan-data/`, which stay frozen; this file records what happened. Progress comes from git
(`plan-data/resume-state.sh`): 14 of 18 items were done before this record, and K101-CT-REC is this record's own
commit. K101-FU-01..03 (M4, the owner's Forever follow-up rulings F1-F3) are still to run.

- **Blocked items:** none. **Exceptions** (`plan-data/exceptions.tsv`): none.
- **Nothing was pushed or merged.** No addon version moved. The tag `v1.110.0` exists in LibKa0s **locally only**
  (annotated, tag object `d4c05e9c`, on commit `e97bf187`).

## What was built

### LibKa0s (M1)

| Id | Commit | What |
|---|---|---|
| K101-LK-01 | `c51dd778` | `LibKa0s-Compat-1.0` minor 5 → 6 (call 1): `ContainerGroups()` → `{bags, bank, accountBank}` from anchored, case-sensitive `Enum.BagIndex` names declared per client (Keyring in bags on Forever only, `AccountBankTab_N` Retail only; calls 2 and 5), `CONTAINER_PATTERNS_BY_CLIENT` (published copy), three-valued `CanViewCharacterBank()` (call 3), `NumPurchasedBankTabs(name)`, `BankerKind(type)` and the pure `UnreadyBankContainers(shape, memory, purchased)` with its first-visit `{short = true}` marker. New suite `tests/test_compat_containers.lua` (29 cases), version-6 API docs, CHANGELOG block, `C_Bank` in `.luacheckrc`. |
| K101-LK-02 | `c2272e3b` | Kit revision 59 → 60 (call 6): both profiles model their client's `Enum.BagIndex` (Retail 20 members, Forever 27), `Enum.BankType` and `C_Bank.CanViewBank` (Account false on Forever, R1). A consumer's own `Enum` / `C_Bank` wins, per global. 9 new `test_mock_client` cases; testkit version-60 docs. |
| K101-LK-REV | `4ca1d12a` | Review fixes, 1 of 3 confirmed (docs only; see Reviews). |
| K101-LK-REL | `8deb4b09`, `e97bf187` | v1.110.0 in releasing.md's two-commit order: version lines, dated CHANGELOG heading, README Compat row (fixed a stale "4" label), release run bundle `docs/automated-tests/20261122-101023/` with ANALYSIS.md and the RESULTS.md row. Local annotated tag `v1.110.0` on `e97bf187` (call 7). |

### Consumers (M2, call 8)

| Id | Commit | What |
|---|---|---|
| K101-BL-01 | `09ffff0` | Re-vendor v1.110.0 (Compat 6, kit 60), provenance rolled, revendor bundle plus the v1.109.0 span back-fill. |
| K101-BL-02 | `cab6d97` | BankLedger reads `ContainerGroups`, `CONTAINER_PATTERNS_BY_CLIENT`, `CanViewCharacterBank` and `UnreadyBankContainers` from the library; `C.BAG_PATTERNS_BY_CLIENT`, `idsMatching`, the numeric fallback and `L.UnreadyContainers` are gone. The 6 s deadline and `L:ShapeMemory` stay (call 4). No `purchased` count is passed, so a first visit behaves as before. Characterization tests first, green on the old code on both profiles. |
| K101-LH-01 | `88403f5` | Re-vendor v1.110.0; `tests/test_libka0s.lua` pins Compat 6 / kit 60 in a v1.110.0 case. |
| K101-LH-02 | `ec4ed15` | LootHistory reads all six new members; `C.CONTAINER_GROUPS_BY_CLIENT`, its own `CanViewCharacterBank` and `NumPurchasedCharacterBankTabs` are gone. `R:BankState` treats only `false` as unviewable (call 3); `purchased` is passed only when `meta.bankSlots` is nil, which keeps today's readiness answers. Bankers arm through a new `R.BANKER_ARMS` table keyed by `BankerKind` (AccountBanker still Retail only). The 5 s deadline stays (call 4). Characterization tests first. |
| K101-OR-01 | `9cdb5b4` | Re-vendor v1.110.0; icon declaration unchanged. |
| K101-OR-02 | `e1a008d` | `Compat.BankBagIDs()` = `ContainerGroups().bank`; `Compat.IsBankerInteraction(k)` = `BankerKind(k) == "character"`. The local series walk is gone; callers unchanged. OutfitterReborn has no bank-readiness logic, so the readiness members were not adopted. |

### Reviews and record (M3)

| Id | Commit | What |
|---|---|---|
| K101-BL-REV | `f1423d7` | Empty commit: the reviewers sent no findings. |
| K101-LH-REV | `589bfad` | Review fixes, 1 of 2 confirmed (see Reviews). |
| K101-OR-REV | `d14fd02` | Empty commit: the reviewers sent no findings. |
| K101-CT-REC | this commit | This record. |

## Gate totals (final tree of each repo, all through `ka0s-bounded`)

| Repo | Retail profile | Forever profile (`KA0S_KIT_CLIENT=forever`) | luacheck | Largest file |
|---|---|---|---|---|
| LibKa0s | 5115 passed / 0 failed / 3 skipped (5118) | 5115 / 0 / 3 | 0 / 0 in 383 files | Compat.lua 683 lines |
| BankLedger | 1856 / 0 / 3 (1859) | 1835 / 0 / 24 (1859) | 0 / 0 in 136 files | modules/Browser.lua 1242 |
| LootHistory | 2154 / 0 / 1 (2155) | 2134 / 0 / 21 (2155) | 0 / 0 in 171 files | tests/test_browsertable.lua 1477 |
| OutfitterReborn | 1616 / 0 / 31 (1647) | 1595 / 0 / 52 (1647) | 0 / 0 in 206 files | tests/test_dock.lua 996 |

LibKa0s's baseline before the run was 5076. Its release run (manifest `20261122-101023`): lint, tests and complexity
pass, max CCN 15, 0 band files over the cap, perf skipped (no `tests/perf.lua`), `git.dirty` false. Its versioning,
manifest, kitsync and prose suites pass.

## Reviews

Each review is recorded as a `refs/notes/ka0s-review` note on the REV commit (LibKa0s `4ca1d12a`, BankLedger
`f1423d7`, LootHistory `589bfad`, OutfitterReborn `d14fd02`).

| Repo | Finding | Verdict | Fix |
|---|---|---|---|
| LibKa0s | F1 `Compat.lua:585`: a present `CanViewBank` answering nil reads false (BankLedger's rule), unlike LootHistory's old `~= false`; the docs claimed LootHistory was unchanged | CONFIRMED (docs) | Doc comment and version-6-docs state the difference. Code unchanged: no client or mock answers nil there. |
| LibKa0s | F2 `Compat.lua:663`: an empty or all-zero memory counts as no memory in `UnreadyBankContainers` | NOT A DEFECT | Deliberate and documented; adoption note added (LootHistory passes `purchased` only when `meta.bankSlots` is nil). |
| LibKa0s | F3 `testkit/mock_client.lua:104`: the kit's `Enum` / `C_Bank` hide a later `_G` assignment | NOT A DEFECT | No suite assigns them after its environment is built; mock-set precedence is the loader's rule. |
| LootHistory | F1: `CanViewCharacterBank` turns an API nil into false | NOT A DEFECT | Library-documented; the safe outcome (bank part unread). |
| LootHistory | F2: the no-library stubs degraded to "no bank, no banker kind", so an install without LibKa0s never armed the bank and every deposit read as an UNTRACKED loss; on Forever the Keyring dropped out of the bags | CONFIRMED | Stubs in `core/CompatClient.lua` are now copies of the library code, with a test that checks each stub against the library on both profiles (failed before the fix). |
| BankLedger | none | — | — |
| OutfitterReborn | none | — | — |

## Deviations

- **LibKa0s:** an undated `## v1.110.0 — unreleased` CHANGELOG block during LK-01/LK-02 (the versioning suite needs
  "Compat minor 6"), dated by LK-REL. The `{0..5}` bags fallback also fires when the enum exists but matches no bag
  (BankLedger's rule). A secret answer from `CanViewBank` or `FetchNumPurchasedBankTabs` gives nil, documented in
  version-6-docs. The new cases sit in their own suite so `test_compat.lua` stays under 1000 lines. The kit decides
  "the consumer's mock wins" per global, not per member (a per-member fill broke a LootHistory case). The kit's
  `CanViewBank` usage-error wording is an approximation, not checked in a client; it does not model
  `FetchNumPurchasedBankTabs`. LK-REL read the manifest with python3 (no jq), did not run releasing.md step 9's
  Consumers-table sweep (consumers had not re-vendored yet), and has two `K101-LK-REL:` commits as step 7 requires;
  the manifest's `addonVersion` reads 1.109.0 (nearest tag), as in v1.109.0.
- **BankLedger:** with the library absent, the stubs give bags 0..5, no bank, nil and nothing unready, so no bank rows
  are written (before, its own copies read the bank). A secret `CanViewBank` answer was true before and is nil now;
  the bank is still read. `BankerKind` and `NumPurchasedBankTabs` were not adopted (no call site; BankLedger opens on
  `BANKFRAME_OPENED`). `docs/forever-probes.md` was also updated.
- **LootHistory:** with no `Enum.BagIndex` the bags are now `{0..5}` (call 2), not empty. A present API's nil reads
  false. The probe's `canViewCharacterBank` stamp records the raw three-valued answer. `R.READABLE_ON` lost its banker
  rows to `R.BANKER_ARMS`. The minor 2 and 4 helpers came off the Compat parity ignore list. After LH-REV the
  no-library stubs are a second copy of the library's container and readiness code, held to it by a parity test.
- **OutfitterReborn:** for an enum carrying both `Bank`/`BankBag_N` and `CharacterBankTab_N` the library returns the
  union, where the old code took only the tabs; no real client has both, and both clients give identical answers
  (6..11 and 6..14). A made-up `test_secrets` case moved from "6,7" to "-1,6,7". With the library absent the members
  answer `{}` and `false`. The compat-layer.md shim count was fixed from a stale 74 to 76.

## Followups

- **Stub inconsistency (decide before merge):** LH-REV confirmed that degrade-to-nothing stubs are a defect and made
  LootHistory's stubs real copies. BankLedger (`core/Compat.lua`) and OutfitterReborn (`core/Compat.lua`) kept
  degrade-to-nothing stubs on purpose, and their reviews sent no findings. The lead should decide whether those two
  get the LootHistory treatment or the LootHistory fix is the exception.
- **Library, optional:** `CanViewCharacterBank` could answer nil (not false) when the API itself answers nil, making it
  fully three-valued. No client does this today.
- **Library, before a later release:** confirm the kit's `CanViewBank` usage-error wording against a live client;
  run releasing.md step 9's Consumers-table sweep now that BankLedger, LootHistory and OutfitterReborn look up Compat.
- **Re-vendoring hosts:** any host whose gate calls `Kit.assertSurfaceParity` on `LibKa0s-Compat-1.0` must wire the six
  new members or list them in `ignore`; hosts re-pin Compat 5 → 6 and `KIT_VERSION` 59 → 60.
- **BankLedger:** passing `purchased = NumPurchasedBankTabs("Character")` from `L:CheckReady` would enable the
  first-visit marker; it changes behavior, so it waits for probes P1 and P2 (as does unifying the 5 s / 6 s deadlines,
  call 4).
- **LootHistory:** `modules/AttributionOut.lua` `SCOPE_OF` and `modules/Probe.lua` still match bankers by name through
  `Compat.InteractionType`; they could move to `BankerKind`.
- **OutfitterReborn:** its bag range is still `0..NUM_TOTAL_EQUIPPED_BAG_SLOTS`, so Forever's Keyring is not scanned
  for gear; adopting `ContainerGroups().bags` (R5) is the owner's call. Retail's warband bank stays unscanned (O19).
- **M4:** K101-FU-01..03 are still to run.

## What the lead still owes

1. Push `feat/2026-11-22-libka0s-101` in LibKa0s, BankLedger, LootHistory, OutfitterReborn and this repo, with the
   `refs/notes/ka0s-review` notes (subagents cannot push).
2. The owner's go-ahead to merge (`/dev-copilot:finalize`, order LibKa0s, then the three consumers, then this repo)
   and to push the tag `v1.110.0`.
3. Close LibKa0s#101 after the merge.
4. The rest of the collection stays on LibKa0s v1.109.0 until the next re-vendor sweep (call 8); each addon vendors its
   own pinned copy, so this is allowed.

## Smoke checklist (owner, in game, both clients)

Smoke checks are the owner's to run; none is marked passed here. Record each result in this section's table when run.

| Id | Client | Check | Result |
|---|---|---|---|
| K101-S1 | Retail | With LootHistory and BankLedger loaded, open the bank at a banker, wait for it to fill, close it. LootHistory books no bogus deposit, withdrawal or UNTRACKED loss; BankLedger records the character bank tabs correctly and no empty or partial tab snapshot. | owed |
| K101-S2 | Retail | Visit a Warband (account) banker. BankLedger records the warband tabs; LootHistory arms the account part; nothing bogus is booked. | owed |
| K101-S3 | Forever | Same as K101-S1 at a Forever banker: tabs 6..14 read, the Keyring counted with the bags (R5), no warband rows (R1), nothing bogus booked by either addon. | owed |
| K101-S4 | Both | Second visit after moving items between bags and bank: only the real moves are recorded (the readiness memory waits for partly loaded tabs, R8). | owed |
| K101-S5 | Retail | OutfitterReborn: with an outfit item stored in the bank, open the bank and equip that outfit; it finds the item in the bank bags and equips it. | owed |
| K101-S6 | Forever | Same as K101-S5 on Forever. | owed |
