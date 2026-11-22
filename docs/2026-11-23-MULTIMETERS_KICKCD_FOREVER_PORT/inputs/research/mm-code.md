# MultiMeters: Forever port code audit (mm-code)

Snapshot: `port/snap/MultiMeters` = master bf67258 (1.2.0, LibKa0s v1.109.0, kit rev 59).
Clients: Forever UI 734f065 (1.60.1.71037), Retail UI ab5cb85 (12.1.5.70961). Forever DB2: wago.tools, build 1.60.1.71037.
Scratch copies, scripts, run logs and downloaded tables: `port/work/mm-code/`.

Paths: plain paths are MultiMeters' own. `UI:` is `port/ui/forever/Interface/AddOns/`. `DOC:` is
`UI:Blizzard_APIDocumentationGenerated/`. `CT:` is CombatTrail master (30df90e) `docs/forever-quirks.md`, own section.

Status: **VERIFIED** = read in the named source, or run here. "VERIFIED (measured)" = another addon's recorded in-game
probe, on the build named. **INFERRED** = reasoning given. **UNKNOWN** = the probe that settles it is given (section 8).

Not designed around, per the brief: master's schema v28 / `skin.swatchesFollow` defaults, which a fix branch reverts.

---

## 0. Verdict

The port is feasible and the core carries over: all eight meter calls, the three meter events, the enums and the death
recap exist on Forever. It is not a TOC-only port, and the classification of 2026-11-07 understates it in one direction
and overstates it in another.

| What the classification said | What this audit found |
|---|---|
| "`C_DamageMeter` loads on Forever, so the core works" | Loads, yes. Three core behaviors are wrong there: the mid-pull join (1.2), mid-pull number text (1.3) and names (1.4). |
| "About 50 `specIconID` reads, each needs a guard" | About 50 mentions with comments and sim data. Four live consumers: `modules/Aggregator_Identity.lua:118` (already guarded), `modules/Row_NameCell.lua:416-417`, `modules/Export.lua:403` (already guarded), and the diagnostics probe (already guarded). The guard is not the work. What the key means without the field is. |
| "The Delve content type is gated off" | Also arena, scenario, housing, skyriding and pet battles, the Retail companion seed and one mount form. |
| "The chat reports need a check" | Whole names work. The description text is Retail-shaped, and a secret system line can raise on both clients (4.6). |
| (not listed) | Sample, test and sim data are Retail-only and 27 of the 52 spell ids in them do not exist on Forever. The role fallback reads every class as a damage dealer. |

Must be fixed before a Forever build ships, in order:

1. **1.2** A player's healing is drawn under another player's name mid-pull (reproduced).
2. **1.3** The number format is bypassed mid-pull, so rates under 1000 print raw decimals, and classic rates are mostly
   under 1000 (reproduced against the documented behavior; the refusal was measured in game on 70888).
3. **1.4** Every roster name loses its surname, so two players collide on screen and Targets cannot match (reproduced).

Nothing found stops the port. Suite on Forever: 45 failures, 44 of them the per-client default skin doing its job and
one a mock-ordering artifact (section 7).

---

## 1. The load-bearing differences

### 1.1 `specIconID` is always secret on Forever

- VERIFIED: `DOC:DamageMeterDocumentation.lua:203,242` has `specIconID ... SecretValue = true` on both the source and the
  spell-detail struct. Retail has `NeverSecret = true` on the same lines. These two lines are the only differences in
  that file; the constants file and the death-recap file are identical.
- VERIFIED: Blizzard's own meter was changed for it on Forever. `UI:Blizzard_DamageMeter/DamageMeterEntry.lua:54` adds
  `issecretvalue(texture)` before its compare.
- INFERRED: the mark is unconditional, so it is secret out of combat too. `SecretValue` carries no predicate, where the
  session functions say `SecretWhenInCombat`. Probe P1.
- VERIFIED (DB2 `ChrSpecialization`, 71037): Forever has one spec per class (1482, 1484-1491, plus 1493 "Default"),
  with icons 625999-626008, one per class. So even a readable icon would say nothing the class does not.

| Site | What happens on Forever | Recommendation |
|---|---|---|
| `modules/Provider.lua:274` | copies the handle | port |
| `modules/Provider.lua:616`, field probe `:665-700` | `noteValue` gates on IsSecret before any key | port; diagnostics say SECRET |
| `modules/Aggregator.lua:180` | secret stored in an in-memory row | port. Not persisted: `modules/Roster.lua:rememberMember` copies no icon |
| `modules/Aggregator_Identity.lua:115-123` | folds to `0`, key is `class_0_isLocal` | **adapt, 1.2** |
| `modules/Row_NameCell.lua:416-418` | truth-tests the secret, hands it to `SetTexture`. A secret 0 cannot be told from a real icon, so the class fallback never runs and the slot can be empty | **adapt**: on Forever always take the class rung. `SetTexture` would accept it (`DOC:SimpleTextureBaseAPIDocumentation.lua:604`, AllowedWhenTainted), but there is no gain |
| `modules/Export.lua:241,403` | `CsvField` answers "", so the `spec` column is always blank | **absent**: drop the `spec` header and field on Forever through a per-client column list |
| `core/Diagnostics_Identity.lua:66-87,385` | prints "collides on class+spec", "collapses to class alone" as a defect | adapt wording and key-field list |
| `modules/Aggregator_Preview.lua:210,223`, `modules/SimWorld.lua:155,380` | plain invented icons, so test mode would show a look live play never has | adapt: none on Forever |
| `settings/Schema.lua:879`, `locales/enUS.lua:510` | "their specialization where it is known" | adapt text |
| Comments: `modules/Aggregator.lua:168-170`, `modules/Row_NameCell.lua:402` | say NeverSecret | false on Forever |
| Docs: `docs/ARCHITECTURE.md:248`, `docs/data-flow.md:257-258,361-370`, `docs/schema.md:1045`, `docs/scope.md:219-240` | same claim | update |
| `modules/Targets.lua` | never reads `combatSpellDetails.specIconID` | none |

Put the choice in one place (a per-client `Constants` value such as "identity uses spec", picked once by
`ClientKey()`), not a client test in each module (clients-§3).

### 1.2 The mid-pull join mislabels with a class-only key

The identity build (`modules/Aggregator_Identity.lua`) runs whenever the Combat restriction is on
(`modules/Aggregator.lua`, `newPass`: `identityMode = Secrets.IsRestricted()`). `detectCollisions` proves a key ambiguous
only when **one column** lists that key twice. With class+spec that hole is narrow. With class alone it is ordinary.

VERIFIED by experiment (`port/work/mm-code/MM4`, log `probe.txt`). Warrior, shadow priest A in Damage only, holy priest B
in Healing only, restricted:

```
plain-icon  | row1 ShadowA | healing -   | row2 HolyB | healing 500
secret-icon | row1 ShadowA | healing 500 |                             ambiguous=false
```

B's row disappears and B's 500 healing is drawn on A's row, with no header warning. That is the exact mislabel the
file's header refuses.

Fix, Forever (every class key):
- Seed the collision set from the roster before the fill: any class worn by two or more non-local members is
  ambiguous, whatever the columns say. The local player keeps their own key through `isLocalPlayer`.
- Count the remembered members too for the Overall session, because departed players are still in that data
  (`modules/Roster.lua`, `rememberMember`). It is a superset, so it can only over-blank.
- Sources with an empty `classFilename` (pets, creatures) share one key; treat that key as ambiguous as well.
- Test: the case above must blank, and raise `ambiguousRows`.

Cost, which the owner should accept knowingly (question 1): a 40-player raid has nine classes
(VERIFIED DB2 `ChrClasses`), so mid-pull almost every column but the sort column is blank until combat ends, and a
same-class player absent from the sort column gets no row (`adoptUnknownSources` refuses a collided key). In a party it
happens whenever two share a class. The other ways out were measured dead on Retail (the file's header); INFERRED the
same here, since every other per-player field has the same secrecy annotations.

Retail keeps class+spec. It has the same hole for two players of one spec in disjoint columns; that is existing
behavior and a separate issue.

### 1.3 The number formatters refuse secrets

- VERIFIED: `DOC:NumericFormatterAPIDocumentation.lua:11-14` `FormatNumber` is
  `SecretArguments = "AllowedWhenUntainted"`. The file is byte-identical on Retail. Addon code is always tainted.
- VERIFIED (measured, Forever 70888, `CT:` "The client number formatters refuse a secret from addon code"): both
  constructors' instances raise "Secret values are only allowed during untainted execution", while `AbbreviateNumbers`,
  `C_StringUtil.FloorToNearestString` and `string.format("%d")` answer a secret string.
- So the premise at `modules/Format.lua:17,40`, `core/Compat.lua:498-520`, `CLAUDE.md`, `docs/data-flow.md:483`,
  `docs/scope.md:104` and `docs/compat-layer.md:215` is false on Forever. INFERRED false on Retail too (same doc, and
  CombatTrail's Retail note says neither formatter served a secret).
- What the code does: `Format.Number` pcalls the formatter, fails, and calls bare `AbbreviateNumbers(v)` with no options
  (`modules/Format.lua:541-543`). In `full` mode it falls to `string.format("%s")`. The decimal setting is ignored and
  each cell pays a raised, caught error on every refresh.

VERIFIED by experiment, with `FormatNumber` raising on a secret as documented and `AbbreviateNumbers` modeled on the
measured answer (69.5625 draws "69.5625"):

| mode | plain rate | secret rate | secret total 30190 |
|---|---|---|---|
| abbreviated | 69 | **69.5625** | 30K |
| abbreviatedWhole | 69 | **69.5625** | 30K |
| abbreviatedTwo | 69 | **69.5625** | 30K |
| full | 69 | **69.5625** | 30190 |

The shipped left slot is `smart`, the rate on Damage and Healing, so this is the number players watch. A float such as
39.714285714286 overflows a 92 px cell.

The suite cannot see it: `tests/wow_mock.lua:627-632` `FormatNumber` calls `reveal(v)` and accepts every secret.

Fix:
- For a secret, skip the formatter (ask `Secrets.IsSecret` first) and call `AbbreviateNumbers(v, { config = ... })`
  with a config built once per mode by `CreateAbbreviateConfig(ladder)`. VERIFIED signatures:
  `DOC:LocalizationDocumentation.lua:26-36,73-84,182-190`. `breakpointData` is ordered largest to smallest, the reverse
  of `BREAKPOINTS`.
- Prove the config on plain probes first, as `ladderTook` does. `CreateAbbreviateConfig` has the precondition
  `RequiresRestrictedAbbreviationBreakpoints`, so whether the 0.001 floor is accepted is UNKNOWN (probe P3).
- Fallback: `C_StringUtil.FloorToNearestString(v)` (`DOC:StringUtilDocumentation.lua:106`, AllowedWhenTainted;
  measured OK on 70888). A whole number, never a float.
- `Format.Duration`'s secret branch (`modules/Format.lua`, through `Format.Number`) gets the same fix free.
- Make the mock raise, as documented, or the fix has no test.

### 1.4 Names are "First Surname"

VERIFIED: forever-quirks-§4 (owner probe, 70790); `UI:Blizzard_FrameXMLUtil/Camelot/NameUtil.lua:4-12`;
surname up to 12 letters (`UI:Blizzard_CharacterCreate/Camelot/Blizzard_CharacterCreate.xml:608`), first name up to 12
(GlobalStrings `CHAR_NAME_TOO_LONG`), so up to **25 characters**.

| Site | Today | Change |
|---|---|---|
| `core/Compat.lua:770-775` `UnitName` | first return only | route display identity through `Compat.UnitCharacterName` (wired at `:89`, unused) |
| `modules/Roster.lua:234,446` | roster name "Traxex"; `newRow` prefers it over the meter's name (`modules/Aggregator.lua:178`) | use `UnitCharacterName`. VERIFIED by experiment: two players both read "Traxex" today, the library answers both whole names |
| `modules/Roster.lua:rememberMember` -> `db.global.roster.byGuid[guid].name` (`defaults/Profile.lua`, global) | stores the first name | **key is the GUID, so no key breaks.** The stored value corrects on the next build. No migration |
| `modules/Sim.lua:201` | `C.UnitName("player")` | whole name |
| `modules/SimWorld.lua:568-574` | comments "Retail, no regional names" | whole invented names; `UnitName` provider follows |
| `modules/Targets.lua:176-184,377` | both sides through `Ambiguate(...,"short")`, which keeps a two-word name whole (measured). The hovered side is the roster's first name, so it cannot match a whole `unitName`; with first names only it would merge two players in `byPlayer` | fixed by the roster change. The `match("^([^-]+)")` fallback is safe for a name with a space. The meter's `unitName` format is UNKNOWN (P4) |
| `modules/Row_NameCell.lua:351-367` | strips at the first hyphen on a `Player-` GUID | skip when `Compat.RegionalNames()`: there is no realm to strip |
| `modules/Row_NameCell.lua:369-374`, `defaults/Profile.lua` `text.maxNameLength = 15` | VERIFIED: "Samplehunter Mockstride" draws "Samplehunter Mo" | owner question 2. The standard says size for the long form or truncate with the whole name in the tooltip |
| `modules/Window.lua:150-200` `nameColumnWidth` | follows the cap (25 chars at 10.5 px is about 135 px with the icon) | `frame.width = 694` may need a Forever default so seven columns still fit; `NAME_COLUMN_WIDTH = 118` (`core/Constants.lua`) is the no-cap fallback and is too narrow |
| `modules/Aggregator_Order.lua` name sorts | sorts the first name, unstable for shared names | fixed by the roster change |
| `modules/DrillDown.lua:311-320` title, tooltip header, `modules/Export.lua` chat and CSV `name` | first name | fixed by the roster change |
| `modules/Export.lua:626-631` `TargetName` | `GetUnitName("target", true)` is already whole | fallback `UnitName` -> `UnitCharacterName` |
| `modules/Export.lua:677` whisper target | trims ends only, keeps the inner space | none |
| `modules/Export.lua:803-809` not-found pattern | captures `(.+)`, takes a space. VERIFIED Forever string unchanged (GlobalStrings 14015) | none |
| `settings/Schema_General.lua:317`, `locales/enUS.lua:922` | "Cross-realm names need the realm, as Name-Realm." | per-client text: "First Surname" |
| `settings/Schema.lua:866`, `locales/enUS.lua:485` | "The realm is always stripped." | per-client text |
| `settings/Slash.lua:643` `/mm window copy` | first word is the source | window names, not characters. None |
| `core/Compat.lua:90-91` CharacterKey, RealmKey | unused | none: the addon stores nothing by character name. AceDB 40 owns the profile keys |
| `modules/Aggregator.lua` joins, `Feign`, `Roster` maps | keyed by GUID | none |

Never split on whitespace, never key on the first word.

### 1.5 Role is class-wide

- VERIFIED DB2 `ChrSpecialization` 71037: `Role = 2` (damage) for **all nine** classes' spec. VERIFIED (measured,
  70862, `CT:`): `GetSpecializationInfo` answers a class pseudo spec whatever the points.
- So the fallback at `modules/Roster.lua:261-268` and `modules/Sim.lua:199-200` answers DAMAGER for a solo tank or
  healer. Consumers: roster sort (`modules/Aggregator_Order.lua` ROLE_RANK), role color mode (`modules/Row.lua:300-301`),
  CSV `role`, the sim's player.
- Adapt: `LibKa0s-Role-1.0` `Resolve(nil)` for the local player (clients-§3). It is already vendored
  (`libs/LibKa0s/Role.lua`). No override setting is needed for these uses. Retail can keep its ladder or use Resolve;
  the latter answers the same. The degraded path keeps today's ladder.
- `core/SimSetup.lua` PURE list: add the new member.
- Others' roles come from `UnitGroupRolesAssigned` (present, same doc). Whether classic groups assign any is UNKNOWN
  (P7); "NONE" already renders.

### 1.6 What the meter itself does differently

| Fact | Status | Effect here |
|---|---|---|
| All eight functions, three events, two enums as on Retail | VERIFIED `DOC:DamageMeterDocumentation.lua`; measured 70862 (`CT:`) | port |
| `GetCombatSessionSource*` has no `amountPerSecond` | VERIFIED: struct `DamageMeterCombatSessionSource` has only spells, max and total. CombatTrail's "nil on the source table" is that struct | none: MM never reads it there |
| The **row's** `amountPerSecond` on an ally in DamageDone | Documented non-nilable (`:206`). CombatTrail's later note says live DPS "comes from the session's local row", and the standard's one-repo note says "the player source's amountPerSecond is nil out of combat" | **UNKNOWN, P2.** If nil, `smart` draws empty Damage and Healing cells (`modules/Row.lua:994-997` has no fallback by design) |
| A pet is folded into its owner's source; its spells and a second "Attack" row carry `creatureName` | VERIFIED (measured, 70888, one Hunter, `CT:`) | `data.mergePets` (`defaults/Profile.lua`, `Aggregator.lua:281-316`) has nothing to merge for a hunter. Warlock pets, totems and guardians UNKNOWN (P5). Keep the setting until measured. Tooltip and drill-down show two same-named rows (`modules/DrillDown.lua:529-545` ignores `creatureName`): append a plain non-empty creature name |
| Meter values secret in combat, plain by 2 s after | VERIFIED (measured, 70888, `CT:`) | the two-build design holds |
| `UNIT_SPELLCAST_SUCCEEDED` spell id plain for player and pet | VERIFIED (measured, 70888). Others' secret: doc predicate | Feign filter works as on Retail |
| EnemyDamageTaken: one row per enemy by creature id, no GUID; solo drill-down is one row, spellID 0, the whole total | VERIFIED (measured, 70888). Whether `combatSpellDetails.unitName` names each attacker in a group was not captured | Targets (`modules/Targets.lua`) UNKNOWN, P4. `showTargets` ships off |
| Avoidable damage "may not be available in all content" | VERIFIED string `DAMAGE_METER_AVOIDABLE_DAMAGE_NOT_ACTIVE` (GlobalStrings 57100), shown by `UI:Blizzard_DamageMeter/DamageMeterSessionWindow.lua:712-714` | default-on column may be empty for all classic content. P6, question 3 |
| Classification icons hidden by Blizzard on Forever | VERIFIED `UI:Blizzard_DamageMeter/Camelot/DamageMeterEntryOverrides.lua` | MM draws none |
| Feign Death is still 5384, one rank | VERIFIED DB2 `SpellName` | `core/MultiMeters.lua` FEIGN_DEATH_SPELL ports. Whether the meter logs a feign as a death: P8 |

### 1.7 Death recap

- VERIFIED: `C_DeathRecap`'s four functions are documented, unchanged.
- VERIFIED: `OpenDeathRecapUI` loads: `UI:Blizzard_DeathRecap/Blizzard_DeathRecap.toc` runs the bootstrap on every game
  type and the body on `mainline`; `Mainline/Blizzard_DeathRecap_Bootstrap.lua:7` defines it. Camelot is inside mainline
  (`UI:Blizzard_FrameXMLUtil/Blizzard_FrameXMLUtil.toc` needs `[ExcludeLoadGameType camelot]` on a mainline line).
- Port: `core/Compat.lua:243-303,849-854`, `modules/DrillDown.lua:215,433,510-603`,
  `modules/Tooltip_Builders.lua`, `core/Diagnostics_DeathRecap.lua`. Recap event fields are undocumented on both
  clients (empty struct), so content is UNKNOWN until P8.

---

## 2. Secret-value sites

| Site | Guard | On Forever |
|---|---|---|
| `core/Secrets.lua:86-141` restriction type and state | enum and API present, values identical | port |
| `core/Secrets.lua:170-330` guards, SafeIterate | APIs present | port. `ITERATION_LIMIT = 512` also caps Deaths rows: 40 players x 13 wipes passes it, so Overall counts can clip |
| `modules/Provider.lua:224-285` row copy | CanAccessTable per row, nil tests only | port |
| `modules/Aggregator.lua` joins, pet fold, percent | IsSafeKey, CanCompare2 | port |
| `modules/Aggregator_Identity.lua:115-123` | IsSecret per part | safe, wrong meaning (1.2) |
| `modules/Aggregator_Order.lua` | CanCompare before sort | port |
| `modules/Row.lua:900-1030` bar and text | setters AllowedWhenTainted (`DOC:SimpleStatusBarAPIDocumentation.lua:229,355`, `DOC:SimpleFontStringAPIDocumentation.lua:664`) | port; text is 1.3 |
| `modules/Row_NameCell.lua:280-376` name | IsConcatSafe, opaque to SetText | port. A secret name is uncapped, and a 25-char one is likelier to run into the next column mid-pull |
| `modules/Row_NameCell.lua:416` | truth test on a non-boolean secret | 1.1 |
| `modules/Roster.lua:256` role compare; `:238` class | `SecretWhenUnitIdentityRestricted`: only non-group, non-player units | safe for group tokens (INFERRED from `DOC:SecretPredicatesDocumentation.lua:130-133`) |
| `modules/Feign.lua` health | CanCompare; `UnitHealth` SecretReturns | port: a secret health neither proves dead nor alive |
| `core/MultiMeters.lua` noteFeignCast | CanCompare(spellID) | port |
| `modules/Export.lua:403` CSV | CanAccess | blank, 1.1 |
| `modules/Export.lua:856-870` system line | **none before `:match`** | 4.6 |
| `modules/Targets.lua:196-300` | CanAccess, IsSafeKey on both ids | port |
| `modules/Tooltip.lua:612` screen size | plainNumber | port |
| `modules/DrillDown.lua:529-545` | `string.format` of a maybe-secret spell id into a row id | never used as a table key (no keyed use found); port |
| `modules/Window_Placement.lua:79` `GetPoint` | own anchor, holds no secret | port |
| Frame strata of Blizzard frames | none read; `GetFrameLevel` on own frames and GameTooltip (`modules/Tooltip_Lines.lua:73`) | port |
| `modules/Tooltip_Builders.lua:488`, `modules/DrillDown.lua:663` | mid-pull pass a synthetic `rank_N` GUID to the meter | existing Retail behavior, unchanged by the port |

---

## 3. Retail-only features

| Feature | Sites | Evidence on Forever | Recommendation |
|---|---|---|---|
| Delves visibility | `core/Compat.lua:680-717`; `settings/Schema_General.lua:82-87`; `defaults/Profile.lua` visibility; `modules/Visibility.lua:109-114`; `modules/SimWorld.lua` IsInDelve | APIs still documented, so feature detection would lie. Delves picker and toast are `standard` only (VERIFIED tocs) | **absent** |
| Arenas | `settings/Schema_General.lua:70-75`; `modules/Visibility.lua` map | VERIFIED DB2 `Map`: zero InstanceType 4. `Blizzard_PVPUI` excludes camelot. Owner ruling QuickComms R1 | **absent** |
| Scenarios, follower dungeons | `settings/Schema_General.lua:88-93` | VERIFIED DB2 `Map`: zero InstanceType 5; `Scenario` table absent (HTTP 400). Same ruling | **absent** |
| Housing | `core/Compat.lua:736-740`; `settings/Schema_General.lua:135-140` | VERIFIED: every Housing addon is `standard` only | **absent** |
| Skyriding | `core/Compat.lua:727-732`; `settings/Schema_General.lua:122-127`; two glide events | INFERRED no skyriding in classic-era content; API and events still documented | **absent** (question 4) |
| Pet battles | `modules/Visibility.lua:189-193`; `settings/Schema_General.lua:142-146`; two events | INFERRED none. `Blizzard_PetBattleUI` does load on camelot and `BattlePetSpecies` has 122 rows, so this is not proved | **absent** (question 4) |
| Vehicles | `modules/Visibility.lua:123-126`; schema `:109-113` | API and events present; DB2 `Vehicle` 55 rows | port |
| Flight paths, mounted, dead, solo, combat rules | Visibility | present; `TaxiPath` 328 rows | port |
| Mount-like forms `{3,4,27}` | `modules/Visibility.lua:160` | VERIFIED DB2 `SpellShapeshiftForm`: 3 Travel, 4 Aquatic, 27 unnamed | **adapt**: per-client `{3,4}`. Same description works |
| Battlegrounds | schema `:76-81` | VERIFIED five maps of type 3 | port |
| Dungeon, raid, open world | schema | present | port |
| Delve companion seed (Valeera 248567) | `core/Constants.lua` COMPANION_CREATURE_IDS; `modules/Aggregator.lua:686-716,779` | no delves | **absent**: empty Forever list by decision (clients-§5) |
| Mythic+ / ChallengeMode | comments only (`core/Secrets.lua`) | no code | none |
| Season | no site | - | none |
| Evoker, DK, Monk, DH | test and sim data only (5) | not classes there (VERIFIED DB2) | **adapt**: own seeds |
| Spec icon, CSV spec | 1.1 | always secret | **absent** |
| Pet merge | 1.6 | folded for hunters | **port** until P5 |
| Avoidable column | `core/Constants.lua` STATS | 1.6 | **port**; default per question 3 |
| Absorbs, Interrupts, Dispels, Deaths, Taken | STATS | same enum, same Blizzard categories | port |
| Death recap | 1.7 | present | port |
| Export to chat, whisper, target | `modules/Export.lua` | sender present, same doc | adapt names |
| Instance chat channel | `core/Constants.lua` EXPORT_CHANNELS | INFERRED serves battleground groups; no LFG group otherwise | port |
| EllesmereUI skin source | TOC OptionalDeps, skin seam | library-owned, feature-detected | port |
| Built-in meter CVar `damageMeterEnabled` | MM reads and writes no CVar; shows Blizzard's reason | VERIFIED exists: `UI:Blizzard_DamageMeter/DamageMeter.lua:1` | port |

No slash verb, launcher entry, page or key binding is client-specific. `Bindings.xml` holds one shared binding.

### How to gate

- `NS.Schema` is indexed at file load (`settings/Schema_Paths.lua`) and reached by get, set, reset, defaults and copy.
  A row-level `clients` hides it in the options renderer and the CLI list (`libs/LibKa0s/Slash.lua:601`,
  `OptionsRegistry.lua:49-70`), but the addon's own path index would still resolve it. Filter the array through
  `ForClient` before the index is built, so the row is absent.
- `defaults/Profile.lua` carries the visibility keys. With the context probe gone on Forever `GetContext` never answers
  those keys, so harmless stored values can stay; drop them from the Forever defaults for a clean pin.
- `core/MultiMeters.lua` EVENTS: add `clients` on the four travel events and register through `ForClient`.
- `VETOES` and `CONTEXT_BY_INSTANCE_TYPE`: per-client lists picked once. Never map an unknown context to a hidden rule.
- `core/Compat.lua` has no `IsForever`, `IsRetail`, `ClientKey` or `ForClient`. Add them (a `core/CompatClient.lua`,
  DropWatcher's precedent), above `core/SimSetup.lua`, and list them in its PURE table.

---

## 4. Smaller findings

1. **Row count.** 40 players is the normal raid. `MAX_ROWS = 40` fits. `tests/perf.lua:88` measures 20 and the ceilings
   were set there: add a 40-player scenario.
2. **`Targets.ENEMY_LIMIT = 64`** (`modules/Targets.lua:105`) silently truncates a walk. Classic raid trash can pass it
   on Overall. INFERRED; low.
3. **Icons and atlases.** VERIFIED in DB2 `UiTextureAtlasElement`: every first-choice atlas exists except
   `poi-scrollofresonance`, whose second choice exists (`modules/HeaderControls.lua:201`). `common-icon-settings` is
   missing but is itself a second choice behind one that exists. No change.
4. **Class coordinates.** `CLASS_ICON_TCOORDS` has all nine (`UI:Blizzard_SharedXML/SharedConstants.lua:27-41`).
5. **Templates and fonts** all resolve (Appendix A.1). `STANDARD_TEXT_FONT` is only a fallback.
6. **A secret system line can raise, both clients.** `CHAT_MSG_SYSTEM` is `SecretInChatMessagingLockdown`, which the
   docs say covers dungeon and raid maps (`DOC:SecretPredicatesDocumentation.lua:65-67`). With a whisper dump in
   flight, `Export.NoteSystemMessage` does `type(message) == "string"` (true for a secret string) and then `:match`.
   INFERRED raise. The mock models a secret as a table, so it returns early and cannot show it. Guard with CanAccess.
7. **Sending during a chat lockdown.** `SendChatMessage` is `HasRestrictions` on both; `Export.Available` checks only
   the Combat restriction. Whether a dungeon send after combat works on Forever: P9.
8. **`core/Compat.lua:84-86` and `modules/Aggregator_Preview.lua`** say "Retail-only tree", "ships Retail only".
   `README.md` says "Retail only for now".
9. **LibKa0s.** v1.109.0 has every member the port needs (client helpers, names, Role, Sim samples, DefaultSkin, the
   `clients` gates). v1.110.0 differs only in `Compat.lua` (the container readers). No re-vendor is required.

---

## 5. Test mode, sim and sample data

| Data | Site | Retail shape | Forever list |
|---|---|---|---|
| Shared five | `modules/Aggregator_Preview.lua:59-65,79` | `Sim.Sample("retail")` forced, local copy | `Sample()` by client; use `fullName` ("Samplehunter Mockstride"); Forever fallback copy |
| Host five | `modules/Aggregator_Preview.lua:68-74` | Monk, Death Knight | Rogue, Warlock, Druid, Shaman, plus one repeat (nine classes, ten rows), two-word names |
| Spec icons | `:53-56` | Retail spec icons | none: class icon |
| Spells | `:121-128` | Chaos Bolt 116858 and Incinerate 29722 missing on Forever (VERIFIED DB2) | `SimWorld` Forever warlock or mage spells |
| Magnitudes | `:133-142`, `:253` recap `maxHealth = 700000` | 4.2M damage | thousands; health about 4000; rates under 1000, which also exercises 1.3 in test mode |
| "Preview Trash" | `:269` | neutral | port |
| Names | `modules/SimWorld.lua:56-63` | forty one-word names | forty pairs, 12+12 max. Include one shared first name |
| Classes | `modules/SimWorld.lua:67-83` | 13, with Evoker, DH, DK, Monk | nine |
| Class spells | same | **25 of 46** ids in the file missing on Forever (VERIFIED DB2) | candidates below |
| Pets | `:95-96` | 17253, 16827, 3110 all exist | port; fold the pet into the owner's rows as Forever does (1.6) |
| Enemy spells | `:97-100` | all four exist | port |
| Rates, health | `:104-140`, `:312` recap 650000 | Retail scale | classic scale |
| Role by class | CLASSES | Warrior and Paladin tank, three healers | fine |
| Zones | `modules/SimWorld.lua:47-52` | Rookery, Priory, Undermine, Isle of Dorn | Deadmines (map 36), Scarlet Monastery (189), Molten Core (409), an open-world zone |
| Bosses | `modules/SimScenario.lua:47-48` | Shadowcrown 211290, Vexie 225821 | names VERIFIED in DB2 `DungeonEncounter`: Edwin VanCleef (2747), Ragnaros (672). Those are encounter ids, **not creature ids**: creature ids are not in DB2, so use invented ids in the sim's range or probe |
| Raid size | `modules/SimScenario.lua` DEFS `raid` | 20 | 40 on Forever; `buildPool` yields 39 mates, so it fits |
| Scenario step keys | DEFS | rookery, undermine, dorn, priory | per-client keys |
| Sim player | `modules/Sim.lua:196-202` | first name, spec role | whole name, Role.Resolve |
| Skin picker preview | `core/SkinSetup.lua:545-560` | enters test mode | follows the seeds |

Candidate Forever spell seeds, each id and name VERIFIED in DB2 `SpellName` 71037 (needs a ruling, clients-§10):

| Class | Ids |
|---|---|
| WARRIOR | 23922 Shield Slam, 6572 Revenge, 6343 Thunder Clap |
| PALADIN | 635 Holy Light, 20271 Judgement, 26573 Consecration |
| PRIEST | 2061 Flash Heal, 2060 Greater Heal, 596 Prayer of Healing |
| DRUID | 774 Rejuvenation, 8936 Regrowth, 5185 Healing Touch |
| SHAMAN | 8004 Lesser Healing Wave, 331 Healing Wave, 1064 Chain Heal |
| MAGE | 116 Frostbolt, 133 Fireball, 2136 Fire Blast |
| ROGUE | 53 Backstab, 1752 Sinister Strike, 2098 Eviscerate |
| HUNTER | 75 Auto Shot, 3044 Arcane Shot, 2643 Multi-Shot |
| WARLOCK | 172 Corruption, 980 Bane of Agony, 686 Shadow Bolt |

---

## 6. Default skin

- VERIFIED already per client: `core/SkinSetup.lua:126` `NS.DEFAULT_SKIN = Skin:DefaultSkin()` read once at load,
  used by `defaults/Profile.lua:902` and the schema row (`settings/Schema_Skin.lua:45`). Under the Forever profile it
  answers `forever`; without the library `ka0s`. No client check in the addon. **No code change is needed.**
- `skin.source = "ka0s"` on both, correct.
- No migration writes a skin id (grep of `core/Database_Migrations.lua`). A fresh Forever DB runs the ladder from 0
  and the database suites pass under the Forever profile.
- `SKIN_VALUES` fallback label (`core/SkinSetup.lua:450`) is right, since DEFAULT can only be `ka0s` there.
- Stale comments: `core/SkinSetup.lua:102,462`, `settings/Schema_Skin.lua:15` say the reset lands on Ka0s Default.
- The Forever skin's HUD scale (0.958) shrinks the name column (118 -> 114) and fonts. Decide the Forever name width
  under that skin, not under Ka0s Default.

---

## 7. The suite under `KA0S_KIT_CLIENT=forever`

Own copy, through `ka0s-bounded`. Logs in `port/work/mm-code/`.

| Run | Result |
|---|---|
| retail | 2657 passed, 0 failed, 3 skipped (`retail.txt`) |
| forever | **2612 passed, 45 failed**, 3 skipped (`forever.txt`) |
| forever, default skin forced to `ka0s` | only #1 below remains, plus two seam tests that assert the override is absent and one eol check the sed edit trips (`forever_ka0s.txt`) |
| retail, default skin forced to `forever` | the same 44 fail, plus those seam and eol artifacts (`retail_foreverskin.txt`) |
| TOC `120105, 16001`, retail | 2657 / 0, client-globals scan armed and clean (`retail_toc.txt`) |
| TOC `120105, 16001`, forever | same 45, scan clean (`forever_toc.txt`) |
| luacheck | 0 warnings / 0 errors, 195 files |

So 44 failures are one cause: fixtures that assume the default skin is Ka0s Default. None is a product bug. The two
cross-runs prove it in both directions.

The 45th (#1): the kit's loader applies the client profile **after** the test's `mutate`
(`tests/_kit/loader.lua:25`, `tests/run.lua:181`), and the Forever profile deletes `GetSpecialization` and
`GetSpecializationInfo`, wiping the globals the test had just installed.

Fixes: tests of Ka0s Default pixels select `ka0s` explicitly (an `afterLibs` option exists); the settings pin takes
`Skin:DefaultSkin()`; #1 installs its globals after load or runs its fallback half on retail only.

**The green cases prove little about Forever.** The profile changes project constants, build info and five globals. It
does not model a secret `specIconID`, two-return names, `RegionalUniqueNamesEnabled`, class-wide specs, or the
formatter refusal. All three critical defects pass today. Build a Forever mock first (as LH-02 and BL-02 did).

Causes: *skin token pixel* = a color, edge, shadow or texture of Ka0s Default; *font scale* = Forever's HUD scale;
*geometry from font scale* = a number derived from that size; *default value* = asserts the id `ka0s`.

| # | Test | Where | Failure | Cause |
|---|---|---|---|---|
| 1 | Compat: the spec shims prefer C_SpecializationInfo and fall back to the globals | tests/test_compat.lua:108 | assertEqual (expected 3, got nil) | mock ordering |
| 2 | An empty session says so rather than leaving a blank grid | tests/test_window.lua:389 | the title in gold | skin token pixel |
| 3 | The name column's formula is calibrated to the shipped width at a 20 cap | tests/test_window_layout.lua:114 | assertEqual (expected 118, got 114) | geometry from font scale |
| 4 | bodyWidth is the frame minus its padding, whatever the grid inside it costs | tests/test_window_layout.lua:337 | the fixture must make the two numbers distinguishable | geometry from font scale |
| 5 | Test mode: the strip is the marker; the red title word only when minimized | tests/test_window_header.lua:593 | and it must be red | skin token pixel |
| 6 | Column headers take their own font, not the cells' | tests/test_window_header.lua:710 | the header took the cell text size (expected 21, got 20.125) | font scale |
| 7 | Header ships GameFontNormal spelled out: 12px, flags From skin, a 1/-1 shadow | tests/test_window_header.lua:922 | the header line is not 12px (expected 12, got 11.5) | font scale |
| 8 | The window refuses to be dragged smaller than the grid needs | tests/test_window_placement.lua:169 | assertTrue failed | geometry from font scale |
| 9 | HeaderControls: a custom header height still centers the whole row | tests/test_headercontrols.lua:221 | bar 8, slot 10: the session line left the frame (expected 0, got 0.25) | geometry from font scale |
| 10 | HeaderControls: a control at rest takes the control color | tests/test_headercontrols.lua:287 | assertEqual (expected 0.7,0.7,0.72, got 0.63921568627451,0.61960784313725,0.5921568627451) | skin token pixel |
| 11 | HeaderControls: the shipped strip is DPS Race's: gray at rest, full strength | tests/test_headercontrols.lua:308 | close is not the rest gray (expected 0.7,0.7,0.72, got 0.63921568627451,0.61960784313725,0.5921568627451) | skin token pixel |
| 12 | HeaderControls: the control under the pointer takes the HOVER color | tests/test_headercontrols.lua:326 | assertEqual (expected 1,0.5,0, got 1,0.66666666666667,0.2) | skin token pixel |
| 13 | HeaderControls: both flags off is the shipped look, unchanged | tests/test_headercontrols.lua:406 | assertEqual (expected 0.7,0.7,0.72, got 0.63921568627451,0.61960784313725,0.5921568627451) | skin token pixel |
| 14 | HeaderControls: with the reveal off, hover is color alone | tests/test_headercontrols.lua:684 | assertEqual (expected 1,0.5,0, got 1,0.66666666666667,0.2) | skin token pixel |
| 15 | Every color mode falls back to one neutral, never to a fourth palette | tests/test_row.lua:440 | assertEqual (expected 0.45, got 0.78823529411765) | skin token pixel |
| 16 | A window that sets neither keeps the border it always had | tests/test_row.lua:723 | assertEqual (expected 0, got 0.28235294117647) | skin token pixel |
| 17 | The configured font reaches both number slots and the spell name | tests/test_tooltip.lua:224 | the amount slot did not take the configured size (expected 17, got 16.291666666667) | font scale |
| 18 | Every tooltip line we restyled is put back when the tooltip hides | tests/test_tooltip.lua:264 | the line never took our font to begin with | font scale |
| 19 | The font survives a UI skin that re-fonts every line on show | tests/test_tooltip.lua:345 | the skin's re-font on Show won — our pass runs too early (expected 17, got 16.291666666667) | font scale |
| 20 | The post-layout pass still restores every line it touched | tests/test_tooltip.lua:390 | the line never took our font (expected 19, got 18.208333333333) | font scale |
| 21 | The gap above a section is half the text size, not a whole blank line | tests/test_tooltip.lua:457 | the gap is not half the configured size (expected 10, got 9) | geometry from font scale |
| 22 | The half-size gap survives the post-layout pass | tests/test_tooltip.lua:477 | the gap was restored to full size by the re-apply (expected 10, got 9) | geometry from font scale |
| 23 | The gap is restored with every other line it was applied alongside | tests/test_tooltip.lua:501 | the gap never took the half size (expected 10, got 9) | geometry from font scale |
| 24 | The name's room is a FIXED span, not the length of the names on screen | tests/test_tooltip_lines.lua:953 | the reserved span is not 25 characters at the configured font (expected 271, got 265.79166666667) | geometry from font scale |
| 25 | Settings pin: the schema holds exactly the pinned rows, keys and defaults unchanged | tests/test_settings_pin.lua:289 | settings drifted. Pinned but gone: skin.skin\|string\|ka0s\|nil\|nil\|nil\|azeroth,contrast,ember,forever,glass,ka0s,midnight,obsidian,wow\|false\|f | default value |
| 26 | Skin seam: the read answers Ka0s Default before the profile store exists | tests/test_skinsetup.lua:84 | assertEqual (expected ka0s, got forever) | default value |
| 27 | Skin seam: every owner token is registered, namespaced mm., and keeps its pixel on Ka0s Default | tests/test_skinsetup.lua:139 | mm.skinSelfEdge[1]: Ka0s Default answers 0.78823529411765, not today's 1 | skin token pixel |
| 28 | Skin seam: the skin keys default to Ka0s Default, the panel ignored and the picker unseen | tests/test_skinsetup.lua:175 | assertEqual (expected ka0s, got forever) | default value |
| 29 | Skin seam: /mm set refuses a skin that is not registered and applies one that is | tests/test_skinsetup.lua:216 | an unknown skin was stored (expected ka0s, got forever) | default value |
| 30 | Skin seam: a profile switch applies the new profile's skin before the rebuild | tests/test_skinsetup.lua:291 | back on Default, Default's skin (expected ka0s, got forever) | default value |
| 31 | Skin outline: /mm set applies the mode live, its own half only | tests/test_skin_outline.lua:63 | the skin did not move (expected ka0s, got forever) | default value |
| 32 | Skin chrome: a Custom window keeps the player's fill and edge through the Shell | tests/test_skin_chrome.lua:65 | the inner rule is win.inner: channel 1 is 0, want 0.24 | skin token pixel |
| 33 | Skin chrome: the TEST MODE word and the restricted notes follow the skin | tests/test_skin_chrome.lua:93 | Ka0s Default keeps NS.GRAY's bytes (expected \|cff9d9d9d, got \|cffa39e97) | skin token pixel |
| 34 | Skin chrome: the export modal paints through the facade, its refusal in mm.warn | tests/test_skin_chrome.lua:118 | the refusal keeps its pixel: channel 2 is 0.3, want 0.25 | skin token pixel |
| 35 | Skin chrome: the rows keep their Ka0s Default pixels through the owner tokens | tests/test_skin_chrome.lua:172 | the stripe: channel 4 is 0.1, want 0.08 | skin token pixel |
| 36 | Skin chrome: the session line's escapes are cached on ApplyConfig, not read per refresh | tests/test_skin_chrome.lua:208 | the cached dim keeps NS.GRAY's bytes (expected \|cff9d9d9d, got \|cffa39e97) | skin token pixel |
| 37 | Skin flip: under Ka0s Default every surface draws what it drew before the flip | tests/test_skin_flip.lua:224 | a column label: channel 1 is 0.78823529411765, want 1 | skin token pixel |
| 38 | Skin flip: under Ka0s Default the header and the cells keep their shadow, the others none | tests/test_skin_flip.lua:240 | the owner token draws as the stored arm (expected false, got true) | skin token pixel |
| 39 | Swatches: a classless row's fill is mm.barNeutral, the old slate under Ka0s Default | tests/test_skin_swatches.lua:117 | Ka0s Default: channel 1 is 0.78823529411765, want 0.45 | skin token pixel |
| 40 | Swatches: degraded, a window has no fill looks, so every swatch draws as stored | tests/test_skin_swatches.lua:144 | the neutral keeps its pixel: channel 1 is 0.78823529411765, want 0.45 | skin token pixel |
| 41 | D4: Ka0s Default draws no stripe and no self edge with both settings off | tests/test_skin_fix.lua:480 | a stripe under Ka0s Default | skin token pixel |
| 42 | Skin fonts: the column labels draw the Font outline and the HUD size scale | tests/test_skin_fonts.lua:273 | Ka0s Default draws the stored size (expected 12, got 11.5) | font scale |
| 43 | Skin window: under Ka0s Default the window wears Ka0s Default's own chrome | tests/test_skin_window.lua:162 | Ka0s Default's win.bg moved: this case reads the wrong token | skin token pixel |
| 44 | Header band: the strip draws the skin's title gradient, and flat for a flat skin | tests/test_header_band.lua:186 | Ka0s Default's bottom stop: channel 1 is 0.019607843137255, want nil | skin token pixel |
| 45 | Skin tools: under Ka0s Default the tooltip lines keep their pixels | tests/test_skin_tools.lua:97 | the header's right half: channel 2 is 0.81960784313725, want 0.82 | skin token pixel |

---

## 8. Probes

Commands are for the owner; none was run in game.

| # | Question | Probe (Forever) | If it disagrees |
|---|---|---|---|
| P1 | Is `specIconID` secret out of combat? | after a fight: `/run local s=C_DamageMeter.GetCombatSessionFromType(0,0) local r=s.combatSources[1] print(issecretvalue(r.specIconID))` | nothing: class icon is still right |
| P2 | Is the row's `amountPerSecond` present, in and out of combat? | same, `print(issecretvalue(r.amountPerSecond) and "secret" or r.amountPerSecond)`; repeat mid-fight | nil: `smart` must show the total on Forever, or a rate derived out of combat |
| P3 | Does the abbreviate config take our ladder and a secret? | out of combat: `/run local c=CreateAbbreviateConfig({{breakpoint=1000,abbreviation="K",significandDivisor=100,fractionDivisor=10,abbreviationIsGlobal=false},{breakpoint=0.001,abbreviation="",significandDivisor=1,fractionDivisor=1,abbreviationIsGlobal=false}}) print(AbbreviateNumbers(69.5625,{config=c}),AbbreviateNumbers(47500,{config=c}))` expects `69 47.5K`; then in combat on a row's `amountPerSecond` | use FloorToNearestString (whole numbers) |
| P4 | Meter `name`, and EnemyDamageTaken `unitName` with two players | two-player fight, after it: `/run local s=C_DamageMeter.GetCombatSessionFromType(0,10) local e=s.combatSources[1] local d=C_DamageMeter.GetCombatSessionSourceFromType(0,10,nil,e.sourceCreatureID) for _,p in ipairs(d.combatSpells) do print(p.totalAmount,p.combatSpellDetails.unitName) end` and print `name` on DamageDone rows | no per-attacker rows: Targets absent on Forever. First-name-only `unitName`: match on GUID-resolved roster names |
| P5 | Are warlock pets, totems, guardians folded? | fight with each, print each DamageDone row's `name`, `classFilename`, `sourceDisplayType`, `sourceGUID` | all folded: `mergePets` absent on Forever |
| P6 | Does Avoidable ever fill? | stand in a boss's ground effect, then `GetCombatSessionFromType(0,8)` row count | empty: default the column off |
| P7 | Are group roles assigned? | in a party: `/dump UnitGroupRolesAssigned("party1")` | always NONE: role color and roster sort mean little |
| P8 | Recap event fields; feign as a death | `/mm debug` recap and feign reports after a death and a hunter feign | adapt the recap reader |
| P9 | Chat send in a dungeon after combat | Export to Party | state the refusal |
| P10 | Pet battle and glide events on Forever | none needed if declared Retail-only | - |
| P11 | Blizzard meter availability below max level, default CVar | `/dump C_DamageMeter.IsDamageMeterAvailable(), GetCVar("damageMeterEnabled")` | the notice already shows the reason |

---

## 9. Files near the 1500-line cap

| Lines | File | The port touches it? |
|---:|---|---|
| 1463 | `modules/Window_Header.lua` | avoid; 37 lines left |
| 1437 | `tests/test_aggregator.lua` | put identity cases in `test_aggregator_identity.lua` (844) |
| 1434 | `tests/test_tooltip_deaths.lua` | no |
| 1408 | `tests/test_export.lua` | CSV per-client test needs a new file |
| 1398 | `tests/wow_mock.lua` | **yes**: put the Forever shape in `tests/mock_forever.lua` |
| 1394 | `tests/test_schema.lua` | per-client absence tests need a new file |
| 1386 | `settings/Schema_Compose.lua` | avoid |
| 1379 | `tests/test_window_header.lua` | fixture fix only |
| 1343 | `modules/Aggregator.lua` | one line; put the rule in `Aggregator_Identity.lua` (667) |
| 1325 | `modules/Row.lua` | no; the icon change is `Row_NameCell.lua` (497) |
| 1324 | `tests/test_headercontrols.lua` | fixture fix only |
| 1289 | `modules/Tooltip.lua` | no |
| 1283 | `locales/enUS.lua` | yes, a few keys |
| 1242 | `tests/test_row.lua` | fixture fix |
| 1189 | `core/Database_Migrations.lua` | no migration needed |
| 1076 | `settings/Schema.lua` | descriptions |
| 993 | `modules/Export.lua` | yes |
| 896 | `core/Compat.lua` | a new `CompatClient.lua` keeps it small |
| 770 | `modules/Format.lua` | yes, room |

---

## 10. Suggested items

1. `CompatClient` (client helpers), SimSetup PURE.
2. Forever mock file: secret icon, surnames, regional names, class-wide spec, strict formatter. Red tests for 1.2-1.4.
3. Suite fixtures (45 failures).
4. Secret number text (both clients, own commit).
5. System-message guard (both clients, own commit).
6. Names: roster, strip, cap and width, export, descriptions.
7. Identity rule, class icon, CSV spec, diagnostics text.
8. Role through LibKa0s Role.
9. Per-client visibility rows, vetoes, events, companion and form seeds.
10. Test-mode and sim seeds.
11. 40-player perf scenario.
12. Shape: TOC `120105, 16001`, README, CLAUDE gate (both runs), `docs/forever-quirks.md`, ARCHITECTURE per-client table,
    data-flow, scope, compat-layer, testing, smoke with absence checks, test-cases; roster row in WowAddonStandards.

---

## Appendix A. Client surface inventory

Generated by `port/work/mm-code/inv.py` from the snapshot's `core`, `defaults`, `modules`, `settings` with comment lines
removed. A site is a line naming the symbol, so wrappers, stubs and seam lists appear beside the real call.
"API doc" = the generated docs of 71037, compared to 12.1.5's entry. "used at" = no doc or Lua definition (a C global);
Blizzard's Forever source references it. Every `C_DamageMeter` caller goes through `core/Compat.lua`.

### A.1 Functions, frames, globals, templates

| Name | MultiMeters sites | Forever evidence (71037) | Status | Forever need |
|---|---|---|---|---|
| `C_DamageMeter.IsDamageMeterAvailable` | core/Compat.lua:123,125,128; modules/Provider.lua:170 | API doc DamageMeterDocumentation.lua:113 (= live) | VERIFIED | none |
| `C_DamageMeter.GetCombatSessionFromType` | core/Compat.lua:137,139,140; modules/Provider.lua:137 | API doc DamageMeterDocumentation.lua:39 (= live); SecretWhenInCombat = true | VERIFIED | port; specIconID is SecretValue (report 1.1) |
| `C_DamageMeter.GetCombatSessionFromID` | core/Compat.lua:148,150,151; modules/Provider.lua:139 | API doc DamageMeterDocumentation.lua:21 (= live); SecretWhenInCombat = true | VERIFIED | port; specIconID is SecretValue (report 1.1) |
| `C_DamageMeter.GetCombatSessionSourceFromType` | core/Compat.lua:167,169,170; modules/Provider.lua:430,486,518 | API doc DamageMeterDocumentation.lua:77 (= live); SecretWhenInCombat = true | VERIFIED | port; specIconID is SecretValue (report 1.1) |
| `C_DamageMeter.GetCombatSessionSourceFromID` | core/Compat.lua:175,177,178; modules/Provider.lua:432,521 | API doc DamageMeterDocumentation.lua:57 (= live); SecretWhenInCombat = true | VERIFIED | port; specIconID is SecretValue (report 1.1) |
| `C_DamageMeter.GetAvailableCombatSessions` | core/Compat.lua:189,191,192; modules/Provider.lua:813,839,864 | API doc DamageMeterDocumentation.lua:11 (= live) | VERIFIED | none |
| `C_DamageMeter.GetSessionDurationSeconds` | core/Compat.lua:200,202,203; modules/Provider.lua:836 | API doc DamageMeterDocumentation.lua:97 (= live) | VERIFIED | none |
| `C_DamageMeter.ResetAllCombatSessions` | core/Compat.lua:211,213,214; modules/Provider.lua:896 | API doc DamageMeterDocumentation.lua:124 (= live) | VERIFIED | none |
| `C_DeathRecap.GetRecapEvents` | core/Compat.lua:260,288,290,291,362,367; modules/Provider.lua:982 | API doc DeathRecapDocumentation.lua:11 (= live) | VERIFIED | none |
| `C_DeathRecap.HasRecapEvents` | core/Compat.lua:272,274,275; modules/Provider.lua:977 | API doc DeathRecapDocumentation.lua:57 (= live) | VERIFIED | none |
| `C_DeathRecap.GetRecapMaxHealth` | core/Compat.lua:300,302,303,363; modules/Provider.lua:992 | API doc DeathRecapDocumentation.lua:41 (= live) | VERIFIED | none |
| `C_RestrictedActions.IsAddOnRestrictionActive` | core/Secrets.lua:115,116 | API doc RestrictedActionsDocumentation.lua:55 (= live) | VERIFIED | none |
| `C_RestrictedActions.GetAddOnRestrictionState` | core/Secrets.lua:134,135 | API doc RestrictedActionsDocumentation.lua:29 (= live) | VERIFIED | none |
| `C_StringUtil.CreateAbbreviatedNumberFormatter` | core/Compat.lua:525,527,528; core/Diagnostics.lua:288,289; modules/Format.lua:427 | API doc StringUtilDocumentation.lua:11 (= live) | VERIFIED | adapt: FormatNumber refuses secrets (1.3) |
| `C_StringUtil.CreateNumericRuleFormatter` | core/Compat.lua:555,557,558; modules/Format.lua:458 | API doc StringUtilDocumentation.lua:21 (= live) | VERIFIED | adapt: FormatNumber refuses secrets (1.3) |
| `C_StringUtil.GetDefaultAbbreviationBreakpoints` | core/Compat.lua:539,541,542; core/Diagnostics.lua:290,291; modules/Format.lua:363 | API doc LocalizationDocumentation.lua:107 (namespace C_StringUtil) | VERIFIED | none |
| `C_Texture.GetAtlasInfo` | core/Compat.lua:657,659; core/Diagnostics.lua:272,273,277 | API doc TextureUtilsDocumentation.lua:75 (= live) | VERIFIED | none |
| `C_PartyInfo.IsDelveInProgress` | core/Compat.lua:697 | API doc PartyInfoDocumentation.lua:411 (= live) | VERIFIED | absent: delve probe Retail-only (3) |
| `C_DelvesUI.HasActiveDelve` | core/Compat.lua:709,712 | API doc DelvesUIDocumentation.lua:373 (= live) | VERIFIED | absent: delve probe Retail-only (3) |
| `C_Map.GetBestMapForUnit` | core/Compat.lua:711 | API doc MapDocumentation.lua:49 (= live) | VERIFIED | absent: delve probe Retail-only (3) |
| `C_PlayerInfo.GetGlidingInfo` | core/Compat.lua:729,730 | API doc PlayerInfoDocumentation.lua:103 (= live) | VERIFIED | absent: skyriding Retail-only (3) |
| `C_Housing.IsInsideHouseOrPlot` | core/Compat.lua:738,739 | API doc HousingUIDocumentation.lua:316 (= live) | VERIFIED | absent: housing Retail-only (3) |
| `C_PetBattles.IsInBattle` | modules/Visibility.lua:191,192 | used at Blizzard_PTRFeedback/Blizzard_PTRFeedback_Tooltips.lua:101 | INFERRED (Blizzard references it) | absent: pet battles Retail-only (3) |
| `C_ChatInfo.SendChatMessage` | core/Compat.lua:894,895 | API doc ChatInfoDocumentation.lua:564 (= live) | VERIFIED | none |
| `C_AddOns.GetAddOnMetadata` | core/EnvSetup.lua:97,98,99 | API doc AddOnsDocumentation.lua:165 (= live) | VERIFIED | none |
| `C_Timer.After` | core/SimSetup.lua:73,124; core/SkinSetup.lua:678,680; modules/Export.lua:959; modules/SimDrivers.lua:166; settings/OptionsSetup.lua:263 | API doc UITimerDocumentation.lua:11 (= live) | VERIFIED | none |
| `C_Spell.GetSpellInfo` | core/Compat.lua:78; core/SimSetup.lua:49; modules/DrillDown.lua:531,532; modules/Tooltip_Lines.lua:702,703 | API doc SpellDocumentation.lua:416 (= live) | VERIFIED | none |
| `C_Spell.GetSpellTexture` | core/Compat.lua:79; core/SimSetup.lua:49; modules/Tooltip_Builders.lua:141,142 | API doc SpellDocumentation.lua:595 (= live) | VERIFIED | none |
| `C_SpecializationInfo.GetSpecialization` | core/Compat.lua:80; core/SimSetup.lua:50; modules/Roster.lua:263; modules/Sim.lua:199 | API doc SpecializationInfoDocumentation.lua:237 (= live) | VERIFIED | adapt: Role.Resolve; spec role is class-wide (1.5) |
| `C_SpecializationInfo.GetSpecializationInfo` | core/Compat.lua:81; core/SimSetup.lua:50 | API doc SpecializationInfoDocumentation.lua:254 (= live) | VERIFIED | none |
| `UnitGUID` | core/Compat.lua:761,762; core/MultiMeters.lua:493; modules/Roster.lua:233; modules/Sim.lua:201; modules/SimWorld.lua:567 | API doc UnitDocumentation.lua:1241 (= live); SecretWhenUnitIdentityRestricted = true | VERIFIED | none |
| `UnitName` | core/Compat.lua:770,771; modules/Export.lua:629; modules/Roster.lua:234; modules/Sim.lua:201; modules/SimWorld.lua:568 | API doc UnitDocumentation.lua:2489 (= live); SecretWhenUnitNameIdentityRestricted = true | VERIFIED | adapt: UnitCharacterName (1.4) |
| `GetUnitName` | modules/Export.lua:626 | Blizzard_UnitFrame/Mainline/UnitFrame.lua:1094 | VERIFIED | none: already the whole name |
| `UnitExists` | core/Compat.lua:779,780; modules/Export.lua:616; modules/Roster.lua:235; modules/SimWorld.lua:575 | API doc UnitDocumentation.lua:1192 (= live) | VERIFIED | none |
| `UnitClass` | core/Compat.lua:786,787; core/CoreSetup.lua:213,265; modules/Roster.lua:238; modules/Sim.lua:198; modules/SimWorld.lua:576 | API doc UnitDocumentation.lua:911 (= live); SecretWhenUnitIdentityRestricted = true | VERIFIED | none |
| `UnitGroupRolesAssigned` | core/Compat.lua:794,795; modules/Roster.lua:256; modules/SimWorld.lua:582 | API doc UnitDocumentation.lua:1318 (= live); SecretWhenUnitIdentityRestricted = true | VERIFIED | none |
| `GetSpecializationRole` | core/Compat.lua:804,805; core/SimSetup.lua:50; modules/Roster.lua:264; modules/Sim.lua:200 | used at Blizzard_SharedXML/UnitUtil.lua:117 | INFERRED (Blizzard references it) | adapt: Role.Resolve; spec role is class-wide (1.5) |
| `GetNumGroupMembers` | core/Compat.lua:811,812; modules/Roster.lua:285; modules/SimWorld.lua:587 | used at Blizzard_PlunderstormPrematchUI/Blizzard_PlunderstormPrematchUI.lua:239 | INFERRED (Blizzard references it) | none |
| `IsInRaid` | core/Compat.lua:817,818; modules/Roster.lua:302,526; modules/SimWorld.lua:588 | used at Blizzard_GamepadTargeting/RaidPartyTargeting/RaidTargetDPAD.lua:33 | INFERRED (Blizzard references it) | none |
| `IsInGroup` | core/Compat.lua:824,825; core/Diagnostics.lua:424; core/Diagnostics_Runtime.lua:210; modules/Sim.lua:111,143; modules/SimWorld.lua:589; modules/Visibility.lua:131 | used at Blizzard_GamepadTargeting/RaidPartyTargeting/RaidTargetDPAD.lua:34 | INFERRED (Blizzard references it) | none |
| `IsInInstance` | core/Compat.lua:831,832; core/Diagnostics.lua:416; core/Diagnostics_Runtime.lua:207; modules/Export.lua:741; modules/Sim.lua:108,145; modules/SimWorld.lua:590; modules/Visibility.lua:112 | API doc InstanceDocumentation.lua:170 (= live) | VERIFIED | none |
| `GetInstanceInfo` | core/Compat.lua:701,702 | API doc InstanceDocumentation.lua:103 (= live) | VERIFIED | absent: delve probe Retail-only (3) |
| `UnitAffectingCombat` | core/Compat.lua:841,842; core/MultiMeters.lua:616; modules/Sim.lua:103; modules/SimWorld.lua:592; modules/Tooltip.lua:700; modules/Visibility.lua:153; modules/WindowManager.lua:655 | API doc UnitDocumentation.lua:614 (= live) | VERIFIED | none |
| `UnitInVehicle` | modules/Visibility.lua:124,125 | API doc UnitDocumentation.lua:1733 (= live) | VERIFIED | none |
| `IsMounted` | modules/Visibility.lua:173 | API doc PlayerScriptDocumentation.lua:1399 (= live) | VERIFIED | none |
| `GetShapeshiftFormID` | modules/Visibility.lua:174 | used at Blizzard_SharedXMLBase/ModelSceneUtil.lua:23 | INFERRED (Blizzard references it) | adapt: forms 3 and 4 only on Forever (3) |
| `UnitOnTaxi` | modules/Visibility.lua:183,184 | API doc UnitDocumentation.lua:2570 (= live) | VERIFIED | none |
| `UnitIsDeadOrGhost` | modules/Visibility.lua:198,199 | API doc UnitDocumentation.lua:1931 (= live) | VERIFIED | none |
| `UnitIsDead` | core/Diagnostics_Feign.lua:224 | API doc UnitDocumentation.lua:1916 (= live) | VERIFIED | none |
| `UnitIsFeignDeath` | core/Diagnostics_Feign.lua:225; modules/Feign.lua:131 | API doc UnitDocumentation.lua:1962 (= live) | VERIFIED | none |
| `UnitHealth` | core/Diagnostics_Feign.lua:223; modules/Feign.lua:93 | API doc UnitDocumentation.lua:1526 (= live); SecretReturns = true | VERIFIED | none |
| `UnitIsPlayer` | modules/Export.lua:621 | API doc UnitDocumentation.lua:2271 (= live) | VERIFIED | none |
| `InCombatLockdown` | core/MultiMeters.lua:342; core/Secrets.lua:119; core/SkinSetup.lua:642; modules/Sim.lua:102; modules/Window_Render.lua:210; settings/Columns.lua:114 | used at Blizzard_APIDocumentationGenerated/RestrictedActionsDocumentation.lua:45 | INFERRED (Blizzard references it) | none |
| `issecretvalue` | core/Secrets.lua:170 | API doc FrameScriptDocumentation.lua:287 (= live) | VERIFIED | none |
| `canaccessvalue` | core/Secrets.lua:186 | API doc FrameScriptDocumentation.lua:65 (= live) | VERIFIED | none |
| `issecrettable` | core/Secrets.lua:280 | API doc FrameScriptDocumentation.lua:270 (= live) | VERIFIED | none |
| `canaccesstable` | core/Secrets.lua:296 | API doc FrameScriptDocumentation.lua:48 (= live) | VERIFIED | none |
| `AbbreviateNumbers` | modules/Format.lua:541 | API doc LocalizationDocumentation.lua:26 (= live) | VERIFIED | adapt: pass a ladder config for secrets (1.3) |
| `Ambiguate` | modules/Targets.lua:178 | API doc PlayerScriptDocumentation.lua:22 (= live) | VERIFIED | none if both operands are whole names (1.4) |
| `GetTime` | core/Diagnostics_Runtime.lua:324; modules/Aggregator.lua:1164 | API doc SystemTimeDocumentation.lua:57 (= live) | VERIFIED | none |
| `debugprofilestop` | core/MultiMeters.lua:523,525,532,534,569,571,579,581,586,589; modules/Aggregator.lua:1229,1264; modules/DrillDown.lua:703,710,722; modules/Provider.lua:355,375; modules/Row.lua:1215,1256; modules/Targets.lua:439,443; modules/Tooltip_Builders.lua:752,798,926,943,961,993,1023,1037,1051; modules/Window_Render.lua:315,320,330,353,360,483,530 | API doc FrameScriptDocumentation.lua:533 (= live) | VERIFIED | none |
| `OpenDeathRecapUI` | core/Compat.lua:850 | Blizzard_DeathRecap/Mainline/Blizzard_DeathRecap_Bootstrap.lua:7 | VERIFIED | none |
| `SendChatMessage` | core/Compat.lua:894,895 | Blizzard_DeprecatedChatInfo/Deprecated_ChatInfo.lua:8 | VERIFIED | none |
| `CreateFrame` | core/LauncherSetup.lua:153; modules/Export_Modal.lua:172,195,248,707,746,758; modules/HeaderControls.lua:643; modules/Row.lua:593,1097,1135; modules/Tooltip_Lines.lua:91,99,187; modules/Window_Frame.lua:163,243,251,275,281,361,373; modules/Window_Header.lua:585,1175; modules/Window_Render.lua:448; settings/ColumnBlocks.lua:121,157,162 | used at Blizzard_APIDocumentationGenerated/PingManagerSecureDocumentation.lua:16 | INFERRED (Blizzard references it) | none |
| `CreateColor` | modules/Window_Header.lua:243,266 | Blizzard_SharedXMLBase/Color.lua:3 | VERIFIED | none |
| `StaticPopup_Show` | modules/HeaderControls.lua:458; settings/General.lua:104,177; settings/Windows.lua:457 | Blizzard_StaticPopup/StaticPopup.lua:309 | VERIFIED | none |
| `StaticPopupDialogs` | settings/General.lua:82,136; settings/Windows.lua:366 | Blizzard_StaticPopup/StaticPopup.lua:21 | VERIFIED | none |
| `UISpecialFrames` | modules/Export_Modal.lua:857,858 | Blizzard_UIParentPanelManager/Shared/UIParentPanelManager.lua:21 | VERIFIED | none |
| `UIParent` | core/LauncherSetup.lua:153; modules/Export_Modal.lua:314,707; modules/Tooltip.lua:568,609; modules/Window_Frame.lua:243,251; modules/Window_Placement.lua:68; settings/ColumnBlocks.lua:121; settings/General.lua:181,183 | used at Blizzard_APIDocumentationGenerated/UIManagerDocumentation.lua:71 | INFERRED (Blizzard references it) | none |
| `GameTooltip` | modules/Tooltip.lua:566,586,587,631,633,635,651,660,698,710,711,719,721,724,729,732,1069,1070,1071,1163,1164,1169,1170,1175,1176,1200,1220; modules/Tooltip_Builders.lua:255,257,435,444,450,526,551,561,585,615,666,675,677,694,695,764,778,789,905,936,939,947,948,953,956,1018,1030,1031,1033,1044,1045; modules/Tooltip_Lines.lua:73,91,378,379,389,394,594,638,729,736; settings/ColumnBlocks.lua:183,185,186,188,189,190,191,195 | Blizzard_GameTooltip/Mainline/GameTooltip.xml:249 | VERIFIED | none |
| `GameTooltipText` | modules/Tooltip.lua:1121,1122; modules/Tooltip_Lines.lua:108,126,130,150,154 | Blizzard_Fonts_Shared/Shared/FontStyles.xml:317 | VERIFIED | none |
| `DEFAULT_CHAT_FRAME` | core/CoreSetup.lua:160,163,166 | Blizzard_ChatFrameBase/Shared/ChatFrameUtil.lua:19 | VERIFIED | none |
| `MenuUtil` | core/Compat.lua:587 | Blizzard_Deprecated/Mainline/Deprecated_12_0_7.lua:8 | VERIFIED | none |
| `Settings` | settings/General.lua:193,281; settings/OptionsSetup.lua:663,667; settings/Profiles.lua:61,134; settings/Windows.lua:428,497,515 | Blizzard_SettingsDefinitions_Frame/Mainline/ColorblindOverrides.lua:177 | VERIFIED | none |
| `RAID_CLASS_COLORS` | core/Diagnostics.lua:604; core/Namespace.lua:70; modules/Aggregator.lua:663; modules/Tooltip.lua:250; modules/Tooltip_Builders.lua:712,1015 | Blizzard_SharedXML/ClassColors.lua:1 | VERIFIED | none |
| `CLASS_ICON_TCOORDS` | modules/Row_NameCell.lua:423 | Blizzard_SharedXML/SharedConstants.lua:27 | VERIFIED | port; becomes the only unit icon on Forever |
| `STANDARD_TEXT_FONT` | core/Constants.lua:53; core/SkinSetup.lua:772,801; modules/Row.lua:378; modules/Tooltip.lua:366; modules/Window.lua:125 | no hit in UI source | UNKNOWN: /dump STANDARD_TEXT_FONT | none (only a fallback behind the shipped face) |
| `ERR_CHAT_PLAYER_NOT_FOUND_S` | modules/Export.lua:803 | used at Blizzard_ChatFrameBase/Mainline/ChatFrameOverrides.lua:398 | INFERRED (Blizzard references it) | none; same string |
| `BackdropTemplate` | modules/Export_Modal.lua:248,707,746; modules/Row.lua:593; modules/Tooltip_Lines.lua:91,99; modules/Window_Frame.lua:251 | Blizzard_SharedXML/Backdrop.xml:5 | VERIFIED | none |
| `GameFontNormal` | modules/Export_Modal.lua:204; modules/Window_Frame.lua:316; settings/ColumnBlocks.lua:199 | Blizzard_Fonts_Shared/Shared/FontStyles.xml:50 | VERIFIED | none |
| `GameFontNormalLarge` | modules/Window_Render.lua:451 | Blizzard_Fonts_Shared/Shared/FontStyles.xml:172 | VERIFIED | none |
| `GameFontNormalSmall` | modules/Export_Modal.lua:776 | Blizzard_Fonts_Shared/Shared/FontStyles.xml:56 | VERIFIED | none |
| `GameFontHighlightSmall` | modules/Export_Modal.lua:266,754,763; modules/Window_Render.lua:453 | Blizzard_Fonts_Shared/Shared/FontStyles.xml:92 | VERIFIED | none |
| `date` | modules/Format.lua:737 | used at Blizzard_ScriptErrorsFrame/Blizzard_ScriptErrorsFrame.lua:152 | INFERRED (Blizzard references it) | none |
| `time` | modules/Format.lua:702 | used at Blizzard_ScriptErrorsFrame/Blizzard_ScriptErrorsFrame.lua:137 | INFERRED (Blizzard references it) | none |
| `strtrim` | settings/Windows.lua:317 | Blizzard_SharedXMLBase/Compat.lua:60 | VERIFIED | none |

### A.2 Events

| Event | Sites | Forever evidence | Status | Forever need |
|---|---|---|---|---|
| `PLAYER_ENTERING_WORLD` | core/MultiMeters.lua:134,347; modules/Sim.lua:173; modules/SimDrivers.lua:63; modules/SimScenario.lua:82 | SystemDocumentation.lua:134 (= live) | VERIFIED | none |
| `GROUP_ROSTER_UPDATE` | core/MultiMeters.lua:135,359; modules/Sim.lua:174; modules/SimDrivers.lua:46,54; modules/SimScenario.lua:72 | PartyInfoDocumentation.lua:678 (= live) | VERIFIED | none |
| `ZONE_CHANGED_NEW_AREA` | core/MultiMeters.lua:136,368; modules/Sim.lua:175; modules/SimDrivers.lua:64; modules/SimScenario.lua:82 | MapDocumentation.lua:663 (= live) | VERIFIED | none |
| `ADDON_RESTRICTION_STATE_CHANGED` | core/MultiMeters.lua:143,548; modules/Sim.lua:172 | RestrictedActionsDocumentation.lua:97 (= live) | VERIFIED | none |
| `PLAYER_REGEN_DISABLED` | core/MultiMeters.lua:156,419; modules/Sim.lua:171; modules/SimDrivers.lua:111; modules/SimScenario.lua:102 | UnitDocumentation.lua:3885 (= live) | VERIFIED | none |
| `PLAYER_REGEN_ENABLED` | core/MultiMeters.lua:157,422; modules/SimDrivers.lua:123; modules/SimScenario.lua:103 | UnitDocumentation.lua:3891 (= live) | VERIFIED | none |
| `PLAYER_MOUNT_DISPLAY_CHANGED` | core/MultiMeters.lua:159 | UnitDocumentation.lua:3859 (= live) | VERIFIED | none |
| `UNIT_ENTERED_VEHICLE` | core/MultiMeters.lua:165,376 | VehicleDocumentation.lua:36 (= live) | VERIFIED | none |
| `UNIT_EXITED_VEHICLE` | core/MultiMeters.lua:166,377 | VehicleDocumentation.lua:68 (= live) | VERIFIED | none |
| `UPDATE_SHAPESHIFT_FORM` | core/MultiMeters.lua:167 | SpellBookDocumentation.lua:990 (= live) | VERIFIED | none |
| `PLAYER_CAN_GLIDE_CHANGED` | core/MultiMeters.lua:168 | UnitDocumentation.lua:3748 (= live) | VERIFIED | absent: register Retail-only (3) |
| `PET_BATTLE_OPENING_START` | core/MultiMeters.lua:169 | BattlePetDocumentation.lua:138 (= live) | VERIFIED | absent: register Retail-only (3) |
| `PET_BATTLE_CLOSE` | core/MultiMeters.lua:170 | BattlePetDocumentation.lua:80 (= live) | VERIFIED | absent: register Retail-only (3) |
| `PLAYER_DEAD` | core/MultiMeters.lua:171 | DeathInfoDocumentation.lua:129 (= live) | VERIFIED | none |
| `PLAYER_ALIVE` | core/MultiMeters.lua:172 | DeathInfoDocumentation.lua:123 (= live) | VERIFIED | none |
| `PLAYER_UNGHOST` | core/MultiMeters.lua:173 | DeathInfoDocumentation.lua:145 (= live) | VERIFIED | none |
| `PLAYER_IS_GLIDING_CHANGED` | core/MultiMeters.lua:181 | UnitDocumentation.lua:3802 (= live) | VERIFIED | absent: register Retail-only (3) |
| `UNIT_SPELLCAST_SUCCEEDED` | core/MultiMeters.lua:187 | UnitDocumentation.lua:4845 (= live) SecretWhenUnitSpellCastRestricted = true | VERIFIED | none: spellID already gated |
| `CHAT_MSG_SYSTEM` | core/MultiMeters.lua:194 | ChatInfoDocumentation.lua:2452 (= live) SecretInChatMessagingLockdown = true | VERIFIED | guard the secret message (4.6) |
| `DAMAGE_METER_CURRENT_SESSION_UPDATED` | core/MultiMeters.lua:197; modules/Sim.lua:176; modules/SimDrivers.lua:99,130; modules/SimScenario.lua:102 | DamageMeterDocumentation.lua:144 (= live) | VERIFIED | none |
| `DAMAGE_METER_COMBAT_SESSION_UPDATED` | core/MultiMeters.lua:198; modules/Sim.lua:177; modules/SimDrivers.lua:127; modules/SimScenario.lua:103 | DamageMeterDocumentation.lua:133 (= live) | VERIFIED | none |
| `DAMAGE_METER_RESET` | core/MultiMeters.lua:199; core/SimSetup.lua:73; modules/Sim.lua:178,224; modules/SimScenario.lua:110 | DamageMeterDocumentation.lua:150 (= live) | VERIFIED | none |

### A.3 Enums

| Enum | Sites | Forever evidence | Status | Need |
|---|---|---|---|---|
| `Enum.DamageMeterType` | core/Constants.lua:124,125,126,127,128,129,130,131,132 | DamageMeterConstantsDocumentation.lua:95 (= live) | VERIFIED | none |
| `Enum.DamageMeterSessionType` | core/Constants.lua:139,140,141 | DamageMeterConstantsDocumentation.lua:35 (= live) | VERIFIED | none |
| `Enum.DamageMeterSourceDisplayType` | core/Constants.lua:156,157,158 | DamageMeterConstantsDocumentation.lua:48 (= live) | VERIFIED | none |
| `Enum.AddOnRestrictionType` | core/Secrets.lua:86 | RestrictedActionsConstantsDocumentation.lua:19 (= live) | VERIFIED | none |
| `Enum.AddOnRestrictionState` | core/Secrets.lua:91 | RestrictedActionsConstantsDocumentation.lua:6 (= live) | VERIFIED | none |
| `Enum.StatusBarInterpolation` | core/Compat.lua:868 | SimpleStatusBarConstantsDocumentation.lua:20 (= live) | VERIFIED | none |

### A.4 CVars, Blizzard frames, other

| Kind | Finding |
|---|---|
| CVars | none read or written (grep `GetCVar`, `SetCVar`, `C_CVar`) |
| Blizzard frames | `UIParent`, `GameTooltip`, `DEFAULT_CHAT_FRAME`, `UISpecialFrames`, `StaticPopup`, the Settings canvas, the death recap through its opener. No hooks (`hooksecurefunc`), no Edit Mode, no meter-frame access |
| Project globals | no `WOW_PROJECT_*` and no `GetBuildInfo` read in shipped code |
| Client-globals scan | clean with the Forever TOC number (section 7) |
