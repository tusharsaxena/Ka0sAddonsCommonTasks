# 06 Smoke tests: seeds and ForeverDB

The owner's in-game checks for this run (spec `03_SPEC.md` §7, §9 and §10), every one owed. The sheet the owner works from is
`/mnt/d/Profile/Users/Tushar/Documents/Ka0sPendingSmoke-2026-11-25-ADDED-SEEDS.csv` (66 rows, run label "SEEDS 11-25 (seed validation + ForeverDB, LibKa0s v1.114.0)").

Every check is live on branch `feat/2026-11-25-seeds-foreverdb` only: check the branch out in each addon's folder (it carries the LibKa0s v1.114.0 re-vendor), then restart the client. ForeverDB checks need ForeverDB 2026.11.24.46 in the Forever client. Rows whose title starts "Decide:" are review items that need the owner's ruling rather than a pass; they are marked "Needs your decision" in the sheet. Combat Trail's seed item (SF-CT-01) changed no player-visible behaviour and adds no row.

**Total: 66 checks**, of which 9 need a decision.

## LibKa0s (6)

| Check ID | Client | Title | Result |
|---|---|---|---|
| LK-FDB-1 | Forever | ForeverDB is not loaded at login | owed |
| LK-FDB-2 | Forever | The diagnostics line never loads ForeverDB | owed |
| LK-FDB-3 | Forever | Available() with ForeverDB enabled | owed |
| LK-FDB-4 | Forever | NPC, ItemSources and Meta answer | owed |
| LK-FDB-5 | Forever | Available() with ForeverDB disabled (or removed) | owed |
| LK-FDB-6 | Retail | Retail answers false, "client" | owed |

## Bank Ledger (4)

| Check ID | Client | Title | Result |
|---|---|---|---|
| FOREVER-20 | Forever | With ForeverDB: the vendor buy price beside the game's sell price | owed |
| FOREVER-21 | Forever | Without ForeverDB: inert, and the row says why | owed |
| FOREVER-22 | Forever | The first ForeverDB load never happens in combat | owed |
| FOREVER-23 | Retail | Retail has no vendor buy price | owed |

## Drop Watcher (3)

| Check ID | Client | Title | Result |
|---|---|---|---|
| FOREVER-18 | Forever | Where a drop comes from, with ForeverDB | owed |
| FOREVER-19 | Forever | Without ForeverDB: no Sources chip | owed |
| FOREVER-20 | Retail | No Sources chip on Retail | owed |

## Loot History (9)

| Check ID | Client | Title | Result |
|---|---|---|---|
| CAP-35 | Retail | Mass Mill attributes again (the name seed is 311413) | owed |
| CAP-36 | Retail | The per-expansion Milling ids attribute by id | owed |
| CAP-37 | Retail | The per-expansion Prospecting ids attribute by id | owed |
| CAP-38 | Retail | Nothing that worked before stopped (the four removed ids) | owed |
| LOC-4 | Retail | The deconstruct name family on a non-English client (amended, cleared to pending) | owed |
| SEEDS-LH-1 | Forever | Item sources with ForeverDB | owed |
| SEEDS-LH-2 | Forever | Item sources without ForeverDB | owed |
| SEEDS-LH-3 | Retail | No item sources on Retail | owed |
| LH-REVIEW-1 | Retail | Decide: the deconstruct name match over-reaches (Disenchanting Rod) | owed |

## Outfitter Reborn (3)

| Check ID | Client | Title | Result |
|---|---|---|---|
| SEEDS-OR-1 | Forever | Missing items described, with ForeverDB | owed |
| SEEDS-OR-2 | Forever | Missing items without ForeverDB | owed |
| SEEDS-OR-3 | Retail | No ForeverDB switch on Retail | owed |

## Quick Comms (1)

| Check ID | Client | Title | Result |
|---|---|---|---|
| FOREVER-27 | Both | The When editor's class picker offers Forever's nine classes | owed |

## Range Master (32)

| Check ID | Client | Title | Result |
|---|---|---|---|
| RANGE-19 | Forever | The Forever warrior's ladder is empty | owed |
| RANGE-20 | Forever | The Forever rogue's ladder is empty | owed |
| RANGE-21 | Retail | The Retail warrior's ladder is Taunt alone | owed |
| BANDS-12 | Forever | The owner's case: the Forever paladin's JUDGE band | owed |
| BANDS-13 | Forever | The Forever hunter keeps its set | owed |
| BANDS-14 (Warrior) | Forever | The Forever warrior's own band set | owed |
| BANDS-14 (Rogue) | Forever | The Forever rogue's own band set | owed |
| BANDS-14 (Priest) | Forever | The Forever priest's own band set | owed |
| BANDS-14 (Shaman) | Forever | The Forever shaman's own band set | owed |
| BANDS-14 (Mage) | Forever | The Forever mage's own band set | owed |
| BANDS-14 (Warlock) | Forever | The Forever warlock's own band set | owed |
| BANDS-14 (Druid) | Forever | The Forever druid's own band set | owed |
| BANDS-15 (Warrior) | Retail | The Retail Warrior's own band set | owed |
| BANDS-15 (Paladin) | Retail | The Retail Paladin's own band set | owed |
| BANDS-15 (Hunter) | Retail | The Retail Hunter's own band set | owed |
| BANDS-15 (Rogue) | Retail | The Retail Rogue's own band set | owed |
| BANDS-15 (Priest, Mage, Warlock) | Retail | The Retail Priest, Mage, Warlock's own band set | owed |
| BANDS-15 (Death Knight) | Retail | The Retail Death Knight's own band set | owed |
| BANDS-15 (Shaman) | Retail | The Retail Shaman's own band set | owed |
| BANDS-15 (Monk) | Retail | The Retail Monk's own band set | owed |
| BANDS-15 (Druid) | Retail | The Retail Druid's own band set | owed |
| BANDS-15 (Demon Hunter) | Retail | The Retail Demon Hunter's own band set | owed |
| BANDS-15 (Evoker) | Retail | The Retail Evoker's own band set | owed |
| BANDS-16 | Both | The tier roles in the band editor | owed |
| BANDS-17 | Both | An existing profile is kept | owed |
| BANDS-JC-1 | Both | Decide: no schema step for the tier roles | owed |
| BANDS-JC-2 | Both | Decide: the warrior's and Forever rogue's 5-8 band is a yard band (CLOSE), not a dead zone | owed |
| BANDS-JC-3 | Both | Decide: no tier band for crowd-control-only abilities | owed |
| BANDS-JC-4 | Both | Decide: the first-run seed still adds the Hunter set to every class | owed |
| BANDS-JC-5 | Both | Decide: the band labels | owed |
| BANDS-JC-6 | Both | Decide: "Judgment" spelled US in authored text | owed |
| RANGE-REVIEW-1 | Forever | Decide: Distract 1725 as the Forever rogue's ranged anchor | owed |

## Skill Master (8)

| Check ID | Client | Title | Result |
|---|---|---|---|
| SM-SEEDFDB-1 | Forever | Angelique Butler is now Alliance (the one data change) | owed |
| SM-SEEDFDB-2 | Forever | Decide: five Forever-only trainers ForeverDB disagrees on | owed |
| SM-FDB-1 | Forever | With ForeverDB: not loaded at login, diagnostics line | owed |
| SM-FDB-2 | Forever | With ForeverDB: a book-taught rank's sources in the skill tooltip | owed |
| SM-FDB-3 | Forever | With ForeverDB: the book seller's card in the trainer popup | owed |
| SM-FDB-4 | Forever | With ForeverDB: the Use ForeverDB switch | owed |
| SM-FDB-5 | Forever | Without ForeverDB: unchanged tooltips | owed |
| SM-FDB-6 | Retail | Skill Master is absent on Retail | owed |

## Recording results

Results are recorded here and in each repo's `docs/smoke-tests.md` (on the check's `Result:` line or Result column) once the owner reports them, with the owner's name and the date. An agent never marks a check passed. A decision row's ruling goes in the owner's findings and, where it changes data, becomes a follow-up item or issue. LibKa0s has no smoke-tests.md: its LK-FDB rows are recorded here and in the run's execution record.
