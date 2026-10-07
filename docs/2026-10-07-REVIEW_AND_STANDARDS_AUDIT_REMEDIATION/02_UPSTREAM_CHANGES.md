# 02 — Upstream Changes (Milestone 1)

**Every change to WowAddonStandards, LibKa0s and dev-copilot, in execution order: what changes, why,
which findings it resolves, and who consumes it.**

> **Nothing in this document has been executed yet.** No section has been amended, no minor bumped, no
> tag cut and no payload copied. Every item below is a planned change. Where this document states a
> present-tense fact about a repository, it was measured on 2026-10-07 against the working trees under
> `/mnt/d/Profile/Users/Tushar/Documents/GIT/`, each on `feat/2026-10-07-review-audit-remediation` at its
> `RA-00` commit (WowAddonStandards `63ccc5c`, LibKa0s `b263c24`, dev-copilot `d90b974`).

Item ids are the ones in `plan-data/items.json`: `WS-nn` for WowAddonStandards, `LK-nn` for LibKa0s and
`DC-nn` for dev-copilot. Milestone 2 holds the eleven re-vendors `RV-<AB>`. Milestone 3 holds the addon
items `<AB>-nn`, each repo closing on its `<AB>-STD` item (the standards-reference roll and docs sync).
The plan-review decisions behind this shape are in `plan-data/PLAN_REVIEW_RESOLUTIONS.md`. The binding
scope is `inputs/OWNER_SCOPE.md`. Finding ids, severities and verdicts come from
`01_CONSOLIDATED_FINDINGS.md`.

---

## What shapes the milestone

**One release per upstream repository.**

| Repo | From | To | Kind |
|---|---|---|---|
| WowAddonStandards | v2.76.1 (2026-10-07) | **v2.77.0** | Minor, because the amendment process changes (the changelog moves out of the index). One version for the whole run: WS-01 opens it, every later WS item appends a bullet, WS-11 closes it. |
| LibKa0s | v1.70.0 (kit revision 37) | **v1.71.0** (kit revision 38) | Minor. Additive or dead-code removal only. No `NEEDS_*` floor rises, no major is added, no member is removed. Tagged **locally**. |
| dev-copilot | 2.0.1 | **2.0.1** (no bump) | Its `CLAUDE.md` asks for a version bump only when a command or agent is added or removed. No item does either. |

**The collection starts flat.** On 2026-10-07 all eleven addons vendor LibKa0s v1.70.0 byte-identically,
for both `libs/LibKa0s/` and `tests/_kit/`, at kit revision 37, with `## Interface: 120100` everywhere
(cross-addon pass, `01_CONSOLIDATED_FINDINGS.md` suite state). One release reaches every consumer in one
re-vendor wave.

**The downstream cost is small and mostly mechanical.** Kit revision 38 changes what the `--list` Totals
table counts (LK-01), so every addon regenerates `docs/test-cases.md` in its re-vendor commit, and in the
six addons with a declared skip that regeneration is the fix for a finding. The library changes are a
non-finite-number refusal in `ParseValue`, two dead fallback rungs removed, and two widget minors used by
LootHistory and BankLedger. Nothing in v1.71.0 requires an addon code change. The standard's changes bind
addons through three routes: the TOC annotation rule (WS-04), the cross-repo citation SHOULD (WS-07) and
the standards-reference roll every addon does at its `<AB>-STD` item (WS-11).

**dev-copilot carries the only `must` findings in this milestone.** `DC-A-06` and `DC-R-02` are one bug:
the bounded-runs hook denies `command -v luacheck` and `command -v lizard`, so every audit and review run
that probes for a tool is refused (DC-01). `DC-A-05` (the audit agent skipping WowAddonStandards' real
register) was `must` in the assessment and is `should` by owner override (OWNER_SCOPE item 2).

### The three upstream repositories

| Repo | Path | Role | Consumers | How the tooling reads it |
|---|---|---|---|---|
| WowAddonStandards | `../WowAddonStandards` | The standard (`standards/`), the playbooks (`AUDIT.md`, `NEW_ADDON.md`, `AUTOMATED_TESTS.md`, `PERF_ANALYSIS.md`) and the roster (`standards/ADDONS.md`). | All eleven addons, LibKa0s, and dev-copilot's commands and agents. | The audit, review and harvest agents fetch it **from GitHub**. This run's `<AB>-STD` items and LK-12 read the **local feature branch** instead (OWNER_SCOPE item 5). |
| LibKa0s | `../LibKa0s` | Fifteen LibStub majors (`LibKa0s/`) and the shared test kit (`testkit/`), vendored whole into every addon. | All eleven addons. | Re-vendors copy from the **local** `v1.71.0` tag, never from the working tree. |
| dev-copilot | `../dev-copilot` | The Claude Code plugin behind `/dev-copilot:*`: commands, agents, WoW profile overlays, hooks, `ka0s-bounded`. | Every session. | Installed from the GitHub marketplace: `dev-copilot@dev-copilot` 2.0.1 at `984cd1d`, cached under `~/.claude/plugins/cache/`. `~/.claude/dev-copilot/bin/ka0s-bounded` is a symlink **into that cache**, not into the sibling checkout. |

The last column decides the release mechanics at the end of this document. A change to WowAddonStandards
or dev-copilot is invisible to the installed tooling until it is merged, pushed and, for dev-copilot, the
plugin is updated.

### Milestone 1 at a glance

| Group | Items | Effort (S/M/L) | Findings resolved | Severity after (medium/low/info) | Needs (must/should/optional) | Raised in another repo | Clusters touched |
|---|---|---|---|---|---|---|---|
| WowAddonStandards | WS-01 … WS-11 | 5 / 5 / 1 | 38 | 6 / 28 / 4 | 0 / 22 / 16 | 9 (AbsorbTracker 2, LibKa0s 2, dev-copilot 3, WhatGroup 1, PrettyChat 1) | C04, C05, C06, C08, C11, C12, C15, C20, C32, C49 |
| LibKa0s | LK-01 … LK-12 | 8 / 4 / 0 | 19 | 0 / 15 / 4 | 0 / 10 / 9 | 3 (AuraMaster, WhatGroup, AbsorbTracker) | C01, C07, C13, C18, C19, C20, C25, C26, C27, C30, C33, C46, C47, C48 |
| dev-copilot | DC-01 … DC-15 | 9 / 6 / 0 | 27 | 8 / 17 / 2 | 2 / 17 / 8 | 1 (WowAddonStandards) | C04, C06, C11, C33, C50, C51, C52, C53 |
| **Total** | **38** | 22 / 15 / 1 | **84** | 14 / 60 / 10 | 2 / 49 / 33 | 13 | |

The 84 are a third of the 251 in-scope findings. Two items resolve no finding: WS-11 (closes the standard
release) and LK-12 (cuts the library release). Two land with no commit and are recorded in
`exceptions.tsv`: LK-11 (GitHub labels only) and DC-14 (deferred to the owner-approved finalize).

---

## Execution order, and the dependencies between the three repos

### Cross-repo dependencies

The standard is written first and the library and plugin follow it. Six edges cross a repo boundary:

| Item | Waits on | Why |
|---|---|---|
| LK-07 (live-doc citations in LibKa0s `CLAUDE.md`) | **WS-07** | It rewrites cross-repo plan ids into the citation form WS-07 defines. |
| LK-12 (cut v1.71.0) | **WS-11** | LibKa0s's README standard pointer moves to the version the standard's feature branch carries, which must be the closed v2.77.0. |
| DC-09 (rotted worked examples in specs) | **WS-07** | It converts examples to WS-07's symbol/heading or `Repo@sha:path:line` form. |
| DC-15 (audit agent and spec handoffs) | **WS-01, WS-03, WS-10, WS-11** | It restates four facts the standard changes (the changelog's new home, check (e)'s quoting, `check-standard.sh`, the version) and reads only the closed v2.77.0. |

No WowAddonStandards item depends on a LibKa0s or dev-copilot item. Inside each repo, `depends_on` gives a
valid order. The milestone runs on hard dependencies, so the three repos proceed in parallel until an
edge above blocks.

### The order

1. **WowAddonStandards:** WS-01 opens v2.77.0. WS-02, WS-03, WS-04, WS-06 and WS-09 follow it in any
   order. WS-05 needs WS-03. WS-07 and WS-08 need WS-05. WS-10 needs WS-02 … WS-09. WS-11 closes the
   entry after WS-10.
2. **LibKa0s:** LK-01 first (it opens the `## v1.71.0 — unreleased` CHANGELOG block and the kit 38 doc).
   LK-02, LK-03, LK-05, LK-06 after LK-01. LK-04 after LK-03 (same Widgets document). LK-07 after LK-01 and
   WS-07, then LK-08, then LK-09 (also after LK-06). LK-10 after LK-03 and LK-04. LK-11 is free. LK-12
   last, after every LK item and WS-11.
3. **dev-copilot:** DC-01, DC-03, DC-04 and DC-14 are free. DC-02 after DC-01, DC-05 after DC-04. DC-06
   after DC-01, DC-03 and DC-05 (its Module Map describes the fixed scripts). DC-07 after DC-06, then
   DC-08 and DC-11. DC-09 after DC-06 and WS-07, then DC-10. DC-15 after DC-06, DC-07 and the four WS
   items above. DC-12 after DC-06 … DC-11 and DC-15. DC-13 last, after DC-12.
4. No addon repo is touched until Milestone 1 is complete. Every `RV-<AB>` depends on LK-12's local tag.
   Every `<AB>-STD` depends on WS-11.

**Critical path (9 items):** WS-01 → WS-03 → WS-05 → WS-07 → WS-10 → WS-11 → DC-15 → DC-12 → DC-13. The
LibKa0s chain (LK-01 → LK-03 → LK-04 → LK-10 → LK-12, and LK-01 → LK-07 → LK-08 → LK-09 → LK-12) joins the
WS chain at LK-07 and LK-12 and is shorter.

```
WS-01 ─┬─ WS-02 ─────────────────────────────┐
       ├─ WS-03 ── WS-05 ─┬─ WS-07 ──────────┤
       │                  └─ WS-08 ──────────┤
       ├─ WS-04 ─────────────────────────────┼─ WS-10 ── WS-11 ─┬─ LK-12
       ├─ WS-06 ─────────────────────────────┤                  └─ DC-15
       └─ WS-09 ─────────────────────────────┘
LK-01 ─┬─ LK-02 ────────────────────────────────────────────────┐
       ├─ LK-03 ── LK-04 ── LK-10 ──────────────────────────────┤
       ├─ LK-05 ────────────────────────────────────────────────┤
       ├─ LK-06 ──────────────────────────┐                     ├─ LK-12 (also WS-11)
       └─ LK-07 (also WS-07) ── LK-08 ── LK-09 ─────────────────┤
LK-11 (free, no commit) ────────────────────────────────────────┘
DC-01 ── DC-02          DC-04 ── DC-05          DC-03          DC-14 (free, deferred)
DC-01 + DC-03 + DC-05 ── DC-06 ─┬─ DC-07 ─┬─ DC-08
                                │         └─ DC-11
                                └─ DC-09 (also WS-07) ── DC-10
DC-06 + DC-07 + WS-01 + WS-03 + WS-10 + WS-11 ── DC-15
DC-06 … DC-11 + DC-15 ── DC-12 ── DC-13
```

---

# Group A — WowAddonStandards (v2.76.1 → v2.77.0)

Path: `../WowAddonStandards`. Documents plus, after WS-10, one shell script. LF repository. Every item
appends one bullet to the single v2.77.0 changelog entry. Nobody bumps the version a second time.

**Blast radius for the whole group.** The standard binds all eleven addons, LibKa0s and dev-copilot. A
ruling changes nothing in an addon until that addon applies it, so each item's cost is its consumer
follow-ups, named per item below. The audit, review and harvest agents read the standard from GitHub, so
until the owner merges this branch they still grade against v2.76.1. The addon `<AB>-STD` items in this
run do not wait for that merge: they read the local feature branch, and their roll lands with the merge
(OWNER_SCOPE item 5).

---

## WS-01 · Open v2.77.0: move the changelog history out of the index into `standards/CHANGELOG.md`

**Resolves (5, cluster C12):** `WAS-R-03` (medium, the index is 92% changelog and grows every release),
`WAS-A-18` (changelog out of order), `WAS-R-12` and `WAS-A-13` (malformed `preview-mode-§` and
`automated-tests-§?` references, a wrong item pointer), `WAS-R-07` (the footer's authority date is three
releases stale).

**Why.** `standards/STANDARDS.md` is 418,659 bytes, of which 384,409 are 99 changelog entries. Every audit,
review and harvest run reads the index, so every run pays for the history. The assessment marked the move
"owner decision required". OWNER_SCOPE item 1 puts `WAS-R-03` in scope and the session lead decides the
shape here.

**Change.**
- New `standards/CHANGELOG.md`: a one-line header, one sentence saying the index carries only the current
  entry and this file carries every earlier one, newest first, then the 99 entries now at
  `STANDARDS.md:99-253` (v2.76.1 … v1.0.0) moved verbatim with exactly three edits: v2.19.0 sits above
  v2.18.0, `preview-mode-§` becomes `preview-mode`, `automated-tests-§?` becomes `automated-tests-§3`.
- `standards/STANDARDS.md`: title `(v2.77.0, <landing date>)`. `## Changelog` keeps only the v2.77.0
  entry, whose first bullet records the move with the 418,659 → ~36 KB measurement, followed by
  `Full history: [CHANGELOG.md](CHANGELOG.md).` `CHANGELOG.md` is listed under `## Related documents`, not
  under `## Sections`, because tools follow Sections and history is not normative. The footer drops its
  date and reads `**End of index. The normative rules live in the section files linked above.**`
- Version stamps roll to v2.77.0 in `README.md` Status, `standards/EXECUTIVE_SUMMARY.md`,
  `standards/NEW_ADDON_CONTEXT.md` line 1 and `CLAUDE.md`'s "As of" line.
- The release-process wording moves to the new home in `CLAUDE.md`, `standards/README.md`, `README.md`
  section A and `docs/ARCHITECTURE.md` (Module Map and Documentation map rows). `CLAUDE.md` says in one
  clause that `standards/CHANGELOG.md` is not at a repo root, so documentation-§1/§3's root-file ban does
  not reach it.
- `documentation.md`'s Tier 1 data-flow row: `documentation-§1 item 8` becomes `item 6`.

**Consumers.** Every agent that reads the index (audit, review, harvest). The handoff to dev-copilot
(`H-01`: `agents/wow-standards-audit.md` and `commands/wow-harvest-standards.md` must point at the new
file) is DC-15, which depends on WS-01 and lands in the same merge, so no published build has one without
the other. Each addon's `<AB>-STD` reads the changelog between v2.76.1 and v2.77.0 from the new file.

**Depends on:** nothing. **Effort:** M.

---

## WS-02 · This repo keeps its own `docs/audits/` and `docs/reviews/` stores

**Resolves (5):** `WAS-A-01` (medium), `WAS-A-02`, `WAS-A-03` (cluster C04); `WAS-A-17` (info),
`WAS-R-11` (cluster C49).

**Why.** documentation-§8 applies `audit-review-history` unchanged to a documentation-and-tooling repo, and
the 2026-10-07 audit and review bundles are already committed here (`RA-00`). Seven passages still say no
audit or review is ever written into this repo, the Documentation map registers neither store, and
`DEPENDENCIES.md` hard-codes a file count the bundles broke.

**Change.**
- Rewrite `CLAUDE.md` (three passages), `docs/ARCHITECTURE.md` and `README.md` (two passages) to one
  meaning: an addon audits itself in its own repo, and this repo, being audited too, keeps its own frozen
  `docs/audits/<date>/` and `docs/reviews/<date>/` stores. `AUDIT.md`, `standards/README.md` and
  `ADDONS.md` describe addon audits and stay accurate.
- `CLAUDE.md` Layout tree gains both directories. `docs/ARCHITECTURE.md` `## Documentation map` gains one
  directory row each, modelled on the `harvests/<date>/` row.
- `DEPENDENCIES.md` drops "67 tracked files: 63 Markdown" and describes the tree by kind.
- `README.md` stops listing the eleven addons and links `standards/ADDONS.md`. `line-endings.md` says
  "every addon in ADDONS.md, plus LibKa0s" instead of enumerating them.
- `standards/ADDONS.md` Folder column becomes plain code text (no link wrapper) on all thirteen rows, so
  nothing 404s on GitHub.

**Consumers.** The audit agent's documentation lane (dev-copilot DC-15 reads this register). No addon
follow-up.

**Depends on:** WS-01. **Effort:** S.

---

## WS-03 · Line endings: the repo's own `.gitattributes` becomes the §5 body; every restatement names both carve-outs

**Resolves (8, cluster C06):** `WAS-R-01`, `WAS-A-04`, `WAS-R-02`, `WAS-A-05`, `WAS-A-06`, `WAS-A-07`
(should), `WAS-R-08` and `DC-A-14` (optional).

**Why.** v2.61.0 widened line-endings-§3 to require both `*.sh` and `*.py text eol=lf`. The standard's own
`.gitattributes` (82 lines against the canonical 85) and five whole-body restatements were never updated,
so the repo fails its own rule and its docs call a non-canonical file canonical. Check (e) splices file
names into `sh -c` script text. line-endings-§7's EOL-gate MUST is unscoped, so it binds a suite-less
documentation repo that cannot run the gate.

**Change.**
- `/.gitattributes` becomes line-endings-§5's non-client body verbatim (the second column-0
  ` ```gitattributes ` fence in `line-endings.md`), with both carve-outs and the eight-line shebang comment.
  `git add --renormalize .` stages nothing.
- The five whole-body restatements (`documentation.md` §8 line-endings row, `NEW_ADDON.md` Step 0,
  `NEW_ADDON_CONTEXT.md` checklist, `EXECUTIVE_SUMMARY.md`, `CLAUDE.md`) name both carve-outs and cite
  line-endings-§3, so the next widening cannot drift.
- Check (e) in `AUDIT.md` and `line-endings.md` passes the path as a positional argument
  (`xargs -0 -n1 sh -c '... "$1" ...' _`), never `"{}"` inside the script body.
- line-endings-§7: the EOL-gate MUST binds every repo that runs a suite (an addon, a Ka0s-owned library,
  or a documentation-and-tooling repo that has acquired one under documentation-§8). A suite-less
  documentation repo runs hand check (e) instead. documentation-§8's line-endings row says the same.

**Consumers.** dev-copilot DC-15 mirrors check (c) (both carve-outs) and check (e) (positional path) in the
audit agent. Addons: no edit unless a doc restates the body; each `<AB>-STD` sweep picks that up.

**Depends on:** WS-01. **Effort:** M.

---

## WS-04 · `toc-file-§5`: the load-bearing denominator covers every position in the listing

**Resolves (2):** `AT-A-15` (cluster C05, the root cause of the whole cluster), `AT-A-14` (cluster C11,
info).

**Why.** The rule (`toc-file.md`, the §5 MUST) covers every position in the TOC listing, but the
denominator paragraph and `AUDIT.md` step 4 narrow the check to the `# Core` block and to `*Setup.lua` plus
`core/Constants.lua`. That narrowing is why load-bearing `settings\` and `modules\` positions in
AbsorbTracker, ConsumableMaster and LootHistory went unflagged. The worked example cites
`AbsorbTracker.toc:35-42`, and the block has since moved to `:37-44`.

**Change.**
- `toc-file.md` denominator paragraph: load-bearing positions are found by reading every listed file that
  binds, reads or writes an NS member or a library major at file scope, in `modules\` and `settings\` as
  much as in the seam files. The "not by counting lines" point and the 2026-09-07 history stay. One new
  sentence: a constraint may be "below at least one of X/Y/Z", and the comment then names what resolves.
- `AUDIT.md` step 4 checks every group in the listing (`# Core`, `# Defaults`, `# Modules`, `# Settings`
  and any other) and reads every listed file for file-scope reads and writes.
- The worked example cites the block by its heading, `# Core (the LibKa0s-Env seam loads first)` in
  `AbsorbTracker.toc`.
- This clarifies an existing MUST's denominator. It adds no obligation.

**Consumers.** AbsorbTracker AT-03, ConsumableMaster CM-08 and LootHistory LH-05 annotate the positions
the wider check finds. Every later audit applies the whole-listing check to all eleven addons.

**Depends on:** WS-01. **Effort:** S.

---

## WS-05 · documentation-§3/§6/§8 and library-stack-§7 agree with themselves

**Resolves (7):** `WAS-A-14` (medium), `WAS-A-12`, `WAS-A-15`, `DC-A-15`, `LK-A-10`, `WAS-A-16`
(cluster C08); `WAS-R-06` (cluster C12).

**Why.** Duplicated lists in the documentation section have drifted apart. §6 keeps a private four-store
frozen list that disagrees with §3's, and its sweep command misses stores. §3 numbers two hub sections by
contradictory ordinals. §8 counts Module Map twice, claims to classify every section while omitting
some, and states three executable-content triggers and then only one. library-stack-§7 labels the citation
scheme `documentation-§5` (it is §6). Two Tier 2 summaries omit `perf-analysis/README.md`.

**Change (all in `documentation.md` unless noted).**
- §6 "Frozen bundles are exempt" cites §3's frozen and generated list by reference (`docs/audits/`,
  `docs/reviews/`, `docs/automated-tests/<run>/`, `docs/perf-analysis/<run>/`,
  `docs/revendor/<date>-v<tag>/`, `docs/superpowers/`, `docs/investigations/`), narrows the automated-tests
  exemption to the per-run folder (README and RESULTS stay live), adds a clause for a repo's own frozen
  stores (`harvests/`, `standards/_raw/`), and replaces the `grep --exclude-dir` sweep with a
  `git ls-files` pipeline that excludes every frozen store.
- §3: the ordinals go; the sections are named.
- §8: Module Map is counted once; the exhaustiveness claim is file-granular and any subsection not listed
  applies unchanged; localization-§1-§4 sit under "Does not apply". The executable-content row states one
  trigger: lint, testing and automated-tests are re-read when the repo tracks its first `.lua` file, and
  any other executable content (a shell or Python script, a non-Lua harness) records in `DEPENDENCIES.md`
  how it is verified. This keeps dev-copilot's Python helpers and WS-10's script out of the Lua suites
  while still requiring a recorded verification.
- `library-stack.md`: the mislabeled row splits into `documentation-§5 | Keeping docs in sync.` and
  `documentation-§6 | The filename-§N citation scheme`, and §7 gains the same "file-granular, unlisted
  subsections apply unchanged" sentence. `AUDIT.md` `documentation-§5/§6` becomes `documentation-§6`.
- `CLAUDE.md` and `EXECUTIVE_SUMMARY.md`: the Tier 2 note includes `perf-analysis/README.md`.

**Consumers.** LootHistory LH-15 (out-of-scope store list), PartyFrameEnhanced PF-05 and PrettyChat PC-07
(row labels and hub wording). WS-10's script relies on the single-trigger ruling. dev-copilot DC-06 and
DC-13 follow the "record how it is verified" ruling for its Python and shell content.

**Depends on:** WS-03. **Effort:** M.

---

## WS-06 · Retire the pre-adoption launcher and disabled-latch wording; correct the scaffold runner comment

**Resolves (2, cluster C08):** `WAS-A-08` (medium), `WAS-R-05` (medium).

**Why.** All eleven addons ship the one-object launcher and the disabled latch on LibKa0s v1.70.0, yet
`AUDIT.md`, `launcher.md` §5 and `slash-commands.md` still tell auditors to expect every addon to fail.
That primes false findings. Separately, `NEW_ADDON_CONTEXT.md`'s scaffold runner comment says a missing
suite is skipped, which is the opposite of testing-§9 and of the kit's `loadSuites`.

**Change.**
- `AUDIT.md` (two passages), `launcher.md` §5 and `slash-commands.md`'s census: the forward-looking
  sentences go; the 2026-09-16 census stays as dated, past-tense history; the post-adoption expectation is
  stated (the audit verifies the latch and the launcher and files what it finds).
- `NEW_ADDON_CONTEXT.md` runner comment moves to the `Kit.run{ suites = ... }` line and says a suite named
  but missing from disk raises (testing-§9), and a suite still being written is declared
  `{ name = ..., pending = "why" }`.

**Consumers.** Every audit run. dev-copilot DC-15 removes the same stale content from the audit agent
(`WAS-A-20`). New addons scaffolded with `/dev-copilot:wow-new-addon`.

**Depends on:** WS-01. **Effort:** S.

---

## WS-07 · documentation-§6 gains a cross-repo citation SHOULD; the rotted citations are converted

**Resolves (5, cluster C11):** `WAS-A-09`, `WAS-A-10`, `LK-A-08` (should); `WAS-A-11`, `WAS-R-09`
(optional).

**Why.** Of the standard's 61 cross-repo `file:line` citations, 12 still match, 43 have moved and 6 name
files or lines that no longer exist (2026-10-07 audit, `03_EVIDENCE.md` E5). Present-tense counts ("Ten
addons ship the re-vendor store", "Five addons ship a private `core/LSMPatch.lua`") rot the same way.
Refreshing the numbers would rot again on the next release.

**Change.**
- New SHOULD in documentation-§6: a present-tense claim about another repo's code cites `Repo path` plus a
  symbol or heading, never a bare line number. A historical claim pins the commit,
  `Repo@<sha>:path:line`. A present-tense count or inventory is written as a rule ("every addon …") or
  dated ("as measured on 2026-10-07").
- Every E5 citation that no longer matches is converted to symbol or heading form or SHA-pinned. The six
  gone claims are past-tensed or deleted (for example `MultiMeters/settings/Schema.lua:1553-1566` and the
  `LSMPatch.lua` claim).
- `AUDIT.md` and `standalone-windows.md` cite BankLedger's `B:MakeCloseButton` by symbol.
- Present-tense counts become rules or are dated, without a full recount: PrettyChat's splitter
  (`tools/split_globalstrings.py`) retires as a known instance, `EXECUTIVE_SUMMARY.md`'s "the eight addons"
  becomes "every addon in ADDONS.md", and so on through `audit-review-history.md`, `AUDIT.md`,
  `documentation.md`, `library-stack.md`, `open-evolutions.md` and `options-ui.md`.
- `testing.md`: "revision 24 ships today" becomes "revision 24 and later ship this", and `tests/_kit/` is
  described as vendored whole and never edited, not as a 4-of-22 file list (also in
  `NEW_ADDON_CONTEXT.md`).
- `library-stack.md` Inter-module dependencies cites the Options → Pool floor by symbol (`NEEDS_POOL`) and
  names all three attach files: `OptionsWidgets.lua`, `OptionsTabs.lua`, `OptionsNav.lua`.

**Consumers.** The rule binds every repo's live docs. Items that write citations in the new form:
LibKa0s LK-07; dev-copilot DC-09; AbsorbTracker AT-09; ConsumableMaster CM-07; KickCD KC-09; LootHistory
LH-05, LH-16; PrettyChat PC-06; WhatGroup WG-06. Every `<AB>-STD` sweep applies it to what remains.

**Depends on:** WS-05. **Effort:** L.

---

## WS-08 · versioning-git matches how the collection works: default-branch work, owner-directed or multi-repo feature branches

**Resolves (1, cluster C32):** `DC-A-16` (should). Makes `DC-A-12` moot (it stays in the "not addressed"
list; no per-repo deviation rows are filed).

**Why.** `versioning-git.md` requires trunk-based work and allows a branch only when the human explicitly
asks. WowAddonStandards' own `CLAUDE.md` uses a looser trigger, and dev-copilot, this repo and
`/dev-copilot:finalize` all make same-named `feat/<date>-<topic>` branches merged `--no-ff` and then
deleted. One stale rule causes the disagreement.

**Change.**
- `versioning-git.md`: work lands on the repo's default branch by default. A changeset the owner directs
  to be isolated, or one that spans several repos, goes on `feat/<YYYY-MM-DD>-<topic>`, the same name in
  every repo it touches, merged into the default branch with `--no-ff` and then deleted (with any worktree
  or stash the run created). Merging, tagging, pushing and releasing keep their owner gates; pushing a
  feature branch at an owner-authorized checkpoint is the sanctioned exception to "never push unless
  asked". The wording is repo-kind-neutral because documentation-§8 and library-stack-§7 bind the section
  to all three kinds.
- Ripple: the `STANDARDS.md` Sections blurb, anti-pattern #21 (number unchanged, range stays #1–#92),
  `NEW_ADDON_CONTEXT.md` git rule 23 and its anti-pattern line, documentation-§8's versioning-git row,
  library-stack-§7's row if it says trunk, and `CLAUDE.md`'s Git workflow.

**Consumers.** Every repo's `CLAUDE.md` that restates the branch rule; each `<AB>-STD` sweep aligns it.
dev-copilot needs no deviation row.

**Depends on:** WS-05. **Effort:** S.

---

## WS-09 · events-frames-taint-§8 names the spell-cooldown fields; open-evolutions records the stub-burden question

**Resolves (2):** `WG-R-08` (cluster C20, should), `PC-R-08` (cluster C15, optional).

**Why.** WhatGroup's teleport-cooldown reader compares and subtracts `C_Spell.GetSpellCooldown`'s
`startTime` and `duration`, which are secret in combat. §8's named-API trigger set does not list those
fields, so an author reading the list does not see the hazard. Separately, PrettyChat carries about 758
lines of library-absent stubs for an install packaging cannot produce; whether an adopted major needs a full
stub is an open design question (U-3 in the audits).

**Change.**
- `events-frames-taint.md` §8 trigger set gains `C_Spell.GetSpellCooldown`'s `startTime` / `duration` /
  `modRate` and `C_Spell.GetSpellCooldownDuration`'s `:GetRemainingDuration()`, and the §8 intro names
  spell cooldowns among its examples. One sentence notes that the "never compare a secret" MUST already
  covers comparison defects independently of the list.
- `open-evolutions.md` gains an entry, "Whether an adopted major needs a full library-absent stub
  (recorded, not ruled)", cross-referencing library-stack "Ship payload vs adoption", slash-commands-§1
  and testing-§8. No rule changes.
- `testing.md`'s worked example citing `PanelMaster/settings/Slash.lua:316` takes WS-07's form.

**Consumers.** WhatGroup WG-01 (the reader fix). Every addon that reads spell cooldowns picks up the named
list at its next audit. No addon removes stubs in this run.

**Depends on:** WS-01. **Effort:** S.

---

## WS-10 · `scripts/check-standard.sh`: an on-demand mechanical gate for the standard's own invariants

**Resolves (1, cluster C49):** `WAS-R-04` (medium).

**Why.** The repo has no mechanical gate. `docs/ARCHITECTURE.md` lists "No mechanical gate" as a Known
Limitation, and this cycle's review found a class of cheap, decidable drift (CR bytes, a non-canonical
`.gitattributes`, malformed citations, stale stamps) that a script catches in seconds.

**Change.**
- New `scripts/check-standard.sh` (bash, LF through the `*.sh` carve-out, executable, `set -u`). It runs on
  demand and from `/dev-copilot:sync-docs`, never as a commit hook. Each check prints its failures; the
  script exits non-zero if any fails and 0 on a clean tree:
  1. No CR byte in any tracked file.
  2. `.gitattributes` equals line-endings-§5's LF body.
  3. Every `filename-§N` in live docs names an existing section file and an existing `### N.` heading; a
     `-§N` against an unnumbered file fails; a bare `-§` or `-§?` fails. Excluded: `harvests/`,
     `standards/_raw/`, `docs/audits/`, `docs/reviews/`, `standards/CHANGELOG.md`.
  4. `STANDARDS.md` `## Sections` links equal `git ls-files 'standards/standards/*.md'`.
  5. `anti-patterns.md` is numbered 1..N contiguously and the index blurb says (#1–#N).
  6. The title version appears in `README.md` Status, `EXECUTIVE_SUMMARY.md`, `NEW_ADDON_CONTEXT.md` line 1
     and `CLAUDE.md`'s "As of" line.
  7. Internal relative `.md` links resolve (excluding `ADDONS.md` sibling paths and frozen stores).
- `DEPENDENCIES.md` gains bash and coreutils/grep/awk with a Verify column, says "one on-demand check
  script", and its setup check runs the script. `docs/ARCHITECTURE.md` gains a Module Map row and rewrites
  the two Known Limitations to what is now covered and what is not (semantic contradictions, wrong but
  in-range citations). `CLAUDE.md`: run the script before committing a change to the standard; the Layout
  tree gains `scripts/`. Under WS-05's ruling a `.sh` file does not pull in the Lua suites;
  `DEPENDENCIES.md` records how the script is verified.

**Consumers.** WowAddonStandards itself (WS-11 gates on it). dev-copilot DC-15 makes the `kind=standards`
sync-docs overlay run it and treat a non-zero exit as drift to fix.

**Depends on:** WS-02 … WS-09. **Effort:** M.

---

## WS-11 · Close v2.77.0: ripple every change; finish the changelog entry; gate on `check-standard.sh`

**Resolves:** no finding. This is the release item `CLAUDE.md`'s Editing rules require.

**Change.**
- `STANDARDS.md` Sections blurbs are re-read against WS-03 (line-endings §7 scope), WS-04 (toc-file
  whole-listing denominator), WS-05/WS-07 (documentation), WS-08 (versioning-git) and WS-09
  (events-frames-taint). The anti-pattern range stays (#1–#92).
- `EXECUTIVE_SUMMARY.md` and `NEW_ADDON_CONTEXT.md` restate every rule WS-02 … WS-09 touched consistently:
  the git rule, the carve-outs, the kit tree, the runner comment, the citation form.
- The playbooks (`AUDIT.md`, `NEW_ADDON.md`, `AUTOMATED_TESTS.md`, `PERF_ANALYSIS.md`) match wherever a
  step restates a changed rule. `README.md` and `standards/README.md` name the changelog location,
  `scripts/` in Layout, and Status v2.77.0.
- The v2.77.0 entry is finalized: lead paragraph, one bullet per WS item with its finding ids, and the
  addon-side follow-ups this version licenses (toc-file-§5 annotations; versioning-git makes `DC-A-12`
  moot; every addon's standards reference rolls to v2.77.0).
- The header date is set to the landing date and all five stamps agree. `bash scripts/check-standard.sh`
  exits 0.

**Consumers.** LibKa0s LK-12 (README pointer), dev-copilot DC-15 (README pointer and spec handoffs), and
the eleven `<AB>-STD` items, which roll each addon's three-place reference to v2.77.0 read from this
branch. Nothing is tagged. The branch is pushed at the M1 checkpoint and merged only on the owner's
go-ahead.

**Depends on:** WS-10. **Effort:** M.

---

# Group B — LibKa0s (v1.70.0 → v1.71.0, kit 37 → 38)

Path: `../LibKa0s`. Every item that moves a file minor follows `docs/releasing.md` steps 2-5: it updates
the open `## v1.71.0 — unreleased` version block (`tests/test_versioning.lua` compares it with
`lib.MODULES`), writes `docs/api/<Major>/version-<new key>-docs.md` from the current one (Status Current,
Supersedes, "What changed at this version", Since on every new or changed member), marks the old one
Superseded, adds the `docs/api/README.md` row and runs `lua tools/gen-api-members.lua`. A major already
moved earlier in this release has an unreleased document; the later item `git mv`s and extends it rather
than writing a second one. Every item regenerates `docs/test-cases.md` with `lua tests/run.lua --list`
(CRLF, per its banner) and keeps `diff -r testkit tests/_kit` empty.

### What v1.71.0 ships

| File / surface | v1.70.0 | v1.71.0 | Item |
|---|---|---|---|
| Test kit (`Kit.VERSION`) | 37 | **38** | LK-01, LK-02 |
| `LibKa0s/Env.lua` | minor 1 | **2** | LK-06 |
| `LibKa0s/SlashParse.lua` (`PARSE_MINOR`) | 1 | **2** | LK-05 |
| `LibKa0s/Slash.lua` (shell minor) | 19 | **20** (Slash key 19.1 → 20.2) | LK-05 |
| `LibKa0s/WidgetsLineChart.lua` (`CHART_MINOR`) | 2 | **3** | LK-03 |
| `LibKa0s/WidgetsAutocomplete.lua` (`AUTOCOMPLETE_MINOR`) | 1 | **2** (Widgets key 12.1.4.2.1 → 12.1.4.3.2) | LK-03, LK-04 |
| `LibKa0s/OptionsIdList.lua` (`IDLIST_MINOR`) | 3 | **4** (Options key moves) | LK-06 |
| Every other file | unchanged | unchanged | — |

No `NEEDS_*` floor rises, no major is added and no member is removed. New members: `ChartMath.ClipSegment`
(library) and `Kit.secret`, `Kit.isSecret`, `Kit.reveal`, `Kit.installSecretValue`, `Kit.SECRET_ERROR`
(kit only).

### Which consumers each change reaches

| Change | Reaches | Owed by the consumer |
|---|---|---|
| Kit 38 Totals (LK-01) | All eleven | Regenerate `docs/test-cases.md` in the re-vendor commit. In AbsorbTracker, BankLedger, KickCD, LootHistory, PanelMaster and PrettyChat this is the fix for a finding (Total now equals the badge). |
| `Kit.secret` (LK-02) | All eleven, opt-in | WhatGroup adopts it (WG-01). Nobody else in this run. |
| LineChart minor 3 (LK-03) | LootHistory (Timeline) | Nothing. A host still calling `ClearHover` before a repaint may keep it. |
| Autocomplete minor 2 (LK-04) | LootHistory, BankLedger | Nothing; both already set their box scripts before calling `lib.Autocomplete` (BankLedger confirms in RV-BL). |
| `ParseValue` refuses nan/inf (LK-05) | Every addon routing `/<slash> set` through Slash | Nothing. Delivered free. |
| Env and OptionsIdList rungs removed (LK-06) | All eleven | Nothing. Four addons' own library-absent `Meta` carries the same dead rung; the plan removes it as a consistency item (BL-05, CM-09, PF-06, WG-07) alongside MultiMeters MM-07 and PanelMaster PM-09. |

---

## LK-01 · Kit revision 38: `--list` Totals count only cases that run; declared skips get their own row

**Resolves (1, cluster C07):** `AM-R-03` (raised in AuraMaster's review as an upstream finding).

**Why.** `testkit/framework.lua` `renderTotals` prints `#tests`, the whole registry including declared
skips, and `renderInventory`'s preamble calls that number the pass count the badge must match. That
contradicts testing-§5 (a skip must not be folded into passed or total) and the kit's own docblock. Every
consumer with a declared skip ships an inventory Total one above its badge (KickCD 1303 vs 1302, PanelMaster
1036 vs 1035, and others). The fix belongs in one place.

**Change.** Suite rows and the runner row count registered non-skipped cases (zero rows are omitted, as
now). When N > 0 declared skips exist, a `| Skipped | N |` row prints immediately before Total. Total is the
number of registered non-skipped cases, equal to the sum of the count rows and to the badge. The preamble
says so. Skipped cases stay listed by name in their groups. `Kit.VERSION` 37 → 38. `framework.lua` stays
under 1000 lines (994 today); if the change would cross it, the three render helpers move unchanged into
`testkit/inventory.lua`. New `docs/api/testkit/version-38-docs.md` (consumer owes: re-vendor `tests/_kit`
whole and regenerate `docs/test-cases.md` in the same commit); version-37 marked Superseded. CHANGELOG opens
`## v1.71.0 — unreleased`. LibKa0s's own `docs/test-cases.md` moves its one declared skip onto the Skipped
row. No payload file changes.

**Consumers.** All eleven addons through `RV-<AB>`. It clears `AT-R-07`, `BL-A-03`, `KC-A-07`, `LH-A-13`,
`PM-R-09` and `PC-R-07` with no addon code change.

**Depends on:** nothing. **Effort:** S.

---

## LK-02 · Kit revision 38: `Kit.secret`, a shared secret-value simulator, and an opt-in `issecretvalue` installer

**Resolves (1, cluster C20):** `WG-R-09`.

**Why.** No kit mock models secret values, so every addon that needs one writes its own (MultiMeters'
`tests/mock_secrets.lua`) or, like WhatGroup, has no regression test for a secret cooldown at all.

**Change.** New `testkit/secrets.lua`, loaded once from `framework.lua` beside `asserts.lua` and
`inventory.lua`. `Kit.secret(v)` returns a wrapper whose metatable raises an error carrying the fixed marker
`secret value` (published as `Kit.SECRET_ERROR`) from every arithmetic, comparison, concatenation, length,
index and call metamethod, and from `__eq` against another wrapper. `Kit.isSecret(v)`, `Kit.reveal(v)` and
`Kit.installSecretValue()` (sets the global `issecretvalue` and returns a restore function). The registry
is one process-wide weak-keyed table. Nothing installs `issecretvalue` by default, so no consumer's
behavior changes on re-vendor. The file header states what Lua 5.1 cannot trap: a boolean test, `==`
against a non-table, and `tostring`. New suite `tests/test_kit_secrets.lua`. The kit 38 document gains the
members (Since 38).

**Consumers.** WhatGroup WG-01 (its regression cases). MultiMeters may use it in MM-02 if simpler; no local
mock is migrated in this run.

**Depends on:** LK-01. **Effort:** M.

---

## LK-03 · WidgetsLineChart minor 3: segments clipped to the plot rect, hover re-syncs on every render

**Resolves (3):** `LK-R-03` (should), `LK-R-01` (cluster C46); `LK-R-10` (cluster C26, info).

**Why.** The chart does not re-sync its hover on `SetData` or `Render`, so after a resize the crosshair
stays at the old pixel and every host must call `ClearHover` before repainting. It draws segments
unclipped, and `ChartMath.Dashes` over one far off-plot point can create an unbounded number of line
regions. The default x-axis label uses `date('%d %b')`, the C-runtime English month, and the doc does not
say so.

**Change.** `CHART_MINOR` 2 → 3. New pure `ChartMath.ClipSegment(x1, y1, x2, y2, left, bottom, right, top)`
(Liang-Barsky) beside `ChartMath.Dashes`; `drawSeries` clips every segment once before choosing solid or
dashed and skips segments wholly outside, so the region count is bounded by plot geometry. Values and
markers are untouched. `render()` resets `c.__hoverIndex` without firing `onHover`, so the armed OnUpdate
re-evaluates against the new scale next frame; with no scale it hides the crosshair. `ClearHover` stays
idempotent and is no longer required. New Widgets document documents both and adds a locale note to
`formatX`.

**Consumers.** LootHistory's Timeline (smoke after re-vendor: the crosshair re-snaps after a pane resize).
LH-06 pins the pane-resize double render (`LK-R-04`) host-side; no library seam is added for it.

**Depends on:** LK-01. **Effort:** M.

---

## LK-04 · WidgetsAutocomplete minor 2: generation-guarded re-hook, set-scripts-first precondition

**Resolves (4, cluster C47):** `LK-R-02` (should), `LK-R-07`, `LK-R-08`, `LK-R-09` (optional).

**Why.** Hooks are installed once per box behind `hooked[box] = true`, so a later host `SetScript` silently
kills the suggestion list and calling `lib.Autocomplete` again cannot restore it. The API doc never says the
host must set its scripts first. A fractional `maxRows` desynchronizes row count from list height. The
backdrop is rebuilt on every show. A comment claims weak entries are collected, which Lua 5.1 cannot do.

**Change.** `AUTOCOMPLETE_MINOR` 1 → 2. A weak-keyed per-box generation replaces the once-only guard: each
call installs fresh `HookScript` wrappers that dispatch only while their generation is current, so a
re-call after a `SetScript` restores the list and a re-call without one does not double-dispatch. The
comment is corrected. `maxRows` is floored after the > 0 check, with a fallback to `AC.MAX_ROWS` below 1.
`SetBackdrop` runs once when the list is created; colors are still applied per show. The API doc states the
set-scripts-first precondition, the re-hook, and integer `maxRows`. The Widgets document moved by LK-03 is
renamed to key `12.1.4.3.2` and extended. No kit change (`mock_base.lua` already drops hooks on
`SetScript`).

**Consumers.** LootHistory and BankLedger search boxes (smoke after re-vendor: unchanged behavior).

**Depends on:** LK-03. **Effort:** M.

---

## LK-05 · Slash key 20.2: `ParseValue` refuses nan/inf; `Slash.lua` cites the standard by section (closes #43)

**Resolves (2):** `LK-R-06` (cluster C30, should), `LK-A-06` (cluster C18, optional).

**Why.** Lua 5.1 `tonumber` accepts `nan`, `inf` and `1e999`. `parseNumber` passes them on, and on an
unbounded number row the write seam stores them; a bounded row absorbs NaN only because of argument order
in `math.max`. `Slash.lua` cites `slash-commands.md:34`, the line-number form issue #43 asked to remove.

**Change.** `SlashParse.lua` `parseNumber`: after `tonumber`, refuse `n ~= n` and `±math.huge` with the
existing `ERR_NUMBER` before the enum and clamp logic. A comment records why the clamp keeps `n` as the
second argument. `PARSE_MINOR` 1 → 2. `Slash.lua` cites `slash-commands-§1` (confirmed against the
standard); Slash shell minor 19 → 20. Slash key 19.1 → 20.2 with its document. After the commit, LibKa0s#43
is relabeled `state:done` and closed with a comment naming the sha, spaced from other GitHub writes.

**Consumers.** Every addon whose `/<slash> set` goes through Slash, free on re-vendor. ConsumableMaster
CM-04 is the host-grammar analogue for `/cm priority`; PanelMaster PM-06 is its own finiteness guard.

**Depends on:** LK-01. **Effort:** S.

---

## LK-06 · Env minor 2 and OptionsIdList minor 4: drop the dead bare-global AddOns rungs

**Resolves (1, cluster C27):** `LK-A-04`.

**Why.** `GetAddOnMetadata` and `IsAddOnLoaded` as bare globals were removed in 11.0, and every admitted
client is Interface 120100. Each rung sits behind a `C_AddOns` rung that answers first, so it is
unreachable, and `Env.lua`'s comment claims the global is "still present", contradicting the standard's
compat worked case.

**Change.** `Env.lua` `GetAddOnMetadata` answers `C_AddOns.GetAddOnMetadata` or nil; the comment says the
bare global is gone and never read. Env minor 1 → 2. `OptionsIdList.lua` `hostLoaded` reads only
`C_AddOns.IsAddOnLoaded`, trusting the name when that is absent, as today. `IDLIST_MINOR` 3 → 4. `.luacheckrc`
drops both names from `read_globals`, so luacheck proves nothing reads them. Env and Options documents
record it.

**Consumers.** All eleven, with no behavior change on any admitted client. MultiMeters MM-07, PanelMaster
PM-09 and the four consistency items BL-05, CM-09, PF-06 and WG-07 remove the same rung from each addon's
own library-absent `Meta`.

**Depends on:** LK-01. **Effort:** S.

---

## LK-07 · Live-doc drift: resolvable evidence ids in `CLAUDE.md`, no derived headroom figure, Perf stub template comments

**Resolves (3):** `LK-A-05` (cluster C25, should), `LK-A-03` (cluster C01), `AT-R-08` (cluster C19, info).

**Why.** Register rows in `CLAUDE.md` cite `LibKa0s-A-07`, `LibKa0s-A-10` and `LibKa0s-A-03`, consolidation
ids that do not resolve in this repo, and cite cross-repo plan items (`LK-29`, `LK-30`) as if they were
local. `CLAUDE.md` and `RESULTS.md` carry a derived "44 lines of room" figure that is already wrong (42).
The Perf API document's host-example comments say AbsorbTracker reads `NS.Perf.suspended`; it asks its
lifecycle latch.

**Change.** Documentation only; no minor moves. Register evidence becomes this repo's own ids (`LK-28`,
`LK-37`, `LK-17d`, each confirmed against `docs/audits/2026-09-23/`). Cross-repo plan items are qualified
with their bundle or replaced by the commit sha, in WS-07's form. The derived headroom figure goes; the
measured LOC and the 1490 trigger stay. The current Perf document (`version-14.1.1.6-docs.md`) keeps
`suspended = false` in the stub template, rewords the two AbsorbTracker comments, and adds one sentence
under host contract rule 2: a latch-based host may ask its latch.

**Consumers.** None. AbsorbTracker AT-06 is the host-side counterpart (its test asserts the latch).

**Depends on:** LK-01, WS-07. **Effort:** S.

---

## LK-08 · US-English sweep of `docs/adoption-prompt.md` and `docs/adoption-report.md`, now gated

**Resolves (1, cluster C33):** `LK-A-02`.

**Why.** Two live pages listed in `CLAUDE.md`'s Documentation map carry 22 British-spelling lines, and the
prose gate does not scan them because register row 3 treats `adoption-prompt.md` as a frozen record.

**Change.** `tests/test_prose.lua` `AUTHORED_FILES` gains both files. Both are swept to US English with the
kit's `BRITISH`/`ALLOWED` lists. Register row 3 stops listing the prompt as a record that must not be
rewritten and says its 2026-09-23 figure was measured then and the page has since been swept and gated.
`docs/adoption/` (frozen per-run bundles) is untouched.

**Consumers.** None.

**Depends on:** LK-07. **Effort:** S.

---

## LK-09 · Band watch list: the five over-shelf-life Options files become one tracked deviation row

**Resolves (1, cluster C48):** `LK-A-01`.

**Why.** automated-tests-§4 and anti-pattern #53: an entry carried as accepted across three consecutive
release runs must be fixed or converted to a tracked deviation with an id and an owner. Five 1000-1500 band
files (`OptionsWidgets.lua` 1444, `OptionsIds.lua` 1359, `OptionsTabs.lua` 1349, `Options.lua` 1288,
`OptionsIdList.lua` 1246) have been "Accepted" for seven to ten runs, and three cite closed #32 and the
finished `LK-ATS-01` as their tracker. This run opens no new GitHub issues (OWNER_SCOPE item 5), so the
tracker is a register row.

**Change.** New row in `CLAUDE.md` `## Documented deviations`: rule automated-tests-§4; the five files with
their re-measured LOC, named seam and re-check trigger (1450 for `OptionsWidgets` and `OptionsIds`, 1350
for `OptionsIdList`, next member or 1400 for `OptionsTabs` and `Options`); why (no file is over the cap,
each has a seam, and a peel is a release with eleven re-vendors); decided 2026-10-07; retired when a file
reaches its trigger or a tracker issue is opened. The register count prose moves from six rows to seven.
The five Disposition cells in `docs/automated-tests/RESULTS.md` point at the row. The band rulings in
`CLAUDE.md` point at it instead of re-arguing acceptance. If LK-03 … LK-06 pushed a file past its trigger,
it is peeled here instead (expected: none).

**Consumers.** None. LK-12's release run carries this wording in its new `RESULTS.md` row.

**Depends on:** LK-08, LK-06. **Effort:** S.

---

## LK-10 · Sampled mutation pass on the widget suites: `-- red under:` notes

**Resolves (1, cluster C48):** `LK-R-11` (optional).

**Why.** testing-§12 SHOULD: a negative case should be shown to fail under the mutation it guards. The
v1.69.0 and v1.70.0 widget suites carry no such notes.

**Change.** For the key negative and boundary cases in `test_widgets_autocomplete.lua`,
`test_widgets_linechart.lua` and `test_widgets_linechart_math.lua`, mutate the guarded line on a backup of
the payload file, confirm the case goes red, restore byte-identically and record `-- red under:
<mutation>`. A case that stays green is strengthened in the same commit. Test files only.

**Consumers.** None.

**Depends on:** LK-03, LK-04. **Effort:** S.

---

## LK-11 · Issue-store housekeeping: closed #32, #33, #37, #39 relabeled `state:done`

**Resolves (1, cluster C13):** `LK-A-07`.

**Why.** Four closed issues carry the open-only label `state:triaged`, which `/dev-copilot:issue-summary`
reports as an inconsistency.

**Change.** GitHub only, no commit: one `gh issue edit <n> --remove-label state:triaged --add-label
state:done` per issue, spaced. Recorded in `exceptions.tsv` with the proof command
`gh issue list --repo tusharsaxena/LibKa0s --state closed --label state:triaged --json number` → `[]`.

**Consumers.** None.

**Depends on:** nothing. **Effort:** S.

---

## LK-12 · Cut LibKa0s v1.71.0: version block, release run with `ANALYSIS.md`, local tag only

**Resolves:** no finding. This is the release every `RV-<AB>` copies from.

**Change.** `docs/releasing.md` steps 4-7 end to end.
- `CHANGELOG.md`: `## v1.71.0 — <date>` with the full version block from the table above, a "What a consumer
  owes" section (re-vendor both payloads whole, roll the provenance line, regenerate `docs/test-cases.md`
  in the same commit because kit 38 changes the Totals table; WhatGroup adopts `Kit.secret`; a host still
  calling `ClearHover` before a chart repaint may keep it), and the standards pointer.
- `README.md`'s standard version moves to the version WowAddonStandards' feature branch carries
  (`head -1 ../WowAddonStandards/standards/STANDARDS.md`, v2.77.0). `docs/releasing.md`'s semver and
  provenance template move to v1.71.0. `docs/api/CONSUMERS.md` is re-run because `ChartMath.ClipSegment`
  is a new surface.
- Commit `LK-12 (1/2): release v1.71.0 …` on a clean tree (the `(1/2)` keeps `resume-state.sh` from
  counting the item landed early), then `tests/_kit/run-automated-tests.sh --release 1.71.0`, then
  `ANALYSIS.md` per `AUTOMATED_TESTS.md`, the release-notes line from the manifest, and the band
  dispositions carrying LK-09's tracker wording. Final commit `LK-12: v1.71.0 release record …`.
- Tag preconditions from the manifest: release `1.71.0`, `dirty` false, lint, tests and complexity pass,
  `complexity.warnings` 0, `ANALYSIS.md` present. Then `git tag -a v1.71.0 -m 'LibKa0s v1.71.0'` on the
  final commit. **The tag is never pushed** in this run without the owner's go-ahead.
- Resume rules: a `LK-12 (1/2)` commit without a `LK-12:` commit means continue from the release run; a
  `LK-12:` commit without the tag means re-check the preconditions and tag before any `RV-` starts; an
  open LibKa0s#43 after LK-05 landed means finish LK-05's close now.

**Consumers.** All eleven `RV-<AB>` items. The owner's smoke after re-vendor: `/reload` with every Ka0s
addon enabled, no Lua errors, every settings panel and slash help opens as before.

**Depends on:** LK-01 … LK-11 and WS-11. **Effort:** M.

---

# Group C — dev-copilot (2.0.1, no version bump)

Path: `../dev-copilot`. Every item's gate is the repo's own: `test_detect_profile.py`,
`test_check_overlays.py`, `test_bounded_runs.py`, `check_overlays.py` (`OK: 13 overlays`), both manifests
parse, and from DC-04 on `test_normalize_eol.py`. No command or agent is added or removed, so
`plugin.json` stays 2.0.1.

**Blast radius.** The installed plugin is the 2.0.1 cache at `984cd1d`, and the `ka0s-bounded` symlink
this run uses points into that cache. Nothing in this group changes the tooling the run itself uses until
the owner merges dev-copilot and the plugin updates. The run keeps calling the absolute
`~/.claude/dev-copilot/bin/ka0s-bounded` path and lives with the `command -v` denial until then.

---

## DC-01 · Bounded-runs hook: stop denying `command -v` tool probes; clean up test tempdirs

**Resolves (3, cluster C50):** `DC-A-06` and `DC-R-02` (medium, **must**: one bug), `DC-R-14`
(optional).

**Why.** `scripts/bounded_runs.py`'s `strip_prefix` treats `command` as a transparent wrapper, so
`command -v luacheck` reads as a luacheck run and the hook denies it. The audit agent hit this itself
during the 2026-10-07 run. Every run that probes for a tool is refused or misdirected. The test file also
leaks a temp directory per case.

**Change.** When the word is `command` and the next is `-v` or `-V`, `strip_prefix` returns no command, so
`command -v luacheck`, `command -V lizard` and `command -v luacheck lizard` produce no check and the hook
stays silent. `command luacheck .` is still denied. The docstring notes the exception. New pass cases, a
deny case, and a hook-JSON case for `command -v luacheck lizard`. Every bare `tempfile.mkdtemp()` in the
tests goes through a helper that registers cleanup. The case count in `CLAUDE.md` and `DEPENDENCIES.md`
moves to what the runner reports.

**Consumers.** Every session, once the plugin updates. Audit and review agents stop being refused on tool
probes.

**Depends on:** nothing. **Effort:** S.

---

## DC-02 · Bounded-runs matcher: close the `ulimit -v unlimited` and `sh -c` false negatives

**Resolves (1, cluster C50):** `DC-R-13` (optional).

**Why.** The bounded-by-hand regex accepts `ulimit -v unlimited`, which bounds nothing, and a heavy command
hidden inside `bash -c '…'` is not seen.

**Change.** The regex requires a numeric limit. When a shell is invoked with an option cluster containing
`c`, the next argument is run through the same segment, prefix and heavy pipeline, recursion bounded to one
or two levels. The `run-automated-tests.sh` script-argument branch stays. Cases that must stay silent
(`bash -c 'grep lizard x'`, `bash -c 'command -v lizard'`, `bash -c 'ka0s-bounded lua tests/run.lua'`)
and cases that must deny (`sh -c "luacheck ."`, `ulimit -v unlimited; luacheck .`).

**Consumers.** Every session, once the plugin updates.

**Depends on:** DC-01. **Effort:** S.

---

## DC-03 · `ka0s-bounded`: kill the whole tree on timeout when non-interactive; recompute slots while waiting

**Resolves (2, cluster C50):** `DC-R-01` (medium, should), `DC-R-08` (optional).

**Why.** `timeout --foreground` signals only the top process, so on a timeout the forked children keep
running and keep holding the slot-pool lock while the run reports itself stopped (reproduced in the
review). The slot count is computed once from `MemAvailable` before the wait loop, so a run started under
memory pressure never takes a second slot.

**Change.** `--foreground` is added only when stdin is a terminal (keeping Ctrl-C), so non-interactive runs,
which is how Claude's Bash tool calls it, let `timeout` signal the whole process group. When
`KA0S_KIT_SLOTS` is unset, the slot count is recomputed from `MemAvailable` on every pass of the wait
loop. A new test runs `bin/ka0s-bounded bash -c 'sleep 4711 & sleep 4711; echo done'` with a 2-second
timeout and stdin from `/dev/null`, asserts rc 124 and that no `sleep 4711` survives. `DEPENDENCIES.md` and
the README Hooks section describe the conditional form.

**Consumers.** Every bounded run in every repo, once the plugin updates.

**Depends on:** nothing. **Effort:** M.

---

## DC-04 · Line-ending hook: add an automated test suite (symlink case expected red)

**Resolves (1, cluster C52):** `DC-R-06` (medium, should).

**Why.** `scripts/normalize-eol.sh` rewrites user files on every Write and Edit and has no automated test.

**Change.** New `scripts/test_normalize_eol.py` (stdlib unittest, LF, shebang, mode 100755). Each case
builds a temp git repo with a `.gitattributes`, writes a file, pipes the hook JSON in, and asserts bytes:
both eol arms, already-correct files unchanged, no eol declared, binary files, a file outside any repo, an
empty path. The symlink case (convert the target, keep the link) is decorated `expectedFailure` with a
comment naming DC-05, so the suite is green until the fix lands. `CLAUDE.md` and `DEPENDENCIES.md` list the
fourth test file.

**Consumers.** dev-copilot's own gate from this item on.

**Depends on:** nothing. **Effort:** M.

---

## DC-05 · Line-ending hook: resolve symlinks so the target is converted and the link survives

**Resolves (1, cluster C52):** `DC-R-03`.

**Why.** `perl -i` on a link path unlinks it and writes a regular file, so the link is replaced and the
target is never converted. The `[[ -f ]]` guard follows links and does not prevent this.

**Change.** Right after the empty and `-f` guards, `file_path="$(readlink -f -- "$file_path")" || exit 0`
and a fresh `-f` check, with a one-line comment, so the target's own repo and `.gitattributes` decide. The
`expectedFailure` decorator goes, and a case for a link whose target is outside any repo is added.

**Consumers.** Every session, once the plugin updates. No tracked symlink exists in the collection today.

**Depends on:** DC-04. **Effort:** S.

---

## DC-06 · Author the `docs/ARCHITECTURE.md` hub (documentation-§8 Substitutes #3)

**Resolves (3, cluster C04):** `DC-A-01`, `DC-A-02`, `DC-A-03`.

**Why.** documentation-§8 requires a documentation-and-tooling repo to carry a five-section
`docs/ARCHITECTURE.md`. dev-copilot has none, so it has no Module Map, no Documentation map and no
Documented deviations register.

**Change.** New `docs/ARCHITECTURE.md` with exactly five sections in order: Overview; Module Map (moved out
of `CLAUDE.md`'s Module/package map, updated for DC-01 … DC-05, with a callout naming the path-addressed
surfaces whose rename breaks callers: the `bin/` names, the hook script paths, the overlay names, the
`~/.claude/dev-copilot/bin/ka0s-bounded` symlink, command and agent names); Known Limitations (only real
ones: the matcher is a tokenizer, the plugin cache is a separate copy, the EOL hook acts only where
`.gitattributes` declares eol); Documentation map (root docs as rows, the `commands/`, `agents/` and
`profiles/wow/` trees as directory rows, `docs/superpowers/`, `docs/audits/<date>/` and
`docs/reviews/<date>/` as frozen stores); Documented deviations reading `None.`. `CLAUDE.md` replaces its
map with a pointer, keeping the version-SSOT and keep-LF/+x footguns as one-liners. `README.md` links the
hub. The audit agent is not edited here (DC-15).

**Consumers.** DC-15 (the audit agent reads this hub as dev-copilot's register). Every later
documentation-lane audit of dev-copilot.

**Depends on:** DC-01, DC-03, DC-05. **Effort:** M.

---

## DC-07 · Finish the wow-addon rename sweep; add the tooling kind to user-facing descriptions

**Resolves (3, cluster C51):** `DC-A-07`, `DC-R-10` (should), `DC-R-15` (optional).

**Why.** Phase 2 of the `wow-addon` → `dev-copilot` rename closed on 2026-10-04, but the audit agent's and
command's frontmatter and `README.md` still name `wow-addon` as a documentation-lane repo, `CLAUDE.md`
allowlists mentions that were already removed, and the profile lists omit the tooling kind.

**Change.** `(WowAddonStandards, wow-addon)` becomes `(WowAddonStandards, dev-copilot)` in
`agents/wow-standards-audit.md`, `commands/wow-standards-audit.md` and `README.md`. `CLAUDE.md`'s allowlist
is trimmed to what exists, "including both symlinks" becomes "including the runner symlink", and the audit
rotation bullet names dev-copilot. "tooling repos" joins the kind list in `README.md` (two places) and in
`plugins[0].description` of both `plugin.json` and `marketplace.json`, the two strings byte-identical. No
version bump.

**Consumers.** Anyone reading the plugin listing. The issue overlays' `wow-addon` clauses are DC-08's.

**Depends on:** DC-06. **Effort:** S.

---

## DC-08 · Issue commands: one shared meaning of `all` in a WoW repo

**Resolves (1, cluster C53):** `DC-R-04` (medium).

**Why.** The four issue overlays disagree on what `all` means: some take the addon table, some add the
upstreams, one still adds the archived `wow-addon`.

**Change.** One identical `- **`all`** → …` bullet in `profiles/wow/issue-audit.md`, `issue-triage.md`,
`issue-summary.md` and `issue-details.md`: every row of `standards/ADDONS.md` (the addon table, the library
table and the documentation-and-tooling table), each tagged with its kind; if `ADDONS.md` is unreachable,
sibling directories with a `.toc` plus the three known upstreams, saying the roster was inferred. The
`wow-addon` clause and scan entry go. Audit and triage run only the base sweep on upstream rows and the
addon-only checks on addon rows. `README.md` describes `all` the same way. `check_overlays.py` still passes.

**Consumers.** Every `/dev-copilot:issue-*` run with `all`.

**Depends on:** DC-07. **Effort:** M.

---

## DC-09 · Replace rotted worked examples in specs with durable citations

**Resolves (1, cluster C11):** `DC-A-09`.

**Why.** The command specs' worked examples copy the habit WS-07 fixes in the standard: LootHistory
`Compat.lua` line ranges, a dead MultiMeters `settings/Schema.lua:670` example, "seven of the eleven
repos", "five addons are permanent perf-skippers", and an `exclude_files` example that says `tests/` where
consumers exclude `tests/_kit/`.

**Change.** `commands/wow-revendor-libka0s.md` says `libs/` and `tests/_kit/`. The examples in it and in
`commands/wow-new-addon.md` take symbol or heading citations or `as of <Repo>@<sha>`; no line number is
re-derived. The MultiMeters example moves to its current home by symbol (`OptionsSetup.lua`, confirmed by
grep). The counts become rules or are dropped; the `359 hits` figure carries its command or goes.
`profiles/wow/agent-review.md` and `profiles/wow/bump-version.md` state the perf-skip rule (no
`tests/perf.lua` or `PerfSetup.lua` → perf recorded as a skip with its reason) instead of a count.

**Consumers.** Every run of those commands.

**Depends on:** DC-06, WS-07. **Effort:** M.

---

## DC-10 · Cross-addon pass: `mktemp` roots file; drop the frozen v1.56.0 baseline

**Resolves (2):** `DC-R-05` (cluster C53, medium), `DC-R-11` (cluster C51, info).

**Why.** The review agent's cross-addon pass writes a fixed shared `/tmp/roots.txt`, which breaks the
plugin's own shared-path rule when two reviews run in parallel (the 2026-10-07 audits collided on scratch
paths). Its baseline table records figures measured at v1.56.0, fourteen releases ago.

**Change.** `profiles/wow/agent-review.md` creates the roots file with `roots=$(mktemp)`, uses it in the
tee, the collision check and the evidence count, removes it afterwards, and cites the shared-path rule. The
baseline table keeps its measurement commands and drops the recorded figures and every v1.56.0 mention:
measure at review time against the tag the addons vendor.

**Consumers.** Every `/dev-copilot:review` run in a WoW addon.

**Depends on:** DC-09. **Effort:** S.

---

## DC-11 · Push-safety wording: the wow-new-addon roster step and finalize's push rejection

**Resolves (2, cluster C53):** `DC-R-07` (medium), `DC-R-12` (optional).

**Why.** `wow-new-addon` must add a row to WowAddonStandards' roster but lacks the Edit tool, and its wording
implies it may push. `finalize`'s push-rejection recovery runs `git pull --ff-only`, which can never succeed
in the state that triggers it.

**Change.** `commands/wow-new-addon.md` adds Edit to `allowed-tools` and rewrites the roster step: edit
`standards/ADDONS.md` in the sibling checkout on a feature branch and commit there, never push; if the
checkout is absent or dirty, leave it and tell the user. `commands/finalize.md` 3e: on push rejection, stop
that repo, optionally fetch and report how far `origin/<default>` moved, paste the push output, and leave
reconciliation to the user; never force, rebase or merge origin in. `profiles/wow/finalize.md` is aligned
if it repeats the pull.

**Consumers.** The next `/dev-copilot:wow-new-addon` and every `/dev-copilot:finalize`, including this
run's owner-approved finalize once the plugin updates.

**Depends on:** DC-07. **Effort:** S.

---

## DC-15 · Audit agent and spec handoffs from the standard

**Resolves (3):** `DC-A-05` (cluster C04, medium; owner override must → should), `WAS-A-20` (cluster
C04), `DC-A-10` (cluster C06).

**Why.** `agents/wow-standards-audit.md` says neither documentation repo has a `docs/ARCHITECTURE.md`, so
every documentation-lane run skips WowAddonStandards' real register (and, after DC-06, dev-copilot's). It
repeats the stale "11 of 11 addons failing" launcher census and describes the launcher by retired rung
letters. Its check (c) names only `*.sh`. And four facts it and other specs restate change in this run:
the changelog's home (WS-01), check (e)'s quoting (WS-03), `check-standard.sh` (WS-10), and the standard
version (WS-11). One commit lands them all after the standard closes, so nothing reads a half-finished
branch.

**Change.**
- `agents/wow-standards-audit.md`: (a) the documentation-lane register read is
  `docs/ARCHITECTURE.md` `## Documented deviations` in both WowAddonStandards and dev-copilot; a missing hub
  is itself a documentation-§8 finding; the GitHub issue store stays the second input; the phrase "neither
  repo has a" is gone. (b) The "expected to fail" wording and the census go; the launcher check describes
  current launcher-§2 behavior (left-click while disabled prints the refusal line and writes nothing;
  right-click opens the panel) without rung letters. (c) Check (c) names both `*.sh` and `*.py text
  eol=lf`, or defers to `AUDIT.md`. (d) Check (e) passes the path positionally, byte-for-byte WS-03's form.
  (e) The index carries the front matter, reading guide, current changelog entry and Sections; earlier
  entries live in `standards/CHANGELOG.md`, fetched only when a run needs history.
- `commands/wow-harvest-standards.md` Step 6: the new entry is written as the index's current entry and the
  previous one moves verbatim to the top of `standards/CHANGELOG.md` in the same change; the file joins
  the ripple list. Any other "changelog at the top of STANDARDS.md" wording in `commands/`, `agents/` or
  `profiles/` is aligned.
- `profiles/wow/sync-docs.md` `kind=standards`: when `scripts/check-standard.sh` exists, run it and treat a
  non-zero exit as drift to fix before writing.
- `README.md` line 3 rolls from v2.76.0 to the version the standard's feature branch reads (v2.77.0).
- `check_overlays.py` still passes. No version bump.

**Consumers.** Every `/dev-copilot:wow-standards-audit` run in the documentation lane, every
`/dev-copilot:wow-harvest-standards` run, and every `sync-docs` run in WowAddonStandards, once the plugin
updates.

**Depends on:** DC-06, DC-07, WS-01, WS-03, WS-10, WS-11. **Effort:** M.

---

## DC-12 · US-English sweep over live specs and root docs

**Resolves (1, cluster C33):** `DC-A-11` (optional).

**Why.** 37 British spellings across commands, agents, profiles, root docs and one script comment, against
localization-§5. dev-copilot has no prose gate.

**Change.** One sweep with the `BRITISH` and `ALLOWED` lists copied whole from the standard's
localization-§5 block over `CLAUDE.md`, `README.md`, `DEPENDENCIES.md`, `docs/ARCHITECTURE.md`, `agents/`,
`commands/`, `profiles/` and script comments. Step headings and output-file instructions first (for
example `commands/wow-revendor-libka0s.md`'s "Step 8 — Summarise" becomes "Summarize"). Frozen
`docs/superpowers/`, `docs/audits/` and `docs/reviews/`, identifiers, file names and quoted upstream text
are left alone. No prose-check script is added in this run.

**Consumers.** None beyond readers.

**Depends on:** DC-06 … DC-11, DC-15. **Effort:** S.

---

## DC-13 · `DEPENDENCIES.md`: command-based inventory, fresh citations, reasoned version floors

**Resolves (2, cluster C51):** `DC-A-08`, `DC-R-09`.

**Why.** `DEPENDENCIES.md` hard-codes "61 tracked files: 43 Markdown …", cites lines that have moved, and
gives version floors with no reason.

**Change.** The inventory becomes the `git ls-files` commands that produce it, with `docs/` described by
role (the hub and the frozen stores). Python files are described as modules plus one test each. Every
`path:N` in the Evidence columns is re-checked against the final tree with `sed -n`. Each floor (python3
3.8, git 2.34, perl 5.10, coreutils 8.30) gets a one-clause reason or becomes "any recent". The
`docs/superpowers/plans/2026-10-04-phase2-rename-ripple.md` plan is covered by the hub's frozen-store row.

**Consumers.** None beyond readers.

**Depends on:** DC-12. **Effort:** S.

---

## DC-14 · Delete the stale `origin/main` branch (owner go-ahead only)

**Resolves (1, cluster C53):** `DC-A-13` (info).

**Why.** `origin/main` points at `d2ed30d`, the initial commit, an ancestor of `master`. The default branch
is `master`.

**Change.** Remote-only, no commit. At the M1 checkpoint, `exceptions.tsv` gains `DC-14` with reason
"deferred to the owner-approved finalize" and the proof
`git -C ../dev-copilot ls-remote --heads origin main` (prints nothing after finalize), so `resume-state.sh`
treats M1 as complete. At finalize, with the owner's go-ahead, `git push origin --delete main` runs; if the
owner declines, the row's reason becomes "declined by owner <date>". No other ref is touched.

**Consumers.** None.

**Depends on:** nothing. **Effort:** S.

---

# Considered and not done upstream

These are recorded so the next cycle does not re-argue them.

- **A LibKa0s UTF-8 truncation helper.** KickCD KC-02 adds a file-local helper modeled on MultiMeters'
  `utf8Truncate`. Two call sites do not clear library-stack-§7's bar for a shared surface, and this release
  has no other reason to carry it.
- **Ruling the library-absent stub burden (U-3).** WS-09 records the question in `open-evolutions.md` and
  changes no rule. No addon removes stubs in this run.
- **A GitHub tracker issue for the five LibKa0s band files.** OWNER_SCOPE item 5 forbids new issue writes;
  LK-09's register row is the tracker and names the issue as its retirement trigger.
- **A library seam for the LineChart pane-resize double render (`LK-R-04`).** LootHistory LH-06 pins the
  count host-side and records it as a bounded cost.
- **Migrating MultiMeters' `tests/mock_secrets.lua` to `Kit.secret`.** It models more than the kit does.
- **A prose gate for dev-copilot.** DC-12 is a one-time sweep.
- **A full recount of the standard's present-tense counts.** WS-07 rewrites them as rules or dates them.
- **A dev-copilot version bump.** No command or agent is added or removed.
- **Findings the assessment recommends leaving** (`01_CONSOLIDATED_FINDINGS.md`, "Recommended NOT to
  address"): `WAS-A-19` (an empty register is correct), `WAS-R-10` (the "One-page TL;DR" label), `LK-A-09`
  (the standard's compat worked case is right; LK-06 fixes the library side), `DC-A-12` (moot after WS-08).
  Refuted: `DC-A-04`, `LK-R-05`. OWNER_SCOPE item 1 keeps all of them out of scope.

---

# Release mechanics

**Nothing is merged to a default branch, and no tag is pushed, without the owner's go-ahead.** At the M1
checkpoint the feature branch of each upstream repo is pushed to origin, unmerged, with
`refs/notes/ka0s-review`.

## LibKa0s: v1.71.0 is a local tag, and every re-vendor copies from it

- LK-12 creates the annotated tag `v1.71.0` locally on its final commit. The branch is pushed at the M1
  checkpoint; the tag is pushed only when the owner approves the LibKa0s merge.
- Every `RV-<AB>` copies from that tag with `git -C ../LibKa0s archive v1.71.0 LibKa0s testkit` (or a
  detached worktree of the tag, removed afterwards), never from the working tree. Each addon's
  `tests/test_vendor_sync.lua` resolves the tag from the local sibling, so the re-vendored suites pass
  offline.
- **The tag must not move once any re-vendor has copied it.** A defect found later is fixed forward as
  v1.71.1, also local.
- An addon branch whose provenance line names v1.71.0 may reach origin before the tag. It is unmerged, and
  the tag is one push away.

## WowAddonStandards v2.77.0 exists only on the feature branch until the merge

- The addon `<AB>-STD` items roll each addon's three-place reference to the version read from the local
  feature branch (`head -1 ../WowAddonStandards/standards/STANDARDS.md`), following the local
  `/dev-copilot:wow-revendor-standards` procedure (OWNER_SCOPE item 5). That roll is correct only once the
  standard merges, and it lands with the same merge.
- Until the merge, `/dev-copilot:wow-standards-audit`, `/dev-copilot:review` and
  `/dev-copilot:wow-harvest-standards` fetch the standard from GitHub and grade against v2.76.1.

## dev-copilot changes reach sessions only after the merge and a plugin update

- The installed plugin is 2.0.1 at `984cd1d`. The `ka0s-bounded` symlink points into its cache. Until the
  owner merges dev-copilot and the plugin updates, the `command -v` denial (DC-01), the timeout leak
  (DC-03) and the symlink hazard (DC-05) remain in the tooling this run uses, and the agents read their old
  specs. Re-vendors and standards rolls follow the local command text by hand where it matters.
- The plugin version does not change, so the marketplace update has to be triggered from the new commit,
  not a version number. Confirm with `installed_plugins.json`'s `gitCommitSha`.

## What the owner approves, and in what order it is published

LibKa0s's README names standard v2.77.0 (LK-12), dev-copilot's README names it too (DC-15), and the
dev-copilot agents point at `standards/CHANGELOG.md`, which exists only in v2.77.0. None of the three reads
correctly on GitHub without the others, so one approval should cover all three, published in this order
(`/dev-copilot:finalize`, dependency order):

1. **WowAddonStandards:** merge `--no-ff` to `master` and push. v2.77.0 is live for the agents.
2. **LibKa0s:** merge to `master`, push, then `git push origin v1.71.0`. Confirm with
   `git ls-remote --tags origin v1.71.0`.
3. **dev-copilot:** merge to `master` and push. With the owner's go-ahead, `git push origin --delete main`
   (DC-14). Update the plugin and confirm the cached commit.
4. **The eleven addons**, whose branches are already on origin from the milestone pushes.
5. **Ka0sAddonsCommonTasks** (`main`).

Then every `feat/2026-10-07-review-audit-remediation` branch, local and remote, is deleted, along with any
stash or worktree the run created.

## Milestone 1 exit criteria

- WowAddonStandards: `head -1 standards/STANDARDS.md` names v2.77.0 with the landing date; the index holds
  one changelog entry and is under 60,000 bytes; `standards/CHANGELOG.md` holds 99 entries;
  `bash scripts/check-standard.sh` exits 0; no tracked file carries a CR; `git log --oneline master..HEAD`
  shows eleven `WS-` commits.
- LibKa0s: `lua tests/run.lua` 0 failed, `luacheck .` 0/0, `diff -r testkit tests/_kit` empty,
  `Kit.VERSION = 38`, `docs/test-cases.md` equal to `--list` with one Skipped row. The release bundle's
  manifest reads release `1.71.0`, `dirty` false, lint, tests and complexity `pass`, complexity warnings 0,
  with `ANALYSIS.md` beside it. `git tag -l v1.71.0` prints the tag on the `LK-12:` commit and
  `git ls-remote --tags origin v1.71.0` prints nothing. LibKa0s#43 is closed `state:done`; #32, #33, #37 and
  #39 carry `state:done`.
- dev-copilot: the four Python suites and `check_overlays.py` green, both manifests parse,
  `docs/ARCHITECTURE.md` has its five sections, `plugin.json` still reads 2.0.1.
- `exceptions.tsv` holds the LK-11 and DC-14 rows, each with its proof command.
- `./resume-state.sh M1` reports the milestone complete, with no unreviewed item and no dirty tree.
- All three feature branches and `refs/notes/ka0s-review` are pushed, and `checkpoints.tsv` has the M1
  line with the test totals and pushed heads.
