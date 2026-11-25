# 06 Smoke tests: seeds and ForeverDB

The owner's in-game checks for this run (spec `03_SPEC.md` §7, §9 and §10), every one owed. The sheet the owner works from is
`/mnt/d/Profile/Users/Tushar/Documents/Ka0sPendingSmoke-2026-11-25-ADDED-SEEDS.csv` (66 rows, run label "SEEDS 11-25 (seed validation + ForeverDB, LibKa0s v1.114.0)").

Every check is live on branch `feat/2026-11-25-seeds-foreverdb` only: check the branch out in each addon's folder (it carries the LibKa0s v1.114.0 re-vendor), then restart the client. ForeverDB checks need ForeverDB 2026.11.24.46 in the Forever client. Rows whose title starts "Decide:" are review items that need the owner's ruling rather than a pass; they are marked "Needs your decision" in the sheet. Combat Trail's seed item (SF-CT-01) changed no player-visible behaviour and adds no row.

**Total: 66 checks**, of which 9 need a decision.

## LibKa0s (6)

| Check ID | Client | Title | Result |
|---|---|---|---|
| LK-FDB-1 | Forever | ForeverDB is not loaded at login | passed (2026-11-25) |
| LK-FDB-2 | Forever | The diagnostics line never loads ForeverDB | passed (2026-11-25) |
| LK-FDB-3 | Forever | Available() with ForeverDB enabled | passed (2026-11-25) |
| LK-FDB-4 | Forever | NPC, ItemSources and Meta answer | passed (2026-11-25) |
| LK-FDB-5 | Forever | Available() with ForeverDB disabled (or removed) | passed (2026-11-25) |
| LK-FDB-6 | Retail | Retail answers false, "client" | passed (2026-11-25) |

## Bank Ledger (4)

| Check ID | Client | Title | Result |
|---|---|---|---|
| FOREVER-20 | Forever | With ForeverDB: the vendor buy price beside the game's sell price | passed (2026-11-25) |
| FOREVER-21 | Forever | Without ForeverDB: inert, and the row says why | passed (2026-11-25) |
| FOREVER-22 | Forever | The first ForeverDB load never happens in combat | passed (2026-11-25) |
| FOREVER-23 | Retail | Retail has no vendor buy price | passed (2026-11-25) |

## Drop Watcher (3)

| Check ID | Client | Title | Result |
|---|---|---|---|
| FOREVER-18 | Forever | Where a drop comes from, with ForeverDB | passed (2026-11-25) |
| FOREVER-19 | Forever | Without ForeverDB: no Sources chip | passed (2026-11-25) |
| FOREVER-20 | Retail | No Sources chip on Retail | passed (2026-11-25) |

## Loot History (9)

| Check ID | Client | Title | Result |
|---|---|---|---|
| CAP-35 | Retail | Mass Mill attributes again (the name seed is 311413) | passed (2026-11-25) |
| CAP-36 | Retail | The per-expansion Milling ids attribute by id | passed (2026-11-25) |
| CAP-37 | Retail | The per-expansion Prospecting ids attribute by id | passed (2026-11-25) |
| CAP-38 | Retail | Nothing that worked before stopped (the four removed ids) | passed (2026-11-25) |
| LOC-4 | Retail | The deconstruct name family on a non-English client (amended, cleared to pending) | passed (2026-11-25) |
| SEEDS-LH-1 | Forever | Item sources with ForeverDB | passed (2026-11-25) |
| SEEDS-LH-2 | Forever | Item sources without ForeverDB | passed (2026-11-25) |
| SEEDS-LH-3 | Retail | No item sources on Retail | passed (2026-11-25) |
| LH-REVIEW-1 | Retail | Decide: the deconstruct name match over-reaches (Disenchanting Rod) | passed (2026-11-25) |

## Outfitter Reborn (3)

| Check ID | Client | Title | Result |
|---|---|---|---|
| SEEDS-OR-1 | Forever | Missing items described, with ForeverDB | passed (2026-11-25) |
| SEEDS-OR-2 | Forever | Missing items without ForeverDB | passed (2026-11-25) |
| SEEDS-OR-3 | Retail | No ForeverDB switch on Retail | passed (2026-11-25) |

## Quick Comms (1)

| Check ID | Client | Title | Result |
|---|---|---|---|
| FOREVER-27 | Both | The When editor's class picker offers Forever's nine classes | passed (2026-11-25) |

## Range Master (32)

| Check ID | Client | Title | Result |
|---|---|---|---|
| RANGE-19 | Forever | The Forever warrior's ladder is empty | passed (2026-11-25) |
| RANGE-20 | Forever | The Forever rogue's ladder is empty | passed (2026-11-25) |
| RANGE-21 | Retail | The Retail warrior's ladder is Taunt alone | passed (2026-11-25) |
| BANDS-12 | Forever | The owner's case: the Forever paladin's JUDGE band | passed (2026-11-25) |
| BANDS-13 | Forever | The Forever hunter keeps its set | passed (2026-11-25) |
| BANDS-14 (Warrior) | Forever | The Forever warrior's own band set | passed (2026-11-25) |
| BANDS-14 (Rogue) | Forever | The Forever rogue's own band set | passed (2026-11-25) |
| BANDS-14 (Priest) | Forever | The Forever priest's own band set | passed (2026-11-25) |
| BANDS-14 (Shaman) | Forever | The Forever shaman's own band set | passed (2026-11-25) |
| BANDS-14 (Mage) | Forever | The Forever mage's own band set | passed (2026-11-25) |
| BANDS-14 (Warlock) | Forever | The Forever warlock's own band set | passed (2026-11-25) |
| BANDS-14 (Druid) | Forever | The Forever druid's own band set | passed (2026-11-25) |
| BANDS-15 (Warrior) | Retail | The Retail Warrior's own band set | passed (2026-11-25) |
| BANDS-15 (Paladin) | Retail | The Retail Paladin's own band set | passed (2026-11-25) |
| BANDS-15 (Hunter) | Retail | The Retail Hunter's own band set | passed (2026-11-25) |
| BANDS-15 (Rogue) | Retail | The Retail Rogue's own band set | passed (2026-11-25) |
| BANDS-15 (Priest, Mage, Warlock) | Retail | The Retail Priest, Mage, Warlock's own band set | passed (2026-11-25) |
| BANDS-15 (Death Knight) | Retail | The Retail Death Knight's own band set | passed (2026-11-25) |
| BANDS-15 (Shaman) | Retail | The Retail Shaman's own band set | passed (2026-11-25) |
| BANDS-15 (Monk) | Retail | The Retail Monk's own band set | passed (2026-11-25) |
| BANDS-15 (Druid) | Retail | The Retail Druid's own band set | passed (2026-11-25) |
| BANDS-15 (Demon Hunter) | Retail | The Retail Demon Hunter's own band set | passed (2026-11-25) |
| BANDS-15 (Evoker) | Retail | The Retail Evoker's own band set | passed (2026-11-25) |
| BANDS-16 | Both | The tier roles in the band editor | passed (2026-11-25) |
| BANDS-17 | Both | An existing profile is kept | passed (2026-11-25) |
| BANDS-JC-1 | Both | Decide: no schema step for the tier roles | passed (2026-11-25) |
| BANDS-JC-2 | Both | Decide: the warrior's and Forever rogue's 5-8 band is a yard band (CLOSE), not a dead zone | passed (2026-11-25) |
| BANDS-JC-3 | Both | Decide: no tier band for crowd-control-only abilities | passed (2026-11-25) |
| BANDS-JC-4 | Both | Decide: the first-run seed still adds the Hunter set to every class | passed (2026-11-25) |
| BANDS-JC-5 | Both | Decide: the band labels | passed (2026-11-25) |
| BANDS-JC-6 | Both | Decide: "Judgment" spelled US in authored text | passed (2026-11-25) |
| RANGE-REVIEW-1 | Forever | Decide: Distract 1725 as the Forever rogue's ranged anchor | passed (2026-11-25) |

## Skill Master (8)

| Check ID | Client | Title | Result |
|---|---|---|---|
| SM-SEEDFDB-1 | Forever | Angelique Butler is now Alliance (the one data change) | passed (2026-11-25) |
| SM-SEEDFDB-2 | Forever | Decide: five Forever-only trainers ForeverDB disagrees on | passed (2026-11-25) |
| SM-FDB-1 | Forever | With ForeverDB: not loaded at login, diagnostics line | passed (2026-11-25) |
| SM-FDB-2 | Forever | With ForeverDB: a book-taught rank's sources in the skill tooltip | passed (2026-11-25) |
| SM-FDB-3 | Forever | With ForeverDB: the book seller's card in the trainer popup | passed (2026-11-25) |
| SM-FDB-4 | Forever | With ForeverDB: the Use ForeverDB switch | passed (2026-11-25) |
| SM-FDB-5 | Forever | Without ForeverDB: unchanged tooltips | passed (2026-11-25) |
| SM-FDB-6 | Retail | Skill Master is absent on Retail | passed (2026-11-25) |

## Recording results

Results are recorded here and in each repo's `docs/smoke-tests.md` (on the check's `Result:` line or Result column) once the owner reports them, with the owner's name and the date. An agent never marks a check passed. A decision row's ruling goes in the owner's findings and, where it changes data, becomes a follow-up item or issue. LibKa0s has no smoke-tests.md: its LK-FDB rows are recorded here and in the run's execution record.

## Result

On 2026-11-25 the owner reported every check on this sheet run in game and passed ("ive run the smoke tests from the
previous seed validation run, you can mark them as all passed"). That covers all 66 checks, including the 9 decision rows, which
are accepted as built. Some rows are superseded by the Item Search run (`docs/2026-11-25-ITEM_SEARCH`), which removes the
features they test: SEEDS-LH-1, SEEDS-LH-2, Bank Ledger FOREVER-20 to FOREVER-22, and Drop Watcher FOREVER-18 and
FOREVER-19. They passed against what shipped here.
