# Design: the upstream release-check note (test-mode data and sim scenarios)

**Area:** OWNER_SCOPE A (last line) and B3. **Items:** WS-25, WS-26, LK-25, DC-01.
**Read-only inputs:** `WowAddonStandards@db00f05` (v2.86.0), `LibKa0s@99fb662` (v1.75.2),
`dev-copilot@43dd69b` (2.4.0). Nothing was written to any repo.

OWNER_SCOPE B3, binding: *"The upstream note is a release-check rule: a rule in the standard's release
section; a step in dev-copilot's WoW bump-version flow that asks the owner whether test-mode data and
sim scenarios are still current; and a line in LibKa0s's release checklist. No tracking issues."*

---

## 1. Current state, with evidence

### 1.1 The standard has no "release section" as such

- `standards/standards/versioning-git.md` (15 lines, one of the eleven unnumbered files) is where the
  version bump is ruled: line 6, *"MUST bump in TOC `## Version:` … The `dev-copilot:bump-version` skill
  automates this."* It is the nearest thing to a release section, but it holds no checklist.
- The release **gate** lives in `automated-tests-§3` (*The release gate*, `automated-tests.md:256`) and
  the release **record** in `automated-tests-§5` (`automated-tests.md:451`: *"`ANALYSIS.md` — the
  write-up (MUST at release, SHOULD otherwise)"*) and §6 (*"MUST produce a full four-suite bundle as part
  of every release"*).
- `AUTOMATED_TESTS.md` (root playbook) owns the `ANALYSIS.md` template (Step 2, lines 41–140) and has a
  *Step 5 — Release runs* (lines 262–269) listing what a release run MUSTs.
- `preview-mode.md` (54 lines, unnumbered) owns test mode (line 10, MUST), the marker (line 11, v2.86.0)
  and *The in-game simulator (MAY)* (line 28). Nothing in it says when the placeholder data or the
  scenarios are revisited. Data that names game content (season dungeons, items, spells, encounter
  names) silently ages every patch.
- `AUDIT.md:938–962` checks the marker and the simulator contract, never their currency.
- `NEW_ADDON_CONTEXT.md:1626` (hard rule 18) and `:1747` (Definition of done checkbox) summarize
  preview-mode.
- `library-stack.md:338`: `preview-mode` does **not** bind a library repo (no on-screen display), so a
  standard rule cannot reach LibKa0s directly. The library's own release practice is
  `LibKa0s/docs/releasing.md`.

### 1.2 LibKa0s release checklist

`LibKa0s/docs/releasing.md` (1058 lines, CRLF, checked by `tests/test_prose.lua:350` for US English),
*Order of operations* steps 1–9. Step numbers are cited from elsewhere (`CLAUDE.md:6` "step 7",
`tests/test_versioning.lua:188` "step 5", `CLAUDE.md:485` "step 1"), so steps **must not be renumbered**.
Step 7 already ends with a precedent: a fixed *"Release gate (…)"* line closing the version's
`CHANGELOG.md` block. The library's preview/sim surfaces are `LibKa0s/Sim.lua`, `SimTimeline.lua`,
`SimPanel.lua`, `W.TestStrip` (in `Widgets.lua` at v1.75.2; this run generalizes it), their fixtures
`tests/fixture_sim_panel.lua`, `tests/test_sim_*.lua`, `tests/test_widgets_teststrip.lua`, and their
API docs `docs/api/Sim/`, `docs/api/Widgets/`. The hosts' scenarios are in the Consumers table's Sim
row (`releasing.md:506`: DropWatcher, LootHistory, BankLedger; this run adds MultiMeters and KickCD).

### 1.3 dev-copilot's WoW bump-version

- Base spec `commands/bump-version.md` (249 lines) with overlay markers `current-version`, `gate`,
  `targets`, `since`, `material`, `release-notes`, `update`, `history`, `report`, `no-commit`,
  `hard-rules`.
- WoW overlay `profiles/wow/bump-version.md` (391 lines, LF). Its `## extra — adds` (line 280) already
  carries two WoW-only steps, each saying where it runs (*The perf-skip exception…* "Runs in Step 4";
  *Write up the release run* "Runs after Step 4, before the Step 5 report"). `kind=standards|tooling`
  skip the overlay (line 13).
- **How the plugin tests its skills:** prose specs have no unit tests. The structural guard is
  `scripts/check_overlays.py` (live tree prints `OK: 13 overlays`), with its own suite
  `scripts/test_check_overlays.py` (15 cases); the checker allows only one section per id except
  `extra`, and an `extra` must say `adds`. A `###` subsection inside the existing `## extra — adds`
  needs no base marker and leaves the checker's count at 13. The other suites
  (`test_detect_profile.py`, `test_bounded_runs.py`, `test_normalize_eol.py`,
  `test_curseforge_journal.py`) are untouched but are the plugin's green gate (`CLAUDE.md:74–83`).
- The plugin's history is the `Current version:` paragraph in `CLAUDE.md:11` (no root CHANGELOG);
  `README.md:39` is the bump-version command row, whose third column carries the WoW behavior.

### 1.4 Where test-mode data and scenarios live in the addons (no convention)

A filename survey (`git ls-files`, excluding `libs/`, `tests/_kit/`, `docs/`) finds them under no
common name: `modules/Preview.lua` (AuraMaster, PartyFrameEnhanced, QuickComms),
`modules/Aggregator_Preview.lua` (MultiMeters), `modules/LedgerTable_TestMode.lua` (BankLedger),
`modules/TestMode.lua` (DropWatcher), `modules/Sim*.lua` + `core/SimSetup.lua`/`core/SimSeam.lua`
(BankLedger, DropWatcher, LootHistory), `settings/SimVerbs.lua` (DropWatcher), and tests such as
`tests/test_preview*.lua`, `tests/test_testmode.lua`, `tests/test_sim_*.lua`, `tests/sim_support.lua`.
Several addons (AbsorbTracker, KickCD, ConsumableMaster, PrettyChat, PGFE) match no name at all,
though some draw placeholders from inside a module. Any discovery must therefore be a heuristic
plus an owner correction, never a silent empty list.

---

## 2. The design

### 2.1 Standard (WS-25, WS-26): one rule, one evidence home

**Home of the rule: `preview-mode`**, a new unnumbered heading appended at the end of the file,
**`### Kept current at every release (MUST)`** (unnumbered, because `preview-mode` is one of the eleven
files with no numbered subsections; a `### N.` heading would break `check-standard.sh`). The rule
belongs with the things it is about (test mode, the marker, the simulator), and `versioning-git` gets a
one-bullet pointer so a reader of the release rules finds it.

Rule text (substance; WS-25 writes it in the file's voice):

- **MUST**, at every version bump of an addon that ships a test mode, a preview drawn by unlocking, or
  a simulator, re-look at:
  1. **Coverage** — every display element and feature this release adds or changes that the preview
     draws appears in the placeholder data; every event-driven feature added since the last release
     that a scenario could exercise is in a scenario step, or the scenario list says why not.
  2. **Currency** — data that names game content (item, spell, encounter, instance, currency and
     affix ids or names, the season's dungeon list, level and item-level ranges) matches the live
     season and patch the release targets (the TOC `## Interface:`).
  3. **Fidelity** — the placeholder data and the scenarios still drive the current render path,
     verbs and UI (no field the display stopped reading, no option that was removed, no step that
     drives a control that is gone).
- **MUST** record the outcome in that release run's `ANALYSIS.md`, under a release-only section
  `## Preview and simulation data` (automated-tests-§5, `AUTOMATED_TESTS.md` Step 2 template), with
  exactly one answer: **Current**, **Refreshed** (citing the commits), **Deferred** (with the reason;
  SHOULD cite a GitHub issue) or **Not applicable** (a frameless addon: no positionable display and no
  simulator). The section lists the files reviewed. `/dev-copilot:bump-version` asks the question and
  writes the section.
- **Why ANALYSIS.md:** it is MUST at release (automated-tests-§5), contributor-facing, frozen with the
  evidence, written by the same command that bumps, and it already exists in every addon. The README
  Version History is player-facing and an addon root may not carry a CHANGELOG (documentation-§1), so
  neither can hold it. A git commit message is not an option either: bump-version never commits in a
  WoW repo.
- **Commencement:** each addon's first release after v2.87.0. A release bundle frozen without the
  section before then is not backfilled (automated-tests-§5 already forbids backfill).
- **No anti-pattern number.** A missing section is a plain MUST finding against preview-mode. This
  keeps the change a note, as the owner asked, and avoids colliding with anti-pattern numbers other
  WS items in this run may take.

Ripple, split across two items so each stays reviewable:

- **WS-25 (normative):** preview-mode heading; versioning-git pointer bullet; automated-tests-§5 bullet
  (the release-only section); `AUTOMATED_TESTS.md` template section + Step 5 bullet; `STANDARDS.md`
  Sections blurbs for `preview-mode` and `versioning-git`; one ruling paragraph in the v2.87.0
  changelog entry WS-00 opened.
- **WS-26 (playbooks and pack):** `AUDIT.md` check after *Then check the simulator* (line 962); 
  `NEW_ADDON_CONTEXT.md` hard rule 18 (line 1626) gains one sentence and the Definition-of-done
  preview checkbox (line 1747) names the section for the first release run. `EXECUTIVE_SUMMARY.md` was
  checked and does not summarize preview-mode, so it is unchanged (WS-26 re-greps to confirm).

### 2.2 LibKa0s (LK-25): a library-local practice in `docs/releasing.md`

The standard cannot bind LibKa0s here (§1.1, `library-stack.md:338`), so the library's checklist
carries it on its own authority:

- **Step 5** (API documents) gains a closing paragraph, **"The preview and simulation re-look."** When
  the release moves the minor of `Sim.lua`, `SimTimeline.lua`, `SimPanel.lua` or the file(s) defining
  `W.TestStrip` and its flavors (`grep -l 'TestStrip' LibKa0s/*.lua`), re-read the fixtures and suites
  that exercise them (`tests/fixture_sim_panel.lua`, `tests/test_sim_*.lua`,
  `tests/test_widgets_teststrip.lua`, and any strip suite added this run) and the new API documents
  for those majors, against the change; and list which hosts' scenarios or test-mode strips the change
  affects (the Consumers table's Sim and Widgets rows), so step 8's re-vendor tells each host to re-look
  at its scenarios.
- **Step 7** (the release-notes line) gains a second fixed line after *Release gate (…)*:
  `Preview and simulation re-look: <Current|Refreshed|Deferred|Not applicable> — <files or reason>.`
  *Not applicable* is the answer when the release moved none of those minors. Precedent: the existing
  *Release gate* line in the same place.
- **Step 8** gains one sentence: a re-vendor that changes `Sim` or the strip carries the step-5 host
  list into each affected host's re-vendor report.
- No step is renumbered. The file stays CRLF and US English (`tests/test_prose.lua`).
- `CHANGELOG.md`: a bullet under the v1.76.0 block's docs/process heading LK-00 opened.

### 2.3 dev-copilot (DC-01): a gated question in the WoW bump-version overlay

A new `###` subsection inside the existing `## extra — adds` of `profiles/wow/bump-version.md`,
**"The preview and simulation re-look (Step 1b)"**, *Runs after Step 1, before the Step 2 gate.*
Placing it before the gate means a "stop" answer leaves the repo byte-for-byte untouched: the Step 2
battery writes a release bundle whatever its verdict, and a release bundle frozen without
`ANALYSIS.md` is itself a breach (automated-tests-§5).

Behavior:

1. **`kind=addon`.** Discover and list, with paths:
   - *Test-mode data*: tracked files outside `libs/`, `tests/_kit/`, `docs/` whose names match
     `(?i)(preview|testmode|test_mode|sample|placeholder|demo)`, plus files outside `tests/` that hold
     a placeholder table (`grep -lE '^\s*(local\s+)?[A-Z_]*(SAMPLE|PLACEHOLDER|PREVIEW|FAKE|DEMO)[A-Z_]*\s*='`).
   - *Simulator*: files named `Sim*.lua` / `*Sim*.lua`, and any file calling
     `LibStub("LibKa0s-Sim-1.0"`.
   - *Their suites*: `tests/test_*{preview,testmode,sim}*.lua`, `tests/sim_support.lua`.
   - For context, the commits since the last release (`git describe --tags --abbrev=0`, else the date
     of the top README Version History row) that touched `modules/`, `settings/`, `core/` versus those
     that touched the listed files, as two counts.
2. **Ask the owner** (AskUserQuestion), naming `preview-mode`, *Kept current at every release*, and
   the three checks (coverage, currency, fidelity), with these options:
   - **Current** — proceed; recorded as Current.
   - **Refreshed** — proceed; the owner names the commits (or the command lists those that touched the
     files since `<since>` for confirmation).
   - **Stale — stop now** — the bump stops here, nothing is modified, and the report names the files
     to refresh. No bundle exists yet because the gate has not run.
   - **Release anyway (Deferred)** — proceed; the owner gives the reason (and optionally an issue),
     recorded as Deferred.
   - **Not applicable** — only offered when discovery found nothing; the owner confirms the addon has
     no positionable display and no simulator, else names the files the heuristic missed.
   An empty discovery list never becomes Not applicable silently: the question is always asked.
3. **`kind=library`.** Ask only when the commits since the last tag changed `LibKa0s/Sim*.lua` or a
   file defining `TestStrip`; list those files plus the fixtures and `docs/api/` folders named in
   `releasing.md` step 5. Otherwise record *Not applicable — this release did not change Sim or the
   strip* without asking, and say so in the report.
4. **Record the answer** in the release write-up:
   - addon: *Write up the release run*, item 1, writes the `## Preview and simulation data` section of
     the bundle's `ANALYSIS.md` from the Step 1b answer (answer, files reviewed, commit counts, note);
   - library: Step 4's CHANGELOG entry ends with the `Preview and simulation re-look:` line beside the
     release-gate line.
5. **Report** (`report — replaces`) gains one bullet: the answer and where it was written.
   **Hard rules** (`hard-rules — replaces`) gain one: never skip the Step 1b question, never infer the
   answer, never write *Not applicable* for an addon whose discovery list was empty without the owner's
   confirmation.
6. The overlay preamble (lines 3–9) gains one clause naming the re-look.

Ripple: `CLAUDE.md:11` 2.5.0 history clause (DC-00 opens the number; DC-01 writes its clause),
`README.md:39` third column gains "and asks whether the test-mode data and simulator scenarios are
still current (Step 1b)". `docs/ARCHITECTURE.md` lists commands only (lines 69, 84), so it is
unchanged.

**Tests.** No prose test exists to extend, and a grep-for-a-heading test would be the "test that
cannot fail" shape the standard warns about. The guards are: `python3 scripts/check_overlays.py`
still prints `OK: 13 overlays` (the new text sits inside the existing `extra` section, so a stray
`## ` heading or a duplicate id would fail it), the five script suites stay green, and the owner's
smoke runs the command against a sim host and stops at Step 1b.

---

## 3. Decisions taken, and why

| # | Decision | Why |
|---|---|---|
| D1 | The rule lives in `preview-mode`, with a pointer in `versioning-git` | The subject is test mode and the simulator. `versioning-git` is 15 lines of one-line bullets and is the place a release reader looks, so it gets the pointer. |
| D2 | Evidence is a release-only `ANALYSIS.md` section | The only contributor-facing, frozen, release-MUST artifact an addon already writes, and the bump command already writes it. |
| D3 | The question runs before the gate (Step 1b) | A "stop" answer must leave nothing behind: the gate writes a bundle on every run, and a release bundle without `ANALYSIS.md` breaches automated-tests-§5. |
| D4 | Four answers, plus a stop option that records nothing | "Never blocks silently": the owner can stop (and is told why and what to refresh) or release with a recorded deferral. A rule that only allowed "current" would get routed around. |
| D5 | No anti-pattern number, no tracking issues | Owner B3 says "note", "no tracking issues". It also avoids colliding with numbers other WS items in this run may take. |
| D6 | LibKa0s carries it in `releasing.md` only, not via the standard | `preview-mode` does not bind a library (`library-stack.md:338`); widening that applicability list for one line would be the bigger change. |
| D7 | No step renumbering in `releasing.md` | Steps 1, 5 and 7 are cited by number from `CLAUDE.md` and `tests/test_versioning.lua`. |
| D8 | Discovery is heuristic and always confirmed | No naming convention exists across the fourteen addons (§1.4). Making one a MUST would be its own change. |
| D9 | DC-01 depends on WS-25 | The overlay cites the standard's heading text and the `ANALYSIS.md` section name, so it must follow them. |

## 4. Risks

- **Heading collisions in `preview-mode`.** Other WS items in this run (the sim strip, the header
  word) also edit `preview-mode.md`. WS-25 appends a new heading at the end of the file and runs after
  them in id order, so the risk is low. Re-read the file before editing.
- **Changelog ruling numbering.** The v2.87.0 entry is shared, so WS-25 numbers its paragraph after the
  ones already there, and the lead's landing pass renumbers the paragraphs if needed.
- **This run's own releases.** LibKa0s v1.76.0 changes `SimPanel`/`SimTimeline` and the strip, so LK-90
  (lead-owned) should be the first to write the `Preview and simulation re-look:` line. If the
  installed plugin is still 2.4.0 when LK-90 runs, the line is written by hand per `releasing.md`
  step 7. No addon version is bumped in this run, so the addon side first fires at the next release.
- **Installed plugin.** The step only takes effect after dev-copilot 2.5.0 is merged and the owner runs
  `/plugin update` and `/reload-plugins` (memory: *Use the installed plugin*).
- **Heuristic noise.** The placeholder-table grep may list a file that is not preview data. The owner
  corrects the list at the question, and the corrected list is what gets recorded.
