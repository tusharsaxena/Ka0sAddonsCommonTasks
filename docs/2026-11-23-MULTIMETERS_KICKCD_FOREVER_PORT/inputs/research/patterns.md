# The dual-client port recipe as of 2026-11-23, applied to MultiMeters and KickCD

Read-only study. Status marks: **V** = VERIFIED (read at the cited place, or run here), **I** = INFERRED (reason given),
**U** = UNKNOWN (probe given).

| Short name | Path |
|---|---|
| `STD` | `GIT/WowAddonStandards/standards/standards` (master 6e062cf, v2.117.0) |
| `LK` | `GIT/LibKa0s` (master a77419d6, tag v1.110.0) |
| `CT-DOCS` | `GIT/Ka0sAddonsCommonTasks/docs` |
| `FUI` / `RUI` | Forever 1.60.1.71037 (734f065) / Retail 12.1.5.70961 (ab5cb85), `Interface/AddOns/` |
| `API` | `Blizzard_APIDocumentationGenerated/` under either UI root |
| `MM` / `KC` | the pinned snapshots, MultiMeters bf67258 / KickCD 333cd49 |
| `LH-PORT` | `CT-DOCS/2026-11-22-LOOTHISTORY_BANKLEDGER_FOREVER_PORT` |
| `QC-PORT` | `CT-DOCS/2026-11-10-QUICKCOMMS_FOREVER_EMOTES` |
| `DW-SPEC` | DropWatcher `docs/superpowers/specs/2026-11-13-drop-watcher-forever-port-design.md` |
| `AM-SPEC` | AuraMaster `docs/superpowers/specs/2026-11-14-auramaster-forever-port-design.md` |
| `CB-Q` | CombatTrail `docs/forever-quirks.md`, section "CombatTrail-specific quirks" |

---

## 0. What matters most

1. **The recipe is settled.** These are the last two `Retail (port pending)` rows (`WowAddonStandards/standards/ADDONS.md:25,28`).
   No standard change or version bump is needed to port them, only the two roster cells.
2. **Both addons already have the per-client default skin.** Most of their red forever-profile tests are fixtures that
   pin Ka0s Default pixels (section 1).
3. **MultiMeters has two real engine problems on Forever.**
   - `specIconID` is an unconditional secret there (V, `FUI/API/DamageMeterDocumentation.lua:203,242`; Retail says
     `NeverSecret` at the same lines). The in-combat join key `class + specIcon + isLocalPlayer`
     (`MM/modules/Aggregator_Identity.lua:114-122`) collapses to class + me, so two players of one class always collide.
   - Both client formatter objects raised on a secret on Forever build 70888 (V, `CB-Q`, "The client number formatters
     refuse a secret"). `NumericRuleFormatter` is MultiMeters' first rung (`MM/modules/Format.lua:525-541`). It will
     fall to `AbbreviateNumbers`, which drew `69.5625` unfloored on a plain value in that probe.
4. **KickCD has a silent failure that the green globals scan cannot see.** `GetNumSpecializationsForClassID` exists
   only as a deprecation fallback, and that addon is gated `classic, standard`
   (`FUI/Blizzard_DeprecatedSpecialization/*.toc`, `Deprecated_Specialization_Standard.lua:4-10`). `KC/core/Util.lua:273`
   and `KC/settings/Spells_Header.lua:88` test for it and return empty. **I:** it is nil on Forever, because its sibling
   `GetSpecialization` from the same file was measured nil (`CT-DOCS/2026-11-07-WOW_FOREVER_PORT/00_OWNER_CHECKS_AND_RULINGS.md:11`).
5. **KickCD needs its own Forever seed pipeline run.** Every shipped key is a Retail spec id, every Forever rank is its
   own spell id, and the seed is written into the profile at first creation.
6. **Re-vendor to v1.110.0 is not needed for function.** It is cheap and recommended as the first item (section 6).

---

## 1. Current state and measured baselines (V, this session)

| | MultiMeters | KickCD |
|---|---|---|
| master | bf67258, 1.2.0 | 333cd49, 1.5.0 |
| TOC | `## Interface: 120105`, no gate | same |
| LibKa0s / kit | v1.109.0 / 59 | v1.109.0 / 59 |
| Client routing | none (no `IsForever`, `ClientKey`, `ForClient`, `clients =`) | none |
| `NS.DEFAULT_SKIN` | done, `core/SkinSetup.lua:126`, `defaults/Profile.lua:902` | done, `core/SkinSetup.lua:127`, `defaults/Profile.lua:386` |
| Sim samples | hard-coded `Sim.Sample("retail")`, `modules/Aggregator_Preview.lua:79`; 13 Retail classes in `modules/SimWorld.lua:68-82` | `Sim.Sample()` per client, `modules/SimScenario.lua:68`; its stand-in copy is Retail-shaped |
| `Bindings.xml` | one shared key | none |
| `forever-quirks.md` | "Not applicable", `docs/ARCHITECTURE.md:557` | same, `:501`; also stale "Retail / Midnight only" at `:467` |
| validate-seeds | no contract | Retail only; Forever section promised, `docs/validate-seeds.md:22-24,167` |
| Files near the 1500 cap | Window_Header 1463, Schema_Compose 1386, Aggregator 1343, Row 1325, Tooltip 1289 | none (max 1092) |

Suites, run in `port/work/patterns/` copies through `ka0s-bounded`:

| Run | MultiMeters (passed/failed/skipped) | KickCD |
|---|---|---|
| retail, as is | 2657/0/3 | 1736/0/3 |
| forever, as is | **2612/45/3** | **1717/19/3** |
| forever, TOC `120105, 16001` (arms the globals scan) | 2612/45/3, scan PASS | 1717/19/3, scan PASS |
| forever, default skin forced to `ka0s` as a diagnosis | 4 failed | 3 failed |
| luacheck, armed copy | 0/0 in 195 files | 0/0 in 160 files |
| v1.110.0 trial, retail | 2656/1/3 | 1735/1/3 |
| v1.110.0 trial, forever | 2611/46/3 | 1716/20/3 |

Reading the diagnosis row (failing-name sets diffed):

- **MultiMeters:** 44 of the 45 are Ka0s Default pixel pins and go away with a `T.ka0sDefault` fixture helper
  (LootHistory LH-04, BankLedger `T.onKa0sDefault`). The one independent failure is "Compat: the spec shims prefer
  C_SpecializationInfo and fall back to the globals": the fixture expects globals the Forever profile removes. The
  other three failures in that run are artifacts of forcing the skin (two DefaultSkin assertions and the CRLF check).
- **KickCD:** 17 of the 19 are pixel pins. The two independent failures are "SimScenario: without LibKa0s the party is
  a copy of the library's rows" (the stand-in is Retail-shaped, expected nil specID, got 253) and "the profile default
  and the pre-store fallback name the library's DefaultSkin, never a literal" (the test itself expects `ka0s` on both
  profiles). The third failure in that run is the CRLF artifact.

The two vendor-sync cases skip in scratch copies because there is no sibling checkout, so vendor byte-identity was
**not** tested here.

Remote branch `KickCD origin/feature/glow-options` is already an ancestor of master. It predates this run, so it is
not this run's to delete.

---

## 2. The recipe

### 2.1 Order of work (what LootHistory, BankLedger, DropWatcher and QuickComms all converged on)

| # | Item | Rule or precedent |
|---|---|---|
| 0 | Bundle: research, rulings, design, items, RESUME, resume-state | CommonTasks CLAUDE.md; `LH-PORT` |
| 1 | Re-vendor, if taken, first and alone | DW-FP01, K101-BL-01 |
| 2 | Client routing seam and a static gate | LH-01 `8b10010` |
| 3 | Per-client test mock and helpers; forever profile green | LH-02, BL-02 |
| 4 | Identity and names | LH-03, BL-03, DW-FP04 |
| 5 | Default skin (both addons have it; only fixtures remain) | LH-04, skinning-§2 |
| 6 | Per-client gates, then seeds, sample and sim data | LH-05..08, DW-FP05..11 |
| 7 | Engine differences | LH-09..11 |
| 8 | Retail-affecting fixes, one commit and one test each | ruling R8 |
| 9 | Probe verbs and probe sheet | LH-13, BL-12 |
| 10 | **Shape commit last**: TOC, README, gate, docs, quirks, table, shape test | LH-14, BL-13, DW-FP12 |
| 11 | Smoke section | LH-15, BL-14 |
| 12 | Independent review, skeptic pass, fixes, git note | LH-REV, BL-REV |
| 13 | Roster flip in the same landing | STD-01 `2d7a05f`, clients-§2 |
| 14 | Execution record and smoke roll-up | CT-REC |

The shape commit goes last because the second TOC number arms the Forever globals scan and claims support
(DW-SPEC §4.1).

### 2.2 Required files per addon

| File | Change | Authority |
|---|---|---|
| `<Addon>.toc` | `## Interface: 120105, 16001`, CRLF kept, one TOC, no load-gating line, no version bump | toc-file.md:59-62 |
| `core/CompatClient.lua` (new) | route the client helpers, loaded straight after Compat | LootHistory, DropWatcher |
| seed file | a second plainly named list, both loaded by the one TOC | toc-file.md:83 |
| `README.md` | badge `WoW-Midnight_12.1.5_and_Forever_1.60.1`; description opens "Supports Retail and WoW Forever."; drop "support is planned"; test badge | documentation.md:66-67 |
| `CLAUDE.md` | gate names `lua tests/run.lua`, `KA0S_KIT_CLIENT=forever lua tests/run.lua`, bounded luacheck; link forever-quirks | clients-§6 |
| `DEPENDENCIES.md` | both clients, both numbers, both runs | LootHistory `tests/test_client_shape.lua` |
| `docs/testing.md` | both runs; automated runner is one profile per call | testing.md:47; STEP5 `99_WAVE1_REPORT.md` |
| `docs/ARCHITECTURE.md` | overview, `### Per-client features (clients-§4)` table, limitations, doc map `forever-quirks.md` Present (midnight stays Present) | clients-§4, documentation-§3 |
| `docs/forever-quirks.md` (new) | vendored v2.117.0 block, then `## <Addon>-specific quirks` | forever-quirks-§1 |
| `docs/forever-probes.md` (new) | probe, safe default, empty Result | LootHistory, DropWatcher |
| `docs/compat-layer.md`, `module-map`, `schema`, `scope`, `data-flow`, `slash-dispatch`, `debug`, `performance` | wherever the port touches them | wave 2, BL-13 |
| `docs/smoke-tests.md` | Client column and `## WoW Forever` | clients-§6 |
| `docs/test-cases.md` | regenerate with `lua tests/run.lua --list` | wave 1 found these stale |
| KickCD `docs/validate-seeds.md` | `## Flavor: forever`, rulings file, frozen bundle | clients-§10 |
| `.luacheckrc` | any newly read global | wave 2 |
| `WowAddonStandards/standards/ADDONS.md` | two rows to `Retail · Forever`, data only, no version bump | STD-01 |

Not touched: `.pkgmeta`, versions, tags, vendored files, earlier frozen bundles.

### 2.3 CompatClient

- Route `IsForever`, `IsRetail`, `ClientKey`, `ForClient`, `RegionalNames`, `UnitCharacterName`, `CharacterKey`, `RealmKey`
  from LibKa0s-Compat-1.0 (`LK/LibKa0s/Compat.lua:128-461`), plus Role readers where used.
- No `WOW_PROJECT_*`, interface number or `GetBuildInfo` client test anywhere else. LootHistory pins this with a
  static test. The only exception is a library-absent stub in the family (compat.md:42).
- **Stubs are real copies where degrading would corrupt or lose behavior**, held by a parity test on both profiles
  (K101-LH-REV F2). A name stub must still join the surname (LH-REV #9, BL-REV #2).
- Sim seam: each addon wraps every Compat member, so each new member is either wrapped or declared PURE. LootHistory
  wraps, BankLedger marks PURE because its seam needs a provider per wrapped member (`LH-PORT/07`, Deviations).
  MultiMeters lists its members in `core/SimSetup.lua:49-55`.
- A client branch in feature code is a smell. Declare, or pick a table once (clients-§3).

### 2.4 Feature gating (clients-§4)

- Library-registered (page, tab, row, rail entry, slash verb, launcher row, binding row): `clients = { "retail" }`.
  All exist in the vendored library (`LK/LibKa0s/OptionsRegistry.lua:49-70`, `Slash.lua:239-248`, `Launcher.lua:183-286`,
  `OptionsKeybinds.lua:70`, `OptionsNav.lua:36`).
- Host-registered (module, event, default, sample, diagnostics line): `Compat.ForClient(...)`.
- Absent, never hidden. Defaults that only a gated feature reads are built on its client only (DW-FP21, CombatTrail's
  table). Feature detection never decides a feature.
- A gated key in a copied profile is inert and kept, never deleted, never a crash (`AM-SPEC` §3.4, `QC-PORT/00_DESIGN.md` §4.2).
- Each declaration gets a present test and an absent test, and a table row. A test checks the table names them all.

### 2.5 Seeds (clients-§5, §10)

- Two lists, picked once by `ClientKey()` at load. Never a filtered Retail list. Empty by decision says so.
- Derive Forever from wago product `wowf`, pinned build, identifying generic User-Agent, stdlib Python, frozen bundle
  (`raw/*.csv.gz`, SOURCES, derived, DIFF, RULINGS, ANALYSIS), rulings as data, sentinels, date as an argument.
- Forever has no `SpecializationSpells` or `TraitTreeLoadout`. Use `Talent`, `TalentTab`, `SkillLineAbility` (V,
  clients.md §10; `AM-SPEC` §2, build 70938).
- Ranks are separate ids, linked by same name within the class, `SupercedesSpell = 0` (`AM-SPEC` §2).
- AuraMaster's shape is the closest to KickCD's need: `tools/spell-research/forever.py`, `forever_rulings.json`,
  rank closure, rune lines 2851/2853 excluded, Forever sentinels.
- The Retail list must stay byte-identical (`AM-SPEC` §3.3).
- The run ships through `/dev-copilot:validate-seeds KickCD forever` once the flavor section exists.

### 2.6 Role and specs

- Forever has one spec per class (ids 1482..1491), class-wide role (V, `AM-SPEC` §2; `CB-Q`).
- `LibKa0s-Role-1.0` minor 1 is already vendored: `Spec()`, `SpecsForClass()`, `Groups()`, `Resolve(store)`,
  `SetOverride`. Order: override, assigned, talent group with most points, spec API, saved (`LK/LibKa0s/Role.lua:20-30`).
- Store is `db.char.role` (QuickComms, DropWatcher).
- Talent changes arrive as `TRAIT_CONFIG_UPDATED` and `CHARACTER_POINTS_CHANGED`, not
  `PLAYER_SPECIALIZATION_CHANGED` (V, DropWatcher quirks, build 70790 research).
- `TALENT_GROUP_ROLE` is "MATCHED, NOT CONFIRMED" (`Role.lua:80-95`). Only Hunter's order was probed. Druid Feral
  always maps DAMAGER, so a bear needs the assigned role or an override.

### 2.7 Sim and test samples (preview-mode.md:75-78)

- Protagonists from `Sim.Sample()` for the running client. Crowd pools stay the host's and follow the same shape.
- Forever sample: `Sampleblade Mockvale`, no realm, one of nine classes, talent tree 1-3 and no Retail spec id.
- Also per client: spell ids (existing on that build), zones, icons, content kinds, test-mode copy.
- The library-absent copy follows the client too (the failing KickCD case).
- MultiMeters: fix `Aggregator_Preview.lua:79` and its `SAMPLE_COPY`, drop DK, Monk, DH and Evoker, replace Retail
  spells and spec icons. Samples must not show plain `specIconID` where the live client gives a secret.

### 2.8 Default skin

`NS.DEFAULT_SKIN = Skin:DefaultSkin()` read once, named in defaults and every fallback (skinning.md:36). A stored choice
is never rewritten. Both addons comply. Tests that pin pixels choose Ka0s Default by name, and one case per profile
pins the default.

### 2.9 Tests

- Both profiles 0 failed at every commit (clients-§6). luacheck 0/0. 1500-line cap. CCN 15 at release (reviews caught
  18 and 19 last time).
- A `tests/test_client_shape.lua` modeled on LootHistory's: TOC numbers and no gate, scan armed (`live,forever`),
  README badge and sentence, gate text in three files, quirks block order, doc map, table completeness, presence and
  absence per profile.
- Retail-only cases are declared skips (`T.RETAIL_ONLY`), each paired with an absence case.
- The kit's forever profile removes only five globals (`LK/testkit/mock_client.lua:49-55`). **Addon mocks must add
  what it does not model**: secret `specIconID`, no `GetNumSpecializationsForClassID` global, formatter raising on a
  secret, two-word `UnitName`, class-wide spec.
- Run the gate serially. LootHistory's `--jobs auto` gave 30 false failures on Forever (`LH-PORT/07`, Code and docs).

### 2.10 Probe verbs (ruling R4 shape, LootHistory `modules/Probe.lua`, `docs/forever-probes.md`)

- `/<slash> debug probe start|stop|status|clear`, bare = status. One chat line each. The disable bracket and a running
  sim refuse it.
- Record into `db.global.probe`, never a new SavedVariables global (QuickComms C4, LH R4).
- Stamp client, version, build, addon version. Cap (LH 500, BL 200), drop oldest, never drop a `start`, count drops.
  Cut strings at 400. Store `<secret>` for secrets. Private frame. Reads outside the sim seam.
- BankLedger's resumes across reloads and records start facts again. That is the better shape for relog-dependent facts.
- In-combat writes need the recorded debug-only performance-§12 exemption (ruling F3). Both of these addons will need
  combat samples, so write it in from the start.
- Never instruct `clear` in a step the owner may repeat on a second character (memory, forever-probe lesson 2026-11-23).
- Any multi-line dump goes to the debug console, not chat (report-routing ruling, LibKa0s#79).

### 2.11 Smoke format

- Addon file: an Index with a Client column, a `## WoW Forever` theme, checks written
  `**FOREVER-n. <title> (<items>, <rulings>).** Client: WoW Forever. <steps> -> <expected>. Fail: <...>. Result:`.
- Include: listed and not out of date, fresh profile wears WoW Forever, one absence check per gated feature, two-word
  names, test mode, sim, probe session, "run every `both` check on Forever", a Retail presence check, one Retail
  regression check per Retail-affecting fix.
- Bundle `06_SMOKE_TESTS.md`: probe walk-through first, then per-addon tables `Id | Client | Steps | Expected | Status`,
  all `owed`. Agents never mark a pass.

### 2.12 Quirks and roster

- The quirks block is copied whole and never edited. Own section holds only what this addon met and does not repeat
  the block.
- File a finding under the client it was measured on. MultiMeters will be the **second repo** for CombatTrail's
  `C_DamageMeter` findings (forever-quirks-§5), so a probe here lets the next harvest promote them.
- Roster: two cells, `scripts/check-standard.sh`, no version bump, same landing.
- `symlinks.txt` already lists both Forever links (lines 32, 34). **U:** whether they exist on disk (not looked at).
  Probe: the owner checks the Forever AddOns list.

### 2.13 Plan mechanics

- Cross-repo bundle `CT-DOCS/<date>-MULTIMETERS_KICKCD_FOREVER_PORT/` with `00_DESIGN`, `06_SMOKE_TESTS`,
  `07_EXECUTION_RECORD`, `RESUME.md`, `checkpoints.tsv`, `inputs/`, `plan-data/{items.tsv,exceptions.tsv,resume-state.sh}`.
- `items.tsv`: `id milestone repo title deps`. Checkpoints: `milestone date evidence heads`.
- **Run-unique id prefix** (for example `FPMK-MM-01`). Bare ids collided with older history and with the next run
  (`LH-PORT/07`, "Item id collisions"; commit 5451141). Match only in `master..branch`.
- One branch name in four repos: MultiMeters, KickCD, WowAddonStandards, Ka0sAddonsCommonTasks.
- Finalize order: standard, addons, CommonTasks. The lead does pushes, merges and GitHub writes.
- MM and KC can build in parallel (separate repos), one item at a time inside each.

---

## 3. Owner rulings that already answer this port's questions

### 3.1 Collection-wide, binding

| Would-be question | Ruling | Source |
|---|---|---|
| One codebase or two, Classic too? | One, Retail + Forever, no Classic | 2026-11-07 `00_OWNER_CHECKS_AND_RULINGS.md` #1; clients-§1 |
| Hide, gray or remove a Retail-only feature? | Absent, never hidden. M+, Delves, group finder, warband, transmog, EJ named | `2026-11-07-WOW_FOREVER_PORT/01_DESIGN.md` §2; clients-§4 |
| Filter the Retail seed? | No. A list per client | same; clients-§5 |
| Drop Forever for either addon? | Only if the core is missing there. It is not for either | clients-§2 (2026-11-10) |
| Default skin on Forever? | WoW Forever; Retail Ka0s Default; library answers | `STEP5/W1_DEFAULT_SKIN_AND_FOREVER_NAMES.md` §1; skinning-§2 |
| A character's identity? | "First Surname", never split, never keyed on the first word | W1 §2; forever-quirks-§4 |
| Realm key? | The ruleset; two PvP realms sharing "PvP" is fine | `STEP5/W1_FOREVER_NAME_PROBE.md`, "The owner's calls" |
| Where do identity readers live? | LibKa0s Compat | same |
| Where does spec and role logic live? | LibKa0s Role | `QC-PORT` R3 |
| What tells tank from DPS? | Talents, player override, saved per character, spec API as fallback | `QC-PORT` R5 |
| Where do reports print? | Debug console, one chat pointer; help, acks, errors in chat | ruling 2026-11-08, LibKa0s#79 |
| Build everything for both clients from now on? | Yes | 2026-11-07 #5 |
| Which quirks file? | One per client; dual addon carries both | ruling 2026-11-10; forever-quirks-§1 |
| Ace3? | Pinned master ac3d1225, no shim, already vendored | `01_DESIGN.md` §2; LibKa0s#76 open |

### 3.2 Per-port rulings that are strong precedent (cite, then default to them)

| Would-be question | Precedent | Source | Carries here as |
|---|---|---|---|
| Probe shape? | Permanent verbs into SavedVariables, plus a `/run` sheet | LH R4; QC C4 | same |
| Probe writes in combat? | Debug-only exemption, documented | F3, `2026-11-22-LIBKA0S_101_CONTAINER_READER/inputs/OWNER_RULINGS_FOREVER_FOLLOWUPS.md` | same |
| A fix that also changes Retail? | Both clients, own commit, own test | LH R8 | same |
| Wait for probes before finishing? | Build on safe defaults; contradictions become follow-ups | LH R3 | build and push yes |
| Merge without probes? | R3 allowed it **for that run only** | LH R3 | **not carried**: this request says no merge without go-ahead |
| Truncated names? | Full-name tooltip whenever cut off, both clients | F2 | MultiMeters rows, KickCD labels |
| Derive Forever spell seeds from what? | Forever DB2; map by name, every rank | AM ruling 1 | KickCD |
| Who decides seed membership? | Claude decides and records; owner checks in game, no review sheet | AM ruling 2 | KickCD |
| A category with nothing on Forever? | Gate it off | AM ruling 4 | KickCD categories |
| Runes? | Excluded from the player pool | AM ruling 3 | default, but see question Q4 |
| Offline seeds unverified by logs? | Ship, with a follow-up issue | AM ruling 5 | KickCD |
| Content kinds on Forever? | Open world, dungeon, raid, battleground. No arena, M+, delve, scenario, housing | QC R1, C3 | MultiMeters visibility and content, KickCD visibility |
| Retail-only words? | A Forever player never sees them | DW-SPEC §2 anti-goals | both |
| Wowhead links? | `https://www.wowhead.com/forever/...` | LH R7 | any link in either |
| Account vs Warband words? | "Account" | LH R2 | only if either shows them |
| Always show an empty Forever-only row? | Case by case; LH's Account holder stays | F4 | no general rule |
| Secure send path on Forever? | Same path | QC R4 | MultiMeters export |
| DpsRace-style missing core? | Retail-only | QC R9 | does not apply |
| Version bump, tag, release? | No | LH R3 and every wave | same |
| Roster change bumps the standard? | No | STD-01, WS-FP01 | same |

### 3.3 From this request (relayed by the owner)

Ask up front, then decide. Resumable checkpointed plan. Branch with incremental commits. Push at milestones, no merge
without go-ahead. Delete the run's branches, stashes and worktrees after the merge.

### 3.4 Standing rulings a port must not disturb

- A sweep or migration never flips a recorded owner override or deviation row (AuraMaster ruling 2026-11-22, memory
  `auramaster-own-colors`; regressed once by SD-SK-AM 99b5b02, restored in v22).
- MultiMeters has many accepted skin deviations in `docs/ARCHITECTURE.md` `## Documented deviations` (the window
  chrome, hover .15, stripe .08). Leave them.
- An R-2 migration audit of 2026-11-23 reported MultiMeters' classless tooltip bar changing gray to blue and is
  **awaiting the owner's calls** (memory `r2-migration-audit-and-forever-probe`). Do not fix or re-migrate it here.
- RangeMaster and OutfitterReborn are in every sweep. Not relevant to a two-addon port, relevant if a re-vendor sweep
  is added.

---

## 4. Lessons from past runs

### 4.1 Taint and protected calls

| Lesson | Source | Here |
|---|---|---|
| Never open CharacterFrame from addon code on Forever; a Blizzard panel needs a hardware click on a secure button | OutfitterReborn OR-S8, 2026-11-09 | grep found no ShowUIPanel or CharacterFrame in either addon (V) |
| Registering `COMBAT_LOG_EVENT_UNFILTERED` raises `ADDON_ACTION_FORBIDDEN`, pcall does not catch it | `CB-Q`, build 70862 | neither registers it (V, grep) |
| Never write into, re-parent or `SetScript` Blizzard's frames | DW-SPEC §2 | KickCD must not touch the cast bars or Cooldown Manager |
| A probed event's lost edge is written in that client's quirks file | events-frames-taint.md:47 | both |

### 4.2 Secret values

| Lesson | Source | Here |
|---|---|---|
| The system is live on Forever; assume every Retail rule and record what is seen | forever-quirks-§2, §3 | both |
| `UnitStat` secret; `C_UnitAuras` may raise, so pcall | forever-quirks-§3 | any aura read |
| Meter totals secret at combat+5 s, plain by +2 s after | `CB-Q` | MultiMeters |
| Cast spell ids and castGUIDs of player and pet were plain in combat (build 70888) | `CB-Q` | player casts only; says nothing about a target's cast |
| Formatter objects refuse secrets; `AbbreviateNumbers`, `FloorToNearestString`, `RoundToNearestString`, `TruncateWhenZero`, `%d` accept | `CB-Q` | MultiMeters Format |
| Color curves cannot evaluate a secret | `CB-Q`, CombatTrail#7 closed | no curve workaround for the identity join |
| A secret boolean cannot be tested | client-quirks-§2 | KickCD `notInterruptible` |
| A secret cannot be a key, and is saved as nil | client-quirks-§2 | probes store `<secret>` |
| `SetTexture` takes a secret from tainted code (`AllowedWhenTainted`) | V, `FUI/API/SimpleTextureBaseAPIDocumentation.lua:604-606` | a secret spec icon can be drawn, not compared |

### 4.3 Meter behavior already measured on Forever by CombatTrail (`CB-Q`)

- `C_DamageMeter` ships whole, enums match Retail (70862).
- The pet folds into the owner's source, marked by `creatureName`, which is secret in combat (70888).
- EnemyDamageTaken has one row per enemy by creature id, no GUID, drill-down is one aggregate spell row. Session
  totals can disagree with the rows, so sum the rows. Group behavior unmeasured (CombatTrail#6).
- `amountPerSecond` was nil on the per-source table. **V:** that struct does not document the field on either
  client (`FUI/API/DamageMeterDocumentation.lua:183-193`), while the session's `combatSources` row does (`:205`). So
  this does not by itself break MultiMeters' rate columns.
- The spec API answers a class pseudo-spec with no icon. **I:** a meter `specIconID` on Forever is probably 0 or a
  class icon, and because it is secret the addon cannot test for 0, so "draw it" may draw a blank.

### 4.4 Two-word names

`UnitName`'s second value is the surname. One-value reads collide. `Ambiguate(short)` and chat senders give the pair.
Sites found (V, grep of the snapshots):

| Site | Problem |
|---|---|
| `MM/core/Compat.lua:770-775` `UnitName` | first name only; feeds Roster (`:234`), Sim (`:201`) |
| `MM/modules/Export.lua:626-631` `TargetName` | fallback gives first name, so a whisper can reach the wrong person |
| `MM/modules/Targets.lua:178-183`, `Row_NameCell.lua:366` | hyphen strip; safe for spaces, pin with a test |
| MM name column width, header band, tooltips, export text | sized for one word; the width calibration test fails on forever |
| `KC/core/Compat.lua:531`, `modules/Castbar_Debug.lua:70` | debug text shows first name |
| KC cast bar and unit labels | width; enemy players show the pair |

Whether a surname can hold a hyphen is **U** (`LH-PORT/07`, Smaller questions). Probe: record `GetUnitName(unit, true)`
for group members.

### 4.5 Migrations and saved data

- "No migration, a Forever DB is born fresh" held for LootHistory and BankLedger (`LH-PORT/00_DESIGN.md`, Identity).
  **It does not automatically hold for KickCD.** A port-pending addon loads out of date on Forever by design
  (clients-§8), and `Database:BuildSpells` seeds once and is idempotent on a populated profile (`KC/docs/schema.md`,
  "Spell list lifecycle"). Any Forever profile created before the port holds Retail lists and will never pick up
  Forever seeds. **U:** whether such profiles exist. Probe: read `KickCDDB.profiles.*.spells` and `schemaVersion`
  in the Forever SavedVariables, read-only, with the lead's path authority.
- Retail stored keys never move. An identity change is regional-names only (D6).
- The game loads the working tree live. AuraMaster's v21 migration reached the owner's SavedVariables 22 minutes
  before its commit. **Build any migration in a scratch clone, back up SavedVariables, switch the checkout only when green.**
- AceDB strips defaults per channel, so a changed color default shifts a partly picked color (R-2 audit).
- Per-install: profiles do not travel between clients (AuraMaster known limitations).

### 4.6 Skin defaults

- Flipping a default hides the Forever effect: "nothing changes under Ka0s Default" was false on Forever
  (AuraMaster blue bars went brown). State the visible effect on **each client's** default skin.
- R-2 (2026-11-20): an addon's own texture, font or color default follows the skin, except recorded overrides.
- New Forever-only defaults must follow R-2 too.

### 4.7 Process

| Lesson | Source |
|---|---|
| Item ids collide across bundles; prefix and scope the grep | `LH-PORT/07` |
| Another session can release the standard mid-run; fetch before finalize | standard-version-collisions |
| `cd repo \|\| exit 1` before destructive git | same |
| Subagent pushes and GitHub writes are refused; the lead does them | subagent-push-refused |
| A mid-run user message hijacks agents; guard every prompt, then check the journal | workflow-midtask-messages |
| A re-vendored facade needs every new member or parity goes red | `LK/docs/releasing.md:253-255` |
| Python edits must keep CRLF; the eol test catches it | OR smoke round |
| The prose gate rejects British spellings | `LH-PORT/07` |
| The design can own a ruling no plan row carries (OR's ammo slot was never built) | OR build 2026-11-09 |
| Sim and probe assumptions were wrong in game (48-slot tab, sender full name, TTLs) | LH+BL probe 2026-11-23 |
| Every review found real defects (7/9, 5/5) | `LH-PORT/07` |

---

## 5. What the two-week-old classification got right and wrong

| Classification claim (`STEP5/00_CLASSIFICATION.md`) | Re-check |
|---|---|
| `C_DamageMeter` and CooldownViewer load on Forever | V, both TOCs `standard, camelot` |
| "About 50 specIconID reads, each needs a guard" | The secret is real (V). The fix is not 50 guards: compares are already guarded (`Aggregator_Identity:119`, `Export.CsvField`). The cost is the identity key, the icon, the CSV column and diagnostics |
| "Delve content gated off" | Plus arena, M+, scenario per QC R1 |
| "Chat reports need a check" | Plus the formatter refusal and the whisper name, both unknown then |
| "KickCD spec ids differ (Warrior 1491)" | V, `AM-SPEC` §2 |
| "Every addon is clean in the missing-globals scan" | Still PASS, and **misleading**: a guarded call is never a finding (`LK/testkit/client_globals.lua` header, KNOWN FALSE NEGATIVES), and the 2026-10-21 Forever set lists deprecation fallbacks Forever does not load |
| Group 4 = medium | QuickComms is done. MultiMeters is nearer high because of identity and formatting; KickCD's effort is mostly data |

Other deprecation-backed globals these addons read (V, scan of `FUI/Blizzard_Deprecated*`):

| Global | Site | Forever |
|---|---|---|
| `GetNumSpecializationsForClassID` | KC Util:273,283; Spells_Header:88,95 | fallback addon not loaded (gate `classic, standard`) |
| `IsPlayerSpell`, `IsSpellKnown` | KC Compat:210-213 | ungated addon, only under CVar `loadDeprecationFallbacks`. **U:** the CVar's value. Probe `/dump IsPlayerSpell, IsSpellKnown, GetCVarBool("loadDeprecationFallbacks")`. If nil, the known-spell filter needs `C_SpellBook` |
| `GetSpellCharges`, `IsUsableSpell` | KC Compat:185,231 | fallbacks behind namespaced rungs or guards; confirm the first rung |
| `GetDeathRecapLink`, `SendChatMessage` | MM Compat:366,895 | ungated fallbacks; `C_ChatInfo` is the first rung |
| `GetSpecializationRole` | MM Compat:805 | **I** present: Forever's own `Blizzard_SharedXML/UnitUtil.lua:117` calls it. Its answer is class-wide, so use Role |

---

## 6. LibKa0s

### 6.1 Does either addon need v1.110.0?

**Not functionally.** V: `git diff v1.109.0 v1.110.0 -- LibKa0s testkit` is four files: `Compat.lua` (six
container and bank members, minor 6), and kit revision 60 (`framework.lua`, `mock_client.lua`, `README.md`) with
BagIndex and C_Bank mocks. Neither addon reads containers or the bank. Every Forever surface this port needs is in
v1.109.0: client helpers (v1.92), names and DefaultSkin (v1.94), Role (v1.95), samples (Sim minor 3).

**Recommended anyway, first item, alone.** It is the newest tag, releasing.md step 8 calls re-vendoring part of a
release, and the K101 run deferred these addons only "until the next sweep" (call 8). Measured cost: exactly one
failing case per addon, the Compat stub parity, fixed by routing or ignoring the six names, plus the kit 59 to 60
pin and the provenance line. No client behavior changes.

### 6.2 Gaps this port hits

| Gap | Evidence | Port's handling | Library follow-up |
|---|---|---|---|
| G1 Kit Forever profile does not remove `GetNumSpecializationsForClassID` | `mock_client.lua:52-53`; fallback TOC gate | addon mock removes it | add to `absent` |
| G2 Globals scan passes guarded-but-absent calls and lists unloaded fallbacks as present | scanner header; scan PASS here | manual deprecation scan (section 5) | generated "fallback not loaded on camelot" set; extends LibKa0s#93 and #44 |
| G3 Kit has no Forever secret-field model | `specIconID` | addon mock | optional kit helper |
| G4 Compat has no class-spec enumeration | Compat members list | use `Role.SpecsForClass` (namespaced rung first, `Role.lua` `numSpecs`). It returns no icon, and KickCD's header needs one | optional `icon` field, additive; or a local CompatClient shim |
| G5 No public "top talent tree" reader | `talentRole` is local; DropWatcher and CombatTrail each wrote one | shim over `Role.Groups()` if needed | third consumer would justify promotion |
| G6 No secret-tolerant number format rung | CombatTrail `Format.Rate` is addon-local | copy the pattern into `MM/modules/Format.lua` | second consumer; consider Core |
| G7 No wago seed helper | LibKa0s#91 closed to dev-copilot#1 | extend KickCD's own `tools/seeds/seeds.py` | dev-copilot#1 |
| G8 Role seed unconfirmed beyond Hunter | `Role.lua:80-82` | probe logs `Groups()` per class played | fix only on evidence |
| G9 Container reader | not used | none | none |

None blocks the port, and none requires a LibKa0s release in this run.

---

## 7. Probes this port needs (exact, all on Forever unless noted)

| P | Fact | Probe |
|---|---|---|
| P1 | `specIconID` secret out of combat too, and what it draws | per source: `issecretvalue(src.specIconID)` in and out of combat; `SetTexture` it on a hidden texture and screenshot |
| P2 | Identity inputs in a group | per source in combat: secrecy of `sourceGUID`, `name`, `classFilename`, `isLocalPlayer`, `sourceCreatureID`; party with two players of one class |
| P3 | Formatter refusal on 71037, both clients | in combat: pcall `FormatNumber` on both objects, `AbbreviateNumbers` and `FloorToNearestString` on a secret `amountPerSecond`; store ok and `<secret>` |
| P4 | Rate on the session row in combat | `type` and secrecy of `combatSources[i].amountPerSecond` |
| P5 | Spec globals | `/dump GetNumSpecializationsForClassID, GetNumClasses, GetClassInfo, GetSpecializationInfoForClassID, GetSpecializationRole, C_SpecializationInfo.GetNumSpecializationsForClassID` |
| P6 | Known-spell readers | the `/dump` in section 5, plus `C_SpellBook.IsSpellKnown` on two ranks of one kick |
| P7 | Cooldown secrecy | in combat after a kick: secrecy of `C_Spell.GetSpellCooldown(id)` fields, `GetSpellCharges` |
| P8 | `notInterruptible` | on a mob cast and a player cast: `select(8, UnitCastingInfo("target"))` secrecy; do the INTERRUPTIBLE events fire |
| P9 | Rank cooldown sharing | cast rank N, read rank 1's cooldown |
| P10 | CooldownViewer data per class | `C_CooldownViewer.GetCooldownViewerCategorySet` sizes per category |
| P11 | Talent order | `Role.Groups()` on each class available |
| P12 | Existing Forever SV | lead reads both addons' Forever SavedVariables before any migration |
| P13 | Event availability | `/mm diagnostics`, `/kcd diagnostics`, and each addon's `debug events` if present |
| P14 | CurseForge dual tagging | unproven for `120105, 16001`; settled by the first alpha or release, the owner's call |

---

## 8. Questions only the owner can answer

- **Q1 MultiMeters, in-combat grid on Forever.** The same-class collision is permanent in combat. Accept blank
  secondary cells for those rows until combat ends (Retail's existing honesty rule, recommended), or show only the sort
  column in combat on Forever?
- **Q2 MultiMeters icon on Forever.** Class icon for everyone (recommended), talent-tree icon for you only, or draw
  the meter's secret icon blind?
- **Q3 MultiMeters numbers on Forever in combat.** If P3 confirms, whole unabbreviated numbers (`30190`, CombatTrail's
  choice) or `AbbreviateNumbers` with a possible decimal tail?
- **Q4 KickCD list key on Forever.** One list per class (the client's one spec, recommended) or one per talent tree?
  And do rune-granted abilities stay excluded, as AuraMaster ruling 3 did for auras?
- **Q5 KickCD ranks.** One row per ability that follows your highest known rank (recommended), or one row per rank id?
- **Q6 Existing Forever profiles.** If P12 finds Retail-seeded lists, re-seed them once (edits lost, after a backup)
  or add Forever lists beside them and leave the rest?

Not asked, because already answered: skin default, absent vs hidden, filtered seeds, names and realm key, probe
shape, Retail-affecting fixes, version bumps, merge gate, seed decision-maker, content kinds.

---

## 9. What was not checked

- The game install, its SavedVariables and the symlinks (outside this study's paths).
- Vendor byte-identity against the tag (skipped in scratch copies).
- The other MultiMeters and KickCD feature surfaces in depth (this is the patterns report; the code reports own them).
- Forever DB2 contents for interrupts. No download was made.
- Anything in game. Every behavior fact above comes from UI source at 71037 or from a dated probe in a repo at 70790,
  70862, 70888 or 70938. The 70xxx measurements are older than the pinned source and should be re-probed.
