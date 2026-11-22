# MultiMeters + KickCD to Retail + WoW Forever: synthesis

2026-11-23. Read-only study. No client was run. Design and items assume the recommended answer to each question in section 6.

| Pin | Value |
|---|---|
| MultiMeters | master bf67258, 1.2.0, LibKa0s v1.109.0, schema 28 |
| KickCD | master 333cd49, 1.5.0, LibKa0s v1.109.0, schema 10 |
| Forever | 1.60.1.71037, interface 16001, UI 734f065 |
| Retail | 12.1.5.70961, interface 120105, UI ab5cb85 |

**How to read the citations.** Reports in this directory: `MM` = mm-code.md, `MA` = forever-meter-api.md, `KC` = kc-code.md, `CA` = forever-cooldown-api.md, `ID` = forever-interrupt-data.md, `PT` = patterns.md, `FC` = factcheck.md (FC wins where they disagree; `FC n` is claim n, `FC A-F` its findings). `SYN` = checked again for this synthesis, with the file named. `D:` = Forever `Interface/AddOns/Blizzard_APIDocumentationGenerated/<Name>Documentation.lua`. Addon paths are in the pinned snapshots.

**Status.** VERIFIED = the named source at the named build says so. For API docs that means documented, not seen in game. INFERRED = reasoning given. UNKNOWN = probe in section 5.

## 0. Read first

1. **Both ports are feasible, and neither core is absent.** A TOC-only change would ship a MultiMeters that can draw one player's healing on another's row (VERIFIED by simulation, MM 1.2) and a KickCD with an empty grid for every character (VERIFIED by simulation, KC B1).
2. **Start blocker: the MultiMeters base branch does not exist here.** VERIFIED (SYN, `git branch -a` and `for-each-ref` over the local checkouts, 2026-11-23): no `fix/2026-11-23-r2-restore-probe-fixes` in MultiMeters or any sibling, locally or in remote-tracking refs, and no stash in MultiMeters. Nothing was fetched. U1 has the default: KickCD starts, MultiMeters waits for that branch. Do not stack on master: the branch reverts master's schema v28 and `swatchesFollow` defaults.
3. **The green suites prove little.** VERIFIED: all critical defects pass the Forever kit profile today (MM 7, KC 8, CA 13). Forever mocks come before the fixes.
4. **The formatter fault is probably live on Retail.** INFERRED: the refusing doc line is byte-identical (FC 4), and CombatTrail recorded Retail live figures on 2026-11-13 that no client formatter served (SYN, CombatTrail master `docs/midnight-quirks.md`, "On Retail the live figures lose their decimals"). The refusal itself was never probed on Retail.
5. **The Avoidable warning is not Forever evidence.** VERIFIED (SYN): Retail carries the same `DAMAGE_METER_AVOIDABLE_DAMAGE_NOT_ACTIVE` line, `Blizzard_DamageMeter/DamageMeterSessionWindow.lua:713` in both trees.
6. **No Forever profiles to repair today.** VERIFIED for this install (FC 72). Look again at the flip, because a running session writes at logout.

## 1. Feature tables

### 1.1 MultiMeters

| Feature | Forever | Evidence | Work |
|---|---|---|---|
| Meter functions, events, enums | port | VERIFIED `D:DamageMeter`, only lines 203 and 242 differ (FC 1, 25) | none |
| Values secret in combat, plain after | port | VERIFIED 70888 for a solo Hunter's own rows; INFERRED beyond (FC 27) | none |
| Mid-pull join across columns | adapt | VERIFIED mislabel by simulation (MM 1.2); `specIconID` secret in combat INFERRED (FC 2, 26) | class key with a roster-seeded collision rule |
| Number text | adapt | VERIFIED refusal 70888 and `D:NumericFormatterAPI:11-14` (FC 4); effect on every cell INFERRED (FC 28) | secret path that skips the formatter |
| Rates | port | local row INFERRED present (FC D); ally UNKNOWN | U5 |
| Names in grid, tooltip, export, Targets | adapt | VERIFIED 70790 (FC 6, 33; MM 1.4) | whole name through `UnitCharacterName` |
| Name column | adapt | VERIFIED 25 characters possible, cap 15 (`defaults/Profile.lua:435`) | Q2 |
| Row icon | adapt | meter icon content UNKNOWN (FC 3); class atlas coordinates VERIFIED (MM 4.4) | class icon for every row |
| CSV `spec` column | absent | VERIFIED a secret exports as blank (`modules/Export.lua:403`, MM 1.1) | per-client column list |
| Role fallback | adapt | VERIFIED class spec is role 2 for all nine in DB2; runtime Hunter only (FC 37) | `LibKa0s-Role-1.0` `Resolve` on Forever |
| Pet merge | port | folding VERIFIED for Hunter pets only (FC 9) | keep the setting; name the pet's spell rows |
| Targets | port, probe | per-attacker rows UNKNOWN (FC 8) | the name fix makes the join possible |
| Death recap | port, probe | existence VERIFIED, working INFERRED (FC 11) | none |
| Avoidable Damage column | port | content UNKNOWN (FC 12); warning on both clients (SYN) | Q4 |
| Damage, Healing, Absorbs, Interrupts, Dispels, Deaths, Taken | port | VERIFIED same enum (MM 3) | none |
| Built-in meter notice | port | collection with the CVar at 0 INFERRED (FC 32) | never call the switch a requirement; never write the CVar |
| Visibility: open world, dungeon, raid, battleground | port | VERIFIED DB2 Map (FC 10) | none |
| Visibility: arena, scenario, Delves, housing | absent | VERIFIED no arena or scenario maps, housing TOCs `standard` (FC 10); QuickComms ruling R1 | gate rows, probes, vetoes |
| Visibility: skyriding, pet battles | absent | INFERRED no such content in classic-era play. The APIs and pet battle UI do load on camelot (VERIFIED SYN, `Blizzard_PetBattleUI` TOC), so they cannot decide it | gate rows and four events; U12 |
| Visibility: vehicles, flight paths, mounted, dead, solo, combat | port | VERIFIED APIs and data (MM 3) | none |
| Mount-like forms | adapt | VERIFIED DB2 forms 3 and 4 (MM 3) | per-client list |
| Delve companion seed | absent | follows Delves | empty by decision |
| Chat export | adapt | sender doc VERIFIED; dungeon lockdown UNKNOWN (FC 36) | names; U11 |
| Secret system line in whisper export | adapt | INFERRED raise on both clients (MM 4.6) | `CanAccess` guard |
| Test mode, sim, samples | adapt | VERIFIED 25 of 46 sim ids absent (MM 5) | Forever lists |
| Default skin | port | VERIFIED already per client (MM 6) | fixture pins only |

### 1.2 KickCD

| Feature | Forever | Evidence | Work |
|---|---|---|---|
| Cooldown, usable, charges, duration objects, curves | port | VERIFIED docs identical (FC 14, 40) | none |
| Cast bar on target and focus | port, probe | VERIFIED docs and sinks (FC 20, 42); real casts UNKNOWN (FC 21) | nil guard, U14 |
| Interruptible colors and masks | port, guard | nilable flag into non-nil sinks VERIFIED (FC 20); fidelity UNKNOWN (FC 43) | a non-secret nil reads false, secret test first |
| Focus | port | frame, binding, event VERIFIED; `/focus` INFERRED (FC 22, 44) | none |
| Spec identity | adapt | VERIFIED nine ids (FC 13); runtime Hunter only (FC 37) | Forever table; fall back to the class's id |
| Default lists | adapt | VERIFIED 56 of 78 Retail ids absent, survivors include traps (KC 2.2; FC 55) | Forever seed run |
| Ranks | adapt | VERIFIED one id per rank (FC 17); known behavior UNKNOWN (FC 18) | rank table and one resolver |
| Druid Feral Charge | adapt | override per form VERIFIED in data, applying INFERRED (FC A) | store 1238122; interrupt in bear only |
| Known-spell check | adapt | VERIFIED deprecation shims only (FC 15) | `C_SpellBook` in Compat |
| Spec names and counts | adapt | bare global absent INFERRED, member VERIFIED (FC 16) | namespaced member |
| Class enumeration | adapt | loop behavior UNKNOWN (FC 24, 48) | Forever list from the seed's nine classes |
| Cooldown Manager add gate | absent | VERIFIED no Spell Lock; linked ranks are present but KickCD reads only `info.spellID` (FC B, 19; `core/SpellInput.lua:204-205`) | Q8; gate Retail-only by declaration |
| Racials | adapt | VERIFIED War Stomp 20549 alone (ID 6) | per-client table |
| Ready glow | port | GCD on most kicks VERIFIED in data; blink INFERRED (FC 23) | Q7 |
| GCD swipe suppression | port | VERIFIED thresholds hold: GCD at most 1.5 s, shortest interrupt 6 s (CA 2) | none |
| GCD mark in the debug log | adapt | 61304 absent from data VERIFIED (FC 60) | say unknown on Forever; log only |
| Charges badge | port | VERIFIED no seeded kick has charges (CA 2) | none |
| Spells page, slash wording | adapt | one spec per class | "Class", `[CLASS]` |
| Empower routes | port | events documented; no emitter expected (INFERRED) | harmless |
| Visibility modes, layout, drag, unit label | port | no client-specific surface (KC 3) | none |
| Sim | adapt | VERIFIED absent ids (KC 5) | Forever seeds and story |
| Sound, chat announce, key bindings | n/a | VERIFIED none exist (KC 3) | none |
| Default skin | port | VERIFIED already per client (KC 7) | fixture pins only |

Forever interrupts, all checked against DB2 71037 (FC "Spell ids"). Each is data, not seen in game.

| Class | Ability and ids | Cooldown | Lockout |
|---|---|---|---|
| Warrior | Pummel 6552, 6554; Shield Bash 72, 1671, 1672 (shared category) | 10 s; 12 s | 4 s; 6 s |
| Rogue | Kick 1766-1769 (not the clones 1775, 3467) | 10 s | 5 s |
| Mage | Counterspell 2139 | 30 s | 10 s |
| Shaman | Earth Shock 8042, 8044, 8045, 8046, 10412, 10413, 10414 | 6 s, shared with shocks | 2 s |
| Priest | Silence 15487 (talent) | 45 s, its own | 3 s UNKNOWN |
| Druid | Feral Charge 1238122, 16979 in bear (talent) | 15 s | 4 s |
| Warlock | Spell Lock 19244, 19647 (Felhunter) | 30 s | 6 s, 8 s |
| Paladin, Hunter | none; a control spell leads (INFERRED no reachable interrupt, FC 54) | | |

## 2. Approaches

### 2.1 MultiMeters

| Approach | For | Against |
|---|---|---|
| A. Minimal: TOC, gates, samples, one guard per secret read | smallest diff | keeps the mislabel, the wrong number text and the lost surnames |
| **B. Shared engine with a few per-client choices** (identity key, icon, columns, visibility lists, name defaults) | fixes all three defects, reuses the reader and the honesty rule, keeps Retail's layout | many blank cells mid-pull with repeated classes |
| C. A separate Forever combat view (sort column only, full grid after combat) | uniform, with no correlation logic | a second presentation to test and document; discards cells that are safe |

**Recommend B.** It is the smallest approach that is honest. Q1 can still pick C's presentation without changing the rest.

### 2.2 KickCD

| Approach | For | Against |
|---|---|---|
| A. Derive lists at runtime from the Cooldown Manager | no seed to maintain | no pet spells, no "interrupts" field, live class only; breaks clients-5 and the validate-seeds contract |
| **B. A frozen Forever seed, one list per class, one row per rank family, one resolver** | fits the stored shape and the spec id the client reports; replayable | a seed run to maintain; hybrids share one order |
| C. B, keyed by talent tree | a tailored order per tree | a new stored key, a rule for hybrids, unconfirmed tree order beyond Hunter (FC 68) |

**Recommend B** (Q5 can pick C).

### 2.3 Cross-cutting

| Choice | Options | Recommendation |
|---|---|---|
| LibKa0s | stay on v1.109.0; re-vendor v1.110.0; cut a release for the class-loop bug | stay. v1.110.0 adds nothing these addons use (FC 71) and does not fix the loop (FC E). Fix locally, file the issue |
| Working place | live checkouts; linked worktrees outside the loaded folders | worktrees, because the client loads the checkouts live. Switch a checkout only at a green checkpoint, for smoke |
| Sequencing | serial; parallel by repo | parallel by repo, one item at a time inside each |

## 3. Draft design

### 3.1 Scope and rules

- Branch `feat/2026-11-23-multimeters-kickcd-forever-port` in MultiMeters, KickCD, WowAddonStandards and Ka0sAddonsCommonTasks. **MultiMeters branches from `fix/2026-11-23-r2-restore-probe-fixes`**, the others from master.
- One codebase, no Classic. No version bump, tag or release. Push at milestones. **No merge without the owner's go-ahead** (this request overrides the last port's R3 merge ruling).
- A Retail-visible change is its own commit with its own test, and only those Q3 accepts.
- Feature presence is declared, never detected (clients-4). Client reads only through `core/CompatClient.lua`, routed from LibKa0s-Compat (clients-3).
- No SavedVariables migration and no schema bump in either addon. Documented owner skin overrides and the fix branch's restores are not touched.

### 3.2 Shared shape

- `core/CompatClient.lua`: `IsForever`, `IsRetail`, `ClientKey`, `ForClient`, `RegionalNames`, `UnitCharacterName`. It loads before SimSetup, and each member is wrapped or declared PURE.
- A host mock file per addon for what the kit does not model: secret `specIconID`, a formatter that raises on secrets, two-word names, class specs at their real ids, ranked known sets, `C_SpellBook`, the absent bare spec global, no 61304.
- Both kit profiles green at every commit. Tests of Ka0s Default pixels select that skin by name.
- Probe verbs under `/mm debug probe` and `/kcd debug probe` (`start|stop|status|clear`), writing a capped `db.global.probe` stamped with client and build, secrets stored as `<secret>`, with the recorded debug-only exemption for in-combat writes. A `/run` sheet in `docs/forever-probes.md`. Builds do not wait for results (precedent R3, R4).
- The TOC `## Interface: 120105, 16001` lands last, with README, gates, quirks, per-client table and shape test.

### 3.3 MultiMeters

**Identity.** A per-client constant says whether identity uses spec. On Forever the key is class plus `isLocalPlayer`, and before any cell is written a key is ambiguous when:
- the roster holds two or more non-local players of that class (for Overall, remembered members count too);
- the roster holds no player of that class;
- the source has no class.

The local player keeps their own key. An ambiguous key keeps the sort column and blanks the rest, and the header note says "class" instead of "class and spec". A non-group player of the same class remains a residual risk (U8). Retail's key is unchanged. Its narrower form of the same hole is filed as an issue, not fixed here.

**Numbers.** For a secret, do not call `FormatNumber`. Use `AbbreviateNumbers(v, { config = cfg })`, the config built once per mode and trusted only if it renders plain test values exactly (FC F: do not copy CombatTrail's call). If the config is refused:
- Forever: totals through `AbbreviateNumbers`, rates and Full mode through `C_StringUtil.FloorToNearestString`, so no decimal tail;
- Retail: today's path, so a failed probe cannot worsen seven-digit rates.

**Names.** Display identity comes from `UnitCharacterName` in roster, sim and export. The first-hyphen strip is skipped on regional names. Joins stay by GUID. The stored roster name corrects itself on the next scan. Width follows Q2 through the Forever window template, so saved windows are not rewritten.

**Absent on Forever.** Arena, scenario, Delves, housing, skyriding and pet battle visibility rows (with probes, vetoes and events), the companion seed, the CSV spec column. Filter the schema array before its path index is built, so `get`, `set` and reset cannot reach an absent row (MM 3).

**Other.** Class icon on Forever. `Role.Resolve` on Forever, Retail's ladder unchanged. Pet spell rows append a plain creature name. Forever samples: nine classes, two-word names, classic magnitudes, 40-player raid, Forever zones and spells. A 40-player perf scenario.

**File caps.** Window_Header 1463, Schema_Compose 1386, Aggregator 1343: new logic goes in Aggregator_Identity, CompatClient and new test and mock files.

### 3.4 KickCD

**Seeds.** `defaults/Spells_Forever.lua` picked once by `ClientKey()`, keyed by 1482 and 1484-1491. The Retail list stays byte-identical (test). A `forever` flavor of `tools/seeds/seeds.py` pins product `wowf` 71037, derives reach from SkillLineAbility (method other than 3), trait trees and pet lines, reads rulings as data and freezes a bundle. Runes, Rebuke 425609, Skull Bash 410176 and the same-name clones are excluded with reasons.

**Ranks.** A stored row is the family's rank-1 id. `defaults/SpellRanks_Forever.lua` lists the ranks, and `NS.ResolveSpell(id)` answers the highest rank known to the player or pet. Cooldowns, icons, dedupe, usable, tooltip, sim, settings and diagnostics all use it. Adding any rank stores the family id. No name-only derivation (FC 17, 70). Re-resolve on `SPELLS_CHANGED`, talent, level and pet events.

**Feral Charge.** Resolve the override of 1238122 before drawing. When it is 414924 (cat) the slot stays and is drawn not ready, with no glow, because the leap does not interrupt.

**Availability, both clients.** `C_SpellBook.IsSpellKnown(id, Player)`, then `IsSpellInSpellBook(id, Player, false)`, then `(id, Pet, false)`: exactly what the shims call (VERIFIED SYN, `Blizzard_DeprecatedSpellBook/Deprecated_SpellBook.lua`).

**Spec.** An id of 0 or less is nil. On Forever fall back to the class's seeded id. Classes and their names come from the per-client table, not from `1..GetNumClasses()` or `Role.SpecsForClass` (FC E). Retail tokens such as `ARMS` are refused on Forever.

**Profiles.** Forever only: add a class list whose key is absent. Never re-seed a key that exists, never delete Retail pairs. Count customized lists over the running client's pairs.

**Adding spells.** Per Q8. The Cooldown Manager gate, its tag, invalidator, diagnostics section and strings are Retail-only.

**Sim.** Forever party, spells and labels. No charge steps in the boss story. Only Counterspell and bear Feral Charge are off the GCD.

### 3.5 Lead's calls (not asked)

| # | Call | Basis |
|---|---|---|
| D1 | Absent, not hidden; separate seed lists; Forever skin by default | clients-4, clients-5, skinning-2 |
| D2 | Whole two-word names; never keyed on the first word | forever-quirks-4 |
| D3 | Class icon for every row on Forever | the secret cannot be tested for blank; a tree icon is a new feature |
| D4 | Number fallback as in 3.3 | no decimal tail, no Retail regression |
| D5 | No built-in meter switch, prompt or CVar write | FC 32 |
| D6 | Skyriding and pet battles absent on Forever | clients-4; content absence INFERRED, U12 |
| D7 | One row per ability, following the highest known rank | clients-10 wants every rank carried; a row per id would draw seven Earth Shocks |
| D8 | Runes and unreachable rune spells excluded | AuraMaster ruling 3; FC 54 |
| D9 | Existing Forever profiles: add absent keys only | none exist (FC 72); nothing to lose |
| D10 | Probe verbs, safe defaults, contradictions become follow-ups | last port R3, R4 |
| D11 | No re-vendor, no LibKa0s change; issue text for the class loop (also in ConsumableMaster `core/SpecHelper.lua:55`) | outside this request; lead files it |
| D12 | Seed membership beyond Q6 is decided and recorded by Claude | AuraMaster ruling 2; KickCD `docs/validate-seeds.md` |

Reader questions and where they went: same-class grid Q1; name cap Q2; Retail fixes and the formatter Q3; Avoidable Q4; per class or tree and Warrior primary Q5; list width Q6; glow Q7; add gate Q8; skyriding D6; meter switch D5; icon D3; formatter fallback D4; ranks D7; runes D8; old profiles D9.

## 4. Checkpointed items

Bundle: `Ka0sAddonsCommonTasks/docs/2026-11-23-MULTIMETERS_KICKCD_FOREVER_PORT/` (`00_DESIGN`, `06_SMOKE_TESTS`, `07_EXECUTION_RECORD`, `RESUME.md`, `checkpoints.tsv`, `inputs/`, `plan-data/`).

Done = a commit subject starting `<ID>: ` in the item's repo, or a row in `exceptions.tsv`. The prefix `MKF-` had no hits in the four repos' histories (SYN). `resume-state.sh` searches `<base>..<branch>` only, with the base being the fix branch for MultiMeters and master for the rest, then master after merge.

Effort: S under half a session, M about one, L more than one.

```
id	milestone	repo	title	deps	effort
MKF-CT-00	M0	Ka0sAddonsCommonTasks	Plan bundle: research, rulings, design, items, resume state	-	S
MKF-MM-00	M1	MultiMeters	Branch from fix/2026-11-23-r2-restore-probe-fixes; record base sha and both-profile baseline (exceptions row)	MKF-CT-00	S
MKF-MM-01	M1	MultiMeters	CompatClient; Sim PURE list; static client-read test	MKF-MM-00	S
MKF-MM-02	M1	MultiMeters	Forever mock; Ka0s Default fixtures pin their skin; both profiles green	MKF-MM-01	M
MKF-MM-03	M1	MultiMeters	Whole names: roster, sim, export, Targets join, realm strip	MKF-MM-02	M
MKF-MM-04	M1	MultiMeters	Name cap and window template on Forever (Q2); descriptions	MKF-MM-03	S
MKF-MM-05	M1	MultiMeters	Identity on Forever: class key, roster-seeded ambiguity, header note (Q1)	MKF-MM-03	L
MKF-MM-06	M1	MultiMeters	Class icon, no CSV spec column, diagnostics wording on Forever	MKF-MM-05	S
MKF-MM-07	M1	MultiMeters	Secret number text (Q3; own commit and test)	MKF-MM-02	M
MKF-MM-08	M1	MultiMeters	Secret system-line guard (Q3; own commit and test)	MKF-MM-02	S
MKF-MM-09	M1	MultiMeters	Role through LibKa0s Role on Forever	MKF-MM-02	S
MKF-MM-10	M1	MultiMeters	Per-client visibility rows, vetoes, events, forms, companion seed; present and absent tests	MKF-MM-02	M
MKF-MM-11	M1	MultiMeters	Avoidable default (Q4); exceptions row if unchanged	MKF-MM-04	S
MKF-MM-12	M1	MultiMeters	Pet spell rows name the creature when plain	MKF-MM-02	S
MKF-MM-13	M1	MultiMeters	Test mode, sim and samples per client	MKF-MM-06	M
MKF-MM-14	M1	MultiMeters	40-player perf scenario	MKF-MM-05	S
MKF-MM-15	M1	MultiMeters	Probe verbs and docs/forever-probes.md	MKF-MM-07	M
MKF-MM-16	M1	MultiMeters	Dual-client shape: TOC, README, gates, docs, quirks, table, shape test, test-cases	MKF-MM-04,MKF-MM-08,MKF-MM-09,MKF-MM-10,MKF-MM-11,MKF-MM-12,MKF-MM-13,MKF-MM-14,MKF-MM-15	M
MKF-MM-17	M1	MultiMeters	Smoke: WoW Forever section, absence and Retail regression checks	MKF-MM-16	S
MKF-KC-01	M2	KickCD	CompatClient; Sim PURE list; static client-read test	MKF-CT-00	S
MKF-KC-02	M2	KickCD	Forever mock world; fixture pins; sample fallback copy; both profiles green	MKF-KC-01	M
MKF-KC-03	M2	KickCD	Availability through C_SpellBook (Q3; own commit and test)	MKF-KC-02	S
MKF-KC-04	M2	KickCD	Namespaced spec count and spec id 0 (Q3; own commit and test)	MKF-KC-02	S
MKF-KC-05	M2	KickCD	Nil notInterruptible guard (Q3; own commit and test)	MKF-KC-02	S
MKF-KC-06	M2	KickCD	Secret-safe debug header and whole names (Q3; own commit and test)	MKF-KC-02	S
MKF-KC-07	M2	KickCD	Seed tool forever flavor, contract section, rulings, frozen 71037 bundle	MKF-KC-02	L
MKF-KC-08	M2	KickCD	Forever lists, spec table, classes, racials (Q5, Q6); Retail list unchanged test	MKF-KC-04,MKF-KC-07	M
MKF-KC-09	M2	KickCD	Rank table and resolver through every consumer; canonical add	MKF-KC-03,MKF-KC-08	L
MKF-KC-10	M2	KickCD	Feral Charge override per form	MKF-KC-09	S
MKF-KC-11	M2	KickCD	Absent-key seeding and customized count per client	MKF-KC-08	S
MKF-KC-12	M2	KickCD	Cooldown Manager gate Retail-only; Forever admission (Q8)	MKF-KC-09	M
MKF-KC-13	M2	KickCD	Spells page and slash wording per client; validate class and spec	MKF-KC-08,MKF-KC-12	M
MKF-KC-14	M2	KickCD	Glow rule (Q7); exceptions row if unchanged	MKF-KC-09	S
MKF-KC-15	M2	KickCD	Sim party, casts, story, off-GCD rule per client	MKF-KC-09	M
MKF-KC-16	M2	KickCD	Probe verbs, GCD log mark, docs/forever-probes.md	MKF-KC-09	M
MKF-KC-17	M2	KickCD	Dual-client shape: TOC, README, gates, docs, quirks, table, shape test, test-cases	MKF-KC-05,MKF-KC-06,MKF-KC-10,MKF-KC-11,MKF-KC-13,MKF-KC-14,MKF-KC-15,MKF-KC-16	M
MKF-KC-18	M2	KickCD	Smoke: WoW Forever section, absence and Retail regression checks	MKF-KC-17	S
MKF-MM-REV	M3	MultiMeters	Independent review, skeptic pass, fixes, git note	MKF-MM-17	M
MKF-KC-REV	M3	KickCD	Independent review, skeptic pass, fixes, git note	MKF-KC-18	M
MKF-STD-01	M4	WowAddonStandards	Two roster rows to Retail and Forever; no version bump	MKF-MM-REV,MKF-KC-REV	S
MKF-CT-REC	M4	Ka0sAddonsCommonTasks	Execution record, smoke roll-up, LibKa0s and Retail-identity issue texts	MKF-STD-01	S
```

| Checkpoint | Passes when | Then |
|---|---|---|
| CP-0 | bundle committed, owner answers recorded, MultiMeters base resolved or recorded as waiting | push CommonTasks branch |
| CP-1 MultiMeters | retail and forever suites 0 failed, luacheck 0/0, every file at most 1500 lines, TOC armed, vendor-sync case actually ran | lead pushes |
| CP-2 KickCD | the same, plus the seed bundle replays offline and the Retail list is byte-identical | lead pushes |
| CP-3 review | both notes recorded, findings fixed, gates rerun, max CCN 15 | lead pushes branches and notes; owner smoke |
| CP-4 land | owner go-ahead, fix branch merged first, fresh fetch of the standard, SavedVariables re-checked | finalize: standard, MultiMeters, KickCD, CommonTasks |
| CP-5 clean | everything merged | delete only this run's branches, worktrees, stashes. Leave `KickCD origin/feature/glow-options`, which predates it |

CP-1 and CP-2 are independent. Run each suite serially (`--jobs auto` gave 30 false failures last port, PT 2.9). Agents never push, never mark smoke passed, never act on a mid-task user message.

## 5. Unknowns

Each has a default that is safe to build on. Commands are for the owner, on Forever 71037 or later unless noted. None blocks the build except U1.

| # | Unknown | Safe default | Probe |
|---|---|---|---|
| U1 | Where the MultiMeters fix branch is | MultiMeters waits; KickCD proceeds | lead: `git -C MultiMeters branch -a --list '*r2-restore*'`, then ask the session that owns it |
| U2 | `specIconID` secret out of combat, and what it draws (FC 2, 3) | never use it on Forever; class icon | after a fight: `/run print(issecretvalue(C_DamageMeter.GetCombatSessionFromType(0,0).combatSources[1].specIconID))` |
| U3 | Plain join fields in combat (FC 30) | existing secret tests; a secret part makes the key ambiguous | mid-fight: `/run local r=C_DamageMeter.GetCombatSessionFromType(1,0).combatSources[1] for k,v in pairs(r) do print(k,issecretvalue(v) and "SECRET" or type(v)) end` |
| U4 | Abbreviation config takes our ladder and a secret (FC 5, F) | fallback in 3.3 | `/run local c=CreateAbbreviateConfig({{breakpoint=1000,abbreviation="K",significandDivisor=100,fractionDivisor=10,abbreviationIsGlobal=false},{breakpoint=0.001,abbreviation="",significandDivisor=1,fractionDivisor=1,abbreviationIsGlobal=false}}) print(AbbreviateNumbers(69.5625,{config=c}),AbbreviateNumbers(47500,{config=c}))`, repeat on a secret row rate; and `/dump AbbreviateLargeNumbers(69.5625)` |
| U5 | An ally's `amountPerSecond` (FC 7) | draw it; an empty rate cell stays empty, no invented value | grouped, mid-fight and after: `/run for _,r in ipairs(C_DamageMeter.GetCombatSessionFromType(1,0).combatSources) do local v=r.amountPerSecond print(issecretvalue(v) and "secret" or v) end` |
| U6 | Retail formatter refusal | skip the formatter only after the config proves good | Retail, in combat: `/run local v=C_DamageMeter.GetCombatSessionFromType(1,0).totalAmount print(pcall(function() return C_StringUtil.CreateAbbreviatedNumberFormatter():FormatNumber(v) end))` |
| U7 | Meter name and `unitName` format; per-attacker rows (FC 8, 34) | match whole names; Targets ships off, as today | two players, after a fight: `/run local s=C_DamageMeter.GetCombatSessionFromType(0,10) local e=s.combatSources[1] local d=C_DamageMeter.GetCombatSessionSourceFromType(0,10,nil,e.sourceCreatureID) for _,p in ipairs(d.combatSpells) do print(p.totalAmount,p.combatSpellDetails.unitName) end` |
| U8 | Non-group players among the sources | zero roster members of a class = ambiguous; the one-member case is documented | fight beside an ungrouped player, after: `/run for _,r in ipairs(C_DamageMeter.GetCombatSessionFromType(1,0).combatSources) do print(r.name,r.classFilename) end` |
| U9 | Non-Hunter pets and guardians folded (FC 9) | keep the merge setting | demon, totem, guardian fights: the U8 line |
| U10 | Collection with the meter CVar at 0 (FC 32) | not a requirement; no write | `/dump GetCVar("damageMeterEnabled"), C_DamageMeter.IsDamageMeterAvailable()`, fight, `/dump #C_DamageMeter.GetAvailableCombatSessions()` |
| U11 | Export during a dungeon lockdown (FC 36) | existing Combat refusal | in a dungeon, out of combat: `/dump C_ChatInfo.InChatMessagingLockdown()`, then Export to Party |
| U12 | Pet battles or skyriding on Forever | absent (D6) | `/dump C_PetBattles and C_PetBattles.IsInBattle(), C_PlayerInfo.GetGlidingInfo()`; owner confirms no such content |
| U13 | Avoidable fills; death recap content; group roles assigned (FC 11, 12) | Q4; existing recap degrade; Role fallback | after a dungeon run: `/dump #C_DamageMeter.GetCombatSessionFromType(0,8).combatSources`; die, `/run OpenDeathRecapUI()`; `/dump UnitGroupRolesAssigned("party1")` |
| U14 | Enemy casts exposed; flag meaningful and non-nil (FC 21, 43) | pass through; nil reads false | `/dump C_GameRules.IsGameRuleActive(Enum.GameRule.TargetCastBarDisabled)`; during casts by a normal and an immune mob: `/dump issecretvalue((select(8,UnitCastingInfo("target"))))` |
| U15 | A superseded rank stays known (FC 18, 56) | resolver asks every rank, highest first | Rogue 26+: `/dump C_SpellBook.IsSpellKnown(1766), C_SpellBook.IsSpellKnown(1767)`; Shaman 8+: the same with 8042, 8044 |
| U16 | Feral Charge override per form (FC A) | as 3.4 | cat, then bear: `/dump GetShapeshiftFormID(), C_Spell.GetOverrideSpell(1238122), C_Spell.GetSpellCooldown(1238122)`, then charge a caster |
| U17 | Pet bank and rebuild events for Spell Lock | pet rung; register each valid event | Felhunter out, then dismissed: `/dump C_SpellBook.IsSpellInSpellBook(19244,1,false)`; `/etrace` over the summon |
| U18 | Class-wide spec at runtime for eight classes, and below level 10 (FC 37) | fall back to the class's id | per class: `/dump C_SpecializationInfo.GetSpecializationInfo(C_SpecializationInfo.GetSpecialization())` |
| U19 | Class loop semantics; bare spec global (FC 16, 24) | static class table; namespaced member | `/dump GetNumClasses(), GetClassInfo(9), GetClassInfo(11), C_SpecializationInfo.GetAllClassIDs(), GetNumSpecializationsForClassID` |
| U20 | Cooldown secrecy per kick; shared Pummel and Shield Bash cooldown (FC 41, 57) | treat all as secret; draw what the client reports | in combat: `/dump C_Secrets.ShouldSpellCooldownBeSecret(6552)`; after Shield Bash: `/dump C_Spell.GetSpellCooldown(6552).isActive` |
| U21 | `isActive` during a GCD; 61304 at runtime (FC 23, 60) | Q7; no log mark | press any instant, at once: `/dump C_Spell.GetSpellCooldown(6552).isActive, C_Spell.GetSpellCooldown(61304)` |
| U22 | Silence's lockout (FC 52) | category silence; no lockout shown | Silence a caster, try the same school after 5 s |
| U23 | `/focus` works (FC 22) | port | `/dump C_GameRules.GetActiveGameMode()`, `/focus`, `/dump UnitExists("focus")` |
| U24 | Rune spells obtainable (FC 54) | excluded | Paladin: `/dump C_SpellBook.IsSpellKnown(425609)`; Druid: the same with 410176 |
| U25 | Deprecation fallbacks (FC 67) | no longer needed after KC-03 | `/dump GetCVarBool("loadDeprecationFallbacks"), IsPlayerSpell` |
| U26 | Glow art; widened name fit under the Forever skin | port; width from the skin's size | smoke all four glow styles, and a 25-character name |
| U27 | Surnames with a hyphen | never strip on Forever | `/dump GetUnitName("target",true)` on such a name, if one exists |

## 6. QUESTIONS FOR THE OWNER

Already settled and not asked: Retail-only features are absent on Forever, Forever gets its own spell lists and the Forever skin, names are "First Surname", and nothing merges without your go-ahead. No option below rewrites a saved Retail profile. Only question 3 changes what Retail looks like, unless an option says otherwise.

### Q1. MultiMeters: what should the grid show mid-fight when two players share a class?

Context: in combat WoW hides who each number belongs to. Retail matches numbers to players by class and spec. Forever hides the spec, so two Warriors look identical. Today's code can then put one Warrior's healing on the other's row. Numbers are complete again when combat ends.

- **A. Fill what is certain, blank the rest (recommended).** Forever: the sorted column is always complete. Other cells are blank for players who share a class, with the existing header note. You always see your own. A Warrior who has no value in the sorted column may have no row until combat ends. A party of five different classes looks full, and a 40-player raid is mostly blank outside the sorted column.
- **B. Sorted column only.** Forever: every other column is blank for everyone during combat, even where the answer is certain. Consistent, but shows less.
- **C. As A, with fewer default columns on Forever (Damage, Healing, Deaths).** Less empty space. Interrupts, Dispels and Avoidable have to be switched on by hand.

Retail and saved profiles: unchanged in all three.

Recommendation: A. It shows the most without ever showing the wrong player's number.

### Q2. MultiMeters: how much room should a Forever name get?

Context: Forever names have two words and up to 25 characters. The name column allows 15, so "Samplehunter Mockstride" reads "Samplehunter Mo". In combat a name can be protected, and the addon then cannot shorten it, so a narrow column clips it.

- **A. 25 characters and a wider window (recommended).** Forever: whole names. The name column grows from about 92 to 136 pixels and the default window from 694 to about 738, so the number columns keep their width.
- **B. 25 characters in the same window.** Forever: whole names, and each of the six number columns narrows from about 96 to 89 pixels.
- **C. Keep 15.** Forever: cut names, whole on hover. Two players can look alike.

Retail: unchanged. Saved profiles: the Forever default applies to new windows only. None exist on your Forever install today.

Recommendation: A.

### Q3. Both addons: should bugs found by the port also be fixed on Retail?

Context: five fixes are not really Forever-specific.
1. MultiMeters numbers mid-fight. The client refuses to format hidden numbers, so your decimals setting is ignored and raw tails such as 39.714285714286 can appear. This is measured on Forever and very likely on Retail.
2. A possible MultiMeters error during whisper export in a dungeon or raid.
3. KickCD's "is this spell known" check depends on functions Blizzard has deprecated.
4. KickCD reads spec counts and a missing spec in an outdated way.
5. KickCD's interruptible display and debug text need two small guards against missing or hidden values.

- **A. All five on both clients, each its own commit and test (recommended).** Retail's look changes in one place: mid-fight numbers follow your chosen format (for example "2.76M" where it may show "2M", "39" instead of a long tail). If Retail refuses the new formatting route, Retail keeps today's display. The other four are invisible unless the bug fires.
- **B. Fixes 2 to 5 on both, the number fix on Forever only.** Retail looks exactly as today and keeps the number bug.
- **C. All five on Forever only.** Retail is untouched and keeps all five, and the code carries more client switches.

Saved profiles: unchanged in all three. Under any option, if Forever refuses the new route, its live rates show as whole numbers such as 30190.

Recommendation: A.

### Q4. MultiMeters: should the Avoidable Damage column be on by default on Forever?

Context: this column depends on Blizzard flagging spells as avoidable. Nobody has yet seen whether it fills on Forever. Blizzard's "may not be available in all content" message appears in Retail's code too, so it is not proof either way.

- **A. On, as on Retail, until a dungeon test shows it is empty (recommended).** Forever: the same columns as Retail. This one may stay empty.
- **B. Off, but selectable.** Forever: five number columns, each wider. You would have to switch it on to find out whether it works.

Retail: unchanged. Saved profiles: the default is copied into a window when it is created, so a later change reaches new windows only.

Recommendation: A, because there is no evidence yet that it is broken.

### Q5. KickCD: one Forever spell list per class, or one per talent tree?

Context: Forever reports one specialization per class. The three talent trees are not specs. Spells you have not learned are hidden, and the first one shown is the big icon. The difference matters most for Warriors: Pummel and Shield Bash share a cooldown, but Pummel needs Berserker Stance and Shield Bash needs a shield.

- **A. Nine lists, one per class, Pummel first for Warriors (recommended).** Forever: simple, and you can reorder. Shield Bash is the big icon until Pummel is learned at 38. After that a shield tank sees Pummel big and may want to swap them.
- **B. Nine lists, Shield Bash first for Warriors.** Forever: better for shield tanks. A Warrior without a shield has a big icon they cannot press.
- **C. Twenty-seven lists, one per tree.** Forever: each tree gets its own order. Respeccing switches lists, hybrids need a tie rule, and Forever profiles store lists in a new shape.

Retail: unchanged. Saved profiles: Forever lists are written into a profile when first created, so changing this later would need a conversion.

Recommendation: A.

### Q6. KickCD: how many control spells should the Forever default lists hold?

Context: your seed rules let Claude add true interrupts, and leave the choice of other cast-stopping spells to you. The core list is every reachable interrupt plus Forever's versions of the stops Retail already ships (stuns, fears, Polymorph and similar). Nine more are possible.

- **A. Core only.** Forever: the shortest grids. Shaman has Earth Shock alone (plus War Stomp for Tauren).
- **B. Core plus Rogue Gouge and Warrior Intercept (recommended).** Forever: two more short-cooldown stops that are useful in dungeons.
- **C. Core plus all nine.** Forever: B plus Holy Wrath, Scare Beast, Confounding Flash, Grounding Totem, Seduction, Pounce and Hibernate. Bigger grids, with several narrow spells and several that have no cooldown and always look ready.

Retail: unchanged. Saved profiles: a later change reaches new profiles, or existing ones only after Defaults is pressed on the Spells page.

Recommendation: B.

### Q7. KickCD: should "glow when ready" go out during the global cooldown?

Context: on Retail most kicks ignore the global cooldown, so their glow stays steady. On Forever most kicks use it (Counterspell and bear Feral Charge do not), so by the current rule the glow goes out for 1 to 1.5 seconds after almost every ability you press.

- **A. Keep it literal (recommended for the port).** Forever: the glow blinks off, and a glow always means "press now works". Judge it in the smoke test.
- **B. Hold it through the global cooldown on Forever.** Forever: a steady glow, which can show up to 1.5 seconds before the kick will fire.
- **C. Hold it on both clients.** Forever as B. **Retail's look changes:** stuns and other spells on the global cooldown stop blinking.

Saved profiles: unchanged in all three.

Recommendation: A, then revisit after you have played with it.

### Q8. KickCD: which spells may a Forever player add to a list?

Context: Retail accepts only spells Blizzard's Cooldown Manager tracks for your spec. Blizzard's Forever sets leave out Spell Lock, the Warlock interrupt, and were not curated for this purpose.

- **A. Anything you or your pet know, plus anything in KickCD's own Forever lists (recommended).** Forever: learned spells and every rank work, and the built-in spells can be restored before you learn them. Other unlearned spells are refused.
- **B. Keep Blizzard's gate, widened to every rank and to known pet spells.** Forever: closest to Retail. A spell you know can still be refused because Blizzard left it out.
- **C. Any spell that exists.** Forever: no refusals, and a wrong id is easy to save as a permanently hidden row.

Retail and saved profiles: unchanged in all three.

Recommendation: A.
