# Execution record

The run was built on 2026-11-25 in scratch clones under `~/ka0s-scratch/seeds/`.

- **Workflows:** `wf_df07c1ab-8d1` (41 agents, 0 errors) and the follow-up `wf_219c4c4a-92a` (6 agents, 0 errors).
- **Branches:** `feat/2026-11-25-seeds-foreverdb` was fetched into all 16 live repos without a checkout, so every
  live repo is still on `master` with a clean tree.
- **Pushed:** all 16 feature branches, with `refs/notes/ka0s-review`.
- **Not pushed:** the LibKa0s `v1.114.0` tag (local only, at 2eaa8fc, in both the live repo and the scratch clone)
  and the standard's v2.121.0 tag, which is not created yet.
- **Not done:** no merge and no version bump. #93, #102, #105 and RangeMaster#20 are still open.

## Outcome per issue

- **LibKa0s#105.**
  - `LibKa0s-ForeverDB-1.0` (minor 1) ships in v1.114.0, with the kit fake `mock_foreverdb` (kit revision 62) and
    the diagnostics line.
  - Five addons adopted it this run (owner answer 1): Drop Watcher, Loot History, Bank Ledger, Skill Master and
    Outfitter Reborn.
  - Each lists ForeverDB under `## OptionalDeps` and `.pkgmeta` `optional-dependencies`, and none requires it.
    Each declares its setting through `clients = { "forever" }`, so the setting is absent on Retail.
  - Each loads ForeverDB on first use, never at login; Bank Ledger never loads it during combat.
  - On the seed-validation side, standard v2.121.0 adds clients-§10's ForeverDB evidence and clients-§11, and
    dev-copilot 2.12.0 adds `scripts/foreverdb.py` and `--foreverdb`.
- **LibKa0s#93.**
  - LibKa0s now has a seed contract and `tools/seeds/libseeds.py`, which check the payload's Enum and API
    assumptions against Ketho/BlizzardInterfaceResources `live` and `forever`.
  - First-run bundles: `docs/seed-research/2026-11-25-{retail,forever}`.
  - The kit's Forever globals were regenerated at Ketho `e230342` (10545 → 10559 names).
- **LibKa0s#102.**
  - New contracts in CombatTrail (ported from DPS Race), RangeMaster and LootHistory.
  - Skill Master gains ForeverDB evidence for its trainers and gathering nodes.
  - The follow-ups are closed out:
    - QuickComms `CLASSES` is per client;
    - QuickComms and OutfitterReborn pin their wago builds;
    - every adopter's CLAUDE.md gate runs its seed tests.
- **RangeMaster#20.** Every class has a band set preset on each client (13 on Retail, 9 on Forever), with tier
  anchors from tier10 to tier30. The Forever Paladin's set is MELEE / JUDGE 5-10 / RANGE 10-30 / OOR.

## Shipped data changed (fix policy: "fix everything flagged")

| Repo | Change | Evidence | Smoke |
|---|---|---|---|
| RangeMaster | Throw 2764 removed from the Forever Warrior and Rogue ladders; Heroic Throw 57755 removed from the Retail Warrior ladder | DB2 SpellRange 8-30, which is never a rung | RANGE-19..21 |
| RangeMaster | tier anchors and per-class presets (SF-RM-02) | DB2 ranges from SF-RM-01's bundles | BANDS-12..17 |
| LootHistory | Retail DECONSTRUCT_IDS goes from 20 to 30; the mass-mill name seed moves from 434926 to 311413 | DB2 SpellName and SkillLineAbility, wow 12.1.5.70961 | CAP-35..38, LOC-4 cleared to pending |
| SkillMaster | Angelique Butler moves from Neutral to Alliance | ForeverDB nfac `A`, and the other Alterac trainers | SM-SEEDFDB-1 |
| QuickComms | Forever CLASSES now holds nine tokens | clients-§5 and Forever ChrClasses | FOREVER-27 |
| LibKa0s | kit Forever globals regenerated | Ketho `forever` e230342 | none (headless only) |

## Needs the owner's decision

- **SkillMaster SM-SEEDFDB-2.** ForeverDB disagrees about four Zephras Isle trainers (Aedi Thriceforged, Eaysaa
  Brightgust, Nasalanna Windsinger, Messana Crestwind) and Norzsh in Durotar, but the data cannot decide. No data
  was changed.
- **RangeMaster judgment calls (SF-RM-02):**
  - tier roles are named by yards, not per class;
  - Warrior and Forever Rogue get a 5-8 yd CLOSE band, not a dead-zone gap;
  - abilities that are only crowd control get no tier;
  - Retail talent tiers are included (Shadowstep, Felblade, Skull Bash);
  - the labels are JUDGE, HAMMER, CHARGE, STEP and so on.

  BANDS-12..17 cover all of these.
- **Bank Ledger.** There is no "value basis" to add the price to, because the 2026-07-27 Insights overhaul removed
  vendor value. The buy price is therefore shown in the tooltip only.
- **The CurseForge slug `forever-db`** in five `.pkgmeta` files comes from the spec. Nobody checked it against the
  live project page (CurseForge project 1807282).

## Deviations worth knowing

- **Bundle cache.** ForeverDB bundles keep only verdicts and sha256 values. The install is CRLF while the tag is
  LF, so the cache compares a line-ending-insensitive sha256.
- **Loot History's leak budget** was raised to 288 MB, and the change is recorded as a documented-deviations row
  (testing-§15).
- **The standard's recount** also corrected drift since v1.109.0: per-major file lists, and the Core-floor census
  (12, not 14).
- **WhatGroup** is Retail-only: its 21 failures under the Forever kit profile are outside its gate, and its
  diff is CLAUDE.md only.

## Lead gate re-run (2026-11-25, at the pushed heads)

| Repo | Head | Retail | Forever | luacheck | Seed tests |
|---|---|---|---|---|---|
| WowAddonStandards | ef4ca98 | check-standard: all 8 checks | | | |
| dev-copilot | ab560b3 | pytest scripts: 205 passed | | | |
| LibKa0s | 58b26061 | 5220/0 | 5220/0 | 0/0 (392 files) | 18 |
| CombatTrail | 2abdc14 | 1638/0 | 1628/0 | 0/0 | 25 |
| RangeMaster | 47aa64d | 814/0 | 814/0 | 0/0 | 23 |
| LootHistory | f54e32b | 2185/0 | 2170/0 | 0/0 | 17 |
| SkillMaster | 5e74782 | n/a (Forever-only) | 906/0 | 0/0 | 24 |
| QuickComms | 97aabe7 | 2125/0 | 2125/0 | 0/0 | 17 |
| OutfitterReborn | 1bae3ee | 1630/0 | 1614/0 | 0/0 | 17 |
| DropWatcher | 3598144 | 2748/0 | 2642/0 | 0/0 | 21 |
| BankLedger | 747270b | 1883/0 | 1862/0 | 0/0 | n/a |
| AuraMaster | 931efc2 | 2598/0 | 2597/0 | 0/0 | 458 |
| ConsumableMaster | fa4ed24 | 1527/0 | 1527/0 | 0/0 | 20 |
| KickCD | 8b9a8de | 1929/0 | 1919/0 | 0/0 | 56 |
| PrettyChat | bee6f2b | 710/0 | 710/0 | 0/0 | 21 |
| WhatGroup | 4fbf4c8 | 1141/0 | (not its gate) | 0/0 | 26 |

## What finalize must do (after the owner's smoke and go-ahead)

1. **Merge in dependency order:** standard, dev-copilot, LibKa0s, then the addons and CommonTasks.
2. **Before merging the standard**, re-check `origin/master`'s version and renumber v2.121.0 if another session
   moved it.
3. **Push** the `v1.114.0` tag and tag the standard `v2.121.0`.
4. **After dev-copilot merges**, the owner updates the plugin (`/plugin marketplace update`, then
   `/reload-plugins`), so that `/dev-copilot:validate-seeds` runs the installed `foreverdb.py`.
5. **Close** LibKa0s#93, #102 and #105, and RangeMaster#20.
6. **Clean up:** delete the branches (local and origin), `~/ka0s-scratch/seeds/` and any stashes.

## Commits per repo

### WowAddonStandards ef4ca98
- ef4ca98 SF-STD-01: review fixes (Core-floor census recounted at LibKa0s v1.114.0: twelve, not fourteen; Skin's eleven secondary files)
- b1b7347 SF-STD-01: library-stack-§7 recounted at LibKa0s v1.114.0 (26 majors, 87 files, ForeverDB row)
- b303a04 SF-STD-01: review fixes (audit grep, replay keyword, perf-page wording, suite pointer)
- 7a009bc SF-STD-01: v2.121.0, ForeverDB as Forever seed evidence (clients-§10) and optional runtime data addons (clients-§11)
### dev-copilot ab560b3
- ab560b3 SF-DC-01: review fixes: byte escapes as UTF-8, raw URLs at the commit, install/tag confirmation both ways
- 140d30b SF-DC-01: dev-copilot 2.12.0: validate-seeds Evidence: ForeverDB, --foreverdb pin, doc parity
- d22df23 SF-DC-01: scripts/foreverdb.py: ForeverDB tag status, fetch, Lua reader and cache
### LibKa0s 58b26061
- 58b26061 SF-LK-02: review fixes (README layout names the seed tool, the scan checks cached globals)
- 2eaa8fc9 SF-LK-REL: v1.114.0's release record (bundle 20261125-021723, ANALYSIS, RESULTS row, release-notes lines)
- 6e8d2484 SF-LK-REL: ForeverDB's Spots under CCN 15 for the release gate (no behavior change)
- 4296bd05 SF-LK-REL: v1.114.0 (2026-11-25): ForeverDB major, the seed contract, kit revision 62
- 2fdaf867 SF-LK-02: the contract's note on a shared helper no longer defers to LibKa0s#91
- 3672dd69 SF-LK-02: LibKa0s seed contract (LibKa0s#93), first runs, forever name set regenerated (kit revision 62)
- 05b56d10 SF-LK-01: review fixes (named shapes in the doc, guarded diagnostics read, range-checked scales)
- 70ee8ef6 SF-LK-01: New major LibKa0s-ForeverDB-1.0, the ForeverDB reader, and the kit's fake (LibKa0s#105)
### CombatTrail 2abdc14
- 2abdc14 SF-CT-01: review fixes, drop the executable bit from the seed fixture CSVs
- c61110f SF-CT-01: first seed runs, retail 12.1.5.70961 and forever 1.60.1.71091 + ForeverDB v2026.11.24.46
- bc3e6be SF-CT-01: seed contract and tool, ported from DPS Race, with a forever flavor
### RangeMaster 47aa64d
- 47aa64d SF-RM-02: review fixes (a Devourer's seed keeps the Demon Hunter set, schema's four-set cases)
- 2b2562d SF-RM-02: A band set preset for every class, per client, with bands at each class's own range tiers (RangeMaster#20)
- 106479d SF-RM-01: review fixes (true evidence in two rulings, DifficultyID test, Distract owner review, emptied-ladder comments, gate comma)
- 29bbbae SF-RM-01: Seeds (retail, forever): first validation against wow 12.1.5.70961 and wowf 1.60.1.71091 (2026-11-25)
- caee4bd SF-RM-01: The seed-validation contract and tool for defaults/SpellSeeds.lua, both flavors
### LootHistory f54e32b
- f54e32b SF-LH-01: review fixes (Item sources absent on Retail, leak-budget deviation row, boot test, LOC-4 pending)
- bffdd0c SF-LH-02: The History item tooltip shows Drops from and Sold by from ForeverDB (LibKa0s#105)
- 153abc6 SF-LH-02: Characterization case for the History row's item tooltip
- 86b63d2 SF-LH-02: Re-vendor LibKa0s v1.114.0 (kit revision 62)
- 1c15fd7 SF-LH-01: Seed contract and tool for the deconstruct seeds, both flavors (LibKa0s#102)
### SkillMaster 5e74782
- 5e74782 SF-SM-01: review fixes (Angelique Butler's reasoning, the probe's side check, invented fixture names, a sellers comment)
- d6d8127 SF-SM-02: ForeverDB, optional: a book rank's sources and a missing trainer spot
- 325d62f SF-SM-02: Characterization tests for the book-rank tooltip and a trainer without a position
- 478c98a SF-SM-02: Re-vendor LibKa0s v1.114.0 (ForeverDB major, kit revision 62)
- d39b052 SF-SM-01: Seeds (forever): re-validated against 1.60.1.71091 + ForeverDB v2026.11.24.46 (2026-11-25); Angelique Butler is Alliance
- b9c3bbd SF-SM-01: seeds.py gains ForeverDB evidence (trainers, gathering nodes); the trainer reader is fixed; the seed tests join the commit gate
### QuickComms 97aabe7
- 97aabe7 SF-QC-01: review fixes: label the two class lists apart; reword the four class rulings
- 6aad210 SF-QC-01: the seed tool's tests join the commit gate
- 390eb1c SF-QC-01: pin tools/derive-gameids.py's Retail fetch to ?build=
- 0f8ebd5 SF-QC-01: CLASSES per client: Forever's class picker offers its own nine
### OutfitterReborn 1bae3ee
- 1bae3ee SF-OR-01: review fixes (testing.md no longer counts the leased majors)
- 6dc7387 SF-OR-02: On WoW Forever, describe an outfit's missing items from ForeverDB
- 142e9fd SF-OR-02: Pin the outfit tooltip's missing list as it draws today (characterization)
- d66d144 SF-OR-02: Re-vendor LibKa0s v1.114.0 (ForeverDB major, diagnostics minor 12, kit revision 62)
- b0653ef SF-OR-01: Pin tools/gen-zones.lua's wago fetch to a build; seed tests join the commit gate
### AuraMaster 931efc2
- 931efc2 SF-GATE-01: seed tests join the commit gate
### ConsumableMaster fa4ed24
- fa4ed24 SF-GATE-01: seed tests join the commit gate
### DropWatcher 3598144
- 3598144 SF-DW-01: review fixes (named headline source, compact-card chip note, setting name)
- 715ea79 SF-DW-01: The detail card says where a drop comes from, from the optional ForeverDB addon (WoW Forever)
- 11d1a6c SF-DW-01: Characterize the detail card's header chips before the ForeverDB adoption
- da0d4a8 SF-DW-01: Re-vendor LibKa0s v1.114.0 (kit revision 62): the ForeverDB major arrives
- 21e661d SF-GATE-01: seed tests join the commit gate
### KickCD 8b9a8de
- 8b9a8de SF-GATE-01: seed tests join the commit gate
### PrettyChat bee6f2b
- bee6f2b SF-GATE-01: seed tests join the commit gate
### WhatGroup 4fbf4c8
- 4fbf4c8 SF-GATE-01: seed tests join the commit gate
### BankLedger 747270b
- 747270b SF-BL-01: review fixes (the load-count pin sees file load; the addon's own Forever gate is pinned)
- c5ee8dc SF-BL-01: The vendor buy price from ForeverDB on WoW Forever's row tooltips (LibKa0s#105)
- 5b81c56 SF-BL-01: Characterize the ledger rows' item tooltips before the vendor buy price
- 1604084 SF-BL-01: Re-vendor LibKa0s v1.114.0 (the ForeverDB reader, kit revision 62)

## Merged (2026-11-25, owner: "merge all branches to master so i can test it in game")

Merged `--no-ff` into `master` ahead of smoke so the owner can test in game, in dependency order (standard →
dev-copilot → LibKa0s → addons → CommonTasks), and pushed. `origin/master` had not moved in any repo, so every
merge tree is identical to the gated branch head (checked per repo), and the lead gate re-run above stands for it.

| Repo | Merge |
|---|---|
| WowAddonStandards | e23dcd5 |
| dev-copilot | f475b87 |
| LibKa0s | cb825436 |
| CombatTrail | e6cf949 |
| RangeMaster | cf7f35e |
| LootHistory | 516c6ba |
| SkillMaster | 6860e9f |
| QuickComms | 32f0aa6 |
| OutfitterReborn | ab08d5f |
| AuraMaster | 74b75a8 |
| ConsumableMaster | 31264c5 |
| DropWatcher | 172ec17 |
| KickCD | d8df588 |
| PrettyChat | 3d67f68 |
| WhatGroup | b250866 |
| BankLedger | cf3b96f |

Still owed after smoke: push the LibKa0s `v1.114.0` tag and tag the standard `v2.121.0`; close LibKa0s#93, #102,
#105 and RangeMaster#20; record the smoke results in `06_SMOKE_TESTS.md`. No `/dev-copilot:sync-docs` pass was run at
merge (each item updated its own docs). The eight addons outside the adapter work still vendor LibKa0s v1.113.0.
