# LibKa0s#101: the shared container-group and bank-readiness reader

Created 2026-11-22, on the owner's call "Build LibKa0s#101 now". The issue text is in `inputs/LIBKA0S_101.md`, and it
is the spec. The context is the Forever port bundle `../2026-11-22-LOOTHISTORY_BANKLEDGER_FOREVER_PORT/`: its rulings
R1, R5, R6 and R8 hold here.

Branch `feat/2026-11-22-libka0s-101` in LibKa0s, LootHistory, BankLedger, OutfitterReborn and
Ka0sAddonsCommonTasks, plus WowAddonStandards only if a standard fact moves.

## Lead's calls (the issue left these open)

1. **The members join the existing `LibKa0s-Compat-1.0`** as minor 5 → 6. There is no new file and no new major, so the
   standard's library-stack counts do not move.
2. **One documented fallback for an absent `Enum.BagIndex`:** `bags = {0, 1, 2, 3, 4, 5}` (BankLedger's guarantee),
   with `bank` and `accountBank` empty.
3. **`CanViewCharacterBank` is three-valued** and answers nil when the build cannot tell. LootHistory today answers
   true when it cannot tell, so its adoption maps nil to readable at the call site, and its behavior is unchanged.
4. **The deadlines and the readiness memory stay in the consumers**, as the issue says. LootHistory keeps 5 s and
   BankLedger keeps 6 s. Unifying them waits for probe P1.
5. **The account bank is declared per client** through the library's own `ForClient`-style declaration (Retail only),
   matching R1. Forever's `accountBank` is empty.
6. **Kit fidelity:** the kit's Forever profile gains the 27-member `Enum.BagIndex` and `C_Bank.CanViewBank`. The kit
   revision bumps. The consumers keep their own `tests/wow_mock.lua` builds until they choose otherwise, and their
   adoption must stay green on the new kit.
7. **Release:** LibKa0s v1.110.0 is tagged **locally**, so the consumers can re-vendor from a tag. Pushing the tag and
   merging wait for the owner's go-ahead. No addon version bumps.
8. **Adoption scope:** only the three consumers the issue names. The other addons stay on v1.109.0 until the next
   sweep, which is allowed because each addon vendors its own pinned copy.

## Items

`plan-data/items.tsv`. Done = a commit whose subject starts `<ID>: ` on the branch. `plan-data/resume-state.sh`
computes progress. Gates per repo: both kit profiles where the repo ships Forever, `ka0s-bounded luacheck .` 0/0,
the 1500-line cap and the repo's own gates (LibKa0s: its versioning, manifest and prose suites).
