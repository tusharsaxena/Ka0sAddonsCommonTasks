# R6-scoping: issues #76, #83, #85, #87, #91

Read-only research, 2026-11-16. LibKa0s master `9bc9cc51` (v1.104.0), standard v2.112.2. Every repo was read
from its default branch.

**Collection fact that matters for the whole run.** `SkillMaster` and `CombatTrail` have the default branch
**`main`** (`git -C SkillMaster branch -a` shows `* main` and `remotes/origin/main` only; the same for CombatTrail).
Ka0sAddonsCommonTasks `CLAUDE.md` says every collection repo is on `master`. Any executor script that hard-codes
`master` will break on these two, so detect the branch per repo. CombatTrail is **not** in `ADDONS.md`, but it is
the only code consumer of `LibKa0s-Callout-1.0` (see #85), so the run has to decide whether to re-vendor it.

---

## #76 Ace3: move from the pinned master commit to a tagged release

### Upstream state (gh api, 2026-11-16)

| Fact | Value |
|---|---|
| Newest tag | `Release-r1403` → `d295b12f` ("Update changelog", 2026-08-12) |
| Previous tags | r1390 `17db0bc6`, r1377 `9268883c`, r1349, r1341, ... |
| GitHub Releases objects | **0** (`gh api repos/WoWUIDev/Ace3/releases --jq length` → 0); Ace3 publishes tags only |
| Pinned commit | `ac3d1225` (2026-10-28, "AceDB-3.0: Recognize RP-PVP for Forever realms") |
| `compare ac3d1225...Release-r1403` | `status=behind, ahead_by=0, behind_by=21`: r1403 is an **ancestor** of the pin and lacks 21 commits, the Forever fixes among them |
| `compare ac3d1225...master` | `identical`: **the pin is still Ace3's master HEAD** |
| Last commits on master | `ac3d1225` 10-28, `5a934499` 10-21 (AceDB surname nil), `94392c42` 10-21 (Bump toc) |

**No tagged release contains ac3d1225.** The issue's trigger has not fired.

### Where Ace3 is vendored

Each addon vendors it under its own `libs/`. LibKa0s does not: its payload `LibKa0s/` has no Ace folders, and
its README:11 says addons "vendor it the way they vendor Ace3". The testkit fakes Ace (`testkit/mock_ace.lua`,
`testkit/README.md:28`), so a LibKa0s change never moves Ace3.

All 18 roster addons and CombatTrail carry **byte-identical** Ace trees (git tree hashes from `ls-tree`):
AceAddon `a08582`, AceConfig `a1afa7`, AceConsole `a8118d`, AceDB `426ad7`, AceDBOptions `2dafad`, AceEvent
`d7cc21`, AceGUI `7e5b68`, AceTimer `06ccb6`, CallbackHandler `13fa4f`, LibStub `861a1b`. The folders differ only
in which libs are present: ConsumableMaster, KickCD and PGFE have no AceTimer, and PrettyChat has no AceEvent,
AceTimer or LibSharedMedia. Spot check (AbsorbTracker): `libs/AceDB-3.0/AceDB-3.0.lua:44` `ACEDB_MINOR = 40`,
CheckBox `Version = 27`. Each addon's `DEPENDENCIES.md` records the provenance line
`Ace3: WoWUIDev/Ace3@ac3d1225 (untagged master; LibKa0s#76).` For example: AbsorbTracker:259, AuraMaster:120,
BankLedger:28, ConsumableMaster:26 (in a table cell), WhatGroup:24 (in a table cell), LootHistory:31 (not
indented). CombatTrail's `DEPENDENCIES.md:20` mentions Ace3 with no commit pin.

### Library code needed
None. This is addon-side vendoring and provenance only.

### Fits this run?
**No. It is blocked upstream.** There is no tag to move to, and the vendored code already equals Ace3's master
HEAD, so a re-copy would change nothing.

### Recommendation
- **Decision: defer #76 and leave it open, `state:triaged`.** Add a comment with today's evidence: newest tag
  r1403 is 21 commits behind the pin, and the pin equals master HEAD.
- Optional cheap item in this run: add CombatTrail's missing pin line to its `DEPENDENCIES.md`. Do it only if
  CombatTrail is in scope.
- When a tag ships, the plan is the issue's own: copy the tag into every `libs/Ace*`, check that AceDB's MINOR
  and profile-key code (the Forever ruleset+surname keys) did not change, update the provenance line in each
  `DEPENDENCIES.md`, run both kit profiles, then an owner smoke on both clients.
- **Risk:** the provenance line is formatted three ways (indented, in a table cell, not indented), so a sed-based
  bulk update has to handle all three.

---

## #83 FTUX: shared guided tour + key-settings setup

### What exists
There is no tour, coach-mark, highlight-overlay or first-run module in LibKa0s. `grep -i 'first.?run|seen'` over
`LibKa0s/*.lua` finds only unrelated locals. The pieces it could build on:
- Schema rows: `LibKa0s-Schema-1.0` minor 3 (`Schema.lua:44`), with `lib.Read/Write` at `Schema.lua:120,138`. The
  "write through the normal settings path" would go through these.
- Options widgets: `LibKa0s-Options-1.0` minor 38 (`Options.lua:52`), with the row renderers spread over
  `OptionsWidgets.lua`, `OptionsCompose.lua` and so on.
- Window chrome: `LibKa0s-Widgets-1.0` minor 27 (the v1.103.0 Footer and strip docking); Skin minor 18 and SkinPaint
  for theming.
- `LibKa0s-Slash-1.0` minor 23 for a `tour` verb.
- Size references: Toast.lua 725 lines; Callout.lua 1283 + CalloutSettings.lua 917.

### Sizing
A new major (`LibKa0s-Tour-1.0`, or `-Ftux-1.0`) needs:
- a step window with Back/Next/Skip;
- a highlight overlay for an arbitrary frame or region, which must clamp to the screen and survive a hidden or
  absent target;
- a key-settings page that renders a subset of the addon's schema rows with the Options renderers, inside a
  non-panel host;
- a first-run flag plus a "seen version" in the addon's SV;
- combat deferral (the settings-panel pattern);
- a slash verb, a panel button, skin and locale plumbing;
- docs/api + members JSON, kit tests, a CONSUMERS row and a standard ripple (most likely a new options-ui or
  launcher subsection).

Estimate: **about 1,200 to 1,800 Lua lines across 2-3 files, plus 300-500 lines of tests.** That is one
milestone on the scale of the Callout run (Callout took several releases, v1.96 → v1.102, with owner smoke at
each). The hard parts are rendering schema rows outside the Options panel (probably needs a new Options entry
point) and keeping the highlight stable across skins and UI scales.

### Open design questions (to grill the owner on)
1. Key settings: **a `key = true` flag on schema rows** (one source of truth, recommended) or a list of ids passed
   to `Tour:New`? The flag is a Schema minor bump plus an audit rule. The list is simpler but can drift from the
   schema.
2. Combat/lockdown: defer as the panel and toasts do? Recommend **yes**: never open in combat, and close plus
   resume on `PLAYER_REGEN_ENABLED`.
3. "What's new" replay after a major version? Recommend **first-run only in v1**, but store `seenVersion` so a
   later minor can add it without a SV migration.
4. A standard rule making it mandatory for every roster addon? Recommend **SHOULD, not MUST, until two consumers
   exist**. Under library-stack-§7 bar 1 a new major needs two consumers, or an owner ruling to enter with one
   (`library-stack.md:324-334`).
5. Reference consumer: QuickComms, as the issue suggests, or a smaller addon?
6. Forever: highlight targets must exist on both clients (the `build-for-retail-and-forever` ruling), so a step
   that points at a Retail-only frame needs a per-client target or a skip.

### Fits this run?
**No. Brainstorm first, build it in its own run.** It is new product surface with at least five unsettled design
calls. It has no consumer yet and it is `state:untriaged`. It is not a library fix and not a re-vendor. Putting it
into a run whose deliverable is "build library changes, re-vendor, fix fallout, defer adoption" would make it the
critical path.

### Recommendation
- **Decision: out of scope for this run.** Record it in the plan as a planned follow-on bundle with its own spec,
  produced by brainstorming. If the owner wants it in, it should be the last library milestone, so every other
  issue can be re-vendored without waiting for it.
- If it is kept in, the minimum viable v1 is: steps (title, body, optional highlight), the key-settings page drawn
  from a schema-row flag, first-run plus a `tour` verb, and no panel button or "what's new".

---

## #85 Callout consumers beyond Combat Trail

### What exists
`LibKa0s-Callout-1.0` is **already shipped**: `Callout.lua:78` MINOR 4, settings shell
`CalloutSettings.lua:94` `SETTINGS_MINOR = 5`, with docs `docs/api/Callout/version-4.5-docs.md` and
`members-4.5.json`. `CONSUMERS.md:82-89` records it as built for Combat Trail with a one-consumer ruling from the
owner. LibKa0s commit `263de083` reads "the owner keeps the Callout in LibKa0s and relaxes library-stack-§7
bar 1".

Code consumers (`git grep 'LibKa0s-Callout|LibKa0s-Toast'` outside `libs/`, `tests/_kit` and docs):
- **Callout:** CombatTrail only (`core/CalloutSetup.lua`, `modules/Countdown.lua`, `settings/Race.lua`,
  `tests/test_callout_settings.lua`).
- **Toast:** DpsRace (`core/ToastSetup.lua`, `modules/BestToast.lua`), DropWatcher (`core/ToastSetup.lua`,
  `modules/Toast.lua`), QuickComms (`core/ToastSetup.lua`, `modules/AutoThank_Toast.lua`), SkillMaster
  (`modules/Alerts.lua:26`) and CombatTrail (`modules/BestToast.lua`).

Candidates found:
- **DpsRace**, the closest analogue. It has its own center-screen countdown: `modules/Countdown.lua`, declared
  `FULLSCREEN SCREEN_ALERT` at `core/Constants.lua:37`, with defaults `centerCountdown`, `countdownCue` (a sound at
  10, 5, 3, 2, 1 s) and `finalCountdown = 10` at `defaults/Profile.lua:102-104`. This is a hand-rolled version of
  what Callout `Countdown{}` provides (anti-patterns #47 territory) and is the natural second consumer. DpsRace is
  Retail-only, which Callout supports.
- **QuickComms:** the alerts are chat-channel output (`modules/Channels.lua`) plus `PlaySound` cues
  (`Dial.lua:602`, `Pad.lua:650`). There is no center-screen moment today, so it is weak.
- **SkillMaster:** the rank-cap toast (`Alerts.lua`) is detail, not urgent, so not a callout.
- **DropWatcher:** the upgrade toast is detail. A "roll now / timer ending" moment is a possible callout.
- No other roster addon calls `RaidNotice_AddMessage`, `RaidWarningFrame`, `PlaySoundFile` or `SpeakText` in
  shipped code (AbsorbTracker, AuraMaster, KickCD, WhatGroup, PFE, ConsumableMaster and OutfitterReborn were
  checked).

### Library code needed
**None.** This is an evaluation issue whose deliverable is per-candidate adopt / not now / never rows. If an
adoption (DpsRace) is accepted, it might expose a Callout gap (for example DpsRace's per-second sound cue at
10/5/3/2/1). That gap would be a new library item, not part of #85.

### Fits this run?
The evaluation fits the **adoption phase [3]**, which the owner has deferred. Doing it now is cheap, read-only work
that could be recorded in the plan's adoption section. The build is deferred.

### Recommendation
- **Decision: no library item. Fold #85 into the plan's adoption milestone [3].** Pre-fill the evaluation table:
  DpsRace **adopt (planned)**, replacing `modules/Countdown.lua`; DropWatcher **not now**; QuickComms **not now**;
  SkillMaster **never**.
- Keep #85 open until adoption runs.
- **Scope consequence:** if the run re-vendors CombatTrail (the only Callout consumer), any Callout change in this
  run has a real consumer to verify against. If CombatTrail is excluded, Callout changes have **no** consumer in
  the run. Recommend **including CombatTrail in the re-vendor sweep**, since it consumes LibKa0s and the owner
  said "all Ka0s addons", while stating plainly that it is outside `ADDONS.md`.

---

## #87 Standard sample character names / classes / specs

### Current state (shipped code, tests excluded)
| Addon | Where | Sample identities |
|---|---|---|
| CombatTrail | `modules/MockFights.lua:71-123` | `REALM="Samplerealm"`, me `Samplehunter` (pet `Grimfang`), alt `Mockarrow` (pet `Ashpaw`), targets `Sampleshaman`, `Samplerogue`; ilvl per client |
| DpsRace | `modules/MockRuns.lua:60,73` | `Sampleblade` PALADIN 70 Retribution, `Mockflame` MAGE 63 Fire |
| DropWatcher | `modules/SimRoster.lua:36-56`, `modules/TestData.lua:326-329` | 25 `NAMES` + 20 `RAID_NAMES` (fantasy), `REALMS` Stormhold/Ashcrest/Duskmere/Silverkeep/Emberfall, Forever `SURNAMES` (Ironhide, Silentshot, ...); test data Seta/Littlewolf/Uniquerogue/Butterz with fake GUIDs `Player-0-0000T00n` |
| MultiMeters | `modules/SimWorld.lua:56-96` | about 40 fantasy names (Aldrenna, Brakthar, ...), `PET_NAMES = { HUNTER="Wolf", WARLOCK="Imp" }` |
| BankLedger | `modules/SimWorld.lua:149`, `LedgerTable_TestMode.lua:107` | `L["Simbanker"]` (localized!), `Mage-Ravencrest` (a **real realm**) |
| WhatGroup | `core/TestPreview.lua:34` | `Testadin-Silvermoon` (a **real realm**) |
| LootHistory | test data | `Mock-Realm`, `Simalt-Realm`, `Mage-Ravencrest` |

Test fixtures add Testchar/Testrealm (LibKa0s, QuickComms, DropWatcher, AbsorbTracker, PFE). They also use **real
realm names**: Frostmourne, Silvermoon, Ravencrest, Draenor, Sargeras, Thrall. Some of those name/realm pairs look
like real characters, possibly the owner's: `Kaosmage-Frostmourne`, `Kaos-Silvermoon`, `Kaosz-Draenor`
(MultiMeters `modules/Export.lua:601` comment), `Traxex Silentshot`. Five conventions are in use: Sample*/Mock*,
Test*, fantasy lists, real realms, and a localized name. The standard has no rule on sample names (grep over
`standards/*.md` found none).

### Where it should live
- **The convention belongs in the standard.** It is a rule about how an addon presents fake people, and the
  natural home is `preview-mode` (test and sim data, "kept current at every release"). The rule: a recognisable
  fictional marker, never a real realm in shipped sample data, never a real player's name, the Forever
  "First Surname" shape with no realm, and never localized names (names are data, not UI text).
- **The data could live in LibKa0s** as a small pure table, for example `Sim.SAMPLE` or a `LibKa0s-Sample-1.0`
  data major: per-client sets of `{ name, realm|surname, classFile, specID, pet }` plus name pools for rosters.
  Pros: one copy, and the specIDs per client can be checked once (Forever specs are talent-tree names). Cons:
  library-stack-§7 bar 3 asks whether this is stable, and roster-heavy addons (DropWatcher 45 names, MultiMeters
  40) have their own pool sizes and seeded determinism (DropWatcher "a seed's group keeps its names"). Swapping
  their pools changes seeded sim output and its suites. A member on the existing `Sim` major (minor 2,
  `Sim.lua:97`) avoids a new major.

### Library code needed
Optional: a pure data table plus 2 accessors. It is small (about 100-200 lines plus tests), but it depends on the
naming convention being ruled first.

### Fits this run?
**Partly.** The issue is `state:untriaged` and its acceptance criteria are `_TBD_`. The library half is cheap, but
it is meaningless before the owner rules on the convention and the home. Adopting the data in 7+ addons is phase
[3], which is deferred.

### Recommendation
- **Decision: rule now, upfront, then build the library half in this run only if the owner picks "both".**
  - Recommended convention: the `Sample`/`Mock` prefix for named protagonists, fictional realms (`Samplerealm`
    plus a small pool such as DropWatcher's), Forever surnames from a fixed fictional pool, fixed specIDs per
    client, and pets from a pool. Never a real realm, never a real character, never localized.
  - Recommended home: **the standard owns the rule; LibKa0s owns the data** as members on `LibKa0s-Sim-1.0` (not a
    new major).
  - Roster pools (DropWatcher, MultiMeters) keep their own lists for determinism; only the "protagonist" samples
    converge.
- **Flag for the owner:** fixtures and comments carry names that look like real characters on real realms. Is that
  intended? A privacy-flavoured cleanup belongs to phase [3] or to a sync-docs pass.

---

## #91 wago.tools DB2 survey

### Current state: most of it was done on 2026-11-15, outside this issue
- The standard **clients-§10**, "Validating seed data against the client's own DB2 (wago.tools)", is at
  `standards/standards/clients.md:110-165`. It covers the endpoints table, builds per product, and names
  AuraMaster's `tools/spell-research/` as the reference implementation (:165).
- dev-copilot **2.10.0** adds `/dev-copilot:validate-seeds` (`commands/validate-seeds.md`, WoW overlay
  `profiles/wow/validate-seeds.md`, product `wow` for retail and `wowf` for forever at :43). The loop and the
  rules are shared, and each repo keeps its own scripts (dev-copilot `CLAUDE.md:11`).
- Ten roster addons have a `docs/validate-seeds.md` contract and frozen `docs/seed-research/2026-11-15-*`
  bundles: AuraMaster, ConsumableMaster, DpsRace, DropWatcher, KickCD, OutfitterReborn, PrettyChat, QuickComms,
  SkillMaster and WhatGroup.
- The issues the survey cites are **closed**: AuraMaster #27, ConsumableMaster #49, KickCD #39.

### What is still open
1. **Duplicated plumbing (Q2).** Nine per-addon scripts each re-implement the fetch, User-Agent, cache and
   Lua-reader code (`http_get` with a User-Agent at SkillMaster `tools/seeds/seeds.py:398-402`, plus a hand-rolled
   Lua table reader at :178-290). The copies are ConsumableMaster seeds.py 1217 lines, KickCD 1147,
   OutfitterReborn 1198, DropWatcher 1018, SkillMaster 994, QuickComms 941, WhatGroup teleports.py 820, PrettyChat
   globalstrings.py 717 and DpsRace 686. They are different blobs, each about 700 to 1200 lines. The ruling so far
   is "loop shared, scripts per repo", and the plumbing was never extracted.
2. **Inventory gaps (Q1).** These roster addons have no contract: AbsorbTracker, BankLedger, LootHistory,
   MultiMeters, PanelMaster, PFE, PGFE and LibKa0sSkinTester. PGFE ships `defaults/Realms.lua`, a realm list that
   DB2 (`ChrRealm`?) or the builds API could check. MultiMeters `SimWorld` spell ids are sim-only. CombatTrail
   cites wago in `defaults/Hearthstones.lua` but has no contract. **LibKa0s itself** has no contract for the
   `Compat` per-client assumptions or the testkit client globals (`testkit/client_globals_forever.lua`,
   `client_globals_live.lua`); that is the most library-relevant check.
3. **Kit integration (Q3).** Nothing in the kit consumes a DB2 snapshot. clients-§10 and testing-§7 keep it
   outside the green gate. Recommend keeping it that way.

### Library code needed
**None for the addons.** A shared Python helper does not belong in the LibKa0s ship payload. If extracted, it
belongs in **dev-copilot**, beside the command, as `scripts/wago.py`: resolve the build, fetch with a User-Agent,
cache per build, freeze to `raw/*.csv.gz`, and read Lua tables. A LibKa0s `docs/validate-seeds.md` contract for
Compat/testkit assumptions would be a LibKa0s *repo* item (tools/docs), not payload code. It moves no LibStub
minor.

### Fits this run?
**No as library work.** It is a research and decision issue whose implementation largely happened in the
validate-seeds rollout. The remaining pieces sit in dev-copilot or are per-addon adoption.

### Recommendation
- **Decision: close #91 as mostly done**, with a comment that maps each of its 3 questions to clients-§10,
  dev-copilot 2.10.0 and the ten contracts.
- File two follow-ups instead:
  - (a) a dev-copilot issue: "extract the shared wago fetch/cache/Lua-reader into `scripts/`, so per-repo
    `seeds.py` keep only rules";
  - (b) a LibKa0s issue, "a `docs/validate-seeds.md` contract for Compat and testkit client globals", which could
    join a later run.
- Closing the issue and filing the follow-ups are GitHub writes, so the lead does them (subagents cannot write to
  GitHub).

---

## Summary table

| Issue | Library payload code? | LibStub minors that would move | In this run? | Recommended decision |
|---|---|---|---|---|
| #76 Ace3 tag | No (addon `libs/Ace*`) | none | **No, blocked**: no Ace3 tag contains ac3d1225; the pin is master HEAD | Defer; comment the evidence; keep open |
| #83 FTUX | Yes, a new major (about 1.2-1.8k lines) | new `LibKa0s-Tour-1.0`; maybe Schema 3→4 (`key` flag); maybe an Options entry point | **No** | Out of scope; own brainstorm and spec run |
| #85 Callout consumers | No | none | Evaluation only → adoption phase [3] | Fold into the plan's adoption section; DpsRace = planned adopter |
| #87 Sample names | Optional small data table | `LibKa0s-Sim-1.0` 2→3 if "both" | Only after the owner rules convention + home | Ask upfront; standard rule + Sim data members |
| #91 wago survey | No | none | **No** | Close as mostly done; file dev-copilot + LibKa0s follow-ups |

## Standard / doc ripple (if the recommendations are taken)
- #87: a new preview-mode subsection (sample identities), a CHANGELOG entry, a version bump of the standard and a
  context-pack refresh. The Sim docs/api would get a new minor document and members JSON, plus a CONSUMERS row.
- #83 (later run): an options-ui or launcher subsection, a Tour docs/api, CONSUMERS, and the bar-1 ruling recorded
  if it ships with one consumer.
- #76, #85, #91: none in this run, apart from issue comments.

## Open questions for the owner (decisions, recommended answer first)
1. **Is CombatTrail (not in ADDONS.md, branch `main`) in the re-vendor sweep?** Recommended: yes. It is the only
   Callout consumer and it vendors LibKa0s. The alternative is to add it to ADDONS.md first.
2. **#76: defer until Ace3 tags?** Recommended: yes, with no work this run.
3. **#83 FTUX: out of this run?** Recommended: yes, as its own brainstorm and spec bundle. If kept: a
   schema-row `key` flag, first-run only, deferred in combat, SHOULD not MUST.
4. **#85: treat as adoption-phase evaluation only?** Recommended: yes. DpsRace's `modules/Countdown.lua` is the
   planned adopter.
5. **#87: home for sample identities?** Recommended: the standard owns the convention and LibKa0s `Sim` owns the
   protagonist data; roster pools stay per addon. Also: keep or scrub the real-realm and real-looking character
   names in fixtures?
6. **#91: close as mostly done and open the dev-copilot helper-extraction issue?** Recommended: yes.

## Risks
- Executor scripts that assume `master` will fail on SkillMaster and CombatTrail (`main`).
- The Ace3 provenance line is formatted three ways, which complicates a future bulk update.
- If #87's data is adopted into addons with seeded sims (DropWatcher, MultiMeters), seeded output changes and
  their suites change with it. Keep the roster pools per addon.
- Pulling #83 into this run would make an unsettled design the critical path of a re-vendor run.
