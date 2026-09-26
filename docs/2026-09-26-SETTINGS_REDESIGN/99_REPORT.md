# 99 — Execution record

SR-REC-01, written 2026-09-26. This file records what the AuraMaster settings redesign (#6) run
actually did. The plan (`03_EXECUTION_PLAN.md`) is frozen and is not edited. Sources are git in the
three repos (`git log master..feat/2026-09-26-settings-redesign`, the `refs/notes/ka0s-review` notes,
`git ls-remote`), `./resume-state.sh -v`, the LibKa0s release manifest, and the workflow's per-item
evidence for the relaunched run. No battery was re-run for this record.

## 1. Outcome

- All eleven build items are done. `resume-state.sh -v` reports M1 5/5, M2 6/6, and SR-REC-01 as
  the only READY item. All four trees were clean when this record was written.
- WowAddonStandards carries v2.69.0 (options-ui-§2, §13 and §14 sanction the nav rail as a first
  level) on its feature branch.
- LibKa0s carries OptionsNav minor 1 (`O.NavRail`, `lib.__railInset`), Options minor 25 and
  OptionsTabs minor 5, released as the **local** annotated tag `v1.61.0`.
- AuraMaster carries the re-vendor of v1.61.0 and the one Containers page: the band, the nav rail
  (General · Filters · Layout · the container's style) and the selected section. The Filters, Layout,
  Bars, Icons and Text sub-pages are retired.
- **Nothing was pushed**: no branch, no tag and no notes. `git ls-remote origin
  refs/heads/feat/2026-09-26-settings-redesign` prints nothing in any of the three repos. Pushes
  were not authorized (O2, `00_OVERVIEW.md`). Nothing was merged, and no addon version was bumped.
- The in-client smoke checks have **not** been run. They are the owner's (section 6).

## 2. Heads

| Repo | `master` (= `origin/master`) | Branch head | Commits ahead | `refs/notes/ka0s-review` (local) |
|---|---|---|---|---|
| WowAddonStandards | `2854053` | `c684262` | 3 | `45546c8` |
| LibKa0s | `bed0eb1` | `c6183bd` | 5 | `5e5135f` |
| AuraMaster | `b1d511e` | `d28d32d` | 13 (4 spec commits + 9 SR commits) | `7eeaad2` |

Each branch sits directly on its current master (the merge base is master's head), so a later
`--no-ff` merge is clean.

**Local tag:** LibKa0s `v1.61.0`, annotated (`7e64131`), on `c6183bd`, the SR-LK-03 release commit
and the branch head. Subject: "LibKa0s v1.61.0: OptionsNav minor 1 (the nav rail); Options
25.31.5.7.4.1". It is not on origin (`git ls-remote --tags origin v1.61.0` is empty).

## 3. What shipped, per repo

### WowAddonStandards (M1)

| Commit | Item | What |
|---|---|---|
| `b613f0a` | SR-WS-01 | options-ui sanctions the nav rail as a first level (v2.69.0): the rail plus the strip is the two-level limit, the band spans the rail and the strip, the rail is not a picker, and Defaults on a railed page covers the active entry. The version header and changelog, and the STANDARDS.md blurb ("the two exemptions"). |
| `522cae3` | SR-WS-02 | Ripple into EXECUTIVE_SUMMARY.md, NEW_ADDON_CONTEXT.md, AUDIT.md checks (g)/(i), library-stack.md and README.md. |
| `c684262` | SR-WS-02R | Review fix: the OptionsNav.lua ripple the planned lines left behind (EXECUTIVE_SUMMARY file count, NEW_ADDON_CONTEXT five -> six files and `LIB_FILES`, anti-pattern #48, the changelog ripple list). |

Review notes: `b613f0a` clean; `522cae3` fixed (by `c684262`).

### LibKa0s (M1)

| Commit | Item | What |
|---|---|---|
| `2cd217b` | SR-LK-01 | `OptionsNav.lua` (minor 1): `O.NavRail`, `lib.__railInset`, the rail top measured off the active tab cap atlas, pooled entries and a combat refusal. Options 25 and OptionsTabs 5 read the one inset. Tests (`test_options_nav.lua` and a combat case), the v1.61.0 CHANGELOG block with "What a consumer owes", the `25.31.5.7.4.1` API doc and members, and test-cases.md. |
| `f88730e` | SR-LK-01R | Review fix: `NavRail` re-anchors a live scroll on a page with no banner (and gives the width back when the rail is released), plus 11 stale `#what-changed-at-this-version` links in the `25.31.5.7.4.1` doc. |
| `9394dff` | SR-LK-02 | Prose and census for the sixth Options file: six Options files, twenty-three scripts in all. |
| `7cbe02c` | SR-LK-03 | Date v1.61.0 and roll the release pointers (CHANGELOG, README standard pointer v2.69.0, releasing.md). |
| `c6183bd` | SR-LK-03 | The v1.61.0 release run, its ANALYSIS.md, the RESULTS.md row and the CHANGELOG gate line. Tagged `v1.61.0`. |

Review notes: `2cd217b` fixed (by `f88730e`); `9394dff`, `7cbe02c` and `c6183bd` clean.

### AuraMaster (M2)

The branch also carries the four spec commits it held at planning time (`9dd8fff`, `ebcea82`,
`192c8e9`, `3fdc667`).

| Commit | Item | Tests at review | What |
|---|---|---|---|
| `04b382e` | SR-AM-01 | 1637 / 0 | Re-vendor LibKa0s v1.61.0 (both payloads, byte-identical to the tag), the `NavRail` stub, CLAUDE.md provenance, and `docs/revendor/2026-09-26-v1.61.0/`. |
| `bea951f` | SR-AM-02 | 1639 / 0 | The Containers section registry (`NS.RegisterContainerSection`, `NS.ContainerSection`); the Diagnostics style gates become data. |
| `7f0bdae` | SR-AM-02R | | Review fix: a stale `settings/GeneralSpells.lua` citation and the regenerated inventory. |
| `600d43a` | SR-AM-03 | 1647 / 0 | The Containers renderer: band -> rail -> section, `SECTION_ORDER`, per-section tab memory, the style heal and the General section. |
| `3139724` | SR-AM-04 | 1653 / 0 | Deep links open Containers on a section, `Helpers.SelectSection`, the `SelectTab` route, and Defaults restores the active section. |
| `6565f5a` | SR-AM-05 | 1640 / 0 | Filters, Layout, Bars, Icons and Text are retired as sub-pages and become Containers sections. D6, the muted notice, `NS.RegisterContainerPage` and `NS.SubPageLabel` are removed, and the tests are migrated (R1-R7). |
| `342af9f` | SR-AM-05R | | Review fix: two `GeneralSpells.lua` citations this change moved, and Text.lua's `pageDim` comment. |
| `4cb463e` | SR-AM-06 | 1640 / 0 | Docs: settings-panel, ARCHITECTURE, module-map, common-tasks, README (badge 1640) and smoke-tests.md checks 251-266 (S1-S16, unmarked). |
| `d28d32d` | SR-AM-06R | 1640 / 0 | Review fix: module-map.md keeps the `test_pages_tabs.lua` row, and the rail row is its own line. |

Review notes: `04b382e`, `600d43a` and `3139724` clean; `bea951f`, `6565f5a` and `4cb463e` fixed (by
`7f0bdae`, `342af9f` and `d28d32d`).

## 4. Gate figures per milestone

Every run went through `ka0s-bounded`. Rows are also in `checkpoints.tsv`.

**M1, WowAddonStandards** (head `c684262`, clean tree): the docs gate over the 8 `.md` files changed
versus master (the array count matched `git diff --name-only`). There were 0 UNRESOLVED section refs,
0 CR bytes in every file, and `git diff --check master` was clean. Check (2) printed 14 BROKEN lines,
all of them gate-regex artifacts: absolute URLs cut at `:` and the backticked `![…](media/logos/…)`
placeholder. Per file, the count is identical on master and on the head, so no real relative link
broke. The evidence did not count the distinct section refs resolved or the links checked.

**M1, LibKa0s** (head and tag `c6183bd`, clean tree): `lua tests/run.lua` 1744 passed, 0 failed,
1 skipped (1745); luacheck 0 warnings / 0 errors in 100 files; lizard `-C 15 -w` printed nothing,
both with libs and tests/_kit excluded and over the whole repo. Release run
`docs/automated-tests/20260926-121411/manifest.json` (git `7cbe02c`, clean, `release: 1.61.0`):
verdict green; lint pass 0/0 in 100; tests 1744/0/1; complexity pass, 0 over CCN 15, 5039
functions; perf skipped (no `tests/perf.lua`). The two over-cap files, `OptionsWidgets.lua` and
`tests/test_options_widgets.lua`, are existing census rows carried forward. `Options.lua` is 1462
lines (budget 1474) and `OptionsTabs.lua` 1493 (budget 1494).

**M2, AuraMaster** (head `d28d32d`, clean before and after): `lua tests/run.lua` 1640 passed,
0 failed, 0 skipped (1640, 16 shards); luacheck 0/0 in 139 files; lizard with libs and tests/_kit
excluded printed nothing (4288 functions, AvgCCN 2.3). The largest authored files are
`settings/GeneralSpells.lua` at 1480 lines and `tests/test_anchors.lua` at 1479, both under the cap.
The vendor matches v1.61.0: SR-AM-01's review found `libs/LibKa0s` and `tests/_kit` byte-identical
to the tag's archive, and `test_vendor_sync` is in the green suite.

## 5. Deviations from the plan

The plan is frozen, so each deviation is recorded here with its reason.

1. **O1 (A2) was never answered explicitly.** The owner waived review of the spec and the plan
   ("go ahead and build the settings redesign without my approval on spec or plan"). The run took
   that as accepting the plan's proposal: the probe measures the active cap atlas. The
   `lib.__alignRail` fallback was not built. **O2:** pushes were not authorized, so nothing was
   pushed.
2. **SR-WS-01, Step 7:** the anchor "header band and tab strip included" matched twice in
   STANDARDS.md, at `:60` (the blurb) and `:110` (the frozen v2.60.0 changelog entry). The
   replacements went to `:60` only. The reviewer rebuilt the files byte for byte and confirmed it.
3. **SR-WS-02's planned lines missed part of the OptionsNav.lua ripple.** SR-WS-02R finished it,
   including `standards/standards/anti-patterns.md`, which the plan did not list. That is why the M1
   docs gate covered 8 files where the plan expected 7.
4. **SR-LK-01 had two defects the plan's code carried.** `NavRail` re-anchored the scroll only when
   a banner had reserved a band, and the renamed section in the `25.31.5.7.4.1` doc left 11 dead
   anchors. Both are fixed in SR-LK-01R (`f88730e`), which adds a new `nav:` test. v1.61.0 was
   tagged after the fix, so the tag carries it.
5. **SR-AM-02R, SR-AM-05R: line citations the plan could not foresee.** Tasks that moved lines broke
   `file:line` citations in code comments, which `tests/test_docs.lua` does not check. SR-AM-05
   itself also fixed three citations in `docs/` (ARCHITECTURE.md, midnight-quirks.md, schema.md)
   that the plan's add list did not name, and reworded the header comments of `settings/Bars.lua`
   and `settings/Text.lua`, which cited the removed `mutedNotice`.
6. **SR-AM-05 ran across the interruption.** Its partial work sat uncommitted in the AuraMaster tree
   when the first run stopped. The relaunch checked it against every step, continued it and
   committed it. Nothing was discarded. The relaunched run found SR-WS-02, SR-LK-02, SR-LK-03 and
   SR-AM-01..04 already in git and skipped them.
7. **SR-AM-06, beyond the plan's text:** the README's Containers paragraph ended with a sentence
   describing the retired notice. It now describes the style list and went through the humanize
   pass. The module-map.md rail row was inserted with a botched substitution that deleted the
   `test_pages_tabs.lua` row; SR-AM-06R restored it. `docs/test-cases.md` was already current, so it
   is unchanged. One small wording difference was left alone: the README says "It remembers" where
   the plan has "The page remembers".
8. **Checkpoint rows were written late.** The M1 and M2 checkpoints ran, but neither row was
   appended to `checkpoints.tsv` at the time. SR-REC-01 appends the M1, M2 and M3 rows from the
   recorded evidence, as its task allows.
9. **`06_SMOKE_TESTS.md` is unchanged.** The task lists it as modified, but its only rule is that
   the Result column stays empty, and it is.

## 6. Smoke checks (owner)

S1-S16 are in `06_SMOKE_TESTS.md` and, word for word, in AuraMaster's `docs/smoke-tests.md` as
checks 251-266 under "Settings redesign (#6)". None has been run, and none is marked. The owner
runs them in the client on AuraMaster `feat/2026-09-26-settings-redesign` (`d28d32d`, LibKa0s
v1.61.0) and records the results in either place.

## 7. Follow-ups

This run was not allowed to file GitHub issues, so the owner files these.

1. **AuraMaster issue for A15: Text.lua's `pageDim` dead path.** `settings/Text.lua`'s `pageDim`
   reads `ctx.__renderDisabled`, which is now always false for the Text section. It is correct and
   harmless, and its one test was deleted in SR-AM-05. File it with `/wow-addon:issue-add` as a
   dead-code sweep. The review of SR-AM-05 found two more things for the same sweep:
   - the Aura type row's `desc` still says "The Filters page offers the categories...";
   - `settings/OptionsSetup.lua`'s `EMPTY_PAGE` ("No containers yet. Create one on Containers...")
     may now be unreachable.

   SR-AM-06's review adds a third: informal mentions such as "the Filters page" and "its Text page"
   remain in the README and `docs/settings-panel.md`. They were outside the plan's list.
2. **MultiMeters#55 and KickCD#33** now have the library minor (OptionsNav 1, LibKa0s v1.61.0) and
   the standard change (v2.69.0) they were waiting for. Each needs a LibKa0s v1.61.0 re-vendor with
   a `NavRail` stub first. That is a new bundle.
3. **The owner's smoke session** over `06_SMOKE_TESTS.md` (section 6).
4. **`/wow-addon:finalize` on the owner's go-ahead.** Merge `--no-ff` in dependency order:
   WowAddonStandards, then LibKa0s (push the `v1.61.0` tag at that point), then AuraMaster. Push the
   `refs/notes/ka0s-review` notes and delete the feature branches. Until then all three branches and
   the tag exist only locally.
