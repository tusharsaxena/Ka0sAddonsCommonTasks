# AuraMaster settings redesign (#6) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:subagent-driven-development. This plan is
> executed by a Workflow with one implementer and one independent reviewer per task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fold AuraMaster's Filters, Layout, Bars, Icons and Text sub-pages into its Containers page.
The result is one config page per container: the container band on top, a pinned nav rail on the left
(General · Filters · Layout · <the container's style>), and the selected section's own pinned tab strip
to its right, over the one scroll. The library seam and the standard's rule that make this legal land
first.

**Architecture:** LibKa0s-Options gains a sixth file, `OptionsNav.lua` (OptionsNav minor 1). It holds
`O.NavRail(ctx, spec)` and one inset function, `lib.__railInset(ctx)`, which the tab strip's placement,
the content panel's left edge and the scroll's left anchor all read. With no rail the inset is 0, so
every other page is laid out byte-identically. AuraMaster keeps its schema untouched: a rail section *is*
a former page key, rendered by the existing `Helpers.RenderPage` with that page's spec. The Containers
page's renderer draws the band, then the rail, then the section. Per-section tab memory, the style heal,
deep links and Defaults are host state around it. The standard (options-ui-§2, §13, §14) sanctions the
rail as a first level before any of it ships.

**Tech Stack:** Lua 5.1 (WoW client), Ace3 (AceGUI-3.0), LibStub, LibKa0s (vendored), and the headless
kit (`tests/run.lua`, LibKa0s test kit revision 27). Tooling: luacheck, lizard, zsh, git.

**Spec:** `/mnt/d/Profile/Users/Tushar/Documents/GIT/AuraMaster/docs/superpowers/specs/2026-09-26-settings-redesign-design.md`,
committed on AuraMaster's branch `feat/2026-09-26-settings-redesign` (`3fdc667`). Read it whole before
any task. Reference implementation: `git -C ../AuraMaster show d0d0196:settings/LayoutLab.lua`, Test10,
lines 665-830. It is a lab that is never merged or copied: it moves `ctx.body` from outside, and this
plan replaces that with the library seam.

---

## Global Constraints

Every task honors every line here. A reviewer rejects a task that breaks one.

- **Rail width 120.** `O.NavRail`'s default `spec.width` is `120`, which is Test10's `NAV_W`. AuraMaster
  passes no width.
- **Draw order is PageBanner -> NavRail -> TabStrip**, on every full render of a railed page.
  `NavRail` reads `ctx.__bannerHeight` (the band the banner reserved), and `TabStrip` reads the inset
  `NavRail` recorded.
- **Rail width 0 (or no rail) is byte-identical to today.** `lib.__railInset(ctx)` answers `0` for
  `ctx.railWidth` nil or <= 0. The strip, the content panel and the scroll then compute exactly the
  numbers they compute at LibKa0s v1.60.0.
- **Schema paths unchanged.** No row's `path`, `page`, `group`, `default` or `label` changes. A
  section key *is* the former page key (`"containers"`, `"filters"`, `"layout"`, `"bars"`, `"icons"`,
  `"text"`). `/am set`, `/am get`, `/am list` and every reset are untouched.
- **Session state is never persisted.** `ctx.activeSection`, `ctx.activeTab` and `ctx.sectionTabs`
  live on the ctx only. Nothing about the rail or the tabs is written to `AuraMasterDB`
  (options-ui-§13).
- **1500-line file cap** (layout-§1) in every repo touched. Tighter budgets: `LibKa0s/Options.lua`
  stays **<= 1474** lines and `LibKa0s/OptionsTabs.lua` **<= 1494** (their CLAUDE.md re-check triggers
  are 1475 and 1495). Neither gains a new `O.*` member. Every new member goes in `OptionsNav.lua`.
  AuraMaster's `settings/OptionsSetup.lua` (554 today) stays under 1500.
- **CCN 15.** No function above cyclomatic complexity 15 (lizard).
- **luacheck 0/0** in every Lua repo, at every commit.
- **Line endings.** LibKa0s and AuraMaster pin `* text=auto eol=crlf`, so every file written there,
  new ones included, is **CRLF**: `test "$(grep -c $'\r$' F)" = "$(wc -l < F)"` for each written
  file `F`. WowAddonStandards pins **LF**: `tr -dc '\r' < F | wc -c` prints `0`. This bundle is LF.
- **Bounded runner.** Every `lua`, `luacheck` and `lizard` run goes through
  `/home/tushar/.claude/wow-addon/bin/ka0s-bounded`. A PreToolUse hook blocks unbounded runs.
- **No version bumps of addons.** AuraMaster's TOC `## Version`, README badges and version history are
  not touched. No CurseForge anything.
- **LibKa0s is released as a LOCAL tag `v1.61.0`, never pushed.** It is an annotated tag on SR-LK-03's
  second (and last) commit, on the feature branch; the Consumers re-sweep runs before the first
  release commit, so nothing is ever committed after the tag. `master` is not touched. A tag is never re-cut: a defect found
  later ships as `v1.61.1`.
- **One branch name in all three repos: `feat/2026-09-26-settings-redesign`.** WowAddonStandards and
  LibKa0s cut it from `master` (`2854053` and `bed0eb1` at planning time, so verify before cutting).
  AuraMaster already has it (`3fdc667`, the spec).
- **Pushes only if the owner authorized them at plan review**, and only at milestone checkpoints:
  feature branches plus `refs/notes/ka0s-review`, never a tag. **Never merge** into `master` or `main`.
  `/wow-addon:finalize` runs later, on the owner's explicit go-ahead.
- **Commits.** One task per commit (SR-LK-03 makes two, as `docs/releasing.md` step 7 requires). The
  subject starts `<ID>: `, and review fixes are `<ID>R: `. Messages end with the session's attribution
  trailers. Stage named files only (`git add <path> ...`), never `git add -A` or `.`.
- **Every commit is green:** its repo's full gate passes on the committed tree. A task that cannot get
  green stops and reports. It never commits red.
- **In-client smoke checks are the owner's.** Claude writes them. Only the owner marks one passed.
- **US English, and `filename-§N` references only** (documentation-§6, WowAddonStandards `CLAUDE.md`).
  README edits go through the `humanize` skill before commit.
- **Read-only elsewhere.** No task touches MultiMeters, KickCD or any other addon. AuraMaster's `libs/`
  and `tests/_kit/` change only by the SR-AM-01 re-vendor copy.

### Command shorthands used below

```sh
GIT=/mnt/d/Profile/Users/Tushar/Documents/GIT
B=/home/tushar/.claude/wow-addon/bin/ka0s-bounded
```

**LibKa0s gate** (run in `$GIT/LibKa0s`):

```sh
$B lua tests/run.lua > /tmp/lk-run.txt 2>&1; tail -3 /tmp/lk-run.txt; grep -c '^  FAIL' /tmp/lk-run.txt   # expect 0 FAIL lines
$B luacheck .                                                        # expect 0 warnings / 0 errors
$B lizard -l lua -C 15 -w .                                          # expect no output (whole repo: the new suites too)
```

**AuraMaster gate** (run in `$GIT/AuraMaster`):

```sh
$B lua tests/run.lua > /tmp/am-run.txt 2>&1; tail -3 /tmp/am-run.txt; grep -c '^  FAIL' /tmp/am-run.txt   # expect 0 FAIL lines
$B luacheck .                                                                 # expect 0 warnings / 0 errors
$B lizard -l lua -C 15 -w -x "./libs/*" -x "./tests/_kit/*" .                 # expect no output
```

The kit prints each case as `  PASS  <name>`, `  FAIL  <name>` or `  SKIP  <name>`. "Run it and see it
fail" below means: run the repo's `lua tests/run.lua` through `$B` and grep the named cases:
`grep -E '^  (FAIL|PASS)  <prefix>' /tmp/<repo>-run.txt`. The kit has no per-suite filter.

**WowAddonStandards docs gate** (run in `$GIT/WowAddonStandards`, over the `.md` files changed versus
`master`). The session shell is **zsh**, which does not word-split an unquoted `$F`: a scalar holding
several newline-joined paths would reach `grep` as ONE path and make check (1) pass having checked
nothing. So `F` is a zsh **array**, one element per changed file, and an empty list prints a FAIL
line instead of running checks that would pass on nothing:

```sh
F=(${(f)"$(git diff --name-only master -- '*.md')"})
if (( ${#F} == 0 )); then echo "NO CHANGED .md FILES -- the gate checked nothing (a FAIL)"; else
print -l -- $F                                           # the files checked, one per line
# (1) every filename-§N resolves: the file exists under standards/standards/ and has a "### N." heading
for ref in $(grep -ohE '\b[a-z][a-z-]*-§[0-9]+' $F < /dev/null | sort -u); do
  f=${ref%-§*}; n=${ref#*-§}; p=standards/standards/$f.md
  [[ -f $p ]] && grep -qE "^### $n\." $p || echo "UNRESOLVED $ref"
done                                                     # expect no output
# (2) every relative link resolves ((…) placeholders excluded)
for md in $F; do d=$(dirname $md)
  grep -oE '\]\([^)#:]+' $md | sed 's/^](//' | grep -v '^…$' | while read -r l; do
    [[ -e $d/$l ]] || echo "BROKEN $md -> $l"; done
done                                                     # expect no output
for md in $F; do printf '%s ' $md; tr -dc '\r' < $md | wc -c; done   # (3) expect 0 each
git diff --check master                                  # (4) expect no output
fi
```

Check the block is splitting before trusting a clean run: `print -l -- $F | wc -l` must equal
`git diff --name-only master -- '*.md' | wc -l` (two at SR-WS-01's gate; seven at SR-WS-02's, its five plus SR-WS-01's two). Run it in
zsh as written; under bash, `(f)` is a syntax error, so the block fails loudly rather than passing.

---

## Review Focus

These are the five failure modes a player is likeliest to hit that no test pins today. Each one gets
a test in the task that owns it. A reviewer checks that the test exists, fails without the fix, and
passes with it.

1. **The first open after `/reload` stacks every tab vertically beside the rail.** The first page
   render happens before the canvas has a width, so `frameWidth` falls back to `TAB_MIN_W` (60). A rail
   inset of 132 would leave a negative usable width, and a resize that re-placed against the full width
   would draw the tabs under the rail. Owned by **SR-LK-01**, test "nav: the first render's zero-width
   chrome re-places the strip, inset included, when the width arrives".
2. **Returning to a section forgets its tab.** A strip click is handled inside the library
   (`OptionsTabs.lua:1472-1478`: it sets the scalar `ctx.activeTab` and re-renders the strip only), so
   the host never sees it. A host that stashed the tab only on its own renders loses
   Filters -> Categories after a trip to Layout (smoke 5). Owned by **SR-AM-03**, test "rail: each
   section keeps its own tab ...".
3. **A Style change strands the page on a section the rail no longer lists, or drops it to General.**
   Bars -> Style = Icons must land on Icons, and Filters must stay Filters (spec §3, smoke 4). Owned by
   **SR-AM-03**, test "rail: a Style change heals an active style section ...".
4. **Defaults resets the wrong rows.** `EnsureDefaultsButton` (`Options.lua:790-825`) captures
   `panel.defaultsOnClick` once, at the first show. A closure that captured the section at build time
   would reset General's rows from Layout (smoke 6). Owned by **SR-AM-04**, test "rail: Defaults
   restores only the active section's rows ...".
5. **The frame picker returns the player to the wrong place.** `settings/Layout.lua:501` reopens with
   `NS.OpenOptionsPage("layout")`. After SR-AM-05 there is no Layout category, and the Containers panel
   is hidden while the picker runs, so the section must be selected on a hidden (dirty) page and drawn
   on its next show (smoke 7). Owned by **SR-AM-04**, test "rail: a former sub-page key opens Containers
   on that section ...". That test selects the section while the kit panel is hidden and asserts the
   next show draws it. `test_pages_layout.lua`'s picker case keeps pinning that the reopen asks for
   `"layout"`.

The combat lock over the rail (smoke 8) is pinned in SR-LK-01's combat case: the cover's level sits
above the rail and its entries, and a rail click in combat does nothing. The pool reuse is pinned in
SR-LK-01 too.

---

## Spec ambiguities and how this plan resolves them

| # | Where | Resolution |
|---|---|---|
| A1 | Spec §4: "like a tab click it carries no combat guard of its own" | Tab clicks **do** refuse in combat, inside the library (`OptionsTabs.lua:952`, `refused()`). The rail does the same: its `OnClick` asks `O.__combatRefused()`. "Of its own" means no **host** guard. |
| A2 | Spec §2/§4: the alignment is "measured after the strip is drawn … from the drawn tab's textures" | **A deviation from the spec's mechanism, not its outcome, and it needs the owner's sign-off at plan review** (`00_OVERVIEW.md`, "Needs the owner's sign-off"). The lab's deferred `GetRegions` scan took the **highest** shown art, which is the selected tab's `Options_Tab_Active_*` cap. The library measures that atlas directly on a probe texture, as `tabArtHeight()` already measures the inactive one (`OptionsTabs.lua:279-295`), because the library has already ruled that reading art back off a drawn tab is a defect: `OptionsTabs.lua:380-383` ("reading it back off a tab drawn in whichever state it happened to be in is the defect this file's atlas section describes"). The rail's top is `-(bannerHeight + TAB_H - activeArtHeight)`: measured at draw time, never hard-coded, and pure enough to pin. The first row's top does not depend on width, so no resize re-measure is needed. The spec's §4 test ("the alignment measurement with a stub texture set") is SR-LK-01's "nav: the probe's cap is the drawn selected tab's own art …", which draws the strip and pins that the probe's number equals the drawn selected tab's art height and that the rail's top follows it. UI scale moves the atlas and the drawn art together, so they cannot part there; smoke S2 is the in-client check. **If the owner rejects A2**, SR-LK-01 instead adds `lib.__alignRail(ctx, artH)` to `OptionsNav.lua`, called at the end of `placeTabs` (OptionsTabs minor 5, guarded) with the tallest `__ka0sTabArt.left:GetHeight()` among the first row's buttons (`p.y == top`), which re-anchors the rail's TOPLEFT; the probe stays as the pre-strip value, and the test above asserts the re-anchored top instead. |
| A3 | Spec §4: "pooled per ctx … released on the next render" | `NavRail` releases its own pool on every call, as `TabStrip` releases its own. `ClearScroll` must not release it, because the rail is chrome and not scroll content. `releaseChrome` is not touched. |
| A4 | Spec §4: "railWidth + gap" gives no gap | `RAIL_GAP = 12` reproduces Test10 exactly. The tabs and the scroll start at body x 144, and the content panel's left edge sits 4px right of the rail's right edge (136 vs 132). The rail's bottom is `PANEL_BOTTOM` (2) above the body's foot, level with the content panel's (the lab used 4). |
| A5 | Where the rail's constants live | They are file-local in `OptionsNav.lua`, not `lib.LAYOUT` and not `O.*`. `tests/test_options.lua:1035-1068` reads `Options.lua` alone for `-- INTERNAL:` annotations, so a LAYOUT key would cost lines in a file at its budget. A published `O.RAIL_W` would also enter every host's parity ignore list. So no options-ui-§8 table row is added. |
| A6 | Spec §3: `ctx.activeTab` per section (a table) | The library keeps one scalar `ctx.activeTab`. The host keeps `ctx.sectionTabs[section]` and stashes the scalar into it **before anything moves the section** (a rail click, a deep link, a render). That catches the library's own strip clicks too. `RenderTabbedSchema` does not change. |
| A7 | Spec §3 Defaults vs options-ui-§13 :320 ("stays page-wide … MUST NOT narrow to the visible tab") | The spec (frozen by the owner) wins, and the standard is extended. On a railed page the blast radius is the **active rail entry**, which is the set the folded sub-page's own button restored, and it still never narrows to the visible tab. SR-WS-01 adds that sentence. Spec §5 did not list it. |
| A8 | The Defaults tooltip: `EnsureDefaultsButton` captures `panel.defaultsTooltip` once | One section-neutral wording (a new locale string), not a per-section tooltip. The click handler is a closure reading `ctx.activeSection` at click time. No library change. |
| A9 | Spec §6 deep links: what `NS.OpenOptionsPage("containers")` does | It opens Containers and **keeps** the section the player left (`modules/Anchors.lua:750`'s right-click means "this container", not "General"). Any other section key selects that section, and a style key the container is not drawn in selects nothing and still opens Containers. |
| A10 | Spec §6: "`Helpers.SelectTab` gains a section-aware path" | The host wraps the library's `SelectTab`. A registered section key routes to `Helpers.SelectSection(key, tabKey)`, and anything else goes to the library. `settings/Filters.lua:278-279` (General -> Spell Categories) is unchanged and still reaches the library. |
| A11 | Rail order | A fixed `SECTION_ORDER` in `settings/OptionsSetup.lua`, not TOC order. Filters..Text's TOC positions become Conventional. General stays load-bearing before Containers, for the tree order. |
| A12 | No containers at all | The rail lists **General** only (the other sections need a container). General draws its existing "No containers yet. Click New container, or type /am new." line. |
| A13 | Rail entry tooltips (spec entries carry `tooltip`; the lab had none) | Six new locale strings, one per section, passed as `spec.tooltip` at registration. |
| A14 | Test seam "`Helpers.__pageCtx` gains the section seam" | After SR-AM-05 every section key aliases the Containers ctx (`__pageCtx.filters == __pageCtx.containers`). `tests/page_helpers.lua`'s `P.show("Filters")` selects the section and shows Containers. Most page suites keep their shape. |
| A15 | Text.lua's `pageDim` (`settings/Text.lua:141-147`) reads `ctx.__renderDisabled`, which is now always false for the Text section | Left in place: correct, and harmless. Removing it is outside spec §6. SR-REC-01 files it as a follow-up issue (a dead-code sweep). Its one test (`test_pages_text.lua:208`, graying on a bars container) is unreachable and is deleted in SR-AM-05. |
| A16 | The Style row's tooltip says "Bars, Icons and Text each have their own settings page" | Reworded in SR-AM-05 to "… each have their own section on this page". This is a `desc` fix, not a label or behavior change. |
| A17 | Only AuraMaster takes v1.61.0 | This matches v1.59.0's precedent (`docs/releasing.md`, "Every step 8"). The other ten hosts stay on v1.60.0, and each one's stub gains `NavRail` when it re-vendors. SR-LK-01 Step 7 writes that into the v1.61.0 CHANGELOG block's "What a consumer owes on re-vendoring v1.61.0" section, in the same commit as the code. SR-LK-02 does not touch `CHANGELOG.md`. |

---

## Task index

| ID | Repo | Title | Depends on |
|---|---|---|---|
| SR-WS-01 | WowAddonStandards | options-ui-§2/§13/§14 sanction the nav rail; v2.69.0 header, changelog, index blurb | — |
| SR-WS-02 | WowAddonStandards | Ripple: EXECUTIVE_SUMMARY, NEW_ADDON_CONTEXT, AUDIT.md (g)/(i), library-stack, README | SR-WS-01 |
| SR-LK-01 | LibKa0s | OptionsNav minor 1 (`O.NavRail`, `lib.__railInset`), Options 25, OptionsTabs 5, tests, versioning docs | — |
| SR-LK-02 | LibKa0s | Prose and census: README, CLAUDE.md, releasing.md (the CHANGELOG block, consumer note included, is SR-LK-01's) | SR-LK-01 |
| SR-LK-03 | LibKa0s | Release v1.61.0: dated block, pointers, release battery, ANALYSIS, local annotated tag | SR-LK-02, SR-WS-02 |
| SR-AM-01 | AuraMaster | Re-vendor LibKa0s v1.61.0; stub gains `NavRail` | SR-LK-03 |
| SR-AM-02 | AuraMaster | The section registry and the style gates as data (Diagnostics) | SR-AM-01 |
| SR-AM-03 | AuraMaster | The Containers page renderer: band, rail, section; per-section tabs; style heal | SR-AM-02 |
| SR-AM-04 | AuraMaster | Deep links, `SelectSection`, the `SelectTab` route, Defaults for the active section | SR-AM-03 |
| SR-AM-05 | AuraMaster | Retire the sub-pages: sections only, drop the disabled notice and D6, locale, TOC, test migration | SR-AM-04 |
| SR-AM-06 | AuraMaster | Docs: settings-panel, ARCHITECTURE, module-map, common-tasks, README, smoke-tests, test-cases | SR-AM-05 |
| SR-REC-01 | Ka0sAddonsCommonTasks | Execution record: `99_REPORT.md`, checkpoint rows, follow-up issues | SR-AM-06 |

M1 = SR-WS-01, SR-WS-02, SR-LK-01, SR-LK-02 and SR-LK-03. The two repos run in parallel, and
SR-LK-03 waits on SR-WS-02. M2 = SR-AM-01..06, one at a time. M3 = SR-REC-01.

---
## M1 — upstream

### Task SR-WS-01: options-ui sanctions the nav rail (v2.69.0)

**Repo:** `$GIT/WowAddonStandards`, branch `feat/2026-09-26-settings-redesign` cut from `master`.

**Files:**
- Modify: `standards/standards/options-ui.md`: §2 bullet at :84; §13 bullets at :317 (insert after it),
  :319 and :320; §14 at :326, :332 (insert after it) and :344.
- Modify: `standards/STANDARDS.md`: header :1, changelog (a new entry above :99), the options-ui
  blurb at :60.

**Interfaces:**
- Consumes: nothing. The rail is described by behavior, and the API name `O.NavRail` is the one SR-LK-01
  publishes (LibKa0s-Options key 25.31.5.7.4.1).
- Produces: the rule text SR-WS-02 ripples, and the standard version **v2.69.0** that SR-LK-03 writes into
  LibKa0s's README pointer.

- [ ] **Step 1: Cut the branch and confirm the rule is absent.**

```sh
cd $GIT/WowAddonStandards
git status --porcelain                      # expect empty
git rev-parse --short master                # expect 2854053 (if it moved, cut from the new tip and note it in the commit body)
git switch -c feat/2026-09-26-settings-redesign master
grep -c 'nav rail' standards/standards/options-ui.md    # expect 0
head -1 standards/STANDARDS.md              # expect: # Ka0s WoW Addon Standard (v2.68.0, 2026-09-26)
```

- [ ] **Step 2: options-ui-§2 (:84), the cover names the rail.** Make two in-line replacements in the
  bullet that starts `- **A page shown in combat is LOCKED.**`:
  - `the header band and the tab strip included` → `the header band, the nav rail and the tab strip included`
  - `and tab switches (options-ui-§13)` → `and tab and rail switches (options-ui-§13)`

- [ ] **Step 3: options-ui-§13, insert a new bullet directly after :317.** :317 is the bullet that
  starts `- **A secondary strip is permitted inside one primary tab, and it lives in the scroll.**`,
  and it stays untouched. Insert this as its own line:

```markdown
- **A nav rail is permitted as a first level, on a page that edits one instance out of many (options-ui-§14).** Where the settings for that instance would otherwise be several sub-pages retargeted by one picker, the page **MAY** fold them into itself and choose among them with a **nav rail**: a pinned vertical list at the body's left, drawn by the library (`O.NavRail`), one entry per folded page, and visibly unlike the tab strip — a list on the left for the first level, tabs on top for the second. The rail is the **first** level and the pinned primary strip, drawn to its right, is the **second**: each entry's strip is that entry's sections, one tab per `group` as above, over the page's one scroll, and only the scroll moves. Rail plus strip is two levels, so the third-level ban above counts the rail: a page with a rail **MUST NOT** also divide a tab with a secondary strip. The rail's selection is session state and **MUST NOT** be persisted, and the active tab is kept **per rail entry**, so returning to an entry returns to the tab you left. A rail click is a structural re-render, refused in combat by the library exactly as a tab click is, and a host adds no guard of its own. The rail's top is level with the top of the tab art beside it, measured, never a hard-coded offset.
```

- [ ] **Step 4: options-ui-§13 :319 and :320.**
  - In :319, replace `**The active tab is session state, per page, and MUST NOT be persisted.**` with
    `**The active tab is session state, per page (per rail entry on a page with a nav rail), and MUST NOT be persisted.**`
  - At the end of :320 (the bullet `- **The per-page Defaults button stays page-wide.** …`), append one
    sentence, with a space before it:
    `On a page with a nav rail its blast radius is the **active rail entry** — the set the folded sub-page's own button restored — and it still **MUST NOT** narrow to the visible tab.`

- [ ] **Step 5: options-ui-§14.**
  - At the end of :326 (`The band above the tab strip is where a page says what it is about. Two things
    belong there and nothing else does.`), append:
    ` Where the page draws a nav rail (options-ui-§13), the band spans the full width above **both** the rail and the strip.`
  - Insert a new bullet directly after :332 (the bullet `- **The selection survives a tab switch and a
    page change.** …`):

```markdown
- **The rail is not a picker.** On a page with a nav rail (options-ui-§13), the rail chooses which part of the selected instance is shown, never which instance: the banner stays the ONLY picker, a rail entry **MUST NOT** carry one, and changing instance **MUST** leave the rail's selection and each entry's tab alone, healing only an entry the new instance no longer offers.
```

  - At the end of the paragraph at :344 (`A page taking this escape has **one** band row and **one**
    `General` tab, …`), append:
    ` On a page with a nav rail, this escape's `General` is the rail's **FIRST entry**, named `General`, and the three conditions read with *entry* for *tab*: the band keeps the picker, `General` is first so the page opens on it, and no page-wide control is drawn under any other entry or tab.`

  Line numbers shift by one after Step 3's insert. Anchor on the quoted text, not the number.

- [ ] **Step 6: STANDARDS.md, the version and the changelog.**
  - Replace :1 with `# Ka0s WoW Addon Standard (v2.69.0, 2026-09-26)` (keep the date if execution is on
    2026-09-26; otherwise use the execution date in the header and in the entry below).
  - Insert as the first bullet under `## Changelog` (above the v2.68.0 entry), on one line:

```markdown
- **v2.69.0 (2026-09-26):** **A page that edits one instance out of many may fold its sub-pages into one page under a nav rail.** **The request.** The collection owner asked for AuraMaster's Filters, Layout, Bars, Icons and Text sub-pages to fold into its Containers page — one config page per container, the picker on top, two visibly different levels of navigation (AuraMaster#6; the design is AuraMaster's `docs/superpowers/specs/2026-09-26-settings-redesign-design.md`), with MultiMeters#55 and KickCD#33 to follow. options-ui-§13 had a secondary strip inside one primary tab and a ban on a third level, and no pinned first level at all. **The ruling.** options-ui-§13 sanctions a **nav rail** as the first level of such a page, drawn by the library (`O.NavRail`, `LibKa0s-Options-1.0` 25.31.5.7.4.1), with the primary strip as the second; the third-level ban now counts the rail, so a railed page draws no secondary strip. The rail's selection is session-only and the active tab is kept per rail entry; a rail click is locked in combat as a tab click is; the page's Defaults restores the active rail entry, the set the folded sub-page's own button restored. options-ui-§14 spans the band above both the rail and the strip, rules that the rail is not a picker, and reads the `General` escape as the rail's first entry. options-ui-§2's cover names the rail. **Ripple in** this file's options-ui blurb (which also drops a stale "single exemption" that contradicted options-ui-§13's two exempt pages), `EXECUTIVE_SUMMARY.md`, `NEW_ADDON_CONTEXT.md`, `AUDIT.md` checks (g) and (i), `library-stack.md`'s Options row and file count, and the root `README.md`.
```

- [ ] **Step 7: STANDARDS.md :60, the options-ui blurb.** Make three in-line replacements:
  - `header band and tab strip included` → `header band, nav rail and tab strip included`
  - `the AceConfig-rendered Profiles page the single exemption` → `the AceConfig-rendered Profiles page and the landing page the two exemptions`
  - `with a page's remaining page-wide acts moving to a `General` FIRST tab where they will not fit beside them` →
    `with a page's remaining page-wide acts moving to a `General` FIRST tab where they will not fit beside them; and, on a page that edits one instance out of many, a **nav rail** as a first level beside the strip — rail plus strip is two levels, never three, the rail is not a picker, and its selection and each entry's tab are session-only`

- [ ] **Step 8: Run the docs gate.** Use the "WowAddonStandards docs gate" block above. Expect no
  UNRESOLVED and no BROKEN, 0 CR bytes per file, and clean `diff --check`. Also:

```sh
grep -c 'nav rail' standards/standards/options-ui.md    # expect >= 6
head -1 standards/STANDARDS.md                          # expect v2.69.0
```

- [ ] **Step 9: Commit.**

```sh
git add standards/standards/options-ui.md standards/STANDARDS.md
git commit -m "SR-WS-01: options-ui sanctions the nav rail as a first level (v2.69.0)" \
  -m "options-ui-§13: a page that edits one instance out of many MAY fold its sub-pages under a nav rail (first level) beside the primary strip (second); the third-level ban counts the rail; the active tab is per rail entry; a railed page's Defaults restores the active entry. options-ui-§14: the band spans the rail and the strip; the rail is not a picker; the General escape is the rail's first entry. options-ui-§2 names the rail under the cover. STANDARDS.md: v2.69.0, changelog, blurb (drops the stale 'single exemption')." \
  -m "<attribution trailers>"
```

### Task SR-WS-02: the v2.69.0 ripple

**Repo:** `$GIT/WowAddonStandards`, same branch.

**Files:**
- Modify: `standards/EXECUTIVE_SUMMARY.md` :11 (version), :22 (the "One panel, contents included"
  paragraph).
- Modify: `standards/NEW_ADDON_CONTEXT.md` :1 (version), :1418, :1419, :1528, :1529.
- Modify: `AUDIT.md` check (g) at :829-851 and check (i) at :868-875. (The root-with-dependents rule at
  :880-884 is read and left unchanged; see Step 4.)
- Modify: `standards/standards/library-stack.md` :82 (the file count), :95 (the Options row).
- Modify: `README.md` :146 (`Standard is at **v2.68.0** and living.`).

**Interfaces:** consumes SR-WS-01's wording. Produces nothing code reads.

- [ ] **Step 1: Confirm the ripple is missing.**

```sh
cd $GIT/WowAddonStandards
grep -c 'nav rail' standards/EXECUTIVE_SUMMARY.md standards/NEW_ADDON_CONTEXT.md AUDIT.md standards/standards/library-stack.md   # expect 0 each
```

- [ ] **Step 2: EXECUTIVE_SUMMARY.md.** In :11, `(current: **v2.68.0**, 2026-09-26)` →
  `(current: **v2.69.0**, 2026-09-26)`. In :22, directly after the sentence ending `… declares no
  sections to strip.`, insert:
  ` A page that edits one instance out of many **MAY** fold its sub-pages into itself under a pinned **nav rail** at the body's left — the first level, with the strip beside it the second, and never a third — its selection and each entry's tab session-only.`
  In the same paragraph, replace `Above the strip sits **one chrome block**:` with
  `Above the strip — and above the rail, where there is one — sits **one chrome block**:`, and after
  `never boxed a second time.` insert ` The rail is not a picker; the block's picker stays the only one.`

- [ ] **Step 3: NEW_ADDON_CONTEXT.md.**
  - :1 → `# New Ka0s Addon — Context Pack (v2.69.0, 2026-09-26)`.
  - :1418: append after its last sentence (`… never a third level.`):
    ` A page that edits one instance out of many **MAY** instead fold its sub-pages under a pinned **nav rail** (`O.NavRail`), the first level, with the primary strip beside it the second: rail plus strip is two levels, so such a page draws no secondary strip, and the rail's selection and each entry's tab are session state (options-ui-§13).`
  - :1419: replace `**Above the strip sits at most ONE chrome block** (options-ui-§14):` with
    `**Above the strip — and the rail, where there is one — sits at most ONE chrome block** (options-ui-§14):`
    and append ` The rail is not a picker.`
  - :1528: append ` A page folding one instance's sub-pages under a **nav rail** keeps the strip beside it and draws no secondary strip; the rail's selection and each entry's tab are never persisted (options-ui-§13).`
  - :1529: replace `**At most one chrome block sits above the strip**,` with
    `**At most one chrome block sits above the strip** (and above the nav rail, on a page that has one),`
    and append ` The rail is not a picker.`

- [ ] **Step 4: AUDIT.md.**
  - Check (i) at :868: replace the heading sentence
    `**(i) A secondary strip lives in the scroll, and there is no third level (options-ui-§13).**` with
    `**(i) A secondary strip lives in the scroll, a nav rail is a first level, and there is no third level (options-ui-§13).**`.
    At the end of check (i)'s paragraph (after `… should be given one.`), append:
    ` Where a page draws a **nav rail**, count it as a level: a secondary strip on a railed page is a third level and the finding. Confirm the rail's selection and each entry's active tab are session state (a stored rail entry or per-entry tab is a finding against the same rule), that a rail click is refused in combat by the library with no host guard, and that the page's Defaults restores the active rail entry's rows and nothing wider or narrower.`
  - Check (g): in the paragraph that opens `**The `General` first tab is compliant, and has three
    conditions to check rather than one**`, directly after its sentence ending
    `… that was the rule until v2.40.0 and it was wrong about a page carrying six acts.`, insert:
    ` On a page with a **nav rail** (options-ui-§13), read the three conditions with *rail entry* for *tab*: `General` is the rail's first entry, the band spans the rail and the strip, and a rail entry carrying a picker is a second picker and the finding.`
  - The root-with-dependents rule at :880-884 needs no new letter (the rail is inside (g) and (i)). Leave it.

- [ ] **Step 5: library-stack.md.**
  - :95, the `LibKa0s-Options-1.0` row: in the file column, append `, `OptionsNav.lua`` after
    `` `OptionsScroll.lua` ``. In the description, replace `the secondary strip,` with
    `the secondary strip, the nav rail a page that edits one instance out of many may lead with (options-ui-§13),`.
  - :82: replace `**fifteen LibStub majors across twenty-two files**` with
    `**fifteen LibStub majors across twenty-three files**`, replace `` `Options` spans five files`` with
    `` `Options` spans six files``, and replace
    `answer **15 and 22** at the v1.60.0 tag, and the library's release run` with
    `answer **15 and 22** at the v1.60.0 tag; **`LibKa0s v1.61.0`** adds no major and one file, `OptionsNav.lua`, a sixth file of the `Options` major added to both lists in the same change, so they answer **15 and 23** at the v1.61.0 tag, and the library's release run`.

- [ ] **Step 6: README.md :146.** `Standard is at **v2.68.0** and living.` →
  `Standard is at **v2.69.0** and living.`

- [ ] **Step 7: Run the docs gate** over every `.md` changed versus `master` (this task's files and
  SR-WS-01's). Expect: no UNRESOLVED, no BROKEN, 0 CR bytes, clean `diff --check`. Then
  `grep -c 'nav rail' standards/EXECUTIVE_SUMMARY.md standards/NEW_ADDON_CONTEXT.md AUDIT.md standards/standards/library-stack.md`,
  expecting >= 1 each. Then `grep -rn 'v2\.68\.0' README.md standards/EXECUTIVE_SUMMARY.md standards/NEW_ADDON_CONTEXT.md | grep -v Changelog`,
  expecting no current-version pin left at v2.68.0 (historical mentions in prose are fine).

- [ ] **Step 8: Commit.**

```sh
git add standards/EXECUTIVE_SUMMARY.md standards/NEW_ADDON_CONTEXT.md AUDIT.md standards/standards/library-stack.md README.md
git commit -m "SR-WS-02: ripple the nav rail into the summary, context pack, audit checks and library stack" \
  -m "EXECUTIVE_SUMMARY and NEW_ADDON_CONTEXT at v2.69.0 with the rail as an optional first level and the block above rail and strip; AUDIT.md (g) reads the General escape as the rail's first entry, (i) counts the rail as a level; library-stack: OptionsNav.lua in the Options row, fifteen majors across twenty-three files; README pointer v2.69.0." \
  -m "<attribution trailers>"
```

### Task SR-LK-01: OptionsNav minor 1 — `O.NavRail` and the one rail inset

**Repo:** `$GIT/LibKa0s`, branch `feat/2026-09-26-settings-redesign` cut from `master` (`bed0eb1` = tag
`v1.60.0` at planning time).

**Files:**
- Create: `LibKa0s/OptionsNav.lua` (the whole file is below).
- Modify: `LibKa0s/LibKa0s.xml` :21 (a new row after `OptionsScroll.lua`).
- Modify: `LibKa0s/Options.lua` :4-7 (header), :26 (`MINOR` 24 -> 25), :846-852 (`anchorScroll`),
  :1449-1454 (the attach tail). Budget: at most 1474 lines.
- Modify: `LibKa0s/OptionsTabs.lua` :41-45 (the minor note and `TABS_MINOR` 4 -> 5), :560-575
  (`drawContentPanel`), :979-999 (`placeTabs`). Budget: at most 1494 lines.
- Modify: `tests/majors.lua` :84-94 (files plus a fifth `paired` row).
- Modify: `tests/run.lua` :84 (the suite list).
- Create: `tests/test_options_nav.lua` (the whole file is below).
- Modify: `tests/test_options_combat.lua` (one case appended after the case at :221-243).
- Modify: `CHANGELOG.md` (a new top block `## v1.61.0 — unreleased` above `## v1.60.0`).
- Create: `docs/api/Options/version-25.31.5.7.4.1-docs.md`, copied from `version-24.31.4.7.4-docs.md` and edited.
- Modify: `docs/api/Options/version-24.31.4.7.4-docs.md` (it becomes Superseded).
- Create (generated): `docs/api/Options/members-25.31.5.7.4.1.json` via `lua tools/gen-api-members.lua`.
- Modify: `docs/api/README.md` :68 (the Options key format), the Options table at :219-223.
- Modify (generated): `docs/test-cases.md`.

**Interfaces:**
- Produces, library level: `lib.__railInset(ctx) -> number`, which is `0` when `ctx.railWidth` is nil or
  `<= 0` and otherwise `ctx.railWidth + 12`. Also `lib.__AttachNav(O)`, `lib.__navMinor = 1`,
  `lib.__navShellMinor`, and `lib.MODULES.OptionsNav = 1`.
- Produces, instance level: `O.NavRail(ctx, spec) -> buttons | nil`, where
  `spec = { entries = { { key, label, tooltip } }, value, onSelect(key), width }` and `width` defaults to
  120. It records `ctx.railWidth`, `ctx.__railFrame`, `ctx.__railPool` and the ledger `ctx.__railKids`.
  Each entry button carries the plain fields `__ka0sNavKey`, `__ka0sNavText`, `__ka0sNavTip` and
  `__ka0sNavSelected`. The test seams are `O.__railInset`, `O.__railTop(ctx) -> y`,
  `O.__railEntryY(i) -> y`, `O.__navArtHeight() -> h` and `O.__resetNavArtHeight()`.
- Consumes: `O.__combatRefused()` (Options.lua:598), `O.__tabArtHeight()` (OptionsTabs.lua:849),
  `O.SetChromeHeight` (Options.lua:856), `ctx.__bannerHeight` (PageBanner, OptionsTabs.lua:1190),
  `LibKa0s-Pool-1.0` (`New`, `Acquire`, `ReleaseAll`).
- The Options version key becomes **25.31.5.7.4.1** (Options 25 · OptionsWidgets 31 · OptionsTabs 5 ·
  OptionsCompose 7 · OptionsScroll 4 · OptionsNav 1).

- [ ] **Step 1: Cut the branch.** First confirm the owner has answered O1 (`00_OVERVIEW.md`, "Needs the
  owner's sign-off"). No answer: stop and ask. Declined: build the rail's top with A2's fallback
  (`lib.__alignRail` from `placeTabs`) in Steps 4-5, and assert the re-anchored top in the drawn-art test.

```sh
cd $GIT/LibKa0s
git status --porcelain                    # expect empty
git rev-parse --short master              # expect bed0eb1
git switch -c feat/2026-09-26-settings-redesign master
wc -l LibKa0s/Options.lua LibKa0s/OptionsTabs.lua   # expect 1457 and 1489
```

- [ ] **Step 2: Write the failing suite.** Create `tests/test_options_nav.lua` (CRLF):

```lua
-- tests/test_options_nav.lua -- LibKa0s-Options-1.0's OptionsNav.lua (minor 1): the nav rail, the
-- first level of a page that edits one instance out of many (options-ui-§13), and the one inset the
-- strip, the content panel and the scroll all read so they start right of it.
--
-- The kit's frame stub no-ops SetPoint and answers no geometry, so every layout case here records
-- anchors itself (`recording`), and the alignment case answers atlas heights itself (`withArt`),
-- the same two devices tests/test_options_tabs.lua's `instrument` uses for the strip.

local T = _G.LK_TEST
local test, assertEqual, assertTrue, assertFalse, assertNil =
  T.test, T.assertEqual, T.assertTrue, T.assertFalse, T.assertNil
local Fixture = dofile("tests/fixture_options.lua")
local lib = T.options
local L = lib.LAYOUT

local panelSeq = 0
local function bench(overrides)
  local O, rec = Fixture.new(overrides)
  panelSeq = panelSeq + 1
  local ctx = O.CreatePanel("NavBench" .. panelSeq, "Nav " .. panelSeq, {})
  return O, rec, ctx
end

local ENTRIES = {
  { key = "general", label = "General", tooltip = "The instance itself." },
  { key = "filters", label = "Filters" },
  { key = "layout",  label = "Layout" },
}

local FOUR_TABS = {
  { key = "a", label = "A" }, { key = "b", label = "B" }, { key = "c", label = "C" }, { key = "d", label = "D" },
}

--- Every frame CreateFrame builds while `fn` runs, with the anchors later set on it. ClearAllPoints
--- empties them, as the client's does. The overrides stay on the frames after `fn` returns, so a
--- case can watch a later re-placement too.
local function recording(fn)
  local real = T.mocks.CreateFrame
  local made = {}
  T.mocks.CreateFrame = function(kind, name, parent, template)
    local f = real(kind, name, parent, template)
    local rec = { kind = kind, parent = parent, template = template, frame = f, points = {} }
    made[#made + 1] = rec
    rawset(f, "SetPoint", function(self, point, rel, relPoint, x, y)
      rec.points[point] = { rel = rel, relPoint = relPoint, x = x, y = y }
      return self
    end)
    rawset(f, "ClearAllPoints", function(self) rec.points = {}; return self end)
    return f
  end
  local ok, err = pcall(fn)
  T.mocks.CreateFrame = real
  if not ok then error(err, 0) end
  return made
end

local function byParent(made, parent, kind)
  local out = {}
  for _, r in ipairs(made) do
    if r.parent == parent and (kind == nil or r.kind == kind) then out[#out + 1] = r end
  end
  return out
end

--- Run `fn` with every texture answering `activeH` for an `*_Active_*` atlas and `inactiveH` for any
--- other, both measurements forgotten on the way in and out (they are cached for the session). Each
--- texture is its OWN object (the kit's CreateTexture answers the frame itself), and every other
--- method is a no-op, so a tab strip drawn inside `fn` dresses its art on these too.
local NOOP = function() end
local function withArt(O, inactiveH, activeH, fn)
  local real = T.mocks.CreateFrame
  T.mocks.CreateFrame = function(kind, ...)
    local f = real(kind, ...)
    rawset(f, "CreateTexture", function()
      local t, atlas = {}, nil
      function t:SetAtlas(name) atlas = name end
      function t:GetHeight()
        if atlas and atlas:find("Active", 1, true) then return activeH end
        return inactiveH
      end
      return setmetatable(t, { __index = function() return NOOP end })
    end)
    return f
  end
  O.__resetNavArtHeight()
  O.__resetTabArtHeight()
  local ok, err = pcall(fn)
  T.mocks.CreateFrame = real
  O.__resetNavArtHeight()
  O.__resetTabArtHeight()
  if not ok then error(err, 0) end
end

--- Draw a four-tab strip on `ctx` (after a rail when `rail`), with the chrome `chromeW` wide, and
--- answer the first tab's x, the content panel's anchors, the scroll's left x and the row count.
local function stripUnder(O, ctx, rail, chromeW)
  if rail then O.NavRail(ctx, { entries = ENTRIES, value = "general" }) end
  ctx.chrome:__setGeom(chromeW or 260, 0)
  local made = recording(function()
    O.TabStrip(ctx, { tabs = FOUR_TABS, value = "a" })
  end)
  local tabs, panels = byParent(made, ctx.chrome, "Button"), byParent(made, ctx.body, "Frame")
  local rows, rowCount = {}, 0
  for _, t in ipairs(tabs) do
    if not rows[t.points.TOPLEFT.y] then rowCount = rowCount + 1 end
    rows[t.points.TOPLEFT.y] = true
  end
  local scroll = O.EnsureScroll(ctx)
  local at = {}
  rawset(scroll.frame, "SetPoint", function(self, point, _, _, x) at[point] = x; return self end)
  O.SetChromeHeight(ctx, ctx.chromeHeight)
  return { tabX = tabs[1].points.TOPLEFT.x, panel = panels[#panels].points, scrollX = at.TOPLEFT,
           rows = rowCount }
end

-- ── the seams ────────────────────────────────────────────────────────────────────────────────

test("nav: the rail inset is zero with no rail and the rail's width plus its 12px gap with one", function()
  -- red under: an inset that answers the gap alone for a page with no rail (every page in the
  -- collection would move 12px right), or one that ignores a released rail's zero width.
  local O, _, ctx = bench()
  assertEqual(O.__railInset(ctx), 0, "a page that never drew a rail")
  ctx.railWidth = 0
  assertEqual(O.__railInset(ctx), 0, "a rail released to nothing")
  ctx.railWidth = 120
  assertEqual(O.__railInset(ctx), 132)
  ctx.railWidth = 90
  assertEqual(O.__railInset(ctx), 102)
  assertEqual(O.__railInset(nil), 0, "no ctx")
  assertEqual(O.__railInset, lib.__railInset, "one function, read by the shell, the strip and the panel")
end)

test("nav: the rail's top is measured off the ACTIVE tab art, under the banner's band", function()
  -- red under: the rail anchored to the tab BUTTON's top (a hard-coded 0), to the inactive art
  -- (a few pixels below the selected tab's top), or with the banner's band left out.
  local O, _, ctx = bench()
  withArt(O, 28, 33, function()
    assertEqual(O.__navArtHeight(), 33, "the active cap, measured")
    assertEqual(O.__railTop(ctx), -(L.TAB_H - 33), "no banner: level with the selected tab's art")
    ctx.__bannerHeight = 50
    assertEqual(O.__railTop(ctx), -(50 + L.TAB_H - 33), "under the band the banner reserved")
  end)
  ctx.__bannerHeight = nil
  withArt(O, 26, 30, function()
    -- another client scale answers another height, and the rail follows it: never hard-coded
    assertEqual(O.__railTop(ctx), -(L.TAB_H - 30))
  end)
  withArt(O, nil, nil, function()
    -- nothing measurable: the strip's own fallback, the button height, so the chrome's top
    assertEqual(O.__railTop(ctx), 0)
  end)
end)

test("nav: the probe's cap is the drawn selected tab's own art, so the rail's top is level with the strip beside it (spec §2, §4; A2)", function()
  -- red under: a probe measuring an atlas other than the one the selected tab is drawn from (the rail
  -- would sit a few pixels off the tab art beside it), or a rail top taken from the shorter,
  -- unselected art. The spec asks for the top "measured from the drawn tab's textures": this pins
  -- that the number the rail uses IS the drawn tab's, with a stub texture set.
  local O, _, ctx = bench()
  withArt(O, 28, 33, function()
    ctx.__bannerHeight = 50
    O.NavRail(ctx, { entries = ENTRIES, value = "general" })
    ctx.chrome:__setGeom(600, 0)                    -- one row: every tab on the rail's line
    O.TabStrip(ctx, { tabs = FOUR_TABS, value = "a" })
    local tallest = 0
    for _, b in ipairs(ctx.__tabKids) do             -- the ledger also holds the content panel
      local art = b.__ka0sTabArt
      if art and art.left then tallest = math.max(tallest, art.left:GetHeight() or 0) end
    end
    assertEqual(tallest, 33, "the selected tab is drawn from the active cap")
    assertEqual(O.__navArtHeight(), tallest, "the probe measured the atlas the drawn tab carries")
    assertEqual(O.__railTop(ctx), -(50 + L.TAB_H - tallest), "and the rail's top is that art's top")
  end)
  ctx.__bannerHeight = nil
end)

test("nav: entries stack 20px apart from 8px below the rail's top", function()
  local O = bench()
  assertEqual(O.__railEntryY(1), -8)
  assertEqual(O.__railEntryY(2), -28)
  assertEqual(O.__railEntryY(3), -48)
end)

-- ── drawing ──────────────────────────────────────────────────────────────────────────────────

test("nav: NavRail draws one entry per spec entry, records railWidth, and disables the selected one", function()
  -- red under: the selection read from anything but spec.value, or the width not recorded (the
  -- strip, the panel and the scroll would never move).
  local O, _, ctx = bench()
  local buttons = O.NavRail(ctx, { entries = ENTRIES, value = "filters", onSelect = function() end })
  assertEqual(#buttons, 3)
  assertEqual(ctx.railWidth, 120, "the default width is Test10's")
  for i, b in ipairs(buttons) do
    assertEqual(b.__ka0sNavKey, ENTRIES[i].key)
    assertEqual(b.__ka0sNavText, ENTRIES[i].label)
    assertTrue(b:IsShown(), ENTRIES[i].key .. " shown")
    assertEqual(ctx.__railKids[i], b, "the ledger a suite reads, in rail order")
  end
  assertFalse(buttons[2]:IsEnabled(), "the selected entry is disabled, as the active tab is")
  assertTrue(buttons[1]:IsEnabled() and buttons[3]:IsEnabled(), "the others are live")
  assertTrue(buttons[2].__ka0sNavSelected and not buttons[1].__ka0sNavSelected)
  assertEqual(buttons[1].__ka0sNavTip, "The instance itself.")
  local again = O.NavRail(ctx, { entries = { ENTRIES[2], ENTRIES[1] }, value = "general", width = 90 })
  assertEqual(ctx.railWidth, 90, "spec.width wins")
  -- red under: a dress that only ADDS fields (a pooled button keeps the last entry's tooltip)
  assertNil(again[1].__ka0sNavTip, "Filters carries no tooltip, whichever button it landed on")
  assertEqual(again[2].__ka0sNavTip, "The instance itself.")
end)

test("nav: the rail hangs in the body at the content column's left edge, from the art's top to the panel's foot", function()
  -- red under: the rail parented to the panel (outside the body, where the lab put it), anchored
  -- anywhere but CONTENT_LEFT, or its entries placed off the pure seam.
  local O, _, ctx = bench()
  local made = recording(function()
    O.NavRail(ctx, { entries = ENTRIES, value = "general" })
  end)
  local rails = byParent(made, ctx.body)
  assertEqual(#rails, 1, "one rail frame, a child of the body, so the cover's level walk finds it")
  local r = rails[1]
  assertEqual(r.template, "BackdropTemplate", "the tree pane's backdrop")
  assertEqual(r.points.TOPLEFT.rel, ctx.body)
  assertEqual(r.points.TOPLEFT.x, L.CONTENT_LEFT)
  assertEqual(r.points.TOPLEFT.y, O.__railTop(ctx))
  assertEqual(r.points.BOTTOMLEFT.rel, ctx.body)
  assertEqual(r.points.BOTTOMLEFT.x, L.CONTENT_LEFT)
  assertEqual(r.points.BOTTOMLEFT.y, L.PANEL_BOTTOM, "level with the content panel's foot")
  local entries = byParent(made, r.frame, "Button")
  assertEqual(#entries, 3)
  for i, e in ipairs(entries) do
    assertEqual(e.points.TOPLEFT.y, O.__railEntryY(i), "entry " .. i)
    assertEqual(e.points.TOPLEFT.x, 5)
    assertEqual(e.points.TOPRIGHT.x, -5)
  end
end)

-- ── the one inset ────────────────────────────────────────────────────────────────────────────

test("nav: with no rail the strip, the content panel and the scroll are anchored exactly as before", function()
  -- red under: an inset that is not zero for railWidth nil or 0 -- every page in the collection,
  -- including the ten hosts that never draw a rail, would move.
  for _, width in ipairs({ false, 0 }) do
    local O, _, ctx = bench()
    if width then ctx.railWidth = width end
    local got = stripUnder(O, ctx, false)
    assertEqual(got.tabX, 0, "the first tab at the chrome's left")
    assertEqual(got.panel.TOPLEFT.x, -(L.CONTENT_LEFT - L.PANEL_LEFT))
    assertEqual(got.panel.BOTTOMLEFT.x, L.PANEL_LEFT)
    assertEqual(got.scrollX, L.CONTENT_LEFT)
    assertEqual(got.rows, 1, "four 60px tabs fit 260px on one row")
  end
end)

test("nav: with a rail the strip, the content panel's left edge and the scroll all move by the one inset", function()
  -- red under: any of the three reading a number of its own (the panel's edge, the first tab and
  -- the first control stop lining up), or the strip wrapping against the chrome's full width (tabs
  -- drawn under the rail's right edge).
  local O, _, ctx = bench()
  local got = stripUnder(O, ctx, true)
  local inset = O.__railInset(ctx)
  assertEqual(inset, 132)
  assertEqual(got.tabX, inset)
  assertEqual(got.panel.TOPLEFT.x, -(L.CONTENT_LEFT - L.PANEL_LEFT) + inset)
  assertEqual(got.panel.BOTTOMLEFT.x, L.PANEL_LEFT + inset)
  assertEqual(got.scrollX, L.CONTENT_LEFT + inset)
  assertEqual(got.rows, 2, "260 - 132 = 128 holds two 60px tabs a row")
  -- Test10's geometry, in body coordinates: the content panel's left edge 4px right of the rail's.
  assertEqual(L.CONTENT_LEFT + got.panel.TOPLEFT.x, L.CONTENT_LEFT + 120 + 4)
end)

test("nav: the first render's zero-width chrome re-places the strip, inset included, when the width arrives", function()
  -- The first page a player opens is drawn before the canvas has a width (OptionsTabs.lua's
  -- replaceOnResize). red under: a usable width left negative (every tab on its own row for good),
  -- or the re-placement measured against the full width, or the inset applied twice.
  local O, _, ctx = bench()
  O.NavRail(ctx, { entries = ENTRIES, value = "general" })
  local made = recording(function()
    O.TabStrip(ctx, { tabs = { { key = "a", label = "A" }, { key = "b", label = "B" } }, value = "a" })
  end)
  local tabs = byParent(made, ctx.chrome, "Button")
  assertEqual(tabs[1].points.TOPLEFT.x, 132, "placed at the inset even at zero width")
  assertTrue(tabs[1].points.TOPLEFT.y ~= tabs[2].points.TOPLEFT.y, "a zero-width chrome stacks them")
  ctx.chrome:GetScript("OnSizeChanged")(ctx.chrome, 600)
  assertEqual(tabs[1].points.TOPLEFT.x, 132)
  assertEqual(tabs[2].points.TOPLEFT.x, 132 + L.TAB_MIN_W + L.TAB_GAP, "one row once 468px arrive")
  assertEqual(tabs[1].points.TOPLEFT.y, tabs[2].points.TOPLEFT.y)
end)

-- ── the pool, the click, the release ─────────────────────────────────────────────────────────

test("nav: a re-render reuses the pooled entries and builds no frame; a shorter one hides the surplus", function()
  -- red under: entries built per render (a frame leaked per click for the session), or a released
  -- entry left shown under the rail's next, shorter list.
  local O, _, ctx = bench()
  local first = O.NavRail(ctx, { entries = ENTRIES, value = "general" })
  local made = recording(function()
    O.NavRail(ctx, { entries = ENTRIES, value = "layout" })
  end)
  assertEqual(#made, 0, "no frame built on the second render")
  local second = O.NavRail(ctx, { entries = { ENTRIES[1], ENTRIES[2] }, value = "general" })
  assertEqual(#second, 2)
  local shown = 0
  for _, b in ipairs(first) do if b:IsShown() then shown = shown + 1 end end
  assertEqual(shown, 2, "the third entry went back to the pool, hidden")
  assertEqual(#ctx.__railKids, 2)
end)

test("nav: a click on another entry hands its key to onSelect; the selected entry and a raising handler do nothing", function()
  local O, _, ctx = bench()
  local picked = {}
  local buttons = O.NavRail(ctx, { entries = ENTRIES, value = "general",
    onSelect = function(key) picked[#picked + 1] = key end })
  buttons[3]:__fire("OnClick")
  assertEqual(table.concat(picked, ","), "layout")
  buttons[1]:__fire("OnClick")
  -- red under: the selected entry re-rendering the page it is already on
  assertEqual(#picked, 1, "the selected entry does nothing")
  buttons = O.NavRail(ctx, { entries = ENTRIES, value = "general", onSelect = function() error("boom") end })
  -- red under: onSelect called bare, so a host's raise escapes into the client's click dispatch
  assertTrue(pcall(function() buttons[2]:__fire("OnClick") end), "a raising host handler stays inside the click")
end)

test("nav: an empty entry list releases the rail and gives the page its full width back", function()
  local O, _, ctx = bench()
  local buttons = O.NavRail(ctx, { entries = ENTRIES, value = "general" })
  assertNil(O.NavRail(ctx, { entries = {} }))
  assertEqual(ctx.railWidth, 0)
  assertEqual(O.__railInset(ctx), 0)
  assertFalse(ctx.__railFrame:IsShown(), "the rail frame is hidden")
  for _, b in ipairs(buttons) do assertFalse(b:IsShown(), "entry " .. b.__ka0sNavKey .. " hidden") end
  assertNil(O.NavRail(nil, { entries = ENTRIES }), "no ctx draws nothing")
end)

test("nav: with OptionsNav.lua absent there is no NavRail and nothing is inset", function()
  -- docs/releasing.md: a partly copied Options major degrades rather than raising at a call site.
  -- red under: an unguarded cross-file call in anchorScroll, placeTabs or drawContentPanel.
  local savedAttach, savedInset = lib.__AttachNav, lib.__railInset
  lib.__AttachNav, lib.__railInset = nil, nil
  local ok, err = pcall(function()
    local O, _, ctx = bench()
    assertNil(O.NavRail, "the rail half really is absent")
    ctx.railWidth = 120
    local got = stripUnder(O, ctx, false)
    assertEqual(got.tabX, 0)
    assertEqual(got.panel.BOTTOMLEFT.x, L.PANEL_LEFT)
    assertEqual(got.scrollX, L.CONTENT_LEFT)
  end)
  lib.__AttachNav, lib.__railInset = savedAttach, savedInset
  if not ok then error(err, 0) end
end)
```

Then register the suite in `tests/run.lua` :84, directly after `"test_options_tabs",`:

```lua
    "test_options_nav",
```

And append this case to `tests/test_options_combat.lua`, directly after the case that ends at :243
(`combat: REGEN_DISABLED covers an open tabbed page above its tab strip`). It reuses that file's
`combatCase`, `withLevels`, `Fixture`, `seq`, `show`, `enterCombat` and `coverShown`:

```lua
combatCase("combat: REGEN_DISABLED covers a page's nav rail, and a rail click in combat is refused", function()
  -- options-ui-§2 (v2.69.0): the cover falls over the whole page, the nav rail included, and a rail
  -- switch is refused with every other structural re-render. red under: the rail parented outside
  -- the panel's child tree (the cover's level walk would miss it), or a rail OnClick that does not
  -- ask the lock.
  withLevels(function()
    local O = Fixture.new()
    seq = seq + 1
    local ctx = O.CreatePanel("CombatPage" .. seq, "Combat " .. seq, { pageKey = "tabbed" })
    local picked = {}
    O.SetRenderer(ctx, function(c)
      O.ClearScroll(c)
      O.NavRail(c, { value = "a", onSelect = function(k) picked[#picked + 1] = k end,
        entries = { { key = "a", label = "A" }, { key = "b", label = "B" } } })
      O.RenderTabbedSchema(c, "tabbed")
    end)
    show(ctx)
    assertEqual(#ctx.__railKids, 2, "the rail was drawn")
    enterCombat()
    assertTrue(coverShown(ctx), "the page is covered")
    local cover = ctx.__combatCover:GetFrameLevel()
    assertTrue(cover > ctx.__railFrame:GetFrameLevel(), "above the rail")
    for _, b in ipairs(ctx.__railKids) do
      assertTrue(cover > b:GetFrameLevel(), "above entry " .. b.__ka0sNavKey)
    end
    ctx.__railKids[2]:__fire("OnClick")
    assertEqual(#picked, 0, "a rail switch is refused in combat")
  end)
end)
```

- [ ] **Step 3: Run the suite and see it fail.**

```sh
$B lua tests/run.lua > /tmp/lk-run.txt 2>&1; grep -E '^  (FAIL|PASS)  (nav:|combat: REGEN_DISABLED covers a page)' /tmp/lk-run.txt
```

Expected: every `nav:` case and the new combat case report `FAIL`, with errors of the form
`attempt to call field '__railInset' (a nil value)` and `attempt to call field 'NavRail' (a nil value)`.
The inventory may also fail on the listed suite until the file loads. Nothing else fails.

- [ ] **Step 4: Create `LibKa0s/OptionsNav.lua`** (CRLF, ASCII string literals):

```lua
-- LibKa0s-Options-1.0 -- the nav rail: a pinned vertical list at the left of a page's body, the FIRST
-- level of a page that edits one instance out of many; the pinned primary tab strip drawn to its
-- right is the second (options-ui-§13). A host folds what would otherwise be several sub-pages,
-- all retargeted by one picker, into one page, and the rail chooses among them.
--
-- A sixth file of the Options major (minor 1), guarded with the same multi-file idiom as
-- OptionsTabs.lua and OptionsScroll.lua. A new file rather than an append because both files it
-- reaches into are at their accepted size (CLAUDE.md's census): Options.lua and OptionsTabs.lua
-- carry only guarded reads of `lib.__railInset`, so a copy vendored without this file lays every
-- page out exactly as it did before the rail existed.
--
-- The look is AceGUI's TreeGroup tree pane -- a list on the left for the first level, gold tabs on
-- top for the second, so the two cannot be mistaken for one another. The geometry is AuraMaster's
-- Test10 (the 2026-09-26 settings lab), which its owner chose over nine alternatives.

local lib = LibStub and LibStub("LibKa0s-Options-1.0", true)
if not lib then return end

-- The primary strip's floor, for the primary strip's reason: the entries are pooled per page.
local Pool = LibStub and LibStub("LibKa0s-Pool-1.0", true)
local NEEDS_POOL = 1
if not Pool or (Pool.MINOR or 0) < NEEDS_POOL then return end

-- Minor 1: O.NavRail, the one inset the strip, the content panel and the scroll read
-- (lib.__railInset), and the rail's top measured off the selected tab's art.
local NAV_MINOR = 1
-- Paired on the SHELL's minor as well as this file's own -- see OptionsScroll.lua for why.
if lib.__navMinor and lib.__navMinor >= NAV_MINOR
  and lib.__navShellMinor == lib.MINOR then return end
lib.__navMinor      = NAV_MINOR
lib.__navShellMinor = lib.MINOR

lib.MODULES = lib.MODULES or {}
lib.MODULES.OptionsNav = NAV_MINOR

local L = lib.LAYOUT

-- File-local, not lib.LAYOUT: tests/test_options.lua's LAYOUT gate reads Options.lua alone, and no
-- host sizes anything off these. A host wanting another width passes spec.width.
local RAIL_W      = 120   -- Test10's NAV_W
-- Rail edge to the content column. With it the content panel's left edge (PANEL_LEFT + inset) lands
-- 4px right of the rail's right edge (CONTENT_LEFT + width), and the first tab and the scroll start
-- at CONTENT_LEFT + width + 12 -- Test10's arrangement, without moving the body from outside.
local RAIL_GAP    = 12
local ENTRY_H     = 20
local ENTRY_TOP   = 8
local ENTRY_INSET = 5
local LABEL_X     = 6
local SELECT_TEX  = "Interface\\QuestFrame\\UI-QuestLogTitleHighlight"
local SELECT_RGB  = { 0.3, 0.5, 1 }
local LABEL_GOLD  = { 1, 0.82, 0 }
local LABEL_WHITE = { 1, 1, 1 }
local ACTIVE_CAP  = "Options_Tab_Active_Left"
local PANE_BACKDROP = {
  bgFile   = "Interface\\ChatFrame\\ChatFrameBackground",
  edgeFile = "Interface\\Tooltips\\UI-Tooltip-Border",
  tile = true, tileSize = 16, edgeSize = 16,
  insets = { left = 3, right = 3, top = 5, bottom = 3 },
}
local PANE_FILL   = { 0.1, 0.1, 0.1, 0.5 }
local PANE_BORDER = { 0.4, 0.4, 0.4 }

-- ── the one inset ──────────────────────────────────────────────────────────────────────────

--- How far right of the content column everything beside the rail starts: the rail's width plus its
--- gap, or 0 for a page with no rail. LIBRARY-level, because OptionsTabs.lua's drawContentPanel is a
--- file-level local with no instance in reach; placeTabs and the shell's anchorScroll read this same
--- function, so the three cannot disagree -- the job __scrollTopInset does for the top edge.
--- @return number
function lib.__railInset(ctx)
  local w = ctx and ctx.railWidth
  if type(w) ~= "number" or w <= 0 then return 0 end
  return w + RAIL_GAP
end

-- ── the rail's top ───────────────────────────────────────────────────────────────────────────
--
-- The tab art is bottom-anchored in a TAB_H button, so the button's top is not where a tab visibly
-- starts. The rail's top is level with the SELECTED tab's art, the tallest thing on the row (the lab
-- measured the highest shown texture, which is that one). Its atlas is measured once on a probe
-- texture, as OptionsTabs.lua measures the unselected one, and cached on success only, so a call
-- made before the client resolves the atlas cannot pin a fallback for the session.
local measuredActiveH
local probeFrame

local function probeTexture()
  probeFrame = probeFrame or CreateFrame("Frame", nil, UIParent)
  if probeFrame.Hide then probeFrame:Hide() end
  local tex = probeFrame.__ka0sNavProbe
  if not tex and probeFrame.CreateTexture then
    tex = probeFrame:CreateTexture(nil, "BACKGROUND")
    probeFrame.__ka0sNavProbe = tex
  end
  return tex
end

--- The selected tab's art height; the strip's own pitch (and through it TAB_H) where nothing measures.
local function activeArtHeight(O)
  if measuredActiveH then return measuredActiveH end
  local h
  local tex = probeTexture()
  if tex and tex.SetAtlas then
    tex:SetAtlas(ACTIVE_CAP, true)
    h = tex.GetHeight and tex:GetHeight()
  end
  if type(h) == "number" and h > 0 and h <= L.TAB_H then
    measuredActiveH = h
    return h
  end
  return (O.__tabArtHeight and O.__tabArtHeight()) or L.TAB_H
end

local function resetActiveArtHeight()
  measuredActiveH, probeFrame = nil, nil
end

--- The rail's top edge below the body's top: the banner's band, then the empty strip above the art.
local function railTop(ctx, artH)
  return -(((ctx and ctx.__bannerHeight) or 0) + (L.TAB_H - artH))
end

local function entryY(i)
  return -(ENTRY_TOP + (i - 1) * ENTRY_H)
end

-- ── the frames ───────────────────────────────────────────────────────────────────────────────

--- The rail itself: ONE per page, built on the first render that draws a rail and kept, the way
--- OptionsTabs.lua keeps a page's rule texture. A child of the BODY, so the combat cover's level walk
--- (lib.__coverLevel) finds it and the cover goes over it.
local function railFrame(ctx)
  local rail = ctx.__railFrame
  if rail then return rail end
  rail = CreateFrame("Frame", nil, ctx.body, "BackdropTemplate")
  if rail.SetBackdrop then
    rail:SetBackdrop(PANE_BACKDROP)
    rail:SetBackdropColor(PANE_FILL[1], PANE_FILL[2], PANE_FILL[3], PANE_FILL[4])
    rail:SetBackdropBorderColor(PANE_BORDER[1], PANE_BORDER[2], PANE_BORDER[3])
  end
  ctx.__railFrame = rail
  return rail
end

--- Wired ONCE per entry and re-aimed by every dress, as a tab's tooltip is (HookScript would
--- accumulate a pair of handlers per render on a pooled button).
local function attachEntryTooltip(b)
  b:SetScript("OnEnter", function()
    if not (GameTooltip and b.__ka0sNavTip) then return end
    GameTooltip:SetOwner(b, "ANCHOR_RIGHT")
    GameTooltip:SetText(b.__ka0sNavText or "", 1, 1, 1)
    GameTooltip:AddLine(b.__ka0sNavTip, nil, nil, nil, true)
    GameTooltip:Show()
  end)
  b:SetScript("OnLeave", function()
    if GameTooltip then GameTooltip:Hide() end
  end)
end

--- A bare entry: the button, its label, the hover glow and the selection bar. The pool's factory;
--- nothing here depends on WHICH entry it will be.
local function newEntry(rail)
  local b = CreateFrame("Button", nil, rail)
  b:SetHeight(ENTRY_H)
  local label = b:CreateFontString(nil, "OVERLAY", "GameFontNormal")
  label:SetPoint("LEFT", b, "LEFT", LABEL_X, 0)
  label:SetJustifyH("LEFT")
  local hover = b:CreateTexture(nil, "HIGHLIGHT")
  hover:SetTexture(SELECT_TEX)
  hover:SetBlendMode("ADD")
  hover:SetAllPoints(b)
  local sel = b:CreateTexture(nil, "BACKGROUND")
  sel:SetTexture(SELECT_TEX)
  sel:SetVertexColor(SELECT_RGB[1], SELECT_RGB[2], SELECT_RGB[3])
  sel:SetBlendMode("ADD")
  sel:SetAllPoints(b)
  b.__ka0sNavLabel, b.__ka0sNavSel = label, sel
  attachEntryTooltip(b)
  return b
end

--- Put one pooled button into the state of one entry. EVERY field is re-applied, because the button
--- may have been another entry a moment ago (OptionsTabs.lua's dressTab says why at length).
--- The selected entry is the DISABLED one, as the active tab is: it neither highlights nor fires.
local function dressEntry(O, b, entry, selected, onSelect)
  b.__ka0sNavKey, b.__ka0sNavText, b.__ka0sNavTip = entry.key, entry.label, entry.tooltip
  b.__ka0sNavSelected = selected
  local label = b.__ka0sNavLabel
  local rgb = selected and LABEL_WHITE or LABEL_GOLD
  label:SetText(entry.label or "")
  label:SetTextColor(rgb[1], rgb[2], rgb[3])
  b.__ka0sNavSel:SetAlpha(selected and 1 or 0)
  b:SetEnabled(not selected)
  b:SetScript("OnClick", function()
    if selected then return end
    -- A rail switch is a structural re-render, refused in combat exactly as a tab click is
    -- (options-ui-§2, §13). The library owns the refusal; a host adds no guard of its own.
    if O.__combatRefused and O.__combatRefused() then return end
    if onSelect then pcall(onSelect, entry.key) end
  end)
end

-- ── the instance half ────────────────────────────────────────────────────────────────────────

function lib.__AttachNav(O)
  local function placeRail(ctx, width)
    local rail = railFrame(ctx)
    rail:ClearAllPoints()
    rail:SetPoint("TOPLEFT",    ctx.body, "TOPLEFT",    L.CONTENT_LEFT, railTop(ctx, activeArtHeight(O)))
    rail:SetPoint("BOTTOMLEFT", ctx.body, "BOTTOMLEFT", L.CONTENT_LEFT, L.PANEL_BOTTOM)
    rail:SetWidth(width)
    rail:Show()
    return rail
  end

  --- A live scroll moves at once; a strip drawn next reads the inset as it places itself.
  local function reanchor(ctx)
    if (ctx.chromeHeight or 0) > 0 and O.SetChromeHeight then O.SetChromeHeight(ctx, ctx.chromeHeight) end
  end

  --- The pinned nav rail (options-ui-§13): the first level of a page that edits one instance out of
  --- many. Draw it AFTER O.PageBanner and BEFORE O.TabStrip: it reads the band the banner reserved
  --- (`ctx.__bannerHeight`) for its top, and the strip reads the width it records for its inset.
  ---
  --- `spec` = { entries = { { key, label, tooltip } }, value, onSelect, width }. `width` defaults to
  --- 120. The selection is the HOST's state, as SubTabStrip's is: `spec.value` and `spec.onSelect`
  --- are the whole contract. Returns the entry buttons in rail order, or nil having drawn nothing (an
  --- empty list releases the rail and gives the page its full width back).
  ---
  --- Entries are POOLED per page and released on every call, as the primary strip's tabs are. The
  --- rail is chrome, not scroll content: O.ClearScroll does not touch it.
  function O.NavRail(ctx, spec)
    if not (ctx and ctx.body) then return nil end
    ctx.__railPool = ctx.__railPool or Pool.New()
    Pool.ReleaseAll(ctx.__railPool)
    ctx.__railKids = {}
    local entries = type(spec) == "table" and spec.entries
    if type(entries) ~= "table" or #entries == 0 then
      ctx.railWidth = 0
      if ctx.__railFrame then ctx.__railFrame:Hide() end
      reanchor(ctx)
      return nil
    end
    local width = tonumber(spec.width) or RAIL_W
    ctx.railWidth = width
    local rail = placeRail(ctx, width)
    local factory = function() return newEntry(rail) end
    local buttons = {}
    for i, entry in ipairs(entries) do
      local b = Pool.Acquire(ctx.__railPool, factory)
      dressEntry(O, b, entry, entry.key == spec.value, spec.onSelect)
      b:ClearAllPoints()
      b:SetPoint("TOPLEFT",  rail, "TOPLEFT",   ENTRY_INSET, entryY(i))
      b:SetPoint("TOPRIGHT", rail, "TOPRIGHT", -ENTRY_INSET, entryY(i))
      b:Show()
      buttons[i], ctx.__railKids[i] = b, b
    end
    reanchor(ctx)
    return buttons
  end

  -- Test seams, `__`-prefixed and therefore outside every host's surface parity.
  O.__railInset         = lib.__railInset
  O.__railTop           = function(ctx) return railTop(ctx, activeArtHeight(O)) end
  O.__railEntryY        = entryY
  O.__navArtHeight      = function() return activeArtHeight(O) end
  O.__resetNavArtHeight = resetActiveArtHeight
end
```

- [ ] **Step 5: Load it and attach it.**
  - `LibKa0s/LibKa0s.xml`: after `	<Script file="OptionsScroll.lua"/>` (:21), add
    `	<Script file="OptionsNav.lua"/>` (tab-indented, CRLF).
  - `LibKa0s/Options.lua` :26: `local MAJOR, MINOR = "LibKa0s-Options-1.0", 24` -> `…, 25`.
  - `LibKa0s/Options.lua` :4-7: replace `-- Five files, one major.` with `-- Six files, one major.`, and
    replace `-- composers; OptionsScroll.lua is the always-shown scrollbar patch and the font preload. They are`
    with the two lines
    `-- composers; OptionsScroll.lua is the always-shown scrollbar patch and the font preload;`
    `-- OptionsNav.lua is the nav rail a page may lead with (minor 25 reads its inset). They are`
    (+1 line).
  - `LibKa0s/Options.lua`, `anchorScroll` (:846-852): replace the TOPLEFT line with

```lua
    -- Right of a nav rail (minor 25): OptionsNav.lua's one inset, zero with no rail or no such file,
    -- so a page without a rail is anchored exactly as before. placeTabs and drawContentPanel read it too.
    local inset = lib.__railInset and lib.__railInset(ctx) or 0
    f:SetPoint("TOPLEFT",     ctx.body, "TOPLEFT",     L.CONTENT_LEFT + inset, -O.__scrollTopInset(ctx))
```

  - `LibKa0s/Options.lua`, the attach tail (:1453, after `if lib.__AttachScroll …`): add
    `  if lib.__AttachNav     then lib.__AttachNav(O)        end`
    (`OptionsNav.lua` takes `O` alone: it reads nothing from the descriptor.)
  - `LibKa0s/OptionsTabs.lua` :45: `local TABS_MINOR = 4` -> `local TABS_MINOR = 5`, and directly above
    it (after the minor-4 note ending `… (AuraMaster-R-04).`) add the one line
    `-- Minor 5: the strip and the content panel start right of a nav rail (OptionsNav.lua's lib.__railInset).`
  - `LibKa0s/OptionsTabs.lua`, `drawContentPanel` (:560-575): after
    `local panel = Pool.Acquire(ctx.__panelPool, function() return newContentPanel(ctx) end)` add
    `  local inset = lib.__railInset and lib.__railInset(ctx) or 0`, and change the two left anchors to

```lua
  panel:SetPoint("TOPLEFT",     ctx.chrome, "BOTTOMLEFT",  -(L.CONTENT_LEFT - L.PANEL_LEFT) + inset, 0)
  panel:SetPoint("BOTTOMLEFT",  ctx.body,   "BOTTOMLEFT",    L.PANEL_LEFT + inset,  L.PANEL_BOTTOM)
```

  - `LibKa0s/OptionsTabs.lua`, `placeTabs` (:979-999): after `ctx.__tabPlacedAt = available` add

```lua
    local inset = lib.__railInset and lib.__railInset(ctx) or 0
    local usable = inset > 0 and math.max(available - inset, L.TAB_MIN_W) or available
```

    change `O.__tabPlacement(widths, available, L.TAB_GAP, top, pitch)` to
    `O.__tabPlacement(widths, usable, L.TAB_GAP, top, pitch)`, and change the placement line to
    `b:SetPoint("TOPLEFT", ctx.chrome, "TOPLEFT", p.x + inset, p.y)`. `ctx.__tabPlacedAt` keeps the
    raw `available`, so `replaceOnResize`'s change test is unchanged.
  - `tests/majors.lua` :86: `files = { …, "OptionsScroll", "OptionsNav" }`, and after the
    `OptionsScroll` paired row (:92) add
    `      { file = "OptionsNav",     minorField = "__navMinor",     probeField = "__navShellMinor" },`

- [ ] **Step 6: Run and see the new cases pass.**

```sh
$B lua tests/run.lua > /tmp/lk-run.txt 2>&1; grep -E '^  (FAIL|PASS)  (nav:|combat: REGEN_DISABLED covers a page)' /tmp/lk-run.txt
```

Expected: every `nav:` case and the combat case report `PASS`. `tests/test_versioning.lua` now fails,
because the CHANGELOG, the API document and the member manifest do not yet name 25/5/1. Step 7 fixes
that.

- [ ] **Step 7: The version record** (`docs/releasing.md` steps 2-6).
  - `CHANGELOG.md`: insert above `## v1.60.0 — 2026-09-26`:

```markdown
## v1.61.0 — unreleased

Versions in this release: **Options minor 25**, **OptionsTabs minor 5** and a new file,
**OptionsNav minor 1** (`LibKa0s-Options-1.0` **25.31.5.7.4.1**). Every other file is unchanged
from v1.60.0: `Core` 8, `Env` 1, `Compat` 1, `Lifecycle` 2, `Bus` 2, `Schema` 2, `Pool` 3, `Item` 2,
`Media` 4, `Widgets` 10 and `WidgetsDragHandle` 3 (key 10.3), `DebugLog` 14 and `DebugLogDiagnostics`
1 (key 14.1), `Slash` 16, `Launcher` 4, `OptionsWidgets` 31, `OptionsCompose` 7, `OptionsScroll` 4,
`Perf` 13 and `PerfPanel` 5 (key 13.5); the test kit stays at **revision 27**. No `NEEDS_*` floor
rises and no major is added; `OptionsNav.lua` is a sixth file of the Options major, so the library is
**fifteen majors across twenty-three files**. Built to the Ka0s WoW Addon Standard **v2.69.0**, whose
options-ui-§13 sanctions the nav rail below, for AuraMaster#6.

### OptionsNav minor 1: the nav rail

- **`O.NavRail(ctx, spec)`**, `spec = { entries = { { key, label, tooltip } }, value, onSelect, width }`:
  a pinned vertical list at the left of the page's body, the first level of a page that edits one
  instance out of many (options-ui-§13), in AceGUI's TreeGroup tree-pane look (tooltip-border
  backdrop, 0.1/0.1/0.1/0.5 fill, 0.4 border; gold `GameFontNormal` entries; the selected entry
  white on the blue `UI-QuestLogTitleHighlight` bar, and disabled, as the active tab is). `width`
  defaults to 120. Draw it after `O.PageBanner` and before `O.TabStrip`. The selection is the host's
  (`spec.value` / `spec.onSelect`, as `O.SubTabStrip`'s is); `onSelect` is pcall'd, and a click is
  refused in combat by the library as a tab click is. Entries are pooled per page and released on
  every call; an empty list releases the rail and records `ctx.railWidth = 0`.
- **`lib.__railInset(ctx)`**: the rail's width plus a 12px gap, or 0 with no rail. The one number
  the strip's placement, the content panel's left edge and the scroll's left anchor read, so the
  three cannot disagree. Library-level because `drawContentPanel` has no instance in reach.
- **The rail's top** is level with the selected tab's art top: `-(bannerHeight + TAB_H -
  activeArtHeight)`, the active cap atlas measured once on a probe texture and cached on success
  only, falling back to the strip's own pitch. Seams: `O.__railTop`, `O.__railEntryY`,
  `O.__navArtHeight`, `O.__resetNavArtHeight`, `O.__railInset`.

### Options minor 25: the scroll starts right of a nav rail

`anchorScroll` adds `lib.__railInset(ctx)` to the scroll's left anchor, and `lib:New` attaches
`OptionsNav.lua` after `OptionsScroll.lua`. Both reads are guarded: with no rail, or no
`OptionsNav.lua` in the copy, the scroll is anchored exactly as at minor 24.

### OptionsTabs minor 5: the strip and the content panel start right of a nav rail

`placeTabs` places every tab `lib.__railInset(ctx)` right of the chrome's left edge and wraps against
the chrome's width less that inset (never less than `TAB_MIN_W`, so the first render's zero-width
chrome cannot go negative; `replaceOnResize` re-places with the inset when the width arrives).
`drawContentPanel` moves the panel's left edge by the same inset. The banner, the header block and
the chrome divider stay full width. With no rail the numbers are minor 4's.

### What a consumer owes on re-vendoring v1.61.0

Copy both payloads whole and move the `CLAUDE.md` provenance line to v1.61.0 in the same commit, as
always; the kit does not move (27). Then, in the same commit so the suite stays green:

- **Surface-parity churn.** An Options degradation stub pinned with `Kit.assertSurfaceParity` by
  name goes red until it gains **`NavRail`** as a no-op (library-absent builds draw no panel). A
  stub checked through an explicit seam list (ConsumableMaster's `OPTIONS_SEAM`) is unaffected. The
  `__`-prefixed seams are outside parity.
- **Nothing else.** A page that draws no rail is laid out exactly as at v1.60.0; the load list
  derived from `LibKa0s.xml` picks up `OptionsNav.lua` with no change.
```

  - `docs/api/Options/version-24.31.4.7.4-docs.md`: `| Status | **Current** |` -> `| Status | Superseded |`;
    `| Superseded by | — |` -> `| Superseded by | [version 25.31.5.7.4.1](./version-25.31.5.7.4.1-docs.md) — the nav rail (`OptionsNav.lua`, a sixth file) |`;
    and append a final section:

```markdown
## Moving to version 25.31.5.7.4.1

`Options.lua` moves to minor **25** and `OptionsTabs.lua` to **5**, and a sixth file joins the
major, `OptionsNav.lua` at minor **1**, so the key gains a component. One instance member is added,
`O.NavRail`, and one library-level function, `lib.__railInset`. No existing member, descriptor
field or row field changes. A page that draws no rail is laid out exactly as at this version. A host
whose degradation stub is pinned by name adds a `NavRail` no-op.
```

  - Create `docs/api/Options/version-25.31.5.7.4.1-docs.md` as a copy of the 24.31.4.7.4 document
    **as it was before the edits just above** (`git show HEAD:docs/api/Options/version-24.31.4.7.4-docs.md > …`),
    then edit it:
    - Title: `` # `LibKa0s-Options-1.0` — version 25.31.5.7.4.1 ``.
    - `Files and minors`: `` `Options.lua` **25** · `OptionsWidgets.lua` **31** · `OptionsTabs.lua` **5** · `OptionsCompose.lua` **7** · `OptionsScroll.lua` **4** · `OptionsNav.lua` **1** ``.
    - `Version key`: `` `<Options>.<OptionsWidgets>.<OptionsTabs>.<OptionsCompose>.<OptionsScroll>.<OptionsNav>`, in load order — the same six numbers `lib.MODULES` reports. ``
    - `Shipped in` -> `v1.61.0`. `Status` stays `**Current**`. `Supersedes` ->
      `[version 24.31.4.7.4](./version-24.31.4.7.4-docs.md)`. `Superseded by` stays `—`.
    - `Requires`: append `; `OptionsNav.lua` requires `LibKa0s-Pool-1.0` minor ≥ 1 (`NEEDS_POOL = 1`), since 25.31.5.7.4.1`.
    - `Confirm in-game`: `{ Options = 25, OptionsWidgets = 31, OptionsTabs = 5, OptionsCompose = 7, OptionsScroll = 4, OptionsNav = 1 }`.
    - The `Since` legend: add `` `O25` for `Options.lua` minor 25, `T5` for `OptionsTabs.lua` minor 5, `N1` for `OptionsNav.lua` minor 1 ``.
    - Rename the heading `## What changed at this version` to `## Previously, at 24.31.4.7.4`, and
      insert above it a new `## What changed at this version` section. Its text is the three `###`
      sections of the CHANGELOG block above (OptionsNav 1, Options 25, OptionsTabs 5), each as a
      bold-led paragraph.
    - In `## The instance surface`'s member table, directly after the `SubTabStrip(ctx, parent, spec)`
      row, add:
      `` | `NavRail(ctx, spec)` | **N1** | The pinned nav rail, the first level of a page that edits one instance out of many (options-ui-§13): `spec = { entries = { { key, label, tooltip } }, value, onSelect, width }`, `width` 120 by default. Draw after `PageBanner`, before `TabStrip`. Records `ctx.railWidth`, which `lib.__railInset` turns into the inset the strip, the content panel and the scroll start at. Entries pooled per page, released on every call; the selected entry disabled; a click refused in combat by the library; `onSelect` pcall'd. The selection is the host's, as `SubTabStrip`'s is. Returns the entry buttons in rail order, or nil having drawn nothing (an empty list releases the rail, `railWidth` 0). | ``
    - In `## The library surface`, add a `` ### `lib.__railInset(ctx)` → number (N1) `` subsection:
      `ctx.railWidth + 12`, or `0` for no rail. It is read by `anchorScroll` (O25), `placeTabs` and
      `drawContentPanel` (T5), and every read is guarded, so a copy without `OptionsNav.lua` lays out as
      at 24.31.4.7.4.
  - `docs/api/README.md`: in the key-format table (:68) change the Options row's key to
    `` `<Options>.<OptionsWidgets>.<OptionsTabs>.<OptionsCompose>.<OptionsScroll>.<OptionsNav>` ``. In
    the "A key gains a component" prose (:77-79) append
    `, and six from `25.31.5.7.4.1` where `OptionsNav.lua` did`, after the `21.20.1.7.3` clause. In
    the Options table (:221) add the new top row
    `` | [25.31.5.7.4.1](./Options/version-25.31.5.7.4.1-docs.md) | `Options.lua` 25 · `OptionsWidgets.lua` 31 · `OptionsTabs.lua` 5 · `OptionsCompose.lua` 7 · `OptionsScroll.lua` 4 · `OptionsNav.lua` 1 | v1.61.0 | **Current** | ``
    and change the 24.31.4.7.4 row's status to `Superseded` and its "Shipped in" to `v1.56.0 – v1.60.0`.
  - Generate the manifest and the test inventory:

```sh
$B lua tools/gen-api-members.lua        # writes docs/api/Options/members-25.31.5.7.4.1.json
$B lua tests/run.lua --list > docs/test-cases.md
```

- [ ] **Step 8: Gate.** Run the LibKa0s gate. Expect 0 FAIL lines (`test_versioning`, `test_prose` and
  `test_surface_parity` included), luacheck 0/0, and no lizard output. Then:

```sh
wc -l LibKa0s/Options.lua LibKa0s/OptionsTabs.lua        # expect <= 1474 and <= 1494
for F in LibKa0s/OptionsNav.lua tests/test_options_nav.lua; do test "$(grep -c $'\r$' $F)" = "$(wc -l < $F)" && echo "$F CRLF"; done
git diff --stat
```

If `test_versioning` or `test_prose` names a file this step did not list, fix exactly what it names
in this commit and add the file to the `git add` below.

- [ ] **Step 9: Commit.**

```sh
git add LibKa0s/OptionsNav.lua LibKa0s/LibKa0s.xml LibKa0s/Options.lua LibKa0s/OptionsTabs.lua \
  tests/majors.lua tests/run.lua tests/test_options_nav.lua tests/test_options_combat.lua CHANGELOG.md \
  docs/api/README.md docs/api/Options/version-24.31.4.7.4-docs.md docs/api/Options/version-25.31.5.7.4.1-docs.md \
  docs/api/Options/members-25.31.5.7.4.1.json docs/test-cases.md
git commit -m "SR-LK-01: OptionsNav minor 1, the nav rail; Options 25 and OptionsTabs 5 read its one inset" \
  -m "O.NavRail(ctx, spec) draws the pinned first-level rail (options-ui-§13, standard v2.69.0) in the body, left of the chrome's tab area, in AceGUI's tree-pane look; entries pooled per page and released on every call; a click refused in combat by the library. lib.__railInset(ctx) = railWidth + 12, or 0, is read by anchorScroll (Options 25), placeTabs and drawContentPanel (OptionsTabs 5), every read guarded, so no rail is byte-identical to v1.60.0. The rail's top is level with the selected tab's art, measured off the active cap atlas. Options key 25.31.5.7.4.1. For AuraMaster#6." \
  -m "<attribution trailers>"
```

### Task SR-LK-02: prose and census for the sixth Options file

**Repo:** `$GIT/LibKa0s`, same branch.

**Files:**
- Modify: `README.md` :49-52 (the Options bullet), :65-67 (Installing, the bail-out sentence), :100 (the
  Options row: description, file list and API key), :220 and :226 (the `MODULES` paragraph), :278 (the
  file tree).
- Modify: `CLAUDE.md` :139, :194, :201, :228, :259, :265 and :268-269 (the band prose: the two
  capped files re-measured).
- Modify: `docs/releasing.md` :8 (the minor-constant list), :28 and :33-34 (the constant names),
  :42-48 (the Options `files` and `paired` arrays, and the key-component history), :226 (the payload
  count), :335-352 (the paired guards and the partial-copy bullet), and :386 (the Consumers row for
  `LibKa0s-Options-1.0`).
- Not touched: `CHANGELOG.md` (SR-LK-01 wrote the whole v1.61.0 block, the consumer note included) and
  `DEPENDENCIES.md` (it names no Options file: `grep -c OptionsScroll DEPENDENCIES.md` prints 0).

**Interfaces:** none. This task is prose only; no code or minor moves.

- [ ] **Step 1: Find every stale count.**

```sh
cd $GIT/LibKa0s
grep -n "twenty-two\|Five files\|five-file\|FIVE files\|SCROLL_MINOR\|paired\` array of four\|the four$\|OptionsScroll, __scrollMinor\|24\.31\.4\.7\.4\|Options = 24\|1457\|1489" \
  README.md CLAUDE.md docs/releasing.md
grep -c '<Script file=' LibKa0s/LibKa0s.xml       # expect 23
grep -c 'major = "LibKa0s-' tests/majors.lua        # expect 15
N_O=$(wc -l < LibKa0s/Options.lua); N_T=$(wc -l < LibKa0s/OptionsTabs.lua); echo "Options $N_O, OptionsTabs $N_T"
```

Expected: the sites under **Files**, plus historical mentions inside released release-notes paragraphs
("Where v1.5x.0 stood", CLAUDE.md :272's "1457 and 1489 as measured"), which stay as written.

- [ ] **Step 2: Make these exact edits** (anchor on the quoted text; line numbers are at `bed0eb1`).

  `README.md`:
  - :49-52, the Options bullet: replace `the header block and the secondary` + line break + `  strip),`
    with `the header block, the secondary` + line break + `  strip and the nav rail),`, and replace
    `Five files, one major.` with `Six files, one major.`
  - :65-67: replace `` `OptionsCompose.lua` and `OptionsScroll.lua` bail too on their own `` with
    `` `OptionsCompose.lua`, `OptionsScroll.lua` and `OptionsNav.lua` bail too on their own ``, and
    `the whole five-file module is absent` with `the whole six-file module is absent`.
  - :100, the `LibKa0s-Options-1.0` row: in the description replace
    `the tab strip every page draws, and the schema composers` with
    `the tab strip every page draws, the nav rail a page that edits one instance out of many may lead with, and the schema composers`;
    in the files column append `` , `OptionsNav.lua` `` after `` `OptionsScroll.lua` ``; replace the key
    cell `[24.31.4.7.4](docs/api/Options/version-24.31.4.7.4-docs.md)` with
    `[25.31.5.7.4.1](docs/api/Options/version-25.31.5.7.4.1-docs.md)`.
  - :220: replace `As of **v1.60.0**, which moves two majors' minors (DebugLog, which also gains the file `DebugLogDiagnostics`, and Slash) and adds no major:`
    with `As of **v1.61.0**, which moves one major's minors (Options, which also gains the file `OptionsNav`) and adds no major:`.
    The other majors' `MODULES` values on :220-227 are unchanged at v1.61.0 and stay.
  - :226: replace `` `Options = { Options = 24, OptionsWidgets = 31, OptionsTabs = 4, OptionsCompose = 7, OptionsScroll = 4 }`, ``
    with `` `Options = { Options = 25, OptionsWidgets = 31, OptionsTabs = 5, OptionsCompose = 7, OptionsScroll = 4, OptionsNav = 1 }`, ``.
  - :278: directly after the `OptionsScroll.lua` tree line, add (same column alignment):
    `  OptionsNav.lua     -- the nav rail a page may lead with, same module, NAV_MINOR of its own`

  `docs/releasing.md`:
  - :8: replace `` `TABS_MINOR` / `SCROLL_MINOR` / `COMPOSE_MINOR` `` with
    `` `TABS_MINOR` / `SCROLL_MINOR` / `NAV_MINOR` / `COMPOSE_MINOR` ``.
  - :28: `twenty-two, by their exact constant names` -> `twenty-three, by their exact constant names`.
    :34: `` in `OptionsScroll.lua`, `COMPOSE_MINOR` in `OptionsCompose.lua`, `` ->
    `` in `OptionsScroll.lua`, `NAV_MINOR` in `OptionsNav.lua`, `COMPOSE_MINOR` in `OptionsCompose.lua`, ``.
  - :42-46: `` a `files` list of five and a `` + line break + `` `paired` array of four ( `` ->
    `` a `files` list of six and a `` + line break + `` `paired` array of five ( ``, and
    `` `{ OptionsScroll, __scrollMinor, __scrollShellMinor }`). `` ->
    `` `{ OptionsScroll, __scrollMinor, __scrollShellMinor }`, `{ OptionsNav, __navMinor, __navShellMinor }`). ``
  - :48: `four from 14.13.1.3 and five from 21.20.1.7.3.` ->
    `four from 14.13.1.3, five from 21.20.1.7.3 and six from 25.31.5.7.4.1.`
  - :226: `the twenty-two `.lua` files` -> `the twenty-three `.lua` files`.
  - :335-337: `and the four` + line break + `  paired-minor guards` -> `and the` + line break +
    `  paired-minor guards`, and `` `OptionsScroll`, `PerfPanel`) `` -> `` `OptionsScroll`, `OptionsNav`, `PerfPanel`) ``.
  - :339-340: `FIVE files since` + line break + `  v1.39.0.` -> `SIX files since` + line break +
    `  v1.61.0 (five from v1.39.0).`
  - :341: `all three` + line break + `  attach files bail` -> `every` + line break + `  attach file bails`
    (the sentence wraps at :341-342; keep its other words).
  - :343-344: `` `OptionsCompose.lua` / `OptionsScroll.lua` fails to arrive `` ->
    `` `OptionsCompose.lua` / `OptionsScroll.lua` / `OptionsNav.lua` fails to arrive ``.
    :346: `` `if lib.__AttachCompose then … end` and `if lib.__AttachScroll then … end` `` ->
    `` `if lib.__AttachCompose then … end`, `if lib.__AttachScroll then … end` and `if lib.__AttachNav then … end` ``.
    :348: `` or `O.PatchAlwaysShowScrollbar`, `` -> `` `O.PatchAlwaysShowScrollbar`, or `O.NavRail`, ``.
    Directly before :352's closing line add the sentence
    `  A copy missing only `OptionsNav.lua` degrades rather than fails at layout: the three inset reads (`anchorScroll`, `placeTabs`, `drawContentPanel`) are guarded, so every page lays out as at v1.60.0 until a host calls `O.NavRail`.`
    and replace :352 `  Five files, one major, one copy.` with `  Six files, one major, one copy.`
  - :386, the `LibKa0s-Options-1.0` row: insert, before the row's closing ` |`, the sentence
    ` **`OptionsNav` minor 1 (v1.61.0), `O.NavRail`:** AuraMaster alone, on its unmerged `feat/2026-09-26-settings-redesign` (`settings/OptionsSetup.lua`'s `Helpers.RenderContainerPage`, the Containers page's rail, AuraMaster#6); the other ten hosts stay on v1.60.0 and add a `NavRail` no-op to an Options degradation stub pinned by name when they re-vendor, MultiMeters (#55) and KickCD (#33) the next adopters.`
    The consumers column (all eleven) does not change: every host consumes the major.

  `CLAUDE.md`, with `N_O` and `N_T` from Step 1 (write the numbers, and write the room left, `1500 - N`,
  in words as the file does):
  - :139: `is **1489** today, minor 22's combat lock, minor 23's dispatcher and,` ->
    `is **<N_T>** today, minor 22's combat lock, minor 23's dispatcher, minor 5's rail inset (`SR-LK-01`, v1.61.0) and,`
  - :194: `` `LibKa0s/OptionsTabs.lua` (1489; 1197 at the last write-out, `` ->
    `` `LibKa0s/OptionsTabs.lua` (<N_T> with `SR-LK-01`'s rail inset, 1489 before it; 1197 at the last write-out, ``
  - :201: `` `LibKa0s/Options.lua` (1457; 1312 at v1.40.0, `` ->
    `` `LibKa0s/Options.lua` (<N_O> with `SR-LK-01`'s rail inset and attach line, 1457 before it; 1312 at v1.40.0, ``
  - :228: `` `LibKa0s/OptionsTabs.lua` at 1489 eleven, `` -> `` `LibKa0s/OptionsTabs.lua` at <N_T> <1500 - N_T in words>, ``
  - :259: `` `LibKa0s/Options.lua` (1457) `` -> `` `LibKa0s/Options.lua` (<N_O>, measured after `SR-LK-01`) ``
  - :265: `` `LibKa0s/OptionsTabs.lua` (1489, measured after `LK-28`) `` ->
    `` `LibKa0s/OptionsTabs.lua` (<N_T>, measured after `SR-LK-01`) ``; :268-269 `with eleven lines of room` ->
    `with <1500 - N_T in words> lines of room`.
  - Keep the band list at :193-222 in descending order: if `N_T` passes 1493, `LibKa0s/OptionsTabs.lua`
    moves ahead of `tests/test_widgets.lua`. The two re-check triggers (1475, 1495) stay as they are,
    and :272's "1457 and 1489 as measured" is history and stays. If `wc -l tests/test_options_nav.lua`
    is 1000 or more, it joins the band list and :193's "Thirteen files" moves by one.

- [ ] **Step 3: Gate.** Run the LibKa0s gate (0 FAIL, luacheck 0/0, no lizard output; `test_prose`
  reads these files). Run the Step 1 grep again and expect only the historical mentions it names.

- [ ] **Step 4: Commit.**

```sh
git add README.md CLAUDE.md docs/releasing.md
git commit -m "SR-LK-02: recount for OptionsNav.lua: six Options files, twenty-three in all" \
  -m "README Options bullet, install note, module row, MODULES line and file tree; CLAUDE.md band re-measured; releasing.md constant list, the Options files/paired arrays, the payload count and the partial-copy prose; the Consumers row (AuraMaster takes v1.61.0 first)." \
  -m "<attribution trailers>"
git status --porcelain            # expect empty
```

### Task SR-LK-03: release v1.61.0 (local tag)

**Repo:** `$GIT/LibKa0s`, same branch. `docs/releasing.md` steps 7 and 9. Step 8, the re-vendor, is
SR-AM-01, for AuraMaster alone.

**Files:**
- Modify: `CHANGELOG.md` (the heading `## v1.61.0 — unreleased` -> `## v1.61.0 — <date>`, plus the
  Release gate line).
- Modify: `README.md` :3 (the standard pointer `, v2.68.0` -> `, v2.69.0`: compare it with
  `git -C $GIT/WowAddonStandards show feat/2026-09-26-settings-redesign:standards/STANDARDS.md | head -1`).
- Modify: `docs/releasing.md`: :7 (the semver example), :250 (the provenance template: it is the
  quoted line in this file itself, `> Bundles [LibKa0s](…) v1.60.0 (MIT).`, not a separate file),
  :434 (the "Where v1.60.0 stands" heading becomes "stood", and a new "Where v1.61.0 stands" paragraph
  goes above it) and :634-638 (the "Every step 8" paragraph). `:386` (the Consumers row) only if Step 2's
  re-sweep finds it stale.
- Create: `docs/automated-tests/<stamp>/` (the runner writes it) and its `ANALYSIS.md`. Modify
  `docs/automated-tests/RESULTS.md` (a row).

**Interfaces:** produces the local annotated tag **`v1.61.0`**, which SR-AM-01 extracts with
`git archive v1.61.0`.

- [ ] **Step 1: Preconditions.**

```sh
cd $GIT/LibKa0s
git status --porcelain                                              # expect empty
git log --format=%s master..HEAD | head                             # expect the SR-LK-02 and SR-LK-01 subjects
git -C $GIT/WowAddonStandards log --format=%s -1 feat/2026-09-26-settings-redesign   # expect "SR-WS-02: …"
git tag -l v1.61.0                                                  # expect empty (never re-cut)
git merge-base master HEAD | cut -c1-7                              # the v1.60.0 base (bed0eb1 at planning)
for a in AbsorbTracker AuraMaster BankLedger ConsumableMaster KickCD LootHistory MultiMeters PanelMaster PartyFrameEnhanced PrettyChat WhatGroup; do
  printf '%s: ' $a; git -C ../$a show master:CLAUDE.md | grep -oE 'Bundles \[LibKa0s\]\([^)]*\) v[0-9.]+' | grep -oE 'v[0-9.]+$'
done                                                                # expect v1.60.0 for all eleven
```

If a consumer does not print v1.60.0, write what it does print into Step 3's "Every step 8" paragraph
instead of the text given there.

- [ ] **Step 2: Re-sweep the Consumers table** (`docs/releasing.md` step 9), BEFORE anything is
  committed or tagged, so a stale row lands in the first release commit and the tag never has to move.
  Run the loop at `docs/releasing.md:212-215` from the LibKa0s root. Every file it prints must appear in
  the `LibKa0s-Options-1.0` row's (:386) third column or in the row of the major it looks up. If a file
  is missing, add it to that row's third column now; it is staged with Step 3's commit. Nothing
  printed that the table lacks: no edit.

- [ ] **Step 3: The first release commit.** Make exactly these edits:
  - `CHANGELOG.md`: `## v1.61.0 — unreleased` -> `## v1.61.0 — <YYYY-MM-DD>` (the execution date).
  - `README.md` :3: `Addon Standard](https://github.com/tusharsaxena/WowAddonStandards)**, v2.68.0` ->
    `Addon Standard](https://github.com/tusharsaxena/WowAddonStandards)**, v2.69.0`.
  - `docs/releasing.md` :7: `` | Repo semver (`v1.60.0`) | `` -> `` | Repo semver (`v1.61.0`) | ``.
  - `docs/releasing.md` :250: `> Bundles [LibKa0s](https://github.com/tusharsaxena/LibKa0s) v1.60.0 (MIT).` ->
    `> Bundles [LibKa0s](https://github.com/tusharsaxena/LibKa0s) v1.61.0 (MIT).`
  - `docs/releasing.md` :434: `**Where v1.60.0 stands (2026-09-26).**` -> `**Where v1.60.0 stood (2026-09-26).**`,
    and directly above it insert this paragraph, then one blank line:

```markdown
**Where v1.61.0 stands (<YYYY-MM-DD>).** Three LibStub minors move and one file is added:
`Options.lua` 25, `OptionsTabs.lua` 5 and the new `OptionsNav.lua` 1 (`LibKa0s-Options-1.0`
25.31.5.7.4.1, twenty-three files now), and the kit stays at **revision 27**; no `NEEDS_*` floor
rises. It is the library's half of the Ka0s WoW Addon Standard v2.69.0's nav rail (`options-ui-§13`,
`options-ui-§14`): `O.NavRail`, the pinned first level of a page that edits one instance out of many,
and `lib.__railInset`, the one inset the strip, the content panel and the scroll read, so a page with
no rail lays out exactly as at v1.60.0. AuraMaster#6 asked for it: its Containers page folds the
Filters, Layout, Bars, Icons and Text sub-pages under the rail. What a consumer owes is in the
`CHANGELOG.md` block: the copy, the provenance line, and a `NavRail` no-op in an Options degradation
stub pinned by name. Built on `feat/2026-09-26-settings-redesign`, stacked on v1.60.0 (`<merge-base>`),
and **not merged**: steps 1–7 are done on that branch, the tag `v1.61.0` exists **locally only**, on
it, and the tag's push, the branch's merge and `master`'s push wait on the owner's go-ahead.
**Step 8 is AuraMaster alone**, as v1.59.0's was; the other ten consumers stay on v1.60.0 until they
take the rail (MultiMeters#55 and KickCD#33 are next) or a later release.
```

  - `docs/releasing.md` :634-638: replace the paragraph that opens `**Every step 8 through v1.58.0 is done**`
    (through `… the other ten take v1.59.0 with it.`) with:

```markdown
**Every step 8 through v1.60.0 is done.** All eleven consumers bundle **v1.60.0** on `master`, and
each `CLAUDE.md` provenance line says so, re-measured on <YYYY-MM-DD> for v1.61.0 against each
consumer's own `master`. What is **not** done is v1.61.0's step 8 beyond AuraMaster: AuraMaster takes
it on its unmerged `feat/2026-09-26-settings-redesign` (see *Where v1.61.0 stands* above), and the
other ten stay on v1.60.0 until they take the nav rail or a later release.
```

  `<merge-base>` is Step 1's `git merge-base` output; `<YYYY-MM-DD>` is the execution date, the same in
  all three places. Run the LibKa0s gate (0 FAIL, luacheck 0/0, no lizard output), then:

```sh
git add CHANGELOG.md README.md docs/releasing.md
git commit -m "SR-LK-03: date v1.61.0 and roll the release pointers" -m "<attribution trailers>"
git status --porcelain            # expect empty
```

- [ ] **Step 4: The release battery.**

```sh
$B tests/_kit/run-automated-tests.sh --release 1.61.0
S=$(ls -d docs/automated-tests/*/ | sort | tail -1)manifest.json
jq -r '.release' "$S"                                         # expect 1.61.0
jq -r '.git.dirty' "$S"                                       # expect false
jq -r '.suites | to_entries[] | "\(.key) \(.value.status)"' "$S"   # expect lint pass, tests pass, complexity pass, perf skip
jq -r '.suites.complexity.warnings' "$S"                      # expect 0
```

If any suite is not `pass` (perf's standing `skip` apart), stop. Do not tag. Fix it in a new
`SR-LK-01R`/`SR-LK-02R` commit and re-run from Step 3's gate.

- [ ] **Step 5: The analysis and the second commit.** Write `docs/automated-tests/<stamp>/ANALYSIS.md`
  in the shape of `docs/automated-tests/20260926-034006/ANALYSIS.md`, add the `RESULTS.md` row, and end
  the v1.61.0 CHANGELOG block with the release-gate line, every figure read off `$S`:

```text
Release gate (`docs/automated-tests/<stamp>/`): lint pass, <warnings>/<errors> in <files> files;
tests pass, <total> tests, <failed> failed; complexity pass, <warnings> over CCN 15. Perf
SKIPPED, not measured — no `tests/perf.lua` — so the gate covered three suites, not four.
```

```sh
git add docs/automated-tests/<stamp> docs/automated-tests/RESULTS.md CHANGELOG.md
git commit -m "SR-LK-03: v1.61.0 release run, analysis and gate line" -m "<attribution trailers>"
git status --porcelain            # expect empty
```

- [ ] **Step 6: Check the tag's preconditions** (`docs/releasing.md` step 7) and tag, locally. This is
  the last step: the Consumers re-sweep (step 9) already ran in Step 2, so nothing is committed after
  the tag.

```sh
grep -l '"release": "1.61.0"' docs/automated-tests/*/manifest.json   # expect >= 1 path, <stamp> among them
test -f docs/automated-tests/<stamp>/ANALYSIS.md && echo present     # expect present
git tag -a v1.61.0 -m "LibKa0s v1.61.0: OptionsNav minor 1 (the nav rail); Options 25.31.5.7.4.1"
git tag -l v1.61.0 && git rev-parse --short v1.61.0^{}               # expect HEAD, the second SR-LK-03 commit
```

**Never** `git push --tags` or push `v1.61.0`. The feature branch is pushed at the M1 checkpoint only
if the owner authorized pushes, and the tag stays local either way. SR-LK-03 is not done until the tag
exists: `resume-state.sh` holds it, and SR-AM-01 behind it, until `v1.61.0` is present.

### M1 checkpoint

- WowAddonStandards: the docs gate over every `.md` changed on the branch versus `master`. Record the
  distinct section refs resolved, the relative links checked, the CR bytes (0) and a clean
  `diff --check`.
- LibKa0s: the gate on the tagged tree. Record the test totals, luacheck 0/0 in N files, lizard 0 over
  CCN 15, and the manifest path of the release run. `git tag -l v1.61.0` shows a local tag.
- If the owner authorized pushes at plan review: `git push -u origin feat/2026-09-26-settings-redesign`
  in both repos, plus `git push origin refs/notes/ka0s-review`. Never a tag.
- Append one row to this bundle's `checkpoints.tsv`:
  `<date>\tM1\t<evidence as above, with the pushed heads and notes shas, or "not pushed (not authorized)">; owner sign-off O1 (A2): <accepted | declined, fallback taken>`.

---

## M2 — AuraMaster

Every AuraMaster task works in `$GIT/AuraMaster` on `feat/2026-09-26-settings-redesign` and ends on the
AuraMaster gate. Rules that apply to every M2 task:

- **Citations move with the code.** `tests/test_docs.lua` checks every `file:line` citation in `docs/`.
  The line must exist, must not be blank or comment-only, and must sit within 3 lines of a name the
  citing sentence gives in backticks. A task that shifts lines in a cited file fixes the citations the
  gate names **in the same commit**: move each one to the line that now holds its named symbol.
- **The generated inventory moves with the tests.** A task that adds, renames or deletes a test
  regenerates `docs/test-cases.md` with `$B lua tests/run.lua --list > docs/test-cases.md` and commits
  it.
- **Line numbers are planning-time** (AuraMaster `3fdc667`). Earlier tasks shift them, so anchor every
  edit on the quoted code or the case name, and use the number only to find it.
- **The locale moves with its callers.** `tests/test_locale.lua` fails on an `L["…"]` missing from
  `locales/enUS.lua`, and on an enUS key nothing uses. Add and remove keys in the commit that adds or
  removes their callers.

### Task SR-AM-01: re-vendor LibKa0s v1.61.0

**Files:**
- Modify (copied): `libs/LibKa0s/**` from the tag. `tests/_kit/**` also comes from the tag, and is
  expected unchanged at kit 27.
- Modify: `CLAUDE.md` (last line, the provenance), `DEPENDENCIES.md` :85 and :92 (`v1.60.0` ->
  `v1.61.0`), `docs/module-map.md` :255 (the library row).
- Modify: `settings/OptionsSetup.lua` :265-280 (the degradation stub's no-op name list gains
  `"NavRail"`).
- Create: `docs/revendor/<YYYY-MM-DD>-v1.61.0/01_DELTA.md`, `02_CANDIDATES.md`, `03_DECISIONS.md` and
  `05_SUMMARY.md`, in the shape of `docs/revendor/2026-09-26-v1.60.0/`.

**Interfaces:** consumes the tag `v1.61.0` in `$GIT/LibKa0s`. Produces `NS.Helpers.NavRail` on the live
instance and a `NavRail` no-op on the library-absent stub.

- [ ] **Step 1: Preconditions.**

```sh
cd $GIT/AuraMaster
git branch --show-current                  # expect feat/2026-09-26-settings-redesign
git status --porcelain                     # expect empty
git -C $GIT/LibKa0s rev-parse --short v1.61.0^{}    # expect SR-LK-03's second commit
```

- [ ] **Step 2: Copy both payloads from the tag, never the working tree** (`/wow-addon:revendor-libka0s`
  :57-68, :178-179). Write `01_DELTA.md` from the two diffs **before** copying.

```sh
S=$(mktemp -d)
git -C $GIT/LibKa0s archive v1.61.0 LibKa0s testkit | tar -x -C "$S"
diff -rq "$S/LibKa0s" libs/LibKa0s ; diff -rq "$S/testkit" tests/_kit     # record both in 01_DELTA.md
cp -r "$S/LibKa0s/." libs/LibKa0s/
cp -r "$S/testkit/." tests/_kit/
```

Expected delta: `OptionsNav.lua` only in the tag; `Options.lua`, `OptionsTabs.lua` and
`LibKa0s.xml` differ; `tests/_kit` identical. Delete a file only if the diff shows it removed upstream.

- [ ] **Step 3: Roll the provenance** in `CLAUDE.md`, last line:
  `Bundles [LibKa0s](https://github.com/tusharsaxena/LibKa0s) v1.61.0 (MIT).` Change DEPENDENCIES.md
  :85 and :92 and module-map.md :255 from `v1.60.0` to `v1.61.0`.

- [ ] **Step 4: Run and see the parity case fail.**

```sh
$B lua tests/run.lua > /tmp/am-run.txt 2>&1; grep -E '^  FAIL' /tmp/am-run.txt
```

Expected: exactly `FAIL  parity: the Options stub carries every helper the host calls, off the load
path as a no-op`, naming `NavRail` as missing from the stub. `test_vendor_sync` passes, because the
bytes equal the tag's.

- [ ] **Step 5: Stub it.** In `settings/OptionsSetup.lua`'s no-op list (:273-275), change
  `"IdList", "UnnamedCandidates", "SelectTab",` to `"IdList", "UnnamedCandidates", "SelectTab", "NavRail",`.

- [ ] **Step 6: Gate.** Run the AuraMaster gate: 0 FAIL, luacheck 0/0, no lizard output. Write
  `02_CANDIDATES.md` (one candidate, `O.NavRail`, adopted by SR-AM-03), `03_DECISIONS.md` (adopt, by
  this plan) and `05_SUMMARY.md` (the gate figures).

- [ ] **Step 7: Commit.**

```sh
git add libs/LibKa0s CLAUDE.md DEPENDENCIES.md docs/module-map.md settings/OptionsSetup.lua docs/revendor/<YYYY-MM-DD>-v1.61.0
git commit -m "SR-AM-01: Re-vendor LibKa0s v1.61.0 and stub NavRail" \
  -m "Both payloads from the v1.61.0 tag: Options 24 -> 25, OptionsTabs 4 -> 5, the new OptionsNav minor 1 (key 25.31.5.7.4.1); kit unchanged at 27. CLAUDE.md provenance, DEPENDENCIES.md and module-map.md move with it. The library-absent stub gains NavRail for the Options surface-parity case. The rail is adopted in SR-AM-03." \
  -m "<attribution trailers>"
```

(Add `tests/_kit` to the `git add` if Step 2's diff was not empty.)

### Task SR-AM-02: the section registry, and the style gates as data

**Files:**
- Modify: `settings/OptionsSetup.lua` :217-224. The per-page `recordContainerPage` becomes the
  section registry, on both arms. :292 (the stub's `NS.RegisterContainerPage`). :535-537 (the live
  `NS.RegisterContainerPage` registers the section).
- Modify: `settings/Filters.lua` :748-765, `settings/Layout.lua` :631-638, `settings/Bars.lua` :206-214,
  `settings/Icons.lua` :124-132, `settings/Text.lua` :503-513 (each spec gains `tooltip`; Bars, Icons
  and Text also gain `style`).
- Modify: `modules/Diagnostics.lua` :533-538 (the comment names the registry).
- Modify: `locales/enUS.lua` (five tooltips added).
- Create: `tests/test_pages_rail.lua`. Modify: `tests/run.lua` (register it after `"test_pages_tabs",`).
- Modify (generated): `docs/test-cases.md`.

**Interfaces:**
- Produces: `NS.RegisterContainerSection(key, label, spec)`, `NS.ContainerSection(key) -> { key, label,
  spec, style, tooltip } | nil`, and `NS.ContainerPageDisabledFor[key] = function(c) return c.style ~=
  style end` for a section with `spec.style`. The section spec fields are
  `spec.style` (`"bars"|"icons"|"text"|nil`) and `spec.tooltip` (the rail entry's tooltip).
- Consumes: nothing new. `modules/Diagnostics.lua:534-545` `inUse` keeps reading
  `NS.ContainerPageDisabledFor[row.page]`, unchanged.

- [ ] **Step 1: Write the failing test.** Create `tests/test_pages_rail.lua` (CRLF):

```lua
-- tests/test_pages_rail.lua -- the Containers page as one page per container (#6): the section
-- registry, the band, the nav rail (General, Filters, Layout and the container's own style), the
-- selected section's tabs, deep links and Defaults, pinned from the outside.
-- Spec: docs/superpowers/specs/2026-09-26-settings-redesign-design.md.

local T = _G.AM_TEST
local test, assertEqual, assertTrue, assertFalse, assertNil =
    T.test, T.assertEqual, T.assertTrue, T.assertFalse, T.assertNil
local loadDegraded = dofile("tests/degraded_env.lua")

-- ── the registry ─────────────────────────────────────────────────────────────────────────────

test("sections: Filters, Layout, Bars, Icons and Text register as sections under their page keys", function()
    local NS = T.NS
    local LABELS = { filters = "Filters", layout = "Layout", bars = "Bars", icons = "Icons", text = "Text" }
    for key, label in pairs(LABELS) do
        local s = NS.ContainerSection(key)
        -- red under: a page file registering a Blizzard sub-page and no section
        assertTrue(s ~= nil, key .. " registered")
        assertEqual(s.key, key, key .. " keeps its page key: every row path is unchanged")
        assertEqual(s.label, NS.L[label], key .. "'s rail label")
        assertEqual(type(s.tooltip), "string", key .. " carries a rail tooltip")
    end
    assertEqual(NS.ContainerSection("bars").style, "bars")
    assertEqual(NS.ContainerSection("icons").style, "icons")
    assertEqual(NS.ContainerSection("text").style, "text")
    assertNil(NS.ContainerSection("filters").style, "Filters is every style's")
    assertNil(NS.ContainerSection("layout").style, "and Layout")
end)

-- Characterization: this case passes before and after SR-AM-02. It pins that the predicate
-- modules/Diagnostics.lua reads survives as data when the disabled notice goes (SR-AM-05).
test("sections: each style section's gate is derived from its style, on both builds (Diagnostics' inert split)", function()
    local function check(gates, build)
        for _, key in ipairs({ "bars", "icons", "text" }) do
            assertEqual(type(gates[key]), "function", build .. " " .. key)
            -- red under: the gate testing the style the wrong way round
            assertFalse(gates[key]({ style = key }), build .. " " .. key .. " is in use on its own style")
            assertTrue(gates[key]({ style = "nope" }), build .. " " .. key .. " is inert on another")
        end
        assertNil(gates.filters, build .. ": Filters is never inert by style")
        assertNil(gates.layout, build .. ": Layout neither")
    end
    check(T.NS.ContainerPageDisabledFor, "live")
    -- red under: the registry defined inside the live arm only (a library-absent /am diagnostics
    -- would call every Bars row on an icons container in use)
    check(loadDegraded().ContainerPageDisabledFor, "library-absent")
end)
```

Register it: in `tests/run.lua`, after `"test_pages_tabs",` add `"test_pages_rail",`.

- [ ] **Step 2: Run and see it fail.**

```sh
$B lua tests/run.lua > /tmp/am-run.txt 2>&1; grep -E '^  (FAIL|PASS)  sections:' /tmp/am-run.txt
```

Expected: `FAIL  sections: Filters, Layout, … register as sections …`, with an error like
`attempt to call field 'ContainerSection' (a nil value)`. `PASS  sections: each style section's gate …`
(the characterization).

- [ ] **Step 3: Implement the registry.** In `settings/OptionsSetup.lua`, replace :217-224 (the three
  comment lines `-- Each per-container page's style gate …` through the end of `recordContainerPage`)
  with:

```lua
-- ---------------------------------------------------------------------------
-- The Containers page's sections (#6)
-- ---------------------------------------------------------------------------
--
-- One config page per container (docs/superpowers/specs/2026-09-26-settings-redesign-design.md): the
-- Containers page draws a nav rail whose entries are these sections, and a section renders its own
-- page key's rows through Helpers.RenderPage exactly as the sub-page it replaced did. A section IS a
-- former page key, so every row path, /am set and Defaults are unchanged. Each settings/<section>.lua
-- registers at FILE LOAD, and the registry lives on BOTH arms: a library-absent build still needs the
-- style gates below.
local sections = {}

-- Each style section's gate, by page key: modules/Diagnostics.lua reads it to tell a stored value the
-- container's style leaves unused from one in use (B9 DX-2). Derived from the section's `style` --
-- the same fact that decides whether the rail lists it -- so the two cannot disagree.
NS.ContainerPageDisabledFor = NS.ContainerPageDisabledFor or {}

--- Register one section of the Containers page.
--- @param key string    the section's page key: the `page` its schema rows carry
--- @param label string  the rail entry's label
--- @param spec table    Helpers.RenderPage's page spec, plus `style` (listed on the rail only for a
---                      container drawn in that style) and `tooltip` (the rail entry's)
function NS.RegisterContainerSection(key, label, spec)
    spec = spec or {}
    local style = spec.style
    sections[key] = { key = key, label = label, spec = spec, style = style, tooltip = spec.tooltip }
    NS.ContainerPageDisabledFor[key] = style and function(c) return c.style ~= style end or nil
end

--- The registered section `key`, or nil. Read-only: for the suite and the Containers page.
function NS.ContainerSection(key) return sections[key] end
```

  Then:
  - The stub (:292):
    `NS.RegisterContainerPage = function(pageKey, title, _, spec) NS.RegisterContainerSection(pageKey, title, spec) end`
  - The live `NS.RegisterContainerPage` (:536): `recordContainerPage(pageKey, spec)` ->
    `NS.RegisterContainerSection(pageKey, title, spec)`.
  - The five specs gain these fields (first thing in each spec table):
    - `settings/Filters.lua` :748: `tooltip = L["Which auras this container shows, and in what order."],`
    - `settings/Layout.lua` :631: `tooltip = L["Where this container sits, what it attaches to, which way it grows, and how it answers the mouse."],`
    - `settings/Bars.lua` :206: `style = "bars", tooltip = L["How this container's bars look."],`
    - `settings/Icons.lua` :124: `style = "icons", tooltip = L["How this container's icons look."],`
    - `settings/Text.lua` :503: `style = "text", tooltip = L["How this container's lines of text look."],`
    Their `disabledFor` and `disabledNotice` stay until SR-AM-05. The sub-pages still draw them.
  - `locales/enUS.lua`: add the five keys, `L["…"] = "…"` each, beside the page's other strings.
  - `modules/Diagnostics.lua` :533-537: the comment's last sentence becomes
    `The page gate is each style section's own style, recorded by NS.RegisterContainerSection (settings/OptionsSetup.lua).`

- [ ] **Step 4: Run and see it pass.** The same grep shows both `sections:` cases `PASS`. `test_diagnostics`'s
  "[Cfg] lists only the settings in use; the rest go on an inert line" still passes.

- [ ] **Step 5: Gate.** Run the AuraMaster gate, fix the citations it names (the rules at the top of
  M2), and regenerate `docs/test-cases.md`.

- [ ] **Step 6: Commit.**

```sh
git add settings/OptionsSetup.lua settings/Filters.lua settings/Layout.lua settings/Bars.lua settings/Icons.lua \
  settings/Text.lua modules/Diagnostics.lua locales/enUS.lua tests/test_pages_rail.lua tests/run.lua docs/test-cases.md
git commit -m "SR-AM-02: the Containers section registry; the style gates become data" \
  -m "NS.RegisterContainerSection(key, label, spec) records each of Filters, Layout, Bars, Icons and Text as a section of the Containers page (#6) on both arms; a style section's Diagnostics gate is derived from its spec.style instead of its disabledFor. The sub-pages still register and draw as before; SR-AM-03 draws the rail from this registry." \
  -m "<attribution trailers>"
```

(Add any docs file whose citations the gate moved.)

### Task SR-AM-03: the Containers page renderer — band, rail, section

**Files:**
- Modify: `settings/OptionsSetup.lua`. In the registry block from SR-AM-02, add `SECTION_ORDER` and
  `GENERAL_SECTION`. Replace :519-522 (`Helpers.RenderContainerPage`) with the rail page block below.
  :545 (the sub-pages' renderer calls `Helpers.RenderPage` with `Helpers.ContainerBanner`). Update the
  `RenderPage` doc comment at :490 ("every per-container page through RenderContainerPage" -> "the
  sub-pages with Helpers.ContainerBanner as `banner`, and the Containers page through
  RenderContainerPage").
- Modify: `settings/Containers.lua` :234-278. General becomes a section, and the builder binds the
  page and renders through `RenderContainerPage`.
- Modify: `locales/enUS.lua` (General's rail tooltip).
- Modify: `tests/page_helpers.lua` (after :24: `P.drawnRail` and `P.rail`).
- Modify: `tests/test_pages_rail.lua` (the rail cases appended).
- Modify: `tests/test_options_descriptor.lua` :265, :283, :305, :322, :328 (a direct
  `RenderContainerPage(ctx, "bars", spec)` becomes `RenderPage(ctx, "bars", spec, ContainerBanner)`),
  :333-346 (the banner case rewritten).
- Modify (generated): `docs/test-cases.md`.

**Interfaces:**
- Produces: `Helpers.RenderContainerPage(ctx, band)` (**new signature**, the Containers page's
  renderer; `band` = `Helpers.ContainerBanner`'s opts, `{ tooltip, action }`), and
  `Helpers.__bindContainersPage(ctx)` (sets `ctx.sectionTabs = {}`, sets
  `ctx.activeSection = "containers"`, and records `Helpers.__pageCtx.containers`). ctx fields:
  `ctx.activeSection`, `ctx.sectionTabs[sectionKey] = tabKey` and `ctx.__renderedSection`.
- Test helpers produced: `P.drawnRail(ctx) -> { entries, value }` and `P.rail(key) -> widgets`.
- Consumes: `Helpers.NavRail` (SR-AM-01), `NS.ContainerSection`/the registry (SR-AM-02),
  `Helpers.RenderPage`, `Helpers.ContainerBanner` and `Helpers.RefreshPanel`.

- [ ] **Step 1: The test helpers.** In `tests/page_helpers.lua`, directly after the `NS.Helpers.TabStrip`
  wrapper (:19-24), add:

```lua
    -- The rail each page's last render drew, recorded off the library's NavRail as it is called,
    -- the way `drawn` records the strip. Weak-keyed, like it.
    local rails = setmetatable({}, { __mode = "k" })
    local navRail = NS.Helpers.NavRail
    NS.Helpers.NavRail = function(ctx, spec, ...)
        if type(ctx) == "table" and type(spec) == "table" then rails[ctx] = spec end
        return navRail(ctx, spec, ...)
    end

    --- The rail `ctx`'s last render drew: `{ entries = { { key, label, tooltip } }, value }`.
    function P.drawnRail(ctx)
        local spec = rails[ctx] or {}
        return { entries = spec.entries or {}, value = spec.value }
    end
```

  and, after `P.tabKeys` (:170-174):

```lua
    --- Click the rail entry `key` on the Containers page and answer what the render it asks for drew.
    --- A kit panel is hidden, so the click marks the page owed a render and the show draws it. The
    --- button is the library's rail ledger (`ctx.__railKids`, in rail order).
    function P.rail(key)
        local ctx = NS.Helpers.__pageCtx.containers
        for i, e in ipairs(P.drawnRail(ctx).entries) do
            if e.key == key then
                return P.during(function()
                    ctx.__railKids[i]:__fire("OnClick")
                    ctx.panel:__fire("OnShow")
                end)
            end
        end
        error("the rail drew no entry " .. tostring(key), 2)
    end
```

- [ ] **Step 2: Write the failing tests.** Append to `tests/test_pages_rail.lua`. Add these two lines
  under the existing `local loadDegraded …`:

```lua
local fresh = dofile("tests/fresh_env.lua")
local pages = dofile("tests/page_helpers.lua")
```

  then append:

```lua
-- ── the page ─────────────────────────────────────────────────────────────────────────────────

local function env()
    local NS, m = fresh()
    return NS, m, pages(NS, m)
end

local function railKeys(P, ctx)
    local out = {}
    for i, e in ipairs(P.drawnRail(ctx).entries) do out[i] = e.key end
    return table.concat(out, ",")
end

test("rail: Containers draws General, Filters, Layout and the selected container's own style, in that order", function()
    local NS, _, P = env()
    local ctx = NS.Helpers.__pageCtx.containers
    local L = NS.L
    NS.Helpers.SelectContainer(1)                   -- drawn as bars
    P.show("Containers")
    -- red under: the style entries filtered the wrong way round, or listed in TOC order
    assertEqual(railKeys(P, ctx), "containers,filters,layout,bars")
    local labels = {}
    for i, e in ipairs(P.drawnRail(ctx).entries) do labels[i] = e.label end
    assertEqual(table.concat(labels, ","), table.concat({ L["General"], L["Filters"], L["Layout"], L["Bars"] }, ","))
    NS.Helpers.SelectContainer(2)                   -- icons
    P.show("Containers")
    assertEqual(railKeys(P, ctx), "containers,filters,layout,icons")
    NS.Helpers.SelectContainer(4)                   -- text
    P.show("Containers")
    assertEqual(railKeys(P, ctx), "containers,filters,layout,text")
end)

test("rail: the page opens on General, today's one General tab under the band, beside a 120px rail", function()
    local NS, _, P = env()
    local ctx = NS.Helpers.__pageCtx.containers
    local ws = P.show("Containers")
    assertEqual(ctx.activeSection, "containers")
    assertEqual(P.drawnRail(ctx).value, "containers")
    assertEqual(table.concat(P.tabKeys("containers"), ","), NS.L["General"])
    assertTrue(P.find(ws, "Button", NS.L["New container"]) ~= nil, "the band keeps New container")
    assertEqual(ctx.railWidth, 120)
end)

test("rail: the draw order is PageBanner, NavRail, TabStrip", function()
    local NS, _, P = env()
    local H = NS.Helpers
    local order = {}
    for _, name in ipairs({ "PageBanner", "NavRail", "TabStrip" }) do
        local real = H[name]
        H[name] = function(...)
            order[#order + 1] = name
            return real(...)
        end
    end
    P.show("Containers")
    -- red under: the rail drawn before the banner (its top ignores the band) or after the strip
    -- (the strip places itself with no inset)
    assertEqual(table.concat(order, ","), "PageBanner,NavRail,TabStrip")
end)

test("rail: a rail click draws that section's strip and rows under the same band", function()
    local NS, _, P = env()
    local ctx = NS.Helpers.__pageCtx.containers
    NS.Helpers.SelectContainer(1)
    P.show("Containers")
    local ws = P.rail("layout")
    assertEqual(ctx.activeSection, "layout")
    assertEqual(P.drawnRail(ctx).value, "layout")
    local want, seen = {}, {}
    for _, row in ipairs(NS.SchemaForPage("layout")) do
        if not seen[row.group] then
            seen[row.group] = true
            want[#want + 1] = row.group
        end
    end
    -- red under: the section rendered under the Containers page key (General's rows, not Layout's)
    assertEqual(table.concat(P.tabKeys("containers"), ","), table.concat(want, ","))
    assertTrue(P.find(ws, "Dropdown", NS.L["Container"]) ~= nil, "the band is drawn with the section")
end)

test("rail: each section keeps its own tab: Filters, Categories, Layout, back to Filters lands on Categories (smoke 5)", function()
    local NS, _, P = env()
    local ctx = NS.Helpers.__pageCtx.containers
    local L = NS.L
    NS.Helpers.SelectContainer(1)
    P.show("Containers")
    P.rail("filters")
    P.tab("containers", L["Categories"])            -- the library's own strip click: no host render
    assertEqual(ctx.activeTab, L["Categories"])
    P.rail("layout")
    assertEqual(ctx.activeTab, P.tabKeys("containers")[1], "Layout opens on its first tab")
    P.tab("containers", L["Anchor"])
    P.rail("filters")
    -- red under: the tab kept only in the scalar ctx.activeTab (Filters reopens on its first tab),
    -- or stashed only on a host render (the strip click above never reaches the host)
    assertEqual(ctx.activeTab, L["Categories"])
    P.rail("layout")
    assertEqual(ctx.activeTab, L["Anchor"])
    P.rail("containers")
    P.rail("filters")
    assertEqual(ctx.activeTab, L["Categories"], "and through General too")
end)

test("rail: a Style change heals an active style section to the new style's entry; other sections stay (smoke 4)", function()
    local NS, _, P = env()
    local ctx = NS.Helpers.__pageCtx.containers
    NS.Helpers.SelectContainer(1)                   -- bars
    P.show("Containers")
    P.rail("bars")
    NS.SetByPath("container.style", "icons", 1)
    NS.Helpers.RefreshAllPanels()
    P.show("Containers")
    -- red under: the heal falling back to General, or keeping a section the rail no longer lists
    assertEqual(ctx.activeSection, "icons")
    assertEqual(railKeys(P, ctx), "containers,filters,layout,icons")
    P.rail("filters")
    NS.SetByPath("container.style", "text", 1)
    NS.Helpers.RefreshAllPanels()
    P.show("Containers")
    assertEqual(ctx.activeSection, "filters", "a section every style has is kept")
end)

test("rail: choosing a container of another style in the band moves Bars to Icons", function()
    local NS, _, P = env()
    local ctx = NS.Helpers.__pageCtx.containers
    NS.Helpers.SelectContainer(1)
    P.show("Containers")
    P.rail("bars")
    P.banner(ctx):__fire("OnValueChanged", 2)      -- the starter icon container
    P.show("Containers")
    assertEqual(ctx.activeSection, "icons")
    assertEqual(P.drawnRail(ctx).value, "icons")
end)

test("rail: with no containers the rail lists General alone, which says how to make one", function()
    local NS, _, P = env()
    local ctx = NS.Helpers.__pageCtx.containers
    for _, c in ipairs(NS.Database.GetContainers()) do NS.ContainerManager.Delete(c.id) end
    local ws = P.rerender("Containers")
    -- red under: a section that needs a container offered with none (an empty page under a strip)
    assertEqual(railKeys(P, ctx), "containers")
    assertTrue(P.hasText(ws, NS.L["No containers yet. Click New container, or type /am new."]))
end)
```

- [ ] **Step 3: Run and see them fail.**

```sh
$B lua tests/run.lua > /tmp/am-run.txt 2>&1; grep -E '^  (FAIL|PASS)  rail:' /tmp/am-run.txt
```

Expected: every `rail:` case `FAIL`s. `railKeys` is empty and there is no `NavRail` call, or they
error on `__pageCtx.containers` having no `sectionTabs`.

- [ ] **Step 4: Implement.** In `settings/OptionsSetup.lua`'s registry block (SR-AM-02), directly
  under `local sections = {}`, add:

```lua
-- The rail's order: General first (options-ui-§14: the page opens on it), then Filters, Layout and
-- the one style section the container is drawn in. Not the TOC's order: the page files load in any.
local GENERAL_SECTION = "containers"
local SECTION_ORDER = { GENERAL_SECTION, "filters", "layout", "bars", "icons", "text" }
```

  Replace `Helpers.RenderContainerPage` (:519-522) with:

```lua
-- ---------------------------------------------------------------------------
-- The Containers page: the band, the nav rail, and the selected section's tabs (#6)
-- ---------------------------------------------------------------------------
--
-- The rail lists General, Filters, Layout and the ONE style section the selected container is drawn
-- in; each section renders through Helpers.RenderPage with its own page key and spec, so every row,
-- default and slash path is the sub-page's it replaced. The section, and each section's tab, are
-- session state on the ctx and never persisted (options-ui-§13).

--- The sections the rail lists for container `cfg`, in rail order. General always (it is where a
--- container is made); the rest only with a container, and a style section only for its own style.
local function railSections(cfg)
    local out = {}
    for _, key in ipairs(SECTION_ORDER) do
        local s = sections[key]
        if s and (key == GENERAL_SECTION or (cfg and (s.style == nil or s.style == cfg.style))) then
            out[#out + 1] = s
        end
    end
    return out
end

--- The section to draw: the one the page holds while the rail still lists it; else, when it held a
--- style section, the container's own style section (a Style change renames the entry, spec §3);
--- else the first.
local function settleSection(ctx, list)
    local held = sections[ctx.activeSection]
    local fallback = list[1]
    for _, s in ipairs(list) do
        if s.key == ctx.activeSection then return s end
        if held and held.style and s.style then fallback = s end
    end
    return fallback
end

--- Keep the tab the page is on for the section it last drew. Called before ANYTHING moves the
--- section: a strip click is the library's alone (O.RenderTabbedSchema re-renders the strip and the
--- body without calling back here), so just before leaving is the one moment the host sees the tab.
local function stashTab(ctx)
    local drawn = ctx.__renderedSection
    if drawn then ctx.sectionTabs[drawn] = ctx.activeTab end
    ctx.__renderedSection = nil
end

--- Bind the Containers page's ctx (settings/Containers.lua's builder). The page opens on General.
function Helpers.__bindContainersPage(ctx)
    ctx.sectionTabs = {}
    ctx.activeSection = GENERAL_SECTION
    Helpers.__pageCtx[GENERAL_SECTION] = ctx
end

--- Render the Containers page: the container band (`band` = ContainerBanner's { tooltip, action }),
--- then the nav rail, then the selected section's strip and tab -- the library's draw order,
--- PageBanner, NavRail, TabStrip (options-ui-§13, §14).
function Helpers.RenderContainerPage(ctx, band)
    ctx.sectionTabs = ctx.sectionTabs or {}
    stashTab(ctx)
    local list = railSections(NS.ActiveContainer())
    local section = settleSection(ctx, list)
    ctx.activeSection = section.key
    ctx.activeTab = ctx.sectionTabs[section.key]
    local entries = {}
    for i, s in ipairs(list) do entries[i] = { key = s.key, label = s.label, tooltip = s.tooltip } end
    Helpers.RenderPage(ctx, section.key, section.spec, function(c)
        Helpers.ContainerBanner(c, band)
        Helpers.NavRail(c, {
            entries  = entries,
            value    = section.key,
            onSelect = function(key)
                stashTab(c)
                c.activeSection = key
                Helpers.RefreshPanel(c, true)
            end,
        })
    end)
    ctx.__renderedSection = section.key
end
```

  In `NS.RegisterContainerPage` (:545), the sub-pages keep drawing as before:
  `Helpers.SetRenderer(ctx, function(c) Helpers.RenderPage(c, pageKey, spec, Helpers.ContainerBanner) end)`.

  In `settings/Containers.lua`, replace the `PAGE_SPEC` table and its comment (:234-243) with the
  section registration below. Delete `local function banner` and `local function renderPage`
  (:258-262). Keep `BAND` (:245-257) as it is:

```lua
-- The page's General section (#6): this file's one tab, now the first entry on the Containers
-- page's nav rail. Every tab draws whether or not a container exists (the render above handles the
-- empty case itself), which is why it is the rail's one entry when there is none.
NS.RegisterContainerSection(PAGE, L["General"], {
    addonWide = true,
    tooltip   = L["Name this container, choose what it shows and how it is drawn, and duplicate, delete or copy settings onto it."],
    tabs      = { { key = GROUP, label = GROUP, render = render } },
})
```

  and in `build` (:264-276) replace `H.__pageCtx[PAGE] = ctx` and `H.SetRenderer(ctx, renderPage)` with:

```lua
    H.__bindContainersPage(ctx)
    -- Through SetRenderer, which owns WHEN the page draws and refuses under combat (options-ui-§11).
    H.SetRenderer(ctx, function(c) H.RenderContainerPage(c, BAND) end)
```

  `locales/enUS.lua`: add
  `L["Name this container, choose what it shows and how it is drawn, and duplicate, delete or copy settings onto it."]`.

  `tests/test_options_descriptor.lua`: at :265, :283, :305 and :322, change
  `NS2.Helpers.RenderContainerPage(ctx, "bars", X)` to `NS2.Helpers.RenderPage(ctx, "bars", X, NS2.Helpers.ContainerBanner)`.
  At :328, change `pcall(NS2.Helpers.RenderContainerPage, ctx, "bars", spec)` to
  `pcall(NS2.Helpers.RenderPage, ctx, "bars", spec, NS2.Helpers.ContainerBanner)`. Replace the case at
  :333-346 with:

```lua
test("options descriptor: RenderPage draws no banner; a banner hook draws the container band first", function()
    local NS2, m2 = fresh()
    local P = pages(NS2, m2)
    NS2.Helpers.__pageCtx.containers.panel:__fire("OnShow")
    assertTrue(P.banner(NS2.Helpers.__pageCtx.containers) ~= nil, "the Containers page draws the band")
    local ctx = NS2.Helpers.__pageCtx.general
    local strips = counter(NS2.Helpers, "TabStrip")
    NS2.Helpers.RenderPage(ctx, "general", { addonWide = true })
    -- red under: RenderPage drawing the container banner (General would grow one, against D1)
    assertNil(P.banner(ctx))
    assertEqual(strips[1], 1, "the strip is still drawn")
    NS2.Helpers.RenderPage(ctx, "general", { addonWide = true }, NS2.Helpers.ContainerBanner)
    assertTrue(P.banner(ctx) ~= nil, "and a banner hook draws it")
end)
```

- [ ] **Step 5: Run and see them pass.** The `rail:` grep shows every case `PASS`, and nothing else
  `FAIL`s. The sub-pages are untouched.

- [ ] **Step 6: Gate.** Run the AuraMaster gate (0 FAIL, luacheck 0/0, no lizard output), fix the
  citations it names, regenerate `docs/test-cases.md`, and check `wc -l settings/OptionsSetup.lua`
  (< 1500).

- [ ] **Step 7: Commit.**

```sh
git add settings/OptionsSetup.lua settings/Containers.lua locales/enUS.lua tests/page_helpers.lua \
  tests/test_pages_rail.lua tests/test_options_descriptor.lua docs/test-cases.md
git commit -m "SR-AM-03: the Containers page draws the band, the nav rail and the selected section" \
  -m "Helpers.RenderContainerPage(ctx, band) renders PageBanner, NavRail, then the section's RenderTabbedSchema through RenderPage with that section's page key and spec (#6, spec §2-§3). The rail lists General, Filters, Layout and the container's own style; ctx.activeSection and ctx.sectionTabs are session state, the tab stashed before anything moves the section so a strip click is remembered too; a Style or container change heals a style section to the new style. General is Containers' old tab, now a section. The sub-pages still register until SR-AM-05." \
  -m "<attribution trailers>"
```

### Task SR-AM-04: deep links, `SelectSection`, the `SelectTab` route, Defaults for the active section

**Files:**
- Modify: `settings/OptionsSetup.lua`. `NS.OpenOptionsPage` (:329-340) maps a section key to Containers.
  `Helpers.__bindContainersPage` records the ctx. `Helpers.SelectSection` and the `SelectTab` wrapper
  go directly after `Helpers.RenderContainerPage`. The stub's no-op list (:265-280) gains
  `"SelectSection"`.
- Modify: `settings/Containers.lua` `build` (:264-276): the Defaults tooltip and the click closure.
- Modify: `locales/enUS.lua`. Add the new Defaults tooltip. Remove
  `L["Restore the selected container's Enabled, Unit, Aura type and Style to its addon default. Its name is kept."]` (:154).
- Modify: `tests/test_pages_rail.lua` (the cases below appended), `tests/test_options_descriptor.lua`
  :431-456, `tests/test_pages_containers.lua` :96-135 and :558-562 (the Defaults-tooltip case; its `assertEqual` is at :561).
- Modify (generated): `docs/test-cases.md`.

**Interfaces:**
- Produces: `Helpers.SelectSection(key, tabKey?) -> boolean`. It is refused in combat. It is false for
  an unbuilt page and for a section the rail does not list. On success it stashes the current tab,
  sets `activeSection` (and `sectionTabs[key] = tabKey` when given), and runs
  `Helpers.RefreshPanel(ctx, true)`. It also produces `Helpers.SelectTab(pageKey, tabKey)`, the
  library's for a page key and `SelectSection` for a section key. `NS.OpenOptionsPage(pageKey)` keeps
  its signature.
- Consumes: `Helpers.__combatRefused()` (the library's refusal), plus `railSections` and `stashTab`
  (SR-AM-03).

- [ ] **Step 1: Write the failing tests.** Append to `tests/test_pages_rail.lua`:

```lua
-- ── deep links, SelectTab, Defaults ─────────────────────────────────────────────────────────

--- A fresh environment whose subcategories answer GetID, as the client's do, and which records the
--- category every OpenToCategory lands on, by its tree label.
local function recordingOpens()
    local byId, opened = {}, {}
    local NS, m = fresh({ before = function(mk)
        local register = mk.Settings.RegisterCanvasLayoutSubcategory
        local count = 0
        mk.Settings.RegisterCanvasLayoutSubcategory = function(parent, panel, name)
            local cat = register(parent, panel, name)
            count = count + 1
            local id = 100 + count
            byId[id] = name
            cat.GetID = function() return id end
            return cat
        end
        mk.Settings.OpenToCategory = function(id) opened[#opened + 1] = byId[id] or "main" end
    end })
    return NS, m, pages(NS, m), opened
end

test("rail: a former sub-page key opens Containers on that section, drawn on the next show (smoke 7)", function()
    local NS, _, P, opened = recordingOpens()
    local ctx = NS.Helpers.__pageCtx.containers
    NS.Helpers.SelectContainer(1)
    P.show("Containers")
    P.rail("filters")
    -- The frame picker closes the settings window and reopens "layout" when the pick lands
    -- (settings/Layout.lua's pickFrame): the page is hidden, so the section is owed, then drawn.
    NS.OpenOptionsPage("layout")
    -- red under: OpenOptionsPage looking the key up in the category table alone
    assertEqual(opened[#opened], NS.L["Containers"])
    assertEqual(ctx.activeSection, "layout", "selected before the show")
    P.show("Containers")
    assertEqual(P.drawnRail(ctx).value, "layout", "and drawn on it")
end)

test("rail: a style key the container is not drawn in opens Containers and moves nothing; Containers keeps the section", function()
    local NS, _, P, opened = recordingOpens()
    local ctx = NS.Helpers.__pageCtx.containers
    NS.Helpers.SelectContainer(1)                   -- bars
    P.show("Containers")
    P.rail("filters")
    NS.OpenOptionsPage("icons")
    assertEqual(opened[#opened], NS.L["Containers"])
    -- red under: a section selected that the rail does not list (an empty page under the strip)
    assertEqual(ctx.activeSection, "filters")
    NS.OpenOptionsPage("containers")
    -- red under: the anchor's right-click (modules/Anchors.lua) dropping the player back on General
    assertEqual(ctx.activeSection, "filters")
end)

test("rail: SelectTab on a section key selects the section and its tab; on the General page it is the library's", function()
    local NS, _, P = env()
    local ctx = NS.Helpers.__pageCtx.containers
    local L = NS.L
    NS.Helpers.SelectContainer(1)
    P.show("Containers")
    -- red under: the call reaching the library's SelectTab, which finds no "filters" page to hold it
    assertTrue(NS.Helpers.SelectTab("filters", L["Sorting"]))
    P.show("Containers")
    assertEqual(ctx.activeSection, "filters")
    assertEqual(ctx.activeTab, L["Sorting"])
    P.show("General")
    assertTrue(NS.Helpers.SelectTab("general", L["Spell Categories"]), "the addon page is the library's")
    assertEqual(NS.Helpers.__pageCtx.general.activeTab, L["Spell Categories"])
end)

test("rail: selecting a section is refused in combat and moves nothing", function()
    local NS, m, P = env()
    local ctx = NS.Helpers.__pageCtx.containers
    P.show("Containers")
    m.__lockdown = true
    -- red under: SelectSection without the library's refusal (a structural re-render in combat)
    assertFalse(NS.Helpers.SelectSection("layout"))
    m.__lockdown = false
    assertEqual(ctx.activeSection, "containers")
end)

test("rail: Defaults restores only the active section's rows for the selected container (smoke 6)", function()
    local NS, m, P = env()
    local T0 = NS.CONTAINER_TEMPLATE
    NS.Helpers.SelectContainer(1)
    P.show("Containers")
    P.rail("layout")
    NS.SetByPath("container.layout.spacing", 9, 1)
    NS.SetByPath("container.bars.width", 300, 1)
    NS.SetByPath("container.enabled", false, 1)
    NS.SetByPath("container.layout.spacing", 9, 2)
    m.__subcategories.Containers.defaultsOnClick()
    -- red under: a click closure that captured the section at build time (General's rows reset)
    assertEqual(NS.Database.FindContainer(1).layout.spacing, T0.layout.spacing, "a Layout row")
    assertEqual(NS.Database.FindContainer(1).bars.width, 300, "a Bars row is not a Layout row")
    assertEqual(NS.Database.FindContainer(1).enabled, false, "a General row is not a Layout row")
    assertEqual(NS.Database.FindContainer(2).layout.spacing, 9, "only the selected container")
    P.rail("containers")
    m.__subcategories.Containers.defaultsOnClick()
    assertEqual(NS.Database.FindContainer(1).enabled, T0.enabled, "on General, General's rows")
end)

test("rail: the Defaults tooltip names the section on screen and the kept name", function()
    local NS, m = env()
    assertEqual(m.__subcategories.Containers.defaultsTooltip,
        NS.L["Restore the selected container's settings in the section on screen to their addon defaults. On General: Enabled, Unit, Aura type and Style; its name is kept."])
end)
```

  Rewrite the three existing expectations that the old behavior pinned:
  - `tests/test_options_descriptor.lua` :446-450: replace the comment and
    `assertEqual(table.concat(opened, ","), "cat:" .. NS2.SubPageLabel("Layout"))` with

```lua
    -- red under: a section key looked up in the category table alone (#6: Layout is a section of
    -- Containers, and the key opens Containers on it)
    assertEqual(table.concat(opened, ","), "cat:" .. NS2.L["Containers"])
    assertEqual(NS2.Helpers.__pageCtx.containers.activeSection, "layout")
```

    and rename the case to `"options descriptor: OpenOptionsPage opens a registered page's category, a section's through Containers, and falls back to the panel otherwise"`.
  - `tests/test_pages_containers.lua` :120-125: replace the comment and
    `assertEqual(opened[1], NS.SubPageLabel("Layout"))` with

```lua
    -- Layout is a section of Containers (#6): the key opens Containers on that section.
    assertEqual(opened[1], NS.L["Containers"])
    assertEqual(NS.Helpers.__pageCtx.containers.activeSection, "layout")
```

  - `tests/test_pages_containers.lua` :558-562 (the `assertEqual` at :561): the expected tooltip becomes
    `NS.L["Restore the selected container's settings in the section on screen to their addon defaults. On General: Enabled, Unit, Aura type and Style; its name is kept."]`,
    and the case's name becomes `"containers: the page's Defaults tooltip names the section on screen and the kept name"`.

- [ ] **Step 2: Run and see them fail.**

```sh
$B lua tests/run.lua > /tmp/am-run.txt 2>&1; grep -E '^  FAIL' /tmp/am-run.txt
```

Expected: the six new `rail:` cases above and the three rewritten expectations `FAIL`: no
`SelectSection`, `OpenOptionsPage("layout")` lands on the Layout sub-page, the old tooltip. Nothing else
fails.

- [ ] **Step 3: Implement.** In `settings/OptionsSetup.lua`:
  - Above `local function railSections`, add `local containersCtx`, and make the bind record it: the
    first line of `Helpers.__bindContainersPage` becomes `containersCtx = ctx`.
  - Directly after `Helpers.RenderContainerPage`, add:

```lua
--- Select section `key` on the Containers page, and optionally its tab: the one seam a link, a deep
--- link or a suite moves the section through. A hidden page is marked owed a render and draws the
--- section on its next show. Refused in combat, as a tab switch is (options-ui-§2). A style section
--- the selected container is not drawn in is not on the rail, and selecting it moves nothing.
--- @return boolean  whether the section was selected
function Helpers.SelectSection(key, tabKey)
    if Helpers.__combatRefused() then return false end
    local ctx = containersCtx
    if not ctx then return false end
    local listed = false
    for _, s in ipairs(railSections(NS.ActiveContainer())) do
        if s.key == key then listed = true end
    end
    if not listed then return false end
    stashTab(ctx)
    ctx.activeSection = key
    if tabKey ~= nil then ctx.sectionTabs[key] = tabKey end
    Helpers.RefreshPanel(ctx, true)
    return true
end

-- The library's SelectTab moves one PAGE's tab. A section key is no page any more (#6): it routes to
-- SelectSection, so a link written against the old page keys still lands. Any other key -- General,
-- the addon page, settings/Filters.lua's "See spells" -- is the library's.
local selectTab = Helpers.SelectTab
function Helpers.SelectTab(pageKey, tabKey)
    if sections[pageKey] then return Helpers.SelectSection(pageKey, tabKey) end
    return selectTab(pageKey, tabKey)
end
```

  - In `NS.OpenOptionsPage`, after the combat refusal and before `local cat = categories[pageKey]`:

```lua
    -- A former sub-page key is a section of Containers now (#6): select it, then open Containers.
    -- "containers" itself keeps the section the player left (an anchor's right-click means "this
    -- container", not "General"), and a style key the container is not drawn in selects nothing.
    if sections[pageKey] then
        if pageKey ~= GENERAL_SECTION then Helpers.SelectSection(pageKey) end
        pageKey = GENERAL_SECTION
    end
```

  - The stub's no-op list: after `"SelectTab", "NavRail",` add `"SelectSection",`.

  In `settings/Containers.lua` `build`, change the `defaultsTooltip` to
  `L["Restore the selected container's settings in the section on screen to their addon defaults. On General: Enabled, Unit, Aura type and Style; its name is kept."]`
  and the click to:

```lua
    -- The ACTIVE section's rows, read at click time: the button is built once, on the first show
    -- (O.EnsureDefaultsButton), so a section captured here would be General's for good (#6, spec §3).
    ctx.panel.defaultsOnClick = function() H.RestoreDefaults(ctx.activeSection or PAGE, ctx) end
```

  `locales/enUS.lua`: add the new tooltip key, and delete the old one at :154.

- [ ] **Step 4: Run and see them pass.** The same grep prints nothing.

- [ ] **Step 5: Gate**, with the citation fixes it names. Regenerate `docs/test-cases.md`.

- [ ] **Step 6: Commit.**

```sh
git add settings/OptionsSetup.lua settings/Containers.lua locales/enUS.lua tests/test_pages_rail.lua \
  tests/test_options_descriptor.lua tests/test_pages_containers.lua docs/test-cases.md
git commit -m "SR-AM-04: deep links open Containers on a section; Defaults restores the active section" \
  -m "NS.OpenOptionsPage keeps its signature: a section key selects that section on Containers and opens it (the frame picker's reopen of \"layout\" lands on Layout), \"containers\" keeps the section the player left, and a style key the container is not drawn in selects nothing. Helpers.SelectSection(key, tabKey) is the one seam, refused in combat; Helpers.SelectTab routes section keys to it and leaves page keys to the library. Containers' Defaults restores the active section's rows for the selected container, read at click time (spec §3); one section-neutral tooltip." \
  -m "<attribution trailers>"
```

### Task SR-AM-05: retire the sub-pages

The five page files register sections only. The disabled-for-this-style notice, the D6 mark and the
sub-page registration go. The tests move onto the Containers ctx plus a section.

**Files:**
- Modify: `settings/OptionsSetup.lua`:
  - Delete :54-97 (the `-- The nesting mark` block through `NS.SubPageLabel`'s `end`).
  - Delete `mutedNotice` and its comment (:429-446).
  - `pageOpts` (:476-483) keeps only `tabs`, `cfg` and `intro`.
  - `RenderPage`'s doc comment (:491-504) loses the `disabledFor` lines.
  - Delete the stub's `NS.RegisterContainerPage` line (:292).
  - Delete the live `NS.RegisterContainerPage` and its doc comment (:524-554). Keep
    `Helpers.__pageCtx = {}`.
  - `Helpers.__bindContainersPage` aliases every section key to the page's ctx.
  - Header comment :3-13: "the CONTAINER BANNER every per-container page shares" -> "the Containers
    page — its band, its nav rail and its sections (#6)".
- Modify: `settings/Filters.lua` :748, `settings/Layout.lua` :631, `settings/Bars.lua` :206-214,
  `settings/Icons.lua` :120-132, `settings/Text.lua` :503-513: `NS.RegisterContainerPage(PAGE, L[…], "AuraMaster…Panel", {…})`
  becomes `NS.RegisterContainerSection(PAGE, L[…], {…})`. Bars, Icons and Text lose `disabledFor` and
  `disabledNotice`, and Icons loses its B-2 comment (:120-123).
- Modify: `settings/Containers.lua`. The header comment :3-28 is replaced whole (text in Step 3).
  The `container.style` row's `desc` (:88) and `BAND.tooltip` (:251) get new wording.
- Modify: `core/Constants.lua` :162-166 (delete `C.NOTICE_COLOR` and its comment; nothing reads it).
- Modify: `locales/enUS.lua`:
  - Delete the six `Not in use: …` keys (:156, :332, :643, :644, :683, :684).
  - Delete `Restore every setting on this page, for the selected container, to its default.` (:398),
    `Which container this page, and the Filters, Layout, Bars, Icons and Text pages, edit. The choice
    is shared by every page.` (:646), and `Draw each aura as a bar, an icon or a line of text. Bars,
    Icons and Text each have their own settings page.`
  - Add the two replacements.
- Modify: `AuraMaster.toc` :127-133 (the two notes). Modify `tests/test_loadorder.lua` :56-64.
- Modify: `tests/page_helpers.lua` :44-58 (`P.show`).
- Modify tests per the migration rules R1-R7 below: `tests/test_optionssetup.lua`,
  `tests/test_options_descriptor.lua`, `tests/test_pages_tabs.lua`, `tests/test_pages_bars.lua`,
  `tests/test_pages_icons.lua`, `tests/test_pages_text.lua`, `tests/test_pages_filters.lua` (R7).
- Modify only if R6 names them (spec §6 moves them onto the Containers ctx too; the alias makes their
  `__pageCtx.<section>` reads the Containers ctx with no edit, so none is expected):
  `tests/test_pages_layout.lua` (13 `__pageCtx.layout` uses, e.g. :199, :379, :482),
  `tests/test_pages_containers.lua` (:338), `tests/test_anchors.lua` (:1409-1418). They are in the
  commit's `git add` either way, so an R6 fix to one of them is never left unstaged.
- Modify (generated): `docs/test-cases.md`.

**Interfaces:**
- Removes: `NS.RegisterContainerPage` and `NS.SubPageLabel`. Also removes the Filters, Layout, Bars,
  Icons and Text Blizzard subcategories and the per-page ctxs (`AuraMaster<Page>Panel`), and
  `C.NOTICE_COLOR`.
- Produces: `Helpers.__pageCtx[sectionKey] == Helpers.__pageCtx.containers` for every section. In the
  test helpers, `P.show("<Section>")` selects the section and shows Containers. It errors when the
  selected container's rail does not list it.

- [ ] **Step 1: Write the failing tests first.** In `tests/test_optionssetup.lua`, replace the
  `PAGES` table and its comment (:13-24) and the case at :31-36 with:

```lua
-- The Settings tree (#6): General, Containers, Profiles. Filters, Layout, Bars, Icons and Text are
-- sections of Containers, reached through its nav rail, and have no tree entry of their own.
local PAGES = {
    { key = "general",    label = "General" },
    { key = "containers", label = "Containers" },
}
-- The Containers page's sections the rail lists for container 1, drawn as bars.
local SECTIONS = { "filters", "layout", "bars" }

test("options: General and Containers register, in TOC order; the former sub-pages do not, and Profiles opts out without AceDBOptions", function()
    for _, p in ipairs(PAGES) do
        assertTrue(mocks.__subcategories[p.label] ~= nil, "page " .. p.label)
    end
    for _, gone in ipairs({ "Filters", "Layout", "Bars", "Icons", "Text" }) do
        -- red under: a page file still registering a Blizzard subcategory (smoke 1)
        assertNil(mocks.__subcategories[gone], gone .. " has no tree entry")
        assertNil(mocks.__subcategories["  - " .. gone], gone .. " has no D6-marked tree entry")
    end
    assertNil(NS.SubPageLabel, "the D6 nesting mark has no caller left")
    assertNil(mocks.__subcategories.Profiles, "the harness has no AceDBOptions; the page returns nil")
end)
```

  and in "every page renders without a reported error" (:62-78), after the `PAGES` loop, add:

```lua
    NS2.State.SetActiveContainer(1)
    for _, key in ipairs(SECTIONS) do
        local before = #aceGUI.__created
        assertTrue(NS2.Helpers.SelectSection(key), key .. " is on the rail")
        NS2.Helpers.__pageCtx.containers.panel:__fire("OnShow")
        assertTrue(#aceGUI.__created > before, key .. " drew widgets")
    end
```

- [ ] **Step 2: Run and see them fail.** `grep -E '^  FAIL' /tmp/am-run.txt` shows
  "options: General and Containers register …" failing (the five subcategories exist, and so does
  `NS.SubPageLabel`).

- [ ] **Step 3: Retire the sub-pages** (the **Files** list above). The code that is not a deletion:

  `settings/OptionsSetup.lua`, `pageOpts`:

```lua
--- The library's `opts` for one render of a page with a container (or an addon-wide page).
local function pageOpts(spec, cfg)
    local intro = spec.intro
    local opts = { tabs = hostTabs(spec, cfg), cfg = cfg }
    if intro and cfg then opts.chrome = function(c) intro(c, cfg) end end
    return opts
end
```

  `Helpers.__bindContainersPage`:

```lua
--- Bind the Containers page's ctx (settings/Containers.lua's builder). The page opens on General.
--- Every section key names the same ctx in the test seam: a section is the page, drawn on it.
function Helpers.__bindContainersPage(ctx)
    containersCtx = ctx
    ctx.sectionTabs = {}
    ctx.activeSection = GENERAL_SECTION
    for key in pairs(sections) do Helpers.__pageCtx[key] = ctx end
    Helpers.__pageCtx[GENERAL_SECTION] = ctx
end
```

  The five registrations. Each replaces the WHOLE `NS.RegisterContainerPage(…)` call, from its first
  line through its closing `})` (SR-AM-02 left `style` and `tooltip` in each spec; they stay).

  `settings/Filters.lua` (:748) and `settings/Layout.lua` (:631): only the call's first line changes,
  and the spec's body (`intro`, `pairWith`, `afterGroup`, `tooltip`, …) is kept exactly:
  - `NS.RegisterContainerPage(PAGE, L["Filters"], "AuraMasterFiltersPanel", {` ->
    `NS.RegisterContainerSection(PAGE, L["Filters"], {`
  - `NS.RegisterContainerPage(PAGE, L["Layout"], "AuraMasterLayoutPanel", {` ->
    `NS.RegisterContainerSection(PAGE, L["Layout"], {`

  `settings/Bars.lua` (:206-214, the whole call):

```lua
NS.RegisterContainerSection(PAGE, L["Bars"], {
    style   = "bars",
    tooltip = L["How this container's bars look."],
})
```

  `settings/Icons.lua`: delete the B-2 comment block directly above the call (the four lines from
  `-- A container drawn as bars sees every row here disabled, under a note naming where its style is`
  through `-- about it, and names the page the style lives on rather than parenthesizing it.`,
  :120-123 at `3fdc667`), and replace the whole call (:124-132 at `3fdc667`; SR-AM-02's `style`/`tooltip`
  line shifts it, so anchor on the text) with:

```lua
NS.RegisterContainerSection(PAGE, L["Icons"], {
    style   = "icons",
    tooltip = L["How this container's icons look."],
})
```

  `settings/Text.lua` (:503-513, the whole call). `tabs` and `afterGroup` are kept exactly as they are
  (the General tab's own renderer, and the Icon and Pandemic notes):

```lua
NS.RegisterContainerSection(PAGE, L["Text"], {
    tabs       = { { key = G_GENERAL, label = G_GENERAL, render = renderGeneral } },
    afterGroup = { [G_ICON] = iconNote, [G_PANDEMIC] = pandemicNote },
    style      = "text",
    tooltip    = L["How this container's lines of text look."],
})
```

  `settings/Containers.lua`:
  - The Style row's `desc` -> `L["Draw each aura as a bar, an icon or a line of text. Bars, Icons and Text each have their own section on this page."]`
  - `BAND.tooltip` -> `L["Which container every section of this page edits."]`
  - The header comment, :3-26 (from `-- settings/Containers.lua — the Containers page:` through
    `-- band before back to AceGUI once the new band exists, never during a render.`), and :28
    (`-- This file registers its own rows and its own page, at the bottom, like every other page file.`),
    become exactly:

```lua
-- settings/Containers.lua — the Containers page: which containers exist, and what each is.
--
--     band      [Container v picker ][ New container ]         <- above the rail AND the strip (options-ui-§14)
--     rail      | General |  [ General ]                        <- the rail's first entry, and its one tab
--               | Filters |  [Name] [Enabled]
--               | Layout  |  -- What it shows, and how --       <- subsection (options-ui-§7)
--               | <style> |  [Unit] [Aura type] / [Style]
--                            [Duplicate] [Delete]               <- acts on the selected container
--                            -- Copy settings from --  [Source v] [What v] [Copy]
--
-- A TOP-LEVEL PAGE (N-1, batch 7), and since #6 the one page per container: the band on top, a
-- nav rail (General, Filters, Layout and the container's own style) and the selected section's
-- tabs. This file's rows are the General section; settings/OptionsSetup.lua draws the page.
--
-- THE PICKER AND NEW CONTAINER SIT IN THE BAND ABOVE THE RAIL AND THE STRIP (feedback #2,
-- 2026-09-19; #6), in the library's page banner with its create action (O.PageBanner's `action`,
-- through Helpers.ContainerBanner in settings/OptionsSetup.lua): the identity controls
-- options-ui-§14 puts there, on one row, and the page's ONLY picker. The rail beside it chooses
-- which part of the container is shown, never which container. The acts on the selected container
-- — Name, Enabled, Duplicate, Delete, Copy settings from — are the rail's General section, whose one
-- tab options-ui-§14 names General. This retired the page's options-ui-§14 deviation
-- (docs/ARCHITECTURE.md). The band is drawn anew on every render, so a Delete's two refreshes cannot
-- lose it; the library gives the widgets of the band before back to AceGUI once the new band
-- exists, never during a render.
--
-- This file registers its own rows and the page's General section, and builds the page (`build`, at
-- the bottom); Helpers.RenderContainerPage in settings/OptionsSetup.lua draws it.
```

  `AuraMaster.toc` (CRLF), the two notes above `settings\Containers.lua` and above `settings\Filters.lua`:

```text
# LOAD-BEARING: Containers is a top-level page (N-1); its tree position, right after General
# and before Profiles, is fixed by this load position.
settings\Containers.lua
# Conventional: the Containers page's sections (#6) -- Filters, Layout, Bars, Icons and Text --
# each registering its rows and its section at load. The rail's order is settings/OptionsSetup.lua's
# SECTION_ORDER, not this one.
```

  `tests/test_loadorder.lua` :56-64 (the comment and the seven pairs) become:

```lua
        -- The Settings tree order is the TOC's own registration order: General, then Containers
        -- (N-1), then Profiles. The Containers page's sections (#6) load after the registry in
        -- settings/OptionsSetup.lua, in any order: the rail's is SECTION_ORDER.
        { "settings/General.lua", "settings/Containers.lua" },
        { "settings/Containers.lua", "settings/Profiles.lua" },
        { "settings/OptionsSetup.lua", "settings/Filters.lua" },
        { "settings/OptionsSetup.lua", "settings/Text.lua" },
```

  `tests/page_helpers.lua`, replacing `P.show` and its comment (:44-58):

```lua
    -- The Containers page's sections by their old page names (#6): `P.show("Filters")` selects the
    -- section and shows Containers, so a suite written against the sub-pages reads the same.
    local SECTIONS = { Filters = "filters", Layout = "layout", Bars = "bars", Icons = "icons", Text = "text" }

    --- Fire a page's OnShow and answer the widgets that render drew. `page` is the page's plain display
    --- name, or a Containers section's (above), which is selected first. A section the selected
    --- container's rail does not list is an error, never a silent draw of another section.
    function P.show(page)
        local mark = #ace.__created
        local key = SECTIONS[page]
        if key then
            if not NS.Helpers.SelectSection(key) then
                error("section " .. key .. " is not on the rail for the selected container", 2)
            end
            page = "Containers"
        end
        m.__subcategories[page]:__fire("OnShow")
        return since(mark)
    end
```

  Locale additions:
  `L["Draw each aura as a bar, an icon or a line of text. Bars, Icons and Text each have their own section on this page."]`
  and `L["Which container every section of this page edits."]`.

- [ ] **Step 4: Migrate the tests.** These are mechanical rules, each with its complete site list.
  Nothing outside the lists changes.

  **R1, showing a section directly.** Replace each
  `NS2.Helpers.__pageCtx.<sec>.panel:__fire("OnShow")` with the two statements
  `assertTrue(NS2.Helpers.SelectSection("<sec>"), "<sec> is on the rail"); NS2.Helpers.__pageCtx.containers.panel:__fire("OnShow")`.
  Sites: `test_options_descriptor.lua` :77, :250, :296, :376, :396; `test_optionssetup.lua` :106, :113,
  :126, :146, :165, :191, :342. One exception: at `test_options_descriptor.lua` :194 the case has
  selected container 2 (icons), so its section is `"icons"`.

  **R2, a tab set before the show.** `test_options_descriptor.lua` :58-59: replace both lines with
  `assertTrue(NS2.Helpers.SelectSection("bars", NS2.L["Icon"])); NS2.Helpers.__pageCtx.containers.panel:__fire("OnShow")`.

  **R3, loops over pages.** In `test_options_descriptor.lua` :230-245 ("every page's Container picker
  sorts …"), the loop header and its first two lines become:

```lua
    for _, page in ipairs({ "containers", "filters", "layout", "bars" }) do
        assertTrue(NS2.Helpers.SelectSection(page), page .. " is on the rail")
        local ctx = NS2.Helpers.__pageCtx[page]
        ctx.panel:__fire("OnShow")
```

  In `test_pages_tabs.lua`, replace the case "tabs: each of the seven pages draws its tab keys and
  labels in order" (:57-69) with:

```lua
-- The style each starter container is drawn in: the rail lists only that style's section (#6).
local STYLE_OF = { [1] = "bars", [2] = "icons" }
local STYLE_PAGE = { Bars = "bars", Icons = "icons", Text = "text" }

test("tabs: every page and section draws its tab keys and labels in order", function()
    local NS, _, P = env()
    for _, id in ipairs({ 1, 2 }) do
        NS.Helpers.SelectContainer(id)
        for _, page in ipairs(STRIPS) do
            local style = STYLE_PAGE[page[1]]
            if style == nil or style == STYLE_OF[id] then
                -- "Containers" is the General section. The page keeps the last section shown, so
                -- without this the id=2 pass would draw Bars (healed to Icons), not General.
                if page[2] == "containers" then
                    assertTrue(NS.Helpers.SelectSection("containers"), "General is on the rail")
                end
                P.rerender(page[1])
                -- red under: a group tab dropped or reordered, a host tab not taking its group's place,
                -- or Overrides not placed ahead of Sorting
                assertEqual(strip(P, NS.Helpers.__pageCtx[page[2]]), page[3], page[2] .. " on container " .. id)
            end
        end
    end
    NS.SetByPath("container.style", "text", 1)
    NS.Helpers.SelectContainer(1)
    P.rerender("Text")
    assertEqual(strip(P, NS.Helpers.__pageCtx.text), STRIPS[7][3], "text on a text container")
end)
```

  and replace "tabs: with no containers every per-container page draws one placeholder tab and the
  empty-registry line" (:130-148) with:

```lua
test("tabs: with no containers General keeps its tabs and Containers offers its General section alone", function()
    local NS, _, P = env()
    for _, c in ipairs(NS.Database.GetContainers()) do NS.ContainerManager.Delete(c.id) end
    P.rerender("General")
    -- red under: an addon-wide page losing its tabs with the registry
    assertEqual(strip(P, NS.Helpers.__pageCtx.general), STRIPS[1][3], "General keeps its tabs")
    local ws = P.rerender("Containers")
    assertEqual(strip(P, NS.Helpers.__pageCtx.containers), STRIPS[2][3], "Containers keeps its one tab")
    assertTrue(P.hasText(ws, NS.L["No containers yet. Click New container, or type /am new."]), "and says how to make one")
    -- red under: a section that needs a container reachable with none (an empty page under a strip)
    assertFalse(NS.Helpers.SelectSection("filters"))
end)
```

  In `test_optionssetup.lua`, delete "options: with no containers a container page draws one
  placeholder tab" (:150-160). SR-AM-03's "rail: with no containers …" case covers it.

  **R4, deleted cases.** These pin the retired disabled notice or a sub-page that no longer exists:
  - `test_optionssetup.lua` :438-452 ("a page drawn for another style heads its tabs with the notice in muted red").
  - `test_options_descriptor.lua` :312-331 ("a page disabled for its container hands the disable to a bespoke tab …").
  - `test_pages_tabs.lua` :88-113 (the `NOTICES` table and "Bars, Icons and Text on a mismatched style draw the muted-red notice …").
  - `test_pages_bars.lua` :17-87 (the batch-8 comment, `MSG`, `NOTICE`, and the three cases at :27, :42 and :62, the last ending at :87).
  - `test_pages_icons.lua` :17-83: the same three cases, :28, :39 and :59 (ending at :83), with their comment and locals.
  - `test_pages_text.lua` :14 (`NOTICE`), :78-97, :99-105 and :204-233 (the owner comment and "the
    Text Template block grays with the page on a bars container"). A15 records that the gray path is
    now unreachable.
  Update each touched file's header comment so it no longer mentions the notice (for example,
  `test_pages_bars.lua` :1-3 "the notice on a container that is not drawn as bars" goes).

  **R5, the `D6` label in an expectation.** `test_optionssetup.lua`'s header comment (:13-15) goes
  with the `PAGES` rewrite in Step 1. No other site: SR-AM-04 already rewrote the two
  `SubPageLabel("Layout")` expectations.

  **R7, a style section shown on a container of another style.** `P.show("<Style>")` now raises
  when the selected container's rail does not list that section (Step 3's `P.show`), where the old
  sub-page drew its notice. These are the cases outside R4 that do it, found by reading every
  `P.show`/`P.rerender`/`P.eachTab` of Bars, Icons and Text against the container selected at that
  point (starter styles: 1 bars, 2 icons, 3 icons, 4 text; `defaults/Profile.lua:285-303`). Line
  numbers are at `3fdc667`, before R4's deletions shift them; anchor on the text:
  - `test_pages_bars.lua` :160-171, "bars: Width writes the selected container, and the page re-reads
    after the banner moves": it moves the band to container 2 (icons) and shows Bars. Keep the case's
    point (the Bars section re-reads after the band moves) on a container drawn as bars: replace
    :168-170 (`P.banner(…):__fire("OnValueChanged", 2)`, `ws = P.show("Bars")` and the
    `"container 2's width"` assertion) with

```lua
    -- #6: container 2 is drawn as icons, so its rail offers no Bars. Move the band to a bars container.
    NS.SetByPath("container.style", "bars", 3)
    P.banner(NS.Helpers.__pageCtx.bars):__fire("OnValueChanged", 3)
    ws = P.show("Bars")
    assertEqual(P.row(ws, "container.bars.width").value, NS.CONTAINER_TEMPLATE.bars.width, "container 3's width")
```

    (:167's `FindContainer(2).bars.width` assertion stays: it pins that the write did not reach
    another container.)
  - `test_pages_filters.lua` :554-557, in "filters: the four tabs read General, Categories, Overrides,
    Sorting (batch 8)" (:544): it shows Text on container 1 (bars). Replace
    `    P.show("Text")` with `    NS.Helpers.SelectContainer(4)                   -- the starter drawn as text`
    + newline + `    P.show("Text")`, and `    P.show("Bars")` with
    `    NS.Helpers.SelectContainer(1)                   -- back to the bars starter` + newline +
    `    P.show("Bars")`.
  - Not a failure, but it would stop testing what its name says: `test_pages_tabs.lua` "tabs:
    re-rendering Filters and Containers ten times each …" (:192) re-renders Containers after Filters,
    so the shared ctx keeps drawing Filters. In its loop, directly before the first
    `P.rerender(page)`, add
    `        if page == "Containers" then assertTrue(NS.Helpers.SelectSection("containers")) end`, and
    change the case's `local _, m, P = env()` to `local NS, m, P = env()`.

  **R6, the leftovers.** Run the suite. For every `FAIL` left, apply R1 or R2 if the case shows a
  section's panel, R3 if it loops over the old pages, or R7 if it shows a style section on a container
  of another style (select a container of that style first, or set the container's style). A `FAIL`
  that none of R1-R3 and R7 describes is a behavior change this plan did not foresee. Stop, and record it in the task's review note with the
  failing case's name and error. **Never delete a case outside R4's list** to get green.

- [ ] **Step 5: Run and see green.**

```sh
$B lua tests/run.lua > /tmp/am-run.txt 2>&1; grep -c '^  FAIL' /tmp/am-run.txt    # expect 0
grep -rn "RegisterContainerPage\|SubPageLabel\|NOTICE_COLOR\|disabledNotice" settings core modules tests locales AuraMaster.toc   # expect no output
```

- [ ] **Step 6: Gate**, with the citation fixes it names. Regenerate `docs/test-cases.md`. Check that
  `wc -l settings/OptionsSetup.lua` is below 1500.

- [ ] **Step 7: Commit.**

```sh
git add settings/OptionsSetup.lua settings/Containers.lua settings/Filters.lua settings/Layout.lua settings/Bars.lua \
  settings/Icons.lua settings/Text.lua core/Constants.lua locales/enUS.lua AuraMaster.toc tests/page_helpers.lua \
  tests/test_loadorder.lua tests/test_optionssetup.lua tests/test_options_descriptor.lua tests/test_pages_tabs.lua \
  tests/test_pages_bars.lua tests/test_pages_icons.lua tests/test_pages_text.lua tests/test_pages_filters.lua \
  tests/test_pages_layout.lua tests/test_pages_containers.lua tests/test_anchors.lua docs/test-cases.md
git diff --name-only; git ls-files --others --exclude-standard   # expect no output: an unstaged or untracked file is an R6 edit this add missed
git commit -m "SR-AM-05: retire the Filters, Layout, Bars, Icons and Text sub-pages; they are Containers sections" \
  -m "The tree is General · Containers · Profiles (#6, smoke 1). Each page file registers its section only; Bars, Icons and Text lose disabledFor/disabledNotice, since the rail never offers a style section for another style, and the Diagnostics gates stay as data (SR-AM-02). NS.RegisterContainerPage, the D6 mark NS.SubPageLabel, mutedNotice and C.NOTICE_COLOR go, with their seven locale strings. TOC notes and load-order pairs: the rail's order is SECTION_ORDER. Tests move onto the Containers ctx plus a section (Helpers.__pageCtx aliases every section key; P.show selects the section)." \
  -m "<attribution trailers>"
```

### Task SR-AM-06: documentation and the in-client checks

**Files:**
- Modify: `docs/settings-panel.md` :16-21 (the pages table), :24-27 (the D6 paragraph), :39-52 ("Four
  pages edit one container"), :70-80 (the band section), and the section headings :393 (Filters), :519
  (Layout), :641 (Bars), :691 (Icons) and :719 (Text), and the three wrong-style notice paragraphs
  :643-649 (Bars), :699-701 (Icons) and :781-784 (Text). Leave :637's D6 alone: it is a different D6,
  Anchors.PlaceLabel from batch 8.
- Modify: `docs/ARCHITECTURE.md` :56-58 (the tree order sentence). The census row for
  `settings/OptionsSetup.lua` is re-measured if the census lists it. Leave :81's D6.
- Modify: `docs/module-map.md` :30-33 (the settings load order), :103 (the OptionsSetup row), the page
  rows :109-113, and the test rows :128, :187, :194-197, plus a `test_pages_rail.lua` row if SR-AM-02
  did not add one.
- Modify: `docs/common-tasks.md` :269-276 ("Add a settings page" becomes "Add a section to the
  Containers page").
- Modify: `README.md` :58-62 (the Containers paragraph) and the test badge at :7 (the new passed count
  from the gate). Run the `humanize` skill over the changed README prose. The README's
  `## Screenshots` section (:29-31) says "No screenshots yet" (issue #3): spec §6's "screenshots
  section if any" is checked in Step 1 and needs no edit while that holds.
- Modify: `docs/smoke-tests.md` :76-78 (the tree line), :968-969 (the band), and the four older checks
  that describe the retired notice (#26 at :132-137, #114 at :703-704, #139 at :843-845, #165 from
  :1012), which are annotated as retired, never deleted or marked. Add a new section,
  "Settings redesign (#6)", with the in-client checks S1-S16 from this bundle's `06_SMOKE_TESTS.md`,
  each with an empty Result.
- Modify (generated): `docs/test-cases.md`, only if it is stale.

**Interfaces:** none. Documentation only.

- [ ] **Step 1: Find every stale sentence, and check the screenshots.**

```sh
cd $GIT/AuraMaster
grep -rn "sub-page\|SubPageLabel\|D6\|Four pages edit one container\|RegisterContainerPage\|Not in use\|muted-red\|disabledNotice\|seven pages" \
  README.md docs/*.md | grep -v "docs/superpowers/\|docs/automated-tests/\|docs/revendor/\|docs/reviews/\|docs/audits/"
sed -n '/^## Screenshots/,/^## /p' README.md          # expect "No screenshots yet" and the issue #3 link
grep -n '!\[' README.md | grep -vi 'img.shields.io'    # expect no output: no screenshot image in the README
```

Expected: the sites under **Files**. Past bundles are frozen and are never edited. If the README has
gained a screenshot of the settings panel since planning (the last two commands print one), it shows
the retired tree: replace its caption with "Screenshot from before the settings redesign (#6)" and
add a line under the section, "The settings panel now has one Containers page with a rail; new
screenshots are tracked in issue #3." Do not take or invent a screenshot.

- [ ] **Step 2: Make these edits.** Anchor on the quoted text; the line numbers are at `3fdc667`.

  `docs/settings-panel.md`:
  - :16-21, the table rows from `| Containers | General |` through the `| - Text (sub-page …` row,
    become:

```markdown
| Containers | a nav rail (options-ui-§13): General · Filters · Layout · the container's own style | One page per container (#6): the band's picker chooses the container, the rail chooses which part of it the tabs below show, and only the scroll moves |
| Containers → General (rail) | General | A top-level page (`N-1`, batch 7): create, select, rename, enable, unit, aura type and style of a container, and duplicate, delete, copy settings between containers |
| Containers → Filters (rail) | General · Categories · Overrides · Sorting | Who cast it, timed or permanent, max duration, and the five-rank priority block at the foot of the tab; the Show/Hide category grids (weapon enchants among them); the whitelist and blacklist spell lists, each entry's verdict in its "?" mark; sort order and cap (per group). Tabs vary with the aura type |
| Containers → Layout (rail) | Frame · Anchor · Growth · Mouse · Label | Scale, opacity, strata and frame level; where the container sits (the screen, another container or a named frame, with only what the mode reads drawn) and the frame picker; growth direction and spacing, the flow inherited from the parent while attached to a container; tooltips, cancel, click-through; the optional name label |
| Containers → Bars (rail, a container drawn as bars) | General · Background & border · Name text · Time text · Stack text · Icon · Pandemic | The look of a container drawn as bars |
| Containers → Icons (rail, a container drawn as icons) | Size · Border · Cooldown · Time text · Stack text · Pandemic | The look of a container drawn as icons |
| Containers → Text (rail, a container drawn as text) | General · Font · Icon · Pandemic · Animation | The look of a container drawn as text: what each line says, its font and its optional icon, its pandemic-window color and blink, its loop, and its opt-in dispel type colors |
```

  - :24-27, the paragraph that opens ``The `- ` prefix is the Settings tree's own nesting mark (`D6`)``,
    becomes:

```markdown
Filters, Layout, Bars, Icons and Text are **sections of the Containers page** (#6), not pages: they
have no Settings tree entry of their own, and the tree reads General · Containers · Profiles. A
section key is the former page key (`filters`, `layout`, `bars`, `icons`, `text`, and `containers` for
General), so every row's `page`, every `/am set`, `/am get` and `/am list` path and every default is
unchanged. The rail lists General, Filters, Layout and the one style section the selected container
is drawn in, in `SECTION_ORDER`'s order (`settings/OptionsSetup.lua`).
```

  - :39-52, the bullet that opens `- **Four pages edit one container.**` (through `… and Containers'
    one tab edits the selected container's identity.`), becomes:

```markdown
- **One page edits one container, through a nav rail** (#6, options-ui-§13). The Containers page
  draws, in the library's order, the band (`Helpers.ContainerBanner`, the page's only picker), the
  rail (`O.NavRail`, 120px, in AceGUI's tree-pane look) and the selected section's tabs, over the
  page's one scroll: `Helpers.RenderContainerPage` (`settings/OptionsSetup.lua`). Each page file
  registers its rows and its section with `NS.RegisterContainerSection(key, label, spec)`, and the
  section renders through `Helpers.RenderPage` with its own key and spec, which maps the spec onto the
  library's `O.RenderTabbedSchema` (`opts`: `tabs`, `cfg`, `chrome`): the section's schema groups
  become tabs, the section's own tabs that the container's aura type admits follow (one keyed by a
  group takes that group's place and is handed its rows; one may name the tab it is drawn ahead of,
  as Filters' Overrides does), a stale active tab heals to the first, and every row resolves against
  the selected container. The host keeps no tab renderer of its own (anti-pattern #47,
  `AuraMaster-R-04`). A style section is listed only for a container drawn in that style, so no
  section is ever drawn disabled, and a Style change moves an open style section to the new style's
  (Bars becomes Icons) while every other section stays. The section (`ctx.activeSection`) and each
  section's tab (`ctx.sectionTabs`) are session state and never persisted: returning to a section
  returns to the tab you left. General, the addon page, is addon-wide, renders through
  `Helpers.RenderPage` and draws no banner.
```

  - :70: `A page that edits one of many containers says which one, in the band above its tab strip, and that`
    -> `The Containers page says which container it edits, in the band above its rail and tab strip, and that`.
  - :73-75, the bullet `- **Filters, Layout, Bars, Icons** draw `Helpers.ContainerBanner` — …  It is the`
    + `  page's only picker.`, becomes:
    `- **Every section of Containers** sits under one band, drawn by `Helpers.ContainerBanner` — a Container dropdown built through the library's `PageBanner`, labeled with each container's unit, aura type and style — above both the rail and the strip. It is the page's only picker; the rail beside it chooses which part of the container is shown, never which container (options-ui-§14).`
  - :79-80: `stay on the page's one tab, which options-ui-§14 then names **General**.` ->
    `are the rail's General section, whose one tab options-ui-§14 names **General**.`
  - The five section headings: replace `— sub-page of Containers (`N-2`, `D6`)` with
    `— a section of Containers (#6)` at :393, :519, :641, :691 and :719.
  - The three wrong-style notice paragraphs, each replaced whole by one sentence:
    - Bars, :643-649 (`When the selected container is drawn as icons, a small muted-red note heads every tab`
      through `The tabs and the container picker stay live.`):
      `This section is on the rail only for a container drawn as bars (#6). A container drawn in another style shows its own style's section instead, so nothing here is ever drawn disabled.`
    - Icons, :699-701 (`When the selected container is drawn as bars, the same small muted-red note` through
      `… and every control is drawn disabled, as on the Bars page.`):
      `This section is on the rail only for a container drawn as icons (#6); another style shows its own section instead.`
    - Text, :781-784 (`When the selected container is drawn as bars or icons, the same small muted-red note`
      through `… disabled, as on the Bars and Icons pages.`):
      `This section is on the rail only for a container drawn as text (#6); another style shows its own section instead.`

  `docs/ARCHITECTURE.md` :56-58: the sentence `The Settings tree's order is the TOC's own registration order (`N-2`): General, then Containers,`
  through `… — then Profiles.` becomes:
  `The Settings tree's order is the TOC's own registration order: General, then Containers, then Profiles. Filters, Layout, Bars, Icons and Text are sections of the Containers page (#6) with no tree entry; they load after `settings/OptionsSetup.lua` in any order, and the rail's order is `SECTION_ORDER` there.`

  `docs/module-map.md`:
  - :30-33: `The page files are in the order their Blizzard subcategories` through
    `` (each marked with `NS.SubPageLabel`'s indent, D6), then `Profiles.lua`. `` becomes:
    ``The page files are in the order their Blizzard subcategories appear (**load-bearing** for the tree order, N-1): `General.lua`, then `Containers.lua`, then `Profiles.lua`. The Containers page's sections, `Filters.lua`, `Layout.lua`, `Bars.lua`, `Icons.lua` and `Text.lua` (#6), load after `OptionsSetup.lua` in any order (**conventional**): the rail's order is `SECTION_ORDER`.``
  - :103, the `settings/OptionsSetup.lua` row: replace
    ``; `RenderPage`, which maps a page spec (its own tabs filtered by aura type, `intro`, `disabledFor` and the muted-red `disabledNotice`, `afterGroup`, `pairWith`) onto the library's `O.RenderTabbedSchema`, and `RenderContainerPage`; `NS.RegisterContainerPage`, `NS.OpenOptionsPage`, `NS.RequestPanelRefresh` |``
    with
    ``; `RenderPage`, which maps a page or section spec (its own tabs filtered by aura type, `intro`, `afterGroup`, `pairWith`) onto the library's `O.RenderTabbedSchema`; the section registry (`NS.RegisterContainerSection`, `NS.ContainerSection`, `SECTION_ORDER`) and the Containers page's renderer `RenderContainerPage` (band, `O.NavRail`, the selected section; per-section tab memory and the style heal, #6); `SelectSection` and the section-aware `SelectTab`; `NS.OpenOptionsPage` (a former sub-page key opens Containers on that section), `NS.RequestPanelRefresh` |``
  - :109-113, the five page rows: replace `The Filters page, a sub-page of Containers (`N-2`, D6):` with
    `The Filters section of the Containers page (#6):`, and the same for Layout, Bars, Icons and Text.
    In the Bars and Icons rows replace the closing `; disabled for any other style |` with
    `; on the rail only for a container drawn in this style |`, and in the Text row replace
    `; disabled for a bars or icons container |` with `; on the rail only for a container drawn as text |`.
  - :128 (`tests/page_helpers.lua`): replace `tab moves, and` with
    `tab moves, the rail (`P.drawnRail`, `P.rail`; `P.show("<Section>")` selects a Containers section first), and`.
  - :187: `The panel: pages, tabs, the container banner,` ->
    `The panel: the tree's three pages and the Containers sections, tabs, the container banner,`.
  - :194: delete `the not-drawn-as-bars notice with every control disabled, `. :195: delete
    `the not-drawn-as-icons notice with every control disabled, `. :196: delete
    `the notice and disabled rows for another style, `.
  - :197: `Every tabbed page's render from the outside, across the seven pages:` ->
    `Every tabbed page's and Containers section's render from the outside:`, and delete
    `the muted-red notice above disabled rows, `; `the empty registry's placeholder tab and line` ->
    `the empty registry's General-only rail and line`.
  - If `grep -c test_pages_rail docs/module-map.md` prints 0, add after :197:
    ``| `test_pages_rail.lua` | The Containers page's nav rail (#6): the section registry and the style gates, the rail's entries per style, the draw order, per-section tab memory, the style heal, deep links and `SelectSection`, Defaults for the active section, the degraded stub's no-ops |``

  `docs/common-tasks.md` :269-276, the whole `## Add a settings page` section, becomes:

```markdown
## Add a section to the Containers page

1. Add the section key to `VALID_PAGES` in `settings/Schema.lua`: a section key is a page key, and
   every row's `page` names it.
2. Create `settings/<Section>.lua` registering its rows and calling
   `NS.RegisterContainerSection(key, L["Title"], spec)`, with `spec.tooltip` (the rail entry's
   tooltip) and, for a section that applies to one style only, `spec.style`. An addon-wide page is
   still `NS.RegisterOptionsPage`.
3. Add the key to `SECTION_ORDER` in `settings/OptionsSetup.lua`: that, not the TOC, is the rail's
   order. Load the file after `settings/OptionsSetup.lua` in `AuraMaster.toc`.
4. Every row needs a `group` (options-ui-§13). Add the section to the table in
   `docs/settings-panel.md`.
```

  `README.md` :58-62: replace from `Its own Container` (end of :59) through `and the choice follows you from page`
  + newline + `to page.` (the start of :62) with:
  `It's one page per container: the Container dropdown at the top picks which one you're editing, and the list down the left side switches between General, Filters, Layout and the container's own style (Bars, Icons or Text), each with its own tabs. The page remembers which tab you were on in each of them until you reload.`
  Then run the `humanize` skill over the paragraph and re-wrap it at the file's width.

  `docs/smoke-tests.md`:
  - :76-78: `The tree reads **General ·` through `… Profiles flush with it (N-2).` becomes
    `The tree reads **General · Containers · Profiles**. Filters, Layout, Bars, Icons and Text are sections of Containers, on its rail, with no tree entry of their own (#6).`
  - :968-969 (anchor on the text): `The Container dropdown in the band of Containers, Filters, Layout, Bars,` + newline +
    `Icons and Text lists` -> `The Container dropdown in the Containers page's band (on every rail` +
    newline + `section) lists`.
  - The four older checks that describe the notice stay in place, words unchanged. The note
    `*(Retired by #6: a container's rail offers only its own style's section, so this notice and the dimmed style page no longer exist; see "Settings redesign (#6)" below.)*`
    goes after the part each one retires:
    - #26 (:132-137): only its notice sentence, so insert the note after `the tabs` + newline +
      `    and the Container dropdown still work.`; the rest of #26 (tab order, Size, Icon border)
      still holds.
    - #114 (:703-704): the whole check; append the note to its last line.
    - #139 (:843-845): only the sentence `On a bars or icons container, the "Not in use" notice … muted
      gold.`; insert the note right after it.
    - #165 (:1012-1016 and on, to the check's end): the whole check; append the note to its last line.
    Nothing in a check's Result is touched.
  - The new section, at the end of the file: `## Settings redesign (#6)`, then one numbered check per
    S1-S16 row of this bundle's `06_SMOKE_TESTS.md` (its "Do" and "Expect" columns as one paragraph),
    numbered on from the file's last check, each ending `Result: ` with nothing after it.

  Cite `settings/OptionsSetup.lua` symbols by file:line only **with the symbol in backticks within 3
  lines** (test_docs); the text above cites none by line.

- [ ] **Step 3: Gate** (test_docs included) and the Step 1 grep again. The hits that may remain, all
  of them another meaning of the word: every `D6` that is batch 8's label rule (`ARCHITECTURE.md:81`,
  `data-flow.md`, `known-limitations.md`, `settings-panel.md:637`, `smoke-tests.md` #204,
  `test-cases.md`'s label case, `schema.md`'s `label.show` row); "Profiles sub-page" (`ARCHITECTURE.md`,
  `module-map.md`, `profiles.md`, `scope.md`); "seven pages" in `ARCHITECTURE.md:87` and `schema.md`,
  which count the schema's page keys and still hold (a section key is a page key); `module-map.md`'s
  `test_anchors_label.lua` row; and the four retired smoke checks' own words. Anything else is a missed
  site. Update the README badge to the gate's passed count.

- [ ] **Step 4: Commit.**

```sh
git add README.md docs/settings-panel.md docs/ARCHITECTURE.md docs/module-map.md docs/common-tasks.md docs/smoke-tests.md docs/test-cases.md
git commit -m "SR-AM-06: document the one Containers page with its nav rail, and the in-client checks" \
  -m "settings-panel.md, ARCHITECTURE.md, module-map.md, common-tasks.md and README describe General · Containers · Profiles, the rail and its sections; smoke-tests.md gains the #6 checks (owner-run, unmarked)." \
  -m "<attribution trailers>"
```

### M2 checkpoint

- The AuraMaster gate on a clean tree: tests (passed, 0 failed, skipped), luacheck 0/0 in N files, and
  complexity 0 over CCN 15. `test_vendor_sync` passes (vendor == v1.61.0).
- If the owner authorized pushes: `git push -u origin feat/2026-09-26-settings-redesign` and
  `git push origin refs/notes/ka0s-review`.
- Append the M2 row to `checkpoints.tsv`.

---

## M3 — record

### Task SR-REC-01: the execution record

**Repo:** `$GIT/Ka0sAddonsCommonTasks`, `main`.

**Files:**
- Create: `docs/2026-09-26-SETTINGS_REDESIGN/99_REPORT.md`.
- Modify: `docs/2026-09-26-SETTINGS_REDESIGN/checkpoints.tsv` (the M1, M2 and M3 rows, if an earlier
  step did not already append them).
- Modify: `docs/2026-09-26-SETTINGS_REDESIGN/06_SMOKE_TESTS.md`. The Result column stays empty. Only
  the owner fills it.

**Interfaces:** none.

- [ ] **Step 1: Collect the facts from git**, never from memory:
  `./resume-state.sh -v` (all 12 items done), `git log --format='%h %s' master..feat/2026-09-26-settings-redesign`
  in the three repos, the review notes (`git notes --ref ka0s-review list`), the LibKa0s release
  manifest, and each checkpoint row.

- [ ] **Step 2: Write `99_REPORT.md`.** It covers what shipped per repo, with commit ids. It names the
  local tag (`v1.61.0`, unpushed). It reports the gate figures per milestone and every deviation from
  `03_EXECUTION_PLAN.md`, each with its reason (the plan itself is frozen and not edited). It lists the
  follow-ups. The four follow-ups are:
  1. File an AuraMaster issue for A15, Text.lua's `pageDim` dead path. Use `/wow-addon:issue-add`.
  2. MultiMeters#55 and KickCD#33 now have the library minor and the standard change they waited on.
     Each needs a LibKa0s v1.61.0 re-vendor with a `NavRail` stub first.
  3. The owner's smoke session over `06_SMOKE_TESTS.md`.
  4. `/wow-addon:finalize` on the owner's go-ahead: merge `--no-ff` in dependency order (WowAddonStandards,
     LibKa0s with its tag pushed then, AuraMaster), and delete the branches.

- [ ] **Step 3: Commit.**

```sh
cd $GIT/Ka0sAddonsCommonTasks
git add docs/2026-09-26-SETTINGS_REDESIGN/99_REPORT.md docs/2026-09-26-SETTINGS_REDESIGN/checkpoints.tsv
git commit -m "SR-REC-01: Execution record for the AuraMaster settings redesign (#6)" -m "<attribution trailers>"
```

(If the bundle itself was never committed, commit it first, as its own commit: `Settings redesign: plan bundle`.)
