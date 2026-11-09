# WoW Forever port, steps 1–4: design

Date: 2026-11-07. Run branch: `feat/2026-11-07-wow-forever-port`, the same name in every repo this touches.
Inputs: `reports/WoW Forever porting research.md` (the research), `research_notes/` (its sources) and
`00_OWNER_CHECKS_AND_RULINGS.md` (in-game checks and rulings). Anything marked **(Claude's call)** was decided
while designing and was not a decision the owner made. The owner can overturn any of those while reading.

## 1. Intent

The owner is porting the whole Ka0s collection to **WoW Forever** (Blizzard's vanilla-era game type "Camelot":
client 1.60.1, interface 16001, `WOW_PROJECT_ID == WOW_PROJECT_CAMELOT == 18`). Each existing addon repo will serve
**both Retail and Forever from one codebase**. There are no separate Forever addons and no Classic flavours.
From 2026-11-07, **all** Ka0s work (addons, the library, the standard and the tooling) builds for both clients.

This design covers the groundwork that makes that possible. Per-addon ports (step 5) come after it, one addon at
a time, each with its own owner decision.

1. **The standard** permits and governs dual-client addons.
2. **LibKa0s** provides the single way to ask "which client am I on", gate features by client, and read the spec on
   Forever. Its test kit can run suites as either client.
3. **Every addon** vendors an Ace3 that works on both clients, together with the new LibKa0s.
4. **dev-copilot** knows each addon's clients and builds, bumps, reviews and audits for both.

## 2. What the owner decided (2026-11-07)

- **Both clients, one repo.** No Classic.
- **A feature is absent on the client that cannot support it, not broken or greyed out.** Re-architect, so that a
  Forever player never sees a Retail-only feature (group finder, warband bank, Mythic+, transmog, Encounter Journal
  and so on), and a Retail player never sees a Forever-only one.
- **Seed lists are per client.** That covers spells, items, talents and similar seeded data, and the actions built
  on them. Forever gets its own lists, not filtered Retail lists.
- **WhatGroup and PremadeGroupsFilterExtension stay Retail-only** for now. They are not ported.
  *Amended 2026-11-10:* **DpsRace is Retail-only too**, by the owner's ruling ("there are no training dummies in
  forever so this makes no sense"); recorded in `../2026-11-07-WOW_FOREVER_PORT_STEP5/00_CLASSIFICATION.md` §1.
- **The standard changes** to allow dual-client support.
- **Ace3 is vendored from untagged master** at commit **`ac3d1225`** (2026-10-28, the master head on 2026-11-07), and
  there is **no shim**. The reason is to get CheckBox v27, ColorPicker v29 and the AceDB Forever profile-key scheme
  now, so that no Forever player's profile keys ever change. LibKa0s#76 stays open to move to Ace3's first tagged
  release that contains this commit.
- **dev-copilot changes**, and every command builds for both clients from now on.
- **Feature-level addons** (BankLedger, LootHistory, DropWatcher, MultiMeters, DpsRace, KickCD, OutfitterReborn) are
  decided one at a time in step 5, not here.

## 3. Goals, non-goals and anti-goals

**Goals**
- A standard that a dual-client addon can comply with, and that tells an auditor exactly what compliance looks like.
- One LibKa0s seam for client detection and feature gating, tested headless as each client.
- No Ka0s checkbox, colour picker or profile breaks on either client because of old Ace3. This also closes today's
  latent Retail bug: `SetDesaturation` has been gone since 12.1.0, and only a third-party CheckBox v27 masks it.
- dev-copilot commands that do the right thing for a dual-client addon and for a Retail-only addon.

**Non-goals (this run)**
- Porting any addon's features, seed lists or TOC to dual-client. That is step 5.
- Releasing anything to CurseForge, bumping addon versions or cutting tags, other than the LibKa0s tag that addons
  re-vendor. This follows the repo's usual rule: never without the owner's go-ahead.
- Classic flavours.

**Anti-goals (a failure even if everything technically works)**
- Detection by interface number, such as `select(4, GetBuildInfo()) >= 100000` or `16xxx` ranges. The common
  Retail test is false on 16001 and sends Forever down Classic paths.
- `WOW_PROJECT_ID == WOW_PROJECT_MAINLINE` used as "modern client". It excludes Forever.
- Features hidden at runtime but still registered: a settings page that exists but is empty, or a slash verb that
  answers "not available". The rule is that a feature is never built on the wrong client.
- Editing a vendored library file, Ace3 included.
- A global put back for other addons' benefit (the Questie-style `SetDesaturation` shim).
- Any change to Retail players' AceDB profile keys from the Ace3 upgrade.

## 4. Constraints

- Every repo's own `CLAUDE.md` governs work inside it: its green gate (`lua tests/run.lua`,
  `~/.claude/dev-copilot/bin/ka0s-bounded luacheck .` with 0 warnings and 0 errors, the 1500-line cap) and its
  conventions.
- Git is the only state: one commit per item, with the subject `<ID>: …`. Feature branches are pushed only at
  milestone checkpoints. Merging to master happens only on the owner's go-ahead, through `/dev-copilot:finalize`.
  **This run has two mid-run merge gates** (owner ruling, 2026-11-07, §9): the commands and the plugin read only
  `master`, so the standard and dev-copilot must reach `master` before step 3.
- In-game smoke is the owner's to run. Claude never marks a smoke check passed.
- The game loads `GIT/<Addon>` through symlinks. Build on the branch checked out in the main repo folder, never in a
  side worktree.
- dev-copilot runs from the installed plugin. After dev-copilot changes are pushed, the owner updates and reloads
  the plugin before any later step relies on the new behaviour.
- GitHub writes are spaced out.

## 5. Step 1: the standard (WowAddonStandards)

The standard goes from "Retail only" to "**Retail and Forever, declared per addon**".

### 5.1 The rules that change

The research found the Retail-only rules at `toc-file.md:57-65`, `compat.md:5,42`, `anti-patterns.md:15,21` (#9, #15),
`packaging.md:46`, `versioning-git.md:8`, `layout.md:11,29`, the README-badge and client-quirks rules, and
`open-evolutions.md:349-352` (WoW:F "recorded, not ruled"). Each one is rewritten and none is simply deleted, and the
open evolution is closed as ruled.

### 5.2 New normative content

1. **Clients are declared in the roster.** `ADDONS.md` gains a **Clients** column, which takes one of three values:
   - `Retail · Forever`: ported, and dual-client.
   - `Retail`: Retail-only **by the owner's decision**. Today these are WhatGroup and PremadeGroupsFilterExtension.
   - `Retail (port pending)`: not ported yet. Every other roster addon has this value until its step-5 port flips it.
   **(Claude's call,** settling a contradiction the builder check found.) A port-pending addon carries no load-gating
   lines, because Forever players already run some of these addons "out of date" (PartyFrameEnhanced#15) and must not
   be cut off. The audit and review agents do not flag a port-pending addon for missing dual-client shapes. They do
   flag a new ungated Retail-only feature. dev-copilot and the audit read this column, and it is the single source
   of truth.
2. **TOC.**
   - A dual-client addon has one unsuffixed TOC with `## Interface: <retail>, <forever>`, today `120105, 16001`. Per-
     flavour TOC files stay forbidden, which keeps one TOC as the rule.
   - A `Retail` (by decision) addon keeps one number and **adds** `## AllowLoadGameType: standard` and
     `## ExcludeLoadGameType: camelot`, so that Forever never lists it. Both lines are needed, because the wiki warns
     that an allow-list the client does not recognise counts as a match.
   - The builder confirms the exact directive spelling against warcraft.wiki.gg's TOC format page.
3. **Client detection** goes **only** through `LibKa0s-Compat-1.0`: `IsForever()`, `IsRetail()`. Addon code never reads
   `WOW_PROJECT_*` and never compares interface numbers. The new anti-pattern names the interface-number test and the
   `== WOW_PROJECT_MAINLINE` test as the two banned shapes. Feature detection (`if C_Foo then`) stays allowed for a
   *specific* API gap inside a feature the client supports. It never decides whether a whole feature exists.
4. **Per-client features.** Every feature (module, settings page or tab, slash verb, launcher menu entry, keybinding,
   event registration) that exists on only one client is **declared** with its client and **gated at registration**,
   through the LibKa0s gate (§6.2). Hiding or disabling it at runtime does not meet the rule. A feature with no
   declaration serves both clients. The ARCHITECTURE doc carries a per-client feature table.
5. **Per-client seed data.** Seeded lists (spells, items, talents and similar) and the actions built on them live
   in separate per-client tables or files, selected once through Compat. **(Claude's call:** a file pair such as
   `data/Seeds_Retail.lua` and `data/Seeds_Forever.lua`, or one file with `Retail = {…}` and `Forever = {…}` tables, are
   both compliant. The rule is "two lists, picked once", not a file layout.) Filtering one Retail list at runtime is
   non-compliant.
6. **Compat scope.** `compat.md` widens from "Retail patch differences, not across game flavours" to "Retail patch
   differences and the Retail/Forever split". The flavour helpers are a collection-wide seam that the standard
   mandates. They therefore satisfy library-stack-§7's two-consumer bar by ruling, and the standard says so
   explicitly, not by counting callers.
7. **Smoke and testing.** A dual-client addon's `docs/smoke-tests.md` covers both clients, and its headless suite runs
   under both kit profiles (§6.3).
8. **README badge and packaging.** The README states which clients the addon supports, and the packaging rules accept
   a two-number Interface line. Before any addon relies on it, the first step-5 port verifies that CurseForge tags a
   file for both clients from that line.
9. **The playbooks** that ship with the standard (`AUDIT.md`, `NEW_ADDON.md`, `AUTOMATED_TESTS.md`, and
   `NEW_ADDON_CONTEXT.md` where it restates rules) are updated to match.

### 5.3 Shape of the change

This is one standard release with the full ripple: section text, index blurbs in `STANDARDS.md`, anti-pattern
entries, `CHANGELOG.md`, the version bump (the next minor, v2.103.0, unless the standard's own versioning rule makes
this a major), the context pack and the playbooks. **(Claude's call:** run `/dev-copilot:wow-revendor-standards` per
addon only in step 3, after LibKa0s is tagged, so that each addon commits once.)

## 6. Step 2: LibKa0s

### 6.1 Flavour helpers in `LibKa0s-Compat-1.0` (new minor)

- `IsForever()`: true only when `WOW_PROJECT_CAMELOT ~= nil and WOW_PROJECT_ID == WOW_PROJECT_CAMELOT`. Both values are
  read bare at call time, following Compat's own rule 1. The test for nil is mandatory: in a harness without the
  constant, `nil == nil` is true, and every client would read as Forever.
- `IsRetail()`: `WOW_PROJECT_ID == WOW_PROJECT_MAINLINE` **and not** `IsForever()`. On any other client both helpers
  answer false. Ka0s supports neither of the other clients, so no third helper is added. **(Claude's call:** a
  `ClientKey()` that answers `"retail"`, `"forever"` or `nil` is added for indexing per-client tables, so that seed-data
  selection never repeats the two-branch `if`.)

### 6.2 Feature gating

A small gate that addons use at registration time, for example `Compat.ForClient("retail"|"forever"|"both")` returning a
boolean, or a descriptor field `clients = { "retail" }` honoured by the library's registries. The library's own
registration points honour the descriptor field: Options pages and tabs, Slash verbs, Launcher menu entries, the
Keybinds editor rows and Lifecycle/Bus registrations. **(Claude's call:** the descriptor field is the primary form,
because the library already owns those registries; the boolean form is for host-owned registrations.) An entry gated
off is never created. It is not created and then hidden. The exact API shape is the builder's choice, and it is recorded
in `docs/api/Compat/`.

### 6.3 Spec readers on Forever

`GetSpecialization` and `GetSpecializationInfo` are nil on Forever (confirmed in game, 2026-11-07). Compat's existing
spec readers already try `C_SpecializationInfo` first (`LibKa0s/LibKa0s/Compat.lua:270-295`), and the research found
that namespace on Forever. The work is therefore to verify that rung on Forever and to document what Forever's spec
values mean, both from the Gethe/wow-ui-source `forever` branch, and to add an owner smoke `/dump` of the readers.
If the namespace is present but answers nothing meaningful, the readers answer `nil` there. **(Claude's
call:** if Forever has no specialization concept, the readers answer `nil` on Forever and say so in the API document,
and consumers already handle nil. The readers never raise and never invent a spec.)

### 6.4 Test kit and lint

- **A Forever kit profile.** The mock gains an opt-in Forever profile, with `WOW_PROJECT_ID = 18`,
  `WOW_PROJECT_CAMELOT = 18`, `GetBuildInfo` answering 1.60.1/16001, and the Forever-absent globals removed, at least
  `GetSpecialization*`. A suite can run under `retail` (the default), `forever`, and `retail` with
  `WOW_PROJECT_CAMELOT` undefined, which is how live Retail really looks. LibKa0s's own suites cover the helpers and the
  spec rungs under all three profiles.
- **Lint.** The project constants (`WOW_PROJECT_ID`, `WOW_PROJECT_MAINLINE`, `WOW_PROJECT_CAMELOT`) are added to the
  `.luacheckrc` globals template.
- **(Claude's call, a SHOULD for the builder:** a static check that flags calls to globals absent on either client.
  The source is the Ketho/BlizzardInterfaceResources `live` and `forever` global lists. It would have caught
  `SetDesaturation`, which headless tests cannot see because AceGUI is faked. If it is too large for this run, it is
  filed as a LibKa0s issue rather than dropped.)

### 6.5 Release

The library takes a version bump and a new tag (the next minor after v1.91.0). The tag is pushed only with the owner's
authorization at the milestone checkpoint.

## 7. Step 3: every addon (all 17 roster addons)

In each addon, on the run branch:

1. **Ace3 at `ac3d1225`.** Copy the Ace3 modules the addon already vendors (no more and no fewer: see library-stack's
   "vendor what you use") from WoWUIDev/Ace3 at `ac3d1225`. Record the provenance as that commit, not a tag. The minimum
   result is AceGUI CheckBox v27, ColorPicker v29 and AceDB MINOR ≥ 40.
   - **Retail profile-key check:** before committing, the builder proves that AceDB's character and realm key is
     unchanged on Retail. Do it with a headless test or a read of the AceDB diff, since the Forever changes are behind
     `RegionalUniqueNamesEnabled()`. MINOR 40 also switches the Retail character key to `UnitNameUnmodified`, and it
     resets any stored profile name that is empty, all spaces or longer than 50 characters. The proof covers both
     changes, and states when `UnitNameUnmodified` can differ from `UnitName`. Record the evidence.
     - Context: the owner's `_retail_` already loads AceDB MINOR 39 and 40 from third-party addons, and LibStub keeps
       only the highest minor, so the owner's own install already runs this code. A player with only Ka0s addons
       does not.
   - Every addon vendors the same unpatched Ace3 copy, so the re-vendor is mechanical (builder check, 2026-11-07).
2. **Re-vendor LibKa0s** to the new tag with `/dev-copilot:wow-revendor-libka0s`, and adopt nothing beyond what this run
   needs.
3. **Refresh the standards reference** to the new standard version with `/dev-copilot:wow-revendor-standards`.
4. **Retail-only addons** (WhatGroup and PremadeGroupsFilterExtension) get the two load-gating TOC lines from §5.2.
   **(Claude's call:** it is cheap and the owner has already decided these two, so it lands now and not in step 5.)
   Every other addon's TOC is left unchanged until its port.
5. Green gate, then one commit per item.

Other vendored libraries (LibSharedMedia, LibDBIcon, LibDataBroker, LibCustomGlow) are **not** refreshed in this run
unless the survey shows one breaks on Forever. **(Claude's call:** the research found no breakage. Their Forever-
readiness is checked per addon in step 5.)

## 8. Step 4: dev-copilot

A dev-copilot minor release (2.8.0). Every Ka0s-WoW-aware command reads each addon's **Clients** from `ADDONS.md`.

- **`wow-bump-interface`** bumps each declared client's number in place on the Interface line: the Live Retail
  number, plus the Live Forever number for a dual-client addon. It must never collapse a two-number line to one. It
  learns the current Forever interface, and recognises `_Forever` and `_Camelot` TOC names in its skip and sanity
  logic. A five-digit `16xxx` is valid for Forever.
- **`wow-new-addon`** scaffolds dual-client by default: the two-number TOC, the flavour-gate wiring, the Forever kit
  profile in the test run, and smoke checklists for both clients. The `NEW_ADDON.md` playbook changes with it (§5.2.9).
- **`bump-version`** gates on the full battery under both kit profiles for a dual-client addon, and checks the
  two-number Interface line.
- **The review agent** stops flagging a two-number Interface line as a finding. It flags interface-number
  detection, `== WOW_PROJECT_MAINLINE` used as "modern", ungated features that use Retail-only APIs in a dual-client
  addon, and filtered (not split) seed lists.
- **The audit agent** follows the updated `AUDIT.md`, and needs no logic beyond that.
- **`wow-automated-tests`** runs both kit profiles for a dual-client addon.
- **The CurseForge journal** (`curseforge_journal.py`) recognises the Forever game-version type (88568) when it
  records a file's versions, so a dual file shows as both. **(Claude's call:** this is included because it is small
  and the first step-5 release would otherwise be journaled wrong.)
- The tests in `scripts/test_*.py` and `test_command_specs.py` cover the new behaviour.

## 9. Order and checkpoints

1. **Standard** (step 1). Commit, push the branch at the checkpoint, then the review.
   - **Merge gate A (owner ruling, 2026-11-07):** on the owner's go-ahead, merge WowAddonStandards to `master`
     (`--no-ff`) and push. `wow-revendor-standards`, the audit, `wow-new-addon` and the other commands fetch the
     standard from `raw.githubusercontent.com/.../WowAddonStandards/master`. Precedent: DR-OW-07 in
     `docs/2026-09-25-DIAGNOSTICS_COMMAND/03_EXECUTION_PLAN.md`.
2. **LibKa0s** (step 2), with its tag. This depends on step 1, because the docs cite the new rules. Its tag is
   pushed at its checkpoint, with authorization. `wow-revendor-libka0s` reads the newest tag from the local checkout,
   so no master merge is needed before step 3.
3. **dev-copilot** (step 4). This depends on step 1. Push the branch at its checkpoint, then the review.
   - **Merge gate B (owner ruling, 2026-11-07):** on the owner's go-ahead, merge dev-copilot to `master` and push.
     The owner then updates and reloads the plugin, because the plugin installs from the `tusharsaxena/dev-copilot`
     marketplace, which serves `master`. Step 3 waits for the owner to confirm the reload, then checks the installed
     version (2.8.0).
4. **Addons** (step 3), after steps 2 and 4 and both merge gates.
5. **Owner smoke, Retail only.** No addon is dual-client yet.
   - For each addon: open the settings, toggle a checkbox, change a colour (alpha included), and confirm the profile
     is intact after `/reload`.
   - With every non-Ka0s addon disabled, confirm checkboxes work. This proves the v27 fix comes from Ka0s itself.
   - Results go in the bundle's smoke file.
6. Merge LibKa0s and the 17 addons, plus this repo's bundle, on the owner's go-ahead.

Each milestone gets a checkpoint entry (test totals and pushed heads) and an independent review recorded as a
`refs/notes/ka0s-review` note, following the bundle conventions in this repo's `CLAUDE.md`.

## 10. Left to the builder

- The plan's item ids, the milestone split, `items.tsv`, `resume-state.sh` and `RESUME.md`.
- The exact Compat API names and signatures, as long as they follow §6.
- How the Forever kit profile is selected (an environment variable, a runner flag or a suite header).
- The exact wording of the new and rewritten standard sections.
- Whether the static global-presence check (§6.4) fits this run.
