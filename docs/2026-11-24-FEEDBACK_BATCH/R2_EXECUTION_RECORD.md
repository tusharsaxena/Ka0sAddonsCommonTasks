# Round 2: execution record (2026-11-24)

This record covers what `R2_SMOKE_FEEDBACK.md` planned. Round 2 ran as workflow `wf_0f1c645f-6fa`: 41 agents, none
failed. The builders and reviewers worked in clones under `~/ka0s-scratch/fb2/`. The lead then fast-forwarded each live
`feat/2026-11-24-feedback-batch` from its clone and fetched the local tag `v1.113.0`. Every addon's `libs/LibKa0s`
(apart from its pruned `media/`) and `tests/_kit` matches `git archive v1.113.0` byte for byte, line endings aside.

## Upstream

- **LibKa0s v1.113.0** (local tag on `cded10bb`; v1.112.0 stays on `1f1904ee`; neither pushed):
  - Sim minor 5: `sim:Start`'s success path shows the step panel, so every start does (D2).
  - WidgetsDropdown minor 4: a selected row, a preset (`isActive`) row and a ticked `W.ContextMenu` row paint
    `menu.textSel`. A skin whose `menu.textSel` sits under 20 CIEDE2000 from its `menu.text` gets Ka0s Default's gold
    instead; of the shipped skins, only Azeroth (16.3) falls back.
  - The review added the public `W.SelectedColor(owner)` so a host's own menu follows the same rule (D3).
  - `Sim.SampleCrowd(client, n, seed)` and `Sim.CROWD_MAX = 64`; the convention's rule 6 is retired (D1, #104).
  - Gate at `cded10bb`: Retail and Forever each 5184 passed, 0 failed, 3 skipped. luacheck 0/0 in 388 files.
  - Release run `docs/automated-tests/20261124-110824/`: green, max CCN 15.
- **WowAddonStandards v2.120.0** (`62f7214` and `12769e2`): every sim start shows the panel (anti-pattern #126),
  a selected entry reads apart through `W.SelectedColor` (#127), and one name source (#128).
  `scripts/check-standard.sh` passes all checks.

## Addons

Every addon got its FB2-`<AB>`-01 items:
- the re-vendor
- the sim-start audit
- the dropdown audit
- sample names taken from the library
- the smoke checks
- the doc sync

Each then had an independent FB2-`<AB>`-REV review, which re-ran the gate on both clients for a ported addon.
Every review returned ok. The review notes are on each live head under `refs/notes/ka0s-review`.

| Repo | Head | FB2 commits |
|---|---|---|
| AbsorbTracker | `2cdc90c` | 6 |
| AuraMaster | `ef7db7f` | 6 |
| BankLedger | `27a7426` | 6 |
| CombatTrail | `1e015e4` | 6 |
| ConsumableMaster | `2b1de05` | 4 |
| DropWatcher | `d98dfed` | 6 |
| KickCD | `3a69a74` | 5 |
| LibKa0sSkinTester | `a98d2c5` | 4 |
| LootHistory | `c358b4c` | 7 |
| MultiMeters | `21aca3d` | 7 |
| OutfitterReborn | `0d9e7d9` | 6 |
| PanelMaster | `a98da3c` | 4 |
| PartyFrameEnhanced | `5245cbc` | 5 |
| PremadeGroupsFilterExtension | `4d61a59` | 5 |
| PrettyChat | `7eee199` | 4 |
| QuickComms | `454cc17` | 6 |
| RangeMaster | `f8c2516` | 7 |
| SkillMaster | `509c52f` | 7 |
| WhatGroup | `41eed47` | 3 |

The reviews found and fixed one real defect: Outfitter Reborn's broker kept a worn outfit's status color over the
selected color (`0d9e7d9`). They also tightened Panel Master's names gate (`a98da3c`) and made a few doc fixes.

## Open for the owner

1. **AceGUI settings dropdowns.** These are the settings-page dropdowns in every addon. `SkinAce`'s `paintPullout`
   marks the picked item with AceGUI's check alone, and its text stays in `menu.text`. The standard scopes these
   pullouts out of rule #127. Six reviewers (AT, CM, KC, MM, QC, RM) raised it. Covering them is a library change in
   `SkinAce` plus one more re-vendor.
2. **Gold against class colors.** Under Ka0s Default, the selected gold is 11.5 CIEDE2000 from the Rogue class color
   and 11.8 from Artifact quality. In a class-colored character list, a selected Rogue reads close to plain rows.
3. Nits are left as they were. `SampleCrowd` accepts a NaN seed. The names gates (`test_sample_names.lua`) list files
   through `git ls-files`.

## Smoke

The owner's sheet is `Documents/Ka0sPendingSmoke-2026-11-24-ADDED-FB2.csv`, with 45 checks. It covers:
- every addon's new checks
- THANK-14's re-check
- Drop Watcher's FEED-114 and the reworded ROLLS-22, which also covers the test-mode bar
- a clean-load check for the three addons that owe no new check: Consumable Master, Panel Master and WhatGroup

Results: owed.
