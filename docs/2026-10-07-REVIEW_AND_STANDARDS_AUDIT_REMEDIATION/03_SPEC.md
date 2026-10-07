# 03 — Spec

**The end state after the run, by cluster and then by repo. This describes what "done" looks like, not
when it happens.**

> **Nothing in this document has been executed yet.** Every sentence describes a target. Where it says a
> file "carries" something or a command "prints" something, read it as "must, when the run is complete".

Inputs: `inputs/OWNER_SCOPE.md` (binding scope and rulings), `01_CONSOLIDATED_FINDINGS.md` (290 findings
in 53 clusters, 251 in scope), `plan-data/items.json` (164 items) and `plan-data/PLAN_REVIEW_RESOLUTIONS.md`
(the plan-review patches). Ordering, dependencies and effort belong in `04_EXECUTION_PLAN.md`; the
upstream changes are explained item by item in `02_UPSTREAM_CHANGES.md`. Item ids: `WS-nn`
(WowAddonStandards), `LK-nn` (LibKa0s), `DC-nn` (dev-copilot), `RV-<AB>` (re-vendor) and `<AB>-nn` /
`<AB>-STD` (addon items). Milestones: **M1** the three upstreams, **M2** the eleven re-vendors, **M3** the
addon items, each repo closing on its `<AB>-STD` item.

Addon codes: AT AbsorbTracker, AM AuraMaster, BL BankLedger, CM ConsumableMaster, KC KickCD, LH LootHistory,
MM MultiMeters, PM PanelMaster, PF PartyFrameEnhanced, PC PrettyChat, WG WhatGroup. These are the eleven
addons in `WowAddonStandards/standards/ADDONS.md`.

---

## How to read this

Part A states the upstream end state, Part B the re-vendor end state, Part C the end state of each
cluster, Part D the standards-reference roll every addon closes on. Each cluster has three parts:

- **Target:** the shape that exists when the cluster is closed, listed by repo.
- **Acceptance:** a command a reader can run, or a state a reader can look at, without asking the author
  what was meant. Commands run from the named repo's root.
- **Non-goals:** what the cluster deliberately leaves alone, so nobody widens it in flight.

RFC-2119 words carry their usual force. Where this spec and the standard disagree, the standard wins,
except in the clusters whose point is to change the standard: those describe v2.77.0.

**Two gates.** A **commit** is gated by the repo's own `CLAUDE.md` green gate. A **tag** additionally needs
a release run whose manifest reads `pass` for every suite with `suites.complexity.warnings == 0`. This run
cuts one tag, LibKa0s `v1.71.0`, locally. No addon is version-bumped or tagged.

**Shorthand used in the acceptance lists.**

- `$B` is `/home/tushar/.claude/dev-copilot/bin/ka0s-bounded`.
- **The standard gate (SG)** for an addon is all of the following:
  1. `$B luacheck .` reports 0 warnings / 0 errors.
  2. `$B lua tests/run.lua` reports 0 failed.
  3. `diff --strip-trailing-cr <(lua tests/run.lua --list) docs/test-cases.md` is empty, and the README
     Tests badge equals the Totals table's `Total` (under kit 38, the count of cases that run; declared
     skips sit on their own `| Skipped | N |` row).
  4. `$B lua tests/perf.lua` exits 0. This applies to AT, AM, CM, KC, LH, MM, PF and WG. BL and PC hold the
     performance-§12 exemption and PM holds its performance-§1 row, so these three have no `tests/perf.lua`.
  5. `$B bash tests/_kit/run-automated-tests.sh --suite complexity --no-bundle` reports 0 functions above
     CCN 15 and 0 blind files.
  6. No authored `.lua` file is over 1500 lines:
     `git ls-files '*.lua' | grep -v '^libs/\|^tests/_kit/' | xargs wc -l | awk '$2!="total" && $1>1500'`
     prints nothing (PrettyChat's generated `GlobalStrings/GlobalStrings.lua` excluded).
- **Red first** means the new case was seen failing on the pre-change tree and carries a
  `-- red under: <mutation>` comment (testing-§12).
- **Live docs** means authored files outside `libs/`, `tests/_kit/` and the frozen stores (`docs/audits/`,
  `docs/reviews/`, `docs/automated-tests/<run>/`, `docs/perf-analysis/<run>/`, `docs/revendor/<bundle>/`,
  `docs/superpowers/`, `docs/investigations/`).

---

## The surfaces this spec depends on

**Baseline, 2026-10-07.** All eleven addons vendor LibKa0s v1.70.0 byte-identically (kit revision 37) with
`## Interface: 120100`. The standard is v2.76.1. dev-copilot is 2.0.1. Every repo is on
`feat/2026-10-07-review-audit-remediation` at its `RA-00` commit.

| Surface | End state | Arrives in | Consumers that act on it |
|---|---|---|---|
| Standard **v2.77.0** | One version, one current changelog entry in the index; history in `standards/CHANGELOG.md`; `scripts/check-standard.sh`; the rulings in A1 | WS-01 … WS-11 | All eleven through `<AB>-STD`; LibKa0s (LK-12 README); dev-copilot (DC-15) |
| Test kit revision **38** | `--list` Total counts cases that run, declared skips on a `Skipped` row; `Kit.secret`, `Kit.isSecret`, `Kit.reveal`, `Kit.installSecretValue`, `Kit.SECRET_ERROR` | LK-01, LK-02 | All eleven through `RV-<AB>`; WG-01 uses `Kit.secret` |
| `LibKa0s-Slash-1.0` key **20.2** | `ParseValue` refuses `nan`, `inf`, `-inf` with `ERR_NUMBER`; `Slash.lua` cites `slash-commands-§1` | LK-05 | Every addon with `/<slash> set`, free |
| `LibKa0s-Env-1.0` minor **2**, OptionsIdList minor **4** | No bare-global `GetAddOnMetadata` / `IsAddOnLoaded` rung | LK-06 | All eleven, no behavior change; seven addons mirror it locally (C27) |
| `LibKa0s-Widgets-1.0` key **12.1.4.3.2** | LineChart minor 3: segments clipped to the plot rect, `ChartMath.ClipSegment`, hover re-sync on every render. Autocomplete minor 2: generation-guarded re-hook, integral `maxRows`, backdrop set once | LK-03, LK-04 | LootHistory (chart, autocomplete), BankLedger (autocomplete) |
| LibKa0s **v1.71.0** | Local annotated tag on the `LK-12:` commit; release bundle with `ANALYSIS.md` | LK-12 | All eleven `RV-<AB>` |
| dev-copilot (2.0.1, new commits) | Hook allows `command -v`; `ka0s-bounded` kills the tree on timeout; EOL hook resolves symlinks and has tests; `docs/ARCHITECTURE.md` hub; audit agent reads both documentation registers | DC-01 … DC-15 | Every session, once the owner merges and the plugin updates |
| Unchanged | Every other LibKa0s file; no `NEEDS_*` floor rises; no major added; no member removed | — | — |

---

# Part A — the upstream end state

## A1 — WowAddonStandards v2.77.0

**Target.** `standards/STANDARDS.md` line 1 reads `# Ka0s WoW Addon Standard (v2.77.0, <landing date>)`.
The rules, as they will be:

- **The index and its history.** The index carries the front matter, the reading guide, `## Sections`,
  `## Related documents` and only the current changelog entry, followed by
  `Full history: [CHANGELOG.md](CHANGELOG.md).` `standards/CHANGELOG.md` holds every earlier entry, newest
  first, listed under Related documents and not under Sections. On the next release the previous entry
  moves verbatim to the top of `CHANGELOG.md`. The footer carries no date. History order is correct
  (v2.19.0 above v2.18.0) and its two malformed references are fixed (WS-01).
- **The repo's own records.** WowAddonStandards keeps its own frozen `docs/audits/<date>/` and
  `docs/reviews/<date>/` stores, registered once each as directory rows in `docs/ARCHITECTURE.md`'s
  Documentation map. The roster lives only in `standards/ADDONS.md`, whose Folder column is plain code text
  (WS-02).
- **line-endings.** The repo's `.gitattributes` is line-endings-§5's non-client body byte-for-byte, with
  both shebang carve-outs. Every restatement names `*.sh` and `*.py` and cites line-endings-§3. Check (e)
  passes each path as a positional argument. The §7 EOL-gate MUST binds repos that run a suite; a
  suite-less documentation repo runs hand check (e) (WS-03).
- **toc-file-§5.** The load-bearing denominator is every position in the listing, found by reading every
  listed file for file-scope reads and writes of NS members and library majors. A constraint may read
  "below at least one of X/Y/Z". `AUDIT.md` step 4 checks every group. The worked example cites the TOC by
  heading (WS-04).
- **documentation.** §6's frozen-bundle exemption cites §3's frozen list by reference, covers a repo's own
  frozen stores, and sweeps with a `git ls-files` pipeline. §3 names sections, not ordinals. §8 counts
  Module Map once, is file-granular, and has one executable-content trigger: the first tracked `.lua`
  re-reads lint/testing/automated-tests, and any other executable content records its verification in
  `DEPENDENCIES.md`. library-stack-§7 labels §5 and §6 correctly and states the same exhaustiveness rule.
  Tier 2 includes `perf-analysis/README.md` (WS-05).
- **Audit expectations.** No playbook or section tells auditors to expect every addon to fail the launcher
  or disabled-state checks; the 2026-09-16 census is dated history. The scaffold runner comment says a
  named suite missing from disk raises (testing-§9) (WS-06).
- **Cross-repo citations (new documentation-§6 SHOULD).** A present-tense claim about another repo cites
  `Repo path` plus a symbol or heading. A historical claim pins `Repo@<sha>:path:line`. A present-tense
  count is a rule or is dated. Every rotted citation in the standard is converted (WS-07).
- **versioning-git.** Work lands on the default branch by default. An owner-directed or multi-repo
  changeset uses `feat/<YYYY-MM-DD>-<topic>`, the same name in every repo, merged `--no-ff` and deleted
  with its worktrees and stashes. Merge, tag, push and release keep their owner gates; pushing a feature
  branch at an owner-authorized checkpoint is sanctioned. Anti-pattern #21 matches; the range stays
  #1–#92 (WS-08).
- **events-frames-taint-§8.** The trigger set names `C_Spell.GetSpellCooldown`'s
  `startTime`/`duration`/`modRate` and `C_Spell.GetSpellCooldownDuration`'s `:GetRemainingDuration()`.
  `open-evolutions.md` records, without ruling, whether an adopted major needs a full library-absent stub
  (WS-09).
- **Mechanical gate.** `scripts/check-standard.sh` checks CR bytes, the `.gitattributes` body, citation
  ranges, the Sections list, anti-pattern contiguity, the five version stamps and internal links. It runs
  on demand and from sync-docs, never as a hook (WS-10).
- **Ripple.** The executive summary, context pack, playbooks, both READMEs and the Sections blurbs agree
  with every rule above. The v2.77.0 entry has one bullet per WS item with its finding ids and names the
  addon follow-ups it licenses (WS-11).

**Acceptance.**
- Every WS-01 … WS-11 `verify` in `plan-data/items.json` passes.
- `bash scripts/check-standard.sh; echo $?` prints `0`.
- `head -1 standards/STANDARDS.md` names v2.77.0. `grep -c '^- \*\*v' standards/STANDARDS.md` is `1` and
  `grep -c '^- \*\*v' standards/CHANGELOG.md` is `99`. `wc -c < standards/STANDARDS.md` is under 60000.
- `git grep -n 'v2\.76\.1' -- . ':!harvests' ':!docs/audits' ':!docs/reviews' ':!standards/CHANGELOG.md'`
  prints nothing.
- `diff <(awk '/^```gitattributes/{n++;f=(n==2);next} /^```/{f=0} f' standards/standards/line-endings.md) .gitattributes`
  is empty, and `git ls-files -z | xargs -0 grep -lI $'\r'` prints nothing.
- `git log --oneline master..HEAD | grep -c ' WS-'` is `11`.
- The branch is pushed at the M1 checkpoint and merged only on the owner's go-ahead.

**Non-goals.** Renumbering any section. Ruling the library-absent stub question. Relabeling "One-page
TL;DR" (`WAS-R-10`). Recounting every present-tense number (WS-07 rewrites them as rules). A tag.

## A2 — LibKa0s v1.71.0 and kit revision 38

**Target.** Every change in the surfaces table ships in one minor release. Each moved file bumps its
LibStub minor once and has its `docs/api/<Major>/version-<key>-docs.md` (Status Current) and members json;
the previous document is Superseded. `CHANGELOG.md`'s `## v1.71.0 — <date>` block lists the minors and
carries "What a consumer owes": re-vendor both payloads whole, roll the provenance line, regenerate
`docs/test-cases.md` in the same commit; WhatGroup adopts `Kit.secret`; a host still calling `ClearHover`
before a chart repaint may keep it. `README.md` names standard v2.77.0. `docs/releasing.md`'s provenance
template is at v1.71.0. `docs/api/CONSUMERS.md` reflects `ChartMath.ClipSegment`. The live docs carry no
unresolvable evidence id, no derived headroom figure and no British spelling in the two adoption pages,
which the prose gate now scans. The five over-shelf-life band files are one register row
(automated-tests-§4) that `RESULTS.md` points at. The widget suites carry `-- red under:` notes on their
key negatives. LibKa0s#43 is closed `state:done`; #32, #33, #37 and #39 carry `state:done`. The release
run is committed with `ANALYSIS.md`. The tag exists **locally** only.

**Acceptance.**
- Every LK-01 … LK-12 `verify` passes.
- `lua tests/run.lua` is green, including `test_versioning`, `test_kitsync` and `test_kit_secrets`.
  `luacheck .` is 0/0. `diff -r testkit tests/_kit` is empty.
- `grep -n 'Kit.VERSION = 38' testkit/framework.lua` hits; `wc -l < testkit/framework.lua` is under 1000.
- `grep -c '| Skipped |' docs/test-cases.md` is `1`.
- For the newest release bundle `S`: `.release` is `1.71.0`, `.git.dirty` is `false`, lint, tests and
  complexity are `pass`, `.suites.complexity.warnings` is `0`, and `ANALYSIS.md` sits beside it.
- `git tag -l v1.71.0` prints the tag on the commit whose subject starts `LK-12: `.
  `git ls-remote --tags origin v1.71.0` prints nothing until the owner approves.
- `grep -nE '\b(GetAddOnMetadata|IsAddOnLoaded)\b' LibKa0s/*.lua` shows only `C_AddOns`-qualified reads.
- `gh issue list --repo tusharsaxena/LibKa0s --state closed --label state:triaged --json number` returns
  `[]`.

**Non-goals.** A major bump or a raised floor. Peeling any band file (unless one crosses its trigger in
this release). A UTF-8 truncation helper. Migrating any consumer's local secret mock. Pushing the tag.

## A3 — dev-copilot (2.0.1, unbumped)

**Target.**
- **Bounded-runs hook.** `command -v` and `command -V` are probes, never runs. `command luacheck .` is still
  denied. `ulimit -v unlimited` is not treated as bounded, and a heavy command inside `sh -c '…'` is seen.
  Tests clean up their temp directories (DC-01, DC-02).
- **`ka0s-bounded`.** On a timeout from a non-interactive caller the whole process tree dies and releases
  its slot; `--foreground` is used only on a terminal. The slot count is recomputed while waiting
  (DC-03).
- **Line-ending hook.** It resolves a symlink before converting, so the target is converted and the link
  survives. `scripts/test_normalize_eol.py` covers both eol arms, binaries, out-of-repo files, empty paths
  and symlinks (DC-04, DC-05).
- **Docs.** `docs/ARCHITECTURE.md` has exactly five sections (Overview, Module Map, Known Limitations,
  Documentation map, Documented deviations reading `None.`). No live doc names `wow-addon` as a current
  repo. The kind list includes tooling repos, identically in both manifests. `DEPENDENCIES.md` describes
  its inventory by command and every `path:N` resolves. Live specs are in US English (DC-06, DC-07, DC-12,
  DC-13).
- **Specs.** The four issue overlays share one meaning of `all` (every `ADDONS.md` row, tagged by kind).
  Worked examples cite by symbol, heading or `Repo@sha`. The cross-addon pass uses `mktemp` and measures
  its baseline at review time. `wow-new-addon` edits the roster on a feature branch and never pushes.
  `finalize` stops on a push rejection and leaves reconciliation to the user (DC-08 … DC-11).
- **Handoffs from the standard.** The audit agent reads `docs/ARCHITECTURE.md` `## Documented deviations`
  in both documentation repos, names both carve-outs in check (c), passes paths positionally in check (e),
  describes the launcher as launcher-§2 does today, and knows the changelog's new home. The harvest command
  writes the new entry into the index and moves the previous one to `standards/CHANGELOG.md`. The
  `kind=standards` sync-docs overlay runs `check-standard.sh`. `README.md` names v2.77.0 (DC-15).
- **Remote.** `origin/main` is deleted at finalize if the owner agrees (DC-14).

**Acceptance.**
- `python3 scripts/test_detect_profile.py`, `test_check_overlays.py`, `test_bounded_runs.py` and
  `test_normalize_eol.py` pass with no expected failures. `python3 scripts/check_overlays.py` prints
  `OK: 13 overlays`. Both manifests parse.
- `python3 -c "import sys; sys.path.insert(0,'scripts'); import bounded_runs as b; assert b.check('command -v luacheck','/tmp')==[]; assert b.check('command luacheck .','/tmp')==['luacheck']"`
  succeeds.
- `KA0S_KIT_TIMEOUT_S=2 KA0S_KIT_CGROUP=off bin/ka0s-bounded bash -c 'sleep 4712; echo done' </dev/null`
  exits 124 and `pgrep -f 'sleep 4712'` then prints nothing.
- `grep -c '^## ' docs/ARCHITECTURE.md` is `5`. `! grep -rn 'neither repo has a' agents/` succeeds.
  `grep -n 'standards/CHANGELOG.md' agents/wow-standards-audit.md commands/wow-harvest-standards.md` hits
  both.
- The plugin version in `.claude-plugin/plugin.json` is still `2.0.1`.
- After finalize: `git ls-remote --heads origin main` prints nothing, or `exceptions.tsv`'s DC-14 row reads
  "declined by owner".

**Non-goals.** A version bump. A prose-check script. Changing how the audit or review agents grade beyond
DC-15's corrections. Retiring the absolute `ka0s-bounded` path in any spec.

---

# Part B — the re-vendor end state (RV-AT … RV-WG)

**Target.** In each of the eleven addons, `libs/LibKa0s/` and `tests/_kit/` are whole copies of the local
`v1.71.0` tag's `LibKa0s/` and `testkit/` trees (runner executable). The root `CLAUDE.md` provenance line
names v1.71.0 **in the same commit**. That commit also regenerates `docs/test-cases.md` under kit 38 and,
where the count moved, rolls the README badge, and writes the re-vendor record by hand following the local
`../dev-copilot/commands/wow-revendor-libka0s.md`, non-interactively (OWNER_SCOPE item 5):

- `docs/revendor/<date>-v1.71.0/`: `01_DELTA.md` whose line 1 is exactly
  `Delta: LibKa0s v1.70.0 -> v1.71.0` (base from the provenance line), with the per-file minors, the kit
  37 → 38 pairing, the majors the addon consumes and the contract changes under unmoved signatures;
  `02_CANDIDATES.md` (or a "Not adopted in this run" section) listing every new surface as
  `not adopted in this run`, except where a planned item adopts it (WG-01 for `Kit.secret`, AT-02 for the
  Widgets seam); `03_DECISIONS.md` where the addon's convention has one; `05_SUMMARY.md`. No interview and
  no GitHub issue.
- In the ten addons whose v1.69.0 and v1.70.0 re-vendors left no record (all but LootHistory, which
  recorded both), one consolidated span bundle `docs/revendor/<date>-v1.69.0-v1.70.0/` holding only
  `01_DELTA.md` and `05_SUMMARY.md`. Line 1 is exactly
  `Delta: LibKa0s v1.69.0 -> v1.70.0 (span: v1.69.0 v1.70.0)`; the body names base v1.68.1 and both
  vendoring commits; `05_SUMMARY.md` has one line per tag (`carried by sweep, nothing adopted`, or the
  adoption sha: BankLedger's v1.70.0 line cites `e5cd620`, the Autocomplete adoption).
- Per-addon extras in the same commit: AM, KC, MM, PF and WG de-tag live docs that name v1.68.1, v1.70.0
  or a kit revision, pointing at the provenance line instead. PF also cuts its `docs/ARCHITECTURE.md`
  Overview re-vendor narrative to one sentence (`PFE-A-05`). PC rolls the version token in its External
  dependencies paragraph.

The commit ends green. A red that is the mechanical consequence of the new payload (a test pinning the old
Totals shape or the old provenance string) is fixed host-side in the same commit and recorded under a
Blockers heading in `01_DELTA.md`. A behavioral red stops the item and becomes a clear-the-reds item before
the repo's M3 items start. Nothing under `libs/` or `tests/_kit/` is edited beyond the copy.

**Findings this closes.** C03 (`AT-A-01`, `AM-A-01`, `BL-A-01`, `CM-A-01`, `KC-A-01`, `MM-A-01`,
`MM-A-02`, `PM-A-11`, `PFE-A-02`, `PFE-A-11`, `PC-A-01`, `WG-A-02`); C07 (`AT-R-07`, `BL-A-03`, `KC-A-07`,
`LH-A-13`, `PM-R-09`, `PC-R-07`); C10 (`PFE-A-05`).

**Acceptance (per addon).**
- `T=$(mktemp -d); git -C ../LibKa0s archive v1.71.0 LibKa0s testkit | tar -x -C $T; diff -r $T/LibKa0s libs/LibKa0s && diff -r $T/testkit tests/_kit`
  prints nothing.
- `grep -n 'Kit.VERSION = 38' tests/_kit/framework.lua` and `grep -n 'v1.71.0' CLAUDE.md` both hit;
  `tests/test_vendor_sync.lua` passes against the tag.
- `grep -c '| Skipped |' docs/test-cases.md` is `1` (every addon carries the kit's diagnostics-contract
  opt-out skip), and the Total equals the README badge.
- `head -1 docs/revendor/*-v1.71.0/01_DELTA.md` is exactly `Delta: LibKa0s v1.70.0 -> v1.71.0`.
- In the ten span-bundle addons, `head -1 docs/revendor/*-v1.69.0-v1.70.0/01_DELTA.md` is exactly the span
  line and `ls` of that folder shows only `01_DELTA.md` and `05_SUMMARY.md`. AUDIT.md's re-vendor check
  (vendored tags since the horizon, minus every tag on line 1 of every `01_DELTA.md`) prints nothing.
- SG steps 1 and 2 are green at the RV commit. `git worktree list` in `../LibKa0s` shows no leftover tag
  worktree.

**Non-goals.** Adopting a new surface in the RV commit. Back-filling per-tag bundles for v1.69.0 or
v1.70.0. Editing any earlier, frozen re-vendor bundle.

---

# Part C — the cluster end state

## C01 — Doc and comment drift against the tree (documentation-§5)

**Target.** Live docs and comments state no derivable figure that disagrees with the tree. Where a figure
has a generated owner (`LibKa0s.xml`, `tests/run.lua`, `docs/test-cases.md` Totals, the provenance line),
the doc points at it instead of restating it. Present-tense cross-repo citations use WS-07's form.
- **LibKa0s (LK-07):** register evidence ids resolve in this repo; no derived headroom figure; the Perf
  stub template's AbsorbTracker comments describe the latch.
- **AbsorbTracker (AT-09):** no "thirty-two files"; both load-order chains include `WidgetsLineChart.lua`
  and `WidgetsAutocomplete.lua`; no v1.68.1 or v1.41.0; the mock description says one frame per unit; no
  restated minors.
- **AuraMaster (AM-08):** docs and comments name the launcher menu's Test mode entry, not left-click; the
  documentation-map row reads `Page | Covers`; the render-coverage comment points at `test_lizard_sighted`.
- **BankLedger (BL-04):** Logo-art pointers go to `docs/media.md`; the mono-glyph comment cites
  debug-logging-§2's exception; docs describe one saved view per tab and a session-only `lastTab`.
- **ConsumableMaster (CM-07):** `docs/ARCHITECTURE.md` cites handlers and writers by name; no
  `/wow-addon:` command name remains in live docs.
- **KickCD (KC-08):** the `addonName` rule, the `.luacheckrc` history comment, the compat-layer combat
  listener and `.pkgmeta` are count-free and true.
- **LootHistory (LH-16):** counts re-derived or dropped; `docs/testing.md` points at Totals instead of
  "Forty-four suites".
- **MultiMeters (MM-10):** no "fifty-eight" count; two retired-row lead-ins become dated "Retired on"
  headings; two `Slash.lua` comments are true.
- **PanelMaster (PM-11):** lifecycle, launcher and slash comments match the code; the census carries the
  command, not figures; `Database.lua` cites `R.Sanitize` by name.
- **PartyFrameEnhanced (PF-05):** no kit revision in the automated-tests README; the shim count comes from
  the standard's grep; no `/wow-addon:` name.
- **PrettyChat (PC-06):** the Item/Pool/Widgets sentence is true for v1.71.0; the performance-sweep header
  and the register row name the same commit; `.luacheckrc` is count-free; `PRETTYCHAT-A-NN` ids map to the
  in-repo `PC-NN` ids; LootHistory is cited by symbol.
- **WhatGroup (WG-05, WG-06):** `docs/performance.md` carries freshly measured `combatGateFlipping` and
  `showFrameRepeat` rows with the bisected cause of the 18 → 19 API move (or a statement that the bisect
  could not isolate it); `Compat.lua`'s header states its real TOC position; settings and Schema counts
  are count-free; `.luacheckrc` and `DEPENDENCIES.md` cite by function name.

**Acceptance.** Each item's verify greps pass (for example, in AbsorbTracker
`grep -rn 'thirty-two' docs/ARCHITECTURE.md docs/module-map.md docs/performance.md` prints nothing; in
PrettyChat `! git grep -n 'PRETTYCHAT-A-' -- ':!docs/audits' ':!docs/reviews' ':!docs/automated-tests' ':!docs/revendor' ':!libs' ':!tests/_kit'`;
in WhatGroup the `lua tests/perf.lua` figures equal the `docs/performance.md` rows). SG holds in every
repo touched.

**Non-goals.** Hand-editing a runner-generated `RESULTS.md` (`AT-A-11`). Editing any frozen bundle. Adding
a test that polices spelled-out counts.

## C02 — Stale or unsighted automated-test records and complexity runs

**Target.**
- **AuraMaster (AM-05):** `logCandidates` in `modules/Anchors_Snap.lua` is at CCN 12 or below through a
  file-local `targetText` helper; its `[Anchor]` line is byte-identical.
- **LootHistory (LH-14):** after the C16 slices, a fresh sighted `docs/automated-tests/<stamp>/` bundle
  (no `--release`) with `ANALYSIS.md` dispositions every 1000-1500 band file at its new line count, and the
  runner wrote `RESULTS.md`.

**Acceptance.** In AuraMaster, `lizard -l lua modules/Anchors_Snap.lua | grep logCandidates` shows CCN at
most 12. In LootHistory, the newest manifest reads `.git.dirty` false and `.suites.complexity.warnings` 0,
with `ANALYSIS.md` present; exactly one `LH-14 (1/2): ` commit and a final `LH-14: automated-test record`
commit exist.

**Non-goals.** Re-running the record in the other nine addons (ten `no` verdicts: staleness between
releases is expected). AuraMaster's four-suite release run (`AM-A-03` part (b)), which is a release-time
duty; AM-05's commit says so.

## C03 — LibKa0s v1.69.0/v1.70.0 re-vendors left unrecorded

**Target.** Part B. Every tag each addon vendored is recorded. AT, AM, BL, CM, KC, MM, PM, PF, PC and WG
each carry one span bundle `docs/revendor/<date>-v1.69.0-v1.70.0/`; LootHistory needs none.

**Acceptance.** Part B's span-bundle checks, in all ten.

**Non-goals.** Per-tag bundles for the lapsed span. A span line naming v1.68.1 (the span names only the
unrecorded tags; the base goes in the body).

## C04 — Documentation-repo doc set and register (WowAddonStandards, dev-copilot)

**Target.**
- **WowAddonStandards (WS-02):** no passage says audits or reviews are never written into this repo; both
  stores are registered once as directory rows; `DEPENDENCIES.md` describes the tree by kind.
- **dev-copilot (DC-06):** the five-section hub exists, with Documented deviations reading `None.`.
- **dev-copilot (DC-15):** the audit agent reads both repos' hub registers and treats a missing hub as a
  documentation-§8 finding; the stale launcher census and rung letters are gone.

**Acceptance.** WS-02's verify (`grep -n 'never here\|does \*\*not\*\* run audits' CLAUDE.md README.md docs/ARCHITECTURE.md`
prints nothing; both rows present). dev-copilot: `grep -c '^## ' docs/ARCHITECTURE.md` is 5;
`! grep -rn 'neither repo has a' agents/`; `! grep -n 'expected to fail\|11 of 11\|rungs (a) and (b)' agents/wow-standards-audit.md`.

**Non-goals.** A register row for WowAddonStandards (`WAS-A-19`: empty is correct). A trunk-based
deviation row in dev-copilot (`DC-A-12`, moot after WS-08).

## C05 — toc-file-§5 load-bearing TOC lines outside `# Core`

**Target.** The standard's denominator and `AUDIT.md` step 4 cover every position (WS-04). In each addon
the cluster named, every load-bearing position in the listing carries a `LOAD-BEARING` comment naming what
it publishes and who reads it at file load, and groups whose order is free say so once:
- **AbsorbTracker (AT-03):** `settings\Schema.lua` and `settings\OptionsSetup.lua` annotated; the rest of
  the listing walked.
- **ConsumableMaster (CM-08):** the `CoreSetup` comment names both file-scope printer consumers
  (`SlashDump`, `SlashCommands`); `SlashDump.lua` cites `CoreSetup`; the seed files are marked
  conventional (after a grep confirms none reads `KCM.Categories` at file scope). The TOC keeps CRLF.
- **LootHistory (LH-05):** `Escrow`, `AnalyticsCharts`, `Timeline` and `settings\Panel.lua` annotated; the
  `# Modules` header drops its false parenthesis and marks the other positions conventional; the Slash
  comment cites LibKa0s-Slash's `:New` by symbol; `AnalyticsCharts.lua` publishes `NS.Analytics`
  idempotently.

**Acceptance.** `grep -n 'every position in the listing' AUDIT.md standards/standards/toc-file.md` hits in
WowAddonStandards. AT: `grep -n -B1 'settings\\Schema.lua\|settings\\OptionsSetup.lua' AbsorbTracker.toc`
shows a `LOAD-BEARING` line above each, and the commit adds only comment lines. CM:
`grep -in conventional ConsumableMaster.toc` shows the `# Defaults` note and CR and LF counts are equal.
LH: `grep -c 'LOAD-BEARING' LootHistory.toc` rose by four; `grep -n 'Attribution before Collector' LootHistory.toc`
prints nothing.

**Non-goals.** Reordering any TOC. Refactoring the load-time reads in LootHistory's Escrow, Timeline and
Panel (they are annotated, not moved).

## C06 — Line-ending `*.py` carve-out and `.gitattributes` drift

**Target.** A1's line-endings bullet (WS-03). dev-copilot's audit agent names both carve-outs in check (c)
and passes paths positionally in check (e), byte-for-byte WS-03's form (DC-15). ConsumableMaster's
`.gitattributes` equals the client-bound §5 body (CM-STD).

**Acceptance.** WS-03's verify. In dev-copilot,
`grep -n '\*.py text eol=lf\|line-endings-§3 carve-outs' agents/wow-standards-audit.md` hits and
`! grep -n '"{}"' agents/wow-standards-audit.md` succeeds.

**Non-goals.** Changing line-endings-§3's carve-out set.

## C07 — Test-kit `--list` Totals count declared skips

**Target.** Kit 38's Totals count cases that run and list declared skips on their own row (LK-01). Every
addon's `docs/test-cases.md` Total equals its README badge (Part B).

**Acceptance.** SG step 3 in all eleven. `grep -c '| Skipped |' docs/test-cases.md` is `1` in all eleven,
since each carries the kit's diagnostics-contract opt-out as its one declared skip (2026-10-07 suite
state). The six findings (AT, BL, KC, LH, PM, PC) close with no addon code change.

**Non-goals.** A local inventory edit in any addon. Making case registration host-dependent.

## C08 — Standard internal contradictions and section-coverage claims

**Target.** A1's documentation and audit-expectation bullets (WS-05, WS-06).

**Acceptance.** WS-05's and WS-06's verifies (`grep -n 'exclude-dir=audits' standards/standards/documentation.md`
prints nothing; `grep -n 'SKIPPED, not failed' standards/NEW_ADDON_CONTEXT.md` prints nothing;
`grep -n 'RAISES (testing-§9)' standards/NEW_ADDON_CONTEXT.md` hits once).

**Non-goals.** Restructuring documentation-§8's tables beyond the counting and trigger fixes.

## C09 — Addon doc-set structure (documentation-§1/§2/§3) and release notes

**Target.**
- **LootHistory (LH-15, LH-17):** the Documentation map's out-of-scope line uses documentation-§3's frozen
  list as WS-05 words it; README Usage closes on one signpost sentence; the 1.4.0 Version History row has
  no contributor-facing gate line.
- **MultiMeters (MM-08):** the 1.1.0 row tells players the minimap setting moved, with the CLI mapping
  verified from git.
- **PanelMaster (PM-12):** `CLAUDE.md`'s stub items are in the standard's order (the green gate directly
  after the docs pointers); README has no angle-bracket placeholders and no release-process line in the
  1.2.0 row.
- **PartyFrameEnhanced (PF-05):** the Documentation map has the `### Addon-specific (documentation-§3,
  Tier 3)` table reading `None.`; `docs/settings-panel.md` is a `Page | Covers` table plus one `## <Page>`
  heading per page.

**Acceptance.** LH: `grep -n 'Released on lint, tests and complexity only' README.md` and the PM equivalent
print nothing; `grep -n 'perf-analysis/<run>' docs/ARCHITECTURE.md` hits in LH. MM:
`grep -n 'global.minimap.shown' README.md` hits the 1.1.0 row. PM: the `Green gate before every commit`
line number in `CLAUDE.md` is lower than the `Bundles [LibKa0s]` line number; `grep -n '/pm profile <' README.md`
prints nothing. PF: `grep -n '### Addon-specific' docs/ARCHITECTURE.md` hits.

**Non-goals.** A new Version History row or a version bump.

## C10 — Hub `docs/ARCHITECTURE.md` past the ~400-line guideline

**Target.** No mandated hub section runs past ~60 lines without spilling to its named target, and the hubs
the plan touches are at or near ~400 lines with no rule content lost:
- **AuraMaster (AM-09):** the drag/snap/detach narrative moves verbatim to `docs/data-flow.md`; Module Map
  ≤ 60 lines; hub ≤ ~400.
- **LootHistory (LH-15):** Module map is a summary plus one link to `docs/module-map.md`.
- **MultiMeters (MM-10):** retired-row paragraphs become one-line pointers; clearly under 578 lines.
- **PanelMaster (PM-11):** the perf-decline preamble and census narrative go; ≤ 400 lines; the
  `Files over the 1500-line cap` heading and table stay.
- **PartyFrameEnhanced (RV-PF):** the Overview re-vendor narrative is one sentence; under 435 lines.
- **PrettyChat (PC-07):** the cap-exemption prose moves to `docs/global-strings.md` `## The cap exemption`;
  the cap heading, command, table and verdict stay; ≤ 400 lines.

**Acceptance.** The `wc -l docs/ARCHITECTURE.md` bounds above. In AM,
`awk '/^## Module Map/,/^## Settings Schema/' docs/ARCHITECTURE.md | wc -l` is at most 60. Each repo's
doc-structure, docmap and layout-cap tests stay green.

**Non-goals.** BankLedger's hub (`BL-A-08`: no mandated section breaches the spill). Removing any live
register row or required section.

## C11 — Rotted cross-repo citations and worked examples

**Target.** A1's cross-repo citation bullet (WS-07) and the TOC worked example by heading (WS-04).
dev-copilot's specs follow the same form (DC-09).

**Acceptance.** WS-07's verify (`grep -rn 'Schema.lua:1553\|LSMPatch.lua\|Browser.lua:98\|revision 24 ships today\|AbsorbTracker.toc:35' AUDIT.md standards/standards standards/EXECUTIVE_SUMMARY.md standards/NEW_ADDON_CONTEXT.md`
prints nothing; each converted E5 citation resolves by symbol grep or `git cat-file -e <sha>:<path>`).
dev-copilot: `! grep -rn 'C.LSMValues' commands profiles` and
`! grep -rn 'five addons are permanent perf-skippers\|seven of the eleven' commands profiles agents`.

**Non-goals.** Re-deriving line numbers. A full recount.

## C12 — Standard changelog, index and citation hygiene

**Target.** A1's index-and-history bullet (WS-01); library-stack-§7 and `AUDIT.md` cite documentation-§6
for the citation scheme (WS-05).

**Acceptance.** WS-01's verify, including the sorted diff of moved entries against the old index with only
the two typo fixes, and `grep -n '^- \*\*v2\.1[789]' standards/CHANGELOG.md` in the order v2.19.0, v2.18.0,
v2.17.1, v2.17.0. `grep -n 'documentation-§5/§6' AUDIT.md` prints nothing.

**Non-goals.** Rewriting the content of historical entries beyond the three named edits.

## C13 — Issue-store housekeeping

**Target.** No closed issue in the collection carries an open-only status label among the ones the findings
named, and two superseded declines say they were superseded:
- **LibKa0s (LK-11):** #32, #33, #37 and #39 `state:done`.
- **AuraMaster (AM-STD):** #22 `state:done`.
- **PanelMaster (PM-10):** #47 `state:done`.
- **KickCD (KC-10):** a comment on closed #11 says #10 (`KickCD@e0da04c`) superseded the RenderGrid decline;
  label unchanged.
- **PrettyChat (PC-08):** a comment on #8 says SP-PC-01's Profiles page superseded the per-character
  profile decline; label unchanged.

Each lands with no commit and has an `exceptions.tsv` row with its proof command. Writes are spaced.

**Acceptance.** `gh issue list --repo tusharsaxena/<Repo> --state closed --label state:triaged --json number`
returns `[]` for LibKa0s and PanelMaster; `gh issue view 22 --repo tusharsaxena/AuraMaster --json labels`
shows `state:done` and no `state:untriaged`; the KC-10 and PC-08 comments are found by their greps; the
five `exceptions.tsv` rows exist.

**Non-goals.** Any other issue write. A rule in dev-copilot that closing an issue swaps its label.

## C14 — Slash command argument parsing and output shape

**Target.**
- **AuraMaster (AM-01):** `/am select` and `/am delete` resolve `#N` as an id always; a bare number resolves
  by exact name first; when a name and an id point at different containers the command refuses, naming
  both. A destructive delete never removes a container other than the one the player named.
- **AuraMaster (AM-03):** the debug help row reads `Toggle the debug console — on/off enable/disable
  logging`; `docs/slash-dispatch.md` describes the containers listing the code prints.
- **KickCD (KC-04):** `/kcd debug <unknown word>` refuses and lists sub-verbs without toggling the console;
  `castbar` and `interrupt` take an optional `target|focus`.
- **MultiMeters (MM-10):** `docs/slash-dispatch.md` and the usage text say `/mm window copy` accepts a window
  id.
- **PartyFrameEnhanced (PF-04):** `/pfe status` prints one unlocked flag.
- **PrettyChat (PC-04):** `/pc test category General` is refused as unknown; General is not in the Valid
  list.

**Acceptance.** SG in each repo; each item's new cases are in `docs/test-cases.md`. AM: `test_locale` green
and `grep -n 'enable or disable logging' locales/enUS.lua settings/Slash.lua` prints nothing. KC:
`grep -n 'runDebug(self, "")' core/KickCD.lua` prints nothing.

**Non-goals.** Forbidding numeric container names. Changing MultiMeters' parser.

## C15 — Library-absent stubs and unreachable fallbacks

**Target.**
- **WowAddonStandards (WS-09):** the stub-burden question is recorded in `open-evolutions.md`, not ruled.
- **AbsorbTracker (AT-02):** `core/WidgetsSetup.lua` publishes `NS.Widgets` (the live major, or a stub
  whose `DragHandle` answers nil and whose `DRAG_HANDLE` keeps `HANDLE_ROOM` at 0); `Bar.lua` and
  `Display.lua` read `NS.Widgets` and never call LibStub for it; the TOC line is annotated
  `LOAD-BEARING`; a parity case and a degraded-load case exist.
- **AuraMaster (AM-03):** the library-absent Slash stub carries no `FormatRow`; degraded rows print
  `/am <cmd>  <desc>` plainly.
- **LootHistory (LH-04):** a Perf parity case asserts the stub exposes every member the addon reads, with
  the grep that derived the list.
- **PanelMaster (PM-08):** the degraded `Sl.FormatKV` renders `path = value` plainly with no `|c`; the byte
  pin against the library is replaced by a degraded-env case.

**Acceptance.** AT: `grep -n 'LibStub' modules/Bar.lua modules/Display.lua` shows no Widgets lookup;
`grep -n 'parity: the Widgets stub' tests/test_surface_parity.lua` hits. AM:
`grep -n 'FormatRow' settings/Slash.lua` shows no stub definition. PM:
`grep -n 'cFFFFFF00%s|r = ' settings/Slash.lua` prints nothing. SG in each.

**Non-goals.** Removing stubs anywhere (U-3 is unruled). AbsorbTracker's unreachable "Debug console
unavailable" arms (`AT-A-16`).

## C16 — Release gate: functions above CCN 15

**Target.** In AuraMaster, BankLedger and LootHistory, the sighted complexity suite reports 0 functions
above CCN 15:
- **AuraMaster (AM-05):** `logCandidates`.
- **BankLedger (BL-01):** `LT.GroupEntries` through two module-level comparators (and a module-level sort
  key helper if needed); group order and in-group order unchanged, pinned by a characterization case
  first.
- **LootHistory (LH-09 … LH-14):** every flagged function in `core/Database.lua`, `core/Ledger.lua`,
  `modules/AnalyticsLedger.lua`, `modules/Reconciler.lua`, `modules/Escrow.lua`,
  `core/LifecycleSetup.lua`, `core/Compat.lua`, `modules/Collector.lua`, `modules/Holdings.lua`,
  `modules/TestData.lua`, `modules/Browser.lua`, `modules/BrowserTable.lua` and
  `modules/BrowserTableGroup.lua`, each with a characterization test first, by file-scope ordered lists
  and named local helpers, with no in-function dispatch table and hot-path upvalues kept. Ledger step
  order, `tests/analytics_golden.txt` and seeded test-mode output are unchanged.

**Acceptance.** SG step 5 in all three. In LootHistory, the stand-down/stand-up order in `test_disabled.lua`
is unchanged and the currency-line perf scenario is not slower beyond noise.

**Non-goals.** PrettyChat's `listSettings` at exactly 15 (`PC-R-09`, refuted). Any behavior change.

## C17 — Files approaching the 1500-line cap

**Target.** Each hot file is peeled on its named seam by a pure move (identical public members, no new
globals, the TOC annotated, module maps updated, the live watch-list row refreshed):
- **AuraMaster (AM-04):** `tests/test_anchors_drag.lua` splits into lifecycle and
  `tests/test_anchors_attach.lua`; the sorted case-name set and Total are unchanged.
- **AuraMaster (AM-06):** the frozen migrations move to `core/Database_Migrations.lua`; both files under
  1000 lines; migrations still run at OnInitialize.
- **BankLedger (BL-03):** the per-tab view machinery moves to `modules/Browser_Views.lua` through an
  explicit seam table; `Browser.lua` under 1250 lines.
- **LootHistory (LH-08, LH-18):** the grouping and holder-move layer moves to
  `modules/BrowserTableGroup.lua` (`BrowserTable.lua` under 1300); the widget kit moves to
  `modules/BrowserWidgets.lua` (`Browser.lua` under 1400); goldens unchanged.

**Acceptance.** The `wc -l` bounds above; `grep -n` finds each new file in the TOC and `docs/module-map.md`;
`docs/test-cases.md` Total unchanged by each peel; SG step 6 in all three.

**Non-goals.** A second peel of BankLedger's `Browser.lua` (skin and geometry). Peeling any file not named.

## C18 — Bare or malformed standard citations (documentation-§6)

**Target.** LibKa0s `Slash.lua` cites `slash-commands-§1` (LK-05). KickCD's standalone bare `§N` sites in
`tests/test_flow_traces.lua`, `tests/test_library_lines.lua`, `docs/settings-panel.md` and
`docs/slash-dispatch.md` name their section file (KC-09). MultiMeters' `core/LifecycleSetup.lua` reads
`(architecture-§4)` (MM-10).

**Acceptance.** LibKa0s: `grep -n 'slash-commands.md:' LibKa0s/*.lua` prints nothing. MM:
`grep -rn 'architecture-4' core settings modules` prints nothing. KC: every remaining bare `§N` hit is a
same-sentence continuation.

**Non-goals.** A per-addon guard test (it would reject the standard's own continuation form).

## C19 — Perf stand-down lifecycle edge cases

**Target.** State armed before or during a stand-down does not outlive it:
- **AbsorbTracker (AT-06):** `/at debug hold` refuses while stood down for a perf capture and arms no
  timer; the degraded-load test asserts `NS2.IsStoodDown()`, not the stub literal; the stub keeps
  `suspended = false`.
- **LootHistory (LH-02):** `Util.Coalesce` tracks its timer handle, so a window canceled by the stand-down
  does not wedge the trigger.
- **PanelMaster (PM-04):** `NS.StandDown` calls `NS.Unlock:DropPending`, and an unlock request while stood
  down applies immediately instead of queuing.
- **LibKa0s (LK-07):** the Perf document says a latch-based host may ask its latch.

**Acceptance.** Each new case is red first and green after. AT: `grep -n 'IsStoodDown' settings/Slash.lua`
shows the gate; `grep -n 'Perf.suspended' tests/test_perf.lua` prints nothing. PM:
`grep -n 'DropPending' core/LifecycleSetup.lua modules/Unlock.lua` hits both.

**Non-goals.** Removing `suspended` from any Perf stub or the host contract.

## C20 — Secret-value handling and test support

**Target.**
- **WowAddonStandards (WS-09):** §8 names the spell-cooldown fields.
- **LibKa0s (LK-02):** `Kit.secret` and its siblings exist; nothing installs `issecretvalue` by default.
- **WhatGroup (WG-01):** `Compat.IsSecret` exists. `Compat.GetSpellCooldownRemaining` reads `isActive` and,
  when `start` or `duration` is secret, does no comparison or arithmetic and returns `nil, isActive`; it
  never returns 0 for a secret reading. The chat notice tags "(on cooldown)" when `isActive`; the button
  renders the cooldown state with no figure; the ticker keeps its last text and stays armed. Swipe values
  pass straight to `Cooldown:SetCooldown`. Regression cases use `Kit.secret` and
  `Kit.installSecretValue`.
- **MultiMeters (MM-02):** `Secrets.PlainTruth` is the one boolean probe; the file-local copies in
  `Aggregator.lua` and `Tooltip.lua` are gone; `Provider.lua` uses it, and the field census checks
  secrecy before the boolean short-circuit.

**Acceptance.** WG: `grep -n 'IsSecret' core/Compat.lua` hits; reverting the guard locally turns the new
cases red. MM: `grep -rn 'local function plainTruth' modules core settings` and
`grep -n 'isLocalPlayer == true\|isLocal == true' modules/Provider.lua` print nothing. SG in both.

**Non-goals.** Migrating MultiMeters' `tests/mock_secrets.lua`. Installing `issecretvalue` in the kit's
default mock.

## C21 — Hot-path allocation and over-broad event registration

**Target.**
- **AbsorbTracker (AT-05):** `doRepaint` iterates `NS.Units.LIST` directly; no closure per coalesced pass;
  the perf ceiling re-derived and lower than AT-01's.
- **ConsumableMaster (CM-03):** `OnSpecChanged(event, unit)` returns early for any unit other than the
  player (nil passes).
- **KickCD (KC-06):** `Util.Throttle` reuses a frozen `EMPTY_ARGS` for zero-argument calls.

**Acceptance.** AT: `grep -n 'ForEachUnit' modules/Timer.lua` prints nothing and `repaintPass` bytes/iter
are below AT-01's figure. CM: `grep -n 'unit ~= "player"' core/ConsumableMaster.lua` hits. KC:
`grep -n 'EMPTY_ARGS' core/Util.lua` hits.

**Non-goals.** PartyFrameEnhanced's driver strings (`PFE-R-06`) and MultiMeters' vehicle-event frame
(`MM-R-09`, refuted).

## C22 — Raw lizard quoted as the complexity check

**Target.** In AT (AT-09), CM (CM-07), LH (LH-16), MM (MM-09) and PM (PM-11), every reader-facing gate line
is `bash tests/_kit/run-automated-tests.sh --suite complexity` (with `--no-bundle` where the doc runs it
ad hoc); raw lizard appears only as a note on what the runner executes. MultiMeters' `DEPENDENCIES.md`
reads "any recent (verified with 1.24.0)" for lizard and states the documentation-§7 parity sentence.

**Acceptance.** `grep -n 'lizard -l lua' docs/automated-tests/README.md` prints nothing in all five, and
also prints nothing for `DEPENDENCIES.md` and `docs/performance.md` in MM and LH.

**Non-goals.** Editing frozen superpowers plans that quote raw lizard.

## C23 — Destructive and reset actions: scope and confirmation

**Target.**
- **PanelMaster (PM-01):** the delete-all popup names the active profile and says every character on it
  loses its panels.
- **PanelMaster (PM-02):** Reset all settings re-locks the panels and hides the debug console inside the
  existing bulk bracket by driving each session-only row through its default; one `PanelsChanged`; the
  comment that defended the omission is gone.
- **PanelMaster (PM-03):** the editor's per-panel Delete and Reset ask first, naming the panel; the popup
  carries the panel id and resolves it afresh on accept; the Registry comment is true.
- **PrettyChat (PC-03):** the Categories header Defaults asks before resetting all eight tabs; the footer
  path, already confirmed by Blizzard's dialog, does not ask twice.

**Acceptance.** PM: `grep -n 'this character' settings/Slash.lua` prints nothing;
`grep -n 'deliberate rather than an oversight' settings/OptionsSetup.lua` prints nothing; the
`KA0S_PANELMASTER_DELETE` and `KA0S_PANELMASTER_RESET` definitions and callers exist. PC:
`grep -n 'PRETTYCHAT_RESET_CATEGORIES' settings/Panel.lua` hits. SG in both.

**Non-goals.** Changing PrettyChat's General page or the library's combat refusal.

## C24 — Debug-logging change gates and load-time logging

**Target.**
- **AuraMaster (AM-02):** every ladder-level migration summary, the stamp line and the starter-seed line
  go through `NS.DebugLog.DebugAtEnable('Migrate', …)` with byte-identical text; per-container lines stay
  gated `NS.Debug`.
- **AbsorbTracker (AT-08):** the absorb-secret edge and the bar-visibility line go through
  `DebugChanged`, so they restate after `Clear()` or a fresh enable; `dbgAbsorbSecret` is gone.

**Acceptance.** AM: `grep -c "DebugAtEnable('Migrate'" core/Database.lua` is at least 13. AT:
`grep -n 'DebugChanged' core/AbsorbTracker.lua modules/Display.lua` shows two sites.

**Non-goals.** ConsumableMaster's `KCM.DebugQuiet` and PartyFrameEnhanced's `runDebug` (both compliant).

## C25 — Deviation register rows and unresolvable evidence ids

**Target.** Every register row's evidence resolves in its own repo, and cross-repo plan ids carry their
bundle:
- **LibKa0s (LK-07):** rows cite `LK-28`, `LK-37`, `LK-17d`.
- **AbsorbTracker (AT-04):** the savedvariables-§1 per-profile-stamp row is retired to
  `docs/recorded-decisions.md` with today's date and its two residual differences (stamp default 1; the v3
  lift writes the stamp), cited by symbol.
- **ConsumableMaster (CM-07):** the compat and options-ui-§1 rows cite ids that resolve here; "WS-02
  route (b)" reads "route (b) of options-ui-§1".
- **PartyFrameEnhanced (PF-05):** row 2 cites the 2026-09-23 audit `PFE-15` and `79cd225`; row 1 drops
  "pending the owner's ratification" only if the owner has confirmed default D9, otherwise the open
  question is recorded in the execution record.

**Acceptance.** LibKa0s: `grep -n 'LibKa0s-A-' CLAUDE.md` prints nothing. AT:
`grep -n 'savedvariables-§1' docs/ARCHITECTURE.md` shows no register row. CM:
`grep -nE 'CM-R-10|CM-18|WS-02' docs/ARCHITECTURE.md` prints nothing in the register.

**Non-goals.** Changing any row's reasoning. An upstream rule on cross-repo ids beyond WS-07's SHOULD.

## C26 — Byte-wise string handling breaks non-Latin locales

**Target.**
- **PanelMaster (PM-05):** `Util.Slugify` keeps ASCII behavior byte-identical and hex-encodes bytes
  ≥ 0x80, so distinct UTF-8 names get distinct frame names; stored frame names are never rewritten.
  `Util.FoldName` folds Latin-1, Latin Extended-A, Greek and Cyrillic case, and `R:FindByName` uses it.
  The README explains the hex form.
- **KickCD (KC-02):** cast-bar truncation counts UTF-8 characters through a file-local `utf8Prefix`; a
  name of exactly `maxChars` characters is never cut.
- **AuraMaster (AM-07):** the container picker stops lowercasing translated labels.
- **LibKa0s (LK-03):** the chart's `formatX` doc says the default uses the C-runtime month and a localized
  host should pass `formatX`.

**Acceptance.** PM: `grep -n 'FoldName' modules/Registry.lua` hits; `wc -l < modules/Registry.lua` under
1000. KC: `grep -n '#name <= maxChars' modules/Castbar.lua` prints nothing. AM:
`grep -n ':lower()' settings/OptionsSetup.lua` shows neither label site.

**Non-goals.** A shared LibKa0s UTF-8 helper. Rewriting stored PanelMaster frame names.

## C27 — Dead compat fallback rungs on removed AddOns globals

**Target.** No authored code in LibKa0s or any addon reads `GetAddOnMetadata`, `IsAddOnLoaded`,
`GetNumAddOns` or `GetAddOnInfo` as a bare global. Each library-absent `Meta` answers Env first, then
`C_AddOns.GetAddOnMetadata`, else nil, and its comment describes that two-rung ladder:
- **LibKa0s (LK-06):** Env and OptionsIdList.
- **MultiMeters (MM-07):** `NS.Meta`, plus its defending "pre-11.x" comments.
- **PanelMaster (PM-09):** `NS.Meta` and `Compat.AddOnFolders` (which answers nil without `C_AddOns`).
- **BankLedger, ConsumableMaster, PartyFrameEnhanced, WhatGroup (BL-05, CM-09, PF-06, WG-07):** the
  identical rung, removed for consistency. These four items trace to no finding; the plan review added
  them, and the owner may drop them without affecting any traced finding.

Each addon gains a red-first case: with Env and `C_AddOns` absent and a recording `_G.GetAddOnMetadata`
spy planted, `Meta` makes zero spy calls and answers nil. `.luacheckrc` drops each name luacheck proves
unread.

**Acceptance.** In all eleven addons,
`git grep -nE '(^|[^._A-Za-z])GetAddOnMetadata\(|_G\.GetAddOnMetadata\(' -- '*.lua' ':!libs' ':!tests'`
prints nothing. In PM, `grep -n 'GetAddOnMetadata\|GetNumAddOns\|GetAddOnInfo' core/EnvSetup.lua core/Compat.lua .luacheckrc`
shows only `C_AddOns` reads. SG in every repo touched.

**Non-goals.** A Compat shim for any of these globals. The standard's compat worked case (`LK-A-09`: it is
right).

## C28 — Event-frame discipline (events-frames-taint-§1)

**Target.**
- **PartyFrameEnhanced (PF-03):** the pending-secure listener is a dedicated AceEvent target (not the addon
  object, not `NS.bus`), registered through `NS.SafeRegisterEvent`, armed only when writes are pending and
  released on fire; `NS.PendingRegenArmed()` is truthful.
- **WhatGroup (WG-03):** `NS.StandDown`'s owed-Hide registration goes through `NS.SafeRegisterEvent`; a
  `__badEvents` case proves a rejected `PLAYER_REGEN_ENABLED` does not raise.

**Acceptance.** PF: `grep -n 'CreateFrame' core/PartyFrameEnhanced.lua` shows no regen watcher. WG:
`grep -rn 'self:RegisterEvent(' core modules settings` prints nothing outside the helper.

**Non-goals.** PrettyChat's named combat watcher (`PC-R-12`, refuted).

## C29 — Pre-formatted chat lines (events-frames-taint-§8)

**Target.** The named sites hand their values to the shared printer as arguments, and the chat text is
byte-identical:
- **AbsorbTracker (AT-08):** `runLadder`'s "Settings upgrade stopped" line.
- **BankLedger (BL-02):** `B:SaveView`, `B:ResetView` and `Sl:ResetEverything`.
- **LootHistory (LH-07):** five lines in `settings/Schema.lua`, `settings/Slash.lua` and `modules/Browser.lua`.

**Acceptance.** AT: `grep -n '" .. from .. "' core/Database.lua` prints nothing. BL:
`grep -n ':format(lastTab)' modules/Browser.lua` prints nothing. Existing chat-capture tests stay green
unchanged.

**Non-goals.** BankLedger's `Slash.lua:253`, `:339` and `DebugLogSetup.lua:51` (not deviations).

## C30 — NaN, infinity and unvalidated numeric input

**Target.**
- **LibKa0s (LK-05):** `ParseValue` refuses non-finite numbers.
- **ConsumableMaster (CM-04):** `/cm priority` accepts only a positive item id or `s:<positive spell id>`;
  anything else prints the usage line.
- **PanelMaster (PM-06):** `Util.IsFinite` guards `COERCE.number`, `Util.Clamp`, `freeNumber` and
  `R:SetPosition`; `/pm recover` repairs a non-finite position in one run and a second run reports nothing
  moved.

**Acceptance.** LibKa0s: `grep -n 'PARSE_MINOR = 2' LibKa0s/SlashParse.lua`. CM:
`grep -n 'parsePriorityID' core/SlashCommands.lua` and its new case. PM:
`grep -n 'IsFinite' settings/PanelSchema.lua core/Util.lua modules/Registry.lua` hits all three.

**Non-goals.** Making `Schema.Set` type-aware.

## C31 — Named non-setting state and schema version targets

**Target.**
- **KickCD (KC-05):** the migration target is `NS.SCHEMA_VERSION = 5`; no `Database.CURRENT_DB_VERSION`
  alias survives in code, tests or live docs.
- **LootHistory (LH-16):** `docs/schema.md`'s holdings Writers bullet names all three writers with the act
  that reaches each.

**Acceptance.** KC: `git grep -n 'CURRENT_DB_VERSION' -- core modules settings 'tests/*.lua' docs/ARCHITECTURE.md docs/module-map.md docs/schema.md`
prints nothing (deliberate red-under notes aside). LH: `grep -n 'MarkGenesis' docs/schema.md` hits.

**Non-goals.** Changing KickCD's stored value. PanelMaster's minimap position row (`PM-A-05`, refuted).

## C32 — versioning-git trunk-based MUST vs feature-branch practice

**Target.** A1's versioning-git bullet (WS-08). Each addon's `CLAUDE.md` that restates the branch rule says
the same thing after its `<AB>-STD`.

**Acceptance.** WS-08's verify: `git grep -n -i 'trunk-based' -- . ':!harvests' ':!docs/audits' ':!docs/reviews' ':!standards/_raw' ':!standards/CHANGELOG.md'`
prints nothing or only the revised rule; `grep -n 'feat/<YYYY-MM-DD>-<topic>' standards/standards/versioning-git.md CLAUDE.md`
hits both; the anti-pattern count is still 92.

**Non-goals.** Per-repo deviation rows.

## C33 — British spellings in live docs (localization-§5)

**Target.** LibKa0s's two adoption pages are in US English and gated (LK-08). dev-copilot's live specs
and root docs are in US English (DC-12).

**Acceptance.** LibKa0s: `grep -niE 'colour|behaviour|judgement|summarise|licence|artefact|modelling|standardised|renormalise' docs/adoption-prompt.md docs/adoption-report.md`
prints nothing and `tests/test_prose.lua` lists both. dev-copilot: the sweep reports hits only under
`docs/superpowers/`.

**Non-goals.** Identifiers, file names, quoted upstream text, frozen bundles.

## C34 — Combat-time preview and profile edge cases

**Target.**
- **AbsorbTracker (AT-07):** `NS.RelockForCombat()` is the one re-lock; `OnEnterCombat`, the end of
  `StandUp` and the running path of `OnEnable` call it when in combat, so `/at enable` or a `/reload`
  mid-combat on an unlocked profile re-locks once and shows live data.
- **PartyFrameEnhanced (PF-02):** the `PROFILE` receiver, in combat with an incoming unlocked profile,
  stores `locked = true` and prints the existing combat re-lock line instead of turning preview on.

**Acceptance.** AT: `grep -n 'RelockForCombat' core/AbsorbTracker.lua core/Lifecycle.lua` shows the
definition and three call sites. PF: the two new cases are red on the parent commit and green after.

**Non-goals.** New event registrations.

## C35 — AbsorbTracker: perf test fidelity and UX

**Target.** `NS.Timer.__doRepaint` is a test seam (no production caller). `tests/perf.lua` has `paintBars`
and `repaintPass`, and `probeOverheadOff`/`probeOverheadOn` run the shipped `doRepaint`;
`PROBE_OFF_BYTES_CEILING` is re-derived by its documented method (AT-01). The Master-scale drift is
recorded as smoke S-05 and a Known Limitation, with no code change (AT-09).

**Acceptance.** `lua tests/perf.lua` exits 0 and prints the four scenario rows;
`grep -n 'paintPass' tests/perf.lua docs/performance.md` prints nothing;
`grep -n 'Master scale' docs/smoke-tests.md docs/ARCHITECTURE.md` hits both.

**Non-goals.** The stored-shape change (C-6) for Master scale, designed only if the owner confirms S-05.

## C36 — AuraMaster: packaging

**Target.** `.pkgmeta` ignores `.claude` (a live line, not commented out) and `media/screenshots`, matching
the other ten addons (AM-10).

**Acceptance.** `grep -n '^  - .claude' .pkgmeta` and `grep -n '^  - media/screenshots' .pkgmeta` hit; the
packaging checks report no unaccounted or unignored path.

**Non-goals.** AuraMaster's ratified unit-swap deviation (`AM-A-10`). A template change upstream.

## C37 — BankLedger: browser search and repaint

**Target.** A file-local `searchClause` trims the query the same way the suggestions do, and the box keeps
the raw text. A shared `dropFilterDebounce` stops `ApplyView` re-running the filter 0.2 s later. `SelectTab`
skips the redundant refresh on a real tab switch (BL-02).

**Acceptance.** `grep -n 'local function searchClause\|local function dropFilterDebounce' modules/Browser.lua`
(or, after BL-03, `modules/Browser_Views.lua`) hits; the new cases are in `docs/test-cases.md`.

**Non-goals.** The backfill budget starvation (`BL-R-06`, not addressed).

## C38 — ConsumableMaster: correctness, data seeds and recompute cost

**Target.**
- **CM-01:** the macro fingerprint is trusted only when `liveBody(macroName)` still holds that body; a
  deleted or overwritten `KCM_*` macro is rewritten (queued in combat).
- **CM-02:** Devourer (`12_1480`) has an Intellect seed with a sourced secondary order (or an empty
  secondary list with a comment saying why); the seed test iterates every playable spec, not every class.
- **CM-03:** spec change runs a discovery pass for the new spec before recomputing.
- **CM-05:** `Selector.compositeRefs` delegates to `MacroManager.CompositeConfig`; one composite-config
  rule; its CCN drops below 15.
- **CM-06:** an out-of-combat bar refresh shares one `scoreCache` across flyouts; no cache outlives the
  refresh.

**Acceptance.** `grep -n 'liveBody' modules/MacroManager.lua docs/macro-manager.md`;
`grep -n '12_1480' defaults/Defaults_StatPriority.lua tests/test_defaults.lua`;
`grep -n 'seeds every playable spec' docs/test-cases.md`; `grep -n 'CompositeConfig' modules/MacroManager.lua modules/Selector.lua`;
`grep -n 'scoreCache' modules/MacroBar.lua modules/MacroBarFlyout.lua`. SG.

**Non-goals.** Quoting a byte figure for CM-06 from the mock.

## C39 — KickCD: cast bar, glow gate and lint

**Target.**
- **KC-01:** `OnGridLayout` caches `primaryIcon` verbatim, nil included, so an empty grid anchors the cast
  bar to the grid frame.
- **KC-03:** the `target_casting` glow trigger means any cast by the unit; the gate compares three scalars,
  so a friendly cast flips it.
- **KC-07:** `.luacheckrc` `read_globals` keeps only names a linted file reads bare.

**Acceptance.** `grep -n 'primaryIcon ~= nil' modules/Castbar_Events.lua` prints nothing;
`grep -nE 'UIDropDownMenu_AddButton|GameFontDisable' .luacheckrc` prints nothing and no `files["tests/"]`
stanza was added; `luacheck .` is 0/0. SG.

**Non-goals.** The Cooldowns rebuild on slider ticks (`KC-R-06`) and new default spell lists
(`KC-R-07`).

## C40 — LootHistory: ledger correctness, perf and architecture

**Target.**
- **LH-03:** `PLAYER_REGEN_ENABLED` is handled before the Perf bracket opens; `ledgerEvent` holds only dirty
  bits and debounces.
- **LH-05:** `AnalyticsCharts.lua` publishes `NS.Analytics` idempotently (C05 covers its TOC line).
- **LH-06:** `TimelineModel` uses `NS.Ledger.LocationHolder`; no private `sideOf`.
- **LH-15:** Known limitations records the auction-exit labeling (counts correct, reasons wrong; the fix
  needs a schema change).
- **LH-STD:** the 24 LED-P2 checks in `docs/smoke-tests.md` are listed in `06_SMOKE_TESTS.md` as the owner's
  release gate for 1.4.0; no agent writes a Result.

**Acceptance.** `grep -n 'local function sideOf' modules/TimelineModel.lua` prints nothing;
`grep -n 'AH_SOLD' docs/ARCHITECTURE.md` hits under Known limitations; the new perf case passes;
`git diff --stat master..HEAD -- docs/smoke-tests.md` shows no LED-P2 Result edit.

**Non-goals.** Pruning `R.recent` (`LH-R-07`). The escrow schema change. Touching
`modules/AttributionOut.lua`'s LED-P2-06 comment before the owner's pass.

## C41 — MultiMeters: pet merge, roster cost and dead code

**Target.**
- **MM-01:** with Merge pets on, an owner's own figures add to a pet-seeded cell (total and rate summed
  under `foldPet`'s guards); a refused guard is counted, never approximated; owner-before-pet order is
  unchanged.
- **MM-03:** `Roster.BeginPass()` arms one retry of a partial roster per aggregate pass.
- **MM-04:** renaming a window to a different case of its own name keeps the name.
- **MM-05:** conformance "Disabled 8" also drives the RightButton menu: only Enabled clickable, nothing
  written, nothing shown.
- **MM-06:** the retired drill-down Back button machinery and its three tests are gone.

**Acceptance.** The `pet ahead of its owner` case is red with the Aggregator change stashed and green with
it; `grep -n 'BeginPass' modules/Roster.lua modules/Aggregator.lua docs/module-map.md` shows the
definition, one call and the doc row; `grep -n 'RightButton' tests/test_disabled.lua` hits;
`grep -rn 'BackButton\|BACK_BUTTON\|backButtons'` over live code, tests and docs prints nothing. SG.

**Non-goals.** Changing the counted-stat or deaths paths.

## C42 — PanelMaster: sanitizer and enabled-state correctness

**Target.** `REPAIR` covers `accentColor`, `accentBorderColor`, `artBlend` and `artDesaturate`;
`R.UNREPAIRED_FIELDS` lists the template keys stored as given; a property test proves every template key
is one or the other; editor reads pass the template color as fallback; lists treat `enabled == nil` as
enabled (PM-07).

**Acceptance.** `grep -n 'accentBorderColor' modules/Registry.lua` shows the REPAIR assignment;
`grep -n 'enabled ~= false' settings/Slash.lua settings/PanelEditor.lua` hits; `modules/Registry.lua` under
1000 lines (or the rules moved verbatim to `modules/RegistryRepair.lua`, loaded just before it).

**Non-goals.** Renderer changes (it already guards all four).

## C43 — PartyFrameEnhanced: secure-write queue

**Target.** `flushSecure` snapshots and clears the queue first, then runs each closure through
`xpcall(fn, geterrorhandler())`, so one raise neither orphans the rest nor skips `PublishVisibility`.
`unwrapFrame`'s re-wrap is guarded the same way. `/pfe profile new` drops the redundant
`ResetProfileCounted` (PF-01).

**Acceptance.** The new cases fail on the parent commit and pass after;
`grep -n 'ResetProfileCounted' settings/Slash.lua` shows no call in the new verb. SG.

**Non-goals.** Changing what a queued write does.

## C44 — PrettyChat cross-addon globals, settings validation and comments

**Target.**
- **LootHistory (LH-01):** the self-loot, currency and roll-won patterns record the globals they were
  compiled from and rebuild when any changes, including a global that appears after a nil first parse; the
  unchanged path allocates nothing.
- **PrettyChat (PC-01):** the schema refuses an empty or whitespace-only format with a localized reason.
- **PrettyChat (PC-02):** a stored `schemaVersion` newer than the build leaves the profile untouched (no
  prune, no restamp).
- **PrettyChat (PC-05):** comments say `_G` writes do taint but only non-protected readers see them; report
  size and addon counts no longer contradict each other.
- **PrettyChat (PC-06):** `docs/ARCHITECTURE.md` describes LootHistory's fixed behavior by symbol and cites
  the old defect once as `LootHistory@<LH-01 sha>`.

**Acceptance.** LH: four new `tests/test_util.lua` cases, each red first. PC:
`grep -n "can't be blank" locales/enUS.lua settings/Schema.lua`; `grep -n 'newer than this build' core/Database.lua`;
`! grep -n "don't taint" docs/data-flow.md`; `! grep -n 'caches its loot and currency patterns once' docs/ARCHITECTURE.md`.

**Non-goals.** A PrettyChat code change for LootHistory's sake, a bus message, or a GitHub issue. The
`1.6.0` fallback literal (`PC-R-13`).

## C45 — WhatGroup: test buttons and tooltip drift

**Target.** `RunTest` never writes `pendingInfo`. Enabled, it shows the sample through the existing preview
path as a one-shot cleared on dismiss; stood down, it prints the chat preview only and builds no frame
(WG-02). The Height tooltip and the `Frame.lua` size comment state no default figure (WG-04).

**Acceptance.** `grep -n 'pendingInfo' core/WhatGroup.lua` shows no write inside `RunTest`;
`grep -rn 'default 260\|260 is the size' settings modules locales` prints nothing. SG.

**Non-goals.** Changing Test mode's own record.

## C46 — LibKa0s: chart rendering and hover

**Target.** A2's LineChart bullet (LK-03). LootHistory pins the pane-resize render count (expected 2) in a
headless case and records it in `docs/performance.md` as a bounded cost (LH-06).

**Acceptance.** LK-03's verify (`grep -n 'CHART_MINOR = 3' LibKa0s/WidgetsLineChart.lua`; `ClipSegment`
documented). LootHistory's render-count case passes.

**Non-goals.** A library seam for the double render.

## C47 — LibKa0s: Autocomplete hooks and options

**Target.** A2's Autocomplete bullet (LK-04).

**Acceptance.** `grep -n 'AUTOCOMPLETE_MINOR = 2' LibKa0s/WidgetsAutocomplete.lua`;
`grep -n 'hooked\[' LibKa0s/WidgetsAutocomplete.lua` prints nothing; only the `12.1.4.3.2` Widgets
document and members file exist for this release.

**Non-goals.** pcalling host callbacks (`LK-R-05`, refuted).

## C48 — LibKa0s: watch-list shelf life and red-under notes

**Target.** The five band files are one automated-tests-§4 register row with triggers, and `RESULTS.md`
points at it (LK-09). The widget suites carry `-- red under:` notes on their key negatives (LK-10).

**Acceptance.** `grep -n 'automated-tests-§4' CLAUDE.md` shows the row;
`grep -n 'LK-ATS-01\|issues/32' docs/automated-tests/RESULTS.md` prints nothing in the band rows; each
file's LOC is below its trigger; `grep -c 'red under'` is above 0 in each widget suite.

**Non-goals.** Peeling any band file now.

## C49 — WowAddonStandards: roster links and mechanical gate

**Target.** The roster is single-sourced with plain Folder text (WS-02). `scripts/check-standard.sh` exists
and exits 0 (WS-10).

**Acceptance.** `grep -c '](../../' standards/ADDONS.md` is 0. `bash scripts/check-standard.sh; echo $?`
prints 0; `git check-attr eol -- scripts/check-standard.sh` reads `lf`; `test -x scripts/check-standard.sh`;
in a scratch clone each of the seven injected defects makes it exit non-zero naming its check.

**Non-goals.** A commit hook.

## C50 — dev-copilot: `ka0s-bounded` runner and bounded-runs hook

**Target.** A3's hook and runner bullets (DC-01, DC-02, DC-03).

**Acceptance.** A3's `bounded_runs` assertion and timeout check; also
`b.check('sh -c "luacheck ."','/tmp')==['luacheck']`, `b.check("bash -c 'grep lizard x'",'/tmp')==[]` and
`b.check('ulimit -v unlimited; luacheck .','/tmp')==['luacheck']`; a test run leaves no new `/tmp/tmp*`
directory.

**Non-goals.** Rewriting the matcher as a shell parser.

## C51 — dev-copilot: stale docs after the rename

**Target.** A3's docs bullet (DC-07, DC-13) and the cross-addon baseline measured at review time (DC-10).

**Acceptance.** `! grep -rn 'WowAddonStandards, wow-addon' agents commands README.md`; the two manifest
descriptions are byte-identical and contain "tooling"; `! grep -n 'v1\.56\.0' profiles/wow/agent-review.md`;
`! grep -n '61 tracked\|62 tracked\|43 Markdown\|44 Markdown' DEPENDENCIES.md`; every `path:N` in
`DEPENDENCIES.md` resolves to a non-blank line.

**Non-goals.** Removing the README migration note.

## C52 — dev-copilot: line-ending hook safety and tests

**Target.** A3's line-ending bullet (DC-04, DC-05).

**Acceptance.** `python3 scripts/test_normalize_eol.py` passes with no expected failures;
`git ls-files -s scripts/test_normalize_eol.py` shows mode 100755; `grep -n 'readlink -f' scripts/normalize-eol.sh`
hits.

**Non-goals.** Changing which files the hook acts on.

## C53 — dev-copilot: command correctness

**Target.** A3's specs bullet (DC-08, DC-10, DC-11) and the remote cleanup (DC-14).

**Acceptance.** The four `- **`all`** →` bullets are identical (`sort -u | wc -l` is 1) and
`! grep -rn 'wow-addon' profiles/wow/`; `! grep -n '/tmp/roots.txt' profiles/wow/agent-review.md`;
`grep -n '^allowed-tools:.*Edit' commands/wow-new-addon.md`; `! grep -rn 'pull --ff-only' commands/finalize.md profiles/wow/finalize.md`;
A3's `origin/main` check after finalize.

**Non-goals.** Touching `master` or any ref other than `origin/main`.

---

# Part D — the standards-reference roll and docs sync (`<AB>-STD`)

**Target.** Each addon closes on one `<AB>-STD` item, after WS-11 and after its own last M3 item:
- **The three-place reference** (TOC `## X-Standard`, README Standard badge, `CLAUDE.md` "Standards
  compliance") takes the form v2.77.0 prescribes, read from WowAddonStandards' feature branch
  (`head -1 ../WowAddonStandards/standards/STANDARDS.md`), following the local
  `/dev-copilot:wow-revendor-standards` procedure. All eleven are version-free today and stay version-free
  unless v2.77.0 requires a stamp; all eleven take the same form. The roll lands with the owner's merge
  (OWNER_SCOPE item 5).
- **The sweep:** no live doc or comment carries retired notation, a retired file name or a `filename-§N`
  reference that does not resolve against v2.77.0. Restatements of the rules this run changed match the
  new text (line-endings carve-outs, toc-file-§5, documentation-§3/§6/§8, versioning-git,
  events-frames-taint-§8). Code-comment citations are corrected comment-only. Historical "standard vX
  introduced Y" citations stay.
- **The docs sync:** `README.md`, `CLAUDE.md`, `DEPENDENCIES.md`, `docs/ARCHITECTURE.md` and the topic pages
  reflect everything the addon's RV and M3 items changed (new files, renamed seams, test counts). Smoke rows
  the run added are listed as pending owner sign-off, never marked passed.
- **Repo-specific:** AM-STD relabels AuraMaster#22 (C13). CM-STD makes `.gitattributes` match the
  client-bound §5 body. LH-STD lists the LED-P2 gate (C40).

**Acceptance (per addon).** SG holds. Every `filename-§N` citation in live docs resolves to a heading in
`../WowAddonStandards/standards/<filename>.md` on the feature branch (the revendor-standards resolver reports
zero unresolved). `grep -n 'X-Standard' <Addon>.toc` matches the form the other ten use. No version
changes: the TOC `## Version`, the README Version History and `CHANGELOG.md` gain nothing.
`git diff master --stat` shows no `libs/` or `tests/_kit/` change outside the RV commit.

**Non-goals.** A version bump, a release, a CHANGELOG release section, or an automated-test release bundle.

---

# Part E — explicitly out of scope for the whole run

- **The 39 `no` verdicts** (27 real but not worth changing, 12 refuted), listed in
  `01_CONSOLIDATED_FINDINGS.md`. Nothing is done for them (OWNER_SCOPE item 1).
- **In-client verification as a claim.** Every in-client check is an instruction to the owner, recorded in
  `06_SMOKE_TESTS.md`. No agent records a result or marks a check passed.
- **Any behavior change not traced to a finding**, except the four C27 consistency items the plan review
  added (BL-05, CM-09, PF-06, WG-07).
- **Editing frozen bundles:** audits, reviews, automated-test runs, perf-analysis runs, re-vendor bundles,
  `docs/superpowers/`, `docs/investigations/`, `harvests/`, `standards/_raw/`.
- **Patching `libs/` or `tests/_kit/`** in any addon, for any reason.
- **Any release other than LibKa0s v1.71.0** (local tag), together with the standard v2.77.0. No addon is
  version-bumped or tagged. dev-copilot keeps 2.0.1.
- **GitHub writes** other than the relabels and comments C13 names and LibKa0s#43's close. No new issue,
  including for declined adoption candidates.
- **Merging, pushing a tag or deleting `origin/main`** without the owner's go-ahead.

---

# Part F — collection-wide invariants

These hold at every committed point, not only at the end.

1. **Every repo is green at every commit.** Each repo's `CLAUDE.md` gate passes at every commit: in the
   twelve Lua repos, `luacheck .` 0/0 and `lua tests/run.lua` 0 failed, and `tests/perf.lua` exits 0
   wherever one ships; in WowAddonStandards, `check-standard.sh` exits 0 from WS-10 on; in dev-copilot, its
   Python suites and `check_overlays.py`. A red-first case and its fix land in the same commit. The RV
   commit ends green too (Part B).
2. **No function above CCN 15.** In every Lua repo the sighted complexity suite reports 0 warnings and 0
   blind files once its C16 items have landed. AuraMaster, BankLedger and LootHistory reach that during M3;
   every other repo holds it throughout.
3. **The 1500-line cap.** No authored `.lua` file in any repo is over 1500 lines.
4. **Every addon is on LibKa0s v1.71.0, byte-identical to the local tag**, with `Kit.VERSION` 38 and the
   provenance line naming v1.71.0, all moved in one commit.
5. **No local edits under `libs/` or `tests/_kit/`.** After each addon's RV commit,
   `git log --format=%H <RV-commit>..HEAD -- libs/ tests/_kit/` is empty. A defect there is fixed upstream
   as v1.71.1 (local) and re-vendored. The v1.71.0 tag never moves once copied.
6. **Every addon references standard v2.77.0** in its three places in the form the standard prescribes,
   from its `<AB>-STD` commit on.
7. **A minor bump is not complete without its API document.** In LibKa0s, `tests/test_versioning.lua` stays
   red until the document, members json and CHANGELOG versions line agree with `lib.MODULES`.
8. **Generated records match the tree.** `docs/test-cases.md` equals `lua tests/run.lua --list` and the
   README badge equals its Total, in the same commit as any case-count or case-name change.
9. **Frozen bundles are evidence and are never edited.** A misstatement is corrected in the next bundle.
10. **US English** in authored prose and player-facing strings, with the standing exemptions for verbatim
    Blizzard and third-party symbols.
11. **Present-tense cross-repo citations name a symbol or heading; historical ones pin a sha.** Every
    count claim names its members or the command that produced it.
12. **Git is the only state.** Every commit subject starts `<ITEM-ID>: ` (several ids joined with ` + `;
    an intermediate commit of a two-commit item uses `<ID> (1/2): `). Items with no commit have an
    `exceptions.tsv` row with a proof command. Each item's independent review is a `refs/notes/ka0s-review`
    note.
13. **Branches and publication.** Every touched repo works on `feat/2026-10-07-review-audit-remediation`.
    Feature branches and review notes are pushed at milestone checkpoints. Nothing is merged to
    `master`/`main`, and the `v1.71.0` tag is not pushed, without the owner's go-ahead. GitHub writes are
    spaced. After the owner-approved merge, every branch, stash and worktree the run created is deleted.
