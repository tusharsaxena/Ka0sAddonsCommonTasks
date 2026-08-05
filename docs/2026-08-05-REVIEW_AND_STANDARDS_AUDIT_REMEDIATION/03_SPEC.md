# 03 — Spec

**The normative end state, per cluster. What "done" looks like — not when it happens.**

Nothing here has been executed. See `00_OVERVIEW.md`. For sequencing, see `04_EXECUTION_PLAN.md`.

---

## How to read this

Each cluster carries three things:

- **Target** — the behavior or shape that must exist when the cluster is closed.
- **Acceptance** — how you know, stated as a check somebody can run or a state somebody can look at.
- **Out of scope** — what this cluster deliberately does not fix, so nobody widens it silently.

RFC-2119 words are used in their standard sense. Where this spec contradicts
`WowAddonStandards/standards/STANDARDS.md`, the standard wins — except where the cluster's whole point
is that the standard is what changes, in which case the change is specified in `02_UPSTREAM_CHANGES.md`
and this spec describes the post-change state.

**The two gates, once, because four clusters depend on the distinction.** A **commit** is gated on
`lint` + the harness and nothing else (`testing-§4`). A **tag** is gated on all four suites at `pass`
plus `suites.complexity.warnings == 0` — zero functions above CCN 15 (`automated-tests-§3`) — evaluated
by `/wow-addon:bump-version` from the run's `manifest.json`, where a `skip` blocks as NOT EVALUATED
rather than reading as a pass. One narrow exception: `perf` skipped because the addon ships no
`tests/perf.lua` passes the gate and MUST be stated in the release notes.

---

## Collection-wide invariants

These hold at every point in the plan, including mid-milestone.

1. **All four suites stay green in every repo.** No work item may be left in a state where
   `luacheck .` is non-zero or `lua5.1 tests/run.lua` reports a failure. Where a new gate is expected to
   redden a repo (`M1-LK-04`'s suite inventory, `M1-LK-05`'s parity cases), the reddening and its fix are
   the **same** work item. Two corollaries, both learned the hard way in review:
   - **`M3-01` re-vendors `libs/LibKa0s/` and `tests/_kit/` in the same commit as `M3-02`'s rewrite and
     the provenance-line bump.** The vendor-sync gate reads the README provenance line as its input and
     compares **both** pairs against that tag (`AbsorbTracker/tests/test_vendor_sync.lua:100-102`,
     `:138-141`, `:144-149`). Bumping the line without re-vendoring the library half points six repos'
     gates at a tag whose `LibKa0s/` bytes they do not hold, and case #1 goes red in all six.
   - **The consumer-side gate keeps its one CR strip.** See C6. Deleting it reddens seven repos on the
     adopting commit.
2. **Frozen bundles are never edited.** `docs/audits/<date>/`, `docs/reviews/<date>/` and
   `docs/automated-tests/<stamp>/` are evidence. Their British spellings, their retired `§N.M` citations
   and their impossible `durationMs` values stay exactly as recorded.
3. **`libs/LibKa0s/` and `tests/_kit/` are never patched in place.** They are whole-folder vendored
   payloads (anti-pattern #48). A defect there is fixed upstream and re-vendored.
4. **Every count claim names its members.** A bare "three docs" or "five topic-detail docs" is the shape
   that goes stale silently. The four sets this plan uses, written out once here and referenced by name
   everywhere else:
   - **The root doc set** — exactly three docs plus `LICENSE`: a full `README.md`, a stub `CLAUDE.md`, and
     `DEPENDENCIES.md` (`documentation-§1`/`§2`/`§7`).
   - **The `docs/` canonical trio** — `ARCHITECTURE.md`, `testing.md`, `smoke-tests.md`
     (`documentation-§3`).
   - **The five required topic-detail docs** — `test-cases.md`, `performance.md`, `perf-runs/README.md`,
     `automated-tests/README.md`, `automated-tests/RESULTS.md` (`documentation-§3`). `M1-STD-01` makes
     `perf-runs/README.md` conditional on the perf exemption, so this count is about to become
     conditional — which is exactly why it is never written bare.
   - **The twelve README sections, in order** (`documentation-§1`) — H1 title, badge row, logo,
     description, `## What's new`, `## Screenshots`, `## Usage`, `## How <it> works`, `## FAQ`,
     `## Troubleshooting`, `## Issues and feature requests`, `## Version History`.
   - **The five CLAUDE.md stub items, in order** (`documentation-§2`) — H1 title
     (`# CLAUDE.md — Ka0s <Name>`), adherence line, `## Standards compliance (read first)`, the
     "read the docs" pointer list, the green-gate line.
5. **US English throughout** — `color`, `gray`, `behavior`, `center`, `canceled`, `-ize`/`-ization`
   (`localization-§5`). Two exemptions: Blizzard and third-party symbols reproduced verbatim, and frozen
   research evidence.
6. **Section references are `filename-§N` only.** The global `§N.M` numbering is retired. Five section
   files carry no numbered subsections and are always referenced by bare filename: `lint`, `packaging`,
   `preview-mode`, `standalone-windows`, `audit-review-history`.

---

# Part A — Upstream end state

## C1 — Perf harness adoption is conditional, and a decline is a compliant state

**Target.** `performance` gains a twelfth section defining a **no-combat-path exemption**. An addon
qualifies when criterion (a) holds — no `OnUpdate` handler, no repeating ticker, and no event handler
doing more than occasional work while the player is in combat, proven by a committed whole-repo sweep of
`RegisterEvent` / `SetScript("OnUpdate"` / `C_Timer` naming the per-event work — **and** it names
whichever of (b) "every declared bucket would read 0.000 by construction" or (c) "suspend would suppress
the data the addon exists to record" applies.

An exempt addon:

- Does **not** ship `core/PerfSetup.lua`, `<Addon>PerfDB`, a `perf` verb registration, a suspend/resume
  contract, `tests/perf.lua`, or `docs/perf-runs/README.md`.
- **Does** still vendor `libs/LibKa0s/` whole; still reserves `perf` so it can mean nothing else; still
  ships `docs/performance.md`, shrunk to a one-screen page stating that the addon brackets nothing and
  why; and still carries `automated-tests-§3`'s `perf: skip` sentence in its release notes.
- Records the exemption **once**, in the deviation register (C4), with a re-check trigger: the first
  `OnUpdate`, repeating ticker or in-combat event handler re-arms the full wiring MUST.

The three wired addons — AbsorbTracker, ConsumableMaster, KickCD — remain bound by the full section, and
their residual gaps are genuine work, not counting artifacts.

**Acceptance.**
- `performance.md` carries `### 12.` and no existing `performance-§N` reference has renumbered.
- BankLedger, LootHistory, PanelMaster, prettychat and WhatGroup each carry one register row with a
  committed sweep and a re-check trigger, plus a `docs/performance.md`.
- A fresh `/wow-addon:standards-audit` in each of those five files **zero** open MUST rows for the perf
  cluster.
- ConsumableMaster ships `tests/perf.lua` with a zero-overhead scenario, `ConsumableMasterPerfDB` in
  `.luacheckrc`, `docs/performance.md` and `docs/perf-runs/README.md`. KickCD ships `tests/perf.lua`,
  `docs/performance.md` and `docs/perf-runs/README.md`, and `core/PerfSetup.lua:104-118`'s cited figures
  either resolve to a committed capture or are removed.

**Out of scope.** Persuading any of the five to adopt the harness. Retro-fitting captures for past
releases. Changing what `Perf` measures.

---

## C6 — A test that cannot look reports a skip, not a pass

**Target.** `testkit/framework.lua` exports `Kit.skip(reason)`. A skipped case is a third status:
counted separately, printed as `SKIP  <name> — <reason>`, rendered in the `--list` inventory with its
reason, **never** folded into `passed`, and **never** changing the process exit code.

`testkit/vendor_sync.lua` is the single implementation of the consumer-side vendored-payload gate,
exposed as `VendorSync.register(T, opts)`. Every repo vendoring `libs/LibKa0s/` calls it. When the sibling
checkout is absent the case calls `Kit.skip` with a reason naming the missing checkout.

**The comparison contract, exactly.** The consumer-side gate compares a **working-tree file** against a
**`git show` blob**, and those are not the same representation: the blob is LF, the working tree is CRLF in
eight of the nine repos (`.gitattributes` pins `text=auto eol=crlf` or `*.lua text eol=crlf`). Measured:
`git -C LibKa0s show HEAD:LibKa0s/Core.lua | tr -cd '\r' | wc -c` → **0**;
`tr -cd '\r' < AbsorbTracker/libs/LibKa0s/Core.lua | wc -c` → **322**. So the gate reads raw bytes in
binary mode and applies **exactly one** normalization — **CR stripped from the working-tree side, nothing
else** — which compares the file to the blob it round-trips to; or, equivalently and normalization-free,
compares `git hash-object <local file>` against the sibling's blob sha. A real fork in content still fails.

`testing-§11` covers both halves — the library repo's kit-sync gate and the consumer-side payload gate —
states that the reason MUST be visible in the case's own recorded result rather than only in a header
comment, and **scopes its no-line-ending-normalization MUST to the library-side pair**, where `testkit/`
and `tests/_kit/` are two working-tree directories in one checkout. Extending that MUST to the
blob-versus-worktree comparison would redden the gate in every consumer on the commit that adopts it,
which is why `ConsumableMaster/tests/test_vendor_sync.lua:133`'s `gsub` is **correct and stays**.

**Acceptance.**
- `grep -n "Kit.skip" LibKa0s/testkit/framework.lua` resolves.
- In each of AbsorbTracker, BankLedger, ConsumableMaster, KickCD, LootHistory, PanelMaster,
  prettychat and WhatGroup, `tests/test_vendor_sync.lua` is a call into `tests/_kit/vendor_sync.lua`
  and contains no `if not tag then return end`.
- Temporarily renaming the sibling checkout makes those cases report SKIP with a reason, and the run's
  exit code stays 0.
- Every repo's gate carries the one documented CR strip on the working-tree side (or the `git hash-object`
  equivalent) and no other normalization, with the header explaining why — carried in verbatim from
  `AbsorbTracker/tests/test_vendor_sync.lua:28-32`.
- `docs/test-cases.md` in each repo discloses the skip.
- Pass counts and README `[tests]` badges are unchanged from today's figures; WhatGroup and prettychat gain
  two cases each, being the two repos with no gate today.

**Out of scope.** Making the gate pass without a sibling. Running the comparison in CI (no repo has
`.github` or git hooks today).

---

## C8 — Every gate statement names its checkpoint

**Target.** The sentence `LibKa0s/testkit/run-automated-tests.sh:372` emits into every `RESULTS.md` names
the checkpoint per suite: `lint` and `tests` gate the run and the commit; `perf` and `complexity` never
fail a run or block a commit; the **tag** is gated on all four suites at `pass` plus zero functions above
CCN 15, evaluated by `/wow-addon:bump-version` from the run's `manifest.json`, where a `skip` is NOT
EVALUATED rather than a pass.

`automated-tests-§4` makes that content a MUST on the emitted text. `testing-§6` and `documentation-§3`
make the hand-written gate table in `docs/testing.md` carry the checkpoint per suite, so
`Gates? no — recorded only` cannot stand unqualified. `revendor-standards` gains a sweep (**3f**) that
rewrites the hand-written half in every repo.

The manifest's `gating` boolean is replaced by a `gates` object naming both checkpoints, with the legacy
boolean retained for one revision.

**Correction carried into this spec.** `bump-version` evaluates the release gate from
`suites.<name>.status` and `suites.complexity.warnings` (`commands/bump-version.md:45-54`); it never reads
`gating`. The gate is **not** broken today. This cluster fixes generated prose and a misleading manifest
field, nothing more.

**Acceptance.**
- A fresh run in any repo writes a `RESULTS.md` lead-in naming both checkpoints.
- `grep -rn "never fail a run" <repo>/docs/` returns only checkpoint-qualified sentences, in all nine
  repos.
- ConsumableMaster's `CLAUDE.md:71` and KickCD's `CLAUDE.md:74` no longer read as unqualified.
- `bump-version`'s gate evaluation is unchanged and still refuses on any `skip` other than the sanctioned
  perf exception.

**Out of scope.** Requiring an addon to restate the release gate's mechanics. Editing frozen `RESULTS.md`
history — the file is overwritten in place and its git history is the trend line, so past rows keep their
past wording.

---

## C12 + C13 + C18 + C33 — the rest of the shared-payload end state

### C12 — Load lists are derived and pinned

**Target.** `testkit/loader.lua` exports `Loader.xmlFiles(xmlPath)`, returning directory-prefixed,
forward-slashed paths in XML order and raising on a missing file. `Kit.assertSuiteInventory(dir, suites)`
fails on either asymmetry between `<dir>/test_*.lua` and the declared list, with distinct messages per
direction. `loadSuites` raises on a declared-but-absent suite; the write-in-progress affordance survives
as an explicit `{ name = …, pending = … }` entry that registers as a skip. `testing-§9` names the suite
list as the third list that MUST be pinned.

**Acceptance.** Every runner's vendored-library list is **either** derived via `Loader.xmlFiles` **or**
pinned against `libs/LibKa0s/LibKa0s.xml` by a case — which is the property `testing-§9` actually wants,
and the reason the earlier "no repo's runner contains a hand-typed list" wording was both unreachable as
scheduled and stricter than the rule. Measured today: BankLedger, ConsumableMaster, LootHistory,
prettychat and WhatGroup already pin their eight-entry list by a case (`tests/test_libka0s.lua` /
`tests/test_harness.lua`); **AbsorbTracker, PanelMaster and KickCD do not**, and PanelMaster's unpinned
**six**-of-eight list at `tests/run.lua:24-31` is exactly how `PM-A-10` survived. `M3-03` covers those
three; `M3-03b` covers ConsumableMaster's and KickCD's post-kit runners.

`LibKa0s/tests/run.lua:17-19` is a `Loader.xmlFiles` call. Deleting a suite file, or adding one without
declaring it, reddens the run in every kit-consuming repo. PanelMaster's harness loads eight library
files, not six.

**Suite-list balance, measured now so a later drift is visible.** Suites on disk versus declared:
AbsorbTracker **21/21**, BankLedger **20/20**, LootHistory **19/19**, PanelMaster **20/20**, prettychat
**16/16**, WhatGroup **14/14**; ConsumableMaster auto-discovers and has no declared list.
BankLedger (`tests/test_harness.lua:22-32`) and PanelMaster (`tests/test_harness.lua:19-32`) **already ship
this gate** and are the reference implementations `Kit.assertSuiteInventory` should match.

**Out of scope.** Deriving the *addon's* own file list where a repo already does it correctly. Making the
loader parse nested XML includes — `LibKa0s.xml` is flat.

### C13 — The standard says what binds a library repo

**Target.** `library-stack-§7` carries an *Applicability* block enumerating what binds a Ka0s-owned
library repo (`testing-§1/§9/§10/§11`, `lint`, `automated-tests`, `versioning-git`, `localization-§5`,
`documentation-§5`, `documentation-§7`), what does not (`documentation-§1`'s player README and badge row,
`documentation-§2`'s addon stub as written, `documentation-§3`'s `docs/` trio (`ARCHITECTURE.md`,
`testing.md`, `smoke-tests.md`) and the five required topic-detail docs (`test-cases.md`,
`performance.md`, `perf-runs/README.md`, `automated-tests/README.md`, `automated-tests/RESULTS.md`),
`toc-file`, `options-ui`, `slash-commands`, `preview-mode`, `savedvariables`,
`packaging`), and what substitutes: a root `CLAUDE.md` carrying `## Standards compliance (read first)`,
a root `DEPENDENCIES.md`, and a README pointer to the standard. `ADDONS.md` carries a second table listing
LibKa0s.

**Acceptance.** LibKa0s ships a root `CLAUDE.md` and `DEPENDENCIES.md`; `README.md` names the standard.
A fresh audit of LibKa0s files zero `documentation-§1`/`§2`/`§3` rows.

**Out of scope.** Adding LibKa0s to the addon roster. Writing `docs/ARCHITECTURE.md` or `docs/testing.md`
for LibKa0s — the applicability block declares those addon-scoped and the content already exists at
`README.md:121-159` and `:196-231`.

### C18 — The executable bit lives in the git index

**Target.** `git ls-files -s` reports **`100755`** for `tests/_kit/run-automated-tests.sh` in all eight
addons and for both `testkit/run-automated-tests.sh` and `tests/_kit/run-automated-tests.sh` in LibKa0s.
`automated-tests-§2` prescribes `git update-index --chmod=+x`, not `chmod +x`, and names the DrvFs /
`core.fileMode=false` trap. A kitsync or vendor-sync case asserts the recorded mode. The plugin's two
vendoring steps use the index-mode form and verify it.

**Acceptance.** `for r in …; do git -C "$r" ls-files -s tests/_kit/run-automated-tests.sh; done` prints
`100755` nine times (counting LibKa0s's two paths). A fresh clone on a case-sensitive filesystem runs
`tests/_kit/run-automated-tests.sh` without `bash`.

**Out of scope.** Changing `core.fileMode` in any repo. Editing frozen bundles that recorded the old mode.

### C33 — Durations cannot be negative

**Target.** `run-automated-tests.sh` resolves a millisecond time source once (`date +%s%3N`, else
`$EPOCHREALTIME`, else seconds × 1000), clamps every emitted duration to `>= 0`, and records which source
was used beside the tool versions in `manifest.json`.

**Acceptance.** A fresh run in any repo emits no negative `durationMs`; sub-second suites emit a non-zero
value where the source supports it; the manifest names the timing source.

**Out of scope.** Rewriting the five committed manifests carrying `-1000` and `-2000`.

---

## C2 (upstream half), C9, C11, C15, C17, C20, C21, C27 — the remaining upstream shape

### C2 upstream — a stub surface is asserted as a set

**Target.** `testkit/framework.lua` exports `Kit.assertSurfaceParity(live, degraded, label)`, reporting
**all** divergences in one message and treating a present-but-nil-valued function key as a divergence.
`testing-§8` MUSTs a stub-surface parity case per adopted LibKa0s module, with the degraded arm produced
by feeding the loader a partial file list (never by hand-stubbing the member under test) and the
grep that produced the member list named in the case comment. Anti-pattern **#56** names the class.

**Acceptance.** Anti-patterns run to #56. Each addon carries one parity case per adopted seam. The three
repos with known drift redden before they are fixed.

**Out of scope.** Catching a stub with the right member set and a wrong implementation — `KCD-A-14` and
`PM-R-03` are `debug-logging-§7` violations and stay addon-side.

### C9 — A perf record asserts only what was observed

**Target.** `LibKa0s/Perf.lua` records **observed** containment beside the declared `within`; the nesting
note refuses to assert containment for a declared parent never observed; `P.Cancel` clears `P.context`;
and the bracket docstrings state the real off-path cost. `performance-§2` names both bracket shapes — the
inline `local t0 = Perf.on and debugprofilestop()` for a single-exit hot path, the `Open`/`Close` pair for
a multi-exit region — and `performance-§3` requires containment be verifiable.

**The mechanism must match the idiom actually deployed.** Containment is supplied at the **recording**
call — `P.Note(key, ms, parentKey)`, defaulting to the declared `P.BUCKET_WITHIN[key]` when omitted — not
inferred from a `P.Open`/`P.Close` stack. Verified: **zero** `P.Open` / `P.Close` call sites exist anywhere
in the collection; all three wired addons (AbsorbTracker at `core/AbsorbTracker.lua:184`,
`modules/Timer.lua:41`, `modules/Display.lua:105`, `:165`, `:202`; KickCD's nine sites across `Castbar`,
`Cooldowns`, `IconGrid`, `IconGrid_Render`; ConsumableMaster's two) use the inline `Perf.Note` form.
Independently, `P.Open()` (`LibKa0s/Perf.lua:400-403`) takes **no key**, so a stack slot has no identity
while a child bracket is open and `parentKey` is unknowable. If the pair is retained its signature becomes
`P.Open(key)`.

**Acceptance.** After `M3-12` passes the parent at `modules/Display.lua:105` and `:165`, a capture in
AbsorbTracker reports `visibility` as observed inside `appearance`, not `repaintPass`, and
`addNestingNote` prints "declared but not observed" for any bucket whose call site supplies nothing. A
`perf report` after `perf cancel` carries no context stamp. The library holds a zero-overhead case proving
the bookkeeping is free with `P.on` false.

**Not in this cluster's acceptance:** unbalanced-bracket detection. `KCD-R-05` / `KCD-A-18`'s two leaked
exits are `Note`-shaped, not `Open`/`Close`-shaped, so no stack bookkeeping surfaces them. They close by
`M3-12`'s hand edit plus its per-bucket reachability case.

**Explicit do-not-execute.** Both AbsorbTracker bundles direct you to drop `within` from `visibility`.
`modules/Display.lua:100` calls `ApplyVisibility` inside the open `appearance` bracket, so `visibility`
**is** nested — in `appearance`. Dropping `within` substitutes one false claim for another. The correct
declared value is `within = "appearance"`, and the durable fix is that the library stops trusting the
declaration.

**Out of scope.** Changing what `Perf` measures or the record schema's existing fields. Adding scenarios
to the library — `performance-§9` keeps them per-addon.

### C11 — The secret-safe printer rule is enforceable

**Target.** `events-frames-taint-§8` is either scoped to sites that can receive a combat-protected value,
with those APIs named and the rest demoted to a SHOULD carrying the drift rationale; **or** LibKa0s ships
a varargs printer so the compliant form (`NS.Print("%s = %s", k, v)`) is no longer than the bypass, and
the MUST stays unscoped. One of the two, stated in the section.

Independently of which is chosen: **no addon calls the global `print()` for user-facing output.**
`BankLedger/modules/Browser.lua:917` and `:926` are a real defect — two chat lines without the `[BL]` tag
every other line carries — and are fixed regardless.

**The (a)/(b) choice is a prerequisite recorded here, before Milestone 1 begins.** The two branches
differ by roughly two orders of magnitude in cost and cannot both be planned: (a) is one paragraph in the
standard plus a re-grade, and `M4-27` becomes a **disposition, not a fix** — the five findings close by
re-grading and recording, with the cited code untouched. (b) is a **LibKa0s API addition**, which under
this plan's hard rule must be a Milestone-1 item: `M1-LK-15`, carrying a `Core.lua` minor bump, an API
document, `tests/test_versioning.lua` pairing, inclusion in `M1-LK-14`'s release, and a re-vendor into all
eight addons (`M3-01`, library half) before a single call site can be converted. `M1-LK-15` is written into
Group A as **CONDITIONAL** so that (b) does not leave a downstream item pointing at an unscheduled upstream
change. Under (a) the plan has 96 work items; under (b), 97.

**Acceptance.** The section states its scope. `grep -n '\bprint(' modules/Browser.lua` in BankLedger
returns only comments. Under option (b), the ~50 pre-formatting sites in AbsorbTracker, KickCD,
PanelMaster and WhatGroup are converted, and `M4-27` depends on `M1-LK-15` and `M3-01` as well as on
`M1-STD-11`.

**Out of scope.** Converting sites in `libs/` or in frozen bundles.

### C15 — A section reference either resolves or is a defect

**Target.** `documentation-§6` grades reference defects: retired global `§N.M` is a **SHOULD**, swept
mechanically; a **malformed or out-of-range** reference is a **MUST** fix. Frozen bundles are exempt.
`revendor-standards` sweeps the whole repo except `libs/`, `tests/_kit/`, `docs/audits/`,
`docs/reviews/` **and `docs/automated-tests/`** — all three `docs/` paths are frozen evidence and exempt by
invariant 2 — range-checks each `filename-§N` against the fetched section file's local heading count, and
applies code and config edits only on confirmation, comment-only. An audit records the sweep as one
rolled-up finding with the command that produces the count.

**Acceptance.** `grep -rEn '§[0-9]+\.[0-9]' <repo>` **excluding all five paths** returns zero in all nine
repos (368 sites today: AbsorbTracker 83, LibKa0s 183, KickCD 39, ConsumableMaster 38, WhatGroup 13,
LootHistory 7, BankLedger 3, PanelMaster 1, prettychat 1). `AbsorbTracker/settings/Slash.lua:199`'s
`slash-commands-§:` and BankLedger's `options-ui-§41`/`§190`/`§189` resolve or are corrected.
`standalone-windows` and `packaging` are cited by bare filename everywhere.

**Two measured facts the acceptance depends on.** (1) `docs/automated-tests/` must be in the exclusion
list or the criterion is unreachable without corrupting evidence: KickCD carries **30** `§N.M` lines inside
frozen bundles (`20260804-182144/`, `-214315/`, `-233245/`, in `test-cases.md` and `tests.txt`), so the
four-path exclusion returns 69 for that repo and the five-path exclusion returns **39**. Those 30 are
evidence and are expected to survive. (2) LibKa0s's two **shipped-source** hits —
`LibKa0s/LibKa0s/Options.lua:129` and `:173` — are swept in **`M1-LK-10`**, not `M3-07`, because that file
is vendored byte-for-byte into all eight addons (`diff -q` against `AbsorbTracker/libs/LibKa0s/Options.lua`
→ identical) and changing it after `M3-01` would redden eight consumers' vendor-sync gates against a
payload they may not patch (invariant 3), with no second re-vendor scheduled. `M3-07` must not touch
`LibKa0s/*.lua`.

**Out of scope.** Editing frozen bundles. Requiring the notation in files that carry no standards
reference today.

### C17 — Rules state their applicability

**Target.** `architecture-§4`'s two-senders MUST states its scope: it binds an addon with two or more
feature modules, or any module registering game events. Below that, direct calls are permitted and
`docs/ARCHITECTURE.md`'s `## Message Bus` section records that there is no bus and why. The rule is
changed rather than register-rowed because the defect is in the rule — a MUST that **no** single-module
addon can satisfy will be re-filed against every future single-module addon.

**Not in scope any more: an `events-frames-taint-§1` carve-out.** An earlier draft also carved a permanent
exception for unit-filtered registration on the evidence of `AT-A-10` — one **Info** row, one repo, with a
sound justification already written at `AbsorbTracker/docs/ARCHITECTURE.md:316-331`, exactly where the
process asks. That is the designed input to `M1-STD-02`'s register, not to a shared normative document
every other addon reads. `AT-A-10` closes as an `M3-08` register row with a re-check trigger.

**Acceptance.** prettychat carries the recorded paragraph (it already does) and is not filed again;
AbsorbTracker carries a register row citing `events-frames-taint-§1` with its re-check trigger. KickCD has exactly one sender for `Ka0s_KickCD_CONFIG_CHANGED` and one for
`Ka0s_KickCD_PROFILE_CHANGED`, and `docs/ARCHITECTURE.md:118`/`:120` agree with the code.

**Out of scope.** Introducing a bus into prettychat.

### C20 — English-only is a terminal compliant state

**Target.** `localization`'s routing SHOULD has two terminal compliant states: strings routed through
`NS.L`, **or** an English-only decision in the deviation register with a re-check trigger (the first
non-English locale file). Both MUSTs — seam exported, `enUS.lua` ships — stay unconditional.

**Acceptance.** AbsorbTracker, PanelMaster, prettychat and WhatGroup each carry one register row.
WhatGroup's five dead keys (`locales/enUS.lua:67-70`, `:104`) are deleted or wired.

**Out of scope.** Actually translating anything.

### C21 — A host can read every layout constant it needs

**Target.** `LibKa0s/Options.lua` publishes **`PADDING_X`** on the instance as an **individual scalar** —
never the `lib.LAYOUT` table, because handing out the table lets one host's mutation retune every other
host's panels. A case pins that every `lib.LAYOUT` key is either published or carries an in-file comment
saying why it is internal.

**One scalar, not six.** An earlier draft published `HEADER_TOP`, `HEADER_HEIGHT`, `DEFAULTS_W`,
`SECTION_TOP_SPACER` and `SECTION_BOTTOM_SPACER` as well. **None of the five has a demonstrated consumer
anywhere in the collection.** The only host copy in evidence is KickCD's `core/Constants.lua:66`
(`KCD-A-03`), and this cluster's other finding, `CM-A-05`, is already fixable against the three constants
published today (`ROW_VSPACER`, `SECTION_HEADING_H`, `BUTTON_PAIR_REL`). Publishing on frequency rather
than on a demonstrated need is anti-pattern **#55** verbatim — *"promoting a shape into a shared lib
because it is repeated, rather than because it is shared … under the additive-only rule a wrong shared
abstraction is surface the library keeps forever"* (`library-stack-§7`, added at v2.21.0). Each of the five
is published the day a host demonstrates it needs it; the pinning case is what keeps that decision visible.

**Acceptance.** KickCD's `core/Constants.lua:66` is deleted and `settings/Panel.lua:307` reads
`O.PADDING_X`; `settings/Panel.lua:426`'s local no longer overwrites `O.ROW_VSPACER` at `:430`.
ConsumableMaster's `settings/Panel.lua:74-75` locals are deleted. No panel moves a pixel.

**Out of scope.** Retuning any value.

### C27 — US English is fixed at the source

**Target.** `LibKa0s/*.lua` and `testkit/*` carry no British spellings in authored comments or
docstrings, and a guard case fails the LibKa0s run on a regression, listing `file:line`. Consumers close
their own findings by re-vendoring.

**Acceptance.** The guard case exists and is green. WhatGroup's `libs/LibKa0s/` hit count is zero after
its next re-vendor. KickCD's remaining hits are in
`docs/superpowers/plans/2026-08-04-ccn-elimination.md` at `:51, :53, :57, :117, :121, :123, :147, :149,
:213` and are swept locally.

**Out of scope.** Identifiers, `lib.SKIN` keys, Blizzard symbols, released CHANGELOG entries, frozen
bundles.

---

# Part B — Addon end state

## C2 (addon half) — a degraded install degrades, and says so honestly

**Target.** With `libs/LibKa0s/` absent or failing LibStub's floor, every addon:

- **Loads without raising.** No bare call on a nil stub member, in any code path a user can reach.
- **Keeps every host-owned verb working.** `slash-commands-§1`: the host verbs never went to the library,
  so they keep working. A stub that blacks out the whole command surface is non-compliant.
- **Renders help on a bare `/<slash>`** (`slash-commands-§3`), listing the verbs that still work.
- **Says one honest line about what is unavailable**, and does not tell the user to use a command that
  answers "unavailable".
- **Answers repeatedly.** A latched "said once" explanation that then goes silent is worse than an error.

Specifically, the eight repos' known defects:

| Repo | Required end state |
|---|---|
| ConsumableMaster | `KCM.Settings.Helpers` **is** the library instance, not a copy-across table (`options-ui-§1`). `RefreshAllPanels` and `RefreshScalars` are present and callable on both paths. `settings/Panel.lua:636`'s `if coerced == nil and value ~= nil` no longer lets an explicit nil bypass validation and delete a key. `settings/Slash.lua:341` dispatches the 11 host-owned verbs; only `help/get/set/list/reset` degrade, and `settings/Panel.lua:265-271`'s text agrees with `settings/Slash.lua:300-303`. |
| PanelMaster | The `settings/Slash.lua` stub assigns `FormatKV`, and a parity case pins the whole member set. `/pm config` answers on every invocation, not once. |
| LootHistory | The Slash stub exports `HelpHeader`. Bare `/lh` prints help listing show/hide/toggle/config/debug/test/purge. |
| KickCD, PanelMaster | The DebugLog stub prints its ack (`debug-logging-§7` requires it) **without** re-implementing the library's line format or its state hexes. |

**Acceptance.** Each repo carries a `Kit.assertSurfaceParity` case per adopted seam, green. Each repo has
a degraded-load case that exercises a **write** through the settings path, not only a read — the gap
`CM-R-04` names. `lua5.1 tests/run.lua` green in all eight.

**Out of scope.** Making a degraded install fully functional. Supporting a LibKa0s older than the floor.

---

## C3 — a comment's named file or caller exists

**Target.** No comment in an addon's own source (excluding `libs/` and `tests/_kit/`) names a file that
does not exist, a caller that does not call, or a line number that does not resolve. `sync-docs` carries
a comment-citation check that reports violations with `file:line` and applies comment-only edits on
confirmation.

**Acceptance.** The eleven cited comments are corrected or deleted:
`AbsorbTracker/modules/Bar.lua:5-6, :86-87`; `BankLedger/settings/Panel.lua:11` and the duplicated
paragraph at `:471-476`; `ConsumableMaster/modules/DebugLog.lua:97-99` and
`core/ConsumableMaster.lua:328, :288-290`; `KickCD/core/PerfSetup.lua:108` and `settings/Slash.lua:211`
plus `tests/test_coresetup.lua:360`; `LootHistory/settings/Slash.lua:111-112, :165-167`;
`PanelMaster/core/CoreSetup.lua:21` and `tests/test_vendor_sync.lua:29-31`;
`prettychat/settings/Panel.lua:182, :248`. Plus `AbsorbTracker/docs/file-index.md:100`, which repeats a
wrong coverage claim.

**Out of scope.** Comments that are merely terse or unhelpful. Prose style.

---

## C4 — a ratified deviation lives in one place and is not re-litigated

**Target.** Every addon's `docs/ARCHITECTURE.md` carries `## Documented deviations` with rows shaped
`| Rule | What differs | Why | Decided | Re-check trigger |`, where **Rule** is a `filename-§N` reference
and **Re-check trigger** is the condition that ends the deviation. `docs/pending/LEDGER.md` may hold the
reasoning and the row cites its id, but **a deviation not in the register is not ratified**. An audit
records a register row as accepted with its id and does not count it toward the MUST tally; an audit
**does** file a register row whose cited rule the standard has since changed.

**Acceptance.** Eight addons carry the section. BankLedger and LootHistory each gain a row for a Perf
decline currently recorded only in their ledgers. AbsorbTracker's four stale entries at
`docs/ARCHITECTURE.md:277-315` — the Wago omission, `AbsorbTrackerPerfDB`, lizard, and the bracket
idiom — are retired, since `savedvariables-§4`, `performance-§2`/`§10` and `toc-file` now sanction all
four. A fresh audit in each repo files zero rows that the register already carries.

**Three rows an earlier draft mapped here without covering, now named explicitly** — the acceptance
criterion above is unmeetable without them:

- **`PC-A-21`** — prettychat's record is at **`DEPENDENCIES.md:118-119`**, not in `CLAUDE.md:5-13`, and the
  substance is a `library-stack` internal contradiction: `library-stack.md:13-14` lists AceEvent and
  AceTimer as vendored while `:39` MUSTs vendoring only what is LibStub'd. No `M1-STD-*` item resolves it,
  so it is a register row citing both lines with a re-check trigger of "the next `library-stack` edit".
- **`CM-A-16`** — ConsumableMaster's within-`core/` load sequence (`ConsumableMaster.toc:48-58`, rationale
  in the TOC's own comments at `:44-47` and `:53-55`). Register row here; the rule half — that
  `toc-file-§5`'s within-section sequence is illustrative, not an ordered MUST — is `M1-STD-15` part 3.
- **`AT-A-10`** — AbsorbTracker's per-unit event frames, justified at `docs/ARCHITECTURE.md:316-331`, with
  a re-check trigger of "a client build where `RegisterUnitEvent` accepts more than two tokens". Moved
  here from `M1-STD-12`, which no longer carves a permanent exception into `events-frames-taint-§1` on one
  Info row's evidence (see C17).

**`WG-A-13` is not in this cluster.** Nothing ratifies it — no register row, no ledger entry, no in-code
rationale — so it is a genuinely unmet `debug-logging-§2` SHOULD, re-filed as a WhatGroup one-off and fixed
as code at `M4-24`: `core/DebugLogSetup.lua:95` supplies a Blizzard fetch-failure fallback for the
`NS.FONT_MONO` path handed in at `core/WhatGroup.lua:96`.

**Out of scope.** Re-deciding any deviation. This cluster moves and shapes records; it does not reverse
decisions.

---

## C5 — the root doc set and the README structure are canonical

**Target.** Every addon repo root ships **exactly three docs plus `LICENSE`**: a full `README.md`, a stub
`CLAUDE.md`, and `DEPENDENCIES.md` (`documentation-§1`/`§2`/`§7`). `CHANGELOG.md` is **forbidden at an
addon root** — the player-facing history lives in `## What's new` and `## Version History` — and
**required in a Ka0s-owned library repo**, because `testing-§10`'s versioning suite asserts against it.
The plugin's `bump-version` writes accordingly.

`README.md` carries only the twelve permitted sections, in the order enumerated in invariant 4 — H1 title,
badge row, logo, description, `## What's new`, `## Screenshots`, `## Usage`, `## How <it> works`, `## FAQ`,
`## Troubleshooting`, `## Issues and feature requests`, `## Version History`. `CLAUDE.md` is the five-item
stub, also enumerated there — H1 `# CLAUDE.md — Ka0s <Name>`, adherence line,
`## Standards compliance (read first)` as item 3, the "read the docs" pointer list, the green-gate line.

**Acceptance.**
- ConsumableMaster's root is `CLAUDE.md`, `DEPENDENCIES.md`, `LICENSE`, `README.md`, and its `CLAUDE.md:1`
  reads `# CLAUDE.md — Ka0s Consumable Master`.
- prettychat's README has no `## Unreleased` and no `## Credits` mid-order, and `CLAUDE.md`'s compliance
  section is item 3.
- WhatGroup's README has no `## Bundled libraries`.
- PanelMaster's `### Settings panel` is a `Tab | Covers` table.
- KickCD's `README.md:191` and prettychat's `README.md:116` carry no angle-bracket placeholders.
- AbsorbTracker's `## What's new in 1.9.0` and its Version History row carry the same highlights, and
  `CLAUDE.md:40-41` says **five** and lists all five: `test-cases.md`, `performance.md`,
  `perf-runs/README.md`, `automated-tests/README.md`, `automated-tests/RESULTS.md`.
- LootHistory's `CLAUDE.md` is a stub, not a 102-line agent brief.
- LibKa0s's `README.md` `## Repo layout` lists `docs/automated-tests/` and `docs/audits/`.

**Out of scope.** Rewriting README prose. Adding screenshots to unreleased addons (`PM-A-18` is correctly
advisory at 0.1.0).

---

## C7 — an exported symbol has a caller or a documented reason

**Target.** A member published on the namespace either has a production caller, or carries a one-line
comment saying why it is exported without one (a documented test seam, a public API surface). A comment
naming a caller that does not exist is a defect (C3), not a reason.

**Acceptance.** The ten cited surfaces are removed, wired, or annotated:
`AbsorbTracker` `Units.DeepCopy` / `Units.Set` (plus the wrong coverage claim at
`docs/file-index.md:100`); `BankLedger` `QualityFromLink`, `DeleteAt` and the four module helpers, with
`core/Database.lua:550`'s false caller comment corrected and `docs/ARCHITECTURE.md:139` updated;
`ConsumableMaster` `TooltipCache.pendingIDs` and `MB.IsShown`; `KickCD` `NS.Castbar` and the
`.luacheckrc:29` allowlist entry; `PanelMaster` `NS.Format` (which is also the one asymmetric member of a
seam whose comment states its member set is exactly what the addon calls); `WhatGroup` `NS.Util.format`;
`LootHistory` `media/logos/wowhead-logo.png`.

**Out of scope.** A general dead-export gate in the kit. That is worth building and is not in this plan.

---

## C10 — options pages are created lazily and registered through the library

**Target.** A page's body and any canvas widget are created on **first `OnShow`**, never in the page
builder (`options-ui-§5`). Page registration goes through the library's registry, and the library's
`CreateOptionsPanel` runs at `PLAYER_LOGIN` — there is no second, private registration path alongside it.
A page hidden when its data changed rebuilds on next open (`options-ui-§11`). Category registration is
**not** gated on `InCombatLockdown()` — `options-ui` is explicit that registration never taints and that
eager registration at load is a MUST; only panel *open* is combat-gated.

**Acceptance.**
- LootHistory: blacklisting an item from the History right-click menu with the settings window closed,
  then opening the Filters page, shows the updated list without `/reload`. (In-game smoke step.)
- KickCD: `settings/Panel.lua:546, :557-604, :607-616` and the six private page tails are gone; the
  library forwarders at `settings/OptionsSetup.lua:228-234` have callers; the combat-gated second open
  path at `core/KickCD.lua:775-790` is the only one. `settings/Panel_Render.lua:259-266` no longer
  duplicates `afterRestoreAll`.
- AbsorbTracker: `settings/Profiles.lua`'s SimpleGroup is created in `OnShow`.
- ConsumableMaster: a `settings/OptionsSetup.lua` exists and holds the seam; the three unguarded
  `LibStub("AceGUI-3.0")` calls at `settings/Panel.lua:19`, `settings/StatPriority.lua:23`,
  `settings/Category.lua:29` pass `true`.
- WhatGroup: `settings/Panel.lua:268-272`'s combat guard is removed.

**Out of scope.** Redesigning any page's layout or content.

---

## C14 — the vendored kit is the harness, not a decoration

**Target.** ConsumableMaster and KickCD load `tests/_kit/framework.lua`, `loader.lua` and `mock_base.lua`
as their registry, assertion set, source loader and base mock (`testing-§1`). prettychat's
`tests/loader.lua` wrapper survives only for the isolated-environment need the kit does not serve —
recorded as LIBKA0S-01 — and shrinks to that. No repo runs a case body at registration time.

**Acceptance.** `grep -n "_kit" tests/run.lua` resolves to a `dofile`, not a comment, in
ConsumableMaster and KickCD. Their pass counts are preserved (656 and 737 today) or the delta is
explained per case. `tests/run.lua:40-53` in KickCD no longer executes at registration.

**Out of scope.** Merging the mock surfaces. Each repo's `wow_mock.lua` extensions stay local.

---

## C16 — a test can go red

**Target.** No assertion pins only a relation between two measured values, or only that a call raised.
A zero-overhead perf assertion pins an **absolute ceiling** on the dormant arm as well as the relation.
A case whose comment claims it covers a write path exercises a write. An `assertError` case asserts on
the **message**, not merely on failure.

**Acceptance.**
- `AbsorbTracker/tests/perf.lua:228-229` gains an absolute bound on `probeOff.bytesPerIter`.
- `ConsumableMaster/tests/test_settingsui.lua:243-246` performs a write through `/cm set` and asserts the
  stored value.
- `prettychat/tests/test_defaults.lua:107-114` compares each override's conversion sequence against the
  **shipped Blizzard signature** in `GlobalStrings/`, not against arguments derived from the override
  itself. This is the case that would have caught `PC-R-01` and `PC-R-02`.
- `LibKa0s/tests/test_perf_core.lua:15-24` asserts on the message in all four arms.

**Out of scope.** A general mutation-testing pass.

---

## C19 + C24 + C28 — SavedVariables discipline

**Target.**
- **One declaration site.** Every default value is declared in `defaults/Profile.lua` (or
  `defaults/Global.lua` for account-wide) and nowhere else (`savedvariables-§2`). A schema row's `default`
  reads from that declaration rather than restating a literal.
- **One write seam.** Writes go through `Schema:Set`. Every carve-out is enumerated in the file a
  maintainer checks before writing a key directly, and a carve-out that writes the live profile and
  restores it wraps the window in a `pcall`.
- **A read does not write.** `Helpers.Get` on an unknown path returns nil without materializing parent
  tables.
- **Boot validation can fire.** The `architecture-§5` check MUST be able to report a typo'd path; a
  conjunct that is structurally never true is a dead assertion.

**Acceptance.**
- ConsumableMaster ships `defaults/Profile.lua`; `core/ConsumableMaster.lua:25`'s inline `dbDefaults`
  is gone. KickCD ships `defaults/Profile.lua` and `modules/Castbar.lua:569-588`'s second copy is
  removed. LootHistory's six `settings/Schema.lua` literals read from `defaults/Global.lua`, as
  `:109` already does for `auction.capture`.
- BankLedger's `settings/Schema.lua:124-125` names all four carve-outs, including
  `modules/SessionWindow.lua:256`, `:287` and `modules/Browser.lua:916`/`:923`.
- KickCD's `settings/Slash.lua:121-123` window is `pcall`-wrapped.
- WhatGroup's `settings/Schema.lua:216` no longer creates tables on a read.
- LootHistory's `settings/Schema.lua:194` and PanelMaster's `settings/Schema.lua:171` report a typo'd
  path; a probe row with a bad path and no default returns a non-zero count.
- AbsorbTracker's account-wide `schemaVersion` no longer defaults to the current value, so a
  freshly-materialized global runs the ladder (`defaults/Profile.lua:78` versus the reasoned `:50-56`).
- PanelMaster's `defaults/Global.lua:13` no longer seeds `schemaVersion = NS.SCHEMA_VERSION` as an AceDB
  default, which today makes the whole v1→v2 migration body unreachable for every account.

**Out of scope.** Introducing new migrations. Changing the schema's storage layout.

---

## C22 + C23 + C25 + C29 + C30 + C31 + C32 — records, config and shape

| Cluster | Target | Acceptance | Out of scope |
|---|---|---|---|
| **C22** lint config | `.luacheckrc` matches the template's exclusions and suppresses no warning class tree-wide to carry one known defect. Redundant per-file suppressions are deleted. | AbsorbTracker excludes `docs/audits/`+`docs/reviews/`, not all of `docs/`. ConsumableMaster's `241` suppression is narrowed to the one site or the defect is fixed. LootHistory's `modules/AuctionPrice.lua:1` comment is deleted. `luacheck .` stays 0/0 everywhere. | Adding new warning classes. |
| **C23** record shape | `RESULTS.md`'s complexity watch list is **two tables with header rows** (`automated-tests-§4`), and a disposition cites a live finding id. `docs/perf-runs/README.md` documents `<YYYY-MM-DD>-ingame-<label>.json` flat, a schema summary and a pointer to the library's contract (`performance-§8`). LibKa0s's release order includes the runner step. | AbsorbTracker's `RESULTS.md:64-91` is a table. LootHistory's `RESULTS.md:49` cites a finding that is not the retired `docs/complexity.md`. LootHistory's `docs/perf-runs/README.md` names the flat convention. `LibKa0s/docs/releasing.md:28-59` has a runner step. | Rewriting past `RESULTS.md` rows. |
| **C25** ARCHITECTURE sections | `docs/ARCHITECTURE.md` carries all mandated headings — Overview, Module Map, Settings Schema, Message Bus, Slash Commands, Event Subscriptions, Taint Notes, Known Limitations, plus `## Documented deviations` (C4). A section may say "there is none, because…". | `grep '^## '` in ConsumableMaster, prettychat and WhatGroup returns the full set. | Writing content for sections that have none — a one-line "there is no message bus, because…" is compliant. |
| **C29** on-notice LOC band | A file in the 1000–1500 band is the **compliant** state and is not filed as a deviation. `layout-§1` caps at 1500. | BankLedger's four files, ConsumableMaster's `tests/test_macrobar.lua` (1497) and prettychat's unshipped 23,842-line build input are not carried in a deviations table. | Splitting any file. Nothing exceeds the cap. |
| **C30** window skin | A standalone window delegates to `Core.ApplySkin` rather than restating the normative edge. Values are identical today, so nothing renders differently. | BankLedger's `modules/Browser.lua:21-34`/`:67-89` and LootHistory's `:20-33`/`:65-86` call the shared helper. | Retuning the edge. |
| **C31** packaging | `.pkgmeta`'s ignore list matches the canonical block plus every dev-only path that exists at root. | ConsumableMaster ignores `.claude/`, `.superpowers/` and (once C5 lands) no longer has a `CHANGELOG.md` to ignore. WhatGroup ignores `_dev` and lockfiles. | Changing the packaging pipeline. |
| **C32** compat routing | Deprecated APIs route through `Compat`. `GetItemInfo`/`GetItemCount` are **live retail globals**, so the rule does not squarely apply — but a comment asserting they are wrapped is a defect. | ConsumableMaster's `.luacheckrc:66` comment is corrected. `core/TooltipCache.lua:459` and `modules/Ranker.lua:88` are guarded consistently with `core/Classifier.lua:167-170`, or the inconsistency is recorded. | Wrapping live APIs in `Compat` for uniformity's sake. |

---

## C26 — preview mode

**Target.** A positionable or persistent on-screen display shows a placeholder while unlocked, and
**clears the preview and returns to live data when the display is re-locked or the preview verb is
toggled off** (`preview-mode`, bullet 3 — a MUST). A timed hold with no off verb and no lock-triggered
clear does not satisfy it.

**Acceptance.** AbsorbTracker's `/at test` either honors the announced duration by scheduling a repaint
at expiry, or drops the duration from the message; and re-locking clears the preview.
`modules/Display.lua:92-98` shows a placeholder fill while unlocked. ConsumableMaster's macro bar gains a
preview path or records a deviation with a re-check trigger.

**Out of scope.** Designing new preview artwork.

---

## The eight Highs — the fastest-moving spec in this document

These are the only items where "done" means a user-visible behavior changes. None depends on any upstream
work.

| ID | Repo | Target | Acceptance |
|---|---|---|---|
| `PC-R-01` | prettychat | `FACTION_STANDING_DECREASED_GENERIC`'s default carries exactly the conversions Blizzard passes — `"Reputation with %s decreased."` — so no `%d` is left unfilled. | A re-derived comparison of every default against `GlobalStrings/` shows each override's conversion sequence is a **positional prefix** of Blizzard's — never longer, never type-mismatched at any position (see the prefix rule below); `tests/test_defaults.lua` asserts that rule (C16). |
| `PC-R-02` | prettychat | `FACTION_STANDING_INCREASED_GUARDIAN` keeps its leading `%s` so the numeric conversion is not handed the guardian's name. | Same check. Contrast `defaults/Defaults.lua:186-189`, which is already correct. |
| `WG-R-01` | WhatGroup | `db.profile.enabled` gates the `inviteaccepted` fresh-fetch branch, not only `OnApplyToGroup`. A disabled addon captures nothing, notifies nothing and opens no popup — matching the tooltip at `settings/Schema.lua:92`. | With `enabled=false`, a live `mock.searchResults[100]` and one `inviteaccepted` event, `pendingInfo` stays nil. A case pins it, and deleting the gate turns that case red. |
| `CM-R-01` / `CM-A-25` | ConsumableMaster | `O.Refresh` never calls a nil member on the degraded path. | `loadWithSchemaDegraded()` completes with `ok=true`; a parity case covers the Options seam. |
| `CM-R-02` | ConsumableMaster | `SetAndRefresh` does not raise after a write has landed. A pcall'ing caller never sees failure over a mutation that persisted. | Same loader; `ok=true` and the written value is readable. `settings/Panel.lua:636` no longer lets an explicit nil delete a key. |
| `CM-A-32` | ConsumableMaster | A degraded install keeps all 11 host-owned verbs — `config, version, debug, perf, resync, rewritemacros, resetall, bar, priority, stat, aio, dump` minus whichever route through the library — and only `help/get/set/list/reset` degrade. | Degraded load; each host verb dispatches; `settings/Panel.lua:265-271`'s advice matches what `/cm` actually answers. |
| `PM-R-01` | PanelMaster | The slash stub (`settings/Slash.lua`, opened `:285`, returning `:316`) assigns `FormatKV`, matching the live assignment at `:381`; `/pm panel` answers on a degraded install. | TOC loaded with no `libs/LibKa0s/*`: `/pm panel audit` returns `ok=true`. A parity case pins the stub's whole member set. |

### The prefix rule — `PC-R-01` / `PC-R-02`'s acceptance criterion, corrected

**"Zero mismatches" is not achievable and, executed literally, mandates four behavior changes with no
finding behind them.** The re-derivation was run here — loading `defaults/Defaults.lua` and all 26
`GlobalStrings/` chunks under `lua5.1` — and reports **81 overrides checked, 6 conversion-sequence
mismatches**:

| Key | Override | Blizzard | Verdict |
|---|---|---|---|
| `FACTION_STANDING_DECREASED_GENERIC` | `[s,d]` | `[s]` | **unsafe** — missing argument raises (`PC-R-01`) |
| `FACTION_STANDING_INCREASED_GUARDIAN` | `[d]` | `[s,d]` | **unsafe** — a name into `%d` raises (`PC-R-02`) |
| `LOOT_DISENCHANT_CREDIT` | `[s]` | `[s,s]` | sanctioned truncation |
| `COMBATLOG_DISHONORGAIN` | `[]` | `[s]` | sanctioned truncation |
| `OPEN_LOCK_OTHER` | `[s,s]` | `[s,s,s]` | sanctioned truncation |
| `OPEN_LOCK_SELF` | `[s]` | `[s,s]` | sanctioned truncation |

The four truncations are deliberate and harmless: Lua's `string.format` ignores surplus arguments
(`string.format("a %s","x","extra")` → `"a x"`). The rule is therefore: **an override's conversion sequence
MUST be a positional prefix of Blizzard's — never longer, and never type-mismatched at any position.** The
four sanctioned keys are named here so the next reader does not "fix" them, and `M4-06`'s
`tests/test_defaults.lua` case is written to the prefix rule rather than to equality — otherwise it is red
on six rows on the day it lands.

---

## Explicitly out of scope for this entire plan

- **In-game verification.** Every smoke step in `04_EXECUTION_PLAN.md` is an instruction to the operator.
  No claim in these documents rests on a client session.
- **Any behavior change not traced to a finding.** Refactors, renames and "while we're here" cleanups.
- **Editing frozen bundles** — audits, reviews, automated-test bundles.
- **Patching `libs/` or `tests/_kit/` in place** in any consumer.
- **Adding LibKa0s to the addon roster.** It gets its own applicability list instead.
- **Persuading any addon to adopt the Perf harness.** C1's answer is that a reasoned decline is a
  compliant state, not that the five should change their minds.
- **Building a dead-export gate in the kit.** Worth doing; not in this plan. C7 is closed per repo.
- **Any release.** No version bump, tag or push is specified anywhere in this plan except the standard's
  own v2.21.0 → v2.22.0, which is a document version.
