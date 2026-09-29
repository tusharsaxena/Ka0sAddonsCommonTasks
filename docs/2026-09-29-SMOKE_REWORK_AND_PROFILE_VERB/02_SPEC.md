# Spec

Every item in `items.tsv` implements a section of this file. Where this spec and an addon's own
`CLAUDE.md` / the Ka0s standard disagree, **stop and report**; do not resolve it silently.

Common to every item:
- Work on the repo's `feat/2026-09-29-smoke-and-profile` branch (cut from `master` by the repo's first item).
- One item, one commit, subject `<ID>: <summary>`; body ends with the session's Co-Authored-By and
  Claude-Session trailers. Named files only in `git add`; never `-A`, `--amend`, `--no-verify`, `--force`.
- Green gate before the commit: `~/.claude/wow-addon/bin/ka0s-bounded lua tests/run.lua` (or the repo's
  runner) and `~/.claude/wow-addon/bin/ka0s-bounded luacheck .` at 0/0. Every Lua / luacheck run goes
  through the bounded runner. A red gate is a stop: no commit, report the real output.
- Line endings: addon files are CRLF (`.gitattributes`); keep them. The kit's eol test catches LF.
- Moved line numbers: fix every `file:line` citation the item's edits shift (the docs citation tests
  enforce it in several repos). Regenerate `docs/test-cases.md` (`lua tests/run.lua --list`, CRLF) and
  the README test badge when the test count moves.
- Never edit `libs/` or `tests/_kit/` except by the re-vendor copy step.
- No version bump of any addon, no tag, except the LibKa0s release in S1 (authorized by D1).

## S1. LibKa0s: `CliProfile` (Slash minor 17, library v1.63.0)

In `LibKa0s/LibKa0s/Slash.lua`, bump `LibKa0s-Slash-1.0` to minor 17 and add:

- **Descriptor field `profiles`** (optional): a function returning the host's profile store, duck-typed:
  `:GetProfiles(tbl) -> tbl, n`, `:GetCurrentProfile() -> name`, `:SetProfile(name)` (AceDB-3.0's
  shape). The library must not require AceDB (slash-commands.md:34). Absent field, or the function
  returning nil: `CliProfile` prints `lib.STRINGS.PROFILE_UNAVAILABLE` and does nothing else.
- **`Sl:CliProfile(rest)`**:
  1. Trim `rest`; strip one pair of matching surrounding quotes (`"x"` or `'x'`); trim again. Case and
     inner spaces are kept (profile names are case-sensitive).
  2. Empty name: print the list. Header `PROFILE_LIST_HEADER` ("Profiles"; no trailing colon), then one
     row per profile, sorted case-insensitively, the current one suffixed `PROFILE_CURRENT_MARK`
     ("(current)"), then the hint row `PROFILE_HINT` ("<slash> profile <name> switches profile").
  3. Name equals the current profile: print `PROFILE_ALREADY` ("Already on profile '%s'.").
  4. Name exists (exact match): if `InCombatLockdown` exists and returns true, print
     `PROFILE_COMBAT` ("Can't switch profiles in combat.") and stop. Otherwise call `SetProfile(name)`
     and print `PROFILE_SWITCHED` ("Switched to profile '%s'."). The switch's debug-log line stays the
     host's profile handler's job (debug-logging-§10); the library logs nothing.
  5. Name does not exist: print `PROFILE_UNKNOWN` ("No profile named '%s'."); if exactly one stored
     profile matches case-insensitively add `PROFILE_DID_YOU_MEAN` ("Did you mean '%s'?"); then the
     list as in 2. Never create a profile.
  All output goes through the host's tagged `print` (slash-commands-§4). Every string is a
  `lib.STRINGS` key, so the existing `L` locale override reaches them.
- **Plain functions** the host's own sub-trees reuse: `lib.ProfileNames(store)` (sorted names, current)
  and `Sl:ProfileSwitch(name)` (steps 3-5 for an already-parsed name). AbsorbTracker and
  PartyFrameEnhanced route their `use <name>` through `ProfileSwitch`.
- `profile` is **not** added to `lib.LIVE_VERBS` and not reserved.
- Tests in `LibKa0s/tests` (fixture_slash + a new or extended suite): quotes stripped, case kept,
  spaces kept, list order and current mark, already-current, unknown + did-you-mean, unknown never
  creates, combat refusal, missing `profiles`, store returning nil, no trailing colon on any line.
- Docs: `docs/api/Slash/version-17-docs.md` (the new members and the descriptor field), CHANGELOG
  `## v1.63.0 — 2026-09-29`, README/CLAUDE counts, and whatever else the repo's own gate requires.
- Tag `v1.63.0` **locally** on the item commit. The tag is pushed only with the owner's merge go-ahead.

## S2. Profile support where it is missing (PrettyChat, WhatGroup, BankLedger, LootHistory)

Goal: the addon behaves like the seven that already have profiles.

- **Vendor** `AceConfig-3.0` and `AceDBOptions-3.0` (with their `AceConfigRegistry`,
  `AceConfigCmd`, `AceConfigDialog` parts, as the Ace3 package lays them out) from the same Ace3 release
  the collection already vendors (copy from `AuraMaster/libs/`; confirm identical versions with a diff
  against another addon). Add them to the TOC / libs XML in the order the seven do, and to
  `DEPENDENCIES.md`.
- **Profiles page**: `settings/Profiles.lua` modeled on `KickCD/settings/Profiles.lua` (AceDBOptions
  in a canvas subcategory named "Profiles", registered last in the Settings tree, no Defaults button,
  excluded from the global reset per options-ui-§3).
- **Profile callbacks**: `OnProfileChanged`, `OnProfileCopied`, `OnProfileReset` registered on the db,
  sharing one adopt path: run profile-scoped migrations idempotently for the new profile
  (savedvariables-§1), re-sync the enable latch if the enabled flag is profile-scoped, re-apply every
  setting's effect, refresh an open panel, and log exactly one line (debug-logging-§10, reusing the
  addon's existing profile tag if any).
- **`docs/profiles.md`** (documentation-§3 Tier 2): what a profile holds, what stays account-wide, the
  events, the `profile` verb. Register it in the ARCHITECTURE Documentation map; replace any
  "Not applicable" line for it.
- **PrettyChat, WhatGroup**: settings are already in `db.profile`; no data moves.
- **BankLedger, LootHistory** (D5, settings only):
  - Every settings schema row moves from `db.global` to `db.profile` (paths, `defaults/Profile.lua`
    created, `defaults/Global.lua` keeps only recorded data + `minimap` + anything the standard pins to
    global). Recorded data (ledger, loot history, sessions, caches) stays in `db.global`.
  - One migration step (bump the schema version): copy each stored settings value from `db.global`
    into the `Default` profile (`db.profiles.Default`, created if absent), then clear it from global.
    Idempotent; a second run is a no-op.
  - BankLedger: delete the `savedvariables-§2` row from `docs/ARCHITECTURE.md` → Documented deviations
    (the addon now conforms); fix every doc that says the addon has no profiles.
  - LootHistory: rewrite `docs/schema.md`'s "addon never touches `db.profile`" section.
  - **D6**: settings that govern recorded data (`retentionDays`, prune/purge rules) stay in
    `db.global`; profile events never prune or delete history.
  - Tests: migration (values land in the profile, global cleared, idempotent), reads resolve against
    the profile, recorded data untouched, profile switch re-applies settings.

## S3. The `profile` verb in every addon (after S1 and, for the four, S2)

Per addon:
1. **Re-vendor LibKa0s v1.63.0** from the local tag (`/wow-addon:revendor-libka0s` procedure: copy
   `libs/LibKa0s/` and `tests/_kit/` whole from the tag, roll the CLAUDE.md provenance line to v1.63.0,
   write the `docs/revendor/` bundle). Adopt no other surface in this item beyond what is needed.
2. **COMMANDS row** `{ "profile", <NS.L description>, function(rest) <dispatcher>:CliProfile(rest) end }`
   placed next to the other settings verbs. Description text: "List profiles, or switch to one: profile
   <name>". AbsorbTracker and PartyFrameEnhanced keep their existing row and sub-tree, reworked so:
   bare `profile` → `CliProfile("")` then the sub-help; a first word matching a sub-verb
   (case-insensitive) → that sub-verb; anything else → `CliProfile(rest)`; `use <name>` →
   `ProfileSwitch(name)` (AbsorbTracker's silent-create is removed, per D3).
3. **Descriptor**: pass `profiles = function() return NS.db end` (the addon's own db handle).
4. **Disabled state**: `profile` answers while disabled. Hosts that pass no `liveVerbs` today start
   passing `lib.LIVE_VERBS` plus `"profile"` (and nothing else); hosts that already widen add `"profile"`.
   Update the comments that say the host passes no liveVerbs. `tests/test_disabled.lua` pins `profile`
   as live.
5. **Degraded stub** (no LibKa0s): carries `CliProfile` (prints the unavailable line) **and
   `ProfileSwitch`** (or an explicit ignore entry for it). The kit's by-name `assertSurfaceParity`
   reads the live dispatcher instance, so the re-vendor alone turns it red until both are on the stub
   (amended 2026-09-29, SP-LIB-01 review).
6. **Tests**: COMMANDS count/order pins, help line counts, disabled pins, a switch test (existing →
   switched + handler ran), an unknown-name test (refused, nothing created), quotes test.
7. **Docs**: ARCHITECTURE Slash Commands table, `docs/slash-dispatch.md`, README command table, verb
   counts wherever quoted (e.g. "23 verbs"), `docs/profiles.md` (the verb; AuraMaster's "There is no
   `/am profile` verb" line goes).

## S4. Smoke-test rework (after S3 in the same repo)

Rewrite `docs/smoke-tests.md` as one evergreen, deduplicated, theme-grouped suite. It must stay under the
kit's 1500-line layout cap; aim for well under the current length.

**Shape**
```
# Smoke tests — <Addon display name>
One paragraph: what this is (in-client checks the headless suite cannot make), how to run it
(/reload clean, debug on where a step says so), how to record (Result lines), ID scheme.
## Index            (table: ID range | Theme | What it covers)
## Before you start (setup shared by all themes)
## <Theme>          (one section per theme, checks numbered <THEME>-<n>)
...
## Non-English client   (this exact heading text; LOC-<n> checks)
## Pending sign-off     (only if any: unsigned owner checks carried over, each with its new ID)
```
**Check format**: `**<ID>. <Title>.** <setup / steps> → <expected>. Result:` on one bullet or short
paragraph. One behavior per check; steps say exactly what to click or type.

**Themes**: choose per addon from this vocabulary (keep the prefixes stable across addons): INSTALL
(install, load, reload, first run), SLASH (commands, help, disabled refusals), PANEL (settings panel and
pages), PROFILE (profiles page and the `profile` verb; always present after S3), STATE (enable/disable,
stand-down, lock), COMBAT (combat lockdown, secret values, restrictions, M+), DIAG (debug console,
diagnostics, perf), DEGRADED (library-absent install), plus 1-5 feature themes named for the addon
(e.g. CONT for AuraMaster containers, MACRO for ConsumableMaster macros). LOC for the non-English section.

**Content rules**
- Keep every in-client behavior the old doc checks, **once**. Merge duplicates. Drop a check only when its
  whole expectation is already asserted by a named headless test (name it in the coverage map) or it
  checks a thing that no longer exists.
- Filled-in historical sign-off batches are dropped; their still-relevant checks survive as evergreen
  checks. Unsigned owner checks (empty or "owed" Result) are kept under Pending sign-off with their
  new ID and origin (old section/number).
- The Non-English client section keeps whatever the addon's doc-structure test requires (WhatGroup: the
  literal `C_SpellBook.IsSpellKnown`). Its first check is `LOC-1`.
- Add PROFILE checks for the new verb (list, switch, unknown name refused, quotes, disabled, combat).
- US English, no AI-isms (the kit's prose gate runs on docs).

**Coverage map** `smoke-maps/<Addon>.md` in this bundle: a table old location (section + number or line
range) → new ID, or "dropped: <reason / covering test>". Every old check appears.

**Inbound references**: update every reference into the old numbering in live files (`docs/*.md` other
than frozen `docs/audits|reviews|revendor|automated-tests|perf-analysis/`, README, CLAUDE.md, code
comments, tests). Cross-addon citations of `ConsumableMaster § 3c` / `KickCD § 9b` become
`ConsumableMaster LOC-1` / `KickCD LOC-1`. Plans in Ka0sAddonsCommonTasks are historical and are not
edited.

## S5. wow-addon plugin

`wow-addon/commands/new-addon.md` (the source repo at `GIT/wow-addon`) cites
`ConsumableMaster/docs/smoke-tests.md § 3c` and `KickCD/docs/smoke-tests.md:229 § 9b` as worked
examples and asks for "a row in the doc's index table". Re-point both to the `LOC-1` checks and
describe the S4 shape. Docs-only; follow that repo's own gate and version rules (report if it demands a
version bump rather than bumping).
