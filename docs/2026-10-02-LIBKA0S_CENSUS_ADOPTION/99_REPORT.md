# Execution record: LibKa0s census adoption (2026-10-02)

All nine issues are fixed on `feat/2026-10-02-libka0s-census-adoption` in 13 repos. Every branch is pushed.
Nothing is merged, the LibKa0s tag `v1.67.0` exists only locally, and no addon version moved. 38 of 38
items are committed and independently reviewed (M0 to M3), and the M1 and M2 checkpoints are in
`checkpoints.tsv`.

## Per issue

| Issue | Fixed by | Commits |
|---|---|---|
| LibKa0s#41 | Core minor 10: `MakeResizable` takes `canResize`, `onResizeStop` and `gripParent` | LibKa0s a4f1d17 |
| LibKa0s#42 | OptionsIdList 3 (the help art accepts `addonName` only when that addon is loaded, one `Cfg` line otherwise), Options 28 (docblock); standard v2.75.0 options-ui-§1 row; all 11 addons pass `addonName` | LibKa0s 008a87a; WowAddonStandards 562379a; `CA-<XX>-NM` in every addon |
| AbsorbTracker#33 | `Slash.SplitVerb`, `Slash.ProfileNames`, `Core.SECRET` | 3f6df55, 1120cca |
| BankLedger#21 | Both windows' grips are `Core.MakeResizable` (no lock gate, as today); a working fallback grip when the library is absent | 3005447, a115afa, d825805, cb23423 |
| ConsumableMaster#44 | `SplitVerb`, `FindCommand`, `CommandRows` through the Slash seam; plain rows when the library is absent | 3c932d3, aaabf34 |
| KickCD#36 | The Slash vocabulary (both sub-help lists and `runDebug`'s split, two copies the issue missed); `Core.SECRET`; `PANEL_HEADER_TOP/HEIGHT` deleted | ece3a6e, 2353c1a, 6cd075e, eff6cfc |
| LootHistory#33 | The History grip is `Core.MakeResizable` with `canResize = not locked`; a working fallback grip when the library is absent | cf8238e, 2685aac |
| MultiMeters#58 | `Core.SECRET` (the zero-reader `Diagnostics.SECRET` alias deleted); the grip is `Core.MakeResizable` on the anchor, drawn on the art frame (`gripParent`), saved once per drag (`onResizeStop`), gated on Core ≥ 10; no grip when the library is absent | 7cf1aea, c2a411f |
| PanelMaster#56 | Reads `O.PADDING_X` for the Profiles container; the stub carries `PADDING_X = 0` | 113f6c4, a04e2d4, 9a8eddc |

The census re-run (CA-LK-04, LibKa0s 8f55167 and d178a2b; data in `plan-data/census-v1.67.0/`) confirms
every flip: 244 consumed, 67 thin, 98 zero (was 240 / 63 / 106). No host duplicate and no suspect shape
is left in the zero set.

## Gates (orchestrator re-run at the M2 checkpoint)

| Repo | Tests (pass/fail/skip) | luacheck | Max CCN | Vendor |
|---|---|---|---|---|
| LibKa0s | 2013/0/2 | 0/0 in 144 | 15 | — |
| AbsorbTracker | 867/0/1 | 0/0 | 14 | identical |
| AuraMaster | 1792/0/1 | 0/0 | 15 | identical |
| BankLedger | 1226/0/1 | 0/0 | 15 | identical |
| ConsumableMaster | 1194/0/1 | 0/0 | 15 | identical |
| KickCD | 1294/0/1 | 0/0 | 15 | identical |
| LootHistory | 1049/0/1 | 0/0 | 15 | identical |
| MultiMeters | 2187/0/1 | 0/0 | 15 | identical |
| PanelMaster | 1035/0/1 | 0/0 | 15 | identical |
| PartyFrameEnhanced | 454/0/1 | 0/0 | 14 | identical |
| PrettyChat | 572/0/1 | 0/0 | 15 | identical |
| WhatGroup | 914/0/1 | 0/0 | 15 | identical |

## Decisions taken without asking

All are in `01_DESIGN.md` (D1 to D3.11). The ones the owner may want to revisit:

- **BankLedger's lock frame still does not stop a resize** (D3.1). Parity with today. Smoke BL-4 asks.
- **MultiMeters' grip grows from 12 to 16 px**, and it has no grip at all when the library is absent
  (D3.3). Smoke MM-2 and DG-2.
- **LootHistory**: a mouse-up after a refused (locked) mouse-down no longer saves (D3.4).
- **AbsorbTracker `/at profile list`** is now sorted and always lists the current profile (D3.5).
- **Degraded sub-help** in ConsumableMaster and KickCD prints plain `cmd  desc` rows (D3.6).
- **#42's issue text overstated its reach**: only AuraMaster draws IdList help marks today, so only
  AuraMaster shows a visible change.

## During execution

- BankLedger#21's second review found the suite red in a clean checkout, though green in the working
  tree (a frame survey counted frames rather than comparing identities). Fixed in cb23423; the
  checkpoint run is green.
- Workflow agents shared one scratchpad. One agent's temporary `tc.md` was overwritten by another's.
  It was caught before commit, and no committed file is affected.
- I force-pushed the `refs/notes/ka0s-review` ref at the M2 checkpoint. The local ref holds every note
  written on this machine, so nothing should be lost, but force was not needed.
- The CA-LK-04 reviewer's one wording finding was fixed by the orchestrator in d178a2b, with no second
  independent review (a one-line doc change).

## Left alone (noticed, outside scope)

- AuraMaster `docs/debug.md` still names older library minors (DebugLog 18, Slash 18), and the FILT-34
  smoke text predates the 2026-09-22 move of "(also in N)" into the help mark.
- BankLedger's smoke-tests index row reads `CAPT-1 – 17` though CAPT-18/19 exist.
- ConsumableMaster `core/SlashDump.lua` keeps a third verb split (D3.10). ConsumableMaster's CLAUDE.md says
  never auto-commit; the commits went ahead under this run's explicit authorization.
- KickCD `settings/Panel.lua:217` comment says KickCD reads `Helpers.PADDING_X`, which no code does.
- The census counts `ResolveId` as thin (1); ConsumableMaster also calls it through its Options instance,
  which the tool counts as name-only. The page already says thin counts are a lower bound.

## What the owner does next

1. Run `03_SMOKE_TESTS.md` (each addon's `docs/smoke-tests.md` carries its rows under its own ids).
2. Give the merge go-ahead. `/wow-addon:finalize` then merges in dependency order (standard → LibKa0s →
   addons → this repo), pushes tag `v1.67.0`, deletes the branches and closes the nine issues.
