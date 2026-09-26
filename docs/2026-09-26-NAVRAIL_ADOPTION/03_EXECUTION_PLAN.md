# NavRail adoption Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:subagent-driven-development. This plan is
> executed by a Workflow with one implementer and one independent reviewer per task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Bring LibKa0s v1.61.0 (the pinned nav rail, `O.NavRail`) into the ten addons that still
vendor v1.60.0. Then give MultiMeters its one-page-per-window Windows page (MultiMeters#55) and
KickCD its Grid page (KickCD#33), both built on AuraMaster's shipped pattern: the picker band on top,
the rail on the left, and each entry's own tab strip to its right, over the one scroll.

**Architecture:** Nothing upstream changes. Each addon copies `LibKa0s/` from the `v1.61.0` tag, and
its library-absent stub gains a `NavRail` no-op. In MultiMeters, a section registry above the fork in
`settings/OptionsSetup.lua` names the Windows page's seven entries. Each entry is a former page key,
so every schema row is untouched. `Helpers.RenderWindowPage` does the rest: it cancels any column
drag, then draws the band, the rail and the entry's own strip. KickCD does the same in
`settings/Panel_Render.lua`: `Helpers.RenderGridPage` hands the rail to the existing
`Helpers.RenderUnitPanel` through a new chrome hook, so the rail sits between the Unit band and
either strip path, linked Focus included. Around each renderer the host keeps the per-entry tab
memory, deep links (`SelectSection`, the `SelectTab` route) and Defaults. The old pages then retire.

**Tech Stack:** Lua 5.1 (WoW client), Ace3 (AceGUI-3.0), LibStub, LibKa0s v1.61.0 (vendored), and the
headless kit (`tests/run.lua`, LibKa0s test kit revision 27). Tooling: luacheck, lizard, zsh, perl,
git.

**Spec:** `02_SPEC.md` in this bundle (the owner's design, 2026-09-26), whose §9 resolves every open
point. The pattern it follows is AuraMaster's
`docs/superpowers/specs/2026-09-26-settings-redesign-design.md`, with code on AuraMaster `master`
`b51aee8`: `settings/OptionsSetup.lua` :184-209 (the registry), :500-599 (`railSections`,
`settleSection`, `stashTab`, `RenderContainerPage`, `SelectSection`, the `SelectTab` route) and
:313-331 (`NS.OpenOptionsPage`). Read both before any M2 task.

---

## Global Constraints

Every task honors every line here. A reviewer rejects a task that breaks one.

- **Read-only upstreams.** LibKa0s, WowAddonStandards and AuraMaster are never written. The payload
  comes from the tag `v1.61.0` (`c6183bd`), never from a working tree. A library defect stops the
  task: report it, and it ships as `v1.61.1` under its own plan.
- **Rail width 120**, the library default. No host passes `width`.
- **Draw order is PageBanner -> NavRail -> TabStrip** on every full render of a railed page.
- **Schema paths unchanged.** No row's `path`, `page`/`panel`, `section`, `unit`, `group`, `default`
  or `label` changes. A rail entry key *is* the former page key: MultiMeters `windows`, `frame`,
  `header`, `bars`, `tooltip`, `visibility`, `columns`; KickCD `icons`, `castbar`, `label`.
  `desc` strings may be reworded (NR-MM-04, 02_SPEC R15).
- **Session state is never persisted.** `ctx.activeSection`, `ctx.activeTab` and `ctx.sectionTabs`
  live on the ctx only. Nothing about the rail or the tabs is written to `MultiMetersDB` or
  `KickCDDB` (options-ui-§13).
- **The rail is not a picker** (options-ui-§14). The band stays the only picker, and changing the
  window or unit leaves the entry and its tab alone.
- **1500-line file cap** (layout-§1), enforced by each addon's `test_layout_cap`.
- **CCN 15.** No new function above cyclomatic complexity 15 (lizard, `libs/` and `tests/_kit/`
  excluded).
- **luacheck 0/0** at every commit.
- **Line endings.** Every one of the ten addons pins `* text=auto eol=crlf`, so every file written
  there, new ones included, is **CRLF**. Run the `crlf` shorthand below on every file a step writes
  or edits. It normalizes the file and prints `EOL FAIL <file>` if any line still lacks `\r`. A
  `sed`/`echo` insert without `\r` turns the kit's `test_eol` red, which the dry run proved in seven
  addons. This bundle is **LF**.
- **Bounded runner.** Every `lua`, `lua5.1`, `luacheck` and `lizard` run goes through
  `/home/tushar/.claude/wow-addon/bin/ka0s-bounded`, spelled out. A PreToolUse hook blocks unbounded
  runs, and it matches on the literal path.
- **No version bumps, tags, pushes or merges.** No addon's TOC `## Version`, version history or
  Version badge changes. The README **Tests** badge moves with `docs/test-cases.md`, because both
  addons' CLAUDE.md files require it. Nothing is pushed (not authorized), and nothing is merged.
- **One branch name in all ten repos: `feat/2026-09-26-navrail-adoption`**, cut from `master` by each
  repo's NR-XX-01 Step 1.
- **Commits.** One task per commit. The subject starts `<ID>: `, and review fixes are `<ID>R: `.
  Messages end with the executing session's attribution trailers (`$TRAILERS` below). Stage named
  files only (`git add <path> ...`), never `git add -A` or `.`.
- **Every commit is green:** the repo's full gate passes on the committed tree. A task that cannot
  get green stops and reports. It never commits red.
- **In-client smoke checks are the owner's.** Claude writes them and never marks one passed.
- **US English, `filename-§N` references only.** README prose edits go through the `humanize` skill
  before commit.
- **Scope.** The M1 items touch only the library copy, the provenance line, the lines that state the
  vendored version, the stub and the hand-typed library lists. Only NR-MM-* and NR-KC-* touch page
  code.

### Command shorthands used below

Define these once per shell (zsh):

```sh
GIT=/mnt/d/Profile/Users/Tushar/Documents/GIT
BR=feat/2026-09-26-navrail-adoption
# The commit attribution lines: first write the lines the executing session's system reminder gives
# for commits, verbatim, one per line, to /tmp/navrail-trailers.txt. Every commit below ends with them.
TRAILERS=$(< /tmp/navrail-trailers.txt)

# CRLF: normalize every line of each file to \r\n, then prove it.
crlf() {
  local f
  for f in "$@"; do
    perl -pi -e 's/\r?\n\z/\r\n/' "$f"
    [[ "$(grep -c $'\r$' "$f")" == "$(wc -l < "$f" | tr -d ' ')" ]] || echo "EOL FAIL $f"
  done
}

# The v1.61.0 library payload, from the TAG. Run in the addon root. Records both deltas in
# /tmp/<Addon>-libs.diff and /tmp/<Addon>-kit.diff (read by rv_bundle), copies LibKa0s/ only, and
# proves the copy byte for byte.
lk_copy() {
  local S a=${PWD:t}
  S=$(mktemp -d)
  git -C $GIT/LibKa0s archive v1.61.0 LibKa0s testkit | tar -x -C "$S"
  diff -rq --strip-trailing-cr "$S/LibKa0s" libs/LibKa0s | sed "s|$S/|<tag>/|g" > /tmp/$a-libs.diff
  diff -rq --strip-trailing-cr "$S/testkit" tests/_kit   | sed "s|$S/|<tag>/|g" > /tmp/$a-kit.diff
  cat /tmp/$a-libs.diff; echo "kit delta lines: $(wc -l < /tmp/$a-kit.diff)"
  cp -r "$S/LibKa0s/." libs/LibKa0s/
  diff -r "$S/LibKa0s" libs/LibKa0s && echo "libs/LibKa0s == v1.61.0 byte for byte"
}

# The docs/revendor/<date>-v1.61.0/ bundle, in the shape of each addon's 2026-09-26 v1.60.0 one.
# $1 = the decision for 03_DECISIONS.md; $2 = the test run's totals line; $3 = luacheck's totals line.
rv_bundle() {
  local a=${PWD:t} d=docs/revendor/$(date +%F)-v1.61.0
  local tagc=$(git -C $GIT/LibKa0s rev-parse --short 'v1.61.0^{}')
  mkdir -p $d
  {
    print -r -- "# LibKa0s v1.60.0 -> v1.61.0: the delta ($a)"
    print -r -- ""
    print -r -- "Copied from the tag \`v1.61.0\` (\`$tagc\`), never from a working tree."
    print -r -- ""
    print -r -- "## libs/LibKa0s (\`diff -rq --strip-trailing-cr\`, before the copy)"
    print -r -- ""
    print -r -- '```'
    cat /tmp/$a-libs.diff
    print -r -- '```'
    print -r -- ""
    print -r -- "- \`Options.lua\`: minor 24 -> 25. The scroll's left anchor reads \`lib.__railInset\`; \`lib:New\` attaches the nav half (\`lib.__AttachNav\`)."
    print -r -- "- \`OptionsTabs.lua\`: minor 4 -> 5. The strip and the content panel start right of a nav rail."
    print -r -- "- \`OptionsNav.lua\`: new, minor 1. \`O.NavRail(ctx, spec)\`, the pinned nav rail (options-ui-§13)."
    print -r -- "- \`LibKa0s.xml\`: loads \`OptionsNav.lua\` after \`OptionsScroll.lua\`."
    print -r -- "- The Options major key moves from \`24.31.4.7.4\` to \`25.31.5.7.4.1\`. With no rail drawn the inset is 0: no page moves."
    print -r -- ""
    print -r -- "## tests/_kit"
    print -r -- ""
    print -r -- "\`testkit/\` is identical at v1.60.0 and v1.61.0 (kit revision 27): $(wc -l < /tmp/$a-kit.diff) differing files, so \`tests/_kit\` is not copied."
  } > $d/01_DELTA.md
  {
    print -r -- "# Candidates ($a)"
    print -r -- ""
    print -r -- "| # | Surface | What it offers | Blocker? |"
    print -r -- "|---|---|---|---|"
    print -r -- "| C1 | \`O.NavRail\` (OptionsNav minor 1) | A pinned first-level nav rail for a page that edits one instance out of many and would otherwise be several sub-pages retargeted by one picker (options-ui-§13, §14). | No: a new member; the stub owes a \`NavRail\` no-op. |"
  } > $d/02_CANDIDATES.md
  {
    print -r -- "# Decisions ($a)"
    print -r -- ""
    print -r -- "- **C1 \`O.NavRail\`:** $1"
    print -r -- "- The library-absent stub gains \`NavRail\` (or, where the host keeps a hand-typed library list, that list gains \`OptionsNav\`), so the surface-parity case stays green."
    print -r -- "- Plan: \`Ka0sAddonsCommonTasks/docs/2026-09-26-NAVRAIL_ADOPTION/\`."
  } > $d/03_DECISIONS.md
  {
    print -r -- "# Summary ($a)"
    print -r -- ""
    print -r -- "LibKa0s v1.60.0 -> v1.61.0 from the tag; \`tests/_kit\` unchanged at kit revision 27; CLAUDE.md provenance rolled."
    print -r -- ""
    print -r -- "Gate after the copy and the stub:"
    print -r -- ""
    print -r -- "- tests: $2"
    print -r -- "- luacheck: $3"
  } > $d/05_SUMMARY.md
  crlf $d/*.md
}
```

The kit prints each case as `  PASS  <name>`, `  FAIL  <name>` or `  SKIP  <name>`. "Run it and see it
fail" means: run the repo's `tests/run.lua` through the bounded runner into a file and grep it:
`grep -E '^  (FAIL|PASS)  <prefix>' /tmp/<repo>-run.txt`. The kit has no per-suite filter.

**The addon gate** (run in the addon's root; the per-task text names any addition):

```sh
/home/tushar/.claude/wow-addon/bin/ka0s-bounded lua tests/run.lua > /tmp/${PWD:t}-run.txt 2>&1
tail -3 /tmp/${PWD:t}-run.txt; grep -c '^  FAIL' /tmp/${PWD:t}-run.txt        # expect 0
/home/tushar/.claude/wow-addon/bin/ka0s-bounded luacheck . | tail -2          # expect 0 warnings / 0 errors
```

M2 tasks add lizard (MultiMeters and KickCD call it optional, but the collection's CCN 15 applies to
new code):

```sh
/home/tushar/.claude/wow-addon/bin/ka0s-bounded lizard -l lua -C 15 -w -x "./libs/*" -x "./tests/_kit/*" .   # expect no output
```

---

## Review Focus

These are the five failure modes a player is likeliest to hit that no test pins today. Each one gets
a test in the task that owns it. A reviewer checks that the test exists, fails without the fix, and
passes with it.

1. **A rail click away from Columns mid-drag hands a live drag handle to a pooled frame.**
   `settings/ColumnBlocks.lua:210` `NS.CancelReorder(ctx)` must run **before** `ClearScroll`.
   Today only Columns' own render does that (`settings/Columns.lua:312-318`). On the Windows page
   the seven entries share one ctx, and a rail click re-renders the whole page. Owned by
   **NR-MM-02**, test "Windows rail: leaving Columns on the rail mid-drag cancels the reorder BEFORE
   the scroll clear".
2. **Defaults on the Windows page resets the wrong rows, or renames the window.**
   `EnsureDefaultsButton` captures `panel.defaultsOnClick` once, at the first show
   (`libs/LibKa0s/Options.lua` ~:809). A closure that fixed the entry at build time would reset
   General's rows from Frame. A row walk on General would write `window.name`'s default
   ("Multi Meters", `settings/Schema.lua:178`). Owned by **NR-MM-02**, test "Windows rail: Defaults
   restores the active entry's rows for the active window; General keeps the name; Columns restores
   both halves".
3. **Returning to an entry forgets its tab.** A strip click is handled inside the library
   (`RenderTabbedSchema` sets the scalar `ctx.activeTab` and re-renders itself), so the host never
   sees it. A host that stashed the tab only on its own renders would lose Cast bar -> Font after a
   trip to Icons (KC-S4). Owned by **NR-KC-02**, test "grid: each entry keeps its own tab, including
   one chosen by the library's own strip click". MultiMeters' equivalent is pinned in NR-MM-02 too.
4. **KickCD's Defaults resets the unit off screen.** The library's `O.RestoreDefaults` omits the unit
   filter on purpose (`libs/LibKa0s/Options.lua:986-1007`), so wiring the Grid button to it would
   reset Focus's cast bar while Target is in the band. That contradicts the owner's ruling (KC-S7).
   Owned by **NR-KC-03**, test "grid: Defaults restores only the active entry's rows, for the unit in
   the band".
5. **A link written against a retired page key lands nowhere.** Once Icons, Cast bar and Text Label
   retire, `NS.Settings.categoryFor.castbar` is nil and `Helpers.__panelFor("castbar")` finds nothing,
   so `Helpers.OpenPageTab("castbar", tab)` would silently return false. The page is hidden while
   the settings window is closed, so the entry must be selected on a hidden (dirty) page and drawn on
   its next show. Owned by **NR-KC-03**, test "grid: a former page key opens Grid on that entry and
   tab, drawn on its next show". MultiMeters' `NS.OpenOptionsPage` is pinned the same way in
   NR-MM-03.

The combat lock over the rail is the library's (pinned in LibKa0s's own suite). Each addon's
`SelectSection` combat refusal is pinned in NR-MM-03 and NR-KC-03.

---

## Spec resolutions

`02_SPEC.md` §9 (R1-R18) resolves every open point. The ones that shape code are cited at the step
that implements them.

---

## Task index

| ID | Repo | Title | Depends on |
|---|---|---|---|
| NR-AT-01 | AbsorbTracker | Re-vendor v1.61.0; stub `Helpers.NavRail` | — |
| NR-BL-01 | BankLedger | Re-vendor v1.61.0; stub `NavRail`; `docs/test-cases.md` regenerated | — |
| NR-CM-01 | ConsumableMaster | Re-vendor v1.61.0; Options inventory gains `OptionsNav` | — |
| NR-KC-01 | KickCD | Re-vendor v1.61.0; stub `NavRail`; Options-file count 6 | — |
| NR-LH-01 | LootHistory | Re-vendor v1.61.0; stub `NavRail`; `LIB_FILES` gains `OptionsNav.lua` | — |
| NR-MM-01 | MultiMeters | Re-vendor v1.61.0; stub `NavRail` | — |
| NR-PM-01 | PanelMaster | Re-vendor v1.61.0; stub `NavRail`; vendor diff gate | — |
| NR-PF-01 | PartyFrameEnhanced | Re-vendor v1.61.0; stub `NavRail` | — |
| NR-PC-01 | PrettyChat | Re-vendor v1.61.0; stub `NavRail` | — |
| NR-WG-01 | WhatGroup | Re-vendor v1.61.0; loader loads `OptionsNav.lua`; stub `H.NavRail`; vendor diff gate | — |
| NR-MM-02 | MultiMeters | The Windows page: registry, rail renderer, per-entry tabs, General, Columns hook, Defaults | NR-MM-01 |
| NR-MM-03 | MultiMeters | Deep links: `NS.OpenOptionsPage`, `SelectSection`, the `SelectTab` route | NR-MM-02 |
| NR-MM-04 | MultiMeters | Retire the six sub-pages; wording; tests; docs; smoke §36 | NR-MM-03 |
| NR-KC-02 | KickCD | The Grid page: registry, rail through RenderUnitPanel's chrome hook, per-entry tabs | NR-KC-01 |
| NR-KC-03 | KickCD | Defaults for the selected unit (deviation row); deep links; `SelectSection`; `SelectTab` route | NR-KC-02 |
| NR-KC-04 | KickCD | Retire Icons, Cast bar and Text Label; slash wording; tests; docs; smoke #36 | NR-KC-03 |
| NR-REC-01 | Ka0sAddonsCommonTasks | Execution record: `99_REPORT.md`, checkpoint rows, follow-ups | every M1 item, NR-MM-04, NR-KC-04 |

M1 is the ten NR-XX-01 items, independent and parallel. M2 is two chains, MultiMeters and KickCD, in
parallel, each in order. M3 is NR-REC-01. Before any of them, the bundle itself is committed (below).

---

## Before M1 — commit the bundle

The plan is frozen once execution starts (`../../CLAUDE.md`, "Bundle conventions"), so it goes into
git first, on `main` in Ka0sAddonsCommonTasks, as the SETTINGS_REDESIGN bundle did (`456a7c8`). This
commit carries no item id, so `resume-state.sh` does not count it. It runs once, before any NR-XX-01
Step 1. A relaunch skips it when `git log --format=%s main -- docs/2026-09-26-NAVRAIL_ADOPTION/03_EXECUTION_PLAN.md`
already prints a subject.

```sh
cd $GIT/Ka0sAddonsCommonTasks
git branch --show-current                                   # expect main
git status --porcelain -- . ':!docs/2026-09-26-NAVRAIL_ADOPTION'   # expect empty: nothing else rides along
git add docs/2026-09-26-NAVRAIL_ADOPTION
git status --porcelain                                      # expect only A lines under the bundle
git commit -m "NavRail adoption: the plan bundle for the v1.61.0 re-vendor, MultiMeters#55 and KickCD#33" \
  -m "Seventeen items in three milestones: LibKa0s v1.61.0 into the ten addons that carry v1.60.0, the MultiMeters Windows page and the KickCD Grid page. The owner waived review of the spec and plan. Not pushed." \
  -m "$TRAILERS"
```

From here on the plan files are not edited. The M1 and M2 rows go into the now-tracked
`checkpoints.tsv`, and NR-REC-01 commits them with `99_REPORT.md`.

---

## M1 — the v1.61.0 re-vendor

Every M1 task works in one addon on `feat/2026-09-26-navrail-adoption`, and ends on that addon's gate
and one commit. The expected test totals below are the dry run's (`Ka0sAddonsCommonTasks` scratch
copies, 2026-09-26): the totals do not move, because no case is added.

The historical `v1.60.0` mentions stay as they are: "introduced in v1.60.0", DebugLog 14.1 "from
v1.60.0", buffer 3000 "at v1.60.0", and the docs/api version-docs citations. Each task names the lines
that state the vendored version **now**, and changes only those.

### Task NR-AT-01: AbsorbTracker takes LibKa0s v1.61.0

**Files:**
- Modify (copied from the tag): `libs/LibKa0s/LibKa0s.xml`, `Options.lua`, `OptionsTabs.lua`. Create
  (copied): `libs/LibKa0s/OptionsNav.lua`.
- Modify: `CLAUDE.md:43` (provenance), `docs/testing.md:170` (the vendored version now),
  `settings/OptionsSetup.lua:314` (the stub).
- Create: `docs/revendor/<date>-v1.61.0/01_DELTA.md`, `02_CANDIDATES.md`, `03_DECISIONS.md`,
  `05_SUMMARY.md`.

**Interfaces:** consumes the tag `v1.61.0`. Produces `NS.Helpers.NavRail` on the live instance (the
library's) and `Helpers.NavRail`, a no-op, on the library-absent stub.

- [ ] **Step 1: Preconditions and branch.**

```sh
cd $GIT/AbsorbTracker
git status --porcelain                              # expect empty
git branch --show-current                           # expect master
git rev-parse --short HEAD                          # 7540ab3 at planning time
git -C $GIT/LibKa0s rev-parse --short 'v1.61.0^{}'  # expect c6183bd
git switch -c $BR
```

- [ ] **Step 2: Copy the payload from the tag.**

```sh
lk_copy
```

Expected: four delta lines, `Files <tag>/LibKa0s/LibKa0s.xml and libs/LibKa0s/LibKa0s.xml differ`,
the same for `Options.lua` and `OptionsTabs.lua`, and `Only in <tag>/LibKa0s: OptionsNav.lua`. Then
`kit delta lines: 0` and `libs/LibKa0s == v1.61.0 byte for byte`. Any other line: stop and report.

- [ ] **Step 3: Roll the provenance line and the version-now line.**

```sh
perl -pi -e 's#(Bundles \[LibKa0s\]\(https://github\.com/tusharsaxena/LibKa0s\) )v1\.60\.0#${1}v1.61.0#' CLAUDE.md
perl -pi -e 's/\*\*v1\.60\.0\*\*, the vendored payloads are that tag/**v1.61.0**, the vendored payloads are that tag/' docs/testing.md
crlf CLAUDE.md docs/testing.md
grep -c 'LibKa0s) v1.61.0' CLAUDE.md                                   # expect 1
grep -c '\*\*v1.61.0\*\*, the vendored payloads are that tag' docs/testing.md   # expect 1
```

- [ ] **Step 4: Run and see the parity case fail.**

```sh
/home/tushar/.claude/wow-addon/bin/ka0s-bounded lua tests/run.lua > /tmp/AbsorbTracker-run.txt 2>&1
grep -E '^  FAIL' /tmp/AbsorbTracker-run.txt; grep -n 'NavRail' /tmp/AbsorbTracker-run.txt
```

Expected: exactly one `FAIL`, the Options surface-parity case in `tests/test_surface_parity.lua`,
whose message names `NavRail is missing (live: function)`. `test_vendor_sync` passes.

- [ ] **Step 5: Stub it.** The stub assigns members one by one, and `Helpers.SelectTab` is the last
  library no-op before the `__` pair:

```sh
perl -0pi -e 's/(    Helpers\.SelectTab = function\(\) end\r?\n)/$1    -- NavRail, new at LibKa0s v1.61.0 (OptionsNav minor 1): drawn only by a page render, and no\r\n    -- page here draws a rail, so the same inert no-op answers.\r\n    Helpers.NavRail = function() end\r\n/' settings/OptionsSetup.lua
crlf settings/OptionsSetup.lua
grep -c 'Helpers.NavRail = function() end' settings/OptionsSetup.lua   # expect 1
```

- [ ] **Step 6: Gate.** Run the addon gate. Expected: `810` passed, 0 failed, 0 skipped. luacheck
  0/0. No `EOL FAIL` line from any `crlf` call.

- [ ] **Step 7: The revendor bundle.**

```sh
rv_bundle "Not adopted here. No AbsorbTracker page edits one instance out of many through sub-pages retargeted by one picker, which is the only shape options-ui-§13 sanctions the rail for." \
  "$(grep -E 'passed' /tmp/AbsorbTracker-run.txt | tail -1)" \
  "$(/home/tushar/.claude/wow-addon/bin/ka0s-bounded luacheck . | tail -1)"
ls docs/revendor/$(date +%F)-v1.61.0     # expect 01_DELTA.md 02_CANDIDATES.md 03_DECISIONS.md 05_SUMMARY.md
```

- [ ] **Step 8: Commit.**

```sh
git add libs/LibKa0s CLAUDE.md docs/testing.md settings/OptionsSetup.lua docs/revendor/$(date +%F)-v1.61.0
git status --porcelain                  # expect empty
git commit -m "NR-AT-01: Re-vendor LibKa0s v1.61.0 and stub NavRail" \
  -m "LibKa0s payload from the v1.61.0 tag: Options 24 -> 25, OptionsTabs 4 -> 5, the new OptionsNav minor 1 (Options key 25.31.5.7.4.1). tests/_kit is unchanged at kit revision 27, so it is not copied. CLAUDE.md provenance and docs/testing.md's version-now line roll with it. The library-absent stub gains a NavRail no-op for the Options surface-parity case; no page here draws a rail." \
  -m "$TRAILERS"
```

### Task NR-BL-01: BankLedger takes LibKa0s v1.61.0

**Files:**
- Modify (copied from the tag): `libs/LibKa0s/LibKa0s.xml`, `Options.lua`, `OptionsTabs.lua`. Create
  (copied): `libs/LibKa0s/OptionsNav.lua`.
- Modify: `CLAUDE.md:46`, `docs/testing.md:97-98`, `settings/OptionsSetup.lua:224` (the stub's table
  literal), `docs/test-cases.md` (regenerated, per BankLedger `CLAUDE.md:57`).
- Create: `docs/revendor/<date>-v1.61.0/` (four files).

**Interfaces:** consumes the tag. Produces the live `NavRail` and a stub no-op `NavRail`.

- [ ] **Step 1: Preconditions and branch.**

```sh
cd $GIT/BankLedger
git status --porcelain                              # expect empty
git branch --show-current                           # expect master
git rev-parse --short HEAD                          # 90b0c60 at planning time
git -C $GIT/LibKa0s rev-parse --short 'v1.61.0^{}'  # expect c6183bd
git switch -c $BR
```

- [ ] **Step 2: Copy the payload.** `lk_copy`. Expected: the four delta lines (`LibKa0s.xml`,
  `Options.lua`, `OptionsTabs.lua` differ; `Only in <tag>/LibKa0s: OptionsNav.lua`),
  `kit delta lines: 0`, and `libs/LibKa0s == v1.61.0 byte for byte`.

- [ ] **Step 3: Provenance and version-now lines.**

```sh
perl -pi -e 's#(Bundles \[LibKa0s\]\(https://github\.com/tusharsaxena/LibKa0s\) )v1\.60\.0#${1}v1.61.0#' CLAUDE.md
perl -pi -e 's/sits on \*\*v1\.60\.0\*\*,/sits on **v1.61.0**,/ if $. == 97; s/names \*\*v1\.60\.0\*\*, and all four/names **v1.61.0**, and all four/ if $. == 98' docs/testing.md
crlf CLAUDE.md docs/testing.md
grep -c 'LibKa0s) v1.61.0' CLAUDE.md          # expect 1
sed -n 97,98p docs/testing.md | grep -c 'v1.61.0'   # expect 2
```

- [ ] **Step 4: Run and see the parity case fail.**

```sh
/home/tushar/.claude/wow-addon/bin/ka0s-bounded lua tests/run.lua > /tmp/BankLedger-run.txt 2>&1
grep -E '^  FAIL' /tmp/BankLedger-run.txt; grep -n 'NavRail' /tmp/BankLedger-run.txt
```

Expected: exactly one `FAIL`, the Options surface-parity case, naming `NavRail`.

- [ ] **Step 5: Stub it** in the table literal, after `SelectTab = function() end,`:

```sh
perl -0pi -e 's/(    SelectTab = function\(\) end,\r?\n)/$1    -- NavRail, new at LibKa0s v1.61.0 (OptionsNav minor 1): drawn only by a page render, and no\r\n    -- page here draws a rail, so a no-op keeps the stub matching the live surface.\r\n    NavRail = function() end,\r\n/' settings/OptionsSetup.lua
crlf settings/OptionsSetup.lua
grep -c '    NavRail = function() end,' settings/OptionsSetup.lua   # expect 1
```

- [ ] **Step 6: Regenerate the inventory and gate.**

```sh
/home/tushar/.claude/wow-addon/bin/ka0s-bounded lua tests/run.lua --list > docs/test-cases.md
crlf docs/test-cases.md
git diff --stat docs/test-cases.md        # expect no change (no case was added)
```

  Then run the addon gate. Expected: `1104` passed, 0 failed. luacheck 0/0.

- [ ] **Step 7: The revendor bundle.**

```sh
rv_bundle "Not adopted here. No BankLedger page edits one instance out of many through sub-pages retargeted by one picker, which is the only shape options-ui-§13 sanctions the rail for." \
  "$(grep -E 'passed' /tmp/BankLedger-run.txt | tail -1)" \
  "$(/home/tushar/.claude/wow-addon/bin/ka0s-bounded luacheck . | tail -1)"
```

- [ ] **Step 8: Commit.**

```sh
git add libs/LibKa0s CLAUDE.md docs/testing.md settings/OptionsSetup.lua docs/test-cases.md docs/revendor/$(date +%F)-v1.61.0
git status --porcelain                  # expect empty
git commit -m "NR-BL-01: Re-vendor LibKa0s v1.61.0 and stub NavRail" \
  -m "LibKa0s payload from the v1.61.0 tag: Options 24 -> 25, OptionsTabs 4 -> 5, the new OptionsNav minor 1 (Options key 25.31.5.7.4.1). tests/_kit is unchanged at kit revision 27. CLAUDE.md provenance and docs/testing.md's version-now lines roll with it; docs/test-cases.md regenerated per CLAUDE.md (no case moved). The stub's table literal gains a NavRail no-op for the Options surface-parity case." \
  -m "$TRAILERS"
```

(`git add docs/test-cases.md` is a no-op when Step 6 showed no change.)

### Task NR-CM-01: ConsumableMaster takes LibKa0s v1.61.0

**Files:**
- Modify (copied from the tag): `libs/LibKa0s/LibKa0s.xml`, `Options.lua`, `OptionsTabs.lua`. Create
  (copied): `libs/LibKa0s/OptionsNav.lua`.
- Modify: `CLAUDE.md:61`, `tests/test_libka0s.lua:55-70` (the Options entry of the `MAJORS`
  inventory).
- Create: `docs/revendor/<date>-v1.61.0/` (four files).
- Not modified: `settings/OptionsSetup.lua`. ConsumableMaster's stub projects a named `OPTIONS_SEAM`
  list (`tests/test_surface_parity.lua:264`) that does not include `NavRail`, so parity does not
  go red. This departs from the letter of the owner's D1 ("each host's stub gains the no-op");
  `02_SPEC.md` R18 records why. `docs/testing.md:146` ("kit revision 27, vendored from LibKa0s v1.60.0") stays true,
  because the kit was not re-copied.

**Interfaces:** consumes the tag. The Options inventory now names six files, and pairs `OptionsNav`
with `lib.__navMinor` / `lib.__navShellMinor`.

- [ ] **Step 1: Preconditions and branch.**

```sh
cd $GIT/ConsumableMaster
git status --porcelain                              # expect empty
git branch --show-current                           # expect master
git rev-parse --short HEAD                          # e2103f9 at planning time
git -C $GIT/LibKa0s rev-parse --short 'v1.61.0^{}'  # expect c6183bd
git switch -c $BR
```

- [ ] **Step 2: Copy the payload.** `lk_copy`. Expected: the four delta lines, `kit delta lines: 0`,
  `libs/LibKa0s == v1.61.0 byte for byte`.

- [ ] **Step 3: Provenance.**

```sh
perl -pi -e 's#(Bundles \[LibKa0s\]\(https://github\.com/tusharsaxena/LibKa0s\) )v1\.60\.0#${1}v1.61.0#' CLAUDE.md
crlf CLAUDE.md
grep -c 'LibKa0s) v1.61.0' CLAUDE.md          # expect 1
```

- [ ] **Step 4: Run and see the inventory case fail.** ConsumableMaster's gate runs `lua5.1`
  (`CLAUDE.md:100`):

```sh
/home/tushar/.claude/wow-addon/bin/ka0s-bounded lua5.1 tests/run.lua > /tmp/ConsumableMaster-run.txt 2>&1
grep -E '^  FAIL' /tmp/ConsumableMaster-run.txt; grep -n 'OptionsNav' /tmp/ConsumableMaster-run.txt
```

Expected: exactly one `FAIL` in `tests/test_libka0s.lua`, the MODULES stray check, reporting that
`LibKa0s-Options-1.0 reports OptionsNav`.

- [ ] **Step 5: Name the sixth file in the inventory.**

```sh
perl -0pi -e 's/(        -- below reads it as a file registering under a major it does not own\.\r?\n)/$1        -- OptionsNav joined at LibKa0s v1.61.0 the same way: the nav rail (O.NavRail), its own\r\n        -- MODULES row, and a paired minor and shell.\r\n/' tests/test_libka0s.lua
perl -pi -e 's/files = \{ "Options", "OptionsWidgets", "OptionsTabs", "OptionsScroll", "OptionsCompose" \},/files = { "Options", "OptionsWidgets", "OptionsTabs", "OptionsScroll", "OptionsCompose", "OptionsNav" },/' tests/test_libka0s.lua
perl -0pi -e 's/(            \{ file = "OptionsCompose", minor = "__composeMinor", shell = "__composeShellMinor" \},\r?\n)/$1            { file = "OptionsNav",     minor = "__navMinor",     shell = "__navShellMinor" },\r\n/' tests/test_libka0s.lua
crlf tests/test_libka0s.lua
grep -n 'OptionsNav' tests/test_libka0s.lua    # expect exactly the three lines below
```

The `grep -n` must show three lines: the new comment, the `files` list, and the paired row
`{ file = "OptionsNav", minor = "__navMinor", shell = "__navShellMinor" }`.

- [ ] **Step 6: Gate.**

```sh
/home/tushar/.claude/wow-addon/bin/ka0s-bounded lua5.1 tests/run.lua > /tmp/ConsumableMaster-run.txt 2>&1
tail -3 /tmp/ConsumableMaster-run.txt; grep -c '^  FAIL' /tmp/ConsumableMaster-run.txt     # expect 0
/home/tushar/.claude/wow-addon/bin/ka0s-bounded luacheck . | tail -2                        # expect 0/0
/home/tushar/.claude/wow-addon/bin/ka0s-bounded lizard -l lua -x "./libs/*" -x "./tests/_kit/*" . | tail -3   # CLAUDE.md:107; no new warning
```

Expected: `1112` passed, 0 failed. The lizard warning count equals `master`'s, since no function
changed.

- [ ] **Step 7: The revendor bundle.**

```sh
rv_bundle "Not adopted here. No ConsumableMaster page edits one instance out of many through sub-pages retargeted by one picker. The stub projects the named OPTIONS_SEAM list, which does not include NavRail, so the fix is tests/test_libka0s.lua's Options inventory (files + the paired __navMinor/__navShellMinor)." \
  "$(grep -E 'passed' /tmp/ConsumableMaster-run.txt | tail -1)" \
  "$(/home/tushar/.claude/wow-addon/bin/ka0s-bounded luacheck . | tail -1)"
```

- [ ] **Step 8: Commit.**

```sh
git add libs/LibKa0s CLAUDE.md tests/test_libka0s.lua docs/revendor/$(date +%F)-v1.61.0
git status --porcelain                  # expect empty
git commit -m "NR-CM-01: Re-vendor LibKa0s v1.61.0; the Options inventory names OptionsNav" \
  -m "LibKa0s payload from the v1.61.0 tag: Options 24 -> 25, OptionsTabs 4 -> 5, the new OptionsNav minor 1 (Options key 25.31.5.7.4.1). tests/_kit is unchanged at kit revision 27. CLAUDE.md provenance rolls with it. tests/test_libka0s.lua's Options inventory gains the sixth file and its paired minor and shell, so the MODULES stray check reads OptionsNav as the major's own. The stub needs no member: its OPTIONS_SEAM list does not include NavRail." \
  -m "$TRAILERS"
```

### Task NR-KC-01: KickCD takes LibKa0s v1.61.0

**Files:**
- Modify (copied from the tag): `libs/LibKa0s/LibKa0s.xml`, `Options.lua`, `OptionsTabs.lua`. Create
  (copied): `libs/LibKa0s/OptionsNav.lua`.
- Modify: `CLAUDE.md:42`, `docs/testing.md:187`, `settings/OptionsSetup.lua:403-405` (the stub's
  no-op name list), `tests/test_options_panel.lua:971-973` (the Options-file count).
- Create: `docs/revendor/<date>-v1.61.0/` (four files).

**Interfaces:** consumes the tag. Produces the live `NavRail` and the stub no-op. NR-KC-02 adopts the
rail.

- [ ] **Step 1: Preconditions and branch.**

```sh
cd $GIT/KickCD
git status --porcelain                              # expect empty
git branch --show-current                           # expect master
git rev-parse --short HEAD                          # 604e922 at planning time
git -C $GIT/LibKa0s rev-parse --short 'v1.61.0^{}'  # expect c6183bd
git switch -c $BR
```

- [ ] **Step 2: Copy the payload.** `lk_copy`. Expected: the four delta lines, `kit delta lines: 0`,
  `libs/LibKa0s == v1.61.0 byte for byte`.

- [ ] **Step 3: Provenance and version-now line.**

```sh
perl -pi -e 's#(Bundles \[LibKa0s\]\(https://github\.com/tusharsaxena/LibKa0s\) )v1\.60\.0#${1}v1.61.0#' CLAUDE.md
perl -pi -e 's/sits on \*\*v1\.60\.0\*\*,/sits on **v1.61.0**,/ if $. == 187' docs/testing.md
crlf CLAUDE.md docs/testing.md
grep -c 'LibKa0s) v1.61.0' CLAUDE.md                   # expect 1
sed -n 187p docs/testing.md | grep -c 'v1.61.0'        # expect 1
```

- [ ] **Step 4: Run and see two cases fail.**

```sh
/home/tushar/.claude/wow-addon/bin/ka0s-bounded lua tests/run.lua > /tmp/KickCD-run.txt 2>&1
grep -E '^  FAIL' /tmp/KickCD-run.txt; grep -n 'NavRail\|five files' /tmp/KickCD-run.txt
```

Expected: exactly two `FAIL`s. One is the Options surface-parity case in
`tests/test_surface_parity.lua`, naming `NavRail`. The other is the case in
`tests/test_options_panel.lua` whose `assertEqual(scanned, 5,` now sees 6.

- [ ] **Step 5: Stub it, and count six files.**

```sh
perl -0pi -e 's/(        "SelectTab",\r?\n)/$1        -- NavRail, new at LibKa0s v1.61.0 (OptionsNav minor 1): drawn only by the Grid page\x27s\r\n        -- render (settings\/Grid.lua), which never runs here, so the same inert no-op applies.\r\n        "NavRail",\r\n/' settings/OptionsSetup.lua
perl -0pi -e 's/assertEqual\(scanned, 5,\r?\n        "the major is five files at LibKa0s v1\.39\.0/assertEqual(scanned, 6,\r\n        "the major is six files at LibKa0s v1.61.0/' tests/test_options_panel.lua
crlf settings/OptionsSetup.lua tests/test_options_panel.lua
grep -c '"NavRail",' settings/OptionsSetup.lua                 # expect 1
grep -c 'assertEqual(scanned, 6,' tests/test_options_panel.lua # expect 1
```

  `settings/Grid.lua` does not exist until NR-KC-02. The comment names it because that task
  creates it, and a reviewer of NR-KC-02 checks that it holds.

- [ ] **Step 6: Gate.** Run the addon gate. Expected: `1189` passed, 0 failed. luacheck 0/0.

- [ ] **Step 7: The revendor bundle.**

```sh
rv_bundle "Adopted by NR-KC-02 (KickCD#33): the Grid page draws the rail, with Icons, Cast bar and Text Label as its entries under the Unit band." \
  "$(grep -E 'passed' /tmp/KickCD-run.txt | tail -1)" \
  "$(/home/tushar/.claude/wow-addon/bin/ka0s-bounded luacheck . | tail -1)"
```

- [ ] **Step 8: Commit.**

```sh
git add libs/LibKa0s CLAUDE.md docs/testing.md settings/OptionsSetup.lua tests/test_options_panel.lua docs/revendor/$(date +%F)-v1.61.0
git status --porcelain                  # expect empty
git commit -m "NR-KC-01: Re-vendor LibKa0s v1.61.0 and stub NavRail" \
  -m "LibKa0s payload from the v1.61.0 tag: Options 24 -> 25, OptionsTabs 4 -> 5, the new OptionsNav minor 1 (Options key 25.31.5.7.4.1). tests/_kit is unchanged at kit revision 27. CLAUDE.md provenance and docs/testing.md's version-now line roll with it. The stub's no-op list gains NavRail for the Options surface-parity case, and the descriptor-L tripwire counts the major's six files. The rail is adopted by NR-KC-02 (#33)." \
  -m "$TRAILERS"
```

### Task NR-LH-01: LootHistory takes LibKa0s v1.61.0

**Files:**
- Modify (copied from the tag): `libs/LibKa0s/LibKa0s.xml`, `Options.lua`, `OptionsTabs.lua`. Create
  (copied): `libs/LibKa0s/OptionsNav.lua`.
- Modify: `CLAUDE.md:56`, `settings/OptionsSetup.lua:115` (the stub's table literal),
  `tests/test_libka0s.lua:60` (the explicit `LIB_FILES` list).
- Create: `docs/revendor/<date>-v1.61.0/` (four files).

**Interfaces:** consumes the tag. Produces the live `NavRail` and the stub no-op.

- [ ] **Step 1: Preconditions and branch.**

```sh
cd $GIT/LootHistory
git status --porcelain                              # expect empty
git branch --show-current                           # expect master
git rev-parse --short HEAD                          # 4f03c04 at planning time
git -C $GIT/LibKa0s rev-parse --short 'v1.61.0^{}'  # expect c6183bd
git switch -c $BR
```

- [ ] **Step 2: Copy the payload.** `lk_copy`. Expected: the four delta lines, `kit delta lines: 0`,
  `libs/LibKa0s == v1.61.0 byte for byte`.

- [ ] **Step 3: Provenance.** LootHistory's line continues after `(MIT)`, so the substitution
  anchors on the link and the tag only:

```sh
perl -pi -e 's#(Bundles \[LibKa0s\]\(https://github\.com/tusharsaxena/LibKa0s\) )v1\.60\.0#${1}v1.61.0#' CLAUDE.md
crlf CLAUDE.md
grep -c 'LibKa0s) v1.61.0' CLAUDE.md          # expect 1
```

- [ ] **Step 4: Run and see two cases fail.**

```sh
/home/tushar/.claude/wow-addon/bin/ka0s-bounded lua tests/run.lua > /tmp/LootHistory-run.txt 2>&1
grep -E '^  FAIL' /tmp/LootHistory-run.txt; grep -n 'NavRail\|OptionsNav\|22\|23' /tmp/LootHistory-run.txt | head
```

Expected: two `FAIL`s. One is the Options surface-parity case naming `NavRail`. The other is
`tests/test_libka0s.lua`'s explicit-list case (22 files listed, 23 in the XML).

- [ ] **Step 5: Stub it, and list the file.**

```sh
perl -0pi -e 's/(    SelectTab = noop,\r?\n)/$1    -- NavRail, new at LibKa0s v1.61.0 (OptionsNav minor 1): drawn only by a page render, and no\r\n    -- page here draws a rail, so the same inert no-op applies.\r\n    NavRail = noop,\r\n/' settings/OptionsSetup.lua
perl -0pi -e 's/(  "libs\/LibKa0s\/OptionsScroll\.lua",\r?\n)/$1  "libs\/LibKa0s\/OptionsNav.lua",\r\n/' tests/test_libka0s.lua
crlf settings/OptionsSetup.lua tests/test_libka0s.lua
grep -c '    NavRail = noop,' settings/OptionsSetup.lua                   # expect 1
grep -c '"libs/LibKa0s/OptionsNav.lua",' tests/test_libka0s.lua          # expect 1
```

- [ ] **Step 6: Gate.** Run the addon gate. Expected: `961` passed, 0 failed. luacheck 0/0.

- [ ] **Step 7: The revendor bundle.**

```sh
rv_bundle "Not adopted here. No LootHistory page edits one instance out of many through sub-pages retargeted by one picker, which is the only shape options-ui-§13 sanctions the rail for." \
  "$(grep -E 'passed' /tmp/LootHistory-run.txt | tail -1)" \
  "$(/home/tushar/.claude/wow-addon/bin/ka0s-bounded luacheck . | tail -1)"
```

- [ ] **Step 8: Commit.**

```sh
git add libs/LibKa0s CLAUDE.md settings/OptionsSetup.lua tests/test_libka0s.lua docs/revendor/$(date +%F)-v1.61.0
git status --porcelain                  # expect empty
git commit -m "NR-LH-01: Re-vendor LibKa0s v1.61.0 and stub NavRail" \
  -m "LibKa0s payload from the v1.61.0 tag: Options 24 -> 25, OptionsTabs 4 -> 5, the new OptionsNav minor 1 (Options key 25.31.5.7.4.1). tests/_kit is unchanged at kit revision 27. CLAUDE.md provenance rolls with it. The stub's table literal gains a NavRail no-op for the Options surface-parity case, and tests/test_libka0s.lua's explicit LIB_FILES list gains OptionsNav.lua in XML order: the v1.61.0 CHANGELOG's 'the XML-derived list needs no change' does not hold for a typed list." \
  -m "$TRAILERS"
```

### Task NR-MM-01: MultiMeters takes LibKa0s v1.61.0

**Files:**
- Modify (copied from the tag): `libs/LibKa0s/LibKa0s.xml`, `Options.lua`, `OptionsTabs.lua`. Create
  (copied): `libs/LibKa0s/OptionsNav.lua`.
- Modify: `CLAUDE.md:54`, `settings/OptionsSetup.lua:408-410` (the stub's no-op name list).
- Create: `docs/revendor/<date>-v1.61.0/` (four files).
- Not modified: `tests/run.lua`'s `EXPECTED` list (:63-81) is a must-contain subset, and
  `docs/ARCHITECTURE.md:399`'s `v1.60.0` is historical.

**Interfaces:** consumes the tag. Produces the live `NavRail` (on the decorated `NS.Helpers`, which
is MultiMeters' parity source, `tests/run.lua:386`) and the stub no-op. NR-MM-02 adopts the rail.

- [ ] **Step 1: Preconditions and branch.**

```sh
cd $GIT/MultiMeters
git status --porcelain                              # expect empty
git branch --show-current                           # expect master
git rev-parse --short HEAD                          # c374876 at planning time
git -C $GIT/LibKa0s rev-parse --short 'v1.61.0^{}'  # expect c6183bd
git switch -c $BR
```

- [ ] **Step 2: Copy the payload.** `lk_copy`. Expected: the four delta lines, `kit delta lines: 0`,
  `libs/LibKa0s == v1.61.0 byte for byte`.

- [ ] **Step 3: Provenance.**

```sh
perl -pi -e 's#(Bundles \[LibKa0s\]\(https://github\.com/tusharsaxena/LibKa0s\) )v1\.60\.0#${1}v1.61.0#' CLAUDE.md
crlf CLAUDE.md
grep -c 'LibKa0s) v1.61.0' CLAUDE.md          # expect 1
```

- [ ] **Step 4: Run and see the parity case fail.**

```sh
/home/tushar/.claude/wow-addon/bin/ka0s-bounded lua tests/run.lua > /tmp/MultiMeters-run.txt 2>&1
grep -E '^  FAIL' /tmp/MultiMeters-run.txt; grep -n 'NavRail' /tmp/MultiMeters-run.txt
```

Expected: exactly one `FAIL`, `parity: the Options stub carries every public member of the live
Helpers surface`, naming `NavRail`.

- [ ] **Step 5: Stub it.**

```sh
perl -0pi -e 's/(        "SelectTab",\r?\n)/$1        -- NavRail, new at LibKa0s v1.61.0 (OptionsNav minor 1): drawn only by the Windows page\x27s\r\n        -- render, which never runs with no library, so the same inert no-op applies.\r\n        "NavRail",\r\n/' settings/OptionsSetup.lua
crlf settings/OptionsSetup.lua
grep -c '"NavRail",' settings/OptionsSetup.lua    # expect 1
```

- [ ] **Step 6: Gate.** Run the addon gate. Expected: `2078` passed, 0 failed. luacheck 0/0.

- [ ] **Step 7: The revendor bundle.**

```sh
rv_bundle "Adopted by NR-MM-02 (MultiMeters#55): the Windows page draws the rail, with General, Frame, Header, Bars, Tooltip, Visibility and Columns as its entries under the Active window band." \
  "$(grep -E 'passed' /tmp/MultiMeters-run.txt | tail -1)" \
  "$(/home/tushar/.claude/wow-addon/bin/ka0s-bounded luacheck . | tail -1)"
```

- [ ] **Step 8: Commit.**

```sh
git add libs/LibKa0s CLAUDE.md settings/OptionsSetup.lua docs/revendor/$(date +%F)-v1.61.0
git status --porcelain                  # expect empty
git commit -m "NR-MM-01: Re-vendor LibKa0s v1.61.0 and stub NavRail" \
  -m "LibKa0s payload from the v1.61.0 tag: Options 24 -> 25, OptionsTabs 4 -> 5, the new OptionsNav minor 1 (Options key 25.31.5.7.4.1). tests/_kit is unchanged at kit revision 27. CLAUDE.md provenance rolls with it. The stub's no-op list gains NavRail for the Options surface-parity case. The rail is adopted by NR-MM-02 (#55)." \
  -m "$TRAILERS"
```

### Task NR-PM-01: PanelMaster takes LibKa0s v1.61.0

**Files:**
- Modify (copied from the tag): `libs/LibKa0s/LibKa0s.xml`, `Options.lua`, `OptionsTabs.lua`. Create
  (copied): `libs/LibKa0s/OptionsNav.lua`.
- Modify: `CLAUDE.md:45`, `settings/OptionsSetup.lua:97` (the stub's table literal).
- Create: `docs/revendor/<date>-v1.61.0/` (four files).

**Interfaces:** consumes the tag. Produces the live `NavRail` and the stub no-op. PanelMaster#55 (a
rail for PanelMaster) is closed `state:will-not-do`.

- [ ] **Step 1: Preconditions and branch.**

```sh
cd $GIT/PanelMaster
git status --porcelain                              # expect empty
git branch --show-current                           # expect master
git rev-parse --short HEAD                          # 5fa3da8 at planning time
git -C $GIT/LibKa0s rev-parse --short 'v1.61.0^{}'  # expect c6183bd
git -C $GIT/LibKa0s status --porcelain              # expect empty: the vendor gate diffs its tree
git -C $GIT/LibKa0s diff --quiet 'v1.61.0' HEAD -- LibKa0s testkit && echo "LibKa0s tree == tag"   # expect the echo
git switch -c $BR
```

- [ ] **Step 2: Copy the payload.** `lk_copy`. Expected: the four delta lines, `kit delta lines: 0`,
  `libs/LibKa0s == v1.61.0 byte for byte`.

- [ ] **Step 3: Provenance.**

```sh
perl -pi -e 's#(Bundles \[LibKa0s\]\(https://github\.com/tusharsaxena/LibKa0s\) )v1\.60\.0#${1}v1.61.0#' CLAUDE.md
crlf CLAUDE.md
grep -c 'LibKa0s) v1.61.0' CLAUDE.md          # expect 1
```

- [ ] **Step 4: Run and see the parity case fail.**

```sh
/home/tushar/.claude/wow-addon/bin/ka0s-bounded lua tests/run.lua > /tmp/PanelMaster-run.txt 2>&1
grep -E '^  FAIL' /tmp/PanelMaster-run.txt; grep -n 'NavRail' /tmp/PanelMaster-run.txt
```

Expected: exactly one `FAIL`, the Options surface-parity case, naming `NavRail`.

- [ ] **Step 5: Stub it.**

```sh
perl -0pi -e 's/(    SelectTab = noop,\r?\n)/$1    -- NavRail, new at LibKa0s v1.61.0 (OptionsNav minor 1): drawn only by a page render, and no\r\n    -- page here draws a rail (PanelMaster#55, will-not-do), so the same inert answer applies.\r\n    NavRail = noop,\r\n/' settings/OptionsSetup.lua
crlf settings/OptionsSetup.lua
grep -c '    NavRail = noop,' settings/OptionsSetup.lua   # expect 1
```

- [ ] **Step 6: Gate, plus PanelMaster's vendor gate** (`CLAUDE.md:62`). Run the addon gate.
  Expected: `962` passed, 0 failed. luacheck 0/0. Then:

```sh
diff -r --strip-trailing-cr $GIT/LibKa0s/LibKa0s libs/LibKa0s && echo ok-libs-cr
diff -r $GIT/LibKa0s/LibKa0s libs/LibKa0s && echo ok-libs
diff -r --strip-trailing-cr $GIT/LibKa0s/testkit tests/_kit && echo ok-kit-cr
diff -r $GIT/LibKa0s/testkit tests/_kit && echo ok-kit
```

Expected: all four `ok-*` lines.

- [ ] **Step 7: The revendor bundle.**

```sh
rv_bundle "Not adopted here (PanelMaster#55 closed will-not-do). No PanelMaster page edits one instance out of many through sub-pages retargeted by one picker." \
  "$(grep -E 'passed' /tmp/PanelMaster-run.txt | tail -1)" \
  "$(/home/tushar/.claude/wow-addon/bin/ka0s-bounded luacheck . | tail -1)"
```

- [ ] **Step 8: Commit.**

```sh
git add libs/LibKa0s CLAUDE.md settings/OptionsSetup.lua docs/revendor/$(date +%F)-v1.61.0
git status --porcelain                  # expect empty
git commit -m "NR-PM-01: Re-vendor LibKa0s v1.61.0 and stub NavRail" \
  -m "LibKa0s payload from the v1.61.0 tag: Options 24 -> 25, OptionsTabs 4 -> 5, the new OptionsNav minor 1 (Options key 25.31.5.7.4.1). tests/_kit is unchanged at kit revision 27. CLAUDE.md provenance rolls with it. The stub's table literal gains a NavRail no-op for the Options surface-parity case. The vendor diff gate is clean against ../LibKa0s." \
  -m "$TRAILERS"
```

### Task NR-PF-01: PartyFrameEnhanced takes LibKa0s v1.61.0

**Files:**
- Modify (copied from the tag): `libs/LibKa0s/LibKa0s.xml`, `Options.lua`, `OptionsTabs.lua`. Create
  (copied): `libs/LibKa0s/OptionsNav.lua`.
- Modify: `CLAUDE.md:39`, `docs/ARCHITECTURE.md:23` and `:42` (the vendored version now; `:49` and
  `:51` are historical and stay), `settings/OptionsSetup.lua:141` (the stub's no-op name list).
- Create: `docs/revendor/<date>-v1.61.0/` (four files).

**Interfaces:** consumes the tag. Produces the live `NavRail` and the stub no-op.

- [ ] **Step 1: Preconditions and branch.**

```sh
cd $GIT/PartyFrameEnhanced
git status --porcelain                              # expect empty
git branch --show-current                           # expect master
git rev-parse --short HEAD                          # 151d467 at planning time
git -C $GIT/LibKa0s rev-parse --short 'v1.61.0^{}'  # expect c6183bd
git switch -c $BR
```

- [ ] **Step 2: Copy the payload.** `lk_copy`. Expected: the four delta lines, `kit delta lines: 0`,
  `libs/LibKa0s == v1.61.0 byte for byte`.

- [ ] **Step 3: Provenance and version-now lines.**

```sh
perl -pi -e 's#(Bundles \[LibKa0s\]\(https://github\.com/tusharsaxena/LibKa0s\) )v1\.60\.0#${1}v1.61.0#' CLAUDE.md
perl -pi -e 's/\*\*LibKa0s v1\.60\.0\*\* vendored whole/**LibKa0s v1.61.0** vendored whole/ if $. == 23; s/^v1\.60\.0\. What the addon/v1.61.0. What the addon/ if $. == 42' docs/ARCHITECTURE.md
crlf CLAUDE.md docs/ARCHITECTURE.md
grep -c 'LibKa0s) v1.61.0' CLAUDE.md                                   # expect 1
sed -n '23p;42p' docs/ARCHITECTURE.md | grep -c 'v1.61.0'              # expect 2
```

- [ ] **Step 4: Run and see the parity case fail.**

```sh
/home/tushar/.claude/wow-addon/bin/ka0s-bounded lua tests/run.lua > /tmp/PartyFrameEnhanced-run.txt 2>&1
grep -E '^  FAIL' /tmp/PartyFrameEnhanced-run.txt; grep -n 'NavRail' /tmp/PartyFrameEnhanced-run.txt
```

Expected: exactly one `FAIL`, the Options surface-parity case, naming `NavRail`.

- [ ] **Step 5: Stub it.** The list keeps several names per line:

```sh
perl -pi -e 's/"SelectTab", "ChoiceGrid", "IdInput", "IdList",/"SelectTab", "ChoiceGrid", "IdInput", "IdList", "NavRail",/' settings/OptionsSetup.lua
crlf settings/OptionsSetup.lua
grep -c '"IdList", "NavRail",' settings/OptionsSetup.lua    # expect 1
```

- [ ] **Step 6: Gate.** Run the addon gate. Expected: `383` passed, 0 failed. luacheck 0/0. No
  `EOL FAIL`.

- [ ] **Step 7: The revendor bundle.**

```sh
rv_bundle "Not adopted here. No PartyFrameEnhanced page edits one instance out of many through sub-pages retargeted by one picker, which is the only shape options-ui-§13 sanctions the rail for." \
  "$(grep -E 'passed' /tmp/PartyFrameEnhanced-run.txt | tail -1)" \
  "$(/home/tushar/.claude/wow-addon/bin/ka0s-bounded luacheck . | tail -1)"
```

- [ ] **Step 8: Commit.**

```sh
git add libs/LibKa0s CLAUDE.md docs/ARCHITECTURE.md settings/OptionsSetup.lua docs/revendor/$(date +%F)-v1.61.0
git status --porcelain                  # expect empty
git commit -m "NR-PF-01: Re-vendor LibKa0s v1.61.0 and stub NavRail" \
  -m "LibKa0s payload from the v1.61.0 tag: Options 24 -> 25, OptionsTabs 4 -> 5, the new OptionsNav minor 1 (Options key 25.31.5.7.4.1). tests/_kit is unchanged at kit revision 27. CLAUDE.md provenance and docs/ARCHITECTURE.md's two version-now lines roll with it. The stub's no-op list gains NavRail for the Options surface-parity case." \
  -m "$TRAILERS"
```

### Task NR-PC-01: PrettyChat takes LibKa0s v1.61.0

**Files:**
- Modify (copied from the tag): `libs/LibKa0s/LibKa0s.xml`, `Options.lua`, `OptionsTabs.lua`. Create
  (copied): `libs/LibKa0s/OptionsNav.lua`.
- Modify: `CLAUDE.md:42`, `docs/testing.md:116`, `docs/ARCHITECTURE.md:409`,
  `settings/OptionsSetup.lua:136` (the stub's table literal).
- Create: `docs/revendor/<date>-v1.61.0/` (four files).

**Interfaces:** consumes the tag. Produces the live `NavRail` and the stub no-op.

- [ ] **Step 1: Preconditions and branch.**

```sh
cd $GIT/PrettyChat
git status --porcelain                              # expect empty
git branch --show-current                           # expect master
git rev-parse --short HEAD                          # bfac822 at planning time
git -C $GIT/LibKa0s rev-parse --short 'v1.61.0^{}'  # expect c6183bd
git switch -c $BR
```

- [ ] **Step 2: Copy the payload.** `lk_copy`. Expected: the four delta lines, `kit delta lines: 0`,
  `libs/LibKa0s == v1.61.0 byte for byte`.

- [ ] **Step 3: Provenance and version-now lines.**

```sh
perl -pi -e 's#(Bundles \[LibKa0s\]\(https://github\.com/tusharsaxena/LibKa0s\) )v1\.60\.0#${1}v1.61.0#' CLAUDE.md
perl -pi -e 's/the gate in the vendored LibKa0s v1\.60\.0 \(kit revision 27\)/the gate in the vendored LibKa0s v1.61.0 (kit revision 27)/ if $. == 116' docs/testing.md
perl -pi -e 's#(\*\*\[LibKa0s\]\(https://github\.com/tusharsaxena/LibKa0s\) )v1\.60\.0\*\*#${1}v1.61.0**# if $. == 409' docs/ARCHITECTURE.md
crlf CLAUDE.md docs/testing.md docs/ARCHITECTURE.md
grep -c 'LibKa0s) v1.61.0' CLAUDE.md                        # expect 1
sed -n 116p docs/testing.md | grep -c 'v1.61.0'             # expect 1
sed -n 409p docs/ARCHITECTURE.md | grep -c 'v1.61.0'        # expect 1
```

- [ ] **Step 4: Run and see the parity case fail.**

```sh
/home/tushar/.claude/wow-addon/bin/ka0s-bounded lua tests/run.lua > /tmp/PrettyChat-run.txt 2>&1
grep -E '^  FAIL' /tmp/PrettyChat-run.txt; grep -n 'NavRail' /tmp/PrettyChat-run.txt
```

Expected: exactly one `FAIL`, the Options surface-parity case, naming `NavRail`.

- [ ] **Step 5: Stub it**, aligned with the literal's `=` column:

```sh
perl -0pi -e 's/(        SelectTab            = function\(\) end,\r?\n)/$1        -- NavRail, new at LibKa0s v1.61.0 (OptionsNav minor 1): drawn only by a page\r\n        -- render, and no page here draws a rail, so the same inert no-op applies.\r\n        NavRail              = function() end,\r\n/' settings/OptionsSetup.lua
crlf settings/OptionsSetup.lua
grep -c 'NavRail              = function() end,' settings/OptionsSetup.lua   # expect 1
```

- [ ] **Step 6: Gate.** Run the addon gate. Expected: `518` passed, 0 failed. luacheck 0/0. No
  `EOL FAIL`.

- [ ] **Step 7: The revendor bundle.**

```sh
rv_bundle "Not adopted here. No PrettyChat page edits one instance out of many through sub-pages retargeted by one picker, which is the only shape options-ui-§13 sanctions the rail for." \
  "$(grep -E 'passed' /tmp/PrettyChat-run.txt | tail -1)" \
  "$(/home/tushar/.claude/wow-addon/bin/ka0s-bounded luacheck . | tail -1)"
```

- [ ] **Step 8: Commit.**

```sh
git add libs/LibKa0s CLAUDE.md docs/testing.md docs/ARCHITECTURE.md settings/OptionsSetup.lua docs/revendor/$(date +%F)-v1.61.0
git status --porcelain                  # expect empty
git commit -m "NR-PC-01: Re-vendor LibKa0s v1.61.0 and stub NavRail" \
  -m "LibKa0s payload from the v1.61.0 tag: Options 24 -> 25, OptionsTabs 4 -> 5, the new OptionsNav minor 1 (Options key 25.31.5.7.4.1). tests/_kit is unchanged at kit revision 27. CLAUDE.md provenance, docs/testing.md and docs/ARCHITECTURE.md's version-now lines roll with it. The stub's table literal gains a NavRail no-op for the Options surface-parity case." \
  -m "$TRAILERS"
```

### Task NR-WG-01: WhatGroup takes LibKa0s v1.61.0

**Files:**
- Modify (copied from the tag): `libs/LibKa0s/LibKa0s.xml`, `Options.lua`, `OptionsTabs.lua`. Create
  (copied): `libs/LibKa0s/OptionsNav.lua`.
- Modify: `CLAUDE.md:79`, `docs/testing.md:285`, `tests/loader.lua:52` (the hand-typed `LIBKA0S`
  list), `settings/OptionsSetup.lua:144` (the stub).
- Create: `docs/revendor/<date>-v1.61.0/` (four files).
- Not modified: the `NO_LIBKA0S` skip lists (`tests/test_envsetup.lua:21`,
  `tests/test_libka0s.lua` ~:497, `tests/test_mediasetup.lua` ~:25) and `tests/test_libka0s.lua:57`'s
  MODULES expectations, which are subsets.

**Interfaces:** consumes the tag. The headless loader loads `OptionsNav.lua`, so the live surface
gains `NavRail`, and the stub answers it.

- [ ] **Step 1: Preconditions and branch.**

```sh
cd $GIT/WhatGroup
git status --porcelain                              # expect empty
git branch --show-current                           # expect master
git rev-parse --short HEAD                          # 0fcfe6f at planning time
git -C $GIT/LibKa0s rev-parse --short 'v1.61.0^{}'  # expect c6183bd
git -C $GIT/LibKa0s status --porcelain              # expect empty: the vendor gate diffs its tree
git -C $GIT/LibKa0s diff --quiet 'v1.61.0' HEAD -- LibKa0s testkit && echo "LibKa0s tree == tag"   # expect the echo
git switch -c $BR
```

- [ ] **Step 2: Copy the payload.** `lk_copy`. Expected: the four delta lines, `kit delta lines: 0`,
  `libs/LibKa0s == v1.61.0 byte for byte`.

- [ ] **Step 3: Provenance and the version-now sentence.** `docs/testing.md:285` also says
  `../LibKa0s`'s HEAD "is that tag's commit". That is no longer true: LibKa0s's `master` is the merge
  `cf38896`, whose payload equals the tag's. So the clause is reworded to the fact the four diff
  commands test:

```sh
perl -pi -e 's#(Bundles \[LibKa0s\]\(https://github\.com/tusharsaxena/LibKa0s\) )v1\.60\.0#${1}v1.61.0#' CLAUDE.md
perl -pi -e 's/\*\*v1\.60\.0\*\*, and `\.\.\/LibKa0s`\x27s HEAD is that tag\x27s commit,/**v1.61.0**, and `..\/LibKa0s`\x27s HEAD carries that tag\x27s payload,/ if $. == 285' docs/testing.md
crlf CLAUDE.md docs/testing.md
grep -c 'LibKa0s) v1.61.0' CLAUDE.md                              # expect 1
sed -n 285p docs/testing.md | grep -c "HEAD carries that tag's payload"   # expect 1
```

- [ ] **Step 4: Run and see the list case fail.**

```sh
/home/tushar/.claude/wow-addon/bin/ka0s-bounded lua tests/run.lua > /tmp/WhatGroup-run.txt 2>&1
grep -E '^  FAIL' /tmp/WhatGroup-run.txt
```

Expected: exactly one `FAIL`, `tests/test_harness.lua`'s "explicit LibKa0s list matches
LibKa0s.xml" (23 in the XML, 22 listed).

- [ ] **Step 5: Load the file, then see parity fail.**

```sh
perl -0pi -e 's/(    "libs\/LibKa0s\/OptionsScroll\.lua",\r?\n)/$1    "libs\/LibKa0s\/OptionsNav.lua",\r\n/' tests/loader.lua
crlf tests/loader.lua
grep -c '"libs/LibKa0s/OptionsNav.lua",' tests/loader.lua    # expect 1
/home/tushar/.claude/wow-addon/bin/ka0s-bounded lua tests/run.lua > /tmp/WhatGroup-run.txt 2>&1
grep -E '^  FAIL' /tmp/WhatGroup-run.txt; grep -n 'NavRail' /tmp/WhatGroup-run.txt
```

Expected: the list case passes, and exactly one `FAIL` remains, the Options surface-parity case,
naming `NavRail`. The live surface has it now that `OptionsNav.lua` loads.

- [ ] **Step 6: Stub it.**

```sh
perl -0pi -e 's/(    H\.SelectTab            = function\(\) end\r?\n)/$1    -- NavRail, new at LibKa0s v1.61.0 (OptionsNav minor 1): drawn only by a page render, and no\r\n    -- page here draws a rail, so the same inert no-op applies.\r\n    H.NavRail              = function() end\r\n/' settings/OptionsSetup.lua
crlf settings/OptionsSetup.lua
grep -c 'H.NavRail              = function() end' settings/OptionsSetup.lua   # expect 1
```

- [ ] **Step 7: Gate, plus WhatGroup's vendor gate** (`CLAUDE.md:105-106`). Run the addon gate.
  Expected: `823` passed, 0 failed. luacheck 0/0. Then:

```sh
diff -r --strip-trailing-cr $GIT/LibKa0s/LibKa0s libs/LibKa0s && echo ok-libs-cr
diff -r $GIT/LibKa0s/LibKa0s libs/LibKa0s && echo ok-libs
diff -r --strip-trailing-cr $GIT/LibKa0s/testkit tests/_kit && echo ok-kit-cr
diff -r $GIT/LibKa0s/testkit tests/_kit && echo ok-kit
```

Expected: all four `ok-*` lines.

- [ ] **Step 8: The revendor bundle.**

```sh
rv_bundle "Not adopted here. No WhatGroup page edits one instance out of many through sub-pages retargeted by one picker. tests/loader.lua's hand-typed LIBKA0S list gains OptionsNav.lua in XML order, and the stub answers the NavRail the loaded file publishes." \
  "$(grep -E 'passed' /tmp/WhatGroup-run.txt | tail -1)" \
  "$(/home/tushar/.claude/wow-addon/bin/ka0s-bounded luacheck . | tail -1)"
```

- [ ] **Step 9: Commit.**

```sh
git add libs/LibKa0s CLAUDE.md docs/testing.md tests/loader.lua settings/OptionsSetup.lua docs/revendor/$(date +%F)-v1.61.0
git status --porcelain                  # expect empty
git commit -m "NR-WG-01: Re-vendor LibKa0s v1.61.0, load OptionsNav, stub NavRail" \
  -m "LibKa0s payload from the v1.61.0 tag: Options 24 -> 25, OptionsTabs 4 -> 5, the new OptionsNav minor 1 (Options key 25.31.5.7.4.1). tests/_kit is unchanged at kit revision 27. CLAUDE.md provenance and docs/testing.md roll with it; the testing.md clause now says ../LibKa0s's HEAD carries the tag's payload, since master is the merge after the tag. tests/loader.lua's hand-typed list loads OptionsNav.lua in XML order, and the stub gains H.NavRail for the Options surface-parity case. The vendor diff gate is clean." \
  -m "$TRAILERS"
```

### M1 checkpoint

Run after all ten NR-XX-01 commits exist (`./resume-state.sh M1` prints `M1: 10/10 COMPLETE`). For
each addon, in its root, on the branch head:

```sh
for a in AbsorbTracker BankLedger ConsumableMaster KickCD LootHistory MultiMeters PanelMaster PartyFrameEnhanced PrettyChat WhatGroup; do
  cd $GIT/$a
  print -- "== $a $(git rev-parse --short HEAD) dirty=$(git status --porcelain | wc -l)"
  S=$(mktemp -d); git -C $GIT/LibKa0s archive v1.61.0 LibKa0s | tar -x -C "$S"
  diff -r --strip-trailing-cr "$S/LibKa0s" libs/LibKa0s >/dev/null && echo "vendor == v1.61.0" || echo "VENDOR DRIFT"
done
```

Then re-run each addon's gate (ConsumableMaster with `lua5.1`). The checkpoint passes when every
addon reports `dirty=0`, `vendor == v1.61.0`, its dry-run total with 0 failed, and luacheck 0/0.
Append one row to `checkpoints.tsv`, `M1`, with each addon's head and totals, and "not pushed (not
authorized)".

---

## M2 — the two layouts

Rules for every M2 task:

- **Work in `$GIT/MultiMeters` or `$GIT/KickCD` on `feat/2026-09-26-navrail-adoption`**, after that
  repo's NR-XX-01. The two chains run in parallel, each strictly in order.
- **Line numbers are planning-time** (MultiMeters `c374876`, KickCD `604e922`, before NR-XX-01).
  Earlier tasks shift them, so anchor every edit on the quoted code or the case name and use the
  number only to find it. Every edit is made with the Edit tool (or the perl shown), then `crlf` on
  the file.
- **Citations move with the code.** Each addon's doc tests (`tests/test_doc_structure.lua`,
  MultiMeters' `tests/test_docmap.lua`) check `file:line` and structure claims in `docs/`. A task
  that shifts lines in a cited file fixes the citations its gate names **in the same commit**. Then
  it greps `docs/` and `README.md` for the file names it touched and fixes any citation that no
  longer points at its symbol. The doc tests do not catch every drift (AuraMaster's `99_REPORT.md`,
  lesson 1).
- **The generated inventory and the badge move with the tests.** A task that adds, renames or
  deletes a case regenerates `docs/test-cases.md`
  (`/home/tushar/.claude/wow-addon/bin/ka0s-bounded lua tests/run.lua --list > docs/test-cases.md`,
  then `crlf`) and sets the README **Tests** badge from the same run:

```sh
P=$(grep -cE '^  PASS' /tmp/${PWD:t}-run.txt); A=$(grep -cE '^  (PASS|FAIL|SKIP)' /tmp/${PWD:t}-run.txt)
perl -pi -e "s/Tests-\d+%2F\d+_passing/Tests-${P}%2F${A}_passing/" README.md; crlf README.md
```

- **The locale moves with its callers.** Each addon's `tests/test_locale.lua` fails on an `L["…"]`
  missing from `locales/enUS.lua`, and on an enUS key nothing uses. Keys are added and removed in the
  commit that adds or removes their callers. Keys are the English strings, so a reworded string is a
  renamed key.
- **Doc tables get rows inserted as their own lines**, never by a substitution that can swallow a
  neighbor (AuraMaster `99_REPORT.md`, lesson 2). `git diff` every table edit before committing.

### Task NR-MM-02: the Windows page — band, rail, entry

**Files:**
- Modify: `settings/OptionsSetup.lua`: insert the section registry above `local lib = LibStub and
  LibStub("LibKa0s-Options-1.0", true)` (:153); add three names to the stub's no-op list (after
  NR-MM-01's `"NavRail",`); append the Windows-page block after the last line,
  `NS.RefreshOptionsPanel = function() Helpers.RefreshAllPanels() end` (:530).
- Modify: `settings/Windows.lua`: the header (:1-4), `renderCopySource`'s label (:382), `render`
  (:444-477) becomes `renderGeneral`, `Build` (:479-495), and a section registration at the end.
- Modify: `settings/Columns.lua` :300-402: `render` splits into `renderSection` (strip and body) and
  the sub-page's own `render`; the Defaults pair becomes `restoreDefaults(ctx)`; a section
  registration.
- Modify: `settings/Frame.lua`, `Header.lua`, `Bars.lua`, `Tooltip.lua`, `Visibility.lua`: each
  appends its section registration. The sub-pages stay until NR-MM-04.
- Modify: `locales/enUS.lua` (the "Windows page" block, :136-162): ten keys added.
- Create: `tests/test_windows_rail.lua`. Modify: `tests/run.lua` (`SUITES`: `"test_windows_rail",`
  after `"test_columns",`).
- Modify: `tests/test_options_panel.lua` (the "declines a Defaults button" case :286-300, the
  `TABBED` table :919-930), `tests/test_degraded.lua` (the namespace-parity list :625-628).
- Modify: `docs/settings-panel.md` (the page table's row 2; a new section before "The tab strip and
  the banner", :283). Modify (generated): `docs/test-cases.md`, the README Tests badge.

**Interfaces:**
- Produces, on both arms: `NS.RegisterWindowSection(key, label, spec)` and `NS.WindowSection(key) ->
  { key, label, tooltip, spec } | nil`. `spec` = `{ tooltip = string, render = fn(ctx)?, defaults =
  fn(ctx)? }`.
- Produces, live: `Helpers.RenderWindowPage(ctx)`, `Helpers.RestoreActiveSection(ctx)` and
  `Helpers.__bindWindowsPage(ctx)`; stub: no-ops of all three.
- ctx fields: `ctx.activeSection` (an entry key), `ctx.sectionTabs` (entry key -> tab key),
  `ctx.__renderedSection`.
- Consumes: `H.WindowBanner`, `H.Relayout` (`settings/Windows.lua`), `NS.CancelReorder`
  (`settings/ColumnBlocks.lua:210`), `Helpers.NavRail` (LibKa0s v1.61.0).

- [ ] **Step 1: Write the failing tests.** Create `tests/test_windows_rail.lua`, then `crlf` it:

```lua
-- tests/test_windows_rail.lua
--
-- The Windows page as one page per window (MultiMeters#55): the Active window band, the nav rail
-- (General, Frame, Header, Bars, Tooltip, Visibility, Columns), each entry's own tab strip, the tab
-- each entry keeps, the Columns reorder cancel on a rail switch, and Defaults for the active entry.
-- The pattern is AuraMaster's Containers page (#6) on LibKa0s v1.61.0's O.NavRail. Pinned from the
-- outside: a fresh instance per case, the page shown the way Blizzard shows it, the rail clicked
-- through the library's own entry buttons.

local T = _G.MULTIMETERS_TEST
local test = T.test
local assertEqual, assertTrue, assertFalse = T.assertEqual, T.assertTrue, T.assertFalse

local RAIL_ORDER = "windows,frame,header,bars,tooltip,visibility,columns"

--- A fresh instance with spies on the three chrome calls, recording each page's last rail and strip,
--- and handles on its Windows page. `opts` goes to T.load.
local function env(opts)
    local inst = T.load(opts)
    local H = inst.NS.Helpers
    local rails, strips, calls = {}, {}, {}
    local navRail, tabStrip, pageBanner = H.NavRail, H.TabStrip, H.PageBanner
    H.NavRail = function(ctx, spec, ...)
        calls[#calls + 1] = "NavRail"
        rails[ctx] = spec
        return navRail(ctx, spec, ...)
    end
    H.TabStrip = function(ctx, spec, ...)
        calls[#calls + 1] = "TabStrip"
        strips[ctx] = spec
        return tabStrip(ctx, spec, ...)
    end
    H.PageBanner = function(ctx, spec, ...)
        calls[#calls + 1] = "PageBanner"
        return pageBanner(ctx, spec, ...)
    end

    local P = { inst = inst, NS = inst.NS, L = inst.NS.L, calls = calls }

    function P.ctx() return H.__panelFor("windows") end

    --- Show the Windows page the way Blizzard does, driving the genuine deferred render.
    function P.show()
        local ctx = P.ctx()
        assertTrue(ctx ~= nil, "no Windows page registered")
        ctx.panel:Hide()
        ctx.panel:Show()
        -- The render is pcall'd by the library, so a raise shows up as no rail, not as an error.
        assertTrue(rails[ctx] ~= nil, "the Windows page drew no rail (its renderer raised)")
        return ctx
    end

    function P.railKeys()
        local out = {}
        for i, e in ipairs((rails[P.ctx()] or {}).entries or {}) do out[i] = e.key end
        return table.concat(out, ",")
    end

    function P.railValue() return (rails[P.ctx()] or {}).value end

    function P.tabLabels()
        local out = {}
        for i, t in ipairs((strips[P.ctx()] or {}).tabs or {}) do out[i] = t.label end
        return table.concat(out, "|")
    end

    --- The library's own rail button for entry `key` (ctx.__railKids is the rail's ledger, in order).
    function P.railButton(key)
        local ctx = P.ctx()
        for i, e in ipairs((rails[ctx] or {}).entries or {}) do
            if e.key == key then return ctx.__railKids[i] end
        end
        error("the rail drew no entry " .. tostring(key), 2)
    end

    --- Click rail entry `key` the way the player does, and answer the page's ctx.
    function P.rail(key)
        local ctx = P.ctx()
        P.railButton(key):__fire("OnClick")
        ctx.panel:Hide()
        ctx.panel:Show()
        return ctx
    end

    return P
end

--- The groups of a page key's rows, in declaration order: the strip RenderTabbedSchema draws.
local function groupsOf(NS, page)
    local out, seen = {}, {}
    for _, row in ipairs(NS.SchemaForPage(page, NS.State and NS.State.activeWindowId)) do
        if row.group and not seen[row.group] then
            seen[row.group] = true
            out[#out + 1] = row.group
        end
    end
    return table.concat(out, "|")
end

--- Whether any widget under `root` is a `wtype` carrying `text` as its label or its text.
local function has(root, wtype, text)
    for _, c in ipairs(root and root.children or {}) do
        if c.type == wtype and (c.text == text or c.labelText == text) then return true end
        if has(c, wtype, text) then return true end
    end
    return false
end

-- ── the registry ─────────────────────────────────────────────────────────────────────────────

test("Windows rail: the seven entries register under their page keys, on both builds", function()
    local L = T.NS.L
    local LABELS = {
        windows = "General", frame = "Frame", header = "Header", bars = "Bars",
        tooltip = "Tooltip", visibility = "Visibility", columns = "Columns",
    }
    local builds = { live = T.NS, ["library-absent"] = T.load{ libFiles = {} }.NS }
    for build, NSx in pairs(builds) do
        for key, label in pairs(LABELS) do
            -- red under: a page file registering no section, or the registry defined inside the
            -- live arm only (a library-absent load would lose it)
            local s = NSx.WindowSection and NSx.WindowSection(key)
            assertTrue(s ~= nil, build .. ": " .. key .. " registered no section")
            assertEqual(s.key, key, build .. ": " .. key .. " keeps its page key, so every row path is unchanged")
            assertEqual(s.label, L[label], build .. ": " .. key .. "'s rail label")
            assertEqual(type(s.tooltip), "string", build .. ": " .. key .. " carries a rail tooltip")
        end
    end
end)

-- ── the page ─────────────────────────────────────────────────────────────────────────────────

test("Windows rail: the band, then the rail General..Columns, 120 wide, opening on General", function()
    local P = env()
    local ctx = P.show()
    -- red under: the rail in TOC order, an entry missing, or the page opening on Frame
    assertEqual(P.railKeys(), RAIL_ORDER)
    assertEqual(ctx.activeSection, "windows", "the page opens on General (options-ui-§14)")
    assertEqual(P.railValue(), "windows")
    assertEqual(ctx.railWidth, 120)
    assertEqual(ctx.__bannerWidget and ctx.__bannerWidget.labelText, P.L["Active window"],
        "the band is the Active window picker")
end)

test("Windows rail: the draw order is PageBanner, NavRail, TabStrip", function()
    local P = env()
    P.show()
    -- red under: the rail drawn before the band (its top ignores the band) or after the strip (the
    -- strip places itself with no inset)
    assertEqual(table.concat({ P.calls[1], P.calls[2], P.calls[3] }, ","), "PageBanner,NavRail,TabStrip")
end)

test("Windows rail: General is one General tab holding the window's acts and a Copy settings from block", function()
    local P = env()
    local ctx = P.show()
    local L = P.L
    -- red under: the old Window / Copy from pair, or Copy from left on a tab of its own
    assertEqual(P.tabLabels(), L["General"])
    assertEqual(ctx.activeTab, L["General"])
    for _, b in ipairs({ "New window", "Duplicate window", "Delete window", "Copy" }) do
        assertTrue(has(ctx.scroll, "Button", L[b]), "General draws " .. b)
    end
    assertTrue(has(ctx.scroll, "EditBox", L["Window name"]), "General draws the name box")
    assertTrue(has(ctx.scroll, "Dropdown", L["Source window"]), "General draws the copy source")
    assertTrue(has(ctx.scroll, "Dropdown", L["Settings to copy"]), "General draws the group filter")
    assertTrue(has(ctx.scroll, "Heading", L["Copy settings from"]), "the copy block has its own heading")
    assertFalse(has(ctx.scroll, "Dropdown", L["Active window"]), "the band is the only picker")
end)

test("Windows rail: a rail click draws that entry's own strip under the same band", function()
    local P = env()
    P.show()
    local L = P.L
    local ctx = P.rail("bars")
    assertEqual(ctx.activeSection, "bars")
    assertEqual(P.railValue(), "bars")
    -- red under: the entry rendered under the page's own key (General's one tab, not Bars')
    assertEqual(P.tabLabels(), groupsOf(P.NS, "bars"))
    assertEqual(ctx.__bannerWidget.labelText, L["Active window"], "the band is drawn with the entry")
    P.rail("columns")
    assertEqual(P.tabLabels(), table.concat({ L["Columns"], L["Header text"], L["Header background"] }, "|"))
end)

test("Windows rail: each entry keeps its own tab, including one chosen by the library's own strip click", function()
    local P = env()
    P.show()
    local L = P.L
    local ctx = P.rail("frame")
    ctx.__tabKids[2]:__fire("OnClick")              -- the library's own strip click: no host render
    assertEqual(ctx.activeTab, L["Size and position"])
    P.rail("bars")
    assertEqual(ctx.activeTab, L["Bar"], "Bars opens on its first tab")
    ctx.__tabKids[3]:__fire("OnClick")
    assertEqual(ctx.activeTab, L["Border"])
    P.rail("frame")
    -- red under: one scalar activeTab for the page (Frame reopens on Border's slot or its first tab),
    -- or a stash only on host renders (the strip click above never reaches the host)
    assertEqual(ctx.activeTab, L["Size and position"])
    P.rail("columns")
    ctx.__tabKids[3]:__fire("OnClick")              -- Columns' own strip: a host render
    assertEqual(ctx.activeTab, L["Header background"])
    P.rail("windows")
    P.rail("bars")
    assertEqual(ctx.activeTab, L["Border"], "and through General")
    P.rail("columns")
    assertEqual(ctx.activeTab, L["Header background"])
end)

test("Windows rail: choosing another window in the band keeps the entry and its tab", function()
    local P = env()
    local NS, L = P.NS, P.L
    assertTrue(NS.WindowManager:Create("Second"))
    local list = NS.Database.GetWindows()
    P.show()
    local ctx = P.rail("bars")
    ctx.__tabKids[3]:__fire("OnClick")
    assertEqual(ctx.activeTab, L["Border"])
    ctx.__bannerWidget:__fire("OnValueChanged", list[2].id)
    assertEqual(NS.State.activeWindowId, list[2].id)
    -- red under: a window switch resetting the entry or the tab (options-ui-§14: the rail is not a picker)
    assertEqual(ctx.activeSection, "bars")
    assertEqual(ctx.activeTab, L["Border"])
    assertEqual(ctx.unit, list[2].id, "the page now edits the second window")
end)

-- Review Focus 1 (NR-MM-02).
test("Windows rail: leaving Columns on the rail mid-drag cancels the reorder BEFORE the scroll clear", function()
    local P = env()
    local inst, NS = P.inst, P.NS
    P.show()
    local ctx = P.rail("columns")
    -- The blocks are raw frames off the mock's creation register, newest first (tests/test_columns.lua).
    local frames, blocks = inst.mocks.__frames, {}
    for i = #frames, 1, -1 do
        local f = frames[i]
        if f.mmIndex and blocks[f.mmIndex] == nil then blocks[f.mmIndex] = f end
    end
    inst.mocks.setMouseDown("LeftButton", true)
    inst.mocks.setCursor(0, 1000)
    blocks[1].mmHandle:_run("OnMouseDown")
    assertTrue(ctx.mmReorder ~= nil, "the press left no live reorder to cancel")

    local order = {}
    local realCancel, realClear = NS.CancelReorder, NS.Helpers.ClearScroll
    NS.CancelReorder = function(c)
        order[#order + 1] = c.mmReorder and "cancel-live" or "cancel"
        return realCancel(c)
    end
    NS.Helpers.ClearScroll = function(c)
        order[#order + 1] = "clear"
        return realClear(c)
    end
    local button = P.railButton("frame")
    local ok, err = pcall(function() button:__fire("OnClick") end)
    NS.CancelReorder, NS.Helpers.ClearScroll = realCancel, realClear
    inst.mocks.setMouseDown("LeftButton", false)
    assertTrue(ok, tostring(err))

    assertEqual(ctx.activeSection, "frame", "the rail click did not switch entries")
    -- red under: the page renderer clearing the scroll before it cancels (a live handle handed to a
    -- pooled frame), or cancelling only when the Columns entry is the one being drawn
    assertEqual(order[1], "cancel-live", "the first thing the switch did was not the cancel: " .. table.concat(order, ","))
    assertEqual(order[2], "clear", "no scroll clear followed the cancel: " .. table.concat(order, ","))
    assertTrue(ctx.mmReorder == nil, "the reorder controller survived the rail switch")
end)

-- Review Focus 2 (NR-MM-02).
test("Windows rail: Defaults restores the active entry's rows for the active window; General keeps the name; Columns restores both halves", function()
    local P = env()
    local NS, L, inst = P.NS, P.L, P.inst
    assertTrue(NS.WindowManager:Create("Second"))
    local w1, w2 = NS.Database.GetWindows()[1], NS.Database.GetWindows()[2]
    NS.State.SetActiveWindow(w1.id)
    assertTrue(NS.SetByPath("window.frame.width", 300, w2.id))
    assertTrue(NS.SetByPath("window.frame.width", 350, w1.id))
    assertTrue(NS.SetByPath("window.header.height", 30, w1.id))
    P.show()
    local ctx = P.rail("frame")

    ctx.panel.defaultsOnClick()
    -- red under: a click closure that fixed the entry at build time (General's nothing), or a walk
    -- over every entry's rows
    assertEqual(NS.Database.FindWindow(w1.id).frame.width, 694, "a Frame row is back")
    assertEqual(NS.Database.FindWindow(w1.id).header.height, 30, "a Header row is not a Frame row")
    assertEqual(NS.Database.FindWindow(w2.id).frame.width, 300, "only the active window")

    P.rail("windows")
    assertTrue(NS.WindowManager:Rename(NS.Database.FindWindow(w1.id).name, "Mine"))
    local before = #inst.mocks.__chat
    ctx.panel.defaultsOnClick()
    -- red under: General's Defaults walking the window.name row (the window renamed to "Multi Meters")
    assertEqual(NS.Database.FindWindow(w1.id).name, "Mine", "General keeps the window's name")
    local said = inst.mocks.__chat[#inst.mocks.__chat] or ""
    assertTrue(#inst.mocks.__chat > before
        and said:find(L["General has no settings to restore. The window's name is kept."], 1, true) ~= nil,
        "General says why nothing moved")

    P.rail("columns")
    local shipped = NS.DefaultWindow(w1.id).columns
    local scrambled = {}
    for i = #shipped, 1, -1 do
        scrambled[#scrambled + 1] = { stat = shipped[i].stat, enabled = i % 2 == 0 }
    end
    assertTrue(NS.SetByPath("window.columns", scrambled))
    assertTrue(NS.SetByPath("window.columnHeader.font", "Skurri"))
    ctx.panel.defaultsOnClick()
    local after = NS.Database.FindWindow(w1.id)
    for i, col in ipairs(shipped) do
        assertEqual(after.columns[i].stat, col.stat, "column " .. i .. " is the shipped statistic")
    end
    assertEqual(after.columnHeader.font, "Friz Quadrata TT", "and the header rows came back with it")
end)

test("Windows rail: the page offers one Defaults button whose tooltip fits every entry", function()
    local P = env()
    local ctx = P.show()
    assertTrue(ctx.panel.wantsDefaultsButton, "the Windows page offers Defaults since #55")
    assertEqual(ctx.panel.defaultsTooltip,
        P.L["Restore the active window's settings in the section on screen to their shipped values. On Columns that includes the shipped column list. General has nothing to restore: the window's name is kept."])
end)
```

  Register the suite in `tests/run.lua`: after `    "test_columns",` add `    "test_windows_rail",`.
  Then `crlf tests/test_windows_rail.lua tests/run.lua`.

- [ ] **Step 2: Run and see them fail.**

```sh
/home/tushar/.claude/wow-addon/bin/ka0s-bounded lua tests/run.lua > /tmp/MultiMeters-run.txt 2>&1
grep -E '^  (FAIL|PASS)  Windows rail:' /tmp/MultiMeters-run.txt
```

  Expected: every `Windows rail:` case `FAIL`s. The registry case fails on `NS.WindowSection` being
  nil. The page cases fail with "the Windows page drew no rail", because `NavRail` is never called.
  Nothing else fails.

- [ ] **Step 3: The registry, above the fork.** In `settings/OptionsSetup.lua`, insert immediately
  above `local lib = LibStub and LibStub("LibKa0s-Options-1.0", true)`:

```lua
-- ---------------------------------------------------------------------
-- The Windows page's entries (MultiMeters#55)
-- ---------------------------------------------------------------------
--
-- ONE PAGE PER WINDOW. The Windows page draws the Active window band, a nav rail
-- (LibKa0s-Options' O.NavRail, options-ui-§13) whose entries are registered here,
-- and the selected entry's own tab strip. An entry IS a page key: its schema rows
-- keep `page`, their window-relative paths and their defaults, so `/mm get`,
-- `/mm set`, `/mm list`, profiles and every reset never see the rail. Each
-- settings/<entry>.lua registers at FILE LOAD, so the registry lives HERE, above
-- the fork: a library-absent load still knows the entries, and a page file never
-- has to ask which build it is on.
local sections = {}

-- The rail's order. General first -- options-ui-§14's escape: the acts on the
-- window whole live on the FIRST entry, named General, and the page opens on it --
-- then the window's surfaces. Fixed here, not taken from the TOC.
local GENERAL_SECTION = "windows"
local SECTION_ORDER = { GENERAL_SECTION, "frame", "header", "bars", "tooltip", "visibility", "columns" }

--- Register one entry of the Windows page.
--- @param key string    the entry's page key: the `page` its schema rows carry
--- @param label string  the rail entry's label
--- @param spec table    { tooltip = the rail entry's tooltip,
---                        render = fn(ctx), drawing the entry's strip and body under the band and
---                                 the rail (default: H.RenderTabbedSchema(ctx, key)),
---                        defaults = fn(ctx), the entry's Defaults (default: H.RestoreDefaults(key, ctx)) }
function NS.RegisterWindowSection(key, label, spec)
    spec = spec or {}
    sections[key] = { key = key, label = label, tooltip = spec.tooltip, spec = spec }
end

--- The registered entry `key`, or nil. Read-only: for the suite and the Windows page.
function NS.WindowSection(key) return sections[key] end

```

- [ ] **Step 4: The stub's no-ops.** In the stub's name list, after NR-MM-01's `"NavRail",` line, add:

```lua
        -- The Windows page's own members (MultiMeters#55), decorated onto the live
        -- instance below the fork. settings/Windows.lua's builder is their only caller,
        -- and it never runs here; the degraded scan and the parity case read them anyway.
        "RenderWindowPage", "RestoreActiveSection", "__bindWindowsPage",
```

- [ ] **Step 5: The Windows page, on the live arm.** Append at the end of
  `settings/OptionsSetup.lua`, after `NS.RefreshOptionsPanel = function() Helpers.RefreshAllPanels() end`:

```lua

-- ---------------------------------------------------------------------
-- The Windows page: the band, the nav rail, the selected entry (#55)
-- ---------------------------------------------------------------------
--
-- AuraMaster's Containers page (#6) is the pattern. The entry on screen and each
-- entry's tab are session state on the ctx and never persisted (options-ui-§13);
-- the band stays the only picker, and a window switch leaves both alone
-- (options-ui-§14).

-- The Windows page's ctx, bound by settings/Windows.lua's builder: the one page
-- SelectSection moves (NR-MM-03).
local windowsCtx

--- The entries the rail lists, in rail order. Every window has every entry, so
--- nothing is filtered by the window; an entry whose file did not load is absent.
local function railSections()
    local out = {}
    for _, key in ipairs(SECTION_ORDER) do
        if sections[key] then out[#out + 1] = sections[key] end
    end
    return out
end

--- The entry to draw: the one the page holds while the rail lists it, else General.
local function settleSection(ctx, list)
    for _, s in ipairs(list) do
        if s.key == ctx.activeSection then return s end
    end
    return list[1]
end

--- Keep the tab the page is on for the entry it last drew. Called before ANYTHING
--- moves the entry: the library's own strip click never calls back here
--- (RenderTabbedSchema re-renders the strip and the rows itself), so leaving is the
--- one moment the host sees the tab.
local function stashTab(ctx)
    local drawn = ctx.__renderedSection
    if drawn then ctx.sectionTabs[drawn] = ctx.activeTab end
    ctx.__renderedSection = nil
end

--- Bind the Windows page's ctx (settings/Windows.lua's builder). The page opens on General.
function Helpers.__bindWindowsPage(ctx)
    windowsCtx = ctx
    ctx.sectionTabs = {}
    ctx.activeSection = GENERAL_SECTION
end

--- Render the Windows page: the Active window band, the nav rail, then the entry's
--- strip and body -- the library's draw order, PageBanner, NavRail, TabStrip.
function Helpers.RenderWindowPage(ctx)
    -- FIRST, before anything clears. The Columns entry's drag handles stay parented
    -- to the scroll's pooled containers until the controller is cancelled
    -- (settings/ColumnBlocks.lua), and the seven entries share this one ctx: a rail
    -- click, a window switch and Columns' own tab click all land here, and each
    -- clears the scroll next. A no-op when nothing is being dragged.
    if NS.CancelReorder then NS.CancelReorder(ctx) end
    ctx.sectionTabs = ctx.sectionTabs or {}
    stashTab(ctx)
    local list = railSections()
    local section = settleSection(ctx, list)
    if not section then return end
    ctx.activeSection = section.key
    ctx.activeTab = ctx.sectionTabs[section.key]
    -- Every window.* row resolves against the ACTIVE window; the id is also the
    -- library's row filter (the descriptor's rowsForPage), as on the sub-pages.
    ctx.unit = NS.State and NS.State.activeWindowId or nil
    Helpers.ClearScroll(ctx)
    Helpers.WindowBanner(ctx)
    local entries = {}
    for i, s in ipairs(list) do entries[i] = { key = s.key, label = s.label, tooltip = s.tooltip } end
    Helpers.NavRail(ctx, {
        entries  = entries,
        value    = section.key,
        onSelect = function(key)
            stashTab(ctx)
            ctx.activeSection = key
            Helpers.RefreshPanel(ctx, true)
        end,
    })
    if section.spec.render then
        section.spec.render(ctx)
    else
        Helpers.RenderTabbedSchema(ctx, section.key)
    end
    Helpers.Relayout(ctx)
    ctx.__renderedSection = section.key
end

--- The Windows page's Defaults: the entry on screen, read at CLICK time. The library
--- builds the button once, at the first show, and captures this handler with it, so
--- a closure that read the entry at build time would reset General's set from Frame.
function Helpers.RestoreActiveSection(ctx)
    local s = sections[ctx and ctx.activeSection] or sections[GENERAL_SECTION]
    if not s then return end
    if s.spec.defaults then return s.spec.defaults(ctx) end
    Helpers.RestoreDefaults(s.key, ctx)
end

--- Test seam: the ctx the Windows page bound, or nil before its builder ran.
function Helpers.__windowsCtx() return windowsCtx end
```

  `windowsCtx` is read by `Helpers.SelectSection` from NR-MM-03 on. The `__windowsCtx` seam is its
  reader until then, so luacheck has no assigned-but-never-accessed local (W231) at this commit. It
  is `__`-prefixed, so it is outside the surface-parity comparison.

- [ ] **Step 6: The General entry.** In `settings/Windows.lua`:

  1. Replace the header's first paragraph (lines 3-4, `-- The Windows page: the window picker, the
     five registry actions (new, rename,` / `-- delete, duplicate) and "copy settings from", with a
     group filter.`) with:

```lua
-- The Windows page (MultiMeters#55): one page per window. The Active window
-- picker is the band, the nav rail chooses General, Frame, Header, Bars,
-- Tooltip, Visibility or Columns, and each entry keeps its own tab strip
-- (settings/OptionsSetup.lua, Helpers.RenderWindowPage). This file owns the band
-- (H.WindowBanner) and the General entry: the registry actions (new, rename,
-- delete, duplicate) and "copy settings from", with a group filter.
```

  2. In `renderCopySource`, change `        label   = L["Copy settings from"],` to
     `        label   = L["Source window"],`. The heading above it now says "Copy settings from"
     (02_SPEC R2).
  3. Replace everything from the comment line `-- The page's content is bespoke rather than schema
     rows -- a name box, three registry buttons,` through the `end` that closes `local function
     render(ctx)` with:

```lua
--- The General entry: ONE tab, named General (options-ui-§14's escape -- the acts on
--- the window whole live on the rail's first entry), holding two headed blocks: the
--- window itself, and "Copy settings from", which was a tab of its own before
--- MultiMeters#55 folded it in. Bespoke rather than schema rows -- a name box,
--- registry buttons, a source picker, a group filter and a Copy button -- so the
--- one-tab strip is drawn directly with H.TabStrip. The band, the rail, the clear
--- and the relayout are the page renderer's.
local function renderGeneral(ctx)
    H.TabStrip(ctx, {
        tabs     = { { key = L["General"], label = L["General"] } },
        value    = L["General"],
        onSelect = function() end,
    })
    ctx.activeTab = L["General"]

    H.Section(ctx, L["Window"])
    renderWindowTab(ctx)
    H.Section(ctx, L["Copy settings from"])
    renderCopyTab(ctx)
end
```

  4. In `Build`, replace everything from `    -- No Defaults button: nothing on this page is a schema row, so there is`
     through `    H.SetRenderer(ctx, render)` with:

```lua
    -- DEFAULTS FOR THE ENTRY ON SCREEN (MultiMeters#55). The button is page-wide in
    -- the sense options-ui-§13 means on a railed page: the active entry's set, which
    -- is what that entry's own sub-page button restored -- for the active window only,
    -- because every row resolves against it. General's set is empty (the Windows page
    -- had no button), and its Defaults says so rather than renaming the window.
    local ctx = H.CreatePanel("MultiMetersWindowsPanel", L["Windows"], {
        pageKey         = PAGE,
        defaultsButton  = true,
        defaultsTooltip = L["Restore the active window's settings in the section on screen to their shipped values. On Columns that includes the shipped column list. General has nothing to restore: the window's name is kept."],
    })
    ctx.panel.defaultsOnClick = function() H.RestoreActiveSection(ctx) end

    H.__bindWindowsPage(ctx)
    H.SetRenderer(ctx, H.RenderWindowPage)
```

  5. Immediately above the final `if NS.RegisterOptionsPage then`, add:

```lua
-- The General entry of the Windows page (MultiMeters#55), first on the rail.
NS.RegisterWindowSection(PAGE, L["General"], {
    tooltip  = L["Rename, create, duplicate or delete windows, and copy settings from another window."],
    render   = renderGeneral,
    defaults = function() print_(L["General has no settings to restore. The window's name is kept."]) end,
})

```

- [ ] **Step 7: The Columns entry.** In `settings/Columns.lua`, replace everything from
  `local function render(ctx)` to the end of the file with:

```lua
--- The Columns entry's strip and body, drawn under the band and the rail by the
--- Windows page's renderer (settings/OptionsSetup.lua, Helpers.RenderWindowPage) --
--- and, until the Columns sub-page retires, under the band by that page's own
--- renderer below. The reorder cancel and the scroll clear are the CALLER's, in
--- that order; both callers cancel first.
local function renderSection(ctx)
    if NS.State and NS.State.debug and NS.Debug then
        local w0 = activeWindow()
        NS.Debug("Columns", "paint window=%s", tostring(w0 and w0.id))
    end

    H.TabStrip(ctx, {
        tabs = {
            { key = TAB_COLUMNS,    label = TAB_COLUMNS },
            { key = TAB_HEADER_TEXT, label = TAB_HEADER_TEXT },
            { key = TAB_HEADER_BG,   label = TAB_HEADER_BG },
        },
        value = ctx.activeTab or TAB_COLUMNS,
        onSelect = function(key)
            if key == ctx.activeTab then return end
            ctx.activeTab = key
            -- No H.ClearScroll here: RefreshPanel(ctx, true) re-enters the page's
            -- renderer, which cancels the reorder controller and THEN clears the
            -- scroll. Clearing here too would run BEFORE the cancel on a tab click.
            H.RefreshPanel(ctx, true)
        end,
    })
    ctx.activeTab = ctx.activeTab or TAB_COLUMNS

    if ctx.activeTab == TAB_HEADER_TEXT then
        H.RenderRows(ctx, rowsOfGroup(TAB_HEADER_TEXT), nil, nil, { noHeadings = true })
    elseif ctx.activeTab == TAB_HEADER_BG then
        H.RenderRows(ctx, rowsOfGroup(TAB_HEADER_BG), nil, nil, { noHeadings = true })
    else
        renderBlockEditor(ctx)
    end
end

--- The Columns sub-page's own renderer, until it retires.
local function render(ctx)
    -- BEFORE ClearScroll, not after. ClearScroll hands every AceGUI container on this page back to
    -- a process-wide pool, and a drag handle is parented to one of them until the controller is
    -- canceled -- so canceling afterwards means some unrelated widget has already been handed a
    -- frame with a live handle on it.
    if NS.CancelReorder then NS.CancelReorder(ctx) end
    H.ClearScroll(ctx)
    H.WindowBanner(ctx)
    renderSection(ctx)
    H.Relayout(ctx)
end

--- The Columns Defaults: TWO RESETS BEHIND ONE BUTTON, because this entry carries both a bespoke
--- array (the column list, addressable only as a whole -- see restoreShippedColumns above) and
--- eight window.columnHeader.* schema rows on its other two tabs. The button restores the whole
--- entry, not the visible tab (options-ui-§13), so both halves come back whichever tab is showing.
---
--- ONE LOG LINE FOR BOTH (debug-logging-§10). The pair is bracketed here, so the array write sits
--- in the same bracket as the library's page walk -- whose own bracket nests inside this one --
--- and the press logs a single `[Set] reset columns: N rows`, the array counted as one row when it
--- moved.
local function restoreDefaults(ctx)
    NS.Bulk.run("reset", PAGE, function()
        restoreShippedColumns()
        H.RestoreDefaults(PAGE, ctx)
    end)
end

local function Build(mainCategory)
    if not (Settings and Settings.RegisterCanvasLayoutSubcategory) then return nil end
    if not (H and H.CreatePanel) then return nil end

    -- A DEFAULTS BUTTON THAT DOES ITS OWN WORK: the statistics that ship ticked, in the order they
    -- ship in, and the header rows (restoreDefaults above).
    local ctx = H.CreatePanel("MultiMetersColumnsPanel", L["Columns"], {
        pageKey          = PAGE,
        defaultsButton   = true,
        defaultsTooltip  = L["Restore the statistics this window ships with, ticked and in their shipped order, and the header text and background settings on this page to their shipped values."],
    })
    ctx.panel.defaultsOnClick = function() restoreDefaults(ctx) end

    H.SetRenderer(ctx, function(c)
        c.unit = NS.State and NS.State.activeWindowId or nil
        render(c)
    end)

    return Settings.RegisterCanvasLayoutSubcategory(mainCategory, ctx.panel, NS.SubPageLabel(L["Columns"]))
end

-- The Columns entry of the Windows page (MultiMeters#55).
NS.RegisterWindowSection(PAGE, L["Columns"], {
    tooltip  = L["Which statistics this window shows, in what order, and how the column headers look."],
    render   = renderSection,
    defaults = restoreDefaults,
})

if NS.RegisterOptionsPage then
    NS.RegisterOptionsPage(PAGE, L["Columns"], Build)
end
```

- [ ] **Step 8: The other five entries.** Append to each file (after its final `end`):

  `settings/Frame.lua`:

```lua

-- The Frame entry of the Windows page (MultiMeters#55).
NS.RegisterWindowSection(PAGE, L["Frame"], {
    tooltip = L["This window's size, position, background, border and rows."],
})
```

  `settings/Header.lua`:

```lua

-- The Header entry of the Windows page (MultiMeters#55).
NS.RegisterWindowSection(PAGE, L["Header"], {
    tooltip = L["This window's title bar, its text and its buttons."],
})
```

  `settings/Bars.lua`:

```lua

-- The Bars entry of the Windows page (MultiMeters#55).
NS.RegisterWindowSection(PAGE, L["Bars"], {
    tooltip = L["How this window's bars, their text and their icons look."],
})
```

  `settings/Tooltip.lua`:

```lua

-- The Tooltip entry of the Windows page (MultiMeters#55).
NS.RegisterWindowSection(PAGE, L["Tooltip"], {
    tooltip = L["What this window's tooltip shows, and how it looks."],
})
```

  `settings/Visibility.lua`:

```lua

-- The Visibility entry of the Windows page (MultiMeters#55).
NS.RegisterWindowSection(PAGE, L["Visibility"], {
    tooltip = L["Where and when this window is shown."],
})
```

- [ ] **Step 9: The locale.** In `locales/enUS.lua`, after
  `L["The last window cannot be deleted."] = "The last window cannot be deleted."` (the end of the
  "Windows page" block), add:

```lua
L["Source window"] = "Source window"
L["General has no settings to restore. The window's name is kept."] =
    "General has no settings to restore. The window's name is kept."
L["Restore the active window's settings in the section on screen to their shipped values. On Columns that includes the shipped column list. General has nothing to restore: the window's name is kept."] =
    "Restore the active window's settings in the section on screen to their shipped values. On Columns that includes the shipped column list. General has nothing to restore: the window's name is kept."
-- The Windows page's rail (MultiMeters#55): one tooltip per entry.
L["Rename, create, duplicate or delete windows, and copy settings from another window."] =
    "Rename, create, duplicate or delete windows, and copy settings from another window."
L["This window's size, position, background, border and rows."] =
    "This window's size, position, background, border and rows."
L["This window's title bar, its text and its buttons."] = "This window's title bar, its text and its buttons."
L["How this window's bars, their text and their icons look."] =
    "How this window's bars, their text and their icons look."
L["What this window's tooltip shows, and how it looks."] = "What this window's tooltip shows, and how it looks."
L["Where and when this window is shown."] = "Where and when this window is shown."
L["Which statistics this window shows, in what order, and how the column headers look."] =
    "Which statistics this window shows, in what order, and how the column headers look."
```

  `crlf` every file edited in Steps 3-9.

- [ ] **Step 10: The existing cases the Windows page changes.**
  - `tests/test_options_panel.lua`, case "Options: a page that declines a Defaults button never grows
    one": replace the two comment lines `-- The Profiles page's rows are user data, and the Windows
    page's are the registry -- restoring` / `-- either would delete something the player made rather
    than reset a preference.` with
    `-- The Profiles page's rows are user data: restoring them would delete something the player made` /
    `-- rather than reset a preference. The Windows page offers Defaults since MultiMeters#55 (the` /
    `-- active entry's rows for the active window; tests/test_windows_rail.lua).`
    Then change `    for _, key in ipairs({ "profiles", "windows" }) do` to
    `    for _, key in ipairs({ "profiles" }) do`.
  - Same file, `TABBED`: `    windows    = "Window",` becomes `    windows    = "General",`. A one-tab
    strip still passes the `#(ctx.__tabKids or {}) >= 2` check, because the strip's ledger also holds
    its content panel (`libs/LibKa0s/OptionsTabs.lua:576`).
  - `tests/test_degraded.lua`, case "Degraded: the namespace publishes the same seam members with and
    without the library": change `"CreateOptionsPanel", "OpenOptionsPanel" }) do` to
    `"CreateOptionsPanel", "OpenOptionsPanel",` followed by a new line
    `                            "RegisterWindowSection", "WindowSection" }) do`.
  - `crlf` both files.

- [ ] **Step 11: Run and see them pass.**

```sh
/home/tushar/.claude/wow-addon/bin/ka0s-bounded lua tests/run.lua > /tmp/MultiMeters-run.txt 2>&1
grep -E '^  (FAIL|PASS)  Windows rail:' /tmp/MultiMeters-run.txt; grep -c '^  FAIL' /tmp/MultiMeters-run.txt
```

  Expected: all ten `Windows rail:` cases `PASS`, and 0 `FAIL` overall. If a page case reports "drew
  no rail", grep the run for the library's `RENDER_FAILED` line. It names the raise inside
  `Helpers.RenderWindowPage`.

- [ ] **Step 12: The doc.** In `docs/settings-panel.md`:
  1. Replace the page table's row 2 (the line starting `| 2 | Windows |`) with:

```markdown
| 2 | Windows | `windows` | 1 (`window.name`) | 1 — **General**, the rail's first entry; every other entry keeps its own strip ([The Windows page](#the-windows-page-band-rail-entry)) | yes — the active entry's rows, for the active window | yes | One page per window (MultiMeters#55): the Active window band, a nav rail, and the selected entry's own strip. **General** holds the name box, New / Duplicate / Delete, and a *Copy settings from* block (the source window, the group filter and Copy). Bespoke rather than schema rows, so its one tab is drawn directly with `H.TabStrip`. |
```

  2. Insert this section, as its own lines, immediately above the heading `## The tab strip and the
     banner`:

```markdown
## The Windows page: band, rail, entry

The Windows page is **one page per window** (MultiMeters#55, `options-ui-§13` and `options-ui-§14`).
It has three pinned pieces, drawn in the library's order on every full render: `PageBanner`,
`NavRail`, `TabStrip`.

- **The band** is `H.WindowBanner` (`settings/Windows.lua`), the Active window picker. It is the
  page's only picker, full width above the rail and the strip. It writes `NS.State.activeWindowId`
  through `NS.State.SetActiveWindow` and forces a structural refresh.
- **The rail** (LibKa0s `O.NavRail`, 120 wide) lists the page's **entries**: General · Frame ·
  Header · Bars · Tooltip · Visibility · Columns. The order is `SECTION_ORDER`
  (`settings/OptionsSetup.lua`), not the TOC's. An entry **is** a page key (`windows`, `frame`,
  `header`, `bars`, `tooltip`, `visibility`, `columns`). Its schema rows keep `page`, their
  window-relative paths and their defaults, so `/mm get`, `/mm set`, `/mm list`, profiles and the
  resets never see the rail. Each file registers its entry at load with
  `NS.RegisterWindowSection(key, label, spec)`. The registry sits above the library fork, so a
  library-absent load knows the entries too.
- **The strip** is the entry's own. Frame, Header, Bars, Tooltip and Visibility use
  `H.RenderTabbedSchema(ctx, key)`. General (one **General** tab) and Columns (Columns, Header text,
  Header background) draw their bespoke strips through the entry's `spec.render`.

`Helpers.RenderWindowPage` draws the page. Its **first** statement is `NS.CancelReorder(ctx)`. The
seven entries share one ctx, and a rail click, a window switch and Columns' own tab click all
re-render the page. A live drag handle must be released before `ClearScroll` hands the Columns
containers back to AceGUI's pool (see [Column editing](#column-editing)).

**Session state, never persisted.** `ctx.activeSection` is the entry on screen, and
`ctx.sectionTabs[entry]` holds each entry's tab. The tab is stashed **before anything moves the
entry**, because the library's own strip click never calls back into the host. So Frame -> Size and
position, then Bars, then Frame again lands on Size and position. Picking another window in the band
keeps the entry and its tab (`options-ui-§14`: the rail is not a picker).

**Defaults** reads the entry **at click time** (`Helpers.RestoreActiveSection`), because the library
captures the handler once, at the first show:

| Entry | What Defaults restores |
|---|---|
| Frame, Header, Bars, Tooltip, Visibility | The entry's rows (`H.RestoreDefaults(entry, ctx)`), for the **active window** only, because the rows are window-relative. |
| Columns | The shipped column list **and** the `window.columnHeader.*` rows, in one bulk bracket, so the press logs one `[Set] reset columns: N rows` line. |
| General | Nothing. Its one schema row is the window's name, which a reset would overwrite. It prints *General has no settings to restore. The window's name is kept.* |

The button carries one tooltip that fits every entry. `tests/test_windows_rail.lua` pins all of it.
```

  `crlf docs/settings-panel.md`.

- [ ] **Step 13: Gate, inventory, badge.** Run the addon gate and lizard. Expected: 0 FAIL, luacheck
  0/0, no lizard output. Then regenerate `docs/test-cases.md` and set the README Tests badge (the M2
  rules above). The run has ten more cases than NR-MM-01's (2088).

- [ ] **Step 14: Commit.**

```sh
git add settings/OptionsSetup.lua settings/Windows.lua settings/Columns.lua settings/Frame.lua settings/Header.lua \
  settings/Bars.lua settings/Tooltip.lua settings/Visibility.lua locales/enUS.lua tests/test_windows_rail.lua \
  tests/run.lua tests/test_options_panel.lua tests/test_degraded.lua docs/settings-panel.md docs/test-cases.md README.md
git status --porcelain                  # expect empty
git commit -m "NR-MM-02: The Windows page draws a nav rail: one page per window" \
  -m "MultiMeters#55. A section registry above the fork (NS.RegisterWindowSection / NS.WindowSection, SECTION_ORDER) names the Windows page's seven entries, each a former page key, so no schema row moves. Helpers.RenderWindowPage cancels any column drag first, then draws the Active window band, the rail (LibKa0s v1.61.0 O.NavRail) and the entry's own strip, keeping each entry's tab across rail clicks, strip clicks and window switches. General is one General tab holding the window acts and the folded-in Copy settings from block. The page gains Defaults, read at click time: the active entry's rows for the active window, Columns' list and header rows together, and nothing on General (the window's name is kept). The six sub-pages still register; NR-MM-04 retires them." \
  -m "$TRAILERS"
```

### Task NR-MM-03: deep links into the Windows page

**Files:**
- Modify: `settings/OptionsSetup.lua`: the live `NS.RegisterOptionsPage` (:518) captures each page's
  category; the Windows-page block gains `Helpers.SelectSection`, the `SelectTab` route and
  `NS.OpenOptionsPage`; the stub gains `"SelectSection"` and `NS.OpenOptionsPage`.
- Modify: `tests/test_windows_rail.lua` (four cases appended), `tests/test_degraded.lua` (the
  namespace-parity list gains `"OpenOptionsPage"`).
- Modify: `docs/settings-panel.md` (a **Deep links** paragraph in the Windows-page section).
  Regenerated: `docs/test-cases.md`, the README badge.

**Interfaces:**
- Produces: `NS.OpenOptionsPage(pageKey)` on both arms (degraded: the one "unavailable" line),
  `Helpers.SelectSection(key, tabKey) -> boolean` (live; stub no-op), and a `Helpers.SelectTab` that
  routes entry keys to `SelectSection` and anything else to the library.
- Consumes: `Helpers.__combatRefused` (the library's combat refusal; one notice per combat) and
  `lib.__IsCombatLocked`.
- Callers: none in the addon today (02_SPEC R3). The seam is for links, the suite, and the follow-up
  that may point the header gear at Windows.

- [ ] **Step 1: Write the failing tests.** Append to `tests/test_windows_rail.lua`:

```lua

-- ── deep links, SelectTab (NR-MM-03) ────────────────────────────────────────────────────────

--- A fresh page whose subcategories answer GetID, as the client's do, recording by tree label the
--- category every OpenToCategory lands on.
local function recordingOpens()
    local byId, opened, count = {}, {}, 0
    local P = env{ mutate = function(mocks)
        local register = mocks.Settings.RegisterCanvasLayoutSubcategory
        mocks.Settings.RegisterCanvasLayoutSubcategory = function(parent, panel, name)
            local cat = register(parent, panel, name) or {}
            count = count + 1
            local id = 100 + count
            byId[id] = name
            cat.GetID = function() return id end
            return cat
        end
        mocks.Settings.OpenToCategory = function(id) opened[#opened + 1] = byId[id] or "main" end
    end }
    return P, opened
end

-- Review Focus 5's MultiMeters half.
test("Windows rail: a former sub-page key opens Windows on that entry, drawn on its next show", function()
    local P, opened = recordingOpens()
    local ctx = P.show()
    P.rail("frame")
    ctx.panel:Hide()                                -- the settings window is closed
    P.NS.OpenOptionsPage("bars")
    -- red under: OpenOptionsPage looking the key up in the category table alone (the Bars sub-page
    -- today, nothing once it retires)
    assertEqual(opened[#opened], P.L["Windows"])
    assertEqual(ctx.activeSection, "bars", "selected before the show")
    ctx.panel:Show()
    assertEqual(P.railValue(), "bars", "and drawn on it")
    P.NS.OpenOptionsPage("windows")
    -- red under: the page's own key dropping the player back on General
    assertEqual(opened[#opened], P.L["Windows"])
    assertEqual(ctx.activeSection, "bars", "Windows keeps the entry the player left")
    P.NS.OpenOptionsPage("general")
    assertEqual(opened[#opened], P.L["General"], "any other key opens its own page")
end)

test("Windows rail: SelectTab on an entry key selects the entry and its tab; the addon page stays the library's", function()
    local P = env()
    local ctx = P.show()
    local L, H = P.L, P.NS.Helpers
    -- red under: the call reaching the library's SelectTab, which moves the page's one scalar tab
    -- (or finds no page once the sub-pages retire)
    assertTrue(H.SelectTab("tooltip", L["Contents"]))
    assertEqual(ctx.activeSection, "tooltip")
    assertEqual(ctx.activeTab, L["Contents"])
    assertTrue(H.SelectTab("general", L["Behavior"]), "the addon page is the library's")
    assertEqual(H.__panelFor("general").activeTab, L["Behavior"])
end)

test("Windows rail: selecting an entry is refused in combat and moves nothing", function()
    local P = env()
    local ctx = P.show()
    P.inst.mocks.setRestricted(true)
    -- red under: SelectSection without the library's refusal (a structural render in combat)
    local ok = P.NS.Helpers.SelectSection("header")
    P.inst.mocks.setRestricted(false)
    assertFalse(ok)
    assertEqual(ctx.activeSection, "windows")
end)

test("Windows rail: OpenOptionsPage in combat opens nothing and selects nothing", function()
    local P, opened = recordingOpens()
    local ctx = P.show()
    P.inst.mocks.setRestricted(true)
    P.NS.OpenOptionsPage("columns")
    P.inst.mocks.setRestricted(false)
    -- red under: selecting the entry before asking whether the open is allowed
    assertEqual(#opened, 0, "a category switch is protected: refused, never deferred")
    assertEqual(ctx.activeSection, "windows")
end)
```

  In `tests/test_degraded.lua`'s namespace-parity list, change `"RegisterWindowSection",
  "WindowSection" }) do` to `"RegisterWindowSection", "WindowSection", "OpenOptionsPage" }) do`.
  Then `crlf` both files.

- [ ] **Step 2: Run and see them fail.**

```sh
/home/tushar/.claude/wow-addon/bin/ka0s-bounded lua tests/run.lua > /tmp/MultiMeters-run.txt 2>&1
grep -E '^  FAIL' /tmp/MultiMeters-run.txt
```

  Expected: the four new `Windows rail:` cases `FAIL`, since `NS.OpenOptionsPage` and
  `Helpers.SelectSection` are nil and `SelectTab("tooltip", …)` reaches the Tooltip sub-page. The
  degraded namespace case also fails, on `OpenOptionsPage`.

- [ ] **Step 3: Capture each page's category.** Replace the live
  `NS.RegisterOptionsPage = function(key, name, builder) Helpers.RegisterOptionsPage(key, name, builder) end`
  with:

```lua
-- Every page's Blizzard category, by page key. The library's registry drops the
-- builder's return value, and Settings.OpenToCategory takes the category's id --
-- so NS.OpenOptionsPage (below) has no other way to send the player to one page.
-- Captured here rather than in the builders, so a page added later gets it free.
local categories = {}

NS.RegisterOptionsPage = function(key, name, builder)
    Helpers.RegisterOptionsPage(key, name, function(mainCategory)
        local cat = builder(mainCategory)
        if cat then categories[key] = cat end
        return cat
    end)
end
```

- [ ] **Step 4: SelectSection, the SelectTab route, OpenOptionsPage.** Append at the end of
  `settings/OptionsSetup.lua` (after `Helpers.RestoreActiveSection`):

```lua

--- Select entry `key` on the Windows page, and optionally its tab: the one seam a
--- link, a deep link or a suite moves the entry through. A hidden page is marked
--- owed a render and draws the entry on its next show. Refused in combat, as a tab
--- switch is (options-ui-§2, §13).
--- @return boolean  whether the entry was selected
function Helpers.SelectSection(key, tabKey)
    if Helpers.__combatRefused() then return false end
    local ctx = windowsCtx
    if not (ctx and sections[key]) then return false end
    stashTab(ctx)
    ctx.activeSection = key
    if tabKey ~= nil then ctx.sectionTabs[key] = tabKey end
    Helpers.RefreshPanel(ctx, true)
    return true
end

-- The library's SelectTab moves one PAGE's tab. An entry key is no page of its own
-- (MultiMeters#55): it routes to SelectSection, so a link written against a page
-- key still lands. Any other key -- General, Profiles -- is the library's.
local selectTab = Helpers.SelectTab
function Helpers.SelectTab(pageKey, tabKey)
    if sections[pageKey] then return Helpers.SelectSection(pageKey, tabKey) end
    return selectTab(pageKey, tabKey)
end

--- Open the settings window at one page. An entry key opens the Windows page on
--- that entry; "windows" itself keeps the entry the player left. Under combat
--- lockdown the library's own open answers -- it refuses with its one line and
--- never defers (options-ui-§2) -- and nothing is selected.
function NS.OpenOptionsPage(pageKey)
    local target = sections[pageKey] and GENERAL_SECTION or pageKey
    local cat = categories[target]
    if lib.__IsCombatLocked() or not (cat and cat.GetID and Settings and Settings.OpenToCategory) then
        return Helpers.OpenOptionsPanel()
    end
    if pageKey ~= target then Helpers.SelectSection(pageKey) end
    Settings.OpenToCategory(cat:GetID())
end
```

- [ ] **Step 5: The stub.** Add `"SelectSection",` to the no-op names line NR-MM-02 added
  (`"RenderWindowPage", "RestoreActiveSection", "__bindWindowsPage", "SelectSection",`). Below the
  stub's `    NS.OpenOptionsPanel = NS.CreateOptionsPanel`, add:

```lua
    -- And the page-targeted open (MultiMeters#55): the same honest line, because
    -- there is no page to open either.
    NS.OpenOptionsPage = NS.CreateOptionsPanel
```

  `crlf settings/OptionsSetup.lua`.

- [ ] **Step 6: Run and see them pass.** Rerun the grep from Step 2. Expected: 0 `FAIL`, and all
  fourteen `Windows rail:` cases `PASS`.

- [ ] **Step 7: The doc.** In `docs/settings-panel.md`, append this paragraph to the end of "The
  Windows page: band, rail, entry" (after "…pins all of it."):

```markdown
**Deep links.** `NS.OpenOptionsPage(key)` opens the settings window at one page. A former sub-page
key (`frame`, `bars`, …) opens Windows **on that entry**, and `windows` itself keeps the entry the
player left. `Helpers.SelectSection(key, tab)` is the one seam that moves the entry, and the host's
`Helpers.SelectTab` routes an entry key to it, so a link written against a page key still lands. A
hidden page is marked owed a render and draws the entry on its next show. Both refuse under combat,
through the library's refusal. Each page's Blizzard category is captured by the
`NS.RegisterOptionsPage` wrapper, because the library's registry drops the builder's return value.
Nothing in the addon calls `OpenOptionsPage` yet: the header gear still opens the main panel.
```

  `crlf docs/settings-panel.md`.

- [ ] **Step 8: Gate, inventory, badge.** Addon gate and lizard: 0 FAIL, 0/0, no lizard output.
  Regenerate `docs/test-cases.md` and set the badge (2092 cases).

- [ ] **Step 9: Commit.**

```sh
git add settings/OptionsSetup.lua tests/test_windows_rail.lua tests/test_degraded.lua docs/settings-panel.md docs/test-cases.md README.md
git status --porcelain                  # expect empty
git commit -m "NR-MM-03: Deep links open the Windows page on an entry" \
  -m "MultiMeters#55. NS.OpenOptionsPage(key) is new: a former sub-page key opens Windows on that entry, 'windows' keeps the entry the player left, and any other key opens its own page; each page's category is captured by the RegisterOptionsPage wrapper. Helpers.SelectSection is the one seam that moves the entry (refused in combat, and drawn on the next show of a hidden page), and Helpers.SelectTab routes entry keys to it. The stub answers both. No caller changes: the header gear still opens the main panel." \
  -m "$TRAILERS"
```

### Task NR-MM-04: retire the six window sub-pages

**Files:**
- Modify: `settings/Frame.lua`, `Header.lua`, `Bars.lua`, `Tooltip.lua`, `Visibility.lua`: each
  keeps its header rationale and its entry registration, and loses its builder and page
  registration.
- Modify: `settings/Columns.lua`: `render`, `Build` and the page registration go; `renderSection`,
  `restoreDefaults` and the entry registration stay.
- Modify: `settings/OptionsSetup.lua`: the nesting-mark block and `NS.SubPageLabel` go (:52-106 at
  planning time).
- Modify: `settings/Windows.lua`: the band tooltip and `H.WindowBanner`'s comment.
- Modify (wording, 02_SPEC R15): `locales/enUS.lua`, `settings/Schema.lua:493`,
  `settings/Schema_Paths.lua:645`, `settings/Schema_Compose.lua:737,741,757`,
  `settings/General.lua:237`.
- Modify: `MultiMeters.toc` (a Conventional note above `settings\Frame.lua`).
- Modify tests: `tests/test_options_panel.lua`, `tests/test_columns.lua`,
  `tests/test_schema_paths.lua:509`, `tests/test_surface_parity.lua:104-108` (comment).
- Modify docs: `docs/settings-panel.md`, `docs/common-tasks.md`, `docs/module-map.md`,
  `docs/ARCHITECTURE.md:340`, `README.md:85`, `docs/schema.md:1451`, `docs/smoke-tests.md`. Regenerated:
  `docs/test-cases.md`, the README badge.

**Interfaces:** no new ones. After this task, `Helpers.__panelFor` knows `general`, `windows` and
`profiles` only, and `T.mocks.__subcategories` holds three names.

- [ ] **Step 1: Rewrite the tests first.** In `tests/test_options_panel.lua`:
  1. `PAGES` becomes `local PAGES = { "general", "windows", "profiles" }`, and its comment's last
     sentence becomes "The order here is the TOC's registration order, which is the order the tree
     draws; the six window pages are entries of Windows since MultiMeters#55." `PANEL_NAME` keeps only
     its `windows`, `general` and `profiles` rows.
  2. Below `showPage`, add:

```lua
--- Show the Windows page on one of its entries (MultiMeters#55): the six window pages are entries of
--- it now, so a case that drove a sub-page drives its entry.
local function showSection(inst, key)
    local ctx = showPage(inst, "windows")
    assertTrue(inst.NS.Helpers.SelectSection(key), "the Windows page lists no entry " .. key)
    assertEqual(ctx.activeSection, key)
    return ctx
end
```

  3. Delete the cases "Options: every window page is marked as nested, and the two that are not are
     not" and "Options: the page HEADING keeps the plain name, mark or no mark". In their place, add:

```lua
test("Options: the tree is General, Windows, Profiles, with no nesting mark", function()
    -- MultiMeters#55: the six window pages are entries of the Windows page, so nothing is nested and
    -- the D6 mark ("  - ") went with them.
    -- red under: a window page still registering a Blizzard category of its own.
    local names = {}
    for name in pairs(T.mocks.__subcategories) do names[#names + 1] = name end
    table.sort(names)
    local want = { NS.L["General"], NS.L["Windows"], NS.L["Profiles"] }
    table.sort(want)
    assertEqual(table.concat(names, "|"), table.concat(want, "|"))
end)
```

  4. In "Options: a widget's set() routes through NS.SetByPath", replace

```lua
    local inst = T.load()
    local ctx = panelFor(inst, "frame")
    ctx.panel:Hide()
    ctx.panel:Show()
```

     with

```lua
    local inst = T.load()
    local ctx = showSection(inst, "frame")
```

  5. In "Options: a checkbox's set() routes through NS.SetByPath too", replace

```lua
    local ctx = panelFor(inst, "header")
    local before = #aceGUI(inst).__created
    ctx.panel:Hide()
    ctx.panel:Show()
```

     with

```lua
    showPage(inst, "windows")
    local before = #aceGUI(inst).__created
    assertTrue(inst.NS.Helpers.SelectSection("header"), "the Windows page lists no Header entry")
```

  6. Then these replacements across the whole file, in this order:

```sh
F=tests/test_options_panel.lua
perl -pi -e 's/showPage\(inst, "(frame|columns|bars)"\)/showSection(inst, "$1")/g' $F
perl -pi -e 's/panelFor\(inst, "frame"\)/panelFor(inst, "windows")/g' $F
perl -pi -e 's/"the Frame page asks for a Defaults button"/"the Windows page asks for a Defaults button"/' $F
perl -pi -e 's/^(\s+)local ctx = showPage\(inst, page\)/${1}local ctx = page == "general" and showPage(inst, page) or showSection(inst, page)/' $F
perl -pi -e 's/^(\s+)local ctx = showPage\(inst, key\)(\r?)$/${1}local ctx = key == "profiles" and showPage(inst, key) or (key == "general" and showPage(inst, key) or showSection(inst, key))$2/' $F
crlf $F
grep -nE '(showPage|panelFor)\((inst|T), "(frame|header|bars|tooltip|visibility|columns)"\)' $F   # expect no output
```

     The two loop lines cover `TABBED`, the banner case's `SUBPAGES` loop (it keeps its final
     `showPage(inst, "windows")`, which is the General entry), the Defaults-log loop, and the
     "declines" loop (`profiles`).
  7. In "Panel: every window sub-page banners the active window, and Windows has no second picker",
     rename the local `SUBPAGES` to `ENTRIES`, and rename the case to "Panel: every Windows entry sits
     under the Active window band, and General has no second picker".

  In `tests/test_columns.lua`: `local PANEL = "MultiMetersColumnsPanel"` becomes
  `local PANEL = "MultiMetersWindowsPanel"`. In `openPage`, replace

```lua
    assertTrue(ctx ~= nil, "the Columns page did not register a panel")

    ctx.panel:Hide()
    ctx.panel:Show()
    assertTrue(ctx._rendered, "the Columns page did not render; the renderer raised "
        .. "and was swallowed by pcall")
```

  with

```lua
    assertTrue(ctx ~= nil, "the Windows page did not register a panel")

    ctx.panel:Hide()
    ctx.panel:Show()
    -- The editor is the Windows page's Columns entry (MultiMeters#55).
    assertTrue(inst.NS.Helpers.SelectSection("columns"), "the Windows page lists no Columns entry")
    assertEqual(ctx.activeSection, "columns")
    assertTrue(ctx._rendered, "the Windows page did not render; the renderer raised "
        .. "and was swallowed by pcall")
```

  In `tests/test_schema_paths.lua`, change `err:find("Columns page", 1, true)` to
  `err:find("Windows > Columns", 1, true)`. In `tests/test_surface_parity.lua`, replace the sentence
  "The window pages draw their own banner (`Helpers.WindowBanner`, decorated by settings/Frame.lua and
  carried by the stub)" with "The Windows page draws its own band (`Helpers.WindowBanner`, decorated by
  settings/Windows.lua and carried by the stub)". `crlf` the four test files.

- [ ] **Step 2: Run and see what fails.**

```sh
/home/tushar/.claude/wow-addon/bin/ka0s-bounded lua tests/run.lua > /tmp/MultiMeters-run.txt 2>&1
grep -E '^  FAIL' /tmp/MultiMeters-run.txt
```

  Expected: "the tree is General, Windows, Profiles" fails (nine names today), and so do
  "subcategory registered eagerly" and "ctx carries its page key" (nine pages registered, three
  expected). `tests/test_schema_paths.lua`'s column-refusal case fails on the old wording (Step 5
  rewords it). The rest pass, because the entries already draw. The statistic-colors case keeps
  passing until Step 5 rewords the key and its literal together.

- [ ] **Step 3: The five schema entries lose their builders.** For each, keep the file's header
  comment, then end the file with the entry registration. Replace everything from the line
  `local PAGE = "<key>"` to the end of the file:

```sh
for spec in "Frame:frame:Frame:This window's size, position, background, border and rows." \
            "Header:header:Header:This window's title bar, its text and its buttons." \
            "Bars:bars:Bars:How this window's bars, their text and their icons look." \
            "Tooltip:tooltip:Tooltip:What this window's tooltip shows, and how it looks." \
            "Visibility:visibility:Visibility:Where and when this window is shown."; do
  IFS=: read f key label tip <<< "$spec"
  KEY=$key LABEL=$label TIP=$tip perl -0pi -e '
    my ($k, $l, $t) = @ENV{qw(KEY LABEL TIP)};
    s/\r?\nlocal PAGE = "\Q$k\E".*\z/\r\n-- The ${l} entry of the Windows page (MultiMeters#55). Its rows are drawn by the page\x27s\r\n-- renderer (settings\/OptionsSetup.lua, Helpers.RenderWindowPage) through\r\n-- H.RenderTabbedSchema(ctx, "$k"): the entry\x27s tabs are the rows\x27 groups.\r\nNS.RegisterWindowSection("$k", L["$l"], {\r\n    tooltip = L["$t"],\r\n})\r\n/s' settings/$f.lua
  crlf settings/$f.lua
  tail -8 settings/$f.lua
done
```

  Then fix each header's first description line, which still names a page:
  - `settings/Frame.lua:3`: `-- The Frame page: the standalone window's own geometry, chrome and lock state.`
    becomes `-- The Windows page's Frame entry: the window's own geometry, chrome and lock state.`
    Delete its paragraph starting `-- WHY THE BODY IS LAZY:` (through `-- marked it dirty while it was
    hidden.`), because the entry has no body of its own now.
  - `settings/Header.lua:3`: `-- The Header page:` becomes `-- The Windows page's Header entry:`, and
    `so this` / `-- file is the registration and the lazy body and nothing else;` becomes `so this` /
    `-- file is the entry's registration and nothing else;`.
  - `settings/Bars.lua:3`: `-- The Bars page —` becomes `-- The Windows page's Bars entry —`.
  - `settings/Tooltip.lua:3`: `-- The Tooltip page:` becomes `-- The Windows page's Tooltip entry:`.
  - `settings/Visibility.lua:3`: `-- The Visibility page:` becomes `-- The Windows page's Visibility entry:`.

  `crlf` all five, then confirm none still references a page mechanic:

```sh
grep -nE 'SubPageLabel|CreatePanel|SetRenderer|RegisterOptionsPage|WindowBanner' settings/Frame.lua settings/Header.lua settings/Bars.lua settings/Tooltip.lua settings/Visibility.lua   # expect no output
```

- [ ] **Step 4: Columns and the nesting mark.**
  - `settings/Columns.lua`: delete `local function render(ctx)` (the sub-page renderer), `local
    function Build(mainCategory)` and the final `if NS.RegisterOptionsPage then … end` block. In
    `renderSection`'s docstring, replace "-- and, until the Columns sub-page retires, under the band by
    that page's own renderer below. The reorder cancel and the scroll clear are the CALLER's, in that
    order; both callers cancel first." with "The reorder cancel and the scroll clear are the
    renderer's, in that order." In the Columns header comment, "The Columns page" becomes "The Windows
    page's Columns entry".
  - `locales/enUS.lua`: delete the key `"Restore the statistics this window ships with, ticked and in
    their shipped order, and the header text and background settings on this page to their shipped
    values."` (both lines). Its only caller was the deleted `Build`.
  - `settings/OptionsSetup.lua`: delete the whole nesting-mark block. It runs from its opening rule
    line (`-- -----…` above `-- The nesting mark`) through the `end` of `function NS.SubPageLabel(name)`.
    Nothing may call `SubPageLabel` afterwards:

```sh
grep -rn 'SubPageLabel\|SUBPAGE_MARK' settings core modules tests   # expect no output
```

- [ ] **Step 5: Wording that names a retired page** (02_SPEC R15). The keys are the English strings,
  so each replacement runs over the locale, its callers and the tests that pin it:

```sh
FILES=(locales/enUS.lua settings/Windows.lua settings/Schema.lua settings/Schema_Paths.lua settings/Schema_Compose.lua settings/General.lua tests/test_options_panel.lua)
perl -pi -e '
  s/Which window the settings on every other page apply to\./Which window every section of this page applies to./g;
  s/edit columns on the Columns page\./edit columns under Windows > Columns./g;
  s/has its own, on the Columns page\./has its own, under Windows > Columns./g;
  s/own Scale on the Frame page\./own Scale under Windows > Frame./g;
  s/own Opacity on the Frame page\./own Opacity under Windows > Frame./g;
  s/\(Frame page, or the lock button in its header\)/(Windows > Frame, or the lock button in its header)/g;
  s/its background \(Bars\), the numbers on it \(Bars > Text style\), and the column header strip \(Columns\)/its background (Windows > Bars), the numbers on it (Windows > Bars > Text style), and the column header strip (Windows > Columns)/g;
' $FILES
crlf $FILES
grep -rnE 'on the (Columns|Frame) page\.|every other page apply|\(Bars\), the numbers' locales settings tests   # expect no output
```

  In `settings/Windows.lua`, `H.WindowBanner`'s docstring sentence "Decorated onto the instance rather
  than kept file-local because SEVEN pages draw it, and a second copy is how two of them end up
  disagreeing about what the list contains." becomes "Decorated onto the instance, and drawn once, as
  the Windows page's band above its rail (MultiMeters#55): the one picker, so the entries cannot
  disagree about which window they edit." The first header paragraph's "WHY THIS PAGE EXISTS AT ALL"
  section keeps its reasoning; replace its sentence "That makes every other settings page ambiguous
  on its own" with "That makes every entry of this page ambiguous on its own".

- [ ] **Step 6: The TOC note.** In `MultiMeters.toc`, insert immediately above `settings\Frame.lua`:

```
# Conventional position: the Windows page's entries (MultiMeters#55) -- Frame, Header, Bars,
# Tooltip, Visibility and Columns -- each registering its entry at load. The rail's order is
# settings/OptionsSetup.lua's SECTION_ORDER, not this one.
```

  `crlf MultiMeters.toc`.

- [ ] **Step 7: Run and see it pass.** Rerun Step 2's commands. Expected: 0 `FAIL`. Then check that
  nothing still reaches a retired page:

```sh
grep -rnE '__panelFor\("(frame|header|bars|tooltip|visibility|columns)"\)|MultiMeters(Frame|Header|Bars|Tooltip|Visibility|Columns)Panel' settings core modules tests   # expect no output
```

- [ ] **Step 8: Docs.** Each edit is in the named file. Insert rows as their own lines, and `git diff`
  each table.
  - `docs/settings-panel.md`:
    1. The page table keeps rows 1 (General), 2 (Windows, from NR-MM-02) and 9 (Profiles, renumbered
       3). Rows 3-8 move into a new table directly under it, headed `### The Windows page's entries`,
       with columns `| Entry | Key | Schema rows | Tabs | What is on it |`. The first row is
       `| General | \`windows\` | 1 (\`window.name\`) | 1 — **General** | The window acts and Copy
       settings from; see row 2 above. |`. Then one row per old row 3-8, keeping each row's Schema
       rows, Tabs and "What is on it" text, with the page name written without the `  - ` prefix. In
       Columns' row, drop the sentence about the `Defaults` column.
    2. "**169 schema rows total.** Five of the nine pages" becomes "**169 schema rows total.** Five of
       the Windows page's seven entries". "Three pages are not schema-driven bodies" becomes "Three
       surfaces are not schema-driven bodies", and its first bullet begins "**The General entry** and
       **Columns**' block editor".
    3. Delete the section "The indent, and why the tree needs one" (heading through the line before
       the next `## ` heading).
    4. In "The two pages with no Defaults button": the heading becomes "The page with no Defaults
       button". The Windows paragraph is replaced by one sentence: "The Windows page has Defaults
       since MultiMeters#55. It restores the active entry's rows, for the active window; see [The
       Windows page](#the-windows-page-band-rail-entry)."
    5. In "The window picker": every "seven pages"/"the seven" becomes "the Windows page's seven
       entries", and "on every other page" becomes "on every entry". Delete the sentence about the
       Windows page having no second picker because the other pages draw the banner. Replace it with:
       "The band is drawn once, above the rail: every entry edits the window it names."
  - `docs/common-tasks.md`, "Add a settings page" (:412-499): rename it to "Add a settings page (an
    addon-wide one)", and cut its window-page steps (the `NS.SubPageLabel` template at :446 and the
    `H.WindowBanner` calls at :442 and :480). Add a sibling section directly after it:

```markdown
## Add an entry to the Windows page

An entry is a page key whose rows are about one window (`window.*` paths).

1. Declare the rows in `settings/Schema.lua` with `page = "<key>"` and a `group` each. The groups
   become the entry's tabs, in declaration order.
2. Create `settings/<Entry>.lua` and register the entry at file load:
   `NS.RegisterWindowSection("<key>", L["<Label>"], { tooltip = L["<what the entry holds>"] })`.
   A bespoke entry also passes `render = fn(ctx)` (it draws its own strip and body under the band and
   the rail) and, if its Defaults is not the row walk, `defaults = fn(ctx)`.
3. Add `settings\<Entry>.lua` to `MultiMeters.toc` below `settings\Windows.lua`, and the key to
   `SECTION_ORDER` in `settings/OptionsSetup.lua`, where the rail should list it.
4. Add the rail tooltip and the label to `locales/enUS.lua`, and a case to
   `tests/test_windows_rail.lua`'s registry list.
```

  Also update `:117` and `:468`, which name the sub-pages, to name the entries.
  - `docs/module-map.md`: in the tree block (:240-250), "the 9 panel pages" becomes "the 3 panel pages
    (General, Windows, Profiles) and the Windows page's 7 entries", and the `  - ` indents go. In the
    settings table (:330-350), the rows for Frame/Header/Bars/Tooltip/Visibility/Columns.lua say
    "Windows-page entry: registers `<key>`" instead of "page", and `Windows.lua`'s row adds "the band,
    the General entry". `OptionsSetup.lua`'s row adds "the Windows page's entry registry,
    `RenderWindowPage`, `SelectSection`, `OpenOptionsPage`".
  - `docs/ARCHITECTURE.md:340`: "The nine pages" becomes "The three pages (the Windows page carries
    seven entries on a nav rail)".
  - `README.md:85` ("on the Windows page") stays true. Every README line that names Frame, Header,
    Bars, Tooltip, Visibility or Columns **as a page** becomes "Windows > <Entry>":

```sh
grep -nE '(Frame|Header|Bars|Tooltip|Visibility|Columns) page' README.md docs/*.md
```

    Rewrite each hit that is about the settings tree, and run the README changes through the
    `humanize` skill before committing.
  - `docs/schema.md:1451`: the sentence naming the page a row renders on says "the Windows page's
    <Entry> entry".
  - `docs/smoke-tests.md`:
    1. :173-178, the indent check: replace it with "The tree reads General · Windows · Profiles.
       There are no nested entries."
    2. §4 Settings panel sweep: "nine pages" becomes "three pages", and "the seven" becomes "the
       Windows page's seven entries". The page-shape checks (:380-411) name entries, not pages. The
       sub-page combat cover (:555-557) becomes the Windows page's, rail included.
    3. §5 Column editor (:566-655): "open the Columns page" becomes "open Windows > Columns".
    4. §6 Multi-window (:656-693): "Copy settings from" is under Windows > General.
    5. :1139 and :1257-1263 name entries.
    6. Append `### 36. The Windows page (MultiMeters#55)`, with a sentence saying the owner fills
       Result, and the table of MM-S1 … MM-S11 copied verbatim from
       `Ka0sAddonsCommonTasks/docs/2026-09-26-NAVRAIL_ADOPTION/06_SMOKE_TESTS.md`, with an empty
       Result column. Add §36 to the file's suite index, if it keeps one.

  `crlf` every doc edited.

- [ ] **Step 9: Gate, inventory, badge.** Addon gate and lizard: 0 FAIL, 0/0, no lizard output, and
  no `EOL FAIL`. Regenerate `docs/test-cases.md` and set the badge. Two cases were deleted and one
  added, so the count is 2091. Then run the doc tests' grep for stale citations:

```sh
grep -rnE 'settings/(Frame|Header|Bars|Tooltip|Visibility|Columns)\.lua:[0-9]+' docs README.md | head -40
```

  Every hit must still point at the named symbol. Fix any that moved.

- [ ] **Step 10: Commit.**

```sh
git add settings/Frame.lua settings/Header.lua settings/Bars.lua settings/Tooltip.lua settings/Visibility.lua \
  settings/Columns.lua settings/OptionsSetup.lua settings/Windows.lua settings/Schema.lua settings/Schema_Paths.lua \
  settings/Schema_Compose.lua settings/General.lua locales/enUS.lua MultiMeters.toc \
  tests/test_options_panel.lua tests/test_columns.lua tests/test_schema_paths.lua tests/test_surface_parity.lua \
  docs/settings-panel.md docs/common-tasks.md docs/module-map.md docs/ARCHITECTURE.md docs/schema.md \
  docs/smoke-tests.md docs/test-cases.md README.md
git status --porcelain                  # expect empty
git commit -m "NR-MM-04: Retire the six window sub-pages; the tree is General, Windows, Profiles" \
  -m "MultiMeters#55. Frame, Header, Bars, Tooltip, Visibility and Columns are entries of the Windows page only: each file keeps its rows' rationale and its entry registration and loses its builder, so no schema row, path or default moves. NS.SubPageLabel and the D6 nesting mark go with nothing left to nest. Player-facing text that named a retired page says Windows > <Entry>. The panel tests drive entries through SelectSection; docs, the module map and smoke-tests §36 follow." \
  -m "$TRAILERS"
```

(Add any other doc whose citations the gate moved.)

### Task NR-KC-02: the Grid page — Unit band, rail, entry

**Files:**
- Modify: `settings/Panel_Render.lua`: `Helpers.RenderUnitPanel` (:99-141) gains a fourth argument,
  `chrome`; the Grid block is inserted above the comment `--- Write one schema row through the seam
  and repaint any open panel's values.` (~:260).
- Create: `settings/Grid.lua`. Modify: `KickCD.toc` (`settings\Grid.lua` after `settings\Label.lua`
  :148, with its note; the Conventional note above `settings\Panel_Widgets.lua` :141-142).
- Modify: `settings/Icons.lua` (after the loop at :436), `settings/Castbar.lua` (after :578),
  `settings/Label.lua` (after :209): each registers its entry. Their pages stay until NR-KC-04.
- Modify: `locales/enUS.lua`: `L["Grid"]` beside `L["Icons"]` (:58), and three rail tooltips.
- Create: `tests/test_grid.lua`. Modify: `tests/run.lua` (`SUITES`: `"test_grid",` after
  `"test_options_panel",`).
- Modify: `tests/test_options_panel.lua`: `PAGE_KEYS`/`PAGE_FILES` (:111-112) gain `grid`, and the
  host-decoration list (:84-88) gains the three Grid members.
- Modify: `docs/settings-panel.md` (a new section above "## Per-unit pages"), `docs/module-map.md`
  (a `Grid.lua` entry after `Label.lua`'s, :283-290). Regenerated: `docs/test-cases.md`, the README
  badge.

**Interfaces:**
- Produces, on both arms (host code): `Helpers.RegisterGridSection(key, label, spec)`,
  `Helpers.GridSection(key) -> { key, label, tooltip } | nil`, `Helpers.RenderGridPage(ctx)` and
  `Helpers.__bindGridPage(ctx)`. `Helpers.RenderUnitPanel(ctx, panelKey, afterGroup, chrome)` gains
  `chrome`, a `fn(ctx)` called after the band and before either strip path.
- ctx fields: `ctx.activeSection` (`icons`|`castbar`|`label`), `ctx.sectionTabs`,
  `ctx.__renderedSection`.
- The Grid page's Defaults in this task is `H.RestoreDefaults(ctx.activeSection, ctx)`, the rows the
  entry's page restored (both units). NR-KC-03 narrows it to the unit in the band.

- [ ] **Step 1: Write the failing tests.** Create `tests/test_grid.lua`, then `crlf` it:

```lua
-- tests/test_grid.lua
--
-- The Grid page (KickCD#33): Icons, Cast bar and Text Label as one page. The Unit band across the
-- top, the nav rail (Icons, Cast bar, Text Label), each entry's own tab strip, the tab each entry
-- keeps, and a linked Focus under the rail -- and, from NR-KC-03, Defaults for the unit in the band
-- and the deep links. The pattern is AuraMaster's Containers page (#6) on LibKa0s v1.61.0's
-- O.NavRail. Pinned from the outside: a fresh instance per case, the page shown the way Blizzard
-- shows it, the rail clicked through the library's own entry buttons.

local T = _G.KICKCD_TEST
local test, assertEqual, assertTrue, assertFalse =
    T.test, T.assertEqual, T.assertTrue, T.assertFalse

local RAIL_ORDER = "icons,castbar,label"

--- A fresh instance with spies on the three chrome calls, recording each page's last rail and strip,
--- and handles on its Grid page. `mutate` goes to T.load (it runs on the mock before any file loads).
local function env(mutate)
    local inst = T.load(true, true, mutate)
    local NS = inst.NS
    local H = NS.Settings.Helpers
    local rails, strips, calls = {}, {}, {}
    local navRail, tabStrip, pageBanner = H.NavRail, H.TabStrip, H.PageBanner
    H.NavRail = function(ctx, spec, ...)
        calls[#calls + 1] = "NavRail"
        rails[ctx] = spec
        return navRail(ctx, spec, ...)
    end
    H.TabStrip = function(ctx, spec, ...)
        calls[#calls + 1] = "TabStrip"
        strips[ctx] = spec
        return tabStrip(ctx, spec, ...)
    end
    H.PageBanner = function(ctx, spec, ...)
        calls[#calls + 1] = "PageBanner"
        return pageBanner(ctx, spec, ...)
    end

    local P = { inst = inst, NS = NS, H = H, L = NS.L, calls = calls }

    function P.ctx() return H.__panelFor("grid") end

    --- Show the Grid page the way Blizzard does, driving the genuine deferred render.
    function P.show()
        local ctx = P.ctx()
        assertTrue(ctx ~= nil, "no Grid page registered")
        ctx.panel:Hide()
        ctx.panel:Show()
        -- The render is pcall'd by the library, so a raise shows up as no rail, not as an error.
        assertTrue(rails[ctx] ~= nil, "the Grid page drew no rail (its renderer raised)")
        return ctx
    end

    function P.railKeys()
        local out = {}
        for i, e in ipairs((rails[P.ctx()] or {}).entries or {}) do out[i] = e.key end
        return table.concat(out, ",")
    end

    function P.railValue() return (rails[P.ctx()] or {}).value end

    function P.tabLabels()
        local out = {}
        for i, t in ipairs((strips[P.ctx()] or {}).tabs or {}) do out[i] = t.label end
        return table.concat(out, "|")
    end

    --- The library's own rail button for entry `key` (ctx.__railKids is the rail's ledger, in order).
    function P.railButton(key)
        local ctx = P.ctx()
        for i, e in ipairs((rails[ctx] or {}).entries or {}) do
            if e.key == key then return ctx.__railKids[i] end
        end
        error("the rail drew no entry " .. tostring(key), 2)
    end

    --- Click rail entry `key` the way the player does (KickCD's frame mock runs a script with
    --- `_run`), and answer the page's ctx.
    function P.rail(key)
        local ctx = P.ctx()
        P.railButton(key):_run("OnClick")
        ctx.panel:Hide()
        ctx.panel:Show()
        return ctx
    end

    return P
end

--- The groups of one entry's rows for one unit, in declaration order: the strip it draws.
local function groupsOf(H, page, unit)
    local out, seen = {}, {}
    for _, def in ipairs(H.SchemaForPanel(page, unit)) do
        if def.group and not seen[def.group] then
            seen[def.group] = true
            out[#out + 1] = def.group
        end
    end
    return out
end

--- Link or unlink Focus's styling to Target's on this instance.
local function focusLink(P, linked)
    local cfg = P.NS.Units.Config("focus")
    assertTrue(cfg ~= nil, "sanity: Focus has a config")
    cfg.link = linked
end

-- ── the registry ─────────────────────────────────────────────────────────────────────────────

test("grid: Icons, Cast bar and Text Label register as Grid entries under their page keys, on both builds", function()
    local L = T.NS.L
    local LABELS = { icons = "Icons", castbar = "Cast bar", label = "Text Label" }
    local builds = {
        live = T.NS.Settings.Helpers,
        ["library-absent"] = T.load(true, false, nil, { libFiles = {} }).NS.Settings.Helpers,
    }
    for build, H in pairs(builds) do
        for key, label in pairs(LABELS) do
            -- red under: a page file registering no entry, or the registry kept behind the fork
            local s = H.GridSection and H.GridSection(key)
            assertTrue(s ~= nil, build .. ": " .. key .. " registered no entry")
            assertEqual(s.key, key, build .. ": " .. key .. " keeps its page key, so every row path is unchanged")
            assertEqual(s.label, L[label], build .. ": " .. key .. "'s rail label")
            assertEqual(type(s.tooltip), "string", build .. ": " .. key .. " carries a rail tooltip")
        end
        assertFalse(H.GridSection("general") ~= nil, build .. ": General is a page of its own, not a Grid entry")
    end
end)

-- ── the page ─────────────────────────────────────────────────────────────────────────────────

test("grid: the Unit band, then the rail Icons, Cast bar, Text Label, 120 wide, opening on Icons", function()
    local P = env()
    local ctx = P.show()
    -- red under: the rail in TOC order or missing an entry, or the page opening elsewhere
    assertEqual(P.railKeys(), RAIL_ORDER)
    assertEqual(ctx.activeSection, "icons")
    assertEqual(P.railValue(), "icons")
    assertEqual(ctx.railWidth, 120)
    assertEqual(ctx.__bannerWidget and ctx.__bannerWidget.labelText, P.L["Unit"], "the band is the Unit picker")
    assertEqual(P.tabLabels(), table.concat(groupsOf(P.H, "icons", "target"), "|"))
end)

test("grid: the draw order is PageBanner, NavRail, TabStrip", function()
    local P = env()
    P.show()
    -- red under: the rail drawn before the band (its top ignores the band) or after the strip (the
    -- strip places itself with no inset)
    assertEqual(table.concat({ P.calls[1], P.calls[2], P.calls[3] }, ","), "PageBanner,NavRail,TabStrip")
end)

test("grid: a rail click draws that entry's own strip under the same band", function()
    local P = env()
    P.show()
    local ctx = P.rail("castbar")
    local want = groupsOf(P.H, "castbar", "target")
    assertEqual(ctx.activeSection, "castbar")
    assertEqual(P.railValue(), "castbar")
    -- red under: every entry rendered under one fixed page key (Icons' strip on Cast bar)
    assertEqual(P.tabLabels(), table.concat(want, "|"))
    assertEqual(want[4], P.L["Font"], "sanity: Cast bar's fourth tab is Font")
    assertEqual(ctx.__bannerWidget.labelText, P.L["Unit"], "the band is drawn with the entry")
    assertEqual(ctx.unit, "target")
end)

-- Review Focus 3.
test("grid: each entry keeps its own tab, including one chosen by the library's own strip click", function()
    local P = env()
    P.show()
    local L = P.L
    local ctx = P.rail("castbar")
    ctx.__tabKids[4]:_run("OnClick")                -- the library's own strip click: no host render
    assertEqual(ctx.activeTab, L["Font"])
    P.rail("label")
    assertEqual(ctx.activeTab, L["General"], "Text Label opens on its first tab")
    ctx.__tabKids[2]:_run("OnClick")
    assertEqual(ctx.activeTab, L["Placement"])
    P.rail("icons")
    P.rail("castbar")
    -- red under: one scalar activeTab for the page, or a stash only on host renders (the strip
    -- click above never reaches the host)
    assertEqual(ctx.activeTab, L["Font"])
    P.rail("label")
    assertEqual(ctx.activeTab, L["Placement"])
end)

test("grid: choosing the other unit in the band keeps the entry and its tab", function()
    local P = env()
    focusLink(P, false)
    P.show()
    local ctx = P.rail("castbar")
    ctx.__tabKids[4]:_run("OnClick")
    assertEqual(ctx.activeTab, P.L["Font"])
    ctx.__bannerWidget:__fire("OnValueChanged", "focus")
    assertEqual(P.H.ViewedUnit(), "focus")
    -- red under: a unit switch resetting the entry or the tab (options-ui-§14: the rail is not a picker)
    assertEqual(ctx.activeSection, "castbar")
    assertEqual(ctx.activeTab, P.L["Font"])
    assertEqual(ctx.unit, "focus", "the page now edits Focus")
end)

test("grid: a linked Focus keeps the rail; each entry draws its full strip, inert, over the link note alone", function()
    local P = env()
    focusLink(P, true)
    P.H.SetViewedUnit("focus")
    local ctx = P.show()
    -- red under: the rail drawn after RenderUnitPanel's linked branch has returned (a linked Focus
    -- with no rail), or drawn only on the RenderTabbedSchema path
    assertEqual(P.railKeys(), RAIL_ORDER)
    for _, key in ipairs({ "icons", "castbar", "label" }) do
        if ctx.activeSection ~= key then P.rail(key) end
        assertEqual(ctx.activeSection, key)
        local buttons = (ctx.__tabLayout or {}).buttons or {}
        assertEqual(#buttons, #groupsOf(P.H, key, "focus"), key .. ": one tab per schema group")
        for i, b in ipairs(buttons) do
            assertEqual(b.__enabled, false, key .. ": tab " .. i .. " is operable on a linked Focus")
        end
        local notes = 0
        for _, child in ipairs(ctx.scroll and ctx.scroll.children or {}) do
            if type(child.text) == "string" and child.text:find("Linked to Target", 1, true) then
                notes = notes + 1
            end
        end
        assertEqual(notes, 1, key .. ": the link note, once")
    end
end)
```

  Register the suite in `tests/run.lua`: after `    "test_options_panel",` add `    "test_grid",`.
  `crlf tests/test_grid.lua tests/run.lua`.

- [ ] **Step 2: Run and see them fail.**

```sh
/home/tushar/.claude/wow-addon/bin/ka0s-bounded lua tests/run.lua > /tmp/KickCD-run.txt 2>&1
grep -E '^  (FAIL|PASS)  grid:' /tmp/KickCD-run.txt
```

  Expected: all seven `grid:` cases `FAIL`. The registry case fails on `GridSection` being nil, and
  the page cases on "no Grid page registered".

- [ ] **Step 3: The chrome hook.** In `settings/Panel_Render.lua`:
  1. `function Helpers.RenderUnitPanel(ctx, panelKey, afterGroup)` becomes
     `function Helpers.RenderUnitPanel(ctx, panelKey, afterGroup, chrome)`.
  2. Directly after `    ctx.__bannerWidget = dd` (and its two comment lines above it), insert:

```lua

    -- The Grid page's nav rail (KickCD#33) goes in HERE: after the band, whose
    -- height it reads for its top, and before EITHER strip path below, which reads
    -- the inset it records. So a linked Focus keeps the rail too. A caller that
    -- passes no chrome draws exactly what it drew before.
    if chrome then chrome(ctx) end
```

- [ ] **Step 4: The Grid block.** In `settings/Panel_Render.lua`, insert above
  `--- Write one schema row through the seam and repaint any open panel's values.`:

```lua
-- ---------------------------------------------------------------------
-- The Grid page: the Unit band, the nav rail, the selected entry (#33)
-- ---------------------------------------------------------------------
--
-- Icons, Cast bar and Text Label are one page (settings/Grid.lua). The Unit
-- picker is the band, a nav rail (LibKa0s-Options' O.NavRail, options-ui-§13)
-- chooses the entry, and each entry keeps the tab strip its own page had. An
-- entry IS the old page key: every row keeps `panel`, `section`, `unit` and its
-- `units.<unit>.<page>.*` path, so /kcd, the defaults, profiles and
-- SchemaForPanel never see the rail. The entry and each entry's tab are session
-- state on the ctx, never persisted; the band stays the only picker, and a unit
-- switch leaves both alone (options-ui-§14). AuraMaster's Containers page (#6) is
-- the pattern.
--
-- Host code on BOTH arms: settings/OptionsSetup.lua's stub returns before this
-- file loads, so a library-absent build still has the registry the page files
-- call at load, and the stub owes nothing but O.NavRail's no-op.

local gridEntries = {}
-- The rail's order, fixed here rather than taken from the TOC.
local GRID_ORDER = { "icons", "castbar", "label" }
-- The Grid page's ctx, bound by its builder: the one page SelectSection moves.
local gridCtx

--- Register one entry of the Grid page. Called at FILE LOAD by settings/Icons.lua,
--- Castbar.lua and Label.lua.
--- @param key string    the entry's page key: the `panel` its schema rows carry
--- @param label string  the rail entry's label
--- @param spec table    { tooltip = the rail entry's tooltip }
function Helpers.RegisterGridSection(key, label, spec)
    spec = spec or {}
    gridEntries[key] = { key = key, label = label, tooltip = spec.tooltip }
end

--- The registered entry `key`, or nil.
function Helpers.GridSection(key) return gridEntries[key] end

--- The entries the rail lists, in rail order. Every unit has all three.
local function railEntries()
    local out = {}
    for _, key in ipairs(GRID_ORDER) do
        if gridEntries[key] then out[#out + 1] = gridEntries[key] end
    end
    return out
end

--- The entry to draw: the one the page holds while the rail lists it, else the first.
local function settleEntry(ctx, list)
    for _, e in ipairs(list) do
        if e.key == ctx.activeSection then return e end
    end
    return list[1]
end

--- Keep the tab the page is on for the entry it last drew. Called before ANYTHING
--- moves the entry: the library's own strip click never calls back here
--- (RenderTabbedSchema re-renders the strip and the rows itself), so leaving is the
--- one moment the host sees the tab.
local function stashTab(ctx)
    local drawn = ctx.__renderedSection
    if drawn then ctx.sectionTabs[drawn] = ctx.activeTab end
    ctx.__renderedSection = nil
end

--- Bind the Grid page's ctx (settings/Grid.lua's builder). The page opens on Icons.
function Helpers.__bindGridPage(ctx)
    gridCtx = ctx
    ctx.sectionTabs = {}
    ctx.activeSection = GRID_ORDER[1]
end

--- Render the Grid page: the Unit band, the nav rail, then the entry's strip and
--- rows -- the library's draw order, PageBanner, NavRail, TabStrip. The band and
--- both strip paths are Helpers.RenderUnitPanel's; the rail goes in through its
--- chrome hook.
function Helpers.RenderGridPage(ctx)
    ctx.sectionTabs = ctx.sectionTabs or {}
    stashTab(ctx)
    local list = railEntries()
    local entry = settleEntry(ctx, list)
    if not entry then return end
    ctx.activeSection = entry.key
    ctx.activeTab = ctx.sectionTabs[entry.key]
    local entries = {}
    for i, e in ipairs(list) do entries[i] = { key = e.key, label = e.label, tooltip = e.tooltip } end
    Helpers.RenderUnitPanel(ctx, entry.key, nil, function(c)
        Helpers.NavRail(c, {
            entries  = entries,
            value    = entry.key,
            onSelect = function(key)
                stashTab(c)
                c.activeSection = key
                Helpers.RefreshPanel(c, true)
            end,
        })
    end)
    ctx.__renderedSection = entry.key
end

```

  End the Grid block with this test seam (NR-KC-03 keeps it):

```lua
--- Test seam: the ctx the Grid page bound, or nil before its builder ran.
function Helpers.__gridCtx() return gridCtx end
```

  `gridCtx` is read by `Helpers.SelectSection` from NR-KC-03 on. The seam is its reader until then,
  so luacheck has no assigned-but-never-accessed local (W231) at this commit.

- [ ] **Step 5: The page.** Create `settings/Grid.lua` (then `crlf`):

```lua
-- settings/Grid.lua
--
-- The Grid page (KickCD#33): Icons, Cast bar and Text Label as one page. The
-- Unit picker is the band across the top, the nav rail on the left chooses the
-- entry, and each entry keeps the tab strip its own page had. An entry IS the
-- old page key, so every row, `/kcd` path, default and profile is unchanged.
-- The registry, the renderer and the rail are settings/Panel_Render.lua's
-- (Helpers.RegisterGridSection, Helpers.RenderGridPage); the rows are declared
-- where they always were, in settings/Icons.lua, Castbar.lua and Label.lua.
--
-- The library owns WHEN this draws (H.SetRenderer): first show, and again when a
-- refresh marked it dirty while it was hidden -- which is what makes the Unit
-- band, the General page's Focus link and a deep link reach this page at all.

local _, NS = ...
local L = NS.L
local H = NS.Settings.Helpers

local function Build(mainCategory)
    if not (Settings and Settings.RegisterCanvasLayoutSubcategory) then
        return nil
    end

    local ctx = H.CreatePanel("KickCDGridPanel", L["Grid"], {
        pageKey        = "grid",
        defaultsButton = true,
    })
    -- Parked, not wired: the button is built at the panel's first OnShow and
    -- captures this handler then, so it reads the entry at CLICK time rather than
    -- fixing the one on screen when the page was built.
    ctx.panel.defaultsOnClick = function()
        H.RestoreDefaults(ctx.activeSection, ctx)
    end

    H.__bindGridPage(ctx)
    H.SetRenderer(ctx, H.RenderGridPage)

    return Settings.RegisterCanvasLayoutSubcategory(
        mainCategory, ctx.panel, L["Grid"])
end

if NS.RegisterOptionsPage then
    NS.RegisterOptionsPage("grid", L["Grid"], Build)
end
```

  In `KickCD.toc`, insert after `settings\Label.lua`:

```
# LOAD-BEARING POSITION: the Grid page (KickCD#33) registers here, and page order is
# registration order, so the tree reads General, Grid, Spells, Profiles. It binds the
# entries settings\Icons.lua, Castbar.lua and Label.lua registered above it.
settings\Grid.lua
```

  and change the note `# Conventional position: below settings\Panel.lua the page files are free
  relative to` / `# each other; the one exception, settings\Spells_Rows.lua, carries its own note.` to:

```
# Conventional position: below settings\Panel.lua the page files are free relative to
# each other, bar two notes: settings\Grid.lua's and settings\Spells_Rows.lua's. The
# Icons, Cast bar and Text Label files call Helpers.RegisterGridSection, which
# settings\Panel_Render.lua publishes, at file scope, so they stay below it.
```

  `crlf KickCD.toc settings/Grid.lua`.

- [ ] **Step 6: The three entries.** Directly after `for _, u in ipairs(NS.Units.LIST) do
  addUnitRows(u) end` in each file, insert:

  `settings/Icons.lua`:

```lua

-- The Icons entry of the Grid page (KickCD#33).
H.RegisterGridSection("icons", L["Icons"], {
    tooltip = L["The interrupt icons: their size, layout, states, border, annotations and ready glow."],
})
```

  `settings/Castbar.lua`:

```lua

-- The Cast bar entry of the Grid page (KickCD#33).
H.RegisterGridSection("castbar", L["Cast bar"], {
    tooltip = L["The cast bar: its size, position, icon, fonts and the colors for casts you can and cannot interrupt."],
})
```

  `settings/Label.lua`:

```lua

-- The Text Label entry of the Grid page (KickCD#33).
H.RegisterGridSection("label", L["Text Label"], {
    tooltip = L["The unit's identity label: what it says, where it sits and its font."],
})
```

- [ ] **Step 7: The locale.** In `locales/enUS.lua`, after `L["Icons"]                       = "Icons"`,
  add `L["Grid"]                        = "Grid"`. At the end of the file's settings block, next to
  the other page tooltips, add:

```lua
-- The Grid page's rail (KickCD#33): one tooltip per entry.
L["The interrupt icons: their size, layout, states, border, annotations and ready glow."] =
    "The interrupt icons: their size, layout, states, border, annotations and ready glow."
L["The cast bar: its size, position, icon, fonts and the colors for casts you can and cannot interrupt."] =
    "The cast bar: its size, position, icon, fonts and the colors for casts you can and cannot interrupt."
L["The unit's identity label: what it says, where it sits and its font."] =
    "The unit's identity label: what it says, where it sits and its font."
```

  `crlf` every file edited in Steps 3-7.

- [ ] **Step 8: The existing cases.** In `tests/test_options_panel.lua`:
  - `local PAGE_KEYS  = { "general", "icons", "castbar", "label", "spells", "profiles" }` becomes
    `local PAGE_KEYS  = { "general", "icons", "castbar", "label", "grid", "spells", "profiles" }`, and
    `PAGE_FILES` gains `"Grid"` in the same place:
    `{ "General", "Icons", "Castbar", "Label", "Grid", "Spells", "Profiles" }`. The comment above them
    says "The six pages"; it becomes "The pages", and "SIX subcategories" in the case below becomes
    "one subcategory per page".
  - The host-decoration list `"RenderUnitPanel", "PartitionUnitRows", …` gains
    `"RegisterGridSection", "GridSection", "RenderGridPage",`.
  - `crlf tests/test_options_panel.lua`.

- [ ] **Step 9: Run and see them pass.**

```sh
/home/tushar/.claude/wow-addon/bin/ka0s-bounded lua tests/run.lua > /tmp/KickCD-run.txt 2>&1
grep -E '^  (FAIL|PASS)  grid:' /tmp/KickCD-run.txt; grep -c '^  FAIL' /tmp/KickCD-run.txt
```

  Expected: seven `grid:` `PASS`, 0 `FAIL`. KC-20's case ("a linked Focus page draws the full strip,
  inert, and only the link note") passes unchanged: it calls `RenderUnitPanel` with no chrome. If a
  page case reports "drew no rail", grep the run for the library's `RENDER_FAILED` line.

- [ ] **Step 10: Docs.**
  - `docs/settings-panel.md`: insert, as its own lines, immediately above `## Per-unit pages (Icons /
    Cast bar / Text Label)`:

```markdown
## The Grid page

**Icons, Cast bar and Text Label are one page, Grid** (KickCD#33, `options-ui-§13` and
`options-ui-§14`). It has three pinned pieces, drawn in the library's order on every full render:
`PageBanner`, `NavRail`, `TabStrip`.

- **The band** is the Unit picker, drawn by `Helpers.RenderUnitPanel` exactly as the three pages drew
  it. It is the page's only picker, shared by every entry through `Helpers.ViewedUnit` /
  `Helpers.SetViewedUnit`.
- **The rail** (LibKa0s `O.NavRail`, 120 wide) lists the **entries** Icons · Cast bar · Text Label, in
  `GRID_ORDER` (`settings/Panel_Render.lua`). An entry **is** the old page key (`icons`, `castbar`,
  `label`), so every row keeps `panel`, `section`, `unit` and its `units.<unit>.<page>.*` path, and
  `/kcd`, the defaults and profiles never see the rail. Each page file registers its entry at load
  with `Helpers.RegisterGridSection`, which is host code on both arms.
- **The strip** is the entry's own, through `Helpers.RenderUnitPanel(ctx, entry, nil, chrome)`. The
  rail goes in through the `chrome` hook, after the band and before **either** strip path, so a
  linked Focus keeps the rail over its inert strip and link note.

`Helpers.RenderGridPage` draws the page. `ctx.activeSection` is the entry on screen, and
`ctx.sectionTabs[entry]` holds each entry's tab. Both are session state and never persisted. The tab
is stashed **before anything moves the entry**, because the library's own strip click never calls
back into the host. So Cast bar -> Font, then Icons, then Cast bar again lands on Font. Picking the
other unit in the band keeps the entry and its tab. Pinned by `tests/test_grid.lua`.
```

  - `docs/module-map.md`: in the settings tree, directly after `Label.lua`'s entry (its last
    continuation line, before the next `├──`), insert as its own lines:

```
    ├── Grid.lua      — the Grid page (KickCD#33): Icons, Cast bar and Text Label as
                        entries on a nav rail under the Unit band; builds "grid", binds
                        the entries; renderer and registry in Panel_Render.lua
```

    In the same tree, `Panel_Render.lua`'s entry gains "the Grid page's entry registry and
    renderer (RegisterGridSection, RenderGridPage)".

  `crlf` both, then `git diff docs/module-map.md` and confirm no neighboring row changed.

- [ ] **Step 11: Gate, inventory, badge.** Run the addon gate and the lizard line from the command
  shorthands. Expected: 0 FAIL, 0/0, no lizard output. Regenerate `docs/test-cases.md` and set the
  badge (1196 cases).

- [ ] **Step 12: Commit.**

```sh
git add settings/Panel_Render.lua settings/Grid.lua settings/Icons.lua settings/Castbar.lua settings/Label.lua \
  KickCD.toc locales/enUS.lua tests/test_grid.lua tests/run.lua tests/test_options_panel.lua \
  docs/settings-panel.md docs/module-map.md docs/test-cases.md README.md
git status --porcelain                  # expect empty
git commit -m "NR-KC-02: The Grid page: Icons, Cast bar and Text Label on a nav rail" \
  -m "KickCD#33. A Grid entry registry (Helpers.RegisterGridSection / GridSection, host code on both arms) names Icons, Cast bar and Text Label, each its old page key, so no row moves. Helpers.RenderGridPage draws the Unit band, the rail (LibKa0s v1.61.0 O.NavRail) and the entry's own strip through RenderUnitPanel's new chrome hook, so a linked Focus keeps the rail over its inert strip and link note. Each entry keeps its tab across rail clicks, strip clicks and unit switches. The new settings/Grid.lua registers between General and Spells; its Defaults restores the entry's rows (both units) until NR-KC-03 narrows it. The three pages still register; NR-KC-04 retires them." \
  -m "$TRAILERS"
```

### Task NR-KC-03: Defaults for the unit in the band, and deep links

**Files:**
- Modify: `settings/Panel_Render.lua`: after `Helpers.RenderGridPage`, add
  `Helpers.RestoreGridSection`, `Helpers.SelectSection` and the `SelectTab` route.
- Modify: `settings/Grid.lua` (the Defaults handler and its tooltip), `settings/Panel_Widgets.lua`
  (`Helpers.OpenPageTab`, :135-150), `locales/enUS.lua` (the tooltip).
- Modify: `docs/ARCHITECTURE.md` (a row in "Documented deviations", after the `options-ui-§15` row),
  `docs/settings-panel.md` (two paragraphs in "The Grid page").
- Modify: `tests/test_grid.lua` (five cases). Regenerated: `docs/test-cases.md`, the README badge.

**Interfaces:**
- Produces: `Helpers.RestoreGridSection(ctx)` (both arms; refused in combat through
  `Helpers.__combatRefused` when the library is present), `Helpers.SelectSection(key, tabKey) ->
  boolean`, and a `Helpers.SelectTab` that routes entry keys to `SelectSection`.
  `Helpers.OpenPageTab(pageKey, tabKey)` routes `icons`, `castbar` and `label` to Grid.
- Consumes: `NS.Settings.Store.BulkBegin/BulkEnd/ApplyDefault` (the schema seam's bracket and
  default writer), `Helpers.SchemaForPanel(panel, unit)`, `Helpers.ViewedUnit()`.
- Unchanged on purpose: the library's `H.RestoreDefaults(page)` still resets every unit, and
  `tests/test_settings_log.lua` keeps pinning it (02_SPEC R8).

- [ ] **Step 1: Write the failing tests.** Append to `tests/test_grid.lua`:

```lua

-- ── Defaults, deep links, SelectTab (NR-KC-03) ─────────────────────────────────────────────

--- The first stored boolean row of `panel` for `unit`: one to move off its default.
local function boolRow(H, panel, unit)
    for _, row in ipairs(H.SchemaForPanel(panel, unit)) do
        if row.type == "bool" and row.default ~= nil and not row.sessionOnly and row.path then return row end
    end
end

-- Review Focus 4.
test("grid: Defaults restores only the active entry's rows, for the unit in the band", function()
    local P = env()
    local H, S = P.H, P.NS.Settings.Store
    focusLink(P, false)
    P.show()
    local ctx = P.rail("castbar")
    local tc, fc, ti = boolRow(H, "castbar", "target"), boolRow(H, "castbar", "focus"), boolRow(H, "icons", "target")
    for _, row in ipairs({ tc, fc, ti }) do
        assertTrue(row ~= nil, "sanity: a boolean row to move")
        assertTrue(S.Set(row.path, not row.default))
    end

    local brackets = {}
    local begin = S.BulkBegin
    S.BulkBegin = function(act, scope, ...)
        brackets[#brackets + 1] = tostring(act) .. " " .. tostring(scope)
        return begin(act, scope, ...)
    end
    local ok, err = pcall(ctx.panel.defaultsOnClick)
    S.BulkBegin = begin
    assertTrue(ok, tostring(err))

    -- red under: the library's page walk (Focus's row reset too), or a closure that fixed the entry
    -- when the page was built (Icons' rows reset from Cast bar)
    assertEqual(S.Get(tc.path), tc.default, "Target's cast bar row is back")
    assertEqual(S.Get(fc.path), not fc.default, "Focus's cast bar row is not the unit in the band's")
    assertEqual(S.Get(ti.path), not ti.default, "Target's icons row is not the active entry's")
    assertEqual(table.concat(brackets, "|"), "reset castbar", "one bulk bracket, scoped to the entry")

    ctx.__bannerWidget:__fire("OnValueChanged", "focus")
    ctx.panel.defaultsOnClick()
    assertEqual(S.Get(fc.path), fc.default, "with Focus in the band, Focus's row")
end)

test("grid: the Defaults tooltip says it acts on the unit in the band", function()
    local P = env()
    local ctx = P.show()
    assertEqual(ctx.panel.defaultsTooltip,
        P.L["Restore the selected unit's settings in the section on screen to their defaults. The other unit keeps its own."])
end)

--- A fresh Grid page whose subcategories answer GetID (KickCD's mock categories do not), recording
--- by tree label the category every OpenToCategory lands on.
local function recordingOpens()
    local byId, opened, count = {}, {}, 0
    local P = env(function(mocks)
        local register = mocks.Settings.RegisterCanvasLayoutSubcategory
        mocks.Settings.RegisterCanvasLayoutSubcategory = function(parent, panel, name)
            local cat = register(parent, panel, name)
            count = count + 1
            local id = 100 + count
            byId[id] = name
            cat.GetID = function() return id end
            return cat
        end
        mocks.Settings.OpenToCategory = function(id) opened[#opened + 1] = byId[id] or "main" end
    end)
    return P, opened
end

-- Review Focus 5.
test("grid: a former page key opens Grid on that entry and tab, drawn on its next show", function()
    local P, opened = recordingOpens()
    local ctx = P.show()
    ctx.panel:Hide()                                -- the settings window is closed
    -- red under: OpenPageTab looking "castbar" up in NS.Settings.categoryFor alone (the Cast bar
    -- page today, nothing once it retires)
    assertTrue(P.H.OpenPageTab("castbar", P.L["Font"]))
    assertEqual(opened[#opened], P.L["Grid"])
    assertEqual(ctx.activeSection, "castbar", "selected before the show")
    ctx.panel:Show()
    assertEqual(P.railValue(), "castbar", "and drawn on it")
    assertEqual(ctx.activeTab, P.L["Font"], "on the named tab")
    assertTrue(P.H.OpenPageTab("general", P.L["Units"]), "the linked-Focus note's own link is unchanged")
    assertEqual(opened[#opened], P.L["General"])
end)

test("grid: SelectTab on an entry key selects the entry and its tab; other pages stay the library's", function()
    local P = env()
    local ctx = P.show()
    local H, L = P.H, P.L
    -- red under: the call reaching the library's SelectTab, which moves the page's one scalar tab
    -- (or finds no page once the three retire)
    assertTrue(H.SelectTab("label", L["Placement"]))
    assertEqual(ctx.activeSection, "label")
    assertEqual(ctx.activeTab, L["Placement"])
    assertTrue(H.SelectTab("general", L["Units"]), "the General page is the library's")
    assertEqual(H.__panelFor("general").activeTab, L["Units"])
end)

test("grid: selecting an entry is refused in combat and moves nothing", function()
    local P = env()
    local ctx = P.show()
    P.inst.mocks.InCombatLockdown = function() return true end
    -- red under: SelectSection without the library's refusal (a structural render in combat)
    local ok = P.H.SelectSection("label")
    P.inst.mocks.InCombatLockdown = function() return false end
    assertFalse(ok)
    assertEqual(ctx.activeSection, "icons")
end)
```

  `crlf tests/test_grid.lua`.

- [ ] **Step 2: Run and see them fail.**

```sh
/home/tushar/.claude/wow-addon/bin/ka0s-bounded lua tests/run.lua > /tmp/KickCD-run.txt 2>&1
grep -E '^  FAIL' /tmp/KickCD-run.txt
```

  Expected: the five new `grid:` cases fail. The Defaults case fails because Focus's row is reset
  too, the tooltip case because it is the library default, the deep link because
  `OpenPageTab("castbar")` opens the Cast bar page, and `SelectTab`/`SelectSection` because
  `SelectSection` is nil.

- [ ] **Step 3: Defaults, SelectSection, the SelectTab route.** In `settings/Panel_Render.lua`, after
  the `end` of `Helpers.RenderGridPage`, insert:

```lua

--- The Grid page's Defaults: the active entry's rows FOR THE UNIT IN THE BAND, and
--- no other unit's. The owner's ruling for KickCD#33, and a documented deviation
--- (docs/ARCHITECTURE.md, options-ui-§13): the library's O.RestoreDefaults resets
--- every unit of a page on purpose, and it still does when called directly.
---
--- The library's own bracket, driven by hand: one `reset <entry>` act, so the
--- console logs one `[Set] reset <entry>: N rows` line and no line per row
--- (debug-logging-§10). Refused in combat, as the library's page reset is.
function Helpers.RestoreGridSection(ctx)
    if Helpers.__combatRefused and Helpers.__combatRefused() then return end
    local entry = gridEntries[ctx and ctx.activeSection]
    if not entry then return end
    local Store = NS.Settings.Store
    local rows = Helpers.SchemaForPanel(entry.key, Helpers.ViewedUnit())
    Store.BulkBegin("reset", entry.key)
    local ok, err = pcall(function()
        for _, row in ipairs(rows) do Store.ApplyDefault(row) end
    end)
    Store.BulkEnd("reset", entry.key, nil, err)
    if not ok then error(err, 0) end
    if Helpers.RefreshScalars then Helpers.RefreshScalars() end
end

--- Select entry `key` on the Grid page, and optionally its tab: the one seam a
--- link, a deep link or a suite moves the entry through. A hidden page is marked
--- owed a render and draws the entry on its next show. Refused in combat, as a tab
--- switch is (options-ui-§2, §13).
--- @return boolean  whether the entry was selected
function Helpers.SelectSection(key, tabKey)
    if Helpers.__combatRefused and Helpers.__combatRefused() then return false end
    local ctx = gridCtx
    if not (ctx and gridEntries[key]) then return false end
    stashTab(ctx)
    ctx.activeSection = key
    if tabKey ~= nil then ctx.sectionTabs[key] = tabKey end
    Helpers.RefreshPanel(ctx, true)
    return true
end

-- The library's SelectTab moves one PAGE's tab. An entry key is no page of its own
-- (KickCD#33): it routes to SelectSection, so a link written against the old page
-- keys still lands. Any other key -- General, Spells -- is the library's.
local selectTab = Helpers.SelectTab
function Helpers.SelectTab(pageKey, tabKey)
    if gridEntries[pageKey] then return Helpers.SelectSection(pageKey, tabKey) end
    return selectTab(pageKey, tabKey)
end
```

- [ ] **Step 4: The page's handler and tooltip.** In `settings/Grid.lua`, the `CreatePanel` options
  gain `defaultsTooltip`, and the handler calls the new function:

```lua
    local ctx = H.CreatePanel("KickCDGridPanel", L["Grid"], {
        pageKey         = "grid",
        defaultsButton  = true,
        defaultsTooltip = L["Restore the selected unit's settings in the section on screen to their defaults. The other unit keeps its own."],
    })
    -- Parked, not wired: the button is built at the panel's first OnShow and
    -- captures this handler then, so it reads the entry at CLICK time. It restores
    -- the entry's rows for the unit in the band only (Helpers.RestoreGridSection).
    ctx.panel.defaultsOnClick = function()
        H.RestoreGridSection(ctx)
    end
```

  In `locales/enUS.lua`, next to the rail tooltips, add:

```lua
L["Restore the selected unit's settings in the section on screen to their defaults. The other unit keeps its own."] =
    "Restore the selected unit's settings in the section on screen to their defaults. The other unit keeps its own."
```

- [ ] **Step 5: The deep link.** In `settings/Panel_Widgets.lua`, `Helpers.OpenPageTab` becomes:

```lua
function Helpers.OpenPageTab(pageKey, tabKey)
    if refusedInCombat() then return false end

    -- A former page key is an entry of the Grid page now (KickCD#33): select the
    -- entry and its tab there, then open Grid. SelectSection marks a hidden page owed
    -- a render, so the entry is what the switch below draws.
    if Helpers.GridSection and Helpers.GridSection(pageKey) then
        if not Helpers.SelectSection(pageKey, tabKey) then return false end
        pageKey, tabKey = "grid", nil
    end

    local ctx = Helpers.__panelFor and Helpers.__panelFor(pageKey)
    if ctx and tabKey then ctx.activeTab = tabKey end

    local id = categoryID(pageKey)
    if not (id and Settings and Settings.OpenToCategory) then return false end

    Settings.OpenToCategory(id)
    -- The destination page may already have been rendered, on another tab. This
    -- is structural -- a different tab is different rows -- so it is the full
    -- sweep rather than a scalar refresh.
    Helpers.RefreshAllPanels()
    return true
end
```

  Add one sentence to its docstring: "An entry key of the Grid page (`icons`, `castbar`, `label`)
  opens Grid on that entry and tab."

  `crlf` every file edited in Steps 3-5.

- [ ] **Step 6: Run and see them pass.** Rerun Step 2's commands. Expected: 0 `FAIL`, twelve `grid:`
  `PASS`. `tests/test_settings_log.lua`'s "`H.RestoreDefaults('castbar')` … 0 rows" case is unchanged
  and passes. The library's page walk was not touched.

- [ ] **Step 7: The deviation, and the doc.**
  - `docs/ARCHITECTURE.md`, "Documented deviations": insert as its own line, directly after the row
    starting `` | `options-ui-§15` | ``:

```markdown
| `options-ui-§13` | The Grid page's **Defaults** restores the active rail entry's rows **for the unit in the band only** (`Helpers.RestoreGridSection`, `settings/Panel_Render.lua`). §13 bounds a railed page's Defaults by "the set the folded sub-page's own button restored", and the Icons, Cast bar and Text Label pages' own buttons reset **both** units: the library's `O.RestoreDefaults` omits the unit filter on purpose. | The owner's ruling for KickCD#33 (2026-09-26). The band names the unit the page is editing, and a Defaults that reached the unit off screen would change settings the player cannot see. MultiMeters' Windows page behaves the same way with no deviation, because its rows are window-relative. The library's page walk is unchanged, so `H.RestoreDefaults(page)` still resets every unit (`tests/test_settings_log.lua`). | 2026-09-26 | options-ui-§13 states the Defaults scope for a railed page whose band picks one of several instances (either way), **or** the owner reverts the Grid page to both units. |
```

  - `docs/settings-panel.md`, at the end of "## The Grid page", add:

```markdown
**Defaults** reads the entry **at click time** (the library captures the handler once, at the first
show) and restores that entry's rows **for the unit in the band only**
(`Helpers.RestoreGridSection`). The other unit keeps its values. That is the owner's ruling, and a
[documented deviation](ARCHITECTURE.md#documented-deviations) from `options-ui-§13`, whose railed
Defaults would reset both units as the three pages' buttons did. It is one bulk act, so the console
logs one `[Set] reset <entry>: N rows` line. The library's `H.RestoreDefaults(page)` is unchanged and
still resets every unit when called directly.

**Deep links.** `Helpers.OpenPageTab("icons"|"castbar"|"label", tab)` opens Grid on that entry and
tab, and the other page keys open their own page as before. `Helpers.SelectSection(entry, tab)` is the
one seam that moves the entry, and the host's `Helpers.SelectTab` routes an entry key to it. A hidden
page is marked owed a render and draws the entry on its next show. Both refuse under combat.
```

  `crlf docs/ARCHITECTURE.md docs/settings-panel.md`, then `git diff docs/ARCHITECTURE.md` and confirm
  no neighboring row changed.

- [ ] **Step 8: Gate, inventory, badge.** Run the addon gate and the lizard line: 0 FAIL, 0/0, no
  lizard output. Regenerate `docs/test-cases.md` and set the badge (1201 cases).

- [ ] **Step 9: Commit.**

```sh
git add settings/Panel_Render.lua settings/Grid.lua settings/Panel_Widgets.lua locales/enUS.lua \
  tests/test_grid.lua docs/ARCHITECTURE.md docs/settings-panel.md docs/test-cases.md README.md
git status --porcelain                  # expect empty
git commit -m "NR-KC-03: Grid Defaults for the unit in the band; deep links open Grid on an entry" \
  -m "KickCD#33. The Grid page's Defaults restores the active entry's rows for the unit in the band only (Helpers.RestoreGridSection, one bulk act), per the owner's ruling, and docs/ARCHITECTURE.md records it as a deviation from options-ui-§13; the library's page walk still resets every unit. Helpers.OpenPageTab sends icons/castbar/label to Grid on that entry and tab, Helpers.SelectSection moves the entry (refused in combat, drawn on the next show of a hidden page), and Helpers.SelectTab routes entry keys to it." \
  -m "$TRAILERS"
```

### Task NR-KC-04: retire the Icons, Cast bar and Text Label pages

**Files:**
- Modify: `settings/Icons.lua`, `settings/Castbar.lua`, `settings/Label.lua`: the builder and the page
  registration go, and the header comment says "entry". The rows and the entry registration stay.
- Modify: `settings/Slash.lua` (:212-245, the retired `/kcd reset <page>` answer and its comment),
  `settings/OptionsSetup.lua:384` (a comment), `settings/Panel.lua:362-365` (a comment),
  `settings/General.lua:214` (a comment naming the pages), `KickCD.toc` (:127-132 note).
- Modify tests: `tests/test_options_panel.lua` (`PAGE_KEYS`/`PAGE_FILES`, the linked-note case
  :667-707, the header comment :17-22).
- Modify docs: `docs/settings-panel.md`, `docs/module-map.md`, `README.md`, `docs/schema.md:196`,
  `docs/smoke-tests.md`. Regenerated: `docs/test-cases.md` (and the badge, if the count moved; it
  should not).

**Interfaces:** no new ones. Afterwards `NS.Settings.categoryFor` holds `general`, `grid`, `spells`
and `profiles`, and `Helpers.__panelFor("castbar")` is nil. Every link goes through `OpenPageTab`'s
Grid route.

- [ ] **Step 1: Rewrite the tests first.** In `tests/test_options_panel.lua`:
  - `PAGE_KEYS` becomes `{ "general", "grid", "spells", "profiles" }`, and `PAGE_FILES` becomes
    `{ "General", "Grid", "Spells", "Profiles" }`.
  - The file's header comment: "all five of this addon's pages (settings/General.lua:226,
    Icons.lua:448, Castbar.lua:561, Label.lua:216, Spells.lua:1113)" becomes "every page this addon
    builds a canvas for (settings/General.lua, Grid.lua and Spells.lua)".
  - In "the linked-Focus note opens General on its Units tab", replace

```lua
    local ctx = iH.__panelFor("castbar")
    assertTrue(ctx ~= nil, "the Cast bar page must be registered")
    ctx.panel:Show()
    iH.RefreshPanel(ctx, true)
```

    with

```lua
    local ctx = iH.__panelFor("grid")
    assertTrue(ctx ~= nil, "the Grid page must be registered")
    assertTrue(iH.SelectSection("castbar"), "the Grid page lists no Cast bar entry")
    ctx.panel:Show()
    iH.RefreshPanel(ctx, true)
```

  `crlf tests/test_options_panel.lua`.

- [ ] **Step 2: Run and see what fails.**

```sh
/home/tushar/.claude/wow-addon/bin/ka0s-bounded lua tests/run.lua > /tmp/KickCD-run.txt 2>&1
grep -E '^  FAIL' /tmp/KickCD-run.txt
```

  Expected: "every page registers exactly once, through the library's registry" fails (seven pages,
  four expected). Nothing else fails.

- [ ] **Step 3: Retire the builders.** For each of the three files, delete from `local function
  Build(mainCategory)` (with the `-- Builder` rule block above it, where there is one) through the
  end of the file:

```sh
for f in Icons Castbar Label; do
  perl -0pi -e 's/(\r?\n)(?:-- -+\r?\n-- Builder\r?\n-- -+\r?\n\r?\n)?local function Build\(mainCategory\).*\z/$1/s' settings/$f.lua
  crlf settings/$f.lua
  tail -6 settings/$f.lua
done
grep -nE 'CreatePanel|SetRenderer|RegisterOptionsPage|RenderUnitPanel\(c' settings/Icons.lua settings/Castbar.lua settings/Label.lua   # expect no output
```

  Each file must now end with its `H.RegisterGridSection(...)` block from NR-KC-02. Then fix each
  header:
  - `settings/Icons.lua:3-6`: "Icons canvas panel. Pure schema: every widget is a row in" /
    "KickCD.Settings.Schema; the builder calls Helpers.RenderUnitPanel, which" / "pins the Unit
    picker into the page's chrome band and hands the rows to" becomes "The Grid page's Icons entry
    (KickCD#33). Pure schema: every widget is a row in" / "KickCD.Settings.Schema; the Grid page
    (settings/Grid.lua) draws it through" / "Helpers.RenderGridPage, which pins the Unit picker into
    the band, draws the rail, and hands the rows to". The rest of the paragraph stays.
  - `settings/Castbar.lua:3-6`: "Castbar canvas panel. Pure schema: every widget is a row in" /
    "KickCD.Settings.Schema; the builder just calls Helpers.RenderUnitPanel," / "which draws the Unit
    picker as the page banner and then hands the rows to" becomes "The Grid page's Cast bar entry
    (KickCD#33). Pure schema: every widget is a row in" / "KickCD.Settings.Schema; the Grid page
    (settings/Grid.lua) draws it through" / "Helpers.RenderGridPage: the Unit band, the rail, then
    the rows handed to".
  - `settings/Label.lua:3`: `-- "Text Label" canvas panel.` becomes
    `-- The Grid page's "Text Label" entry (KickCD#33).` The header's last line, `-- RenderUnitPanel.`,
    becomes `-- RenderUnitPanel, under the Grid page's rail.`

- [ ] **Step 4: The slash answer.** In `settings/Slash.lua`, replace `local RETIRED_RESET_PAGES = { …
  }` and the `if RETIRED_RESET_PAGES[lowered] then … end` block in `runReset` with:

```lua
-- Where each old page's reset went. Icons, Cast bar and Text Label are entries of the
-- Grid page (KickCD#33), whose Defaults restores the entry for the unit in the band.
local RETIRED_RESET_PAGES = {
    general = "the General page's |cFFFFFF00Defaults|r button to reset the whole page",
    icons   = "Grid \226\134\146 Icons' |cFFFFFF00Defaults|r button to reset that section for the unit in the band",
    castbar = "Grid \226\134\146 Cast bar's |cFFFFFF00Defaults|r button to reset that section for the unit in the band",
    label   = "Grid \226\134\146 Text Label's |cFFFFFF00Defaults|r button to reset that section for the unit in the band",
}
```

  and

```lua
        local where = RETIRED_RESET_PAGES[lowered]
        if where then
            out(("`/kcd reset %s` is gone \226\128\148 `reset` now takes a setting path. "):format(lowered)
                .. "Use " .. where .. ", or |cFFFFFF00/kcd reset <path>|r for one setting (try /kcd list).")
            return
        end
```

  In the comment above them, "every schema-driven page here already carries a Defaults button that
  resets it (settings/General.lua, Icons.lua, Castbar.lua, Label.lua all wire one)" becomes "every
  schema-driven page here already carries a Defaults button: settings/General.lua's, and
  settings/Grid.lua's, which resets the entry on screen for the unit in the band".
  `tests/test_slash.lua`'s "the old page-shaped reset names its replacement" keeps passing, since each
  answer names "Defaults".

- [ ] **Step 5: Comments and TOC notes that count or name the pages.**
  - `settings/OptionsSetup.lua` (~:384): the sentence ending "…it is now called by all six of this
    addon's pages rather than four." becomes "…every page this addon registers calls it."
  - `settings/Panel.lua` (~:362-365): "six builders" becomes "four builders (General, Grid, Spells,
    Profiles)".
  - `settings/General.lua:214`: "Icons / Cast bar / Text Label pages" becomes "Grid page's Icons,
    Cast bar and Text Label entries".
  - `KickCD.toc`: in the note above `settings\OptionsSetup.lua`, "the per-tab files
    General/Icons/Castbar/Label" becomes "the page and entry files General/Icons/Castbar/Label/Grid".
    The note above `settings\Panel.lua` stays: Icons.lua and Castbar.lua still call `AddComposed` at
    file scope.
  - `crlf` all four.

- [ ] **Step 6: Run and see it pass.** Rerun Step 2's commands. Expected: 0 `FAIL`. Then:

```sh
grep -rnE '__panelFor\("(icons|castbar|label)"\)|KickCD(Icons|Castbar|Label)Panel|categoryFor\.(icons|castbar|label)' settings core modules tests   # expect no output
```

- [ ] **Step 7: Docs.** Insert rows as their own lines, and `git diff` each table.
  - `docs/settings-panel.md`:
    1. "## The pages": "Six pages sit under **Ka0s KickCD**" becomes "Four pages sit under **Ka0s
       KickCD**". In the page table, the **Icons**, **Cast bar** and **Text Label** rows become one
       row:
       `| **Grid** | Three entries on a nav rail under the **Unit** picker (Target / Focus): **Icons** (icon size, grid layout, ready and not-ready looks, borders, cooldown text and charges, tooltips, the ready glow), **Cast bar** (turn it on, place it, size it, its direction, a font, and separate colors for casts you can and can't interrupt) and **Text Label** (a custom identity label on a unit's icon grid or cast bar: its text, where it attaches, its offset, alignment, rotation and font). |`
       The paragraph under it, "On the Icons, Cast bar and Text Label pages, the unit picker above the
       tabs scopes the whole page.", becomes "On the Grid page, the Unit picker above the rail and the
       tabs scopes every entry."
    2. "## The tab strip" table: the rows `| **Icons** |`, `| **Cast bar** |` and `| **Text Label** |`
       become `| **Grid → Icons** |`, `| **Grid → Cast bar** |` and `| **Grid → Text Label** |`.
       "Counts are **per unit** on the three unit-scoped pages" becomes "Counts are **per unit** on
       the Grid page's three entries".
    3. "### Cast bar: what moved, and why": "This page renders through `Helpers.RenderUnitPanel`"
       becomes "This entry renders through `Helpers.RenderUnitPanel` (under the Grid page's rail)".
    4. "## Per-unit pages (Icons / Cast bar / Text Label)" becomes "## The Grid page's entries (Icons /
       Cast bar / Text Label)". Its first sentence becomes "These three render through
       `Helpers.RenderGridPage`, which hands each to `Helpers.RenderUnitPanel(ctx, panelKey, afterGroup,
       chrome)` (`settings/Panel_Render.lua`). That call does three things in this order, and the
       order matters. The Grid page's rail goes in through `chrome`, between the first and the other
       two:". In item 1, "**The selection is shared by all three pages" becomes "**The selection is
       shared by all three entries". The sentence "Selecting a unit therefore publishes a
       **structural** `Helpers.RefreshAllPanels` rather than re-rendering the one page — the other two
       are now showing the wrong unit, and the hidden ones are marked dirty so they repaint on their
       next `OnShow`." becomes "Selecting a unit publishes a **structural** `Helpers.RefreshAllPanels`:
       the Grid page re-renders on the new unit and keeps its entry and tab, and a hidden page is
       marked dirty so it repaints on its next `OnShow`." In the General-link paragraph, "That is what
       lets the control reach the three unit pages from another page at all." becomes "That is what
       lets the control reach the Grid page from another page at all."
  - `docs/module-map.md`: the entries for `Icons.lua`, `Castbar.lua` and `Label.lua` (:259-290) now
    say "Grid entry" where they said "canvas panel" or "page". Update :223-229, :267, :278, :372-374
    and :442-443 wherever they call Icons, Cast bar or Text Label a page.
  - `docs/schema.md:196`: the page it names among the three becomes "Grid → <entry>".
  - `README.md`: every settings breadcrumb that starts at a retired page gains Grid:

```sh
grep -nE '(Icons|Cast bar|Text Label) (→|->)|(Icons|Cast bar|Text Label) page' README.md
```

    Each hit about the settings tree becomes `Grid → Icons → …` (and so on), including :34, :69, :71,
    :75, :79, :91 and :111. Run the README changes through the `humanize` skill before committing.
  - `docs/smoke-tests.md`:
    1. In the suite index (:21-58), add a row for #36.
    2. #22 Text label (:609-636): "open the Text Label page" becomes "open Grid → Text Label".
    3. The unit/tab checks (:332-345), the resets (:481, :485), the focus-link checks (:521-530) and
       :1048 name Grid entries where they named pages.
    4. Append `## 36. The Grid page (KickCD#33)`, in the heading style of #35, with a sentence saying
       the owner fills Result, and the table of KC-S1 … KC-S11 copied verbatim from
       `Ka0sAddonsCommonTasks/docs/2026-09-26-NAVRAIL_ADOPTION/06_SMOKE_TESTS.md`, with an empty
       Result column. "When to run which subset" (:1123) gains "#36 after any change to
       settings/Grid.lua, settings/Panel_Render.lua or the three entry files".

  `crlf` every doc edited.

- [ ] **Step 8: Gate, inventory.** Run the addon gate and the lizard line: 0 FAIL, 0/0, no lizard
  output, no `EOL FAIL`. Regenerate `docs/test-cases.md`. The case count stays 1201: no case was
  added or deleted, and no case title changed. If the count moved, set the badge. Then check
  citations:

```sh
grep -rnE 'settings/(Icons|Castbar|Label|Panel_Render|Panel_Widgets)\.lua:[0-9]+' docs README.md | head -40
```

  Every hit must still point at its named symbol. Fix any that moved.

- [ ] **Step 9: Commit.**

```sh
git add settings/Icons.lua settings/Castbar.lua settings/Label.lua settings/Slash.lua settings/OptionsSetup.lua \
  settings/Panel.lua settings/General.lua KickCD.toc tests/test_options_panel.lua \
  docs/settings-panel.md docs/module-map.md docs/schema.md docs/smoke-tests.md docs/test-cases.md README.md
git status --porcelain                  # expect empty
git commit -m "NR-KC-04: Retire the Icons, Cast bar and Text Label pages; the tree is General, Grid, Spells, Profiles" \
  -m "KickCD#33. The three files keep their rows and their Grid entry registration and lose their builders, so no schema row, path or default moves. /kcd reset icons|castbar|label now points at Grid -> <entry>'s Defaults for the unit in the band. The panel tests reach Cast bar through the Grid page; comments, TOC notes, the settings-panel doc, the module map, the README's breadcrumbs and smoke-tests #36 follow." \
  -m "$TRAILERS"
```

(Add any other doc whose citations the gate moved.)

### M2 checkpoint

Run after NR-MM-04 and NR-KC-04 exist (`./resume-state.sh M2` prints `M2: 6/6 COMPLETE`). In each of
MultiMeters and KickCD, on the branch head: `git status --porcelain` is empty; the addon gate reports
0 FAIL and luacheck 0/0; the lizard line from the command shorthands prints nothing; and
`grep -m1 -E 'Tests-[0-9]+%2F[0-9]+' README.md` equals the run's PASS count over its total.

Expected totals: MultiMeters 2091, KickCD 1201. Append one row to `checkpoints.tsv`, `M2`, with both
heads, totals, the lizard result, "not pushed (not authorized)", and the smoke checks left for the
owner.

---

## M3 — record

### Task NR-REC-01: the execution record

**Files:**
- Create: `99_REPORT.md` in this bundle. Modify: `checkpoints.tsv` (the M3 row; M1 and M2 were logged
  at their checkpoints, uncommitted until this task), and `06_SMOKE_TESTS.md` if the owner's results
  have arrived. The rest of the bundle was committed before M1 and is not edited.

**Interfaces:** reads git in the ten repos and this bundle. Writes this bundle only, on `main`.

- [ ] **Step 1: Collect the state.**

```sh
cd $GIT/Ka0sAddonsCommonTasks/docs/2026-09-26-NAVRAIL_ADOPTION
./resume-state.sh -v                    # expect M1 10/10, M2 6/6, M3 0/1, READY: NR-REC-01
for a in AbsorbTracker BankLedger ConsumableMaster KickCD LootHistory MultiMeters PanelMaster PartyFrameEnhanced PrettyChat WhatGroup; do
  print -- "== $a"; git -C $GIT/$a log --oneline master..$BR
done
```

- [ ] **Step 2: Write `99_REPORT.md`** in the SETTINGS_REDESIGN `99_REPORT.md`'s shape, LF, with
  these sections:
  1. **Outcome:** what shipped per repo, on which branch head, and that nothing was pushed, merged,
     tagged or version-bumped.
  2. **Commits:** a table of id -> repo -> commit (short hash) -> subject, from Step 1. It includes
     every `R` review fix.
  3. **Gates:** each addon's M1 totals, and MultiMeters' and KickCD's M2 totals, luacheck and lizard,
     copied from `checkpoints.tsv`.
  4. **Deviations from the plan:** each place execution departed from `03_EXECUTION_PLAN.md`, with
     the commit that shows it. The plan is not edited.
  5. **Follow-ups**, one line each with where it would be filed. Nothing is filed by this task:
     - AuraMaster: the clean-up issue for leftover sub-page wording and dead code (Text.lua's
       `pageDim` and its unreachable `ctx.__renderDisabled` read). The SETTINGS_REDESIGN run could not
       file it. Record whether the launching session filed it, with the issue number, or that it is
       still owed.
     - MultiMeters#55 and KickCD#33: the "ready once v1.61.0 is published" comments owed from
       SETTINGS_REDESIGN, and the new state (built on the branch, not merged). Record whether each was
       commented.
     - MultiMeters: the header gear (`modules/HeaderControls.lua`'s `settings` action) could open
       Windows on the gear's window with `NS.OpenOptionsPage("windows")` instead of the main panel
       (02_SPEC R3).
     - WowAddonStandards: options-ui-§13 could state the Defaults scope for a railed page whose band
       picks one of several instances, as KickCD's deviation row asks (02_SPEC R8).
  6. **Owner smoke:** RV-S1, MM-S1 … MM-S11 and KC-S1 … KC-S11 are unrun and unmarked. The owner
     fills `06_SMOKE_TESTS.md`.
  7. **Finalize:** what `/wow-addon:finalize` would merge (ten feature branches), once the owner says
     go.

- [ ] **Step 3: The M3 row.**

```sh
printf '%s\tM3\t%s\n' "$(date +%F)" "NR-REC-01: 99_REPORT.md and these rows committed on main (not pushed). resume-state.sh -v before the commit: M1 10/10, M2 6/6, M3 0/1 (NR-REC-01 READY); all ten trees clean. Smoke checks unrun, unmarked (owner)." >> checkpoints.tsv
```

- [ ] **Step 4: Commit** (on `main` in Ka0sAddonsCommonTasks, this bundle's files only). The whole
  directory is staged, so the M1 and M2 checkpoint rows, the M3 row and anything else the run wrote
  here (`exceptions.tsv`, owner smoke results) land together. `git diff --cached --stat` must show no
  change to `00_OVERVIEW.md`, `02_SPEC.md`, `03_EXECUTION_PLAN.md`, `items.tsv`, `resume-state.sh` or
  `RESUME.md`: the frozen plan was committed before M1.

```sh
cd $GIT/Ka0sAddonsCommonTasks
git add docs/2026-09-26-NAVRAIL_ADOPTION
git diff --cached --stat                # expect 99_REPORT.md, checkpoints.tsv (+ exceptions.tsv, 06_SMOKE_TESTS.md if written)
git commit -m "NR-REC-01: Execution record for the NavRail adoption (v1.61.0 in ten addons, MM#55, KC#33)" \
  -m "99_REPORT.md: commits per repo, gate figures, deviations, follow-ups (the AuraMaster clean-up issue, the MultiMeters header gear, the options-ui-§13 Defaults question) and the owner's open smoke checks. The M3 checkpoint row. Nothing pushed." \
  -m "$TRAILERS"
./docs/2026-09-26-NAVRAIL_ADOPTION/resume-state.sh        # expect M3: 1/1 COMPLETE
```
