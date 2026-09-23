# 03 — Spec

**The normative end state, per cluster. This describes what "done" looks like, not when it happens.**

> **Nothing in this bundle has been executed.** No repository has changed. No tag has been cut, no
> payload copied, no section amended and no issue closed. Every sentence below is in the imperative
> because it describes a *target*. Where this document says a file "carries" something, read it as
> "must carry when the cluster is closed".

Inputs: `inputs/OWNER_SCOPE.md` (binding scope and rulings), `01_CONSOLIDATED_FINDINGS.md` (436 verified
findings in 47 clusters, C01–C47), `plan-data/items.json` (the final items, including the reconcile
results and the plan-review amendments listed in its `amendment_log`) and
`plan-data/PLAN_REVIEW_RESOLUTIONS.md` (the decisions behind those amendments). Ordering,
dependencies and effort belong in `04_EXECUTION_PLAN.md` and are left out here. Item ids are the plan's:
`WS-nn` (WowAddonStandards), `LK-nn` (LibKa0s), `WA-nn` (wow-addon), `RV-<AB>` (re-vendor) and `<AB>-nn`
(addon items). `05_TRACEABILITY.md` maps every finding to them. Milestones are named only where a target
depends on them: M1 is the upstream work, M2 the re-vendors plus the pre-re-vendor fixes (AT-01, AM-01,
AM-02, BL-01, BL-02, CM-01, KC-01, WG-01), M3 the addon work, and M4 the owner-gated
`/wow-addon:revendor-standards` rolls.

Addon codes: AT AbsorbTracker, AM AuraMaster, BL BankLedger, CM ConsumableMaster, KC KickCD,
LH LootHistory, MM MultiMeters, PM PanelMaster, PF PartyFrameEnhanced, PC PrettyChat, WG WhatGroup.
These are the eleven addons in `WowAddonStandards/standards/ADDONS.md`.

---

## How to read this

Every cluster has three parts:

- **Target**: the shape that must exist when the cluster is closed.
- **Acceptance**: a check a reader can run, or a state a reader can look at, without asking the author
  what was meant. Commands run from the named repo's root.
- **Non-goals**: what this cluster deliberately does not fix, so nobody widens it in flight.

RFC-2119 words carry their usual force. Where this spec and `WowAddonStandards/standards/STANDARDS.md`
disagree, the standard wins, with one exception: the clusters whose point is to change the standard
describe the post-amendment state (v2.65.0).

**Two gates.** A **commit** is gated on `luacheck .` and `lua5.1 tests/run.lua` and nothing else. A
**tag** is gated by `/wow-addon:bump-version`: all four suites must read `pass` in the run's
`manifest.json` and `suites.complexity.warnings == 0`. A `skip` blocks as NOT EVALUATED unless it carries
a ratified skip reason. This plan cuts one tag, LibKa0s `v1.56.0`. No addon is version-bumped or tagged.

**Shorthand used in the acceptance lists.**

- `$B` is `~/.claude/wow-addon/bin/ka0s-bounded`. After WA-02 the bare name `ka0s-bounded` resolves on
  the plugin's PATH entry as well. Both forms are acceptable.
- **The standard gate (SG)** for an addon is all of the following:
  1. `$B luacheck .` reports 0 warnings / 0 errors.
  2. `$B lua5.1 tests/run.lua` reports 0 failed.
  3. `diff --strip-trailing-cr <(lua5.1 tests/run.lua --list) docs/test-cases.md` is empty, and the README
     Tests badge equals the Totals row.
  4. `$B lua5.1 tests/perf.lua` exits 0. This applies only to AT, AM, CM, KC, MM, PF and WG. BL, LH and PC
     hold the performance-§12 exemption, and PM holds its performance-§1 row, so these four have no
     `tests/perf.lua`.
  5. `lizard -l lua -x './libs/*' -x './tests/_kit/*' -C 15 -w .` prints nothing.
  6. `git ls-files '*.lua' | grep -v '^libs/\|^tests/_kit/' | xargs wc -l | awk '$2!="total" && $1>1500'`
     prints nothing. In PrettyChat, `GlobalStrings/GlobalStrings.lua` (generated) is also excluded.
- "Red first" means the case is seen failing on the pre-change tree before the fix lands, and it carries
  a `-- red under: <mutation>` comment. A case that has only ever been green is not a gate.

---

## The surfaces this spec depends on

**Baseline, 2026-09-23.** All eleven consumers vendor LibKa0s `v1.55.0` (kit revision 25), and every one
is byte-identical to it (`01_CONSOLIDATED_FINDINGS.md`, suite state). The standard is `v2.64.0` and the
plugin is `2.3.0`. The rows below are the surfaces the clusters rely on and the release that carries each.

| Surface | End state | Arrives in | Consumers that must adopt it |
|---|---|---|---|
| `LibKa0s-Core-1.0` minor 8 | `printer.Format` pcalls `string.format`, so a secret value falls back to a joined line. `lib.SafeRegisterEvent`, `SafeRegisterUnitEvent` and `SafeRegisterEvents` (IsEventValid front gate, pcall, caller-owned `rejected` list, no library state) | v1.56.0 (LK-10, LK-11) | all eleven (C03). Every Core stub gains one-rung pcall bodies |
| `LibKa0s-Item-1.0` minor 2 | `QualityFromLink` reads `\|cnIQ<n>`; the quality map is cached only when non-empty | v1.56.0 (LK-12) | BL, LH (smoke and link-shape tests) |
| `LibKa0s-Media-1.0` minor 4 | JetBrains Mono registered with a western+ruRU langmask; a count includes only fonts LSM accepted | v1.56.0 (LK-13) | none (KC's LSM fake is fixed pre-RV, KC-01) |
| `LibKa0s-Bus-1.0` minor 2 | tracking wrappers re-stamped at each edge after a newer AceEvent re-embed | v1.56.0 (LK-14) | none. PM adopts `Catalog`, which already shipped (PM-12) |
| `LibKa0s-Lifecycle-1.0` minor 2 | re-entrancy documented and pinned; code unchanged | v1.56.0 (LK-15) | none |
| `LibKa0s-Launcher-1.0` minor 2 | optional `isEnabled` / `disabledLine` gate a rung (a)/(b) left click; missing-library notices print once, without the `[LibKa0s] ` prefix | v1.56.0 (LK-16) | AT, AM, BL, CM, LH, MM, WG |
| `LibKa0s-Slash-1.0` minor 15 | `CliSet` prints the seam's `false, err, why` refusal instead of echoing; `CliReset` prints `NO_DEFAULT`; the version-15 doc prescribes the degradation stub | v1.56.0 (LK-17, LK-18) | every addon whose descriptor `set` can refuse |
| `LibKa0s-DebugLog-1.0` minor 13 | batched buffer trim; `MAX_BUFFER` stays 1500 | v1.56.0 (LK-19) | none |
| `LibKa0s-Perf-1.0` minor 13 (key 13.5) | `armed`/`recording`/`label` are raw `false`, never nil; `openDepth` resets at window edges | v1.56.0 (LK-20) | none (dry-run reds only) |
| `LibKa0s-Widgets-1.0` minor 10 (key 10.2) | `ReorderList` polls on its own ghost frame; the drop line comes from a library pool | v1.56.0 (LK-21) | CM, KC, MM (smoke only) |
| `LibKa0s-Schema-1.0` minor 2 | `instanceId` forwarded by `Get`/`ApplyDefault`; `row.normalize`; `SetMany` (all-or-nothing, one bracket line, `announceBatch` once); `writeThrough` (a declared path list stored without a row by the live instance and the degradation stub) | v1.56.0 (LK-22, LK-23) | every Schema stub (parity); adopters CM#39, KC#22, MM#52, PF#14, WG#22, AM#21 (partial) |
| Options key `24.31.4.7.4` | Options 24: font preload peeled to OptionsScroll 4; `CreateOptionsPanel` parks in combat and replays itself; `OpenOptionsPanel` answers a boolean. OptionsWidgets 31: throttles keep their own armed flag. OptionsTabs 4: no per-render widget leak; `RenderTabbedSchema` lives here and gains `opts.tabs` (a tab keyed by a schema group takes that group's place in the strip and is handed its rows), `disabledFor`/`disabledNotice` (the notice draws above the rows, which render disabled, not in place of them) and `chrome`; `PageBanner` gains `action` | v1.56.0 (LK-24..LK-28) | CM-05, WG-02 (park/replay); AM-17, CM-20 (tab opts); AT-15, KC-20, MM-18 (adopt or decline) |
| Test kit revision 26 | `asserts.lua`, `prose_lists.lua`, `Kit.assertErrorMatches`, `Kit.assertLibraryConstant`; the AceDB fake raises on a bad Copy/Delete and strips defaults on SetProfile; a recording `EventRegistry`; frame `RegisterEvent`/`RegisterUnitEvent` honor `__badEvents`; `C_EventUtils.IsEventValid`; `CreateFrame` starts shown; `test_eol` catches lone CRs; the prose gate scans store-root files, skips `docs/superpowers/` and `docs/investigations/`, and lists `synchronis`; case names carry `§`; the runner records the performance-§12 skip as reason (2) and heads empty tables; an AceGUI Create/Release survey | v1.56.0 (LK-01..LK-09, LK-27) | all eleven through RV-<AB> |
| Unchanged | Env 1, Compat 1, Pool 3, WidgetsDragHandle 2, PerfPanel 5, OptionsCompose 7. No `NEEDS_*` floor rises and no major changes | — | — |
| Standard `v2.65.0` | one version, one changelog entry (WS-01 opens it, WS-08 closes it) | WS-01..WS-08 | all eleven through `/wow-addon:revendor-standards` (M4, owner-gated) |
| Plugin `2.4.0` | `bin/ka0s-bounded`; `revendor-libka0s` takes its base from the provenance line and writes span bundles; the review brief's baseline is re-measured and derived at run time | WA-01..WA-03 | none (tooling) |

Three surfaces the plan uses are **already shipped and need no tag**: `LibKa0s-Bus-1.0`'s `Catalog`
(PM#52), the Schema minor-1 bracket `BulkRun`/`BulkAdd` (PC#18), and the Schema minor-1 primitives and
registry (AM#21's partial adoption). An item that depends only on these depends on no upstream release,
apart from the re-vendor it follows.

---

# Part A — the upstream end state

## A1 — WowAddonStandards v2.65.0

**Target.** `standards/STANDARDS.md` line 1 reads `# Ka0s WoW Addon Standard (v2.65.0, <date>)`. One dated
changelog entry holds numbered paragraphs (1)–(7) for WS-01..WS-07 and the WS-08 one-line summary. The
rulings are as follows.

- AUDIT.md: the re-vendor check counts same-day commits (`--since="$horizon 00:00"`). It reads every tag
  on line 1 of a two-tag `docs/revendor/<date>-v<A>-v<B>/` span bundle, and it grades by step 5 (an
  unrecorded re-vendor is doc-only, so **Low**). `audit-review-history` defines the span bundle.
- options-ui-§1 (WS-02): composers stay hollow and anti-pattern #73 stands. On a library-absent load, a
  host verb whose write targets a composed row either writes through the Schema `writeThrough` list
  (route (a), which is the SHOULD for `enable`/`disable`) or prints the library-absent line (route (b)).
  In both routes it never raises and never acknowledges a write that did not land. slash-commands-§1
  carries the line `%s is unavailable: the LibKa0s library did not load.` and sanctions a stub's single
  verbatim `DISABLED_LINE_FORMAT`, pinned with `Kit.assertLibraryConstant`.
- savedvariables-§1 (WS-03): defaults declare `schemaVersion = 0`, `NS.SCHEMA_VERSION` is the runner's
  target, the stamp advances only past a step that returned, and a profile-scoped step runs over every
  stored profile.
- events-frames-taint-§1 (WS-04): Core's `SafeRegisterEvent` family is the named helper. An addon that
  embeds no AceEvent gets a carve-out for one lazily created watcher frame. The architecture-§4 bus
  threshold is stated.
- compat (WS-05): `core/Compat.lua` is required only by an addon that owns a deprecated or version-variant
  call, and a dead fallback rung is deleted, not shimmed.
- WS-06: reserved verbs may be reused inside a noun's sub-tree. The value hold lives at
  `/<slash> debug hold`. A library-drawn tab strip is pinned by the library, not the consumer. The minimap
  row's path reads `<root>.minimap.shown` while storage stays `minimap.hide`.
- WS-07 text corrections: the debug buffer is 1500 lines, the bootstrap names an unread vararg `_`, the
  settings-panel table is `Page | Covers`, the TOC literal is gone, the editable `.png` is excluded by
  `.pkgmeta`, `synchronis` is on the list (92/30), and the lone-CR note is corrected.

**Acceptance.**
- Every WS-01..WS-08 `verify` command in `plan-data/items.json` passes.
- `head -1 standards/STANDARDS.md | grep -q v2.65.0`, and `grep -c 'v2.65.0' standards/STANDARDS.md` finds
  exactly one changelog entry heading.
- `grep -rnE '§[0-9]+\.[0-9]+' standards AUDIT.md NEW_ADDON.md` prints nothing.
- `git ls-files -z | xargs -0 grep -lI $'\r'` prints nothing (an LF repository).
- The branch is merged to the default branch and pushed. **This is the gate for every addon's
  standards-reference roll** (AT-26, AM-35, BL-25, CM-31, KC-27, LH-36, MM-32, PC-26, PF-25, PM-16, WG-30),
  because `/wow-addon:revendor-standards` reads the standard from GitHub. Those eleven items form M4: they
  are owner-gated, each runs after its addon's `<AB>-DOCS` item (which does not wait on them), and each
  carries its own three-place ripple. Each opens with the same gate check, and stops with the item left
  open if it misses:
  `gh api repos/tusharsaxena/WowAddonStandards/contents/standards/STANDARDS.md --jq .content | base64 -d | grep -m1 v2.65.0`
  hits.

**Non-goals.** Ruling the in-combat/combat-edge detection question (C28 stays local). A library migration
runner, since WS-03 fixes the template rather than shipping a runner. Any section renumbering.

## A2 — LibKa0s v1.56.0 and kit revision 26

**Target.** Every change listed in the surfaces table ships in one minor release, `v1.56.0`. The tag's
dependency closure includes LK-03 (the AceDB fake fidelity change), so v1.56.0 carries it. WA-02 and
WA-03 are plugin-only and are not ancestors of any re-vendor, but they are M1 items and M2 starts only once
M1 is complete. Each file that
moved bumps its LibStub minor once. Each bumped minor has its `docs/api/<Major>/version-<key>-docs.md`
(Status Current) and `members-<key>.json`, and the previous document is marked Superseded. The Options
key's one unreleased document is renamed as the key moves, and only `23.30.3.7.3` becomes Superseded.
`CHANGELOG.md`'s `## v1.56.0` block is dated, lists the minors, and carries a consumer-obligations section
naming the surface-parity churn and the behavioral kit flips. The release run (`--release 1.56.0`) is
committed with its `ANALYSIS.md`, and `docs/releasing.md` step 7 enforces the manifest precondition, the
`ANALYSIS.md` sub-step and the three-suites perf line (LK-31). The tag exists **locally**. It is pushed
only when the owner approves the LibKa0s merge. The branch is pushed to origin at the end of M1, unmerged.

**Acceptance.**
- LK-33's verify passes, and LK-03 is among its `depends_on`. For the newest bundle `S`: `jq -r .release $S` is `1.56.0`, `.git.dirty` is
  `false`, lint, tests and complexity are `pass`, perf is `skip` with reason (1), and
  `.suites.complexity.warnings` is `0`. `test -f $(dirname $S)/ANALYSIS.md` succeeds.
- `git tag -l v1.56.0` prints the tag. `git ls-remote --tags origin v1.56.0` is empty until the owner
  approves.
- `lua5.1 tests/run.lua` is green, including `test_versioning` (the docs, members json and CHANGELOG
  versions line agree with `lib.MODULES`), `test_kitsync` (`diff -r testkit tests/_kit` is empty and both
  trees carry `asserts.lua` and `prose_lists.lua`) and the kit layout cap.
- `grep -n 'Kit.VERSION = 26' testkit/framework.lua` hits. `wc -l testkit/framework.lua
  testkit/test_prose.lua LibKa0s/Options.lua LibKa0s/OptionsTabs.lua` are each under 1500, and
  `LibKa0s/OptionsWidgets.lua` is smaller than 3922 lines.
- The LK-05, LK-06 and LK-07 collection dry-runs exist for all eleven addons, and every red they recorded
  is assigned to an addon item: an M2 pre-re-vendor fix where the plan has one for that addon, or else
  the M3 item that clears it (Part B).
- `README.md` names standard v2.65.0, and `docs/releasing.md` has its provenance template at v1.56.0.

**Non-goals.** A major bump. Retiring any `NEEDS_*` floor. Pushing the tag before the owner approves the
LibKa0s merge, or merging the branch without the owner's go-ahead. Retiring
AuraMaster's `minimise` icon key. Splitting `LibKa0s/OptionsWidgets.lua` or the other band files beyond
LK-24/LK-28's peels: those are filed as issues (LK-32), not built.

## A3 — wow-addon plugin 2.4.0

**Target.** `bin/ka0s-bounded` is a POSIX exec wrapper (mode +x, LF), so the bare name resolves. The
`revendor-libka0s` command takes the delta base from the addon's provenance line, names bundles by tag,
writes WS-01 span bundles, and reports any sibling whose newest bundle's base disagrees with its history.
`agents/review.md`'s cross-addon baseline is measured at v1.56.0 (eleven addons, fifteen majors, kit 26,
Interface 120100, 22 slash roots), and each figure sits beside the command that produced it, with an
instruction to re-derive it at run time.

**Acceptance.** WA-01..WA-03 verify commands pass. `python3 scripts/test_bounded_runs.py` is green. `jq -r
.version .claude-plugin/plugin.json` prints `2.4.0`. `! grep -n '120007' agents/review.md` succeeds. After
a plugin reload in a new session, `command -v ka0s-bounded` resolves.

**Non-goals.** Any change to the standards-audit or review agents' grading. Retiring
`scripts/ka0s-bounded`.

---

# Part B — the re-vendor end state (RV-AT … RV-WG)

**Target.** In each of the eleven addons, `libs/LibKa0s/` and `tests/_kit/` are whole copies of the
`v1.56.0` tag's `LibKa0s/` and `testkit/` trees (the runner keeps its +x bit). The root `CLAUDE.md`
provenance line names v1.56.0 **in the same commit**. The re-vendor commit is copy-only: it carries the
payload, the provenance line and the re-vendor bundle, and nothing else. Every red that the kit-26
dry-runs predicted is fixed at its production cause, and no assertion is weakened.

The same rule holds in all eleven addons: the RV commit is green **or** lists its reds in its commit body.
The addon's M2 pre-fixes aim to make it green, its M3 items clear any remaining red, and the addon is green
again at the latest by `<AB>-DOCS`.

Where the plan has a pre-re-vendor fix, that fix is an M2 item that lands **before** the re-vendor commit,
depends on LK-33, and must pass on both the v1.55.0 payload and the v1.56.0 dry run. The RV item depends
on it, and the fix aims to make that re-vendor commit green:

| Addon | M2 pre-re-vendor items (land before RV) |
|---|---|
| AbsorbTracker | AT-01 (Schema degradation stub catches up to Schema minor 2: `SetMany`, `normalize`, `instanceId` forwarding, the `writeThrough` store) |
| AuraMaster | AM-01 (the lone CR at `tests/page_helpers.lua:80`, plus every other dry-run red), AM-02 (span bundle) |
| BankLedger | BL-01 (drop the `wow_mock` `C_Timer.After` no-op; the prune rides AceTimer), BL-02 (Schema stub `SetMany`, mirroring LK-22) |
| ConsumableMaster | CM-01 (`analysed`, `neighbours`, `synchronisation`, plus any other dry-run red) |
| KickCD | KC-01 (perf-analysis README spellings; the LSM fake's locale bits) |
| WhatGroup | WG-01 (the SetItemRef callback) |

LootHistory, MultiMeters, PanelMaster, PartyFrameEnhanced and PrettyChat have no M2 pre-fix. In any of
the eleven, if the re-vendor commit goes red because the new kit or library is stricter, the commit body
lists every failing case, and the addon's M3 items clear them. The predicted ones are the Schema-stub
`SetMany` parity case (LH-15, PM-01, PC-01) and PartyFrameEnhanced's `test_disabled` steps 3 and 5 (PF-05,
PF-06). WhatGroup's Options park/replay re-pin (WG-02) is an M3 item after RV-WG: any red at RV-WG is
listed in that commit's body, and WG-02 clears it.

The same commit writes the re-vendor record `docs/revendor/2026-09-23-v1.56.0/` **by hand**, following the
local `../wow-addon/commands/revendor-libka0s.md` as amended by WA-01. The installed plugin is fetched from
GitHub and does not carry WA-01 until the owner merges wow-addon, so the RV item depends on WA-01 and does
not run the command. `01_DELTA.md` line 1 is exactly `Delta: LibKa0s v1.55.0 -> v1.56.0`, followed by the
per-file LibStub minors, both payload diffs, the kit-revision pairing (25 -> 26), the majors this addon
consumes and the contract changes. `05_SUMMARY.md` sits beside it. Adoption decisions are not taken
there: they are the addon's M3 items.

**Acceptance (per addon).**
- `T=$(mktemp -d); git -C ../LibKa0s archive v1.56.0 LibKa0s testkit | tar -x -C $T; diff -r $T/LibKa0s libs/LibKa0s && diff -r $T/testkit tests/_kit`
  prints nothing.
- `test -x tests/_kit/run-automated-tests.sh` succeeds.
- `tests/test_vendor_sync.lua` is green against the tag the provenance line names, and
  `grep -n 'v1.56.0' CLAUDE.md` hits the provenance line.
- `head -1 docs/revendor/2026-09-23-v1.56.0/01_DELTA.md | grep -q 'v1.55.0 -> v1.56.0'` succeeds, and
  `05_SUMMARY.md` exists beside it.
- `git show --stat <RV commit>` touches only `libs/LibKa0s/`, `tests/_kit/`, `CLAUDE.md` and
  `docs/revendor/2026-09-23-v1.56.0/`.
- All eleven: SG steps 1–2 are green at the RV commit, or the commit body lists every red and each is
  cleared by a named M3 item, with the addon green again at the latest by `<AB>-DOCS`. In AT, AM, BL, CM,
  KC and WG, each M2 pre-fix was green on the v1.55.0 payload when it landed.
- SG step 3 (the regenerated `docs/test-cases.md` and badge after kit 26's `§` case names) holds from the
  addon's first later item that regenerates the inventory, and at the latest at `<AB>-DOCS`.

**Non-goals.** Adopting any new surface inside the RV commit. Fixing a red inside the RV commit. Editing
anything under `libs/` or `tests/_kit/` afterwards.

---

# Part C — the cluster end state

## C01 — Unrecorded LibKa0s re-vendor bundles

**Target.** Every tag each addon ever vendored is recorded. The span that lapsed (19–28 tags per addon,
v1.16.0/v1.18.0/v1.35.0 up to v1.53.0/v1.54.2/v1.55.0) is covered by **one** consolidated span bundle per
addon, `docs/revendor/<date>-v<A>-v<B>/`, holding only `01_DELTA.md` and `05_SUMMARY.md`. Line 1 of
`01_DELTA.md` is exactly `Delta: LibKa0s v<A> -> v<B> (span: v<A> v<...> v<B>)` and names every tag.
`05_SUMMARY.md` has one line per tag, reading either "carried by sweep, nothing adopted" or the adoption
commit's sha. The v1.56.0 re-vendor then writes its own normal bundle. Items: AT-25, AM-02, BL-23, CM-28,
KC-24, LH-34, MM-30, PC-25, PF-24, PM-18 and WG-29, plus WA-01 so the tool writes the shape from now on.

**Acceptance.**
- In each addon, the WS-01-amended AUDIT.md step-4 re-vendor check (vendored tags since the horizon, read
  from the provenance history with `--since="<horizon> 00:00"`, minus every tag on line 1 of every
  `docs/revendor/*/01_DELTA.md`) prints nothing, and that includes v1.56.0.
- `head -1 docs/revendor/*-v<A>-v<B>/01_DELTA.md | grep -oE 'v[0-9]+\.[0-9]+\.[0-9]+' | wc -l` equals the
  tag count the item derived from its CLAUDE.md history. For AuraMaster the span is v1.35.0–v1.54.2
  (22 tags, including v1.43.0 and v1.45.0).
- The kit prose and EOL gates are green over the new files.

**Non-goals.** Writing one bundle per lapsed tag. Editing any frozen bundle. Adding a "correction"
paragraph about AuraMaster's v1.55.0 base note: `v1.54.2 -> v1.55.0` is correct, because commit 329e1a3
re-vendored v1.54.2 kit-only.

## C02 — AUDIT.md playbook contradictions (upstream)

**Target.** AUDIT.md grades an unrecorded re-vendor by step 5's impact table (Low, doc-only), counts
same-day commits, and reads span bundles (WS-01). The standard's `settings-panel.md` row reads
`Page | Covers`, and the `.png` sentence says the file is excluded by `.pkgmeta` (WS-07). WhatGroup's
`docs/settings-panel.md` and `.pkgmeta` comment match the new wording (WG-26).

**Acceptance.**
- WS-01's verify passes, including `! sed -n '/Check every re-vendor commit has its bundle/,/Check every bus message name/p' AUDIT.md | grep -n '\*\*High\*\*'`.
- The amended recorded-side loop, run over a scratch span folder, emits all three tags.
- In WhatGroup, `grep -n '| Page | Covers |' docs/settings-panel.md` and `grep -n 'layout-§4' .pkgmeta`
  both hit, and `! git grep -n '120007' -- ':!libs' ':!docs/audits' ':!docs/reviews'` succeeds.

**Non-goals.** Re-grading findings already filed in frozen audit bundles.

## C03 — Event registration without per-event pcall isolation

**Target.** No authored `RegisterEvent`/`RegisterUnitEvent` call runs outside Core's `SafeRegister*`
family, except inside a Core stub's one-rung bodies. Each addon owns one rejected-names list
(`NS.RejectedEvents`, `NS.State.rejectedEvents` or `NS.EventRecord`, one per addon, as the item names it).
A player can reach that list: the `[Init]` summary names rejected events when there are any, and/or a
debug verb prints the list (`/at debug events`, `/bl debug scan`, `/mm debug diag`, `/lh debug events`,
`/kcd debug events`, `/cm dump events`, `/pfe status`, `/pm debug dump`, `/pc debug on` [Init], `/wg debug
on` [Init], `/am debug on` [Init]). LibKa0s itself adopts the helper where it registers, and records its
three widget-owned private frames in a Documented deviations row (LK-30). Items: LK-11, LK-30, AT-07,
AM-07, BL-06, CM-15, KC-04, LH-17, MM-07, PC-12, PF-10, PM-08, WG-06.

**Acceptance.**
- In each addon, `git grep -nE ':Register(Unit)?Event\(' -- core modules settings | grep -v SafeRegister`
  prints only the stub bodies in `core/CoreSetup.lua` (or the addon's equivalent), with no other hit.
- Each addon carries a red-first case of the shape "one retired event name does not abort the block". The
  case sets `__badEvents = { <NAME> = true }` (kit 26), enables, and asserts that every other event is
  still in `__registrations()`, that the rejected list holds the name exactly once (still once after a
  disable/enable cycle), and that nothing raised. It runs once with `C_EventUtils` present and once with
  `C_EventUtils = nil` (the pcall rung).
- Surface parity: every Core degradation stub carries the SafeRegister members it publishes, and the
  addon's `test_surface_parity` Core case is green. PanelMaster re-exports only `SafeRegisterEvent`, which
  is the member it calls.
- In client on 12.1: the debug surface prints "none"/no rejected clause, and a `/<slash> disable` then
  `/<slash> enable` restores every registration.

**Non-goals.** Library-side state, printing or a global rejected list. Requiring `C_EventUtils`. Changing
which events an addon listens to (C04 does that).

## C04 — Event subscription scope

**Target.** Ordinary non-unit event traffic rides the addon's AceEvent object. Private frames remain only
where WS-04's carve-out or the unit-filter carve-out sanctions them, and in that case they are fully
unregistered on stand-down. The standard's events-frames-taint-§1 and library-stack-§1 texts agree
(WS-04). Narrow-use events are registered by the feature that needs them, only while it is on.
- BankLedger drops the dead `GUILDBANKFRAME_OPENED/_CLOSED` registrations. It adopts
  `PLAYER_INTERACTION_MANAGER` only if an `/etrace` capture proves it fires (BL-07).
- PartyFrameEnhanced moves its session-long registrations into each owner's `syncEvents` (PF-09).
- WhatGroup's two private `PLAYER_REGEN_ENABLED` frames become a combat-end queue drained by its AceEvent
  handler (WG-05).
- AuraMaster's `UNIT_AURA` moves to the module's player/pet `RegisterUnitEvent` frame (AM-08).
- KickCD's combat listener becomes an AceEvent target, its dead `PLAYER_LOGIN` re-registration goes, and
  the spell-input cache invalidator is an AceEvent target (KC-06, KC-07).
- PrettyChat cites the carve-out and threshold (PC-12).
- MultiMeters measures `UNIT_SPELLCAST_SUCCEEDED` and `CHAT_MSG_SYSTEM` in two perf buckets (MM-19).

**Acceptance.**
- `grep -rn 'CreateFrame' core/State.lua` is empty (KC).
- `grep -n "RegisterEvent(\"UNIT_AURA\"" modules` is empty (AM), and
  `TS.unitFrame.__unitEvents.UNIT_AURA == {'player','pet'}`.
- WG `tests/test_disabled.lua` shows no raw frame keeping a registration after stand-down, and the
  combat-defer cases fire through `mock.__fireEvent('PLAYER_REGEN_ENABLED')`.
- BL: `NS.EventRecord.registered` has no `GUILDBANKFRAME_*` name.
- PF: with `target.enabled = false`, or solo, no `PLAYER_TARGET_CHANGED`/`RAID_TARGET_UPDATE`
  registration exists for `NS.TargetFrames.__ev`.
- MM: `tests/perf.lua` prints `spellEventOff/On` at 0 B/iter while disarmed. An in-client `/mm perf`
  capture is recorded under `docs/perf-analysis/<stamp>/`.
- SG green in each touched addon.

**Non-goals.** MultiMeters' registration decision for the two measured events. That is taken after the
capture, not in this cluster. Replacing unit-filtered `RegisterUnitEvent` frames. Adopting
`PLAYER_INTERACTION_MANAGER` on inference alone.

## C05 — Unannotated load-bearing TOC positions (toc-file-§5)

**Target.** Every TOC line whose position is load-bearing (a file-scope read of an `NS` member,
`GetModule` at load, or Setup ordering) has an at-line `LOAD-BEARING` comment naming the dependency.
Every conventional group says it is conventional. Where the addon can pin the order, a load-order case
does so. ARCHITECTURE/module-map restate the same load-bearing set without ordinals. Items: AT-20, BL-16,
CM-24, KC-23, LH-27, MM-24, PC-18, PF-20, PM-14, WG-20.

**Acceptance.**
- `grep -c 'LOAD-BEARING' <Addon>.toc` rises by the count each item names: AT +5, BL +2, MM +3, LH 6 or 7
  in total, PC 4 lines. `grep -n -i conventional <Addon>.toc` hits once per conventional group.
- Red-first order pins are green:
  - BL: "InsightsWidgets loads before Insights, and Schema before Slash, each annotated LOAD-BEARING".
  - PF: "LifecycleSetup loads before PerfSetup, and the TOC says why".
  - MM: CoreSetup/EnvSetup/OptionsSetup order plus the preceding-comment check.
  - KC: every file-scope `NS:GetModule` sits below its parent under a LOAD-BEARING comment.
  - PC: ARCHITECTURE's load-order line names every TOC-loaded authored file in TOC order.
- The TOC file list is unchanged:
  `diff <(git show <base>:<Addon>.toc | grep -v '^#') <(grep -v '^#' <Addon>.toc)` is empty.

**Non-goals.** Reordering any TOC line. Adding load-order tests where the addon already derives its order
from the TOC.

## C06 — Stand-down leaves timers, callbacks, drivers and frames armed

**Target.** A stand-down cancels every timer, unregisters every event, EventRegistry callback and secure
state driver, hides every owned frame and drops capture context (slash-commands-§7). A stand-up restores
exactly one of each. The disabled conformance suites can see these registrations, because the kit records
`kind = 'callback'` entries and starts frames shown. The items are:
- BL-01: the prune rides AceTimer and postpones rather than cancels.
- BL-03: `L:DropContext`.
- PF-04: the target/pet drivers are unregistered, not replaced with `hide`.
- PF-05: `EditMode.Exit` is unregistered and `burst()` arms nothing while suspended.
- PF-06: the fade and holder frames hide.
- MM-01: the latch holds on every show path.
- MM-21: the roster is bounded, with the branch chosen by the SM-06 observation.
- WG-01 and WG-10: `SetItemRef` is dropped and restored, and the survey uses the kit recorder.
- CM-06: flyout attribute drivers.
- AM-04: no container frames while stood down.
- AM-06: the coalescing and scan timers are canceled.
- KC-05: one cast filter frame per (module, unit), armed and disarmed.
- KC-07: the combat listener.

**Acceptance.**
- Each addon's `tests/test_disabled.lua` "every registration is unregistered" step is empty after
  stand-down, including `callback|…` entries, and "every frame that was on screen is hidden" holds against
  the kit-26 shown-by-default baseline.
- These red-first cases are green:
  - PF: `EventRegistry:TriggerEvent('EditMode.Exit')` while disabled leaves `#mocks.__timers() == 0`, and
    no target or pet button keeps `__drivers.visibility`.
  - KC: "two disable/enable cycles create no frames" (a frame delta of 0; it was +36 per cycle).
  - AM: "a disabled login builds no container frame", and "a queued apply and a queued scan are canceled"
    (`#mocks.__timers() == 0`).
  - WG: `disabled 3` names `callback:SetItemRef` under the mutation.
  - CM: no frame in `mock.attributeDrivers` still carries `kcmCombat` after the disable.
  - BL: "a movement made while disabled is not recorded after re-enable".
  - MM: "Disabled 10/11" (test-mode exit and `/mm toggle` under suspend show nothing).
- In client: `/fstack` after `/pfe disable` shows no `PartyFrameEnhanced_Fade_*`/`*_Holder` frame, and a
  disable in combat completes on regen with no `ADDON_ACTION_BLOCKED`.

**Non-goals.** Gating uncancellable callbacks on the latch as a substitute for canceling them. Changing
what a stand-up re-shows beyond restoring the pre-disable state.

## C07 — Disabled/suspended latch bypassed by UI paths

**Target.** Every UI path (show, unlock, test mode, toggle, reset, launcher click) reads one latch-aware
predicate per addon. A disabled or perf-suspended addon does not redraw, arm drag, re-show windows or lose
its settings category. The items are:
- MM-01/MM-02: `WindowProto:Show`, the test-mode exit, `/mm toggle` and the launcher, through
  `NS.IsStoodDown`.
- PM-02: an unlocked panel is hidden, stripped and undraggable while stood down.
- CM-05: CreateOptionsPanel park/replay (LK-25).
- CM-07: stand-up runs the discovery pass.
- CM-08: bare `/cm bar` toggles the stored flag.
- CM-09: an unlock on a switched-off bar says so.
- CM-14: the truthful comment, a Known Limitation, and a filed `LoadItem` issue.
- BL-04: Reset all re-runs the latch and announces `LedgerChanged` once.
- AM-05: the degraded latch is edge-triggered.
- AM-09: Test mode refuses while disabled on every surface.

**Acceptance.**
- These red-first cases are green:
  - PM "Disabled 5b" routes A, B and C.
  - MM "Disabled 10/11" and "launcher: a left click under a perf suspend shows nothing and prints the
    suspend line".
  - CM "a registration parked while the addon is stood down still registers on regen", "Disabled 9c",
    and "bare /cm bar toggles the stored flag during a perf hold".
  - BL "ResetEverything while disabled stands the addon back up" and "announces LedgerChanged exactly
    once".
  - AM "the degraded latch stands up and down only on an edge", and "the panel's Test mode row refuses
    to start while disabled and prints one refusal line".
- `! git grep -nE '_settingsCategoryID|registerPendi' -- settings core` in CM.
- `grep -n 'IsDisabled' core/LauncherSetup.lua` hits only inside `isEnabled`/`disabledLine` in AM and MM.
- `gh issue list -R tusharsaxena/ConsumableMaster --search 'LoadItem in:title'` shows the filed issue.
- In client: `/mm disable` then untick Test mode shows no window. `/cm disable`, `/reload` in combat and
  leaving combat shows the category and its Enable checkbox.

**Non-goals.** Hydrating the CM panel's item data while disabled. That stays a documented Known Limitation
with a filed issue.

## C08 — Disabled refusal line and the launcher disabled-state seam

**Target.** There is one refusal line per addon: the library's `DISABLED_LINE_FORMAT` formatted with the
brand and the enable verb. A degraded Slash stub may carry those bytes verbatim, and only those bytes. It
pins them with `Kit.assertLibraryConstant(<stub format>, 'LibKa0s-Slash-1.0', 'DISABLED_LINE_FORMAT')`, or
with the byte-equality fallback against a live load where the kit resolves the name to the Slash instance.
Launchers pass `isEnabled`/`disabledLine` to Launcher minor 2 instead of hand-writing a gate. Launcher
notices print once, untagged. Lock-row fallbacks print the same line. Items: LK-16, LK-18, PF-07, PF-12,
MM-02, LH-11, LH-16, WG-13, with the adopters AT-09/AT-10, AM-09, BL-08, CM-09, KC-19 and PC-02 sharing
the shape.

**Acceptance.**
- `! grep -n '\[LibKa0s\]' LibKa0s/Launcher.lua` succeeds. The LK-16 cases "with isEnabled false, a left
  click prints disabledLine and never calls onClick" and "two Register calls print NO_ICON once" are
  green.
- Each touched addon's `assertLibraryConstant` (or byte-equality) case is green and red under a one-byte
  drift.
- WG "no seam re-spells the refusal line" scans `core/*.lua` and `settings/*.lua` for the literal
  `is disabled` outside the one constant, with no hit.
- `grep -n 'isEnabled\|disabledLine' core/LauncherSetup.lua` hits in AT, AM, BL, CM, LH, MM and WG. Host
  left-click gates are deleted: `grep -n RefuseIfDisabled core/LauncherSetup.lua` in BL and
  `git grep -n 'GetSetting("enabled") == false' -- core/LauncherSetup.lua` in AT are both empty.
- PF: while disabled, `NS.SetByPath('locked', false)` returns false, prints exactly one line equal to
  `cli:DisabledLine()`, and leaves `locked` true.
- In client: `/<slash> disable`, then a left-click on the minimap button prints one line of the form
  `<Brand> is disabled — enable it with /<slash> enable`. Right-click still opens settings.

**Non-goals.** Copying `FormatRow` or any other library string into a stub. Adopting the Launcher gate in
PartyFrameEnhanced and KickCD, which is left to their re-vendor adoption interviews.

## C09 — Test-kit and mock fidelity gaps

**Target.** The vendored kit behaves like the client where tests depend on it (LK-03, LK-04, LK-05):
- AceDB `CopyProfile`/`DeleteProfile` raise AceDB-3.0's own message on the current or a missing profile,
  unless `silent`.
- `SetProfile` strips defaults from the outgoing profile.
- `CreateFrame` starts shown.
- `EventRegistry` records callbacks.
- Frame registration honors `__badEvents`.

Local mocks catch up rather than diverge:
- BL-01: `wow_mock` stops no-opping `C_Timer.After`.
- CM-02: the local AceDB fake strips defaults and raises the same way.
- MM-10: the MultiMeters mock reads its version from the TOC.
- PF-05: the stand-down suite reads callbacks.

**Acceptance.**
- LibKa0s `tests/test_mock_record.lua` has the seven red-first cases from LK-03, asserted with
  `assertErrorMatches` against the verbatim AceDB text, citing `AceDB-3.0.lua:531-537/:581-587`.
  `tests/test_mock_events.lua` has LK-04's cases. "A new frame is shown until hidden, as in the client"
  is green.
- CM "AceDB fake: a profile switch strips at-default values from the outgoing profile" is green, and
  `wc -l tests/wow_mock.lua` stays under 1500.
- MM "the default fixture's Version is the TOC's" is green, and
  `grep -n '0.1.0' tests/wow_mock.lua tests/test_envsetup.lua` is empty.

**Non-goals.** Retiring ConsumableMaster's local AceDB fake. That needs the kit to gain the string-method
callback form and `db.profiles`, which is a separate LibKa0s issue. Modeling AceDB's `'*'`/`'**'`
wildcard arms. They are named in a comment, not built.

## C10 — Slash verbs that misreport their outcome

**Target.** Verbs validate their input and echo the real resulting state:
- `profile new <existing>` refuses with "already exists" and never switches or wipes.
- `use`, `copy` and `delete` refuse a missing name, and `copy` refuses the current one. There is no raw
  AceDB error and no pcall wrapper around `db:CopyProfile`.
- `/at lock|unlock|enable|disable` echo the stored value in the set shape (`locked = true`) and refresh the
  open panel. An in-combat unlock prints the refusal and then `locked = true`.
- The AbsorbTracker value hold moves to `/at debug hold <value> [secs]` with a validated duration.
  `/at test` is gone.
- LibKa0s `CliSet`/`CliReset` print the seam's refusal (LK-17). A PartyFrameEnhanced profile switch, copy
  or reset places elements by the new profile whatever the bus dispatch order (PF-02).

Items: LK-17, AT-03, AT-04, AT-11, PF-01, PF-02.

**Acceptance.**
- PF `tests/test_slash.lua` cases (a)–(e) of PF-01 and AT `tests/test_slashcmds.lua` "profile new
  refuses an existing name" are green, and each is red under removing its `exists()` guard.
- `tests/test_profile_switch.lua` (PF) is green: `NS.Anchor.ApplyAll()` directly after `SetProfile('Free')`
  places every element by the new profile.
- LibKa0s `tests/test_slash_refusal.lua` is green: `set` answering `false,'Invalid value for x','must be
  1-10'` prints both lines and no echo, and `CliReset` with `applyDefault` false prints `NO_DEFAULT`.
- AT: `git grep -n '/at test' -- ':!docs/audits' ':!docs/reviews' ':!docs/investigations' ':!docs/superpowers' ':!docs/automated-tests' ':!docs/revendor'`
  is empty, and `tests/test_debughold.lua` exists with the negative-duration case.
- In client (real AceDB-3.0): `/at profile copy NoSuchProfile` and `/pfe profile copy <current>` print
  one refusal each, and BugSack stays clean.

**Non-goals.** New profile verbs. Renaming `/at debug` sub-verbs other than the hold.

## C11 — Profile switch and SavedVariables migration correctness

**Target.** Every addon with a migration runner follows savedvariables-§1 at v2.65.0 (WS-03):
- defaults declare `schemaVersion = 0`, so AceDB never strips a stamp equal to a current-version default;
- `NS.SCHEMA_VERSION` (or the addon's named constant) is the target;
- the stamp advances only past a step that returned without raising;
- a profile-scoped step runs over every stored profile (the raw SV `profiles` table), or idempotently
  per profile on `OnProfileChanged` with a per-profile stamp;
- every step is idempotent against a fresh default profile.

Profile switches leave no stale cached config: PF-02, where Anchor reads the live section. Items: AT-06,
AM-10, BL-11, CM-16, KC-03, LH-12, MM-12, PC-03, PF-08, PM-10, WG-08.

**Acceptance.**
- In every addon, `grep -rn 'schemaVersion = 0' defaults core` hits the defaults declaration, and a
  red-first case asserts `NS.defaults.global.schemaVersion == 0` (or the addon's equivalent).
- Red-first cases per addon:
  - "a profile-scoped step lifts a non-active stored profile": KC's color steps via `SetProfile('Alt')`,
    PM's frame-name step on `profiles.Other`, and the AT, PC and PF injected steps.
  - "a raising step leaves the stamp at the last completed step".
  - WG "the stamp survives AceDB's logout strip, so the first real migration runs".
- `lizard` keeps each `RunMigrations` at CCN 10 or below (AT, PF, PM) and 15 or below elsewhere.
- In client, after logout, `WTF/Account/<acct>/SavedVariables/<Addon>.lua` shows the current stamp stored
  (for example `WhatGroupDB.global.schemaVersion = 1` after WG-08, and `schemaVersion = 8` for
  LootHistory after LH-12). The minimap rename (C46) adds no step and bumps no stamp in any addon.
- The minimap rename's carry-over is pinned test-first in all eleven addons, not by a migration: see C46's
  carry-over criterion.

**Non-goals.** A shared library migration runner (declined by design decision (3)). Rewriting historic
steps beyond making them idempotent.

## C12 — British spellings and the kit prose gate

**Target.** The kit-26 prose gate scans the store-root files (`docs/automated-tests/README.md`,
`RESULTS.md`, `docs/perf-analysis/README.md`, named file by file), skips `docs/superpowers/` and
`docs/investigations/`, and publishes `synchronis` (92/30). LibKa0s's own authored prose, including tests
and the live API documents, is US English (LK-29), with two ratified exclusions: the AceTimer/C_Timer
`.cancelled`/`IsCancelled` identifiers and the gate's own fixtures. The addons fix every hit:
- CM-01: `analysed`, `neighbours`, `synchronisation`.
- KC-01: the perf-analysis README.
- PM-17: restores the two frozen specs' `catalogued`, now that `docs/superpowers/` is skipped.
- MM-13: US `minimize` everywhere authored, with a v15→v16 SavedVariables migration of the two stored
  keys (`frame.minimised`, `showMinimise`) in every window of every profile.

**Acceptance.**
- LibKa0s `tests/test_kit_prose.lua` fixture cases are green, and `PUBLISHED_BRITISH == #BRITISH == 92`.
  LK-29's widened British gate is green over `tests/*.lua` and the live docs set, and it was red on the
  pre-sweep tree.
- `! git grep -n -iE 'analysed|neighbours|synchronis' -- docs/perf-analysis/README.md docs/settings-panel.md`
  succeeds in CM and KC.
- MM: `git grep -n -i 'minimis' -- ':!libs' ':!tests/_kit' ':!docs/audits' ':!docs/reviews' ':!docs/automated-tests' ':!docs/revendor' ':!docs/superpowers' ':!docs/perf-analysis'`
  hits only the library icon key. `tests/test_migrations.lua` (a)–(c) are green: two profiles × two windows
  migrate, a second run is a no-op, and a fresh install has no British key. In client, a collapsed window
  stays collapsed across the upgrade.
- PM: `git diff e30e329^ -- docs/superpowers/specs/2026-07-31-panel-artwork-design.md docs/superpowers/specs/2026-08-02-wiki-artwork-import-design.md`
  shows no line-5 difference.

**Non-goals.** Renaming the LibKa0s `minimise` icon key or its `.tga`. Editing released CHANGELOG entries'
quoted "was → is" lines. Editing any frozen bundle.

## C13 — Automated-test runner cannot record the performance-§12 exemption

**Target.** `testkit/run-automated-tests.sh` reads the `## Documented deviations` register (in
`docs/ARCHITECTURE.md` for an addon, root `CLAUDE.md` for the library). A `performance-§?12` row makes the
perf skip record reason (2), `performance-§12 no-combat-path exemption (ratified; <file> -> Documented
deviations)`. An unparseable register exits 2. Empty watch-list tables print their header row
(LK-09). `docs/releasing.md` carries the three-suites release-notes line (LK-31). BankLedger, LootHistory
and PrettyChat record reason (2) in a fresh bundle. PrettyChat's and LootHistory's `performance.md` shrink
to one screen, with the sweep moved to a Tier-3 page (PC-23, LH-31). PanelMaster (performance-§1 row,
"§12 does not apply") and LibKa0s record reason (1).

**Acceptance.**
- LibKa0s `tests/test_kit_runner.lua` is green: reason (2) with a row, reason (1) without, exit 2 on a
  malformed register, and a headed empty complexity table. `! grep -n "printf 'None" testkit/run-automated-tests.sh`
  succeeds.
- In BL, LH and PC: `jq -r '.suites.perf.skipReason' docs/automated-tests/<stamp>/manifest.json | grep 'performance-§12'`
  hits. In PM the newest manifest's `skipReason` is reason (1), and the register row is unchanged.
- `wc -l docs/performance.md` is 40 lines or fewer in LH and PC. `grep -n 'combat-path-sweep.md'` (LH) and
  `grep -n 'performance-sweep.md'` (PC) resolve from ARCHITECTURE and performance.md.

**Non-goals.** Relabeling PanelMaster's performance-§1 row as §12. `KA0S_PERF_EXEMPT=1` as a way around a
present register.

## C14 — Stale automated-test records, watch lists and release bundles

**Target.** Each of the eleven addons ends the cycle with one fresh bundle recorded on kit 26 at a clean
HEAD after all its M2 and M3 items (`<AB>-DOCS`). The owner-gated M4 standards roll that follows is
documentation only (the three-place reference and the retired-notation sweep), and the `<AB>-DOCS`
bundle stands. `RESULTS.md`'s newest row names that stamp. The bundle carries an
`ANALYSIS.md`. `docs/test-cases.md` and the README badge match the run. Every watch-list row has a
terminal disposition that points at a live issue or a dated re-rule, never "watch, no action" citing a
retired tracker. LibKa0s's release bundle does the same and names once the six tags that shipped without
a bundle (LK-33). Peel issues are filed for every band file whose disposition asks for one: LK-32
(LibKa0s), CM-30, KC-28, LH-35 and MM-23's peel.

**Acceptance.**
- For each addon, `S=$(ls -d docs/automated-tests/2*/ | tail -1)`. `jq '.suites' $S/manifest.json` shows
  lint `pass`, tests `pass`, complexity `pass` with `warnings == 0`, and perf `pass` or a skip with the
  reason C13 names. `jq -r .git.dirty $S/manifest.json` is `false`. `test -f $S/ANALYSIS.md` succeeds.
- SG step 3 holds, and `RESULTS.md`'s newest row is `$S`.
- Issues exist:
  - `gh issue list -R tusharsaxena/LibKa0s --label state:triaged --search 'peel OR split'` lists LK-32's
    issues.
  - `gh issue list -R tusharsaxena/ConsumableMaster --search 'Peel settings in:title'` lists CM-30's.
  - `gh issue list -R tusharsaxena/LootHistory --search 'Peel modules/Analytics.lua'` shows one open
    issue, labeled `state:triaged` and `severity:low`.
  - KickCD's band issues carry `state:triaged`.
- KickCD `grep -n 'A-2\|KCD-30' docs/module-map.md docs/automated-tests/RESULTS.md` cites no retired
  tracker as a live disposition.

**Non-goals.** Backfilling `ANALYSIS.md` into historic bundles. Editing any frozen bundle. A version bump
or tag in any addon.

## C15 — Complexity gate, file-size band and test runtime

**Target.** No authored function in any repo is above CCN 15. AuraMaster's two offenders are gone:
`Cat.SyncUserCategories` (CCN 25) is split into phases and `renderCategories` (CCN 16) is table-dispatched
(AM-13). If `defaults/Categories.lua` would cross 1500, the user-category section is peeled into
`defaults/UserCategories.lua`. No authored `.lua` exceeds 1500 lines. At-cap and band files are peeled or
carry a filed issue:
- MM-23 peels `tests/test_provider.lua` (1500) into files each under 1000.
- KC-13 peels the Spells row builders into `settings/Spells_Rows.lua`, taking Spells.lua to about 1100.
- AbsorbTracker's `tests/test_helpers.lua` gets its disposition in AT-DOCS.
- CM-30 files the Panel.lua/Category.lua issues.

LibKa0s's four at-15 functions are dispositioned in the release ANALYSIS (LK-33). AuraMaster's commit gate
runs sharded (`--jobs`) after measurement (AM-22).

**Acceptance.**
- `lizard -l lua -x './libs/*' -x './tests/_kit/*' -C 15 -w .` prints nothing in all twelve repos. In
  LibKa0s `.suites.complexity.warnings == 0`.
- SG step 6 prints nothing in all eleven addons.
- `wc -l tests/test_provider*.lua` (MM) shows each file under 1000, and the case names and totals are
  unchanged (`--list | sort` differs only in suite attribution). The KC peel keeps
  `git diff --stat tests/` empty.
- AM: `$B lua5.1 tests/run.lua` and `$B lua5.1 tests/run.lua -j 1` print identical totals, and the wall
  times are recorded in the commit body.

**Non-goals.** Lowering the CCN ceiling. Peeling any file that is under the cap and has no filed disposition
asking for it. Splitting production files by line count alone.

## C16 — ARCHITECTURE hub size and one-screen doc limits

**Target.** Each addon's `docs/ARCHITECTURE.md` is a hub of about 400 lines or fewer. Every mandated
section is about 60 lines or fewer, with the overflow moved (never deleted) to a Tier-2/3 topic doc:
`schema.md`, `settings-panel.md`, `message-bus.md`, `lifecycle.md`, `stand-down.md`,
`disabled-state.md`, `texture-paths.md`. An exempt `performance.md` fits one screen. Two stated
exceptions apply: MultiMeters' hub is at or under 560 lines, with the texture census moved and two
catalog declines given register rows (MM-28), and ConsumableMaster's hub is at or under 420 lines (CM-26).
Items: AT-24, AM-33, BL-19, CM-26, KC-26, LH-30, LH-31, MM-28, PC-23, PM-21, WG-28.

**Acceptance.**
- `wc -l docs/ARCHITECTURE.md` is ≤400 in AT, AM, BL, KC, LH, PM and WG, ≤420 in CM, and ≤560 in MM.
- `awk '/^## /{if(n)print s, NR-n; s=$0; n=NR}' docs/ARCHITECTURE.md` shows no mandated section over about
  60 lines.
- Each addon's doc-structure/docmap test is green, and a new topic doc has its map row.
- MM `tests/test_texture_paths.lua` is red under deleting either new register row.
- CM `! grep -n '^| \`preview-mode\`' docs/ARCHITECTURE.md` succeeds.

**Non-goals.** Deleting content to meet the budget. Restructuring Tier-2 docs beyond receiving the moved
sections.

## C17 — Tier-2 doc set

**Target.** Every documentation-map row tells the truth. A doc whose trigger has fired exists and is
marked Present:
- BL-21 `debug.md`;
- KC-25 `debug.md`;
- MM-27 `slash-dispatch.md`, `message-bus.md`, `profiles.md`;
- PM-20 `compat-layer.md` (eight shims).

The `module-map.md` files list every test and tool file (PM-22, AT-22). `compat-layer.md`/`debug.md`
document only the addon's own surfaces and never restate LibKa0s contracts (WG-24, KC-25). Frozen stores
are registered as Tier-3 rows (AM-31: `docs/spell-research/`). The standard's settings-panel row wording
is consistent (WS-07), and WhatGroup's `settings-panel.md` follows it (WG-26).

**Acceptance.**
- `test -f` holds for each named doc, and `grep -n '<doc>' docs/ARCHITECTURE.md | grep Present` hits.
  MM's three map rows have 0 `Not applicable`.
- PM: `for f in tests/*.lua tools/artwork/*.py tools/sunn/*.py; do grep -q "$(basename $f)" docs/module-map.md || echo MISSING $f; done`
  prints nothing, and `grep -c '^function Compat\.' core/Compat.lua` equals the doc's section count (8).
- KC `grep -cE '^\| \`(IsSecret|GetSpellCooldown|GetSpellInfo|GetSpellTexture|GetSpecialization|GetSpecializationInfo)\`' docs/compat-layer.md`
  is 0. WG `! grep -in 'eight' docs/compat-layer.md` succeeds.
- AM `tests/test_docs.lua` "every .md under docs/ appears in the documentation map" accepts the Tier-3
  store row, and it is red for an unregistered `docs/<store>/x.md`.

**Non-goals.** Writing a Tier-2 doc whose trigger has not fired. Re-documenting library API in addon
docs.

## C18 — Documented-deviations register hygiene

**Target.** Every register row is live: its rule is current, its trigger has not fired or has been
re-checked and dated, its evidence ids resolve, and it records a real deviation, never compliant
behavior. The fixes are:
- Stale rows are retired: AT-23 (the unit-filter carve-out is not a deviation), PF-22
  (events-frames-taint-§1), PC-21 (debug-logging-§2), CM-26 (preview-mode) and BL-05's expired
  options-ui-§12 row.
- Real declines get rows: PF-22 (library-stack-§6 for the EllesmereUIDB read, option (b)), LH-29
  (localization-§4), MM-28 (two catalog declines), LK-30 (the LibKa0s widget-owned private frames) and
  WG-12 (options-ui-§1 route (b), the WhatGroup#22 ruling).
- AuraMaster's unratified layout-§1 over-cap rows disappear because the files are peeled (AM-23..AM-26,
  the owner's #16–#19). The census heading stays with an empty table.
- Untriggered rows get a dated re-check (BL-24: `Re-checked 2026-09-23`, four rows).
- The WhatGroup register gate can fail (WG-22).

**Acceptance.**
- Each addon's register parser (the kit's `deviationRows`, via `test_layout_cap`/`test_prose`) is green.
- These row checks hold:
  - `grep -n 'library-stack-§6' docs/ARCHITECTURE.md` (PF) hits once, and
    `! grep -n '^| \`events-frames-taint-§1\`' docs/ARCHITECTURE.md` (PF) succeeds.
  - `grep -n '^| \`localization-§4\`'` (LH) and `grep -n '^| \`localization-§1\`'` (WG) hit.
  - `! grep -n 'WG-A-08\|WG-R-06' docs/ARCHITECTURE.md` (WG) succeeds, and WG's `test_register.lua` is
    red under restoring `WG-A-08` in a Why cell.
  - `grep -c 'Re-checked 2026-09-23' docs/ARCHITECTURE.md` (BL) is 4.
  - `grep -n 'options-ui-§12' docs/ARCHITECTURE.md` (BL) finds no register row.
  - `grep -rn 'LIBKA0S-05'` (PC, outside frozen bundles) is empty.
- AM: SG step 6 prints nothing, and the census preamble reads "No authored file is over the cap".
- LibKa0s `grep -n 'events-frames-taint-§1' CLAUDE.md` and `grep -n '1f1790c' CLAUDE.md` hit.

**Non-goals.** Ratifying a deviation to avoid a fix that is in scope. Rewriting rows whose rule and
trigger are current.

## C19 — Issue-store label and premise housekeeping

**Target.** Every closed issue in the touched repos carries a terminal label (`state:done` or
`state:will-not-do`). No open issue carries `state:done`. Triaged issues whose premise is resolved are
closed with a comment naming the evidence. The work is BL-24 (#3), MM-31 (#4, #21, #24), AT-DOCS (#10,
#25, #26), PM-15 (#19, #20, #22, #23, #24, plus one new `state:triaged` issue carrying the architecture-§5
option (a)), AM-28 (#10) and KC-28 (#15 closed, #9 retitled, #12 annotated). Every `gh` write is spaced at
least 5 s apart and happens after the owner's approval.

**Acceptance.**
- `gh issue list -R tusharsaxena/<Repo> --state closed --label state:triaged` and `... --label state:untriaged`
  are empty for AT, AM, BL, KC, MM and PM.
- `gh issue list -R tusharsaxena/<Repo> --state open --label state:done` is empty.
- These spot checks hold:
  - `gh issue view 3 -R tusharsaxena/BankLedger --json state,labels` shows CLOSED with `state:done`.
  - `gh issue view 15 -R tusharsaxena/KickCD --json state -q .state` is CLOSED.
  - `gh issue view 9 -R tusharsaxena/KickCD --json title -q .title` has no `[Optional]`.
  - `gh issue list -R tusharsaxena/PanelMaster --state open` lists none of 19, 20, 22, 23, 24.

**Non-goals.** Triaging `state:untriaged` issues outside the findings. Closing any open enhancement not in
OWNER_SCOPE (for example MultiMeters #2, #8–#12, #18, LootHistory #9, #11, #16, #17, BankLedger #1, #2,
WhatGroup #1, #2, #4, PartyFrameEnhanced #12, PanelMaster #47's split).

## C20 — Malformed standards citations (documentation-§6)

**Target.** Every citation to the standard is `<section-file>-§<N>`. There is no retired global `§N`, no
dotted or space form, no `§`-less dash form, no literal `\194\167` bytes and no `<file>.md:<line>` form
(for example `packaging.md:28` becomes `packaging`). The kit's own case names and strings carry `§`
(LK-08), so a regenerated `docs/test-cases.md` renders them correctly. The LibKa0s ASCII gate scopes to
the shipped `LibKa0s/` payload. Items: LK-08, AT-21, BL-20, CM-27, KC-22, LH-24, MM-26, PF-DOCS, WG-21,
WG-DOCS.

**Acceptance.**
- LibKa0s: `! grep -nE '"[^"]*(localization|line-endings|layout|testing)-[0-9]' testkit/*.lua` succeeds,
  and "the ASCII gate scans LibKa0s/ and not testkit/" is green.
- In each addon, with frozen stores excluded:
  - `git grep -nE '[a-z-] §[0-9]|(^|[^a-z0-9-])§[0-9]+|(localization|layout|line-endings|testing|slash-commands)-[0-9@]|packaging\.md:28|lint\.md|§[0-9]+\.[0-9]+' -- ':!libs' ':!tests/_kit' ':!docs/audits' ':!docs/reviews' ':!docs/automated-tests' ':!docs/revendor' ':!docs/superpowers' ':!docs/investigations'`
    prints nothing.
  - LH `grep -rn 'disabled-§' tests/*.lua docs/test-cases.md` is 0, with exactly 12 renamed lines and an
    unchanged count.
- `docs/test-cases.md` is regenerated after the kit-26 re-vendor in every addon (SG step 3).

**Non-goals.** Rewriting citations inside frozen bundles or vendored trees.

## C21 — Doc prose and file:line drift

**Target.** Stated inventories, counts, load orders and citations in `ARCHITECTURE.md`, `module-map.md`,
`performance.md`, `schema.md`, `CLAUDE.md` and `DEPENDENCIES.md` match the tree. Hand-maintained counts are
replaced by pointers to their generated source, or by symbol citations, or they are pinned by a test:
- MM-29: the hub's file count matches `git ls-files`.
- PF-23: the bus Consumers cells are derived from `RegisterMessage` sites.
- AM-34: a docs-gate case refuses a citation that lands on a comment or blank line.
- LK-30: the LibKa0s figures point at RESULTS.md's generated lint sentence.
- KC-14: perf nesting reports the Rebuild-path parent (a `rebuildEmit` root bucket) and the bucket table
  matches the descriptor.

Items: LK-30, AM-30, AM-34, BL-20, CM-23, CM-24, KC-14, KC-26, LH-28, MM-29, PC-20, PF-19, PF-22, PF-23,
PM-22, WG-25.

**Acceptance.**
- These red-first doc tests are green: MM "the hub's file count matches git ls-files", PF "every
  receiving module's name appears in that message's Consumers cell", AM "citations landing on '--' lines"
  and KC "every spellState note names its real parent".
- LibKa0s:
  - `! grep -n -i 'eighty' CLAUDE.md docs/releasing.md DEPENDENCIES.md` succeeds.
  - For every `` `(LibKa0s|tests|testkit)/*.lua` `` named in `CLAUDE.md`, `wc -l` equals its stated figure.
- PF: every figure in `docs/performance.md` equals the current `tests/perf.lua` output, and
  `grep -cE '^function Compat\.|^Compat\.[A-Za-z]+ *=' core/Compat.lua` is 15.
- These greps return nothing: WG `grep -n 'FIFO\|row above'`, PC `grep -rn 'packaging.md:28\|40/60\|second reader\|Slash minor 13'`,
  CM `git grep -nE 'macroBar\.point\|x\|y|restoreProfileDefaults|TECHNICAL_DESIGN'`, and each item's
  named stale-phrase grep.

**Non-goals.** Editing frozen bundles. Replacing every line citation with a symbol where the line
citation is correct and inside a doc that a test pins.

## C22 — Stale or misplaced code comments

**Target.** Source comments describe current behavior, sit above the function they document, and carry no
review-round narration. The items are:
- AM-27: unfuse the Database doc blocks, drop "fix round" narration, fix the "500-line" buffer.
- MM-25: ShouldShow doc, handler docs, ladder step numbers, load order.
- WG-21: stale taint and ticker comments, file homes, counts.
- PM-09, PM-10, PM-19: the printer home, the AceConsole embed, the stamp sentences.
- PC-10: the Test tooltip names the debug console, and the resetall help row says "every setting".
- AT-04, AT-22, CM-23, CM-24, KC-22, LH-28.

**Acceptance.**
- For comment-only items, `git diff -U0 | grep '^[-+]' | grep -vE '^[-+]\s*--|^[-+]{3}'` prints nothing
  (AM-27's check), and the case count is unchanged.
- These greps are empty: `grep -rnE 'fix round|review round|CORRECTION \(review' core modules settings defaults`
  (AM), `grep -n '500-line' core/DebugLogSetup.lua` (AM), and
  `grep -rn 'recovery measures\|AceGUI.s own :Print\|defined in core/Util.lua' core docs/*.md` (PM).
- MM `grep -n 'STEP 2' core/MultiMeters.lua` is preceded by a STEP 1.
- PC's red-first cases are green: "no locale string tells a player /pc test prints to chat" and "the
  resetall help row says it resets every setting".

**Non-goals.** Behavior changes hidden inside comment-only commits. The one exception is WG-21's harmless
`stopCooldownTicker(self)` argument drop.

## C23 — README and DEPENDENCIES.md content

**Target.** READMEs say only true, current, player-facing things:
- no removed sections (CM-25 "What's new in 1.6.2");
- no angle-bracket placeholders (PM-24);
- the default retention is disclosed (BL-22: 30 days);
- no deferred-config promise (KC-15, where `/kcd resetposition` also restores every unit's icon grid);
- Usage ends on a one-sentence configuration signpost (LH-32, PM-24);
- Version History rows speak to players (PC-24, AM-34).

`DEPENDENCIES.md` cites correctly, groups its tools correctly, and names Python 3 and Pillow for the logo
recipe under Release/assets (AM-29, PC-24, WG-27, with lizard labeled as required at release). The root
`CLAUDE.md` puts the green gate before the provenance line (LH-33). PM-23 cites the kit by function name
and re-derived line.

**Acceptance.**
- `grep -n '30 days' README.md` (BL) hits. `! grep -n "What's new" README.md` (CM) succeeds.
  `grep -nE '<[a-zA-Z][a-zA-Z _-]*>' README.md` (PM) finds no placeholder.
  `grep -n 'waits until combat\|opens the moment combat' README.md` (KC) is empty.
- `grep -n 'python3-pil\|import PIL\|Pillow' DEPENDENCIES.md` hits in AM, PC and WG.
- LH `grep -n '^## ' CLAUDE.md` lists Green gate before Vendored LibKa0s.
- KC "/kcd resetposition restores the focus grid too" is green.
- The kit prose gate is green over each README.

**Non-goals.** README screenshots. They are AuraMaster #3's follow-up, captured in client (AM-32), and are
not a gate.

## C24 — Namespace bootstrap and self-naming file headers

**Target.** Every TOC-loaded authored file opens on the namespace bootstrap on line 1
(`local <name|_>, NS = ...`, with `_` for an unread vararg per WS-07), followed within lines 2–4 by a
`-- <that path> — ` self-naming header. `NS.<X>` publishes are idempotent: no bare `NS.X = {}` over an
existing table (PC-16). Logo paths derive from `addonName` (PF-21). Items: WS-07, PF-21, PC-16, AT-22.

**Acceptance.**
- PF `tests/test_loadorder.lua` "every TOC-listed authored file opens on the namespace bootstrap" is green
  (it was red on 13 files).
- PC `tests/test_doc_structure.lua` "every TOC-loaded authored file names its own path in its first
  comment" and "no module publishes NS.<X> with a bare table constructor" are green.
- PF `NS.Constants.LOGO_PATH == 'Interface\\AddOns\\PartyFrameEnhanced\\media\\logos\\partyframeenhanced.logo.tga'`
  holds.
- luacheck stays 0/0 without a `211` suppression for `addonName`.

**Non-goals.** Renaming files. Reformatting file bodies.

## C25 — Unused `.luacheckrc` read_globals

**Target.** No `.luacheckrc` allowlists a global that no authored file reads, or a removed or deprecated
client global, so a regression cannot lint clean. WhatGroup's config also excludes `docs/revendor/`, as
the template does. Where an addon has a lint-config test, it keeps the list honest: AM-21 checks that
every `read_globals` name is referenced, and KC-21 checks that no deprecated spell/spec global is
whitelisted for shipped code. Items: AT-17, AM-21, KC-21, MM-11, PC-17, PF-14, WG-18.

**Acceptance.**
- `luacheck .` stays 0/0 in each addon with the names removed.
- `grep -n 'GetSpellInfo' .luacheckrc` (MM) and `grep -cE 'UISpecialFrames|GameFont|"wipe"|"date"' .luacheckrc`
  (PC) print nothing or 0.
- For the PF list (`GetTime wipe Mixin UnitExists UnitGUID UnitIsUnit UnitIsDeadOrGhost UnitIsConnected C_Secrets RegisterUnitWatch UnregisterUnitWatch`)
  and the AT list (`C_Timer hooksecurefunc CreateColor PlaySound strsplit strtrim tinsert tremove`),
  `git grep -nw <g>` over the authored tree finds only comments or `mocks.X` accesses.
- WG `tests/test_lintconfig.lua` "exclude_files carries the template's frozen stores" and "read_globals
  grants no removed or unread global" are green.
- As a red proof, a scratch `local x = GetSpellInfo` warns in MM.

**Non-goals.** Tightening other luacheck options.

## C26 — Degradation stubs: library copies and surface parity

**Target.** Every library-absent stub completes the runtime without copying library formatters or
composers (anti-pattern #73). Options stub composers answer `{}`. Stubs never overwrite a real host
function: WG-09 keeps the host's `RestoreAllDefaults`. Stubs are edge-triggered wherever the library is
(AM-05). Every Schema stub carries the minor-2 surface: `SetMany` (all-or-nothing, log-silent), `normalize`,
`instanceId` forwarding, and the `writeThrough` store where the addon takes route (a).

On a library-absent load, each addon's composed-row verbs follow its declared WS-02 route:

| Route | Addons and paths |
|---|---|
| (a) `writeThrough` | AT `{enabled, locked}` (AT-08), AM `{enabled, locked}` in its own seam and the instance (AM-16), BL `{settings.enabled}` (BL-10), KC `{enabled, locked}` (KC-18/KC-19), LH `{settings.enabled}` (LH-15/LH-16), MM `{enabled}` (MM-15), PF `{enabled, locked}` (PF-11), PM `{settings.enabled}` (PM-09) |
| (b) library-absent line | WG enable/disable/test (WG-12, owner ruling), CM enable/disable/bar/lock/unlock (CM-18), PM lock/unlock (PM-09), and any other composed-row verb in the route-(a) addons |

A route-(b) choice for `enable`/`disable` is recorded as a SHOULD deviation row keyed options-ui-§1 (WG-12,
CM-18). Every seam with a stub has a testing-§8 surface-parity case: AT-14 (Perf, Lifecycle), LH-22 (Env,
Item, Media, Pool, Lifecycle), PM-13 (Lifecycle), WG-14 (Launcher, Lifecycle), plus the Schema
instance-vs-stub pairs in the adopters. Degraded row counts are pinned as full, degraded and named-gap
figures (BL-14, AT-08, AM-16). Degraded debug formatters carry no library format string (LH-20).
PrettyChat's `/pc test` falls back to chat when DebugLog is absent (PC-08).

**Acceptance.**
- In every addon, `tests/test_surface_parity.lua` is green, and each new parity case goes red when one
  member is deleted from its stub. The mutation is recorded in the commit body.
- In every route-(a) addon, a headless degraded-load case shows `pcall(<Slash>.OnSlash, …, 'disable')`
  returning ok, the stored `enabled` path false, the lifecycle latch down, and exactly one set-shape echo.
  `'enable'` reverses it. A row-less path not in the list is refused and not stored.
- In every route-(b) addon or verb, a headless degraded-load case shows `pcall` ok, exactly one line
  `<verb> is unavailable: the LibKa0s library did not load.`, and an unchanged store.
- `git grep -n 'composeBlock\|ORDER_STEP' -- settings` (AT) and `grep -n 'composeBlock' settings/OptionsSetup.lua`
  (AM) are empty. `grep -n 'cff6f8faf\|cffc9a66b' core/DebugLogSetup.lua tests/test_debuglog.lua` (LH) is
  empty.
- BL "schema: the live and library-absent row counts, and the composed delta" asserts 16/8 and 17/9.
- In client, on a copy with `libs/LibKa0s` renamed: `/<slash> disable` then `/<slash> enable` behave per
  the addon's route, with no Lua error (BugSack clean).

**Non-goals.** Host copies of composers to make a degraded build feature-complete. The AbsorbTracker A1
alternative (composers in a unit that loads without Options) is declined. PrettyChat's degraded
MasterControls stub, which emits leaves rather than `{}`, is not planned. It is noted for the next audit.

## C27 — Compat and deprecated API use

**Target.** Deprecated or version-variant client calls live only in `core/Compat.lua` behind a `C_*`-first
ladder, and dead fallback rungs are deleted rather than shimmed (WS-05):
- MM-04: chat export sends through `Compat.ChatSender` (`C_ChatInfo` first) and names a missing sender.
- CM-13: `GetItemInfo` goes through `KCM.Compat` (`C_Item` first), and the unread `subType` is dropped.
- AT-16, PC-15, LH-26: the dead `GetAddOnMetadata` global rung is deleted.
- AM-19: the pre-11.0 `GetMouseFocus` rung is deleted, and one enabled predicate remains.

AbsorbTracker and PrettyChat carry no `Compat.lua` and cite the applicability condition in their
compat-layer map row.

**Acceptance.**
- `grep -n 'SendChatMessage' modules/*.lua | grep -v '^\s*--'` (MM) is empty, and `grep -n 'ChatSender'
  core/Compat.lua modules/Export.lua` hits both.
- `! git grep -nE '(^|[^.A-Za-z_])GetItemInfo\(' -- modules settings core ':!core/Compat.lua'` (CM)
  succeeds.
- `git grep -n 'GetAddOnMetadata' -- core settings modules .luacheckrc | grep -v 'C_AddOns\|Env\.'` (AT,
  LH, PC) is empty, and the red-first "legacy-only surface yields nil" case is green.
- `grep -n 'GetMouseFocus()' core/Compat.lua` (AM) is empty, and `grep -n 'GetSetting("enabled") ~= false'
  core settings` (AM) has exactly one hit.
- In client: `/am pick` still resolves the frame under the cursor, and an MM export to PARTY arrives in
  party chat.

**Non-goals.** PanelMaster's `Compat.AddOnFolders` global rung. It is documented only (PM-20), and
deleting it is an owner call outside this plan.

## C28 — Combat-state detection and secure-frame writes

**Target.** Visibility decides from the combat edge, not from `InCombatLockdown()`, which is still false
at `PLAYER_REGEN_DISABLED`. LootHistory threads the event's truth into the gate (LH-05). PanelMaster does
the same, and its `Compat.InCombat` prefers `UnitAffectingCombat` (PM-03). Tests deliver events in the
client's order. PartyFrameEnhanced's secure-write memos compare against the requested value, so a change
reverted in combat is not lost (PF-03). Its holders and stand-in opt out of the layout cache with
`SetDontSavePosition(true)` (PF-16). ConsumableMaster's `FlushPending` replays the queued body through
`commitMacro`, so a combat-deferred weapon-enchant macro keeps `/use 16` and `/use 17` (CM-04).

**Acceptance.**
- These red-first cases are green:
  - LH `M.__fire("PLAYER_REGEN_DISABLED")` with `InCombatLockdown` false hides an `outOfCombat` window,
    with the mirror case for `inCombat`.
  - PM "leaving and entering combat both reach the renderer" delivers `OnRegenDisabled` with `__inCombat`
    still false.
  - PF "toggled back in combat" leaves `*type1 == 'target'` after `OnLeaveCombat`.
  - CM "FlushPending replays a per-hand weapon-enchant body".
- In client: with "Only out of combat", the LH window and PM panels hide on the first swing. PF
  `layout-local.txt` has no `PartyFrameEnhanced_*_Holder` entry. The CM `KCM_WPN_ENCH` body keeps both
  hand lines after `/cm rewritemacros` in combat.

**Non-goals.** A library-level combat-edge helper. The defect recurs in only two addons and stays local
(design decision (3)).

## C29 — WhatGroup popup combat taint and visibility

**Target.** Reopening a soft-hidden popup in combat with no capture never calls the secure teleport
button's protected `Hide` (a `NO_CAPTURE` sentinel, WG-03). `ApplyFrameAlpha` honors the soft-hidden
state, so a gate-declined or alpha-only reopen in combat does not reveal a popup that the launcher and
Escape cannot close (WG-04). Both paths are covered by `tests/test_frame_secure.lua`, a new sibling suite
created because `test_frame.lua` is at 1421 lines.

**Acceptance.**
- "frame: reopening a soft-hidden popup in combat with no capture never Hides the secure button" asserts
  `#mock.blocked == 0`.
- "a gate-declined reopen in combat leaves a soft-hidden popup at alpha 0, and the launcher still closes
  it" is green.
- `wc -l tests/test_frame.lua` is not above 1421.
- In client (S-001): Close in combat, wipe the capture, `/wg show` in combat. There is no
  `ADDON_ACTION_BLOCKED`, and after combat the popup shows "No data". With "Only out of combat", the
  popup stays invisible mid-fight and Escape opens the game menu after combat.

**Non-goals.** A redesign of the popup's show/hide model.

## C30 — Options reset semantics (options-ui-§12/§13)

**Target.** Every reset control has one declared scope, and destructive scope is confirmed:
- BL-05: Reset all settings, the page and footer Defaults and `/bl resetall` all raise the one confirm
  popup. Accepting it resets the profile and discards recorded history (the audit's Option A, flagged to
  the owner as a player-visible data-loss change), closes the debug console, turns test mode off and
  leaves a hidden minimap button hidden.
- BL-04: a reset while disabled re-enables the addon.
- LH-04: a shorter "Keep history for" asks before deleting records, and declining restores the previous
  retention.
- PC-06: the Categories page Defaults resets every category tab (option (a)), and General gains a Defaults
  button behind the reset-all path.
- CM-03: a color reset stores a copy, never the `dbDefaults` table.
- CM-11: one global reset act behind both doors, with the combat refusal inside `ResetAllToDefaults`.

**Acceptance.**
- These red-first cases are green:
  - BL "every reset control raises the one confirm popup and changes nothing before accept".
  - LH (a)–(e): `StaticPopup_Show('KA0S_LOOTHISTORY_PRUNE')` with `n=3`, accept deletes, decline
    restores 90.
  - PC "the Categories Defaults button resets every category, not only the selected tab", with exactly
    one `[Set] reset Categories:` line.
  - CM "resetting a color row stores a copy, not the dbDefaults table", and "/cm resetall confirmed in
    combat refuses and writes nothing".
- `! git grep -n 'KCM_RESET_ALL'` (CM) succeeds. `grep -n 'options-ui-§12' docs/ARCHITECTURE.md` (BL)
  shows no register row.
- In client: BL's four reset doors each show the one popup, and No leaves everything. LH 90→7 shows the
  count confirm.

**Non-goals.** Changing BankLedger's 30-day default retention (CP2 is not taken). Per-row reset UI.

## C31 — Printer pre-formatting and chat fallbacks

**Target.** Chat call sites hand arguments to the shared printer (events-frames-taint-§8) instead of
pre-formatting with `..` or `:format`, and the printed bytes stay the same. Debug calls pass a format and
raw values (debug-logging-§4, WG-16). Dead `DEFAULT_CHAT_FRAME` and `_G.print` fallbacks are gone
(AT-18, KC-21). The events-frames-taint-§8 register row counts are re-measured (AT-19). Items: AT-18,
AT-19, BL-17, KC-21, LH-25, WG-16.

**Acceptance.**
- `grep -nE 'print\(\("|print\(.*\):format' modules/LedgerTable.lua settings/Schema.lua settings/Slash.lua`
  (BL) is empty. `git grep -nE 'NS\.Print\(\("|NS\.Print\("[^"]*" *\.\.' -- core/DebugLogSetup.lua core/Lifecycle.lua settings/UnitPanel.lua`
  (AT) is empty. `grep -rn 'or _G.print' core modules settings` (KC) is empty.
- Characterization cases pin the exact rendered text before and after: LH `[LH] blacklist cleared (2 ids).`
  and `[LH] test mode on`, and WG's DebugLog buffer lines.

**Non-goals.** Rewording any player-visible line, except where BL-17 re-pins the LedgerTable pair and the
two "cleared" lines.

## C32 — Localization of player-visible strings

**Target.** Player-visible acknowledgements and errors route through `L` as whole sentences with
placeholders, and plurals use two distinct keys:
- MM-22: every user-facing line in `settings/Slash.lua`.
- AM-18: the library-missing lines are one sentence with a placeholder.
- PF-15: provider labels and DebugLog stub strings go through `NS.L`.

Confirmations use the set-shape echo: AM-12 (`enabled = false`, `locked = true`) and CM-10 (`/cm enable`
prints one line). Error sentences are right: MM-06 answers "No window named 'nope'." and has an empty-name
sentence. Dead or duplicate keys are removed (WG-19, PF-15). LibKa0s registers its font with a langmask
(LK-13).

**Acceptance.**
- These red-first cases are green: MM's spy-locale case (each verb reads its key, and the plural uses two
  keys), AM "no library-missing line joins a routed fragment", WG "every key enUS.lua defines has a
  reader", CM "/cm disable prints exactly one line, the enabled echo", AM "echo the stored value in the
  set shape", and LK-13's langmask and count cases.
- `grep -nE 'out\("[A-Za-z]' settings/Slash.lua` (MM) finds nothing outside the documented fallback.
  `grep -n 'Setting not found' modules/WindowManager.lua` (MM) is empty. `! git grep -n 'Master enable '
  -- settings tests` (CM) succeeds.

**Non-goals.** Adding a second locale.

## C33 — Hard-coded brand, folder names and non-catalog marks

**Target.** The brand string and addon folder name are typed once, at their single source. Every other
site reads that source:
- BL-18: `NS.BRAND_NAME`.
- AT-18: `C.BRAND`.
- CM-21, WG-17, PF-21: logo paths derive from the folder name.

Blizzard atlases and textures are used only where the LibKa0s catalog has no mark. KC-12's remove button
uses a catalog mark. LootHistory's Blizzard resize grabber stays, under a library-stack-§8 register row,
and the grip honors Lock frame (LH-10).

**Acceptance.**
- `grep -rn '"Ka0s Bank Ledger' core settings modules` (BL) hits only `LauncherSetup.lua:89` and
  `CoreSetup.lua:34`, and `git grep -n 'Ka0s Absorb Tracker"' -- core settings modules` (AT) hits only
  `core/Constants.lua`.
- CM "the About logo path follows the folder name" and WG "the landing logo path is built from the folder
  this copy loaded from" are green.
- `grep -n 'HookScript\|transmog-icon-remove' settings/Spells.lua` (KC) hits only the degraded atlas
  fallback.
- LH: with `locked=true`, the grip's `OnMouseDown` never calls `StartSizing`, and
  `grep -n 'library-stack-§8' docs/ARCHITECTURE.md` resolves.

**Non-goals.** Growing the LibKa0s icon catalog to replace Blizzard chrome.

## C34 — Message-bus literals and the no-bus ruling

**Target.** Tests send and subscribe bus messages through `NS.MSG` constants, and one oracle
(`test_bus.lua`) holds the wire names (BL-15, LH-23, CM-22). architecture-§4's threshold is stated
(WS-04): a shell plus one feature module is below it. WhatGroup's and PrettyChat's `## Message Bus`
sections cite it (WG-23, PC-12).

**Acceptance.**
- `grep -n '"Ka0s_' tests/*.lua` (BL) hits only `test_bus.lua:19-22` and the one scratch constant.
- `grep -rnE '(Send|Register)Message\("Ka0s_' --include='*.lua' . | grep -v '^./libs/\|^./tests/_kit/'`
  (LH) is empty.
- `test "$(git grep -o Ka0s_ConsumableMaster_HarnessPing -- tests | wc -l)" = 1` (CM) succeeds.
- `grep -n 'architecture-§4' docs/ARCHITECTURE.md` hits in WG and PC.

**Non-goals.** Adding a bus to WhatGroup or PrettyChat.

## C35 — Hot-path allocation, throttles and redundant work

**Target.** Hot paths allocate nothing per call and skip redundant work. Each change is gated on a
measurement where the item says so. LibKa0s changes:
- LK-19: the DebugLog trim is batched (at most one compaction per 64 lines; `D.buffer` stays a public
  ordered array).
- LK-20: Perf raw fields, and a leaked Open cannot parent a later window's bracket.
- LK-26: the Options slider and color throttles keep their own armed flag, so a nil-returning
  `scheduleTimer` still gets the 50 ms throttle.

Addon changes:
- KC-10: KickCD's `scheduleTimer` returns a real handle anyway.
- BL-13: module-level name lists.
- PF-18: a zero-overhead scenario pins capture-off against instrumentation absent.
- MM-08: `Visibility:Evaluate` runs only under debug.
- MM-20: Render keeps rows bound. It is **committed only if** the after-capture's render ms/call is lower,
  otherwise it is reverted.
- LH-08: `PruneOld` fires only when it removed rows.
- LH-18: one gate-config table is reused.
- LH-19: measure first, then memoize the AH tag parse.
- AT-05: POSITION/APPEARANCE/REPAINT are published once on an enable edge.
- PC-11: one memoized sorted name list.
- WG-15: the teleport button's script handlers are defined once.

**Acceptance.**
- LibKa0s `tests/test_options_throttle.lua`: ten `OnValueChanged` calls with a nil-returning
  `scheduleTimer` schedule exactly one timer. LK-19's 1564-add case costs at most one compaction, and
  every public reader answers 1500. `! grep -nE 'P\.(armed|recording|label) *= *nil' LibKa0s/Perf.lua`
  succeeds.
- These addon red-first cases are green:
  - BL "ApplyVisibility and ApplyMasterChrome build no table literal per call", with
    `grep -n 'pairs({' core/Util.lua` empty.
  - LH "the same table is passed both times (rawequal)" and "PruneOld over an all-fresh history gives
    count 0".
  - MM "a ZONE edge makes zero NS.ShouldShow calls" with debug off.
  - WG "reconfiguring the teleport button reuses the same three script handlers".
  - AT "an off-to-on switch publishes APPEARANCE once".
  - PC "SortedStringNames answers the same sorted table on every call".
- `$B lua5.1 tests/perf.lua` holds each item's stated figure: MM `refresh20x7` bytes/iter ≤ 303438.1 with
  8 API calls, and PF `probeOverheadOff` 0 bracket calls/iter.
- MM-20 carries before and after `docs/perf-analysis/<stamp>/` bundles, or it is absent.

**Non-goals.** Optimizing paths not named by a finding. A LibKa0s ring buffer, since `D.buffer` stays an
array. Changing `MAX_BUFFER`.

## C36 — Test-only exports and dead code on the production namespace

**Target.** Production modules publish nothing that only tests read (AT-13 deletes `NS.bar`,
`statusBar`, `valueText`, `backdropInfo`), and they write no field that nothing reads (WG-17's category
handles). There is one predicate or flow per concern:
- KC-09: `NS.MasterEnabled`.
- AM-20: `NS.FramePicker.PickFor` owns resolve, combat refusal and the two writes.
- AM-19: one enabled predicate.

Defaults are declared once (PC-14: `NS.GlobalDefaults`, `NS.GeneralDefaults`). A duplicated host tab
strip and its wrap-invariance cases are gone where the library draws the strip (CM-20 adopts
`RenderTabbedSchema` `opts.tabs` on General and Macro Bar, deletes `GENERAL_TABS`, and files a
`will-not-do` decline for Stat Priority and Macros).

**Acceptance.**
- `git grep -nE 'NS\.(bar|statusBar|valueText|backdropInfo)([^A-Za-z0-9_s]|$)' -- core modules settings tests ':!tests/_kit'`
  (AT) is empty.
- KC "module readers answer what NS.MasterEnabled answers" and "no module reads profile.enabled directly"
  are green.
- `grep -n 'container.attach.frame' settings/Slash.lua settings/Layout.lua` (AM) is empty.
- `! git grep -n GENERAL_TABS -- core settings tests` (CM) succeeds, and CM's characterization of tab keys
  and rendered rows is green before and after.
- PC `tests/test_database.lua` reads `NS.GlobalDefaults.schemaVersion == 0`.

**Non-goals.** Deleting test seams that production also reads.

## C37 — Vacuous assertions and missing invariant tests

**Target.** Every assertion can fail:
- No test asserts `nil == nil` against a removed key (AT-02).
- `assertError` calls assert on the raised text (LK-02 adds `Kit.assertErrorMatches` and rewrites the 23
  LibKa0s sites).
- Disabled suites have no `or true` assertions (CM-12).
- A raising `OnInitialize` fails `T.load` (KC-02).
- Addons stop re-testing library internals (LH-20).
- A lone CR can no longer hide a file from EOL normalization (LK-06, AM-01).

A library-drawn strip's wrap invariance is pinned by the library (WS-06 (3)). A host-drawn strip is
pinned by the host (AT-15 evaluates `RenderTabbedSchema` for the Appearance page: it adopts, or files a
`state:triaged` decline, and the characterization is green either way).

**Acceptance.**
- `! grep -nE '^\s*(T\.|Kit\.)?assertError\(' tests/*.lua` (LibKa0s) succeeds.
- These mutation checks hold:
  - AT: deleting `NS.ResetProfileCounted(db)` from `new` reddens the rewritten case.
  - CM: making `__fireUnconditional` answer 0 reddens `:292`, and `! grep -nE 'or true,|truthy\(true' tests/test_disabled.lua`
    succeeds.
  - KC: "a raising OnInitialize fails T.load instead of passing silently" is green.
- `perl -ne '$c += () = /\r(?!\n)/g; END{print $c+0}' tests/page_helpers.lua` (AM) prints 0, and LibKa0s
  `tests/test_kit_eol.lua`'s `\r\r\n` fixture fails with path:line.
- AT: either `git grep -n 'partitionTabs' -- settings tests` is empty (adopted), or
  `gh issue list -R tusharsaxena/AbsorbTracker --search 'RenderTabbedSchema'` shows the decline.

**Non-goals.** Raising coverage for its own sake.

## C38 — LibKa0s library defects

**Target.** The library's own correctness bugs are fixed in v1.56.0:
- LK-12: `QualityFromLink` parses `|cnIQ<n>`, and an empty quality map is retried.
- LK-27: PageBanner, PageHeader and the chrome divider stop leaking a widget per render, and the kit's
  AceGUI fake surveys Create/Release.
- LK-14: Bus re-stamps its wrappers after a newer AceEvent re-embed.
- LK-10: `printer.Format` survives a secret value.
- LK-21: `ReorderList` no longer hijacks pooled frames.
- LK-22: Schema forwards `instanceId`.
- LK-15: Lifecycle re-entrancy is documented and pinned.

Consumers observe the fixes after re-vendor: BL-DOCS and LH-21 via the cold-cache epic smoke, CM-29,
KC-12 and MM-18 via the ReorderList drag smoke.

**Acceptance.**
- LibKa0s red-first cases are green:
  - `'|cnIQ4:|Hitem:19019::::::::60:::::|h[Thunderfury]|h|r'` answers 4, and `|cnIQ0` answers 0.
  - "after two full renders of a banner page, `M.__aceguiLive('Dropdown') == 1`".
  - The Bus re-embed simulation leaves no registration after StandDown, and the debug seam reports
    `restamped = 1`.
  - `printer.Format('%d rows', <secret>)` emits a line and does not raise.
  - "a host OnUpdate on a row frame survives a drag".
  - "Get passes instanceId to row.get".
  - The Lifecycle nested-edge characterization.
- LH "the uncached resolver answers quality 4 for EPIC_LINK with no palette" is red under a v1.55.0
  payload and green under v1.56.0.
- In client: an uncached epic records with epic quality in BL and LH. Dragging a ReorderList row in CM,
  KC and MM draws the drop line in the list's own color, and Esc mid-drag leaves no stray line.

**Non-goals.** Changing `LoadItem`'s fixed 0.4 s timer. It is byte-identical in both hosts, and the Item
version-2 doc says so. A metatable proxy or an Ace3 fork for the Bus fix.

## C39 — KickCD Spells page and icon grid

**Target.**
- The Spells page hooks no pooled AceGUI frame, and its tooltips work without leaking (KC-12).
- One commit renders the page once, and a raise in the render cannot latch the guard (KC-11).
- `core/SpellInput.lua` is the one resolver. It gates the CLI on the Cooldown Manager, accepts
  multi-word names, validates class and spec, and invalidates its cache through AceEvent (KC-06).
- `GateHint` asks `valuesFor` instead of writing the live profile (KC-16).
- Empowered casts are tracked, with one cast filter per (module, unit) (KC-05).
- A rebuilt icon is seeded from Cooldowns' current state, not painted ready (KC-08).

**Acceptance.**
- These red-first cases are green:
  - "`/kcd spells add Wind Shear` adds 57994 for a Shaman" and "`spells add <id> WARLORD 99999` writes
    nothing".
  - "no Spells row widget hooks its pooled frame".
  - "one commitSoon flush renders the Spells page once" and "a raising render does not latch the guard".
  - "GateHint never writes the profile when the row declares valuesFor".
  - "an icon rebuilt after Cooldowns already emitted keeps its cooldown".
  - "two disable/enable cycles create no frames".
- `wc -l settings/Spells.lua core/SpellInput.lua` each under 1500, with `ParseTail` at CCN 15 or below.
- In client (as a Shaman): the Wind Shear add works, a non-CM spell prints the Cooldown Manager line, an
  interrupt on cooldown keeps its swipe across a talent swap, and an empowered cast drives the bar (or is
  recorded as untested if no Evoker is available).

**Non-goals.** Redesigning the Spells page layout. Renaming the `spells enable|disable` sub-verbs, which
WS-06 (1) sanctions under the noun's sub-tree.

## C40 — LootHistory capture and export correctness

**Target.**
- The Mythic+ keystone context clears on leaving the party instance or a key reset (LH-01).
- The encounter context survives a grace window after a successful `ENCOUNTER_END`, so boss-corpse loot
  carries `encounterID`, and a wipe clears it at once (LH-02).
- The currency-category cache rebuilds once per missed id (LH-03).
- The warbound repair warms the cache from the link (LH-06).
- `Database:Export` deep-copies `auctionPrice` and `sourceDetail` (LH-07).
- Both CSV exports use one bind-state vocabulary, `Not Bound` (LH-09).
- The resize grip honors Lock frame (LH-10).

**Acceptance.**
- These red-first cases are green: LH-01's five cases, LH-02's (a)–(c), LH-03's frozen-snapshot case with
  exactly one extra walk, "the spy saw 258586", "the live row still reads 100 and 1",
  `'A-Realm / Not Bound'`, and the grip case.
- `grep -n 'Soulbound\|Warbound (UE)' modules/Export.lua` is empty.
- `wc -l modules/Attribution.lua core/Compat.lua` each under 1500, and `Export E` stays at CCN 15 or
  below.
- In client: S-001 (MPLUS then CONTAINER after leaving, with the "keystone cleared" debug line), S-002
  (encounter end before `LOOT_OPENED`, and `sourceDetail.encounterID` present), S-003, S-007 and S-008.1.

**Non-goals.** PrettyChat handoff H-1, the rebuilding of loot and currency patterns when the source
globals change. It belongs to LootHistory's issue store and is not built here (C43 documents PrettyChat's
side).

## C41 — MultiMeters window rows and drill-down

**Target.** "Always show yourself" pins the player into the rows the window actually draws, including the
default `maxRows=0` profile, and it is scroll-aware (MM-03). Renaming a window no longer closes its
drill-down. A copy still closes it (MM-05).

**Acceptance.**
- `tests/test_window.lua` (a)–(c): the player at rank 15 of 20 is the 10th drawn row with rank argument
  15. With `scrollOffset=6` there is no pin. With `alwaysShowSelf=false`, row 10 is rank 10.
- `tests/test_drilldown.lua` "Rename keeps the view open" and "CopyFrom still closes it" are green.
- `lizard modules/Window.lua | grep Render` shows CCN ≤ 14. `refresh20x7` keeps 8 API calls/iter and
  bytes/iter ≤ 303438.1.
- In client: SM-04 and SM-10 hold.

**Non-goals.** Changing how many rows the default window draws.

## C42 — PanelMaster panel geometry and frame naming

**Target.**
- `/pm recover` bounds offsets in the panel's scaled space, using one `Util.EffectiveScale` shared with
  the renderer (PM-04).
- `RenderAll` releases every mismatched frame before rendering, so a profile swap of frame names never
  creates a duplicate named frame (PM-05).
- The per-panel Unlock tick shows the real state, including after an in-combat queue (PM-06, issue #47's
  state bug).
- `C.MAX_GRID` is 64, matching the slider (PM-07).

**Acceptance.**
- These red-first cases are green:
  - "at an effective scale of 0.5 a visible TOPLEFT panel at 1.5 × screen width is left alone", and the
    scale-2 mirror.
  - "swapping frame names across ids creates no second named frame" (six switches).
  - The Unlock tick (a) and (b).
  - "the grid-size slider and the write seam share one maximum".
- `wc -l settings/PanelEditor.lua` ≤ 1488.
- In client: §10 at Master scale 0.5 and 2, `/pm debug dump` reports `0 orphaned` after five swaps, and
  §9's Unlock box shows ticked and greyed while globally unlocked.

**Non-goals.** Splitting `settings/PanelEditor.lua` (open issue #47's split half).

## C43 — PrettyChat format overrides and cross-addon interaction

**Target.**
- No Blizzard global is registered under two categories. The dead Loot copies of
  `LOOT_ITEM_CREATED_SELF/_MULTIPLE` are dropped, and an idempotent v2 profile migration moves any stored
  Loot override onto Tradeskill (PC-04, which also resolves PrettyChat#4).
- `NS.OriginalFormat` answers the snapshot's nil for a global the client never defined (PC-07).
- The New box hands `Schema.Set` exactly `(path, value)` (PC-09).
- The authored generator lives at `tools/split_globalstrings.py`, repo-root relative, and `tools/` is
  packaged out (PC-19).
- PrettyChat documents that it rewrites the loot, currency and money chat globals for every addon
  (handoff H-1), with smoke step SMK-F001 (PC-22).

**Acceptance.**
- These red-first cases are green: "no Blizzard global is registered under two categories",
  "OriginalFormat answers nil for a global the client never defined, even after ApplyStrings", and "the
  New box hands Schema.Set exactly (path, value)" (2 arguments).
- `python3 tools/split_globalstrings.py && test -z "$(git status --porcelain GlobalStrings/)"` succeeds.
- `grep -n 'H-1' docs/ARCHITECTURE.md docs/scope.md docs/smoke-tests.md` and
  `grep -n 'SMK-F001' docs/smoke-tests.md` hit.
- In client: after `/reload` with an old SV holding a Loot-only override, the override now applies under
  Tradeskill.

**Non-goals.** Changing LootHistory from PrettyChat's side. If LootHistory's plan did not pick up H-1, the
fix is a LootHistory issue citing F-001.

## C44 — PartyFrameEnhanced third-party SavedVariables and packaging

**Target.**
- PartyFrameEnhanced keeps the `EllesmereUIDB` read that sizes its stand-in, under a library-stack-§6
  register row (option (b)), and `docs/scope.md` says so truthfully (PF-22). The item spells out option
  (a) for the owner.
- The package ships no screenshots. The screenshot files are renamed to `partyframeenhanced.*`, and the
  phantom `.claude`/`.superpowers` ignores are dropped (PF-17).
- AuraMaster's `.pkgmeta` stops ignoring a `.claude` directory that does not exist (AM-28).

**Acceptance.**
- `grep -n 'media/screenshots' .pkgmeta` (PF) hits once. `! grep -n '\.claude\|\.superpowers' .pkgmeta`
  (PF) succeeds. `ls media/screenshots` shows only `partyframeenhanced.*`.
  `grep -rn 'partframe' --exclude-dir=.git --exclude-dir=libs --exclude-dir=audits --exclude-dir=reviews --exclude-dir=automated-tests .`
  prints nothing.
- In AM, `for p in $(grep -E '^\s*- ' .pkgmeta | sed -E 's/^\s*- ([^ #]+).*/\1/'); do [ -e "$p" ] || echo FALSE CLAIM $p; done`
  prints nothing.
- `grep -n 'EllesmereUIDB\|saved settings' docs/scope.md` (PF) hits.

**Non-goals.** Removing the EllesmereUIDB read (option (a)) unless the owner picks it at execution time.

## C45 — AuraMaster container frames and host re-implementations

**Target.** A container id that returns out of combat revives its destroyed instance instead of building a
second `AuraMasterAnchor<id>` frame set (AM-03). AuraMaster's host tab renderer and header fork are
deleted. All seven pages render through `O.RenderTabbedSchema` with `opts.tabs`,
`disabledFor`/`disabledNotice` and `chrome`, and the Containers band uses `O.PageBanner`'s `action` for
the picker+create band (AM-17, on LK-28). Under LK-28's shape, `disabledFor` answering true draws the
`disabledNotice` above the rows and renders the rows disabled rather than replacing them, and a `tabs`
entry whose key equals a schema group takes that group's place in the strip and is handed the group's
rows. So AM-17 adopts with no change to its disabled-state characterization.

**Acceptance.**
- `tests/test_containermanager.lua` "an id that returns out of combat revives its destroyed instance":
  `spyCreate(mocks,'AuraMasterAnchor3')` counts 0, and `CM.instances[3]` is the same table.
- `grep -nE 'collectTabs|settleActiveTab|renderActiveTab|RenderTabbedPage|buildContainerHeader|__bannerWidget\s*=' settings/`
  is empty. The seven-page characterization (tab keys and labels in order, active-tab heal, disabled
  notice, Filters warnings, empty-registry line, Containers band) is green before and after.
  `wc -l settings/OptionsSetup.lua` shrinks.
- In client: an A → B → A profile switch ten times leaves one `AuraMasterAnchor5` with the same table
  address. Every page draws its strip. Bars on an icons container shows the muted-red notice.

**Non-goals.** A local fork of `RenderTabbedSchema`. If the v1.56.0 Options doc contradicts AM-17's
mapping, the item stops and the gap goes upstream.

## C46 — WhatGroup LFG status, and the minimap row path across the collection

**Target.**
- **LFG status.** A WhatGroup capture ends on the terminal LFG statuses `timedout`, `invitedeclined` and
  `failed` (WG-07). The exact `newStatus` strings are recorded from an `/etrace` capture before coding.
- **Minimap path rename (WS-06, launcher-§3).** In every one of the eleven addons, the minimap row's
  schema and CLI path reads in the row's own shown sense, `<root>.minimap.shown` (for example
  `global.minimap.shown`; `minimap.shown` in BL and LH). The row's get and set closures invert onto
  LibDBIcon's stored `minimap.hide`. `/<slash> get <root>.minimap.shown` answers true while the button is
  visible, and the old `…minimap.hide` path answers the unknown-setting refusal. Reset all settings and
  page Defaults leave a hidden button hidden. Items: AT-12, AM-14, BL-12, CM-19, KC-17, LH-13, MM-16,
  PC-13, PF-13, PM-11, WG-11.
- **SavedVariables continuity.** Every existing player keeps their minimap setting. The stored key does
  not move, so `hide = true` carries over by itself. **No stored `shown` key may exist** (anti-pattern
  #81). No addon ships a SavedVariables migration step for the rename, and no addon bumps its schema
  version or `CURRENT_DB_VERSION` for it. Instead, all eleven rename items carry the same test-first
  carry-over check (the acceptance criterion below). If the MultiMeters implementer finds a path string
  persisted in SavedVariables (a saved reset-exempt list, a bookmark or similar), they stop and raise it
  with the owner; this plan adds no migration for it (MM-16).
- Each addon's commit body records the player-facing macro change:
  `/<slash> set …minimap.hide` becomes `/<slash> set …minimap.shown <inverted>`, and the old path answers
  the unknown-setting refusal.

**Acceptance.**
- WG `tests/test_capture.lua` has one red-first case per terminal status, and the accept then finds no
  capture.
- In every addon, a red-first case shows `get <root>.minimap.shown` true while `hide == false`, and
  `set … false` storing `hide = true` with the button hidden and `shown == nil` in the raw SV. The old path
  is unknown (`FindRow('…minimap.hide') == nil`, or "Setting not found"). A reset-survival case shows a
  hidden button staying hidden through Reset all settings.
- In every addon,
  `git grep -n 'minimap\.hide' -- ':!libs' ':!tests/_kit' ':!docs/audits' ':!docs/reviews' ':!docs/automated-tests' ':!docs/revendor' ':!docs/superpowers'`
  hits only storage reads and writes, the store-path constant and docs that name the storage key.
  `grep -rn 'minimap\.shown\s*=' core defaults settings modules` finds no stored-key write.
- **Carry-over, test-first, in all eleven addons** (AT-12, AM-14, BL-12, CM-19, KC-17, LH-13, MM-16,
  PC-13, PF-13, PM-11, WG-11). Written before the rename (it reads the new path, so it is red until the
  rename lands): a legacy store with `minimap = { hide = true, minimapPos = 200 }` reads
  `<slash> get <root>.minimap.shown` as false, the button stays hidden, `minimapPos` is untouched, and no
  `shown` key is ever written to the raw SV after a set. MultiMeters also runs the same shape through its
  existing runner from a pre-v15 `profile.minimap.hide = true` (MM-16 (f), seeded at `schemaVersion` 14).
- In client, per addon: on an account whose button was hidden before the upgrade, log in on the new
  build. The button stays hidden, `/<slash> get <root>.minimap.shown` prints false, and after logout the
  SV file shows `minimap.hide = true` and no `shown` key (LH also `/dump LootHistoryDB.global.minimap`).
  Setting it true brings the button back at its old dragged position.

**Non-goals.** Moving the stored key off `minimap.hide`. Keeping `…minimap.hide` as an alias path. A
SavedVariables migration step or a schema-version bump for the rename, in any addon. A version bump: the
rename commences at each addon's next release, which the owner cuts.

## C47 — Standard text conflicts and tooling baseline (upstream)

**Target.** The upstream observations are ruled and the tooling works:
- The lock-is-preview shape ships no `test` verb, and a one-shot value hold lives at
  `/<slash> debug hold` (WS-06 (2); AbsorbTracker AT-11 applies it).
- debug-logging-§1 says 1500 lines (WS-07).
- Reserved verbs may be reused inside a noun's sub-tree (WS-06 (1); KickCD's ruling is recorded in
  `docs/`, KC-25).
- `CreateOptionsPanel` parks and replays in combat (LK-25), and ConsumableMaster adopts it, deleting its
  host park (CM-05).
- `ka0s-bounded` is on PATH (WA-02).
- The review brief's baseline is re-measured and derived at run time (WA-03).

**Acceptance.**
- WS-06's and WS-07's verify greps hit. `! grep -n '\b500\b' standards/standards/debug-logging.md`
  succeeds.
- LibKa0s `tests/test_options_combat.lua`: in combat, `CreateOptionsPanel` registers nothing and arms
  `REGEN_ENABLED`, then registers exactly once on the event. `OpenOptionsPanel` returns false in combat
  and true out of it.
- `command -v ka0s-bounded` resolves after a plugin reload, and `grep -n 'majors.lua' agents/review.md`
  hits.
- A flag for the owner is recorded in WhatGroup's plan notes: parking registration in combat sits
  uneasily with options-ui-§9's "category registration never taints". WG-02 follows the library, and the
  standard may want a sentence.

**Non-goals.** Changing options-ui-§9 in this cycle.

---

# Part D — the owner-scope enhancement issues

`OWNER_SCOPE.md` binds twelve enhancement issues to this cycle. Each one is closed by the item named, and
its GitHub state ends as CLOSED with `state:done`, applied after the owner merges, with each `gh` write
spaced at least 5 s apart. The commit body carries `Closes #N` or `Fixes #N`. The seven closed
`state:will-not-do` issues stay declined, and **no code is written for them**: AbsorbTracker #31,
AuraMaster #20, BankLedger #20, PanelMaster #53, PrettyChat #16 and #17, and WhatGroup #21.

**Acceptance common to all twelve.** `gh issue view <N> -R tusharsaxena/<Repo> --json state,labels` shows
CLOSED with `state:done`. The addon's SG is green at the closing commit. For the seven declined issues,
`gh issue view <N> -R tusharsaxena/<Repo> --json state,labels` still shows CLOSED with `state:will-not-do`.

## D1 — WhatGroup #22: adopt LibKa0s-Schema-1.0 (WG-12, with WS-02, LK-18, LK-23)

**Target.** WhatGroup's settings seam is a `LibKa0s-Schema-1.0` instance published as `NS.SchemaRuntime`.
`settings/SchemaSetup.lua` loads directly above `settings\Schema.lua` under a load-bearing comment and
resolves the library, or else a `HostSchemaStub` copied from LibKa0s's `referenceStub` at v1.56.0 and
trimmed to what WhatGroup calls. The host copies are deleted: `Helpers.RawSet`, `Resolve`, the
SESSION/GLOBAL dispatch, the bulk state, `sameValue`, `FindSchema`, `countChangedProfileRows` and
`pendingResetCount`. The descriptors bind `S.Get/Set/FindRow/ApplyDefault` and the bracket, so Slash
minor 15's `CliSet` prints the seam's refusal. **No `writeThrough` list is passed.** Under the owner's
ruling this is WS-02 route (b), accepted as a known gap.

**The owner's ruling, stated exactly.** In a library-less (degraded) build, the affected verbs
(`/wg enable`, `/wg disable`, `/wg test`, `/wg test on`, `/wg test off`) print a chat message that names
the verb and says it needs LibKa0s, and they raise no Lua error. The message is
`<verb> is unavailable: the LibKa0s library did not load.`, routed through `L` as one sentence with one
placeholder. They write nothing and acknowledge nothing. This is pinned by a headless test that loads the
addon without LibKa0s.

The deviation is recorded as a Documented deviations row keyed `options-ui-§1`. It states what differs,
why ("the owner's ruling on WhatGroup#22 (2026-09-23), accepted as a known gap; composers stay hollow and
no host copy is written (#73)"), the decision date, and its re-check trigger (a report of a
library-absent install that needs the switch, options-ui-§1 raising (a) to a MUST, or the owner reopening
#22).

**Acceptance.**
- The headless degraded-load cases in `tests/test_libka0s.lua` (the `NO_LIBKA0S` load, where LibKa0s
  never loads) are green:
  - "degraded: `/wg disable` and `/wg enable` print the library-absent line and write nothing
    (options-ui-§1, WhatGroup#22)". `pcall(OnSlashCommand, 'disable')` is ok, the last print ends with
    `/wg disable is unavailable: the LibKa0s library did not load.`, and `db.profile.enabled` is still
    true. The same holds for `enable`.
  - "degraded: `/wg test on|off` print the library-absent line and move nothing". The line names
    `/wg test`, `NS.State.testMode` is not true, and the popup was not built.

  Both were red on the pre-adoption seam, where `RawSet` wrote the row-less path.
- After the swap, exactly the eight re-pins the Schema doc's Adoption notes sanction are made, each with a
  comment naming its bullet. A ninth red is a defect.
- Parity: `T.assertSurfaceParity(live.SchemaRuntime, degraded.SchemaRuntime, 'schema instance vs host stub')`
  and `T.assertSurfaceParity(degraded.addon.Settings.SchemaLib, 'LibKa0s-Schema-1.0', { 'STRINGS' })` are
  green. `tests/run.lua`'s surface-source map names `LibKa0s-Schema-1.0`.
- `! grep -nE 'RawSet|skipOnChange|skipRefresh|bulkDepth|local function Resolve' settings/*.lua` succeeds,
  and `grep -n 'SchemaSetup' WhatGroup.toc` hits.
- `grep -n '^| \`options-ui-§1\`' docs/ARCHITECTURE.md` hits the new row. `grep -rn 'did not load' locales/enUS.lua`
  hits the one key.
- In client, library-present: `/wg disable`, `/wg enable`, `/wg test on|off`, the Master controls
  checkboxes and `/wg set notify.delay 3` behave as before, with one `[Set]` line per write under
  `/wg debug on`. Library-absent (`libs/LibKa0s` renamed): `/wg disable` and `/wg test on` each print the
  line with no Lua error.

**Non-goals.** Making the degraded `enable`/`disable` work (route (a)). Adopting `writeThrough` in
WhatGroup. Any host copy of a composer.

## D2 — PartyFrameEnhanced #14: adopt Schema once a library-less build can write its composed rows (PF-11, with WS-02, LK-23)

**Target.** The rolled-back adoption is re-applied **on top of the Schema `writeThrough` surface (LK-23)**,
which is WS-02 route (a). The `settings/Schema.lua` setup resolves `LibKa0s-Schema-1.0` minor 2, or else a
`HostSchemaStub` from the version-2 doc's "The degradation stub". The stub carries `SetMany` and honors
`row.normalize`. Both the instance and the stub receive `writeThrough = { 'enabled', 'locked' }`, which
covers every path the degraded build writes without a row:
- `settings/Slash.lua` runEnabled: `NS.SetByPath("enabled", on)`;
- runLock: `NS.SetByPath("locked", locked)`;
- `modules/Preview.lua` forceLock: the combat, master-switch and perf re-lock.

The stub stores a listed row-less path as a copy and refuses every other row-less path. The host
registries, `byPath`, the bracket and `SetSetting` are deleted. `NS.SetByPath = inst.Set`. `AcceptLock`
stays in `row.validate`, and the Slash descriptor's `set` still returns nothing, so the refusal line is not
printed twice. `NS.__schema`/`NS.__schemaLib` are published for parity. Known Limitations records that
on a library-less build `/pfe enable|disable|lock|unlock` store the switch without the row's `onChange`,
which is unchanged from today.

**Acceptance.**
- The degraded-build write tests in `tests/test_schema.lua` are green on the adopted seam:
  - `:209` "without the library, /pfe disable and /pfe enable still write the stored path";
  - the new degraded `/pfe lock` and `/pfe unlock` cases writing `locked`;
  - a degraded write to a row-less path not in `writeThrough` (`'general.__nope'`), which is refused and
    not stored.
- The deliberate deltas are re-pinned per the Adoption notes: an unknown path is refused on the live
  build, table values are copied, and there is no `'%s refused'` line.
- `T.assertSurfaceParity(NS.__schema, NS2.__schema, 'schema instance vs host stub')` and
  `T.assertSurfaceParity(NS2.__schemaLib, 'LibKa0s-Schema-1.0', { 'STRINGS' })` are green.
- `grep -n 'local byPath\|RegisterSessionSetting\|RegisterGlobalSetting' settings/` is empty. `tests/perf.lua`
  keeps `resolveUnchanged` at 0.0 B/iter.
- In client, library-absent (`libs/LibKa0s` renamed): `/pfe disable`, then `/reload`, keeps the addon
  disabled, and `/pfe enable` restores it, with no Lua error.

**Non-goals.** Running the row's `onChange` on the degraded path. Adopting Launcher minor 2's gate in
PartyFrameEnhanced.

## D3 — AuraMaster #21: adopt Schema primitives, registry, bulk bracket and validation (AM-15)

**Target.** On the live path, the primitives (`SplitPath`/`Read`/`Write`), the registry
(`FindRow`/`AddRows`/`Reindex`), the bracket (`BulkBegin/End/Run/Add/InBulk`), `SameValue` and `Validate`
are the library's. The host bodies stay only as the library-absent arm. `NS.SetByPath` is **kept**, and
`S.Set` is not adopted. The re-evaluation that #21's triggers required is recorded in `docs/schema.md`
("Write seam: why AuraMaster keeps SetByPath"), with its re-check trigger. The degraded `enable`,
`disable` and `lock` still write through a declared data-only `writeThrough` list (AM-16).

**Acceptance.**
- "schema: with LibKa0s the bracket, registry and validator are the library's"
  (`NS.Bulk.Begin == S.BulkBegin`, and `FindSchemaRow == S.FindRow` for every row) is green, and red under
  the host copies.
- "schema: without LibKa0s the host arm still answers" is green. "-0 over 0 is still no change under
  SameValue" is green. `NS.ValidateSchema() == 0`.
- The existing seam suites stay green apart from the JC-9 re-pins.
- `wc -l settings/Schema.lua` ≤ 1500. The write-seam perf scenario shows no bytes/iter rise.
- `gh issue view 21 -R tusharsaxena/AuraMaster` carries the decision comment and `state:done`.

**Non-goals.** Adopting `S.Set` (declined, with a stated trigger).

## D4 — AuraMaster #16–#19: the layout-§1 peels (AM-23, AM-24, AM-25, AM-26)

**Target.**
- #16: Dispel Colors moves whole into `settings/GeneralDispel.lua`, which loads after `GeneralSpells` and
  before `General` under the amended LOAD-BEARING comment. `BULLET`/`BULLET_GAP` are published once and
  not copied.
- #17: user-category suites move from `tests/test_database.lua` to `tests/test_database_categories.lua`.
- #18: user-category suites move from `tests/test_filtercompiler.lua` to a sibling.
- #19: category-editing suites move from `tests/test_pages_general.lua` to
  `tests/test_pages_general_categories.lua`, with shared helpers in `tests/general_page_helpers.lua`.

Each peel deletes its own census and register row. After #19 the census heading stays with the preamble
"No authored file is over the cap" and no table (or a header-only table).

**Acceptance.**
- `git ls-files '*.lua' | grep -v -e '^libs/' -e '^tests/_kit/' | xargs wc -l | awk '$2!="total" && $1>1500'`
  is **empty**.
- Totals and case names are unchanged across #17–#19 (`--list | sort` is identical apart from suite
  grouping). The General → Dispel Colors cases and the load-order case are green.
- The kit's `test_layout_cap` is green with no census row naming a file under the cap.
- In client: Dispel Colors draws its lead-in, four bullets and five swatches, and a swatch recolors a
  dispel-typed bar.

**Non-goals.** Behavior changes inside a peel.

## D5 — ConsumableMaster #39: adopt Schema for the settings write seam (CM-17, on LK-22, LK-17)

**Target.** The settings seam is a `LibKa0s-Schema-1.0` minor-2 instance (`Helpers.schema`), or else
`KCM.SchemaStub` (`settings/SchemaStub.lua`, loaded immediately before `settings\OptionsSetup.lua`,
write-completing and log-silent, with an empty `writeThrough`). Type rules split into `validate` and
`normalize`: a number clamps in normalize, and table types copy. Host reactions ride a host `apply` field
run by `announce`/`announceBatch` through the existing pcall reporter, so a page reset is still one
`applyBar`. The diversions become rows (`state.debugConsole` session-only, and the minimap row with its
get/set). `SESSION_PATHS`, `GLOBAL_PATHS`, `divertedPath`, `Helpers.Resolve`, `sameValue` and the bulk
frame chain are deleted. The Slash descriptor's `set = S.Set`, so LK-17's `CliSet` prints INVALID plus the
reason once. The degraded composed-row verbs take route (b) and record the SHOULD deviation (CM-18).

**Acceptance.**
- `tests/test_schema_adoption.lua` characterization cases (a)–(k) were green on the old seam and stay
  green after the cutover. (l) (a normalize refusal reaches the CLI once) and (m) (both parity pairs) are
  green.
- `! git grep -nE 'SESSION_PATHS|GLOBAL_PATHS|divertedPath|Helpers.Resolve\b|runFrame' -- settings core`
  succeeds. `wc -l settings/Panel.lua settings/SchemaStub.lua tests/test_schema_adoption.lua` are each
  under 1500. `tests/perf.lua` runs before and after, with both figures in the commit body.
- In client: a page Defaults shows exactly one `[Set]` line and one bar re-apply. `/cm set macroBar.<number> 9999`
  clamps. A bad enum shows one refusal.

**Non-goals.** Moving host reactions onto Schema's `onChange`. Route (a) for ConsumableMaster's degraded
verbs.

## D6 — KickCD #22: adopt Schema for the settings runtime (KC-18, on LK-22, LK-23)

**Target.** `settings/SchemaSetup.lua` is the first line of the TOC's settings block, under a
LOAD-BEARING comment. It creates `NS.Settings.Store`, a `LibKa0s-Schema-1.0` instance or a
`HostSchemaStub`, with `writeThrough = { 'enabled', 'locked' }` (route (a)).
- `announce` sends `CONFIG_CHANGED` with the row's section, and `announceBatch` fires each distinct
  section once.
- `resetExempt = { ['global.minimap.shown'] = true }`.
- Copy styling is one `SetMany` with `act = 'copy'`.
- The host copies in `settings/Panel.lua` and `Panel_Render.lua` are deleted (Panel.lua shrinks by about
  300 lines).
- The panel and section enum check moves from runtime into `tests/test_schema.lua`.

**Acceptance.**
- `tests/test_schema_store.lua` (a)–(i) are green, including "Copy styling is one SetMany: one
  `[Set] copy target→focus: N rows` line", "a bad value in a batch writes nothing" and the degraded
  `Store.Set("enabled", false)` writing through without a Lua error.
- The parity pairs are green. `grep -rn 'Helpers\.Set(\|H\.Set(\|Helpers\.Get(\|H\.Get(\|ValidateSchema\|SetRows\|MuteSetLog\|FindSchema' core settings modules`
  is empty.
- In client: every page persists across `/reload`. A color drag gives one debounced `[Set]` line.
  `/kcd set icons.nope 1` prints "Setting not found".

**Non-goals.** Adopting Launcher minor 2's gate in KickCD.

## D7 — MultiMeters #52: adopt Schema path primitives, registry and bulk bracket (MM-14, on LK-22)

**Target.** `settings/Schema_Paths.lua` builds one instance with a window-aware `resolveRoot(parts,
windowId)`. `announceBatch` sends `CONFIG_CHANGED` **once** per batch. `SetByPaths` becomes `S:SetMany`
with `instanceId`, and the single-path writes go through `S:Set` (`NS.SetByPath = S:Set`). The host
primitives, the registry and the bracket are deleted, and their public names stay as shims. The columns
carve-out becomes a hidden row with `normalize`. The minimap closures move onto the row. The degradation
stub is trimmed to what MultiMeters calls. The file ends at about 880 lines.

**Acceptance.**
- `tests/test_schema_batch.lua` characterization (a)–(g) is green before and after the swap, including
  "a valid 3-entry SetByPaths sends exactly one CONFIG_CHANGED" and "`window.frame.width` written with
  windowId 2 lands in window 2". The parity case (h) is green.
- `grep -n 'local function splitPath\|local function reindex\|local function runBulk' settings/Schema_Paths.lua`
  is empty. `refresh20x7` bytes/iter ≤ 303438.1.
- In client: a Frame slider on window 2 moves only window 2, and copying settings gives one refresh and
  one `[Set]` line.

**Non-goals.** Changing the columns in-array refusal (`window.columns.2.width` stays refused).

## D8 — PanelMaster #52: wrap the bus message constants in Bus Catalog (PM-12)

**Target.** A new `core/BusSetup.lua` loads right after `core\CoreSetup.lua` under a load-bearing comment.
It publishes `NS.BusLib`, the library or a stub whose `Catalog` returns its table. `R.MSG =
NS.BusLib.Catalog(addonName, {PANELS, PANEL})` and `S.MSG = …{SETTINGS}` replace the three loose
constants. Every reader uses the strict read, and a mistyped key raises on the live arm. The record half
(`Bus:New`) is not adopted.

**Acceptance.**
- "Parity: the Bus seam's degraded surface matches the live one" (`assertSurfaceParity(degradedNS.BusLib,
  'LibKa0s-Bus-1.0', { 'New' })`, with the same wire names on both arms) is green.
- "a mistyped message key raises at the read" (`assertErrorMatches(…, 'no bus message named PANELZ')`)
  is green, and the degraded arm answers nil.
- `grep -rn 'MSG_PANELS\|MSG_PANEL\b\|MSG_SETTINGS' core modules settings tests/*.lua docs/*.md` is empty.
- In client: `/reload` gives no Lua error, and a drag or a Master scale change repaints.

**Non-goals.** Adopting Bus tracked targets.

## D9 — PrettyChat #18: move `Schema.ResetRows` onto BulkRun/BulkAdd (PC-05)

**Target.** `ResetRows` filters the eligible rows first. It returns 0 without opening a bracket when none
are eligible, and otherwise runs inside `S.BulkRun('reset', label, walk)`, counting by read-back with
`S.BulkAdd(1)`. The console line stays byte-identical (`[Set] reset <label>: N rows`), and the re-apply
and the panel notify stay inside the bracket. `NS.Util.RunAct`'s use here and the `{wrote, changed}` tally
are gone.

**Acceptance.**
- Every existing bulk-line pin in `tests/test_override.lua` stays green **unchanged**.
- New cases are green: "an all-already-default reset still logs `[Set] reset Loot: 0 rows`", "a reset list
  with no eligible row logs nothing and returns 0", "ResetRows runs inside the runtime's bracket" (a spy
  sees one `BulkRun('reset','Loot')`), and the read-back count case.
- `grep -n 'BulkRun\|BulkAdd' settings/Schema.lua` hits, and `grep -n 'RunAct' settings/Schema.lua` no
  longer shows `ResetRows`.
- In client: two changed Loot strings then Defaults gives exactly one `[Set] reset …: 2 rows` line.

**Non-goals.** Any other PrettyChat seam change.

---

# Part E — explicitly out of scope for this entire plan

- **In-game verification as a claim.** Every in-client check is an instruction to an operator. No
  statement here rests on a client session having happened.
- **Any behavior change not traced to a finding, a consumer follow-up or an owner-scope issue.** No
  opportunistic refactors or renames.
- **Editing frozen bundles**: audits, reviews, automated-test bundles, revendor bundles, perf-analysis
  bundles, `docs/superpowers/` and `docs/investigations/`.
- **Patching `libs/` or `tests/_kit/`** in any consumer, for any reason.
- **Any release other than LibKa0s v1.56.0**, together with the standard v2.65.0 and the plugin 2.4.0.
  No addon is version-bumped or tagged, and nothing is merged without the owner's approval. Branches are
  pushed to origin at the end of each milestone, unmerged; the `v1.56.0` tag is pushed only when the owner
  approves the LibKa0s merge. A re-vendor
  changes a repository, not a player's client. The player-facing fixes reach players at each addon's next
  release, and the owner decides those.
- **The seven `state:will-not-do` issues** in OWNER_SCOPE, and every open issue not in OWNER_SCOPE's table.
- **A shared migration runner**, a library combat-edge helper, and AbsorbTracker's A1 alternative. These
  were declined by design decisions (1) and (3).
- **Renaming LibKa0s's `minimise` icon key.**
- **Adding a second locale.**

---

# Part F — collection-wide invariants

These hold at every committed point, not only at the end.

1. **All suites are green in every repository at every commit.** In each of the twelve code repositories
   (LibKa0s and the eleven addons), `luacheck .` reports 0/0 and `lua5.1 tests/run.lua` reports 0
   failed at every commit. `tests/perf.lua` exits 0 wherever one ships. At every cluster close the full
   standard gate (SG) holds. When a new gate is expected to redden a repo (kit 26's flips, a red-first
   case, a parity case after the re-vendor), the red is seen, and no commit leaves the repository red.
   The gate and its fix land in the same commit, or the fix lands first. Splitting them into two *work
   items* is fine. Splitting them into two *commits* is not. The one exception is the copy-only re-vendor
   commit (`libs/LibKa0s`, `tests/_kit`, the `CLAUDE.md` provenance line and
   `docs/revendor/2026-09-23-v1.56.0/`) in any of the eleven addons: it is green or lists its reds in its
   commit body. The addon's M2 pre-fixes aim to make it green, its M3 items clear any remaining red, and
   the addon is green again at the latest by `<AB>-DOCS` (Part B).
2. **Complexity: no function above CCN 15.** In every repository,
   `lizard -l lua -x './libs/*' -x './tests/_kit/*' -C 15 -w .` prints nothing, and each bundle's
   `suites.complexity.warnings` is 0. After AM-13 this holds with no carried exception.
3. **The 1500-line cap.** No authored `.lua` file in any repository is over 1500 lines
   (`git ls-files '*.lua' | grep -v '^libs/\|^tests/_kit/' | xargs wc -l | awk '$2!="total" && $1>1500'`
   prints nothing; in LibKa0s the check covers `LibKa0s/`, `testkit/` and `tests/`). After AM-26,
   AuraMaster's over-cap census is empty, so the invariant holds with no ratified exception anywhere in
   the collection.
4. **Every addon is on LibKa0s v1.56.0, byte-identical to the tag.** For each of the eleven addons,
   `diff -r <v1.56.0:LibKa0s> libs/LibKa0s` and `diff -r <v1.56.0:testkit> tests/_kit` are empty (via
   `git -C ../LibKa0s archive v1.56.0 LibKa0s testkit`). `CLAUDE.md`'s provenance line names v1.56.0,
   `tests/test_vendor_sync.lua` is green, and `Kit.VERSION` is 26. The payload, the kit and the provenance
   line moved in one commit.
5. **No local edits under `libs/` or `tests/_kit/`.** After each addon's RV commit,
   `git log --format=%H <RV-commit>..HEAD -- libs/ tests/_kit/` is empty. A defect found there is fixed
   upstream, tagged and re-vendored, never patched in place.
6. **Every addon references standard v2.65.0** in its three places (the TOC `## X-Standard` line, the
   README badge, and `CLAUDE.md` "Standards compliance"). The roll is done by `/wow-addon:revendor-standards`
   only after WowAddonStandards' v2.65.0 is on its default branch at origin, and never by hand from the
   local sibling. These are the M4 items, owner-gated; until the owner merges and pushes the standard, the
   invariant holds at v2.64.0 and the M4 items stay open.
7. **A minor bump is not complete without its API document.** In LibKa0s, `tests/test_versioning.lua`
   derives `docs/api/<Major>/version-<key>-docs.md` and `members-<key>.json` from `lib.MODULES` and stays
   red until they exist. The CHANGELOG versions line agrees.
8. **Generated records match the tree.** `docs/test-cases.md` equals `lua5.1 tests/run.lua --list`, and
   the README Tests badge equals its Totals, in the same commit as any case-count or case-name change.
   The copy-only re-vendor commit is the exception: the kit-26 case-name change it brings is regenerated
   by the addon's next item that touches the inventory, and at the latest by `<AB>-DOCS` (Part B).
9. **Frozen bundles are evidence and are never edited.** A base misstatement is corrected in the next
   bundle, never in the old one.
10. **US English** in authored prose and player-facing strings. The standing exemptions are verbatim
    Blizzard and third-party symbols, the `.cancelled`/`IsCancelled` timer identifiers, and LibKa0s's
    `minimise` icon key.
11. **No stored `minimap.shown` key** exists in any addon's SavedVariables. The stored key is LibDBIcon's
    `minimap.hide` everywhere, and the rename adds no migration step and no schema-version bump.
12. **GitHub writes are throttled** to at least 5 s apart and happen only after the owner's approval.
    Every commit subject starts `<ITEM-ID>: `. At the end of each milestone every touched repository's
    `feat/2026-09-23-review-audit-remediation` is pushed to origin; nothing is merged to `master`/`main`
    without the owner's go-ahead. The `v1.56.0` tag stays local until the owner approves the LibKa0s merge,
    and an addon branch whose provenance line names v1.56.0 may be on origin before the tag is.
13. **Every count claim names its members** or the command that produced it.
