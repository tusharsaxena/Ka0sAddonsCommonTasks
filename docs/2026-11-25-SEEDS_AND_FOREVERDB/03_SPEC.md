# Spec: seeds and ForeverDB

Decided by the lead under the owner's standing autonomy (decide, checkpoint, branch, push at milestones, merge on
go-ahead). Every builder follows this file. A deviation is written into the builder's own commit body and reported.

## 0. Facts this spec rests on (measured 2026-11-25)

- **ForeverDB** (github.com/foreverfraddons/forever-db, GPL-3.0 merged data, CurseForge project 1807282).
  - It ships three LoadOnDemand addons, each with its own global: `ForeverDB` → `ForeverDB`, `ForeverDB_Full` →
    `ForeverDBFull` and `ForeverDB_Locales` → `ForeverDBLocale`.
  - The TOC reads `## Interface: 16001, 120007` and `## Version: 2026.11.24.46`.
  - Each build is an immutable git tag, `vYYYY.MM.DD.N` (newest `v2026.11.24.46`, commit
    `6e0a34b4bd017483aff616f5766348e1cea519ae`). Only the moving `latest` release carries assets
    (`forever.json.gz` and others), so a run pins the **tag** and reads `ForeverDB/ForeverDB*.lua` at that tag.
  - **The Lua shape.** Files are generated as `ForeverDB = ForeverDB or {}`, `local D = ForeverDB`,
    `D.meta = {...}`, `D.<tbl> = D.<tbl> or {}`, then `;(function() local t = D.<tbl> ... t[<key>]={...} ... end)()`.
    Keys are numbers, or strings such as `"c1001"` (creature) and `"o45"` (object). Rows are positional arrays.
  - **`meta`:** `build` (date), `hash`, `counts`, `sourceList`.
  - **The tables the adapter reads, with their positions:**
    - `npc[id] = {name, sub, minLv, maxLv, rank}`
    - `item[id] = {name, quality, reqLevel, itemLevel, class, subclass, inventoryType, icon, allowableClass, requiredSkill, requiredSkillRank, allowableRaces, minFaction, minReputation}`
    - `quest[id] = {title, level, minLevel}`
    - `qg[q]` and `qe[q] = {"c288", "o45", ...}`
    - `drop[item]`, `odrop[item]` and `idrop[item] = {sourceId, chancePer10000, sourceId, chance, ...}` (flat pairs; `0` = rate unknown)
    - `vend[item] = {npcId, ...}`
    - `vp[npc] = {[item] = {price, seen}}`
    - `world[item]` (minimum level)
    - `spm["c<id>" | "o<id>"] = {[uiMap] = {x, y, x, y, ...}}` (0–1000)
    - `nfac[npc] = "A" | "H" | "AH"`
    - `obj[id] = {name}`
    - `trn[npc] = {[spellName] = {cost, level, ?, ?}}`
    - `spf.<Name>` (Shortest Path Forever data, `trainers` among it)
  - The README's table list is authoritative for meaning. A field that is absent reads as nil.
- **The owner's install** is ForeverDB 2026.11.24.46 under `/mnt/g/Games/Blizzard/World of Warcraft/_forever_/Interface/AddOns/`.
  It is read-only for every agent.
- **Ketho/BlizzardInterfaceResources**, branches `live` and `forever`, is the source of the kit's
  `testkit/client_globals_{live,forever}.lua`. The Forever file was generated at sha `d1ee5698…` (2026-10-21) by
  `tools/client_globals_data.lua`. The branches also carry `Resources/LuaEnum.lua`.
- **Versions:** standard v2.120.0, LibKa0s v1.113.0, dev-copilot 2.11.0 (installed and master).

## 0.5 Who needs ForeverDB installed (owner question, 2026-11-25)

The owner asked whether every user needs forever-db installed, as a dependency through `.pkgmeta`, or whether it is
only a dev-time reference for the authors. **No player ever needs it.** ForeverDB is used in two ways:

1. **Seed validation (dev time, authors only).**
   - What reads it: `/dev-copilot:validate-seeds`, through `scripts/foreverdb.py`.
   - Where it reads from: the pinned GitHub tag, or the owner's install.
   - What a player gets: the corrected ids and positions, committed as the addon's own data.
   - Shipped code never reads ForeverDB for this.
2. **The runtime adapter (`LibKa0s-ForeverDB-1.0`, #105), optional for players.**
   - **How it is declared:** an addon that adopts it lists ForeverDB in `## OptionalDeps`, and **MAY** list it
     under `.pkgmeta` `optional-dependencies` so that CurseForge shows the relationship.
   - **What it never does:** list it in `## Dependencies` or under `.pkgmeta` `required-dependencies`. ForeverDB's
     own README tells consumers to make it required; this collection deliberately does not.
   - **Without ForeverDB:** the addon works unchanged, and the one feature that would use it says it needs ForeverDB.

In this run no addon adopts the adapter; each candidate consumer gets an issue. So after this run, no shipped addon
reads ForeverDB at runtime.

## 1. Licensing rule (holds for every item)

ForeverDB's data is GPL-3.0, while LibKa0s and every addon are MIT.

- **Never** copy ForeverDB rows into any Ka0s repo. That covers the payload, test fixtures and frozen bundles.
- The kit fake and every test fixture use **invented** values in ForeverDB's real *shape*: made-up names, ids from
  a range no real row uses (900000+), and made-up coordinates.
- A seed bundle that used ForeverDB evidence stores no raw rows. It stores:
  - `SOURCES.md`: the tag, its commit sha, the sha256 of every file read, the fetch date, the URLs, and the version
    of the owner's install if present;
  - per-id **verdicts** (`found`, `missing`, `name-mismatch`, `position-off`, with the shipped value). A verdict
    may quote the single field it compares, such as an NPC's name, which is a fact and not a copy of the database;
  - the hand-written `ANALYSIS.md`.
- **Replay** means re-fetching the pinned tag, which is immutable, not an offline `raw/`. The standard records this
  as the one exception to clients-§10's bundle rule.

## 2. WowAddonStandards: v2.121.0 (item SF-STD-01)

Fetch `origin/master` first and renumber if another session moved it (see the standard-version-collisions memory).

- **clients-§10 gains a subsection, *A second evidence source for Forever: ForeverDB*.**
  - DB2 is the client's data, so it knows nothing the server supplies: creatures, their spawns, trainers, vendors,
    quest givers and objects. The collection found this three times (DpsRace's dummies, Outfitter Reborn's quest
    NPCs, Skill Master's trainers).
  - For the `forever` flavor, a contract **MAY** name ForeverDB as a secondary source for exactly those facts.
  - DB2 stays primary for everything DB2 has. ForeverDB never overrides a DB2 answer, and when the two disagree
    the result is a flag.
  - A run pins one ForeverDB tag per run and records it.
  - ForeverDB is **evidence, not truth**: its sources are classic-era server dumps merged with Forever data, so a
    mismatch is a candidate for a human ruling, never an automatic apply. The precedent the owner recorded for
    Skill Master, "trust the sources (the 1.12 dump) over owner smoke", is one contract's ruling and not a
    collection rule.
  - The bundle follows the §1 licensing rule: verdicts and hashes, no raw rows, replay by tag.
  - The Retail flavor never reads ForeverDB.
- **A new clients-§11, *Optional runtime data addons*.** A Ka0s addon that uses an external data addon (ForeverDB
  is the first):
  - reads it only at runtime, through `LibKa0s-ForeverDB-1.0`, and never through its own wiring;
  - lists it in `## OptionalDeps`, **MAY** list it under `.pkgmeta`'s `optional-dependencies`, and never lists it in
    `## Dependencies` or `.pkgmeta`'s `required-dependencies` (§0.5); a player never needs it installed;
  - may also use it at dev time only, as seed-validation evidence (clients-§10), which needs nothing from a player;
  - loads it only when a feature first asks, never at login;
  - works unchanged without it, and says in the feature's tooltip or settings row that the feature needs it;
  - never vendors or copies its data, test fixtures included (§1);
  - gates the feature on Forever (clients-§4); the Retail answer is "not available";
  - records the memory it adds in the perf ceiling of the addon that loads it.
- **New anti-patterns:**
  - a GPL data addon vendored or copied into an MIT repo;
  - a data addon loaded at login, or required.
- **The usual ripple:** the index blurb and anti-pattern range, the CHANGELOG, the version stamps, the matching
  NEW_ADDON_CONTEXT and AUDIT.md lines where they enumerate the clients rules, and open-evolutions if it tracks
  #91 or #105.

## 3. dev-copilot: 2.12.0 (item SF-DC-01)

- **A new `scripts/foreverdb.py`** (Python 3 stdlib only, with tests in `scripts/test_foreverdb.py` beside the
  others).
  - `status [--json]`: the newest `vYYYY.MM.DD.N` tag, read from the GitHub tags API with no auth and with
    `git ls-remote --tags` as the fallback.
  - `fetch --tag <tag> --date <YYYY-MM-DD> [--from-install <AddOns/ForeverDB dir>]`:
    - downloads `ForeverDB/ForeverDB.toc` and every Lua file the TOC lists at that tag from
      `raw.githubusercontent.com`, or reads them from the install directory;
    - checks that the TOC `## Version` equals the tag without its `v`, and refuses on a mismatch;
    - parses the generated Lua with a small stdlib parser written for this format: table constructors, strings with
      escapes, numbers, `nil`/`true`/`false`, `[k]=` and positional fields, and the `t[k]=` statement form;
    - writes `foreverdb.json` and `SOURCES.json` (tag, commit sha, per-file sha256, date) to
      `${XDG_CACHE_HOME:-~/.cache}/ka0s-seeds/foreverdb/<tag>/`;
    - prints that path;
    - re-uses the cache when its sha256s match.
  - The User-Agent is `ka0s-seed-check`. The tests run on an invented fixture and never touch the network.
- **The validate-seeds WoW overlay (`profiles/wow/validate-seeds.md`)**, section `flavor`:
  - the `forever` flavor's row may add **Evidence: ForeverDB** beside product `wowf`;
  - the run then resolves the tag through `python3 "<root>/scripts/foreverdb.py" status`;
  - a `retail` row that names ForeverDB is a stop;
  - the product-follows-client rule is unchanged.
  - Add a line to the `--build` handling: `--foreverdb <tag>` pins the tag.
  - The generic `commands/validate-seeds.md` learns the `--foreverdb <tag>` argument as a passthrough only when the
    overlay is active. Keep the generic spec's language generic.
- **Also:**
  - `roster_clients.py` needs no change;
  - CHANGELOG, plugin version 2.12.0, README/CLAUDE parity, and `test_command_specs.py` green.
- **Contracts call it as `python3 "<root>/scripts/foreverdb.py" ...`.** For the first-run bundles in this run,
  builders call the dev-copilot **feature-branch checkout's** script, because the plugin is updated only after merge.
  Each bundle's SOURCES.md records the dev-copilot commit it used.

## 4. LibKa0s: v1.114.0, a local tag (items SF-LK-01 and SF-LK-02)

### SF-LK-01: `LibKa0s-ForeverDB-1.0` (#105)

- **The file:** `LibKa0s/ForeverDB.lua` (MINOR 1), loaded in `LibKa0s.xml` after `Item.lua`, in the derived and
  pinned load lists.
  - It is registered in `MODULES`, in DebugLogDiagnostics' module list and in `docs/api/ForeverDB/`
    (`version-1-docs.md` and `members-1.json` via `tools/gen-api-members.lua`).
  - It also goes in CONSUMERS.md and the README module table.
  - Its header follows Role.lua's shape: why it exists, rules every member obeys, dependencies.
- **Members.** Each answers plain tables or nil and never errors on a missing, old or reshaped ForeverDB:
  - `Available()`, which answers `ok, reason`:
    - Retail (through `Compat.IsForever` at call time; without Compat it assumes "not Forever") answers
      `false, "client"`;
    - the addon is not installed (`C_AddOns.GetAddOnInfo` / `DoesAddOnExist`) answers `false, "missing"`;
    - otherwise it calls `C_AddOns.LoadAddOn("ForeverDB")` **only here** and only the first time; a load failure
      answers `false, <reason>`, and `_G.ForeverDB` not being a table answers `false, "reshaped"`;
    - the answer is cached for the session; `lib.__reset()` exists for tests.
  - `IsLoaded()` answers without loading anything, for diagnostics.
  - `Meta()` answers `{ version = TOC Version, build, hash, counts }`, or nil.
  - `NPC(id)` answers `{ id, name, subname, minLevel, maxLevel, rank, faction = "A"|"H"|"AH"|nil }`.
  - `Item(id)` answers `{ id, name, quality, requiredLevel, itemLevel, classID, subclassID, inventoryType, icon }`.
  - `Quest(id)` answers `{ id, title, level, minLevel, givers = { {kind="npc"|"object", id=n}, ... }, enders = {...} }`.
  - `ItemSources(id)` answers
    `{ creatures = { {id, chance} }, objects = {...}, items = {...}, vendors = {ids}, worldMinLevel }`. Chance is
    0..1, and nil where the source says 0 (rate unknown). It answers nil when there is nothing at all.
  - `VendorPrice(itemID)` answers `price, npcID` (the lowest seen across `vend[item]` × `vp[npc][item]`), or nil.
  - `Spots(kind, id)` answers `{ [uiMapID] = { {x, y}, ... } }` with x and y in 0..1. `kind` is "npc" or "object".
  - `TrainerSpells(npcID)` answers `{ [spellName] = { cost, level } }`, or nil.
  - The Full and Locales addons are **not** read in v1. They are recorded as a later minor.
- **Its rules:**
  - every member calls `Available()` first, so the first lookup is what loads;
  - globals are read bare at call time;
  - no pcall: defensive type checks instead, so a row that is not a table, or a field that is not the expected type,
    answers nil;
  - a lookup returns a fresh table, never ForeverDB's own row, so a caller cannot mutate the shared database.
- **The kit fake:** `testkit/mock_foreverdb.lua`.
  - `install(m, opts)` puts an invented `ForeverDB` global in the mock environment together with `C_AddOns`
    stubs (exists, load succeeds or fails, `GetAddOnMetadata` version).
  - Its presets are `present`, `missing`, `loadfails` and `reshaped`, and it records the load count, so a test can
    prove that nothing loads at file load.
  - This is a kit revision bump; record it in `testkit/README.md` and `docs/api/testkit/version-<n>-docs.md`.
- **Tests:** `tests/test_foreverdb.lua` covers:
  - the client gate;
  - absent, missing, load failure and reshaped;
  - every member's field mapping, chance scaling and coordinate scaling;
  - fresh tables;
  - no load at file load;
  - diagnostics with and without it loaded.
- **Diagnostics:** the library's diagnostics dump reports ForeverDB `present` / `loaded` / its version, plus
  `meta.build` and `hash` when it is loaded. It never loads ForeverDB itself.
- **Bookkeeping:** a CHANGELOG `v1.114.0` entry, the README version, and every gate in LibKa0s's CLAUDE.md green
  on both kit profiles.

### SF-LK-02: LibKa0s seed contract (#93)

- **The contract.** `docs/validate-seeds.md` with flavors `retail` (source Ketho/BlizzardInterfaceResources `live`)
  and `forever` (branch `forever`). The *build* is the branch's commit sha. It carries every heading the command
  requires.
- **The tool.** `tools/seeds/libseeds.py` (stdlib), with `test_libseeds.py`. Subcommands:
  - `status`: compares the sha recorded in `testkit/client_globals_<live|forever>.lua` with the branch head (via
    `gh api` or a raw fetch).
  - `freeze --sha --date --bundle`: fetches GlobalAPI.lua, FrameXML.lua and LuaEnum.lua at the sha into a
    git-ignored cache (MIT-compatible data, so the bundle may keep `raw/*.lua.gz` as clients-§10 asks).
  - `derive`, which writes:
    - (a) the kit-globals diff: names added and removed against the checked-in kit file;
    - (b) the **assumptions** list, scanned from the shipped `LibKa0s/*.lua`: every `Enum.X.Y` member, and every
      `C_*.*` and bare global API the payload calls. Each is checked on each branch. An assumption missing on a
      branch is a candidate that needs a ruling, for example "guarded rung: absent on Forever by design, cite
      Compat.lua:<line>";
    - (c) a **reach** check: every name in the kit file's set still exists upstream.
  - `rule --tsv`, `check` (prints OK when nothing is unruled), `report` and `apply`. `apply` regenerates
    `testkit/client_globals_<branch>.lua` through the existing `tools/client_globals_data.lua`, and only when the
    flavor's rulings accept the regeneration. That is a kit revision.
  - Rulings live in `tools/seeds/{retail,forever}_rulings.json`, keyed by name, never by sha.
- **The first-run bundles:** `docs/seed-research/2026-11-25-retail/` and `2026-11-25-forever/`, with SOURCES,
  candidates, RULINGS, DIFF and a hand-written ANALYSIS.
- **Applying.** Apply only where the evidence is unambiguous; a regenerated kit file must leave every kit and
  consumer-facing test green. List anything uncertain as "needs owner review" in ANALYSIS.
- **The gate:** CLAUDE.md gains `python3 -m pytest -q tools/seeds` (or unittest, if pytest is absent; detect it).

## 5. Addons (#102 and ForeverDB evidence)

**General rules for each addon item:**

- Follow that repo's CLAUDE.md gate. Run the headless suite under both kit profiles where its Clients value is
  `Retail · Forever`, and Forever only for SkillMaster.
- The contract takes the shape of the existing adopters: `tools/seeds/seeds.py` + `test_seeds.py` +
  `<flavor>_rulings.json`, with bundles under `docs/seed-research/2026-11-25-<flavor>/`.
- The wago fetches pin `?build=`: Retail `wow` and Forever `wowf`, the newest live non-bgdl build from
  `https://wago.tools/api/builds`, resolved once and recorded.
- The User-Agent is `<addon>-seed-check`.
- Add the seed test command to the repo's CLAUDE.md commit gate, the (c) follow-up.
- Change shipped data only where DB2 (or, for Forever server-side facts, ForeverDB) is unambiguous **and** the
  repo's precedent supports it. Everything else is ruled, or listed as needs-owner-review. Never re-litigate an
  owner ruling recorded in the repo: "EMPTY BY DECISION" stays empty, and so on.

| Item | Repo | Scope |
|---|---|---|
| SF-CT-01 | CombatTrail | The contract and tool, porting DpsRace's (`../DpsRace/docs/validate-seeds.md` and `tools/seeds/`; read them, never edit DpsRace). Flavors are `retail` (Hearthstones via the DpsRace rules; IgnoreSeeds 6603, 75 and 5019 on the Spell tables) and `forever` (IgnoreSeeds). The Forever Dummies stay EMPTY BY DECISION. The ForeverDB evidence step lists training-dummy NPCs (name match) as *information only* in ANALYSIS, ruled reject by precedent. Retail Dummies are recorded as not checkable. |
| SF-RM-01 | RangeMaster | The contract and tool for `defaults/SpellSeeds.lua`, both flavors. Per id it checks that the spell exists (SpellName), the class (SkillLineAbility / SpellClassOptions), and its **range** (SpellMisc `RangeIndex` → SpellRange `RangeMin_*`/`RangeMax_*`). The derived chip, ladder and anchor ranges are compared against what the addon's code assumes for each chip or rung. That is the high-value check: report every chip whose DB2 range disagrees with the band or rung it sits in. On Forever it also checks rank-1 ids. A recorded owner precedent stands: Wing Clip 2974 is the melee anchor, and Raptor Strike and Attack 6603 have no range requirement. |
| SF-LH-01 | LootHistory | The contract and tool for `modules/Attribution.lua`'s `DECONSTRUCT_IDS`, both flavors (SpellName, SkillLineAbility for the Enchanting, Inscription and Jewelcrafting lines). Milling and Prospecting on Forever stay EMPTY BY DECISION. |
| SF-SM-01 | SkillMaster | Add **ForeverDB evidence** to the forever flavor. Trainers (`defaults/Trainers_Forever.lua`): match each trainer by name to `npc` (and `nfac` against the faction the trainer is shipped under), and compare the shipped position against `spm` (uiMap, distance in map units) and `spf` trainers. Gathering node names (`Gathering_Forever.lua`) are checked against `obj`. Each mismatch is a candidate, ruled with precedent: "trust the sources (1.12 dump)", "nothing shown as unverified", the neutral trainers of Zephras Isle and Riverglades, and Annora at Uldaman's back entrance at 65.3,42.6. Apply only unambiguous position or name fixes with the evidence cited, and list the rest for owner review. |
| SF-QC-01 | QuickComms | `CLASSES` per client (clients-§5): the Forever list drops DEATHKNIGHT, MONK, DEMONHUNTER and EVOKER, it is picked through Compat, and its test pins both. Update the contract's flag ruling. Also pin `tools/derive-gameids.py`'s Retail fetch to `?build=`. |
| SF-OR-01 | OutfitterReborn | Pin `tools/gen-zones.lua`'s wago fetch to a build, as an argument, and update the contract's Notes. No ForeverDB step: its 23 uncheckable quest NPCs are Retail (Argent Tournament, Ulduar), and ForeverDB is classic-era. |
| SF-GATE-01 | AuraMaster, ConsumableMaster, DropWatcher, KickCD, PrettyChat, WhatGroup | Add each contract's own seed test command (as written in its `## Gate`) to the CLAUDE.md commit gate, one commit per repo with id `SF-GATE-01`. Docs only. |

## 6. What is filed, not built (lead, spaced GitHub writes)

- One `#105` consumer issue each in DropWatcher, LootHistory, BankLedger, SkillMaster and OutfitterReborn, each
  naming the feature, the adapter members it would use, and "smoke with and without ForeverDB".
- Comments on LibKa0s#93, #102 and #105 that link this bundle. They are closed only when the run merges.
- MultiMeters (enum fallbacks and one measured creature id) and BankLedger (test-mode sample data only) get no
  contract. The reasons are recorded in #102's closing comment.
- DpsRace's orphaned contract stays where it is (the repo is retired and archived). CombatTrail's contract says it
  supersedes it.

## 7. Smoke (owner)

The lead writes `06_SMOKE_TESTS.md` and a `Documents/Ka0sPendingSmoke-2026-11-25-ADDED-SEEDS.csv` sheet (a new file;
never overwrite an existing sheet). Its checks:

- `/dump LibStub("LibKa0s-ForeverDB-1.0").Available()` on Forever with ForeverDB installed, and with it disabled;
- `.NPC(<a trainer id>)`, `.ItemSources(<a common drop>)` and `.Meta()`;
- the diagnostics dump showing the ForeverDB line;
- Retail answering `false, "client"`;
- no ForeverDB in the addon list's loaded set at login;
- QuickComms' Forever class picker without DK, Monk, DH or Evoker;
- any shipped-data change an addon item made (a trainer position, a RangeMaster chip, and so on), one row each.

## 8. Owner answers (2026-11-25, asked up front)

These supersede anything above that conflicts with them.

1. **Consumers:** "All five consumers". The adapter is adopted **in this run** by Drop Watcher, Loot History,
   Bank Ledger, Skill Master and Outfitter Reborn (§9). §6's "file one consumer issue each" is withdrawn. §0.5's
   "no shipped addon reads ForeverDB at runtime" becomes: five addons read it at runtime as an **optional**
   dependency, and no player needs it installed.
2. **Fix policy:** "Fix everything flagged". Builders apply every mismatch the evidence supports, judgment calls
   included, each with its evidence cited in the ruling and **one smoke row per shipped-data change**. Two things
   are not mismatches and stay as they are:
   - an owner ruling already recorded in the repo (for example EMPTY BY DECISION, Wing Clip as the melee anchor,
     or the neutral trainers);
   - a candidate the data cannot decide.
   Every judgment-call fix is listed in the item's ANALYSIS under *Judgment calls applied*, so the owner can
   reverse any of them at smoke.
3. **Kit regeneration:** "Regenerate". SF-LK-02 regenerates `testkit/client_globals_{live,forever}.lua` when
   Ketho has moved. That is a kit revision inside v1.114.0, with every LibKa0s gate green and the delta recorded.
4. **QuickComms CLASSES:** "Split per client" (SF-QC-01, as in §5).

## 9. Consumer adoption (#105), one item per addon

Each item waits for SF-LK-REL and runs **after** that repo's own seed item, in the same clone and on the same
branch.

**Steps, in order:**

1. **Re-vendor.** Copy LibKa0s v1.114.0 from `~/ka0s-scratch/seeds/LibKa0s` (its branch head, tag `v1.114.0`)
   following `/dev-copilot:wow-revendor-libka0s`'s rules:
   - both payloads are copied whole, `libs/LibKa0s/` and `tests/_kit/`;
   - the CLAUDE.md provenance line moves to v1.114.0;
   - the icon declaration and prune are re-run;
   - a revendor bundle goes under `docs/revendor/2026-11-25-v1.114.0/`.
2. **Wire the adapter in:**
   - `## OptionalDeps` gains `ForeverDB`, and `.pkgmeta` gains `optional-dependencies: [forever-db]` (check the
     CurseForge slug, `forever-db`, against the project page link in the issue);
   - the feature is gated on Forever (clients-§4);
   - it reads only through `LibKa0s-ForeverDB-1.0`, and its first call is what loads;
   - it is hidden or inert without ForeverDB, and its tooltip or settings row says it needs ForeverDB;
   - a settings toggle, default on, sits where the addon's other display options live.
3. **Write a characterization test first**, then the feature's tests on the kit fake (`mock_foreverdb`) with the
   present, missing and reshaped presets, plus a Retail-profile case that proves it is inert.
4. **Record perf.** The perf ceiling's notes record that ForeverDB is about 12 MB on disk and that the load happens
   on first use.
5. **Add smoke rows** to `docs/smoke-tests.md`: with ForeverDB, without it (disabled in the addon list), and on
   Retail.
6. **Run the repo's whole gate** on both kit profiles.

| Item | Repo | The feature |
|---|---|---|
| SF-DW-01 | DropWatcher | **The drop card or detail view.** It shows where the item drops: up to three top sources, each with its chance. It also shows a world-drop minimum level when there is one, and "sold by" when the item is a vendor item. Members used: `ItemSources` and `NPC` (for the names). |
| SF-LH-02 | LootHistory | **The History browser's item tooltip or detail.** It shows "Drops from" (the top 3, with chances) and "Sold by" with the lowest vendor price seen. Members used: `ItemSources`, `NPC` and `VendorPrice`. |
| SF-BL-01 | BankLedger | **The holdings valuation.** It adds a vendor buy price (from ForeverDB) beside the client's sell price, in the item tooltip or detail and as an optional value basis where the ledger already offers one. It never replaces the client's own price. Member used: `VendorPrice`. |
| SF-SM-02 | SkillMaster | **Recipe sources and trainer spots.** A recipe or item tooltip in the skills window gains its sources (vendor or drop). The trainer popup gains ForeverDB's map spots when the shipped data has none, never overriding shipped positions, which SF-SM-01 has already reconciled. Members used: `ItemSources`, `Spots` and `NPC`. |
| SF-OR-02 | OutfitterReborn | **Items not in the bags.** Where the outfit window shows an item the player does not carry, which the client cannot describe until it is cached, it falls back to ForeverDB's quality and required level. The client's own answer always wins when it exists. Member used: `Item`. |
