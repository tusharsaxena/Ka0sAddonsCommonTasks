# 04 — Execution Plan

**164 work items in three milestones, ordered by dependency.** Branch in every repository:
`feat/2026-10-07-review-audit-remediation`.

> **Nothing in this plan has been executed.** Every "add", "move" and "re-vendor" below describes a change
> that has not been made yet. `./resume-state.sh` is the only record of progress, and it reads git.

`plan-data/items.json` is the single source of truth. It holds each item's full spec, steps, verify block
and smoke check, and the executor hands that record to the agent that implements the item. The tables at
the end of this document list the items. They are derived from `items.json`, so when the two disagree,
`items.json` wins. `03_SPEC.md` gives the end state, `02_UPSTREAM_CHANGES.md` the upstream rationale and
`05_TRACEABILITY.md` maps each finding to its item.

There are no dates here. The milestones set the order of the work, not a schedule.

---

## Milestone map

| M | Name | Items | Repos | Starts when |
|---|---|---|---|---|
| **M1** | Upstream | **38**: WS-01…WS-11 (11), LK-01…LK-12 (12), DC-01…DC-15 (15) | WowAddonStandards, LibKa0s, dev-copilot | now |
| **M2** | Re-vendor LibKa0s v1.71.0 | **11**: RV-AT, RV-AM, RV-BL, RV-CM, RV-KC, RV-LH, RV-MM, RV-PM, RV-PF, RV-PC, RV-WG | all eleven addons | LK-12 has landed and the local `v1.71.0` tag exists |
| **M3** | Addon items | **115**: AT 10 · AM 11 · BL 6 · CM 10 · KC 11 · LH 19 · MM 11 · PM 13 · PF 7 · PC 9 · WG 8 | all eleven addons | that addon's RV item has landed |

### M1: upstream

WowAddonStandards, LibKa0s and dev-copilot run in parallel with each other, and serially within each
repository. A few cross-repo edges set the order between them:

- **WowAddonStandards opens and closes one version, v2.77.0.** WS-01 opens it and moves the changelog
  history out of the index into `standards/CHANGELOG.md`. WS-02…WS-10 each add a bullet to the same
  v2.77.0 entry, and none of them bumps the version again. WS-10 adds `scripts/check-standard.sh`, an
  on-demand mechanical gate for the standard's own invariants. WS-11 closes the version: it ripples every
  change through the executive summary, context pack, playbooks, README and index blurbs, and it must pass
  `check-standard.sh`.
- **LibKa0s cuts v1.71.0 with kit revision 38.** LK-01 is the kit change, where `--list` Totals stop
  counting declared skips. Most LK items build on it. LK-07 depends on WS-07, because WS-07 defines the
  durable-citation form that LK-07 writes. LK-12 runs last. It depends on every other LK item and on
  WS-11, because LibKa0s's README names the closed standard version. LK-12 makes two commits. The first,
  `LK-12 (1/2): release v1.71.0 …`, is not matched by the id regex. The second records the release run
  and carries the annotated **local** tag `v1.71.0`.
- **dev-copilot** runs DC-01…DC-15 on hard dependencies. DC-09 depends on WS-07. DC-15 carries the
  handoffs from the standard into the audit agent and specs, so it depends on WS-01, WS-03, WS-10 and
  WS-11 and reads only the closed standard. DC-12, the US-English sweep, runs after DC-15. DC-14 deletes
  the stale `origin/main` branch, and only inside the owner-approved finalize. At the M1 checkpoint it
  gets an `exceptions.tsv` row that says it is deferred.

### M2: re-vendor

M2 starts once `git -C ../LibKa0s tag -l v1.71.0` prints the tag. The eleven RV items are independent and
run in parallel, one per addon. Each RV item:

1. Extracts the local tag with `git archive` into its own scratch directory. It never checks the tag out
   in LibKa0s.
2. Replaces `libs/LibKa0s/` and `tests/_kit/` whole from the tag, and rolls the CLAUDE.md provenance line
   from v1.70.0 to v1.71.0 in the same commit.
3. Regenerates `docs/test-cases.md` in the same commit. Kit revision 38 changes the Totals table: the
   Total now equals the README badge's passing count, and a `| Skipped | N |` row lists declared skips.
4. Writes `docs/revendor/<date>-v1.71.0/`, and the span bundle `docs/revendor/<date>-v1.69.0-v1.70.0/`
   (`01_DELTA.md` and `05_SUMMARY.md` only) for the two re-vendors that were never recorded. Line 1 of
   each `01_DELTA.md` follows the grammar in the local `../dev-copilot` `wow-revendor-libka0s` command.
   Adoption candidates the plan does not require are listed as "not adopted in this run".
5. Makes whatever finding-specific edits the item names, such as removing a stale version stamp from a
   live doc.

**Every RV commit must be green.** A mechanical blocker, such as a contract change under an unchanged
signature, is fixed in the re-vendor commit and named in its body. A behavioural red stops the item and
becomes a new `<AB>-00` item. No RV item adopts a new surface. WhatGroup's adoption of `Kit.secret` is
WG-01, in M3.

### M3: addon items

Each addon's items run **serially, in manifest order**, and the eleven addons run **in parallel**. Inside
an addon, the manifest order respects every `depends_on`. Most addons form one chain from the RV item to
the `<AB>-STD` item.

- **Cross-repo dependencies point back at M1 or M2**, for example CM-04 on LK-05, WG-01 on LK-02 and
  WS-09, and every `<AB>-STD` on WS-11. All of those have landed before M3 starts. There is one
  exception: **PC-06 depends on LH-01** (PrettyChat's ARCHITECTURE.md restates LootHistory's
  pattern-rebuild behaviour once LH-01 makes it true). `next_args.py --order` drops cross-repo edges, so
  PC-06's first step checks that `LH-01: ` exists in LootHistory and returns blocked if it does not. To
  avoid a wasted pass, launch PrettyChat after LH-01 has landed, or run PrettyChat in items/deps mode.
- **LH-14 makes two commits.** The first is `LH-14 (1/2): …` and the final one is `LH-14: …`, because it
  writes a fresh sighted automated-test bundle after the complexity work.
- **Each addon closes with `<AB>-STD`.** That item rolls the three-place standards reference (TOC
  `## X-Standard`, the README Standard badge and CLAUDE.md's "Standards compliance") to v2.77.0, read
  from `head -1 ../WowAddonStandards/standards/STANDARDS.md` on the feature branch. Today all three are
  versionless, so they stay versionless unless v2.77.0 requires a stamp. It also sweeps retired notation
  and unresolvable `filename-§N` references out of live docs, and syncs the docs for everything the
  addon's earlier items changed.

---

## The per-item loop

`plan-data/tools/execute_milestone.js` runs every item through the same three steps. One agent works on
one item at a time in a given repository. Agents in different repositories run in parallel.

1. **Implement, test first.**
   - If a commit for the item already exists, the step returns `already-landed` and does nothing else.
   - It checks that the item's same-repo dependencies have landed. If one has not, it returns `blocked`.
   - It inspects a dirty tree. If the changes are this item's partial work, it continues them. Otherwise it
     stashes them with a message. It never discards work with `reset` or `checkout`.
   - Where behaviour changes, it writes the failing case first and watches it fail for the right reason,
     then implements until the case passes.
   - It makes every ripple the repository's rules require in the same commit: LibStub minors, the
     CHANGELOG block, `docs/api/`, `docs/test-cases.md` and the README tests badge.
   - It commits only the files it touched. The subject is **`<ID>: <imperative summary>`**, and the body
     gives the finding ids and any departure from the item text. The message ends with the session's
     attribution trailers.
2. **Independent review.** A second agent reads the commit or commits against the item spec, the findings
   and `03_SPEC.md`, and re-runs the gates itself. It looks for bugs, regressions, missed ripples, tests
   that do not really pin the behaviour, and collateral edits. For an RV item, it also checks that the
   payloads are byte-identical to the tag, that the provenance line has rolled, and that the bundle is
   present. If the review finds no problem, it records the note
   `git notes --ref=ka0s-review add -m "reviewed ok <ID>" <last commit>`. A note is not a commit.
3. **One fix round.** If the review finds real problems, a third agent checks each one against the code
   and fixes the real ones in **one new commit**, `<ID>: address review — <summary>`. It never amends an
   earlier commit. It then records `reviewed, fixed <ID>` as the review note. An issue it judges not real
   is explained in the result, and is not fixed.

An item is **landed** when its `<ID>: ` commit exists. It is **closed** when one of its commits carries a
`refs/notes/ka0s-review` note. A landed but unreviewed item is reviewed again on the next launch, and
`next_args.py <M> --unreviewed` lists such items.

### Standing rules for every item

- Only the item's own repository is written. Sibling repositories are read-only.
- **Never edit an addon's `libs/` or `tests/_kit/`.** Only an RV item writes there, and only by whole
  copy. A defect found in either belongs upstream, as a new LibKa0s item.
- Scratch files go in a directory created with `mktemp -d /tmp/claude-1000/ka0s-<ID>.XXXXXX`, never a
  shared fixed path. Other agents run at the same time.
- Every heavy run goes through the bounded runner,
  `/home/tushar/.claude/dev-copilot/bin/ka0s-bounded`, called by absolute path.
- An addon's gate:
  - `luacheck .` at 0 warnings and 0 errors
  - `lua5.1 tests/run.lua` with 0 failed
  - `lizard -l lua -x "./libs/*" -x "./tests/_kit/*" .` with no function above CCN 15, or the kit's
    sighted `run-automated-tests.sh --suite complexity --no-bundle`
  - no authored `.lua` file over 1500 lines
  - the item's own verify block
- LibKa0s runs the same gate plus its own release rules.
- dev-copilot runs its Python suites: `scripts/test_detect_profile.py`, `test_check_overlays.py`,
  `test_bounded_runs.py`, the EOL-hook suite DC-04 adds, and `check_overlays.py`.
- WowAddonStandards has no suite. It checks no CR bytes and the item's verify block, plus
  `scripts/check-standard.sh` once WS-10 has landed.
- **When an addon's case count moves, `docs/test-cases.md` and the README tests badge move in the same
  commit.**
- If the item text is wrong against the code, for example a stale line number or a renamed symbol, the
  agent does what the item intends and records the departure in the commit body. It returns `blocked`
  only when the item cannot be done.

### GitHub writes

The run writes to GitHub only on issues a finding names, one call at a time and spaced apart. Five items
land with no commit and get an `exceptions.tsv` row with a proof command:

- **LK-11** relabels LibKa0s #32, #33, #37 and #39 to `state:done`.
- **PM-10** relabels PanelMaster #47.
- **KC-10** comments on KickCD #11.
- **PC-08** comments on PrettyChat #8.
- **DC-14** is the deferred deletion of `origin/main`.

Two items make a GitHub write and also commit:

- **LK-05** closes LibKa0s #43.
- **AM-STD** relabels AuraMaster #22 before its commit, so a landed AM-STD implies that the relabel
  happened.

---

## Launching

```
python3 plan-data/tools/next_args.py M1          > /tmp/claude-1000/args.json   # hard dependencies
python3 plan-data/tools/next_args.py M2          > /tmp/claude-1000/args.json
python3 plan-data/tools/next_args.py M3 --order  > /tmp/claude-1000/args.json   # serial per repo
```

Then run the Workflow tool with `scriptPath` set to the absolute path of
`plan-data/tools/execute_milestone.js` and `args` set to that JSON, passed as an object. The arguments
list only items that have not landed, and they drop dependencies that have. Relaunching after a crash is
therefore safe. Finished run results go to `plan-data/runs/`. `RESUME.md` has the full procedure.

---

## Milestone checkpoints

Stop at the end of each milestone. In M3, an addon can also be checkpointed on its own once its
`<AB>-STD` item is closed.

1. **State.** `./resume-state.sh <M>` reports the milestone complete, no unreviewed items, no dirty trees
   and no repository off the branch.
2. **Green gate in every repository the milestone touched**, run through
   `/home/tushar/.claude/dev-copilot/bin/ka0s-bounded`:
   - Addons and LibKa0s: `luacheck .` at 0/0, `lua5.1 tests/run.lua` with 0 failed and its `--list`
     matching `docs/test-cases.md`, `lizard -l lua -x "./libs/*" -x "./tests/_kit/*" .` with no function
     above CCN 15, and nothing over the 1500-line cap.
   - dev-copilot: its Python suites and `check_overlays.py`.
   - WowAddonStandards: `scripts/check-standard.sh` exits 0.

   A red gate is fixed before the checkpoint passes. It is never carried into the next milestone.
3. **M1 only.** `git -C ../LibKa0s tag -l v1.71.0` prints the tag, which sits on LK-12's final commit.
   `git -C ../LibKa0s ls-remote --tags origin v1.71.0` prints nothing. The DC-14 deferred row is in
   `exceptions.tsv`.
4. **Push** each touched repository's feature branch, and its review notes:
   `git push -u origin feat/2026-10-07-review-audit-remediation` and
   `git push origin refs/notes/ka0s-review`. Pushing a branch is not a merge. Never push the `v1.71.0`
   tag.
5. **Record** the checkpoint as one line in `checkpoints.tsv`: the date, the checkpoint, and the evidence
   (test totals per repository and the pushed heads). Commit that line in Ka0sAddonsCommonTasks on the
   same branch, and push it.

---

## What waits for the owner

- **Merging** every `feat/2026-10-07-review-audit-remediation` branch, through `/dev-copilot:finalize`
  with `--no-ff`. The order is WowAddonStandards, LibKa0s, dev-copilot, the eleven addons, then
  Ka0sAddonsCommonTasks.
- **Pushing the LibKa0s `v1.71.0` tag.** It stays local until the LibKa0s merge is approved.
- **DC-14**, deleting dev-copilot's `origin/main`. Ask about it in the same message as the merge
  go-ahead. If the owner declines, rewrite the `exceptions.tsv` reason to "declined by owner <date>".
- **In-client smoke checks** for the 57 `⚠` items and LootHistory's LED-P2-01..24
  (`06_SMOKE_TESTS.md`). No agent records a smoke result or marks one passed.
- **Releases and version bumps.** No addon version, Version History row or release tag moves in this run.
- **Cleanup after the merge.** Delete every remediation branch, local and on origin, and every stash and
  worktree the run created.

---

## The `⚠` mark

`⚠` after a title means the item has an in-client smoke check (a non-empty `smoke` field in
`items.json`). There are 57: M1 4, M2 6 and M3 47. The headless suites cannot prove those items alone.
They are code-complete when they land, and verified in the client only once the owner runs the check.

---

## M1 — Upstream: WowAddonStandards v2.77.0, LibKa0s v1.71.0 (local tag), dev-copilot

38 items · effort 22 S · 15 M · 1 L · 4 with a smoke check (⚠).

### WowAddonStandards (11 items)

| Id | Repo | Title | Depends on | Effort |
|---|---|---|---|---|
| WS-01 | WowAddonStandards | Open v2.77.0: move the changelog history out of the index into standards/CHANGELOG.md; fix the changelog typos, the order and the footer stamp | — | M |
| WS-02 | WowAddonStandards | This repo keeps its own docs/audits/ and docs/reviews/ stores: rewrite the self-description, register both stores, drop the file count and single-source the roster | WS-01 | S |
| WS-03 | WowAddonStandards | line-endings: the repo's own .gitattributes becomes the §5 LF body byte-for-byte; every restatement names both shebang carve-outs; check (e) passes paths positionally; the §7 EOL-gate MUST is scoped to repos that run a suite | WS-01 | M |
| WS-04 | WowAddonStandards | toc-file-§5: the load-bearing denominator covers every position in the listing; AUDIT.md step 4 checks the whole TOC; the worked example is cited by heading | WS-01 | S |
| WS-05 | WowAddonStandards | documentation-§3/§6/§8 and library-stack-§7 agree with themselves: §6 cites §3's frozen-store list, §8's arithmetic and single executable-content trigger, the documentation-§5/§6 row labels, ordinals and Tier 2 membership | WS-03 | M |
| WS-06 | WowAddonStandards | Retire the pre-adoption 'expect findings in every addon' wording for launcher and the disabled latch; correct the scaffold runner comment on missing suites | WS-01 | S |
| WS-07 | WowAddonStandards | documentation-§6 gains a cross-repo citation SHOULD (symbol/heading for present tense, Repo@sha:path:line for history); convert the rotted citations and misleading counts to it | WS-05 | L |
| WS-08 | WowAddonStandards | versioning-git: default-branch work by default, owner-directed or multi-repo changesets on a same-named feat/<date>-<topic> branch merged --no-ff; ripple to the index blurb, context pack, anti-pattern #21, documentation-§8 and CLAUDE.md | WS-05 | S |
| WS-09 | WowAddonStandards | events-frames-taint-§8 names the spell-cooldown fields in its trigger set; open-evolutions records the library-absent stub-burden question (U-3) | WS-01 | S |
| WS-10 | WowAddonStandards | scripts/check-standard.sh: an on-demand mechanical gate for the standard's own invariants (CR bytes, .gitattributes body, citation ranges, Sections list, anti-pattern contiguity, version stamps, roster pointers) | WS-02, WS-03, WS-04, WS-05, WS-06, WS-07, WS-08, WS-09 | M |
| WS-11 | WowAddonStandards | Close v2.77.0: ripple every change through the executive summary, context pack, playbooks, README and index blurbs; finish the changelog entry; gate on check-standard.sh | WS-10 | M |

### LibKa0s (12 items)

| Id | Repo | Title | Depends on | Effort |
|---|---|---|---|---|
| LK-01 | LibKa0s | Kit revision 38: --list Totals count only cases that run; declared skips get their own row | — | S |
| LK-02 | LibKa0s | Kit revision 38: Kit.secret, a shared secret-value simulator and an opt-in issecretvalue installer | LK-01 | M |
| LK-03 | LibKa0s | WidgetsLineChart minor 3: segments clipped to the plot rect, hover re-syncs on every render, formatX locale note ⚠ | LK-01 | M |
| LK-04 | LibKa0s | WidgetsAutocomplete minor 2: generation-guarded re-hook, set-scripts-first precondition, integral maxRows, backdrop set once ⚠ | LK-03 | M |
| LK-05 | LibKa0s | Slash key 20.2: ParseValue refuses nan/inf, and Slash.lua cites the standard by section (closes #43) ⚠ | LK-01 | S |
| LK-06 | LibKa0s | Env minor 2 and OptionsIdList minor 4: drop the dead bare-global GetAddOnMetadata and IsAddOnLoaded rungs | LK-01 | S |
| LK-07 | LibKa0s | Live-doc drift: resolvable evidence ids in CLAUDE.md, no derived headroom figure, Perf stub template comments | LK-01, WS-07 | S |
| LK-08 | LibKa0s | US-English sweep of docs/adoption-prompt.md and docs/adoption-report.md, now gated as authored files | LK-07 | S |
| LK-09 | LibKa0s | Band watch list: the five over-shelf-life 'accepted' Options files become one tracked deviation row; dispositions point at it | LK-08, LK-06 | S |
| LK-10 | LibKa0s | Sampled mutation pass on the widget suites: '-- red under:' notes for the key negative cases | LK-03, LK-04 | S |
| LK-11 | LibKa0s | Issue-store housekeeping: closed #32, #33, #37, #39 relabelled state:done | — | S |
| LK-12 | LibKa0s | Cut LibKa0s release v1.71.0: version block, release run with ANALYSIS.md, LOCAL tag only ⚠ | LK-01, LK-02, LK-03, LK-04, LK-05, LK-06, LK-07, LK-08, LK-09, LK-10, LK-11, WS-11 | M |

### dev-copilot (15 items)

| Id | Repo | Title | Depends on | Effort |
|---|---|---|---|---|
| DC-01 | dev-copilot | Bounded-runs hook: stop denying 'command -v' tool probes; clean up test tempdirs | — | S |
| DC-02 | dev-copilot | Bounded-runs matcher: close the 'ulimit -v unlimited' and 'sh -c' false negatives | DC-01 | S |
| DC-03 | dev-copilot | ka0s-bounded: kill the whole tree on timeout when non-interactive; recompute slots while waiting | — | M |
| DC-04 | dev-copilot | Line-ending hook: add an automated test suite (symlink case expected-red) | — | M |
| DC-05 | dev-copilot | Line-ending hook: resolve symlinks so the target is converted and the link survives | DC-04 | S |
| DC-06 | dev-copilot | Author the docs/ARCHITECTURE.md hub (documentation-§8 Substitutes #3): Overview, Module Map, Known Limitations, Documentation map, Documented deviations | DC-01, DC-03, DC-05 | M |
| DC-07 | dev-copilot | Finish the wow-addon rename sweep and add the tooling kind to user-facing descriptions | DC-06 | S |
| DC-08 | dev-copilot | Issue commands: one shared meaning of 'all' in a WoW repo | DC-07 | M |
| DC-09 | dev-copilot | Replace rotted worked examples in specs with durable citations | DC-06, WS-07 | M |
| DC-10 | dev-copilot | Cross-addon pass: mktemp roots file and drop the frozen v1.56.0 baseline | DC-09 | S |
| DC-11 | dev-copilot | Push-safety wording: wow-new-addon roster step and finalize push rejection | DC-07 | S |
| DC-15 | dev-copilot | Audit agent and spec handoffs from the standard: documentation-lane register read, stale launcher/EOL content, the changelog's new home, check (e) quoting, sync-docs runs check-standard.sh, README standard version | DC-06, DC-07, WS-01, WS-03, WS-10, WS-11 | M |
| DC-12 | dev-copilot | US-English sweep over live specs and root docs | DC-06, DC-07, DC-08, DC-09, DC-10, DC-11, DC-15 | S |
| DC-13 | dev-copilot | DEPENDENCIES.md: command-based inventory, fresh citations and reasoned version floors | DC-12 | S |
| DC-14 | dev-copilot | Delete the stale origin/main branch (owner go-ahead only) | — | S |

## M2 — Re-vendor LibKa0s v1.71.0 into the eleven addons

11 items · effort 0 S · 11 M · 0 L · 6 with a smoke check (⚠).

| Id | Repo | Title | Depends on | Effort |
|---|---|---|---|---|
| RV-AT | AbsorbTracker | Re-vendor LibKa0s v1.71.0 from the local tag; record the unrecorded v1.69.0/v1.70.0 span; kit 38 clears the Totals/badge mismatch ⚠ | LK-12 | M |
| RV-AM | AuraMaster | Re-vendor LibKa0s v1.71.0 from the local tag; record the unrecorded v1.69.0/v1.70.0 span ⚠ | LK-12 | M |
| RV-BL | BankLedger | Re-vendor LibKa0s v1.71.0 (kit 38) from the local tag; record it plus the unrecorded v1.69.0/v1.70.0 span bundle ⚠ | LK-12 | M |
| RV-CM | ConsumableMaster | Re-vendor LibKa0s v1.71.0 from the local tag; record the unrecorded v1.69.0/v1.70.0 re-vendors in one span bundle ⚠ | LK-12 | M |
| RV-KC | KickCD | Re-vendor LibKa0s v1.71.0 from the local tag, with the v1.71.0 bundle and the unrecorded v1.69.0-v1.70.0 span bundle | LK-12 | M |
| RV-LH | LootHistory | Re-vendor LibKa0s v1.71.0 from the local tag: both payloads whole, provenance line, docs/revendor bundle, regenerated inventory | LK-12 | M |
| RV-MM | MultiMeters | Re-vendor LibKa0s v1.71.0 from the local tag; record the unrecorded v1.69.0/v1.70.0 re-vendors as a span bundle and de-tag the stale library/kit stamps | LK-12 | M |
| RV-PM | PanelMaster | Re-vendor LibKa0s v1.71.0 (kit revision 38) from the local tag; record the unrecorded v1.69.0-v1.70.0 span | LK-12 | M |
| RV-PF | PartyFrameEnhanced | Re-vendor LibKa0s v1.71.0 from the local tag; record the unrecorded v1.69.0/v1.70.0 span; de-tag live docs ⚠ | LK-12 | M |
| RV-PC | PrettyChat | Re-vendor LibKa0s v1.71.0 from the local tag; record the unrecorded v1.69.0/v1.70.0 re-vendors in one span bundle ⚠ | LK-12 | M |
| RV-WG | WhatGroup | Re-vendor LibKa0s v1.71.0 (kit 38) from the local tag; record the unrecorded v1.69.0/v1.70.0 re-vendors in a span bundle; de-tag stale v1.68.1 stamps | LK-12 | M |

## M3 — Addon items

115 items · effort 80 S · 34 M · 1 L · 47 with a smoke check (⚠).

### AbsorbTracker (10 items)

| Id | Repo | Title | Depends on | Effort |
|---|---|---|---|---|
| AT-01 | AbsorbTracker | Offline perf measures the shipped doRepaint: NS.Timer.__doRepaint seam, repaintPass scenario, re-derived dormant ceiling | RV-AT | M |
| AT-02 | AbsorbTracker | LibKa0s-Widgets-1.0 gets its setup seam: core/WidgetsSetup.lua publishes NS.Widgets with a library-absent stub and a parity case ⚠ | RV-AT, AT-01 | M |
| AT-03 | AbsorbTracker | Annotate the load-bearing settings TOC lines: Schema.lua and OptionsSetup.lua | RV-AT, AT-02, WS-04 | S |
| AT-04 | AbsorbTracker | Retire the savedvariables-§1 register row the standard now sanctions, recording its two residual differences | RV-AT, AT-03 | S |
| AT-05 | AbsorbTracker | doRepaint iterates NS.Units.LIST directly instead of building a closure per coalesced pass ⚠ | RV-AT, AT-01, AT-04 | S |
| AT-06 | AbsorbTracker | /at debug hold refuses while the addon is stood down for a perf capture; the degraded-load test asserts the latch, not a stub literal ⚠ | RV-AT, AT-05 | S |
| AT-07 | AbsorbTracker | NS.RelockForCombat: standing up or enabling mid-combat re-locks unlocked bars so the fight starts on live data ⚠ | RV-AT, AT-06 | S |
| AT-08 | AbsorbTracker | Debug and chat output hygiene: the two log-on-change memos go through DebugChanged; the migration-failure line hands its parts to the printer | RV-AT, AT-07 | S |
| AT-09 | AbsorbTracker | Doc drift sweep against the tree; the automated-tests page quotes the runner; Master-scale drift recorded for smoke S-05 ⚠ | RV-AT, AT-08, WS-07 | M |
| AT-STD | AbsorbTracker | Roll the standards reference to the version WowAddonStandards opens in this run (v2.77.0); docs sync of everything AT-01..AT-09 changed | WS-11, AT-09 | S |

### AuraMaster (11 items)

| Id | Repo | Title | Depends on | Effort |
|---|---|---|---|---|
| AM-01 | AuraMaster | /am select and /am delete resolve a bare number by exact name before id, refuse a cross-match, '#N' always means id ⚠ | RV-AM | S |
| AM-02 | AuraMaster | Schema-migration summary lines reach the log through DebugAtEnable ⚠ | AM-01 | S |
| AM-03 | AuraMaster | Slash help rows: the library-absent stub stops copying FormatRow; debug row rekeyed; containers listing documented as printed ⚠ | AM-02 | S |
| AM-04 | AuraMaster | Split tests/test_anchors_drag.lua along the lifecycle vs drop/attach seam | AM-03 | M |
| AM-05 | AuraMaster | logCandidates below CCN 15: extract the per-target text helper (byte-identical [Anchor] line) | AM-04 | S |
| AM-06 | AuraMaster | Peel the frozen schema migrations out of core/Database.lua into core/Database_Migrations.lua ⚠ | AM-05 | M |
| AM-07 | AuraMaster | Container picker labels stop lowercasing translated strings ⚠ | AM-06 | S |
| AM-08 | AuraMaster | Launcher test-mode drift: docs and comments name the menu's Test mode entry; stale map row and test comment | AM-07 | S |
| AM-09 | AuraMaster | docs/ARCHITECTURE.md Module Map spills its drag/snap/detach narrative into docs/data-flow.md | AM-08 | S |
| AM-10 | AuraMaster | .pkgmeta ignores .claude and media/screenshots | AM-09 | S |
| AM-STD | AuraMaster | Roll the standards reference to the run's standard version; docs sync; close-out label on #22 | WS-11, AM-10 | S |

### BankLedger (6 items)

| Id | Repo | Title | Depends on | Effort |
|---|---|---|---|---|
| BL-01 | BankLedger | LT.GroupEntries back under CCN 15: module-level group comparators, characterization case first | RV-BL | S |
| BL-02 | BankLedger | Browser search: trimmed query matches the suggestions, one filter pass per ApplyView/tab switch, printer arguments ⚠ | BL-01 | M |
| BL-03 | BankLedger | Peel the per-tab view machinery out of modules/Browser.lua into modules/Browser_Views.lua (pure move) ⚠ | BL-02 | M |
| BL-04 | BankLedger | Docs drift sweep: Logo-art pointers, the mono-glyph comment, per-tab saved views, session-only lastTab, PANEL-28 both tabs ⚠ | BL-03 | S |
| BL-05 | BankLedger | Library-absent Meta drops the dead bare-global GetAddOnMetadata rung (cluster C27 parity with LK-06, MM-07, PM-09) | RV-BL, BL-04 | S |
| BL-STD | BankLedger | Roll the standards reference to WowAddonStandards v2.77.0 and sync docs for this run's changes | WS-11, BL-05 | S |

### ConsumableMaster (10 items)

| Id | Repo | Title | Depends on | Effort |
|---|---|---|---|---|
| CM-01 | ConsumableMaster | Macro fingerprint is trusted only when the live account-wide macro still holds that body; deleted or overwritten KCM_* macros are rewritten ⚠ | RV-CM | M |
| CM-02 | ConsumableMaster | Seed the Devourer Demon Hunter stat priority (12_1480, Intellect) and test per playable spec, not per class ⚠ | RV-CM, CM-01 | S |
| CM-03 | ConsumableMaster | OnSpecChanged ignores groupmates' respecs and runs a discovery pass for the new spec before recomputing ⚠ | RV-CM, CM-02 | S |
| CM-04 | ConsumableMaster | /cm priority accepts only a positive item ID or s:<positive spell ID>; everything else prints the usage line | RV-CM, CM-03, LK-05 | S |
| CM-05 | ConsumableMaster | One composite-config rule: Selector.compositeRefs delegates to a published MacroManager.CompositeConfig | RV-CM, CM-04 | S |
| CM-06 | ConsumableMaster | Out-of-combat bar refresh scores each flyout candidate once: one scoreCache per MacroBar.Refresh threaded to Selector.ListAvailable ⚠ | RV-CM, CM-05 | M |
| CM-07 | ConsumableMaster | Authored-doc drift: cite handlers and writers by name in ARCHITECTURE.md, resolvable register evidence ids, the renamed perf-analysis command, and the sighted complexity command | RV-CM, CM-06, WS-07 | S |
| CM-08 | ConsumableMaster | TOC load-bearing notes: CoreSetup names both file-scope printer consumers, SlashDump cites the right seam, and the seed files are marked conventional | RV-CM, CM-07, WS-04 | S |
| CM-09 | ConsumableMaster | Library-absent Meta drops the dead bare-global GetAddOnMetadata rung (cluster C27 parity with LK-06, MM-07, PM-09) | RV-CM, CM-08 | S |
| CM-STD | ConsumableMaster | Roll the standards reference to the version WowAddonStandards opens in this run, and sync the docs earlier items changed | WS-11, CM-09 | S |

### KickCD (11 items)

| Id | Repo | Title | Depends on | Effort |
|---|---|---|---|---|
| KC-01 | KickCD | Cast bar drops a stale primary-icon anchor when the icon grid empties ⚠ | RV-KC | S |
| KC-02 | KickCD | Cast-bar name truncation counts UTF-8 characters, not bytes ⚠ | RV-KC, KC-01 | S |
| KC-03 | KickCD | Glow gate tracks any target cast so the target_casting glow trigger follows friendly casts ⚠ | RV-KC, KC-02 | S |
| KC-04 | KickCD | /kcd debug: an unknown word refuses without toggling the console; castbar and interrupt take an optional target\|focus unit ⚠ | RV-KC, KC-03 | M |
| KC-05 | KickCD | Migration target published as NS.SCHEMA_VERSION; the Database.CURRENT_DB_VERSION alias goes | RV-KC, KC-04 | M |
| KC-06 | KickCD | Util.Throttle reuses a frozen empty-args sentinel for zero-argument calls | RV-KC, KC-05 | S |
| KC-07 | KickCD | .luacheckrc read_globals keeps only names a linted file reads bare | RV-KC, KC-06 | S |
| KC-08 | KickCD | Rot-proof the four drifted inventories: ARCHITECTURE addonName rule, .luacheckrc history comment, compat-layer combat listener, .pkgmeta count | RV-KC, KC-07 | S |
| KC-09 | KickCD | Qualify the standalone bare §N citations in tests and live docs | RV-KC, KC-08, WS-07 | S |
| KC-10 | KickCD | Issue store: record on closed #11 that #10 (e0da04c) superseded the RenderGrid decline | RV-KC, KC-09 | S |
| KC-STD | KickCD | Roll the standards reference to Ka0s WoW Addon Standard v2.77.0 and sync the docs | WS-11, KC-10 | M |

### LootHistory (19 items)

| Id | Repo | Title | Depends on | Effort |
|---|---|---|---|---|
| LH-01 | LootHistory | Self-loot, currency and roll-won patterns rebuild when the chat globals they were compiled from change (PrettyChat rewrites them mid-session) ⚠ | RV-LH | M |
| LH-02 | LootHistory | Util.Coalesce: a window canceled by the stand-down no longer wedges the trigger for the rest of the session ⚠ | RV-LH, LH-01 | S |
| LH-03 | LootHistory | Reconciler: the combat-exit LoginScan/Flush runs outside the ledgerEvent perf bracket | RV-LH, LH-02 | S |
| LH-04 | LootHistory | Surface parity case for the Perf library-absent stub | RV-LH, LH-03 | S |
| LH-05 | LootHistory | TOC: annotate the four unannotated load-bearing positions, mark the # Modules group's free positions, AnalyticsCharts publishes NS.Analytics idempotently | RV-LH, LH-04, WS-04, WS-07 | S |
| LH-06 | LootHistory | Timeline: one parser for the holder/container location string; the pane-resize double render pinned and recorded | RV-LH, LH-05 | S |
| LH-07 | LootHistory | Five chat lines pass their arguments to the shared printer instead of pre-formatting | RV-LH, LH-06 | S |
| LH-08 | LootHistory | Peel BrowserTable's grouping/holder-move layer into modules/BrowserTableGroup.lua (pure move) ⚠ | RV-LH, LH-07 | M |
| LH-18 | LootHistory | Peel Browser's widget kit into modules/BrowserWidgets.lua (pure move) ⚠ | RV-LH, LH-08 | M |
| LH-09 | LootHistory | Complexity: core/Database.lua's four functions above CCN 15 (convertHolderMoves, compileFilter, accumulateLedger, Database:Stats) | RV-LH, LH-18 | M |
| LH-10 | LootHistory | Complexity: core/Ledger.lua (PairHolders, scopeReason, RecomputeFlows) and modules/AnalyticsLedger.lua (BackToBackRows) | RV-LH, LH-09 | M |
| LH-11 | LootHistory | Complexity: modules/Reconciler.lua (onEvent, planHolder, WriteRows) and modules/Escrow.lua (planMailMoney, planExits, commitExits) | RV-LH, LH-10, LH-03 | L |
| LH-12 | LootHistory | Complexity: core/LifecycleSetup.lua (NS.StandDown, NS.StandUp) and core/Compat.lua (ListedCurrencyID, ListCurrencies) ⚠ | RV-LH, LH-11 | M |
| LH-13 | LootHistory | Complexity: modules/Collector.lua currencyLine, modules/Holdings.lua Holdings:Search, modules/TestData.lua walk and DefaultTimelineThing | RV-LH, LH-12 | M |
| LH-14 | LootHistory | Complexity: Browser/BrowserTable (historyCharItems, holderCharItems, holderMoves, SetTestMode, GroupRecords) to zero warnings; fresh sighted automated-test bundle ⚠ | RV-LH, LH-13, LH-08, LH-18 | M |
| LH-15 | LootHistory | docs/ARCHITECTURE.md hub: spill the module map to module-map.md, complete the out-of-scope store list, record the auction-exit known limitation | RV-LH, LH-14, WS-05 | M |
| LH-16 | LootHistory | Doc-set drift: re-derived counts and citations, the complexity command, the holdings writer list, the suite count | RV-LH, LH-15, WS-07 | S |
| LH-17 | LootHistory | README: one closing signpost sentence in Usage; drop the contributor-facing line from the 1.4.0 Version History row | RV-LH, LH-16 | S |
| LH-STD | LootHistory | Roll the standards reference to the version WowAddonStandards opens in this run; docs sync of everything earlier items changed; owner's LED-P2 in-client gate listed ⚠ | WS-11, LH-17 | S |

### MultiMeters (11 items)

| Id | Repo | Title | Depends on | Effort |
|---|---|---|---|---|
| MM-01 | MultiMeters | Merge pets: an owner's own figures add to a cell its pet created earlier in the column instead of replacing it ⚠ | RV-MM | M |
| MM-02 | MultiMeters | Secrets.PlainTruth is the one boolean probe; Aggregator, Tooltip and the Provider diagnostics use it and the field census no longer short-circuits on booleans | RV-MM, MM-01 | S |
| MM-03 | MultiMeters | A partial roster is rebuilt at most once per aggregate pass, not on every lookup | RV-MM, MM-02 | M |
| MM-04 | MultiMeters | Renaming a window to a different case of its own name keeps the name instead of appending ' 2' ⚠ | RV-MM, MM-03 | S |
| MM-05 | MultiMeters | Conformance 'Disabled 8' also drives the launcher right-click menu: only Enabled clickable, nothing written, nothing shown | RV-MM, MM-04 | S |
| MM-06 | MultiMeters | Remove the retired drill-down Back button machinery and its three tests ⚠ | RV-MM, MM-05 | S |
| MM-07 | MultiMeters | Library-absent NS.Meta drops the dead bare-global GetAddOnMetadata rung; its defending comments reworded | RV-MM, MM-06, LK-06 | S |
| MM-08 | MultiMeters | 1.1.0 Version History row tells players the minimap CLI path moved to global.minimap.shown | RV-MM, MM-07 | S |
| MM-09 | MultiMeters | Docs quote the kit's sighted complexity suite, not raw lizard; un-pin lizard per documentation-§7 | RV-MM, MM-08 | S |
| MM-10 | MultiMeters | Hub and comment truth: ARCHITECTURE.md counts and retired-row headings, hub slimmed toward ~400 lines, two false Slash.lua comments, the architecture-§4 citation, and window-copy by id documented | RV-MM, MM-09 | M |
| MM-STD | MultiMeters | Roll the standards reference to WowAddonStandards v2.77.0 and sync the docs earlier items changed | WS-11, MM-10 | S |

### PanelMaster (13 items)

| Id | Repo | Title | Depends on | Effort |
|---|---|---|---|---|
| PM-01 | PanelMaster | Delete-all popup names the active profile and says every character on it loses its panels ⚠ | RV-PM | S |
| PM-02 | PanelMaster | Reset all settings sweeps the session-only rows: re-lock and hide the debug console, with a blast-radius test ⚠ | PM-01 | M |
| PM-03 | PanelMaster | Per-panel Delete and Reset in the editor ask first, naming the panel; the Registry comment becomes true ⚠ | PM-02 | M |
| PM-04 | PanelMaster | Stand-down drops combat-held unlocks so a later combat exit cannot unlock every panel ⚠ | RV-PM | S |
| PM-05 | PanelMaster | Non-Latin and accented panel names get distinct frame names; duplicate-name check folds UTF-8 case ⚠ | PM-03 | M |
| PM-06 | PanelMaster | Panel number fields refuse NaN and infinity, and /pm recover repairs a non-finite position in one run ⚠ | PM-05 | M |
| PM-07 | PanelMaster | R.Sanitize repairs every template field (accent colors, artBlend, artDesaturate) with a coverage property test; lists treat enabled==nil as enabled | PM-06 | S |
| PM-08 | PanelMaster | Library-absent Slash stub stops copying the library's colored key = value format | PM-07 | S |
| PM-09 | PanelMaster | Delete the dead bare-global AddOns fallbacks in EnvSetup and Compat.AddOnFolders | PM-08 | S |
| PM-10 | PanelMaster | Issue store: closed #47 relabelled state:done | RV-PM | S |
| PM-11 | PanelMaster | Doc-and-comment sweep against the tree: lifecycle/launcher comments, register row, census, sighted complexity runner, ARCHITECTURE trim | PM-09, PM-04 | M |
| PM-12 | PanelMaster | CLAUDE.md stub items in standard order; README drops angle-bracket placeholders and the 1.2.0 release-process line | PM-11 | S |
| PM-STD | PanelMaster | Roll the standards reference to WowAddonStandards v2.77.0 and sync the docs the earlier items changed | WS-11, PM-12 | S |

### PartyFrameEnhanced (7 items)

| Id | Repo | Title | Depends on | Effort |
|---|---|---|---|---|
| PF-01 | PartyFrameEnhanced | Secure-write queue: one raising deferred write no longer orphans the rest; unwrapFrame re-wrap guarded ⚠ | RV-PF | M |
| PF-02 | PartyFrameEnhanced | Profile change in combat cannot turn preview on: PROFILE receiver honours the combat refusal ⚠ | RV-PF, PF-01 | S |
| PF-03 | PartyFrameEnhanced | Pending-secure listener moves from a private CreateFrame to a dedicated AceEvent target (events-frames-taint-§1) ⚠ | RV-PF, PF-02 | S |
| PF-04 | PartyFrameEnhanced | /pfe status prints one unlocked flag ⚠ | RV-PF, PF-03 | S |
| PF-05 | PartyFrameEnhanced | Doc-set drift: kit/command/shim-count fixes, fourth Documentation-map table, settings-panel shape, register row text | RV-PF, PF-04, WS-05 | S |
| PF-06 | PartyFrameEnhanced | Library-absent Meta drops the dead bare-global GetAddOnMetadata rung (cluster C27 parity with LK-06, MM-07, PM-09) | RV-PF, PF-05 | S |
| PF-STD | PartyFrameEnhanced | Roll the standards reference to WowAddonStandards v2.77.0 and sync docs | WS-11, PF-06 | S |

### PrettyChat (9 items)

| Id | Repo | Title | Depends on | Effort |
|---|---|---|---|---|
| PC-01 | PrettyChat | Schema refuses an empty or whitespace-only format, so the panel can no longer store a blank chat string ⚠ | RV-PC | S |
| PC-02 | PrettyChat | RunMigrations leaves a newer build's data alone: no prune and no restamp when the stored schemaVersion is ahead | RV-PC, PC-01 | S |
| PC-03 | PrettyChat | Categories page header Defaults asks before resetting all eight tabs; the footer path (already confirmed by Blizzard) does not ask twice ⚠ | RV-PC, PC-02 | S |
| PC-04 | PrettyChat | /pc test category: General is not a test category; leave it out of the Valid list and refuse it as unknown ⚠ | RV-PC, PC-03 | S |
| PC-05 | PrettyChat | Comment and doc truth: _G writes do taint (only non-protected readers), and the report-size and addon-count figures stop contradicting each other | RV-PC, PC-04 | S |
| PC-06 | PrettyChat | Docs sync against the tree: the Item/Pool/Widgets sentence, the perf-sweep commit, .luacheckrc counts, PRETTYCHAT-A-NN ids remapped, LootHistory cited by name | RV-PC, WS-07, PC-05, LH-01 | M |
| PC-07 | PrettyChat | Hub ARCHITECTURE.md back under ~400 lines: census exemption prose to global-strings.md, retired-row narratives to one line | RV-PC, WS-05, PC-06 | S |
| PC-08 | PrettyChat | Issue #8: comment that SP-PC-01's Profiles page superseded the per-character profile decline (no relabel, no commit) | RV-PC, PC-07 | S |
| PC-STD | PrettyChat | Roll the standards reference to the version WowAddonStandards opens in this run (v2.77.0) and sync docs with this run's changes | WS-11, PC-08 | S |

### WhatGroup (8 items)

| Id | Repo | Title | Depends on | Effort |
|---|---|---|---|---|
| WG-01 | WhatGroup | Teleport-cooldown reader survives secret cooldown values: unknown instead of a raise, ticker stays armed; regression cases on Kit.secret ⚠ | RV-WG, LK-02, WS-09 | M |
| WG-02 | WhatGroup | RunTest previews without clobbering pendingInfo, and builds nothing while stood down; reloadProfile comment corrected ⚠ | WG-01 | M |
| WG-03 | WhatGroup | Stand-down's owed-Hide PLAYER_REGEN_ENABLED registration goes through NS.SafeRegisterEvent | WG-02 | S |
| WG-04 | WhatGroup | Popup Height tooltip and Frame.lua size comment stop restating a default number ⚠ | WG-03 | S |
| WG-05 | WhatGroup | Re-measure the offline perf baseline after WG-01/WG-02; bisect the showFrameRepeat 18->19 API move and record the cause | WG-04 | S |
| WG-06 | WhatGroup | Docs and comment drift sync: Compat load-order header, shim count via the documentation-§3 grep, durable citations, count-free settings and .pkgmeta wording | WG-05, WS-07 | M |
| WG-07 | WhatGroup | Library-absent Meta drops the dead bare-global GetAddOnMetadata rung (cluster C27 parity with LK-06, MM-07, PM-09) | RV-WG, WG-06 | S |
| WG-STD | WhatGroup | Roll the standards reference to the v2.77.x WowAddonStandards opens in this run; docs sync of everything WG-01..WG-07 changed | WS-11, WG-07 | S |

