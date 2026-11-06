# WoW Forever Port, Steps 1–4: Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Item status lives in git, not in these checkboxes. Run `plan-data/resume-state.sh`.

**Goal:** Make the Ka0s collection ready to build for Retail and WoW Forever from one codebase. That means a standard that allows it, a LibKa0s seam to detect the client and gate features, every addon on an Ace3 that works on both clients, and dev-copilot commands that understand both.

**Architecture:** The work goes upstream first. The standard (merge gate A) comes first. Then LibKa0s (local tag), then dev-copilot (merge gate B, followed by an owner plugin reload). After that, all 17 addons re-vendor Ace3 `ac3d1225`, LibKa0s and the standards reference. The owner smokes on Retail, and the finalize waits for the owner's go-ahead.

**Tech Stack:** Lua 5.1 (WoW), Ace3, the LibKa0s test kit (`lua tests/run.lua`), luacheck through `ka0s-bounded`, Markdown standard sections, dev-copilot command specs (Markdown) and Python scripts with pytest-style `scripts/test_*.py`.

**Spec:** `docs/2026-11-07-WOW_FOREVER_PORT/01_DESIGN.md`. The rulings are in `00_OWNER_CHECKS_AND_RULINGS.md`, and the research is in `reports/WoW Forever porting research.md`.

## Global Constraints

- Branch `feat/2026-11-07-wow-forever-port` in every repo touched. Every item id carries the `WFP-` prefix (bare ids such as `ST-01` collide with earlier runs). Each commit subject starts with `<ID>: ` and ends with the session's attribution trailers.
- Forever identity: client 1.60.1, build 70790, interface **16001**, `WOW_PROJECT_ID == WOW_PROJECT_CAMELOT == 18`. `WOW_PROJECT_CAMELOT` is **nil on Retail**. Retail interface **120105**.
- Detection only through `LibKa0s-Compat-1.0`. Never by interface number, and never treat `== WOW_PROJECT_MAINLINE` as meaning "modern client".
- Ace3 from WoWUIDev/Ace3 commit **`ac3d1225`** (2026-10-28). Copy exactly the modules each addon already vendors, and edit no vendored file.
- Roster `Clients` values, verbatim: `Retail · Forever`, `Retail`, `Retail (port pending)`. WhatGroup and PremadeGroupsFilterExtension are `Retail`; the other 15 are `Retail (port pending)`.
- Load-gating lines, only for `Retail` addons: `## AllowLoadGameType: standard` and `## ExcludeLoadGameType: camelot`.
- Standard release: **v2.103.0** (from v2.102.2). LibKa0s release: **v1.92.0** (from v1.91.0). The tag stays local until the finalize. dev-copilot release: **2.8.0** (from 2.7.1).
- Green gate per repo, as its `CLAUDE.md` defines it: `lua tests/run.lua` with 0 failed, `~/.claude/dev-copilot/bin/ka0s-bounded luacheck .` with 0/0, and the 1500-line cap.
- Merge gates A (WowAddonStandards) and B (dev-copilot) need the owner's go-ahead. Merge `--no-ff` and push master. Nothing else merges before the finalize.
- Subagents never push or write to GitHub. The lead session does every push, merge and issue write. Space out GitHub writes.
- Smoke is the owner's. Never mark an SM-* check passed.

## Review Focus

1. **A harness with no project constants.** A Lua test env where `WOW_PROJECT_CAMELOT` and `WOW_PROJECT_ID` are both nil must make `IsForever()` false and `IsRetail()` false, never Forever. Pinned by `test_compat_client_unknown` (WFP-LK-02).
2. **Live Retail shape.** `WOW_PROJECT_ID = 1` with `WOW_PROJECT_CAMELOT` nil must give `IsRetail()` true and `ClientKey() == "retail"`. Pinned by `test_compat_client_retail` (WFP-LK-02).
3. **A gated-off entry is never built.** A settings tab, slash verb, launcher entry or keybind row declared `clients = { "retail" }` must not exist at all under the Forever profile: not hidden, not listed in help, not counted. Pinned by `test_gate_*_absent_on_forever` (WFP-LK-03, WFP-LK-04).
4. **The Retail profile key survives Ace3.** A Retail character's AceDB key (`Name - Realm`) and existing profile names must be unchanged after MINOR 33 → 40. Pinned by WFP-ACE-00's proof and `test_acedb_retail_key_stable`.
5. **A two-number Interface line must survive `wow-bump-interface`.** `## Interface: 120105, 16001` bumped to Retail 120107 must give `120107, 16001`, never one number. Pinned by `test_bump_interface_dual` (WFP-DC-02).

---

## Milestone M0: plan (Ka0sAddonsCommonTasks)

### Task WFP-PLAN: commit the plan bundle
- [ ] Commit `02_EXECUTION_PLAN.md`, `03_SMOKE_TESTS.md`, `RESUME.md`, `checkpoints.tsv` and `plan-data/`. Subject `WFP-PLAN: …`.

## Milestone M1: the standard (WowAddonStandards, v2.103.0)

Verification for every M1 task: the repo's own doc checks, if its `CLAUDE.md` names any. Also confirm that each
`grep` named in the task shows the old Retail-only wording gone.

### Task WFP-ST-01: a Clients column in the roster
**Files:** Modify `standards/ADDONS.md`.
- [ ] Add a `Clients` column to the in-scope table, holding the values from Global Constraints. Add a paragraph saying the column is normative, is the single source of truth that dev-copilot and the audit read, and records what the addon **ships today**.
- [ ] Define the three values: what each one means, which TOC shape it requires, and what the audit flags for each.
- [ ] Commit `WFP-ST-01: …`.

### Task WFP-ST-02: a new `clients` section
**Files:** Create `standards/standards/clients.md`. Modify `standards/STANDARDS.md` (Sections list and index blurb).
- [ ] Write the section, numbered like its siblings (`clients-§1..§n`):
  - §1 the supported clients, with the identity values from Global Constraints.
  - §2 the roster declaration (cite ADDONS.md).
  - §3 detection only through Compat (`IsForever`, `IsRetail`, `ClientKey`). Feature detection is allowed only for a specific API gap inside a feature that is supported.
  - §4 per-client features: declared, and gated at registration through the library's `clients` descriptor field or `Compat.ForClient`. Never hidden at runtime. Includes the ARCHITECTURE per-client feature table.
  - §5 per-client seed data: two lists, chosen once through `ClientKey()`. Filtering one list is non-compliant.
  - §6 tests and smoke: both kit profiles, and a smoke file that covers both clients.
  - §7 the Retail-only (by decision) shape.
  - §8 the port-pending shape.
- [ ] Commit `WFP-ST-02: …`.

### Task WFP-ST-03: rewrite the Retail-only rules
**Files:**
- Modify `standards/standards/toc-file.md:57-65`, `compat.md:5,42`, `anti-patterns.md` (entries #9 and #15, plus new entries), `packaging.md:46`, `versioning-git.md:8` and `layout.md:11,29`.
- Modify `documentation.md` (the README badge and the supported-clients line), `client-quirks.md`, `testing.md`, `library-stack.md` §7 and `open-evolutions.md:349-352`.
- [ ] `toc-file`: allow the dual line `## Interface: <retail>, <forever>` and the two load-gating lines for `Retail` addons. Per-flavour TOC files stay forbidden. Confirm the directive spelling against warcraft.wiki.gg's TOC_format page and cite it.
- [ ] `compat`: widen the scope to "Retail patch differences and the Retail/Forever split".
- [ ] `library-stack-§7`: the flavour helpers meet the two-consumer bar **by ruling**.
- [ ] New anti-patterns, each with a bad and a good example: interface-number detection; `== WOW_PROJECT_MAINLINE` as "modern"; a feature registered and then hidden; a seed list filtered rather than split; a bare `WOW_PROJECT_*` read outside Compat.
- [ ] Close the WoW:F open evolution as ruled, citing v2.103.0.
- [ ] Check: `grep -rn "flavor\|flavour\|Retail-only\|single.*Interface" standards/standards/` shows no remaining ban that contradicts `clients.md`.
- [ ] Commit `WFP-ST-03: …`. Split it into several commits under the same id if that helps review.

### Task WFP-ST-04: playbooks and context pack
**Files:** Modify `AUDIT.md`, `NEW_ADDON.md`, `AUTOMATED_TESTS.md`, `standards/NEW_ADDON_CONTEXT.md` and `standards/EXECUTIVE_SUMMARY.md` where it restates the scope.
- [ ] `AUDIT.md`: the audit reads `Clients` and applies the per-value checks from WFP-ST-01.
- [ ] `NEW_ADDON.md`: scaffold dual-client by default (`Retail · Forever`), with the dual TOC line, the gate wiring and both kit profiles.
- [ ] `AUTOMATED_TESTS.md`: a dual-client addon runs the battery under both kit profiles (`KA0S_KIT_CLIENT`, from WFP-LK-01).
- [ ] Commit `WFP-ST-04: …`.

### Task WFP-ST-05: release v2.103.0
**Files:** `standards/CHANGELOG.md`, the version header in `standards/STANDARDS.md:1`, and every other place the version appears (`grep -rn "2\.102\.2"`).
- [ ] Changelog entry, version bump and date 2026-11-07. Commit `WFP-ST-05: …`.

### Checkpoint CP-1, then merge gate A
- [ ] Run an independent review of the M1 diff. Record it as a `refs/notes/ka0s-review` note.
- [ ] Push the branch and the notes, then log a row in `checkpoints.tsv`.
- [ ] **Ask the owner for gate A.** On the go-ahead: `git merge --no-ff` into master with subject `WFP-GATE-A: Merge …`, then push master.

## Milestone M2: LibKa0s (v1.92.0, local tag)

The gate for every M2 task: `lua tests/run.lua` with 0 failed, under both `KA0S_KIT_CLIENT=retail` and `=forever`, plus luacheck 0/0.

### Task WFP-LK-01: client profiles in the test kit
**Files:**
- Create `testkit/mock_client.lua`.
- Modify `testkit/loader.lua` (apply the profile to the mock set), `testkit/README.md` and `tests/wow_mock.lua`. In `tests/wow_mock.lua`, move `GetBuildInfo` to the profile.
- Test: `tests/test_mock_client.lua`.

**Interfaces:**
- Produces `MockClient.apply(mocks, name)`, where `name` is `"retail"` or `"forever"`, defaulting to `os.getenv("KA0S_KIT_CLIENT") or "retail"`.
  - retail: `WOW_PROJECT_ID=1`, `WOW_PROJECT_MAINLINE=1`, `WOW_PROJECT_CAMELOT=nil`, and `GetBuildInfo` → `"12.1.5","70783",…,120105`.
  - forever: `WOW_PROJECT_ID=18`, `WOW_PROJECT_MAINLINE=1`, `WOW_PROJECT_CAMELOT=18`, and `GetBuildInfo` → `"1.60.1","70790","Nov  3 2026",16001`. It also removes the globals absent on Forever: `GetSpecialization`, `GetSpecializationInfo`, `GetActiveSpecGroup`, `GetTalentInfo` and `SetDesaturation`. `SetDesaturation` is also removed under retail.
  - An unknown name raises.
- Produces `MockClient.current()` → `"retail"|"forever"`.
- [ ] Write `test_mock_client_retail_defaults` (constants as above, `WOW_PROJECT_CAMELOT == nil`).
- [ ] Write `test_mock_client_forever` (18/18, `GetBuildInfo` 4th return 16001, `GetSpecialization == nil`).
- [ ] Write `test_mock_client_unknown_raises`.
- [ ] Run the tests and watch them fail. Implement, then run them and watch them pass under both env values. Bump the kit revision (52) in `testkit/README.md`.
- [ ] Commit `WFP-LK-01: …`.

### Task WFP-LK-02: client helpers in Compat (minor 2)
**Files:**
- Modify `LibKa0s/Compat.lua`: `MINOR` 1→2, and update the header's member count and "why narrow" note to name the ruling.
- Create `docs/api/Compat/version-2-docs.md` and `members-2.json` (generate with `tools/gen-api-members.lua`).
- Test: `tests/test_compat.lua`.
- Modify `.luacheckrc`: add `WOW_PROJECT_ID`, `WOW_PROJECT_MAINLINE` and `WOW_PROJECT_CAMELOT` to `read_globals`. Do the same in the kit's luacheck template if it has one (`grep -rn read_globals testkit`).

**Interfaces:**
- `lib.IsForever() -> boolean`: `WOW_PROJECT_CAMELOT ~= nil and WOW_PROJECT_ID == WOW_PROJECT_CAMELOT`, read bare at call time.
- `lib.IsRetail() -> boolean`: `WOW_PROJECT_MAINLINE ~= nil and WOW_PROJECT_ID == WOW_PROJECT_MAINLINE and not lib.IsForever()`.
- `lib.ClientKey() -> "retail"|"forever"|nil`.
- `lib.ForClient(clients) -> boolean`: `clients` is nil (meaning both), the string `"both"`, or an array of `"retail"`/`"forever"`. It is true when `ClientKey()` is listed. When `ClientKey()` is nil, it is true only for nil or `"both"`. An unknown token raises at call time with the message `ForClient: unknown client "<x>"`.
- [ ] Write the tests:
  - `test_compat_client_retail`: Review Focus 2.
  - `test_compat_client_forever`.
  - `test_compat_client_unknown`: Review Focus 1, with both constants nil, so `IsForever`, `IsRetail` and `ClientKey` all answer false/false/nil.
  - `test_compat_client_read_at_call_time`: flip the mock after load and watch the answer change.
  - `test_compat_forclient_cases`: nil, `"both"`, `{"retail"}` and `{"forever"}`, each under both profiles, plus the raise.
- [ ] Run the tests and watch them fail. Implement, then run them under both profiles and watch them pass. Update the docs and the members JSON.
- [ ] Commit `WFP-LK-02: …`.

### Task WFP-LK-03: `clients` gating in the Options registry
**Files:**
- Modify `LibKa0s/OptionsRegistry.lua` and `OptionsTabs.lua`/`OptionsTabbed.lua`. Those are the page and tab descriptor consumers; confirm with `grep -n "descriptor\|tabs" LibKa0s/Options*.lua`.
- Bump each touched module's minor, and add a `docs/api/<module>/` version doc.
- Test: `tests/test_options_clients.lua` (new).

**Interfaces:**
- Consumes `Compat.ForClient` (WFP-LK-02).
- Produces an optional field `clients` on page, tab, row and section descriptors. It takes the same values `ForClient` accepts.
- [ ] Write `test_gate_page_absent_on_forever`: a page declared `{ "retail" }` registers no Settings category under forever, and does under retail.
- [ ] Write `test_gate_tab_absent_on_forever`: no tab button, and the strip geometry is computed without it.
- [ ] Write `test_gate_row_absent_on_forever`: no widget is acquired from the AceGUI pool.
- [ ] Write `test_gate_forever_only_absent_on_retail`: the mirror case.
- [ ] Implement by filtering descriptors **before** construction, at one choke point per registry. Run the tests and watch them pass. Commit `WFP-LK-03: …`.

### Task WFP-LK-04: `clients` gating in Slash, Launcher and Keybinds
**Files:**
- Modify `LibKa0s/Slash.lua` (verb table and help listing), `Launcher.lua` (menu entries) and `OptionsKeybinds.lua` (rows).
- Bump each module's minor, and add the matching docs.
- Test: `tests/test_gate_clients.lua` (new).
- [ ] Write `test_gate_slash_verb_absent_on_forever`: the verb is not dispatched, not listed in help and not counted, and typing it answers the dispatcher's normal unknown-verb line.
- [ ] Write `test_gate_launcher_entry_absent_on_forever`.
- [ ] Write `test_gate_keybind_row_absent_on_forever`.
- [ ] Lifecycle and Bus get **no** descriptor field. Event and message registrations are host code, and a host gates them with `Compat.ForClient`. Record this in the Compat API doc as the form for host-owned registrations (design §6.2). The design listed Lifecycle/Bus, and this plan narrows it, because those registries take no feature descriptors.
- [ ] Implement, then run the tests under both profiles and watch them pass. Commit `WFP-LK-04: …`.

### Task WFP-LK-05: spec readers on Forever
**Files:** `LibKa0s/Compat.lua:270-298` (code only if needed), `docs/api/Compat/version-2-docs.md` and `tests/test_compat.lua`.
- [ ] Read the Gethe/wow-ui-source `forever` branch for `C_SpecializationInfo.GetSpecialization` and `GetSpecializationInfo`: do they exist, and what do they return? Record the finding with the file path and build in the API doc.
- [ ] Write `test_compat_spec_forever`. Under forever, `GetSpecialization()` answers what the `C_SpecializationInfo` mock returns. If the namespace is absent, it answers `nil` without raising.
- [ ] Add the owner smoke `/dump` to `03_SMOKE_TESTS.md` (SM-F1). Commit `WFP-LK-05: …`.

### Task WFP-LK-06: static check for missing globals (SHOULD)
**Files:**
- Create `testkit/client_globals.lua` and data under `testkit/data/` (the global name sets for `live` and `forever` from Ketho/BlizzardInterfaceResources, recording the commit SHA).
- Test: `testkit/test_client_globals.lua`.
- [ ] The check scans the addon's tracked `*.lua`, **including `libs/`**, for bare calls to names that are absent from a client's set and are not guarded by a presence test on the same name. It reports `file:line name client`.
- [ ] Write `test_client_globals_flags_setdesaturation`: a fixture calling `SetDesaturation(x, true)` is flagged for both clients.
- [ ] Write `test_client_globals_ignores_guarded`: `if SetDesaturation then SetDesaturation(x) end` is not flagged.
- [ ] If this item is more than one session's work: file a LibKa0s issue instead, labelled `enhancement`, `state:triaged`, `severity:medium`, and record the item in `exceptions.tsv` with proof `gh issue view <n> -R tusharsaxena/LibKa0s`.
- [ ] Commit `WFP-LK-06: …`.

### Task WFP-LK-07: release v1.92.0 (local tag)
- [ ] Write the CHANGELOG entry, listing every module minor as v1.91.0's entry does and the kit revision 52. Bump the version wherever `grep -rn "1\.91\.0"` shows it in non-frozen docs.
- [ ] Gate under both profiles. Commit `WFP-LK-07: …`. Tag `v1.92.0` locally and do not push it.

### Checkpoint CP-2
- [ ] Review note, push the branch and notes (not the tag), and log a `checkpoints.tsv` row with test totals under both profiles.

## Milestone M3: dev-copilot (2.8.0)

The gate: the repo's own tests (`python3 -m pytest scripts/` or what its `CLAUDE.md` names) and `test_command_specs.py`.

### Task WFP-DC-01: roster Clients reader
**Files:** Create `scripts/roster_clients.py`. Test: `scripts/test_roster_clients.py`.

**Interfaces:**
- Produces the CLI `roster_clients.py <AddonFolder> [--roster <path>]`, which prints one of `retail+forever`, `retail` or `retail-pending` and exits 0. It exits 2 if the addon is not in the roster.
- The default roster path is `$KA0S_GIT/WowAddonStandards/standards/ADDONS.md`, falling back to `../WowAddonStandards/standards/ADDONS.md` from the repo root.
- [ ] Write the tests for the three values, the missing addon and a missing Clients column (exit 3 with the message `roster has no Clients column`).
- [ ] Implement, and have the tests pass. Commit `WFP-DC-01: …`.

### Task WFP-DC-02: `wow-bump-interface` per client
**Files:** `commands/wow-bump-interface.md`, plus a helper `scripts/bump_interface.py` with `scripts/test_bump_interface.py`.

**Interfaces:**
- `bump_interface.py <toc> --retail N [--forever M]` rewrites the Interface line in place. The Retail slot is the 6-digit number and the Forever slot is the `16xxx` number. The order is Retail first. It preserves the file's declared EOL.
- [ ] Write `test_bump_interface_dual` (Review Focus 5) and `test_bump_interface_retail_only`. A single-number line stays a single number when the addon is `retail` or `retail-pending`.
- [ ] Write `test_bump_interface_forever_slot` and `test_bump_interface_eol_crlf`.
- [ ] Rewrite the command:
  - resolve Clients with WFP-DC-01;
  - resolve the Live Retail and Live Forever numbers, asking if unsure;
  - accept 5-digit `16xxx`;
  - skip `_Forever`/`_Camelot` TOCs as forbidden shapes and report them;
  - update the README's supported-clients line if the standard requires it.
- [ ] Commit `WFP-DC-02: …`.

### Task WFP-DC-03: `wow-new-addon` dual by default
**Files:** `commands/wow-new-addon.md`.
- [ ] Defaults: the dual TOC line, the roster row with `Retail · Forever`, Compat-gated feature wiring, `KA0S_KIT_CLIENT` both profiles in the gate, and smoke for both clients. These follow `NEW_ADDON.md` (WFP-ST-04).
- [ ] Remove "Retail-only single `## Interface:`" at `:254` and update the report section at `:263`. Commit `WFP-DC-03: …`.

### Task WFP-DC-04: `bump-version` and `wow-automated-tests` run both profiles
**Files:** `profiles/wow/bump-version.md`, `commands/bump-version.md` if it duplicates it, and `commands/wow-automated-tests.md`.
- [ ] For a `retail+forever` addon, the release battery runs under `KA0S_KIT_CLIENT=retail` and `=forever`, and both must be green. The two-number Interface line is checked against the Live numbers. For the other values the behaviour is unchanged.
- [ ] Commit `WFP-DC-04: …`.

### Task WFP-DC-05: review agent and the WoW profile docs
**Files:**
- `profiles/wow/agent-review.md`: class 4 at `:443-500`, the line at `:655` and the API list at `:560-615`.
- `profiles/wow/diff.md:28` and `profiles/wow/sync-docs.md:71,97`.
- [ ] Class 4: uniformity is per client slot. The Retail slots must agree across siblings, and so must the Forever slots. A two-number line is clean for a `retail+forever` addon. It is a finding for a `retail-pending` addon only if the addon also gates features (half-ported).
- [ ] New checks: interface-number detection; `WOW_PROJECT_*` read outside Compat; `== WOW_PROJECT_MAINLINE` as "modern"; a Retail-only API reached from an ungated feature in a `retail+forever` addon; a filtered seed list; missing load-gating lines on a `retail` addon.
- [ ] Commit `WFP-DC-05: …`.

### Task WFP-DC-06: the CurseForge journal and Forever versions
**Files:** `scripts/curseforge_journal.py:478` and `scripts/test_curseforge_journal.py`.
- [ ] Write `test_journal_records_forever_version`: a file whose API `gameVersions` lists `["12.1.5","1.60.1"]` is recorded with both, and the chat/report shows both.
- [ ] If the test passes with no change, record WFP-DC-06 in `exceptions.tsv` with proof `python3 -m pytest scripts/test_curseforge_journal.py -k forever`. Otherwise fix it and commit `WFP-DC-06: …`. The test is committed either way, under WFP-DC-06.

### Task WFP-DC-07: release 2.8.0
- [ ] Bump `.claude-plugin/plugin.json` to 2.8.0, plus the README and CHANGELOG as the repo's `CLAUDE.md` requires. `test_command_specs.py` passes. Commit `WFP-DC-07: …`.

### Checkpoint CP-3, then merge gate B
- [ ] Review note, push the branch and notes, and log a `checkpoints.tsv` row.
- [ ] **Ask the owner for gate B.** On the go-ahead: merge `--no-ff` with subject `WFP-GATE-B: Merge …`, then push master.
- [ ] Ask the owner to update and reload the plugin. Then check: `cat ~/.claude/plugins/cache/dev-copilot/dev-copilot/*/.claude-plugin/plugin.json | grep version` shows 2.8.0. M4 does not start before this.

## Milestone M4: every addon (17 repos)

Abbreviations: AT AbsorbTracker, AM AuraMaster, BL BankLedger, CM ConsumableMaster, DR DpsRace, DW DropWatcher,
KC KickCD, ST LibKa0sSkinTester, LH LootHistory, MM MultiMeters, OR OutfitterReborn, PM PanelMaster,
PFE PartyFrameEnhanced, PGFE PremadeGroupsFilterExtension, PC PrettyChat, QC QuickComms, WG WhatGroup.

### Task WFP-ACE-00: the Ace3 proof (Ka0sAddonsCommonTasks)
**Files:** Create `docs/2026-11-07-WOW_FOREVER_PORT/ACE3_AC3D1225.md`, and `plan-data/ace3/` (a sparse clone, or the fetched module tree, pinned at `ac3d1225`).
- [ ] Fetch WoWUIDev/Ace3 at `ac3d1225`. Record the SHA and each module's MINOR (AceDB 40 expected, CheckBox 27, ColorPicker 29).
- [ ] Diff AceDB MINOR 33 (vendored) against 40. Prove that the Retail key is unchanged (Review Focus 4):
  - where `UnitNameUnmodified` can differ from `UnitName` on Retail;
  - the profile-name reset rule (empty, all spaces, or more than 50 characters), and whether any Ka0s default or migration creates such a name (`grep` every addon's `defaults` and migrations);
  - that the Forever-only branch sits behind `RegionalUniqueNamesEnabled()`.
- [ ] Write a headless check, `test_acedb_retail_key_stable`, in the doc as a runnable snippet against the kit's AceDB mock or the real AceDB loaded in the kit: a Retail character key built by MINOR 40 equals the MINOR 33 key. Run it and record the output.
- [ ] Diff the other vendored modules (33 → `ac3d1225`) and list anything that changes behaviour a Ka0s addon uses.
- [ ] If the proof fails, **stop and ask the owner**. Otherwise commit `WFP-ACE-00: …`.

### Tasks ACE-<abbr> (17): vendor Ace3 `ac3d1225`
Per addon, on the run branch:
- [ ] Replace each vendored Ace3 module folder under `libs/` with the `ac3d1225` copy. Add no modules and remove none. Keep the repo's declared EOL (run `normalize-eol` if the repo uses it).
- [ ] Update the Ace3 provenance (in `DEPENDENCIES.md` or wherever the repo records it) to `WoWUIDev/Ace3@ac3d1225 (untagged master; LibKa0s#76)`.
- [ ] Gate green. Commit `ACE-<abbr>: …`.

### Tasks RV-<abbr> (17): LibKa0s v1.92.0 and standard v2.103.0
- [ ] Run `/dev-copilot:wow-revendor-libka0s` (installed 2.8.0). It copies the payload and the kit at revision 52, and rolls the provenance. Adopt **no** candidates in this run, and decline each one with "deferred to the addon's Forever port". It files nothing; record the declines in the revendor bundle.
- [ ] Run `/dev-copilot:wow-revendor-standards` to move to v2.103.0.
- [ ] Add the roster value's TOC shape:
  - WG and PGFE: add the two load-gating lines (Global Constraints).
  - The others: no TOC change.
- [ ] Gate green under `KA0S_KIT_CLIENT=retail`. Every RV commit uses the subject prefix `RV-<abbr>: `, including the commits the commands make. Amend the command's subject if it does not carry the prefix.

### Checkpoint CP-4
- [ ] For each of the 17, check the gate totals, and read a review note over the ACE and RV diffs.
- [ ] Push the 17 branches and notes, and log a `checkpoints.tsv` row with every head.

## Milestone M5: owner smoke (Retail) and finalize

### Task WFP-SMOKE
- [ ] The owner runs `03_SMOKE_TESTS.md` (SM-R1..R5 on Retail, plus SM-F1 on Forever) and Claude records the results.
- [ ] Failures become new items with the id `FIX-<n>`, in the owning repo.

### Task WFP-FIN: finalize (only on the owner's go-ahead)
- [ ] Run `/dev-copilot:finalize` across LibKa0s, the 17 addons and Ka0sAddonsCommonTasks, in dependency order. Push the `v1.92.0` tag. Delete every run branch, stash and worktree.
- [ ] Write `99_REPORT.md`, update memory, and comment on LibKa0s#44 with the outcome (link #76).
